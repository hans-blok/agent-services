from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from workflow_architect.core import PolicyError, execute_operation


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
    taak_naam: str | None,
    success: bool,
    message: str,
    artifacts: list[Path],
    **kwargs,
) -> Path:
    temp_dir = workspace_root / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    trace_path = temp_dir / f"workflow-architect-trace-{_timestamp_for_filename()}.md"

    lines: list[str] = []
    lines.append("# Workflow Architect Trace\n")
    lines.append(f"- operation: {operation}\n")
    lines.append(f"- success: {str(success).lower()}\n")
    lines.append(f"- message: {message}\n")
    lines.append("\n## Input\n")
    
    if taak_naam is not None:
        lines.append(f"- taak-naam: {taak_naam}\n")
    
    for key, value in kwargs.items():
        if value is not None:
            if isinstance(value, list):
                lines.append(f"- {key}: {', '.join(str(v) for v in value)}\n")
            else:
                lines.append(f"- {key}: {value}\n")

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
        description="Workflow Architect runner (frontdoor). Ontwerpt workflows, pipelines en artefact-flows."
    )

    parser.add_argument(
        "operation",
        choices=[
            "ontwerp-workflow",
            "ontwerp-pipeline",
            "definieer-artefact-flow",
        ],
        help="Welke operatie uitvoeren",
    )

    # Common parameters
    parser.add_argument(
        "--taak-naam",
        type=str,
        required=True,
        help="Naam van de taak (gebruikt voor output bestandsnaam)",
    )

    # Parameters voor ontwerp-workflow
    parser.add_argument(
        "--taak-beschrijving",
        type=str,
        default=None,
        help="Beschrijving van de complexe taak (vereist voor ontwerp-workflow)",
    )

    parser.add_argument(
        "--gewenst-resultaat",
        type=str,
        default=None,
        help="Wat moet het eindresultaat zijn (vereist voor ontwerp-workflow)",
    )

    parser.add_argument(
        "--beschikbare-agents",
        type=str,
        nargs="*",
        default=None,
        help="Lijst van agents die gebruikt kunnen worden (optioneel)",
    )

    parser.add_argument(
        "--constraints",
        type=str,
        nargs="*",
        default=None,
        help="Beperkingen (optioneel, bijv. 'maximaal 3 stappen')",
    )

    # Parameters voor ontwerp-pipeline
    parser.add_argument(
        "--workflow-bestand",
        type=str,
        default=None,
        help="Pad naar workflow document (vereist voor ontwerp-pipeline en definieer-artefact-flow)",
    )

    parser.add_argument(
        "--gate-types",
        type=str,
        nargs="*",
        choices=["validatie", "review", "test", "approval"],
        default=None,
        help="Welke soorten gates gewenst zijn (optioneel voor ontwerp-pipeline)",
    )

    parser.add_argument(
        "--stop-on-failure",
        type=str,
        choices=["true", "false"],
        default="true",
        help="Of pipeline stopt bij eerste fout (optioneel voor ontwerp-pipeline, default: true)",
    )

    parser.add_argument(
        "--parallel-execution",
        type=str,
        choices=["true", "false"],
        default="false",
        help="Of stappen parallel kunnen draaien (optioneel voor ontwerp-pipeline, default: false)",
    )

    # Parameters voor definieer-artefact-flow
    parser.add_argument(
        "--pipeline-bestand",
        type=str,
        default=None,
        help="Pad naar pipeline document (vereist voor definieer-artefact-flow)",
    )

    parser.add_argument(
        "--artefact-locaties",
        type=str,
        default=None,
        help="Waar artefacten opgeslagen worden (optioneel voor definieer-artefact-flow)",
    )

    parser.add_argument(
        "--naming-conventions",
        type=str,
        nargs="*",
        default=None,
        help="Naamgevingsconventies voor artefacten (optioneel voor definieer-artefact-flow)",
    )

    return parser


def run_frontdoor(*, workspace_root: Path) -> FrontdoorResult:
    parser = build_parser()
    args = parser.parse_args()

    operation = args.operation
    taak_naam = args.taak_naam

    # Converteer string booleans naar bool
    stop_on_failure = args.stop_on_failure == "true" if args.stop_on_failure else True
    parallel_execution = args.parallel_execution == "true" if args.parallel_execution else False

    try:
        result = execute_operation(
            workspace_root=workspace_root,
            operation=operation,
            taak_naam=taak_naam,
            taak_beschrijving=args.taak_beschrijving,
            gewenst_resultaat=args.gewenst_resultaat,
            beschikbare_agents=args.beschikbare_agents,
            constraints=args.constraints,
            workflow_bestand=args.workflow_bestand,
            gate_types=args.gate_types,
            stop_on_failure=stop_on_failure,
            parallel_execution=parallel_execution,
            pipeline_bestand=args.pipeline_bestand,
            artefact_locaties=args.artefact_locaties,
            naming_conventions=args.naming_conventions,
        )

        trace_path = _write_trace(
            workspace_root=workspace_root,
            operation=operation,
            taak_naam=taak_naam,
            success=result.success,
            message=result.message,
            artifacts=result.artifacts,
            taak_beschrijving=args.taak_beschrijving,
            gewenst_resultaat=args.gewenst_resultaat,
            beschikbare_agents=args.beschikbare_agents,
            constraints=args.constraints,
            workflow_bestand=args.workflow_bestand,
            gate_types=args.gate_types,
            stop_on_failure=stop_on_failure,
            parallel_execution=parallel_execution,
            pipeline_bestand=args.pipeline_bestand,
            artefact_locaties=args.artefact_locaties,
            naming_conventions=args.naming_conventions,
        )

        return FrontdoorResult(
            success=result.success,
            message=result.message,
            trace_path=trace_path,
        )

    except PolicyError as err:
        trace_path = _write_trace(
            workspace_root=workspace_root,
            operation=operation,
            taak_naam=taak_naam,
            success=False,
            message=f"Policy violation: {err}",
            artifacts=[],
            taak_beschrijving=args.taak_beschrijving,
            gewenst_resultaat=args.gewenst_resultaat,
        )
        return FrontdoorResult(
            success=False,
            message=f"Policy violation: {err}",
            trace_path=trace_path,
        )

    except ValueError as err:
        trace_path = _write_trace(
            workspace_root=workspace_root,
            operation=operation,
            taak_naam=taak_naam,
            success=False,
            message=f"Validation error: {err}",
            artifacts=[],
            taak_beschrijving=args.taak_beschrijving,
            gewenst_resultaat=args.gewenst_resultaat,
        )
        return FrontdoorResult(
            success=False,
            message=f"Validation error: {err}",
            trace_path=trace_path,
        )

    except Exception as err:
        trace_path = _write_trace(
            workspace_root=workspace_root,
            operation=operation,
            taak_naam=taak_naam,
            success=False,
            message=f"Unexpected error: {err}",
            artifacts=[],
            taak_beschrijving=args.taak_beschrijving,
            gewenst_resultaat=args.gewenst_resultaat,
        )
        return FrontdoorResult(
            success=False,
            message=f"Unexpected error: {err}",
            trace_path=trace_path,
        )
