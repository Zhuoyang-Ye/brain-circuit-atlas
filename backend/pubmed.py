#!/usr/bin/env python3
"""
Brain Circuit Atlas - PubMed & NCBI Utilities
Provides background caching, rate-limited queries, and fast local lookups.
"""
import urllib.request
import urllib.parse
import json
import time

ESEARCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'

def fetch_count(term, api_key=None):
    """Fetch count for a query term from NCBI E-Utilities."""
    params = {
        'db': 'pubmed',
        'rettype': 'count',
        'retmode': 'json',
        'tool': 'brain-circuit-atlas-backend',
        'term': term
    }
    if api_key:
        params['api_key'] = api_key

    url = f"{ESEARCH}?{urllib.parse.urlencode(params)}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'BrainCircuitAtlas/0.1'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return int(data.get('esearchresult', {}).get('count', 0))
        except Exception as e:
            if attempt == 2:
                raise e
            time.sleep(1.5 * (attempt + 1))
    return 0
