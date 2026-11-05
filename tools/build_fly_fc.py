#!/usr/bin/env python3
"""Build data/fly_connectivity.json: structural and functional connectivity of the fly central brain, for the
fruit fly's Functional map, recomputed from the published data of Turner, Mann & Clandinin (2021).

    python3 tools/build_fly_fc.py

Source: "Drosophila central brain connectivity", figshare doi:10.6084/m9.figshare.13349282 (v3, MIT licence), the data
of Turner MH, Mann K, Clandinin TR (2021) The connectome predicts resting-state functional connectivity across the
Drosophila brain. Curr Biol 31:2386-2394 (PMID 33770490). The archive (about 250 MB) is downloaded once into
.cache/turner2021/ (gitignored). The computation follows the authors' code (github.com/mhturner/SC-FC):

  regions     the 37 regions of the Ito et al. (2014) atlas that the paper analyses (scfc/bridge.getItoNames)
  functional  per fly, each region's fluorescence trace is high-pass filtered (first-order Butterworth, 0.01 Hz, sampled
              at 1.2 Hz), trimmed of its first 100 frames (and of the artefacts the authors list), and correlated with
              every other region's; the correlations are Fisher z-transformed and averaged over the 20 flies
              (functional_connectivity.getCmat)
  structural  the number of hemibrain neurons with input in one region and output in another (cell count, rows =
              source; anatomical_connectivity.getAtlasConnectivity, metric 'cellcount')
  r           Pearson correlation of mean functional z with log10 cell count, symmetrized, over region pairs (Fig. 2F)
  difference  z-scored functional connectivity minus z-scored log10 cell count over connected pairs, averaged per
              region and fly (Fig. 4)
  geometry    each region's frontal outline and centroid, from the atlas label volume the imaging was registered to
              (atlas_data/vfb_68_Original.nii.gz; 2.61 x 2.61 x 2.7 um voxels, x toward the fly's left, y ventral,
              z posterior); projected along z, so the view is from the front, with the fly's right on the left

The response files are pickled pandas DataFrames from an older pandas. They are read with a restricted unpickler that
only allows the numpy and pandas constructors those files use, so loading them cannot run other code.
Needs numpy, scipy, pandas, nibabel and scikit-image.
"""
import gzip
import io
import json
import pathlib
import pickle
import tarfile
import urllib.request

import nibabel as nib
import numpy as np
import pandas as pd
from scipy import ndimage, signal
from scipy.stats import pearsonr, zscore
from skimage import measure

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache' / 'turner2021'
ARCHIVE = CACHE / 'data_TurnerMannClandinin.tar.gz'
URL = 'https://ndownloader.figshare.com/files/26356327'
OUT = ROOT / 'data' / 'fly_connectivity.json'

ITO = ['AL_R', 'AOTU_R', 'ATL_R', 'ATL_L', 'AVLP_R', 'BU_R', 'BU_L', 'CAN_R', 'CRE_R', 'CRE_L', 'EB', 'EPA_R', 'FB',
       'GOR_R', 'GOR_L', 'IB_R', 'IB_L', 'ICL_R', 'LAL_R', 'LH_R', 'MB_CA_R', 'MB_ML_R', 'MB_ML_L', 'MB_PED_R', 'MB_VL_R',
       'NO', 'PB', 'PLP_R', 'PVLP_R', 'SCL_R', 'SIP_R', 'SLP_R', 'SMP_R', 'SMP_L', 'SPS_R', 'VES_R', 'WED_R']
# frames to keep, per recording (scfc/functional_connectivity.trimRegionResponse); all others drop the first 100
TRIM = {'2018-10-19_1': list(range(100, 900)) + list(range(1100, 2000)),
        '2017-11-08_1': list(range(100, 1900)) + list(range(2000, 4000)),
        '2018-10-20_1': list(range(100, 1000))}
VOXEL = (2.611173, 2.611173, 2.7)   # um
MIT_NOTICE = ('The source data, "Drosophila central brain connectivity" by Max Turner (figshare, doi:10.6084/m9.figshare.13349282), '
              'are released under the MIT License. Copyright (c) Max Turner. Permission is hereby granted, free of charge, to any '
              'person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software '
              'without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, '
              'sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, '
              'subject to the following conditions: The above copyright notice and this permission notice shall be included in all '
              'copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, '
              'EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE '
              'AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER '
              'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE '
              'OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.')


def archive():
    if not ARCHIVE.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        print('downloading the Turner et al. (2021) data from figshare (about 250 MB) ...')
        req = urllib.request.Request(URL, headers={'User-Agent': 'brain-circuit-atlas'})
        tmp = ARCHIVE.with_suffix('.part')
        with urllib.request.urlopen(req, timeout=1800) as r, open(tmp, 'wb') as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
        tmp.rename(ARCHIVE)
    return tarfile.open(ARCHIVE, 'r:gz')


try:                                   # numpy 2 moved it; older pickles name the numpy 1 path
    from numpy._core.multiarray import _reconstruct
except ImportError:
    from numpy.core.multiarray import _reconstruct


class _Stub:
    """Stands in for a pandas DataFrame or BlockManager; keeps only the pickled state."""
    def __setstate__(self, state):
        self.state = state


class SafeUnpickler(pickle.Unpickler):
    """Allows only the constructors the response files use (checked with pickletools)."""
    def find_class(self, module, name):
        if (module, name) == ('builtins', 'slice'):
            return slice
        if (module, name) == ('numpy', 'ndarray'):
            return np.ndarray
        if (module, name) == ('numpy', 'dtype'):
            return np.dtype
        if (module, name) == ('numpy.core.multiarray', '_reconstruct'):
            return _reconstruct
        if (module, name) in (('pandas.core.frame', 'DataFrame'), ('pandas.core.internals.managers', 'BlockManager')):
            return type(name, (_Stub,), {})
        if (module, name) == ('pandas.core.indexes.base', '_new_Index'):
            return lambda cls, d: (cls, d)
        if module in ('pandas.core.indexes.numeric', 'pandas.core.indexes.range'):
            return name
        raise pickle.UnpicklingError(f'blocked {module}.{name}')


def read_responses(raw):
    """Region x time array and region numbers from one pickled DataFrame (legacy BlockManager layout)."""
    frame = SafeUnpickler(io.BytesIO(raw)).load()
    mgr = frame.state.get('_mgr') or frame.state.get('_data')
    st = mgr.state[0] if len(mgr.state[0]) == 4 else mgr.state
    axes, values = st[0], st[1]

    def index(a):
        cls, d = a
        return np.arange(d.get('start', 0), d['stop'], d.get('step', 1)) if cls == 'RangeIndex' else np.asarray(d['data'])
    columns, rows = index(axes[0]), index(axes[1])
    assert len(values) == 1 and values[0].shape == (len(columns), len(rows))
    return values[0].T.astype(float), rows


def main():
    tar = archive()
    members = {m.name: m for m in tar.getmembers()}
    read = lambda name: tar.extractfile(members['data/' + name]).read()

    dec = pd.read_csv(io.BytesIO(read('ito_68_atlas/Original_Index_panda_full.csv')))
    num = dict(zip(dec.iloc[:, 0].str.strip(), dec['num']))
    inc = np.array([num[r] for r in ITO])
    n = len(ITO)

    # functional connectivity
    sos = signal.butter(1, 0.01, 'hp', fs=1.2, output='sos')
    cz = []
    for name in sorted(k for k in members if k.startswith('data/ito_responses/') and k.endswith('.pkl')):
        fid = name.rsplit('/', 1)[1][len('ito_'):-len('.pkl')]
        x, rows = read_responses(tar.extractfile(members[name]).read())
        x = signal.sosfilt(sos, x)
        x = x[:, TRIM[fid]] if fid in TRIM else x[:, 100:]
        x = pd.DataFrame(x, index=rows).reindex(inc).to_numpy()
        c = np.corrcoef(x)
        np.fill_diagonal(c, np.nan)
        cz.append(np.arctanh(c))
    fc = np.stack(cz, 2)
    fc = np.where(np.eye(n, dtype=bool)[..., None], 0, fc).mean(2)   # the diagonal is NaN in every fly
    np.fill_diagonal(fc, np.nan)

    # structural connectivity: cell count, rows = source region
    full = pd.read_csv(io.BytesIO(read('hemi_2_atlas/JRC2018_ito_cellcount_matrix.csv')), header=0).to_numpy()[:, 1:]
    full = pd.DataFrame(full, index=np.arange(1, 87), columns=np.arange(1, 87))
    sc = np.array([[full.loc[s, t] for t in inc] for s in inc], float)
    np.fill_diagonal(sc, 0)

    iu = np.triu_indices(n, k=1)
    scs = (sc + sc.T) / 2
    keep = scs[iu] > 0
    r, p = pearsonr(np.log10(scs[iu][keep]), fc[iu][keep])
    fly_r = [pearsonr(np.log10(scs[iu][keep]), c[iu][keep])[0] for c in cz]

    # function minus wiring (Fig. 4): z-scored FC minus z-scored log10 SC over connected pairs, per region and fly
    conn = np.where(sc > 0)
    a_z = zscore(np.log10(sc[conn]))
    diff_fly = []
    for c in cz:
        f = np.where(np.isnan(c), 0, c)
        d = np.zeros((n, n))
        d[conn] = zscore(f[conn]) - a_z
        diff_fly.append(d.mean(axis=0))
    diff_fly = np.array(diff_fly)          # fly x region
    f_mean = np.where(np.isnan(fc), 0, fc)
    dmat = np.zeros((n, n))
    dmat[conn] = zscore(f_mean[conn]) - a_z

    # geometry from the atlas label volume
    vol = tar.extractfile(members['data/atlas_data/vfb_68_Original.nii.gz']).read()
    img = nib.Nifti1Image.from_bytes(gzip.decompress(vol))
    lab = np.asarray(img.dataobj)
    um = lambda pts: [[round(float(px) * VOXEL[0], 1), round(float(py) * VOXEL[1], 1)] for px, py in pts]

    def largest(mask):
        cc, k = ndimage.label(mask)
        if k <= 1:
            return mask
        sizes = ndimage.sum(mask, cc, range(1, k + 1))
        return cc == (np.argmax(sizes) + 1)

    def outline(mask2d, tol):
        cs = measure.find_contours(np.pad(mask2d, 1).astype(float), 0.5)
        c = max(cs, key=len) - 1
        return um(measure.approximate_polygon(c, tolerance=tol))

    geo = []
    for name in ITO:
        m = largest(lab == num[name])
        pts = np.argwhere(m)
        geo.append({'c': um([pts[:, :2].mean(0)])[0], 'z': round(float(pts[:, 2].mean()) * VOXEL[2], 1),
                    'vol': int(m.sum()), 'outline': outline(ndimage.binary_closing(m.any(2), iterations=2), 0.9)})
    brain = largest(ndimage.binary_closing(ndimage.binary_fill_holes((lab > 0).any(2)), iterations=3))
    shape = [round(lab.shape[0] * VOXEL[0], 1), round(lab.shape[1] * VOXEL[1], 1)]

    out = {
        'source': 'Turner, Mann & Clandinin (2021), data on figshare (doi:10.6084/m9.figshare.13349282, v3, MIT licence), '
                  'recomputed with tools/build_fly_fc.py following the authors\' code (github.com/mhturner/SC-FC)',
        'refs': ['turner2021'],
        'license': MIT_NOTICE,
        'flies': len(cz),
        'regions': ITO,
        'fc': [[None if i == j else round(float(fc[i, j]), 3) for j in range(n)] for i in range(n)],
        'sc': sc.astype(int).tolist(),
        'r': round(float(r), 3), 'p': float(f'{p:.2g}'), 'pairs': int(keep.sum()),
        'flyR': [round(float(v), 3) for v in fly_r],
        'diff': [[round(float(dmat[i, j]), 2) for j in range(n)] for i in range(n)],
        'diffRegion': [round(float(v), 3) for v in diff_fly.mean(0)],
        'diffRegionSem': [round(float(v), 3) for v in diff_fly.std(0) / np.sqrt(len(cz))],
        'frame': {'size': shape, 'note': 'frontal view in um; x toward the fly\'s left (so the fly\'s right is on the left), y ventral'},
        'brain': outline(brain, 1.2),
        'geometry': geo,
    }
    OUT.write_text(json.dumps(out, separators=(',', ':')) + '\n', encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB): {len(cz)} flies, {n} regions, '
          f'{int(keep.sum())} region pairs, structure-function r = {r:.2f} (per fly {np.mean(fly_r):.2f}, '
          f'{min(fly_r):.2f}-{max(fly_r):.2f})')
    top = np.argsort(-diff_fly.mean(0))[:6]
    print('  most more coupled in activity than in wiring:', ', '.join(f'{ITO[i]} {diff_fly.mean(0)[i]:+.2f}' for i in top))


if __name__ == '__main__':
    main()
