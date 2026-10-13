# Deck generators

Two of the bundled decks are not written by hand — they are generated, and the `.txt` files
in the parent directory are build output. This is the source.

| Deck | Generator | Output |
|---|---|---|
| **Noun phrases** (3,000) | `gen.py` | `../greek-articles-adjectives-nouns-3000.txt` |
| **Pronouns** (3,000) | `pbuild.py` | `../greek-pronouns-3000.txt` |

Both are deterministic: regenerating reproduces the committed file byte for byte. Nothing
here needs installing — plain Python 3, no dependencies.

```bash
cd tools

python test_lex.py            # 86 gold noun paradigms
python test_verbs.py          # 89 gold verb paradigms, plus δικός and the final-ν rule

python gen.py     ../greek-articles-adjectives-nouns-3000.txt
python pbuild.py  ../greek-pronouns-3000.txt

python validate.py  ../greek-articles-adjectives-nouns-3000.txt
python klikcheck.py ../greek-articles-adjectives-nouns-3000.txt
python pvalidate.py ../greek-pronouns-3000.txt
python pklik.py     ../greek-pronouns-3000.txt

cd .. && python build-langcards.py      # re-embed everything into langcards.html
```

Run the gold tests before trusting a change to the inflection rules, and the validator and the
KLIK check before committing a regenerated deck. **A deck that fails either check must not
ship**: the first means a card cannot be solved from its own prompt, the second that a card
uses a word outside the exam list.

## The two invariants

Everything here exists to hold two properties, and both are checked over all 3,000 cards of
each deck rather than spot-checked.

**Every card re-derives exactly from its own prompt.** `validate.py` and `pvalidate.py` throw
the answer away, read only what the learner is given — the bracketed hint, plus the case named
in the explanation — rebuild the missing words from the paradigm tables, and require the result
to equal the answer character for character. A card that fails this is one a learner could not
solve, however good it looks.

**Every Greek word traces back to a KLIK A2 headword.** `klikcheck.py` and `pklik.py` check
three things: that every noun, adjective and verb the deck inflects is a KLIK headword; that
every word hard-coded into a sentence frame is one too, or an inflected form of one named
explicitly in the script; and that every Greek token of every finished card is one of those, an
article, a pronoun, or a form the deck itself generated. A word with nowhere to trace to is an
error, not a warning.

## Files

### Shared

| File | What it is |
|---|---|
| `greeklex.py` | The inflection engine: syllabification, accent placement, the 11 noun classes, `-ος/-η/-ο` adjectives, the articles and the final-ν rule. |
| `test_lex.py` | 86 hand-written gold noun paradigms (~460 forms), plus adjective and final-ν cases. |
| `data.py` | The raw lexicon: 511 nouns as `(greek, class, tag, en_sg, en_pl)` and 148 adjectives. |
| `data2.py` | The refined lexicon: finer semantic tags, the mass-noun and blocked-pair sets, and the per-adjective noun whitelists that keep pairings meaningful. |

`greeklex.py` deliberately omits the **genitive plural** of the `-ας`, `-ης`, `-α` and `-η`
classes. There it is lexical rather than rule-governed, so the generators skip those
combinations instead of guessing. `decline_noun` returns a dict, and a missing key means
*do not use this form*, not *derive it yourself*.

### Noun phrases

| File | What it is |
|---|---|
| `gen.py` | 66 sentence frames and the noun-balanced selection that fills them. |
| `validate.py` | The re-derivation check. |
| `klikcheck.py` | The vocabulary check. |

### Pronouns

| File | What it is |
|---|---|
| `pron.py` | The pronoun paradigms — strong and weak, `δικός`, the demonstrative — plus present-tense conjugation for groups A / B1 / B2 and a table for the irregulars. |
| `frames.py` | The sentence frames, one table per job the pronoun can be doing. |
| `groups.py` | Curated noun pools. A tag like `obj` holds both a suitcase and a plug socket; only one of them can be taken to work or owned, so each slot gets the pool that makes sense in it. |
| `pgen.py` | Enumerates every candidate card. |
| `pbuild.py` | Picks the final 3,000 against the case and number targets and writes the file. |
| `pvalidate.py` | The re-derivation check. |
| `pklik.py` | The vocabulary check. |
| `test_verbs.py` | 89 gold present-tense paradigms, the `δικός` paradigm, and the final-ν rule on the clitic. |

Frames carry an animacy mark. One about people never asks for a neuter pronoun — *the waiter
asks it* is not a sentence — and one about things runs in the third person only and glosses
every gender as English *it*, which is what `αυτός`/`αυτή`/`αυτό` mean of an object.

The quotas in `pbuild.py` are the deck's shape: 1,200 nominative / 1,600 accusative / 200
genitive, and 1,500 singular / 1,500 plural counted on the referent. Each family's quota must
be **even**, because it is split evenly between singular and plural, and must not exceed what
`pgen.py` actually produced — `pbuild.py` prints a warning line naming the family when it falls
short, and the totals then miss. Change the quotas and re-run; the warning tells you what to
adjust.

## Changing the decks

The failure mode is not a crash, it is a card that is grammatically perfect and says something
nobody would say — *a technological column*, *the pure salary*, *I am drinking a cheap dish*,
*the waiter asks it*. Both generators grew their whitelists by auditing output, so:

1. Make the change.
2. Regenerate, then **read a sample across every family**, not just the first few cards. The
   checkers verify form, not sense; only reading catches a bad pairing.
3. Run the gold tests, the validator and the KLIK check.
4. Rebuild `langcards.html` and commit the deck, the generator change and the built file
   together.

If a change to `greeklex.py` breaks a gold test, the test is usually right. Twice it was not —
`την ξένη` is correct because ξ is a double consonant — but assume the engine is wrong first.
