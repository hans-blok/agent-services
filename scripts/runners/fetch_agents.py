#!/usr/bin/env python3
"""
Fetch and organize agents from a remote GitHub repository using manifest-driven selection.

This script reads the agents-publicatie.json manifest from the root of the
remote repository (agent-services) to determine which agents are applicable
to the requested value-stream. It then copies only the relevant files into
the local workspace structure.

The manifest-driven approach ensures:
  - Consistent versioning and traceability
  - Clear agent applicability rules per value-stream
  - No implicit folder scanning or guesswork
  - Proper handling of universal utilities vs stream-specific agents

Directory mapping:
  - Prompts (*.prompt.md) → .github/prompts/
  - Charters (charter*.md) → charters-agents/
  - Runners (*.py) → scripts/

Usage:
    python fetch_agents.py <value-stream> [--manifest <name>] [--source-repo <url>]
    python fetch_agents.py --list

Examples:
    python fetch_agents.py kennispublicatie
    python fetch_agents.py it-development --source-repo https://github.com/user/repo.git
    python fetch_agents.py --list
    python fetch_agents.py kennispublicatie --manifest agents-v2.json

Dependencies:
    - Python 3.9+
    - git command-line tool
    - Standard library only (json, pathlib, subprocess, etc.)

Author: Python Expert Agent
Version: 2.0 (manifest-driven)
"""

import os
import sys
import json
import shutil
import filecmp
import argparse
import tempfile
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Optional


@dataclass
class AgentSpec:
    """Represents a single agent entry from the manifest.
    
    Attributes:
        name: Agent identifier (e.g., 'workflow-architect')
        agent_type: 'utility' or 'value-stream'
        value_streams: List of applicable streams, or ['*'] for universal
        files: List of relative file paths from repo root
        metadata: Additional metadata (version, status, etc.)
    """
    name: str
    agent_type: str
    value_streams: List[str] = field(default_factory=list)
    files: List[Path] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)

    def is_applicable_to(self, value_stream: str) -> bool:
        """Check if agent applies to the given value-stream."""
        value_stream = value_stream.lower()
        
        # Universal agents (empty list or wildcard)
        if not self.value_streams or "*" in self.value_streams:
            return True
        
        # Explicit match
        return value_stream in self.value_streams


def run_command(cmd: List[str], cwd: Optional[str] = None, check: bool = True) -> str:
    """Execute shell command and return output.
    
    Args:
        cmd: Command and arguments as list
        cwd: Working directory for command execution
        check: Raise exception on non-zero exit code
        
    Returns:
        Standard output of the command (stripped)
        
    Raises:
        subprocess.CalledProcessError: If command fails and check=True
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check,
            encoding="utf-8"
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {' '.join(cmd)}")
        print(f"        Exit code: {e.returncode}")
        if e.stderr:
            print(f"        {e.stderr}")
        raise


def fetch_remote_repo(repo_url: str, temp_dir: str) -> Path:
    """Clone remote repository into temporary directory.
    
    Args:
        repo_url: Git repository URL
        temp_dir: Temporary directory path
        
    Returns:
        Path to cloned repository
        
    Raises:
        subprocess.CalledProcessError: If git clone fails
    """
    print(f"[CLONE] Fetching repository: {repo_url}")
    clone_path = Path(temp_dir) / "remote_repo"
    run_command(["git", "clone", "--depth", "1", repo_url, str(clone_path)])
    return clone_path


def load_manifest(repo_path: Path, manifest_name: str) -> Tuple[List[AgentSpec], Dict[str, str]]:
    """Load and parse the agents manifest from repository root.
    
    Expected JSON structure:
    {
      "version": "2026-01-18",
      "published_at": "2026-01-18T12:00:00Z",
      "agents": [
        {
          "name": "workflow-architect",
          "type": "utility",
          "value_streams": ["kennispublicatie", "it-development"],
          "files": [
            "exports/utility/prompts/workflow-architect.prompt.md",
            "exports/utility/charters-agents/charter.workflow-architect.md",
            "exports/utility/runners/workflow-architect.py"
          ],
          "status": "active",
          "version": "1.2.0"
        }
      ]
    }
    
    Args:
        repo_path: Path to cloned repository
        manifest_name: Name of manifest file (e.g., 'agents-publicatie.json')
        
    Returns:
        Tuple of (agent_specs, manifest_metadata)
        
    Raises:
        FileNotFoundError: If manifest doesn't exist
        ValueError: If manifest format is invalid
    """
    manifest_path = repo_path / manifest_name
    
    if not manifest_path.exists():
        available_files = [f.name for f in repo_path.iterdir() if f.is_file()]
        raise FileNotFoundError(
            f"Manifest '{manifest_name}' not found in repository root.\n"
            f"Expected location: {manifest_path}\n"
            f"Available files in root: {', '.join(available_files)}"
        )
    
    # Parse JSON
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Manifest '{manifest_name}' contains invalid JSON:\n"
            f"  Line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    
    # Validate structure
    if not isinstance(manifest_data, dict):
        raise ValueError("Manifest must be a JSON object at root level.")
    
    if "agents" not in manifest_data:
        raise ValueError(
            "Manifest must contain an 'agents' array.\n"
            f"Found keys: {', '.join(manifest_data.keys())}"
        )
    
    agents_raw = manifest_data["agents"]
    if not isinstance(agents_raw, list):
        raise ValueError(f"'agents' must be an array, got {type(agents_raw).__name__}")
    
    # Parse agent entries
    specs: List[AgentSpec] = []
    for idx, entry in enumerate(agents_raw):
        if not isinstance(entry, dict):
            raise ValueError(f"Agent entry {idx} must be an object, got {type(entry).__name__}")
        
        # Extract required fields (with fallback aliases)
        name = entry.get("name") or entry.get("agent")
        agent_type = entry.get("type") or entry.get("agent_type")
        
        if not name:
            raise ValueError(f"Agent entry {idx} missing required field: 'name'")
        if not agent_type:
            raise ValueError(f"Agent '{name}' missing required field: 'type'")
        
        # Extract optional fields
        value_streams = entry.get("value_streams") or entry.get("streams") or []
        files = entry.get("files") or []
        
        # Validate types
        if not isinstance(value_streams, list):
            raise ValueError(f"Agent '{name}': 'value_streams' must be a list")
        
        if not isinstance(files, list):
            raise ValueError(f"Agent '{name}': 'files' must be a list")
        
        if not files:
            print(f"[WARN] Agent '{name}' has no files listed in manifest")
        
        # Extract metadata (everything except known fields)
        reserved_fields = {
            "name", "agent", "type", "agent_type", 
            "value_streams", "streams", "files"
        }
        metadata = {
            k: str(v) for k, v in entry.items() 
            if k not in reserved_fields
        }
        
        # Create spec
        spec = AgentSpec(
            name=str(name),
            agent_type=str(agent_type).lower(),
            value_streams=[str(vs).lower() for vs in value_streams],
            files=[Path(f) for f in files],
            metadata=metadata
        )
        specs.append(spec)
    
    # Extract manifest metadata
    manifest_meta = {
        "version": str(manifest_data.get("version", "unspecified")),
        "published_at": str(manifest_data.get("published_at", "unspecified")),
        "agent_count": str(len(specs))
    }
    
    print(f"[OK] Loaded manifest: version {manifest_meta['version']}, {len(specs)} agents")
    
    return specs, manifest_meta


def derive_available_value_streams(specs: List[AgentSpec]) -> List[str]:
    """Extract all unique value-streams mentioned in manifest (excluding wildcards).
    
    Args:
        specs: List of agent specifications
        
    Returns:
        Sorted list of value-stream names
    """
    streams = set()
    for spec in specs:
        for vs in spec.value_streams:
            if vs and vs != "*":
                streams.add(vs.lower())
    return sorted(streams)


def filter_applicable_agents(
    specs: List[AgentSpec], 
    value_stream: str
) -> Tuple[List[AgentSpec], List[AgentSpec]]:
    """Filter agents into applicable vs skipped based on value-stream.
    
    Applicability rules:
      - Utility agents: apply if value_streams is empty, contains '*', or contains target
      - Value-stream agents: apply only if value_streams contains target or '*'
    
    Args:
        specs: All agent specifications from manifest
        value_stream: Target value-stream name
        
    Returns:
        Tuple of (applicable_agents, skipped_agents)
    """
    value_stream = value_stream.lower()
    applicable: List[AgentSpec] = []
    skipped: List[AgentSpec] = []
    
    for spec in specs:
        # Skip deprecated agents
        if spec.metadata.get("status", "active").lower() == "deprecated":
            skipped.append(spec)
            continue
        
        if spec.is_applicable_to(value_stream):
            applicable.append(spec)
        else:
            skipped.append(spec)
    
    return applicable, skipped


def resolve_agent_files(
    repo_path: Path, 
    specs: List[AgentSpec]
) -> Tuple[List[Path], List[Path], List[str]]:
    """Resolve file paths for agents and categorize by type.
    
    Args:
        repo_path: Path to cloned repository
        specs: Applicable agent specifications
        
    Returns:
        Tuple of (value_stream_files, utility_files, missing_file_warnings)
    """
    value_stream_files: List[Path] = []
    utility_files: List[Path] = []
    missing: List[str] = []
    
    for spec in specs:
        # Determine target bucket
        bucket = utility_files if spec.agent_type == "utility" else value_stream_files
        
        # Resolve each file path
        for rel_path in spec.files:
            abs_path = repo_path / rel_path
            
            if not abs_path.exists():
                missing.append(
                    f"Agent '{spec.name}': file not found '{rel_path}'"
                )
                continue
            
            bucket.append(abs_path)
    
    return value_stream_files, utility_files, missing


def organize_agents(
    value_stream_files: List[Path],
    utility_files: List[Path],
    workspace_root: Path
) -> Dict[str, int]:
    """Copy agent files into local workspace structure.
    
    Target directories:
      .github/prompts/     ← *.prompt.md files
      charters-agents/     ← charter*.md files
      scripts/             ← *.py files
    
    Args:
        value_stream_files: Files from value-stream agents
        utility_files: Files from utility agents
        workspace_root: Root of target workspace
        
    Returns:
        Statistics dict with counts per category
    """
    workspace = workspace_root if isinstance(workspace_root, Path) else Path(workspace_root)
    
    # Define target directories
    prompts_dir = workspace / ".github" / "prompts"
    charters_dir = workspace / "charters-agents"
    scripts_dir = workspace / "scripts"
    
    # Create directories
    prompts_dir.mkdir(parents=True, exist_ok=True)
    charters_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)
    
    # Combine all files
    all_files = value_stream_files + utility_files
    
    print(f"\n[INFO] Organizing {len(all_files)} files...")
    print(f"       Value-stream files: {len(value_stream_files)}")
    print(f"       Utility files: {len(utility_files)}")
    
    # Track statistics
    stats = {"new": 0, "updated": 0, "unchanged": 0, "error": 0}
    
    # Copy files to appropriate locations
    for src_file in all_files:
        dest = None
        
        if src_file.suffix == ".md":
            if "charter" in src_file.name.lower():
                dest = charters_dir / src_file.name
            elif "prompt" in src_file.name.lower():
                dest = prompts_dir / src_file.name
        elif src_file.suffix == ".py":
            dest = scripts_dir / src_file.name
        
        if dest:
            status = _copy_file(src_file, dest)
            stats[status] += 1
        else:
            print(f"  [SKIP] Unknown file type: {src_file.name}")
    
    return stats


def _copy_file(src: Path, dest: Path) -> str:
    """Copy file with change detection and logging.
    
    Args:
        src: Source file path
        dest: Destination file path
        
    Returns:
        Status string: 'new', 'updated', 'unchanged', or 'error'
    """
    try:
        # Determine status
        if dest.exists():
            if filecmp.cmp(src, dest, shallow=False):
                status = "unchanged"
            else:
                status = "updated"
        else:
            status = "new"
        
        # Copy file
        shutil.copy2(src, dest)
        
        # Log with relative path for readability
        try:
            rel_path = dest.relative_to(dest.parent.parent.parent)
        except ValueError:
            rel_path = dest
        
        status_label = status.upper()
        print(f"  [{status_label:10}] {src.name} → {rel_path}")
        
        return status
        
    except Exception as e:
        print(f"  [ERROR] Failed to copy {src.name}: {e}")
        return "error"


def write_audit_trail(
    workspace_root: Path,
    value_stream: str,
    manifest_meta: Dict[str, str],
    applicable_agents: List[AgentSpec],
    skipped_agents: List[AgentSpec],
    stats: Dict[str, int]
) -> None:
    """Write audit trail of fetch operation to JSON file.
    
    Args:
        workspace_root: Root of workspace
        value_stream: Target value-stream
        manifest_meta: Manifest metadata
        applicable_agents: Agents that were applied
        skipped_agents: Agents that were skipped
        stats: Copy statistics
    """
    audit_path = workspace_root / "temp" / "fetch-audit.json"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    
    audit_data = {
        "timestamp": datetime.now().isoformat(),
        "value_stream": value_stream,
        "manifest": manifest_meta,
        "agents_applied": [
            {
                "name": spec.name,
                "type": spec.agent_type,
                "streams": spec.value_streams,
                "file_count": len(spec.files),
                "version": spec.metadata.get("version", "unspecified")
            }
            for spec in applicable_agents
        ],
        "agents_skipped": [
            {
                "name": spec.name,
                "type": spec.agent_type,
                "reason": "not_applicable" if spec.metadata.get("status") != "deprecated" else "deprecated"
            }
            for spec in skipped_agents
        ],
        "statistics": stats
    }
    
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[AUDIT] Trail written to: {audit_path}")


def main() -> int:
    """Main entry point for fetch_agents script."""
    parser = argparse.ArgumentParser(
        description="Fetch agents from remote repository using manifest-driven selection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available value-streams
  python fetch_agents.py --list
  
  # Fetch agents for a value-stream
  python fetch_agents.py kennispublicatie
  
  # Use different manifest file
  python fetch_agents.py kennispublicatie --manifest agents-v2.json
  
  # Use different source repository
  python fetch_agents.py it-development --source-repo https://github.com/user/repo.git
        """
    )
    
    parser.add_argument(
        "value_stream",
        nargs="?",
        help="Value-stream name (e.g., 'kennispublicatie', 'it-development')"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available value-streams from manifest"
    )
    parser.add_argument(
        "--manifest",
        default="agents-publicatie.json",
        help="Manifest filename in repo root (default: agents-publicatie.json)"
    )
    parser.add_argument(
        "--source-repo",
        default="https://github.com/hans-blok/agent-services.git",
        help="Remote repository URL (default: hans-blok/agent-services)"
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Keep temporary clone directory for inspection"
    )
    parser.add_argument(
        "--no-audit",
        action="store_true",
        help="Skip writing audit trail to temp/fetch-audit.json"
    )
    
    args = parser.parse_args()
    
    # Strip quotes (CMD/PowerShell may pass them literally)
    value_stream = args.value_stream.strip("'\"") if args.value_stream else None
    
    workspace_root = Path(os.getcwd())
    
    # Create temporary directory for cloning
    temp_context = tempfile.TemporaryDirectory() if not args.no_cleanup else None
    temp_dir = temp_context.name if temp_context else tempfile.mkdtemp()
    
    try:
        # Fetch repository
        repo_path = fetch_remote_repo(args.source_repo, temp_dir)
        
        # Load manifest
        specs, manifest_meta = load_manifest(repo_path, args.manifest)
        available_streams = derive_available_value_streams(specs)
        
        # Handle --list flag
        if args.list:
            print("\n" + "=" * 60)
            print("AVAILABLE VALUE-STREAMS (from manifest)")
            print("=" * 60)
            
            if available_streams:
                for vs in available_streams:
                    # Count applicable agents
                    applicable, _ = filter_applicable_agents(specs, vs)
                    print(f"  • {vs:30} ({len(applicable)} agents)")
            else:
                print("  (no value-streams defined)")
            
            print("\nManifest metadata:")
            print(f"  Version: {manifest_meta.get('version')}")
            print(f"  Published: {manifest_meta.get('published_at')}")
            print(f"  Total agents: {manifest_meta.get('agent_count')}")
            
            return 0
        
        # Require value_stream for normal operation
        if not value_stream:
            print("[ERROR] value-stream argument is required")
            print("        Use --list to see available value-streams")
            return 1
        
        # Warn if value-stream not in manifest
        if available_streams and value_stream.lower() not in available_streams:
            print(f"[WARN] Value-stream '{value_stream}' not explicitly listed in manifest")
            print("       Available streams:")
            for vs in available_streams:
                print(f"         • {vs}")
            print()
        
        # Filter applicable agents
        applicable_agents, skipped_agents = filter_applicable_agents(specs, value_stream)
        
        if not applicable_agents:
            print(f"[ERROR] No agents applicable to value-stream '{value_stream}'")
            if skipped_agents:
                print("\nAgents in manifest (but not applicable):")
                for spec in skipped_agents:
                    print(f"  • {spec.name} ({spec.agent_type})")
            return 1
        
        # Resolve files
        vs_files, util_files, missing_files = resolve_agent_files(repo_path, applicable_agents)
        
        if missing_files:
            print("\n[WARN] Files referenced in manifest but missing from repository:")
            for msg in missing_files:
                print(f"       • {msg}")
            print()
        
        if not vs_files and not util_files:
            print("[ERROR] No files found for applicable agents")
            return 1
        
        # Organize into workspace
        stats = organize_agents(vs_files, util_files, workspace_root)
        
        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Value-stream: {value_stream}")
        print(f"Manifest version: {manifest_meta.get('version')}")
        print(f"Manifest published: {manifest_meta.get('published_at')}")
        print()
        print(f"Agents applied: {len(applicable_agents)}")
        for spec in applicable_agents:
            print(f"  • {spec.name} ({spec.agent_type})")
        
        if skipped_agents:
            print(f"\nAgents skipped: {len(skipped_agents)}")
            for spec in skipped_agents[:5]:  # Limit to first 5
                reason = spec.metadata.get("status", "not applicable")
                print(f"  • {spec.name} ({reason})")
            if len(skipped_agents) > 5:
                print(f"  ... and {len(skipped_agents) - 5} more")
        
        print(f"\nFiles copied:")
        print(f"  New:       {stats['new']}")
        print(f"  Updated:   {stats['updated']}")
        print(f"  Unchanged: {stats['unchanged']}")
        if stats['error'] > 0:
            print(f"  Errors:    {stats['error']}")
        
        # Write audit trail
        if not args.no_audit:
            write_audit_trail(
                workspace_root, 
                value_stream, 
                manifest_meta,
                applicable_agents, 
                skipped_agents, 
                stats
            )
        
        print("\n[SUCCESS] Agents fetched and organized successfully")
        return 0
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        return 1
    except ValueError as e:
        print(f"\n[ERROR] Invalid manifest: {e}")
        return 1
    except subprocess.CalledProcessError:
        print("\n[ERROR] Git operation failed")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if temp_context:
            temp_context.cleanup()
        elif args.no_cleanup:
            print(f"\n[DEBUG] Temporary directory preserved: {temp_dir}")


if __name__ == "__main__":
    sys.exit(main())
