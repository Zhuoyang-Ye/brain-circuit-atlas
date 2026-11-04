#!/usr/bin/env python3
"""Insula audit fixes (2026-11-04): every new sentence read against the abstracts. Applied once."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / 'data/knowledge.json'
kb = json.loads(P.read_text(encoding='utf-8'))
E = {e['id']: e for e in kb['entities']}
L = {f"{l['s']}>{l['t']}": l for l in kb['links']}


def sub(obj, field, old, new):
    assert obj[field].count(old) == 1, (field, old[:60])
    obj[field] = obj[field].replace(old, new)


# naqvi2007: "undergo a disruption of smoking addiction"
sub(E['insula'], 'summary', 'were more likely to lose their addiction (human).', 'were more likely to have their addiction disrupted (human).')
# singer2004: AI and ACC activation "correlated with individual empathy scores"
sub(E['ains'], 'summary', 'and to a signal that a loved one is in pain, in proportion to empathy (human),',
    'and to a signal that a loved one is in pain, with responses that correlate with empathy scores (human),')
sub(L['ains>f-social'], 'rel', "and to a loved one's, scaled with empathy scores (human),", "and to a loved one's, correlated with empathy scores (human),")
# wang2018: the taste inputs to the amygdala assign valence
sub(E['gc'], 'summary', 'project to distinct parts of the amygdala, which assign taste valence (mouse),',
    'project to distinct parts of the amygdala, and these inputs assign taste valence (mouse),')
P.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('applied 4 fixes')
