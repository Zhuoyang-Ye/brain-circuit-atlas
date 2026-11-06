#!/usr/bin/env python3
"""
Brain Circuit Atlas - SQLite Database Layer
Stores user hypotheses, research notes, bookmarks, and cached PubMed queries.
"""
import os
import sqlite3
import pathlib
import json
from datetime import datetime

def get_db_path():
    """Returns application data path in macOS Application Support, with fallback to local."""
    home = pathlib.Path.home()
    app_dir = home / 'Library' / 'Application Support' / 'BrainCircuitAtlas'
    try:
        app_dir.mkdir(parents=True, exist_ok=True)
        return str(app_dir / 'atlas.db')
    except Exception:
        # Fallback to current workspace
        return str(pathlib.Path(__file__).resolve().parent.parent / 'atlas_user.db')

class Database:
    def __init__(self, path=None):
        self.path = path or get_db_path()
        self.init_db()

    def get_conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS hypotheses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    region TEXT NOT NULL,
                    title TEXT NOT NULL,
                    summary TEXT,
                    chain_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id TEXT NOT NULL,
                    item_kind TEXT NOT NULL,
                    note TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS pubmed_cache (
                    term TEXT PRIMARY KEY,
                    count INTEGER NOT NULL,
                    cached_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
            """)

    # --- Hypotheses ---
    def list_hypotheses(self, region=None):
        with self.get_conn() as conn:
            if region:
                cur = conn.execute(
                    "SELECT * FROM hypotheses WHERE region = ? ORDER BY updated_at DESC", (region,)
                )
            else:
                cur = conn.execute("SELECT * FROM hypotheses ORDER BY updated_at DESC")
            return [dict(row) for row in cur.fetchall()]

    def save_hypothesis(self, region, title, summary, chain_json, hyp_id=None):
        now = datetime.utcnow().isoformat()
        with self.get_conn() as conn:
            if hyp_id:
                conn.execute(
                    """UPDATE hypotheses
                       SET region = ?, title = ?, summary = ?, chain_json = ?, updated_at = ?
                       WHERE id = ?""",
                    (region, title, summary, chain_json, now, hyp_id)
                )
                return hyp_id
            else:
                cur = conn.execute(
                    """INSERT INTO hypotheses (region, title, summary, chain_json, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (region, title, summary, chain_json, now, now)
                )
                return cur.lastrowid

    def delete_hypothesis(self, hyp_id):
        with self.get_conn() as conn:
            conn.execute("DELETE FROM hypotheses WHERE id = ?", (hyp_id,))
            return True

    # --- PubMed Caching ---
    def get_pubmed_count(self, term):
        with self.get_conn() as conn:
            cur = conn.execute("SELECT count FROM pubmed_cache WHERE term = ?", (term,))
            row = cur.fetchone()
            return row['count'] if row else None

    def set_pubmed_count(self, term, count):
        now = datetime.utcnow().isoformat()
        with self.get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO pubmed_cache (term, count, cached_at) VALUES (?, ?, ?)",
                (term, count, now)
            )

    # --- Settings (Cloudflare R2, etc.) ---
    def get_setting(self, key, default=None):
        with self.get_conn() as conn:
            cur = conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cur.fetchone()
            return row['value'] if row else default

    def set_setting(self, key, value):
        with self.get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, str(value))
            )
