# Agent Boundary — Converter MD to ArchiMate

**Aangemaakt**: 2026-01-22  
**Beheerd door**: Agent Curator  
**Value Stream**: architectuur-en-oplossingsontwerp

---

## Aanleiding

Er is behoefte om bestaande ArchiMate-modellen die in gestructureerd Markdown zijn vastgelegd om te zetten naar tool-importeerbare formaten zoals Archi XML of Open Exchange Format. Dit maakt de modellen bruikbaar in ArchiMate-tooling voor visualisatie, analyse en verdere bewerking. De converter biedt een brug tussen markdown-gebaseerde documentatie en ArchiMate tooling.

---

## Gewenste Capability

Converteert gestructureerd Markdown met ArchiMate-elementen en relaties naar tool-importeerbare formaten (Archi XML, Open Exchange Format) volgens ArchiMate 3.x specificatie.

---

## Output (4 regels)

```
agent-naam: converter-md-to-archimate
capability-boundary: Converteert gestructureerd Markdown met ArchiMate-elementen en relaties naar tool-importeerbare formaten (Archi XML, Open Exchange Format); valideert input-structuur en output-conformiteit.
doel: ArchiMate Markdown-modellen omzetten naar tooling-importeerbare formaten voor visualisatie en analyse.
domein: ArchiMate format conversie
```

---

## Toelichting Boundary

### Agent-naam
- **converter-md-to-archimate** — lowercase, hyphens, duidelijke conversie-richting (Markdown → ArchiMate tool formats)

### Capability-boundary
- **Wat de agent WEL doet**: 
  - Converteert gestructureerd Markdown naar Archi XML formaat
  - Converteert gestructureerd Markdown naar Open Exchange Format (OEF)
  - Valideert input Markdown structuur (correcte element-codes, relatie-types)
  - Valideert output conformiteit aan ArchiMate 3.x specificatie
  - Mapt Markdown-elementen naar correcte ArchiMate XML-elementen
  - Behoudt traceerbaarheid (element IDs, relaties, metadata)
  - Ondersteunt alle ArchiMate-lagen (motivatie, strategie, business, applicatie, technologie, implementatie/migratie)

- **Wat de agent NIET doet**: 
  - Creëert geen nieuwe ArchiMate-modellen (zie archimate-modelleur)
  - Valideert geen model-kwaliteit of architecturale correctheid (zie archimate-modelleur analyse)
  - Genereert geen visualisaties of diagrammen
  - Wijzigt geen model-inhoud of -structuur
  - Converteert niet van tool-formaten naar Markdown (inverse conversie)
  - Genereert geen HTML/PDF publicaties (zie Publisher)

### Doel
ArchiMate Markdown-modellen die door archimate-modelleur zijn geproduceerd omzetten naar tool-importeerbare formaten, zodat deze gebruikt kunnen worden in ArchiMate-tooling (Archi, Sparx EA) voor visualisatie en verdere analyse.

### Domein
ArchiMate format conversie — specifiek de technische transformatie tussen tekstuele (Markdown) en tool-importeerbare (XML/OEF) representaties van ArchiMate-modellen.

---

## Consistentie met Value Stream

De agent past binnen **architectuur-en-oplossingsontwerp** omdat:
- Het architectuurmodellen toegankelijk maakt in professionele tooling
- Het complementair is aan archimate-modelleur (die modelleert in Markdown)
- Het technische format-conversie uitvoert zonder architectuurinhoud te wijzigen
- Het de workflow ondersteunt: modelleren (archimate-modelleur) → converteren (converter-md-to-archimate) → visualiseren/analyseren (in tooling)

---

## Overlap-analyse en Positionering

### Complementair met archimate-modelleur
- **archimate-modelleur**: Modelleert ArchiMate uit tekst → Markdown output
- **converter-md-to-archimate**: Converteert Markdown → tool-formaten (Archi XML, OEF)
- **Geen overlap**: Verschillende verantwoordelijkheden in de model-lifecycle
- **Workflow**: tekst → [archimate-modelleur] → Markdown → [converter-md-to-archimate] → Archi XML/OEF → tooling

### Onderscheid met andere agents
- **Publisher**: Converteert naar HTML/PDF (publicatieformaten), niet naar tool-formaten
- **Solution Architect agents**: Maken architectuurbeslissingen, geen format-conversie
- **Vertaler**: Vertaalt talen (NL/EN), niet formaten

### Typische use cases
1. Import ArchiMate-modellen in Archi tool voor diagrammen
2. Export naar Open Exchange Format voor enterprise repositories
3. Integratie met Sparx Enterprise Architect
4. Validatie van modellen in professionele tooling

---

## Aanbevelingen

1. **Folder structuur**: Plaats agent-artefacten in `exports/architectuur-en-oplossingsontwerp/`:
   - `charters-agents/charter.converter-md-to-archimate.md`
   - `prompts/` voor prompt-contracten
   - `runners/` voor Python conversion scripts

2. **Input-formaat**: Definieer duidelijk verwacht Markdown-structuur:
   - Element-codes (D01, A01, G01, BA01, etc.)
   - Relatie-notatie (element1 --[serving]--> element2)
   - Metadata-headers (naam, type, laag, beschrijving)

3. **Output-formaten**: Prioriteer:
   - **Archi XML** (meest gebruikt, Archi tool compatibel)
   - **Open Exchange Format** (ArchiMate standaard uitwisselformaat)
   - Optioneel: andere tool-specifieke formaten

4. **Validatie**: Twee-staps validatie:
   - Input: Markdown-structuur correct en compleet?
   - Output: XML/OEF conform ArchiMate 3.x schema?

5. **Traceerbaarheid**: Behoud:
   - Element IDs van Markdown naar XML
   - Metadata (aanmaakdatum, bron-document referentie)
   - Relatie-mappings voor troubleshooting

6. **Error handling**: Duidelijke foutmeldingen bij:
   - Ongeldige element-codes in Markdown
   - Ontbrekende verplichte velden
   - Relaties naar niet-bestaande elementen
   - XML schema validatie failures

---

**Status**: Boundary gedefinieerd, gereed voor handoff naar Agent Smeder

