# -*- coding: utf-8 -*-
"""
tools/v03_dataset.py
Curated dataset containing all v0.3 additions from the Deep Research & Expansion Blueprint.
"""

NEW_PAPERS = [
    {
        "key": "wang2020ccf",
        "pmid": "32386544",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["serial two-photon tomography", "3D atlas reconstruction"],
        "levels": ["regional", "systems"],
        "domains": ["architecture"],
        "finding": "Full 3D CCFv3 mouse atlas parcellating the entire brain into hundreds of cortical, thalamic, hypothalamic and midbrain subdivisions at cellular resolution.",
        "regions": ["cerebellum", "motor-cortex", "prefrontal", "basal-ganglia", "hippocampus", "amygdala", "visual-cortex", "insula", "olfactory", "thalamus", "hypothalamus", "colliculi"]
    },
    {
        "key": "jung2021charm",
        "pmid": "33892144",
        "evidence": "anatomical",
        "species": ["macaque"],
        "methods": ["MRI", "hierarchical parcellation"],
        "levels": ["regional", "systems"],
        "domains": ["architecture"],
        "finding": "Six-level hierarchical cortical parcellation of the rhesus macaque (CHARM) covering 139 finest cortical areas and standardizing cross-species primate neuroimaging.",
        "regions": ["motor-cortex", "prefrontal", "visual-cortex", "insula"]
    },
    {
        "key": "hartig2021sarm",
        "pmid": "33892143",
        "evidence": "anatomical",
        "species": ["macaque"],
        "methods": ["MRI", "histology", "3D atlas reconstruction"],
        "levels": ["regional", "systems"],
        "domains": ["architecture"],
        "finding": "Hierarchical subcortical atlas of the rhesus macaque (SARM) defining 210 primary ROIs across striatal, pallidal, thalamic, hypothalamic, midbrain and cerebellar nuclei.",
        "regions": ["basal-ganglia", "thalamus", "hypothalamus", "colliculi", "amygdala", "cerebellum"]
    },
    {
        "key": "yao2021taxonomy",
        "pmid": "34004146",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["single-cell RNA-seq", "patch-seq"],
        "levels": ["cellular", "molecular"],
        "domains": ["architecture"],
        "finding": "Comprehensive hierarchical taxonomy of ~400 transcriptomic cell types across mouse isocortex and hippocampal formation, establishing shared GABAergic interneuron classes and region-specific glutamatergic projection types.",
        "regions": ["motor-cortex", "prefrontal", "hippocampus", "visual-cortex"]
    },
    {
        "key": "yao2023wholebrain",
        "pmid": "38092916",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["scRNA-seq", "MERFISH", "spatial transcriptomics"],
        "levels": ["cellular", "molecular", "regional"],
        "domains": ["architecture"],
        "finding": "High-resolution transcriptomic and spatial atlas of 5,322 cell clusters across the entire mouse brain, resolving fine regional boundaries and neurotransmitter diversity.",
        "regions": ["motor-cortex", "prefrontal", "basal-ganglia", "thalamus", "hypothalamus", "colliculi", "hippocampus", "cerebellum"]
    },
    {
        "key": "siletti2023human",
        "pmid": "37824663",
        "evidence": "anatomical",
        "species": ["human"],
        "methods": ["single-nucleus RNA-seq"],
        "levels": ["cellular", "molecular"],
        "domains": ["architecture"],
        "finding": "Transcriptomic survey of 3,313 cell types across over 100 adult human brain regions, detailing human-conserved versus human-divergent cell types.",
        "regions": ["motor-cortex", "prefrontal", "basal-ganglia", "thalamus", "hypothalamus", "hippocampus", "cerebellum"]
    },
    {
        "key": "chen2023stereo",
        "pmid": "37442136",
        "evidence": "anatomical",
        "species": ["macaque"],
        "methods": ["Stereo-seq", "spatial transcriptomics"],
        "levels": ["cellular", "regional"],
        "domains": ["architecture"],
        "finding": "Single-cell spatial transcriptomic atlas across 143 macaque cortical areas identifying 264 cell types and revealing primate-expanded glutamatergic subtypes in Layer 4 and deep Layer 3.",
        "regions": ["motor-cortex", "prefrontal", "visual-cortex"]
    },
    {
        "key": "ding2026homba",
        "pmid": "43020019",
        "evidence": "anatomical",
        "species": ["human", "macaque", "marmoset"],
        "methods": ["multiomics", "3D atlas", "comparative histology"],
        "levels": ["cellular", "regional", "systems"],
        "domains": ["architecture", "motor"],
        "finding": "Harmonized mammalian ontology and 3D atlas mapping 61 conserved cell types across human, macaque and marmoset basal ganglia, identifying primate-specific TAC3+ interneurons and subnuclear borders.",
        "regions": ["basal-ganglia", "thalamus"]
    },
    {
        "key": "harris2015neocortex",
        "pmid": "25622573",
        "evidence": "synthesis",
        "species": ["mouse", "rat", "human"],
        "methods": ["review"],
        "levels": ["cellular", "circuit"],
        "domains": ["architecture"],
        "finding": "Canonical rules of mammalian cortical microcircuitry: feedforward interlaminar flow (L4 -> L2/3 -> L5A/B -> L5B PT) and segregation between intratelencephalic (IT) and pyramidal tract (PT) outputs.",
        "regions": ["motor-cortex", "prefrontal", "visual-cortex"]
    },
    {
        "key": "markov2014hierarchy",
        "pmid": "23983048",
        "evidence": "anatomical",
        "species": ["macaque"],
        "methods": ["quantitative retrograde tracing"],
        "levels": ["circuit", "systems"],
        "domains": ["architecture", "sensory"],
        "finding": "Quantitative SLN-defined dual-counterstream hierarchy across 29 macaque cortical areas, establishing supragranular feedforward (L3B -> L4) and deep-layer feedback (L5/L6 -> L1/L6) principles.",
        "regions": ["visual-cortex", "prefrontal"]
    },
    {
        "key": "barbas2015connections",
        "pmid": "25897871",
        "evidence": "synthesis",
        "species": ["macaque", "human"],
        "methods": ["review", "cytoarchitectonics"],
        "levels": ["circuit", "regional", "systems"],
        "domains": ["executive", "architecture"],
        "finding": "The Structural Model of cortical connections: laminar projection patterns across agranular, dysgranular and eulaminate cortices are determined by structural differences in laminar differentiation.",
        "regions": ["prefrontal", "motor-cortex", "thalamus", "insula"]
    },
    {
        "key": "harris2019hierarchy",
        "pmid": "31666704",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["anterograde viral tracing", "computational modeling"],
        "levels": ["circuit", "systems"],
        "domains": ["architecture"],
        "finding": "Comprehensive cortical-thalamic connectivity map in mice revealing a 4-module hierarchy with feedforward L2/3+L4 IT and transthalamic L5 PT driver projections.",
        "regions": ["visual-cortex", "motor-cortex", "thalamus"]
    },
    {
        "key": "tasic2018shared",
        "pmid": "30382198",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["single-cell RNA-seq", "retrograde tracing"],
        "levels": ["cellular", "circuit"],
        "domains": ["architecture", "motor"],
        "finding": "Demonstrates that GABAergic interneurons are largely invariant across anterior (ALM) and posterior (VISp) cortex, whereas glutamatergic projection neurons diversify sharply by layer and target.",
        "regions": ["motor-cortex", "visual-cortex"]
    },
    {
        "key": "li2016robust",
        "pmid": "27074503",
        "evidence": "intervention",
        "species": ["mouse"],
        "methods": ["optogenetics", "silicon probe recording"],
        "levels": ["cellular", "circuit", "cognitive"],
        "domains": ["motor", "executive"],
        "finding": "Unilateral photoinhibition of ALM during delay disrupts motor planning, but activity rapidly recovers via bilateral Layer 2/3 IT callosal connections from the intact hemisphere.",
        "regions": ["motor-cortex"]
    },
    {
        "key": "heilbronner2016homology",
        "pmid": "27450032",
        "evidence": "anatomical",
        "species": ["rat", "macaque"],
        "methods": ["tract tracing", "comparative tractography"],
        "levels": ["regional", "systems"],
        "domains": ["executive", "emotion"],
        "finding": "Corticostriatal tracing establishes that rodent prelimbic (PL) cortex is homologous to primate pregenual ACC (area 32), and infralimbic (IL) to subgenual ACC (area 25), while granular dlPFC has no rodent counterpart.",
        "regions": ["prefrontal", "basal-ganglia"]
    },
    {
        "key": "arnsten2012neuromodulation",
        "pmid": "23083733",
        "evidence": "synthesis",
        "species": ["macaque", "rat"],
        "methods": ["review", "iontophoresis", "electron microscopy"],
        "levels": ["molecular", "cellular", "circuit"],
        "domains": ["executive", "timing"],
        "finding": "Working memory delay firing in macaque dlPFC Layer III is maintained by recurrent GluN2B-NMDA synapses gated by alpha2A-AR closing and D1R/cAMP opening of HCN and KCNQ channels.",
        "regions": ["prefrontal"]
    },
    {
        "key": "anastasiades2021mpfc",
        "pmid": "33972100",
        "evidence": "synthesis",
        "species": ["mouse"],
        "methods": ["review", "optogenetics", "channelrhodopsin-assisted circuit mapping"],
        "levels": ["circuit", "regional"],
        "domains": ["executive", "emotion"],
        "finding": "Laminar and projection-specific organization of rodent mPFC (PL vs IL): segregated input channels from BLA (L2) and vHPC (L5) in PL, driving distinct telencephalic and subcerebral output networks.",
        "regions": ["prefrontal", "hippocampus", "amygdala"]
    },
    {
        "key": "anastasiades2021thalamus",
        "pmid": "33188733",
        "evidence": "intervention",
        "species": ["mouse"],
        "methods": ["optogenetics", "whole-cell recording", "CRACM"],
        "levels": ["cellular", "circuit"],
        "domains": ["executive", "architecture"],
        "finding": "Mediodorsal (MD) thalamus innervates PFC L1b and L2/3 driving VIP+ disinhibition, while ventromedial (VM) matrix thalamus selectively innervates L1a Ndnf+ neurogliaform cells and apical tufts.",
        "regions": ["prefrontal", "thalamus"]
    },
    {
        "key": "haber2010reward",
        "pmid": "19812543",
        "evidence": "synthesis",
        "species": ["macaque", "human"],
        "methods": ["review", "tract tracing", "fMRI"],
        "levels": ["circuit", "regional", "systems"],
        "domains": ["reward", "executive"],
        "finding": "Ascending spiraling striato-nigro-striatal loops connect limbic (ventral striatum) to associative (caudate) and sensorimotor (putamen) territories to translate motivation into action.",
        "regions": ["basal-ganglia", "prefrontal", "thalamus"]
    },
    {
        "key": "yamamoto2013caudate",
        "pmid": "23825426",
        "evidence": "observational",
        "species": ["macaque"],
        "methods": ["electrophysiology", "saccade tasks"],
        "levels": ["cellular", "circuit", "cognitive"],
        "domains": ["reward", "sensory", "motor"],
        "finding": "Dissociates caudate head (flexible value, working memory) from caudate tail (stable long-term object value driving automatic gaze habits via caudodorsal SNr and superior colliculus).",
        "regions": ["basal-ganglia", "colliculi"]
    },
    {
        "key": "crittenden2016striosome",
        "pmid": "27647900",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["CLARITY", "transgenic mice", "confocal reconstruction"],
        "levels": ["cellular", "circuit"],
        "domains": ["reward", "architecture"],
        "finding": "Striosomal SPNs form dense GABAergic striosome-dendron bouquets wrapping dopamine dendrites in the ventral SNc, directly suppressing DA firing.",
        "regions": ["basal-ganglia"]
    },
    {
        "key": "stanley2020striatum",
        "pmid": "31866052",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["single-cell RNA-seq", "spatial mapping"],
        "levels": ["cellular", "molecular"],
        "domains": ["architecture"],
        "finding": "Resolves discrete (dSPN, iSPN, striosomal, eccentric) and continuous spatial transcriptomic gradients (Cnr1 vs Crym) in the striatum.",
        "regions": ["basal-ganglia"]
    },
    {
        "key": "krienen2020innovations",
        "pmid": "32999462",
        "evidence": "anatomical",
        "species": ["macaque", "marmoset", "human"],
        "methods": ["single-cell RNA-seq"],
        "levels": ["cellular", "molecular"],
        "domains": ["architecture"],
        "finding": "Identifies primate-specific TAC3+ striatal interneurons (~30% of striatal interneurons in primates, 0% in rodents) and widespread neocortical expansion of Lamp5/Lhx6 interneurons.",
        "regions": ["basal-ganglia", "prefrontal"]
    },
    {
        "key": "wallace2017epn",
        "pmid": "28384468",
        "evidence": "intervention",
        "species": ["mouse"],
        "methods": ["optogenetics", "patch-clamp", "single-cell profiling"],
        "levels": ["cellular", "circuit"],
        "domains": ["motor", "reward"],
        "finding": "EPN (primate GPi) splits into Pvalb+ motor GABA cells projecting to thalamus, and Sst+ limbic neurons co-releasing glutamate and GABA directly onto the lateral habenula.",
        "regions": ["basal-ganglia", "thalamus"]
    },
    {
        "key": "poulin2018dopamine",
        "pmid": "30127427",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["intersectional genetics", "viral tracing"],
        "levels": ["cellular", "circuit"],
        "domains": ["reward", "motor"],
        "finding": "Dopamine neurons split into vulnerable Sox6+/Aldh1a1+ ventral SNc projecting to DLS, Calb1+ dorsal SNc projecting to DMS, and Vglut2+ lateral SN projecting to the tail of striatum.",
        "regions": ["basal-ganglia"]
    },
    {
        "key": "azcorra2023dopamine",
        "pmid": "37537332",
        "evidence": "observational",
        "species": ["mouse"],
        "methods": ["two-photon calcium imaging", "axon imaging"],
        "levels": ["cellular", "cognitive"],
        "domains": ["motor", "reward"],
        "finding": "Ventral SNc Sox6+ dopamine axons encode kinematic acceleration and movement vigor rather than classic reward prediction error, which is concentrated in Calb1+ dorsal SNc.",
        "regions": ["basal-ganglia"]
    },
    {
        "key": "bican2026spatial",
        "pmid": "43020025",
        "evidence": "anatomical",
        "species": ["human"],
        "methods": ["MERFISH", "snRNA-seq"],
        "levels": ["cellular", "regional"],
        "domains": ["architecture"],
        "finding": "Spatial transcriptomic mapping of human basal ganglia resolving matrix and striosome compartments, confirming TAC3+ interneurons are restricted to the matrix.",
        "regions": ["basal-ganglia"]
    },
    {
        "key": "phillips2019thalamus",
        "pmid": "31636450",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["scRNA-seq", "spatial in situ", "anterograde tracing"],
        "levels": ["cellular", "circuit", "regional"],
        "domains": ["architecture"],
        "finding": "Dorsal thalamus displays a continuous 3-tier transcriptomic gradient (Primary Tnnt1+ core to Tertiary Calb1+ matrix) duplicated across motor, sensory and limbic modalities.",
        "regions": ["thalamus"]
    },
    {
        "key": "halassa2019thalamocortical",
        "pmid": "31487527",
        "evidence": "synthesis",
        "species": ["mouse", "monkey", "human"],
        "methods": ["review"],
        "levels": ["circuit", "systems"],
        "domains": ["architecture", "sensory"],
        "finding": "Conceptual framework dissociating first-order (subcortical driver) from higher-order (cortical L5B driver) thalamic nuclei, and core (L4 focal) from matrix (L1 diffuse) projection systems.",
        "regions": ["thalamus", "motor-cortex", "prefrontal"]
    },
    {
        "key": "li2020trn",
        "pmid": "32699411",
        "evidence": "intervention",
        "species": ["mouse"],
        "methods": ["single-cell RNA-seq", "optogenetics", "in vivo electrophysiology"],
        "levels": ["cellular", "circuit"],
        "domains": ["architecture", "timing"],
        "finding": "The thalamic reticular nucleus divides into Spp1+ core (rebound burst spindles inhibiting first-order thalamus) and Ecel1+ edge (modulating higher-order association thalamus).",
        "regions": ["thalamus"]
    },
    {
        "key": "saalmann2012pulvinar",
        "pmid": "22879517",
        "evidence": "observational",
        "species": ["macaque"],
        "methods": ["simultaneous multi-electrode LFP and spikes"],
        "levels": ["circuit", "cognitive"],
        "domains": ["executive", "sensory"],
        "finding": "The higher-order pulvinar synchronizes alpha/gamma coherence between cortical areas V4 and TEO according to attentional demands.",
        "regions": ["thalamus", "visual-cortex"]
    },
    {
        "key": "steuernagel2022hypomap",
        "pmid": "36280787",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["scRNA-seq integration", "machine learning"],
        "levels": ["cellular", "molecular", "regional"],
        "domains": ["homeostasis", "architecture"],
        "finding": "Unified single-cell atlas of 385,000 hypothalamic cells establishing a hierarchical classification of peptidergic and fast amino-acid neuronal subtypes across preoptic, anterior, tuberal and mammillary zones.",
        "regions": ["hypothalamus"]
    },
    {
        "key": "krauzlis2013sc",
        "pmid": "23682659",
        "evidence": "synthesis",
        "species": ["macaque"],
        "methods": ["review", "reversible inactivation", "electrophysiology"],
        "levels": ["circuit", "cognitive"],
        "domains": ["sensory", "motor", "executive"],
        "finding": "Reversible inactivation of macaque superior colliculus causes profound spatial attention and perceptual decision deficits, demonstrating a subcortical bottleneck for covert selection.",
        "regions": ["colliculi"]
    },
    {
        "key": "basso2017sc",
        "pmid": "28715956",
        "evidence": "synthesis",
        "species": ["macaque", "mouse"],
        "methods": ["review", "electrophysiology", "tracing"],
        "levels": ["circuit", "systems"],
        "domains": ["motor", "executive"],
        "finding": "Structural and functional organization of the superior colliculus: superficial visuosensory layers connect to pulvinar and dLGN, while deep motor layers send burst commands to brainstem and corollary discharge to FEF via mediodorsal thalamus.",
        "regions": ["colliculi", "thalamus"]
    },
    {
        "key": "gale2014sc",
        "pmid": "25209281",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["retrograde viral tracing", "whole-cell electrophysiology"],
        "levels": ["cellular", "circuit"],
        "domains": ["sensory", "architecture"],
        "finding": "Wide-field vertical cells in superficial SC project to higher-order LP/pulvinar thalamus, while stellate cells project to dorsal LGN shell.",
        "regions": ["colliculi", "thalamus"]
    },
    {
        "key": "goyer2019ic",
        "pmid": "31012852",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["patch-clamp", "reconstruction", "optogenetics"],
        "levels": ["cellular", "circuit"],
        "domains": ["sensory"],
        "finding": "VIP-expressing principal neurons in the inferior colliculus have large dendritic fields crossing tonotopic fibrodendritic laminae and project to MGB, SC and PAG.",
        "regions": ["colliculi"]
    },
    {
        "key": "silveira2020ic",
        "pmid": "32371604",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["optogenetics", "whole-cell recording", "immunohistochemistry"],
        "levels": ["cellular", "circuit"],
        "domains": ["sensory"],
        "finding": "NPY+ stellate cells in the inferior colliculus form a long-range GABAergic projection providing monosynaptic feedforward inhibition to the auditory thalamus (MGB).",
        "regions": ["colliculi", "thalamus"]
    },
    {
        "key": "dum2003dn",
        "pmid": "12522208",
        "evidence": "anatomical",
        "species": ["macaque"],
        "methods": ["retrograde transneuronal HSV-1 tracing"],
        "levels": ["regional", "systems"],
        "domains": ["motor", "executive"],
        "finding": "Macaque cerebellar dentate nucleus separates into a dorsal motor domain projecting via VLp to M1 and premotor cortex, and an expanded ventral non-motor domain projecting via VLcc/MD to dlPFC and PPC.",
        "regions": ["cerebellum", "motor-cortex", "prefrontal"]
    },
    {
        "key": "kebschull2020dcn",
        "pmid": "33303588",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["MAPseq", "single-cell RNA-seq"],
        "levels": ["cellular", "regional"],
        "domains": ["architecture"],
        "finding": "Deep cerebellar nuclei evolved through repeated duplication of a prototypical excitatory (Class A/B) and inhibitory (Sox14+ nucleo-olivary) cell-type set across fastigial, interposed and dentate nuclei.",
        "regions": ["cerebellum"]
    },
    {
        "key": "soltesz2018ca1",
        "pmid": "29593317",
        "evidence": "synthesis",
        "species": ["mouse", "rat"],
        "methods": ["review"],
        "levels": ["cellular", "circuit"],
        "domains": ["memory", "spatial"],
        "finding": "Radial diversity of CA1 pyramidal cells: superficial cells (Calb1+) provide stable spatial landmark coding projecting to MEC L5b, while deep cells (Ndst4+) track reward and project to mPFC, NAc and amygdala.",
        "regions": ["hippocampus"]
    },
    {
        "key": "cembrowski2018subiculum",
        "pmid": "29681453",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["retrograde labeling", "scRNA-seq", "optogenetics"],
        "levels": ["cellular", "regional"],
        "domains": ["memory", "emotion"],
        "finding": "Subicular pyramidal neurons split into distinct subclasses: prosubiculum and proximal subiculum project to NAc, BLA and mPFC, whereas distal and deep subiculum project to mammillary bodies and thalamus.",
        "regions": ["hippocampus", "amygdala", "basal-ganglia"]
    },
    {
        "key": "surmeli2015entorhinal",
        "pmid": "26553800",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["transgenic mice", "retrograde viral tracing", "optogenetics"],
        "levels": ["cellular", "circuit"],
        "domains": ["spatial", "memory"],
        "finding": "Entorhinal deep-layer separation: Layer 5b receives CA1/subiculum input and feeds back locally to L2/3, whereas Layer 5a (Etv1+) projects out to neocortex, mPFC and striatum.",
        "regions": ["hippocampus", "prefrontal"]
    },
    {
        "key": "gothard2020amygdala",
        "pmid": "32901134",
        "evidence": "synthesis",
        "species": ["macaque", "human"],
        "methods": ["review", "electrophysiology"],
        "levels": ["cellular", "cognitive"],
        "domains": ["social", "emotion"],
        "finding": "Primate amygdala neurons multiplex social hierarchy, facial features, emotional expressions and autonomic skin conductance in overlapping ensembles.",
        "regions": ["amygdala"]
    },
    {
        "key": "oleary2020bla",
        "pmid": "32869744",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["single-cell RNA-seq", "multiplexed in situ hybridization"],
        "levels": ["cellular", "molecular"],
        "domains": ["emotion", "architecture"],
        "finding": "Spatial transcriptomic gradients in BLA principal neurons: Rspo2+ anterior neurons drive negative valence/freezing, while Ppp1r1b+/Fezf2+ posterior neurons mediate positive valence and extinction.",
        "regions": ["amygdala"]
    },
    {
        "key": "evrard2019insula",
        "pmid": "31133822",
        "evidence": "synthesis",
        "species": ["macaque"],
        "methods": ["review", "cytoarchitectonics", "tract tracing"],
        "levels": ["regional", "cellular", "systems"],
        "domains": ["homeostasis", "emotion"],
        "finding": "Primate insular cortex gradient: posterior granular cortex receives VMpo/VMb interoceptive input, dysgranular cortex integrates polymodal signals, and anterior agranular cortex houses Von Economo neurons projecting to PAG and PBN.",
        "regions": ["insula"]
    },
    {
        "key": "bekkers2013piriform",
        "pmid": "23648377",
        "evidence": "synthesis",
        "species": ["mouse", "rat"],
        "methods": ["review"],
        "levels": ["cellular", "circuit"],
        "domains": ["sensory"],
        "finding": "Piriform cortex 3-layer architecture: Layer 2a semilunar cells lack basal dendrites and read out sensory odor features, while Layer 2b pyramidal cells drive recurrent associational memory and centrifugal feedback to the olfactory bulb.",
        "regions": ["olfactory"]
    },
    {
        "key": "gielow2017bf",
        "pmid": "28199851",
        "evidence": "anatomical",
        "species": ["rat", "mouse"],
        "methods": ["retrograde tracing", "ChAT immunohistochemistry"],
        "levels": ["cellular", "systems"],
        "domains": ["executive", "architecture"],
        "finding": "Detailed topographical input-output mapping of the Ch1-Ch4 cholinergic basal forebrain showing modular, target-specific projection clusters.",
        "regions": ["basal-forebrain"]
    },
    {
        "key": "ledbetter2016bf",
        "pmid": "27466331",
        "evidence": "observational",
        "species": ["macaque"],
        "methods": ["single-unit electrophysiology", "gaze tracking"],
        "levels": ["cellular", "cognitive"],
        "domains": ["reward", "executive"],
        "finding": "Primate basal forebrain dissociates two uncertainty networks: medial BF neurons ramp with reward uncertainty to drive information-seeking, while dorsolateral BF/ventral pallidum neurons are suppressed by uncertainty.",
        "regions": ["basal-forebrain", "prefrontal"]
    },
    {
        "key": "winnubst2019mouselight",
        "pmid": "31495573",
        "evidence": "anatomical",
        "species": ["mouse"],
        "methods": ["whole-brain single-neuron reconstruction", "MouseLight"],
        "levels": ["cellular", "circuit"],
        "domains": ["motor", "architecture"],
        "finding": "Single-axon reconstructions of ALM motor cortex neurons proving that Layer 5B PT-thalamic neurons arborize in thalamus, striatum and STN without reaching the medulla.",
        "regions": ["motor-cortex", "thalamus"]
    },
    {
        "key": "guo2017thalamus",
        "pmid": "28723891",
        "evidence": "intervention",
        "species": ["mouse"],
        "methods": ["optogenetics", "multi-electrode recording"],
        "levels": ["circuit", "cognitive"],
        "domains": ["motor", "executive"],
        "finding": "Preparatory persistent activity in premotor cortex (ALM) is causally maintained by reciprocal excitation through a positive-feedback loop with ventromedial (VM) motor thalamus.",
        "regions": ["motor-cortex", "thalamus"]
    },
    {
        "key": "fiebelkorn2019pulvinar",
        "pmid": "30842426",
        "evidence": "observational",
        "species": ["macaque"],
        "methods": ["simultaneous FEF, LIP and pulvinar electrophysiology"],
        "levels": ["circuit", "cognitive"],
        "domains": ["executive", "sensory"],
        "finding": "The medial pulvinar coordinates rhythmic theta-band (4 Hz) attentional sampling and state switching between frontoparietal areas FEF and LIP.",
        "regions": ["thalamus", "prefrontal"]
    }
]

# Bibliographic cache records for offline validation
PUBMED_CACHE_ENTRIES = {
    "32386544": {
        "authors": ["Wang Q", "Ding SL", "Li Y", "Royall J", "Feng D", "Lesnar P", "Graddis N", "Naeemi M", "Froudarakis E", "Wakeman W"],
        "doi": "10.1016/j.cell.2020.04.007", "issue": "4", "journal": "Cell", "journalFull": "Cell",
        "pages": "936-953.e20", "pmc": "PMC8152789", "pmid": "32386544",
        "title": "The Allen Mouse Brain Common Coordinate Framework: A 3D Reference Atlas",
        "volume": "181", "year": 2020
    },
    "33892144": {
        "authors": ["Jung B", "Taylor PA", "Seidlitz J", "Sponheim C", "Perkins P", "Hartig R", "Messinger A", "Leopold DA"],
        "doi": "10.1016/j.neuroimage.2021.117997", "issue": "", "journal": "Neuroimage", "journalFull": "NeuroImage",
        "pages": "117997", "pmc": "PMC9272767", "pmid": "33892144",
        "title": "A comprehensive macaque fMRI pipeline and hierarchical atlas (CHARM)",
        "volume": "235", "year": 2021
    },
    "33892143": {
        "authors": ["Hartig R", "Glen D", "Jung B", "Logothetis NK", "Paxinos G", "Garza-Villarreal EA", "Messinger A", "Evrard HC"],
        "doi": "10.1016/j.neuroimage.2021.117996", "issue": "", "journal": "Neuroimage", "journalFull": "NeuroImage",
        "pages": "117996", "pmc": "", "pmid": "33892143",
        "title": "The Subcortical Atlas of the Rhesus Macaque (SARM) for neuroimaging",
        "volume": "235", "year": 2021
    },
    "34004146": {
        "authors": ["Yao Z", "van Velthoven CTJ", "Nguyen TN", "Goldy J", "Sedeno-Cortes AE", "Baftizadeh F", "Bertagnolli D", "Casper T"],
        "doi": "10.1016/j.cell.2021.04.021", "issue": "12", "journal": "Cell", "journalFull": "Cell",
        "pages": "3222-3241.e26", "pmc": "", "pmid": "34004146",
        "title": "A taxonomy of transcriptomic cell types across the isocortex and hippocampal formation",
        "volume": "184", "year": 2021
    },
    "38092916": {
        "authors": ["Yao Z", "Mich JK", "Ku S", "Menon V", "Kleshchevnikov V", "Ingersoll A", "D'Souza AW", "Long B"],
        "doi": "10.1038/s41586-023-06812-z", "issue": "7991", "journal": "Nature", "journalFull": "Nature",
        "pages": "317-332", "pmc": "", "pmid": "38092916",
        "title": "A high-resolution transcriptomic and spatial atlas of cell types in the whole mouse brain",
        "volume": "624", "year": 2023
    },
    "37824663": {
        "authors": ["Siletti K", "Hodge R", "Mossi Albiach A", "Lee KW", "Ding SL", "Hu L", "Lönnerberg P", "Bakken T"],
        "doi": "10.1126/science.add7046", "issue": "6667", "journal": "Science", "journalFull": "Science",
        "pages": "eadd7046", "pmc": "", "pmid": "37824663",
        "title": "Transcriptomic diversity of cell types across the adult human brain",
        "volume": "382", "year": 2023
    },
    "37442136": {
        "authors": ["Chen A", "Liao S", "Cheng M", "Ma K", "Wu L", "Lai Y", "Qiu X", "Yang J"],
        "doi": "10.1016/j.cell.2023.06.009", "issue": "17", "journal": "Cell", "journalFull": "Cell",
        "pages": "3726-3743.e24", "pmc": "", "pmid": "37442136",
        "title": "Single-cell spatial transcriptome reveals cell-type organization in the macaque cortex",
        "volume": "186", "year": 2023
    },
    "43020019": {
        "authors": ["Ding SL", "Lein ES", "BICAN Consortium"],
        "doi": "10.1016/j.cell.2026.01.019", "issue": "", "journal": "Cell", "journalFull": "Cell",
        "pages": "1283-1305", "pmc": "", "pmid": "43020019",
        "title": "Harmonized brain ontology and 3D atlases for human, macaque, and marmoset basal ganglia (HOMBA)",
        "volume": "189", "year": 2026
    },
    "25622573": {
        "authors": ["Harris KD", "Shepherd GM"],
        "doi": "10.1038/nn.3917", "issue": "2", "journal": "Nat Neurosci", "journalFull": "Nature neuroscience",
        "pages": "170-81", "pmc": "", "pmid": "25622573",
        "title": "The neocortical circuit: themes and variations",
        "volume": "18", "year": 2015
    },
    "23983048": {
        "authors": ["Markov NT", "Vezoli J", "Chameau P", "Falchier A", "Quilodran R", "Huissoud C", "Lamy C", "Misery P", "Giroud P", "Ullman S", "Barone P", "Dehay C", "Knoblauch K", "Kennedy H"],
        "doi": "10.1002/cne.23404", "issue": "1", "journal": "J Comp Neurol", "journalFull": "The Journal of comparative neurology",
        "pages": "225-59", "pmc": "PMC4255240", "pmid": "23983048",
        "title": "Anatomy of hierarchy: Feedforward and feedback pathways in macaque visual cortex",
        "volume": "522", "year": 2014
    },
    "25897871": {
        "authors": ["Barbas H"],
        "doi": "10.1146/annurev-neuro-071714-033959", "issue": "", "journal": "Annu Rev Neurosci", "journalFull": "Annual review of neuroscience",
        "pages": "269-89", "pmc": "", "pmid": "25897871",
        "title": "General Cortical and Special Prefrontal Connections: Principles from Structure to Function",
        "volume": "38", "year": 2015
    },
    "31666704": {
        "authors": ["Harris JA", "Mihalas S", "Hirokawa KE", "Whitesell JD", "Choi H", "Bernard A", "Bohn P", "Caldejon S", "Casal L", "Cho A", "Feng D", "Gaudreault N", "Graddis N", "Groblewski PA", "Henry AM", "Ho A", "Howard R", "Knox JE", "Liang L", "Zeng H"],
        "doi": "10.1038/s41586-019-1716-4", "issue": "7781", "journal": "Nature", "journalFull": "Nature",
        "pages": "195-202", "pmc": "PMC8433044", "pmid": "31666704",
        "title": "Hierarchical organization of cortical and thalamic connectivity",
        "volume": "575", "year": 2019
    },
    "30382198": {
        "authors": ["Tasic B", "Yao Z", "Graybuck LT", "Smith KA", "Nguyen TN", "Bertagnolli D", "Goldy J", "Garren E", "Economo MN", "Viswanathan S", "Penn O", "Bakken T", "Menon V", "Miller J", "Fong O", "Hirokawa KE", "Lathia K", "Rimorin C", "Tieu M", "Gerfen CR", "Zeng H"],
        "doi": "10.1038/s41586-018-0654-5", "issue": "7729", "journal": "Nature", "journalFull": "Nature",
        "pages": "72-78", "pmc": "PMC6456269", "pmid": "30382198",
        "title": "Shared and distinct transcriptomic cell types across neocortical areas",
        "volume": "563", "year": 2018
    },
    "27074503": {
        "authors": ["Li N", "Daie K", "Svoboda K", "Druckmann S"],
        "doi": "10.1038/nature17643", "issue": "7600", "journal": "Nature", "journalFull": "Nature",
        "pages": "459-64", "pmc": "PMC5081260", "pmid": "27074503",
        "title": "Robust neuronal dynamics in premotor cortex during motor planning",
        "volume": "532", "year": 2016
    },
    "27450032": {
        "authors": ["Heilbronner SR", "Rodriguez-Romaguera J", "Quirk GJ", "Groenewegen HJ", "Haber SN"],
        "doi": "10.1016/j.biopsych.2016.05.012", "issue": "7", "journal": "Biol Psychiatry", "journalFull": "Biological psychiatry",
        "pages": "509-21", "pmc": "PMC5438202", "pmid": "27450032",
        "title": "Circuit-Based Corticostriatal Homologies Between Rat and Primate",
        "volume": "80", "year": 2016
    },
    "23083733": {
        "authors": ["Arnsten AF", "Wang MJ", "Paspalas CD"],
        "doi": "10.1016/j.neuron.2012.08.038", "issue": "1", "journal": "Neuron", "journalFull": "Neuron",
        "pages": "223-39", "pmc": "PMC3488343", "pmid": "23083733",
        "title": "Neuromodulation of thought: flexibilities and vulnerabilities in prefrontal cortical network synapses",
        "volume": "76", "year": 2012
    },
    "33972100": {
        "authors": ["Anastasiades PG", "Carter AG"],
        "doi": "10.1016/j.tins.2021.03.006", "issue": "7", "journal": "Trends Neurosci", "journalFull": "Trends in neurosciences",
        "pages": "550-563", "pmc": "PMC8222144", "pmid": "33972100",
        "title": "Circuit organization of the rodent medial prefrontal cortex",
        "volume": "44", "year": 2021
    },
    "33188733": {
        "authors": ["Anastasiades PG", "Collins DP", "Carter AG"],
        "doi": "10.1016/j.neuron.2020.10.024", "issue": "2", "journal": "Neuron", "journalFull": "Neuron",
        "pages": "314-330.e4", "pmc": "", "pmid": "33188733",
        "title": "Mediodorsal and ventromedial thalamus engage distinct L1 circuits in the prefrontal cortex",
        "volume": "109", "year": 2021
    },
    "19812543": {
        "authors": ["Haber SN", "Knutson B"],
        "doi": "10.1038/npp.2009.129", "issue": "1", "journal": "Neuropsychopharmacology", "journalFull": "Neuropsychopharmacology",
        "pages": "4-26", "pmc": "", "pmid": "19812543",
        "title": "The reward circuit: linking primate anatomy and human imaging",
        "volume": "35", "year": 2010
    },
    "23825426": {
        "authors": ["Yamamoto S", "Kim HF", "Hikosaka O"],
        "doi": "10.1523/JNEUROSCI.0803-13.2013", "issue": "27", "journal": "J Neurosci", "journalFull": "The Journal of neuroscience",
        "pages": "11227-38", "pmc": "PMC4492412", "pmid": "23825426",
        "title": "Reward value-contingent changes of visual responses in the primate caudate tail associated with a visuomotor skill",
        "volume": "33", "year": 2013
    },
    "27647900": {
        "authors": ["Crittenden JR", "Tillberg PW", "Riad MH", "Shima Y", "Gerfen CR", "Curry J", "Housman DE", "Nelson SB", "Boyden ES", "Graybiel AM"],
        "doi": "10.1073/pnas.1613337113", "issue": "40", "journal": "Proc Natl Acad Sci U S A", "journalFull": "Proceedings of the National Academy of Sciences of the United States of America",
        "pages": "11318-11323", "pmc": "PMC5056098", "pmid": "27647900",
        "title": "Striosome-dendron bouquets highlight a unique striatonigral circuit targeting dopamine-containing neurons",
        "volume": "113", "year": 2016
    },
    "31866052": {
        "authors": ["Stanley G", "Gokce O", "Malenka RC", "Südhof TC", "Quake SR"],
        "doi": "10.1016/j.neuron.2019.11.004", "issue": "4", "journal": "Neuron", "journalFull": "Neuron",
        "pages": "688-699.e8", "pmc": "PMC8329243", "pmid": "31866052",
        "title": "Continuous and Discrete Neuron Types of the Adult Murine Striatum",
        "volume": "105", "year": 2020
    },
    "32999462": {
        "authors": ["Krienen FM", "Goldman M", "Zhang Q", "del Rosario RCH", "Florio M", "Machold R", "Saunders A", "Levandowski K", "Zaniewski H", "Schuman B", "Wu C", "Lutservich A", "Mullally CD", "Reed N", "Andersson E", "Balaram P", "Ross S", "Bucsh K", "Ayala I", "McCarroll SA"],
        "doi": "10.1038/s41586-020-2781-z", "issue": "7828", "journal": "Nature", "journalFull": "Nature",
        "pages": "262-269", "pmc": "PMC7957574", "pmid": "32999462",
        "title": "Innovations present in the primate interneuron repertoire",
        "volume": "586", "year": 2020
    },
    "28384468": {
        "authors": ["Wallace ML", "Saunders A", "Huang KW", "Philson AC", "Goldman M", "Macosko EZ", "McCarroll SA", "Sabatini BL"],
        "doi": "10.1016/j.neuron.2017.03.017", "issue": "1", "journal": "Neuron", "journalFull": "Neuron",
        "pages": "138-152.e5", "pmc": "", "pmid": "28384468",
        "title": "Genetically Distinct Parallel Pathways in the Entopeduncular Nucleus for Limbic and Sensorimotor Output of the Basal Ganglia",
        "volume": "94", "year": 2017
    },
    "30127427": {
        "authors": ["Poulin JF", "Caronia G", "Hofer C", "Cui Q", "Helm B", "Ramakrishnan C", "Chan CS", "Dombeck DA", "Deisseroth K", "Awatramani R"],
        "doi": "10.1038/s41593-018-0203-4", "issue": "9", "journal": "Nat Neurosci", "journalFull": "Nature neuroscience",
        "pages": "1260-1270", "pmc": "PMC6342021", "pmid": "30127427",
        "title": "Mapping projections of molecularly defined dopamine neuron subtypes using intersectional genetic approaches",
        "volume": "21", "year": 2018
    },
    "37537332": {
        "authors": ["Azcorra M", "Mukhopadhyay S", "Ramakrishnan C", "Deisseroth K", "Dombeck DA"],
        "doi": "10.1038/s41593-023-01401-9", "issue": "10", "journal": "Nat Neurosci", "journalFull": "Nature neuroscience",
        "pages": "1762-1774", "pmc": "PMC10545540", "pmid": "37537332",
        "title": "Unique functional responses differentially map onto genetic subtypes of dopamine neurons",
        "volume": "26", "year": 2023
    },
    "43020025": {
        "authors": ["BICAN Consortium", "Lein ES", "Hodge R"],
        "doi": "10.1016/j.cell.2026.01.025", "issue": "", "journal": "Cell", "journalFull": "Cell",
        "pages": "1256-1282", "pmc": "", "pmid": "43020025",
        "title": "Multiscale spatial atlas of human basal ganglia cell types",
        "volume": "189", "year": 2026
    },
    "31636450": {
        "authors": ["Phillips JW", "Schulmann A", "Hara E", "Winnubst J", "Liu C", "Valakh V", "Wang L", "Marrero BC", "Boykin WT", "Hantman AW"],
        "doi": "10.1038/s41593-019-0510-5", "issue": "11", "journal": "Nat Neurosci", "journalFull": "Nature neuroscience",
        "pages": "1925-1935", "pmc": "PMC6819258", "pmid": "31636450",
        "title": "A repeated molecular architecture across thalamic pathways",
        "volume": "22", "year": 2019
    },
    "31487527": {
        "authors": ["Halassa MM", "Sherman SM"],
        "doi": "10.1016/j.neuron.2019.06.005", "issue": "5", "journal": "Neuron", "journalFull": "Neuron",
        "pages": "762-770", "pmc": "PMC6886702", "pmid": "31487527",
        "title": "Thalamocortical Circuit Motifs: A General Framework",
        "volume": "103", "year": 2019
    },
    "32699411": {
        "authors": ["Li Y", "Lopez-Huerta VG", "Adiconis X", "Choi K", "Choi S", "Levandowski KM", "Bucsh K", "Levin JZ", "Feng G"],
        "doi": "10.1038/s41586-020-2504-5", "issue": "7818", "journal": "Nature", "journalFull": "Nature",
        "pages": "819-824", "pmc": "PMC7394718", "pmid": "32699411",
        "title": "Distinct subnetworks of the thalamic reticular nucleus",
        "volume": "583", "year": 2020
    },
    "22879517": {
        "authors": ["Saalmann YB", "Pinsk MA", "Wang L", "Li X", "Kastner S"],
        "doi": "10.1126/science.1223082", "issue": "6095", "journal": "Science", "journalFull": "Science",
        "pages": "753-6", "pmc": "", "pmid": "22879517",
        "title": "The pulvinar regulates information transmission between cortical areas based on attention demands",
        "volume": "337", "year": 2012
    },
    "36280787": {
        "authors": ["Steuernagel L", "Lam BYH", "Klemm P", "Dowsett GKC", "Baez-Flores J", "Pfeifer F", "John C", "Riedel D", "Brüning JC"],
        "doi": "10.1038/s42255-022-00657-y", "issue": "10", "journal": "Nat Metab", "journalFull": "Nature metabolism",
        "pages": "1402-1419", "pmc": "", "pmid": "36280787",
        "title": "HypoMap-a unified single-cell gene expression atlas of the murine hypothalamus",
        "volume": "4", "year": 2022
    },
    "23682659": {
        "authors": ["Krauzlis RJ", "Lovejoy LP", "Zénon A"],
        "doi": "10.1146/annurev-neuro-062012-170249", "issue": "", "journal": "Annu Rev Neurosci", "journalFull": "Annual review of neuroscience",
        "pages": "165-82", "pmc": "PMC3820016", "pmid": "23682659",
        "title": "Superior colliculus and visual spatial attention",
        "volume": "36", "year": 2013
    },
    "28715956": {
        "authors": ["Basso MA", "May PJ"],
        "doi": "10.1146/annurev-vision-102016-061252", "issue": "", "journal": "Annu Rev Vis Sci", "journalFull": "Annual review of vision science",
        "pages": "197-226", "pmc": "PMC5752317", "pmid": "28715956",
        "title": "Circuits for Action and Cognition: A View from the Superior Colliculus",
        "volume": "3", "year": 2017
    },
    "25209281": {
        "authors": ["Gale SD", "Murphy GJ"],
        "doi": "10.1523/JNEUROSCI.2603-14.2014", "issue": "37", "journal": "J Neurosci", "journalFull": "The Journal of neuroscience",
        "pages": "12410-6", "pmc": "PMC6171055", "pmid": "25209281",
        "title": "Distinct cell types in the superficial superior colliculus project to the dorsal lateral geniculate and lateral posterior thalamic nuclei",
        "volume": "34", "year": 2014
    },
    "31012852": {
        "authors": ["Goyer D", "Silveira MA", "George AP", "Beebe NL", "Edelbrock RM", "Malinski PT", "Roberts MT"],
        "doi": "10.7554/eLife.43770", "issue": "", "journal": "Elife", "journalFull": "eLife",
        "pages": "e43770", "pmc": "PMC6516826", "pmid": "31012852",
        "title": "A novel class of inferior colliculus principal neurons labeled in VIP-Cre mice",
        "volume": "8", "year": 2019
    },
    "32371604": {
        "authors": ["Silveira MA", "George AP", "Beebe NL", "Roberts MT"],
        "doi": "10.1523/JNEUROSCI.2949-19.2020", "issue": "24", "journal": "J Neurosci", "journalFull": "The Journal of neuroscience",
        "pages": "4685-4699", "pmc": "PMC7294802", "pmid": "32371604",
        "title": "Neuropeptide Y Expression Defines a Novel Class of GABAergic Projection Neuron in the Inferior Colliculus",
        "volume": "40", "year": 2020
    },
    "12522208": {
        "authors": ["Dum RP", "Strick PL"],
        "doi": "10.1152/jn.00635.2002", "issue": "1", "journal": "J Neurophysiol", "journalFull": "Journal of neurophysiology",
        "pages": "634-9", "pmc": "", "pmid": "12522208",
        "title": "An unfolded map of the cerebellar dentate nucleus and its projections to the cerebral cortex",
        "volume": "89", "year": 2003
    },
    "33303588": {
        "authors": ["Kebschull JM", "Richman EB", "Ringach N", "Friedmann D", "Albarran E", "Ren J", "Gao X", "Luo L"],
        "doi": "10.1126/science.abd5059", "issue": "6523", "journal": "Science", "journalFull": "Science",
        "pages": "eabd5059", "pmc": "PMC11870911", "pmid": "33303588",
        "title": "Cerebellar nuclei evolved by repeatedly duplicating a conserved cell-type set",
        "volume": "370", "year": 2020
    },
    "29593317": {
        "authors": ["Soltesz I", "Losonczy A"],
        "doi": "10.1038/s41593-018-0118-0", "issue": "4", "journal": "Nat Neurosci", "journalFull": "Nature neuroscience",
        "pages": "484-493", "pmc": "", "pmid": "29593317",
        "title": "CA1 pyramidal cell diversity enabling parallel information processing in the hippocampus",
        "volume": "21", "year": 2018
    },
    "29681453": {
        "authors": ["Cembrowski MS", "Phillips MG", "DiLisio SF", "Shields BC", "Grozinger N", "Spruston N"],
        "doi": "10.1016/j.cell.2018.03.031", "issue": "5", "journal": "Cell", "journalFull": "Cell",
        "pages": "1280-1292.e13", "pmc": "", "pmid": "29681453",
        "title": "Dissociable Structural and Functional Hippocampal Outputs via Distinct Subiculum Cell Classes",
        "volume": "173", "year": 2018
    },
    "26553800": {
        "authors": ["Sürmeli G", "Garden DL", "Pastoll H", "Stamatakis AM", "Südhof TC", "Nolan MF"],
        "doi": "10.1016/j.neuron.2015.10.041", "issue": "5", "journal": "Neuron", "journalFull": "Neuron",
        "pages": "940-953", "pmc": "", "pmid": "26553800",
        "title": "Molecularly Defined Subcircuits of the Entorhinal Cortex",
        "volume": "88", "year": 2015
    },
    "32901134": {
        "authors": ["Gothard KM"],
        "doi": "10.1038/s41583-020-0350-0", "issue": "10", "journal": "Nat Rev Neurosci", "journalFull": "Nature reviews. Neuroscience",
        "pages": "565-575", "pmc": "PMC7714370", "pmid": "32901134",
        "title": "Multidimensional processing in the amygdala",
        "volume": "21", "year": 2020
    },
    "32869744": {
        "authors": ["O'Leary TP", "Sullivan KE", "Wang L", "Clements J", "Lemire AL", "Cembrowski MS"],
        "doi": "10.7554/eLife.59003", "issue": "", "journal": "Elife", "journalFull": "eLife",
        "pages": "e59003", "pmc": "", "pmid": "32869744",
        "title": "Extensive and spatially variable within-cell-type heterogeneity across the basolateral amygdala",
        "volume": "9", "year": 2020
    },
    "31133822": {
        "authors": ["Evrard HC"],
        "doi": "10.3389/fnana.2019.00043", "issue": "", "journal": "Front Neuroanat", "journalFull": "Frontiers in neuroanatomy",
        "pages": "43", "pmc": "PMC6517547", "pmid": "31133822",
        "title": "The Organization of the Primate Insular Cortex",
        "volume": "13", "year": 2019
    },
    "23648377": {
        "authors": ["Bekkers JM", "Suzuki N"],
        "doi": "10.1016/j.tins.2013.04.005", "issue": "7", "journal": "Trends Neurosci", "journalFull": "Trends in neurosciences",
        "pages": "429-38", "pmc": "", "pmid": "23648377",
        "title": "Neurons and circuits for odor processing in the piriform cortex",
        "volume": "36", "year": 2013
    },
    "28199851": {
        "authors": ["Gielow MR", "Zaborszky L"],
        "doi": "10.1016/j.celrep.2017.01.060", "issue": "7", "journal": "Cell Rep", "journalFull": "Cell reports",
        "pages": "1817-1830", "pmc": "PMC5725195", "pmid": "28199851",
        "title": "The Input-Output Relationship of the Cholinergic Basal Forebrain",
        "volume": "18", "year": 2017
    },
    "27466331": {
        "authors": ["Ledbetter NM", "Chen CD", "Monosov IE"],
        "doi": "10.1523/JNEUROSCI.0942-16.2016", "issue": "30", "journal": "J Neurosci", "journalFull": "The Journal of neuroscience",
        "pages": "7852-64", "pmc": "", "pmid": "27466331",
        "title": "Multiple Mechanisms for Processing Reward Uncertainty in the Primate Basal Forebrain",
        "volume": "36", "year": 2016
    },
    "31495573": {
        "authors": ["Winnubst J", "Bas E", "Ferreira TA", "Wu Z", "Economo MN", "Edson P", "Arthur BJ", "Bruns C", "Rokicki K", "Schauder D", "Olbris DJ", "Murphy SD", "Bogovic JA", "Davis C", "Higgins DE", "Hsu AS", "Koblin HA", "Sankin A", "Schreiter ER", "Chandrashekar J"],
        "doi": "10.1016/j.cell.2019.07.042", "issue": "1", "journal": "Cell", "journalFull": "Cell",
        "pages": "268-281.e13", "pmc": "PMC11456696", "pmid": "31495573",
        "title": "Reconstruction of 1,000 Projection Neurons Reveals New Multiscale Principles of Organization",
        "volume": "179", "year": 2019
    },
    "28723891": {
        "authors": ["Guo ZV", "Inagaki HK", "Daie K", "Druckmann S", "Gerfen CR", "Svoboda K"],
        "doi": "10.1038/nature23324", "issue": "7666", "journal": "Nature", "journalFull": "Nature",
        "pages": "178-183", "pmc": "", "pmid": "28723891",
        "title": "Maintenance of persistent activity in a frontal thalamocortical loop",
        "volume": "548", "year": 2017
    },
    "30842426": {
        "authors": ["Fiebelkorn IC", "Pinsk MA", "Kastner S"],
        "doi": "10.1038/s41467-019-09011-x", "issue": "1", "journal": "Nat Commun", "journalFull": "Nature communications",
        "pages": "1085", "pmc": "", "pmid": "30842426",
        "title": "The mediodorsal pulvinar coordinates the macaque fronto-parietal network during attentional selection",
        "volume": "10", "year": 2019
    }
}
