# Agents Publicatie — Volledig Overzicht

**Publicatiedatum**: 2026-01-18  
**Versie**: 1.0  
**Scope**: volledig

---

## Samenvatting

- **Totaal aantal agents**: 12
- **Aantal value streams**: 4
- **Totaal aantal prompts**: 26
- **Totaal aantal runners**: 3

### Per Value Stream

| Value Stream | Aantal agents | Aantal prompts | Aantal runners |
|--------------|---------------|----------------|----------------|
| kennispublicatie | 7 | 12 | 0 |
| it-development | 2 | 4 | 2 |
| ondernemingsvorming | 1 | 1 | 0 |
| utility | 2 | 9 | 1 |

---

## Agents per Value Stream

### kennispublicatie

| Agent | Aantal prompts | Aantal runners |
|-------|----------------|----------------|
| agent-publisher | 1 | 0 |
| artikel-schrijver | 6 | 0 |
| de-schrijver | 0 | 0 |
| essayist | 1 | 0 |
| heraut | 2 | 0 |
| presentatie-architect | 1 | 0 |
| vertaler | 1 | 0 |

### it-development

| Agent | Aantal prompts | Aantal runners |
|-------|----------------|----------------|
| pipeline-executor | 1 | 1 |
| workflow-architect | 3 | 1 |

### ondernemingsvorming

| Agent | Aantal prompts | Aantal runners |
|-------|----------------|----------------|
| mandarin-ea | 1 | 0 |

### utility

| Agent | Aantal prompts | Aantal runners |
|-------|----------------|----------------|
| moeder | 6 | 1 |
| python-expert | 3 | 0 |

---

## Metadata

**Gescande folders**:
- `exports/kennispublicatie/charters-agents/` (7 charters)
- `exports/kennispublicatie/prompts/` (12 prompts)
- `exports/kennispublicatie/runners/` (0 runners)
- `exports/it-development/charters-agents/` (2 charters)
- `exports/it-development/prompts/` (4 prompts)
- `exports/it-development/runners/` (2 runners)
- `exports/ondernemingsvorming/charters-agents/` (1 charter)
- `exports/ondernemingsvorming/prompts/` (0 prompts)
- `exports/ondernemingsvorming/runners/` (0 runners)
- `exports/utility/charters-agents/` (2 charters)
- `exports/utility/prompts/` (9 prompts)
- `exports/utility/runners/` (1 runner)

**Gelezen charters**: 12  
**Template**: `templates/agents-publicatie-template.md`

---

## Herkomstverantwoording

Deze publicatie is gegenereerd door Agent Curator op basis van:
- Charter-metadata uit `exports/<value-stream>/charters-agents/`
- Prompts-scan uit `exports/<value-stream>/prompts/`
- Runners-scan uit `exports/<value-stream>/runners/`

Alle agents zijn traceerbaar naar hun value stream en beschikbare artefacten (charters, prompts, runners).

---

## Gebruik

**Charter locatie**: `exports/<value-stream>/charters-agents/charter.<agent-naam>.md`  
**Prompt locatie**: `exports/<value-stream>/prompts/<agent-naam>-<werkwoord>.prompt.md`  
**Runner locatie**: `exports/<value-stream>/runners/<agent-naam>.py`

**Fetching vanuit project workspaces**:
1. Raadpleeg dit overzicht voor beschikbare agents
2. Identificeer agent-naam en value stream
3. Fetch charter uit `exports/<value-stream>/charters-agents/`
4. Fetch prompts uit `exports/<value-stream>/prompts/`
5. Fetch runners uit `exports/<value-stream>/runners/` (indien beschikbaar)

---

**Bron**: agent-services repository  
**Onderhoud**: Agent Curator  
**Governance**: `agent-charters/charter.agent-curator.md`
