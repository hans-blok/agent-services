#!/usr/bin/env python3
"""
Fetch and organize agents from agent-services using the manifest in repo root.
Supports Dutch manifest fields (agents-publicatie.json) as provided in agent-services.

BELANGRIJK - Overschrijfgedrag:
- Charters: Volledig overschreven met versie uit agent-services
- Prompts: Bestaande prompts met dezelfde naam overschreven; extra prompts behouden
- Runner module folders: Volledig verwijderd en vervangen (niet gemerged!)

Dit is by design: fetching installeert de canonieke versie uit agent-services.
Workspace-specifieke aanpassingen worden overschreven.

Usage:
    python fetch_agents.py kennispublicatie
    python fetch_agents.py --list
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class AgentSpec:
    name: str
    agent_type: str  # utility or value-stream
    value_streams: List[str] = field(default_factory=list)
    files: List[Path] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)

    def is_applicable_to(self, value_stream: str) -> bool:
        value_stream = value_stream.lower()
        if self.agent_type == "utility":
            return True if not self.value_streams or "*" in self.value_streams else value_stream in self.value_streams
        return value_stream in self.value_streams or "*" in self.value_streams


def run_command(cmd: List[str], cwd: Path | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout.strip()


def fetch_repo(repo_url: str, temp_dir: Path) -> Path:
    clone_path = temp_dir / "agent-services"
    run_command(["git", "clone", "--depth", "1", repo_url, str(clone_path)])
    return clone_path


def load_manifest(repo_path: Path, manifest_name: str) -> Tuple[List[AgentSpec], Dict[str, str], Dict[str, str]]:
    manifest_path = repo_path / manifest_name
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest '{manifest_name}' not found in repo root")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))

    agents_raw = data.get("agents", [])
    locaties = data.get("locaties", {})
    specs: List[AgentSpec] = []

    for idx, entry in enumerate(agents_raw):
        if not isinstance(entry, dict):
            raise ValueError(f"Agent entry {idx} must be object")
        naam = entry.get("naam") or entry.get("name")
        value_stream = entry.get("valueStream") or entry.get("value_stream")
        aantal_prompts = entry.get("aantalPrompts", 0)
        aantal_runners = entry.get("aantalRunners", 0)
        if not naam or not value_stream:
            raise ValueError(f"Agent entry {idx} missing naam/valueStream")

        agent_type = "utility" if value_stream.lower() == "utility" else "value-stream"
        files: List[Path] = []
        # charter
        if locaties.get("charters"):
            files.append(Path(locaties["charters"].replace("<value-stream>", value_stream).replace("<agent-naam>", naam)))
        # prompts (wildcard)
        if aantal_prompts > 0 and locaties.get("prompts"):
            files.append(Path(locaties["prompts"].replace("<value-stream>", value_stream).replace("<agent-naam>", naam).replace("<werkwoord>", "*")))
        # runner
        if aantal_runners > 0 and locaties.get("runners"):
            files.append(Path(locaties["runners"].replace("<value-stream>", value_stream).replace("<agent-naam>", naam)))

        specs.append(
            AgentSpec(
                name=str(naam),
                agent_type=agent_type,
                value_streams=["*"] if agent_type == "utility" else [value_stream.lower()],
                files=files,
                metadata={"aantalPrompts": str(aantal_prompts), "aantalRunners": str(aantal_runners)},
            )
        )

    meta = {
        "version": str(data.get("versie", "unspecified")),
        "published_at": str(data.get("publicatiedatum", "unspecified")),
        "agent_count": str(len(specs)),
    }
    return specs, meta, locaties


def derive_streams(specs: List[AgentSpec]) -> List[str]:
    streams = set()
    for s in specs:
        for vs in s.value_streams:
            if vs and vs != "*":
                streams.add(vs)
    return sorted(streams)


def filter_agents(specs: List[AgentSpec], value_stream: str) -> Tuple[List[AgentSpec], List[AgentSpec]]:
    applicable: List[AgentSpec] = []
    skipped: List[AgentSpec] = []
    for spec in specs:
        if spec.is_applicable_to(value_stream):
            applicable.append(spec)
        else:
            skipped.append(spec)
    return applicable, skipped


def resolve_files(repo_path: Path, specs: List[AgentSpec]) -> Tuple[List[Path], List[Path], List[Path], List[str]]:
    """Resolve agent files. Returns (vs_files, util_files, runner_modules, missing).
    
    runner_modules zijn directories die volledig moeten worden overschreven.
    """
    vs_files: List[Path] = []
    util_files: List[Path] = []
    runner_modules: List[Path] = []  # Module folders to replace entirely
    missing: List[str] = []

    for spec in specs:
        bucket = util_files if spec.agent_type == "utility" else vs_files
        for rel in spec.files:
            if "*" in rel.name:
                parent = (repo_path / rel).parent
                if not parent.exists():
                    missing.append(f"{spec.name}: dir missing {parent.relative_to(repo_path)}")
                    continue
                pattern = rel.name
                matches = list(parent.glob(pattern))
                if not matches:
                    if int(spec.metadata.get("aantalPrompts", "0")) > 0:
                        missing.append(f"{spec.name}: no files match {rel}")
                    continue
                bucket.extend(matches)
            else:
                abs_path = repo_path / rel
                if not abs_path.exists():
                    missing.append(f"{spec.name}: file missing {rel}")
                    continue
                # If runner is a package directory, mark for full replacement
                if abs_path.is_dir() and "runners" in abs_path.parts:
                    runner_modules.append(abs_path)
                elif abs_path.is_dir():
                    # Non-runner directory, copy all py inside
                    bucket.extend(abs_path.rglob("*.py"))
                else:
                    bucket.append(abs_path)
    return vs_files, util_files, runner_modules, missing


def _copy_file(src: Path, dest: Path) -> str:
    try:
        if dest.exists():
            if dest.is_file() and src.read_bytes() == dest.read_bytes():
                status = "unchanged"
            else:
                status = "updated"
        else:
            status = "new"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"  [{status.upper():9}] {src.name} -> {dest.relative_to(dest.parent.parent.parent)}")
        return status
    except Exception as e:
        print(f"  [ERROR] Failed to copy {src}: {e}")
        return "error"


def organize(vs_files: List[Path], util_files: List[Path], runner_modules: List[Path], workspace: Path) -> Dict[str, int]:
    """Organize files into workspace. Runner modules are replaced entirely."""
    prompts_dir = workspace / ".github" / "prompts"
    charters_dir = workspace / "charters-agents"
    scripts_dir = workspace / "scripts"
    stats = {"new": 0, "updated": 0, "unchanged": 0, "error": 0, "modules_replaced": 0}

    all_files = vs_files + util_files
    print(f"\n[INFO] Organizing {len(all_files)} files + {len(runner_modules)} runner modules...")
    print(f"       Value-stream files: {len(vs_files)}")
    print(f"       Utility files: {len(util_files)}")
    print(f"       Runner modules: {len(runner_modules)}")

    # Handle runner modules first - FULL REPLACEMENT
    for module_src in runner_modules:
        module_name = module_src.name
        module_dst = scripts_dir / module_name
        
        try:
            # BELANGRIJK: Verwijder bestaande module VOLLEDIG (niet mergen!)
            # Als workspace-folder 2 files heeft en agent-services 1 file,
            # blijven na fetch alleen het 1 file uit agent-services over.
            if module_dst.exists():
                print(f"  [REPLACE] Removing existing {module_name}/ before copy")
                shutil.rmtree(module_dst)
            
            # Copy entire module
            shutil.copytree(module_src, module_dst)
            print(f"  [MODULE] {module_name}/ -> {module_dst.relative_to(workspace)}")
            stats["modules_replaced"] += 1
            
            # Validate __init__.py exists
            init_file = module_dst / "__init__.py"
            if not init_file.exists():
                print(f"  [WARNING] Runner module {module_name}/ has no __init__.py")
                
        except Exception as e:
            print(f"  [ERROR] Failed to replace module {module_name}: {e}")
            stats["error"] += 1

    # Handle individual files
    for src in all_files:
        dest = None
        if src.suffix == ".md":
            if "charter" in src.name.lower():
                dest = charters_dir / src.name
            elif "prompt" in src.name.lower():
                dest = prompts_dir / src.name
        elif src.suffix == ".py":
            # Check if this file is part of a module we already replaced
            is_in_module = any(module_src in src.parents for module_src in runner_modules)
            if is_in_module:
                continue  # Skip, already handled by module copy
            
            # Standalone runner script
            dest = scripts_dir / src.name

        if dest:
            status = _copy_file(src, dest)
            if status in stats:
                stats[status] += 1
        else:
            print(f"  [SKIP] {src}")
    return stats


def sync_self_script(repo_path: Path, workspace: Path) -> str:
    """Update the local fetch_agents.py from the source repo if available."""
    src = repo_path / "scripts" / "fetch_agents.py"
    dest = workspace / "scripts" / "fetch_agents.py"

    if not src.exists():
        return "missing"

    try:
        if dest.exists() and src.read_bytes() == dest.read_bytes():
            status = "unchanged"
        elif dest.exists():
            status = "updated"
        else:
            status = "new"

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        return status
    except Exception:
        return "error"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch agents via manifest")
    parser.add_argument("value_stream", nargs="?", help="Target value-stream")
    parser.add_argument("--manifest", default="agents-publicatie.json")
    parser.add_argument("--source-repo", default="https://github.com/hans-blok/agent-services.git")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--no-cleanup", action="store_true")
    args = parser.parse_args()

    value_stream = args.value_stream.strip("'\"") if args.value_stream else None
    workspace = Path(os.getcwd())

    tmp_ctx = tempfile.TemporaryDirectory()
    tmp_dir = Path(tmp_ctx.name)

    try:
        repo = fetch_repo(args.source_repo, tmp_dir)
        specs, meta, _loc = load_manifest(repo, args.manifest)
        streams = derive_streams(specs)

        if args.list:
            print("Available streams:")
            for s in streams:
                applicable, _ = filter_agents(specs, s)
                print(f"  - {s} ({len(applicable)} agents)")
            print(f"  - utility (always included for utility agents)")
            print(f"Manifest version: {meta['version']} published: {meta['published_at']}")
            return 0

        if not value_stream:
            print("[ERROR] value-stream argument is required (or use --list)")
            return 1

        if streams and value_stream.lower() not in streams and value_stream.lower() != "utility":
            print(f"[WARN] Value-stream '{value_stream}' not in manifest streams: {', '.join(streams)}")

        applicable, skipped = filter_agents(specs, value_stream)
        if not applicable:
            print("[ERROR] No applicable agents")
            return 1

        vs_files, util_files, runner_modules, missing = resolve_files(repo, applicable)
        if missing:
            print("[WARN] Missing files:")
            for m in missing:
                print(f"  - {m}")

        if not vs_files and not util_files and not runner_modules:
            print("[ERROR] No files resolved")
            return 1

        stats = organize(vs_files, util_files, runner_modules, workspace)

        # Sync this script from source of truth (agent-services)
        self_status = sync_self_script(repo, workspace)

        print("\nSUMMARY")
        print(f"Value-stream: {value_stream}")
        print(f"Manifest version: {meta['version']} published: {meta['published_at']}")
        print(f"Agents applied: {len(applicable)}")
        for spec in applicable:
            print(f"  - {spec.name} ({spec.agent_type})")
        if skipped:
            print(f"Agents skipped: {len(skipped)}")
        print(f"Files copied -> new: {stats['new']}, updated: {stats['updated']}, unchanged: {stats['unchanged']}, errors: {stats['error']}")
        if stats.get('modules_replaced', 0) > 0:
            print(f"Runner modules replaced: {stats['modules_replaced']} (⚠️  old content removed)")
        if self_status != "missing":
            print(f"fetch_agents.py sync: {self_status}")
        print("[SUCCESS] Agents fetched")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1
    finally:
        if not args.no_cleanup:
            tmp_ctx.cleanup()
        else:
            print(f"[DEBUG] Temp dir retained: {tmp_dir}")


if __name__ == "__main__":
    raise SystemExit(main())
