# Agent Boundary — c4-modelleur

**Datum**: 2026-01-22  
**Aangemaakt door**: Agent Curator  
**Value Stream**: architectuur-en-oplossingsontwerp

---

## Boundary Output

```
agent-naam: c4-modelleur
capability-boundary: Modelleert softwarearchitectuur volgens C4-methode (Context, Containers, Components, Code); genereert tekstuele C4-modellen in Markdown
doel: Software-architectuur visualiseerbaar vastleggen met focus op verschillende abstractieniveaus
domein: Software-architectuur modellering
```

---

## Toelichting

### Aanleiding
C4 is een veelgebruikte methode voor het communiceren van software-architectuur op vier abstractieniveaus. De C4-modelleur vult een specifieke niche naast de bestaande architecture agents: waar ArchiMate zich richt op enterprise architecture en bedrijfslagen, focust C4 op software system architecture met emphasis op containers en components.

### Capability Beschrijving
De c4-modelleur modelleert software-architectuur volgens de C4-methode:
- **Level 1: System Context** — Systeem in zijn omgeving (users, external systems)
- **Level 2: Container** — High-level technology choices (applications, databases, file systems)
- **Level 3: Component** — Componentenstructuur binnen containers
- **Level 4: Code** — UML class diagrams (optioneel, vaak te gedetailleerd)

De agent levert tekstuele C4-modellen in Markdown-formaat, tooling-onafhankelijk. Diagrammen kunnen daaruit afgeleid worden via tools zoals Structurizr, PlantUML of C4-PlantUML.

### Differentiatie met Bestaande Agents

**vs. archimate-modelleur**:
- ArchiMate: Enterprise architecture, alle lagen (business, application, technology)
- C4: Software-systeem architectuur, focus op containers/components
- Geen overlap: verschillende notaties, verschillende abstractieniveaus
- Complementair: ArchiMate voor enterprise view, C4 voor software detail

**vs. bedrijfsarchitect**:
- Bedrijfsarchitect: Business Layer only, upstream positioning
- C4: Software architecture, downstream positioning (na business requirements)
- Geen overlap: verschillende domeinen (business vs. technical)

**vs. converter-md-to-archimate**:
- Converter: Format transformatie (Markdown → tool formats)
- C4: Content creatie (architecture modeling)
- Geen overlap: verschillende taken (transformatie vs. creatie)

### Positionering in Value Stream
De c4-modelleur opereert in de value stream "architectuur-en-oplossingsontwerp" als:
- **Uitvoerend Agent** voor software-architectuur modellering
- **Downstream** van bedrijfsarchitect (na business requirements)
- **Input provider** voor solution architects en development teams
- **Complementair** aan archimate-modelleur (andere notatie, andere focus)

### Scope
**Binnen scope**:
- C4 Level 1–3 (System Context, Container, Component)
- Tekstuele model-beschrijvingen in Markdown
- Element-definities en relaties
- Tooling-onafhankelijke output
- Validatie van volledigheid en consistentie

**Buiten scope**:
- Enterprise architecture (zie archimate-modelleur)
- Business Layer modellering (zie bedrijfsarchitect)
- Visuele diagrammen als source of truth (alleen tekstueel)
- Format conversie naar tool-specifieke formats (zie converter)
- Code-level details (C4 Level 4 is optioneel/excluded)

### Use Cases
1. **Software System Context vastleggen**: Wie/wat interacteert met het systeem
2. **Container Diagram maken**: Welke applicaties, databases, services bouwen we
3. **Component Diagram uitwerken**: Interne structuur van containers
4. **Solution Architecture documenteren**: Hoe ziet de technische oplossing eruit
5. **ADR-ondersteuning**: C4-diagrams als input voor Architecture Decision Records

### Aanbevelingen
- Gebruik C4 voor software-systeem architectuur waar focus op containers/components relevant is
- Gebruik ArchiMate voor enterprise-wide architectuur en cross-layer traceerbaarheid
- Combineer indien nodig: ArchiMate voor enterprise view, C4 voor software detail
- Markdown als source of truth, diagrammen zijn afgeleid
- Integreer met ADR-proces (C4 models ondersteunen decision documentation)

---

## Consistency Check

**Overlap met bestaande agents**: Geen  
**Value stream validatie**: ✅ architectuur-en-oplossingsontwerp bestaat en is geregistreerd  
**Boundary sharpness**: ✅ Eén zin, helder afgebakend  
**Governance compliance**: ✅ Binnen scope van software/IT architectuur  

---

## Referenties
- **C4 Model**: https://c4model.com/ (Simon Brown)
- **Value Streams Overzicht**: docs/resultaten/agent-curator/value-streams-overzicht.md
- **Agent Charter Normering**: canon/grondslagen/globaal/agent-charter-normering.md
- **Complementaire Agents**: archimate-modelleur, bedrijfsarchitect, converter-md-to-archimate

---

**Status**: Goedgekeurd voor handoff naar Agent Smeder  
**Volgende stap**: Agent Smeder Stap 1 (definieer prompt contract)
