#!/usr/bin/env python3
"""Build js/data/meshes_octopus.js: a schematic octopus brain for the 3D atlas.

    python3 tools/build_octopus.py

No octopus atlas volume or labelled mesh is available to this project, so the octopus is drawn as a schematic: each lobe
is an ellipsoid and the arms are tapered tubes, placed by hand from the textbook layout of the central brain (the
supra-oesophageal mass above the oesophagus, the sub-oesophageal mass below it, the optic lobes at the sides with the
peduncle complex on the optic tracts, the eyes outside them and the arms around the mouth). Shapes, sizes and positions
are for orientation only, and every structure is flagged `approx`, so the site labels it in italics with ≈.

The shapes are listed in data/meshes.json under "octopus" (with "schematic": true). Item fields:
  shape      "ellipsoid" (default), "tube", "arms" or "suckers"
  center     [x, y, z] and radii [a, b, c] for an ellipsoid; x is left (-) to right (+), y ventral to dorsal, z posterior to
             anterior, in the same frame and scale as the other species' meshes
  mirror     true: draw a left and a right copy (x and -x), named "(left)" and "(right)" and tagged with their side
  points     for a tube: a polyline; radius: a number or [start, end]
  arms       n, crown (centre of the arm crown), axis (direction the arms leave in), ring (radius of the arm bases), length,
             radius [base, tip]
  suckers    of: the key of an "arms" item; per_arm: suckers on each arm, on its oral (inner) side
Output: the same bundle format as tools/build_meshes.py (label, credit, qs, bounds, anchors, spine, meshes), standard
library only.
"""
import base64
import json
import math
import pathlib
import struct

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'js' / 'data' / 'meshes_octopus.js'


def add(a, b): return [a[i] + b[i] for i in range(3)]
def sub(a, b): return [a[i] - b[i] for i in range(3)]
def mul(a, k): return [x * k for x in a]
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def norm(a):
    n = math.sqrt(dot(a, a)) or 1.0
    return [x / n for x in a]


def ellipsoid(center, radii, nu=28, nv=18):
    v, f = [], []
    for j in range(nv + 1):
        th = math.pi * j / nv
        for i in range(nu):
            ph = 2 * math.pi * i / nu
            v.append([center[0] + radii[0] * math.sin(th) * math.cos(ph), center[1] + radii[1] * math.cos(th),
                      center[2] + radii[2] * math.sin(th) * math.sin(ph)])
    for j in range(nv):
        for i in range(nu):
            a, b = j * nu + i, j * nu + (i + 1) % nu
            c, d = a + nu, b + nu
            f += [[a, c, b], [b, c, d]]
    return v, f


def tube(points, r0, r1, sides=10, steps_per_seg=6):
    """A tapered tube along a polyline (Catmull-Rom smoothed), with parallel-transported rings and closed ends."""
    pts = [points[0]] + points + [points[-1]]
    path = []
    for k in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[k - 1], pts[k], pts[k + 1], pts[k + 2]
        for s in range(steps_per_seg):
            t = s / steps_per_seg
            path.append([0.5 * ((2 * p1[i]) + (-p0[i] + p2[i]) * t + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t * t
                                + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t ** 3) for i in range(3)])
    path.append(points[-1])
    tang = [norm(sub(path[min(i + 1, len(path) - 1)], path[max(i - 1, 0)])) for i in range(len(path))]
    ref = [0, 0, 1] if abs(tang[0][2]) < 0.9 else [1, 0, 0]
    n = norm(cross(tang[0], ref))
    v, f = [], []
    for i, p in enumerate(path):
        if i:
            n = norm(sub(n, mul(tang[i], dot(n, tang[i]))))   # parallel transport
        b = cross(tang[i], n)
        r = r0 + (r1 - r0) * i / (len(path) - 1)
        for s in range(sides):
            a = 2 * math.pi * s / sides
            v.append(add(p, add(mul(n, r * math.cos(a)), mul(b, r * math.sin(a)))))
    for i in range(len(path) - 1):
        for s in range(sides):
            a, b2 = i * sides + s, i * sides + (s + 1) % sides
            f += [[a, a + sides, b2], [b2, a + sides, b2 + sides]]
    for end, ring in ((path[0], 0), (path[-1], len(path) - 1)):   # caps
        v.append(end)
        c = len(v) - 1
        for s in range(sides):
            a, b2 = ring * sides + s, ring * sides + (s + 1) % sides
            f.append([c, b2, a] if ring == 0 else [c, a, b2])
    return v, f


def arm_paths(it):
    """Centre lines of the arms: each leaves the crown along `axis`, spreads outward and curls slightly at the tip."""
    axis = norm(it['axis'])
    u = norm(cross(axis, [1, 0, 0] if abs(axis[0]) < 0.9 else [0, 1, 0]))
    w = cross(axis, u)
    out = []
    for k in range(it['n']):
        a = 2 * math.pi * (k + 0.5) / it['n']
        radial = add(mul(u, math.cos(a)), mul(w, math.sin(a)))
        base = add(it['crown'], mul(radial, it['ring']))
        pts = []
        for s in range(9):
            t = s / 8
            spread = it['length'] * (0.55 * t + 0.25 * t * t)
            drop = it['length'] * (0.75 * t - 0.2 * t * t)
            curl = it['length'] * 0.12 * t ** 3
            pts.append(add(base, add(mul(radial, spread - curl), mul(axis, drop + curl))))
        out.append((pts, radial))
    return out


def merge(parts):
    v, f = [], []
    for pv, pf in parts:
        off = len(v)
        v += pv
        f += [[a + off, b + off, c + off] for a, b, c in pf]
    return v, f


def centroids(v):
    mean = lambda vs: [sum(p[i] for p in vs) / len(vs) for i in range(3)]
    c = mean(v)
    left, right = [p for p in v if p[0] < 0], [p for p in v if p[0] > 0]
    return [c, mean(left) if left else c, mean(right) if right else c]


def shapes(it, items):
    """Yield (key, name, side, vertices, faces) for one item of the spec."""
    kind = it.get('shape', 'ellipsoid')
    if kind == 'arms':
        for k, (pts, _) in enumerate(arm_paths(it)):
            v, f = tube(pts, it['radius'][0], it['radius'][1], sides=12)
            yield f"{it['key']}{k + 1}", f"{it['name']} {k + 1}", '', v, f
        return
    if kind == 'suckers':
        arms = items[it['of']]
        parts = []
        for pts, radial in arm_paths(arms):
            n = it['per_arm']
            for s in range(n):
                t = 0.08 + 0.84 * s / (n - 1)
                seg = t * (len(pts) - 1)
                i0 = min(int(seg), len(pts) - 2)
                p = add(pts[i0], mul(sub(pts[i0 + 1], pts[i0]), seg - i0))
                r_arm = arms['radius'][0] + (arms['radius'][1] - arms['radius'][0]) * t
                centre = sub(p, mul(radial, r_arm * 0.85))   # on the oral side, toward the arm crown's axis
                parts.append(ellipsoid(centre, [r_arm * 0.55] * 3, nu=8, nv=5))
        v, f = merge(parts)
        yield it['key'], it['name'], '', v, f
        return
    sides = [('L', -1), ('R', 1)] if it.get('mirror') else [('', 1)]
    for side, sx in sides:
        if kind == 'tube':
            pts = [[sx * abs(p[0]) if it.get('mirror') else p[0], p[1], p[2]] for p in it['points']]
            r = it['radius'] if isinstance(it['radius'], list) else [it['radius']] * 2
            v, f = tube(pts, r[0], r[1])
        else:
            c = list(it['center'])
            if it.get('mirror'):
                c[0] = sx * abs(c[0])
            v, f = ellipsoid(c, it['radii'])
        name = it['name'] + (f" ({'left' if side == 'L' else 'right'})" if side else '')
        yield it['key'] + (f'-{side}' if side else ''), name, side, v, f


def main():
    spec = json.loads((ROOT / 'data' / 'meshes.json').read_text(encoding='utf-8'))['octopus']
    items = {it['key']: it for it in spec['items']}
    raw = []
    for it in spec['items']:
        for key, name, side, v, f in shapes(it, items):
            rec = {k: it[k] for k in ('entity', 'related', 'group', 'note', 'tone') if k in it}
            rec.update(name=name, key=key, approx=True)
            if side:
                rec['side'] = side
            rec['c'], rec['cl'], rec['cr'] = centroids(v)
            raw.append((rec, v, f))
    rmax = max(abs(x) for _, v, _ in raw for p in v for x in p)
    q = 32767.0 / rmax
    meshes = []
    for rec, v, f in raw:
        rec['p'] = base64.b64encode(struct.pack(f'<{3 * len(v)}h', *[round(x * q) for p in v for x in p])).decode('ascii')
        rec['i32'] = len(v) > 65535
        rec['i'] = base64.b64encode(struct.pack(f"<{3 * len(f)}{'I' if rec['i32'] else 'H'}", *[i for t in f for i in t])).decode('ascii')
        for k in ('c', 'cl', 'cr'):
            rec[k] = [round(x, 3) for x in rec[k]]
        meshes.append(rec)
    allv = [p for _, v, _ in raw for p in v]
    bundle = {'label': spec['label'], 'credit': spec['credit'], 'qs': 1.0 / q,
              'bounds': [[round(min(p[i] for p in allv), 3) for i in range(3)], [round(max(p[i] for p in allv), 3) for i in range(3)]],
              'anchors': {}, 'spine': [], 'meshes': meshes}
    OUT.write_text('window.CA_MESHES = window.CA_MESHES || {};\n'
                   f'window.CA_MESHES.octopus = {json.dumps(bundle, separators=(",", ":"))};\n', encoding='utf-8')
    print(f'{OUT.relative_to(ROOT)}: {len(meshes)} meshes, {OUT.stat().st_size / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
