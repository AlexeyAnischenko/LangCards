# -*- coding: utf-8 -*-
"""Build the irregular-verbs deck and the table behind the Greek-A2-Basics
irregular grid, from one list.

Scope: every verb in the KLIK A1 + A2 books and the 2015-2018 A2 exam papers
(support-materials/KLIK A1+A2 dictionary.xlsx, plus the old A2 glossary) whose
past simple, past continuous or future cannot be built with the rules on the
sheets:

  * the ψ / ξ / σ trick (lips -> ψ, throat -> ξ, teeth -> σ, nose ν -> σ,
    vowel -> σ, -άω / -ώ -> -ησα), λ / ρ stems that simply keep the stem
    (αναφέρω -> ανέφερα, σέρβιρα is listed only for its -ίσα twin);
  * the augment: έ- on a short word, and the internal ε- of a prefixed verb
    (επιτρέπω -> επέτρεψα, αναφέρω -> ανέφερα) - that alone is NOT irregular;
  * the regular passive aorists (-ζομαι -> -στηκα, -νομαι -> -θηκα,
    -εύομαι -> -εύτηκα, -άμαι / -ούμαι -> -ήθηκα);
  * the imperfect: present stem + -α (-ούσα for -άω / -ώ, -όμουν for -μαι).

Each verb: present 1sg; aorist 1sg + 1pl; imperfect 1sg + 1pl (for a -μαι
verb, 1sg + 3pl); future 1sg with θα. The other persons are mechanical.

Outputs
  ../greek-a2-irregular-verbs.txt                      the LangCards deck
  ../../Greek-A2-Basics/grammar/data/irregular-verbs.tsv  the grid's data

Run from anywhere:  python tools/irregulardeck.py
"""
import io, os, sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
LC = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from writingdeck import latin                                # noqa: E402
from greeklex import deaccent, nuclei                         # noqa: E402
from irregular_en import table as en_table                    # noqa: E402

OUT = os.path.join(LC, 'greek-a2-irregular-verbs.txt')
BASICS = os.path.join(os.path.dirname(LC), 'Greek-A2-Basics')
TSV = os.path.join(BASICS, 'grammar', 'data', 'irregular-verbs.tsv')
XLSX = os.path.join(BASICS, 'support-materials', 'KLIK A1+A2 dictionary.xlsx')
A2GLOSS = os.path.join(LC, 'klik-a2-vocabulary.txt')

GROUPS = [
    ('core', 'Irregular stem — learn these by heart'),
    ('aino', '-αίνω — the past drops to a short stem'),
    ('nu', '-νω / -λνω / -ρνω — no σ, or the vowel changes'),
    ('xi', 'ξ where the trick says σ'),
    ('asa', '-άω / -ώ — -ασα, -εσα or -ισα instead of -ησα'),
    ('learned', 'Formal verbs from the readings — ancient stems'),
    ('mai', '-μαι verbs with an unexpected past'),
    ('loan', '-άρω / -ίρω loanwords'),
]

# present | meaning | aorist 1sg 1pl | imperfect 1sg 1pl (-μαι: 1sg 3pl) | future | flags | note
# flags: i = the imperfect is irregular too.  '-' = no form.
DATA = u"""
core
είμαι | be | - - | ήμουν ήμασταν | θα είμαι | i | no aorist: ήμουν is the only past, for both "was" and "was being"
έχω | have | - - | είχα είχαμε | θα έχω | i | no aorist: είχα is the only past
ξέρω | know | - - | ήξερα ξέραμε | θα ξέρω | i | no aorist: ήξερα is the only past; ή- only where stressed
θέλω | want | θέλησα θελήσαμε | ήθελα θέλαμε | θα θέλω | i | ή- in the past continuous; θα θελήσω exists but θα θέλω is what people say
πάω | go | πήγα πήγαμε | πήγαινα πηγαίναμε | θα πάω | i | also πηγαίνω, πηγαίνεις, πηγαίνει - same past
έρχομαι | come | ήρθα ήρθαμε | ερχόμουν έρχονταν | θα έρθω | | -μαι in the present and past continuous, active endings in the past simple
βλέπω | see | είδα είδαμε | έβλεπα βλέπαμε | θα δω | | the ει- of είδα stays in every person
ξαναβλέπω | see again | ξαναείδα ξαναείδαμε | ξανάβλεπα ξαναβλέπαμε | θα ξαναδώ | | like βλέπω
λέω | say | είπα είπαμε | έλεγα λέγαμε | θα πω | i | the past continuous takes a γ: έλεγα
ξαναλέω | say again | ξαναείπα ξαναείπαμε | ξανάλεγα ξαναλέγαμε | θα ξαναπώ | i | like λέω
τρώω | eat | έφαγα φάγαμε | έτρωγα τρώγαμε | θα φάω | i | the past continuous takes a γ: έτρωγα
πίνω | drink | ήπια ήπιαμε | έπινα πίναμε | θα πιω | | the ή- of ήπια stays in every person
παίρνω | take | πήρα πήραμε | έπαιρνα παίρναμε | θα πάρω | | past πήρα with η, future πάρω with α
βρίσκω | find | βρήκα βρήκαμε | έβρισκα βρίσκαμε | θα βρω | |
μπαίνω | go in | μπήκα μπήκαμε | έμπαινα μπαίναμε | θα μπω | |
βγαίνω | go out | βγήκα βγήκαμε | έβγαινα βγαίναμε | θα βγω | |
ανεβαίνω | go up | ανέβηκα ανεβήκαμε | ανέβαινα ανεβαίναμε | θα ανεβώ | |
κατεβαίνω | go down | κατέβηκα κατεβήκαμε | κατέβαινα κατεβαίναμε | θα κατεβώ | |
δίνω | give | έδωσα δώσαμε | έδινα δίναμε | θα δώσω | | the past simple has ω: έδωσα
ξαναδίνω | give again | ξανάδωσα ξαναδώσαμε | ξανάδινα ξαναδίναμε | θα ξαναδώσω | | like δίνω
παραδίδω | hand over | παρέδωσα παραδώσαμε | παρέδιδα παραδίδαμε | θα παραδώσω | | like δίνω: past simple -δωσα
εκδίδω | issue | εξέδωσα εκδώσαμε | εξέδιδα εκδίδαμε | θα εκδώσω | | like δίνω; εκ- becomes εξ- before the ε-
βάζω | put | έβαλα βάλαμε | έβαζα βάζαμε | θα βάλω | | ζ becomes λ
βγάζω | take out | έβγαλα βγάλαμε | έβγαζα βγάζαμε | θα βγάλω | | ζ becomes λ
κάνω | do, make | έκανα κάναμε | έκανα κάναμε | θα κάνω | | past simple and past continuous look the same
φεύγω | leave | έφυγα φύγαμε | έφευγα φεύγαμε | θα φύγω | | ευ becomes υ
αποφεύγω | avoid | απέφυγα αποφύγαμε | απέφευγα αποφεύγαμε | θα αποφύγω | | like φεύγω
ξεφεύγω | escape | ξέφυγα ξεφύγαμε | ξέφευγα ξεφεύγαμε | θα ξεφύγω | | like φεύγω
μένω | stay, live | έμεινα μείναμε | έμενα μέναμε | θα μείνω | | ε becomes ει, no σ
περιμένω | wait | περίμενα περιμέναμε | περίμενα περιμέναμε | θα περιμένω | | past simple and past continuous look the same
ακούω | hear | άκουσα ακούσαμε | άκουγα ακούγαμε | θα ακούσω | i | the past continuous takes a γ: άκουγα
καίω | burn | έκαψα κάψαμε | έκαιγα καίγαμε | θα κάψω | i | ψ in the past simple, γ in the past continuous
πέφτω | fall | έπεσα πέσαμε | έπεφτα πέφταμε | θα πέσω | | φτ gives σ, not ψ

aino
μαθαίνω | learn | έμαθα μάθαμε | μάθαινα μαθαίναμε | θα μάθω | |
καταλαβαίνω | understand | κατάλαβα καταλάβαμε | καταλάβαινα καταλαβαίναμε | θα καταλάβω | |
προλαβαίνω | be in time | πρόλαβα προλάβαμε | προλάβαινα προλαβαίναμε | θα προλάβω | |
παθαίνω | suffer, happen to | έπαθα πάθαμε | πάθαινα παθαίναμε | θα πάθω | |
πεθαίνω | die | πέθανα πεθάναμε | πέθαινα πεθαίναμε | θα πεθάνω | |
αρρωσταίνω | fall ill | αρρώστησα αρρωστήσαμε | αρρώσταινα αρρωσταίναμε | θα αρρωστήσω | | -ησα, like an -άω verb
παχαίνω | put on weight | πάχυνα παχύναμε | πάχαινα παχαίναμε | θα παχύνω | | αι becomes υ
σημαίνω | mean | σήμανα σημάναμε | σήμαινα σημαίναμε | θα σημάνω | | mostly 3rd person: τι σημαίνει; τι σήμαινε;

nu
φέρνω | bring | έφερα φέραμε | έφερνα φέρναμε | θα φέρω | | the ν drops, no σ
καταφέρνω | manage | κατάφερα καταφέραμε | κατάφερνα καταφέρναμε | θα καταφέρω | | like φέρνω
στέλνω | send | έστειλα στείλαμε | έστελνα στέλναμε | θα στείλω | | ε becomes ει, the ν drops
παραγγέλνω | order | παρήγγειλα παραγγείλαμε | παράγγελνα παραγγέλναμε | θα παραγγείλω | | also spelt παραγγέλλω; like στέλνω. The dictionary prefers παράγγειλα; παρήγγειλα is just as common in speech
πλένω | wash | έπλυνα πλύναμε | έπλενα πλέναμε | θα πλύνω | | ε becomes υ
ξεπλένω | rinse | ξέπλυνα ξεπλύναμε | ξέπλενα ξεπλέναμε | θα ξεπλύνω | | like πλένω
κρίνω | judge | έκρινα κρίναμε | έκρινα κρίναμε | θα κρίνω | | the ν stays, no σ: both pasts look the same
διακρίνω | make out | διέκρινα διακρίναμε | διέκρινα διακρίναμε | θα διακρίνω | | like κρίνω
συγκρίνω | compare | σύγκρινα συγκρίναμε | σύγκρινα συγκρίναμε | θα συγκρίνω | | like κρίνω
προτείνω | suggest | πρότεινα προτείναμε | πρότεινα προτείναμε | θα προτείνω | | the ν stays, no σ: both pasts look the same
ενθαρρύνω | encourage | ενθάρρυνα ενθαρρύναμε | ενθάρρυνα ενθαρρύναμε | θα ενθαρρύνω | | the ν stays, no σ: both pasts look the same
αυξάνω | increase | αύξησα αυξήσαμε | αύξανα αυξάναμε | θα αυξήσω | | -άνω gives -ησα

xi
παίζω | play | έπαιξα παίξαμε | έπαιζα παίζαμε | θα παίξω | |
αλλάζω | change | άλλαξα αλλάξαμε | άλλαζα αλλάζαμε | θα αλλάξω | |
κοιτάζω | look at | κοίταξα κοιτάξαμε | κοίταζα κοιτάζαμε | θα κοιτάξω | | also κοιτάω / κοιτώ - same past simple
φωνάζω | shout, call | φώναξα φωνάξαμε | φώναζα φωνάζαμε | θα φωνάξω | |
στάζω | drip | έσταξα στάξαμε | έσταζα στάζαμε | θα στάξω | |
νυστάζω | feel sleepy | νύσταξα νυστάξαμε | νύσταζα νυστάζαμε | θα νυστάξω | |
ταιριάζω | match, suit | ταίριαξα ταιριάξαμε | ταίριαζα ταιριάζαμε | θα ταιριάξω | |
πετάω | throw, fly | πέταξα πετάξαμε | πετούσα πετούσαμε | θα πετάξω | | -άω but ξ, not -ησα
φυσάω | blow | φύσηξα φυσήξαμε | φυσούσα φυσούσαμε | θα φυσήξω | | -ηξα, not -ησα

asa
ξεχνάω | forget | ξέχασα ξεχάσαμε | ξεχνούσα ξεχνούσαμε | θα ξεχάσω | | the ν drops: ξεχ-άσα
περνάω | pass, spend | πέρασα περάσαμε | περνούσα περνούσαμε | θα περάσω | | the ν drops: περ-άσα
ξαναπερνάω | pass again | ξαναπέρασα ξαναπεράσαμε | ξαναπερνούσα ξαναπερνούσαμε | θα ξαναπεράσω | | like περνάω
ξεπερνάω | exceed, get over | ξεπέρασα ξεπεράσαμε | ξεπερνούσα ξεπερνούσαμε | θα ξεπεράσω | | like περνάω
πεινάω | be hungry | πείνασα πεινάσαμε | πεινούσα πεινούσαμε | θα πεινάσω | |
διψάω | be thirsty | δίψασα διψάσαμε | διψούσα διψούσαμε | θα διψάσω | |
χαλάω | break, spoil | χάλασα χαλάσαμε | χαλούσα χαλούσαμε | θα χαλάσω | |
γελάω | laugh | γέλασα γελάσαμε | γελούσα γελούσαμε | θα γελάσω | |
φοράω | wear | φόρεσα φορέσαμε | φορούσα φορούσαμε | θα φορέσω | |
πονάω | hurt | πόνεσα πονέσαμε | πονούσα πονούσαμε | θα πονέσω | |
γυρνάω | turn, come back | γύρισα γυρίσαμε | γυρνούσα γυρνούσαμε | θα γυρίσω | | the past simple comes from γυρίζω
τριγυρνάω | wander around | τριγύρισα τριγυρίσαμε | τριγυρνούσα τριγυρνούσαμε | θα τριγυρίσω | | like γυρνάω
μπορώ | can | μπόρεσα μπορέσαμε | μπορούσα μπορούσαμε | θα μπορέσω | | θα μπορώ is also common
καλώ | invite, call | κάλεσα καλέσαμε | καλούσα καλούσαμε | θα καλέσω | |
παρακαλώ | ask, beg | παρακάλεσα παρακαλέσαμε | παρακαλούσα παρακαλούσαμε | θα παρακαλέσω | | like καλώ
προσκαλώ | invite | προσκάλεσα προσκαλέσαμε | προσκαλούσα προσκαλούσαμε | θα προσκαλέσω | | like καλώ
προκαλώ | cause | προκάλεσα προκαλέσαμε | προκαλούσα προκαλούσαμε | θα προκαλέσω | | like καλώ
ανακαλώ | recall | ανακάλεσα ανακαλέσαμε | ανακαλούσα ανακαλούσαμε | θα ανακαλέσω | | like καλώ
αρκώ | be enough | άρκεσα αρκέσαμε | αρκούσα αρκούσαμε | θα αρκέσω | | mostly 3rd person: αρκεί, άρκεσε
ζω | live | έζησα ζήσαμε | ζούσα ζούσαμε | θα ζήσω | | one syllable in the present: ζω, ζεις, ζει

learned
λαμβάνω | receive | έλαβα λάβαμε | λάμβανα λαμβάναμε | θα λάβω | | the μ drops: λαμβ- / λαβ-
επαναλαμβάνω | repeat | επανέλαβα επαναλάβαμε | επαναλάμβανα επαναλαμβάναμε | θα επαναλάβω | | like λαμβάνω
περιλαμβάνω | include | περιέλαβα περιλάβαμε | περιλάμβανα περιλαμβάναμε | θα περιλάβω | | like λαμβάνω
συμπεριλαμβάνω | include | συμπεριέλαβα συμπεριλάβαμε | συμπεριλάμβανα συμπεριλαμβάναμε | θα συμπεριλάβω | | like λαμβάνω
απολαμβάνω | enjoy | απόλαυσα απολαύσαμε | απολάμβανα απολαμβάναμε | θα απολαύσω | | -λαυσα, not -λαβα
επιτυγχάνω | achieve, succeed | επέτυχα επιτύχαμε | επιτύγχανα επιτυγχάναμε | θα επιτύχω | | formal; everyday speech uses πετυχαίνω: πέτυχα, θα πετύχω
διεξάγω | carry out | διεξήγαγα διεξαγάγαμε | διεξήγα διεξήγαμε | θα διεξαγάγω | i | -άγω gives -ήγαγα
παράγω | produce | παρήγαγα παραγάγαμε | παρήγα παράγαμε | θα παραγάγω | i | -άγω gives -ήγαγα
αναπαράγω | reproduce | αναπαρήγαγα αναπαραγάγαμε | αναπαρήγα αναπαράγαμε | θα αναπαραγάγω | i | like παράγω
αναπτύσσω | develop | ανέπτυξα αναπτύξαμε | ανέπτυσσα αναπτύσσαμε | θα αναπτύξω | | -σσω gives ξ
συντάσσω | draw up | συνέταξα συντάξαμε | συνέτασσα συντάσσαμε | θα συντάξω | | -σσω gives ξ
συμβάλλω | contribute | συνέβαλα συμβάλαμε | συνέβαλλα συμβάλλαμε | θα συμβάλω | | one λ in the past simple, two in the past continuous
συμμετέχω | take part | συμμετείχα συμμετέχαμε | συμμετείχα συμμετέχαμε | θα συμμετάσχω | i | like έχω: συμμετείχα serves both pasts (formal past simple συμμετέσχα); θα συμμετέχω is also common
παρέχω | provide | παρέσχα παράσχαμε | παρείχα παρέχαμε | θα παράσχω | i | like έχω: past continuous παρείχα (ει only where stressed). The past simple is formal and mostly 3rd person: παρέσχε
υπάρχω | exist | υπήρξα υπήρξαμε | υπήρχα υπήρχαμε | θα υπάρξω | i | ά becomes ή in both pasts
προϋπάρχω | pre-exist | προϋπήρξα προϋπήρξαμε | προϋπήρχα προϋπήρχαμε | θα προϋπάρξω | i | like υπάρχω
αναπνέω | breathe | ανέπνευσα αναπνεύσαμε | ανέπνεα αναπνέαμε | θα αναπνεύσω | | -έω gives -ευσα
συνδέω | connect | συνέδεσα συνδέσαμε | συνέδεα συνδέαμε | θα συνδέσω | | -έω gives -εσα
συνιστώ | recommend | συνέστησα συστήσαμε | συνιστούσα συνιστούσαμε | θα συστήσω | | the ν drops in the past simple: συ-στήσ-
καθιστώ | render | κατέστησα καταστήσαμε | καθιστούσα καθιστούσαμε | θα καταστήσω | | καθ- becomes κατ- in the past simple
αντικαθιστώ | replace | αντικατέστησα αντικαταστήσαμε | αντικαθιστούσα αντικαθιστούσαμε | θα αντικαταστήσω | | like καθιστώ
διαρκώ | last | διήρκεσα διαρκέσαμε | διαρκούσα διαρκούσαμε | θα διαρκέσω | | mostly 3rd person: διαρκεί, διήρκεσε

mai
γίνομαι | become | έγινα γίναμε | γινόμουν γίνονταν | θα γίνω | | active endings in the past simple
κάθομαι | sit | κάθισα καθίσαμε | καθόμουν κάθονταν | θα καθίσω | | active endings; spoken future θα κάτσω
βρίσκομαι | be (somewhere) | βρέθηκα βρεθήκαμε | βρισκόμουν βρίσκονταν | θα βρεθώ | | ι becomes ε
χαίρομαι | be glad | χάρηκα χαρήκαμε | χαιρόμουν χαίρονταν | θα χαρώ | | αι becomes α
φαίνομαι | seem | φάνηκα φανήκαμε | φαινόμουν φαίνονταν | θα φανώ | | αι becomes α
αισθάνομαι | feel | αισθάνθηκα αισθανθήκαμε | αισθανόμουν αισθάνονταν | θα αισθανθώ | | the ν stays: -νθηκα
απευθύνομαι | address, turn to | απευθύνθηκα απευθυνθήκαμε | απευθυνόμουν απευθύνονταν | θα απευθυνθώ | | the ν stays: -νθηκα
ανταποκρίνομαι | respond | ανταποκρίθηκα ανταποκριθήκαμε | ανταποκρινόμουν ανταποκρίνονταν | θα ανταποκριθώ | |
τρελαίνομαι | go mad, be crazy about | τρελάθηκα τρελαθήκαμε | τρελαινόμουν τρελαίνονταν | θα τρελαθώ | | αι drops: τρελ-άθηκα
δίνομαι | be given | δόθηκα δοθήκαμε | δινόμουν δίνονταν | θα δοθώ | | ι becomes ο
καίγομαι | get burnt | κάηκα καήκαμε | καιγόμουν καίγονταν | θα καώ | |
ξεπερνιέμαι | be outdated | ξεπεράστηκα ξεπεραστήκαμε | ξεπερνιόμουν ξεπερνιόνταν | θα ξεπεραστώ | | like ξεπερνάω
εύχομαι | wish | ευχήθηκα ευχηθήκαμε | ευχόμουν εύχονταν | θα ευχηθώ | | -ήθηκα
υπόσχομαι | promise | υποσχέθηκα υποσχεθήκαμε | υποσχόμουν υπόσχονταν | θα υποσχεθώ | | -έθηκα
αντιλαμβάνομαι | realise | αντιλήφθηκα αντιληφθήκαμε | αντιλαμβανόμουν αντιλαμβάνονταν | θα αντιληφθώ | | -λήφθηκα
επιτυγχάνομαι | be achieved | επιτεύχθηκα επιτευχθήκαμε | επιτυγχανόμουν επιτυγχάνονταν | θα επιτευχθώ | | mostly 3rd person: επιτεύχθηκε
λέγομαι | be called | - - | λεγόμουν λέγονταν | θα λέγομαι | i | "my name was": λεγόμουν; no past simple in this sense

loan
σερβίρω | serve | σέρβιρα σερβίραμε | σέρβιρα σερβίραμε | θα σερβίρω | | also σερβίρισα; both pasts look the same
παρκάρω | park | πάρκαρα παρκάραμε | πάρκαρα παρκάραμε | θα παρκάρω | | also παρκάρισα; both pasts look the same
τρακάρω | crash (a car) | τράκαρα τρακάραμε | τράκαρα τρακάραμε | θα τρακάρω | | also τρακάρισα; both pasts look the same
"""

# The present singular, where the ending rules do not give it.
PRESENT = {
    u'είμαι': (u'είσαι', u'είναι'),
    u'λέω': (u'λες', u'λέει'), u'ξαναλέω': (u'ξαναλές', u'ξαναλέει'),
    u'τρώω': (u'τρως', u'τρώει'), u'ακούω': (u'ακούς', u'ακούει'),
    u'καίω': (u'καις', u'καίει'), u'πάω': (u'πας', u'πάει'),
    u'ζω': (u'ζεις', u'ζει'),
}

# Futures whose persons are not the 1sg with -εις / -ει: spelled out on the card.
FUT_FULL = {
    u'θα δω': u'δω, δεις, δει, δούμε, δείτε, δουν',
    u'θα ξαναδώ': u'ξαναδώ, ξαναδείς, ξαναδεί, ξαναδούμε, ξαναδείτε, ξαναδούν',
    u'θα πω': u'πω, πεις, πει, πούμε, πείτε, πουν',
    u'θα ξαναπώ': u'ξαναπώ, ξαναπείς, ξαναπεί, ξαναπούμε, ξαναπείτε, ξαναπούν',
    u'θα πιω': u'πιω, πιεις, πιει, πιούμε, πιείτε, πιουν',
    u'θα φάω': u'φάω, φας, φάει, φάμε, φάτε, φάνε',
    u'θα πάω': u'πάω, πας, πάει, πάμε, πάτε, πάνε',
    u'θα βρω': u'βρω, βρεις, βρει, βρούμε, βρείτε, βρουν',
    u'θα μπω': u'μπω, μπεις, μπει, μπούμε, μπείτε, μπουν',
    u'θα βγω': u'βγω, βγεις, βγει, βγούμε, βγείτε, βγουν',
    u'θα ανεβώ': u'ανεβώ, ανεβείς, ανεβεί, ανεβούμε, ανεβείτε, ανεβούν',
    u'θα κατεβώ': u'κατεβώ, κατεβείς, κατεβεί, κατεβούμε, κατεβείτε, κατεβούν',
    u'θα καώ': u'καώ, καείς, καεί, καούμε, καείτε, καούν',
}

# States, not actions: English says "I knew", not "I was knowing", for the
# past continuous of these.
STATIVE = {u'είμαι', u'έχω', u'ξέρω', u'θέλω', u'μπορώ', u'σημαίνω', u'υπάρχω',
           u'προϋπάρχω', u'αρκώ', u'διαρκώ', u'πεινάω', u'διψάω', u'φαίνομαι',
           u'βρίσκομαι', u'χαίρομαι', u'λέγομαι', u'νυστάζω', u'ταιριάζω',
           u'περιλαμβάνω', u'συμπεριλαμβάνω', u'αισθάνομαι', u'πονάω'}


def english(v, en):
    """The 1st person singular in English: present, past simple, past
    continuous, future."""
    i_pres, _, _, i_past, _, ing = en
    base = i_pres[3:] if i_pres.startswith(u'am ') else i_pres
    base = u'be ' + base if i_pres.startswith(u'am ') else base
    if i_pres == u'am':
        base = u'be'
    cont = i_past if (v['pres'] in STATIVE or ing == u'-') else u'was ' + ing
    fut = u'will be able to' if v['pres'] == u'μπορώ' else u'will ' + base
    return u'I ' + i_pres, u'I ' + i_past, u'I ' + cont, u'I ' + fut


PRON = [u'εγώ', u'εσύ', u'αυτός', u'εμείς', u'εσείς', u'αυτοί']


def parse():
    verbs, group = [], None
    for line in DATA.strip().split(u'\n'):
        line = line.strip()
        if not line:
            continue
        if u'|' not in line:
            group = line
            continue
        f = [x.strip() for x in line.split(u'|')]
        assert len(f) == 7, line
        pres, mean, aor, imp, fut, flags, note = f
        a1, a2 = aor.split()
        i1, i2 = imp.split()
        verbs.append(dict(pres=pres, mean=mean, group=group, aor=(a1, a2),
                          imp=(i1, i2), fut=fut, imp_irr=u'i' in flags, note=note))
    return verbs


def present_sg(p):
    if p in PRESENT:
        return (p,) + PRESENT[p]
    if p.endswith(u'ιέμαι'):
        s = p[:-4]
        return p, s + u'έσαι', s + u'έται'
    if p.endswith(u'ομαι'):
        s = p[:-4]
        return p, s + u'εσαι', s + u'εται'
    if p.endswith(u'άω'):
        s = p[:-2]
        return p, s + u'άς', s + u'άει'
    if p.endswith(u'ώ'):
        s = p[:-1]
        return p, s + u'είς', s + u'εί'
    assert p.endswith(u'ω'), p
    s = p[:-1]
    return p, s + u'εις', s + u'ει'


def active6(sg1, pl1):
    assert sg1.endswith(u'α') and pl1.endswith(u'αμε'), (sg1, pl1)
    st, pst = sg1[:-1], pl1[:-3]
    return [sg1, st + u'ες', st + u'ε', pl1, pst + u'ατε', st + u'αν']


def aorist6(v):
    a1, a2 = v['aor']
    return None if a1 == u'-' else active6(a1, a2)


def imperfect6(v):
    i1, i2 = v['imp']
    if i1 == u'ήμουν':
        return [u'ήμουν', u'ήσουν', u'ήταν', u'ήμασταν', u'ήσασταν', u'ήταν']
    if i1.endswith(u'όμουν'):
        s = i1[:-5]
        return [i1, s + u'όσουν', s + u'όταν', s + u'όμασταν', s + u'όσασταν', i2]
    return active6(i1, i2)


def fut_irregular(v):
    """The future is irregular when it is not the past-simple stem + -ω
    (active) or + -ώ (passive -ηκα): θα δω from είδα, θα πάρω from πήρα."""
    a1, a2 = v['aor']
    f = deaccent(v['fut'][3:]).split()[0]
    if a1 == u'-':
        return False
    if a2.endswith(u'ήκαμε'):
        want = deaccent(a2[:-5]) + u'ω'
    else:
        want = deaccent(a2[:-3]) + u'ω'
        # the augment stays only in the past: έδωσα / δώσαμε -> δώσω
    return f != want


# one syllable when spoken (πιω = pχo), though the letters show two vowels
SYNIZESIS = {u'πιω'}


def check_word(w, where):
    n = sum(1 for c in w if c in u'άέήίόύώΐΰ')
    syl = 1 if w in SYNIZESIS else len(nuclei(w))
    if syl > 1:
        assert n == 1, (where, w)
    else:
        assert n <= 1, (where, w)


def klik_books():
    """headword -> 'A1+A2+EXAM' etc., from the A1+A2 dictionary; the old A2
    glossary fills in what that file merged away."""
    books = {}
    if os.path.isfile(XLSX):
        import openpyxl
        wb = openpyxl.load_workbook(XLSX, read_only=True)
        for r in list(wb['Dictionary'].iter_rows(values_only=True))[1:]:
            if r[1] == 'verb' and r[0]:
                books.setdefault(deaccent(str(r[0]).lower()), r[4])
    for rec in io.open(A2GLOSS, encoding='utf-8').read().split(u'\n\n'):
        l = rec.strip().split(u'\n')
        if len(l) >= 4 and u'— verb' in l[3]:
            books.setdefault(deaccent(l[1].lower()), u'A2')
    return books


def main():
    verbs = parse()
    names = dict(GROUPS)
    assert all(v['group'] in names for v in verbs)
    assert len({v['pres'] for v in verbs}) == len(verbs), 'duplicate verb'
    books = klik_books()
    alias = {u'πάω': u'πηγαίνω', u'παραγγέλνω': u'παραγγέλλω'}
    missing = []
    for v in verbs:
        b = books.get(deaccent(v['pres'])) or books.get(deaccent(alias.get(v['pres'], u'')))
        if not b:
            missing.append(v['pres'])
        v['books'] = b or u'?'
    if missing and books:
        print('WARNING - not a KLIK headword:', u', '.join(missing))

    EN = en_table()
    assert set(EN) == {v['pres'] for v in verbs}, set(EN) ^ {v['pres'] for v in verbs}
    cards, rows = [], []
    for v in verbs:
        e_pres, e_past, e_cont, e_fut = english(v, EN[v['pres']])
        sg = present_sg(v['pres'])
        aor, imp = aorist6(v), imperfect6(v)
        for w in list(sg) + (aor or []) + imp + v['fut'][3:].split():
            check_word(w, v['pres'])
        v['fut_irr'] = fut_irregular(v)

        # ---- the card
        front = u' · '.join(sg)
        w1 = max([len(u'past simple'), len(e_past)] + [len(x) for x in (aor or [u'—'])]) + 2
        lines = [u'%-7s%-*s%s' % (u'', w1, u'past simple', u'past continuous')]
        for k in range(6):
            lines.append(u'%-7s%-*s%s' % (PRON[k], w1, aor[k] if aor else u'—', imp[k]))
        lines.append(u'%-7s%-*s%s' % (u'EN', w1, e_past if aor else u'—', e_cont))
        full = FUT_FULL.get(v['fut'])
        lines.append(u'%-7s%s  = %s' % (u'θα', full or v['fut'][3:], e_fut))
        if v['note']:
            lines.append(u'⚠ ' + v['note'])
        eng = e_pres
        cards.append((front, u' · '.join(latin(x) for x in sg), eng, lines))

        # ---- the grid row
        def b(s, on):
            return u'**%s**' % s if on else s
        a_txt = u'—' if not aor else u'%s · %s' % (aor[0], aor[3])
        rows.append([v['group'], u' · '.join(sg), v['mean'],
                     b(a_txt, aor is not None),
                     b(u'%s · %s' % (imp[0], imp[3]), v['imp_irr']),
                     b(v['fut'], v['fut_irr']), v['books'], v['note']])

    out = []
    for i, (front, lat, eng, lines) in enumerate(cards, 1):
        out.append(u'%d\n%s\n%s\n%s | %s\n' % (i, front, lat, eng,
                                                u' | '.join(lines)))
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(out))
    print('%d cards -> %s' % (len(cards), OUT))

    if os.path.isdir(os.path.dirname(TSV)):
        head = [u'group', u'present', u'meaning', u'past simple', u'past continuous',
                u'future', u'books', u'note']
        with io.open(TSV, 'w', encoding='utf-8', newline='\n') as f:
            f.write(u'# generated by LangCards/tools/irregulardeck.py - edit the list there\n')
            f.write(u'# group\t' + u'\t'.join(u'%s=%s' % g for g in GROUPS) + u'\n')
            f.write(u'\t'.join(head) + u'\n')
            for r in rows:
                assert not any(u'\t' in c for c in r)
                f.write(u'\t'.join(r) + u'\n')
        print('%d rows  -> %s' % (len(rows), TSV))
    from collections import Counter
    print(Counter(v['group'] for v in verbs))
    print('future irregular:', u', '.join(v['fut'] for v in verbs if v['fut_irr']))


if __name__ == '__main__':
    main()
