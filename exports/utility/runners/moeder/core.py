from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
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
        workspace_root / "governance" / "workspace-standaard.md",
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
    Scope opties: structure, names, markdown, docs-resultaten, github-prompts
    """
    _policy_gate_workspace_paths(workspace_root)
    _policy_gate_governance_exists(workspace_root)
    
    # Placeholder implementatie - deze operatie vereist vaak menselijke beoordeling
    artifacts: list[Path] = []
    
    scope_desc = f" (scope: {scope})" if scope else ""
    mode_desc = "Analyse" if check_only else "Actie"
    
    message = f"{mode_desc}: Workspace ordening{scope_desc} - '{opdracht}' (nog te implementeren)"
    
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
    
    Definieert capability boundary voor nieuwe agent (output voor Agent Smeder).
    Schrijft boundary weg naar docs/resultaten/moeder/<agent-naam>-boundary.md
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
    
    # Extract agent-naam from opdracht (format: "Beschrijf boundary voor <agent-naam>")
    # Als opdracht geen agent-naam bevat, gebruik gewenste_capability om er een te maken
    agent_naam = _extract_agent_naam_from_opdracht(opdracht, gewenste_capability)
    
    # Afleiden van doel en domein uit capability (simpele heuristiek)
    # Doel: eerste werkwoord + object uit capability
    doel = gewenste_capability if len(gewenste_capability) < 80 else gewenste_capability[:80] + "..."
    
    # Domein: extract from capability or use generic
    domein = "Software Architecture" if "architecture" in gewenste_capability.lower() else \
             "Data Management" if "data" in gewenste_capability.lower() else \
             "Enterprise Modeling"
    
    # Zorg dat output directory bestaat
    output_dir = workspace_root / "docs" / "resultaten" / "moeder"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Schrijf boundary bestand
    boundary_file = output_dir / f"{agent_naam}-boundary.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# Agent Boundary: {agent_naam}

**Gegenereerd**: {timestamp}  
**Status**: Gedefinieerd door Moeder

## Aanleiding

{aanleiding}

## Gewenste Capability

{gewenste_capability}

## Agent Definitie

agent-naam: {agent_naam}
capability-boundary: {gewenste_capability}
doel: {doel}
domein: {domein}

## Output voor Agent Smeder

Deze boundary is klaar voor verwerking door Agent Smeder stap 2 (definieer prompt).

---

*Dit document is gegenereerd door Moeder (zet-agent-boundary operatie)*
"""
    
    boundary_file.write_text(content, encoding="utf-8")
    
    artifacts: list[Path] = [boundary_file]
    
    message = f"Agent boundary voor '{agent_naam}' opgeslagen in {boundary_file.relative_to(workspace_root).as_posix()}"
    
    return OperationResult(
        success=True,
        message=message,
        artifacts=artifacts,
    )


def _extract_agent_naam_from_opdracht(opdracht: str, gewenste_capability: str) -> str:
    """Extract agent naam from opdracht or generate from capability."""
    # Zoek naar "voor <agent-naam>" patroon in opdracht
    import re
    match = re.search(r'voor\s+(?:een\s+)?([a-z0-9-]+)', opdracht.lower())
    if match:
        return match.group(1)
    
    # Fallback: maak naam van eerste 2-3 woorden van capability
    words = gewenste_capability.lower().split()[:3]
    # Filter stopwoorden
    stopwords = {'de', 'het', 'een', 'en', 'of', 'voor', 'van', 'in', 'op', 'met', 'aan'}
    words = [w for w in words if w not in stopwords]
    
    # Maak lowercase-hyphen naam
    agent_naam = '-'.join(words[:2]) if len(words) >= 2 else '-'.join(words)
    
    # Clean up: alleen alphanumeriek en hyphens
    agent_naam = re.sub(r'[^a-z0-9-]', '', agent_naam)
    agent_naam = re.sub(r'-+', '-', agent_naam)  # Meerdere hyphens naar één
    
    return agent_naam or "nieuwe-agent"


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
