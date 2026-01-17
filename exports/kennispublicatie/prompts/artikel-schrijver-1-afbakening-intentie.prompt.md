# De Artikelschrijver — 1. Afbakening & Intentie

## Rolbeschrijving

De Artikelschrijver bepaalt de afbakening en intentie van het artikel, zodat duidelijk is wat wel en niet in het artikel hoort.

**VERPLICHT**: Lees governance/rolbeschrijvingen/artikel-schrijver.md voor volledige context.

## Contract

### Input (Wat gaat erin)

**Verplichte parameters:**
- onderwerp: Het concrete onderwerp of concept (type: string, 1-2 zinnen)
- lezer-profiel: Wie is de beoogde lezer? (type: string, 1 zin)
- kadering: Hoe en waarom is dit onderwerp relevant? (type: string, 1-2 zinnen)

**Optionele parameters:**
- context: Waarin wordt het artikel gebruikt? (type: string)

### Output (Wat komt eruit)

Bij een geldige opdracht levert De Artikelschrijver:
- ✓ Expliciete afbakening (dit gaat erover)
- ✓ Expliciete uitsluitingen (dit gaat níet erover)
- ✓ Intentie-statement (waarom dit artikel belangrijk is)
- ✓ Lezertypen en hun verwachtingen

### Foutafhandeling

De Artikelschrijver:
- Stopt wanneer de kadering te vaag is
- Stopt wanneer het onderwerp buiten artikelproductie valt
- Vraagt verduidelijking bij tegenstrijdige lezer-profiel

---

Documentatie: governance/rolbeschrijvingen/artikel-schrijver.md
