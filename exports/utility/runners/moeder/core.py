from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
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


def op_fetch_agents(
    *,
    workspace_root: Path,
    opdracht: str,
    value_stream: str | None,
    branch: str,
    agent_services_url: str,
    include_runners: bool,
) -> OperationResult:
    """Operatie: fetch-agents
    
    Haalt agents op uit agent-services repository en installeert in workspace.
    Leest agents-publicatie.json om beschikbare agents te bepalen.
    
    BELANGRIJK - Overschrijfgedrag:
    - Charters: Volledig overschreven met versie uit agent-services
    - Prompts: Bestaande prompts met dezelfde naam overschreven; extra prompts behouden
    - Runner module folders: Volledig verwijderd en vervangen (niet gemerged!)
    
    Dit is by design: fetching installeert de canonieke versie uit agent-services.
    Workspace-specifieke aanpassingen worden overschreven.
    """
    # Valideer verplichte parameters
    if not value_stream:
        raise ValueError("Parameter --value-stream is verplicht voor fetch-agents operatie")
    
    value_stream = value_stream.lower()
    
    _policy_gate_workspace_paths(workspace_root)
    
    artifacts: list[Path] = []
    
    # Maak temp directory voor clone
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        repo_path = temp_path / "agent-services"
        
        # Clone repository
        try:
            subprocess.run(
                ["git", "clone", "--branch", branch, "--depth", "1", agent_services_url, str(repo_path)],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            raise PolicyError(
                f"Kan agent-services repository niet clonen (branch: {branch}): {e.stderr}"
            )
        
        # Lees agents-publicatie.json
        manifest_path = repo_path / "agents-publicatie.json"
        if not manifest_path.exists():
            raise PolicyError(
                f"agents-publicatie.json niet gevonden in repository root (branch: {branch})"
            )
        
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        # Valideer value-stream bestaat
        available_streams = manifest.get("valueStreams", [])
        if value_stream not in available_streams:
            raise PolicyError(
                f"Value stream '{value_stream}' niet gevonden in publicatie. "
                f"Beschikbare streams: {', '.join(available_streams)}"
            )
        
        # Filter agents voor deze value stream
        agents = manifest.get("agents", [])
        filtered_agents = [a for a in agents if a.get("valueStream") == value_stream]
        
        if not filtered_agents:
            return OperationResult(
                success=True,
                message=f"Geen agents gevonden voor value stream '{value_stream}'",
                artifacts=[],
            )
        
        # Installeer elke agent
        installed_count = 0
        prompts_count = 0
        runners_count = 0
        
        for agent in filtered_agents:
            agent_naam = agent.get("naam")
            
            # Charter
            charter_src = repo_path / "exports" / value_stream / "charters-agents" / f"charter.{agent_naam}.md"
            if charter_src.exists():
                charter_dst = workspace_root / "charters-agents" / f"charter.{agent_naam}.md"
                charter_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(charter_src, charter_dst)
                artifacts.append(charter_dst)
            
            # Prompts
            prompts_src_dir = repo_path / "exports" / value_stream / "prompts"
            if prompts_src_dir.exists():
                for prompt_file in prompts_src_dir.glob(f"{agent_naam}-*.prompt.md"):
                    prompt_dst = workspace_root / ".github" / "prompts" / prompt_file.name
                    prompt_dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(prompt_file, prompt_dst)
                    artifacts.append(prompt_dst)
                    prompts_count += 1
            
            # Runners (optioneel)
            if include_runners:
            runner_found = False  # Track of deze agent een runner heeft
            
            # Standalone runner file
            runner_src = repo_path / "exports" / value_stream / "runners" / f"{agent_naam}.py"
            if runner_src.exists():
                runner_dst = workspace_root / "scripts" / f"{agent_naam}.py"
                runner_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(runner_src, runner_dst)
                artifacts.append(runner_dst)
                runner_found = True
            
            # Runner module folder (indien aanwezig)
            runner_module_src = repo_path / "exports" / value_stream / "runners" / agent_naam
            if runner_module_src.exists() and runner_module_src.is_dir():
                runner_module_dst = workspace_root / "scripts" / agent_naam
                
                # BELANGRIJK: Verwijder bestaande module VOLLEDIG (niet mergen!)
                # Dit is by design - workspace krijgt de canonieke versie uit agent-services.
                # Als workspace-folder 2 files heeft en agent-services 1 file,
                # blijven na fetch alleen het 1 file uit agent-services over.
                if runner_module_dst.exists():
                    try:
                        shutil.rmtree(runner_module_dst)
                    except (PermissionError, OSError) as e:
                        raise PolicyError(
                            f"Kan bestaande runner module niet verwijderen: {runner_module_dst}\n"
                            f"Fout: {e}\n"
                            f"Tip: Sluit programma's die deze files gebruiken."
                        )
                
                # Kopieer module
                shutil.copytree(runner_module_src, runner_module_dst)
                artifacts.append(runner_module_dst)
                runner_found = True
                
                # Valideer module heeft __init__.py
                init_file = runner_module_dst / "__init__.py"
                if not init_file.exists():
                    print(f"[WARNING] Runner module {agent_naam}/ heeft geen __init__.py", file=sys.stderr)
            
            # Tel als 1 runner (ongeacht file/module structuur)
            if runner_found:
                runners_count += 1
        
        # Genereer manifest
        manifest_dst = workspace_root / "docs" / "agents-manifest.md"
        manifest_dst.parent.mkdir(parents=True, exist_ok=True)
        
        manifest_lines = [
            f"# Agents Manifest\n\n",
            f"**Datum**: {datetime.now().strftime('%Y-%m-%d')}\n",
            f"**Value Stream**: {value_stream}\n",
            f"**Branch**: {branch}\n",
            f"**Bron**: {agent_services_url}\n\n",
            f"## Geïnstalleerde Agents ({installed_count})\n\n",
        ]
        
        for agent in filtered_agents:
            manifest_lines.append(f"- **{agent.get('naam')}**: {agent.get('aantalPrompts', 0)} prompts")
            if include_runners and agent.get('aantalRunners', 0) > 0:
                manifest_lines.append(f", {agent.get('aantalRunners')} runners")
            manifest_lines.append("\n")
        
        manifest_lines.append(f"\n## Statistieken\n\n")
        manifest_lines.append(f"- Agents: {installed_count}\n")
        manifest_lines.append(f"- Prompts: {prompts_count}\n")
        manifest_lines.append(f"- Runners: {runners_count}\n")
        
        manifest_dst.write_text("".join(manifest_lines), encoding="utf-8")
        artifacts.append(manifest_dst)
        
        # Genereer fetch-log met timestamp
        logs_dir = workspace_root / "docs" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        log_timestamp = datetime.now()
        timestamp = log_timestamp.strftime("%Y%m%d-%H%M%S")
        log_dst = logs_dir / f"fetch-agents-{timestamp}.md"
        
        log_lines = [
            f"# Fetch Agents Log\n\n",
            f"**Datum**: {log_timestamp.strftime('%Y-%m-%d')}\n",
            f"**Tijd**: {log_timestamp.strftime('%H:%M:%S')}\n",
            f"**Value Stream**: {value_stream}\n",
            f"**Branch**: {branch}\n",
            f"**Repository**: {agent_services_url}\n\n",
            f"## Status\n\n",
            f"✓ SUCCESS: {installed_count} agents geïnstalleerd\n\n",
            f"## Geïnstalleerde Agents\n\n",
        ]
        
        for agent in filtered_agents:
            log_lines.append(
                f"- **{agent.get('naam')}**: "
                f"{agent.get('aantalPrompts', 0)} prompts"
            )
            if include_runners and agent.get('aantalRunners', 0) > 0:
                log_lines.append(f", {agent.get('aantalRunners')} runners")
            log_lines.append("\n")
        
        log_lines.append(f"\n## Totaal Statistieken\n\n")
        log_lines.append(f"| Categorie | Aantal |\n")
        log_lines.append(f"|-----------|--------|\n")
        log_lines.append(f"| Agents | {installed_count} |\n")
        log_lines.append(f"| Prompts | {prompts_count} |\n")
        log_lines.append(f"| Runners | {runners_count} |\n")
        log_lines.append(f"\n## Locaties\n\n")
        log_lines.append(f"- Charters: `charters-agents/`\n")
        log_lines.append(f"- Prompts: `.github/prompts/`\n")
        log_lines.append(f"- Runners: `scripts/`\n")
        log_lines.append(f"- Manifest: `docs/agents-manifest.md`\n")
        
        log_dst.write_text("".join(log_lines), encoding="utf-8")
        artifacts.append(log_dst)
    
    message = (
        f"Agents opgehaald: {installed_count} agents, {prompts_count} prompts, {runners_count} runners "
        f"(value-stream: {value_stream}, branch: {branch})"
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
    opdracht: str,
    check_only: bool,
    scope: str | None,
    aanleiding: str | None,
    gewenste_capability: str | None,
    value_stream: str | None,
    branch: str,
    agent_services_url: str,
    include_runners: bool,
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
    
    elif operation == "fetch-agents":
        return op_fetch_agents(
            workspace_root=workspace_root,
            opdracht=opdracht,
            value_stream=value_stream,
            branch=branch,
            agent_services_url=agent_services_url,
            include_runners=include_runners,
        )
    
    else:
        raise ValueError(f"Onbekende operatie: {operation}")
