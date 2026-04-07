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
from src.run_context import dvc_lock_digest, git_head_short, params_digest

ROOT = _ROOT
PARAMS_PATH = ROOT / "params.yaml"
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


def inject_stress_bias_train(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    sensitive_col: str,
    seed: int,
    minority_keep_fraction: float,
    mode: str,
) -> tuple[pd.DataFrame, np.ndarray]:
    """Distort training only: undersample rare sensitive level, or remove it entirely."""
    s = X_train[sensitive_col]
    rare_level = s.value_counts().idxmin()
    if mode == "remove_rare":
        keep = s != rare_level
        return (
            X_train.loc[keep].reset_index(drop=True),
            y_train[keep.values],
        )
    is_rare = (s == rare_level).values
    rare_pos = np.where(is_rare)[0]
    other_pos = np.where(~is_rare)[0]
    n_keep = max(1, int(len(rare_pos) * minority_keep_fraction))
    rng = np.random.default_rng(seed)
    kept_rare = rng.choice(rare_pos, size=n_keep, replace=False) if len(rare_pos) else np.array([], dtype=int)
    keep_idx = np.sort(np.concatenate([kept_rare, other_pos]))
    return X_train.iloc[keep_idx].reset_index(drop=True), y_train[keep_idx]


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

    stress_cfg = params.get("stress") or {}
    stress_on = stress_cfg.get("enabled") is True or os.environ.get("STRESS_BIAS", "").lower() in (
        "1",
        "true",
        "yes",
    )
    stress_note = "off"
    if stress_on:
        mode = os.environ.get("STRESS_MODE", stress_cfg.get("mode", "undersample"))
        frac = float(
            os.environ.get(
                "STRESS_MINORITY_KEEP",
                stress_cfg.get("minority_keep_fraction", 0.05),
            )
        )
        X_train, y_train = inject_stress_bias_train(
            X_train, y_train, sensitive_col, seed, frac, mode
        )
        stress_note = (
            f"remove_rare_sensitive_train" if mode == "remove_rare" else f"undersample_rare_sensitive_keep={frac}"
        )

    pipe = build_pipeline(X_train)
    model_params = params.get("model", {})
    pipe.set_params(
        clf__max_iter=int(model_params.get("max_iter", 500)),
        clf__C=float(model_params.get("C", 1.0)),
    )

    git_sha = git_head_short(ROOT)
    p_digest = params_digest(PARAMS_PATH)
    lock_digest = dvc_lock_digest(ROOT)

    with mlflow.start_run():
        mlflow.set_tags(
            {
                "git_commit": git_sha,
                "params_yaml_sha16": p_digest,
                "dvc_lock_sha16": lock_digest,
                "stress_bias": stress_note,
            }
        )
        mlflow.log_params(
            {
                "seed": seed,
                "model": model_params.get("name", "logistic_regression"),
                "data_provenance": data_provenance,
                "sensitive_column": sensitive_col,
                "pipeline_profile": params["pipeline"]["profile"],
                "stress_enabled": str(stress_on),
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

    fn = getattr(pipe, "feature_names_in_", None)
    if fn is not None:
        names = [str(x) for x in fn]
        dtypes = {str(c): str(X_val[c].dtype) for c in names if c in X_val.columns}
        schema_out = {
            "schema_version": 1,
            "feature_names": names,
            "dtypes": dtypes,
            "git_commit": git_sha,
            "params_yaml_sha16": p_digest,
            "data_provenance": data_provenance,
        }
        with open(ARTIFACTS / "feature_schema.json", "w", encoding="utf-8") as f:
            json.dump(schema_out, f, indent=2)

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
        "git_commit": git_sha,
        "params_yaml_sha16": p_digest,
        "dvc_lock_sha16": lock_digest,
        "stress_bias": stress_note,
    }
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
