/* Cells & molecules: the parallel fiber–Purkinje synapse plasticity cascade, cell lineages and disease genes. */
(function () {
  'use strict';
  const CA = window.CA, h = CA.h, s = CA.s;
  let root, svg, meter, outcome, explain, unsub = null, timers = [];
  let zebrin = 'plus', ampaCount = 6;

  CA.register('molecules', { title: 'Cells & molecules', mount, unmount });

  const C = { glu: '#ffa657', ampa: '#79c0ff', mglur: '#b392f0', plc: '#d2a8ff', pkc: '#f778ba', ca: '#58a6ff', cf: '#ff9e64', mli: '#ff7b72', glud: '#3fb9a5', trpc: '#e3b341' };
  // Ca2+ levels (arbitrary units) and plasticity thresholds of the inverse BCM rule (Coesmans et al., 2004)
  const TH_LTP = 0.18, TH_LTD = 0.62;
  const PROTOCOLS = {
    pf: { label: 'Parallel fibers alone', ca: 0.38, refs: ['coesmans2004', 'hansel2001'],
      text: 'Parallel-fiber activity alone raises spine Ca²⁺ only modestly: above the LTP threshold but below the LTD threshold. Result: potentiation; AMPA receptors are inserted.' },
    pfcf: { label: 'Parallel fibers + climbing fiber', ca: 0.86, refs: ['ito1982', 'coesmans2004', 'wang2000', 'aiba1994'],
      text: 'The climbing fiber adds a dendritic Ca²⁺ spike. Together with mGluR1 → PLCβ → PKC signaling, high Ca²⁺ triggers GluA2 phosphorylation and clathrin-mediated AMPA-receptor endocytosis: LTD.' },
    pfcfmli: { label: 'PF + CF + interneuron inhibition', ca: 0.5, refs: ['rowan2018'],
      text: 'Molecular-layer interneurons active at the same time suppress the climbing-fiber Ca²⁺ spike. Ca²⁺ stays below the LTD threshold, so the same pairing now produces potentiation; inhibition can reverse the direction of learning (Rowan et al., 2018).' },
  };

  function mount(node) {
    root = node;
    ampaCount = 6;
    svg = s('svg', { viewBox: '0 0 760 482', width: '100%', style: { display: 'block' } });
    drawSynapse();
    meter = h('div', { class: 'meter' }, h('div', { class: 'fill', style: { height: '8%' } }),
      h('div', { class: 'thr', style: { bottom: (TH_LTP * 100) + '%', borderColor: '#3fb950' }, title: 'LTP threshold' }),
      h('div', { class: 'thr', style: { bottom: (TH_LTD * 100) + '%', borderColor: '#ff7b72' }, title: 'LTD threshold' }));
    outcome = h('div', { class: 'outcome' }, 'Choose a stimulation protocol');
    explain = h('p', { class: 'small' }, '');
    const zb = h('div', { class: 'seg' },
      [['plus', 'Zebrin+ (PLCβ3)'], ['minus', 'Zebrin− (PLCβ4, TRPC3)']].map(([k, l]) => h('button', {
        class: zebrin === k ? 'on' : '', 'data-z': k,
        onclick: () => { zebrin = k; zb.querySelectorAll('button').forEach((b) => b.classList.toggle('on', b.dataset.z === k)); updateZebrin(); },
      }, l)));
    root.appendChild(h('div', { class: 'page' },
      h('div', { class: 'page-head' }, h('div', {},
        h('h2', {}, 'Cells & molecules'),
        h('p', {}, 'At the parallel fiber–Purkinje synapse, calcium decides the sign of plasticity: low calcium potentiates, high calcium (with a climbing-fiber spike) depresses. Click any molecule for its evidence and links upward to circuits, behavior and disease.'))),
      h('div', { class: 'lab-grid' },
        h('div', { class: 'svgwrap', style: { padding: '6px' } }, svg),
        h('div', { class: 'card' },
          h('h3', {}, 'Stimulate the synapse'),
          h('div', { style: { display: 'grid', gap: '6px' } },
            Object.entries(PROTOCOLS).map(([k, p]) => h('button', { class: 'btn', onclick: () => run(k) }, '▶ ' + p.label))),
          h('div', { class: 'row', style: { marginTop: '14px', alignItems: 'flex-start', gap: '14px' } },
            h('div', { style: { textAlign: 'center' } }, meter, h('div', { class: 'tiny muted', style: { marginTop: '4px' } }, 'spine Ca²⁺')),
            h('div', { class: 'grow' },
              h('div', { class: 'tiny', style: { color: '#ff7b72' } }, '— LTD threshold'),
              h('div', { class: 'tiny', style: { color: '#3fb950', marginBottom: '10px' } }, '— LTP threshold'),
              outcome, explain, h('div', { id: 'mol-refs' }))),
          h('h4', {}, 'Purkinje-cell module'), zb,
          h('p', { class: 'small muted', id: 'zeb-text', style: { marginTop: '8px' } }))),
      h('h3', { style: { marginTop: '28px' } }, 'Where the cells come from'),
      h('div', { class: 'svgwrap', style: { padding: '6px' } }, lineage()),
      h('h3', { style: { marginTop: '28px' } }, 'Genes, cells and disease'),
      h('div', { class: 'card' }, diseaseTable())));
    updateZebrin();
    unsub = CA.on('select', paintSel);
    paintSel();
  }
  function unmount() { timers.forEach(clearTimeout); timers = []; if (unsub) unsub(); }

  function el(entity, label, ...kids) {
    const g = s('g', { class: 'mc-el', 'data-entity': entity }, ...kids);
    g.addEventListener('mousemove', (ev) => CA.tip.show(`<b>${CA.esc(label)}</b>`, ev));
    g.addEventListener('mouseleave', () => CA.tip.hide());
    g.addEventListener('click', () => CA.select(entity));
    return g;
  }
  const txt = (x, y, t, o) => s('text', Object.assign({ x, y, fill: '#c9d1d9', 'font-size': 12, 'text-anchor': 'middle', 'pointer-events': 'none' }, o || {}), t);
  const pill = (x, y, w, hgt, color, label) => [s('rect', { x, y, width: w, height: hgt, rx: hgt / 2, fill: color, opacity: 0.9 }), txt(x + w / 2, y + hgt / 2 + 4, label, { fill: '#0d1117', 'font-weight': 600 })];

  function drawSynapse() {
    // presynaptic parallel-fiber bouton
    svg.append(
      el('granule', 'Parallel-fiber bouton (granule-cell axon)',
        s('path', { d: 'M 120 30 C 120 10, 640 10, 640 30 L 640 92 C 640 120, 120 120, 120 92 Z', fill: 'rgba(121,192,255,0.12)', stroke: '#79c0ff', 'stroke-width': 1.5 }),
        txt(380, 52, 'Parallel-fiber terminal (granule cell)', { fill: '#79c0ff' })),
      s('g', { id: 'vesicles' }, ...[180, 260, 340, 420, 500, 580].map((x) => s('circle', { cx: x, cy: 82, r: 9, fill: 'none', stroke: C.glu, 'stroke-width': 1.5 }))),
      // cleft + postsynaptic spine
      s('path', { d: 'M 90 160 L 670 160 L 670 450 L 90 450 Z', fill: 'rgba(247,120,186,0.07)', stroke: '#f778ba', 'stroke-width': 1.5 }),
      txt(600, 440, 'Purkinje-cell spine', { fill: '#f778ba', 'text-anchor': 'end' }),
      s('g', { id: 'glu' }),
      el('glud2', 'GluD2–Cbln1: trans-synaptic organizer',
        s('rect', { x: 640, y: 104, width: 16, height: 56, rx: 5, fill: C.glud }), txt(662, 134, 'GluD2–Cbln1', { fill: C.glud, 'font-size': 11, 'text-anchor': 'start' })),
      s('g', { id: 'ampa' }),
      el('mglur1', 'mGluR1 (metabotropic glutamate receptor)', ...pill(110, 166, 90, 26, C.mglur, 'mGluR1')),
      el('plcb', 'PLCβ (β3 in zebrin+, β4 in zebrin− cells)', ...pill(118, 222, 76, 24, C.plc, 'PLCβ')),
      el('pkc', 'Protein kinase C', ...pill(118, 280, 76, 24, C.pkc, 'PKC')),
      el('trpc3', 'TRPC3 cation channel (high in zebrin− modules)', s('g', { id: 'trpc' }, ...pill(224, 166, 74, 26, C.trpc, 'TRPC3'))),
      el('ampar', 'AMPA receptors (GluA2): fast transmission; endocytosed in LTD',
        txt(450, 210, 'AMPA receptors (GluA2)', { fill: C.ampa, 'font-size': 11 })),
      s('path', { d: 'M 156 192 L 156 222 M 156 246 L 156 280', stroke: '#8b949e', 'stroke-width': 1.5, 'marker-end': 'url(#ah)' }),
      s('path', { id: 'pkcarrow', d: 'M 196 292 C 300 300, 360 260, 380 196', stroke: C.pkc, 'stroke-width': 1.5, fill: 'none', 'stroke-dasharray': '4 3', 'marker-end': 'url(#ah)' }),
      txt(300, 316, 'phosphorylates GluA2 → internalization', { fill: C.pkc, 'font-size': 11 }),
      el('ltd', 'LTD: clathrin-mediated AMPA-receptor endocytosis',
        s('circle', { id: 'endo', cx: 470, cy: 330, r: 26, fill: 'none', stroke: '#8b949e', 'stroke-width': 1.5, 'stroke-dasharray': '3 3' }),
        txt(470, 374, 'endocytosis (LTD)', { fill: '#8b949e', 'font-size': 11 })),
      el('ltp', 'LTP: AMPA-receptor insertion',
        s('rect', { x: 560, y: 300, width: 70, height: 40, rx: 8, fill: 'none', stroke: '#8b949e', 'stroke-width': 1.5, 'stroke-dasharray': '3 3' }),
        txt(595, 358, 'insertion (LTP)', { fill: '#8b949e', 'font-size': 11 })),
      s('rect', { id: 'cafill', x: 92, y: 448, width: 576, height: 0, fill: C.ca, opacity: 0.22 }),
      txt(200, 425, 'Ca²⁺', { fill: C.ca, 'font-size': 13, 'font-weight': 600 }),
      el('cf-pathway', 'Climbing-fiber input → dendritic Ca²⁺ spike',
        s('path', { id: 'cfpath', d: 'M 740 450 C 720 380, 700 300, 672 250', stroke: C.cf, 'stroke-width': 3, fill: 'none' }), txt(712, 470, 'climbing fiber', { fill: C.cf, 'font-size': 11 })),
      el('mli', 'Molecular-layer interneuron (GABAergic)',
        s('path', { id: 'mlipath', d: 'M 20 400 C 50 380, 70 360, 92 350', stroke: C.mli, 'stroke-width': 3, fill: 'none' }), txt(40, 425, 'interneuron', { fill: C.mli, 'font-size': 11 })),
      s('defs', {}, s('marker', { id: 'ah', viewBox: '0 0 10 10', refX: 8, refY: 5, markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse' }, s('path', { d: 'M0 0 L10 5 L0 10 z', fill: '#8b949e' }))));
    drawAmpa();
  }

  function drawAmpa() {
    const g = svg.querySelector('#ampa');
    CA.clear(g);
    for (let i = 0; i < ampaCount; i++) {
      const x = 330 + i * 32;
      g.appendChild(s('g', { class: 'mc-el', 'data-entity': 'ampar' },
        s('rect', { x, y: 150, width: 20, height: 34, rx: 6, fill: C.ampa })));
    }
    g.querySelectorAll('.mc-el').forEach((n) => n.addEventListener('click', () => CA.select('ampar')));
  }

  function setCa(level) {
    meter.querySelector('.fill').style.height = Math.round(level * 100) + '%';
    const r = svg.querySelector('#cafill');
    r.setAttribute('height', level * 250); r.setAttribute('y', 448 - level * 250);
  }

  function run(key) {
    timers.forEach(clearTimeout); timers = [];
    const p = PROTOCOLS[key];
    outcome.textContent = 'Stimulating…'; outcome.style.borderLeftColor = '#6e7681';
    explain.textContent = '';
    setCa(0.05);
    // glutamate release
    const glu = svg.querySelector('#glu');
    CA.clear(glu);
    for (let i = 0; i < 18; i++) glu.appendChild(s('circle', { cx: 180 + Math.random() * 420, cy: 100, r: 3, fill: C.glu }));
    timers.push(setTimeout(() => glu.querySelectorAll('circle').forEach((c) => { c.setAttribute('cy', 140 + Math.random() * 14); c.style.transition = 'cy .5s'; }), 30));
    const cfOn = key !== 'pf';
    svg.querySelector('#cfpath').setAttribute('stroke-width', cfOn ? 6 : 3);
    svg.querySelector('#mlipath').setAttribute('stroke-width', key === 'pfcfmli' ? 6 : 3);
    // Ca2+ rises; with zebrin− cells the mGluR1–TRPC3 contribution is larger
    const level = Math.min(0.97, p.ca + (zebrin === 'minus' ? 0.04 : 0));
    timers.push(setTimeout(() => setCa(level), 450));
    timers.push(setTimeout(() => {
      CA.clear(glu);
      svg.querySelector('#cfpath').setAttribute('stroke-width', 3);
      svg.querySelector('#mlipath').setAttribute('stroke-width', 3);
      let res;
      if (level >= TH_LTD) { res = 'LTD: AMPA receptors removed'; ampaCount = Math.max(2, ampaCount - 2); outcome.style.borderLeftColor = '#ff7b72'; }
      else if (level >= TH_LTP) { res = 'LTP: AMPA receptors added'; ampaCount = Math.min(10, ampaCount + 2); outcome.style.borderLeftColor = '#3fb950'; }
      else { res = 'No change'; }
      drawAmpa();
      svg.querySelector('#endo').setAttribute('stroke', level >= TH_LTD ? '#ff7b72' : '#8b949e');
      outcome.textContent = res;
      explain.textContent = p.text;
      const refs = document.getElementById('mol-refs');
      if (refs) CA.clear(refs).append(...CA.citeChips(p.refs));
    }, 1300));
  }

  function updateZebrin() {
    const t = document.getElementById('zeb-text');
    svg.querySelector('#trpc').setAttribute('opacity', zebrin === 'minus' ? 1 : 0.35);
    if (!t) return;
    CA.clear(t).append(zebrin === 'plus'
      ? 'Zebrin+ Purkinje cells express PLCβ3, fire simple spikes at lower rates and are proposed to learn mainly by depression ("downbound"). '
      : 'Zebrin− Purkinje cells express PLCβ4 and stronger TRPC3 signaling, fire at higher rates and are proposed to learn mainly by potentiation ("upbound"). ',
    ...CA.citeChips(['sarna2006', 'zhou2014', 'dezeeuw2021']));
  }

  function paintSel() {
    root.querySelectorAll('.mc-el').forEach((g) => g.classList.toggle('sel', g.dataset.entity === CA.selected));
  }

  /* ------------------------------------------------------------------ lineage */
  function lineage() {
    const g = s('svg', { viewBox: '0 0 960 250', width: '100%', style: { display: 'block' } });
    const box = (x, y, w, label, entity, color, sub) => {
      const node = el(entity, (CA.ent[entity] || {}).name || label,
        s('rect', { x, y, width: w, height: 40, rx: 8, fill: color + '26', stroke: color, 'stroke-width': 1.5 }),
        txt(x + w / 2, y + (sub ? 17 : 25), label, { fill: '#e6edf3', 'font-weight': 600 }),
        sub ? txt(x + w / 2, y + 32, sub, { fill: '#8b949e', 'font-size': 10.5 }) : null);
      g.appendChild(node);
    };
    const arrow = (x1, y1, x2, y2, color, dash) => g.appendChild(s('path', { d: `M ${x1} ${y1} C ${(x1 + x2) / 2} ${y1}, ${(x1 + x2) / 2} ${y2}, ${x2} ${y2}`, stroke: color || '#8b949e', 'stroke-width': 1.5, fill: 'none', 'stroke-dasharray': dash || '', 'marker-end': 'url(#lah)' }));
    g.appendChild(s('defs', {}, s('marker', { id: 'lah', viewBox: '0 0 10 10', refX: 8, refY: 5, markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse' }, s('path', { d: 'M0 0 L10 5 L0 10 z', fill: '#8b949e' }))));
    box(20, 40, 190, 'Rhombic lip', 'rhombic-lip', '#f778ba', 'Atoh1+ (expanded in humans)');
    box(20, 160, 190, 'Ventricular zone', 'rhombic-lip', '#f778ba', 'Ptf1a+');
    box(260, 10, 120, 'Atoh1', 'atoh1', '#b392f0');
    box(260, 190, 120, 'Ptf1a', 'ptf1a', '#b392f0');
    box(450, 10, 170, 'Granule cells', 'granule', '#79c0ff', 'via external granular layer');
    box(450, 62, 170, 'Unipolar brush cells', 'ubc', '#56d4dd');
    box(450, 140, 170, 'Purkinje cells', 'purkinje', '#f778ba');
    box(450, 192, 170, 'Interneurons', 'mli', '#d2a8ff', 'MLIs, Golgi cells');
    box(700, 10, 160, 'Sonic hedgehog', 'shh', '#b392f0', 'Purkinje → GCP mitogen');
    box(700, 90, 160, 'SHH medulloblastoma', 'c-medullo', '#ff7b72');
    box(700, 170, 160, 'Dandy–Walker', 'c-dandy', '#ff7b72', 'vermis hypoplasia');
    arrow(210, 60, 260, 30); arrow(380, 30, 450, 30); arrow(380, 30, 450, 82);
    arrow(210, 180, 260, 210); arrow(380, 210, 450, 160); arrow(380, 210, 450, 212);
    arrow(620, 160, 700, 30, '#b392f0', '4 3'); arrow(780, 50, 780, 90, '#ff7b72', '4 3'); arrow(210, 70, 700, 190, '#ff7b72', '4 3');
    g.appendChild(txt(860, 242, 'Click a box for evidence', { fill: '#6e7681', 'font-size': 11, 'text-anchor': 'end' }));
    return g;
  }

  function diseaseTable() {
    const rows = [
      ['cacna1a', 'purkinje', 'Small polyglutamine expansion in the P/Q calcium channel', 'c-sca', 'zhuchenko1997'],
      ['atxn1', 'purkinje', 'Expanded CAG repeat; longer repeats, earlier onset', 'c-sca', 'orr1993'],
      ['tsc1', 'purkinje', 'Loss lowers Purkinje excitability; rapamycin-preventable autistic-like behavior', 'c-asd', 'tsai2012'],
      ['shank2', 'purkinje', 'Loss of LTP and intrinsic plasticity; irregular simple spikes', 'c-asd', 'peter2016'],
      ['fmr1', 'purkinje', 'Enhanced LTD, elongated spines, impaired eyeblink conditioning', 'c-fxs', 'koekkoek2005'],
      ['shh', 'granule', 'Over-active Sonic hedgehog pathway in granule precursors', 'c-medullo', 'wechslerreya1999'],
    ];
    return h('table', { class: 'data' },
      h('tr', {}, h('th', {}, 'Gene'), h('th', {}, 'Cell'), h('th', {}, 'Mechanism'), h('th', {}, 'Disorder'), h('th', {}, 'Evidence')),
      rows.map(([g, c, m, d, ref]) => h('tr', {},
        h('td', {}, CA.entChip(g)), h('td', {}, CA.entChip(c)), h('td', { class: 'small' }, m), h('td', {}, CA.entChip(d)), h('td', {}, CA.citeChips([ref])))));
  }
})();
