"""Load South German Credit from UCI .asc, CSV, or OpenML credit-g fallback (shared by train and gates)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_params() -> dict:
    with open(ROOT / "params.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def detect_target_column(df: pd.DataFrame) -> str:
    target_candidates = {"class", "target", "credit", "risk", "label", "kredit", "credit_risk"}
    for c in df.columns:
        if str(c).lower() in target_candidates:
            return c
    return str(df.columns[-1])


def load_xy_from_config(params: dict) -> tuple[pd.DataFrame, pd.Series, str]:
    """Return X, y, provenance string."""
    raw_csv = params["data"]["raw_csv"]
    raw_asc = params["data"].get("raw_asc", "data/raw/SouthGermanCredit.asc")
    csv_path = ROOT / raw_csv if not Path(raw_csv).is_absolute() else Path(raw_csv)
    asc_path = ROOT / raw_asc if not Path(raw_asc).is_absolute() else Path(raw_asc)

    if csv_path.exists():
        df = pd.read_csv(csv_path)
        tcol = detect_target_column(df)
        y = df[tcol]
        X = df.drop(columns=[tcol])
        return X, y, f"csv:{csv_path.name}"

    if asc_path.exists():
        df = pd.read_csv(asc_path, sep=r"\s+", engine="python")
        tcol = detect_target_column(df)
        y = df[tcol]
        X = df.drop(columns=[tcol])
        return X, y, f"uci-asc:{asc_path.name}"

    from sklearn.datasets import fetch_openml

    bunch = fetch_openml(name="credit-g", version=1, as_frame=True)
    return bunch.data, bunch.target, "openml:credit-g (Statlog German Credit; dev fallback)"
