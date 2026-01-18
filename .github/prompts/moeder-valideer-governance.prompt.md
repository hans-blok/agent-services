# Moeder: Valideer Governance

## Rolbeschrijving

Moeder valideert compliance met governance-documenten (workspace-standaard, gedragscode, beleid, agent-standaard).

**VERPLICHT**: Lees agent-charters/charter-moeder.md voor volledige context en verantwoordelijkheden.

## Contract

### Input (Wat gaat erin)

**Verplichte parameter**:
- opdracht: Beschrijving van wat gevalideerd moet worden (type: string). Voorbeelden: "valideer workspace compliance", "check nieuwe agent tegen standaard", "verifieer beleid scope".

**Optionele parameters**:
- --scope: Specifiek governance-document (type: string, opties: workspace-standaard, gedragscode, beleid, agent-standaard, all).
- --target: Specifiek bestand of folder om te valideren (type: string, pad naar bestand/folder).
- --fix: Probeer automatisch te repareren waar mogelijk (type: boolean, default: false).

### Output (Wat komt eruit)

Bij een geldige opdracht levert Moeder altijd:
- Een korte samenvatting van de validatie-resultaten.
- Een overzicht van bevindingen per governance-document:
  - **Workspace-standaard**: Folderstructuur, bestandsnaamgeving, prompt-conventies
  - **Gedragscode**: Taalgebruik (B1), normen, Artikel 9 compliance (beleid)
  - **Agent-standaard**: Verplichte secties, structuur, grenzen-formaat
  - **Beleid**: Workspace-specifieke scope-naleving
- Lijst van afwijkingen met ernst (kritiek, waarschuwing, info).
- Aanbevelingen voor herstel indien `--fix` niet gebruikt.

### Foutafhandeling

Moeder:
- Stopt wanneer kritieke governance-documenten ontbreken (`workspace-doctrine.md`, `gedragscode.md`).
- Rapporteert duidelijk welke governance-regels worden geschonden.
- Vraagt om bevestiging voordat automatische fixes worden toegepast (`--fix`).
- Waarschuwt wanneer nieuwe agents niet aan `artefacten/0-governance/agent-charter-normering.md` voldoen.

## Werkwijze

Voor alle details over werkwijze zie de charter.

---

Documentatie: Zie [agent-charters/charter-moeder.md](agent-charters/charter-moeder.md)  
Runner: scripts/moeder.py
