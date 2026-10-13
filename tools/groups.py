# -*- coding: utf-8 -*-
"""Noun pools, narrower than the raw semantic tags.

A tag like 'obj' holds both a suitcase and a plug socket; only one of them
can be taken to work or owned. Each pool below is the set of nouns that
makes sense in one particular slot.
"""
from data2 import NOUNS

# things a person can own and talk about as theirs
OWNABLE = (u'καρέκλα', u'κρεβάτι', u'κουρτίνα', u'χαλί', u'μαξιλάρι',
           u'κουβέρτα', u'σεντόνι', u'στρώμα', u'καθρέφτης', u'πολυθρόνα',
           u'ψυγείο', u'πλυντήριο', u'κατσαρόλα', u'τηγάνι', u'πιάτο',
           u'ποτήρι', u'φλιτζάνι', u'μαχαίρι', u'πετσέτα', u'κουτί',
           u'σακούλα', u'τσάντα', u'βαλίτσα', u'πορτοφόλι', u'μολύβι',
           u'τηλέφωνο', u'υπολογιστής', u'τηλεόραση', u'ραδιόφωνο',
           u'μικρόφωνο', u'κιθάρα', u'πιάνο', u'εισιτήριο', u'διαβατήριο',
           u'κάρτα', u'φάκελος', u'αφίσα', u'φωτογραφία', u'ομπρέλα',
           u'γάντι', u'μάσκα', u'θήκη', u'χάρτης', u'δώρο', u'κάδρο',
           u'φωτιστικό', u'συσκευή')

# the subset of those that a person carries about
PORTABLE = (u'τσάντα', u'βαλίτσα', u'πορτοφόλι', u'μολύβι', u'τηλέφωνο',
            u'υπολογιστής', u'ομπρέλα', u'κουτί', u'σακούλα', u'κάρτα',
            u'εισιτήριο', u'διαβατήριο', u'φάκελος', u'θήκη', u'χάρτης',
            u'μάσκα', u'γάντι', u'φωτογραφία', u'δώρο', u'κιθάρα')

# what gets washed up or washed
WASHABLE = (u'πιάτο', u'ποτήρι', u'φλιτζάνι', u'μαχαίρι', u'πιρούνι',
            u'κατσαρόλα', u'τηγάνι', u'πετσέτα', u'χαρτοπετσέτα',
            u'σεντόνι', u'κουβέρτα', u'τραπεζομάντιλο')

# a place a person can call their own
OWNED_PLACE = (u'σπίτι', u'δωμάτιο', u'κουζίνα', u'σαλόνι', u'κήπος',
               u'αυλή', u'διαμέρισμα', u'μονοκατοικία', u'γραφείο',
               u'αποθήκη', u'γήπεδο', u'ξενοδοχείο', u'εστιατόριο',
               u'ταβέρνα', u'καφετέρια', u'βιβλιοπωλείο', u'φαρμακείο')

# rooms and buildings that get cleaned
CLEANABLE = (u'σπίτι', u'δωμάτιο', u'κουζίνα', u'σαλόνι', u'αυλή',
             u'γραφείο', u'αίθουσα', u'αποθήκη', u'διαμέρισμα', u'ισόγειο')

# somewhere two people can arrange to meet
VENUE = (u'σπίτι', u'κουζίνα', u'σαλόνι', u'κήπος', u'αυλή', u'σχολείο',
         u'βιβλιοθήκη', u'μουσείο', u'θέατρο', u'εστιατόριο', u'ταβέρνα',
         u'καφετέρια', u'ξενοδοχείο', u'φαρμακείο', u'γραφείο', u'αγορά',
         u'εκκλησία', u'κάστρο', u'πλατεία', u'κέντρο', u'σταθμός',
         u'αεροδρόμιο', u'λιμάνι', u'παραλία', u'γήπεδο', u'γυμναστήριο',
         u'πισίνα', u'ταχυδρομείο', u'βιβλιοπωλείο', u'αίθουσα',
         u'είσοδος', u'έξοδος', u'σχολή', u'ωδείο', u'πολυκατάστημα',
         u'μνημείο', u'αξιοθέατο', u'πυραμίδα')

# what a person reads
READABLE = (u'βιβλίο', u'εφημερίδα', u'περιοδικό', u'άρθρο', u'κείμενο',
            u'έγγραφο', u'λεξικό', u'σελίδα', u'γράμμα', u'μήνυμα',
            u'φυλλάδιο', u'σημείωση', u'παροιμία', u'διάλογος',
            u'πρόσκληση', u'αγγελία', u'διαφήμιση', u'ειδοποίηση',
            u'συνταγή', u'ερωτηματολόγιο')

# what a person writes
WRITABLE = (u'γράμμα', u'μήνυμα', u'άρθρο', u'κείμενο', u'σημείωση',
            u'πρόσκληση', u'αγγελία', u'συνταγή', u'έγγραφο',
            u'ερωτηματολόγιο', u'αίτηση')

# what a person watches or follows week by week
WATCHABLE = (u'ταινία', u'εκπομπή', u'παράσταση', u'αγώνας', u'συναυλία',
             u'πρόγραμμα')

# cooked and prepared dishes
COOKED = (u'φαγητό', u'γεύμα', u'σούπα', u'σαλάτα', u'γλυκό', u'τούρτα',
          u'πρωινό', u'μεσημεριανό', u'βραδινό', u'κοτόπουλο', u'πατάτα',
          u'ρύζι', u'λαχανικό', u'φασόλι', u'φακή', u'πάστα', u'κρέμα',
          u'αβγό')

# food worth buying, trying or preferring
EDIBLE = (u'ψωμί', u'τυρί', u'αβγό', u'γιαούρτι', u'μέλι', u'ρύζι',
          u'κρασί', u'χυμός', u'ποτό', u'αναψυκτικό', u'σούπα', u'σαλάτα',
          u'πατάτα', u'καρότο', u'αγγούρι', u'μαρούλι', u'λαχανικό',
          u'φρούτο', u'μήλο', u'πορτοκάλι', u'λεμόνι', u'κεράσι',
          u'πεπόνι', u'αμύγδαλο', u'καρύδι', u'φουντούκι', u'φασόλι',
          u'φακή', u'κοτόπουλο', u'παγωτό', u'γλυκό', u'τούρτα',
          u'φαγητό', u'γεύμα', u'πρωινό', u'πάστα', u'κρέμα')

# what a person puts on
WEARABLE = (u'πουκάμισο', u'φούστα', u'φόρεμα', u'φουστάνι', u'σακάκι',
            u'κοστούμι', u'σκούφος', u'φόρμα', u'ποδιά', u'γάντι',
            u'μάσκα')

VEHICLE = (u'ποδήλατο', u'αυτοκίνητο', u'λεωφορείο', u'πλοίο', u'καράβι',
           u'αεροπλάνο')

# only these go down a street, and only these does a learner drive
DRIVEABLE = (u'ποδήλατο', u'αυτοκίνητο', u'λεωφορείο')

# people one can be related to, work with or wait for
PEOPLE = (u'φίλος', u'φίλη', u'αδερφός', u'αδερφή', u'μητέρα', u'πατέρας',
          u'γιαγιά', u'θείος', u'θεία', u'ξάδερφος', u'ξαδέρφη', u'ανιψιός',
          u'ανιψιά', u'εγγονός', u'εγγονή', u'γείτονας', u'γειτόνισσα',
          u'κόρη', u'παιδί', u'δάσκαλος', u'δασκάλα', u'γιατρός',
          u'συνάδελφος', u'συμμαθητής', u'συμμαθήτρια', u'συγκάτοικος',
          u'πελάτης', u'φοιτητής', u'φοιτήτρια', u'καλλιτέχνης',
          u'τραγουδιστής', u'ηθοποιός', u'δικηγόρος', u'μηχανικός',
          u'σερβιτόρος', u'υπάλληλος', u'μάγειρας', u'οδοντίατρος')

# bills and charges that get paid
PAYABLE = (u'λογαριασμός', u'ενοίκιο', u'μισθός', u'τιμή', u'παραγγελία',
           u'εργασία', u'υπηρεσία')

# things that get looked for and lost
SEARCHABLE = PORTABLE

# what a person needs for a lesson
NEEDED = (u'μολύβι', u'βιβλίο', u'λεξικό', u'υπολογιστής', u'χάρτης',
          u'τσάντα', u'κάρτα', u'φάκελος', u'σημείωση')

# what a shop sells and a person uses
USABLE = (u'υπολογιστής', u'τηλέφωνο', u'ψυγείο', u'πλυντήριο',
          u'κατσαρόλα', u'τηγάνι', u'μαχαίρι', u'ομπρέλα', u'χάρτης',
          u'λεξικό', u'συσκευή', u'μικρόφωνο', u'σαπούνι',
          u'καθαριστικό', u'απορρυπαντικό')

# events worth remembering
MEMORABLE = (u'ταξίδι', u'γάμος', u'εκδρομή', u'συναυλία', u'γιορτή',
             u'συνάντηση', u'παράσταση', u'βόλτα', u'συζήτηση', u'αγώνας',
             u'συνέντευξη', u'πτήση', u'γλέντι', u'πρεμιέρα')

# a present someone might choose
GIFT = (u'βιβλίο', u'δώρο', u'λουλούδι', u'φωτογραφία', u'κάρτα',
        u'κιθάρα', u'ομπρέλα', u'τσάντα', u'πορτοφόλι', u'κάδρο',
        u'αφίσα', u'θήκη')

# things that get served at table
SERVED = (u'φαγητό', u'σούπα', u'σαλάτα', u'γλυκό', u'παγωτό',
          u'κρασί', u'χυμός', u'ποτό', u'αναψυκτικό', u'τούρτα', u'πάστα')

GROUPS = {
    'ownable': OWNABLE, 'portable': PORTABLE, 'washable': WASHABLE,
    'owned_place': OWNED_PLACE, 'cleanable': CLEANABLE, 'venue': VENUE,
    'readable': READABLE, 'writable': WRITABLE, 'watchable': WATCHABLE,
    'cooked': COOKED, 'edible': EDIBLE, 'wearable': WEARABLE,
    'vehicle': VEHICLE, 'driveable': DRIVEABLE, 'people': PEOPLE, 'payable': PAYABLE,
    'searchable': SEARCHABLE, 'needed': NEEDED, 'usable': USABLE,
    'memorable': MEMORABLE, 'gift': GIFT, 'served': SERVED,
}

_LEMMAS = set(g for (g, c, t, e, p) in NOUNS)
for _name, _pool in GROUPS.items():
    for _w in _pool:
        assert _w in _LEMMAS, u'%s: %s is not in the noun list' % (_name, _w)
