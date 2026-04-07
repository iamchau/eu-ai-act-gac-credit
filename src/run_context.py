"""Reproducibility context for MLflow tags and metrics (git SHA, params digest, optional DVC files)."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


def git_head_short(cwd: Path, length: int = 12) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        return out.stdout.strip()[:length]
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return "unknown"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def params_digest(params_path: Path) -> str:
    if not params_path.is_file():
        return "missing"
    return file_sha256(params_path)


def dvc_lock_digest(root: Path) -> str:
    lock = root / "dvc.lock"
    if not lock.is_file():
        return "no_lock"
    return file_sha256(lock)
