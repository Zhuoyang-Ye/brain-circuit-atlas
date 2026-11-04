#!/usr/bin/env python3
"""Apply the insula region (2026-11-04, cloud session). Run once, from the repo root:

    python3 handoff/scripts/apply_ins.py && python3 tools/jsonfmt.py data/papers.json data/knowledge.json data/meshes.json

Adds 31 papers (handoff/insula/draft_papers.json), the region record, 9 tagged and 3 shared entities, sentences on
8 shared entities, 27 links, 4 chains, 4 questions, 3 circuits, 3D aliases/sides/composite and mesh items.
Every sentence was written from the PubMed abstracts (see HANDOFF section 6c). Asserts that ids are new and that
every link, chain and circuit resolves.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
KP, PP, MP = ROOT / 'data/knowledge.json', ROOT / 'data/papers.json', ROOT / 'data/meshes.json'
kb = json.loads(KP.read_text(encoding='utf-8'))
papers = json.loads(PP.read_text(encoding='utf-8'))
meshes = json.loads(MP.read_text(encoding='utf-8'))
draft = json.loads((ROOT / 'handoff/insula/draft_papers.json').read_text(encoding='utf-8'))
R = 'insula'

have = {p['key'] for p in papers}
for p in draft:
    assert p['key'] not in have, p['key']
papers.extend(draft)
PK = {p['key'] for p in papers}

assert R not in {r['id'] for r in kb['regions']}
kb['regions'].append({
    'id': R, 'label': 'Insula', 'entity': 'insula',
    'query': '(insula[tiab] OR insular[tiab] OR "gustatory cortex"[tiab] OR "taste cortex"[tiab] OR interocepti*[tiab])',
    'view': 'insula',
    'views': ['atlas', 'scales', 'gaps', 'lab', 'library'],
    'levelDesc': {
        'regional': 'Anterior (agranular and dysgranular) and posterior (granular) insula; gustatory cortex',
        'circuit': 'Thalamic taste input to gustatory cortex and on to the amygdala; posterior insula outputs to the central amygdala and accumbens; amygdala input that carries hunger; the salience network with the anterior cingulate',
    },
    'levelQueries': {
        'cellular': '(neuron*[tiab] OR "von Economo"[tiab] OR interneuron*[tiab] OR GABA*[tiab])',
        'circuit': '(circuit*[tiab] OR projection*[tiab] OR pathway*[tiab] OR connectivity[tiab])',
        'regional': '("anterior insula"[tiab] OR "posterior insula"[tiab] OR "gustatory cortex"[tiab] OR frontoinsular[tiab])',
    },
    'methods': {
        'molecular': {'manipulate': ['Benzodiazepines (diazepam) during a sensitive period', 'Knockout mouse models (GAD65, Shank3, Mecp2)', 'Chemogenetic activation of hypothalamic AgRP neurons'],
                      'readout': ['GABA circuit maturation', 'Acetylcholinesterase histochemistry', 'Tau pathology in surviving neurons']},
        'cellular': {'manipulate': ['Silencing defined neuron populations', 'Optogenetic activation of taste-cortex fields', 'Chemogenetics in hunger and thirst'],
                     'readout': ['Cellular imaging through a microprism', 'Two-photon imaging of taste responses', 'Stereological counts of von Economo neurons']},
        'circuit': {'manipulate': ['Projection-specific optogenetics (to the amygdala and accumbens)', 'Inhibiting transmitter release from projection neurons', 'Viral and classic tract tracing'],
                    'readout': ['Optogenetics-assisted circuit mapping', 'Topography of cortical projections to the amygdala', 'Afferent and efferent cortical connections']},
        'regional': {'manipulate': ['Electrical stimulation through depth electrodes (patients)', 'Expectancy manipulation', 'Thermal and painful stimulation'],
                     'readout': ['Gustotopic maps', 'PET and fMRI activation by cooling, pain and taste', 'Gray matter volume']},
        'systems': {'manipulate': ['Task-free (resting-state) recording', 'Salient events (oddballs, event boundaries)', 'Hunger and thirst'],
                    'readout': ['Intrinsic connectivity networks', 'Granger causality between networks', 'Population activity tracking physiological state']},
        'cognitive': {'manipulate': ['Heartbeat detection', 'Watching a loved one receive pain', 'Go/no-go tasks reinforced by tastes'],
                      'readout': ['Interoceptive accuracy and awareness', 'Empathy scores', 'Risky betting']},
        'clinical': {'manipulate': ['Lesion patients (smoking, gambling, disgust)', 'Epilepsy surgery workup', 'Transdiagnostic meta-analysis'],
                     'readout': ['Quitting smoking without urges', 'Von Economo neuron loss in frontotemporal dementia', 'Gray matter loss across psychiatric diagnoses']},
    },
    'intro': {
        'title': 'Insula, the brain\'s map of the body',
        'text': 'The anterior and posterior insula and the taste cortex: how heartbeat, temperature, pain and taste are represented, how tastes gain pleasant or aversive value through the amygdala, how hunger and thirst change what insular neurons signal, the insula\'s part in empathy, disgust and the salience network, and what changes in smoking addiction, frontotemporal dementia, central pain and across psychiatric disorders. Every connection is tied to the papers behind it and graded by how strong the evidence is.',
    },
    'speciesNote': {
        'human': 'Human: the Allen short insular gyri stand for the anterior insula and the long insular gyri for the posterior insula. The atlas does not mark the taste cortex, which in humans lies in the insula and operculum, so it is shown in the anterior insula, as are the von Economo neurons.',
        'mouse': 'Mouse: Allen CCFv3 agranular insular area (dorsal and ventral parts for the anterior insula; the posterior part with the visceral area for the posterior insula) and the gustatory areas. Von Economo neurons are not placed in the mouse brain.',
        'macaque': 'Macaque: CHARM agranular and dysgranular insula (anterior) and granular insula (posterior). The taste cortex is shown in the anterior insula, and the lateral agranular insula is drawn with orbitofrontal cortex. Von Economo neurons are not placed in the macaque brain.',
    },
})

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
    assert not e.get('region'), (id_, 'tagged entities would need the papers tagged too')
    e['summary'] = e['summary'].rstrip() + ' ' + sentence
    for r in refs_ok(refs):
        if r not in e['refs']:
            e['refs'].append(r)


ent('insula', 'Insular cortex', 'regional', 'area', ['homeostasis', 'emotion'],
    'Cortex hidden in the depth of the hemisphere by the frontal and temporal opercula (human). In the rhesus monkey it has agranular, dysgranular and granular sectors and forms with lateral orbital and temporopolar cortex a paralimbic belt, and the human insula has a virtually identical plan (monkey). It receives input from prefrontal, orbital, opercular, cingulate, olfactory, temporopolar, superior temporal, rhinal and posterior parietal cortex and projects back to the areas that project to it; through its connections with the amygdala it gives somatosensory, auditory, gustatory, olfactory and visceral sensations a route to the limbic system (monkey). Imaging meta-analysis divides the human insula into sensorimotor (mid-posterior), social-emotional (anterior-ventral), olfacto-gustatory (central) and cognitive (anterior-dorsal) regions (human). Smokers whose brain damage involved the insula were more likely to lose their addiction (human). In mice its neurons respond preferentially to food cues when the animal is hungry (mouse), and its ongoing activity tracks the return to homeostasis during hunger and thirst (mouse).',
    ['cauda2011', 'mesulam1982a', 'mufson1982', 'mesulam1982b', 'kurth2010', 'naqvi2007', 'livneh2017', 'livneh2020'],
    aka=['insula', 'insular cortex', 'insular lobe', 'InsCtx', 'Reil'])
ent('ains', 'Anterior insula', 'regional', 'area', ['homeostasis', 'emotion', 'social'],
    'The anterior insula, with agranular and dysgranular cortex in front of the granular posterior part (human). Activity in the right anterior insula predicts the accuracy of heartbeat detection, and its gray matter volume correlates with interoceptive accuracy and visceral awareness (human); its re-representation of interoception is proposed as a basis for subjective feelings and awareness (review). It responds both to one\'s own pain and to a signal that a loved one is in pain, in proportion to empathy (human), and to feeling disgust as well as seeing it on others\' faces (human). With the dorsal anterior cingulate it anchors a salience network (human), and gray matter loss across psychiatric diagnoses converges in both insulae and the dorsal anterior cingulate (human). Perceived thermal intensity correlates with right anterior insula activity (human).',
    ['cauda2011', 'critchley2004', 'craig2009', 'singer2004', 'wicker2003', 'seeley2007', 'goodkind2015', 'craig2000'],
    aka=['AIC', 'anterior insular cortex', 'frontoinsular cortex', 'FI', 'agranular insula'])
ent('pins', 'Posterior insula', 'regional', 'area', ['sensory', 'homeostasis'],
    'The posterior insula, mostly granular cortex (monkey). Graded cooling activates the dorsal margin of the middle/posterior insula, which corresponds to the lamina I spinothalamocortical pathway of monkeys (human), and stimulating the upper posterior insula evokes painful sensations, while posterior sites also evoke non-painful somatic sensations (human). Posterior insula/secondary somatosensory responses are specific to one\'s own pain, not a loved one\'s (human). In mice the posterior insula processes aversive stimuli and bodily states; its projection to the central amygdala mediates anxiety-related behaviours, and a separate accumbens-projecting pathway regulates feeding (mouse).',
    ['mesulam1982a', 'craig2000', 'ostrowsky2002', 'singer2004', 'gehrlach2019'],
    aka=['PIC', 'pIC', 'posterior insular cortex', 'granular insula', 'dorsal posterior insula'])
ent('gc', 'Gustatory cortex', 'regional', 'area', ['sensory'],
    'The primary taste cortex, which in humans consists of the insula and operculum (human). In mice each taste quality (sweet, bitter, umami, salty) has its own cortical field (mouse), and manipulating the sweet and bitter fields controls taste perception and behaviour even without taste input (mouse). Its sweet- and bitter-responsive fields project to distinct parts of the amygdala, which assign taste valence (mouse), and its projection to the lateral central amygdala is needed to learn taste-guided avoidance (mouse). Expecting a milder taste reduces its response to an aversive bitter taste (human). In primates the thalamic taste area projects to insular-opercular cortex (review).',
    ['nitschke2006', 'chen2011', 'peng2015', 'wang2018', 'schiff2018', 'augustine1996'],
    aka=['GC', 'taste cortex', 'primary taste cortex', 'GU', 'gustatory areas'])
ent('vens', 'Von Economo neurons', 'cellular', 'cell type', ['social', 'emotion'],
    'Large bipolar projection neurons found only in great apes and humans, and only in anterior cingulate and frontoinsular cortex (human). Frontotemporal dementia causes an early, severe and selective loss of them, which Alzheimer\'s disease does not (human), and they are proposed to contribute to awareness (review).',
    ['seeley2006', 'craig2009'], aka=['VENs', 'spindle neurons'])
ent('c-addiction', 'Addiction to smoking', 'clinical', 'disorder', ['reward'],
    'Smokers with brain damage involving the insula were more likely than smokers with damage elsewhere to quit easily and immediately, without relapse or a persisting urge to smoke (human).',
    ['naqvi2007'], aka=['nicotine addiction', 'smoking'])
ent('c-ftd', 'Frontotemporal dementia', 'clinical', 'disorder', ['social', 'emotion'],
    'A neurodegenerative disease that erodes social behaviour and emotion and injures anterior cingulate and frontoinsular cortex early; it causes a selective loss of von Economo neurons, unlike Alzheimer\'s disease (human).',
    ['seeley2006'], aka=['FTD', 'behavioural-variant frontotemporal dementia'])
ent('c-central-pain', 'Central post-stroke pain', 'clinical', 'disorder', ['sensory'],
    'Lesions of the dorsal posterior insula, where cooling is represented, can produce central post-stroke pain, which the authors take to support the proposal that central pain results from loss of the normal inhibition of pain by cold (human).',
    ['craig2000'], aka=['central pain syndrome', 'thalamic pain'])
ent('c-psych', 'Mental illness across diagnoses', 'clinical', 'disorder', ['emotion', 'executive'],
    'In 193 morphometry studies of schizophrenia, bipolar disorder, depression, addiction, obsessive-compulsive disorder and anxiety, gray matter loss converged in the dorsal anterior cingulate and both insulae, with few diagnosis-specific effects (human).',
    ['goodkind2015'], aka=['transdiagnostic', 'common substrate of mental illness'])
ent('salience-net', 'Salience network', 'systems', 'network', ['executive', 'emotion'],
    'An intrinsic connectivity network anchored by the dorsal anterior cingulate and orbital frontoinsular cortices, with robust subcortical and limbic connectivity; connectivity of its cingulate node correlates with anxiety (human). The right fronto-insular cortex appears to drive switches between the central-executive and default-mode networks (human), and the network is proposed to mark salient events for further processing (review).',
    ['seeley2007', 'sridharan2008', 'menon2010'], aka=['SN', 'cingulo-opercular network'], region=None)
ent('f-interoception', 'Interoception', 'cognitive', 'function', ['homeostasis', 'sensory'],
    'Sensing the physiological condition of the body. Right anterior insula activity and gray matter volume relate to the accuracy of heartbeat detection and to visceral awareness (human), graded cooling activates the dorsal posterior insula (human), and mouse insular cortex tracks the return to homeostasis during hunger and thirst (mouse).',
    ['critchley2004', 'craig2000', 'livneh2020'], aka=['interoceptive awareness', 'body sense'], region=None)
ent('f-taste', 'Taste', 'cognitive', 'function', ['sensory', 'reward'],
    'Detecting sweet, bitter, umami, salty and sour tastes. In mice each quality is represented in its own field of gustatory cortex (mouse), and amygdala inputs from those fields assign taste valence separately from taste identity (mouse).',
    ['chen2011', 'wang2018'], aka=['gustation'], region=None)

extend('f-pain', 'Stimulating the upper posterior insula evokes painful sensations (human), and the anterior insula and rostral anterior cingulate respond to a loved one\'s pain as well as one\'s own (human).',
       ['ostrowsky2002', 'singer2004'])
extend('f-social', 'Empathy for pain engages a core network of anterior insula and medial/anterior cingulate cortex that overlaps with responses to one\'s own pain (human).',
       ['lamm2011', 'singer2004'])
extend('f-emotion', 'Feeling disgust and seeing it on others\' faces activate the same anterior insula sites (human), and a patient with insula and putamen damage showed impaired recognition of disgust (human).',
       ['wicker2003', 'calder2000'])
extend('f-feeding', 'Mouse insular neurons respond preferentially to food cues only when the animal is hungry, a bias that hypothalamic AgRP neurons restore through the paraventricular thalamus and basolateral amygdala (mouse).',
       ['livneh2017'])
extend('f-decision', 'Patients with insular lesions fail to adjust their bets to the odds of winning (human).', ['clark2008'])
extend('f-attention', 'The right fronto-insular cortex appears to drive switching between the central-executive and default-mode networks at salient events (human).', ['sridharan2008'])
extend('c-anxiety', 'Anxiety proneness is proposed to involve an augmented interoceptive prediction signal in which the anterior insula plays a key role (hypothesis).', ['paulus2006'])
extend('thalamus', 'Its taste area, the parvicellular ventral posteromedial nucleus, projects to insular-opercular cortex (review).', ['augustine1996'])

L = {f"{l['s']}>{l['t']}": l for l in kb['links']}


def link(s, t, kind, status, rel, refs):
    lid = f'{s}>{t}'
    assert lid not in L, lid
    assert s in E and t in E, lid
    l = {'s': s, 't': t, 'rel': rel, 'status': status, 'kind': kind, 'refs': refs_ok(refs)}
    kb['links'].append(l)
    L[lid] = l


link('thalamus', 'gc', 'anatomical', 'supported', 'the thalamic taste area, the parvicellular ventral posteromedial nucleus, projects to insular-opercular cortex (review)', ['augustine1996'])
link('insula', 'amygdala', 'anatomical', 'supported',
     'the insula connects with the lateral, basolateral, central, cortical and medial amygdaloid nuclei (review), giving somatosensory, auditory, gustatory, olfactory and visceral sensations a route to the limbic system (monkey)',
     ['mesulam1982b', 'augustine1996'])
link('gc', 'amygdala', 'causal', 'emerging',
     'sweet- and bitter-responsive taste cortex project to distinct parts of the amygdala; manipulating these inputs imposes or reverses taste valence, and silencing amygdala neurons abolishes valence-related behaviour but not taste discrimination (mouse)',
     ['wang2018'])
link('gc', 'cea', 'anatomical', 'emerging',
     'direct excitatory projection to the lateral central amygdala; inhibiting it prevents learning to withhold licking for an aversive taste, and activating it suppresses licking and can instruct avoidance (mouse)',
     ['schiff2018'])
link('pins', 'cea', 'causal', 'emerging', 'the posterior insula projection to the central amygdala mediates anxiety-related behaviours (mouse)', ['gehrlach2019'])
link('pins', 'nac', 'causal', 'emerging', 'an accumbens-projecting posterior insula pathway regulates feeding upon changes in bodily state (mouse)', ['gehrlach2019'])
link('bla', 'insula', 'anatomical', 'supported',
     'hunger signals from hypothalamic AgRP neurons reach insular cortex via the paraventricular thalamus and basolateral amygdala (mouse), and insular cortex appears to combine visceral signals with this hypothalamus-gated amygdala input (mouse)',
     ['livneh2017', 'livneh2020'])
link('ains', 'acc', 'functional', 'supported',
     'at rest the anterior insula is coupled with the anterior cingulate cortex (human), and a right fronto-insular and anterior cingulate network is activated by salient events (human)',
     ['cauda2011', 'sridharan2008'])
link('ains', 'salience-net', 'functional', 'supported',
     'the orbital frontoinsular cortex anchors the salience network with the dorsal anterior cingulate (human), and the anterior insula is proposed as its hub (review)', ['seeley2007', 'menon2010'])
link('acc', 'salience-net', 'functional', 'emerging',
     'the dorsal anterior cingulate is the other anchor of the salience network, and its connectivity correlates with prescan anxiety (human)', ['seeley2007'])
link('salience-net', 'f-attention', 'functional', 'supported',
     'Granger causality analysis indicates that the right fronto-insular cortex drives switching between the central-executive and default-mode networks (human); the network is proposed to give salient events access to attention and working memory (review)',
     ['sridharan2008', 'menon2010'])
link('ains', 'f-interoception', 'localization', 'supported',
     'right anterior insula activity predicts the accuracy of heartbeat detection, and its gray matter volume correlates with interoceptive accuracy and visceral awareness (human); proposed to re-represent interoception as a basis for feelings (review)',
     ['critchley2004', 'craig2009'])
link('pins', 'f-interoception', 'localization', 'emerging',
     'graded cooling activates the dorsal margin of the middle/posterior insula, which the authors consider an interoceptive area of limbic sensory cortex (human)', ['craig2000'])
link('insula', 'f-interoception', 'functional', 'emerging',
     'ongoing insular activity tracks the return to homeostasis during hunger and thirst, and cues shift it toward the future satiety-related pattern (mouse)', ['livneh2020'])
link('pins', 'f-pain', 'localization', 'supported',
     'stimulating the upper posterior insula evokes painful sensations, mostly on the right (human), and graded cooling activates the dorsal posterior insula (human)', ['ostrowsky2002', 'craig2000'])
link('ains', 'f-social', 'localization', 'supported',
     'empathy: the anterior insula responds both to one\'s own pain and to a loved one\'s, scaled with empathy scores (human), meta-analysis places it in a core network for empathy for pain (human), and seeing disgust activates the same sites as feeling it (human)',
     ['singer2004', 'lamm2011', 'wicker2003'])
link('ains', 'f-emotion', 'localization', 'supported',
     'disgust: feeling disgust and seeing it on others\' faces activate the same anterior insula sites (human), and a patient with insula and putamen damage showed impaired recognition of disgust (human)',
     ['wicker2003', 'calder2000'])
link('gc', 'f-taste', 'localization', 'supported',
     'each basic taste quality has its own field in mouse gustatory cortex, and manipulating the sweet or bitter field controls taste perception and behaviour (mouse); expectancy modulates the human taste cortex response to an aversive taste (human)',
     ['chen2011', 'peng2015', 'nitschke2006'])
link('insula', 'f-feeding', 'functional', 'supported',
     'insular neurons respond preferentially to food cues only when hungry, a bias restored by activating AgRP hunger neurons (mouse), and a posterior insula to accumbens pathway regulates feeding with changes in bodily state (mouse)',
     ['livneh2017', 'gehrlach2019'])
link('insula', 'c-addiction', 'clinical', 'emerging',
     'smokers whose brain damage involved the insula were more likely to quit easily, immediately and without relapse or urges (human)', ['naqvi2007'])
link('insula', 'f-decision', 'clinical', 'emerging', 'patients with insular lesions fail to adjust their bets to the odds of winning (human)', ['clark2008'])
link('vens', 'c-ftd', 'clinical', 'emerging',
     'frontotemporal dementia causes an early, severe and selective loss of anterior cingulate von Economo neurons (74% fewer per section), which Alzheimer\'s disease does not (human)', ['seeley2006'])
link('ains', 'c-ftd', 'clinical', 'emerging', 'frontotemporal dementia injures anterior cingulate and frontoinsular cortex early (human)', ['seeley2006'])
link('ains', 'c-anxiety', 'theoretical', 'hypothesis',
     'proposed: anxiety-prone people show an augmented interoceptive prediction signal, in which the anterior insula plays a key role (hypothesis)', ['paulus2006'])
link('ains', 'c-psych', 'clinical', 'emerging',
     'gray matter loss across six psychiatric diagnoses converges in both insulae and the dorsal anterior cingulate (meta-analysis, human)', ['goodkind2015'])
link('insula', 'c-asd', 'clinical', 'emerging',
     'multisensory integration in insular cortex is impaired in the BTBR autism model, reflecting weakened GABA circuits, and early diazepam rescues it; GAD65, Shank3 and Mecp2 knockouts are also impaired (mouse)',
     ['gogolla2014'])
link('pins', 'c-central-pain', 'clinical', 'hypothesis',
     'lesions of the dorsal posterior insula can produce central post-stroke pain, consistent with the proposal that central pain results from losing the normal inhibition of pain by cold (human)', ['craig2000'])

C = {c['id'] for c in kb['chains']}


def chain(id_, name, nodes, desc):
    assert id_ not in C, id_
    for a, b in zip(nodes, nodes[1:]):
        assert f'{a}>{b}' in L or f'{b}>{a}' in L, (id_, a, b)
    kb['chains'].append({'id': id_, 'name': name, 'nodes': nodes, 'desc': desc})
    C.add(id_)


chain('ins-taste-valence', 'From taste to its value', ['thalamus', 'gc', 'amygdala', 'f-valence'],
      'The thalamic taste area projects to insular-opercular cortex (review). Sweet- and bitter-responsive taste cortex projects to distinct parts of the amygdala, and these inputs assign taste valence (mouse); amygdala neurons encode positive and negative values (monkey).')
chain('ins-anxiety', 'The posterior insula and anxiety', ['pins', 'cea', 'f-anxiety'],
      'The posterior insula projection to the central amygdala mediates anxiety-related behaviours (mouse), and bilateral central amygdala lesions suggest a role for it in fear- and anxiety-related responses (monkey).')
chain('ins-hunger', 'Hunger reaches the insula', ['bla', 'insula', 'f-feeding'],
      'Signals from hypothalamic AgRP hunger neurons reach insular cortex via the paraventricular thalamus and basolateral amygdala and bias insular neurons toward food cues (mouse).')
chain('ins-salience', 'Salience and switching', ['ains', 'salience-net', 'f-attention'],
      'The frontoinsular cortex anchors the salience network with the dorsal anterior cingulate (human), and the right fronto-insular cortex appears to drive switches between the central-executive and default-mode networks (human).')

Q = {q['id'] for q in kb['questions']}


def question(id_, title, text, entities, refs, approaches):
    assert id_ not in Q, id_
    for e in entities:
        assert e in E, e
    for r in refs:
        assert f'({r})' in text, (id_, r)
    kb['questions'].append({'id': id_, 'title': title, 'text': text, 'entities': entities, 'refs': refs_ok(refs), 'approaches': approaches})
    Q.add(id_)


question('q-ins-feeling', 'Does the anterior insula turn body signals into feelings?',
         'Right anterior insula activity and gray matter volume relate to how accurately people detect their own heartbeat and to visceral awareness (critchley2004), and the anterior insula is proposed to re-represent interoception as a basis for subjective feelings and awareness (craig2009). Smokers whose brain damage involved the insula were more likely to quit without a persisting urge to smoke (naqvi2007), and anxiety proneness is proposed to reflect an augmented interoceptive prediction signal (paulus2006). Is the anterior insula needed for feelings, or for awareness of them?',
         ['ains', 'f-interoception', 'c-addiction'], ['critchley2004', 'craig2009', 'naqvi2007', 'paulus2006'],
         ['Test interoceptive accuracy and reported feelings in patients with focal anterior insula lesions.',
          'Relate anterior insula responses to heartbeats to moment-by-moment ratings of urges and emotions.',
          'Train interoceptive accuracy in anxious people and measure insula activity and anxiety.'])
question('q-ins-taste-value', 'Where does a taste get its value?',
         'In mice each taste quality has its own field of gustatory cortex (chen2011), and manipulating the sweet or bitter field controls taste perception and behaviour (peng2015). Projections from those fields to the amygdala assign valence separately from identity (wang2018), and a projection to the lateral central amygdala is needed to learn taste-guided avoidance (schiff2018). Does the same split between identity in the insula and value in the amygdala hold in primates, and how does learning change it?',
         ['gc', 'f-taste', 'amygdala'], ['chen2011', 'peng2015', 'wang2018', 'schiff2018'],
         ['Record taste cortex and amygdala together while a taste is devalued by pairing it with illness.',
          'Image the human taste cortex with high resolution for a gustotopic map.',
          'Silence insula-to-amygdala projections in primates and measure taste preference and discrimination.'])
question('q-ins-prediction', 'How does the insula predict the body\'s needs?',
         'Insular neurons respond to food cues only when mice are hungry, a bias carried by AgRP neurons through the paraventricular thalamus and basolateral amygdala (livneh2017); insular activity tracks the return to homeostasis and cues shift it toward the predicted future state (livneh2020); and the posterior insula drives anxiety through the central amygdala and feeding through the accumbens (gehrlach2019). How do predicted and actual body states combine, and is the same circuit used for thirst, pain or fear?',
         ['insula', 'pins', 'f-feeding'], ['livneh2017', 'livneh2020', 'gehrlach2019'],
         ['Record insular neurons while feeding is delayed or the meal is infused directly into the stomach.',
          'Manipulate amygdala input to the insula and measure prediction-related activity.',
          'Compare insular coding of hunger, thirst and aversive bodily states in the same neurons.'])
question('q-ins-switch', 'Is the anterior insula a switch between brain networks?',
         'The salience network is anchored by frontoinsular and dorsal anterior cingulate cortex (seeley2007), the right fronto-insular cortex appears to drive switching between the central-executive and default-mode networks (sridharan2008), and the anterior insula is proposed as the network\'s hub (menon2010). Gray matter loss across psychiatric diagnoses converges on the same insula and cingulate regions (goodkind2015). Does the switch depend on the insula itself, and could its damage explain shared symptoms across disorders?',
         ['salience-net', 'ains', 'c-psych'], ['seeley2007', 'sridharan2008', 'menon2010', 'goodkind2015'],
         ['Test network switching in patients with focal anterior insula lesions.',
          'Stimulate the anterior insula during intracranial recordings and measure network transitions.',
          'Relate insula integrity to executive function across psychiatric diagnoses.'])

A3 = kb['atlas3d']
A3['composite']['insula'] = ['ains', 'pins', 'gc']
A3['aliases']['human']['gc'] = 'ains'
A3['aliases']['human']['vens'] = 'ains'
A3['aliases']['macaque']['gc'] = 'ains'
for e in ['insula', 'ains', 'pins', 'gc', 'vens']:
    assert all(e not in v for v in A3['sides'].values()), e
A3['sides']['L'].extend(['insula', 'ains', 'pins', 'gc', 'vens'])
CI = {c['id'] for c in A3['circuits']}


def circuit(id_, name, desc, links):
    assert id_ not in CI, id_
    for x in links:
        assert x in L, (id_, x)
    A3['circuits'].append({'id': id_, 'region': R, 'name': name, 'desc': desc, 'links': links, 'view': 'insula'})
    CI.add(id_)


circuit('ins-taste', 'Taste: thalamus, insula and amygdala',
        'The thalamic taste area projects to insular-opercular cortex (review); sweet- and bitter-responsive taste cortex projects to distinct parts of the amygdala, whose inputs assign taste valence, and to the lateral central amygdala, needed to learn taste-guided avoidance (mouse). In primates the taste cortex is shown in the anterior insula.',
        ['thalamus>gc', 'gc>amygdala', 'gc>cea'])
circuit('ins-body', 'Bodily state in and out',
        'Hunger signals reach insular cortex through the basolateral amygdala (mouse); the posterior insula drives anxiety-related behaviour through the central amygdala and regulates feeding through the nucleus accumbens (mouse).',
        ['bla>insula', 'pins>cea', 'pins>nac'])
circuit('ins-salience', 'Anterior insula, cingulate and amygdala',
        'At rest the anterior insula is coupled with the anterior cingulate, and the two form a network activated by salient events (human); the insula connects with several amygdaloid nuclei (review).',
        ['ains>acc', 'insula>amygdala'])

kb['meta']['subtitle'] = 'An evidence-linked map of the cerebellum, the motor and prefrontal cortex, the basal ganglia, the hippocampus, the amygdala, the visual cortex, the insula and their connections, from molecules to mind'


def add(sp, item):
    keys = {it['key'] for it in meshes[sp]['items']}
    assert item['key'] not in keys, (sp, item['key'])
    meshes[sp]['items'].append(item)


add('human', {'key': 'sig', 'src': 12178, 'name': 'Short insular gyri (anterior insula)', 'entity': 'ains', 'group': 'cortex', 'faces': 1500, 'tone': '#e879f9',
              'note': 'The short insular gyri stand for the anterior insula; the atlas does not mark the taste cortex, which in humans lies in the insula and operculum, so it is shown here.'})
add('human', {'key': 'lig', 'src': 12177, 'name': 'Long insular gyri (posterior insula)', 'entity': 'pins', 'group': 'cortex', 'faces': 1200, 'tone': '#c084fc'})
add('mouse', {'key': 'ai-ant', 'src': [104, 119], 'name': 'Agranular insular area, dorsal and ventral parts (anterior insula)', 'entity': 'ains', 'group': 'cortex', 'faces': 1200, 'tone': '#e879f9'})
add('mouse', {'key': 'ai-post', 'src': [111, 677], 'name': 'Agranular insular area, posterior part, and visceral area (posterior insula)', 'entity': 'pins', 'group': 'cortex', 'faces': 1200, 'tone': '#c084fc'})
add('mouse', {'key': 'gu', 'src': 1057, 'name': 'Gustatory areas (GU)', 'entity': 'gc', 'group': 'cortex', 'faces': 800, 'tone': '#f0abfc'})
add('macaque', {'key': 'ins-ant', 'charm': ['Ia/Id'], 'name': 'Agranular and dysgranular insula (anterior insula)', 'entity': 'ains', 'group': 'cortex', 'faces': 1500, 'tone': '#e879f9'})
add('macaque', {'key': 'ins-post', 'charm': ['Ig'], 'name': 'Granular insula (posterior insula)', 'entity': 'pins', 'group': 'cortex', 'faces': 1000, 'tone': '#c084fc'})

KP.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
PP.write_text(json.dumps(papers, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
MP.write_text(json.dumps(meshes, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('applied: 31 papers, 12 new entities (9 tagged insula, 3 shared), 8 extended, 27 links, 4 chains, 4 questions, 3 circuits, 7 mesh items')
