#!/usr/bin/env python3
"""Cloud substitute for regions_snapshot.py: per-region membership from js/data/bundle.js (run tools/build.py first).

    python3 handoff/tools/regions_snapshot.py out.json             # write a snapshot
    python3 handoff/tools/regions_snapshot.py --diff old.json new.json

The diff lists, per region, items lost (a loss in an earlier region is a bug) and items gained (check each is an
intended bridge, not a leak).
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def snapshot():
    t = (ROOT / 'js/data/bundle.js').read_text(encoding='utf-8')
    D = json.loads(t[t.index('=') + 1:].strip().rstrip(';'))
    out = {}
    for r in D['regions']:
        rid = r['id']
        out[rid] = {
            'entities': sorted(D['regionEntities'][rid]),
            'links': sorted(f"{l['s']}>{l['t']}" for l in D['links'] if rid in l['regions']),
            'chains': sorted(c['id'] for c in D['chains'] if rid in c['regions']),
            'questions': sorted(q['id'] for q in D['questions'] if rid in q['regions']),
            'papers': sorted(p['key'] for p in D['papers'] if rid in p['regions']),
        }
    return out


if sys.argv[1:2] == ['--diff']:
    a, b = (json.loads(pathlib.Path(p).read_text()) for p in sys.argv[2:4])
    lost = False
    for rid in b:
        if rid not in a:
            print(f'{rid}: new region ' + ', '.join(f'{k} {len(v)}' for k, v in b[rid].items()))
            continue
        for k in b[rid]:
            gone = sorted(set(a[rid][k]) - set(b[rid][k]))
            new = sorted(set(b[rid][k]) - set(a[rid][k]))
            if gone:
                lost = True
                print(f'{rid} LOST {k}: {gone}')
            if new:
                print(f'{rid} gained {k}: {new}')
    sys.exit(1 if lost else 0)
pathlib.Path(sys.argv[1]).write_text(json.dumps(snapshot(), indent=1))
print('wrote', sys.argv[1])
