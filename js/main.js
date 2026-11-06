/* Brain Circuit Atlas: navigation, global search, About dialog and start-up. */
(function () {
  'use strict';
  const CA = window.CA, D = CA.D, h = CA.h;
  const NAV = [
    ['atlas', '3D atlas', 'Each region in a real brain, with evidence-graded connections to brain and body'],
    ['map', 'Functional map', 'Where functions and activity sit: the flattened cerebellar cortex, or the fly central brain’s functional and structural connectivity'],
    ['circuit', 'Microcircuit', 'The canonical cerebellar circuit or the fly’s mushroom body, animated, with a simulated learning experiment'],
    ['molecules', 'Cells & molecules', 'Synaptic plasticity, neuromodulators, development and genes: the cerebellar parallel-fiber synapse or the fly’s Kenyon cell synapse'],
    ['scales', 'Across scales', 'Every entity from genes to disorders and the links between them'],
    ['gaps', 'Evidence & gaps', 'Where the evidence is dense, thin or missing, with live PubMed counts'],
    ['lab', 'Hypothesis lab', 'Chain entities across levels and draft a testable hypothesis'],
    ['library', 'Library', 'Every paper behind the atlas'],
  ];

  let navOpen = () => false, setNavOpen = () => {};

  function buildNav() {
    const nav = document.getElementById('nav');
    NAV.filter(([id]) => CA.views[id]).forEach(([id, label, desc]) => nav.appendChild(h('a', { href: '#/' + id, 'data-view': id, title: desc }, label)));
    // when the tabs do not fit, fade the right edge to show that the bar scrolls
    const more = () => nav.classList.toggle('more', nav.scrollLeft + nav.clientWidth < nav.scrollWidth - 1);
    nav.addEventListener('scroll', more);
    window.addEventListener('resize', more);
    CA.on('view-mounted', more);

    // phones (css: max-width 860px): the tabs fold into a drop-down list behind a menu button named after the current view
    const toggle = document.getElementById('nav-toggle'), current = document.getElementById('nav-current');
    navOpen = () => nav.classList.contains('open');
    setNavOpen = (open) => {
      nav.classList.toggle('open', open);
      document.body.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close the list of views' : 'Open the list of views');
    };
    toggle.addEventListener('click', () => setNavOpen(!navOpen()));
    nav.addEventListener('click', (ev) => { if (ev.target.closest('a')) setNavOpen(false); });
    document.getElementById('nav-scrim').addEventListener('click', () => setNavOpen(false));
    if (window.matchMedia) {
      const phone = matchMedia('(max-width: 860px)');
      const shut = () => setNavOpen(false);
      if (phone.addEventListener) phone.addEventListener('change', shut); else phone.addListener(shut);
    }
    CA.on('view-mounted', (v) => {
      const label = (NAV.find(([id]) => id === v) || [])[1] || '';
      current.textContent = label;
      toggle.title = 'Views' + (label ? ': ' + label : '');
    });
  }

  /* ---------- global search ---------- */
  function initSearch() {
    const input = document.getElementById('search'), box = document.getElementById('search-results');
    let results = [], active = -1;
    const close = () => { box.classList.add('hidden'); active = -1; };
    const choose = (r) => {
      close(); input.value = ''; input.blur();
      if (r.type === 'entity') CA.select(r.id); else CA.showPaper(r.id);
    };
    const draw = () => {
      CA.clear(box);
      const q = input.value.trim();
      if (!q) { close(); return; }
      box.classList.remove('hidden');
      if (!results.length) {
        box.appendChild(h('div', { class: 'sr muted' }, 'Nothing in the atlas. ',
          h('a', { href: CA.pubmedSearchUrl(`(${q}) AND ${CA.region.query}`), target: '_blank', rel: 'noopener' }, 'Search PubMed ↗')));
        return;
      }
      results.forEach((r, i) => box.appendChild(h('button', {
        class: 'sr' + (i === active ? ' on' : ''),
        onmousedown: (ev) => { ev.preventDefault(); choose(r); },
      },
      h('div', {}, r.type === 'entity'
        ? h('span', { class: 'dot', style: { background: CA.entColor(r.id), marginRight: '7px' } })
        : h('span', { class: 'ev', style: { marginRight: '7px' } }, 'paper'), r.label),
      h('div', { class: 'muted' }, r.sub))));
    };
    input.addEventListener('input', () => { results = CA.search(input.value, 12); active = results.length ? 0 : -1; draw(); });
    input.addEventListener('keydown', (ev) => {
      if (ev.key === 'ArrowDown') { active = Math.min(results.length - 1, active + 1); draw(); ev.preventDefault(); }
      else if (ev.key === 'ArrowUp') { active = Math.max(0, active - 1); draw(); ev.preventDefault(); }
      else if (ev.key === 'Enter' && results[active]) choose(results[active]);
      else if (ev.key === 'Escape') { close(); input.blur(); }
    });
    input.addEventListener('blur', () => setTimeout(close, 150));
    input.addEventListener('focus', () => { if (input.value.trim()) draw(); });
    document.addEventListener('keydown', (ev) => {
      const typing = /^(input|textarea|select)$/i.test(document.activeElement.tagName);
      if (ev.key === '/' && !typing) { ev.preventDefault(); input.focus(); }
      if (ev.key === 'Escape' && !typing) {
        const modal = document.getElementById('modal');
        if (navOpen()) { setNavOpen(false); document.getElementById('nav-toggle').focus(); }
        else if (!modal.classList.contains('hidden')) closeModal(); else CA.closePanel();
      }
    });
  }

  /* ---------- About dialog ---------- */
  function closeModal() { const m = document.getElementById('modal'); m.classList.add('hidden'); CA.clear(m); }
  function openAbout() {
    const m = CA.clear(document.getElementById('modal'));
    const ext = (href, text) => h('a', { href, target: '_blank', rel: 'noopener' }, text);
    const macaque = D.atlas3d.species.includes('macaque');   // switched off in knowledge.json atlas3d.species → no macaque credit
    const later = D.regions.slice(1).map((r) => 'the ' + r.label.toLowerCase());
    const followed = later.length < 2 ? later.join('') : later.slice(0, -1).join(', ') + ' and ' + later[later.length - 1];
    const card = h('div', { class: 'card', onclick: (ev) => ev.stopPropagation() },
      h('div', { class: 'row', style: { justifyContent: 'space-between' } }, h('h2', { style: { margin: 0 } }, D.meta.title),
        h('button', { class: 'icon-btn', onclick: closeModal, title: 'Close (Esc)' }, '✕')),
      h('p', { class: 'muted' }, D.meta.subtitle),
      h('p', {}, 'This atlas organizes what the literature shows about brain regions, from molecules and cells to circuits, brain-wide loops, behavior and disease. ',
        'It began with the cerebellum, which has several times as many neurons as the cerebral cortex and joins in motor control, cognition, emotion and social behavior',
        later.length ? `; ${followed} followed. ` : '. ',
        'Pick a region in the Region menu, at the top left of each page (in the 3D atlas, at the top of the left panel). ',
        'Every connection is graded by its evidence and linked to the papers behind it, so you can see what is established, what is debated, and where the gaps are.'),
      h('h4', {}, 'Views'),
      h('div', {}, NAV.filter(([id]) => CA.views[id]).map(([id, label, desc]) => h('div', { class: 'small', style: { margin: '3px 0' } },
        h('a', { href: '#/' + id, onclick: closeModal }, label), h('span', { class: 'muted' }, ' · ' + desc)))),
      h('h4', {}, 'Reading the evidence'),
      h('table', { class: 'data' }, D.statuses.map((st) => h('tr', {}, h('td', { style: { width: '120px' } }, CA.statusBadge(st.id)), h('td', { class: 'small' }, st.desc)))),
      h('p', { class: 'small', style: { marginTop: '8px' } }, 'Each paper is also tagged by the kind of evidence it gives: ',
        D.evidence.map((e, i) => [i ? ', ' : '', h('span', { title: e.desc || '' }, e.label)]), '.'),
      h('h4', {}, 'Sources and caveats'),
      h('ul', { class: 'small', style: { paddingLeft: '18px' } },
        h('li', {}, `${D.papers.length} curated publications. Titles, authors, journals and identifiers come from PubMed through the NCBI E-utilities; the evidence statuses, findings and map scores were written for this atlas.`),
        h('li', {}, D.meta.disclaimer),
        h('li', {}, 'Each one-sentence finding was checked against the paper\'s PubMed abstract. Albus (1971) is not in PubMed, and seven papers without a PubMed abstract (Scoville & Milner, 1957; Messenger, 1967; O\'Keefe & Dostrovsky, 1971; Hoffer et al., 1973; Weiskrantz et al., 1974; Schulman et al., 1981; Morris et al., 1982) are summarized from their titles, as their findings state.'),
        h('li', {}, 'Human lobules and deep nuclei in 3D come from a probabilistic atlas fitted to a different brain, so their boundaries are approximate; the fastigial nucleus is especially uncertain. Structures without a mesh (eyes, inner ear, gut, several brainstem nuclei and, in the human brain, the substantia nigra, the neuromodulator source nuclei, premotor areas, S1 and basal forebrain) are placed approximately and shown in italics. Human M1 is drawn as the whole precentral gyrus, which also holds part of premotor cortex, and human prefrontal areas as whole gyri (dorsolateral PFC as the middle frontal gyrus, ventromedial PFC as the gyrus rectus, the subgenual cingulate as the subcallosal gyrus). The human atlas does not separate the hippocampal fields (dentate gyrus, CA1–CA3, subiculum), so they are shown in the hippocampus, whose head stands for the anterior (ventral) and its body and tail for the posterior (dorsal) part; the entorhinal cortex is drawn as the anterior parahippocampal gyrus. In the mouse, the dorsal and ventral hippocampus are placed approximately. The human atlas does not separate the amygdala\'s nuclei either, so they are shown in the amygdala, and the medial geniculate nucleus is shown in the thalamus. Nor does it mark visual areas: V1 is drawn as the occipital pole, cuneus and lingual gyrus, V4 as the occipital part of the fusiform gyrus, the fusiform face area as its temporal part and inferotemporal cortex as the inferior temporal gyrus; MT is placed approximately, and the lateral geniculate nucleus is shown in the thalamus. The insula is drawn as its short (anterior) and long (posterior) insular gyri, and the taste cortex and von Economo neurons are shown in the anterior insula. The cortical amygdala is shown in the amygdala, and olfactory sensory neurons are placed approximately in front of the olfactory bulb.', macaque ? ' Macaque structures are computed from atlas labels on a population template, so small nuclei are approximate; the macaque substantia nigra and hippocampus are labeled as wholes, so the reticular part of the nigra, the hippocampal fields and the anterior and posterior hippocampus are placed approximately or shown within them. The macaque atlas has no label for the amygdala\'s intercalated cells, so they are placed approximately, and the macaque taste cortex is shown in the anterior insula. The macaque template does not include the olfactory bulb, so it is placed approximately under the orbital surface.' : ''),
        h('li', {}, 'The octopus brain in 3D is a schematic drawn for this site, not a scan or an atlas volume: its lobe shapes, sizes and positions are approximate and only for orientation, so every octopus label carries ≈. Octopus findings come from several species, mainly Octopus vulgaris and O. bimaculoides.'),
        h('li', {}, 'The fruit fly brain in 3D shows neuropil regions from the Janelia male CNS connectome, simplified for the web; cell types are shown in the neuropils they belong to (Kenyon cells and output neurons in the mushroom body, for example), and photoreceptors and olfactory and gustatory receptor neurons, which lie outside the brain, are placed approximately. Fly findings come from Drosophila melanogaster, and the connectomes cited come from different flies, female and male, so structural and functional connectivity are not from the same brain. The fly’s Functional map recomputes resting-state functional connectivity (20 flies) and hemibrain structural connectivity for 37 central-brain regions from the data of Turner, Mann & Clandinin (2021); the two come from different animals. Its odour-conditioning and synapse models, like the eyeblink model, are toy models for intuition.'),
        h('li', {}, 'Coverage is a curated core, not a systematic review. Live PubMed counts in Evidence & gaps show how much literature exists beyond it.')),
      h('h4', {}, 'Credits'),
      h('ul', { class: 'small', style: { paddingLeft: '18px' } },
        h('li', {}, 'Literature metadata: ', ext('https://pubmed.ncbi.nlm.nih.gov/', 'PubMed'), ', U.S. National Library of Medicine, via the NCBI E-utilities.'),
        h('li', {}, 'Mouse anatomy: Allen Mouse Brain Common Coordinate Framework v3 (Wang et al., 2020, Cell; ', ext('https://doi.org/10.1016/j.cell.2020.04.007', 'doi:10.1016/j.cell.2020.04.007'), '), © Allen Institute for Brain Science.'),
        h('li', {}, 'Human anatomy: Allen Human Reference Atlas (Ding et al., 2016, J Comp Neurol; ', ext('https://doi.org/10.1002/cne.24080', 'doi:10.1002/cne.24080'), '), © Allen Institute for Brain Science, obtained through the ',
          ext('https://brainglobe.info/', 'BrainGlobe'), ' Atlas API.'),
        h('li', {}, 'Human cerebellar lobules and nuclei: SUIT probabilistic atlases (Diedrichsen et al., 2009, NeuroImage; ', ext('https://doi.org/10.1016/j.neuroimage.2009.01.045', 'doi:10.1016/j.neuroimage.2009.01.045'),
          '; Diedrichsen et al., 2011, NeuroImage; ', ext('https://doi.org/10.1016/j.neuroimage.2010.10.035', 'doi:10.1016/j.neuroimage.2010.10.035'), '), from the ',
          ext('https://github.com/DiedrichsenLab/cerebellar_atlases', 'cerebellar_atlases'), ' collection, CC BY.'),
        macaque && h('li', {}, 'Macaque anatomy: the ', ext('https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/nonhuman/macaque_tempatl/template_nmtv2.html', 'NIMH Macaque Template v2'),
          ' (Seidlitz et al., 2018, NeuroImage; ', ext('https://doi.org/10.1016/j.neuroimage.2017.04.063', 'doi:10.1016/j.neuroimage.2017.04.063'),
          '; Jung et al., 2021, NeuroImage; ', ext('https://doi.org/10.1016/j.neuroimage.2021.117997', 'doi:10.1016/j.neuroimage.2021.117997'),
          ') with its CHARM cortical atlas (Jung et al., 2021) and SARM subcortical atlas (Hartig et al., 2021, NeuroImage; ',
          ext('https://doi.org/10.1016/j.neuroimage.2021.117996', 'doi:10.1016/j.neuroimage.2021.117996'), '), distributed with AFNI. Surfaces computed from the atlas labels.'),
        h('li', {}, 'Octopus anatomy: a schematic drawn for this site; lobes named as in octopus brain atlases (Jung et al., 2018, ', ext('https://pubmed.ncbi.nlm.nih.gov/30181688/', 'PMID 30181688'),
          '; Jacobs et al., 2022, ', ext('https://pubmed.ncbi.nlm.nih.gov/35256541/', 'PMID 35256541'), ').'),
        h('li', {}, 'Fruit fly anatomy: neuropil meshes from the Janelia FlyEM ', ext('https://male-cns.janelia.org/', 'male CNS connectome'), ' (Berg et al., 2026, Cell; ',
          ext('https://doi.org/10.1016/j.cell.2026.08.015', 'doi:10.1016/j.cell.2026.08.015'), '), licensed CC BY; simplified for this site.'),
        h('li', {}, 'Fly functional and structural connectivity: recomputed from the data of Turner, Mann & Clandinin (2021, Curr Biol; ', ext('https://doi.org/10.1016/j.cub.2021.03.004', 'doi:10.1016/j.cub.2021.03.004'),
          '), ', ext('https://doi.org/10.6084/m9.figshare.13349282', 'figshare'), ', MIT license; structural measures from the hemibrain connectome (Scheffer et al., 2020, eLife; ',
          ext('https://doi.org/10.7554/eLife.57443', 'doi:10.7554/eLife.57443'), ').'),
        h('li', {}, '3D rendering: ', ext('https://threejs.org/', 'three.js'), ' (MIT license).')),
      h('p', { class: 'tiny muted', style: { marginTop: '12px' } }, `Version ${D.meta.version}, knowledge base built ${D.built}. Press / to search and Esc to close panels. The sun/moon button switches between light and dark mode.`),
      CA.hasBackend && h('div', { style: { marginTop: '12px', borderTop: '1px solid var(--border)', paddingTop: '10px' } },
        h('button', { class: 'btn small', onclick: (e) => { e.preventDefault(); CA.openCloudModal(); } }, 'Cloudflare R2 & Website Sync Settings')));
    m.appendChild(card);
    m.classList.remove('hidden');
  }

  /* ---------- start-up ---------- */
  function init() {
    buildNav();
    initSearch();
    document.getElementById('about-btn').addEventListener('click', openAbout);
    const themeBtn = document.getElementById('theme-btn');
    const themeLabel = () => {
      const t = CA.theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode';
      themeBtn.title = t; themeBtn.setAttribute('aria-label', t);
    };
    themeBtn.addEventListener('click', () => CA.setTheme(CA.theme === 'light' ? 'dark' : 'light'));
    CA.on('theme', themeLabel); themeLabel();
    // names on the 3D model or in a legend at the side: shown with the 3D atlas only
    const labelsSeg = document.getElementById('labels-seg');
    const syncLabels = () => labelsSeg.querySelectorAll('button').forEach((b) => {
      const on = b.dataset.mode === CA.labelMode;
      b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on));
    });
    labelsSeg.querySelectorAll('button').forEach((b) => b.addEventListener('click', () => CA.setLabelMode(b.dataset.mode)));
    CA.on('labels', syncLabels); syncLabels();
    CA.on('view-mounted', (v) => { labelsSeg.hidden = v !== 'atlas'; });
    document.getElementById('modal').addEventListener('click', closeModal);
    document.getElementById('panel-back').addEventListener('click', CA.panelBack);
    document.getElementById('panel-close').addEventListener('click', CA.closePanel);
    const bar = document.getElementById('errbar');
    bar.title = 'Click to dismiss';
    bar.addEventListener('click', () => { bar.style.display = 'none'; });
    window.addEventListener('hashchange', CA.route);
    CA.route();
  }
  window.addEventListener('error', (ev) => CA.reportError(ev.error || ev.message));
  window.addEventListener('unhandledrejection', (ev) => CA.reportError(ev.reason));
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
