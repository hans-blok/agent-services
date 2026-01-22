# Agents Publicatie Overzicht

**Publicatiedatum**: 2026-01-22
**Tijdstip**: 20:15:00
**Scope**: volledig
**Totaal agents**: 18

## Value Stream: agent-enablement

**Aantal agents**: 2

| Agent | Domein | Prompts | Runners |
|-------|--------|---------|----------|
| agent-curator | Agent boundary-setting, value stream administratie, agent ecosysteem oversight | 4 | 1 |
| agent-smeder | Agent-ontwerp, capability boundaries en contract-first uitvoering | 3 | 0 |

## Value Stream: architectuur-en-oplossingsontwerp

**Aantal agents**: 4

| Agent | Domein | Prompts | Runners |
|-------|--------|---------|----------|
| archimate-modelleur | Enterprise architecture modellering | 2 | 0 |
| bedrijfsarchitect | Business architecture modellering | 0 | 0 |
| c4-modelleur | Software-architectuur modellering | 2 | 0 |
| converter-md-to-archimate | ArchiMate format conversie | 1 | 0 |

## Value Stream: it-development

**Aantal agents**: 2

| Agent | Domein | Prompts | Runners |
|-------|--------|---------|----------|
| pipeline-executor | Pipeline-uitvoering, workflow-orkestratie | 0 | 1 |
| workflow-architect | Workflow-ontwerp, multi-agent orkestratie | 3 | 1 |

## Value Stream: kennispublicatie

**Aantal agents**: 7

| Agent | Domein | Prompts | Runners |
|-------|--------|---------|----------|
| agent-publisher | Kennispublicatie | 1 | 0 |
| artikel-schrijver | Artikelproductie, kennisoverdracht | 6 | 0 |
| de-schrijver | Narratieve tekstproductie, kennisoverdracht | 0 | 0 |
| essayist | Essayproductie, reflectieve kennisoverdracht | 1 | 0 |
| heraut | Canonieke aankondiging, governance communicatie | 2 | 0 |
| presentatie-architect | Presentatie-ontwerp | 1 | 0 |
| vertaler | Tekstvertaling, meertalige kennisoverdracht | 1 | 0 |

## Value Stream: ondernemingsvorming

**Aantal agents**: 1

| Agent | Domein | Prompts | Runners |
|-------|--------|---------|----------|
| mandarin-ea | Enterprise Architecture & Strategie | 1 | 0 |

## Value Stream: utility

**Aantal agents**: 2

| Agent | Domein | Prompts | Runners |
|-------|--------|---------|----------|
| moeder | Workspace-ordening, governance, agent-lifecycle | 6 | 1 |
| python-expert | Python-ontwikkeling, code-kwaliteit | 3 | 0 |

## Metadata

- **Gescande folders**:
  - `agent-charters/` (agent-enablement)
  - `exports/*/charters/` (value streams)
  - `exports/*/charters-agents/` (value streams)
  - `.github/prompts/` (agent-enablement prompts)
  - `exports/*/prompts/` (value stream prompts)
  - `scripts/runners/` (runners)
- **Value stream bron**: Charter header (`**Value Stream**:` veld)
- **Traceability**: Agent Curator charter v0.4.4, publiceer-agents-overzicht prompt

## Samenvatting

### Totalen per categorie

| Categorie | Aantal |
|-----------|--------|
| **Totaal agents** | 18 |
| **Totaal prompts** | 43 |
| **Totaal runners** | 5 |
| **Value streams** | 6 |

### Per Value Stream

| Value Stream | Agents | Prompts | Runners |
|--------------|--------|---------|----------|
| agent-enablement | 2 | 7 | 1 |
| architectuur-en-oplossingsontwerp | 4 | 5 | 0 |
| it-development | 2 | 3 | 2 |
| kennispublicatie | 7 | 13 | 0 |
| ondernemingsvorming | 1 | 1 | 0 |
| utility | 2 | 9 | 1 |

### Agents met runners

1. **agent-curator** (agent-enablement): 1 runner
2. **moeder** (utility): 1 runner  
3. **pipeline-executor** (it-development): 1 runner
4. **workflow-architect** (it-development): 1 runner

*Totaal: 4 agents met runners, 5 runner artefacten*

### Value Stream classificatie

**Agent-enablement** (infrastructuur):
- Agents die het agent-ecosysteem ondersteunen
- Focus op boundary-bepaling, agent-ontwerp

**Architectuur-en-oplossingsontwerp** (domein):
- Enterprise en software architecture modellering
- ArchiMate, C4, Business Layer

**IT-development** (technical):
- Workflow orkestratie en pipeline execution
- Multi-agent workflows

**Kennispublicatie** (content):
- Kennisproductie, artikelen, essays, presentaties
- Vertaling en publicatie

**Ondernemingsvorming** (strategie):
- Enterprise Architecture en strategisch advies

**Utility** (cross-functional):
- Workspace management, Python development
- Gebruikt in alle value streams

## Herkomstverantwoording

Alle agents zijn gescand uit hun charter-headers. De `**Value Stream**:` metadata in elke charter (regel 4-5) is leidend voor toewijzing aan value stream. 

Prompts zijn geteld via wildcardmatching op agent-naam in:
- `.github/prompts/<agent-naam>-*.prompt.md` (agent-enablement)
- `exports/<value-stream>/prompts/<agent-naam>-*.prompt.md` (overige streams)

Runners zijn geteld in `scripts/runners/`:
- Individual scripts: `<agent-naam>.py`
- Module folders: `<agent-naam>/` (met `__init__.py`)

Dit overzicht is gegenereerd door Agent Curator conform:
- Charter: agent-charters/charter.agent-curator.md (versie 0.4.4)
- Prompt: .github/prompts/agent-curator-publiceer-agents-overzicht.prompt.md
- Runner: scripts/runners/agent-curator.py (verbeterd met Python Expert standaarden)

**Kwaliteitsborging**: Alle agents hebben verplichte header-velden (Agent, Value Stream), duplicates worden gedetecteerd, missing charters worden gerapporteerd.
