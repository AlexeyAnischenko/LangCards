# -*- coding: utf-8 -*-
"""Build langcards.html from langcards.template.html, embedding the dictionaries
raw-deflated and base64-encoded, inflated in the browser via DecompressionStream.

langcards.html is GENERATED - edit langcards.template.html and rerun this script."""
import io, zlib, base64, textwrap

SRC = 'langcards.template.html'
DST = 'langcards.html'

DICTS = [
    ('a2',      'a2-exam-400-greek-sentences.txt', u'A2 exam — Greek sentences'),
    ('common',  'common-1100-greek-sentences.txt', u'Common — Greek sentences'),
    ('travel',  'travel-300-greek-sentences.txt',  u'Travel — Greek sentences'),
    # fill-in-the-blank deck: field 2 holds the completed sentence, not a transcription
    ('grammar', 'greek-endings-articles-prepositions-conjugations-1000.txt',
                u'Grammar — articles, prepositions, verbs'),
    # fill-in-the-blank deck: field 2 holds the completed sentence
    ('phrases', 'greek-articles-adjectives-nouns-3000.txt',
                u'Noun phrases — article + adjective + noun'),
    ('klik',    'klik-a2-vocabulary.txt', u'KLIK A2 — the exam word list'),
    # the words both KLIK books use 5+ times: the backbone, against the 1,509
    # entries the two books print exactly once
    ('klik5',   'greek-a1-a2-klik-5timesplus.txt',
                u'Greek A1-A2-Klik-5timesplus'),
    # the oral interview for the article 111B(2) fast-track naturalisation
    # (form M127): the officer's question on the front, a model A2 answer behind
    ('interview', 'greek-cyprus-citizenship-interview.txt',
                u'Cyprus citizenship interview — questions & answers'),
    # every adjective the two books and the exams use, fully declined
    ('adj',     'greek-a2-adjectives.txt',
                u'A2 adjectives — full declension'),
]

s = io.open(SRC, encoding='utf-8').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, 'anchor not unique (%d): %r' % (s.count(old), old[:70])
    s = s.replace(old, new)


# ---------- CSS for the dictionary picker ----------
rep("""    #file-input {
      display: none;
    }""",
    """    .dict-select {
      background: var(--card-hover);
      color: var(--text-color);
      border: 1px solid var(--text-muted);
      border-radius: 0.375rem;
      padding: 0.5rem 0.75rem;
      font-size: 0.875rem;
      font-family: inherit;
      cursor: pointer;
      max-width: 22rem;
    }

    .dict-select option {
      background: var(--card-bg);
      color: var(--text-color);
    }

    #file-input {
      display: none;
    }""")

# ---------- the picker, right next to the file selector ----------
options = '\n'.join(
    '            <option value="%s">%s</option>' % (key, label)
    for key, _path, label in DICTS
)
rep("""        </div>
        <div class="file-info">""",
    u"""        </div>
        <select class="dict-select" id="dict-select" title="Choose a built-in dictionary">
%s
            <option value="">Uploaded file…</option>
        </select>
        <div class="file-info">""" % options)

# ---------- embedded dictionary payloads (raw deflate + base64) ----------
payloads = []
raw_total = enc_total = 0
for key, path, label in DICTS:
    text = io.open(path, encoding='utf-8-sig').read().replace('\r\n', '\n').strip().encode('utf-8')
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)  # -15 == raw deflate, no header
    blob = base64.b64encode(compressor.compress(text) + compressor.flush()).decode('ascii')
    raw_total += len(text)
    enc_total += len(blob)
    payloads.append(
        '  <script type="text/plain" id="dict-%s" data-label="%s">\n%s\n  </script>'
        % (key, label, '\n'.join(textwrap.wrap(blob, 120)))
    )

rep("""  <script>
    // State""",
    '\n'.join(payloads) + """

  <script>
    // State""")

# ---------- reset the picker when a file is uploaded ----------
rep("""      fileNameDisplay.textContent = file.name;
      statusDisplay.textContent = 'Reading file...';""",
    """      fileNameDisplay.textContent = file.name;
      statusDisplay.textContent = 'Reading file...';
      dictSelect.value = '';
      localStorage.removeItem('dictionary');""")

# ---------- loader + wiring, appended at the end of the script ----------
rep("""    greekOnlyCheckbox.addEventListener('change', function() {
      isGreekOnly = this.checked;
      showGreek = true;
      showTranslation = false;
      updateCardDisplay();
    });""",
    """    greekOnlyCheckbox.addEventListener('change', function() {
      isGreekOnly = this.checked;
      showGreek = true;
      showTranslation = false;
      updateCardDisplay();
    });

    // Built-in dictionaries, embedded in this file as raw deflate + base64.
    const dictionaryCache = new Map();

    async function inflateDictionary(base64) {
      const binary = atob(base64);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
      }
      const stream = new Blob([bytes]).stream()
        .pipeThrough(new DecompressionStream('deflate-raw'));
      return (await new Response(stream).text()).trim();
    }

    async function loadBuiltinDictionary(key) {
      const payload = document.getElementById('dict-' + key);
      if (!payload) return;

      // the dropdown already names the deck - repeating it here just overflows the row
      fileNameDisplay.textContent = '';

      let text = dictionaryCache.get(key);
      if (text === undefined) {
        statusDisplay.textContent = 'Unpacking...';
        try {
          text = await inflateDictionary(payload.textContent);
        } catch (error) {
          statusDisplay.textContent = 'Could not unpack dictionary: ' + error.message;
          return;
        }
        dictionaryCache.set(key, text);
      }

      const newCards = parseVocabularyData(text);
      if (newCards.length > 0) {
        cards = newCards;
        statusDisplay.textContent = `${cards.length} cards loaded`;
        flashcardUI.style.display = 'block';
        totalCardsElement.textContent = cards.length;
        displayRandomCard();
      } else {
        cards = [];
        currentCardIndex = -1;
        flashcardUI.style.display = 'none';
        statusDisplay.textContent = 'No valid cards found';
      }
    }

    dictSelect.addEventListener('change', function() {
      if (!this.value) return;
      localStorage.setItem('dictionary', this.value);
      loadBuiltinDictionary(this.value);
    });

    const savedDictionary = localStorage.getItem('dictionary');
    if (savedDictionary && document.getElementById('dict-' + savedDictionary)) {
      dictSelect.value = savedDictionary;
    }
    if (dictSelect.value) {
      loadBuiltinDictionary(dictSelect.value);
    }""")

# ---------- DOM handle for the picker ----------
rep("""    const helpTooltip = document.querySelector('.help-tooltip');""",
    """    const helpTooltip = document.querySelector('.help-tooltip');
    const dictSelect = document.getElementById('dict-select');""")

BANNER = u"""<!--
  GENERATED FILE - do not edit.
  Source: %s plus the *-greek-sentences.txt dictionaries.
  Rebuild with: python build-langcards.py
-->
""" % SRC

marker = u'<!DOCTYPE html>\n'
assert s.count(marker) == 1
s = s.replace(marker, marker + BANNER, 1)

io.open(DST, 'w', encoding='utf-8', newline='').write(s)
print('wrote %s (%.1f KB)' % (DST, len(s.encode('utf-8')) / 1024.0))
print('  dictionaries: %.1f KB raw -> %.1f KB embedded (%.0f%% smaller)'
      % (raw_total / 1024.0, enc_total / 1024.0, 100 - 100.0 * enc_total / raw_total))
