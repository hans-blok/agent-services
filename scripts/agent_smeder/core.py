from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

# Policy constants
MIN_BOUNDARY_LENGTH = 10
FORBIDDEN_TERMS_DEFAULT = ("pdf", "html")


@dataclass(frozen=True)
class OperationResult:
    success: bool
    message: str
    artifacts: List[Path]


class PolicyError(Exception):
    pass


def _is_valid_agent_name(agent_name: str) -> bool:
    if not agent_name:
        return False
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
    if any(ch not in allowed for ch in agent_name):
        return False
    if agent_name.startswith("-") or agent_name.endswith("-"):
        return False
    if "--" in agent_name:
        return False
    return True


def _policy_gate_common(
    *,
    agent_name: str,
    capability_boundary: str,
    forbidden_terms: Iterable[str] = ("pdf", "html"),
) -> None:
    if not _is_valid_agent_name(agent_name):
        raise PolicyError(
            "agent-naam is ongeldig: gebruik lowercase, cijfers en hyphens (geen spaties)."
        )
    if not capability_boundary or len(capability_boundary.strip()) < MIN_BOUNDARY_LENGTH:
        raise PolicyError(f"capability-boundary is te kort (minimaal {MIN_BOUNDARY_LENGTH} karakters) of ontbreekt.")

    lowered = capability_boundary.lower()
    for term in forbidden_terms:
        if term in lowered:
            raise PolicyError(
                f"capability-boundary bevat '{term}'. Publicatieformaten horen alleen bij Publisher."
            )


def _write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def op_init_skeleton(
    *,
    workspace_root: Path,
    agent_name: str,
    capability_boundary: str,
    doel: str,
    domein: str,
) -> OperationResult:
    _policy_gate_common(agent_name=agent_name, capability_boundary=capability_boundary)

    artifacts: List[Path] = []

    role_path = workspace_root / "governance" / "rolbeschrijvingen" / f"{agent_name}.md"
    prompt_path = (
        workspace_root / ".github" / "prompts" / f"{agent_name}.prompt.md"
    )
    runner_path = workspace_root / "scripts" / f"{agent_name}.py"

    role_content = (
        f"# Rolbeschrijving: {agent_name}\n\n"
        f"**Agent**: workspace.{agent_name}  \n"
        f"**Domein**: {domein}  \n"
        f"**Type**: <type>\n\n"
        f"---\n\n"
        f"## Rol en Verantwoordelijkheid\n\n"
        f"Doel: {doel}.\n\n"
        f"Capability boundary: {capability_boundary}\n\n"
        f"### Kerntaken\n\n"
        f"1. **<Taak 1>**\n   - <onderdelen>\n\n"
        f"## Grenzen\n\n"
        f"### Wat {agent_name} NIET doet\n- ❌ <beperking>\n\n"
        f"### Wat {agent_name} WEL doet\n- ✅ <mogelijkheid>\n\n"
        f"---\n\n"
        f"**Versie**: 0.1  \n"
        f"**Laatst bijgewerkt**: <datum>\n"
    )

    prompt_content = (
        "---\n"
        f"agent: workspace.{agent_name}\n"
        f"description: {doel}\n"
        "---\n\n"
        f"# {agent_name} Prompt\n\n"
        "## Rolbeschrijving\n\n"
        f"{doel}.\n\n"
        f"**VERPLICHT**: Lees governance/rolbeschrijvingen/{agent_name}.md voor volledige context.\n\n"
        "## Contract\n\n"
        "### Input (Wat gaat erin)\n\n"
        "**Verplichte parameters**:\n"
        "- <param>: <beschrijving> (type: <type>)\n\n"
        "### Output (Wat komt eruit)\n\n"
        "Bij een geldige opdracht levert de agent altijd:\n"
        "- Een korte samenvatting van de actie.\n"
        "- Een overzicht van resultaten.\n"
        "- Eventuele waarschuwingen bij governance-conflict.\n\n"
        "### Foutafhandeling\n\n"
        "De agent:\n"
        "- Stopt bij governance-conflict.\n"
        "- Vraagt om verduidelijking bij onduidelijke input.\n\n"
        "## Werkwijze\n\n"
        "Deze prompt is een contract op hoofdlijnen. Voor details verwijst de agent naar de rolbeschrijving.\n\n"
        "---\n\n"
        f"Documentatie: Zie governance/rolbeschrijvingen/{agent_name}.md  \n"
        f"Runner: scripts/{agent_name}.py\n"
    )

    runner_content = (
        "#!/usr/bin/env python3\n"
        f"\"\"\"\n{agent_name} Runner\n\n"
        f"Automatiseert taken van de {agent_name} agent zonder AI-interactie.\n\n"
        "Usage:\n"
        f"    python scripts/{agent_name}.py --help\n\n"
        "Requirements:\n"
        "    - Python 3.10+\n"
        "\"\"\"\n\n"
        "import argparse\n"
        "from pathlib import Path\n\n"
        "WORKSPACE_ROOT = Path(__file__).parent.parent\n\n"
        "\n"
        "def main() -> None:\n"
        "    parser = argparse.ArgumentParser(description='Agent runner')\n"
        "    parser.add_argument('--dry-run', action='store_true', help='Geen wijzigingen schrijven')\n"
        "    args = parser.parse_args()\n"
        "    if args.dry_run:\n"
        "        print('dry-run: geen wijzigingen')\n"
        "        return\n"
        "    print('TODO: implementeer runner-logica')\n\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )

    if _write_if_missing(role_path, role_content):
        artifacts.append(role_path)
    if _write_if_missing(prompt_path, prompt_content):
        artifacts.append(prompt_path)
    if _write_if_missing(runner_path, runner_content):
        artifacts.append(runner_path)

    msg = "Agent-skeleton aangemaakt" if artifacts else "Agent-skeleton bestond al"
    return OperationResult(success=True, message=msg, artifacts=artifacts)


def op_design_prompt_contract(
    *,
    workspace_root: Path,
    agent_name: str,
    capability_boundary: str,
    doel: str,
    domein: str,
) -> OperationResult:
    _policy_gate_common(agent_name=agent_name, capability_boundary=capability_boundary)

    prompt_path = workspace_root / ".github" / "prompts" / f"{agent_name}.prompt.md"

    content = (
        "---\n"
        f"agent: workspace.{agent_name}\n"
        f"description: {doel}\n"
        "---\n\n"
        f"# {agent_name} Prompt\n\n"
        "## Rolbeschrijving\n\n"
        f"{doel}.\n\n"
        f"Capability boundary: {capability_boundary}\n\n"
        f"Domein: {domein}\n\n"
        f"**VERPLICHT**: Lees governance/rolbeschrijvingen/{agent_name}.md voor volledige context.\n\n"
        "## Contract\n\n"
        "### Input (Wat gaat erin)\n\n"
        "**Verplichte parameters**:\n"
        "- <param>: <beschrijving> (type: <type>)\n\n"
        "**Optionele parameters**:\n"
        "- <param>: <beschrijving> (type: <type>, default: <waarde>)\n\n"
        "### Output (Wat komt eruit)\n\n"
        "Bij een geldige opdracht levert de agent altijd:\n"
        "- Een korte samenvatting van de actie.\n"
        "- Een overzicht van de belangrijkste resultaten.\n"
        "- Eventuele waarschuwingen bij governance-conflict.\n\n"
        "### Foutafhandeling\n\n"
        "De agent:\n"
        "- Stopt wanneer acties in strijd zouden zijn met governance of eigen grenzen.\n"
        "- Vraagt om verduidelijking bij onduidelijke opdrachten of ontbrekende informatie.\n\n"
        "## Werkwijze\n\n"
        "Deze prompt is een contract op hoofdlijnen. Voor details verwijst de agent volledig naar de rolbeschrijving.\n\n"
        "---\n\n"
        f"Documentatie: Zie governance/rolbeschrijvingen/{agent_name}.md  \n"
        f"Runner: scripts/{agent_name}.py\n"
    )

    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(content, encoding="utf-8")

    return OperationResult(success=True, message="Prompt-contract geschreven", artifacts=[prompt_path])


def op_write_role_description(
    *,
    workspace_root: Path,
    agent_name: str,
    capability_boundary: str,
    doel: str,
    domein: str,
) -> OperationResult:
    _policy_gate_common(agent_name=agent_name, capability_boundary=capability_boundary)

    role_path = workspace_root / "governance" / "rolbeschrijvingen" / f"{agent_name}.md"

    content = (
        f"# Rolbeschrijving: {agent_name}\n\n"
        f"**Agent**: workspace.{agent_name}  \n"
        f"**Domein**: {domein}  \n"
        f"**Type**: <type>\n\n"
        f"---\n\n"
        f"## Rol en Verantwoordelijkheid\n\n"
        f"{doel}.\n\n"
        f"Capability boundary: {capability_boundary}\n\n"
        f"### Kerntaken\n\n"
        f"1. **<Taak 1>**\n   - <onderdelen>\n\n"
        f"2. **<Taak 2>**\n   - <onderdelen>\n\n"
        f"## Specialisaties\n\n"
        f"### <Specialisatie 1>\n<details>\n\n"
        f"## Grenzen\n\n"
        f"### Wat {agent_name} NIET doet\n- ❌ <beperking>\n\n"
        f"### Wat {agent_name} WEL doet\n- ✅ <mogelijkheid>\n\n"
        f"## Werkwijze\n\n"
        f"### Bij <scenario>\n1. <stap>\n\n"
        f"---\n\n"
        f"**Versie**: 0.1  \n"
        f"**Laatst bijgewerkt**: <datum>\n"
    )

    role_path.parent.mkdir(parents=True, exist_ok=True)
    role_path.write_text(content, encoding="utf-8")

    return OperationResult(success=True, message="Rolbeschrijving geschreven", artifacts=[role_path])


def op_write_runner_skeleton_for_agent(
    *,
    workspace_root: Path,
    agent_name: str,
    capability_boundary: str,
) -> OperationResult:
    _policy_gate_common(agent_name=agent_name, capability_boundary=capability_boundary)

    runner_path = workspace_root / "scripts" / f"{agent_name}.py"

    content = (
        "#!/usr/bin/env python3\n"
        f"\"\"\"\n{agent_name} Runner\n\n"
        f"Automatiseert taken van de {agent_name} agent zonder AI-interactie.\n\n"
        "Usage:\n"
        f"    python scripts/{agent_name}.py --help\n\n"
        "Requirements:\n"
        "    - Python 3.10+\n"
        "\"\"\"\n\n"
        "import argparse\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        "WORKSPACE_ROOT = Path(__file__).parent.parent\n\n"
        "\n"
        "def main() -> None:\n"
        "    parser = argparse.ArgumentParser(description='Agent runner')\n"
        "    parser.add_argument('--version', action='store_true', help='Toon versie')\n"
        "    args = parser.parse_args()\n"
        "    if args.version:\n"
        "        print('0.1')\n"
        "        return\n"
        "    print('TODO: implementeer runner-logica')\n\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    try:\n"
        "        main()\n"
        "    except Exception as exc:\n"
        "        print(f'Onverwachte fout: {exc}', file=sys.stderr)\n"
        "        raise\n"
    )

    runner_path.parent.mkdir(parents=True, exist_ok=True)
    runner_path.write_text(content, encoding="utf-8")

    return OperationResult(success=True, message="Runner-skelet geschreven", artifacts=[runner_path])


def execute_operation(
    *,
    workspace_root: Path,
    operation: str,
    agent_name: str,
    capability_boundary: str,
    doel: str | None = None,
    domein: str | None = None,
) -> OperationResult:
    op = operation.strip().lower()

    if op == "init-skeleton":
        if not doel or not domein:
            raise PolicyError("doel en domein zijn verplicht voor init-skeleton")
        return op_init_skeleton(
            workspace_root=workspace_root,
            agent_name=agent_name,
            capability_boundary=capability_boundary,
            doel=doel,
            domein=domein,
        )

    if op == "design-prompt":
        if not doel or not domein:
            raise PolicyError("doel en domein zijn verplicht voor design-prompt")
        # Policy gate: promptnamen moeten een werkwoord in gebiedende wijs bevatten
        # (bijv. "schrijf-", "valideer-", "controleer-") zodat direct duidelijk is
        # welke actie de agent uitvoert.
        if "-" not in agent_name:
            raise PolicyError(
                "agent-naam moet een werkwoord in gebiedende wijs bevatten (bijv. schrijf-*, valideer-*)"
            )
        return op_design_prompt_contract(
            workspace_root=workspace_root,
            agent_name=agent_name,
            capability_boundary=capability_boundary,
            doel=doel,
            domein=domein,
        )

    if op == "write-role":
        if not doel or not domein:
            raise PolicyError("doel en domein zijn verplicht voor write-role")
        return op_write_role_description(
            workspace_root=workspace_root,
            agent_name=agent_name,
            capability_boundary=capability_boundary,
            doel=doel,
            domein=domein,
        )

    if op == "write-runner":
        return op_write_runner_skeleton_for_agent(
            workspace_root=workspace_root,
            agent_name=agent_name,
            capability_boundary=capability_boundary,
        )

    raise PolicyError(
        "Onbekende operatie. Kies uit: init-skeleton, design-prompt, write-role, write-runner."
    )
