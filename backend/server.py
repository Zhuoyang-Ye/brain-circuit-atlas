#!/usr/bin/env python3
"""
Brain Circuit Atlas - Local Application & API Server
Serves static web assets and provides local SQLite & Cloudflare R2 endpoints.
Standard library only (no pip dependencies required).
"""
import http.server
import json
import os
import pathlib
import sys
import urllib.parse
from http import HTTPStatus

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from db import Database
from r2 import CloudflareR2
from pubmed import fetch_count
from website_sync import rebuild_static_bundle, get_bundle_info

db = Database()

def get_r2_client():
    account_id = db.get_setting('r2_account_id', os.environ.get('R2_ACCOUNT_ID', ''))
    access_key = db.get_setting('r2_access_key', os.environ.get('R2_ACCESS_KEY', ''))
    secret_key = db.get_setting('r2_secret_key', os.environ.get('R2_SECRET_KEY', ''))
    bucket = db.get_setting('r2_bucket', os.environ.get('R2_BUCKET', ''))
    pub_url = db.get_setting('r2_public_url', os.environ.get('R2_PUBLIC_URL', ''))
    return CloudflareR2(account_id, access_key, secret_key, bucket, pub_url)

class AtlasRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        # Enable CORS for local desktop & web development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()

    def send_json(self, data, status=HTTPStatus.OK):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self):
        content_len = int(self.headers.get('Content-Length', 0))
        if content_len == 0:
            return {}
        raw = self.rfile.read(content_len)
        return json.loads(raw.decode('utf-8'))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API routing
        if path == '/api/status':
            r2 = get_r2_client()
            return self.send_json({
                "status": "ok",
                "app": "Brain Circuit Atlas",
                "version": "0.1.0",
                "database": db.path,
                "r2_configured": r2.is_configured(),
                "r2_bucket": r2.bucket_name if r2.is_configured() else None,
                "bundle_info": get_bundle_info()
            })

        if path == '/api/hypotheses':
            region = query.get('region', [None])[0]
            return self.send_json(db.list_hypotheses(region))

        if path == '/api/pubmed/count':
            term = query.get('term', [''])[0]
            if not term:
                return self.send_json({"error": "Missing 'term' parameter"}, status=HTTPStatus.BAD_REQUEST)
            
            # Check SQLite cache first
            cached = db.get_pubmed_count(term)
            if cached is not None:
                return self.send_json({"term": term, "count": cached, "cached": True})
            
            # Otherwise query NCBI
            try:
                count = fetch_count(term)
                db.set_pubmed_count(term, count)
                return self.send_json({"term": term, "count": count, "cached": False})
            except Exception as e:
                return self.send_json({"error": str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        if path == '/api/r2/config':
            r2 = get_r2_client()
            return self.send_json({
                "account_id": r2.account_id,
                "access_key_id": r2.access_key_id,
                "secret_key_masked": ("*" * 12 + r2.secret_access_key[-4:]) if r2.secret_access_key else "",
                "bucket_name": r2.bucket_name,
                "public_url": r2.public_url or "",
                "configured": r2.is_configured()
            })

        # Default to static file serving
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/api/hypotheses':
            data = self.read_json_body()
            region = data.get('region', 'cerebellum')
            title = data.get('title', 'Untitled Hypothesis')
            summary = data.get('summary', '')
            chain_json = json.dumps(data.get('chain', []))
            hyp_id = data.get('id')
            saved_id = db.save_hypothesis(region, title, summary, chain_json, hyp_id)
            return self.send_json({"ok": True, "id": saved_id})

        if path == '/api/r2/config':
            data = self.read_json_body()
            if 'account_id' in data: db.set_setting('r2_account_id', data['account_id'])
            if 'access_key_id' in data: db.set_setting('r2_access_key', data['access_key_id'])
            if 'secret_access_key' in data and data['secret_access_key']:
                db.set_setting('r2_secret_key', data['secret_access_key'])
            if 'bucket_name' in data: db.set_setting('r2_bucket', data['bucket_name'])
            if 'public_url' in data: db.set_setting('r2_public_url', data['public_url'])
            return self.send_json({"ok": True, "configured": get_r2_client().is_configured()})

        if path == '/api/r2/test':
            r2 = get_r2_client()
            res = r2.test_connection()
            return self.send_json(res)

        if path == '/api/r2/sync_meshes':
            r2 = get_r2_client()
            if not r2.is_configured():
                return self.send_json({"ok": False, "message": "R2 not configured"}, status=HTTPStatus.BAD_REQUEST)
            meshes_dir = ROOT / 'js' / 'data'
            uploaded = []
            for mf in meshes_dir.glob('meshes_*.js'):
                res = r2.upload_file(str(mf), remote_key=f"data/{mf.name}")
                uploaded.append(res)
            return self.send_json({"ok": True, "uploaded": uploaded})

        if path == '/api/website/rebuild':
            res = rebuild_static_bundle()
            return self.send_json(res)

        self.send_error(HTTPStatus.NOT_FOUND, "API route not found")

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith('/api/hypotheses/'):
            hyp_id = int(path.split('/')[-1])
            db.delete_hypothesis(hyp_id)
            return self.send_json({"ok": True, "deleted": hyp_id})
        self.send_error(HTTPStatus.NOT_FOUND, "API route not found")

def run(port=8765):
    server_address = ('127.0.0.1', port)
    httpd = http.server.ThreadingHTTPServer(server_address, AtlasRequestHandler)
    print(f"Brain Circuit Atlas backend running at http://127.0.0.1:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    run(port)
