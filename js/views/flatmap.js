/* Functional map: a schematic SUIT-style flatmap of the human cerebellar cortex with literature-based overlays. */
(function () {
  'use strict';
  const CA = window.CA, D = CA.D, FM = D.flatmap, h = CA.h, s = CA.s;
  const OV = FM.overlays;
  let root, svg, card, overlayId = CA.store.get('map.overlay', 'dominant'), selRegion = null, unsub = null;

  CA.register('map', { title: 'Functional map', mount, unmount });

  // ------- geometry: bands stacked top (anterior) to bottom (posterior), split into L / vermis / R -------
  const PAD_X = 90, PAD_Y = 56, MAXW = Math.max(...FM.bands.map((b) => b.w));
  const W = 2 * MAXW + 2 * PAD_X, CX = W / 2;
  let y = PAD_Y;
  FM.bands.forEach((b) => { b.y0 = y; y += b.h; b.y1 = y; });
  const H = y + PAD_Y;
  const VH = FM.vermisHalf;

  const regions = [];
  FM.bands.forEach((b) => ['L', 'V', 'R'].forEach((side) => regions.push({
    id: side + '-' + b.id, band: b, side,
    x0: side === 'L' ? CX - b.w - 30 : side === 'V' ? CX - VH : CX + VH,
    x1: side === 'L' ? CX - VH : side === 'V' ? CX + VH : CX + b.w + 30,
  })));
  const sideName = { L: 'Left', V: 'Vermis', R: 'Right' };
  const regionName = (r) => r.side === 'V' ? `Vermis ${r.band.vlabel || r.band.label}` : `${sideName[r.side]} ${r.band.label}`;
  const regionEntity = (r) => (r.side === 'V' && r.band.vermis) ? r.band.vermis : r.band.entity;

  function score(ov, r) {
    const sc = ov.scores;
    if (sc[r.id] != null) return sc[r.id];
    if (sc[r.band.id] != null) return sc[r.band.id];
    return 0;
  }
  function lesionCat(r) {
    const m = FM.lesion.map;
    return m[r.id] || m[r.band.id] || null;
  }
  function dominant(r) {
    const scored = OV.map((o) => ({ o, v: score(o, r) })).filter((x) => x.v > 0).sort((a, b) => b.v - a.v);
    if (!scored.length) return null;
    const top = scored.filter((x) => x.v === scored[0].v);
    return { v: scored[0].v, list: top.map((x) => x.o) };
  }

  // smooth silhouette through band half-widths
  function silhouette() {
    const pts = [[CX + FM.bands[0].w * 0.55, PAD_Y - 6]];
    FM.bands.forEach((b) => pts.push([CX + b.w, (b.y0 + b.y1) / 2]));
    const last = FM.bands[FM.bands.length - 1];
    pts.push([CX + last.w * 0.6, last.y1 + 8]);
    const right = catmull(pts);
    const left = catmull(pts.map(([x, yy]) => [2 * CX - x, yy]).reverse());
    return `M ${CX} ${PAD_Y - 10} L ${pts[0][0]} ${pts[0][1]} ${right} L ${CX} ${last.y1 + 12} L ${2 * CX - pts[pts.length - 1][0]} ${pts[pts.length - 1][1]} ${left} Z`;
  }
  function catmull(p) {
    let d = '';
    for (let i = 0; i < p.length - 1; i++) {
      const p0 = p[i - 1] || p[i], p1 = p[i], p2 = p[i + 1], p3 = p[i + 2] || p2;
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += ` C ${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
    }
    return d;
  }

  // ------- view -------
  function mount(node) {
    root = node;
    const chips = h('div', { class: 'chips' });
    const opts = [{ id: 'dominant', label: 'Dominant domain' }, ...OV.map((o) => ({ id: o.id, label: o.label, color: o.color })), { id: 'lesion', label: 'Lesion syndromes' }];
    opts.forEach((o) => chips.appendChild(h('span', {
      class: 'chip' + (o.id === overlayId ? ' on' : ''), 'data-o': o.id,
      onclick: () => { overlayId = o.id; CA.store.set('map.overlay', o.id); chips.querySelectorAll('.chip').forEach((c) => c.classList.toggle('on', c.dataset.o === o.id)); paint(); renderCard(); },
    }, o.color ? h('span', { class: 'dot', style: { background: o.color } }) : null, o.label)));
    card = h('div', {});
    svg = s('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: { maxHeight: 'calc(100vh - 210px)', display: 'block' } });
    drawMap();
    root.appendChild(h('div', { class: 'page' },
      h('div', { class: 'page-head' },
        h('div', {}, h('h2', {}, 'Functional map of the human cerebellar cortex'),
          h('p', {}, 'The cerebellar cortex unfolded into a flatmap (anterior lobe at top). Overlays summarize where imaging meta-analyses, connectivity maps and lesion studies place each function. Click a region for its scores, sources and the lobule entry.'))),
      h('div', { class: 'cols' },
        h('div', {}, h('div', { class: 'card' }, h('h4', { style: { marginTop: 0 } }, 'Overlay'), chips, h('div', { id: 'fm-legend', style: { marginTop: '10px' } })), h('div', { class: 'card' }, card)),
        h('div', { class: 'svgwrap', style: { padding: '8px' } }, svg)),
      h('p', { class: 'small muted', style: { marginTop: '12px' } }, FM.note, ' ', CA.citeChips(FM.refs))));
    paint();
    renderCard();
    unsub = CA.on('select', paintSelection);
  }
  function unmount() { if (unsub) unsub(); unsub = null; }

  function drawMap() {
    const defs = s('defs', {},
      s('clipPath', { id: 'fm-clip' }, s('path', { d: silhouette() })),
      s('pattern', { id: 'fm-hatch', width: 8, height: 8, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' },
        s('rect', { width: 8, height: 8, fill: '#3a3f4b' }), s('line', { x1: 0, y1: 0, x2: 0, y2: 8, stroke: '#9ca3af', 'stroke-width': 3 })));
    svg.appendChild(defs);
    svg.appendChild(s('path', { d: silhouette(), fill: '#1c2230', stroke: '#3d444d', 'stroke-width': 1.5 }));
    const g = s('g', { 'clip-path': 'url(#fm-clip)' });
    regions.forEach((r) => {
      const rect = s('rect', { class: 'fm-region', x: r.x0, y: r.band.y0, width: r.x1 - r.x0, height: r.band.h, 'data-r': r.id, fill: '#2a3140' });
      rect.addEventListener('mousemove', (ev) => CA.tip.show(tipHtml(r), ev));
      rect.addEventListener('mouseleave', () => CA.tip.hide());
      rect.addEventListener('click', () => { selRegion = r; renderCard(); paintSelection(); CA.select(regionEntity(r)); });
      r.el = rect;
      g.appendChild(rect);
    });
    svg.appendChild(g);
    // vermis guide lines, fissures, labels
    svg.appendChild(s('line', { x1: CX - VH, x2: CX - VH, y1: PAD_Y, y2: H - PAD_Y, stroke: '#0d1117', 'stroke-width': 2, 'clip-path': 'url(#fm-clip)' }));
    svg.appendChild(s('line', { x1: CX + VH, x2: CX + VH, y1: PAD_Y, y2: H - PAD_Y, stroke: '#0d1117', 'stroke-width': 2, 'clip-path': 'url(#fm-clip)' }));
    FM.fissures.forEach((f) => {
      const b = FM.bands.find((x) => x.id === f.after);
      svg.appendChild(s('line', { x1: PAD_X - 10, x2: W - PAD_X + 10, y1: b.y1, y2: b.y1, stroke: '#e6edf3', 'stroke-width': 1.5, 'stroke-dasharray': '6 4', opacity: 0.7, 'clip-path': 'url(#fm-clip)' }));
      // two short lines so the label fits in the margin beside the widest bands
      const words = f.label.split(' ');
      svg.appendChild(s('text', { x: W - 6, y: b.y1 - 2, 'text-anchor': 'end', fill: '#8b949e', 'font-size': 11 },
        s('tspan', { x: W - 6 }, words.slice(0, -1).join(' ') || f.label), words.length > 1 ? s('tspan', { x: W - 6, dy: 12 }, words[words.length - 1]) : null));
    });
    FM.bands.forEach((b) => {
      svg.appendChild(s('text', { x: CX + b.w + 36, y: (b.y0 + b.y1) / 2 + 4, fill: '#c9d1d9', 'font-size': 12, 'pointer-events': 'none' }, b.label));
      svg.appendChild(s('text', { x: CX - b.w - 36, y: (b.y0 + b.y1) / 2 + 4, fill: '#c9d1d9', 'font-size': 12, 'text-anchor': 'end', 'pointer-events': 'none' }, b.label));
    });
    svg.appendChild(s('text', { x: CX - MAXW * 0.55, y: 24, fill: '#8b949e', 'font-size': 13, 'text-anchor': 'middle' }, 'Left hemisphere'));
    svg.appendChild(s('text', { x: CX, y: 24, fill: '#8b949e', 'font-size': 13, 'text-anchor': 'middle' }, 'Vermis'));
    svg.appendChild(s('text', { x: CX + MAXW * 0.55, y: 24, fill: '#8b949e', 'font-size': 13, 'text-anchor': 'middle' }, 'Right hemisphere'));
    svg.appendChild(s('text', { x: 12, y: FM.bands[0].y0 + 14, fill: '#6e7681', 'font-size': 11 }, 'Anterior lobe'));
    svg.appendChild(s('text', { x: 12, y: FM.bands[2].y0 + 16, fill: '#6e7681', 'font-size': 11 }, 'Posterior lobe'));
    svg.appendChild(s('text', { x: 12, y: FM.bands[FM.bands.length - 1].y1 - 4, fill: '#6e7681', 'font-size': 11 }, 'Flocculonodular lobe'));
  }

  function fillFor(r) {
    if (overlayId === 'lesion') {
      const c = lesionCat(r);
      return c ? { fill: FM.lesion.cats[c].color, op: c === 'vestib' ? 0.45 : 0.85 } : { fill: '#2a3140', op: 1 };
    }
    if (overlayId === 'dominant') {
      const d = dominant(r);
      if (!d) return { fill: '#2a3140', op: 1 };
      if (d.list.length > 1) return { fill: 'url(#fm-hatch)', op: 0.35 + 0.2 * d.v };
      return { fill: d.list[0].color, op: 0.25 + 0.23 * d.v };
    }
    const ov = OV.find((o) => o.id === overlayId);
    const v = score(ov, r);
    return v ? { fill: ov.color, op: 0.2 + 0.26 * v } : { fill: '#2a3140', op: 1 };
  }

  function paint() {
    regions.forEach((r) => { const f = fillFor(r); r.el.setAttribute('fill', f.fill); r.el.setAttribute('fill-opacity', f.op); });
    const lg = document.getElementById('fm-legend');
    if (!lg) return;
    CA.clear(lg);
    if (overlayId === 'lesion') {
      Object.values(FM.lesion.cats).forEach((c) => lg.appendChild(h('div', { class: 'row small' }, h('span', { class: 'dot', style: { background: c.color } }), c.label)));
      lg.appendChild(h('div', { class: 'small', style: { marginTop: '6px' } }, CA.citeChips(FM.lesion.refs)));
    } else if (overlayId === 'dominant') {
      lg.appendChild(h('div', { class: 'small muted' }, 'Color = highest-scoring domain; strength = score.'));
      OV.forEach((o) => lg.appendChild(h('div', { class: 'row small' }, h('span', { class: 'dot', style: { background: o.color } }), o.label)));
      lg.appendChild(h('div', { class: 'row small' }, h('span', { class: 'dot', style: { background: 'repeating-linear-gradient(45deg,#9ca3af 0 3px,#3a3f4b 3px 6px)' } }), 'Overlapping association domains'));
    } else {
      const ov = OV.find((o) => o.id === overlayId);
      lg.appendChild(h('div', { class: 'row small' }, ['weak', 'moderate', 'strong'].map((t, i) =>
        h('span', { class: 'row' }, h('span', { class: 'dot', style: { background: ov.color, opacity: 0.2 + 0.26 * (i + 1) } }), t))));
      lg.appendChild(h('div', { class: 'small', style: { marginTop: '6px' } }, 'Sources: ', CA.citeChips(ov.refs)));
    }
    paintSelection();
  }

  function paintSelection() {
    const sel = CA.selected;
    regions.forEach((r) => {
      const on = selRegion ? selRegion === r : (sel && (regionEntity(r) === sel));
      r.el.classList.toggle('sel', !!on);
    });
  }

  function tipHtml(r) {
    const lines = OV.map((o) => ({ o, v: score(o, r) })).filter((x) => x.v > 0)
      .map((x) => `<span style="color:${x.o.color}">●</span> ${CA.esc(x.o.label)}: ${'●'.repeat(x.v)}${'○'.repeat(3 - x.v)}`);
    const les = lesionCat(r);
    return `<b>${CA.esc(regionName(r))}</b><br>${lines.join('<br>') || '<span class="muted">no overlay scores</span>'}`
      + (les ? `<br><span class="muted">Lesion: ${CA.esc(FM.lesion.cats[les].label)}</span>` : '');
  }

  function renderCard() {
    CA.clear(card);
    if (!selRegion) {
      card.append(h('h3', {}, 'How to read this map'),
        h('p', { class: 'small' }, 'Motor functions sit in two mirrored maps (anterior lobe and lobule VIII). Cognitive, social and affective functions sit mainly in the posterior lobe (Crus I/II, VIIB, IX): language right-lateralized, emotion in the vermis.'),
        h('p', { class: 'small muted' }, 'This mirrors crossed cerebro-cerebellar loops: right cerebellum ↔ left cerebral (language-dominant) hemisphere.'),
        h('p', { class: 'small' }, 'To see these lobules in 3D, with the rest of the brain, open the ', h('a', { href: '#/atlas' }, '3D atlas'), '.'));
      return;
    }
    const r = selRegion;
    const ent = regionEntity(r);
    const les = lesionCat(r);
    card.append(h('h3', {}, regionName(r)),
      h('div', { class: 'row', style: { marginBottom: '8px' } }, CA.entChip(ent), r.side === 'V' && r.band.entity !== ent ? CA.entChip(r.band.entity) : null),
      h('div', { class: 'scoregrid' }, OV.map((o) => {
        const v = score(o, r);
        return [h('span', {}, o.label), h('div', { class: 'bar' }, h('i', { style: { width: (v / 3 * 100) + '%', background: o.color } })), h('span', { class: 'muted tiny' }, v)];
      })),
      les ? h('p', { class: 'small', style: { marginTop: '10px' } }, 'Lesions: ', CA.entChip(FM.lesion.cats[les].entity), h('br'), h('span', { class: 'muted' }, FM.lesion.cats[les].label)) : null,
      h('h4', {}, 'Sources for nonzero scores'),
      h('div', {}, [...new Set(OV.filter((o) => score(o, r) > 0).flatMap((o) => o.refs))].map((k) => CA.citeChips([k]))),
      h('div', { class: 'row', style: { marginTop: '10px' } },
        h('button', { class: 'btn', onclick: () => CA.labAdd(ent) }, '+ Hypothesis'),
        h('button', { class: 'btn ghost', onclick: () => { selRegion = null; renderCard(); paintSelection(); } }, 'Clear')));
  }
})();
