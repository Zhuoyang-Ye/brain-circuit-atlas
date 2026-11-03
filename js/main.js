/* Cerebellum Atlas: navigation, global search, About dialog and start-up. */
(function () {
  'use strict';
  const CA = window.CA, D = CA.D, h = CA.h;
  const NAV = [
    ['atlas', '3D atlas', 'The cerebellum in a real brain, with evidence-graded connections to brain and body'],
    ['map', 'Functional map', 'Flattened cerebellar cortex: motor, cognitive, social and affective territories'],
    ['circuit', 'Microcircuit', 'The canonical circuit, animated, with a simulated learning experiment'],
    ['molecules', 'Cells & molecules', 'Plasticity at the parallel-fiber synapse, development and disease genes'],
    ['scales', 'Across scales', 'Every entity from genes to disorders and the links between them'],
    ['gaps', 'Evidence & gaps', 'Where the evidence is dense, thin or missing, with live PubMed counts'],
    ['lab', 'Hypothesis lab', 'Chain entities across levels and draft a testable hypothesis'],
    ['library', 'Library', 'Every paper behind the atlas'],
  ];

  function buildNav() {
    const nav = document.getElementById('nav');
    NAV.filter(([id]) => CA.views[id]).forEach(([id, label, desc]) => nav.appendChild(h('a', { href: '#/' + id, 'data-view': id, title: desc }, label)));
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
          h('a', { href: CA.pubmedSearchUrl(`(${q}) AND cerebell*`), target: '_blank', rel: 'noopener' }, 'Search PubMed ↗')));
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
        if (!modal.classList.contains('hidden')) closeModal(); else CA.closePanel();
      }
    });
  }

  /* ---------- About dialog ---------- */
  function closeModal() { const m = document.getElementById('modal'); m.classList.add('hidden'); CA.clear(m); }
  function openAbout() {
    const m = CA.clear(document.getElementById('modal'));
    const ext = (href, text) => h('a', { href, target: '_blank', rel: 'noopener' }, text);
    const card = h('div', { class: 'card', onclick: (ev) => ev.stopPropagation() },
      h('div', { class: 'row', style: { justifyContent: 'space-between' } }, h('h2', { style: { margin: 0 } }, D.meta.title),
        h('button', { class: 'icon-btn', onclick: closeModal, title: 'Close (Esc)' }, '✕')),
      h('p', { class: 'muted' }, D.meta.subtitle),
      h('p', {}, 'The cerebellum holds most of the brain\'s neurons and joins in motor control, cognition, emotion and social behavior. ',
        'This atlas organizes what the literature shows about it, from molecules and cells to circuits, brain-wide loops, behavior and disease. ',
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
        h('li', {}, 'Human lobules and deep nuclei in 3D come from a probabilistic atlas fitted to a different brain, so their boundaries are approximate; the fastigial nucleus is especially uncertain. Structures without a mesh (eyes, inner ear, gut and several brainstem nuclei) are placed approximately and shown in italics.'),
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
        h('li', {}, '3D rendering: ', ext('https://threejs.org/', 'three.js'), ' (MIT license).')),
      h('p', { class: 'tiny muted', style: { marginTop: '12px' } }, `Version ${D.meta.version}, knowledge base built ${D.built}. Press / to search and Esc to close panels.`));
    m.appendChild(card);
    m.classList.remove('hidden');
  }

  /* ---------- start-up ---------- */
  function init() {
    buildNav();
    initSearch();
    document.getElementById('about-btn').addEventListener('click', openAbout);
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
