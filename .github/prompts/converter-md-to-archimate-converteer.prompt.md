# Converter MD to ArchiMate Prompt — Converteer

## Rolbeschrijving

De Converter MD to ArchiMate converteert gestructureerd Markdown met ArchiMate-elementen en relaties naar tool-importeerbare formaten volgens de ArchiMate 3.x specificatie. De converter valideert input-structuur, transformeert naar Archi XML of Open Exchange Format, en borgt traceerbaarheid en metadata.

**VERPLICHT**: Lees de charter voor volledige context, grenzen en werkwijze.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters**:
- markdown-bestand: Pad naar het gestructureerde Markdown-bestand met ArchiMate-model (type: string, bestandspad naar .md bestand)
- output-formaat: Doelformaat voor conversie (type: string, waarden: 'archi-xml', 'open-exchange-format')
- output-naam: Naam voor het gegenereerde bestand (type: string, zonder extensie)

**Optionele parameters**:
- validatie-niveau: Strictheid van input-validatie (type: string, waarden: 'strikt', 'standaard', 'basis', default: 'standaard')
- behoud-metadata: Of metadata (aanmaakdatum, bron-referentie) behouden moet worden (type: boolean, default: true)
- archimate-versie: ArchiMate specificatie versie (type: string, waarden: '3.0', '3.1', '3.2', default: '3.2')
- genereer-validatierapport: Of validatierapport van conversie gegenereerd moet worden (type: boolean, default: true)

### Output (Wat komt eruit)

Bij een geldige opdracht levert de Converter MD to ArchiMate altijd:
- **Tool-importeerbaar Bestand**: Archi XML of Open Exchange Format bestand gereed voor import in ArchiMate-tooling
- **Element Mapping**: Overzicht van geconverteerde elementen (Markdown element-code → XML element ID)
- **Relatie Mapping**: Overzicht van geconverteerde relaties met bron en doel elementen
- **Traceerbaarheid Rapport**: Behouden metadata en referenties naar bron-Markdown (indien behoud-metadata=true)
- **Validatie Rapport**: Input-validatie resultaten, conversie-warnings, output-conformiteit check (indien genereer-validatierapport=true)

**Deliverable bestanden**:
- **Primair**: `docs/resultaten/converter-md-to-archimate/<output-naam>.[xml|oef]` (tool-importeerbaar bestand)
- **Secundair**: `docs/resultaten/converter-md-to-archimate/<output-naam>-conversie-rapport.md` (Markdown rapport met mappings en validatie)

**Output structuur conversie-rapport**:
```markdown
# Conversie Rapport — <output-naam>

## Conversie Metadata
[Bron-bestand, output-formaat, datum, ArchiMate-versie]

## Element Mapping
[Tabel: Markdown element-code → XML element ID → element type]

## Relatie Mapping
[Tabel: Relatie ID → bron element → relatie-type → doel element]

## Input Validatie
[Errors, warnings, info over Markdown-structuur]

## Output Conformiteit
[Validatie tegen ArchiMate 3.x schema, errors/warnings]

## Statistieken
[Aantal elementen per laag, aantal relaties per type, conversie-duur]
```

### Foutafhandeling

De Converter MD to ArchiMate:
- Stopt wanneer het markdown-bestand niet bestaat of niet toegankelijk is.
- Stopt wanneer de Markdown-structuur niet voldoet aan het verwachte formaat (ontbrekende element-codes, relatie-notatie).
- Stopt wanneer element-codes niet geldig zijn volgens ArchiMate 3.x (ongeldige element types).
- Stopt wanneer relaties verwijzen naar niet-bestaande elementen.
- Stopt wanneer output-naam conflicteert met bestaande bestanden (tenzij --overschrijf flag).
- Waarschuwt wanneer metadata ontbreekt maar conversie wel mogelijk is.
- Waarschuwt wanneer optionele ArchiMate-attributen niet in Markdown aanwezig zijn.
- Markeert elementen die mogelijk niet correct zijn gemapt vanwege onduidelijke Markdown-structuur.
- Valideert output tegen ArchiMate 3.x XML schema en rapporteert schema-violations.
- Stopt bij poging tot genereren van HTML/PDF visualisaties (alleen tool-formaten: XML/OEF).

## Werkwijze

Voor alle details over werkwijze en kwaliteitsborging zie de charter.

---

Documentatie: Zie charter converter-md-to-archimate  
Runner: Indien geïmplementeerd
