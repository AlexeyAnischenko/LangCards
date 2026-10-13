# -*- coding: utf-8 -*-
"""Modern Greek inflection for the KLIK A2 noun classes and -ος/-η/-ο adjectives."""

ACUTE = {u'α': u'ά', u'ε': u'έ', u'η': u'ή', u'ι': u'ί', u'ο': u'ό',
         u'υ': u'ύ', u'ω': u'ώ', u'ϊ': u'ΐ', u'ϋ': u'ΰ'}
PLAIN = dict((v, k) for k, v in ACUTE.items())

VOWELS = set(ACUTE) | set(PLAIN)
DIAERESIS = set(u'ϊϋΐΰ')

# first vowel -> set of legal second vowels of a written digraph
DIGRAPH = {u'α': u'ιυ', u'ε': u'ιυ', u'η': u'υ', u'ο': u'ιυ', u'υ': u'ι'}


def strip_accents(word):
    return u''.join(PLAIN.get(c, c) if c not in DIAERESIS or c in u'ΐΰ'
                    else c for c in
                    (u''.join({u'ΐ': u'ϊ', u'ΰ': u'ϋ'}.get(c, c) for c in word)))


def _plain(c):
    return PLAIN.get(c, c)


def nuclei(word):
    """Vowel-nucleus spans, left to right, as (start, end) half-open indices."""
    out = []
    i = 0
    n = len(word)
    while i < n:
        c = word[i]
        if c in VOWELS:
            j = i + 1
            # A digraph needs an *unaccented* first element (ρολόι is ρο-λό-ι,
            # but είναι is εί-ναι) and a second element without a diaeresis.
            if c not in PLAIN and j < n:
                b = word[j]
                if _plain(b) in DIGRAPH.get(c, u'') and b not in DIAERESIS:
                    j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def accent_pos(word):
    """Index into nuclei() of the accented nucleus, or None."""
    for k, (s, e) in enumerate(nuclei(word)):
        if any(ch in PLAIN for ch in word[s:e]):
            return k
    return None


def deaccent(word):
    return u''.join(PLAIN.get(c, c) for c in word)


def accent_on(word, k):
    """Return `word` accented on nucleus k (0-based from the left)."""
    bare = deaccent(word)
    ns = nuclei(bare)
    if not ns or k is None or k < 0 or k >= len(ns):
        return bare
    s, e = ns[k]
    # the acute sits on the last vowel of the nucleus (αι -> αί, ου -> ού)
    p = e - 1
    return bare[:p] + ACUTE.get(bare[p], bare[p]) + bare[p + 1:]


def accent_from_end(word, k):
    """Accent the k-th nucleus counting from the end (1 = ultimate)."""
    ns = nuclei(deaccent(word))
    return accent_on(word, len(ns) - k)


def nsyl(word):
    return len(nuclei(word))


def is_proparoxytone(word):
    p = accent_pos(word)
    return p is not None and len(nuclei(word)) - p == 3


def shift_right(word):
    """Move the accent one nucleus towards the end."""
    p = accent_pos(word)
    if p is None:
        return word
    return accent_on(word, p + 1)


def keep_from_end(source, target):
    """Put target's accent where source's is, counted from the end."""
    p = accent_pos(source)
    if p is None:
        return target
    return accent_from_end(target, len(nuclei(source)) - p)


# --------------------------------------------------------------------------
# nouns
# --------------------------------------------------------------------------
CASES = ('nom', 'acc', 'gen')


def decline_noun(word, cls):
    """word: bare nominative singular. cls: 'M1'..'N4'.

    Returns {('nom'|'acc'|'gen', 'sg'|'pl'): form}; a missing key means the
    form is not safely derivable and must not be used.
    """
    f = {}
    w = word

    if cls in ('M1', 'M2'):          # -ας / -ης : stem + ας/ης, α/η, α/η | ες
        stem = w[:-2]                                    # drop -ας / -ης
        v = u'α' if cls == 'M1' else u'η'
        f[('nom', 'sg')] = keep_from_end(w, stem + v + u'ς')
        f[('acc', 'sg')] = keep_from_end(w, stem + v)
        f[('gen', 'sg')] = keep_from_end(w, stem + v)
        f[('nom', 'pl')] = keep_from_end(w, stem + u'ες')
        f[('acc', 'pl')] = keep_from_end(w, stem + u'ες')
        # genitive plural of M1/M2 is lexically unpredictable -> omitted

    elif cls in ('M3', 'F4'):        # -ος : -ος -ο -ου | -οι -ους -ων
        stem = w[:-2]
        pro = is_proparoxytone(w)
        base = lambda end: keep_from_end(w, stem + end)
        f[('nom', 'sg')] = w
        f[('acc', 'sg')] = base(u'ο')
        f[('gen', 'sg')] = shift_right(base(u'ου')) if pro else base(u'ου')
        f[('nom', 'pl')] = base(u'οι')
        f[('acc', 'pl')] = shift_right(base(u'ους')) if pro else base(u'ους')
        f[('gen', 'pl')] = shift_right(base(u'ων')) if pro else base(u'ων')

    elif cls in ('F1', 'F2'):        # -α / -η : +ς in the genitive singular
        stem = w[:-1]
        v = w[-1]
        f[('nom', 'sg')] = w
        f[('acc', 'sg')] = w
        f[('gen', 'sg')] = keep_from_end(w, stem + deaccent(v) + u'ς')
        f[('nom', 'pl')] = keep_from_end(w, stem + u'ες')
        f[('acc', 'pl')] = keep_from_end(w, stem + u'ες')
        # genitive plural of F1/F2 is lexically unpredictable -> omitted

    elif cls == 'F3':                # -ση/-ξη/-ψη : pl -εις (paroxytone)
        stem = w[:-1]
        f[('nom', 'sg')] = w
        f[('acc', 'sg')] = w
        f[('gen', 'sg')] = keep_from_end(w, stem + u'ης')
        pl = accent_from_end(stem + u'εις', 2)
        f[('nom', 'pl')] = pl
        f[('acc', 'pl')] = pl
        f[('gen', 'pl')] = accent_from_end(stem + u'εων', 3)

    elif cls == 'N1':                # -ο : -ο -ο -ου | -α -α -ων
        stem = w[:-1]
        pro = is_proparoxytone(w)
        base = lambda end: keep_from_end(w, stem + end)
        f[('nom', 'sg')] = w
        f[('acc', 'sg')] = w
        f[('gen', 'sg')] = shift_right(base(u'ου')) if pro else base(u'ου')
        f[('nom', 'pl')] = base(u'α')
        f[('acc', 'pl')] = base(u'α')
        f[('gen', 'pl')] = shift_right(base(u'ων')) if pro else base(u'ων')

    elif cls == 'N2':                # -ι : gen -ιού, pl -ια/-ιά, gen pl -ιών
        stem = w[:-1]
        bare = deaccent(stem)
        oxy = accent_pos(w) == len(nuclei(w)) - 1     # ends in stressed -ί
        f[('nom', 'sg')] = w
        f[('acc', 'sg')] = w
        f[('gen', 'sg')] = accent_from_end(bare + u'ιου', 1)
        # -ί -> -ιά (παιδιά); otherwise -ια is one syllable and the stem keeps
        # its own accent unchanged (σπίτι -> σπίτια, καλοκαίρι -> καλοκαίρια)
        pl = accent_from_end(bare + u'ια', 1) if oxy else stem + u'ια'
        f[('nom', 'pl')] = pl
        f[('acc', 'pl')] = pl
        f[('gen', 'pl')] = accent_from_end(bare + u'ιων', 1)

    elif cls == 'N3':                # -μα : -ματος, -ματα, -μάτων
        stem = w[:-2]
        f[('nom', 'sg')] = w
        f[('acc', 'sg')] = w
        f[('gen', 'sg')] = accent_from_end(stem + u'ματος', 3)
        pl = accent_from_end(stem + u'ματα', 3)
        f[('nom', 'pl')] = pl
        f[('acc', 'pl')] = pl
        f[('gen', 'pl')] = accent_from_end(stem + u'ματων', 2)

    elif cls == 'N4':                # -ος neuter : -ους | -η, -ών
        stem = w[:-2]
        f[('nom', 'sg')] = w
        f[('acc', 'sg')] = w
        f[('gen', 'sg')] = keep_from_end(w, stem + u'ους')
        f[('nom', 'pl')] = keep_from_end(w, stem + u'η')
        f[('acc', 'pl')] = keep_from_end(w, stem + u'η')
        f[('gen', 'pl')] = accent_from_end(stem + u'ων', 1)

    else:
        raise ValueError('unhandled class %s' % cls)

    return f


# --------------------------------------------------------------------------
# adjectives in -ος / -η|-α / -ο  (the accent never moves)
# --------------------------------------------------------------------------
ADJ_END = {
    ('m', 'nom', 'sg'): u'ος', ('m', 'acc', 'sg'): u'ο',  ('m', 'gen', 'sg'): u'ου',
    ('m', 'nom', 'pl'): u'οι', ('m', 'acc', 'pl'): u'ους', ('m', 'gen', 'pl'): u'ων',
    ('n', 'nom', 'sg'): u'ο',  ('n', 'acc', 'sg'): u'ο',  ('n', 'gen', 'sg'): u'ου',
    ('n', 'nom', 'pl'): u'α',  ('n', 'acc', 'pl'): u'α',  ('n', 'gen', 'pl'): u'ων',
}


def decline_adj(masc_nom, fem_vowel, gender, case, number):
    """masc_nom e.g. 'μεγάλος'; fem_vowel is 'η' or 'α'."""
    stem = masc_nom[:-2]
    if gender == 'f':
        if number == 'sg':
            end = fem_vowel + (u'ς' if case == 'gen' else u'')
        else:
            end = u'ων' if case == 'gen' else u'ες'
    else:
        end = ADJ_END[(gender, case, number)]
    return keep_from_end(masc_nom, stem + end)


# --------------------------------------------------------------------------
# articles
# --------------------------------------------------------------------------
KEEP_NU_SINGLE = set(u'κπτξψ')
KEEP_NU_DOUBLE = (u'γκ', u'μπ', u'ντ', u'τσ', u'τζ')


def keeps_nu(nxt):
    """Final -ν of την/στην/έναν survives before a vowel or a stop."""
    if not nxt:
        return True
    w = deaccent(nxt.lower())
    if w[0] in u'αεηιουω':
        return True
    if w[0] in KEEP_NU_SINGLE:
        return True
    return w[:2] in KEEP_NU_DOUBLE


DEF_ART = {
    ('m', 'nom', 'sg'): u'ο',   ('m', 'acc', 'sg'): u'τον', ('m', 'gen', 'sg'): u'του',
    ('m', 'nom', 'pl'): u'οι',  ('m', 'acc', 'pl'): u'τους', ('m', 'gen', 'pl'): u'των',
    ('f', 'nom', 'sg'): u'η',   ('f', 'acc', 'sg'): u'την', ('f', 'gen', 'sg'): u'της',
    ('f', 'nom', 'pl'): u'οι',  ('f', 'acc', 'pl'): u'τις', ('f', 'gen', 'pl'): u'των',
    ('n', 'nom', 'sg'): u'το',  ('n', 'acc', 'sg'): u'το',  ('n', 'gen', 'sg'): u'του',
    ('n', 'nom', 'pl'): u'τα',  ('n', 'acc', 'pl'): u'τα',  ('n', 'gen', 'pl'): u'των',
}

INDEF_ART = {
    ('m', 'nom'): u'ένας', ('m', 'acc'): u'έναν', ('m', 'gen'): u'ενός',
    ('f', 'nom'): u'μια',  ('f', 'acc'): u'μια',  ('f', 'gen'): u'μιας',
    ('n', 'nom'): u'ένα',  ('n', 'acc'): u'ένα',  ('n', 'gen'): u'ενός',
}


def definite(gender, case, number, nxt):
    art = DEF_ART[(gender, case, number)]
    if art == u'την' and not keeps_nu(nxt):
        return u'τη'
    return art


def indefinite(gender, case, nxt):
    return INDEF_ART[(gender, case)]
