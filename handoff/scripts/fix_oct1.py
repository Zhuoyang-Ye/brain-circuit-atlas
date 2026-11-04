#!/usr/bin/env python3
"""Octopus fix 1 (applied once): cite hochner2012 (it was not cited) with a sentence worded from its abstract."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
KP = ROOT / 'data/knowledge.json'
kb = json.loads(KP.read_text(encoding='utf-8'))
e = next(x for x in kb['entities'] if x['id'] == 'oct-arm-ns')
assert 'hochner2012' not in e['refs']
e['summary'] = e['summary'].rstrip() + " The arms' flexibility is argued to have shaped an embodied organization, in which intelligent behaviour emerges from the interplay of brain, body and environment (review)."
e['refs'].append('hochner2012')
KP.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('oct-arm-ns cites hochner2012')
