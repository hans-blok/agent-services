#!/usr/bin/env python3
"""
Fetch and organize agents from a remote GitHub repository.

Fetches agents from a specified value-stream in exports/ folder,
plus all utility agents, and organizes them locally:
  - Prompts → .github/prompts/
  - Charters → charters-agents/
  - Runners → scripts/

Usage:
    python fetch_agents.py <value-stream> [--source-repo <url>] [--no-git]

Example:
    python fetch_agents.py kennispublicatie
    python fetch_agents.py it-development --source-repo https://github.com/user/repo.git
"""

import os
import sys
import shutil
import argparse
import tempfile
import subprocess
from pathlib import Path
from typing import List, Tuple


def run_command(cmd: List[str], cwd: str = None, check: bool = True) -> str:
    """Execute shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {' '.join(cmd)}")
        print(f"        {e.stderr}")
        raise


def fetch_remote_repo(repo_url: str, temp_dir: str) -> str:
    """Clone remote repository into temp directory."""
    print(f"[CLONE] Cloning repository: {repo_url}")
    clone_path = os.path.join(temp_dir, "remote_repo")
    run_command(["git", "clone", repo_url, clone_path])
    return clone_path


def find_agents(repo_path: str, value_stream: str) -> Tuple[List[Path], List[Path]]:
    """
    Find agent files for value-stream and utility agents.
    Returns: (value_stream_files, utility_files)
    """
    exports_dir = Path(repo_path) / "exports"
    
    if not exports_dir.exists():
        raise FileNotFoundError(f"exports/ directory not found in {repo_path}")
    
    value_stream_files = []
    utility_files = []
    
    # Fetch value-stream specific agents
    vs_path = exports_dir / value_stream
    if vs_path.exists():
        print(f"[OK] Found value-stream folder: {value_stream}")
        value_stream_files.extend(_collect_agent_files(vs_path))
    else:
        print(f"[WARN] Value-stream folder not found: {value_stream}")
    
    # Fetch utility agents
    utility_path = exports_dir / "utility"
    if utility_path.exists():
        print(f"[OK] Found utility agents")
        utility_files.extend(_collect_agent_files(utility_path))
    else:
        print(f"[WARN] Utility agents folder not found")
    
    return value_stream_files, utility_files


def _collect_agent_files(base_path: Path) -> List[Path]:
    """Collect all agent-related files from a folder tree."""
    files = []
    
    # Prompts: *.prompt.md
    prompts_dir = base_path / "prompts"
    if prompts_dir.exists():
        files.extend(prompts_dir.glob("*.prompt.md"))
    
    # Charters: charter*.md (both charter.*.md and charter-*.md formats)
    charters_dir = base_path / "charters-agents"
    if charters_dir.exists():
        files.extend(charters_dir.glob("charter*.md"))
    
    # Runners: *.py (but not __init__.py or __pycache__)
    runners_dir = base_path / "runners"
    if runners_dir.exists():
        for py_file in runners_dir.glob("*.py"):
            if not py_file.name.startswith("__"):
                files.append(py_file)
    
    return files


def organize_agents(
    value_stream_files: List[Path],
    utility_files: List[Path],
    workspace_root: str
) -> None:
    """
    Organize fetched agents into local workspace structure.
    
    Structure:
      .github/prompts/          ← prompts
      charters-agents/          ← charters
      scripts/                  ← runners
    """
    workspace = Path(workspace_root)
    
    # Define target directories
    prompts_dir = workspace / ".github" / "prompts"
    charters_dir = workspace / "charters-agents"
    scripts_dir = workspace / "scripts"
    
    # Create directories if they don't exist
    prompts_dir.mkdir(parents=True, exist_ok=True)
    charters_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)
    
    all_files = value_stream_files + utility_files
    
    print(f"\n[INFO] Organizing {len(all_files)} agent files...")
    
    for src_file in all_files:
        if src_file.suffix == ".md":
            if "charter" in src_file.name:
                # Charter file → charters-agents/
                dest = charters_dir / src_file.name
                _copy_file(src_file, dest)
            elif "prompt" in src_file.name:
                # Prompt file → .github/prompts/
                dest = prompts_dir / src_file.name
                _copy_file(src_file, dest)
        elif src_file.suffix == ".py":
            # Runner file → scripts/
            dest = scripts_dir / src_file.name
            _copy_file(src_file, dest)


def _copy_file(src: Path, dest: Path) -> None:
    """Copy file with logging."""
    try:
        shutil.copy2(src, dest)
        rel_path = dest.relative_to(dest.parent.parent.parent)
        print(f"  [OK] {src.name} -> {rel_path}")
    except Exception as e:
        print(f"  [ERROR] Failed to copy {src.name}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and organize agents from remote GitHub repository"
    )
    parser.add_argument(
        "value_stream",
        help="Value-stream name (e.g., 'kennispublicatie', 'it-development')"
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
    
    args = parser.parse_args()
    
    if not args.value_stream:
        print("❌ value-stream argument is required")
        sys.exit(1)
    
    workspace_root = os.getcwd()
    
    # Create temporary directory for cloning
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Clone remote repo
            repo_path = fetch_remote_repo(args.source_repo, temp_dir)
            
            # Find agents
            vs_files, util_files = find_agents(repo_path, args.value_stream)
            
            if not vs_files and not util_files:
                print("[ERROR] No agents found")
                sys.exit(1)
            
            print(f"\n[SUMMARY]")
            print(f"  Value-stream agents: {len(vs_files)}")
            print(f"  Utility agents: {len(util_files)}")
            
            # Organize into workspace
            organize_agents(vs_files, util_files, workspace_root)
            
            print(f"\n[SUCCESS] Agents organized successfully in {workspace_root}")
            
        except Exception as e:
            print(f"\n[ERROR] {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
