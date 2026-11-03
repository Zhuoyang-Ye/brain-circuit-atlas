/* 3D atlas: real atlas meshes (human or mouse) with evidence-coded connections to the rest of the brain and body. */
(function () {
  'use strict';
  const CA = window.CA, D = CA.D, A3 = D.atlas3d, h = CA.h;

  const GROUP = {
    shell: { color: 0x9aa7b8, opacity: 0.09 },
    cerebellum: { color: 0xe3b341, opacity: 1 },
    nuclei: { color: 0xff5f57, opacity: 1 },
    tract: { color: 0xffa657, opacity: 0.85 },
    brainstem: { color: 0x3fb9a5, opacity: 0.95 },
    context: { color: 0x8b949e, opacity: 0.2 },
    target: { color: 0x58a6ff, opacity: 0.9 },
    cortex: { color: 0xb392f0, opacity: 0.55 },
  };
  // distinguishable warm tones for cerebellar subdivisions
  const CB_TONES = {
    'zone-vermis': 0xf5d76e, 'zone-paravermis': 0xe9a23b, 'zone-lateral': 0xd9822b,
    'lob-ant': 0xf5d76e, 'vermis-post': 0xe8b04a, 'lob-ix': 0xf0c75e, 'lob-x': 0xc6d96b,
    'lob-vi': 0xe39b35, 'lob-crus1': 0xe07b39, 'lob-crus2': 0xc9652b, 'lob-viib': 0xd88a3a, 'lob-viii': 0xb8742f,
  };
  const BODY_COLORS = { eyes: 0x9ad0ff, labyrinth: 0xd2a8ff, gut: 0xe879f9, body: 0x4fd1c5, spinal: 0x3fb9a5 };
  const VIEWS = {
    human: {
      overview: { pos: [-11.5, 5.5, -11], target: [0, -0.8, 0] },
      cerebellum: { pos: [-5.2, 0.6, -9.5], target: [0, -2.6, -2.4] },
      left: { pos: [-17, 0.5, 0], target: [0, -0.8, 0] },
      back: { pos: [0, 1.5, -17], target: [0, -1.2, 0] },
      top: { pos: [0, 17, -0.01], target: [0, 0, 0] },
      below: { pos: [0.01, -16, 2], target: [0, -1, 0] },
    },
    mouse: {
      overview: { pos: [-10, 7, -9], target: [0, -0.5, -0.5] },
      cerebellum: { pos: [-5, 3, -9], target: [0, -0.6, -3.5] },
      left: { pos: [-16, 0.5, 0], target: [0, -0.5, 0] },
      back: { pos: [0, 2, -16], target: [0, -0.5, 0] },
      top: { pos: [0, 16, -0.01], target: [0, 0, 0] },
      below: { pos: [0.01, -15, 1], target: [0, 0, 0] },
    },
  };

  let root, el = {}, renderer, scene, camera, controls, raf = 0, ro, clock, pointer = null, pointerDirty = false;
  let species = CA.store.get('atlas.species', 'human');
  let opts = Object.assign({ shell: true, xray: false, labels: true, bodyParts: true, animate: true, opacity: 0.09 }, CA.store.get('atlas.opts', {}));
  let circuitId = CA.store.get('atlas.circuit', 'loops');
  let pickables = [], meshObjs = [], linkObjs = [], pulses = [], labelEls = [], markerObjs = [];
  let positions = {}, hovered = null, tween = null, unsubs = [], disposed = false, buildToken = 0;
  const geomCache = {};

  CA.register('atlas', { title: '3D atlas', mount, unmount, route });

  /* ---------------------------------------------------------------- mount */
  function mount(node) {
    root = node;
    disposed = false;
    const wrap = h('div', { class: 'atlas' });
    el.canvas = h('div', { class: 'atlas-canvas' });
    el.labels = h('div', { class: 'atlas-labels' });
    el.msg = h('div', { class: 'atlas-msg' }, 'Loading 3D anatomy…');
    el.controls = buildControls();
    el.legend = buildLegend();
    el.hint = h('div', { class: 'atlas-hint' }, 'Drag to rotate · scroll to zoom · right-drag to pan · click a structure');
    wrap.append(el.canvas, el.labels, el.controls, el.legend, el.hint, el.msg);
    if (!CA.store.get('intro.dismissed', false)) wrap.append(buildIntro());
    root.appendChild(wrap);

    if (!window.THREE || !webglOK()) {
      el.msg.innerHTML = '<div><h3>3D view unavailable</h3><p>This browser could not start WebGL. The other views (functional map, microcircuit, across scales, evidence & gaps) work without it.</p></div>';
      return;
    }
    initThree();
    unsubs.push(CA.on('select', () => { applyHighlight(); rebuildLinks(); }));
    loadSpecies(species);
  }

  function unmount() {
    disposed = true;
    cancelAnimationFrame(raf);
    unsubs.forEach((u) => u()); unsubs = [];
    if (ro) ro.disconnect();
    if (renderer) {
      clearScene();
      renderer.dispose();
      if (renderer.forceContextLoss) renderer.forceContextLoss();
      renderer.domElement.remove();
    }
    renderer = scene = camera = controls = null;
    CA.tip.hide();
  }

  function route(r) {
    if (r.kind === 'e' && CA.ent[r.id]) focusEntity(r.id);
  }

  function webglOK() {
    try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; }
  }

  /* ---------------------------------------------------------------- UI */
  function buildIntro() {
    const box = h('div', { class: 'intro' },
      h('h2', {}, 'The cerebellum, wired into brain and body'),
      h('p', { class: 'small' }, 'A map that joins motor, cognitive and social functions of the cerebellum, from molecules to behavior. Every connection is tied to the papers behind it and graded by how strong the evidence is.'),
      h('ol', { class: 'small' },
        h('li', {}, 'Pick a ', h('b', {}, 'circuit'), ' on the left to see its pathways; pulses show signal direction.'),
        h('li', {}, 'Click any structure for its evidence, connections and open questions.'),
        h('li', {}, 'Go deeper: ', h('a', { href: '#/map' }, 'functional map'), ', ', h('a', { href: '#/circuit' }, 'microcircuit'), ', ', h('a', { href: '#/molecules' }, 'molecules'), '.'),
        h('li', {}, 'Find what is unknown in ', h('a', { href: '#/gaps' }, 'Evidence & gaps'), ' and draft tests in the ', h('a', { href: '#/lab' }, 'Hypothesis lab'), '.')),
      h('div', { class: 'row' },
        h('button', { class: 'btn primary', onclick: () => { flyTo('cerebellum'); } }, 'Zoom to cerebellum'),
        h('button', { class: 'btn', onclick: () => { CA.store.set('intro.dismissed', true); box.remove(); } }, 'Got it')));
    return box;
  }

  function buildControls() {
    const box = h('div', { class: 'atlas-controls' });
    const seg = h('div', { class: 'seg' },
      ['human', 'mouse'].map((sp) => h('button', {
        class: sp === species ? 'on' : '', 'data-sp': sp,
        onclick: () => { if (sp !== species) { species = sp; CA.store.set('atlas.species', sp); seg.querySelectorAll('button').forEach((b) => b.classList.toggle('on', b.dataset.sp === sp)); loadSpecies(sp); } },
      }, sp === 'human' ? 'Human' : 'Mouse')));
    el.speciesNote = h('div', { class: 'desc' });
    const circs = h('div', {});
    const all = [...A3.circuits, { id: 'all', name: 'All mapped connections', desc: 'Every anatomical or functional link in the knowledge base with both ends placed in this atlas.' },
      { id: 'none', name: 'Anatomy only', desc: 'Hide pathways. Click a structure to show its own connections.' }];
    all.forEach((c) => circs.appendChild(h('button', {
      class: 'circ' + (c.id === circuitId ? ' on' : ''), 'data-c': c.id,
      onclick: () => {
        circuitId = c.id; CA.store.set('atlas.circuit', c.id);
        circs.querySelectorAll('.circ').forEach((b) => b.classList.toggle('on', b.dataset.c === c.id));
        el.circDesc.textContent = c.desc || '';
        rebuildLinks();
      },
    }, c.name)));
    el.circDesc = h('div', { class: 'desc' }, (all.find((c) => c.id === circuitId) || {}).desc || '');
    const check = (key, label, fn) => h('label', { class: 'check small' },
      h('input', { type: 'checkbox', checked: opts[key], onchange: (ev) => { opts[key] = ev.target.checked; CA.store.set('atlas.opts', opts); fn(); } }), label);
    const views = h('div', { class: 'chips' }, [['overview', 'Overview'], ['cerebellum', 'Cerebellum'], ['left', 'Left'], ['back', 'Back'], ['top', 'Top'], ['below', 'Below']]
      .map(([k, label]) => h('span', { class: 'chip', onclick: () => flyTo(k) }, label)));
    el.credit = h('div', { class: 'atlas-credit' });
    box.append(
      h('h4', {}, 'Species'), seg, el.speciesNote,
      h('h4', {}, 'Circuits'), circs, el.circDesc,
      h('h4', {}, 'Display'),
      check('shell', 'Brain surface', applyMaterials),
      h('input', { type: 'range', min: 0.03, max: 0.35, step: 0.01, value: opts.opacity, style: { width: '100%' },
        oninput: (ev) => { opts.opacity = +ev.target.value; CA.store.set('atlas.opts', opts); applyMaterials(); } }),
      check('xray', 'X-ray cerebellum (see nuclei)', applyMaterials),
      check('labels', 'Labels', () => {}),
      check('bodyParts', 'Body & senses', () => markerObjs.forEach((m) => { m.visible = opts.bodyParts || !m.userData.body; })),
      check('animate', 'Animate signals', () => {}),
      h('h4', {}, 'Camera'), views, el.credit);
    return box;
  }

  function buildLegend() {
    const items = D.statuses.filter((s) => s.id !== 'gap').map((s) => h('div', { class: 'lg' },
      h('span', { class: 'sw', style: { borderColor: s.color, borderTopStyle: (s.id === 'debated' || s.id === 'hypothesis') ? 'dashed' : 'solid' } }), s.label));
    items.push(h('div', { class: 'lg' }, h('span', { class: 'sw', style: { borderColor: '#8b949e', borderTopStyle: 'dashed' } }), 'functional / route unknown'));
    items.push(h('div', { class: 'lg' }, h('span', { style: { fontStyle: 'italic' } }, 'italic ≈'), 'approximate position'));
    return h('div', { class: 'atlas-legend' }, items);
  }

  /* ---------------------------------------------------------------- three.js */
  function initThree() {
    const T = window.THREE;
    renderer = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setClearColor(0x000000, 0);
    el.canvas.appendChild(renderer.domElement);
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(38, 1, 0.1, 200);
    camera.position.set(-11.5, 5.5, -11);
    scene.add(camera);
    scene.add(new T.HemisphereLight(0xdde6ff, 0x1a1410, 0.75));
    const key = new T.DirectionalLight(0xffffff, 0.85);
    key.position.set(-3, 6, 4);
    camera.add(key);
    const rim = new T.DirectionalLight(0x88aaff, 0.35);
    rim.position.set(6, -2, -6);
    scene.add(rim);
    controls = new T.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.minDistance = 3;
    controls.maxDistance = 40;
    controls.addEventListener('start', () => { tween = null; });
    clock = new T.Clock();
    resize();
    ro = new ResizeObserver(resize);
    ro.observe(el.canvas);
    const cv = renderer.domElement;
    cv.addEventListener('pointermove', (ev) => { pointer = ev; pointerDirty = true; });
    cv.addEventListener('pointerleave', () => { pointer = null; pointerDirty = true; });
    let down = null;
    cv.addEventListener('pointerdown', (ev) => { down = [ev.clientX, ev.clientY]; });
    cv.addEventListener('pointerup', (ev) => {
      if (down && Math.hypot(ev.clientX - down[0], ev.clientY - down[1]) < 5) onClick(ev);
      down = null;
    });
    loop();
  }

  function resize() {
    if (!renderer) return;
    const w = el.canvas.clientWidth || 800, ht = el.canvas.clientHeight || 600;
    renderer.setSize(w, ht, false);
    renderer.domElement.style.width = w + 'px';
    renderer.domElement.style.height = ht + 'px';
    camera.aspect = w / ht;
    camera.updateProjectionMatrix();
  }

  function loadSpecies(sp) {
    const token = ++buildToken;
    el.msg.style.display = 'flex';
    el.msg.textContent = 'Loading 3D anatomy…';
    el.speciesNote.textContent = sp === 'human'
      ? 'Human: lobules and deep nuclei from the SUIT probabilistic atlas (Diedrichsen 2009, 2011), fitted to the Allen human brain. Brainstem nuclei not segmented in these atlases are approximate (≈).'
      : 'Mouse: Allen CCFv3 lobules and nuclei. Most causal circuit evidence comes from mice.';
    CA.loadScript(`js/data/meshes_${sp}.js`).then(() => {
      if (disposed || token !== buildToken) return;
      const bundle = window.CA_MESHES && window.CA_MESHES[sp];
      if (!bundle) throw new Error('mesh bundle missing for ' + sp);
      buildScene(sp, bundle);
      el.msg.style.display = 'none';
      const r = CA.parseHash();
      if (r.kind === 'e' && CA.ent[r.id]) focusEntity(r.id, true);
      else jumpTo('overview');
    }).catch((e) => {
      el.msg.innerHTML = '<div><h3>Could not load 3D data</h3><p class="small">' + CA.esc(e.message) + '</p><p class="small">Run <code>python tools/build_meshes.py</code> to generate the mesh files.</p></div>';
    });
  }

  function clearScene() {
    const kill = (o) => {
      scene.remove(o);
      o.traverse((c) => {
        if (c.geometry && !c.geometry.userData.cached) c.geometry.dispose();
        if (c.material) (Array.isArray(c.material) ? c.material : [c.material]).forEach((m) => m.dispose());
      });
    };
    [...meshObjs, ...linkObjs, ...markerObjs].forEach(kill);
    meshObjs = []; linkObjs = []; markerObjs = []; pickables = []; pulses = [];
    labelEls.forEach((l) => l.el.remove()); labelEls = [];
  }

  function b64(s) {
    const bin = atob(s), u = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    return u;
  }

  function geometryFor(sp, rec, qs) {
    const key = sp + ':' + rec.key;
    if (geomCache[key]) return geomCache[key];
    const T = window.THREE;
    const p16 = new Int16Array(b64(rec.p).buffer);
    const pos = new Float32Array(p16.length);
    for (let i = 0; i < p16.length; i++) pos[i] = p16[i] * qs;
    const ib = b64(rec.i).buffer;
    const g = new T.BufferGeometry();
    g.setAttribute('position', new T.BufferAttribute(pos, 3));
    g.setIndex(new T.BufferAttribute(rec.i32 ? new Uint32Array(ib) : new Uint16Array(ib), 1));
    g.computeVertexNormals();
    g.computeBoundingSphere();
    g.userData.cached = true;
    geomCache[key] = g;
    return g;
  }

  function buildScene(sp, bundle) {
    const T = window.THREE;
    clearScene();
    el.credit.textContent = 'Anatomy: ' + bundle.credit;
    bundle.meshes.forEach((rec) => {
      const style = GROUP[rec.group] || GROUP.context;
      let color = style.color;
      if (rec.group === 'cerebellum' && CB_TONES[rec.entity || rec.related]) color = CB_TONES[rec.entity || rec.related];
      if (rec.tone) color = new T.Color(rec.tone).getHex(); // per-lobule tone, alternating light/dark so neighbors separate
      const mat = new T.MeshStandardMaterial({ color, roughness: 0.62, metalness: 0.05, transparent: true, opacity: style.opacity });
      const mesh = new T.Mesh(geometryFor(sp, rec, bundle.qs), mat);
      mesh.userData = { rec, base: color, baseOpacity: style.opacity, entity: rec.entity || null };
      if (rec.group === 'shell') { mesh.renderOrder = 10; mat.depthWrite = false; }
      scene.add(mesh);
      meshObjs.push(mesh);
      if (rec.group !== 'shell') pickables.push(mesh);
    });
    computePositions(bundle);
    buildBodyAndMarkers(sp, bundle);
    applyMaterials();
    applyHighlight();
    rebuildLinks();
  }

  /* -------- entity positions: mesh centroids, mesh groups, anchors, aliases -------- */
  function computePositions(bundle) {
    const T = window.THREE;
    positions = {};
    const agg = (recs) => {
      if (!recs.length) return null;
      const mean = (arrs) => arrs.length ? new T.Vector3(...[0, 1, 2].map((k) => arrs.reduce((s, a) => s + a[k], 0) / arrs.length)) : null;
      const c = mean(recs.map((r) => r.c));
      return { c, l: mean(recs.filter((r) => r.side !== 'R').map((r) => r.cl)) || c, r: mean(recs.filter((r) => r.side !== 'L').map((r) => r.cr)) || c };
    };
    const byEnt = {};
    bundle.meshes.forEach((r) => { if (r.entity) (byEnt[r.entity] = byEnt[r.entity] || []).push(r); });
    Object.entries(byEnt).forEach(([id, recs]) => { positions[id] = agg(recs); });
    Object.entries(A3.groups).forEach(([id, group]) => {
      if (!positions[id]) {
        const p = agg(bundle.meshes.filter((r) => r.group === group));
        if (p) positions[id] = p;
      }
    });
    Object.entries(bundle.anchors || {}).forEach(([id, a]) => {
      if (!positions[id]) positions[id] = { c: new T.Vector3(...a[0]), l: new T.Vector3(...a[1]), r: new T.Vector3(...a[2]), approx: species === 'human' && !['spinal', 'body', 'gut', 'eyes', 'labyrinth'].includes(id) };
    });
  }

  function sideOf(id) {
    for (const [side, ids] of Object.entries(A3.sides)) if (ids.includes(id)) return side;
    return 'C';
  }
  function resolve(id) {
    if (positions[id]) return id;
    const alias = (A3.aliases[species] || {})[id];
    return alias && positions[alias] ? alias : null;
  }
  function posOf(id, side) {
    const rid = resolve(id);
    if (!rid) return null;
    const p = positions[rid];
    side = side || sideOf(id);
    return (side === 'R' ? p.r : side === 'L' ? p.l : p.c).clone();
  }

  /* -------- body, senses, spinal cord and approximate markers -------- */
  function buildBodyAndMarkers(sp, bundle) {
    const T = window.THREE;
    const human = sp === 'human';
    const add = (obj, entity, body) => {
      obj.userData.entity = entity; obj.userData.body = body; obj.userData.marker = true;
      obj.visible = opts.bodyParts || !body;
      scene.add(obj); markerObjs.push(obj); pickables.push(obj);
    };
    const mat = (c, o) => new T.MeshStandardMaterial({ color: c, roughness: 0.5, transparent: true, opacity: o == null ? 0.9 : o, emissive: c, emissiveIntensity: 0.12 });
    if (bundle.spine && bundle.spine.length > 1) {
      const pts = bundle.spine.map((p) => new T.Vector3(...p));
      const curve = new T.CatmullRomCurve3(pts);
      add(new T.Mesh(new T.TubeGeometry(curve, 40, human ? 0.2 : 0.14, 10, false), mat(BODY_COLORS.spinal, 0.55)), 'spinal', true);
    }
    const A = bundle.anchors || {};
    const at = (id, k) => new T.Vector3(...A[id][k]);
    if (A.eyes) [1, 2].forEach((k) => { const m = new T.Mesh(new T.SphereGeometry(human ? 0.42 : 0.3, 24, 16), mat(BODY_COLORS.eyes, 0.75)); m.position.copy(at('eyes', k)); add(m, 'eyes', true); });
    if (A.labyrinth) [1, 2].forEach((k) => {
      const g = new T.Group();
      [[0, 0, 0], [Math.PI / 2, 0, 0], [0, Math.PI / 2, 0]].forEach((rot, i) => {
        const t = new T.Mesh(new T.TorusGeometry(human ? 0.2 : 0.15, 0.04, 8, 24), mat(BODY_COLORS.labyrinth, 0.95));
        t.rotation.set(...rot); t.position.x = (i - 1) * 0.06; g.add(t);
      });
      g.position.copy(at('labyrinth', k)); add(g, 'labyrinth', true);
    });
    if (A.gut) { const m = new T.Mesh(new T.SphereGeometry(human ? 0.55 : 0.4, 24, 16), mat(BODY_COLORS.gut, 0.6)); m.scale.set(1.4, 0.8, 1); m.position.copy(at('gut', 0)); add(m, 'gut', true); }
    if (A.body) { const m = new T.Mesh(new T.CapsuleGeometry(human ? 0.22 : 0.16, human ? 0.7 : 0.5, 6, 12), mat(BODY_COLORS.body, 0.75)); m.position.copy(at('body', 2)); add(m, 'body', true); }
    // structures without a segmented mesh in this atlas
    Object.entries(positions).forEach(([id, p]) => {
      if (!p.approx) return;
      const side = sideOf(id);
      const m = new T.Mesh(new T.OctahedronGeometry(human ? 0.16 : 0.12), mat(0x3fb9a5, 0.95));
      m.position.copy(side === 'R' ? p.r : side === 'L' ? p.l : p.c);
      add(m, id, false);
      m.userData.approx = true;
    });
  }

  /* -------- materials, highlight -------- */
  function selectedSet() {
    const id = CA.selected;
    if (!id) return new Set();
    const s = new Set([id]);
    const rid = resolve(id);
    if (rid) s.add(rid);
    return s;
  }

  function applyMaterials() {
    meshObjs.forEach((m) => {
      const r = m.userData.rec, mat = m.material;
      if (r.group === 'shell') { m.visible = opts.shell; mat.opacity = opts.opacity; return; }
      if (r.group === 'cerebellum') {
        mat.opacity = opts.xray ? 0.22 : 1;
        mat.depthWrite = !opts.xray;
      } else {
        mat.opacity = m.userData.baseOpacity;
        mat.depthWrite = m.userData.baseOpacity > 0.6;
      }
      mat.needsUpdate = true;
    });
  }

  function applyHighlight() {
    const sel = selectedSet();
    const T = window.THREE;
    meshObjs.concat(markerObjs).forEach((m) => {
      const rel = m.userData.rec && m.userData.rec.related;
      const on = (m.userData.entity && sel.has(m.userData.entity)) || (rel && sel.has(rel));
      const hov = hovered && hovered === m;
      m.traverse((c) => {
        if (!c.material || !c.material.emissive) return;
        c.material.emissive = new T.Color(on ? 0x4a7dff : hov ? 0x555555 : (c.material.color || new T.Color(0)).getHex());
        c.material.emissiveIntensity = on ? 0.55 : hov ? 0.5 : (m.userData.marker ? 0.12 : 0);
      });
    });
  }

  /* -------- connections -------- */
  function activeLinks() {
    const ids = new Set();
    if (circuitId === 'all') D.links.forEach((l) => { if (l.kind === 'anatomical' || l.kind === 'functional') ids.add(l.id); });
    else if (circuitId !== 'none') (A3.circuits.find((c) => c.id === circuitId) || { links: [] }).links.forEach((x) => ids.add(x));
    const sel = CA.selected;
    if (sel) CA.linksOf(sel).forEach((l) => { if (l.kind === 'anatomical' || l.kind === 'functional') ids.add(l.id); });
    return [...ids].map((id) => CA.link[id]).filter(Boolean);
  }

  function rebuildLinks() {
    if (!scene) return;
    const T = window.THREE;
    linkObjs.forEach((o) => { scene.remove(o); o.traverse((c) => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); }); });
    pickables = pickables.filter((p) => !p.userData.link);
    linkObjs = []; pulses = [];
    labelEls.forEach((l) => l.el.remove()); labelEls = [];
    const human = species === 'human';
    const sel = CA.selected;
    const drawn = new Set();
    activeLinks().forEach((l) => {
      const a = posOf(l.s), b = posOf(l.t);
      if (!a || !b || a.distanceTo(b) < 0.08) return;
      const key = [resolve(l.s), sideOf(l.s), resolve(l.t), sideOf(l.t)].join('|');
      if (drawn.has(key)) return;   // e.g. dentate and DCN share one position in the human atlas
      drawn.add(key);
      const dist = a.distanceTo(b);
      const mid = a.clone().add(b).multiplyScalar(0.5);
      const out = mid.clone(); if (out.length() < 0.01) out.set(0, 1, 0);
      const ctrl = mid.add(out.normalize().multiplyScalar(0.16 * dist + 0.35));
      const curve = new T.QuadraticBezierCurve3(a, ctrl, b);
      const color = new T.Color(CA.statusColor(l.status));
      const focus = sel && (l.s === sel || l.t === sel);
      const dashed = l.kind === 'functional' || l.status === 'hypothesis' || l.status === 'debated';
      let obj;
      if (dashed) {
        const g = new T.BufferGeometry().setFromPoints(curve.getPoints(64));
        obj = new T.Line(g, new T.LineDashedMaterial({ color: l.kind === 'functional' && l.status !== 'hypothesis' ? 0x9aa4b2 : color, dashSize: 0.16, gapSize: 0.1, transparent: true, opacity: 0.95 }));
        obj.computeLineDistances();
        const hit = new T.Mesh(new T.TubeGeometry(curve, 24, 0.09, 5, false), new T.MeshBasicMaterial({ visible: false }));
        obj.add(hit); hit.userData.link = l; pickables.push(hit);
      } else {
        const radius = ({ established: 0.055, supported: 0.045, emerging: 0.038 }[l.status] || 0.04) * (human ? 1 : 0.85) * (focus ? 1.4 : 1);
        obj = new T.Mesh(new T.TubeGeometry(curve, 48, radius, 7, false), new T.MeshBasicMaterial({ color, transparent: true, opacity: 0.8 }));
        obj.userData.link = l; pickables.push(obj);
      }
      obj.renderOrder = 5;
      scene.add(obj); linkObjs.push(obj);
      const n = Math.max(1, Math.round(dist / 3));
      for (let k = 0; k < n; k++) {
        const s = new T.Mesh(new T.SphereGeometry(human ? 0.085 : 0.07, 10, 8), new T.MeshBasicMaterial({ color: color.clone().lerp(new T.Color(0xffffff), 0.45) }));
        s.renderOrder = 6;
        scene.add(s); linkObjs.push(s);
        pulses.push({ mesh: s, curve, offset: k / n, speed: 0.22 / Math.max(1, dist / 4) * (l.status === 'hypothesis' ? 0.5 : 1) });
      }
      [l.s, l.t].forEach((id) => addLabel(id));
    });
    if (sel) addLabel(sel);
    if (opts.labels && circuitId === 'none' && !sel) Object.keys(positions).forEach((id) => { if (CA.ent[id] && !['body', 'gut', 'spinal'].includes(id)) addLabel(id); });
  }

  function addLabel(id) {
    if (labelEls.some((l) => l.id === id)) return;
    const p = posOf(id);
    if (!p || !CA.ent[id]) return;
    const rid = resolve(id);
    const approx = rid && positions[rid].approx;
    const viaAlias = rid && rid !== id;
    const name = CA.ent[id].name + (viaAlias ? ' (in ' + CA.ent[rid].name.toLowerCase() + ')' : '') + (approx ? ' ≈' : '');
    const e = h('div', { class: 'alabel' + (approx ? ' approx' : '') + (CA.selected === id ? ' sel' : '') }, name);
    el.labels.appendChild(e);
    labelEls.push({ id, el: e, pos: p });
  }

  /* -------- interaction -------- */
  const raycaster = () => (raycaster.rc = raycaster.rc || new window.THREE.Raycaster());
  function pick(ev) {
    if (!camera || !pickables.length) return null;
    const rect = renderer.domElement.getBoundingClientRect();
    const v = new window.THREE.Vector2(((ev.clientX - rect.left) / rect.width) * 2 - 1, -((ev.clientY - rect.top) / rect.height) * 2 + 1);
    const rc = raycaster();
    rc.setFromCamera(v, camera);
    const hits = rc.intersectObjects(pickables.filter((o) => o.visible || o.userData.link), true);
    for (const hit of hits) {
      let o = hit.object;
      while (o && !o.userData.rec && !o.userData.entity && !o.userData.link) o = o.parent;
      if (o) return o;
    }
    return null;
  }

  function describe(o) {
    if (o.userData.link) {
      const l = o.userData.link, st = CA.statusById[l.status];
      return `<b>${CA.esc(CA.ent[l.s].name)} → ${CA.esc(CA.ent[l.t].name)}</b><br>${CA.esc(l.rel)}<br><span style="color:${st.color}">${st.label}</span> · ${(l.refs || []).length} paper(s)`;
    }
    const rec = o.userData.rec;
    const ent = CA.ent[o.userData.entity];
    if (rec) {
      const rel = rec.related && CA.ent[rec.related] ? `<br><span class="muted">related: ${CA.esc(CA.ent[rec.related].name)}</span>` : '';
      const note = rec.note && /uncertain/.test(rec.note) ? `<br><span class="muted">${CA.esc(rec.note.replace(/^.*?fitted to this brain\. /, ''))}</span>` : '';
      return `<b>${CA.esc(rec.name)}</b>${ent && ent.name !== rec.name ? '<br><span class="muted">' + CA.esc(ent.name) + '</span>' : ''}${rel}${note}`;
    }
    if (ent) return `<b>${CA.esc(ent.name)}</b>${o.userData.approx ? '<br><span class="muted">approximate position (not segmented in this atlas)</span>' : ''}`;
    return '';
  }

  function onClick(ev) {
    const o = pick(ev);
    if (!o) return;
    if (o.userData.link) { CA.showLink(o.userData.link.id); return; }
    const rec = o.userData.rec;
    if (o.userData.entity) { CA.select(o.userData.entity); return; }
    if (rec) {
      CA.showInfo('Structure', h('div', {},
        h('h2', {}, rec.name),
        rec.note ? h('p', { class: 'summary' }, rec.note) : null,
        rec.related ? h('div', {}, h('h4', {}, 'Related entry'), CA.entChip(rec.related)) : null,
        h('p', { class: 'small muted', style: { marginTop: '12px' } }, 'Shown for anatomical context.')));
    }
  }

  function focusEntity(id, instant) {
    const p = posOf(id);
    if (!p || !camera) return;
    const dir = camera.position.clone().sub(controls.target).normalize();
    const dist = species === 'human' ? 9 : 8;
    const to = { pos: p.clone().add(dir.multiplyScalar(dist)).toArray(), target: p.toArray() };
    if (instant) { camera.position.fromArray(to.pos); controls.target.fromArray(to.target); controls.update(); } else startTween(to);
  }

  function jumpTo(name) {
    const v = VIEWS[species][name];
    camera.position.fromArray(v.pos); controls.target.fromArray(v.target); controls.update();
  }
  function flyTo(name) { if (camera) startTween(VIEWS[species][name]); }
  function startTween(to) {
    tween = { t0: performance.now(), dur: 900, fromPos: camera.position.clone(), fromTarget: controls.target.clone(),
      toPos: new window.THREE.Vector3(...to.pos), toTarget: new window.THREE.Vector3(...to.target) };
  }

  /* -------- render loop -------- */
  function loop() {
    raf = requestAnimationFrame(loop);
    if (!renderer || !scene) return;
    const T = window.THREE;
    if (tween) {
      const k = Math.min(1, (performance.now() - tween.t0) / tween.dur), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      camera.position.lerpVectors(tween.fromPos, tween.toPos, e);
      controls.target.lerpVectors(tween.fromTarget, tween.toTarget, e);
      if (k >= 1) tween = null;
    }
    controls.update();
    const t = clock.getElapsedTime();
    pulses.forEach((p) => {
      p.mesh.visible = opts.animate;
      if (opts.animate) p.mesh.position.copy(p.curve.getPointAt((t * p.speed + p.offset) % 1));
    });
    if (pointerDirty) {
      pointerDirty = false;
      const o = pointer ? pick(pointer) : null;
      if (o !== hovered) { hovered = o; applyHighlight(); }
      if (o) { CA.tip.show(describe(o), pointer); renderer.domElement.style.cursor = 'pointer'; }
      else { CA.tip.hide(); renderer.domElement.style.cursor = ''; }
    }
    renderer.render(scene, camera);
    // HTML labels
    const w = el.canvas.clientWidth, ht = el.canvas.clientHeight;
    const v = new T.Vector3();
    const vis = [];
    labelEls.forEach((l) => {
      v.copy(l.pos).project(camera);
      const show = (opts.labels || l.id === CA.selected) && v.z < 1;
      l.el.style.display = show ? '' : 'none';
      if (show) { l.x = (v.x + 1) / 2 * w; l.y = (1 - v.y) / 2 * ht; vis.push(l); }
    });
    // greedy de-collision: the selected label keeps its place, others step down below any label they would cover
    const LH = 20, placed = [];
    vis.sort((a, b) => (b.id === CA.selected) - (a.id === CA.selected) || a.y - b.y).forEach((l) => {
      if (!l.w) l.w = l.el.offsetWidth;
      const lw = l.w || 100;
      let y = l.y;
      for (let k = 0; k < 6; k++) {
        const hit = placed.find((p) => Math.abs(p.x - l.x) < (p.w + lw) / 2 + 4 && Math.abs(p.y - y) < LH);
        if (!hit) break;
        y = hit.y + LH;
      }
      placed.push({ x: l.x, y, w: lw });
      l.el.style.left = l.x + 'px'; l.el.style.top = y + 'px';
    });
  }

  CA.atlas3d = { flyTo, focusEntity, posOf: (id) => posOf(id), resolve: (id) => resolve(id) };
})();
