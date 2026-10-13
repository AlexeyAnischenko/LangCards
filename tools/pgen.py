# -*- coding: utf-8 -*-
"""Builds every candidate card for the pronoun deck.

The selector in pbuild.py then picks the final set. Two rules run through
all of it: a frame about people never asks for a neuter pronoun, and a
frame about things runs in the third person only and glosses every gender
as English "it".
"""
from __future__ import print_function
import collections

from greeklex import decline_noun, decline_adj, definite, indefinite
from data2 import NOUNS, ADJS
from groups import GROUPS
from pron import (PERSONS, PINFO, STRONG_NOM, STRONG_ACC, WEAK_GEN, DEM,
                  weak_acc, dikos, gloss, en_of, label, conjugate, en_verb,
                  cap, se_art)
import frames as F

GL = {'M': 'm', 'F': 'f', 'N': 'n'}
ADJ_FV = dict((a[0], a[1]) for a in ADJS)
PORDER = [k for (k, p, n, g) in PERSONS]
HUMAN = [k for (k, p, n, g) in PERSONS if g != 'n']        # 8 keys, 4 + 4
THING = [k for (k, p, n, g) in PERSONS if p == 3]          # 6 keys, 3 + 3


class Noun(object):
    def __init__(self, gr, cls, tag, en_sg, en_pl):
        self.gr, self.cls, self.tag = gr, cls, tag
        self.g = GL[cls[0]]
        self.en_sg, self.en_pl = en_sg, en_pl
        self.forms = decline_noun(gr, cls)
        self.key = (gr, self.g)

    def has(self, case, num):
        if num == 'pl' and not self.en_pl:
            return False
        return (case, num) in self.forms

    def form(self, case, num):
        return self.forms[(case, num)]

    def en(self, num):
        return self.en_pl if num == 'pl' else self.en_sg

    def np(self, case, num, art='def'):
        f = self.form(case, num)
        if art == 'def':
            return definite(self.g, case, num, f) + u' ' + f
        if art == 'indef':
            return indefinite(self.g, case, f) + u' ' + f
        return f

    def np_en(self, num, art='def'):
        head = self.en(num)
        if art == 'def':
            return u'the ' + head
        if art == 'indef':
            return (u'an ' if head[0] in u'aeiou' else u'a ') + head
        return head


BY_KEY = {}
BY_LEMMA = collections.defaultdict(list)
for _gr, _cls, _tag, _es, _ep in NOUNS:
    n = Noun(_gr, _cls, _tag, _es, _ep)
    if n.key in BY_KEY:            # one entry per lemma+gender
        continue
    BY_KEY[n.key] = n
    BY_LEMMA[_gr].append(n)

POOLS = dict((name, [n for w in lemmas for n in BY_LEMMA[w]])
             for name, lemmas in GROUPS.items())

# nouns with no useful plural, whatever the lexicon says
MASS = set([u'ζάχαρη', u'αλεύρι', u'ρύζι', u'αλάτι', u'πιπέρι', u'μέλι',
            u'βούτυρο', u'ελαιόλαδο', u'ξύδι', u'ρίγανη', u'σκόρδο',
            u'καλαμπόκι'])

CARDS = []

HINT = {
    'nom_fix': ('subj', u'strong subject pronoun'),
    'nom_q': ('subj', u'strong subject pronoun'),
    'nom_be': ('subj', u'strong subject pronoun'),
    'nom_pred': ('subj', u'strong subject pronoun'),
    'nom_obj': ('subj', u'strong subject pronoun'),
    'nom_thing': ('tsubj', u'strong subject pronoun'),
    'nom_thing_pred': ('tsubj', u'strong subject pronoun'),
    'acc_weak': ('obj', u'weak pronoun, direct object'),
    'acc_weak_thing': ('tobj', u'weak pronoun, direct object'),
    'acc_weak_place': ('obj', u'weak pronoun, direct object'),
    'acc_prep': ('obj', u'strong pronoun after a preposition'),
    'acc_emph': ('obj', u'strong pronoun, emphatic object'),
    'gen_io': ('to_obj', u'weak pronoun, indirect object'),
    'gen_io_obj': ('to_obj', u'weak pronoun, indirect object'),
    'gen_aresei': ('to_obj', u'weak pronoun with αρέσει'),
    'gen_poss': ('poss', u'weak possessive'),
    'dikos_pred': ('mine', u'emphatic δικός-type possessive'),
    'dikos_nom': ('own', u'emphatic δικός-type possessive'),
    'dikos_acc': ('own', u'emphatic δικός-type possessive'),
    'dikos_gen': ('own', u'emphatic δικός-type possessive'),
}


def make_hint(family, key):
    kind, what = HINT[family]
    if kind == 'to_obj':
        return u'to %s - %s' % (gloss(key, 'obj'), what)
    return u'%s - %s' % (gloss(key, kind), what)


def tail(text):
    """Join a tail to the gap, unless it is punctuation."""
    return text if text[:1] in u'.;,' else u' ' + text


SEEN = set()


def add(family, case, key, fill, pre, post, en, expl, noun=None, frame=0):
    sentence = pre + u'___' + post
    answer = pre + (fill if pre else cap(fill)) + post
    # two frames can land on the same sentence; the first one wins
    stamp = (sentence, make_hint(family, key))
    if stamp in SEEN:
        return
    SEEN.add(stamp)
    CARDS.append({
        'family': family, 'case': case, 'key': key, 'num': PINFO[key][1],
        'fill': fill, 'prompt': sentence, 'answer': answer,
        'en': en, 'expl': expl, 'noun': noun, 'frame': frame,
        'hint': make_hint(family, key),
    })


def tidy(text):
    return cap(u' '.join(text.split()).replace(u' .', u'.'))


# --------------------------------------------------------------------------
# 1. nominative, strong subject pronoun
# --------------------------------------------------------------------------
def nom_note(key, verb_form, lead=u''):
    form = STRONG_NOM[key] if lead else cap(STRONG_NOM[key])
    return (u'%s → strong personal pronoun, %s — the subject of %s; Greek'
            u' leaves the subject pronoun out unless it is emphatic'
            % (form, label(key, 'nom', True), verb_form))


def build_nom_fix():
    for i, (vb, gtail, etail, glead, elead) in enumerate(F.NOM_FIX):
        grp, eb, e3 = F.VERBS[vb]
        for key in HUMAN:
            p, n, g = PINFO[key]
            v = conjugate(vb, grp, p, n)
            post = u' %s %s' % (v, gtail)
            en = tidy(u'%s%s %s %s' % (elead, en_of(key, 'subj'),
                                       en_verb(eb, e3, key), etail))
            add('nom_fix', 'nom', key, STRONG_NOM[key], glead, post, en,
                nom_note(key, v, glead), frame=i)


def build_nom_q():
    for i, (vb, gtail, etail, prog) in enumerate(F.NOM_Q):
        grp, eb, e3 = F.VERBS[vb]
        for key in HUMAN:
            p, n, g = PINFO[key]
            v = conjugate(vb, grp, p, n)
            if prog:
                aux = {1: u'Am', 2: u'Are', 3: u'Is'}[p] if n == 'sg' \
                    else u'Are'
                en = tidy(u'%s %s %s' % (aux, en_of(key, 'subj'), etail))
            else:
                aux = u'Does' if (p == 3 and n == 'sg') else u'Do'
                en = tidy(u'%s %s %s %s' % (aux, en_of(key, 'subj'), eb,
                                            etail))
            add('nom_q', 'nom', key, STRONG_NOM[key], u'',
                u' %s %s' % (v, gtail), en, nom_note(key, v), frame=i)


def build_nom_be():
    for i, (gtail, etail) in enumerate(F.NOM_BE):
        for key in HUMAN:
            p, n, g = PINFO[key]
            v = conjugate(u'είμαι', 'X', p, n)
            be = {1: u'am', 2: u'are', 3: u'is'}[p] if n == 'sg' else u'are'
            en = tidy(u'%s %s %s' % (en_of(key, 'subj'), be, etail))
            add('nom_be', 'nom', key, STRONG_NOM[key], u'',
                u' %s %s' % (v, gtail), en, nom_note(key, v), frame=i)


def build_nom_pred():
    for i, (adj, en_adj) in enumerate(F.NOM_PRED):
        for key in HUMAN:
            p, n, g = PINFO[key]
            if p != 3:
                continue
            v = conjugate(u'είμαι', 'X', p, n)
            a = decline_adj(adj, ADJ_FV[adj], g, 'nom', n)
            be = u'is' if n == 'sg' else u'are'
            en = tidy(u'%s %s %s.' % (en_of(key, 'subj'), be, en_adj))
            add('nom_pred', 'nom', key, STRONG_NOM[key], u'',
                u' %s %s.' % (v, a), en, nom_note(key, v), frame=i)


def build_nom_obj():
    for i, (vb, pool, art, gtail, etail) in enumerate(F.NOM_OBJ):
        grp, eb, e3 = F.VERBS[vb]
        for noun in POOLS[pool]:
            for num in ('sg', 'pl'):
                if not noun.has('acc', num):
                    continue
                if num == 'pl' and noun.gr in MASS:
                    continue
                if art == 'indef' and num == 'pl':
                    continue
                for key in HUMAN:
                    p, n, g = PINFO[key]
                    v = conjugate(vb, grp, p, n)
                    post = u' %s %s %s' % (v, noun.np('acc', num, art), gtail)
                    en = tidy(u'%s %s %s %s' % (en_of(key, 'subj'),
                                                en_verb(eb, e3, key),
                                                noun.np_en(num, art), etail))
                    add('nom_obj', 'nom', key, STRONG_NOM[key], u'', post,
                        en, nom_note(key, v), noun=noun.key, frame=i)


def build_nom_thing():
    for i, (vb, gtail, etail) in enumerate(F.NOM_THING):
        grp, eb, e3 = F.VERBS[vb]
        for key in THING:
            p, n, g = PINFO[key]
            v = conjugate(vb, grp, p, n)
            if vb == u'είμαι':
                ev = u'is' if n == 'sg' else u'are'
            else:
                ev = e3 if n == 'sg' else eb
            en = tidy(u'%s %s %s' % (en_of(key, 'tsubj'), ev, etail))
            add('nom_thing', 'nom', key, STRONG_NOM[key], u'',
                u' %s %s' % (v, gtail), en, nom_note(key, v), frame=i)


def build_nom_thing_pred():
    for i, (adj, en_adj) in enumerate(F.NOM_THING_PRED):
        for key in THING:
            p, n, g = PINFO[key]
            v = conjugate(u'είμαι', 'X', p, n)
            a = decline_adj(adj, ADJ_FV[adj], g, 'nom', n)
            be = u'is' if n == 'sg' else u'are'
            en = tidy(u'%s %s %s.' % (en_of(key, 'tsubj'), be, en_adj))
            add('nom_thing_pred', 'nom', key, STRONG_NOM[key], u'',
                u' %s %s.' % (v, a), en, nom_note(key, v), frame=i)


# --------------------------------------------------------------------------
# 2. accusative, weak object pronoun
# --------------------------------------------------------------------------
def acc_weak_note(key, form, verb_form):
    return (u'%s → weak personal pronoun, %s — the direct object of %s; the'
            u' weak form goes in front of the verb, never after it'
            % (form, label(key, 'acc', False), verb_form))


SUBJ_PERSON = {'1sg': 1, '1pl': 1, '2sg': 2, '2pl': 2, '3sg': 3, '3pl': 3}


def _subject_verb(vb, sp):
    grp, eb, e3 = F.VERBS[vb]
    p = SUBJ_PERSON[sp]
    n = 'sg' if sp.endswith('sg') else 'pl'
    return conjugate(vb, grp, p, n), eb, e3, p, (p == 3 and n == 'sg')


def _weak_rows(family, rows, keys, objkind, lead_en):
    for i, (lead, esubj, vb, sp, neg, gtail, etail) in enumerate(rows):
        v, eb, e3, sp_p, third = _subject_verb(vb, sp)
        subject = esubj or lead_en[lead]
        for key in keys:
            p, n, g = PINFO[key]
            if p == sp_p and p in (1, 2):      # 'I see me' is not a sentence
                continue
            form = weak_acc(key, v)
            obj = en_of(key, objkind)
            if neg:
                aux = u"doesn't" if third else u"don't"
                body = u'%s %s %s %s %s' % (subject, aux, eb, obj, etail)
            else:
                body = u'%s %s %s %s' % (subject, e3 if third else eb,
                                         obj, etail)
            add(family, 'acc', key, form, lead, u' %s%s' % (v, tail(gtail)),
                tidy(body), acc_weak_note(key, cap(form) if not lead
                                          else form, v), frame=i)


def build_acc_weak():
    _weak_rows('acc_weak', F.ACC_WEAK, HUMAN, 'obj', F.LEAD_EN)


def build_acc_weak_thing():
    _weak_rows('acc_weak_thing', F.ACC_WEAK_THING, THING, 'tobj', {})


def build_acc_weak_place():
    for i, (vb, sp, esubj) in enumerate(F.ACC_WEAK_PLACE):
        v, eb, e3, sp_p, third = _subject_verb(vb, sp)
        for noun in POOLS['venue']:
            for num in ('sg',):
                if not noun.has('acc', num):
                    continue
                head = noun.form('acc', num)
                place = u'%s %s' % (se_art(noun.g, num, head), head)
                for key in HUMAN:
                    p, n, g = PINFO[key]
                    if p == sp_p and p in (1, 2):
                        continue
                    form = weak_acc(key, v)
                    en = tidy(u'%s %s %s at %s.'
                              % (esubj, e3 if third else eb,
                                 en_of(key, 'obj'), noun.np_en(num)))
                    add('acc_weak_place', 'acc', key, form, u'',
                        u' %s %s.' % (v, place), en,
                        acc_weak_note(key, cap(form), v), noun=noun.key,
                        frame=i)


# --------------------------------------------------------------------------
# 3. accusative, strong pronoun after a preposition
# --------------------------------------------------------------------------
def build_acc_prep():
    fid = 0
    for lead, elead, idxs, gtail, etail, excl in F.ACC_PREP:
        for pi in idxs:
            prep, eprep, third_ok = F.PREPS[pi]
            for key in HUMAN:
                p, n, g = PINFO[key]
                if p == 3 and not third_ok:
                    continue
                # 'I am taking the key from me' is not a sentence
                if excl is not None and p == excl:
                    continue
                form = STRONG_ACC[key]
                note = (u'%s → strong personal pronoun, %s — after a'
                        u' preposition such as %s only the strong form is'
                        u' possible, never the weak one'
                        % (form, label(key, 'acc', True), prep))
                if p in (1, 2):
                    note += u'; in speech the first ε often drops: %s %s' \
                            % (prep, form[1:])
                en = tidy(u'%s%s %s%s' % (elead, eprep, en_of(key, 'obj'),
                                          tail(etail)))
                add('acc_prep', 'acc', key, form, lead + prep + u' ',
                    gtail if gtail[:1] in u'.;,' else u' ' + gtail,
                    en, note, frame=fid)
            fid += 1


# --------------------------------------------------------------------------
# 4. accusative, strong pronoun as an emphatic object
# --------------------------------------------------------------------------
def build_acc_emph():
    for i, (lead, elead) in enumerate(F.ACC_EMPH):
        for key in HUMAN:
            p, n, g = PINFO[key]
            # the contrast is always with the other side of the conversation
            oth_gr, oth_en = (u'εσένα', u'you') if p == 1 else (u'εμένα', u'me')
            form = STRONG_ACC[key]
            en = tidy(u'%s%s, not %s.' % (elead, en_of(key, 'obj'), oth_en))
            note = (u'%s → strong personal pronoun, %s — a weak pronoun'
                    u' cannot carry a contrast, so the strong one stands'
                    u' after the verb, against %s'
                    % (form, label(key, 'acc', True), oth_gr))
            add('acc_emph', 'acc', key, form, lead,
                u', όχι %s.' % oth_gr, en, note, frame=i)


# --------------------------------------------------------------------------
# 5. genitive, weak pronoun as indirect object
# --------------------------------------------------------------------------
def gen_io_note(key, form, verb_form):
    return (u'%s → weak personal pronoun, %s — the indirect object of %s;'
            u' Greek puts the person who receives in the genitive, in front'
            u' of the verb' % (form, label(key, 'gen', False), verb_form))


def build_gen_io():
    for i, row in enumerate(F.GEN_IO):
        lead, esubj, vb, sp, neg, gtail, etail, to_phrase = row
        v, eb, e3, sp_p, third = _subject_verb(vb, sp)
        subject = esubj or F.GEN_LEAD_EN[lead]
        for key in HUMAN:
            p, n, g = PINFO[key]
            if p == sp_p and p in (1, 2):
                continue
            form = WEAK_GEN[key]
            obj = en_of(key, 'obj')
            # English takes a bare indirect object in front of the direct
            # one, but a 'to ...' phrase with verbs like explain and talk
            rest = etail.rstrip(u'.')
            if to_phrase == 'before':
                parts = [u'to ' + obj, rest]
            elif to_phrase == 'after':
                parts = [rest, u'to ' + obj]
            else:
                parts = [obj, rest]
            parts = u' '.join(x for x in parts if x)
            if neg == 'never':
                head = u'%s never %s' % (subject, e3 if third else eb)
            elif neg:
                head = u'%s %s %s' % (subject,
                                      u"doesn't" if third else u"don't", eb)
            else:
                head = u'%s %s' % (subject, e3 if third else eb)
            body = u'%s %s.' % (head, parts)
            add('gen_io', 'gen', key, form, lead,
                u' %s %s' % (v, gtail), tidy(body),
                gen_io_note(key, cap(form) if not lead else form, v),
                frame=i)


def build_gen_io_obj():
    for i, (vb, sp, esubj, pool, art) in enumerate(F.GEN_IO_OBJ):
        v, eb, e3, sp_p, third = _subject_verb(vb, sp)
        for noun in POOLS[pool]:
            for num in ('sg', 'pl'):
                if not noun.has('acc', num) or noun.gr in MASS:
                    continue
                if art == 'indef' and num == 'pl':
                    continue
                for key in HUMAN:
                    p, n, g = PINFO[key]
                    if p == sp_p and p in (1, 2):
                        continue
                    form = WEAK_GEN[key]
                    en = tidy(u'%s %s %s %s.'
                              % (esubj, e3 if third else eb,
                                 en_of(key, 'obj'), noun.np_en(num, art)))
                    add('gen_io_obj', 'gen', key, form, u'',
                        u' %s %s.' % (v, noun.np('acc', num, art)), en,
                        gen_io_note(key, cap(form), v), noun=noun.key,
                        frame=i)


def build_gen_aresei():
    for i, (num, gtail, etail) in enumerate(F.GEN_ARESEI):
        v = u'αρέσει' if num == 'sg' else u'αρέσουν'
        for key in HUMAN:
            p, n, g = PINFO[key]
            form = WEAK_GEN[key]
            who = en_of(key, 'subj')
            vb = u'likes' if (p == 3 and n == 'sg') else u'like'
            note = (u'%s → weak personal pronoun, %s — with αρέσει the'
                    u' person who likes something stands in the genitive'
                    u' and the thing liked is the subject'
                    % (cap(form), label(key, 'gen', False)))
            add('gen_aresei', 'gen', key, form, u'',
                u' %s %s' % (v, gtail), tidy(u'%s %s %s' % (who, vb, etail)),
                note, frame=i)


# --------------------------------------------------------------------------
# 6. genitive, the weak possessive
# --------------------------------------------------------------------------
def build_gen_poss():
    for i, row in enumerate(F.GEN_POSS):
        lead, elead, pool, num, case, gtail, etail, dem = row
        for noun in POOLS[pool]:
            if not noun.has(case, num) or noun.gr in MASS:
                continue
            head = noun.form(case, num)
            if dem:
                lead = u'%s %s ' % (cap(DEM[(noun.g, 'nom', num)]),
                                    conjugate(u'είμαι', 'X', 3, num))
            pre = lead + noun.np(case, num) + u' '
            for key in HUMAN:
                form = WEAK_GEN[key]
                en = tidy(u'%s%s %s%s' % (elead, en_of(key, 'poss'),
                                          noun.en(num), etail))
                note = (u'%s → weak possessive pronoun, %s — the possessive'
                        u' clitic follows the noun it belongs to, here %s'
                        % (form, label(key, 'gen', False), head))
                add('gen_poss', 'gen', key, form, pre, gtail, en, note,
                    noun=noun.key, frame=i)


# --------------------------------------------------------------------------
# 7. δικός μου
# --------------------------------------------------------------------------
CASE_EN = {'nom': u'nominative', 'acc': u'accusative', 'gen': u'genitive'}
GEN_EN = {'m': u'masculine', 'f': u'feminine', 'n': u'neuter'}


def dikos_note(key, form, g, case, num, head):
    return (u'%s → emphatic possessive, %s %s %s to agree with %s, with the'
            u' weak genitive %s for the owner — δικός/δική/δικό takes the'
            u' gender, case and number of the thing owned, and the clitic'
            u' says whose it is'
            % (form, GEN_EN[g], CASE_EN[case],
               {'sg': u'singular', 'pl': u'plural'}[num], head,
               WEAK_GEN[key]))


def build_dikos_pred():
    for i, (pool, num, neg, gtail, etail) in enumerate(F.DIKOS_PRED):
        for noun in POOLS[pool]:
            if not noun.has('nom', num) or noun.gr in MASS:
                continue
            head = noun.form('nom', num)
            lead = u'%s %s %s %s%s ' % (
                cap(DEM[(noun.g, 'nom', num)]),
                definite(noun.g, 'nom', num, head), head,
                u'δεν ' if neg else u'', conjugate(u'είμαι', 'X', 3, num))
            for key in HUMAN:
                form = u'%s %s' % (dikos(noun.g, 'nom', num), WEAK_GEN[key])
                en = tidy(u'%s %s %s%s %s%s' % (
                    u'This' if num == 'sg' else u'These', noun.en(num),
                    u'is' if num == 'sg' else u'are',
                    u' not' if neg else u'', en_of(key, 'mine'), etail))
                add('dikos_pred', 'nom', key, form, lead, gtail, en,
                    dikos_note(key, form, noun.g, 'nom', num, head),
                    noun=noun.key, frame=i)


def _dikos_attr(family, case, pool, nums, lead, elead, gtail_f, etail_f,
                frame):
    for noun in POOLS[pool]:
        for num in nums:
            if not noun.has(case, num) or noun.gr in MASS:
                continue
            head = noun.form(case, num)
            art = definite(noun.g, case, num, u'δικ')
            pre = u'%s%s ' % (lead, art) if lead else cap(art) + u' '
            post = u' %s%s' % (head, tail(gtail_f(num)))
            for key in HUMAN:
                form = u'%s %s' % (dikos(noun.g, case, num), WEAK_GEN[key])
                en = tidy(u'%s%s %s %s' % (elead, en_of(key, 'own'),
                                           noun.en(num), etail_f(num)))
                add(family, case, key, form, pre, post, en,
                    dikos_note(key, form, noun.g, case, num, head),
                    noun=noun.key, frame=frame)


def build_dikos_nom():
    for i, (pool, nums, gtail, e_sg, e_pl) in enumerate(F.DIKOS_NOM):
        _dikos_attr('dikos_nom', 'nom', pool, nums, u'', u'',
                    lambda num, t=gtail: t,
                    lambda num, a=e_sg, b=e_pl: a if num == 'sg' else b, i)


def build_dikos_acc():
    for i, (lead, elead, pool, nums, gtail, etail) in enumerate(F.DIKOS_ACC):
        _dikos_attr('dikos_acc', 'acc', pool, nums, lead, elead,
                    lambda num, t=gtail: t, lambda num, t=etail: t, i)


def build_dikos_gen():
    for i, (lead, elead, pool, nums, gtail, etail) in enumerate(F.DIKOS_GEN):
        _dikos_attr('dikos_gen', 'gen', pool, nums, lead, elead,
                    lambda num, t=gtail: t, lambda num, t=etail: t, i)


BUILDERS = [
    build_nom_fix, build_nom_q, build_nom_be, build_nom_pred, build_nom_obj,
    build_nom_thing, build_nom_thing_pred,
    build_acc_weak, build_acc_weak_thing, build_acc_weak_place,
    build_acc_prep, build_acc_emph,
    build_gen_io, build_gen_io_obj, build_gen_aresei, build_gen_poss,
    build_dikos_pred, build_dikos_nom, build_dikos_acc, build_dikos_gen,
]


def build_all():
    del CARDS[:]
    SEEN.clear()
    for b in BUILDERS:
        b()
    return CARDS
