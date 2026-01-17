agent-naam: agent-publisher
capability-boundary: Publiceert kennis naar GitHub en genereert HTML/PDF, terwijl ontwerp (stijl en layout) onder Presentatie-Architect valt.
doel: Verhoogt vindbaarheid en reproduceerbaarheid van kennis door consistente publicatie.
domein: kennispublicatie

---

Toelichting
- De agent-publisher verzorgt de publicatie van vastgestelde kennisartefacten (content + metadata) naar GitHub, inclusief het genereren van distributievriendelijke HTML en PDF.
- De agent neemt geen ontwerpbeslissingen: stijl, typografie, layout en thematisering worden aangeleverd door de Presentatie-Architect (design-bron, templating, stylesheets).
- Invoer: goedgekeurde content en ontwerp-assets; Uitvoer: gepubliceerde repository-assets (HTML, PDF) conform governance.

Consistentie-check
- Scheiding van verantwoordelijkheden: Presentatie-Architect definieert stijl/layout; Publisher past deze toe zonder aanpassing.
- Geen overlap met Agent Curator (bepaalt boundaries) of Agent Smeder (handoff en constructie); publisher opereert aan de publicatiezijde van de value stream.
- Past binnen governance/beleid: publicatie van kennis is in scope en volgt vastgestelde doctrine.

Overlaps en aanbevelingen
- Mogelijke raakvlakken met build/pipeline-executor: publishing-stap integreren als afzonderlijke taak na rendering.
- Aanbevolen: expliciete design-tokens en templating-contract van Presentatie-Architect als bron; publisher consumeert, niet ontwerpt.
- Traceerbaarheid: versiebeheer van gegenereerde artefacten (HTML/PDF) en bronverwijzing naar design-assets.

Referentie naar criteria (nummering, positionering, canon)
- Nummering/positionering: onder "kennispublicatie" in de canon-structuur; volgt vaste map- en naamconventie.
- Canon-consistentie: houdt publicatie objectief en reproduceerbaar, zonder interpretatieve vormgeving.

Documentatie
- Zie docs/resultaten/moeder/agent-boundary-agent-curator.md voor volledige criteria en werkwijze.
