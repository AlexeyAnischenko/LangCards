# LangCards

A lightweight, browser-based flashcard application for learning foreign language vocabulary, initially created to learn Greek. 
Built with vanilla JavaScript and CSS, this single-page application runs entirely in the browser with no server requirements.

## Features

- **File Upload**: Import vocabulary lists (decks of flashcards, dictionaries) from local text files, or by URL parameter: `?url=http://path/to/your/deck.txt`
- **Smart Parsing**: Robust parsing of vocabulary files with detailed error reporting
- **Embedded Deck**: Export html with current deck embedded - creating a single file flashcards drill trainer
- **Dark Mode**: Toggle between light and dark themes
- **Study Modes**:
  - Greek-only mode (show Greek first, click to reveal English)
  - Mixed mode (randomly shows either Greek or English first)
- **Transcription Support**: Hover over Greek text to see Latin alphabet transcription
- **Progress Tracking**: Shows current card number and total cards
- **Random Card Selection**: Cards are shuffled, and there is a button to reshuffle the deck again
- **Debug Information**: Optional detailed parsing information for troubleshooting

## File Format

The application expects a text file with vocabulary entries in the following format:

```
1
Γεια. Γεια σας, τι κάνετε;
Ya. Ya sas, ti kánete?
Hello. Hello, how are you?
2
Συγγνώμη. Συγγνώμη, κάθεστε στη θέση μου.
Signómi. Signómi, kátheste sti thési mou.
Excuse me. Excuse me, you are sitting on my seat.
```

Each card entry must contain exactly 4 lines:
1. Card number
2. Greek text (or any other "foreign" text, like Math or Cobol, which is all Greek to most of the human beings)
3. Transcription in Latin alphabet (or anything else you want to display as tooltip when hovering over card)
4. English translation (or anything else you want to display on clicking the card)

## Usage

0. Open [**langcards.html**](https://alexeyanischenko.github.io/LangCards/langcards.html) in your browser.
1. Click "Upload Dictionary File" to select your vocabulary (deck) file. You will need a deck file for that, check the .txt examples in this repository, like [this one](https://alexeyanischenko.github.io/LangCards/common-1100-greek-sentences.txt). You can also specify the deck file in URL param [like that](https://alexeyanischenko.github.io/LangCards/langcards.html?url=https://alexeyanischenko.github.io/LangCards/common-1100-greek-sentences.txt).
2. The application will parse the file and display the number of cards loaded (expand parsing details to check for errors).
3. Use the checkbox to toggle between Greek-only and mixed modes.
4. Click "Next Card" to get a new random card.
5. Click on the card to reveal its translation.
6. Hover over Greek text to see its transcription.
7. Optionally export the currently loaded deck, embedding it to html file.

## Error Handling

The application includes robust error handling for file parsing:
- Validates card number format
- Checks for missing or empty fields
- Attempts to resync on format errors
- Provides detailed parsing information through the debug view
