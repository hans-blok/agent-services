#!/usr/bin/env python3
"""
Agent Curator Runner — Publiceer Agents Overzicht

Deze runner scant alle agent-charters, leest metadata uit de headers,
telt prompts en runners, en publiceert een overzicht in JSON en Markdown.

Usage:
    python scripts/runners/agent-curator.py --scope volledig
    python scripts/runners/agent-curator.py --scope value-stream --filter kennispublicatie
    python scripts/runners/agent-curator.py --help

Output:
    - agents-publicatie.json (root, voor fetching)
    - docs/resultaten/agent-publicaties/agents-publicatie-<datum>.md (archief)

Traceability:
    Charter: agent-charters/charter.agent-curator.md
    Prompt: .github/prompts/agent-curator-publiceer-agents-overzicht.prompt.md
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class AgentMetadata:
    """Metadata extracted from agent charter header."""
    naam: str
    value_stream: str
    domein: str = ""
    agent_soort: str = ""
    charter_path: Path = None
    aantal_prompts: int = 0
    aantal_runners: int = 0


def extract_header_field(content: str, field_name: str) -> str:
    """Extract a field value from charter header.
    
    Looks for pattern: **FieldName**: value
    """
    pattern = rf"\*\*{re.escape(field_name)}\*\*:\s*(.+?)(?:\n|$)"
    match = re.search(pattern, content, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def scan_charter(charter_path: Path) -> Optional[AgentMetadata]:
    """Scan a charter file and extract metadata from header."""
    try:
        content = charter_path.read_text(encoding="utf-8")
        
        # Extract required fields from header
        naam = extract_header_field(content, "Agent")
        value_stream = extract_header_field(content, "Value Stream")
        
        if not naam or not value_stream:
            print(f"[WARN] Charter missing required fields: {charter_path.name}")
            return None
        
        # Extract optional fields
        domein = extract_header_field(content, "Domein")
        agent_soort = extract_header_field(content, "Agent-soort")
        
        return AgentMetadata(
            naam=naam,
            value_stream=value_stream,
            domein=domein,
            agent_soort=agent_soort,
            charter_path=charter_path
        )
    except Exception as e:
        print(f"[ERROR] Failed to scan charter {charter_path}: {e}")
        return None


def count_prompts(agent_naam: str, workspace_root: Path) -> int:
    """Count prompts for an agent by scanning .github/prompts/ and exports/."""
    count = 0
    
    # Scan .github/prompts/
    prompts_dir = workspace_root / ".github" / "prompts"
    if prompts_dir.exists():
        pattern = f"{agent_naam}-*.prompt.md"
        count += len(list(prompts_dir.glob(pattern)))
    
    # Scan exports/*/prompts/
    exports_dir = workspace_root / "exports"
    if exports_dir.exists():
        for value_stream_dir in exports_dir.iterdir():
            if value_stream_dir.is_dir():
                vs_prompts = value_stream_dir / "prompts"
                if vs_prompts.exists():
                    pattern = f"{agent_naam}-*.prompt.md"
                    count += len(list(vs_prompts.glob(pattern)))
    
    return count


def count_runners(agent_naam: str, workspace_root: Path) -> int:
    """Count runners for an agent by scanning scripts/runners/."""
    runners_dir = workspace_root / "scripts" / "runners"
    if not runners_dir.exists():
        return 0
    
    count = 0
    
    # Individual runner script
    runner_file = runners_dir / f"{agent_naam}.py"
    if runner_file.exists():
        count += 1
    
    # Runner module folder
    runner_module = runners_dir / agent_naam
    if runner_module.exists() and runner_module.is_dir():
        count += 1
    
    return count


def scan_all_agents(workspace_root: Path) -> List[AgentMetadata]:
    """Scan all charters in agent-charters/ and exports/."""
    agents = []
    
    # Scan agent-charters/ (utility and agent-enablement)
    charters_dir = workspace_root / "agent-charters"
    if charters_dir.exists():
        for charter_file in charters_dir.glob("charter.*.md"):
            if charter_file.name == "charter-moeder.md":
                # Handle legacy naming
                charter_file_alt = charters_dir / "charter.moeder.md"
                if charter_file_alt.exists():
                    charter_file = charter_file_alt
            
            metadata = scan_charter(charter_file)
            if metadata:
                metadata.aantal_prompts = count_prompts(metadata.naam, workspace_root)
                metadata.aantal_runners = count_runners(metadata.naam, workspace_root)
                agents.append(metadata)
    
    # Scan exports/*/charters/ and exports/*/charters-agents/
    exports_dir = workspace_root / "exports"
    if exports_dir.exists():
        for value_stream_dir in exports_dir.iterdir():
            if not value_stream_dir.is_dir():
                continue
            
            # Try both charters/ and charters-agents/
            for charter_subdir in ["charters", "charters-agents"]:
                charters_vs = value_stream_dir / charter_subdir
                if charters_vs.exists():
                    for charter_file in charters_vs.glob("charter.*.md"):
                        metadata = scan_charter(charter_file)
                        if metadata:
                            metadata.aantal_prompts = count_prompts(metadata.naam, workspace_root)
                            metadata.aantal_runners = count_runners(metadata.naam, workspace_root)
                            agents.append(metadata)
    
    return agents


def generate_json(agents: List[AgentMetadata], workspace_root: Path) -> Dict:
    """Generate JSON structure for agents-publicatie.json."""
    # Collect unique value streams
    value_streams = sorted(set(agent.value_stream for agent in agents))
    
    # Build agents list
    agents_list = []
    for agent in sorted(agents, key=lambda a: a.naam):
        agents_list.append({
            "naam": agent.naam,
            "valueStream": agent.value_stream,
            "aantalPrompts": agent.aantal_prompts,
            "aantalRunners": agent.aantal_runners
        })
    
    # Build locaties structure
    locaties = {
        "charters": {
            "agent-enablement": "agent-charters/charter.<agent-naam>.md",
            "architectuur-en-oplossingsontwerp": "exports/architectuur-en-oplossingsontwerp/charters/charter.<agent-naam>.md",
            "default": "exports/<value-stream>/charters-agents/charter.<agent-naam>.md"
        },
        "prompts": {
            "agent-enablement": ".github/prompts/<agent-naam>-<werkwoord>.prompt.md",
            "architectuur-en-oplossingsontwerp": "exports/architectuur-en-oplossingsontwerp/prompts/<agent-naam>-<werkwoord>.prompt.md",
            "default": "exports/<value-stream>/prompts/<agent-naam>-<werkwoord>.prompt.md"
        },
        "runners": "scripts/runners/<agent-naam>.py"
    }
    
    return {
        "publicatiedatum": datetime.now().strftime("%Y-%m-%d"),
        "versie": "1.1",
        "agents": agents_list,
        "valueStreams": value_streams,
        "locaties": locaties
    }


def generate_markdown(agents: List[AgentMetadata], scope: str, filter_waarde: Optional[str] = None) -> str:
    """Generate Markdown archive with full metadata."""
    lines = []
    
    # Header
    lines.append(f"# Agents Publicatie Overzicht\n\n")
    lines.append(f"**Publicatiedatum**: {datetime.now().strftime('%Y-%m-%d')}\n")
    lines.append(f"**Tijdstip**: {datetime.now().strftime('%H:%M:%S')}\n")
    lines.append(f"**Scope**: {scope}\n")
    if filter_waarde:
        lines.append(f"**Filter**: {filter_waarde}\n")
    lines.append(f"**Totaal agents**: {len(agents)}\n\n")
    
    # Group by value stream
    by_stream = defaultdict(list)
    for agent in agents:
        by_stream[agent.value_stream].append(agent)
    
    # Generate tables per value stream
    for stream in sorted(by_stream.keys()):
        stream_agents = sorted(by_stream[stream], key=lambda a: a.naam)
        lines.append(f"## Value Stream: {stream}\n\n")
        lines.append(f"**Aantal agents**: {len(stream_agents)}\n\n")
        
        # Table
        lines.append("| Agent | Domein | Prompts | Runners |\n")
        lines.append("|-------|--------|---------|----------|\n")
        for agent in stream_agents:
            lines.append(f"| {agent.naam} | {agent.domein} | {agent.aantal_prompts} | {agent.aantal_runners} |\n")
        lines.append("\n")
    
    # Metadata
    lines.append("## Metadata\n\n")
    lines.append(f"- **Gescande folders**:\n")
    lines.append(f"  - `agent-charters/` (utility & agent-enablement)\n")
    lines.append(f"  - `exports/*/charters/` (value streams)\n")
    lines.append(f"  - `exports/*/charters-agents/` (value streams)\n")
    lines.append(f"  - `.github/prompts/` (prompts)\n")
    lines.append(f"  - `exports/*/prompts/` (value stream prompts)\n")
    lines.append(f"  - `scripts/runners/` (runners)\n")
    lines.append(f"- **Value stream bron**: Charter header (`**Value Stream**:` veld)\n")
    lines.append(f"- **Traceability**: Agent Curator charter, publiceer-agents-overzicht prompt\n")
    
    return "".join(lines)


def write_outputs(json_data: Dict, markdown_content: str, workspace_root: Path, scope: str, filter_waarde: Optional[str] = None):
    """Write JSON and Markdown outputs."""
    # Write JSON to root (only for volledig scope)
    if scope == "volledig":
        json_path = workspace_root / "agents-publicatie.json"
        json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[JSON] {json_path.relative_to(workspace_root)}")
    
    # Write Markdown to archive
    archive_dir = workspace_root / "docs" / "resultaten" / "agent-publicaties"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if scope == "volledig":
        md_filename = f"agents-publicatie-{timestamp}.md"
    elif scope == "value-stream":
        md_filename = f"agents-publicatie-{filter_waarde}-{timestamp}.md"
    elif scope == "agent-soort":
        md_filename = f"agents-publicatie-{filter_waarde}-{timestamp}.md"
    else:
        md_filename = f"agents-publicatie-{scope}-{timestamp}.md"
    
    md_path = archive_dir / md_filename
    md_path.write_text(markdown_content, encoding="utf-8")
    print(f"[MARKDOWN] {md_path.relative_to(workspace_root)}")


def main():
    """Main entry point for Agent Curator runner."""
    parser = argparse.ArgumentParser(
        description="Agent Curator — Publiceer Agents Overzicht"
    )
    parser.add_argument(
        "--scope",
        required=True,
        choices=["volledig", "value-stream", "agent-soort"],
        help="Publicatie scope"
    )
    parser.add_argument(
        "--filter",
        dest="filter_waarde",
        help="Filter waarde (value stream of agent-soort naam)"
    )
    parser.add_argument(
        "--include-drafts",
        action="store_true",
        help="Include agents in draft status"
    )
    
    args = parser.parse_args()
    
    # Validate filter requirement
    if args.scope in ["value-stream", "agent-soort"] and not args.filter_waarde:
        print(f"[ERROR] --filter is required when scope is '{args.scope}'", file=sys.stderr)
        return 1
    
    workspace_root = Path(__file__).parent.parent.parent
    
    print("Agent Curator — Publiceer Agents Overzicht")
    print("=" * 60)
    print(f"Scope: {args.scope}")
    if args.filter_waarde:
        print(f"Filter: {args.filter_waarde}")
    print()
    
    # Scan all agents
    print("[INFO] Scanning agent charters...")
    all_agents = scan_all_agents(workspace_root)
    print(f"[INFO] Found {len(all_agents)} agents")
    
    # Filter based on scope
    if args.scope == "value-stream":
        agents = [a for a in all_agents if a.value_stream == args.filter_waarde]
        if not agents:
            print(f"[WARN] No agents found for value stream '{args.filter_waarde}'")
    elif args.scope == "agent-soort":
        agents = [a for a in all_agents if a.agent_soort == args.filter_waarde]
        if not agents:
            print(f"[WARN] No agents found for agent-soort '{args.filter_waarde}'")
    else:
        agents = all_agents
    
    print(f"[INFO] Publishing {len(agents)} agents")
    
    # Generate outputs
    json_data = generate_json(agents, workspace_root)
    markdown_content = generate_markdown(agents, args.scope, args.filter_waarde)
    
    # Write outputs
    write_outputs(json_data, markdown_content, workspace_root, args.scope, args.filter_waarde)
    
    print("\n[SUCCESS] Agents overzicht gepubliceerd")
    return 0


if __name__ == "__main__":
    sys.exit(main())
