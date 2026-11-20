# -*- coding: utf-8 -*-
"""
tools/build_all_v03.py
Master generator for Brain Circuit Atlas v0.3.
Populates knowledge.json, papers.json, pubmed_cache.json, meshes.json.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
sys.path.insert(0, str(ROOT / 'tools'))

from v03_dataset import NEW_PAPERS, PUBMED_CACHE_ENTRIES
from v03_entities import NEW_REGIONS
from v03_data_builder import get_entities
from v03_links import get_links, get_circuits

REF_REMAP = {
    'gordon2023scan': 'gordon2023',
    'biccn2021m1': 'biccn2021',
    'kozareva2021cerebellum': 'kozareva2021',
    'hao2024cerebellum': 'hao2024',
    'bostan2010bgcb': 'bostan2010',
    'rathelot2009cm': 'rathelot2009',
    'economo2018descending': 'economo2018',
    'tovote2016midbrain': 'tovote2016',
    'strick2009cerebellum': 'strick2009',
    'krienen2020interneurons': 'krienen2020innovations',
    'chen2023macaque': 'chen2023stereo'
}

EXISTING_PARENTS = {
    'caudate': 'striatum',
    'putamen': 'striatum',
    'nac': 'striatum',
    'gpe': 'basal-ganglia',
    'gpi': 'basal-ganglia',
    'snr': 'basal-ganglia',
    'snc': 'basal-ganglia',
    'm1': 'motor-cortex',
    'premotor': 'motor-cortex',
    'alm': 'premotor',
    'pt-neurons': 'm1',
    'l23-pyr': 'm1',
    'm1-pv': 'm1',
    'm1-sst': 'm1',
    'cm-cells': 'm1',
    'dlpfc': 'pfc',
    'vmpfc': 'pfc',
    'ofc': 'pfc',
    'acc': 'pfc',
    'sgacc': 'acc',
    'mpfc': 'pfc',
    'mpfc-pl': 'mpfc',
    'mpfc-il': 'mpfc',
    'dentate': 'dcn',
    'fastigial': 'dcn',
    'interposed': 'dcn',
    'cb-cortex': 'cerebellum',
    'dcn': 'cerebellum',
    'io': 'cerebellum',
    'purkinje': 'cb-cortex',
    'granule': 'cb-cortex',
    'golgi': 'cb-cortex',
    'mli': 'cb-cortex',
    'ubc': 'cb-cortex',
    'lugaro': 'cb-cortex',
    'bergmann': 'cb-cortex',
    'dg': 'hippocampus',
    'ca3': 'hippocampus',
    'ca2': 'hippocampus',
    'ca1': 'hippocampus',
    'subiculum': 'hippocampus',
    'entorhinal': 'hippocampus',
    'v1': 'visual-cortex',
    'v2': 'visual-cortex',
    'v4': 'visual-cortex',
    'mt': 'visual-cortex',
    'it': 'visual-cortex',
    'ffa': 'it',
    'la': 'bla-complex',
    'bla': 'bla-complex',
    'cea': 'amygdala',
    'mea': 'amygdala',
    'itc': 'amygdala',
    'ains': 'insula',
    'pins': 'insula',
    'gc': 'insula',
    'vens': 'ains',
    'ob': 'olfactory',
    'piriform': 'olfactory',
    'coa': 'olfactory',
    'vno': 'olfactory',
    'lateral-septum': 'basal-forebrain',
    'diagonal-band': 'basal-forebrain',
    'substantia-innominata': 'basal-forebrain',
    'medial-septum': 'basal-forebrain'
}

def clean_refs(refs):
    return [REF_REMAP.get(r, r) for r in refs]

def run():
    print("=== Master v0.3 Build Starting (from clean v02 baselines) ===")
    with open(DATA / 'knowledge.json', 'r', encoding='utf-8') as f:
        kb = json.load(f)
    with open(DATA / 'papers.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
    with open(DATA / 'pubmed_cache.json', 'r', encoding='utf-8') as f:
        cache = json.load(f)
    with open(DATA / 'meshes.json', 'r', encoding='utf-8') as f:
        meshes = json.load(f)

    # 1. Update meta
    kb['meta']['version'] = '0.3'
    kb['meta']['subtitle'] = (
        "An evidence-linked map of the cerebellum, motor and prefrontal cortex, basal ganglia, "
        "hippocampus, thalamus, hypothalamus, colliculi & tectum, amygdala, visual cortex, insula, "
        "olfactory system, basal forebrain and their connections, with single-cell taxonomies, "
        "laminar wiring and primate homology, from molecules to mind"
    )

    # 2. Add new papers
    for p in papers:
        if 'decision' in p.get('domains', []):
            p['domains'] = ['executive' if d == 'decision' else d for d in p['domains']]
    for e in kb['entities']:
        if 'decision' in e.get('domains', []):
            e['domains'] = ['executive' if d == 'decision' else d for d in e['domains']]
    existing_paper_keys = {p['key']: p for p in papers}
    added_papers = 0
    for np in NEW_PAPERS:
        if np['key'] not in existing_paper_keys:
            papers.append(np)
            existing_paper_keys[np['key']] = np
            added_papers += 1
        else:
            p = existing_paper_keys[np['key']]
            for r in np.get('regions', []):
                if r not in p['regions']:
                    p['regions'].append(r)
    print(f"Added {added_papers} new papers; total papers: {len(papers)}")

    # 3. Add pubmed cache entries
    added_cache = 0
    for pmid, rec in PUBMED_CACHE_ENTRIES.items():
        if pmid not in cache:
            cache[pmid] = rec
            added_cache += 1
    print(f"Added {added_cache} new pubmed cache records; total cache: {len(cache)}")

    # 4. Insert new regions before condition (adhd)
    existing_region_ids = [r['id'] for r in kb['regions']]
    for nr in NEW_REGIONS:
        if nr['id'] not in existing_region_ids:
            idx = next((i for i, r in enumerate(kb['regions']) if r.get('kind') == 'condition'), len(kb['regions']))
            kb['regions'].insert(idx, nr)
            existing_region_ids.insert(idx, nr['id'])
            print(f"Inserted region: {nr['id']}")

    # 5. Assign parents to existing entities
    existing_ent_map = {e['id']: e for e in kb['entities']}
    for eid, pid in EXISTING_PARENTS.items():
        if eid in existing_ent_map:
            existing_ent_map[eid]['parent'] = pid

    # 6. Merge entities from get_entities()
    new_entities = get_entities()
    added_ents = 0
    for ne in new_entities:
        ne['refs'] = clean_refs(ne.get('refs', []))
        eid = ne['id']
        if eid in existing_ent_map:
            # Merge refs and optional fields
            cur = existing_ent_map[eid]
            for r in ne['refs']:
                if r not in cur['refs']:
                    cur['refs'].append(r)
            if 'parent' in ne and 'parent' not in cur:
                cur['parent'] = ne['parent']
            if 'region' in ne and not cur.get('region'):
                cur['region'] = ne['region']
        else:
            kb['entities'].append(ne)
            existing_ent_map[eid] = ne
            added_ents += 1
    print(f"Added {added_ents} new entities; total entities: {len(kb['entities'])}")

    # Special adjustments for thalamus and scan
    if 'thalamus' in existing_ent_map:
        existing_ent_map['thalamus']['region'] = 'thalamus'
        existing_ent_map['thalamus']['kind'] = 'region'
        existing_ent_map['thalamus']['level'] = 'regional'
    if 'scan' in existing_ent_map:
        existing_ent_map['scan']['parent'] = 'm1'

    # 7. Add new links from get_links()
    existing_link_ids = {f"{l['s']}>{l['t']}" for l in kb['links']}
    new_links = get_links()
    added_links = 0
    for nl in new_links:
        nl['refs'] = clean_refs(nl.get('refs', []))
        lid = f"{nl['s']}>{nl['t']}"
        if lid not in existing_link_ids:
            kb['links'].append(nl)
            existing_link_ids.add(lid)
            added_links += 1
        else:
            cur_l = next(l for l in kb['links'] if f"{l['s']}>{l['t']}" == lid)
            if 'laminar' in nl and 'laminar' not in cur_l:
                cur_l['laminar'] = nl['laminar']
            for r in nl['refs']:
                if r not in cur_l['refs']:
                    cur_l['refs'].append(r)
    print(f"Added {added_links} new links; total links: {len(kb['links'])}")

    # 8. Add circuits to kb['atlas3d']['circuits']
    existing_circuit_ids = {c['id'] for c in kb['atlas3d']['circuits']}
    new_circuits = get_circuits()
    added_circuits = 0
    for nc in new_circuits:
        if nc['id'] not in existing_circuit_ids:
            kb['atlas3d']['circuits'].append(nc)
            existing_circuit_ids.add(nc['id'])
            added_circuits += 1
    print(f"Added {added_circuits} new 3D circuits; total circuits: {len(kb['atlas3d']['circuits'])}")

    # 9. Update atlas3d macaque aliases
    m_aliases = kb['atlas3d']['aliases']['macaque']
    m_aliases['mpfc-pl'] = 'acc'
    m_aliases['mpfc-il'] = 'sgacc'

    # Add aliases for new subregions/cells in macaque/mouse/human
    for sp in ['macaque', 'mouse', 'human']:
        aliases = kb['atlas3d']['aliases'][sp]
        for tid in ['thal-va', 'thal-vla', 'thal-vlp', 'md-mc', 'md-pc', 'atn', 'atn-ad', 'atn-av', 'pvt', 'reuniens', 'trn', 'zi', 'mhb', 'lhb', 'thal-core-relay', 'thal-matrix-relay', 'trn-spp1-core', 'trn-ecel1-edge', 'lhb-bursting', 'vpmpc', 'mgv', 'mgd', 'mgm']:
            if tid not in aliases:
                aliases[tid] = 'thalamus'
        for hid in ['mpoa', 'vlpo', 'mnpo-ovlt', 'scn', 'pvn', 'son', 'ahn', 'arc', 'vmh', 'vmh-dm', 'vmh-vl', 'dmh', 'sum', 'mm-lm', 'arc-agrp', 'arc-pomc', 'arc-kndy', 'pvn-oxt', 'pvn-crh', 'vlpo-sleep', 'vmh-dm-sf1', 'vmh-vl-esr1', 'lha-orexin', 'sum-glugaba']:
            if hid not in aliases:
                aliases[hid] = 'hypothalamus'
        for cid in ['sc-med', 'sc-lat', 'pbg', 'sc-widefield-vert', 'sc-narrowfield-vert', 'dsc-pitx2-orient', 'dsc-pvalb-looming', 'ic-cnic', 'ic-dcic', 'ic-ecic', 'ic-disc-tonotopic', 'ic-vip-stellate', 'ic-npy-gaba-proj', 'dmpag-dlpag', 'lpag', 'vlpag', 'vlpag-chx10-freeze', 'mlr', 'cnf']:
            if cid not in aliases:
                aliases[cid] = 'superior-colliculus' if 'sc-' in cid or 'dsc-' in cid or cid == 'pbg' else ('inferior-colliculus' if 'ic-' in cid else 'pag')

    # 10. Update atlas3d composite entries
    comp = kb['atlas3d']['composite']
    comp['striatum'] = ['caudate', 'putamen', 'nac']
    comp['thalamus'] = ['thal-val', 'thal-vm', 'thal-md', 'pf', 'thal-cmpf', 'thal-va', 'thal-vlp', 'vpm', 'vpl', 'pulvinar', 'mgv', 'mgd', 'mgm', 'lp']
    comp['superior-colliculus'] = ['sc-sup', 'sc-deep']
    comp['inferior-colliculus'] = ['ic-cnic', 'ic-dcic', 'ic-ecic']
    comp['tectum'] = ['sc-sup', 'sc-deep', 'ic-cnic', 'ic-dcic', 'ic-ecic']
    comp['hypothalamus'] = ['mpoa', 'vlpo', 'scn', 'pvn', 'son', 'ahn', 'arc', 'vmh', 'dmh', 'sum', 'mm-lm']
    comp['bla-complex'] = ['la', 'bla', 'pal']

    # 11. Uncollapse meshes.json
    for item in meshes['human']['items']:
        if item.get('key') == 'caudate':
            item['entity'] = 'caudate'
        elif item.get('key') == 'putamen':
            item['entity'] = 'putamen'

    for item in meshes['mouse']['items']:
        if item.get('key') == 'vm':
            item['entity'] = 'thal-vm'
        elif item.get('key') == 'pf':
            item['entity'] = 'pf'
        elif item.get('key') == 'val':
            item['entity'] = 'thal-val'
        elif item.get('key') == 'md':
            item['entity'] = 'thal-md'

    for item in meshes['macaque']['items']:
        if item.get('key') == 'cd':
            item['entity'] = 'caudate'
        elif item.get('key') == 'pu':
            item['entity'] = 'putamen'
        elif item.get('key') == 'vavl':
            item['entity'] = 'thal-val'
        elif item.get('key') == 'md':
            item['entity'] = 'thal-md'
        elif item.get('key') == 'cmpf':
            item['entity'] = 'thal-cmpf'

    # 12. Ensure all papers cited by entities include the entity's region
    paper_map = {p['key']: p for p in papers}
    for e in kb['entities']:
        r = e.get('region')
        if r:
            for ref in e.get('refs', []):
                if ref in paper_map and r not in paper_map[ref]['regions']:
                    paper_map[ref]['regions'].append(r)

    # 13. Write out all updated files
    with open(DATA / 'knowledge.json', 'w', encoding='utf-8') as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)
    with open(DATA / 'papers.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    with open(DATA / 'pubmed_cache.json', 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)
    with open(DATA / 'meshes.json', 'w', encoding='utf-8') as f:
        json.dump(meshes, f, indent=2, ensure_ascii=False)

    print("=== Master v0.3 Build Complete! All files written successfully. ===")

if __name__ == '__main__':
    run()
