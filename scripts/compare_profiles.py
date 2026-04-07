"""
P3 — Run standard vs governed on the same repo state; write metrics/experiment_comparison.json
for the thesis evaluation chapter (same seed in params.yaml).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
OUT = ROOT / "metrics" / "experiment_comparison.json"


def run(cmd: list[str], env: dict) -> tuple[int, float]:
    t0 = time.perf_counter()
    r = subprocess.run(cmd, cwd=ROOT, env=env, check=False)
    dt = time.perf_counter() - t0
    return r.returncode, dt


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    base = os.environ.copy()
    base["PYTHONPATH"] = str(ROOT)

    results: dict = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        or "unknown",
        "profiles": {},
    }

    # Standard: train only
    env_s = base | {"PIPELINE_PROFILE": "standard"}
    code_s, wall_s = run([PY, "src/train.py"], env_s)
    train_s = read_json(ROOT / "metrics" / "train_metrics.json")
    results["profiles"]["standard"] = {
        "exit_code": code_s,
        "wall_time_seconds": round(wall_s, 3),
        "train_metrics": train_s,
        "gates_run": False,
    }

    # Governed: train + gates
    env_g = base | {"PIPELINE_PROFILE": "governed"}
    t0 = time.perf_counter()
    code_tr = subprocess.run([PY, "src/train.py"], cwd=ROOT, env=env_g, check=False).returncode
    code_ff = subprocess.run([PY, "src/gate_fairness.py"], cwd=ROOT, env=env_g, check=False).returncode
    code_sh = subprocess.run([PY, "src/gate_shap.py"], cwd=ROOT, env=env_g, check=False).returncode
    wall_g = time.perf_counter() - t0

    train_g = read_json(ROOT / "metrics" / "train_metrics.json")
    gov_exit = 0 if (code_tr == 0 and code_ff == 0 and code_sh == 0) else 1
    results["profiles"]["governed"] = {
        "exit_code": gov_exit,
        "wall_time_seconds": round(wall_g, 3),
        "train_metrics": train_g,
        "fairness_gate": read_json(ROOT / "metrics" / "fairness_gate.json"),
        "shap_gate": read_json(ROOT / "metrics" / "shap_gate.json"),
        "gates_run": True,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))
    print(f"\nWrote {OUT.relative_to(ROOT)}")
    return 0 if gov_exit == 0 and code_s == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
