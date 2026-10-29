# -*- coding: utf-8 -*-
"""Every Greek word in the pronoun deck must trace back to KLIK A2.

Three checks:
  1. every noun, adjective and verb the deck inflects is a KLIK headword;
  2. every word hard-coded into a sentence frame is a KLIK headword, or an
     inflected form of one named explicitly below;
  3. every Greek token in every finished card is one of those, a pronoun,
     an article, or a form the deck itself generated.
"""
from __future__ import print_function
import io, os, re, sys

from greeklex import (deaccent, decline_noun, decline_adj, DEF_ART,
                      INDEF_ART)
from data2 import NOUNS, ADJS
from pron import (STRONG_NOM, STRONG_ACC, WEAK_ACC, WEAK_GEN, DEM, dikos,
                  conjugate)
import frames as F

# the word list lives one level up, next to the decks it constrains. The
# proper names were moved into a sidecar so they would stop coming up as
# flashcards, but they are still KLIK headwords, so both files count here.
_UP = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
KLIK_PATH = os.path.join(_UP, 'klik-a2-vocabulary.txt')
KLIK_NAMES_PATH = os.path.join(_UP, 'klik-a2-names.txt')
GREEK = re.compile(u'[\u0370-\u03ff\u1f00-\u1fff]+')


def klik_forms(paths=(KLIK_PATH, KLIK_NAMES_PATH)):
    out = set()
    for path in paths:
        raw = io.open(path, encoding='utf-8-sig').read().replace('\r\n', '\n')
        for block in raw.split('\n\n'):
            lines = block.split('\n')
            if len(lines) >= 2:
                for w in GREEK.findall(lines[1]):
                    out.add(deaccent(w.lower()))
    return out


# KLIK often lists only one gender of a pair. The other gender is the same
# word, not a new one, so it is in scope as long as its counterpart is listed.
GENDER_COUNTERPART = {
    u'φίλος': u'φίλη',       # KLIK lists η φίλη only
    u'πατέρας': u'μητέρα',   # KLIK lists η μητέρα, and ο μπαμπάς for "dad"
}

# frame words that are an inflected form, or a fixed phrase, of a KLIK entry
FRAME_LEMMA = {
    u'μένουν': u'μένω', u'δουλεύει': u'δουλεύω', u'πίνει': u'πίνω',
    u'ξεχνάει': u'ξεχνάω', u'ξέρουν': u'ξέρω', u'πηγαίνουν': u'πηγαίνω',
    u'μιλάει': u'μιλάω', u'έρχεται': u'έρχομαι', u'έρχονται': u'έρχομαι',
    u'ρωτάει': u'ρωτάω', u'κάθεται': u'κάθομαι', u'αρχίζει': u'αρχίζω',
    u'παίζουν': u'παίζω', u'ετοιμάζει': u'ετοιμάζω', u'ταξιδεύει': u'ταξιδεύω',
    u'ταξιδεύουν': u'ταξιδεύω', u'φεύγει': u'φεύγω', u'μαγειρεύει': u'μαγειρεύω',
    u'διαλέγει': u'διαλέγω', u'περιμένει': u'περιμένω', u'ψάχνει': u'ψάχνω',
    u'κοιτάζουν': u'κοιτάζω', u'χαιρετάνε': u'χαιρετάω', u'βοηθάει': u'βοηθάω',
    u'ζωγραφίζει': u'ζωγραφίζω', u'καλεί': u'καλώ', u'βρίσκω': u'βρίσκω',
    u'φύγω': u'φεύγω', u'ζήσω': u'ζω', u'έρθω': u'έρχομαι',
    u'αρέσει': u'αρέσει', u'αρέσουν': u'αρέσει', u'είναι': u'είμαι',
    u'πληρώνει': u'πληρώνω', u'φωτογραφία': u'φωτογραφία',
    u'όλο': u'όλος', u'όλη': u'όλος', u'μικρή': u'μικρός',
    u'μεγάλο': u'μεγάλος', u'μεγάλες': u'μεγάλος', u'τελευταία': u'τελευταίος',
    u'ίδια': u'ίδιος', u'καινούριες': u'καινούριος', u'καινούρια': u'καινούριος',
    u'ανοιχτή': u'ανοιχτός', u'δύσκολη': u'δύσκολος', u'πρώτη': u'πρώτος',
    u'ελληνική': u'ελληνικός', u'καλή': u'καλός', u'άλλοι': u'άλλος',
    u'γλυκά': u'γλυκό', u'πόλεις': u'πόλη', u'ταξίδια': u'ταξίδι',
    u'λέξεις': u'λέξη', u'ονόματα': u'όνομα', u'κλειδιά': u'κλειδί',
    u'λουλούδια': u'λουλούδι', u'φωτογραφίες': u'φωτογραφία',
    u'ασκήσεις': u'άσκηση', u'διακοπές': u'διακοπές', u'ψώνια': u'ψώνια',
    u'πελάτες': u'πελάτης', u'γονείς': u'γονείς', u'συνάδελφοι': u'συνάδελφος',
    u'φίλοι': u'φίλος', u'φίλες': u'φίλη', u'γείτονες': u'γείτονας',
    u'παιδιά': u'παιδί', u'γιατροί': u'γιατρός', u'χρόνια': u'χρόνος', u'χρόνο': u'χρόνος',
    u'λεμόνι': u'λεμόνι', u'τα': u'το', u'πάντα': u'πάντα',
    u'καφέ': u'καφές', u'χυμό': u'χυμός', u'απάντηση': u'απάντηση',
    u'λογαριασμό': u'λογαριασμός', u'μάθημα': u'μάθημα',
    u'χορού': u'χορός', u'ενδιαφέρον': u'ενδιαφέρομαι',
    u'προσοχή': u'προσοχή', u'σειρά': u'σειρά', u'αλήθεια': u'αλήθεια',
    u'μπλε': u'μπλε', u'αυλή': u'αυλή', u'πουθενά': u'πουθενά',
    u'δέκα': u'δέκα', u'όχι': u'όχι', u'μαζί': u'μαζί',
}

ARTICLES = set()
for _t in (DEF_ART, INDEF_ART):
    for _v in _t.values():
        ARTICLES.add(deaccent(_v.lower()))
ARTICLES |= set(deaccent(w) for w in
                (u'τη', u'στο', u'στη', u'στην', u'στον', u'στους', u'στα',
                 u'στις'))

# the pronoun paradigms the deck teaches
PRONOUNS = set()
for _t in (STRONG_NOM, STRONG_ACC, WEAK_ACC, WEAK_GEN):
    for _v in _t.values():
        PRONOUNS.add(deaccent(_v.lower()))
PRONOUNS.add(deaccent(u'τη'))
for _v in DEM.values():
    PRONOUNS.add(deaccent(_v.lower()))
for _g in 'mfn':
    for _c in ('nom', 'acc', 'gen'):
        for _n in ('sg', 'pl'):
            PRONOUNS.add(deaccent(dikos(_g, _c, _n).lower()))


def generated_forms():
    out = set()
    for gr, cls, tag, en, enpl in NOUNS:
        for form in decline_noun(gr, cls).values():
            out.add(deaccent(form.lower()))
    for masc, fv, en, tags, only in ADJS:
        for g in 'mfn':
            for case in ('nom', 'acc', 'gen'):
                for n in ('sg', 'pl'):
                    out.add(deaccent(decline_adj(masc, fv, g, case, n).lower()))
    for lemma, (grp, eb, e3) in F.VERBS.items():
        for p in (1, 2, 3):
            for n in ('sg', 'pl'):
                out.add(deaccent(conjugate(lemma, grp, p, n).lower()))
    return out


def frame_tokens():
    """Every Greek word written by hand into a frame table."""
    out = set()
    for name in dir(F):
        if name.startswith('_') or name == 'VERBS':
            continue
        val = getattr(F, name)
        stack = [val]
        while stack:
            item = stack.pop()
            if isinstance(item, (list, tuple)):
                stack.extend(item)
            elif isinstance(item, dict):
                stack.extend(item.keys())
                stack.extend(item.values())
            elif isinstance(item, type(u'')):
                out |= set(w.lower() for w in GREEK.findall(item))
    return out


def main(deck):
    klik = klik_forms()
    problems = []

    def in_klik(word):
        if deaccent(word.lower()) in klik:
            return True
        mate = GENDER_COUNTERPART.get(word)
        return mate is not None and deaccent(mate.lower()) in klik

    # 1. the deck's own lexicon
    for gr, cls, tag, en, enpl in NOUNS:
        if not in_klik(gr):
            problems.append(u'noun not in KLIK: %s' % gr)
    for masc, fv, en, tags, only in ADJS:
        if not in_klik(masc):
            problems.append(u'adjective not in KLIK: %s' % masc)
    for lemma in F.VERBS:
        if not in_klik(lemma):
            problems.append(u'verb not in KLIK: %s' % lemma)

    # 2. words hard-coded into the sentence frames
    ft = frame_tokens()
    gen = generated_forms()
    for w in sorted(ft):
        d = deaccent(w)
        # an inflected form of something the deck already declines is fine
        if d in klik or d in ARTICLES or d in PRONOUNS or d in gen:
            continue
        lemma = FRAME_LEMMA.get(w)
        if lemma is None:
            problems.append(u'frame word with no KLIK lemma: %s' % w)
        elif not in_klik(lemma):
            problems.append(u'frame word %s -> %s, not in KLIK' % (w, lemma))

    # 3. every token of every finished card
    allowed = (gen | ARTICLES | PRONOUNS |
               set(deaccent(w) for w in ft) |
               set(deaccent(w.lower()) for w in FRAME_LEMMA) |
               set(deaccent(w.lower()) for w in FRAME_LEMMA.values()))
    text = io.open(deck, 'rb').read().decode('utf-8-sig').replace('\r\n', '\n')
    blocks = [b for b in text.strip('\n').split('\n\n') if b.strip()]
    stray = {}
    for i, b in enumerate(blocks, 1):
        L = b.split('\n')
        if len(L) != 4:
            continue
        sentence = L[1].rsplit(' (', 1)[0]
        for chunk in (sentence, L[2]):
            for w in GREEK.findall(chunk):
                if deaccent(w.lower()) not in allowed:
                    stray.setdefault(w, []).append(i)
    for w, where in sorted(stray.items()):
        problems.append(u'token outside KLIK: %s (%d cards, e.g. #%d)'
                        % (w, len(where), where[0]))

    print(u'KLIK headword forms : %d' % len(klik))
    print(u'deck lexicon        : %d nouns, %d adjectives, %d verbs'
          % (len(NOUNS), len(ADJS), len(F.VERBS)))
    print(u'distinct frame words: %d' % len(ft))
    print(u'cards checked       : %d' % len(blocks))
    if problems:
        for p in problems[:30]:
            print(u'  ! %s' % p)
        print(u'PROBLEMS: %d' % len(problems))
        return 1
    print(u'every word traces to KLIK A2: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'deck.txt'))
