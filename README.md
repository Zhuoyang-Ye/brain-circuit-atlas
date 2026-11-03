# Cerebellum Atlas

An interactive, evidence-linked map of brain regions and their connections to the rest of the brain and body, starting with the cerebellum, the motor cortex and the prefrontal cortex. For each region it runs from molecules and cells through circuits and brain-wide loops to behavior, cognition and disease. Every connection carries an evidence grade and links to the PubMed papers behind it, and a hypothesis lab turns weak or missing links into testable experiments.

**Live site:** <https://zhuoyang-ye.github.io/cerebellum-atlas/>

## Run it

Open `index.html` in a browser. There is no build step and no server code, and it works straight from disk.

To serve it locally instead (for example, to test on another device):

```bash
cd cerebellum-atlas
python3 -m http.server 8000      # then open http://localhost:8000
```

The page itself loads about 1.4 MB. The 3D atlas loads the meshes for one species when you open it: about 2.6 MB for the human brain, 1.6 MB for the mouse and 1.4 MB for the macaque.

## Regions

Pick a region with the **Region** menu: at the top of the left panel in the 3D atlas, and at the top left of every other page. The site remembers the choice.

| Region | Entities | Links | Chains | Open questions | Papers |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cerebellum | 134 | 291 | 22 | 17 | 257 |
| Motor cortex | 46 | 62 | 10 | 6 | 65 |
| Prefrontal cortex | 51 | 69 | 10 | 6 | 57 |

Some structures, such as the thalamus, striatum, VTA, amygdala, hippocampus, dopamine and the spinal cord, are shared and appear in several regions. So do links between regions, such as cerebellar output reaching motor and prefrontal cortex through the thalamus. The totals are 194 entities, 410 links, 38 chains, 27 open questions and 371 papers.

The region sets:

- which circuits the 3D atlas offers and which structures it brings forward;
- which entities, links and chains Across scales shows (tick *All regions* to see everything);
- which papers, weak links and open questions Evidence & gaps, the Hypothesis lab and the Library start from (the Library can also *Include other regions*);
- the PubMed query used for live counts and searches.

The Functional map, Microcircuit and Cells & molecules views exist only for the cerebellum for now. In another region their menu entries are dimmed, and opening one shows a notice with a button to switch region.

## Views

| View | What it shows |
| --- | --- |
| **3D atlas** | Human, macaque and mouse brains with the current region and its partners. Human lobules and nuclei come from the SUIT probabilistic atlas, fitted to the Allen Human Reference Atlas, which supplies the other human structures (including the precentral gyrus); macaque structures come from the CHARM cortical and SARM subcortical atlases on the NIMH Macaque Template; mouse structures come from the Allen CCFv3. Choose a circuit to see evidence-graded pathways. For the cerebellum: cerebro-cerebellar loops, olive, basal ganglia and substantia nigra, VTA/reward, fear and anxiety, navigation, feeding, vestibular, body, neuromodulators. For the motor cortex: descending output, inputs to M1, cerebellar and basal ganglia loops, motor planning (ALM), the Go cue that releases a planned movement, and learning signals. For the prefrontal cortex: the working-memory network (mediodorsal thalamus, hippocampal input, frontal-parietal link), fear, safety and mood (amygdala, dorsal raphe), neuromodulator inputs, and the cerebellar loop. Arrowheads show each pathway's direction. For a loop or chain (the cerebro-cerebellar loops, for example), *Trace step by step* sends one pulse through the circuit in order, lights each structure as it arrives and lists the steps in the left panel; the order follows the circuit's pathways, and the timing is schematic. *Animate signal flow* (off by default) also sends dots along every pathway. In the neuromodulator circuit, a tag on each pathway names the transmitter it carries. Eyes, inner ear, gut and body are shown as approximate markers. |
| **Functional map** | A schematic flatmap of human cerebellar cortex (SUIT-style). Overlays show the motor, oculomotor, executive, language, social and emotional territories, plus a lesion map. |
| **Microcircuit** | The canonical circuit (mossy/parallel fibers, climbing fibers, Purkinje, Golgi, MLI, UBC, nuclei, olive), with animated signals and a toy eyeblink-conditioning model. You can switch off LTD and watch learning partly survive. |
| **Cells & molecules** | The parallel-fiber–Purkinje synapse: calcium sets the sign of plasticity (LTP vs. LTD), with zebrin modules, developmental lineage and disease genes. A matrix shows which neuromodulators (noradrenaline, serotonin, dopamine, acetylcholine, histamine), neuropeptides (orexin, CRF, CGRP, opioids, oxytocin, CCK, NPY, PACAP), retrograde and glial messengers, hormones and glycine act on which cells, with receptor, sign of effect and evidence grade. |
| **Across scales** | The region's entities in seven level columns, linked by graded connections, with highlighted mechanistic chains (all regions together: 194 entities, 410 links, 38 chains). |
| **Evidence & gaps** | A domain × level matrix of the region's curated papers, plus live PubMed counts fetched from your browser. It lists untested bridges, the weakest links, and open questions. |
| **Hypothesis lab** | Chain entities across levels. Each step is checked against the knowledge graph; the weakest step becomes the critical experiment, with predictions, alternative routes and methods. Export the result as Markdown. |
| **Library** | The region's papers (371 in all), filterable by level, domain, evidence type, species and year. Exports BibTeX. |

Every entity, link and paper opens in the side panel. Links in the panel are shareable (for example `#/scales/e/dentate`). Press `/` to search and `Esc` to close the panel. The sun/moon button at the top right switches between light and dark mode; until you choose, the site follows your system setting.

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
data/knowledge.json     regions, entities, links, chains, open questions, flatmap, 3D circuits
data/papers.json        curated papers: PMID, regions, evidence type, species, levels, domains, finding
data/pubmed_cache.json  cached PubMed metadata
data/meshes.json        which atlas structures to export for the 3D view
tools/build.py          validates the knowledge base and writes js/data/bundle.js
tools/build_meshes.py   builds js/data/meshes_*.js from the Allen, SUIT and NMT (CHARM, SARM) atlases
tools/jsonfmt.py        rewrites the data files in their compact, diff-friendly layout
```

## Editing the knowledge base

All content lives in two JSON files. After any edit, rebuild the bundle:

```bash
python3 tools/build.py            # fetches metadata for new PMIDs, validates, writes the bundle
python3 tools/build.py --offline  # no network; use cached metadata only
```

If you edit the JSON with a script, run `python3 tools/jsonfmt.py data/*.json` afterwards to restore the one-record-per-line layout.

`build.py` uses only the Python standard library. It checks every cross-reference (entity ids, paper keys, region ids, domains, levels, statuses) and stops with a clear message if anything is wrong. Setting `NCBI_API_KEY` raises the NCBI rate limit, but it is optional.

**Add a paper.**

1. Run `python3 tools/build.py --add 12345678`. It prints a template with the title and authors filled in.
2. Paste the template into `data/papers.json` and fill in `regions` (one or more region ids, for example `["motor-cortex"]`), `evidence`, `species`, `methods`, `levels`, `domains` and a one-sentence `finding`. Check the finding against the abstract.
3. Cite the paper's `key` in the `refs` of an entity or link in `data/knowledge.json`, then rebuild.

**Add a connection.** Append to `links` in `data/knowledge.json`:

```json
{"s": "dentate", "t": "striatum", "rel": "disynaptic via intralaminar thalamus",
 "status": "supported", "kind": "anatomical", "refs": ["hoshi2005"], "note": "optional caveat"}
```

`s` and `t` are entity ids. `status` is one of the ids in `statuses` at the top of `knowledge.json`. `kind` is one of `mechanistic`, `anatomical`, `causal`, `functional`, `clinical`, `developmental`, `localization`, `theoretical` or `evolutionary`.

Neuromodulatory links can also carry `tx` (a transmitter code from `neuromodulation.tx`, drawn as a tag in the 3D view), `via` (the receptor, free text) and `sign` (`+`, `-`, `±` or `~`). A link from a messenger listed in `neuromodulation.groups` to a cell or pathway listed in `neuromodulation.targets` appears in the matrix in Cells & molecules.

**Add an entity, chain or open question.** Follow the existing records in `entities`, `chains` and `questions`. Give an entity a `region` if it belongs to one region. Leave it out for structures and messengers shared by several regions, such as the thalamus or dopamine. To place a new entity in the 3D view, add it to `atlas3d.sides` (which hemisphere) or to `atlas3d.aliases`.

Links, chains and questions get their regions when the bundle is built, so they don't carry a region field:

- **Links:** a link belongs to the regions of its region-tagged endpoints. It also belongs to the regions that all its cited papers share; if the papers share none, it belongs to every region any of them covers.
- **Chains:** a chain takes the regions of its tagged entities. If none of them is tagged, it takes the regions of its links.
- **Questions:** a question takes the regions of its tagged entities, or else those of its cited papers.

Shared entities show up in a region when one of that region's links, chains or questions uses them.

## Adding a brain region

1. **Region record.** Add a record to `regions` in `knowledge.json` with these fields:
   - `id` and `label`;
   - `entity`, the entity that stands for the whole region;
   - `query`, a PubMed term added to the region's searches and live counts;
   - `views`, the views that cover this region;
   - `view`, a camera preset in `VIEWS` in `js/views/atlas3d.js` (add one for each species);
   - `intro`, a `{title, text}` object for the 3D atlas introduction.

   Optional: `speciesNote` (`{human, mouse, macaque}`), and `levelDesc`, `levelQueries` and `methods`, keyed by level, which replace the defaults for this region.
2. **Papers.** Collect papers and add each with `regions` set, checking every finding against its abstract.
3. **Content.** Write the entities (with `region`), links, chains and open questions, citing those papers. Keep each status within what the cited abstracts show.
4. **3D.** Add `atlas3d.circuits` with `"region": "<id>"`. Map structures to entities in `data/meshes.json` (Allen structure ids for the human and mouse, CHARM or SARM labels for the macaque; a list of ids in `src` merges several structures into one), or add an anchor in `tools/build_meshes.py` for a structure without a mesh, then rebuild the meshes. If one entity covers several entities, list them in `atlas3d.composite` (for example, motor cortex = M1 + premotor).
5. **Build.** Run `python3 tools/build.py`, which validates the region ids and prints per-region counts. Then open every view with the new region selected.

## Rebuilding the 3D meshes (rarely needed)

```bash
pip install numpy scipy scikit-image nibabel trimesh fast_simplification   # fast_simplification is optional
python3 tools/build_meshes.py              # the species in atlas3d.species; or name one: python3 tools/build_meshes.py mouse
```

On the first run the script downloads the Allen CCFv3 structure meshes, the BrainGlobe `allen_human_500um` atlas (about 160 MB), the SUIT lobule atlas and the NIMH Macaque Template v2.0 archive (`NMT_v2.0_sym.tgz`, about 270 MB, of which only the 0.5 mm volumes and the label tables are unpacked) into `.cache/`. It decimates, smooths and aligns the meshes into one frame. For the human brain it extracts lobule and nucleus surfaces from SUIT and fits them to the Allen cerebellum (scaled ICP, mean surface distance about 0.8 mm). For the macaque it computes surfaces from the CHARM and SARM label volumes. The output is `js/data/meshes_*.js`. `.cache/` is not needed to run the site.

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
- **Macaque anatomy**: the [NIMH Macaque Template](https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/nonhuman/macaque_tempatl/template_nmtv2.html) v2.0 (NMT v2, symmetric, 0.5 mm), distributed with AFNI. Seidlitz J et al. (2018) *NeuroImage* 170:121–131, doi:10.1016/j.neuroimage.2017.04.063; Jung B et al. (2021) *NeuroImage* 235:117997, doi:10.1016/j.neuroimage.2021.117997. Cortical areas: the Cortical Hierarchy Atlas of the Rhesus Macaque (CHARM; Jung et al., 2021). Subcortical structures and the cerebellum: the Subcortical Atlas of the Rhesus Macaque (SARM). Hartig R et al. (2021) *NeuroImage* 235:117996, doi:10.1016/j.neuroimage.2021.117996. The surfaces were computed here from the atlas labels. The AFNI documentation asks users to cite these papers; we found no explicit licence, so check the terms before reusing the meshes.
- Allen Institute data are used under the Allen Institute [Terms of Use](https://alleninstitute.org/terms-of-use/). Check them, and their citation requirements, before public or commercial deployment.
- **three.js** r147, MIT license (`js/vendor/THREE_LICENSE`).

### Switching off the macaque brain

The NMT v2, CHARM and SARM atlases come without an explicit licence. Their documentation asks users to cite the three papers above, and the 3D canvas, the About dialog and this README do. If their terms turn out not to allow this use, switch the macaque off:

1. In `data/knowledge.json`, remove `"macaque"` from `atlas3d.species`.
2. Delete the derived surfaces: `git rm js/data/meshes_macaque.js`.
3. Run `python3 tools/build.py` (it warns until the file is gone) and commit.

The Macaque button and its credits disappear, and `tools/build_meshes.py` no longer builds it. The same switch works for any species. Older versions of the file stay in the repository's history, which is private; GitHub Pages serves only the current files.

## Caveats

- The entity summaries, findings, link statuses and map scores were **drafted with AI assistance from PubMed abstracts**. They need review by researchers in each field before the site is used for teaching or published. Every claim is linked to its sources so it can be checked.
- Each paper's one-sentence finding was checked against its PubMed abstract. Albus (1971) is not in PubMed, and Hoffer et al. (1973) and Schulman et al. (1981) have no PubMed abstract, so their findings rest on the titles and say so.
- The library is a curated core of about 370 papers, not a systematic review. Use the live PubMed counts in Evidence & gaps to see the wider literature. The neuromodulator layer is thin in places: many effects come from a single slice study in one species, and where the oxytocin receptor is expressed in the cerebellum is still debated.
- The motor and prefrontal cortex are newer and thinner regions (65 and 57 papers), mostly from mice, rats and monkeys, and many of their links rest on a single study. Rodent and primate prefrontal areas are not simple homologues, so the site keeps rodent prelimbic and infralimbic cortex apart from primate dorsolateral, ventromedial and subgenual areas, and tags each claim with its species.
- Macaque structures are surfaces computed from atlas labels on a population template (0.5 mm voxels) and then smoothed, so small nuclei are approximate. The macaque substantia nigra is drawn whole, and the tuberomammillary nucleus and brainstem serotonin neurons are placed approximately. Mouse ALM is shown at the macaque and human premotor areas as a possible homologue.
- In the human 3D brain, M1 is drawn as the whole precentral gyrus, because the Allen human atlas does not separate M1 from premotor cortex. The human premotor areas, primary somatosensory cortex and basal forebrain have no mesh and are placed approximately. In the mouse, the secondary motor area (MOs) stands in for premotor cortex and includes ALM. Human prefrontal areas are drawn as whole gyri: the middle frontal gyrus for dorsolateral PFC, the orbital gyri for orbitofrontal cortex, the gyrus rectus for ventromedial PFC, the rostral cingulate gyrus for the ACC and the subcallosal gyrus for the subgenual cingulate, so their borders are approximate. The human dorsal raphe has no mesh and is placed approximately.
- Diagrams are schematic. The eyeblink model is a toy model for intuition, not a fitted model.
- Human lobules and nuclei come from a group probabilistic atlas fitted to a different brain, so their boundaries are approximate. The fastigial nucleus is barely resolved in SUIT and is drawn from a low probability threshold. Brainstem nuclei, the human neuromodulator source nuclei and body structures without meshes are placed approximately (italic labels).
