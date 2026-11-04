#!/usr/bin/env python3
"""Cloud substitute for readme_counts.py: rewrite the README's region table, the totals sentence, and the
all-region counts in the Across scales and Library rows, from js/data/bundle.js (run tools/build.py first).

    python3 handoff/tools/readme_counts.py          # rewrite README.md in place and print the table
    python3 handoff/tools/readme_counts.py --check  # print only; exit 1 if README.md is out of date
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
t = (ROOT / 'js/data/bundle.js').read_text(encoding='utf-8')
D = json.loads(t[t.index('=') + 1:].strip().rstrip(';'))

rows = ['| Region | Entities | Links | Chains | Open questions | Papers |', '| --- | ---: | ---: | ---: | ---: | ---: |']
for r in D['regions']:
    rid = r['id']
    n = lambda xs: sum(rid in x['regions'] for x in xs)
    rows.append(f"| {r['label']} | {len(D['regionEntities'][rid])} | {n(D['links'])} | {n(D['chains'])} | {n(D['questions'])} | {n(D['papers'])} |")
table = '\n'.join(rows)
E, L, C, Q, P = (len(D[k]) for k in ('entities', 'links', 'chains', 'questions', 'papers'))
totals = f'The totals are {E} entities, {L} links, {C} chains, {Q} open questions and {P} papers.'

readme = (ROOT / 'README.md').read_text(encoding='utf-8')
new = re.sub(r'\| Region \| Entities \|[^\n]*\n\| --- [^\n]*\n(?:\|[^\n]*\n)+', table + '\n', readme, count=1)
new = re.sub(r'The totals are \d+ entities, \d+ links, \d+ chains, \d+ open questions and \d+ papers\.', totals, new, count=1)
new = re.sub(r'\(all regions together: \d+ entities, \d+ links, \d+ chains\)', f'(all regions together: {E} entities, {L} links, {C} chains)', new, count=1)
new = re.sub(r"The region's papers \(\d+ in all\)", f"The region's papers ({P} in all)", new, count=1)

print(table)
print(totals)
if '--check' in sys.argv:
    sys.exit(0 if new == readme else 1)
if new != readme:
    (ROOT / 'README.md').write_text(new, encoding='utf-8')
    print('README.md updated')
else:
    print('README.md already up to date')
