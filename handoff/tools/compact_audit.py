#!/usr/bin/env python3
"""Cloud substitute for compact_audit.py: print only the new or changed sentences in data/knowledge.json since an
old version, each item followed by the findings of the papers it cites (each finding printed once per item).

    python3 handoff/tools/compact_audit.py OLD [--region R] [--out FILE]

OLD is a knowledge.json path or a git revision (read as <rev>:data/knowledge.json). With --region, only items in
that region (bundle membership) or citing a paper tagged with it are printed. Chains and circuits have no refs of
their own; they are shown with the refs of their links.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser()
ap.add_argument('old')
ap.add_argument('--region')
ap.add_argument('--out')
a = ap.parse_args()

if pathlib.Path(a.old).exists():
    old = json.loads(pathlib.Path(a.old).read_text(encoding='utf-8'))
else:
    old = json.loads(subprocess.run(['git', '-C', str(ROOT), 'show', f'{a.old}:data/knowledge.json'],
                                    capture_output=True, text=True, check=True).stdout)
new = json.loads((ROOT / 'data/knowledge.json').read_text(encoding='utf-8'))
papers = {p['key']: p for p in json.loads((ROOT / 'data/papers.json').read_text(encoding='utf-8'))}
t = (ROOT / 'js/data/bundle.js').read_text(encoding='utf-8')
B = json.loads(t[t.index('=') + 1:].strip().rstrip(';'))

def flat(v):
    if isinstance(v, dict):
        return ' '.join(flat(x) for x in v.values())
    if isinstance(v, list):
        return ' '.join(flat(x) for x in v)
    return str(v or '')


split = lambda s: [x.strip() for x in re.split(r'(?<=[.;?!])\s+(?=[A-Z(])', flat(s)) if x.strip()]


def items(kb):
    """(kind, id) -> {'texts': {field: text}, 'refs': [...], 'links': [...]}"""
    out = {}
    lk = {f"{l['s']}>{l['t']}": l for l in kb['links']}
    for e in kb['entities']:
        out[('entity', e['id'])] = {'texts': {'name': e.get('name', ''), 'summary': e.get('summary', '')}, 'refs': e.get('refs', [])}
    for l in kb['links']:
        lid = f"{l['s']}>{l['t']}"
        out[('link', lid)] = {'texts': {'rel': l.get('rel', ''), 'note': l.get('note', ''), 'status': l.get('status', '')}, 'refs': l.get('refs', [])}
    for c in kb['chains']:
        refs = []
        for x, y in zip(c['nodes'], c['nodes'][1:]):
            refs += (lk.get(f'{x}>{y}') or lk.get(f'{y}>{x}') or {}).get('refs', [])
        out[('chain', c['id'])] = {'texts': {'name': c.get('name', ''), 'desc': c.get('desc', ''), 'nodes': ' → '.join(c['nodes'])}, 'refs': refs}
    for q in kb['questions']:
        out[('question', q['id'])] = {'texts': {'title': q.get('title', ''), 'text': q.get('text', ''), 'approaches': ' '.join(q.get('approaches', []))}, 'refs': q.get('refs', [])}
    for c in kb.get('atlas3d', {}).get('circuits', []):
        refs = [r for x in c.get('links', []) for r in lk.get(x, {}).get('refs', [])]
        out[('circuit', c['id'])] = {'texts': {'name': c.get('name', ''), 'desc': c.get('desc', '')}, 'refs': refs, 'region': c.get('region')}
    for r in kb['regions']:
        texts = {k: r.get(k, '') for k in ('label', 'intro')}
        texts.update({f'speciesNote.{k}': v for k, v in (r.get('speciesNote') or {}).items()})
        texts.update({f'levelDesc.{k}': v for k, v in (r.get('levelDesc') or {}).items()})
        out[('region', r['id'])] = {'texts': texts, 'refs': [], 'region': r['id']}
    return out


O, N = items(old), items(new)
reg = a.region
member = {}
if reg:
    for l in B['links']:
        member[('link', f"{l['s']}>{l['t']}")] = reg in l['regions']
    for c in B['chains']:
        member[('chain', c['id'])] = reg in c['regions']
    for q in B['questions']:
        member[('question', q['id'])] = reg in q['regions']
    for e in B['entities']:
        member[('entity', e['id'])] = e['id'] in B['regionEntities'][reg]

lines, n_items, n_sent = [], 0, 0
for key, it in N.items():
    was = O.get(key, {'texts': {}, 'refs': []})
    newsents = []
    for f, txt in it['texts'].items():
        oldsents = set(split(was['texts'].get(f, '')))
        for s in split(txt):
            if s not in oldsents:
                newsents.append((f, s))
    newrefs = [r for r in it['refs'] if r not in was['refs']]
    if not newsents and not newrefs:
        continue
    if reg and not (member.get(key) or it.get('region') == reg or any(reg in papers.get(r, {}).get('regions', []) for r in it['refs'])):
        continue
    n_items += 1
    n_sent += len(newsents)
    lines.append(f"\n=== {key[0]} {key[1]}" + (' (NEW)' if key not in O else ' (changed)'))
    for f, s in newsents:
        lines.append(f'  [{f}] {s}')
    if newrefs and key in O:
        lines.append(f'  new refs: {", ".join(newrefs)}')
    seen = set()
    for r in it['refs']:
        if r in seen:
            continue
        seen.add(r)
        p = papers.get(r)
        if not p:
            lines.append(f'    !! {r}: not in papers.json')
            continue
        lines.append(f"    - {r} ({', '.join(p.get('species', []))}; {p.get('evidence')}): {p.get('finding')}")
text = '\n'.join(lines) + f'\n\n{n_items} items, {n_sent} new sentences\n'
if a.out:
    pathlib.Path(a.out).write_text(text, encoding='utf-8')
    print(f'{n_items} items, {n_sent} new sentences → {a.out}')
else:
    sys.stdout.write(text)
