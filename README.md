# LangCards

A lightweight, browser-based flashcard application for learning foreign language vocabulary, initially created to learn Greek. 
Built with vanilla JavaScript and CSS, this single-page application runs entirely in the browser with no server requirements.

## Features

- **File Upload**: Import vocabulary lists from text files
- **Smart Parsing**: Robust parsing of vocabulary files with detailed error reporting
- **Dark Mode**: Toggle between light and dark themes
- **Study Modes**:
  - Greek-only mode (show Greek first, click to reveal English)
  - Mixed mode (randomly shows either Greek or English first)
- **Transcription Support**: Hover over Greek text to see Latin alphabet transcription
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

Each card entry must contain exactly 4 lines:
1. Card number
2. Greek text
3. Transcription in Latin alphabet
4. English translation

## Usage

0. Open langcards.html in your browser
1. Click "Upload Dictionary File" to select your vocabulary file
2. The application will parse the file and display the number of cards loaded
3. Use the checkbox to toggle between Greek-only and mixed modes
4. Click "Next Card" to get a new random card
5. Click on the card to reveal its translation
6. Hover over Greek text to see its transcription

## Error Handling

The application includes robust error handling for file parsing:
- Validates card number format
- Checks for missing or empty fields
- Attempts to resync on format errors
- Provides detailed parsing information through the debug view
