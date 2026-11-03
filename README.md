# Cerebellum Atlas

An interactive, evidence-linked map of the cerebellum and its connections to the rest of the brain and body. It runs from molecules and cells through circuits and brain-wide loops to behavior, cognition and disease. Every connection carries an evidence grade and links to the PubMed papers behind it, and a hypothesis lab turns weak or missing links into testable experiments.

**Live site:** <https://zhuoyang-ye.github.io/cerebellum-atlas/>

## Run it

Open `index.html` in a browser. There is no build step and no server code, and it works straight from disk.

To serve it locally instead (for example, to test on another device):

```bash
cd cerebellum-atlas
python3 -m http.server 8000      # then open http://localhost:8000
```

The page loads about 4.5 MB, mostly 3D meshes. These load only when you open the 3D atlas.

## Views

| View | What it shows |
| --- | --- |
| **3D atlas** | Human and mouse brains with the cerebellum, deep nuclei and their partners. Human lobules and nuclei come from the SUIT probabilistic atlas, fitted to the Allen Human Reference Atlas; mouse structures come from the Allen CCFv3. Choose a circuit (cerebro-cerebellar loops, olive, basal ganglia and substantia nigra, VTA/reward, fear and anxiety, navigation, feeding, vestibular, body, neuromodulators) to see evidence-graded pathways. *Animate signal flow* sends dots along each pathway from source to target to show its direction; the timing is schematic. In the neuromodulator circuit, a tag on each pathway names the transmitter it carries. Eyes, inner ear, gut and body are shown as approximate markers. |
| **Functional map** | A schematic flatmap of human cerebellar cortex (SUIT-style). Overlays show the motor, oculomotor, executive, language, social and emotional territories, plus a lesion map. |
| **Microcircuit** | The canonical circuit (mossy/parallel fibers, climbing fibers, Purkinje, Golgi, MLI, UBC, nuclei, olive), with animated signals and a toy eyeblink-conditioning model. You can switch off LTD and watch learning partly survive. |
| **Cells & molecules** | The parallel-fiber–Purkinje synapse: calcium sets the sign of plasticity (LTP vs. LTD), with zebrin modules, developmental lineage and disease genes. A matrix shows which neuromodulators (noradrenaline, serotonin, dopamine, acetylcholine, histamine), neuropeptides (orexin, CRF, CGRP, opioids, oxytocin, CCK, NPY, PACAP), retrograde and glial messengers, hormones and glycine act on which cells, with receptor, sign of effect and evidence grade. |
| **Across scales** | All 132 entities in seven level columns, linked by 290 graded connections, with 20 highlighted mechanistic chains. |
| **Evidence & gaps** | A domain × level matrix of curated papers, plus live PubMed counts fetched from your browser. It lists untested bridges, the weakest links, and open questions. |
| **Hypothesis lab** | Chain entities across levels. Each step is checked against the knowledge graph; the weakest step becomes the critical experiment, with predictions, alternative routes and methods. Export the result as Markdown. |
| **Library** | The 257 papers, filterable by level, domain, evidence type, species and year. Exports BibTeX. |

Every entity, link and paper opens in the side panel. Links in the panel are shareable (for example `#/scales/e/dentate`). Press `/` to search and `Esc` to close the panel.

## How the evidence is graded

Each connection has a **status**:

| Status | Meaning |
| --- | --- |
| Established | Replicated, causal and anatomical evidence across labs or species |
| Supported | Good evidence, but limited replication or indirect causality |
| Emerging | One or a few studies |
| Debated | Conflicting evidence |
| Hypothesis | Proposed, not directly tested |

Each paper also has an **evidence type**: causal manipulation, patients & lesions, recording & imaging, anatomy & profiling, review / meta-analysis, or theory & modeling. Map scores (0–3) are qualitative summaries of the cited studies.

## Project layout

```text
index.html              page shell
css/style.css           all styles
js/core.js              data indexes, DOM helpers, router, detail panel, search
js/main.js              navigation, global search, About dialog, start-up
js/views/*.js           one file per view
js/data/bundle.js       GENERATED: knowledge base + PubMed metadata
js/data/meshes_*.js     GENERATED: 3D meshes (quantized)
js/vendor/              three.js r147 + OrbitControls (MIT)
data/knowledge.json     entities, links, chains, open questions, flatmap, 3D circuits
data/papers.json        curated papers: PMID, evidence type, species, levels, domains, finding
data/pubmed_cache.json  cached PubMed metadata
data/meshes.json        which atlas structures to export for the 3D view
tools/build.py          validates the knowledge base and writes js/data/bundle.js
tools/build_meshes.py   builds js/data/meshes_*.js from the Allen and SUIT atlases
tools/jsonfmt.py        rewrites the data files in their compact, diff-friendly layout
```

## Editing the knowledge base

All content lives in two JSON files. After any edit, rebuild the bundle:

```bash
python3 tools/build.py            # fetches metadata for new PMIDs, validates, writes the bundle
python3 tools/build.py --offline  # no network; use cached metadata only
```

If you edit the JSON with a script, run `python3 tools/jsonfmt.py data/*.json` afterwards to restore the one-record-per-line layout.

`build.py` uses only the Python standard library. It checks every cross-reference (entity ids, paper keys, domains, levels, statuses) and stops with a clear message if anything is wrong. Setting `NCBI_API_KEY` raises the NCBI rate limit, but it is optional.

**Add a paper.**

1. Run `python3 tools/build.py --add 12345678`. It prints a template with the title and authors filled in.
2. Paste the template into `data/papers.json` and fill in `evidence`, `species`, `methods`, `levels`, `domains` and a one-sentence `finding`.
3. Cite the paper's `key` in the `refs` of an entity or link in `data/knowledge.json`, then rebuild.

**Add a connection.** Append to `links` in `data/knowledge.json`:

```json
{"s": "dentate", "t": "striatum", "rel": "disynaptic via intralaminar thalamus",
 "status": "supported", "kind": "anatomical", "refs": ["hoshi2005"], "note": "optional caveat"}
```

`s` and `t` are entity ids. `status` is one of the ids in `statuses` at the top of `knowledge.json`. `kind` is one of `mechanistic`, `anatomical`, `causal`, `functional`, `clinical`, `developmental`, `localization`, `theoretical` or `evolutionary`.

Neuromodulatory links can also carry `tx` (a transmitter code from `neuromodulation.tx`, drawn as a tag in the 3D view), `via` (the receptor, free text) and `sign` (`+`, `-`, `±` or `~`). A link from a messenger listed in `neuromodulation.groups` to a cell or pathway listed in `neuromodulation.targets` appears in the matrix in Cells & molecules.

**Add an entity, chain or open question.** Follow the existing records in `entities`, `chains` and `questions`. To place a new entity in the 3D view, add it to `atlas3d.sides` (which hemisphere) or to `atlas3d.aliases`.

## Rebuilding the 3D meshes (rarely needed)

```bash
pip install numpy scipy scikit-image nibabel trimesh fast_simplification   # fast_simplification is optional
python3 tools/build_meshes.py              # or: python3 tools/build_meshes.py mouse
```

On the first run the script downloads the Allen CCFv3 structure meshes, the BrainGlobe `allen_human_500um` atlas (about 160 MB) and the SUIT lobule atlas into `.cache/`. It decimates, smooths and aligns the meshes into one frame. For the human brain it extracts lobule and nucleus surfaces from SUIT and fits them to the Allen cerebellum (scaled ICP, mean surface distance about 0.8 mm). The output is `js/data/meshes_*.js`. `.cache/` is not needed to run the site.

## Publishing

The site is static, so any static host works. It is published with GitHub Pages at <https://zhuoyang-ye.github.io/cerebellum-atlas/>, built from the root of the `main` branch. The repository is private, but the site, and every file in the repository, is public. Every push to `main` republishes the site. The `.nojekyll` file tells Pages to serve the files as they are, and all paths are relative, so the site also works under a project subpath.

To publish a copy from another account with the [GitHub CLI](https://cli.github.com/):

```bash
gh repo create cerebellum-atlas --private --source . --push   # or --public
gh api "repos/$(gh api user --jq .login)/cerebellum-atlas/pages" -X POST \
  -f "source[branch]=main" -f "source[path]=/"
```

Pages from a private repository needs a paid GitHub plan. On a free plan, use `--public`.

Before you publish, read the terms below.

## Sources, credits and terms

- **Literature metadata**: PubMed (U.S. National Library of Medicine), retrieved through the NCBI E-utilities. Follow NCBI's usage guidelines: at most 3 requests per second without an API key. The Evidence & gaps view stays under that limit.
- **Mouse anatomy**: Allen Mouse Brain Common Coordinate Framework v3. Wang Q et al. (2020) *Cell* 181:936–953, doi:10.1016/j.cell.2020.04.007. © Allen Institute for Brain Science.
- **Human anatomy**: Allen Human Reference Atlas. Ding S-L et al. (2016) *J Comp Neurol* 524:3127–3481, doi:10.1002/cne.24080. © Allen Institute for Brain Science. Obtained through the BrainGlobe Atlas API (Claudi F et al., 2020, *J Open Source Softw* 5:2668).
- **Human cerebellar lobules and nuclei**: SUIT probabilistic atlases from the DiedrichsenLab [cerebellar_atlases](https://github.com/DiedrichsenLab/cerebellar_atlases) collection, CC BY. Diedrichsen J et al. (2009) *NeuroImage* 46:39–46, doi:10.1016/j.neuroimage.2009.01.045; Diedrichsen J et al. (2011) *NeuroImage* 54:1786–1794, doi:10.1016/j.neuroimage.2010.10.035.
- Allen Institute data are used under the Allen Institute [Terms of Use](https://alleninstitute.org/terms-of-use/). Check them, and their citation requirements, before public or commercial deployment.
- **three.js** r147, MIT license (`js/vendor/THREE_LICENSE`).

## Caveats

- The entity summaries, findings, link statuses and map scores were **drafted with AI assistance from PubMed abstracts**. They need review by cerebellum researchers before the site is used for teaching or published. Every claim is linked to its sources so it can be checked.
- Each paper's one-sentence finding was checked against its PubMed abstract. Albus (1971) is not in PubMed, and Hoffer et al. (1973) and Schulman et al. (1981) have no PubMed abstract, so their findings rest on the titles and say so.
- The library is a curated core of about 260 papers, not a systematic review. Use the live PubMed counts in Evidence & gaps to see the wider literature. The neuromodulator layer is thin in places: many effects come from a single slice study in one species, and where the oxytocin receptor is expressed in the cerebellum is still debated.
- Diagrams are schematic. The eyeblink model is a toy model for intuition, not a fitted model.
- Human lobules and nuclei come from a group probabilistic atlas fitted to a different brain, so their boundaries are approximate. The fastigial nucleus is barely resolved in SUIT and is drawn from a low probability threshold. Brainstem nuclei, the human neuromodulator source nuclei and body structures without meshes are placed approximately (italic labels).
