#!/usr/bin/env python3
"""Amygdala audit fixes, part 2 (2026-11-04, cloud session, checked against the PubMed abstracts).

  - kalin2004: the abstract concludes only that the CeA "plays a role" ("results suggest"); state what the
    bilateral lesions changed and hedge the conclusion (f-anxiety, cea>f-anxiety).
  - knobloch2012: in vitro, light on oxytocin axons activated the local GABAergic circuit that inhibited neurons in the
    CeA output region; in vivo, evoked oxytocin release decreased freezing (oxytocin, oxytocin>cea, amy-oxytocin).
  - adolphs2005: the impairment stems from not making normal use of the eye region, which the authors trace to a lack
    of spontaneous fixations on the eyes (f-social, amygdala>f-social).
  - demartino2010: two people, not a general rule (f-valence, amygdala>f-valence).
  - herry2008: transitions are triggered by a switch in the balance of activity between two populations (bla>f-fear).
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


def sub(obj, field, old, new):
    s = obj[field]
    assert s.count(old) == 1, (field, old[:70], s.count(old))
    obj[field] = s.replace(old, new)


# kalin2004
sub(E['f-anxiety'], 'summary',
    'Bilateral central amygdala lesions reduce fear- and anxiety-related behavioral and endocrine responses (monkey).',
    'Bilateral central amygdala lesions reduce fear-related behavior toward a snake and freezing toward a human intruder and lower cerebrospinal fluid CRF and plasma ACTH, which suggests that the central amygdala plays a role in fear- and anxiety-related behavioral and endocrine responses (monkey).')
sub(L['cea>f-anxiety'], 'rel',
    'bilateral lesions reduce fear- and anxiety-related behavioral and pituitary–adrenal responses (monkey)',
    'bilateral lesions reduce fear-related behavior and freezing toward a human intruder and lower cerebrospinal fluid CRF and plasma ACTH, suggesting a role in fear- and anxiety-related behavioral and pituitary–adrenal responses (monkey)')

# knobloch2012
sub(E['oxytocin'], 'summary',
    'where evoked oxytocin release activates a local GABAergic circuit and decreases freezing in fear-conditioned rats;',
    'where stimulating these axons activates a local GABAergic circuit (in vitro) and evoked oxytocin release decreases freezing in fear-conditioned rats;')
sub(L['oxytocin>cea'], 'rel',
    'oxytocin released from hypothalamic axons activates a local GABAergic circuit that inhibits central amygdala output neurons (in vitro) and decreases freezing;',
    'stimulating hypothalamic oxytocin axons activates a local GABAergic circuit that inhibits neurons in the central amygdala output region (in vitro), and evoked oxytocin release there decreases freezing;')
sub(C['amy-oxytocin'], 'desc',
    'Oxytocin released from hypothalamic axons activates a local GABAergic circuit in the central amygdala that inhibits its output neurons (in vitro), and decreases freezing in fear-conditioned rats without affecting the cardiovascular response.',
    'Stimulating hypothalamic oxytocin axons in the central amygdala activates a local GABAergic circuit that inhibits neurons in its output region (in vitro), and evoked oxytocin release there decreases freezing in fear-conditioned rats; oxytocin decreases freezing without affecting the cardiovascular response (rat).')

# adolphs2005
sub(E['f-social'], 'summary',
    'In patient SM, impaired recognition of fear stems from a lack of spontaneous fixations on the eyes,',
    'In patient SM, impaired recognition of fear stems from not making normal use of the eye region of faces, which the authors trace to a lack of spontaneous fixations on the eyes,')
sub(L['amygdala>f-social'], 'rel',
    'and in patient SM impaired fear recognition stems from a lack of spontaneous fixations on the eyes (human)',
    'and in patient SM impaired fear recognition stems from not making normal use of the eye region of faces (human)')

# demartino2010
sub(E['f-valence'], 'summary',
    'People with focal bilateral amygdala lesions show a dramatic reduction in loss aversion in monetary gambles (human).',
    'Two people with focal bilateral amygdala lesions showed a dramatic reduction in loss aversion in monetary gambles (human).')
sub(L['amygdala>f-valence'], 'rel',
    'and focal bilateral lesions dramatically reduce loss aversion in monetary gambles (human)',
    'and two people with focal bilateral lesions showed a dramatic reduction in loss aversion in monetary gambles (human)')

# herry2008
sub(L['bla>f-fear'], 'rel',
    'two populations of basal amygdala neurons switch activity between high fear (renewal) and low fear (extinction), and inactivating the basal amygdala prevents these transitions;',
    'transitions between high fear (renewal) and low fear (extinction) are triggered by a switch in the balance of activity between two populations of basal amygdala neurons, and inactivating the basal amygdala prevents them;')

P.write_text(json.dumps(kb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('applied 10 fixes; run tools/jsonfmt.py and tools/build.py --offline next')
