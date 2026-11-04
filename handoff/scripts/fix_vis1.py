#!/usr/bin/env python3
"""Visual cortex audit fixes (2026-11-04): every new sentence read against the PubMed abstracts. Applied once.

  - marshel2011's seven areas include V1 (V1 + six higher areas);
  - britten1992: "most" MT neurons, not single neurons;
  - hadjikhani2001: three people; benson1988: five patients (a case series, not a definition);
  - hendry2000: the parallel pathways are "likely" to process different aspects of the scene;
  - ko2011: twice the rate *of orthogonally tuned pairs*;
  - moran1985: no "classic study" (an editorial label);
  - statuses: links that rest on one study are "emerging" (definition in knowledge.json statuses).
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / 'data/knowledge.json'
kb = json.loads(P.read_text(encoding='utf-8'))
E = {e['id']: e for e in kb['entities']}
L = {f"{l['s']}>{l['t']}": l for l in kb['links']}
C = {c['id']: c for c in kb['chains']}


def sub(obj, field, old, new):
    s = obj[field]
    assert s.count(old) == 1, (field, old[:70], s.count(old))
    obj[field] = s.replace(old, new)


sub(E['v1'], 'summary', 'Attention did not affect striate cells in a classic study (monkey).',
    'Striate cells were unaffected by attention in monkeys attending to one of two stimuli (monkey).')
sub(E['mouse-hva'], 'summary',
    'Seven of these areas each encode a distinct combination of spatial and temporal frequency, orientation and direction preferences, perhaps forming motion- and pattern-related groups analogous to dorsal and ventral streams (mouse).',
    'In V1 and six higher areas, layer 2/3 populations each encode a distinct combination of spatial and temporal frequency, orientation and direction preferences, and the higher areas may form motion- and pattern-related groups analogous to dorsal and ventral streams (mouse).')
sub(E['mt'], 'summary', 'and single MT neurons are about as sensitive to weak motion as the animal itself (monkey).',
    'and most MT neurons are about as sensitive to weak motion as the animal itself (monkey).')
sub(L['mt>f-vision'], 'rel', 'and single MT neurons match the animal\'s sensitivity to motion (monkey)',
    'and most MT neurons match the animal\'s sensitivity to motion (monkey)')
sub(C['vis-motion'], 'desc', 'MT lesions raise motion thresholds and single MT neurons match',
    'MT lesions raise motion thresholds and most MT neurons match')
sub(E['c-migraine'], 'summary', 'During visual aura, fMRI shows changes', 'During visual aura in three people, fMRI showed changes')
sub(L['visual-cortex>c-migraine'], 'rel', 'during visual aura, changes', 'during visual aura in three people, changes')
sub(E['c-pca'], 'summary',
    'A progressive dementia heralded by disorders of higher visual function, followed by alexia,',
    'In five patients, a progressive dementia was heralded by disorders of higher visual function, followed by alexia,')
sub(L['visual-cortex>c-pca'], 'rel',
    'a progressive dementia heralded by disorders of higher visual function, with predominant parieto-occipital atrophy on imaging in two of five patients (human)',
    'five patients had a progressive dementia heralded by disorders of higher visual function, with predominant parieto-occipital atrophy on imaging in two of them (human)')
sub(L['eyes>lgn'], 'rel', 'and a third, koniocellular channel carry different aspects of the image (review)',
    'and a third, koniocellular channel are likely to carry different aspects of the image (review)')
sub(E['v1-pyr'], 'summary', 'They connect at twice the rate when they share an orientation preference,',
    'They connect at twice the rate when they share an orientation preference as when their preferences are orthogonal,')
for lid in ('v1>mt', 'v1>v4', 'v1>mouse-hva', 'it>f-face', 'ffa>f-face', 'visual-cortex>pontine'):
    assert L[lid]['status'] == 'supported', lid
    L[lid]['status'] = 'emerging'

P.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('applied 11 wording fixes and 6 status changes')
