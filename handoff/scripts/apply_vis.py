#!/usr/bin/env python3
"""Apply the visual cortex region (2026-11-04, cloud session). Run once, from the repo root:

    python3 handoff/scripts/apply_vis.py && python3 tools/jsonfmt.py data/papers.json data/knowledge.json data/meshes.json

Adds: 45 papers (handoff/visual/draft_papers.json), the region record, 21 new entities (visual-cortex tagged unless
shared), sentences on 5 shared entities, 37 links, 9 chains, 5 questions, 4 circuits, 3D aliases/sides/composite and
mesh items. Every sentence was written from the PubMed abstracts in the session scratchpad (see HANDOFF section 6b).
Asserts that new ids are new and that every link, chain and circuit resolves.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
KP, PP, MP = ROOT / 'data/knowledge.json', ROOT / 'data/papers.json', ROOT / 'data/meshes.json'
kb = json.loads(KP.read_text(encoding='utf-8'))
papers = json.loads(PP.read_text(encoding='utf-8'))
meshes = json.loads(MP.read_text(encoding='utf-8'))
draft = json.loads((ROOT / 'handoff/visual/draft_papers.json').read_text(encoding='utf-8'))
R = 'visual-cortex'

# ---------------------------------------------------------------- papers
have = {p['key'] for p in papers}
for p in draft:
    assert p['key'] not in have, p['key']
papers.extend(draft)
PK = {p['key'] for p in papers}

# ---------------------------------------------------------------- region record
assert R not in {r['id'] for r in kb['regions']}
kb['regions'].append({
    'id': R, 'label': 'Visual cortex', 'entity': 'visual-cortex',
    'query': '("visual cortex"[tiab] OR "visual cortical"[tiab] OR "striate cortex"[tiab] OR extrastriate[tiab] OR "primary visual"[tiab])',
    'view': 'visual-cortex',
    'views': ['atlas', 'scales', 'gaps', 'lab', 'library'],
    'levelDesc': {
        'regional': 'Areas: V1 (striate cortex), V4, MT (V5), inferotemporal cortex and the fusiform face area; the mouse higher visual areas',
        'circuit': 'Retina to lateral geniculate to V1, the ventral and dorsal streams, and top-down input from the frontal eye field, amygdala and basal forebrain',
    },
    'levelQueries': {
        'cellular': '(neuron*[tiab] OR interneuron*[tiab] OR "receptive field*"[tiab] OR "orientation selectiv*"[tiab] OR parvalbumin[tiab] OR somatostatin[tiab])',
        'circuit': '(circuit*[tiab] OR projection*[tiab] OR pathway*[tiab] OR geniculate[tiab] OR "ocular dominance"[tiab] OR plasticity[tiab])',
        'regional': '(V1[tiab] OR V4[tiab] OR "area MT"[tiab] OR V5[tiab] OR inferotemporal[tiab] OR fusiform[tiab] OR "higher visual area*"[tiab])',
    },
    'methods': {
        'molecular': {'manipulate': ['Knockout of a GABA-synthesizing enzyme (GAD65)', 'Benzodiazepines to enhance inhibition', 'Chondroitinase-ABC to degrade perineuronal-net proteoglycans'],
                      'readout': ['Perineuronal-net staining', 'Responses to a deprived eye after monocular deprivation', 'Inhibitory synaptic transmission']},
        'cellular': {'manipulate': ['Optogenetic activation of PV+, SOM+ or VIP+ interneurons', 'Photolytic damage of identified interneurons', 'Microstimulation'],
                     'readout': ['Single-unit receptive fields (orientation, direction, spatial frequency)', 'Calcium imaging of neuron populations', 'In vitro connectivity of neurons characterized in vivo']},
        'circuit': {'manipulate': ['Monocular deprivation and dark rearing', 'Cortical cooling to isolate thalamic input', 'Perturbing visual flow during locomotion'],
                    'readout': ['Thalamocortical cross-correlation', 'Ocular dominance shifts', 'Surround suppression and locomotion gain']},
        'regional': {'manipulate': ['Ibotenic acid lesions of single areas (MT)', 'Transcranial magnetic stimulation of occipital cortex', 'Tracer injections'],
                     'readout': ['Retinotopic fMRI maps and area borders', 'PET and fMRI activation by colour, motion and faces', 'Corticopontine and corticocortical projections']},
        'systems': {'manipulate': ['Frontal eye field microstimulation', 'Locomotion and behavioural state', 'Amygdala lesions in patients'],
                    'readout': ['Attention effects on V4 and IT responses', 'Hierarchy and streams from laminar connections', 'Visual responses modulated by running']},
        'cognitive': {'manipulate': ['Attention tasks with competing stimuli', 'Motion-direction discrimination at threshold', 'Grasping objects that cannot be perceived'],
                      'readout': ['Neuronal versus psychophysical sensitivity', 'Orientation discrimination', 'Face, object and location matching']},
        'clinical': {'manipulate': ['Experimental strabismus and anisometropia (monkey)', 'Braille reading in early-blind people', 'Recording during migraine aura'],
                     'readout': ['Residual vision in the blind field', 'Cortical binocularity and resolution in amblyopia', 'Occipital atrophy on imaging']},
    },
    'intro': {
        'title': 'Visual cortex, from receptive fields to recognition',
        'text': 'Primary visual cortex and the areas beyond it: how geniculate input builds orientation-tuned receptive fields, how inhibition and the extracellular matrix open and close the critical period for binocular vision, the areas and streams for motion, colour, objects, faces and action, how attention and running change visual responses, and what changes in amblyopia, cortical blindness, early blindness and migraine aura. Every connection is tied to the papers behind it and graded by how strong the evidence is.',
    },
    'speciesNote': {
        'human': 'Human: the Allen atlas does not mark visual areas, so V1 is drawn as the occipital pole, cuneus and lingual gyrus (which also hold V2 and V3), V4 as the occipital part of the fusiform gyrus, the fusiform face area as its temporal part and inferotemporal cortex as the inferior temporal gyrus; MT (V5) is placed approximately (≈). The lateral geniculate nucleus is shown in the thalamus, and the frontal eye field is not placed.',
        'mouse': 'Mouse: Allen CCFv3 primary visual area (VISp), the higher visual areas LM, AL, AM, PM, LI and P (the anterior and rostrolateral areas are drawn with posterior parietal cortex) and the dorsal lateral geniculate nucleus. V4, MT, inferotemporal cortex, the fusiform face area and the frontal eye field are not placed in the mouse brain.',
        'macaque': 'Macaque: CHARM V1, V4, MT, inferior temporal cortex (TE and TEO) and area 8A (frontal eye field), and the SARM dorsal lateral geniculate nucleus. The fusiform face area and the mouse higher visual areas are not placed.',
    },
})

# ---------------------------------------------------------------- entities
E = {e['id']: e for e in kb['entities']}


def refs_ok(refs):
    for r in refs:
        assert r in PK, r
    return refs


def ent(id_, name, level, kind, domains, summary, refs, aka=(), region=R):
    assert id_ not in E, id_
    e = {'id': id_, 'name': name, 'level': level, 'kind': kind}
    if region:
        e['region'] = region
    if aka:
        e['aka'] = list(aka)
    e.update({'domains': domains, 'summary': summary, 'refs': refs_ok(refs)})
    kb['entities'].append(e)
    E[id_] = e


def extend(id_, sentence, refs):
    e = E[id_]
    e['summary'] = e['summary'].rstrip() + ' ' + sentence
    for r in refs_ok(refs):
        if r not in e['refs']:
            e['refs'].append(r)


ent('visual-cortex', 'Visual cortex', 'regional', 'area', ['sensory'],
    'The occipital and occipitotemporal areas devoted to vision. In the macaque, a database of reported connections lists 25 predominantly visual areas and 7 visual-association areas, linked by 305 mostly reciprocal pathways and arranged in a hierarchy of 10 cortical levels with intertwined processing streams (monkey). Cells in V1, V2 and higher areas fall into interdigitating subdivisions selective for colour, stereopsis, movement and orientation, which appear to derive mainly from the parvocellular (form and colour) and magnocellular (depth and movement) geniculate subdivisions (review). Much of human visual cortex is organized into visual field maps, in medial, lateral, ventral and dorsal occipital and in posterior parietal cortex (review), whose borders retinotopic fMRI can delineate (human). Face matching and location matching engage separate ventral (occipitotemporal) and dorsal (superior parietal) regions (human).',
    ['felleman1991', 'livingstone1988', 'wandell2007', 'sereno1995', 'haxby1991'], aka=['occipital cortex', 'visual areas'])
ent('v1', 'Primary visual cortex (V1)', 'regional', 'area', ['sensory'],
    'Striate cortex (area 17; VISp in the mouse), which receives visual input from the eyes through the lateral geniculate nucleus. In monkeys most of its cells are simple, complex or hypercomplex, grouped in two independent column systems, for orientation and for eye preference (ocular dominance), with simple, monocularly driven cells in and near layer IV (monkey). Mouse V1 neurons, although their receptive fields are much larger, are nearly as selective for orientation and spatial frequency as in other species (mouse). Most mouse V1 neurons more than double their visual responses when the animal runs, whereas the lateral geniculate does not (mouse), and nearly half combine visual speed with run speed (mouse). Attention did not affect striate cells in a classic study (monkey). In people blind from early life, tactile discrimination activates primary visual cortex (human).',
    ['sadato1996', 'hubel1968', 'niell2008', 'niell2010', 'saleem2013', 'moran1985'], aka=['V1', 'striate cortex', 'area 17', 'VISp', 'primary visual area'])
ent('lgn', 'Lateral geniculate nucleus (visual thalamus)', 'regional', 'nucleus', ['sensory'],
    'The dorsal lateral geniculate nucleus, the thalamic relay from the retina to V1. In primates its parvocellular and magnocellular subdivisions differ in colour selectivity, contrast sensitivity, temporal properties and spatial resolution and appear to give rise to the form and colour and the depth and movement pathways (review), and koniocellular layers form a third channel that relays short-wavelength cone input to the blobs of V1 and low-acuity input to its layer I (review). Geniculate neurons connect to simple cells according to their on or off signature (cat), and their orientation-tuned input to simple cells survives cooling of the cortex (cat). Its visual responses did not increase with locomotion (mouse).',
    ['livingstone1988', 'hendry2000', 'reid1995', 'ferster1996', 'niell2010'], aka=['LGN', 'dLGN', 'LGd', 'DLG', 'lateral geniculate body'])
ent('mt', 'Area MT (V5)', 'regional', 'area', ['sensory'],
    'The middle temporal area. Ibotenic acid lesions raise thresholds for discriminating motion direction but not contrast thresholds (monkey), and single MT neurons are about as sensitive to weak motion as the animal itself (monkey). In humans, visual motion activates area V5 at the temporo-parieto-occipital junction (human).',
    ['newsome1988', 'britten1992', 'zeki1991'], aka=['MT', 'V5', 'hMT+', 'middle temporal area'])
ent('v4', 'Area V4', 'regional', 'area', ['sensory', 'executive'],
    'A prestriate visual area. When two stimuli fall in the receptive field of a V4 neuron, attending to one dramatically reduces the response to the other (monkey), and microstimulating the corresponding site in the frontal eye field enhances V4 visual responses (monkey). In humans, colour activates area V4 in the lingual and fusiform gyri (human).',
    ['moran1985', 'moore2003', 'zeki1991'], aka=['V4', 'hV4'])
ent('it', 'Inferotemporal cortex', 'regional', 'area', ['sensory', 'social'],
    'The end of the ventral visual stream, which is proposed to play the major role in identifying objects (review). Many of its neurons respond to almost any stimulus, others are selective for shape, colour or texture over large receptive fields, and a separate population responds selectively to faces, with a particularly high incidence deep in the superior temporal sulcus (monkey). Attending to one of two stimuli in a neuron\'s receptive field dramatically reduces the response to the other (monkey). The inferior temporal gyrus sends no projections to the pons (monkey).',
    ['goodale1992', 'desimone1984', 'moran1985', 'schmahmann1993'], aka=['IT', 'TE', 'TEO', 'inferior temporal cortex'])
ent('ffa', 'Fusiform face area', 'regional', 'area', ['sensory', 'social'],
    'A region of the human fusiform gyrus selectively involved in face perception: it is more active for faces than for objects, houses or hands and for intact than scrambled faces (human). Fusiform cortex responds more to fearful than to neutral faces, but not in patients with amygdala damage (human).',
    ['kanwisher1997', 'vuilleumier2004'], aka=['FFA', 'fusiform gyrus'])
ent('mouse-hva', 'Higher visual areas (mouse)', 'regional', 'area', ['sensory', 'architecture'],
    'Mouse V1 projects to 15 cortical fields, at least nine of which hold complete maps of the visual hemifield; of the areas on its lateral border only LM shares the vertical meridian with V1 and may be homologous to V2 (mouse). Seven of these areas each encode a distinct combination of spatial and temporal frequency, orientation and direction preferences, perhaps forming motion- and pattern-related groups analogous to dorsal and ventral streams (mouse). Together they form a complex network of specialized higher-order areas (review).',
    ['wang2007', 'marshel2011', 'glickfeld2017'], aka=['LM', 'AL', 'AM', 'PM', 'LI', 'HVAs', 'extrastriate areas (mouse)'])
ent('v1-orientation', 'Orientation selectivity', 'cellular', 'computation', ['sensory'],
    'Simple cells respond best to bright or dark oriented contours (cat). In the cat, geniculate neurons connect to simple cells according to their on or off signature, which implies that simple receptive fields and their orientation selectivity are laid down at the first thalamocortical synapse, and the orientation tuning of geniculate input survives inactivation of the cortex. Cells sharing an orientation preference are grouped in columns (monkey), and the centres of orientation pinwheels are highly ordered at single-cell resolution (cat). Mouse V1 neurons are nearly as orientation selective as those of other species (mouse); activating PV+ interneurons sharpens their tuning and improves orientation discrimination (mouse), and layer 2/3 pyramidal neurons sharing an orientation preference connect at twice the rate of those with orthogonal preferences (mouse).',
    ['reid1995', 'ferster1996', 'hubel1968', 'ohki2006', 'niell2008', 'lee2012', 'ko2011'], aka=['simple cells', 'complex cells', 'orientation tuning', 'orientation columns', 'pinwheels'])
ent('v1-pyr', 'V1 layer 2/3 pyramidal neurons', 'cellular', 'cell type', ['sensory'],
    'They connect at twice the rate when they share an orientation preference, and at much higher rates when their responses to natural stimuli are similar, pointing to fine-scale subnetworks (mouse). During locomotion in a virtual environment they are strongly driven by running and by mismatch between actual and expected visual flow, suggesting predictive coding (mouse). Somatostatin interneurons contribute to their surround suppression (mouse).',
    ['ko2011', 'keller2012', 'adesnik2012'], aka=['L2/3 pyramidal neurons'])
ent('v1-pv', 'V1 PV+ interneurons', 'cellular', 'cell type', ['sensory'],
    'Parvalbumin-positive interneurons. Optogenetically activating them sharpens the orientation tuning and direction selectivity of nearby neurons and improves orientation discrimination, whereas activating somatostatin or VIP interneurons does not (mouse).',
    ['lee2012'], aka=['parvalbumin interneurons', 'PV+'])
ent('v1-sst', 'V1 SOM+ interneurons', 'cellular', 'cell type', ['sensory'],
    'Somatostatin-expressing interneurons of the superficial layers. Unlike pyramidal cells, they respond more as a stimulus extends into the receptive-field surround, because horizontal cortical axons preferentially excite them, and they contribute to the surround suppression of pyramidal cells (mouse).',
    ['adesnik2012'], aka=['somatostatin interneurons', 'SOM+', 'SST+'])
ent('v1-vip', 'V1 VIP+ interneurons', 'cellular', 'cell type', ['sensory', 'motor'],
    'Locomotion activates them independently of visual stimulation, largely through nicotinic input from the basal forebrain; activating them increases V1 visual responses in stationary mice, and damaging them abolishes the enhancement of V1 responses by locomotion (mouse).',
    ['fu2014'], aka=['vasoactive intestinal peptide interneurons', 'VIP+'])
ent('od-plasticity', 'Ocular dominance plasticity', 'circuit', 'plasticity', ['development', 'sensory'],
    'Experience-dependent plasticity of binocular responses in V1. In mice, 4 days of monocular deprivation at postnatal day 28 maximally reduce responses to the deprived eye, during a critical period between P19 and P32, through a competitive, correlation-based plasticity of geniculocortical and intracortical connections (mouse). Disrupting one isoform of glutamic acid decarboxylase prevents it and benzodiazepines restore it (mouse), and studies of mice lacking GAD65 suggest that a threshold level of inhibition may trigger the critical period, once in life (mouse). Degrading the chondroitin sulphate proteoglycans of perineuronal nets lets monocular deprivation shift ocular dominance in adult rats (rat). Early experimental strabismus or anisometropia often causes amblyopia, with reduced cortical binocularity (monkey).',
    ['gordon1996', 'hensch1998', 'fagiolini2000', 'pizzorusso2002', 'kiorpes1998'], aka=['critical period', 'monocular deprivation'])
ent('gad65', 'GAD65', 'molecular', 'enzyme', ['development'],
    'An isoform of glutamic acid decarboxylase, the GABA-synthesizing enzyme. In mice lacking it, benzodiazepines unmask plasticity to monocular deprivation at any age, and enhancing GABA transmission early in life makes them insensitive to deprivation as adults (mouse).',
    ['fagiolini2000'], aka=['glutamic acid decarboxylase 65', 'Gad2'])
ent('pnn', 'Perineuronal nets', 'molecular', 'structure', ['development'],
    'Extracellular-matrix structures formed by chondroitin sulphate proteoglycans. In rat visual cortex they form as the critical period ends, later after dark rearing, and degrading the proteoglycans with chondroitinase-ABC reactivates ocular dominance plasticity in adults (rat).',
    ['pizzorusso2002'], aka=['PNNs', 'chondroitin sulphate proteoglycans', 'CSPGs'])
ent('c-amblyopia', 'Amblyopia', 'clinical', 'disorder', ['sensory', 'development'],
    'A developmental disorder of pattern vision. Macaques often develop it after early experimental strabismus or anisometropia; cortical binocularity is reduced, and in severe cases neurons driven by the amblyopic eye have lower spatial resolution, although these changes do not explain all of the visual deficit (monkey).',
    ['kiorpes1998'], aka=['lazy eye'])
ent('c-cortical-blindness', 'Cortical blindness and blindsight', 'clinical', 'disorder', ['sensory'],
    'Blindness in part of the visual field after damage to visual cortex. Some visual capacity remains in the hemianopic field after a restricted occipital ablation (human), and some patients with extensive damage to primary visual cortex can point or make saccades toward stimuli in the blind field (human). Koniocellular geniculate neurons that innervate extrastriate cortex are likely to sustain some visual behaviours without V1 (review).',
    ['weiskrantz1974', 'goodale1991', 'hendry2000'], aka=['blindsight', 'hemianopia'])
ent('c-blind', 'Early blindness', 'clinical', 'condition', ['sensory', 'development'],
    'In people blind from early life, tactile discrimination such as Braille reading activates primary and secondary visual cortex, which it deactivates in sighted people (human), and disrupting occipital cortex with magnetic stimulation causes errors in reading Braille and distorts tactile perception (human).',
    ['sadato1996', 'cohen1997'], aka=['blindness', 'cross-modal plasticity'])
ent('c-migraine', 'Migraine with aura', 'clinical', 'disorder', ['sensory'],
    'During visual aura, fMRI shows changes with the characteristics of cortical spreading depression, starting in extrastriate area V3A and spreading slowly over occipital cortex in register with the retinotopy of the percept (human).',
    ['hadjikhani2001'], aka=['visual aura', 'cortical spreading depression'])
ent('c-pca', 'Posterior cortical atrophy', 'clinical', 'disorder', ['sensory', 'memory'],
    'A progressive dementia heralded by disorders of higher visual function, followed by alexia, agraphia, visual agnosia and components of Balint\'s and Gerstmann\'s syndromes, with memory relatively spared until late; imaging showed predominant parieto-occipital atrophy in two of five patients (human).',
    ['benson1988'], aka=['PCA', 'Benson syndrome'])
ent('c-akinetopsia', 'Akinetopsia (motion blindness)', 'clinical', 'disorder', ['sensory'],
    'A patient with bilateral posterior brain damage, attributed to the lateral temporo-occipital cortex, showed a disturbance of movement vision with no impression of movement in depth and impaired visually guided eye and finger movements, while movement perception through hearing and touch was intact (human).',
    ['zihl1983'], aka=['motion blindness'])
ent('f-vision', 'Visual perception', 'cognitive', 'function', ['sensory'],
    'Seeing form, colour, motion and depth. These attributes are thought to be analysed in parallel subdivisions of the visual system (review), and colour and motion activate different prestriate areas, V4 and V5 (human).',
    ['livingstone1988', 'zeki1991'], aka=['vision', 'seeing'], region=None)
ent('f-face', 'Face perception', 'cognitive', 'function', ['sensory', 'social'],
    'In humans and macaques, fMRI shows cortical regions that respond more to faces than to objects; in macaques almost all visually responsive neurons in the largest such region are strongly face selective (monkey), and inferotemporal cortex holds a population of face-selective neurons whose responses depend on the configuration of facial features (monkey). In humans a region of the fusiform gyrus is selectively involved in face perception (human).',
    ['tsao2006', 'desimone1984', 'kanwisher1997'], aka=['face recognition'], region=None)
ent('fef', 'Frontal eye field', 'regional', 'area', ['executive', 'motor'],
    'A frontal area where stimulation can evoke saccades. Brief stimulation of an FEF site, below the current that evokes saccades, enhances the visual responses of V4 neurons at the corresponding location and can suppress those at non-corresponding locations (monkey).',
    ['moore2003'], aka=['FEF', 'area 8A'], region=None)

extend('pontine', 'Extrastriate areas concerned mainly with spatial vision, visual motion and the peripheral visual field project to the pontine nuclei, but ventral V4, area TEO and the inferior temporal gyrus do not, and primary visual cortex sends only a few corticopontine cells, from its representation of the lower peripheral field (monkey).',
       ['schmahmann1993', 'glickstein1985'])
extend('parietal', 'The dorsal visual stream from striate to posterior parietal cortex is proposed to mediate the sensorimotor transformations for visually guided action (review), and a spatial location task activates lateral superior parietal cortex (human).',
       ['goodale1992', 'haxby1991'])
extend('f-attention', 'Attending to one of two stimuli in the receptive field of a V4 or inferior temporal neuron dramatically reduces the response to the unattended one, whereas striate cells are unaffected (monkey), and microstimulating the frontal eye field enhances V4 responses at the corresponding location (monkey).',
       ['moran1985', 'moore2003'])
extend('basal-forebrain', 'Its nicotinic input largely mediates the activation of VIP interneurons in mouse V1 by locomotion (mouse).', ['fu2014'])
extend('amygdala', 'Amygdala damage abolishes the larger response of fusiform and occipital cortex to fearful than to neutral faces, although the visual areas are intact (human).', ['vuilleumier2004'])

# ---------------------------------------------------------------- links
L = {f"{l['s']}>{l['t']}": l for l in kb['links']}


def link(s, t, kind, status, rel, refs, note=None):
    lid = f'{s}>{t}'
    assert lid not in L, lid
    assert s in E and t in E, lid
    l = {'s': s, 't': t, 'rel': rel, 'status': status, 'kind': kind, 'refs': refs_ok(refs)}
    if note:
        l['note'] = note
    kb['links'].append(l)
    L[lid] = l


link('eyes', 'lgn', 'anatomical', 'established',
     'retinal input reaches V1 through the lateral geniculate; in primates its parvocellular and magnocellular subdivisions, which differ already in the retina in colour selectivity, contrast sensitivity, temporal properties and spatial resolution, and a third, koniocellular channel carry different aspects of the image (review)',
     ['sadato1996', 'livingstone1988', 'hendry2000'])
link('lgn', 'v1', 'anatomical', 'established',
     'geniculate neurons connect monosynaptically to simple cells of matching on or off signature (cat); koniocellular layers relay short-wavelength cone input to the blobs and low-acuity input to layer I (review); monocular deprivation alters geniculocortical as well as intracortical connections (mouse)',
     ['reid1995', 'hendry2000', 'gordon1996'])
link('lgn', 'v1-orientation', 'mechanistic', 'supported',
     'the specificity of geniculate connections implies that simple receptive fields and their orientation selectivity are laid down at the first thalamocortical synapse, and the orientation tuning of geniculate input to simple cells survives inactivation of the cortex (cat)',
     ['reid1995', 'ferster1996'])
link('v1-orientation', 'f-vision', 'causal', 'emerging',
     'sharpening orientation tuning by activating PV+ interneurons improved orientation discrimination (mouse)', ['lee2012'])
link('v1-pv', 'v1-orientation', 'causal', 'emerging',
     'activating PV+ interneurons sharpens orientation tuning and direction selectivity, whereas activating SOM+ or VIP+ interneurons does not (mouse)', ['lee2012'])
link('v1-sst', 'v1-pyr', 'causal', 'emerging',
     'excited preferentially by horizontal cortical axons, SOM+ interneurons contribute to the surround suppression of pyramidal cells (mouse)', ['adesnik2012'])
link('basal-forebrain', 'v1-vip', 'anatomical', 'emerging',
     'nicotinic input from the basal forebrain largely mediates the activation of VIP interneurons by locomotion (mouse)', ['fu2014'])
link('v1-vip', 'v1', 'causal', 'emerging',
     'activating VIP interneurons increases V1 visual responses, and damaging them abolishes the enhancement of those responses by locomotion (mouse)', ['fu2014'])
link('v1-pyr', 'f-timing', 'functional', 'emerging',
     'layer 2/3 neurons respond to mismatch between actual and expected visual flow during locomotion, suggesting predictive coding (mouse)', ['keller2012'])
link('v1', 'f-spatial', 'functional', 'emerging',
     'nearly half of V1 neurons combine visual speed and run speed during virtual navigation (mouse)', ['saleem2013'])
link('v1', 'mt', 'anatomical', 'supported', 'in the monkey, V1 and V2 feed area V5 (MT)', ['zeki1991'])
link('v1', 'v4', 'anatomical', 'supported', 'in the monkey, V1 and V2 feed area V4', ['zeki1991'])
link('v1', 'it', 'anatomical', 'supported',
     'the ventral stream runs from striate to inferotemporal cortex and is proposed to play the major role in identifying objects (review)', ['goodale1992'])
link('v1', 'parietal', 'anatomical', 'supported',
     'the dorsal stream runs from striate to posterior parietal cortex and is proposed to mediate the sensorimotor transformations for visually guided action (review)', ['goodale1992'])
link('v1', 'mouse-hva', 'anatomical', 'supported',
     'V1 projects to 15 cortical fields, at least nine of them distinct areas with complete maps of the visual field (mouse)', ['wang2007'])
link('fef', 'v4', 'causal', 'emerging',
     'stimulating a frontal eye field site below saccade threshold enhances the visual responses of V4 neurons at the corresponding location and can suppress them at non-corresponding locations (monkey)', ['moore2003'])
link('amygdala', 'ffa', 'causal', 'emerging',
     'amygdala damage abolishes the larger response of fusiform and occipital cortex to fearful than to neutral faces, and the fusiform emotional response is parametrically related to the extent of the damage (human)', ['vuilleumier2004'])
link('mt', 'f-vision', 'causal', 'established',
     'motion perception: MT lesions raise motion but not contrast thresholds and single MT neurons match the animal\'s sensitivity to motion (monkey), and visual motion activates V5 (human)',
     ['newsome1988', 'britten1992', 'zeki1991'])
link('v4', 'f-vision', 'localization', 'emerging', 'colour activates area V4 in the lingual and fusiform gyri (human)', ['zeki1991'])
link('v4', 'f-attention', 'functional', 'supported',
     'attention filters unattended stimuli from the receptive fields of V4 neurons (monkey), and frontal eye field stimulation enhances V4 responses at the corresponding location (monkey)', ['moran1985', 'moore2003'])
link('it', 'f-vision', 'functional', 'supported',
     'object recognition: the ventral stream to inferotemporal cortex is proposed to play the major role in identifying objects (review), and many inferotemporal neurons are selective for shape, colour or texture (monkey)', ['goodale1992', 'desimone1984'])
link('it', 'f-face', 'functional', 'supported',
     'a population of inferotemporal neurons responds selectively to faces, depending on the configuration of facial features (monkey)', ['desimone1984'])
link('ffa', 'f-face', 'localization', 'supported',
     'more active for faces than for objects, houses or hands and for intact than scrambled faces (human)', ['kanwisher1997'])
link('parietal', 'f-voluntary', 'functional', 'supported',
     'visually guided action: the dorsal stream is proposed to mediate the sensorimotor transformations for visually guided actions such as grasping (review), and a patient who could not perceive object shape, size and orientation grasped the objects accurately (human)',
     ['goodale1992', 'goodale1991'])
link('parietal', 'f-vision', 'localization', 'emerging',
     'spatial localization: a dot-location matching task activated lateral superior parietal cortex (human)', ['haxby1991'])
link('mouse-hva', 'f-vision', 'functional', 'emerging',
     'each area encodes a distinct combination of spatiotemporal features, perhaps forming motion- and pattern-related groups (mouse)', ['marshel2011'])
link('v1', 'c-cortical-blindness', 'clinical', 'supported',
     'after a restricted occipital ablation some visual capacity remains in the hemianopic field, and some patients with extensive V1 damage can point or make saccades toward stimuli in the blind field (human)',
     ['weiskrantz1974', 'goodale1991'])
link('lgn', 'c-cortical-blindness', 'clinical', 'hypothesis',
     'koniocellular geniculate neurons that innervate extrastriate cortex are likely to sustain some visual behaviours in the absence of V1 (review)', ['hendry2000'])
link('v1', 'c-blind', 'clinical', 'supported',
     'in the early blind, Braille reading activates primary visual cortex, and occipital magnetic stimulation disrupts it (human)', ['sadato1996', 'cohen1997'])
link('gad65', 'od-plasticity', 'mechanistic', 'supported',
     'disrupting one isoform of glutamic acid decarboxylase prevents the loss of responses to a deprived eye and benzodiazepines restore it; a threshold level of inhibition may trigger the critical period (mouse)',
     ['hensch1998', 'fagiolini2000'])
link('pnn', 'od-plasticity', 'mechanistic', 'emerging',
     'perineuronal nets form as the critical period ends, and degrading their proteoglycans lets monocular deprivation shift ocular dominance in adults (rat)', ['pizzorusso2002'])
link('od-plasticity', 'c-amblyopia', 'developmental', 'emerging',
     'early experimental strabismus or anisometropia often causes amblyopia, with reduced cortical binocularity and, in severe cases, lower spatial resolution of neurons driven by the amblyopic eye (monkey)', ['kiorpes1998'])
link('visual-cortex', 'c-migraine', 'clinical', 'emerging',
     'during visual aura, changes with the characteristics of cortical spreading depression start in area V3A and spread over occipital cortex in register with the percept (human)', ['hadjikhani2001'])
link('visual-cortex', 'c-pca', 'clinical', 'emerging',
     'a progressive dementia heralded by disorders of higher visual function, with predominant parieto-occipital atrophy on imaging in two of five patients (human)', ['benson1988'])
link('visual-cortex', 'c-akinetopsia', 'clinical', 'emerging',
     'bilateral damage attributed to the lateral temporo-occipital cortex disturbed movement vision in a rather pure form (human)', ['zihl1983'])
link('visual-cortex', 'pontine', 'anatomical', 'supported',
     'extrastriate areas concerned mainly with spatial vision, visual motion and the peripheral field project to the pontine nuclei, but areas for object identification and central vision do not (monkey)', ['schmahmann1993'])
link('v1', 'pontine', 'anatomical', 'emerging',
     'only a few corticopontine cells, in the part of area 17 that represents the lower peripheral visual field (monkey)', ['glickstein1985'])

# ---------------------------------------------------------------- chains
C = {c['id'] for c in kb['chains']}


def chain(id_, name, nodes, desc):
    assert id_ not in C, id_
    for a, b in zip(nodes, nodes[1:]):
        assert f'{a}>{b}' in L or f'{b}>{a}' in L, (id_, a, b)
    kb['chains'].append({'id': id_, 'name': name, 'nodes': nodes, 'desc': desc})
    C.add(id_)


chain('vis-orientation', 'From the retina to oriented edges', ['eyes', 'lgn', 'v1-orientation', 'f-vision'],
      'Retinal input reaches V1 through the lateral geniculate nucleus (review). Geniculate neurons connect to simple cells by on or off signature, which implies that orientation selectivity is laid down at the first thalamocortical synapse (cat), and sharpening that tuning by activating PV+ interneurons improves orientation discrimination (mouse).')
chain('vis-motion', 'Seeing motion', ['v1', 'mt', 'f-vision'],
      'In the monkey, V1 and V2 feed area MT (V5); MT lesions raise motion thresholds and single MT neurons match the animal\'s sensitivity to motion (monkey), and motion activates V5 in humans.')
chain('vis-ventral', 'The ventral stream to faces', ['v1', 'it', 'f-face'],
      'The ventral stream runs from striate to inferotemporal cortex and is proposed to play the major role in identifying objects (review), and a population of inferotemporal neurons responds selectively to faces (monkey).')
chain('vis-dorsal', 'Vision for action', ['v1', 'parietal', 'f-voluntary'],
      'The dorsal stream from striate to posterior parietal cortex is proposed to mediate visually guided action (review); a patient who could not perceive the shape, size and orientation of objects grasped them accurately (human).')
chain('vis-attention', 'Attention from the frontal eye field', ['fef', 'v4', 'f-attention'],
      'Stimulating a frontal eye field site below saccade threshold enhances V4 responses at the corresponding location (monkey), and attention filters unattended stimuli from the receptive fields of V4 neurons (monkey).')
chain('vis-locomotion', 'Running turns up V1', ['basal-forebrain', 'v1-vip', 'v1'],
      'Locomotion activates VIP interneurons in V1, largely through nicotinic input from the basal forebrain, and these neurons are needed for the enhancement of V1 visual responses by running (mouse).')
chain('vis-critical-period', 'Inhibition and the critical period', ['gad65', 'od-plasticity', 'c-amblyopia'],
      'Without one isoform of glutamic acid decarboxylase, a deprived eye does not lose its cortical responses, and benzodiazepines restore this plasticity (mouse); abnormal visual experience early in life (experimental strabismus or anisometropia) often causes amblyopia, with reduced cortical binocularity (monkey).')
chain('vis-pontine', 'Visual cortex to the cerebellum', ['visual-cortex', 'pontine', 'cb-cortex'],
      'Extrastriate areas concerned mainly with spatial vision, motion and the peripheral field project to the pontine nuclei (monkey), whose crossed mossy fibers reach the cerebellar cortex.')
chain('vis-fear-faces', 'The amygdala and faces', ['amygdala', 'ffa', 'f-face'],
      'The larger fusiform response to fearful than to neutral faces is absent after amygdala damage (human), and the fusiform face area is selectively involved in face perception (human).')

# ---------------------------------------------------------------- questions
Q = {q['id'] for q in kb['questions']}


def question(id_, title, text, entities, refs, approaches):
    assert id_ not in Q, id_
    for e in entities:
        assert e in E, e
    for r in refs:
        assert f'({r})' in text, (id_, r)
    kb['questions'].append({'id': id_, 'title': title, 'text': text, 'entities': entities, 'refs': refs_ok(refs), 'approaches': approaches})
    Q.add(id_)


question('q-vis-cerebellum', 'Does the cerebellum take part in seeing?',
         'Corticopontine input to the cerebellum appears to come from extrastriate areas concerned with spatial vision, visual motion and the peripheral field rather than object identification (schmahmann1993), and primary visual cortex sends only a few corticopontine cells (glickstein1985). Most of the human cerebellum is functionally coupled to cerebral association networks, in proportion to their cerebral extent, but primary visual cortex is the exception (buckner2011). Does the cerebellum use these visual signals only to guide movement, or does it also contribute to perception?',
         ['visual-cortex', 'pontine', 'cb-cortex'], ['schmahmann1993', 'glickstein1985', 'buckner2011'],
         ['Record mossy fibre and Purkinje cell responses to visual motion in the lobules that receive these pontine inputs.',
          'Test motion perception and visually guided reaching separately in people with cerebellar lesions.',
          'Silence the visual corticopontine pathway and measure both perception and visually guided movement.'])
question('q-vis-critical-period', 'Can the critical period be reopened to treat amblyopia?',
         'Ocular dominance plasticity in mouse V1 is confined to a critical period (gordon1996) whose onset may require a threshold level of inhibition (fagiolini2000), and degrading perineuronal-net proteoglycans reactivates it in adult rats (pizzorusso2002). In amblyopic monkeys, cortical binocularity is reduced, but the changes in V1 neurons do not explain the full deficit (kiorpes1998). Would reopening plasticity in adults restore vision through an amblyopic eye, and where beyond V1 does the deficit lie?',
         ['od-plasticity', 'c-amblyopia', 'pnn', 'gad65'], ['gordon1996', 'fagiolini2000', 'pizzorusso2002', 'kiorpes1998'],
         ['Combine treatments that reopen plasticity with patching of the good eye in animal models of amblyopia.',
          'Record extrastriate areas in amblyopic monkeys.',
          'Follow binocular responses and visual acuity together during treatment.'])
question('q-vis-perception-action', 'Are seeing objects and acting on them separate?',
         'A patient who could not perceive the shape, orientation and size of objects grasped them accurately (goodale1991), which led to the proposal that a ventral stream identifies objects and a dorsal stream guides action (goodale1992). In healthy people, face and location matching engage separate occipitotemporal and parietal regions (haxby1991), and mouse higher visual areas may form motion- and pattern-related groups (marshel2011). How strictly are the streams separated, and do mice have the same division?',
         ['parietal', 'it', 'f-voluntary', 'mouse-hva'], ['goodale1991', 'goodale1992', 'haxby1991', 'marshel2011'],
         ['Test perception and grasping of the same objects after selective lesions of each stream.',
          'Record parietal and inferotemporal neurons while animals both judge and grasp objects.',
          'Silence groups of mouse higher visual areas during visually guided behaviour and during discrimination.'])
question('q-vis-prediction', 'What does V1 predict?',
         'In mice, running more than doubles V1 visual responses (niell2010) through VIP interneurons recruited by basal forebrain input (fu2014), layer 2/3 neurons signal mismatch between actual and expected visual flow (keller2012), and V1 neurons combine visual speed and run speed (saleem2013). Where do the motor-related predictions come from, and do primate V1 responses change in the same way?',
         ['v1-pyr', 'v1-vip', 'v1'], ['niell2010', 'fu2014', 'keller2012', 'saleem2013'],
         ['Silence candidate sources of motor-related input to V1 and measure mismatch responses.',
          'Record V1 in monkeys or humans during self-generated versus passively viewed visual flow.',
          'Relate mismatch signals to learning of new visuomotor couplings.'])
question('q-vis-faces', 'How do face cells relate to face areas?',
         'Inferotemporal cortex holds a population of face-selective neurons (desimone1984), almost all neurons in the largest face-selective fMRI region of macaques are face selective (tsao2006), and the human fusiform face area responds selectively to faces (kanwisher1997). The larger fusiform response to fearful faces depends on the amygdala (vuilleumier2004). How do face-selective neurons map onto the face areas seen with fMRI in each species, and how does the amygdala tune them?',
         ['ffa', 'it', 'f-face'], ['desimone1984', 'tsao2006', 'kanwisher1997', 'vuilleumier2004'],
         ['Record single neurons in fMRI-defined face areas of neurosurgical patients.',
          'Compare face-area responses to fearful faces before and after amygdala inactivation in monkeys.',
          'Map face-selective neurons and face areas in the same animals.'])

# ---------------------------------------------------------------- 3D atlas
A3 = kb['atlas3d']
A3['composite']['visual-cortex'] = ['v1', 'mouse-hva', 'v4', 'mt', 'it', 'ffa']
cellular = ['v1-orientation', 'v1-pyr', 'v1-pv', 'v1-sst', 'v1-vip', 'od-plasticity', 'gad65', 'pnn']
for sp in ('human', 'mouse', 'macaque'):
    al = A3['aliases'][sp]
    for e in cellular:
        assert e not in al
        al[e] = 'v1'
A3['aliases']['human']['lgn'] = 'thalamus'
new_side = ['visual-cortex', 'v1', 'lgn', 'mt', 'v4', 'it', 'ffa', 'mouse-hva', 'fef'] + cellular
for e in new_side:
    assert all(e not in v for v in A3['sides'].values()), e
A3['sides']['L'].extend(new_side)
CI = {c['id'] for c in A3['circuits']}


def circuit(id_, name, desc, links):
    assert id_ not in CI, id_
    for x in links:
        assert x in L, (id_, x)
    A3['circuits'].append({'id': id_, 'region': R, 'name': name, 'desc': desc, 'links': links, 'view': 'visual-cortex'})
    CI.add(id_)


circuit('vis-geniculate', 'From the eye to visual cortex',
        'Retinal input reaches V1 through the lateral geniculate nucleus, and in the monkey V1 and V2 feed areas V4 and MT (V5). In the human brain the geniculate is shown in the thalamus; V4 and MT are not placed in the mouse brain.',
        ['eyes>lgn', 'lgn>v1', 'v1>mt', 'v1>v4'])
circuit('vis-streams', 'Ventral and dorsal streams',
        'The ventral stream runs from striate to inferotemporal cortex and is proposed to play the major role in identifying objects, and the dorsal stream runs to posterior parietal cortex and is proposed to mediate visually guided action (review). In the mouse, V1 projects to at least nine higher visual areas (mouse).',
        ['v1>it', 'v1>parietal', 'v1>mouse-hva'])
circuit('vis-topdown', 'Attention, emotion and running',
        'Stimulating the frontal eye field enhances V4 responses at the corresponding location (monkey); amygdala damage abolishes the larger fusiform response to fearful faces (human); and basal forebrain input recruits VIP interneurons that raise V1 responses during running (mouse).',
        ['fef>v4', 'amygdala>ffa', 'basal-forebrain>v1-vip'])
circuit('vis-cb', 'Visual cortex and cerebellum',
        'Extrastriate areas concerned mainly with spatial vision, motion and the peripheral field project to the pontine nuclei, whereas primary visual cortex sends only a few corticopontine cells (monkey); the pontine nuclei send crossed mossy fibers to the cerebellar cortex.',
        ['v1>pontine', 'visual-cortex>pontine', 'pontine>cb-cortex'])

kb['meta']['subtitle'] = 'An evidence-linked map of the cerebellum, the motor and prefrontal cortex, the basal ganglia, the hippocampus, the amygdala, the visual cortex and their connections, from molecules to mind'

# ---------------------------------------------------------------- meshes
def add(sp, item):
    keys = {it['key'] for it in meshes[sp]['items']}
    assert item['key'] not in keys, (sp, item['key'])
    meshes[sp]['items'].append(item)


add('human', {'key': 'v1-occ', 'src': [12149, 12150, 12151], 'name': 'Occipital pole, cuneus and lingual gyrus', 'entity': 'v1', 'group': 'cortex', 'faces': 3000, 'tone': '#dc8b8b',
              'note': 'V1 lies along the calcarine sulcus, between the cuneus and the lingual gyrus, and reaches the occipital pole; the atlas does not mark its borders, so these gyri, which also hold V2 and V3, stand for it.'})
add('human', {'key': 'fug-o', 'src': 12152, 'name': 'Fusiform gyrus, occipital part', 'entity': 'v4', 'group': 'cortex', 'faces': 1500, 'tone': '#e7a3a3',
              'note': 'Colour activates area V4 in the lingual and fusiform gyri (Zeki et al. 1991); the occipital part of the fusiform gyrus stands for it here.'})
add('human', {'key': 'fug-t', 'src': 12143, 'name': 'Fusiform gyrus, temporal part', 'entity': 'ffa', 'group': 'cortex', 'faces': 1500, 'tone': '#eb6f92',
              'note': 'The fusiform face area lies in the fusiform gyrus (Kanwisher et al. 1997); the atlas does not mark it, so the temporal part of the gyrus stands for it.'})
add('human', {'key': 'itg', 'src': 12142, 'name': 'Inferior temporal gyrus', 'entity': 'it', 'group': 'cortex', 'faces': 1500, 'tone': '#c97f8f'})
add('human', {'key': 'iog', 'src': 12153, 'name': 'Inferior occipital gyrus', 'group': 'helper', 'faces': 600})
add('human', {'key': 'mtg', 'src': 12141, 'name': 'Middle temporal gyrus', 'group': 'helper', 'faces': 800})
add('mouse', {'key': 'visp', 'src': 385, 'name': 'Primary visual area (VISp)', 'entity': 'v1', 'group': 'cortex', 'faces': 1500, 'tone': '#dc8b8b'})
add('mouse', {'key': 'hva', 'src': [409, 402, 394, 533, 312782574, 425], 'name': 'Higher visual areas (LM, AL, AM, PM, LI, P)', 'entity': 'mouse-hva', 'group': 'cortex', 'faces': 2000, 'tone': '#e7a3a3'})
add('mouse', {'key': 'lgd', 'src': 170, 'name': 'Dorsal lateral geniculate nucleus (LGd)', 'entity': 'lgn', 'group': 'target', 'faces': 800})
add('macaque', {'key': 'v1', 'charm': ['V1'], 'name': 'Primary visual cortex (V1)', 'entity': 'v1', 'group': 'cortex', 'faces': 4000, 'tone': '#dc8b8b'})
add('macaque', {'key': 'v4', 'charm': ['V4'], 'name': 'Area V4', 'entity': 'v4', 'group': 'cortex', 'faces': 2000, 'tone': '#e7a3a3'})
add('macaque', {'key': 'mt', 'charm': ['MT'], 'name': 'Middle temporal area (MT)', 'entity': 'mt', 'group': 'cortex', 'faces': 800, 'tone': '#f0b37a'})
add('macaque', {'key': 'itc', 'charm': ['ITC'], 'name': 'Inferior temporal cortex (TE and TEO)', 'entity': 'it', 'group': 'cortex', 'faces': 3000, 'tone': '#c97f8f'})
add('macaque', {'key': 'fef', 'charm': ['area_8A'], 'name': 'Frontal eye field (area 8A)', 'entity': 'fef', 'group': 'cortex', 'faces': 1200, 'tone': '#f6c177'})
add('macaque', {'key': 'dlg', 'sarm': ['DLG'], 'name': 'Dorsal lateral geniculate nucleus', 'entity': 'lgn', 'group': 'target', 'faces': 600})

KP.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
PP.write_text(json.dumps(papers, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
MP.write_text(json.dumps(meshes, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('applied: 45 papers, 25 new entities (22 tagged visual-cortex, 3 shared), 5 extended, 37 links, 9 chains, 5 questions, 4 circuits, 15 mesh items')
