/* Fruit fly Functional map: resting-state functional connectivity of the central brain beside its wiring, from the
   data of Turner, Mann & Clandinin (2021), recomputed by tools/build_fly_fc.py. A frontal network map, the two
   matrices, their correlation and the regions whose activity departs most from their wiring. */
(function () {
  'use strict';
  const CA = window.CA, D = CA.D, h = CA.h, s = CA.s;
  const C = (D.connectivity || {}).fly, CFG = ((D.regionViews || {}).fly || {}).map;
  if (!C || !CFG) return;

  const N = C.regions.length;
  const idx = Object.fromEntries(C.regions.map((r, i) => [r, i]));
  const groupOf = {};
  CFG.groups.forEach((g) => g.regions.forEach((r) => { groupOf[r] = g; }));
  const ORDER = CFG.groups.flatMap((g) => g.regions).map((r) => idx[r]);   // matrix order: by super-region
  const info = (i) => CFG.regions[C.regions[i]] || { name: C.regions[i], abbr: C.regions[i], entities: [] };
  const abbr = (i) => info(i).abbr;
  const fc = (i, j) => (i === j ? null : C.fc[i][j]);
  const scSym = (i, j) => (C.sc[i][j] + C.sc[j][i]) / 2;
  const diffSym = (i, j) => (C.diff[i][j] + C.diff[j][i]) / 2;
  const signed = (x) => (x >= 0 ? '+' : '−') + Math.abs(x).toFixed(2);

  // pairs and their weight in each layer
  const PAIRS = [];
  for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) PAIRS.push([i, j]);
  const LAYERS = {
    fc: { label: 'Activity', long: 'Functional connectivity (activity)', w: (i, j) => fc(i, j), unit: (v) => `z = ${v.toFixed(2)}` },
    sc: { label: 'Wiring', long: 'Structural connectivity (wiring)', w: (i, j) => Math.log10(Math.max(1, scSym(i, j))), unit: (v) => `${Math.round(10 ** v).toLocaleString()} cells` },
    diff: { label: 'Activity − wiring', long: 'Activity minus wiring', w: (i, j) => diffSym(i, j), unit: (v) => signed(v) + ' (z)', abs: true },
  };

  // functions tied to each region through the atlas's evidence-graded links (region entity → cognitive entity)
  const FUNCS = {};
  const regionFuncs = C.regions.map((r, i) => {
    const out = {};
    info(i).entities.forEach((e) => (CA.out[e] || []).forEach((l) => {
      const t = CA.ent[l.t];
      if (t && t.level === 'cognitive' && l.regions.includes('fly')) { (out[l.t] = out[l.t] || []).push(l); FUNCS[l.t] = (FUNCS[l.t] || 0) + 1; }
    }));
    return out;
  });

  // node positions: atlas centroids (frontal view, um), pushed apart just enough to keep labels legible
  const POS = C.geometry.map((g) => g.c.slice());
  (function relax() {
    const dmin = 25;
    for (let it = 0; it < 240; it++) {
      for (let a = 0; a < N; a++) for (let b = a + 1; b < N; b++) {
        const dx = POS[b][0] - POS[a][0], dy = POS[b][1] - POS[a][1], d = Math.hypot(dx, dy) || 0.01;
        if (d < dmin) { const k = (dmin - d) / d / 2; POS[a][0] -= dx * k; POS[a][1] -= dy * k; POS[b][0] += dx * k; POS[b][1] += dy * k; }
      }
      POS.forEach((p, i) => { p[0] += (C.geometry[i].c[0] - p[0]) * 0.04; p[1] += (C.geometry[i].c[1] - p[1]) * 0.04; });
    }
  })();
  // frame the regions and the brain's dorsal edge; the outline's lower part (outside the imaged regions) is cut off
  const allPts = C.brain.concat(POS);
  const BX0 = Math.min(...allPts.map((p) => p[0])) - 10, BX1 = Math.max(...allPts.map((p) => p[0])) + 10;
  const BY0 = Math.min(...allPts.map((p) => p[1])) - 22, BY1 = Math.max(...POS.map((p) => p[1])) + 26;
  const poly = (pts) => 'M' + pts.map((p) => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('L') + 'Z';

  // colour ramps (perceptual, readable on both themes)
  const SEQ = ['#00204c', '#2c3e6b', '#575d6d', '#7c7b78', '#a59c74', '#d3c064', '#ffe945'];
  const DIV = ['#2166ac', '#67a9cf', '#d1e5f0', '#f7f7f7', '#fddbc7', '#ef8a62', '#b2182b'];
  const ramp = (stops, t) => {
    t = CA.clamp(t, 0, 1) * (stops.length - 1);
    const k = Math.min(stops.length - 2, Math.floor(t)), f = t - k;
    const a = stops[k].match(/\w\w/g).map((x) => parseInt(x, 16)), b = stops[k + 1].match(/\w\w/g).map((x) => parseInt(x, 16));
    return '#' + a.map((v, n) => Math.round(v + (b[n] - v) * f).toString(16).padStart(2, '0')).join('');
  };
  const fcVals = PAIRS.map(([i, j]) => fc(i, j));
  const FC_MIN = Math.min(...fcVals), FC_MAX = Math.max(...fcVals);
  const SC_MAX = Math.log10(Math.max(...C.sc.flat()));
  const DIFF_MAX = Math.max(...C.diff.flat().map(Math.abs));
  const DR_MAX = Math.max(...C.diffRegion.map(Math.abs));

  let root, mapSvg, edgeG, nodeG, outlineG, card, ctl, unsub = null;
  let layer = CA.store.get('flymap.layer', 'fc'), colorBy = CA.store.get('flymap.color', 'group'), top = CA.store.get('flymap.top', 8);
  let func = null, sel = null;
  if (!LAYERS[layer]) layer = 'fc';

  CA.registerVariant('map', 'fly', { mount, unmount });

  function mount(node) {
    root = node;
    sel = null;
    card = h('div', {});
    ctl = h('div', {});
    mapSvg = s('svg', { viewBox: `${BX0} ${BY0} ${BX1 - BX0} ${BY1 - BY0}`, width: '100%', class: 'flymap', role: 'img', 'aria-label': 'Frontal map of fly central brain regions and their connections' });
    drawMap();
    root.appendChild(h('div', { class: 'page' },
      h('div', { class: 'page-head' }, h('div', {}, h('h2', {}, CFG.title), h('p', {}, CFG.intro))),
      h('div', { class: 'cols fm-cols' },
        h('div', {}, h('div', { class: 'card' }, ctl), h('div', { class: 'card' }, card)),
        h('div', { class: 'svgwrap', style: { padding: '6px' } }, mapSvg)),
      h('h3', { style: { marginTop: '26px' } }, 'Activity and wiring, region by region'),
      h('p', { class: 'small muted', style: { maxWidth: '920px' } }, 'Rows and columns are the 37 regions, grouped by super-region as in Turner et al. (Fig. 2D, E). Hover over a cell for its values; click one to select its row’s region.'),
      h('div', { class: 'grid2' },
        h('div', { class: 'card' }, h('h4', { style: { marginTop: 0 } }, 'Functional connectivity'),
          h('div', { class: 'tiny muted' }, `Resting-state calcium imaging · correlation of region activity (Fisher z), mean of ${C.flies} flies`), matrix('fc')),
        h('div', { class: 'card' }, h('h4', { style: { marginTop: 0 } }, 'Structural connectivity'),
          h('div', { class: 'tiny muted' }, 'Hemibrain EM connectome · neurons with input in the row region and output in the column region (log scale)'), matrix('sc'))),
      h('h3', { style: { marginTop: '26px' } }, 'How well wiring predicts activity'),
      h('div', { class: 'grid2' },
        h('div', { class: 'card' }, h('h4', { style: { marginTop: 0 } }, 'Every pair of regions'), scatterPlot()),
        h('div', { class: 'card' }, h('h4', { style: { marginTop: 0 } }, 'Regions whose activity departs from their wiring'), diffChart())),
      h('p', { class: 'small muted', style: { marginTop: '14px', maxWidth: '1000px' } }, CFG.note, ' ', CA.citeChips(CFG.refs)),
      h('p', { class: 'small muted', style: { maxWidth: '1000px' } }, 'Data: ', C.source, '. ',
        (CFG.links || []).map((l, k) => [k ? ' · ' : 'Explore further: ', h('a', { href: l.href, target: '_blank', rel: 'noopener' }, l.label + ' ↗')]))));
    renderControls();
    paint();
    renderCard();
    unsub = CA.on('select', paintSelected);
  }
  function unmount() { if (unsub) unsub(); unsub = null; CA.tip.hide(); }

  /* ------------------------------------------------------------------ the frontal map */
  function drawMap() {
    const t = (x, y, str, o) => s('text', Object.assign({ x, y, fill: CA.tc('#8b949e'), 'font-size': 7, 'text-anchor': 'middle', 'pointer-events': 'none' }, o || {}), str);
    mapSvg.append(
      s('path', { d: poly(C.brain), fill: CA.tc('#1c2230'), stroke: CA.tc('#3d444d'), 'stroke-width': 1.2 }),
      t((BX0 + BX1) / 2, BY0 + 9, 'Seen from the front', { 'font-size': 7.5 }),
      t(BX0 + 4, BY0 + 9, '← fly’s right', { 'text-anchor': 'start' }),
      t(BX1 - 4, BY0 + 9, 'fly’s left →', { 'text-anchor': 'end' }),
      t(BX0 + 4, BY1 - 5, 'dorsal ↑ · ventral ↓', { 'text-anchor': 'start', 'font-size': 6.5 }));
    outlineG = s('g', { 'pointer-events': 'none' });
    edgeG = s('g', { 'pointer-events': 'none' });
    nodeG = s('g', {});
    mapSvg.append(outlineG, edgeG, nodeG);
    C.regions.forEach((r, i) => {
      const [x, y] = POS[i];
      const g = s('g', { class: 'fm-node', 'data-i': i, tabindex: 0, role: 'button', 'aria-label': info(i).name },
        s('circle', { cx: x, cy: y, r: 2.4 + Math.sqrt(C.geometry[i].vol) / 34 }),
        s('text', { x, y: y - 3.6 - Math.sqrt(C.geometry[i].vol) / 34, 'text-anchor': 'middle', 'font-size': 7 }, abbr(i)));
      g.addEventListener('mousemove', (ev) => CA.tip.show(nodeTip(i), ev));
      g.addEventListener('mouseleave', () => CA.tip.hide());
      g.addEventListener('click', () => choose(i));
      g.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); choose(i); } });
      nodeG.appendChild(g);
    });
  }
  function choose(i) {
    sel = sel === i ? null : i;
    CA.tip.hide();
    paint();
    renderCard();
  }

  function partners(i, lay, n) {
    const L = LAYERS[lay];
    return C.regions.map((r, j) => ({ j, v: j === i ? null : L.w(i, j) })).filter((x) => x.v != null)
      .sort((a, b) => (L.abs ? Math.abs(b.v) - Math.abs(a.v) : b.v - a.v)).slice(0, n);
  }
  function nodeTip(i) {
    const g = groupOf[C.regions[i]];
    const best = partners(i, layer, 3).map((p) => `${CA.esc(abbr(p.j))} (${LAYERS[layer].unit(p.v)})`).join(', ');
    return `<b>${CA.esc(info(i).name)}</b> · ${CA.esc(abbr(i))}<br><span class="muted">${CA.esc(g.label)}</span>` +
      `<br>${CA.esc(LAYERS[layer].label)}: ${best}<br><span class="muted">Activity − wiring: ${signed(C.diffRegion[i])}</span>`;
  }

  function nodeColor(i) {
    if (colorBy === 'diff') return ramp(DIV, 0.5 + C.diffRegion[i] / DR_MAX / 2);
    if (colorBy === 'func') return func && regionFuncs[i][func] ? CA.tc('#e3b341') : CA.tc('#3d444d');
    return groupOf[C.regions[i]].color;
  }
  function edgeColor(v) {
    if (layer === 'diff') return v >= 0 ? CA.tc('#f85149') : CA.tc('#58a6ff');
    return layer === 'fc' ? CA.tc('#f0883e') : CA.tc('#58a6ff');
  }

  function paint() {
    const L = LAYERS[layer];
    CA.clear(edgeG);
    CA.clear(outlineG);
    // the strongest pairs overall, and with a region selected, its own strongest partners on top
    const ranked = PAIRS.map(([i, j]) => ({ i, j, v: L.w(i, j) })).sort((a, b) => (L.abs ? Math.abs(b.v) - Math.abs(a.v) : b.v - a.v));
    const shown = ranked.slice(0, Math.round(PAIRS.length * top / 100));
    const vmax = Math.abs(ranked[0].v), vmin = Math.abs(shown[shown.length - 1].v);
    const line = (e, op, w) => s('line', { x1: POS[e.i][0], y1: POS[e.i][1], x2: POS[e.j][0], y2: POS[e.j][1], stroke: edgeColor(e.v), 'stroke-width': w, 'stroke-opacity': op, 'stroke-linecap': 'round' });
    const width = (e) => 0.6 + 3.2 * (Math.abs(e.v) - vmin) / Math.max(1e-9, vmax - vmin);
    if (sel != null) {
      const g = C.geometry[sel];
      outlineG.appendChild(s('path', { d: poly(g.outline), fill: groupOf[C.regions[sel]].color, 'fill-opacity': 0.18, stroke: groupOf[C.regions[sel]].color, 'stroke-width': 1, 'stroke-dasharray': '3 2' }));
      shown.forEach((e) => edgeG.appendChild(line(e, 0.12, width(e))));
      partners(sel, layer, 8).forEach((p) => {
        const e = { i: sel, j: p.j, v: p.v };
        edgeG.appendChild(line(e, 0.9, Math.max(1.2, width(e))));
      });
    } else {
      shown.slice().reverse().forEach((e) => edgeG.appendChild(line(e, 0.25 + 0.6 * (Math.abs(e.v) - vmin) / Math.max(1e-9, vmax - vmin), width(e))));
    }
    const near = sel == null ? null : new Set(partners(sel, layer, 8).map((p) => p.j));
    nodeG.querySelectorAll('.fm-node').forEach((g) => {
      const i = +g.dataset.i;
      const c = g.querySelector('circle');
      c.setAttribute('fill', nodeColor(i));
      c.setAttribute('stroke', i === sel ? CA.tc('#e6edf3') : CA.tc('#0d1117'));
      c.setAttribute('stroke-width', i === sel ? 1.8 : 0.8);
      const dim = (near && i !== sel && !near.has(i)) || (colorBy === 'func' && func && !regionFuncs[i][func]);
      g.style.opacity = dim ? 0.35 : 1;
      g.querySelector('text').setAttribute('fill', CA.tc('#c9d1d9'));
    });
    paintSelected();
    renderLegend();
    document.querySelectorAll('.fmx rect.cell').forEach((r) => r.classList.toggle('row-on', sel != null && +r.dataset.i === sel));
  }
  function paintSelected() {
    const e = CA.selected;
    nodeG.querySelectorAll('.fm-node').forEach((g) => g.classList.toggle('sel', !!e && info(+g.dataset.i).entities.includes(e)));
  }

  /* ------------------------------------------------------------------ controls, legend and region card */
  let legendEl;
  function renderControls() {
    const seg = h('div', { class: 'seg', role: 'group', 'aria-label': 'Connections shown' },
      Object.entries(LAYERS).map(([k, L]) => h('button', { class: k === layer ? 'on' : '', 'aria-pressed': String(k === layer), onclick: () => {
        layer = k; CA.store.set('flymap.layer', k);
        seg.querySelectorAll('button').forEach((b, n) => { const on = Object.keys(LAYERS)[n] === k; b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on)); });
        paint(); renderCard();
      } }, L.label)));
    const topOut = h('span', { class: 'small muted' }, top + '%');
    const slider = h('input', { type: 'range', min: 2, max: 25, step: 1, value: top, style: { width: '120px' }, 'aria-label': 'Share of region pairs to draw',
      oninput: (ev) => { top = +ev.target.value; topOut.textContent = top + '%'; CA.store.set('flymap.top', top); paint(); } });
    const colorSel = h('select', { 'aria-label': 'Colour regions by', onchange: (ev) => { colorBy = ev.target.value; CA.store.set('flymap.color', colorBy); funcRow.style.display = colorBy === 'func' ? '' : 'none'; paint(); } },
      [['group', 'Super-region'], ['diff', 'Activity − wiring'], ['func', 'A function in the atlas']].map(([v, l]) => h('option', { value: v, selected: v === colorBy }, l)));
    const funcs = Object.keys(FUNCS).sort((a, b) => CA.ent[a].name.localeCompare(CA.ent[b].name));
    if (!func || !FUNCS[func]) func = funcs.includes('f-associative') ? 'f-associative' : funcs[0];
    const funcRow = h('div', { class: 'chips', style: { marginTop: '8px', display: colorBy === 'func' ? '' : 'none' } },
      funcs.map((f) => h('span', { class: 'chip' + (f === func ? ' on' : ''), 'data-f': f, onclick: () => {
        func = f; funcRow.querySelectorAll('.chip').forEach((c) => c.classList.toggle('on', c.dataset.f === f)); paint();
      } }, CA.ent[f].name)));
    legendEl = h('div', { style: { marginTop: '10px' } });
    CA.clear(ctl).append(
      h('h4', { style: { marginTop: 0 } }, 'Connections'), seg,
      h('div', { class: 'row small', style: { marginTop: '8px' } }, 'Strongest', slider, topOut, h('span', { class: 'muted' }, 'of pairs')),
      h('h4', {}, 'Colour regions by'), colorSel, funcRow, legendEl);
  }
  function renderLegend() {
    if (!legendEl) return;
    CA.clear(legendEl);
    const row = (color, label, title) => h('div', { class: 'row small', title }, h('span', { class: 'dot', style: { background: color } }), label);
    if (colorBy === 'group') CFG.groups.forEach((g) => legendEl.appendChild(row(g.color, g.label)));
    else if (colorBy === 'diff') {
      legendEl.append(h('div', { class: 'fm-ramp', style: { background: `linear-gradient(90deg, ${DIV.join(',')})` } }),
        h('div', { class: 'row tiny muted', style: { justifyContent: 'space-between' } }, h('span', {}, 'less coupled than wired'), h('span', {}, 'more coupled than wired')));
    } else if (func) {
      legendEl.append(h('div', { class: 'small muted' }, 'Regions holding a structure or cell type with an evidence-graded link to ', CA.entChip(func), ' in this atlas.'));
    }
    const L = LAYERS[layer];
    legendEl.appendChild(h('div', { class: 'small muted', style: { marginTop: '8px' } }, layer === 'diff'
      ? [h('span', { style: { color: CA.tc('#f85149') } }, '— more'), ' or ', h('span', { style: { color: CA.tc('#58a6ff') } }, '— less'), ' coupled in activity than the wiring predicts (z-scored difference, Fig. 4)']
      : [h('span', { style: { color: edgeColor(1) } }, '—'), ' ', L.long, layer === 'fc' ? ': correlated spontaneous activity' : ': neurons linking the regions, both directions']));
  }

  function renderCard() {
    CA.clear(card);
    if (sel == null) {
      card.append(h('h3', {}, 'How to read this map'),
        h('p', { class: 'small' }, 'Each dot is a brain region, placed where it lies in a front view of the brain and sized by its volume. Lines join the most strongly connected pairs: by correlated activity, by the neurons that wire them, or by how far the two disagree.'),
        h('p', { class: 'small' }, `Across all ${C.pairs} pairs of regions, the log number of connecting neurons predicts the activity correlation with r = ${C.r.toFixed(2)}. The regions most coupled in activity beyond their wiring sit in the mushroom body and the antennal lobe, as Turner et al. found.`),
        h('p', { class: 'small muted' }, 'Click a region for its strongest partners. ', h('a', { href: '#/atlas' }, 'The 3D atlas'), ' shows the main neuropils in 3D.'));
      return;
    }
    const i = sel, r = C.regions[i], g = groupOf[r], ents = info(i).entities;
    const rank = C.diffRegion.map((v, k) => [v, k]).sort((a, b) => b[0] - a[0]).findIndex(([, k]) => k === i) + 1;
    const plist = (lay, n) => h('div', { class: 'fm-plist' }, partners(i, lay, n).map((p) =>
      h('button', { class: 'fm-p', onclick: () => choose(p.j), title: info(p.j).name },
        h('span', { class: 'dot', style: { background: groupOf[C.regions[p.j]].color } }), h('span', { class: 'grow' }, abbr(p.j)), h('span', { class: 'muted tiny' }, LAYERS[lay].unit(p.v)))));
    const fns = Object.keys(regionFuncs[i]);
    card.append(h('h3', {}, info(i).name),
      h('div', { class: 'row small', style: { marginBottom: '8px' } }, h('span', { class: 'dot', style: { background: g.color } }), g.label, h('span', { class: 'muted' }, '· ' + abbr(i))),
      ents.length ? h('div', { class: 'chips', style: { marginBottom: '6px' } }, ents.map((e) => CA.entChip(e)))
        : h('p', { class: 'small muted' }, 'No structure or cell type of this atlas is placed in this region yet.'),
      fns.length ? h('div', { class: 'small', style: { margin: '6px 0' } }, 'Functions linked in the atlas: ', h('span', { class: 'chips', style: { display: 'inline-flex' } }, fns.map((f) => CA.entChip(f)))) : null,
      h('h4', {}, 'Strongest activity partners'), plist('fc', 5),
      h('h4', {}, 'Most wired partners'), plist('sc', 5),
      h('p', { class: 'small', style: { marginTop: '10px' } }, `Activity − wiring: ${signed(C.diffRegion[i])} ± ${C.diffRegionSem[i].toFixed(2)} (z, mean ± s.e.m. over ${C.flies} flies), ${rank} of ${N}. `,
        h('span', { class: 'muted' }, C.diffRegion[i] > 0 ? 'Its activity is more coupled to other regions’ than its direct wiring predicts.' : 'Its activity is less coupled to other regions’ than its wiring predicts.')),
      h('div', { class: 'row', style: { marginTop: '8px' } },
        ents.length ? h('button', { class: 'btn', onclick: () => CA.labAdd(ents[0]) }, '+ Hypothesis') : null,
        h('button', { class: 'btn ghost', onclick: () => choose(i) }, 'Clear')));
  }

  /* ------------------------------------------------------------------ matrices, scatter and per-region difference */
  function matrix(kind) {
    const cell = 10, M = 64, size = M + N * cell + 4;
    const svg = s('svg', { viewBox: `0 0 ${size} ${size}`, width: '100%', class: 'fmx', role: 'img', 'aria-label': kind === 'fc' ? 'Functional connectivity matrix' : 'Structural connectivity matrix' });
    const val = (i, j) => (kind === 'fc' ? fc(i, j) : C.sc[i][j]);
    const color = (v) => (v == null ? CA.tc('#30363d') : kind === 'fc' ? ramp(SEQ, (v - FC_MIN) / (FC_MAX - FC_MIN)) : ramp(SEQ, v > 0 ? Math.log10(v) / SC_MAX : 0));
    ORDER.forEach((i, a) => {
      svg.appendChild(s('text', { x: M - 3, y: M + a * cell + cell * 0.75, 'text-anchor': 'end', 'font-size': 7, fill: CA.tc('#c9d1d9') }, abbr(i)));
      svg.appendChild(s('text', { x: 0, y: 0, transform: `translate(${M + a * cell + cell * 0.72} ${M - 3}) rotate(-90)`, 'font-size': 7, fill: CA.tc('#c9d1d9') }, abbr(i)));
      ORDER.forEach((j, b) => {
        const v = val(i, j);
        const r = s('rect', { class: 'cell', 'data-i': i, x: M + b * cell, y: M + a * cell, width: cell, height: cell, fill: color(v) });
        r.addEventListener('mousemove', (ev) => CA.tip.show(kind === 'fc'
          ? `<b>${CA.esc(abbr(i))} ↔ ${CA.esc(abbr(j))}</b><br>${v == null ? '' : 'Activity correlation z = ' + v.toFixed(2)}<br><span class="muted">${Math.round(scSym(i, j)).toLocaleString()} connecting cells (mean of both directions)</span>`
          : `<b>${CA.esc(abbr(i))} → ${CA.esc(abbr(j))}</b><br>${v.toLocaleString()} neurons with input in ${CA.esc(abbr(i))} and output in ${CA.esc(abbr(j))}<br><span class="muted">reverse: ${C.sc[j][i].toLocaleString()}</span>`, ev));
        r.addEventListener('mouseleave', () => CA.tip.hide());
        r.addEventListener('click', () => { sel = i; paint(); renderCard(); mapSvg.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); });
        svg.appendChild(r);
      });
    });
    let k = 0;   // super-region separators
    CFG.groups.forEach((g) => {
      k += g.regions.length;
      if (k >= N) return;
      const p = M + k * cell;
      svg.append(s('line', { x1: M, x2: M + N * cell, y1: p, y2: p, stroke: CA.tc('#e6edf3'), 'stroke-width': 0.8, opacity: 0.55 }),
        s('line', { y1: M, y2: M + N * cell, x1: p, x2: p, stroke: CA.tc('#e6edf3'), 'stroke-width': 0.8, opacity: 0.55 }));
    });
    const lo = kind === 'fc' ? (Math.abs(FC_MIN) < 0.05 ? 0 : FC_MIN).toFixed(1) + ' z' : '0 cells';
    const hi = kind === 'fc' ? FC_MAX.toFixed(1) + ' z' : Math.round(10 ** SC_MAX).toLocaleString() + ' cells';
    return h('div', {}, svg, h('div', { class: 'row tiny muted', style: { gap: '8px' } }, h('span', {}, lo),
      h('span', { class: 'fm-ramp grow', style: { background: `linear-gradient(90deg, ${SEQ.join(',')})` } }), h('span', {}, hi)));
  }

  function scatterPlot() {
    const W = 420, H = 300, L = 46, B = 36, T = 12, R = 24;
    const pts = PAIRS.map(([i, j]) => ({ i, j, x: Math.log10(Math.max(1, scSym(i, j))), y: fc(i, j) }));
    const x0 = Math.floor(Math.min(...pts.map((p) => p.x))), x1 = Math.ceil(Math.max(...pts.map((p) => p.x)));
    const y0 = Math.floor(FC_MIN * 5) / 5, y1 = Math.ceil(FC_MAX * 5) / 5;
    const X = (v) => L + (W - L - R) * (v - x0) / (x1 - x0), Y = (v) => H - B - (H - B - T) * (v - y0) / (y1 - y0);
    const n = pts.length, mx = pts.reduce((a, p) => a + p.x, 0) / n, my = pts.reduce((a, p) => a + p.y, 0) / n;
    const slope = pts.reduce((a, p) => a + (p.x - mx) * (p.y - my), 0) / pts.reduce((a, p) => a + (p.x - mx) ** 2, 0);
    const svg = s('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': 'Structural against functional connectivity for every pair of regions' });
    const ax = CA.tc('#8b949e');
    for (let v = x0; v <= x1; v++) svg.append(s('line', { x1: X(v), x2: X(v), y1: T, y2: H - B, stroke: CA.tc('#30363d') }),
      s('text', { x: X(v), y: H - B + 14, 'text-anchor': 'middle', 'font-size': 10, fill: ax }, (10 ** v).toLocaleString()));
    for (let v = y0; v <= y1 + 1e-9; v += 0.2) svg.append(s('line', { x1: L, x2: W - R, y1: Y(v), y2: Y(v), stroke: CA.tc('#30363d') }),
      s('text', { x: L - 6, y: Y(v) + 3.5, 'text-anchor': 'end', 'font-size': 10, fill: ax }, v.toFixed(1)));
    svg.append(s('text', { x: (L + W - R) / 2, y: H - 4, 'text-anchor': 'middle', 'font-size': 10.5, fill: ax }, 'Connecting neurons (hemibrain, log scale)'),
      s('text', { x: 0, y: 0, transform: `translate(12 ${(T + H - B) / 2}) rotate(-90)`, 'text-anchor': 'middle', 'font-size': 10.5, fill: ax }, 'Activity correlation (z)'));
    pts.forEach((p) => {
      const c = s('circle', { cx: X(p.x), cy: Y(p.y), r: 2.4, fill: CA.tc('#79c0ff'), 'fill-opacity': 0.55 });
      c.addEventListener('mousemove', (ev) => CA.tip.show(`<b>${CA.esc(abbr(p.i))} ↔ ${CA.esc(abbr(p.j))}</b><br>z = ${p.y.toFixed(2)} · ${Math.round(10 ** p.x).toLocaleString()} cells`, ev));
      c.addEventListener('mouseleave', () => CA.tip.hide());
      c.addEventListener('click', () => { sel = p.i; paint(); renderCard(); mapSvg.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); });
      svg.appendChild(c);
    });
    svg.appendChild(s('line', { x1: X(x0), x2: X(x1), y1: Y(my + slope * (x0 - mx)), y2: Y(my + slope * (x1 - mx)), stroke: CA.tc('#f0883e'), 'stroke-width': 2 }));
    svg.appendChild(s('text', { x: L + 8, y: T + 14, 'font-size': 12, fill: CA.tc('#e6edf3'), 'font-weight': 600 }, `r = ${C.r.toFixed(2)}`));
    const fr = C.flyR;
    return h('div', {}, svg, h('p', { class: 'tiny muted', style: { marginTop: '6px' } },
      `Each dot is a pair of regions (${C.pairs}); the line is the least-squares fit. Pearson r over pairs = ${C.r.toFixed(2)} in this recomputation (the paper reports 0.74 for this comparison); within single flies r ranges ${Math.min(...fr).toFixed(2)}–${Math.max(...fr).toFixed(2)}.`));
  }

  function diffChart() {
    const order = C.diffRegion.map((v, i) => [v, i]).sort((a, b) => b[0] - a[0]).map(([, i]) => i);
    const W = 420, rowH = 11, T = 6, L = 64, R = 12, H = T + order.length * rowH + 22;
    const lim = Math.ceil(Math.max(...order.map((i) => Math.abs(C.diffRegion[i]) + C.diffRegionSem[i])) * 5) / 5;
    const X = (v) => L + (W - L - R) * (v + lim) / (2 * lim);
    const svg = s('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': 'Mean difference between activity and wiring, per region' });
    svg.appendChild(s('line', { x1: X(0), x2: X(0), y1: T, y2: H - 20, stroke: CA.tc('#8b949e') }));
    order.forEach((i, k) => {
      const y = T + k * rowH + rowH / 2, v = C.diffRegion[i], e = C.diffRegionSem[i], col = groupOf[C.regions[i]].color;
      const g = s('g', { class: 'mc-el' },
        s('text', { x: L - 6, y: y + 3, 'text-anchor': 'end', 'font-size': 8.5, fill: CA.tc('#c9d1d9') }, abbr(i)),
        s('rect', { x: Math.min(X(0), X(v)), y: y - 3.6, width: Math.abs(X(v) - X(0)), height: 7.2, fill: col, 'fill-opacity': 0.8 }),
        s('line', { x1: X(v - e), x2: X(v + e), y1: y, y2: y, stroke: CA.tc('#e6edf3'), 'stroke-width': 1 }));
      g.addEventListener('mousemove', (ev) => CA.tip.show(`<b>${CA.esc(info(i).name)}</b><br>${signed(v)} ± ${e.toFixed(2)} (z)`, ev));
      g.addEventListener('mouseleave', () => CA.tip.hide());
      g.addEventListener('click', () => { sel = i; paint(); renderCard(); mapSvg.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); });
      svg.appendChild(g);
    });
    svg.append(s('text', { x: X(-lim), y: H - 6, 'font-size': 9.5, fill: CA.tc('#8b949e') }, 'less coupled than wired'),
      s('text', { x: X(lim), y: H - 6, 'font-size': 9.5, fill: CA.tc('#8b949e'), 'text-anchor': 'end' }, 'more coupled than wired'));
    return h('div', {}, svg, h('p', { class: 'tiny muted', style: { marginTop: '6px' } },
      'Per region, the mean of z-scored activity correlation minus z-scored log connecting cells over its connected pairs, as in Turner et al. (Fig. 4); bars are mean ± s.e.m. over flies, coloured by super-region.'));
  }
})();
