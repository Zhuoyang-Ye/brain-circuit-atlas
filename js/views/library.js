/* Library: every paper behind the atlas, filterable by region, level, domain, evidence type, species and year. */
(function () {
  'use strict';
  const CA = window.CA, D = CA.D, h = CA.h, s = CA.s;
  // Categorical slots validated for CVD separation and contrast on the dark surfaces (fixed order = D.evidence order).
  const EV_COLORS = ['#3987e5', '#d95926', '#199e70', '#c98500', '#d55181', '#008300'];
  const evColor = (id) => EV_COLORS[D.evidence.findIndex((e) => e.id === id)] || '#8b949e';
  const YEARS = D.papers.map((p) => +p.year).filter(Boolean);
  const YMIN = Math.min(...YEARS), YMAX = Math.max(...YEARS);
  const SORTS = { 'year-desc': 'Newest first', 'year-asc': 'Oldest first', cited: 'Most used in the atlas', author: 'First author A–Z' };
  let root, f, els = {};

  CA.register('library', { title: 'Library', mount, unmount() {} });
  CA.evColor = evColor;

  const defaults = () => ({ q: '', allRegions: false, levels: [], domains: [], ev: D.evidence.map((e) => e.id), species: [], y0: YMIN, y1: YMAX, sort: 'year-desc' });
  const pool = () => (f.allRegions ? D.papers : D.papers.filter((p) => p.regions.includes(CA.region.id)));
  const usage = (k) => (CA.citedBy[k] || []).length;

  function mount(node) {
    root = node;
    const saved = CA.store.get('library.filters', {});
    if (!saved.v) { delete saved.y0; delete saved.y1; }  // saved before year bounds were stored open-ended
    f = Object.assign(defaults(), saved);
    // An open-ended year range is stored as null, so newly added years stay visible.
    if (f.y0 == null || f.y0 < YMIN) f.y0 = YMIN;
    if (f.y1 == null || f.y1 > YMAX) f.y1 = YMAX;
    els.list = h('div', {});
    els.count = h('span', { class: 'small muted' });
    els.stack = h('div', { class: 'stack', style: { height: '14px', gap: '2px', background: 'transparent' } });
    els.legend = h('div', { class: 'row tiny', style: { marginTop: '8px', gap: '4px 14px' } });
    els.hist = h('div', {});
    els.filters = h('div', {});
    els.intro = h('p', {});
    root.appendChild(h('div', { class: 'page' },
      h('div', { class: 'page-head' },
        h('div', {}, h('h2', {}, 'Library'), els.intro),
        h('div', { class: 'row' }, h('button', { class: 'btn', onclick: exportBib, title: 'BibTeX for the papers currently shown' }, 'Export .bib'))),
      h('div', { class: 'cols' },
        h('div', { class: 'card' }, els.filters),
        h('div', {},
          h('div', { class: 'card' },
            h('div', { class: 'row', style: { justifyContent: 'space-between', marginBottom: '8px' } }, h('h3', { style: { margin: 0 } }, 'Evidence type'), els.count),
            els.stack, els.legend,
            h('h3', { style: { marginTop: '16px' } }, 'Publication year ', h('span', { class: 'small muted' }, '(papers shown, 5-year bins)')),
            els.hist),
          h('div', { style: { marginTop: '12px' } }, els.list)))));
    renderFilters();
    render();
  }

  function save() { CA.store.set('library.filters', Object.assign({}, f, { v: 2, y0: f.y0 === YMIN ? null : f.y0, y1: f.y1 === YMAX ? null : f.y1 })); }
  function toggle(arr, v) { const i = arr.indexOf(v); if (i >= 0) arr.splice(i, 1); else arr.push(v); }
  function update() { save(); renderFilters(); render(); }

  /* ---------- filters ---------- */
  function renderFilters() {
    const box = CA.clear(els.filters);
    const q = h('input', { class: 'text', type: 'search', placeholder: 'Title, author, finding, PMID…', style: { width: '100%' } });
    q.value = f.q;
    q.addEventListener('input', CA.debounce(() => { f.q = q.value; save(); render(); }, 150));
    const evCount = {}, spCount = {};
    pool().forEach((p) => { evCount[p.evidence] = (evCount[p.evidence] || 0) + 1; (p.species || []).forEach((x) => { spCount[x] = (spCount[x] || 0) + 1; }); });
    const species = Object.keys(spCount).sort((a, b) => spCount[b] - spCount[a]);
    const y0 = h('input', { type: 'range', min: YMIN, max: YMAX, value: f.y0, style: { width: '100%' } });
    const y1 = h('input', { type: 'range', min: YMIN, max: YMAX, value: f.y1, style: { width: '100%' } });
    const ylab = h('span', { class: 'small' }, `${f.y0}–${f.y1}`);
    const onYear = () => {
      f.y0 = Math.min(+y0.value, +y1.value); f.y1 = Math.max(+y0.value, +y1.value);
      ylab.textContent = `${f.y0}–${f.y1}`; save(); render();
    };
    y0.addEventListener('input', onYear); y1.addEventListener('input', onYear);
    const others = D.papers.length - D.papers.filter((p) => p.regions.includes(CA.region.id)).length;
    CA.append(box,
      q,
      D.regions.length > 1 ? h('label', { class: 'check small', style: { marginTop: '10px' }, title: `Only papers on the ${CA.region.label.toLowerCase()} are listed unless this is ticked` },
        h('input', { type: 'checkbox', checked: f.allRegions, onchange: () => { f.allRegions = !f.allRegions; update(); } }),
        'Include other regions', h('span', { class: 'muted' }, ` +${others}`)) : null,
      h('h4', {}, 'Level'),
      h('div', { class: 'chips' }, D.levels.map((l) => h('span', { class: 'chip' + (f.levels.includes(l.id) ? ' on' : ''), onclick: () => { toggle(f.levels, l.id); update(); } },
        h('span', { class: 'dot', style: { background: l.color } }), l.label))),
      h('h4', {}, 'Domain'),
      h('div', { class: 'chips' }, D.domains.map((d) => CA.domainChip(d.id, { on: f.domains.includes(d.id), onclick: () => { toggle(f.domains, d.id); update(); } }))),
      h('h4', {}, 'Evidence type'),
      D.evidence.map((e) => h('label', { class: 'check small', title: e.desc || '' },
        h('input', { type: 'checkbox', checked: f.ev.includes(e.id), onchange: () => { toggle(f.ev, e.id); save(); render(); } }),
        h('span', { class: 'dot', style: { background: evColor(e.id), borderRadius: '2px' } }), e.label, h('span', { class: 'muted' }, ` ${evCount[e.id] || 0}`))),
      h('h4', {}, 'Species'),
      h('div', { class: 'chips' }, species.map((x) => h('span', { class: 'chip' + (f.species.includes(x) ? ' on' : ''), onclick: () => { toggle(f.species, x); update(); } },
        x, h('span', { class: 'muted' }, String(spCount[x]))))),
      h('h4', {}, 'Years ', ylab),
      y0, y1,
      h('h4', {}, 'Sort'),
      h('select', { style: { width: '100%' }, onchange: (ev) => { f.sort = ev.target.value; save(); render(); } },
        Object.entries(SORTS).map(([k, v]) => h('option', { value: k, selected: f.sort === k }, v))),
      h('div', { class: 'row', style: { marginTop: '14px' } }, h('button', { class: 'btn ghost', onclick: () => { f = defaults(); update(); } }, 'Reset filters')),
      h('p', { class: 'tiny muted', style: { marginTop: '14px' } },
        'Within a group, filters combine with OR; across groups, with AND. The library is a curated core, not a systematic review: use Evidence & gaps for live PubMed counts.'));
  }

  function matches(p) {
    if (f.levels.length && !(p.levels || []).some((l) => f.levels.includes(l))) return false;
    if (f.domains.length && !(p.domains || []).some((d) => f.domains.includes(d))) return false;
    if (!f.ev.includes(p.evidence)) return false;
    if (f.species.length && !(p.species || []).some((x) => f.species.includes(x))) return false;
    const y = +p.year;
    if (y < f.y0 || y > f.y1) return false;
    if (f.q) {
      const hay = [p.key, p.pmid, p.title, (p.authors || []).join(' '), p.journal, p.finding, (p.methods || []).join(' ')].join(' ').toLowerCase();
      if (!f.q.toLowerCase().split(/\s+/).filter(Boolean).every((w) => hay.includes(w))) return false;
    }
    return true;
  }

  function sorted(list) {
    const first = (p) => CA.lastName((p.authors || [p.key])[0]).toLowerCase();
    const cmp = {
      'year-desc': (a, b) => b.year - a.year || first(a).localeCompare(first(b)),
      'year-asc': (a, b) => a.year - b.year || first(a).localeCompare(first(b)),
      cited: (a, b) => usage(b.key) - usage(a.key) || b.year - a.year,
      author: (a, b) => first(a).localeCompare(first(b)) || a.year - b.year,
    }[f.sort] || (() => 0);
    return list.slice().sort(cmp);
  }

  /* ---------- summary charts ---------- */
  function renderStack(list) {
    CA.clear(els.stack); CA.clear(els.legend);
    const n = list.length;
    D.evidence.forEach((e) => {
      const k = list.filter((p) => p.evidence === e.id).length;
      if (k) {
        const seg = h('i', { style: { flexGrow: k, background: evColor(e.id), cursor: 'pointer' } });
        seg.addEventListener('mousemove', (ev) => CA.tip.show(`<b>${CA.esc(e.label)}</b><br>${k} paper${k === 1 ? '' : 's'} (${Math.round(100 * k / n)}%)<br><span class="muted">${CA.esc(e.desc || '')}</span>`, ev));
        seg.addEventListener('mouseleave', () => CA.tip.hide());
        seg.addEventListener('click', () => { f.ev = f.ev.length === 1 && f.ev[0] === e.id ? D.evidence.map((x) => x.id) : [e.id]; CA.tip.hide(); update(); });
        els.stack.appendChild(seg);
      }
      els.legend.appendChild(h('span', { class: 'row', style: { gap: '5px', opacity: k ? 1 : 0.45 } },
        h('span', { class: 'dot', style: { background: evColor(e.id), borderRadius: '2px' } }), e.label, h('span', { class: 'muted' }, String(k))));
    });
    if (!n) els.stack.appendChild(h('i', { style: { flexGrow: 1, background: 'var(--bg3)' } }));
  }

  function renderHist(list) {
    CA.clear(els.hist);
    const b0 = Math.floor(YMIN / 5) * 5, b1 = Math.floor(YMAX / 5) * 5;
    const bins = [];
    for (let y = b0; y <= b1; y += 5) bins.push({ y, n: 0 });
    list.forEach((p) => { const b = bins[Math.floor((+p.year - b0) / 5)]; if (b) b.n++; });
    const W = 720, H = 120, PL = 26, PB = 20, PT = 8;
    const max = Math.max(4, ...bins.map((b) => b.n));
    const bw = (W - PL) / bins.length;
    const yv = (v) => H - PB - (v / max) * (H - PB - PT);
    const svg = s('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: { display: 'block', maxHeight: '150px' }, role: 'img', 'aria-label': 'Histogram of publication years' });
    const step = [1, 2, 5, 10, 20, 50, 100].find((k) => max / k <= 4) || 200;  // at most ~4 gridlines
    for (let v = 0; v <= max; v += step) {
      svg.appendChild(s('line', { x1: PL, x2: W, y1: yv(v), y2: yv(v), stroke: '#30363d', 'stroke-width': 1 }));
      svg.appendChild(s('text', { x: PL - 6, y: yv(v) + 3.5, 'text-anchor': 'end', 'font-size': 10, fill: '#8b949e' }, String(v)));
    }
    bins.forEach((b, i) => {
      const x = PL + i * bw + 1, w = bw - 2;
      if (b.n) {
        const top = yv(b.n), base = yv(0), r = Math.min(4, w / 2, base - top);
        svg.appendChild(s('path', { d: `M${x},${base} V${top + r} Q${x},${top} ${x + r},${top} H${x + w - r} Q${x + w},${top} ${x + w},${top + r} V${base} Z`, fill: '#3987e5' }));
      }
      if (b.y % 10 === 0) svg.appendChild(s('text', { x: x + w / 2, y: H - 5, 'text-anchor': 'middle', 'font-size': 10, fill: '#8b949e' }, String(b.y)));
      const hit = s('rect', { x: PL + i * bw, y: PT, width: bw, height: H - PB - PT, fill: 'transparent', style: { cursor: b.n ? 'pointer' : 'default' } });
      hit.addEventListener('mousemove', (ev) => CA.tip.show(`<b>${b.y}–${b.y + 4}</b><br>${b.n} paper${b.n === 1 ? '' : 's'}${b.n ? '<br><span class="muted">click to filter to these years</span>' : ''}`, ev));
      hit.addEventListener('mouseleave', () => CA.tip.hide());
      hit.addEventListener('click', () => { if (!b.n) return; f.y0 = Math.max(YMIN, b.y); f.y1 = Math.min(YMAX, b.y + 4); CA.tip.hide(); update(); });
      svg.appendChild(hit);
    });
    svg.appendChild(s('line', { x1: PL, x2: W, y1: yv(0), y2: yv(0), stroke: '#6e7681', 'stroke-width': 1 }));
    els.hist.appendChild(svg);
  }

  /* ---------- list ---------- */
  function card(p) {
    const url = CA.paperUrl(p);
    const recs = CA.citedBy[p.key] || [];
    const ents = [...new Set(recs.filter((r) => r.kind === 'entity').map((r) => r.id))];
    const nLinks = recs.filter((r) => r.kind === 'link').length;
    const ev = CA.evidenceById[p.evidence];
    return h('div', { class: 'pcard' },
      h('div', { class: 'row meta' },
        h('b', { style: { color: 'var(--text)' } }, CA.shortCite(p)), h('i', {}, p.journal),
        h('span', { class: 'ev', title: ev ? ev.desc : '' }, h('span', { class: 'dot', style: { background: evColor(p.evidence), borderRadius: '2px', marginRight: '5px', width: '8px', height: '8px' } }), ev ? ev.label : p.evidence),
        (p.species || []).length ? h('span', {}, p.species.join(', ')) : null),
      h('div', { class: 't', onclick: () => CA.showPaper(p.key) }, p.title),
      h('div', { class: 'small', style: { color: '#c9d1d9' } }, p.finding),
      h('div', { class: 'row', style: { marginTop: '8px' } },
        (p.levels || []).map((l) => CA.lvlTag(l)),
        h('span', { class: 'grow' }),
        url ? h('a', { class: 'small', href: url, target: '_blank', rel: 'noopener' }, p.pmid ? 'PubMed ↗' : 'Source ↗') : null,
        p.doi ? h('a', { class: 'small', href: 'https://doi.org/' + p.doi, target: '_blank', rel: 'noopener' }, 'DOI ↗') : null,
        p.pmc ? h('a', { class: 'small', href: `https://www.ncbi.nlm.nih.gov/pmc/articles/${p.pmc}/`, target: '_blank', rel: 'noopener' }, 'Full text ↗') : null),
      ents.length || nLinks ? h('div', { class: 'row', style: { marginTop: '8px' } },
        h('span', { class: 'tiny muted' }, 'Evidence for:'), ents.slice(0, 8).map((id) => CA.entChip(id)),
        ents.length > 8 ? h('span', { class: 'tiny muted' }, `+${ents.length - 8}`) : null,
        nLinks ? h('span', { class: 'tiny muted' }, `${ents.length ? '· ' : ''}${nLinks} connection${nLinks === 1 ? '' : 's'}`) : null) : null);
  }

  function render() {
    const all = pool(), list = sorted(all.filter(matches));
    els.intro.textContent = `The ${all.length} publications ${f.allRegions ? '' : 'on the ' + CA.region.label.toLowerCase() + ' '}behind every entity, connection and map score, `
      + 'with metadata verified against PubMed. Each card states the finding the atlas relies on.';
    els.count.textContent = `${list.length} of ${all.length} papers`;
    renderStack(list);
    renderHist(list);
    CA.clear(els.list);
    if (!list.length) {
      els.list.append(h('div', { class: 'card' }, h('p', { class: 'muted', style: { margin: 0 } }, 'No papers match these filters. '),
        h('a', { href: CA.pubmedSearchUrl(f.q ? `(${f.q}) AND ${CA.region.query}` : CA.region.query), target: '_blank', rel: 'noopener' }, 'Search PubMed instead ↗')));
      return;
    }
    list.forEach((p) => els.list.appendChild(card(p)));
  }

  /* ---------- export ---------- */
  function bibAuthor(a) { const m = /^(.*\S)\s+([A-Z]{1,4})$/.exec(a); return m ? `${m[1]}, ${m[2].split('').join('. ')}.` : a; }
  function exportBib() {
    const esc = (t) => String(t || '').replace(/[{}]/g, '');
    const bib = sorted(pool().filter(matches)).map((p) => {
      const fields = [
        ['author', (p.authors || []).map(bibAuthor).join(' and ')], ['title', `{${esc(p.title).replace(/\.$/, '')}}`], ['journal', esc(p.journal)],
        ['year', p.year], ['volume', p.volume], ['pages', (p.pages || '').replace('-', '--')], ['doi', p.doi], ['pmid', p.pmid],
        ['note', p.finding ? D.meta.title + ': ' + esc(p.finding) : ''],
      ].filter(([, v]) => v);
      return `@article{${p.key},\n` + fields.map(([k, v]) => `  ${k} = {${v}}`).join(',\n') + '\n}';
    }).join('\n\n');
    const a = h('a', { href: URL.createObjectURL(new Blob([bib + '\n'], { type: 'application/x-bibtex' })), download: D.meta.title.toLowerCase().replace(/\W+/g, '-') + '.bib' });
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }
})();
