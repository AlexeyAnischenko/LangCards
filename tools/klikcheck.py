# -*- coding: utf-8 -*-
"""Every Greek word in the deck must trace back to the KLIK A2 word list.

Three things are checked:
  1. every noun and adjective the deck inflects is a KLIK headword;
  2. every word hard-coded into a sentence frame is a KLIK headword, or an
     inflected form of one named explicitly below;
  3. every Greek token in every finished card is one of those, an article,
     or a form the deck itself generated.
"""
import io, os, re, sys
from greeklex import deaccent, decline_noun, decline_adj, DEF_ART, INDEF_ART
from data2 import NOUNS, ADJS

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

# frame words that are an inflected form of a KLIK headword
FRAME_LEMMA = {
    u'έχουμε': u'έχω', u'ήρθαμε': u'έρχομαι', u'ήρθαν': u'έρχομαι',
    u'καθαρίζουμε': u'καθαρίζω', u'μιλάμε': u'μιλάω', u'περπατάμε': u'περπατάω',
    u'ταξιδεύουμε': u'ταξιδεύω', u'τρώμε': u'τρώω', u'άλλαξε': u'αλλάζω',
    u'ήταν': u'είμαι', u'ανοιχτά': u'ανοιχτός', u'ανοιχτή': u'ανοιχτός',
    u'αρέσουν': u'αρέσει', u'γνωστό': u'γνωστός', u'δύσκολη': u'δύσκολος',
    u'καινούριο': u'καινούριος', u'καλή': u'καλός',
    u'καταπληκτική': u'καταπληκτικός', u'κοιμάται': u'κοιμάμαι',
    u'μεγάλη': u'μεγάλος', u'μεγάλο': u'μεγάλος', u'παράθυρα': u'παράθυρο',
    u'υπέροχη': u'υπέροχος', u'φίλες': u'φίλη', u'φτηνά': u'φτηνός',
    u'χρώματα': u'χρώμα', u'ωραίο': u'ωραίος', u'όμορφη': u'όμορφος',
    u'άνοιξε': u'ανοίγω', u'άνοιξαν': u'ανοίγω', u'άρχισε': u'αρχίζω',
    u'άρχισαν': u'αρχίζω', u'τελείωσε': u'τελειώνω', u'τελείωσαν': u'τελειώνω',
    u'βοήθησε': u'βοηθάω', u'βοήθησαν': u'βοηθάω', u'δουλεύει': u'δουλεύω',
    u'δουλεύουν': u'δουλεύω', u'κοστίζει': u'κοστίζω', u'κοστίζουν': u'κοστίζω',
    u'παίζει': u'παίζω', u'παίζουν': u'παίζω', u'πουλάει': u'πουλάω',
    u'πουλάνε': u'πουλάω', u'πονάει': u'πονάω', u'πονάνε': u'πονάω',
    u'είναι': u'είμαι', u'μπορώ': u'μπορώ', u'φίλοι': u'φίλος',
}

ARTICLES = set()
for table in (DEF_ART, INDEF_ART):
    for v in table.values():
        ARTICLES.add(deaccent(v.lower()))
ARTICLES |= set([u'τη', u'στο', u'στη', u'στην', u'στον', u'στους', u'στα', u'στις'])


def generated_forms():
    """Every form the deck can legitimately produce from its own lexicon."""
    out = set()
    for gr, cls, tag, en, enpl in NOUNS:
        for form in decline_noun(gr, cls).values():
            out.add(deaccent(form.lower()))
    genders = ('m', 'f', 'n')
    for masc, fv, en, tags, only in ADJS:
        for g in genders:
            for case in ('nom', 'acc', 'gen'):
                for num in ('sg', 'pl'):
                    out.add(deaccent(decline_adj(masc, fv, g, case, num).lower()))
    return out


def main(deck):
    klik = klik_forms()
    problems = []

    # 1. the deck's own lexicon
    for gr, cls, tag, en, enpl in NOUNS:
        if deaccent(gr.lower()) in klik:
            continue
        mate = GENDER_COUNTERPART.get(gr)
        if mate is None:
            problems.append(u'noun not in KLIK: %s' % gr)
        elif deaccent(mate.lower()) not in klik:
            problems.append(u'noun %s claims counterpart %s, which is not in KLIK'
                            % (gr, mate))
    for masc, fv, en, tags, only in ADJS:
        if deaccent(masc.lower()) not in klik:
            problems.append(u'adjective not in KLIK: %s' % masc)

    # 2. words hard-coded into the sentence frames
    import gen
    frame_tokens = set()
    for t in gen.T:
        for part in (t[0], t[1]):
            frame_tokens |= set(w.lower() for w in GREEK.findall(part))
    for table in (gen.GR_AGREE,):
        for v in table.values():
            for f in v:
                frame_tokens |= set(w.lower() for w in GREEK.findall(f))
    for w in sorted(frame_tokens):
        if deaccent(w) in klik or deaccent(w) in ARTICLES:
            continue
        lemma = FRAME_LEMMA.get(w)
        if lemma is None:
            problems.append(u'frame word with no KLIK lemma: %s' % w)
            continue
        if deaccent(lemma.lower()) in klik:
            continue
        mate = GENDER_COUNTERPART.get(lemma)
        if mate is None or deaccent(mate.lower()) not in klik:
            problems.append(u'frame word %s -> %s, which is not in KLIK' % (w, lemma))

    # 3. every token of every finished card
    allowed = generated_forms() | ARTICLES | set(deaccent(w) for w in frame_tokens)
    allowed |= set(deaccent(w.lower()) for w in FRAME_LEMMA)
    text = io.open(deck, 'rb').read().decode('utf-8-sig').replace('\r\n', '\n')
    blocks = [b for b in text.strip('\n').split('\n\n') if b.strip()]
    stray = {}
    for i, b in enumerate(blocks, 1):
        L = b.split('\n')
        if len(L) != 4:
            continue
        # the prompt sentence (minus the bracketed hint) and the full answer
        sentence = L[1].rsplit(' (', 1)[0]
        for chunk in (sentence, L[2]):
            for w in GREEK.findall(chunk):
                if deaccent(w.lower()) not in allowed:
                    stray.setdefault(w, []).append(i)
    for w, where in sorted(stray.items()):
        problems.append(u'token outside KLIK: %s (%d cards, e.g. #%d)'
                        % (w, len(where), where[0]))

    print(u'KLIK headword forms      : %d' % len(klik))
    print(u'deck lexicon             : %d nouns, %d adjectives'
          % (len(NOUNS), len(ADJS)))
    print(u'distinct frame words     : %d' % len(frame_tokens))
    print(u'cards checked            : %d' % len(blocks))
    if problems:
        for p in problems[:25]:
            print(u'  ! %s' % p)
        print(u'PROBLEMS: %d' % len(problems))
        return 1
    print(u'every word traces to KLIK A2: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'deck.txt'))
