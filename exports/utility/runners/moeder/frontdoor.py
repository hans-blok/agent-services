from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from moeder.core import PolicyError, execute_operation


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
    opdracht: str,
    check_only: bool,
    scope: str | None,
    success: bool,
    message: str,
    artifacts: list[Path],
) -> Path:
    temp_dir = workspace_root / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    trace_path = temp_dir / f"moeder-trace-{_timestamp_for_filename()}.md"

    lines: list[str] = []
    lines.append("# Moeder Trace\n")
    lines.append(f"- operation: {operation}\n")
    lines.append(f"- success: {str(success).lower()}\n")
    lines.append(f"- message: {message}\n")
    lines.append("\n## Input\n")
    lines.append(f"- opdracht: {opdracht}\n")
    lines.append(f"- check-only: {str(check_only).lower()}\n")
    if scope is not None:
        lines.append(f"- scope: {scope}\n")

    lines.append("\n## Artifacts\n")
    if artifacts:
        for path in artifacts:
            try:
                rel = path.relative_to(workspace_root)
                lines.append(f"- {rel.as_posix()}\n")
            except ValueError:
                lines.append(f"- {str(path)}\n")
    else:
        lines.append("- (geen)\n")

    trace_path.write_text("".join(lines), encoding="utf-8")
    return trace_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Moeder runner (frontdoor). Orkestreert workspace ordening operaties.",
        epilog="""
Operaties (zie charter.moeder.md v2.2):
  1. beheer-git          - Repository beheer (commits, branches, .gitignore, hooks)
  2. configureer-github  - GitHub publicatie en configuratie  
  3. orden-workspace     - Workspace structuur ordenen
  4. schrijf-beleid      - Beleid genereren bij nieuwe workspace
  5. zet-agent-boundary  - Agent boundary definitie (voor handoff naar Agent Smeder)
  6. valideer-governance - Governance compliance validatie
  7. fetch-agents        - Agents ophalen uit agent-services (LET OP: overschrijft bestaande!)

Kerntaak 7 (beheer-workspace-state) is conversationeel - geen runner.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "operation",
        choices=[
            "beheer-git",
            "configureer-github",
            "orden-workspace",
            "schrijf-beleid",
            "zet-agent-boundary",
            "valideer-governance",
            "fetch-agents",
        ],
        help="Welke operatie uitvoeren",
    )

    parser.add_argument(
        "--opdracht",
        type=str,
        required=True,
        help="Beschrijving van de gewenste actie",
    )

    parser.add_argument(
        "--check-only",
        action="store_true",
        default=False,
        help="Alleen analyseren, geen wijzigingen",
    )

    parser.add_argument(
        "--scope",
        type=str,
        default=None,
        help="Beperking tot deelgebied (bijv. structure, names, markdown, gitignore)",
    )

    # Specifieke parameters voor zet-agent-boundary
    parser.add_argument(
        "--aanleiding",
        type=str,
        default=None,
        help="Waarom is deze agent nodig (voor zet-agent-boundary)",
    )

    parser.add_argument(
        "--gewenste-capability",
        type=str,
        default=None,
        help="Wat moet de agent kunnen (voor zet-agent-boundary)",
    )

    # Specifieke parameters voor fetch-agents
    parser.add_argument(
        "--value-stream",
        type=str,
        default=None,
        help="Value stream voor agents (voor fetch-agents, verplicht)",
    )

    parser.add_argument(
        "--branch",
        type=str,
        default="main",
        help="Branch van agent-services (voor fetch-agents, default: main)",
    )

    parser.add_argument(
        "--agent-services-url",
        type=str,
        default="https://github.com/hans-blok/agent-services.git",
        help="URL van agent-services repository (voor fetch-agents)",
    )

    parser.add_argument(
        "--include-runners",
        action="store_true",
        default=True,
        help="Ook runners ophalen (voor fetch-agents, default: true)",
    )

    return parser


def run_frontdoor(*, workspace_root: Path) -> FrontdoorResult:
    parser = build_parser()
    args = parser.parse_args()

    operation: str = args.operation
    opdracht: str = args.opdracht
    check_only: bool = args.check_only
    scope: str | None = args.scope
    aanleiding: str | None = args.aanleiding
    gewenste_capability: str | None = args.gewenste_capability
    value_stream: str | None = args.value_stream
    branch: str = args.branch
    agent_services_url: str = args.agent_services_url
    include_runners: bool = args.include_runners

    try:
        result = execute_operation(
            workspace_root=workspace_root,
            operation=operation,
            opdracht=opdracht,
            check_only=check_only,
            scope=scope,
            aanleiding=aanleiding,
            gewenste_capability=gewenste_capability,
            value_stream=value_stream,
            branch=branch,
            agent_services_url=agent_services_url,
            include_runners=include_runners,
        )

        trace_path = _write_trace(
            workspace_root=workspace_root,
            operation=operation,
            opdracht=opdracht,
            check_only=check_only,
            scope=scope,
            success=result.success,
            message=result.message,
            artifacts=result.artifacts,
        )

        return FrontdoorResult(
            success=result.success,
            message=result.message,
            trace_path=trace_path,
        )

    except PolicyError as exc:
        trace_path = _write_trace(
            workspace_root=workspace_root,
            operation=operation,
            opdracht=opdracht,
            check_only=check_only,
            scope=scope,
            success=False,
            message=f"Policy error: {exc}",
            artifacts=[],
        )

        return FrontdoorResult(
            success=False,
            message=str(exc),
            trace_path=trace_path,
        )

    except ValueError as exc:
        trace_path = _write_trace(
            workspace_root=workspace_root,
            operation=operation,
            opdracht=opdracht,
            check_only=check_only,
            scope=scope,
            success=False,
            message=f"Value error: {exc}",
            artifacts=[],
        )

        return FrontdoorResult(
            success=False,
            message=str(exc),
            trace_path=trace_path,
        )

    except Exception as exc:
        trace_path = _write_trace(
            workspace_root=workspace_root,
            operation=operation,
            opdracht=opdracht,
            check_only=check_only,
            scope=scope,
            success=False,
            message=f"Unexpected error: {exc}",
            artifacts=[],
        )

        return FrontdoorResult(
            success=False,
            message=f"Unexpected error: {exc}",
            trace_path=trace_path,
        )
