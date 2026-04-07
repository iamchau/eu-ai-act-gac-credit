"""
FastAPI scoring service for the trained sklearn Pipeline (artifacts/model.joblib).
Thesis / portfolio slice — not production banking infrastructure.

Extensions: optional API key, max body size, JSON access logs, feature_schema.json (see docs/deployment/TECHNICAL_EXTENSIONS.md).
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import joblib
import pandas as pd
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.run_context import git_head_short, params_digest

MODEL_PATH = Path(os.environ.get("MODEL_PATH", str(_ROOT / "artifacts" / "model.joblib")))
SCHEMA_PATH = Path(os.environ.get("SCHEMA_PATH", str(_ROOT / "artifacts" / "feature_schema.json")))
PARAMS_PATH = _ROOT / "params.yaml"

_pipeline = None
_feature_names: list[str] | None = None
_schema: dict[str, Any] | None = None


def _env_int(name: str, default: int) -> int:
    v = os.environ.get(name)
    if v is None or v == "":
        return default
    return int(v)


def _log_json_enabled() -> bool:
    return os.environ.get("LOG_JSON_ACCESS", "1").strip().lower() in ("1", "true", "yes", "on")


def load_model() -> None:
    global _pipeline, _feature_names
    if not MODEL_PATH.is_file():
        raise RuntimeError(
            f"Model not found at {MODEL_PATH}. Run `python src/train.py` first, "
            "or set MODEL_PATH and ensure the file exists (e.g. docker-compose mount)."
        )
    _pipeline = joblib.load(MODEL_PATH)
    fn = getattr(_pipeline, "feature_names_in_", None)
    if fn is not None:
        _feature_names = [str(x) for x in fn]
    else:
        _feature_names = None


def load_schema() -> None:
    global _schema
    if not SCHEMA_PATH.is_file():
        _schema = None
        return
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        _schema = json.load(f)
    if _feature_names is not None and _schema.get("feature_names"):
        sfn = [str(x) for x in _schema["feature_names"]]
        if set(sfn) != set(_feature_names):
            print(
                json.dumps(
                    {
                        "event": "schema_model_mismatch",
                        "schema_features": sfn,
                        "model_features": _feature_names,
                    }
                ),
                flush=True,
            )


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    load_schema()
    yield


app = FastAPI(
    title="GaC Credit - scoring API (thesis demo)",
    description="Serves sklearn pipeline from train.py; illustrative deployment only.",
    version="0.2.0",
    lifespan=lifespan,
)


class LimitBodySizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_bytes: int):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next):
        if request.method == "POST" and request.url.path.rstrip("/").endswith("/predict"):
            cl = request.headers.get("content-length")
            if cl:
                try:
                    if int(cl) > self.max_bytes:
                        return JSONResponse(
                            {
                                "detail": "Request body too large",
                                "max_bytes": self.max_bytes,
                            },
                            status_code=413,
                        )
                except ValueError:
                    pass
        return await call_next(request)


class JsonAccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not _log_json_enabled():
            return await call_next(request)
        rid = str(uuid.uuid4())
        request.state.request_id = rid
        t0 = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - t0) * 1000, 3)
        line = {
            "event": "http_access",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "request_id": rid,
        }
        print(json.dumps(line), flush=True)
        response.headers["X-Request-ID"] = rid
        return response


# Last added = outermost: access log wraps limit so 413 from limit is still logged.
app.add_middleware(LimitBodySizeMiddleware, max_bytes=_env_int("MAX_BODY_BYTES", 1048576))
app.add_middleware(JsonAccessLogMiddleware)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": _pipeline is not None}


@app.get("/version")
def version() -> dict:
    git_sha = os.environ.get("GIT_COMMIT", git_head_short(_ROOT))
    p_sha = os.environ.get("PARAMS_SHA16")
    if not p_sha and PARAMS_PATH.is_file():
        p_sha = params_digest(PARAMS_PATH)
    out: dict = {
        "git_commit": git_sha,
        "params_yaml_sha16": p_sha or "unknown",
        "model_path": str(MODEL_PATH.resolve()),
        "schema_path": str(SCHEMA_PATH.resolve()) if SCHEMA_PATH.is_file() else None,
        "serving": "fastapi",
    }
    return out


def require_predict_key(x_api_key: str | None = Header(None, alias="X-API-Key")) -> None:
    expected = os.environ.get("SERVING_API_KEY", "").strip()
    if not expected:
        return
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key")


class PredictRequest(BaseModel):
    """One or more rows with the same columns as training features X."""

    records: list[dict[str, float | int | str | None]] = Field(
        ...,
        min_length=1,
        description="Feature rows; column names must match training data.",
    )


def _expected_columns() -> list[str] | None:
    if _schema and _schema.get("feature_names"):
        return [str(x) for x in _schema["feature_names"]]
    return _feature_names


@app.post("/predict")
def predict(
    body: PredictRequest,
    _: None = Depends(require_predict_key),
) -> dict:
    if _pipeline is None:
        raise HTTPException(503, "Model not loaded")
    df = pd.DataFrame(body.records)
    cols = _expected_columns()
    if cols is not None:
        missing = set(cols) - set(df.columns)
        extra = set(df.columns) - set(cols)
        if missing:
            raise HTTPException(400, f"Missing columns: {sorted(missing)}")
        if extra:
            raise HTTPException(400, f"Unknown columns: {sorted(extra)}")
        df = df[cols]
    try:
        proba = _pipeline.predict_proba(df)
        pred = _pipeline.predict(df)
    except Exception as e:
        raise HTTPException(400, f"Prediction failed: {e!s}") from e
    n = len(df)
    out = []
    for i in range(n):
        p_pos = float(proba[i, 1]) if proba.shape[1] > 1 else float(proba[i, 0])
        out.append(
            {
                "prediction": int(pred[i]),
                "proba_positive": p_pos,
            }
        )
    return {"n_rows": n, "results": out}


def main() -> None:
    import uvicorn

    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run("serving.app:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
