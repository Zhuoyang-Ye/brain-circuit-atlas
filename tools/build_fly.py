#!/usr/bin/env python3
"""Build js/data/meshes_fly.js: the fruit-fly (Drosophila) brain for the 3D atlas, from Janelia FlyEM's male CNS.

    python3 tools/build_fly.py

The meshes are the neuropil regions of interest (ROIs) of the male CNS connectome (Berg et al., 2026, Cell;
male-cns.janelia.org), which the release licenses under CC-BY. They are served as neuroglancer legacy single-resolution
meshes (`<name>.ngmesh`: uint32 vertex count, float32 xyz vertices in nm, uint32 triangle indices) from the public
bucket gs://flyem-male-cns, and are cached in .cache/fly_malecns/ (gitignored) on the first run.

The structures are listed in data/meshes.json under "fly" (with "builder": "tools/build_fly.py"). Item fields:
  src     list of "<set>:<ROI name>", where <set> is a key of source.sets; "{s}" in a name stands for the side, L or R
  pair    true: one mesh per side, from the "(L)" and "(R)" ROIs, named "(left)" / "(right)" and tagged with their side
  faces   target triangle count after decimation (per mesh); smooth: Taubin smoothing iterations (default 5)
  pitch   voxel size in µm for remeshing (default 2): each ROI is voxelized, filled and re-surfaced by marching cubes,
          which gives a closed, smooth surface that decimates cleanly; opening: binary-opening iterations on the voxels,
          which trims thin protrusions such as the nerve roots of the nerve cord
  name, entity, related, group, note, tone: as in tools/build_meshes.py
  The first "shell" item is the brain surface that sets the scale; the nerve cord is a second shell, drawn as a faint
  outline so that it does not hide the brain.
Frame: in the male CNS volume x runs toward the fly's left, y ventral and z posterior. The scene has x to the right,
y dorsal and z anterior, so every axis is negated (and triangle winding reversed); the midline is the centre of the
central-brain ROI, and the brain (the shell) is scaled to the same longest extent as the other species.
Output: the bundle format of tools/build_meshes.py (label, credit, qs, bounds, anchors, spine, meshes). Needs numpy and
trimesh, scipy and scikit-image, like build_meshes.py.
"""
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

import numpy as np
import trimesh

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_meshes import EXTENT, b64, centroids, clean, simplify  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache' / 'fly_malecns'
OUT = ROOT / 'js' / 'data' / 'meshes_fly.js'


def fetch(spec, set_key, name):
    """Local path of one ROI mesh, downloaded from the release bucket if needed."""
    folder = CACHE / set_key
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'{name}.ngmesh'
    if not path.exists():
        url = spec['source']['url'].format(set=spec['source']['sets'][set_key], name=urllib.parse.quote(name + '.ngmesh'))
        print('  downloading', set_key, name)
        req = urllib.request.Request(url, headers={'User-Agent': 'brain-circuit-atlas'})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        tmp = path.with_suffix('.part')
        tmp.write_bytes(data)
        tmp.rename(path)
        time.sleep(0.3)
    return path


def read_ngmesh(path):
    b = path.read_bytes()
    n = int(np.frombuffer(b, '<u4', 1)[0])
    v = np.frombuffer(b, '<f4', 3 * n, 4).reshape(-1, 3).astype(float)
    f = np.frombuffer(b, '<u4', offset=4 + 12 * n).reshape(-1, 3).astype(np.int64)
    if f.max() >= n:
        raise ValueError(f'{path.name}: triangle index out of range')
    return v, f


def load(spec, srcs, side=None):
    """Merged raw mesh (nm, volume axes) of a list of "<set>:<name>" sources."""
    vs, fs, n = [], [], 0
    for s in srcs:
        set_key, name = s.split(':', 1)
        v, f = read_ngmesh(fetch(spec, set_key, name.replace('{s}', side or '')))
        vs.append(v)
        fs.append(f + n)
        n += len(v)
    return np.concatenate(vs), np.concatenate(fs)


def remesh(v, f, pitch_nm, opening=0, sigma=1.0):
    """Closed, smooth surface of a mesh's volume: voxelize, fill, optionally open, blur and run marching cubes."""
    from scipy import ndimage
    from skimage import measure
    grid = trimesh.Trimesh(v, f, process=False).voxelized(pitch_nm).fill()
    mat = grid.matrix
    if opening:
        mat = ndimage.binary_opening(mat, iterations=opening)
    field = ndimage.gaussian_filter(np.pad(mat.astype(np.float32), 3), sigma)
    vv, ff, _, _ = measure.marching_cubes(field, 0.5)
    vv = (vv - 3) @ grid.transform[:3, :3].T + grid.transform[:3, 3]
    return vv, ff.astype(np.int64)


def main():
    spec = json.loads((ROOT / 'data' / 'meshes.json').read_text(encoding='utf-8'))['fly']
    shell = next(it for it in spec['items'] if it['group'] == 'shell')
    mid = load(spec, spec['frame']['midline_from'])[0]
    midline = (mid[:, 0].min() + mid[:, 0].max()) / 2

    def to_scene(v):   # nm, volume axes -> µm, scene axes
        return np.column_stack([-(v[:, 0] - midline), -v[:, 1], -v[:, 2]]) / 1000.0

    sv = to_scene(load(spec, shell['src'])[0])
    lo, hi = sv.min(0), sv.max(0)
    center = (lo + hi) / 2
    center[0] = 0.0
    scale = EXTENT / (hi - lo).max()
    print(f'[fly] midline x = {midline:.0f} nm; brain {np.round(hi - lo, 1)} µm; scale {scale:.4f} / µm')

    meshes = []
    for it in spec['items']:
        for side in (('L', 'R') if it.get('pair') else (None,)):
            v, f = load(spec, it['src'], side)
            v, f = remesh(v, f, it.get('pitch', 2) * 1000.0, it.get('opening', 0))
            v = (to_scene(v) - center) * scale
            f = f[:, ::-1]   # three axes negated: keep the triangles facing outward
            v, f = simplify(v, f, it['faces'])
            v, f = clean(v, f, it.get('smooth', 5))
            rec = {k: it[k] for k in ('name', 'entity', 'related', 'group', 'note', 'tone') if k in it}
            rec['key'] = it['key'] + (f'-{side}' if side else '')
            if side:
                rec['side'] = side
                rec['name'] = f"{it['name']} ({'left' if side == 'L' else 'right'})"
                if (v[:, 0].mean() < 0) != (side == 'L'):
                    raise ValueError(f"{rec['key']}: mesh lies on the wrong side of the midline")
            rec['_v'], rec['_f'] = v, f
            rec['c'], rec['cl'], rec['cr'] = centroids(v)
            meshes.append(rec)
            print(f"  {rec['key']:<12} {len(f):>6} faces")

    def part(key, side):
        return next(m['_v'] for m in meshes if m['key'] == f'{key}-{side}')

    def sided(p):   # anchor record (centre, left, right) for a point given on the right (x > 0)
        p = np.asarray(p, float)
        return [[round(float(x), 3) for x in a] for a in (p * [0, 1, 1], p * [-1, 1, 1], p)]

    # Sensory neurons outside the brain, placed roughly (shown as approximate markers):
    la, al = part('la', 'R'), part('al', 'R')
    gng = np.vstack([m['_v'] for m in meshes if m['key'] == 'gng'])
    lat = la[la[:, 0] >= np.percentile(la[:, 0], 90)].mean(0)
    front = al[al[:, 2] >= np.percentile(al[:, 2], 90)].mean(0)
    low = gng[gng[:, 1] <= np.percentile(gng[:, 1], 10)].mean(0)
    anchors = {
        'fly-retina': sided(lat + [0.45, 0.0, 0.0]),            # photoreceptors: the compound eye, outside the lamina
        'fly-orn': sided(front + [0.35, -0.2, 0.9]),            # olfactory receptor neurons: the antenna, in front of the antennal lobe
        'fly-grn': sided([0.35, low[1] - 0.7, low[2] + 0.9]),   # gustatory receptor neurons: the proboscis, below and in front of the GNG
    }

    rmax = max(np.abs(m['_v']).max() for m in meshes)
    q = 32767.0 / rmax
    for m in meshes:
        v, f = m.pop('_v'), m.pop('_f')
        m['p'] = b64(np.round(v * q).astype('<i2'))
        m['i32'] = bool(len(v) > 65535)
        m['i'] = b64(f.astype('<u4' if m['i32'] else '<u2'))
        for k in ('c', 'cl', 'cr'):
            m[k] = [round(x, 3) for x in m[k]]
    bundle = {
        'label': spec['label'], 'credit': spec['credit'], 'qs': 1.0 / q,
        'bounds': [[round(float(x), 3) for x in (lo - center) * scale],
                   [round(float(x), 3) for x in (hi - center) * scale]],
        'anchors': anchors, 'spine': [], 'meshes': meshes,
    }
    OUT.write_text('window.CA_MESHES = window.CA_MESHES || {};\n'
                   f'window.CA_MESHES.fly = {json.dumps(bundle, separators=(",", ":"))};\n')
    print(f'  -> {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1e6:.2f} MB, {len(meshes)} meshes)')


if __name__ == '__main__':
    main()
