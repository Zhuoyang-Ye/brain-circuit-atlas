#!/usr/bin/env python3
"""Olfactory audit fixes (2026-11-04): every new sentence read against the abstracts. Applied once.
Also records the earlier fix: q-olf-pd no longer lists c-alzheimers as an entity (it pulled that entity into the
basal-ganglia region; the text still names Alzheimer's disease)."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / 'data/knowledge.json'
kb = json.loads(P.read_text(encoding='utf-8'))
E = {e['id']: e for e in kb['entities']}
Q = {q['id']: q for q in kb['questions']}


def sub(obj, field, old, new):
    assert obj[field].count(old) == 1, (field, old[:60])
    obj[field] = obj[field].replace(old, new)


sub(E['ob'], 'summary', 'The first relay of smell, where receptor inputs converge on glomeruli',
    'Where the distributed input from the nose converges on glomeruli')
sub(E['osn'], 'summary', 'Ablating the dorsal-zone neurons abolishes innate aversion to odours without abolishing their detection (mouse).',
    'Ablating the dorsal-zone neurons abolishes innate responses to aversive odorants, although the mice still detect them (mouse).')
sub(Q['q-olf-cerebellum'], 'text', 'cerebellar hemispheres in proportion to concentration and sniffing',
    'cerebellar hemispheres, more strongly at higher concentrations, and sniffing')
assert Q['q-olf-pd']['entities'] == ['olfactory', 'c-parkinson']
P.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('applied 3 fixes')
