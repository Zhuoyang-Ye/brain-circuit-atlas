/* Fruit fly Microcircuit: the mushroom body, the fly's centre for learned odour value, as an interactive schematic,
   with a toy model of odour conditioning (sparse Kenyon cell codes, APL feedback, dopamine-gated plasticity). */
(function () {
  'use strict';
  const CA = window.CA, h = CA.h, s = CA.s;
  let root, svg, caption, unsub = null, anims = [], stopped = false;

  CA.registerVariant('circuit', 'fly', { mount, unmount });

  const COL = CA.palette({ orn: '#56d4dd', pn: '#3fb950', kc: '#e3b341', apl: '#ff7b72', ppl1: '#f85149', pam: '#3fb9a5', mbon: '#d2a8ff',
    dpm: '#bc8cff', lh: '#ffa657', exc: '#3fb950', inh: '#ff7b72', g0: '#7ee787', g1: '#79c0ff', g2: '#ffa657', g3: '#d2a8ff', app: '#58a6ff', av: '#f0883e' });
  // compartments: name, lobe, position, which dopamine neurons innervate it (Aso et al., 2014a; schematic)
  const COMP = [
    { id: 'a3', name: 'α3', lobe: 'v', y0: 40, y1: 128, dan: 'ppl1' },
    { id: 'a2', name: 'α2', lobe: 'v', y0: 128, y1: 216, dan: 'ppl1' },
    { id: 'a1', name: 'α1', lobe: 'v', y0: 216, y1: 300, dan: 'pam' },
    { id: 'g1', name: 'γ1', lobe: 'h', x0: 566, x1: 628, dan: 'ppl1' },
    { id: 'g2', name: 'γ2', lobe: 'h', x0: 628, x1: 690, dan: 'ppl1' },
    { id: 'g3', name: 'γ3', lobe: 'h', x0: 690, x1: 752, dan: 'pam' },
    { id: 'g4', name: 'γ4', lobe: 'h', x0: 752, x1: 814, dan: 'pam' },
    { id: 'g5', name: 'γ5', lobe: 'h', x0: 814, x1: 876, dan: 'pam' },
  ];
  const VX0 = 516, VX1 = 566, HY0 = 300, HY1 = 352;   // vertical lobe x range, horizontal lobe y range
  const cc = (c) => (c.lobe === 'v' ? [VX1, (c.y0 + c.y1) / 2] : [(c.x0 + c.x1) / 2, HY1]);
  const NKC = 6;

  function mount(node) {
    root = node;
    stopped = false;
    svg = s('svg', { viewBox: '0 0 900 610', width: '100%', style: { display: 'block' }, role: 'img', 'aria-label': 'Schematic of the fly olfactory pathway and mushroom body' });
    drawCircuit();
    caption = h('div', { class: 'small muted', style: { minHeight: '2.6em', marginTop: '8px' } }, 'Hover or click any element. Play a signal to watch information flow.');
    const lab = buildLab();
    root.appendChild(h('div', { class: 'page', style: { maxWidth: '1400px' } },
      h('div', { class: 'page-head' }, h('div', {},
        h('h2', {}, 'The mushroom body microcircuit'),
        h('p', {}, 'Where a fly learns what an odour means. Projection neurons carry each odour from the antennal lobe to the lateral horn, for innate responses, and to about 2,000 Kenyon cells, which code it sparsely. Kenyon cell axons run through a row of compartments, each with its own dopamine neurons and output neurons; dopamine changes the Kenyon cells’ synapses onto the output neurons, and so what the odour makes the fly do.'))),
      h('div', { class: 'lab-grid' },
        h('div', {},
          h('div', { class: 'svgwrap', style: { padding: '6px' } }, svg),
          h('div', { class: 'row', style: { marginTop: '10px', flexWrap: 'wrap' } },
            h('button', { class: 'btn', onclick: () => playOdour() }, '▶ Odour'),
            h('button', { class: 'btn', onclick: () => playAPL() }, '▶ APL feedback'),
            h('button', { class: 'btn', onclick: () => playDA('ppl1') }, '▶ Punishment dopamine'),
            h('button', { class: 'btn', onclick: () => playDA('pam') }, '▶ Reward dopamine'),
            h('span', { class: 'grow' }),
            h('span', { class: 'row small muted' }, h('span', { class: 'dot', style: { background: COL.exc } }), 'excitatory', h('span', { class: 'dot', style: { background: COL.inh } }), 'inhibitory')),
          caption,
          h('p', { class: 'tiny muted', style: { marginTop: '6px' } }, 'Schematic, not to scale; compartments named as in Aso et al. (2014), with only the γ lobe drawn horizontally and the α lobe vertically. ',
            ...CA.citeChips(['aso2014a', 'claridgechang2009', 'liuc2012']))),
        lab)));
    unsub = CA.on('select', paintSel);
    paintSel();
    requestAnimationFrame(drawLab);
  }
  function unmount() { stopped = true; anims.forEach((a) => cancelAnimationFrame(a)); anims = []; if (unsub) unsub(); unsub = null; ro.disconnect(); }

  /* ------------------------------------------------------------------ schematic */
  function grp(entity, label, ...kids) {
    const g = s('g', { class: 'mc-el', 'data-entity': entity }, ...kids);
    g.addEventListener('mousemove', (ev) => CA.tip.show(`<b>${CA.esc(label)}</b><br><span class="muted">${CA.esc(CA.ent[entity] ? CA.ent[entity].name : '')}</span>`, ev));
    g.addEventListener('mouseleave', () => CA.tip.hide());
    g.addEventListener('click', () => CA.select(entity));
    return g;
  }
  const syn = (x, y, inh) => s('circle', { cx: x, cy: y, r: 3.6, fill: inh ? COL.inh : COL.exc, stroke: CA.tc('#0d1117'), 'stroke-width': 1 });
  const txt = (x, y, t, o) => s('text', Object.assign({ x, y, fill: CA.tc('#c9d1d9'), 'font-size': 12, 'pointer-events': 'none' }, o || {}), t);

  function drawCircuit() {
    svg.appendChild(s('defs', {}, s('marker', { id: 'fah', viewBox: '0 0 10 10', refX: 8, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse' },
      s('path', { d: 'M 0 0 L 10 5 L 0 10 z', fill: CA.tc('#8b949e') }))));
    // antennal lobe with four glomeruli, fed by receptor neurons from the antenna
    const glom = [[96, 462], [142, 500], [186, 452], [214, 500]];
    svg.appendChild(grp('fly-orn', 'Olfactory receptor neurons: neurons with the same receptor converge on one glomerulus',
      ...glom.map(([x, y], i) => s('path', { id: 'orn' + i, d: `M 8 ${430 + i * 38} C 40 ${430 + i * 38}, ${x - 40} ${y}, ${x - 14} ${y}`, stroke: COL['g' + i], 'stroke-width': 2, fill: 'none' })),
      txt(10, 418, 'from the antenna', { 'font-size': 11, fill: CA.tc('#8b949e') })));
    svg.appendChild(grp('fly-al', 'Antennal lobe: about 50 glomeruli, one per receptor type',
      s('ellipse', { cx: 155, cy: 478, rx: 98, ry: 60, fill: CA.tc('rgba(63,185,80,0.08)'), stroke: COL.pn, 'stroke-width': 1.5 }),
      ...glom.map(([x, y], i) => s('circle', { id: 'gl' + i, cx: x, cy: y, r: 16, fill: COL['g' + i], 'fill-opacity': 0.35, stroke: COL['g' + i] })),
      txt(155, 560, 'Antennal lobe', { 'text-anchor': 'middle' })));
    // projection neurons: from the glomeruli to the calyx and on to the lateral horn
    svg.appendChild(grp('fly-pn', 'Projection neurons: carry each glomerulus’s odour signal to the calyx and the lateral horn',
      s('path', { id: 'pnt', d: 'M 186 440 C 220 380, 250 300, 252 196', stroke: COL.pn, 'stroke-width': 2.6, fill: 'none' }),
      s('path', { id: 'pnca', d: 'M 252 196 C 262 160, 300 140, 318 128', stroke: COL.pn, 'stroke-width': 2.2, fill: 'none' }),
      s('path', { id: 'pnlh', d: 'M 252 196 C 236 150, 190 132, 160 124', stroke: COL.pn, 'stroke-width': 2.2, fill: 'none' }),
      syn(318, 128, false), syn(160, 124, false), txt(262, 300, 'projection', { 'font-size': 11 }), txt(262, 314, 'neurons', { 'font-size': 11 })));
    svg.appendChild(grp('fly-lh', 'Lateral horn: innate odour responses',
      s('ellipse', { cx: 108, cy: 116, rx: 66, ry: 40, fill: CA.tc('rgba(255,166,87,0.12)'), stroke: COL.lh, 'stroke-width': 1.5 }),
      txt(108, 120, 'Lateral horn', { 'text-anchor': 'middle' }),
      s('path', { id: 'lhout', d: 'M 64 90 C 44 70, 30 50, 24 26', stroke: COL.lh, 'stroke-width': 1.8, fill: 'none', 'marker-end': 'url(#fah)' }),
      txt(34, 20, 'innate behaviour', { 'font-size': 11, fill: CA.tc('#8b949e') })));
    // mushroom body: calyx, pedunculus, vertical (α) and horizontal (γ) lobes
    svg.appendChild(grp('fly-mb', 'Mushroom body: calyx, pedunculus and lobes',
      s('path', { d: `M 316 112 C 318 150, 400 150, 404 112 L 404 104 C 380 132, 340 132, 316 104 Z`, fill: CA.tc('rgba(227,179,65,0.16)'), stroke: COL.kc, 'stroke-width': 1.2 }),
      s('path', { d: `M 344 138 L 376 138 L ${VX1} ${HY0 + 6} L ${VX0 - 6} ${HY1} Z`, fill: CA.tc('rgba(227,179,65,0.08)'), stroke: CA.tc('#3d444d') }),
      s('rect', { x: VX0, y: 40, width: VX1 - VX0, height: HY1 - 40, rx: 12, fill: CA.tc('rgba(227,179,65,0.08)'), stroke: CA.tc('#3d444d') }),
      s('rect', { x: VX0, y: HY0, width: 876 - VX0, height: HY1 - HY0, rx: 12, fill: CA.tc('rgba(227,179,65,0.08)'), stroke: CA.tc('#3d444d') }),
      txt(318, 150, 'calyx', { 'font-size': 11, fill: CA.tc('#8b949e') }), txt(420, 238, 'pedunculus', { 'font-size': 11, fill: CA.tc('#8b949e'), transform: 'rotate(52 420 238)' })));
    COMP.forEach((c) => {
      const r = c.lobe === 'v' ? { x: VX0 + 2, y: c.y0 + 2, width: VX1 - VX0 - 4, height: c.y1 - c.y0 - 4 } : { x: c.x0 + 2, y: HY0 + 2, width: c.x1 - c.x0 - 4, height: HY1 - HY0 - 4 };
      svg.appendChild(s('rect', Object.assign({ id: 'comp-' + c.id, rx: 8, fill: COL[c.dan], 'fill-opacity': 0.13, stroke: COL[c.dan], 'stroke-opacity': 0.5, 'pointer-events': 'none' }, r)));
      svg.appendChild(c.lobe === 'v' ? txt(VX0 - 8, (c.y0 + c.y1) / 2 + 4, c.name, { 'text-anchor': 'end', 'font-size': 11 }) : txt((c.x0 + c.x1) / 2, HY0 - 6, c.name, { 'text-anchor': 'middle', 'font-size': 11 }));
    });
    // Kenyon cells: somata above the calyx, dendrites in it, axons through the pedunculus into both lobes
    const kcx = (k) => 326 + k * 13;
    const kcs = grp('fly-kc', 'Kenyon cells: each samples a few random glomeruli and fires sparsely');
    for (let k = 0; k < NKC; k++) {
      const off = (k - (NKC - 1) / 2) * 5;
      kcs.append(
        s('circle', { id: 'kcs' + k, cx: kcx(k), cy: 66, r: 6, fill: COL.kc }),
        s('path', { id: 'kcd' + k, d: `M ${kcx(k)} 72 L ${kcx(k)} 116`, stroke: COL.kc, 'stroke-width': 1.3, fill: 'none' }),
        s('path', { id: 'kcp' + k, d: `M ${360 + off} 138 L ${541 + off} ${326 + off * 0.2}`, stroke: COL.kc, 'stroke-width': 1.2, fill: 'none', opacity: 0.8 }),
        s('path', { id: 'kch' + k, d: `M ${541 + off} ${326 + off * 0.2} L 872 ${326 + off}`, stroke: COL.kc, 'stroke-width': 1.2, fill: 'none', opacity: 0.8 }),
        s('path', { id: 'kcv' + k, d: `M ${541 + off} ${326 + off * 0.2} L ${541 + off} 46`, stroke: COL.kc, 'stroke-width': 1.2, fill: 'none', opacity: 0.8 }));
    }
    kcs.appendChild(txt(392, 52, 'Kenyon cells', { 'font-size': 11.5 }));
    svg.appendChild(kcs);
    // APL: one GABAergic neuron, driven by the Kenyon cells and inhibiting them
    svg.appendChild(grp('fly-apl', 'APL neuron (GABA): Kenyon cells excite it and it inhibits them, keeping the odour code sparse',
      s('path', { id: 'aplin', d: `M ${VX0 - 4} 290 C 470 270, 452 238, 446 214`, stroke: COL.apl, 'stroke-width': 1.6, fill: 'none', 'stroke-dasharray': '5 3' }),
      s('path', { id: 'aplout', d: 'M 446 204 C 440 160, 420 128, 404 118', stroke: COL.apl, 'stroke-width': 1.6, fill: 'none', 'stroke-dasharray': '5 3' }),
      s('circle', { cx: 446, cy: 208, r: 8, fill: COL.apl }), syn(404, 118, true), txt(458, 204, 'APL', { 'font-size': 11.5 })));
    // DPM: serotonin and Amnesiac onto the lobes
    svg.appendChild(grp('fly-dpm', 'DPM neurons: release the Amnesiac neuropeptide and serotonin onto the lobes, for memory',
      s('path', { d: `M 470 410 C 500 390, 530 370, 548 ${HY1 + 4} M 470 410 C 600 400, 700 380, 760 ${HY1 + 4}`, stroke: COL.dpm, 'stroke-width': 1.3, fill: 'none', 'stroke-dasharray': '2 3' }),
      s('circle', { cx: 466, cy: 414, r: 7, fill: COL.dpm }), txt(452, 436, 'DPM', { 'font-size': 11 })));
    // dopamine neurons: PPL1 (punishment) above, PAM (reward) below
    const dan = (key, sx, sy, label, sub, left) => {
      const comps = COMP.filter((c) => c.dan === key);
      return grp('fly-dan', label,
        ...comps.map((c) => { const [x, y] = cc(c); return s('path', { id: `da-${c.id}`, d: `M ${sx} ${sy} C ${(sx + x) / 2 + 30} ${sy}, ${x + 12} ${(sy + y) / 2}, ${x + (c.lobe === 'v' ? -2 : 0)} ${c.lobe === 'v' ? y : y - 6}`, stroke: COL[key], 'stroke-width': 1.6, fill: 'none' }); }),
        s('circle', { cx: sx, cy: sy, r: 9, fill: COL[key] }),
        txt(left ? sx - 14 : sx + 14, sy + 4, sub, { 'font-size': 11.5, fill: COL[key], 'text-anchor': left ? 'end' : 'start' }));
    };
    svg.appendChild(dan('ppl1', 640, 64, 'PPL1 dopamine neurons: signal punishment to the vertical lobe and the heel', 'PPL1 dopamine (punishment)'));
    svg.appendChild(dan('pam', 600, 470, 'PAM dopamine neurons: signal sugar reward, mainly to the horizontal lobes', 'PAM dopamine (reward)', true));
    // output neurons: one per compartment, pooled here by the behaviour their activation biases
    const box = (x, y, label, key) => [s('rect', { x, y, width: 168, height: 40, rx: 8, fill: COL[key], 'fill-opacity': 0.14, stroke: COL[key] }),
      txt(x + 84, y + 17, 'output neurons', { 'text-anchor': 'middle', 'font-size': 11 }), txt(x + 84, y + 32, label, { 'text-anchor': 'middle', 'font-size': 12.5, fill: COL[key], 'font-weight': 600 })];
    svg.appendChild(grp('fly-mbon', 'Mushroom body output neurons: their balance biases approach or avoidance',
      ...COMP.map((c) => {
        const [x, y] = c.lobe === 'v' ? [VX1, (c.y0 + c.y1) / 2] : [(c.x0 + c.x1) / 2, HY0 + 4];
        const toApp = c.dan === 'ppl1';
        const tx = 700, ty = toApp ? 168 : 548;
        const d = c.lobe === 'v' ? `M ${x} ${y} C ${x + 60} ${y}, ${tx - 40} ${ty}, ${tx} ${ty}` : (toApp ? `M ${x} ${y} C ${x} ${y - 60}, ${tx - 40} ${ty + 30}, ${tx} ${ty}` : `M ${x} ${HY1} C ${x} ${HY1 + 70}, ${tx - 30} ${ty - 10}, ${tx} ${ty}`);
        return s('path', { id: 'mb-' + c.id, d, stroke: COL.mbon, 'stroke-width': 1.3, fill: 'none', opacity: 0.85 });
      }),
      ...box(700, 148, '→ approach', 'app'), ...box(700, 528, '→ avoid', 'av'),
      s('path', { d: 'M 868 168 L 892 168 M 868 548 L 892 548', stroke: CA.tc('#8b949e'), 'stroke-width': 1.5, 'marker-end': 'url(#fah)' })));
    svg.appendChild(txt(890, 596, 'to descending neurons and behaviour →', { 'font-size': 10.5, fill: CA.tc('#8b949e'), 'text-anchor': 'end' }));
    svg.appendChild(s('g', { id: 'fpulses' }));
  }

  function paintSel() {
    if (svg) svg.querySelectorAll('.mc-el').forEach((g) => g.classList.toggle('sel', g.dataset.entity === CA.selected));
  }

  /* ------------------------------------------------------------------ animations */
  function pulseAlong(id, color, ms, reverse) {
    return new Promise((resolve) => {
      const path = svg.querySelector('#' + id);
      if (!path || stopped) return resolve();
      const len = path.getTotalLength();
      const dot = s('circle', { r: 5, fill: color, stroke: CA.tc('#fff'), 'stroke-width': 1.2 });
      svg.querySelector('#fpulses').appendChild(dot);
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
  function flash(id, attr, value, ms) {
    const el = svg.querySelector('#' + id);
    if (!el) return Promise.resolve();
    const old = el.getAttribute(attr);
    el.setAttribute(attr, value);
    return new Promise((r) => setTimeout(() => { if (el.isConnected) el.setAttribute(attr, old); r(); }, ms));
  }
  const say = (t) => { caption.textContent = t; };
  const ACTIVE = [1, 4];   // the two Kenyon cells this odour excites in the animation: a sparse code

  async function playOdour() {
    say('An odour activates receptor neurons; those with the same receptor converge on one glomerulus of the antennal lobe.');
    await Promise.all([0, 2].map((i) => pulseAlong('orn' + i, COL['g' + i], 800)));
    say('Projection neurons carry the odour to the lateral horn, for innate responses, and to the calyx of the mushroom body.');
    await pulseAlong('pnt', COL.pn, 700);
    await Promise.all([pulseAlong('pnca', COL.pn, 500), pulseAlong('pnlh', COL.pn, 500)]);
    say('Each Kenyon cell samples a few glomeruli at random and needs several inputs to fire, so only a few percent respond to any odour: a sparse code.');
    await Promise.all(ACTIVE.map((k) => flash('kcs' + k, 'r', 10, 500)));
    await Promise.all(ACTIVE.map((k) => pulseAlong('kcp' + k, COL.kc, 700)));
    await Promise.all(ACTIVE.flatMap((k) => [pulseAlong('kch' + k, COL.kc, 1100), pulseAlong('kcv' + k, COL.kc, 900)]));
    say('In every compartment they pass, the active Kenyon cells excite that compartment’s output neurons, whose balance pushes the fly toward approach or avoidance.');
    await Promise.all(COMP.map((c) => pulseAlong('mb-' + c.id, COL.mbon, 900)));
  }
  async function playAPL() {
    say('Kenyon cells excite the single APL neuron in each hemisphere…');
    await Promise.all(ACTIVE.map((k) => pulseAlong('kcp' + k, COL.kc, 600)));
    await pulseAlong('aplin', COL.apl, 600);
    say('…which inhibits them back in the calyx. This feedback keeps the odour code sparse and decorrelated, which flies need to tell similar odours apart (Lin et al., 2014).');
    await pulseAlong('aplout', COL.inh, 600);
    await Promise.all([0, 1, 2, 3, 4, 5].map((k) => flash('kcd' + k, 'stroke', COL.inh, 500)));
  }
  async function playDA(key) {
    const comps = COMP.filter((c) => c.dan === key);
    say(key === 'ppl1'
      ? 'A shock activates PPL1 dopamine neurons, which reach the vertical lobe and the heel; activating them is enough to write an aversive memory (Claridge-Chang et al., 2009).'
      : 'Sugar activates PAM dopamine neurons, which reach mainly the horizontal lobes and signal reward (Liu et al., 2012).');
    await Promise.all(comps.map((c) => pulseAlong('da-' + c.id, COL[key], 900)));
    await Promise.all(comps.map((c) => flash('comp-' + c.id, 'fill-opacity', 0.45, 900)));
    say('In those compartments only, dopamine depresses the synapses of the Kenyon cells that were active just before it, so the trained odour now drives those output neurons less (Hige et al., 2015). The balance of outputs tilts, and the fly avoids or approaches the odour.');
  }

  /* ------------------------------------------------------------------ learning lab (toy model) */
  // A toy model: 40 glomeruli, 400 Kenyon cells each summing 7 random glomeruli, APL feedback as a cap on the fraction
  // of Kenyon cells that fire, and two pools of output neurons (approach, avoid) reading all Kenyon cells.
  const NG = 40, K = 400, IN = 7, BETA = 5;
  function mulberry32(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const rng = mulberry32(20240607);
  const gauss = () => { let u = 0; while (!u) u = rng(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rng()); };
  const KCIN = Array.from({ length: K }, () => Array.from({ length: IN }, () => Math.floor(rng() * NG)));
  const BASE = Array.from({ length: NG }, gauss), INDEP = Array.from({ length: NG }, gauss);
  const FLIES = {
    wt: { label: 'Wild type', frac: 0.06, eta: 0.35, fwd: 'dep', refs: ['quinn1974', 'tully1985', 'hige2015', 'aso2014b', 'owald2015'],
      text: 'Kenyon cells code each odour sparsely. Dopamine that follows the odour depresses the active Kenyon cells’ synapses onto the output neurons of its compartments (Hige et al., 2015), shifting the balance of the output network (Aso et al., 2014b). In this toy, shock dopamine depresses the approach pool and sugar dopamine the avoid pool; activating the M4/6 outputs, in reward-dopamine compartments, does make flies avoid (Owald et al., 2015).' },
    apl: { label: 'APL silenced', frac: 0.3, eta: 0.35, fwd: 'dep', refs: ['linac2014', 'liux2009', 'hige2015'],
      text: 'Without APL feedback, many more Kenyon cells respond and two odours share more of them, so a memory of one spreads to the other. Flies with a disrupted Kenyon cell–APL loop fail to discriminate similar odours but still learn dissimilar ones (Lin et al., 2014); compare wild type and APL-silenced flies at a similarity of 70–80%. This toy silences APL completely; partly reducing its GABA instead enhanced learning (Liu & Davis, 2009).' },
    dopr1: { label: 'DopR1 (dDA1) mutant', frac: 0.06, eta: 0.35, fwd: 'weak', refs: ['kimyc2007', 'handler2019'],
      text: 'dDA1 mutants barely learn with shock and learn less with sugar, and dDA1 in the mushroom body rescues them (Kim et al., 2007). Handler et al. (2019) found that without DopR1, odour-then-dopamine pairing no longer depresses Kenyon cell output and gives weak potentiation instead, which this toy copies; potentiation through DopR2 is spared.' },
    rut: { label: 'rutabaga mutant', frac: 0.06, eta: 0.12, fwd: 'dep', refs: ['livingstone1984', 'tomchik2009', 'zars2000', 'tully1985'],
      text: 'The rutabaga adenylyl cyclase, stimulated by calcium/calmodulin (Livingstone et al., 1984), makes cAMP when dopamine follows Kenyon cell activity (Tomchik & Davis, 2009), and it is needed only in Kenyon cells (Zars et al., 2000). rutabaga flies learn partly and forget within 30 minutes (Tully & Quinn, 1985); here, plasticity is weaker.' },
  };
  let M;
  function newFlies(keep) {
    const prev = M || {};
    M = { fly: prev.fly || 'wt', us: prev.us || 'shock', timing: prev.timing || 'fwd', sim: prev.sim != null ? prev.sim : 0.5, trials: [], app: new Float64Array(K).fill(1), av: new Float64Array(K).fill(1) };
    if (keep) Object.assign(M, keep);
    code();
  }
  function code() {
    const sim = M.sim;
    const A = BASE.map((x) => Math.max(0, x));
    const B = BASE.map((x, g) => Math.max(0, sim * x + Math.sqrt(1 - sim * sim) * INDEP[g]));
    const kc = (pn) => {
      const inp = KCIN.map((ins) => ins.reduce((a, g) => a + pn[g], 0));
      const th = inp.slice().sort((a, b) => b - a)[Math.round(K * FLIES[M.fly].frac) - 1];
      return inp.map((v) => (v >= th && v > 0 ? 1 : 0));
    };
    M.kcA = kc(A); M.kcB = kc(B);
  }
  const drive = (kcs, w) => { let n = 0, s0 = 0; kcs.forEach((a, k) => { if (a) { n++; s0 += w[k]; } }); return n ? s0 / n : 0; };
  function test() {
    const vA = drive(M.kcA, M.app) - drive(M.kcA, M.av), vB = drive(M.kcB, M.app) - drive(M.kcB, M.av);
    const pA = 1 / (1 + Math.exp(-BETA * (vA - vB)));   // chance of choosing odour A (the trained odour) in the T-maze
    return M.us === 'shock' ? 1 - 2 * pA : 2 * pA - 1;    // performance index: avoid the shock odour, approach the sugar odour
  }
  function trainOnce() {
    const f = FLIES[M.fly], w = M.us === 'shock' ? M.app : M.av;
    M.kcA.forEach((a, k) => {
      if (!a) return;
      if (M.timing === 'fwd') {
        if (f.fwd === 'dep') w[k] *= 1 - f.eta;                  // odour, then dopamine: depression (DopR1, cAMP)
        else w[k] += 0.04 * (1.15 - w[k]);                        // DopR1 mutant: weak potentiation instead
      } else {
        w[k] += 0.3 * (1.15 - w[k]);                              // dopamine, then odour: potentiation (DopR2)
      }
    });
    M.trials.push({ pi: test(), us: M.us, timing: M.timing });
  }
  function train(n) { for (let i = 0; i < n; i++) trainOnce(); drawLab(); }

  let L = {};
  function buildLab() {
    newFlies();
    const seg = (opts, key, onchange) => {
      const el = h('div', { class: 'seg', role: 'group' }, opts.map(([v, l]) => h('button', { class: M[key] === v ? 'on' : '', 'aria-pressed': String(M[key] === v), 'data-v': v,
        onclick: () => { M[key] = v; el.querySelectorAll('button').forEach((b) => { const on = b.dataset.v === v; b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on)); }); onchange(); } }, l)));
      return el;
    };
    const flySel = h('select', { 'aria-label': 'Genotype', onchange: (ev) => { newFlies({ fly: ev.target.value }); drawLab(); } },
      Object.entries(FLIES).map(([k, v]) => h('option', { value: k }, v.label)));
    const simOut = h('span', { class: 'small muted' }, Math.round(M.sim * 100) + '%');
    const sim = h('input', { type: 'range', min: 0, max: 0.95, step: 0.05, value: M.sim, style: { width: '120px' }, 'aria-label': 'How similar the two odours are',
      oninput: (ev) => { simOut.textContent = Math.round(+ev.target.value * 100) + '%'; newFlies({ sim: +ev.target.value }); drawLab(); } });
    L = {
      flySel,
      pattern: h('canvas', { class: 'plot', style: { height: '150px' } }),
      drive: h('canvas', { class: 'plot', style: { height: '96px' } }),
      curve: h('canvas', { class: 'plot', style: { height: '120px' } }),
      status: h('div', { class: 'outcome' }),
      text: h('p', { class: 'small' }), refs: h('div', {}), stats: h('div', { class: 'tiny muted', style: { margin: '6px 0 2px' } }),
    };
    return h('div', { class: 'card' },
      h('h3', {}, 'Learning lab: odour conditioning'),
      h('p', { class: 'small muted' }, 'Flies smell odour A with a shock or sugar and odour B alone, then choose between them in a T-maze (Quinn et al., 1974; Tully & Quinn, 1985). A toy model of the circuit at left: 400 Kenyon cells, two pools of output neurons, and dopamine-gated plasticity.'),
      h('div', { class: 'row small' }, 'Fly', flySel),
      h('div', { class: 'row small', style: { marginTop: '6px' } }, 'Reinforcer', seg([['shock', 'Shock (PPL1)'], ['sugar', 'Sugar (PAM)']], 'us', () => drawLab())),
      h('div', { class: 'row small', style: { marginTop: '6px' } }, 'Timing', seg([['fwd', 'Odour, then dopamine'], ['bwd', 'Dopamine, then odour']], 'timing', () => drawLab())),
      h('div', { class: 'row small', style: { marginTop: '6px' } }, 'Odour similarity', sim, simOut),
      h('div', { class: 'row', style: { margin: '10px 0' } },
        h('button', { class: 'btn primary', onclick: () => train(1) }, 'Train ×1'),
        h('button', { class: 'btn', onclick: () => train(5) }, 'Train ×5'),
        h('button', { class: 'btn ghost', onclick: () => { newFlies({ trials: [] }); drawLab(); } }, 'New flies')),
      L.status,
      h('div', { class: 'tiny muted', style: { margin: '8px 0 2px' } }, `Kenyon cells responding to odour A (amber), odour B (blue) and both (${CA.theme === 'light' ? 'black' : 'white'}); 400 cells`), L.pattern, L.stats,
      h('div', { class: 'tiny muted', style: { margin: '8px 0 2px' } }, 'How strongly each odour drives the two output pools (1 = untrained)'), L.drive,
      h('div', { class: 'tiny muted', style: { margin: '8px 0 2px' } }, 'Learning curve: performance index after each training trial'), L.curve,
      L.text, L.refs);
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
    if (!L.pattern || !L.pattern.isConnected) return;
    const f = FLIES[M.fly], n = M.trials.length;
    L.flySel.value = M.fly;
    const pi = n ? M.trials[n - 1].pi : 0;
    const pct = Math.round(pi * 100);
    const what = M.us === 'shock' ? 'avoiding the shock-paired odour' : 'approaching the sugar-paired odour';
    L.status.textContent = n ? `Trial ${n} · performance index ${pct}% (${pct >= 0 ? what : 'the opposite of ' + what})` : 'Untrained: the flies split evenly between the odours (index 0%)';
    L.status.style.borderLeftColor = pct > 50 ? CA.tc('#3fb950') : pct > 15 ? CA.tc('#e3b341') : pct < -15 ? CA.tc('#ff7b72') : CA.tc('#6e7681');
    const timingText = M.timing === 'bwd' ? ' Dopamine before the odour potentiates instead, through DopR2, and can undo a memory written by forward pairing (Handler et al., 2019); in the classic shock assay, shock before the odour produced no learning (Tully & Quinn, 1985).' : '';
    L.text.textContent = f.text + timingText;
    CA.clear(L.refs).append(...CA.citeChips(f.refs.concat(M.timing === 'bwd' ? ['handler2019', 'tully1985'] : []).filter((k, i, a) => a.indexOf(k) === i)));

    // Kenyon cell patterns: a 20 x 20 grid per odour
    let { ctx, w, h: H } = setupCanvas(L.pattern);
    const cell = Math.min((w - 50) / 40, (H - 20) / 20), gw = cell * 20, gap = Math.min(60, w - 20 - 2 * gw);
    const ox = [(w - 2 * gw - gap) / 2, (w + gap) / 2], cA = CA.tc('#e3b341'), cB = CA.tc('#58a6ff'), both = CA.tc('#e6edf3'), off = CA.tc('#30363d');
    [M.kcA, M.kcB].forEach((pat, o) => {
      for (let k = 0; k < K; k++) {
        const x = ox[o] + (k % 20) * cell, y = 14 + Math.floor(k / 20) * cell;
        const a = pat[k], other = (o ? M.kcA : M.kcB)[k];
        ctx.fillStyle = a ? (other ? both : o ? cB : cA) : off;
        ctx.fillRect(x + 0.5, y + 0.5, cell - 1, cell - 1);
      }
      ctx.fillStyle = CA.tc('#8b949e'); ctx.fillText(o ? 'odour B' : 'odour A (trained)', ox[o], 10);
    });
    const nA = M.kcA.reduce((a, b) => a + b, 0), nB = M.kcB.reduce((a, b) => a + b, 0), nAB = M.kcA.reduce((a, v, k) => a + (v && M.kcB[k] ? 1 : 0), 0);
    L.stats.textContent = `Responding: ${Math.round(100 * nA / K)}% of Kenyon cells to A, ${Math.round(100 * nB / K)}% to B; ${Math.round(100 * nAB / Math.max(1, nA))}% of A’s cells also respond to B.`;

    // output drive bars
    ({ ctx, w, h: H } = setupCanvas(L.drive));
    const rows = [['A', M.kcA], ['B', M.kcB]];
    const bw = (w - 110) / 1.3;
    rows.forEach(([name, pat], r) => {
      [['approach', M.app, CA.tc('#58a6ff')], ['avoid', M.av, CA.tc('#f0883e')]].forEach(([lab, wts, col], j) => {
        const y = 8 + r * 44 + j * 18, v = drive(pat, wts);
        ctx.fillStyle = CA.tc('#8b949e'); ctx.fillText(`${name} → ${lab}`, 4, y + 11);
        ctx.fillStyle = col; ctx.fillRect(96, y, Math.max(1, v * bw), 13);
        ctx.fillStyle = CA.tc('#c9d1d9'); ctx.fillText(v.toFixed(2), 100 + v * bw, y + 11);
      });
    });
    ctx.strokeStyle = CA.tc('#8b949e'); ctx.setLineDash([3, 3]); ctx.beginPath(); ctx.moveTo(96 + bw, 2); ctx.lineTo(96 + bw, H - 2); ctx.stroke(); ctx.setLineDash([]);

    // learning curve
    ({ ctx, w, h: H } = setupCanvas(L.curve));
    const N = Math.max(15, n), top = 22, bot = H - 14, y0 = (top + bot) / 2, yy = (pi) => y0 - pi * (bot - top) / 2;
    ctx.strokeStyle = CA.tc('#30363d');
    [1, 0, -1].forEach((v) => { ctx.beginPath(); ctx.moveTo(40, yy(v)); ctx.lineTo(w - 8, yy(v)); ctx.stroke(); });
    ctx.fillStyle = CA.tc('#8b949e'); ctx.fillText('100%', 4, yy(1) + 4); ctx.fillText('0', 26, y0 + 4); ctx.fillText('−100%', 0, yy(-1) + 4); ctx.fillText('trials →', w - 52, H - 2);
    M.trials.forEach((tr, i) => {
      ctx.fillStyle = tr.timing === 'bwd' ? CA.tc('#d2a8ff') : tr.us === 'shock' ? CA.tc('#f85149') : CA.tc('#3fb9a5');
      ctx.beginPath(); ctx.arc(40 + (w - 52) * (i + 0.5) / N, yy(tr.pi), 3, 0, 7); ctx.fill();
    });
    ctx.font = '10px -apple-system, Segoe UI, sans-serif';
    [['shock', CA.tc('#f85149')], ['sugar', CA.tc('#3fb9a5')], ['dopamine first', CA.tc('#d2a8ff')]].forEach(([l, c], i) => { ctx.fillStyle = c; ctx.fillText('● ' + l, 44 + i * 64, 11); });
  }

  const ro = new ResizeObserver(CA.debounce(() => drawLab(), 60));
  CA.on('view-mounted', (id) => { if (id === 'circuit' && L.pattern && L.pattern.isConnected) { drawLab(); ro.observe(L.pattern); } });
})();
