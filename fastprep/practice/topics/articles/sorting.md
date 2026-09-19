# Sorting: the Landscape

> Sorting is almost never the answer to a question. It is the move that makes
> the answer local: you pay `n log n` once, and afterwards everything you need
> to know about the whole set can be read off from neighbours.

## When you reach for it

Eight hundred and twenty-six problems in this bank use sorting, which puts it
at #4 of 150 — behind only [[arrays]], [[strings]] and [[hash-tables]]. That is
not evidence that sorting is hard; it is evidence that sorting is
*infrastructure*, the step you take before the interesting step. So the useful
question is not "do I know how to sort?" but "when does sorting earn its
`log n`?"

One test decides it, and it takes five seconds:

> **Would the answer change if I shuffled the input?**

If the answer is no — the problem is about a *set* or *multiset*, not a
sequence — then you may reorder the input however you like, for free, and
sorted order is the most useful order there is. *Minimum Absolute Difference
Pairs* wants the closest two values anywhere in the array; that is
permutation-invariant, so sort, and the closest pair is now adjacent, and an
`O(n²)` scan collapses to one `O(n)` pass. *All Pairs with Target Sum* is the
same argument feeding [[two-pointers]], *Merge Intervals* the same argument
feeding a left-to-right sweep.

The uses fall into three shapes, worth naming separately because they fail in
different ways.

**Sorting is the whole answer.** The statement spells out an order and you
transcribe it. *Cardinality Sorting* wants "ascending first by binary
cardinality, then by decimal value". *Sort Products by Aisle With Frozen Items
Last* wants non-frozen before frozen, then aisle descending, then SKU
ascending. The difficulty is never the algorithm; it is reading the
specification exactly and getting the tie-breakers right.

**Sorting is a preprocessing step.** The real work happens afterwards and is
easy only because the data is ordered: a sweep ([[intervals]], [[sweep-line]]),
a greedy taking items in a proven-good order ([[greedy]]), a two-pointer scan,
a binary search ([[binary-search]]). Sorting is one line here — but choosing
the *right key* is usually the entire insight.

**Sorting is in the answer's definition.** Some problems mention the sorted
array without asking for it. *Count Students Outside Their Sorted Positions*
compares the input against its own sorted copy; *Minimum Swaps to Sort an
Array* asks how far the input is from sorted; *Max Chunks to Make Sorted II*
asks where you may cut so that sorting the pieces sorts the whole. The sorted
copy is a reference object, and the mistake is to sort in place and destroy the
thing you needed to compare against.

Now the other side. Sorting is the *wrong* tool when:

- **Order carries meaning.** Subarrays, prefixes, streaks, events in time.
  Sorting destroys contiguity, so it destroys the problem. [[sliding-window]]
  and [[kadane]] live on the side of the line where you may not reorder.
- **The input is already sorted.** *Squares of a Sorted Array* and *Merge
  Sorted Array* both hand you sorted data. `sorted()` answers correctly in
  `O(n log n)` when `O(n)` is sitting right there, and that gap is exactly what
  the question tests.
- **You only need a few elements.** [[quickselect]] is `O(n)` expected and a
  size-`k` heap is `O(n log k)`. See [[top-k]].
- **The key space is tiny.** *Sorted Character Frequencies* has 26 possible
  keys; *Sort Colors* has three. See [[counting-sort]].
- **The data arrives over time.** You cannot sort a stream you have not
  finished reading: [[heap]], [[median-maintenance]], [[streaming]].

## The idea

A comparison sort is a game of twenty questions against an adversary who is
holding one of `n!` possible orderings, and the only question you are allowed
to ask is "is this one smaller than that one?"

Everything else in this chapter falls out of that image. At the start, all `n!`
arrangements are possible. Each comparison has two outcomes, so it splits the
set of still-possible answers in two and you continue in whichever part the
answer sends you. You are finished when one arrangement survives. An algorithm
is therefore a **decision tree**: internal nodes are comparisons, edges are the
two answers, leaves are outputs.

<svg viewBox="0 0 700 280" role="img" aria-label="decision tree of comparisons sorting three elements a, b, c, with six leaves and depth three">
  <g>
    <rect class="fill" x="300" y="12" width="90" height="30" rx="6"/>
    <text x="345" y="32" text-anchor="middle">a &lt; b ?</text>
    <line x1="320" y1="42" x2="185" y2="86"/>
    <line x1="370" y1="42" x2="515" y2="86"/>
    <text x="235" y="68">yes</text>
    <text x="450" y="68">no</text>
    <rect class="fill" x="140" y="86" width="90" height="30" rx="6"/>
    <text x="185" y="106" text-anchor="middle">b &lt; c ?</text>
    <rect class="fill" x="470" y="86" width="90" height="30" rx="6"/>
    <text x="515" y="106" text-anchor="middle">a &lt; c ?</text>
    <line x1="160" y1="116" x2="80" y2="164"/>
    <line x1="210" y1="116" x2="280" y2="164"/>
    <line x1="490" y1="116" x2="420" y2="164"/>
    <line x1="540" y1="116" x2="620" y2="164"/>
    <text x="80" y="182" text-anchor="middle">a b c</text>
    <rect class="fill" x="240" y="164" width="90" height="30" rx="6"/>
    <text x="285" y="184" text-anchor="middle">a &lt; c ?</text>
    <text x="420" y="182" text-anchor="middle">b a c</text>
    <rect class="fill" x="575" y="164" width="90" height="30" rx="6"/>
    <text x="620" y="184" text-anchor="middle">b &lt; c ?</text>
    <line x1="262" y1="194" x2="210" y2="238"/>
    <line x1="308" y1="194" x2="355" y2="238"/>
    <line x1="598" y1="194" x2="548" y2="238"/>
    <line x1="643" y1="194" x2="690" y2="238"/>
    <text x="205" y="256" text-anchor="middle">a c b</text>
    <text x="358" y="256" text-anchor="middle">c a b</text>
    <text x="545" y="256" text-anchor="middle">b c a</text>
    <text x="688" y="256" text-anchor="middle">c b a</text>
    <text x="20" y="274">6 leaves, so some path is at least 3 long</text>
  </g>
</svg>

Read that picture twice. The first reading tells you how sorting works. The
second tells you how fast it can possibly be: a binary tree with `n!` leaves
must have a path of length at least `log₂(n!)`, which is about `n log₂ n`.
There is no cleverness below that line. This is the **`n log n` lower bound**,
derived properly in *What it costs*.

The image also explains the whole family in one sentence: **the algorithms
differ in how much of the remaining uncertainty one comparison destroys.**
Insertion sort at its worst rules out one arrangement per comparison, so it
needs `Θ(n²)`. Merge sort and quicksort each halve the surviving set, so they
need `Θ(n log n)`. Counting sort refuses to play: it *reads* the key instead of
comparing it, leaves the model, and finishes in `O(n + k)`.

The trace below uses a second, more hands-on view of the same thing. An
**inversion** is a pair of positions `i < j` with `a[i] > a[j]`. A sorted array
has none; a reversed array has `n(n-1)/2`. Sorting is the job of destroying
every inversion, and speed is decided by how many you destroy per unit of work.

## Worked by hand

Insertion sort on `a = [5, 2, 4, 1, 3]`, written the way you would do it on
paper: take the next element and slide it left past everything bigger, one
adjacent swap at a time. The array starts with 7 inversions — `(5,2)`, `(5,4)`,
`(5,1)`, `(5,3)`, `(2,1)`, `(4,1)`, `(4,3)`.

| pass | element | comparisons | slides | array after | inversions left |
| --- | --- | --- | --- | --- | --- |
| start | — | — | — | `[5, 2, 4, 1, 3]` | 7 |
| 1 | 2 | 1 (`5>2`) | 1 | `[2, 5, 4, 1, 3]` | 6 |
| 2 | 4 | 2 (`5>4`, `2>4` stop) | 1 | `[2, 4, 5, 1, 3]` | 5 |
| 3 | 1 | 3 (`5>1`, `4>1`, `2>1`) | 3 | `[1, 2, 4, 5, 3]` | 2 |
| 4 | 3 | 3 (`5>3`, `4>3`, `2>3` stop) | 2 | `[1, 2, 3, 4, 5]` | 0 |
| | | **9 total** | **7 total** | sorted | |

Four things in that table are worth more than the algorithm itself.

**Slides equal inversions, exactly.** Seven slides, seven inversions, and not
by luck: swapping two *adjacent* out-of-order elements removes the inversion
between them and changes no other pair, since every other pair keeps both its
relative order and its relative position. A sort that only swaps neighbours
therefore pays one swap per inversion, and a reversed array of a hundred
thousand elements holds about `5 × 10⁹` of them. That is the real reason bubble
sort and insertion sort are slow — not "two nested loops", but *one inversion
destroyed per unit of work*.

**Comparisons exceed slides by exactly the number of early stops.** Nine
comparisons, seven slides, two passes (2 and 4) that ended on a failed
comparison. That extra comparison per pass makes insertion sort **adaptive**:
on sorted input every pass stops immediately, giving `n - 1` comparisons, zero
slides and `Θ(n)`. It is why Python's sort is fast on nearly-sorted data, and
why *Minimum Right Shifts to Sort the Array* — really "how many sorted runs are
there?" — is a run-detection question.

**Pass 3 moved an element three places; pass 1 moved one, one place.** The work
is not uniform. An element far from home is expensive, and no amount of local
tidying makes it cheap. The escape is to move elements *far* in one operation,
which is what [[merge-sort]] does when it merges two long runs and what
[[quicksort]] does when it throws an element across the pivot.

**The prefix is always sorted.** After pass `k`, positions `0..k` hold the
first `k+1` input values in sorted order. That sentence is the loop invariant,
and it is what the next section turns into a proof.

## Why it is correct

Two claims need proving: that the output is in order, and that it is a
rearrangement of the input rather than some other pile of numbers. Most people
prove the first and assume the second — and the second is the one that breaks
when a comparator or a key function is wrong.

:::proof Insertion sort sorts, and sorts stably
**Setup.** An array `a[0..n-1]` and a comparison `<` that is a *strict weak
ordering*: `x < x` is false, `x < y` and `y < z` imply `x < z`, and
"incomparable" is itself transitive. The algorithm: for `i = 1 .. n-1`, set
`key = a[i]`, then while `j >= 0` and `a[j] > key`, copy `a[j]` to `a[j+1]` and
decrement `j`; finally write `key` to `a[j+1]`.

**Invariant.** At the start of the iteration for index `i`:

- **(I1)** `a[0..i-1]` is sorted: `a[p] <= a[q]` for all `p < q < i`.
- **(I2)** `a[0..n-1]` is a permutation of the original array.
- **(I3)** Among elements of `a[0..i-1]` that compare equal, their relative
  order is the order they had in the input.

**Base case.** `i = 1`. `a[0..0]` is one element, trivially sorted, so (I1)
holds; nothing has been written, so (I2) and (I3) hold.

**Inductive step.** Assume the invariant before the iteration for `i`. The
inner loop shifts right, one at a time, exactly those elements of `a[0..i-1]`
strictly greater than `key`, stopping at the first `a[j] <= key` (or at
`j = -1`). Call that index `j*`, so `key` is written to `a[j*+1]`.

*(I2).* The loop performs `i - 1 - j*` copies of the form `a[t+1] = a[t]`, then
writes the saved value `key` into the vacated slot `a[j*+1]`. Every value that
was in `a[0..i]` is still there exactly once: the copies form a chain with no
value overwritten before it is copied (we move right to left), and the one slot
that would have been lost, `a[i]`, held `key`, which we saved before the loop
and restore at the end. The multiset is unchanged.

*(I1).* `a[0..i-1]` was sorted, so the elements greater than `key` form a
*suffix* of it: if `a[p] > key` and `q > p` then `a[q] >= a[p]`, and
`a[q] <= key` with `a[p] > key` would contradict transitivity. The loop shifts
precisely that suffix, and after the write `a[0..j*] <= key` (the scan stopped
at `j*`, and everything left of it is `<= a[j*]`) and `key <= a[j*+2..i]`
(those are the shifted elements, each strictly greater). A sorted block, then
`key`, then a sorted block, with those boundary relations, is a sorted
`a[0..i]`.

*(I3).* The loop condition `a[j] > key` is strict, so an element equal to `key`
never shifts and `key` comes to rest *after* every equal element already
placed. Elements are inserted in increasing input index, so equal elements end
up in input order.

**Termination.** The outer loop runs exactly `n - 1` times. The inner loop
decrements `j`, an integer bounded below by `-1`, so it runs at most `i` times.

**Conclusion.** After the iteration for `i = n-1`, (I1) says `a[0..n-1]` is
sorted, (I2) says it is a permutation of the input, and (I3) says equal
elements kept their input order. ∎
:::

Now the assumptions, spelled out, because this is where the bugs are.

- **The comparison is a strict weak ordering.** (I1) used transitivity twice —
  to argue the greater-than elements form a suffix, and to extend
  `a[0..j*] <= key` leftwards. A non-transitive comparator ("`a` before `b` if
  `a` is more than five smaller") makes the proof false and the output
  unsorted, with no error raised. In C++ the same defect is undefined behaviour
  and can read off the end of the array.
- **The keys do not change during the sort.** The proof compares `a[j]` with
  `key` at different times and assumes the answer does not move. Sorting by a
  field the comparator mutates, or by a dictionary you are updating as you go,
  breaks this silently.
- **The algorithm only moves elements, never invents them.** (I2) rests on
  every write being a copy of a value already present. An algorithm that
  *writes* values — counting sort reconstructs the output from tallies — needs
  its own permutation argument, and a wrong tally loses or duplicates elements
  without ever producing an unsorted array.
- **Stability is a property of the algorithm, not of sortedness.** (I3) came
  from one detail: the loop condition is `>`, not `>=`. Flip that character and
  the output is still sorted and no longer stable.
- **Nothing above mentioned speed.** The proof works for insertion sort, bubble
  sort, merge sort and heapsort alike. Wrong and slow are different bugs, found
  in different places.

## What it costs

Take the three regimes in turn, deriving each.

**Insertion sort.** The inner loop runs once per slide plus at most one failed
comparison per pass, so the work is `Θ(inversions + n)`. Inversions range from
`0` (sorted) to `n(n-1)/2` (reversed), and in a uniformly random permutation
each of the `C(n,2)` pairs is inverted with probability `1/2`, giving an
expected `n(n-1)/4`. So `Θ(n)` best, `Θ(n²)` average and worst, `Θ(1)` space.

**Divide and conquer.** [[merge-sort]] splits into halves, sorts each and
merges in one linear pass:

```
T(n) = 2 T(n/2) + Θ(n),   T(1) = Θ(1)
```

Unroll it rather than quoting the master theorem. At depth `k` there are `2ᵏ`
subproblems of size `n/2ᵏ`, each costing `Θ(n/2ᵏ)` to merge, so every level
costs `2ᵏ · Θ(n/2ᵏ) = Θ(n)`, independent of `k`. The recursion bottoms out when
`n/2ᵏ = 1`, at `k = log₂ n`. Total: `Θ(n) · log₂ n = Θ(n log n)`.

<svg viewBox="0 0 640 210" role="img" aria-label="recursion tree with four levels, each level totalling n work, showing n work per level and log n levels">
  <g>
    <rect class="fill" x="60" y="20" width="512" height="26" rx="4"/>
    <text x="316" y="38" text-anchor="middle">n</text>
    <rect class="fill" x="60" y="62" width="250" height="26" rx="4"/>
    <rect class="fill" x="322" y="62" width="250" height="26" rx="4"/>
    <text x="316" y="80" text-anchor="middle">n/2 + n/2 = n</text>
    <rect class="fill" x="60" y="104" width="119" height="26" rx="4"/>
    <rect class="fill" x="191" y="104" width="119" height="26" rx="4"/>
    <rect class="fill" x="322" y="104" width="119" height="26" rx="4"/>
    <rect class="fill" x="453" y="104" width="119" height="26" rx="4"/>
    <text x="316" y="122" text-anchor="middle">4 pieces, still n</text>
    <rect class="fill" x="60" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="126" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="192" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="258" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="324" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="390" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="456" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="518" y="146" width="54" height="26" rx="4"/>
    <text x="316" y="164" text-anchor="middle">8 pieces, still n</text>
    <text x="316" y="196" text-anchor="middle">log n levels, n per level</text>
  </g>
</svg>

[[quicksort]] has the same recurrence when the pivot splits evenly, and
`T(n) = T(n-1) + Θ(n) = Θ(n²)` when it does not. Heapsort is `Θ(n log n)`
deterministically, in place ([[heap]]).

**The floor.** Now the bound the decision tree promised:

:::proof No comparison sort beats `⌈log₂(n!)⌉` comparisons
Fix any deterministic algorithm that decides the output ordering using only
comparisons between input elements. Run it on all `n!` permutations of `n`
distinct values. Its execution is described by a binary tree: each internal
node is one comparison, its two edges are the two possible answers, and a leaf
is where the algorithm halts and emits an ordering.

**Every permutation reaches a distinct leaf.** Suppose `π ≠ σ` reached the same
leaf. Then the algorithm made the same comparisons, got the same answers, and
emitted the same output ordering for both. But the correct output ordering
differs between `π` and `σ` — that is what it means for them to be different
permutations of distinct values — so on one of the two it is wrong. A correct
algorithm therefore has at least `n!` leaves.

**A binary tree of height `h` has at most `2ʰ` leaves.** By induction: height 0
is one leaf, and a tree of height `h` has at most two subtrees of height `h-1`,
so at most `2 · 2^(h-1) = 2ʰ` leaves.

**Combine.** `2ʰ >= n!`, so `h >= log₂(n!)`, and `h` is the comparison count on
the longest path — the worst case.

**And `log₂(n!) = Ω(n log n)`,** by an argument that needs no Stirling. Drop
the smallest half of the factors: `n! >= n · (n-1) ··· (n/2) >= (n/2)^(n/2)`,
so `log₂(n!) >= (n/2)·log₂(n/2) = (n/2)(log₂ n - 1) = Ω(n log n)`. ∎
:::

What that proof assumes matters as much as what it proves: the algorithm learns
about the data **only** through comparisons, and it is deterministic.
Randomisation does not help — the same argument on expected depth gives the
same bound — but *looking at the key* does. Counting sort indexes an array with
the key, extracting `log₂ k` bits rather than one; radix sort does it `d`
times. Neither is a counterexample; both are outside the model. See
[[counting-sort]].

```python run
from itertools import permutations
from math import factorial, log2, ceil


def merge_sort(a, cmps):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    left, right = merge_sort(a[:m], cmps), merge_sort(a[m:], cmps)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        cmps[0] += 1                                  # every comparison, counted
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


n = 7
best, worst, total = 10 ** 9, 0, 0
for p in permutations(range(n)):
    c = [0]
    assert merge_sort(list(p), c) == list(range(n))
    best, worst, total = min(best, c[0]), max(worst, c[0]), total + c[0]

bound = ceil(log2(factorial(n)))
print("n = %d, so there are %d possible answers" % (n, factorial(n)))
print("information bound  ceil(log2(n!)) = %d comparisons, worst case" % bound)
print("merge sort         best %d, average %.2f, worst %d" % (best, total / factorial(n), worst))
assert worst >= bound                                 # no sort may beat the bound
print("worst >= bound, with %d comparison(s) to spare" % (worst - bound))


def counting_sort(pairs, k):
    """Stable sort of (key, payload) with 0 <= key < k. No comparisons at all."""
    count = [0] * k
    for key, _ in pairs:
        count[key] += 1
    start, s = [0] * k, 0
    for v in range(k):                                # running offsets = stability
        start[v] = s
        s += count[v]
    out = [None] * len(pairs)
    for item in pairs:
        out[start[item[0]]] = item
        start[item[0]] += 1
    return out


data = [(2, "a"), (0, "b"), (2, "c"), (1, "d"), (0, "e"), (2, "f")]
got = counting_sort(data, 3)
print("counting sort     ", got)
assert got == sorted(data, key=lambda p: p[0])        # same order, ties included
print("stable, O(n + k), and it never once asked 'is x < y?'")
```

Note the average, 12.73, sitting *below* the worst-case bound of 13. Not a
contradiction: the bound is about the longest root-to-leaf path, not the mean.
The tree may have short branches.

**Space.** Merge sort needs `Θ(n)` scratch; quicksort `Θ(log n)` of stack if
you recurse on the smaller side; heapsort `Θ(1)`. Python's `sorted` builds a
new list and costs `Θ(n)` on top of the input; `list.sort()` does not.

**The cost people forget** is the cost of one comparison.

- **The key function runs `n` times, not `n log n`** — Python computes each key
  once — but it is not free. `sorted(words, key=sorted)` for *Group Anagrams*
  is `O(n · L log L)` for the keys plus `O(n L log n)` for the comparisons.
  Counting characters gives an `O(nL)` key instead.
- **Comparing strings is `O(L)`, not `O(1)`.** *Custom Sort String* caps the
  total input at `10⁶` characters precisely so that `O(total · log n)` passes.
- **`functools.cmp_to_key` calls back into Python on every comparison**, an
  order of magnitude slower than a key function. Reach for a comparator only
  when the order genuinely is not a key — *Camel Cards* and *Find Largest
  Number (Google Early Career)* are that kind of problem.

Two numbers worth carrying: `log₂(10⁵) ≈ 17` and `log₂(10⁶) ≈ 20`. Sorting
`2 × 10⁵` items is about `3.5 × 10⁶` comparisons — nothing. Sorting inside a
loop over `n` items is `10⁵` times that, and that is your timeout.

## The implementation

In an interview you will almost never write a sort. You will write a **key**.
The implementation worth drilling is the vocabulary for turning an English
ordering sentence into one.

```python run
from collections import Counter

# "sort ascending first by binary cardinality, then by decimal value."
# Read the ordering sentence left to right; the sentence IS the tuple.
nums = [20, 3, 7, 8, 1, 6]
card = sorted(nums, key=lambda x: (bin(x).count("1"), x))
print("Cardinality Sorting :", card)
assert card == [1, 8, 3, 6, 20, 7]

# "lower frequency first, then smaller numeric value."
codes = [4, 4, 1, 2, 2, 2, 3]
freq = Counter(codes)
by_freq = sorted(codes, key=lambda c: (freq[c], c))
print("Sort Error Codes    :", by_freq)
assert by_freq == [1, 3, 4, 4, 2, 2, 2]

# A custom alphabet is a rank table, and a tuple of ranks does the rest -
# including "a prefix comes first", which tuple comparison already obeys.
rank = {ch: i for i, ch in enumerate("cba")}
arr = ["abc", "ab", "ca"]
custom = sorted(arr, key=lambda s: tuple(rank[ch] for ch in s))
print("Custom Sort String  :", custom)
assert custom == ["ca", "ab", "abc"]

# Mixed directions: non-frozen first, aisle DESCENDING, sku ascending.
products = [("A9", 3, False), ("B2", 7, True), ("C1", 3, False),
            ("A1", 7, False), ("B1", 7, True)]
one_pass = [p[0] for p in sorted(products, key=lambda p: (p[2], -p[1], p[0]))]
print("one tuple key       :", one_pass)
assert one_pass == ["A1", "A9", "C1", "B1", "B2"]

# The same order with no negation anywhere, leaning on stability: sort by the
# LEAST significant key first, then re-sort by each more significant key.
t = sorted(products, key=lambda p: p[0])                  # sku ascending
t = sorted(t, key=lambda p: p[1], reverse=True)           # aisle descending
t = sorted(t, key=lambda p: p[2])                         # non-frozen first
print("three stable passes :", [p[0] for p in t])
assert [p[0] for p in t] == one_pass

# When the answer is positions, sort the positions and not the values.
pos = sorted(range(len(nums)), key=lambda i: nums[i])
print("order of indices    :", pos)
assert [nums[i] for i in pos] == sorted(nums)
```

Three lines are carrying the chapter.

`key=lambda x: (bin(x).count("1"), x)` works because **tuples compare
lexicographically**: Python looks at the first components, and only if they tie
does it look at the second. "First by A, then by B, then by C" is `(A, B, C)`,
in that order. Almost every "sort by these rules" problem here — *Cardinality
Sorting*, *Items Sort*, *Filter and Sort Scheduled Tasks*, *Email Log
Processing, Grouping, and Sorting* — is one tuple.

`-p[1]` reverses one key inside a tuple, and only works for numbers. A string
cannot be negated, and `reverse=True` reverses *all* the keys, not one. The fix
is the three-pass block: because Python's sort is **stable**, sorting by the
least significant key first and then re-sorting by more significant keys leaves
ties broken by the earlier passes. That is the defining property of stability,
and the same property radix sort is built on.

`sorted(range(len(nums)), key=lambda i: nums[i])` saves you when the output is
positions — *Array Rank Transform* and *Count Students Outside Their Sorted
Positions* both need the original index after sorting. Sort the indices, or
sort `(value, index)` pairs; never sort the values and then try to remember
where they came from.

## Variants you will meet

**[[merge-sort]]** — split, sort the halves, merge. Stable, `Θ(n log n)`
guaranteed, `Θ(n)` space. The merge step alone answers *Merge Sorted Array*,
*Merge Two Sorted Arrays* and *Merge Three Sorted Arrays*, none of which need a
sort at all.

**[[quicksort]]** — partition around a pivot, recurse on both sides. In place,
excellent constants, `Θ(n²)` if the pivot choice is adversarial. *Implement
Merge Sort* and *Sort Colors* are the "write it yourself" problems here.

**[[quickselect]]** — quicksort that recurses on one side only, giving the
`k`-th order statistic in `O(n)` expected. *Kth Largest Element in an Array*.

**Heapsort** — build a heap, pop `n` times. In place, `Θ(n log n)` worst case,
unstable, cache-hostile. See [[heap]].

**Timsort** — what `sorted` actually is: find maximal sorted runs, extend short
ones with binary insertion sort, then merge runs under a stack discipline.
`O(n)` on sorted or reverse-sorted input, never worse than `O(n log n)`.

**[[counting-sort|Counting and radix sort]]** — no comparisons. `O(n + k)` for
keys in `0..k-1`; radix sort chains `d` stable counting sorts for `O(d(n+k))`.
The right tool for *Sort Colors* (three keys) and *Sorted Character
Frequencies* (26).

**Three-way partition / Dutch national flag** — one pass, three regions,
`O(1)` space. *Sort Colors* asks for exactly this and forbids the library call.

**[[cyclic-sort]]** — when the values are a permutation of `1..n`, put each in
its own index in `O(n)`. *Min Operations to Sort All Packages* and *Minimum
Swaps to Sort an Array* live here: the minimum number of arbitrary swaps is `n`
minus the number of cycles in the permutation.

**[[k-way-merge]]** — merge `k` sorted sequences with a `k`-element heap.
*Merge k Sorted Lists*, *Merge Multiple Sorted Streams*, *Smallest Range
Covering Elements from K Lists*.

**[[top-k]] and partial sorting** — need `k` of `n`, do not pay for the other
`n - k`. *Top K Frequent Elements*, *K Largest Integers in Descending Order*.

**[[inversion-count]]** — merge sort, instrumented: the merge step counts how
many left-half elements jump over each right-half element, giving the inversion
count in `O(n log n)` instead of `O(n²)`.

**[[custom-comparators]]** — when the order is not expressible as a key.
*Camel Cards*, and *Find Largest Number (Google Early Career)* where the rule
is "`a` before `b` if the concatenation `a+b` is larger than `b+a`".

**External sorting** — data too big for memory: sort chunks, write them out,
`k`-way merge them back. The merge is the same merge.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **The output specification names an order, with tie-breakers.** "first by
   X, then by Y", "priorities descending; scheduledTimes ascending; then
   taskIds lexicographically ascending". Transcribe it into a tuple. This is
   the single most common sorting signal in the bank.
2. **"Preserve their original input order" for ties.** *Sort Documents Left to
   Right* says exactly that. It is a demand for a **stable** sort, ruling out a
   hand-rolled quicksort and ruling in `sorted` or a `(key, index)` tuple.
3. **The question is permutation-invariant.** "any pair", "the two closest
   values", "the k-th largest". Nothing refers to position, so position is
   yours to change.
4. **An obvious `O(n²)` pairwise scan, with `n` up to `10⁵`.** *All Pairs with
   Target Sum*, *Minimum Absolute Difference Pairs*. After sorting, the pairs
   worth examining are adjacent or reachable by [[two-pointers]].
5. **"Overlapping", "merge", "conflict", "schedule", "meeting".** Sort by start
   time and sweep: [[intervals]], [[sweep-line]], [[scheduling]].
6. **"Median", "rank", "percentile", "k-th".** *All About Medians*, *Array Rank
   Transform*, *Median Home Price by City* — order statistics are defined on
   the sorted array whether or not you build it.
7. **A greedy whose exchange argument needs an order.** "Cheapest first",
   "earliest deadline first": the sort is step one of the proof as much as of
   the code. See [[greedy-exchange]].

The anti-signals, which are just as valuable:

- **The input is stated to be sorted.** A gift, not a formality: *Squares of a
  Sorted Array*, *Merge Sorted Array*, *Find K Closest Elements in a Sorted
  Array*, *Count Distinct Values in a Sorted Array*. The intended solution is
  `O(n)` or `O(log n)`; `sorted()` answers correctly and fails the question.
- **The statement forbids it.** *Check Anagrams Without Sorting* and *Sort
  Colors* say so explicitly, because a 26-bucket or 3-bucket count is linear.
- **Contiguity matters.** "subarray", "substring", "consecutive days", "in the
  order they arrive". Reordering changes the answer, so it is illegal.
- **Only the extremes are wanted.** One pass, a heap, or [[quickselect]].
- **The output must be in input order.** *Array Rank Transform* returns its
  result "in the original order" — sort a copy to compute ranks, then map back.

## Traps

**Sorting the array you still needed unsorted.** *Count Students Outside Their
Sorted Positions* compares each position against the sorted copy; sort in place
and every position matches. Symptom: an answer of zero, always.

**Text that looks numeric.** `"10" < "9"` is true. Symptom: the result is
sorted, just not the way anyone wanted. *Median of Parsed Integer Strings*
names the parse in its title for this reason.

**Negating a key that is not a number.** `-name` is a `TypeError`;
`reverse=True` flips every key, not one. Symptom: a crash, or a silently wrong
tie order. Use the stable multi-pass form.

**Assuming stability you were not given.** Python's `sorted` and Java's
`Collections.sort` are stable; C++'s `std::sort`, Java's primitive
`Arrays.sort` and any quicksort you write yourself are not. Symptom: correct on
the samples, wrong on a hidden test with ties. If you need a tie order, put it
in the key — `(key, index)` — rather than trusting the algorithm.

**A comparator that is not a strict weak ordering.** Tolerance comparisons,
float comparisons with an epsilon, "`a` before `b` if `a` beats `b`" for a
non-transitive game. Symptom: the output is not sorted and the library is
blamed.

**Keys that move while you sort**, because the comparator or another thread
modifies them. Symptom: irreproducible orders.

**`list.sort()` returns `None`.** Symptom: `AttributeError: 'NoneType' object
has no attribute ...` two lines later.

**Re-sorting in a loop.** A sorted view recomputed after each of `n` updates is
`O(n² log n)`. Symptom: a timeout on the large case only. Maintain a heap, an
[[ordered-set]] or a [[balanced-bst]] instead.

**Sorting when bucketing would do.** `O(n log n)` where `O(n)` exists is not
wrong, but on a 26-letter alphabet it is the difference between "solved it" and
"solved it well".

```python run
from functools import cmp_to_key

# TRAP: the values are digits, but the type is text.
tokens = ["10", "9", "100", "23"]
print("lexicographic :", sorted(tokens))
print("numeric       :", sorted(tokens, key=int))
assert sorted(tokens) == ["10", "100", "23", "9"]
assert sorted(tokens, key=int) == ["9", "10", "23", "100"]

# TRAP: a comparator with a tolerance. "Close enough counts as equal" is not an
# ordering, because 'equal' stops being transitive.
def close_enough(a, b, tol=5):
    if a < b - tol:
        return -1
    if b < a - tol:
        return 1
    return 0

assert close_enough(0, 4) == 0 and close_enough(4, 8) == 0
assert close_enough(0, 8) == -1          # 0 ~ 4 and 4 ~ 8, yet 0 < 8
vals = [8, 4, 0, 12, 3]
out = sorted(vals, key=cmp_to_key(close_enough))
print("tolerance sort:", out, " ascending?", all(x <= y for x, y in zip(out, out[1:])))
assert out != sorted(vals)               # the library is fine; the order is not

# TRAP: sort() mutates and returns None.
ranked = [3, 1, 2].sort()
print("sort() returns:", ranked, "- it rearranges in place")
assert ranked is None

# TRAP: sorting the reference you were supposed to compare against.
heights = [1, 3, 2]
target = sorted(heights)                 # a copy; heights still holds the input
misplaced = sum(1 for h, t in zip(heights, target) if h != t)
print("heights", heights, "target", target, "-> out of place:", misplaced)
assert heights == [1, 3, 2] and misplaced == 2
```

## What to memorise

Very little of it is code.

**The template**, which should come out of your fingers:

```python
rows.sort(key=lambda r: (r.group, -r.score, r.name))   # "by group, score desc, name"

t = sorted(rows, key=lambda r: r.name)                 # mixed directions, no negation:
t = sorted(t,    key=lambda r: r.score, reverse=True)  # least significant key first,
t = sorted(t,    key=lambda r: r.group)                # relying on stability
```

**The sentence** that decides whether to sort at all: *"Would the answer change
if I shuffled the input? If not, sort — then ask what has become true about
neighbours."* Almost every use of sorting here is that second half: afterwards
the closest pair is adjacent, the overlapping intervals are consecutive, the
duplicates are together, the `k`-th largest is at a known index.

**The habit**: write the ordering rule out in English, then transcribe it left
to right into a tuple. Do not reason about `<` signs under pressure; three
tie-breakers with two directions is where everybody's fingers slip.

**The numbers.** `log₂(10⁵) ≈ 17`, `log₂(10⁶) ≈ 20`. `Θ(n log n)` is optimal
for comparisons; `O(n + k)` is available when the keys are small integers. A
reversed array has `n(n-1)/2` inversions and any adjacent-swap sort pays one
step for each. Python's sort is stable and `O(n)` on data already in runs.

## Check yourself

:::check
Why is `log₂(n!)` equal to `Θ(n log n)`? Give the lower bound without using
Stirling's approximation.
--
Upper bound, easily: `n! <= nⁿ`, so `log₂(n!) <= n log₂ n`.

Lower bound: throw away the smaller half of the factors. The product
`n · (n-1) ··· 2 · 1` contains the `n/2` factors from `n/2` up to `n`, each at
least `n/2`, and every discarded factor is at least 1. So `n! >= (n/2)^(n/2)`,
and therefore

```
log₂(n!) >= (n/2) · log₂(n/2) = (n/2)(log₂ n - 1)
```

which is `Ω(n log n)`. Both bounds together give `Θ(n log n)`, and this version
is reconstructible at a whiteboard in twenty seconds.
:::

:::check
Someone says: "counting sort runs in `O(n)`, so the `n log n` lower bound is
simply false." Where are they wrong?
--
They have dropped the hypothesis. The theorem is about **comparison sorts**:
algorithms whose only access to the data is asking "is `x < y`?". The proof
builds a binary decision tree out of those comparisons and counts its leaves;
with no comparisons there is no tree to count. Counting sort uses the key as an
array index, and one indexing operation distinguishes `k` outcomes rather than
2, so the information argument gives a different bound. A different model, not
a contradiction.

The version of their worry that matters: counting sort is `O(n + k)`, so it
only wins when `k` is comparable to `n`. Sorting `10⁵` values drawn from
`0 … 10⁹` would need a billion buckets. Radix sort fixes that by sorting `d`
digits at a time, at the price of `d` stable passes.
:::

:::check
You must order records by department ascending, then by manager name
*descending*, then by employee id ascending. Write the plan, and explain why it
produces the right answer.
--
A string cannot be negated, so one tuple will not do it. Sort three times, from
the least significant key to the most significant:

```python
t = sorted(rows, key=lambda r: r.emp_id)
t = sorted(t,    key=lambda r: r.manager, reverse=True)
t = sorted(t,    key=lambda r: r.dept)
```

It works because the sort is **stable**: equal elements keep the relative order
they had going in. After pass 1 the records are in employee-id order; pass 2
groups by manager and, within a manager, leaves pass 1's order; pass 3 groups
by department and leaves each department's internal order — now exactly
"manager descending, then employee id" — untouched. By induction, after pass
`i` the records are ordered by keys `i, i-1, …, 1` in that priority.

This is the argument that makes radix sort work, and why a radix sort built on
an unstable inner sort is not merely slow but wrong.
:::

:::check
A candidate writes a comparator: "`a` comes before `b` if `a.price` is at least
one cent less than `b.price`; otherwise they are equal." The code compiles,
runs, and produces an unsorted list. Why, and what is the general rule being
broken?
--
A comparator must be a **strict weak ordering**, and the part being broken is
that *incomparability must be transitive*. With a one-cent tolerance, `1.000`
and `1.009` are "equal", and `1.009` and `1.018` are "equal", but `1.000` and
`1.018` are not. "Equal" has stopped being an equivalence relation, so there is
no consistent order to produce.

The proof above used transitivity twice — to show the elements greater than the
key form a contiguous suffix of a sorted prefix, and to extend `a[j] <= key`
leftwards. Both steps fail here, and implementations fail differently: Python
returns an arbitrary arrangement, C++'s `std::sort` may run off the array.

The fix: sort by the raw price and apply the tolerance afterwards, when
grouping the sorted list. Tolerance is a clustering rule, not an ordering rule.
:::

:::check
Insertion sort is `Θ(n²)`. Why, then, is it inside Python's `sorted`, which is
`O(n log n)`?
--
Because the quadratic term is `Θ(inversions)`, not `Θ(n²)` unconditionally, and
Timsort only ever runs it on inputs where the inversions are few.

Timsort scans for maximal ascending or strictly descending runs, reversing the
descending ones, and uses insertion sort only to extend a run shorter than the
minimum run length (32 to 64). On a segment of at most 64 elements the
`Θ(inversions)` bound is a small constant times `n`, and insertion sort's tiny
constant factor and sequential memory access beat merge sort's allocation.

The lesson: asymptotics classify algorithms, they do not choose them. Below a
few dozen elements the `Θ(n²)` algorithm with the better constant wins, which
is why every industrial-strength sort is a hybrid — and why nearly-sorted
input, the *Minimum Right Shifts to Sort the Array* shape, sorts in linear time
in practice.
:::
