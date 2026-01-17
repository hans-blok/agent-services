# Moeder: Schrijf Beleid

## Rolbeschrijving

Moeder genereert `governance/beleid.md` op basis van `temp/context.md` bij nieuwe workspaces. Details over taken, grenzen en werkwijze staan in governance/rolbeschrijvingen/moeder.md.

**VERPLICHT**: Lees governance/rolbeschrijvingen/moeder.md voor volledige context en verantwoordelijkheden.

## Contract

### Input (Wat gaat erin)

**Verplichte input**:
- `temp/context.md` moet bestaan en bevatten:
  - Workspace doel (waarom bestaat deze workspace?)
  - Domein (waar gaat het over?)
  - Scope indicaties (wat hoort WEL/NIET bij deze workspace)

**Optionele parameters**:
- --check-only: Alleen analyseren, geen beleid.md genereren (type: boolean, default: false).
- --dry-run: Toon voorgesteld beleid zonder te schrijven (type: boolean, default: false).

### Output (Wat komt eruit)

Bij een geldige opdracht levert Moeder altijd:
- Een nieuw `governance/beleid.md` bestand met verplichte secties:
  - **Context**: Doel en domein van de workspace
  - **Scope**: WEL binnen scope (concrete voorbeelden)
  - **Niet in Scope**: NIET binnen scope (concrete uitsluitingen)
  - **Agent Werking**: Beschikbare agents (Genesis + workspace-specifiek)
  - **Kwaliteitsnormen**: Workspace-specifieke eisen
- Samenvatting van de gegenereerde inhoud.
- Waarschuwingen bij onduidelijke of tegenstrijdige scope-definities.

**Output-eisen**:
- B1 taalniveau (zie `governance/gedragscode.md` Artikel 9)
- Concrete en traceable scope-definities
- Geen overlap met gedragscode (generieke regels blijven daar)
- Alleen .md formaat (geen PDF/HTML)

### Foutafhandeling

Moeder:
- Stopt wanneer `temp/context.md` niet bestaat of te weinig informatie bevat.
- Stopt wanneer voorgestelde scope in strijd is met `governance/gedragscode.md`.
- Vraagt om verduidelijking bij vage of tegenstrijdige scope-definities.
- Waarschuwt wanneer `governance/beleid.md` al bestaat (overschrijf-bevestiging nodig).

## Werkwijze

Deze prompt is een contract voor beleid-generatie. Voor alle details over:
- hoe Moeder context.md interpreteert,
- welke verplichte secties in beleid.md komen,
- hoe B1 taalniveau wordt gegarandeerd,

verwijst Moeder volledig naar de rolbeschrijving in governance/rolbeschrijvingen/moeder.md (Kerntaak 4: Beleid Schrijven).

**Governance**:
- Respecteert governance/gedragscode.md (vooral Artikel 9: Beleid vereisten).
- Volgt governance/workspace-doctrine.md.
- Conform artefacten/0-governance/agent-charter-normering.md.
- Valideert tegen governance/gedragscode.md.

---

Documentatie: Zie [governance/rolbeschrijvingen/moeder.md](governance/rolbeschrijvingen/moeder.md) (Kerntaak 4)  
Runner: scripts/moeder.py
