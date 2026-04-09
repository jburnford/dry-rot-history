"""Generate a temporal network visualization of the dry rot knowledge graph."""

import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('dry-rot-knowledge-graph.json', 'r') as f:
    kg = json.load(f)

# Define key years and what happens in each
year_events = {}

# Extract years from sources
for src in kg.get('sources', []):
    year = src.get('year')
    if year and isinstance(year, int) and 1660 <= year <= 1880:
        if year not in year_events:
            year_events[year] = []
        year_events[year].append({
            'id': src['id'],
            'label': src.get('title', '')[:60],
            'type': 'source',
            'authors': src.get('authors', []),
            'context': src.get('context', ''),
            'relevance': src.get('relevance', ''),
        })

# Extract years from events (check year, start_year, end_year)
for evt in kg.get('events', []):
    year = evt.get('year') or evt.get('start_year') or evt.get('end_year')
    if year and isinstance(year, int) and 1660 <= year <= 1880:
        if year not in year_events:
            year_events[year] = []
        year_events[year].append({
            'id': evt['id'],
            'label': evt.get('description', '')[:60],
            'type': 'event',
        })

# Select which years to show (only years with evidence, plus key milestones)
all_years = sorted(year_events.keys())
# Add some gap years for context
display_years = sorted(set(all_years))

# Color scheme
COLORS = {
    'year': {'bg': '#2d3748', 'border': '#4a5568'},
    'person': '#76B7B2',
    'person_key': '#E15759',
    'source_phil_trans': '#4E79A7',
    'source_building': '#F28E2B',
    'source_naval': '#59A14F',
    'source_botanical': '#EDC948',
    'source_legal': '#B07AA1',
    'source_encyclopedia': '#AF7AC5',
    'source_other': '#9C755F',
    'event': '#FF9DA7',
    'organism': '#BAB0AC',
    'negative': '#666666',
}

def source_color(src):
    ctx = src.get('context', '')
    rel = src.get('relevance', '')
    sid = src.get('id', '')
    if rel == 'negative_evidence':
        return COLORS['negative']
    if 'britannica' in sid or src.get('evidence_type') == 'encyclopedia_entry':
        return COLORS['source_encyclopedia']
    if 'phil_trans' in sid or 'Phil Trans' in src.get('title', '') or (src.get('identifier') or '').startswith('jstor-'):
        return COLORS['source_phil_trans']
    if 'navy' in ctx or 'naval' in ctx:
        return COLORS['source_naval']
    if 'building' in ctx or 'legal' in ctx:
        return COLORS['source_building']
    if 'botan' in ctx or 'mycol' in ctx:
        return COLORS['source_botanical']
    return COLORS['source_other']

# Build nodes
nodes = []
edges = []
node_ids = set()

# Year nodes along timeline
x_spacing = 90
year_x = {}
for i, year in enumerate(display_years):
    x = i * x_spacing
    year_x[year] = x
    nodes.append({
        'id': f'year_{year}',
        'label': str(year),
        'x': x,
        'y': 0,
        'fixed': {'x': True, 'y': True},
        'shape': 'box',
        'color': {'background': COLORS['year']['bg'], 'border': COLORS['year']['border'],
                  'highlight': {'background': '#4a5568', 'border': '#718096'}},
        'font': {'color': '#e2e8f0', 'size': 12, 'face': 'monospace'},
        'nodeType': 'year',
        'size': 20,
        'mass': 10,
    })
    node_ids.add(f'year_{year}')

# === Rot type and fungi nodes (positioned ABOVE the timeline) ===
rot_types = [
    {
        'id': 'rot_brown',
        'label': 'BROWN ROT',
        'title': 'Brown cubical rot\nDigests cellulose, leaves lignin.\nWood shrinks, cracks into cubes, crumbles to powder.\nCaused by multiple fungi — symptom shared by wet rot AND dry rot.',
        'color': '#8B4513',
        'y': -200,
        'x': year_x.get(1750, 500),
    },
    {
        'id': 'rot_wet',
        'label': 'WET ROT',
        'title': 'Requires sustained high moisture.\nStops when wood dries out.\nCannot spread to dry timber.\nCaused by native European fungi.\nPepys\'s toadstools (1684) = wet rot.',
        'color': '#2E86C1',
        'y': -300,
        'x': year_x.get(1720, 300),
    },
    {
        'id': 'rot_dry',
        'label': 'DRY ROT',
        'title': 'Serpula lacrymans.\nSpreads via rhizomorphs to DRY timber.\nCrosses masonry, brick, dry gaps.\nAttacks timber that appears dry.\nName describes the paradox: rot where there shouldn\'t be rot.',
        'color': '#C0392B',
        'y': -300,
        'x': year_x.get(1790, 800),
    },
]

for rt in rot_types:
    nodes.append({
        'id': rt['id'],
        'label': rt['label'],
        'x': rt['x'],
        'y': rt['y'],
        'fixed': {'x': False, 'y': False},
        'shape': 'hexagon',
        'color': {'background': rt['color'], 'border': rt['color'],
                  'highlight': {'background': '#fff', 'border': rt['color']}},
        'font': {'color': '#ffffff', 'size': 11, 'bold': True},
        'nodeType': 'rot_type',
        'size': 22,
        'mass': 15,
        'title': rt['title'],
    })
    node_ids.add(rt['id'])

# Brown rot is parent of both wet and dry
edges.append({'from': 'rot_brown', 'to': 'rot_wet', 'color': {'color': 'rgba(139,69,19,0.5)'}, 'width': 3, 'title': 'Wet rot is a type of brown rot', 'length': 150})
edges.append({'from': 'rot_brown', 'to': 'rot_dry', 'color': {'color': 'rgba(139,69,19,0.5)'}, 'width': 3, 'title': 'Dry rot is a type of brown rot', 'length': 150})

# === Institution nodes (positioned BELOW the timeline) ===
INST_COLOR = '#6C5B7B'
institutions = [
    {
        'id': 'inst_navy_board',
        'label': 'NAVY BOARD',
        'title': 'Board of Commissioners of the Navy.\nManaged dockyards, ship construction, timber supply.\nCommissioned Sowerby (1812). Adopted his recommendations fleet-wide.\nKey figures: Hartwell, Legge, Thompson, Rule, Seppings, Byam Martin.',
        'color': '#2C6E49',
        'y': 500,
        'x': year_x.get(1800, 700),
    },
    {
        'id': 'inst_admiralty',
        'label': 'ADMIRALTY',
        'title': 'Lords Commissioners of the Admiralty.\nPolitical leadership of the Royal Navy.\nSt Vincent as First Lord (1801-04) caused the green timber crisis.\nApproved Sowerby\'s fleet-wide recommendations (Aug 1812).',
        'color': '#1B4332',
        'y': 600,
        'x': year_x.get(1805, 750),
    },
    {
        'id': 'inst_royal_society',
        'label': 'ROYAL SOCIETY',
        'title': 'Royal Society of London.\nPhilosophical Transactions = primary scientific journal.\nPresidents: Pepys (1684-86), Pringle (1772-78), Banks (1778-1820).\nNo Phil Trans articles on dry rot during Banks\'s 42-year presidency\ndespite his courtroom testimony on the subject (1785).',
        'color': '#4A4E69',
        'y': 500,
        'x': year_x.get(1750, 400),
    },
    {
        'id': 'inst_society_arts',
        'label': 'SOCIETY OF ARTS',
        'title': 'Society for the Encouragement of Arts, Manufactures, and Commerce.\nHoused in the Adelphi (Adam brothers\' building).\nOffered gold medal for discovering cause of dry rot (1783-1789+).\nNever awarded. No dry rot prize in 20+ years of premiums before 1783.',
        'color': '#7B2D8E',
        'y': 600,
        'x': year_x.get(1780, 550),
    },
    {
        'id': 'inst_parliament',
        'label': 'PARLIAMENT',
        'title': 'Houses of Parliament.\nHouse of Commons: earliest "dry Rot" for timber (1774).\nHouse of Lords: Select Committee on Timber Trade (1820).\nTimber supply inquiries: 1771, 1783 (Middleton), 1808, 1820.',
        'color': '#8B6914',
        'y': 500,
        'x': year_x.get(1774, 350),
    },
]

for inst in institutions:
    nodes.append({
        'id': inst['id'],
        'label': inst['label'],
        'x': inst['x'],
        'y': inst['y'],
        'fixed': {'x': False, 'y': False},
        'shape': 'box',
        'color': {'background': inst['color'], 'border': inst['color'],
                  'highlight': {'background': '#fff', 'border': inst['color']}},
        'font': {'color': '#ffffff', 'size': 10, 'bold': True},
        'nodeType': 'institution',
        'size': 25,
        'mass': 8,
        'title': inst['title'],
    })
    node_ids.add(inst['id'])

# (Person/Event → Institution edges are deferred to after all nodes are added — see below)

# Fungi nodes
fungi_nodes = [
    # Wet rot fungi (native)
    {'id': 'fun_coniophora', 'label': 'Coniophora\nputeana', 'parent': 'rot_wet',
     'title': 'Cellar fungus. Most common wet rot in European buildings.\nAlso in forests on dead wood.\nDark brown cubical rot — dried wood crumbles to powder.',
     'color': '#3498DB'},
    {'id': 'fun_donkioporia', 'label': 'Donkioporia\nexpansa', 'parent': 'rot_wet',
     'title': 'Oak mazegill. Major wet rot of oak structural timber.\nProduces bracket-like fruiting bodies.',
     'color': '#3498DB'},
    {'id': 'fun_laetiporus', 'label': 'Laetiporus\nsulphureus', 'parent': 'rot_wet',
     'title': 'Chicken of the woods. Common on living/dead oaks.\nSevere brown cubical rot of heartwood.',
     'color': '#3498DB'},
    {'id': 'fun_fibroporia', 'label': 'Fibroporia\nvaillantii', 'parent': 'rot_wet',
     'title': 'Mine fungus / White pore fungus.\nNative to European pine forests.\nRapid brown cubical rot in damp environments.',
     'color': '#3498DB'},
    # Dry rot fungus
    {'id': 'fun_serpula', 'label': 'Serpula\nlacrymans', 'parent': 'rot_dry',
     'title': 'THE dry rot fungus. Himalayan origin.\nSpreads via rhizomorphs. Transports water to dry timber.\nClassified by Wulfen 1781. "Much too common in England" by 1797 (Sowerby).\nOrange-brown fruiting body with water droplets (lachrymans = weeping).',
     'color': '#E74C3C'},
]

for fn in fungi_nodes:
    nodes.append({
        'id': fn['id'],
        'label': fn['label'],
        'shape': 'ellipse',
        'color': {'background': fn['color'], 'border': fn['color'],
                  'highlight': {'background': '#fff', 'border': fn['color']}},
        'font': {'color': '#ffffff', 'size': 8, 'face': 'monospace'},
        'nodeType': 'fungus',
        'size': 14,
        'mass': 10,
        'title': fn['title'],
    })
    node_ids.add(fn['id'])
    # Edge to parent rot type
    edges.append({
        'from': fn['id'],
        'to': fn['parent'],
        'color': {'color': 'rgba(255,255,255,0.3)'},
        'width': 1.5,
        'title': f"Causes {fn['parent'].replace('rot_','')} rot",
    })

# Connect rot_dry to people who named/described it
rot_dry_people = [
    ('per_hartley', '"Commonly called by the term Dry-Rot" (1776)\nAdmitted cause unknown. Wainscot puzzle.'),
    ('per_mahon', 'First Phil Trans use of "dry-rot" (1778)\nFireproofing context.'),
    ('per_mann', 'Introduced term to French audience (1778)\n"ce que les anglois nomment Dry-rot"'),
]
for pid, note in rot_dry_people:
    edges.append({
        'from': pid, 'to': 'rot_dry',
        'color': {'color': 'rgba(192,57,43,0.5)'},
        'width': 2,
        'title': note,
        'arrows': {'to': {'enabled': True, 'scaleFactor': 0.5}},
    })

# Connect Serpula to Wulfen and Sowerby
edges.append({'from': 'per_wulfen', 'to': 'fun_serpula', 'color': {'color': 'rgba(237,201,72,0.7)'}, 'width': 3, 'title': 'Classified 1781', 'arrows': {'to': {'enabled': True, 'scaleFactor': 0.6}}})
edges.append({'from': 'per_sowerby', 'to': 'fun_serpula', 'color': {'color': 'rgba(237,201,72,0.7)'}, 'width': 3, 'title': 'Illustrated as "Common Dry-rot" 1797.\nFound "very little" on HMS Queen Charlotte 1812.\nThe building dry rot ≠ the ship dry rot.', 'arrows': {'to': {'enabled': True, 'scaleFactor': 0.6}}})
edges.append({'from': 'per_withering', 'to': 'fun_serpula', 'color': {'color': 'rgba(237,201,72,0.5)'}, 'width': 2, 'title': 'Added to British flora 1792', 'arrows': {'to': {'enabled': True, 'scaleFactor': 0.6}}})

# === Speculative edges: decay events to rot types and fungi ===
# Direction: Event --> Rot Type (what caused it) and Event --> Fungus (which organism)
# Certainty: definitive, high, medium, low
speculative_edges = [
    # === 1680s NAVAL CRISIS ===
    # Pepys toadstools — wet rot
    {'from': 'evt_pepys_toadstools', 'to': 'rot_wet', 'certainty': 'high',
     'title': 'HIGH: Wet rot.\nToadstools in damp, unventilated holds.\nSustained moisture conditions.\nNo Serpula behaviour described.'},
    {'from': 'evt_pepys_toadstools', 'to': 'fun_coniophora', 'certainty': 'medium',
     'title': 'MEDIUM: Coniophora puteana (cellar fungus)\nmost likely candidate for damp ship holds.\nProduces brown cubical rot and powder.'},
    {'from': 'evt_pepys_toadstools', 'to': 'fun_donkioporia', 'certainty': 'medium',
     'title': 'MEDIUM: Donkioporia expansa (oak mazegill)\npossible — attacks oak structural timber.\nCould produce large fruiting bodies.'},
    {'from': 'evt_pepys_toadstools', 'to': 'rot_dry', 'certainty': 'low',
     'title': 'LOW: No strong evidence Serpula was present.\nBut cannot be ruled out — absence of evidence\nis not evidence of absence.\nConditions described fit wet rot;\nno spreading-to-dry-timber behaviour observed.'},
    # 30 ships crisis — wet rot from neglect
    {'from': 'evt_30_ships_crisis', 'to': 'rot_wet', 'certainty': 'medium',
     'title': 'MEDIUM: Wet rot from neglect.\nShips never cleaned, aired, heeled, or breemed.\nPepys attributes entirely to omission of maintenance.\nNo novel organism suspected.'},

    # === 1755 HARBOUR SHIP DECAY ===
    {'from': 'evt_hales_alarm', 'to': 'rot_wet', 'certainty': 'medium',
     'title': 'MEDIUM: Hales attributes to "putrid corroding air".\nConsistent with wet rot.\nBut the WORSENING problem could indicate\nearly Serpula spread in dockyards.'},
    {'from': 'evt_hales_alarm', 'to': 'rot_dry', 'certainty': 'low',
     'title': 'LOW: Could be early Serpula —\nHales notes harbour ship decay as newly alarming.\nBut could equally be another brown rot.\nHis explanation ("putrid corroding air") is\ncompatible with either.'},

    # === 1780s BUILDING CRISIS ===
    # Keate v Adams — dry rot in new building
    {'from': 'evt_keate_v_adams', 'to': 'rot_dry', 'certainty': 'high',
     'title': 'HIGH: Dry rot (Serpula).\nNew building. Damp cement in walls.\n"Common AND dry rot" distinguished.\nTextbook Serpula mechanism:\nmoisture in masonry → timber attack.'},
    {'from': 'evt_keate_v_adams', 'to': 'fun_serpula', 'certainty': 'high',
     'title': 'HIGH: Serpula lacrymans.\nDamp walls causing rot in timber throughout building.\nDistinguished from "common" (wet) rot.\nBanks testified as expert.'},

    # === 1790s SCIENTIFIC IDENTIFICATION ===
    # Wulfen — definitive classification
    {'from': 'evt_wulfen_classification', 'to': 'fun_serpula', 'certainty': 'definitive',
     'title': 'DEFINITIVE: First formal classification\nof Serpula lacrymans (as Boletus lachrymans).\nAustria, 1781.'},
    # Withering — definitive British entry
    {'from': 'evt_withering_addition', 'to': 'fun_serpula', 'certainty': 'definitive',
     'title': 'DEFINITIVE: First British botanical entry.\nB. lachrymans = "dry-rot" added to flora.\nAbsent from 1776 1st edition.'},
    # Sowerby — definitive illustration
    {'from': 'evt_sowerby_classification', 'to': 'fun_serpula', 'certainty': 'definitive',
     'title': 'DEFINITIVE: First British illustration.\n"Common Dry-rot." "Much too common in England."\nExplains etymology of both names.'},

    # === 1798 WOOLWICH SHIP ===
    {'from': 'evt_woolwich_ship_1798', 'to': 'rot_dry', 'certainty': 'high',
     'title': 'HIGH: Serpula lacrymans.\n"Orange and brown fungi in inverted cones"\n= textbook Serpula fruiting bodies.\nFirst description on a SHIP.\nCAVEAT: via Britton 1875 citing European Mag 1811.'},
    {'from': 'evt_woolwich_ship_1798', 'to': 'fun_serpula', 'certainty': 'high',
     'title': 'HIGH: Serpula lacrymans.\nOrange-brown colour + inverted cone shape\nmatches modern identification.\nDeck sinking with a man\'s weight = advanced decay.'},
    # Woolwich could also have wet rot alongside
    {'from': 'evt_woolwich_ship_1798', 'to': 'rot_wet', 'certainty': 'medium',
     'title': 'MEDIUM: Wet rot likely also present.\nShips typically harbour multiple decay fungi.\nSerpula and wet rot can coexist.'},

    # === 1810 HMS QUEEN CHARLOTTE ===
    {'from': 'evt_hms_queen_charlotte', 'to': 'rot_dry', 'certainty': 'medium',
     'title': 'MEDIUM: Called "dry rot" but Sowerby (1812)\nfound VERY LITTLE B. lachrymans.\nPrimary fungi were B. hybridus and\nXylostroma giganteum (oak-specific).'},
    {'from': 'evt_hms_queen_charlotte', 'to': 'fun_serpula', 'certainty': 'low',
     'title': 'LOW: Sowerby found "very little remains"\nof B. lachrymans on the QC in 1812.\nThe building dry rot fungus was NOT\nthe primary ship decay organism.'},
    {'from': 'evt_hms_queen_charlotte', 'to': 'rot_wet', 'certainty': 'high',
     'title': 'HIGH: Sowerby found B. hybridus (EF 289)\nand Xylostroma giganteum (EF 358).\nOak-specific wet/brown rot fungi.\nHygrometer: 828.6° in hold (near saturation).'},
    {'from': 'evt_hms_queen_charlotte', 'to': 'fun_fibroporia', 'certainty': 'high',
     'title': 'HIGH: B. hybridus = Fibroporia vaillantii\n(Parmasto 1968). Brown-rot polypore of\nconifers (order Polyporales).\nLikely on softwood components of ship.'},

    # === 1812 SOWERBY INSPECTION ===
    {'from': 'evt_sowerby_qc_inspection', 'to': 'rot_wet', 'certainty': 'definitive',
     'title': 'DEFINITIVE: Sowerby identified species.\nB. hybridus (EF 289) = abundant.\nXylostroma giganteum (EF 358) = present.\nBoth are oak-specific wet rot fungi.'},
    {'from': 'evt_sowerby_qc_inspection', 'to': 'fun_serpula', 'certainty': 'definitive',
     'title': 'DEFINITIVE: "Very little remains of\nBoletus Lachrymans E.F. 113,\nthe best known Dryrot."\nSerpula was NOT the primary attacker.'},
    {'from': 'evt_sowerby_qc_inspection', 'to': 'fun_fibroporia', 'certainty': 'high',
     'title': "HIGH: B. hybridus (on QC) = Fibroporia\nvaillantii. \"White rugged soft Fungi.\"\nConifer specialist — likely on ship's\npine/fir decking and joinery."},

    # === 1801-1804 ST VINCENT POLICY ===
    {'from': 'evt_st_vincent_timber', 'to': 'rot_wet', 'certainty': 'high',
     'title': 'HIGH: Green timber policy created\nideal conditions for fungal growth.\nUnseasoned wood = high moisture content\n= immediate substrate for decay fungi.'},
    {'from': 'evt_st_vincent_timber', 'to': 'rot_dry', 'certainty': 'medium',
     'title': 'MEDIUM: Green timber also susceptible\nto Serpula if conditions right.\nBut Lambert says "dry rot" label\nmay have been applied loosely.'},

    # === 1821 COMMONS INQUIRY ===
    {'from': 'evt_1821_commons_inquiry', 'to': 'rot_dry', 'certainty': 'high',
     'title': 'HIGH: Bellhouse describes Serpula rhizomorphs:\n"strings of fungus like little bits of leather\nrunning all along in the joints" of wall.\nTextbook Serpula spreading through masonry.'},
    {'from': 'evt_1821_commons_inquiry', 'to': 'fun_serpula', 'certainty': 'high',
     'title': 'HIGH: Bellhouse\'s description matches\nSerpula lacrymans precisely:\nrhizomorphs through masonry joints,\ninfecting timber in adjacent room within 12 months.'},
    {'from': 'evt_1821_commons_inquiry', 'to': 'rot_wet', 'certainty': 'medium',
     'title': 'MEDIUM: Haigh (Liverpool) found Riga timber\n"completely decayed all over fungus" in 9 years.\nWet rot from damp under wine cellar.\nAmerican pine in same builder\'s houses — sound.'},
]

certainty_styles = {
    'definitive': {'color': 'rgba(231,76,60,0.8)', 'width': 3, 'dashes': False},
    'high': {'color': 'rgba(46,204,113,0.6)', 'width': 2.5, 'dashes': False},
    'medium': {'color': 'rgba(241,196,15,0.5)', 'width': 2, 'dashes': [8, 4]},
    'low': {'color': 'rgba(149,165,166,0.4)', 'width': 1.5, 'dashes': [3, 5]},
}

# (Speculative edges deferred to after all nodes are added — see below)

# People nodes
people_added = set()
for person in kg.get('people', []):
    pid = person['id']
    name = person['name']
    # Determine if key person
    is_key = pid in ['per_pepys', 'per_pringle', 'per_banks', 'per_hales',
                     'per_hartley', 'per_mahon', 'per_sowerby', 'per_withering',
                     'per_wulfen', 'per_adam_robert', 'per_seppings',
                     'per_lukin', 'per_byam_martin', 'per_st_vincent',
                     'per_wallace', 'per_copland', 'per_bellhouse']
    color = COLORS['person_key'] if is_key else COLORS['person']
    size = 18 if is_key else 12

    # Short label
    short = name.split('(')[0].strip()
    if len(short) > 25:
        parts = short.split()
        short = parts[-1] if len(parts) > 1 else short[:20]

    nodes.append({
        'id': pid,
        'label': short,
        'shape': 'dot',
        'color': {'background': color, 'border': color,
                  'highlight': {'background': '#fff', 'border': color}},
        'font': {'color': '#ffffff', 'size': 10},
        'nodeType': 'person',
        'size': size,
        'mass': 2,
        'title': f"{name}\n{person.get('role', '')}\n\n{person.get('relevance', '')[:200]}",
    })
    node_ids.add(pid)
    people_added.add(pid)

# Phil Trans corpus — special spanning node (no single year)
if any(s['id'] == 'src_phil_trans_corpus' for s in kg.get('sources', [])):
    corpus_x = year_x.get(1750, (display_years[0]+display_years[-1])//2*x_spacing) if display_years else 0
    nodes.append({
        'id': 'src_phil_trans_corpus',
        'label': 'PHIL TRANS\n1665–1869',
        'x': corpus_x,
        'y': 750,
        'fixed': {'x': False, 'y': False},
        'shape': 'box',
        'color': {'background': COLORS['source_phil_trans'], 'border': '#2c5282',
                  'highlight': {'background': '#fff', 'border': '#2c5282'}},
        'font': {'color': '#ffffff', 'size': 11, 'bold': True},
        'nodeType': 'corpus',
        'size': 30,
        'mass': 12,
        'title': "Philosophical Transactions of the Royal Society\n1665-1869, 8,128 articles\nOCR'd via OLMoCR (8,121 successful)\nGitHub: github.com/jburnford/philosophical-transactions-ocr-1665-1869\n\nPRIMARY CORPUS — all jstor-* sources are articles from this journal.\nKEY NEGATIVE FINDING: dry rot is virtually absent from Phil Trans\n1665-1869 despite the 1810s naval crisis. The Royal Society did not\npublish on the disease — crisis literature appeared in standalone\ntreatises and parliamentary inquiries instead.",
    })
    node_ids.add('src_phil_trans_corpus')

# Source nodes (as diamonds)
for src in kg.get('sources', []):
    sid = src['id']
    if sid == 'src_phil_trans_corpus':
        continue  # already handled above
    year = src.get('year')
    if not year or not isinstance(year, int) or year < 1660 or year > 1880:
        continue

    color = source_color(src)
    title_short = src.get('title', '')
    if len(title_short) > 50:
        title_short = title_short[:47] + '...'

    authors = src.get('authors') or []
    author_str = ', '.join(a for a in authors if a) if authors else 'Anon.'

    # Fix x position to match year node
    src_x = year_x.get(year)
    src_node = {
        'id': sid,
        'label': f"{author_str[:15]} {year}",
        'shape': 'diamond',
        'color': {'background': color, 'border': color,
                  'highlight': {'background': '#fff', 'border': color}},
        'font': {'color': '#ffffff', 'size': 9},
        'nodeType': 'source',
        'size': 10,
        'mass': 1,
        'title': f"{src.get('title', '')}\n{author_str} ({year})\n\n{src.get('dry_rot_connection', src.get('notes', ''))[:300]}",
    }
    if src_x is not None:
        src_node['x'] = src_x
        src_node['fixed'] = {'x': True, 'y': False}
    nodes.append(src_node)
    node_ids.add(sid)

    # Edge to year — short length to anchor sources near their year
    yr_key = f'year_{year}'
    if yr_key in node_ids:
        edges.append({
            'from': sid,
            'to': yr_key,
            'color': {'color': 'rgba(255,255,255,0.15)'},
            'width': 1,
            'length': 60,
        })

    # Edge to authors (people)
    if authors:
        for author in authors:
            # Try to match to a person node
            for person in kg.get('people', []):
                if author and person['name'] and author.lower() in person['name'].lower():
                    if person['id'] in node_ids:
                        edges.append({
                            'from': sid,
                            'to': person['id'],
                            'color': {'color': 'rgba(255,255,255,0.2)'},
                            'width': 1,
                            'dashes': True,
                        })
                    break

# Event nodes
for evt in kg.get('events', []):
    eid = evt['id']
    year = evt.get('year') or evt.get('start_year')
    if not year or not isinstance(year, int) or year < 1660 or year > 1880:
        continue

    desc = evt.get('description', '')
    if len(desc) > 40:
        desc = desc[:37] + '...'

    evt_x = year_x.get(year)
    evt_node = {
        'id': eid,
        'label': desc,
        'shape': 'star',
        'color': {'background': COLORS['event'], 'border': COLORS['event'],
                  'highlight': {'background': '#fff', 'border': COLORS['event']}},
        'font': {'color': '#ffffff', 'size': 9},
        'nodeType': 'event',
        'size': 12,
        'mass': 1,
        'title': f"{evt.get('description', '')}\n{year}\n\n{evt.get('significance', '')[:300]}",
    }
    if evt_x is not None:
        evt_node['x'] = evt_x
        evt_node['fixed'] = {'x': True, 'y': False}
    nodes.append(evt_node)
    node_ids.add(eid)

    yr_key = f'year_{year}'
    if yr_key in node_ids:
        edges.append({
            'from': eid,
            'to': yr_key,
            'color': {'color': 'rgba(255,160,167,0.3)'},
            'width': 2,
            'length': 60,
        })

# === Build rich edges ===

# 1. Person -> Source edges (from key_works fields)
for person in kg.get('people', []):
    pid = person['id']
    for field in ['key_works', 'key_works_phil_trans', 'key_sources']:
        for sid in person.get(field, []):
            if pid in node_ids and sid in node_ids:
                edges.append({
                    'from': pid,
                    'to': sid,
                    'color': {'color': 'rgba(118,183,178,0.4)'},
                    'width': 2,
                    'title': f"{person['name']} authored/connected to this source",
                })

# 2. Person -> Year edges (presidency start/end only, not every year)
for person in kg.get('people', []):
    pid = person['id']
    pres = person.get('presidency', {})
    if pres and pid in node_ids:
        start = pres.get('start', 0)
        end = pres.get('end', 0)
        for y in [start, end]:
            yr_key = f'year_{y}'
            if yr_key in node_ids:
                edges.append({
                    'from': pid,
                    'to': yr_key,
                    'color': {'color': 'rgba(225,87,89,0.25)'},
                    'width': 1.5,
                    'dashes': [6, 4],
                    'title': f"{person['name']} — PRS {start}-{end}",
                    'length': 80,
                })

# 3. Explicit relationships from the KG
rel_colors = {
    'RECEIVED_PAPER_FROM': 'rgba(78,121,167,0.5)',
    'COMMUNICATED_PAPER_FOR': 'rgba(78,121,167,0.5)',
    'ADDRESSED_PAPER_TO': 'rgba(78,121,167,0.5)',
    'CLASSIFIED': 'rgba(237,201,72,0.6)',
    'FIRST_BRITISH_BOTANICAL_ENTRY': 'rgba(237,201,72,0.6)',
    'FIRST_BRITISH_ILLUSTRATION': 'rgba(237,201,72,0.6)',
    'FIRST_PHIL_TRANS_USE': 'rgba(242,142,43,0.6)',
    'CONFIRMED_AS_COMMON_TERM': 'rgba(242,142,43,0.6)',
    'INTRODUCED_TO_FRENCH_AUDIENCE': 'rgba(242,142,43,0.6)',
    'EXPLAINED_ETYMOLOGY': 'rgba(242,142,43,0.6)',
    'TESTIFIED_ABOUT': 'rgba(225,87,89,0.5)',
    'TESTIFIED_IN': 'rgba(225,87,89,0.5)',
    'OBSERVED_FRUITING_BODIES': 'rgba(89,161,79,0.5)',
    'OBSERVED_WITHOUT_UNDERSTANDING': 'rgba(89,161,79,0.5)',
    'CRITICISED': 'rgba(255,255,255,0.3)',
    'CITED_EXPERIMENTS': 'rgba(255,255,255,0.3)',
    'CONNECTED_VIA_RS': 'rgba(255,255,255,0.2)',
    'PREVENTED_IDENTIFICATION_OF': 'rgba(255,100,100,0.4)',
    'PROVIDES_NEGATIVE_EVIDENCE': 'rgba(100,100,100,0.4)',
    'COMMISSIONED_BY_NAVY': 'rgba(89,161,79,0.6)',
    'CONDUCTED_INSPECTION': 'rgba(89,161,79,0.6)',
    'RECOMMENDATIONS_ADOPTED': 'rgba(89,161,79,0.7)',
    'DESIGNED_EXPERIMENT': 'rgba(89,161,79,0.5)',
    'RECEIVED_PAYMENT': 'rgba(255,255,255,0.3)',
    'ACCOMPANIED': 'rgba(118,183,178,0.4)',
    'IMPLEMENTED': 'rgba(118,183,178,0.4)',
    'CAUSED': 'rgba(225,87,89,0.5)',
    'LED_TO': 'rgba(225,87,89,0.4)',
    'CONTINUED_POLICY': 'rgba(118,183,178,0.3)',
    'AUTHOR_CONTINUITY': 'rgba(237,201,72,0.5)',
    'FOUND_VERY_LITTLE': 'rgba(149,165,166,0.5)',
    'FOUND_ABUNDANT': 'rgba(46,204,113,0.5)',
    'PUBLISHED_IN': 'rgba(78,121,167,0.35)',
    'DOCUMENTS': 'rgba(255,157,167,0.5)',
    'DESCRIBES_BEHAVIOUR': 'rgba(237,201,72,0.55)',
    'DESCRIBES_FRUITING_BODIES': 'rgba(237,201,72,0.65)',
    'DESCRIBES_BIOLOGICALLY': 'rgba(237,201,72,0.6)',
    'DESCRIBES_ECOLOGY': 'rgba(237,201,72,0.55)',
    'DOCUMENTS_SPREAD': 'rgba(237,201,72,0.55)',
    'DOCUMENTS_XYLOSTROMA': 'rgba(46,204,113,0.5)',
    'DOCUMENTS_25_DOCKYARD_SPECIES': 'rgba(46,204,113,0.6)',
    'DISTINGUISHES_FROM_WET_ROT': 'rgba(237,201,72,0.55)',
    'DISTINGUISHES_TWO_ORGANISMS': 'rgba(237,201,72,0.7)',
    'DISCUSSES': 'rgba(237,201,72,0.4)',
    'NAMES_ON_ENGLISH_OAK_SHIPS': 'rgba(192,57,43,0.7)',
    'FORMALLY_NAMED': 'rgba(237,201,72,0.8)',
    'PERFORMED': 'rgba(255,157,167,0.55)',
    'CITES': 'rgba(176,122,161,0.55)',
    'CORROBORATES': 'rgba(46,204,113,0.6)',
    'REPRINTED_IN': 'rgba(176,122,161,0.5)',
    'NEGATIVE_EVIDENCE': 'rgba(120,120,120,0.55)',
    'TESTS_BRITANNICA_CLAIM': 'rgba(176,122,161,0.65)',
    'OPENED': 'rgba(255,157,167,0.6)',
    'CLOSED': 'rgba(255,157,167,0.6)',
    'PART_OF': 'rgba(255,157,167,0.4)',
    'FOUND_VERY_LITTLE_ON_QC': 'rgba(149,165,166,0.55)',
    'FOUND_ABUNDANT_ON_QC': 'rgba(46,204,113,0.55)',
    'PROVIDES_MANUSCRIPT_BASIS': 'rgba(237,201,72,0.55)',
    'USED_AS_COMMON_TERM': 'rgba(242,142,43,0.6)',
    'INTRODUCED_TO_FRENCH': 'rgba(242,142,43,0.6)',
    'USES_TERM_FOR_TIMBER': 'rgba(242,142,43,0.6)',
    'TREATISE_ON': 'rgba(242,142,43,0.55)',
    'OBSERVES_TIMBER_DECAY': 'rgba(89,161,79,0.5)',
    'POLICY_OF': 'rgba(225,87,89,0.5)',
}

for rel in kg.get('relationships', []):
    src = rel.get('source', '')
    tgt = rel.get('target', '')
    rtype = rel.get('type', '')
    if src in node_ids and tgt in node_ids:
        color = rel_colors.get(rtype, 'rgba(255,255,255,0.15)')
        width = 3 if rtype in ['CLASSIFIED', 'FIRST_BRITISH_ILLUSTRATION', 'FIRST_PHIL_TRANS_USE', 'TESTIFIED_ABOUT', 'COMMISSIONED_BY_NAVY', 'RECOMMENDATIONS_ADOPTED', 'CONDUCTED_INSPECTION', 'CAUSED'] else 1.5
        edges.append({
            'from': src,
            'to': tgt,
            'color': {'color': color},
            'width': width,
            'title': f"{rtype}: {rel.get('notes', '')}",
            'arrows': {'to': {'enabled': True, 'scaleFactor': 0.5}} if rtype not in ['CONNECTED_VIA_RS'] else {},
        })

# 4. Person -> Event edges (for key events like Wulfen's classification)
person_event_links = [
    ('per_wulfen', 'evt_wulfen_classification', 'CLASSIFIED Serpula lacrymans'),
    ('per_pepys', 'evt_pepys_toadstools', 'Gathered toadstools from ship holds'),
    ('per_pepys', 'evt_30_ships_crisis', 'Documented the crisis'),
    ('per_pepys', 'evt_pepys_timber_conference', 'Organised the conference'),
    ('per_banks', 'evt_keate_v_adams', 'Testified as expert'),
    ('per_hartley', 'evt_keate_v_adams', 'Fireproofing context'),
    ('per_adam_robert', 'evt_keate_v_adams', 'Defendant'),
    ('per_chambers', 'evt_keate_v_adams', 'Arbitrator'),
    ('per_sowerby', 'evt_sowerby_classification', 'Illustrated B. lachrymans'),
    ('per_withering', 'evt_withering_addition', 'Added B. lachrymans to flora'),
    ('per_sowerby', 'evt_sowerby_navy_commission', 'Commissioned by Navy Board'),
    ('per_sowerby', 'evt_sowerby_qc_inspection', 'Inspected Queen Charlotte'),
    ('per_sowerby', 'evt_sowerby_report_adopted', 'Recommendations adopted fleet-wide'),
    ('per_sowerby', 'evt_sowerby_dockyard_inspections', 'Inspected Deptford & Woolwich'),
    ('per_sowerby', 'evt_sowerby_timber_stacks', 'Designed experimental timber stacks'),
    ('per_sowerby', 'evt_sowerby_payment', 'Awarded 200 guineas'),
    ('per_lukin', 'evt_sowerby_qc_inspection', 'Accompanied Sowerby to Plymouth'),
    ('per_lukin', 'evt_lukin_kiln_explosion', 'Kiln explosion at Woolwich'),
    ('per_seppings', 'evt_sowerby_dockyard_inspections', 'Accompanied Sowerby'),
    ('per_seppings', 'evt_1820_lords_inquiry', 'Testified on timber quality'),
    ('per_st_vincent', 'evt_st_vincent_timber', 'Ran down timber stocks'),
    ('per_wallace', 'evt_1821_commons_inquiry', 'Chaired the committee'),
    ('per_copland', 'evt_1820_lords_inquiry', 'Testified: dry rot in own house'),
    ('per_copland', 'evt_1821_commons_inquiry', 'Testified: dry rot in own house'),
    ('per_white_john', 'evt_1820_lords_inquiry', 'Testified: fungus from red pine'),
    ('per_white_john', 'evt_1821_commons_inquiry', 'Testified: moisture is cause'),
    ('per_haigh', 'evt_1821_commons_inquiry', 'CONTRADICTED: American pine sound after 10 yrs'),
    ('per_bellhouse', 'evt_1821_commons_inquiry', 'Described Serpula rhizomorphs in wall'),
    ('per_mghie', 'evt_1821_commons_inquiry', 'Never saw Quebec ship rotten in 6 yrs'),
    ('per_markham', 'evt_markham_speech', 'Merchant ships "ruin of the navy"'),
]
for pid, eid, note in person_event_links:
    if pid in node_ids and eid in node_ids:
        edges.append({
            'from': pid,
            'to': eid,
            'color': {'color': 'rgba(255,157,167,0.5)'},
            'width': 2,
            'title': note,
            'arrows': {'to': {'enabled': True, 'scaleFactor': 0.5}},
        })

# 5. Event -> Source edges (from source_id field)
for evt in kg.get('events', []):
    eid = evt['id']
    sid = evt.get('source_id')
    if sid and eid in node_ids and sid in node_ids:
        edges.append({
            'from': eid,
            'to': sid,
            'color': {'color': 'rgba(255,157,167,0.4)'},
            'width': 1.5,
            'title': f"Event documented in source",
        })

# === Deferred speculative edges (all nodes now in node_ids) ===
for se in speculative_edges:
    src = se['from']
    tgt = se['to']
    cert = se['certainty']
    style = certainty_styles[cert]
    if src in node_ids and tgt in node_ids:
        edge = {
            'from': src,
            'to': tgt,
            'color': {'color': style['color']},
            'width': style['width'],
            'title': se['title'],
            'arrows': {'to': {'enabled': True, 'scaleFactor': 0.5}},
        }
        if style['dashes']:
            edge['dashes'] = style['dashes']
        edges.append(edge)

# === Deferred Institution edges (all people/events now in node_ids) ===
person_institutions = [
    # Navy Board
    ('per_hartwell', 'inst_navy_board', 'Commissioner of the Navy'),
    ('per_legge', 'inst_navy_board', 'Commissioner of the Navy'),
    ('per_thompson_tb', 'inst_navy_board', 'Commissioner of the Navy'),
    ('per_rule', 'inst_navy_board', 'Surveyor of the Navy'),
    ('per_seppings', 'inst_navy_board', 'Surveyor of the Navy (1813-1832)'),
    ('per_byam_martin', 'inst_navy_board', 'Controller of the Navy (1815-1831)'),
    ('per_knowles', 'inst_navy_board', 'Navy Office official'),
    ('per_lukin', 'inst_navy_board', 'Navy consultant on timber preservation'),
    ('per_sowerby', 'inst_navy_board', 'Consultant mycologist (1812-1814)'),
    ('per_sutton', 'inst_navy_board', 'Ventilation inventor'),
    ('per_pepys', 'inst_navy_board', 'Secretary of the Admiralty'),
    # Admiralty
    ('per_st_vincent', 'inst_admiralty', 'First Lord of the Admiralty (1801-1804)'),
    # Royal Society
    ('per_pepys', 'inst_royal_society', 'PRS (1684-1686)'),
    ('per_pringle', 'inst_royal_society', 'PRS (1772-1778)'),
    ('per_banks', 'inst_royal_society', 'PRS (1778-1820)'),
    ('per_hales', 'inst_royal_society', 'FRS'),
    ('per_cook', 'inst_royal_society', 'FRS'),
    ('per_priestley', 'inst_royal_society', 'FRS'),
    ('per_watson_william', 'inst_royal_society', 'FRS'),
    ('per_smeathman', 'inst_royal_society', 'FRS'),
    ('per_mann', 'inst_royal_society', 'FRS'),
    ('per_chambers', 'inst_royal_society', 'FRS'),
    ('per_mahon', 'inst_royal_society', 'FRS'),
    ('per_sowerby', 'inst_royal_society', 'FLS (connected via Banks network)'),
    ('per_withering', 'inst_royal_society', 'FRS (connected)'),
    # Society of Arts
    ('per_adam_robert', 'inst_society_arts', 'Built the Adelphi (Society\'s home)'),
    ('per_hartley', 'inst_society_arts', 'Fireproofing experiments shown to George III'),
    ('per_banks', 'inst_society_arts', 'Member (early period and again after 1791)'),
    # Parliament
    ('per_hartley', 'inst_parliament', 'MP; voted £2,500 for fireproofing'),
    ('per_wallace', 'inst_parliament', 'Chaired 1821 Commons timber inquiry'),
    ('per_copland', 'inst_parliament', 'Testified 1820 & 1821 (London builder)'),
    ('per_white_john', 'inst_parliament', 'Testified 1820 & 1821 (London timber merchant)'),
    ('per_haigh', 'inst_parliament', 'Testified 1821 (Liverpool builder)'),
    ('per_bellhouse', 'inst_parliament', 'Testified 1821 (Manchester builder)'),
    ('per_mghie', 'inst_parliament', 'Testified 1821 (shipbroker)'),
    ('per_markham', 'inst_parliament', 'MP; spoke on dry rot in ships 1804'),
    ('per_markham', 'inst_navy_board', 'Naval captain'),
]

for pid, iid, note in person_institutions:
    if pid in node_ids and iid in node_ids:
        edges.append({
            'from': pid,
            'to': iid,
            'color': {'color': 'rgba(255,255,255,0.15)'},
            'width': 1.5,
            'dashes': [4, 4],
            'title': note,
            'length': 500,
        })

event_institutions = [
    ('evt_sowerby_navy_commission', 'inst_navy_board', 'Navy Board commissioned Sowerby'),
    ('evt_sowerby_report_adopted', 'inst_admiralty', 'Admiralty adopted recommendations fleet-wide'),
    ('evt_sowerby_dockyard_inspections', 'inst_navy_board', 'Inspected Navy Board dockyards'),
    ('evt_sowerby_timber_stacks', 'inst_navy_board', 'Experimental stacks at Deptford dockyard'),
    ('evt_sowerby_payment', 'inst_navy_board', 'Navy Board awarded 200 guineas'),
    ('evt_keate_v_adams', 'inst_royal_society', 'Banks (PRS) testified as expert'),
    ('evt_hms_queen_charlotte', 'inst_navy_board', 'Peak of naval dry rot crisis'),
    ('evt_st_vincent_timber', 'inst_admiralty', 'St Vincent ran down timber stocks'),
    ('evt_1820_lords_inquiry', 'inst_parliament', 'Lords Select Committee on Timber Trade'),
    ('evt_pringle_presidency', 'inst_royal_society', 'Pringle as PRS'),
    ('evt_30_ships_crisis', 'inst_navy_board', 'Parliamentary programme ships decayed'),
    ('evt_pepys_timber_conference', 'inst_navy_board', 'Conference of Master Builders'),
    ('evt_1821_commons_inquiry', 'inst_parliament', 'Commons Select Committee on Timber Trade'),
    ('evt_markham_speech', 'inst_parliament', 'Commons debate on naval supply, March 1804'),
]

for eid, iid, note in event_institutions:
    if eid in node_ids and iid in node_ids:
        edges.append({
            'from': eid,
            'to': iid,
            'color': {'color': 'rgba(255,255,255,0.12)'},
            'width': 1,
            'dashes': [2, 4],
            'title': note,
            'length': 500,
        })

# Navy Board → Admiralty
edges.append({
    'from': 'inst_navy_board', 'to': 'inst_admiralty',
    'color': {'color': 'rgba(255,255,255,0.2)'},
    'width': 2,
    'title': 'Navy Board reported to the Admiralty',
    'arrows': {'to': {'enabled': True, 'scaleFactor': 0.5}},
})

# Count stats
n_people = sum(1 for n in nodes if n.get('nodeType') == 'person')
n_sources = sum(1 for n in nodes if n.get('nodeType') == 'source')
n_events = sum(1 for n in nodes if n.get('nodeType') == 'event')
n_years = sum(1 for n in nodes if n.get('nodeType') == 'year')

# Generate HTML
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dry Rot Knowledge Graph - Temporal View</title>
    <script src="vis-network.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            height: 100vh;
            color: #eee;
            overflow: hidden;
        }}
        .header {{
            padding: 15px 30px;
            background: rgba(0,0,0,0.3);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .header h1 {{ font-size: 1.4rem; }}
        .header .subtitle {{ color: #888; font-size: 0.85rem; margin-top: 4px; }}
        .main-container {{
            display: flex;
            height: calc(100vh - 70px);
            overflow: hidden;
        }}
        .network-panel {{
            flex: 1;
            overflow: hidden;
            position: relative;
        }}
        #network {{ width: 100%; height: 100%; }}
        .sidebar {{
            width: 300px;
            background: rgba(0,0,0,0.3);
            padding: 20px;
            overflow-y: auto;
            border-left: 1px solid rgba(255,255,255,0.1);
        }}
        .sidebar h3 {{
            color: #aaa;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            margin-top: 15px;
        }}
        .sidebar h3:first-child {{ margin-top: 0; }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 6px;
            font-size: 0.78rem;
        }}
        .legend-dot {{ width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; flex-shrink: 0; }}
        .legend-diamond {{
            width: 10px; height: 10px;
            transform: rotate(45deg);
            margin-right: 8px;
            flex-shrink: 0;
        }}
        .legend-star {{ margin-right: 8px; flex-shrink: 0; font-size: 14px; }}
        .legend-box {{
            width: 18px; height: 12px;
            margin-right: 8px;
            border-radius: 2px;
            flex-shrink: 0;
        }}
        .stat-item {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
            font-size: 0.78rem;
        }}
        .stat-item .label {{ color: #888; }}
        .stat-item .value {{ color: #fff; font-weight: 500; }}
        .control-btn {{
            display: block;
            width: 100%;
            padding: 8px;
            margin-bottom: 6px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 5px;
            color: #ccc;
            font-size: 0.8rem;
            cursor: pointer;
            text-align: center;
        }}
        .control-btn:hover {{ background: rgba(255,255,255,0.1); color: #fff; }}
        .details-panel {{
            margin-top: 15px;
            padding-top: 12px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
        .details-content {{ font-size: 0.8rem; color: #bbb; line-height: 1.5; }}
        .instructions {{
            margin-top: 12px;
            padding: 8px;
            background: rgba(255,255,255,0.03);
            border-radius: 5px;
            font-size: 0.72rem;
            color: #888;
            line-height: 1.4;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Dry Rot in Britain: Temporal Knowledge Graph</h1>
        <p class="subtitle">Tracing dry rot from Pepys (1684) through Sowerby's inspection of HMS Queen Charlotte (1812) and the naval crisis (1810s-20s) to Britton's retrospective (1875)</p>
    </div>
    <div class="main-container">
        <div class="network-panel">
            <div id="network"></div>
        </div>
        <div class="sidebar">
            <h3>Node Types</h3>
            <div class="legend-item"><div class="legend-box" style="background: {COLORS['year']['bg']}; border: 1px solid {COLORS['year']['border']};"></div><span>Years (fixed timeline)</span></div>
            <div class="legend-item"><div class="legend-dot" style="background: {COLORS['person_key']};"></div><span>Key People</span></div>
            <div class="legend-item"><div class="legend-dot" style="background: {COLORS['person']};"></div><span>Other People</span></div>
            <div class="legend-item"><span class="legend-star">&#9733;</span><span>Events</span></div>

            <h3>Institutions</h3>
            <div class="legend-item"><div class="legend-box" style="background: #2C6E49;"></div><span>Navy Board</span></div>
            <div class="legend-item"><div class="legend-box" style="background: #1B4332;"></div><span>Admiralty</span></div>
            <div class="legend-item"><div class="legend-box" style="background: #4A4E69;"></div><span>Royal Society</span></div>
            <div class="legend-item"><div class="legend-box" style="background: #7B2D8E;"></div><span>Society of Arts</span></div>
            <div class="legend-item"><div class="legend-box" style="background: #8B6914;"></div><span>Parliament</span></div>

            <h3>Biological</h3>
            <div class="legend-item"><div class="legend-dot" style="background: #8B4513; width: 14px; height: 14px; border-radius: 3px;"></div><span>Brown rot (parent type)</span></div>
            <div class="legend-item"><div class="legend-dot" style="background: #2E86C1; width: 14px; height: 14px; border-radius: 3px;"></div><span>Wet rot / native fungi</span></div>
            <div class="legend-item"><div class="legend-dot" style="background: #C0392B; width: 14px; height: 14px; border-radius: 3px;"></div><span>Dry rot / Serpula</span></div>

            <h3>Certainty of Attribution</h3>
            <div class="legend-item" style="font-size:0.72rem;"><span style="margin-right:8px;color:#2ecc71;">&#9644;&#9644;</span><span>High confidence</span></div>
            <div class="legend-item" style="font-size:0.72rem;"><span style="margin-right:8px;color:#f1c40f;">- - -</span><span>Medium confidence</span></div>
            <div class="legend-item" style="font-size:0.72rem;"><span style="margin-right:8px;color:#95a5a6;">. . .</span><span>Low / speculative</span></div>
            <div class="legend-item" style="font-size:0.72rem;"><span style="margin-right:8px;color:#e74c3c;">&#9644;&#9644;</span><span>Definitive ID</span></div>

            <h3>Source Types</h3>
            <div class="legend-item"><div class="legend-diamond" style="background: {COLORS['source_phil_trans']};"></div><span>Phil Trans articles</span></div>
            <div class="legend-item"><div class="legend-diamond" style="background: {COLORS['source_building']};"></div><span>Building / legal</span></div>
            <div class="legend-item"><div class="legend-diamond" style="background: {COLORS['source_naval']};"></div><span>Naval</span></div>
            <div class="legend-item"><div class="legend-diamond" style="background: {COLORS['source_botanical']};"></div><span>Botanical / mycological</span></div>
            <div class="legend-item"><div class="legend-diamond" style="background: {COLORS['source_encyclopedia']};"></div><span>Encyclopedia entries</span></div>
            <div class="legend-item"><div class="legend-diamond" style="background: {COLORS['source_other']};"></div><span>Other sources</span></div>
            <div class="legend-item"><div class="legend-diamond" style="background: {COLORS['negative']};"></div><span>Negative evidence</span></div>

            <h3>Statistics</h3>
            <div class="stat-item"><span class="label">Years</span><span class="value">{display_years[0]}-{display_years[-1]}</span></div>
            <div class="stat-item"><span class="label">People</span><span class="value">{n_people}</span></div>
            <div class="stat-item"><span class="label">Sources</span><span class="value">{n_sources}</span></div>
            <div class="stat-item"><span class="label">Events</span><span class="value">{n_events}</span></div>
            <div class="stat-item"><span class="label">Connections</span><span class="value">{len(edges)}</span></div>

            <h3>Controls</h3>
            <button class="control-btn" onclick="togglePhysics()">Toggle Physics</button>
            <button class="control-btn" onclick="resetView()">Reset View</button>

            <div class="details-panel">
                <h3>Details</h3>
                <div class="details-content" id="details">Click a node to see details.</div>
            </div>

            <div class="instructions">
                <strong>Navigation:</strong> Scroll to zoom, drag to pan, click nodes for details.
                Years are fixed along the top. Sources (diamonds) connect to their year.
                People (circles) float below, pulled toward years they're connected to.
            </div>
        </div>
    </div>
    <script>
        const networkNodes = {json.dumps(nodes)};
        const networkEdges = {json.dumps(edges)};
        const nodes = new vis.DataSet(networkNodes);
        const edges = new vis.DataSet(networkEdges);
        let physicsEnabled = true;

        const network = new vis.Network(document.getElementById('network'), {{ nodes, edges }}, {{
            nodes: {{
                font: {{ color: '#ffffff', size: 10 }},
                borderWidth: 2
            }},
            edges: {{
                smooth: {{ type: 'continuous' }}
            }},
            physics: {{
                enabled: true,
                stabilization: {{ iterations: 800, fit: true }},
                barnesHut: {{
                    gravitationalConstant: -3000,
                    centralGravity: 0.01,
                    springLength: 100,
                    springConstant: 0.08,
                    damping: 0.5,
                    avoidOverlap: 0.5
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                navigationButtons: true,
                keyboard: true,
                dragNodes: true
            }}
        }});

        const MIN_PERSON_Y = 150;
        const MIN_BIO_Y = 500;
        const PUSH_STRENGTH = 0.5;
        network.on('beforeDrawing', function(ctx) {{
            nodes.forEach(function(node) {{
                if (node.nodeType === 'year') return;
                const pos = network.getPosition(node.id);
                if (node.nodeType === 'rot_type' || node.nodeType === 'fungus') {{
                    // Push rot/fungi nodes toward bottom
                    if (pos.y < MIN_BIO_Y) {{
                        const newY = pos.y + (MIN_BIO_Y - pos.y) * PUSH_STRENGTH;
                        network.moveNode(node.id, pos.x, newY);
                    }}
                }} else {{
                    if (pos.y < MIN_PERSON_Y) {{
                        const newY = pos.y + (MIN_PERSON_Y - pos.y) * PUSH_STRENGTH;
                        network.moveNode(node.id, pos.x, newY);
                    }}
                }}
            }});
        }});

        network.on('stabilizationIterationsDone', function() {{
            network.setOptions({{
                physics: {{
                    barnesHut: {{
                        gravitationalConstant: -2000,
                        centralGravity: 0.005,
                        springConstant: 0.04,
                        damping: 0.6
                    }}
                }}
            }});
        }});

        network.on('click', function(params) {{
            if (params.nodes.length > 0) {{
                const nodeId = params.nodes[0];
                const node = nodes.get(nodeId);
                if (node && node.title) {{
                    const html = node.title.replace(/\\n/g, '<br>');
                    document.getElementById('details').innerHTML = '<b>' + node.label + '</b><br><br>' + html;
                }} else if (node) {{
                    document.getElementById('details').innerHTML = '<b>' + node.label + '</b>';
                }}
            }}
        }});

        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
            network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
        }}

        function resetView() {{
            network.fit({{ animation: true }});
        }}
    </script>
</body>
</html>'''

os.makedirs('docs', exist_ok=True)
out_path = os.path.join('docs', 'index.html')
with open(out_path, 'w') as f:
    f.write(html)

print(f"Generated {out_path}")
print(f"  {n_years} years, {n_people} people, {n_sources} sources, {n_events} events")
print(f"  {len(edges)} edges")
print(f"  Year range: {display_years[0]}-{display_years[-1]}")
