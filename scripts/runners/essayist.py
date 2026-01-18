#!/usr/bin/env python3
"""Runner voor de Essayist agent.

Deze runner automatiseert herhaalbare stappen voor de Essayist:
- controle van verplichte input (onderwerp en standpunt);
- aanmaken van een eenvoudig essaysjabloon in Markdown;
- schrijven naar de juiste locatie (docs/resultaten/essayist/);
- toevoegen van basis metadata (datum en parameters).

Gebruik (voorbeeld):
    python scripts/essayist.py \
        --onderwerp "Context en beschrijving" \
        --standpunt "Het kernstandpunt" \
        [--bronmateriaal "Referenties"] \
        [--richting "kritisch|praktijkgericht|historiserend"] \
        [--lengte "kort|midden|lang"] \
        [--output-naam "bestandsnaam-zonder-extensie"]

Output:
- docs/resultaten/essayist/<output-naam>.md
- temp/essayist-trace-<timestamp>.md (tracebestand)

De runner schrijft geen inhoudelijk essay en roept geen AI aan.
Hij maakt alleen de basisstructuur en valideert de invoer.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class EssayistInput:
    onderwerp: str
    standpunt: str
    bronmateriaal: str | None
    richting: str | None
    lengte: str | None
    output_naam: str


@dataclass(frozen=True)
class RunnerResult:
    success: bool
    message: str
    output_path: Path | None
    trace_path: Path | None


def _timestamp_for_filename(now: datetime | None = None) -> str:
    now = now or datetime.now()
    return now.strftime("%Y%m%d-%H%M%S")


def _validate_input(args: argparse.Namespace) -> EssayistInput | str:
    """Validate input parameters. Returns EssayistInput or error string."""
    
    if not args.onderwerp or not args.onderwerp.strip():
        return "ERROR: --onderwerp is verplicht en mag niet leeg zijn"
    
    if not args.standpunt or not args.standpunt.strip():
        return "ERROR: --standpunt is verplicht en mag niet leeg zijn"
    
    # Validate richting if provided
    valid_richting = ["kritisch", "praktijkgericht", "historiserend"]
    if args.richting and args.richting.strip().lower() not in valid_richting:
        return f"ERROR: --richting moet één van zijn: {', '.join(valid_richting)}"
    
    # Validate lengte if provided
    valid_lengte = ["kort", "midden", "lang"]
    if args.lengte and args.lengte.strip().lower() not in valid_lengte:
        return f"ERROR: --lengte moet één van zijn: {', '.join(valid_lengte)}"
    
    # Default output name from onderwerp
    output_naam = args.output_naam
    if not output_naam:
        # Create safe filename from onderwerp (first 5 words, lowercase, hyphens)
        words = args.onderwerp.strip().split()[:5]
        output_naam = "-".join(w.lower() for w in words)
        output_naam = "".join(c if c.isalnum() or c == "-" else "" for c in output_naam)
    
    return EssayistInput(
        onderwerp=args.onderwerp.strip(),
        standpunt=args.standpunt.strip(),
        bronmateriaal=args.bronmateriaal.strip() if args.bronmateriaal else None,
        richting=args.richting.strip().lower() if args.richting else None,
        lengte=args.lengte.strip().lower() if args.lengte else None,
        output_naam=output_naam,
    )


def _create_essay_skeleton(
    inp: EssayistInput,
    output_path: Path,
) -> None:
    """Maak een eenvoudig essaysjabloon met metadata en basisstructuur."""
    
    lines: list[str] = []
    
    # Metadata
    lines.append("---\n")
    lines.append(f"onderwerp: {inp.onderwerp}\n")
    lines.append(f"standpunt: {inp.standpunt}\n")
    if inp.bronmateriaal:
        lines.append(f"bronmateriaal: {inp.bronmateriaal}\n")
    if inp.richting:
        lines.append(f"richting: {inp.richting}\n")
    if inp.lengte:
        lines.append(f"lengte: {inp.lengte}\n")
    lines.append(f"gegenereerd: {datetime.now().strftime('%Y-%m-%d')}\n")
    lines.append("---\n\n")
    
    # Title placeholder
    lines.append("# [Titel]\n\n")
    
    # Opening paragraph placeholder
    lines.append("## Inleiding\n\n")
    lines.append(f"**Context**: {inp.onderwerp}\n\n")
    lines.append(f"**Standpunt**: {inp.standpunt}\n\n")
    
    # Body placeholder
    lines.append("## [Hoofdsectie 1]\n\n")
    lines.append("[Ontwikkel het standpunt hier...]\n\n")
    
    lines.append("## [Hoofdsectie 2]\n\n")
    lines.append("[Verdere uitwerking...]\n\n")
    
    # Closing placeholder
    lines.append("## Slot\n\n")
    lines.append("[Afronding zonder expliciete samenvatting...]\n\n")
    
    # Write
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(lines), encoding="utf-8")


def _write_trace(
    workspace_root: Path,
    inp: EssayistInput,
    success: bool,
    message: str,
    output_path: Path | None,
) -> Path:
    """Schrijf een tracebestand weg in temp/."""
    
    temp_dir = workspace_root / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    trace_path = temp_dir / f"essayist-trace-{_timestamp_for_filename()}.md"
    
    lines: list[str] = []
    lines.append("# Essayist Runner Trace\n\n")
    lines.append(f"- success: {str(success).lower()}\n")
    lines.append(f"- message: {message}\n\n")
    
    lines.append("## Input\n\n")
    lines.append(f"- onderwerp: {inp.onderwerp}\n")
    lines.append(f"- standpunt: {inp.standpunt}\n")
    if inp.bronmateriaal:
        lines.append(f"- bronmateriaal: {inp.bronmateriaal}\n")
    if inp.richting:
        lines.append(f"- richting: {inp.richting}\n")
    if inp.lengte:
        lines.append(f"- lengte: {inp.lengte}\n")
    lines.append(f"- output-naam: {inp.output_naam}\n\n")
    
    lines.append("## Output\n\n")
    if output_path:
        try:
            rel = output_path.relative_to(workspace_root)
            lines.append(f"- {rel.as_posix()}\n")
        except ValueError:
            lines.append(f"- {str(output_path)}\n")
    else:
        lines.append("- (geen)\n")
    
    trace_path.write_text("".join(lines), encoding="utf-8")
    return trace_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Essayist runner voor validatie en essaysjabloon"
    )
    
    parser.add_argument(
        "--onderwerp",
        required=True,
        help="Waar gaat het essay inhoudelijk over? (1-3 zinnen met context)",
    )
    
    parser.add_argument(
        "--standpunt",
        required=True,
        help="Het kernstandpunt dat het essay moet innemen (1 zin)",
    )
    
    parser.add_argument(
        "--bronmateriaal",
        help="Verwijzing naar bron(nen) of bestaande teksten (optioneel)",
    )
    
    parser.add_argument(
        "--richting",
        choices=["kritisch", "praktijkgericht", "historiserend"],
        help="Korte aanwijzingen voor toon of invalshoek (optioneel)",
    )
    
    parser.add_argument(
        "--lengte",
        choices=["kort", "midden", "lang"],
        help="Gewenste lengte-indicatie (optioneel)",
    )
    
    parser.add_argument(
        "--output-naam",
        help="Bestandsnaam zonder extensie (default: afgeleid van onderwerp)",
    )
    
    parser.add_argument(
        "--no-trace",
        action="store_true",
        help="Schrijf geen tracebestand weg",
    )
    
    args = parser.parse_args()
    
    # Validate
    validated = _validate_input(args)
    if isinstance(validated, str):
        print(validated, file=sys.stderr)
        return 1
    
    inp = validated
    workspace_root = Path(__file__).parent.parent.resolve()
    
    # Create output
    output_path = workspace_root / "docs" / "resultaten" / "essayist" / f"{inp.output_naam}.md"
    
    try:
        _create_essay_skeleton(inp, output_path)
        message = f"Essaysjabloon aangemaakt: {output_path.name}"
        
        # Write trace
        trace_path = None
        if not args.no_trace:
            trace_path = _write_trace(
                workspace_root=workspace_root,
                inp=inp,
                success=True,
                message=message,
                output_path=output_path,
            )
        
        print(f"OK: {message}")
        if trace_path:
            print(f"Trace: {trace_path.relative_to(workspace_root).as_posix()}")
        
        return 0
    
    except Exception as exc:
        error_msg = f"Runner fout: {exc}"
        print(f"ERROR: {error_msg}", file=sys.stderr)
        
        # Write trace even on error
        if not args.no_trace:
            trace_path = _write_trace(
                workspace_root=workspace_root,
                inp=inp,
                success=False,
                message=error_msg,
                output_path=None,
            )
            print(f"Trace: {trace_path.relative_to(workspace_root).as_posix()}", file=sys.stderr)
        
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
