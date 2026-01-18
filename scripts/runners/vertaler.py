#!/usr/bin/env python3
"""Vertaler Runner

Runner voor de Vertaler agent die technische teksten tussen NL en EN vertaalt.

Deze runner automatiseert:
- Validatie van verplichte input (brontekst, richting)
- Inlezen van brontekst en optionele terminologielijst
- Voorbereiden van output-structuur
- Metadata toevoegen (timestamp, parameters)

Usage:
    python scripts/vertaler.py \\
        --brontekst "pad/naar/document.md" \\
        --richting "nl-en" \\
        [--terminologie "term1:translation1,term2:translation2"] \\
        [--context "essay over agent-boundaries"] \\
        [--behoud-opmaak true] \\
        [--output-naam "bestandsnaam-zonder-extensie"]

Output:
    - docs/resultaten/vertaler/<output-naam>-<doeltaal>.md
    - temp/vertaler-trace-<timestamp>.md (trace artefact)

Deze runner is NIET bedoeld om de vertaling zelf uit te voeren (dat is AI-werk).
De runner maakt alleen de structuur, valideert input en bereidt output voor.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class VertalerInput:
    brontekst_path: Path
    richting: str
    terminologie: dict[str, str] | None
    context: str | None
    behoud_opmaak: bool
    output_naam: str
    doeltaal: str  # "en" of "nl"


@dataclass(frozen=True)
class RunnerResult:
    success: bool
    message: str
    output_path: Path | None
    trace_path: Path | None


def _timestamp_for_filename(now: datetime | None = None) -> str:
    now = now or datetime.now()
    return now.strftime("%Y%m%d-%H%M%S")


def _parse_terminologie(terminologie_str: str | None) -> dict[str, str] | None:
    """Parse terminologie string naar dict. Format: 'term1:translation1,term2:translation2'"""
    if not terminologie_str:
        return None
    
    result: dict[str, str] = {}
    for pair in terminologie_str.split(","):
        pair = pair.strip()
        if ":" not in pair:
            continue
        key, value = pair.split(":", 1)
        result[key.strip()] = value.strip()
    
    return result if result else None


def _validate_input(args: argparse.Namespace, workspace_root: Path) -> VertalerInput | str:
    """Validate input parameters. Returns VertalerInput or error string."""
    
    # Validate brontekst
    if not args.brontekst or not args.brontekst.strip():
        return "ERROR: --brontekst is verplicht en mag niet leeg zijn"
    
    brontekst_path = Path(args.brontekst.strip())
    if not brontekst_path.is_absolute():
        brontekst_path = workspace_root / brontekst_path
    
    if not brontekst_path.is_file():
        return f"ERROR: brontekst bestaat niet of is niet leesbaar: {brontekst_path}"
    
    if brontekst_path.suffix != ".md":
        return f"ERROR: brontekst moet een .md bestand zijn, niet: {brontekst_path.suffix}"
    
    # Validate richting
    valid_richting = ["nl-en", "en-nl"]
    if not args.richting or args.richting.strip().lower() not in valid_richting:
        return f"ERROR: --richting moet één van zijn: {', '.join(valid_richting)}"
    
    richting = args.richting.strip().lower()
    doeltaal = "en" if richting == "nl-en" else "nl"
    
    # Parse terminologie
    terminologie = _parse_terminologie(args.terminologie)
    
    # Default output name from brontekst
    output_naam = args.output_naam
    if not output_naam:
        output_naam = brontekst_path.stem
    
    return VertalerInput(
        brontekst_path=brontekst_path,
        richting=richting,
        terminologie=terminologie,
        context=args.context.strip() if args.context else None,
        behoud_opmaak=args.behoud_opmaak,
        output_naam=output_naam,
        doeltaal=doeltaal,
    )


def _create_translation_skeleton(
    inp: VertalerInput,
    brontekst_content: str,
    output_path: Path,
) -> None:
    """Create translation skeleton with metadata and placeholders."""
    
    lines: list[str] = []
    
    # Metadata
    lines.append("---\n")
    lines.append(f"brontekst: {inp.brontekst_path.name}\n")
    lines.append(f"richting: {inp.richting}\n")
    lines.append(f"doeltaal: {inp.doeltaal}\n")
    if inp.context:
        lines.append(f"context: {inp.context}\n")
    if inp.terminologie:
        lines.append("terminologie:\n")
        for term, translation in inp.terminologie.items():
            lines.append(f"  - {term}: {translation}\n")
    lines.append(f"gegenereerd: {datetime.now().strftime('%Y-%m-%d')}\n")
    lines.append("---\n\n")
    
    # Placeholder voor vertaling
    lines.append("# [VERTALING HIER]\n\n")
    lines.append(f"**Brontekst**: {inp.brontekst_path.name}\n")
    lines.append(f"**Richting**: {inp.richting}\n\n")
    
    lines.append("---\n\n")
    lines.append("## Originele tekst (referentie)\n\n")
    lines.append(brontekst_content)
    lines.append("\n")
    
    # Write
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(lines), encoding="utf-8")


def _write_trace(
    workspace_root: Path,
    inp: VertalerInput,
    success: bool,
    message: str,
    output_path: Path | None,
) -> Path:
    """Write trace artefact to temp/."""
    
    temp_dir = workspace_root / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    trace_path = temp_dir / f"vertaler-trace-{_timestamp_for_filename()}.md"
    
    lines: list[str] = []
    lines.append("# Vertaler Runner Trace\n\n")
    lines.append(f"- success: {str(success).lower()}\n")
    lines.append(f"- message: {message}\n\n")
    
    lines.append("## Input\n\n")
    lines.append(f"- brontekst: {inp.brontekst_path}\n")
    lines.append(f"- richting: {inp.richting}\n")
    lines.append(f"- doeltaal: {inp.doeltaal}\n")
    if inp.context:
        lines.append(f"- context: {inp.context}\n")
    if inp.terminologie:
        lines.append("- terminologie:\n")
        for term, translation in inp.terminologie.items():
            lines.append(f"  - {term}: {translation}\n")
    lines.append(f"- behoud-opmaak: {str(inp.behoud_opmaak).lower()}\n")
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
        description="Vertaler runner: validatie en vertaling-skeleton creatie"
    )
    
    parser.add_argument(
        "--brontekst",
        required=True,
        help="Pad naar het te vertalen Markdown-bestand",
    )
    
    parser.add_argument(
        "--richting",
        required=True,
        choices=["nl-en", "en-nl"],
        help="Vertaalrichting: nl-en (Nederlands naar Engels) of en-nl (Engels naar Nederlands)",
    )
    
    parser.add_argument(
        "--terminologie",
        help="Lijst van termen met vertalingen, format: 'term1:translation1,term2:translation2' (optioneel)",
    )
    
    parser.add_argument(
        "--context",
        help="Korte toelichting op het document (bijvoorbeeld: 'essay over agent-boundaries') (optioneel)",
    )
    
    parser.add_argument(
        "--behoud-opmaak",
        type=bool,
        default=True,
        help="Of de originele Markdown-opmaak volledig behouden moet blijven (default: true)",
    )
    
    parser.add_argument(
        "--output-naam",
        help="Bestandsnaam zonder extensie (default: afgeleid van brontekst)",
    )
    
    parser.add_argument(
        "--no-trace",
        action="store_true",
        help="Schrijf geen trace artefact weg",
    )
    
    args = parser.parse_args()
    
    workspace_root = Path(__file__).parent.parent.resolve()
    
    # Validate
    validated = _validate_input(args, workspace_root)
    if isinstance(validated, str):
        print(validated, file=sys.stderr)
        return 1
    
    inp = validated
    
    # Read brontekst
    try:
        brontekst_content = inp.brontekst_path.read_text(encoding="utf-8")
    except Exception as exc:
        error_msg = f"Kan brontekst niet lezen: {exc}"
        print(f"ERROR: {error_msg}", file=sys.stderr)
        return 1
    
    # Create output
    output_path = workspace_root / "docs" / "resultaten" / "vertaler" / f"{inp.output_naam}-{inp.doeltaal}.md"
    
    try:
        _create_translation_skeleton(inp, brontekst_content, output_path)
        message = f"Vertaling-skeleton aangemaakt: {output_path.name}"
        
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
