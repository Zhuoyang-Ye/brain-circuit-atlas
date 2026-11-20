# -*- coding: utf-8 -*-
"""
tools/v03_links.py
Defines the comprehensive v0.3 links and 3D circuits for Brain Circuit Atlas.
Includes laminar connectivity metadata:
src_layer, dst_layer, cell_class, tract, hierarchy_dir
"""

def get_links():
    return [
        # =========================================================================
        # 1. THALAMUS & EPITHALAMUS CIRCUITS (LAMINAR & SUBREGIONAL)
        # =========================================================================
        {
            "s": "thal-va", "t": "premotor",
            "rel": "motor and executive thalamic projection to premotor and pre-SMA",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "VApc/VAmc", "dst_layer": "L4, L3", "cell_class": "Core", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["halassa2019thalamocortical", "hartig2021sarm"]
        },
        {
            "s": "thal-vla", "t": "sma",
            "rel": "GPi-recipient motor thalamic drive to supplementary motor area",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "VLa/VLo", "dst_layer": "L4, L3", "cell_class": "Core", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["halassa2019thalamocortical", "wallace2017epn"]
        },
        {
            "s": "thal-vlp", "t": "m1",
            "rel": "cerebellar-recipient motor thalamic (Vim) excitatory driver to M1",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "VLp (Vim)", "dst_layer": "L4, L3", "cell_class": "Core", "tract": "superior cerebellar peduncle relay", "hierarchy_dir": "feedforward"},
            "refs": ["dum2003dn", "strick2009", "bostan2010"]
        },
        {
            "s": "thal-val", "t": "m1",
            "rel": "rodent/primate motor thalamic complex excitatory projection to M1",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "VAL Core", "dst_layer": "L4, L5B", "cell_class": "Core", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["guo2017thalamus", "economo2018", "wang2020ccf"]
        },
        {
            "s": "m1", "t": "thal-val",
            "rel": "corticothalamic layer 6 feedback to motor thalamus",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L6 CT", "dst_layer": "VAL", "cell_class": "CT", "tract": "corticothalamic", "hierarchy_dir": "feedback"},
            "refs": ["halassa2019thalamocortical", "winnubst2019mouselight"]
        },
        {
            "s": "l5-pt-thal", "t": "thal-vm",
            "rel": "ALM/M1 layer 5B upper PT projection sustaining preparatory activity",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "L5B (upper)", "dst_layer": "VM matrix core", "cell_class": "PT/ET", "tract": "corticothalamic", "hierarchy_dir": "corticofugal"},
            "refs": ["guo2017thalamus", "winnubst2019mouselight"]
        },
        {
            "s": "thal-vm", "t": "l23-it",
            "rel": "Calb1+ matrix thalamocortical projection to outer layer 1a apical tufts",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "VM (Matrix)", "dst_layer": "L1a", "cell_class": "Matrix", "tract": "thalamocortical", "hierarchy_dir": "ascending"},
            "refs": ["guo2017thalamus", "phillips2019thalamus"]
        },
        {
            "s": "thal-md", "t": "dlpfc-9",
            "rel": "mediodorsal thalamic reciprocal projection to area 9 dlPFC",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "MD", "dst_layer": "L3, L1", "cell_class": "Core/Matrix", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["halassa2019thalamocortical", "jung2021charm"]
        },
        {
            "s": "md-mc", "t": "ofc-med",
            "rel": "magnocellular MD projection to medial orbitofrontal cortex",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "MDmc", "dst_layer": "L3, L4", "cell_class": "Core", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["hartig2021sarm", "jung2021charm"]
        },
        {
            "s": "md-pc", "t": "dlpfc-46d",
            "rel": "parvocellular MD projection to area 46d sustaining working memory delay firing",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "MDpc", "dst_layer": "L3", "cell_class": "Core", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["halassa2019thalamocortical", "jung2021charm"]
        },
        {
            "s": "dlpfc-46d", "t": "thal-md",
            "rel": "prefrontal layer 5B driver projection to mediodorsal thalamus",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "L5B", "dst_layer": "MD", "cell_class": "PT/ET", "tract": "corticothalamic", "hierarchy_dir": "corticofugal"},
            "refs": ["halassa2019thalamocortical", "phillips2019thalamus"]
        },
        {
            "s": "pulvinar", "t": "v4",
            "rel": "higher-order pulvinar coordinates attentional synchrony to visual area V4",
            "status": "supported", "kind": "functional",
            "laminar": {"src_layer": "Pulvinar (PL)", "dst_layer": "L4, L1", "cell_class": "HO Matrix", "tract": "thalamocortical", "hierarchy_dir": "transthalamic"},
            "refs": ["saalmann2012pulvinar", "fiebelkorn2019pulvinar"]
        },
        {
            "s": "pulvinar", "t": "mt",
            "rel": "inferior pulvinar extrastriate relay to motion area MT",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "Pulvinar (PI)", "dst_layer": "L4", "cell_class": "HO Core", "tract": "thalamocortical", "hierarchy_dir": "transthalamic"},
            "refs": ["saalmann2012pulvinar", "krauzlis2013sc"]
        },
        {
            "s": "v1", "t": "pulvinar",
            "rel": "primary visual cortex layer 5 driver projection to pulvinar",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L5B", "dst_layer": "Pulvinar", "cell_class": "PT/ET", "tract": "corticothalamic", "hierarchy_dir": "corticofugal"},
            "refs": ["saalmann2012pulvinar", "halassa2019thalamocortical", "markov2014hierarchy"]
        },
        {
            "s": "diagonal-band", "t": "bf-cholinergic",
            "rel": "topographical Ch1-Ch4 cholinergic projection modules to sensory and limbic targets",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "HDB/VDB", "dst_layer": "Neocortex", "cell_class": "ChAT+", "tract": "medial forebrain bundle", "hierarchy_dir": "ascending"},
            "refs": ["gielow2017bf", "ledbetter2016bf"]
        },
        {
            "s": "lp", "t": "v1",
            "rel": "lateral posterior thalamus (rodent pulvinar homologue) matrix drive to visual cortex",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "LP", "dst_layer": "L1, L4", "cell_class": "Matrix", "tract": "thalamocortical", "hierarchy_dir": "modulatory"},
            "refs": ["phillips2019thalamus", "gale2014sc"]
        },
        {
            "s": "vpm", "t": "l4-it",
            "rel": "ventral posteromedial nucleus barreloid lemniscal drive to S1 layer 4 barrels",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "VPM Core", "dst_layer": "L4 barrels", "cell_class": "Core", "tract": "medial lemniscal", "hierarchy_dir": "feedforward"},
            "refs": ["phillips2019thalamus", "wang2020ccf"]
        },
        {
            "s": "vpl", "t": "l4-it",
            "rel": "ventral posterolateral nucleus spinothalamic lemniscal relay to primary somatosensory cortex",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "VPL Core", "dst_layer": "L4", "cell_class": "Core", "tract": "medial lemniscal", "hierarchy_dir": "feedforward"},
            "refs": ["phillips2019thalamus", "wang2020ccf"]
        },
        {
            "s": "pom", "t": "l23-it",
            "rel": "posterolateral nucleus (POm) paralemniscal matrix drive to S1 layer 1 and 5A",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "POm Matrix", "dst_layer": "L1, L5A", "cell_class": "Matrix", "tract": "thalamocortical", "hierarchy_dir": "modulatory"},
            "refs": ["phillips2019thalamus", "halassa2019thalamocortical"]
        },
        {
            "s": "vpmpc", "t": "ins-gran",
            "rel": "parvicellular VPM gustatory/visceral relay to posterior granular insula",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "VPMpc", "dst_layer": "L4", "cell_class": "Core", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["evrard2019insula", "hartig2021sarm"]
        },
        {
            "s": "mgv", "t": "l4-it",
            "rel": "ventral medial geniculate tonotopic core projection to auditory cortex layer 4",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "MGv", "dst_layer": "L4", "cell_class": "Core", "tract": "brachium of IC", "hierarchy_dir": "feedforward"},
            "refs": ["goyer2019ic", "silveira2020ic"]
        },
        {
            "s": "mgd", "t": "l23-it",
            "rel": "dorsal medial geniculate diffuse matrix projection to secondary auditory cortex",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "MGd", "dst_layer": "L1, L2/3", "cell_class": "Matrix", "tract": "thalamocortical", "hierarchy_dir": "modulatory"},
            "refs": ["goyer2019ic", "halassa2019thalamocortical"]
        },
        {
            "s": "mgm", "t": "amygdala",
            "rel": "medial division of MGB non-tonotopic multisensory projection to lateral amygdala",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "MGm", "dst_layer": "BLA/LA", "cell_class": "Matrix", "tract": "thalamoamygdalar", "hierarchy_dir": "feedforward"},
            "refs": ["gothard2020amygdala", "oleary2020bla"]
        },
        {
            "s": "atn", "t": "reuniens",
            "rel": "anterior thalamic complex coordination with midline nucleus reuniens",
            "status": "supported", "kind": "structural",
            "refs": ["wang2020ccf", "cembrowski2018subiculum"]
        },
        {
            "s": "atn-ad", "t": "rsp",
            "rel": "anterodorsal thalamic head-direction relay to retrosplenial cortex",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "AD", "dst_layer": "L3, L4", "cell_class": "Core", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["wang2020ccf", "cembrowski2018subiculum"]
        },
        {
            "s": "atn-av", "t": "prosubiculum",
            "rel": "anteroventral thalamic theta-rhythmic drive to prosubiculum and subiculum",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "AV", "dst_layer": "Pyramidal layer", "cell_class": "Core", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["cembrowski2018subiculum", "wang2020ccf"]
        },
        {
            "s": "pvt", "t": "nac-mshell",
            "rel": "paraventricular thalamic projection to nucleus accumbens medial shell gating arousal and valence",
            "status": "supported", "kind": "mechanistic",
            "refs": ["ding2026homba", "phillips2019thalamus"]
        },
        {
            "s": "reuniens", "t": "ca1-sup-pyr",
            "rel": "midline nucleus reuniens glutamatergic driver to CA1 stratum lacunosum-moleculare",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "RE", "dst_layer": "SLM", "cell_class": "Matrix", "tract": "thalamocortical", "hierarchy_dir": "ascending"},
            "refs": ["soltesz2018ca1", "cembrowski2018subiculum"]
        },
        {
            "s": "thal-cmpf", "t": "cmn",
            "rel": "centromedian-parafascicular complex containing CMn and PF nuclei",
            "status": "established", "kind": "structural",
            "refs": ["hartig2021sarm", "ding2026homba"]
        },
        {
            "s": "cmn", "t": "putamen",
            "rel": "primate PVALB+ centromedian nucleus dense driver to sensorimotor putamen",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "CMn", "dst_layer": "Matrix", "cell_class": "Core-like", "tract": "thalamostriatal", "hierarchy_dir": "feedforward"},
            "refs": ["hartig2021sarm", "ding2026homba"]
        },
        {
            "s": "pf", "t": "caudate",
            "rel": "parafascicular nucleus driving cholinergic interneurons in associative caudate",
            "status": "established", "kind": "mechanistic",
            "laminar": {"src_layer": "PF", "dst_layer": "CINs", "cell_class": "Matrix", "tract": "thalamostriatal", "hierarchy_dir": "modulatory"},
            "refs": ["yamamoto2013caudate", "ding2026homba"]
        },
        {
            "s": "pf", "t": "dms",
            "rel": "mouse parafascicular thalamic drive to dorsomedial striatal cholinergic interneurons",
            "status": "supported", "kind": "mechanistic",
            "refs": ["wang2020ccf", "stanley2020striatum"]
        },
        {
            "s": "trn", "t": "thal-val",
            "rel": "thalamic reticular nucleus topographic GABAergic feedforward inhibition",
            "status": "established", "kind": "structural",
            "refs": ["li2020trn", "halassa2019thalamocortical"]
        },
        {
            "s": "trn-spp1-core", "t": "vpm",
            "rel": "Spp1+ core TRN burst firing driving sleep spindles and sensory gating of first-order thalamus",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "TRN Core (Spp1+)", "dst_layer": "VPM", "cell_class": "GABAergic", "hierarchy_dir": "inhibitory"},
            "refs": ["li2020trn", "halassa2019thalamocortical"]
        },
        {
            "s": "trn-ecel1-edge", "t": "thal-md",
            "rel": "Ecel1+ edge TRN modulating higher-order association thalamus during cognitive switching",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "TRN Edge (Ecel1+)", "dst_layer": "MD", "cell_class": "GABAergic", "hierarchy_dir": "inhibitory"},
            "refs": ["li2020trn", "halassa2019thalamocortical"]
        },
        {
            "s": "zi", "t": "pom",
            "rel": "zona incerta GABAergic gating of higher-order thalamus",
            "status": "supported", "kind": "mechanistic",
            "refs": ["halassa2019thalamocortical", "wang2020ccf"]
        },
        {
            "s": "mhb", "t": "lhb",
            "rel": "medial to lateral habenula communication coordinating negative valence",
            "status": "supported", "kind": "structural",
            "refs": ["wang2020ccf", "wallace2017epn"]
        },
        {
            "s": "lhb", "t": "rmtg",
            "rel": "lateral habenula excitatory drive to rostromedial tegmental nucleus",
            "status": "established", "kind": "structural",
            "refs": ["wallace2017epn", "azcorra2023dopamine"]
        },
        {
            "s": "lhb-bursting", "t": "rmtg-gaba",
            "rel": "LHb bursting neurons encoding negative reward prediction error driving RMTg GABAergic firing",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "LHb", "dst_layer": "RMTg", "cell_class": "Glutamatergic", "hierarchy_dir": "feedforward"},
            "refs": ["wallace2017epn", "azcorra2023dopamine"]
        },
        {
            "s": "thal-core-relay", "t": "l4-it",
            "rel": "canonical core thalamocortical relay terminating focally in Layer 4",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "FO Core (Tnnt1+/Pvalb+)", "dst_layer": "L4 spiny stellate", "cell_class": "Core", "tract": "thalamocortical", "hierarchy_dir": "feedforward"},
            "refs": ["halassa2019thalamocortical", "phillips2019thalamus"]
        },
        {
            "s": "thal-matrix-relay", "t": "l23-it",
            "rel": "canonical matrix thalamocortical relay dispersing across Layer 1 apical tufts",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "HO Matrix (Calb1+)", "dst_layer": "L1 apical dendrites", "cell_class": "Matrix", "tract": "thalamocortical", "hierarchy_dir": "ascending"},
            "refs": ["halassa2019thalamocortical", "phillips2019thalamus"]
        },

        # =========================================================================
        # 2. HYPOTHALAMUS CIRCUITS (PEPTIDERGIC, FAST TRANSMITTER & HOMEOSTATIC)
        # =========================================================================
        {
            "s": "hypothalamus", "t": "pvn",
            "rel": "hypothalamic central neuroendocrine and autonomic integration hub",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "wang2020ccf"]
        },
        {
            "s": "mpoa", "t": "pvn-oxt",
            "rel": "medial preoptic area driving parental care and oxytocinergic activation",
            "status": "supported", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "yao2023wholebrain"]
        },
        {
            "s": "vlpo", "t": "vlpo-sleep",
            "rel": "ventrolateral preoptic nucleus housing GABA/galanin sleep-active neurons",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "yao2023wholebrain"]
        },
        {
            "s": "vlpo-sleep", "t": "lha-orexin",
            "rel": "VLPO GABAergic inhibition of orexin neurons promoting slow-wave sleep",
            "status": "established", "kind": "mechanistic",
            "refs": ["steuernagel2022hypomap", "siletti2023human"]
        },
        {
            "s": "mnpo-ovlt", "t": "pvn",
            "rel": "median preoptic and OVLT osmosensory neurons driving thirst and vasopressin release",
            "status": "supported", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "wang2020ccf"]
        },
        {
            "s": "scn", "t": "pvn-crh",
            "rel": "suprachiasmatic master circadian clock pacing rhythmic CRH secretion",
            "status": "established", "kind": "mechanistic",
            "refs": ["steuernagel2022hypomap", "wang2020ccf"]
        },
        {
            "s": "pvn", "t": "pvn-oxt",
            "rel": "paraventricular nucleus magnocellular oxytocin neurons",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "siletti2023human"]
        },
        {
            "s": "pvn", "t": "pvn-crh",
            "rel": "paraventricular nucleus parvocellular CRH neurons initiating HPA stress response",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "siletti2023human"]
        },
        {
            "s": "son", "t": "pvn",
            "rel": "supraoptic nucleus neurosecretory cooperation with PVN",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "wang2020ccf"]
        },
        {
            "s": "ahn", "t": "vlpag",
            "rel": "anterior hypothalamic nucleus defensive flight and risk assessment circuit",
            "status": "supported", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "tovote2016"]
        },
        {
            "s": "arc", "t": "arc-agrp",
            "rel": "arcuate nucleus housing hunger-promoting AgRP/NPY neurons",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "yao2023wholebrain"]
        },
        {
            "s": "arc", "t": "arc-pomc",
            "rel": "arcuate nucleus housing satiety-promoting POMC/CART neurons",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "yao2023wholebrain"]
        },
        {
            "s": "arc", "t": "arc-kndy",
            "rel": "arcuate KNDy neurons pacing pulsatile GnRH release for reproduction",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "siletti2023human"]
        },
        {
            "s": "arc-agrp", "t": "lha-orexin",
            "rel": "AgRP/NPY/GABA neurons inhibiting lateral hypothalamic satiety mechanisms and stimulating appetite",
            "status": "established", "kind": "mechanistic",
            "refs": ["steuernagel2022hypomap", "siletti2023human"]
        },
        {
            "s": "arc-pomc", "t": "pvn-crh",
            "rel": "POMC-derived alpha-MSH activating MC4R in PVN to suppress food intake",
            "status": "established", "kind": "mechanistic",
            "refs": ["steuernagel2022hypomap", "siletti2023human"]
        },
        {
            "s": "vmh", "t": "vmh-dm",
            "rel": "ventromedial hypothalamus dorsomedial subdivision",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "wang2020ccf"]
        },
        {
            "s": "vmh", "t": "vmh-vl",
            "rel": "ventromedial hypothalamus ventrolateral subdivision",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "wang2020ccf"]
        },
        {
            "s": "vmh-dm-sf1", "t": "ahn",
            "rel": "SF1+ VMHdm neurons driving predator fear defense and glucose counter-regulation",
            "status": "supported", "kind": "mechanistic",
            "refs": ["steuernagel2022hypomap", "tovote2016"]
        },
        {
            "s": "vmh-vl-esr1", "t": "dmpag-dlpag",
            "rel": "ESR1+ VMHvl neurons projecting to dorsal PAG driving social attack and mounting",
            "status": "supported", "kind": "mechanistic",
            "refs": ["steuernagel2022hypomap", "tovote2016"]
        },
        {
            "s": "dmh", "t": "pvn",
            "rel": "dorsomedial hypothalamus projection driving stress-induced autonomic tachycardia",
            "status": "supported", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "wang2020ccf"]
        },
        {
            "s": "sum", "t": "sum-glugaba",
            "rel": "supramammillary nucleus housing co-transmitting Glu/GABA neurons",
            "status": "supported", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "cembrowski2018subiculum"]
        },
        {
            "s": "sum-glugaba", "t": "dg",
            "rel": "supramammillary dual Glu/GABA projection to dentate gyrus granule cells regulating spatial novelty",
            "status": "supported", "kind": "mechanistic",
            "refs": ["steuernagel2022hypomap", "cembrowski2018subiculum"]
        },
        {
            "s": "mm-lm", "t": "atn-av",
            "rel": "mammillary bodies projecting via mammillothalamic tract to anteroventral thalamus",
            "status": "established", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "wang2020ccf"]
        },
        {
            "s": "lha-orexin", "t": "snc-v",
            "rel": "lateral hypothalamic orexin neurons projecting to ventral tier SNc dopamine neurons",
            "status": "supported", "kind": "mechanistic",
            "refs": ["steuernagel2022hypomap", "azcorra2023dopamine"]
        },

        # =========================================================================
        # 3. COLLICULI & MIDBRAIN TECTUM CIRCUITS
        # =========================================================================
        {
            "s": "tectum", "t": "sc-sup",
            "rel": "midbrain tectum roof encompassing superficial retinorecipient layers",
            "status": "established", "kind": "structural",
            "refs": ["krauzlis2013sc", "basso2017sc"]
        },
        {
            "s": "sc-sup", "t": "sc-med",
            "rel": "superficial superior colliculus medial division representing upper visual field",
            "status": "established", "kind": "structural",
            "refs": ["krauzlis2013sc", "wang2020ccf"]
        },
        {
            "s": "sc-sup", "t": "sc-lat",
            "rel": "superficial superior colliculus lateral division representing lower visual field",
            "status": "established", "kind": "structural",
            "refs": ["krauzlis2013sc", "wang2020ccf"]
        },
        {
            "s": "sc-sup", "t": "sc-widefield-vert",
            "rel": "superficial SC stratum opticum wide-field vertical cells",
            "status": "established", "kind": "structural",
            "refs": ["gale2014sc", "basso2017sc"]
        },
        {
            "s": "sc-sup", "t": "sc-narrowfield-vert",
            "rel": "superficial SC stratum griseum superficiale narrow-field vertical cells",
            "status": "established", "kind": "structural",
            "refs": ["gale2014sc", "basso2017sc"]
        },
        {
            "s": "sc-widefield-vert", "t": "pulvinar",
            "rel": "wide-field vertical neurons projecting to LP/pulvinar for spatial attention",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "Lower SGS/SO", "dst_layer": "Pulvinar (PI)/LP", "cell_class": "Wide-field vertical", "tract": "tectothalamic", "hierarchy_dir": "ascending"},
            "refs": ["gale2014sc", "saalmann2012pulvinar"]
        },
        {
            "s": "sc-narrowfield-vert", "t": "pbg",
            "rel": "narrow-field vertical cells projecting to parabigeminal nucleus",
            "status": "supported", "kind": "structural",
            "refs": ["gale2014sc", "basso2017sc"]
        },
        {
            "s": "pbg", "t": "sc-sup",
            "rel": "parabigeminal cholinergic feedback projection to superficial SC",
            "status": "supported", "kind": "structural",
            "refs": ["basso2017sc", "wang2020ccf"]
        },
        {
            "s": "sc-sup", "t": "sc-deep",
            "rel": "interlaminar excitatory cascade from superficial visuosensory to deep motor SC",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "SGS", "dst_layer": "SGI/SGP", "cell_class": "Interlaminar", "hierarchy_dir": "descending"},
            "refs": ["basso2017sc", "krauzlis2013sc"]
        },
        {
            "s": "sc-deep", "t": "dsc-pitx2-orient",
            "rel": "deep superior colliculus Pitx2+ motor burst neurons",
            "status": "supported", "kind": "structural",
            "refs": ["basso2017sc", "yao2023wholebrain"]
        },
        {
            "s": "sc-deep", "t": "dsc-pvalb-looming",
            "rel": "deep superior colliculus PVALB+ looming-sensitive threat neurons",
            "status": "supported", "kind": "structural",
            "refs": ["basso2017sc", "tovote2016"]
        },
        {
            "s": "dsc-pitx2-orient", "t": "mlr",
            "rel": "Pitx2+ motor neurons projecting to mesencephalic locomotor region to trigger orienting",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "SGI/SGP", "dst_layer": "MLR", "cell_class": "Pitx2+ motor", "tract": "predorsal bundle", "hierarchy_dir": "descending"},
            "refs": ["basso2017sc", "yao2023wholebrain"]
        },
        {
            "s": "dsc-pvalb-looming", "t": "dmpag-dlpag",
            "rel": "PVALB+ looming neurons projecting to dlPAG triggering explosive escape leaps",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "SGI", "dst_layer": "dlPAG", "cell_class": "PVALB+ looming", "hierarchy_dir": "descending"},
            "refs": ["tovote2016", "basso2017sc"]
        },
        {
            "s": "sc-deep", "t": "cnf",
            "rel": "deep SC motor projection to cuneiform nucleus driving rapid locomotor escape",
            "status": "supported", "kind": "structural",
            "refs": ["tovote2016", "basso2017sc"]
        },
        {
            "s": "sc-deep", "t": "thal-md",
            "rel": "ascending corollary discharge from deep SC to MD thalamus projecting to FEF",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "SGI/SGP", "dst_layer": "MDmf", "cell_class": "Corollary discharge", "tract": "tectothalamic", "hierarchy_dir": "ascending"},
            "refs": ["basso2017sc", "krauzlis2013sc"]
        },
        {
            "s": "inferior-colliculus", "t": "ic-cnic",
            "rel": "central nucleus of inferior colliculus primary auditory lemniscal core",
            "status": "established", "kind": "structural",
            "refs": ["goyer2019ic", "silveira2020ic"]
        },
        {
            "s": "inferior-colliculus", "t": "ic-dcic",
            "rel": "dorsal cortex of inferior colliculus corticorecipient belt",
            "status": "established", "kind": "structural",
            "refs": ["goyer2019ic", "silveira2020ic"]
        },
        {
            "s": "inferior-colliculus", "t": "ic-ecic",
            "rel": "external cortex of inferior colliculus multisensory shell",
            "status": "established", "kind": "structural",
            "refs": ["goyer2019ic", "silveira2020ic"]
        },
        {
            "s": "ic-cnic", "t": "ic-disc-tonotopic",
            "rel": "tonotopically organized disc-shaped principal neurons in CNIC",
            "status": "established", "kind": "structural",
            "refs": ["goyer2019ic", "silveira2020ic"]
        },
        {
            "s": "ic-cnic", "t": "ic-vip-stellate",
            "rel": "VIP-expressing principal neurons with large dendritic fields in CNIC",
            "status": "supported", "kind": "structural",
            "refs": ["goyer2019ic"]
        },
        {
            "s": "ic-cnic", "t": "ic-npy-gaba-proj",
            "rel": "NPY+ GABAergic projection neurons providing feedforward inhibition to auditory thalamus",
            "status": "supported", "kind": "structural",
            "refs": ["silveira2020ic"]
        },
        {
            "s": "ic-disc-tonotopic", "t": "mgv",
            "rel": "ascending tonotopic lemniscal drive from CNIC to ventral MGB",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "CNIC Disc", "dst_layer": "MGv", "cell_class": "Lemniscal tonotopic", "tract": "brachium of IC", "hierarchy_dir": "feedforward"},
            "refs": ["goyer2019ic", "silveira2020ic"]
        },
        {
            "s": "ic-dcic", "t": "mgd",
            "rel": "dorsal cortex of IC projecting to dorsal MGB",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "DCIC L1-L3", "dst_layer": "MGd", "cell_class": "Corticorecipient", "hierarchy_dir": "feedforward"},
            "refs": ["goyer2019ic", "halassa2019thalamocortical"]
        },
        {
            "s": "ic-ecic", "t": "sc-deep",
            "rel": "multisensory external IC projection to deep SC for sound-guided gaze shifts",
            "status": "supported", "kind": "structural",
            "refs": ["goyer2019ic", "basso2017sc"]
        },
        {
            "s": "dmpag-dlpag", "t": "cnf",
            "rel": "dorsal and dorsolateral PAG driving active panic escape maneuvers",
            "status": "supported", "kind": "mechanistic",
            "refs": ["tovote2016", "wang2020ccf"]
        },
        {
            "s": "lpag", "t": "mlr",
            "rel": "lateral PAG coordinating confrontation and predatory chase",
            "status": "supported", "kind": "structural",
            "refs": ["tovote2016", "wang2020ccf"]
        },
        {
            "s": "vlpag", "t": "vlpag-chx10-freeze",
            "rel": "ventrolateral PAG housing Chx10+ freezing neurons",
            "status": "supported", "kind": "structural",
            "refs": ["tovote2016", "yao2023wholebrain"]
        },
        {
            "s": "vlpag-chx10-freeze", "t": "spinal-in",
            "rel": "Chx10+ freezing neurons projecting to premotor interneurons driving behavioral arrest",
            "status": "supported", "kind": "mechanistic",
            "refs": ["tovote2016", "yao2023wholebrain"]
        },
        {
            "s": "mlr", "t": "cnf",
            "rel": "mesencephalic locomotor region comprising cuneiform and pedunculopontine nuclei",
            "status": "established", "kind": "structural",
            "refs": ["wang2020ccf", "tovote2016"]
        },

        # =========================================================================
        # 4. MOTOR CORTEX LAMINAR & CELLULAR SUBDIVISIONS
        # =========================================================================
        {
            "s": "m1", "t": "m1-caudal",
            "rel": "caudal M1 division housing monosynaptic corticomotoneuronal (CM) cells",
            "status": "established", "kind": "structural",
            "refs": ["rathelot2009", "biccn2021"]
        },
        {
            "s": "m1", "t": "m1-rostral",
            "rel": "rostral M1 division with polysynaptic descending spinal drive",
            "status": "established", "kind": "structural",
            "refs": ["rathelot2009", "biccn2021"]
        },
        {
            "s": "m1-caudal", "t": "m1-cm",
            "rel": "caudal M1 layer 5B corticomotoneuronal cells",
            "status": "established", "kind": "structural",
            "refs": ["rathelot2009", "siletti2023human"]
        },
        {
            "s": "m1-cm", "t": "spinal-in",
            "rel": "monosynaptic CM cell drive to spinal motoneurons for dexterous finger fractionation",
            "status": "established", "kind": "mechanistic",
            "laminar": {"src_layer": "L5B (deep)", "dst_layer": "Lamina IX motoneurons", "cell_class": "CM pyramidal", "tract": "corticospinal tract", "hierarchy_dir": "corticofugal"},
            "refs": ["rathelot2009", "siletti2023human"]
        },
        {
            "s": "motor-cortex", "t": "pmd",
            "rel": "dorsal premotor cortex mediating reaching preparation",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "biccn2021"]
        },
        {
            "s": "motor-cortex", "t": "pmv",
            "rel": "ventral premotor cortex mediating grasping and visuomotor transformation",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "biccn2021"]
        },
        {
            "s": "motor-cortex", "t": "presma",
            "rel": "pre-supplementary motor area mediating cognitive motor sequencing",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "biccn2021"]
        },
        {
            "s": "motor-cortex", "t": "sma",
            "rel": "supplementary motor area mediating bimanual coordination and execution",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "biccn2021"]
        },
        {
            "s": "presma", "t": "sma",
            "rel": "hierarchical feedforward drive from pre-SMA to SMA during motor sequence initiation",
            "status": "supported", "kind": "structural",
            "refs": ["jung2021charm", "biccn2021"]
        },
        {
            "s": "m1", "t": "scan",
            "rel": "somato-cognitive action network inter-effector regions alternating with classic homunculus",
            "status": "supported", "kind": "structural",
            "refs": ["gordon2023"]
        },
        {
            "s": "scan", "t": "dacc",
            "rel": "SCAN functional connectivity with dorsal anterior cingulate cortex during whole-body action",
            "status": "supported", "kind": "functional",
            "refs": ["gordon2023"]
        },
        {
            "s": "l23-it", "t": "l5-it",
            "rel": "intracortical intratelencephalic feedforward cascade from L2/3 to L5 IT",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L2/3", "dst_layer": "L5A", "cell_class": "IT", "hierarchy_dir": "descending"},
            "refs": ["biccn2021", "yao2021taxonomy"]
        },
        {
            "s": "l4-it", "t": "l23-it",
            "rel": "granular layer 4 spiny stellate/pyramidal drive to superficial supragranular layers",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L4", "dst_layer": "L2/3", "cell_class": "IT", "hierarchy_dir": "ascending"},
            "refs": ["biccn2021", "siletti2023human"]
        },
        {
            "s": "l5-it", "t": "dms",
            "rel": "bilateral Layer 5 IT corticostriatal projection to associative striatal matrix",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L5A", "dst_layer": "Matrix", "cell_class": "IT", "tract": "corticostriatal", "hierarchy_dir": "feedforward"},
            "refs": ["biccn2021", "ding2026homba"]
        },
        {
            "s": "l5-pt-thal", "t": "thal-val",
            "rel": "upper L5B PT-thalamic projection sustaining persistent motor preparatory activity",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "L5B (upper)", "dst_layer": "VAL", "cell_class": "PT/ET", "tract": "corticothalamic", "hierarchy_dir": "corticofugal"},
            "refs": ["winnubst2019mouselight", "guo2017thalamus"]
        },
        {
            "s": "l5-pt-med", "t": "mlr",
            "rel": "lower L5B PT-medullary projection driving motor execution commands",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L5B (lower)", "dst_layer": "MLR/medulla", "cell_class": "PT/ET", "tract": "corticobulbar", "hierarchy_dir": "corticofugal"},
            "refs": ["winnubst2019mouselight", "economo2018"]
        },
        {
            "s": "l56-np", "t": "l5-pt-med",
            "rel": "near-projecting L5/6 neurons providing dense local recurrent modulation",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "L5/6 NP", "dst_layer": "L5B PT", "cell_class": "NP", "hierarchy_dir": "local"},
            "refs": ["yao2021taxonomy", "biccn2021"]
        },
        {
            "s": "l6-ct", "t": "thal-val",
            "rel": "layer 6 corticothalamic feedback to motor thalamus",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L6 CT", "dst_layer": "VAL Core", "cell_class": "CT", "tract": "corticothalamic", "hierarchy_dir": "feedback"},
            "refs": ["biccn2021", "halassa2019thalamocortical"]
        },
        {
            "s": "l6-it", "t": "l23-it",
            "rel": "layer 6 IT intracortical feedback to supragranular layers",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "L6 IT", "dst_layer": "L2/3", "cell_class": "IT", "hierarchy_dir": "ascending"},
            "refs": ["yao2021taxonomy", "biccn2021"]
        },
        {
            "s": "l6b", "t": "thal-vm",
            "rel": "subplate layer 6b neurons innervating matrix thalamus and responding to orexin",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "L6b", "dst_layer": "VM", "cell_class": "Subplate", "tract": "corticothalamic", "hierarchy_dir": "corticofugal"},
            "refs": ["yao2021taxonomy", "phillips2019thalamus"]
        },
        {
            "s": "pv-chandelier", "t": "l23-it",
            "rel": "axo-axonic chandelier cells terminating on the axon initial segment (AIS) of pyramidal cells",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L2/3", "dst_layer": "AIS", "cell_class": "PVALB+", "hierarchy_dir": "local"},
            "refs": ["krienen2020innovations", "yao2021taxonomy"]
        },
        {
            "s": "sst-martinotti", "t": "l23-it",
            "rel": "Martinotti interneurons targeting Layer 1 apical dendritic tufts of pyramidal cells",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L5", "dst_layer": "L1 tuft", "cell_class": "SST+", "hierarchy_dir": "local"},
            "refs": ["yao2021taxonomy", "krienen2020innovations"]
        },
        {
            "s": "sst-chodl", "t": "l23-it",
            "rel": "SST-Chodl long-range projecting nitric oxide synthase interneurons modulating slow-wave sleep",
            "status": "supported", "kind": "structural",
            "refs": ["yao2021taxonomy", "siletti2023human"]
        },
        {
            "s": "vip-disinhibitory", "t": "sst-martinotti",
            "rel": "VIP interneurons inhibiting SST Martinotti cells to open dendritic input windows",
            "status": "established", "kind": "mechanistic",
            "laminar": {"src_layer": "L2/3", "dst_layer": "L5", "cell_class": "VIP+", "hierarchy_dir": "disinhibition"},
            "refs": ["krienen2020innovations", "yao2021taxonomy"]
        },
        {
            "s": "lamp5-canopy", "t": "l23-it",
            "rel": "Lamp5 neurogliaform canopy cells mediating volume transmission GABAergic inhibition in Layer 1",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "L1", "dst_layer": "L1/L2", "cell_class": "Lamp5+", "hierarchy_dir": "local"},
            "refs": ["yao2021taxonomy", "krienen2020innovations"]
        },

        # =========================================================================
        # 5. PREFRONTAL CORTEX REGIONAL SUBDIVISIONS
        # =========================================================================
        {
            "s": "pfc", "t": "dlpfc-9",
            "rel": "granular prefrontal area 9 mediating abstract rule representations",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "chen2023stereo"]
        },
        {
            "s": "pfc", "t": "dlpfc-46d",
            "rel": "dorsal area 46 mediating spatial and verbal working memory delay firing",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "chen2023stereo"]
        },
        {
            "s": "pfc", "t": "vlpfc",
            "rel": "ventrolateral prefrontal cortex mediating active memory retrieval and response inhibition",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "chen2023stereo"]
        },
        {
            "s": "pfc", "t": "fpc-10l",
            "rel": "lateral frontopolar cortex mediating multi-task branching and exploration",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "chen2023stereo"]
        },
        {
            "s": "pfc", "t": "ofc-lat",
            "rel": "lateral orbitofrontal cortex evaluating stimulus-outcome associations and credit assignment",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "chen2023stereo"]
        },
        {
            "s": "pfc", "t": "ofc-med",
            "rel": "medial orbitofrontal cortex encoding subjective reward values and economic utility",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "chen2023stereo"]
        },
        {
            "s": "pfc", "t": "dacc",
            "rel": "dorsal anterior cingulate cortex mediating cognitive conflict monitoring and effort-reward trade-offs",
            "status": "established", "kind": "structural",
            "refs": ["jung2021charm", "chen2023stereo"]
        },
        {
            "s": "dlpfc-46d", "t": "caudate",
            "rel": "primate executive corticostriatal projection from area 46 to caudate head",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "L5A", "dst_layer": "Matrix", "cell_class": "IT", "tract": "corticostriatal", "hierarchy_dir": "feedforward"},
            "refs": ["haber2010reward", "ding2026homba"]
        },
        {
            "s": "ofc-med", "t": "nac-core",
            "rel": "ventral frontostriatal projection to nucleus accumbens core encoding value",
            "status": "established", "kind": "structural",
            "refs": ["haber2010reward", "ding2026homba"]
        },
        {
            "s": "dacc", "t": "stn-assoc",
            "rel": "hyperdirect projection from dACC to STN associative territory for reactive stopping",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "L5B", "dst_layer": "STN", "cell_class": "ET", "tract": "hyperdirect", "hierarchy_dir": "feedforward"},
            "refs": ["haber2010reward", "hartig2021sarm"]
        },

        # =========================================================================
        # 6. BASAL GANGLIA SINGLE-CELL, COMPARTMENT & DOPAMINE TAXONOMIES
        # =========================================================================
        {
            "s": "striatum", "t": "dms",
            "rel": "associative territory of dorsal striatum mediating flexible action-outcome learning",
            "status": "established", "kind": "structural",
            "refs": ["haber2010reward", "stanley2020striatum"]
        },
        {
            "s": "striatum", "t": "caudate",
            "rel": "primate associative division of striatum supporting cognitive goal maintenance",
            "status": "established", "kind": "structural",
            "refs": ["haber2010reward", "ding2026homba"]
        },
        {
            "s": "striatum", "t": "dls",
            "rel": "sensorimotor territory of rodent dorsal striatum mediating motor habits",
            "status": "established", "kind": "structural",
            "refs": ["haber2010reward", "stanley2020striatum"]
        },
        {
            "s": "striatum", "t": "putamen",
            "rel": "primate sensorimotor striatum driving skilled motor habit execution",
            "status": "established", "kind": "structural",
            "refs": ["haber2010reward", "ding2026homba"]
        },
        {
            "s": "striatum", "t": "ts-cdt",
            "rel": "striatal tail / caudal caudate mediating stable value coding of visual objects",
            "status": "supported", "kind": "structural",
            "refs": ["yamamoto2013caudate", "ding2026homba"]
        },
        {
            "s": "striatum", "t": "striosome",
            "rel": "mu-opioid receptor-rich striosome (patch) compartment receiving limbic inputs",
            "status": "established", "kind": "structural",
            "refs": ["crittenden2016striosome", "bican2026spatial"]
        },
        {
            "s": "striatum", "t": "matrix",
            "rel": "calbindin-rich matrix compartment receiving sensorimotor and executive cortical inputs",
            "status": "established", "kind": "structural",
            "refs": ["crittenden2016striosome", "bican2026spatial"]
        },
        {
            "s": "striatum", "t": "nac-core",
            "rel": "nucleus accumbens core subregion mediating cue-directed pavlovian approach",
            "status": "established", "kind": "structural",
            "refs": ["haber2010reward", "ding2026homba"]
        },
        {
            "s": "striatum", "t": "nac-mshell",
            "rel": "nucleus accumbens medial shell subregion mediating hedonic impact and valence",
            "status": "established", "kind": "structural",
            "refs": ["haber2010reward", "ding2026homba"]
        },
        {
            "s": "dspn-striosome", "t": "snc-v",
            "rel": "striosome dSPNs forming striosome-dendron bouquets directly inhibiting dopamine neurons",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "Striosome", "dst_layer": "SNc ventral tier", "cell_class": "dSPN", "hierarchy_dir": "inhibitory"},
            "refs": ["crittenden2016striosome", "poulin2018dopamine"]
        },
        {
            "s": "dspn-matrix", "t": "gpi-motor",
            "rel": "matrix dSPNs directly inhibiting internal globus pallidus output neurons",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "Matrix", "dst_layer": "GPi", "cell_class": "dSPN", "tract": "direct pathway", "hierarchy_dir": "feedforward"},
            "refs": ["bican2026spatial", "ding2026homba"]
        },
        {
            "s": "ispn-matrix", "t": "gpe-prototypic",
            "rel": "matrix iSPNs projecting to prototypic GPe neurons in the indirect pathway",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "Matrix", "dst_layer": "GPe", "cell_class": "iSPN", "tract": "indirect pathway", "hierarchy_dir": "feedforward"},
            "refs": ["bican2026spatial", "ding2026homba"]
        },
        {
            "s": "ispn-striosome", "t": "gpe-arkypallidal",
            "rel": "striosome iSPNs modulating arkypallidal feedback to dorsal striatum",
            "status": "supported", "kind": "structural",
            "refs": ["bican2026spatial", "stanley2020striatum"]
        },
        {
            "s": "str-tac3-in", "t": "matrix",
            "rel": "human and primate TAC3+ interneurons selectively positioned in the matrix compartment",
            "status": "supported", "kind": "structural",
            "refs": ["bican2026spatial", "krienen2020innovations"]
        },
        {
            "s": "gpe-prototypic", "t": "stn-motor",
            "rel": "prototypic PVALB+ GPe neurons providing feedforward inhibition to subthalamic nucleus",
            "status": "established", "kind": "structural",
            "refs": ["bican2026spatial", "hartig2021sarm"]
        },
        {
            "s": "gpe-arkypallidal", "t": "striatum",
            "rel": "arkypallidal Foxp2+ GPe neurons sending retrograde collateral inhibition to striatum",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "GPe", "dst_layer": "Striatum", "cell_class": "Foxp2+ arkypallidal", "hierarchy_dir": "feedback"},
            "refs": ["bican2026spatial", "stanley2020striatum"]
        },
        {
            "s": "gpi-motor", "t": "thal-vla",
            "rel": "motor GPi output delivering tonic GABAergic inhibition to VLa/VLo thalamus",
            "status": "established", "kind": "structural",
            "refs": ["halassa2019thalamocortical", "hartig2021sarm"]
        },
        {
            "s": "gpi-limbic", "t": "lhb",
            "rel": "limbic EPN/GPi territory projecting to lateral habenula to encode negative reward outcomes",
            "status": "supported", "kind": "structural",
            "refs": ["wallace2017epn", "hartig2021sarm"]
        },
        {
            "s": "epn-limbic-glugaba", "t": "lhb",
            "rel": "somatostatin-expressing EPN neurons co-releasing glutamate and GABA onto LHb",
            "status": "supported", "kind": "mechanistic",
            "refs": ["wallace2017epn"]
        },
        {
            "s": "vp-dl", "t": "stn-assoc",
            "rel": "dorsolateral ventral pallidum associative output modulating cognitive selection",
            "status": "supported", "kind": "structural",
            "refs": ["ledbetter2016bf", "haber2010reward"]
        },
        {
            "s": "vp-vm", "t": "lhb",
            "rel": "ventromedial ventral pallidum projecting to lateral habenula to signal loss",
            "status": "supported", "kind": "structural",
            "refs": ["ledbetter2016bf", "wallace2017epn"]
        },
        {
            "s": "stn-motor", "t": "gpi-motor",
            "rel": "motor STN driving excitatory bursting in motor GPi",
            "status": "established", "kind": "structural",
            "refs": ["hartig2021sarm", "ding2026homba"]
        },
        {
            "s": "stn-assoc", "t": "snr-vm",
            "rel": "associative STN driving ventromedial SNr during action cancelation",
            "status": "supported", "kind": "structural",
            "refs": ["hartig2021sarm", "haber2010reward"]
        },
        {
            "s": "snr-vm", "t": "thal-va",
            "rel": "ventromedial SNr territory gating motor and executive thalamic relays",
            "status": "established", "kind": "structural",
            "refs": ["halassa2019thalamocortical", "hartig2021sarm"]
        },
        {
            "s": "snr-cdl", "t": "sc-deep",
            "rel": "caudodorsal-lateral SNr tonic inhibition of deep collicular saccade burst neurons",
            "status": "established", "kind": "structural",
            "refs": ["basso2017sc", "hartig2021sarm"]
        },
        {
            "s": "snc-v", "t": "snc-sox6-aldh1a1",
            "rel": "ventral tier SNc housing vulnerable Sox6+/Aldh1a1+ dopamine neurons",
            "status": "established", "kind": "structural",
            "refs": ["poulin2018dopamine", "azcorra2023dopamine"]
        },
        {
            "s": "snc-d", "t": "snc-calb1",
            "rel": "dorsal tier SNc housing resilient Calb1+ dopamine neurons",
            "status": "established", "kind": "structural",
            "refs": ["poulin2018dopamine", "azcorra2023dopamine"]
        },
        {
            "s": "snl", "t": "ts-cdt",
            "rel": "substantia nigra pars lateralis projecting to striatal tail",
            "status": "supported", "kind": "structural",
            "refs": ["yamamoto2013caudate", "ding2026homba"]
        },
        {
            "s": "snc-sox6-aldh1a1", "t": "dls",
            "rel": "Sox6+ dopamine neurons encoding kinematic vigor projecting to dorsolateral striatum",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "Ventral Tier", "dst_layer": "DLS", "cell_class": "Dopamine (Sox6+)", "tract": "nigrostriatal", "hierarchy_dir": "ascending"},
            "refs": ["azcorra2023dopamine", "poulin2018dopamine"]
        },
        {
            "s": "snc-calb1", "t": "dms",
            "rel": "Calb1+ dopamine neurons encoding reward prediction errors projecting to dorsomedial striatum",
            "status": "supported", "kind": "mechanistic",
            "laminar": {"src_layer": "Dorsal Tier", "dst_layer": "DMS", "cell_class": "Dopamine (Calb1+)", "tract": "nigrostriatal", "hierarchy_dir": "ascending"},
            "refs": ["azcorra2023dopamine", "poulin2018dopamine"]
        },
        {
            "s": "snc-lat-vglut2", "t": "ts-cdt",
            "rel": "lateral SN dopamine neurons co-releasing glutamate projecting to striatal tail",
            "status": "supported", "kind": "structural",
            "refs": ["poulin2018dopamine", "yamamoto2013caudate"]
        },
        {
            "s": "rmtg", "t": "rmtg-gaba",
            "rel": "rostromedial tegmental nucleus GABAergic tail of VTA",
            "status": "established", "kind": "structural",
            "refs": ["azcorra2023dopamine", "wallace2017epn"]
        },
        {
            "s": "rmtg-gaba", "t": "snc-v",
            "rel": "RMTg GABAergic brake providing strong inhibition to midbrain dopamine neurons",
            "status": "established", "kind": "mechanistic",
            "refs": ["azcorra2023dopamine", "wallace2017epn"]
        },

        # =========================================================================
        # 7. HIPPOCAMPAL-PARAHIPPOCAMPAL LAMINAR & SINGLE-CELL TAXONOMIES
        # =========================================================================
        {
            "s": "ca1", "t": "ca1-sup-pyr",
            "rel": "superficial CA1 pyramidal cells expressing Calb1 with stable landmark firing",
            "status": "established", "kind": "structural",
            "refs": ["soltesz2018ca1", "yao2021taxonomy"]
        },
        {
            "s": "ca1", "t": "ca1-deep-pyr",
            "rel": "deep CA1 pyramidal cells expressing Ndst4 encoding reward and projecting extrahippocampally",
            "status": "established", "kind": "structural",
            "refs": ["soltesz2018ca1", "yao2021taxonomy"]
        },
        {
            "s": "ca1-sup-pyr", "t": "mec",
            "rel": "superficial CA1 pyramidal cells projecting to medial entorhinal cortex layer 5B",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "CA1 superficial", "dst_layer": "MEC L5B", "cell_class": "Calb1+ pyramidal", "hierarchy_dir": "feedforward"},
            "refs": ["soltesz2018ca1", "surmeli2015entorhinal"]
        },
        {
            "s": "ca1-deep-pyr", "t": "nac",
            "rel": "deep CA1 pyramidal cells projecting to nucleus accumbens for reward-place associations",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "CA1 deep", "dst_layer": "NAc", "cell_class": "Ndst4+ pyramidal", "hierarchy_dir": "ascending"},
            "refs": ["soltesz2018ca1", "cembrowski2018subiculum"]
        },
        {
            "s": "ca1-deep-pyr", "t": "bla",
            "rel": "deep CA1 pyramidal cells projecting to basolateral amygdala for contextual valence",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "CA1 deep", "dst_layer": "BLA", "cell_class": "Ndst4+ pyramidal", "hierarchy_dir": "ascending"},
            "refs": ["soltesz2018ca1", "oleary2020bla"]
        },
        {
            "s": "hippocampus", "t": "prosubiculum",
            "rel": "prosubiculum transitional allocortex nestled between CA1 and classical subiculum",
            "status": "established", "kind": "structural",
            "refs": ["cembrowski2018subiculum", "wang2020ccf"]
        },
        {
            "s": "prosubiculum", "t": "nac-mshell",
            "rel": "prosubiculum projecting to nucleus accumbens medial shell driving contextual motivation",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "Prosubiculum", "dst_layer": "NAc mShell", "cell_class": "Pyramidal", "hierarchy_dir": "feedforward"},
            "refs": ["cembrowski2018subiculum"]
        },
        {
            "s": "subiculum", "t": "mm-lm",
            "rel": "distal subiculum projecting via postcommissural fornix to mammillary bodies",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "Distal Subiculum", "dst_layer": "Mammillary", "cell_class": "Pyramidal", "tract": "fornix", "hierarchy_dir": "descending"},
            "refs": ["cembrowski2018subiculum", "wang2020ccf"]
        },
        {
            "s": "hippocampus", "t": "mec",
            "rel": "medial entorhinal cortex housing grid cells and head-direction representations",
            "status": "established", "kind": "structural",
            "refs": ["surmeli2015entorhinal", "wang2020ccf"]
        },
        {
            "s": "hippocampus", "t": "lec",
            "rel": "lateral entorhinal cortex housing object, item, and odor representations",
            "status": "established", "kind": "structural",
            "refs": ["surmeli2015entorhinal", "bekkers2013piriform"]
        },
        {
            "s": "mec", "t": "rsp",
            "rel": "medial entorhinal cortex reciprocal communication with retrosplenial cortex",
            "status": "established", "kind": "structural",
            "refs": ["surmeli2015entorhinal", "wang2020ccf"]
        },
        {
            "s": "lec", "t": "piriform",
            "rel": "lateral entorhinal cortex reciprocal connection with primary piriform cortex",
            "status": "established", "kind": "structural",
            "refs": ["bekkers2013piriform", "surmeli2015entorhinal"]
        },
        {
            "s": "rsp", "t": "atn-ad",
            "rel": "retrosplenial cortex projection to anterodorsal thalamus for head-direction integration",
            "status": "established", "kind": "structural",
            "refs": ["wang2020ccf", "cembrowski2018subiculum"]
        },

        # =========================================================================
        # 8. CEREBELLAR SUBDIVISIONS & CELL-TYPE TAXONOMIES
        # =========================================================================
        {
            "s": "cb-cortex", "t": "paraflocculus",
            "rel": "paraflocculus lobule regulating smooth-pursuit eye movements and vestibulo-ocular reflexes",
            "status": "established", "kind": "structural",
            "refs": ["wang2020ccf", "hartig2021sarm"]
        },
        {
            "s": "cb-cortex", "t": "purkinje-zebrin-pos",
            "rel": "Purkinje cells in Zebrin II-positive (Aldoc+) bands firing at lower rates and exhibiting LTP",
            "status": "established", "kind": "structural",
            "refs": ["kozareva2021", "hao2024"]
        },
        {
            "s": "cb-cortex", "t": "purkinje-zebrin-neg",
            "rel": "Purkinje cells in Zebrin II-negative (Aldoc-) bands firing at higher baseline rates and exhibiting LTD",
            "status": "established", "kind": "structural",
            "refs": ["kozareva2021", "hao2024"]
        },
        {
            "s": "purkinje-zebrin-pos", "t": "dn-ventral",
            "rel": "Zebrin-positive Purkinje cells inhibiting ventral dentate non-motor territory",
            "status": "supported", "kind": "structural",
            "refs": ["dum2003dn", "hao2024"]
        },
        {
            "s": "purkinje-zebrin-neg", "t": "dn-dorsal",
            "rel": "Zebrin-negative Purkinje cells inhibiting dorsal dentate motor territory",
            "status": "supported", "kind": "structural",
            "refs": ["dum2003dn", "hao2024"]
        },
        {
            "s": "cb-cortex", "t": "mli1",
            "rel": "molecular layer interneuron 1 (basket cells) forming pericellular nests around Purkinje somata",
            "status": "established", "kind": "structural",
            "refs": ["kozareva2021", "hao2024"]
        },
        {
            "s": "cb-cortex", "t": "mli2",
            "rel": "molecular layer interneuron 2 (stellate cells) targeting Purkinje dendritic trees",
            "status": "established", "kind": "structural",
            "refs": ["kozareva2021", "hao2024"]
        },
        {
            "s": "mli1", "t": "purkinje",
            "rel": "MLI1 basket cells providing powerful ephaptic and GABAergic inhibition at Purkinje axon initial segment",
            "status": "established", "kind": "mechanistic",
            "refs": ["kozareva2021", "hao2024"]
        },
        {
            "s": "cb-cortex", "t": "candelabrum",
            "rel": "candelabrum interneurons located in Purkinje cell layer receiving parallel fiber inputs",
            "status": "supported", "kind": "structural",
            "refs": ["kozareva2021", "siletti2023human"]
        },
        {
            "s": "dcn", "t": "dn-dorsal",
            "rel": "dorsal dentate nucleus motor domain connecting with motor cortex via VLp",
            "status": "established", "kind": "structural",
            "refs": ["dum2003dn", "bostan2010"]
        },
        {
            "s": "dcn", "t": "dn-ventral",
            "rel": "ventral dentate nucleus expanded non-motor cognitive domain connecting with dlPFC",
            "status": "established", "kind": "structural",
            "refs": ["dum2003dn", "strick2009"]
        },
        {
            "s": "dn-dorsal", "t": "thal-vlp",
            "rel": "dorsal dentate projecting to VLp motor thalamus reaching M1",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "Dorsal Dentate", "dst_layer": "VLp (Vim)", "cell_class": "Class A glutamatergic", "tract": "superior cerebellar peduncle", "hierarchy_dir": "ascending"},
            "refs": ["dum2003dn", "bostan2010"]
        },
        {
            "s": "dn-ventral", "t": "thal-md",
            "rel": "ventral dentate projecting via MD/VLcc thalamus reaching dorsolateral prefrontal cortex",
            "status": "established", "kind": "structural",
            "laminar": {"src_layer": "Ventral Dentate", "dst_layer": "MD/VLcc", "cell_class": "Class A glutamatergic", "tract": "superior cerebellar peduncle", "hierarchy_dir": "ascending"},
            "refs": ["dum2003dn", "strick2009"]
        },
        {
            "s": "dcn", "t": "dcn-class-ab",
            "rel": "excitatory large projection neurons across deep cerebellar nuclei",
            "status": "established", "kind": "structural",
            "refs": ["kebschull2020dcn", "hao2024"]
        },
        {
            "s": "dcn", "t": "dcn-sox14-no",
            "rel": "inhibitory Sox14+ nucleo-olivary projection neurons across deep cerebellar nuclei",
            "status": "established", "kind": "structural",
            "refs": ["kebschull2020dcn", "hao2024"]
        },
        {
            "s": "dcn-sox14-no", "t": "io",
            "rel": "DCN nucleo-olivary GABAergic projection providing feedback inhibition to inferior olive",
            "status": "established", "kind": "mechanistic",
            "refs": ["kebschull2020dcn", "hao2024"]
        },

        # =========================================================================
        # 9. AMYGDALA, INSULA & EXTENDED SYSTEMS
        # =========================================================================
        {
            "s": "amygdala", "t": "bla-complex",
            "rel": "basolateral amygdalar complex comprising lateral, basal, and accessory nuclei",
            "status": "established", "kind": "structural",
            "refs": ["gothard2020amygdala", "hartig2021sarm"]
        },
        {
            "s": "bla-complex", "t": "pal",
            "rel": "paralaminar nucleus harboring immature plastic DCX+ neurons in primates",
            "status": "supported", "kind": "structural",
            "refs": ["hartig2021sarm", "gothard2020amygdala"]
        },
        {
            "s": "amygdala", "t": "bnst",
            "rel": "bed nucleus of the stria terminalis forming extended amygdala",
            "status": "established", "kind": "structural",
            "refs": ["wang2020ccf", "hartig2021sarm"]
        },
        {
            "s": "bnst", "t": "lha-orexin",
            "rel": "BNST projection to lateral hypothalamus orchestrating stress-induced wakefulness",
            "status": "supported", "kind": "structural",
            "refs": ["steuernagel2022hypomap", "hartig2021sarm"]
        },
        {
            "s": "insula", "t": "ins-gran",
            "rel": "posterior granular insular cortex primary interoceptive sensory area",
            "status": "established", "kind": "structural",
            "refs": ["evrard2019insula", "hartig2021sarm"]
        },
        {
            "s": "insula", "t": "ins-dys",
            "rel": "intermediate dysgranular insular cortex polymodal integration belt",
            "status": "established", "kind": "structural",
            "refs": ["evrard2019insula", "hartig2021sarm"]
        },
        {
            "s": "insula", "t": "ins-agran",
            "rel": "anterior agranular insular cortex salience and visceral autonomic hub",
            "status": "established", "kind": "structural",
            "refs": ["evrard2019insula", "hartig2021sarm"]
        },
        {
            "s": "ins-agran", "t": "ven-fork",
            "rel": "anterior agranular insula Layer 5b Von Economo and fork projection neurons",
            "status": "established", "kind": "structural",
            "refs": ["evrard2019insula", "siletti2023human"]
        },
        {
            "s": "ven-fork", "t": "vlpag",
            "rel": "Von Economo neuron projection to ventrolateral PAG and autonomic brainstem",
            "status": "supported", "kind": "structural",
            "laminar": {"src_layer": "L5b", "dst_layer": "vlPAG", "cell_class": "VEN", "hierarchy_dir": "descending"},
            "refs": ["evrard2019insula", "siletti2023human"]
        },
        {
            "s": "insula", "t": "claustrum",
            "rel": "subcortical telencephalic claustrum deeply adjacent to insula",
            "status": "established", "kind": "structural",
            "refs": ["wang2020ccf", "hartig2021sarm"]
        },
        {
            "s": "claustrum", "t": "dlpfc-9",
            "rel": "claustrum widespread reciprocal synchronizing projections across prefrontal cortex",
            "status": "supported", "kind": "structural",
            "refs": ["wang2020ccf", "hartig2021sarm"]
        }
    ]

def get_circuits():
    return [
        {
            "id": "thalamocortical-core-matrix",
            "name": "Core and Matrix Thalamocortical Architecture",
            "region": "thalamus",
            "desc": "Dissociation between focal Core relay targeting Layer 4 (e.g. VAL, VPM, LGN) and diffuse Matrix relay targeting Layer 1 apical tufts across the neocortex (e.g. VM, POm, Pulvinar).",
            "links": [
                "thal-core-relay>l4-it",
                "thal-matrix-relay>l23-it",
                "thal-vlp>m1",
                "thal-val>m1",
                "thal-vm>l23-it",
                "vpm>l4-it",
                "pom>l23-it"
            ]
        },
        {
            "id": "transthalamic-corticothalamic",
            "name": "Transthalamic Cortico-Thalamo-Cortical Pathways",
            "region": "thalamus",
            "desc": "Cortical Layer 5B pyramidal tract neurons send driver projections to higher-order thalamus (MD, Pulvinar, POm), which in turn project to association cortex, forming indirect transthalamic information routes.",
            "links": [
                "l5-pt-thal>thal-vm",
                "dlpfc-46d>thal-md",
                "v1>pulvinar",
                "thal-md>dlpfc-9",
                "pulvinar>v4",
                "pulvinar>mt",
                "m1>thal-val"
            ]
        },
        {
            "id": "reticular-thalamic-gating",
            "name": "Thalamic Reticular (TRN) Sensory Gating & Spindles",
            "region": "thalamus",
            "desc": "TRN Spp1+ core and Ecel1+ edge neurons provide topography-specific feedforward and feedback GABAergic inhibition to first-order and higher-order thalamus, regulating sleep spindles and sensory gating.",
            "links": [
                "trn>thal-val",
                "trn-spp1-core>vpm",
                "trn-ecel1-edge>thal-md",
                "zi>pom",
                "mhb>lhb",
                "lhb>rmtg"
            ]
        },
        {
            "id": "arcuate-feeding-circuit",
            "name": "Arcuate AgRP/POMC Feeding & Satiety Circuit",
            "region": "hypothalamus",
            "desc": "Orexigenic AgRP/NPY neurons and anorexigenic POMC neurons in the arcuate nucleus integrate leptin, ghrelin, and nutrients to reciprocally drive and inhibit feeding via PVN and lateral hypothalamus.",
            "links": [
                "hypothalamus>pvn",
                "arc>arc-agrp",
                "arc>arc-pomc",
                "arc-agrp>lha-orexin",
                "arc-pomc>pvn-crh"
            ]
        },
        {
            "id": "circadian-arousal-network",
            "name": "SCN & Hypothalamic Sleep-Wake Arousal Network",
            "region": "hypothalamus",
            "desc": "Suprachiasmatic master clock synchronizes lateral hypothalamic orexin/hypocretin neurons (promoting wakefulness) and VLPO GABA/galanin neurons (promoting slow-wave sleep).",
            "links": [
                "scn>pvn-crh",
                "vlpo>vlpo-sleep",
                "vlpo-sleep>lha-orexin",
                "lha-orexin>snc-v"
            ]
        },
        {
            "id": "hypothalamic-autonomic-stress",
            "name": "HPA Axis & Sympathoadrenal Stress Response",
            "region": "hypothalamus",
            "desc": "Paraventricular CRH/oxytocin neurons orchestrate pituitary-adrenal glucocorticoid secretion and autonomic fight-or-flight signaling via brainstem and spinal preganglionic centers.",
            "links": [
                "pvn>pvn-crh",
                "pvn>pvn-oxt",
                "dmh>pvn",
                "ahn>vlpag",
                "vmh-dm-sf1>ahn",
                "vmh-vl-esr1>dmpag-dlpag"
            ]
        },
        {
            "id": "tectal-retinotopic-orienting",
            "name": "Superior Colliculus Visuomotor Orienting & Saccades",
            "region": "colliculi",
            "desc": "Superficial SC visuosensory layers process retinotopic visual salience and drive deep motor SC, which issues saccadic commands via the predorsal bundle to brainstem premotor centers.",
            "links": [
                "tectum>sc-sup",
                "sc-sup>sc-med",
                "sc-sup>sc-lat",
                "sc-sup>sc-deep",
                "sc-deep>dsc-pitx2-orient",
                "dsc-pitx2-orient>mlr",
                "sc-deep>thal-md"
            ]
        },
        {
            "id": "tectal-pulvinar-extrageniculate",
            "name": "Extrageniculate Tecto-Pulvinar Visual Pathway",
            "region": "colliculi",
            "desc": "Wide-field vertical neurons in superficial SC project to pulvinar and lateral posterior (LP) thalamus, bypassing the primary visual pathway to mediate blindsight and covert spatial attention.",
            "links": [
                "sc-sup>sc-widefield-vert",
                "sc-widefield-vert>pulvinar",
                "sc-sup>sc-narrowfield-vert",
                "sc-narrowfield-vert>pbg",
                "pbg>sc-sup"
            ]
        },
        {
            "id": "tectal-escape-defense",
            "name": "Collicular-PAG Looming Threat & Escape Circuit",
            "region": "colliculi",
            "desc": "Deep SC Parvalbumin+ looming-detecting neurons project to dorsolateral PAG and cuneiform nucleus to initiate explosive escape maneuvers, while ventrolateral PAG drives freezing.",
            "links": [
                "sc-deep>dsc-pvalb-looming",
                "dsc-pvalb-looming>dmpag-dlpag",
                "dmpag-dlpag>cnf",
                "sc-deep>cnf",
                "vlpag>vlpag-chx10-freeze",
                "vlpag-chx10-freeze>spinal-in"
            ]
        },
        {
            "id": "auditory-collicular-cascade",
            "name": "Inferior Colliculus Tonotopic & Corticofugal Cascade",
            "region": "colliculi",
            "desc": "Ascending auditory brainstem inputs converge onto central IC tonotopic disc neurons projecting to MGv, while auditory cortex Layer 5B feeds back giant boutons onto dorsal IC.",
            "links": [
                "inferior-colliculus>ic-cnic",
                "inferior-colliculus>ic-dcic",
                "inferior-colliculus>ic-ecic",
                "ic-cnic>ic-disc-tonotopic",
                "ic-disc-tonotopic>mgv",
                "ic-dcic>mgd",
                "ic-ecic>sc-deep"
            ]
        }
    ]
