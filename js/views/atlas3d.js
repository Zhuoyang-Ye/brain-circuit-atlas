/* 3D atlas: real atlas meshes (human, mouse, macaque or fruit fly; a schematic octopus) with evidence-coded connections to the rest of the brain and body. */
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
    modulator: { color: 0xf778ba, opacity: 0.9 },
  };
  const NM = D.neuromodulation || { tx: {}, sources: [] };
  // one colour per transmitter, for its pathways, its tags on them and the key (dark-theme values; CA.tc maps them)
  const TX_COLORS = { NA: 0x58a6ff, '5-HT': 0xbc8cff, DA: 0xf0883e, ACh: 0x3fb950, HA: 0xe3b341, OX: 0xf778ba, CRF: 0x39c5cf, OA: 0x2dd4bf, GnRH: 0xdb61a2 };
  const txHex = (code) => CA.tc(TX_COLORS[code] != null ? TX_COLORS[code] : 0x8b949e);
  const MOD_SRC = new Set(NM.sources || []);   // neuromodulator source nuclei (drawn pink)
  const BODY_ANCHORS = ['spinal', 'body', 'gut', 'eyes', 'labyrinth'];
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
      modulators: { pos: [7.4, 0.9, -1.6], target: [0.45, -2.0, -1.1] },   // right side, close to brainstem and cerebellum
      motor: { pos: [-15, 4.2, 5.2], target: [-0.6, -0.8, 0.2] },   // left front: frontal motor areas, thalamus, brainstem and spinal cord
      prefrontal: { pos: [-12.5, 2.5, 11.5], target: [0, -1.0, 1.4] },   // front left, a little low: frontal lobe, its undersurface and the brainstem
      'basal-ganglia': { pos: [-10.5, 4.0, 8.5], target: [-0.8, -0.35, 0.3] },   // left front, above: the deep nuclei through the translucent cortex
      hippocampus: { pos: [-12, 0.5, 4], target: [-1.2, -1.3, -0.3] },   // left side, low: the medial temporal lobe through the cortex
      'hip-fields': { pos: [-8.65, -0.1, 2.8], target: [-1.3, -1.35, -0.1] },   // closer: the human atlas does not separate the fields, so the circuit is the entorhinal cortex and hippocampus
      amygdala: { pos: [-11.5, 1.0, 6.5], target: [-0.9, -0.9, 0.3] },   // left front, low: the amygdala, thalamus and brainstem through the cortex
      'amy-nuclei': { pos: [-6.2, -0.45, 3.45], target: [-1.39, -1.31, 0.66] },   // closer: the atlas does not separate the nuclei, so the circuit lies inside the amygdala
      'visual-cortex': { pos: [-13, 3.5, -6.5], target: [-0.8, -0.6, -0.9] },   // left side, behind and above: eye to occipital lobe, temporal areas and pons
      insula: { pos: [-10.5, 5.5, 8], target: [-1.2, -0.4, 0.6] },   // left front, above: the insula under the opercula, thalamus, amygdala and cingulate
      olfactory: { pos: [-10, -4.5, 9], target: [-0.9, -1.6, 2.0] },   // left front, from below: bulb, piriform and orbitofrontal cortex on the underside
    },
    mouse: {
      overview: { pos: [-10, 7, -9], target: [0, -0.5, -0.5] },
      cerebellum: { pos: [-5, 3, -9], target: [0, -0.6, -3.5] },
      left: { pos: [-16, 0.5, 0], target: [0, -0.5, 0] },
      back: { pos: [0, 2, -16], target: [0, -0.5, 0] },
      top: { pos: [0, 16, -0.01], target: [0, 0, 0] },
      below: { pos: [0.01, -15, 1], target: [0, 0, 0] },
      modulators: { pos: [6.5, -6.0, -1.0], target: [0.5, -1.3, -2.2] },   // right side from below, under hippocampus and striatum
      motor: { pos: [-14.5, 5.5, 0.2], target: [-0.3, -0.6, -1.5] },   // left side: motor areas to the spinal cord
      prefrontal: { pos: [-12, 5, 10], target: [0, -0.5, 0.5] },   // front left: frontal pole, thalamus, hippocampus and midbrain
      'basal-ganglia': { pos: [-11, 5, 6], target: [-1.1, -0.45, 0.0] },   // left side, a little in front: striatum to midbrain
      hippocampus: { pos: [-10, 5, -2], target: [-1.2, 0.3, -0.8] },   // left side, above and behind: the hippocampal fields and entorhinal area
      'hip-fields': { pos: [-3.6, 3.65, -8.0], target: [-1.8, 0.45, -0.9] },   // behind, above: the fields as in a coronal section of the dorsal hippocampus
      amygdala: { pos: [-11, -2.5, 4], target: [-1.4, -0.6, 0.0] },   // left side, from below: the amygdalar nuclei and their targets
      'amy-nuclei': { pos: [-7.0, -2.45, 1.8], target: [-2.2, -1.5, -0.2] },   // closer: the lateral, basolateral, central and intercalated nuclei
      'visual-cortex': { pos: [-13, 4.5, -2.5], target: [-1.0, 0.6, -0.5] },   // left side, a little above and behind: eye, geniculate and the visual areas on the dorsal cortex
      insula: { pos: [-12.5, 2.5, 5.5], target: [-2.0, -0.6, 0.6] },   // left side, in front: insular areas on the lateral cortex, amygdala and accumbens
      olfactory: { pos: [-11, -2, 8], target: [-1.5, -1.0, 1.5] },   // left front, a little below: bulb, piriform cortex and cortical amygdala
    },
    macaque: {
      overview: { pos: [-11.5, 5.5, -11], target: [0, -0.8, 0] },
      cerebellum: { pos: [-5.2, 0.6, -9.5], target: [0, -2.6, -2.4] },
      left: { pos: [-17, 0.5, 0], target: [0, -0.8, 0] },
      back: { pos: [0, 1.5, -17], target: [0, -1.2, 0] },
      top: { pos: [0, 17, -0.01], target: [0, 0, 0] },
      below: { pos: [0.01, -16, 2], target: [0, -1, 0] },
      modulators: { pos: [9.5, 0.2, -2.5], target: [0.3, -1.4, -1.0] },   // right side, a little further back than the human view
      motor: { pos: [-15, 4.2, 5.2], target: [-0.6, -0.8, 0.2] },
      prefrontal: { pos: [-10.2, 2.4, 9.6], target: [0, -0.5, 0.9] },   // closer than the human view: the macaque brain is smaller relative to the body parts
      'basal-ganglia': { pos: [-10, 3.8, 8.2], target: [-0.9, -0.25, 0.4] },
      hippocampus: { pos: [-11, 2, 5], target: [-1.1, -0.9, 0.0] },
      'hip-fields': { pos: [-8.4, 0.7, 3.6], target: [-1.5, -1.3, 0.1] },   // nor does the macaque one
      amygdala: { pos: [-10.5, 1.0, 6.5], target: [-0.9, -0.8, 0.5] },
      'amy-nuclei': { pos: [-5.8, -0.4, 3.8], target: [-1.5, -1.2, 1.1] },
      'visual-cortex': { pos: [-13, 3.5, -6], target: [-1.0, -0.3, -0.8] },
      insula: { pos: [-12.5, 1.8, 6], target: [-1.6, -0.3, 1.0] },
      olfactory: { pos: [-10, -3.5, 9.5], target: [-0.9, -0.8, 2.5] },
    },
    // the schematic octopus: y is dorsal, z points toward the arm crown, the optic lobes and eyes sit at the sides
    octopus: {
      overview: { pos: [-11, 6.5, -10], target: [0, -1.2, 0.6] },
      left: { pos: [-16, 1.0, 0.5], target: [0, -0.8, 0.5] },
      back: { pos: [0, 3.0, -16], target: [0, -0.8, 0.3] },
      top: { pos: [0, 16, 0.4], target: [0, 0, 0.3] },
      below: { pos: [0.01, -15, 3], target: [0, -1.5, 1] },
      octopus: { pos: [-4.2, 10.5, -7.8], target: [-0.7, 0.6, -0.1] },   // the central brain, left optic lobe and eye, from above and behind
      'oct-vl': { pos: [-3.2, 5.6, -3.6], target: [0, 1.3, -0.1] },   // closer: the vertical lobe and the superior frontal lobe
      'oct-arms': { pos: [-14, 5.0, 11], target: [0, -1.6, 1.6] },   // left front: the brain above the arm crown
    },
    // the fruit fly (Janelia male CNS): y is dorsal, z anterior (antennal lobes in front), the optic lobes at the sides and
    // the ventral nerve cord behind and below the brain
    fly: {
      overview: { pos: [-12, 7.5, 12], target: [0, -0.5, -1.2] },
      left: { pos: [-17, 1.5, -1.5], target: [0, -0.5, -1.5] },
      back: { pos: [0, 4.5, -17], target: [0, 0, 0] },
      top: { pos: [0, 17, -1], target: [0, 0, -1] },
      below: { pos: [0.01, -16, 3], target: [0, -0.5, -0.5] },
      fly: { pos: [-6.5, 5, 13], target: [-0.3, 0.2, 0.3] },   // front, above and to the left: the antennal lobes, mushroom bodies and central complex
      'fly-mb': { pos: [-3.5, 4.5, 12], target: [-1.0, 0.6, 0.3] },   // from in front and a little above (the nerve cord stays hidden): the left mushroom body, lateral horn and antennal lobe
      'fly-cx': { pos: [-3, 4.5, 12], target: [-1.2, 0.5, 0.3] },   // the left medulla, optic tubercle and the central complex on the midline
      'fly-ol': { pos: [-12, 2.5, 10], target: [-2.4, -0.3, -0.2] },   // the left optic lobe, from the front and side
      'fly-body': { pos: [-19, 4, -4], target: [0, -1.5, -4] },   // from the left: the brain, neck connective and nerve cord
    },
  };
  // the 3D brains on offer: those listed in knowledge.json atlas3d.species (a species is switched off there)
  const SPECIES = [['human', 'Human'], ['macaque', 'Macaque'], ['mouse', 'Mouse'], ['octopus', 'Octopus'], ['fly', 'Fruit fly']].filter(([sp]) => A3.species.includes(sp));
  // A region lists the species it is drawn in (`species`); the mammalian regions leave it out and use these three.
  // The species and the region always match: choosing the octopus (or the fly) switches to one of its regions, and back.
  const MAMMALS = ['human', 'macaque', 'mouse'];
  const speciesOf = (R) => (R.species || MAMMALS).filter((sp) => SPECIES.some(([x]) => x === sp));
  const speciesOK = (R, sp) => speciesOf(R).includes(sp);
  const groupOf = (sp) => (MAMMALS.includes(sp) ? 'mammal' : sp);

  let root, el = {}, renderer, scene, camera, controls, raf = 0, ro, clock, pointer = null, pointerDirty = false;
  let species = CA.store.get('atlas.species', 'human');
  if (!SPECIES.some(([sp]) => sp === species)) species = SPECIES[0][0];
  // `flow` (moving dots) is off by default: arrowheads show direction, and the trace shows the order of steps
  let opts = Object.assign({ shell: true, xray: false, labels: true, bodyParts: true, flow: false, opacity: 0.09, solid: 0 }, CA.store.get('atlas.opts', {}));
  let circuitId = null;   // set per region by pickCircuit()
  // meshes without an entity of their own take the region of the entity drawn as their whole group (cerebellar cortex, nuclei)
  const GROUP_REGION = Object.fromEntries(Object.entries(A3.groups).map(([id, g]) => [g, CA.ent[id] && CA.ent[id].region]));
  let pickables = [], meshObjs = [], linkObjs = [], pulses = [], labelEls = [], markerObjs = [];
  let drawnLinks = [], trace = null;   // the pathways on screen ({l, curve, objs, s, t}); the running step-by-step trace
  let positions = {}, hovered = null, tween = null, unsubs = [], disposed = false, buildToken = 0;
  // entity -> categorical slot (kept while the circuit stays), mesh -> legend row, the hovered row
  let slotOf = new Map(), slotKey = '', ownerOf = new Map(), nameHot = null, layoutKey = '', layoutIdle = 0;
  let switching = false;   // true while a species change switches the region: the scene is rebuilt right after
  // the structures that the pathways on screen (and the selection) touch: they keep their colours, everything else turns
  // grey; null when nothing is drawn or selected, and the current region's structures are coloured instead
  let focusIds = null;
  const geomCache = {};

  CA.register('atlas', { title: '3D atlas', mount, unmount, route, onRegion, onTheme });

  /* ---------------------------------------------------------------- mount */
  function mount(node) {
    root = node;
    disposed = false;
    if (!speciesOK(CA.region, species)) {   // a stored region of another animal (the octopus and the fly have their own regions)
      const mammal = CA.store.get('atlas.mammal', 'human');
      species = speciesOK(CA.region, mammal) ? mammal : speciesOf(CA.region)[0];
    }
    CA.store.set('atlas.region.' + groupOf(species), CA.region.id);
    pickCircuit();
    const wrap = h('div', { class: 'atlas' });
    el.canvas = h('div', { class: 'atlas-canvas' });
    el.labels = h('div', { class: 'atlas-labels' });
    el.msg = h('div', { class: 'atlas-msg' }, 'Loading 3D anatomy…');
    el.controls = buildControls();
    el.names = h('div', { class: 'atlas-names', style: { display: 'none' } });
    el.txOverlay = h('div', { class: 'atlas-txkey', style: { display: 'none' }, 'aria-label': 'Transmitter key' });
    wrap.append(el.canvas, el.labels, el.controls, el.names, el.txOverlay, el.msg);
    if (!CA.store.get('intro.dismissed', false)) wrap.append(el.intro = buildIntro());
    root.appendChild(wrap);

    if (!window.THREE || !webglOK()) {
      el.msg.innerHTML = '<div><h3>3D view unavailable</h3><p>This browser could not start WebGL. The other views (functional map, microcircuit, across scales, evidence & gaps) work without it.</p></div>';
      return;
    }
    initThree();
    unsubs.push(CA.on('select', () => { applyHighlight(); rebuildLinks(); }));
    unsubs.push(CA.on('labels', () => refreshNames()));
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
    const R = CA.region;
    const deeper = [['map', 'functional map'], ['circuit', 'microcircuit'], ['molecules', 'molecules'], ['scales', 'across scales']]
      .filter(([v]) => R.views.includes(v)).slice(0, 3);
    const open = CA.store.get('atlas.introOpen', window.innerWidth > 860);
    const contentId = 'atlas-intro-content';
    let introToggle;
    const box = h('div', { class: 'intro' + (open ? '' : ' shut') },
      h('div', { class: 'intro-head' },
        h('h2', {}, R.intro.title),
        introToggle = h('button', {
          class: 'icon-btn intro-toggle',
          type: 'button',
          'aria-expanded': String(open),
          'aria-controls': contentId,
          title: open ? 'Collapse introduction' : 'Expand introduction',
          'aria-label': open ? 'Collapse introduction' : 'Expand introduction',
          onclick: () => {
            const next = box.classList.toggle('shut');
            CA.store.set('atlas.introOpen', !next);
            introToggle.setAttribute('aria-expanded', String(!next));
            introToggle.title = next ? 'Expand introduction' : 'Collapse introduction';
            introToggle.setAttribute('aria-label', introToggle.title);
          },
        }, open ? '−' : '+')),
      h('div', { id: contentId, class: 'intro-content' },
        h('p', { class: 'small' }, R.intro.text),
        h('ol', { class: 'small' },
        h('li', {}, 'Pick a ', h('b', {}, 'circuit'), ' on the left to see its pathways; arrowheads show their direction. For a loop or chain, ', h('b', {}, 'Trace step by step'), ' follows the signal in order.'),
        h('li', {}, 'Click any structure for its evidence, connections and open questions.'),
        h('li', {}, 'Go deeper: ', deeper.map(([v, label], i) => [i ? ', ' : '', h('a', { href: '#/' + v }, label)]), '.'),
        h('li', {}, 'Find what is unknown in ', h('a', { href: '#/gaps' }, 'Evidence & gaps'), ' and draft tests in the ', h('a', { href: '#/lab' }, 'Hypothesis lab'), '.')),
        h('div', { class: 'row' },
          h('button', { class: 'btn primary', onclick: () => { flyTo(R.view); } }, 'Zoom to ' + R.label.toLowerCase()),
          h('button', { class: 'btn', onclick: () => { CA.store.set('intro.dismissed', true); box.remove(); el.intro = null; } }, 'Got it'))));
    return box;
  }

  /* circuits of the current region, a Neuromodulators entry (the region's own, or one built from its transmitter-tagged
     pathways), and the two generic choices */
  const isNMCircuit = (c) => /neuromod/i.test(c.id + ' ' + c.name);
  // a structure's name inside a sentence: no trailing parenthesis, and lower case unless it starts with an acronym (VTA)
  const inline = (id) => { const n = CA.ent[id].name.replace(/\s*\([^)]*\)$/, ''); return /^[A-Z][a-z]/.test(n) ? n[0].toLowerCase() + n.slice(1) : n; };
  function nmCircuit(R) {
    const own = A3.circuits.find((c) => c.region === R.id && isNMCircuit(c));
    if (own) return Object.assign({ nm: true }, own, { name: 'Neuromodulators' });
    const links = D.links.filter((l) => l.tx && NM.tx[l.tx] && l.regions.includes(R.id) && CA.has3D(l.s) && CA.has3D(l.t));
    const byTx = {};
    links.forEach((l) => { (byTx[l.tx] = byTx[l.tx] || new Set()).add(inline(l.s)); });
    const parts = Object.entries(byTx).map(([tx, srcs]) => `${NM.tx[tx].label.toLowerCase()} (${tx}) from the ${[...srcs].join(' and the ')}`);
    const desc = links.length
      ? `Where the ${R.label.toLowerCase()} gets its neuromodulators: ${parts.join('; ')}. Each transmitter has its own colour, named in the key; arrows point from the source nucleus to its target.`
      : `No neuromodulatory pathway with both ends placed in this atlas is curated for the ${R.label.toLowerCase()} yet.`;
    return { id: 'nm-auto', nm: true, fit: true, name: 'Neuromodulators', desc, links: links.map((l) => l.id) };
  }
  function regionCircuits() {
    return [...A3.circuits.filter((c) => c.region === CA.region.id && !isNMCircuit(c)), nmCircuit(CA.region),
      { id: 'all', name: 'All mapped connections', desc: `Every anatomical or functional link of the ${CA.region.label.toLowerCase()} content with both ends placed in this atlas.` },
      { id: 'none', name: 'Anatomy only', desc: 'Hide pathways. Click a structure to show its own connections.' }];
  }
  const currentCircuit = () => regionCircuits().find((c) => c.id === circuitId) || null;
  const circuitKey = () => 'atlas.circuit' + (CA.region === D.regions[0] ? '' : '.' + CA.region.id);
  function pickCircuit() {
    const list = regionCircuits(), saved = CA.store.get(circuitKey(), null);
    circuitId = list.some((c) => c.id === saved) ? saved : list[0].id;
  }
  function fillCircuits() {
    const list = regionCircuits();
    CA.clear(el.circs);
    list.forEach((c) => el.circs.appendChild(h('button', { class: 'circ' + (c.id === circuitId ? ' on' : ''), 'data-c': c.id, onclick: () => chooseCircuit(c) }, c.name)));
    el.circDesc.textContent = (list.find((c) => c.id === circuitId) || {}).desc || '';
  }
  function chooseCircuit(c) {
    circuitId = c.id; CA.store.set(circuitKey(), c.id);
    el.circs.querySelectorAll('.circ').forEach((b) => b.classList.toggle('on', b.dataset.c === c.id));
    el.circDesc.textContent = c.desc || '';
    // some circuits run inside the cerebellum or under other structures: see through it and move the camera close
    if (c.xray && !opts.xray) { opts.xray = true; CA.store.set('atlas.opts', opts); el.xrayBox.checked = true; applyMaterials(); }
    if (c.view && VIEWS[species][c.view]) flyTo(c.view);
    rebuildLinks();
    if (c.fit && !c.view) flyTo(fitView(c.links));
  }

  /** A camera that frames the ends of these pathways, looking from the current direction. */
  function fitView(linkIds) {
    if (!camera) return null;
    const T = window.THREE;
    const pts = [];
    linkIds.forEach((id) => { const l = CA.link[id]; if (l) [posOf(l.s), posOf(l.t)].forEach((p) => { if (p) pts.push(p); }); });
    if (!pts.length) return null;
    const box = new T.Box3().setFromPoints(pts);
    const centre = box.getCenter(new T.Vector3()), r = Math.max(2, box.getSize(new T.Vector3()).length() / 2);
    const dir = camera.position.clone().sub(controls.target).normalize();
    const dist = CA.clamp(r / Math.sin((camera.fov * Math.PI / 180) / 2) * 1.1, controls.minDistance + 1, controls.maxDistance - 1);
    return { pos: centre.clone().add(dir.multiplyScalar(dist)).toArray(), target: centre.toArray() };
  }

  /** The region changed (the dropdown in the left panel): swap circuits, notes and emphasis, and fly to the region. */
  function onRegion(R) {
    pickCircuit();
    fillCircuits();
    if (el.intro) { const fresh = buildIntro(); el.intro.replaceWith(fresh); el.intro = fresh; }
    if (!speciesOK(R, species)) {   // a region of another animal, picked from the menu: switch the species too
      const mammal = CA.store.get('atlas.mammal', 'human');
      species = speciesOK(R, mammal) ? mammal : speciesOf(R)[0];
      CA.store.set('atlas.species', species);
      markSpecies();
      CA.store.set('atlas.region.' + groupOf(species), R.id);
      loadSpecies(species);
      return;
    }
    CA.store.set('atlas.region.' + groupOf(species), R.id);
    el.speciesNote.textContent = (R.speciesNote || {})[species] || '';
    if (!scene || switching) return;
    applyMaterials();
    applyHighlight();
    rebuildLinks();
    const c = currentCircuit();
    if (c && c.fit && !c.view) flyTo(fitView(c.links) || R.view);
    else flyTo(c && c.view && VIEWS[species][c.view] ? c.view : R.view);
  }

  /** Switch species. The octopus and the fly have their own regions and the mammals theirs, so a switch across them also switches the
   *  region, to the one last used for that animal; the scene is then rebuilt for the new species. */
  function chooseSpecies(sp) {
    if (sp === species) return;
    species = sp;
    CA.store.set('atlas.species', sp);
    if (MAMMALS.includes(sp)) CA.store.set('atlas.mammal', sp);
    markSpecies();
    if (!speciesOK(CA.region, sp)) {
      const last = CA.store.get('atlas.region.' + groupOf(sp), null);
      const R = D.regions.find((r) => r.id === last && speciesOK(r, sp)) || D.regions.find((r) => speciesOK(r, sp));
      if (R) { switching = true; try { CA.setRegion(R.id); } finally { switching = false; } }
    }
    loadSpecies(sp);
  }
  function markSpecies() {
    if (el.seg) el.seg.querySelectorAll('button').forEach((b) => b.classList.toggle('on', b.dataset.sp === species));
  }
  /** Camera presets: the regions drawn in this species, plus the fixed directions. */
  function fillViews() {
    if (!el.views) return;
    CA.clear(el.views);
    [['overview', 'Overview'], ...D.regions.filter((r) => speciesOK(r, species)).map((r) => [r.view, r.label]), ['left', 'Left'], ['back', 'Back'], ['top', 'Top'], ['below', 'Below']]
      .forEach(([k, label]) => el.views.appendChild(h('span', { class: 'chip', onclick: () => flyTo(k) }, label)));
  }

  function buildControls() {
    const box = h('div', { class: 'atlas-controls' });
    const fold = h('button', {
      class: 'atlas-fold-toggle icon-btn',
      type: 'button',
      'aria-expanded': 'true',
      title: 'Collapse atlas controls',
      'aria-label': 'Collapse atlas controls',
      onclick: () => {
        const folded = box.classList.toggle('folded');
        fold.setAttribute('aria-expanded', String(!folded));
        fold.title = folded ? 'Expand atlas controls' : 'Collapse atlas controls';
        fold.setAttribute('aria-label', fold.title);
      },
    }, '‹');
    box.append(fold);
    if (window.matchMedia && window.matchMedia('(max-width: 860px)').matches) {
      box.classList.add('folded');
      fold.setAttribute('aria-expanded', 'false');
      fold.title = 'Expand atlas controls';
      fold.setAttribute('aria-label', fold.title);
    }
    const seg = el.seg = h('div', { class: 'seg species-seg' },
      SPECIES.map(([sp, label]) => h('button', { class: sp === species ? 'on' : '', 'data-sp': sp, onclick: () => chooseSpecies(sp) }, label)));
    el.speciesNote = h('div', { class: 'desc' });
    el.circs = h('div', {});
    el.circDesc = h('div', { class: 'desc' });
    el.txKey = h('div', { class: 'tx-key', style: { display: 'none' } });
    el.traceBtn = h('button', { class: 'btn', title: 'Send one pulse through the circuit in order, lighting each structure as it arrives. The order follows the circuit\'s pathways; the timing is schematic.',
      onclick: () => (trace ? stopTrace() : startTrace()) }, '▶ Trace step by step');
    el.traceInfo = h('div', {});
    el.traceBox = h('div', { class: 'trace', style: { display: 'none' } }, el.traceBtn, el.traceInfo);
    fillCircuits();
    const check = (key, label, fn, title) => h('label', { class: 'check small', title },
      h('input', { type: 'checkbox', checked: opts[key], onchange: (ev) => { opts[key] = ev.target.checked; CA.store.set('atlas.opts', opts); fn(); } }), label);
    const views = el.views = h('div', { class: 'chips' });
    fillViews();
    el.credit = h('div', { class: 'atlas-credit' });
    const xrayLabel = check('xray', 'X-ray cerebellum (see nuclei)', applyMaterials);
    el.xrayBox = xrayLabel.querySelector('input');
    CA.append(box,
      h('h4', { style: { marginTop: 0 } }, 'Species'), seg, el.speciesNote,
      D.regions.length > 1 ? [h('h4', {}, 'Region'), CA.regionPicker()] : null,
      h('h4', {}, 'Circuits'), el.circs, el.circDesc, el.txKey, el.traceBox,
      h('h4', {}, 'Display'),
      check('shell', 'Brain surface', applyMaterials),
      h('input', { type: 'range', min: 0.03, max: 0.35, step: 0.01, value: opts.opacity, style: { width: '100%' },
        oninput: (ev) => { opts.opacity = +ev.target.value; CA.store.set('atlas.opts', opts); applyMaterials(); } }),
      h('div', { class: 'small', style: { marginTop: '6px' } }, 'Structures: see-through ↔ solid'),
      h('input', { type: 'range', min: -1, max: 1, step: 0.05, value: opts.solid, style: { width: '100%' },
        title: 'Opacity of the brain structures. The middle keeps the default look; double-click to reset.',
        oninput: (ev) => { opts.solid = +ev.target.value; CA.store.set('atlas.opts', opts); applyMaterials(); },
        ondblclick: (ev) => { ev.target.value = 0; opts.solid = 0; CA.store.set('atlas.opts', opts); applyMaterials(); } }),
      xrayLabel,
      check('labels', 'Labels', () => rebuildLinks(), 'Name the structures, on the model or in the legend at the side (switch next to the theme button).'),
      check('bodyParts', 'Body & senses', showMarkers),
      check('flow', 'Animate signal flow', () => {}, 'Dots also travel along every pathway, from source to target. Dot color follows the evidence grade, and hypothetical links move at half speed. The motion is schematic, not real conduction timing.'),
      h('h4', {}, 'Camera'), views, el.credit);
    return box;
  }

  /** The background and labels follow the CSS theme; recolour the brain surface and pathways in place. */
  function onTheme() {
    if (!scene) return;
    meshObjs.forEach((m) => { if (m.userData.rec.group === 'shell') m.material.color.setHex(CA.tc(GROUP.shell.color)); });
    rebuildLinks();
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
    el.speciesNote.textContent = (CA.region.speciesNote || {})[sp] || '';
    fillViews();
    CA.loadScript(`js/data/meshes_${sp}.js`).then(() => {
      if (disposed || token !== buildToken) return;
      const bundle = window.CA_MESHES && window.CA_MESHES[sp];
      if (!bundle) throw new Error('mesh bundle missing for ' + sp);
      buildScene(sp, bundle);
      el.msg.style.display = 'none';
      const r = CA.parseHash();
      const circ = currentCircuit();
      const fit = circ && circ.fit && !circ.view && fitView(circ.links);
      if (r.kind === 'e' && CA.ent[r.id]) focusEntity(r.id, true);
      else if (fit) { camera.position.fromArray(fit.pos); controls.target.fromArray(fit.target); controls.update(); }
      else jumpTo(circ && circ.view && VIEWS[sp][circ.view] ? circ.view : 'overview');
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
    stopTrace();
    [...meshObjs, ...linkObjs, ...markerObjs].forEach(kill);
    meshObjs = []; linkObjs = []; markerObjs = []; pickables = []; pulses = []; drawnLinks = []; ownerOf = new Map();
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
      let color = rec.group === 'shell' ? CA.tc(style.color) : style.color;   // the surface darkens on a light background
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
      // a structure drawn only by schematic (hand-placed) meshes is approximate: labelled in italics with ≈
      return { c, l: mean(recs.filter((r) => r.side !== 'R').map((r) => r.cl)) || c, r: mean(recs.filter((r) => r.side !== 'L').map((r) => r.cr)) || c,
        approx: recs.every((r) => r.approx) };
    };
    const byEnt = {};
    bundle.meshes.forEach((r) => { if (r.entity) (byEnt[r.entity] = byEnt[r.entity] || []).push(r); });
    Object.entries(byEnt).forEach(([id, recs]) => { positions[id] = agg(recs); });
    Object.entries(A3.composite || {}).forEach(([id, kids]) => {   // an umbrella entity sits at the middle of its parts
      if (!positions[id]) {
        const p = agg(bundle.meshes.filter((r) => kids.includes(r.entity)));
        if (p) positions[id] = p;
      }
    });
    Object.entries(A3.groups).forEach(([id, group]) => {
      if (!positions[id]) {
        const p = agg(bundle.meshes.filter((r) => r.group === group));
        if (p) positions[id] = p;
      }
    });
    Object.entries(bundle.anchors || {}).forEach(([id, a]) => {
      if (!positions[id]) positions[id] = { c: new T.Vector3(...a[0]), l: new T.Vector3(...a[1]), r: new T.Vector3(...a[2]), approx: !BODY_ANCHORS.includes(id), marker: true };
    });
  }

  function sideOf(id) {
    for (const [side, ids] of Object.entries(A3.sides)) if (ids.includes(id)) return side;
    return 'C';
  }
  function resolve(id) {
    if (positions[id]) return id;
    const alias = (A3.aliases[species] || {})[id];
    if (alias && positions[alias]) return alias;
    return ((A3.composite || {})[id] || []).find((k) => positions[k]) || null;
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
    const human = sp !== 'mouse';   // primate marker sizes
    const add = (obj, entity, body) => {
      obj.userData.entity = entity; obj.userData.body = body; obj.userData.marker = true;
      scene.add(obj); markerObjs.push(obj); pickables.push(obj);
    };
    const mat = (c, o) => {
      const m = new T.MeshStandardMaterial({ color: c, roughness: 0.5, transparent: true, opacity: o == null ? 0.9 : o, emissive: c, emissiveIntensity: 0.12 });
      m.userData.base = c;   // restored when the legend gives the structure a colour of its own and then takes it back
      m.userData.op0 = m.opacity;
      return m;
    };
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
      if (!p.approx || !p.marker) return;   // a marker only where no mesh stands for the structure
      const side = sideOf(id);
      const color = MOD_SRC.has(id) ? GROUP.modulator.color : CA.ent[id] && CA.ent[id].kind === 'area' ? GROUP.cortex.color : 0x3fb9a5;
      const m = new T.Mesh(new T.OctahedronGeometry(human ? 0.16 : 0.12), mat(color, 0.95));
      m.position.copy(side === 'R' ? p.r : side === 'L' ? p.l : p.c);
      add(m, id, false);
      m.userData.approx = true;
    });
    showMarkers();
  }

  /** Body parts follow their checkbox; approximate markers show for the current region's structures (or the selection). */
  function showMarkers() {
    markerObjs.forEach((m) => {
      const id = m.userData.entity;
      m.visible = m.userData.body ? opts.bodyParts : !m.userData.approx || CA.inRegion(id) || CA.selected === id;
    });
  }

  /* -------- materials, highlight -------- */
  function selectedSet() {
    const id = CA.selected;
    if (!id) return new Set();
    const s = new Set([id, ...((A3.composite || {})[id] || [])]);
    const rid = resolve(id);
    if (rid) s.add(rid);
    return s;
  }

  /** The region a mesh belongs to: its entity's, else that of the entity drawn as its whole group; null if shared. */
  function meshRegion(r) {
    const e = CA.ent[r.entity || r.related];
    return (e && e.region) || GROUP_REGION[r.group] || null;
  }
  /** Whether a mesh's structure takes part in the current region's content (shared structures and umbrella entities included). */
  function meshInRegion(r) {
    const id = r.entity || r.related;
    if (!id) return !GROUP_REGION[r.group] || GROUP_REGION[r.group] === CA.region.id;
    return CA.inRegion(id) || Object.entries(A3.composite || {}).some(([p, kids]) => kids.includes(id) && CA.inRegion(p));
  }

  /** The "Structures" slider: 0 keeps the default emphasis, 1 makes every structure opaque, -1 nearly invisible. */
  function solidify(o) {
    const s = CA.clamp(+opts.solid || 0, -1, 1);
    return s >= 0 ? o + (1 - o) * s : o * (1 + 0.85 * s);
  }

  /* Colour and opacity, in one place. Every structure is drawn in a light tint of its colour; the one under the pointer
   * (on the model or in the legend) in a deep, solid version, so it stands out. While pathways are drawn (a circuit, or
   * the selection's connections), only the structures they touch keep their colours and the rest of the brain turns
   * grey and faint; the touched structures stay see-through, so the pathways and their arrowheads inside them show. */
  const TINT = 0.45, DEEPEN = { dark: 0.15, light: 0.3 };
  const relevant = (o) => !focusIds || [...focusIds].some((rid) => claimRank(rid, o) >= 0);
  function meshOpacity(m, fit, hov) {
    const r = m.userData.rec;
    let o = m.userData.baseOpacity;
    if (hov) o = 0.92;
    else if (focusIds) o = !fit ? Math.min(o, 0.1) : Math.min(Math.max(o, 0.5), drawnLinks.length ? 0.55 : 0.85);
    else {
      const reg = meshRegion(r);
      if (reg === CA.region.id) o = Math.max(o, 0.75);           // the current region stands out
      else if (!meshInRegion(r)) o = Math.min(o, o > 0.6 ? 0.5 : 0.2);   // structures outside its content recede
      else if (reg && o > 0.6) o = 0.5;                           // another region's structures, kept as context
    }
    if (!hov && legendOn() && slotOf.has(ownerOf.get(m))) o = Math.max(o, 0.45);   // a structure with a legend colour of its own shows it
    if (r.group === 'cerebellum' && opts.xray && !hov) return 0.22;   // x-ray keeps the cerebellum see-through
    return hov ? o : solidify(o);
  }
  function paint() {
    if (!scene) return;
    showMarkers();
    const T = window.THREE;
    const sel = selectedSet(), hotRid = nameHot && resolve(nameHot);   // the structure hovered in the legend
    const pal = PALETTE[CA.theme === 'light' ? 'light' : 'dark'];
    const grey = new T.Color(CA.tc(0x8b949e)), white = new T.Color(0xffffff), black = new T.Color(0x000000);
    const deepen = DEEPEN[CA.theme === 'light' ? 'light' : 'dark'];
    meshObjs.forEach((m) => { if (m.userData.rec.group === 'shell') { m.visible = opts.shell; m.material.opacity = opts.opacity; } });
    meshObjs.filter((m) => m.userData.rec.group !== 'shell').concat(markerObjs).forEach((o) => {
      const rel = o.userData.rec && o.userData.rec.related;
      const on = (o.userData.entity && sel.has(o.userData.entity)) || (rel && sel.has(rel));
      const hov = (hovered && hovered === o) || (hotRid && ownerOf.get(o) === hotRid);
      const fit = relevant(o);
      const slot = legendOn() ? slotOf.get(ownerOf.get(o)) : undefined;
      if (o.userData.rec) {
        const op = meshOpacity(o, fit, hov);
        o.material.opacity = op;
        o.material.depthWrite = op > 0.8;   // see-through surfaces must not hide the pathways behind them
        o.material.needsUpdate = true;
      }
      o.traverse((c) => {
        if (!c.material || !c.material.color) return;
        const base = new T.Color(slot != null ? pal[slot] : c.material.userData.base != null ? c.material.userData.base : o.userData.base);
        const col = hov || on ? base.clone().lerp(black, deepen)   // hovered or selected: deep and solid
          : !fit ? grey                                            // not on the pathways shown: colourless
            : slot != null ? base                                  // a legend colour: as its swatch shows it
              : base.clone().lerp(white, TINT);                    // everything else: a light tint
        c.material.color.copy(col);
        if (!o.userData.rec && c.material.userData.op0 != null) {   // markers and body parts
          c.material.opacity = hov ? Math.max(c.material.userData.op0, 0.92) : fit ? c.material.userData.op0 : Math.min(c.material.userData.op0, 0.25);
        }
        if (c.material.emissive) {
          c.material.emissive.copy(on ? new T.Color(0x4a7dff) : col);
          c.material.emissiveIntensity = on ? 0.45 : o.userData.marker && !hov ? 0.12 : 0;
        }
      });
    });
    // and the legend row of whatever the pointer is on, in the legend or on the model
    const hovRid = hovered && ownerOf.get(hovered);
    if (el.names) el.names.querySelectorAll('.nm').forEach((n) => n.classList.toggle('hot', n.dataset.id === nameHot || (!!hovRid && n.dataset.rid === hovRid)));
  }
  const applyMaterials = paint, applyHighlight = paint;

  /* -------- connections -------- */
  function activeLinks() {
    const ids = new Set();
    if (circuitId === 'all') D.links.forEach((l) => { if ((l.kind === 'anatomical' || l.kind === 'functional') && l.regions.includes(CA.region.id)) ids.add(l.id); });
    else if (circuitId !== 'none') (currentCircuit() || { links: [] }).links.forEach((x) => ids.add(x));
    const sel = CA.selected;
    if (sel) CA.linksOf(sel).forEach((l) => { if (l.kind === 'anatomical' || l.kind === 'functional') ids.add(l.id); });
    return [...ids].map((id) => CA.link[id]).filter(Boolean);
  }

  function rebuildLinks() {
    if (!scene) return;
    const T = window.THREE;
    stopTrace();
    linkObjs.forEach((o) => { scene.remove(o); o.traverse((c) => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); }); });
    pickables = pickables.filter((p) => !p.userData.link);
    linkObjs = []; pulses = []; drawnLinks = [];
    labelEls.forEach((l) => l.el.remove()); labelEls = []; layoutKey = '';
    const human = species !== 'mouse';   // primate tube sizes
    const sel = CA.selected;
    const drawn = new Set(), txSeen = {};   // transmitter code -> names of the source structures
    const at = (id) => { const p = posOf(id); return p ? p.toArray().map((x) => x.toFixed(2)).join(',') : id; };
    const keyOf = (s, t) => at(s) + '|' + at(t);   // links between the same two points are drawn once
    const links = activeLinks();
    const circ = currentCircuit(), nmMode = !!(circ && circ.nm);   // in a neuromodulator circuit, pathways take their transmitter's colour
    const keys = new Set(links.map((l) => keyOf(l.s, l.t)));
    const collapsed = [];   // pathways with both ends in one mesh (the human amygdala's nuclei): not drawn
    links.forEach((l) => {
      const a = posOf(l.s), b = posOf(l.t);
      if (!a || !b) return;
      if (a.distanceTo(b) < 0.08) { collapsed.push(l); return; }
      const key = keyOf(l.s, l.t);
      if (drawn.has(key)) return;   // e.g. dentate and DCN share one position in the human atlas
      drawn.add(key);
      const dist = a.distanceTo(b);
      const mid = a.clone().add(b).multiplyScalar(0.5);
      const out = mid.clone(); if (out.length() < 0.01) out.set(0, 1, 0);
      out.normalize();
      const ctrl = mid.clone().add(out.clone().multiplyScalar(0.16 * dist + 0.35));
      // a pathway drawn in both directions: bow the two curves apart (the cross product flips with direction)
      if (keys.has(keyOf(l.t, l.s))) {
        const perp = b.clone().sub(a).cross(out);
        if (perp.length() > 1e-6) ctrl.add(perp.normalize().multiplyScalar(0.12 * dist + 0.2));
      }
      const curve = new T.QuadraticBezierCurve3(a, ctrl, b);
      const txOn = nmMode && l.tx && NM.tx[l.tx];
      const color = new T.Color(txOn ? txHex(l.tx) : CA.statusColor(l.status));
      const focus = sel && (l.s === sel || l.t === sel);
      const dashed = l.kind === 'functional' || l.status === 'hypothesis' || l.status === 'debated';
      let obj;
      if (dashed) {
        const g = new T.BufferGeometry().setFromPoints(curve.getPoints(64));
        obj = new T.Line(g, new T.LineDashedMaterial({ color: l.kind === 'functional' && l.status !== 'hypothesis' && !txOn ? CA.tc(0x9aa4b2) : color, dashSize: 0.16, gapSize: 0.1, transparent: true, opacity: 0.95 }));
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
      const objs = [obj];
      // arrowheads a little past the middle show the direction, in still images too (the ends sit inside the structures)
      const headColor = l.kind === 'functional' && l.status !== 'hypothesis' && !txOn ? new T.Color(CA.tc(0x9aa4b2)) : color;
      const headR = (human ? 0.17 : 0.135) * (focus ? 1.25 : 1) * (txOn ? 0.7 : 1);   // neuromodulatory pathways often converge: smaller heads
      // two heads on a long pathway, and on every neuromodulatory one, so its direction reads even where an end is hidden
      (dist > 9 || txOn ? [0.36, 0.7] : [0.58]).forEach((u) => {
        const cone = new T.Mesh(new T.ConeGeometry(headR, headR * 2.7, 14), new T.MeshBasicMaterial({ color: headColor, transparent: true, opacity: 0.95 }));
        cone.position.copy(curve.getPointAt(u));
        cone.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), curve.getTangentAt(u).normalize());   // a cone points along +y
        cone.renderOrder = 6;
        cone.userData.link = l; pickables.push(cone);
        scene.add(cone); linkObjs.push(cone); objs.push(cone);
      });
      objs.forEach((o) => { o.userData.op = o.material.opacity; o.userData.color = o.material.color.clone(); });   // restored after a trace
      drawnLinks.push({ l, curve, objs, s: at(l.s), t: at(l.t) });   // the trace joins pathways by position (two entities can share one)
      const n = Math.max(1, Math.round(dist / 3));
      for (let k = 0; k < n; k++) {
        const s = new T.Mesh(new T.SphereGeometry(human ? 0.085 : 0.07, 10, 8), new T.MeshBasicMaterial({ color: color.clone().lerp(new T.Color(0xffffff), 0.45) }));
        s.renderOrder = 6;
        scene.add(s); linkObjs.push(s);
        pulses.push({ mesh: s, curve, offset: k / n, speed: 0.22 / Math.max(1, dist / 4) * (l.status === 'hypothesis' ? 0.5 : 1) });
      }
      [l.s, l.t].forEach((id) => addLabel(id, true));
      if (l.tx && NM.tx[l.tx]) {   // transmitter tag at the middle of the pathway, in the transmitter's colour
        const hex = hexCss(txHex(l.tx));
        const tag = h('div', { class: 'alabel tx', title: NM.tx[l.tx].label, style: { color: hex, borderColor: hex } }, l.tx);
        el.labels.appendChild(tag);
        labelEls.push({ id: 'tx:' + l.id, el: tag, pos: curve.getPoint(0.5), tag: true });
        (txSeen[l.tx] = txSeen[l.tx] || new Set()).add(inline(l.s));
      }
    });
    // name the structure that holds an undrawn pathway, unless a label already marks that spot
    collapsed.forEach((l) => {
      const p = posOf(l.s), rid = resolve(l.s);
      if (rid && !labelEls.some((x) => !x.tag && x.pos.distanceTo(p) < 0.08)) addLabel(rid, true);
    });
    renderTxKey(txSeen);
    // the structures these pathways touch keep their colours; the rest of the brain turns grey
    focusIds = null;
    if (drawnLinks.length || collapsed.length || sel) {
      focusIds = new Set();
      const add = (id) => { if (!id) return; focusIds.add(id); const rid = resolve(id); if (rid) focusIds.add(rid); ((A3.composite || {})[id] || []).forEach((k) => focusIds.add(k)); };
      drawnLinks.forEach((d) => { add(d.l.s); add(d.l.t); });
      collapsed.forEach((l) => { add(l.s); add(l.t); });
      add(sel);
    }
    if (sel) addLabel(sel, true);
    if (opts.labels && circuitId === 'none' && !sel) Object.keys(positions).forEach((id) => { if (CA.ent[id] && !['body', 'gut', 'spinal'].includes(id)) addLabel(id); });
    showTraceButton();
    refreshNames();
  }

  /* -------- step-by-step trace -------- */
  const HOP_MS = 1300, PAUSE_MS = 500, END_MS = 1500, TRACE_COLOR = '#56d364';   // a colour no evidence grade or structure uses

  /** The current circuit's pathways on screen, in steps: in the circuit's own order, with consecutive pathways out of one
   *  structure (or into one) travelling together. Only a chain or loop has an order to trace, so every step must leave
   *  from where the step before arrived; parallel pathways (several outputs of one area, say) get no steps. */
  function traceSteps() {
    const c = currentCircuit();
    if (!c || !c.links) return [];
    const steps = [];
    drawnLinks.filter((d) => c.links.includes(d.l.id)).sort((a, b) => c.links.indexOf(a.l.id) - c.links.indexOf(b.l.id)).forEach((d) => {
      const last = steps[steps.length - 1];
      if (last && (last.every((x) => x.s === d.s) || last.every((x) => x.t === d.t))) last.push(d);
      else steps.push([d]);
    });
    // where a step arrived: the point, the structure, the one whose mesh it borrows, and its parts or its umbrella
    // (PT neurons borrow M1, which is part of the motor cortex)
    const comp = A3.composite || {};
    const arrived = (st) => new Set(st.flatMap((d) => {
      const ids = [d.l.t, resolve(d.l.t)].filter(Boolean);
      return [d.t, ...ids, ...ids.flatMap((id) => comp[id] || []), ...Object.keys(comp).filter((p) => ids.some((id) => comp[p].includes(id)))];
    }));
    for (let k = 1; k < steps.length; k++) {
      const reached = arrived(steps[k - 1]);
      if (!steps[k].some((d) => reached.has(d.s) || reached.has(d.l.s) || reached.has(resolve(d.l.s)))) return [];
    }
    return steps;
  }

  /** The trace button shows for a chain or loop of two or more steps; a finished trace keeps its list of steps. */
  function showTraceButton(keep) {
    if (!el.traceBox) return;
    el.traceBox.style.display = trace || traceSteps().length >= 2 ? '' : 'none';
    el.traceBtn.textContent = trace ? '■ Stop' : keep ? '▶ Trace again' : '▶ Trace step by step';
    if (!trace && !keep) CA.clear(el.traceInfo);
  }

  function startTrace() {
    const steps = traceSteps();
    if (steps.length < 2 || !scene) return;
    const T = window.THREE, human = species !== 'mouse';
    trace = { steps, k: -1, t0: 0, arrived: 0, ended: 0, dots: [], lit: new Map(), color: new T.Color(CA.tc(TRACE_COLOR)),
      dotGeo: new T.SphereGeometry(human ? 0.2 : 0.15, 16, 12), haloGeo: new T.SphereGeometry(human ? 0.45 : 0.34, 16, 12) };
    drawnLinks.forEach((d) => d.objs.forEach((o) => { o.material.opacity = 0.14; }));   // every pathway dims and lights up as the pulse travels it
    CA.clear(el.traceInfo).append(el.traceList = h('ol', { class: 'trace-steps' }));
    nextStep(performance.now());
    showTraceButton();
  }

  function nextStep(now) {
    const T = window.THREE, tr = trace;
    tr.dots.forEach((m) => { scene.remove(m); m.material.dispose(); });
    tr.dots = [];
    tr.k += 1; tr.t0 = now; tr.arrived = 0;
    const step = tr.steps[tr.k];
    step.forEach((d) => {
      lightUp(d.l.s, now, false);   // already lit, unless this pathway joins the trace here
      d.objs.forEach((o) => { o.material.opacity = 1; o.material.color.copy(tr.color); });   // the pathway being travelled takes the pulse's colour
      // the pulse draws last and over everything, so it stays visible where the pathway runs through a structure
      const dot = new T.Mesh(tr.dotGeo, new T.MeshBasicMaterial({ color: tr.color, transparent: true, depthTest: false }));
      const halo = new T.Mesh(tr.haloGeo, new T.MeshBasicMaterial({ color: tr.color, transparent: true, opacity: 0.3, depthTest: false, depthWrite: false }));
      [halo, dot].forEach((m, j) => { m.renderOrder = 20 + j; m.position.copy(d.curve.getPointAt(0)); scene.add(m); tr.dots.push(m); });
    });
    const name = (id) => CA.ent[id].name;
    el.traceList.querySelectorAll('li.now').forEach((li) => li.classList.remove('now'));
    const li = h('li', { class: 'now' }, step.map((d) => h('div', { class: 'hop' },
      h('b', {}, name(d.l.s) + ' → ' + name(d.l.t)), h('div', { class: 'rel', title: d.l.rel }, d.l.rel))));
    el.traceList.append(li);
    li.scrollIntoView({ block: 'nearest' });
  }

  /** A structure glows once the pulse reaches it, and flashes on arrival: its meshes, an umbrella entity's parts, the mesh
   *  it borrows, or its whole mesh group (the cerebellar cortex is every lobule, the deep nuclei every nucleus). */
  function lightUp(id, now, flash) {
    const ids = new Set([id, ...((A3.composite || {})[id] || [])]);
    const rid = resolve(id);
    if (rid) ids.add(rid);
    const groups = new Set([...ids].map((x) => A3.groups[x]).filter(Boolean));
    meshObjs.concat(markerObjs).forEach((m) => {
      const r = m.userData.rec;
      const hit = ids.has(m.userData.entity) || (r && (ids.has(r.related) || groups.has(r.group)));
      if (hit && (flash || !trace.lit.has(m))) trace.lit.set(m, now);
    });
    labelEls.forEach((l) => { if (ids.has(l.id)) l.el.classList.add('lit'); });
    el.names.querySelectorAll('.nm').forEach((n) => { if (ids.has(n.dataset.id) || ids.has(n.dataset.rid)) n.classList.add('lit'); });
  }

  function runTrace(now) {
    const tr = trace, step = tr.steps[tr.k];
    const u = Math.min(1, (now - tr.t0) / HOP_MS), e = u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
    step.forEach((d, i) => { const p = d.curve.getPointAt(e); tr.dots[2 * i].position.copy(p); tr.dots[2 * i + 1].position.copy(p); });   // halo, dot
    if (u >= 1 && !tr.arrived) {
      tr.arrived = now;
      step.forEach((d) => { lightUp(d.l.t, now, true); d.objs.forEach((o) => { o.material.opacity = 0.75; o.material.color.copy(o.userData.color); }); });
    }
    tr.lit.forEach((t0, m) => m.traverse((c) => {
      if (!c.material || !c.material.emissive) return;
      c.material.emissive.copy(tr.color);
      c.material.emissiveIntensity = 0.3 + 0.9 * Math.exp(-(now - t0) / 380);
      if (c.material.opacity < 0.55) c.material.opacity = 0.55;
    }));
    if (tr.arrived && !tr.ended && now - tr.arrived > PAUSE_MS) {
      if (tr.k + 1 < tr.steps.length) nextStep(now);
      else { tr.ended = now; tr.dots.forEach((m) => { m.visible = false; }); }
    }
    if (tr.ended && now - tr.ended > END_MS) stopTrace(true);
  }

  /** End the trace and restore the pathways and the materials; a finished trace leaves its list of steps. */
  function stopTrace(finished) {
    const tr = trace;
    if (!tr) return;
    trace = null;
    tr.dots.forEach((m) => { if (scene) scene.remove(m); m.material.dispose(); });
    tr.dotGeo.dispose(); tr.haloGeo.dispose();
    labelEls.forEach((l) => l.el.classList.remove('lit'));
    el.names.querySelectorAll('.nm.lit').forEach((n) => n.classList.remove('lit'));
    drawnLinks.forEach((d) => d.objs.forEach((o) => { o.material.opacity = o.userData.op; o.material.color.copy(o.userData.color); }));
    if (scene) { applyMaterials(); applyHighlight(); }
    if (finished) el.traceList.querySelectorAll('li.now').forEach((li) => li.classList.remove('now'));
    showTraceButton(finished);
  }

  /** A structure's name as labels and the legend show it: where it borrows another's mesh, and ≈ if placed by hand. */
  function labelText(id) {
    const rid = resolve(id);
    const approx = rid && positions[rid].approx;
    const viaAlias = rid && rid !== id;
    return CA.ent[id].name + (viaAlias ? ' (in ' + CA.ent[rid].name.replace(/\s*\([^)]*\)$/, '').toLowerCase() + ')' : '') + (approx ? ' ≈' : '');
  }

  /** Name a structure (`path`: it is on a pathway on screen, or selected, so the legend may give it a colour). */
  function addLabel(id, path) {
    const had = labelEls.find((l) => l.id === id);
    if (had) { if (path) had.path = true; return; }
    const p = posOf(id);
    if (!p || !CA.ent[id]) return;
    const rid = resolve(id);
    const approx = rid && positions[rid].approx;
    const e = h('div', { class: 'alabel' + (approx ? ' approx' : '') + (CA.selected === id ? ' sel' : '') }, labelText(id));
    el.labels.appendChild(e);
    labelEls.push({ id, el: e, pos: p, path: !!path });
  }

  /** The transmitter key: each transmitter on screen, its colour, full name and source; in the left panel and on the canvas. */
  function renderTxKey(seen) {
    const codes = Object.keys(NM.tx).filter((c) => seen[c]).concat(Object.keys(seen).filter((c) => !NM.tx[c]));
    const pill = (c) => { const hex = hexCss(txHex(c)); return h('span', { class: 'txp', style: { color: hex, borderColor: hex } }, c); };
    const full = (c) => (NM.tx[c] ? NM.tx[c].label : c);
    if (el.txKey) {
      CA.clear(el.txKey);
      el.txKey.style.display = codes.length ? '' : 'none';
      if (codes.length) CA.append(el.txKey, h('div', { class: 'tiny muted' }, 'Transmitters on these pathways'),
        codes.map((c) => h('div', { class: 'txr' }, pill(c), h('span', {}, h('b', {}, full(c)), h('span', { class: 'muted' }, ' from the ' + [...seen[c]].join(' and the '))))));
    }
    if (el.txOverlay) {
      CA.clear(el.txOverlay);
      el.txOverlay.style.display = codes.length ? '' : 'none';
      codes.forEach((c) => el.txOverlay.appendChild(h('span', { class: 'txr' }, pill(c), full(c))));
    }
  }

  /* -------- the legend at the side: names off the model, colour-coded --------
   * The header switch next to the theme button puts the names here instead of on the model. The structures on the
   * pathways on screen (and the selection) take a colour of their own, painted on the model, from one categorical
   * palette in a fixed order: up to eight, the first structures of the circuit, and a structure keeps its colour while
   * the circuit stays (selecting something only adds colours). Every other structure keeps its atlas colour, which its
   * swatch shows. Colour is never the only link: hovering a name lights the structure and names it on the model, and
   * hovering the model lights its row. Palette: validated for both themes (CVD and normal-vision separation of
   * neighbouring slots, lightness band); the light steps of aqua, yellow and pink are under 3:1 against the panel,
   * so every swatch sits beside its name. */
  const PALETTE = {
    dark: [0x3987e5, 0xd95926, 0x199e70, 0xc98500, 0xd55181, 0x008300, 0x9085e9, 0xe66767],
    light: [0x2a78d6, 0xeb6834, 0x1baf7a, 0xeda100, 0xe87ba4, 0x008300, 0x6250d6, 0xe34948],
  };
  const legendOn = () => CA.labelMode === 'legend' && !!opts.labels;
  const hexCss = (x) => '#' + x.toString(16).padStart(6, '0');

  /** How directly a mesh or marker draws a structure: 0 its own (or the one it borrows), 1 a part of an umbrella entity
   *  or a mesh related to it, 2 its whole mesh group; -1 not at all. */
  function claimRank(rid, o) {
    const ent = o.userData.entity, r = o.userData.rec;
    if (ent && ent === rid) return 0;
    if (ent && ((A3.composite || {})[rid] || []).includes(ent)) return 1;
    if (r && r.related === rid) return 1;
    if (r && A3.groups[rid] && r.group === A3.groups[rid]) return 2;
    return -1;
  }
  const baseOf = (o) => {
    let hex = null;
    o.traverse((c) => { if (hex == null && c.material && c.material.color) hex = c.material.userData.base != null ? c.material.userData.base : o.userData.base; });
    return hex;
  };

  function refreshNames() {
    if (!el.names || !scene) return;
    const on = legendOn(), pal = PALETTE[CA.theme === 'light' ? 'light' : 'dark'];
    const rows = [], seen = new Set();
    labelEls.forEach((l) => { if (!l.tag && !seen.has(l.id)) { seen.add(l.id); rows.push({ id: l.id, rid: resolve(l.id), path: l.path || l.id === CA.selected }); } });
    // which legend row each mesh and marker belongs to: the structure that draws it most directly
    const want = [...new Set(rows.filter((r) => r.path && r.rid).map((r) => r.rid))];
    const order = [...want, ...new Set(rows.map((r) => r.rid).filter((x) => x && !want.includes(x)))];
    const objs = meshObjs.filter((m) => m.userData.rec.group !== 'shell').concat(markerObjs);
    ownerOf = new Map();
    objs.forEach((o) => {
      let best = null, bestRank = 9;
      order.forEach((rid) => { const k = claimRank(rid, o); if (k >= 0 && k < bestRank) { best = rid; bestRank = k; } });
      if (best) ownerOf.set(o, best);
    });
    // colours: kept per entity while the species, region and circuit stay; new structures take the first free slot
    const key = [species, CA.region.id, circuitId].join('|');
    if (key !== slotKey) { slotOf = new Map(); slotKey = key; }
    const owners = new Set(ownerOf.values());
    const colourable = on ? want.filter((rid) => owners.has(rid)) : [];
    [...slotOf.keys()].forEach((rid) => { if (!colourable.includes(rid)) slotOf.delete(rid); });
    colourable.forEach((rid) => {
      if (slotOf.has(rid)) return;
      const used = new Set(slotOf.values());
      const k = pal.findIndex((_, i) => !used.has(i));
      if (k >= 0) slotOf.set(rid, k);
    });
    paint();
    layoutKey = '';
    if (nameHot && !seen.has(nameHot)) nameHot = null;
    // the list: coloured structures in palette order, then the rest by name
    CA.clear(el.names);
    el.names.style.display = on && rows.length ? '' : 'none';
    if (!on || !rows.length) return;
    const swatchOf = (r) => {
      if (slotOf.has(r.rid)) return pal[slotOf.get(r.rid)];
      const o = objs.find((x) => ownerOf.get(x) === r.rid);
      if (!o) return null;
      const c = new window.THREE.Color(baseOf(o)).lerp(new window.THREE.Color(0xffffff), TINT);   // the light tint the model shows
      return c.getHex();
    };
    const row = (r) => {
      const pos = r.rid && positions[r.rid], approx = pos && pos.approx, marker = pos && pos.marker, hex = swatchOf(r);
      return h('div', {
        class: 'nm' + (r.id === CA.selected ? ' sel' : '') + (r.id === nameHot ? ' hot' : ''), 'data-id': r.id, 'data-rid': r.rid || '',
        title: 'Click for its evidence and connections',
        onmouseenter: () => setNameHot(r.id), onmouseleave: () => setNameHot(null), onclick: () => CA.select(r.id),
      },
      h('span', { class: 'nsw' + (marker ? ' dia' : '') + (hex == null ? ' none' : ''), style: hex == null ? null : { background: hexCss(hex) },
        title: hex == null ? 'Drawn as its parts, which are listed separately' : null }),
      h('span', { class: approx ? 'approx' : '' }, labelText(r.id)));
    };
    const coloured = rows.filter((r) => slotOf.has(r.rid)).sort((a, b) => slotOf.get(a.rid) - slotOf.get(b.rid));
    const rest = rows.filter((r) => !slotOf.has(r.rid)).sort((a, b) => labelText(a.id).localeCompare(labelText(b.id)));
    const unpainted = want.filter((rid) => owners.has(rid) && !slotOf.has(rid)).length;
    const open = CA.store.get('atlas.namesOpen', window.innerWidth > 860);   // starts closed on a narrow screen
    el.names.classList.toggle('shut', !open);
    const listId = 'atlas-names-list';
    CA.append(el.names,
      h('button', { class: 'nm-head', type: 'button', 'aria-expanded': String(open), 'aria-controls': listId, title: open ? 'Hide the list' : 'Show the list',
        onclick: () => { CA.store.set('atlas.namesOpen', !open); refreshNames(); } },
      h('i', {}, open ? '▾' : '▸'), ' Structures (' + rows.length + ')', h('span', {}, ' · hover to find, click for details')),
      h('div', { id: listId, class: 'atlas-names-list' },
        coloured.map(row),
        rest.length ? h('div', { class: 'nm-sub' }, coloured.length ? 'Other structures (atlas colours)' : 'In their atlas colours') : null,
        rest.map(row),
        unpainted ? h('div', { class: 'nm-note' }, `Up to ${pal.length} structures of a circuit get a colour of their own; ${unpainted} more keep their atlas colours.`) : null));
  }

  function setNameHot(id) {
    if (id === nameHot) return;
    nameHot = id;
    applyHighlight();
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
      const tx = l.tx && NM.tx[l.tx] ? `<br>Transmitter: ${CA.esc(NM.tx[l.tx].label)} (${CA.esc(l.tx)})` : '';
      return `<b>${CA.esc(CA.ent[l.s].name)} → ${CA.esc(CA.ent[l.t].name)}</b><br>${CA.esc(l.rel)}${tx}<br><span style="color:${st.color}">${st.label}</span> · ${(l.refs || []).length} paper(s)`;
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
    const dist = species === 'mouse' ? 8 : 9;
    const to = { pos: p.clone().add(dir.multiplyScalar(dist)).toArray(), target: p.toArray() };
    if (instant) { camera.position.fromArray(to.pos); controls.target.fromArray(to.target); controls.update(); } else startTween(to);
  }

  function jumpTo(name) {
    const v = VIEWS[species][name];
    camera.position.fromArray(v.pos); controls.target.fromArray(v.target); controls.update();
  }
  function flyTo(v) {   // a preset name or { pos, target }; a preset this species lacks is ignored
    const to = typeof v === 'string' ? VIEWS[species][v] : v;
    if (camera && to) startTween(to);
  }
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
      p.mesh.visible = opts.flow && !trace;
      if (p.mesh.visible) p.mesh.position.copy(p.curve.getPointAt((t * p.speed + p.offset) % 1));
    });
    if (pointerDirty) {
      pointerDirty = false;
      const o = pointer ? pick(pointer) : null;
      if (o !== hovered) { hovered = o; applyHighlight(); }
      if (o) { CA.tip.show(describe(o), pointer); renderer.domElement.style.cursor = 'pointer'; }
      else { CA.tip.hide(); renderer.domElement.style.cursor = ''; }
    }
    if (trace) runTrace(performance.now());
    renderer.render(scene, camera);
    layoutLabels(T);
  }

  /* -------- HTML labels --------
   * Placement is stable from frame to frame, so labels do not flicker while the camera moves:
   * - every label has a fixed priority (the selection, then the current region's structures, then other structures,
   *   then transmitter tags, each in the order they were added), never one that follows screen position;
   * - a label keeps its row while nothing overlaps it there, but takes a new row only with ENTER px to spare, so a
   *   label sitting at the edge of a neighbour does not flip between two rows as the camera moves by a pixel;
   * - a label that finds no free row near its anchor fades out instead of piling onto the others, and fades back in
   *   once a row has room to spare, but not within SETTLE frames of fading out (the selection always shows); zooming
   *   in names more structures;
   * - a label that stepped down moves back towards its anchor only after that row has stayed clear for SETTLE frames.
   * Positions are whole pixels. Boxes are compared by their centres: names sit above their anchor, tags on the pathway. */
  const LH = 20, ROWS = 4, SETTLE = 12, ENTER = 3;
  let layoutFrame = 0;
  function labelRank(l) {
    if (l.id === CA.selected) return 0;
    if (l.tag) return 3;
    return CA.inRegion(l.id) ? 1 : 2;
  }
  function setShown(l, on) {
    if (l.shown === on) return;
    l.shown = on;
    l.el.style.display = on ? '' : 'none';
  }
  function setFits(l, on) {
    if (l.fits === on) return;
    l.fits = on;
    l.el.classList.toggle('off', !on);
  }
  function layoutLabels(T) {
    const w = el.canvas.clientWidth, ht = el.canvas.clientHeight;
    // nothing to do while the camera, the canvas and the labels stay as they are (once the rows have settled)
    const key = [w, ht, labelEls.length, CA.selected, nameHot, CA.labelMode, opts.labels].join('|') + camera.matrixWorld.elements.join(',');
    if (key === layoutKey) { if (++layoutIdle > SETTLE + 1) return; } else { layoutKey = key; layoutIdle = 0; }
    const onModel = CA.labelMode !== 'legend', frame = ++layoutFrame;
    const v = new T.Vector3(), vis = [];
    labelEls.forEach((l, i) => {
      v.copy(l.pos).project(camera);
      // in legend mode the model stays clean: only the structure hovered in the legend is named on it
      const want = onModel ? opts.labels || l.id === CA.selected : !l.tag && l.id === nameHot;
      if (!want || v.z >= 1) { setShown(l, false); l.row = null; return; }
      l.x = Math.round((v.x + 1) / 2 * w); l.y = Math.round((1 - v.y) / 2 * ht); l.order = i;
      vis.push(l);
    });
    vis.sort((a, b) => labelRank(a) - labelRank(b) || a.order - b.order);
    const placed = [];
    const free = (l, row, pad) => {
      const cy = l.y + l.dy + row * LH;
      return !placed.some((p) => Math.abs(p.x - l.x) < (p.w + l.w) / 2 + 4 + pad && Math.abs(p.cy - cy) < LH + pad);
    };
    vis.forEach((l) => {
      setShown(l, true);
      if (!l.w) l.w = l.el.offsetWidth || 100;
      l.dy = l.tag ? 0 : -14;
      const rows = l.tag ? 2 : ROWS;
      let row = l.row != null && l.row < rows && free(l, l.row, 0) ? l.row : null;
      if (row === null) {
        // the nearest row with room to spare to the one it had (or to its anchor), so a blocked label moves least
        const from = l.row != null ? Math.min(l.row, rows - 1) : 0;
        l.clear = 0;
        const held = l.fits === false && frame - l.outAt < SETTLE;   // faded out a moment ago: stay out a little longer
        for (let d = 0; d < rows && row === null && !held; d++) {
          for (const k of d ? [from - d, from + d] : [from]) if (k >= 0 && k < rows && free(l, k, ENTER)) { row = k; break; }
        }
        if (row === null && l.id === CA.selected) row = 0;
      } else if (row > 0) {
        let k = 0;
        while (k < row && !free(l, k, ENTER)) k++;
        if (k >= row) l.clear = 0;
        else if ((l.clear = (l.clear || 0) + 1) >= SETTLE) { row = k; l.clear = 0; }
      }
      l.row = row;
      if (row === null && l.fits !== false) l.outAt = frame;
      setFits(l, row !== null);
      if (row === null) return;
      placed.push({ x: l.x, cy: l.y + l.dy + row * LH, w: l.w });
      const left = l.x + 'px', top = (l.y + row * LH) + 'px';
      if (l.el.style.left !== left) l.el.style.left = left;
      if (l.el.style.top !== top) l.el.style.top = top;
    });
  }

  CA.atlas3d = { flyTo, focusEntity, posOf: (id) => posOf(id), resolve: (id) => resolve(id) };
})();
