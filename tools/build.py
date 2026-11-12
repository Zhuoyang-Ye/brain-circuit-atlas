#!/usr/bin/env python3
"""
Build js/data/bundle.js from the curated data files.

    python3 tools/build.py              # fetch missing PubMed metadata, validate, write bundle
    python3 tools/build.py --offline    # use data/pubmed_cache.json only
    python3 tools/build.py --refresh    # re-fetch metadata for every PMID
    python3 tools/build.py --add 12345678 23456789
                                        # print papers.json templates for new PMIDs

Inputs:  data/papers.json     curated annotations (evidence type, levels, domains, finding, regions)
         data/knowledge.json  regions, entities, evidence-graded links, chains, questions, map overlays
         data/meshes.json     3D atlas catalog (only checked here)
         data/fly_connectivity.json  fly structural and functional connectivity (tools/build_fly_fc.py), if present
Output:  js/data/bundle.js    window.CA_DATA, loadable from file:// without a server

Bibliographic metadata comes from NCBI E-utilities (esummary). Set NCBI_API_KEY in the
environment to raise the rate limit. Standard library only (Python 3.8+).
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
CACHE = DATA / 'pubmed_cache.json'
OUT = ROOT / 'js' / 'data' / 'bundle.js'
CONNECTIVITY = {'fly': DATA / 'fly_connectivity.json'}   # region -> generated connectivity data for its Functional map
VIEW_IDS = {'atlas', 'map', 'circuit', 'molecules', 'scales', 'gaps', 'lab', 'library'}   # views registered in js/views/
ESUMMARY = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'


def esummary(pmids):
    """Fetch esummary records for a list of PMIDs; returns {pmid: record}."""
    out = {}
    for i in range(0, len(pmids), 150):
        params = {'db': 'pubmed', 'retmode': 'json', 'tool': 'brain-circuit-atlas', 'id': ','.join(pmids[i:i + 150])}
        if os.environ.get('NCBI_API_KEY'):
            params['api_key'] = os.environ['NCBI_API_KEY']
        data = urllib.parse.urlencode(params).encode()
        for attempt in range(3):
            try:
                with urllib.request.urlopen(ESUMMARY, data=data, timeout=60) as resp:
                    result = json.load(resp)['result']
                break
            except Exception as exc:  # network hiccup or 429
                if attempt == 2:
                    raise
                print(f'  retrying after error: {exc}', file=sys.stderr)
                time.sleep(2 * (attempt + 1))
        for uid in result.get('uids', []):
            out[uid] = simplify(result[uid])
        time.sleep(0.4)
    return out


def simplify(r):
    ids = {a['idtype']: a['value'] for a in r.get('articleids', [])}
    year = (r.get('sortpubdate') or r.get('pubdate') or '')[:4]
    return {
        'pmid': r['uid'],
        'authors': [a['name'] for a in r.get('authors', []) if a.get('authtype', 'Author') == 'Author'],
        'title': r.get('title', '').rstrip('.'),
        'journal': r.get('source', ''),
        'journalFull': r.get('fulljournalname', ''),
        'year': int(year) if year.isdigit() else None,
        'volume': r.get('volume', ''),
        'issue': r.get('issue', ''),
        'pages': r.get('pages', ''),
        'doi': ids.get('doi', ''),
        'pmc': ids.get('pmc', ''),
    }


def load_json(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


class Checker:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def validate(kb, papers, meshes, ck):
    levels = {l['id'] for l in kb['levels']}
    statuses = {s['id'] for s in kb['statuses']}
    evidence = {e['id'] for e in kb['evidence']}
    domains = {d['id'] for d in kb['domains']}
    regions = kb.get('regions') or []
    region_ids = {r.get('id') for r in regions}
    if not regions or None in region_ids or len(region_ids) != len(regions):
        ck.err('knowledge.json needs a regions list with unique ids')
    keys, paper_regions = set(), {}
    for p in papers:
        k = p.get('key')
        if not k or k in keys:
            ck.err(f'paper key missing or duplicated: {k!r}')
        keys.add(k)
        if not p.get('pmid') and not p.get('manual'):
            ck.err(f'{k}: needs a pmid or manual citation')
        if p.get('evidence') not in evidence:
            ck.err(f"{k}: unknown evidence type {p.get('evidence')!r}")
        for l in p.get('levels', []):
            if l not in levels:
                ck.err(f'{k}: unknown level {l!r}')
        for d in p.get('domains', []):
            if d not in domains:
                ck.err(f'{k}: unknown domain {d!r}')
        if not p.get('finding'):
            ck.err(f'{k}: missing finding')
        prs = p.get('regions')
        if not prs or any(r not in region_ids for r in prs):
            ck.err(f'{k}: regions must list known region ids, got {prs!r}')
        paper_regions[k] = set(prs or [])

    def refs_ok(where, refs):
        for r in refs or []:
            if r not in keys:
                ck.err(f'{where}: unknown reference {r!r}')

    ents = {}
    for e in kb['entities']:
        if e['id'] in ents:
            ck.err(f"duplicate entity {e['id']}")
        ents[e['id']] = e
        if e.get('level') not in levels:
            ck.err(f"{e['id']}: unknown level {e.get('level')!r}")
        for d in e.get('domains', []):
            if d not in domains:
                ck.err(f"{e['id']}: unknown domain {d!r}")
        refs_ok(e['id'], e.get('refs'))
        if e.get('region') and e['region'] not in region_ids:
            ck.err(f"{e['id']}: unknown region {e['region']!r}")
        elif e.get('region'):
            for r in e.get('refs', []):
                if r in paper_regions and e['region'] not in paper_regions[r]:
                    ck.warn(f"{e['id']} (region {e['region']}) cites {r}, which is not tagged with that region")

    for r in regions:
        rid = r.get('id')
        for f in ('label', 'query', 'entity', 'view', 'views', 'intro'):
            if not r.get(f):
                ck.err(f'region {rid}: missing {f}')
        if r.get('entity') and r['entity'] not in ents:
            ck.err(f"region {rid}: unknown entity {r['entity']!r}")
        for v in r.get('views', []):
            if v not in VIEW_IDS:
                ck.err(f'region {rid}: unknown view {v!r}')
        for f in ('levelDesc', 'levelQueries', 'methods'):
            for l in r.get(f, {}):
                if l not in levels:
                    ck.err(f'region {rid}: {f} has unknown level {l!r}')
        # a condition (ADHD) is a profile across regions: listed in the Condition menu, not the Region menu
        if r.get('kind') not in (None, 'condition'):
            ck.err(f"region {rid}: kind must be 'condition' or left out, got {r.get('kind')!r}")
    if regions and regions[0].get('kind') == 'condition':
        ck.err('the first entry of regions must be a brain region, not a condition')

    link_ids = set()
    degree = {i: 0 for i in ents}
    for l in kb['links']:
        lid = f"{l['s']}>{l['t']}"
        if lid in link_ids:
            ck.err(f'duplicate link {lid}')
        link_ids.add(lid)
        for end in (l['s'], l['t']):
            if end not in ents:
                ck.err(f'{lid}: unknown entity {end!r}')
            else:
                degree[end] += 1
        if l.get('status') not in statuses or l.get('status') == 'gap':
            ck.err(f"{lid}: invalid status {l.get('status')!r}")
        if not l.get('refs'):
            ck.warn(f'{lid}: no references')
        refs_ok(lid, l.get('refs'))
    for i, n in degree.items():
        if n == 0:
            ck.warn(f'entity {i} has no links')

    for c in kb['chains']:
        for n in c['nodes']:
            if n not in ents:
                ck.err(f"chain {c['id']}: unknown entity {n!r}")
        for a, b in zip(c['nodes'], c['nodes'][1:]):
            if f'{a}>{b}' not in link_ids and f'{b}>{a}' not in link_ids:
                ck.warn(f"chain {c['id']}: no link between {a} and {b} (shown as a gap)")
    for q in kb['questions']:
        for n in q['entities']:
            if n not in ents:
                ck.err(f"question {q['id']}: unknown entity {n!r}")
        refs_ok(q['id'], q.get('refs'))

    fm = kb['flatmap']
    for b in fm['bands']:
        for k in ('entity', 'vermis'):
            if b.get(k) and b[k] not in ents:
                ck.err(f"flatmap band {b['id']}: unknown entity {b[k]!r}")
    for o in fm['overlays']:
        refs_ok(f"overlay {o['id']}", o['refs'])
        if o.get('domain') not in domains:
            ck.err(f"overlay {o['id']}: unknown domain")
    refs_ok('flatmap', fm.get('refs'))
    refs_ok('lesion overlay', fm['lesion']['refs'])
    for c in fm['lesion']['cats'].values():
        if c.get('entity') and c['entity'] not in ents:
            ck.err(f"lesion category: unknown entity {c['entity']!r}")

    a3 = kb['atlas3d']
    # atlas3d.species lists the 3D brains the site offers; dropping one switches it off (for example, if its atlas licence forbids reuse)
    offered = a3.get('species') or []
    if not offered:
        ck.err('atlas3d.species: list the species the 3D atlas offers')
    for sp in offered:
        if sp not in meshes:
            ck.err(f'atlas3d.species: {sp!r} has no entry in meshes.json')
        elif not (ROOT / 'js' / 'data' / f'meshes_{sp}.js').exists():
            ck.warn(f'atlas3d.species: js/data/meshes_{sp}.js is missing (run tools/build_meshes.py {sp})')
    for f in sorted((ROOT / 'js' / 'data').glob('meshes_*.js')):
        if f.stem[len('meshes_'):] not in offered:
            rel = f.relative_to(ROOT)
            ck.warn(f'{rel} is switched off in atlas3d.species but still in the repo, so the site would still publish it: git rm {rel}')
    for side, ids in a3['sides'].items():
        for i in ids:
            if i not in ents:
                ck.err(f'atlas3d side {side}: unknown entity {i!r}')
    for sp, amap in a3['aliases'].items():
        for a, b in amap.items():
            if a not in ents or b not in ents:
                ck.err(f'atlas3d alias {sp}: {a} -> {b} unknown')
    for parent, kids in a3.get('composite', {}).items():
        if parent not in ents or not kids or any(k not in ents for k in kids):
            ck.err(f'atlas3d composite {parent}: unknown entity in {kids!r}')
    for c in a3['circuits']:
        if c.get('region') not in region_ids:
            ck.err(f"3D circuit {c['id']}: unknown region {c.get('region')!r}")
        for lid in c['links']:
            if lid not in link_ids:
                ck.err(f"3D circuit {c['id']}: link {lid} not in knowledge base")
        for i in c.get('focus', []):   # structures lit up without a pathway
            if i not in ents:
                ck.err(f"3D circuit {c['id']}: focus names unknown entity {i!r}")
        if not c['links'] and not c.get('focus'):
            ck.err(f"3D circuit {c['id']}: needs links or focus")

    # neuromodulator matrix, and the optional transmitter / receptor / sign fields on links
    nm = kb.get('neuromodulation', {})
    for t in nm.get('targets', []):
        if t['id'] not in ents:
            ck.err(f"neuromodulation target: unknown entity {t['id']!r}")
    for g in nm.get('groups', []):
        for r in g['rows']:
            if r not in ents:
                ck.err(f"neuromodulation group {g['label']!r}: unknown entity {r!r}")
    for code, v in nm.get('tx', {}).items():
        if v.get('entity') not in ents:
            ck.err(f"neuromodulation tx {code}: unknown entity {v.get('entity')!r}")
    for i in nm.get('sources', []):
        if i not in ents:
            ck.err(f'neuromodulation source: unknown entity {i!r}')
    for l in kb['links']:
        lid = f"{l['s']}>{l['t']}"
        if 'tx' in l and l['tx'] not in nm.get('tx', {}):
            ck.err(f"{lid}: unknown transmitter code {l['tx']!r}")
        if 'sign' in l and l['sign'] not in nm.get('signs', {}):
            ck.err(f"{lid}: unknown sign {l['sign']!r}")
        if 'via' in l and not (isinstance(l['via'], str) and l['via']):
            ck.err(f'{lid}: via must be a non-empty string')

    # region-specific versions of the Functional map, Microcircuit and Cells & molecules views
    rv_refs = []
    for rid, views in kb.get('regionViews', {}).items():
        if rid not in region_ids:
            ck.err(f'regionViews: unknown region {rid!r}')
            continue
        reg = next(r for r in regions if r['id'] == rid)
        for v, cfg in views.items():
            if v not in VIEW_IDS or v not in reg.get('views', []):
                ck.err(f'regionViews {rid}: view {v!r} is not one of the region\'s views')
            rv_refs += cfg.get('refs', [])
            refs_ok(f'regionViews {rid}/{v}', cfg.get('refs'))
            if v == 'map':
                conn_path = CONNECTIVITY.get(rid)
                conn = load_json(conn_path) if conn_path and conn_path.exists() else None
                grouped = [x for g in cfg.get('groups', []) for x in g['regions']]
                if len(set(grouped)) != len(grouped):
                    ck.err(f'regionViews {rid}/map: a region is in two groups')
                if conn is None:
                    ck.warn(f'regionViews {rid}/map: no connectivity data (run tools/build_fly_fc.py)')
                elif set(grouped) != set(conn['regions']):
                    ck.err(f'regionViews {rid}/map: groups do not cover the connectivity regions exactly')
                for name, info in cfg.get('regions', {}).items():
                    if name not in grouped:
                        ck.err(f'regionViews {rid}/map: region {name!r} is in no group')
                    for e in info.get('entities', []):
                        if e not in ents:
                            ck.err(f'regionViews {rid}/map region {name}: unknown entity {e!r}')
            nmx = cfg.get('neuromodulation')
            if nmx:
                for t in nmx.get('targets', []):
                    if t['id'] not in ents:
                        ck.err(f"regionViews {rid}/{v} neuromodulation target: unknown entity {t['id']!r}")
                for g in nmx.get('groups', []):
                    for r in g['rows']:
                        if r not in ents:
                            ck.err(f"regionViews {rid}/{v} neuromodulation row: unknown entity {r!r}")

    for sp, spec in meshes.items():
        for it in spec['items']:
            for k in ('entity', 'related'):
                if it.get(k) and it[k] not in ents:
                    ck.err(f"meshes.json {sp}/{it['key']}: unknown {k} {it[k]!r}")

    cited = set()
    for e in kb['entities']:
        cited.update(e.get('refs', []))
    for l in kb['links']:
        cited.update(l.get('refs', []))
    for q in kb['questions']:
        cited.update(q.get('refs', []))
    cited.update(fm.get('refs', []))
    cited.update(rv_refs)
    for o in fm['overlays']:
        cited.update(o['refs'])
    for k in keys - cited:
        ck.warn(f'paper {k} is not cited by any entity or link')


def derive_regions(kb, papers):
    """Region membership, computed for the bundle (not stored in the data files).

    Untagged entities are shared between regions. A link belongs to the regions of its region-tagged
    endpoints and to the regions that all its papers share (else to every region they name). A chain or
    question belongs to the regions of its tagged entities (else of its links or papers). A region's
    entities are its tagged ones plus those its links, chains and questions use."""
    order = [r['id'] for r in kb['regions']]
    ordered = lambda s: [r for r in order if r in s] or list(order)
    preg = {p['key']: set(p['regions']) for p in papers}
    ereg = {e['id']: e['region'] for e in kb['entities'] if e.get('region')}

    def from_papers(refs):
        sets = [preg[r] for r in refs or [] if r in preg]
        return set.intersection(*sets) or set.union(*sets) if sets else set()

    links = []
    for l in kb['links']:
        s = {ereg[x] for x in (l['s'], l['t']) if x in ereg} | from_papers(l.get('refs'))
        links.append(dict(l, regions=ordered(s)))
    lreg = {f"{l['s']}>{l['t']}": set(l['regions']) for l in links}
    chains = []
    for c in kb['chains']:
        s = {ereg[n] for n in c['nodes'] if n in ereg}
        for a, b in ([] if s else zip(c['nodes'], c['nodes'][1:])):
            s |= lreg.get(f'{a}>{b}', set()) | lreg.get(f'{b}>{a}', set())
        chains.append(dict(c, regions=ordered(s)))
    questions = [dict(q, regions=ordered({ereg[n] for n in q['entities'] if n in ereg} or from_papers(q.get('refs'))))
                 for q in kb['questions']]
    members = {r: {i for i, x in ereg.items() if x == r} for r in order}
    for items, nodes in ((links, lambda l: (l['s'], l['t'])), (chains, lambda c: c['nodes']), (questions, lambda q: q['entities'])):
        for it in items:
            for r in it['regions']:
                members[r].update(nodes(it))
    ids = [e['id'] for e in kb['entities']]
    return links, chains, questions, {r: [i for i in ids if i in members[r]] for r in order}


def add_templates(pmids):
    recs = esummary(pmids)
    for pm in pmids:
        r = recs.get(pm)
        if not r:
            print(f'// {pm}: not found', file=sys.stderr)
            continue
        last = re.sub(r'[^a-z]', '', (r['authors'][0].split()[0] if r['authors'] else 'anon').lower())
        tmpl = {'key': f"{last}{r['year']}", 'pmid': pm, 'evidence': 'observational', 'species': ['mouse'],
                'methods': [], 'levels': [], 'domains': [], 'finding': ''}
        print(f"// {r['authors'][0] if r['authors'] else ''} {r['year']} {r['journal']}: {r['title']}")
        print(json.dumps(tmpl, ensure_ascii=False) + ',')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--offline', action='store_true', help='do not contact NCBI')
    ap.add_argument('--refresh', action='store_true', help='re-fetch all PubMed metadata')
    ap.add_argument('--add', nargs='+', metavar='PMID', help='print templates for new papers and exit')
    args = ap.parse_args()

    if args.add:
        add_templates(args.add)
        return

    kb = load_json(DATA / 'knowledge.json')
    papers = load_json(DATA / 'papers.json')
    meshes = load_json(DATA / 'meshes.json')
    cache = load_json(CACHE) if CACHE.exists() else {}

    pmids = [p['pmid'] for p in papers if p.get('pmid')]
    todo = pmids if args.refresh else [p for p in pmids if p not in cache]
    if todo and not args.offline:
        print(f'fetching {len(todo)} records from PubMed ...')
        cache.update(esummary(todo))
        CACHE.write_text(json.dumps(cache, indent=1, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')

    ck = Checker()
    validate(kb, papers, meshes, ck)

    out_papers = []
    for p in papers:
        meta = dict(p.get('manual') or {})
        if p.get('pmid'):
            if p['pmid'] in cache:
                meta = cache[p['pmid']]
            else:
                ck.warn(f"{p['key']}: no PubMed metadata for {p['pmid']} (run without --offline)")
        rec = {k: v for k, v in p.items() if k != 'manual'}
        rec.update({
            'authors': meta.get('authors', []),
            'title': meta.get('title', p['key']),
            'journal': meta.get('journal', ''),
            'year': meta.get('year'),
            'volume': meta.get('volume', ''),
            'pages': meta.get('pages', ''),
            'doi': meta.get('doi', ''),
            'pmc': meta.get('pmc', ''),
        })
        out_papers.append(rec)

    for w in ck.warnings:
        print('warning:', w)
    if ck.errors:
        for e in ck.errors:
            print('ERROR:', e, file=sys.stderr)
        sys.exit(f'{len(ck.errors)} error(s); bundle not written')

    bundle = dict(kb)
    bundle['papers'] = out_papers
    bundle['links'], bundle['chains'], bundle['questions'], bundle['regionEntities'] = derive_regions(kb, papers)
    bundle['mesh3d'] = {sp: {'label': spec['label'], 'credit': spec['credit'],
                             'entities': sorted({it['entity'] for it in spec['items'] if it.get('entity')})}
                        for sp, spec in meshes.items() if sp in kb['atlas3d']['species']}
    bundle['connectivity'] = {rid: load_json(path) for rid, path in CONNECTIVITY.items() if path.exists()}
    bundle['built'] = datetime.date.today().isoformat()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('/* generated by tools/build.py; edit data/*.json instead */\n'
                   'window.CA_DATA = ' + json.dumps(bundle, ensure_ascii=False, separators=(',', ':')) + ';\n',
                   encoding='utf-8')
    print(f"wrote {OUT.relative_to(ROOT)}: {len(kb['entities'])} entities, {len(kb['links'])} links, "
          f"{len(out_papers)} papers ({OUT.stat().st_size / 1024:.0f} KB)")
    for r in kb['regions']:
        rid = r['id']
        print(f"  {r['label']}: {len(bundle['regionEntities'][rid])} entities, "
              f"{sum(rid in l['regions'] for l in bundle['links'])} links, {sum(rid in p['regions'] for p in out_papers)} papers")


if __name__ == '__main__':
    main()
