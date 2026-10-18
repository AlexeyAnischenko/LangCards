# -*- coding: utf-8 -*-
"""Build the ordinals-and-colours deck.

Two topics the A2 syllabus treats as vocabulary but which are really grammar:

  * every ordinal is a plain type-A adjective, so it has to agree - and the
    ordinals of the tens are not built from the modern cardinals at all
    (σαράντα -> τεσσαρακοστός), which is the only part that has to be learnt
    rather than derived;
  * a colour is an adjective too, except for the six loanwords that have no
    Greek ending to change and so never agree with anything.

Card back carries the three genders, because that is the whole decision the
learner has to make, plus the figure spelling (1ος / 1η / 1ο) for ordinals,
which is how they are actually written on a lift button or an address.

Run from anywhere:  python tools/ordcol.py
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

LC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(LC, 'greek-a2-ordinals-colours.txt')

# ------------------------------------------------------------- transcription
# Same scheme as the other decks in this repo, copied rather than imported so
# the generator stands on its own.
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
        two = s[i:i + 2]
        nxt = s[i + 2] if i + 2 < len(s) else u''
        if two in (u'αυ', u'ευ', u'ηυ', u'αύ', u'εύ'):
            v = {u'α': u'a', u'ά': u'a', u'ε': u'e', u'έ': u'e', u'η': u'i'}[two[0]]
            out.append(v + (u'v' if nxt in VOICED or not nxt else u'f'))
            i += 2
            continue
        if two in (u'μπ', u'ντ', u'γκ', u'γγ', u'τσ', u'τζ'):
            first = not out or out[-1] in u' -'
            out.append({u'μπ': u'b' if first else u'mb', u'ντ': u'd' if first else u'nd',
                        u'γκ': u'g' if first else u'ng', u'γγ': u'ng',
                        u'τσ': u'ts', u'τζ': u'tz'}[two])
            i += 2
            continue
        if two in PAIR:
            out.append(PAIR[two])
            i += 2
            continue
        c = s[i]
        if c == u'γ' and s[i + 1:i + 2] in (u'ε', u'ι', u'η', u'υ', u'έ', u'ί', u'ή'):
            out.append(u'y')
            i += 1
            continue
        out.append(SINGLE.get(c, c))
        i += 1
    return u''.join(out)


# ------------------------------------------------------------------ ordinals
# The masculine of every unit and every ten. Everything between them is built
# by juxtaposition - δέκατος τρίτος, εικοστός πρώτος - with BOTH halves
# declining, which is the mistake worth drilling.
UNITS = {
    1:  (u'πρώτος',    u'first'),
    2:  (u'δεύτερος',  u'second'),
    3:  (u'τρίτος',    u'third'),
    4:  (u'τέταρτος',  u'fourth'),
    5:  (u'πέμπτος',   u'fifth'),
    6:  (u'έκτος',     u'sixth'),
    7:  (u'έβδομος',   u'seventh'),
    8:  (u'όγδοος',    u'eighth'),
    9:  (u'ένατος',    u'ninth'),
    10: (u'δέκατος',   u'tenth'),
    11: (u'ενδέκατος', u'eleventh'),
    12: (u'δωδέκατος', u'twelfth'),
}
TENS = {
    10: (u'δέκατος',          u'tenth'),
    20: (u'εικοστός',         u'twentieth'),
    30: (u'τριακοστός',       u'thirtieth'),
    40: (u'τεσσαρακοστός',    u'fortieth'),
    50: (u'πεντηκοστός',      u'fiftieth'),
}
# the ordinal of a ten that cannot be guessed from the modern cardinal
ANCIENT = {30: u'τριάντα', 40: u'σαράντα', 50: u'πενήντα'}

ORD_EN = {1: u'first', 2: u'second', 3: u'third', 4: u'fourth', 5: u'fifth',
          6: u'sixth', 7: u'seventh', 8: u'eighth', 9: u'ninth', 10: u'tenth',
          11: u'eleventh', 12: u'twelfth', 13: u'thirteenth', 14: u'fourteenth',
          15: u'fifteenth', 16: u'sixteenth', 17: u'seventeenth',
          18: u'eighteenth', 19: u'nineteenth', 20: u'twentieth',
          30: u'thirtieth', 40: u'fortieth', 50: u'fiftieth'}

# an ordinal in use, for the numbers where a natural one exists
EXAMPLE = {
    1:  (u'ο πρώτος όροφος', u'the first floor'),
    2:  (u'για δεύτερη φορά', u'for the second time'),
    3:  (u'η τρίτη πόρτα δεξιά', u'the third door on the right'),
    4:  (u'ένα τέταρτο', u'a quarter (of an hour)'),
    5:  (u'στον πέμπτο όροφο', u'on the fifth floor'),
    6:  (u'η έκτη μέρα', u'the sixth day'),
    7:  (u'ο έβδομος μήνας', u'the seventh month'),
    8:  (u'η όγδοη σελίδα', u'the eighth page'),
    9:  (u'το ένατο μάθημα', u'the ninth lesson'),
    10: (u'τα δέκατα γενέθλιά του', u'his tenth birthday'),
    11: (u'η ενδέκατη ώρα', u'the eleventh hour'),
    12: (u'ο δωδέκατος όροφος', u'the twelfth floor'),
    20: (u'ο εικοστός αιώνας', u'the twentieth century'),
    21: (u'ο εικοστός πρώτος αιώνας', u'the twenty-first century'),
    30: (u'η τριακοστή μέρα', u'the thirtieth day'),
    40: (u'τα τεσσαρακοστά του γενέθλια', u'his fortieth birthday'),
    50: (u'η πεντηκοστή φορά', u'the fiftieth time'),
}


def fem(masc):
    """Ordinals are plain type-A adjectives; only the stress tells the two
    endings apart. -στός is end-stressed and takes -ή, everything else -η."""
    return masc[:-2] + (u'ή' if masc.endswith(u'ός') else u'η')


def neut(masc):
    return masc[:-2] + (u'ό' if masc.endswith(u'ός') else u'ο')


def gen_m(masc):
    return masc[:-2] + (u'ού' if masc.endswith(u'ός') else u'ου')


def ordinal(n):
    """(masculine, feminine, neuter) for 1..50."""
    if n in UNITS:
        m = UNITS[n][0]
    elif n in TENS:
        m = TENS[n][0]
    else:
        ten, unit = (n // 10) * 10, n % 10
        head = TENS[ten][0] if ten != 10 else UNITS[10][0]
        m = u'%s %s' % (head, UNITS[unit][0])
    parts = m.split()
    return (m,
            u' '.join(fem(p) for p in parts),
            u' '.join(neut(p) for p in parts))


def en_ordinal(n):
    if n in ORD_EN:
        return ORD_EN[n]
    ten, unit = (n // 10) * 10, n % 10
    if ten == 10:
        return ORD_EN[n]
    return u'%s-%s' % ({20: u'twenty', 30: u'thirty', 40: u'forty',
                        50: u'fifty'}[ten], ORD_EN[unit])


def suffix(n, g):
    """How the figure is written: 1ος / 1η / 1ο - the ending of the LAST word."""
    last = ordinal(n)[g].split()[-1]
    return u'%d%s' % (n, last[-2:] if g == 0 else last[-1:])


def ordinal_cards():
    cards = []
    for n in range(1, 51):
        m, f, nt = ordinal(n)
        back = [u'%s — ordinal number' % en_ordinal(n),
                u'm  ο %s' % m,
                u'f  η %s' % f,
                u'n  το %s' % nt,
                u'gen  του %s' % u' '.join(gen_m(p) for p in m.split()),
                u'written  %s / %s / %s' % (suffix(n, 0), suffix(n, 1), suffix(n, 2))]
        if len(m.split()) == 2:
            back.append(u'⚠ both halves take the ending')
        if n in ANCIENT:
            back.append(u'⚠ not built from %s — learn it as a word' % ANCIENT[n])
        if n in EXAMPLE:
            back.append(u'%s — %s' % EXAMPLE[n])
        cards.append((m, back))
    return cards


# ------------------------------------------------------------------- colours
# (greek, english, kind, note-lines)
AGREE = u'agrees'
NEVER = u'never changes'
IOTA = u'one form'

COLOURS = [
    (u'άσπρος', u'white', AGREE, u'A', u'άσπρος / άσπρη / άσπρο',
     u'το άσπρο πουκάμισο · η άσπρη πόρτα · τα άσπρα μαλλιά'),
    (u'λευκός', u'white (formal, written)', AGREE, u'A', u'λευκός / λευκή / λευκό',
     u'το λευκό κρασί · η Λευκωσία'),
    (u'μαύρος', u'black', AGREE, u'A', u'μαύρος / μαύρη / μαύρο',
     u'ο μαύρος καφές · η μαύρη τσάντα · τα μαύρα παπούτσια'),
    (u'κόκκινος', u'red', AGREE, u'A', u'κόκκινος / κόκκινη / κόκκινο',
     u'το κόκκινο κρασί · η κόκκινη μπλούζα · το κόκκινο φανάρι'),
    (u'πράσινος', u'green', AGREE, u'A', u'πράσινος / πράσινη / πράσινο',
     u'τα πράσινα μάτια · το πράσινο φανάρι'),
    (u'κίτρινος', u'yellow', AGREE, u'A', u'κίτρινος / κίτρινη / κίτρινο',
     u'ο κίτρινος ήλιος · τα κίτρινα λουλούδια'),
    (u'γαλάζιος', u'light blue, sky blue', AGREE, u'B ⚠ -α not -η',
     u'γαλάζιος / γαλάζια / γαλάζιο',
     u'έχει γαλάζια μάτια — she has blue eyes'),
    (u'γκρίζος', u'grey', AGREE, u'B ⚠ -α not -η', u'γκρίζος / γκρίζα / γκρίζο',
     u'τα γκρίζα μαλλιά · μια γκρίζα μέρα'),
    (u'χρυσός', u'gold, golden', AGREE, u'A', u'χρυσός / χρυσή / χρυσό',
     u'το χρυσό μετάλλιο — the gold medal | ένα χρυσό δαχτυλίδι — a gold ring | '
     u'ο χρυσός = gold, the metal'),
    (u'ασημένιος', u'silver', AGREE, u'B ⚠ -α not -η',
     u'ασημένιος / ασημένια / ασημένιο',
     u'το ασημένιο μετάλλιο — the silver medal | '
     u'ένα ασημένιο δαχτυλίδι — a silver ring | το ασήμι = silver, the metal'),
    (u'χάλκινος', u'bronze, copper', AGREE, u'A', u'χάλκινος / χάλκινη / χάλκινο',
     u'το χάλκινο μετάλλιο — the bronze medal | ο χαλκός = copper | '
     u'⚠ μπρούντζινος is the material (ένα μπρούντζινο άγαλμα), never the medal'),
    (u'καστανός', u'brown (hair and eyes)', AGREE, u'A',
     u'καστανός / καστανή / καστανό',
     u'έχει καστανά μάτια — he has brown eyes'),
    (u'ξανθός', u'blond, fair', AGREE, u'-ός / -ιά / -ό',
     u'ξανθός / ξανθιά (ξανθή) / ξανθό',
     u'είναι ξανθιά — she is blonde'),
    (u'μελαχρινός', u'dark-haired, olive-skinned', AGREE, u'A',
     u'μελαχρινός / μελαχρινή / μελαχρινό',
     u'ο θείος είναι ψηλός και μελαχρινός'),
    (u'μπλε', u'blue', NEVER, None, None,
     u'ο μπλε τοίχος · η μπλε μπλούζα · το μπλε αυτοκίνητο · τα μπλε αυτοκίνητα'),
    (u'γκρι', u'grey', NEVER, None, None,
     u'το γκρι παντελόνι · οι γκρι τοίχοι  (γκρίζος is the one that agrees)'),
    (u'καφέ', u'brown', NEVER, None, None,
     u'τα καφέ παπούτσια · μια καφέ τσάντα  (καστανός for hair and eyes)'),
    (u'ροζ', u'pink', NEVER, None, None,
     u'το ροζ φόρεμα · τα ροζ λουλούδια'),
    (u'μωβ', u'purple', NEVER, None, None, u'μια μωβ μπλούζα · τα μωβ λουλούδια'),
    (u'μπεζ', u'beige', NEVER, None, None, u'ένα μπεζ παλτό'),
    (u'πορτοκαλί', u'orange', IOTA, None, None,
     u'ένα πορτοκαλί μπλουζάκι · μια πορτοκαλί τσάντα | '
     u'⚠ η πορτοκαλιά = the orange TREE'),
    (u'θαλασσί', u'sea blue, turquoise', IOTA, None, None, u'ένα θαλασσί φόρεμα'),
    (u'ασημί', u'silver (the colour)', IOTA, None, None,
     u'ένα ασημί αυτοκίνητο — a silver car | '
     u'⚠ ασημένιος = made of silver; ασημί = silver-coloured'),
    (u'βυσσινί', u'cherry red, maroon', IOTA, None, None, u'ένα βυσσινί παλτό'),
]

EXTRA = [
    (u'το χρώμα', u'the colour — noun, neuter, -μα type',
     [u'τα χρώματα — the colours',
      u'Το αγαπημένο μου χρώμα είναι το πράσινο. — My favourite colour is green.',
      u'το κόκκινο, το μπλε — a colour on its own takes το']),
    (u'Τι χρώμα είναι;', u'What colour is it?',
     [u'also Τι χρώμα έχει;',
      u'the answer agrees with the NOUN, not with χρώμα',
      u'Τι χρώμα είναι η μπλούζα σου; — Είναι κόκκινη.',
      u'Τι χρώμα είναι τα παπούτσια σου; — Είναι μαύρα.']),
    (u'ανοιχτό', u'light (shade)',
     [u'ανοιχτό μπλε, ανοιχτό γκρι — stays neuter before an invariable colour',
      u'ανοιχτοπράσινος, ανοιχτογάλαζος — as one word it declines normally']),
    (u'σκούρο', u'dark (shade)',
     [u'σκούρο μπλε, σκούρο καφέ — stays neuter before an invariable colour',
      u'σκουροπράσινος, σκουροκόκκινος — as one word it declines normally',
      u'ένα σκούρο μπλε παντελόνι — a dark blue pair of trousers']),
    (u'το μετάλλιο', u'the medal — noun, neuter',
     [u'τα μετάλλια — the medals',
      u'the colour is neuter too: το χρυσό / ασημένιο / χάλκινο μετάλλιο',
      u'Πήρε το χρυσό. — He/She took the gold.',
      u'Κέρδισε δύο χρυσά μετάλλια. — He/She won two gold medals.']),
    (u'ασπρόμαυρος', u'black and white',
     [u'ασπρόμαυρος / ασπρόμαυρη / ασπρόμαυρο',
      u'⚠ Greek says it the other way round — white-black',
      u'μια ασπρόμαυρη φωτογραφία — a black-and-white photo']),
]


def colour_cards():
    cards = []
    for greek, en, kind, typ, forms, example in COLOURS:
        back = [u'%s — colour' % en]
        if kind == AGREE:
            back.append(u'agrees — the %s type' % typ if typ.startswith(u'-')
                        else u'agrees — type %s' % typ)
            back.append(forms)
        elif kind == NEVER:
            back.append(u'⚠ never changes — same in every gender, case and number')
        else:
            back.append(u'one form for everything (neuter of an old -ής / -ιά / -ί word)')
        back += [p.strip() for p in example.split(u'|')]
        cards.append((greek, back))
    for greek, en, lines in EXTRA:
        cards.append((greek, [en] + lines))
    return cards


def main():
    cards = ordinal_cards() + colour_cards()
    out = []
    for i, (front, back) in enumerate(cards, 1):
        out.append(u'%d\n%s\n%s\n%s\n' % (i, front, translit(front), u' | '.join(back)))
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(out))

    print(u'%d cards -> %s' % (len(cards), OUT))
    print(u'   ordinals %d   colours %d' % (len(ordinal_cards()), len(colour_cards())))
    print()
    for want in (u'πρώτος', u'όγδοος', u'δέκατος τρίτος', u'εικοστός πρώτος',
                 u'τεσσαρακοστός', u'πεντηκοστός', u'κόκκινος', u'μπλε',
                 u'πορτοκαλί', u'Τι χρώμα είναι;'):
        for front, back in cards:
            if front == want:
                print(u'   %s  [%s]' % (front, translit(front)))
                for line in back:
                    print(u'        %s' % line)
                print()
                break


if __name__ == '__main__':
    main()
