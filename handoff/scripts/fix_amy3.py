#!/usr/bin/env python3
"""Amygdala audit fixes, part 1 (2026-11-04, cloud session; no abstracts available).

Each new amygdala sentence was read against the one-sentence findings of the papers it cites. These fixes bring the
wording back to what the findings (themselves checked against the abstracts while drafting) support:
  - single-patient case reports (adolphs1994, feinstein2011) were written as general rules ("bilateral amygdala damage
    impairs ..."); now "a patient with ...";
  - hong2014: "a GABAergic subpopulation" and "two other social behaviors", as in the finding;
  - knobloch2012: the inhibition of central amygdala output neurons was shown in vitro;
  - kirsch2005: "visual stimuli", not "pictures";
  - amy-fear circuit: ledoux1988 says the projections "appear to mediate"; the mouse result is tovote2016's.
Applied once; asserts that every old string is present exactly once.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
P = ROOT / 'data/knowledge.json'
kb = json.loads(P.read_text(encoding='utf-8'))
E = {e['id']: e for e in kb['entities']}
L = {f"{l['s']}>{l['t']}": l for l in kb['links']}
C = {c['id']: c for c in kb['chains']}
CI = {c['id']: c for c in kb['atlas3d']['circuits']}


def sub(obj, field, old, new):
    s = obj[field]
    assert s.count(old) == 1, (field, old[:70], s.count(old))
    obj[field] = s.replace(old, new)


# --- one patient, not a general rule
sub(E['f-social'], 'summary',
    'Selective bilateral amygdala damage impairs recognizing fear in faces, which in patient SM stems from a lack of spontaneous fixations on the eyes; her recognition of fearful faces became normal when she was told to look at the eyes (human).',
    'A patient with selective bilateral amygdala damage was impaired at recognizing fear in facial expressions (human). In patient SM, impaired recognition of fear stems from a lack of spontaneous fixations on the eyes, and her recognition of fearful faces became normal when she was told to look at the eyes (human).')
sub(E['f-emotion'], 'summary',
    'Selective bilateral amygdala damage impairs the recognition of fear in facial expressions (human), and the amygdala',
    'A patient with selective bilateral amygdala damage was impaired at recognizing fear in facial expressions (human), and the amygdala')
sub(L['amygdala>f-emotion'], 'rel',
    'fear and affect: bilateral amygdala damage impairs recognizing fear in faces and the experience of fear, and the amygdala responds more to fearful than to happy faces (human)',
    'fear and affect: a patient with selective bilateral amygdala damage was impaired at recognizing fear in faces, a patient with focal bilateral amygdala lesions showed an impoverished experience of fear, and the left amygdala responds more to fearful than to happy faces (human)')
sub(L['amygdala>f-social'], 'rel',
    'selective bilateral damage impairs recognizing fear in faces (human), which in patient SM stems from not looking at the eyes (human)',
    'a patient with selective bilateral damage was impaired at recognizing fear in faces, and in patient SM impaired fear recognition stems from a lack of spontaneous fixations on the eyes (human)')

# --- hong2014
sub(E['f-social'], 'summary',
    'In the medial amygdala, GABAergic neurons promote aggression and other social behaviors,',
    'In the medial amygdala, a GABAergic subpopulation promotes aggression and two other social behaviors,')
sub(L['mea>f-social'], 'rel',
    'a GABAergic subpopulation promotes aggression and other social behaviors,',
    'a GABAergic subpopulation promotes aggression and two other social behaviors,')

# --- knobloch2012: in vitro
sub(L['oxytocin>cea'], 'rel',
    'activates a local GABAergic circuit that inhibits central amygdala output neurons and decreases freezing;',
    'activates a local GABAergic circuit that inhibits central amygdala output neurons (in vitro) and decreases freezing;')
sub(C['amy-oxytocin'], 'desc',
    'activates a local GABAergic circuit in the central amygdala that inhibits its output neurons, and decreases freezing',
    'activates a local GABAergic circuit in the central amygdala that inhibits its output neurons (in vitro), and decreases freezing')

# --- kirsch2005
sub(L['oxytocin>amygdala'], 'rel', 'by fear-inducing pictures', 'by fear-inducing visual stimuli')

# --- amy-fear circuit: ledoux1988 "appear to mediate"; tovote2016 for the mouse
sub(CI['amy-fear'], 'desc',
    'Central amygdala projections to the periaqueductal gray and the lateral hypothalamus mediate freezing and the conditioned arterial pressure response (rat, mouse).',
    'Its projections to the periaqueductal gray and the lateral hypothalamus appear to mediate freezing and the conditioned arterial pressure response (rat), and an inhibitory pathway to the ventrolateral periaqueductal gray produces freezing (mouse).')

P.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('applied 11 fixes; run tools/jsonfmt.py and tools/build.py --offline next')
