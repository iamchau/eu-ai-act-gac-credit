"""Normalize **`path`** inline code in Markdown (bold + code spans).

Default: docs/thesis/MANUSCRIPT.md. Pass more paths relative to repo root:

  python scripts/fix_manuscript_inline_md.py PROJECT_PLAN.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def fix_text(text: str) -> tuple[str, int]:
    def repl(m: re.Match[str]) -> str:
        return f"**`{m.group(1)}`**"

    p1 = r"`\*\*([^`]+)\*\*`"
    p2 = r"`\*\*([^`]+)`\*\*"
    p3 = r"\*\*`([^`]+)\*\*`"

    total = 0
    while True:
        text, n1 = re.subn(p1, repl, text)
        text, n2 = re.subn(p2, repl, text)
        total += n1 + n2
        if n1 + n2 == 0:
            break
    text, n3 = re.subn(p3, repl, text)
    total += n3
    return text, total


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    rels = sys.argv[1:] if len(sys.argv) > 1 else ["docs/thesis/MANUSCRIPT.md"]
    grand = 0
    for rel in rels:
        path = root / rel
        text = path.read_text(encoding="utf-8")
        text, n = fix_text(text)
        path.write_text(text, encoding="utf-8")
        grand += n
        print(f"{rel}: {n}")
    print(f"total replacements: {grand}")


if __name__ == "__main__":
    main()
