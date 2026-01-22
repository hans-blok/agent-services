# Agent Services Repository

**Centrale bron voor AI agents in het workspace-ecosysteem**

Deze repository bevat alle AI agents (charters, prompts, runners) die beschikbaar zijn voor gebruik in workspace repositories. Andere repositories **fetchen agents uit deze repository** via `exports/fetch_agents.py` en het manifest `agents-publicatie.json`.

---

## 📋 Overzicht

**Doel**: Centraal beheer van herbruikbare AI agents voor kennispublicatie, architectuur, ontwikkeling en onderneming.

**Gebruik**: Workspace repositories klonen deze repository, lezen het manifest, en kopiëren de benodigde agent-artefacten naar hun eigen workspace.

**Publicatie**: Agents worden gepubliceerd via `agents-publicatie.json` (manifest met digest voor change-tracking).

---

## 🤖 Agent-Soorten

Agents worden ingedeeld in **drie soorten** op basis van hun rol en bevoegdheden:

### 1. **Adviserend Agent**
- **Rol**: Beschouwend — analyseert en adviseert zonder directe wijziging
- **Wijzigt inhoud**: ❌ Nee — levert voorstel, geen wijziging
- **Wijzigt structuur**: ❌ Nee — raakt geen architectonische keuzes
- **Gezag**: Inzicht — autoriteit ontleend aan kwaliteit van analyse
- **Risico**: 🟢 Laag — geen directe impact op gedeelde werkelijkheid
- **Output**: Voorstel, analyse, advies

**Voorbeelden**: Validatie-agents, review-agents, analyse-agents

### 2. **Uitvoerend Agent**
- **Rol**: Inhoudelijk — voert wijzigingen uit in documenten en artefacten
- **Wijzigt inhoud**: ✅ Ja — wijzigt tekst, data, inhoudelijke artefacten
- **Wijzigt structuur**: ❌ Nee — raakt niet de architectuur of governance-structuur
- **Gezag**: Mandaat — autoriteit ontleend aan expliciet charter en workspace-beleid
- **Risico**: 🟡 Hoog — wijzigingen hebben impact op inhoud en gebruikers
- **Output**: Gewijzigde documenten, nieuwe artefacten

**Voorbeelden**: Schrijvers, modelleurs, converters

### 3. **Beheeragent**
- **Rol**: Operationeel — beheert structuur, governance en infrastructuur
- **Wijzigt inhoud**: ❌ Nee — raakt geen inhoudelijke artefacten
- **Wijzigt structuur**: ✅ Ja — past workspace-structuur, configuratie, agent-definities aan
- **Gezag**: Beheer — autoriteit ontleend aan infrastructurele verantwoordelijkheid
- **Risico**: 🔴 Hoog — wijzigingen in structuur impact gehele workspace
- **Output**: Workspace-wijzigingen, configuratie-updates, structurele aanpassingen

**Voorbeelden**: Moeder (workspace-beheer), Agent Curator (agent-publicatie)

---

## 📂 Repository Structuur

```
agent-services/
├── agents-publicatie.json          # Manifest met digest (voor fetch_agents.py)
├── publiceer-agents.bat            # Publicatie script (Windows)
│
├── agent-charters/                 # Charters voor agent-enablement agents
│   ├── charter.agent-curator.md
│   └── charter.agent-smeder.md
│
├── .github/prompts/                # Prompts voor agent-enablement agents
│   ├── agent-curator-*.prompt.md
│   └── agent-smeder-*.prompt.md
│
├── exports/                        # Agents per value stream
│   ├── architectuur-en-oplossingsontwerp/
│   │   ├── charters/
│   │   └── prompts/
│   ├── it-development/
│   │   ├── charters-agents/
│   │   └── prompts/
│   ├── kennispublicatie/
│   │   ├── charters-agents/
│   │   └── prompts/
│   ├── ondernemingsvorming/
│   │   ├── charters-agents/
│   │   └── prompts/
│   ├── utility/
│   │   ├── charters-agents/
│   │   ├── prompts/
│   │   └── runners/
│   └── fetch_agents.py             # Script voor andere repos
│
├── scripts/runners/                # Runners (alle agents)
│   ├── agent-curator.py
│   ├── agent-smeder.py
│   ├── moeder.py
│   └── ...
│
├── docs/resultaten/                # Output van agents
│   ├── agent-curator/
│   └── agent-publicaties/
│
└── copilot/
    └── agents.yaml                 # GitHub Copilot configuratie
```

---

## 🔄 Fetching Agents (voor andere repositories)

Andere workspace repositories gebruiken `exports/fetch_agents.py` om agents op te halen:

### Stap 1: Kopieer fetch script
```bash
# Eenmalig: kopieer fetch_agents.py naar je workspace
curl -o fetch_agents.py https://raw.githubusercontent.com/<org>/agent-services/main/exports/fetch_agents.py
```

### Stap 2: Fetch agents voor je value stream
```bash
# Haal agents op voor specifieke value stream
python fetch_agents.py kennispublicatie

# Lijst beschikbare value streams
python fetch_agents.py --list
```

### Wat gebeurt er?
1. **Clone/Pull**: agent-services repository wordt gedownload naar `agent-services/` (cache)
2. **Clean**: Oude agent-artefacten worden verwijderd (charters, prompts, runners)
3. **Copy**: Nieuwe versies worden gekopieerd naar workspace:
   - Charters → `agent-charters/` of `exports/<stream>/charters-agents/`
   - Prompts → `.github/prompts/` of `exports/<stream>/prompts/`
   - Runners → `scripts/runners/`
4. **Self-update**: fetch_agents.py werkt zichzelf bij naar nieuwste versie
5. **Log**: Activiteit wordt gelogd in `logs/fetch-agents-<timestamp>.log`

### ⚠️ Belangrijk: Overschrijfgedrag

**Charters**: Volledig overschreven met versie uit agent-services  
**Prompts**: Bestaande prompts met dezelfde naam overschreven; extra prompts behouden  
**Runners**: Volledig verwijderd en vervangen (module folders worden niet gemerged!)

Dit is **by design**: fetching installeert de canonieke versie. Workspace-specifieke aanpassingen worden overschreven.

---

## 📜 Manifest: agents-publicatie.json

Het manifest bevat metadata van alle beschikbare agents:

### Structuur
```json
{
  "publicatiedatum": "2026-01-22",
  "digest": "a6821",
  "agents": [
    {
      "naam": "agent-curator",
      "valueStream": "agent-enablement",
      "aantalPrompts": 4,
      "aantalRunners": 1
    }
  ],
  "valueStreams": ["agent-enablement", "kennispublicatie", ...],
  "locaties": { ... }
}
```

### Digest (Change Tracking)

De **digest** is een 5-karakter SHA-256 hash van de gesorteerde agents-lijst. Het vervangt versienummering:

- **Doel**: Automatische change-detection
- **Input**: Gesorteerde lijst van agents (naam, valueStream, aantalPrompts, aantalRunners)
- **Output**: Eerste 5 karakters van SHA-256 hash (hex format)
- **Gebruik**: Elke wijziging in agents (toevoegen, verwijderen, artifact-aanpassing) produceert nieuwe digest

**Voordeel**: Content-based change detection zonder handmatige versienummers.

---

## ✅ Correcte Metadata is Verplicht

**Agent-charters moeten correct gevuld zijn**. De charter-header bevat essentiële metadata:

### Verplichte Velden (Charter Header)

```markdown
**Agent**: agent-naam  
**Domein**: Waar gaat het over  
**Agent-soort**: Uitvoerend Agent | Beheeragent | Adviserend Agent  
**Value Stream**: kennispublicatie | architectuur-en-oplossingsontwerp | ...  
```

### Waarom is dit belangrijk?

1. **Agent Curator** scant charter-headers voor metadata-extractie
2. **Manifest generatie** (`agents-publicatie.json`) gebruikt deze metadata
3. **fetch_agents.py** gebruikt value stream voor artifact routing
4. **Digest berekening** gebruikt deze velden voor change-tracking

### Gevolgen van incorrecte metadata:
- ❌ Agent wordt niet opgenomen in manifest
- ❌ Foutieve routing naar workspace (verkeerde folders)
- ❌ Digest wordt niet correct berekend
- ❌ Fetching faalt voor downstream repositories

**Regel**: Charter-header is **authoritative source** voor metadata. Folder locatie is secundair.

---

## 🛠️ Publicatie Workflow

### Publiceer agents-overzicht

```bash
# Windows
publiceer-agents.bat

# Handmatig (alle platforms)
python scripts/runners/agent-curator.py --scope volledig
```

### Output
- `agents-publicatie.json` (root, met digest)
- `docs/resultaten/agent-publicaties/agents-publicatie-YYYYMMDD-HHMMSS.md` (archief)

### Wanneer publiceren?
- Na toevoegen/verwijderen van agent
- Na wijziging van prompts/runners (artifact counts veranderen)
- Na value stream wijziging in charter
- Digest wordt automatisch herberekend

---

## 🎯 Value Streams

Agents zijn georganiseerd per **value stream**:

| Value Stream | Beschrijving | Agents |
|--------------|--------------|--------|
| **agent-enablement** | Agent-creatie en publicatie | agent-curator, agent-smeder |
| **architectuur-en-oplossingsontwerp** | Enterprise/software architectuur | archimate-modelleur, c4-modelleur, bedrijfsarchitect, converter |
| **kennispublicatie** | Content creatie en publicatie | artikel-schrijver, essayist, vertaler, agent-publisher, etc. |
| **it-development** | Software ontwikkeling | workflow-architect, pipeline-executor, python-expert |
| **ondernemingsvorming** | Business strategy | mandarin-ea |
| **utility** | Workspace beheer | moeder, python-expert |

---

## 🔗 Gerelateerde Repositories

- **Canon**: Governance, grondslagen, doctrines (`https://github.com/hans-blok/canon.git`)
- **Workspaces**: Repositories die agents fetchen (kennispublicatie, architectuur, etc.)

---

## 📞 Support

Voor vragen over:
- **Agent creatie**: Gebruik `@agent-smeder` of `moeder` in workspace
- **Publicatie issues**: Check `scripts/runners/agent-curator.py` logs
- **Fetching problemen**: Check `logs/fetch-agents-*.log` in workspace
- **Metadata errors**: Valideer charter headers tegen template

---

**Laatst bijgewerkt**: 2026-01-22  
**Digest**: a6821  
**Agents**: 18
