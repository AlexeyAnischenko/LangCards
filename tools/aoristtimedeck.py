# -*- coding: utf-8 -*-
"""Build the present → aorist deck: a time word and a present-tense verb on the
front, the same sentence moved into the past on the back.

    Σήμερα ο Νίκος γράφει.         →   Χθες ο Νίκος έγραψε.
    Τώρα εσείς ψάχνετε.            →   Πριν από λίγο εσείς ψάξατε.
    Φέτος τα παιδιά μετακομίζουν.  →   Πέρσι τα παιδιά μετακόμισαν.

Both the time word and the verb change; the time words come in fixed pairs
(σήμερα → χθες, φέτος → πέρσι, αυτή την εβδομάδα → την προηγούμενη εβδομάδα
...), all of them KLIK A2 words. Only one-off past events are paired, never a
habit (κάθε μέρα, συνήθως): their past is the imperfect, not the aorist.

The verbs and their aorists are the ones in aoristdeck.py (KLIK A2, aorist
written by hand per verb); the present tense comes from pron.conjugate, with
the deponent -μαι verbs it does not cover written out below. The 3rd persons
rotate between pronouns and noun subjects (ο Νίκος, η μαμά μου, τα παιδιά …)
so that matching the ending to a noun subject gets drilled too.

3,000 cards: 163 verbs × 6 persons × 3 time words = 2,934, plus 66 extra
cards on the irregular verbs, spread so that every person has exactly 500.
Deterministic: rerunning reproduces the file byte for byte.

Run from anywhere:  python tools/aoristtimedeck.py
"""
import io, os, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
LC = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from aoristdeck import VERBS, paradigm, check                  # noqa: E402
from pron import conjugate, IRREGULAR                          # noqa: E402
from greeklex import accent_pos, accent_on, deaccent           # noqa: E402
from klikcheck import klik_forms, GREEK                        # noqa: E402

OUT = os.path.join(LC, 'greek-a2-present-to-aorist-3000.txt')
TOTAL = 3000

# "today I die" is no drill sentence, and ζω / μεγαλώνω / σπουδάζω only make
# sense with a place or a span of years (έζησα στην Αθήνα δύο χρόνια) that a
# bare verb cannot carry. All four stay in the plain aorist deck.
SKIP = {u'πεθαίνω', u'ζω', u'μεγαλώνω', u'σπουδάζω'}

# ------------------------------------------------------------------ present
MORE_IRREGULAR = {
    u'καίω': [u'καίω', u'καις', u'καίει', u'καίμε', u'καίτε', u'καίνε'],
    u'λυπάμαι': [u'λυπάμαι', u'λυπάσαι', u'λυπάται', u'λυπόμαστε',
                 u'λυπάστε', u'λυπούνται'],
}


def omai(lemma):
    """-ομαι deponents: έρχομαι-type; 1pl moves the stress to -όμαστε."""
    st = lemma[:-4]
    plain = deaccent(st)
    return [st + u'ομαι', st + u'εσαι', st + u'εται',
            plain + u'όμαστε', st + u'εστε', st + u'ονται']


def present(lemma):
    if lemma in IRREGULAR:
        return list(IRREGULAR[lemma])
    if lemma in MORE_IRREGULAR:
        return MORE_IRREGULAR[lemma]
    if lemma.endswith(u'ομαι'):
        return omai(lemma)
    if lemma.endswith(u'άω'):
        g = 'B1'
    elif lemma.endswith(u'ώ'):
        g = 'B2'
    else:
        g = 'A'
    return [conjugate(lemma, g, p, n)
            for p, n in ((1, 'sg'), (2, 'sg'), (3, 'sg'),
                         (1, 'pl'), (2, 'pl'), (3, 'pl'))]


PRESENT_GOLD = {
    u'γίνομαι': u'γίνομαι γίνεσαι γίνεται γινόμαστε γίνεστε γίνονται',
    u'ενδιαφέρομαι': u'ενδιαφέρομαι ενδιαφέρεσαι ενδιαφέρεται ενδιαφερόμαστε '
                     u'ενδιαφέρεστε ενδιαφέρονται',
    u'ξεκουράζομαι': u'ξεκουράζομαι ξεκουράζεσαι ξεκουράζεται ξεκουραζόμαστε '
                     u'ξεκουράζεστε ξεκουράζονται',
    u'επισκέπτομαι': u'επισκέπτομαι επισκέπτεσαι επισκέπτεται επισκεπτόμαστε '
                     u'επισκέπτεστε επισκέπτονται',
    u'αισθάνομαι': u'αισθάνομαι αισθάνεσαι αισθάνεται αισθανόμαστε '
                   u'αισθάνεστε αισθάνονται',
    u'παντρεύομαι': u'παντρεύομαι παντρεύεσαι παντρεύεται παντρευόμαστε '
                    u'παντρεύεστε παντρεύονται',
    u'καταλαβαίνω': u'καταλαβαίνω καταλαβαίνεις καταλαβαίνει καταλαβαίνουμε '
                    u'καταλαβαίνετε καταλαβαίνουν',
    u'μιλάω': u'μιλάω μιλάς μιλάει μιλάμε μιλάτε μιλάνε',
    u'καλώ': u'καλώ καλείς καλεί καλούμε καλείτε καλούν',
    u'καίω': u'καίω καις καίει καίμε καίτε καίνε',
}

# ------------------------------------------------------------------ time words
# (present-time phrase, past-time phrase, English past-time phrase)
SHORT = [
    (u'σήμερα', u'χθες', u'yesterday'),
    (u'σήμερα το πρωί', u'χθες το πρωί', u'yesterday morning'),
    (u'σήμερα το απόγευμα', u'χθες το απόγευμα', u'yesterday afternoon'),
    (u'σήμερα το βράδυ', u'χθες το βράδυ', u'yesterday evening'),
    (u'τώρα', u'πριν από λίγο', u'a little while ago'),
    (u'αυτό το Σαββατοκύριακο', u'το προηγούμενο Σαββατοκύριακο',
     u'last weekend'),
]
LONG = [
    (u'αυτή την εβδομάδα', u'την προηγούμενη εβδομάδα', u'last week'),
    (u'αυτόν τον μήνα', u'τον προηγούμενο μήνα', u'last month'),
    (u'φέτος', u'πέρσι', u'last year'),
    (u'αυτό το καλοκαίρι', u'πέρσι το καλοκαίρι', u'last summer'),
]
# Events measured in months or years: "yesterday I moved house" is odd.
LONG_ONLY = {u'μετακομίζω', u'παντρεύομαι'}
# Things that happen once in a day just as well as once in a year.
ANY_SPAN = set(u'''ταξιδεύω γιορτάζω νοικιάζω κερδίζω μαθαίνω γνωρίζω
    διασκεδάζω επισκέπτομαι φιλοξενώ δουλεύω αρχίζω τελειώνω συνεχίζω χάνω
    αποφασίζω ξοδεύω μαζεύω σχεδιάζω δοκιμάζω ζωγραφίζω διαβάζω γράφω
    μαγειρεύω χορεύω παίζω αγοράζω πουλάω πληρώνω βάφω στέλνω γίνομαι
    ξεκουράζομαι κάνω ετοιμάζω καθαρίζω ψωνίζω φτιάχνω βοηθάω συναντάω φτάνω
    επιστρέφω γυρίζω φεύγω έρχομαι πηγαίνω μένω λείπω βγαίνω αλλάζω
    καταφέρνω προσπαθώ'''.split())

# ------------------------------------------------------------------ subjects
# (Greek, English, note on why it is that person or None)
S3SG = [
    (u'αυτός', u'he', None),
    (u'αυτή', u'she', None),
    (u'ο Νίκος', u'Nikos', u'ο Νίκος = he'),
    (u'η Μαρία', u'Maria', u'η Μαρία = she'),
    (u'η μαμά μου', u'my mum', u'η μαμά μου = she'),
    (u'ο μπαμπάς μου', u'my dad', u'ο μπαμπάς μου = he'),
]
S3PL = [
    (u'αυτοί', u'they', None),
    (u'αυτές', u'they (women)', None),
    (u'τα παιδιά', u'the children',
     u'τα παιδιά = they: a neuter plural takes a plural verb'),
    (u'οι γονείς μου', u'my parents', u'οι γονείς μου = they'),
    (u'οι φίλοι μου', u'my friends', u'οι φίλοι μου = they'),
]
PERSONS = ['1sg', '2sg', '3sg', '1pl', '2pl', '3pl']
FIXED = {'1sg': (u'εγώ', u'I'), '2sg': (u'εσύ', u'you (one person)'),
         '1pl': (u'εμείς', u'we'), '2pl': (u'εσείς', u'you (several / polite)')}
ENDING = {'1sg': u'-α', '2sg': u'-ες', '3sg': u'-ε',
          '1pl': u'-αμε', '2pl': u'-ατε', '3pl': u'-αν'}

# Inflected forms used in the time phrases and subjects, traced to a KLIK
# headword (the check below fails on any Greek word with nowhere to trace to).
FRAME_LEMMA = {u'αυτή': u'αυτός', u'αυτόν': u'αυτός', u'αυτές': u'αυτός',
               u'προηγούμενη': u'προηγούμενος', u'προηγούμενο': u'προηγούμενος',
               u'μήνα': u'μήνας', u'φίλοι': u'φίλη', u'την': u'το',
               u'τον': u'το'}

# ------------------------------------------------------------------ rules
GROUP_START = [  # first verb of each block in aoristdeck.VERBS
    (u'βλέπω', 'irr'), (u'γράφω', 'psi'), (u'ανοίγω', 'xi'),
    (u'αγοράζω', 'sigma'), (u'πληρώνω', 'osa'), (u'αγαπάω', 'isa'),
    (u'ξεχνάω', 'asa'), (u'κάθομαι', 'mai'),
]
INTERNAL_AUGMENT = {u'περιγράφω', u'επιστρέφω', u'επιλέγω',
                    u'παραγγέλνω', u'επαναλαμβάνω'}


def rule(pres, sg1, group):
    if group == 'irr' or pres in (u'κάθομαι', u'γίνομαι'):
        return u'irregular aorist (%s → %s): learn it' % (pres, sg1)
    if group == 'psi':
        return (u'-εύω → -εψα' if pres.endswith(u'εύω')
                else u'-φω / -βω / -πω → -ψα')
    if group == 'xi':
        return u'-γω / -χω / -χνω / -ζω → -ξα'
    if group == 'sigma':
        if pres.endswith(u'ίζω'):
            return u'-ίζω → -ισα'
        if pres.endswith(u'άζω'):
            return u'-άζω → -ασα'
        if pres.endswith(u'νω'):
            return u'-νω → -σα'
        return u'aorist in -σα'
    if group == 'osa':
        return u'-ώνω → -ωσα'
    if group == 'isa':
        return u'-άω / -ώ → -ησα'
    if group == 'asa':
        return u'-άω → -%sσα (not -ησα)' % (u'ε' if u'εσα' in sg1 else u'α')
    if group == 'mai':
        return u'-μαι verb: aorist in -ηκα'
    raise ValueError(group)


def augment_note(pres, forms, key):
    sg1, pl1 = forms['1sg'], forms['1pl']
    if pres in INTERNAL_AUGMENT:
        return (u'the augment inside the word drops in the plural'
                if key in ('1pl', '2pl') else
                u'augment inside the word, after the prefix')
    if sg1[0] in u'έή' and pl1[0] not in u'έή' and deaccent(pres[0]) != u'ε':
        return (u'no %s-: the stress moves right, so the augment drops'
                % sg1[0] if key in ('1pl', '2pl') else
                u'%s- added to carry the stress, 3rd syllable from the end'
                % sg1[0])
    return None


def cap(t):
    return t[0].upper() + t[1:]


def spoken_3pl(forms):
    return forms['1pl'][:-3] + u'ανε'


def main():
    klik = klik_forms()
    group, verbs = None, []
    starts = dict(GROUP_START)
    for pres, sg1, pl1, en in VERBS:
        group = starts.get(pres, group)
        if pres not in SKIP:
            verbs.append((pres, sg1, pl1, en, group))

    # check the present tense against the hand-written gold
    for lemma, want in PRESENT_GOLD.items():
        got = u' '.join(present(lemma))
        assert got == want, (lemma, got)

    # the cards left over after 3 per verb-person go to the irregular verbs,
    # one person at a time so every person ends up with the same count
    irr = [v[0] for v in verbs if v[4] == 'irr']
    extra = Counter()
    for k in range(TOTAL - 18 * len(verbs)):
        extra[(irr[k % len(irr)], PERSONS[(k + k // len(irr)) % 6])] += 1
    cards, c3s, c3p, cadv = [], 0, 0, 0
    for vi, (pres, sg1, pl1, en, grp) in enumerate(verbs):
        aor = paradigm(sg1, pl1)
        check(pres, aor)
        prs = dict(zip(PERSONS, present(pres)))
        if pres in LONG_ONLY:
            pool = LONG
        elif pres in ANY_SPAN:
            pool = SHORT + LONG
        else:
            pool = SHORT
        for pi, key in enumerate(PERSONS):
            n = 3 + extra[(pres, key)]
            for j in range(n):
                adv = pool[(cadv + j * 2) % len(pool)] if len(pool) > 6 \
                    else pool[(cadv + j) % len(pool)]
                if key == '3sg':
                    subj = S3SG[c3s % len(S3SG)]
                    c3s += 1
                elif key == '3pl':
                    subj = S3PL[c3p % len(S3PL)]
                    c3p += 1
                else:
                    subj = FIXED[key] + (None,)
                cards.append((pres, key, adv, subj, prs[key], aor, en, grp))
            cadv += 1

    assert len(cards) == TOTAL, len(cards)
    per = Counter(c[1] for c in cards)
    assert all(per[k] == TOTAL // 6 for k in PERSONS), per

    out, fronts, unknown = [], set(), Counter()
    allowed = klik | set(deaccent(w.lower()) for w in FRAME_LEMMA)
    for i, (pres, key, adv, subj, pform, aor, en, grp) in enumerate(cards, 1):
        now, past, past_en = adv
        sgr, sen, snote = subj
        front = cap(u'%s %s %s.' % (now, sgr, pform))
        back = cap(u'%s %s %s.' % (past, sgr, aor[key]))
        assert front not in fronts, front
        fronts.add(front)
        bits = [u'%s → %s' % (pform, aor[key])]
        if not (grp == 'irr' and key == '1sg'):
            bits.append(rule(pres, aor['1sg'], grp))
        if snote:
            bits.append(snote)
        bits.append(u'%s %s' % (sgr if key in FIXED else
                                (u'αυτός/αυτή' if key == '3sg' else u'αυτοί'),
                                ENDING[key]))
        a = augment_note(pres, aor, key)
        if a:
            bits.append(a)
        if key == '3pl':
            bits.append(u'spoken: %s' % spoken_3pl(aor))
        bits.append(u'%s → %s' % (now, past))
        if en.startswith(u'was ') and key not in ('1sg', '3sg'):
            en = u'were' + en[3:]
        eng = cap(u'%s %s %s.' % (past_en, sen, en))
        out.append(u'%d\n%s\n%s\n%s — %s\n' % (i, front, back, eng,
                                                u' · '.join(bits)))
        # every Greek word on both sides must trace to KLIK or to this deck
        own = set(deaccent(w.lower()) for w in list(aor.values()) +
                  list(prs_of(pres)))
        for w in GREEK.findall(front + u' ' + back):
            d = deaccent(w.lower())
            if d not in allowed and d not in own:
                unknown[w] += 1
    assert not unknown, unknown
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(out))
    print('%d verbs, %d cards -> %s' % (len(verbs), len(out), OUT))
    print('per person:', dict(per))
    print('time words:', Counter(c[2][0] for c in cards).most_common())


def prs_of(lemma):
    return present(lemma)


if __name__ == '__main__':
    main()
