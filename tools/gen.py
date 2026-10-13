# -*- coding: utf-8 -*-
"""Build the article + adjective + noun fill-in deck."""
import io, random, sys
from greeklex import decline_noun, decline_adj, definite, indefinite, deaccent
from data2 import NOUNS, ADJS, NO_MASS, BLOCK

GENDER = {'M': 'm', 'F': 'f', 'N': 'n'}
GENDER_EN = {'m': u'masculine', 'f': u'feminine', 'n': u'neuter'}
CLASS_LABEL = {
    'M1': u'M1 · -ας', 'M2': u'M2 · -ης', 'M3': u'M3 · -ος',
    'F1': u'F1 · -α', 'F2': u'F2 · -η', 'F3': u'F3 · -ση/-ξη/-ψη',
    'F4': u'F4 · -ος feminine',
    'N1': u'N1 · -ο', 'N2': u'N2 · -ι', 'N3': u'N3 · -μα', 'N4': u'N4 · -ος neuter',
}
CASE_EN = {'nom': u'nominative', 'acc': u'accusative', 'gen': u'genitive'}
NUM_EN = {'sg': u'singular', 'pl': u'plural'}

GR_AGREE = {u'{AR}': (u'αρέσει', u'αρέσουν'), u'{KOST}': (u'κοστίζει', u'κοστίζουν'),
            u'{EIN}': (u'είναι', u'είναι'), u'{DOUL}': (u'δουλεύει', u'δουλεύουν'),
            u'{ARX}': (u'άρχισε', u'άρχισαν'), u'{TEL}': (u'τελείωσε', u'τελείωσαν'),
            u'{PEZ}': (u'παίζει', u'παίζουν'), u'{VOITH}': (u'με βοήθησε', u'με βοήθησαν'),
            u'{ANOIX}': (u'άνοιξε', u'άνοιξαν'), u'{POUL}': (u'πουλάει', u'πουλάνε'),
            u'{PON}': (u'Πονάει', u'Πονάνε')}
EN_AGREE = {u'{V}': (u'is', u'are'), u'{VW}': (u'was', u'were'),
            u'{COST}': (u'costs', u'cost'), u'{WORK}': (u'works', u'work'),
            u'{BEGAN}': (u'began', u'began'), u'{PLAY}': (u'is playing', u'are playing'),
            u'{HELP}': (u'helped', u'helped'), u'{FIN}': (u'finished', u'finished')}

# (greek prefix, greek suffix, english prefix, english suffix,
#  case, numbers, articles, tags, role)
T = [
 # ---- nominative: subject -------------------------------------------------
 (u'', u' {EIN} εδώ.', u'', u' {V} here.',
  'nom', 'sg pl', 'def', 'obj plc per anm fod txt veh clo nat', u'the subject of the sentence'),
 (u'Πού {EIN} ', u';', u'Where {V} ', u'?',
  'nom', 'sg pl', 'def', 'obj plc per anm txt veh clo', u'the subject of the question'),
 (u'Μου {AR} πολύ ', u'.', u'I like ', u' very much.',
  'nom', 'sg pl', 'def', 'obj plc fod txt nat anm clo veh evt idea feel', u'the subject of αρέσει, the thing that pleases me'),
 (u'Εδώ {EIN} ', u'.', u'Here {V} ', u'.',
  'nom', 'sg pl', 'def', 'obj plc txt fod', u'the subject of the sentence'),
 (u'', u' {KOST} πολλά χρήματα.', u'', u' {COST} a lot of money.',
  'nom', 'sg pl', 'def', 'obj clo veh fod plc', u'the subject of the sentence'),
 (u'Αυτό {EIN} ', u'.', u'This is ', u'.',
  'nom', 'sg', 'indef', 'obj fod txt clo plc anm idea', u'the complement of είμαι, which stays in the nominative'),
 (u'', u' {EIN} στο γραφείο.', u'', u' {V} on the desk.',
  'nom', 'sg pl', 'def', 'obj fod txt', u'the subject of the sentence'),
 (u'', u' {ARX} χθες.', u'', u' {BEGAN} yesterday.',
  'nom', 'sg pl', 'def', 'evt tim wrk', u'the subject of the sentence'),
 (u'', u' {TEL} νωρίς.', u'', u' {FIN} early.',
  'nom', 'sg pl', 'def', 'evt tim wrk', u'the subject of the sentence'),
 (u'', u' {DOUL} εδώ.', u'', u' {WORK} here.',
  'nom', 'sg pl', 'def', 'per', u'the subject of the sentence'),
 (u'', u' {EIN} πολύ μακριά.', u'', u' {V} very far away.',
  'nom', 'sg pl', 'def', 'plc', u'the subject of the sentence'),
 (u'', u' {VOITH} πολύ.', u'', u' {HELP} me a lot.',
  'nom', 'sg pl', 'def', 'per', u'the subject of the sentence'),
 (u'', u' {PEZ} έξω.', u'', u' {PLAY} outside.',
  'nom', 'pl', 'def', 'per anm', u'the subject of the sentence'),
 # ---- accusative: direct object ------------------------------------------
 (u'Βλέπω ', u'.', u'I see ', u'.',
  'acc', 'sg pl', 'def indef', 'obj plc per anm nat txt veh clo bdy', u'the direct object of Βλέπω'),
 (u'Θέλω ', u'.', u'I want ', u'.',
  'acc', 'sg pl', 'def indef', 'obj fod txt clo idea wrk feel', u'the direct object of Θέλω'),
 (u'Αγοράζω ', u'.', u'I am buying ', u'.',
  'acc', 'sg pl', 'def indef', 'obj fod clo veh txt', u'the direct object of Αγοράζω'),
 (u'Ψάχνω ', u'.', u'I am looking for ', u'.',
  'acc', 'sg pl', 'def indef', 'obj plc per txt idea wrk', u'the direct object of Ψάχνω'),
 (u'Έχουμε ', u'.', u'We have ', u'.',
  'acc', 'sg pl', 'def indef', 'obj fod txt idea plc veh clo anm', u'the direct object of Έχουμε'),
 (u'Διαβάζω ', u'.', u'I am reading ', u'.',
  'acc', 'sg pl', 'def indef', 'txt', u'the direct object of Διαβάζω'),
 (u'Τρώμε ', u'.', u'We are eating ', u'.',
  'acc', 'sg pl', 'def indef', 'fod', u'the direct object of Τρώμε'),
 (u'Πίνω ', u'.', u'I am drinking ', u'.',
  'acc', 'sg', 'def indef', 'fod', u'the direct object of Πίνω'),
 (u'Ξέρω ', u'.', u'I know ', u'.',
  'acc', 'sg pl', 'def', 'per plc idea txt lng wrk', u'the direct object of Ξέρω'),
 (u'Περιμένω ', u'.', u'I am waiting for ', u'.',
  'acc', 'sg pl', 'def', 'per evt tim wrk', u'the direct object of Περιμένω'),
 (u'Προτιμώ ', u'.', u'I prefer ', u'.',
  'acc', 'sg pl', 'def', 'obj fod txt clo idea plc', u'the direct object of Προτιμώ'),
 (u'Δεν βρίσκω ', u'.', u'I cannot find ', u'.',
  'acc', 'sg pl', 'def', 'obj txt plc clo', u'the direct object of βρίσκω'),
 (u'Καθαρίζουμε ', u'.', u'We are cleaning ', u'.',
  'acc', 'sg pl', 'def', 'plc obj clo bdy', u'the direct object of Καθαρίζουμε'),
 (u'Ετοιμάζω ', u'.', u'I am preparing ', u'.',
  'acc', 'sg pl', 'def indef', 'fod evt obj', u'the direct object of Ετοιμάζω'),
 (u'', u' {POUL} φτηνά.', u'', u' sells cheaply.',
  'nom', 'sg', 'def', 'plc', u'the subject of the sentence'),
 (u'Μαθαίνω ', u'.', u'I am learning ', u'.',
  'acc', 'sg pl', 'def', 'idea txt lng', u'the direct object of Μαθαίνω'),
 (u'Φοράω ', u'.', u'I am wearing ', u'.',
  'acc', 'sg', 'def indef', 'clo', u'the direct object of Φοράω'),
 (u'{ANOIX} ', u' το πρωί.', u'He opened ', u' in the morning.',
  'acc', 'sg pl', 'def', 'obj plc', u'the direct object of άνοιξε'),
 # ---- accusative: after a preposition ------------------------------------
 (u'Μιλάμε για ', u'.', u'We are talking about ', u'.',
  'acc', 'sg pl', 'def indef', 'idea per plc txt obj evt wrk med feel lng', u'after για, which takes the accusative'),
 (u'Ταξιδεύουμε με ', u'.', u'We are travelling by ', u'.',
  'acc', 'sg', 'def', 'veh', u'after με, which takes the accusative'),
 (u'Το δώρο {EIN} για ', u'.', u'The present is for ', u'.',
  'acc', 'sg pl', 'def indef', 'per', u'after για, which takes the accusative'),
 (u'Ήρθαμε από ', u'.', u'We came from ', u'.',
  'acc', 'sg pl', 'def', 'plc', u'after από, which takes the accusative'),
 (u'Δεν μπορώ χωρίς ', u'.', u'I cannot manage without ', u'.',
  'acc', 'sg pl', 'def', 'obj per idea', u'after χωρίς, which takes the accusative'),
 (u'Η καρέκλα {EIN} μπροστά από ', u'.', u'The chair is in front of ', u'.',
  'acc', 'sg pl', 'def', 'obj plc', u'after μπροστά από, which takes the accusative'),
 (u'Η γάτα κοιμάται κάτω από ', u'.', u'The cat is sleeping under ', u'.',
  'acc', 'sg pl', 'def', 'obj', u'after κάτω από, which takes the accusative'),
 (u'Περπατάμε μέχρι ', u'.', u'We are walking as far as ', u'.',
  'acc', 'sg pl', 'def', 'plc', u'after μέχρι, which takes the accusative'),
 (u'Γράφω για ', u'.', u'I am writing about ', u'.',
  'acc', 'sg pl', 'def', 'idea plc per nat evt feel wrk', u'after για, which takes the accusative'),
 # ---- genitive ------------------------------------------------------------
 (u'Το χρώμα ', u' {EIN} ωραίο.', u'The colour of ', u' is lovely.',
  'gen', 'sg pl', 'def', 'obj clo veh nat bdy', u'the genitive of possession, showing whose colour it is'),
 (u'Η τιμή ', u' {EIN} μεγάλη.', u'The price of ', u' is high.',
  'gen', 'sg pl', 'def', 'obj fod clo veh plc', u'the genitive of possession, showing whose price it is'),
 (u'Το όνομα ', u' {EIN} γνωστό.', u'The name of ', u' is well known.',
  'gen', 'sg pl', 'def', 'plc', u'the genitive of possession, showing whose name it is'),
 (u'Η πόρτα ', u' {EIN} ανοιχτή.', u'The door of ', u' is open.',
  'gen', 'sg pl', 'def', 'plc', u'the genitive of possession, showing whose door it is'),
 (u'Το τέλος ', u' ήταν ωραίο.', u'The ending of ', u' was lovely.',
  'gen', 'sg pl', 'def', 'evt txt tim wrk', u'the genitive of possession, showing whose ending it is'),
 (u'Η αρχή ', u' ήταν δύσκολη.', u'The beginning of ', u' was difficult.',
  'gen', 'sg pl', 'def', 'evt txt tim wrk', u'the genitive of possession, showing whose beginning it is'),
 (u'Η γεύση ', u' {EIN} υπέροχη.', u'The taste of ', u' is wonderful.',
  'gen', 'sg pl', 'def', 'fod', u'the genitive of possession, showing whose taste it is'),
 (u'Η θέα ', u' {EIN} καταπληκτική.', u'The view of ', u' is amazing.',
  'gen', 'sg pl', 'def', 'plc nat', u'the genitive of possession, showing whose view it is'),
 (u'Η ποιότητα ', u' {EIN} καλή.', u'The quality of ', u' is good.',
  'gen', 'sg pl', 'def', 'obj fod', u'the genitive of possession, showing whose quality it is'),
 (u'Η είσοδος ', u' {EIN} εκεί.', u'The entrance of ', u' is over there.',
  'gen', 'sg pl', 'def', 'plc', u'the genitive of possession, showing whose entrance it is'),
 (u'Η ώρα ', u' άλλαξε.', u'The time of ', u' has changed.',
  'gen', 'sg pl', 'def', 'evt', u'the genitive of possession, showing whose time it is'),
 (u'Τα χρώματα ', u' μου αρέσουν.', u'I like the colours of ', u'.',
  'gen', 'pl', 'def', 'obj nat clo', u'the genitive of possession, showing whose colours they are'),
 # genitive with a person: English prefers the possessive -'s
 (u'Το βιβλίο ', u' {EIN} εδώ.', u'', u' book is here.',
  'gen', 'sg pl', 'def', 'per', u'the genitive of possession, showing whose book it is'),
 (u'Τα παιδιά ', u' παίζουν έξω.', u'', u' children are playing outside.',
  'gen', 'sg pl', 'def', 'per', u'the genitive of possession, showing whose children they are'),
 (u'Η δουλειά ', u' {EIN} δύσκολη.', u'', u' job is difficult.',
  'gen', 'sg pl', 'def', 'per', u'the genitive of possession, showing whose job it is'),
 (u'Το αυτοκίνητο ', u' {EIN} καινούριο.', u'', u' car is new.',
  'gen', 'sg pl', 'def', 'per', u'the genitive of possession, showing whose car it is'),
 (u'Πονάει ', u' πολύ.', u'', u' hurts a lot.',
  'nom', 'sg', 'def', 'bdy med', u'the subject of the sentence'),
 (u'Έχω ', u' από χθές.', u'I have had ', u' since yesterday.',
  'acc', 'sg', 'def indef', 'med', u'the direct object of Έχω'),
 (u'Νιώθω ', u'.', u'I feel ', u'.',
  'acc', 'sg', 'def indef', 'feel', u'the direct object of Νιώθω'),
 (u'Δεν ξέρω τη σημασία ', u'.', u'I do not know the meaning of ', u'.',
  'gen', 'sg pl', 'def', 'lng txt', u'the genitive of possession, showing whose meaning it is'),
 (u'Η φωτογραφία ', u' {EIN} όμορφη.', u'The photograph of ', u' is beautiful.',
  'gen', 'sg pl', 'def', 'plc nat', u'the genitive of possession, showing what the photograph shows'),
 (u'Ο αριθμός ', u' {EIN} μεγάλος.', u'The number of ', u' is large.',
  'gen', 'pl', 'def', 'obj evt', u'the genitive of possession, showing what is being counted'),
 (u'Τα παράθυρα ', u' {EIN} ανοιχτά.', u'The windows of ', u' are open.',
  'gen', 'sg pl', 'def', 'plc', u'the genitive of possession, showing whose windows they are'),
 (u'Η ζωή ', u' {EIN} δύσκολη.', u'', u' life is difficult.',
  'gen', 'sg pl', 'def', 'per', u'the genitive of possession, showing whose life it is'),
 (u'Το σπίτι ', u' {EIN} μεγάλο.', u'', u' house is big.',
  'gen', 'sg pl', 'def', 'per', u'the genitive of possession, showing whose house it is'),
 (u'Οι φίλοι ', u' ήρθαν χθες.', u'', u' friends came yesterday.',
  'gen', 'sg pl', 'def', 'per', u'the genitive of possession, showing whose friends they are'),
]

DRINKABLE = set(u'κρασί χυμός ποτό αναψυκτικό'.split())
READABLE = set(u'βιβλίο εφημερίδα περιοδικό άρθρο κείμενο έγγραφο λεξικό σελίδα γράμμα μήνυμα φυλλάδιο ερωτηματολόγιο πιστοποιητικό σημείωση παροιμία διάλογος αγγελία διαφήμιση πρόσκληση ειδοποίηση συνταγή'.split())
EDIBLE = set(u'ψωμί τυρί αβγό γιαούρτι σούπα σαλάτα πατάτα καρότο αγγούρι μαρούλι παντζάρι κουνουπίδι λαχανικό φρούτο μήλο πορτοκάλι κεράσι πεπόνι αμύγδαλο καρύδι φουντούκι φασόλι φακή κοτόπουλο παγωτό γλυκό τούρτα φαγητό γεύμα πρωινό μεσημεριανό βραδινό πάστα ρύζι καλαμπόκι'.split())
# a verb in the frame that only takes certain objects
FRAME_ONLY = ((u'πινω', DRINKABLE), (u'τρωμε', EDIBLE), (u'διαβαζω', READABLE))

# only these can 'begin yesterday' / 'finish early'
BEGINNABLE = set(u'μέρα εβδομάδα μήνας χρονιά έτος καλοκαίρι χειμώνας άνοιξη φθινόπωρο εποχή νύχτα βραδιά απόγευμα διάλειμμα καθυστέρηση διάστημα τάξη δουλειά'.split())

# In a genitive frame the gap is a possessor, so the number of the gap must
# not drive the main verb: 'Ta paidia tou X paizoun', never 'paizei'.
for _t in T:
    if _t[4] != 'gen':
        continue
    for _k, (_s, _p) in GR_AGREE.items():
        if _s != _p and (_k in _t[0] or _k in _t[1]):
            raise AssertionError(
                'genitive frame %r agrees a verb with the gap: %s' % (_t[0], _k))
    for _k, (_s, _p) in EN_AGREE.items():
        if _s != _p and (_k in _t[2] or _k in _t[3]):
            raise AssertionError(
                'genitive frame %r agrees english with the gap: %s' % (_t[2], _k))

VOWEL_START = set('aeiou')
AN_EXCEPTIONS = set(['usual'])


def en_indef(word):
    w = word.lower()
    if w in AN_EXCEPTIONS:
        return u'a'
    return u'an' if w[0] in VOWEL_START else u'a'


def agree(text, table, number):
    i = 0 if number == 'sg' else 1
    for k, v in table.items():
        if k in text:
            text = text.replace(k, v[i])
    return text


def cap(s):
    return s[0].upper() + s[1:] if s else s


def build():
    rng = random.Random(20260928)
    nouns = [dict(zip(('gr', 'cls', 'tag', 'en', 'enpl'), n)) for n in NOUNS]
    adjs = [dict(gr=a[0], fv=a[1], en=a[2], tags=set(a[3].split()), only=set(a[4]))
            for a in ADJS]
    by_tag, by_lemma = {}, {}
    for a in adjs:
        for t in a['tags']:
            by_tag.setdefault(t, []).append(a)
        for lemma in a['only']:
            by_lemma.setdefault(lemma, []).append(a)

    # pre-compute noun paradigms
    for n in nouns:
        n['forms'] = decline_noun(n['gr'], n['cls'])
        n['g'] = GENDER[n['cls'][0]]
        n['key'] = n['gr'] + u'/' + n['g']

    # every noun collects its own pool of usable (template, adjective, …) slots
    pools = dict((n['key'], []) for n in nouns)
    for ti, tpl in enumerate(T):
        case, nums, arts, tags = tpl[4], tpl[5], tpl[6], tpl[7]
        tagset = set(tags.split())
        frame = deaccent((tpl[0] + u' ' + tpl[1]).lower())
        for n in nouns:
            if n['tag'] not in tagset:
                continue
            for a in by_tag.get(n['tag'], []) + by_lemma.get(n['gr'], []):
                if not n['enpl'] and a['gr'] in NO_MASS:
                    continue          # no "big sugar", "new rice"
                if (a['gr'], n['gr']) in BLOCK:
                    continue
                stem = deaccent(a['gr'].lower())[:4]
                if stem in frame:
                    continue          # adjective echoes the template verb
                if stem == deaccent(n['gr'].lower())[:4]:
                    continue          # 'a central centre', 'a home-made home'
                if any(v in frame and n['gr'] not in allowed
                       for v, allowed in FRAME_ONLY):
                    continue          # you cannot drink a dish or read a film
                if (('{arx}' in frame or '{tel}' in frame)
                        and n['tag'] != 'evt' and n['gr'] not in BEGINNABLE):
                    continue
                for num in nums.split():
                    if num == 'pl' and not n['enpl']:
                        continue
                    if (case, num) not in n['forms']:
                        continue
                    for art in arts.split():
                        if art == 'indef' and (num == 'pl' or not n['enpl']):
                            continue
                        pools[n['key']].append((ti, a['gr'], case, num, art))

    noun_of = dict((n['key'], n) for n in nouns)
    adj_of = dict((a['gr'], a) for a in adjs)
    for v in pools.values():
        rng.shuffle(v)

    target = 3000
    order = [n['key'] for n in nouns if pools[n['key']]]
    rng.shuffle(order)
    a_use = {}
    pair_use = {}
    case_use = {'nom': 0, 'acc': 0, 'gen': 0}
    case_cap = (target + 2) // 3      # the three cases get equal shares
    PAIR_CAP = 3          # one adjective+noun pair should not carry the deck
    acap = target // len(adjs) + 4
    # per noun, keep picks as different as possible from each other
    chosen = dict((g, []) for g in order)
    seen_gr, cards = set(), []
    round_no = 0
    while len(cards) < target and round_no < 80:
        round_no += 1
        progressed = False
        for ng in order:
            if len(cards) >= target:
                break
            n = noun_of[ng]
            used = chosen[ng]
            best, best_score = None, None
            for cand in pools[ng]:
                ti, ag, case, num, art = cand
                if cand in used:
                    continue
                if a_use.get(ag, 0) >= acap:
                    continue
                if pair_use.get((ng, ag), 0) >= PAIR_CAP:
                    continue
                if case_use[case] >= case_cap:
                    continue
                # keep the three cases level first, then prefer an unseen
                # case/number, template and adjective for this noun
                score = (case_use[case] // 25,
                         sum(1 for u in used if u[2] == case and u[3] == num),
                         sum(1 for u in used if u[0] == ti),
                         sum(1 for u in used if u[1] == ag),
                         a_use.get(ag, 0))
                if best_score is None or score < best_score:
                    best, best_score = cand, score
            if best is None:
                continue
            ti, ag, case, num, art = best
            card = make(T[ti], n, adj_of[ag], num, art)
            if card is None or card[0] in seen_gr:
                used.append(best)
                continue
            seen_gr.add(card[0])
            used.append(best)
            a_use[ag] = a_use.get(ag, 0) + 1
            pair_use[(ng, ag)] = pair_use.get((ng, ag), 0) + 1
            case_use[case] += 1
            cards.append(card)
            progressed = True
        if not progressed:
            break
    return cards


def make(tpl, n, a, num, art):
    gp, gs, ep, es, case, nums, arts, tags, role = tpl
    g = n['g']
    noun_form = n['forms'][(case, num)]
    adj_form = decline_adj(a['gr'], a['fv'], g, case, num)
    article = (definite(g, case, num, adj_form) if art == 'def'
               else indefinite(g, case, adj_form))
    np = u'%s %s %s' % (article, adj_form, noun_form)

    gr_pre = agree(gp, GR_AGREE, num)
    gr_suf = agree(gs, GR_AGREE, num)
    prompt = gr_pre + u'___' + gr_suf
    answer = gr_pre + np + gr_suf
    if not gr_pre:                   # the phrase opens the sentence
        prompt = cap(prompt)
        answer = cap(answer)
        np, article = cap(np), cap(article)

    # English noun phrase
    head = n['enpl'] if num == 'pl' else n['en']
    if art == 'def':
        en_np = u'the %s %s' % (a['en'], head)
    else:
        en_np = u'%s %s %s' % (en_indef(a['en']), a['en'], head)

    en_pre = agree(ep, EN_AGREE, num)
    en_suf = agree(es, EN_AGREE, num)
    if case == 'gen' and not ep:         # possessive frame: "the old teacher's book"
        poss = en_np + (u"'" if num == 'pl' and head.endswith('s') else u"'s")
        english = cap(poss + en_suf)
    else:
        english = cap(en_pre + en_np + en_suf) if not ep else en_pre + en_np + en_suf

    # The sentence fixes the case, but nothing in it reveals the number or
    # whether the article is definite, so the prompt states both.
    hint = u'(%s + %s %s - %s, %s)' % (
        a['gr'], definite(g, 'nom', 'sg', n['gr']), n['gr'],
        u'definite' if art == 'def' else u'indefinite', NUM_EN[num])
    expl = (u'%s → %s article + adjective + noun, %s %s %s — %s; %s and %s '
            u'agree with %s (%s, %s)'
            % (np, u'definite' if art == 'def' else u'indefinite',
               GENDER_EN[g], CASE_EN[case], NUM_EN[num], role,
               article, adj_form, noun_form, GENDER_EN[g], CLASS_LABEL[n['cls']]))
    return (prompt + u' ' + hint, answer, english + u' — ' + expl,
            n['tag'], case, num, art, n['cls'])


if __name__ == '__main__':
    cards = build()
    out = []
    for i, c in enumerate(cards, 1):
        out.append(u'%d\n%s\n%s\n%s\n' % (i, c[0], c[1], c[2]))
    path = sys.argv[1] if len(sys.argv) > 1 else 'deck.txt'
    body = u'\n'.join(out).rstrip(u'\n') + u'\n'
    # UTF-8 with a BOM and CRLF line endings, like the other dictionaries
    with io.open(path, 'w', encoding='utf-8-sig', newline='\r\n') as fh:
        fh.write(body)
    print('cards: %d' % len(cards))
    from collections import Counter
    for name, idx in (('tag', 3), ('case', 4), ('num', 5), ('art', 6), ('class', 7)):
        print(name, dict(Counter(c[idx] for c in cards).most_common()))
