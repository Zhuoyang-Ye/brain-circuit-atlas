/* Across scales: every entity of the current region (or of all regions) in seven level columns, linked by evidence-graded connections. */
(function () {
  'use strict';
  const CA = window.CA, D = CA.D, h = CA.h, s = CA.s;
  const COLW = 182, ROWH = 27, NODEW = 156, TOP = 56;
  let root, svg, nodes = {}, edges = [], focus = null, chain = null, domain = null, unsub = null, hidden = new Set(), hoverId = null;
  let scope = null;   // a region id, or 'all'
  const layoutCache = {};
  const scopedEntities = () => (scope === 'all' ? D.entities : D.entities.filter((e) => CA.inRegion(e.id)));
  const scopedLinks = () => (scope === 'all' ? D.links : D.links.filter((l) => l.regions.includes(scope)));
  const scopedChains = () => (scope === 'all' ? D.chains : D.chains.filter((c) => c.regions.includes(scope)));

  CA.register('scales', { title: 'Across scales', mount, unmount, route });

  const DASH = { established: '', supported: '', emerging: '6 4', debated: '8 3 2 3', hypothesis: '1.5 4' };
  const WIDTH = { established: 2.4, supported: 1.6, emerging: 1.4, debated: 1.4, hypothesis: 1.4 };

  /* ---------- layout: barycentric ordering within level columns ---------- */
  function layout() {
    if (layoutCache[scope]) return layoutCache[scope];
    const ents = scopedEntities(), inScope = new Set(ents.map((e) => e.id));
    const cols = D.levels.map((l) => ents.filter((e) => e.level === l.id).map((e) => e.id));
    const kindOrder = (id) => (CA.ent[id].kind || '') + CA.ent[id].name;
    cols.forEach((c) => c.sort((a, b) => kindOrder(a).localeCompare(kindOrder(b))));
    const pos = {};
    const setPos = () => cols.forEach((c) => c.forEach((id, i) => { pos[id] = c.length > 1 ? i / (c.length - 1) : 0.5; }));
    setPos();
    for (let it = 0; it < 12; it++) {
      const order = it % 2 ? [...cols.keys()].reverse() : [...cols.keys()];
      order.forEach((ci) => {
        const bary = {};
        cols[ci].forEach((id) => {
          const nb = [...CA.neighbors(id)].filter((n) => inScope.has(n) && CA.ent[n].level !== CA.ent[id].level);
          bary[id] = nb.length ? nb.reduce((a, n) => a + pos[n], 0) / nb.length : pos[id];
        });
        cols[ci].sort((a, b) => bary[a] - bary[b]);
        cols[ci].forEach((id, i) => { pos[id] = cols[ci].length > 1 ? i / (cols[ci].length - 1) : 0.5; });
      });
    }
    const maxN = Math.max(1, ...cols.map((c) => c.length));
    const xy = {};
    cols.forEach((c, ci) => {
      const off = (maxN - c.length) * ROWH / 2;
      c.forEach((id, i) => { xy[id] = { x: 20 + ci * COLW, y: TOP + off + i * ROWH, col: ci }; });
    });
    layoutCache[scope] = { xy, width: 40 + D.levels.length * COLW - (COLW - NODEW), height: TOP + maxN * ROWH + 30 };
    return layoutCache[scope];
  }

  function mount(node, r) {
    root = node;
    nodes = {}; chain = null;
    // an entity of another region, opened from its panel, shows the whole knowledge base
    const want = r && r.kind === 'e' && CA.ent[r.id] ? r.id : null;
    const allRegions = CA.store.get('scales.allRegions', false) || (want && !CA.inRegion(want));
    scope = allRegions ? 'all' : CA.region.id;
    const L = layout();
    svg = s('svg', { width: L.width, height: L.height, style: { display: 'block' } });
    draw(L);
    const chainSel = h('select', { onchange: (ev) => { setChain(ev.target.value || null); } },
      h('option', { value: '' }, 'Highlight a chain…'), scopedChains().map((c) => h('option', { value: c.id }, c.name)));
    const regionBox = D.regions.length > 1 ? h('label', { class: 'check small', title: 'Show the entities and links of every region' },
      h('input', { type: 'checkbox', checked: allRegions, onchange: (ev) => { CA.store.set('scales.allRegions', ev.target.checked); CA.clear(root); unmount(); mount(root, null); } }),
      'All regions') : null;
    const what = scope === 'all' ? 'Every entity in the knowledge base' : `Every ${CA.region.label.toLowerCase()} entity, with the shared structures and functions it links to`;
    const domChips = h('div', { class: 'chips' }, D.domains.map((d) => {
      const chip = CA.domainChip(d.id, { onclick: () => { domain = domain === d.id ? null : d.id; domChips.querySelectorAll('.chip').forEach((c) => c.classList.toggle('on', c.dataset.d === domain)); paint(); } });
      chip.dataset.d = d.id;
      return chip;
    }));
    const statusBoxes = h('div', { class: 'row small' }, D.statuses.filter((x) => x.id !== 'gap').map((st) => h('label', { class: 'check' },
      h('input', { type: 'checkbox', checked: true, onchange: (ev) => { if (ev.target.checked) hidden.delete(st.id); else hidden.add(st.id); paint(); } }),
      legendLine(st.id), st.label)));
    root.appendChild(h('div', { class: 'page', style: { maxWidth: 'none' } },
      h('div', { class: 'page-head' }, h('div', {},
        h('h2', {}, 'Across scales'),
        h('p', {}, what + ', from genes to disorders, with its evidence-graded links. Hover to see a neighborhood, click for details, or highlight a mechanistic chain that crosses levels.')),
        h('div', { class: 'row' }, regionBox, chainSel, h('button', { class: 'btn ghost', onclick: () => { focus = null; chainSel.value = ''; setChain(null); } }, 'Clear'))),
      h('div', { class: 'card', style: { marginBottom: '12px' } },
        h('div', { class: 'row', style: { justifyContent: 'space-between' } }, statusBoxes,
          h('span', { class: 'small muted' }, '± debated · ? hypothesis')),
        h('div', { style: { marginTop: '8px' } }, h('span', { class: 'small muted' }, 'Filter by domain: '), domChips),
        h('div', { id: 'chain-info', class: 'small', style: { marginTop: '8px' } })),
      h('div', { class: 'svgwrap' }, svg)));
    unsub = CA.on('select', (id) => { focus = id; paint(); });
    focus = CA.selected;
    route(r);
    paint();
  }
  function unmount() { if (unsub) unsub(); unsub = null; }
  function route(r) {
    if (r && r.kind === 'c' && scopedChains().some((c) => c.id === r.id)) setChain(r.id);
  }

  function legendLine(status) {
    return s('svg', { width: 26, height: 8 }, s('line', { x1: 1, y1: 4, x2: 25, y2: 4, stroke: CA.statusColor(status), 'stroke-width': WIDTH[status], 'stroke-dasharray': DASH[status] }));
  }

  function edgePath(a, b) {
    const ya = a.y + 10, yb = b.y + 10;
    if (a.col === b.col) {
      const x = a.x + NODEW, bend = 40 + Math.abs(ya - yb) * 0.15;
      return `M ${x} ${ya} C ${x + bend} ${ya}, ${x + bend} ${yb}, ${x} ${yb}`;
    }
    const fwd = b.col > a.col;
    const x1 = fwd ? a.x + NODEW : a.x, x2 = fwd ? b.x : b.x + NODEW;
    const dx = Math.max(40, Math.abs(x2 - x1) * 0.45) * (fwd ? 1 : -1);
    return `M ${x1} ${ya} C ${x1 + dx} ${ya}, ${x2 - dx} ${yb}, ${x2} ${yb}`;
  }

  function draw(L) {
    D.levels.forEach((l, ci) => {
      svg.appendChild(s('text', { x: 20 + ci * COLW + NODEW / 2, y: 24, 'text-anchor': 'middle', fill: l.color, 'font-size': 13, 'font-weight': 600 }, l.label));
      svg.appendChild(s('text', { x: 20 + ci * COLW + NODEW / 2, y: 40, 'text-anchor': 'middle', fill: '#6e7681', 'font-size': 10.5 }, scope === 'all' ? l.desc : CA.levelDesc(l.id)));
    });
    const eg = s('g', {}), ng = s('g', {}), gg = s('g', {});
    svg.append(eg, gg, ng);
    edges = scopedLinks().filter((l) => L.xy[l.s] && L.xy[l.t]).map((l) => {
      const a = L.xy[l.s], b = L.xy[l.t];
      const path = s('path', { class: 'edge', d: edgePath(a, b), stroke: '#8b949e', 'stroke-width': WIDTH[l.status], 'stroke-dasharray': DASH[l.status], opacity: 0.35 });
      path.addEventListener('mousemove', (ev) => CA.tip.show(`<b>${CA.esc(CA.ent[l.s].name)} → ${CA.esc(CA.ent[l.t].name)}</b><br>${CA.esc(l.rel)}<br><span style="color:${CA.statusColor(l.status)}">${CA.statusById[l.status].label}</span>`, ev));
      path.addEventListener('mouseleave', () => CA.tip.hide());
      path.addEventListener('click', () => CA.showLink(l.id));
      path.style.cursor = 'pointer';
      eg.appendChild(path);
      let glyph = null;
      if (l.status === 'debated' || l.status === 'hypothesis') {
        glyph = s('text', { 'font-size': 11, 'text-anchor': 'middle', fill: CA.statusColor(l.status), 'pointer-events': 'none', 'font-weight': 700 }, l.status === 'debated' ? '±' : '?');
        gg.appendChild(glyph);
      }
      return { l, path, glyph };
    });
    Object.entries(L.xy).forEach(([id, p]) => {
      const e = CA.ent[id];
      const label = e.name.length > 24 ? e.name.slice(0, 23) + '…' : e.name;
      const g = s('g', { class: 'node', transform: `translate(${p.x},${p.y})` },
        s('rect', { width: NODEW, height: 21, rx: 5, fill: '#1c2230', stroke: CA.levelColor(e.level), 'stroke-width': 1.2 }),
        s('text', { x: 8, y: 14.5 }, label));
      g.addEventListener('mouseenter', (ev) => { hoverId = id; paint(); CA.tip.show(`<b>${CA.esc(e.name)}</b><br><span class="muted">${CA.neighbors(id).size} connections</span>`, ev); });
      g.addEventListener('mousemove', (ev) => CA.tip.move(ev));
      g.addEventListener('mouseleave', () => { hoverId = null; paint(); CA.tip.hide(); });
      g.addEventListener('click', () => CA.select(id));
      ng.appendChild(g);
      nodes[id] = g;
    });
    // midpoint glyphs need the paths in the DOM to measure; place them lazily
    requestAnimationFrame(() => edges.forEach((ed) => {
      if (!ed.glyph || !ed.path.isConnected) return;
      const len = ed.path.getTotalLength(), m = ed.path.getPointAtLength(len / 2);
      ed.glyph.setAttribute('x', m.x); ed.glyph.setAttribute('y', m.y + 4);
    }));
  }

  function setChain(id) {
    chain = id ? scopedChains().find((c) => c.id === id) : null;
    const info = document.getElementById('chain-info');
    if (info) {
      CA.clear(info);
      if (chain) {
        info.append(h('b', {}, chain.name + ': '), chain.desc + ' ',
          h('a', { href: '#', onclick: (ev) => { ev.preventDefault(); CA.labAdd(chain.nodes.filter((n, i, a) => a.indexOf(n) === i)); } }, 'Test this chain in the Hypothesis lab →'));
      }
    }
    paint();
  }

  function paint() {
    if (!svg) return;
    const center = hoverId || focus;
    const nb = center ? CA.neighbors(center) : null;
    const chainNodes = chain ? new Set(chain.nodes) : null;
    const chainEdges = new Set();
    if (chain) chain.nodes.forEach((n, i) => { if (i) { const l = CA.linkBetween(chain.nodes[i - 1], n); if (l) chainEdges.add(l.id); } });
    const domOK = (id) => !domain || (CA.ent[id].domains || []).includes(domain);
    Object.entries(nodes).forEach(([id, g]) => {
      let on = true;
      if (chainNodes) on = chainNodes.has(id);
      else if (center) on = id === center || nb.has(id);
      if (!domOK(id)) on = false;
      g.style.opacity = on ? 1 : 0.18;
      const rect = g.firstChild;
      rect.setAttribute('fill', id === center || (chainNodes && chainNodes.has(id)) ? '#28344a' : '#1c2230');
      rect.setAttribute('stroke-width', id === center ? 2.5 : 1.2);
    });
    edges.forEach(({ l, path, glyph }) => {
      let on;
      if (hidden.has(l.status)) on = false;
      else if (chain) on = chainEdges.has(l.id);
      else if (center) on = l.s === center || l.t === center;
      else on = null;
      if (domain && !(domOK(l.s) && domOK(l.t))) on = false;
      path.setAttribute('stroke', on ? CA.statusColor(l.status) : '#8b949e');
      path.setAttribute('opacity', on === null ? 0.33 : on ? 0.95 : 0.05);
      path.setAttribute('stroke-width', WIDTH[l.status] * (on ? 1.4 : 1));
      if (glyph) glyph.setAttribute('opacity', on === false ? 0.08 : 1);
    });
  }
})();
