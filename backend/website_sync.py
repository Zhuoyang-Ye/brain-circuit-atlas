#!/usr/bin/env python3
"""
Brain Circuit Atlas - Website & Data Build Utilities
Rebuilds data bundles and assists in publishing to GitHub Pages / Cloudflare R2.
"""
import subprocess
import pathlib
import sys
import os

ROOT = pathlib.Path(__file__).resolve().parent.parent

def rebuild_static_bundle():
    """Runs tools/build.py --offline or standard build to regenerate js/data/bundle.js."""
    script = ROOT / 'tools' / 'build.py'
    res = subprocess.run([sys.executable, str(script), '--offline'], capture_output=True, text=True, cwd=str(ROOT))
    if res.returncode != 0:
        # Retry without offline if needed
        res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, cwd=str(ROOT))
    return {
        "success": res.returncode == 0,
        "stdout": res.stdout,
        "stderr": res.stderr
    }

def get_bundle_info():
    """Returns file stats for bundle.js and meshes."""
    bundle = ROOT / 'js' / 'data' / 'bundle.js'
    meshes_dir = ROOT / 'js' / 'data'
    mesh_files = list(meshes_dir.glob('meshes_*.js'))
    return {
        "bundle_size_bytes": bundle.stat().st_size if bundle.exists() else 0,
        "mesh_files": [{ "name": m.name, "size_bytes": m.stat().st_size } for m in mesh_files],
        "root": str(ROOT)
    }
