# Permutations and Combinations (generation)

> Enumeration is not about nested loops or clever formulas. It is about picking a
> canonical form for the objects you want, so that one depth-first walk over
> choices reaches every object exactly once — no misses, no repeats.

## When you reach for it

You reach for generation when the statement asks for **the objects themselves** and
the constraint line is small enough that there are few of them. One hundred and
thirty-one problems here lean on it, which puts it at #29 of 150. They come in four
shapes.

- **Every ordering of a collection.** *Permutations*, *Generate All String
  Permutations*, *Permutations of Unique Characters*, *String Permutations in
  Custom Character Order*. Note the bounds: 8 values, 9 characters, 7 characters.
  Those numbers are not arbitrary.
- **Every sub-collection.** *Subsets*, *Sorted Subsets of a String* — the latter
  capped at 16 characters, which is `2^16 = 65536` rows.
- **One choice from each of several lists.** *Letter Combinations of a Phone
  Number*, *Phone Keypad Letter Combinations*, *ABO Parent Genotype Combinations*.
  The branching factor changes from level to level, and the total is the product of
  the list sizes.
- **Sub-collections satisfying a predicate.** *Combination Sum with Reusable
  Values*, *Combination Sum with Single-Use Values*, *Factor Combinations*. Here
  the predicate also prunes, which is what keeps the search honest.

The tool is wrong in three situations, and all three are common.

The first is when the question is **how many**, not **which ones**. *Count
Permutations Without Three Equal Parities in a Row* allows 500 values; *Unique
Digit Permutations Without Leading Zero* allows 20 digits. Counting is a different
skill — a formula ([[combinatorics]]), a recurrence ([[counting-dp]]), or a
state-compressed DP ([[dp-bitmask]]).

The second is when the statement asks for **one specific object**: the next, the
previous, the k-th, a random one. Each has a direct construction that never
materialises its neighbours. *Next Permutation* appears three times in this bank,
and *Next and Previous Lexicographic Permutation* demands `O(1)` auxiliary space,
which rules generation out by fiat.

The third is the trap that catches people who have just learned the word.
*Balanced Permutation Subarrays* (200,000 elements), *Can Sort Permutation in Given
Moves* (100,000 elements), *Permutation Sorter* and *Minimum Number of Permutation
Operations* all say "permutation" in the first sentence, and none of them wants you
to enumerate anything. There, "permutation" is a *property of the input* — each of
`1..n` appears exactly once — to be exploited, not expanded.

## The idea

Build the object one slot at a time, and let the recursion be the loop nest you
cannot write.

If you knew the answer had exactly three slots you would write three nested loops.
You do not know that, and even if you did, the loops would have to skip values
already used, which nested loops cannot express. So write one function that fills
**the next slot** and calls itself for the rest. The call stack holds the partial
object; its depth is the slot number ([[recursion]]).

Drawn out, the recursion is a tree. The root is the empty object. The children of
a node are the legal choices for the next slot. Every leaf is a finished object,
and every finished object sits at the end of exactly one root-to-leaf path.

<svg viewBox="0 0 680 300" role="img" aria-label="choice tree for the permutations of one two three: root, three children, six leaves">
  <g>
    <circle class="fill" cx="340" cy="30" r="16"/>
    <text x="340" y="36" text-anchor="middle">·</text>
    <circle cx="130" cy="115" r="16"/>
    <text x="130" y="121" text-anchor="middle">1</text>
    <circle cx="340" cy="115" r="16"/>
    <text x="340" y="121" text-anchor="middle">2</text>
    <circle cx="550" cy="115" r="16"/>
    <text x="550" y="121" text-anchor="middle">3</text>
    <line x1="328" y1="42" x2="142" y2="103"/>
    <line x1="340" y1="46" x2="340" y2="99"/>
    <line x1="352" y1="42" x2="538" y2="103"/>
    <circle cx="70" cy="200" r="16"/>
    <text x="70" y="206" text-anchor="middle">2</text>
    <circle cx="190" cy="200" r="16"/>
    <text x="190" y="206" text-anchor="middle">3</text>
    <circle cx="280" cy="200" r="16"/>
    <text x="280" y="206" text-anchor="middle">1</text>
    <circle cx="400" cy="200" r="16"/>
    <text x="400" y="206" text-anchor="middle">3</text>
    <circle cx="490" cy="200" r="16"/>
    <text x="490" y="206" text-anchor="middle">1</text>
    <circle cx="610" cy="200" r="16"/>
    <text x="610" y="206" text-anchor="middle">2</text>
    <line x1="122" y1="129" x2="78" y2="186"/>
    <line x1="138" y1="129" x2="182" y2="186"/>
    <line x1="332" y1="129" x2="288" y2="186"/>
    <line x1="348" y1="129" x2="392" y2="186"/>
    <line x1="542" y1="129" x2="498" y2="186"/>
    <line x1="558" y1="129" x2="602" y2="186"/>
    <line x1="70" y1="216" x2="70" y2="240"/>
    <line x1="190" y1="216" x2="190" y2="240"/>
    <line x1="280" y1="216" x2="280" y2="240"/>
    <line x1="400" y1="216" x2="400" y2="240"/>
    <line x1="490" y1="216" x2="490" y2="240"/>
    <line x1="610" y1="216" x2="610" y2="240"/>
    <text x="70" y="258" text-anchor="middle">123</text>
    <text x="190" y="258" text-anchor="middle">132</text>
    <text x="280" y="258" text-anchor="middle">213</text>
    <text x="400" y="258" text-anchor="middle">231</text>
    <text x="490" y="258" text-anchor="middle">312</text>
    <text x="610" y="258" text-anchor="middle">321</text>
    <text x="340" y="290" text-anchor="middle">left to right is lexicographic order, because the choices are tried in order</text>
  </g>
</svg>

Everything interesting about this topic is the phrase *exactly one path*. It is
easy to write a walk that reaches every object, and easy to write one that never
repeats; getting both at once is the craft, and it has a name: **canonical form**.
Decide, before writing code, what makes two choice sequences the same object, then
design the choices so each object has one legal sequence.

Three canonical forms cover nearly everything:

- **Permutations.** Order matters, so nothing is redundant: slot `i` takes any
  element not yet used, and the path *is* the object.
- **Combinations and subsets.** Order does not matter, so `{1,3}` and `{3,1}` are
  one object. Declare the increasing listing canonical: slot `i` may take only
  indices greater than the previous slot's. That one restriction is the entire
  difference between `n!` and `2^n`.
- **Multisets.** Two equal values in different positions are interchangeable, so a
  node branches **once per distinct value**, not once per position.

The same twelve lines generate permutations, subsets, combinations, keypad strings
and combination sums; only the candidate rule at a node differs.

## Worked by hand

Take `a = [1, 2, 3]` and walk the tree above with a pen. The state is a `path` list
and three booleans `used`. The walk fills slot `len(path)`; at each node it scans
`i = 0, 1, 2` and descends into every `i` that is free.

| step | depth | path | used | action |
| --- | --- | --- | --- | --- |
| 1 | 0 | `[]` | `FFF` | try `i=0`: free, take 1 |
| 2 | 1 | `[1]` | `TFF` | try `i=0`: used. `i=1`: free, take 2 |
| 3 | 2 | `[1,2]` | `TTF` | `i=2` free, take 3 |
| 4 | 3 | `[1,2,3]` | `TTT` | depth 3: **emit a copy** `[1,2,3]` |
| 5 | 2 | `[1,2]` | `TTF` | undo 3; loop over, undo 2 |
| 6 | 1 | `[1]` | `TFF` | try `i=2`: free, take 3 |
| 7 | 2 | `[1,3]` | `TFT` | `i=1` free, take 2 |
| 8 | 3 | `[1,3,2]` | `TTT` | **emit** `[1,3,2]` |
| 9 | 0 | `[]` | `FFF` | all of 1's subtree done; undo 1, try `i=1` |
| 10 | 1 | `[2]` | `FTF` | subtree emits `[2,1,3]`, `[2,3,1]` |
| 11 | 0 | `[]` | `FFF` | undo 2, try `i=2` |
| 12 | 1 | `[3]` | `FFT` | subtree emits `[3,1,2]`, `[3,2,1]` |

Six leaves, `3! = 6`. Four things in that table are worth more than the code.

**Step 4 says "emit a copy", and the copy is not a detail.** `path` is one list
object, mutated all the way down and all the way back up. Store it rather than a
copy and, by step 12, every row you stored is the same empty list. The traps
section demonstrates this, because everyone writes it once.

**Every descent is paired with an undo.** After step 5, `used` is exactly what it
was at step 2 — not approximately, exactly. That pairing is what lets you reason
about sibling branches independently, and it is the whole content of the word
[[backtracking]].

**The output came out sorted without a sort.** Nothing in the walk compares two
permutations. They arrive in lexicographic order because the loop tries candidates
in ascending order and a prefix decided earlier dominates everything decided later.
Problems demanding lexicographic output — *Permutations*, *Generate All String
Permutations*, *Sorted Subsets of a String* — are asking you to notice this, not to
call `sort` on a factorial-sized list.

**The tree is not stored anywhere.** The "tree" is the shape traced by the call
stack over time; at any instant only one root-to-node path exists in memory, which
is why the space cost is `O(n)` while the time cost is factorial.

## Why it is correct

The interesting claim is not that the walk produces permutations, but that it
produces *each distinct one exactly once*, even when the input has repeats — the
case *Unique String Permutations* and *String Permutations in Custom Character
Order* both insist on. So prove that version: sort the input into `a[0..n-1]`;
walk with `path` and `used`; at each node scan `i` upward and descend into `i` when
`a[i]` is unused **and** differs from the value of the previous descent here.

:::proof The walk emits every distinct arrangement exactly once, in order
**Notation.** `M` is the input multiset, `P` the current `path`, `R = M − P` the
multiset of values whose positions are still unused, and `P·Q` concatenation. An
*arrangement of `R`* is a sequence containing each element of `R` with its
multiplicity; two arrangements are the same when they are equal as sequences.

**Lemma (exact restoration).** A call to `walk` returns with `path` and `used` as
it found them. Induction on `|R|`: with `|R| = 0` the body only reads; otherwise
each iteration does `used[i] = True; path.append(...)`, then a recursive call which
by the hypothesis restores what it changed, then `path.pop(); used[i] = False`,
inverting the two writes. A finite loop of state-preserving iterations preserves
state. ∎

**Claim.** A call with path `P` emits exactly the sequences `{P·Q : Q an
arrangement of R}`, each exactly once, in increasing lexicographic order of `Q`.

**Base case, `|R| = 0`.** Then `len(path) == n`, and the body emits `P` and
returns. The empty multiset has exactly one arrangement, the empty sequence, so
the emitted set is `{P·ε}` — one element, once, vacuously ordered.

**Inductive step, `|R| = m > 0`.** Assume the claim for every call with `m − 1`
remaining.

*The accepted children are exactly the distinct values of `R`, in increasing
order.* The array is sorted, so positions holding a given value are contiguous and
unused positions are scanned in nondecreasing value order. The first unused
position holding a value `v ∈ R` is accepted; every later position holding `v` is
rejected, since the last accepted value is still `v` when the scan reaches it. And
because the scan is nondecreasing in value, `v` can never reappear after a larger
value was accepted. So the children are in bijection with the distinct values of
`R`, met in increasing order.

*Each child emits the right set.* Descending on value `v` yields path `P·v` and
remaining multiset `R − {v}` of size `m − 1`; by the induction hypothesis it emits
exactly `{P·v·Q' : Q' an arrangement of R − {v}}`, each once, in increasing order
of `Q'`. By the lemma each sibling starts from the state its predecessor started
from, so the hypothesis applies to all of them with the same `R`.

*Completeness.* Let `Q` be any arrangement of `R`. Since `m > 0`, `Q = v·Q'` with
`v ∈ R` and `Q'` an arrangement of `R − {v}`, and the child for `v` emits `P·Q`.

*Uniqueness.* Two emissions from different children differ at position `|P|`, since
distinct children commit distinct values there; two from the same child contradict
that child's hypothesis.

*Order.* All sequences have length `n`, so comparison is decided at the first
differing position. Everything from the child for `v` carries `v` at position
`|P|`, and everything from a later child carries a strictly larger value there, so
the blocks come in increasing order; inside a block the hypothesis gives it.

**Termination.** Each recursive call strictly decreases the non-negative integer
`|R|`, and each node runs a loop of at most `n` iterations, so the walk finishes at
depth at most `n`.

**Corollary (the count).** Let `f(R)` be the number of leaves below a node with
remaining multiset `R`. The argument above gives `f(∅) = 1` and
`f(R) = Σ_{v distinct in R} f(R − v)`, which is the standard recurrence for the
multinomial coefficient `|R|! / ∏_v m_v!`. For distinct values that is `n!`. ∎
:::

Now name what the proof used, because that list is where the bugs live.

- **The input is sorted.** The "distinct children" step needed equal values to be
  contiguous in scan order. Run the same guard on an unsorted array and you get
  duplicates — not a crash, just extra rows that sample tests with distinct values
  never reveal.
- **Restoration is exact, and covers *everything*.** The lemma was proved about
  `path` and `used`. A running sum, a counter, a "seen" set, a string being built —
  every piece of mutable state carried down must be undone, or the sibling's
  induction hypothesis is false.
- **The emission is of the value, not the container.** The proof says "emits `P`",
  meaning the sequence. Appending a reference to a list you keep mutating emits
  something else.
- **Equal values are interchangeable.** Dedup by value is right only when two equal
  values really produce the same answer. If elements carry identity the output
  preserves, the guard silently deletes real answers. *Combination Sum with
  Single-Use Values* draws exactly this line: duplicate values may both be used,
  but two selections with the same multiset count once.
- **All outputs have the same length.** The ordering half of the proof relied on
  it. When lengths differ, as in the combination-sum family, "lexicographic" needs
  a tie rule for prefixes, and *Combination Sum II With Negative Values* spells one
  out: a row that is a prefix of another comes first.

Notice what the proof did *not* use: any claim about pruning. A sound cut changes
the running time, never the answer set. If the output is wrong, the prune is a
suspect only when it removed a branch that did contain a solution.

## What it costs

Two numbers matter: how many leaves there are, and how much the tree above them
costs on top.

**Node count.** For `n` distinct values, the nodes at depth `k` are the ordered
selections of `k` values from `n`, so there are `n!/(n−k)!` of them. Total:

```
N = Σ_{k=0}^{n} n!/(n−k)! = n! · Σ_{j=0}^{n} 1/j! < e · n! ≈ 2.72 · n!
```

The tree has fewer than three nodes per leaf, so the search is
*output-sensitive*: you pay a constant factor over the size of the answer, not a
factor that grows.

**Time.** Let `T(m)` be the cost of a call with `m` values remaining. A node does
`Θ(m)` scanning work and recurses `m` times; a leaf copies `n` values:

```
T(0) = Θ(n)                    T(m) = m · T(m−1) + Θ(m)
```

Unrolling, the `n!` leaves each cost `Θ(n)` and dominate the internal work, so
generating all permutations is `Θ(n · n!)`. The `n` is the copy: unavoidable if the
permutations must be returned, absent if you only test each one — which is why
"count them" and "return them" can differ in complexity.

**Subsets** have `2^{n+1} − 1` nodes and `2^n` leaves, and the total output size is
`Σ_k k·C(n,k) = n·2^{n−1}` values, so `Θ(n · 2^n)` with copies.

**Combinations** are where pruning earns its keep. Choosing `k` of `n` with the
increasing-index rule, add the cut "stop if fewer than `k − len(path)` indices
remain". With it every node has at least one leaf below it, and every leaf has at
most `k + 1` ancestors, so the node count is at most `(k+1)·C(n,k)` — again
output-sensitive. Without it a node can head a completely barren subtree, and for
`k` near `n` most of the tree is barren. See [[pruning]].

**Space** is `O(n)` for the path plus `O(n)` stack frames; the output dominates
memory whenever you accumulate it.

**The costs people forget.** `value in path` is `Θ(n)` per candidate, and also
*wrong* for multisets. Building strings by concatenation allocates at every node.
And deduplicating by dumping tuples into a set costs a hash of the whole sequence
per leaf, on top of the branches you could have skipped.

Numbers worth carrying, because they explain every constraint line in this bank:

| `n` | `n!` | `2^n` |
| --- | --- | --- |
| 8 | 40,320 | 256 |
| 10 | 3,628,800 | 1,024 |
| 11 | 39,916,800 | 2,048 |
| 13 | 6,227,020,800 | 8,192 |
| 16 | — | 65,536 |
| 20 | — | 1,048,576 |
| 25 | — | 33,554,432 |

*Alternating Parity Permutations* allows `n ≤ 11`, so the full tree has 39.9
million leaves — but the valid answers for `n = 11` (six odd values in the odd
positions, five even in the even positions) number only `6!·5! = 86,400`. The ratio
of 462 to 1 is collected by rejecting a candidate whose parity matches the previous
one *at the node where it is chosen*, not by filtering leaves. That is a three-word
change, and it is the difference between a solution and a timeout.

## The implementation

```python run
from itertools import permutations as ref
from math import factorial


def permutations_lex(items):
    """Every distinct arrangement of a multiset, in lexicographic order."""
    a = sorted(items)
    n = len(a)
    used = [False] * n
    path, out = [], []

    def walk():
        if len(path) == n:
            out.append(list(path))            # a copy; path keeps changing
            return
        prev = None
        for i in range(n):
            if used[i] or a[i] == prev:       # one branch per distinct value
                continue
            prev = a[i]
            used[i] = True
            path.append(a[i])
            walk()
            path.pop()                        # undo, exactly
            used[i] = False

    walk()
    return out


def multinomial(items):
    total = factorial(len(items))
    for v in set(items):
        total //= factorial(items.count(v))
    return total


print("permutations of 'aab' :", ["".join(p) for p in permutations_lex("aab")])
print("permutations of 1,2,3 :", permutations_lex([1, 2, 3]))
print("'aabb' has", len(permutations_lex("aabb")), "distinct arrangements, not", factorial(4))

for case in ["aab", "abc", "aabb", "", "zza", [3, 1, 1, 2]]:
    got = permutations_lex(case)
    want = sorted(set(ref(sorted(case))))
    assert [tuple(p) for p in got] == want, case
    assert got == sorted(got), "output is not lexicographic"
    assert len(got) == multinomial(list(case)), case
print("6 inputs: matches deduplicated itertools, sorted, and the multinomial count")
```

Three lines carry the weight.

`a = sorted(items)` does two jobs at once, which is why it is easy to forget that
it is load-bearing: it makes the output lexicographic, and it makes equal values
adjacent so the duplicate guard can be local. Remove it and both go, silently.

`if used[i] or a[i] == prev` is the whole multiset story. `prev` is the value of
the last branch taken *at this node*, so skipping a candidate equal to it makes the
node branch once per distinct value — exactly the "children are the distinct values
of `R`" step of the proof. You will also see the equivalent
`if i > 0 and a[i] == a[i-1] and not used[i-1]: continue`, which keeps only the
leftmost unused copy; it is correct but harder to justify at a whiteboard.

`path.pop()` and `used[i] = False` are the lemma, written down. Whatever else you
carry — a running sum for *Combination Sum*, the parity of the last value for
*Alternating Parity Permutations* — gets its undo on the same two lines.

Two adaptations, both fragments of the same shape:

```python
# combinations: canonical form is "indices strictly increase", plus the prune
def walk(start):
    if len(path) == k:
        out.append(list(path)); return
    for i in range(start, n - (k - len(path)) + 1):    # enough left to finish
        path.append(a[i]); walk(i + 1); path.pop()

# combination sum, reusable values: pass i, not i + 1, to reuse a[i]
def walk(start, left):
    if left == 0:
        out.append(list(path)); return
    for i in range(start, n):
        if a[i] <= left:                               # sound only for positives
            path.append(a[i]); walk(i, left - a[i]); path.pop()
```

The difference between *Combination Sum with Reusable Values* and *Combination Sum
with Single-Use Values* is the character between `i` and `i + 1`. Both stay
non-decreasing, so both emit each multiset once; reuse just lets the index stand
still.

## Variants you will meet

**Subsets and the power set.** Take-or-skip at each index — the same tree with a
branching factor of two — or a loop over bitmasks `0 .. 2^n − 1`. The required
*order* picks the implementation: *Subsets* asks for increasing mask order, the
bitmask loop; *Sorted Subsets of a String* asks for lexicographic string order, the
DFS preorder (`""`, `"a"`, `"ab"`, `"abc"`, `"ac"`, `"b"`, …). See [[subsets]].

**Combinations, `C(n, k)`.** Increasing indices plus the remaining-count prune.
*Fixed-Length Combination Sum* is this with a predicate at the leaf.

**Cartesian products.** One choice from each list: *Letter Combinations of a Phone
Number*, *Expand Attribute Combinations*, *ABO Parent Genotype Combinations*. The
recursion advances a *level* instead of consuming a pool, so there is no `used`
array at all, and the output size is the product of the level sizes.

**Next permutation.** The lexicographic successor, in place, in `O(n)`:

<svg viewBox="0 0 660 190" role="img" aria-label="next permutation: pivot, descending suffix, swap with the rightmost larger element, then reverse">
  <g>
    <rect x="20" y="30" width="56" height="40" rx="4"/>
    <rect x="76" y="30" width="56" height="40" rx="4"/>
    <rect class="fill" x="132" y="30" width="56" height="40" rx="4"/>
    <rect x="188" y="30" width="56" height="40" rx="4"/>
    <rect x="244" y="30" width="56" height="40" rx="4"/>
    <rect x="300" y="30" width="56" height="40" rx="4"/>
    <text x="48" y="56" text-anchor="middle">1</text>
    <text x="104" y="56" text-anchor="middle">2</text>
    <text x="160" y="56" text-anchor="middle">4</text>
    <text x="216" y="56" text-anchor="middle">7</text>
    <text x="272" y="56" text-anchor="middle">6</text>
    <text x="328" y="56" text-anchor="middle">5</text>
    <text x="160" y="22" text-anchor="middle">pivot</text>
    <text x="272" y="22" text-anchor="middle">non-increasing suffix</text>
    <line x1="188" y1="76" x2="356" y2="76"/>
    <text x="272" y="96" text-anchor="middle">swap pivot with rightmost value &gt; 4, then reverse the suffix</text>
    <rect x="400" y="30" width="42" height="40" rx="4"/>
    <rect x="442" y="30" width="42" height="40" rx="4"/>
    <rect class="fill" x="484" y="30" width="42" height="40" rx="4"/>
    <rect x="526" y="30" width="42" height="40" rx="4"/>
    <rect x="568" y="30" width="42" height="40" rx="4"/>
    <rect x="610" y="30" width="42" height="40" rx="4"/>
    <text x="421" y="56" text-anchor="middle">1</text>
    <text x="463" y="56" text-anchor="middle">2</text>
    <text x="505" y="56" text-anchor="middle">5</text>
    <text x="547" y="56" text-anchor="middle">4</text>
    <text x="589" y="56" text-anchor="middle">6</text>
    <text x="631" y="56" text-anchor="middle">7</text>
    <text x="526" y="96" text-anchor="middle">the successor</text>
    <text x="330" y="140" text-anchor="middle">a maximal non-increasing suffix is already the largest arrangement of its values,</text>
    <text x="330" y="162" text-anchor="middle">so the change must happen at the pivot, and must be the smallest possible increase</text>
  </g>
</svg>

Scan from the right for the first index `i` with `a[i] < a[i+1]` (the pivot). The
suffix after `i` is non-increasing, hence already the largest arrangement of its
values, so position `i` must change, and by the least possible amount: swap `a[i]`
with the rightmost suffix value strictly greater than it, then reverse the suffix
into the smallest arrangement of the tail. No pivot means the array is already the
largest; reverse it all to wrap. That is *Next Permutation* and, with the
comparisons flipped, the "PREVIOUS" half of *Next and Previous Lexicographic
Permutation*.

**Ranking and unranking.** The `n!` permutations of a sorted pool split into `n`
blocks of `(n−1)!`, one per first element, so the `k`-th is read off directly:
`idx, k = divmod(k, (n−1)!)` picks the first element, then repeat. This is the
factorial number system; it costs `O(n^2)` and answers "the k-th arrangement" for
`k` far beyond anything you could enumerate.

```python run
from itertools import permutations


def next_permutation(a):
    """Lexicographic successor, in place. Returns False (and wraps to the
    smallest arrangement) when a is already the largest."""
    i = len(a) - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i < 0:
        a.reverse()
        return False
    j = len(a) - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])
    return True


def kth_permutation(items, k):
    """The k-th (0-based) arrangement of distinct items, without the others."""
    pool = sorted(items)
    n = len(pool)
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i
    assert 0 <= k < fact[n]
    out = []
    for slot in range(n, 0, -1):
        idx, k = divmod(k, fact[slot - 1])     # block size = (slot-1)!
        out.append(pool.pop(idx))
    return out


a = [1, 2, 3]
chain = [list(a)]
while next_permutation(a):
    chain.append(list(a))
print("successors from [1,2,3]:", chain)
assert chain == sorted(chain) and len(chain) == 6

d = [1, 5, 1]                                  # duplicates: 3 arrangements exist
tail = [list(d)]
while next_permutation(d):
    tail.append(list(d))
print("successors from [1,5,1]:", tail, "- [1,1,5] is earlier, so it is not here")
assert tail == [[1, 5, 1], [5, 1, 1]]

full = sorted("".join(p) for p in permutations("abcde"))
for k in range(len(full)):
    assert "".join(kth_permutation("abcde", k)) == full[k]
print("kth_permutation agrees with the full list on all", len(full), "of 'abcde'")
print("the 1,000,000th arrangement of 0..9 is", "".join(kth_permutation("0123456789", 10 ** 6)))
```

**A random arrangement.** Fisher-Yates: for `i` from `n−1` down to 1, swap `a[i]`
with `a[randint(0, i)]`. Every arrangement is equally likely, by the same
block-counting argument as unranking. See [[randomized-algorithms]].

**Counting instead of generating.** When `n` leaves the single digits, switch
tools. Three patterns cover the counting problems here.

- A **closed form**: *Unique Digit Permutations Without Leading Zero* is the
  multinomial of the digit multiset minus the arrangements starting with zero —
  20 digits, pure [[combinatorics]].
- A **DP over a compressed state**: *Count Permutations Without Three Equal
  Parities in a Row* allows 500 values, but needs tracking only of how many even
  and odd values remain and the current parity run — [[counting-dp]]. *Count
  Divisible Permutations* caps `n` at 15, the signature of a mask DP over "which
  values are already placed": [[dp-bitmask]].
- The **loop order separating ordered from unordered**: *Count Ordered Combination
  Sums* counts sequences, *Count Unordered Coin Combinations* counts multisets, and
  the difference is which loop is outermost. See [[unbounded-knapsack]].

**Permutations as functions.** A permutation `p` of `1..n` is a bijection, so it
decomposes uniquely into cycles, and that decomposition answers questions that look
nothing like enumeration. Applying `p` repeatedly returns every element home after
the least common multiple of the cycle lengths — exactly what *Permutation
Operations* and *Minimum Number of Permutation Operations* ask for (modulo
`10^9+7`, so combine prime powers, not the numbers — [[number-theory]]). The
minimum number of swaps sorting `p` is `n` minus the number of cycles `c`, since a
swap raises the cycle count by at most one; and since every swap flips parity,
*Can Sort Permutation in Given Moves* answers each query in `O(1)`: `m` works when
`m ≥ n − c` and `m ≡ n − c (mod 2)`, with `n = 1` degenerate. See
[[cycle-detection]].

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"Return every / all / each" plus a single-digit or low-teens bound.** The
   pairing is the signal. `1 <= s.length <= 8` next to "return every permutation"
   is a constraint written backwards from `8! = 40320`. Bounds of 16 to 20 with
   "subset" mean `2^n` instead.
2. **A sentence defining when two answers are the same.** "Selections with the same
   multiset of values are one combination"; "two sequences with the same values in
   different orders count separately". That is the canonical form, handed to you.
3. **"In lexicographic order", or a custom order.** Sort the candidate pool and
   emit in DFS order. *String Permutations in Custom Character Order* redefines the
   alphabet — digits, then lowercase, then uppercase — changing the sort key and
   nothing else.
4. **"Distinct" or "no duplicates" with an input that can repeat.** Dedup at the
   node, by value.
5. **One choice per position from a fixed menu.** A keypad, an attribute list, a
   pair of parent genotypes. Cartesian product.
6. **A predicate testable on a partial object.** "Adjacent elements have different
   parity", "the running sum must not exceed the target". This is the invitation to
   prune, and usually the reason the bound is larger than the raw count allows.

The anti-signals, all of which appear in this bank:

- **"How many", with `n` in the hundreds or a target in the thousands.** Count, do
  not generate. A modulus of `10^9+7` confirms it: nobody asks you to enumerate a
  set whose size overflows.
- **"The next", "the previous", "the k-th", "a random one".** Direct construction.
- **`O(1)` auxiliary space.** Incompatible with holding a result list.
- **"Permutation" describing the input.** *Balanced Permutation Subarrays*,
  *Balanced Prefix Sets in a Permutation* and *Permutation Sorter* use the word to
  promise that the values are `1..n` exactly once. That promise is a gift for index
  tricks — in the two "balanced prefix" problems, the prefix `[0, i]` holds exactly
  `{1..k}` precisely when its maximum equals `i + 1` — and has nothing to do with
  enumeration.
- **The answer is a single optimum.** "Maximum", "minimum" or "the best ordering"
  over a large `n` is [[greedy]] or [[dynamic-programming]], not a search over `n!`
  candidates.

## Traps

**Storing the live path.** The most common bug in the topic, with an unmistakable
symptom: the right number of rows, all identical, usually all empty. Demonstrated
below.

**Forgetting to undo one piece of state.** `path.pop()` is remembered because it is
visible; the running sum, the parity flag, the `used` entry on an early `continue`
are not. Symptom: answers correct for the first branch and increasingly wrong
afterwards.

**Deduplicating at the end.** `set(tuple(p) for p in results)` gives the right
answers in factorial time and memory. For `"aabbb"` it explores about ten times as
many nodes as the node-level guard, and the gap grows with the repeats.
Demonstrated below.

**The duplicate guard on an unsorted pool.** It compares against the previous
candidate at the node, so if equal values are not adjacent it catches nothing.
Symptom: duplicates, only when repeats are separated.

**`if value in path` as the used-test.** Two bugs at once: it is `O(n)` per
candidate, and it forbids a second copy of a repeated value. Track *positions*, not
values.

**Pruning on a sum when values can be negative.** `if total > target: return` is
sound only for non-negative candidates. *Combination Sum II With Negative Values*
exists to punish the reflex, and caps the array at 16 values because without the
monotone cut the search is exponential.

**The combination prune, off by one.** `range(start, n - (k - len(path)) + 1)`
needs the `+ 1` because `range` excludes its end. Symptom: the last combination of
every block is missing.

**Expecting order out of a set or a dictionary.** Hash order is not an order; get
lexicographic output from the walk, or sort explicitly ([[hash-tables]]).

```python run
def gen(a, dedup_at_node, alias):
    """Return (rows, nodes visited). Two independent switches, both bugs."""
    a = sorted(a)
    n = len(a)
    used, path, out = [False] * n, [], []
    nodes = 0

    def walk():
        nonlocal nodes
        nodes += 1
        if len(path) == n:
            out.append(path if alias else list(path))     # alias: the live list
            return
        prev = None
        for i in range(n):
            if used[i]:
                continue
            if dedup_at_node and a[i] == prev:
                continue
            prev = a[i]
            used[i] = True
            path.append(a[i])
            walk()
            path.pop()
            used[i] = False

    walk()
    return out, nodes


w = "aabbb"
right, n_right = gen(w, dedup_at_node=True, alias=False)
late, n_late = gen(w, dedup_at_node=False, alias=False)
print("dedup at the node :", len(right), "rows,", n_right, "nodes visited")
print("dedup at the end  :", len(set(map(tuple, late))), "rows,", n_late, "nodes visited")
assert [tuple(p) for p in right] == sorted(set(map(tuple, late)))
assert n_right * 5 < n_late
print("same answers, %.1f times fewer nodes -- and the gap grows with the repeats"
      % (n_late / n_right))

aliased, _ = gen("abc", dedup_at_node=True, alias=True)
print("storing the live path:", ["".join(p) for p in aliased], "<- six rows, all empty")
assert len(aliased) == 6 and all(row == [] for row in aliased)
assert all(row is aliased[0] for row in aliased), "every row is the same list object"
print("they are not merely equal; they are the same object, emptied on the way out")
```

## What to memorise

One template, one sentence, one habit.

**The template**, which should come out of your fingers unprompted:

```python
path, out = [], []

def walk(state):
    if complete(state):
        out.append(list(path))        # copy
        return
    for choice in candidates(state):  # canonical order; skip repeats by value
        path.append(choice)
        walk(advance(state, choice))
        path.pop()                    # undo everything you did
```

**The sentence** that turns a problem into it: *"What is one choice, and what makes
two sequences of choices the same object?"* The first half gives you `candidates`;
the second gives you the canonical form — increasing indices for combinations, one
branch per distinct value for multisets, nothing at all for permutations of
distinct values.

**The habit**: write the undo immediately after the do, then write the recursive
call between them. Every piece of state touched on the way down gets its inverse on
the way up, in the same edit. That discipline removes most backtracking bugs, and
it is the lemma the correctness proof needed.

Numbers worth carrying: `8! = 40,320`, `10! ≈ 3.6·10^6`, `13! ≈ 6.2·10^9`;
`2^16 = 65,536`, `2^20 ≈ 10^6`, `2^25 ≈ 3.4·10^7`. If the bound is 8 to 12, they
want permutations; 16 to 25, subsets or a mask DP; larger, a count.

## Check yourself

:::check
Why does "sort, then branch once per distinct value at each node" produce each
distinct arrangement exactly once? Answer with the mechanism, not the rule.
--
Because it makes the children of a node correspond one-to-one with the *distinct
values still available*, rather than with the *positions* still free.

Every arrangement of the remaining multiset `R` begins with some value `v ∈ R`, so
the arrangements are partitioned by that first value — exhaustively (every
arrangement has a first value) and disjointly (it has only one). One child per
distinct value realises exactly that partition, and completeness plus uniqueness
follow by induction on `|R|`. Two positions holding the same value would give two
children realising the same block, which is where repeats come from. The sort is
what lets the guard detect that locally: equal values become adjacent, so "is this
the value I just branched on?" is enough.
:::

:::check
Someone says: "Node-level deduplication is fiddly. I will generate all `n!`
arrangements and put them in a set — same answers, simpler code." Where are they
wrong, and where are they right?
--
They are right about the answers: a set of tuples returns exactly the distinct
arrangements, and on distinct inputs the two approaches visit the same tree.

They are wrong about the cost, in two ways that compound. The work is `n!`
regardless of how many *distinct* answers exist: for 10 characters forming five
repeated pairs, that is 3,628,800 leaves for 113,400 answers, a factor of 32 thrown
away. And the set holds every produced tuple, so peak memory is the size of the
un-deduplicated output. The gap is the multinomial denominator `∏ m_v!`, and it
grows fast.
:::

:::check
A statement reads: "Return the number of permutations of `nums` in which no three
consecutive values have the same parity, modulo `10^9 + 7`", with
`1 <= nums.length <= 500`. What do you do, and what in the statement told you?
--
Not generation. Three things say so: the word "number" rather than "return every",
the bound of 500 (`500!` has over a thousand digits), and the modulus, which only
makes sense when the answer cannot be listed.

Count instead, noticing that the answer depends on the values only through their
parities. Let the state be `(evens left, odds left, parity just placed, length of
the current run of that parity)`; each transition places an even or an odd value,
the run extends or resets, and a run of three is forbidden. That is `O(n^2)` states
with `O(1)` transitions. Multiply at the end by `E!·O!`, since the evens are
interchangeable within the pattern and likewise the odds. This is *Count
Permutations Without Three Equal Parities in a Row*; the technique is
[[counting-dp]].
:::

:::check
In `next_permutation`, after locating the pivot `i`, why is the element swapped in
the *rightmost* value greater than `a[i]`, and why is the suffix *reversed*
afterwards rather than sorted?
--
The suffix after the pivot is non-increasing, by the definition of the pivot as the
last index with `a[i] < a[i+1]`. So it is already the largest arrangement of its
values, and no successor can be found by rearranging it alone: position `i` must
increase. To make the smallest possible increase, `a[i]` must be replaced by the
smallest suffix value strictly greater than it — and in a non-increasing sequence
that is the rightmost such value, which is what the backward scan finds.

After the swap the suffix is still non-increasing: everything right of `j` is
`<= a[i]` and everything left of it is `> a[i]`, so the outgoing and incoming values
occupy the same slot in the descending order. Reversing a non-increasing sequence
gives its smallest arrangement — exactly what the successor needs once the prefix
has grown. Reversing is `O(m)`; sorting would cost `O(m log m)` and give the same
result, which is a good way to test the claim.
:::

:::check
*Combination Sum with Reusable Values* recurses with `walk(i, ...)` and *Combination
Sum with Single-Use Values* with `walk(i + 1, ...)`. Why does passing `i` not
produce duplicate combinations, given that it lets the same value be chosen again?
--
Because the canonical form is unchanged. Both only ever choose an index `>= start`,
so every emitted row is non-decreasing in index and therefore in value; a multiset
has exactly one non-decreasing listing, so each is reachable by exactly one path.
Reuse only lets a path stand still on an index instead of always advancing.

What reuse changes is termination: with `i + 1` the depth is bounded by `n`, with
`i` only by `target / min(candidates)`, which is why that version needs positive
candidates and a `left >= 0` guard.
:::
