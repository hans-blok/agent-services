#!/usr/bin/env python3
"""Kopieer agent-artefacten naar een andere workspace.

Dit script kopieert alle relevante artefacten van een specifieke agent naar een
doelworkspace binnen c:/gitrepo. Het identificeert automatisch de artefacten op
basis van de agentnaam en kopieert:

- GitHub prompts (.github/prompts/*.prompt.md)
- Rolbeschrijvingen (charters-agents/*.md)
- Python runners (scripts/*.py)
- Agent modules (scripts/<agent_name>/)

Het script voert alleen lokale kopieer-acties uit zonder Git- of GitHub-operaties.

Usage:
    python copy_agent.py <agentnaam> <doelworkspace>
    python copy_agent.py vertaler agentische-systemen
    python copy_agent.py moeder production-workspace
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Tuple
import shutil


def ensure_dir(path: Path) -> None:
    """Zorg dat de doelmap bestaat.
    
    Args:
        path: Het pad naar de map die aangemaakt moet worden.
    """
    path.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dest: Path) -> None:
    """Kopieer één bestand naar dest, maak de doelmap indien nodig.
    
    Args:
        src: Het bronbestand dat gekopieerd moet worden.
        dest: Het doelpad waar het bestand naartoe gekopieerd moet worden.
    """
    ensure_dir(dest.parent)
    shutil.copy2(src, dest)


def copy_directory(src: Path, dest: Path) -> None:
    """Kopieer een hele directory recursief.
    
    Args:
        src: De bronmap die gekopieerd moet worden.
        dest: Het doelpad waar de map naartoe gekopieerd moet worden.
    """
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def find_agent_artifacts(
    agent_name: str,
    workspace_root: Path
) -> List[Tuple[Path, str]]:
    """Zoek alle artefacten van een specifieke agent.
    
    Args:
        agent_name: De naam van de agent (bijv. 'vertaler', 'moeder').
        workspace_root: Het pad naar de root van de workspace.
    
    Returns:
        Lijst van tuples (bronpad, relatief_doelpad).
    """
    artifacts: List[Tuple[Path, str]] = []
    
    # Zoek prompt bestanden in .github/prompts/
    prompts_dir = workspace_root / ".github" / "prompts"
    if prompts_dir.exists():
        for prompt_file in prompts_dir.glob(f"{agent_name}-*.prompt.md"):
            rel_path = f".github/prompts/{prompt_file.name}"
            artifacts.append((prompt_file, rel_path))
    
    # Zoek charter/rolbeschrijving in charters-agents/
    charters_dir = workspace_root / "charters-agents"
    if charters_dir.exists():
        # Zoek charter.<agent_name>.md
        charter_file = charters_dir / f"charter.{agent_name}.md"
        if charter_file.exists():
            artifacts.append((charter_file, f"charters-agents/{charter_file.name}"))
        
        # Zoek charter-<agent_name>.md (alternatieve naamgeving)
        charter_file_alt = charters_dir / f"charter-{agent_name}.md"
        if charter_file_alt.exists():
            artifacts.append((charter_file_alt, f"charters-agents/{charter_file_alt.name}"))
        
        # Zoek standalone <agent_name>.md
        standalone_file = charters_dir / f"{agent_name}.md"
        if standalone_file.exists():
            artifacts.append((standalone_file, f"charters-agents/{standalone_file.name}"))
    
    # Zoek Python runner in scripts/
    runner_file = workspace_root / "scripts" / f"{agent_name}.py"
    if runner_file.exists():
        artifacts.append((runner_file, f"scripts/{runner_file.name}"))
    
    # Zoek agent module directory in scripts/<agent_name>/
    agent_module_dir = workspace_root / "scripts" / agent_name.replace("-", "_")
    if agent_module_dir.exists() and agent_module_dir.is_dir():
        artifacts.append((agent_module_dir, f"scripts/{agent_module_dir.name}"))
    
    return artifacts


def copy_agent(
    agent_name: str,
    target_workspace: str,
    source_workspace: Path
) -> int:
    """Kopieer alle artefacten van een agent naar een doelworkspace.
    
    Args:
        agent_name: De naam van de agent die gekopieerd moet worden.
        target_workspace: De naam van de doelworkspace (binnen c:/gitrepo).
        source_workspace: Het pad naar de bronworkspace.
    
    Returns:
        0 bij succes, 1 bij foutieve invoer, 2 bij geen artefacten gevonden.
    """
    # Valideer doelworkspace
    target_root = Path(f"c:/gitrepo/{target_workspace}")
    
    # Vind alle artefacten
    artifacts = find_agent_artifacts(agent_name, source_workspace)
    
    if not artifacts:
        print(f"[FOUT] Geen artefacten gevonden voor agent '{agent_name}'", file=sys.stderr)
        print(f"Gezocht in: {source_workspace}", file=sys.stderr)
        return 2
    
    print(f"Gevonden {len(artifacts)} artefact(en) voor agent '{agent_name}':")
    
    # Kopieer alle artefacten
    copied_count = 0
    skipped_count = 0
    
    for src, rel_dest in artifacts:
        dest = target_root / rel_dest
        
        if not src.exists():
            print(f"[WAARSCHUWING] Bron ontbreekt, sla over: {src}")
            skipped_count += 1
            continue
        
        try:
            if src.is_dir():
                copy_directory(src, dest)
                print(f"[OK] Directory gekopieerd: {rel_dest}")
            else:
                copy_file(src, dest)
                print(f"[OK] Bestand gekopieerd: {rel_dest}")
            copied_count += 1
        except Exception as e:
            print(f"[FOUT] Kan niet kopiëren {src} -> {dest}: {e}", file=sys.stderr)
            skipped_count += 1
    
    print(f"\nSamenvatting: {copied_count} gekopieerd, {skipped_count} overgeslagen")
    print(f"Doel: {target_root}")
    
    return 0


def main() -> int:
    """Hoofdfunctie die argumenten parsed en de kopieer-actie uitvoert.
    
    Returns:
        Exit code: 0 bij succes, >0 bij fouten.
    """
    parser = argparse.ArgumentParser(
        description="Kopieer agent-artefacten naar een andere workspace.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Voorbeelden:
  %(prog)s vertaler agentische-systemen
  %(prog)s moeder production-workspace
  %(prog)s agent-smeder nieuwe-workspace

De doelworkspace moet zich bevinden in c:/gitrepo/<workspace-naam>.
        """
    )
    
    parser.add_argument(
        "agent_name",
        help="Naam van de agent die gekopieerd moet worden (bijv. 'vertaler', 'moeder')"
    )
    
    parser.add_argument(
        "target_workspace",
        help="Naam van de doelworkspace binnen c:/gitrepo/"
    )
    
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Bronworkspace (standaard: huidige workspace)"
    )
    
    args = parser.parse_args()
    
    # Bepaal bronworkspace
    if args.source:
        source_workspace = args.source.resolve()
    else:
        # Standaard: ga uit van scripts/ subdirectory in de workspace
        source_workspace = Path(__file__).resolve().parent.parent
    
    if not source_workspace.exists():
        print(f"[FOUT] Bronworkspace niet gevonden: {source_workspace}", file=sys.stderr)
        return 1
    
    # Valideer doelworkspace naam (geen path separators toegestaan)
    if "/" in args.target_workspace or "\\" in args.target_workspace:
        print(
            f"[FOUT] Doelworkspace mag geen pad-separators bevatten: '{args.target_workspace}'",
            file=sys.stderr
        )
        print("Gebruik alleen de workspace-naam, bijv. 'agentische-systemen'", file=sys.stderr)
        return 1
    
    return copy_agent(args.agent_name, args.target_workspace, source_workspace)


if __name__ == "__main__":
    sys.exit(main())
