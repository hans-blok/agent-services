# Agent Boundary — Moeder (herzien)

**Datum**: 2026-01-18  
**Aanleiding**: Moeder wordt uitgebreid met verantwoordelijkheid voor agent-fetching uit agent-services repository naar project workspaces.  
**Value Stream**: utility

---

## Boundary Definitie

```
agent-naam: moeder
capability-boundary: Workspace-ordening, governance, Git/GitHub beheer, én agent-fetching uit agent-services
doel: Beheer workspace structuur, governance compliance, Git workflows, én haal benodigde agents op uit agent-services repository
domein: Workspace beheer & Agent provisioning
```

---

## Toelichting

**Huidige capability** (blijft behouden):
- Git en GitHub workflow (commits, branches, configuratie)
- Workspace ordening (folderstructuur, validatie)
- Beleid aanmaken bij nieuwe workspaces
- Workspace state beheer en logging
- Governance compliance validatie

**Nieuwe capability** (toegevoegd):
- **Agent fetching**: Raadpleegt `agents-publicatie.json` uit agent-services repository
- **Selectieve fetch**: Haalt alleen benodigde agents op basis van workspace-behoeften
- **Artefacten ophalen**: Fetcht charters, prompts en runners uit `exports/<value-stream>/`
- **Lokale integratie**: Installeert gefetchte agents in workspace volgens workspace-doctrine

**Rationale voor uitbreiding**:
- Moeder kent de workspace-behoeften (governance, structuur, context)
- Moeder bepaalt al agent-boundaries voor nieuwe workspace-agents
- Logische uitbreiding: ook benodigde agents ophalen uit centraal register
- Scheiding blijft: Moeder fetcht, maar schrijft niet zelf agent-artefacten

---

## Consistentie-check

**Overlap met bestaande agents**:
- **Agent Curator**: Beheert agent-services repository, publiceert overzicht → geen overlap
- **Agent Smeder**: Ontwerpt en implementeert agents → geen overlap
- **Moeder**: Workspace beheer + nu ook agent provisioning → consistente uitbreiding

**Value stream alignment**:
- Value stream: **utility** (workspace beheer, agent provisioning zijn utility functies)
- Geen conflict met kennispublicatie, it-development of ondernemingsvorming

**Governance compliance**:
- Blijft binnen workspace-doctrine scope
- Agent-fetching is infrastructurele taak, geen strategische besluitvorming
- Moeder escaleert complexe keuzes naar governance (blijft behouden)

---

## Folder-structuur (ongewijzigd)

- Charter: `exports/utility/charters-agents/charter.moeder.md`
- Prompts: `exports/utility/prompts/moeder-*.prompt.md` (7 bestaand + 1 nieuw voor fetching)
- Runner: `exports/utility/runners/moeder.py`

---

## Aanbevelingen

1. **Nieuwe prompt toevoegen**: `moeder-fetch-agents.prompt.md`
   - Input: workspace-context, benodigde capabilities
   - Output: Gefetchte agents in workspace (charters, prompts, runners)
   - Leest: `agents-publicatie.json` uit agent-services

2. **Charter bijwerken**: Kerntaak 8 toevoegen voor agent-fetching

3. **Runner uitbreiden**: `moeder.py` met functionaliteit voor:
   - JSON parsing (`agents-publicatie.json`)
   - HTTP/Git fetch uit agent-services repository
   - Lokale installatie volgens workspace-doctrine

---

## Handoff naar Agent Smeder

Deze boundary is gereed voor implementatie door Agent Smeder:
- Nieuwe prompt: `moeder-fetch-agents.prompt.md`
- Charter update: Kerntaak 8 + werkwijze sectie
- Runner update: fetch functionaliteit toevoegen aan `moeder.py`

**Input voor Agent Smeder**:
```
agent-naam: moeder
capability-boundary: Workspace-ordening, governance, Git/GitHub beheer, én agent-fetching uit agent-services
doel: Beheer workspace structuur, governance compliance, Git workflows, én haal benodigde agents op uit agent-services repository
domein: Workspace beheer & Agent provisioning
```

---

**Governance**: `agent-charters/charter.agent-curator.md`  
**Referentie**: Huidige charter `exports/utility/charters-agents/charter.moeder.md`
