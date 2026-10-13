# -*- coding: utf-8 -*-
"""Checks over the pronoun deck.

The strong check: take only what the *prompt* gives the learner — the
English gloss, the kind of pronoun wanted, and (for δικός) the agreement
named in the explanation — re-derive the pronoun from the paradigm tables,
and require it to equal what the answer actually has. A card that fails
this is one a learner could not solve from the prompt.
"""
from __future__ import print_function
import io, re, sys, collections

from greeklex import deaccent
from pron import (PERSONS, PINFO, STRONG_NOM, STRONG_ACC, WEAK_GEN, TAG,
                  TTAG, TABLES, weak_acc, dikos, cap)

CASE_OF = {u'nominative': 'nom', u'accusative': 'acc', u'genitive': 'gen'}
NUM_OF = {u'singular': 'sg', u'plural': 'pl'}
GEN_OF = {u'masculine': 'm', u'feminine': 'f', u'neuter': 'n'}
ORD_OF = {u'1st': 1, u'2nd': 2, u'3rd': 3}

# every gloss the prompt can carry, mapped back to the referent it names
GLOSS = {}
for _kind, _table in TABLES.items():
    _tag = TTAG if _kind.startswith('t') else TAG
    for _key in _table:
        if _key not in _tag:
            continue
        GLOSS.setdefault(_kind, {})[_table[_key] + _tag[_key]] = _key

# the pronoun kind named in the prompt -> (which gloss table, which job)
KIND = {
    u'strong subject pronoun': (('subj', 'tsubj'), 'nom_strong'),
    u'weak pronoun, direct object': (('obj', 'tobj'), 'acc_weak'),
    u'strong pronoun after a preposition': (('obj',), 'acc_strong'),
    u'strong pronoun, emphatic object': (('obj',), 'acc_strong'),
    u'weak pronoun, indirect object': (('obj',), 'gen_weak'),
    u'weak pronoun with αρέσει': (('obj',), 'gen_weak'),
    u'weak possessive': (('poss',), 'gen_weak'),
    u'emphatic δικός-type possessive': ((), 'dikos'),
}

PROMPT = re.compile(u'^(.*?___.*?) \\((.+?) - (.+)\\)$')
LABEL = re.compile(u'(1st|2nd|3rd) person (?:(masculine|feminine|neuter) )?'
                   u'(nominative|accusative|genitive) (singular|plural)')
AGREE = re.compile(u'(masculine|feminine|neuter) '
                   u'(nominative|accusative|genitive) (singular|plural) '
                   u'to agree with (\\S+), with the weak genitive (\\S+)')
LATIN = re.compile(u'[A-Za-z]')

path = sys.argv[1] if len(sys.argv) > 1 else 'deck.txt'
text = io.open(path, 'rb').read().decode('utf-8-sig').replace('\r\n', '\n')
blocks = [b.strip('\n') for b in text.strip('\n').split('\n\n') if b.strip()]

errs = collections.Counter()


def bad(kind, detail):
    errs[kind] += 1
    if errs[kind] <= 3:
        print(u'[%s] %s' % (kind, detail))


seen = set()
cases = collections.Counter()
nums = collections.Counter()

for i, b in enumerate(blocks, 1):
    L = b.split('\n')
    if len(L) != 4:
        bad('lines', u'card %d has %d lines' % (i, len(L)))
        continue
    num, prompt, answer, english = L
    if num != str(i):
        bad('number', u'card %d numbered %s' % (i, num))

    m = PROMPT.match(prompt)
    if not m:
        bad('prompt', u'card %d: %s' % (i, prompt))
        continue
    sentence, gl, kind_name = m.groups()
    if sentence.count('___') != 1:
        bad('blank', u'card %d: %s' % (i, sentence))
    if prompt in seen:
        bad('dup', u'card %d: %s' % (i, prompt))
    seen.add(prompt)
    if kind_name not in KIND:
        bad('kind', u'card %d: %s' % (i, kind_name))
        continue
    table, job = KIND[kind_name]

    if u' — ' not in english:
        bad('expl', u'card %d has no explanation' % i)
        continue
    en, expl = english.split(u' — ', 1)

    # ---- what the learner actually wrote in the gap ----------------------
    pre, post = sentence.split('___')
    if not answer.startswith(pre) or not answer.endswith(post):
        bad('frame', u'card %d: %r does not fit %r' % (i, answer, sentence))
        continue
    got = answer[len(pre):len(answer) - len(post)]

    # ---- rebuild it from the prompt --------------------------------------
    if job == 'dikos':
        am = AGREE.search(expl)
        if not am:
            bad('agree', u'card %d: no agreement in %s' % (i, expl))
            continue
        g_en, case_en, num_en, head, clitic = am.groups()
        # the gloss is 'my own' / 'mine' and friends
        key = GLOSS['own'].get(gl) or GLOSS['mine'].get(gl)
        if key is None:
            bad('gloss', u'card %d: %s' % (i, gl))
            continue
        if WEAK_GEN[key] != clitic:
            bad('clitic', u'card %d: %s vs %s' % (i, WEAK_GEN[key], clitic))
        want = u'%s %s' % (dikos(GEN_OF[g_en], CASE_OF[case_en],
                                 NUM_OF[num_en]), WEAK_GEN[key])
        case, number = CASE_OF[case_en], PINFO[key][1]
        if head not in answer:
            bad('head', u'card %d: %s not in the answer' % (i, head))
    else:
        if gl.startswith(u'to '):
            gl = gl[3:]
        key = None
        for _t in table:
            key = GLOSS[_t].get(gl)
            if key is not None:
                break
        if key is None:
            bad('gloss', u'card %d: %r (%s)' % (i, gl, table))
            continue
        lm = LABEL.search(expl)
        if not lm:
            bad('label', u'card %d: %s' % (i, expl))
            continue
        ord_en, g_en, case_en, num_en = lm.groups()
        case, number = CASE_OF[case_en], NUM_OF[num_en]
        p, n, g = PINFO[key]
        if ORD_OF[ord_en] != p or n != number:
            bad('person', u'card %d: gloss %s vs label %s' % (i, key, lm.group(0)))
        if (GEN_OF[g_en] if g_en else None) != g:
            bad('gender', u'card %d: gloss %s vs label %s' % (i, key, lm.group(0)))
        if job == 'nom_strong':
            want = STRONG_NOM[key]
        elif job == 'acc_strong':
            want = STRONG_ACC[key]
        elif job == 'acc_weak':
            # the final -ν of την depends on the word that follows
            nxt = post.strip().split(' ')[0] if post.strip() else u''
            want = weak_acc(key, nxt)
        else:
            want = WEAK_GEN[key]

    if got != want and got != cap(want):
        bad('derive', u'card %d: answer %r, derived %r' % (i, got, want))

    cases[case] += 1
    nums[number] += 1

    # ---- surface -------------------------------------------------------
    if not en[0].isupper() or en[-1] not in u'.?!':
        bad('ensurface', u'card %d: %s' % (i, en))
    if u'  ' in en or u'  ' in answer or u' .' in answer or u' ,' in answer:
        bad('space', u'card %d: %r' % (i, answer))
    if LATIN.search(answer):
        bad('latin', u'card %d: %s' % (i, answer))
    if not answer[0].isupper():
        bad('cap', u'card %d: %s' % (i, answer))
    if answer[-1] not in u'.;!':
        bad('stop', u'card %d: %s' % (i, answer))

print(u'cards : %d' % len(blocks))
print(u'case  : %s' % dict(cases))
print(u'number: %s' % dict(nums))
print(u'errors: %s' % (dict(errs) if errs else 'none'))
sys.exit(1 if errs else 0)
