# Strings and Encoding

> A string is an array you are not allowed to write into, over an alphabet small
> enough that you can count it — and most string problems are decided by which
> of those two facts you notice first.

## When you reach for it

This is the second-largest topic in the bank: 1,206 of the problems here touch
it, behind only [[arrays]]. That size is a warning, not a recommendation. "Use
strings" is not a technique. So this chapter is about the one shape that shows up
underneath a huge fraction of those problems, and about the cost model that
decides whether your answer is fast or accidentally quadratic.

The shape is: **one left-to-right pass that cuts the input into maximal blocks
and emits a piece per block.** You reach for it when the statement talks about
*consecutive* things — a run of equal characters, a group, a streak, a segment
between delimiters — and wants a string or a count back.

The bank's canonical family is run-length compression, and it appears with every
possible variation of the rules:

- **Encode every run** — *Run-Length Encode a String*, *Run-Length String
  Compression*, *String Compression Problem*.
- **Encode, but only keep it if it helped** — *Basic String Compression with
  Length Guard*, which returns the original unless the code is strictly shorter.
- **Encode something that is not a character run** — *Compress Consecutive
  Integer Ranges* runs the same scanner over sorted integers with "consecutive"
  in place of "equal"; *URL / Path Segment Compression Part 1* abbreviates each
  dot-separated segment to first + count + last.
- **Measure runs instead of emitting them** — *Longest Same-Character Substring*,
  *Longest Contiguous Character Run*, *Rightmost Longest Character Run*.

The same scanner, with the emit step changed, solves all of them.

It is the wrong tool the moment the question stops being about adjacency.
*Better Compression* looks like run-length encoding and is not: it totals each
character across the whole string and emits them alphabetically, so `a3c9b2c1`
becomes `a3b2c10`. Runs are irrelevant there; you want a count per letter
([[frequency-counting]]). If the question is "where does this pattern occur",
that is [[string-matching]]. If there are nested brackets or a grammar —
*Expand Given String* — that is [[parsing]] and a [[stack]]. If you are asked
about a window of bounded badness, like *Get Special Substring (MTS)*, that is
[[sliding-window]]. If two strings have to be aligned against each other, that is
[[dp-strings]].

And one honest anti-signal that catches good candidates: **substring is not
subsequence**. *Check a Repeated String as a Subsequence* and *DFS Subsequences
of a String* say subsequence and mean it — characters keep their order but need
not be adjacent. A run scanner answers nothing there. Read that word twice before
you write a line.

## The idea

A string is an array of code units that you cannot write into, so every string
algorithm is a **reader** and a **writer**: one cursor that walks the input
exactly once, and a list of pieces that becomes the output exactly once, at the
join.

The reader almost never wants characters. It wants **blocks**. So carry two
indices: `i`, the first position of the block you are currently on, and `j`,
which runs forward while the block continues. When `j` stops, the block is
`s[i:j]`, you emit one piece for it, and you set `i = j`. That last assignment is
the whole performance argument: `i` jumps over everything `j` looked at, so the
two nested loops together examine each position once, not `n` times each.

<svg viewBox="0 0 640 200" role="img" aria-label="a string cut into maximal runs, with cursors i and j bracketing the current run and an output buffer below">
  <g>
    <text x="160" y="16" text-anchor="middle">i</text>
    <text x="360" y="16" text-anchor="middle">j</text>
    <line x1="160" y1="22" x2="160" y2="42"/>
    <line x1="360" y1="22" x2="360" y2="42"/>
    <rect class="fill" x="40" y="45" width="40" height="40" rx="3"/>
    <rect class="fill" x="80" y="45" width="40" height="40" rx="3"/>
    <rect class="fill" x="120" y="45" width="40" height="40" rx="3"/>
    <rect x="160" y="45" width="40" height="40" rx="3"/>
    <rect x="200" y="45" width="40" height="40" rx="3"/>
    <rect x="240" y="45" width="40" height="40" rx="3"/>
    <rect x="280" y="45" width="40" height="40" rx="3"/>
    <rect x="320" y="45" width="40" height="40" rx="3"/>
    <rect x="360" y="45" width="40" height="40" rx="3"/>
    <rect x="400" y="45" width="40" height="40" rx="3"/>
    <rect x="440" y="45" width="40" height="40" rx="3"/>
    <text x="60" y="72" text-anchor="middle">a</text>
    <text x="100" y="72" text-anchor="middle">a</text>
    <text x="140" y="72" text-anchor="middle">b</text>
    <text x="180" y="72" text-anchor="middle">c</text>
    <text x="220" y="72" text-anchor="middle">c</text>
    <text x="260" y="72" text-anchor="middle">c</text>
    <text x="300" y="72" text-anchor="middle">c</text>
    <text x="340" y="72" text-anchor="middle">c</text>
    <text x="380" y="72" text-anchor="middle">a</text>
    <text x="420" y="72" text-anchor="middle">a</text>
    <text x="460" y="72" text-anchor="middle">a</text>
    <line x1="160" y1="95" x2="360" y2="95"/>
    <line x1="160" y1="95" x2="160" y2="88"/>
    <line x1="360" y1="95" x2="360" y2="88"/>
    <text x="260" y="112" text-anchor="middle">the current run: c five times</text>
    <text x="100" y="112" text-anchor="middle">already emitted</text>
    <rect x="40" y="130" width="30" height="34" rx="3"/>
    <rect x="70" y="130" width="30" height="34" rx="3"/>
    <rect x="100" y="130" width="30" height="34" rx="3"/>
    <rect x="130" y="130" width="30" height="34" rx="3"/>
    <text x="55" y="153" text-anchor="middle">a</text>
    <text x="85" y="153" text-anchor="middle">2</text>
    <text x="115" y="153" text-anchor="middle">b</text>
    <text x="145" y="153" text-anchor="middle">1</text>
    <text x="330" y="153" text-anchor="middle">out: a list of pieces, joined once at the end</text>
  </g>
</svg>

Written down, that is six lines, and the rest of this chapter is those six lines
wearing different hats:

```python
i, n = 0, len(s)
while i < n:
    j = i + 1
    while j < n and s[j] == s[i]:
        j += 1
    emit(s[i], j - i)       # one piece per block
    i = j                   # jump; never re-read what j already saw
```

## Worked by hand

Take `s = "aabcccccaaa"`, length 11, and produce the always-count encoding: each
run becomes its character followed by its length in base 10.

| step | i | j on exit | run | piece | out so far | length |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | `a` × 2 | `a2` | `a2` | 2 |
| 2 | 2 | 3 | `b` × 1 | `b1` | `a2b1` | 4 |
| 3 | 3 | 8 | `c` × 5 | `c5` | `a2b1c5` | 6 |
| 4 | 8 | 11 | `a` × 3 | `a3` | `a2b1c5a3` | 8 |
| — | 11 | — | — | — | stop | 8 < 11 |

Now the same table for `s = "abc"`, where compression is a bad idea:

| step | i | j on exit | run | piece | out so far | length |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | `a` × 1 | `a1` | `a1` | 2 |
| 2 | 1 | 2 | `b` × 1 | `b1` | `a1b1` | 4 |
| 3 | 2 | 3 | `c` × 1 | `c1` | `a1b1c1` | 6 |

Six characters out of three in. *Basic String Compression with Length Guard*
exists precisely because of this table: it says return the original unless the
encoding is strictly shorter.

Four things the trace shows that reading the code does not.

**`i` jumps to `j`, so the inner loop is not a second pass.** In step 3 the inner
loop advanced `j` four times; those four positions are never examined again,
because `i` became 8. Add up the inner-loop work across all four steps and you
get 11 — one visit per character. That is the counting argument the next-but-one
section turns into a complexity bound.

**The letter `a` owns two runs.** Steps 1 and 4 both emit `a`, and the encoding
contains `a` twice. Run-length encoding sees *adjacency*, never *totals*. This is
exactly the line between *Run-Length String Compression* and *Better
Compression*, whose whole job is to merge the `c9` and the `c1` in `a3c9b2c1`
into a single `c10`. Two problems, near-identical output alphabets, opposite
semantics.

**Output length is driven by the number of runs, not by their lengths.** Each run
contributes one character plus its digit count, so a run of five and a run of two
cost the same two characters. Compression wins when there are *few* runs, and
"few runs" is the property to look for in the statement.

**The guard can be decided early.** The running output length is non-decreasing,
so once it reaches `len(s)` no future run can rescue it. In the `"abc"` trace
that happens at step 2, with a third of the string still unread. You never need
to build the whole encoding to answer the guarded version.

## Why it is correct

There are two separate claims hiding in "the code run-length encodes the string",
and they need separate arguments. First, the scanner really does cut the string
into its maximal runs. Second, the encoding can be decoded — which is true only
under a condition the statements rarely spell out.

:::proof The scanner produces exactly the maximal runs, and the always-count encoding is invertible
**Definitions.** Let `s` have length `n`. Define the relation `t ≈ t+1` on
positions when `s[t] = s[t+1]`, and let `~` be the equivalence it generates. The
classes of `~` are intervals of positions carrying a single character, maximal
under extension, and they partition `[0, n)`. Call them the **runs** of `s`. An
interval `[a, b)` is a run iff `s[a] = … = s[b-1]`, and (`a = 0` or
`s[a-1] ≠ s[a]`), and (`b = n` or `s[b] ≠ s[b-1]`).

**Inner loop.** Enter with `i < n` and `j = i + 1`, and run
`while j < n and s[j] == s[i]: j += 1`.

*Invariant:* at every test, `s[t] = s[i]` for all `t` in `[i, j)`.
*Base:* `j = i + 1`, so the interval is `{i}` and the claim is `s[i] = s[i]`.
*Step:* if the test passes then `s[j] = s[i]`, so the claim extends to
`[i, j + 1)`.
*Termination:* `j` strictly increases and is bounded above by `n`.

On exit either `j = n` or `s[j] ≠ s[i]`, and no `j'` in `(i, j)` had
`s[j'] ≠ s[i]` — the loop would have stopped there. So `j` is the least index
above `i` that breaks the run, and `[i, j)` is a run of `s` **provided `i` starts
one**.

**Outer loop.** Let `P(i)` be: `out` holds the pieces of all runs contained in
`[0, i)`, in left-to-right order; those runs exactly cover `[0, i)`; and `i = 0`
or `i = n` or `s[i] ≠ s[i-1]`.

*Base:* `i = 0`, `out` empty, the empty union covers `[0, 0)`. `P(0)` holds.
*Step:* assume `P(i)` and `i < n`. Then `i = 0` or `s[i] ≠ s[i-1]`, so `i` starts
a run, and by the inner-loop claim `[i, j)` is that run. Appending its piece and
setting `i := j` restores the first two parts; the third holds because on exit
`j = n` or `s[j] ≠ s[i] = s[j-1]`. So `P(j)`.
*Termination:* `j > i`, so `i` strictly increases inside `[0, n]`, and the loop
exits with `i = n`.

At exit `P(n)` says `out` lists the pieces of every run of `s`, in order. That is
the first claim.

**Invertibility.** Assume the alphabet `Σ` contains no decimal digit. Let `E(s)`
be the concatenation of `c · dec(k)` over the runs, and let `D` be the decoder
that repeatedly reads one character, then the longest following block of digits,
and appends that character repeated that many times.

Induct on the number of runs `R`.
*Base:* `R = 0` means `s` is empty, `E(s)` is empty, and `D` returns the empty
string.
*Step:* let the first run be `c` repeated `k` times and let `s'` be the rest, with
`R - 1` runs. Then `E(s) = c · dec(k) · E(s')`. `D` reads `c`, correctly, since
`E(s)` begins at a run head. It then takes the longest digit block starting after
`c`: every character of `dec(k)` is a digit, and the character after it is either
absent or the first character of `E(s')`, which is a run head and so lies in `Σ`
and is not a digit. Therefore the block read is exactly `dec(k)`, and `D` emits
`c` repeated `k` times. By the induction hypothesis `D(E(s')) = s'`. Hence
`D(E(s)) = c^k · s' = s`.

Since `D ∘ E` is the identity, `E` is injective: two different strings cannot
share an encoding. ∎
:::

Now name what the proof leaned on, because that list is where the bugs live.

- **The alphabet contains no digits.** Drop this and injectivity dies
  immediately: `E("a1") = "a1" + "11" = "a111"`, and `E` of the letter `a`
  repeated 111 times is also `"a111"`. *Run-Length String Compression*
  (Salesforce) explicitly allows "letters, digits, or symbols", so the encoding
  it asks for is **not** decodable. That is fine — the problem only asks you to
  produce it — but never promise a round trip you have not earned. Real formats
  buy the guarantee back with an escape character or a fixed-width count.
- **Every run is emitted, including the last one.** The outer-loop invariant
  emits inside the loop, once per run. A version that instead emits when the
  character *changes* has `R - 1` change events and `R` runs, and loses the final
  one. This is the single most common bug in this family.
- **The inner loop stops at the first difference.** Maximality is what makes the
  decomposition unique. A scanner that caps run lengths at 9 to keep counts
  single-digit is still decodable — the decoder does not care — but the encoding
  is no longer canonical, so two encodings of the same string now exist and any
  later argument that compares encodings for equality breaks.
- **Counts are written in base 10, digit by digit.** `dec(k)` has
  `⌊log₁₀ k⌋ + 1` characters. Emitting `chr(ord('0') + k)` works up to 9 and then
  silently emits punctuation.
- **Character equality means code-point equality.** In Unicode a user-perceived
  character can be several code points — `e` followed by a combining acute — and
  a run scanner will happily split it, or treat two visually identical strings as
  different. If a statement says "characters" and the input is not ASCII,
  normalise first. All the statements in this bank say ASCII or lowercase
  English, which is why this never bites here and always bites in production.

## What it costs

**Comparisons.** Let the runs have lengths `k₁, …, k_R` with `Σ k_r = n`. For run
`r` the inner loop performs `k_r - 1` successful comparisons and at most one
failing one. Total:

    Σ_r (k_r - 1) + R  =  (n - R) + R  =  n

So at most `n` character comparisons, and at least `n - 1` — one per position
beyond the first, which matches the observation from the trace that each index is
the inner cursor exactly once. The work per comparison is O(1), so the scan is
**Θ(n)**. As a recurrence, peeling the first run gives `T(n) = T(n - k₁) + Θ(k₁)`,
which unrolls to `Θ(n)` regardless of how the runs are distributed.

**Output length.** The always-count form emits `1 + d(k_r)` characters for run
`r`, where `d(k) = ⌊log₁₀ k⌋ + 1`. Since `d(k) ≤ k` for every `k ≥ 1`,

    |E(s)|  =  Σ_r (1 + d(k_r))  ≤  Σ_r (1 + k_r)  =  R + n  ≤  2n

with equality exactly when every run has length 1 — that is, when no two adjacent
characters are equal, as in `"abc"`. So the always-count encoding **never more
than doubles** the input, and doubles it on the worst case.

The omit-one form is sharper. Its cost for a run is `1` when `k = 1` and
`1 + d(k)` otherwise, and `1 + d(k) ≤ k` for every `k ≥ 2` (check `k = 2`:
`1 + 1 = 2`; for `k ≥ 3`, `d(k) ≤ k - 2` since a number with `d` digits is at
least `10^(d-1) ≥ d + 2`). Therefore `|E_omit(s)| ≤ n` **always**. That single
inequality is what makes in-place compression safe, and it is the content of one
of the self-checks below.

Turning it around: a run of length `k` is worth encoding only when
`1 + d(k) < k`, which first happens at `k = 3`. Two-character runs break even,
single characters lose. A string of mostly short runs cannot compress, no matter
how the code is written.

**Space** is Θ(|output|) for the pieces, plus O(1) for the scanner itself. If the
statement hands you a mutable buffer, the omit-one bound above lets you drop the
output entirely.

**The cost people forget** is building the string. Suppose you assemble `m`
characters with `out = out + piece`. Strings are immutable, so each `+` allocates
a fresh string and copies everything: at step `r` it copies the current length.
With `m` pieces of one character each, the total copied is
`1 + 2 + … + m = m(m+1)/2 = Θ(m²)`. Collecting pieces in a list and calling
`"".join` copies each character once: `Θ(m)`. CPython has an in-place resize
optimisation that hides the quadratic behaviour when the left operand has exactly
one reference, which is why the bad version sometimes looks fine on your machine
and times out on the judge — it is an implementation detail, not a language
guarantee, and it vanishes the moment any other name holds the string.

Slicing has the same shape. `s[i:j]` copies `j - i` characters, so `s = s[1:]`
inside a loop, or taking a fresh slice at every position, is `Θ(n²)`. Work with
indices; slice once, at the end.

Finally, string *comparison* is `Θ` of the length, and *hashing* a string is `Θ`
of its length too ([[hash-tables]]). Putting `m` substrings in a set costs the
total number of characters, not `m`. That is why *Detect a Keyword Substring*
bounds "the total keyword length is at most 10^5" rather than the number of
keywords: the total length is the real input size.

## The implementation

```python run
def runs(s):
    """Yield (character, length) for every maximal run of equal characters."""
    i, n = 0, len(s)
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        yield s[i], j - i
        i = j


def rle(s):                    # character, then the decimal length, always
    return "".join(c + str(k) for c, k in runs(s))


def rle_omit_one(s):           # ... unless the run has length one
    return "".join(c + (str(k) if k > 1 else "") for c, k in runs(s))


def rle_guarded(s):            # keep the original unless the code is shorter
    out, total, n = [], 0, len(s)
    for c, k in runs(s):
        piece = c + str(k)
        total += len(piece)
        if total >= n:         # the length only grows; no run can rescue it
            return s
        out.append(piece)
    return "".join(out)


def unrle(e):
    """Inverse of rle, for alphabets that contain no decimal digit."""
    out, i, n = [], 0, len(e)
    while i < n:
        c, i = e[i], i + 1
        j = i
        while j < n and e[j].isdigit():
            j += 1
        out.append(c * int(e[i:j]))
        i = j
    return "".join(out)


s = "aabcccccaaa"
print("input      ", s, " length", len(s))
print("runs       ", list(runs(s)))
print("rle        ", rle(s), " length", len(rle(s)))
print("omit ones  ", rle_omit_one(s))
print("guarded    ", rle_guarded(s), " | on 'abc':", rle_guarded("abc"))
print("collision  ", rle("a1"), "==", rle("a" * 111), " <- digits break the inverse")
assert rle(s) == "a2b1c5a3" and rle_omit_one(s) == "a2bc5a3"
assert rle_guarded("abc") == "abc" and rle_guarded(s) == "a2b1c5a3"
assert rle("") == "" and rle_guarded("") == "" and unrle("") == ""
assert rle("a1") == rle("a" * 111) == "a111"

import random
rng = random.Random(3)
for _ in range(500):
    t = "".join(rng.choice("aab c") for _ in range(rng.randrange(0, 30)))
    assert unrle(rle(t)) == t
    assert len(rle(t)) <= 2 * len(t)
    assert sum(k for _, k in runs(t)) == len(t)
print("500 random digit-free strings: round trip holds, and |rle(s)| <= 2|s|")
```

Three lines carry the weight.

`while j < n and s[j] == s[i]` puts the bounds test **first**, and relies on
`and` short-circuiting. Swap the two and the last run raises `IndexError`, on
every input, which is at least an honest failure; the version that writes
`while j < n and s[j] == s[j - 1]` is correct too but only because `j` starts at
`i + 1`, and it stops being correct the moment someone "simplifies" the
initialisation.

`i = j` is the performance. It is also the reason `runs` can be a generator with
no state beyond two integers: the consumer never needs to look back.

`return "".join(out)` instead of `out += piece`. One join, one pass, one
allocation of the final size. Make this reflexive; the quadratic version is
demonstrated in the traps below.

The guard deserves a second look. `rle_guarded` does not build the encoding and
then measure it — it measures as it goes and bails the moment `total >= n`. That
is a strict improvement, not a micro-optimisation: on an incompressible 100,000
character input it returns after a handful of runs instead of allocating a
200,000 character string first. *Basic String Compression with Length Guard*
allows inputs of that size.

## Variants you will meet

**Omit the count when the run has length one.** *Run-Length String Compression*
(Oracle and Salesforce) and *String Compression Problem* differ from each other
on exactly this rule, and on whether the result must be shorter. Read the bullet
list in the statement, not the title.

**The length guard.** Return the original unless the encoding is strictly
shorter. Watch the word *strictly*: equal length means return the original.

**Compress in place.** The classic follow-up: write the code back into the input
buffer and return the new length. Safe because, as derived above, the omit-one
encoding of a prefix never exceeds that prefix — so the write cursor can never
overtake the read cursor. See [[in-place-rearrangement]].

<svg viewBox="0 0 620 150" role="img" aria-label="one buffer with a write cursor trailing a read cursor, showing the writer never overtakes the reader">
  <g>
    <text x="210" y="18" text-anchor="middle">write</text>
    <text x="380" y="18" text-anchor="middle">read</text>
    <line x1="210" y1="24" x2="210" y2="44"/>
    <line x1="380" y1="24" x2="380" y2="44"/>
    <rect class="fill" x="40" y="46" width="34" height="38" rx="3"/>
    <rect class="fill" x="74" y="46" width="34" height="38" rx="3"/>
    <rect class="fill" x="108" y="46" width="34" height="38" rx="3"/>
    <rect class="fill" x="142" y="46" width="34" height="38" rx="3"/>
    <rect class="fill" x="176" y="46" width="34" height="38" rx="3"/>
    <rect x="210" y="46" width="34" height="38" rx="3"/>
    <rect x="244" y="46" width="34" height="38" rx="3"/>
    <rect x="278" y="46" width="34" height="38" rx="3"/>
    <rect x="312" y="46" width="34" height="38" rx="3"/>
    <rect x="346" y="46" width="34" height="38" rx="3"/>
    <rect x="380" y="46" width="34" height="38" rx="3"/>
    <rect x="414" y="46" width="34" height="38" rx="3"/>
    <rect x="448" y="46" width="34" height="38" rx="3"/>
    <text x="125" y="108" text-anchor="middle">code already written</text>
    <text x="300" y="108" text-anchor="middle">dead zone</text>
    <text x="448" y="108" text-anchor="middle">not yet read</text>
    <text x="300" y="136" text-anchor="middle">write &lt;= read holds after every run, because 1 + digits(k) &lt;= k</text>
  </g>
</svg>

**A different notion of "continues".** Replace `s[j] == s[i]` with any predicate
on consecutive elements and the same scanner cuts the sequence into blocks.
*Compress Consecutive Integer Ranges* sorts, deduplicates, and uses
`next == prev + 1`. *Clean Up Captions*-style problems use "same word", parsers
use "same character class".

**Fixed-shape abbreviation instead of runs.** *URL / Path Segment Compression
Part 1* splits on `/`, then on `.`, and rewrites each piece as first character +
count of removed characters + last character, so `googlecomabc` becomes `g10c`.
Split, map, join — and the count is multi-digit, which is the trap the statement
goes out of its way to spell out.

**Decoding and expansion.** *Decoding String* reverses a digit string and reads
ASCII values greedily; *Expand Given String* has nested parentheses and needs a
[[stack]]. Expansion is the direction where output size explodes, so always check
the bound on the result before you build it. Grammar-shaped input belongs to
[[parsing]].

**Edits that need a stack.** *Backspace String Compare* and *Compare Character
Arrays with Backspaces* process `#` as a delete; *Eliminate Substring* removes
every occurrence of `AWS` repeatedly, including the ones created by earlier
removals. Both are one pass with a stack, and both have a tempting quadratic
solution — see the traps.

**Counting instead of scanning.** When only the multiset matters, drop to a
26-slot array: [[frequency-counting]], [[anagrams]], and *Better Compression*
with its per-letter totals.

**Real compression.** When symbol frequencies are skewed you want
variable-length codes: [[huffman]], which *The Huffman Decoder* is built on.

**Searching and indexing.** [[string-matching]] for KMP, Z and Rabin-Karp,
[[rolling-hash]] for fingerprints, [[trie]] for prefix sets, [[palindromes]] and
[[manachers]] for mirrored structure, [[suffix-structures]] for every substring
at once.

```python run
def blocks(seq, continues):
    """Maximal blocks of seq under a 'this element continues the block' test."""
    i, n, out = 0, len(seq), []
    while i < n:
        j = i + 1
        while j < n and continues(seq[j - 1], seq[j]):
            j += 1
        out.append(seq[i:j])
        i = j
    return out


def compress_ranges(nums):
    """Distinct values ascending; maximal consecutive runs written start-end."""
    parts = []
    for b in blocks(sorted(set(nums)), lambda a, c: c == a + 1):
        parts.append(str(b[0]) if len(b) == 1 else "%d-%d" % (b[0], b[-1]))
    return ",".join(parts)


def compress_in_place(chars):
    """Omit-one encoding written back into the same list; returns new length."""
    write, i, n = 0, 0, len(chars)
    while i < n:
        j = i + 1
        while j < n and chars[j] == chars[i]:
            j += 1
        chars[write], write = chars[i], write + 1
        if j - i > 1:
            for d in str(j - i):
                chars[write], write = d, write + 1
        assert write <= j, "the writer overtook the reader"
        i = j
    return write


print("ranges  ", compress_ranges([7, 3, 1, 2, 9, 8, 3]))
assert compress_ranges([7, 3, 1, 2, 9, 8, 3]) == "1-3,7-9"
assert compress_ranges([]) == "" and compress_ranges([5]) == "5"
assert compress_ranges([1, 3, 5]) == "1,3,5"

buf = list("aabcccccaaa")
m = compress_in_place(buf)
print("in place", "".join(buf[:m]), "| new length", m, "of 11")
assert "".join(buf[:m]) == "a2bc5a3"

import random
rng = random.Random(5)
for _ in range(400):
    t = [rng.choice("ab") for _ in range(rng.randrange(0, 40))]
    buf = list(t)
    m = compress_in_place(buf)
    ref = []
    for b in blocks(t, lambda a, c: a == c):
        ref.append(b[0])
        if len(b) > 1:
            ref.append(str(len(b)))
    assert "".join(buf[:m]) == "".join(ref) and m <= len(t)
print("400 random buffers: in-place result matches, and never exceeds the input")
```

The `assert write <= j` inside `compress_in_place` is not decoration. It is the
proof obligation from the cost section, checked on every run of every random
input — if the omit-one bound were ever violated the loop would be silently
corrupting data it has not read yet, and this assert is the only thing that would
notice.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"maximal run of equal consecutive characters"**, verbatim or nearly. Several
   statements in this bank use exactly that phrase. It is the most reliable
   single sentence in the topic.
2. **"consecutive", "in a row", "group", "streak", "contiguous"** applied to
   equal or related elements. *Longest Same-Character Substring* and *Count
   Substrings With Identical Characters* both hinge on the word contiguous.
3. **A rule list with an exception for length one**, or a sentence about
   returning the original when the result is not shorter. That is the compression
   family, and the exception is the whole difficulty.
4. **An example whose count reaches two digits**, like `g10c` or `c10`. The
   statement is warning you, in the only way it can, that a count is a decimal
   *string* and not a character.
5. **`length <= 10^5` or `2 * 10^5`, and the answer is a string.** That
   constraint rules out anything quadratic, which in practice rules out `+=` in a
   loop and repeated slicing. It is telling you the intended solution is one
   pass with a list builder.
6. **Alphabet declared as "lowercase English letters"**, which is 26 symbols and
   an invitation to index an array by `ord(c) - ord('a')` instead of hashing.

Anti-signals:

- **"subsequence"** — order preserved, adjacency not required. Nothing in this
  chapter applies. *Check a Repeated String as a Subsequence*, *String
  Subsequences*, *Find Words in String Not in Subsequence*.
- **"alphabetical order" plus "total count"** — that is a frequency table, not
  runs. *Better Compression* is the trap, and it is an easy problem people fail
  by pattern-matching on the word "compression".
- **"occurrence of a pattern"**, "index of the first occurrence", a needle and a
  haystack — [[string-matching]]. *Find the Substring* even adds a wildcard.
- **Nested delimiters, parentheses, a grammar** — [[parsing]].
- **A window with a budget** ("at most k of something") — [[sliding-window]].

## Traps

**Losing the last run.** Symptom: the output is right except that the final group
is missing, on every input. Cause: emitting when the character *changes* rather
than emitting once per run. Demonstrated below.

**Building the answer with `+=`.** Symptom: correct on the samples, times out at
`n = 10^5`, and is mysteriously fine when you profile it locally. Cause: `Θ(m²)`
characters copied. Demonstrated below.

**Single-digit counts.** Symptom: encodings containing `:` or `<` for runs of ten
or more. Cause: `chr(ord('0') + k)` instead of `str(k)`. Demonstrated below.

**`>=` where the statement says strictly shorter.** Symptom: on inputs where the
encoding ties the original, you return the encoding and the judge wants the
original. Only shows up on one test.

**Repeated `replace` until nothing changes.** *Eliminate Substring* asks you to
remove every `AWS`, including ones formed by earlier removals, so
`while "AWS" in s: s = s.replace("AWS", "")` is tempting. Each pass is `Θ(n)` and
there can be `Θ(n)` passes, so it is `Θ(n²)` at `|s| = 10^5`. The linear version
pushes characters onto a stack and pops three whenever the top three spell the
pattern backwards.

**Slicing inside the loop.** `s[i:i+len(p)] == p` at every `i` is
`Θ(n · |p|)` and allocates `n` strings. Compare with `s.startswith(p, i)`, which
allocates nothing, or use [[string-matching]] when `|p|` is large.

**Assuming the encoding is reversible.** Covered in the proof: only on digit-free
alphabets.

**`len` is not the number of characters a human sees.** Under Unicode it counts
code points. The statements here say ASCII, so you are safe; the habit is not.

**Forgetting the empty string.** `s[0]` on an empty input raises. Every
compression statement quoted in the brief mentions the empty case explicitly —
*Basic String Compression with Length Guard* says "the empty string remains
empty". The block scanner handles it for free because the outer `while i < n`
never runs; a `for` loop over `range(1, n)` with a separate first-element read
does not.

```python run
def blocks_of(s):
    i, n, out = 0, len(s), []
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        out.append((s[i], j - i))
        i = j
    return out


def right(s):
    return "".join(c + str(k) for c, k in blocks_of(s))


def forgot_flush(s):
    out, i = [], 0
    for j in range(1, len(s)):
        if s[j] != s[i]:
            out.append(s[i] + str(j - i))
            i = j
    return "".join(out)                 # the final run never leaves the loop


def single_digit(s):
    return "".join(c + chr(ord("0") + k) for c, k in blocks_of(s))


s = "aabcccccaaa"
print("right        ", right(s))
print("forgot flush ", forgot_flush(s), "  <- the trailing a3 is gone")
print("single digit ", single_digit("a" * 12), "        <- chr(48 + 12) is '<'")
assert right(s) == "a2b1c5a3"
assert forgot_flush(s) == "a2b1c5"
assert single_digit("a" * 12) != "a12"


def copies_with_plus(pieces):
    """Characters copied by `out = out + piece`: a fresh string every time."""
    total = copied = 0
    for p in pieces:
        total += len(p)
        copied += total
    return copied


def copies_with_join(pieces):
    """Characters copied by list.append plus one "".join."""
    return sum(len(p) for p in pieces)


for m in (10, 100, 1000):
    ps = ["x"] * m
    print("m = %5d   '+=' copies %8d    join copies %6d"
          % (m, copies_with_plus(ps), copies_with_join(ps)))
assert copies_with_plus(["x"] * 1000) == 1000 * 1001 // 2
assert copies_with_join(["x"] * 1000) == 1000
print("'+=' copies m(m+1)/2 characters; join copies m. That is the whole story.")
```

The copy counters are a model, not a benchmark: they count what each strategy
has to move, which no interpreter optimisation can argue with.

## What to memorise

Almost nothing. One template, one question, one habit.

**The template**, which should come out of your fingers without thought:

```python
i, n = 0, len(s)
out = []
while i < n:
    j = i + 1
    while j < n and s[j] == s[i]:
        j += 1
    out.append(...)          # one piece for the run s[i:j], length j - i
    i = j
answer = "".join(out)
```

**The question** that turns a statement into that template: *"Does the answer
depend on where equal characters sit next to each other, or only on how many
there are in total?"* Adjacency means the run scanner. Totals mean a frequency
array. Confusing the two is how *Better Compression* eats people.

**The habit**: build a list and join once, never `+=` in a loop; and write the
loop so that the emit happens once per block, inside the loop, so there is no
final flush to forget.

Numbers worth carrying: an always-count encoding is at most `2n` and hits `2n`
when no two neighbours match; an omit-one encoding is at most `n`, which is what
makes in-place safe; a run first pays for itself at length 3; `ord('a') = 97`,
`ord('A') = 65`, `ord('0') = 48`, and a lowercase alphabet is 26 slots — small
enough to index directly instead of hashing.

## Check yourself

:::check
Run-length encoding is supposed to compress. Why can its output be longer than
its input, and what is the exact worst case for the always-count form?
--
Because the cost of a run is `1 + d(k)` characters — the character plus its
decimal length — and that is independent of `k` except through the digit count.
A run of length 1 costs 2, so it *expands*. A string with no two equal neighbours
is all length-1 runs.

Summing, `|E(s)| = Σ (1 + d(k_r)) ≤ Σ (1 + k_r) = R + n ≤ 2n`, with equality iff
every `k_r = 1`. So the worst case is exactly double, achieved by `"abc"`,
`"abab"`, and any string with no repeats in adjacent positions.

That inequality is why *Basic String Compression with Length Guard* exists: it
asks for the encoding only when it is strictly shorter, which for short runs is
never. A run first pays for itself at length 3, where 2 characters replace 3.
:::

:::check
Someone says: "run-length encoding is lossless, so I can always decode the output
back to the input." Where are they wrong?
--
Lossless-ness depends on an assumption about the alphabet that the phrase hides:
the encoding is invertible only when the alphabet contains **no decimal digit**.
The proof needs it at exactly one step — the decoder reads the longest digit
block after a character, and it is correct only because the next character after
the count is a run head, hence not a digit.

Concretely, the two-character string `a1` encodes to `a1` followed by `11`, which
is `a111`; the letter `a` repeated 111 times also encodes to `a111`. Two
different inputs, one output, so no decoder can exist. *Run-Length String
Compression* (Salesforce) allows "letters, digits, or symbols", so its output is
genuinely not decodable — which is fine, because it never asks you to decode.

Real formats pay for the guarantee, with an escape character, a fixed-width
count, or a separator. If you promise a round trip in an interview, say what you
are assuming about the alphabet.
:::

:::check
In-place compression writes the code back into the input buffer with a write
cursor and a read cursor. Why can the write cursor never overtake the read
cursor — and which encoding rule is that argument relying on?
--
It relies on the **omit-one** rule: a run of length 1 emits just its character,
with no count.

Under that rule a run of length `k` emits `1` character when `k = 1`, and
`1 + d(k)` when `k ≥ 2`, where `d(k) = ⌊log₁₀ k⌋ + 1`. Check `1 + d(k) ≤ k`:
at `k = 1` it is `1 ≤ 1`; at `k = 2` it is `2 ≤ 2`; for `k ≥ 3` a number with `d`
digits is at least `10^(d-1)`, which is at least `d + 2`, so `k ≥ d(k) + 2`.

Now induct on the runs. Before processing the run `[i, j)` we have `write ≤ i`.
The run consumes `k = j - i` positions and writes at most `k`, so afterwards
`write ≤ i + k = j`, which is the next `i`. The base case is `write = i = 0`.
Since every position written is below `j` and every position read is at or above
`i ≥ write`, no unread character is ever clobbered.

The argument breaks for the always-count rule, where a length-1 run writes 2
characters: the very first single character would push `write` past `read`. That
is why the in-place variant is always stated with the omit-one rule.
:::

:::check
Two statements look identical: *Run-Length String Compression* asks you to
compress `aabaa`, and *Better Compression* asks you to compress `a3c9b2c1`. Give
the answers, and say in one sentence what distinguishes the two problems.
--
`aabaa` run-length encodes to `a2b1a2` (or `a2ba2` under the omit-one rule): two
separate runs of `a`, kept apart and kept in place.

`a3c9b2c1` "better compresses" to `a3b2c10`: the input is already a sequence of
character-count pairs, the two `c` entries are *totalled* into 10, and the result
is sorted alphabetically.

The distinction: run-length encoding is about **adjacency** and preserves order;
better compression is about **totals** and imposes alphabetical order. One is the
block scanner in this chapter, the other is a frequency table
([[frequency-counting]]) plus a sort. The giveaway words are "consecutive" in the
first and "alphabetical order" plus "total count" in the second.

Two practical notes on the second: the counts in the input are multi-digit, so
parsing must read a whole digit block, and `c9` plus `c1` giving `c10` is the
example the statement chooses precisely to catch a single-digit parser.
:::

:::check
Why is `out = out + piece` inside a loop asymptotically worse than
`out.append(piece)` followed by one `"".join(out)`, when both produce the same
string and both look like one operation per piece?
--
Because strings are immutable, so `+` cannot extend anything — it must allocate a
new string of the combined length and copy both operands into it. On step `r` it
copies the whole prefix built so far. With `m` one-character pieces the total
copied is `1 + 2 + … + m = m(m+1)/2`, so `Θ(m²)` character moves for an `m`
character answer.

`join` is given the whole list up front. It sums the lengths, allocates once, and
copies each character exactly once: `Θ(m)`.

The reason this bug survives testing is that CPython has an in-place resize
optimisation for `s += t` when `s`'s reference count is exactly 1, which makes
the quadratic version behave linearly in the simplest possible loop. It is an
implementation detail, not a language guarantee; it disappears as soon as another
name refers to the string, when the concatenation is written `s = s + t` in some
builds, or on a different interpreter. Depending on it means your correctness
argument for the *running time* rests on a refcount you cannot see. See
[[complexity-analysis]] for why that distinction matters more than the constant
factor.
:::
