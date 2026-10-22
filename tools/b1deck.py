# -*- coding: utf-8 -*-
"""Build the B1 additions deck: words the B1 book uses that A2 never did.

The candidate list came out of a frequency count over the B1 text, but a raw
count is not usable on its own. Two filters had to run before this script:

  * a spaCy pass over whole sentences, so inflected forms collapse onto one
    lemma and a part of speech is attached;
  * agents, to repair what both the OCR and the parser got wrong - the parser
    invents masculine -ος lemmas for neuter nouns (βιβλίος for το βιβλίο) and
    returns inflected forms as lemmas (μπορής for μπορώ), while the OCR eats a
    word-initial η and reads it as π (πλικία for η ηλικία).

Which leaves the job here: subtract A2 **again**, now against the corrected
lemmas. That second subtraction is the point. A word like μπορώ was already in
the A2 dictionary, but the first pass compared against "μπορής" and so let it
through; only once the lemma is right does the word match and drop out.

Run from anywhere:  python tools/b1deck.py
"""
import io, os, re, sys, glob, json, unicodedata, collections

sys.stdout.reconfigure(encoding='utf-8')

LC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = (r'C:/Users/ALEKSE~1.ANI/AppData/Local/Temp/claude/C--Work-Personal/'
      r'76763e5c-92fc-4381-9832-65f387224c81/scratchpad')
B1 = os.path.join(SC, 'b1')
OUT = os.path.join(LC, 'greek-b1-additions-3times.txt')

ART = (u'ο', u'η', u'το', u'οι', u'τα')

# ------------------------------------------------------------- transcription
VOICED = set(u'αεηιουωάέήίόύώβγδζλμνρ')
PAIR = {u'αι': u'e', u'ει': u'i', u'οι': u'i', u'υι': u'i', u'ου': u'ou',
        u'αί': u'e', u'εί': u'i', u'οί': u'i', u'ού': u'ou'}
SINGLE = {
    u'α': u'a', u'β': u'v', u'γ': u'g', u'δ': u'd', u'ε': u'e', u'ζ': u'z',
    u'η': u'i', u'θ': u'th', u'ι': u'i', u'κ': u'k', u'λ': u'l', u'μ': u'm',
    u'ν': u'n', u'ξ': u'x', u'ο': u'o', u'π': u'p', u'ρ': u'r', u'σ': u's',
    u'ς': u's', u'τ': u't', u'υ': u'i', u'φ': u'f', u'χ': u'h', u'ψ': u'ps',
    u'ω': u'o', u'ά': u'a', u'έ': u'e', u'ή': u'i', u'ί': u'i', u'ό': u'o',
    u'ύ': u'i', u'ώ': u'o', u'ϊ': u'i', u'ϋ': u'i', u'ΐ': u'i', u'ΰ': u'i',
}


def translit(text):
    s = text.lower()
    out, i = [], 0
    while i < len(s):
        two, nxt = s[i:i + 2], s[i + 2] if i + 2 < len(s) else u''
        if two in (u'αυ', u'ευ', u'ηυ', u'αύ', u'εύ'):
            v = {u'α': u'a', u'ά': u'a', u'ε': u'e', u'έ': u'e', u'η': u'i'}[two[0]]
            out.append(v + (u'v' if nxt in VOICED or not nxt else u'f')); i += 2; continue
        if two in (u'μπ', u'ντ', u'γκ', u'γγ', u'τσ', u'τζ'):
            first = not out or out[-1] in u' -'
            out.append({u'μπ': u'b' if first else u'mb', u'ντ': u'd' if first else u'nd',
                        u'γκ': u'g' if first else u'ng', u'γγ': u'ng',
                        u'τσ': u'ts', u'τζ': u'tz'}[two]); i += 2; continue
        if two in PAIR:
            out.append(PAIR[two]); i += 2; continue
        c = s[i]
        if c == u'γ' and s[i + 1:i + 2] in (u'ε', u'ι', u'η', u'υ', u'έ', u'ί', u'ή'):
            out.append(u'y'); i += 1; continue
        out.append(SINGLE.get(c, c)); i += 1
    return u''.join(out)


def bare(s):
    s = unicodedata.normalize('NFD', s.lower())
    return u''.join(c for c in s if unicodedata.category(c) != 'Mn')


def head(lemma):
    """The lemma without its article, for matching against A2."""
    t = lemma.split()
    return bare(t[-1]) if len(t) > 1 and t[0] in ART else bare(lemma)


def a2_known():
    seen = set()
    p = os.path.join(SC, 'dictionary.json')
    for r in json.loads(io.open(p, encoding='utf-8').read()):
        for w in [r['lemma']] + list(r.get('forms') or []):
            for part in w.split():
                if part not in ART:
                    seen.add(bare(part))
    for f in glob.glob(os.path.join(LC, '*.txt')):
        if os.path.basename(f) == os.path.basename(OUT):
            continue
        for b in io.open(f, encoding='utf-8', errors='replace').read().split('\n\n'):
            lines = b.split('\n')
            if len(lines) >= 2:
                for part in lines[1].split():
                    p2 = part.strip(u'.,;:!?()«»"\'·')
                    if p2 and p2 not in ART:
                        seen.add(bare(p2))
    return seen


# the agents flagged basics in their own words; honour that too
BASIC = re.compile(u'\\bA1\\b|\\bA1/A2\\b|\\bA2\\b', re.I)


def main():
    words = json.loads(io.open(os.path.join(B1, 'wf_words.json'),
                               encoding='utf-8').read())
    cand = {c['lemma']: c for c in json.loads(
        io.open(os.path.join(B1, 'b1_candidates.json'), encoding='utf-8').read())}

    print('agent results            : %d' % len(words))
    real = [w for w in words if w.get('verdict') == 'word' and w.get('lemma')]
    print('  real words             : %d' % len(real))
    print('  rejected as OCR damage : %d' % (len(words) - len(real)))

    known = a2_known()
    print('A2 surface forms known   : %d' % len(known))

    merged = collections.OrderedDict()
    dropped_a2, dropped_flag = [], []
    for w in real:
        lem = w['lemma'].strip()
        h = head(lem)
        if h in known:
            dropped_a2.append(lem)
            continue
        if BASIC.search(w.get('note') or u''):
            dropped_flag.append(lem)
            continue
        src = cand.get(w['candidate'], {})
        if lem in merged:
            m = merged[lem]
            m['n'] += src.get('n', 0)
            m['forms'] |= set(src.get('forms') or [])
        else:
            merged[lem] = {
                'lemma': lem, 'pos': w.get('pos') or '', 'en': w.get('en') or '',
                'note': (w.get('note') or '').strip(),
                'n': src.get('n', 0), 'forms': set(src.get('forms') or []),
            }

    print('  dropped, already in A2 : %d' % len(dropped_a2))
    print('  dropped, agent said A1/A2: %d' % len(dropped_flag))
    print('  distinct lemmas left   : %d' % len(merged))

    rows = sorted(merged.values(), key=lambda r: (-r['n'], bare(r['lemma'])))
    rows = [r for r in rows if r['n'] >= 3]
    print('  seen 3+ times          : %d  <- the deck' % len(rows))

    out = []
    for i, r in enumerate(rows, 1):
        back = [u'%s — %s' % (r['en'], r['pos'] or 'word')]
        forms = sorted(f for f in r['forms'] if bare(f) != head(r['lemma']))
        if forms:
            back.append(u'as printed: ' + u', '.join(forms[:6]))
        back.append(u'seen %d times in the B1 book' % r['n'])
        if r['note'] and not BASIC.search(r['note']):
            back.append(u'⚠ ' + r['note'])
        out.append(u'%d\n%s\n%s\n%s\n' % (i, r['lemma'], translit(r['lemma']),
                                          u' | '.join(back)))
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(out))

    by_pos = collections.Counter(r['pos'] for r in rows)
    print('\n%d cards -> %s' % (len(rows), OUT))
    print('by part of speech: %s' % dict(by_pos))
    print('\ntop 25:')
    for r in rows[:25]:
        print(u'   %-26s %-10s x%-4d %s' % (r['lemma'], r['pos'], r['n'], r['en'][:42]))


if __name__ == '__main__':
    main()
