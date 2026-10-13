# -*- coding: utf-8 -*-
"""Greek personal pronouns, the δικός-type possessive, and present-tense verbs.

Everything here is paradigm data plus the two rules that act on it: the
final-ν rule and the fixed-accent rule of -ος/-η/-ο words.
"""
from greeklex import (accent_on, accent_pos, deaccent, keeps_nu, nsyl,
                      decline_adj, decline_noun, definite)

# the ten referents a card can ask for: person, number, gender
#   gender is None for 1st and 2nd person, which do not inflect for it
PERSONS = [
    ('1sg', 1, 'sg', None), ('2sg', 2, 'sg', None),
    ('3sgm', 3, 'sg', 'm'), ('3sgf', 3, 'sg', 'f'), ('3sgn', 3, 'sg', 'n'),
    ('1pl', 1, 'pl', None), ('2pl', 2, 'pl', None),
    ('3plm', 3, 'pl', 'm'), ('3plf', 3, 'pl', 'f'), ('3pln', 3, 'pl', 'n'),
]
PINFO = dict((k, (p, n, g)) for (k, p, n, g) in PERSONS)

# --------------------------------------------------------------------------
# personal pronouns
# --------------------------------------------------------------------------
# strong (emphatic) forms — the only ones that exist in the nominative
STRONG_NOM = {
    '1sg': u'εγώ', '2sg': u'εσύ', '3sgm': u'αυτός', '3sgf': u'αυτή',
    '3sgn': u'αυτό', '1pl': u'εμείς', '2pl': u'εσείς', '3plm': u'αυτοί',
    '3plf': u'αυτές', '3pln': u'αυτά',
}
STRONG_ACC = {
    '1sg': u'εμένα', '2sg': u'εσένα', '3sgm': u'αυτόν', '3sgf': u'αυτήν',
    '3sgn': u'αυτό', '1pl': u'εμάς', '2pl': u'εσάς', '3plm': u'αυτούς',
    '3plf': u'αυτές', '3pln': u'αυτά',
}
# weak (clitic) forms
WEAK_ACC = {
    '1sg': u'με', '2sg': u'σε', '3sgm': u'τον', '3sgf': u'την',
    '3sgn': u'το', '1pl': u'μας', '2pl': u'σας', '3plm': u'τους',
    '3plf': u'τις', '3pln': u'τα',
}
WEAK_GEN = {
    '1sg': u'μου', '2sg': u'σου', '3sgm': u'του', '3sgf': u'της',
    '3sgn': u'του', '1pl': u'μας', '2pl': u'σας', '3plm': u'τους',
    '3plf': u'τους', '3pln': u'τους',
}

# English glosses, keyed by the job the pronoun is doing
EN_SUBJ = {'1sg': u'I', '2sg': u'you', '3sgm': u'he', '3sgf': u'she',
           '3sgn': u'it', '1pl': u'we', '2pl': u'you', '3plm': u'they',
           '3plf': u'they', '3pln': u'they'}
EN_OBJ = {'1sg': u'me', '2sg': u'you', '3sgm': u'him', '3sgf': u'her',
          '3sgn': u'it', '1pl': u'us', '2pl': u'you', '3plm': u'them',
          '3plf': u'them', '3pln': u'them'}
EN_POSS = {'1sg': u'my', '2sg': u'your', '3sgm': u'his', '3sgf': u'her',
           '3sgn': u'its', '1pl': u'our', '2pl': u'your', '3plm': u'their',
           '3plf': u'their', '3pln': u'their'}
EN_MINE = {'1sg': u'mine', '2sg': u'yours', '3sgm': u'his', '3sgf': u'hers',
           '3sgn': u'its', '1pl': u'ours', '2pl': u'yours', '3plm': u'theirs',
           '3plf': u'theirs', '3pln': u'theirs'}
# 'my own' keeps the emphatic δικός apart from the plain possessive 'my'
EN_OWN = {'1sg': u'my own', '2sg': u'your own', '3sgm': u'his own',
          '3sgf': u'her own', '3sgn': u'its own', '1pl': u'our own',
          '2pl': u'your own', '3plm': u'their own', '3plf': u'their own',
          '3pln': u'their own'}

# the prompt has to say exactly which referent is meant: English "you" and
# "them" are ambiguous where Greek is not, so every gloss carries a tag
TAG = {'1sg': u'', '2sg': u' (singular)', '3sgm': u'', '3sgf': u'',
       '3sgn': u'', '1pl': u'', '2pl': u' (plural)',
       '3plm': u' (masculine)', '3plf': u' (feminine)',
       '3pln': u' (neuter)'}

GENDER_EN = {'m': u'masculine', 'f': u'feminine', 'n': u'neuter'}
ORD_EN = {1: u'1st person', 2: u'2nd person', 3: u'3rd person'}
NUM_EN = {'sg': u'singular', 'pl': u'plural'}


# A thing is αυτός, αυτή or αυτό in Greek but always "it" in English,
# so for those prompts the gender tag is the only thing that picks the form.
EN_T_SUBJ = {'3sgm': u'it', '3sgf': u'it', '3sgn': u'it',
             '3plm': u'they', '3plf': u'they', '3pln': u'they'}
EN_T_OBJ = {'3sgm': u'it', '3sgf': u'it', '3sgn': u'it',
            '3plm': u'them', '3plf': u'them', '3pln': u'them'}
TTAG = {'3sgm': u' (masculine)', '3sgf': u' (feminine)',
        '3sgn': u' (neuter)', '3plm': u' (masculine)',
        '3plf': u' (feminine)', '3pln': u' (neuter)'}

TABLES = {'subj': EN_SUBJ, 'obj': EN_OBJ, 'poss': EN_POSS,
          'mine': EN_MINE, 'own': EN_OWN,
          'tsubj': EN_T_SUBJ, 'tobj': EN_T_OBJ}


def gloss(key, kind):
    """The English hint for a referent, e.g. 'them (neuter)'.

    English 'you' and 'they' cover more ground than any one Greek form, so
    the tag is what makes the prompt answerable.
    """
    tag = TTAG[key] if kind.startswith('t') else TAG[key]
    return TABLES[kind][key] + tag


def en_of(key, kind):
    """The same word without the tag, for use inside an English sentence."""
    return TABLES[kind][key]


def label(key, case, strong):
    """'3rd person masculine accusative singular' for the explanation."""
    p, n, g = PINFO[key]
    bits = [ORD_EN[p]]
    if g:
        bits.append(GENDER_EN[g])
    bits.append({'nom': u'nominative', 'acc': u'accusative',
                 'gen': u'genitive'}[case])
    bits.append(NUM_EN[n])
    return u' '.join(bits)


def weak_acc(key, nxt):
    """Weak accusative, with the final-ν rule applied to την.

    τον keeps its -ν everywhere in standard practice, so that it is never
    confused with the neuter το; την follows the rule.
    """
    form = WEAK_ACC[key]
    if form == u'την' and not keeps_nu(nxt):
        return u'τη'
    return form


# --------------------------------------------------------------------------
# αυτός as a demonstrative ('this car'), which declines like an adjective
# --------------------------------------------------------------------------
DEM = {
    ('m', 'nom', 'sg'): u'αυτός', ('m', 'acc', 'sg'): u'αυτόν',
    ('m', 'gen', 'sg'): u'αυτού', ('m', 'nom', 'pl'): u'αυτοί',
    ('m', 'acc', 'pl'): u'αυτούς', ('m', 'gen', 'pl'): u'αυτών',
    ('f', 'nom', 'sg'): u'αυτή', ('f', 'acc', 'sg'): u'αυτή',
    ('f', 'gen', 'sg'): u'αυτής', ('f', 'nom', 'pl'): u'αυτές',
    ('f', 'acc', 'pl'): u'αυτές', ('f', 'gen', 'pl'): u'αυτών',
    ('n', 'nom', 'sg'): u'αυτό', ('n', 'acc', 'sg'): u'αυτό',
    ('n', 'gen', 'sg'): u'αυτού', ('n', 'nom', 'pl'): u'αυτά',
    ('n', 'acc', 'pl'): u'αυτά', ('n', 'gen', 'pl'): u'αυτών',
}

# --------------------------------------------------------------------------
# δικός / δική / δικό — fixed accent, so the adjective engine handles it
# --------------------------------------------------------------------------
def dikos(gender, case, number):
    return decline_adj(u'δικός', u'ή', gender, case, number)


# --------------------------------------------------------------------------
# σε + definite article
# --------------------------------------------------------------------------
SE = {('m', 'sg'): u'στον', ('f', 'sg'): u'στην', ('n', 'sg'): u'στο',
      ('m', 'pl'): u'στους', ('f', 'pl'): u'στις', ('n', 'pl'): u'στα'}


def se_art(gender, number, nxt):
    form = SE[(gender, number)]
    if form == u'στην' and not keeps_nu(nxt):
        return u'στη'
    return form


# --------------------------------------------------------------------------
# present tense
# --------------------------------------------------------------------------
IDX = {('1', 'sg'): 0, ('2', 'sg'): 1, ('3', 'sg'): 2,
       ('1', 'pl'): 3, ('2', 'pl'): 4, ('3', 'pl'): 5}

A_END = [u'ω', u'εις', u'ει', u'ουμε', u'ετε', u'ουν']
B1_END = [u'άω', u'άς', u'άει', u'άμε', u'άτε', u'άνε']
B2_END = [u'ώ', u'είς', u'εί', u'ούμε', u'είτε', u'ούν']

# verbs whose present is not produced by any of the three patterns
IRREGULAR = {
    u'είμαι':   [u'είμαι', u'είσαι', u'είναι', u'είμαστε', u'είστε', u'είναι'],
    u'πάω':     [u'πάω', u'πας', u'πάει', u'πάμε', u'πάτε', u'πάνε'],
    u'λέω':     [u'λέω', u'λες', u'λέει', u'λέμε', u'λέτε', u'λένε'],
    u'τρώω':    [u'τρώω', u'τρως', u'τρώει', u'τρώμε', u'τρώτε', u'τρώνε'],
    u'ακούω':   [u'ακούω', u'ακούς', u'ακούει', u'ακούμε', u'ακούτε',
                 u'ακούνε'],
    u'ζω':      [u'ζω', u'ζεις', u'ζει', u'ζούμε', u'ζείτε', u'ζουν'],
    u'έρχομαι': [u'έρχομαι', u'έρχεσαι', u'έρχεται', u'ερχόμαστε',
                 u'έρχεστε', u'έρχονται'],
    u'κάθομαι': [u'κάθομαι', u'κάθεσαι', u'κάθεται', u'καθόμαστε',
                 u'κάθεστε', u'κάθονται'],
    u'σκέφτομαι': [u'σκέφτομαι', u'σκέφτεσαι', u'σκέφτεται', u'σκεφτόμαστε',
                   u'σκέφτεστε', u'σκέφτονται'],
    u'κοιμάμαι': [u'κοιμάμαι', u'κοιμάσαι', u'κοιμάται', u'κοιμόμαστε',
                  u'κοιμάστε', u'κοιμούνται'],
    u'θυμάμαι': [u'θυμάμαι', u'θυμάσαι', u'θυμάται', u'θυμόμαστε',
                 u'θυμάστε', u'θυμούνται'],
    u'φοβάμαι': [u'φοβάμαι', u'φοβάσαι', u'φοβάται', u'φοβόμαστε',
                 u'φοβάστε', u'φοβούνται'],
    u'χρειάζομαι': [u'χρειάζομαι', u'χρειάζεσαι', u'χρειάζεται',
                    u'χρειαζόμαστε', u'χρειάζεστε', u'χρειάζονται'],
}


def conjugate(lemma, group, person, number):
    """Present tense. group is 'A', 'B1', 'B2' or 'X' (table above)."""
    i = IDX[(str(person), number)]
    if group == 'X':
        return IRREGULAR[lemma][i]
    if group == 'B1':
        return lemma[:-2] + B1_END[i]
    if group == 'B2':
        return lemma[:-1] + B2_END[i]
    # group A: the accent sits on a fixed syllable of the stem
    form = deaccent(lemma[:-1]) + A_END[i]
    k = accent_pos(lemma)
    out = accent_on(form, k)
    # the three-syllable limit, in case a stem ever needs it
    p = accent_pos(out)
    if p is not None and nsyl(out) - p > 3:
        out = accent_on(out, nsyl(out) - 3)
    return out


def en_verb(base, third, key):
    """English present: the -s form for he/she/it, the bare form elsewhere."""
    p, n, g = PINFO[key]
    return third if (p == 3 and n == 'sg') else base


def cap(text):
    return text[0].upper() + text[1:] if text else text
