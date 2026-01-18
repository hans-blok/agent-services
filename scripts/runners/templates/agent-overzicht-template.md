# Agent Overzicht (Intern)

**Publicatiedatum**: <datum>  
**Scope**: <scope>  
**Basis-folder**: exports/  
**Aantal gescande charters**: <aantal>

---

## Samenvatting

**Totaal aantal agents**: <totaal>

**Aantal per Value Stream**:
- <value-stream-1>: <aantal> agents
- <value-stream-2>: <aantal> agents
- <value-stream-n>: <aantal> agents

**Aantal per Agent-soort**:
- Uitvoerend Agent: <aantal> agents
- Beheeragent: <aantal> agents
- Adviserend Agent: <aantal> agents

---

## Agents Overzicht (Gegroepeerd per Value Stream)

### Value Stream: <value-stream-naam>

| Agent Naam | Agent-soort | Domein | Prompts | Status |
|------------|-------------|--------|---------|--------|
| <agent-naam> | <soort> | <domein> | <aantal> | <status> |

**Beschikbare prompts**:
- <agent-naam>: <prompt-1>, <prompt-2>, <prompt-n>

---

### Value Stream: <volgende-stream>

| Agent Naam | Agent-soort | Domein | Prompts | Status |
|------------|-------------|--------|---------|--------|
| <agent-naam> | <soort> | <domein> | <aantal> | <status> |

**Beschikbare prompts**:
- <agent-naam>: <prompt-lijst>

---

## Metadata

**Output formaat**: <format>  
**Sortering**: <sort-by>  
**Include drafts**: <boolean>  
**Include prompts**: <boolean>

**Gescande folders**:
- exports/<value-stream-1>/charters-agents/
- exports/<value-stream-2>/charters-agents/
- exports/<value-stream-n>/charters-agents/

**Gelezen charters**: <aantal>
- charter.<agent-naam-1>.md
- charter.<agent-naam-2>.md
- charter.<agent-naam-n>.md

---

## Herkomstverantwoording

Dit overzicht is gegenereerd door **Agent Curator** op basis van:
- Alle charters in exports/<value-stream>/charters-agents/
- Alle prompts in .github/prompts/ (matching op agent-naam prefix)
- Agent-metadata uit charter headers (Agent, Agent-soort, Value Stream, Domein)
- Status: <toelichting-status>

**Doel**: Dit overzicht dient als basis voor het fetchen van agents vanuit project workspaces. Elke agent is identificeerbaar via:
- Unieke agent-naam (lowercase-hyphens)
- Agent-soort (Adviserend Agent | Uitvoerend Agent | Beheeragent)
- Value Stream (domein/context)
- Beschikbare prompts (capabilities)

**Bronnen**:
- Charter-normering: canon/grondslagen/globaal/doctrine-agent-charter-normering.md
- Agent Curator charter: agent-charters/charter.agent-curator.md
- Prompt-contract: .github/prompts/agent-curator-publiceer-agents-overzicht.prompt.md

---

## Gebruik voor Fetching

Project workspaces kunnen agents fetchen door:
1. Dit overzicht te raadplegen voor beschikbare agents
2. Agent te selecteren op basis van agent-naam en value stream
3. Prompts te identificeren voor gewenste capability
4. Charter te lezen voor volledige context: `exports/<value-stream>/charters-agents/charter.<agent-naam>.md`
5. Prompt te activeren: `.github/prompts/<agent-naam>-<capability>.prompt.md`

**Voorbeeld fetching flow**:
```
Zoek agent → <agent-naam> (<value-stream>)
Bekijk prompts → <aantal> beschikbaar
Lees charter → exports/<value-stream>/charters-agents/charter.<agent-naam>.md
Activeer prompt → .github/prompts/<agent-naam>-<capability>.prompt.md
```

---

**Versie**: <versie>  
**Gegenereerd door**: Agent Curator  
**Conform**: agent-curator-publiceer-agents-overzicht.prompt.md (versie <versie>)
