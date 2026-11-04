#!/usr/bin/env python3
"""Apply the olfactory region (2026-11-04, cloud session). Run once, from the repo root:

    python3 handoff/scripts/apply_olf.py && python3 tools/jsonfmt.py data/papers.json data/knowledge.json data/meshes.json

Adds 31 papers (handoff/olfactory/draft_papers.json), the region record, 10 tagged and 1 shared entity, sentences on
4 untagged shared entities, 19 links, 4 chains, 4 questions, 2 circuits, 3D aliases/sides/composite and mesh items.
Every sentence was written from the PubMed abstracts (HANDOFF section 6d). Asserts that ids are new and that every
link, chain and circuit resolves.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
KP, PP, MP = ROOT / 'data/knowledge.json', ROOT / 'data/papers.json', ROOT / 'data/meshes.json'
kb = json.loads(KP.read_text(encoding='utf-8'))
papers = json.loads(PP.read_text(encoding='utf-8'))
meshes = json.loads(MP.read_text(encoding='utf-8'))
draft = json.loads((ROOT / 'handoff/olfactory/draft_papers.json').read_text(encoding='utf-8'))
R = 'olfactory'

have = {p['key'] for p in papers}
for p in draft:
    assert p['key'] not in have, p['key']
papers.extend(draft)
PK = {p['key'] for p in papers}

assert R not in {r['id'] for r in kb['regions']}
kb['regions'].append({
    'id': R, 'label': 'Olfactory system', 'entity': 'olfactory',
    'query': '(olfactory[tiab] OR olfaction[tiab] OR odor*[tiab] OR odour*[tiab] OR piriform[tiab])',
    'view': 'olfactory',
    'views': ['atlas', 'scales', 'gaps', 'lab', 'library'],
    'levelDesc': {
        'regional': 'Olfactory bulb, piriform cortex, cortical amygdala, and the orbitofrontal and entorhinal targets',
        'circuit': 'Sensory neurons converge on glomeruli; mitral cells project diffusely to piriform cortex and in patches to the cortical amygdala; granule cells inhibit mitral cells',
    },
    'levelQueries': {
        'cellular': '("sensory neuron*"[tiab] OR "mitral cell*"[tiab] OR "granule cell*"[tiab] OR interneuron*[tiab] OR neurogenesis[tiab])',
        'circuit': '(glomerul*[tiab] OR circuit*[tiab] OR projection*[tiab] OR pathway*[tiab] OR oscillation*[tiab])',
        'regional': '("olfactory bulb"[tiab] OR piriform[tiab] OR "cortical amygdala"[tiab] OR "olfactory cortex"[tiab])',
    },
    'methods': {
        'molecular': {'manipulate': ['Receptor swaps and receptor knockouts', 'TRP2 knockout (vomeronasal signalling)', 'Single-cell expression of virus entry genes'],
                      'readout': ['Odorant receptor gene cloning', 'In situ hybridization of receptor mRNA', 'Calcium imaging with single-cell RT-PCR']},
        'cellular': {'manipulate': ['Genetic ablation of sensory neurons by zone', 'Genetic ablation of adult-born neurons', 'Grafts of subventricular zone cells'],
                     'readout': ['Genetic labelling of receptor-specific axons', 'Slice recordings of dendrodendritic synapses', 'Whole-cell recording in piriform cortex']},
        'circuit': {'manipulate': ['Optogenetic activation of piriform or cortical amygdala ensembles', 'Silencing the bulb-to-cortical-amygdala circuit', 'Pairing neuron activation with reward or shock'],
                    'readout': ['Tracing from single glomeruli', 'Rabies trans-synaptic tracing', 'Oscillations and sparse spiking']},
        'regional': {'manipulate': ['Orbitofrontal lesions (monkey)', 'Odorants at different concentrations', 'Sniffing odourless air'],
                     'readout': ['PET and fMRI activation by odours and sniffing', 'Multivariate fMRI patterns of odour quality', 'Evoked potentials along olfactory pathways']},
        'systems': {'manipulate': ['Nasal versus oral breathing', 'Odour-guided navigation', 'Eating a food to satiety'],
                    'readout': ['Respiration-locked oscillations', 'Entorhinal-hippocampal coherence', 'Orbitofrontal responses to food odours']},
        'cognitive': {'manipulate': ['Odour discrimination at psychophysical limits', 'Innate versus conditioned aversion', 'Breathing phase during memory tasks'],
                      'readout': ['Speed and accuracy of discrimination', 'Perceived odour similarity', 'Smell identification tests']},
        'clinical': {'manipulate': ['Population cohorts followed for Parkinson\'s disease', 'Follow-up of idiopathic smell loss', 'Meta-analysis across neurodegenerative diseases'],
                     'readout': ['Odour identification, recognition and threshold', 'Age-related smell loss', 'COVID-19 anosmia']},
    },
    'intro': {
        'title': 'Olfaction, from receptor genes to memory',
        'text': 'The olfactory system: how a large family of receptor genes and a map of glomeruli in the olfactory bulb encode odours, how the bulb\'s map is scattered across piriform cortex but kept in the cortical amygdala, how odours gain learned or innate meaning, the vomeronasal system and social behaviour, how breathing paces olfactory and limbic activity, and why smell fails with age, in Parkinson\'s and Alzheimer\'s diseases and in COVID-19. Every connection is tied to the papers behind it and graded by how strong the evidence is.',
    },
    'speciesNote': {
        'human': 'Human: the Allen olfactory bulb and piriform cortex. The atlas does not separate the cortical amygdala, so it is shown in the amygdala; olfactory sensory neurons are placed approximately (≈) in front of the bulb, and the vomeronasal organ is not placed.',
        'mouse': 'Mouse: Allen CCFv3 main and accessory olfactory bulbs, piriform area and cortical amygdalar area; olfactory sensory neurons are placed approximately (≈) in front of the bulb, and the vomeronasal organ is not placed.',
        'macaque': 'Macaque: SARM piriform cortex and ventral cortical amygdaloid nucleus. The template does not include the olfactory bulb, so the bulb and the olfactory sensory neurons are placed approximately (≈) under the front of the orbital surface; the vomeronasal organ is not placed.',
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


ent('olfactory', 'Olfactory system', 'systems', 'system', ['sensory'],
    'Distributed activity of sensory neurons in the nose is converted into a segregated map in the olfactory bulb and passed on to higher olfactory centres, including the piriform cortex and the cortical amygdala (mouse); a separate vomeronasal organ is thought to mediate pheromone-driven social behaviour (mouse). In humans, odours activate piriform and right orbitofrontal cortex (human), and smell identification declines markedly after the seventh decade (human). Smell is severely impaired in Alzheimer\'s and Parkinson\'s diseases (human), and impaired smell can precede clinical Parkinson\'s disease by at least 4 years (human).',
    ['sosulski2011', 'stowers2002', 'zatorre1992', 'doty1984', 'mesholam1998', 'ross2008'], aka=['olfaction', 'smell', 'olfactory pathway'])
ent('or-genes', 'Odorant receptor genes', 'molecular', 'gene', ['sensory'],
    'An extremely large multigene family of seven-transmembrane-domain proteins expressed only in the olfactory epithelium, likely to encode odorant receptors (rat). About 1000 receptor types are expressed in the mouse nose (mouse); one receptor recognizes several odorants and one odorant several receptors, but different odorants activate different combinations, so odours are encoded combinatorially (mouse).',
    ['buck1991', 'ressler1994', 'malnic1999'], aka=['ORs', 'olfactory receptors', 'odorant receptors'])
ent('osn', 'Olfactory sensory neurons', 'cellular', 'cell type', ['sensory'],
    'Sensory neurons of the nasal epithelium. Neurons expressing different receptors are scattered within four zones (mouse), and those expressing a given receptor converge on one or a few glomeruli (rat), two fixed loci among about 1800 in the mouse bulb (mouse). Ablating the dorsal-zone neurons abolishes innate aversion to odours without abolishing their detection (mouse). The SARS-CoV-2 entry protein ACE2 is expressed in nasal support, stem and perivascular cells rather than in these neurons (mouse, monkey, human).',
    ['ressler1994', 'vassar1994', 'mombaerts1996', 'kobayakawa2007', 'brann2020'], aka=['OSNs', 'olfactory receptor neurons', 'ORNs'])
ent('ob', 'Olfactory bulb', 'regional', 'structure', ['sensory'],
    'The first relay of smell, where receptor inputs converge on glomeruli to form a highly organized, perhaps stereotyped, spatial map (mouse); glomerular positions are bilaterally symmetric and constant across individuals (rat). Its dorsal domain carries innate aversive information (mouse). Mitral and granule cells interact through reciprocal dendrodendritic synapses (rat), and adult neurogenesis replaces most of its granule neurons (mouse). Rats discriminate odours at maximal accuracy within a single sniff (rat).',
    ['ressler1994', 'vassar1994', 'kobayakawa2007', 'isaacson1998', 'imayoshi2008', 'uchida2003'], aka=['OB', 'MOB', 'main olfactory bulb', 'glomeruli'])
ent('mitral', 'Mitral cells', 'cellular', 'cell type', ['sensory'],
    'Projection neurons of the olfactory bulb. Their dendrites release glutamate onto granule cell dendrites and receive GABAergic dendrodendritic inhibition back, which can mediate lateral inhibition between mitral cells without axonal action potentials (rat). Individual olfactory cortex neurons receive input from multiple mitral cells representing broadly distributed glomeruli (mouse).',
    ['isaacson1998', 'miyamichi2011'], aka=['mitral and tufted cells'])
ent('ob-granule', 'Bulb granule cells', 'cellular', 'cell type', ['sensory', 'development'],
    'Inhibitory interneurons of the olfactory bulb that provide NMDA receptor-dependent dendrodendritic inhibition to mitral cells (rat). They are replaced throughout adult life: subventricular zone cells migrate long distances and become olfactory bulb neurons (mouse), continuous neurogenesis replaces the majority of bulb granule neurons, and ablating new neurons gradually depletes them (mouse).',
    ['isaacson1998', 'lois1994', 'imayoshi2008'], aka=['granule cells', 'adult-born neurons', 'rostral migratory stream'])
ent('piriform', 'Piriform cortex', 'regional', 'area', ['sensory', 'memory'],
    'The primary olfactory cortex. Axons from individual glomeruli project diffusely across it, and its neurons sample the whole bulb without obvious spatial bias (mouse); odours evoke sparse spiking there, shaped by broadly tuned inhibition and fast oscillations (rat). Activating arbitrary ensembles of its neurons paired with reward or shock elicits learned behaviour (mouse). In humans, posterior piriform ensemble patterns track perceived odour quality (human), sniffing alone activates it (human), and odours activate it bilaterally (human); the identification and categorization of odours are thought to rely on odour objects formed there (review). Nasal breathing synchronizes its oscillations with those of the amygdala and hippocampus (human).',
    ['sosulski2011', 'miyamichi2011', 'poo2009', 'choi2011', 'howard2009', 'sobel1998', 'zatorre1992', 'gottfried2010', 'zelano2016'],
    aka=['PIR', 'Pir', 'primary olfactory cortex', 'pyriform cortex'])
ent('coa', 'Cortical amygdala', 'regional', 'area', ['sensory', 'emotion'],
    'The cortical amygdaloid nuclei. Projections from individual glomeruli form spatially stereotyped patches there, and it preferentially receives dorsal bulb input (mouse); its circuit from the bulb is necessary for innate aversive and appetitive odour responses, and activating its odour-responsive neurons recapitulates them (mouse).',
    ['sosulski2011', 'miyamichi2011', 'root2014'], aka=['CoA', 'COA', 'cortical amygdalar area', 'VCo'])
ent('vno', 'Vomeronasal organ', 'systems', 'body', ['social'],
    'A sensory organ thought to mediate social behaviours and neuroendocrine changes elicited by pheromones; activation of its sensory neurons requires the ion channel TRP2 (mouse).',
    ['stowers2002'], aka=['VNO', 'accessory olfactory system'])
ent('c-anosmia', 'Smell loss (anosmia)', 'clinical', 'disorder', ['sensory'],
    'More than half of people aged 65 to 80 and more than three-quarters of those over 80 have major impairment of smell identification (human). In COVID-19, infection of non-neuronal cells of the olfactory epithelium is suggested to cause anosmia (mouse, monkey, human).',
    ['doty1984', 'brann2020'], aka=['anosmia', 'hyposmia', 'olfactory dysfunction'])
ent('f-smell', 'Smell', 'cognitive', 'function', ['sensory'],
    'Detecting and discriminating odours. Odours are encoded by combinations of receptors (mouse), rats discriminate them at maximal accuracy within a single sniff (rat), and the cerebellum is activated by odours and by sniffing (human).',
    ['malnic1999', 'uchida2003', 'sobel1998cb'], aka=['olfaction', 'odour perception'], region=None)

extend('f-social', 'In male mice, loss of vomeronasal signalling abolishes male-male aggression and leads to courtship of both sexes (mouse).', ['stowers2002'])
extend('c-alzheimers', 'Odour identification, recognition and detection are severely impaired in Alzheimer\'s disease, as in Parkinson\'s disease (meta-analysis, human).', ['mesholam1998'])
extend('f-valence', 'Innate odour aversion depends on dorsal olfactory bulb glomeruli (mouse) and on the circuit from the bulb to the cortical amygdala (mouse).', ['kobayakawa2007', 'root2014'])
extend('f-feeding', 'Orbitofrontal responses to the odour of a food decline after that food is eaten to satiety (human).', ['odoherty2000'])

L = {f"{l['s']}>{l['t']}": l for l in kb['links']}


def link(s, t, kind, status, rel, refs):
    lid = f'{s}>{t}'
    assert lid not in L, lid
    assert s in E and t in E, lid
    l = {'s': s, 't': t, 'rel': rel, 'status': status, 'kind': kind, 'refs': refs_ok(refs)}
    kb['links'].append(l)
    L[lid] = l


link('or-genes', 'osn', 'mechanistic', 'established',
     'odorant receptors, a large multigene family expressed only in the olfactory epithelium (rat), encode odours combinatorially: one receptor recognizes several odorants and one odorant several receptors (mouse)',
     ['buck1991', 'malnic1999'])
link('osn', 'ob', 'anatomical', 'established',
     'neurons expressing a given receptor converge on one or a few glomeruli at positions constant across individuals (rat), two fixed loci among about 1800 in the mouse bulb (mouse), forming a fine spatial map (mouse)',
     ['vassar1994', 'mombaerts1996', 'ressler1994'])
link('ob', 'piriform', 'anatomical', 'supported',
     'axons from individual glomeruli project diffusely across piriform cortex, and piriform neurons sample the whole bulb without obvious spatial bias (mouse)', ['sosulski2011', 'miyamichi2011'])
link('ob', 'coa', 'anatomical', 'supported',
     'projections from individual glomeruli form spatially stereotyped patches in the cortical amygdala, which prefers dorsal bulb input (mouse)', ['sosulski2011', 'miyamichi2011'])
link('ob-granule', 'mitral', 'mechanistic', 'emerging',
     'reciprocal dendrodendritic synapses: mitral glutamate excites granule dendrites, which return NMDA receptor-dependent GABAergic inhibition that can mediate lateral inhibition between mitral cells (rat)',
     ['isaacson1998'])
link('mitral', 'piriform', 'anatomical', 'emerging',
     'individual olfactory cortex neurons receive input from multiple mitral cells representing broadly distributed glomeruli (mouse)', ['miyamichi2011'])
link('piriform', 'ofc', 'anatomical', 'emerging',
     'olfactory bulb signals reach the lateroposterior orbitofrontal cortex through the anterior piriform cortex (probably with the medial amygdala) and the hypothalamus, not the thalamus (monkey)',
     ['tanabe1975'])
link('ofc', 'f-smell', 'localization', 'supported',
     'odours activate the right orbitofrontal cortex (human) and its lateral and anterior gyri regardless of sniffing (human); removing the lateroposterior orbitofrontal area strikingly impairs odour discrimination (monkey); its response to a food\'s odour falls after that food is eaten to satiety (human)',
     ['zatorre1992', 'sobel1998', 'tanabe1975', 'odoherty2000'])
link('piriform', 'f-smell', 'localization', 'supported',
     'posterior piriform ensemble patterns track perceived odour quality (human), odours and sniffing activate piriform cortex (human), odours evoke sparse spiking there (rat), and odour objects are thought to form there (review)',
     ['howard2009', 'zatorre1992', 'sobel1998', 'poo2009', 'gottfried2010'])
link('piriform', 'f-valence', 'causal', 'emerging',
     'activating arbitrary piriform ensembles paired with reward or shock elicits learned appetitive or aversive behaviour (mouse)', ['choi2011'])
link('coa', 'f-valence', 'causal', 'emerging',
     'the bulb to cortical amygdala circuit is necessary for innate aversive and appetitive odour responses, and activating odour-responsive cortical amygdala neurons recapitulates them (mouse)',
     ['root2014'])
link('ob', 'f-valence', 'causal', 'emerging',
     'mice lacking dorsal bulb glomeruli detect aversive odours and can learn to avoid them but lack innate aversive responses (mouse)', ['kobayakawa2007'])
link('ob', 'f-smell', 'functional', 'supported',
     'the bulb\'s spatial map of glomeruli is proposed to let combinations of about 1000 receptor inputs discriminate odours (mouse), each odorant activating a specific topographic pattern (rat), and rats discriminate odours within a single sniff (rat)',
     ['ressler1994', 'vassar1994', 'uchida2003'])
link('vno', 'f-social', 'causal', 'emerging',
     'without the vomeronasal channel TRP2, male mice show no male-male aggression and court both sexes, suggesting that vomeronasal activation is essential for sex discrimination (mouse)', ['stowers2002'])
link('olfactory', 'c-parkinson', 'clinical', 'supported',
     'impaired smell can precede Parkinson\'s disease by at least 4 years (human), 7% of people with idiopathic smell loss developed it within 4 years (human), smell loss affects about 90% of early-stage cases (review), and deficits are severe across smell domains (meta-analysis, human)',
     ['ross2008', 'haehner2007', 'doty2012', 'mesholam1998'])
link('olfactory', 'c-alzheimers', 'clinical', 'supported',
     'odour identification, recognition and detection are severely impaired, as in Parkinson\'s disease (meta-analysis, human), and the deficits equal those of Parkinson\'s disease (review)',
     ['mesholam1998', 'doty2012'])
link('olfactory', 'c-anosmia', 'clinical', 'supported',
     'smell identification declines markedly after the seventh decade (human), and COVID-19 anosmia is suggested to stem from infection of non-neuronal support cells in the olfactory epithelium (mouse, monkey, human)',
     ['doty1984', 'brann2020'])
link('cb-cortex', 'f-smell', 'localization', 'emerging',
     'odours activate the posterior lateral cerebellar hemispheres, more at higher concentrations, and sniffing activates the anterior cerebellum (human); the cerebellum is proposed to regulate sniff volume according to odour concentration (hypothesis)',
     ['sobel1998cb'])
link('olfactory', 'entorhinal', 'anatomical', 'emerging',
     'the lateral entorhinal cortex and distal CA1 receive the predominant olfactory input to the hippocampal region, and their 20 to 40 Hz coupling develops as rats learn odour-guided navigation (rat)',
     ['igarashi2014'])

C = {c['id'] for c in kb['chains']}


def chain(id_, name, nodes, desc):
    assert id_ not in C, id_
    for a, b in zip(nodes, nodes[1:]):
        assert f'{a}>{b}' in L or f'{b}>{a}' in L, (id_, a, b)
    kb['chains'].append({'id': id_, 'name': name, 'nodes': nodes, 'desc': desc})
    C.add(id_)


chain('olf-code', 'From receptor genes to cortex', ['or-genes', 'osn', 'ob', 'piriform'],
      'Odorant receptors, a large gene family expressed in the olfactory epithelium (rat), encode odours combinatorially (mouse); neurons expressing one receptor converge on one or a few glomeruli (rat, mouse), and each glomerulus projects diffusely across piriform cortex (mouse).')
chain('olf-innate', 'Innate odour responses', ['ob', 'coa', 'f-valence'],
      'Glomeruli project in stereotyped patches to the cortical amygdala (mouse), and this circuit is necessary for innate aversive and appetitive odour responses (mouse).')
chain('olf-learned', 'Learned odour meaning', ['ob', 'piriform', 'f-valence'],
      'Glomeruli project diffusely to piriform cortex (mouse), where arbitrary ensembles of neurons can acquire learned appetitive or aversive meaning (mouse).')
chain('olf-ofc', 'Smell in the orbitofrontal cortex', ['piriform', 'ofc', 'f-smell'],
      'Olfactory bulb signals reach the lateroposterior orbitofrontal cortex through the anterior piriform cortex and the hypothalamus, and removing that area strikingly impairs odour discrimination (monkey).')

Q = {q['id'] for q in kb['questions']}


def question(id_, title, text, entities, refs, approaches):
    assert id_ not in Q, id_
    for e in entities:
        assert e in E, e
    for r in refs:
        assert f'({r})' in text, (id_, r)
    kb['questions'].append({'id': id_, 'title': title, 'text': text, 'entities': entities, 'refs': refs_ok(refs), 'approaches': approaches})
    Q.add(id_)


question('q-olf-map', 'Why is the bulb\'s map scattered in piriform cortex?',
         'Sensory neurons expressing one receptor converge on two fixed glomeruli (mombaerts1996), but each glomerulus projects diffusely across piriform cortex (sosulski2011) and piriform neurons sample the whole bulb (miyamichi2011); arbitrary piriform ensembles can acquire learned meaning (choi2011), and in humans posterior piriform patterns track perceived odour quality (howard2009). How does a scattered code support stable odour perception, and what does the stereotyped map in the cortical amygdala add?',
         ['ob', 'piriform', 'coa'], ['mombaerts1996', 'sosulski2011', 'miyamichi2011', 'choi2011', 'howard2009'],
         ['Record the same piriform neurons across days while animals learn new odour meanings.',
          'Compare odour responses of piriform and cortical amygdala neurons to innately and learned meaningful odours.',
          'Test whether disrupting the stereotyped amygdala projection alters odour perception or only innate behaviour.'])
question('q-olf-pd', 'Why does smell fail early in Parkinson\'s disease?',
         'Impaired smell can precede Parkinson\'s disease by at least 4 years (ross2008), 7% of people with idiopathic smell loss developed the disease within 4 years (haehner2007), and smell loss affects about 90% of early cases and correlates with neuron loss in the locus coeruleus, raphe and nucleus basalis (doty2012); Alzheimer\'s disease causes equally severe deficits (mesholam1998). Where in the olfactory pathway does the damage begin, and can smell tests pick out people at risk?',
         ['olfactory', 'c-parkinson', 'c-alzheimers'], ['ross2008', 'haehner2007', 'doty2012', 'mesholam1998'],
         ['Follow people with idiopathic smell loss with dopamine-transporter imaging and repeated smell tests.',
          'Map pathology along the olfactory pathway in people who died at prodromal stages.',
          'Compare smell deficits across neurodegenerative diseases to separate shared from disease-specific damage.'])
question('q-olf-cerebellum', 'What does the cerebellum do for smell?',
         'Odours activate the posterior lateral cerebellar hemispheres in proportion to concentration and sniffing activates the anterior cerebellum, and the authors propose that the cerebellum adjusts sniff volume to odour concentration (sobel1998cb). Sniffing alone drives piriform cortex (sobel1998), and rats discriminate odours within a single sniff (uchida2003). Does the cerebellum control sniffing, or does it take part in odour perception?',
         ['cb-cortex', 'f-smell', 'olfactory'], ['sobel1998cb', 'sobel1998', 'uchida2003'],
         ['Measure sniff volume and odour discrimination in people with cerebellar lesions.',
          'Record cerebellar activity in rodents while sniffing adapts to odour concentration.',
          'Perturb the cerebellum during odour discrimination and measure sniffing and accuracy separately.'])
question('q-olf-breath', 'Does breathing pace memory?',
         'Nasal breathing synchronizes oscillations in human piriform cortex, amygdala and hippocampus, and breathing phase enhanced fear discrimination and memory retrieval (zelano2016); respiration imposes a slow rhythm on piriform responses (poo2009), and lateral entorhinal-CA1 coupling develops as rats learn odour-guided navigation (igarashi2014). Is it the nasal airflow itself that times memory, and does the effect extend beyond smell?',
         ['piriform', 'entorhinal'], ['zelano2016', 'poo2009', 'igarashi2014'],
         ['Compare memory encoding during nasal and oral breathing with intracranial recordings.',
          'Block nasal airflow signals in rodents and measure hippocampal oscillations and memory.',
          'Time stimuli to inspiration or expiration in memory tasks without odours.'])

A3 = kb['atlas3d']
A3['composite']['olfactory'] = ['piriform', 'ob', 'coa']
for sp in ('human', 'mouse', 'macaque'):
    al = A3['aliases'][sp]
    for e, t in (('mitral', 'ob'), ('ob-granule', 'ob'), ('or-genes', 'osn')):
        assert e not in al
        al[e] = t
A3['aliases']['human']['coa'] = 'amygdala'
new_side = ['olfactory', 'or-genes', 'osn', 'ob', 'mitral', 'ob-granule', 'piriform', 'coa', 'vno']
for e in new_side:
    assert all(e not in v for v in A3['sides'].values()), e
A3['sides']['L'].extend(new_side)
CI = {c['id'] for c in A3['circuits']}


def circuit(id_, name, desc, links):
    assert id_ not in CI, id_
    for x in links:
        assert x in L, (id_, x)
    A3['circuits'].append({'id': id_, 'region': R, 'name': name, 'desc': desc, 'links': links, 'view': 'olfactory'})
    CI.add(id_)


circuit('olf-path', 'From the nose to olfactory cortex',
        'Sensory neurons expressing one receptor converge on one or a few glomeruli of the olfactory bulb (rat, mouse); each glomerulus projects diffusely across piriform cortex and in stereotyped patches to the cortical amygdala (mouse). Sensory neurons are placed approximately in front of the bulb.',
        ['osn>ob', 'ob>piriform', 'ob>coa'])
circuit('olf-beyond', 'Beyond olfactory cortex',
        'Olfactory signals reach the lateroposterior orbitofrontal cortex through the anterior piriform cortex and the hypothalamus (monkey), and the lateral entorhinal cortex receives the predominant olfactory input to the hippocampal region (rat).',
        ['piriform>ofc', 'olfactory>entorhinal'])

kb['meta']['subtitle'] = 'An evidence-linked map of the cerebellum, the motor and prefrontal cortex, the basal ganglia, the hippocampus, the amygdala, the visual cortex, the insula, the olfactory system and their connections, from molecules to mind'


def add(sp, item):
    keys = {it['key'] for it in meshes[sp]['items']}
    assert item['key'] not in keys, (sp, item['key'])
    meshes[sp]['items'].append(item)


add('human', {'key': 'ob', 'src': 10307, 'name': 'Olfactory bulb', 'entity': 'ob', 'group': 'target', 'faces': 600})
add('human', {'key': 'pir', 'src': 10311, 'name': 'Piriform cortex', 'entity': 'piriform', 'group': 'cortex', 'faces': 1000, 'tone': '#f0b37a'})
add('mouse', {'key': 'mob', 'src': [507, 151], 'name': 'Main and accessory olfactory bulbs', 'entity': 'ob', 'group': 'cortex', 'faces': 2000, 'tone': '#f6c177'})
add('mouse', {'key': 'pir', 'src': 961, 'name': 'Piriform area', 'entity': 'piriform', 'group': 'cortex', 'faces': 1500, 'tone': '#f0b37a'})
add('mouse', {'key': 'coa', 'src': 631, 'name': 'Cortical amygdalar area', 'entity': 'coa', 'group': 'cortex', 'faces': 800, 'tone': '#ff9e64'})
add('macaque', {'key': 'pir', 'sarm': ['Pir'], 'name': 'Piriform cortex', 'entity': 'piriform', 'group': 'cortex', 'faces': 1200, 'tone': '#f0b37a'})
add('macaque', {'key': 'vco', 'sarm': ['VCo'], 'name': 'Ventral cortical amygdaloid nucleus', 'entity': 'coa', 'group': 'cortex', 'faces': 500, 'tone': '#ff9e64'})

KP.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
PP.write_text(json.dumps(papers, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
MP.write_text(json.dumps(meshes, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('applied: 31 papers, 11 new entities (10 tagged olfactory, 1 shared), 4 extended, 19 links, 4 chains, 4 questions, 2 circuits, 7 mesh items')
