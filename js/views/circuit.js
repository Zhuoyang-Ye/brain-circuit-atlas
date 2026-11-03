/* Microcircuit: interactive schematic of the cerebellar cortex + a toy eyeblink-conditioning learning lab. */
(function () {
  'use strict';
  const CA = window.CA, h = CA.h, s = CA.s;
  let root, svg, unsub = null, anims = [], stopped = false, caption;

  CA.register('circuit', { title: 'Microcircuit', mount, unmount });

  const COL = { pc: '#f778ba', gc: '#79c0ff', golgi: '#a5d6ff', mli: '#d2a8ff', ubc: '#56d4dd', mf: '#3fb9a5', pf: '#ffa657', cf: '#ff9e64', dcn: '#ff5f57', io: '#ffa657', exc: '#3fb950', inh: '#ff7b72' };
  const PCX = [250, 470, 690];

  function mount(node) {
    root = node;
    stopped = false;
    svg = s('svg', { viewBox: '0 0 900 650', width: '100%', style: { display: 'block' } });
    drawCircuit();
    caption = h('div', { class: 'small muted', style: { minHeight: '2.6em', marginTop: '8px' } }, 'Hover or click any element. Play a signal to watch information flow.');
    const lab = buildLab();
    root.appendChild(h('div', { class: 'page', style: { maxWidth: '1400px' } },
      h('div', { class: 'page-head' }, h('div', {},
        h('h2', {}, 'The cerebellar microcircuit'),
        h('p', {}, 'The same three-layer circuit repeats across the whole cerebellar cortex, whether a module serves eye movements, language or social behavior. Two inputs, mossy fibers and climbing fibers, converge on Purkinje cells, the only output of the cortex.'))),
      h('div', { class: 'lab-grid' },
        h('div', {},
          h('div', { class: 'svgwrap', style: { padding: '6px' } }, svg),
          h('div', { class: 'row', style: { marginTop: '10px' } },
            h('button', { class: 'btn', onclick: () => playMossy() }, '▶ Mossy-fiber input'),
            h('button', { class: 'btn', onclick: () => playClimbing() }, '▶ Climbing-fiber input'),
            h('button', { class: 'btn', onclick: () => playFFI() }, '▶ Feedforward inhibition'),
            h('span', { class: 'grow' }),
            h('span', { class: 'row small muted' }, h('span', { class: 'dot', style: { background: COL.exc } }), 'excitatory', h('span', { class: 'dot', style: { background: COL.inh } }), 'inhibitory synapse')),
          caption),
        lab)));
    unsub = CA.on('select', paintSel);
    paintSel();
  }
  function unmount() { stopped = true; anims.forEach((a) => cancelAnimationFrame(a)); anims = []; if (unsub) unsub(); }

  /* ------------------------------------------------------------------ schematic */
  function grp(entity, label, ...kids) {
    const g = s('g', { class: 'mc-el', 'data-entity': entity }, ...kids);
    g.addEventListener('mousemove', (ev) => CA.tip.show(`<b>${CA.esc(label)}</b><br><span class="muted">${CA.esc(CA.ent[entity] ? CA.ent[entity].name : '')}</span>`, ev));
    g.addEventListener('mouseleave', () => CA.tip.hide());
    g.addEventListener('click', () => CA.select(entity));
    return g;
  }
  const syn = (x, y, inh) => s('circle', { cx: x, cy: y, r: 3.6, fill: inh ? COL.inh : COL.exc, stroke: '#0d1117', 'stroke-width': 1 });

  function drawCircuit() {
    const layer = (y0, y1, fill, label) => [
      s('rect', { x: 0, y: y0, width: 900, height: y1 - y0, fill }),
      s('text', { x: 10, y: y0 + 16, fill: '#8b949e', 'font-size': 12 }, label)];
    svg.append(...layer(20, 250, 'rgba(179,146,240,0.07)', 'Molecular layer'),
      ...layer(250, 284, 'rgba(247,120,186,0.09)', 'Purkinje layer'),
      ...layer(284, 425, 'rgba(88,166,255,0.06)', 'Granular layer'),
      ...layer(425, 470, 'rgba(139,148,158,0.07)', 'White matter'),
      s('text', { x: 10, y: 494, fill: '#8b949e', 'font-size': 12 }, 'Brainstem & cerebellar nuclei'));

    // parallel fibers
    const pfY = [62, 88, 114, 140, 166, 192, 218];
    svg.appendChild(grp('mf-pathway', 'Parallel fibers (granule-cell axons)',
      ...pfY.map((y, i) => s('line', { id: 'pf' + i, x1: 60, x2: 880, y1: y, y2: y, stroke: COL.pf, 'stroke-width': 1.5, opacity: 0.55 }))));

    // Purkinje cells
    PCX.forEach((x, k) => {
      const d = `M ${x} 254 L ${x} 206 M ${x} 214 L ${x - 46} 150 L ${x - 62} 56 M ${x - 46} 150 L ${x - 24} 66 M ${x - 46} 150 L ${x - 80} 110
                 M ${x} 214 L ${x + 42} 140 L ${x + 58} 52 M ${x + 42} 140 L ${x + 16} 70 M ${x + 42} 140 L ${x + 82} 100 M ${x} 206 L ${x + 4} 120 L ${x - 6} 44`;
      const axon = `M ${x} 278 C ${x} 380, ${600 + k * 20} 440, ${610 + k * 22} 528`;
      svg.appendChild(grp('purkinje', 'Purkinje cell',
        s('path', { id: 'pcd' + k, d, stroke: COL.pc, 'stroke-width': 2.6, fill: 'none', 'stroke-linecap': 'round' }),
        s('path', { id: 'pca' + k, d: axon, stroke: COL.pc, 'stroke-width': 1.6, fill: 'none', opacity: 0.8 }),
        s('circle', { cx: x, cy: 266, r: 12, fill: COL.pc }),
        syn(610 + k * 22, 528, true),
        // a few PF synapses on the dendrites
        syn(x - 52, 114, false), syn(x + 50, 88, false), syn(x - 2, 140, false)));
    });
    // Purkinje collateral (Witter et al., 2016)
    svg.appendChild(grp('purkinje', 'Purkinje-cell axon collateral (feeds back to Purkinje cells and interneurons)',
      s('path', { d: 'M 470 290 C 430 320, 320 310, 262 280', stroke: COL.pc, 'stroke-width': 1.3, fill: 'none', 'stroke-dasharray': '4 3' }), syn(262, 280, true)));

    // granule cells with ascending axons
    const gcs = [[350, 352, 0], [388, 372, 2], [425, 344, 4], [515, 362, 1], [552, 346, 3], [590, 374, 5], [322, 392, 6]];
    svg.appendChild(grp('granule', 'Granule cells (most numerous neurons in the brain)',
      ...gcs.map(([x, y, i]) => s('path', { id: 'gca' + i, d: `M ${x} ${y} L ${x} ${pfY[i]}`, stroke: COL.gc, 'stroke-width': 1.3, fill: 'none', opacity: 0.85 })),
      ...gcs.map(([x, y, i]) => s('path', { d: `M ${x - 10} ${pfY[i]} L ${x + 10} ${pfY[i]}`, stroke: COL.gc, 'stroke-width': 2 })),
      ...gcs.map(([x, y]) => s('circle', { cx: x, cy: y, r: 6.5, fill: COL.gc }))));

    // mossy fibers from pontine nuclei, with collateral to the nuclei
    svg.appendChild(grp('mf-pathway', 'Mossy fibers (from pontine, spinal, vestibular and reticular nuclei)',
      s('path', { id: 'mf0', d: 'M 450 588 C 450 520, 372 470, 372 382', stroke: COL.mf, 'stroke-width': 2.4, fill: 'none' }),
      s('path', { id: 'mf1', d: 'M 450 520 C 470 470, 548 440, 552 390', stroke: COL.mf, 'stroke-width': 2.4, fill: 'none' }),
      s('path', { id: 'mfc', d: 'M 452 548 C 500 552, 560 552, 590 548', stroke: COL.mf, 'stroke-width': 1.6, fill: 'none' }),
      s('circle', { cx: 372, cy: 374, r: 10, fill: 'none', stroke: COL.mf, 'stroke-width': 2.4 }),
      s('circle', { cx: 552, cy: 382, r: 10, fill: 'none', stroke: COL.mf, 'stroke-width': 2.4 }),
      syn(362, 370, false), syn(545, 375, false), syn(590, 548, false)));

    // Golgi cell
    svg.appendChild(grp('golgi', 'Golgi cell: inhibits granule cells (feedforward and feedback)',
      s('path', { d: 'M 465 312 L 465 150 M 465 200 L 440 120 M 465 220 L 500 130', stroke: COL.golgi, 'stroke-width': 1.4, fill: 'none', opacity: 0.7 }),
      s('path', { d: 'M 465 320 C 430 340, 400 360, 380 368 M 465 320 C 500 340, 530 365, 548 374', stroke: COL.golgi, 'stroke-width': 1.4, fill: 'none', 'stroke-dasharray': '3 2' }),
      s('circle', { cx: 465, cy: 314, r: 9, fill: COL.golgi }), syn(382, 380, true), syn(560, 388, true)));

    // molecular layer interneurons (stellate + basket)
    svg.appendChild(grp('mli', 'Molecular-layer interneurons (stellate and basket cells): inhibit Purkinje cells',
      s('path', { id: 'mli0', d: 'M 360 104 L 412 116 L 424 114', stroke: COL.mli, 'stroke-width': 1.5, fill: 'none' }),
      s('path', { id: 'mli1', d: 'M 600 128 L 650 118 L 666 112', stroke: COL.mli, 'stroke-width': 1.5, fill: 'none' }),
      s('path', { id: 'mli2', d: 'M 340 226 C 300 236, 280 250, 262 258', stroke: COL.mli, 'stroke-width': 1.5, fill: 'none' }),
      s('circle', { cx: 360, cy: 104, r: 7, fill: COL.mli }), s('circle', { cx: 600, cy: 128, r: 7, fill: COL.mli }), s('circle', { cx: 340, cy: 226, r: 7, fill: COL.mli }),
      syn(424, 114, true), syn(666, 112, true), syn(262, 258, true)));

    // unipolar brush cell
    svg.appendChild(grp('ubc', 'Unipolar brush cell (vestibular lobules): amplifies mossy-fiber input',
      s('path', { d: 'M 212 392 C 200 400, 196 408, 192 414 M 212 392 C 206 404, 206 412, 204 418', stroke: COL.ubc, 'stroke-width': 1.6, fill: 'none' }),
      s('path', { d: 'M 220 384 L 236 330', stroke: COL.ubc, 'stroke-width': 1.3, fill: 'none' }),
      s('circle', { cx: 218, cy: 388, r: 7.5, fill: COL.ubc })));

    // climbing fiber from the inferior olive, wrapping the middle Purkinje dendrite
    const cfd = 'M 196 566 C 210 490, 470 500, 476 292 L 476 262 L 466 248 L 476 234 L 466 220 L 474 206 L 464 194 L 452 178 L 442 168 L 432 154 L 424 140 L 418 120 L 412 104 L 410 84 L 408 66';
    svg.appendChild(grp('cf-pathway', 'Climbing fiber: one per Purkinje cell; triggers complex spikes',
      s('path', { id: 'cf', d: cfd, stroke: COL.cf, 'stroke-width': 2.2, fill: 'none' }), syn(472, 226, false), syn(436, 160, false)));

    // nuclei, olive, pons
    svg.appendChild(grp('dcn-neurons', 'Cerebellar nuclear neurons: receive Purkinje inhibition and mossy-fiber collaterals',
      s('ellipse', { cx: 640, cy: 556, rx: 82, ry: 32, fill: 'rgba(255,95,87,0.22)', stroke: COL.dcn, 'stroke-width': 1.6 }),
      s('text', { x: 640, y: 560, 'text-anchor': 'middle', fill: '#ffd8d3', 'font-size': 12.5 }, 'Cerebellar nuclei')));
    svg.appendChild(grp('dcn', 'Output to thalamus, red nucleus, VTA, PAG, vestibular nuclei…',
      s('path', { id: 'out', d: 'M 722 556 L 860 556', stroke: COL.dcn, 'stroke-width': 2.4, fill: 'none', 'marker-end': 'url(#arrow)' }),
      s('text', { x: 735, y: 545, fill: '#c9d1d9', 'font-size': 11.5 }, 'to thalamus, red nucleus,'),
      s('text', { x: 735, y: 578, fill: '#c9d1d9', 'font-size': 11.5 }, 'VTA, PAG, olive …')));
    svg.appendChild(grp('dcn-neurons', 'Nucleo-olivary inhibition: closes the olivo-cortico-nuclear loop',
      s('path', { id: 'no', d: 'M 580 578 C 470 630, 320 630, 236 590', stroke: COL.inh, 'stroke-width': 1.5, fill: 'none', 'stroke-dasharray': '5 3' }), syn(236, 590, true)));
    svg.appendChild(grp('io-neurons', 'Inferior olive: electrically coupled neurons, source of climbing fibers',
      s('ellipse', { cx: 180, cy: 584, rx: 62, ry: 26, fill: 'rgba(255,166,87,0.18)', stroke: COL.io, 'stroke-width': 1.6 }),
      s('text', { x: 180, y: 588, 'text-anchor': 'middle', fill: '#ffe2c6', 'font-size': 12.5 }, 'Inferior olive')));
    svg.appendChild(grp('pontine', 'Pontine nuclei: relay cerebral cortex → cerebellum',
      s('ellipse', { cx: 430, cy: 604, rx: 66, ry: 22, fill: 'rgba(63,185,165,0.18)', stroke: COL.mf, 'stroke-width': 1.6 }),
      s('text', { x: 430, y: 608, 'text-anchor': 'middle', fill: '#c8f5ec', 'font-size': 12.5 }, 'Pontine nuclei'),
      s('text', { x: 330, y: 636, fill: '#8b949e', 'font-size': 11 }, '← input from cerebral cortex')));
    svg.appendChild(s('defs', {}, s('marker', { id: 'arrow', viewBox: '0 0 10 10', refX: 8, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse' },
      s('path', { d: 'M 0 0 L 10 5 L 0 10 z', fill: COL.dcn }))));
    svg.appendChild(s('g', { id: 'pulses' }));
  }

  function paintSel() {
    svg.querySelectorAll('.mc-el').forEach((g) => g.classList.toggle('sel', g.dataset.entity === CA.selected));
  }

  /* ------------------------------------------------------------------ animations */
  function pulseAlong(id, color, ms, reverse) {
    return new Promise((resolve) => {
      const path = svg.querySelector('#' + id);
      if (!path || stopped) return resolve();
      const len = path.getTotalLength();
      const dot = s('circle', { r: 5.5, fill: color, stroke: '#fff', 'stroke-width': 1.2 });
      svg.querySelector('#pulses').appendChild(dot);
      const t0 = performance.now();
      const step = (now) => {
        if (stopped) { dot.remove(); return resolve(); }
        const k = Math.min(1, (now - t0) / ms);
        const p = path.getPointAtLength((reverse ? 1 - k : k) * len);
        dot.setAttribute('cx', p.x); dot.setAttribute('cy', p.y);
        if (k < 1) anims.push(requestAnimationFrame(step)); else { dot.remove(); resolve(); }
      };
      anims.push(requestAnimationFrame(step));
    });
  }
  function flash(id, color, ms) {
    const el = svg.querySelector('#' + id);
    if (!el) return Promise.resolve();
    const old = { stroke: el.getAttribute('stroke'), w: el.getAttribute('stroke-width') };
    el.setAttribute('stroke', color); el.setAttribute('stroke-width', 4.5);
    return new Promise((r) => setTimeout(() => { el.setAttribute('stroke', old.stroke); el.setAttribute('stroke-width', old.w); r(); }, ms));
  }
  const say = (t) => { caption.textContent = t; };

  async function playMossy() {
    say('Mossy fibers carry sensory, motor and cortical context to thousands of granule cells (and send collaterals to the nuclei).');
    await Promise.all([pulseAlong('mf0', COL.mf, 900), pulseAlong('mf1', COL.mf, 900), pulseAlong('mfc', COL.mf, 1400)]);
    say('Granule cells recode the input; their axons ascend and split into parallel fibers that cross many Purkinje dendrites.');
    await Promise.all([0, 2, 4, 1].map((i) => pulseAlong('gca' + i, COL.gc, 700)));
    await Promise.all([0, 2, 4, 1].map((i) => pulseAlong('pf' + i, COL.pf, 1500)));
    say('Purkinje cells sum ~100,000 parallel-fiber inputs into simple spikes and inhibit the nuclei: cortical output is a pattern of pauses and bursts in inhibition.');
    await Promise.all([0, 1, 2].map((k) => flash('pcd' + k, '#ffffff', 260)));
    await Promise.all([0, 1, 2].map((k) => pulseAlong('pca' + k, COL.inh, 900)));
    say('The nuclei combine Purkinje inhibition with excitatory collaterals and send the cerebellum\'s output to the rest of the brain.');
    await pulseAlong('out', COL.dcn, 700);
  }
  async function playClimbing() {
    say('The inferior olive fires a climbing fiber, about once per second, wrapping one Purkinje cell\'s dendrite with hundreds of synapses.');
    await pulseAlong('cf', COL.cf, 1500);
    say('Complex spike: a dendritic calcium surge. Parallel-fiber synapses active at the same moment are depressed (LTD); without it they potentiate (LTP).');
    await flash('pcd1', COL.cf, 900);
    say('Classic view: an error signal teaching motor learning. Newer data: climbing fibers also signal reward and learned predictions (Heffley 2018; Kostadinov 2019).');
    await pulseAlong('no', COL.inh, 1100, true);
  }
  async function playFFI() {
    say('Parallel fibers excite molecular-layer interneurons as well as Purkinje cells…');
    await Promise.all([pulseAlong('pf0', COL.pf, 900), pulseAlong('pf1', COL.pf, 900)]);
    say('…which inhibit Purkinje dendrites and somata a moment later, sharpening timing. MLIs also gate climbing-fiber calcium and can flip plasticity from potentiation to depression (Rowan et al., 2018).');
    await Promise.all([pulseAlong('mli0', COL.inh, 600), pulseAlong('mli1', COL.inh, 600), pulseAlong('mli2', COL.inh, 600)]);
    await Promise.all([0, 1].map((k) => flash('pcd' + k, COL.inh, 400)));
  }

  /* ------------------------------------------------------------------ learning lab (toy model) */
  const DT = 5, T = 1000, CS = 100, NB = 50, EYE_FULL = 25;
  const NT = T / DT;
  const tau = Array.from({ length: NB }, (_, i) => i * 16);
  const G = tau.map((tu) => {
    const sg = 15 + 0.12 * tu;
    return Float64Array.from({ length: NT }, (_, k) => { const t = k * DT; return t >= CS ? Math.exp(-((t - CS - tu) ** 2) / (2 * sg * sg)) : 0; });
  });
  const S = Float64Array.from({ length: NT }, (_, k) => Math.max(1e-9, G.reduce((a, g) => a + g[k], 0)));
  const GBAR = G.map((g) => g.reduce((a, b) => a + b, 0) / NT);
  const SCEN = {
    classic: { label: 'Wild type', ltd: true, other: false, ref: ['mccormick1984', 'ito1982', 'medina2008'],
      text: 'LTD at parallel-fiber synapses active just before the climbing-fiber (air-puff) signal creates a well-timed pause in Purkinje firing; the disinhibited nuclei drive the learned eyelid closure.' },
    mglur1: { label: 'mGluR1 knockout (no LTD induction)', ltd: false, other: false, ref: ['aiba1994'],
      text: 'mGluR1-knockout mice lack LTD and show impaired eyeblink conditioning (Aiba et al., 1994). Caution: they are also ataxic and keep multiple climbing fibers, so other defects contribute.' },
    expr: { label: 'LTD-expression mutant + other plasticity', ltd: false, other: true, ref: ['schonewille2011', 'gao2012', 'rowan2018'],
      text: 'Mutants that cannot internalize AMPA receptors lack LTD yet learn normally (Schonewille et al., 2011). Here a second, climbing-fiber-gated mechanism (e.g., interneuron or intrinsic plasticity) takes over. In this toy it is slower; in the mice, learning was not impaired.' },
  };
  let M;
  function resetModel() {
    M = { w: new Float64Array(NB).fill(1), v: new Float64Array(NB), trials: [], scen: (M && M.scen) || 'classic', isi: (M && M.isi) || 250, last: null };
  }
  resetModel();

  function runTrial(us) {
    const ss = new Float64Array(NT), dcn = new Float64Array(NT), eye = new Float64Array(NT);
    let e = 0;
    for (let k = 0; k < NT; k++) {
      const t = k * DT;
      let drive = 0;
      for (let i = 0; i < NB; i++) drive += (M.w[i] - M.v[i]) * G[i][k];
      ss[k] = t >= CS ? Math.max(0, 80 + 60 * drive / S[k]) : 80;
      const ss0 = t >= CS ? 140 : 80;
      dcn[k] = Math.max(0, 40 + 0.9 * (ss0 - ss[k]));
      e += DT / 40 * (Math.max(0, dcn[k] - 48) - e);
      eye[k] = e;
    }
    const kUS = Math.round((CS + M.isi) / DT);
    return { ss, dcn, eye, kUS, us, cr: Math.min(1.1, eye[kUS] / EYE_FULL) };
  }
  function learn(us) {
    const sc = SCEN[M.scen];
    const kL = Math.round((CS + M.isi) / DT) - 6;   // eligibility peaks ~30 ms before the climbing-fiber signal
    for (let i = 0; i < NB; i++) {
      if (us) {
        if (sc.ltd) M.w[i] -= 0.25 * G[i][kL] * M.w[i];
        if (sc.other) M.v[i] += 0.15 * G[i][kL] * (0.75 - M.v[i]);
      } else if (sc.other) {
        M.v[i] -= 0.6 * GBAR[i] * M.v[i];
      }
      M.w[i] += 0.6 * GBAR[i] * (1 - M.w[i]);   // PF activity without CF → LTP
    }
  }
  function train(n, us) {
    for (let j = 0; j < n; j++) {
      const r = runTrial(us);
      M.trials.push({ cr: r.cr, us, scen: M.scen });
      learn(us);
    }
    M.last = runTrial(us);
    drawLab();
  }

  let labEls = {};
  function buildLab() {
    const scenSel = h('select', { onchange: (ev) => { M.scen = ev.target.value; drawLab(); } },
      Object.entries(SCEN).map(([k, v]) => h('option', { value: k }, v.label)));
    const isiOut = h('span', { class: 'small muted' }, M.isi + ' ms');
    const isi = h('input', { type: 'range', min: 150, max: 600, step: 25, value: M.isi, style: { width: '140px' },
      oninput: (ev) => { M.isi = +ev.target.value; isiOut.textContent = M.isi + ' ms'; M.last = runTrial(true); drawLab(); } });
    labEls = {
      scenSel, isi, isiOut,
      trace: h('canvas', { class: 'plot', style: { height: '170px' } }),
      weights: h('canvas', { class: 'plot', style: { height: '110px' } }),
      curve: h('canvas', { class: 'plot', style: { height: '120px' } }),
      status: h('div', { class: 'outcome' }),
      text: h('p', { class: 'small' }),
      refs: h('div', {}),
    };
    return h('div', { class: 'card' },
      h('h3', {}, 'Learning lab: eyeblink conditioning'),
      h('p', { class: 'small muted' }, 'A tone (CS) is followed by an air puff (US). Granule cells fire at a spread of delays after the tone; the puff drives a climbing fiber. A toy model of the circuit at left, after Marr–Albus–Ito theory.'),
      h('div', { class: 'row small' }, 'Model', scenSel),
      h('div', { class: 'row small', style: { marginTop: '6px' } }, 'Tone → puff interval', isi, isiOut),
      h('div', { class: 'row', style: { margin: '10px 0' } },
        h('button', { class: 'btn primary', onclick: () => train(1, true) }, 'Train ×1'),
        h('button', { class: 'btn', onclick: () => train(10, true) }, 'Train ×10'),
        h('button', { class: 'btn', onclick: () => train(10, false) }, 'Tone alone ×10'),
        h('button', { class: 'btn ghost', onclick: () => { resetModel(); M.last = runTrial(true); drawLab(); } }, 'Reset')),
      labEls.status,
      h('div', { class: 'tiny muted', style: { margin: '8px 0 2px' } }, 'Last trial: Purkinje simple spikes (pink), nuclear output (red), eyelid closure (blue)'), labEls.trace,
      h('div', { class: 'tiny muted', style: { margin: '8px 0 2px' } }, 'Parallel-fiber weights by granule-cell delay after the tone (gray: other plasticity site)'), labEls.weights,
      h('div', { class: 'tiny muted', style: { margin: '8px 0 2px' } }, 'Learning curve: conditioned response at puff time'), labEls.curve,
      labEls.text, labEls.refs);
  }

  function setupCanvas(c) {
    const r = c.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    c.width = Math.max(10, Math.round(r.width * dpr)); c.height = Math.max(10, Math.round(r.height * dpr));
    const ctx = c.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, r.width, r.height);
    ctx.font = '11px -apple-system, Segoe UI, sans-serif';
    return { ctx, w: r.width, h: r.height };
  }

  function drawLab() {
    if (!labEls.trace || !labEls.trace.isConnected) return;
    if (!M.last) M.last = runTrial(true);
    const sc = SCEN[M.scen];
    labEls.scenSel.value = M.scen;
    const r = M.last, n = M.trials.length;
    const crPct = Math.round(r.cr * 100);
    let peak = 0;
    for (let k = 0; k < NT; k++) if (r.eye[k] > r.eye[peak]) peak = k;
    labEls.status.textContent = `Trial ${n} · learned eyelid closure at puff time: ${crPct}%` + (crPct > 15 ? ` · peaks at ${peak * DT - CS} ms after tone (puff at ${M.isi} ms)` : '');
    labEls.status.style.borderLeftColor = crPct > 50 ? '#3fb950' : crPct > 15 ? '#e3b341' : '#6e7681';
    labEls.text.textContent = sc.text;
    CA.clear(labEls.refs).append(...CA.citeChips(sc.ref.concat(['marr1969', 'albus1971', 'giovannucci2017'])));

    // trial traces
    let { ctx, w, h: H } = setupCanvas(labEls.trace);
    const x = (t) => 30 + (w - 40) * t / T;
    ctx.fillStyle = 'rgba(227,179,65,.18)'; ctx.fillRect(x(CS), 0, x(T) - x(CS), H);
    ctx.fillStyle = '#e3b341'; ctx.fillText('tone', x(CS) + 4, 12);
    ctx.strokeStyle = '#ff7b72'; ctx.setLineDash([4, 3]); ctx.beginPath(); ctx.moveTo(x(CS + M.isi), 0); ctx.lineTo(x(CS + M.isi), H); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = '#ff7b72'; ctx.fillText('puff', x(CS + M.isi) + 4, 12);
    const line = (arr, color, scale, off) => {
      ctx.strokeStyle = color; ctx.lineWidth = 1.8; ctx.beginPath();
      for (let k = 0; k < NT; k++) { const yy = H - 8 - (arr[k] - off) * scale; k ? ctx.lineTo(x(k * DT), yy) : ctx.moveTo(x(k * DT), yy); }
      ctx.stroke();
    };
    const yScale = (H - 24) / 160;
    line(r.ss, '#f778ba', yScale, 0);
    line(r.dcn, '#ff5f57', yScale, 0);
    ctx.fillStyle = 'rgba(88,166,255,.35)'; ctx.strokeStyle = '#58a6ff';
    ctx.beginPath(); ctx.moveTo(x(0), H - 8);
    for (let k = 0; k < NT; k++) ctx.lineTo(x(k * DT), H - 8 - Math.min(1.2, r.eye[k] / EYE_FULL) * (H - 30));
    ctx.lineTo(x(T), H - 8); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#8b949e'; ctx.fillText('0', 18, H - 6); ctx.fillText(T + ' ms', w - 46, H - 12);

    // weights
    ({ ctx, w, h: H } = setupCanvas(labEls.weights));
    const bw = (w - 40) / NB;
    for (let i = 0; i < NB; i++) {
      const xx = 30 + i * bw;
      ctx.fillStyle = '#ffa657'; ctx.fillRect(xx, H - 10 - M.w[i] * (H - 22), Math.max(1, bw - 1), M.w[i] * (H - 22));
      if (M.v[i] > 0.01) { ctx.fillStyle = 'rgba(200,200,210,.75)'; ctx.fillRect(xx, H - 10 - M.v[i] * (H - 22), Math.max(1, bw - 1), 2.5); }
    }
    const xu = 30 + ((M.isi) / 16) * bw;
    ctx.strokeStyle = '#ff7b72'; ctx.setLineDash([4, 3]); ctx.beginPath(); ctx.moveTo(xu, 0); ctx.lineTo(xu, H); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = '#8b949e'; ctx.fillText('0 ms', 26, H - 1); ctx.fillText(Math.round((NB - 1) * 16) + ' ms', w - 50, H - 1);

    // learning curve
    ({ ctx, w, h: H } = setupCanvas(labEls.curve));
    const N = Math.max(20, n);
    ctx.strokeStyle = '#30363d'; ctx.beginPath(); ctx.moveTo(30, H - 12); ctx.lineTo(w - 8, H - 12); ctx.stroke();
    M.trials.forEach((tr, i) => {
      ctx.fillStyle = tr.us ? '#58a6ff' : '#e3b341';
      ctx.beginPath(); ctx.arc(30 + (w - 44) * (i + 0.5) / N, H - 12 - Math.min(1.1, tr.cr) * (H - 26), 2.6, 0, 7); ctx.fill();
    });
    ctx.fillStyle = '#8b949e'; ctx.fillText('100%', 0, 18); ctx.fillText('trials →', w - 52, H - 1);
    ctx.fillStyle = '#e3b341'; if (M.trials.some((t) => !t.us)) ctx.fillText('● tone alone', 40, 12);
  }

  // redraw canvases once the view is laid out
  const ro = new ResizeObserver(CA.debounce(() => drawLab(), 60));
  CA.on('view-mounted', (id) => { if (id === 'circuit') { M.last = runTrial(true); drawLab(); if (labEls.trace) ro.observe(labEls.trace); } });
})();
