#!/usr/bin/env python3
"""Octopus audit fixes (applied once). Each wording now matches its abstract:

- bidel2023: ~25 million is the vertical lobe's cell count (simple amacrines are 89.3% of it), not the amacrine count;
- shomrat2010: 5-HT-immunoreactive terminals innervate the neuropil and applied 5-HT facilitates (terminals themselves
  were not shown to facilitate);
- pophale2023: activity during active sleep is strongest in the superior frontal and vertical lobes among the regions
  recorded (not "most active during active sleep");
- sternmentch2022: output neurons label for GABA and co-express FMRFamide-like peptides ("many" is not in the abstract);
- saidel1982: the optic lobe projects to the lateral basal lobe (not "back"); its many central inputs make the medulla
  an integrative area;
- wangzy2018: the catecholamine, steroid, insulin and feeding-peptide changes come across behavioural stages;
- sumbre2006: only the medial joint is set where the two waves collide;
- olson2025b: the sucker ganglion has cells expressing sensory and motor markers, with fibres to the oral roots that
  extend to the axial nerve cord; olson2025: nerves form a topographic map of the suckers;
- deryckere2021: the squid comparison is about progenitor location, the long migration about vertebrates;
- hochner2012: behaviour emerges from the octopus's embodied organization (no "environment" in the abstract).
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
KP, PP = ROOT / 'data/knowledge.json', ROOT / 'data/papers.json'
kb = json.loads(KP.read_text(encoding='utf-8'))
papers = json.loads(PP.read_text(encoding='utf-8'))
E = {e['id']: e for e in kb['entities']}
LK = {f"{l['s']}>{l['t']}": l for l in kb['links']}
CH = {c['id']: c for c in kb['chains']}
QU = {q['id']: q for q in kb['questions']}
CI = {c['id']: c for c in kb['atlas3d']['circuits']}
PA = {p['key']: p for p in papers}


def sub(obj, field, old, new):
    assert obj[field].count(old) == 1, (field, old)
    obj[field] = obj[field].replace(old, new)


sub(E['oct-vl'], 'summary', 'About 1.8 million input axons sparsely innervate some 25 million amacrine interneurons (octopus), and serotonin-containing terminals in its neuropil facilitate transmission and LTP induction (octopus).',
    'About 1.8 million input axons sparsely innervate its amacrine interneurons, which make up most of its roughly 25 million cells (octopus); serotonin-immunoreactive terminals innervate its neuropil, and applied 5-HT facilitates transmission and LTP induction (octopus).')
sub(E['oct-vl'], 'summary', 'and with the superior frontal lobe it is most active during active sleep (octopus).',
    'and during active sleep its activity, with that of the superior frontal lobe, is the strongest of the brain regions recorded (octopus).')
sub(E['oct-sfl'], 'summary', 'and with the vertical lobe it shows the strongest wake-like activity in active sleep and spindle-like oscillations in quiet sleep (octopus).',
    'and during active sleep its activity, with that of the vertical lobe, is the strongest of the brain regions recorded, while in quiet sleep both generate oscillations resembling sleep spindles (octopus).')
sub(E['oct-vl-am'], 'summary', 'Simple amacrine cells (89.3% of about 25 million cells)', "Simple amacrine cells (89.3% of the lobe's roughly 25 million cells)")
sub(E['oct-vl-ln'], 'summary', 'Many contain GABA together with FMRFamide-like neuropeptides, suggesting an inhibitory output with a neuromodulatory role, and a group is glutamatergic (octopus).',
    'Their cell bodies label for GABA, suggesting an inhibitory output, and they co-express FMRFamide-like neuropeptides, suggesting a neuromodulatory role as well; a group of them is glutamatergic (octopus).')
sub(E['oct-basal'], 'summary', 'send input to the optic lobe, which sends fibres back to the lateral basal lobe (octopus).',
    'send input to the optic lobe, and the optic lobe sends fibres to the lateral basal lobe (octopus).')
sub(E['oct-ol'], 'summary', 'Its medulla receives input from many higher motor and associative lobes, the contralateral optic lobe and the retina (octopus).',
    'It receives input from the retina, the contralateral optic lobe and many higher motor and associative centres, which makes its medulla an exceptionally complex integrative area (octopus).')
sub(E['oct-optic-gland'], 'summary', 'After mating it shifts catecholamine, steroid, insulin and feeding-peptide signalling and raises synthesis of pregnane steroids, 7-dehydrocholesterol and bile acid intermediates (octopus)',
    'Across reproductive stages it up- and downregulates catecholamine, steroid, insulin and feeding-peptide pathways (octopus), after reproduction it raises synthesis of pregnane steroids, 7-dehydrocholesterol and bile acid intermediates (octopus)')
sub(E['oct-arm-ns'], 'summary', 'and fetching food uses three dynamic joints set where two waves of muscle activation collide (octopus).',
    'and fetching food uses three dynamic joints, the middle one set where two waves of muscle activation collide (octopus).')
sub(E['oct-arm-ns'], 'summary', "The arms' flexibility is argued to have shaped an embodied organization, in which intelligent behaviour emerges from the interplay of brain, body and environment (review).",
    "The arms' flexibility is argued to have shaped unique brain-body-behaviour relationships, in which intelligent behaviour emerges from the octopus's embodied organization (review).")
sub(E['oct-sucker'], 'summary', "A ganglion in each sucker's stalk contains sensory and motor neurons and sends fibres to the sucker muscles and to the axial nerve cord, suggesting local reflexes for each sucker (octopus).",
    "A ganglion in each sucker's stalk has cells expressing sensory and motor neuron markers and sends fibres to the sucker muscles and to the oral roots that extend to the axial nerve cord, suggesting local reflexes for each sucker (octopus).")

sub(LK['oct-vl>f-sleep'], 'rel', 'with the superior frontal lobe, strongest wake-like activity in active sleep and spindle-like oscillations in quiet sleep (high-density recordings) (octopus)',
    'during active sleep, whose brain activity resembles waking, its activity is the strongest of the regions recorded, with the superior frontal lobe; in quiet sleep both generate spindle-like oscillations (high-density recordings) (octopus)')
sub(LK['oct-sfl>f-sleep'], 'rel', 'with the vertical lobe, strongest wake-like activity in active sleep and spindle-like oscillations in quiet sleep (high-density recordings) (octopus)',
    'during active sleep, whose brain activity resembles waking, its activity is the strongest of the regions recorded, with the vertical lobe; in quiet sleep both generate spindle-like oscillations (high-density recordings) (octopus)')
sub(LK['oct-arm-ns>f-motor'], 'rel', 'and fetching uses joints set where two waves of muscle activation collide (octopus)',
    'and fetching sets its middle joint where two waves of muscle activation collide (octopus)')
sub(LK['oct-sucker>oct-arm-ns'], 'rel', "each sucker’s ganglion sends fibres to the oral roots of the axial nerve cord, whose segments map the suckers in order (‘suckerotopy’) (octopus)",
    "each sucker’s ganglion sends fibres to the oral roots that extend to the axial nerve cord, whose nerves form a topographic map of the suckers (‘suckerotopy’) (octopus)")
sub(LK['oct-optic-gland>f-reproduction'], 'rel', 'after mating they shift steroid, catecholamine, insulin and feeding-peptide signalling (octopus)',
    'across reproductive stages they up- and downregulate steroid, catecholamine, insulin and feeding-peptide pathways (octopus)')

sub(CH['oct-fan'], 'desc', 'innervate some 25 million amacrine interneurons, which converge sharply onto large output neurons',
    "innervate the amacrine interneurons, most of the lobe's roughly 25 million cells, which converge sharply onto large output neurons")
sub(CI['oct-arms'], 'desc', 'and each sucker’s ganglion feeds the arm’s nerve cord (octopus).',
    'and each sucker’s ganglion sends fibres toward the arm’s nerve cord (octopus).')
sub(QU['q-oct-optic-gland'], 'text', 'After mating the glands raise pregnane steroids, 7-dehydrocholesterol and bile acid intermediates and shift catecholamine, insulin and feeding-peptide pathways (wang2022, wangzy2018),',
    'After reproduction the glands raise synthesis of pregnane steroids, 7-dehydrocholesterol and bile acid intermediates (wang2022), across reproductive stages they up- and downregulate catecholamine, insulin and feeding-peptide pathways (wangzy2018),')

sub(PA['bidel2023'], 'finding', 'simple amacrine cells (89.3% of about 25 million cells)', "simple amacrine cells (89.3% of the lobe's roughly 25 million cells)")
sub(PA['deryckere2021'], 'finding', 'and lineage tracing showed that their progeny generate neurons for the different lobes, migrating over long distances, as in the squid Doryteuthis pealeii (octopus).',
    'and lineage tracing showed that, depending on their location in the lips, progenitors generate neurons for the different lobes, as in the squid Doryteuthis pealeii, and that newborn neurons migrate over long distances, reminiscent of vertebrate neurogenesis (octopus).')

KP.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
PP.write_text(json.dumps(papers, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('octopus audit fixes applied')
