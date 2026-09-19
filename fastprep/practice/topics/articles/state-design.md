# Designing the State

> Every dynamic program is a bet that you are allowed to forget most of the past.
> The state is the part you may not forget. Choose it correctly and the
> recurrence is transcription; choose it badly and no amount of clever code will
> save you.

## When you reach for it

You reach for state design the moment you decide a problem is dynamic
programming — which is to say, constantly. Four hundred and twenty-three problems
in this bank practise it, making it #10 of 150 topics. It is not an algorithm you
run; it is the decision you make *before* any algorithm exists, and everything
else depends on it.

The trigger has three parts, and all three must hold:

1. A solution is a **sequence of decisions**. Buy or don't buy on day `i`. Rob
   house `i` or skip it. Take coin `c` next. Match this character or delete it.
2. A brute force over those decisions **exists** — with infinite time you could
   enumerate them all.
3. That brute force **revisits the same situation** repeatedly, because many
   different prefixes leave you facing an identical remaining problem.

The state is the name you give to "the same remaining problem". Get it right and
the exponential tree collapses into a polynomial table. Get it wrong one way and
you compute a confidently incorrect number; wrong the other way, the right number
too slowly.

It is the wrong tool in three cases. If a single decision is *provably* safe at
every step you need no table — that is a greedy, found with an
[[greedy-exchange|exchange argument]], not intuition. If the subproblems never
repeat, memoising costs memory and buys nothing; that is plain [[backtracking]].
And if the summary the future needs genuinely *is* the whole history, no small
state exists: expect [[dp-bitmask]] with `n <= 20`, [[meet-in-the-middle]], or a
problem whose tiny constraints admit that nothing polynomial is known.

Most named DP problems are one method with different answers to one question.
*Best Time to Buy and Sell Stock* appears four times in this bank, from
FlexTrade, JP Morgan Chase, Oracle and Zoox; *House Robber*, *0/1 Knapsack*,
*Coin Change* and *Edit Distance* sit alongside it. Not four algorithms — four
state spaces.

## The idea

**Two partial solutions are the same state when every possible future is worth
exactly the same to both of them.**

That is the entire chapter. Everything below is consequences.

Picture the brute-force recursion tree: the root is "nothing decided yet", each
edge is one decision, each leaf a complete solution, and there are exponentially
many nodes. Now look along one level and ask: *from here on, does it matter which
path I took to get here?* For the stock problem it does not matter which days you
looked at — only which day you are on and whether you hold a share. Every node
agreeing on those two facts faces an identical future. Merge them. The tree
becomes a directed acyclic graph, and the size of that graph is the cost of your
algorithm.

<svg viewBox="0 0 690 250" role="img" aria-label="a brute-force recursion tree on the left, and on the right the same tree with nodes of equal state merged into a DAG">
  <g>
    <circle cx="160" cy="32" r="16"/>
    <text x="160" y="38" text-anchor="middle">·</text>
    <circle cx="90" cy="105" r="16"/>
    <text x="90" y="111" text-anchor="middle">a</text>
    <circle cx="230" cy="105" r="16"/>
    <text x="230" y="111" text-anchor="middle">b</text>
    <circle cx="45" cy="180" r="16"/>
    <text x="45" y="186" text-anchor="middle">p</text>
    <circle class="fill" cx="125" cy="180" r="16"/>
    <text x="125" y="186" text-anchor="middle">q</text>
    <circle class="fill" cx="195" cy="180" r="16"/>
    <text x="195" y="186" text-anchor="middle">q</text>
    <circle cx="275" cy="180" r="16"/>
    <text x="275" y="186" text-anchor="middle">r</text>
    <line x1="150" y1="46" x2="100" y2="91"/>
    <line x1="170" y1="46" x2="220" y2="91"/>
    <line x1="80" y1="119" x2="55" y2="166"/>
    <line x1="100" y1="119" x2="115" y2="166"/>
    <line x1="220" y1="119" x2="205" y2="166"/>
    <line x1="240" y1="119" x2="265" y2="166"/>
    <text x="160" y="225" text-anchor="middle">every path is its own node</text>
    <text x="160" y="243" text-anchor="middle">nodes grow like b to the n</text>
    <line x1="320" y1="105" x2="375" y2="105"/>
    <line x1="375" y1="105" x2="363" y2="98"/>
    <line x1="375" y1="105" x2="363" y2="112"/>
    <text x="347" y="92" text-anchor="middle">merge</text>
    <circle cx="530" cy="32" r="16"/>
    <text x="530" y="38" text-anchor="middle">·</text>
    <circle cx="460" cy="105" r="16"/>
    <text x="460" y="111" text-anchor="middle">a</text>
    <circle cx="600" cy="105" r="16"/>
    <text x="600" y="111" text-anchor="middle">b</text>
    <circle cx="415" cy="180" r="16"/>
    <text x="415" y="186" text-anchor="middle">p</text>
    <circle class="fill" cx="530" cy="180" r="16"/>
    <text x="530" y="186" text-anchor="middle">q</text>
    <circle cx="645" cy="180" r="16"/>
    <text x="645" y="186" text-anchor="middle">r</text>
    <line x1="520" y1="46" x2="470" y2="91"/>
    <line x1="540" y1="46" x2="590" y2="91"/>
    <line x1="450" y1="119" x2="425" y2="166"/>
    <line x1="470" y1="119" x2="520" y2="166"/>
    <line x1="590" y1="119" x2="540" y2="166"/>
    <line x1="610" y1="119" x2="635" y2="166"/>
    <text x="530" y="225" text-anchor="middle">equal states are one node</text>
    <text x="530" y="243" text-anchor="middle">nodes grow like the state space</text>
  </g>
</svg>

Statisticians call that summary a **sufficient statistic**; physicists say the
process is **Markov** in the state. Both mean the same practical thing: given the
state, the future is independent of the past.

In practice you find it by writing the brute force first, as a recursive
function, then reading its signature back to yourself:

> **Question 1. What decision do I make next?** The answer names the axis you
> walk — usually an index into an array, a position in a grid, a node in a tree,
> a remaining amount.
>
> **Question 2. What about the past does that decision depend on, that I cannot
> recompute from the axis alone?** Each answer is one extra axis. "Whether I hold
> a share." "How many transactions I have used." "What colour the previous house
> is." "How much capacity is left."
>
> **Question 3. Is the set of possible answers small and finite?** If yes, you
> have a DP. If no, you have a search — go back to question 2 and look for
> something you are carrying that you do not need.

Question 2 is where the thinking happens, and its mirror image saves more time
than any micro-optimisation: **what am I carrying that the future does not
need?** A parameter recomputable from the others is not an axis but a multiplier
on your running time. In knapsack, "capacity used" and "capacity remaining" are
one axis wearing two hats. Carry one.

## Worked by hand

The simplest problem in the bank that needs a second axis is *Best Time to Buy
and Sell Stock*: prices on consecutive days, buy at most one share, sell it on a
strictly later day, maximise profit.

The obvious first attempt is one number per day: `best[i]` = the most profit
obtainable using only days `0..i`. It is a perfectly good *quantity* and it is
not a state. Suppose `prices = [7, 1, 5, 3, 6]` and you have computed
`best[3] = 4`. Day 4 arrives at price 6. What is `best[4]`? You cannot say: the
4 tells you what the answer was and nothing about the cheapest available buy.
`best[3]` is an answer, not a summary.

So ask question 2. On day `i` the decision is buy / sell / do nothing, and which
of those are legal depends on exactly one bit of history: **am I holding a share
right now?** Two states per day:

- `cash` — I own nothing; the number is my profit so far.
- `hold` — I own one share; the number is my profit so far, which is negative
  because I have paid for the share and not sold it.

<svg viewBox="0 0 560 210" role="img" aria-label="a two-node state machine: cash and hold, with buy and sell transitions between them and a rest self-loop on each">
  <g>
    <circle cx="150" cy="115" r="46"/>
    <text x="150" y="121" text-anchor="middle">cash</text>
    <circle cx="410" cy="115" r="46"/>
    <text x="410" y="121" text-anchor="middle">hold</text>
    <line x1="197" y1="98" x2="362" y2="98"/>
    <line x1="362" y1="98" x2="350" y2="91"/>
    <line x1="362" y1="98" x2="350" y2="105"/>
    <text x="280" y="86" text-anchor="middle">buy: value − price</text>
    <line x1="362" y1="136" x2="197" y2="136"/>
    <line x1="197" y1="136" x2="209" y2="129"/>
    <line x1="197" y1="136" x2="209" y2="143"/>
    <text x="280" y="158" text-anchor="middle">sell: value + price</text>
    <circle cx="150" cy="48" r="21"/>
    <circle cx="410" cy="48" r="21"/>
    <text x="150" y="20" text-anchor="middle">rest</text>
    <text x="410" y="20" text-anchor="middle">rest</text>
    <text x="280" y="196" text-anchor="middle">one bit of history, four transitions, done</text>
  </g>
</svg>

Because only one transaction is allowed, a buy always starts from a profit of
zero rather than from `cash`. Each day, compute `cash` from *yesterday's* `hold`
(so the sell is strictly later than the buy), then update `hold`. Start at
`cash = 0`, `hold = −∞` — holding is not yet possible.

| day | price | `cash` = max(cash, hold + price) | `hold` = max(hold, −price) | reading |
| --- | --- | --- | --- | --- |
| — | — | 0 | −∞ | before trading |
| 0 | 7 | max(0, −∞) = 0 | max(−∞, −7) = **−7** | bought at 7 |
| 1 | 1 | max(0, −7 + 1) = 0 | max(−7, −1) = **−1** | switched the buy to 1 |
| 2 | 5 | max(0, −1 + 5) = **4** | max(−1, −5) = −1 | first profit |
| 3 | 3 | max(4, −1 + 3) = 4 | max(−1, −3) = −1 | selling at 3 is worse |
| 4 | 6 | max(4, −1 + 6) = **5** | max(−1, −6) = −1 | the answer |

Answer: 5, buying on day 1 and selling on day 4.

Three things in that table are invisible in the code.

**The `hold` column is never the answer, and the algorithm cannot run without
it.** It is pure state: a number whose only job is to carry the one fact the
future needs. When a DP feels like it "should" be one number and is not working,
the missing column looks like this one.

**`hold` is the minimum price so far, negated** — −7, −1, −1, −1, −1 against
running minima 7, 1, 1, 1, 1. The famous one-liner, "track the minimum price and
the best profit", *is* this state machine with the sign flipped and the
vocabulary thrown away. A well-chosen state usually turns out to be what an
experienced person tracks by instinct; the method gets you there without it.

**Day 3 shows the merge happening.** Neither row changes: a worse candidate
arrived and was dropped. Every such `max` discards a whole subtree of the brute
force, and the proof below is the licence to do it.

## Why it is correct

The recurrence is not the thing to prove. What needs proof is the step everyone
takes without noticing: **keeping one number per state, and throwing every other
partial solution away.**

:::proof One value per state loses no optimum
**Setup.** A solution is a finite sequence of decisions. Let `P` be the set of
reachable decision prefixes, `ε` the empty one. For `p ∈ P` write `val(p)` for
the value accumulated so far and `Ext(p)` for the legal completions — sequences
`c` making `p·c` a complete solution, worth `val(p) + gain(p, c)`. The objective
is a maximum; for a minimum, flip every inequality.

A **state map** is any `σ : P → S`. Call it **adequate** if, whenever
`σ(p) = σ(q)`:

- **(A1)** `Ext(p) = Ext(q)` — the same completions are legal after both;
- **(A2)** `gain(p, c) = gain(q, c)` for every such `c` — each completion is
  worth the same after both;
- **(A3)** one decision `d` moves state and value by amounts depending only on
  the state: `σ(p·d) = σ(q·d)`, written `δ(σ(p), d)`, and
  `val(p·d) − val(p) = val(q·d) − val(q)`, written `cost(σ(p), d)`.

Define `f(s) = max { val(p) : p ∈ P, σ(p) = s }`, with `max ∅ = −∞`.

**Claim 1 (dominance).** If `σ(p) = σ(q)` and `val(p) >= val(q)`, then the best
complete solution extending `p` is at least as good as the best extending `q`.

*Proof.* Let `c ∈ Ext(q)`. By (A1), `c ∈ Ext(p)`; by (A2) the two gain the same,
so `val(p) + gain(p, c) >= val(q) + gain(q, c)`. Take the maximum over `c`. ∎

This is an exchange argument: given an optimal solution `q·c`, cut off its prefix
and graft on `p`. The result is legal and no worse. So a prefix that is not the
best of its state is never *needed*, and one number per state suffices.

**Claim 2 (the recurrence computes `f`).** Let `f_k(s)` be the maximum of
`val(p)` over prefixes `p` of length at most `k` with `σ(p) = s`. Then

```
f_0(s)     = 0 if s = σ(ε) else −∞
f_{k+1}(s) = max( f_0(s),  max over (t, d) with δ(t, d) = s  of  f_k(t) + cost(t, d) )
```

*Base case.* Only `ε` has length 0, and `val(ε) = 0`.

*Inductive step.* Take any prefix `p` of length at most `k+1` with `σ(p) = s`.
Either `p = ε`, covered by the `f_0` term, or `p = q·d` with `|q| <= k`. By (A3),
`val(p) = val(q) + cost(σ(q), d)` and `δ(σ(q), d) = s`, and by hypothesis
`f_k(σ(q)) >= val(q)`, so the right-hand side is at least `val(p)` and hence at
least `f_{k+1}(s)`. Conversely every term on the right is `val(q·d)` for a
genuine prefix of length at most `k+1` mapping to `s`, so the right-hand side is
at most `f_{k+1}(s)`. The two are equal. ∎

**Termination.** `P` is finite, so some `K` bounds every prefix length and
`f = f_K`. If the state graph `(S, δ)` is acyclic, evaluating states in
topological order computes `f` in one pass over the edges; if it has cycles,
iterate until the values stop changing — that is [[bellman-ford|Bellman-Ford]],
and it converges only if no cycle has positive total cost.

**Conclusion.** The optimum is `max { f(s) : s a terminal state }`, and computing
all of `f` touches each `(state, decision)` pair once. ∎
:::

Now say out loud what that proof leaned on. Every DP bug you will write is one of
these assumptions quietly failing.

- **(A1) — the same futures must be legal.** The assumption people break. If a
  completion is legal after `p` but illegal after `q`, merging them invents
  solutions that do not exist and the answer comes out *too good*. In *Maximum
  Value from Circular Houses* the index alone is not a state, because whether you
  may take the last house depends on whether you took the first.
- **(A2) — the same futures must be worth the same.** Broken when the price of a
  future decision depends on history you dropped: "the `k`-th ride costs `k`
  euros" puts `k` in the state.
- **(A3) — the objective must be separable.** `val` must accumulate one decision
  at a time. Sums and maxima of sums are separable; an *average*, a *ratio* or
  "largest minus smallest" is not, and must be lifted into the state (carry the
  count, carry the minimum) or the problem reformulated.
- **Acyclicity, or a convergence argument.** The proof inducts on prefix length;
  code needs an evaluation order in which every dependency is already done. A
  state that depends on itself is an infinite recursion or a wrong answer.
- **Finiteness and determinism.** `S` must be small, and `cost(s, d)` must not
  secretly consult anything outside `s`.

:::note Counting is a different proof
Everything above maximises. If you are *counting* — *Count Staircase Ways*,
*Coloring Houses*, *Count Sawtooth Subarrays* — replace `max` by `+` and Claim 1
by something stronger: the map from paths through the state graph to objects
counted must be a **bijection**. Dominance is irrelevant, you keep every prefix;
instead you must guarantee that no object is reachable by two paths (overcount)
and none by zero (undercount). The demonstration in **Traps** is this failure,
the commonest counting-DP bug. See [[counting-dp]].
:::

## What it costs

A DP's running time is not a fact about dynamic programming. It is a fact about
the state space you designed, computable before you write a line.

Start with what memoisation buys. A brute-force recursion with branching
factor `b` and depth `n` has `Θ(bⁿ)` nodes. Memoised, each *distinct* state is
expanded exactly once, and expanding it costs `b` transitions. So

```
T  =  (number of states) × (transitions per state) × (cost of one transition)
```

and that is the whole story: the speedup is `bⁿ / |S|`. A DP being fast means its
state space is small, nothing else.

That space is a **product**, `|S| = |A₁| × |A₂| × … × |A_d|`, which is why an
axis is expensive: a new one multiplies your cost, it never adds to it. Run the
numbers on the families in this bank:

- **Stock with at most `k` transactions.** `n` days × `(k+1)` transactions × 2
  holding flags, 2 transitions each, so `Θ(nk)`. *Maximum Profit with at Most K
  Transactions* bounds `n <= 1000` and `k <= 100`: about `2 × 10⁵` edges. And
  `k > n/2` is the same as unlimited, so clamping `k` to `n/2` keeps it from
  inflating the table.
- **0/1 knapsack.** `n` items × `W` capacities, 2 transitions, so `Θ(nW)`. That
  is *pseudo*-polynomial: `W` enters as a number while the input writes it in
  `log W` bits, which is why a capacity of `10⁹` kills the algorithm that a
  capacity of `10⁴` cannot dent. See [[knapsack]].
- **Bitmask over subsets.** `2ⁿ × n` states, `n` transitions, so `Θ(n² 2ⁿ)`. At
  `n = 20` that is `4 × 10⁸` — a C++ number, not a Python number, and the reason
  every bitmask problem prints `n <= 20` in its constraints. See [[dp-bitmask]].

**Space** follows the same product, with one discount: if every transition moves
the position axis forward by a bounded amount, only a bounded number of layers is
live, and space falls from `|S|` to `|S| / n`. That is the rolling array — the
stock machine keeps `2(k+1)` numbers for any `n`.

Four costs people forget:

- **The cost of one transition.** A DP over substrings has `Θ(n²)` states; if
  each transition calls an `O(n)` palindrome check, the total is `Θ(n³)` — you
  have quietly cubed a quadratic algorithm. *Split a String into Three
  Palindromes* and *Count Palindromic Substrings* both want the palindrome table
  precomputed. See [[palindromes]].
- **The cost of naming a state.** A top-down memo hashes a tuple on every call,
  and a dict entry costs about a hundred bytes against 8 for an array slot. Ten
  million states as a dict is impossible; as a rolling pair of lists it is two
  rows. See [[memoization]].
- **Recursion depth.** A top-down DP whose axis runs to `10⁵` hits Python's
  recursion limit long before its time limit.
- **Unbounded integers in counting DP.** Counts become thousand-bit integers and
  arithmetic stops being `O(1)`. *Coloring Houses* asking for the answer modulo
  `10⁹ + 7` is not decoration; it keeps the arithmetic constant time. See
  [[modular-arithmetic]].

## The implementation

The stock ladder as one state machine parameterised by `k`, checked against an
independent brute force that enumerates buy/sell days directly.

```python run
from itertools import combinations

NEG = float("-inf")


def best_profit(prices, k):
    """Max profit with at most k transactions. State: (day, j used, holding)."""
    n = len(prices)
    k = min(k, n // 2)                  # more transactions than days is the same
    if k == 0:                          # as unlimited: each needs a distinct buy
        return 0
    buy = [NEG] * (k + 1)               # buy[j]:  j-th transaction open
    sell = [0] * (k + 1)                # sell[j]: j transactions closed
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]


def brute(prices, k):
    """Independent: try every set of 2m days, paired buy-sell in order."""
    n, best = len(prices), 0
    for m in range(1, k + 1):
        for days in combinations(range(n), 2 * m):
            best = max(best, sum(prices[days[2 * t + 1]] - prices[days[2 * t]]
                                 for t in range(m)))
    return best


prices = [7, 1, 5, 3, 6]
cash, hold = 0, NEG                     # the hand trace, printed
print("day price  cash  hold")
for i, p in enumerate(prices):
    cash, hold = max(cash, hold + p), max(hold, -p)
    print("%3d %5d %5d %5s" % (i, p, cash, hold))
assert cash == best_profit(prices, 1) == 5

print()
for k in (1, 2, 3):
    print("k =", k, "->", best_profit(prices, k), "(brute force:", brute(prices, k), ")")

import random
rng = random.Random(3)
for _ in range(300):
    ps = [rng.randrange(0, 12) for _ in range(rng.randint(1, 8))]
    for k in (1, 2, 3):
        assert best_profit(ps, k) == brute(ps, k), (ps, k)
print("\n300 random price series x 3 transaction limits agree with brute force")
```

Three lines carry the weight.

`buy[j] = max(buy[j], sell[j - 1] - p)` is the only place the transaction counter
moves. Opening the `j`-th transaction must start where `j - 1` are already
closed — that dependency of `j` on `j - 1` is the second axis earning its place.
Delete the axis and you have *Maximum Stock Profit with Unlimited Transactions*;
pin it at 2 and you have *Maximum Stock Profit with At Most Two Transactions*.
One axis, three problems.

`sell[j] = max(sell[j], buy[j] + p)` reads `buy[j]` *after* the same day updated
it, permitting a same-day buy and sell for a profit of zero. That is harmless — a
zero-profit transaction never improves a maximum — and it is far simpler than
tracking yesterday's values. The hand trace above uses yesterday's `hold`, the
pedantic reading of "sell on a later day"; both give 5, and knowing which corners
are safe to cut is half of writing DP quickly.

`k = min(k, n // 2)` is a state-space optimisation, not a micro-optimisation:
each transaction needs its own buy day and sell day, so more than `n/2` can never
be used. Without the clamp, `k <= 100` against `n = 2` allocates fifty times more
table than the problem contains.

## Variants you will meet

The families below are one method. What changes is the answer to question 2.

**Position alone.** The purest case: *Climb Stairs with One, Two, or Three
Steps*, *Count Staircase Ways*. See [[dp-1d]].

**Position plus a running quantity you cannot recompute.** "Best subarray ending
exactly at `i`" is a state; "best subarray in `0..i`" is not. That distinction is
the whole of [[kadane]], and why *Maximum Subarray* is a one-liner once stated
correctly.

**Position plus a small mode flag.** The stock machine; *Coloring Houses*, where
the flag is the previous house's colour; *Count Sawtooth Subarrays*, where it is
the parity of the last element.

**Two positions**, one index into each of two sequences: *Edit Distance*,
*Interleaving String*, *Longest Palindromic Subsequence*. See [[dp-strings]] and
[[dp-2d]].

**Position plus a budget**, an axis as large as its bound: *0/1 Knapsack*,
*Coin Change*, *Budget-Constrained Project Selection*. See [[knapsack]] and
[[unbounded-knapsack]].

**An interval as the state.** When decisions merge neighbours rather than extend
a prefix, the state is `(left, right)`: *Minimum Cost to Merge Stones*,
*Coin Game From The Ends*. See [[partition-dp]].

**Digits plus a tightness flag** — position in the decimal string, whether the
prefix still equals the bound's, plus whatever is accumulated. *Count Numbers
with Digit Sum*, *Count Four-Digit Codes with Sum S*. See [[digit-dp]].

**A subset as the state**, when nothing smaller than "which items are used"
works: *Beautiful Arrangement*. See [[dp-bitmask]].

**Whose turn it is** — a player axis, or the negamax trick of storing the score
difference from the mover's point of view: *Stone Game III*, *Optimal Card Game
Score*. See [[game-dp]].

**A graph node as the state.** *Cheapest Flights Within K Stops* is a shortest
path whose state is `(city, stops used)`, not `city`; the "at most K" is an axis,
and adding it makes an otherwise-illegal Dijkstra legal. See [[shortest-path]].

**The state on a tree**, where children are combined rather than sequenced:
*Tree-Dependent Knapsack*, *Best Sum Downward Tree Path*. See [[tree-dp]].

**Swapping the value and the axis.** When the value is huge and the answer small,
invert: instead of "the best value at index `i`", store "the smallest tail for
each achievable length". That turns the `O(n²)` longest increasing subsequence
into the `O(n log n)` one. See [[lis]].

And the variant that is really a case split: **circular constraints**. Here is
the (A1) failure from the proof, made concrete and runnable.

```python run
def rob_line(nums):
    """Max non-adjacent sum on a line. State: (index, was the last one taken)."""
    take, skip = 0, 0
    for v in nums:
        take, skip = skip + v, max(skip, take)
    return max(take, skip)


def rob_circle(nums):
    """Houses 0 and n-1 are adjacent. Split on the axis 'did I take house 0'."""
    if len(nums) == 1:
        return nums[0]
    return max(rob_line(nums[:-1]),      # house 0 allowed, last house banned
               rob_line(nums[1:]))       # house 0 banned, last house allowed


def brute_circle(nums):
    n, best = len(nums), 0
    for mask in range(1 << n):
        if n > 1 and any(mask >> i & 1 and mask >> ((i + 1) % n) & 1 for i in range(n)):
            continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best


nums = [2, 3, 2]
print("houses          ", nums)
print("rob_line        ", rob_line(nums), "<- takes both ends: illegal on a circle")
print("rob_circle      ", rob_circle(nums))
print("brute force     ", brute_circle(nums))
assert rob_line(nums) == 4 and rob_circle(nums) == brute_circle(nums) == 3

import random
rng = random.Random(5)
for _ in range(400):
    a = [rng.randrange(0, 9) for _ in range(rng.randint(1, 10))]
    assert rob_circle(a) == brute_circle(a), a
print("400 random circles agree with brute force")
```

The lesson is not "special-case the circle". It is that `index` stopped being a
state once the ends became adjacent, because the legality of the last decision
depended on the first — assumption (A1), broken. The repair is an axis, "did I
take house 0", and since it has two values you may as well run the whole DP twice
and keep the better answer. *House Robber* and *Maximum Non-Adjacent House Value*
need one pass; *Maximum Value from Circular Houses* needs the axis.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"at most `k` …"**, **"within `k` steps"**, **"no more than `k` …"**. That
   `k` is an axis, and the statement bounding it is the author telling you the
   table fits. *Maximum Profit with at Most K Transactions*, *Cheapest Flights
   Within K Stops*.
2. **A constraint linking consecutive decisions**: "no two adjacent", "cannot
   repeat the previous colour", "must alternate", "must sell before buying
   again". The last decision becomes an axis, usually a tiny one. *House
   Robber*, *Coloring Houses*, *Count Sawtooth Subarrays*.
3. **The constraint line, read as a budget for the state space** — the most
   mechanical signal there is. `n <= 20` means a subset axis of `2ⁿ`; `n <= 100`
   with an interval flavour means `O(n³)`; `n <= 5000` means two position axes;
   `n <= 10⁵` means a constant number of states per index, a flag rather than a
   second array. A bound on a *sum* or *capacity* is naming an axis out loud.
   Find the product that fits the bounds and you have usually found the state.
4. **"How many ways …", "count the number of …", "modulo 10⁹ + 7"** — a counting
   DP, where the bijection assumption above matters more than dominance. See
   [[counting-dp]].
5. **"Maximise/minimise" plus an exponential brute force** that visibly re-solves
   the same tail: criterion 3 of the trigger.

The anti-signals, which are just as valuable:

- **A single decision is provably safe.** If sorting and taking greedily is
  correct, a table is wasted work. Prove it with an exchange argument
  ([[greedy-exchange]]), never by testing two examples.
- **The objective is not separable.** Averages, ratios, medians and
  "maximum minus minimum" break (A3). Lift the missing piece into the state, or
  transform the problem.
- **No repetition.** *Enumerate Right-and-Down Matrix Paths* asks you to list the
  paths, not count them; listing is `Θ(output)` and memoising cannot help. That
  is [[backtracking]].
- **The state would have to hold the whole history.** If nothing smaller works
  and `n` is large, stop looking for a polynomial DP.

## Traps

**A state that is not sufficient.** The chief trap, hard to catch because the
program runs and the samples pass. Symptom: answers too good (you merged prefixes
with different legal futures) or too bad (you split identical states and lost an
optimum). Cure: for every axis you left out, write "the future does not care
about X because …" and see if you believe it. The circular-robber block above is
this trap caught in the act.

**Double counting in a counting DP**, demonstrated below.

**An axis you could have recomputed.** Carrying `(index, count_taken)` when
`count_taken` follows from the other axes multiplies the table for nothing.
Symptom: memory or time limits on an otherwise correct solution.

**An unbounded axis** — a running *sum* as a key when sums reach `10⁹`. The sum
belongs in the value. Symptom: memory explodes.

**A base case that confuses "free" with "impossible".** `f(0) = 0` means the
empty solution is legal and free; `f(0) = −∞` means unreachable. Mixing them
gives the classic *Coin Change* bug where an unmakeable amount reports a number
instead of "impossible" — wrong on exactly the inputs with no solution.

**A cyclic state graph.** A transition leaving the state unchanged, or two states
depending on each other, breaks the evaluation order the proof assumed. Symptom:
`RecursionError` top-down; bottom-up, a cell read before it was final.

**The rolling-array direction.** Collapsing knapsack to one row works, but the
capacity loop must run *downward* for 0/1 and *upward* for unbounded. Symptom:
items used more often than allowed, and only where reuse helps. The direction is
not a convention; it encodes whether the source state is the previous layer or
this one.

```python run
COINS, TARGET = [1, 2, 5], 5


def ways_ordered(coins, target):
    """State = amount. A path through it is a SEQUENCE of coins."""
    f = [0] * (target + 1)
    f[0] = 1
    for a in range(1, target + 1):
        for c in coins:
            if c <= a:
                f[a] += f[a - c]
    return f[target]


def ways_unordered(coins, target):
    """State = (coins considered so far, amount). A path is a MULTISET."""
    f = [0] * (target + 1)
    f[0] = 1
    for c in coins:                       # the coin axis is the outer loop
        for a in range(c, target + 1):
            f[a] += f[a - c]
    return f[target]


def brute_sequences(coins, t):
    return 1 if t == 0 else sum(brute_sequences(coins, t - c) for c in coins if c <= t)


def brute_multisets(coins, t, i=0):
    if t == 0:
        return 1
    if i == len(coins) or t < 0:
        return 0
    return brute_multisets(coins, t - coins[i], i) + brute_multisets(coins, t, i + 1)


print("coins", COINS, "target", TARGET)
print("state = amount            ->", ways_ordered(COINS, TARGET),
      "  ordered sequences (1+2+2 and 2+1+2 both count)")
print("state = (coin, amount)    ->", ways_unordered(COINS, TARGET),
      "  distinct multisets")
assert ways_ordered(COINS, TARGET) == brute_sequences(COINS, TARGET) == 9
assert ways_unordered(COINS, TARGET) == brute_multisets(COINS, TARGET) == 4

for t in range(0, 14):
    assert ways_ordered(COINS, t) == brute_sequences(COINS, t), t
    assert ways_unordered(COINS, t) == brute_multisets(COINS, t), t
print("both agree with brute force for every target 0..13")
print("the two functions differ only in which loop is outer")
```

The two functions differ by the order of two `for` statements and answer
different questions — *Count Ordered Combination Sums* wants the first number,
*Count Unordered Coin Combinations* the second. Nothing in the code says which
you wrote; the state says it. With `amount` alone, `1 → 1+2 → 1+2+2` and
`2 → 2+1 → 2+1+2` are two paths and both count, so you are counting ordered
sequences. The coin-index axis forces each multiset into one canonical assembly
order, restoring the bijection.

:::warn Say which one you are counting, out loud
"How many ways" is ambiguous in English and unambiguous in a state diagram. Name
one concrete object that should be counted once, then find the unique path that
produces it. Two paths means a missing axis.
:::

## What to memorise

Almost nothing. Three questions, one template, one habit.

**The three questions**, asked in order, of any DP problem:

1. What decision do I make next? (the axis you walk)
2. What about the past does that decision depend on that the axis does not
   already tell me? (the extra axes)
3. Can I recompute any of those from the others? (delete them)

**The template**, top-down, because the state is visible in the signature:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def f(i, extra):
    """The best value over all futures, given that <state means this>."""
    if i == n:
        return 0                      # or -inf if this state is infeasible
    return max(f(i + 1, g(extra)) + cost(i, choice) for choice in options(i, extra))
```

**The sentence** that turns a problem into a state: *"Two partial solutions are
the same when every future is worth the same to both."* And its test: *name
something the future cares about that my state does not record.* If you cannot,
the state is sufficient.

**The habit**: write the docstring before the code — a full English sentence
saying what `f(state)` *is*, with the word "all" in it. "`f(i, j)` is the maximum
profit over **all** ways of trading in days `i..n-1` having used `j`
transactions." A DP you cannot describe in one such sentence is one you are
guessing at, and its base cases will be wrong.

Numbers worth carrying: `10⁸` simple operations per second as a budget;
`2²⁰ ≈ 10⁶`, so subset DP lives at `n <= 20`; and the product rule — two axes of
size 1000 is a million states, three is a billion.

## Check yourself

:::check
Why does *Best Time to Buy and Sell Stock* need two numbers per day rather than
one, when the question asks for a single number?
--
Because "best profit so far" is an answer, not a summary. To extend it to day
`i + 1` you need the cheapest price available to buy at, and that is not
recoverable from the profit.

Formally, assumption (A2) fails: two prefixes with the same best-profit-so-far
can have different cheapest buys, so the future "sell on day `i + 1`" is worth
different amounts to them. The repair is the smallest thing that restores it —
one bit, "am I holding a share", whose value under `hold` is exactly the negated
minimum price. Two numbers per day, only one of them ever reported.
:::

:::check
Someone says: "To be safe, put everything you know into the state — extra axes
can only make it more correct." Where are they wrong?
--
On two counts, and the second is the interesting one.

The obvious one: the state space is a product, so an extra axis *multiplies*
time and memory. Carried to its conclusion, a state recording the entire decision
prefix is perfectly sufficient and is exactly the brute force — every node
distinct, nothing merged, `bⁿ` work. A state's job is not to be sufficient but to
be the *smallest* sufficient thing. Merging is the whole mechanism.

The subtler one: an extra axis can make a correct program wrong. Add a component
that two routes to the same situation compute differently and you split one state
into several; a counting DP will then count the same object more than once. Extra
axes are neither free nor safe.
:::

:::check
You are counting sequences with a DP whose state is `amount`, and the answer
comes out too large. Before touching the code, what single question tells you
where the bug is?
--
*Name one object that should be counted once, and find every path through the
state graph that produces it.* If there are two, the state is missing an axis.

With `amount` alone, the multiset `{1, 2, 2}` is produced by the paths `1,2,2`
and `2,1,2` and `2,2,1`, so it is counted three times. Adding a "coin types
considered so far" axis forbids going back to an earlier coin type, which forces
one canonical assembly order per multiset and restores the bijection. Nothing
about the loops says which you wrote; only the state does.
:::

:::check
The proof required the state graph to be acyclic (or a convergence argument).
Give a concrete way to break this, and say what the program does.
--
Add a decision that does not move the position axis — in a grid path DP, allow
all four directions rather than only right and down. Then `f(r, c)` depends on
`f(r, c+1)`, which depends on `f(r, c)`.

Top-down, that is infinite mutual recursion: a stack overflow, or a wrong answer
if you memoise an in-progress state. Bottom-up it is worse — the loops run,
nothing crashes, and cells are read before they are final, so the output is a
deterministic, plausible, wrong number.

The fix is not a DP trick. A cyclic state graph with non-negative costs is a
shortest-path problem: use [[dijkstra]], or [[bfs]] if every edge costs the same,
and let the priority queue supply the evaluation order the recurrence could not.
:::

:::check
*Cheapest Flights Within K Stops* gives you a graph with edge prices and asks for
the cheapest route from source to destination using at most `k` intermediate
stops. Why is `city` not a state, and what does that cost?
--
Because (A1) fails, and dominance with it. Two routes reaching the same city with
different stop counts do not have the same legal futures: one may still afford
three hops, the other none. So the cheapest route to a city is not necessarily
the one worth extending — a dearer route with fewer stops used can beat it. That
is why plain Dijkstra on `city` is wrong here.

The state is `(city, stops used)`. The axis restores the assumption: among routes
with the same city *and* stop count, the cheapest does dominate. The cost is a
factor of `k` in time and memory — `O(k · E)` relaxations, `O(k · V)` states —
the table Bellman-Ford builds when stopped after `k` rounds. See
[[bellman-ford]].
:::
