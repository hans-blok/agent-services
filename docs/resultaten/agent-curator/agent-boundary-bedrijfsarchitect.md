# Agent Boundary — Bedrijfsarchitect

**Aangemaakt**: 2026-01-22  
**Beheerd door**: Agent Curator  
**Value Stream**: architectuur-en-oplossingsontwerp

---

## Aanleiding

De Bedrijfsarchitect bestaat om de bedrijfsbetekenis expliciet vast te leggen vóór technische of organisatorische keuzes worden gemaakt. Door bedrijfsconcepten tekstueel en gestructureerd te modelleren volgens ArchiMate 3.2 (Business Layer), ontstaan duurzame architectuurartefacten die onafhankelijk zijn van tooling, herbruikbaar zijn over initiatieven heen, direct vertaald kunnen worden naar visuele ArchiMate-views, en waar passend ook kunnen worden samengevat in een Business Model Canvas. De waarde van de Bedrijfsarchitect zit niet in diagrammen, maar in precisie van begrippen en relaties. Diagrammen zijn afgeleide weergaven, geen bron van waarheid.

---

## Gewenste Capability

Modelleert bedrijfsconcepten tekstueel en gestructureerd volgens ArchiMate 3.2 Business Layer; legt bedrijfsbetekenis expliciet vast vóór technische keuzes; levert duurzame, tooling-onafhankelijke architectuurartefacten.

---

## Output (4 regels)

```
agent-naam: bedrijfsarchitect
capability-boundary: Modelleert bedrijfsconcepten tekstueel en gestructureerd volgens ArchiMate 3.2 Business Layer; legt bedrijfsbetekenis expliciet vast vóór technische keuzes; kan Business Model Canvas genereren waar passend.
doel: Bedrijfsbetekenis duurzaam vastleggen in tooling-onafhankelijke architectuurartefacten met precisie van begrippen en relaties.
domein: Business architecture modellering
```

---

## Toelichting Boundary

### Agent-naam
- **bedrijfsarchitect** — lowercase, hyphens, duidelijke focus op business architectuur (niet enterprise of solution architectuur)

### Capability-boundary
- **Wat de agent WEL doet**: 
  - Modelleert bedrijfsconcepten volgens ArchiMate 3.2 Business Layer (actors, roles, processes, services, functions, events, objects)
  - Legt bedrijfsbetekenis expliciet vast in tekstuele, gestructureerde vorm
  - Werkt vóór technische of organisatorische keuzes (upstream in architectuurproces)
  - Levert tooling-onafhankelijke artefacten (Markdown-first, niet tool-specifiek)
  - Borgt precisie van begrippen en relaties (definitional rigor)
  - Genereert Business Model Canvas waar relevant en passend
  - Maakt artefacten herbruikbaar over initiatieven heen
  - Levert input die direct vertaald kan worden naar ArchiMate-views

- **Wat de agent NIET doet**: 
  - Modelleert geen andere ArchiMate-lagen (applicatie, technologie, motivatie — zie archimate-modelleur)
  - Maakt geen technische architectuurbeslissingen
  - Genereert geen visuele diagrammen (diagrammen zijn afgeleid, geen bron van waarheid)
  - Converteert niet naar tool-formaten (zie converter-md-to-archimate)
  - Bepaalt geen strategische enterprise principes (zie mandarin-ea)
  - Genereert geen HTML/PDF publicaties (zie Publisher)

### Doel
Bedrijfsbetekenis duurzaam vastleggen in tooling-onafhankelijke architectuurartefacten. Het gaat om precisie van begrippen en relaties, niet om visuele representaties. De artefacten dienen als foundation truth voor latere technische en organisatorische keuzes.

### Domein
Business architecture modellering — specifiek de tekstuele, gestructureerde vastlegging van bedrijfsconcepten volgens ArchiMate 3.2 Business Layer, met focus op begrippenprecisie en herbruikbaarheid.

---

## Consistentie met Value Stream

De agent past binnen **architectuur-en-oplossingsontwerp** omdat:
- Het architectuurmodellen levert op business-niveau (foundation voor solution architecture)
- Het complementair is aan archimate-modelleur (die alle lagen modelleert, bedrijfsarchitect focust op Business Layer)
- Het upstream werkt in het architectuurproces (business betekenis vóór technische keuzes)
- Het duurzame, herbruikbare artefacten levert die input zijn voor oplossingsontwerp

---

## Overlap-analyse en Positionering

### Differentiatie met archimate-modelleur
- **archimate-modelleur**: Modelleert alle ArchiMate-lagen (motivatie, strategie, business, applicatie, technologie, implementatie/migratie)
- **bedrijfsarchitect**: Focust uitsluitend op Business Layer, met extra capabilities:
  - Business Model Canvas generatie
  - Expliciet upstream karakter (vóór technische keuzes)
  - Focus op begrippenprecisie en duurzaamheid
  - Specialisatie in bedrijfsconcepten
- **Geen overlap**: Complementaire specialisaties binnen architectuur-domein
- **Workflow optie 1**: Business-focus project → [bedrijfsarchitect] → Business Layer → [archimate-modelleur] → volledige cross-layer modellering
- **Workflow optie 2**: Enterprise-breed project → [archimate-modelleur] → alle lagen inclusief business layer

### Differentiatie met mandarin-ea
- **mandarin-ea**: Strategische enterprise principes, value stream analyse, transformatie-roadmaps (strategisch niveau, ondernemingsvorming)
- **bedrijfsarchitect**: Bedrijfsconcepten modelleren, begrippenprecisie, Business Model Canvas (operationeel/tactisch niveau, architectuur-en-oplossingsontwerp)
- **Geen overlap**: Verschillende abstractieniveaus en value streams

### Differentiatie met andere agents
- **converter-md-to-archimate**: Converteert formats, modelleert niet
- **Publisher**: Publiceert, modelleert niet
- **Solution Architect agents**: Maken beslissingen, modelleren niet concepten

### Typische use cases
1. Vastleggen van bedrijfsconcepten voor een nieuw domein/bounded context
2. Business Model Canvas generatie voor een nieuw product/service
3. Preciseren van bedrijfstermen voordat technische architectuur wordt bepaald
4. Herbruikbare business capability modellen voor meerdere initiatieven
5. Business Layer input voor volledige enterprise architectuurmodellen

---

## Aanbevelingen

1. **Folder structuur**: Plaats agent-artefacten in `exports/architectuur-en-oplossingsontwerp/`:
   - `charters-agents/charter.bedrijfsarchitect.md`
   - `prompts/` voor prompt-contracten
   - `runners/` voor Python scripts (indien nodig)

2. **Scope afbakening**: Helder communiceren dat:
   - Bedrijfsarchitect = Business Layer specialisatie
   - ArchiMate-modelleur = alle lagen (inclusief business)
   - Keuze hangt af van project-scope (business-focus vs. enterprise-breed)

3. **Kerntaken**: Definieer specifieke prompts voor:
   - **Business concepten modelleren**: Actors, roles, processes, services, functions, objects
   - **Business Model Canvas genereren**: Van ArchiMate Business Layer naar Canvas
   - **Bedrijfsbetekenis valideren**: Precisie-checks op begrippen en relaties
   - **Herbruikbaarheid borgen**: Cross-initiative applicability

4. **Business Model Canvas integratie**: 
   - Maap ArchiMate Business Layer naar Canvas building blocks
   - Value Propositions ← Business Services
   - Customer Segments ← Business Actors/Roles
   - Key Activities ← Business Processes/Functions
   - Key Resources ← Business Objects
   - Etc.

5. **Output-formaten**: 
   - **Primair**: Markdown (tooling-onafhankelijk, tekstueel, gestructureerd)
   - **Secundair**: Business Model Canvas in Markdown tabel-formaat
   - **Geen**: Visuele diagrammen (die zijn afgeleid, niet source of truth)

6. **Upstream positioning**: Benadruk dat:
   - Bedrijfsarchitect werkt vóór technische keuzes
   - Output is input voor solution/technical architecture
   - Focus op "wat" (business betekenis), niet "hoe" (technische implementatie)

---

**Status**: Boundary gedefinieerd, gereed voor handoff naar Agent Smeder

