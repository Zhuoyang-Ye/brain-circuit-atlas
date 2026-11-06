/* Evidence & gaps: where the literature on the current region is dense or thin, by function domain × level of analysis. */
(function () {
  'use strict';
  const CA = window.CA, D = CA.D, h = CA.h;
  const ESEARCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi';
  let root, mode = CA.store.get('gaps.mode', 'curated'), sel = null, table, side, progress, fetchBtn, cacheNote, helpEl, aborted = false;
  let pm = null;    // {date, counts: {key: n}}, stored per region
  let CUR = {}, PAPERS = [];
  const pmKey = () => 'gaps.pubmed' + (CA.region === D.regions[0] ? '' : '.' + CA.region.id);

  CA.register('gaps', { title: 'Evidence & gaps', mount, unmount });

  /* ---------- counts ---------- */
  function curated() {
    const c = {};
    PAPERS.forEach((p) => (p.domains || []).forEach((d) => (p.levels || []).forEach((l) => {
      const k = d + '|' + l; (c[k] = c[k] || []).push(p.key);
    })));
    return c;
  }
  const curCount = (d, l) => (CUR[d + '|' + l] || []).length;
  const qTerm = (d, l) => [CA.region.query, d ? CA.domainById[d].q : null, l ? CA.levelQuery(l) : null].filter(Boolean).join(' AND ');
  const pmCount = (d, l) => (pm && pm.counts) ? pm.counts[(d || '*') + '|' + (l || '*')] : undefined;

  function cellValue(d, l) {
    if (mode === 'curated') return { v: curCount(d, l), text: String(curCount(d, l)) };
    const n = pmCount(d, l);
    if (n == null) return { v: null, text: '…' };
    if (mode === 'pubmed') return { v: n, text: n >= 1000 ? (n / 1000).toFixed(n >= 10000 ? 0 : 1) + 'k' : String(n) };
    const tot = pmCount(null, null), row = pmCount(d, null), col = pmCount(null, l);
    if (!tot || !row || !col) return { v: null, text: '…' };
    const ratio = n / (row * col / tot);
    return { v: ratio, text: '×' + (ratio >= 10 ? ratio.toFixed(0) : ratio.toFixed(ratio < 1 ? 2 : 1)) };
  }

  function cellStyle(d, l, v) {
    if (v == null) return { background: CA.tc('#161b22') };
    if (mode === 'ratio') {
      const x = CA.clamp(Math.log2(v) / 2, -1, 1);
      return x < 0 ? { background: `rgba(255,123,114,${0.15 + 0.6 * -x})` } : { background: `rgba(88,166,255,${0.15 + 0.6 * x})` };
    }
    const max = mode === 'curated' ? Math.max(1, ...D.domains.flatMap((dd) => D.levels.map((ll) => curCount(dd.id, ll.id))))
      : Math.max(1, ...D.domains.flatMap((dd) => D.levels.map((ll) => pmCount(dd.id, ll.id) || 0)));
    const k = mode === 'curated' ? v / max : Math.log10(1 + v) / Math.log10(1 + max);
    return { background: `rgba(63,185,165,${v ? 0.12 + 0.7 * k : 0})` };
  }

  /* ---------- live PubMed counts ---------- */
  async function fetchCounts() {
    const key = pmKey();
    const jobs = [[null, null], ...D.domains.map((d) => [d.id, null]), ...D.levels.map((l) => [null, l.id]),
      ...D.domains.flatMap((d) => D.levels.map((l) => [d.id, l.id]))];
    const counts = {};
    aborted = false;
    fetchBtn.disabled = true;
    for (let i = 0; i < jobs.length; i++) {
      if (aborted) return;
      const [d, l] = jobs[i];
      const term = qTerm(d, l);
      let n = null, wasCached = false;
      if (CA.hasBackend) {
        try {
          const r = await fetch(`/api/pubmed/count?term=${encodeURIComponent(term)}`);
          if (r.ok) {
            const data = await r.json();
            n = data.count;
            wasCached = data.cached;
          }
        } catch (e) {}
      }
      if (n == null) {
        const url = `${ESEARCH}?db=pubmed&rettype=count&retmode=json&tool=brain-circuit-atlas&term=${encodeURIComponent(term)}`;
        for (let attempt = 0; attempt < 3 && n == null; attempt++) {
          try {
            const r = await fetch(url);
            if (r.ok) n = +(await r.json()).esearchresult.count;
            else await sleep(1500);
          } catch (e) { await sleep(1500); }
        }
      }
      if (n == null) { cacheNote.textContent = 'PubMed did not respond; try again later.'; fetchBtn.disabled = false; return; }
      counts[(d || '*') + '|' + (l || '*')] = n;
      progress.firstChild.style.width = ((i + 1) / jobs.length * 100) + '%';
      if (!wasCached) await sleep(360);   // stay under NCBI's limit of 3 requests per second only for live fetches
    }
    pm = { date: new Date().toISOString().slice(0, 10), counts };
    CA.store.set(key, pm);
    fetchBtn.disabled = false;
    fetchBtn.textContent = 'Refresh PubMed counts';
    cacheNote.textContent = `counts from ${pm.date}`;
    renderTable();
    renderSide();
  }
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  /* ---------- view ---------- */
  function mount(node) {
    root = node;
    sel = null;
    pm = CA.store.get(pmKey(), null);
    PAPERS = D.papers.filter((p) => p.regions.includes(CA.region.id));
    CUR = curated();
    const R = CA.region;
    const seg = h('div', { class: 'seg' }, [['curated', 'Curated papers'], ['pubmed', 'PubMed counts'], ['ratio', 'Relative coverage']].map(([k, l]) => h('button', {
      class: k === mode ? 'on' : '', 'data-m': k,
      onclick: () => { mode = k; CA.store.set('gaps.mode', k); seg.querySelectorAll('button').forEach((b) => b.classList.toggle('on', b.dataset.m === k)); renderTable(); renderSide(); },
    }, l)));
    fetchBtn = h('button', { class: 'btn', onclick: fetchCounts }, pm ? 'Refresh PubMed counts' : 'Fetch PubMed counts');
    progress = h('div', { class: 'progress', style: { width: '160px' } }, h('i', { style: { width: pm ? '100%' : '0' } }));
    cacheNote = h('span', { class: 'small muted' }, pm ? `counts from ${pm.date}` : '~100 queries, about 40 s');
    table = h('div', { style: { overflowX: 'auto' } });
    side = h('div', {});
    root.appendChild(h('div', { class: 'page' },
      h('div', { class: 'page-head' }, h('div', {},
        h('h2', {}, 'Evidence & gaps'),
        h('p', {}, `Literature on the ${R.label.toLowerCase()}: rows are functional domains, columns are levels of analysis. Thin cells, especially relative to their row and column, mark places where mechanisms are not yet connected across scales: candidate questions for new research.`))),
      h('div', { class: 'card' },
        h('div', { class: 'row' }, seg, h('span', { class: 'grow' }), fetchBtn, progress, cacheNote),
        helpEl = h('p', { class: 'small muted', style: { margin: '8px 0 0' } }, modeHelp())),
      h('div', { class: 'cols', style: { gridTemplateColumns: 'minmax(0, 1fr) 340px', marginTop: '14px' } }, h('div', { class: 'card' }, table), side),
      h('h3', { style: { marginTop: '28px' } }, 'Weakest links in the knowledge graph'),
      h('p', { class: 'small muted' }, 'Proposed, debated or single-study connections. Each is a ready-made experiment.'),
      h('div', { class: 'card' }, weakLinks()),
      h('h3', { style: { marginTop: '28px' } }, 'Open questions'),
      h('div', {}, D.questions.filter((q) => q.regions.includes(R.id)).map((q) => h('div', { class: 'qcard', onclick: () => { CA.store.set('lab.question', q.id); CA.go('lab'); } },
        h('b', {}, q.title), h('span', { class: 'small muted' }, q.text))))));
    renderTable();
    renderSide();
  }
  function unmount() { aborted = true; }

  function modeHelp() {
    const R = CA.region;
    return mode === 'curated' ? `Papers on the ${R.label.toLowerCase()} in this site's curated library, tagged with each domain and level. Small by design: it shows what the atlas covers, not the field.`
      : mode === 'pubmed' ? `Live PubMed counts for ${R.query} AND domain terms AND level terms (title/abstract keyword queries; approximate).`
        : `Observed ÷ expected PubMed count, where expected = row total × column total ÷ all ${R.label.toLowerCase()} papers. Red = fewer papers than the row and column would predict.`;
  }

  function renderTable() {
    if (!table) return;
    if (helpEl) helpEl.textContent = modeHelp();
    CA.clear(table);
    const needPm = mode !== 'curated' && !pm;
    if (needPm) {
      table.append(h('p', { class: 'muted' }, 'Fetch PubMed counts to use this mode. Queries go straight from your browser to NCBI E-utilities.'));
      return;
    }
    const t = h('table', { class: 'matrix' },
      h('tr', {}, h('th', {}), D.levels.map((l) => h('th', { style: { color: l.color } }, l.label)),
        mode !== 'ratio' ? h('th', {}, 'Total') : null));
    D.domains.forEach((d) => {
      t.appendChild(h('tr', {},
        h('th', { class: 'rowh' }, h('span', { class: 'row', style: { justifyContent: 'flex-end' } }, d.label, h('span', { class: 'dot', style: { background: d.color } }))),
        D.levels.map((l) => {
          const c = cellValue(d.id, l.id);
          const td = h('td', {
            class: (c.v === 0 ? 'zero' : '') + (sel && sel.d === d.id && sel.l === l.id ? ' sel' : ''),
            style: cellStyle(d.id, l.id, c.v), title: `${d.label} × ${l.label}`,
            onclick: () => { sel = { d: d.id, l: l.id }; renderTable(); renderSide(); },
          }, c.text);
          return td;
        }),
        mode !== 'ratio' ? h('td', { class: 'muted', style: { cursor: 'default' } },
          mode === 'curated' ? String(PAPERS.filter((p) => (p.domains || []).includes(d.id)).length) : String(pmCount(d.id, null) || '')) : null));
    });
    table.appendChild(t);
  }

  function renderSide() {
    if (!side) return;
    CA.clear(side);
    if (!sel) {
      side.append(h('div', { class: 'card' }, h('h3', {}, 'Pick a cell'),
        h('p', { class: 'small' }, 'See the curated papers behind it, the PubMed query, the entities involved, and untested bridges between levels for that domain.'),
        h('p', { class: 'small muted' }, 'Dashed cells have no curated paper yet.')));
      return;
    }
    const d = CA.domainById[sel.d], l = CA.levelById[sel.l];
    const keys = CUR[sel.d + '|' + sel.l] || [];
    const n = pmCount(sel.d, sel.l);
    const ents = D.entities.filter((e) => e.level === sel.l && (e.domains || []).includes(sel.d) && CA.inRegion(e.id));
    side.append(h('div', { class: 'card' },
      h('h3', {}, d.label, h('span', { class: 'muted' }, ' × '), l.label),
      h('p', { class: 'small' }, `${keys.length} curated paper(s)` + (n != null ? ` · ${n.toLocaleString()} PubMed hits` : '')),
      h('a', { class: 'small', href: CA.pubmedSearchUrl(qTerm(sel.d, sel.l)), target: '_blank', rel: 'noopener' }, 'Open this query in PubMed ↗'),
      h('h4', {}, 'Curated papers'),
      keys.length ? h('div', {}, CA.citeChips(keys)) : h('p', { class: 'small muted' }, 'None yet. A candidate for curation or new work.'),
      h('h4', {}, `Entities (${ents.length})`),
      ents.length ? h('div', { class: 'chips' }, ents.map((e) => CA.entChip(e.id))) : h('p', { class: 'small muted' }, 'No entity at this level is tagged with this domain.'),
      h('h4', {}, 'Untested bridges'),
      bridges(sel.d)));
  }

  /** Entity pairs in one domain, one or two levels apart, with no direct link and no two-step path. */
  function bridges(domain) {
    const ents = D.entities.filter((e) => (e.domains || []).includes(domain) && CA.inRegion(e.id));
    const cands = [];
    ents.forEach((a) => ents.forEach((b) => {
      const la = CA.levelById[a.level].index, lb = CA.levelById[b.level].index;
      if (!(lb > la && lb - la <= 2)) return;
      if (CA.linkBetween(a.id, b.id)) return;
      const na = CA.neighbors(a.id), nb = CA.neighbors(b.id);
      if ([...na].some((x) => nb.has(x))) return;
      cands.push({ a: a.id, b: b.id, score: na.size + nb.size });
    }));
    cands.sort((x, y) => y.score - x.score);
    if (!cands.length) return h('p', { class: 'small muted' }, 'Every pair is already linked directly or through one intermediate.');
    return h('div', {}, cands.slice(0, 8).map((c) => h('div', { class: 'suggest' },
      h('div', { class: 'row' }, CA.entChip(c.a), h('span', { class: 'muted' }, '→'), CA.entChip(c.b)),
      h('button', { class: 'btn ghost small', onclick: () => CA.labAdd([c.a, c.b]) }, 'Draft'))));
  }

  function weakLinks() {
    const weak = D.links.filter((l) => ['hypothesis', 'debated', 'emerging'].includes(l.status) && l.regions.includes(CA.region.id))
      .sort((a, b) => CA.rank(a.status) - CA.rank(b.status) || (a.refs || []).length - (b.refs || []).length);
    return h('table', { class: 'data' },
      h('tr', {}, h('th', {}, 'Status'), h('th', {}, 'From'), h('th', {}, 'To'), h('th', {}, 'Claim'), h('th', {}, 'Evidence'), h('th', {})),
      weak.map((l) => h('tr', { class: 'click', onclick: () => CA.showLink(l.id) },
        h('td', {}, CA.statusBadge(l.status)), h('td', {}, CA.entChip(l.s)), h('td', {}, CA.entChip(l.t)),
        h('td', { class: 'small' }, l.rel), h('td', {}, CA.citeChips(l.refs)),
        h('td', {}, h('button', { class: 'btn ghost small', onclick: (ev) => { ev.stopPropagation(); CA.labAdd([l.s, l.t]); } }, 'Test')))));
  }
})();
