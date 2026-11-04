/* Brain Circuit Atlas: shared data indexes, brain regions, DOM helpers, router and the detail panel. */
(function () {
  'use strict';
  const D = window.CA_DATA;
  const CA = window.CA = { D, views: {}, order: [], current: null, params: {}, state: {} };

  /* ---------- indexes ---------- */
  const byId = (arr) => Object.fromEntries(arr.map((x) => [x.id, x]));
  CA.levelById = byId(D.levels);
  D.levels.forEach((l, i) => { l.index = i; });
  CA.statusById = byId(D.statuses);
  CA.evidenceById = byId(D.evidence);
  CA.domainById = byId(D.domains);
  CA.ent = byId(D.entities);
  CA.paper = Object.fromEntries(D.papers.map((p) => [p.key, p]));
  CA.out = {}; CA.inc = {};
  D.entities.forEach((e) => { CA.out[e.id] = []; CA.inc[e.id] = []; });
  D.links.forEach((l) => { l.id = l.s + '>' + l.t; CA.out[l.s].push(l); CA.inc[l.t].push(l); });
  CA.link = byId(D.links);
  CA.citedBy = {};
  const cite = (key, rec) => { (CA.citedBy[key] = CA.citedBy[key] || []).push(rec); };
  D.entities.forEach((e) => (e.refs || []).forEach((k) => cite(k, { kind: 'entity', id: e.id })));
  D.links.forEach((l) => (l.refs || []).forEach((k) => cite(k, { kind: 'link', id: l.id })));

  CA.linkBetween = (a, b) => CA.link[a + '>' + b] || CA.link[b + '>' + a] || null;
  CA.linksOf = (id) => (CA.out[id] || []).concat(CA.inc[id] || []);
  CA.neighbors = (id) => new Set(CA.linksOf(id).map((l) => (l.s === id ? l.t : l.s)));
  CA.rank = (status) => (CA.statusById[status] ? CA.statusById[status].rank : 0);
  CA.levelColor = (lv) => (CA.levelById[lv] ? CA.levelById[lv].color : CA.tc('#8b949e'));
  CA.entColor = (id) => CA.levelColor(CA.ent[id] && CA.ent[id].level);
  CA.statusColor = (s) => (CA.statusById[s] ? CA.statusById[s].color : CA.tc('#8b949e'));
  CA.has3D = (id) => {
    const a3 = D.atlas3d;
    if (Object.values(D.mesh3d || {}).some((m) => m.entities.includes(id))) return true;
    if (Object.values(a3.sides).some((ids) => ids.includes(id)) || (a3.composite || {})[id]) return true;
    return Object.values(a3.aliases).some((m) => m[id]);
  };

  /* ---------- small helpers ---------- */
  CA.esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  function append(node, kids) {
    for (const k of kids) {
      if (k == null || k === false) continue;
      if (Array.isArray(k)) append(node, k);
      else node.appendChild(k instanceof Node ? k : document.createTextNode(String(k)));
    }
  }
  function setAttrs(node, attrs, svg) {
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v == null || v === false) continue;
      if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
      else if (k === 'style' && typeof v === 'object') Object.assign(node.style, v);
      else if (k === 'html') node.innerHTML = v;
      else if (k === 'text') node.textContent = v;
      else if (!svg && k === 'class') node.className = v;
      else node.setAttribute(k, v === true ? '' : v);
    }
  }
  /** h('div', {class: 'x', onclick: fn}, child, ...) */
  CA.h = function (tag, attrs, ...kids) {
    const node = document.createElement(tag);
    setAttrs(node, attrs, false);
    append(node, kids);
    return node;
  };
  const SVGNS = 'http://www.w3.org/2000/svg';
  CA.s = function (tag, attrs, ...kids) {
    const node = document.createElementNS(SVGNS, tag);
    setAttrs(node, attrs, true);
    append(node, kids);
    return node;
  };
  /** Like Element.append, but flattens nested arrays and skips null/false. */
  CA.append = (node, ...kids) => { append(node, kids); return node; };
  CA.clear = (node) => { while (node.firstChild) node.removeChild(node.firstChild); return node; };
  CA.debounce = (fn, ms) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };
  CA.clamp = (x, a, b) => Math.max(a, Math.min(b, x));

  /* ---------- events ---------- */
  const listeners = {};
  CA.on = (ev, fn) => { (listeners[ev] = listeners[ev] || []).push(fn); return () => CA.off(ev, fn); };
  CA.off = (ev, fn) => { listeners[ev] = (listeners[ev] || []).filter((f) => f !== fn); };
  CA.emit = (ev, ...args) => (listeners[ev] || []).slice().forEach((fn) => {
    try { fn(...args); } catch (e) { CA.reportError(e); }
  });

  /* ---------- storage ---------- */
  CA.store = {
    get(key, def) {
      try { const v = localStorage.getItem('ca.' + key); return v == null ? def : JSON.parse(v); } catch (e) { return def; }
    },
    set(key, val) { try { localStorage.setItem('ca.' + key, JSON.stringify(val)); } catch (e) { /* private mode */ } },
  };

  /* ---------- colour theme ---------- */
  // Colours are written for the dark theme. In the light theme CA.tc() maps each one to a light-theme counterpart:
  // neutrals (backgrounds, lines, text) through a fixed table, and hues by lowering their OKLab lightness, keeping
  // the hue, until they reach 4.5:1 contrast with white. Views take colours through CA.tc(), CA.palette() or the
  // data's .color fields, which are recoloured when the theme changes; style.css has its own light variables.
  const NEUTRAL = {   // dark-theme neutral -> light-theme neutral
    '#000000': '#ffffff', '#0d1117': '#ffffff', '#161b22': '#ffffff', '#1c2230': '#eef1f5', '#28344a': '#dbe7fb',
    '#2a3140': '#e2e7ed', '#30363d': '#d0d7de', '#3a3f4b': '#c4ccd5', '#3d444d': '#b9c1ca', '#6e7681': '#6e7781',
    '#8b949e': '#57606a', '#c9d1d9': '#2f353d', '#e6edf3': '#1f2328', '#ffffff': '#1f2328',
  };
  const hex2 = (n) => Math.round(n).toString(16).padStart(2, '0');
  function parseColor(c) {   // -> [r, g, b (0-255), alpha], or null
    if (typeof c === 'number') return [(c >> 16) & 255, (c >> 8) & 255, c & 255, 1];
    let m = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(c);
    if (m) { const x = m[1].length === 3 ? m[1].replace(/./g, '$&$&') : m[1]; return [0, 2, 4].map((k) => parseInt(x.slice(k, k + 2), 16)).concat(1); }
    m = /^rgba?\(([^)]+)\)$/i.exec(c);
    if (m) { const p = m[1].split(',').map(Number); return p.length >= 3 && p.every((v) => !isNaN(v)) ? [p[0], p[1], p[2], p.length > 3 ? p[3] : 1] : null; }
    return null;
  }
  const lin = (u) => { u /= 255; return u <= 0.04045 ? u / 12.92 : ((u + 0.055) / 1.055) ** 2.4; };
  const unlin = (u) => 255 * (u <= 0.0031308 ? 12.92 * u : 1.055 * u ** (1 / 2.4) - 0.055);
  const contrastWithWhite = (r, g, b) => 1.05 / (0.2126 * r + 0.7152 * g + 0.0722 * b + 0.05);   // linear-light rgb
  function toLab(r, g, b) {
    const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
    const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
    const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
    return [0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s, 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
      0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s];
  }
  function fromLab(L, A, B) {   // -> linear-light rgb, possibly outside the sRGB gamut
    const l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3;
    const m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3;
    const s = (L - 0.0894841775 * A - 1.2914855480 * B) ** 3;
    return [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
      -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s];
  }
  /** Darken a colour (same OKLab hue, chroma clipped to the gamut) until it has 4.5:1 contrast with white. */
  function inkOnWhite([r, g, b]) {
    const c0 = [r, g, b].map(lin);
    if (contrastWithWhite(...c0) >= 4.5) return [r, g, b];
    let [L, A, B] = toLab(...c0);
    const out = (c) => c.some((u) => u < -1e-7 || u > 1 + 1e-7);
    for (let i = 0; i < 200 && L > 0; i++) {
      L -= 0.005;
      let c = fromLab(L, A, B);
      for (let j = 0; j < 200 && out(c); j++) { A *= 0.97; B *= 0.97; c = fromLab(L, A, B); }
      c = c.map((u) => CA.clamp(u, 0, 1));
      if (contrastWithWhite(...c) >= 4.5) return c.map(unlin);
    }
    return [0, 0, 0];
  }
  const tcCache = {};
  /** The current theme's version of a dark-theme colour ('#rrggbb', '#rgb', 'rgb(a)(…)' or a three.js number). */
  CA.tc = (c) => {
    if (CA.theme !== 'light' || c == null) return c;
    const key = typeof c === 'number' ? 'n' + c : String(c).toLowerCase().replace(/\s+/g, '');
    if (key in tcCache) return tcCache[key];
    const rgb = parseColor(key[0] === 'n' ? c : key);
    if (!rgb) return c;
    const hex = '#' + rgb.slice(0, 3).map(hex2).join('');
    const o = NEUTRAL[hex] ? parseColor(NEUTRAL[hex]) : inkOnWhite(rgb);
    const res = typeof c === 'number' ? (Math.round(o[0]) << 16) | (Math.round(o[1]) << 8) | Math.round(o[2])
      : /^rgba?\(/.test(key) ? `rgba(${o.slice(0, 3).map(Math.round).join(',')},${rgb[3]})` : '#' + o.slice(0, 3).map(hex2).join('');
    return (tcCache[key] = res);
  };
  const palettes = [];
  /** A palette (object or array of dark-theme colours) whose values follow the theme; `light`, if given, holds
   *  hand-picked light-theme values (e.g. a categorical set validated for the light surface) instead of CA.tc's. */
  const paletteValue = (base, light, k) => (CA.theme === 'light' && light ? light[k] : CA.tc(base[k]));
  CA.palette = (base, light) => {
    const p = Array.isArray(base) ? [] : {};
    palettes.push([p, base, light]);
    Object.keys(base).forEach((k) => { p[k] = paletteValue(base, light, k); });
    return p;
  };
  const coloured = [];   // data records with a .color: levels, statuses, domains, flatmap overlays and lesion groups
  (function collect(o) {
    if (Array.isArray(o)) { o.forEach(collect); return; }
    if (!o || typeof o !== 'object') return;
    if (typeof o.color === 'string') { o.color0 = o.color; coloured.push(o); }
    Object.values(o).forEach((v) => { if (v && typeof v === 'object') collect(v); });
  })([D.levels, D.statuses, D.domains, D.flatmap]);
  function recolour() {
    coloured.forEach((o) => { o.color = CA.tc(o.color0); });
    palettes.forEach(([p, base, light]) => Object.keys(base).forEach((k) => { p[k] = paletteValue(base, light, k); }));
  }
  CA.theme = document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';   // set early in index.html
  recolour();
  CA.setTheme = (t, keep) => {
    t = t === 'light' ? 'light' : 'dark';
    if (!keep) CA.store.set('theme', t);
    if (t === CA.theme) return;
    CA.theme = t;
    document.documentElement.setAttribute('data-theme', t);
    recolour();
    CA.emit('theme', t);
  };
  // Without a saved choice, follow the system setting as it changes.
  const lightQuery = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)');
  if (lightQuery && lightQuery.addEventListener) {
    lightQuery.addEventListener('change', (e) => { if (CA.store.get('theme') == null) CA.setTheme(e.matches ? 'light' : 'dark', true); });
  }

  /* ---------- where the 3D atlas names its structures: on the model, or in a colour-coded legend at the side ---------- */
  CA.labelMode = CA.store.get('labels', 'model') === 'legend' ? 'legend' : 'model';
  CA.setLabelMode = (m) => {
    m = m === 'legend' ? 'legend' : 'model';
    CA.store.set('labels', m);
    if (m === CA.labelMode) return;
    CA.labelMode = m;
    CA.emit('labels', m);
  };

  /* ---------- brain regions ---------- */
  // Each region brings its own entities, papers, 3D circuits and PubMed query. Untagged entities (shared
  // structures, messengers, functions) belong to every region whose links, chains or questions use them.
  CA.regionById = byId(D.regions);
  CA.regionMembers = Object.fromEntries(D.regions.map((r) => [r.id, new Set(D.regionEntities[r.id] || [])]));
  CA.region = CA.regionById[CA.store.get('region')] || D.regions[0];
  CA.setRegion = (id) => {
    if (!CA.regionById[id] || id === CA.region.id) return;
    CA.region = CA.regionById[id];
    CA.store.set('region', id);
    CA.emit('region', CA.region);
  };
  /** The region dropdown: in the 3D atlas's left panel and at the top left of every other view. */
  CA.regionPicker = () => {
    // regions grouped by animal when there is more than one (`group` on a region; the mammalian regions leave it out)
    const groups = [...new Set(D.regions.map((r) => r.group || 'Mammals'))];
    const opt = (r) => CA.h('option', { value: r.id }, r.label);
    const sel = CA.h('select', { class: 'region-pick', title: 'Brain region: switches the circuits, layouts, queries and papers shown', 'aria-label': 'Brain region',
      onchange: () => { CA.setRegion(sel.value); sel.blur(); } },
    groups.length < 2 ? D.regions.map(opt)
      : groups.map((g) => CA.h('optgroup', { label: g }, D.regions.filter((r) => (r.group || 'Mammals') === g).map(opt))));
    sel.value = CA.region.id;
    return sel;
  };
  CA.on('region', (r) => document.querySelectorAll('select.region-pick').forEach((s) => { s.value = r.id; }));
  CA.inRegion = (id, r) => CA.regionMembers[(r || CA.region).id].has(id);
  CA.regionOf = (id) => (CA.ent[id] && CA.ent[id].region ? CA.regionById[CA.ent[id].region] : null);
  CA.levelDesc = (lv) => (CA.region.levelDesc || {})[lv] || (CA.levelById[lv] || {}).desc || '';
  CA.levelQuery = (lv) => (CA.region.levelQueries || {})[lv] || D.levelQueries[lv];
  CA.methodsFor = (lv) => (CA.region.methods || {})[lv] || D.methods[lv];

  const loaded = {};
  CA.loadScript = (src) => loaded[src] || (loaded[src] = new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = src; s.onload = resolve;
    s.onerror = () => { delete loaded[src]; reject(new Error('Could not load ' + src)); };
    document.head.appendChild(s);
  }));

  /* ---------- citations ---------- */
  CA.lastName = (name) => String(name || '').replace(/\s+[A-Z]{1,4}(\s+(Jr|Sr|II|III|IV))?$/, '');
  CA.shortCite = (p) => {
    if (!p) return '?';
    const a = p.authors || [];
    const who = a.length === 0 ? p.key : a.length === 1 ? CA.lastName(a[0])
      : a.length === 2 ? CA.lastName(a[0]) + ' & ' + CA.lastName(a[1]) : CA.lastName(a[0]) + ' et al.';
    return who + ', ' + (p.year || '');
  };
  CA.fullCite = (p) => {
    const a = p.authors || [];
    const au = a.length > 6 ? a.slice(0, 6).join(', ') + ', et al.' : a.join(', ');
    return `${au} (${p.year}). ${p.title}. ${p.journal}${p.volume ? ' ' + p.volume : ''}${p.pages ? ':' + p.pages : ''}.`
      + (p.pmid ? ' PMID ' + p.pmid + '.' : '') + (p.doi ? ' doi:' + p.doi : '');
  };
  CA.paperUrl = (p) => (p.pmid ? `https://pubmed.ncbi.nlm.nih.gov/${p.pmid}/` : p.doi ? `https://doi.org/${p.doi}` : null);
  CA.pubmedSearchUrl = (term) => 'https://pubmed.ncbi.nlm.nih.gov/?term=' + encodeURIComponent(term);

  /* ---------- reusable widgets ---------- */
  const h = CA.h;
  CA.lvlTag = (lv) => h('span', { class: 'lvl', style: { background: CA.levelColor(lv) } }, CA.levelById[lv] ? CA.levelById[lv].label : lv);
  CA.statusBadge = (status) => {
    const s = CA.statusById[status] || { label: status, color: CA.tc('#8b949e') };
    return h('span', { class: 'badge', title: s.desc || '', style: { color: s.color, borderColor: s.color + '88' } }, s.label);
  };
  CA.evTag = (ev) => h('span', { class: 'ev', title: CA.evidenceById[ev] ? CA.evidenceById[ev].desc : '' }, CA.evidenceById[ev] ? CA.evidenceById[ev].label : ev);
  CA.entChip = (id, opts) => {
    const e = CA.ent[id];
    if (!e) return h('span', { class: 'chip' }, id);
    return h('a', {
      class: 'chip' + (opts && opts.on ? ' on' : ''), href: '#', title: (CA.levelById[e.level] || {}).label + ': ' + e.name,
      onclick: (ev) => { ev.preventDefault(); ev.stopPropagation(); (opts && opts.onclick ? opts.onclick : CA.select)(id); },
    }, h('span', { class: 'dot', style: { background: CA.levelColor(e.level) } }), (opts && opts.label) || e.name);
  };
  CA.citeChips = (refs) => (refs || []).map((k) => {
    const p = CA.paper[k];
    return h('span', {
      class: 'cite', title: p ? p.title : k,
      onclick: (ev) => { ev.stopPropagation(); CA.showPaper(k); },
    }, p ? CA.shortCite(p) : k);
  });
  CA.domainChip = (id, opts) => {
    const d = CA.domainById[id];
    return h('span', { class: 'chip' + (opts && opts.on ? ' on' : ''), onclick: opts && opts.onclick },
      h('span', { class: 'dot', style: { background: d ? d.color : CA.tc('#888888') } }), d ? d.label : id);
  };

  /* ---------- tooltip ---------- */
  let tipEl;
  CA.tip = {
    show(html, ev) {
      tipEl = tipEl || document.getElementById('tooltip');
      tipEl.innerHTML = html;
      tipEl.style.display = 'block';
      CA.tip.move(ev);
    },
    move(ev) {
      if (!tipEl || !ev) return;
      const pad = 14, w = tipEl.offsetWidth, hgt = tipEl.offsetHeight;
      let x = ev.clientX + pad, y = ev.clientY + pad;
      if (x + w > window.innerWidth - 8) x = ev.clientX - w - pad;
      if (y + hgt > window.innerHeight - 8) y = ev.clientY - hgt - pad;
      tipEl.style.left = x + 'px'; tipEl.style.top = y + 'px';
    },
    hide() { if (tipEl) tipEl.style.display = 'none'; },
  };

  /* ---------- selection + detail panel ---------- */
  CA.selected = null;
  let panel, panelBody, panelTitle, history_ = [];
  function panelEls() {
    panel = panel || document.getElementById('panel');
    panelBody = panelBody || document.getElementById('panel-body');
    panelTitle = panelTitle || document.getElementById('panel-kind');
  }
  function openPanel(kind, content, key) {
    panelEls();
    CA.clear(panelBody);
    append(panelBody, [content]);
    panelTitle.textContent = kind;
    panel.classList.add('open');
    panelBody.scrollTop = 0;
    if (key && history_[history_.length - 1] !== key) history_.push(key);
    if (history_.length > 30) history_.shift();
    document.getElementById('panel-back').disabled = history_.length < 2;
  }
  CA.closePanel = () => {
    panelEls();
    panel.classList.remove('open');
    history_ = [];
    if (CA.selected) { CA.selected = null; CA.emit('select', null); }
    setHash(null);
  };
  /** Draw the open panel again (its colours follow the theme). */
  CA.refreshPanel = () => {
    panelEls();
    const top = history_[history_.length - 1];
    if (!panel.classList.contains('open') || !top) return;
    const [kind, id] = top.split(':');
    const scroll = panelBody.scrollTop;
    if (kind === 'e') CA.showEntity(id); else if (kind === 'p') CA.showPaper(id); else if (kind === 'l') CA.showLink(id);
    panelBody.scrollTop = scroll;
  };
  CA.panelBack = () => {
    history_.pop();
    const prev = history_.pop();
    if (!prev) return;
    const [kind, id] = prev.split(':');
    if (kind === 'e') CA.select(id); else if (kind === 'p') CA.showPaper(id); else if (kind === 'l') CA.showLink(id);
  };

  function setHash(part) {
    if (!CA.current) return;
    const h0 = '#/' + CA.current + (part ? '/' + part : '');
    if (location.hash !== h0) history.replaceState(null, '', location.href.split('#')[0] + h0);
  }

  /** Select an entity everywhere: views highlight it and the panel shows its details. */
  CA.select = function (id, opts) {
    if (!CA.ent[id]) return;
    CA.selected = id;
    CA.emit('select', id);
    if (!(opts && opts.noPanel)) CA.showEntity(id);
    setHash('e/' + id);
  };

  function linkRow(l, fromId) {
    const outgoing = l.s === fromId;
    const other = outgoing ? l.t : l.s;
    return h('div', { class: 'conn' },
      h('div', { class: 'arrow', title: outgoing ? 'outgoing' : 'incoming' }, outgoing ? '→' : '←'),
      h('div', {},
        h('div', { class: 'row' }, CA.entChip(other), CA.statusBadge(l.status)),
        h('div', { class: 'rel' },
          h('a', { href: '#', onclick: (ev) => { ev.preventDefault(); CA.showLink(l.id); } }, l.rel), ' ',
          CA.citeChips(l.refs))));
  }

  function paperLine(k) {
    const p = CA.paper[k];
    if (!p) return null;
    return h('div', { class: 'paperline' },
      h('div', { class: 'row' }, h('span', { class: 'cite', onclick: () => CA.showPaper(k) }, CA.shortCite(p)), CA.evTag(p.evidence),
        h('span', { class: 'tiny muted' }, (p.species || []).join(', '))),
      h('div', { class: 'find' }, p.finding));
  }

  CA.showEntity = function (id) {
    const e = CA.ent[id];
    if (!e) return;
    const lv = CA.levelById[e.level];
    const links = CA.linksOf(id).slice().sort((a, b) => CA.rank(b.status) - CA.rank(a.status));
    const byLevel = {};
    links.forEach((l) => {
      const other = CA.ent[l.s === id ? l.t : l.s];
      (byLevel[other.level] = byLevel[other.level] || []).push(l);
    });
    const content = h('div', {},
      h('div', { class: 'row' }, CA.lvlTag(e.level), e.kind ? h('span', { class: 'muted small' }, e.kind) : null),
      h('h2', {}, e.name),
      CA.regionOf(id) && CA.regionOf(id) !== CA.region ? h('div', { class: 'small muted', style: { marginTop: '-4px', marginBottom: '6px' } },
        'Part of the ' + CA.regionOf(id).label.toLowerCase() + ' content. ',
        h('a', { href: '#', onclick: (ev) => { ev.preventDefault(); CA.setRegion(e.region); } }, 'Switch to ' + CA.regionOf(id).label)) : null,
      e.aka && e.aka.length ? h('div', { class: 'small muted', style: { marginTop: '-4px', marginBottom: '8px' } }, 'Also: ' + e.aka.join(', ')) : null,
      h('p', { class: 'summary' }, e.summary),
      e.domains && e.domains.length ? h('div', { class: 'chips' }, e.domains.map((d) => CA.domainChip(d))) : null,
      h('div', { class: 'row', style: { marginTop: '12px' } },
        CA.has3D(id) ? h('button', { class: 'btn', onclick: () => CA.go('atlas', 'e/' + id) }, 'Show in 3D') : null,
        h('button', { class: 'btn', onclick: () => CA.go('scales', 'e/' + id) }, 'Across scales'),
        h('button', { class: 'btn', onclick: () => CA.labAdd(id) }, '+ Hypothesis')),
      h('h4', {}, `Connections (${links.length})`),
      links.length ? D.levels.filter((l) => byLevel[l.id]).map((l) => h('div', {},
        h('div', { class: 'tiny muted', style: { marginTop: '6px' } }, l.label),
        byLevel[l.id].map((lk) => linkRow(lk, id))))
        : h('p', { class: 'muted small' }, 'No curated connections yet; a gap worth exploring.'),
      h('h4', {}, `Key evidence (${(e.refs || []).length})`),
      (e.refs || []).map(paperLine),
      h('p', { class: 'small', style: { marginTop: '12px' } },
        h('a', { href: CA.pubmedSearchUrl(`(${e.name.replace(/[()]/g, '')}) AND ${(CA.regionOf(id) || CA.region).query}`), target: '_blank', rel: 'noopener' }, 'Search PubMed for more ↗')));
    openPanel(lv ? lv.label + ' level' : 'Entity', content, 'e:' + id);
  };

  CA.showPaper = function (key) {
    const p = CA.paper[key];
    if (!p) return;
    const url = CA.paperUrl(p);
    const cited = CA.citedBy[key] || [];
    const content = h('div', {},
      h('div', { class: 'row' }, CA.evTag(p.evidence), h('span', { class: 'small muted' }, (p.species || []).join(', '))),
      h('h2', {}, p.title),
      h('p', { class: 'small muted' }, (p.authors || []).join(', ')),
      h('p', { class: 'small' }, h('i', {}, p.journal), ' ', p.year, p.volume ? `; ${p.volume}` : '', p.pages ? `:${p.pages}` : ''),
      h('div', { class: 'row small' },
        url ? h('a', { href: url, target: '_blank', rel: 'noopener' }, p.pmid ? `PubMed ${p.pmid} ↗` : 'Publisher ↗') : null,
        p.doi ? h('a', { href: 'https://doi.org/' + p.doi, target: '_blank', rel: 'noopener' }, 'DOI ↗') : null,
        p.pmc ? h('a', { href: `https://www.ncbi.nlm.nih.gov/pmc/articles/${p.pmc}/`, target: '_blank', rel: 'noopener' }, 'Free full text ↗') : null),
      h('h4', {}, 'Curated finding'),
      h('p', { class: 'summary' }, p.finding),
      h('div', { class: 'chips' }, (p.levels || []).map((l) => CA.lvlTag(l)), (p.domains || []).map((d) => CA.domainChip(d))),
      p.methods && p.methods.length ? h('p', { class: 'small muted', style: { marginTop: '8px' } }, 'Methods: ' + p.methods.join('; ')) : null,
      h('h4', {}, `Used as evidence for (${cited.length})`),
      cited.map((c) => c.kind === 'entity'
        ? h('div', { style: { margin: '4px 0' } }, CA.entChip(c.id))
        : h('div', { class: 'small', style: { margin: '4px 0' } },
          h('a', { href: '#', onclick: (ev) => { ev.preventDefault(); CA.showLink(c.id); } },
            CA.ent[CA.link[c.id].s].name + ' → ' + CA.ent[CA.link[c.id].t].name), ' ', CA.statusBadge(CA.link[c.id].status))));
    openPanel('Paper', content, 'p:' + key);
    setHash('p/' + key);
  };

  /** Neuromodulatory links carry a transmitter (tx), a receptor (via) and a sign of effect. */
  CA.signGlyph = { '+': '↑', '-': '↓', '±': '±', '~': '~' };
  CA.linkMeta = function (l) {
    const nm = D.neuromodulation || {};
    const parts = [];
    if (l.tx && nm.tx && nm.tx[l.tx]) parts.push(['Transmitter', `${nm.tx[l.tx].label} (${l.tx})`]);
    if (l.via) parts.push(['Receptor', l.via]);
    if (l.sign && nm.signs && nm.signs[l.sign]) parts.push(['Effect', `${CA.signGlyph[l.sign]} ${nm.signs[l.sign]}`]);
    return parts.length ? h('div', { class: 'linkmeta' }, parts.map(([k, v]) => h('span', {}, h('span', { class: 'muted' }, k + ': '), v))) : null;
  };

  CA.showLink = function (id) {
    const l = CA.link[id];
    if (!l) return;
    const st = CA.statusById[l.status];
    const content = h('div', {},
      h('div', { class: 'row' }, CA.statusBadge(l.status), h('span', { class: 'small muted' }, l.kind + ' link')),
      h('h2', { style: { marginTop: '8px' } }, CA.ent[l.s].name, h('span', { class: 'muted' }, ' → '), CA.ent[l.t].name),
      h('p', { class: 'summary' }, l.rel),
      CA.linkMeta(l),
      l.note ? h('p', { class: 'small', style: { borderLeft: '3px solid ' + st.color, paddingLeft: '8px' } }, l.note) : null,
      h('p', { class: 'small muted' }, st.label + ': ' + st.desc),
      h('div', { class: 'row' }, CA.entChip(l.s), h('span', { class: 'muted' }, '→'), CA.entChip(l.t)),
      h('div', { class: 'row', style: { marginTop: '10px' } },
        h('button', { class: 'btn', onclick: () => CA.labAdd([l.s, l.t]) }, 'Build a hypothesis from this link')),
      h('h4', {}, `Evidence (${(l.refs || []).length})`),
      (l.refs || []).map(paperLine));
    openPanel('Connection', content, 'l:' + id);
    setHash('l/' + encodeURIComponent(id));
  };

  CA.showInfo = function (title, node) { openPanel(title, node, null); };

  /** Send entities to the hypothesis lab. */
  CA.labAdd = function (ids) {
    ids = Array.isArray(ids) ? ids : [ids];
    const chain = CA.store.get('lab.chain', []);
    const next = (Array.isArray(ids) && ids.length > 1) ? ids.slice() : chain.concat(ids.filter((x) => chain[chain.length - 1] !== x));
    CA.store.set('lab.chain', next);
    if (CA.current === 'lab') CA.emit('lab-chain', next); else CA.go('lab');
  };

  /* ---------- search ---------- */
  const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  CA.search = function (q, limit) {
    q = norm(q).trim();
    if (!q) return [];
    const res = [];
    D.entities.forEach((e) => {
      const name = norm(e.name), aka = (e.aka || []).map(norm);
      let score = 0;
      if (name === q) score = 100;
      else if (name.startsWith(q)) score = 80;
      else if (aka.some((a) => a === q)) score = 75;
      else if (name.includes(q)) score = 60;
      else if (aka.some((a) => a.includes(q))) score = 50;
      else if (norm(e.summary).includes(q)) score = 20;
      if (score) res.push({ type: 'entity', id: e.id, score, label: e.name,
        sub: (CA.levelById[e.level] || {}).label + (e.region && D.regions.length > 1 ? ' · ' + CA.regionById[e.region].label : '') });
    });
    D.papers.forEach((p) => {
      const hay = norm([p.title, (p.authors || []).join(' '), p.key, p.journal, p.year].join(' '));
      if (hay.includes(q)) res.push({ type: 'paper', id: p.key, score: 10, label: CA.shortCite(p), sub: p.title });
    });
    return res.sort((a, b) => b.score - a.score).slice(0, limit || 12);
  };

  /* ---------- router ---------- */
  CA.register = (id, view) => { view.id = id; CA.views[id] = view; CA.order.push(id); };
  CA.go = (view, sub) => { location.hash = '#/' + view + (sub ? '/' + sub : ''); };
  CA.parseHash = () => {
    const parts = location.hash.replace(/^#\/?/, '').split('/').filter(Boolean).map(decodeURIComponent);
    return { view: parts[0], kind: parts[1], id: parts.slice(2).join('/') };
  };

  function mountView(viewId, r) {
    const root = document.getElementById('view');
    const old = CA.views[CA.current];
    if (old && old.unmount) { try { old.unmount(); } catch (e) { CA.reportError(e); } }
    CA.tip.hide();
    CA.clear(root);
    root.scrollTop = 0;
    CA.current = viewId;
    document.querySelectorAll('#nav a').forEach((a) => a.classList.toggle('active', a.dataset.view === viewId));
    const tab = document.querySelector('#nav a.active');
    if (tab) tab.scrollIntoView({ block: 'nearest', inline: 'nearest' });   // a tab scrolled out of a narrow bar
    document.title = CA.views[viewId].title + ' · ' + D.meta.title;
    regionBar();
    try { CA.views[viewId].mount(root, r); } catch (e) { CA.reportError(e); }
    regionRow(root);
    CA.emit('view-mounted', viewId);
  }

  /** Views without a region dropdown of their own (all but the 3D atlas) get one at the top left of their page head. */
  function regionRow(root) {
    if (D.regions.length < 2 || root.querySelector('select.region-pick')) return;
    const head = root.querySelector('.page-head > div');
    if (head) head.prepend(h('label', { class: 'region-row' }, h('span', {}, 'Region'), CA.regionPicker()));
  }

  /** Views that cover other regions only say so above their content and offer a switch. */
  function regionBar() {
    const bar = document.getElementById('regionbar');
    if (!bar) return;
    const v = CA.current, off = v && !CA.region.views.includes(v);
    document.querySelectorAll('#nav a').forEach((a) => a.classList.toggle('offregion', !CA.region.views.includes(a.dataset.view)));
    document.body.classList.toggle('regionbar-on', !!off);
    CA.clear(bar);
    if (!off) return;
    const homes = D.regions.filter((x) => x.views.includes(v));
    CA.append(bar, h('span', {}, `${CA.views[v].title} covers ${homes.map((x) => 'the ' + x.label.toLowerCase()).join(' and ')} only; `
      + `there is nothing here on the ${CA.region.label.toLowerCase()} yet.`),
    homes.map((x) => h('button', { class: 'btn', onclick: () => CA.setRegion(x.id) }, 'Switch to ' + x.label)));
  }

  // On a region change, a view with onRegion() updates in place; any other view is mounted again.
  CA.on('region', () => {
    const v = CA.views[CA.current];
    if (!v) return;
    regionBar();
    if (v.onRegion) { try { v.onRegion(CA.region); } catch (e) { CA.reportError(e); } } else mountView(CA.current, CA.parseHash());
  });

  // On a theme change, a view with onTheme() recolours in place; any other view is mounted again.
  CA.on('theme', () => {
    CA.refreshPanel();
    const v = CA.views[CA.current];
    if (!v) return;
    if (v.onTheme) { try { v.onTheme(CA.theme); } catch (e) { CA.reportError(e); } } else mountView(CA.current, CA.parseHash());
  });

  CA.route = function () {
    const r = CA.parseHash();
    const viewId = CA.views[r.view] ? r.view : CA.order[0];
    if (viewId !== CA.current) {
      mountView(viewId, r);
    } else if (CA.views[viewId].route) {
      CA.views[viewId].route(r);
    }
    if (r.kind === 'e' && CA.ent[r.id]) CA.select(r.id);
    else if (r.kind === 'p' && CA.paper[r.id]) CA.showPaper(r.id);
    else if (r.kind === 'l' && CA.link[r.id]) CA.showLink(r.id);
  };

  CA.reportError = function (e) {
    console.error(e);
    const bar = document.getElementById('errbar');
    if (!bar) return;
    bar.textContent = 'Something went wrong: ' + (e && e.message ? e.message : e) + '\n(see the browser console for details)';
    bar.style.display = 'block';
  };
})();
