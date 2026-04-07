"""
Gate B — Explainability: SHAP summary for validation set; writes report + metrics JSON.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import joblib
import numpy as np
import pandas as pd
import shap
import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "artifacts" / "shap_report.md"
METRICS_PATH = ROOT / "metrics" / "shap_gate.json"


def main() -> int:
    with open(ROOT / "params.yaml", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    min_top = float(params["gates"]["shap"]["min_top_mean_abs_shap"])

    model = joblib.load(ROOT / "artifacts" / "model.joblib")
    X_val = pd.read_csv(ROOT / "artifacts" / "X_val.csv")
    X_bg = pd.read_csv(ROOT / "artifacts" / "X_background.csv")

    def predict_proba_positive(X: np.ndarray | pd.DataFrame) -> np.ndarray:
        p = model.predict_proba(X)
        return p[:, 1] if p.shape[1] > 1 else p[:, 0]

    # Masker from background for mixed feature spaces
    masker = shap.maskers.Independent(X_bg)
    explainer = shap.Explainer(predict_proba_positive, masker=masker)
    shap_vals = explainer(X_val)

    # Mean |SHAP| per feature (class 0 slice if multi-output)
    sv = shap_vals.values
    if sv.ndim == 3:
        sv = sv[:, :, 0]
    mean_abs = np.abs(sv).mean(axis=0)
    names = list(X_val.columns)
    order = np.argsort(-mean_abs)
    top_name = names[order[0]]
    top_val = float(mean_abs[order[0]])

    lines = [
        "# SHAP summary (validation)",
        "",
        f"- Top feature by mean |SHAP|: **{top_name}** = {top_val:.6f}",
        "",
        "| Feature | Mean |SHAP| |",
        "|---------|---------------|",
    ]
    for i in order[:15]:
        lines.append(f"| {names[i]} | {mean_abs[i]:.6f} |")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    passed = top_val >= min_top
    out = {
        "top_feature": top_name,
        "top_mean_abs_shap": top_val,
        "min_required": min_top,
        "gate_passed": passed,
    }
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

    if not passed:
        print("SHAP GATE FAILED: top_mean_abs_shap below threshold.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
