# Agents Publicatie Overzicht

**Publicatiedatum**: 2026-01-18  
**Scope**: volledig  
**Basis-folder**: exports/  
**Aantal gescande charters**: 12

---

## Samenvatting

**Totaal aantal agents**: 12

**Aantal per Value Stream**:
- kennispublicatie: 7 agents
- utility: 2 agents
- it-development: 2 agents
- ondernemingsvorming: 1 agent

**Aantal per Agent-soort**:
- Uitvoerend Agent: 10 agents
- Beheeragent: 1 agent
- Adviserend Agent: 2 agents

---

## Agents Overzicht (Gegroepeerd per Value Stream)

### Value Stream: it-development

| Agent Naam | Agent-soort | Domein | Prompts | Status |
|------------|-------------|--------|---------|--------|
| pipeline-executor | Uitvoerend Agent | Pipeline-uitvoering, workflow-orkestratie | 1 | Actief |
| workflow-architect | Adviserend Agent | Workflow-ontwerp, multi-agent orkestratie | 0 | Actief |

**Beschikbare prompts**:
- pipeline-executor: pipeline-executor-voer-uit

---

### Value Stream: kennispublicatie

| Agent Naam | Agent-soort | Domein | Prompts | Status |
|------------|-------------|--------|---------|--------|
| agent-publisher | Uitvoerend Agent | Kennispublicatie | 1 | Actief |
| artikel-schrijver | Uitvoerend Agent | Artikelproductie, kennisoverdracht | 7 | Actief |
| de-schrijver | Uitvoerend Agent | Narratieve tekstproductie, kennisoverdracht | 1 | Actief |
| essayist | Uitvoerend Agent | Essayproductie, reflectieve kennisoverdracht | 1 | Actief |
| heraut | Uitvoerend Agent | Canonieke aankondiging, governance communicatie | 2 | Actief |
| presentatie-architect | Uitvoerend Agent | Presentatie-ontwerp | 0 | Actief |
| vertaler | Uitvoerend Agent | Tekstvertaling, meertalige kennisoverdracht | 1 | Actief |

**Beschikbare prompts**:
- agent-publisher: agent-publisher-publiceer
- artikel-schrijver: artikel-schrijver-1-afbakening-intentie, artikel-schrijver-2-kernboodschap, artikel-schrijver-3-structuur, artikel-schrijver-4-artikeldefinitie, artikel-schrijver-5-tekstproductie, artikel-schrijver-6-redactie-afronding, artikel-schrijver
- de-schrijver: de-schrijver
- essayist: essayist-schrijf-essay
- heraut: heraut-schrijf-korte-post, heraut-schrijf-orientatiedocument
- vertaler: vertaler-vertaal

---

### Value Stream: ondernemingsvorming

| Agent Naam | Agent-soort | Domein | Prompts | Status |
|------------|-------------|--------|---------|--------|
| mandarin-ea | Adviserend Agent | Enterprise Architecture & Strategie | 1 | Actief |

**Beschikbare prompts**:
- mandarin-ea: mandarin-ea-definieer-strategie

---

### Value Stream: utility

| Agent Naam | Agent-soort | Domein | Prompts | Status |
|------------|-------------|--------|---------|--------|
| moeder | Beheeragent | Workspace-ordening, governance, agent-lifecycle | 5 | Actief |
| python-expert | Uitvoerend Agent | Python-ontwikkeling, code-kwaliteit | 3 | Actief |

**Beschikbare prompts**:
- moeder: moeder-beheer-git, moeder-configureer-github, moeder-orden-workspace, moeder-schrijf-beleid, moeder-valideer-governance
- python-expert: python-expert-review-code, python-expert-run-script, python-expert-schrijf-script

---

## Metadata

**Output formaat**: markdown-tabel  
**Sortering**: value-stream  
**Include drafts**: false  
**Include prompts**: true

**Gescande folders**:
- exports/it-development/charters-agents/
- exports/kennispublicatie/charters-agents/
- exports/ondernemingsvorming/charters-agents/
- exports/utility/charters-agents/

**Gelezen charters**: 12
- charter.pipeline-executor.md
- charter.workflow-architect.md
- charter.agent-publisher.md
- charter.artikel-schrijver.md
- charter.de-schrijver.md
- charter.essayist.md
- charter.heraut.md
- charter.presentatie-architect.md
- charter.vertaler.md
- charter.mandarin-ea.md
- charter.moeder.md
- charter.python-expert.md

---

## Herkomstverantwoording

Dit overzicht is gegenereerd door **Agent Curator** op basis van:
- Alle charters in exports/<value-stream>/charters-agents/
- Alle prompts in .github/prompts/ (matching op agent-naam prefix)
- Agent-metadata uit charter headers (Agent, Agent-soort, Value Stream, Domein)
- Status: alle agents zijn actief (geen draft-status gevonden)

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
Zoek agent → artikel-schrijver (kennispublicatie)
Bekijk prompts → 7 beschikbaar (1-afbakening t/m 6-redactie)
Lees charter → exports/kennispublicatie/charters-agents/charter.artikel-schrijver.md
Activeer prompt → .github/prompts/artikel-schrijver-1-afbakening-intentie.prompt.md
```

---

**Versie**: 1.0  
**Gegenereerd door**: Agent Curator  
**Conform**: agent-curator-publiceer-agents-overzicht.prompt.md (versie 1.0)
