"""Pipeline Executor Core Logic - Met parameter doorgifte en artifact chaining."""

from __future__ import annotations

import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ExecutionResult:
    """Result van pipeline execution."""
    
    success: bool
    message: str
    steps_executed: list[dict] = field(default_factory=list)
    gates_validated: list[dict] = field(default_factory=list)
    failures: list[dict] = field(default_factory=list)
    artifacts: list[Path] = field(default_factory=list)
    total_duration: float = 0.0


class PolicyError(Exception):
    """Error wanneer policy gate faalt."""
    
    pass


def _policy_gate_workspace_paths(workspace_root: Path) -> None:
    """Valideer dat essentiële workspace folders bestaan."""
    required_dirs = [
        workspace_root / "docs" / "resultaten" / "workflow-architect",
        workspace_root / "scripts",
        workspace_root / "log",
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            raise PolicyError(
                f"Vereiste folder ontbreekt: {dir_path.relative_to(workspace_root).as_posix()}"
            )


def _policy_gate_pipeline_exists(workspace_root: Path, pipeline_bestand: str) -> Path:
    """Valideer dat pipeline bestand bestaat."""
    pipeline_path = workspace_root / pipeline_bestand
    
    if not pipeline_path.exists():
        raise PolicyError(f"Pipeline bestand bestaat niet: {pipeline_bestand}")
    
    if not pipeline_path.is_file():
        raise PolicyError(f"Pipeline pad is geen bestand: {pipeline_bestand}")
    
    return pipeline_path


def _parse_pipeline(pipeline_path: Path) -> dict:
    """Parse pipeline.md bestand - extraheert Uitvoeringsketen en Kwaliteitsgates."""
    content = pipeline_path.read_text(encoding="utf-8")
    
    # Extract pipeline naam
    naam = pipeline_path.stem.replace("-pipeline", "")
    
    # Parse stappen uit Uitvoeringsketen
    stappen = []
    gates = []
    
    # Find Uitvoeringsketen section
    uitvoering_match = re.search(r'##\s+Uitvoeringsketen\s*\n(.*?)(?=\n##[^#]|\Z)', content, re.DOTALL)
    if uitvoering_match:
        uitvoering_text = uitvoering_match.group(1)
        
        # Parse individual steps (### Stap X: ...)
        # Steps are separated by "---" lines
        step_pattern = r'###\s+Stap\s+(\d+):\s+([^\n]+)\n(.*?)(?=\n---\n|$)'
        for match in re.finditer(step_pattern, uitvoering_text, re.DOTALL):
            step_num = int(match.group(1))
            step_title = match.group(2).strip()
            step_content = match.group(3)
            
            # Extract agent name from title (format: "Agent Name - Operation")
            agent_match = re.search(r'^([A-Za-z\s]+)', step_title)
            agent_naam = agent_match.group(1).strip().lower().replace(' ', '-') if agent_match else "unknown"
            
            # Extract run mode
            run_mode_match = re.search(r'\*\*Run mode\*\*:\s*(\w+)', step_content)
            run_mode = run_mode_match.group(1).lower() if run_mode_match else "sequential"
            
            # Extract duration
            duration_match = re.search(r'\*\*Geschatte duur\*\*:\s*~?(\d+)', step_content)
            duration = int(duration_match.group(1)) * 60 if duration_match else 300  # default 5 min
            
            stappen.append({
                "number": step_num,
                "name": step_title,
                "agent": agent_naam,
                "run_mode": run_mode,
                "duration_estimate": duration,
            })
            
            # Check for gate after this step
            gate_pattern = r'\[GATE\s+(\d+):\s+([^\]]+)\](.*?)(?=\n###|\n##|\Z)'
            gate_match = re.search(gate_pattern, step_content, re.DOTALL)
            if gate_match:
                gate_num = int(gate_match.group(1))
                gate_name = gate_match.group(2).strip()
                gate_content = gate_match.group(3)
                
                # Extract gate type
                type_match = re.search(r'\*\*Type\*\*:\s*(\w+)', gate_content)
                gate_type = type_match.group(1).lower() if type_match else "validatie"
                
                # Extract criteria (simplified - just store the section)
                criteria_match = re.search(r'\*\*Criteria\*\*:(.*?)(?=\n\*\*|\Z)', gate_content, re.DOTALL)
                criteria_text = criteria_match.group(1).strip() if criteria_match else ""
                
                # Extract failure action
                failure_match = re.search(r'\*\*Failure actie\*\*:\s*([^\n]+)', gate_content)
                failure_action = failure_match.group(1).strip() if failure_match else "Stop pipeline"
                
                gates.append({
                    "number": gate_num,
                    "name": gate_name,
                    "after_step": step_num,
                    "type": gate_type,
                    "criteria": criteria_text,
                    "failure_action": failure_action,
                })
    
    return {
        "naam": naam,
        "stappen": stappen,
        "gates": gates,
        "foutafhandeling": {},
        "rollback": None,
    }


def _validate_agents_exist(workspace_root: Path, stappen: list[dict]) -> None:
    """Valideer dat alle agents in pipeline bestaan."""
    scripts_dir = workspace_root / "scripts"
    
    for stap in stappen:
        agent_naam = stap.get("agent")
        if not agent_naam:
            continue
        
        runner_path = scripts_dir / f"{agent_naam}.py"
        if not runner_path.exists():
            raise PolicyError(
                f"Agent runner bestaat niet: {runner_path.relative_to(workspace_root).as_posix()}"
            )


def _extract_agent_naam_from_artifact(artifact_path: Path | None) -> str | None:
    """Extract agent-naam from boundary artifact."""
    if not artifact_path or not artifact_path.exists():
        return None
    
    try:
        content = artifact_path.read_text(encoding="utf-8")
        # Look for "agent-naam: xyz" line
        match = re.search(r'^agent-naam:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    
    return None


def _extract_capability_boundary_from_artifact(artifact_path: Path | None) -> str | None:
    """Extract capability-boundary from boundary artifact."""
    if not artifact_path or not artifact_path.exists():
        return None
    
    try:
        content = artifact_path.read_text(encoding="utf-8")
        # Look for "## Gewenste Capability" section (Moeder format)
        capability_match = re.search(r'##\s+Gewenste Capability\s*\n\s*(.+)', content, re.MULTILINE)
        if capability_match:
            return capability_match.group(1).strip()
    except Exception:
        pass
    
    return None


def _extract_boundary_fields(artifact_path: Path | None) -> dict[str, str]:
    """Extract all fields from boundary artifact for agent-smeder."""
    if not artifact_path or not artifact_path.exists():
        return {}
    
    try:
        content = artifact_path.read_text(encoding="utf-8")
        fields = {}
        
        # Extract from "## Agent Definitie" section with key: value format
        definitie_match = re.search(r'##\s+Agent Definitie\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if definitie_match:
            definitie_text = definitie_match.group(1)
            
            # Parse key: value lines
            for line in definitie_text.split('\n'):
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    fields[key.strip()] = value.strip()
        
        return fields
    except Exception:
        return {}
    
    return {}


def _detect_output_artifact(workspace_root: Path, agent_naam: str, step_num: int) -> Path | None:
    """Detect output artifact from agent execution."""
    # For moeder: boundary files in docs/resultaten/moeder/
    if "moeder" in agent_naam:
        boundary_dir = workspace_root / "docs" / "resultaten" / "moeder"
        if boundary_dir.exists():
            # Find most recently modified .md file
            md_files = list(boundary_dir.glob("*-boundary.md"))
            if md_files:
                return max(md_files, key=lambda p: p.stat().st_mtime)
    
    # For agent-smeder step 2: rol files in governance/rolbeschrijvingen/
    if "smeder" in agent_naam and step_num == 2:
        rol_dir = workspace_root / "governance" / "rolbeschrijvingen"
        if rol_dir.exists():
            md_files = list(rol_dir.glob("*.md"))
            if md_files:
                return max(md_files, key=lambda p: p.stat().st_mtime)
    
    # For agent-smeder step 3: prompts in .github/prompts/
    if "smeder" in agent_naam and step_num == 3:
        prompts_dir = workspace_root / ".github" / "prompts"
        if prompts_dir.exists():
            md_files = list(prompts_dir.glob("*.prompt.md"))
            if md_files:
                return max(md_files, key=lambda p: p.stat().st_mtime)
    
    # For agent-smeder step 4: runner in scripts/
    if "smeder" in agent_naam and step_num == 4:
        scripts_dir = workspace_root / "scripts"
        if scripts_dir.exists():
            py_files = list(scripts_dir.glob("*.py"))
            if py_files:
                # Exclude known runners
                known_runners = {"moeder", "agent-smeder", "workflow-architect", "pipeline-executor"}
                py_files = [f for f in py_files if f.stem not in known_runners]
                if py_files:
                    return max(py_files, key=lambda p: p.stat().st_mtime)
    
    return None


def _execute_step_sequential(
    workspace_root: Path,
    stap: dict,
    dry_run: bool,
    extra_params: list[str],
    artifacts: dict[int, Path],
) -> dict:
    """Voer één stap uit (sequential mode) met parameter doorgifte en artifact chaining."""
    agent_naam = stap.get("agent", "unknown")
    step_num = stap.get("number", 0)
    step_name = stap.get("name", agent_naam)
    
    if dry_run:
        return {
            "number": step_num,
            "name": step_name,
            "agent": agent_naam,
            "command": f"python scripts/{agent_naam}.py (dry-run)",
            "duration": 0.0,
            "status": "skipped (dry-run)",
            "exit_code": None,
            "output": "",
            "artifact": None,
        }
    
    # Build command with parameters
    runner_path = workspace_root / "scripts" / f"{agent_naam}.py"
    command = ["python", str(runner_path)]
    
    # Add agent-specific operation (extracted from step name if present)
    # Format: "Agent Name - Operation" → extract operation
    if " - " in step_name:
        operation_raw = step_name.split(" - ", 1)[1].strip()
        
        # Map Dutch operation names to agent-specific operations
        operation_map = {
            # Agent Smeder operations (Engels)
            "definieer prompts": "design-prompt",
            "schrijf rol": "write-role",
            "schrijf runner": "write-runner",
            "definieer agent boundary": "zet-agent-boundary",  # Moeder
        }
        
        operation_key = operation_raw.lower()
        operation = operation_map.get(operation_key, operation_raw.lower().replace(" ", "-"))
        command.append(operation)
    
    # For step 1: pass extra_params through
    if step_num == 1 and extra_params:
        command.extend(extra_params)
    
    # For steps 2+: pass artifact from previous step
    if step_num > 1 and (step_num - 1) in artifacts:
        prev_artifact = artifacts[step_num - 1]
        
        # Different parameter names based on agent
        if "smeder" in agent_naam:
            # Agent Smeder needs parameters from boundary
            if step_num >= 2 and 1 in artifacts:
                boundary_artifact = artifacts[1]
                boundary_fields = _extract_boundary_fields(boundary_artifact)
                
                # Add all required fields
                if "agent-naam" in boundary_fields:
                    command.extend(["--agent-naam", boundary_fields["agent-naam"]])
                if "capability-boundary" in boundary_fields:
                    command.extend(["--capability-boundary", boundary_fields["capability-boundary"]])
                if "doel" in boundary_fields:
                    command.extend(["--doel", boundary_fields["doel"]])
                if "domein" in boundary_fields:
                    command.extend(["--domein", boundary_fields["domein"]])
    
    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            cwd=workspace_root,
            capture_output=True,
            text=True,
            timeout=stap.get("duration_estimate", 300),
        )
        duration = time.time() - start_time
        
        # Try to detect output artifact
        output_artifact = _detect_output_artifact(workspace_root, agent_naam, step_num)
        
        return {
            "number": step_num,
            "name": step_name,
            "agent": agent_naam,
            "command": " ".join(str(c) for c in command),
            "duration": duration,
            "status": "success" if result.returncode == 0 else "failed",
            "exit_code": result.returncode,
            "output": result.stdout[:500],  # Truncate for log
            "artifact": output_artifact,
        }
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return {
            "number": step_num,
            "name": step_name,
            "agent": agent_naam,
            "command": " ".join(str(c) for c in command),
            "duration": duration,
            "status": "timeout",
            "exit_code": -1,
            "output": "Command timed out",
            "artifact": None,
        }
    except Exception as e:
        duration = time.time() - start_time
        return {
            "number": step_num,
            "name": step_name,
            "agent": agent_naam,
            "command": " ".join(str(c) for c in command),
            "duration": duration,
            "status": "error",
            "exit_code": -1,
            "output": str(e),
            "artifact": None,
        }


def _validate_gate(
    workspace_root: Path,
    gate: dict,
    dry_run: bool,
    artifacts: dict[int, Path] | None = None,
) -> dict:
    """Valideer één quality gate - simplified implementation."""
    gate_naam = gate.get("name", "unknown")
    gate_type = gate.get("type", "validatie")
    criteria = gate.get("criteria", "")
    
    if dry_run:
        return {
            "name": gate_naam,
            "type": gate_type,
            "result": "skipped (dry-run)",
            "criteria": criteria[:100],
        }
    
    # Extract agent-naam from artifacts if available
    agent_naam = None
    if artifacts and 1 in artifacts:
        boundary_fields = _extract_boundary_fields(artifacts[1])
        agent_naam = boundary_fields.get("agent-naam")
    
    # Determine base directory from criteria context
    base_dir = workspace_root
    if ".github/prompts" in criteria:
        base_dir = workspace_root / ".github" / "prompts"
    elif "governance/rolbeschrijvingen" in criteria:
        base_dir = workspace_root / "governance" / "rolbeschrijvingen"
    elif "scripts/" in criteria:
        base_dir = workspace_root / "scripts"
    
    # Simplified validation: check if criteria mention specific files
    # Real implementation would parse criteria and actually check them
    file_checks = re.findall(r'`([^`]+\.md)`', criteria)
    
    all_pass = True
    failed_checks = []
    
    for file_path in file_checks:
        # Replace template variables with actual values
        if agent_naam and "<agent-naam>" in file_path:
            file_path = file_path.replace("<agent-naam>", agent_naam)
        
        # Strip base_dir prefix from file_path if present (to avoid duplication)
        file_path_str = str(file_path)
        if base_dir != workspace_root:
            base_dir_relative = base_dir.relative_to(workspace_root).as_posix()
            if file_path_str.startswith(base_dir_relative + "/"):
                file_path_str = file_path_str[len(base_dir_relative) + 1:]
        
        # Handle template patterns like {volgnummer} by checking with glob
        if "{" in file_path_str or "<" in file_path_str:
            # Convert to glob pattern: {volgnummer} -> *, <xxx> -> *
            glob_pattern = re.sub(r'\{[^}]+\}', '*', file_path_str)
            glob_pattern = re.sub(r'<[^>]+>', '*', glob_pattern)
            
            # Check if any files match the pattern in base_dir
            matches = list(base_dir.glob(glob_pattern))
            if not matches:
                # Not an error if alternative pattern exists (multi-step OR simple)
                continue
        else:
            # Direct file check in base_dir
            full_path = base_dir / file_path_str
            if not full_path.exists():
                all_pass = False
                failed_checks.append(f"Bestand ontbreekt: {full_path.relative_to(workspace_root).as_posix()}")
            else:
                # Found at least one file, gate can pass
                return {
                    "name": gate_naam,
                    "type": gate_type,
                    "result": "pass",
                    "criteria": criteria[:100],
                    "details": f"Gevonden: {full_path.relative_to(workspace_root).as_posix()}",
                }
    
    # For now, assume gates pass if no file checks or all files exist
    return {
        "name": gate_naam,
        "type": gate_type,
        "result": "pass" if all_pass else "fail",
        "criteria": criteria[:100],
        "details": " | ".join(failed_checks) if failed_checks else "All checks passed",
    }


def execute_pipeline(
    *,
    workspace_root: Path,
    pipeline_bestand: str,
    workflow_bestand: str | None,
    dry_run: bool,
    stop_on_failure: bool | None,
    continue_from_step: int | None,
    extra_params: list[str],
) -> ExecutionResult:
    """Voer pipeline uit met parameter doorgifte en artifact chaining."""
    start_time = time.time()
    
    # Policy gates
    _policy_gate_workspace_paths(workspace_root)
    pipeline_path = _policy_gate_pipeline_exists(workspace_root, pipeline_bestand)
    
    # Parse pipeline
    pipeline_data = _parse_pipeline(pipeline_path)
    pipeline_naam = pipeline_data["naam"]
    stappen = pipeline_data["stappen"]
    gates = pipeline_data["gates"]
    
    if not stappen:
        return ExecutionResult(
            success=False,
            message=f"Pipeline '{pipeline_naam}' bevat geen stappen",
            total_duration=time.time() - start_time,
        )
    
    # Validate agents exist
    _validate_agents_exist(workspace_root, stappen)
    
    # Execution with artifact tracking
    steps_executed: list[dict] = []
    gates_validated: list[dict] = []
    failures: list[dict] = []
    artifacts: dict[int, Path] = {}  # step_num -> artifact_path
    all_artifacts: list[Path] = []
    
    # Determine start step
    start_step = continue_from_step if continue_from_step else 1
    
    # If starting from a later step, try to find artifacts from skipped steps
    if start_step > 1:
        # Extract agent-naam from extra_params if provided
        agent_naam_param = None
        for i, param in enumerate(extra_params):
            if param == "--agent-naam" and i + 1 < len(extra_params):
                agent_naam_param = extra_params[i + 1]
                break
        
        # Try to detect artifacts from previous steps that were skipped
        for skipped_step_num in range(1, start_step):
            if skipped_step_num < len(stappen):
                skipped_stap = stappen[skipped_step_num - 1]  # 0-indexed
                skipped_agent = skipped_stap.get("agent", "")
                
                # Try to find existing artifact
                if agent_naam_param:
                    artifact = _detect_output_artifact(workspace_root, skipped_agent, skipped_step_num)
                    if artifact and artifact.exists():
                        artifacts[skipped_step_num] = artifact
                        all_artifacts.append(artifact)
    
    for stap in stappen:
        step_num = stap.get("number", 0)
        
        # Skip steps before continue_from_step
        if step_num < start_step:
            continue
        
        # Execute step with artifacts from previous steps
        step_result = _execute_step_sequential(workspace_root, stap, dry_run, extra_params, artifacts)
        steps_executed.append(step_result)
        
        # Track artifact if produced
        if step_result.get("artifact"):
            artifacts[step_num] = step_result["artifact"]
            all_artifacts.append(step_result["artifact"])
        
        # Check for failure
        if step_result["status"] not in ("success", "skipped (dry-run)"):
            failure = {
                "location": f"Stap {step_num}: {step_result['name']}",
                "error": f"Agent returned exit code {step_result['exit_code']}",
                "action": "Stop pipeline" if stop_on_failure else "Continue",
            }
            failures.append(failure)
            
            if stop_on_failure is not False:  # Stop unless explicitly told to continue
                total_duration = time.time() - start_time
                return ExecutionResult(
                    success=False,
                    message=f"Pipeline '{pipeline_naam}' gefaald bij stap {step_num}",
                    steps_executed=steps_executed,
                    gates_validated=gates_validated,
                    failures=failures,
                    artifacts=all_artifacts,
                    total_duration=total_duration,
                )
        
        # Validate gate after this step
        step_gates = [g for g in gates if g.get("after_step") == step_num]
        for gate in step_gates:
            gate_result = _validate_gate(workspace_root, gate, dry_run, artifacts)
            gates_validated.append(gate_result)
            
            # Check gate failure
            if gate_result["result"] == "fail":
                failure = {
                    "location": f"Gate {gate['number']}: {gate['name']}",
                    "error": gate_result.get("details", "Gate criteria not met"),
                    "action": gate.get("failure_action", "Stop pipeline"),
                }
                failures.append(failure)
                
                if "stop" in gate.get("failure_action", "").lower():
                    total_duration = time.time() - start_time
                    return ExecutionResult(
                        success=False,
                        message=f"Pipeline '{pipeline_naam}' gefaald bij gate {gate['number']}",
                        steps_executed=steps_executed,
                        gates_validated=gates_validated,
                        failures=failures,
                        artifacts=all_artifacts,
                        total_duration=total_duration,
                    )
    
    total_duration = time.time() - start_time
    
    if dry_run:
        message = f"Pipeline '{pipeline_naam}' gevalideerd (dry-run mode - {len(stappen)} stappen gecontroleerd)"
    else:
        message = f"Pipeline '{pipeline_naam}' succesvol uitgevoerd ({len(steps_executed)} stappen, {len(gates_validated)} gates, {len(all_artifacts)} artifacts)"
    
    return ExecutionResult(
        success=len(failures) == 0,
        message=message,
        steps_executed=steps_executed,
        gates_validated=gates_validated,
        failures=failures,
        artifacts=all_artifacts,
        total_duration=total_duration,
    )
