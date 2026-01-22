# Agents Publicatie Overzicht

**Publicatiedatum**: 2026-01-22
**Tijdstip**: 19:55:00
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
  - `agent-charters/` (utility & agent-enablement)
  - `exports/*/charters/` (value streams)
  - `exports/*/charters-agents/` (value streams)
  - `.github/prompts/` (prompts)
  - `exports/*/prompts/` (value stream prompts)
  - `scripts/runners/` (runners)
- **Value stream bron**: Charter header (`**Value Stream**:` veld)
- **Traceability**: Agent Curator charter, publiceer-agents-overzicht prompt

## Samenvatting

- **Totaal agents**: 18
- **Totaal prompts**: 43
- **Totaal runners**: 5
- **Value streams**: 6

### Per Value Stream

| Value Stream | Agents | Prompts | Runners |
|--------------|--------|---------|----------|
| agent-enablement | 2 | 7 | 1 |
| architectuur-en-oplossingsontwerp | 4 | 5 | 0 |
| it-development | 2 | 3 | 2 |
| kennispublicatie | 7 | 13 | 0 |
| ondernemingsvorming | 1 | 1 | 0 |
| utility | 2 | 9 | 1 |

## Herkomstverantwoording

Alle agents zijn gescand uit hun charter-headers. De `**Value Stream**:` metadata in elke charter is leidend voor toewijzing aan value stream. Prompts zijn geteld via wildcardmatching op agent-naam in `.github/prompts/` en `exports/*/prompts/`. Runners zijn geteld in `scripts/runners/` (zowel `.py` bestanden als module folders).

Dit overzicht is gegenereerd door Agent Curator conform charter (versie 0.4.4) en prompt `agent-curator-publiceer-agents-overzicht.prompt.md`.
