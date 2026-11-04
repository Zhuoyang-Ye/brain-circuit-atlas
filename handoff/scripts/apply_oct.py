#!/usr/bin/env python3
"""Add the octopus brain as a region of its own, drawn in a new 3D species, 'octopus' (2026-11-04, cloud session).

The user chose: octopus first; links only where an abstract states them; literature before any downloaded data. Every
sentence below is worded from the abstracts in handoff/octopus (keys.json; PMIDs verified with pubmed_abs.py find:
title, first author and year). messenger1967 has no abstract and is cited by its title only. Papers are tagged
`octopus` only, so links to shared functions stay in the octopus region. Applied once.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
KP, PP = ROOT / 'data/knowledge.json', ROOT / 'data/papers.json'
kb = json.loads(KP.read_text(encoding='utf-8'))
papers = json.loads(PP.read_text(encoding='utf-8'))
KEYS = json.loads((ROOT / 'handoff/octopus/keys.json').read_text(encoding='utf-8'))
O = ['octopus']


def P(key, evidence, methods, levels, domains, finding, species=None):
    return {'key': key, 'pmid': KEYS[key], 'regions': ['octopus'], 'evidence': evidence, 'species': species or O,
            'methods': methods, 'levels': levels, 'domains': domains, 'finding': finding}


new_papers = [
    P('jung2018', 'anatomical', ['histology (serial H&E sections)'], ['regional'], ['architecture'],
      'A histological atlas of the adult Octopus minor brain, from serial sagittal and coronal sections stained with haematoxylin and eosin, delineated more than 70 subregions; the authors describe it as the first brain atlas for any adult cephalopod (octopus).'),
    P('jacobs2022', 'anatomical', ['diffusion MRI tractography'], ['regional', 'circuit'], ['architecture'],
      'High angular resolution diffusion MRI tractography of three Octopus bimaculoides brains, segmented into 25 lobes, found 92 connections between lobes (53 among supra-oesophageal lobes and 26 between the optic lobes and other structures), largely agreeing with earlier studies, except that connections between the vertical lobe and more basal supra-oesophageal structures were not found (octopus).'),
    P('chung2022', 'anatomical', ['brain imaging', 'phylogenetic comparison'], ['regional'], ['architecture', 'sensory', 'social'],
      'A phylogenetically informed imaging comparison of diurnal and nocturnal coastal and deep-sea octopus species linked enlargement and division of the optic lobe and structural folding of the central brain to behaviour and habitat, with phylogeny possibly playing a part; the difference between solitary and social life was mirrored in the brain, including multiple compartments (gyri) in the vertical lobe, which the authors liken to the vertebrate cortex (octopus).'),
    P('saidel1982', 'anatomical', ['HRP tract tracing'], ['circuit'], ['sensory', 'architecture'],
      'Horseradish peroxidase tracing showed that the optic lobe receives input from the anterior, median and dorsal basal, interbasal, subvertical, precommissural, brachial and magnocellular lobes, the contralateral optic lobe, optic tract lobes and photoreceptors of the ipsilateral retina, and sends fibres to the superior frontal and lateral basal lobes; fibres partly from the posterior subvertical lobe were labelled in the neuropil of vertical lobules (octopus).'),
    P('shigeno2018', 'synthesis', ['review'], ['regional', 'systems'], ['architecture', 'development'],
      'Review: summarizes molecular, anatomical and developmental data and, from body and brain axes defined in early embryos, describes cephalopod neural systems that show similarities to the vertebrate cerebral cortex, thalamus, basal ganglia, midbrain, cerebellum, hypothalamus, brain stem and spinal cord, while how far a vertebrate equivalence exists remains unanswered.'),
    P('wangzy2024', 'anatomical', ['gene expression mapping'], ['molecular', 'regional'], ['homeostasis', 'architecture'],
      'In Octopus bimaculoides the peduncle complex rests on the optic tract between the optic lobe and the central brain and comprises the peduncle lobe, which regulates visuomotor behaviour, the olfactory lobe, thought to receive input from the olfactory organ, and the optic gland, which controls sexual maturation and maternal death; optic gland peptide and steroid pathways extended beyond the gland into lobular territories, and the olfactory lobe included steroidogenic territories overlapping cells expressing molluscan neuropeptides and dopamine beta-hydroxylase (octopus).'),
    P('styfhals2022', 'observational', ['single-cell transcriptomics', 'spatial mapping of cell types'], ['molecular', 'cellular'], ['architecture', 'memory', 'development'],
      'A cell type atlas of the paralarval Octopus vulgaris brain mapped neural cells, several glial subtypes, endothelial cells and fibroblasts to the vertical, subesophageal and optic lobes; vertical lobe cells were enriched for learning- and memory-related genes and showed molecular similarities with Drosophila Kenyon cells, and glia shared a gene signature with mouse and fly glia (octopus).'),
    P('songcocasey2022', 'observational', ['single-cell RNA sequencing', 'RNA fluorescence in situ hybridization'], ['molecular', 'cellular'], ['sensory', 'architecture'],
      'Single-cell RNA sequencing with RNA in situ hybridization of the Octopus bimaculoides optic lobe, the primary visual processing structure, revealed six major neuronal classes defined by neurotransmitter or neuropeptide use, subtypes with distinct laminar locations, and immature neurons in this continuously growing tissue (octopus).'),
    P('albertin2015', 'observational', ['genome and transcriptome sequencing'], ['molecular'], ['architecture', 'development'],
      'The Octopus bimaculoides genome showed no whole-genome duplications but massive expansions of the protocadherins, which regulate neuronal development, and of C2H2 zinc-finger transcription factors, extensive mRNA editing in genes for neural excitability and other functions, and hundreds of cephalopod-specific genes, many highly expressed in skin, suckers and the nervous system (octopus).'),
    P('hochner2003', 'observational', ['brain slice field potential recording'], ['cellular'], ['learning', 'memory'],
      'In brain slices of the vertical lobe, an area involved in learning and memory, field potential recordings revealed long-term potentiation of glutamatergic synaptic field potentials similar to that in vertebrates (octopus).'),
    P('shomrat2008', 'intervention', ['tetanization of the vertical lobe pathway', 'tract transection', 'passive avoidance learning'], ['circuit', 'cognitive'], ['learning', 'memory'],
      'Tetanizing the vertical lobe pathway to enhance its synapses globally accelerated short-term learning of a passive avoidance task, whereas transecting the pathway slowed it, but both impaired long-term recall the next day, suggesting that the vertical lobe acquires long-term memory through LTP and also modulates short-term learning (Octopus vulgaris).'),
    P('shomrat2011', 'observational', ['electrophysiology', 'comparative analysis'], ['cellular', 'circuit'], ['learning', 'memory'],
      'In both Octopus vulgaris and the cuttlefish Sepia officinalis the vertical lobe has the same fan-out fan-in architecture of three neuron types, but synaptic plasticity lies at the fan-out glutamatergic layer in the octopus and at the fan-in cholinergic layer in the cuttlefish; the linear input-output relations of the intermediate-layer neurons let both networks perform the same computation (octopus, cuttlefish).',
      species=['octopus', 'cuttlefish']),
    P('shomrat2010', 'intervention', ['immunohistochemistry', 'slice electrophysiology', 'pharmacology'], ['cellular', 'molecular'], ['learning', 'reward'],
      'Serotonin-immunoreactive afferent terminals innervate the neuropil, but not the cell bodies, of the vertical lobe, and 5-HT (effective at a high, 100 µM concentration) facilitated synaptic transmission and activity-dependent LTP induction without clear long-term facilitation; the authors propose it is part of a reinforcing or reward signalling system (Octopus vulgaris).'),
    P('shomrat2015', 'synthesis', ['review'], ['cellular', 'circuit'], ['learning', 'memory'],
      'Review: JZ Young described the morphological convergence of the cephalopod vertical lobe with the mammalian hippocampus, the cerebellum and the insect mushroom body; octopus and cuttlefish vertical lobes share a fan-out fan-in network with activity-dependent long-term plasticity, but their neurons, transmitters, neuromodulators and LTP mechanisms vary between species.'),
    P('sternmentch2022', 'anatomical', ['histolabeling', 'in situ hybridization', 'immunolabeling'], ['cellular', 'molecular'], ['learning', 'memory'],
      'Histolabeling of the vertical lobe confirmed glutamatergic median superior frontal lobe inputs and cholinergic amacrine interneurons, with intense nitric oxide synthase activity in amacrine neurites in line with NO-dependent presynaptic LTP; it also found GABAergic amacrines, GABA in large output neurons that co-express FMRFamide-like peptides, a glutamatergic group of output neurons and a catecholaminergic "deep nucleus" (Octopus vulgaris).'),
    P('bidel2023', 'anatomical', ['serial-section electron microscopy'], ['cellular', 'circuit'], ['learning', 'memory'],
      'Serial-section electron microscopy of a small volume of the Octopus vulgaris vertical lobe found that about 1.8 million input axons sparsely innervate two interconnected feedforward networks: simple amacrine cells (89.3% of about 25 million cells), each receiving input from a single input axon at a likely LTP "memory site", and newly described complex amacrine cells (1.6%) that integrate many inputs and appear to provide balancing inhibition to the output layer (octopus).'),
    P('fiorito1992', 'observational', ['visual discrimination test'], ['cognitive'], ['learning', 'social'],
      'Untrained octopuses that watched trained conspecifics choose between two objects differing only in colour then chose the same object, irrespective of which colour the demonstrators had been trained on and faster than by conditioning, showing observational learning in an invertebrate (Octopus vulgaris).'),
    P('fiorito1995', 'intervention', ['vertical lobe lesion', 'observational learning test'], ['regional', 'cognitive'], ['learning', 'memory', 'social'],
      'Removing about 50% of the vertical lobe impaired performance after observational learning of a visual discrimination, but performance improved 24 h later; the authors conclude that the lesion impairs short-term recall but not acquisition or retention of observational long-term memory (Octopus vulgaris).'),
    P('fiorito1998', 'intervention', ['pharmacology (scopolamine)'], ['molecular', 'cognitive'], ['memory'],
      'The muscarinic antagonist scopolamine did not affect predation on live crabs but impaired memory recall: solving the jar problem within the first hour after injection (partly recovered after 24 h) and both individually and observationally learned visual discriminations (Octopus vulgaris).'),
    P('robertson1994', 'intervention', ['pharmacology (nitric oxide synthase inhibitor)'], ['molecular', 'cognitive'], ['learning'],
      'Intramuscular injection of a nitric oxide synthase inhibitor completely blocked touch learning: eight control animals learned a touch paradigm and none of eight inhibitor-treated animals did, the first evidence that nitric oxide is essential for learning in an invertebrate (Octopus vulgaris).'),
    P('gutnick2023', 'observational', ['implanted electrodes with a data logger in freely moving animals'], ['circuit'], ['learning', 'memory'],
      'A data logger inserted into the octopus recorded activity from electrodes in the vertical lobe system for up to 12 h in unanaesthetized, untethered animals, synchronized with video; distinct activity patterns appeared consistently, some resembling mammalian patterns and others, such as episodes of 2 Hz large-amplitude oscillations, not reported before (octopus).'),
    P('pungor2023', 'observational', ['two-photon calcium imaging'], ['cellular', 'circuit'], ['sensory'],
      'Two-photon calcium imaging of the optic lobe, the primary visual processing centre, found spatially localized receptive fields for light (ON) and dark (OFF) stimuli, retinotopically organized, with the OFF pathway and greater size selectivity emerging across the layers of the optic lobe and asymmetries in spatial processing of ON and OFF stimuli (octopus).'),
    P('messenger1967', 'observational', [], ['regional'], ['motor', 'sensory'],
      'Per its title (PubMed lists no abstract): the peduncle lobe is a visuo-motor centre in the octopus (octopus).'),
    P('sumbre2001', 'intervention', ['arms severed from the brain', 'kinematic analysis'], ['circuit', 'systems'], ['motor'],
      'Arm extensions evoked mechanically or electrically in arms whose connection with the brain had been severed showed kinematic features almost identical to normal behaviour, suggesting that the basic motor program for voluntary arm extension is embedded in the neural circuitry of the arm itself (octopus).'),
    P('sumbre2006', 'observational', ['kinematic analysis'], ['systems', 'circuit'], ['motor'],
      'When fetching food to the mouth, octopus arms form a quasi-articulated structure with three dynamic joints; two waves of muscle activation propagate toward each other and their collision point sets the medial joint, and kinematic invariants appear at the joint level, as in certain human arm movements (octopus).'),
    P('zullo2009', 'intervention', ['brain microstimulation in freely behaving animals'], ['circuit', 'systems'], ['motor'],
      'Microstimulation of the basal lobes, the higher motor centres, in freely behaving octopuses evoked discrete and complex movements, recruited from shared basic components as stimulation strength increased, but no site evoked movement of a single arm or body part, so these centres show no central topographical organization (octopus).'),
    P('gutnick2011', 'observational', ['operant three-choice maze'], ['cognitive', 'systems'], ['motor', 'learning', 'sensory'],
      'In a three-choice maze that required a single arm to reach a visually marked goal compartment, octopuses guided one arm through a complex movement to the goal, showing that they combine peripheral arm location information with visual input to control goal-directed movement (Octopus vulgaris).'),
    P('gutnick2020', 'observational', ['operant two-choice single-arm mazes'], ['cognitive', 'systems'], ['motor', 'learning', 'sensory'],
      'In two-choice single-arm mazes that mimic tactile exploration, the central nervous system used peripheral information about arm motion as well as tactile input to learn tasks requiring directed arm movement; only about one third of octopus neurons are central, the rest lying in the peripheral nervous system including the eight arms, yet the arms are subject to central control (Octopus vulgaris).'),
    P('levy2015', 'observational', ['kinematic analysis'], ['systems'], ['motor'],
      'Kinematic analysis of crawling showed that octopuses can crawl in any direction relative to their body orientation, control body and crawling orientation independently, and coordinate their arms without apparent rhythmic patterns, the central controller choosing moment to moment which arms push the body by elongation (octopus).'),
    P('kuuspalu2022', 'anatomical', ['tracking of nerve cords'], ['circuit'], ['motor', 'architecture'],
      'The oral intramuscular nerve cords of each arm, thought to include proprioceptive neurons and motoneurons, continue beyond the arm base, bypass the two adjacent arms and join the nearer oral cord of the third arm over, so each arm connects to the arms two away on either side; the aboral cords also extend beyond the arm base (octopus).'),
    P('olson2025', 'anatomical', ['histology', 'molecular labelling', 'comparative study of squid'], ['cellular', 'circuit'], ['motor', 'sensory', 'architecture'],
      "The axial nerve cord of the octopus arm is segmented: its neurons form segments along the cord, nerves exit in the septa between segments, and for each sucker they form a spatial topographic map ('suckerotopy'); comparison with squid arms and tentacles links segmentation to flexible sucker-laden arms (octopus, squid).",
      species=['octopus', 'squid']),
    P('olson2025b', 'anatomical', ['in situ hybridization', 'histology'], ['cellular', 'molecular'], ['sensory', 'motor'],
      'The sucker ganglion in the stalk of every sucker contains cell bodies expressing sensory (PIEZO) and motor (LHX3, MNX) neuron markers, and its nerve fibres target the sucker musculature and the oral roots extending to the axial nerve cord; the authors suggest it facilitates local reflexes for each sucker rather than being a simple relay (Octopus bimaculoides).'),
    P('nesher2014', 'intervention', ['amputated arm preparation', 'behavioural tests'], ['systems'], ['motor', 'sensory'],
      'Suckers of amputated arms never attached to octopus skin because a chemical in the skin inhibits the sucker attachment reflex; behaving octopuses sometimes overrode this and grabbed amputated arms, and treated arms of other octopuses like food more often than their own (octopus).'),
    P('hochner2012', 'synthesis', ['review'], ['systems'], ['motor'],
      "Review: argues that the octopus's long, flexible arms, with their infinite degrees of freedom, have imposed unique brain-body-behaviour relationships best explained as intelligent behaviour emerging from the animal's embodied organization."),
    P('hochner2023', 'synthesis', ['review'], ['circuit', 'systems'], ['motor'],
      'Review: almost 30 years of research on Octopus vulgaris motor control show that the higher motor control centres coordinate limbs with large numbers of degrees of freedom without using body-part maps to represent sensory and motor information, as vertebrates do, through control embodied in the body morphology.'),
    P('zullo2019', 'intervention', ['isolated nerve tract stimulation and recording'], ['circuit'], ['motor'],
      'In isolated cerebrobrachial tracts connecting the brain and the arms, electrical activity and contraction of a small attached muscle strand were evoked at low threshold regardless of stimulus direction and distance, suggesting that axons carrying motor commands run along the tract and innervate a large pool of motor neurons en passant (Octopus vulgaris).'),
    P('vangiesen2020', 'observational', ['receptor and cell physiology'], ['molecular', 'cellular'], ['sensory'],
      "Octopus arms use a family of cephalopod-specific chemotactile receptors, which form discrete ion channel complexes, to detect poorly soluble natural products on contact ('taste by touch'), and distinct chemo- and mechanosensory cells with specific receptor expression and electrical activity support peripheral information coding (octopus)."),
    P('allard2023', 'observational', ['cryo-electron microscopy', 'evolutionary and biophysical analysis'], ['molecular'], ['sensory'],
      'A cryo-electron microscopy structure of an octopus chemotactile receptor, which diverged from nicotinic acetylcholine receptors, showed a conserved channel architecture but a ligand-binding site under diversifying selection, with an exceptionally hydrophobic binding pocket suited to sensing greasy compounds (octopus).'),
    P('pophale2023', 'observational', ['high-density electrophysiology', 'computational analysis of skin patterns'], ['circuit', 'cognitive'], ['homeostasis', 'memory'],
      "Octopus 'quiet' sleep is interrupted by bouts of about 60 s of 'active' sleep that are homeostatically regulated, rapidly reversible and have a raised arousal threshold, with skin patterns strongly resembling waking ones; local field potentials during active sleep resemble waking, strongest in the superior frontal and vertical lobes, which in quiet sleep are relatively silent but generate oscillations resembling mammalian sleep spindles (octopus)."),
    P('medeiros2021', 'observational', ['video recording', 'automated image analysis', 'arousal threshold tests'], ['cognitive'], ['homeostasis'],
      "In Octopus insularis a 'quiet sleep' state with pale skin, closed pupils and long episodes alternated with short 'active sleep' episodes (median 40.8 s) with dynamic skin colour and texture and rapid eye movements; active sleep recurred periodically (60% of recurrences 26 to 39 min apart) and mostly followed quiet sleep, suggesting an ultradian sleep cycle analogous to that of amniotes (octopus)."),
    P('wangzy2018', 'observational', ['transcriptome sequencing', 'behavioural analysis'], ['molecular', 'systems'], ['homeostasis'],
      'Maternal behaviours of brooding female octopuses are eradicated if the optic glands, the octopus analogue of the pituitary, are removed; across behavioural stages the optic gland up- and downregulated catecholamine, steroid, insulin and feeding peptide pathways, changes that were not general markers of senescence in other tissues (Octopus bimaculoides).'),
    P('wang2022', 'observational', ['mass spectrometry'], ['molecular'], ['homeostasis'],
      'The optic glands control lifespan and reproduction, and their removal reverses the post-mating course of brooding, fasting, self-injury and death; after reproduction, female optic glands mobilized at least three steroidogenic pathways, producing pregnane steroids, 7-dehydrocholesterol and bile acid intermediates (Octopus bimaculoides).'),
    P('edsinger2018', 'intervention', ['pharmacology (MDMA)', 'genome analysis'], ['molecular', 'cognitive'], ['social'],
      'MDMA enhanced acute prosocial behaviour in Octopus bimaculoides, a member of a predominantly asocial and solitary order, paralleled by evolutionary conservation of the MDMA binding site of the serotonin transporter in its genome, suggesting that serotonergic transmission has a conserved role in social behaviour (octopus).'),
    P('crook2021', 'intervention', ['conditioned place preference', 'local anaesthesia'], ['cognitive'], ['emotion'],
      'Octopuses avoided a context in which pain was experienced, preferred one where they experienced relief and showed no conditioned preference without pain, and grooming of an acetic acid injection site was abolished by local anaesthesia, suggesting that octopuses experience the affective component of pain (octopus).'),
    P('alupay2014', 'observational', ['behavioural observation', 'electrophysiology'], ['cellular', 'systems'], ['sensory'],
      'After arm injury the octopus Abdopus aculeatus showed nocifensive behaviours including arm autotomy and neural hyperexcitability in both injured and uninjured arms for at least 24 h; the authors note that this does not demonstrate pain-like states (octopus).'),
    P('deryckere2021', 'observational', ['histology', 'lineage tracing'], ['cellular', 'molecular'], ['development'],
      'In Octopus vulgaris embryos an important pool of neural progenitors expressing achaete-scute or neurogenin lies outside the central brain cords, in the lateral lips next to the eyes, and lineage tracing showed that their progeny generate neurons for the different lobes, migrating over long distances, as in the squid Doryteuthis pealeii (octopus).'),
]
have = {p['key'] for p in papers}
pm = {str(p['pmid']) for p in papers}
for p in new_papers:
    assert p['key'] not in have and str(p['pmid']) not in pm, p['key']
assert len(new_papers) == len(KEYS) - 2, (len(new_papers), len(KEYS))   # budelmann1994 and zarrella2015 dropped
papers.extend(new_papers)
PK = {p['key'] for p in new_papers}

# ------------------------------------------------------------------ region
assert 'octopus' not in {r['id'] for r in kb['regions']}
kb['regions'].append({
    'id': 'octopus', 'label': 'Octopus brain', 'group': 'Octopus', 'species': ['octopus'], 'entity': 'oct-brain',
    'query': '(octopus[tiab] OR octopuses[tiab] OR octopod*[tiab] OR cephalopod*[tiab])',
    'view': 'octopus', 'views': ['atlas', 'scales', 'gaps', 'lab', 'library'],
    'levelDesc': {
        'regional': 'Vertical, superior frontal, subvertical, basal and brachial lobes; optic lobes; the peduncle complex and optic gland; the arms’ nerve cords',
        'circuit': 'Retina to optic lobe; optic lobe to the superior frontal and basal lobes; superior frontal input to the vertical lobe; basal lobes and brain to the arms',
    },
    'levelQueries': {
        'cellular': '(neuron*[tiab] OR amacrine[tiab] OR interneuron*[tiab])',
        'circuit': '(circuit*[tiab] OR connect*[tiab] OR pathway*[tiab] OR tract*[tiab])',
        'regional': '("vertical lobe"[tiab] OR "optic lobe"[tiab] OR "basal lobe"[tiab] OR "frontal lobe"[tiab])',
    },
    'methods': {
        'molecular': {'manipulate': ['Nitric oxide synthase inhibition', 'Muscarinic block (scopolamine)', 'MDMA'],
                      'readout': ['Single-cell RNA sequencing', 'In situ hybridization', 'Mass spectrometry of optic gland secretions']},
        'cellular': {'manipulate': ['Tetanic stimulation of the vertical lobe pathway', 'Serotonin applied to brain slices'],
                     'readout': ['Field potentials in vertical lobe slices', 'Serial-section electron microscopy', 'Histolabeling of transmitters']},
        'circuit': {'manipulate': ['Transecting the vertical lobe pathway', 'Stimulating isolated cerebrobrachial tracts'],
                    'readout': ['HRP tract tracing', 'Diffusion MRI tractography', 'Two-photon calcium imaging of the optic lobe']},
        'regional': {'manipulate': ['Vertical lobe lesions', 'Microstimulation of the basal lobes', 'Optic gland removal'],
                     'readout': ['Histological brain atlas', 'Comparative brain imaging across species']},
        'systems': {'manipulate': ['Arms severed from the brain', 'Arm injury'],
                    'readout': ['Data loggers in freely moving animals', 'High-density brain recordings during sleep', 'Arm kinematics']},
        'cognitive': {'manipulate': ['Watching trained conspecifics', 'Passive avoidance training', 'Single-arm maze tasks'],
                      'readout': ['Visual discrimination choices', 'Recall the next day', 'Sleep stages scored from skin patterns']},
        'clinical': {'manipulate': ['Noxious stimulation with local anaesthesia'],
                     'readout': ['Nocifensive behaviour', 'Conditioned place preference']},
    },
    'intro': {
        'title': 'Octopus brain, a large brain that evolved separately',
        'text': 'The cephalopod brain evolved independently of the vertebrate brain. Here: the vertical lobe’s learning and memory network and its long-term potentiation, the optic lobes’ visual maps, the basal lobes that command eight arms without a body map, the arms’ own nerve cords and suckers that taste by touch, two stages of sleep, and the optic gland that controls maturation and maternal death. Every connection is tied to the papers behind it and graded by how strong the evidence is.',
    },
    'speciesNote': {
        'octopus': 'Octopus: a schematic brain drawn for this site, because no octopus atlas volume is available to it. Lobe shapes, sizes and positions are approximate and for orientation only, so every label carries ≈. The vertical lobe’s amacrine and output neurons are shown in the vertical lobe. Findings come from several species (mainly Octopus vulgaris and O. bimaculoides).',
    },
})

# ------------------------------------------------------------------ entities
E = {e['id']: e for e in kb['entities']}


def ent(id_, name, level, kind, domains, summary, refs, aka=None, region='octopus'):
    assert id_ not in E, id_
    for r in refs:
        assert r in PK, (id_, r)
    e = {'id': id_, 'name': name, 'level': level, 'kind': kind}
    if aka:
        e['aka'] = aka
    if region:
        e['region'] = region
    e.update(domains=domains, summary=summary, refs=refs)
    kb['entities'].append(e)
    E[id_] = e


ent('oct-brain', 'Octopus brain', 'systems', 'structure', ['architecture'],
    'The central brain of the octopus. Only about one third of octopus neurons are central; the rest lie in the peripheral nervous system, including the eight arms (octopus). A histological atlas of the adult Octopus minor brain delineates more than 70 subregions (octopus), and diffusion MRI tractography of 25 lobes found 92 connections between them, largely matching earlier studies (octopus). Its genome shows massive expansions of protocadherins and C2H2 zinc-finger transcription factors and extensive mRNA editing (octopus). In embryos, neural progenitors outside the brain cords, in the lateral lips next to the eyes, generate neurons that migrate long distances into the lobes (octopus). Cephalopod neural systems have been compared with the vertebrate cortex, thalamus, basal ganglia, cerebellum and other structures, but how far a vertebrate equivalence exists is unanswered (review). Inhibiting nitric oxide synthesis blocks touch learning (octopus), and the muscarinic antagonist scopolamine impairs memory recall without affecting predation (octopus).',
    ['gutnick2020', 'jung2018', 'jacobs2022', 'albertin2015', 'deryckere2021', 'shigeno2018', 'robertson1994', 'fiorito1998'],
    aka=['central brain', 'cephalopod brain'])
ent('oct-vl', 'Vertical lobe', 'regional', 'structure', ['learning', 'memory'],
    'A learning and memory centre of the octopus brain. Its synapses show glutamatergic long-term potentiation similar to that in vertebrates (octopus); enhancing its pathway speeds and cutting it slows short-term avoidance learning, but both impair recall the next day, so it acquires long-term memory through LTP and also modulates short-term learning (octopus). Removing about half of it impairs short-term recall of a visual discrimination learned by watching another octopus, but not its acquisition or long-term retention (octopus). About 1.8 million input axons sparsely innervate some 25 million amacrine interneurons (octopus), and serotonin-containing terminals in its neuropil facilitate transmission and LTP induction (octopus). Its cells are enriched for learning- and memory-related genes and resemble Drosophila Kenyon cells molecularly (octopus), and JZ Young likened its organization to the hippocampus, the cerebellum and the insect mushroom body (review). Differences between social and solitary species include multiple compartments (gyri) in it (octopus). Its activity can be recorded in untethered, behaving animals, with episodes of 2 Hz large-amplitude oscillations (octopus), and with the superior frontal lobe it is most active during active sleep (octopus).',
    ['hochner2003', 'shomrat2008', 'fiorito1995', 'bidel2023', 'shomrat2010', 'styfhals2022', 'shomrat2015', 'chung2022', 'gutnick2023', 'pophale2023'],
    aka=['VL', 'vertical lobe system', 'vertical lobules'])
ent('oct-sfl', 'Superior frontal lobe', 'regional', 'structure', ['learning', 'memory'],
    'A lobe of the supra-oesophageal brain. Its median part, the median superior frontal lobe (MSFL), sends the glutamatergic input axons of the vertical lobe, which innervate millions of amacrine interneurons en passant (octopus). It receives fibres from the optic lobe (octopus), and with the vertical lobe it shows the strongest wake-like activity in active sleep and spindle-like oscillations in quiet sleep (octopus).',
    ['sternmentch2022', 'saidel1982', 'pophale2023'], aka=['SFL', 'median superior frontal lobe', 'MSFL', 'MSF'])
ent('oct-vl-am', 'Vertical lobe amacrine interneurons', 'cellular', 'cell type', ['learning', 'memory'],
    'The small interneurons of the vertical lobe: input axons from the median superior frontal lobe innervate them en passant, and they converge sharply onto the large output neurons (octopus). Simple amacrine cells (89.3% of about 25 million cells) each receive one input axon at a synapse endowed with LTP, while the newly described complex amacrine cells integrate many inputs and appear to provide balancing inhibition (octopus). They are cholinergic, with a GABAergic subpopulation, and their neurites show intense nitric oxide synthase activity (octopus).',
    ['sternmentch2022', 'bidel2023'], aka=['amacrine cells', 'AMs', 'simple amacrine cells', 'SAMs', 'complex amacrine cells', 'CAMs'])
ent('oct-vl-ln', 'Vertical lobe large output neurons', 'cellular', 'cell type', ['learning', 'memory'],
    'The output neurons of the vertical lobe, onto which amacrine interneurons converge through cholinergic synapses (octopus). Many contain GABA together with FMRFamide-like neuropeptides, suggesting an inhibitory output with a neuromodulatory role, and a group is glutamatergic (octopus). In the cuttlefish, unlike the octopus, synaptic plasticity lies at this cholinergic fan-in layer (cuttlefish).',
    ['sternmentch2022', 'shomrat2011'], aka=['LNs', 'large neurons'])
ent('oct-subvertical', 'Subvertical lobe', 'regional', 'structure', ['memory', 'architecture'],
    'A supra-oesophageal lobe whose cells project to the optic lobe; fibres partly from its posterior part reach the neuropil of the vertical lobules (octopus).',
    ['saidel1982'], aka=['SV'])
ent('oct-basal', 'Basal lobes', 'regional', 'structure', ['motor'],
    'The higher motor centres of the central brain. Microstimulating them in freely behaving octopuses evokes discrete and complex movements, but no site moves a single arm or body part, so they lack a central topographical map (octopus), and they coordinate the arms without body-part maps of sensory and motor information (review). The anterior, median and dorsal basal lobes send input to the optic lobe, which sends fibres back to the lateral basal lobe (octopus).',
    ['zullo2009', 'hochner2023', 'saidel1982'], aka=['higher motor centres', 'anterior basal lobe', 'median basal lobe', 'dorsal basal lobe', 'lateral basal lobe'])
ent('oct-brachial', 'Brachial lobe', 'regional', 'structure', ['motor'],
    'A lobe of the sub-oesophageal brain whose cells send input to the optic lobe (octopus).',
    ['saidel1982'])
ent('oct-eye', 'Eye (octopus)', 'systems', 'body', ['sensory'],
    'Cephalopods have camera-type eyes and rely heavily on vision (octopus). Photoreceptors of its retina project to the optic lobe on the same side (octopus), and octopuses use vision to guide a single arm to a goal (octopus).',
    ['pungor2023', 'saidel1982', 'gutnick2011'], aka=['octopus eye', 'retina'])
ent('oct-ol', 'Optic lobe', 'regional', 'structure', ['sensory'],
    'The paired primary visual processing centres. Two-photon imaging shows retinotopically organized ON and OFF receptive fields, with the OFF pathway and greater size selectivity emerging across its layers (octopus), and single-cell sequencing finds six major neuronal classes with distinct laminar positions and immature neurons in this continuously growing tissue (octopus). Its medulla receives input from many higher motor and associative lobes, the contralateral optic lobe and the retina (octopus). Its enlargement and division differ with habit and habitat across octopus species (octopus).',
    ['pungor2023', 'songcocasey2022', 'saidel1982', 'chung2022'], aka=['OL', 'optic lobes'])
ent('oct-peduncle', 'Peduncle lobe', 'regional', 'structure', ['motor', 'sensory'],
    'Part of the peduncle complex, which rests on the optic tract between the optic lobe and the central brain; described as a visuo-motor centre that regulates visuomotor behaviour (octopus).',
    ['messenger1967', 'wangzy2024'], aka=['peduncle complex'])
ent('oct-olf-lobe', 'Olfactory lobe', 'regional', 'structure', ['sensory'],
    'Part of the peduncle complex, thought to receive input from the olfactory organ. It is heterogeneous and includes steroidogenic territories that overlap cells expressing molluscan neuropeptides and dopamine beta-hydroxylase (octopus).',
    ['wangzy2024'])
ent('oct-optic-gland', 'Optic gland', 'systems', 'structure', ['homeostasis'],
    'The principal neuroendocrine centre of the octopus, an analogue of the vertebrate pituitary, in the peduncle complex (octopus). It controls sexual maturation, lifespan and reproduction: removing it abolishes maternal brooding and reverses the post-mating decline toward death (octopus). After mating it shifts catecholamine, steroid, insulin and feeding-peptide signalling and raises synthesis of pregnane steroids, 7-dehydrocholesterol and bile acid intermediates (octopus), and its neurochemistry extends into neighbouring lobular territories (octopus).',
    ['wangzy2018', 'wang2022', 'wangzy2024'], aka=['optic glands'])
ent('oct-arm-ns', 'Arm nervous system', 'systems', 'structure', ['motor', 'sensory'],
    "Most octopus neurons lie outside the brain, in the peripheral nervous system including the eight arms (octopus). Each arm's axial nerve cord is segmented, with nerves leaving between segments and a topographic map of the suckers ('suckerotopy') (octopus, squid). Severed arms still produce near-normal extensions, so the basic motor program lies in the arm itself (octopus), and fetching food uses three dynamic joints set where two waves of muscle activation collide (octopus). Motor command axons run along the cerebrobrachial tracts and recruit many motor neurons en passant (octopus). Nerve cords link each arm with the arms two away on either side, outside the brain (octopus), and when crawling the octopus recruits arms moment to moment without rhythmic patterns (octopus). Arm injury causes neural hyperexcitability in injured and uninjured arms for at least 24 h (octopus).",
    ['gutnick2020', 'olson2025', 'sumbre2001', 'sumbre2006', 'zullo2019', 'kuuspalu2022', 'levy2015', 'alupay2014'],
    aka=['arms', 'axial nerve cord', 'ANC', 'intramuscular nerve cords', 'cerebrobrachial tract'])
ent('oct-sucker', 'Suckers', 'systems', 'body', ['sensory', 'motor'],
    "Hundreds of suckers line each arm. A ganglion in each sucker's stalk contains sensory and motor neurons and sends fibres to the sucker muscles and to the axial nerve cord, suggesting local reflexes for each sucker (octopus). Suckers 'taste by touch' with cephalopod-specific chemotactile receptors, which diverged from nicotinic acetylcholine receptors and detect poorly soluble, greasy molecules (octopus). A chemical in octopus skin inhibits their attachment reflex, so that the arms do not interfere with each other (octopus).",
    ['olson2025b', 'vangiesen2020', 'allard2023', 'nesher2014'], aka=['sucker', 'sucker ganglion'])
ent('f-sleep', 'Sleep', 'cognitive', 'function', ['homeostasis'],
    "Sleep and its stages. Octopuses alternate long 'quiet' sleep with short 'active' sleep bouts with dynamic skin patterns and rapid eye movements, suggesting an ultradian cycle analogous to that of amniotes (octopus); active sleep is homeostatically regulated, and its skin patterns and brain activity resemble waking (octopus).",
    ['medeiros2021', 'pophale2023'], region=None)
ent('f-reproduction', 'Reproduction and maternal care', 'cognitive', 'function', ['homeostasis', 'social'],
    'Sexual maturation, reproduction and care of offspring. In the octopus the optic glands control maturation, reproduction and lifespan; after mating, brooding females fast and decline toward death, a course that removing the glands reverses (octopus).',
    ['wang2022', 'wangzy2018'], region=None, aka=['maternal behaviour', 'brooding'])


def extend(id_, sentence, refs):
    e = E[id_]
    assert not e.get('region'), id_
    e['summary'] = e['summary'].rstrip() + ' ' + sentence
    for r in refs:
        assert r in PK
        if r not in e['refs']:
            e['refs'].append(r)


extend('f-pain', 'Octopuses avoid a place where they experienced pain and prefer one where it was relieved, suggesting that an invertebrate experiences the affective component of pain (octopus).', ['crook2021'])
extend('f-social', 'In the predominantly asocial octopus, MDMA enhances prosocial behaviour and the serotonin transporter keeps its MDMA binding site (octopus), and untrained octopuses learn a visual discrimination by watching trained ones (octopus).', ['edsinger2018', 'fiorito1992'])

# ------------------------------------------------------------------ links
L = {f"{l['s']}>{l['t']}" for l in kb['links']}
LINKS = [
    ('oct-eye', 'oct-ol', 'anatomical', 'supported', 'photoreceptors of the ipsilateral retina project to the optic lobe (HRP tracing), where ON and OFF receptive fields are retinotopically organized (calcium imaging) (octopus)', ['saidel1982', 'pungor2023']),
    ('oct-ol', 'f-vision', 'functional', 'supported', 'the primary visual processing centre: retinotopic ON and OFF receptive fields, with the OFF pathway and size selectivity emerging across its layers (two-photon imaging) (octopus)', ['pungor2023', 'songcocasey2022']),
    ('oct-basal', 'oct-ol', 'anatomical', 'supported', 'the anterior, median and dorsal basal lobes send input to the optic lobe (HRP tracing) (octopus)', ['saidel1982']),
    ('oct-ol', 'oct-basal', 'anatomical', 'supported', 'optic lobe fibres reach the lateral basal lobe (HRP tracing) (octopus)', ['saidel1982']),
    ('oct-subvertical', 'oct-ol', 'anatomical', 'supported', 'subvertical lobe cells send input to the optic lobe (HRP tracing) (octopus)', ['saidel1982']),
    ('oct-brachial', 'oct-ol', 'anatomical', 'supported', 'brachial lobe cells send input to the optic lobe (HRP tracing) (octopus)', ['saidel1982']),
    ('oct-ol', 'oct-sfl', 'anatomical', 'supported', 'optic lobe fibres reach the superior frontal lobe (HRP tracing) (octopus)', ['saidel1982']),
    ('oct-sfl', 'oct-vl', 'anatomical', 'established', 'the median superior frontal lobe sends the glutamatergic input of the vertical lobe, about 1.8 million axons whose synapses show LTP (histolabeling, electron microscopy, slice recordings) (octopus)', ['sternmentch2022', 'bidel2023', 'hochner2003']),
    ('oct-subvertical', 'oct-vl', 'anatomical', 'emerging', 'fibres partly from the posterior subvertical lobe reach the neuropil of the vertical lobules (HRP tracing) (octopus)', ['saidel1982']),
    ('oct-sfl', 'oct-vl-am', 'anatomical', 'established', 'input axons innervate the amacrine interneurons en passant at a glutamatergic synapse with LTP; each simple amacrine cell receives a single input axon (fan-out) (octopus)', ['sternmentch2022', 'bidel2023', 'shomrat2011']),
    ('oct-vl-am', 'oct-vl-ln', 'anatomical', 'supported', 'amacrine interneurons converge sharply onto the large output neurons through cholinergic synapses (fan-in) (octopus)', ['sternmentch2022', 'shomrat2011']),
    ('oct-vl', 'f-consolidation', 'functional', 'supported', 'acquires long-term memory through LTP: tetanizing or cutting its pathway impairs recall the next day (octopus)', ['shomrat2008', 'hochner2003']),
    ('oct-vl', 'f-social', 'functional', 'emerging', 'removing about half of it impairs short-term recall of a discrimination learned by watching another octopus, but not acquisition or long-term retention (octopus)', ['fiorito1995']),
    ('oct-vl', 'f-sleep', 'functional', 'emerging', 'with the superior frontal lobe, strongest wake-like activity in active sleep and spindle-like oscillations in quiet sleep (high-density recordings) (octopus)', ['pophale2023']),
    ('oct-sfl', 'f-sleep', 'functional', 'emerging', 'with the vertical lobe, strongest wake-like activity in active sleep and spindle-like oscillations in quiet sleep (high-density recordings) (octopus)', ['pophale2023']),
    ('oct-basal', 'oct-arm-ns', 'causal', 'supported', 'microstimulation of these higher motor centres evokes discrete and complex movements, but never of a single arm: no central body map (octopus)', ['zullo2009', 'hochner2023']),
    ('oct-brain', 'oct-arm-ns', 'anatomical', 'emerging', 'motor command axons run along the cerebrobrachial tracts and recruit many arm motor neurons en passant (isolated tract recordings) (octopus)', ['zullo2019']),
    ('oct-arm-ns', 'oct-brain', 'functional', 'emerging', 'the central brain uses information about one arm’s motion and touch to learn directed arm movements (single-arm mazes) (octopus)', ['gutnick2020']),
    ('oct-eye', 'oct-arm-ns', 'functional', 'emerging', 'vision guides a single arm through a complex movement to a visually marked goal (three-choice maze) (octopus)', ['gutnick2011']),
    ('oct-arm-ns', 'f-motor', 'functional', 'supported', 'the arm’s own circuitry holds motor programs: severed arms still extend almost normally, and fetching uses joints set where two waves of muscle activation collide (octopus)', ['sumbre2001', 'sumbre2006']),
    ('oct-sucker', 'oct-arm-ns', 'anatomical', 'emerging', 'each sucker’s ganglion sends fibres to the oral roots of the axial nerve cord, whose segments map the suckers in order (‘suckerotopy’) (octopus)', ['olson2025b', 'olson2025']),
    ('oct-sucker', 'f-taste', 'functional', 'emerging', '‘taste by touch’: cephalopod-specific chemotactile receptors detect poorly soluble molecules on contact (octopus)', ['vangiesen2020', 'allard2023']),
    ('oct-arm-ns', 'f-pain', 'functional', 'emerging', 'arm injury triggers nocifensive behaviour, including arm autotomy, and hyperexcitability in injured and uninjured arms for at least 24 h (octopus)', ['alupay2014']),
    ('oct-peduncle', 'f-motor', 'functional', 'supported', 'a visuo-motor centre that regulates visuomotor behaviour (octopus)', ['messenger1967', 'wangzy2024']),
    ('oct-olf-lobe', 'f-smell', 'functional', 'hypothesis', 'thought to receive input from the olfactory organ (octopus)', ['wangzy2024']),
    ('oct-optic-gland', 'f-reproduction', 'causal', 'supported', 'removing the optic glands abolishes maternal brooding and reverses the post-mating decline toward death; after mating they shift steroid, catecholamine, insulin and feeding-peptide signalling (octopus)', ['wangzy2018', 'wang2022']),
]
for s, t, kind, status, rel, refs in LINKS:
    assert f'{s}>{t}' not in L, (s, t)
    assert s in E and t in E, (s, t)
    for r in refs:
        assert r in PK
    kb['links'].append({'s': s, 't': t, 'rel': rel, 'status': status, 'kind': kind, 'refs': refs})
    L.add(f'{s}>{t}')

# ------------------------------------------------------------------ chains
C = {c['id'] for c in kb['chains']}
for cid, name, nodes, desc in [
    ('oct-eye-memory', 'From the eye to the vertical lobe', ['oct-eye', 'oct-ol', 'oct-sfl', 'oct-vl'],
     'Retinal photoreceptors project to the optic lobe, whose fibres reach the superior frontal lobe (HRP tracing); the median superior frontal lobe sends the glutamatergic input of the vertical lobe, whose LTP supports long-term memory (octopus).'),
    ('oct-fan', "The vertical lobe's fan-out fan-in network", ['oct-sfl', 'oct-vl-am', 'oct-vl-ln'],
     'About 1.8 million input axons from the median superior frontal lobe innervate some 25 million amacrine interneurons, which converge sharply onto large output neurons; plasticity sits at the input layer in the octopus and at the output layer in the cuttlefish, yet both networks perform the same computation (octopus, cuttlefish).'),
    ('oct-eye-arm', 'From the eye to an arm', ['oct-eye', 'oct-ol', 'oct-basal', 'oct-arm-ns'],
     'The optic lobe receives retinal input and exchanges fibres with the basal lobes, the higher motor centres, whose stimulation evokes movements without a body map; octopuses use vision to guide a single arm to a goal (octopus).'),
]:
    assert cid not in C
    for a, b in zip(nodes, nodes[1:]):
        assert f'{a}>{b}' in L, (cid, a, b)
    kb['chains'].append({'id': cid, 'name': name, 'nodes': nodes, 'desc': desc})

# ------------------------------------------------------------------ questions
Q = {q['id'] for q in kb['questions']}
for q in [
    {'id': 'q-oct-vl-convergence', 'title': 'How far did the vertical lobe converge on the hippocampus and the cerebellum?',
     'text': 'JZ Young likened the vertical lobe to the hippocampus, the cerebellum and the insect mushroom body (shomrat2015). Its input synapses show hippocampal-like LTP (hochner2003, sternmentch2022), and its cells resemble Drosophila Kenyon cells molecularly (styfhals2022). Yet octopus and cuttlefish place their plasticity at different layers while performing the same computation (shomrat2011), and its complex amacrine cells form part of a circuit the authors call unique (bidel2023). Which features does associative learning itself require, and which are accidents of each lineage?',
     'entities': ['oct-vl', 'oct-vl-am', 'f-consolidation'], 'refs': ['shomrat2015', 'hochner2003', 'sternmentch2022', 'styfhals2022', 'shomrat2011', 'bidel2023'],
     'approaches': ['Compare how sparsely single input axons drive simple amacrine cells with how mossy fibres drive cerebellar granule cells and perforant-path axons drive dentate granule cells.',
                    'Silence complex amacrine cells and test whether vertical lobe output loses stimulus specificity, as balancing inhibition predicts.',
                    'Locate the plastic synapses in the vertical lobes of other cephalopods, such as squid, to see how often the site changes.']},
    {'id': 'q-oct-arm-map', 'title': 'How does a brain without a body map steer one arm?',
     'text': 'Stimulating the basal lobes evokes movements without any site moving a single arm (zullo2009), and the higher motor centres work without body-part maps (hochner2023), yet octopuses guide a single arm to a visual goal (gutnick2011) and learn from one arm’s motion and touch (gutnick2020). The arms carry their own motor programs (sumbre2001), and nerve cords link arms outside the brain (kuuspalu2022). Where is the choice of arm made, and how does the command reach the right arm?',
     'entities': ['oct-basal', 'oct-arm-ns', 'oct-brain'], 'refs': ['zullo2009', 'hochner2023', 'gutnick2011', 'gutnick2020', 'sumbre2001', 'kuuspalu2022'],
     'approaches': ['Record basal lobe neurons while an octopus reaches with one arm in a single-arm maze, and test whether activity predicts which arm is used.',
                    'Cut the nerve cords that link arms near the arm bases and test whether single-arm choices or multi-arm coordination change.',
                    'Stimulate the cerebrobrachial tract of one arm while recording from the others to compare central and peripheral routes.']},
    {'id': 'q-oct-sleep', 'title': 'What does active sleep do for octopus memory?',
     'text': 'Active sleep bouts recur through quiet sleep in a cycle (medeiros2021). During them the superior frontal and vertical lobes, linked to learning and memory, show wake-like activity, and in quiet sleep they generate oscillations resembling sleep spindles (pophale2023). The vertical lobe acquires long-term memory through LTP (shomrat2008). Does active sleep replay or consolidate what the vertical lobe learned that day?',
     'entities': ['oct-vl', 'oct-sfl', 'f-sleep'], 'refs': ['medeiros2021', 'pophale2023', 'shomrat2008'],
     'approaches': ['Prevent active sleep after a learning session and test recall the next day.',
                    'Record the vertical lobe during learning and look for the same activity patterns in the following active sleep.',
                    'Tetanize the vertical lobe pathway and test whether active sleep bouts change in number or length.']},
    {'id': 'q-oct-optic-gland', 'title': 'Which optic gland signal ends an octopus mother’s life?',
     'text': 'Removing the optic glands abolishes maternal brooding and reverses the decline toward death (wangzy2018, wang2022). After mating the glands raise pregnane steroids, 7-dehydrocholesterol and bile acid intermediates and shift catecholamine, insulin and feeding-peptide pathways (wang2022, wangzy2018), and optic gland chemistry extends into neighbouring lobes of the peduncle complex (wangzy2024). Which of these signals drives fasting, self-injury and death, and what tells the gland that mating has happened?',
     'entities': ['oct-optic-gland', 'f-reproduction', 'oct-olf-lobe'], 'refs': ['wangzy2018', 'wang2022', 'wangzy2024'],
     'approaches': ['Block each steroid pathway in brooding females and score fasting, self-injury and survival.',
                    'Give 7-dehydrocholesterol or bile acid intermediates to females without optic glands and test whether the decline returns.',
                    'Trace which brain lobes signal to the optic gland around mating.']},
]:
    assert q['id'] not in Q
    for r in q['refs']:
        assert r in PK and r in q['text'], (q['id'], r)
    kb['questions'].append(q)

# ------------------------------------------------------------------ 3D
A3 = kb['atlas3d']
assert 'octopus' not in A3['species']
A3['species'].append('octopus')
A3['aliases']['octopus'] = {'oct-vl-am': 'oct-vl', 'oct-vl-ln': 'oct-vl'}
for i in ['oct-eye', 'oct-ol', 'oct-peduncle', 'oct-olf-lobe', 'oct-optic-gland']:
    assert i not in A3['sides']['L']
    A3['sides']['L'].append(i)
A3['composite']['oct-brain'] = ['oct-vl', 'oct-sfl', 'oct-subvertical', 'oct-basal', 'oct-brachial']
for c in [
    {'id': 'oct-memory', 'region': 'octopus', 'name': 'Vision to the vertical lobe',
     'desc': 'Retinal photoreceptors project to the optic lobe, whose fibres reach the superior frontal lobe (HRP tracing); the median superior frontal lobe sends the glutamatergic input of the vertical lobe, the learning and memory centre (octopus).',
     'links': ['oct-eye>oct-ol', 'oct-ol>oct-sfl', 'oct-sfl>oct-vl'], 'view': 'octopus'},
    {'id': 'oct-fan', 'region': 'octopus', 'name': 'Inside the vertical lobe',
     'desc': 'Input axons from the median superior frontal lobe fan out onto millions of amacrine interneurons, which converge onto the large output neurons (fan-out fan-in); all three are shown in the vertical lobe (octopus).',
     'links': ['oct-sfl>oct-vl-am', 'oct-vl-am>oct-vl-ln', 'oct-subvertical>oct-vl'], 'view': 'oct-vl'},
    {'id': 'oct-visual', 'region': 'octopus', 'name': 'Optic lobe connections',
     'desc': 'The optic lobe receives the retina and input from the basal, subvertical and brachial lobes, and sends fibres to the superior frontal and lateral basal lobes (HRP tracing, octopus).',
     'links': ['oct-eye>oct-ol', 'oct-basal>oct-ol', 'oct-subvertical>oct-ol', 'oct-brachial>oct-ol', 'oct-ol>oct-sfl', 'oct-ol>oct-basal'], 'view': 'octopus'},
    {'id': 'oct-arms', 'region': 'octopus', 'name': 'Brain and arms',
     'desc': 'The basal lobes command movements without a body map, motor axons run along the cerebrobrachial tracts, the brain learns from one arm’s motion and touch, vision guides an arm, and each sucker’s ganglion feeds the arm’s nerve cord (octopus).',
     'links': ['oct-basal>oct-arm-ns', 'oct-brain>oct-arm-ns', 'oct-arm-ns>oct-brain', 'oct-eye>oct-arm-ns', 'oct-sucker>oct-arm-ns'], 'view': 'oct-arms'},
]:
    for lid in c['links']:
        assert lid in L, lid
    A3['circuits'].append(c)

KP.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
PP.write_text(json.dumps(papers, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(f'added {len(new_papers)} papers, region octopus, 18 entities (2 shared functions), {len(LINKS)} links, 3 chains, 4 questions, 4 circuits')
