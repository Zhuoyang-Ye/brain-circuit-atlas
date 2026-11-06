# Brain Circuit Atlas (v0.2)

An interactive, evidence-linked map of brain regions and their connections to the rest of the brain and body, covering the cerebellum, motor cortex, prefrontal cortex, basal ganglia, hippocampus, amygdala, visual cortex, insula, olfactory system, and the basal forebrain, alongside two invertebrate brains: the octopus brain, which evolved separately, and the fruit fly brain, whose wiring has been mapped across the whole brain by electron microscopy. For each region it runs from molecules and cells through circuits and brain-wide loops to behavior, cognition and disease. Every connection carries an evidence grade and links to the PubMed papers behind it, and a hypothesis lab turns weak or missing links into testable experiments.

**Live site:** <https://zhuoyang-ye.github.io/brain-circuit-atlas/>

## Run it

Open `index.html` in a browser. There is no build step and no server code, and it works straight from disk.

To serve it locally instead (for example, to test on another device):

```bash
cd brain-circuit-atlas
python3 -m http.server 8000      # then open http://localhost:8000
```

The page itself loads about 1.5 MB. The 3D atlas loads the meshes for one species when you open it: about 2.9 MB for the human brain, 1.8 MB for the mouse, 1.6 MB for the macaque, 0.5 MB for the octopus and 0.7 MB for the fruit fly.

## macOS Desktop App & Local Backend

Brain Circuit Atlas includes a native macOS desktop application (< 7 MB) with a local Python backend, SQLite persistence, and Cloudflare R2 cloud synchronization:

- **Launch the Mac App:**
  ```bash
  open "dist/Brain Circuit Atlas.app"
  ```
- **Local Dev Server:**
  ```bash
  ./launch.sh                    # runs backend on http://127.0.0.1:8765/
  ```
- **Build the Mac App:**
  ```bash
  ./app/build_mac_app.sh         # compiles Swift ARM64 app into dist/
  ```

**Features enabled by the desktop app:**
- **Persistent Hypotheses & Notes:** Stored in local SQLite (`~/Library/Application Support/BrainCircuitAtlas/atlas.db`).
- **PubMed Caching:** Fast local SQLite lookups in Evidence & Gaps that eliminate NCBI 429 rate limits.
- **Cloudflare R2 Integration:** Store and sync 3D brain meshes to Cloudflare R2 (10 GB free tier with \$0 download fees).
- **Website Sync:** Rebuild and stage updated data bundles for GitHub Pages with one click from the UI.

## Regions

Pick a region with the **Region** menu: in the left panel of the 3D atlas, under the species, and at the top left of every other page. The site remembers the choice.

| Region | Entities | Links | Chains | Open questions | Papers |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cerebellum | 143 | 298 | 24 | 19 | 259 |
| Motor cortex | 51 | 65 | 12 | 6 | 67 |
| Prefrontal cortex | 72 | 94 | 14 | 7 | 67 |
| Basal ganglia | 44 | 52 | 11 | 5 | 41 |
| Hippocampus | 54 | 59 | 10 | 7 | 71 |
| Amygdala | 54 | 61 | 14 | 7 | 62 |
| Visual cortex | 39 | 42 | 9 | 5 | 51 |
| Insula | 34 | 34 | 4 | 5 | 39 |
| Olfactory system | 24 | 25 | 4 | 4 | 39 |
| Basal forebrain | 28 | 34 | 4 | 3 | 11 |
| Octopus brain | 25 | 28 | 3 | 4 | 49 |
| Fruit fly brain | 68 | 94 | 8 | 7 | 98 |

Some structures, such as the thalamus, striatum, VTA, amygdala, hippocampus, lateral hypothalamus, basal forebrain, dopamine and the spinal cord, are shared and appear in several regions. So do links between regions, such as cerebellar output reaching motor and prefrontal cortex through the thalamus, septohippocampal acetylcholine/GABA cotransmission, striatal regulation of amygdalar acetylcholine via substantia innominata, or ascending arousal projections from brainstem to default mode network. The totals are 378 entities, 773 links, 93 chains, 68 open questions and 805 papers.

The region sets:

- which circuits the 3D atlas offers and which structures it brings forward;
- which entities, links and chains Across scales shows (tick *All regions* to see everything);
- which papers, weak links and open questions Evidence & gaps, the Hypothesis lab and the Library start from (the Library can also *Include other regions*);
- the PubMed query used for live counts and searches.

The Functional map, Microcircuit and Cells & molecules views exist for the cerebellum and the fruit fly brain, each with its own version (the fly's are in `js/views/fly_*.js`). In another region their menu entries are dimmed, and opening one shows a notice with buttons to switch region.

## Views

| View | What it shows |
| --- | --- |
| **3D atlas** | Human, macaque and mouse brains with the current region and its partners, a schematic octopus brain for the octopus region and a fruit fly brain for the fruit fly region (choosing the octopus or the fruit fly switches to its region, and a mammalian region switches back). Human lobules and nuclei come from the SUIT probabilistic atlas, fitted to the Allen Human Reference Atlas, which supplies the other human structures (including the precentral gyrus); macaque structures come from the CHARM cortical and SARM subcortical atlases on the NIMH Macaque Template; mouse structures come from the Allen CCFv3; fruit fly neuropils come from the Janelia FlyEM male CNS connectome. Choose a circuit to see evidence-graded pathways. For the cerebellum: cerebro-cerebellar loops, olive, basal ganglia and substantia nigra, VTA/reward, fear and anxiety, navigation, feeding, vestibular, body, neuromodulators. For the motor cortex: descending output, inputs to M1, cerebellar and basal ganglia loops, motor planning (ALM), the Go cue that releases a planned movement, and learning signals. For the prefrontal cortex: the working-memory network (mediodorsal thalamus, hippocampal input, frontal-parietal link), fear, safety and mood (amygdala, dorsal raphe), neuromodulator inputs, and the cerebellar loop. For the basal ganglia: the direct, indirect and hyperdirect pathways, nigral dopamine and its inputs, the two cell types of the external pallidum, the nigral gate on saccades, and the loop with the cerebellum. For the hippocampus: the trisynaptic pathway with its CA2 route, the outputs of the ventral hippocampus (prefrontal cortex, accumbens, amygdala, lateral hypothalamus), the link with prefrontal cortex, and cerebellar input. For the amygdala: the fear pathway from the auditory thalamus through the lateral and central amygdala to the PAG and lateral hypothalamus, intercalated cells and extinction, basolateral outputs, prefrontal connections, and cerebellar input. For the visual cortex: the pathway from the eye through the lateral geniculate nucleus to V1 and on to V4 and MT, the ventral and dorsal streams, top-down effects of the frontal eye field, amygdala and basal forebrain, and visual input to the cerebellum through the pontine nuclei. For the insula: taste from the thalamus through the gustatory cortex to the amygdala, hunger signals reaching the insula from the basolateral amygdala, posterior insula outputs to the central amygdala and accumbens, and the anterior insula's coupling with the anterior cingulate. For the olfactory system: sensory neurons to the olfactory bulb and on to the piriform cortex and cortical amygdala, and olfactory input to the orbitofrontal and entorhinal cortex. For the octopus brain: vision to the vertical lobe, inside the vertical lobe, optic lobe connections, and the brain and arms. For the fruit fly brain: smell from the antennal lobe to the mushroom body and lateral horn, mushroom body outputs, the anterior visual pathway to the ellipsoid body, motion vision to escape, and the brain to the nerve cord. Arrowheads show each pathway's direction. For a loop or chain (the cerebro-cerebellar loops, for example), *Trace step by step* sends one pulse through the circuit in order, lights each structure as it arrives and lists the steps in the left panel; the order follows the circuit's pathways, and the timing is schematic. *Animate signal flow* (off by default) also sends dots along every pathway. Every region has a *Neuromodulators* entry: the region's own neuromodulator circuit where one is curated (the cerebellum, the prefrontal cortex and the octopus), otherwise one built from its pathways that carry a transmitter tag, framed by the camera; where none is curated yet, the entry says so. The mammalian cortical and subcortical regions draw their modulatory inputs from the brainstem and basal forebrain nuclei (for example, locus coeruleus noradrenaline and co-released dopamine, raphe serotonin and basal-forebrain acetylcholine to the hippocampus, amygdala, visual cortex, insula and olfactory bulb; nigral and VTA dopamine, mesopontine acetylcholine and raphe serotonin to the basal ganglia); the fruit fly shows the octopaminergic broadcast from its subesophageal ventral unpaired median neurons, and the octopus the gonadotropin-releasing-hormone drive from the olfactory lobe to the optic gland. On these pathways, the tube, its two arrowheads and its tag take the transmitter's colour, and a key, in the left panel and at the foot of the canvas, names each transmitter and its source (NA noradrenaline, 5-HT serotonin, DA dopamine, ACh acetylcholine, HA histamine, OX orexin, CRF corticotropin-releasing factor, OA octopamine, GnRH gonadotropin-releasing hormone). While pathways are drawn, only the structures they touch keep their colours, in a light tint and see-through so that the pathways inside them show, and the rest of the brain turns grey; the structure under the pointer is drawn deep and solid. Eyes, inner ear, gut and body, and the fly's photoreceptors and olfactory and gustatory receptor neurons, are shown as approximate markers. The switch next to the theme button puts the structure names on the model or in a colour-coded list at the side, which keeps the model clean: there, the structures of the chosen circuit (up to eight) take a colour of their own, the rest keep their atlas colours, and hovering a name lights the structure and names it on the model. On the model, labels hold their place as the view turns; where they would overlap, some fade out until there is room, so zooming in names more structures. |
| **Functional map** | Cerebellum: a schematic flatmap of human cerebellar cortex (SUIT-style). Overlays show the motor, oculomotor, executive, language, social and emotional territories, plus a lesion map. Fruit fly: the central brain's resting-state functional connectivity (correlated calcium activity, 20 flies) beside its structural connectivity (neurons linking each pair of regions in the hemibrain connectome), recomputed from the data of Turner, Mann & Clandinin (2021) for 37 regions: a frontal map of the regions with the strongest connections by activity, by wiring or by how far the two disagree; the two matrices; their correlation over all region pairs (r = 0.72); and the regions whose activity departs most from their wiring. Regions can also be coloured by the functions the atlas links to them. |
| **Microcircuit** | Cerebellum: the canonical circuit (mossy/parallel fibers, climbing fibers, Purkinje, Golgi, MLI, UBC, nuclei, olive), with animated signals and a toy eyeblink-conditioning model. You can switch off LTD and watch learning partly survive. Fruit fly: the mushroom body (receptor neurons, antennal lobe, projection neurons, lateral horn, Kenyon cells, APL, DPM, PPL1 and PAM dopamine neurons, compartments and output neurons), with animated signals and a toy odour-conditioning model: shock or sugar, forward or backward pairing, odour similarity, and wild-type, APL-silenced, DopR1 and rutabaga flies. |
| **Cells & molecules** | Cerebellum: the parallel-fiber–Purkinje synapse: calcium sets the sign of plasticity (LTP vs. LTD), with zebrin modules, developmental lineage and disease genes. A matrix shows which neuromodulators (noradrenaline, serotonin, dopamine, acetylcholine, histamine), neuropeptides (orexin, CRF, CGRP, opioids, oxytocin, CCK, NPY, PACAP), retrograde and glial messengers, hormones and glycine act on which cells, with receptor, sign of effect and evidence grade. Fruit fly: the Kenyon cell output synapse, where the order of odour and dopamine sets the sign of plasticity (rutabaga, cAMP and DopR1 for depression, DopR2 for potentiation), with dunce, rutabaga and DopR1 mutants; the learning circuit's neuromodulators and neuropeptides (dopamine, octopamine, serotonin, neuropeptide F, Amnesiac); mushroom body and projection neuron development; and genes and fly models of human disease. |
| **Across scales** | The region's entities in seven level columns, linked by graded connections, with highlighted mechanistic chains (all regions together: 369 entities, 720 links, 89 chains). |
| **Evidence & gaps** | A domain × level matrix of the region's curated papers, plus live PubMed counts fetched from your browser. It lists untested bridges, the weakest links, and open questions. |
| **Hypothesis lab** | Chain entities across levels. Each step is checked against the knowledge graph; the weakest step becomes the critical experiment, with predictions, alternative routes and methods. Export the result as Markdown. |
| **Library** | The region's papers (757 in all), filterable by level, domain, evidence type, species and year. Exports BibTeX. |

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
js/views/*.js           one file per view (fly_*.js: the fruit fly's versions of three of them)
js/data/bundle.js       GENERATED: knowledge base + PubMed metadata
js/data/meshes_*.js     GENERATED: 3D meshes (quantized)
js/vendor/              three.js r147 + OrbitControls (MIT)
data/knowledge.json     regions, entities, links, chains, open questions, flatmap, 3D circuits
data/papers.json        curated papers: PMID, regions, evidence type, species, levels, domains, finding
data/pubmed_cache.json  cached PubMed metadata
data/meshes.json        which atlas structures to export for the 3D view
data/fly_connectivity.json  GENERATED: fly structural and functional connectivity (tools/build_fly_fc.py)
tools/build.py          validates the knowledge base and writes js/data/bundle.js
tools/build_meshes.py   builds js/data/meshes_*.js from the Allen, SUIT and NMT (CHARM, SARM) atlases
tools/build_octopus.py  draws the schematic octopus brain (js/data/meshes_octopus.js)
tools/build_fly.py      builds js/data/meshes_fly.js from the Janelia FlyEM male CNS neuropils
tools/build_fly_fc.py   recomputes data/fly_connectivity.json from the Turner et al. (2021) data
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

   A region can also have its own version of the Functional map, Microcircuit or Cells & molecules view: list the view in `views`, register it in a script with `CA.registerVariant('<view>', '<region id>', { mount, unmount })`, and put its curated settings under `regionViews.<region id>.<view>` in `knowledge.json`, which `build.py` checks (the fruit fly's are the example).
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

The octopus and the fruit fly have scripts of their own (`build_meshes.py` skips them):

```bash
python3 tools/build_octopus.py             # schematic octopus brain, from the shapes in data/meshes.json
python3 tools/build_fly.py                 # fruit fly neuropils
```

The fruit fly's Functional map has a data file of its own, recomputed from published data (needs numpy, scipy, pandas, nibabel and scikit-image):

```bash
python3 tools/build_fly_fc.py              # writes data/fly_connectivity.json; then run tools/build.py
```

On its first run it downloads the data of Turner, Mann & Clandinin (2021) from figshare (about 250 MB) into `.cache/turner2021/`. Following the authors' code (github.com/mhturner/SC-FC), it correlates each region's high-pass filtered calcium signal with every other region's in each of 20 flies, averages the Fisher z values, takes the hemibrain cell counts between regions, and places each region by its centroid in the atlas the imaging was registered to. The data's region responses are pickled pandas tables; the script reads them with an unpickler that allows only the numpy and pandas constructors they contain. The recomputed structure-function correlation is r = 0.72 (the paper reports 0.74).

On its first run `build_fly.py` downloads the neuropil meshes of the male CNS connectome (about 100 MB) from Janelia's public bucket into `.cache/fly_malecns/`. It voxelizes and re-surfaces each neuropil so that it simplifies cleanly, turns the volume's axes (toward the fly's left, ventral, posterior) into the site's frame (toward its right, dorsal, anterior), and scales the brain to the same size as the other species. The neuropils it exports, and which entities they stand for, are listed under `"fly"` in `data/meshes.json`.

## Publishing

The site is static, so any static host works. It is published with GitHub Pages at <https://zhuoyang-ye.github.io/brain-circuit-atlas/>, built from the root of the `main` branch. The repository is private, but the site, and every file in the repository, is public. Every push to `main` republishes the site. The `.nojekyll` file tells Pages to serve the files as they are, and all paths are relative, so the site also works under a project subpath.

To publish a copy from another account with the [GitHub CLI](https://cli.github.com/):

```bash
gh repo create brain-circuit-atlas --private --source . --push   # or --public
gh api "repos/$(gh api user --jq .login)/brain-circuit-atlas/pages" -X POST \
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
- **Fruit fly anatomy**: neuropil meshes (regions of interest) of the Janelia FlyEM [male CNS connectome](https://male-cns.janelia.org/), licensed CC BY. Berg S et al. (2026) *Cell* 189:5504–5526, doi:10.1016/j.cell.2026.08.015. Re-surfaced and simplified here.
- **Fly structural and functional connectivity**: recomputed from "Drosophila central brain connectivity" (figshare, doi:10.6084/m9.figshare.13349282, v3), the data of Turner MH, Mann K, Clandinin TR (2021) *Curr Biol* 31:2386–2394, doi:10.1016/j.cub.2021.03.004, released under the MIT license (the notice is in `data/fly_connectivity.json`). Its structural measures come from the hemibrain connectome, Scheffer LK et al. (2020) *eLife* 9:e57443, doi:10.7554/eLife.57443, and its regions from the insect brain nomenclature of Ito K et al. (2014) *Neuron* 81:755–765.
- **three.js** r147, MIT license (`js/vendor/THREE_LICENSE`).

### Switching off the macaque brain

The NMT v2, CHARM and SARM atlases come without an explicit licence. Their documentation asks users to cite the three papers above, and the 3D canvas, the About dialog and this README do. If their terms turn out not to allow this use, switch the macaque off:

1. In `data/knowledge.json`, remove `"macaque"` from `atlas3d.species`.
2. Delete the derived surfaces: `git rm js/data/meshes_macaque.js`.
3. Run `python3 tools/build.py` (it warns until the file is gone) and commit.

The Macaque button and its credits disappear, and `tools/build_meshes.py` no longer builds it. The same switch works for any species. Older versions of the file stay in the repository's history, which is private; GitHub Pages serves only the current files.

## Caveats

- The entity summaries, findings, link statuses and map scores were **drafted with AI assistance from PubMed abstracts**. They need review by researchers in each field before the site is used for teaching or published. Every claim is linked to its sources so it can be checked.
- Each paper's one-sentence finding was checked against its PubMed abstract. Albus (1971) is not in PubMed, and six papers have no PubMed abstract (Scoville & Milner, 1957; O'Keefe & Dostrovsky, 1971; Hoffer et al., 1973; Weiskrantz et al., 1974; Schulman et al., 1981; Morris et al., 1982), so their findings rest on the titles and say so.
- The library is a curated core of about 790 papers, not a systematic review. Use the live PubMed counts in Evidence & gaps to see the wider literature. The neuromodulator layer is thin in places: many effects come from a single slice study in one species, the modulatory inputs curated for each region are a representative sample rather than a complete inventory, and where the oxytocin receptor is expressed in the cerebellum is still debated.
- The motor cortex, prefrontal cortex, basal ganglia, hippocampus, amygdala, visual cortex, insula, olfactory system, octopus brain and fruit fly brain are newer and thinner regions (65, 60, 35, 62, 53, 45, 33, 31, 46 and 96 papers), mostly from mice, rats and monkeys (octopuses for the octopus brain, *Drosophila melanogaster* for the fruit fly), and many of their links rest on a single study. Rodent and primate prefrontal areas are not simple homologues, so the site keeps rodent prelimbic and infralimbic cortex apart from primate dorsolateral, ventromedial and subgenual areas, and tags each claim with its species.
- Macaque structures are surfaces computed from atlas labels on a population template (0.5 mm voxels) and then smoothed, so small nuclei are approximate. The macaque substantia nigra and hippocampus are each drawn whole, so the reticular part of the nigra and the anterior and posterior hippocampus are placed approximately and the hippocampal fields are shown within the hippocampus, and the tuberomammillary nucleus and brainstem serotonin neurons are placed approximately. SARM has no label for the amygdala's intercalated cells, so they are placed approximately. Mouse ALM is shown at the macaque and human premotor areas as a possible homologue.
- The octopus brain in 3D is a schematic drawn for this site (`tools/build_octopus.py`, shapes in `data/meshes.json`), not a scan or an atlas volume: lobe shapes, sizes and positions are approximate and only for orientation, so every octopus label carries ≈. Octopus findings come from several species, mainly *Octopus vulgaris* and *O. bimaculoides*.
- The fruit fly brain in 3D shows neuropils of the Janelia male CNS connectome (one male fly), re-surfaced and simplified for the web (`tools/build_fly.py`). The nerve cord is drawn as a faint outline, like the brain surface. Cell types are shown in the neuropil that holds them: Kenyon cells and the mushroom body's output, dopamine and APL neurons in the mushroom body, projection neurons in the antennal lobe, ring and E-PG neurons in the ellipsoid body, T4/T5 cells in the lobula plate, LC neurons in the lobula, and descending neurons, with the giant fibre, at the neck connective. Photoreceptors and olfactory and gustatory receptor neurons lie outside the brain and are placed approximately; the feeding-command (Fdg) neurons are not placed. Each fly link has a kind, which keeps structural links (anatomical, mostly from electron-microscopy connectomes) apart from those based on activity, behaviour, manipulation or models, and the connectomes cited come from different flies, female and male, so structural and functional connectivity never come from the same brain.
- In the human 3D brain, M1 is drawn as the whole precentral gyrus, because the Allen human atlas does not separate M1 from premotor cortex. The human premotor areas, primary somatosensory cortex and basal forebrain have no mesh and are placed approximately. In the mouse, the secondary motor area (MOs) stands in for premotor cortex and includes ALM. Human prefrontal areas are drawn as whole gyri: the middle frontal gyrus for dorsolateral PFC, the orbital gyri for orbitofrontal cortex, the gyrus rectus for ventromedial PFC, the rostral cingulate gyrus for the ACC and the subcallosal gyrus for the subgenual cingulate, so their borders are approximate. The human dorsal raphe and substantia nigra (compact and reticular parts) have no mesh and are placed approximately. The mouse internal globus pallidus (the entopeduncular nucleus in rodents) is drawn from the Allen CCFv3 label of that name. The human atlas does not separate the hippocampal fields, so the dentate gyrus, CA fields and subiculum are shown in the hippocampus; its head stands for the anterior (ventral) and its body and tail for the posterior (dorsal) hippocampus, and the entorhinal cortex is drawn as the anterior parahippocampal gyrus. In the mouse, the dorsal and ventral hippocampus are placed approximately within the hippocampal fields. The human atlas does not separate the amygdala's nuclei, so the lateral, basal, central, medial and intercalated nuclei are shown in the amygdala, and the medial geniculate nucleus is shown in the thalamus. In the mouse, the basal amygdala is drawn as the basolateral and basomedial nuclei together. The human atlas does not mark visual areas: V1 is drawn as the occipital pole, cuneus and lingual gyrus, which also hold V2 and V3; V4 as the occipital part of the fusiform gyrus; the fusiform face area as its temporal part; and inferotemporal cortex as the inferior temporal gyrus. Human MT is placed approximately, between the inferior occipital gyrus and the back of the middle temporal gyrus, and the lateral geniculate nucleus is shown in the thalamus. In the mouse, the higher visual areas LM, AL, AM, PM, LI and P are drawn together, and the anterior and rostrolateral areas belong to the posterior parietal cortex mesh; V4, MT, inferotemporal cortex, the fusiform face area and the frontal eye field are not placed in the mouse, and the fusiform face area is not placed in the macaque. The human insula is drawn as the short (anterior) and long (posterior) insular gyri; the taste cortex, which the human atlas does not mark, and the von Economo neurons are shown in the anterior insula. In the mouse, the anterior insula is drawn as the dorsal and ventral agranular insular areas and the posterior insula as the posterior agranular insular and visceral areas, with the gustatory areas separate; in the macaque, the taste cortex is shown in the anterior insula, and von Economo neurons are placed only in the human brain. The human cortical amygdala is shown in the amygdala; the macaque template does not include the olfactory bulb, so it is placed approximately under the orbital surface; and olfactory sensory neurons are placed approximately in front of the bulb in every species. The vomeronasal organ is not placed.
- The fruit fly's Functional map compares activity and wiring measured in different animals: spontaneous calcium activity in 20 flies, and the hemibrain connectome of one fly, through a shared atlas. It is a cross-animal comparison, not structure and function from one brain, and the activity is spontaneous, recorded without a task. The imaging covered the right side of the central brain and the midline, so 37 regions, most of them right-hemisphere ones, are compared. Region positions are atlas centroids seen from the front, nudged apart so that labels can be read.
- The fly disease models are models: human genes expressed in flies, or fly genes lost, reproduce some features of the human disorders, and the links to those disorders are graded by the fly evidence alone.
- Diagrams are schematic. The eyeblink, odour-conditioning and Kenyon cell synapse models are toy models for intuition, not fitted models.
- Human lobules and nuclei come from a group probabilistic atlas fitted to a different brain, so their boundaries are approximate. The fastigial nucleus is barely resolved in SUIT and is drawn from a low probability threshold. Brainstem nuclei, the human neuromodulator source nuclei and body structures without meshes are placed approximately (italic labels).
