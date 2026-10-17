#!/usr/bin/env python3
# Scrabble Math oracle - mirrors engine.js float-for-float.
import json, math

LETTER_VALUES = dict(A=1,B=3,C=3,D=2,E=1,F=4,G=2,H=4,I=1,J=8,K=5,L=1,M=3,
                     N=1,O=1,P=3,Q=10,R=1,S=1,T=1,U=1,V=4,W=4,X=8,Y=4,Z=10)
BAG_DIST = dict(A=9,B=2,C=2,D=4,E=12,F=2,G=3,H=2,I=9,J=1,K=1,L=4,M=2,
                N=6,O=8,P=2,Q=1,R=6,S=4,T=6,U=4,V=2,W=2,X=1,Y=2,Z=1)
VOWEL_SOUND = "AEFHILMNORSX"

def _fixed1(x):
    t = math.floor(x * 10 + 0.5)
    return f"{t // 10}.{t % 10}"

def _mult_word(n):
    return "doubled" if n == 2 else "tripled"

def _clean(word):
    w = str(word).upper()
    if not w.isalpha() or not w.isascii():
        raise ValueError("letters only")
    return w

def word_truth(word, pos, letter_mult, word_mult):
    w = _clean(word)
    if letter_mult < 1 or letter_mult > 3:
        raise ValueError("the letter premium must be 1, 2, or 3")
    if word_mult < 1 or word_mult > 3:
        raise ValueError("the word premium must be 1, 2, or 3")
    if letter_mult > 1 and (pos < 1 or pos > len(w)):
        raise ValueError("the letter position must be inside the word")
    base = 0
    for i, ch in enumerate(w):
        v = LETTER_VALUES[ch]
        if letter_mult > 1 and i == pos - 1:
            v *= letter_mult
        base += v
    if word_mult > 1:
        score = base * word_mult
        desc = f"{base} on the tiles"
        if letter_mult > 1:
            desc += f" with the {w[pos-1]} {_mult_word(letter_mult)}"
        return (f"{w} scores {score} - {desc}, times {word_mult} for the "
                f"{'double' if word_mult == 2 else 'triple'} word.")
    if letter_mult > 1:
        return (f"{w} scores {base} - the tiles with the {w[pos-1]} "
                f"{_mult_word(letter_mult)}, no word premium.")
    return f"{w} scores {base} - plain squares, just the tiles."

def bingo_truth(word):
    w = _clean(word)
    if len(w) != 7:
        raise ValueError(f"a bingo needs all 7 tiles - {w} has {len(w)}")
    total_letters = sum(LETTER_VALUES[ch] for ch in w)
    total = total_letters + 50
    quip = ("the bonus outscores the word" if total_letters < 50
            else "the word outscores its own bonus" if total_letters > 50
            else "the bonus matches the word exactly")
    return (f"{w} is {total_letters} on the tiles plus 50 for the bingo - {total} "
            f"before any premium squares, and {quip}.")

def bag_truth(letter, copies_left, tiles_left):
    L = str(letter).upper()
    if len(L) != 1 or not L.isalpha():
        raise ValueError("one letter only")
    if not math.isfinite(copies_left) or copies_left < 0:
        raise ValueError("copies left must be zero or more")
    if copies_left > BAG_DIST[L]:
        raise ValueError(f"the bag only ever holds {BAG_DIST[L]} {L}"
                         + (" tile" if BAG_DIST[L] == 1 else " tiles"))
    if not math.isfinite(tiles_left) or tiles_left <= 0:
        raise ValueError("the bag must still have tiles")
    if copies_left > tiles_left:
        raise ValueError("there cannot be more of a letter than tiles")
    if copies_left == 0:
        return f"There are no {L}'s left in the bag - stop waiting on it."
    pct = copies_left / tiles_left * 100
    art = "an" if L in VOWEL_SOUND else "a"
    plural = "" if copies_left == 1 else "'s"
    return (f"With {tiles_left} tiles left and {copies_left} {L}{plural} unseen, "
            f"the next tile is {art} {L} {_fixed1(pct)}% of the time - "
            f"count the board before you wait on a letter.")

CASES = [
    ("wordTruth", ("QUIZ", 4, 2, 3)),
    ("wordTruth", ("QUIZ", 0, 1, 1)),
    ("wordTruth", ("hello", 2, 3, 1)),
    ("wordTruth", ("ZOO", 1, 2, 2)),
    ("wordTruth", ("QU1Z", 0, 1, 1)),
    ("wordTruth", ("QUIZ", 5, 2, 1)),
    ("bingoTruth", ("JAZZILY",)),
    ("bingoTruth", ("TRAINED",)),
    ("bingoTruth", ("QUIZ",)),
    ("bagTruth", ("E", 3, 40)),
    ("bagTruth", ("Z", 1, 50)),
    ("bagTruth", ("E", 0, 40)),
    ("bagTruth", ("J", 2, 30)),
]

FNS = {"wordTruth": word_truth, "bingoTruth": bingo_truth, "bagTruth": bag_truth}

out = []
for name, args in CASES:
    try:
        expected = FNS[name](*args)
    except ValueError as e:
        expected = "ERR:" + str(e)
    out.append({"fn": name, "args": list(args), "expected": expected})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, indent=2) + "\n")
print(f"{len(out)} cases written")
