# -*- coding: utf-8 -*-
"""Build the A2 writing deck: 100 ready phrases for the two exam texts.

The A2 writing paper has two parts of 80-100 words each:

  * Part A, informal - a letter or email to a friend. Past topics (Κέντρο
    Ελληνικής Γλώσσας, 2015-2018): an accident, music lessons you started, a
    painting prize you won, a new restaurant you tried.
  * Part B, more formal - an announcement, a letter to people you don't know.
    Past topics: photography lessons, a letter to a host family, your city
    described for a school forum, new activities at the library. The
    University of Cyprus adds invitations, thank-you letters and
    congratulations.

The phrases follow those topics, so every card is something that could go
straight into one of those texts. Each back says which part it belongs to and
where in the text it goes.

Run from anywhere:  python tools/writingdeck.py
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
LC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b1deck import translit                                 # noqa: E402

OUT = os.path.join(LC, 'greek-a2-writing-100-phrases.txt')

INF, FOR = u'INFORMAL', u'FORMAL'

CARDS = [
    # ------------------------------------------------ informal: opening
    (INF, u'opening', u'Λευκωσία, 15 Μαΐου 2025',
     u'Nicosia, 15 May 2025 — top right; the month in the genitive'),
    (INF, u'opening', u'Γεια σου, Νίκο!',
     u'Hi Nikos! — the name in the vocative: Νίκος → Νίκο'),
    (INF, u'opening', u'Αγαπητή μου Ελένη,',
     u'My dear Eleni,'),
    (INF, u'opening', u'Πώς είσαι; Εγώ είμαι πολύ καλά.',
     u'How are you? I am very well.'),
    (INF, u'opening', u'Πώς πέρασες το Σαββατοκύριακο;',
     u'How was your weekend?'),
    (INF, u'opening', u'Ελπίζω να είσαι καλά.',
     u'I hope you are well.'),
    (INF, u'opening', u'Συγγνώμη που δεν σου έγραψα τόσο καιρό.',
     u"Sorry I haven't written to you for so long."),
    (INF, u'opening', u'Ευχαριστώ πολύ για το γράμμα σου.',
     u'Thank you very much for your letter.'),
    (INF, u'opening', u'Χάρηκα πολύ που πήρα το μήνυμά σου.',
     u'I was very glad to get your message.'),
    (INF, u'reason', u'Σου γράφω για να σου πω τα νέα μου.',
     u"I'm writing to tell you my news."),
    (INF, u'reason', u'Έχω πολύ καλά νέα!',
     u'I have very good news!'),
    (INF, u'reason', u'Δεν είμαι πολύ καλά.',
     u"I'm not very well. — opener for bad news"),
    (INF, u'reason', u'Θέλω να σου πω τι έγινε την προηγούμενη εβδομάδα.',
     u'I want to tell you what happened last week.'),
    # ------------------------------------------------ informal: the news
    (INF, u'news · accident', u'Πριν από λίγες μέρες είχα ένα ατύχημα.',
     u'A few days ago I had an accident.'),
    (INF, u'news · accident', u'Έπεσα από το ποδήλατο και έσπασα το χέρι μου.',
     u'I fell off my bike and broke my arm.'),
    (INF, u'news · accident', u'Πήγα αμέσως στο νοσοκομείο.',
     u'I went to the hospital straight away.'),
    (INF, u'news · accident', u'Τώρα είμαι καλύτερα, αλλά πρέπει να μείνω στο σπίτι μια εβδομάδα.',
     u'Now I am better, but I have to stay at home for a week.'),
    (INF, u'news · lessons', u'Ξεκίνησα μαθήματα πιάνου.',
     u'I have started piano lessons.'),
    (INF, u'news · lessons', u'Έχω μάθημα δύο φορές την εβδομάδα.',
     u'I have a lesson twice a week.'),
    (INF, u'news · lessons', u'Η δασκάλα μου είναι πολύ καλή και υπομονετική.',
     u'My teacher is very good and patient.'),
    (INF, u'news · lessons', u'Είμαι πολύ ευχαριστημένος με τα μαθήματα.',
     u"I'm very pleased with the lessons. — a woman writes ευχαριστημένη"),
    (INF, u'news · prize', u'Κέρδισα το πρώτο βραβείο σε έναν διαγωνισμό!',
     u'I won first prize in a competition!'),
    (INF, u'news · prize', u'Ο διαγωνισμός έγινε στο Δημαρχείο τον περασμένο μήνα.',
     u'The competition took place at the Town Hall last month.'),
    (INF, u'news · prize', u'Το βράδυ γιορτάσαμε με τους φίλους μου.',
     u'In the evening we celebrated with my friends.'),
    (INF, u'news · outing', u'Το Σάββατο πήγα σε ένα καινούριο εστιατόριο με την οικογένειά μου.',
     u'On Saturday I went to a new restaurant with my family.'),
    (INF, u'news · outing', u'Φάγαμε ψάρι και σαλάτα. Όλα ήταν πολύ νόστιμα.',
     u'We ate fish and salad. Everything was very tasty.'),
    (INF, u'news · outing', u'Πληρώσαμε μόνο 20 ευρώ ο καθένας.',
     u'We paid only 20 euros each.'),
    (INF, u'news · outing', u'Μετά πήγαμε βόλτα στην παραλία.',
     u'Afterwards we went for a walk on the beach.'),
    (INF, u'news · outing', u'Μου άρεσε πολύ το φαγητό.',
     u'I liked the food a lot.'),
    # ------------------------------------------------ informal: feelings
    (INF, u'feelings', u'Πέρασα πολύ ωραία.',
     u'I had a really good time.'),
    (INF, u'feelings', u'Ήταν μια υπέροχη μέρα!',
     u'It was a wonderful day!'),
    (INF, u'feelings', u'Ήμουν πολύ χαρούμενος.',
     u'I was very happy. — a woman writes χαρούμενη'),
    (INF, u'feelings', u'Δυστυχώς, ο καιρός δεν ήταν καλός.',
     u"Unfortunately, the weather wasn't good."),
    # ------------------------------------------------ informal: to the friend
    (INF, u'to your friend', u'Πρέπει να πας κι εσύ!',
     u'You must go too!'),
    (INF, u'to your friend', u'Θέλεις να έρθεις μαζί μου την επόμενη φορά;',
     u'Do you want to come with me next time?'),
    (INF, u'to your friend', u'Τι λες; Πάμε μαζί το Σάββατο;',
     u"What do you say? Shall we go together on Saturday?"),
    (INF, u'to your friend', u'Εσύ τι κάνεις; Πώς πάει η δουλειά;',
     u"And you, how are you doing? How's work going?"),
    (INF, u'to your friend', u'Πες μου τα νέα σου!',
     u'Tell me your news!'),
    # ------------------------------------------------ informal: closing
    (INF, u'closing', u'Γράψε μου σύντομα!',
     u'Write to me soon!'),
    (INF, u'closing', u'Περιμένω το γράμμα σου.',
     u"I'm waiting for your letter."),
    (INF, u'closing', u'Τα λέμε σύντομα!',
     u'See you soon! / Talk soon!'),
    (INF, u'closing', u'Χαιρετίσματα στην οικογένειά σου.',
     u'Say hello to your family.'),
    (INF, u'closing', u'Πολλά φιλιά,',
     u'Lots of love, (lit. many kisses)'),
    (INF, u'closing', u'Ο φίλος σου, Πέτρος',
     u'Your friend, Petros — a woman: Η φίλη σου, Μαρία. Sign with an invented name, never your own (exam rule)'),

    # ------------------------------------------------ formal: opening
    (FOR, u'opening', u'Αγαπητέ κύριε Παπαδόπουλε,',
     u'Dear Mr Papadopoulos, — the surname in the vocative: -ος → -ε'),
    (FOR, u'opening', u'Αγαπητή κυρία Γεωργίου,',
     u'Dear Mrs Georgiou,'),
    (FOR, u'opening', u'Αγαπητοί κύριε και κυρία Δέλλιου,',
     u'Dear Mr and Mrs Delliou, — from the 2016 exam (host family)'),
    (FOR, u'opening', u'Αξιότιμε κύριε / Αξιότιμη κυρία,',
     u'Dear Sir / Madam, — very formal, to someone you do not know'),
    (FOR, u'opening', u'Αγαπητοί φίλοι,',
     u'Dear friends, — for an announcement or a forum post'),
    (FOR, u'reason', u'Σας γράφω για να σας ευχαριστήσω για την υπέροχη βραδιά.',
     u"I'm writing to thank you for the wonderful evening."),
    (FOR, u'reason', u'Σας γράφω για να σας πω πότε θα φτάσω.',
     u"I'm writing to tell you when I will arrive."),
    # ------------------------------------------------ formal: thanks
    (FOR, u'thank you', u'Σας ευχαριστώ πολύ για τη βοήθειά σας.',
     u'Thank you very much for your help.'),
    (FOR, u'thank you', u'Σας ευχαριστώ για το υπέροχο δώρο.',
     u'Thank you for the wonderful present.'),
    (FOR, u'thank you', u'Σας ευχαριστώ για την πρόσκληση.',
     u'Thank you for the invitation.'),
    (FOR, u'thank you', u'Σας ευχαριστώ πολύ για τη φιλοξενία.',
     u'Thank you very much for your hospitality.'),
    (FOR, u'thank you', u'Πέρασα πολύ ωραία στο σπίτι σας.',
     u'I had a lovely time at your house.'),
    (FOR, u'thank you', u'Δεν θα ξεχάσω ποτέ αυτές τις μέρες.',
     u'I will never forget these days.'),
    (FOR, u'thank you', u'Ήταν μεγάλη χαρά για μένα να σας γνωρίσω.',
     u'It was a great pleasure for me to meet you.'),
    # ------------------------------------------------ formal: congratulations
    (FOR, u'congratulations', u'Συγχαρητήρια για τον γάμο σας!',
     u'Congratulations on your wedding!'),
    (FOR, u'congratulations', u'Να ζήσετε!',
     u'The traditional wish to a newly married couple (lit. may you live!)'),
    (FOR, u'congratulations', u'Συγχαρητήρια για το μωρό! Να σας ζήσει!',
     u'Congratulations on the baby! — Να σας ζήσει = may it live for you, the standard wish for a birth'),
    (FOR, u'congratulations', u'Συγχαρητήρια για τη νέα σας δουλειά!',
     u'Congratulations on your new job!'),
    (FOR, u'congratulations', u'Συγχαρητήρια για το πτυχίο σου!',
     u'Congratulations on your degree! — σου: to a friend'),
    (FOR, u'congratulations', u'Χρόνια πολλά για τα γενέθλιά σας!',
     u'Happy birthday! (lit. many years)'),
    (FOR, u'congratulations', u'Χρόνια πολλά για τη γιορτή σας!',
     u'Happy name day!'),
    (FOR, u'congratulations', u'Σας εύχομαι υγεία και ευτυχία.',
     u'I wish you health and happiness.'),
    (FOR, u'congratulations', u'Σας εύχομαι καλή επιτυχία στη νέα σας δουλειά.',
     u'I wish you every success in your new job.'),
    (FOR, u'congratulations', u'Καλή αρχή!',
     u'Good luck with the new start! — new job, school, home'),
    # ------------------------------------------------ formal: invitation
    (FOR, u'invitation', u'Θα ήθελα να σας προσκαλέσω στα γενέθλιά μου.',
     u'I would like to invite you to my birthday party.'),
    (FOR, u'invitation', u'Σας προσκαλούμε στον γάμο μας, το Σάββατο 10 Ιουνίου.',
     u'We invite you to our wedding, on Saturday 10 June.'),
    (FOR, u'invitation', u'Η γιορτή θα γίνει στο σπίτι μου, στις 8 το βράδυ.',
     u'The party will be at my house, at 8 in the evening.'),
    (FOR, u'invitation', u'Παρακαλώ, ενημερώστε με αν μπορείτε να έρθετε.',
     u'Please let me know if you can come.'),
    (FOR, u'saying no', u'Δυστυχώς, δεν μπορώ να έρθω, γιατί έχω δουλειά.',
     u"Unfortunately, I can't come, because I have work."),
    (FOR, u'saying no', u'Λυπάμαι πολύ, αλλά εκείνη τη μέρα δουλεύω.',
     u"I'm very sorry, but I'm working that day."),
    # ------------------------------------------------ formal: host family
    (FOR, u'about you', u'Θα φτάσω στην Αθήνα στις 3 Ιουλίου με το αεροπλάνο.',
     u'I will arrive in Athens on 3 July by plane.'),
    (FOR, u'about you', u'Θα μείνω τρεις εβδομάδες στο σπίτι σας.',
     u'I will stay at your house for three weeks.'),
    (FOR, u'about you', u'Είμαι τριάντα χρονών και δουλεύω ως μηχανικός.',
     u'I am thirty years old and I work as an engineer.'),
    (FOR, u'about you', u'Μου αρέσει πολύ το διάβασμα και το κολύμπι.',
     u'I really like reading and swimming.'),
    (FOR, u'about you', u'Τρώω σχεδόν τα πάντα, αλλά δεν τρώω κρέας.',
     u"I eat almost everything, but I don't eat meat."),
    # ------------------------------------------------ formal: announcement
    (FOR, u'announcement', u'ΑΝΑΚΟΙΝΩΣΗ',
     u'ANNOUNCEMENT — the title, in capitals'),
    (FOR, u'announcement', u'Σας αρέσει η φωτογραφία;',
     u'Do you like photography? — a question to open with, from the 2015 exam'),
    (FOR, u'announcement', u'Η ομάδα μας οργανώνει μαθήματα φωτογραφίας.',
     u'Our group is organising photography lessons.'),
    (FOR, u'announcement', u'Τα μαθήματα ξεκινούν τη Δευτέρα 5 Οκτωβρίου.',
     u'The lessons start on Monday 5 October.'),
    (FOR, u'announcement', u'Τα μαθήματα θα γίνονται κάθε Τρίτη και Πέμπτη, από τις 6 έως τις 8 το απόγευμα.',
     u'The lessons will take place every Tuesday and Thursday, from 6 to 8 in the evening.'),
    (FOR, u'announcement', u'Θα γίνουν στο Πολιτιστικό Κέντρο του Δήμου.',
     u"They will take place at the Municipality's Cultural Centre."),
    (FOR, u'announcement', u'Η τιμή είναι 50 ευρώ τον μήνα.',
     u'The price is 50 euros a month.'),
    (FOR, u'announcement', u'Η συμμετοχή είναι δωρεάν.',
     u'Taking part is free.'),
    (FOR, u'announcement', u'Μπορούν να έρθουν μικροί και μεγάλοι.',
     u'Young and old can come.'),
    (FOR, u'announcement', u'Στο τέλος των μαθημάτων θα κάνουμε μια έκθεση φωτογραφίας.',
     u'At the end of the lessons we will hold a photography exhibition.'),
    (FOR, u'announcement', u'Για περισσότερες πληροφορίες, τηλεφωνήστε στο 22 123456.',
     u'For more information, call 22 123456.'),
    (FOR, u'announcement', u'Σας περιμένουμε!',
     u'We look forward to seeing you! (lit. we are waiting for you)'),
    # ------------------------------------------------ formal: your city
    (FOR, u'your city', u'Η πόλη μου βρίσκεται στο νότιο μέρος της Κύπρου, κοντά στη θάλασσα.',
     u'My city is in the south of Cyprus, near the sea.'),
    (FOR, u'your city', u'Τον χειμώνα ο καιρός είναι ήπιος και το καλοκαίρι κάνει πολλή ζέστη.',
     u'In winter the weather is mild and in summer it is very hot.'),
    (FOR, u'your city', u'Τα πιο γνωστά αξιοθέατα είναι το κάστρο και το μουσείο.',
     u'The best-known sights are the castle and the museum.'),
    (FOR, u'your city', u'Σας προσκαλούμε να έρθετε εκδρομή στην πόλη μας!',
     u'We invite you to come on a trip to our city!'),
    # ------------------------------------------------ formal: closing
    (FOR, u'closing', u'Περιμένω την απάντησή σας.',
     u'I look forward to your reply.'),
    (FOR, u'closing', u'Ευχαριστώ εκ των προτέρων.',
     u'Thank you in advance.'),
    (FOR, u'closing', u'Με εκτίμηση,',
     u'Yours sincerely, — the most formal'),
    (FOR, u'closing', u'Με φιλικούς χαιρετισμούς,',
     u'Kind regards,'),
    (FOR, u'closing', u'Με θερμούς χαιρετισμούς,',
     u'Warm regards,'),
]


def latin(greek):
    """Word by word, so a capital in the Greek stays a capital in Latin."""
    out = []
    for w in greek.split(u' '):
        t = translit(w).replace(u';', u'?').replace(u'·', u';')
        if w[:1].isupper() and t:
            t = t[0].upper() + t[1:]
        out.append(t)
    return u' '.join(out)


def main():
    assert len(CARDS) == 100, len(CARDS)
    fronts = [c[2] for c in CARDS]
    assert len(set(fronts)) == 100, 'duplicate front'
    out = []
    for i, (part, slot, gr, en) in enumerate(CARDS, 1):
        out.append(u'%d\n%s\n%s\n%s | %s · %s\n' % (i, gr, latin(gr), en, part, slot))
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(u'\n'.join(out))
    n_inf = sum(1 for c in CARDS if c[0] == INF)
    print('%d cards (%d informal, %d formal) -> %s' % (len(CARDS), n_inf, 100 - n_inf, OUT))


if __name__ == '__main__':
    main()
