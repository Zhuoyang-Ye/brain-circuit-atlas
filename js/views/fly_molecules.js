/* Fruit fly Cells & molecules: the Kenyon cell output synapse, where the order of odour and dopamine sets the sign of
   plasticity; the circuit's neuromodulators; where its cells come from; and genes that tie the fly to learning, sleep
   and models of human brain disease. */
(function () {
  'use strict';
  const CA = window.CA, h = CA.h, s = CA.s;
  const CFG = ((CA.D.regionViews || {}).fly || {}).molecules || {};
  let root, svg, meter, outcome, explain, refsEl, unsub = null, timers = [];
  let geno = 'wt', strength = 6;

  CA.registerVariant('molecules', 'fly', { mount, unmount });

  const C = CA.palette({ ca: '#58a6ff', cam: '#79c0ff', rut: '#e3b341', camp: '#ffa657', pka: '#f778ba', dnc: '#8b949e', dopr1: '#ff7b72', dopr2: '#d2a8ff',
    da: '#f85149', ves: '#3fb950', kc: '#e3b341', mbon: '#d2a8ff' });
  const TH = 0.62;   // cAMP level (arbitrary units) above which the toy synapse depresses
  const GENO = {
    wt: { label: 'Wild type' },
    rut: { label: 'rutabaga' },
    dnc: { label: 'dunce' },
    dopr1: { label: 'DopR1 mutant' },
  };
  const PROTOCOLS = {
    odour: { label: 'Odour alone', refs: ['tomchik2009', 'hige2015'] },
    da: { label: 'Dopamine alone', refs: ['tomchik2009', 'hige2015'] },
    fwd: { label: 'Odour, then dopamine', refs: ['tomchik2009', 'hige2015', 'kimyc2007', 'handler2019'] },
    bwd: { label: 'Dopamine, then odour', refs: ['handler2019', 'aso2016'] },
  };
  // what the toy synapse does: cAMP level, and the change in release (vesicles: −2 depression, +2 potentiation)
  function outcomeOf(p, g) {
    const base = g === 'dnc' ? 0.7 : 0.08;   // without the phosphodiesterase, cAMP stays high
    let camp = base, change = 0, why;
    if (p === 'odour') { camp = base + 0.12; why = 'Odour-evoked spikes let Ca²⁺ into the Kenyon cell terminal, and Ca²⁺/calmodulin primes the rutabaga cyclase, but without dopamine cAMP rises only a little.'; }
    if (p === 'da') { camp = base + (g === 'dopr1' ? 0.04 : 0.22); why = 'Dopamine alone raises cAMP in the lobes modestly (Tomchik & Davis, 2009); without coincident Kenyon cell activity, nothing is stored.'; }
    if (p === 'fwd') {
      if (g === 'rut') { camp = base + 0.2; why = 'Without the rutabaga cyclase, depolarization followed by dopamine no longer raises cAMP synergistically (Tomchik & Davis, 2009); the synapse is not depressed.'; }
      else if (g === 'dopr1') { camp = base + 0.1; change = 1; why = 'Without DopR1, odour-then-dopamine pairing no longer depresses the synapse and instead potentiates it weakly (Handler et al., 2019); dDA1 mutants barely learn with shock (Kim et al., 2007).'; }
      else { camp = base + 0.78; why = 'Dopamine that follows Kenyon cell activity raises cAMP synergistically through the rutabaga cyclase, a coincidence detector (Tomchik & Davis, 2009); PKA then depresses the synapse onto the output neuron, odour-specifically and only in this compartment (Hige et al., 2015). DopR1 is needed for this depression (Handler et al., 2019).'; }
    }
    if (p === 'bwd') { camp = base + 0.16; change = 2; why = 'Dopamine before the odour acts through DopR2, coupled to a different second messenger, and potentiates the synapse instead, which can undo a memory written by forward pairing (Handler et al., 2019); single dopamine neuron types follow such timing rules differently (Aso & Rubin, 2016).'; }
    camp = Math.min(0.97, camp);
    if (g === 'dnc') {
      change = -2;
      why = 'Without the cAMP phosphodiesterase that dunce appears to encode (Byers et al., 1981), cAMP stays high. In this toy every stimulus then crosses the threshold, so the synapse cannot tell a pairing from a single stimulus; dunce flies fail to learn (Dudai et al., 1976) or forget within 30 minutes (Tully & Quinn, 1985).';
    } else if (camp >= TH) change = -2;
    return { camp, change, why, refs: g === 'dnc' ? ['byers1981', 'dudai1976', 'tully1985'] : g === 'rut' && p === 'fwd' ? ['tomchik2009', 'livingstone1984', 'zars2000'] : PROTOCOLS[p].refs };
  }

  function mount(node) {
    root = node;
    strength = 6;
    svg = s('svg', { viewBox: '0 0 760 470', width: '100%', style: { display: 'block' }, role: 'img', 'aria-label': 'Kenyon cell output synapse with its plasticity cascade' });
    drawSynapse();
    meter = h('div', { class: 'meter' }, h('div', { class: 'fill', style: { height: '8%' } }),
      h('div', { class: 'thr', style: { bottom: (TH * 100) + '%', borderColor: CA.tc('#ff7b72') }, title: 'depression threshold' }));
    outcome = h('div', { class: 'outcome' }, 'Choose a protocol');
    explain = h('p', { class: 'small' }, '');
    refsEl = h('div', {});
    const gseg = h('div', { class: 'seg', role: 'group', 'aria-label': 'Genotype' }, Object.entries(GENO).map(([k, g]) => h('button', {
      class: geno === k ? 'on' : '', 'data-g': k, 'aria-pressed': String(geno === k),
      onclick: () => { geno = k; strength = 6; drawVesicles(); gseg.querySelectorAll('button').forEach((b) => { const on = b.dataset.g === k; b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on)); }); paintGeno(); },
    }, g.label)));
    root.appendChild(h('div', { class: 'page' },
      h('div', { class: 'page-head' }, h('div', {},
        h('h2', {}, 'Cells & molecules'),
        h('p', {}, 'At the Kenyon cell’s output synapse, the order of odour and dopamine decides the sign of plasticity: dopamine that follows Kenyon cell activity raises cAMP through the rutabaga cyclase and depresses the synapse; dopamine that comes first potentiates it through DopR2. Below, the circuit’s neuromodulators and neuropeptides, where its cells come from, and genes that tie the fly to learning, sleep and models of human brain disease. Click any molecule for its evidence.'))),
      h('div', { class: 'lab-grid' },
        h('div', { class: 'svgwrap', style: { padding: '6px' } }, svg),
        h('div', { class: 'card' },
          h('h3', {}, 'Stimulate the synapse'),
          h('div', { class: 'row small', style: { marginBottom: '8px', flexWrap: 'wrap' } }, 'Fly', gseg),
          h('div', { style: { display: 'grid', gap: '6px' } }, Object.entries(PROTOCOLS).map(([k, p]) => h('button', { class: 'btn', onclick: () => run(k) }, '▶ ' + p.label))),
          h('div', { class: 'row', style: { marginTop: '14px', alignItems: 'flex-start', gap: '14px' } },
            h('div', { style: { textAlign: 'center' } }, meter, h('div', { class: 'tiny muted', style: { marginTop: '4px' } }, 'cAMP')),
            h('div', { class: 'grow' },
              h('div', { class: 'tiny', style: { color: CA.tc('#ff7b72'), marginBottom: '10px' } }, '— depression threshold'),
              outcome, explain, refsEl)),
          h('p', { class: 'tiny muted', style: { marginTop: '10px' } }, 'A toy model: cAMP levels and thresholds are illustrative, not measured.'))),
      h('h3', { style: { marginTop: '28px' } }, 'Neuromodulators and neuropeptides of the learning circuit'),
      h('p', { class: 'small muted', style: { maxWidth: '920px' } }, (CFG.neuromodulation || {}).desc || ''),
      h('div', { class: 'card' }, CA.neuromodMatrix ? CA.neuromodMatrix(CFG.neuromodulation, 'fly') : null),
      h('h3', { style: { marginTop: '28px' } }, 'Where the cells come from'),
      h('div', { class: 'svgwrap', style: { padding: '6px' } }, lineage()),
      h('p', { class: 'small muted', style: { marginTop: '6px' } }, ...CA.citeChips(['itok1997', 'leet1999', 'jefferis2001'])),
      h('h3', { style: { marginTop: '28px' } }, 'Genes, cells, behaviour and disease'),
      h('div', { class: 'card' }, geneTable())));
    paintGeno();
    unsub = CA.on('select', paintSel);
    paintSel();
  }
  function unmount() { timers.forEach(clearTimeout); timers = []; if (unsub) unsub(); unsub = null; }

  /* ------------------------------------------------------------------ the synapse */
  function el(entity, label, ...kids) {
    const g = s('g', { class: 'mc-el', 'data-entity': entity }, ...kids);
    g.addEventListener('mousemove', (ev) => CA.tip.show(`<b>${CA.esc(label)}</b>`, ev));
    g.addEventListener('mouseleave', () => CA.tip.hide());
    g.addEventListener('click', () => CA.select(entity));
    return g;
  }
  const txt = (x, y, t, o) => s('text', Object.assign({ x, y, fill: CA.tc('#c9d1d9'), 'font-size': 12, 'text-anchor': 'middle', 'pointer-events': 'none' }, o || {}), t);
  const pill = (x, y, w, hgt, color, label, id) => [s('rect', { id, x, y, width: w, height: hgt, rx: hgt / 2, fill: color, opacity: 0.9 }), txt(x + w / 2, y + hgt / 2 + 4, label, { fill: CA.tc('#0d1117'), 'font-weight': 600, 'font-size': 11.5 })];
  const arrow = (d, color, dash, id) => s('path', { id, d, stroke: color, 'stroke-width': 1.6, fill: 'none', 'stroke-dasharray': dash || '', 'marker-end': 'url(#mah)' });

  function drawSynapse() {
    svg.append(
      s('defs', {}, s('marker', { id: 'mah', viewBox: '0 0 10 10', refX: 8, refY: 5, markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse' }, s('path', { d: 'M0 0 L10 5 L0 10 z', fill: CA.tc('#8b949e') }))),
      // Kenyon cell terminal
      el('fly-kc', 'Kenyon cell axon terminal, in one mushroom body compartment',
        s('path', { d: 'M 40 40 C 40 18, 560 18, 560 40 L 560 300 C 560 330, 40 330, 40 300 Z', fill: CA.tc('rgba(227,179,65,0.08)'), stroke: C.kc, 'stroke-width': 1.5 }),
        txt(300, 40, 'Kenyon cell axon terminal', { fill: C.kc })),
      s('rect', { id: 'cafill', x: 42, y: 300, width: 516, height: 0, fill: C.ca, opacity: 0.12 }),
      txt(56, 78, 'odour → spikes → Ca²⁺', { fill: C.ca, 'font-size': 11.5, 'text-anchor': 'start' }),
      el('fly-camp', 'Ca²⁺/calmodulin: activates the rutabaga adenylyl cyclase', ...pill(56, 92, 104, 26, C.cam, 'Ca²⁺/CaM')),
      el('fly-camp', 'rutabaga adenylyl cyclase: stimulated by Ca²⁺/calmodulin and by Gαs, so it detects the coincidence of odour and dopamine', ...pill(206, 128, 138, 30, C.rut, 'rutabaga cyclase', 'rutpill')),
      el('fly-dopr', 'DopR1 (dDA1): D1-like dopamine receptor, coupled to Gαs and cAMP', ...pill(470, 92, 82, 26, C.dopr1, 'DopR1', 'dopr1pill')),
      el('fly-dopr', 'DopR2: dopamine receptor coupled to a different second messenger; potentiation after backward pairing', ...pill(470, 194, 82, 26, C.dopr2, 'DopR2', 'dopr2pill')),
      txt(420, 132, 'Gαs', { fill: C.dopr1, 'font-size': 11 }),
      arrow('M 160 112 C 180 120, 192 132, 204 140', CA.tc('#8b949e')),
      arrow('M 470 112 C 420 118, 380 130, 346 140', C.dopr1, '', 'gsarrow'),
      el('fly-camp', 'cAMP: made by rutabaga, broken down by the dunce phosphodiesterase',
        s('ellipse', { id: 'camp', cx: 275, cy: 200, rx: 52, ry: 22, fill: C.camp, 'fill-opacity': 0.25, stroke: C.camp }), txt(275, 205, 'cAMP', { fill: C.camp, 'font-weight': 600 })),
      arrow('M 275 158 L 275 176', CA.tc('#8b949e')),
      el('fly-dunce', 'dunce: cAMP phosphodiesterase, breaks cAMP down', ...pill(96, 188, 88, 26, C.dnc, 'dunce PDE', 'dncpill')),
      arrow('M 222 200 L 186 200', C.dnc, '3 3'),
      txt(204, 228, 'breaks down', { fill: CA.tc('#8b949e'), 'font-size': 10 }),
      el('fly-camp', 'Protein kinase A: acts on release machinery; depression', ...pill(240, 240, 70, 24, C.pka, 'PKA')),
      arrow('M 275 222 L 275 238', CA.tc('#8b949e')),
      arrow('M 310 252 C 360 262, 380 280, 390 292', C.pka, '4 3'),
      txt(420, 272, 'depression', { fill: C.pka, 'font-size': 11 }),
      arrow('M 510 220 C 520 260, 480 280, 430 294', C.dopr2, '4 3'),
      txt(520, 262, 'potentiation', { fill: C.dopr2, 'font-size': 11 }),
      s('g', { id: 'ves' }),
      // output neuron dendrite
      el('fly-mbon', 'Mushroom body output neuron dendrite',
        s('path', { d: 'M 60 360 C 60 344, 540 344, 540 360 L 540 430 L 60 430 Z', fill: CA.tc('rgba(210,168,255,0.10)'), stroke: C.mbon, 'stroke-width': 1.5 }),
        txt(300, 412, 'Output neuron dendrite', { fill: C.mbon })),
      s('g', { id: 'release' }),
      // dopamine neuron terminal
      el('fly-dan', 'Dopamine neuron terminal: punishment (PPL1) or reward (PAM) for this compartment',
        s('path', { d: 'M 620 70 C 620 50, 740 50, 740 70 L 740 230 C 740 250, 620 250, 620 230 Z', fill: CA.tc('rgba(248,81,73,0.10)'), stroke: C.da, 'stroke-width': 1.5 }),
        txt(680, 92, 'dopamine', { fill: C.da }), txt(680, 108, 'neuron', { fill: C.da })),
      s('g', { id: 'dadots' }),
      el('fly-dpm', 'DPM neurons: serotonin and the Amnesiac neuropeptide onto the lobes, for memory',
        s('path', { d: 'M 690 300 C 650 320, 600 300, 566 290', stroke: CA.tc('#bc8cff'), 'stroke-width': 2, fill: 'none', 'stroke-dasharray': '2 3' }),
        txt(700, 320, 'DPM: 5-HT, Amnesiac', { fill: CA.tc('#bc8cff'), 'font-size': 10.5 })));
    drawVesicles();
  }

  function drawVesicles() {
    const g = svg.querySelector('#ves');
    CA.clear(g);
    for (let i = 0; i < strength; i++) {
      const x = 90 + i * 44;
      g.appendChild(s('circle', { cx: x, cy: 306, r: 9, fill: 'none', stroke: C.ves, 'stroke-width': 1.6 }));
    }
    g.appendChild(txt(560 - 6, 318, `release: ${strength}`, { 'text-anchor': 'end', fill: C.ves, 'font-size': 10.5 }));
  }

  function setLevel(level) {
    meter.querySelector('.fill').style.height = Math.round(level * 100) + '%';
    svg.querySelector('#camp').setAttribute('fill-opacity', 0.15 + level * 0.7);
  }
  function paintGeno() {
    const dim = (id, on) => { const e = svg.querySelector('#' + id); if (e) e.setAttribute('opacity', on ? 0.9 : 0.2); };
    dim('rutpill', geno !== 'rut'); dim('dncpill', geno !== 'dnc'); dim('dopr1pill', geno !== 'dopr1'); dim('gsarrow', geno !== 'dopr1');
    setLevel(geno === 'dnc' ? 0.7 : 0.08);
    outcome.textContent = 'Choose a protocol'; outcome.style.borderLeftColor = CA.tc('#6e7681');
    explain.textContent = geno === 'wt' ? '' : {
      rut: 'rutabaga: the Ca²⁺/calmodulin-stimulated adenylyl cyclase is missing (Livingstone et al., 1984).',
      dnc: 'dunce: the cAMP phosphodiesterase is missing (Byers et al., 1981), so cAMP stays high.',
      dopr1: 'DopR1 (dDA1) mutant: dopamine cannot raise cAMP through Gαs (Kim et al., 2007; Handler et al., 2019).',
    }[geno];
    CA.clear(refsEl);
  }

  function run(key) {
    timers.forEach(clearTimeout); timers = [];
    const o = outcomeOf(key, geno);
    outcome.textContent = 'Stimulating…'; outcome.style.borderLeftColor = CA.tc('#6e7681');
    explain.textContent = '';
    const odour = key !== 'da', da = key !== 'odour', daFirst = key === 'bwd';
    const ca = svg.querySelector('#cafill'), dots = svg.querySelector('#dadots');
    const pulseCa = () => { ca.setAttribute('height', 150); ca.setAttribute('y', 150); timers.push(setTimeout(() => { ca.setAttribute('height', 0); ca.setAttribute('y', 300); }, 600)); };
    const pulseDa = () => {
      CA.clear(dots);
      for (let i = 0; i < 14; i++) dots.appendChild(s('circle', { cx: 600 - Math.random() * 30, cy: 90 + Math.random() * 120, r: 3, fill: C.da }));
      timers.push(setTimeout(() => CA.clear(dots), 650));
    };
    const first = daFirst ? pulseDa : odour ? pulseCa : pulseDa;
    const second = key === 'fwd' ? pulseDa : key === 'bwd' ? pulseCa : null;
    first();
    if (second) timers.push(setTimeout(second, 420));
    timers.push(setTimeout(() => setLevel(o.camp), 700));
    timers.push(setTimeout(() => {
      const before = strength;
      strength = CA.clamp(strength + o.change, 2, 10);
      drawVesicles();
      const d = strength - before;
      outcome.textContent = o.change < 0 ? (d ? 'Depression: less transmitter released onto the output neuron' : 'Depression (already at the floor)')
        : o.change > 0 ? (d ? 'Potentiation: more transmitter released' : 'Potentiation (already at the ceiling)') : 'No lasting change';
      outcome.style.borderLeftColor = o.change < 0 ? CA.tc('#ff7b72') : o.change > 0 ? CA.tc('#3fb950') : CA.tc('#6e7681');
      explain.textContent = o.why;
      CA.clear(refsEl).append(...CA.citeChips(o.refs));
    }, 1350));
  }

  function paintSel() {
    root.querySelectorAll('.mc-el, .nm-row, .nmx th.col').forEach((g) => g.classList.toggle('sel', g.dataset.entity === CA.selected));
  }

  /* ------------------------------------------------------------------ lineage */
  function lineage() {
    const g = s('svg', { viewBox: '0 0 960 240', width: '100%', style: { display: 'block' }, role: 'img', 'aria-label': 'Developmental origin of Kenyon cells and projection neurons' });
    const box = (x, y, w, label, entity, color, sub) => g.appendChild(el(entity, (CA.ent[entity] || {}).name || label,
      s('rect', { x, y, width: w, height: 42, rx: 8, fill: color + '26', stroke: color, 'stroke-width': 1.5 }),
      txt(x + w / 2, y + (sub ? 18 : 26), label, { fill: CA.tc('#e6edf3'), 'font-weight': 600 }),
      sub ? txt(x + w / 2, y + 33, sub, { fill: CA.tc('#8b949e'), 'font-size': 10.5 }) : null));
    const arrowL = (x1, y1, x2, y2) => g.appendChild(s('path', { d: `M ${x1} ${y1} C ${(x1 + x2) / 2} ${y1}, ${(x1 + x2) / 2} ${y2}, ${x2} ${y2}`, stroke: CA.tc('#8b949e'), 'stroke-width': 1.5, fill: 'none', 'marker-end': 'url(#lah2)' }));
    g.appendChild(s('defs', {}, s('marker', { id: 'lah2', viewBox: '0 0 10 10', refX: 8, refY: 5, markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse' }, s('path', { d: 'M0 0 L10 5 L0 10 z', fill: CA.tc('#8b949e') }))));
    const kc = CA.tc('#e3b341'), nb = CA.tc('#f778ba'), pn = CA.tc('#3fb950');
    box(20, 50, 200, 'Mushroom body neuroblasts', 'fly-nb', nb, 'four, each making every type');
    box(300, 6, 200, 'γ Kenyon cells', 'fly-kc', kc, 'born first, in the larva');
    box(300, 62, 200, 'α′/β′ Kenyon cells', 'fly-kc', kc, 'late larva, until pupation');
    box(300, 118, 200, 'α/β Kenyon cells', 'fly-kc', kc, 'after puparium formation');
    box(580, 6, 330, 'At metamorphosis, γ neurons prune their', 'fly-kc', kc, 'larval branches and grow into the adult γ lobe');
    arrowL(220, 70, 300, 27); arrowL(220, 71, 300, 83); arrowL(220, 72, 300, 139); arrowL(500, 27, 580, 27);
    box(20, 186, 200, 'Projection neuron lineages', 'fly-pn', pn, 'lineage and birth order…');
    box(300, 186, 200, '…choose the glomerulus', 'fly-al', pn, 'and so the receptor input');
    arrowL(220, 207, 300, 207);
    g.appendChild(txt(940, 232, 'Click a box for evidence', { fill: CA.tc('#6e7681'), 'font-size': 11, 'text-anchor': 'end' }));
    return g;
  }

  /* ------------------------------------------------------------------ genes, cells, behaviour and disease */
  function geneTable() {
    const learning = [
      ['fly-dunce', 'fly-kc', 'cAMP phosphodiesterase; mutants fail to learn, or forget within 30 minutes', 'f-associative', ['dudai1976', 'byers1981', 'tully1985']],
      ['fly-camp', 'fly-kc', 'rutabaga: Ca²⁺/calmodulin-stimulated adenylyl cyclase, needed in Kenyon cells only', 'f-associative', ['livingstone1984', 'zars2000']],
      ['fly-dopr', 'fly-kc', 'dDA1 (DopR1) needed for shock and sugar learning; DopR1 and DopR2 set the sign of plasticity by timing', 'f-associative', ['kimyc2007', 'handler2019']],
      ['fly-no', 'fly-dan', 'Nitric oxide cotransmitter in MB dopamine neurons acts on soluble guanylate cyclase Gyc88E in Kenyon cells to regulate memory decay and updating', 'f-associative', ['aso2019no']],
      ['fly-co', 'fly-kc', 'Heme oxygenase in Kenyon cells synthesizes CO as an on-demand retrograde messenger regulating dopamine release', 'f-associative', ['ueno2017']],
      ['fly-snpf', 'fly-orn', 'Short neuropeptide F upregulates sNPFR1 in ORNs to facilitate presynaptic transmitter release during starvation', 'f-smell', ['root2011', 'nassel2022']],
      ['fly-sifa', 'fly-sif-n', 'Four hub neurons release SIFamide brain-wide to arbitrate behavioral priorities, suppressing courtship for feeding', 'f-reward', ['martelli2017', 'nassel2022']],
      ['fly-pdf', 'fly-lnv', 'Pigment-dispersing factor released by LNv clock neurons signals via PDFR to synchronize circadian rhythms and morning anticipation', 'f-sleep', ['renn1999']],
      ['fly-ta', 'fly-gng', 'Tyramine acts via TyrR to coordinate motor switching and locomotion, distinct from octopamine', 'f-motor', ['roeder2005']],
      ['fly-ha', 'fly-retina', 'Histamine released by photoreceptors provides fast inhibitory transmission to lamina neurons via ort/HisCl1 channels', 'f-vision', ['gengs2002']],
      ['fly-amn', 'fly-dpm', 'Neuropeptide released by the DPM neurons onto the lobes; mutants forget quickly', 'f-consolidation', ['waddell2000', 'tully1985']],
      ['fly-creb', null, 'A dominant-negative CREB blocks long-term memory but spares learning', 'f-consolidation', ['yin1994', 'tully1994']],
      ['fly-or', 'fly-orn', 'Or83b, the broadly expressed co-receptor, is needed for responses to many odours', 'f-smell', ['larsson2004']],
      ['fly-fru', null, 'Male-specific splicing specifies the neurons of courtship', 'f-social', ['demir2005', 'manoli2005']],
      ['fly-shaker', null, 'Potassium channel; minisleep mutants sleep a third of the normal amount', 'f-sleep', ['cirelli2005']],
    ];
    const disease = [
      ['fly-m-pd', null, 'Human α-synuclein: adult-onset loss of dopaminergic neurons, inclusions and locomotor decline; parkin loss: muscle degeneration with mitochondrial pathology', 'c-parkinson', ['feany2000', 'greene2003']],
      ['fly-m-ad', null, 'Human Aβ42: amyloid deposits, age-dependent learning defects and neurodegeneration', 'c-alzheimers', ['iijima2004']],
      ['fly-m-fxs', 'fly-mb', 'Loss of dfmr1: courtship-memory and mushroom body defects, rescued by mGluR antagonists or lithium', 'c-fxs', ['mcbride2005']],
      ['fly-m-polyq', null, 'Expanded-polyglutamine SCA3 fragment: nuclear inclusions and late-onset neurodegeneration', 'c-sca', ['warrick1998']],
    ];
    const row = ([g, c, m, d, ref]) => h('tr', {},
      h('td', {}, CA.entChip(g)), h('td', {}, c ? CA.entChip(c) : h('span', { class: 'muted' }, '—')), h('td', { class: 'small' }, m), h('td', {}, CA.entChip(d)), h('td', {}, CA.citeChips(ref)));
    return h('div', { class: 'nmx-wrap' }, h('table', { class: 'data' },
      h('tr', {}, h('th', {}, 'Gene or model'), h('th', {}, 'Cell'), h('th', {}, 'What it does'), h('th', {}, 'Links to'), h('th', {}, 'Evidence')),
      h('tr', {}, h('td', { colspan: 5, class: 'tiny muted' }, 'Learning, memory, smell, courtship and sleep')),
      learning.map(row),
      h('tr', {}, h('td', { colspan: 5, class: 'tiny muted' }, 'Fly models of human brain disease, linked to the disorders in the other regions of this atlas')),
      disease.map(row)));
  }
})();
