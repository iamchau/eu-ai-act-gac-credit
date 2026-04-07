"""
Training run: South German Credit (CSV / UCI .asc / OpenML fallback) + sklearn + MLflow + audit artifacts for gates.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import joblib
import mlflow
import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.data_loading import load_params, load_xy_from_config

ROOT = _ROOT
METRICS_PATH = ROOT / "metrics" / "train_metrics.json"
ARTIFACTS = ROOT / "artifacts"


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
    profile = os.environ.get("PIPELINE_PROFILE")
    if not profile:
        profile = params.get("pipeline", {}).get("profile", "governed")
    params.setdefault("pipeline", {})["profile"] = profile

    seed = int(params.get("seed", 42))
    mlflow.set_tracking_uri(params["mlflow"]["tracking_uri"])
    mlflow.set_experiment(params["mlflow"]["experiment_name"])

    X, y, data_provenance = load_xy_from_config(params)
    y_codes = pd.Categorical(y).codes
    if len(np.unique(y_codes)) < 2:
        print("Target has a single class; check dataset.", file=sys.stderr)
        return 1

    sensitive_col = params["gates"]["fairness"]["sensitive_column"]
    if sensitive_col not in X.columns:
        fb = params["gates"]["fairness"].get("sensitive_column_fallback", "personal_status")
        if fb in X.columns:
            sensitive_col = fb
        else:
            print(
                f"Sensitive column not in features. Tried {sensitive_col!r} and {fb!r}. "
                f"Columns: {list(X.columns)}",
                file=sys.stderr,
            )
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
                "sensitive_column": sensitive_col,
                "pipeline_profile": params["pipeline"]["profile"],
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

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, ARTIFACTS / "model.joblib")

    proba_pos = proba[:, 1] if proba.shape[1] > 1 else proba[:, 0]
    audit = pd.DataFrame(
        {
            "y_true": y_val,
            "y_pred": pred,
            "proba_pos": proba_pos,
            "sensitive": X_val[sensitive_col].astype(float).values,
        }
    )
    audit.to_csv(ARTIFACTS / "val_audit.csv", index=False)
    X_val.to_csv(ARTIFACTS / "X_val.csv", index=False)

    bg_n = int(params["gates"]["shap"]["background_samples"])
    X_bg = X_train.sample(n=min(bg_n, len(X_train)), random_state=seed)
    X_bg.to_csv(ARTIFACTS / "X_background.csv", index=False)

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    out = {
        **metrics_out,
        "n_train": int(len(X_train)),
        "n_val": int(len(X_val)),
        "seed": seed,
        "data_provenance": data_provenance,
        "pipeline_profile": params["pipeline"]["profile"],
    }
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
