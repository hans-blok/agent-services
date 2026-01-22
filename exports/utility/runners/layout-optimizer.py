#!/usr/bin/env python3
"""
Layout Optimizer Runner

Automatiseert basistaken van de layout-optimizer agent zonder AI-interactie.

Usage:
    python scripts/layout-optimizer.py --input-pad path/to/diagram --formaat mermaid

Requirements:
    - Python 3.8+
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List


WORKSPACE_ROOT = Path(__file__).parent.parent
AGENT_NAME = "layout-optimizer"
VERSION = "1.1.0"


class LayoutOptimizerRunner:
    """Runner voor Layout Optimizer agent."""

    def __init__(self, workspace_root: Path) -> None:
        """Initialiseer runner.

        Args:
            workspace_root: Root directory van de workspace.
        """
        self.workspace_root = workspace_root
        self.docs_dir = workspace_root / "docs"
        # Resultaatlocaties
        self.results_dir = self.docs_dir / "resultaten" / AGENT_NAME
        # Locatie waar de C4 Modelleur zijn Structurizr workspace.dsl verwacht
        self.structurizr_dir = (
            self.docs_dir / "resultaten" / "c4-modelleur" / ".structurizr"
        )

    def validate_input(self, input_pad: str, formaat: str) -> bool:
        """Valideer input parameters.

        Args:
            input_pad: Pad naar bronbestand of graph-spec.
            formaat: Bronformaat (bijv. graph-spec, mermaid, plantuml, dot, dsl).

        Returns:
            True als input geldig is.

        Raises:
            ValueError: Als verplichte parameter ontbreekt of ongeldig is.
        """
        if not input_pad or not input_pad.strip():
            raise ValueError("Parameter 'input-pad' mag niet leeg zijn")

        if not formaat or not formaat.strip():
            raise ValueError("Parameter 'formaat' mag niet leeg zijn")

        allowed_formats = {"graph-spec", "mermaid", "plantuml", "dot", "dsl"}
        if formaat.strip().lower() not in allowed_formats:
            raise ValueError(
                "Parameter 'formaat' moet een van de volgende waarden hebben: "
                + ", ".join(sorted(allowed_formats)),
            )

        return True

    def run(
        self,
        input_pad: str,
        formaat: str,
        richting: str | None = None,
        check_only: bool = False,
    ) -> Dict[str, object]:
        """Voer layout-optimizer taak uit.

        Deze runner:
        - valideert invoer;
        - bepaalt een logische bestandsnaam met tijdstempel voor het
          geoptimaliseerde diagram;
        - schrijft een geoptimaliseerde kopie weg onder
          docs/resultaten/layout-optimizer/ (tenzij check_only=True);
        - en kopieert bij Structurizr DSL-input de laatst geoptimaliseerde
          versie ook naar docs/resultaten/c4-modelleur/.structurizr/workspace.dsl
          zodat de live-visualisatie de laatste layout toont.

        Args:
            input_pad: Pad naar bronbestand of graph-spec.
            formaat: Bronformaat.
            richting: Gewenste leesrichting (TB of LR), optioneel.
            check_only: Alleen analyseren, geen wijzigingen.

        Returns:
            Dictionary met output resultaten.
        """
        self.validate_input(input_pad=input_pad, formaat=formaat)

        fmt = formaat.strip().lower()

        # Bouw samenvatting
        summary_lines: List[str] = []
        summary_lines.append(f"Agent: {AGENT_NAME}")
        summary_lines.append(f"Input: {input_pad}")
        summary_lines.append(f"Formaat: {fmt}")
        if richting:
            summary_lines.append(f"Richting: {richting.strip().upper()}")

        # Normaliseer en controleer pad
        src_path = Path(input_pad)
        if not src_path.is_absolute():
            src_path = self.workspace_root / src_path

        if not src_path.exists():
            raise ValueError(f"Bronbestand bestaat niet: {src_path}")

        now = datetime.now()
        canonical_timestamp = now.strftime("%Y-%m-%d:%H:%M")
        filename_timestamp = now.strftime("%Y-%m-%d_%H-%M")

        artifacts: List[Path] = []

        if check_only:
            summary_lines.append("Modus: check-only (geen bestanden geschreven)")
            base_name = src_path.stem
            optimized_name = f"{base_name}-optimized-{filename_timestamp}{src_path.suffix}"
            summary_lines.append(
                "Voorstel bestandsnaam geoptimaliseerd diagram: "
                f"docs/resultaten/layout-optimizer/{optimized_name}"
            )
        else:
            summary_lines.append("Modus: optimalisatie-uitvoer (kopie van bronbestand)")
            summary_lines.append(f"Canonieke tijdstempel: {canonical_timestamp}")

            self.results_dir.mkdir(parents=True, exist_ok=True)

            base_name = src_path.stem
            optimized_name = f"{base_name}-optimized-{filename_timestamp}{src_path.suffix}"
            optimized_path = self.results_dir / optimized_name

            # Voor nu: kopieer het bronbestand 1-op-1 als "geoptimaliseerde" versie.
            shutil.copy2(src_path, optimized_path)
            artifacts.append(optimized_path)

            # Indien Structurizr DSL: update ook workspace.dsl voor live-visualisatie
            if fmt == "dsl":
                self.structurizr_dir.mkdir(parents=True, exist_ok=True)
                workspace_dsl_path = self.structurizr_dir / "workspace.dsl"
                shutil.copy2(optimized_path, workspace_dsl_path)
                artifacts.append(workspace_dsl_path)
                summary_lines.append(
                    "Actuele Structurizr workspace.dsl bijgewerkt voor visualisatie op poort 8080."
                )

        message = "\n".join(summary_lines)

        return {
            "success": True,
            "artifacts": [str(p.relative_to(self.workspace_root)) for p in artifacts],
            "message": message,
        }


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description=f"{AGENT_NAME} runner - Automatiseert layout-optimalisatie taken",
    )

    parser.add_argument(
        "--input-pad",
        required=True,
        help="Pad naar de bron van het diagram of de graph-spec.",
    )

    parser.add_argument(
        "--formaat",
        required=True,
        help="Bronformaat (graph-spec, mermaid, plantuml, dot of dsl).",
    )

    parser.add_argument(
        "--richting",
        help="Gewenste leesrichting (TB voor Top-to-Bottom, LR voor Left-to-Right).",
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

    runner = LayoutOptimizerRunner(WORKSPACE_ROOT)

    try:
        results = runner.run(
            input_pad=args.input_pad,
            formaat=args.formaat,
            richting=args.richting,
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
