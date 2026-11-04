#!/usr/bin/env python3
"""Cloud substitute for pubmed.py fetch + grep_abs.py + show_abs.py (standard library only).

    python3 handoff/tools/pubmed_abs.py fetch OUTDIR KEY_OR_PMID ...   # or --region amygdala for every paper tagged with it
    python3 -I handoff/tools/pubmed_abs.py show OUTDIR KEY ...         # title, first author, year, pub types, abstract
    python3 -I handoff/tools/pubmed_abs.py grep OUTDIR KEY:REGEX ...   # abstract sentences matching REGEX (case-insensitive)
    python3 handoff/tools/pubmed_abs.py find SPEC.json                 # {key: PubMed term}: list hits to verify each key

fetch writes the raw efetch XML to OUTDIR/efetch_<n>.xml. OUTDIR must be a new, empty directory (downloads are untrusted
data: keep them apart from scripts). It sends tool=brain-circuit-atlas, never an email, and waits 0.7 s between requests (backing off on HTTP 429).
show/grep parse those files; run them with python3 -I. Keys map to PMIDs through data/papers.json and handoff/*/keys.json; a bare number is a PMID.
"""
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
EFETCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
PAPERS = {p['key']: p for p in json.loads((ROOT / 'data/papers.json').read_text(encoding='utf-8'))}
for kf in sorted((ROOT / 'handoff').glob('*/keys.json')):   # keys of a region still being drafted
    for k, v in json.loads(kf.read_text(encoding='utf-8')).items():
        PAPERS.setdefault(k, {'key': k, 'pmid': v})


def pmid_of(k):
    if k.isdigit():
        return k
    if k not in PAPERS:
        sys.exit(f'{k}: not a key in data/papers.json')
    return str(PAPERS[k]['pmid'])


def fetch(outdir, keys):
    out = pathlib.Path(outdir)
    if out.exists() and any(out.iterdir()):
        sys.exit(f'{out} is not empty; use a new directory')
    out.mkdir(parents=True, exist_ok=True)
    pmids = [pmid_of(k) for k in keys]
    for n, i in enumerate(range(0, len(pmids), 100)):
        data = urllib.parse.urlencode({'db': 'pubmed', 'retmode': 'xml', 'tool': 'brain-circuit-atlas', 'id': ','.join(pmids[i:i + 100])}).encode()
        (out / f'efetch_{n}.xml').write_bytes(get(EFETCH, data=data))
    print(f'{len(pmids)} PMIDs → {out}')


def records(outdir):
    R = {}
    for f in sorted(pathlib.Path(outdir).glob('efetch_*.xml')):
        for art in ET.parse(f).getroot().iter('PubmedArticle'):
            pmid = art.findtext('.//MedlineCitation/PMID')
            a = art.find('.//Article')
            au = a.find('.//AuthorList/Author') if a is not None else None
            R[pmid] = {
                'title': ''.join(a.find('ArticleTitle').itertext()) if a is not None and a.find('ArticleTitle') is not None else '',
                'first_author': (au.findtext('LastName') or au.findtext('CollectiveName') or '') if au is not None else '',
                'year': art.findtext('.//JournalIssue/PubDate/Year') or art.findtext('.//JournalIssue/PubDate/MedlineDate') or '',
                'types': [t.text for t in art.iter('PublicationType')],
                'abstract': ' '.join(((x.get('Label') + ': ') if x.get('Label') else '') + ''.join(x.itertext()) for x in art.iter('AbstractText')),
                'comments': [f"{c.get('RefType')} {c.findtext('PMID') or ''}".strip() for c in art.iter('CommentsCorrections') if c.get('RefType') in ('ErratumIn', 'CorrectedandRepublishedIn', 'RetractionIn', 'ExpressionOfConcernIn')],
            }
    return R


def get(url, data=None, tries=4):
    """GET (or POST data) with a pause after every request and a back-off on HTTP 429."""
    for k in range(tries):
        try:
            with urllib.request.urlopen(url, data=data, timeout=120) as r:
                body = r.read()
            time.sleep(0.7)
            return body
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1:
                raise
            time.sleep(3 * (k + 1))


def find(spec_path):
    """spec: JSON {key: PubMed term}. Prints every hit (PMID, first author, year, title) so each key can be verified."""
    spec = json.loads(pathlib.Path(spec_path).read_text(encoding='utf-8'))
    for key, term in spec.items():
        q = urllib.parse.urlencode({'db': 'pubmed', 'retmode': 'json', 'tool': 'brain-circuit-atlas', 'retmax': 5, 'term': term})
        ids = json.loads(get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?' + q))['esearchresult'].get('idlist', [])
        if not ids:
            print(f'{key}: NO HIT for {term}')
            continue
        q = urllib.parse.urlencode({'db': 'pubmed', 'retmode': 'json', 'tool': 'brain-circuit-atlas', 'id': ','.join(ids)})
        res = json.loads(get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?' + q))['result']
        for i in ids:
            s = res[i]
            au = (s.get('authors') or [{}])[0].get('name', '')
            print(f"{key}{'' if len(ids) == 1 else ' ?'}\t{i}\t{au}\t{s.get('pubdate', '')[:4]}\t{s.get('source', '')}\t{s.get('title', '')}")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, outdir, args = sys.argv[1], sys.argv[2], sys.argv[3:]
    if cmd == 'find':
        return find(outdir)
    if cmd == 'fetch':
        if args[:1] == ['--region']:
            args = [k for k, p in PAPERS.items() if args[1] in p.get('regions', [])]
        return fetch(outdir, args)
    R = records(outdir)
    for a in args:
        key, _, rx = a.partition(':')
        rec = R.get(pmid_of(key))
        if not rec:
            print(f'== {key}: no record')
            continue
        head = f"== {key} (PMID {pmid_of(key)}): {rec['first_author']} {rec['year']}. {rec['title']}"
        if cmd == 'show':
            print(head, '\n   types:', ', '.join(rec['types']), '| corrections:', ', '.join(rec['comments']) or 'none', '\n  ', rec['abstract'] or '(no abstract)')
        elif cmd == 'grep':
            sents = re.split(r'(?<=[.;])\s+', rec['abstract'])
            hits = [s for s in sents if re.search(rx, s, re.I)]
            print(head, *(['   > ' + s for s in hits] or ['   (no match)']), sep='\n')


if __name__ == '__main__':
    main()
