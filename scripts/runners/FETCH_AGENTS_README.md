# fetch_agents.py

Haal agents op uit agent-services repository en orden ze lokaal.

## Gebruik

```bash
# Vanuit workspace root
fetch-agents <value-stream>

# Voorbeelden
fetch-agents kennispublicatie
fetch-agents it-development
fetch-agents utility
```

## Wat doet het?

Haalt agents op uit **één bron**: `github.com/hans-blok/agent-services`

- Value-stream agents: `exports/<value-stream>/`
- Utility agents: `exports/utility/`

Plaatst ze in:
- `.github/prompts/` — prompts
- `charters-agents/` — charters  
- `scripts/` — runners

## Vereisten

- Python 3.7+
- Git command-line tool

---

**Bron**: https://github.com/hans-blok/agent-services  
**Script**: `scripts/fetch_agents.py`
