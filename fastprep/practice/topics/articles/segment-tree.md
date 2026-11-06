# Segment Trees

> A segment tree stores the answer for a fixed set of halving segments, so that any range is glued together from at most two of them per level, and any single change touches only the one segment per level that contains it.

## The problem it solves

You are given an array of eight numbers:

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| a | 5 | 8 | 6 | 3 | 2 | 7 | 2 | 6 |

Then a stream of operations arrives, mixed together in any order:

- `set i v`: the value at index i becomes v;
- `sum l r`: report a[l] + a[l+1] + ... + a[r].

For example: `sum 1 6` (answer 28), then `set 3 10`, then `sum 1 6` again (now
35). The array is not fixed. It changes between the questions, and every
question must see the latest values.

That is the whole problem: **range queries mixed with updates**. The operation
inside the query can be a sum, a minimum, a maximum, a count, a gcd, an "is there
anything here"; the update can change one value or a whole range. The bank's
[[p:capital-one-dynamic-wall-range-query|Dynamic Wall Building and Range Query]]
is this exact shape: build a wall at index i, then ask whether any wall stands in
[l, r]. With n and q both up to 2·10^5.

The first solution anyone writes keeps the array and does what the operations
say. `set` is one assignment. `sum l r` is a loop from l to r. An update costs
O(1), and a query costs up to n steps. With 2·10^5 queries over a 2·10^5 array,
that is up to 4·10^10 additions. Far too slow.

The second solution anyone writes is [[prefix-sums]]. Precompute
P[k] = a[0] + ... + a[k-1], and every `sum l r` is P[r+1] - P[l], one
subtraction. That is perfect while the array never changes. But `set 3 10`
changes a[3], and a[3] is inside P[4], P[5], P[6], P[7] and P[8]: every prefix
that reaches past index 3. One update rewrites up to n prefixes. The cost has
moved, not gone: queries are O(1), updates are O(n), and the same 4·10^10 is
waiting on the other side.

So the two obvious structures sit at opposite ends:

| structure | update | query | q = n = 2·10^5, worst case |
|---|---|---|---|
| plain array | O(1) | O(n) | 4·10^10 |
| prefix sums | O(n) | O(1) | 4·10^10 |
| segment tree | O(log n) | O(log n) | about 2·10^5 × 2 × 18 ≈ 7·10^6 node visits |

This chapter builds the third row. It is not a trick; it falls out of asking
what, exactly, each of the first two wastes.

### When it is the wrong tool

- **The array never changes.** Then there are no updates to pay for. Use prefix
  sums for sums and counts, and a [[sparse-table]] for min, max and gcd, which
  answers in O(1) after O(n log n) preprocessing.
- **The queries are all prefixes and the operation can be undone.** Sums, counts
  and XORs over prefixes with point updates are a [[fenwick-tree]]: a third of the
  code and much faster in practice. This chapter derives it as a special case.
- **The window only slides forward.** "Max of the last k values" where both ends
  only move right is a [[monotonic-deque]], O(1) amortised.
- **All the operations are known in advance and their order can be changed.**
  Often you can sort the queries and sweep ([[sweep-line]]), and the "update" then
  becomes an insertion into something simpler.
- **You need order statistics on a changing set and nothing else.** An
  [[ordered-set]] (a balanced tree, or a sorted list in Python) may say it more
  directly, though the segment tree over compressed values does the same job.

The bank tags 52 problems as segment trees. Many are the textbook shape with a
disguise: counting smaller elements to the left, inversions, the k-th largest of
a growing multiset, peak concurrency of intervals. They appear below where they
teach something.

## Build it from the brute force

We will not start with a tree. We start with the two slow programs above and
fix their waste one step at a time. The tree appears at the end, as the obvious
thing to build.

### Step 1: count what each extreme wastes

The plain array answers `sum 1 6` by adding six numbers. Then `set 3 10`. Then
`sum 1 6` again adds six numbers, five of which did not change. Then `sum 2 5`
adds four numbers it has already added twice. **The query re-adds work it has
already done.** Nothing is ever remembered.

Prefix sums go to the other extreme. They remember a sum for every prefix, n
precomputed numbers, and that is too many dependent facts: a single value takes
part in up to n of them. **The update has to repair too many stored answers.**

So we want something in between: store *some* precomputed sums, few enough that
one value belongs to only a few of them, and well chosen enough that any range
can be glued together from only a few of them.

### You might think: "Store the answer for every range."

That is the prefix-sum idea pushed further: precompute sum(l, r) for all
n(n+1)/2 pairs, and every query is a lookup. For n = 2·10^5 that is 2·10^10
stored numbers, before the first query. And a single update at index i changes
every range that contains i: (i+1)·(n-i) of them, 10^10 when i is in the middle.
More stored answers means more answers to repair. This is the wrong direction.

### You might think: "Prefix sums work for sum. I will do prefix maxima for max."

The plain array and prefix-sum argument above was about sums. People then assume
the same trick works for every operation. It does not.

Take a = [5, 1, 2]. The prefix maxima are M = [5, 5, 5]. Now ask for
max(a[1..2]), which is 2. For sums you would compute P[3] - P[1]. For maxima there
is no subtraction: M[2] = 5 and M[0] = 5, and no arithmetic on 5 and 5 produces
2. The 5 has swallowed the information. Sums can be undone, maxima cannot.

Remember this counterexample. It is the reason a Fenwick tree (which is built on
prefixes) handles sums and not general range maxima, and the reason the segment
tree is built on *segments*, not prefixes.

### Step 2: blocks, the first middle ground

Cut the array into blocks of B consecutive values, and store each block's sum.
With B = 2 on the example:

| block | [0,1] | [2,3] | [4,5] | [6,7] |
|---|---|---|---|---|
| sum | 13 | 9 | 9 | 8 |

Now `sum 1 6` is: a[1] by hand (the start is mid-block), then the whole blocks
[2,3] and [4,5] from the table, then a[6] by hand. That is 8 + 9 + 9 + 2 = 28,
with four additions instead of six. `set 3 10` changes a[3] and the one block
that contains it, [2,3], which becomes 6 + 10 = 16. Two writes.

In general a query does at most B values by hand on each end plus at most n/B
whole blocks, and an update does two writes. Choosing B = √n balances the two
terms: about 2√n ≈ 900 steps per query when n = 2·10^5. That is
[[sqrt-decomposition]], and it is already a hundred times better than the
plain array. It is a real technique, and it is the right answer to some
problems.

But look at what the query still does: it walks across up to n/B whole blocks,
one at a time. Those block sums are themselves an array, and we are summing a
range of it with a loop. That is the plain-array problem again, one level up.
The cure is the same cure, applied again: group the blocks into bigger blocks.

### Step 3: blocks of blocks, all the way up

Keep going. Pairs of values form blocks of 2, pairs of those form blocks of 4,
and so on, until one block covers everything. With eight values:

| level | segments and their sums |
|---|---|
| 3 (size 8) | [0,7] = 39 |
| 2 (size 4) | [0,3] = 22, [4,7] = 17 |
| 1 (size 2) | [0,1] = 13, [2,3] = 9, [4,5] = 9, [6,7] = 8 |
| 0 (size 1) | 5, 8, 6, 3, 2, 7, 2, 6 |

Each segment is split exactly in half by the level below it. That is a binary
tree: every segment is a node, its two halves are its children, and the single
values are the leaves. The total number of stored sums is
n + n/2 + n/4 + ... + 1 = 2n - 1. Not n², not even n log n. Just under twice the
array.

Now ask the two questions that matter.

**How many segments contain one index?** Exactly one per level: index 3 is in
[3,3], [2,3], [0,3] and [0,7]. That is log2(n) + 1 segments. So an update
repairs log n + 1 stored sums, not n.

**How many segments does a range need?** Take [1,6]. Use a segment whenever it
fits entirely inside the range; otherwise, split it and look at its halves.
[0,7] does not fit, split. [0,3] does not fit, split. [0,1] does not fit, split:
[0,0] is outside, [1,1] fits (8). [2,3] fits (9). [4,7] does not fit, split.
[4,5] fits (9). [6,7] does not fit: [6,6] fits (2), [7,7] is outside. Total
8 + 9 + 9 + 2 = 28, from four stored sums.

### The question that unlocks it

The step from blocks to the tree came from one question. Ask it on every
problem of this family:

**Which fixed segments should I precompute so that every range is a union of a
few of them, and every index lies in only a few of them?**

The answer for a line of n values is the halving segments: each range is a
union of at most two per level, and each index is in exactly one per level.
Both "few"s are O(log n). Everything else in this chapter (Fenwick trees, lazy
propagation, compressed coordinates, nodes that store several numbers) is a
variation on what is stored in those segments or which of them are kept.

Say it a second way. A query is fast if the answer is pre-glued in big chunks.
An update is fast if each value is glued into few chunks. Prefix sums satisfy
the first and violate the second; the plain array satisfies the second and
violates the first. The halving segments are the only simple family where
both chunk counts are logarithmic at once.

### Why "at most two per level" is true

When we split segments for [1,6], only segments that *straddle a boundary* of
the range were split: they contain l or r, but are not inside the range. At any
one level the segments do not overlap, so at most one contains l and at most one
contains r. So at most two segments per level are split, and each split produces
two children on the next level. That means at most four segments are *looked
at* per level, and at most two of them are *used*. With log n levels that is at
most about 4 log n visits per query. The proof below makes this exact.

### You might think: "The range [1,6] should use the segments [1,2], [3,4], [5,6]."

Those would be lovely, and they do not exist. The segments are fixed in
advance, aligned to their size: size-2 segments start at even indices, size-4
segments at multiples of 4. That is the price of having only 2n - 1 of them. A
range rarely aligns, so its decomposition takes ragged pieces of different
sizes: here sizes 1, 2, 2, 1. The decomposition is not the prettiest one; it is
whatever the fixed segments allow, and the argument above says it is never more
than two per level.

### Step 4: the operations, as recursion on the tree

Every node knows its segment [lo, hi] and stores the sum of a[lo..hi].

- **Build.** A leaf stores its value. An inner node builds both children, then
  stores left + right. One pass from the leaves upward: O(n).
- **Update `set i v`.** Start at the root. If the node is the leaf [i, i], write
  v. Otherwise go into the one child whose half contains i, then, on the way
  back up, recompute this node as left + right. One node per level.
- **Query `sum l r`** at a node [lo, hi], three cases:
  1. **No overlap** (r < lo or hi < l): this node contributes nothing; return 0.
  2. **Full cover** (l <= lo and hi <= r): the stored sum is exactly this node's
     share; return it without looking further.
  3. **Partial overlap**: the answer is the query on the left child plus the
     query on the right child.

Case 2 is where the speed comes from: it stops the recursion at a big
precomputed chunk. Case 3 is the only case that goes deeper, and the argument
above says it fires at most twice per level.

### The technique in one sentence

**Store the operation's result for every halving segment of the array; answer a
range by combining the at-most-two-per-level segments that tile it, and apply a
change by recomputing the one segment per level that contains it.**

And the unlocking question again, because it is the transferable part: which
segments should be precomputed so that both "how many per range" and "how many
per index" are small?

## Worked by hand

### The tree, with real numbers

Here is the tree for a = [5, 8, 6, 3, 2, 7, 2, 6]. Each box shows its segment
and its sum. The four shaded boxes are the ones that `sum 1 6` uses.

<svg viewBox="0 0 800 300" role="img" aria-label="segment tree over the array 5 8 6 3 2 7 2 6: root [0,7] sum 39, children [0,3] 22 and [4,7] 17, then [0,1] 13, [2,3] 9, [4,5] 9, [6,7] 8, then the eight leaves; the nodes [1,1] 8, [2,3] 9, [4,5] 9 and [6,6] 2 are shaded because the query sum of indices 1 to 6 uses exactly them">
  <g>
    <rect x="360" y="10" width="80" height="44" rx="4"/>
    <text x="400" y="28" text-anchor="middle">[0,7]</text>
    <text x="400" y="47" text-anchor="middle">39</text>
    <rect x="160" y="80" width="80" height="44" rx="4"/>
    <text x="200" y="98" text-anchor="middle">[0,3]</text>
    <text x="200" y="117" text-anchor="middle">22</text>
    <rect x="560" y="80" width="80" height="44" rx="4"/>
    <text x="600" y="98" text-anchor="middle">[4,7]</text>
    <text x="600" y="117" text-anchor="middle">17</text>
    <rect x="60" y="150" width="80" height="44" rx="4"/>
    <text x="100" y="168" text-anchor="middle">[0,1]</text>
    <text x="100" y="187" text-anchor="middle">13</text>
    <rect class="fill" x="260" y="150" width="80" height="44" rx="4"/>
    <text x="300" y="168" text-anchor="middle">[2,3]</text>
    <text x="300" y="187" text-anchor="middle">9</text>
    <rect class="fill" x="460" y="150" width="80" height="44" rx="4"/>
    <text x="500" y="168" text-anchor="middle">[4,5]</text>
    <text x="500" y="187" text-anchor="middle">9</text>
    <rect x="660" y="150" width="80" height="44" rx="4"/>
    <text x="700" y="168" text-anchor="middle">[6,7]</text>
    <text x="700" y="187" text-anchor="middle">8</text>
    <rect x="15" y="230" width="70" height="44" rx="4" stroke-dasharray="5 4"/>
    <text x="50" y="248" text-anchor="middle">[0]</text>
    <text x="50" y="267" text-anchor="middle">5</text>
    <rect class="fill" x="115" y="230" width="70" height="44" rx="4"/>
    <text x="150" y="248" text-anchor="middle">[1]</text>
    <text x="150" y="267" text-anchor="middle">8</text>
    <rect x="215" y="230" width="70" height="44" rx="4"/>
    <text x="250" y="248" text-anchor="middle">[2]</text>
    <text x="250" y="267" text-anchor="middle">6</text>
    <rect x="315" y="230" width="70" height="44" rx="4"/>
    <text x="350" y="248" text-anchor="middle">[3]</text>
    <text x="350" y="267" text-anchor="middle">3</text>
    <rect x="415" y="230" width="70" height="44" rx="4"/>
    <text x="450" y="248" text-anchor="middle">[4]</text>
    <text x="450" y="267" text-anchor="middle">2</text>
    <rect x="515" y="230" width="70" height="44" rx="4"/>
    <text x="550" y="248" text-anchor="middle">[5]</text>
    <text x="550" y="267" text-anchor="middle">7</text>
    <rect class="fill" x="615" y="230" width="70" height="44" rx="4"/>
    <text x="650" y="248" text-anchor="middle">[6]</text>
    <text x="650" y="267" text-anchor="middle">2</text>
    <rect x="715" y="230" width="70" height="44" rx="4" stroke-dasharray="5 4"/>
    <text x="750" y="248" text-anchor="middle">[7]</text>
    <text x="750" y="267" text-anchor="middle">6</text>
    <line x1="385" y1="54" x2="215" y2="80"/>
    <line x1="415" y1="54" x2="585" y2="80"/>
    <line x1="185" y1="124" x2="115" y2="150"/>
    <line x1="215" y1="124" x2="285" y2="150"/>
    <line x1="585" y1="124" x2="515" y2="150"/>
    <line x1="615" y1="124" x2="685" y2="150"/>
    <line x1="90" y1="194" x2="55" y2="230"/>
    <line x1="110" y1="194" x2="145" y2="230"/>
    <line x1="290" y1="194" x2="255" y2="230"/>
    <line x1="310" y1="194" x2="345" y2="230"/>
    <line x1="490" y1="194" x2="455" y2="230"/>
    <line x1="510" y1="194" x2="545" y2="230"/>
    <line x1="690" y1="194" x2="655" y2="230"/>
    <line x1="710" y1="194" x2="745" y2="230"/>
  </g>
</svg>

Check any box with a pen: [4,7] = 2 + 7 + 2 + 6 = 17, and [0,7] = 22 + 17 = 39.
Every inner node is the sum of its two children, and that is the only rule.

The same tree, concretely, on the array itself. Put the range [1,6] under the
values and mark which stored sum covers each index:

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| a | 5 | 8 | 6 | 3 | 2 | 7 | 2 | 6 |
| in [1,6]? | no | yes | yes | yes | yes | yes | yes | no |
| covered by | | [1,1]=8 | [2,3]=9 | [2,3] | [4,5]=9 | [4,5] | [6,6]=2 | |

Every index of the range is covered exactly once, nothing outside is covered,
and the pieces have sizes 1, 2, 2, 1.

### The query, node by node

Here is `sum 1 6` as the recursion sees it. The order is depth first, left
child before right child.

| step | node | segment | relation to [1,6] | action | returns |
|---|---|---|---|---|---|
| 1 | root | [0,7] | partial | split | 28 (from below) |
| 2 | | [0,3] | partial | split | 17 |
| 3 | | [0,1] | partial | split | 8 |
| 4 | | [0,0] | none: 0 < 1 | stop | 0 |
| 5 | | [1,1] | full | use stored | 8 |
| 6 | | [2,3] | full | use stored | 9 |
| 7 | | [4,7] | partial | split | 11 |
| 8 | | [4,5] | full | use stored | 9 |
| 9 | | [6,7] | partial | split | 2 |
| 10 | | [6,6] | full | use stored | 2 |
| 11 | | [7,7] | none: 6 < 7 | stop | 0 |

The story of step 6 in words: "I am the node for [2,3]. The question is about
[1,6]. All of my segment, indices 2 and 3, is inside the question, so my stored
9 is exactly my share of the answer. I do not need to look at my children; that
is the whole reason I stored 9."

The story of step 3: "I am [0,1]. The question wants index 1 but not index 0.
My stored 13 mixes the two, so I cannot use it. I ask my children: [0,0] says
'not mine, 0', [1,1] says 'all mine, 8'. I return 8."

Count the visits per level: level 3 one node, level 2 two nodes, level 1 four
nodes, level 0 four nodes. Never more than four, as promised, and only the
partial nodes, [0,7], [0,3], [0,1], [4,7] and [6,7], went deeper.

### The update, node by node

Now `set 3 10`. Index 3 is in [0,7], then [0,3] (left half, since 3 <= 3), then
[2,3] (right half of [0,3], since 3 > 1), then the leaf [3,3].

| step | node | why this way | new value |
|---|---|---|---|
| down | [0,7] | 3 <= mid 3, go left | |
| down | [0,3] | 3 > mid 1, go right | |
| down | [2,3] | 3 > mid 2, go right | |
| leaf | [3,3] | write | 10 |
| up | [2,3] | 6 + 10 | 16 |
| up | [0,3] | 13 + 16 | 29 |
| up | [0,7] | 29 + 17 | 46 |

Four nodes changed, one per level, and nothing else in the tree is stale: no
other segment contains index 3. Now `sum 1 6` uses the same four nodes as
before, [1,1] = 8, [2,3] = 16, [4,5] = 9, [6,6] = 2, total 35. Check against the
array: 8 + 6 + 10 + 2 + 7 + 2 = 35.

Notice the direction of the update: down to find the leaf, *up* to repair. A
parent can only be recomputed after its child has the new value. Writing the
parent first and the child second would leave the parent computed from the old
child.

### A second trace: uneven halves, and a maximum

The first trace had n = 8, a power of two, and a sum. Real inputs are neither.
Take a = [4, 1, 7, 3, 6], n = 5, and store maxima instead of sums. The split
point of a node [lo, hi] is mid = (lo + hi) // 2, the left child is [lo, mid],
and the right child is [mid+1, hi].

| node | mid | left child | right child | stored max |
|---|---|---|---|---|
| [0,4] | 2 | [0,2] | [3,4] | 7 |
| [0,2] | 1 | [0,1] | [2,2] | 7 |
| [3,4] | 3 | [3,3] | [4,4] | 6 |
| [0,1] | 0 | [0,0] | [1,1] | 4 |

The tree is lopsided: the left subtree has three leaves and two levels below
it, the right has two leaves and one level. Leaves sit at different depths.
Nothing in the algorithm cares. Every node is still split into two halves that
tile it, and that is all the query uses.

Query max over [1,3]:

| node | relation to [1,3] | returns |
|---|---|---|
| [0,4] | partial | max(7, 3) = 7 |
| [0,2] | partial | max(1, 7) = 7 |
| [0,1] | partial | max(nothing, 1) = 1 |
| [0,0] | none | "nothing" |
| [1,1] | full | 1 |
| [2,2] | full | 7 |
| [3,4] | partial | max(3, nothing) = 3 |
| [3,3] | full | 3 |
| [4,4] | none | "nothing" |

The answer is 7, which is right: max(1, 7, 3) = 7.

This trace shows something the first did not. What does a node outside the
range return? For sums it was 0, because adding 0 changes nothing. For maxima,
0 is wrong: if every value were negative, a disjoint node returning 0 would win
the max and the answer would be 0, which is not in the array at all. The right
"nothing" for max is minus infinity, the value that never wins. In general the
disjoint case must return the **identity** of the operation: 0 for +, minus
infinity for max, plus infinity for min, 0 for gcd and XOR and OR, all-ones for
AND. That is the subtle line of the basic segment tree, and it gets its own
demonstration below.

## From the idea to the code

### The direct version: recursive, with nodes numbered 1, 2, 3, ...

The tree lives in a flat list. The root is node 1; node k has children 2k and
2k+1. No pointers, no objects, and the children of any node are one
multiplication away.

```python run
def build(t, a, node, lo, hi):
    if lo == hi:                                  # leaf: one value
        t[node] = a[lo]
        return
    mid = (lo + hi) // 2
    build(t, a, 2 * node, lo, mid)                # left half
    build(t, a, 2 * node + 1, mid + 1, hi)        # right half
    t[node] = t[2 * node] + t[2 * node + 1]       # a node is the sum of its halves

def update(t, node, lo, hi, i, v):
    if lo == hi:                                  # reached leaf [i, i]
        t[node] = v
        return
    mid = (lo + hi) // 2
    if i <= mid:
        update(t, 2 * node, lo, mid, i, v)        # i is in the left half
    else:
        update(t, 2 * node + 1, mid + 1, hi, i, v)
    t[node] = t[2 * node] + t[2 * node + 1]       # repair on the way back up

def query(t, node, lo, hi, l, r, used=None):
    if r < lo or hi < l:                          # case 1: no overlap
        return 0                                  # the identity of +
    if l <= lo and hi <= r:                       # case 2: full cover
        if used is not None:
            used.append(((lo, hi), t[node]))
        return t[node]
    mid = (lo + hi) // 2                          # case 3: partial, split
    return (query(t, 2 * node, lo, mid, l, r, used)
            + query(t, 2 * node + 1, mid + 1, hi, l, r, used))

a = [5, 8, 6, 3, 2, 7, 2, 6]
n = len(a)
t = [0] * (4 * n)
build(t, a, 1, 0, n - 1)
used = []
print("sum 1 6 =", query(t, 1, 0, n - 1, 1, 6, used), "from", used)
assert used == [((1, 1), 8), ((2, 3), 9), ((4, 5), 9), ((6, 6), 2)]
update(t, 1, 0, n - 1, 3, 10)
print("after set 3 10: root =", t[1], " sum 1 6 =", query(t, 1, 0, n - 1, 1, 6))
assert t[1] == 46 and query(t, 1, 0, n - 1, 1, 6) == 35

import random
rng = random.Random(7)
for trial in range(200):
    n = rng.randint(1, 30)
    a = [rng.randint(-50, 50) for _ in range(n)]
    t = [0] * (4 * n)
    build(t, a, 1, 0, n - 1)
    for _ in range(30):
        if rng.random() < 0.5:
            i, v = rng.randrange(n), rng.randint(-50, 50)
            a[i] = v
            update(t, 1, 0, n - 1, i, v)
        else:
            l = rng.randrange(n); r = rng.randrange(l, n)
            assert query(t, 1, 0, n - 1, l, r) == sum(a[l:r + 1])
print("200 random arrays, 6000 mixed operations: tree == brute force")

def max_index(node, lo, hi):                      # largest node number used
    if lo == hi:
        return node
    mid = (lo + hi) // 2
    return max(max_index(2 * node, lo, mid), max_index(2 * node + 1, mid + 1, hi))

print("n = 6 uses node", max_index(1, 0, 5), "> 2n =", 12)
assert max_index(1, 0, 5) == 13
assert all(max_index(1, 0, m - 1) < 4 * m for m in range(1, 3000))
print("4n slots suffice for every n below 3000")
```

### Each line, and which part of the idea it is

| line | in plain words | in the idea |
|---|---|---|
| `t = [0] * (4 * n)` | room for every node number that can occur | the 2n - 1 segments, laid out by the 1, 2k, 2k+1 rule |
| `if lo == hi: t[node] = a[lo]` | a leaf stores its one value | level 0 of the table of segments |
| `mid = (lo + hi) // 2` | where this segment is cut | the fixed halving; every function must cut at the same place |
| `t[node] = t[2*node] + t[2*node+1]` | a node is the sum of its halves | the "glue" operation, also used to repair after an update |
| `if i <= mid` in update | which half holds i | "exactly one segment per level contains i" |
| `if r < lo or hi < l: return 0` | outside the question | contributes nothing: the identity |
| `if l <= lo and hi <= r: return t[node]` | inside the question | the precomputed chunk; this is the line that makes it fast |
| the final `return ... + ...` | straddles a boundary | split, and glue the two halves' answers |

Three lines do the real work: the full-cover return (speed), the
recompute-from-children line (correctness after updates), and the disjoint
return (the identity, which is right for sums only by luck of 0).

### Settling the boring confusions

**Why do the functions take lo and hi as arguments?** Because the list stores
only sums, not segments. A node does not know its own segment; the caller
tells it. The root is [0, n-1], and each call passes its children their halves.
This is also why every function must compute mid the same way: if `build` cut
at (lo+hi)//2 and `query` cut at (lo+hi+1)//2, they would disagree about which
segment node 2k is, and the stored sums would be read as the sums of the wrong
segments.

**Why 4n and not 2n?** There are 2n - 1 nodes, but the numbering 1, 2k, 2k+1
leaves holes when n is not a power of two. With n = 6 the root [0,5] has
children [0,2] (node 2) and [3,5] (node 3); node 3's left child [3,4] is node 6,
and its children are nodes 12 and 13. Node 13 does not fit in a list of length
12. The run block shows that 13 is reached, and that 4n is always enough. (The
precise bound is 2·2^ceil(log2 n), which is below 4n.) If you size it 2n, the
symptom is an IndexError for some n and not others, which is the worst kind.

**Why l and r inclusive?** Because the segments are inclusive, [lo, hi]. Mixing
an inclusive tree with a half-open query, [l, r), shifts every boundary test by
one. Pick one convention for the whole file. This chapter uses inclusive
everywhere.

**Does recursion depth matter in Python?** No. The depth is the height of the
tree, about log2(n) + 1, so 19 for n = 2·10^5. The default limit is 1000.
Recursion in a segment tree is safe; it is only slow (see *What it costs*).

**What does the root store?** The answer for the whole array. A query for
[0, n-1] stops at the root after one visit.

### The optimised version: bottom-up, 2n slots, no recursion

The recursive version visits nodes from the top. You can also start from the
leaves. Put the leaves at positions n..2n-1, let node k be the sum of nodes 2k
and 2k+1 for k from n-1 down to 1, and walk two pointers up from the ends of the
range. When the left pointer is a right child, its node is fully inside the
range and its parent is not, so take it and step right; symmetrically on the
other side.

```python run
def build(a):
    n = len(a)
    t = [0] * n + list(a)                 # leaves at n .. 2n-1
    for k in range(n - 1, 0, -1):
        t[k] = t[2 * k] + t[2 * k + 1]
    return t

def update(t, n, i, v):
    i += n
    t[i] = v
    while i > 1:                          # walk to the root, repairing
        i //= 2
        t[i] = t[2 * i] + t[2 * i + 1]

def query(t, n, l, r):                    # inclusive l..r
    res = 0
    l += n
    r += n + 1                            # half-open [l, r) inside the loop
    while l < r:
        if l & 1:                         # l is a right child: take it
            res += t[l]
            l += 1
        if r & 1:                         # r-1 is a left child's sibling: take it
            r -= 1
            res += t[r]
        l //= 2
        r //= 2
    return res

a = [5, 8, 6, 3, 2, 7, 2, 6]
t = build(a)
print("tree slots 1..15:", t[1:])
print("sum 1 6 =", query(t, 8, 1, 6))
assert t[1] == 39 and query(t, 8, 1, 6) == 28
update(t, 8, 3, 10)
assert t[1] == 46 and query(t, 8, 1, 6) == 35

import random
rng = random.Random(3)
for trial in range(300):
    n = rng.randint(1, 40)                # any n, not only powers of two
    a = [rng.randint(-9, 9) for _ in range(n)]
    t = build(a)
    for _ in range(40):
        i = rng.randrange(n); v = rng.randint(-9, 9)
        a[i] = v; update(t, n, i, v)
        l = rng.randrange(n); r = rng.randrange(l, n)
        assert query(t, n, l, r) == sum(a[l:r + 1])
print("300 random arrays of every size: bottom-up == brute force")
```

It is shorter, it uses exactly 2n slots, and in Python it is several times
faster because it makes no function calls. Two cautions. First, for n not a power
of two the tree is not one tidy binary tree, but every node is still the glue of
two slots and the walk still collects a tiling of the range, which is why the
random check runs over every size. Second, the walk collects pieces from the left
and from the right out of order, so for a non-commutative glue (the
weighted-score node in *Variations*) you keep a left accumulator and a right
accumulator and join them at the end. When the glue is plain + or max, none of
that matters.

### The subtle line, both ways

The line people get wrong is the one that looks like boilerplate:
`if r < lo or hi < l: return 0`. The 0 is not "nothing". It is "the value that
does not change the answer when glued in", and for sums that happens to be 0.
Copy the sum tree, change `+` to `max`, forget to change the 0, and the tree
still passes every test whose values are non-negative.

Take a = [-3, -1, -4], n = 3, and ask for max over [0,1]. Root [0,2] splits into
[0,1] (node 2) and [2,2] (node 3).

| node | relation to [0,1] | wrong version returns | right version returns |
|---|---|---|---|
| [0,1] | full | -1 | -1 |
| [2,2] | none | **0** | -inf |
| [0,2] | partial: max of the two | max(-1, **0**) = **0** | max(-1, -inf) = -1 |

The wrong cell is the disjoint node [2,2]. It was supposed to say "I am not part
of this", and instead it said "I contain a 0", and 0 beats every real value. The
answer 0 is not even in the array.

```python run
NEG = float("-inf")

def build(t, a, node, lo, hi):
    if lo == hi:
        t[node] = a[lo]; return
    mid = (lo + hi) // 2
    build(t, a, 2 * node, lo, mid); build(t, a, 2 * node + 1, mid + 1, hi)
    t[node] = max(t[2 * node], t[2 * node + 1])

def query(t, node, lo, hi, l, r, nothing, log):
    if r < lo or hi < l:
        log.append(((lo, hi), "none", nothing))
        return nothing
    if l <= lo and hi <= r:
        log.append(((lo, hi), "full", t[node]))
        return t[node]
    mid = (lo + hi) // 2
    res = max(query(t, 2 * node, lo, mid, l, r, nothing, log),
              query(t, 2 * node + 1, mid + 1, hi, l, r, nothing, log))
    log.append(((lo, hi), "partial", res))
    return res

a = [-3, -1, -4]
t = [NEG] * 12
build(t, a, 1, 0, 2)
for label, nothing in (("wrong (0)", 0), ("right (-inf)", NEG)):
    log = []
    ans = query(t, 1, 0, 2, 0, 1, nothing, log)
    print(label, "max over [0,1] =", ans)
    for row in log:
        print("    ", row)
    if nothing == 0:
        assert ans == 0 and ans not in a             # an answer from nowhere
    else:
        assert ans == -1 == max(a[0:2])

# the same bug is invisible on non-negative data, which is why it survives
b = [4, 1, 7, 3, 6]
t2 = [NEG] * 20
build(t2, b, 1, 0, 4)
for l in range(5):
    for r in range(l, 5):
        assert query(t2, 1, 0, 4, l, r, 0, []) == max(b[l:r + 1])
print("with values >= 0 the wrong identity passes every query: the bug hides")
assert query(t2, 1, 0, 4, 1, 3, NEG, []) == 7      # the second hand trace
```

What does the wrong version accidentally compute? max(0, true answer) for every
query that has any disjoint node, and the true answer for a query that is
exactly one node. So it computes "the max, clamped at zero, except sometimes".
That "except sometimes" is why it is hard to find by staring at outputs.

The rule, said twice. The disjoint case returns the identity of the glue: the
value e with glue(e, x) = x for every x. If your glue has no identity (you can
always invent one, like None, and teach the glue to skip it), do not return a
fake one; check for disjointness before recursing instead.

### Memo, table, or tree?

You may have noticed that the segment tree is a cache. Every node is a
precomputed answer to a subproblem ("sum of [lo, hi]"), and the query reuses
those answers instead of recomputing them, the same move as memoisation in
[[dynamic-programming]]. The difference is that the subproblems are chosen in
advance, the halving segments, so that each one has only one parent to
invalidate when its value changes. It is a [[divide-and-conquer]] whose results
are kept and kept up to date.

## Why it is correct

:::proof The query returns the sum of exactly a[l..r], visiting O(log n) nodes
**The invariant of the stored values.** For every node with segment [lo, hi],
t[node] = a[lo] + a[lo+1] + ... + a[hi], for the current array a.

*After build.* By induction on the segment length. A leaf [i, i] stores a[i].
An inner node stores t[left] + t[right]; by induction these are the sums of
[lo, mid] and [mid+1, hi], which do not overlap and together are [lo, hi]. So
their total is the sum of [lo, hi].

*After `set i v`.* Only segments that contain i have a different true sum. Those
are exactly the nodes on the path from the root to the leaf [i, i], because each
inner node's segment is split into two halves and i is in exactly one of them.
The update writes the leaf, then recomputes each path node from its children,
bottom to top. When a path node is recomputed, its child on the path has
already been repaired and its other child never needed repair, so by the same
argument as in the build, the node is correct. Nodes off the path were correct
before and their true sums did not change. So the invariant holds again.

**What the query returns.** Claim: query(node [lo, hi], l, r) returns the sum of
a[j] over all j in both [lo, hi] and [l, r] (zero if there are none). By
induction on the segment length.

1. No overlap: no j is in both, and the code returns 0. Correct.
2. Full cover: every j in [lo, hi] is in [l, r], so the wanted sum is the sum of
   [lo, hi], which is t[node] by the invariant. Correct.
3. Partial overlap: the segment is not a leaf (a leaf either overlaps fully or
   not at all), so it has children [lo, mid] and [mid+1, hi]. The indices in
   both [lo, hi] and [l, r] split, without overlap and without loss, into those
   in the left half and those in the right half. By induction each recursive
   call returns its part. Their sum is the whole. Correct.

At the root, [lo, hi] = [0, n-1] contains [l, r], so the root call returns the
sum of a[l..r]. Termination: each recursive call is on a strictly shorter
segment.

**How many nodes are visited.** A node is split only in case 3, which means it
contains l or contains r (it overlaps the range without being inside it, so the
range's edge cuts through it). The nodes at one depth have disjoint segments, so
at most one of them contains l and at most one contains r: at most two nodes
per depth are split. Every visited node below the root is a child of a split
node, so at most four nodes per depth are visited. The depth is at most
ceil(log2 n), so a query visits at most 4·ceil(log2 n) + 1 nodes, and an update
visits ceil(log2 n) + 1. ∎
:::

The proof leaned on these assumptions. Each is a place where a variation can
break the method.

- **The glue is associative.** The tree puts parentheses wherever the halves
  fall: (a0 + a1) + (a2 + a3), not ((a0 + a1) + a2) + a3. That is only the same
  answer if the operation is associative. Sum, min, max, gcd, XOR, AND, OR,
  matrix product: yes. Average: no (the average of two averages is not the
  average); store (sum, count) instead and divide at the end.
- **The disjoint case returns an identity.** Case 1 said "return 0" is correct
  because 0 adds nothing. For another operation the identity is different,
  as the subtle-line demo showed.
- **The order of gluing is left then right.** The proof added the left answer
  and the right answer. For + it does not matter which comes first. For a
  non-commutative glue (string concatenation, the weighted score, matrix
  product) the left child's answer must come first.
- **A node's value depends only on the values in its segment.** That is what
  lets an update repair only the path. If a node's stored value depended on
  something outside its segment (a global offset, a position counted from the
  start of the whole array), an update elsewhere would make it stale, and the
  path repair would miss it.
- **Each query is about one contiguous range of indices.** A query about "all
  values less than x" is not a range of indices; it becomes one only after you
  index the tree by value instead of by position (coordinate compression,
  variation D).

## What it costs

**Build.** There are 2n - 1 nodes, each computed once from its two children:
O(n).

**Update.** One node per level, and the height is ceil(log2 n): O(log n). For
n = 2·10^5 that is 19 nodes.

**Query.** At most four visits per level by the proof, and at most two stored
values used per level: O(log n), at most about 4·18 + 1 = 73 visits for
n = 2·10^5.

**Space.** 4n slots for the recursive layout, 2n for the bottom-up one. For
n = 2·10^5, 8·10^5 slots, which is nothing.

**The total for q operations.** O(n + q log n). For n = q = 2·10^5 that is
roughly 2·10^5 × 40 ≈ 8·10^6 node visits on average (a typical query visits far
fewer than the worst-case 73).

**The trap: the hidden constant in Python.** O(q log n) is fast in C++. In
Python, the recursive version makes a function call per visited node, and a
function call costs on the order of 100 nanoseconds or more. Ten million calls
is a second or several. That is why the bottom-up version, or a
[[fenwick-tree]] when it fits, is the practical choice in Python, and why you
should not add a class with method calls per node on top of the recursion if
time is tight. The asymptotics are identical; the constant is not.

**The other hidden cost: compression.** When the tree is indexed by value
instead of by position (variation D), you first sort the distinct values:
O(n log n), plus a dictionary or a binary search for each lookup. That usually
dominates the tree itself, and it is still well within limits.

**For comparison.** Block decomposition: O(√n) per operation, about 900 for
n = 2·10^5, so 2·10^5 operations are about 2·10^8 steps: fine in C++, too slow
in Python. The plain array and prefix sums: O(n) on one side, 4·10^10 in the
worst case. The segment tree's log n is not a small improvement; it is the
difference between running and not.

## How to think about it

The code is short. What is hard is seeing that a problem is a segment tree, and
deciding what each node stores. Ask these questions, in this order, every time.

1. **What is the array?** Sometimes it is given. Often it is hidden: time
   slots, positions in a sorted order of values, the letters of a string, the
   Euler tour of a tree. Name the index and what lives at it.
2. **What is a query, as a range of that array?** If the query is not a range
   of indices, look for an index under which it becomes one. "How many earlier
   values are smaller than x" is the range [smallest value, x-1] of an array
   indexed by value.
3. **What is the glue?** Sum, min, max, count, gcd, OR. Is it associative? What
   is its identity? Is it commutative (does the left-then-right order matter)?
4. **Is the glue enough on one number?** If the answer for a whole segment cannot
   be computed from one number per half, the node must store more: the maximum
   subarray needs four numbers per node, the weighted score needs three. Ask
   "what must each half tell me so that I can answer for the whole?", which is
   the knapsack question in another form: what is the least the parent needs to
   know about each child?
5. **What is an update: one point, or a range?** One point: the basic tree.
   A range: lazy propagation (variation F), or, if the queries are single
   points, a difference array in a Fenwick tree (variation E).
6. **Are the queries all prefixes, and is the glue invertible?** Then a Fenwick
   tree does it in a third of the code (variation C).
7. **Are the coordinates huge?** Values up to 10^9 but only 2·10^5 of them:
   compress first (variation D). Know every coordinate in advance, including
   the ones that only queries mention.
8. **Is there a cheaper structure?** No updates: prefix sums or a sparse table.
   A window that only slides: a deque. Offline queries: sort and sweep.

Then, before writing code, write four lines: **the index**, **what a node
stores**, **the glue and its identity**, and **what an update does to a leaf**.
If you cannot write those four lines, you do not have the tree yet.

### Telling it from its neighbours

- **Prefix sums** ([[prefix-sums]]). Same queries, no updates. If there are no
  updates, the segment tree is the wrong tool and costs a log for nothing.
- **Fenwick tree** ([[fenwick-tree]]). Prefix queries with an invertible glue
  and point updates. Every Fenwick problem is a segment-tree problem; not every
  segment-tree problem is a Fenwick problem.
- **Sparse table** ([[sparse-table]]). Static range min or max in O(1). It
  overlaps segments instead of tiling them, which is only allowed when gluing a
  value with itself changes nothing (min, max, gcd, but not sum).
- **Sqrt decomposition** ([[sqrt-decomposition]]). One level of blocks. Easier
  to adapt to strange operations, slower by a factor of √n / log n.
- **Ordered set / balanced BST** ([[ordered-set]]). Rank and k-th queries on a
  changing set. A segment tree over compressed values answers the same questions
  if every value is known in advance; an ordered set does not need that.
- **Merge sort for inversions** ([[inversion-count]]). Counting inversions once
  is a merge sort; counting under updates, or counting "smaller to the left" for
  every position, is the Fenwick tree over compressed values.

## Variations

Eight variations, from the everyday to the rare. Each says what changes and
why, with a small example and a bank problem where one exists.

### A. A different glue: min, max, OR, gcd, count

**What changes:** the operation in the "repair" line and the identity in the
disjoint case. Nothing else.

**Why:** the proof only used associativity and an identity.

**Example:** [[p:capital-one-dynamic-wall-range-query|Dynamic Wall Building and Range Query]].
Leaf i stores 1 if a wall stands there, 0 otherwise; the glue is OR (or max, or
sum, all three work); `build i` sets leaf i to 1; `query l r` returns the glue
over [l, r]. Walls only appear, never disappear, so even simpler structures
would do (a sorted list of wall positions and a binary search for the first
wall at or after l), and noticing that is worth saying in an interview.

### B. A node that stores more than one number

**What changes:** a node stores a small tuple, and the glue combines two tuples.

**Why:** some answers for a segment cannot be computed from one number per
half. The question "what must each half tell the parent?" decides the tuple.

**Example 1, the weighted score.**
[[p:intuit-dynamic-weighted-range-scores|Dynamic Weighted Range Scores]] asks,
under point updates, for a[l] + 2·a[l+1] + 3·a[l+2] + ..., with weights
restarting at 1 at l. One number per node is not enough: when a left segment of
length L is glued in front of a right segment, every weight in the right
segment goes up by L. So each node stores (length, sum, weighted), and

```
glue(A, B) = (A.len + B.len,  A.sum + B.sum,  A.w + B.w + A.len * B.sum)
```

The A.len · B.sum term is "B's elements all moved L places to the right, so each
gains L more copies of itself". Check on [2, 3, 4]: A = [2] gives (1, 2, 2);
B = [3, 4] gives (2, 7, 3 + 8 = 11); glue gives (3, 9, 2 + 11 + 1·7 = 20), and
2 + 2·3 + 3·4 = 20. This glue is not commutative: A must be on the left.

**Example 2, the maximum subarray inside a range.**
[[p:inmobi-range-maximum-subarray-sum-queries|Range Maximum Subarray Sum Queries]]
needs, per node, (sum, best prefix, best suffix, best). The best subarray of a
glued segment is the best of the left, the best of the right, or one that
crosses the middle: left's best suffix plus right's best prefix. That is
[[kadane]] made mergeable.

```python run
def leaf(x):
    return (1, x, x)                                   # (len, sum, weighted)

def glue(A, B):                                        # A is on the left
    return (A[0] + B[0], A[1] + B[1], A[2] + B[2] + A[0] * B[1])

def build(t, a, node, lo, hi):
    if lo == hi:
        t[node] = leaf(a[lo]); return
    mid = (lo + hi) // 2
    build(t, a, 2 * node, lo, mid); build(t, a, 2 * node + 1, mid + 1, hi)
    t[node] = glue(t[2 * node], t[2 * node + 1])

def update(t, node, lo, hi, i, x):
    if lo == hi:
        t[node] = leaf(x); return
    mid = (lo + hi) // 2
    if i <= mid: update(t, 2 * node, lo, mid, i, x)
    else:        update(t, 2 * node + 1, mid + 1, hi, i, x)
    t[node] = glue(t[2 * node], t[2 * node + 1])

def query(t, node, lo, hi, l, r):                      # None means "nothing"
    if r < lo or hi < l:
        return None
    if l <= lo and hi <= r:
        return t[node]
    mid = (lo + hi) // 2
    A = query(t, 2 * node, lo, mid, l, r)
    B = query(t, 2 * node + 1, mid + 1, hi, l, r)
    return B if A is None else A if B is None else glue(A, B)

a = [2, 3, 4]                                          # the bank example, 0-based here
t = [None] * 12
build(t, a, 1, 0, 2)
first = query(t, 1, 0, 2, 0, 2)[2]
update(t, 1, 0, 2, 1, 1)
second = query(t, 1, 0, 2, 1, 2)[2]
print("score of [2,3,4] =", first, "; after a[1]=1, score of [1,4] =", second)
assert (first, second) == (20, 9)

def brute(a, l, r):
    return sum((k + 1) * a[l + k] for k in range(r - l + 1))

import random
rng = random.Random(11)
a = [rng.randint(-20, 20) for _ in range(25)]
t = [None] * 100
build(t, a, 1, 0, 24)
for _ in range(2000):
    i = rng.randrange(25); a[i] = rng.randint(-20, 20); update(t, 1, 0, 24, i, a[i])
    l = rng.randrange(25); r = rng.randrange(l, 25)
    assert query(t, 1, 0, 24, l, r)[2] == brute(a, l, r)
print("2000 random update+query pairs: weighted glue == brute force")
assert glue(leaf(3), leaf(4)) != glue(leaf(4), leaf(3))   # order matters
```

Note the identity: there is no tuple that acts as "nothing" for this glue in an
obvious way, so the code uses None and teaches the query to skip it. That is the
safe habit for every tuple-valued tree.

### C. A Fenwick tree for prefix sums

**What changes:** half the nodes are thrown away, the tree is stored in n + 1
slots, and the walk is driven by the lowest set bit of the index.

**Why:** if every query is a prefix sum(0..r), and a range is
prefix(r) - prefix(l-1), then a node's right child is never needed: its sum
is parent - left, and subtraction is available for sums. A prefix that ends
inside a right child takes the whole left sibling and continues inside the
right one, so it never needs the right child's own stored sum. Drop every right child and n nodes
remain, one per index. Number them so that node i (1-based) covers the segment
(i - lowbit(i), i], where lowbit(i) = i & -i is the value of i's lowest set bit
([[bit-manipulation]]).

For the running example, 1-based:

| i | binary | lowbit | covers | tree[i] |
|---|---|---|---|---|
| 1 | 0001 | 1 | a1 | 5 |
| 2 | 0010 | 2 | a1..a2 | 13 |
| 3 | 0011 | 1 | a3 | 6 |
| 4 | 0100 | 4 | a1..a4 | 22 |
| 5 | 0101 | 1 | a5 | 2 |
| 6 | 0110 | 2 | a5..a6 | 9 |
| 7 | 0111 | 1 | a7 | 2 |
| 8 | 1000 | 8 | a1..a8 | 39 |

<svg viewBox="0 0 700 220" role="img" aria-label="Fenwick tree ranges for indices 1 to 8: each index i owns a bar ending at i whose length is the lowest set bit of i; the bars for 7, 6 and 4 are shaded because prefix of 7 is tree 7 plus tree 6 plus tree 4">
  <g>
    <text x="10" y="205">index</text>
    <text x="95" y="205" text-anchor="middle">1</text>
    <text x="175" y="205" text-anchor="middle">2</text>
    <text x="255" y="205" text-anchor="middle">3</text>
    <text x="335" y="205" text-anchor="middle">4</text>
    <text x="415" y="205" text-anchor="middle">5</text>
    <text x="495" y="205" text-anchor="middle">6</text>
    <text x="575" y="205" text-anchor="middle">7</text>
    <text x="655" y="205" text-anchor="middle">8</text>
    <rect x="58" y="150" width="74" height="30" rx="3"/>
    <text x="95" y="170" text-anchor="middle">t1 = 5</text>
    <rect x="218" y="150" width="74" height="30" rx="3"/>
    <text x="255" y="170" text-anchor="middle">t3 = 6</text>
    <rect x="378" y="150" width="74" height="30" rx="3"/>
    <text x="415" y="170" text-anchor="middle">t5 = 2</text>
    <rect class="fill" x="538" y="150" width="74" height="30" rx="3"/>
    <text x="575" y="170" text-anchor="middle">t7 = 2</text>
    <rect x="58" y="110" width="154" height="30" rx="3"/>
    <text x="135" y="130" text-anchor="middle">t2 = 13</text>
    <rect class="fill" x="378" y="110" width="154" height="30" rx="3"/>
    <text x="455" y="130" text-anchor="middle">t6 = 9</text>
    <rect class="fill" x="58" y="70" width="314" height="30" rx="3"/>
    <text x="215" y="90" text-anchor="middle">t4 = 22</text>
    <rect x="58" y="30" width="634" height="30" rx="3"/>
    <text x="375" y="50" text-anchor="middle">t8 = 39</text>
  </g>
</svg>

**Prefix query: strip the lowest bit.** prefix(7) starts at i = 7 (covers a7),
then i = 7 - 1 = 6 (covers a5..a6), then i = 6 - 2 = 4 (covers a1..a4), then
i = 4 - 4 = 0, stop. Sum 2 + 9 + 22 = 33, and 5 + 8 + 6 + 3 + 2 + 7 + 2 = 33.
The pieces tile 1..7 because each step jumps exactly to just before the start of
the piece it took. The number of steps is the number of set bits of i, at most
log2(n) + 1.

**Point update: add the lowest bit.** Adding 7 to a4 (the `set 3 10` from
before, 0-based index 3) must touch every piece that covers position 4: i = 4,
then 4 + 4 = 8, then 16 > 8, stop. tree[4] becomes 29, tree[8] becomes 46.
Adding lowbit moves to the next piece whose segment reaches back over position
i, and there is one per level.

**The subtle line of the Fenwick tree: why 1-based.** At i = 0, lowbit(0) is
0 & -0 = 0. An update loop `while i <= n: tree[i] += d; i += i & -i` at i = 0
adds 0 forever. A Fenwick tree with 0-based indices is an infinite loop on the
first update of index 0. Shift every index up by one at the boundary
(`add(i + 1, d)`), and keep slot 0 unused.

**Point update in a Fenwick tree is "add", not "set".** To set a[i] = v, keep a
copy of the array and add v - a[i]. The tree stores sums of differences; it has
no way to overwrite.

**When a Fenwick tree is not enough.** Range max with arbitrary updates: max is
not invertible (the [5, 1, 2] counterexample), so prefix(r) "minus"
prefix(l-1) is meaningless. Use a segment tree.

### D. Coordinate compression before counting

**What changes:** the tree's index is not a position in the input, but the rank
of a value among all values.

**Why:** many counting questions are about values, not positions. "How many
earlier elements are smaller than x" is a range query over *values*: count
of seen values in [min, x-1]. Index an array by value, store a count at each
value, and that is a sum query. But values go up to 10^9 and an array of 10^9
counts does not exist. Only the *order* of the values matters, so replace each
value by its rank among the distinct values: at most n distinct ranks, an array
of size n.

**Example:** [[p:tcs-count-smaller-prior-elements|Count Smaller Prior Elements]],
nums = [5, 2, 6, 1, 3]. Distinct sorted values [1, 2, 3, 5, 6], so the ranks are
1→1, 2→2, 3→3, 5→4, 6→5 (1-based, for the Fenwick tree). Walk left to right; for
each value, ask how many seen values have rank below its rank, then add it.

| step | x | rank | seen ranks before | count of ranks < rank | answer |
|---|---|---|---|---|---|
| 1 | 5 | 4 | {} | 0 | 0 |
| 2 | 2 | 2 | {4} | 0 | 0 |
| 3 | 6 | 5 | {4, 2} | 2 | 2 |
| 4 | 1 | 1 | {4, 2, 5} | 0 | 0 |
| 5 | 3 | 3 | {4, 2, 5, 1} | 2 (ranks 1, 2) | 2 |

Output [0, 0, 2, 0, 2], which matches the bank's expected answer. Strictness
lives in one place: "smaller" queries prefix(rank - 1), so equal values (the
same rank) are not counted. "Smaller or equal" would query prefix(rank).

The same machine, pointed differently, gives a family:

- **Inversions.** For each element, count earlier elements that are *greater*:
  (number seen so far) - prefix(rank). Total over all positions.
  [[p:tcs-count-array-inversions|Count Array Inversions]]; merge sort does it
  too ([[inversion-count]]).
- **Minimum adjacent swaps.**
  [[p:epic-minimum-adjacent-transpositions|Minimum Adjacent Transpositions]]:
  replace each character of source by the position its copy must reach in
  target (k-th occurrence to k-th occurrence), and the number of adjacent swaps
  is the number of inversions of that sequence. "GUM" to "MUG": G→2, U→1, M→0,
  sequence [2, 1, 0], three inversions, answer 3.
- **Triplets.** [[p:airbnb-count-decreasing-triplets|Count Decreasing Triplets]]:
  for each middle j, (greater elements to its left) × (smaller elements to its
  right). One Fenwick sweep left to right, one right to left.
- **k-th largest in a growing multiset.**
  [[p:google-dynamic-kth-largest|Dynamic K-th Largest Queries]]: counts per rank,
  and "find the k-th" walks down the tree, going left or right by comparing k
  with the left child's count (variation G). This needs every value in advance,
  so read all the operations first.

```python run
from bisect import bisect_left

class Fenwick:
    def __init__(self, n):
        self.n, self.t = n, [0] * (n + 1)          # slot 0 unused
    def add(self, i, d, path=None):                # 1-based i
        while i <= self.n:
            if path is not None: path.append(i)
            self.t[i] += d
            i += i & -i                            # next piece that covers i
    def prefix(self, i, path=None):                # sum of a1..ai
        s = 0
        while i > 0:
            if path is not None: path.append(i)
            s += self.t[i]
            i -= i & -i                            # jump before this piece
        return s

a = [5, 8, 6, 3, 2, 7, 2, 6]
f = Fenwick(8)
for i, x in enumerate(a):
    f.add(i + 1, x)
print("tree[1..8] =", f.t[1:])
assert f.t[1:] == [5, 13, 6, 22, 2, 9, 2, 39]
p = []; s = f.prefix(7, p)
print("prefix(7) visits", p, "=", s)
assert p == [7, 6, 4] and s == 33 == sum(a[:7])
p = []; f.add(4, 7, p)
print("add(4, +7) visits", p, "; tree[4], tree[8] =", f.t[4], f.t[8])
assert p == [4, 8] and (f.t[4], f.t[8]) == (29, 46)

i, steps = 0, 0                                    # the 0-based bug, bounded
while i <= 8 and steps < 5:
    i += i & -i; steps += 1
print("from i = 0 the update loop is still at i =", i, "after", steps, "steps")
assert i == 0

def count_smaller_before(nums):
    vals = sorted(set(nums))                       # compress: value -> rank
    f, out = Fenwick(len(vals)), []
    for x in nums:
        r = bisect_left(vals, x) + 1               # 1-based rank
        out.append(f.prefix(r - 1))                # strictly smaller ranks
        f.add(r, 1)
    return out

print(count_smaller_before([5, 2, 6, 1, 3]), count_smaller_before([2, 2, 2]))
assert count_smaller_before([5, 2, 6, 1, 3]) == [0, 0, 2, 0, 2]
assert count_smaller_before([2, 2, 2]) == [0, 0, 0]

def inversions(seq):
    vals = sorted(set(seq)); f = Fenwick(len(vals)); inv = 0
    for seen, x in enumerate(seq):
        r = bisect_left(vals, x) + 1
        inv += seen - f.prefix(r)                  # earlier and strictly greater
        f.add(r, 1)
    return inv

assert inversions([2, 4, 1, 3, 5]) == 3            # the bank example
assert inversions([2, 1, 0]) == 3                  # GUM -> MUG
assert inversions([2, 3, 0, 1]) == 4               # aabb -> bbaa
import random
rng = random.Random(5)
for _ in range(300):
    s = [rng.randint(-10**9, 10**9) % 7 for _ in range(rng.randint(1, 12))]
    assert count_smaller_before(s) == [sum(s[j] < s[i] for j in range(i)) for i in range(len(s))]
print("compressed Fenwick counts agree with brute force on 300 arrays")
```

**The compression trap.** Compress *every* coordinate that will ever be used as
an index, including the ones that only queries mention. If a query asks about a
value that never appears in the data, it still needs a rank (or a `bisect` that
finds where it would go).

### E. Range update, point query: a difference array in a Fenwick tree

**What changes:** store differences instead of values. "Add v to every index in
[l, r]" becomes two point updates, +v at l and -v at r + 1. The value at index
i is the prefix sum of the differences up to i.

**Why:** this is the [[prefix-sums]] difference-array trick, made dynamic. The
Fenwick tree does the prefix sum, and point updates to the difference array
are exactly what it supports.

**Example:**
[[p:google-dynamic-point-range-coverage|Dynamic Point-in-Range Queries]]:
insert closed intervals, then ask whether a point is covered. Insert [l, r] is
+1 at l, -1 at r + 1; a point is covered if its prefix sum is positive. If the
coordinates are large, read all operations first and compress the l, r + 1 and
query points together. Three lines: [1,5] gives +1 at 1, -1 at 6; point 3 has
prefix 1 (covered); point 6 has prefix 0 (not covered).

### F. Range update, range query: lazy propagation

**What changes:** each node gets a second field, a **pending tag**: "every value
in my segment must still receive +v, and my children have not been told". A
range update stops at fully covered nodes, as a query does, and leaves a tag
there instead of walking to the leaves.

**Why:** without tags, "add 5 to [0, n-1]" changes every leaf, n updates of
log n each. But a fully covered node does not need its children to be correct
*yet*; it only needs its own sum to be correct, which is sum + v × length. The
children are told later, only if some operation goes below this node. That
later moment is the **push**: before descending from a node, hand its tag to
both children (each updates its sum and adds to its own tag) and clear it.

This is the whole of [[lazy-propagation]], and its subtle line is the push. It
is demonstrated both ways in *Traps*, with a hand trace in *Check yourself*.

**Example:** [[p:uber-streaming-interval-peak-concurrency|Streaming Interval Peak Concurrency]].
Each arriving interval [s, e) adds 1 to every time in it; after each arrival,
report the maximum over the whole timeline. Compress all endpoints (the
intervals can be read in advance), keep a max tree with an "add" tag, and the
answer is the root. Here the glue is max, the tag is +v, and applying the tag to
a node is max += v (every value in the segment rises by v, so the maximum does
too).

What tags must satisfy: applying a tag to a node must be computable from the
node's stored value and length alone, and two tags must compose into one tag.
"Add v" composes by adding. "Assign v" composes by keeping the newer one, and
an assign arriving on top of an add replaces it. Mixing assign and add needs a
rule for the order, and that rule is where bugs go.
[[p:walmart-range-module|Range Module]] (add, remove and query ranges of
tracked points) is assign-tags over compressed coordinates.

### G. Walking down the tree: the first index where something holds

**What changes:** instead of answering a range, the query descends from the
root, choosing one child per level.

**Why:** if each node stores a count, then "the k-th smallest" is: at a node,
if the left child holds at least k values, the answer is in the left; otherwise
subtract the left count from k and go right. One path, O(log n), no binary search
around the tree. The same walk finds "the first index with value at least x"
with a max tree: go left if the left child's max is at least x. Combining a
[[binary-search]] with range queries would cost O(log² n); walking the tree is
O(log n).

**Example:** [[p:google-dynamic-kth-largest|Dynamic K-th Largest Queries]], on
counts over compressed values. A Fenwick tree has an equivalent walk by powers
of two.

### H. The rare ones

These appear in hard rounds and rarely in OAs. Know they exist.

- **Merge-sort tree:** each node stores its segment's values sorted; "how many
  values in a[l..r] are below x" is O(log² n), with no updates.
- **Persistent segment tree** ([[persistent-structures]]): an update copies only
  the log n path, so every past version remains queryable.
- **2-D trees:** a tree of trees for rectangle sums; usually a 2-D Fenwick.
- **Segment tree on an Euler tour:** subtree updates and queries on a rooted
  tree become range updates and queries, because a subtree is a contiguous range
  of the DFS order. [[p:pinterest-subtree-access-overrides|Subtree Access Overrides]]
  is this shape: grant or deny a whole subtree, check one node.
- **Dynamic (sparse) segment tree:** nodes created only when touched, for huge
  coordinates that cannot be compressed because they are not known in advance.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **Two kinds of operation interleaved: one changes the data, one asks about a
   range.** "Process q operations: update ... / query ...". This is the
   strongest signal there is. Dynamic Wall Building, Dynamic Weighted Range
   Scores.
2. **n and q both around 10^5 to 2·10^5.** O(nq) is 10^10 and O((n + q) log n)
   is a few million. The constraint is telling you the log.
3. **"For each element, how many earlier (or later) elements are smaller /
   greater".** A count over values while sweeping positions: a Fenwick tree over
   compressed values. Count Smaller Prior Elements, inversions, triplets.
4. **"Add v to every element in [l, r]" next to "report the sum / max of
   [l, r]".** Lazy propagation.
5. **"Minimum adjacent swaps".** Inversions in disguise.
6. **"k-th smallest / largest" with insertions mixed in.** A count tree with a
   walk, or an ordered set.
7. **Intervals arriving one by one, with "after each one, report...".** Range
   updates over compressed time.

The disguises, with the step that reveals them:

- **"How many earlier values are smaller"** becomes a range query once you index
  by value: the range is [smallest rank, rank(x) - 1].
- **"Minimum adjacent swaps to turn s into t"** becomes inversions once you
  replace each character by its target position.
- **"Is point p covered by any interval inserted so far"** becomes a point query
  on a difference array.
- **"Subtree of v"** becomes a range [tin[v], tout[v]] once you number the nodes
  in DFS order.

### Anti-signals: looks like a segment tree, is not

- **"Range sum" with no updates.** Prefix sums. A tree is a log factor and fifty
  lines of risk for nothing.
- **"Range min" with no updates.** A sparse table, or offline tricks.
- **"Max of the last k elements" with a fixed k and time moving forward.** A
  monotonic deque.
- **Updates that only ever append, and queries over a suffix.** Often a stack or
  a deque suffices.
- **The "range" is a range of values on a static set.** Sort once and binary
  search.
- **The query is about a whole-array property after a global operation.** For
  [[p:doordash-adjust-prices|Adjust Prices]], "raise every price below v to v"
  is a global floor; a single running floor plus the time of each item's last
  point update answers it without any tree. Look for the global shortcut before
  building range machinery.

## Traps

**The identity in the disjoint case.** Returning 0 from a max or min tree.
Symptom: correct on non-negative inputs, wrong on negative ones, an answer that
is not in the array. Demonstrated in *From the idea to the code*.

**Sizing the array 2n for the recursive layout.** Symptom: IndexError for some
n (6, for instance) and not for others. Use 4n, or the bottom-up layout, which
needs exactly 2n.

**Inconsistent mid.** Computing mid differently in build and query. Symptom:
answers for the wrong segments, usually off by one element.

**Inclusive vs half-open ranges.** A tree written for [l, r] called with
[l, r). Symptom: every answer misses or includes the last element.

**Recomputing the parent before the child.** Symptom: the root is one update
behind.

**Fenwick at index 0.** Symptom: the first update hangs. Shift to 1-based.

**Fenwick "set".** Calling add(i, v) to set a[i] = v. Symptom: values
accumulate. Add v - a[i] and keep a copy of a.

**Strict vs non-strict in counting.** prefix(rank) counts equal values;
prefix(rank - 1) does not. Symptom: wrong only on inputs with duplicates, like
[2, 2, 2].

**Forgetting coordinates that only queries use.** Symptom: KeyError, or a
query value mapped to a wrong rank.

**Forgetting to push the lazy tag.** The big one. A range update leaves a tag at
a fully covered node and stops. Later, an operation that only partly covers
that node descends into its children, whose sums never heard about the tag. Two
symptoms, depending on where the push is missing:

- missing in the **query**: the children are stale, so a query that goes below
  the tagged node reads old values;
- missing in the **update**: the update descends, changes a child, and then
  recomputes the parent as left + right from children that never received the
  tag. The parent's own correct sum is overwritten by a wrong one, and the tag's
  effect disappears from the whole tree.

Here is the tree on eight zeros. Add 5 to [0,7]: the root is fully covered, so
the root gets sum 40 and tag 5, and nothing below it changes. Then query [0,3].

| node | right (with push) | wrong (no push) |
|---|---|---|
| [0,7], partial for [0,3] | push: [0,3] gets sum 20 tag 5, [4,7] gets sum 20 tag 5 | no push |
| [0,3], full | returns **20** | returns **0**: its sum was never updated |

```python run
class Lazy:
    def __init__(self, n, push=True):
        self.n, self.s, self.z, self.do_push = n, [0] * (4 * n), [0] * (4 * n), push

    def _apply(self, node, lo, hi, v):           # every value in [lo,hi] += v
        self.s[node] += v * (hi - lo + 1)
        self.z[node] += v                        # children still owe v

    def _push(self, node, lo, hi):
        if self.do_push and self.z[node]:
            mid = (lo + hi) // 2
            self._apply(2 * node, lo, mid, self.z[node])
            self._apply(2 * node + 1, mid + 1, hi, self.z[node])
            self.z[node] = 0

    def add(self, l, r, v, node=1, lo=0, hi=None):
        hi = self.n - 1 if hi is None else hi
        if r < lo or hi < l: return
        if l <= lo and hi <= r:
            self._apply(node, lo, hi, v); return   # stop here, leave a tag
        self._push(node, lo, hi)                   # THE LINE
        mid = (lo + hi) // 2
        self.add(l, r, v, 2 * node, lo, mid); self.add(l, r, v, 2 * node + 1, mid + 1, hi)
        self.s[node] = self.s[2 * node] + self.s[2 * node + 1]

    def query(self, l, r, node=1, lo=0, hi=None):
        hi = self.n - 1 if hi is None else hi
        if r < lo or hi < l: return 0
        if l <= lo and hi <= r: return self.s[node]
        self._push(node, lo, hi)                   # THE LINE again
        mid = (lo + hi) // 2
        return self.query(l, r, 2 * node, lo, mid) + self.query(l, r, 2 * node + 1, mid + 1, hi)

for push in (True, False):
    t = Lazy(8, push)
    t.add(0, 7, 5)
    q1 = t.query(0, 3)                             # query below a tag
    t.add(0, 0, 1)                                 # update below a tag
    q2 = t.query(0, 7)
    print("push" if push else "no push", ": sum[0,3] =", q1, " then after +1 at 0, sum[0,7] =", q2)
    assert (q1, q2) == ((20, 41) if push else (0, 1))

for push in (True, False):                         # the hand trace in Check yourself
    t = Lazy(4, push); t.add(0, 3, 3); t.add(1, 2, 2)
    assert t.query(0, 1) == (8 if push else 2)

import random
rng = random.Random(9)
for _ in range(200):
    n = rng.randint(1, 20); a = [0] * n; t = Lazy(n)
    for _ in range(30):
        l = rng.randrange(n); r = rng.randrange(l, n); v = rng.randint(-5, 5)
        t.add(l, r, v)
        for k in range(l, r + 1): a[k] += v
        l = rng.randrange(n); r = rng.randrange(l, n)
        assert t.query(l, r) == sum(a[l:r + 1])
print("with the push: 200 random runs agree with brute force")
```

Look at what the no-push version reported after `add(0, 0, 1)`: the sum of the
whole array is 1. The update descended through the root (partial cover), changed
leaf 0, and recomputed the root as the sum of its children, which had never
received the 5s. The 40 is gone. Said the other way round: a tag is a debt the
node owes its children, and you must pay the debt before you look at, or
change, anything below it.

**Tags that do not compose.** Adding an "assign" tag on top of a pending "add"
tag and keeping both, in the wrong order. Symptom: a range that was assigned
still shows an old addition. Decide the composition rule before you write
`_apply`.

## What to memorise

**The sentence.** Precompute the halving segments; a range is at most two of
them per level, an index is in one per level.

**The template**, recursive, three cases in the query:

```
if r < lo or hi < l:      return IDENTITY
if l <= lo and hi <= r:   return t[node]
push(node)                                  # only with lazy tags
return glue(query(left half), query(right half))
```

and update as "down to the leaf, then glue on the way up".

**The Fenwick pair**, 1-based: update `i += i & -i`, prefix `i -= i & -i`.

**The habit.** Before coding, write the four lines: the index, what a node
stores, the glue with its identity, and what an update does. If any of the four
is unclear, the tree is not designed yet.

**Numbers worth carrying.** 2n - 1 nodes; 4n slots for the recursive layout;
height about 18 for n = 2·10^5; at most four visits per level per query.

## Check yourself

:::check
Build the sum tree for a = [2, 1, 4, 3, 5, 0] (n = 6, mid = (lo + hi) // 2).
Write every node's segment and sum. Then trace `sum 1 4`: list every node the
query visits, with its case (none, full, partial), and the answer. Then apply
`set 4 1` and list the nodes that change.
--
Nodes: [0,5] = 15; [0,2] = 7, [3,5] = 8; [0,1] = 3, [2,2] = 4, [3,4] = 8,
[5,5] = 0; leaves [0,0] = 2, [1,1] = 1, [3,3] = 3, [4,4] = 5.

Query [1,4]: [0,5] partial → [0,2] partial → [0,1] partial → [0,0] none (0),
[1,1] full (1); [2,2] full (4); [3,5] partial → [3,4] full (8); [5,5] none (0).
Nine visits, three nodes used: 1 + 4 + 8 = 13, which is 1 + 4 + 3 + 5.

`set 4 1`: the path is [0,5] → [3,5] → [3,4] → [4,4]. New values bottom-up:
[4,4] = 1, [3,4] = 3 + 1 = 4, [3,5] = 4 + 0 = 4, [0,5] = 7 + 4 = 11. Four nodes,
one per level, which is ceil(log2 6) + 1 = 4.
:::

:::check
Fenwick tree by hand, 1-based, a = [3, 1, 4, 1, 5, 9]. Fill tree[1..6] using
"tree[i] covers (i - lowbit(i), i]". Compute prefix(6) and prefix(5) by listing
the indices visited. Then do add(3, +2), listing the indices it touches, and
compute sum(2..5).
--
lowbits: 1, 2, 1, 4, 1, 2. tree[1] = 3, tree[2] = 3 + 1 = 4, tree[3] = 4,
tree[4] = 3 + 1 + 4 + 1 = 9, tree[5] = 5, tree[6] = 5 + 9 = 14.

prefix(6): 6 → 6 - 2 = 4 → 4 - 4 = 0. tree[6] + tree[4] = 14 + 9 = 23, the sum
of everything. prefix(5): 5 → 4 → 0, 5 + 9 = 14 = 3 + 1 + 4 + 1 + 5.

add(3, +2): 3 → 3 + 1 = 4 → 4 + 4 = 8 > 6, stop. tree[3] = 6, tree[4] = 11.

sum(2..5) = prefix(5) - prefix(1) = (tree[5] + tree[4]) - tree[1] =
(5 + 11) - 3 = 13, and the array is now [3, 1, 6, 1, 5, 9], so 1 + 6 + 1 + 5 = 13.
:::

:::check
Lazy propagation by hand. n = 4, all zeros, a range-add / range-sum tree with
nodes [0,3]; [0,1], [2,3]; and four leaves. Do `add 0 3 +3`, then `add 1 2 +2`,
then `query 0 1`. Write each node's (sum, tag) after each operation. Then redo
it with the push removed and find the moment the answer goes wrong.
--
With the push. After `add 0 3 +3`: the root is fully covered: [0,3] = (12, 3);
nothing else changes.

`add 1 2 +2`: the root is partial, so push first: [0,1] = (6, 3),
[2,3] = (6, 3), root tag 0. [0,1] is partial: push: [0,0] = (3, 3),
[1,1] = (3, 3), [0,1] tag 0. [0,0] none; [1,1] full: (5, 5). Recompute
[0,1] = 3 + 5 = 8. Symmetrically [2,3]: push, [2,2] full → (5, 5), [3,3] stays
(3, 3), [2,3] = 8. Root = 8 + 8 = 16, which is 3 + 5 + 5 + 3.

`query 0 1`: the root is partial (push does nothing, tag is 0); [0,1] is full:
8. Correct: 3 + 5.

Without the push. After the first add: root (12, 3), children still (0, 0).
The second add descends into [0,1] without handing over the 3s: [1,1] becomes
2, [0,1] = 0 + 2 = 2; [2,2] becomes 2, [2,3] = 2; then the root is recomputed
from its children as 4, and the 12 is lost. The answer goes wrong at that
recompute: `query 0 1` returns [0,1]'s 2 instead of 8. The run block in *Traps*
asserts both numbers.
:::

:::check
Why can a Fenwick tree answer range sums but not range maxima under arbitrary
point updates, when a segment tree answers both?
--
A Fenwick tree only stores prefix-shaped pieces, so a range [l, r] has to be
computed as "prefix(r) with prefix(l-1) removed". Removing needs an inverse:
for sums it is subtraction. Max has no inverse. With a = [5, 1, 2], the prefix
maxima are 5, 5, 5, and max(a[1..2]) = 2 cannot be produced from any of them,
because the 5 hid everything after it.

A segment tree never removes anything. It tiles the range with segments that
lie entirely inside it and glues them, which needs only associativity and an
identity. That is why it handles max, min, gcd and the tuple-valued nodes, and
the Fenwick tree does not. (A Fenwick tree can do prefix maxima when values only
increase, because then nothing ever needs removing, but that is a special case.)
:::

:::check
Someone says: "There are 2n - 1 nodes, so a list of size 2n is enough for the
recursive tree with children 2k and 2k + 1." Where are they wrong?
--
The count is right and the conclusion is wrong. The 2k, 2k+1 numbering is the
numbering of a *complete* binary tree, and when n is not a power of two the
tree is not complete: some leaves are deeper than others, and the numbers of
the missing positions are skipped but still used up. For n = 6, root [0,5] is
node 1, [3,5] is node 3, [3,4] is node 6, and its children [3,3] and [4,4] are
nodes 12 and 13. Node 13 is past a list of length 12.

The safe bound is 2·2^ceil(log2 n), which is less than 4n. Or use the bottom-up
layout, which does use exactly 2n slots, because it numbers only the nodes that
exist.
:::

:::check
Reduce this to something in this chapter, and give the answer for the example.
"Given strings source = 'aabb' and target = 'bbaa' with the same letters, return
the minimum number of swaps of adjacent characters that turn source into
target."
--
Each adjacent swap fixes at most one pair that is in the wrong relative order,
and a pair in the right order never needs to be swapped. So the answer is the
number of pairs that are in the wrong order, the inversions, once you know
where every character must go.

Assign the k-th 'a' of source to the k-th 'a' of target (this never crosses two
equal letters, which would waste swaps), and the same for 'b'. Source positions
0, 1 are 'a', which go to target positions 2, 3; source positions 2, 3 are 'b',
which go to target positions 0, 1. The sequence of destinations is
[2, 3, 0, 1]. Its inversions: (2,0), (2,1), (3,0), (3,1), four. The answer is 4,
which matches the bank's example for Minimum Adjacent Transpositions.

For n = 2·10^5 count the inversions with a Fenwick tree over the destinations
(already 0..n-1, so no compression needed), or with merge sort.
:::
