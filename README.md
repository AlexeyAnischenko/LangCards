# LangCards

A lightweight, browser-based flashcard application for learning foreign language vocabulary, initially created to learn Greek. 
Built with vanilla JavaScript and CSS, this single-page application runs entirely in the browser with no server requirements.

## Files

| File | What it is |
|------|------------|
| `langcards.html` | **The app.** Generated — open this one. Dictionaries are compressed inside it, so it works on its own. |
| `langcards.template.html` | **The source.** Same app *without* the embedded dictionaries. Edit this when changing markup, CSS or JS. |
| `build-langcards.py` | Compresses the `.txt` dictionaries into `langcards.template.html` and writes `langcards.html`. |
| `*-greek-sentences.txt`, `greek-endings-...-1000.txt` | The dictionary sources. Edit these to change card content, then rebuild. |

Editing `langcards.html` directly is a mistake — the next build overwrites it. Change
`langcards.template.html` or a `.txt` file, then run `python build-langcards.py`.

## Features

- **Self-contained**: `langcards.html` is the whole app — the four bundled dictionaries are
  compressed into the HTML and chosen from a dropdown next to the file picker, so the page works
  on its own with no `.txt` files alongside it
- **File Upload**: Import your own vocabulary lists from text files
- **Smart Parsing**: Robust parsing of vocabulary files with detailed error reporting
- **Dark Mode**: Toggle between light and dark themes
- **Study Modes**:
  - Greek-only mode (show Greek first, click to reveal English)
  - Mixed mode (randomly shows either Greek or English first)
- **Transcription Support**: Shown under the Greek text when a card is revealed, and on hover
  over the Greek text as a tooltip
- **One-key / one-tap study loop**: `Space` (or a tap/click on the card) reveals the
  transcription and translation; again draws the next card
- **Phone-friendly**: on a narrow screen the controls stack into a single column, the deck
  picker leads, and the card fills the tall viewport — the whole study loop is one thumb tap
- **Progress Tracking**: Shows current card number and total cards
- **Random Card Selection**: Cards are presented in random order for better learning
- **Debug Information**: Optional detailed parsing information for troubleshooting

## File Format

The application expects a text file with vocabulary entries in the following format:

```
1
Γεια. Γεια σας, τι κάνετε;
Ya. Ya sas, ti kánete?
Hello. Hello, how are you?
```

Each card entry is exactly 4 lines:
1. Card number
2. Greek text
3. Transcription in Latin alphabet
4. English translation

Entries may be separated by a blank line (as the bundled dictionaries are) or run straight
together — the parser accepts both, along with CRLF line endings and a UTF-8 BOM.

### Fill-in-the-blank decks

The third line does not have to be a transcription — it is simply whatever you want revealed
alongside the translation. The bundled **Grammar** deck uses it for the completed sentence, so
line 2 is a prompt with a `___` gap and line 3 is the same sentence with the gap filled:

```
1
Πηγαίνω ___ σχολείο κάθε μέρα.
Πηγαίνω στο σχολείο κάθε μέρα.
I go to school every day.
```

### The bundled dictionaries

| Deck | Cards | Third line holds |
|------|-------|------------------|
| A2 exam | 458 | transcription |
| Common | 1072 | transcription |
| Travel | 292 | transcription |
| Grammar | 746 | the completed sentence |

They have been cleaned up:

- **Deduplicated** — where two entries had identical Greek text, only the first was kept.
- **Proofread** — every card was checked for Greek and English grammar. Corrections covered
  gender and agreement errors, the final-ν rule (`μη`/`μην`, `στη`/`στην`), missing second
  accents on proparoxytones with an enclitic (`τη βοήθειά σας`), missing prepositions, and
  transcriptions that romanised the wrong word or word form.

- **Renumbered** — after the cleanup each deck is numbered contiguously from 1, so the `#N` on a
  card is also its position in the `.txt` file.

The Grammar deck additionally had its prompts repaired where the `___` gap did not line up with
the completed sentence (a gap that filled with nothing, a prompt whose word order differed from
the answer, a missing second accent), and its gap marker normalised to `___` throughout. Its
grammar pass also corrected 101 breaches of the final-ν rule (`την`/`στην` before a consonant
that does not keep the ν) — the very rule several of its cards set out to teach.

## Usage

0. Open `langcards.html` in your browser.
1. Pick a bundled dictionary from the dropdown, or click "Upload Dictionary File" to load your
   own vocabulary file
2. The application will parse the file and display the number of cards loaded
3. Use the checkbox to toggle between Greek-only and mixed modes
4. Tap the card, or press `Space`, to reveal the transcription and translation
5. Tap or press `Space` again — or use "Next Card" — to get a new random card
6. On a device with a mouse, hover over the Greek text to see its transcription as a tooltip

## Building langcards.html

`langcards.html` is **generated**. Edit `langcards.template.html` (the app without the embedded
dictionaries), then regenerate:

```
python build-langcards.py
```

The same script also rebuilds after any `.txt` edit. Its `DICTS` list at the top controls which
dictionaries get embedded and how they are labelled in the dropdown. Each is stored as
raw-deflate + base64 (341 KB of text becomes 119 KB of payload) and the page inflates them with
the browser's `DecompressionStream`, so it needs a reasonably current browser (Chrome 103+,
Firefox 113+, Safari 16.4+).

## Error Handling

A record starts at a line that is a bare number and ends at the next bare number or at a blank
line. That makes the parser self-synchronising: anything it does not recognise — stray prose,
` ``` ` fences, a card missing a field — is skipped and reported with its line number, and can
never be silently absorbed into a neighbouring card.

- Validates card number format
- Reports entries that have fewer than 3 fields, with the line they start on
- Warns about duplicate card numbers
- Provides detailed parsing information through the debug view

All four bundled dictionaries currently parse with 0 skipped entries.
