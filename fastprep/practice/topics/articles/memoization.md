# Memoisation vs Tabulation

> Memoisation is not a trick for speeding up recursion. It is the claim that
> your recursive function is a *function* — same arguments, same answer, every
> time — and that claim is what collapses an exponential tree of calls into a
> linear walk over a graph.

## When you reach for it

Four hundred and twenty-three problems in this bank are dynamic programming,
which puts the method at #11 of 150 topics. Every one of them can be solved in
either of two ways, and the choice is almost never about correctness. You reach
for this chapter once you already have a recurrence — [[dynamic-programming]]
is where the recurrence comes from, [[state-design]] is where you decide what
the arguments are — and now have to decide whether to write it as a recursion
that caches, or as a loop that fills a table.

The trigger for **memoisation (top-down)** is: *I can write the brute-force
recursion, and I would rather not think about the order.* You write the
recursion you would have written anyway, add a dictionary, and the machine
works out the order for you. This is the right default when the state is a
tuple of unlike things — an index, a remaining capacity, a bitmask, a last
choice — as in *0/1 Knapsack* or *Alphanumeric Combinations*, because the
enumeration order of such a state space is not obvious and getting it wrong
costs you the problem.

The trigger for **tabulation (bottom-up)** is: *I know the order, I need every
cell anyway, and either the input is big or the recursion would be deep.*
*Pascal's Triangle* is the extreme case: the table **is** the answer, so
building it lazily would be perverse. *Maximum Subarray* and *Best Time to Buy
and Sell Stock* are the other extreme: one state per index and a table of two
variables, where a dictionary and a recursion cost far more than the loop they
replace — and with `prices.length` up to 200,000, the recursion would overflow
Python's stack long before the time limit.

Both are wrong when the recursion is not a function of its arguments. If the
answer depends on *how you got here* — a path already walked, a set already
visited, a running best updated as a side effect — there is nothing to cache,
because the same arguments genuinely do deserve different answers. That is
[[backtracking]], and bolting a memo onto it produces confident nonsense. The
other anti-signal is the absence of overlap: [[merge-sort]] and
[[divide-and-conquer|divide and conquer]] in general recurse on *disjoint*
subproblems, so a cache never gets a hit and costs you memory and hashing for
nothing.

## The idea

Draw the calls your recursion makes. It is a tree. Now notice that many of its
nodes carry the same label, and a node's label determines its entire subtree.
Glue the identical nodes together. The tree becomes a directed acyclic graph,
and the whole method is: **do the work once per node of that graph, not once
per path through it.**

<svg viewBox="0 0 740 230" role="img" aria-label="a recursion tree with repeated subtrees on the left, and the same computation as a directed acyclic graph of five states on the right">
  <g>
    <circle cx="170" cy="30" r="14"/>
    <text x="170" y="35" text-anchor="middle">4</text>
    <circle cx="70" cy="100" r="14"/>
    <text x="70" y="105" text-anchor="middle">3</text>
    <circle class="fill" cx="170" cy="100" r="14"/>
    <text x="170" y="105" text-anchor="middle">2</text>
    <circle cx="270" cy="100" r="14"/>
    <text x="270" y="105" text-anchor="middle">1</text>
    <circle class="fill" cx="25" cy="170" r="14"/>
    <text x="25" y="175" text-anchor="middle">2</text>
    <circle cx="70" cy="170" r="14"/>
    <text x="70" y="175" text-anchor="middle">1</text>
    <circle cx="115" cy="170" r="14"/>
    <text x="115" y="175" text-anchor="middle">0</text>
    <circle cx="160" cy="170" r="14"/>
    <text x="160" y="175" text-anchor="middle">1</text>
    <circle cx="205" cy="170" r="14"/>
    <text x="205" y="175" text-anchor="middle">0</text>
    <circle cx="270" cy="170" r="14"/>
    <text x="270" y="175" text-anchor="middle">0</text>
    <line x1="160" y1="43" x2="80" y2="88"/>
    <line x1="170" y1="44" x2="170" y2="86"/>
    <line x1="180" y1="43" x2="260" y2="88"/>
    <line x1="62" y1="113" x2="33" y2="157"/>
    <line x1="70" y1="114" x2="70" y2="156"/>
    <line x1="78" y1="113" x2="107" y2="157"/>
    <line x1="167" y1="114" x2="163" y2="156"/>
    <line x1="177" y1="113" x2="198" y2="157"/>
    <line x1="270" y1="114" x2="270" y2="156"/>
    <text x="25" y="205" text-anchor="middle">…</text>
    <text x="70" y="205" text-anchor="middle">…</text>
    <text x="160" y="205" text-anchor="middle">…</text>
    <text x="150" y="222">one node per path: 2ⁿ-ish</text>
    <circle cx="430" cy="100" r="14"/>
    <text x="430" y="105" text-anchor="middle">4</text>
    <circle cx="495" cy="100" r="14"/>
    <text x="495" y="105" text-anchor="middle">3</text>
    <circle class="fill" cx="560" cy="100" r="14"/>
    <text x="560" y="105" text-anchor="middle">2</text>
    <circle cx="625" cy="100" r="14"/>
    <text x="625" y="105" text-anchor="middle">1</text>
    <circle cx="690" cy="100" r="14"/>
    <text x="690" y="105" text-anchor="middle">0</text>
    <line x1="444" y1="100" x2="481" y2="100"/>
    <line x1="509" y1="100" x2="546" y2="100"/>
    <line x1="574" y1="100" x2="611" y2="100"/>
    <line x1="639" y1="100" x2="676" y2="100"/>
    <line x1="424" y1="89" x2="495" y2="58"/>
    <line x1="495" y1="58" x2="566" y2="89"/>
    <line x1="489" y1="89" x2="560" y2="58"/>
    <line x1="560" y1="58" x2="631" y2="89"/>
    <line x1="554" y1="89" x2="625" y2="58"/>
    <line x1="625" y1="58" x2="696" y2="89"/>
    <line x1="428" y1="114" x2="527" y2="150"/>
    <line x1="527" y1="150" x2="623" y2="114"/>
    <line x1="493" y1="114" x2="592" y2="150"/>
    <line x1="592" y1="150" x2="688" y2="114"/>
    <text x="560" y="185" text-anchor="middle">one node per state: 5 nodes, 9 edges</text>
    <text x="560" y="222" text-anchor="middle">the shaded state is one node, not two</text>
  </g>
</svg>

The picture on the left is `ways(4)` for *Climb Stairs with One, Two, or Three
Steps*: from step `n` you may have arrived from `n-1`, `n-2` or `n-3`, so
`ways(n) = ways(n-1) + ways(n-2) + ways(n-3)`, with `ways(0) = 1` and
`ways(n) = 0` for negative `n`. The state `2` appears twice in the tree and its
subtree is drawn twice. The picture on the right is the same computation with
identical states identified: five nodes, nine edges.

There are exactly two ways to evaluate a DAG, and they are the two halves of
this chapter's title.

**Top-down** starts at the node you care about and does a depth-first search,
computing a node's value from its successors' values, and writing each finished
value down so that the second visitor reads instead of recomputes. The cache is
the "finished" mark of the DFS.

**Bottom-up** sorts the nodes so that every node comes after everything it
depends on — a [[topological-sort]] of the DAG, usually available for free as
`for i in range(n)` — and then sweeps through them in that order with a loop.

Same graph, same values, same number of arithmetic operations. The difference
is who works out the order: the call stack, or you.

## Worked by hand

Trace `ways(5)` top-down, with `memo` a dictionary and the three recursive
calls made left to right. Negative arguments return 0 immediately and `0`
returns 1; neither is stored.

| # | what runs | outcome | `memo` after |
| --- | --- | --- | --- |
| 1 | `go(5)` | miss — descend into `go(4)` | `{}` |
| 2 | `go(4)` | miss — descend into `go(3)` | `{}` |
| 3 | `go(3)` | miss — descend into `go(2)` | `{}` |
| 4 | `go(2)` | miss — descend into `go(1)` | `{}` |
| 5 | `go(1)` | miss — descend into `go(0)` | `{}` |
| 6 | `go(0)`, `go(-1)`, `go(-2)` | base cases: 1, 0, 0 | `{}` |
| 7 | `go(1)` returns `1+0+0` | first store | `{1:1}` |
| 8 | `go(2)`: `go(0)`=1, `go(-1)`=0, sum `1+1+0` | store | `{1:1, 2:2}` |
| 9 | `go(3)`: `go(2)` **hit** 2, `go(1)` **hit** 1, `go(0)`=1 | store | `{1:1, 2:2, 3:4}` |
| 10 | `go(4)`: `go(3)` **hit** 4, `go(2)` **hit** 2, `go(1)` **hit** 1 | store | `… 4:7` |
| 11 | `go(5)`: `go(4)` returned 7, `go(3)` **hit** 4, `go(2)` **hit** 2 | store | `… 5:13` |

Answer 13. Four things there are worth a pen.

**Nothing is stored until the deepest call returns.** The memo fills in the
order 1, 2, 3, 4, 5 — bottom-up — even though the code reads top-down. That
order is precisely the loop a tabulated version would write. Memoisation does
not avoid the ordering problem; it *discovers* the order at run time, by
descending until it hits something it can answer and unwinding from there.

**Each state is computed once and read many times.** Five misses, five hits, six
base-case calls. The speedup is not that work is skipped; it is that work is
charged per *state* rather than per *path* — the 13 distinct routes through the
tree become five stores.

**The hits are not where you expect.** `go(3)` in step 9 hit on `go(2)`, a state
that was computed while `go(3)` was still on the stack, below it. A state can be
finished while its parent is unfinished. That is why you cannot reason about a
memoised recursion by looking at stack depth — the stack is a path, the memo is
a set, and they grow on different schedules.

**Base cases were visited but never stored.** `go(-1)` was answered from an
`if`, not from the dictionary. Keeping impossible states out of the key space
makes the memo smaller and the state count easier to do. Storing them is also
correct, just noisier.

## Why it is correct

The claim to prove is not "the cache is fast". It is that adding the cache
changes no answer, and that the loop version computes the same thing. Both fall
out of one induction, once the setting is stated precisely.

:::proof Memoised recursion and tabulation both compute the unique solution of the recurrence
**Setting.** Let `S` be a set of states. For each `s ∈ S` let `dep(s) ⊆ S` be a
finite set of states, and let `C` be a rule that turns `s` together with the
values at `dep(s)` into a value. Build the digraph `D` with an edge `s → t`
for each `t ∈ dep(s)`. Assume the part of `D` reachable from the query state
`q` is **finite and acyclic**.

Acyclicity lets us define `rank(s)` = the number of edges on the longest
directed path leaving `s`, a natural number, with `rank(s) = 0` exactly when
`dep(s)` is empty. Note `s → t` implies `rank(s) ≥ 1 + rank(t)`. Because `rank`
is a well-founded measure, the equations

    f(s) = C(s, (f(t))ₜ ∈ dep(s))

have exactly one solution `f` on the reachable part: `f` is determined on rank
0 by `C` alone, and determined on rank `k` once it is determined on ranks
`< k`. Call that unique `f` the *specification*.

**The program.** `solve(s)`: if `s` is in `memo`, return `memo[s]`; otherwise
compute `v = C(s, (solve(t))ₜ ∈ dep(s))`, set `memo[s] = v`, return `v`.

**Invariant (I).** Whenever control is not inside a call, every key `s` present
in `memo` satisfies `memo[s] = f(s)`.

**Base.** `memo` starts empty, so (I) holds vacuously.

**Claim.** For every reachable `s`, if (I) holds on entry to `solve(s)` then
the call terminates, returns `f(s)`, and (I) holds on exit. By strong induction
on `rank(s)`.

*Rank 0.* `dep(s)` is empty, so no recursive call is made and the body returns
`C(s)`, which is `f(s)` by the specification. It writes `memo[s] = f(s)`, which
preserves (I). If instead `s` was already in `memo`, the returned value is
`memo[s] = f(s)` by (I), and `memo` is unchanged.

*Rank k > 0.* If `s ∈ memo` the call returns `memo[s] = f(s)` by (I) and writes
nothing. Otherwise, every `t ∈ dep(s)` has `rank(t) ≤ k - 1`, so the induction
hypothesis applies to each recursive call in turn: the first returns `f(t₁)`
and re-establishes (I), which is the precondition for the second, and so on.
The body therefore computes `C(s, (f(t))ₜ)`, which is `f(s)` by the
specification, stores it — preserving (I) — and returns it.

*Termination.* Every recursive call strictly decreases `rank`, and `rank` is a
natural number, so the depth of recursion from `q` is at most `rank(q)`: no
infinite descent. The number of *misses* is at most the number of reachable
states, since a miss inserts a key that is never removed, so that state never
misses again; the total number of calls is therefore at most
`1 + Σ |dep(s)|` over reachable `s`, a finite number.

**Tabulation.** Let `s₁, …, s_N` enumerate the reachable states so that every
`t ∈ dep(sᵢ)` appears strictly before `sᵢ`. Such an order exists precisely
because `D` is finite and acyclic — it is a reverse topological order. The loop
sets `table[sᵢ] = C(sᵢ, (table[t])ₜ ∈ dep(sᵢ))` for `i = 1 … N`. By induction on
`i`: assume `table[s_j] = f(s_j)` for all `j < i`; the assignment reads only
entries with index `< i`, which are correct by hypothesis, so it stores
`C(sᵢ, (f(t))ₜ) = f(sᵢ)`.

**Conclusion.** Both programs return `f(q)`, and `f` is unique, so they agree —
and they agree with the *uncached* recursion, which is the same induction with
the memo lookups deleted. ∎
:::

Now the assumptions, in plain words, because every one of them is a bug you
will write.

- **The answer depends only on the key.** The proof's subject is a function `f`
  of the state. If the body reads a mutable global, a `visited` set, an
  accumulated path, or the input array that changes between queries, then no
  such `f` exists and the proof has nothing to talk about. This is the single
  most common cause of a memoised solution that is wrong while the uncached one
  is right.
- **The key is the whole state.** Two states that deserve different answers
  must hash and compare differently. Dropping a dimension from the key does not
  slow anything down — it returns another state's answer. (Dropping a dimension
  that genuinely does not matter is free and desirable; that is
  [[state-design]].)
- **The dependency graph is acyclic.** `rank` is what made the induction and
  the termination argument work. A cyclic dependency — `f(a)` needs `f(b)`
  needs `f(a)` — gives infinite recursion, and often there is no unique `f` at
  all. Caching cannot fix this; you need an ordering ([[topological-sort]]) or
  a fixpoint iteration ([[shortest-path]]).
- **"Absent" is distinguishable from "stored".** The proof says "if `s` is in
  `memo`". Testing truthiness instead of membership makes every state whose
  value is `0`, `False`, `None` or `""` look absent.
- **Stored values are not mutated afterwards.** If `solve` returns a list and
  the caller appends to it, `memo[s]` is no longer `f(s)` and (I) breaks silently.
- **For tabulation only: the loop order really is a linear extension.** The
  loop is correct only if every read has already been written. `for i in
  range(n)` is a topological order *if* the recurrence looks left. Reverse the
  recurrence and forget to reverse the loop and you read zeros.

One diagnostic falls out of all this and is worth more than the rest of the
section. **If the answer changes when you disable the cache, the bug is the key
or the purity, not the recurrence.** On a small input, delete the two memo lines
and re-run. If the uncached answer is right and the cached one is wrong, stop
looking at your arithmetic.

## What it costs

**Without a cache.** Climbing stairs with steps 1, 2 and 3 gives
`T(n) = T(n-1) + T(n-2) + T(n-3) + Θ(1)`. The homogeneous solution grows like
`ρⁿ` where `ρ ≈ 1.8393` is the real root of `x³ = x² + x + 1`, so the call count
is `Θ(1.84ⁿ)`. The code below counts 128,287 calls for `n = 18`, and
`1.84¹⁸ ≈ 1.1 × 10⁵` — the exponential is not a figure of speech.

**With a cache.** Charge every unit of work to a node or an edge of the DAG.

- Each state misses at most once (the proof's termination argument), so the
  "compute" half of the body runs at most `|V|` times, where `V` is the set of
  *reachable* states.
- Every edge `s → t` causes exactly one lookup, and that lookup is a hit or the
  one miss of `t`. So the number of lookups is exactly `|E| = Σ_s |dep(s)|`.

Hence **time = Θ(|V| · w + |E| · h)**, with `w` the non-recursive work per
state and `h` the cost of one cache probe. When the transition is O(1) this is
the formula to carry:

> cost = (number of reachable states) × (transitions per state)

Check it against the trace: 19 states, 3 transitions each, so `1 + 3 × 18 = 55`
calls — exactly what the program prints. For *0/1 Knapsack* the rectangle is
`(n+1)(W+1)` states with two transitions each, so `Θ(nW)`: polynomial in the
*value* `W`, not in its `log W` digits, which is why knapsack is called
pseudo-polynomial and why *0/1 Knapsack* always caps the capacity.

**Where the two differ.** Bottom-up computes every state it enumerates.
Top-down computes only the states reachable from the query, and that set can be
dramatically smaller. Knapsack again: at depth `i` the residual capacity is
`cap` minus a subset sum of the first `i` weights, so

    |V_reach| ≤ Σᵢ min(2ⁱ, W+1)  ≤  min((n+1)(W+1), 2ⁿ⁺¹)

and if every weight is a multiple of `g`, only capacities congruent to `cap`
mod `g` are ever reached, cutting the bound by a factor of `g`. The code below
has 8 items with weights that are multiples of 500 and a capacity of 6,000: the
full table is 54,009 cells and the memo stores 64. That is not a constant
factor.

<svg viewBox="0 0 400 200" role="img" aria-label="a grid of table cells with only a sparse subset shaded, showing that top-down visits far fewer states than bottom-up fills">
  <g>
    <rect x="60" y="40" width="22" height="22"/>
    <rect x="84" y="40" width="22" height="22"/>
    <rect x="108" y="40" width="22" height="22"/>
    <rect x="132" y="40" width="22" height="22"/>
    <rect x="156" y="40" width="22" height="22"/>
    <rect x="180" y="40" width="22" height="22"/>
    <rect x="204" y="40" width="22" height="22"/>
    <rect x="228" y="40" width="22" height="22"/>
    <rect x="252" y="40" width="22" height="22"/>
    <rect x="276" y="40" width="22" height="22"/>
    <rect x="300" y="40" width="22" height="22"/>
    <rect class="fill" x="324" y="40" width="22" height="22"/>
    <rect x="60" y="64" width="22" height="22"/>
    <rect x="84" y="64" width="22" height="22"/>
    <rect x="108" y="64" width="22" height="22"/>
    <rect x="132" y="64" width="22" height="22"/>
    <rect x="156" y="64" width="22" height="22"/>
    <rect x="180" y="64" width="22" height="22"/>
    <rect x="204" y="64" width="22" height="22"/>
    <rect x="228" y="64" width="22" height="22"/>
    <rect class="fill" x="252" y="64" width="22" height="22"/>
    <rect x="276" y="64" width="22" height="22"/>
    <rect x="300" y="64" width="22" height="22"/>
    <rect class="fill" x="324" y="64" width="22" height="22"/>
    <rect x="60" y="88" width="22" height="22"/>
    <rect x="84" y="88" width="22" height="22"/>
    <rect x="108" y="88" width="22" height="22"/>
    <rect class="fill" x="132" y="88" width="22" height="22"/>
    <rect x="156" y="88" width="22" height="22"/>
    <rect x="180" y="88" width="22" height="22"/>
    <rect class="fill" x="204" y="88" width="22" height="22"/>
    <rect x="228" y="88" width="22" height="22"/>
    <rect class="fill" x="252" y="88" width="22" height="22"/>
    <rect x="276" y="88" width="22" height="22"/>
    <rect x="300" y="88" width="22" height="22"/>
    <rect class="fill" x="324" y="88" width="22" height="22"/>
    <rect x="60" y="112" width="22" height="22"/>
    <rect class="fill" x="84" y="112" width="22" height="22"/>
    <rect x="108" y="112" width="22" height="22"/>
    <rect class="fill" x="132" y="112" width="22" height="22"/>
    <rect x="156" y="112" width="22" height="22"/>
    <rect x="180" y="112" width="22" height="22"/>
    <rect class="fill" x="204" y="112" width="22" height="22"/>
    <rect x="228" y="112" width="22" height="22"/>
    <rect class="fill" x="252" y="112" width="22" height="22"/>
    <rect x="276" y="112" width="22" height="22"/>
    <rect x="300" y="112" width="22" height="22"/>
    <rect class="fill" x="324" y="112" width="22" height="22"/>
    <rect class="fill" x="60" y="136" width="22" height="22"/>
    <rect class="fill" x="84" y="136" width="22" height="22"/>
    <rect x="108" y="136" width="22" height="22"/>
    <rect class="fill" x="132" y="136" width="22" height="22"/>
    <rect x="156" y="136" width="22" height="22"/>
    <rect x="180" y="136" width="22" height="22"/>
    <rect class="fill" x="204" y="136" width="22" height="22"/>
    <rect x="228" y="136" width="22" height="22"/>
    <rect class="fill" x="252" y="136" width="22" height="22"/>
    <rect x="276" y="136" width="22" height="22"/>
    <rect x="300" y="136" width="22" height="22"/>
    <rect class="fill" x="324" y="136" width="22" height="22"/>
    <text x="30" y="100">item</text>
    <text x="150" y="182">remaining capacity</text>
    <text x="60" y="28">bottom-up fills all of it; top-down touches the shaded cells</text>
  </g>
</svg>

**Space.** Top-down holds `|V_reach|` entries plus a call stack as deep as
`rank(q)`. Bottom-up holds the whole table — but only bottom-up can throw most
of it away: if a row depends only on the previous row, keep two rows and the
space drops from `Θ(nW)` to `Θ(W)`. A memo cannot, because it has no idea which
states will never be asked for again, and a bounded cache ([[lru-cache]]) that
evicts a state still needed turns `Θ(V)` work back into exponential work.

**The cost people forget** is the constant. A dict probe hashes the key, which
for a tuple of length `k` costs `Θ(k)`, paid twice per state plus once per edge:
five to ten times a list index in Python, and the reason a two-variable
recurrence like *Maximum Subarray* should never be memoised. Recursion adds a
frame per call, and the default limit of 1,000 is a hard wall — top-down over
`n = 200,000` days of *Best Time to Buy and Sell Stock* does not run slowly, it
raises `RecursionError`.

## The implementation

Three spellings of the same recurrence, cross-checked, with the call counts
that prove the collapse.

```python run
from functools import lru_cache

STEPS = (1, 2, 3)
calls = {"naive": 0, "memo": 0}


def naive(n):
    """Ways to climb n stairs in steps of 1, 2 or 3. No cache."""
    calls["naive"] += 1
    if n < 0:
        return 0
    if n == 0:
        return 1
    return sum(naive(n - s) for s in STEPS)


def top_down(n):
    memo = {}

    def go(k):
        calls["memo"] += 1
        if k < 0:
            return 0
        if k == 0:
            return 1
        if k in memo:                       # membership, never truthiness
            return memo[k]
        memo[k] = sum(go(k - s) for s in STEPS)
        return memo[k]

    return go(n), memo


def bottom_up(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for k in range(1, n + 1):               # k only ever reads smaller indices
        dp[k] = sum(dp[k - s] for s in STEPS if k - s >= 0)
    return dp[n]


@lru_cache(maxsize=None)
def cached(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    return sum(cached(n - s) for s in STEPS)


value, memo = top_down(5)
print("ways(5) =", value, " memo after the call:", dict(sorted(memo.items())))
assert value == 13

for n in range(0, 26):
    assert top_down(n)[0] == bottom_up(n) == cached(n)
print("top-down, bottom-up and lru_cache agree for n = 0..25")

n = 18
calls["naive"] = calls["memo"] = 0
assert naive(n) == top_down(n)[0]
print("n = %d: naive made %d calls, memoised made %d" % (n, calls["naive"], calls["memo"]))
assert calls["memo"] == 1 + len(STEPS) * n == 55     # 1 root + 3 per stored state
print("predicted by 1 + transitions x states:", 1 + len(STEPS) * n)
```

Three lines carry the weight.

`if k in memo` is a membership test, not `if memo.get(k)` and not
`if memo[k] is not None`. Half the states of a counting DP are legitimately
zero, and a falsy value read as "absent" restores the exponential without
changing a single answer — the worst kind of bug, because the tests pass.

`memo[k] = sum(...)` stores on *every* path out of the recursive branch. A
common mutation of this code computes the value, checks something, returns early
in one branch and stores only in the other; that state then misses forever and
the cache quietly stops working.

`@lru_cache(maxsize=None)` (`functools.cache` since 3.9) is the one-line
version, right whenever the arguments are hashable scalars. It buys you the
dictionary and the membership test; it costs you control, because the cache
lives on the function object and survives between calls — what you want inside
one problem, and what ruins you when the next test case has a different input
array. Closing over data that changes means `cache_clear()`, or a closure-local
dictionary as in `top_down`.

The bottom-up version allocates one list, never recurses, and would survive
`n = 10⁶`. It also needed a decision the other two did not: that
`range(1, n + 1)` is a valid order. It is, because `dp[k]` reads only smaller
indices — the linear extension from the proof, hiding in plain sight.

## Variants you will meet

**Plain tabulation.** The loop above: the default for one-dimensional
recurrences over an index, and for any `n` large enough to threaten the stack.
See [[dynamic-programming]].

**Rolling arrays.** Tabulation where you keep only the last one or two rows,
because the recurrence looks back a bounded distance. Reduces space by a factor
of `n` and is unavailable top-down.

**`functools.cache` on a pure function of scalars.** One decorator. Use it when
the arguments are ints, strs or tuples and the function reads nothing mutable.

**A dictionary keyed on a tuple.** The workhorse for states that are not a
rectangle: `(index, capacity, last_choice)`, `(mask, position)` in
[[dp-bitmask]], `(position, tight, sum_so_far)` in [[digit-dp]]. *Count
Four-Digit Codes with Sum S* and *Count Numbers with Digit Sum* are the
friendly end of that family — the state is `(digits left, sum left)` and most
of the rectangle is unreachable.

**A memo keyed on a node.** [[tree-dp]] memoises on `(node, took_it)`; the DAG
is the tree itself, so every state has in-degree one and the cache never hits —
you are memoising for the notation, not the speed.

**Interval DP.** State `(i, j)` with `j - i` shrinking. Top-down is much easier
to get right here, because bottom-up must loop over *lengths*, not over `i` and
`j`, and that is the single most commonly inverted loop order in DP. *Palindromic
Substrings* is the gentlest example of the shape.

**Memoising the transition, not the state.** When the combine step is itself
expensive, cache it separately — a precomputed `is_palindrome[i][j]` table, a
prefix-sum array ([[prefix-sums]]). Two small tables usually beat one big one.

**An explicit stack.** When top-down is the natural formulation but the depth
exceeds the recursion limit, convert the recursion to a stack of frames rather
than raising the limit; see [[recursion]].

**Astronomically large `n`.** If the state is an index and `n` is 10¹⁸, neither
form works: the number of states is the problem. Use
[[matrix-exponentiation]].

**Caching across queries.** When many queries share subproblems, compute once
and keep the table. *Pascal's Triangle* and *Suffix Maximum Frequency Queries*
are of this shape: the preprocessing is the DP and the query is a lookup.

```python run
import random
from itertools import combinations


def knap_top_down(w, v, cap):
    """0/1 knapsack, lazily. Returns (best value, states stored)."""
    memo = {}

    def go(i, c):
        if i == len(w):
            return 0
        if (i, c) in memo:
            return memo[(i, c)]
        best = go(i + 1, c)                                  # skip item i
        if w[i] <= c:
            best = max(best, v[i] + go(i + 1, c - w[i]))     # take item i
        memo[(i, c)] = best
        return best

    return go(0, cap), len(memo)


def knap_bottom_up(w, v, cap):
    """The same recurrence, every cell filled. Returns (best, cells)."""
    n = len(w)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):                # i reads only i+1: valid order
        for c in range(cap + 1):
            dp[i][c] = dp[i + 1][c]
            if w[i] <= c:
                dp[i][c] = max(dp[i][c], v[i] + dp[i + 1][c - w[i]])
    return dp[0][cap], (n + 1) * (cap + 1)


weights = [500, 1500, 2000, 3000, 1000, 2500, 500, 4000]
values = [3, 8, 9, 14, 6, 11, 2, 18]
cap = 6000

td, states = knap_top_down(weights, values, cap)
bu, cells = knap_bottom_up(weights, values, cap)
print("best value     :", td, "(top-down)", bu, "(bottom-up)")
print("states reached :", states, " cells in the full table:", cells)
print("               : %.0fx fewer states than cells" % (cells / states))
assert td == bu and states * 50 < cells

rng = random.Random(3)
for _ in range(200):                              # both against exhaustive search
    n = rng.randint(0, 7)
    w = [rng.randint(1, 9) for _ in range(n)]
    v = [rng.randint(1, 9) for _ in range(n)]
    c = rng.randint(0, 20)
    exp = max((sum(v[i] for i in s)
               for r in range(n + 1) for s in combinations(range(n), r)
               if sum(w[i] for i in s) <= c), default=0)
    assert knap_top_down(w, v, c)[0] == knap_bottom_up(w, v, c)[0] == exp
print("200 random instances match exhaustive subset search")
```

## Recognising it in a statement

That a DP is wanted at all is [[dynamic-programming]]'s subject: "how many
ways…" over a sequence of choices (*Count Staircase Ways*, *Count Four-Digit
Codes with Sum S*), "maximum total" where a greedy choice can be defeated by an
example (*Maximum Gold Path*, *0/1 Knapsack*), or `n ≤ 20` beside an
exponential brute force. Given that, choose the form. Reach **top-down** when:

- the state is a tuple of unlike quantities, so the enumeration order is not
  obvious;
- the dependencies do not all point one way (interval DP, games, grids with
  four-directional moves plus a budget);
- the reachable states are a thin slice of the rectangle — large capacities,
  large target sums, coarse weights;
- you are under time pressure and already have the brute force written. Adding
  four lines beats rewriting.

Reach **bottom-up** when:

- `n` is 10⁵ or more along any dimension, so the stack is a real risk;
- you need every cell anyway, or the table is the output (*Pascal's Triangle*);
- space matters and a rolling array applies;
- the recurrence is one-dimensional and the "table" is two variables
  (*Maximum Subarray*, *Best Time to Buy and Sell Stock*) — here a memo is pure
  overhead.

The anti-signal for the whole chapter: if the recursion's answer depends on the
route taken rather than on its arguments, it is not memoisable. A statement that
asks for *the* path, or that forbids revisiting a cell, is describing a search
over paths; the state would have to include the set of visited cells, and once
it does, "overlapping subproblems" usually evaporates.

## Traps

**A key that is not the whole state.** Symptom: wrong answers, often *better*
than possible, and only on inputs where two paths reach the same index with
different resources. Demonstrated below.

**Truthiness instead of membership.** `if memo.get(k):` or `if memo[k]:` treats
a stored `0` as absent. Symptom: correct answers, timeout, and the small tests
pass because they never reach a zero state. Demonstrated below.

**A cache that outlives its input.** An `@lru_cache`'d function closing over a
global grid, called again after the grid changes, returns the previous grid's
answers. Symptom: the first test case passes and every later one is wrong, which
looks like a reading-the-input bug and is not. Cure: put the varying data in the
key, clear the cache, or use a closure-local dictionary per call.

**`RecursionError` at depth ~1,000.** Symptom: a crash, not a slowdown, and only
on the large hidden tests. Raising `sys.setrecursionlimit` trades a clean
exception for a C-level stack overflow. Rewrite bottom-up.

**Returning a mutable value from the cache.** The caller appends to the list you
stored and corrupts the entry. Symptom: answers that change depending on the
order the queries arrive in. Return tuples, or copy on the way out.

**Memoising something with no overlap.** A cache on a
[[divide-and-conquer|divide and conquer]] recursion never hits and costs memory
and hashing. Check that two different call paths can actually produce the same
arguments.

**A cyclic dependency.** Symptom: infinite recursion, or — with an "in
progress" sentinel — plausible wrong answers. The recurrence is wrong.

```python run
def codes(k, target, membership):
    """k-digit codes (digits 0-9) whose digits sum to target."""
    memo, calls = {}, [0]

    def go(d, s):
        calls[0] += 1
        if s < 0:
            return 0
        if d == 0:
            return 1 if s == 0 else 0
        if membership:
            if (d, s) in memo:                 # right
                return memo[(d, s)]
        elif memo.get((d, s)):                 # wrong: a stored 0 is falsy
            return memo[(d, s)]
        memo[(d, s)] = sum(go(d - 1, s - x) for x in range(10))
        return memo[(d, s)]

    return go(k, target), calls[0], len(memo)


for k, target in ((4, 9), (6, 47)):
    a, ca, na = codes(k, target, True)
    b, cb, nb = codes(k, target, False)
    print("k=%d sum=%d -> %d codes, %d states" % (k, target, a, na))
    print("   'in memo': %7d calls      '.get()': %7d calls  (%.0fx)"
          % (ca, cb, cb / ca))
    assert a == b                              # same answer, always
assert codes(6, 47, False)[1] > 100 * codes(6, 47, True)[1]
print("the falsy-zero bug is invisible at k=4 and 500x at k=6\n")


def knap(w, v, cap, full_key):
    memo = {}

    def go(i, c):
        if i == len(w):
            return 0
        key = (i, c) if full_key else i        # c is part of the state
        if key in memo:
            return memo[key]
        best = go(i + 1, c)
        if w[i] <= c:
            best = max(best, v[i] + go(i + 1, c - w[i]))
        memo[key] = best
        return best

    return go(0, cap)


w, v, cap = [3, 4, 5], [4, 5, 7], 7
print("knapsack, key (i, c):", knap(w, v, cap, True),
      "  key i only:", knap(w, v, cap, False), "(takes all three items)")
assert knap(w, v, cap, True) == 9 and knap(w, v, cap, False) == 16
```

The second half is the more instructive failure. Dropping `c` from the key gives
16, which is *larger* than the true optimum of 9 — the cached answer for index 1
was computed with capacity 7 and handed back to a caller that only had capacity
4. A memo with an incomplete key does not lose information; it invents it.

## What to memorise

The template, which should arrive without thought:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def solve(i, rest):
    if base_case(i, rest):
        return base_value
    return best(solve(j, rest') for each choice)
```

and its hand-rolled twin, for when the function closes over data that changes:

```python
memo = {}
def solve(i, rest):
    key = (i, rest)
    if key in memo:            # membership, not truthiness
        return memo[key]
    ...
    memo[key] = answer
    return answer
```

The sentence that turns a problem into it: *"Is the same argument tuple always
worth the same answer?"* If yes, memoise. If the answer depends on how you got
there, you are backtracking, not memoising.

The habit: after writing the recursion, **list everything the body reads that is
not an argument.** Every item on that list must be constant for the whole run,
or it belongs in the key. That one audit prevents the incomplete-key bug and the
stale-cache bug, which between them account for most wrong memoised solutions.

Numbers worth carrying. Cost is states × transitions; 10⁷ state-transitions is
about the ceiling for Python in a few seconds, 10⁸ is not. Python's recursion
limit is 1,000, so any dimension above about 10⁴ wants a loop. A dict probe with
a tuple key costs roughly five to ten times a list index. And a cached value
that is falsy is the difference between `Θ(V + E)` and exponential.

## Check yourself

:::check
The memoised stair climb made 55 calls for `n = 18`, not 19. Where do the other
36 come from, and what does that tell you about how to cost a top-down solution?
--
There are 19 states (`0 … 18`), and each of the 18 non-base states makes 3
recursive calls, plus the one call at the root: `1 + 3 × 18 = 55`.

The lesson is that the states count the *misses*, but the calls count the
*edges* of the dependency DAG. A top-down solution costs
`Θ(|V| · work-per-state + |E| · probe)`, and `|E|` is `|V|` times the branching
factor. A DP with 10⁶ states and 100 transitions each is 10⁸ probes, which is
too slow, even though "a million states" sounds fine. Always multiply by the
branching factor before you decide the solution fits.
:::

:::check
Someone says: "memoisation and tabulation are the same algorithm, so they always
have the same time and space complexity." Where are they wrong?
--
They are right that both compute the same function and that the *per-state* work
is identical. They are wrong three times over about which states, and about the
constants.

*Time.* Bottom-up computes every state it enumerates; top-down computes only the
states reachable from the query. In the knapsack above, 64 versus 54,009 — the
reachable set is bounded by `min((n+1)(W+1), 2ⁿ⁺¹)` and by divisibility
structure in the weights, and either bound can be far below the rectangle. So
top-down can be asymptotically faster.

*Space.* Bottom-up can throw rows away: a recurrence that looks back one row
needs `Θ(W)`, not `Θ(nW)`. Top-down cannot, because it does not know when a
state has been asked for the last time. So bottom-up can be asymptotically
smaller — and it uses no call stack, while top-down uses one as deep as the
longest dependency chain.

*Constants.* A dict probe on a tuple key hashes `Θ(k)` bytes and a Python frame
is expensive; a `dp[i][c]` index is neither. For a recurrence whose whole table
is two variables, memoising is strictly worse on every axis.
:::

:::check
Why does replacing `if key in memo` with `if memo.get(key):` leave every answer
correct while destroying the running time — and why do small tests miss it?
--
Correctness is untouched because all that changed is *when* the cache is
consulted. A missed hit just recomputes the value, and the proof never assumed
the cache was consulted at all — the uncached recursion is correct too.

The running time dies because a state whose value is `0` can never be served
from the cache: `memo.get(key)` returns `0`, which is falsy, so the body runs
again, recursing into *its* successors, which are also often zero. The zero
region of the state space reverts to the uncached exponential, and it does so
recursively. In the code above, `k = 6, sum = 47` goes from 1,411 calls to
765,591.

Small tests miss it because the zero states are the *unreachable-sum* states:
with four digits and a target of 9 no partial sum is ever impossible, so no zero
is ever stored and both versions behave identically. You need a target near the
edge of the feasible range before the bug appears at all.
:::

:::check
Why does memoisation require the dependency graph to be acyclic, when the cache
seems like it would break a cycle by returning the stored value?
--
Because nothing is stored until a call *returns*, and in a cycle no call ever
returns. `f(a)` calls `f(b)` calls `f(a)`; the second `f(a)` finds the memo
empty for `a` (the first `f(a)` has not finished computing, so it has written
nothing) and recurses again. You get infinite recursion, not a hit.

The deeper problem is that the proof used `rank`, the longest path out of a
state, both to define the specification `f` and to justify termination. With a
cycle there may be no unique solution to the equations at all — think of a
shortest-path recurrence around a zero-weight cycle, where infinitely many
assignments satisfy every equation. Caching cannot manufacture a well-founded
order that the recurrence does not have. Either impose one (add a dimension such
as "number of edges used", which strictly decreases), find a topological order
([[topological-sort]]), or iterate to a fixpoint ([[shortest-path]]).
:::

:::check
A colleague's grid solution memoises `go(r, c)` — the longest path from cell
`(r, c)` moving in any of the four directions without revisiting a cell — by
keeping a `visited` set in an enclosing scope. It is fast and wrong. Diagnose it
in the vocabulary of the proof, and say what the fix costs.
--
The body reads `visited`, which is not part of the key. So there is no function
`f` of `(r, c)` for the cache to store: the correct answer for `(r, c)` depends
on which cells are already on the current path, and two different paths arriving
at `(r, c)` genuinely deserve different answers. The invariant "every key in
`memo` maps to `f(key)`" cannot even be stated.

The tell-tale diagnostic applies: disable the cache and the answers change. When
that happens the recurrence is not the suspect.

The honest fix puts the visited set into the key — `(r, c, frozenset)` — at
which point the state space is `Θ(rc · 2^{rc})`, no two paths share a state, the
cache never hits, and you have written [[backtracking]] with extra memory. The
conclusion is not "memoise harder" but "this is not a DP over cells". It becomes
one only if the moves cannot revisit anything — right and down only, say, which
is why *Maximum Gold Path* and *Matrix Traversal* are DPs and a free-roaming
longest path is not.
:::
