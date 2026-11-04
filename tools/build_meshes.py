#!/usr/bin/env python3
"""
Build the 3D anatomy bundles used by the "3D atlas" view.

    python tools/build_meshes.py            # every species in data/meshes.json
    python tools/build_meshes.py mouse      # one species

Reads data/meshes.json, downloads the source meshes into .cache/ on first run
(Allen Mouse CCFv3 structure meshes; Allen Human Reference Atlas via BrainGlobe;
human cerebellar lobules and nuclei from the SUIT probabilistic atlas, Diedrichsen 2009/2011;
for the macaque, the NIMH Macaque Template v2.0 with its CHARM cortical and SARM subcortical
label volumes, from which surfaces are computed here), decimates and smooths them, puts every
species into one scene frame
(x = left->right, y = ventral->dorsal, z = posterior->anterior; brain ~10 units long)
and writes js/data/meshes_<species>.js (quantized, base64) so the site also works
when index.html is opened straight from disk.

Needs numpy and trimesh; the human lobules and the macaque also need nibabel, scipy and scikit-image.
If fast_simplification is installed it is used for quadric decimation (better shapes);
otherwise vertex clustering is used.

The SUIT lobules live in MNI space while the Allen human meshes do not, so the SUIT
cerebellum is fitted onto the Allen cerebellum surface (items marked "align_only"):
scaled ICP, then a per-axis scale refinement.
"""
import base64
import json
import pathlib
import sys
import tarfile
import urllib.request

import numpy as np
import trimesh
from trimesh.smoothing import filter_taubin

try:
    import fast_simplification
except ImportError:  # optional
    fast_simplification = None

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / '.cache'
OUT = ROOT / 'js' / 'data'
EXTENT = 10.0  # longest brain dimension, in scene units


def load_obj(path):
    verts, faces = [], []
    with open(path) as fh:
        for line in fh:
            if line.startswith('v '):
                verts.append(line.split()[1:4])
            elif line.startswith('f '):
                idx = [int(tok.split('/')[0]) for tok in line.split()[1:]]
                faces.extend((idx[0], idx[k], idx[k + 1]) for k in range(1, len(idx) - 1))
    return np.asarray(verts, float), np.asarray(faces, np.int64) - 1


def src_ids(it):
    """An item's atlas structure ids: one id, or a list whose meshes are merged into one structure."""
    return it['src'] if isinstance(it['src'], list) else [it['src']]


def source_paths(spec):
    """Return a function structure id -> local .obj path, downloading sources if needed."""
    src = spec['source']
    if src['type'] == 'allen_ccf':
        folder = CACHE / 'mouse_ccf'
        folder.mkdir(parents=True, exist_ok=True)
        for it in spec['items']:
            for sid in src_ids(it):
                path = folder / f"{sid}.obj"
                if not path.exists():
                    print('  downloading', path.name)
                    urllib.request.urlretrieve(src['url'].format(src=sid), path)
        return lambda sid: folder / f"{sid}.obj"
    if src['type'] == 'brainglobe':
        folder = CACHE / 'human_atlas'
        mesh_dir = folder / src['dir']
        if not mesh_dir.exists():
            folder.mkdir(parents=True, exist_ok=True)
            tgz = folder / 'atlas.tar.gz'
            if not tgz.exists():
                print('  downloading BrainGlobe atlas (~160 MB) ...')
                urllib.request.urlretrieve(src['url'], tgz)
            with tarfile.open(tgz) as tf:
                members = [m for m in tf.getmembers() if '/meshes/' in m.name]
                try:
                    tf.extractall(folder, members=members, filter='data')
                except TypeError:  # Python < 3.12
                    tf.extractall(folder, members=members)
        return lambda sid: mesh_dir / f"{sid}.obj"
    raise ValueError(f"unknown source type {src['type']}")


def to_scene_mm(v, frame, ml0):
    """Atlas axes (AP, SI, ML) -> scene axes (x right, y up, z anterior), in mm."""
    u = frame['unit_mm']
    ap, si, ml = v[:, 0], v[:, 1], v[:, 2]
    if frame.get('mirror'):
        x = -(ml - ml0)  # the annotated hemisphere is drawn on the left
    else:
        x = ml - frame['midline']
    return np.column_stack([x * u, -si * u, -ap * u])


def simplify(v, f, target):
    if len(f) <= target:
        return v, f
    if fast_simplification is not None:
        v2, f2 = fast_simplification.simplify(
            v.astype(np.float32), f.astype(np.int32), 1.0 - target / len(f))
        return v2.astype(float), f2.astype(np.int64)
    # Fallback: vertex clustering on a grid tuned to roughly hit the target.
    lo = v.min(0)
    cell = np.linalg.norm(v.max(0) - lo) / 80
    for _ in range(16):
        key = np.floor((v - lo) / cell).astype(np.int64)
        _, inv = np.unique(key, axis=0, return_inverse=True)
        inv = inv.reshape(-1)
        ff = inv[f]
        ff = ff[(ff[:, 0] != ff[:, 1]) & (ff[:, 1] != ff[:, 2]) & (ff[:, 0] != ff[:, 2])]
        if len(ff) > target * 1.15:
            cell *= 1.2
        elif len(ff) < target * 0.6:
            cell *= 0.88
        else:
            break
    nv = np.zeros((inv.max() + 1, 3))
    np.add.at(nv, inv, v)
    nv /= np.bincount(inv)[:, None]
    return nv, ff


def clean(v, f, smooth):
    m = trimesh.Trimesh(v, f, process=True)
    m.update_faces(m.nondegenerate_faces())
    m.remove_unreferenced_vertices()
    if smooth:
        filter_taubin(m, iterations=smooth)
    return np.asarray(m.vertices), np.asarray(m.faces)


def centroids(v):
    c = v.mean(0)
    left, right = v[v[:, 0] < 0], v[v[:, 0] > 0]
    cl = left.mean(0) if len(left) else c
    cr = right.mean(0) if len(right) else c
    return [list(map(float, c)), list(map(float, cl)), list(map(float, cr))]


def split_lr(v, f):
    """Split faces into left / right meshes by face-centroid x."""
    out = {}
    side = v[f].mean(1)[:, 0] >= 0
    for name, mask in (('L', ~side), ('R', side)):
        ff = f[mask]
        used = np.unique(ff)
        remap = -np.ones(len(v), np.int64)
        remap[used] = np.arange(len(used))
        out[name] = (v[used], remap[ff])
    return out


def b64(arr):
    return base64.b64encode(arr.tobytes()).decode('ascii')


def loader(spec):
    """Return item -> (vertices in scene mm: x right, y up, z anterior; faces)."""
    if spec['source']['type'] == 'nmt':
        return NMT(spec['source']).surface
    path_of = source_paths(spec)
    frame = spec['frame']
    shell = next(it for it in spec['items'] if it['group'] == 'shell')
    ml0 = load_obj(path_of(shell['src']))[0][:, 2].min()

    def load(it):
        vs, fs, n = [], [], 0
        for sid in src_ids(it):
            v, f = load_obj(path_of(sid))
            vs.append(v)
            fs.append(f + n)
            n += len(v)
        return to_scene_mm(np.concatenate(vs), frame, ml0), np.concatenate(fs)
    return load


class NMT:
    """NIMH Macaque Template v2 (symmetric) with the CHARM cortical and SARM subcortical hierarchical atlases.

    Items name labels by abbreviation: {"charm": ["M1"], "sarm": ["Cb1V", ...]} (each read at its finest level),
    or a template mask: {"mask": "brainmask"}. Surfaces come from marching cubes on the label volumes."""

    def __init__(self, src):
        import nibabel as nib
        base = CACHE / 'macaque_nmt' / src['dir']
        if not base.exists():
            folder = base.parent
            folder.mkdir(parents=True, exist_ok=True)
            tgz = folder / src['url'].rsplit('/', 1)[-1]
            if not tgz.exists():
                print('  downloading NMT v2 (~270 MB) ...')
                urllib.request.urlretrieve(src['url'], tgz)
            keep = (f"{src['dir']}/{src['res']}/", f"{src['dir']}/tables_")
            with tarfile.open(tgz) as tf:
                members = [m for m in tf.getmembers() if m.name.startswith(keep) and (m.isfile() or m.isdir())]
                try:
                    tf.extractall(folder, members=members, filter='data')
                except TypeError:  # Python < 3.12
                    tf.extractall(folder, members=members)
        self.res = base / src['res']
        self.base, self.tag, self.nib = base, src['res'], nib
        self.vols, self.tables = {}, {}

    def table(self, atlas):
        if atlas not in self.tables:
            rows = {}
            with open(self.base / f'tables_{atlas}' / f'{atlas}_key_all.txt') as fh:
                next(fh)
                for line in fh:
                    idx, abbr, _name, _first, last = line.rstrip('\n').split('\t')[:5]
                    rows[abbr] = (int(idx), int(last))
            self.tables[atlas] = rows
        return self.tables[atlas]

    def volume(self, atlas):
        if atlas not in self.vols:
            img = self.nib.load(str(self.res / f'{atlas}_in_{self.tag}.nii.gz'))
            self.vols[atlas] = (np.asarray(img.dataobj), img.affine)
        return self.vols[atlas]

    def mask(self, it):
        if 'mask' in it:
            img = self.nib.load(str(self.res / f"{self.tag}_{it['mask']}.nii.gz"))
            return np.asarray(img.dataobj) > 0, img.affine
        m, aff = None, None
        for atlas in ('CHARM', 'SARM'):
            labels = it.get(atlas.lower(), [])
            if not labels:
                continue
            vol, aff = self.volume(atlas)
            tab = self.table(atlas)
            for lab in labels:
                idx, level = tab[lab]
                hit = vol[..., 0, level - 1] == idx
                if not hit.any():
                    raise ValueError(f"{it['key']}: {atlas} label {lab} is empty")
                m = hit if m is None else m | hit
        return m, aff

    def surface(self, it):
        m, aff = self.mask(it)
        idx = np.argwhere(m)
        lo, hi = np.maximum(idx.min(0) - 2, 0), idx.max(0) + 3   # crop to the structure
        crop = m[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
        a2 = aff.copy()
        a2[:3, 3] = aff[:3, :3] @ lo + aff[:3, 3]
        v, f = field_surface(crop.astype(np.float32), a2, 0.5, it.get('sigma', 0.8))
        return v, outward(v, f)


def build(species, spec):
    print(f'[{species}]')
    load = loader(spec)
    frame = spec['frame']
    shell = next(it for it in spec['items'] if it['group'] == 'shell')
    sv, _ = load(shell)
    if frame.get('mirror'):
        sv = np.vstack([sv, sv * [-1, 1, 1]])
    lo, hi = sv.min(0), sv.max(0)
    center = (lo + hi) / 2
    center[0] = 0.0  # keep the midline at x = 0
    scale = EXTENT / (hi - lo).max()

    meshes, helpers, targets = [], {}, []
    for it in spec['items']:
        if 'suit' in it:
            continue  # built below, once the alignment target is known
        v, f = load(it)
        v = (v - center) * scale
        if it.get('align_only'):
            if frame.get('mirror'):
                v, f = np.vstack([v, v * [-1, 1, 1]]), np.vstack([f, f[:, ::-1] + len(v)])
            targets.append((v, f))
            print(f"  {it['key']:<14} alignment target only")
            continue
        v, f = simplify(v, f, it['faces'])
        v, f = clean(v, f, it.get('smooth', 4))
        if frame.get('mirror'):
            v, f = np.vstack([v, v * [-1, 1, 1]]), np.vstack([f, f[:, ::-1] + len(v)])
        if it['group'] == 'helper':
            helpers[it['key']] = (v.min(0), v.max(0), v.mean(0), v)
            continue
        parts = split_lr(v, f).items() if it.get('split') else [('', (v, f))]
        for side, (pv, pf) in parts:
            rec = {k: it[k] for k in ('name', 'entity', 'related', 'group', 'note', 'tone') if k in it}
            rec['key'] = it['key'] + (f'-{side}' if side else '')
            if side:
                rec['side'] = side
                rec['name'] = f"{it['name']} ({'left' if side == 'L' else 'right'})"
            rec['_v'], rec['_f'] = pv, pf
            rec['c'], rec['cl'], rec['cr'] = centroids(pv)
            meshes.append(rec)
        print(f"  {it['key']:<14} {len(f):>6} faces")

    if any('suit' in it for it in spec['items']):
        meshes.extend(build_suit(spec, targets))

    anchors, spine = extra_anchors(species, meshes, helpers)

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
        'anchors': anchors, 'spine': spine, 'meshes': meshes,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f'meshes_{species}.js'
    out.write_text('window.CA_MESHES = window.CA_MESHES || {};\n'
                   f'window.CA_MESHES.{species} = {json.dumps(bundle, separators=(",", ":"))};\n')
    print(f'  -> {out.relative_to(ROOT)} ({out.stat().st_size / 1e6:.2f} MB, {len(meshes)} meshes)')


def suit_file(url):
    folder = CACHE / 'suit'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / url.rsplit('/', 1)[-1]
    if not path.exists():
        print('  downloading', path.name)
        urllib.request.urlretrieve(url, path)
    return path


def suit_volume(src):
    import nibabel as nib
    img = nib.load(str(suit_file(src['url'])))
    return np.asarray(img.dataobj).astype(np.int16), img.affine


def suit_prob(src):
    import nibabel as nib
    return np.asarray(nib.load(str(suit_file(src['prob_url']))).dataobj, dtype=np.float32)


def field_surface(field, aff, level=0.5, sigma=0.8):
    """Iso-surface of a voxel field in mm, scene axes (x right, y up, z anterior).

    Small structures are upsampled 2x first so they come out smooth rather than blocky."""
    from scipy import ndimage
    from skimage import measure
    up = 2 if (field >= level).sum() < 1500 else 1
    m = np.pad(field.astype(np.float32), 3)
    if up > 1:
        m = m.repeat(up, 0).repeat(up, 1).repeat(up, 2)
    m = ndimage.gaussian_filter(m, sigma * up)
    v, f, _, _ = measure.marching_cubes(m, min(level, 0.5 * m.max()))
    v = (v + 0.5) / up - 0.5 - 3               # back to voxel indices
    v = v @ aff[:3, :3].T + aff[:3, 3]          # voxel -> MNI mm (RAS)
    return v[:, [0, 2, 1]], f.astype(np.int64)  # RAS -> scene axes


def label_surface(lab, aff, labels, sigma=0.8):
    return field_surface(np.isin(lab, labels).astype(np.float32), aff, 0.5, sigma)


def outward(v, f):
    """Flip the winding if the surface encloses negative volume (axis swaps mirror it)."""
    return f[:, ::-1] if trimesh.Trimesh(v, f, process=False).volume < 0 else f


def fit_to_target(src_v, targets):
    """Similarity ICP of the SUIT cerebellum onto the Allen cerebellum, then per-axis scaling.

    Closest points come from a KD-tree over a dense sample of the target surface
    (no rtree / libspatialindex needed)."""
    from scipy.spatial import cKDTree
    tv = np.vstack([t[0] for t in targets])
    offs = np.cumsum([0] + [len(t[0]) for t in targets[:-1]])
    tf = np.vstack([t[1] + o for t, o in zip(targets, offs)])
    target = trimesh.Trimesh(tv, tf, process=True)
    tpts, _ = trimesh.sample.sample_surface(target, 200000, seed=1)
    tree = cKDTree(tpts)
    pts = src_v[:: max(1, len(src_v) // 6000)]
    s0 = float(np.mean(np.ptp(tv, 0) / np.ptp(pts, 0)))
    init = np.eye(4)
    init[:3, :3] *= s0
    init[:3, 3] = (tv.max(0) + tv.min(0)) / 2 - s0 * (pts.max(0) + pts.min(0)) / 2
    M, _, _ = trimesh.registration.icp(pts, tpts, initial=init, threshold=1e-7, max_iterations=100,
                                       reflection=False, translation=True, scale=True)
    apply = lambda M_, v: v @ M_[:3, :3].T + M_[:3, 3]
    for _ in range(8):  # per-axis scale + shift against closest surface points
        p = apply(M, pts)
        q = tpts[tree.query(p)[1]]
        A = np.eye(4)
        for k in range(3):
            a, b = np.polyfit(p[:, k], q[:, k], 1)
            A[k, k], A[k, 3] = a, b
        M = A @ M
    d = tree.query(apply(M, pts))[0]
    det = np.linalg.det(M[:3, :3])
    rot = M[:3, :3] / np.cbrt(abs(det))
    print(f'  SUIT fit: scale {np.cbrt(det):.4f} units/mm (axes {np.round(np.linalg.norm(M[:3, :3], axis=0), 4)}), '
          f'surface distance mean {d.mean():.3f} / p95 {np.percentile(d, 95):.3f} units, '
          f'rotation ~{np.degrees(np.arccos(np.clip((np.trace(rot) - 1) / 2, -1, 1))):.1f} deg')
    return lambda v: apply(M, v)


def build_suit(spec, targets):
    if not targets:
        raise ValueError('SUIT items need at least one "align_only" target mesh')
    lab, aff = suit_volume(spec['suit'])
    cv, _ = label_surface(lab, aff, list(range(1, 29)), sigma=1.0)
    tf = fit_to_target(cv, targets)
    out, prob = [], None
    for it in spec['items']:
        if 'suit' not in it:
            continue
        for side, labels in it['suit'].items():
            labels = labels if isinstance(labels, list) else [labels]
            if it.get('suit_prob'):  # iso-surface of the probabilistic map instead of the max-probability label
                prob = prob if prob is not None else suit_prob(spec['suit'])
                v, f = field_surface(sum(prob[..., k - 1] for k in labels), aff, it['suit_prob'], 0.6)
            else:
                v, f = label_surface(lab, aff, labels)
            v = tf(v)
            v, f = simplify(v, f, it['faces'])
            v, f = clean(v, f, it.get('smooth', 4))
            f = outward(v, f)
            rec = {k: it[k] for k in ('name', 'entity', 'related', 'group', 'note', 'tone') if k in it}
            rec['key'] = it['key'] + ('' if side == 'C' else f'-{side}')
            if side != 'C':
                rec['side'] = side
                rec['name'] = f"{it['name']} ({'left' if side == 'L' else 'right'})"
            rec['_v'], rec['_f'] = v, f
            rec['c'], rec['cl'], rec['cr'] = centroids(v)
            out.append(rec)
        print(f"  {it['key']:<14} {len(f):>6} faces (SUIT)")
    return out


def bbox(meshes, key):
    vs = [m['_v'] for m in meshes if m['key'] == key or m['key'].startswith(key + '-')]
    v = np.vstack(vs)
    return v.min(0), v.max(0), v.mean(0)


def sided(p):
    """Anchor record (c, left, right) for a point given on the right side (x >= 0)."""
    p = np.asarray(p, float)
    left = p * [-1, 1, 1]
    c = p * [0, 1, 1]
    return [[round(float(x), 3) for x in a] for a in (c, left, p)]


def extra_anchors(species, meshes, helpers):
    """Approximate positions for structures that have no mesh (marked as such in the UI)."""
    blo, bhi, _ = bbox(meshes, 'brain')
    width = bhi[0] - blo[0]
    a = {}
    if species == 'human':
        mlo, mhi, mc = bbox(meshes, 'midbrain-teg')
        dlo, dhi, dc = bbox(meshes, 'medulla')
        plo, phi, pc = bbox(meshes, 'pons-basilar')
        aq_lo, aq_hi, aq_c = helpers['aqueduct'][:3]
        v4lo, v4hi, v4c = helpers['v4'][:3]
        a['pag'] = sided([0.18, aq_c[1], aq_c[2]])
        a['vta'] = sided([0.18, mlo[1] + 0.3 * (mhi[1] - mlo[1]), mlo[2] + 0.75 * (mhi[2] - mlo[2])])
        a['snc'] = sided([0.55, mlo[1] + 0.3 * (mhi[1] - mlo[1]), mlo[2] + 0.65 * (mhi[2] - mlo[2])])
        a['snr'] = sided([0.75, mlo[1] + 0.2 * (mhi[1] - mlo[1]), mlo[2] + 0.6 * (mhi[2] - mlo[2])])   # pars reticulata: ventrolateral to the compact part
        a['brainstem-motor'] = sided([0.3, mlo[1] + 0.45 * (mhi[1] - mlo[1]), mc[2]])
        a['io'] = sided([0.25, dlo[1] + 0.35 * (dhi[1] - dlo[1]), dlo[2] + 0.85 * (dhi[2] - dlo[2])])
        a['vestibular-nuclei'] = sided([0.55 * v4hi[0], v4c[1], v4c[2] + 0.1])
        a['labyrinth'] = sided([0.3 * width, pc[1], pc[2] - 0.35])
        a['eyes'] = sided([0.22 * width, blo[1] + 0.42 * (bhi[1] - blo[1]), bhi[2] - 0.3])
        # neuromodulator sources, placed from neighboring structures (y up, z anterior)
        tlo, thi, _ = bbox(meshes, 'pons-teg')
        slo, _, sc = bbox(meshes, 'stn')
        a['lc'] = sided([0.3, thi[1] - 0.3 * (thi[1] - tlo[1]), tlo[2] + 0.2 * (thi[2] - tlo[2])])   # rostral dorsal pons, by the 4th ventricle
        a['ppn'] = sided([0.5, mlo[1] + 0.1 * (mhi[1] - mlo[1]), mlo[2] + 0.4 * (mhi[2] - mlo[2])])  # caudal midbrain tegmentum, lateral
        a['mrn'] = sided([0.5, mlo[1] + 0.55 * (mhi[1] - mlo[1]), mlo[2] + 0.5 * (mhi[2] - mlo[2])])  # midbrain reticular nucleus: lateral tegmentum, above the red nucleus level
        a['ser-neurons'] = sided([0.0, dhi[1] - 0.2 * (dhi[1] - dlo[1]), dlo[2] + 0.55 * (dhi[2] - dlo[2])])  # rostral medullary reticular formation
        a['drn'] = sided([0.0, aq_lo[1] - 0.12, aq_lo[2] + 0.3 * (aq_hi[2] - aq_lo[2])])   # dorsal raphe: midline, just below the caudal aqueduct
        a['tmn'] = sided([0.25, slo[1] - 0.15, sc[2] + 0.15])   # posterior hypothalamus, below and in front of the STN
        a['lh'] = sided([0.45, sc[1] - 0.05, sc[2] + 0.45])     # lateral hypothalamus, in front of the STN

        def right(key):   # mean of the right-hemisphere vertices of a bilateral mesh
            v = np.vstack([m['_v'] for m in meshes if m['key'] == key])
            return v[v[:, 0] > 0].mean(0)
        # motor-cortex neighbours the Allen meshes here do not segment (y up, z anterior)
        pr = right('precentral')
        a['premotor'] = sided([0.6 * pr[0], pr[1] + 0.4, pr[2] + 0.9])   # in front of and above M1 (dorsal premotor, toward SMA)
        a['s1'] = sided([pr[0], pr[1], pr[2] - 0.9])                     # postcentral gyrus, behind M1
        ulo, _, _ = bbox(meshes, 'putamen')
        a['basal-forebrain'] = sided([0.75, ulo[1], (right('accumbens')[2] + right('amygdala')[2]) / 2])   # below the striatum, between accumbens and amygdala
        # MT (V5) lies in lateral occipitotemporal cortex, which the Allen meshes here do not segment: halfway between the
        # inferior occipital gyrus and the posterior fifth of the middle temporal gyrus (right hemisphere)
        iv, tv = helpers['iog'][3], helpers['mtg'][3]
        iv, tv = iv[iv[:, 0] > 0], tv[tv[:, 0] > 0]
        a['mt'] = sided((iv.mean(0) + tv[tv[:, 2] <= np.percentile(tv[:, 2], 20)].mean(0)) / 2)
        start = np.array([0.0, dlo[1] + 0.1, dc[2]])
        spine = [start, start + [0, -1.6, -0.15], start + [0, -3.2, -0.25]]
    elif species == 'macaque':
        vlo, vhi, vc = bbox(meshes, 've')
        a['labyrinth'] = sided([0.27 * width, vc[1] - 0.1, vc[2]])   # inner ear, lateral to the vestibular nuclei
        olo, ohi, _ = bbox(meshes, 'ofc')
        a['eyes'] = sided([0.24 * width, olo[1] - 0.9, ohi[2] - 0.3])   # orbits below the orbitofrontal cortex
        a['ser-neurons'] = sided([0.0, *helpers['gi'][2][1:]])           # medullary reticular formation, as in the mouse
        sv = np.vstack([m['_v'] for m in meshes if m['key'] == 'sn'])
        sv = sv[sv[:, 0] > 0]                                            # SARM labels the substantia nigra as a whole:
        a['snr'] = sided([np.percentile(sv[:, 0], 75), np.percentile(sv[:, 1], 25), sv[:, 2].mean()])   # pars reticulata, its ventrolateral part
        hv = np.vstack([m['_v'] for m in meshes if m['key'] == 'hip'])
        hv = hv[hv[:, 0] > 0]                                            # the primate anterior hippocampus corresponds to the rodent
        a['vhpc'] = sided(hv[hv[:, 2] >= np.percentile(hv[:, 2], 80)].mean(0))   # ventral one: the front fifth of the hippocampus,
        a['dhpc'] = sided(hv[hv[:, 2] <= np.percentile(hv[:, 2], 20)].mean(0))   # and the posterior (dorsal) one the back fifth
        mlo, mhi, mc = helpers['mm'][:3]
        a['tmn'] = sided([mhi[0] + 0.12, mc[1], mc[2]])                  # posterior hypothalamus, beside the mammillary bodies
        ov = np.vstack([m['_v'] for m in meshes if m['key'] == 'ofc'])    # NMT does not include the olfactory bulb: place it
        ov = ov[ov[:, 0] > 0]                                            # under the front of the orbital surface, near the midline
        front = ov[ov[:, 2] >= np.percentile(ov[:, 2], 70)]               # the front of the label also holds the frontal pole,
        tip = front[front[:, 1] <= np.percentile(front[:, 1], 15)].mean(0)  # so take its lowest part (the orbital surface)
        a['ob'] = sided([0.35 * tip[0], tip[1] - 0.15, tip[2]])
        mv = helpers['med'][3]                                           # the spinal cord continues the long axis of the medulla
        c = mv.mean(0)
        d = np.linalg.svd(mv - c, full_matrices=False)[2][0]
        d = d if d[1] < 0 else -d
        d[0] = 0.0
        d /= np.linalg.norm(d)
        start = c + d * ((mv - c) @ d).max()
        start[0] = 0.0
        spine = [start, start + 1.6 * d, start + 3.2 * d]
    else:
        io_lo, io_hi, io_c = bbox(meshes, 'io')
        vlo, vhi, vc = bbox(meshes, 'vnc')
        a['labyrinth'] = sided([0.45 * width, vc[1] - 0.15, vc[2]])
        a['eyes'] = sided([0.42 * width, blo[1] + 0.55 * (bhi[1] - blo[1]), bhi[2] - 0.3 * (bhi[2] - blo[2])])
        if 'grn' in helpers:  # serotonergic afferents arise mainly in the medullary reticular formation (rat)
            a['ser-neurons'] = sided([0.0, *helpers['grn'][2][1:]])
        hv = np.vstack([m['_v'] for m in meshes if m['key'] in ('dg', 'ca1', 'ca2', 'ca3')])
        hv = hv[hv[:, 0] > 0]
        a['dhpc'] = sided(hv[hv[:, 1] >= np.percentile(hv[:, 1], 80)].mean(0))   # dorsal hippocampus: the upper fifth of the fields
        a['vhpc'] = sided(hv[hv[:, 1] <= np.percentile(hv[:, 1], 20)].mean(0))   # ventral hippocampus: the lower fifth
        z0 = a['dhpc'][2][2]   # the fields are placed where they cross the dorsal hippocampus, as in a coronal section:
        for m in meshes:       # the centroids of their curved sheets lie close together, deep in the formation
            if m['key'] in ('dg', 'ca1', 'ca2', 'ca3'):
                m['c'], m['cl'], m['cr'] = centroids(m['_v'][np.abs(m['_v'][:, 2] - z0) < 0.2])
        start = np.array([0.0, io_c[1] + 0.15, blo[2] + 0.15])
        spine = [start, start + [0, -0.25, -1.6], start + [0, -0.35, -3.2]]
    # olfactory sensory neurons line the nasal epithelium, in front of and below the olfactory bulb
    bv = [m['_v'] for m in meshes if m.get('entity') == 'ob']
    if bv:
        bv = np.vstack(bv)
        bv = bv[bv[:, 0] > 0]
        ob_front = bv[bv[:, 2] >= np.percentile(bv[:, 2], 90)].mean(0)
    elif 'ob' in a:
        ob_front = np.asarray(a['ob'][2])
    else:
        ob_front = None
    if ob_front is not None:
        a['osn'] = sided(ob_front + [0.0, -0.25, 0.45])
    end = spine[-1]
    a['spinal'] = sided([0.0, *spine[1][1:]])
    a['body'] = sided([0.9, end[1] - 0.6, end[2] - 0.3])
    a['gut'] = sided([0.0, end[1] - 1.2, end[2] + {'human': 1.6, 'macaque': 1.4}.get(species, 1.2)])
    spine = [[round(float(x), 3) for x in p] for p in spine]
    return a, spine


def main():
    cfg = json.loads((ROOT / 'data' / 'meshes.json').read_text())
    # by default, only the species switched on in knowledge.json (atlas3d.species)
    offered = json.loads((ROOT / 'data' / 'knowledge.json').read_text())['atlas3d']['species']
    species = sys.argv[1:] or [sp for sp in cfg if sp in offered]
    print('decimation:', 'quadric (fast_simplification)' if fast_simplification else 'vertex clustering')
    for sp in species:
        if cfg[sp].get('schematic'):   # no atlas volume: drawn by tools/build_octopus.py
            print(f'[{sp}] schematic: run tools/build_octopus.py')
            continue
        build(sp, cfg[sp])


if __name__ == '__main__':
    main()
