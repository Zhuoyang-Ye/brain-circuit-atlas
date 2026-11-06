/* Hypothesis lab: chain entities across levels, see the evidence for each step, and draft a testable hypothesis. */
(function () {
  'use strict';
  const CA = window.CA, D = CA.D, h = CA.h;
  let root, chain = [], questionId = null, notes = '', els = {}, unsub = null;

  CA.register('lab', { title: 'Hypothesis lab', mount, unmount });

  const name = (id) => (CA.ent[id] ? CA.ent[id].name : id);
  const lvl = (id) => CA.ent[id].level;
  const cap = (t) => (/^[a-z]+[A-Z0-9]/.test(t) ? t : t.charAt(0).toUpperCase() + t.slice(1)); // leaves "mGluR1" alone
  // lower-case a method name for mid-sentence use, but keep acronyms and proper nouns ("CCAS scale", "Neuropixels")
  const lc = (t) => (/^(\S[A-Z]|Neuropixels|Purkinje)/.test(t) ? t : t.charAt(0).toLowerCase() + t.slice(1));
  // what you would measure for an entity at each level
  // an entity name for mid-sentence use: "social cognition", but "Purkinje cell", "Crus I", "VTA (dopamine)", "mGluR1"
  const inl = (id) => {
    const n = name(id);
    return lvl(id) === 'molecular' || /^(\S[A-Z]|Crus|Dandy|Purkinje|Prader|Golgi|Bergmann)/.test(n) ? n : n.charAt(0).toLowerCase() + n.slice(1);
  };
  const signal = (id) => ({
    molecular: `${inl(id)} expression or signaling`, cellular: `${inl(id)} activity`, circuit: `activity in the ${inl(id)}`,
    regional: `activity in ${inl(id)}`, systems: `activity in ${inl(id)}`, cognitive: `${inl(id)} performance`, clinical: `${inl(id)} symptoms`,
  }[lvl(id)] || name(id));

  function mount(node) {
    root = node;
    chain = CA.store.get('lab.chain', []).filter((id) => CA.ent[id]);
    questionId = CA.store.get('lab.question', null);
    notes = CA.store.get('lab.notes', '');
    els.chain = h('div', { class: 'chain' });
    els.suggest = h('div', {});
    els.out = h('div', {});
    els.saved = h('div', {});
    els.question = h('div', {});
    const input = h('input', { class: 'text', placeholder: 'Add an entity by name or synonym (e.g. ' + D.entities.filter((e) => e.region === CA.region.id).slice(0, 3).map((e) => (e.aka && e.aka[0]) || e.name).join(', ') + ')…', style: { width: '100%' } });
    const drop = h('div', { class: 'search-results', style: { left: 0, right: 'auto', width: '100%', top: '36px', display: 'none' } });
    input.addEventListener('input', () => {
      const res = CA.search(input.value, 10).filter((r) => r.type === 'entity');
      CA.clear(drop);
      drop.style.display = res.length ? 'block' : 'none';
      res.forEach((r) => drop.appendChild(h('button', { class: 'sr', onclick: () => { add(r.id); input.value = ''; drop.style.display = 'none'; } },
        h('div', {}, r.label), h('div', { class: 'muted' }, r.sub))));
    });
    input.addEventListener('keydown', (ev) => {
      if (ev.key === 'Enter') { const b = drop.querySelector('.sr'); if (b) b.click(); }
      if (ev.key === 'Escape') drop.style.display = 'none';
    });
    root.appendChild(h('div', { class: 'page' },
      h('div', { class: 'page-head' }, h('div', {},
        h('h2', {}, 'Hypothesis lab'),
        h('p', {}, 'Build a mechanistic chain across levels, from a gene or cell to a behavior or disorder. Each step shows its evidence status; the weakest step becomes the critical experiment.'))),
      h('div', { class: 'cols' },
        h('div', {},
          h('div', { class: 'card' }, h('h3', {}, 'Start from a chain'),
            D.chains.filter((c) => c.regions.includes(CA.region.id)).map((c) => h('div', { class: 'qcard', onclick: () => { setChain(c.nodes.filter((n, i, a) => a.indexOf(n) === i)); } },
              h('b', {}, c.name), h('span', { class: 'small muted' }, c.desc)))),
          h('div', { class: 'card' }, h('h3', {}, 'or an open question'),
            D.questions.filter((q) => q.regions.includes(CA.region.id)).map((q) => h('div', { class: 'qcard', onclick: () => setQuestion(q.id) }, h('b', {}, q.title)))),
          h('div', { class: 'card' }, h('h3', {}, 'Saved'), els.saved)),
        h('div', {},
          els.question,
          h('div', { class: 'card' },
            h('div', { class: 'row', style: { justifyContent: 'space-between' } }, h('h3', { style: { margin: 0 } }, 'Your chain'),
              h('div', { class: 'row' },
                h('button', { class: 'btn ghost', onclick: () => setChain(chain.slice().reverse()) }, '⇄ Reverse'),
                h('button', { class: 'btn ghost', onclick: () => setChain([]) }, 'Clear'))),
            h('div', { style: { position: 'relative', margin: '10px 0' } }, input, drop),
            els.chain),
          h('div', { class: 'card' }, els.suggest),
          h('div', { class: 'card' }, els.out)))));
    unsub = CA.on('lab-chain', (c) => setChain(c));
    renderAll();
  }
  function unmount() { if (unsub) unsub(); unsub = null; }

  function setChain(c) { chain = c.filter((id) => CA.ent[id]); CA.store.set('lab.chain', chain); renderAll(); }
  function add(id) { if (chain[chain.length - 1] !== id) setChain(chain.concat([id])); }
  function setQuestion(id) {
    questionId = id; CA.store.set('lab.question', id);
    const q = D.questions.find((x) => x.id === id);
    if (q && !chain.length) setChain(q.entities.slice(0, 2)); else renderAll();
  }
  function renderAll() { renderQuestion(); renderChain(); renderSuggest(); renderOut(); renderSaved(); }

  /* ---------- steps & evidence ---------- */
  function steps() {
    const out = [];
    for (let i = 1; i < chain.length; i++) {
      const a = chain[i - 1], b = chain[i], l = CA.linkBetween(a, b);
      out.push({ a, b, link: l, status: l ? l.status : 'gap', reversed: l ? l.s !== a : false });
    }
    return out;
  }

  function renderQuestion() {
    CA.clear(els.question);
    const q = D.questions.find((x) => x.id === questionId);
    if (!q) return;
    els.question.append(h('div', { class: 'card', style: { borderColor: CA.tc('#1f6feb') } },
      h('div', { class: 'row', style: { justifyContent: 'space-between' } }, h('h3', { style: { margin: 0 } }, 'Open question: ' + q.title),
        h('button', { class: 'btn ghost', onclick: () => { questionId = null; CA.store.set('lab.question', null); renderAll(); } }, '×')),
      h('p', { class: 'small', style: { marginTop: '6px' } }, q.text),
      h('div', { class: 'chips' }, q.entities.map((id) => CA.entChip(id, { onclick: add }))),
      h('p', { class: 'tiny muted', style: { margin: '6px 0' } }, 'Click an entity to add it to your chain.'),
      h('div', { class: 'small' }, 'Approaches: ', h('ul', { style: { margin: '4px 0', paddingLeft: '18px' } }, q.approaches.map((a) => h('li', {}, a)))),
      h('div', {}, CA.citeChips(q.refs))));
  }

  function renderChain() {
    CA.clear(els.chain);
    if (!chain.length) {
      els.chain.append(h('p', { class: 'muted small' }, 'Empty. Pick a preset, search above, or use "+ Hypothesis" on any entity in the other views.'));
      return;
    }
    const st = steps();
    chain.forEach((id, i) => {
      if (i) {
        const s = st[i - 1], col = s.link ? CA.statusColor(s.status) : CA.tc('#6e7681');
        els.chain.append(h('div', { class: 'clink' + (s.link ? '' : ' gap'), onclick: () => s.link && CA.showLink(s.link.id), title: s.link ? s.link.rel : 'No curated link' },
          h('span', { style: { color: col } }, s.link ? CA.statusById[s.status].label : 'GAP'),
          h('div', { class: 'ln', style: { borderColor: col } }),
          h('span', { class: 'muted' }, s.link ? (s.reversed ? '(reverse link)' : (s.link.refs || []).length + ' paper(s)') : 'untested')));
      }
      els.chain.append(h('div', { class: 'cnode', style: { borderTop: '3px solid ' + CA.entColor(id) } },
        h('div', { class: 'tiny muted' }, CA.levelById[lvl(id)].label),
        h('div', { class: 'nm', onclick: () => CA.select(id) }, name(id)),
        h('div', { class: 'tools' },
          i > 0 ? h('button', { title: 'Move left', onclick: () => { const c = chain.slice(); [c[i - 1], c[i]] = [c[i], c[i - 1]]; setChain(c); } }, '←') : null,
          i < chain.length - 1 ? h('button', { title: 'Move right', onclick: () => { const c = chain.slice(); [c[i + 1], c[i]] = [c[i], c[i + 1]]; setChain(c); } }, '→') : null,
          h('button', { title: 'Remove', onclick: () => setChain(chain.filter((_, j) => j !== i)) }, '✕'))));
    });
  }

  function renderSuggest() {
    CA.clear(els.suggest);
    const last = chain[chain.length - 1];
    if (!last) { els.suggest.append(h('h3', {}, 'Suggestions'), h('p', { class: 'small muted' }, 'Add an entity to see suggested next steps.')); return; }
    const inChain = new Set(chain);
    const known = CA.linksOf(last).filter((l) => !inChain.has(l.s === last ? l.t : l.s))
      .sort((a, b) => (b.s === last) - (a.s === last) || CA.rank(b.status) - CA.rank(a.status)).slice(0, 10);
    const doms = new Set(CA.ent[last].domains || []);
    const li = CA.levelById[lvl(last)].index;
    const nb = CA.neighbors(last);
    const untested = D.entities.filter((e) => !inChain.has(e.id) && !nb.has(e.id) && e.id !== last && CA.inRegion(e.id)
      && Math.abs(CA.levelById[e.level].index - li) <= 2 && CA.levelById[e.level].index !== li
      && (e.domains || []).some((d) => doms.has(d)))
      .map((e) => ({ e, score: CA.neighbors(e.id).size + (CA.levelById[e.level].index > li ? 2 : 0) }))
      .sort((a, b) => b.score - a.score).slice(0, 6);
    CA.append(els.suggest, h('h3', {}, 'Next step from ', h('span', { style: { color: CA.entColor(last) } }, name(last))),
      h('h4', {}, 'Known connections'),
      known.length ? known.map((l) => {
        const other = l.s === last ? l.t : l.s;
        return h('div', { class: 'suggest' },
          h('div', {}, h('div', { class: 'row' }, h('span', { class: 'muted' }, l.s === last ? '→' : '←'), CA.entChip(other, { onclick: add }), CA.statusBadge(l.status)),
            h('div', { class: 'tiny muted' }, l.rel)),
          h('button', { class: 'btn ghost', onclick: () => add(other) }, 'Add'));
      }) : h('p', { class: 'small muted' }, 'No further curated links.'),
      h('h4', {}, 'Untested combinations (shared domain, no curated link)'),
      untested.length ? untested.map(({ e }) => h('div', { class: 'suggest' },
        h('div', { class: 'row' }, CA.entChip(e.id, { onclick: add }), h('span', { class: 'tiny muted' }, CA.levelById[e.level].label)),
        h('button', { class: 'btn ghost', onclick: () => add(e.id) }, 'Add'))) : h('p', { class: 'small muted' }, 'None found.'));
  }

  /* ---------- composed hypothesis ---------- */
  function compose() {
    if (chain.length < 2) return null;
    const st = steps();
    const weakest = st.reduce((w, s) => (CA.rank(s.status) < CA.rank(w.status) ? s : w), st[0]);
    const first = chain[0], last = chain[chain.length - 1];
    const mid = chain.slice(1, -1).map(inl);
    const statement = `${name(first)} influences ${inl(last)}` + (mid.length ? ` through ${mid.join(' → ')}` : ' directly') + '.';
    const refs = [...new Set(st.flatMap((s) => (s.link && s.link.refs) || []))].filter((k) => CA.paper[k]);
    const species = {};
    refs.forEach((k) => (CA.paper[k].species || []).forEach((sp) => { species[sp] = (species[sp] || 0) + 1; }));
    const topSpecies = Object.entries(species).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([sp, n]) => `${sp} (${n})`);
    const ma = CA.methodsFor(lvl(weakest.a)), mb = CA.methodsFor(lvl(weakest.b));
    const A = inl(weakest.a), B = inl(weakest.b);
    const full = mid.length
      ? `Every step has support, so test the whole chain: perturb ${inl(first)} and ask whether its effect on ${inl(last)} requires ${mid[0]} (block ${mid[0]} during the perturbation).`
      : `The direct link is supported. Test its specificity next: does perturbing ${inl(first)} change ${inl(last)} more than perturbing a neighboring structure at the same level, and does the effect hold across species and developmental windows?`;
    const test = {
      gap: `No curated evidence connects ${A} and ${B}. First establish whether they interact at all: manipulate ${A} (e.g., ${lc(ma.manipulate[0])}) and read out ${B} (e.g., ${lc(mb.readout[0])}).`,
      hypothesis: `The step ${A} → ${B} has been proposed but not tested directly. Manipulate ${A} (e.g., ${lc(ma.manipulate[0])}) and measure ${B} (e.g., ${lc(mb.readout[0])}).`,
      debated: `Evidence on ${A} → ${B} conflicts. Design a test that separates the competing explanations, for example by comparing acute and chronic manipulation (${lc(ma.manipulate[1] || ma.manipulate[0])}) with ${lc(mb.readout[0])} as the readout.`,
      emerging: `${name(weakest.a)} → ${B} rests on one or a few studies. Replicate it with an independent method, ideally in a second species: manipulate with ${lc(ma.manipulate[0])} and read out with ${lc(mb.readout[0])}.`,
      supported: full,
      established: full,
    }[weakest.status];
    const predictions = [
      `Perturbing ${inl(first)} changes ${signal(last)}${mid.length ? `, and the change is reduced or abolished when ${mid[mid.length - 1]} is blocked` : ''}.`,
      `${cap(signal(weakest.b))} tracks ${signal(weakest.a)} across trials or individuals (the correlational signature of the weakest step).`,
      `The effect is specific: perturbing a control structure at the same level as ${inl(first)} does not reproduce it.`,
    ];
    if (lvl(last) === 'clinical' && chain.length > 2) predictions.push(`In patients, ${signal(chain[chain.length - 2])} scales with ${inl(last)} severity.`);
    // alternative routes in the knowledge graph (≤ 3 steps) that bypass the chain's intermediates
    const alts = [];
    if (chain.length >= 2) {
      const avoid = new Set(chain.slice(1, -1));
      const queue = [[first]];
      while (queue.length && alts.length < 4) {
        const path = queue.shift();
        const end = path[path.length - 1];
        if (path.length > 4) continue;
        CA.neighbors(end).forEach((n) => {
          if (path.includes(n) || avoid.has(n)) return;
          if (n === last) { if (path.length > 1 || chain.length > 2) alts.push(path.concat([n])); return; }
          queue.push(path.concat([n]));
        });
      }
    }
    const qs = D.questions.filter((q) => q.id === questionId || q.entities.some((e) => chain.includes(e)));
    const levels = [...new Set(chain.map(lvl))].sort((a, b) => CA.levelById[a].index - CA.levelById[b].index);
    return { st, weakest, statement, refs, topSpecies, test, predictions, alts: alts.slice(0, 3), qs, levels };
  }

  function renderOut() {
    CA.clear(els.out);
    const c = compose();
    if (!c) { els.out.append(h('h3', {}, 'Composed hypothesis'), h('p', { class: 'small muted' }, 'Add at least two entities.')); return; }
    const notesBox = h('textarea', { class: 'text', rows: 3, style: { width: '100%', marginTop: '6px', background: 'var(--bg2)', color: 'inherit', border: '1px solid var(--line2)', borderRadius: '6px', padding: '6px' },
      placeholder: 'Your notes: model system, controls, predictions…', oninput: (ev) => { notes = ev.target.value; CA.store.set('lab.notes', notes); } });
    notesBox.value = notes;
    els.out.append(h('div', { class: 'hyp-out' },
      h('h3', {}, 'Hypothesis'),
      h('p', { style: { fontSize: '1.05rem' } }, c.statement),
      h('h4', {}, 'Evidence for each step'),
      h('table', { class: 'data' }, c.st.map((s) => h('tr', { class: s.link ? 'click' : '', onclick: () => s.link && CA.showLink(s.link.id) },
        h('td', {}, s.link ? CA.statusBadge(s.status) : h('span', { class: 'badge', style: { color: CA.tc('#8b949e'), borderColor: CA.tc('#6e7681') } }, 'Gap')),
        h('td', {}, name(s.a), ' → ', name(s.b), s.link ? h('div', { class: 'tiny muted' }, s.link.rel + (s.reversed ? ' (curated in the reverse direction)' : '')) : null),
        h('td', {}, s.link ? CA.citeChips(s.link.refs) : h('a', { class: 'small', target: '_blank', rel: 'noopener', href: CA.pubmedSearchUrl(`(${name(s.a)}) AND (${name(s.b)}) AND ${CA.region.query}`) }, 'search PubMed ↗'))))),
      h('h4', {}, 'Critical test (weakest step)'),
      h('p', {}, c.test),
      h('h4', {}, 'Predictions'),
      h('ul', {}, c.predictions.map((p) => h('li', {}, p))),
      c.alts.length ? [h('h4', {}, 'Alternative routes to rule out'),
        h('ul', {}, c.alts.map((p) => h('li', { class: 'small' }, p.map(name).join(' → '))))] : null,
      h('h4', {}, 'Methods by level'),
      h('div', { class: 'small' }, c.levels.map((l) => h('div', { style: { margin: '4px 0' } },
        CA.lvlTag(l), ' ', h('b', {}, 'Manipulate: '), CA.methodsFor(l).manipulate.slice(0, 2).join('; '), ' · ', h('b', {}, 'Read out: '), CA.methodsFor(l).readout.slice(0, 2).join('; ')))),
      c.topSpecies.length ? h('p', { class: 'small muted', style: { marginTop: '8px' } }, 'Supporting evidence comes mostly from: ' + c.topSpecies.join(', ') + '. Consider whether each step has been shown in the species you care about.') : null,
      c.qs.length ? [h('h4', {}, 'Related open questions'), h('div', {}, c.qs.map((q) => h('div', { class: 'small' }, '• ', h('a', { href: '#', onclick: (ev) => { ev.preventDefault(); setQuestion(q.id); } }, q.title))))] : null,
      h('h4', {}, 'Notes'), notesBox,
      h('div', { class: 'row', style: { marginTop: '12px' } },
        h('button', { class: 'btn primary', onclick: save }, 'Save'),
        h('button', { class: 'btn', onclick: (ev) => copyMd(ev.target) }, 'Copy as Markdown'),
        h('button', { class: 'btn', onclick: downloadMd }, 'Download .md'))));
  }

  function markdown() {
    const c = compose();
    if (!c) return '';
    const q = D.questions.find((x) => x.id === questionId);
    const lines = [`# Hypothesis: ${c.statement}`, '', `Drafted with the Brain Circuit Atlas on ${new Date().toISOString().slice(0, 10)}.`, ''];
    if (q) lines.push(`**Open question:** ${q.title} ${q.text}`, '');
    lines.push('## Chain and evidence', '');
    c.st.forEach((s) => lines.push(`- **${name(s.a)} → ${name(s.b)}**: ${s.link ? CA.statusById[s.status].label + '. ' + s.link.rel + '. ' + (s.link.refs || []).map((k) => CA.shortCite(CA.paper[k])).join('; ') : 'Gap: no curated evidence.'}`));
    lines.push('', '## Critical test', '', c.test, '', '## Predictions', '', ...c.predictions.map((p) => '- ' + p));
    if (c.alts.length) lines.push('', '## Alternative routes to rule out', '', ...c.alts.map((p) => '- ' + p.map(name).join(' → ')));
    lines.push('', '## Methods', '', ...c.levels.map((l) => `- ${CA.levelById[l].label}: manipulate with ${CA.methodsFor(l).manipulate.slice(0, 2).join('; ')}; read out with ${CA.methodsFor(l).readout.slice(0, 2).join('; ')}`));
    if (notes) lines.push('', '## Notes', '', notes);
    lines.push('', '## References', '', ...c.refs.map((k) => '- ' + CA.fullCite(CA.paper[k])));
    lines.push('', '_Evidence statuses were drafted with AI assistance from PubMed abstracts; verify against the sources._');
    return lines.join('\n');
  }
  function copyMd(btn) {
    const md = markdown();
    const done = () => { const t = btn.textContent; btn.textContent = 'Copied ✓'; setTimeout(() => { btn.textContent = t; }, 1500); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(md).then(done, () => fallbackCopy(md, done));
    else fallbackCopy(md, done);
  }
  function fallbackCopy(text, done) {
    const ta = h('textarea', { style: { position: 'fixed', left: '-9999px' } });
    ta.value = text; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); done(); } catch (e) { /* ignore */ }
    ta.remove();
  }
  function downloadMd() {
    const blob = new Blob([markdown()], { type: 'text/markdown' });
    const a = h('a', { href: URL.createObjectURL(blob), download: CA.region.id + '-hypothesis.md' });
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }

  /* ---------- saved ---------- */
  function save() {
    const c = compose();
    if (!c) return;
    const item = { id: Date.now(), title: c.statement, chain: chain.slice(), question: questionId, notes, date: new Date().toISOString().slice(0, 10) };
    const saved = CA.store.get('lab.saved', []);
    saved.unshift(item);
    CA.store.set('lab.saved', saved.slice(0, 50));
    if (CA.hasBackend) {
      fetch('/api/hypotheses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ region: CA.region.id, title: item.title, summary: item.notes, chain: item.chain })
      }).catch(() => {});
    }
    renderSaved();
  }
  function renderSaved() {
    CA.clear(els.saved);
    const saved = CA.store.get('lab.saved', []);
    if (!saved.length) { els.saved.append(h('p', { class: 'small muted' }, CA.hasBackend ? 'Hypotheses are saved to your local Atlas database.' : 'Saved hypotheses stay in this browser.')); return; }
    saved.forEach((x) => els.saved.append(h('div', { class: 'suggest' },
      h('a', { href: '#', class: 'small', onclick: (ev) => { ev.preventDefault(); notes = x.notes || ''; CA.store.set('lab.notes', notes); questionId = x.question; CA.store.set('lab.question', questionId); setChain(x.chain); } }, x.title),
      h('button', { class: 'btn ghost', title: 'Delete', onclick: () => { CA.store.set('lab.saved', CA.store.get('lab.saved', []).filter((y) => y.id !== x.id)); renderSaved(); } }, '✕'))));
  }
})();
