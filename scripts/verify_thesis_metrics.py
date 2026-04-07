"""Verify committed metrics JSON used by the thesis parses and key fields are present.

Run from repository root: python scripts/verify_thesis_metrics.py
Exit 0 on success; non-zero if files missing or invalid.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> dict:
    p = ROOT / "metrics" / name
    if not p.is_file():
        print(f"MISSING: {p}", file=sys.stderr)
        sys.exit(1)
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ec = _load("experiment_comparison.json")
    assert "git_commit" in ec and "profiles" in ec
    std = ec["profiles"]["standard"]["train_metrics"]
    gov = ec["profiles"]["governed"]["train_metrics"]
    assert std["accuracy"] == gov["accuracy"]
    print("experiment_comparison.json OK")
    print(f"  git_commit: {ec['git_commit']}")
    print(f"  standard wall_time_s: {ec['profiles']['standard']['wall_time_seconds']}")
    print(f"  governed wall_time_s: {ec['profiles']['governed']['wall_time_seconds']}")

    ho = _load("human_oversight_latency.json")
    for k in ("human_oversight_latency_seconds", "workflow_run_url", "gates_completed_epoch", "approval_epoch"):
        assert k in ho, k
    print("human_oversight_latency.json OK")
    print(f"  latency_s: {ho['human_oversight_latency_seconds']}")

    demo = ROOT / "metrics" / "fairness_gate_subrq1_threshold_demo_fail.json"
    if demo.is_file():
        with demo.open(encoding="utf-8") as f:
            d = json.load(f)
        assert d.get("gate_passed") is False
        print("fairness_gate_subrq1_threshold_demo_fail.json OK")
    else:
        print("fairness_gate_subrq1_threshold_demo_fail.json (optional demo) not found — skip")

    print("\nCompare thesis Chapter 6 tables to these values before PDF lock.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
