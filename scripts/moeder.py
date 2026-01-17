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
- Standaard schrijft de runner een trace artefact weg in temp/.
- Bij succesvolle operaties met aangepaste artefacten geeft de runner een
  expliciete herinnering om de wijziging te loggen in de workspace state
  (`state-<workspace-naam>.md`) conform
  `artefacten/0-governance/doctrine-workspace-state-en-legitimiteit.md`.
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
        # Indien er artefacten zijn aangeraakt, herinner aan loggingplicht in state
        if getattr(result, "artifacts", None):
            print(
                "Let op: log deze wijziging in de workspace state "
                "(state-<workspace-naam>.md) volgens "
                "artefacten/0-governance/doctrine-workspace-state-en-legitimiteit.md."
            )
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
