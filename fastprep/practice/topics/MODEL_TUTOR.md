# The model for a tutor chapter

This is a real tutoring exchange about 0/1 knapsack, kept as the reference for how a
Version 2 chapter teaches (see AUTHORING.md). The learner's own words are summarised
in the [brackets]. The tutor's answers are kept as they were. What to copy is the
method, not the text: derive from brute force, kill wrong instincts with
counterexamples, trace real numbers, map code to idea line by line, demonstrate the
one subtle line both ways, and end with hand exercises.

---

[The learner asked to learn knapsack DP deeply: the ideas, the techniques, every
variation, and how to think about it.]

## Knapsack DP, from first principles

I'll build this in layers: the core idea, the derivation, the thinking framework,
then the variations and the traps.

### 1. The core idea

Knapsack is a family of problems with this shape:

> You have items. Each decision is independent except that all decisions share a
> limited resource. Optimize (or count, or test feasibility) over the choices.

The key insight is that **the only thing the past tells the future is how much
resource is left**. Once you've decided about items 1..i and used capacity c, it
doesn't matter which items you took. The future only cares about (i, c). That is the
whole reason DP works here, and it's the question you should ask in every DP
problem: *"What is the minimum information about the past that I need to decide the
future?"*

Greedy fails because items are indivisible. Taking the best value/weight ratio can
leave wasted capacity that a different combination would have filled. Brute force is
2^n. DP collapses all subsets that lead to the same (i, c) into one state.

### 2. Deriving 0/1 knapsack (don't memorize it, derive it)

Step 1: brute force. For each item, take it or skip it.

    f(i, c) = max value using items i..n with capacity c
    f(i, c) = max( f(i+1, c),                 // skip
                   v[i] + f(i+1, c - w[i]) )  // take, if w[i] <= c
    f(n+1, c) = 0

Step 2: notice overlap. Different paths reach the same (i, c). Memoize it: n x W
states, O(1) transition, so O(nW).

Step 3: make it iterative. dp[i][c] depends only on row i-1.

Step 4: compress to 1D. dp[c] depends on dp[c] and dp[c - w] from the previous row.
Iterating c downward guarantees dp[c - w] hasn't been overwritten yet, so it still
holds the old row:

    for each item (w, v):
        for (c = W; c >= w; c--)
            dp[c] = max(dp[c], dp[c - w] + v);

**Why downward is the most important line to understand.** If you iterate upward,
dp[c - w] was already updated with this item, so you can use the item multiple
times. That is unbounded knapsack. The loop direction is literally the difference
between "use once" and "use unlimited."

Complexity caveat: O(nW) is pseudo-polynomial. W is a number, and its input size is
log W bits. Knapsack is NP-hard, and that's why W <= ~10^5-10^7 appears in
constraints. If W is huge, you must use a different formulation.

### 3. The thinking framework (ask these every time)

1. What are the items? What is one "decision"?
2. What is the shared resource? (capacity, budget, time, a target sum, number of picks)
3. What am I computing? Max value, min cost, count of ways, or just yes/no feasibility?
4. Can each item be used 0/1 times, unlimited, or k times?
5. Does the order of items matter? (If not, you choose the processing order. If the
   constraint depends on order, you must first sort by an exchange argument, then
   knapsack.)
6. **Which quantity is small?** n, W, the values, or the sum of weights? The answer
   decides which dimension becomes the DP index.
7. Are there extra constraints? (groups, dependencies, a second resource, a count limit)

Step 6 is where most people get stuck, and it's what separates deep understanding
from memorized templates.

### 4. The variations

- **A. Subset sum / feasibility.** dp[c] = true/false. Same loop with |=. Speedup:
  bitset, bs |= bs << w, giving O(nW/64).
- **B. Exact capacity vs. at most capacity.** "Exactly c": dp[0] = 0, all others
  -INF. "At most c": dp[all] = 0 (or take the max over all c at the end). Mixing these
  up is a classic bug.
- **C. Unbounded knapsack.** Forward loop.
- **D. Counting ways (coin change).** dp[c] += dp[c - w]. Loop order changes the
  meaning: items outer, capacity inner counts combinations; capacity outer, items
  inner counts permutations. With items outer, you fix a canonical order in which
  items are "introduced", so each multiset is counted once.
- **E. Bounded knapsack (item i available k_i times).** Binary splitting into
  1, 2, 4, ..., remainder (O(nW log k)); monotone deque per residue class (O(nW));
  feasibility version with a used[c] counter (O(nW)).
- **F. Swap the dimension.** If W <= 10^9 but the sum of values is small:
  dp[val] = minimum weight to achieve value val; the answer is the largest val with
  dp[val] <= W. The DP index should be whichever quantity is small.
- **G. Meet in the middle.** n <= 40 and both W and values huge: split, enumerate
  2^20 subsets per half, sort, combine with two pointers.
- **H. Group / multiple-choice knapsack.** At most one item per group: groups, then
  capacity (descending), then items in the group. The capacity loop must sit outside
  the item loop, or you could take two items from one group.
- **I. Two or more resources.** dp[c1][c2] ("at most m ones and n zeros").
- **J. Count-limited.** "Pick exactly k items": add a dimension, dp[j][c].
- **K. Tree knapsack / dependencies.** dp[v][c] over a subtree, merging children
  like knapsack convolutions; bounding by subtree sizes gives O(nW).
- **L. Sort first, then knapsack.** When order matters (deadlines), find the order by
  an exchange argument, then knapsack in that order.
- **M. Disguised knapsack.** Partition with minimal difference (subset sum up to S/2);
  +/- signs to reach T (subset sum with target (S+T)/2, where the algebra is the
  insight); maximize something under a budget; "can you form exactly X?";
  probability knapsack.
- **N. Advanced tools.** O(sqrt S) distinct weights; offline add/remove with
  divide and conquer; max-plus convolution; removing an item from a counting
  knapsack by polynomial division.

### 5. Common bugs and traps

- Wrong loop direction in 1D (0/1 vs. unbounded).
- -INF plus a value overflowing or being "revived": guard with `if dp[c-w] != -INF`.
- "Exactly" vs. "at most" changes the init.
- Reconstructing the answer from a 1D array (you can't): keep the 2D table.
- Modular counting: don't subtract without adding the mod back.
- Mixing up combinations and permutations.

### 6. How to practice so the thinking sticks

For each problem, before coding, write down: the state in words; the transition and
why it is exhaustive and non-overlapping; which dimension is small and why; the init
and the answer cell. If you can't state those four, you don't have the idea yet.

---

[The learner tried and wrote: "solving limit x = answer of x-1 + some number"; asked
whether two recursive calls are needed or "just take if allowed"; and thought dp
stores the cost and the best value.]

## Part 0: Three corrections to your thinking

**1. "Solving limit x = answer of x-1 + some number."** The best value for limit 5 is
usually not the answer for limit 4 plus something. If the state is only the limit,
you forget which items you already used, and then you can use the same item again and
again. That is a different problem (unbounded knapsack). So the state needs two
things: which items I am allowed to use, and how much room I have.

**2. "Do I need two recursive calls, or just take if allowed?"** Yes, two calls: take
and skip. Taking whenever it fits fails. Example: limit 10, items (w=6, v=13),
(w=5, v=10), (w=5, v=10). "Take if it fits" takes the first item (13) and then nothing
else fits. The best answer is the other two items (20). Sometimes you must skip an
item that fits.

**3. "dp stores the cost and the best value."** It stores only the best value. The
weight is not stored. It is the column number c, which is the limit (the size of the
bag).

## Part 1: The state in plain words

> dp[i][c] = the most value I can carry if I may only use the first i items and my
> bag holds at most c.

Row i is "which items am I allowed to look at": items 1..i. Column c is "how big is my
bag". The cell is the best value for that situation. Row 0 means "I may use zero
items," so the value is 0 for every c. That is the base case. Final answer: dp[n][W].

## Part 2: Building the recursion (take/skip)

Either the best solution for (i, c) uses item i, or it doesn't.

- Skip item i: the best with only the first i-1 items and the same bag, f(i-1, c).
- Take item i (only if w[i] <= c): v[i], and the bag has c - w[i] left. The rest must
  come from the first i-1 items, because item i is used up: v[i] + f(i-1, c - w[i]).

Why is it OK to trust the best of the sub-problem? Suppose the best solution for
(i, c) takes item i. The other items in it must be the best possible for
(i-1, c-w[i]). If a better set existed, I could swap it in and get a better total for
(i, c), which contradicts "best."

## Part 3: The recursion tree (where the speed comes from)

Items X(w=1, v=2), Y(w=2, v=3), Z(w=2, v=4), W = 4. f(1,2) appears twice: "skip Z,
take Y" and "take Z, skip Y" are different choices that land in the same situation,
"items {X} left, 2 space left". The future only cares about those two numbers, so I
compute f(1,2) once. Distinct situations = (n+1) x (W+1), not 2^n.

## Part 4: Filling the table by hand

Items (w, v): A(1,1), B(3,4), C(4,5), D(5,7). W = 7.

    cap c ->      0  1  2  3  4  5  6  7
    row 0 (none)  0  0  0  0  0  0  0  0
    row 1 (+A)    0  1  1  1  1  1  1  1
    row 2 (+B)    0  1  1  4  5  5  5  5
    row 3 (+C)    0  1  1  4  5  6  6  9
    row 4 (+D)    0  1  1  4  5  7  8  9   <- answer 9

Row 2 (item B: w=3, v=4) from row 1: c = 0,1,2 B does not fit, copy from above; c = 3:
skip = row1[3] = 1, take = row1[0] + 4 = 4, max 4; c = 4: skip 1, take row1[1] + 4 = 5 ...
Each cell looks at exactly two places in the row above: straight up (skip), and up
and to the left by w (take).

Getting the items: walk backward from the corner. (4,7) equals (3,7), so D was not
taken; (3,7) differs from (2,7), so C was taken, c = 3; (2,3) differs from (1,3), so B
was taken, c = 0. Items B and C, value 9. This needs the full table.

## Part 5: The code, line by line

    for (int i = 1; i <= n; i++)            // allow one more item each round
      for (int c = 0; c <= W; c++) {        // every bag size
        dp[i][c] = dp[i-1][c];              // assume I skip item i (always legal)
        if (c >= w[i])                      // can item i fit in this bag?
          dp[i][c] = max(dp[i][c], dp[i-1][c - w[i]] + v[i]);  // compare with take
      }

| Recursion | Table code |
|---|---|
| f(i-1, c) | dp[i-1][c] |
| f(i-1, c-w[i]) | dp[i-1][c - w[i]] |
| if (i == 0) return 0 | row 0 is all zeros |
| call smaller first | outer loop goes i = 1, 2, 3... |

## Part 6: How the row index stops you using an item twice

The take case jumps to row i-1, which only knows items 1..i-1. Row i-1 cannot see item
i at all. Every step moves one row up, and you can never move back down. A state with
only c (dp[c] = max over j of dp[c - w_j] + v_j) has nothing saying "item j is gone":
that is unbounded knapsack.

## Part 7: From 2D to 1D (why the direction matters)

Row i only needs row i-1, so keep one array and turn it from "row i-1" into "row i" in
place. The take case reads left (c - w < c). Right to left: the cells on the left
have not been touched yet, so they still hold row i-1 (correct). Left to right: the
cells on the left already hold row i and may include item i (wrong for 0/1).

---

[The learner did not understand three things. In the recursion we subtract from the
limit, but the loop doesn't subtract, so how is c - w the same logic? The arrow
diagram was confusing. Must V and W be 1-based? And the 1D direction explanation did
not click. They said one line, "plus the best I can do in the leftover space c - w[i]
using only the earlier items", started to make it click.]

## 1. "The loop doesn't subtract. How is c - w the same logic?"

    recursion:   v[i] + f(i-1, c - w[i])
    table:       v[i] + dp[i-1][c - w[i]]

The subtraction is in both. In the recursion, c is a running value that shrinks as you
go deeper. In the table, c is not running: it is a label for which question this cell
answers. dp[i][5] is "bag of size 5, first i items"; dp[i][3] is a different,
independent question. The table already holds the answers to every bag size for the
previous items, so the call f(i-1, c - w) becomes a lookup in column c - w.

> "I'm answering the question for a bag of size 5, with item B (w=3, v=4) allowed. If
> I put B in, 3 units are used, so 2 units are left. What's the best I can do with 2
> units using only the earlier items? That is already written in the previous row, in
> column 2. I add 4 to it."

## 2. The diagram, redone with real numbers

    column c:     0   1   2   3   4   5   6   7
    row 1:        0   1  [1]  1   1  [1]  1   1
                          ^           ^
                          |           +-- SKIP: don't use B, same bag (5): row1[5] = 1
                          +-------------- TAKE: use B (w 3), bag left 5-3 = 2: row1[2] + 4 = 5
    row 2:        .   .   .   .   .  [5]  .   .      max(skip=1, take=5) = 5

Skip means "look straight above, same column." Take means "look 3 columns to the left,
then add 4." Take goes left by exactly the item's weight, because that is how much
space the item eats.

## 3. "Must V and W be 1-based?"

No. Row i means "the first i items are allowed"; the i-th item sits at index i-1:

    for (int i = 1; i <= n; i++) {
        int weight = w[i-1], value = v[i-1];
        for (int c = 0; c <= W; c++) {
            dp[i][c] = dp[i-1][c];
            if (c >= weight) dp[i][c] = max(dp[i][c], dp[i-1][c - weight] + value);
        }
    }

The extra row is there because you need a row for zero items to build on.

## 4. The 1D version, from scratch

> To compute the new dp[c], I need the OLD value of dp[c - w] (from the previous row),
> not a new one.

Why old? The take case means "best for the bag c - w using only the earlier items."
If dp[c-w] was already updated for this item, it already contains the item, and I'd
be adding the item on top of itself. c - w is always to the left of c. So the question
is: when I reach cell c, has the cell to my left already been overwritten this round?

One item w=2, v=5, W=6, start all zeros (`*` = overwritten this round):

    Right to left (correct)                  Left to right (wrong)
    start:  0 0 0  0  0  0  0                start:  0 0 0  0   0   0   0
    c=6: dp[4] old 0 -> 5                    c=2: dp[0] old 0 -> 5
    c=5: dp[3] old 0 -> 5                    c=3: dp[1] old 0 -> 5
    c=4: dp[2] old 0 -> 5                    c=4: dp[2] NEW 5 -> 10   item used twice
    c=3: dp[1] old 0 -> 5                    c=5: dp[3] NEW 5 -> 10
    c=2: dp[0] old 0 -> 5                    c=6: dp[4] NEW 10 -> 15  three times
    final:  0 0 5* 5* 5* 5* 5*               final:  0 0 5* 5* 10* 10* 15*

The whole difference between the two loops: do I read the cell before or after it has
been updated for this item? Going right to left works because writing at c never
ruins reading at something smaller than c.

## Check yourself (the tutor's exercises)

- Items (w, v): A(2,3), B(3,4), C(4,5). W = 5. Fill the full 2D table by hand and write,
  for each cell, which two cells you compared. Walk backward to find the items. Do the
  1D version downward and upward and find the cell where an item gets used twice.
- Item (w=1, v=1), W=4, array [0,0,0,0,0]: what do the left-to-right and right-to-left
  loops produce? In one sentence, what does the left-to-right result mean in real life?
