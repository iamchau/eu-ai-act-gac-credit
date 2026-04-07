#!/usr/bin/env python3
"""
Smoke test for the scoring API: GET /health, GET /ready, GET /version, POST /predict.
Requires trained artifacts (model.joblib; feature_schema.json recommended).

Usage (from repo root, API running on 8080):
  python scripts/smoke_serving.py
  python scripts/smoke_serving.py --base-url http://127.0.0.1:8080
  set SERVING_API_KEY=secret && python scripts/smoke_serving.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _req(
    method: str,
    url: str,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, bytes]:
    h = dict(headers or {})
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.getcode(), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def main() -> int:
    ap = argparse.ArgumentParser(description="Smoke test serving API")
    ap.add_argument("--base-url", default=os.environ.get("SMOKE_BASE_URL", "http://127.0.0.1:8080"))
    ap.add_argument("--artifacts", type=Path, default=ROOT / "artifacts")
    args = ap.parse_args()
    base = args.base_url.rstrip("/")
    key = os.environ.get("SERVING_API_KEY", "").strip()

    h_code, h_body = _req("GET", f"{base}/health")
    print("GET /health", h_code, h_body.decode()[:200])
    if h_code != 200:
        return 1

    r_code, r_body = _req("GET", f"{base}/ready")
    print("GET /ready", r_code, r_body.decode()[:300])
    if r_code != 200:
        return 1

    v_code, v_body = _req("GET", f"{base}/version")
    print("GET /version", v_code, v_body.decode()[:300])
    if v_code != 200:
        return 1

    schema_path = args.artifacts / "feature_schema.json"
    if schema_path.is_file():
        with open(schema_path, encoding="utf-8") as f:
            schema = json.load(f)
        names = [str(x) for x in schema["feature_names"]]
        dtypes = schema.get("dtypes") or {}
        row: dict = {}
        for n in names:
            dt = str(dtypes.get(n, "float64")).lower()
            if "int" in dt:
                row[n] = 0
            elif "float" in dt or "double" in dt:
                row[n] = 0.0
            else:
                row[n] = 0.0
    else:
        print("WARN: artifacts/feature_schema.json missing; using single dummy column (may 400).", file=sys.stderr)
        row = {"dummy": 0.0}

    payload = json.dumps({"records": [row]}).encode("utf-8")
    ph = {"Content-Type": "application/json"}
    if key:
        ph["X-API-Key"] = key
    p_code, p_body = _req("POST", f"{base}/predict", data=payload, headers=ph)
    print("POST /predict", p_code, p_body.decode()[:500])
    return 0 if p_code == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main())
