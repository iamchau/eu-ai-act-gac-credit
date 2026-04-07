"""
Gate A — Fairness: equalized odds difference vs threshold (non-zero exit = block deploy).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pandas as pd
import yaml
from fairlearn.metrics import equalized_odds_difference

ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = ROOT / "metrics" / "fairness_gate.json"


def main() -> int:
    with open(ROOT / "params.yaml", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    max_diff = float(params["gates"]["fairness"]["max_equalized_odds_difference"])

    audit = pd.read_csv(ROOT / "artifacts" / "val_audit.csv")
    y_true = audit["y_true"].values
    y_pred = audit["y_pred"].values
    sens = audit["sensitive"].values

    eod = float(equalized_odds_difference(y_true, y_pred, sensitive_features=sens))
    abs_eod = abs(eod)

    passed = abs_eod <= max_diff
    out = {
        "equalized_odds_difference": eod,
        "abs_equalized_odds_difference": abs_eod,
        "max_allowed": max_diff,
        "gate_passed": passed,
    }
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

    if not passed:
        print(
            f"FAIRNESS GATE FAILED: |equalized_odds_difference|={abs_eod:.4f} > {max_diff}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
