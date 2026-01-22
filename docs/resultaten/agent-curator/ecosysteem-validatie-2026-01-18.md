# Ecosysteem Validatie — Agent Artefact Plaatsing (2026-01-18)

## Samenvatting
- Misplaatsingen gedetecteerd door Smeder/handmatig: charters onder `governance/` i.p.v. `exports/<value-stream>/charter-agents/`.
- Source vs project routing onduidelijk; `.github/prompts` in `agent-services` zou enkel voor fetched projectworkspaces moeten gelden.
- Autoritatieve kopieën bestaan onder `exports/solution-architecting/...`; duplicaten blijven verwarrend.
- Voorstel ingediend: standaardiseer plaatsing + runner-routing; voeg validatieregel toe.

## Tabel — Folder mismatches
| Artefact | Huidige locatie | Gewenste locatie (source repo) | Status |
|---|---|---|---|
| Charter: solution-architect | governance/charters-agents/charter.solution-architect.md | exports/solution-architecting/charter-agents/charter.solution-architect.md | Dubbel (autoritatief in exports)|
| Prompt: solution-architect-beoordeel-referentie-en-domeinarchitectuur | exports/solution-architecting/prompts/... | exports/solution-architecting/prompts/... | OK |

## Bevindingen
- Smeder-runner schreef default naar `.github/prompts/` en `governance/` (skeleton & prompt-contract). Dit is correct voor project workspaces, niet voor broncatalogus.
- `agent-services` functioneert als broncatalogus; `.github/prompts` dient te worden gevuld door fetch in project-repos, niet direct hier.

## Aanbevelingen (governance)
- Adopteer de voorgestelde standaard: zie `canon/grondslagen/globaal/proposals/cr-agent-artifact-placement-standard.md`.
- Markeer governance-duplicaten voor verwijdering na akkoord (niet automatisch verwijderen).
- Laat Curator validatie rapporteren wanneer in bronrepo artefacten buiten `exports/<value-stream>` worden aangetroffen.

## Herkomstverantwoording
- Gescand: `.github/prompts/`, `governance/`, `exports/*` in deze repository.
- Normatieve referentie: `canon/grondslagen/globaal/agent-charter-normering.md` (structuur), value stream overzicht.
