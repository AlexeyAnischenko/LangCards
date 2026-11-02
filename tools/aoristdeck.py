# -*- coding: utf-8 -*-
"""Build the A2 aorist deck: the simple past of the KLIK A2 verbs, every person.

Every verb comes from the KLIK A2 word list (`klik-a2-vocabulary.txt`); each
one gets six cards, one per pronoun:

    εγώ έγραψα · εσύ έγραψες · αυτός/αυτή έγραψε · εμείς γράψαμε · εσείς γράψατε · αυτοί έγραψαν

The aorist is not derived by rule. The stem is lexical (πετάω → πέταξα but
ρωτάω → ρώτησα; παίζω → έπαιξα but διαβάζω → διάβασα) and so is the way the
stress and the augment move, so the table below writes two forms by hand for
every verb, the 1st person singular and the 1st person plural:

    γράφω    έγραψα      γράψαμε        έ- augment, dropped in the plural
    βλέπω    είδα        είδαμε         irregular stem, augment stays
    επιστρέφω επέστρεψα  επιστρέψαμε    internal augment, dropped in the plural
    κοιμάμαι κοιμήθηκα   κοιμηθήκαμε    passive aorist, stress moves right

The other four are mechanical: 2sg / 3sg / 3pl swap the 1sg -α for -ες / -ε /
-αν, and 2pl swaps the 1pl -αμε for -ατε. The 3rd person plural also has a
spoken form in -ανε (έγραψανε, γράψανε); the deck uses -αν throughout.

The deck is shuffled and either side can come up first, so each side must be
answerable on its own: the Greek carries the pronoun, and the English names
the present-tense verb (English "started" could be άρχισα or ξεκίνησα) and
says whether "you" is one person or several.

Run from anywhere:  python tools/aoristdeck.py
"""
import io, os, sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
LC = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from writingdeck import latin                                # noqa: E402
from greeklex import accent_pos, nuclei                       # noqa: E402

OUT = os.path.join(LC, 'greek-a2-aorist-verbs.txt')

# (present, aorist 1sg, aorist 1pl, English past)
VERBS = [
    # ---------------------------------------------- irregular stems
    (u'βλέπω', u'είδα', u'είδαμε', u'saw'),
    (u'λέω', u'είπα', u'είπαμε', u'said'),
    (u'έρχομαι', u'ήρθα', u'ήρθαμε', u'came'),
    (u'πηγαίνω', u'πήγα', u'πήγαμε', u'went'),
    (u'τρώω', u'έφαγα', u'φάγαμε', u'ate'),
    (u'πίνω', u'ήπια', u'ήπιαμε', u'drank'),
    (u'παίρνω', u'πήρα', u'πήραμε', u'took'),
    (u'βρίσκω', u'βρήκα', u'βρήκαμε', u'found'),
    (u'μπαίνω', u'μπήκα', u'μπήκαμε', u'went in'),
    (u'βγαίνω', u'βγήκα', u'βγήκαμε', u'went out'),
    (u'ανεβαίνω', u'ανέβηκα', u'ανεβήκαμε', u'went up'),
    (u'κατεβαίνω', u'κατέβηκα', u'κατεβήκαμε', u'went down'),
    (u'δίνω', u'έδωσα', u'δώσαμε', u'gave'),
    (u'βάζω', u'έβαλα', u'βάλαμε', u'put'),
    (u'βγάζω', u'έβγαλα', u'βγάλαμε', u'took off'),
    (u'μαθαίνω', u'έμαθα', u'μάθαμε', u'learned'),
    (u'καταλαβαίνω', u'κατάλαβα', u'καταλάβαμε', u'understood'),
    (u'προλαβαίνω', u'πρόλαβα', u'προλάβαμε', u'made it in time'),
    (u'παθαίνω', u'έπαθα', u'πάθαμε', u'suffered'),
    (u'πεθαίνω', u'πέθανα', u'πεθάναμε', u'died'),
    (u'μένω', u'έμεινα', u'μείναμε', u'stayed'),
    (u'φεύγω', u'έφυγα', u'φύγαμε', u'left'),
    (u'φέρνω', u'έφερα', u'φέραμε', u'brought'),
    (u'καταφέρνω', u'κατάφερα', u'καταφέραμε', u'managed'),
    (u'στέλνω', u'έστειλα', u'στείλαμε', u'sent'),
    (u'παραγγέλνω', u'παρήγγειλα', u'παραγγείλαμε', u'ordered'),
    (u'πλένω', u'έπλυνα', u'πλύναμε', u'washed'),
    (u'πέφτω', u'έπεσα', u'πέσαμε', u'fell'),
    (u'καίω', u'έκαψα', u'κάψαμε', u'burned'),
    (u'περιμένω', u'περίμενα', u'περιμέναμε', u'waited'),
    (u'κάνω', u'έκανα', u'κάναμε', u'did'),
    (u'μπορώ', u'μπόρεσα', u'μπορέσαμε', u'was able to'),
    (u'καλώ', u'κάλεσα', u'καλέσαμε', u'invited'),
    (u'επαναλαμβάνω', u'επανέλαβα', u'επαναλάβαμε', u'repeated'),
    (u'προτείνω', u'πρότεινα', u'προτείναμε', u'suggested'),
    (u'συγκρίνω', u'σύγκρινα', u'συγκρίναμε', u'compared'),
    (u'σερβίρω', u'σέρβιρα', u'σερβίραμε', u'served'),

    # ---------------------------------------------- -ψα (-φω, -βω, -πω, -εύω)
    (u'γράφω', u'έγραψα', u'γράψαμε', u'wrote'),
    (u'περιγράφω', u'περιέγραψα', u'περιγράψαμε', u'described'),
    (u'επιστρέφω', u'επέστρεψα', u'επιστρέψαμε', u'returned'),
    (u'βάφω', u'έβαψα', u'βάψαμε', u'painted'),
    (u'κόβω', u'έκοψα', u'κόψαμε', u'cut'),
    (u'κρύβω', u'έκρυψα', u'κρύψαμε', u'hid'),
    (u'λείπω', u'έλειψα', u'λείψαμε', u'was away'),
    (u'δουλεύω', u'δούλεψα', u'δουλέψαμε', u'worked'),
    (u'μαγειρεύω', u'μαγείρεψα', u'μαγειρέψαμε', u'cooked'),
    (u'ταξιδεύω', u'ταξίδεψα', u'ταξιδέψαμε', u'travelled'),
    (u'χορεύω', u'χόρεψα', u'χορέψαμε', u'danced'),
    (u'πιστεύω', u'πίστεψα', u'πιστέψαμε', u'believed'),
    (u'μαζεύω', u'μάζεψα', u'μαζέψαμε', u'collected'),
    (u'ξοδεύω', u'ξόδεψα', u'ξοδέψαμε', u'spent'),

    # ---------------------------------------------- -ξα (-γω, -χω, -ζω, -χνω)
    (u'ανοίγω', u'άνοιξα', u'ανοίξαμε', u'opened'),
    (u'διαλέγω', u'διάλεξα', u'διαλέξαμε', u'chose'),
    (u'επιλέγω', u'επέλεξα', u'επιλέξαμε', u'selected'),
    (u'τρέχω', u'έτρεξα', u'τρέξαμε', u'ran'),
    (u'προσέχω', u'πρόσεξα', u'προσέξαμε', u'paid attention'),
    (u'δείχνω', u'έδειξα', u'δείξαμε', u'showed'),
    (u'ψάχνω', u'έψαξα', u'ψάξαμε', u'looked for'),
    (u'φτιάχνω', u'έφτιαξα', u'φτιάξαμε', u'made'),
    (u'ρίχνω', u'έριξα', u'ρίξαμε', u'threw'),
    (u'παίζω', u'έπαιξα', u'παίξαμε', u'played'),
    (u'αλλάζω', u'άλλαξα', u'αλλάξαμε', u'changed'),
    (u'κοιτάζω', u'κοίταξα', u'κοιτάξαμε', u'looked at'),
    (u'πετάω', u'πέταξα', u'πετάξαμε', u'threw away'),

    # ---------------------------------------------- -σα (-ζω, -ίζω, -άζω)
    (u'αγοράζω', u'αγόρασα', u'αγοράσαμε', u'bought'),
    (u'διαβάζω', u'διάβασα', u'διαβάσαμε', u'read'),
    (u'ετοιμάζω', u'ετοίμασα', u'ετοιμάσαμε', u'prepared'),
    (u'προετοιμάζω', u'προετοίμασα', u'προετοιμάσαμε', u'prepared in advance'),
    (u'δοκιμάζω', u'δοκίμασα', u'δοκιμάσαμε', u'tried'),
    (u'σπουδάζω', u'σπούδασα', u'σπουδάσαμε', u'studied'),
    (u'νοικιάζω', u'νοίκιασα', u'νοικιάσαμε', u'rented'),
    (u'γιορτάζω', u'γιόρτασα', u'γιορτάσαμε', u'celebrated'),
    (u'διασκεδάζω', u'διασκέδασα', u'διασκεδάσαμε', u'had fun'),
    (u'σχεδιάζω', u'σχεδίασα', u'σχεδιάσαμε', u'planned'),
    (u'νευριάζω', u'νευρίασα', u'νευριάσαμε', u'got angry'),
    (u'σπάζω', u'έσπασα', u'σπάσαμε', u'broke'),
    (u'αρχίζω', u'άρχισα', u'αρχίσαμε', u'began'),
    (u'αποφασίζω', u'αποφάσισα', u'αποφασίσαμε', u'decided'),
    (u'γεμίζω', u'γέμισα', u'γεμίσαμε', u'filled'),
    (u'γνωρίζω', u'γνώρισα', u'γνωρίσαμε', u'got to know'),
    (u'γυρίζω', u'γύρισα', u'γυρίσαμε', u'came back'),
    (u'ελπίζω', u'έλπισα', u'ελπίσαμε', u'hoped'),
    (u'ζωγραφίζω', u'ζωγράφισα', u'ζωγραφίσαμε', u'drew'),
    (u'θυμίζω', u'θύμισα', u'θυμίσαμε', u'reminded'),
    (u'καθαρίζω', u'καθάρισα', u'καθαρίσαμε', u'cleaned'),
    (u'κερδίζω', u'κέρδισα', u'κερδίσαμε', u'won'),
    (u'μετακομίζω', u'μετακόμισα', u'μετακομίσαμε', u'moved house'),
    (u'νομίζω', u'νόμισα', u'νομίσαμε', u'thought'),
    (u'συνεχίζω', u'συνέχισα', u'συνεχίσαμε', u'continued'),
    (u'φροντίζω', u'φρόντισα', u'φροντίσαμε', u'took care of'),
    (u'ψωνίζω', u'ψώνισα', u'ψωνίσαμε', u'did the shopping'),
    (u'ζω', u'έζησα', u'ζήσαμε', u'lived'),
    (u'αφήνω', u'άφησα', u'αφήσαμε', u'left behind'),
    (u'σβήνω', u'έσβησα', u'σβήσαμε', u'switched off'),
    (u'συστήνω', u'σύστησα', u'συστήσαμε', u'introduced'),
    (u'ακούω', u'άκουσα', u'ακούσαμε', u'heard'),
    (u'φτάνω', u'έφτασα', u'φτάσαμε', u'arrived'),
    (u'χάνω', u'έχασα', u'χάσαμε', u'lost'),
    (u'κλείνω', u'έκλεισα', u'κλείσαμε', u'closed'),
    (u'προσθέτω', u'πρόσθεσα', u'προσθέσαμε', u'added'),

    # ---------------------------------------------- -ωσα (-ώνω)
    (u'πληρώνω', u'πλήρωσα', u'πληρώσαμε', u'paid'),
    (u'τελειώνω', u'τελείωσα', u'τελειώσαμε', u'finished'),
    (u'διορθώνω', u'διόρθωσα', u'διορθώσαμε', u'corrected'),
    (u'μεγαλώνω', u'μεγάλωσα', u'μεγαλώσαμε', u'grew up'),
    (u'μαλώνω', u'μάλωσα', u'μαλώσαμε', u'quarrelled'),
    (u'συμπληρώνω', u'συμπλήρωσα', u'συμπληρώσαμε', u'filled in'),
    (u'σημειώνω', u'σημείωσα', u'σημειώσαμε', u'wrote down'),
    (u'κρυώνω', u'κρύωσα', u'κρυώσαμε', u'got cold'),
    (u'στρώνω', u'έστρωσα', u'στρώσαμε', u'laid the table'),
    (u'νιώθω', u'ένιωσα', u'νιώσαμε', u'felt'),

    # ---------------------------------------------- -άω / -ώ  →  -ησα
    (u'αγαπάω', u'αγάπησα', u'αγαπήσαμε', u'loved'),
    (u'απαντάω', u'απάντησα', u'απαντήσαμε', u'answered'),
    (u'βοηθάω', u'βοήθησα', u'βοηθήσαμε', u'helped'),
    (u'ζητάω', u'ζήτησα', u'ζητήσαμε', u'asked for'),
    (u'κρατάω', u'κράτησα', u'κρατήσαμε', u'held'),
    (u'μιλάω', u'μίλησα', u'μιλήσαμε', u'spoke'),
    (u'ξεκινάω', u'ξεκίνησα', u'ξεκινήσαμε', u'set off'),
    (u'ξυπνάω', u'ξύπνησα', u'ξυπνήσαμε', u'woke up'),
    (u'περπατάω', u'περπάτησα', u'περπατήσαμε', u'walked'),
    (u'πουλάω', u'πούλησα', u'πουλήσαμε', u'sold'),
    (u'προτιμάω', u'προτίμησα', u'προτιμήσαμε', u'preferred'),
    (u'ρωτάω', u'ρώτησα', u'ρωτήσαμε', u'asked'),
    (u'σταματάω', u'σταμάτησα', u'σταματήσαμε', u'stopped'),
    (u'συζητάω', u'συζήτησα', u'συζητήσαμε', u'discussed'),
    (u'συναντάω', u'συνάντησα', u'συναντήσαμε', u'met'),
    (u'τραγουδάω', u'τραγούδησα', u'τραγουδήσαμε', u'sang'),
    (u'φιλάω', u'φίλησα', u'φιλήσαμε', u'kissed'),
    (u'χαιρετάω', u'χαιρέτησα', u'χαιρετήσαμε', u'greeted'),
    (u'χτυπάω', u'χτύπησα', u'χτυπήσαμε', u'knocked'),
    (u'κολλάω', u'κόλλησα', u'κολλήσαμε', u'caught (a cold)'),
    (u'ακολουθώ', u'ακολούθησα', u'ακολουθήσαμε', u'followed'),
    (u'αργώ', u'άργησα', u'αργήσαμε', u'was late'),
    (u'εξηγώ', u'εξήγησα', u'εξηγήσαμε', u'explained'),
    (u'επικοινωνώ', u'επικοινώνησα', u'επικοινωνήσαμε', u'got in touch'),
    (u'ευχαριστώ', u'ευχαρίστησα', u'ευχαριστήσαμε', u'thanked'),
    (u'οδηγώ', u'οδήγησα', u'οδηγήσαμε', u'drove'),
    (u'παρακολουθώ', u'παρακολούθησα', u'παρακολουθήσαμε', u'watched'),
    (u'προσπαθώ', u'προσπάθησα', u'προσπαθήσαμε', u'tried hard'),
    (u'συμφωνώ', u'συμφώνησα', u'συμφωνήσαμε', u'agreed'),
    (u'διαφωνώ', u'διαφώνησα', u'διαφωνήσαμε', u'disagreed'),
    (u'τηλεφωνώ', u'τηλεφώνησα', u'τηλεφωνήσαμε', u'phoned'),
    (u'φιλοξενώ', u'φιλοξένησα', u'φιλοξενήσαμε', u'had as a guest'),
    (u'χρησιμοποιώ', u'χρησιμοποίησα', u'χρησιμοποιήσαμε', u'used'),

    # ---------------------------------------------- -άω  →  -ασα / -εσα
    (u'ξεχνάω', u'ξέχασα', u'ξεχάσαμε', u'forgot'),
    (u'περνάω', u'πέρασα', u'περάσαμε', u'passed'),
    (u'πεινάω', u'πείνασα', u'πεινάσαμε', u'got hungry'),
    (u'χαλάω', u'χάλασα', u'χαλάσαμε', u'broke down'),
    (u'φοράω', u'φόρεσα', u'φορέσαμε', u'wore'),
    (u'πονάω', u'πόνεσα', u'πονέσαμε', u'was in pain'),

    # ---------------------------------------------- -μαι  →  passive aorist
    (u'κάθομαι', u'κάθισα', u'καθίσαμε', u'sat down'),
    (u'γίνομαι', u'έγινα', u'γίναμε', u'became'),
    (u'κοιμάμαι', u'κοιμήθηκα', u'κοιμηθήκαμε', u'slept'),
    (u'θυμάμαι', u'θυμήθηκα', u'θυμηθήκαμε', u'remembered'),
    (u'φοβάμαι', u'φοβήθηκα', u'φοβηθήκαμε', u'got scared'),
    (u'λυπάμαι', u'λυπήθηκα', u'λυπηθήκαμε', u'felt sorry'),
    (u'χαίρομαι', u'χάρηκα', u'χαρήκαμε', u'was glad'),
    (u'φαίνομαι', u'φάνηκα', u'φανήκαμε', u'seemed'),
    (u'σκέφτομαι', u'σκέφτηκα', u'σκεφτήκαμε', u'thought about'),
    (u'αισθάνομαι', u'αισθάνθηκα', u'αισθανθήκαμε', u'felt (a feeling)'),
    (u'βρίσκομαι', u'βρέθηκα', u'βρεθήκαμε', u'ended up'),
    (u'επισκέπτομαι', u'επισκέφτηκα', u'επισκεφτήκαμε', u'visited'),
    (u'ενδιαφέρομαι', u'ενδιαφέρθηκα', u'ενδιαφερθήκαμε', u'was interested'),
    (u'χρειάζομαι', u'χρειάστηκα', u'χρειαστήκαμε', u'needed'),
    (u'ξεκουράζομαι', u'ξεκουράστηκα', u'ξεκουραστήκαμε', u'rested'),
    (u'ντύνομαι', u'ντύθηκα', u'ντυθήκαμε', u'got dressed'),
    (u'παντρεύομαι', u'παντρεύτηκα', u'παντρευτήκαμε', u'got married'),
    (u'ονειρεύομαι', u'ονειρεύτηκα', u'ονειρευτήκαμε', u'dreamed'),
]

# Two 3rd-person-singular pronouns, alternated by verb, so both come up.
PERSONS = [
    # key, Greek pronoun, English subject, ending source
    ('1sg', u'εγώ', u'I'),
    ('2sg', u'εσύ', u'you (one person)'),
    ('3sg', None, None),
    ('1pl', u'εμείς', u'we'),
    ('2pl', u'εσείς', u'you (several / polite)'),
    ('3pl', u'αυτοί', u'they'),
]


def paradigm(sg1, pl1):
    assert sg1.endswith(u'α') and pl1.endswith(u'αμε'), (sg1, pl1)
    st, pst = sg1[:-1], pl1[:-3]
    return {'1sg': sg1, '2sg': st + u'ες', '3sg': st + u'ε',
            '1pl': pl1, '2pl': pst + u'ατε', '3pl': st + u'αν'}


def check(present, forms):
    """Exactly one accent per form; the plural stress no further left than the
    3rd syllable from the end (the aorist rule), so a typo in an anchor shows."""
    for k, f in forms.items():
        n = sum(1 for c in f if c in u'άέήίόύώ')
        assert n == 1, (present, k, f)
    for k in ('1pl', '2pl'):
        f = forms[k]
        if f.startswith(u'ήπια'):    # ή-πια-με: ια is one syllable here
            continue
        from_end = len(nuclei(f)) - accent_pos(f)
        assert from_end <= 3, (present, k, f, from_end)


# Forms graded correct in the homework this session: free gold.
GOLD = {
    (u'λείπω', '3sg'): u'έλειψε', (u'κρύβω', '3sg'): u'έκρυψε',
    (u'προσθέτω', '1pl'): u'προσθέσαμε', (u'παίζω', '1pl'): u'παίξαμε',
    (u'επιστρέφω', '2pl'): u'επιστρέψατε', (u'γράφω', '3pl'): u'έγραψαν',
    (u'τρώω', '1pl'): u'φάγαμε', (u'πίνω', '3pl'): u'ήπιαν',
    (u'κοιμάμαι', '2pl'): u'κοιμηθήκατε', (u'βλέπω', '2sg'): u'είδες',
}


def main():
    presents = [v[0] for v in VERBS]
    assert len(set(presents)) == len(presents), 'duplicate verb'
    out, n = [], 0
    by = {}
    for i, (pres, sg1, pl1, en) in enumerate(VERBS):
        forms = paradigm(sg1, pl1)
        check(pres, forms)
        for k, f in forms.items():
            by[(pres, k)] = f
        for key, pron, subj in PERSONS:
            if key == '3sg':
                pron, subj = (u'αυτός', u'he') if i % 2 == 0 else (u'αυτή', u'she')
            gr = u'%s %s' % (pron, forms[key])
            n += 1
            out.append(u'%d\n%s\n%s\n%s %s | %s · aorist\n'
                       % (n, gr, latin(gr), subj, en, pres))
    for k, want in GOLD.items():
        assert by[k] == want, (k, by[k], want)
    fronts = [c.split(u'\n')[1] for c in out]
    assert len(set(fronts)) == len(fronts), 'duplicate front'
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(out))
    print('%d verbs, %d cards -> %s' % (len(VERBS), n, OUT))


if __name__ == '__main__':
    main()
