"""
Minimal training run: South German Credit (file or OpenML) + sklearn + MLflow + DVC metrics JSON.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import mlflow
import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_openml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = ROOT / "metrics" / "train_metrics.json"


def load_params() -> dict:
    path = ROOT / "params.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _detect_target_column(df: pd.DataFrame) -> str:
    target_candidates = {"class", "target", "credit", "risk", "label"}
    for c in df.columns:
        if str(c).lower() in target_candidates:
            return c
    return str(df.columns[-1])


def load_xy(params: dict) -> tuple[pd.DataFrame, pd.Series, str]:
    """Return X, y, and a short provenance label for MLflow."""
    raw = params["data"]["raw_csv"]
    raw_path = ROOT / raw if not Path(raw).is_absolute() else Path(raw)

    if raw_path.exists():
        df = pd.read_csv(raw_path)
        tcol = _detect_target_column(df)
        y = df[tcol]
        X = df.drop(columns=[tcol])
        return X, y, f"csv:{raw_path.name}"

    # OpenML "credit-g" = Statlog German Credit (~1000 rows). Use for pipeline dev.
    # For thesis experiments, place the South German Credit UPDATE CSV at data/raw/ (see README).
    bunch = fetch_openml(name="credit-g", version=1, as_frame=True)
    return bunch.data, bunch.target, "openml:credit-g (Statlog German Credit; dev fallback)"


def build_pipeline(X: pd.DataFrame) -> Pipeline:
    numeric = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]

    transformers = []
    if numeric:
        transformers.append(("num", StandardScaler(), numeric))
    if categorical:
        enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        transformers.append(("cat", enc, categorical))
    if not transformers:
        raise ValueError("No features after load; check dataset.")

    pre = ColumnTransformer(transformers)

    return Pipeline(
        steps=[
            ("prep", pre),
            (
                "clf",
                LogisticRegression(
                    max_iter=500,
                    C=1.0,
                    solver="lbfgs",
                    random_state=42,
                ),
            ),
        ]
    )


def main() -> int:
    params = load_params()
    seed = int(params.get("seed", 42))
    mlflow.set_tracking_uri(params["mlflow"]["tracking_uri"])
    mlflow.set_experiment(params["mlflow"]["experiment_name"])

    X, y, data_provenance = load_xy(params)
    y_codes = pd.Categorical(y).codes
    if len(np.unique(y_codes)) < 2:
        print("Target has a single class; check dataset.", file=sys.stderr)
        return 1

    X_train, X_val, y_train, y_val = train_test_split(
        X, y_codes, test_size=0.25, random_state=seed, stratify=y_codes
    )

    pipe = build_pipeline(X_train)
    model_params = params.get("model", {})
    pipe.set_params(
        clf__max_iter=int(model_params.get("max_iter", 500)),
        clf__C=float(model_params.get("C", 1.0)),
    )

    with mlflow.start_run():
        mlflow.log_params(
            {
                "seed": seed,
                "model": model_params.get("name", "logistic_regression"),
                "data_provenance": data_provenance,
            }
        )
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_val)
        proba = pipe.predict_proba(X_val)

        acc = float(accuracy_score(y_val, pred))
        metrics_out: dict[str, float] = {"accuracy": acc}
        if proba.shape[1] == 2:
            try:
                metrics_out["roc_auc"] = float(roc_auc_score(y_val, proba[:, 1]))
            except ValueError:
                pass

        mlflow.log_metrics(metrics_out)
        mlflow.sklearn.log_model(pipe, name="model")

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    out = {
        **metrics_out,
        "n_train": int(len(X_train)),
        "n_val": int(len(X_val)),
        "seed": seed,
    }
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
