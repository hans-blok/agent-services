# Moeder Prompt — Fetch Agents

## Rolbeschrijving

Moeder haalt benodigde agents op uit het agent-services repository en installeert deze in de huidige workspace. Dit gebeurt op basis van workspace-behoeften en de beschikbare agents in het centrale register.

**VERPLICHT**: Lees exports/utility/charters-agents/charter.moeder.md voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- value-stream: Uit welke value stream moeten agents opgehaald worden? (type: string, bijv. 'kennispublicatie', 'it-development', 'utility', 'ondernemingsvorming')
- branch: Welke branch van agent-services moet gebruikt worden? (type: string, bijv. 'main', 'develop')

**Optionele parameters**:
- agent-services-locatie: Locatie van agent-services repository (type: string, default: 'https://github.com/hans-blok/agent-services.git')
- include-runners: Ook runners ophalen (type: boolean, default: true)
- workspace-folder: Waar moeten de agents geïnstalleerd worden? (type: string, default: huidige workspace root)

### Output (Wat komt eruit)

Bij een geldige opdracht levert Moeder altijd:

**Per gefetchte agent**:
- Charter gekopieerd naar workspace lokatie (volgens workspace-doctrine)
- Prompts gekopieerd naar workspace `.github/prompts/`
- Runners gekopieerd naar workspace `scripts/` (indien `include-runners=true`)

**Samenvatting**:
- Lijst van geïnstalleerde agents met locaties
- Overzicht alle agents uit de opgegeven value-stream (gelezen uit `agents-publicatie.json`)
- Lijst van van gekopieerde artefacten (aantal charters, prompts, runners)
- Verificatie dat agents bruikbaar zijn in de workspace

**Manifest** (optioneel):
- Opgeslagen in `docs/agents-manifest.md`
- Bevat: welke agents, welke versie, installatie-datum, bron (agent-services)

### Foutafhandeling

Moeder:
- Stopt wanneer value-stream of branch parameter ontbreekt.
- Stopt wanneer value-stream niet bestaat in `agents-publicatie.json`.
- Stopt wanneer branch niet bestaat in agent-services repository.
- Stopt wanneer agent-services repository niet gevonden kan worden.
- Stopt wanneer `agents-publicatie.json` niet gelezen kan worden uit de opgegeven branch.
- Waarschuwt wanneer een agent uit de value-stream geen prompts of runners heeft.
- Vraagt om bevestiging bij het overschrijven van bestaande agent-artefacten in de workspace.
- Valideert dat gefetchte bestanden correct geïnstalleerd zijn (bestaan op verwachte locatie).
- Escaleert naar gebruiker bij permissie-problemen of conflicten met bestaande workspace-structuur.

## Werkwijze

Voor alle details over werkwijze (JSON parsing, Git fetch, installatie-logica, workspace-doctrine compliance) zie de charter.

---

Documentatie: Zie [exports/utility/charters-agents/charter.moeder.md](exports/utility/charters-agents/charter.moeder.md)  
Runner: exports/utility/runners/moeder.py
