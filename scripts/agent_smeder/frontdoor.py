from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from agent_smeder.core import PolicyError, execute_operation


@dataclass(frozen=True)
class FrontdoorResult:
    success: bool
    message: str
    trace_path: Path | None


def _timestamp_for_filename(now: datetime | None = None) -> str:
    now = now or datetime.now()
    return now.strftime("%y%m%d-%H-%M-%S")


def _write_trace(
    *,
    workspace_root: Path,
    operation: str,
    agent_name: str,
    capability_boundary: str,
    doel: str | None,
    domein: str | None,
    success: bool,
    message: str,
    artifacts: list[Path],
    value_stream: str | None = None,
) -> Path:
    temp_dir = workspace_root / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    trace_path = temp_dir / f"agent-smeder-trace-{_timestamp_for_filename()}.md"

    lines: list[str] = []
    lines.append("# Agent Smeder Trace\n")
    lines.append(f"- operation: {operation}\n")
    lines.append(f"- agent-naam: {agent_name}\n")
    lines.append(f"- success: {str(success).lower()}\n")
    lines.append(f"- message: {message}\n")
    lines.append("\n## Input\n")
    lines.append(f"- capability-boundary: {capability_boundary}\n")
    if doel is not None:
        lines.append(f"- doel: {doel}\n")
    if domein is not None:
        lines.append(f"- domein: {domein}\n")
    if value_stream is not None:
        lines.append(f"- value-stream: {value_stream}\n")

    lines.append("\n## Artifacts\n")
    if artifacts:
        for path in artifacts:
            try:
                rel = path.relative_to(workspace_root)
                lines.append(f"- {rel.as_posix()}\n")
            except ValueError:
                # Path is not relative to workspace_root
                lines.append(f"- {str(path)}\n")
    else:
        lines.append("- (geen)\n")

    trace_path.write_text("".join(lines), encoding="utf-8")
    return trace_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Agent Smeder runner (frontdoor). Orkestreert operations met policy gates."
        )
    )

    parser.add_argument(
        "operation",
        choices=["init-skeleton", "design-prompt", "write-role", "write-runner"],
        help="Welke operatie uitvoeren",
    )

    parser.add_argument(
        "--agent-naam",
        required=True,
        help="Unieke identifier (lowercase met hyphens)",
    )

    parser.add_argument(
        "--capability-boundary",
        required=True,
        help="De expliciete afbakening in één zin",
    )

    parser.add_argument("--doel", help="Wat de agent doet in één zin")
    parser.add_argument("--domein", help="Kennisgebied of specialisatie")
    parser.add_argument(
        "--value-stream",
        help=(
            "Primaire value stream voor plaatsing. In bronrepo's (AGENTS_SOURCE_REPO=true) "
            "schrijft Smeder prompts naar exports/<value-stream>/prompts/."
        ),
    )

    parser.add_argument(
        "--no-trace",
        action="store_true",
        help="Schrijf geen trace artefact weg",
    )

    return parser


def run_frontdoor(*, workspace_root: Path, argv: list[str] | None = None) -> FrontdoorResult:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        result = execute_operation(
            workspace_root=workspace_root,
            operation=args.operation,
            agent_name=args.agent_naam,
            capability_boundary=args.capability_boundary,
            doel=args.doel,
            domein=args.domein,
            value_stream=args.value_stream,
        )

        trace_path = None
        if not args.no_trace:
            trace_path = _write_trace(
                workspace_root=workspace_root,
                operation=args.operation,
                agent_name=args.agent_naam,
                capability_boundary=args.capability_boundary,
                doel=args.doel,
                domein=args.domein,
                value_stream=args.value_stream,
                success=result.success,
                message=result.message,
                artifacts=result.artifacts,
            )

        return FrontdoorResult(success=True, message=result.message, trace_path=trace_path)

    except PolicyError as exc:
        trace_path = None
        if not args.no_trace:
            trace_path = _write_trace(
                workspace_root=workspace_root,
                operation=args.operation,
                agent_name=args.agent_naam,
                capability_boundary=args.capability_boundary,
                doel=args.doel,
                domein=args.domein,
                value_stream=args.value_stream,
                success=False,
                message=str(exc),
                artifacts=[],
            )
        return FrontdoorResult(success=False, message=str(exc), trace_path=trace_path)
