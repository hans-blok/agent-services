#!/usr/bin/env python3
"""Moeder Runner

Eén runner met twee lagen:
- Frontdoor: intent parsing + output formatting
- Core: operation execution + policy gates

Deze runner automatiseert herhaalbare stappen zonder AI-interactie.

Usage:
    python scripts/moeder.py --help

Voor de Moeder agent voert de runner één operatie per run uit:
    beheer-git | configureer-github | orden-workspace | schrijf-beleid | 
    zet-agent-boundary | valideer-governance

Traceability:
    Standaard schrijft de runner een trace artefact weg in temp/.
"""

import sys
from pathlib import Path

from moeder.frontdoor import run_frontdoor


WORKSPACE_ROOT = Path(__file__).parent.parent


def main() -> int:
    result = run_frontdoor(workspace_root=WORKSPACE_ROOT)

    if result.success:
        print(f"OK: {result.message}")
        if result.trace_path is not None:
            print(f"Trace: {result.trace_path.relative_to(WORKSPACE_ROOT).as_posix()}")
        return 0

    print(f"ERROR: {result.message}", file=sys.stderr)
    if result.trace_path is not None:
        try:
            rel = result.trace_path.relative_to(WORKSPACE_ROOT).as_posix()
        except ValueError:
            rel = str(result.trace_path)
        print(f"Trace: {rel}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
