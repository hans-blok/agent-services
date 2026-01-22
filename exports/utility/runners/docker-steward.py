#!/usr/bin/env python3
"""
Docker Steward Runner

Automatiseert basistaken van de docker-steward agent zonder AI-interactie.

Usage:
    python scripts/docker-steward.py --opdracht "status"
    python scripts/docker-steward.py --opdracht "start visualisatie" --port 8080

Requirements:
    - Python 3.8+
    - (Optioneel) Docker CLI beschikbaar in PATH
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List


WORKSPACE_ROOT = Path(__file__).parent.parent
AGENT_NAME = "docker-steward"
VERSION = "1.0.0"


class DockerStewardRunner:
    """Runner voor Docker Steward agent."""

    def __init__(self, workspace_root: Path) -> None:
        """Initialiseer runner.

        Args:
            workspace_root: Root directory van de workspace.
        """
        self.workspace_root = workspace_root
        self.docs_dir = workspace_root / "docs"
        self.results_dir = self.docs_dir / "resultaten" / AGENT_NAME

    def validate_input(self, opdracht: str, port: int | None = None) -> bool:
        """Valideer input parameters.

        Args:
            opdracht: Beschrijving van de gewenste actie (start/stop/status).
            port: Optionele poort voor lokale visualisaties.

        Returns:
            True als input geldig is.

        Raises:
            ValueError: Als verplichte parameter ontbreekt of ongeldig is.
        """
        if not opdracht or not opdracht.strip():
            raise ValueError("Parameter 'opdracht' mag niet leeg zijn")

        if port is not None and (port <= 0 or port > 65535):
            raise ValueError("Parameter 'port' moet een geldig poortnummer zijn (1-65535)")

        return True

    def run(self, opdracht: str, port: int | None = None, check_only: bool = False) -> Dict[str, object]:
        """Voer docker-steward taak uit.

        Deze skeleton-runner voert nog geen echte Docker-commando's uit,
        maar valideert invoer en geeft een samenvattend resultaat terug.

        Args:
            opdracht: Beschrijving van de gewenste actie.
            port: Optionele poort voor lokale visualisaties.
            check_only: Alleen analyseren, geen wijzigingen.

        Returns:
            Dictionary met output resultaten.
        """
        self.validate_input(opdracht=opdracht, port=port)

        summary_lines: List[str] = []
        summary_lines.append(f"Agent: {AGENT_NAME}")
        summary_lines.append(f"Opdracht: {opdracht.strip()}")
        if port is not None:
            summary_lines.append(f"Poort: {port}")
        summary_lines.append("Modus: analyse" + (" (check-only)" if check_only else " (voorbereiding)"))

        message = "\n".join(summary_lines)

        return {
            "success": True,
            "artifacts": [],
            "message": message,
        }


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description=f"{AGENT_NAME} runner - Automatiseert lokale Docker- en visualisatietaken",
    )

    parser.add_argument(
        "--opdracht",
        required=True,
        help="Korte beschrijving van de gewenste actie (bijvoorbeeld 'start visualisatie', 'stop', 'status').",
    )

    parser.add_argument(
        "--port",
        type=int,
        help="Gewenste poort voor de lokale visualisatieservice (bijvoorbeeld 8080).",
    )

    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Alleen analyseren en samenvatten, geen wijzigingen doorvoeren.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"{AGENT_NAME} runner v{VERSION}",
    )

    args = parser.parse_args()

    runner = DockerStewardRunner(WORKSPACE_ROOT)

    try:
        results = runner.run(
            opdracht=args.opdracht,
            port=args.port,
            check_only=args.check_only,
        )

        if results.get("success"):
            print(f"✅ {AGENT_NAME} succesvol uitgevoerd")
            if results.get("message"):
                print()
                print(results["message"])
            artifacts = results.get("artifacts") or []
            if artifacts:
                print("\nAangemaakte/gewijzigde bestanden:")
                for artifact in artifacts:
                    print(f"  - {artifact}")
        else:
            print(f"❌ {AGENT_NAME} gefaald: {results.get('message', 'Onbekende fout')}")
            sys.exit(1)

    except ValueError as exc:
        print(f"❌ Validatiefout: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(f"❌ Onverwachte fout: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
