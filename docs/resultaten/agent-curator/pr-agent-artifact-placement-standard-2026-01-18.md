# PR: Agent Artifact Placement Standard — Source vs Project Routing (2026-01-18)

## Samenvatting
- Doel: standaardiseer plaatsing van agent-artefacten (charters, prompts) in de broncatalogus vs project-workspaces.
- Kern: in `agent-services` (bron) gaan artefacten naar `exports/<value-stream>/...`; in project-repos staan prompts onder `.github/prompts/` via fetch.
- Runner-update: Smeder ondersteunt `--value-stream` en `AGENTS_SOURCE_REPO=true` voor bronmodus.
- Impact: voorkomt duplicaten/mismatches; verduidelijkt source-of-truth; sluit aan op fetch-flow.

## Wijzigingen (in deze PR)
- Nieuwe governance change request: `canon/grondslagen/globaal/proposals/cr-agent-artifact-placement-standard.md`.
- Smeder routing:
  - `scripts/agent_smeder/core.py` — prompt-pad routing helper + value-stream doorvoer
  - `scripts/agent_smeder/frontdoor.py` — `--value-stream` vlag + trace opname
- Curator rapportage: `docs/resultaten/agent-curator/ecosysteem-validatie-2026-01-18.md` (mismatches + aanbevelingen)
- Duplicate charter onder governance verwijderd (autoriteit staat in `exports/solution-architecting/charter-agents/`).

## Brondocumenten en artefacten
- Autoritatieve charter: `exports/solution-architecting/charter-agents/charter.solution-architect.md`
- Prompt (voorbeeld): `exports/solution-architecting/prompts/solution-architect-beoordeel-referentie-en-domeinarchitectuur.prompt.md`

## Rationale
- `.github/prompts` in bronrepo leidt tot verwarring; moet alleen consumptie in project-workspaces vertegenwoordigen.
- `exports/<value-stream>/...` definieert het canonieke agent-landschap per stream.

## Testinstructies
1. Zet bronmodus aan en schrijf een prompt naar de juiste stream:
   - Windows CMD:
     ```bat
     set AGENTS_SOURCE_REPO=true
     python scripts\runners\agent-smeder.py design-prompt --agent-naam demo-agent-schrijf-voorbeeld --capability-boundary "Schrijft voorbeeldcontracten in Markdown." --doel "Schrijft een voorbeeld prompt-contract" --domein "utility" --value-stream utility
     ```
2. Controleer resultaat:
   - Prompt staat onder `exports/utility/prompts/demo-agent-schrijf-voorbeeld.prompt.md`
   - Trace in `temp/agent-smeder-trace-*.md` vermeldt `value-stream: utility`
3. Zet bronmodus uit en herhaal (verwacht `.github/prompts/` in project-workspace):
   ```bat
   set AGENTS_SOURCE_REPO=
   python scripts\runners\agent-smeder.py design-prompt --agent-naam demo-agent-schrijf-voorbeeld --capability-boundary "Schrijft voorbeeldcontracten in Markdown." --doel "Schrijft een voorbeeld prompt-contract" --domein "utility"
   ```

## Roll-out
- Na akkoord: toepassen op charter-writer (separate kleine wijziging) zodat charters ook direct onder `exports/<value-stream>/charter-agents/` worden geplaatst.
- Curator-regel toevoegen: waarschuwen voor artefacten buiten `exports` in bronmodus.

## Checklist voor reviewers
- [ ] Routing naar `exports/<value-stream>/prompts/` in bronmodus is correct
- [ ] Geen breaking changes voor project-workspaces (fallback `.github/prompts/`)
- [ ] Proposal-tekst dekt bron/consumptie en uitzonderingslogica voor `agent-services`
- [ ] Curator-rapport duidelijk en reproduceerbaar
