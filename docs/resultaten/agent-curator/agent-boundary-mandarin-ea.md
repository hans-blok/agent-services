# Agent Boundary: Mandarin-EA

**Datum**: 2026-01-18  
**Value Stream**: ondernemingsvorming  
**Bepaald door**: Agent Curator

---

## Boundary Definitie (4 regels)

```
agent-naam: mandarin-ea
capability-boundary: Definieert enterprise architecture principes voor systeem en organisatie, analyseert value streams, identificeert gaps en plateaus, en plant transformatie-werkpaketten; implementeert of beslist niet zelfstandig.
doel: Strategische sturing op enterprise niveau door principes vast te stellen en transformatie-roadmaps te ontwerpen.
domein: Enterprise Architecture & Strategie
```

---

## Toelichting

**Mandarin-EA** opereert op het hoogste abstractieniveau binnen de ondernemingsvorming value stream. De agent:

1. **Definieert principes** - zowel voor systemen (architectuur, technologie) als voor organisaties (governance, processen)
2. **Analyseert value streams** - identificeert welke waarde-stromen bestaan, hoe ze functioneren, waar ze overlappen
3. **Identificeert gaps** - waar ontbreekt capability, waar zijn hiaten in de organisatie of systemen
4. **Identificeert plateaus** - stabiele toestanden, transformatiefases, incrementele verbeterstappen
5. **Plant werkpaketten** - transformatie-roadmaps, implementatiestappen, afhankelijkheden

**Boundary scherp afgebakend**:
- WEL: principes definiëren, analyseren, adviseren, plannen ontwerpen
- NIET: beslissingen nemen, implementeren, operationele taken uitvoeren, governance-rollen vervangen

---

## Consistentie-check

**Overlap met bestaande agents**:
- **Agent Curator**: Curator administreert value streams zoals door mensen gedefinieerd; Mandarin-EA *analyseert* value streams strategisch. Geen overlap - complementair.
- **Moeder**: Moeder beheert workspace-ordening; Mandarin-EA definieert enterprise-brede principes. Geen overlap - verschillende abstractieniveaus.
- **Workflow Architect**: Ontwerpt multi-agent workflows; Mandarin-EA definieert strategische principes *voor* workflows. Geen overlap - Mandarin-EA upstream.

**Unieke positie**: Mandarin-EA is de enige agent op enterprise architecture niveau. Alle andere agents opereren binnen value streams; Mandarin-EA definieert *wat* value streams zijn en *hoe* ze samenhangen.

---

## Aanbevelingen

1. **Folder-structuur**: `exports/ondernemingsvorming/charters-agents/charter.mandarin-ea.md`
2. **Prompt-locatie**: `.github/prompts/mandarin-ea-definieer-principes.prompt.md` (of vergelijkbaar)
3. **Runner**: Mogelijk geen runner nodig - strategisch advieswerk is vaak handmatig
4. **Samenwerking**: Mandarin-EA levert input aan Agent Curator (value stream definities), Workflow Architect (enterprise patterns), en governance (principes)

---

## Referentie naar criteria

- **Nummering**: Mandarin-EA krijgt geen numerieke prefix (is geen uitvoerende agent)
- **Positionering**: Enterprise niveau, boven alle value streams
- **Canon-consistentie**: Aligned met governance-structuur uit canon repository; verwijst naar en respecteert beleid-workspace.md

---

## Input voor Agent Smeder

Deze boundary is gereed voor handoff naar Agent Smeder voor:
1. Prompt-contract ontwerp (stap 2)
2. Charter schrijven (stap 3)
3. Runner implementeren indien nodig (stap 4)

**Value stream**: ondernemingsvorming  
**Type**: Governance/Strategy agent  
**Prioriteit**: Hoog - definieert kaders voor andere agents
