# Dry Rot Knowledge Graph — Status Report, April 9, 2026

## Research Question

When did *Serpula lacrymans* (dry rot) arrive in Britain, and what role did it play in the Royal Navy's catastrophic timber decay during the Napoleonic Wars? The 1823 *Encyclopedia Britannica* claims the disease was known "at some period... of Sir John Pringle's presidency of the Royal Society" (1772-1778). The naval crisis of 1810-1820 produced a wave of "dry rot" literature blaming a single disease for the decay of warships built with American and Canadian timber. We set out to test whether one organism could account for the crisis, or whether — as Sowerby's 1812 inspection of HMS Queen Charlotte suggested — "dry rot" was actually a multi-organism syndrome misdiagnosed by laypeople.

## What's New Since April 3

The April 3 report covered the Phil Trans archive search, the Pepys baseline, the term's etymology (Gray 1725 for cordage, House of Commons 1774 for timber), Hartley's 1776 wainscot puzzle, the Society of Arts gold medal, and Withering/Sowerby's botanical identification of *Boletus lachrymans*. Since then, we have:

1. **Read the Sowerby NHM archive in full** (B95-B98, 442 pages of correspondence, field notes, drafts, and fair copies)
2. **Identified the modern taxonomy** of Sowerby's *Boletus hybridus* as *Fibroporia vaillantii* (DC.) Parmasto 1968 — confirmed against GBIF, MycoDB, Index Fungorum, MycoBank, and Petersen 1983
3. **Built a stratified three-organism model** of ship decay, with humidity zones and timber substrates
4. **OCR'd and read seven contemporary dry rot books** (Johnson 1795, Papworth 1803, Randall 1807, Pering 1812, Blackburn 1817, Lingard 1819, Knowles 1821)
5. **Found NAUTICUS 1811** — the original source for Britton's "orange and brown inverted cones" Woolwich description
6. **Documented 18 timber species** used in Royal Navy ships, including the Canadian and American softwoods that drove the crisis

## Methods

### Knowledge graph as primary research tool

Every significant finding becomes a node or edge in `dry-rot-knowledge-graph.json` (now 204 KB). The graph contains:

- 43 people, 63 sources, 25 events, 18 timber types
- 3 fungal organisms mapped to ecological niches within a ship
- 18 timber types with origins, uses, and durability data
- 60+ explicit relationships, plus ~150 embedded edges (people→sources, events→sources, zones→fungi)
- 18 open research questions, with status tracking as evidence accumulates

Plain-English description of new findings is converted to structured KG entries by Claude Code, which also maintains a vis.js timeline visualization regenerated from the JSON.

### OCR pipeline for primary sources

PDFs from Internet Archive processed through OLMoCR on the Nibi cluster (H100 GPUs). Output: clean markdown that retains page structure and footnotes. Total OCR'd this session: ~1.1 MB across 7 books, plus 442 pages of NHM Sowerby manuscripts (transcribed separately).

### Multi-witness corroboration

For each key claim, we search for independent confirmation across sources written by people with different expertise:
- **Mycologists** (Sowerby, Withering, Petersen) — species identification
- **Architects** (Johnson, Papworth, Randall) — building decay
- **Dockyard officers** (Pering, NAUTICUS) — ship decay observations
- **Naval administrators** (Knowles) — institutional records and ecology
- **Modern science** (Kauserud, Haas, Watkinson) — phylogeography and ecology

A claim that survives in three independent traditions is treated as confirmed.

### Wikidata MCP for taxonomy

When taxonomic questions arise, the Wikidata MCP server provides authoritative species identifications, synonym chains, and modern classifications. The B. hybridus = F. vaillantii identification rests on the nomenclatural databases as accessed through this server.

## Major Findings

### 1. The three-organism stratified model

Naval "dry rot" was not one disease but a syndrome caused by at least three fungi occupying different ecological niches within a single ship:

| Zone | Humidity | Timber | Primary Fungus |
|------|----------|--------|----------------|
| Hold / below waterline | 828-900° | Oak frames, keelson | **Xylostroma giganteum** (oak-specific) |
| Between decks (damp, not wet) | 700-800° | Pitch pine ceiling planks, deal decking | **Boletus lachrymans / Serpula lacrymans** + **B. hybridus / Fibroporia vaillantii** (both conifer specialists) |
| Upper works (ventilated) | 400-600° | Oak hull planking | No significant fungal growth |

The humidity ranges are from Sowerby's own 1812 hygrometer scale (1000° = saturation). The timber zones come from Knowles 1821 Chapter IX. The fungal placements are from Sowerby's 1812 dockyard survey and Knowles's independent ecological observations.

### 2. The B. hybridus taxonomy is resolved

Sowerby's *Boletus hybridus* (EF Tab. 289) = *Fibroporia vaillantii* (DC.) Parmasto 1968. The transfer chain is:

> *Boletus hybridus* Sowerby (c. 1803) → *Polyporus hybridus* (Berkeley & Broome, c. 1860) → *Poria hybrida* (Cooke, 1886) → heterotypic synonym of *Fibroporia vaillantii*

This is a brown-rot polypore in order **Polyporales**, taxonomically remote from *Serpula lacrymans* (order Boletales). The previous KG suggestion of *Donkioporia expansa* was incorrect — D. expansa has a separate basionym (*Boletus expansus* Desm. 1823) and was never connected to *B. hybridus*.

The substrate paradox (F. vaillantii is a conifer specialist, but the QC was nominally an oak ship) is resolved by recognizing that the QC used pine for between-decks components — exactly where Sowerby found B. hybridus.

### 3. Serpula was real on ships, but its presence was concealed by the inspection timing

Four independent witnesses confirm *Serpula lacrymans* on warships:

- **NAUTICUS (1811)**: "the orange and brown coloured fungi were hanging in the shape of inverted cones from deck to deck" at Woolwich c.1798. The colour ("orange and brown") and form ("inverted cones") are diagnostic for Serpula fruiting bodies.
- **Knowles (1812 letter, B95)**: "Many ships that have been constructed of English Oak only, have also been destroyed by Boletus lachrymans"
- **Knowles (1821, Chapter VIII)**: "the *Boletus lachrymans* spreads with a wonderful rapidity, and by taking root on the timber, or insinuating itself into the fissures, like a parasite, soon destroys the parent"
- **Pering (1812)**: distinguishes "fungus" from "dry rot" as different phenomena — fungus needs sustained moisture, dry rot spreads in drier conditions and is contagious

But Sowerby found "very little remains of Boletus Lachrymans" on the QC in July 1812. Why? **The most damaged timber had already been removed before he arrived.** The between-decks pine — where B. lachrymans would have been most prevalent — was the most accessible area and was stripped first. Knowles tells us the QC required "all the planking both within and without board, together with many of the timbers and beams to be removed... from the topside to the gun-deck clamps." Sowerby inspected what was left: the oak frame deeper in the ship, in the saturated hold, where Xylostroma and B. hybridus were still growing in conditions too wet for Serpula to favour.

Sowerby was not wrong. He accurately documented what was present at the moment of inspection. But his "very little" applies to a stripped ship, not to the QC's original infestation.

### 4. The Canadian timber connection

HMS Queen Charlotte was built with **Canada oak** and **American pitch pine** (Knowles 1821 p.117). Both were notoriously vulnerable. The keel was laid October 1805, frame completed December 1806, launched May 1810 — built during the timber crisis after Trafalgar created urgent demand and the Berlin/Milan decrees (1807) cut off Baltic timber supplies. The QC was literally built from the crisis.

Knowles documents the durability disaster of Canadian softwoods:
- **Canadian white pine** (= yellow pine, *Pinus strobus*): 3 frigates built 1814-1815, average durability **less than 3 years**
- **Canadian red pine** (*Pinus resinosa*): 15 frigates built 1814-1815, average **3.5 years**
- **American pitch pine** (Carolina/Georgia): 7 frigates built 1813-1814, average **6.5 years**
- **Canadian white oak** (*Quercus alba*): "would not last for more than five years"
- **English oak**: potentially **century-long** durability when properly seasoned

The Royal William lasted 94 years (mostly in harbour). The Devonshire (1812), built of "the best kind of American white oak that could be procured," was totally decayed in February 1817 — without ever going to sea.

### 5. The building crisis was a decade ahead of the naval crisis in understanding

By 1803, Papworth had described *Serpula lacrymans* behaviour with precision — penetration through brick walls, varying morphology with humidity, parasitical spreading, and water droplets — without knowing the species name. He conducted experiments on fungal propagation. By 1807, Randall had documented fir as preferentially attacked over oak, and reported the dry rot in the Bank of England dome, the Adelphi (Society of Arts headquarters), the Pantheon in Paris, and Mr. Batson's house in London. The building authors (Johnson 1795, Papworth 1803, Randall 1807) describe Serpula clearly without using the binomial — they're seeing the same organism Sowerby would later identify on ships.

The naval crisis broke later because:
- Ships used a different (worse) substrate mix (Canadian pine and oak)
- Dockyard observation lacked mycological training
- The Navy Board had been trying chemical solutions for 70+ years (Reed's tar acid 1740, Jackson's salt 1767-1773, White's lime 1798, charring 1808)
- Lukin's stove-heating method (1808-1812) actively created conditions for fungal growth

When Sowerby was finally called in July 1812, he brought building-mycology expertise to a problem the navy had been trying to solve as a chemical engineering challenge.

### 6. The "dry rot" terminology was deliberately misapplied

Knowles, the Secretary to the Committee of Surveyors, explicitly admits in 1821 (p.110): "since the defective state of the Queen Charlotte was discovered in 1811, and this term applied to her defects, it has become a favourite name, and been given indiscriminately to almost every description of rot, **whether fungus was or was not present**. By the terms being thus confounded, the cause of the decay of ships cannot be accurately ascertained from official reports, but only by actual inspection."

This is the key admission. The "dry rot crisis" of 1810-1820 in the Royal Navy was, in significant part, a terminological crisis: a building-disease term applied to all manner of timber failures, regardless of whether *Serpula lacrymans* was actually present. Some failures were genuine Serpula infections; others were Xylostroma on saturated oak; others were B. hybridus / F. vaillantii on pine; others were simply unseasoned timber rotting from within. The single "dry rot" label obscured the biological diversity of what was happening.

### 7. Every chemical preservation method failed

Knowles Chapter IV is a graveyard of failed experiments spanning 80 years:
- **Reed's tar acid** (1740): no perceptible effect after 5 years; iron nails corroded
- **Jackson's salt/lime/copperas process** (1767-1773): 9 ships of the line + many frigates treated; less durable than untreated; deliquescent salts caused constant damp; workers complained of poisoning
- **White's lime seasoning** (Amethyst 1798): timbers rent in lime pit; more defective than untreated when examined 1809
- **Charring** (Dauntless 1808): "some of the timbers and plank which had been charred were in a state of decomposition, with fungus growing upon them" by 1814
- **Train oil** (Fame): only the parts the oil penetrated were sound, and oil only penetrated 12-18 inches
- **Lukin's seasoning house** (1812): elaborate gas chamber with retorts, hygrometers, gasometers — failed
- **Mineral tar** (Mr. Bill, 1820): experiments still ongoing as of publication

This explains why Sowerby's environmental approach (ventilation, hygrometer monitoring, no chemicals) was such a breakthrough. Every chemical alternative had been tried and discarded. The Navy had nothing left to try.

### 8. The credit dispute and the institutional dynamics

Sowerby was awarded 200 guineas in January 1814, but the Navy Board explicitly denied him credit for saving the QC: "we do not attach to you the merit of having saved the Queen Charlotte by your advice, all the defective materials having been taken out of that Ship at Plymouth when she was repaired there." Sowerby insisted the ship was "providentially saved by my directions."

The B95 correspondence reveals the institutional dynamics: Knowles initiated the commission against Lukin's preferred approach; the Admiralty overrode Lukin's stove-heating method ("repairs shall be proceeded with according to your suggestions without further reference to Mr Lukin's reports"); the Board credited Sowerby for the generalizable contribution (timber seasoning) while denying credit for the specific ship. By 1817, Seppings was inviting Sowerby for private advice "up the private stairs" but not paying — Sowerby refused, having submitted his expenses twice unpaid.

The pattern: the institution absorbed the expert's contribution while managing the credit attribution to protect existing hierarchies.

## The Knowledge Graph Today

```
metadata        — hypothesis, sources, dates
organisms       — Serpula lacrymans + native brown rot group (with F. vaillantii synonyms, Wikidata QIDs)
ship_decay_ecology
  ├── 3 humidity zones with primary fungi
  ├── 18 timber types with origins and durability data
  ├── full dockyard species list (~25 species from B98 p.25)
  ├── humidity-fungi correlation scale
  └── implications
terminology     — 9 terms with earliest documented uses
people          — 43 historical figures (Wikidata QIDs where available)
sources         — 63 primary and secondary sources, many with full OCR analysis
events          — 25 dated events 1684-1821
conceptual_frameworks — 3 competing theories (miasmatic, antiseptic, worm damage)
relationships   — 60+ explicit edges, ~150 total counting embedded references
modern_scholarship — 4 modern secondary sources
open_questions  — 18 research questions with status tracking
```

File size: 204 KB. Validated as well-formed JSON after every edit.

## Open Questions Still to Answer

The KG tracks 18 research questions. Recent updates:

- **Q12 (B. hybridus modern identity)**: SUBSTANTIALLY ANSWERED — F. vaillantii confirmed by nomenclatural databases
- **Q13 (Sowerby NHM archive contents)**: ANSWERED — fully read and analyzed
- **Q15 (Navy Board credit dispute)**: PARTIALLY ANSWERED — institutional dynamics documented
- **Q16 (NEW)**: Was the QC built of American Timber? — ANSWERED by Knowles p.117: Canada oak + American pitch pine
- **Q17 (NEW)**: What happened to Sowerby's herbarium specimens at the NHM? — UNANSWERED, requires NHM mycology collection inquiry
- **Q18 (NEW)**: What was the fate of HMS Vigo and how did Lukin's heating method cause dry rot? — UNANSWERED, requires further Navy Board records research

Older questions still open:
- Q1: Does "dry-rot" appear in Navy records before 1778?
- Q2: When was the term first used in shipbuilding manuals?
- Q3-Q11: Various sub-questions about the term's spread
- Q14: Was there a connection between Pringle's antiseptic chemistry framework and the early dry rot literature?

## Future Work

### Immediate next steps

1. **Read remaining OCR'd texts**: Lingard 1819 (timber preservation chemistry), Blackburn 1817 (largest book, mostly unread beyond the dry rot chapter), Johnson 1795 (full text), Knowles Chapters V-VII in more detail
2. **Find the European Magazine December 1811** original publication of NAUTICUS — verify the citation chain to Britton 1875
3. **Read Ramsbottom 1937** (*Essex Naturalist* 25: 231-267) — the most important secondary source on naval dry rot, currently uncited
4. **Investigate "Turtosa" / African teak** — the Sierra Leone timber Knowles describes; likely *Oldfieldia africana* but needs confirmation

### Medium-term research directions

1. **Society of Arts archive** — find records of the gold medal prize (1783-1818) and Bowden's 1818 winning paper
2. **NHM Mycology collections** — locate any surviving Sowerby specimens for potential molecular analysis
3. **Navy Board records (ADM series)** — confirm the dates and personnel in the QC repair history; find the fates of HMS Vigo, Foudroyant, and Ajax
4. **Cranfield University HMS Victory PhD (2022)** — follow up on the molecular analysis of historic naval timber that the compass artifact mentioned but had not yet published
5. **Linnean Society Transactions** — Sowerby's 1815 paper on Lycoperdon cancellatum may shed light on his late mycological thinking

### The big unsettled question

**Did Serpula lacrymans actually arrive in Britain in the 18th century, or was it always present at low levels and amplified by changes in construction practice?**

The Kauserud et al. 2007 phylogeography puts the divergence of European populations from Asian wild populations at 2,000-5,000 years ago — much older than the documentary evidence of explosive expansion in the late 1700s. This suggests the organism may have been present in Europe for centuries but became epidemic only when conditions changed:
- More enclosed timber construction
- Less ventilation
- Damp masonry in contact with wood
- The Adelphi-style underground/basement spaces
- The shift from English oak to imported softwoods

The molecular and documentary evidence point to an "amplification" model rather than a "first introduction" model. The 1770s-1810s crisis was real, but it was a population explosion of an organism that had been quietly present.

## Methodological Reflections

This project demonstrates a workflow that didn't exist a year ago: using Claude Code as both research assistant and structured-data manager for a humanities project. Key lessons:

1. **Plain-English research notes become structured data automatically.** The historian describes findings in natural language; Claude Code converts to JSON nodes and edges. No spreadsheet maintenance, no schema design upfront — the structure emerges from the research.

2. **The graph IS the synthesis.** Traditional historical writing treats the synthesis as the output and the notes as input. Here, the KG is the persistent, queryable, version-controlled product. The narrative report (this file) is generated FROM the KG, not the other way around.

3. **OCR + LLM analysis + structured KG is a force multiplier.** A single afternoon working through Knowles 1821 produced Chapter VIII, Chapter IX, the timber types section, and the historical context for the entire 1812 crisis. Reading the same book traditionally would have taken weeks.

4. **Multi-witness corroboration is the key methodological discipline.** It's tempting to treat any LLM-extracted claim as authoritative. The discipline of finding three independent witnesses for any major claim — and tracking which witnesses are independent vs. derivative — is what keeps the analysis honest.

5. **Memory across sessions matters.** The project memory file (`project_dry_rot_kg.md`) is updated after each session and preserves continuity. Without it, each session would start from scratch.

## Date

Status report: 2026-04-09
Previous report: 2026-04-03 (april3.md)
KG last validated: 2026-04-09
