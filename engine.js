// Scrabble Math engine - published scoring rules, run exactly.
// Mirrored float-for-float by oracle.py; keep the op order identical.

var LETTER_VALUES = {A:1,B:3,C:3,D:2,E:1,F:4,G:2,H:4,I:1,J:8,K:5,L:1,M:3,
  N:1,O:1,P:3,Q:10,R:1,S:1,T:1,U:1,V:4,W:4,X:8,Y:4,Z:10};
var BAG_DIST = {A:9,B:2,C:2,D:4,E:12,F:2,G:3,H:2,I:9,J:1,K:1,L:4,M:2,
  N:6,O:8,P:2,Q:1,R:6,S:4,T:6,U:4,V:2,W:2,X:1,Y:2,Z:1};
var VOWEL_SOUND = "AEFHILMNORSX";

function _fixed1(x) {
  var t = Math.floor(x * 10 + 0.5);
  return Math.floor(t / 10) + "." + (t % 10);
}

function _multWord(n) { return n === 2 ? "doubled" : "tripled"; }

function _clean(word) {
  var w = String(word).toUpperCase();
  if (!/^[A-Z]+$/.test(w)) throw new Error("letters only");
  return w;
}

// The word truth: one word, one optional letter premium, one word premium.
function wordTruth(word, pos, letterMult, wordMult) {
  var w = _clean(word);
  if (letterMult < 1 || letterMult > 3) throw new Error("the letter premium must be 1, 2, or 3");
  if (wordMult < 1 || wordMult > 3) throw new Error("the word premium must be 1, 2, or 3");
  if (letterMult > 1 && (pos < 1 || pos > w.length)) {
    throw new Error("the letter position must be inside the word");
  }
  var base = 0;
  for (var i = 0; i < w.length; i++) {
    var v = LETTER_VALUES[w[i]];
    if (letterMult > 1 && i === pos - 1) v *= letterMult;
    base += v;
  }
  if (wordMult > 1) {
    var score = base * wordMult;
    var desc = base + " on the tiles";
    if (letterMult > 1) desc += " with the " + w[pos - 1] + " " + _multWord(letterMult);
    return w + " scores " + score + " - " + desc + ", times " + wordMult +
      " for the " + (wordMult === 2 ? "double" : "triple") + " word.";
  }
  if (letterMult > 1) {
    return w + " scores " + base + " - the tiles with the " + w[pos - 1] + " " +
      _multWord(letterMult) + ", no word premium.";
  }
  return w + " scores " + base + " - plain squares, just the tiles.";
}

// The bingo truth: all 7 tiles at once is worth 50 on top.
function bingoTruth(word) {
  var w = _clean(word);
  if (w.length !== 7) throw new Error("a bingo needs all 7 tiles - " + w + " has " + w.length);
  var sum = 0;
  for (var i = 0; i < w.length; i++) sum += LETTER_VALUES[w[i]];
  var total = sum + 50;
  var quip = sum < 50 ? "the bonus outscores the word"
    : sum > 50 ? "the word outscores its own bonus"
    : "the bonus matches the word exactly";
  return w + " is " + sum + " on the tiles plus 50 for the bingo - " + total +
    " before any premium squares, and " + quip + ".";
}

// The bag truth: what the next tile probably is, from counts you tracked.
function bagTruth(letter, copiesLeft, tilesLeft) {
  var L = String(letter).toUpperCase();
  if (!/^[A-Z]$/.test(L)) throw new Error("one letter only");
  if (!isFinite(copiesLeft) || copiesLeft < 0) throw new Error("copies left must be zero or more");
  if (copiesLeft > BAG_DIST[L]) {
    throw new Error("the bag only ever holds " + BAG_DIST[L] + " " + L + (BAG_DIST[L] === 1 ? " tile" : " tiles"));
  }
  if (!isFinite(tilesLeft) || tilesLeft <= 0) throw new Error("the bag must still have tiles");
  if (copiesLeft > tilesLeft) throw new Error("there cannot be more of a letter than tiles");
  if (copiesLeft === 0) {
    return "There are no " + L + "'s left in the bag - stop waiting on it.";
  }
  var pct = copiesLeft / tilesLeft * 100;
  var art = VOWEL_SOUND.indexOf(L) >= 0 ? "an" : "a";
  return "With " + tilesLeft + " tiles left and " + copiesLeft + " " + L +
    (copiesLeft === 1 ? "" : "'s") + " unseen, the next tile is " + art + " " + L + " " +
    _fixed1(pct) + "% of the time - count the board before you wait on a letter.";
}
