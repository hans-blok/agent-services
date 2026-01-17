#!/usr/bin/env python3
"""Pipeline Executor Runner

Voert multi-agent pipelines uit door workflow-documenten te lezen, agents in volgorde
aan te roepen, quality gates te valideren en failures af te handelen.

Usage:
    python scripts/pipeline-executor.py --help

Voor de Pipeline Executor agent voert de runner pipeline execution uit:
    python scripts/pipeline-executor.py --pipeline-bestand <path>

Traceability:
    Schrijft execution log naar temp/pipeline-executor-<pipeline-naam>-{timestamp}.md
"""

import sys
from pathlib import Path

from pipeline_executor.frontdoor import run_frontdoor


WORKSPACE_ROOT = Path(__file__).parent.parent


def main() -> int:
    result = run_frontdoor(workspace_root=WORKSPACE_ROOT)

    if result.success:
        print(f"OK: {result.message}")
        if result.execution_log is not None:
            print(f"Execution log: {result.execution_log.relative_to(WORKSPACE_ROOT).as_posix()}")
        return 0

    print(f"ERROR: {result.message}", file=sys.stderr)
    if result.execution_log is not None:
        try:
            rel = result.execution_log.relative_to(WORKSPACE_ROOT).as_posix()
        except ValueError:
            rel = str(result.execution_log)
        print(f"Execution log: {rel}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
