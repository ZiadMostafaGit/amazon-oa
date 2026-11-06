# Partition and Interval DP

> When the last operation on a contiguous block splits it into two blocks that never touch each other again, the only thing the future needs to know is where the block starts and where it ends, so every way of building the block collapses into one cell (i, j), and the cell is the best over where that last operation falls.

## The problem it solves

Four piles of stones stand in a row: 3, 2, 4, 1. In one move you pick two piles that are **next to each other** and merge them into one pile. The move costs the number of stones in the new pile. You keep merging until one pile is left. What is the cheapest total?

Try one plan by hand. Merge 3 and 2 (cost 5): the row is 5, 4, 1. Merge 4 and 1 (cost 5): the row is 5, 5. Merge those (cost 10). Total 20. Another plan: merge 2 and 4 first (cost 6): 3, 6, 1. Merge 3 and 6 (cost 9): 9, 1. Merge (cost 10). Total 25. The plans differ, the totals differ, and the question is which plan is cheapest. The answer for this row is 20.

That is [[p:google-merge-stones|Minimum Cost to Merge Stones]] with k = 2, and it is the cleanest member of a family that looks varied on the surface:

- put brackets into "T^F|F" in every way and count how many come out true ([[p:intuit-boolean-parenthesization|Count True Boolean Parenthesizations]]);
- two players take coins from either end of a row, and you want the first player's best margin ([[p:rippling-optimal-endpoint-score-difference|Optimal Score Difference in an Endpoint Game]]);
- remove arithmetic triples from an array, where removals glue far elements together ([[p:medianet-minimum-length-after-arithmetic-triple-removals|Minimum Length After Removing Arithmetic Triples]]);
- cut an array into K contiguous pieces as cheaply as possible ([[p:linkedin-split-array-largest-sum|Split Array Largest Sum]]);
- choose nodes of a tree, no parent together with its child ([[p:zip-tree-independent-set|Maximum Nonadjacent Sum in a General Tree]]).

All of them have the same bones: the input is a **sequence whose order you may not change** (or a tree, which is a sequence in disguise, as we will see), and the decisions are about how to group, bracket, cut or consume **contiguous** stretches of it.

### The naive solutions

The first program anyone writes for the stones is "try every plan". At the start there are n - 1 adjacent pairs you could merge. After that, n - 2. So the number of complete plans is (n - 1)(n - 2)...1 = (n - 1)!. Four piles give 6 plans. The bank's version allows 30 piles, and 29! is about 8.8 x 10^30. No.

The second program is a greedy rule: "always merge the cheapest adjacent pair". It is the rule that is optimal when *any* two piles may be merged (that is Huffman coding, see [[greedy-exchange]]). With the adjacency rule it fails. Row 3, 2, 2, 3: the cheapest pair is the middle 2 + 2 = 4. Then the row is 3, 4, 3, both pairs cost 7, merge one: 7, 3, then 10. Total 4 + 7 + 10 = 21. But merging 3 + 2 = 5 and 2 + 3 = 5 first and then 10 costs 20. The cheap merge in the middle glued the two halves into a pile that both outer piles then had to lift.

What this chapter builds is a method that is exact like trying everything and costs about n^3 / 6 small steps: for 30 piles, under 5,000.

### When it is the wrong tool

- **The items are not in a fixed order.** "Split the numbers into two groups with equal sums" lets any element go to either group. That is a subset, and subsets are [[knapsack]]: [[p:expedia-partition-equal-subset-sum|Partition into Equal-Sum Subsets]] has "partition" in its name and is not interval DP at all.
- **A greedy rule is provably right.** [[p:bloomberg-partition-labels|Partition Labels]] cuts a string into contiguous parts, which smells like this chapter, but the rule "close the part as soon as every letter in it has appeared for the last time" is optimal, and one linear scan is the whole solution.
- **You must list every grouping, not find the best one.** [[p:expedia-palindrome-partitions|All Palindrome Partitions]] wants every way to cut a string into palindromes. Listing is [[backtracking]]. A DP can count them or find the fewest pieces, but it cannot print exponentially many answers faster than printing them.
- **The sequence is long.** The core recurrence is cubic. With n = 10^5 it is hopeless. Then either one end of the interval is pinned (a 1-D partition DP, variation A), or the interval is determined by a small counter (variation G), or the problem has a greedy or a monotone structure.
- **The pieces do not interact and the split is fixed.** Merge sort splits in the middle, solves both halves and combines. No choice of split, no overlap: that is [[divide-and-conquer]], and memoising it buys nothing.

## Build it from the brute force

We start from the slowest correct program and remove one waste at a time. The table will appear at the end, as the obvious thing to do.

### Step 1: try every plan

A plan is a sequence of merges. The brute force makes the first merge in every possible place, and for each, solves the shorter row that results:

```
best(row) = 0                                         if row has one pile
best(row) = min over t of (row[t] + row[t+1]) + best(row with t, t+1 merged)
```

It is correct, because every plan starts with some first merge. It is slow, because the rows it creates are arbitrary: after merging 2 and 4 in 3, 2, 4, 1 you get 3, 6, 1, a row that is not a piece of the input. The state of this recursion is "the whole current row", and there are a great many possible rows.

### Step 2: notice the first waste

Look at two of the six plans for 3, 2, 4, 1:

- merge 3+2 (cost 5), then 4+1 (cost 5), then 5+5 (cost 10);
- merge 4+1 (cost 5), then 3+2 (cost 5), then 5+5 (cost 10).

They are different sequences and the same plan. The two early merges happen in different parts of the row and do not affect each other. Their order is noise. Six sequences, but only five genuinely different ways to bracket four piles:

```
((3 2) 4) 1    (3 (2 4)) 1    (3 2) (4 1)    3 ((2 4) 1)    3 (2 (4 1))
```

A plan is really a **bracketing**: a binary tree whose leaves are the piles in order and whose internal nodes are merges. The cost of a plan is the sum, over internal nodes, of the stones underneath. Order of independent merges does not change the tree, so it does not change the cost.

### The question that unlocks it

Where should we cut the problem? The brute force cuts on the **first** merge, and that leaves an odd row behind. Look instead at the **last** merge.

**What is the last thing that happens to this block?**

The very last merge joins two piles into one. The left pile is made of some piles 0..m, the right one of piles m+1..n-1, for some split m. And here is the whole point: up to that moment, the two sides never touched. Every earlier merge happened entirely on the left of the split or entirely on the right. So the cheapest plan whose last merge is at m costs

```
(cheapest way to make piles 0..m into one pile)
  + (cheapest way to make piles m+1..n-1 into one pile)
  + (all the stones, for the last merge itself)
```

and the two "cheapest ways" are the **same problem on a shorter contiguous block**. Not a strange row, a block of the original input. We do not know m, so we try all of them.

Say it a second way. The last merge is a wall. Whatever happened to the left of the wall stayed on the left; whatever happened on the right stayed on the right. A wall turns one problem into two independent problems of the same shape, and both are described by nothing more than their two ends.

That is the answer to the question every DP asks ([[state-design]]): **what is the least the future needs to know about the past?** For a contiguous block, two numbers: where it starts and where it ends. How the block was built inside does not matter to anyone outside it.

### You might think: "Merge the cheapest pair first."

We saw it fail on 3, 2, 2, 3: greedy pays 21, the best is 20. The reason is worth saying in words. A merge is not only paid once; the stones it creates are lifted again by **every later merge above it in the tree**. Merging the middle 2 + 2 makes a pile of 4 in the middle, where both neighbours must eventually merge with it. The greedy rule sees the price of this merge and not the price it forces on later merges. Nothing local can see that, which is why we need the table.

### You might think: "Go left to right, like a 1-D DP."

The instinct is: let g(j) = cheapest way to merge piles 0..j, and build g(j) from g(j-1) by merging pile j into the pile you already have. That is a prefix state, and it forces every plan to look like (((a b) c) d): pile j always merges into everything before it.

On 1, 1, 1, 1 that costs 2 + 3 + 4 = 9. The plan (1 1)(1 1) costs 2 + 2 + 4 = 8. The prefix state cannot express "merge the right part on its own first, then join", because the right part has no name in it. One end of the block is not enough; the right part is a block with **two** free ends. (When one end really is pinned, a prefix state is exactly right: that is the linear partition DP of variation A. Merging is not such a problem; cutting into pieces is.)

### You might think: "Cut on the first merge, it is the same thing."

It is not. Suppose the first merge joins piles 1 and 2 of 3, 2, 4, 1. What remains is 3, 6, 1, and the 6 is a pile that will later merge with the 3 *or* with the 1. It belongs to neither side. The first merge does not divide the row into independent parts; it creates a new element that sits between them. The last merge is the only one guaranteed to be a clean wall. This "last, not first" choice is the heart of the whole family, and it reappears in a sharper form in Burst Balloons (variation D), where splitting on the first balloon gives a wrong answer outright.

### Step 3: write the recursion on blocks

Number the piles 0..n-1. Let S(i, j) be the number of stones in piles i..j. Define

> f(i, j) = the cheapest cost to merge piles i..j (inclusive) into one pile.

```
f(i, i) = 0                                              one pile: nothing to do
f(i, j) = min over m in i..j-1 of  f(i, m) + f(m+1, j)   the last merge is between m and m+1
          + S(i, j)                                      the last merge lifts every stone
```

The answer is f(0, n-1). The split m runs from i to j-1 so that both sides are non-empty. S(i, j) comes from prefix sums: with P[k] = sum of the first k piles, S(i, j) = P[j+1] - P[i].

Notice what is *not* in the recursion: the merges inside each side, their order, the shape of the tree. All of it is summarised by one number per side.

### Step 4: count it, and see the overlap

The recursion is far better than (n-1)! already, but without memory it is still exponential. On 3, 2, 4, 1 it makes 27 calls, and on n piles 3^(n-1) calls: each call of length L spawns two calls for every split. The waste is visible in the tree.

<svg viewBox="0 0 760 290" role="img" aria-label="the split recursion tree of f(0,3) on four piles: the three splits of f(0,3), then the two splits of f(1,3) and of f(0,2); the blocks f(2,3) and f(1,2) each appear twice and are shaded">
  <g>
    <rect x="348" y="12" width="64" height="28" rx="4"/>
    <text x="380" y="31" text-anchor="middle">f(0,3)</text>
    <rect x="72" y="95" width="56" height="28" rx="4"/>
    <text x="100" y="114" text-anchor="middle">f(0,0)</text>
    <text x="135" y="114" text-anchor="middle">+</text>
    <rect x="142" y="95" width="56" height="28" rx="4"/>
    <text x="170" y="114" text-anchor="middle">f(1,3)</text>
    <rect x="317" y="95" width="56" height="28" rx="4"/>
    <text x="345" y="114" text-anchor="middle">f(0,1)</text>
    <text x="380" y="114" text-anchor="middle">+</text>
    <rect class="fill" x="387" y="95" width="56" height="28" rx="4"/>
    <text x="415" y="114" text-anchor="middle">f(2,3)</text>
    <rect x="562" y="95" width="56" height="28" rx="4"/>
    <text x="590" y="114" text-anchor="middle">f(0,2)</text>
    <text x="625" y="114" text-anchor="middle">+</text>
    <rect x="632" y="95" width="56" height="28" rx="4"/>
    <text x="660" y="114" text-anchor="middle">f(3,3)</text>
    <line x1="365" y1="40" x2="135" y2="95"/>
    <line x1="380" y1="40" x2="380" y2="95"/>
    <line x1="395" y1="40" x2="625" y2="95"/>
    <text x="230" y="62" text-anchor="end">m=0</text>
    <text x="386" y="72">m=1</text>
    <text x="530" y="62">m=2</text>
    <rect x="22" y="185" width="56" height="28" rx="4"/>
    <text x="50" y="204" text-anchor="middle">f(1,1)</text>
    <text x="85" y="204" text-anchor="middle">+</text>
    <rect class="fill" x="92" y="185" width="56" height="28" rx="4"/>
    <text x="120" y="204" text-anchor="middle">f(2,3)</text>
    <rect class="fill" x="172" y="185" width="56" height="28" rx="4"/>
    <text x="200" y="204" text-anchor="middle">f(1,2)</text>
    <text x="235" y="204" text-anchor="middle">+</text>
    <rect x="242" y="185" width="56" height="28" rx="4"/>
    <text x="270" y="204" text-anchor="middle">f(3,3)</text>
    <line x1="160" y1="123" x2="85" y2="185"/>
    <line x1="180" y1="123" x2="235" y2="185"/>
    <rect x="462" y="185" width="56" height="28" rx="4"/>
    <text x="490" y="204" text-anchor="middle">f(0,0)</text>
    <text x="525" y="204" text-anchor="middle">+</text>
    <rect class="fill" x="532" y="185" width="56" height="28" rx="4"/>
    <text x="560" y="204" text-anchor="middle">f(1,2)</text>
    <rect x="612" y="185" width="56" height="28" rx="4"/>
    <text x="640" y="204" text-anchor="middle">f(0,1)</text>
    <text x="675" y="204" text-anchor="middle">+</text>
    <rect x="682" y="185" width="56" height="28" rx="4"/>
    <text x="710" y="204" text-anchor="middle">f(2,2)</text>
    <line x1="580" y1="123" x2="525" y2="185"/>
    <line x1="600" y1="123" x2="675" y2="185"/>
    <text x="380" y="250" text-anchor="middle">Each pair is one split: left block + right block. f(1,3) and f(0,2) split again below.</text>
    <text x="380" y="270" text-anchor="middle">Shaded: f(2,3) and f(1,2) are each reached twice, by different splits of different blocks.</text>
  </g>
</svg>

f(2, 3), "merge 4 and 1", is asked for by the split m = 1 of the whole row, and again by the split m = 1 of the block 2, 4, 1. Those are two different stories ("the last wall is after 2" and "the last wall of the block 2,4,1 is after 2"), and they ask the same question about piles 2..3. The same happens to f(1, 2).

How many different questions are there? A block is a pair i <= j, so n(n+1)/2 of them: 10 for four piles, 465 for thirty. Everything else in the exponential tree is those few questions asked again.

### Step 5: remember the answers

Memoise f on (i, j) and each block is solved once. The following program runs the plan-by-plan brute force, the split recursion without memory and with it, checks that they agree, and also checks the two wrong instincts.

```python run
from functools import lru_cache
import random

def every_order(piles):                 # brute force: try every adjacent merge, in every order
    calls = 0
    def go(row):
        nonlocal calls
        calls += 1
        if len(row) == 1:
            return 0
        best = None
        for t in range(len(row) - 1):   # merge piles t and t+1 next
            s = row[t] + row[t + 1]
            cost = s + go(row[:t] + (s,) + row[t + 2:])
            best = cost if best is None else min(best, cost)
        return best
    return go(tuple(piles)), calls

def by_last_merge(piles, remember):     # f(i, j): cheapest way to make piles i..j one pile
    P = [0]
    for x in piles:
        P.append(P[-1] + x)
    calls, seen = 0, {}
    def f(i, j):
        nonlocal calls
        calls += 1
        if remember and (i, j) in seen:
            return seen[(i, j)]
        if i == j:
            ans = 0                     # one pile: nothing to merge
        else:                           # last merge joins [i..m] and [m+1..j]
            ans = min(f(i, m) + f(m + 1, j) for m in range(i, j)) + P[j + 1] - P[i]
        seen[(i, j)] = ans
        return ans
    return f(0, len(piles) - 1), calls, len(seen)

def cheapest_pair_first(piles):         # the greedy instinct
    row, cost = list(piles), 0
    while len(row) > 1:
        t = min(range(len(row) - 1), key=lambda t: row[t] + row[t + 1])
        s = row[t] + row[t + 1]
        cost += s
        row[t:t + 2] = [s]
    return cost

def left_to_right(piles):               # the prefix instinct: always merge into the left pile
    cost, acc = 0, piles[0]
    for x in piles[1:]:
        acc += x
        cost += acc
    return cost

a = [3, 2, 4, 1]
print("every order:", every_order(a))
print("split, no memo:", by_last_merge(a, False))
print("split, memo   :", by_last_merge(a, True))
assert every_order(a)[0] == by_last_merge(a, True)[0] == 20

print("greedy on [3,2,2,3]:", cheapest_pair_first([3, 2, 2, 3]), "best:", every_order([3, 2, 2, 3])[0])
assert cheapest_pair_first([3, 2, 2, 3]) == 21 and every_order([3, 2, 2, 3])[0] == 20
print("left-to-right on [1,1,1,1]:", left_to_right([1, 1, 1, 1]), "best:", every_order([1, 1, 1, 1])[0])
assert left_to_right([1, 1, 1, 1]) == 9 and every_order([1, 1, 1, 1])[0] == 8

random.seed(7)
b = [random.randint(1, 9) for _ in range(8)]
(x, c1), (y, c2, _), (z, c3, states) = every_order(b), by_last_merge(b, False), by_last_merge(b, True)
print("8 piles: orders", c1, "calls | split", c2, "calls | memo", c3, "calls,", states, "states")
assert x == y == z and states == 8 * 9 // 2
for _ in range(100):
    r = [random.randint(1, 9) for _ in range(random.randint(1, 6))]
    assert every_order(r)[0] == by_last_merge(r, True)[0]
print("split recursion == every order on 100 random rows")
```

On the four piles, the plan brute force makes 16 calls, the split recursion 27, the memo 21 calls over only 10 distinct blocks. On eight random piles the gap opens: 13,700 calls for the plans, 2,187 for the split recursion without memory, 169 with it, over 36 blocks. The plans grow like a factorial, the bare split recursion like 3^n, and the memo like n^2 blocks.

### Step 6: fill the answers in order

What does f(i, j) need? Blocks f(i, m) and f(m+1, j) for every split. Every one of them is **strictly shorter** than (i, j). So if we solve all blocks of length 1, then all of length 2, then length 3, every lookup finds its answer ready. Store f(i, j) in dp[i][j], an n x n table of which only the upper triangle (i <= j) is used. That is the table version, and the order of filling turns out to be its one subtle line.

### The technique in one sentence

**Interval DP: the state is a contiguous block (i, j); the value of a block is the best, over where the last operation splits it, of the two smaller blocks plus the cost of that last operation; blocks are solved shortest first.**

And the question that produced it, worth asking on every new problem in this family: **what is the last thing that happens to this block, and does it split the block into parts that never touch again?**


## Worked by hand

Get a pen. Piles 3, 2, 4, 1, indexed 0..3. Prefix sums P = [0, 3, 5, 9, 10], so S(i, j) = P[j+1] - P[i]. The table has a row for each start i and a column for each end j. Cells with j < i are not blocks and stay empty.

Before the numbers, the shape of a single cell. A block i..j and a wall after position m:

<svg viewBox="0 0 640 170" role="img" aria-label="a block of piles from i to j with a wall after position m; the left block i..m costs dp[i][m], the right block m+1..j costs dp[m+1][j], and the last merge costs the sum of the whole block">
  <g>
    <rect x="60" y="40" width="70" height="40"/>
    <rect x="130" y="40" width="70" height="40"/>
    <rect x="200" y="40" width="70" height="40"/>
    <rect class="fill" x="270" y="40" width="10" height="40"/>
    <rect x="280" y="40" width="70" height="40"/>
    <rect x="350" y="40" width="70" height="40"/>
    <rect x="420" y="40" width="70" height="40"/>
    <rect x="490" y="40" width="70" height="40"/>
    <text x="95" y="65" text-anchor="middle">i</text>
    <text x="235" y="65" text-anchor="middle">m</text>
    <text x="315" y="65" text-anchor="middle">m+1</text>
    <text x="525" y="65" text-anchor="middle">j</text>
    <line x1="60" y1="95" x2="270" y2="95"/>
    <line x1="280" y1="95" x2="560" y2="95"/>
    <text x="165" y="115" text-anchor="middle">left block: dp[i][m]</text>
    <text x="420" y="115" text-anchor="middle">right block: dp[m+1][j]</text>
    <line x1="60" y1="135" x2="560" y2="135"/>
    <text x="310" y="157" text-anchor="middle">last merge: S(i, j), the same for every m</text>
    <text x="275" y="28" text-anchor="middle">wall</text>
  </g>
</svg>

The left block and the right block are solved separately, and the wall moves through every position from i to j-1. Now the same thing on real numbers.

**Length 1.** dp[0][0] = dp[1][1] = dp[2][2] = dp[3][3] = 0. A single pile is already one pile.

**Length 2.** A block of two piles has only one split, so its cost is just their sum.

- dp[0][1] = 0 + 0 + (3 + 2) = 5.
- dp[1][2] = 0 + 0 + (2 + 4) = 6.
- dp[2][3] = 0 + 0 + (4 + 1) = 5.

**Length 3.** Two splits each.

- dp[0][2], piles 3, 2, 4, S = 9. Wall after 0: [3] | [2 4] costs dp[0][0] + dp[1][2] = 0 + 6 = 6. Wall after 1: [3 2] | [4] costs dp[0][1] + dp[2][2] = 5 + 0 = 5. Minimum 5, plus 9: **14**.
- dp[1][3], piles 2, 4, 1, S = 7. Wall after 1: [2] | [4 1] = 0 + 5 = 5. Wall after 2: [2 4] | [1] = 6 + 0 = 6. Minimum 5, plus 7: **12**.

**Length 4.** dp[0][3], all four piles, S = 10. Three walls:

| wall after | left block | right block | left + right |
|---|---|---|---|
| m = 0 | [3]: dp[0][0] = 0 | [2 4 1]: dp[1][3] = 12 | 12 |
| m = 1 | [3 2]: dp[0][1] = 5 | [4 1]: dp[2][3] = 5 | **10** |
| m = 2 | [3 2 4]: dp[0][2] = 14 | [1]: dp[3][3] = 0 | 14 |

Minimum 10, plus 10: **20**.

The finished table:

| | j=0 | j=1 | j=2 | j=3 |
|---|---|---|---|---|
| i=0 | 0 | 5 | 14 | **20** |
| i=1 | | 0 | 6 | 12 |
| i=2 | | | 0 | 5 |
| i=3 | | | | 0 |

Here is the story of the winning split in words:

> "I am answering the question for the whole row 3, 2, 4, 1. Suppose the very last merge has the wall after the 2: on its left is a pile made from 3 and 2, on its right a pile made from 4 and 1. Before that moment, the left pile had to be built, and the cheapest way to build it is already written in row 0, column 1: 5. The right pile had to be built too, cheapest in row 2, column 3: 5. Those two jobs never touched each other, so their costs simply add. Then the last merge lifts all 10 stones. 5 + 5 + 10 = 20. The other two walls give 22 and 24, so 20 it is."

And the same cell as a picture of the table. The cell (0, 3) reads along its own row to the left (blocks that start at 0) and down its own column (blocks that end at 3), and pairs them up:

<svg viewBox="0 0 680 330" role="img" aria-label="the upper-triangular table for piles 3 2 4 1; the corner cell dp[0][3] equals 20 and pairs dp[0][0] with dp[1][3], dp[0][1] with dp[2][3], and dp[0][2] with dp[3][3]; the winning pair dp[0][1] equals 5 and dp[2][3] equals 5 is shaded">
  <g>
    <text x="145" y="40" text-anchor="middle">j=0</text>
    <text x="215" y="40" text-anchor="middle">j=1</text>
    <text x="285" y="40" text-anchor="middle">j=2</text>
    <text x="355" y="40" text-anchor="middle">j=3</text>
    <text x="80" y="80" text-anchor="middle">i=0</text>
    <text x="80" y="150" text-anchor="middle">i=1</text>
    <text x="80" y="220" text-anchor="middle">i=2</text>
    <text x="80" y="290" text-anchor="middle">i=3</text>
    <rect x="110" y="50" width="70" height="50"/>
    <text x="145" y="80" text-anchor="middle">0</text>
    <rect class="fill" x="180" y="50" width="70" height="50"/>
    <text x="215" y="80" text-anchor="middle">5</text>
    <rect x="250" y="50" width="70" height="50"/>
    <text x="285" y="80" text-anchor="middle">14</text>
    <rect class="fill" x="320" y="50" width="70" height="50" stroke-width="3"/>
    <text x="355" y="80" text-anchor="middle">20</text>
    <rect x="180" y="120" width="70" height="50"/>
    <text x="215" y="150" text-anchor="middle">0</text>
    <rect x="250" y="120" width="70" height="50"/>
    <text x="285" y="150" text-anchor="middle">6</text>
    <rect x="320" y="120" width="70" height="50"/>
    <text x="355" y="150" text-anchor="middle">12</text>
    <rect x="250" y="190" width="70" height="50"/>
    <text x="285" y="220" text-anchor="middle">0</text>
    <rect class="fill" x="320" y="190" width="70" height="50"/>
    <text x="355" y="220" text-anchor="middle">5</text>
    <rect x="320" y="260" width="70" height="50"/>
    <text x="355" y="290" text-anchor="middle">0</text>
    <text x="420" y="70">m=0: dp[0][0] + dp[1][3] = 0 + 12</text>
    <text x="420" y="95">m=1: dp[0][1] + dp[2][3] = 5 + 5</text>
    <text x="420" y="120">m=2: dp[0][2] + dp[3][3] = 14 + 0</text>
    <text x="420" y="155">best 10, plus S(0,3) = 10</text>
    <text x="420" y="180">dp[0][3] = 20</text>
    <text x="420" y="230">row 0, left of the corner:</text>
    <text x="420" y="250">blocks that start at 0</text>
    <text x="420" y="280">column 3, below the corner:</text>
    <text x="420" y="300">blocks that end at 3</text>
  </g>
</svg>

The pairing is always "the k-th cell from the left of the row with the k-th cell from the top of the column below". Read the row left to right and the column top to bottom at the same time: (0,0) with (1,3), (0,1) with (2,3), (0,2) with (3,3). That is the wall moving right.

### Getting the plan back

The table holds costs, not plans. To recover the plan, remember which wall won in every cell (a second table, `cut`), then unfold from the corner. cut[0][3] = 1: the last merge joins [3 2] and [4 1]. cut[0][1] = 0 and cut[2][3] = 2: each of those is a single merge. The plan is (3 2)(4 1): merge 3+2, merge 4+1 (in either order), then the two halves.

Ties, as in knapsack, mean several plans share the optimal cost. Any tie rule gives a valid optimal plan.

### A second trace: the cheap merge that the corner does not use

Now the greedy counterexample, 3, 2, 2, 3. P = [0, 3, 5, 7, 10].

| | j=0 | j=1 | j=2 | j=3 |
|---|---|---|---|---|
| i=0 | 0 | 5 | 11 | **20** |
| i=1 | | 0 | 4 | 11 |
| i=2 | | | 0 | 5 |
| i=3 | | | | 0 |

- dp[1][2] = 4: the middle pair, the merge greedy loves.
- dp[0][2] (3, 2, 2; S = 7): walls give 0 + 4 = 4 and 5 + 0 = 5, so 4 + 7 = 11. This block *does* use the cheap middle merge.
- dp[1][3] (2, 2, 3; S = 7): walls give 0 + 5 = 5 and 4 + 0 = 4, so 11. Uses it too.
- dp[0][3] (S = 10): walls give 0 + 11 = 11, 5 + 5 = 10, 11 + 0 = 11. Best 10, total **20**, with the wall in the middle.

Look at the walls m = 0 and m = 2 of the corner. Both total 11 + 10 = 21, and both are worlds in which the middle pair was merged early. 21 is exactly what greedy paid. The table did not have to "decide against" greedy; it kept, side by side, the best plan for every block, including the plans that merge the middle pair and the plan that does not. The corner compares them as three numbers and picks the smallest.

That is what this trace shows and the code alone hides: **a block's cell knows nothing about the world outside the block.** dp[1][2] = 4 is the best way to merge the middle pair *if you ever want it merged on its own*. Whether you want that is decided higher up, by a cell that sees what it costs the neighbours.

## From the idea to the code

### The direct version: the table, shortest blocks first

```python run
def merge_cost(piles):
    n = len(piles)
    P = [0] * (n + 1)                         # P[k] = sum of the first k piles
    for k, x in enumerate(piles):
        P[k + 1] = P[k] + x
    dp = [[0] * n for _ in range(n)]          # dp[i][i] = 0: a single pile costs nothing
    cut = [[None] * n for _ in range(n)]      # the best last split, for reconstruction
    for length in range(2, n + 1):            # short blocks before long ones
        for i in range(0, n - length + 1):
            j = i + length - 1
            best = None
            for m in range(i, j):             # last merge: [i..m] + [m+1..j]
                c = dp[i][m] + dp[m + 1][j]
                if best is None or c < best:
                    best, cut[i][j] = c, m
            dp[i][j] = best + P[j + 1] - P[i]  # the last merge costs the whole block
    return dp, cut

def shape(piles, cut, i, j):                  # rebuild the merge tree from the cuts
    if i == j:
        return str(piles[i])
    m = cut[i][j]
    return "(" + shape(piles, cut, i, m) + " " + shape(piles, cut, m + 1, j) + ")"

def show(piles):
    dp, cut = merge_cost(piles)
    n = len(piles)
    print("piles", piles)
    for i in range(n):
        print("  i=%d " % i + " ".join("  ." if j < i else "%3d" % dp[i][j] for j in range(n)))
    print("  cost", dp[0][n - 1], "shape", shape(piles, cut, 0, n - 1))
    return dp, cut

dp, cut = show([3, 2, 4, 1])
assert dp[0][1] == 5 and dp[1][2] == 6 and dp[2][3] == 5
assert dp[0][2] == 14 and dp[1][3] == 12 and dp[0][3] == 20
assert cut[0][3] == 1 and shape([3, 2, 4, 1], cut, 0, 3) == "((3 2) (4 1))"

dp2, cut2 = show([3, 2, 2, 3])                # the greedy counterexample
assert dp2[1][2] == 4                         # the cheap middle pair is in the table...
assert dp2[0][3] == 20 and cut2[0][3] == 1    # ...and the corner does not use it
```

### Each line, and which part of the recursion it is

| line | in plain words | in the recursion |
|---|---|---|
| `P[k + 1] = P[k] + x` | prefix sums, so any block's total is one subtraction | S(i, j) = P[j+1] - P[i] |
| `dp = [[0] * n ...]` | n x n, all zero; the diagonal stays 0 | the base case f(i, i) = 0 |
| `for length in range(2, n + 1)` | blocks of length 2, then 3, ... | "solve smaller blocks first" |
| `for i in range(0, n - length + 1)` with `j = i + length - 1` | every block of this length | every (i, j) with j - i + 1 = length |
| `for m in range(i, j)` | every position of the last wall | the min over m in i..j-1 |
| `dp[i][m] + dp[m + 1][j]` | the two sides, already solved | f(i, m) + f(m+1, j) |
| `+ P[j + 1] - P[i]` | the last merge lifts the whole block | + S(i, j) |
| `cut[i][j] = m` | remember the winning wall | not in the recursion; it rebuilds the plan |

Three lines do the real work: the loop over m, the sum of the two sides, and the cost of the last merge. The rest is order and bookkeeping.

Settle the boring confusions now, so they do not cost you an hour later:

- **Inclusive ends.** dp[i][j] covers piles i through j, both included. The block's length is j - i + 1. Mixing inclusive and half-open ends inside one recurrence is the most common off-by-one in this family. Pick one and write it at the top of your solution. (Burst Balloons below uses *open* intervals on purpose, and says so.)
- **The range of m.** m runs from i to j - 1 so that the left block i..m and the right block m+1..j are both non-empty. `range(i, j)` does exactly that. If m reached j, the right block would be m+1..j = j+1..j, empty, and you would be "merging" a pile with nothing at full price.
- **The diagonal.** dp[i][i] = 0 is a real answer (one pile costs nothing), not a placeholder. For other problems the diagonal holds other base values: the coin itself in the game, the truth value of the operand in boolean parenthesisation.
- **The lower triangle.** Cells with j < i are never read. Allocating the full square wastes half the memory, which nobody cares about at n = 500.
- **What a cell stores.** Only the cost. Not the plan, not the shape, not the number of stones (that is S(i, j), recomputed from prefix sums). The plan lives in `cut`.

### The subtle line, both ways: the order you fill the table

In knapsack the subtle line was the direction of a loop. Here it is the same kind of thing: **the order in which cells are filled**. dp[i][j] reads dp[i][m] (same row, to the left) and dp[m+1][j] (same column, below). Every cell it reads must already be final.

The natural-looking double loop, row by row from the top, `for i in range(n): for j in range(i + 1, n)`, breaks that rule. When it computes dp[0][2] it needs dp[1][2], which is in a row it has not reached yet. Python happily reads the 0 that is sitting there. The program below fills the same table in three orders and logs, for each cell, which cells it read before they were filled.

```python run
def fill(piles, order):
    n = len(piles)
    P = [0]
    for x in piles:
        P.append(P[-1] + x)
    dp = [[0] * n for _ in range(n)]
    done = {(i, i) for i in range(n)}          # cells that hold a real answer
    log = []
    for i, j in order(n):
        stale = [(a, b) for m in range(i, j) for a, b in ((i, m), (m + 1, j)) if (a, b) not in done]
        dp[i][j] = min(dp[i][m] + dp[m + 1][j] for m in range(i, j)) + P[j + 1] - P[i]
        done.add((i, j))
        log.append(((i, j), dp[i][j], stale))
    return dp, log

def rows_top_down(n):                          # WRONG: i = 0, 1, 2 ... with j rising
    return [(i, j) for i in range(n) for j in range(i + 1, n)]

def by_length(n):                              # right: every shorter block first
    return [(i, i + L - 1) for L in range(2, n + 1) for i in range(n - L + 1)]

def rows_bottom_up(n):                         # also right: i falling, j rising
    return [(i, j) for i in range(n - 1, -1, -1) for j in range(i + 1, n)]

piles = [3, 2, 4, 1]
for name, order in (("rows top-down", rows_top_down), ("by length", by_length),
                    ("rows bottom-up", rows_bottom_up)):
    dp, log = fill(piles, order)
    print(name)
    for (i, j), v, stale in log:
        print("   dp[%d][%d] = %2d" % (i, j, v), " read unfilled " + str(stale) if stale else "")
    print("   answer", dp[0][3])

wrong, log = fill(piles, rows_top_down)
assert log[1] == ((0, 2), 9, [(1, 2)])         # the first bad cell: read dp[1][2] before it existed
assert wrong[0][3] == 10                       # and the answer is too cheap
assert fill(piles, by_length)[0][0][3] == fill(piles, rows_bottom_up)[0][0][3] == 20
assert all(not stale for _, _, stale in fill(piles, by_length)[1])
assert all(not stale for _, _, stale in fill(piles, rows_bottom_up)[1])
```

Read the top-down log as a table. A `*` marks a value read before its cell was computed (still the initial 0):

| step | cell | walls tried | value | true value |
|---|---|---|---|---|
| 1 | dp[0][1] | 0 + 0, plus 5 | 5 | 5 |
| 2 | dp[0][2] | **0 + 0\***, 5 + 0, plus 9 | **9** | 14 |
| 3 | dp[0][3] | 0 + 0\*, 5 + 0\*, 9 + 0, plus 10 | 10 | 20 |
| 4 | dp[1][2] | 0 + 0, plus 6 | 6 | 6 |
| 5 | dp[1][3] | 0 + 0\*, 6 + 0, plus 7 | 7 | 12 |
| 6 | dp[2][3] | 0 + 0, plus 5 | 5 | 5 |

Point at step 2. The wall after pile 0 should cost dp[0][0] + dp[1][2] = 0 + 6, but dp[1][2] is computed at step 4. At step 2 it is still 0, so the program believes "merge 2 and 4" is free, and dp[0][2] comes out 9 instead of 14. The error then spreads: step 3 reads three stale or wrong cells and gets 10, which is just the cost of the final merge, as if everything before it were free.

So the wrong order does not compute garbage at random. It computes "the cost of the plan where every block that has not been reached yet is free". Here, with non-negative costs, its answers are always too cheap. In general a stale cell contributes whatever the table was initialised with, so the error has no fixed direction. On tiny inputs (two piles) the answers are right, which is why this bug survives the first sample test.

Two orders are correct, and both appear in real solutions:

- **by length**: all blocks of length 2, then 3, and so on. Every cell reads only shorter blocks. This is the safest to reason about.
- **rows from the bottom, columns left to right**: `for i in range(n - 1, -1, -1): for j in range(i + 1, n)`. dp[i][m] (same row, to the left) is done because j rises; dp[m+1][j] (a lower row) is done because i falls.

The rule behind both: **a cell reads to its left and below, so finish the left and the bottom first.** Draw the arrows for one cell before writing loops, every time. The equivalent statement for the memo version is "nothing to get wrong": recursion computes what it needs when it needs it, which is a fair reason to start with the memo in an interview and switch to the table only if asked.

### Memo or table?

The memo with `lru_cache` is the recursion from Step 3, verbatim. It is the quickest to write and impossible to get the order wrong. Its costs are Python's: a function call per lookup, and a recursion depth equal to the block length, fine for n = 500, a problem near n = 2,000 (raise the recursion limit, or use the table). The table is faster by a constant factor and lets you keep the `cut` table for free. For the game variants, where each cell has two choices, the table can also be shrunk to one row (variation E).

## Why it is correct

:::proof The table holds the true minimum for every block
**What we claim.** For every block 0 <= i <= j <= n-1, dp[i][j] equals OPT(i, j), the smallest total cost of any sequence of adjacent merges that turns piles i..j into one pile.

**A fact about plans first.** Take any complete plan for the block i..j with j > i. Its final merge joins two piles, a left one L and a right one R, and since merges only ever join neighbours, L is the result of merging some contiguous run i..m and R of the run m+1..j, for some m with i <= m < j. Every earlier merge combined two piles that were both inside L or both inside R (a merge across the wall would have produced a pile containing pile m and pile m+1, and then the final merge could not be between them). So the plan's earlier merges split into two lists: the merges inside i..m, which on their own form a complete plan for that block, and the merges inside m+1..j, which form a complete plan for that one. The cost of the whole plan is (cost of the left list) + (cost of the right list) + S(i, j), because the final merge lifts all stones of the block. Conversely, any plan for i..m, followed by any plan for m+1..j, followed by one merge, is a valid plan for i..j with exactly that cost.

**Base case, length 1.** A single pile needs no merges, so OPT(i, i) = 0. The code leaves dp[i][i] = 0.

**Inductive step.** Assume dp is correct for every block shorter than L, and take a block (i, j) of length L >= 2. Sort all plans for (i, j) into groups by the position m of their final wall. The groups do not overlap (a plan has one final merge) and together cover every plan (every plan has one). By the fact above, the cheapest plan in group m costs OPT(i, m) + OPT(m+1, j) + S(i, j): the left and right lists can be chosen independently, and choosing each as cheap as possible is best, because the costs add. Both blocks are shorter than L, so by the assumption these are dp[i][m] and dp[m+1][j], and both are already filled when (i, j) is computed (all shorter blocks are filled first). The cheapest plan overall is the cheapest of the group minima, and that is exactly the min over m that the code writes into dp[i][j].

**Never too low, never too high.** Every value the code produces is the cost of a real plan (follow the `cut` table down). And the optimal plan belongs to some group m, whose value is one of the numbers the code compares. So dp[i][j] is at most OPT and at least OPT.

**Termination.** n(n+1)/2 cells, each computed once with a finite loop. ∎
:::

The proof used these assumptions, and each one is a place a variant can break the method:

- **Only neighbours interact.** The wall argument needs "a merge across the wall cannot happen before the last merge". If any two piles could merge, the left pile would not be a contiguous run, and the state (i, j) would mean nothing. That problem is Huffman, solved by a greedy.
- **The two sides are independent.** The cost of the left list does not depend on what the right list does. That is what lets "best left plus best right" be the best of the group. In Burst Balloons, if you split on the *first* balloon, this fails: the two sides become neighbours of each other afterwards. Splitting on the last balloon restores it. Whenever a split leaves something that both sides still touch, the state must grow until it doesn't.
- **The cost of the last step depends only on the block, not on how the sides were built.** Here it is S(i, j). In matrix chain multiplication it is rows(i) x cols(m) x cols(j), which depends on m but still not on the inside of the sides: fine. If the last step's cost depended on, say, how many merges the left side used, you would have to put that number in the state.
- **The objective adds up, and we take a min (or a max).** For counting, min becomes a sum over groups and the two sides multiply (variation C). The "groups do not overlap" line then matters even more: if a plan could be counted in two groups, the count would be wrong. Bracketings have exactly one outermost split, which is why counting them by the last operator is exact.
- **Shorter first.** The induction is on length. Any fill order that respects "a block is computed after all its sub-blocks" is the same proof. The top-down row order is not such an order, which is the bug of the previous section in the language of the proof.

For the game variant the same skeleton proves the difference recurrence; it is spelled out in variation E.

## What it costs

**States.** One per block with i <= j: n(n+1)/2.

**Work per state.** A block of length L has L - 1 walls, each O(1) with prefix sums. So the total is the sum over L of (number of blocks of length L) x (L - 1) = sum over L from 2 to n of (n - L + 1)(L - 1). That sum is (n^3 - n) / 6. Check it on four piles: walls tried = 3 (length 2) + 4 (two blocks of length 3, two walls each) + 3 (length 4) = 10, and (64 - 4) / 6 = 10.

| n | blocks | walls tried, (n^3 - n)/6 | in Python |
|---|---|---|---|
| 30 | 465 | 4,495 | instant |
| 200 | 20,100 | 1.3 million | well under a second |
| 500 | 125,250 | 21 million | several seconds; tighten the inner loop |
| 2,000 | 2 million | 1.3 billion | no |

So O(n^3) time and O(n^2) space. The constraint that signals it: **n up to a few hundred**. The bank's merge stones has n <= 30, boolean parenthesisation 19 operands, triple removals 200, and that is the reason those numbers are so small.

**The hidden costs.**

- **The block sum.** Without prefix sums, S(i, j) is a loop of length L inside the loop over walls, and the whole thing becomes O(n^4) for no reason. Compute it once per cell, outside the wall loop, or from prefix sums.
- **Recursion.** The memo version recurses as deep as the longest block. Python's default limit is 1,000 frames.
- **Problems with only two choices per cell** (take the left end or the right end, as in every game here) do not loop over walls at all. They are O(n^2): 10^6 cells for n = 1,000, fine; [[p:openai-optimal-first-player-card-score|Optimal First-Player Card Score]] with n = 2,000 is 4 million cells, still fine as a list of lists or a rolling row.
- **Tree DP** is O(n) in total: each node combines its children once, and each node is a child once. Tree knapsack is O(n x capacity) with the right bookkeeping.

**Faster, and rare.** Some interval DPs satisfy a monotonicity of the best wall (the optimal m for (i, j) lies between the optimal m for (i, j-1) and for (i+1, j)); Knuth's optimisation then brings O(n^3) down to O(n^2). Merging adjacent piles with k = 2 even has an O(n log n) algorithm (Garsia-Wachs). Neither is expected in an interview; knowing they exist tells you that n = 5,000 on a merge problem is not a typo. See [[dynamic-programming]] on DP optimisations.

## How to think about it

The recurrence is short. The hard part is choosing **which operation is "last"**, and checking that it really cuts the problem into independent parts. Ask these, in order, every time.

1. **Is there a sequence whose order is fixed?** Piles in a row, operands with operators between them, coins in a line, characters of a string, nodes in a tree. If the elements may be rearranged or chosen freely, think [[knapsack]] or [[greedy]] instead.
2. **Do the decisions concern contiguous stretches?** Merging neighbours, bracketing, cutting into pieces, taking from the ends. If yes, a block (i, j) is a candidate state.
3. **Is one end pinned?** If every piece starts where the previous one ended, and you always work from the left, the state is just a prefix length: dp[i] over prefixes, choosing the last piece. That is O(n^2), or O(n) with a trick. Do not reach for (i, j) when (i) suffices.
4. **What is the last operation on a block, and where does it fall?** The last merge, the operator applied last, the balloon burst last, the last piece. Its position is the split m.
5. **Does the split leave two parts that never touch again?** If yes, the recurrence is "best over m of left + right + cost". If no, find what they still share (a neighbour, a count, a boundary element) and add it to the state, or choose a different "last" operation.
6. **What does the cost of the last operation depend on?** Only (i, j)? On m? On the elements just outside the block (Burst Balloons)? It must not depend on the inside of the parts.
7. **Optimise, count, or decide?** Min/max over m, a sum of products over m, or an or over m.
8. **Two players?** Store the mover's best score **minus** the opponent's. The cell is then the same kind of number at every depth (variation E).
9. **A tree?** A subtree is a block, its children are the parts, and each node usually needs two or three numbers, one per "status" (taken or not, covered or not).
10. **What is n?** A few hundred: O(n^3) is the intended solution. A few thousand: you need O(n^2), so only O(1) choices per cell, or a pinned end. 10^5: no interval table; look for a pinned end, a small counter, or a greedy.

Then, before writing any code, write five lines: **the state in words** ("dp[i][j] = cheapest cost to merge piles i..j into one"), **the last operation and its split**, **the cost of that operation**, **the base cells**, and **the fill order** (by length). If you cannot write the fourth and fifth lines, the code will be wrong in exactly the way the top-down demonstration was.

### Telling it from its neighbours

- **Knapsack** ([[knapsack]]). Subsets, any elements, a shared resource. "Partition into two subsets" is knapsack. "Partition into contiguous pieces" is this chapter. The word "partition" is in both; contiguity decides.
- **DP on two strings** ([[dp-strings]]). Edit distance and LCS also have two indices, but they are positions in *two different* strings, and each cell has three neighbours, not a loop over splits. The palindrome table (dp[i][j] for one string, shrinking from both ends) is the bridge between the two families.
- **One-dimensional DP** ([[dp-1d]]). House Robber is a prefix DP; its tree version is tree DP (variation J). Linear partition (variation A) is a prefix DP whose transition loops over the last piece.
- **Game DP** ([[game-dp]]). Games whose states are "what is left" in a row are interval DPs; games on graphs, Nim and Sprague-Grundy are their own world.
- **Tree DP** ([[tree-dp]]). Its own chapter goes further: rerooting, diameters, all-roots answers. Here it appears because a subtree is a block.
- **Divide and conquer** ([[divide-and-conquer]]). A fixed split and no overlapping subproblems. Interval DP is what divide and conquer becomes when the split must be *chosen* and the same sub-blocks recur.
- **Backtracking** ([[backtracking]]). When the answer is the list of all groupings.

## Variations

The family, from the everyday to the rare. Each says what changes in the state or the loop, why, a small example you can check, and a problem from this bank that teaches it. A, B, C, E and J are the common ones in assessments and interviews. D, F, G, K and L are regular. H, I and M are less common. N is rare.

### A. Linear partition: cut a sequence into contiguous pieces

**What changes.** The pieces are consecutive and cover the array from left to right, so one end of every block is pinned to where the previous piece stopped. The state drops from (i, j) to a prefix length: best[i] = the best way to handle the first i elements. The transition loops over **the last piece**, arr[j..i-1]:

```
best[0] = 0
best[i] = min over j < i of  best[j] + cost(piece j..i-1)
```

If the number of pieces is fixed at K, add it to the state: best[k][i], filled one k at a time.

**Why.** It is the same "what happens last" question. In a left-to-right cutting, the last decision is where the last piece starts. Everything before that start is a prefix, and a prefix is a block whose left end is always 0, so it needs one number, not two.

**Example.** [[p:linkedin-split-array-largest-sum|Split Array Largest Sum]] (as stated in this bank: exactly K pieces, minimise the **sum of the pieces' maxima**): [1, 5, 3, 4, 2], K = 2 gives 6, from [1] and [5, 3, 4, 2], 1 + 5. Fewest palindromic pieces: "aab" needs 2 ("aa", "b"); "abacdc" needs 2 ("aba", "cdc"). The palindrome test itself is an interval table, pal[i][j] = s[i] == s[j] and pal[i+1][j-1], filled with i falling: a block that shrinks from both ends.

```python run
from itertools import combinations
import random

def min_sum_of_maxima(arr, K):                 # exactly K contiguous pieces, minimise sum of maxima
    n, INF = len(arr), float("inf")
    best = [0] + [INF] * n                     # best[i]: first i elements in k pieces (k = 0 now)
    for _ in range(K):                         # add one piece per round
        nxt = [INF] * (n + 1)
        for i in range(1, n + 1):
            top = -INF
            for j in range(i - 1, -1, -1):     # the last piece is arr[j..i-1]
                top = max(top, arr[j])
                nxt[i] = min(nxt[i], best[j] + top)
        best = nxt
    return best[n]

def min_palindrome_pieces(s):                  # fewest palindromic pieces (cuts = pieces - 1)
    n = len(s)
    pal = [[False] * n for _ in range(n)]      # an interval table, filled with i falling
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
    best = [0] + [n + 1] * n                   # best[i]: fewest pieces for s[:i]
    for i in range(1, n + 1):
        best[i] = min(best[j] + 1 for j in range(i) if pal[j][i - 1])
    return best[n]

def brute_pieces(arr, K):
    n, out = len(arr), float("inf")
    for cuts in combinations(range(1, n), K - 1):
        c = (0,) + cuts + (n,)
        out = min(out, sum(max(arr[c[t]:c[t + 1]]) for t in range(K)))
    return out

print("[1,5,3,4,2], K=2:", min_sum_of_maxima([1, 5, 3, 4, 2], 2))
assert min_sum_of_maxima([1, 5, 3, 4, 2], 2) == 6
print("aab:", min_palindrome_pieces("aab"), "pieces; abacdc:", min_palindrome_pieces("abacdc"))
assert min_palindrome_pieces("aab") == 2 and min_palindrome_pieces("abacdc") == 2
random.seed(2)
for _ in range(300):
    a = [random.randint(1, 9) for _ in range(random.randint(1, 7))]
    k = random.randint(1, len(a))
    assert min_sum_of_maxima(a, k) == brute_pieces(a, k)
print("prefix-and-last-piece DP == every set of cuts on 300 random arrays")
```

**A twist worth knowing.** [[p:google-partition-into-k-subarrays-minimum-sum|Partition Into K Subarrays With Sum at Least X]] asks whether n <= 2,000 elements, possibly negative, can be cut into **exactly** k pieces, each with sum at least x >= 1. A best[k][i] table with a loop over j is k x n^2, up to 8 x 10^9. The way out is to ask what is small about the answer: if a valid cut into p pieces exists, merging two neighbouring pieces keeps every sum at least x (two sums of at least x add to at least 2x >= x), so a cut into p - 1 pieces exists too. The achievable counts are everything from 1 up to some maximum. So store only the **maximum** number of valid pieces for each prefix, best[i] = max over j of best[j] + 1 where P[i] - P[j] >= x, and answer best[n] >= k. One dimension gone by one line of reasoning.

**Anti-example.** [[p:salesforce-minimum-unique-segments-after-deletion|Minimum Unique-Character Segments After Deletion]] also cuts a string into the fewest contiguous segments, but with n up to 2 x 10^5. The rule "extend the segment until a letter repeats" is optimal there, so the prefix DP is not needed; a greedy scan is.

### B. Interval DP with a split point (the main derivation)

**What changes.** Nothing beyond the chapter's template: dp[i][j] over blocks, the min over the last wall m, the cost of the last operation. What varies between problems is that cost.

**Why.** The last operation on a block cuts it into two blocks that never interact again.

**Example.** Matrix chain multiplication: matrices of sizes 10x20, 20x30, 30x40. (AB)C costs 10·20·30 + 10·30·40 = 18,000; A(BC) costs 20·30·40 + 10·20·40 = 32,000. dp[i][j] = min over m of dp[i][m] + dp[m+1][j] + rows(i)·cols(m)·cols(j). The last multiplication's cost depends on m, which the recurrence allows. The bank has no matrix chain problem; the pattern is here because interviews elsewhere use it as the canonical example.

**Bank.** [[p:google-merge-stones|Minimum Cost to Merge Stones]] with k = 2 is exactly the chapter's problem. Its general k is variation D.

### C. Counting over the split: bracketings that evaluate to true

**What changes.** The cell counts instead of minimising. Across a split, the left and right choices are independent, so their counts **multiply**. Across different splits, the bracketings are different (the outermost operator differs), so the counts **add**. And since the operator decides whether true or false comes out, each cell keeps two numbers: T[i][j] and F[i][j], the ways operands i..j evaluate to true and to false.

**Why.** Every full bracketing has exactly one operator applied last. That is the split. Given that operator, a bracketing of the whole is a bracketing of the left times a bracketing of the right, and the operator's truth table says which combinations come out true:

```
&  : T = lT·rT                              
|  : T = all - lF·rF        all = (lT + lF)(rT + rF)
^  : T = lT·rF + lF·rT
F = all - T, in every case
```

**Example.** "T^F|F" has two bracketings: (T^F)|F = T|F = true, and T^(F|F) = T^F = true. So 2. "T&F|T": (T&F)|T = true, T&(F|T) = true: also 2. The program below checks the counting recurrence against listing every bracketing, and also checks Burst Balloons (variation D).

**Bank.** [[p:intuit-boolean-parenthesization|Count True Boolean Parenthesizations]], up to 19 operands, exact 64-bit count. The node's other "two indices with a split" problem is [[p:expedia-scramble-string|Scramble String]] (variation I).

```python run
import random
from itertools import combinations

def count_true(expr):                          # split at the operator applied LAST
    v, ops, n = expr[0::2], expr[1::2], len(expr) // 2 + 1
    T = [[int(v[i] == "T") if i == j else 0 for j in range(n)] for i in range(n)]
    F = [[int(v[i] == "F") if i == j else 0 for j in range(n)] for i in range(n)]
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            for k in range(i, j):              # ops[k] joins operands i..k and k+1..j
                lt, lf, rt, rf = T[i][k], F[i][k], T[k + 1][j], F[k + 1][j]
                ways = (lt + lf) * (rt + rf)   # counts MULTIPLY across a split
                t = {"&": lt * rt, "|": ways - lf * rf, "^": lt * rf + lf * rt}[ops[k]]
                T[i][j] += t                   # and ADD across different splits
                F[i][j] += ways - t
    return T[0][n - 1]

def all_values(expr):                          # brute force: every full parenthesisation
    if len(expr) == 1:
        return [expr == "T"]
    out = []
    for k in range(1, len(expr), 2):
        for a in all_values(expr[:k]):
            for b in all_values(expr[k + 1:]):
                out.append({"&": a and b, "|": a or b, "^": a != b}[expr[k]])
    return out

def burst(nums):                               # choose the balloon burst LAST in (i, j)
    a = [1] + nums + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]           # dp[i][j]: open interval, walls i and j stay
    for gap in range(2, n):
        for i in range(n - gap):
            j = i + gap
            dp[i][j] = max(dp[i][k] + a[i] * a[k] * a[j] + dp[k][j] for k in range(i + 1, j))
    return dp[0][n - 1]

def burst_brute(nums):
    if not nums:
        return 0
    return max((nums[t - 1] if t else 1) * nums[t] * (nums[t + 1] if t + 1 < len(nums) else 1)
               + burst_brute(nums[:t] + nums[t + 1:]) for t in range(len(nums)))

print("T^F|F:", count_true("T^F|F"), " T&F|T:", count_true("T&F|T"))
assert count_true("T^F|F") == 2 and count_true("T&F|T") == 2
print("burst [3,1,5,8]:", burst([3, 1, 5, 8]))
assert burst([3, 1, 5, 8]) == 167
random.seed(11)
for _ in range(200):
    e = random.choice("TF") + "".join(random.choice("&|^") + random.choice("TF")
                                      for _ in range(random.randint(0, 5)))
    assert count_true(e) == sum(all_values(e))
    b = [random.randint(1, 9) for _ in range(random.randint(0, 6))]
    assert burst(b) == burst_brute(b)
print("both agree with brute force on 200 random inputs")
```

### D. The last removal: Burst Balloons, merge stones with k piles, removing triples

This is the variation where "last, not first" stops being a matter of taste and becomes the difference between right and wrong.

**Burst Balloons (the archetype).** Balloons with numbers in a row. Bursting balloon k earns left · k · right, where left and right are its **current** neighbours (1 beyond the ends). Maximise the total. If you split on the balloon burst *first*, its neighbours afterwards are each other's neighbours: the two sides interact, and the recurrence is false. If you split on the balloon burst **last** in a block, then while the rest of the block is being burst, that balloon stands there as a wall, and the block's own boundaries (the balloons just outside it) are still standing too, because they are outside. So with an open interval (i, j), the walls i and j staying alive:

```
dp[i][j] = max over k in (i, j) of  dp[i][k] + a[i]·a[k]·a[j] + dp[k][j]
```

The cost of the last burst depends on the block's *outside* neighbours a[i] and a[j]. That is allowed; they are part of the state. [3, 1, 5, 8] gives 167 (burst 1, 5, 3, then 8). Not in this bank; it is the textbook case, and the Traps section shows the "first" version failing on it.

**Merge stones with k piles per move** ([[p:google-merge-stones|Minimum Cost to Merge Stones]], n <= 30). Each move merges exactly k consecutive piles. Now a block may not be mergeable into one pile at all: n piles become one only if (n - 1) is a multiple of (k - 1), otherwise the answer is -1. The standard state is dp[i][j] = the cheapest cost to merge block i..j into **as few piles as possible**, which is ((j - i) mod (k - 1)) + 1 piles. The wall m moves in steps of k - 1 (so the left part becomes exactly one pile), and the block's sum is added only when the block itself can collapse to one pile, (j - i) mod (k - 1) == 0. [3, 2, 4, 1] with k = 3 is impossible (-1); [3, 5, 1, 2, 6] with k = 3 costs 25. The extra condition is the "what do the parts still share" question of the checklist: a part that ends as two piles is not a finished pile yet.

**Removing arithmetic triples** ([[p:medianet-minimum-length-after-arithmetic-triple-removals|Minimum Length After Removing Arithmetic Triples]], n <= 200). Removals glue far elements together, which is exactly the situation where you reason about the block, not the moves. Two tables:

- R[i][j]: can the block a[i..j-1] be removed completely? Look at a[i]. It leaves in some triple (a[i], a[p], a[q]) with i < p < q. Before that triple goes, everything between i and p and everything between p and q must already be gone, and both are blocks that must vanish on their own. After the triple, the rest a[q+1..j-1] must vanish on its own too. So R[i][j] is true if some p, q make an arithmetic triple with R[i+1][p], R[p+1][q] and R[q+1][j] all true. (Block lengths are multiples of 3.)
- then a linear partition (variation A) on top: f[j] = the shortest remaining length of the prefix a[0..j-1], f[j] = min(f[j-1] + 1, min over i with R[i][j] of f[i]): either a[j-1] survives, or it is the end of a block that vanishes.

[1, 5, 6, 7, 4, 7]: (5, 6, 7) vanishes, then (1, 4, 7), so the answer is 0. This shape, "an interval table of what can vanish, then a prefix DP that chooses which blocks vanish", is worth recognising on its own.

### E. Two players on an interval: store the difference

**What changes.** Two players alternately take a coin from the left or right end of a row, each maximising their own total. The row that remains is always a contiguous block, so the state is (i, j). The value stored is **the mover's total minus the opponent's total from here on**, d[i][j], both playing optimally:

```
d[i][i] = a[i]
d[i][j] = max( a[i] - d[i+1][j],     take the left coin, then the other player is the mover on (i+1, j)
               a[j] - d[i][j-1] )    take the right coin
```

**Why the minus sign.** After I take a[i], the opponent becomes the mover on the block (i+1, j), and d[i+1][j] is *their* margin over me there. My margin is the coin minus their margin. Say it a second way: every cell is "the margin of whoever moves now", so at each move the point of view flips, and flipping a margin is negating it. This one sign is the subtle line of the variation. With a plus, the recurrence says "my coin plus my opponent's margin is good for me", which is the cooperative game in which one player takes everything: it returns the total sum, always.

**Example, by hand.** [8, 15, 3, 7]:

| | j=0 | j=1 | j=2 | j=3 |
|---|---|---|---|---|
| i=0 | 8 | 7 | -4 | **11** |
| i=1 | | 15 | 12 | 11 |
| i=2 | | | 3 | 4 |
| i=3 | | | | 7 |

- d[0][1] = max(8 - 15, 15 - 8) = 7. d[1][2] = max(15 - 3, 3 - 15) = 12. d[2][3] = max(3 - 7, 7 - 3) = 4.
- d[0][2] = max(8 - d[1][2], 3 - d[0][1]) = max(8 - 12, 3 - 7) = -4: on [8, 15, 3] the mover loses by 4 whatever they do.
- d[1][3] = max(15 - d[2][3], 7 - d[1][2]) = max(15 - 4, 7 - 12) = 11.
- d[0][3] = max(8 - d[1][3], 7 - d[0][2]) = max(8 - 11, 7 - (-4)) = **11**.

In words: "If I take the 8, the opponent faces [15, 3, 7] as the mover and beats me there by 11, so my margin is 8 - 11 = -3. If I take the 7, the opponent faces [8, 15, 3], where the mover *loses* by 4, so my margin is 7 + 4 = 11. Take the 7." The scores follow from the margin: first = (total + d) / 2 = (33 + 11) / 2 = 22, second 11. Greedy "take the bigger end" takes the 8 and ends 15 to 18: it loses.

```python run
from functools import lru_cache
import random

def diff_table(a, sign):
    n = len(a)
    d = [[0] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = a[i]                         # one coin: the mover takes it
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            d[i][j] = max(a[i] + sign * d[i + 1][j],   # take the left end
                          a[j] + sign * d[i][j - 1])   # take the right end
    return d

def right(a):  return diff_table(a, -1)[0][len(a) - 1]   # mover minus opponent
def wrong(a):  return diff_table(a, +1)[0][len(a) - 1]   # the sign flipped

def minimax(a):                                 # the truth: both scores, both players optimal
    @lru_cache(None)
    def best(i, j):                             # (mover's total, other's total) on a[i..j]
        if i > j:
            return (0, 0)
        o1, m1 = best(i + 1, j)                 # after I take a[i], the other moves
        o2, m2 = best(i, j - 1)
        return max((a[i] + m1, o1), (a[j] + m2, o2))
    me, other = best(0, len(a) - 1)
    return me - other

def greedy(a):                                  # both players take the larger end
    a, score, turn = list(a), [0, 0], 0
    while a:
        score[turn] += a.pop(0) if a[0] >= a[-1] else a.pop()
        turn ^= 1
    return score

for a in ([1, 5, 2], [4, 7, 2, 9], [8, 15, 3, 7], [20, 30, 2, 2, 2, 10]):
    print(a, "diff", right(a), "flipped sign", wrong(a), "first player gets", (sum(a) + right(a)) // 2)
    assert right(a) == minimax(a) and wrong(a) == sum(a)
assert right([1, 5, 2]) == -2 and right([4, 7, 2, 9]) == 10
assert (sum([8, 15, 3, 7]) + right([8, 15, 3, 7])) // 2 == 22 and greedy([8, 15, 3, 7]) == [15, 18]
assert (sum([20, 30, 2, 2, 2, 10]) + right([20, 30, 2, 2, 2, 10])) // 2 == 42
print("table for [8,15,3,7]:")
for row in diff_table([8, 15, 3, 7], -1):
    print("  ", row)
random.seed(3)
for _ in range(300):
    a = [random.randint(-9, 9) for _ in range(random.randint(1, 8))]
    assert right(a) == minimax(a)
    pos = [abs(x) + 1 for x in a + a[:len(a) % 2]]   # even length, positive values
    assert right(pos) >= 0                          # the first player never loses
print("difference table == two-score minimax on 300 random rows")
```

**Bank.** [[p:rippling-optimal-endpoint-score-difference|Optimal Score Difference in an Endpoint Game]] returns d[0][n-1] directly (with negative coins, so the parity trick below does not apply). [[p:openai-optimal-first-player-card-score|Optimal First-Player Card Score]] returns (total + d) / 2. [[p:tekion-coin-game-from-ends|Coin Game From The Ends]] asks whether the first player gets at least as much: d >= 0.

**A trap that is also a gift.** For an even-length row of positive coins, the first player can never lose: colour the positions alternately, sum each colour, and always take the coin of the richer colour; the opponent is then always forced onto the other colour. So Coin Game From The Ends is always true. Know the argument, and still know the DP, because the moment the question asks for the score, the margin, an odd length or negative coins, the parity trick says nothing.

**Space.** d[i][j] reads only blocks one shorter, so filling by length needs only the previous length's row: O(n) memory.

### F. Two players on a suffix

**What changes.** In [[p:google-stone-game-iii|Stone Game III]] each player removes the first 1, 2 or 3 stones from the front. What remains is always a suffix, so one index suffices: d[i] = the mover's margin on stones i..n-1,

```
d[i] = max over k in {1, 2, 3}, i + k <= n, of  (sum of stones i..i+k-1) - d[i+k]
```

**Why.** It is the interval game with one end pinned, the same move from (i, j) to (i) that took us from variation B to A.

**Example.** [1, 2, 3, 7]: d = -1, Bob wins. [1, 2, 3, -9]: Alice takes 1, 2, 3 and leaves Bob the -9, d = 15, Alice. Note the negative values: a player may be forced to take a bad stone, and "take as many as you like" is not allowed to be zero. n up to 50,000 makes the O(n) suffix form necessary.

### G. The interval pinned down by a counter

**What changes.** [[p:google-maximum-weighted-end-pick-score|Maximum Weighted End-Pick Score]] takes exactly m numbers from the ends of an array of length up to 10^5, the step-th pick multiplied by multipliers[step]. The remaining array is a block (i, j), but an n x n table is 10^10 cells. Notice that after `step` picks, of which `left` were from the left, the block is exactly i = left, j = n - 1 - (step - left). Two small numbers name it. So dp[step][left], with m <= 200: 40,000 cells.

**Why.** This is the checklist's last question, "what is small?", applied to the state. The interval is the honest state; the counters are a cheaper *name* for the same states, valid because only the reachable blocks matter.

**Example.** nums [1, 2, 3], multipliers [3, 2, 1]: take 3, 2, 1 from the right, 9 + 4 + 1 = 14. With nums [-5, -3, -3, -2, 7, 1] and multipliers [-10, -5, 3, 4, 6] the best is 102.

### H. Shrinking from both ends, no split

**What changes.** Some interval DPs have no loop over m at all: the cell looks only at its neighbours (i+1, j), (i, j-1), (i+1, j-1). The palindrome table of variation A is one; the longest palindromic subsequence is another (if s[i] == s[j], 2 + dp[i+1][j-1], else the max of dropping either end). The games in E are the same shape with a minus sign.

**Why.** The "last" operation is at an end of the block, so there is only one or two ways to make it. O(n^2) instead of O(n^3).

**Where it lives.** These are usually filed under [[palindromes]] and [[dp-strings]]. The fill-order rule is the same: a cell reads below and to the left, so fill by length or with i falling.

### I. Two strings split together

**What changes.** [[p:expedia-scramble-string|Scramble String]]: a string is split into two non-empty parts, which may be swapped, recursively. Is `second` a scramble of `first`? The state is a block of each string, of the same length: (i, j, length). The split point k is tried two ways, kept (first's left k characters against second's left k) and swapped (first's left k against second's right k).

**Why.** The last split (the top one in the recursion) divides both strings into two independent pairs of blocks. Because the two blocks always have equal length, three numbers name the state, n^3 states with O(n) splits each: O(n^4), fine for n <= 30.

**Example.** "great" and "rgeat": split "great" into "gr" | "eat", and "gr" swapped is "rg"; true. "abcde" and "caebd": false.

### J. Tree DP: choose or skip each node

**What changes.** The input is a tree. The block is a **subtree**; the parts are the children's subtrees; and each node needs a small vector of numbers, one per status it can be in. For "choose nodes, never a node together with its child" ([[p:zip-tree-independent-set|Maximum Nonadjacent Sum in a General Tree]], House Robber III on a general tree):

```
take[v] = value[v] + sum over children c of skip[c]
skip[v] =            sum over children c of max(take[c], skip[c])
answer  = max(take[root], skip[root])
```

**Why it belongs in this chapter.** Write the nodes in preorder (a DFS that lists a node before its children). Every subtree is then a **contiguous block** of that list. The tree DP is an interval DP whose blocks are not every (i, j), only the n subtree blocks, and whose "splits" are given by the tree instead of chosen. That is why it costs O(n), not O(n^3). The take/skip pair is the tree version of "what the future needs to know": the parent only needs to know whether this child was taken, not which nodes below it were.

**You might think: "take every other level".** On the path 10 - 1 - 1 - 10, the even levels give 10 + 1 = 11 and the odd levels 1 + 10 = 11, but taking both ends gives 20: the best set skips two levels in a row. **Or: "take the biggest node, then exclude its neighbours".** On a star with centre 5 and two leaves of 3, that takes 5; the leaves give 6.

**Example, by hand.** The bank's example, nodes [value, parent]: [[5,-1],[4,0],[6,0],[7,1],[2,1],[3,2]]. Node 0 (5) has children 1 (4) and 2 (6); node 1 has children 3 (7) and 4 (2); node 2 has child 5 (3). Since every parent has a smaller index than its children, visiting i = 5, 4, ..., 1 finishes every child before its parent, with no recursion:

| visit | parent | take[parent] | skip[parent] |
|---|---|---|---|
| start | | take = values, skip = 0 | |
| i=5 (take 3, skip 0) | 2 | 6 + 0 = 6 | 0 + max(3, 0) = 3 |
| i=4 (take 2, skip 0) | 1 | 4 + 0 = 4 | 0 + 2 = 2 |
| i=3 (take 7, skip 0) | 1 | 4 + 0 = 4 | 2 + 7 = 9 |
| i=2 (take 6, skip 3) | 0 | 5 + 3 = 8 | 0 + 6 = 6 |
| i=1 (take 4, skip 9) | 0 | 8 + 9 = 17 | 6 + 9 = 15 |

Answer max(17, 15) = **17**: nodes 0, 3, 4, 5 (5 + 7 + 2 + 3). The row i=1 is the one to read slowly: node 1 itself is worth 4 if taken, but its subtree is worth 9 *without* it (its children 7 and 2). So whether the root is taken or not, the best from node 1's subtree, given the root, comes from skipping node 1.

```python run
import random
from itertools import product

def best_nonadjacent(nodes):                   # nodes[i] = [value, parent], parent < i
    n = len(nodes)
    take = [v for v, _ in nodes]               # best in i's subtree if i IS chosen
    skip = [0] * n                             # best in i's subtree if i is NOT chosen
    for i in range(n - 1, 0, -1):              # children have larger ids: they finish first
        p = nodes[i][1]
        take[p] += skip[i]                     # p chosen: child i must be skipped
        skip[p] += max(take[i], skip[i])       # p skipped: child i is free
    return max(take[0], skip[0])

def brute(nodes):
    n, best = len(nodes), 0
    for pick in product((0, 1), repeat=n):
        if all(not (pick[i] and pick[nodes[i][1]]) for i in range(1, n)):
            best = max(best, sum(v for (v, _), x in zip(nodes, pick) if x))
    return best

example = [[5, -1], [4, 0], [6, 0], [7, 1], [2, 1], [3, 2]]
print("zip example:", best_nonadjacent(example))
assert best_nonadjacent(example) == brute(example) == 17

path = [[10, -1], [1, 0], [1, 1], [10, 2]]     # 10 - 1 - 1 - 10
print("path 10-1-1-10:", best_nonadjacent(path), "every other level would give", max(10 + 1, 1 + 10))
assert best_nonadjacent(path) == 20
star = [[5, -1], [3, 0], [3, 0]]               # greedy takes 5, best is 3 + 3
assert best_nonadjacent(star) == 6

random.seed(5)
for _ in range(300):
    n = random.randint(1, 10)
    t = [[random.randint(0, 9), -1]] + [[random.randint(0, 9), random.randrange(i)] for i in range(1, n)]
    assert best_nonadjacent(t) == brute(t)
print("take/skip pair == every subset on 300 random trees")
```

### K. Tree DP with three states

**What changes.** [[p:amazon-binary-tree-cameras|Binary Tree Cameras]]: a camera on a node watches the node, its parent and its children; find the fewest cameras that watch every node. Two statuses are not enough, because a node without a camera can be watched by a child *or* left for its parent to watch. Three numbers per node: has a camera; no camera but watched by a child; no camera and not yet watched (the parent must take care of it).

```
cam[v]  = 1 + sum over children of min(cam, watched, unwatched)
watched = sum over children of min(cam, watched), with at least one child a camera
            (add the cheapest "upgrade" min over children of cam - min(cam, watched) if none is)
unwatch = sum over children of watched          (no child camera, every child already watched)
answer  = min(cam[root], watched[root])         (the root has no parent to rely on)
```

A missing child counts as watched at cost 0 and can never be a camera.

**Why.** The third status is what the parent needs to know that two statuses could not say: "I still need someone to watch me." The forgotten line is the root: an unwatched root has no parent, so it is not a valid final state.

### L. One pass of subtree totals

**What changes.** [[p:twosigma-sewer-drainage-partition|Sewer Drainage Partition]] cuts one edge of a rooted tree (n up to 10^5) and minimises the difference between the two parts' totals. Cutting the edge above v leaves v's subtree on one side, so the difference is |total - 2·sub[v]|. One bottom-up pass computes every sub[v] (children have larger ids, so a reverse loop over i adds sub[i] into sub[parent[i]]), then a minimum over v != root.

**Why.** The simplest tree DP: one number per node, combined by a sum. It is here because it is the template every other tree DP elaborates.

### M. Tree knapsack: a node needs its parent

**What changes.** [[p:google-tree-dependent-knapsack|Tree-Dependent Knapsack]]: choose items under a capacity (<= 2,000), where an item may be chosen only if its parent is. List the nodes in preorder, and let end[v] be the position just after v's subtree block. Then, over preorder positions from the back,

```
g[pos][c] = max( g[end[v]][c],                          skip v: its whole subtree block is skipped
                 value[v] + g[pos + 1][c - cost[v]] )   take v: continue into its first child
```

**Why.** This is the preorder-is-intervals idea used literally: skipping a node must skip its descendants, and in preorder they are exactly the block up to end[v], so "skip" is a jump to the end of a block. Each position is one knapsack row: O(n · capacity), 400,000 cells. See also [[knapsack]], variation K, for the child-merging form.

### N. The rare ones

- **Cyclic rows** (piles in a circle): double the array and take the best block of length n. O(n^3) on 2n elements.
- **Knuth's optimisation** and **Garsia-Wachs** (see "What it costs").
- **Interval DP with an extra "colour" index**, such as "remove boxes", where a block also needs to know how many equal boxes are glued to its left end. It is the "what do the parts still share" question again, with a third index.
- **Rerooting** for tree DP, when the answer is wanted for every possible root; covered in [[tree-dp]].

## Recognising it in a statement

Ordered from the most reliable signal to the weakest.

1. **"Adjacent" or "consecutive" plus "merge", "combine", "remove" or "burst", with a cost that depends on what is merged.** Merge stones, burst balloons, removing triples that make neighbours adjacent. The phrase "the left and right parts join" is nearly a signature: it means the order of moves creates new adjacencies, and the cure is to reason about a block and its last move.
2. **"In how many ways can you parenthesise", "full parenthesisation", "order of operations", "evaluate in any order".** The operator applied last is the split. Matrix chain, boolean parenthesisation.
3. **"Two players take from either end", "both play optimally".** The remainder is a block; store the difference. If they take from one end only, it is a suffix (variation F).
4. **"Split into k contiguous parts", "partition the array (in order) into pieces", "cut the string into palindromes / words".** Linear partition, variation A. Check first whether a greedy is provably right.
5. **A tree, a value per node, and a rule linking a node to its parent or children.** "Cannot choose a node and its child", "a camera watches its neighbours", "requires its parent". Tree DP, variations J to M.
6. **n small: at most a few hundred, sometimes 30 or 50.** On its own this proves nothing, but together with a contiguity rule it points straight at O(n^3).
7. **A string, a recursive split, and swaps or reversals of parts.** Scramble String, variation I.

### Disguised forms

- **"Cut a stick of length L at given positions; each cut costs the current length of the piece being cut."** Sort the cut positions and add the two ends: c = [0, cuts..., L]. The *first* cut of a piece is the one whose cost is the piece's length, and after it the two parts are independent. Reversing time turns it into merging: dp[i][j] over the open interval between cut points c[i] and c[j], min over the cut k between them of dp[i][k] + dp[k][j] + (c[j] - c[i]). It is merge stones in which the "piles" are the gaps between cuts. Here splitting on the first cut is correct, because a cut, unlike a burst balloon, really does separate the two sides.
- **"Delete characters / elements one by one, each deletion scores something depending on its neighbours."** The deletion order is the noise; the last deletion in a block is the wall. Burst Balloons in costume.
- **"The first player wins if..." on a row of numbers.** Compute the margin; win means margin > 0 (or >= 0, read the statement).
- **"Choose a subset of employees, no one together with their direct manager."** Independent set on the reporting tree, variation J.
- **"Minimum number of pieces such that each piece is X."** Linear partition with a validity table, often an interval table itself (palindromes).

### Anti-signals: looks like this, is not

- **"Partition into two subsets", "split into groups with equal sums".** No order is kept. Knapsack or subset sum.
- **"Partition labels", "as many parts as possible", "each letter in one part".** Greedy, linear.
- **"Return all partitions".** Backtracking.
- **"Merge any two piles".** Huffman: a heap and a greedy.
- **A contiguous subarray with some sum or property, and nothing is merged or cut.** [[prefix-sums]] or [[sliding-window]].
- **Two strings and "edit", "common", "interleave".** Two-string DP: two indices, but no split loop.

## Traps

**1. Filling the table in the wrong order.** Symptom: correct on two or three elements, too cheap (for a minimum) or simply wrong on longer inputs; the wrong cells are always ones that read a cell from a *lower row*. Cause: `for i in range(n): for j in range(i+1, n)` reads dp[m+1][j] before it exists. Cure: fill by length, or with i falling. Demonstrated in "From the idea to the code".

**2. Splitting on the first operation when the last one is the wall.** Symptom: an answer that looks plausible and is wrong by a lot. In Burst Balloons, choosing the *first* balloon to burst and pricing it with its original neighbours assumes the two sides stay apart afterwards, and they do not: the moment balloon k is gone, its two neighbours are neighbours of each other. The demonstration below replays every order honestly and compares.

```python run
from functools import lru_cache
from itertools import permutations

def score_of_order(nums, order):               # replay an order of bursts, honestly
    row, alive, total = [1] + nums + [1], list(range(1, len(nums) + 1)), 0
    for k in order:
        p = alive.index(k)
        left = row[alive[p - 1]] if p > 0 else 1
        right = row[alive[p + 1]] if p + 1 < len(alive) else 1
        total += left * row[k] * right
        alive.pop(p)
    return total

def split_on_first(nums):                      # WRONG: k is burst FIRST, priced with its original neighbours
    a = [1] + nums + [1]
    @lru_cache(None)
    def f(i, j):
        if i > j:
            return 0
        return max(a[k - 1] * a[k] * a[k + 1] + f(i, k - 1) + f(k + 1, j) for k in range(i, j + 1))
    return f(1, len(nums))

def split_on_last(nums):                       # right: k is burst LAST; i-1 and j+1 are still there
    a = [1] + nums + [1]
    @lru_cache(None)
    def f(i, j):
        if i > j:
            return 0
        return max(f(i, k - 1) + a[i - 1] * a[k] * a[j + 1] + f(k + 1, j) for k in range(i, j + 1))
    return f(1, len(nums))

nums = [3, 1, 5, 8]
truth = max(score_of_order(nums, o) for o in permutations(range(1, 5)))
print("every order:", truth, "| split on first:", split_on_first(nums), "| split on last:", split_on_last(nums))
assert truth == split_on_last(nums) == 167 and split_on_first(nums) == 98
best = max(permutations(range(1, 5)), key=lambda o: score_of_order(nums, o))
print("an optimal order bursts balloons", [nums[k - 1] for k in best], "and 8 goes last")
assert [nums[k - 1] for k in best][-1] == 8
# Split on first: burst 1 first (3*1*5), then the "left half" [3] is priced as 1*3*1 = 3.
# But 1 is gone, so 3's right neighbour is now 5: bursting 3 next really earns 1*3*5 = 15.
assert score_of_order(nums, [2, 1]) == 3 * 1 * 5 + 1 * 3 * 5
```

Read the failure on [3, 1, 5, 8]. The first-split recurrence prices bursting 1 first as 3·1·5 = 15, and then prices the left half [3] on its own as 1·3·1 = 3, as if the balloon 1 were still standing to its right. But it is gone: 3's right neighbour is now 5, and bursting 3 next really earns 1·3·5 = 15. The "independent halves" were never independent. The first-split version tops out at 98; the truth is 167. With the split on the **last** balloon, the walls i-1 and j+1 are still standing while the inside is burst, and the halves really are independent.

**3. The game sign.** Symptom: the "difference" equals the sum of all coins, for every input. Cause: `a[i] + d[i+1][j]` instead of `a[i] - d[i+1][j]`. The second player's best margin is bad for the first player. Demonstrated in variation E, which asserts that the flipped version always returns the total.

**4. Mixing "best score" and "best margin".** Symptom: wrong answers on rows with negative values or odd length. Some people store "the mover's best total" and write best[i][j] = max(a[i] + (S(i+1, j) - best[i+1][j]), ...). That is correct, but only with the block sum; forgetting the sum, or mixing the two formulations between cells, breaks it. Pick the margin, convert at the end with (total + margin) / 2.

**5. Greedy on games.** Symptom: [8, 15, 3, 7]; take-the-bigger-end loses 15 to 18, the DP wins 22 to 11. The bigger end can open the door to a much bigger coin for the opponent.

**6. An O(n^4) that should be O(n^3).** Symptom: time limit exceeded at n = 200. Cause: summing the block inside the loop over walls. Cure: prefix sums, or compute S(i, j) once per cell.

**7. The wall's range.** Symptom: an index error, or a cell that "merges" with an empty block. m runs from i to j - 1 for inclusive ends; k runs strictly between i and j for open intervals (Burst Balloons). Write which convention you use next to the state definition.

**8. Impossible blocks treated as zero.** Symptom: merge stones with k = 3 returns a cost where the answer should be -1. Cause: blocks that cannot become one pile still get a value, and that value is added as if they had. Cure: check (n - 1) % (k - 1) == 0 first, step the wall by k - 1, and add the sum only for collapsible blocks.

**9. Tree recursion depth.** Symptom: RecursionError on a path-shaped tree of 10^4 nodes. Cure: when parents have smaller ids than children, as in Maximum Nonadjacent Sum in a General Tree and Sewer Drainage Partition, a reverse loop over ids is a valid bottom-up order and needs no recursion. Otherwise build an explicit DFS order with a stack.

**10. The root in multi-state tree DP.** Symptom: Binary Tree Cameras off by one on a single node. Cause: returning min over all three statuses, including "not yet watched", which only makes sense when a parent exists. The root's answer is min(camera, watched).

**11. Treating the parity shortcut as general.** Symptom: wrong answers when the row has odd length, negative values, or the question asks for a score. The shortcut only proves "the first player does not lose" for even-length rows of non-negative coins.

## What to memorise

The template, for the core case:

```python
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = min(dp[i][m] + dp[m + 1][j] for m in range(i, j)) + cost(i, j)
```

The game, as a margin:

```python
d[i][j] = max(a[i] - d[i + 1][j], a[j] - d[i][j - 1])
```

The tree, as a pair per node:

```python
take[v] = val[v] + sum(skip[c]);  skip[v] = sum(max(take[c], skip[c]))
```

**The sentence that turns a problem into it:** "Look at the last thing that happens to a block; if it splits the block into parts that never touch again, the block's two ends are the state."

**The habit that prevents the common bug:** before writing the loops, draw one cell and the cells it reads. Interval cells read to the left and below, so fill shortest blocks first.

**The numbers:** (n^3 - n) / 6 wall checks; n <= 500 is the ceiling for cubic in Python; n(n+1)/2 blocks; games and shrink-from-the-ends DPs are O(n^2); tree DPs are O(n).

## Check yourself

:::check
Fill the table for piles 1, 3, 1, 2 (merge neighbours, cost = stones in the new pile). For every cell of length 3 and 4, write the walls you compared. What is the cheapest total, and what is the plan?
--
Prefix sums 0, 1, 4, 5, 7. Length 2: dp[0][1] = 4, dp[1][2] = 4, dp[2][3] = 3. Length 3: dp[0][2] (S = 5): walls 0 + 4 = 4 and 4 + 0 = 4, so 4 + 5 = 9. dp[1][3] (S = 6): walls 0 + 3 = 3 and 4 + 0 = 4, so 3 + 6 = 9. Length 4: dp[0][3] (S = 7): walls 0 + 9 = 9, 4 + 3 = 7, 9 + 0 = 9, so 7 + 7 = **14**. The table, rows i = 0..3: [0, 4, 9, 14], [-, 0, 4, 9], [-, -, 0, 3], [-, -, -, 0]. The plan is (1 3)(1 2): merge 1+3 = 4, merge 1+2 = 3, then 7. 4 + 3 + 7 = 14. Note the tie in dp[0][2]: both walls give 4, and either plan is optimal for that block.
:::

:::check
Now fill the same piles 1, 3, 1, 2 with the wrong order, rows from the top (`for i in range(4): for j in range(i+1, 4)`), with unfilled cells reading 0. Which cell is the first to go wrong, which cell did it read too early, and what answer comes out?
--
Order: (0,1), (0,2), (0,3), (1,2), (1,3), (2,3). dp[0][1] = 4, correct. dp[0][2] is first to go wrong: the wall after 0 reads dp[1][2], which is still 0, so it gives 0 + 0 + 5 = 5 instead of 9. dp[0][3]: walls read dp[1][3] = 0, dp[0][1] + dp[2][3] = 4 + 0, dp[0][2] + dp[3][3] = 5 + 0; minimum 0, plus 7 = 7. Then dp[1][2] = 4, dp[1][3] = min(0 + 0, 4 + 0) + 6 = 6 (wrong, reads dp[2][3] early), dp[2][3] = 3. The answer comes out **7**, which is just the cost of the final merge: the wrong order priced everything below the corner as free.
:::

:::check
Two players take a coin from either end of [3, 9, 1, 2]. Fill the margin table d[i][j] by hand. What is the first player's best margin, their score, and their first move? What does take-the-bigger-end score for the first player?
--
Length 1: 3, 9, 1, 2. Length 2: d[0][1] = max(3 - 9, 9 - 3) = 6; d[1][2] = max(9 - 1, 1 - 9) = 8; d[2][3] = max(1 - 2, 2 - 1) = 1. Length 3: d[0][2] = max(3 - d[1][2], 1 - d[0][1]) = max(-5, -5) = -5; d[1][3] = max(9 - d[2][3], 2 - d[1][2]) = max(8, -6) = 8. Length 4: d[0][3] = max(3 - d[1][3], 2 - d[0][2]) = max(3 - 8, 2 + 5) = **7**. The first move is the right coin, 2: it leaves [3, 9, 1], where the mover loses by 5, and whichever end the opponent takes, the 9 becomes available. Score: (15 + 7) / 2 = 11 (2 + 9), opponent 4. Greedy takes 3 (3 >= 2), the opponent takes 9, and greedy finishes with 3 + 2 = 5 against 10.
:::

:::check
Why does Burst Balloons split on the balloon burst last in a block and not the one burst first, while "cut a stick" may split on the first cut? Answer in two or three sentences.
--
The split is only valid if the two parts never interact again. Bursting a balloon first makes its two neighbours adjacent, so the left and right parts interact afterwards; bursting it last means it stands as a wall while both sides are burst, and the block's outer neighbours are fixed, so the parts are independent and the last burst's price a[i]·a[k]·a[j] is known. Cutting a stick, by contrast, physically separates the two pieces, so after the first cut they really never interact again, and the first cut is a clean wall.
:::

:::check
Someone claims: "For the coin game the state should be (i, j, whose turn), and I need two tables, one for each player's best total." Where are they right and where are they making it harder than necessary?
--
They are right that the information is sufficient: (i, j) plus the player to move describes the situation, and two tables of totals can be made to work. But the turn is already determined by (i, j) (it is the parity of how many coins are gone), and more importantly the two players' situations are symmetric: on any block, the mover faces the same problem whoever they are. Storing the mover's margin, d[i][j] = max(a[i] - d[i+1][j], a[j] - d[i][j-1]), uses one table, no turn index, and one minus sign for the change of point of view. The first player's score is recovered at the end as (total + d) / 2.
:::

:::check
A stick of length 7 must be cut at positions 1, 3, 4 and 5. Each cut costs the length of the piece it is made in. Reduce it to an interval DP: what are the "piles", the state, the recurrence, the base, and the answer? (Bonus: the minimum is 16; find a cut order that achieves it.)
--
Sort the cuts and add the ends: c = [0, 1, 3, 4, 5, 7]. State dp[i][j] = cheapest cost to make every cut strictly between c[i] and c[j], for the piece from c[i] to c[j]. Recurrence: dp[i][j] = min over i < k < j of dp[i][k] + dp[k][j] + (c[j] - c[i]), because the first cut made in that piece costs its full length and leaves two independent pieces. Base: dp[i][i+1] = 0 (no cut inside). Answer dp[0][5]. The "piles" are the gaps between consecutive points, lengths 1, 2, 1, 1, 2, and the cost is the merge-stones cost run backwards in time. One optimal order: cut at 3 first (7), then at 5 in the piece 3..7 (4), then at 4 in 3..5 (2), then at 1 in 0..3 (3): 7 + 4 + 2 + 3 = 16.
:::

:::check
Trace the take/skip tree DP on this tree: node 0 has value 1 and children 1 (value 4) and 2 (value 5); node 1 has children 3 (value 3) and 4 (value 3). Write take and skip for every node, then the answer and the chosen set. Then say what "every other level" would choose.
--
Leaves: take[3] = 3, skip[3] = 0; take[4] = 3, skip[4] = 0; take[2] = 5, skip[2] = 0. Node 1: take = 4 + 0 + 0 = 4; skip = max(3, 0) + max(3, 0) = 6. Node 0: take = 1 + skip[1] + skip[2] = 1 + 6 + 0 = 7; skip = max(4, 6) + max(5, 0) = 6 + 5 = 11. Answer max(7, 11) = **11**: nodes 2, 3, 4 (5 + 3 + 3), which mixes levels 1 and 2. Levels: level 0 = 1, level 1 = 4 + 5 = 9, level 2 = 3 + 3 = 6; even levels 1 + 6 = 7, odd level 9. Both lose to 11.
:::

:::check
Someone wants to decide whether an array of n = 2,000 numbers (some negative) can be cut into exactly k contiguous pieces, each with sum at least x >= 1, and writes ok[p][i] = "the first i elements can be cut into p valid pieces", with a loop over the last piece. What does it cost, and how do you remove the p dimension?
--
k · n · n, up to 2,000^3 = 8 x 10^9 steps: far too slow. The fix is a fact about the answers: if p valid pieces exist, merging any two neighbouring pieces gives p - 1 valid pieces, because two sums of at least x add up to at least 2x >= x. So the achievable piece counts for the whole array are exactly 1..max, and it is enough to compute the maximum: best[i] = max over j < i with best[j] reachable and P[i] - P[j] >= x of best[j] + 1, then answer best[n] >= k. That is O(n^2) = 4 million steps.
:::
