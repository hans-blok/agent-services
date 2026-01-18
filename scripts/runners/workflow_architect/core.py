from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class OperationResult:
    success: bool
    message: str
    artifacts: list[Path]


class PolicyError(Exception):
    pass


def _policy_gate_workspace_paths(workspace_root: Path) -> None:
    """Valideer dat essentiële workspace folders bestaan."""
    required_dirs = [
        workspace_root / "governance",
        workspace_root / "governance" / "rolbeschrijvingen",
        workspace_root / "docs" / "resultaten",
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            raise PolicyError(
                f"Vereiste folder ontbreekt: {dir_path.relative_to(workspace_root).as_posix()}"
            )


def _policy_gate_workflow_architect_output_dir(workspace_root: Path) -> Path:
    """Valideer en maak output directory voor Workflow Architect."""
    output_dir = workspace_root / "docs" / "resultaten" / "workflow-architect"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _policy_gate_file_exists(file_path: Path, description: str) -> None:
    """Valideer dat een bestand bestaat."""
    if not file_path.exists():
        raise PolicyError(f"{description} bestaat niet: {file_path}")
    
    if not file_path.is_file():
        raise PolicyError(f"{description} is geen bestand: {file_path}")


def op_ontwerp_workflow(
    *,
    workspace_root: Path,
    taak_naam: str,
    taak_beschrijving: str | None,
    gewenst_resultaat: str | None,
    beschikbare_agents: list[str] | None,
    constraints: list[str] | None,
) -> OperationResult:
    """Operatie: ontwerp-workflow
    
    Ontwerpt workflow-structuur met stappen, afhankelijkheden en kritieke paden.
    """
    _policy_gate_workspace_paths(workspace_root)
    
    # Valideer verplichte parameters
    if taak_beschrijving is None:
        raise ValueError("--taak-beschrijving is verplicht voor ontwerp-workflow")
    
    if gewenst_resultaat is None:
        raise ValueError("--gewenst-resultaat is verplicht voor ontwerp-workflow")
    
    # Maak output directory
    output_dir = _policy_gate_workflow_architect_output_dir(workspace_root)
    
    # Output bestandsnaam
    output_file = output_dir / f"{taak_naam}-workflow.md"
    
    # Placeholder implementatie - deze operatie vereist AI-interactie
    artifacts: list[Path] = []
    
    constraints_desc = ""
    if constraints:
        constraints_desc = f" (constraints: {', '.join(constraints)})"
    
    agents_desc = ""
    if beschikbare_agents:
        agents_desc = f" met agents: {', '.join(beschikbare_agents)}"
    
    message = (
        f"Workflow ontwerp voor '{taak_naam}': {taak_beschrijving} → {gewenst_resultaat}"
        f"{agents_desc}{constraints_desc} "
        f"(output: {output_file.relative_to(workspace_root).as_posix()}) "
        f"(nog te implementeren - vereist AI voor agent-selectie en afhankelijkheids-analyse)"
    )
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=artifacts,
    )


def op_ontwerp_pipeline(
    *,
    workspace_root: Path,
    taak_naam: str,
    workflow_bestand: str | None,
    gate_types: list[str] | None,
    stop_on_failure: bool,
    parallel_execution: bool,
) -> OperationResult:
    """Operatie: ontwerp-pipeline
    
    Ontwerpt pipeline met execution chain, quality gates en failure handling.
    """
    _policy_gate_workspace_paths(workspace_root)
    
    # Valideer verplichte parameters
    if workflow_bestand is None:
        raise ValueError("--workflow-bestand is verplicht voor ontwerp-pipeline")
    
    # Valideer dat workflow bestand bestaat
    workflow_path = workspace_root / workflow_bestand
    _policy_gate_file_exists(workflow_path, "Workflow bestand")
    
    # Maak output directory
    output_dir = _policy_gate_workflow_architect_output_dir(workspace_root)
    
    # Output bestandsnaam
    output_file = output_dir / f"{taak_naam}-pipeline.md"
    
    # Placeholder implementatie - deze operatie vereist AI-interactie
    artifacts: list[Path] = []
    
    gates_desc = ""
    if gate_types:
        gates_desc = f" met gates: {', '.join(gate_types)}"
    
    exec_mode = "parallel" if parallel_execution else "sequential"
    failure_mode = "stop bij fout" if stop_on_failure else "continue bij fout"
    
    message = (
        f"Pipeline ontwerp voor '{taak_naam}' gebaseerd op {workflow_bestand}"
        f"{gates_desc} "
        f"(execution: {exec_mode}, failure: {failure_mode}) "
        f"(output: {output_file.relative_to(workspace_root).as_posix()}) "
        f"(nog te implementeren - vereist AI voor gate-criteria en failure-strategieën)"
    )
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=artifacts,
    )


def op_definieer_artefact_flow(
    *,
    workspace_root: Path,
    taak_naam: str,
    workflow_bestand: str | None,
    pipeline_bestand: str | None,
    artefact_locaties: str | None,
    naming_conventions: list[str] | None,
) -> OperationResult:
    """Operatie: definieer-artefact-flow
    
    Definieert artefact-flow met input/output mapping, transformaties en lifecycle.
    """
    _policy_gate_workspace_paths(workspace_root)
    
    # Valideer verplichte parameters
    if workflow_bestand is None:
        raise ValueError("--workflow-bestand is verplicht voor definieer-artefact-flow")
    
    if pipeline_bestand is None:
        raise ValueError("--pipeline-bestand is verplicht voor definieer-artefact-flow")
    
    # Valideer dat bestanden bestaan
    workflow_path = workspace_root / workflow_bestand
    _policy_gate_file_exists(workflow_path, "Workflow bestand")
    
    pipeline_path = workspace_root / pipeline_bestand
    _policy_gate_file_exists(pipeline_path, "Pipeline bestand")
    
    # Maak output directory
    output_dir = _policy_gate_workflow_architect_output_dir(workspace_root)
    
    # Output bestandsnaam
    output_file = output_dir / f"{taak_naam}-artefact-flow.md"
    
    # Placeholder implementatie - deze operatie vereist AI-interactie
    artifacts: list[Path] = []
    
    locaties_desc = ""
    if artefact_locaties:
        locaties_desc = f" (locaties: {artefact_locaties})"
    
    conventions_desc = ""
    if naming_conventions:
        conventions_desc = f" met naming: {', '.join(naming_conventions)}"
    
    message = (
        f"Artefact-flow definitie voor '{taak_naam}' gebaseerd op "
        f"{workflow_bestand} + {pipeline_bestand}"
        f"{locaties_desc}{conventions_desc} "
        f"(output: {output_file.relative_to(workspace_root).as_posix()}) "
        f"(nog te implementeren - vereist AI voor data-lineage analyse en orphaned/missing artifact detectie)"
    )
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=artifacts,
    )


def execute_operation(
    *,
    workspace_root: Path,
    operation: str,
    taak_naam: str,
    taak_beschrijving: str | None,
    gewenst_resultaat: str | None,
    beschikbare_agents: list[str] | None,
    constraints: list[str] | None,
    workflow_bestand: str | None,
    gate_types: list[str] | None,
    stop_on_failure: bool,
    parallel_execution: bool,
    pipeline_bestand: str | None,
    artefact_locaties: str | None,
    naming_conventions: list[str] | None,
) -> OperationResult:
    """Route naar de juiste operation handler."""
    
    if operation == "ontwerp-workflow":
        return op_ontwerp_workflow(
            workspace_root=workspace_root,
            taak_naam=taak_naam,
            taak_beschrijving=taak_beschrijving,
            gewenst_resultaat=gewenst_resultaat,
            beschikbare_agents=beschikbare_agents,
            constraints=constraints,
        )
    
    elif operation == "ontwerp-pipeline":
        return op_ontwerp_pipeline(
            workspace_root=workspace_root,
            taak_naam=taak_naam,
            workflow_bestand=workflow_bestand,
            gate_types=gate_types,
            stop_on_failure=stop_on_failure,
            parallel_execution=parallel_execution,
        )
    
    elif operation == "definieer-artefact-flow":
        return op_definieer_artefact_flow(
            workspace_root=workspace_root,
            taak_naam=taak_naam,
            workflow_bestand=workflow_bestand,
            pipeline_bestand=pipeline_bestand,
            artefact_locaties=artefact_locaties,
            naming_conventions=naming_conventions,
        )
    
    else:
        raise ValueError(f"Onbekende operatie: {operation}")
