#!/usr/bin/env python3
"""Add two locus coeruleus taste papers to the insula region (2026-11-04, at the user's request). Applied once.

  fan2026  PMID 42747960  Fan W, To P, Sciolino NR. Locus coeruleus activation transforms cortical taste
           representations. Cell Rep 2026. doi 10.1016/j.celrep.2026.117990 (UpdateOf a bioRxiv preprint; no erratum)
  fan2024  PMID 38649278  Fan W, Engborg CB, Sciolino NR. Locus ceruleus dynamics are suppressed during licking and
           enhanced postlicking independent of taste novelty. eNeuro 2024. doi 10.1523/ENEURO.0535-23.2024 (no erratum)

Both mouse (MeSH). Every sentence below is worded from the two abstracts. Adds the papers (tag insula), sentences on
lc (untagged) and gc (tagged insula), links lc>gc and lc>f-taste, question q-ins-ne-taste, and lc>gc to circuit
ins-taste.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
KP, PP = ROOT / 'data/knowledge.json', ROOT / 'data/papers.json'
kb = json.loads(KP.read_text(encoding='utf-8'))
papers = json.loads(PP.read_text(encoding='utf-8'))

new = [
    {"key": "fan2026", "pmid": "42747960", "regions": ["insula"], "evidence": "intervention", "species": ["mouse"],
     "methods": ["optogenetics", "miniscope calcium imaging"], "levels": ["circuit", "cellular"], "domains": ["sensory", "reward"],
     "finding": "Phasic optogenetic activation of the locus coeruleus strengthened correlations between gustatory cortex responses and palatability and expanded the range of taste representations along a palatability axis, through an aversive shift of every tastant except sucrose, whereas tonic activation affected fewer neurons and did not expand the attribute axes (mouse)."},
    {"key": "fan2024", "pmid": "38649278", "regions": ["insula"], "evidence": "observational", "species": ["mouse"],
     "methods": ["fiber photometry"], "levels": ["cellular", "cognitive"], "domains": ["sensory", "reward"],
     "finding": "In water-restricted mice licking novel or familiar tastants, noradrenergic locus coeruleus activity was suppressed during lick bursts and transiently rose when licking stopped, regardless of novelty, and brief unexpected tastants did not activate it although visual and auditory stimuli did; the authors suggest a possible role for noradrenergic nuclei other than the locus coeruleus in signalling critical information about taste (mouse)."},
]
have = {p['key'] for p in papers}
for p in new:
    assert p['key'] not in have and str(p['pmid']) not in {str(x['pmid']) for x in papers}, p['key']
papers.extend(new)

E = {e['id']: e for e in kb['entities']}


def extend(id_, sentence, refs):
    e = E[id_]
    e['summary'] = e['summary'].rstrip() + ' ' + sentence
    for r in refs:
        if r not in e['refs']:
            e['refs'].append(r)


assert not E['lc'].get('region') and E['gc'].get('region') == 'insula'
extend('lc', 'Phasic activation of it reshapes taste coding in the gustatory cortex along a palatability axis (mouse), but its activity is not driven by taste novelty: it is suppressed while mice lick and rises briefly when licking stops (mouse).',
       ['fan2026', 'fan2024'])
extend('gc', 'Phasic locus coeruleus activation strengthens the link between its responses and palatability, shifting the representations of all tastants except sucrose in the aversive direction (mouse).',
       ['fan2026'])

L = {f"{l['s']}>{l['t']}" for l in kb['links']}
for s, t, kind, status, rel, refs in [
    ('lc', 'gc', 'causal', 'emerging',
     'phasic activation strengthens gustatory cortex correlations with palatability and expands taste representations along a palatability axis, shifting all tastants except sucrose toward aversive; tonic activation does not expand the attribute axes (mouse)',
     ['fan2026']),
    ('lc', 'f-taste', 'functional', 'emerging',
     'locus coeruleus activity is suppressed during licking and rises briefly afterwards, independent of taste novelty, and brief unexpected tastes do not activate it although visual and auditory stimuli do (mouse)',
     ['fan2024']),
]:
    assert f'{s}>{t}' not in L
    kb['links'].append({'s': s, 't': t, 'rel': rel, 'status': status, 'kind': kind, 'refs': refs})

assert 'q-ins-ne-taste' not in {q['id'] for q in kb['questions']}
kb['questions'].append({
    'id': 'q-ins-ne-taste', 'title': 'Where does the noradrenaline for a new taste come from?',
    'text': 'New tastes are known to increase noradrenaline release in forebrain areas that process taste, yet locus coeruleus activity in mice is suppressed during licking and is not influenced by taste novelty, suggesting a possible role for other noradrenergic nuclei (fan2024). Phasic locus coeruleus activation does reshape taste coding in the gustatory cortex along a palatability axis (fan2026). Which noradrenergic nuclei signal taste novelty, and when does locus coeruleus release reshape taste coding during natural eating?',
    'entities': ['lc', 'gc', 'f-taste'], 'refs': ['fan2024', 'fan2026'],
    'approaches': ['Record noradrenergic nuclei of the medulla (A1/A2) as mice first meet a new taste.',
                   'Measure noradrenaline release in the gustatory cortex with a genetically encoded sensor during novel and familiar tastes.',
                   'Activate the locus coeruleus at the end of a lick bout, when it naturally rises, and test taste preference later.'],
})

C = {c['id']: c for c in kb['atlas3d']['circuits']}
c = C['ins-taste']
assert c['links'] == ['thalamus>gc', 'gc>amygdala', 'gc>cea']
c['links'] = ['thalamus>gc', 'lc>gc', 'gc>amygdala', 'gc>cea']
c['desc'] = c['desc'].replace(
    'The thalamic taste area projects to insular-opercular cortex (review);',
    'The thalamic taste area projects to insular-opercular cortex (review), and phasic locus coeruleus activation reshapes taste coding there along a palatability axis (mouse);')
assert 'locus coeruleus' in c['desc']

KP.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
PP.write_text(json.dumps(papers, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('added fan2026, fan2024; 2 links, 1 question; lc and gc extended; lc>gc in ins-taste')
