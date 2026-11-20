# -*- coding: utf-8 -*-
"""
tools/v03_entities.py
All new regions, hierarchical entities, single-cell taxonomies,
laminar links, circuits, chains and questions for Brain Circuit Atlas v0.3.
"""

NEW_REGIONS = [
    {
        "id": "thalamus",
        "label": "Thalamus & epithalamus",
        "entity": "thalamus",
        "query": "(\"thalamus\"[tiab] OR thalamocortical[tiab] OR \"thalamic reticular\"[tiab] OR habenula[tiab] OR epithalamus[tiab] OR \"zona incerta\"[tiab] OR pulvinar[tiab])",
        "view": "thalamus",
        "views": ["atlas", "scales", "gaps", "lab", "library"],
        "levelDesc": {
            "regional": "Nuclei, nuclear groups & epithalamus",
            "circuit": "First-order vs higher-order, core vs matrix, TRN gain control",
            "cellular": "Relay projection neurons, local interneurons, TRN pacemakers"
        },
        "intro": {
            "title": "The thalamus & epithalamus: driver and modulator gateway",
            "text": "The central sensory, motor and cognitive relay and synchronizing hub of the forebrain. Organized along two orthogonal axes: driver source (first-order subcortical vs higher-order cortical L5B transthalamic) and cortical termination (focal L4 core vs diffuse L1 matrix), regulated by the inhibitory thalamic reticular nucleus and epithalamic habenular circuits."
        },
        "speciesNote": {
            "human": "Human: thalamus, subthalamic nucleus and epithalamus from the Allen Human 3D reference atlas.",
            "mouse": "Mouse: Allen CCFv3 parcellation of VM, VAL, MD, PF, LGd, MG, LP, PVT, TRN and habenula.",
            "macaque": "Macaque: SARM subcortical atlas parcellation of VA, VLa, VLp, MD, CMn-PF, Pulvinar and RT."
        }
    },
    {
        "id": "hypothalamus",
        "label": "Hypothalamus",
        "entity": "hypothalamus",
        "query": "(hypothalam*[tiab] OR \"preoptic area\"[tiab] OR suprachiasmatic[tiab] OR \"arcuate nucleus\"[tiab] OR \"ventromedial hypothalamus\"[tiab] OR \"lateral hypothalamus\"[tiab] OR mammillary[tiab])",
        "view": "hypothalamus",
        "views": ["atlas", "scales", "gaps", "lab", "library"],
        "levelDesc": {
            "regional": "Preoptic, anterior, tuberal and mammillary zones",
            "circuit": "Peptidergic survival circuits, neuroendocrine axes, circadian gating",
            "cellular": "Molecularly defined peptidergic and fast amino-acid neurons (HypoMap)"
        },
        "intro": {
            "title": "The hypothalamus: master coordinator of homeostasis and survival",
            "text": "Spans 4 rostrocaudal zones (preoptic, supraoptic/anterior, tuberal, mammillary) and 3 mediolateral zones. Integrates circadian rhythms, energy balance, thermoregulation, defensive escape, parenting, sexual behavior and autonomic/neuroendocrine outflow."
        },
        "speciesNote": {
            "human": "Human: hypothalamic region from the Allen Human reference atlas.",
            "mouse": "Mouse: Allen CCFv3 parcellation of MPO, SCN, PVH, ARH, VMH, DMH, LHA, MM and TMN.",
            "macaque": "Macaque: SARM subcortical atlas parcellation of preoptic, supraoptic, tuberal and mammillary nuclei."
        }
    },
    {
        "id": "colliculi",
        "label": "Colliculi & midbrain tectum",
        "entity": "tectum",
        "query": "(collicul*[tiab] OR \"superior colliculus\"[tiab] OR \"inferior colliculus\"[tiab] OR tectum[tiab] OR \"periaqueductal gray\"[tiab] OR \"mesencephalic locomotor\"[tiab])",
        "view": "colliculi",
        "views": ["atlas", "scales", "gaps", "lab", "library"],
        "levelDesc": {
            "regional": "Superior colliculus, inferior colliculus, PAG and MLR",
            "circuit": "Superficial retinotopic/tonotopic sensory layers vs deep multimodal/motor decision columns",
            "cellular": "Narrow-field/wide-field vertical, disc tonotopic, VIP/NPY IC projection, Chx10 vlPAG"
        },
        "intro": {
            "title": "Midbrain tectum & tegmentum: multimodal orienting, acoustic maps and survival decisions",
            "text": "The corpora quadrigemina (superior and inferior colliculi) and periaqueductal gray (PAG) form an evolutionarily conserved sensorimotor decision network: transforming visual, auditory and somatosensory inputs into gaze orienting, prey capture, acoustic localization, active escape and passive freezing."
        },
        "speciesNote": {
            "human": "Human: superior and inferior colliculi and periaqueductal gray from the Allen Human reference atlas.",
            "mouse": "Mouse: Allen CCFv3 superior colliculus (superficial vs deep), inferior colliculus, PAG and cuneiform nucleus.",
            "macaque": "Macaque: SARM subcortical atlas parcellation of SC, IC, PAG and tegmental nuclei."
        }
    }
]
