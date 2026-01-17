# fetch_agents.py

Python script om agents op te halen uit een remote GitHub repository en deze netjes in de lokale workspace in te ordenen.

## Functie

Haalt agents op uit:
- **Value-stream specifiek**: `exports/<value-stream>/{prompts, charters-agents, runners}`
- **Utility agents**: `exports/utility/{prompts, charters-agents, runners}`

En plaatst deze in:
- **Prompts** (`.prompt.md`) → `.github/prompts/`
- **Charters** (`charter.*.md`) → `charters-agents/`
- **Runners** (`.py`) → `scripts/`

## Gebruik

```bash
# Standaard (haalt van hans-blok/agent-services)
python scripts/fetch_agents.py <value-stream>

# Voorbeeld
python scripts/fetch_agents.py kennispublicatie
python scripts/fetch_agents.py it-development
python scripts/fetch_agents.py utility
```

### Opties

- `--source-repo <url>` — Custom repository URL (default: hans-blok/agent-services)
- `--no-cleanup` — Behoud temp-directory voor inspectie

### Voorbeelden

```bash
# Fetch van eigenrepo
python scripts/fetch_agents.py kennispublicatie --source-repo https://github.com/user/my-repo.git

# Debug: behoud temp files
python scripts/fetch_agents.py it-development --no-cleanup
```

## Output

```
📥 Cloning repository: ...
✓ Found value-stream folder: kennispublicatie
✓ Found utility agents

📊 Summary:
  Value-stream agents: 21
  Utility agents: 11

📁 Organizing 32 agent files...
  ✓ agent-publisher-publiceer.prompt.md → .github/prompts/...
  ✓ charter.agent-publisher.md → charters-agents/...
  ...

✅ Agents organized successfully
```

## Vereisten

- Python 3.7+
- `git` command-line tool

## Wat gebeurt er?

1. Clone remote repo in temp-directory
2. Zoek `exports/<value-stream>` en `exports/utility`
3. Verzamel `.prompt.md`, `charter.*.md` en `.py` bestanden
4. Kopieër naar locale workspace mappen (`.github/prompts/`, `charters-agents/`, `scripts/`)
5. Opschonen temp-directory

## Foutafhandeling

Script stopt en geeft duidelijke foutmeldingen als:
- Value-stream folder niet gevonden
- Git clone faalt
- Kopieën van bestanden mislukt

---

**Script locatie**: `scripts/fetch_agents.py`  
**Werkomgeving**: Vereist in root van agent-services workspace
