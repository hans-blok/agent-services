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
        workspace_root / ".github" / "prompts",
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            raise PolicyError(
                f"Vereiste folder ontbreekt: {dir_path.relative_to(workspace_root).as_posix()}"
            )


def _policy_gate_governance_exists(workspace_root: Path) -> None:
    """Valideer dat governance documenten bestaan."""
    required_files = [
        workspace_root / "governance" / "workspace-doctrine.md",
        workspace_root / "governance" / "gedragscode.md",
    ]
    
    for file_path in required_files:
        if not file_path.exists():
            raise PolicyError(
                f"Vereist governance document ontbreekt: {file_path.relative_to(workspace_root).as_posix()}"
            )


def op_beheer_git(
    *,
    workspace_root: Path,
    opdracht: str,
    check_only: bool,
    scope: str | None,
) -> OperationResult:
    """Operatie: beheer-git
    
    Beheert Git workflows, branches, commits en .gitignore.
    Scope opties: commits, branches, gitignore, hooks
    """
    _policy_gate_workspace_paths(workspace_root)
    
    # Placeholder implementatie - deze operatie is meestal manueel/conversationeel
    artifacts: list[Path] = []
    
    scope_desc = f" (scope: {scope})" if scope else ""
    mode_desc = "Analyse" if check_only else "Actie"
    
    message = f"{mode_desc}: Git beheer{scope_desc} - '{opdracht}' (nog te implementeren)"
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=artifacts,
    )


def op_configureer_github(
    *,
    workspace_root: Path,
    opdracht: str,
    check_only: bool,
    scope: str | None,
) -> OperationResult:
    """Operatie: configureer-github
    
    Configureert GitHub repository settings, collaboratie en automation.
    Scope opties: repository-setup, collaboratie, automation, pages
    """
    _policy_gate_workspace_paths(workspace_root)
    
    # Placeholder implementatie - deze operatie is meestal manueel/conversationeel
    artifacts: list[Path] = []
    
    scope_desc = f" (scope: {scope})" if scope else ""
    mode_desc = "Analyse" if check_only else "Actie"
    
    message = f"{mode_desc}: GitHub configuratie{scope_desc} - '{opdracht}' (nog te implementeren)"
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=artifacts,
    )


def op_orden_workspace(
    *,
    workspace_root: Path,
    opdracht: str,
    check_only: bool,
    scope: str | None,
) -> OperationResult:
        """Operatie: orden-workspace
    
        Ordent workspace structuur, naamgeving en markdown.
        Scope opties: structure, names, markdown, docs-resultaten, github-prompts.

        Bij alle acties waarbij bestanden worden verplaatst, hanteert Moeder
        **single source of truth**:

        - bestanden worden daadwerkelijk **verplaatst** (bijvoorbeeld met `git mv`);
        - er blijven geen kopieën van hetzelfde bronbestand achter op de oude
            locatie of in andere workspaces.
        """
    _policy_gate_workspace_paths(workspace_root)
    _policy_gate_governance_exists(workspace_root)
    
    # Placeholder implementatie - deze operatie vereist vaak menselijke beoordeling
    artifacts: list[Path] = []
    
    scope_desc = f" (scope: {scope})" if scope else ""
    mode_desc = "Analyse" if check_only else "Actie"
    
    message = (
        f"{mode_desc}: Workspace ordening{scope_desc} - '{opdracht}' "
        "(nog te implementeren; bij verplaatsen geen kopieën, single source)"
    )
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=artifacts,
    )


def op_schrijf_beleid(
    *,
    workspace_root: Path,
    opdracht: str,
    check_only: bool,
) -> OperationResult:
    """Operatie: schrijf-beleid
    
    Genereert governance/beleid.md op basis van temp/context.md.
    """
    _policy_gate_workspace_paths(workspace_root)
    _policy_gate_governance_exists(workspace_root)
    
    context_path = workspace_root / "temp" / "context.md"
    beleid_path = workspace_root / "governance" / "beleid.md"
    
    # Valideer dat context.md bestaat
    if not context_path.exists():
        raise PolicyError(
            f"temp/context.md ontbreekt - kan geen beleid genereren zonder context"
        )
    
    # Waarschuw als beleid.md al bestaat
    if beleid_path.exists() and not check_only:
        raise PolicyError(
            f"governance/beleid.md bestaat al - gebruik --check-only of verwijder eerst het bestaande beleid"
        )
    
    artifacts: list[Path] = []
    
    if check_only:
        message = f"Analyse: Beleid generatie op basis van context.md (dry-run)"
    else:
        # Placeholder implementatie - beleid generatie vereist AI/menselijke input
        message = f"Beleid generatie - '{opdracht}' (nog te implementeren)"
        # artifacts.append(beleid_path)  # Zou hier komen na implementatie
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=artifacts,
    )


def op_zet_agent_boundary(
    *,
    workspace_root: Path,
    opdracht: str,
    aanleiding: str | None,
    gewenste_capability: str | None,
) -> OperationResult:
    """Operatie: zet-agent-boundary
    
    Definieert capability boundary voor nieuwe agent en slaat op als deliverable.
    Output wordt opgeslagen in docs/resultaten/moeder/agent-boundary-{agent-naam}.md
    voor traceerbaarheid en handoff naar Agent Smeder.
    """
    _policy_gate_workspace_paths(workspace_root)
    _policy_gate_governance_exists(workspace_root)
    
    beleid_path = workspace_root / "governance" / "beleid.md"
    
    # Valideer dat beleid.md bestaat
    if not beleid_path.exists():
        raise PolicyError(
            f"governance/beleid.md ontbreekt - kan geen agent boundary valideren zonder beleid"
        )
    
    # Valideer input parameters
    if not aanleiding:
        raise ValueError("--aanleiding is verplicht voor zet-agent-boundary operatie")
    
    if not gewenste_capability:
        raise ValueError("--gewenste-capability is verplicht voor zet-agent-boundary operatie")
    
    # Placeholder: in werkelijkheid zou hier de boundary door AI worden gegenereerd
    # Voor nu gebruiken we opdracht als basis en verwachten we dat de gebruiker
    # de boundary als onderdeel van opdracht formuleert
    
    # Parseer opdracht voor boundary-componenten (verwacht format in opdracht)
    # Dit is een vereenvoudigde implementatie - in productie zou dit door AI gebeuren
    message = (
        f"Agent boundary definitie - aanleiding: '{aanleiding}', "
        f"capability: '{gewenste_capability}'. "
        "Boundary moet handmatig worden vastgelegd in docs/resultaten/moeder/agent-boundary-<agent-naam>.md"
    )
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=[],
    )


def op_valideer_governance(
    *,
    workspace_root: Path,
    opdracht: str,
    scope: str | None,
) -> OperationResult:
    """Operatie: valideer-governance
    
    Valideert compliance met governance documenten.
    Scope opties: workspace-standaard, gedragscode, beleid, agent-standaard, all
    """
    _policy_gate_workspace_paths(workspace_root)
    _policy_gate_governance_exists(workspace_root)
    
    artifacts: list[Path] = []
    
    scope_desc = f" (scope: {scope})" if scope else " (scope: all)"
    
    # Placeholder implementatie - governance validatie vereist uitgebreide checks
    message = f"Governance validatie{scope_desc} - '{opdracht}' (nog te implementeren)"
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=artifacts,
    )


def execute_operation(
    *,
    workspace_root: Path,
    operation: str,
    opdracht: str,
    check_only: bool,
    scope: str | None,
    aanleiding: str | None,
    gewenste_capability: str | None,
) -> OperationResult:
    """Route operatie naar juiste handler."""
    
    if operation == "beheer-git":
        return op_beheer_git(
            workspace_root=workspace_root,
            opdracht=opdracht,
            check_only=check_only,
            scope=scope,
        )
    
    elif operation == "configureer-github":
        return op_configureer_github(
            workspace_root=workspace_root,
            opdracht=opdracht,
            check_only=check_only,
            scope=scope,
        )
    
    elif operation == "orden-workspace":
        return op_orden_workspace(
            workspace_root=workspace_root,
            opdracht=opdracht,
            check_only=check_only,
            scope=scope,
        )
    
    elif operation == "schrijf-beleid":
        return op_schrijf_beleid(
            workspace_root=workspace_root,
            opdracht=opdracht,
            check_only=check_only,
        )
    
    elif operation == "zet-agent-boundary":
        return op_zet_agent_boundary(
            workspace_root=workspace_root,
            opdracht=opdracht,
            aanleiding=aanleiding,
            gewenste_capability=gewenste_capability,
        )
    
    elif operation == "valideer-governance":
        return op_valideer_governance(
            workspace_root=workspace_root,
            opdracht=opdracht,
            scope=scope,
        )
    
    else:
        raise ValueError(f"Onbekende operatie: {operation}")
