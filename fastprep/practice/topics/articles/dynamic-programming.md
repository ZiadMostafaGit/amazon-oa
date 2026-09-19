# Dynamic Programming: the Method

> Dynamic programming is not a table. It is the discovery that a tree of
> exponentially many decision sequences is really a small graph of repeated
> situations, plus the discipline of paying for each situation once.

## When you reach for it

You reach for dynamic programming when a problem asks for the best — or the
count — over a set of candidates that is too large to enumerate, and the
candidates are built one decision at a time.

Four hundred and twenty-three problems in this bank use it, which makes it #9 of
150 and the largest single family here. They look nothing alike on the surface:
*Coin Change*, *Edit Distance*, *House Robber*, *Interleaving String*, *Dungeon
Game*, *Count Stepping Numbers In Range*, *Maximum Profit in Job Scheduling*.
What they share is a shape, and the shape has two halves.

**Optimal substructure.** An optimal solution to the whole contains optimal
solutions to parts of itself. If the cheapest way to make 6 units of change
starts with a 3-unit coin, then the rest of it must be the cheapest way to make
3 — otherwise you could swap in the cheaper way and beat something you called
optimal.

**Overlapping subproblems.** Those parts recur. The naive recursion asks "what is
the cheapest way to make 3?" down branch after branch, re-deriving the same
answer each time.

Miss either half and you want a different tool. If the subproblems are optimal
but never repeat — sorting the left and right halves of an array — you have
[[divide-and-conquer]], and memoising buys nothing. If one local rule is provably
safe at every step, you have a [[greedy]] and can skip the table; the proof
obligation moves to an [[greedy-exchange|exchange argument]]. If you must produce
the arrangement itself and the candidates really are few, that is
[[backtracking]].

The sharpest anti-signal is a state that cannot be written down. This works only
when everything the future needs to know about the past fits in a small label.
"Maximise the profit, but never use a coin you have already used twice, and never
two coins whose values sum to a prime" — the label must now remember the whole
multiset, so the state space *is* the candidate space and nothing has been saved.

One honest boundary: many problems here are dynamic programming with a
one-variable state, which makes them look like a scan. *Best Time to Buy and Sell
Stock* keeps a single number, the lowest price so far, and is exactly "the best
transaction ending today is today's price minus the best buy in the prefix".
*Maximum Subarray* is the same idea with a different aggregate and gets its own
chapter, [[kadane]]. If you can see those as DP, you can see the rest.

## The idea

Draw the recursion tree of the brute force. Then notice that many of its nodes
are labelled with the same thing, and glue them together.

That is the whole method. Gluing equal nodes turns a tree into a **directed
acyclic graph**: each distinct label — each *state* — appears once, with edges to
the states it depends on. A tree with `b^d` leaves can collapse into a DAG with
a few thousand nodes, because the number of distinct situations is tiny compared
to the number of ways of arriving at one.

<svg viewBox="0 0 690 250" role="img" aria-label="an exponential recursion tree on the left collapsing into a small directed acyclic graph of distinct states on the right">
  <g>
    <circle cx="145" cy="30" r="16"/>
    <text x="145" y="35" text-anchor="middle">6</text>
    <circle cx="60" cy="105" r="16"/>
    <text x="60" y="110" text-anchor="middle">5</text>
    <circle cx="145" cy="105" r="16"/>
    <text x="145" y="110" text-anchor="middle">3</text>
    <circle class="fill" cx="230" cy="105" r="16"/>
    <text x="230" y="110" text-anchor="middle">2</text>
    <line x1="132" y1="42" x2="73" y2="93"/>
    <line x1="145" y1="46" x2="145" y2="89"/>
    <line x1="158" y1="42" x2="217" y2="93"/>
    <circle cx="20" cy="180" r="16"/>
    <text x="20" y="185" text-anchor="middle">4</text>
    <circle class="fill" cx="62" cy="180" r="16"/>
    <text x="62" y="185" text-anchor="middle">2</text>
    <circle class="fill" cx="104" cy="180" r="16"/>
    <text x="104" y="185" text-anchor="middle">1</text>
    <circle class="fill" cx="150" cy="180" r="16"/>
    <text x="150" y="185" text-anchor="middle">2</text>
    <circle cx="192" cy="180" r="16"/>
    <text x="192" y="185" text-anchor="middle">0</text>
    <circle class="fill" cx="240" cy="180" r="16"/>
    <text x="240" y="185" text-anchor="middle">1</text>
    <line x1="52" y1="120" x2="27" y2="166"/>
    <line x1="60" y1="121" x2="62" y2="164"/>
    <line x1="70" y1="120" x2="97" y2="166"/>
    <line x1="142" y1="121" x2="150" y2="164"/>
    <line x1="152" y1="120" x2="186" y2="167"/>
    <line x1="232" y1="121" x2="239" y2="164"/>
    <text x="130" y="228" text-anchor="middle">tree: the same amount, over and over</text>
    <path d="M 290 130 L 350 130"/>
    <path d="M 350 130 L 338 123"/>
    <path d="M 350 130 L 338 137"/>
    <text x="320" y="115" text-anchor="middle">glue</text>
    <circle cx="410" cy="150" r="16"/>
    <text x="410" y="155" text-anchor="middle">0</text>
    <circle cx="455" cy="150" r="16"/>
    <text x="455" y="155" text-anchor="middle">1</text>
    <circle cx="500" cy="150" r="16"/>
    <text x="500" y="155" text-anchor="middle">2</text>
    <circle cx="545" cy="150" r="16"/>
    <text x="545" y="155" text-anchor="middle">3</text>
    <circle cx="590" cy="150" r="16"/>
    <text x="590" y="155" text-anchor="middle">4</text>
    <circle cx="635" cy="150" r="16"/>
    <text x="635" y="155" text-anchor="middle">5</text>
    <circle class="fill" cx="665" cy="90" r="16"/>
    <text x="665" y="95" text-anchor="middle">6</text>
    <path d="M 635 134 Q 660 115 660 106"/>
    <path d="M 545 134 Q 610 85 651 84"/>
    <path d="M 500 134 Q 590 55 655 76"/>
    <text x="540" y="228" text-anchor="middle">DAG: seven states, each solved once</text>
  </g>
</svg>

Once the picture is a DAG, the method is mechanical — always the same four
questions:

1. **What is the state?** The smallest label that makes the future independent of
   the past. This is the only hard question; it has its own chapter,
   [[state-design]].
2. **What is the transition?** How the value at a state is built from the values
   at the states it points to.
3. **What are the base cases?** The states with no outgoing edges, whose values
   are known outright.
4. **In what order do I evaluate?** Any topological order of the DAG. Going
   forwards and filling an array is *tabulation*; going backwards from the answer
   and caching is *memoisation* ([[memoization]]). They compute the same values.

The word "programming" here means scheduling, as in a television programme; what
is being scheduled is the order in which the states get evaluated.

## Worked by hand

Coins `{1, 3, 4}`, unlimited supply, target 6, minimise the number of coins.
This is *Coin Change*, which appears in this bank from four different companies,
and *Minimum Coins for a Target* is the same problem.

State: `dp[a]` = fewest coins summing to exactly `a`. Base: `dp[0] = 0`.
Transition: `dp[a] = 1 + min(dp[a-1], dp[a-3], dp[a-4])`, skipping any coin
larger than `a`.

| `a` | via `1`: `dp[a-1]+1` | via `3`: `dp[a-3]+1` | via `4`: `dp[a-4]+1` | `dp[a]` | coin taken |
| --- | --- | --- | --- | --- | --- |
| 0 | — | — | — | 0 | — |
| 1 | `0+1 = 1` | — | — | **1** | 1 |
| 2 | `1+1 = 2` | — | — | **2** | 1 |
| 3 | `2+1 = 3` | `0+1 = 1` | — | **1** | 3 |
| 4 | `1+1 = 2` | `1+1 = 2` | `0+1 = 1` | **1** | 4 |
| 5 | `1+1 = 2` | `2+1 = 3` | `1+1 = 2` | **2** | 1 or 4 |
| 6 | `2+1 = 3` | `1+1 = 2` | `2+1 = 3` | **2** | 3 |

The answer is 2, and the coins are `3 + 3`.

<svg viewBox="0 0 640 195" role="img" aria-label="the dp array for amounts zero to six, with three arcs pointing from cells two, three and five into cell six">
  <g>
    <rect x="20" y="110" width="55" height="42" rx="4"/>
    <text x="47" y="136" text-anchor="middle">0</text>
    <rect x="75" y="110" width="55" height="42" rx="4"/>
    <text x="102" y="136" text-anchor="middle">1</text>
    <rect x="130" y="110" width="55" height="42" rx="4"/>
    <text x="157" y="136" text-anchor="middle">2</text>
    <rect x="185" y="110" width="55" height="42" rx="4"/>
    <text x="212" y="136" text-anchor="middle">1</text>
    <rect x="240" y="110" width="55" height="42" rx="4"/>
    <text x="267" y="136" text-anchor="middle">1</text>
    <rect x="295" y="110" width="55" height="42" rx="4"/>
    <text x="322" y="136" text-anchor="middle">2</text>
    <rect class="fill" x="350" y="110" width="55" height="42" rx="4"/>
    <text x="377" y="136" text-anchor="middle">2</text>
    <text x="47" y="170" text-anchor="middle">a=0</text>
    <text x="157" y="170" text-anchor="middle">a=2</text>
    <text x="267" y="170" text-anchor="middle">a=4</text>
    <text x="377" y="170" text-anchor="middle">a=6</text>
    <path d="M 157 110 Q 267 25 372 104"/>
    <path d="M 212 110 Q 295 45 375 104"/>
    <path d="M 322 110 Q 350 85 378 104"/>
    <text x="258" y="38" text-anchor="middle">+4</text>
    <text x="300" y="60" text-anchor="middle">+3</text>
    <text x="345" y="88" text-anchor="middle">+1</text>
    <text x="470" y="120">every arrow points strictly left:</text>
    <text x="470" y="140">one pass, left to right, is legal</text>
  </g>
</svg>

Four things in that table are worth more than the answer.

**Greedy loses here, and you can see exactly where.** "Take the largest coin that
fits" takes a 4 and lands on `dp[2] = 2`, for 3 coins total; the optimal first
move takes a 3 and lands on `dp[3] = 1`, for 2. Greedy commits to the biggest
immediate step, while the table compares the *consequences* of each first step —
precisely the information greedy refuses to gather. With coins `{1, 5, 10, 25}`
greedy happens to be right, which is why the failure surprises people.

**Row 6 contains row 3 inside it.** The optimal `3 + 3` is "one 3, then the
optimal solution for 3", and that is itself a single 3. Optimal substructure is
not an abstraction here; it is literally how the row was filled.

**Row 5 has a tie.** Both `1 + dp[4]` and `4 + dp[1]` give 2. The *value* is
unique, the *witness* is not. If a problem asks for the coins and not just the
count, you must record the choice as you make it — reconstructing it afterwards
by re-deriving "which coin was best" can pick a different tie and, in problems
with extra constraints, a wrong one.

**Every arrow points strictly left.** That is not a cosmetic property. It is why
a single loop `for a in 1..6` is a valid evaluation order: when we compute
`dp[a]`, every cell it reads is already final. Get that wrong and the code still
runs and still prints a number.

## Why it is correct

The proof obligation for a dynamic program is not "the loop fills the array". It
is: **the recurrence computes the true optimum at every state**. That splits
into two inequalities, and only one of them is interesting.

:::proof The coin-change recurrence equals the true optimum
**Setup.** Let `C = {c₁, …, c_k}` be positive integers. For an amount `a ≥ 0`
let `S(a)` be the set of finite multisets of elements of `C` whose elements sum
to `a`, and let `opt(a) = min{ |M| : M ∈ S(a) }`, with `opt(a) = ∞` when `S(a)`
is empty. Define

    dp(0) = 0
    dp(a) = 1 + min{ dp(a − c) : c ∈ C, c ≤ a }     for a ≥ 1

where the minimum of an empty set is `∞`.

**Well-definedness.** Every coin is at least 1, so `dp(a)` refers only to
`dp(b)` with `b < a`. The dependency relation on `{0, …, A}` is therefore a
strict partial order — the state graph is acyclic — and `dp` is a legitimate
definition by strong recursion, not a circular one.

**Claim.** `dp(a) = opt(a)` for every `a ≥ 0`. By strong induction on `a`.

**Base case `a = 0`.** No nonempty multiset of positive integers sums to 0, so
`S(0) = {∅}` and `opt(0) = 0 = dp(0)`.

**Inductive step.** Fix `a ≥ 1` and assume `dp(b) = opt(b)` for every `b < a`.

*Soundness — `opt(a) ≤ dp(a)`: everything the recurrence claims is achievable.*
If `dp(a) = ∞` there is nothing to prove. Otherwise `dp(a) = 1 + dp(a − c)` for
some `c ∈ C` with `c ≤ a` and `dp(a − c)` finite. By the hypothesis,
`dp(a − c) = opt(a − c)`, so some multiset `M ∈ S(a − c)` has `|M| = dp(a − c)`.
Then `M ∪ {c}` sums to `a`, so it lies in `S(a)` and witnesses
`opt(a) ≤ |M| + 1 = dp(a)`.

*Completeness — `dp(a) ≤ opt(a)`: every optimal solution is covered by some
branch.* If `opt(a) = ∞` there is nothing to prove. Otherwise pick any optimal
`M ∈ S(a)` with `|M| = opt(a)`. Since `a ≥ 1` and every coin is positive, `M` is
nonempty; choose any element `c ∈ M`. The multiset `M \ {c}` sums to `a − c`, so
it belongs to `S(a − c)` and hence `opt(a − c) ≤ |M| − 1`. Also `c ≤ a`, so the
branch for `c` is one of the branches the minimum ranges over, and `a − c < a`,
so the hypothesis gives `dp(a − c) = opt(a − c) ≤ opt(a) − 1`. Therefore
`dp(a) ≤ 1 + dp(a − c) ≤ opt(a)`.

Both inequalities give `dp(a) = opt(a)`, completing the induction.

**Evaluation order.** The loop `for a = 1 … A` visits the states in an order in
which every predecessor of `a` (namely `a − c < a`) has already been assigned its
final value, so each read returns `dp(a − c)` and not a placeholder. Hence the
array computed by the loop is the function `dp`, which is `opt`. ∎
:::

The completeness half is the entire method in miniature, and it is worth
restating in words, because every DP proof you will write is this sentence with
different nouns: **take an arbitrary optimal solution, identify its last decision,
delete it, and observe that what remains solves a smaller instance the recurrence
already considered.** If that deletion always lands inside the set of subproblems
your recurrence enumerates, the optimum cannot be missed. If some optimal
solution's last decision is not one of your branches, the recurrence is wrong, and
no amount of debugging the loop will help.

Now name what the proof leaned on, because that list is where the bugs live.

- **Acyclicity**, used to make `dp` well defined and to justify the loop order. It
  came from `c ≥ 1`. A "coin" of value 0, or a transition that can return to the
  same state, makes the recurrence an equation rather than a definition, and you
  need relaxation to a fixed point instead — which is why cyclic shortest paths
  belong to [[bellman-ford]] and not here.
- **Sufficiency of the state.** The proof deleted a coin and looked only at the
  remaining amount, which is legitimate because coins are unlimited and order does
  not matter. Make the supply finite and `a` is no longer a state: which coins
  were spent now matters, and you need a second dimension. That is the difference
  between [[unbounded-knapsack]] and [[knapsack]], and the most common modelling
  error in this family.
- **Additivity and monotonicity of the objective.** Total cost is `1 +` the
  subcost, and `x ↦ 1 + x` is increasing, so a better subsolution is never a worse
  whole. Ratios, averages and variances break this: a better prefix can be a worse
  whole, and optimal substructure quietly fails.
- **Covering is enough for a min, but not for a count.** The completeness step
  only needed *at least one* branch to reach each optimal solution; overlapping
  branches are harmless when you are taking a minimum. A counting recurrence
  needs the branches to be **exhaustive and pairwise disjoint**, or it
  double-counts. Same recurrence, strictly stronger obligation — see
  [[counting-dp]], and the first trap below.
- **Values are final when read.** Stated separately from the maths because in
  code it is a property of your loop, not of your recurrence. Most "my DP is
  subtly wrong" bugs are here.

## What it costs

Start with the brute force, so the improvement is a number and not a feeling. The
naive recursion does `O(1)` work and then recurses once per coin:

    T(a) = 1 + Σ_{c ∈ C, c ≤ a} T(a − c),    T(0) = 1

Take `C = {1, 2}` to solve it in closed form. Then `T(a) = T(a−1) + T(a−2) + 1`.
Setting `U(a) = T(a) + 1` gives `U(a) = U(a−1) + U(a−2)`, the Fibonacci
recurrence, so `T(a) = Θ(φ^a)` with `φ = (1+√5)/2 ≈ 1.618`. The cost is
exponential in the *amount*, and the amount is a number in the input, not the
size of the input.

Now count the memoised version, and note that the counting argument is generic —
it is the same for every dynamic program:

> **total work = Σ over states of (work to evaluate that state)**

because each state is evaluated exactly once, and every other visit is a cache
hit costing `O(1)`. Here there are `A + 1` states and each one loops over `k`
coins, so the total is `O(A·k)` time and `O(A)` space. Going from `Θ(1.618^A)` to
`Θ(A·k)` did not require a cleverer recurrence; it required not recomputing.

Three costs people forget.

**The work inside a transition.** "`n²` states, `O(1)` transitions" is often a
lie. A DP over substrings that writes `s[i:j]` inside the loop pays `O(j − i)`
per slice, and the honest total is `O(n³)`. Anything that builds a tuple, sorts a
small list or calls a looping helper belongs in the per-state cost.

**The key.** A `dict` keyed by tuples hashes every component on every lookup; a
list of lists indexed by integers does not. At `10⁶` states that is the difference
between a solution and a timeout, and it is invisible in the asymptotics. See
[[hash-tables]].

**Pseudo-polynomiality.** `O(A·k)` for coin change and `O(n·W)` for knapsack are
polynomial in the *values*, and the values are written in binary in the input, so
`W = 10⁹` occupies about 30 bits and the algorithm is exponential in the input
length. This is not pedantry: it is why *0/1 Knapsack* states a small capacity,
why *Budget-Constrained Project Selection* bounds the budget, and why a knapsack
with a nine-digit capacity needs [[meet-in-the-middle]] or a different
formulation instead. When you read a constraint like `target ≤ 10⁴`, the problem
setter is telling you the intended state space.

Space is `O(|states|)` unless the transition reaches back only a bounded
distance, in which case a rolling window suffices: coin change needs the last
`max(C)` entries, a grid DP the previous row. Rolling is the first optimisation
to reach for and the one most likely to break reconstruction, since it throws
away the choices you would need to replay.

## The implementation

Three versions of the same recurrence: the brute force with a call counter, the
memoised recursion, and the table with reconstruction. The counters are the
point — they turn the complexity derivation into an observation.

```python run
INF = float("inf")
COINS = (1, 3, 4)


def naive(a, counter):
    counter[0] += 1
    if a == 0:
        return 0
    best = INF
    for c in COINS:
        if c <= a:
            best = min(best, 1 + naive(a - c, counter))
    return best


def topdown(a, counter):
    memo = {}

    def go(x):
        if x == 0:
            return 0
        if x in memo:
            return memo[x]
        counter[0] += 1                       # counted once per distinct state
        best = INF
        for c in COINS:
            if c <= x:
                best = min(best, 1 + go(x - c))
        memo[x] = best
        return best

    return go(a)


def bottomup(A):
    dp = [INF] * (A + 1)
    took = [None] * (A + 1)
    dp[0] = 0
    for a in range(1, A + 1):                 # a valid topological order
        for c in COINS:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
                took[a] = c                   # record the choice, do not re-derive it
    return dp, took


def coins_used(took, A):
    out, a = [], A
    while a > 0:
        out.append(took[a])
        a -= took[a]
    return sorted(out)


dp, took = bottomup(6)
print("dp[0..6] =", dp)
print("best change for 6:", coins_used(took, 6), "->", dp[6], "coins")
assert dp == [0, 1, 2, 1, 1, 2, 2]
assert coins_used(took, 6) == [3, 3] and sum(coins_used(took, 6)) == 6

greedy, a = 0, 6                              # 'take the largest that fits'
while a:
    a -= max(c for c in COINS if c <= a)
    greedy += 1
print("greedy needs", greedy, "coins; the table needs", dp[6])
assert greedy == 3 > dp[6]

A = 26
c1, c2 = [0], [0]
assert naive(A, c1) == topdown(A, c2) == bottomup(A)[0][A]
print("amount %d: naive made %d calls, memoised evaluated %d states"
      % (A, c1[0], c2[0]))
assert c1[0] > 200 * c2[0]                    # exponential vs linear, measured
```

Three lines carry the weight.

`if x in memo: return memo[x]` is the entire difference between exponential and
linear, and the counter proves it: the memoised run evaluates one state per
amount while the naive run makes hundreds of times more calls at `A = 26`, and
the gap widens with every step.

`took[a] = c` sits in the same branch that updates `dp[a]`, which is how the
witness stays consistent with the value. Recording it in a second pass is how you
pick a different member of a tie.

`for a in range(1, A + 1)` is the topological order, stated as a loop. Whenever
you write a tabulation, ask what that loop is silently claiming: *is every cell I
read already final?* Here `a − c < a`, so yes.

## Variants you will meet

The rest of this section of the syllabus is this method with different state
spaces. Read them in roughly this order.

**Top-down vs bottom-up.** Same values, different engineering: memoisation visits
only reachable states and needs no order, but can blow the stack; tabulation is
faster and allows rolling arrays, but you must name the order. See
[[memoization]].

**One-dimensional DP.** State is a position. *House Robber*, *Climb Stairs with
One, Two, or Three Steps*, *Decode Ways*, *Word Break*. See [[dp-1d]], and
[[kadane]] for the running-aggregate special case.

**Grids and two sequences.** State is a pair of indices. *Minimum Path Sum*,
*Dungeon Game*, *Count Paths from the Top Left to the Bottom Right* are
[[dp-2d]]; *Edit Distance*, *Longest Common Subsequence Length*, *Interleaving
String* and *Is Regex Matching* are [[dp-strings]].

**Subset-sum shaped.** State is (index, remaining budget). *0/1 Knapsack*,
*Subset Sum to Target*, *Closest Subsequence Sum* — see [[knapsack]]; with
unlimited copies, *Coin Change* and [[unbounded-knapsack]].

**Counting.** Replace `min` with `+`; the branches must then partition, not merely
cover. *Count Staircase Ways*, *Count Four-Digit Codes with Sum S*, *Count Good
Strings*. See [[counting-dp]] and [[modular-arithmetic]].

**Intervals and partitions.** State is a range `(i, j)` and the transition picks a
split point. *Minimum Matrix-Chain Multiplications*, *Minimum Cost to Merge
Stones*, *Split a String into Three Palindromes*. See [[partition-dp]].

**Trees.** State is a subtree, evaluated in post-order. *Binary Tree Maximum Path
Sum*, *Binary Tree Cameras*, *Tree-Dependent Knapsack*. See [[tree-dp]].

**Bitmask.** State is a subset, for `n ≤ 20`. *Shortest Path Visiting All Nodes*,
*Shortest Round Trip Through All Deliveries*. See [[dp-bitmask]].

**Digits.** State is (position in the expansion, a small summary, is the prefix
already below the bound). *Count Stepping Numbers In Range*, *Count Numbers with
Digit Sum*. See [[digit-dp]].

**Games.** Two players, the value of a state is defined by the opponent's best
reply. *Stone Game III*, *Coin Game From The Ends*, *Optimal Card Game Score*.
See [[game-dp]].

### DP optimisation: making the transition cheaper

When `|states| × transitions` is too big, the states are usually fine and the
transitions are the problem. The fix is always the same in spirit: the inner
`min` or `max` is a query over a structured set, so answer it with a data
structure instead of a loop.

**Monotonic deque**, when the transition ranges over a *sliding window* of
previous states: `dp[i] = a[i] + max(dp[i-k] … dp[i-1])`. Keep the candidate
indices in a deque, decreasing in `dp` value; the front is the window maximum.
Each index is pushed once and popped once, so the amortised cost per state is
`O(1)` and `O(n·k)` becomes `O(n)`. See [[monotonic-deque]]; the block below
measures it.

**Convex hull trick**, when the transition has the form
`dp[i] = min_j (dp[j] + b_j · x_i)`. Read each `j` as the line
`y = b_j · x + dp[j]`; the query at `x_i` asks for the lowest line at that
abscissa, which is a point on the **lower envelope** of a set of lines. Maintaining
that envelope costs `O(log n)` per operation, or `O(1)` amortised when the slopes
are added in sorted order and the queries are monotone — so `O(n²)` becomes
`O(n log n)` or `O(n)`. The envelope is exactly the lower hull of the dual points
`(b_j, dp[j])`, which is why it is a [[convex-hull]] in disguise.

**Range queries by segment or Fenwick tree**, when the transition is "the best
over earlier states with a smaller key". That is how *Longest Increasing
Subsequence With Bounded Adjacent Differences* and *Russian Doll Envelopes* reach
`O(n log n)`. See [[fenwick-tree]], [[segment-tree]] and [[lis]].

**Binary search over the predecessors**, when the states are intervals sorted by
end time: *Maximum Profit in Job Scheduling* finds the last non-overlapping job
with [[binary-search]].

**Divide-and-conquer and Knuth optimisation**, when the optimal split point is
monotone in the range — interval DPs drop from `O(n³)` to `O(n²)`.

**Matrix exponentiation**, when the recurrence is linear with constant
coefficients and the index is huge: `n = 10¹⁸` steps in `O(log n)` matrix
multiplications. See [[matrix-exponentiation]].

```python run
import random
from collections import deque

# dp[i] = a[i] + max(dp[i-k] .. dp[i-1]);  dp[0] = a[0]
# the same recurrence, evaluated two ways, with the inner work counted.


def by_scan(a, k):
    n, ops = len(a), 0
    dp = [0] * n
    dp[0] = a[0]
    for i in range(1, n):
        best = -10 ** 18
        for j in range(max(0, i - k), i):
            ops += 1
            if dp[j] > best:
                best = dp[j]
        dp[i] = a[i] + best
    return dp[-1], ops


def by_deque(a, k):
    n, ops = len(a), 0
    dp = [0] * n
    dp[0] = a[0]
    dq = deque([0])                       # indices, dp values strictly decreasing
    for i in range(1, n):
        while dq[0] < i - k:              # slide the window
            dq.popleft()
            ops += 1
        dp[i] = a[i] + dp[dq[0]]          # front is the window maximum
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()                      # dominated: later and not larger
            ops += 1
        dq.append(i)
        ops += 1
    return dp[-1], ops


rng = random.Random(4)
for _ in range(300):
    n = rng.randint(1, 30)
    k = rng.randint(1, 6)
    arr = [rng.randint(-9, 9) for _ in range(n)]
    assert by_scan(arr, k)[0] == by_deque(arr, k)[0], (arr, k)
print("300 random instances: the deque agrees with the scan on every one")

big = [rng.randint(-1000, 1000) for _ in range(1200)]
v1, o1 = by_scan(big, 300)
v2, o2 = by_deque(big, 300)
print("n=1200, k=300 ->", v1, "; inner steps: scan", o1, "deque", o2)
assert v1 == v2 and o2 < o1 // 40
print("each index enters and leaves the deque once: %.1fx fewer steps" % (o1 / o2))
```

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"In how many ways…", especially with "modulo 10⁹ + 7".** The modulus exists
   because the count is astronomical, so you are not going to enumerate. *Count
   Staircase Ways*, *Count Good Strings*, *Count Four-Digit Codes with Sum S*.
2. **A second small bound next to `n`.** `1 ≤ n ≤ 100` *and* `1 ≤ target ≤ 10⁴`
   is the setter handing you the state space. Likewise "at most `k` transactions"
   in *Maximum Profit with at Most K Transactions* and "at most `k` stops" in
   *Cheapest Flights Within K Stops* — `k` is a dimension.
3. **"Minimum / maximum" over take-or-leave decisions where taking one constrains
   the next.** *House Robber* (no two adjacent), *0/1 Knapsack* (weights fit).
4. **Two sequences to be aligned.** Insert, delete, match, skip — a grid over the
   two index positions. *Edit Distance*, *Longest Common Subsequence Length*,
   *Interleaving String*.
5. **A grid with monotone movement**, right and down only, or a DAG of stages:
   *Minimum Path Sum*, *Path Through an O/X Grid Using Only Right and Down*,
   *Factory Cost — Minimum Cost Across Stages*.
6. **"Optimal play by both sides."** The value of a position is defined by the
   opponent's best reply: minimax, which is DP on positions.
7. **A brute force describable as "try every choice at every step".** Write that
   recursion first; if its argument list is short and its arguments repeat, you
   already have the state.

The anti-signals:

- **A safe local rule exists.** If you can prove an exchange argument, use
  [[greedy]] — shorter and faster. Coin change is the cautionary tale in both
  directions: greedy is wrong for `{1, 3, 4}` and right for ordinary currency,
  and only a proof tells them apart.
- **Subproblems that never repeat.** That is [[divide-and-conquer]]; the cache
  would only waste memory.
- **The state would have to be the whole history**, or the answer is a structure
  and `n ≤ 12` — [[backtracking]], not DP.
- **It smells like DP but the transitions form a cycle.** Shortest paths with
  arbitrary edges are not acyclic; that is [[bellman-ford]] or [[dijkstra]],
  which are DP over a *relaxation* schedule rather than a topological one. On an
  acyclic graph the two coincide — see [[topological-sort]].

## Traps

**Counting with a covering, not a partitioning, recurrence.** For a minimum,
double-covered solutions are harmless. For a count they are fatal, and the two
loop orders below differ by nothing except which loop is outside. *Count
Unordered Coin Combinations* and *Count Ordered Combination Sums* are the same
input asking the two different questions; getting the loops the wrong way round
answers the other problem, silently, with a plausible number.

**A forward in-place loop in 0/1 knapsack.** `dp[w] += dp[w - weight]` scanned
upwards reads a cell that has already been updated *in this item's own pass*, so
the item gets used more than once and you have accidentally solved
[[unbounded-knapsack]]. Symptom: answers that are too good, and only on inputs
where reusing an item helps.

**Initialising "unreachable" as 0.** `0` means "achievable at zero cost"; `∞` (or
`-∞` for a maximum) means "impossible". Symptom: a min-cost problem that returns
0 for an impossible instance.

**A state that is not sufficient.** The recurrence is fine, the loop is fine, one
test is wrong. Something the future depends on was left out of the label — items
used, parity, whether the previous cell was taken. The tell: you cannot state what
`dp[i]` means in one sentence without an "and also".

**A memo key that includes irrelevant fields.** Correct, but never hits, so the
run stays exponential. Symptom: a timeout on an algorithm you believe is
polynomial. Count your distinct states before blaming the language.

**Python recursion depth.** A top-down DP over `10⁵` positions raises
`RecursionError` around a thousand frames; convert to tabulation rather than
raising the limit. See [[recursion]].

**Taking the modulus only at the end.** With `10⁹+7` the intermediates stay
correct in Python but the arithmetic slows on huge integers, and in any other
language it overflows. Reduce at every addition.

```python run
def combinations(coins, t):          # unordered: each coin considered once
    dp = [0] * (t + 1)
    dp[0] = 1
    for c in coins:                  # <- coin loop OUTSIDE
        for a in range(c, t + 1):
            dp[a] += dp[a - c]
    return dp[t]


def permutations(coins, t):          # ordered: sequences, not multisets
    dp = [0] * (t + 1)
    dp[0] = 1
    for a in range(1, t + 1):        # <- amount loop OUTSIDE
        for c in coins:
            if c <= a:
                dp[a] += dp[a - c]
    return dp[t]


COINS, T = [1, 2, 5], 5
print("coins", COINS, "target", T)
print("  unordered multisets:", combinations(COINS, T))
print("  ordered sequences  :", permutations(COINS, T))
assert combinations(COINS, T) == 4        # 11111, 1112, 122, 5
assert permutations(COINS, T) == 9        # the same four, in every order
print("one loop swap, two different problems\n")


def knap01(w, v, cap):
    dp = [0] * (cap + 1)
    for i in range(len(w)):
        for c in range(cap, w[i] - 1, -1):     # DOWNWARD: dp[c - w] is last round's
            dp[c] = max(dp[c], dp[c - w[i]] + v[i])
    return dp[cap]


def knap_forward(w, v, cap):
    dp = [0] * (cap + 1)
    for i in range(len(w)):
        for c in range(w[i], cap + 1):         # upward: dp[c - w] may already
            dp[c] = max(dp[c], dp[c - w[i]] + v[i])   # include item i
    return dp[cap]


def brute(w, v, cap):
    best = 0
    for mask in range(1 << len(w)):
        tw = sum(w[i] for i in range(len(w)) if mask >> i & 1)
        if tw <= cap:
            best = max(best, sum(v[i] for i in range(len(v)) if mask >> i & 1))
    return best


W, V, CAP = [2, 4], [5, 6], 8
print("weights", W, "values", V, "capacity", CAP)
print("  0/1, downward loop:", knap01(W, V, CAP), "(matches brute force", brute(W, V, CAP), ")")
print("  upward loop       :", knap_forward(W, V, CAP), "- it reused item 0 four times")
assert knap01(W, V, CAP) == brute(W, V, CAP) == 11
assert knap_forward(W, V, CAP) == 20
```

Both are the same bug in different clothes: a cell was read before it held the
value the recurrence meant. That is the fifth assumption from the proof, and why
"in what order do I evaluate?" is one of the four questions.

## What to memorise

Not a template — the state space differs every time. Memorise the procedure.

**The four questions**, asked in this order, on paper, before any code: *what is
the state, what is the transition, what are the base cases, in what order do I
evaluate?* If you cannot answer the first, nothing after it can be right.

**The sentence** that turns a problem into a dynamic program: *"What is the last
decision in an optimal solution, and what smaller instance does deleting it leave
behind?"* If the answer is a short label, that label is your state, and the
recurrence writes itself.

**The habit**: write down, in one English sentence, what `dp[i][j]` *means*,
before writing the loop. "The minimum cost to process the first `i` items using
exactly `j` machines." If the sentence needs an "and also", the state is
incomplete, and you have found the bug before you had it.

Numbers worth carrying, all of them just `states × transitions`: a `10³ × 10³`
table with `O(1)` transitions is `10⁶` cells and comfortable; the same table with
an `O(n)` inner loop is `10⁹` and is not. Bitmask DP is capped by `n ≤ 20`, where
`2²⁰ ≈ 10⁶` states and `n · 2ⁿ ≈ 2 × 10⁷` transitions are still tractable.
A knapsack is `n × W`, and `W` is a *value*, so read the constraint on `W` before
you commit.

## Check yourself

:::check
In coin change the state is just the remaining amount, but in 0/1 knapsack you
also need an item index. Why — and what exactly goes wrong if you drop the index?
--
Because the state must make the future independent of the past, and the legal
futures differ. With unlimited coins, the continuations from "amount `a` remains"
are the same whichever coins you already spent, so `a` is a sufficient summary.
With each item available once, they depend on *which* items are gone — something
`a` alone cannot say.

Drop the index and nothing prevents `dp[c - w[i]]` from already containing item
`i` — the forward-loop bug in the Traps block, giving 20 instead of 11. The index
is compressed away in the standard one-array implementation but still present: it
lives in the *loop order*, which guarantees `dp[c - w[i]]` is the previous item's
value. That is why the inner loop's direction is load-bearing, not a style
choice.
:::

:::check
Why is "every optimal solution is covered by some branch" enough for a minimising
DP, while a counting DP needs more?
--
Because multiplicity is invisible to `min`. Achievable-but-worse branches are
discarded, and an optimum reachable through two branches merely offers the same
value twice. So *soundness* (every branch is achievable) plus *covering* (every
optimum is offered at least once) pins the value exactly.

A count sums over branches, and a sum is sensitive to multiplicity: an object
reachable two ways is counted twice, so the branches must partition the solution
set — exhaustive *and* pairwise disjoint. That is the whole content of the
loop-order difference between *Count Unordered Coin Combinations* (coins outside,
so each multiset is built in one canonical order) and *Count Ordered Combination
Sums* (amount outside, so every ordering is its own branch).
:::

:::check
Someone says: "Top-down memoisation and bottom-up tabulation are the same
algorithm, so it never matters which you write." Where are they wrong?
--
They are right about the values and wrong about almost everything else.

Bottom-up requires you to name a topological order, and it computes *every* state
in the range. Top-down needs no order — the call stack discovers one — and
computes only the states reachable from the answer, which on a sparse state space
is a small fraction, so memoisation is genuinely faster there.

Against that: Python's recursion limit kills top-down at around a thousand deep,
which a chain DP over `10⁵` positions hits immediately; a `dict` keyed by tuples
is much slower per access than an integer-indexed list; and the space-saving
tricks — rolling one row, the single-array knapsack — exist only bottom-up,
because they depend on knowing when a cell becomes dead. The choice is a real
engineering decision with a real failure mode on each side.
:::

:::check
A candidate proves their DP correct by saying: "`dp[a]` is computed as the
minimum over all the coins, so it is the minimum." What is missing from that
argument, and what would fix it?
--
It assumes the conclusion. The recurrence minimises over values stored at *other
states*, so the sentence only says "the minimum of those numbers is their
minimum". It never connects those numbers to the true optimum over multisets, and
never rules out an optimal solution that no branch reaches.

The fix is the two-sided induction above. One direction shows every value the
recurrence produces is realised by an actual multiset, so it never promises the
impossible. The other takes an *arbitrary* optimal solution, removes its last
coin, and shows the remainder is a solution to a strictly smaller state the
recurrence already ranges over — so no optimum can hide between the branches. The
second direction is where a wrong state design gets caught, which is why it is
the half worth writing out.
:::

:::check
A problem gives `n ≤ 200` items and a capacity `W ≤ 10⁹`, and asks for the
maximum value of a subset that fits. Why is the textbook `O(nW)` knapsack the
wrong answer, and what does the constraint pair suggest instead?
--
Because `O(nW)` is pseudo-polynomial: `nW ≈ 2 × 10¹¹` operations and `W + 1`
array cells fit in neither time nor memory. The complexity is polynomial in the
magnitude of a number, not the length of the input.

The pairing of a tiny `n` with a huge `W` is the signal. With `n ≤ 40`, split the
items in half and match `2²⁰` subset sums per side — [[meet-in-the-middle]]. If
instead the total *value* is small, flip the table: `dp[v]` = least weight
achieving value `v`, which is `O(n · ΣV)`. Making the small quantity the state is
the most useful modelling reflex in this family.
:::
