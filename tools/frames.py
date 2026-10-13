# -*- coding: utf-8 -*-
"""Sentence frames for the pronoun deck.

A frame is a skeleton with one gap. Everything outside the gap is fixed, or
filled from a curated pool of KLIK nouns; the gap always holds a pronoun,
and the frame alone decides which case that pronoun has to be in.

Everything is in the present tense, so no card asks for a verb form the
deck has not derived from a rule. Each frame is also marked for what it can
talk about: 'h' frames are about people, and leave the neuter out, because
"the waiter asks it" is not a sentence; 't' frames are about things, run in
the third person only, and gloss every gender as English "it".
"""

# (lemma, group, english base, english 3rd singular)
VERBS = {
    u'μένω':        ('A', u'live', u'lives'),
    u'δουλεύω':     ('A', u'work', u'works'),
    u'διαβάζω':     ('A', u'read', u'reads'),
    u'γράφω':       ('A', u'write', u'writes'),
    u'βλέπω':       ('A', u'see', u'sees'),
    u'περιμένω':    ('A', u'wait for', u'waits for'),
    u'καταλαβαίνω': ('A', u'understand', u'understands'),
    u'ετοιμάζω':    ('A', u'prepare', u'prepares'),
    u'ξέρω':        ('A', u'know', u'knows'),
    u'παίρνω':      ('A', u'take', u'takes'),
    u'πηγαίνω':     ('A', u'go', u'goes'),
    u'φεύγω':       ('A', u'leave', u'leaves'),
    u'μαγειρεύω':   ('A', u'cook', u'cooks'),
    u'ταξιδεύω':    ('A', u'travel', u'travels'),
    u'στέλνω':      ('A', u'send', u'sends'),
    u'δίνω':        ('A', u'give', u'gives'),
    u'ψάχνω':       ('A', u'look for', u'looks for'),
    u'δείχνω':      ('A', u'show', u'shows'),
    u'μαθαίνω':     ('A', u'learn', u'learns'),
    u'αγοράζω':     ('A', u'buy', u'buys'),
    u'κοιτάζω':     ('A', u'look at', u'looks at'),
    u'χορεύω':      ('A', u'dance', u'dances'),
    u'φέρνω':       ('A', u'bring', u'brings'),
    u'πληρώνω':     ('A', u'pay', u'pays'),
    u'καθαρίζω':    ('A', u'clean', u'cleans'),
    u'διαλέγω':     ('A', u'choose', u'chooses'),
    u'θέλω':        ('A', u'want', u'wants'),
    u'σπουδάζω':    ('A', u'study', u'studies'),
    u'δοκιμάζω':    ('A', u'try', u'tries'),
    u'νοικιάζω':    ('A', u'rent', u'rents'),
    u'τρέχω':       ('A', u'run', u'runs'),
    u'πλένω':       ('A', u'wash', u'washes'),
    u'χάνω':        ('A', u'lose', u'loses'),
    u'προσέχω':     ('A', u'look after', u'looks after'),
    u'σερβίρω':     ('A', u'serve', u'serves'),
    u'βρίσκω':      ('A', u'find', u'finds'),
    u'φτιάχνω':     ('A', u'make', u'makes'),
    u'κοστίζω':     ('A', u'cost', u'costs'),
    u'αρχίζω':      ('A', u'start', u'starts'),
    u'τελειώνω':    ('A', u'finish', u'finishes'),
    u'φτάνω':       ('A', u'arrive', u'arrives'),
    u'αγαπάω':      ('B1', u'love', u'loves'),
    u'μιλάω':       ('B1', u'talk', u'talks'),
    u'ρωτάω':       ('B1', u'ask', u'asks'),
    u'βοηθάω':      ('B1', u'help', u'helps'),
    u'ξυπνάω':      ('B1', u'wake up', u'wakes up'),
    u'περπατάω':    ('B1', u'walk', u'walks'),
    u'συναντάω':    ('B1', u'meet', u'meets'),
    u'απαντάω':     ('B1', u'answer', u'answers'),
    u'ξεχνάω':      ('B1', u'forget', u'forgets'),
    u'φοράω':       ('B1', u'wear', u'wears'),
    u'οδηγάω':      ('B1', u'drive', u'drives'),
    u'πουλάω':      ('B1', u'sell', u'sells'),
    u'προτιμάω':    ('B1', u'prefer', u'prefers'),
    u'τραγουδάω':   ('B1', u'sing', u'sings'),
    u'κρατάω':      ('B1', u'hold', u'holds'),
    u'ξεκινάω':     ('B1', u'start', u'starts'),
    u'χαιρετάω':    ('B1', u'greet', u'greets'),
    u'ευχαριστώ':   ('B2', u'thank', u'thanks'),
    u'τηλεφωνώ':    ('B2', u'phone', u'phones'),
    u'παρακολουθώ': ('B2', u'watch', u'watches'),
    u'εξηγώ':       ('B2', u'explain', u'explains'),
    u'συμπαθώ':     ('B2', u'like', u'likes'),
    u'ακολουθώ':    ('B2', u'follow', u'follows'),
    u'χρησιμοποιώ': ('B2', u'use', u'uses'),
    u'φιλοξενώ':    ('B2', u'host', u'hosts'),
    u'αργώ':        ('B2', u'be late', u'is late'),
    u'είμαι':       ('X', u'are', u'is'),
    u'λέω':         ('X', u'tell', u'tells'),
    u'τρώω':        ('X', u'eat', u'eats'),
    u'ακούω':       ('X', u'listen to', u'listens to'),
    u'ζω':          ('X', u'live', u'lives'),
    u'έρχομαι':     ('X', u'come', u'comes'),
    u'κάθομαι':     ('X', u'sit', u'sits'),
    u'θυμάμαι':     ('X', u'remember', u'remembers'),
    u'χρειάζομαι':  ('X', u'need', u'needs'),
}

# --------------------------------------------------------------------------
# 1. NOMINATIVE — a strong subject pronoun, the verb agreeing with it
# --------------------------------------------------------------------------
# (verb, greek tail, english tail, greek lead-in, english lead-in)
NOM_FIX = [
    (u'μένω', u'κοντά στο κέντρο.', u'near the centre.', u'', u''),
    (u'μένω', u'σε μια μικρή πόλη.', u'in a small town.', u'', u''),
    (u'δουλεύω', u'σε ένα μεγάλο γραφείο.', u'in a big office.', u'', u''),
    (u'δουλεύω', u'κάθε Σάββατο.', u'every Saturday.', u'', u''),
    (u'ταξιδεύω', u'πολύ τον χειμώνα.', u'a lot in the winter.', u'', u''),
    (u'ξυπνάω', u'πολύ νωρίς κάθε πρωί.', u'very early every morning.',
     u'', u''),
    (u'περπατάω', u'στην παραλία κάθε απόγευμα.',
     u'on the beach every afternoon.', u'', u''),
    (u'τρέχω', u'στο γυμναστήριο κάθε μέρα.', u'at the gym every day.',
     u'', u''),
    (u'μαγειρεύω', u'πολύ καλά.', u'very well.', u'', u''),
    (u'χορεύω', u'σε μια σχολή χορού.', u'at a dance school.', u'', u''),
    (u'σπουδάζω', u'στην Αθήνα φέτος.', u'in Athens this year.', u'', u''),
    (u'οδηγάω', u'με προσοχή.', u'carefully.', u'', u''),
    (u'πηγαίνω', u'στη δουλειά με το ποδήλατο.', u'to work by bike.',
     u'', u''),
    (u'φεύγω', u'αύριο το πρωί.', u'tomorrow morning.', u'', u''),
    (u'έρχομαι', u'με το λεωφορείο.', u'by bus.', u'', u''),
    (u'κάθομαι', u'στην τελευταία σειρά.', u'in the last row.', u'', u''),
    (u'ζω', u'στην Ελλάδα τώρα.', u'in Greece now.', u'', u''),
    (u'μιλάω', u'πολύ γρήγορα.', u'very fast.', u'', u''),
    (u'διαβάζω', u'κάθε βράδυ.', u'every evening.', u'', u''),
    (u'τρώω', u'συνήθως στο σπίτι.', u'at home usually.', u'', u''),
    (u'αργώ', u'πάντα στο ραντεβού.', u'for the appointment always.',
     u'', u''),
    (u'τραγουδάω', u'πολύ ωραία.', u'very nicely.', u'', u''),
    (u'πληρώνω', u'με κάρτα.', u'by card.', u'', u''),
    (u'δουλεύω', u'στο κέντρο.', u'in the centre.',
     u'Ο Νίκος δουλεύει έξω από την πόλη, αλλά ',
     u'Nikos works outside the city, but '),
    (u'μένω', u'σε ένα διαμέρισμα.', u'in a flat.',
     u'Οι γονείς μένουν σε ένα σπίτι, αλλά ',
     u'The parents live in a house, but '),
    (u'προτιμάω', u'τον χυμό.', u'juice.',
     u'Η Μαρία πίνει καφέ, αλλά ', u'Maria drinks coffee, but '),
    (u'μαθαίνω', u'καινούριες λέξεις κάθε μέρα.', u'new words every day.',
     u'Ο Γιώργος ξεχνάει τα πάντα, αλλά ',
     u'Giorgos forgets everything, but '),
    (u'θυμάμαι', u'τα πάντα.', u'everything.',
     u'Ο Νίκος ξεχνάει τα ονόματα, αλλά ',
     u'Nikos forgets names, but '),
    (u'ξέρω', u'την απάντηση.', u'the answer.',
     u'Οι άλλοι δεν ξέρουν, αλλά ', u'The others do not know, but '),
    (u'δουλεύω', u'από το σπίτι.', u'from home.',
     u'Οι συνάδελφοι πηγαίνουν στο γραφείο, αλλά ',
     u'The colleagues go to the office, but '),
]

# the same, but the sentence is a question
NOM_Q = [
    # (verb, greek tail, english tail, english reads as a progressive)
    (u'μένω', u'στο κέντρο;', u'in the centre?', False),
    (u'δουλεύω', u'εδώ;', u'here?', False),
    (u'έρχομαι', u'στη γιορτή;', u'coming to the party?', True),
    (u'θέλω', u'λίγο καφέ;', u'some coffee?', False),
    (u'ξέρω', u'τη διεύθυνση;', u'the address?', False),
    (u'πηγαίνω', u'στη συναυλία;', u'going to the concert?', True),
    (u'οδηγάω', u'σήμερα;', u'driving today?', True),
    (u'πληρώνω', u'τον λογαριασμό;', u'paying the bill?', True),
]


# είμαι with a complement that does not change for gender
NOM_BE = [
    (u'στο γραφείο όλη μέρα.', u'in the office all day.'),
    (u'από την Ελλάδα.', u'from Greece.'),
    (u'στην ταβέρνα τώρα.', u'at the taverna now.'),
    (u'στο σπίτι το Σαββατοκύριακο.', u'at home at the weekend.'),
    (u'στην παραλία όλο το απόγευμα.', u'on the beach all afternoon.'),
    (u'εδώ κάθε πρωί.', u'here every morning.'),
    (u'στην ίδια τάξη.', u'in the same class.'),
    (u'στη φωτογραφία.', u'in the photograph.'),
]

# είμαι with a predicate adjective — the gender has to be fixed by the
# prompt, so these run in the third person only
NOM_PRED = [
    (u'κουρασμένος', u'tired'), (u'χαρούμενος', u'happy'),
    (u'έτοιμος', u'ready'), (u'άρρωστος', u'ill'),
    (u'σίγουρος', u'sure'), (u'ελεύθερος', u'free'),
    (u'ευγενικός', u'polite'), (u'ήσυχος', u'quiet'),
]

# a transitive verb plus an object drawn from a curated pool
# (verb, pool, article, greek tail, english tail)
NOM_OBJ = [
    (u'αγοράζω', 'edible', 'def', u'από την αγορά.', u'at the market.'),
    (u'αγοράζω', 'wearable', 'indef', u'για τον γάμο.', u'for the wedding.'),
    (u'διαβάζω', 'readable', 'def', u'κάθε βράδυ.', u'every evening.'),
    (u'γράφω', 'writable', 'indef', u'για τη δουλειά.', u'for work.'),
    (u'ετοιμάζω', 'cooked', 'def', u'για το βράδυ.', u'for the evening.'),
    (u'μαγειρεύω', 'cooked', 'def', u'κάθε Κυριακή.', u'every Sunday.'),
    (u'πλένω', 'washable', 'def', u'μετά το φαγητό.', u'after the meal.'),
    (u'καθαρίζω', 'cleanable', 'def', u'κάθε Σάββατο.', u'every Saturday.'),
    (u'ψάχνω', 'searchable', 'def', u'κάθε πρωί.', u'every morning.'),
    (u'φοράω', 'wearable', 'def', u'στη δουλειά.', u'to work.'),
    (u'νοικιάζω', 'vehicle', 'indef', u'για τις διακοπές.',
     u'for the holidays.'),
    (u'οδηγάω', 'driveable', 'def', u'με προσοχή.', u'carefully.'),
    (u'προτιμάω', 'edible', 'def', u'το καλοκαίρι.', u'in the summer.'),
    (u'παρακολουθώ', 'watchable', 'def', u'κάθε εβδομάδα.', u'every week.'),
    (u'πληρώνω', 'payable', 'def', u'στην αρχή του μήνα.',
     u'at the beginning of the month.'),
    (u'περιμένω', 'people', 'def', u'στην είσοδο.', u'at the entrance.'),
    (u'συναντάω', 'people', 'def', u'κάθε Δευτέρα.', u'every Monday.'),
    (u'χρησιμοποιώ', 'usable', 'def', u'κάθε μέρα.', u'every day.'),
    (u'φέρνω', 'served', 'indef', u'στην κουζίνα.', u'to the kitchen.'),
    (u'διαλέγω', 'gift', 'indef', u'για δώρο.', u'as a present.'),
    (u'δοκιμάζω', 'edible', 'def', u'για πρώτη φορά.',
     u'for the first time.'),
    (u'θυμάμαι', 'memorable', 'def', u'πολύ καλά.', u'very well.'),
    (u'χρειάζομαι', 'needed', 'indef', u'για το μάθημα.',
     u'for the lesson.'),
    (u'ξεχνάω', 'portable', 'def', u'στο γραφείο.', u'at the office.'),
    (u'σερβίρω', 'served', 'def', u'στους πελάτες.', u'to the customers.'),
    (u'πουλάω', 'ownable', 'def', u'σε καλή τιμή.', u'at a good price.'),
]

# a thing as subject: αυτός/αυτή/αυτό all translate as English "it"
# (verb, greek tail, english tail)
NOM_THING = [
    (u'κοστίζω', u'πολύ.', u'a lot.'),
    (u'αρχίζω', u'σε λίγο.', u'in a moment.'),
    (u'τελειώνω', u'αύριο.', u'tomorrow.'),
    (u'φτάνω', u'αύριο το πρωί.', u'tomorrow morning.'),
    (u'είμαι', u'στο δωμάτιο.', u'in the room.'),
    (u'είμαι', u'εδώ από χθες.', u'here since yesterday.'),
]
NOM_THING_PRED = [
    (u'ακριβός', u'expensive'), (u'φτηνός', u'cheap'),
    (u'καινούριος', u'new'), (u'ωραίος', u'nice'),
    (u'μεγάλος', u'big'), (u'μικρός', u'small'),
    (u'καθαρός', u'clean'), (u'ανοιχτός', u'open'),
]

# --------------------------------------------------------------------------
# 2. ACCUSATIVE — a weak object pronoun, which stands in front of the verb
# --------------------------------------------------------------------------
# (greek lead-in, english subject, verb, subject person, negated,
#  greek tail, english tail)
ACC_WEAK = [
    (u'', u'I', u'βλέπω', '1sg', False, u'κάθε μέρα.', u'every day.'),
    (u'', u'I', u'περιμένω', '1sg', False, u'στην πόρτα.',
     u'at the door.'),
    (u'', u'I', u'ξέρω', '1sg', False, u'από το σχολείο.', u'from school.'),
    (u'', u'I', u'ευχαριστώ', '1sg', False, u'πολύ.', u'very much.'),
    (u'', u'I', u'θυμάμαι', '1sg', False, u'από τη δουλειά.', u'from work.'),
    (u'', u'I', u'συμπαθώ', '1sg', False, u'πολύ.', u'a lot.'),
    (u'', u'I', u'ψάχνω', '1sg', False, u'όλο το πρωί.', u'all morning.'),
    (u'', u'I', u'βοηθάω', '1sg', False, u'με τις ασκήσεις.',
     u'with the exercises.'),
    (u'', u'I', u'ακούω', '1sg', False, u'πολύ καλά.', u'very well.'),
    (u'', u'I', u'προσέχω', '1sg', False, u'το Σαββατοκύριακο.',
     u'at the weekend.'),
    (u'', u'we', u'συναντάω', '1pl', False, u'κάθε Σάββατο.',
     u'every Saturday.'),
    (u'', u'we', u'φιλοξενώ', '1pl', False, u'το καλοκαίρι.',
     u'in the summer.'),
    (u'', u'we', u'ακολουθώ', '1pl', False, u'με το αυτοκίνητο.', u'by car.'),
    (u'', u'we', u'περιμένω', '1pl', False, u'στο λιμάνι.', u'at the port.'),
    (u'', u'he', u'βλέπω', '3sg', False, u'στο γυμναστήριο.', u'at the gym.'),
    (u'', u'she', u'ρωτάω', '3sg', False, u'για το ταξίδι.',
     u'about the trip.'),
    (u'', u'she', u'βοηθάω', '3sg', False, u'με τα ψώνια.',
     u'with the shopping.'),
    (u'', u'they', u'περιμένω', '3pl', False, u'στον σταθμό.',
     u'at the station.'),
    (u'', u'they', u'κοιτάζω', '3pl', False, u'με ενδιαφέρον.',
     u'with interest.'),
    (u'', u'they', u'χαιρετάω', '3pl', False, u'από την αυλή.',
     u'from the yard.'),
    (u'Δεν ', u'I', u'βλέπω', '1sg', True, u'καθόλου.', u'at all.'),
    (u'Δεν ', u'I', u'καταλαβαίνω', '1sg', True, u'.', u'.'),
    (u'Δεν ', u'we', u'ξέρω', '1pl', True, u'καλά.', u'well.'),
    (u'Δεν ', u'I', u'ακούω', '1sg', True, u'από εδώ.', u'from here.'),
    (u'Δεν ', u'I', u'θυμάμαι', '1sg', True, u'από το σχολείο.',
     u'from school.'),
    (u'Δεν ', u'they', u'περιμένω', '3pl', True, u'σήμερα.', u'today.'),
    (u'Ο δάσκαλος δεν ', u'', u'ρωτάω', '3sg', True, u'ποτέ.', u'ever.'),
    (u'Η γιαγιά ', u'', u'περιμένω', '3sg', False, u'στην αυλή.',
     u'in the yard.'),
    (u'Τα παιδιά ', u'', u'ακούω', '3pl', False, u'με προσοχή.',
     u'carefully.'),
    (u'Ο γιατρός ', u'', u'προσέχω', '3sg', False, u'πολύ.', u'very well.'),
    (u'Οι φίλες ', u'', u'βοηθάω', '3pl', False, u'πάντα.', u'always.'),
    (u'Η δασκάλα δεν ', u'', u'βλέπω', '3sg', True, u'από το γραφείο.',
     u'from her desk.'),
    (u'Οι γείτονες ', u'', u'χαιρετάω', '3pl', False, u'κάθε πρωί.',
     u'every morning.'),
    (u'Ο σερβιτόρος ', u'', u'ρωτάω', '3sg', False, u'για την παραγγελία.',
     u'about the order.'),
]

# the english subject that belongs to each of those lead-ins
LEAD_EN = {
    u'Ο δάσκαλος δεν ': u'The teacher',
    u'Η γιαγιά ': u'Grandmother',
    u'Τα παιδιά ': u'The children',
    u'Ο γιατρός ': u'The doctor',
    u'Οι φίλες ': u'The friends',
    u'Η δασκάλα δεν ': u'The teacher',
    u'Οι γείτονες ': u'The neighbours',
    u'Ο σερβιτόρος ': u'The waiter',
}

# the same job, but the object is a thing, so every gender is English "it"
ACC_WEAK_THING = [
    (u'', u'I', u'διαβάζω', '1sg', False, u'κάθε βράδυ.', u'every evening.'),
    (u'', u'I', u'πλένω', '1sg', False, u'μετά το φαγητό.',
     u'after the meal.'),
    (u'', u'I', u'αγοράζω', '1sg', False, u'από την αγορά.',
     u'at the market.'),
    (u'', u'I', u'χρειάζομαι', '1sg', False, u'για τη δουλειά.',
     u'for work.'),
    (u'Δεν ', u'I', u'βρίσκω', '1sg', True, u'πουθενά.', u'anywhere.'),
    (u'', u'we', u'καθαρίζω', '1pl', False, u'κάθε Σάββατο.',
     u'every Saturday.'),
    (u'', u'I', u'χρησιμοποιώ', '1sg', False, u'κάθε μέρα.', u'every day.'),
    (u'Δεν ', u'I', u'θέλω', '1sg', True, u'.', u'.'),
    (u'', u'they', u'πουλάω', '3pl', False, u'σε καλή τιμή.',
     u'at a good price.'),
    (u'', u'she', u'φέρνω', '3sg', False, u'στην κουζίνα.',
     u'to the kitchen.'),
    (u'', u'I', u'ψάχνω', '1sg', False, u'όλο το πρωί.',
     u'all morning.'),
    (u'', u'he', u'φτιάχνω', '3sg', False, u'κάθε Κυριακή.',
     u'every Sunday.'),
    (u'Δεν ', u'we', u'χρειάζομαι', '1pl', True, u'σήμερα.', u'today.'),
    (u'', u'I', u'προτιμάω', '1sg', False, u'το καλοκαίρι.',
     u'in the summer.'),
    (u'', u'we', u'παίρνω', '1pl', False, u'μαζί στο ταξίδι.',
     u'along on the trip.'),
]

# --------------------------------------------------------------------------
# 3. ACCUSATIVE — a strong pronoun after a preposition
# --------------------------------------------------------------------------
# (preposition, english preposition, may take a third-person pronoun)
PREPS = [
    (u'για', u'for', False), (u'με', u'with', True),
    (u'από', u'from', True), (u'χωρίς', u'without', True),
    (u'μαζί με', u'together with', True),
]
# (greek lead-in, english lead-in, which prepositions, greek tail,
#  english tail)
ACC_PREP = [
    # (greek lead-in, english lead-in, prepositions, greek tail, english
    #  tail, person the frame's own subject already uses)
    (u'Αυτό το δώρο είναι ', u'This present is ', (0, 2), u'.', u'.', None),
    (u'Η δασκάλα μιλάει ', u'The teacher is talking ', (1,), u'.', u'.',
     None),
    (u'Δεν θέλω να φύγω ', u'I do not want to leave ', (3,), u'.', u'.', 1),
    (u'Ο Νίκος έρχεται στη γιορτή ', u'Nikos is coming to the party ',
     (4,), u'.', u'.', None),
    (u'Το γράμμα είναι ', u'The letter is ', (0, 2), u'.', u'.', None),
    (u'Θα έρθω στο θέατρο ', u'I will come to the theatre ', (1, 4),
     u'.', u'.', 1),
    (u'Η ζωή είναι δύσκολη ', u'Life is difficult ', (3,), u'.', u'.', None),
    (u'Αγοράζω ένα βιβλίο ', u'I am buying a book ', (0,), u'.', u'.', 1),
    (u'Ο γιατρός ρωτάει ', u'The doctor is asking ', (1,), u'.', u'.', None),
    (u'Παίρνω το κλειδί ', u'I am taking the key ', (2,), u'.', u'.', 1),
    (u'Δεν μπορώ να ζήσω ', u'I cannot live ', (3,), u'.', u'.', 1),
    (u'Οι φίλοι ταξιδεύουν ', u'The friends are travelling ', (4,),
     u'.', u'.', None),
    (u'Αυτή η φωτογραφία είναι ', u'This photograph is ', (0, 2), u'.',
     u'.', None),
    (u'Μιλάω στον γιατρό ', u'I am talking to the doctor ', (0,), u'.',
     u'.', 1),
    (u'Η γιαγιά μαγειρεύει ', u'Grandmother is cooking ', (0,), u'.',
     u'.', None),
    (u'Το παιδί κάθεται ', u'The child is sitting ', (1,), u'.', u'.', None),
    (u'Το λεωφορείο φεύγει ', u'The bus is leaving ', (3,), u'.', u'.',
     None),
    (u'Η ταινία αρχίζει ', u'The film is starting ', (3,), u'.', u'.',
     None),
    (u'Τα παιδιά παίζουν ', u'The children are playing ', (1, 4),
     u'στην αυλή.', u'in the yard.', None),
    (u'Ο δάσκαλος ετοιμάζει το μάθημα ', u'The teacher prepares the lesson ',
     (0,), u'.', u'.', None),
    (u'Ο Νίκος δεν ταξιδεύει ποτέ ', u'Nikos never travels ', (3,), u'.',
     u'.', None),
    (u'Η εταιρεία δουλεύει ', u'The company works ', (1,), u'.', u'.', None),
    (u'Αυτά τα λουλούδια είναι ', u'These flowers are ', (0, 2), u'.',
     u'.', None),
    (u'Ο γείτονας έρχεται στην εκδρομή ', u'The neighbour is coming on the '
     u'trip ', (4,), u'.', u'.', None),
    (u'Το παιδί δεν φεύγει ποτέ ', u'The child never leaves ', (3,),
     u'.', u'.', None),
]


# --------------------------------------------------------------------------
# 4. ACCUSATIVE — a strong pronoun as an emphatic object, against a contrast
# --------------------------------------------------------------------------
ACC_EMPH = [
    (u'Ο δάσκαλος ρωτάει ', u'The teacher is asking '),
    (u'Η εταιρεία διαλέγει ', u'The company is choosing '),
    (u'Ο γιατρός περιμένει ', u'The doctor is waiting for '),
    (u'Τα παιδιά χαιρετάνε ', u'The children are greeting '),
    (u'Η αστυνομία ψάχνει ', u'The police are looking for '),
    (u'Οι γείτονες κοιτάζουν ', u'The neighbours are looking at '),
    (u'Ο σκηνοθέτης διαλέγει ', u'The director is choosing '),
    (u'Η δασκάλα βοηθάει ', u'The teacher is helping '),
    (u'Ο καλλιτέχνης ζωγραφίζει ', u'The artist is painting '),
    (u'Ο δήμαρχος καλεί ', u'The mayor is inviting '),
]

# --------------------------------------------------------------------------
# 5. GENITIVE — a weak pronoun as indirect object
# --------------------------------------------------------------------------
# (greek lead-in, english subject, verb, subject person, negated,
#  greek tail, english tail)
GEN_IO = [
    # (greek lead-in, english subject, verb, subject person, negation —
    #  False, True or 'never', greek tail, english tail, english puts the
    #  pronoun in a 'to ...' phrase after the object)
    (u'', u'he', u'τηλεφωνώ', '3sg', False, u'κάθε μέρα.', u'every day.',
     False),
    (u'', u'she', u'γράφω', '3sg', False, u'από την Ελλάδα.',
     u'from Greece.', 'before'),
    (u'', u'they', u'στέλνω', '3pl', False, u'ένα δώρο κάθε χρόνο.',
     u'a present every year.', False),
    (u'', u'he', u'δίνω', '3sg', False, u'τα κλειδιά.', u'the keys.', False),
    (u'', u'she', u'ετοιμάζω', '3sg', False, u'έναν καφέ.', u'a coffee.',
     False),
    (u'', u'they', u'φέρνω', '3pl', False, u'λουλούδια.', u'flowers.',
     False),
    (u'', u'he', u'εξηγώ', '3sg', False, u'την άσκηση.', u'the exercise.',
     'after'),
    (u'', u'she', u'δείχνω', '3sg', False, u'τις φωτογραφίες.',
     u'the photographs.', False),
    (u'Δεν ', u'he', u'απαντάω', '3sg', 'never', u'ποτέ.', u'', False),
    (u'Δεν ', u'they', u'λέω', '3pl', True, u'την αλήθεια.', u'the truth.',
     False),
    (u'Η δασκάλα δεν ', u'', u'εξηγώ', '3sg', True, u'τίποτα.',
     u'anything.', 'after'),
    (u'Ο σερβιτόρος δεν ', u'', u'φέρνω', '3sg', True, u'τον λογαριασμό.',
     u'the bill.', False),
    (u'Οι γείτονες δεν ', u'', u'μιλάω', '3pl', True, u'καθόλου.',
     u'at all.', 'before'),
]

GEN_LEAD_EN = {
    u'Η δασκάλα δεν ': u'The teacher',
    u'Ο σερβιτόρος δεν ': u'The waiter',
    u'Οι γείτονες δεν ': u'The neighbours',
}

# μου αρέσει — the construction every A2 learner meets first
GEN_ARESEI = [
    ('sg', u'ο καφές το πρωί.', u'coffee in the morning.'),
    ('sg', u'η ελληνική μουσική.', u'Greek music.'),
    ('pl', u'τα γλυκά.', u'sweets.'),
    ('pl', u'οι μεγάλες πόλεις.', u'big cities.'),
    ('sg', u'το καλοκαίρι.', u'summer.'),
    ('pl', u'τα ταξίδια.', u'travelling.'),
]

# --------------------------------------------------------------------------
# 6. GENITIVE — the weak possessive, which follows its noun
# --------------------------------------------------------------------------
# (greek lead-in, english lead-in, pool, number, greek tail, english tail)
GEN_POSS = [
    # (greek lead-in, english lead-in, pool, number, case of the slot,
    #  greek tail, english tail, build 'αυτός/αυτή/αυτό είναι' to agree)
    (u'', u'This is ', 'owned_place', 'sg', 'nom', u'.', u'.', True),
    (u'', u'These are ', 'portable', 'pl', 'nom', u'.', u'.', True),
    (u'Πού είναι ', u'Where is ', 'portable', 'sg', 'nom', u';', u'?',
     False),
    (u'Δεν βρίσκω ', u'I cannot find ', 'searchable', 'pl', 'acc', u'.',
     u'.', False),
    (u'Μου αρέσει πολύ ', u'I really like ', 'owned_place', 'sg', 'nom',
     u'.', u'.', False),
    (u'Περιμένω ', u'I am waiting for ', 'people', 'sg', 'acc',
     u' στην είσοδο.', u' at the entrance.', False),
    (u'Έρχονται ', u'', 'people', 'pl', 'nom', u' στο σπίτι.',
     u' are coming to the house.', False),
    (u'Καθαρίζω ', u'I clean ', 'cleanable', 'sg', 'acc',
     u' κάθε Σάββατο.', u' every Saturday.', False),
    (u'Πού είναι ', u'Where are ', 'searchable', 'pl', 'nom', u';', u'?',
     False),
]


# --------------------------------------------------------------------------
# 7. δικός μου — the emphatic possessive, agreeing with the thing owned
# --------------------------------------------------------------------------
# predicative, 'this car is mine' — nominative
# (pool, number, negated, greek tail, english tail)
DIKOS_PRED = [
    ('ownable', 'sg', False, u'.', u'.'),
    ('vehicle', 'sg', False, u'.', u'.'),
    ('ownable', 'pl', False, u'.', u'.'),
    ('wearable', 'sg', True, u'.', u'.'),
    ('owned_place', 'sg', False, u'.', u'.'),
    ('readable', 'pl', True, u'.', u'.'),
    ('portable', 'sg', False, u'.', u'.'),
    ('wearable', 'pl', False, u'.', u'.'),
]


# attributive, nominative — (pool, greek tail, english singular tail,
# english plural tail)
DIKOS_NOM = [
    # (pool, numbers, greek tail, english singular tail, english plural tail)
    ('owned_place', ('sg',), u'είναι κοντά στο κέντρο.',
     u'is near the centre.', u'are near the centre.'),
    ('driveable', ('sg', 'pl'), u'είναι στον δρόμο.', u'is in the street.',
     u'are in the street.'),
    ('ownable', ('sg', 'pl'), u'είναι στην κουζίνα.', u'is in the kitchen.',
     u'are in the kitchen.'),
    ('readable', ('sg', 'pl'), u'είναι στη βιβλιοθήκη.',
     u'is in the library.', u'are in the library.'),
    ('wearable', ('sg', 'pl'), u'είναι στο δωμάτιο.', u'is in the room.',
     u'are in the room.'),
    ('portable', ('sg', 'pl'), u'είναι στο γραφείο.', u'is in the office.',
     u'are in the office.'),
]


# attributive, accusative — (greek lead-in, english lead-in, pool,
# greek tail, english tail)
DIKOS_ACC = [
    # (greek lead-in, english lead-in, pool, numbers, greek tail,
    #  english tail)
    (u'Παίρνω ', u'I am taking ', 'portable', ('sg', 'pl'),
     u'στη δουλειά.', u'to work.'),
    (u'Προτιμάω ', u'I prefer ', 'edible', ('sg', 'pl'), u'.', u'.'),
    (u'Δεν βρίσκω ', u'I cannot find ', 'searchable', ('sg', 'pl'),
     u'.', u'.'),
    (u'Θέλω ', u'I want ', 'portable', ('sg', 'pl'), u'πίσω.', u'back.'),
    (u'Χρησιμοποιώ ', u'I use ', 'usable', ('sg', 'pl'), u'κάθε μέρα.',
     u'every day.'),
    (u'Αγοράζω ', u'I am buying ', 'wearable', ('sg', 'pl'),
     u'από την αγορά.', u'at the market.'),
    (u'Καθαρίζω ', u'I clean ', 'cleanable', ('sg',), u'κάθε Σάββατο.',
     u'every Saturday.'),
    (u'Οδηγάω ', u'I drive ', 'driveable', ('sg',), u'με προσοχή.',
     u'carefully.'),
    (u'Διαβάζω ', u'I read ', 'readable', ('sg', 'pl'), u'κάθε βράδυ.',
     u'every evening.'),
]


# attributive, genitive — the head noun of the phrase is fixed, so the
# adjective at the end agrees with it and never with the slot
# (greek lead-in, english lead-in, pool, greek tail, english tail)
DIKOS_GEN = [
    # (greek lead-in, english lead-in, pool, numbers, greek tail,
    #  english tail)
    (u'Η πόρτα ', u'The door of ', 'owned_place', ('sg',),
     u'είναι ανοιχτή.', u'is open.'),
    (u'Το χρώμα ', u'The colour of ', 'vehicle', ('sg',), u'είναι μπλε.',
     u'is blue.'),
    (u'Η τιμή ', u'The price of ', 'ownable', ('sg',), u'είναι μεγάλη.',
     u'is high.'),
    (u'Τα παράθυρα ', u'The windows of ', 'owned_place', ('sg',),
     u'είναι καινούρια.', u'are new.'),
    (u'Τα κλειδιά ', u'The keys of ', 'owned_place', ('sg',),
     u'είναι στο γραφείο.', u'are in the office.'),
    (u'Ο αριθμός ', u'The number of ', 'driveable', ('sg',),
     u'είναι στην κάρτα.', u'is on the card.'),
]


# --------------------------------------------------------------------------
# 8. fan-out families: the same jobs, with a noun drawn from the pools
# --------------------------------------------------------------------------
# weak accusative object + a place: (verb, subject person, english subject)
# these run with a singular venue only: the card's number is the number of
# the pronoun, not of the place, so nothing is lost by it
ACC_WEAK_PLACE = [
    (u'περιμένω', '1sg', u'I'),
    (u'βλέπω', '1sg', u'I'),
    (u'συναντάω', '1pl', u'we'),
    (u'ψάχνω', '3pl', u'they'),
    (u'περιμένω', '3sg', u'he'),
    (u'βλέπω', '3pl', u'they'),
    (u'συναντάω', '1sg', u'I'),
    (u'ακολουθώ', '3sg', u'she'),
]

# weak genitive indirect object + a direct object drawn from a pool
# (verb, subject person, english subject, pool, article)
GEN_IO_OBJ = [
    (u'δίνω', '3sg', u'he', 'portable', 'def'),
    (u'στέλνω', '3pl', u'they', 'writable', 'indef'),
    (u'φέρνω', '3sg', u'she', 'served', 'def'),
    (u'δείχνω', '3sg', u'he', 'venue', 'def'),
    (u'αγοράζω', '3pl', u'they', 'wearable', 'indef'),
    (u'ετοιμάζω', '3sg', u'she', 'cooked', 'def'),
]
