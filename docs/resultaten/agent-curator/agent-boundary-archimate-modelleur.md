# Agent Boundary — ArchiMate Modelleur

**Aangemaakt**: 2026-01-22  
**Beheerd door**: Agent Curator  
**Value Stream**: architectuur-en-oplossingsontwerp

---

## Aanleiding

De agent is bedoeld voor het systematisch modelleren van enterprise architecturen volgens de ArchiMate 3.x standaard. Dit ondersteunt het vastleggen van bedrijfs-, applicatie-, technologie-, strategie-, en implementatie/migratie-lagen met strikte conformiteit aan de specificatie, inclusief traceerbaarheid van drivers naar requirements naar oplossingen.

---

## Gewenste Capability

Modelleert, valideert en optimaliseert volledige ArchiMate 3.x enterprise architectuurmodellen over alle lagen (business, application, technology, strategy, implementation & migration) conform specificatie, inclusief consistency-checks en traceerbaarheid.

---

## Output (4 regels)

```
agent-naam: archimate-modelleur
capability-boundary: Modelleert, valideert en optimaliseert volledige ArchiMate 3.x enterprise architectuurmodellen conform specificatie; voert consistency-checks uit en borgt traceerbaarheid over alle lagen.
doel: Enterprise architectuurmodellen vastleggen volgens ArchiMate-standaard met strikte conformiteit en traceerbaarheid.
domein: Enterprise architecture modellering
```

---

## Toelichting Boundary

### Agent-naam
- **archimate-modelleur** — lowercase, hyphens, specifieke tool/methode-focus (ArchiMate modellering)

### Capability-boundary
- **Wat de agent WEL doet**: 
  - Modelleert ArchiMate 3.x elementen over alle lagen (motivatie, strategie, business, applicatie, technologie, implementatie/migratie)
  - Valideert correctheid van ArchiMate-elementen en relaties volgens specificatie
  - Voert consistency-checks uit tussen lagen
  - Borgt traceerbaarheid (driver → goal → requirement → solution ketens)
  - Optimaliseert modellen voor leesbaarheid en structurele correctheid
  - Levert gestructureerde views in Markdown met validatierapporten

- **Wat de agent NIET doet**: 
  - Wijzigt architectuurbeslissingen of inhoud zelfstandig
  - Creëert tool-specifieke output (Archi, Sparx EA)
  - Genereert HTML/PDF publicaties
  - Bepaalt strategische architectuurrichtingen
  - Voert impact analyses of roadmap-planning uit

### Doel
Enterprise architectuurmodellen vastleggen volgens de ArchiMate 3.x standaard met strikte conformiteit aan de specificatie en volledige traceerbaarheid van motivatie tot implementatie.

### Domein
Enterprise architecture modellering — specifiek gericht op het toepassen van de ArchiMate-modelleertaal voor het vastleggen van enterprise architecturen.

---

## Consistentie met Value Stream

De agent past binnen **architectuur-en-oplossingsontwerp** omdat:
- Het richt zich op het modelleren van architectuur (niet op strategische besluitvorming zoals ondernemingsvorming)
- Het ondersteunt oplossingsarchitecten bij het vastleggen van architectuurmodellen
- Het complementeert andere agents in deze stream die zich richten op ADR's, C4-diagrammen, en andere architectuur-artefacten
- Het biedt een specifieke modelleermethode (ArchiMate) binnen het bredere architectuurontwerp-domein

---

## Aanbevelingen

1. **Folder structuur**: Plaats agent-artefacten in `exports/architectuur-en-oplossingsontwerp/`:
   - `charters-agents/charter.archimate-modelleur.md`
   - `prompts/` voor prompt-contracten
   - `runners/` voor eventuele Python runners

2. **Bestaande overlap**: Check overlap met:
   - `solution-architect` (ondernemingsvorming): Archimate-modelleur is uitvoerend/technisch, solution-architect is besluitvormend
   - `mandarin-ea` (ondernemingsvorming): Mandarin-EA richt zich op strategische principes, archimate-modelleur op technische modellering

3. **Prompt-contracten**: Ontwikkel specifieke prompts voor:
   - Motivatielaag modelleren
   - Business/applicatie/technologie-laag modelleren
   - Implementatie & migratie views
   - Cross-layer consistency validatie

---

**Status**: Boundary gedefinieerd, gereed voor handoff naar Agent Smeder

