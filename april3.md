# Dry Rot Knowledge Graph — Status Report, April 3, 2026

## Research Question

When did *Serpula lacrymans* (dry rot) arrive in Britain, and how did British science come to recognise it? The 1823 Encyclopedia Britannica claims the disease was known "at some period... of Sir John Pringle's presidency of the Royal Society" (1772-1778). We set out to test this claim against primary sources.

## What We Did

Starting from a semantic vector search of the complete Philosophical Transactions OCR archive (8,128 articles, 1665-1869), we expanded outward through building manuals, parliamentary records, botanical surveys, newspaper archives, French scientific journals, and the Society of Arts premiums — assembling a knowledge graph of every fragment of evidence for the emergence of dry rot in Britain.

## Key Findings

### The term "dry rot"

| Date | Source | Applied to | Significance |
|------|--------|-----------|--------------|
| 1725 | Gray, *Royal Navy suitably manned* | **Cordage** (rope) | Earliest known use — naval stores, not timber |
| 1774 | House of Commons Journals | **Timber** (church) | Earliest confirmed use for timber — "a dry Rot has destroyed the Floors and Pews" |
| 1776 | Hartley, fire-plates pamphlet | **Timber** (buildings) | "Commonly called by the term Dry-Rot" — already established. "We do not know the real cause." |
| 1778 | Mahon, Phil Trans | **Timber** (buildings) | First use in a scientific journal |
| 1778 | Mann, French journal | **Timber** (buildings) | "Ce que les anglois nomment Dry-rot" — term exported to Continent |
| 1785 | *The Times*, Keate v. Adams | **Timber** (buildings) | "The common AND dry rot" — two types distinguished in court. Banks testified. |

### The organism

| Date | Source | Finding |
|------|--------|---------|
| 1708 | Scamozzi/Leyburn, building manual | One mention of "rot" in entire book. No dry rot concept. |
| 1726 | Neve, builder's dictionary | No "dry rot" entry. Same year Gray uses the term for cordage. |
| 1776 | Withering, *Botanical Arrangement* 1st ed. | Comprehensive fungi survey (~80 species). **No *B. lachrymans*.** |
| 1781 | Wulfen (Austria) | *Serpula lacrymans* formally classified |
| 1792 | Withering, 2nd ed. | *B. lachrymans* = "dry-rot" added to British flora |
| 1797 | Sowerby, *Coloured Figures* | "Much too common in England." First British illustration. Explains etymology. |

### The institutional response

| Date | Source | Finding |
|------|--------|---------|
| 1759-1780 | Society of Arts, *Premiums offered* | **No dry rot prize** across 20+ years. Prizes for planting timber but nothing on timber decay. |
| 1781-1782 | Missing volumes | Critical gap — not yet located |
| 1783 | Society of Arts, *Transactions* vol. 3 | **Gold medal** offered for discovering "the cause of the Dry Rot in Timber" |
| 1784-1789 | Society of Arts, *Abstract of Premiums* | Prize re-advertised annually. **Never awarded.** Escalated in 1789. |
| 1785 | *The Times* | Banks (PRS) testifies on dry rot in court — yet no Phil Trans articles on dry rot during his 42-year presidency |

### The baseline: Pepys (1684)

Pepys gathered toadstools "as big as my Fists" from neglected ship holds. The conditions (damp, unventilated, sealed) and the absence of any surprise at the *type* of decay indicate **wet rot from native brown rot fungi** — not *Serpula lacrymans*. The "perished to powder" symptom is shared by multiple native species (*Coniophora puteana*, *Laetiporus sulphureus*, *Donkioporia expansa*, etc.) and is not diagnostic of *Serpula* specifically. The distinguishing feature of *Serpula* is not the symptom (powder) but the **behaviour**: spreading to dry timber via rhizomorphs.

### The Hartley passage (1776)

The single most analytically important source. David Hartley:
- Confirms "Dry-Rot" was **commonly called** by 1776
- Admits **"we do not know the real cause"**
- Notes the **wainscot puzzle**: dry rot in open rooms contradicts the ventilation theory
- Proposes renaming it **"Wet-Rot"** because the cause is moisture

He is observing *Serpula lacrymans* spreading beyond the damp zone — and is baffled by it.

## The Evidence Trajectory

```
1684  Pepys: toadstools in ship holds (WET ROT — native fungi)
1708  Building manuals: rot = moisture. One sentence.
1725  "Dry-Rot" for CORDAGE — naval stores term
1726  Builder's dictionary: no "dry rot" for timber
1742  Ship ventilation: "putrid air" framework
1749  Pringle: antiseptic chemistry dominates decay discourse
1755  Hales: ship timber decay alarming — "putrid corroding air"
1758  Hales: CONNECTS ships and buildings — rot ascending from damp earth
      ---- THE TERM MIGRATES FROM CORDAGE TO TIMBER ----
1774  House of Commons: "a dry Rot" destroys church (EARLIEST TIMBER USE)
1776  Hartley: "commonly called" — cause unknown — wainscot puzzle
1776  Withering 1st ed: comprehensive fungi, NO B. lachrymans
1778  Mahon (Phil Trans) + Mann (French journal): term in print
      ---- THE ORGANISM IS CLASSIFIED ----
1781  Wulfen (Austria): Serpula lacrymans formally classified
1783  Society of Arts: gold medal — cause still unknown
1785  Times: Keate v. Adams lawsuit — Banks testifies
1792  Withering 2nd ed: B. lachrymans = "dry-rot" in British flora
1795  Johnson: first book on dry rot
1797  Sowerby: "Much too common in England" — illustrated
1797  Gentleman's Magazine: public debate on causes
      ---- THE NAVAL CRISIS ----
1798  Woolwich ship: "orange and brown fungi in inverted cones"
1810  HMS Queen Charlotte: new ship riddled with rot
1812-1821  9+ books in 10 years — crisis peak
1823  Encyclopedia Britannica: "not known... beyond the middle of the last century"
```

## Files

| File | Description |
|------|-------------|
| `dry-rot-knowledge-graph.json` | Structured KG: 51 sources, 25 people, 14 events, 5 fungi, 3 rot types, 12 open questions |
| `dry-rot-phil-trans-report.md` | Narrative research report with full evidence analysis |
| `dry-rot-timeline.html` | Interactive vis.js temporal network visualization |
| `generate_dry_rot_timeline.py` | Generates the HTML from the JSON |
| `dryrot_sources/` | 7 PDFs downloaded from Internet Archive |

## Sources Consulted

### Primary sources read in detail
- Pepys, *Memoires Relating to the State of the Royal Navy* (1690) — full text via PDF
- Philosophical Transactions of the Royal Society (1665-1869) — via SQLite/FTS + vector search
- Withering, *Botanical Arrangement* 1st ed. (1776) and 2nd ed. (1792) — fungi sections
- Sowerby, *Coloured Figures of English Fungi* (1797) — Tabs. CXIII, CCLXXXIX, CCCCIII
- Hartley, *Fire-plates* (1776) — dry rot passage
- Mahon, Phil Trans (1778) — dry rot passage
- Mann, *Observations sur la Physique* (1778) — dry rot passage
- *The Times* (Dec 1785) — Keate v. Adams trial, Banks testimony
- House of Commons Journals (1774) — dry rot in church
- Society of Arts, *Transactions* vol. 3 (1783) and *Premiums offered* (1758-1789)
- Scamozzi/Leyburn (1708) and Neve (1726) — building manuals
- Gray (1725) — naval cordage
- Britton, *Treatise on Dry Rot* (1875) — secondary source, used with caution
- Encyclopedia Britannica (1823) — dry rot article

### Downloaded but not yet read
- Johnson (1795), Papworth (1803), Randall (1807), Pering (1812), Blackburn (1817), Lingard (1819), Knowles (1821)

## Open Questions

1. Does "dry rot" appear in Admiralty records before 1774?
2. Can the 1781-1782 Society of Arts premium volumes be located?
3. What does the OED say for earliest use of "dry rot"?
4. Can the European Magazine (Dec 1811) Woolwich ship article be verified?
5. What is the original source for Banks's wine cask anecdote?
6. Did Hartley publish anything else on dry rot?
7. Was the Society of Arts gold medal ever awarded?
8. Can we identify the specific fungi Britton distinguishes as *Polyporus hybridus* (ships) vs *Merulius lachrymans* (buildings)?
9. What is the relationship between the building construction boom and *Serpula* spread?
10. What are the earliest uses in the Times Digital Archive before 1785?

## Hypothesis Status

**Supported with modifications.** The evidence is consistent with *Serpula lacrymans* arriving and spreading aggressively in Britain during the second half of the 18th century:

- **Before 1750**: No concept of "dry rot" in timber. Building manuals know only moisture rot. Pepys's 1684 decay is wet rot from neglect.
- **1750-1774**: Something changes. Hales (1755, 1758) notes worsening harbour ship decay and connects it to buildings. The term "dry rot" migrates from cordage to timber.
- **1774-1783**: The disease is named, debated, and institutionally recognised. Hartley (1776) observes the wainscot puzzle — decay in dry conditions. The Society of Arts offers its gold medal.
- **1781-1797**: The organism is classified (Wulfen), added to British flora (Withering), and illustrated as "much too common in England" (Sowerby).
- **1798-1823**: The naval crisis. Ships condemned after 3-5 years. 9+ books published. The problem becomes a matter of national security.

The modification: Kauserud et al. (2007) suggest the divergence between Asian wild and European domestic strains is **2,000-5,000 years old** — much older than the 18th-century crisis. The organism may have been present in Europe for centuries at low levels. What changed in the 18th century was not necessarily the organism's arrival but the **conditions**: more enclosed timber construction, less ventilation, damp masonry in contact with wood. The building boom created ideal *Serpula* habitat. The crisis was an ecological explosion enabled by architectural change.

## Methods

- **Phil Trans search**: SQLite FTS5 + NV-Embed-v2 vector search (4096-dim HNSW) via Modal GraphRAG endpoint
- **Primary source reading**: PDFs via Claude Code multimodal (Pepys, Withering, Sowerby, building manuals)
- **Database searches**: ECCO (Eighteenth Century Collections Online), Times Digital Archive, Internet Archive API, Nineteenth Century Collections Online
- **OLMoCR**: Society of Arts *Premiums* series (1758-1789) processed on Nibi cluster
- **Phylogeographic context**: Kauserud et al. (2007), *Molecular Ecology* 16(16): 3350-3360

## Next Steps

1. **OCR the Society of Arts Premiums** — the full 1758-1783 series as a database of 18th-century institutional priorities
2. **Read the downloaded crisis literature** — especially Johnson 1795 (earliest book) and Pering 1812 (naval crisis)
3. **Check the OED** — may have earlier citations
4. **Search Admiralty records** (National Archives ADM series) for pre-1774 uses
5. **Locate the 1781-1782 Premiums volumes** — critical gap
6. **Verify Britton's claims** against underlying primary sources (European Magazine 1811, Banks anecdote)
7. **Expand the knowledge graph** to include the Adelphi/Adam brothers thread more fully
