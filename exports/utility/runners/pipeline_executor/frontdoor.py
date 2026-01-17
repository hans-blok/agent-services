from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from pipeline_executor.core import PolicyError, execute_pipeline


@dataclass(frozen=True)
class FrontdoorResult:
    success: bool
    message: str
    execution_log: Path | None


def _timestamp_for_filename(now: datetime | None = None) -> str:
    now = now or datetime.now()
    return now.strftime("%y%m%d-%H-%M-%S")


def _write_execution_log(
    *,
    workspace_root: Path,
    pipeline_naam: str,
    success: bool,
    message: str,
    steps_executed: list[dict],
    gates_validated: list[dict],
    failures: list[dict],
    artifacts: list[Path],
    total_duration: float,
) -> Path:
    log_dir = workspace_root / "log"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_path = log_dir / f"pipeline-executor-{pipeline_naam}-{_timestamp_for_filename()}.md"

    lines: list[str] = []
    lines.append(f"# Pipeline Execution Log: {pipeline_naam}\n\n")
    lines.append(f"**Status**: {'Success' if success else 'Failed'}\n")
    lines.append(f"**Total Duration**: {total_duration:.2f} seconds\n")
    lines.append(f"**Timestamp**: {datetime.now().isoformat()}\n\n")

    lines.append("## Summary\n\n")
    lines.append(f"{message}\n\n")

    lines.append("## Execution Trace\n\n")
    if steps_executed:
        for step in steps_executed:
            lines.append(f"### Step {step.get('number')}: {step.get('name')}\n")
            lines.append(f"- **Agent**: {step.get('agent')}\n")
            lines.append(f"- **Command**: `{step.get('command')}`\n")
            lines.append(f"- **Duration**: {step.get('duration', 0):.2f}s\n")
            lines.append(f"- **Status**: {step.get('status')}\n")
            if step.get('exit_code') is not None:
                lines.append(f"- **Exit Code**: {step.get('exit_code')}\n")
            lines.append("\n")
    else:
        lines.append("(geen stappen uitgevoerd)\n\n")

    lines.append("## Gate Validations\n\n")
    if gates_validated:
        for gate in gates_validated:
            lines.append(f"### Gate: {gate.get('name')}\n")
            lines.append(f"- **Type**: {gate.get('type')}\n")
            lines.append(f"- **Result**: {gate.get('result')}\n")
            lines.append(f"- **Criteria**: {gate.get('criteria')}\n")
            lines.append("\n")
    else:
        lines.append("(geen gates gevalideerd)\n\n")

    if failures:
        lines.append("## Failures\n\n")
        for failure in failures:
            lines.append(f"### {failure.get('location')}\n")
            lines.append(f"- **Error**: {failure.get('error')}\n")
            lines.append(f"- **Action**: {failure.get('action')}\n")
            lines.append("\n")

    lines.append("## Artifacts Produced\n\n")
    if artifacts:
        for artifact in artifacts:
            try:
                rel = artifact.relative_to(workspace_root)
                lines.append(f"- {rel.as_posix()}\n")
            except ValueError:
                lines.append(f"- {str(artifact)}\n")
    else:
        lines.append("- (geen artifacts)\n")

    log_path.write_text("".join(lines), encoding="utf-8")
    return log_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pipeline Executor. Voert multi-agent pipelines uit."
    )

    parser.add_argument(
        "--pipeline-bestand",
        type=str,
        required=True,
        help="Pad naar pipeline document (bijv. docs/resultaten/workflow-architect/<naam>-pipeline.md)",
    )

    parser.add_argument(
        "--workflow-bestand",
        type=str,
        default=None,
        help="Pad naar workflow document (optioneel, voor validatie)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Alleen valideren en plannen, geen agents daadwerkelijk uitvoeren",
    )

    parser.add_argument(
        "--stop-on-failure",
        type=str,
        choices=["true", "false"],
        default=None,
        help="Override pipeline setting - stoppen bij eerste failure (default: volg pipeline-spec)",
    )

    parser.add_argument(
        "--execution-log",
        type=str,
        default=None,
        help="Waar execution log opslaan (default: temp/pipeline-executor-<naam>-{timestamp}.md)",
    )

    parser.add_argument(
        "--continue-from-step",
        type=int,
        default=None,
        help="Herstart pipeline vanaf specifieke stap (voor recovery na failure)",
    )
    
    # Allow additional parameters to pass to agents
    parser.add_argument(
        "extra_params",
        nargs=argparse.REMAINDER,
        help="Extra parameters door te geven aan agents (bijv. --agent-naam test --capability '...')",
    )

    return parser


def run_frontdoor(*, workspace_root: Path) -> FrontdoorResult:
    parser = build_parser()
    args = parser.parse_args()

    pipeline_bestand = args.pipeline_bestand
    workflow_bestand = args.workflow_bestand
    dry_run = args.dry_run
    stop_on_failure = args.stop_on_failure == "true" if args.stop_on_failure else None
    execution_log_path = args.execution_log
    continue_from_step = args.continue_from_step
    extra_params = args.extra_params if hasattr(args, 'extra_params') else []

    try:
        result = execute_pipeline(
            workspace_root=workspace_root,
            pipeline_bestand=pipeline_bestand,
            workflow_bestand=workflow_bestand,
            dry_run=dry_run,
            stop_on_failure=stop_on_failure,
            continue_from_step=continue_from_step,
            extra_params=extra_params,
        )

        # Extract pipeline naam from path
        pipeline_path = Path(pipeline_bestand)
        pipeline_naam = pipeline_path.stem.replace("-pipeline", "")

        # Write execution log
        execution_log = _write_execution_log(
            workspace_root=workspace_root,
            pipeline_naam=pipeline_naam,
            success=result.success,
            message=result.message,
            steps_executed=result.steps_executed,
            gates_validated=result.gates_validated,
            failures=result.failures,
            artifacts=result.artifacts,
            total_duration=result.total_duration,
        )

        return FrontdoorResult(
            success=result.success,
            message=result.message,
            execution_log=execution_log,
        )

    except PolicyError as err:
        # Extract pipeline naam
        try:
            pipeline_path = Path(pipeline_bestand)
            pipeline_naam = pipeline_path.stem.replace("-pipeline", "")
        except:
            pipeline_naam = "unknown"

        execution_log = _write_execution_log(
            workspace_root=workspace_root,
            pipeline_naam=pipeline_naam,
            success=False,
            message=f"Policy violation: {err}",
            steps_executed=[],
            gates_validated=[],
            failures=[{"location": "Pre-execution", "error": str(err), "action": "Stop"}],
            artifacts=[],
            total_duration=0.0,
        )

        return FrontdoorResult(
            success=False,
            message=f"Policy violation: {err}",
            execution_log=execution_log,
        )

    except ValueError as err:
        try:
            pipeline_path = Path(pipeline_bestand)
            pipeline_naam = pipeline_path.stem.replace("-pipeline", "")
        except:
            pipeline_naam = "unknown"

        execution_log = _write_execution_log(
            workspace_root=workspace_root,
            pipeline_naam=pipeline_naam,
            success=False,
            message=f"Validation error: {err}",
            steps_executed=[],
            gates_validated=[],
            failures=[{"location": "Pre-execution", "error": str(err), "action": "Stop"}],
            artifacts=[],
            total_duration=0.0,
        )

        return FrontdoorResult(
            success=False,
            message=f"Validation error: {err}",
            execution_log=execution_log,
        )

    except Exception as err:
        try:
            pipeline_path = Path(pipeline_bestand)
            pipeline_naam = pipeline_path.stem.replace("-pipeline", "")
        except:
            pipeline_naam = "unknown"

        execution_log = _write_execution_log(
            workspace_root=workspace_root,
            pipeline_naam=pipeline_naam,
            success=False,
            message=f"Unexpected error: {err}",
            steps_executed=[],
            gates_validated=[],
            failures=[{"location": "Execution", "error": str(err), "action": "Stop"}],
            artifacts=[],
            total_duration=0.0,
        )

        return FrontdoorResult(
            success=False,
            message=f"Unexpected error: {err}",
            execution_log=execution_log,
        )
