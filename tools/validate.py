# -*- coding: utf-8 -*-
"""Checks over the generated deck.

The strong check: take only what the *prompt* gives the learner (adjective,
noun, definiteness, number) plus the case named in the explanation, re-derive
the whole noun phrase from the paradigms, and require it to equal the answer.
A card that fails this is one a learner could not solve.
"""
import io, re, sys, collections
from greeklex import (decline_noun, decline_adj, definite, indefinite,
                      keeps_nu, deaccent)
from data2 import NOUNS, ADJS

# a lemma can carry two genders (ο γιατρός / η γιατρός), so key on both
GLETTER = {'M': 'm', 'F': 'f', 'N': 'n'}
NOUN = dict(((g, GLETTER[cls[0]]), (cls, tag, en, enpl))
            for (g, cls, tag, en, enpl) in NOUNS)
ADJ = dict((a[0], a[1]) for a in ADJS)
GENDER = {'M': 'm', 'F': 'f', 'N': 'n'}
CASE = {u'nominative': 'nom', u'accusative': 'acc', u'genitive': 'gen'}
NUM = {u'singular': 'sg', u'plural': 'pl'}

HINT = re.compile(u'^(.*?___.*?) \\((\\S+) \\+ (\\S+) (\\S+) - '
                  u'(definite|indefinite), (singular|plural)\\)$')
FORM = re.compile(u'(masculine|feminine|neuter) '
                  u'(nominative|accusative|genitive) (singular|plural)')
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
for i, b in enumerate(blocks, 1):
    L = b.split('\n')
    if len(L) != 4:
        bad('lines', u'card %d has %d lines' % (i, len(L)))
        continue
    num, prompt, answer, english = L
    if num != str(i):
        bad('number', u'card %d numbered %s' % (i, num))

    m = HINT.match(prompt)
    if not m:
        bad('prompt', u'card %d: %s' % (i, prompt))
        continue
    sentence, adj, art_cite, noun, definiteness, number = m.groups()

    if sentence.count('___') != 1:
        bad('blank', u'card %d: %s' % (i, sentence))
    if prompt in seen:
        bad('dup', u'card %d: %s' % (i, prompt))
    seen.add(prompt)
    if adj not in ADJ:
        bad('adj', u'card %d: unknown adjective %s' % (i, adj))
        continue
    if not any((noun, x) in NOUN for x in 'mfn'):
        bad('noun', u'card %d: unknown noun %s' % (i, noun))
        continue

    if u' — ' not in english:
        bad('expl', u'card %d has no explanation' % i)
        continue
    en, expl = english.split(u' — ', 1)
    fm = FORM.search(expl)
    if not fm:
        bad('form', u'card %d: no gender/case/number in explanation' % i)
        continue
    gender_en, case_en, number_en = fm.groups()

    # the prompt and the explanation must agree about the number
    if number_en != number:
        bad('numclash', u'card %d: prompt says %s, explanation %s'
            % (i, number, number_en))
    stated_def = u'definite' if u'definite article' in expl and \
        u'indefinite article' not in expl else u'indefinite'
    if stated_def != definiteness:
        bad('defclash', u'card %d: prompt says %s, explanation %s'
            % (i, definiteness, stated_def))

    # ---- rebuild the phrase from the prompt alone ------------------------
    # gender comes from the citation article in the prompt, which is the only
    # thing telling the learner which of ο/η γιατρός is meant
    g = {u'ο': 'm', u'η': 'f', u'το': 'n'}.get(art_cite)
    if g is None or (noun, g) not in NOUN:
        bad('cite', u'card %d: %s %s' % (i, art_cite, noun))
        continue
    cls, tag, en_sg, en_pl = NOUN[(noun, g)]
    case, nu = CASE[case_en], NUM[number]
    if g != {'masculine': 'm', 'feminine': 'f', 'neuter': 'n'}[gender_en]:
        bad('gender', u'card %d: prompt says %s, explanation %s'
            % (i, art_cite, gender_en))
    forms = decline_noun(noun, cls)
    if (case, nu) not in forms:
        bad('noform', u'card %d: %s has no %s %s' % (i, noun, case, nu))
        continue
    noun_f = forms[(case, nu)]
    adj_f = decline_adj(adj, ADJ[adj], g, case, nu)
    art_f = (definite(g, case, nu, adj_f) if definiteness == u'definite'
             else indefinite(g, case, adj_f))
    want = u'%s %s %s' % (art_f, adj_f, noun_f)

    pre, suf = sentence.split('___')
    if not answer.startswith(pre) or not answer.endswith(suf):
        bad('frame', u'card %d: %r does not fit %r' % (i, answer, sentence))
        continue
    got = answer[len(pre):len(answer) - len(suf)] if suf else answer[len(pre):]
    if got != want and got != want[0].upper() + want[1:]:
        bad('derive', u'card %d: answer %r, derived %r' % (i, got, want))

    # english surface
    if not en[0].isupper() or en[-1] not in u'.?!':
        bad('ensurface', u'card %d: %s' % (i, en))
    if '  ' in en or '  ' in answer:
        bad('space', u'card %d' % i)
    if LATIN.search(answer):
        bad('latin', u'card %d: %s' % (i, answer))
    # the english head noun must follow the stated number
    head = en_pl if nu == 'pl' else en_sg
    if head and head not in en:
        bad('enhead', u'card %d: %r not in %r' % (i, head, en))

print(u'cards: %d' % len(blocks))
print(u'errors: %s' % (dict(errs) if errs else 'none'))
sys.exit(1 if errs else 0)
