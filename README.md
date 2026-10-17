# Scrabble Math

Scrabble scoring honesty. The bingo bonus outscores most words. Scrabble Math runs the game's published scoring rules exactly: letter values, premium squares, the 50-point bingo, and what the bag still holds.

## What it computes

- **The word truth** - a word with one optional letter premium and one word premium: QUIZ with the Z doubled and the whole word tripled scores 96, and the tiles only make 32.
- **The bingo truth** - all 7 tiles at once: JAZZILY is 35 on the tiles plus 50 for the bingo, and the bonus outscores the word.
- **The bag truth** - with 40 tiles left and 3 E's unseen, the next tile is an E 7.5% of the time.

## Boundary

Rules arithmetic only. Letter values, premium squares, and the bingo bonus are the game's published scoring rules, run exactly. Scrabble Math never judges whether a word is legal or a play is smart - the dictionary and the table decide those.

## Files

- `index.html` - landing page with the honesty pitch and the boundary.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic, shared by the app and the tests.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (13 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/scrabblemath/
Repo: https://github.com/iLanis-agent/scrabblemath
