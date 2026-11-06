# Knapsack

> Knapsack works because the future needs only two numbers from the past, which items are still allowed and how much room is left, so 2^n subsets collapse into (n+1)(W+1) situations that are each solved once.

## The problem it solves

You have a bag that holds at most 7 kilograms and four things you might pack:

| item | weight | value |
|---|---|---|
| A | 1 | 1 |
| B | 3 | 4 |
| C | 4 | 5 |
| D | 5 | 7 |

Each item is either in the bag or not. You cannot take half of one, and you cannot
take two of the same one. What is the most value you can carry?

That is the whole of 0/1 knapsack: a list of items, each with a weight and a
value, one shared limit, and a yes-or-no decision per item. The "0/1" means each
item is used zero times or one time.

The first solution anyone writes is to try every subset. Four items have
2^4 = 16 subsets. List them, throw away the ones heavier than 7, keep the most
valuable one. For this bag the winner is {B, C}: weight 3 + 4 = 7, value
4 + 5 = 9. Trying everything is correct, and for four items it is fine.

It stops being fine fast. Every new item doubles the number of subsets. Twenty
items give about a million. Forty give about a trillion. The 0/1 knapsack problems
in this bank, such as [[p:amazon-zero-one-knapsack|0/1 Knapsack]], allow 200 items,
and 2^200 is a number with 61 digits. No computer will list those subsets.

The second solution anyone writes is a greedy rule. Two are popular, and both are
wrong.

- "Take the item with the best value per kilogram first." The ratios are A 1.0,
  B 1.33, C 1.25, D 1.4. Greedy takes D (5 kg, value 7), then B does not fit in
  the 2 kg left, C does not fit, A does: total weight 6, value 8. The best is 9.
- "Go through the items and take each one if it still fits." In the order
  A, B, C, D this takes A and B (4 kg, value 5), then C does not fit, D does not
  fit: value 5. Worse.

Greedy fails here for one reason: items do not split. A greedy rule is right for
the *fractional* knapsack, where you may take 2/5 of item D, because then no
kilogram is ever wasted. With whole items, a locally good item can leave a gap
that only a different combination would have filled.

What this chapter builds is a method that is exact like the brute force and fast
like a loop: for 200 items and a 10,000 kg bag it does about two million small
steps. It is a direct application of [[dynamic-programming]], and that chapter's
ideas (state, transition, base case, order) are assumed here.

### When it is the wrong tool

Knapsack is not always the answer to "choose a subset under a limit".

- **The items are divisible.** Fractional knapsack is a greedy by ratio, sorted
  once.
- **Every item has the same weight, or the same value.** Then sorting wins. In
  [[p:google-unit-weight-knapsack|Unit-Weight Knapsack with Limited Quantities]]
  every item weighs one unit, so the best bag of k items is simply the k most
  valuable units. The capacity there is up to 10^9, so a knapsack table could not
  even be allocated. In [[p:infosys-maximize-purchases-cooler-bag|Maximum Purchases with a Cooler-Bag Fee]]
  you maximise the *number* of items bought, every item is worth 1, and the
  cheapest-first rule is optimal.
- **The limit is huge and the items are few.** With 40 items and a limit of 10^9,
  the table has 10^9 columns. You split the items in half instead
  ([[meet-in-the-middle]]).
- **The values have special structure.** In
  [[p:fortinet-calculate-maximum-profit|Madam C.J. Walker's Business Plan]] item i
  is worth 2^i. Since 2^i is bigger than all smaller powers put together, taking
  the highest index you can afford beats every set of lower ones, and a greedy from
  the top is exact.
- **The choice is contiguous.** "A subarray that sums to k" is not a subset. That
  is [[prefix-sums]], not knapsack. Problems such as
  [[p:amazon-count-subarrays-with-target-sum|Count Subarrays With Target Sum]]
  look similar and are a different family.

Fourteen problems in this bank are tagged knapsack. Many more are knapsack in
disguise: subset sum, equal partition, minimum difference, coin change, "ones and
zeroes", budgets. The sections below name them where they teach something.

## Build it from the brute force

We will not start with a table. We will start with the slowest correct program a
beginner would write, and fix it one waste at a time. The table will appear at
the end, as the obvious thing to do.

### Step 1: one decision at a time

The brute force "try every subset" can be written as a sequence of decisions. Look
at the last item. Either it is in the bag, or it is not. Those are the only two
possibilities, and every subset falls into exactly one of them.

- If the last item is **not** in the bag, the rest of the bag is some choice among
  the other items, with the full limit still available.
- If the last item **is** in the bag, it uses up its weight, and the rest of the
  bag is some choice among the other items with that much less room.

Write that as a function. Number the items 1 to n. Let

> f(i, c) = the most value I can carry if I may only use items 1..i and my bag
> holds at most c.

Then:

```
f(i, c) = f(i-1, c)                          skip item i
f(i, c) = max(that, v_i + f(i-1, c - w_i))   take item i, only if w_i <= c
f(0, c) = 0                                  no items allowed: nothing to carry
```

The answer is f(n, W).

Read the take branch slowly. After taking item i, two things change: item i is no
longer available (so the first argument drops to i-1) and the room shrinks by
w_i (so the second argument drops to c - w_i). The value v_i is collected now.
Everything else comes from the smaller problem.

### You might think: "I only need one call. Take it if it fits."

This is the most common first instinct, and it is wrong. "If the item fits, take
it, otherwise skip it" makes one decision per item, and the decision is greedy.

The counterexample is small. Limit 10, items in this order: (w=6, v=13),
(w=5, v=10), (w=5, v=10). "Take it if it fits" takes the first item, value 13, and
4 units are left. Neither of the others fits. Final value 13. But skipping the
first item and taking the other two weighs exactly 10 and is worth 20.

So sometimes the right move is to skip an item that fits. You cannot know at the
moment of deciding whether this is one of those times, because it depends on the
items you have not looked at yet. That is why the recursion tries both and keeps
the better result. Two calls are not a style; they are the whole point.

### You might think: "The answer for limit 5 is the answer for limit 4 plus something."

This instinct says the state is only the limit: g(c) = best value for a bag of
size c, and maybe g(c) = max over items j of g(c - w_j) + v_j.

Try it on one item, (w=2, v=5), with limit 6. g(0) = g(1) = 0, g(2) = g(0) + 5 = 5,
g(4) = g(2) + 5 = 10, g(6) = g(4) + 5 = 15. But there is only one item. The real
answer is 5.

The formula is not wrong arithmetic. It answers a different question. A state
that holds only "how much room is left" has no way to say "item j is already in
the bag", so it lets you put item j in again and again. That is a real problem
with its own name, unbounded knapsack ([[unbounded-knapsack]]), and coin change
is exactly this. For 0/1 knapsack the state must also remember which items are
still allowed.

### Step 2: count it

How slow is the two-call recursion? Each call with i > 0 makes up to two calls
with i - 1. That is a binary tree of depth n, so up to 1 + 2 + 4 + ... + 2^n =
2^(n+1) - 1 calls. For n = 200 that is the same astronomical number as listing
the subsets, which makes sense: the recursion *is* the list of subsets, written as
a tree. Every root-to-leaf path is one subset.

So far we have only rewritten the brute force. It is correct and just as slow. The
question is where the time goes.

### Step 3: notice the waste

Take three small items: X (w=1, v=2), Y (w=2, v=3), Z (w=2, v=4), and limit 4.
Start at f(3, 4) and decide Z first, then Y, then X. Here is the whole tree.

<svg viewBox="0 0 760 330" role="img" aria-label="the recursion tree of f(3,4) for items X, Y, Z: the state f(1,2) is reached twice, once by skipping Z and taking Y, once by taking Z and skipping Y, and both copies are shaded">
  <g>
    <rect x="342" y="15" width="76" height="30" rx="4"/>
    <text x="380" y="35" text-anchor="middle">f(3,4)</text>
    <rect x="162" y="95" width="76" height="30" rx="4"/>
    <text x="200" y="115" text-anchor="middle">f(2,4)</text>
    <rect x="522" y="95" width="76" height="30" rx="4"/>
    <text x="560" y="115" text-anchor="middle">f(2,2)</text>
    <rect x="62" y="175" width="76" height="30" rx="4"/>
    <text x="100" y="195" text-anchor="middle">f(1,4)</text>
    <rect class="fill" x="262" y="175" width="76" height="30" rx="4"/>
    <text x="300" y="195" text-anchor="middle">f(1,2)</text>
    <rect class="fill" x="422" y="175" width="76" height="30" rx="4"/>
    <text x="460" y="195" text-anchor="middle">f(1,2)</text>
    <rect x="622" y="175" width="76" height="30" rx="4"/>
    <text x="660" y="195" text-anchor="middle">f(1,0)</text>
    <rect x="18" y="255" width="64" height="30" rx="4"/>
    <text x="50" y="275" text-anchor="middle">f(0,4)</text>
    <rect x="118" y="255" width="64" height="30" rx="4"/>
    <text x="150" y="275" text-anchor="middle">f(0,3)</text>
    <rect x="223" y="255" width="64" height="30" rx="4"/>
    <text x="255" y="275" text-anchor="middle">f(0,2)</text>
    <rect x="313" y="255" width="64" height="30" rx="4"/>
    <text x="345" y="275" text-anchor="middle">f(0,1)</text>
    <rect x="383" y="255" width="64" height="30" rx="4" stroke-dasharray="5 4"/>
    <text x="415" y="275" text-anchor="middle">f(0,2)</text>
    <rect x="473" y="255" width="64" height="30" rx="4" stroke-dasharray="5 4"/>
    <text x="505" y="275" text-anchor="middle">f(0,1)</text>
    <rect x="628" y="255" width="64" height="30" rx="4"/>
    <text x="660" y="275" text-anchor="middle">f(0,0)</text>
    <line x1="370" y1="45" x2="210" y2="95"/>
    <line x1="390" y1="45" x2="550" y2="95"/>
    <line x1="190" y1="125" x2="110" y2="175"/>
    <line x1="210" y1="125" x2="290" y2="175"/>
    <line x1="550" y1="125" x2="470" y2="175"/>
    <line x1="570" y1="125" x2="650" y2="175"/>
    <line x1="90" y1="205" x2="55" y2="255"/>
    <line x1="110" y1="205" x2="145" y2="255"/>
    <line x1="290" y1="205" x2="260" y2="255"/>
    <line x1="310" y1="205" x2="340" y2="255"/>
    <line x1="450" y1="205" x2="420" y2="255" stroke-dasharray="5 4"/>
    <line x1="470" y1="205" x2="500" y2="255" stroke-dasharray="5 4"/>
    <line x1="660" y1="205" x2="660" y2="255"/>
    <text x="280" y="62" text-anchor="end">skip Z</text>
    <text x="480" y="62">take Z</text>
    <text x="140" y="148" text-anchor="end">skip Y</text>
    <text x="262" y="148">take Y</text>
    <text x="500" y="148" text-anchor="end">skip Y</text>
    <text x="622" y="148">take Y</text>
    <text x="380" y="308" text-anchor="middle">left edge: skip the item; right edge: take it. f(1,0) has no take: X does not fit.</text>
    <text x="380" y="325" text-anchor="middle">Shaded: one situation, reached twice. The dashed subtree repeats work already done.</text>
  </g>
</svg>

Look at the two shaded boxes. Both say f(1, 2). One was reached by "skip Z, take
Y". The other by "take Z, skip Y". Those are different histories: different
items are in the bag, and the bag holds different values so far (3 versus 4).
But the question each one asks about the *future* is identical: "I may still use
item X, and I have 2 units of room. What is the most I can add?" The answer is 2
(take X) in both. The tree computes it twice, and the dashed subtree under the
second copy is pure repetition.

The leaves repeat too: f(0, 2) and f(0, 1) appear twice each. In this tiny tree
the waste is three boxes out of fourteen. With 200 items and a bag of 10,000 it is
almost everything: the tree has up to 2^201 nodes, but the boxes can only say
f(i, c) for i in 0..200 and c in 0..10,000. That is about two million different
labels. Nearly all of the tree is the same two million questions asked over and
over.

### The question that unlocks it

Why did the two different histories collapse into one box? Because the future does
not care how you got here. It does not care which items are in the bag, or what
they are worth. It cares about exactly two things: which items you may still
decide about, and how much room is left.

That is the question to ask on every problem in this family, and on every DP
problem:

**What is the least the future needs to know about the past?**

For 0/1 knapsack the answer is (i, c): "items 1..i are still undecided" and "c
units of room are left". The value already collected is *not* part of the state,
because the future adds to it whatever is best, regardless of what it is. Two
paths with different collected values and the same (i, c) have the same best
future, so you only need to solve that future once and add it to each.

Say it a second way. The past is a long story: "I looked at Z, put it in, looked
at Y, left it out." The future only reads the last line of the story: "X left,
room 2." DP is the decision to stop telling the story and keep only that line.

### Step 4: remember answers (memoisation)

The cure for asking the same question twice is to write down the answer the first
time. Keep a dictionary from (i, c) to f(i, c). Before computing, look it up.

The recursion is unchanged. Only the bookkeeping is new. Now each distinct (i, c)
is computed once, and each computation does O(1) work besides its two lookups, so
the total work is at most (n+1)(W+1) steps. For the bank's limits that is two
million instead of 2^201.

The following program runs both versions, counts the calls of the brute force and
the distinct states of the memo, and checks both against plain enumeration of
every subset.

```python run
from functools import lru_cache
from itertools import combinations
import random

def brute(items, W):
    calls = 0
    def f(i, c):                      # best value, first i items, bag c
        nonlocal calls
        calls += 1
        if i == 0:
            return 0                  # no items allowed: nothing to add
        w, v = items[i - 1]           # item i lives at index i-1
        best = f(i - 1, c)            # skip item i
        if w <= c:                    # take item i, if it fits
            best = max(best, v + f(i - 1, c - w))
        return best
    return f(len(items), W), calls

def memo(items, W):
    seen = {}                         # (i, c) -> answer
    def f(i, c):
        if (i, c) in seen:
            return seen[(i, c)]
        if i == 0:
            ans = 0
        else:
            w, v = items[i - 1]
            ans = f(i - 1, c)
            if w <= c:
                ans = max(ans, v + f(i - 1, c - w))
        seen[(i, c)] = ans
        return ans
    return f(len(items), W), len(seen)

def every_subset(items, W):           # the truth, by enumeration
    best = 0
    for k in range(len(items) + 1):
        for s in combinations(items, k):
            if sum(w for w, _ in s) <= W:
                best = max(best, sum(v for _, v in s))
    return best

xyz = [(1, 2), (2, 3), (2, 4)]        # X, Y, Z
print("X,Y,Z, W=4:", brute(xyz, 4), memo(xyz, 4))
abcd = [(1, 1), (3, 4), (4, 5), (5, 7)]
print("A,B,C,D, W=7:", brute(abcd, 7), memo(abcd, 7))
assert brute(abcd, 7)[0] == memo(abcd, 7)[0] == every_subset(abcd, 7) == 9

random.seed(1)
items = [(random.randint(1, 10), random.randint(1, 30)) for _ in range(16)]
(b, calls), (m, states) = brute(items, 40), memo(items, 40)
print("16 items, W=40: brute calls", calls, "memo states", states)
assert b == m == every_subset(items, 40)
assert states <= (16 + 1) * (40 + 1) < calls
for _ in range(200):                  # random small cases agree with enumeration
    its = [(random.randint(1, 6), random.randint(0, 9)) for _ in range(random.randint(0, 7))]
    W = random.randint(0, 15)
    assert memo(its, W)[0] == every_subset(its, W)
print("memo == every subset on 200 random cases")
```

On X, Y, Z the brute force makes 14 calls (the 14 boxes in the picture) and the
memo solves 11 distinct states (14 minus the three repeats). On sixteen random
items the gap is already about 70,000 calls against under 500 states. The gap
grows exponentially with n.

### Step 5: fill the answers in order (the table)

The memo works, but it decides the order of work by recursion: it asks f(n, W),
which asks f(n-1, ...), and so on down to row 0. We can do the same work without
recursion if we compute the answers in an order where everything a cell needs is
already known.

What does f(i, c) need? Only f(i-1, c) and f(i-1, c - w_i). Both are in row i-1.
So if we compute all of row 0, then all of row 1, then all of row 2, every lookup
finds its answer ready. Store row i in a list indexed by c, and you have a table
dp[i][c] with n+1 rows and W+1 columns.

### You might think: "Each cell stores the weight and the best value."

It stores only the best value. The weight is not stored anywhere in the cell. It
is the column number. dp[2][5] means "the first 2 items allowed, a bag of size
5", and the 5 is where the cell sits, not what it contains. The cell does not even
store *which* items achieved its value; we will recover those later by comparing
neighbouring cells.

A cell also does not mean "the bag is filled to exactly c". It means "at most c".
dp[1][7] = 1 in the example below, although item A only weighs 1. Six units are
empty, and that is allowed.

### Step 6: keep only one row

Row i is computed from row i-1 alone. Once row i is done, rows 0..i-1 are never
read again. So in principle one row of W+1 numbers is enough, rewritten in place
for each item. Doing that correctly needs exactly one subtle line, the direction
of the inner loop, and it gets its own demonstration in "From the idea to the
code".

### The technique in one sentence

**0/1 knapsack: the state is (items still allowed, room left); each state is the
better of skipping the next item and taking it, and since the future depends only
on that state, the 2^n subsets collapse into an (n+1) x (W+1) table filled row by
row.**

And the question that produced it, worth asking again on every new problem:
**what is the least the future needs to know about the past?**

## Worked by hand

Get a pen. Items A (1, 1), B (3, 4), C (4, 5), D (5, 7), limit W = 7. Rows are
"how many items are allowed", columns are "how big is the bag".

| | c=0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| row 0 (no items) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| row 1 (+A: w1 v1) | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| row 2 (+B: w3 v4) | 0 | 1 | 1 | 4 | 5 | 5 | 5 | 5 |
| row 3 (+C: w4 v5) | 0 | 1 | 1 | 4 | 5 | 6 | 6 | 9 |
| row 4 (+D: w5 v7) | 0 | 1 | 1 | 4 | 5 | 7 | 8 | **9** |

Every cell is the larger of two numbers, and both come from the row directly
above:

- **skip**: the cell straight above, same column.
- **take**: the cell above and w columns to the left, plus v. Only if c >= w.

**Row 0** is all zeros. With no items allowed, every bag carries nothing.

**Row 1** allows A (w=1, v=1). Column 0: A does not fit, copy 0 from above. Every
other column: skip gives 0, take gives row0[c-1] + 1 = 1. So the row is 0 then all
ones.

**Row 2** allows B (w=3, v=4). Columns 0, 1, 2: B does not fit, so copy from above:
0, 1, 1. Column 3: skip = row1[3] = 1; take = row1[0] + 4 = 4; max is 4. Column 4:
skip 1, take row1[1] + 4 = 5. Column 5, told in full:

> "I am answering the question for a bag of size 5, with items A and B allowed. If
> I skip B, the best is whatever A alone can do in a bag of 5: that is the cell
> straight above, row 1 column 5, which is 1. If I put B in, it uses 3 units, so 2
> units are left. What is the best I can do with 2 units using only the earlier
> items? That question was already answered: row 1, column 2, which is 1. I add
> B's value 4 and get 5. The larger of 1 and 5 is 5."

Here is that one cell as a picture, with the real numbers:

<svg viewBox="0 0 640 240" role="img" aria-label="row 1 and row 2 of the table for columns 0 to 7; the cell row 2 column 5 reads row 1 column 5 straight above for skip, value 1, and row 1 column 2, three columns to the left, for take, value 1 plus 4 equals 5">
  <g>
    <text x="141" y="40" text-anchor="middle">c=0</text>
    <text x="203" y="40" text-anchor="middle">1</text>
    <text x="265" y="40" text-anchor="middle">2</text>
    <text x="327" y="40" text-anchor="middle">3</text>
    <text x="389" y="40" text-anchor="middle">4</text>
    <text x="451" y="40" text-anchor="middle">5</text>
    <text x="513" y="40" text-anchor="middle">6</text>
    <text x="575" y="40" text-anchor="middle">7</text>
    <text x="10" y="75">row 1 (A)</text>
    <rect x="110" y="50" width="62" height="40"/>
    <text x="141" y="75" text-anchor="middle">0</text>
    <rect x="172" y="50" width="62" height="40"/>
    <text x="203" y="75" text-anchor="middle">1</text>
    <rect class="fill" x="234" y="50" width="62" height="40"/>
    <text x="265" y="75" text-anchor="middle">1</text>
    <rect x="296" y="50" width="62" height="40"/>
    <text x="327" y="75" text-anchor="middle">1</text>
    <rect x="358" y="50" width="62" height="40"/>
    <text x="389" y="75" text-anchor="middle">1</text>
    <rect class="fill" x="420" y="50" width="62" height="40"/>
    <text x="451" y="75" text-anchor="middle">1</text>
    <rect x="482" y="50" width="62" height="40"/>
    <text x="513" y="75" text-anchor="middle">1</text>
    <rect x="544" y="50" width="62" height="40"/>
    <text x="575" y="75" text-anchor="middle">1</text>
    <text x="10" y="185">row 2 (+B)</text>
    <rect x="110" y="160" width="62" height="40"/>
    <text x="141" y="185" text-anchor="middle">0</text>
    <rect x="172" y="160" width="62" height="40"/>
    <text x="203" y="185" text-anchor="middle">1</text>
    <rect x="234" y="160" width="62" height="40"/>
    <text x="265" y="185" text-anchor="middle">1</text>
    <rect x="296" y="160" width="62" height="40"/>
    <text x="327" y="185" text-anchor="middle">4</text>
    <rect x="358" y="160" width="62" height="40"/>
    <text x="389" y="185" text-anchor="middle">5</text>
    <rect class="fill" x="420" y="160" width="62" height="40"/>
    <text x="451" y="185" text-anchor="middle">5</text>
    <rect x="482" y="160" width="62" height="40" stroke-dasharray="4 4"/>
    <rect x="544" y="160" width="62" height="40" stroke-dasharray="4 4"/>
    <line x1="451" y1="90" x2="451" y2="160"/>
    <polyline points="445,152 451,160 457,152"/>
    <line x1="265" y1="90" x2="435" y2="160"/>
    <polyline points="424.8,161.2 435,160 428.6,152"/>
    <text x="460" y="128">skip B: row1[5] = 1</text>
    <text x="120" y="135">take B: row1[2] + 4 = 5</text>
    <text x="320" y="228" text-anchor="middle">row 2, c = 5: max(skip 1, take 5) = 5</text>
  </g>
</svg>

Skip means "look straight up, same column". Take means "look 3 columns to the
left in the row above, then add 4". It goes left by exactly the item's weight,
because that is how much room the item eats.

Columns 6 and 7 of row 2 work the same way: skip 1, take row1[3] + 4 = 5 and
row1[4] + 4 = 5. Both 5. With only A and B allowed you cannot do better than
A + B = 5, however large the bag.

**Row 3** allows C (w=4, v=5). Columns 0..3 copy row 2: 0, 1, 1, 4. Column 4: skip
5, take row2[0] + 5 = 5. A tie; the value is 5 either way. Column 5: skip 5, take
row2[1] + 5 = 6 (C plus A). Column 6: skip 5, take row2[2] + 5 = 6. Column 7: skip
5, take row2[3] + 5 = 4 + 5 = 9. That 9 is "C, plus the best 3-unit bag from A and
B", and the best 3-unit bag from A and B is B alone.

**Row 4** allows D (w=5, v=7). Columns 0..4 copy: 0, 1, 1, 4, 5. Column 5: skip 6,
take row3[0] + 7 = 7, so 7. Column 6: skip 6, take row3[1] + 7 = 8 (D plus A).
Column 7: skip 9, take row3[2] + 7 = 1 + 7 = 8. Skip wins: **9**.

That last cell is worth staring at. D has the best ratio of all four items, and it
fits. Taking it would give 8. The table says no, because the cell straight above
already holds a 9 that does not use D. The decision that greedy could not make is
made here by comparing two numbers.

### Getting the items back

The table holds values, not sets. To find the items, walk backward from the
corner and ask, at each row, "did this item change the answer?"

1. Cell (4, 7) = 9 and the cell above, (3, 7), is also 9. Item D did not change the
   answer, so D was skipped. Stay in column 7.
2. Cell (3, 7) = 9, the cell above (2, 7) = 5. C changed it, so C was taken. Move
   left by C's weight: column 7 - 4 = 3.
3. Cell (2, 3) = 4, the cell above (1, 3) = 1. B was taken. Column 3 - 3 = 0.
4. Cell (1, 0) = 0, above (0, 0) = 0. A was skipped.

Taken: B and C, value 9, weight 7. This walk needs the full table, because it
reads row i-1 while standing in row i. Hold on to that; it matters when we squeeze
the table to one row.

When the two cells are equal, the walk says "skip". Taking might have been equally
good (a tie, like row 3 column 4). Choosing skip on ties still produces a valid
optimal set, because "equal to the cell above" means an optimal set without this
item exists. If a problem wants a particular optimal set, such as the
lexicographically smallest, the tie rule is where you encode it.

### A second trace: the item that fits first is not in the answer

Now the counterexample from earlier, limit 10, items 1 (w=6, v=13), 2 (w=5, v=10),
3 (w=5, v=10).

| | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| row 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| row 1 (+1: w6 v13) | 0 | 0 | 0 | 0 | 0 | 0 | 13 | 13 | 13 | 13 | 13 |
| row 2 (+2: w5 v10) | 0 | 0 | 0 | 0 | 0 | 10 | 13 | 13 | 13 | 13 | 13 |
| row 3 (+3: w5 v10) | 0 | 0 | 0 | 0 | 0 | 10 | 13 | 13 | 13 | 13 | **20** |

Row 2, column 10: skip = 13 (item 1), take = row1[5] + 10 = 0 + 10 = 10. Skip
wins. With only items 1 and 2 allowed, the best is item 1 alone, as greedy said.

Row 2, column 5: skip = 0, take = row1[0] + 10 = 10. This cell holds 10, and the
10 is item 2 *without* item 1. Nobody had to decide to throw item 1 out. Column 5
simply never had room for it.

Row 3, column 10: skip = 13, take = row2[5] + 10 = 10 + 10 = 20. Take wins, and
it wins by reading the cell that does not contain item 1.

This is what the trace shows and the code hides: **the table never undoes a
decision**. It keeps, for every bag size, the best answer for that size, side by
side. The "skip item 1" world lives in column 5 the whole time, waiting. When item
3 arrives, it picks whichever world gives the best total. The greedy "take if it
fits" had only one world, the one where item 1 was already in.

Walk back: (3, 10) = 20 differs from (2, 10) = 13, take item 3, column 5. (2, 5) =
10 differs from (1, 5) = 0, take item 2, column 0. (1, 0) = 0 equals (0, 0),
skip item 1. Items 2 and 3, value 20.

## From the idea to the code

### The direct version: the full table

```python run
def knapsack_table(items, W):
    n = len(items)
    dp = [[0] * (W + 1) for _ in range(n + 1)]   # row 0: no items allowed
    for i in range(1, n + 1):                     # allow one more item
        w, v = items[i - 1]                       # item i is at index i-1
        for c in range(W + 1):                    # every bag size
            dp[i][c] = dp[i - 1][c]               # skip item i
            if w <= c:                            # take item i, if it fits
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)
    return dp

def chosen(dp, items, W):
    picked, c = [], W
    for i in range(len(items), 0, -1):            # walk back from the corner
        if dp[i][c] != dp[i - 1][c]:              # changed, so item i was taken
            picked.append(i)
            c -= items[i - 1][0]
    return picked[::-1], c

names = "ABCD"
items = [(1, 1), (3, 4), (4, 5), (5, 7)]
dp = knapsack_table(items, 7)
print("c ->        " + " ".join("%2d" % c for c in range(8)))
for i, row in enumerate(dp):
    label = "row 0 none " if i == 0 else "row %d +%s   " % (i, names[i - 1])
    print(label + " ".join("%2d" % x for x in row))
picked, left = chosen(dp, items, 7)
print("taken:", [names[i - 1] for i in picked], "value", dp[4][7], "unused", left)
assert dp[4][7] == 9 and [names[i - 1] for i in picked] == ["B", "C"]
assert dp[2][5] == max(dp[1][5], dp[1][2] + 4) == 5      # the cell told in words
assert sum(items[i - 1][1] for i in picked) == dp[4][7]

# second trace: the item that fits first is not in the answer
items2 = [(6, 13), (5, 10), (5, 10)]
dp2 = knapsack_table(items2, 10)
for i, row in enumerate(dp2):
    print("row %d" % i, row)
picked2, _ = chosen(dp2, items2, 10)
print("taken items:", picked2, "value", dp2[3][10])
assert dp2[3][10] == 20 and picked2 == [2, 3]
assert dp2[2][10] == 13            # with only the first two, skipping wins
assert dp2[2][5] == 10             # this cell does NOT contain item 1
```

### Each line, and which part of the recursion it is

| line | in plain words | in the recursion |
|---|---|---|
| `dp = [[0] * (W + 1) for _ in range(n + 1)]` | n+1 rows, W+1 columns, all zero | row 0 is the base case f(0, c) = 0 |
| `for i in range(1, n + 1)` | allow one more item each round | "solve smaller i first": row i-1 is complete before row i starts |
| `w, v = items[i - 1]` | fetch the i-th item | v_i and w_i |
| `for c in range(W + 1)` | answer the question for every bag size | every possible second argument |
| `dp[i][c] = dp[i - 1][c]` | assume we skip; always legal | the skip branch, f(i-1, c) |
| `if w <= c` | can item i fit in this bag at all | the guard on the take branch |
| `max(dp[i][c], dp[i - 1][c - w] + v)` | compare with taking | the take branch, v_i + f(i-1, c - w_i), and the max |
| `return dp` and read `dp[n][W]` | the corner | f(n, W) |

Three lines do the real work: the skip line, the guard, and the take line. The
rest is scaffolding.

### "The recursion subtracts from the limit. The loop does not. How is it the same?"

The subtraction is in both:

```
recursion:   v_i + f(i-1, c - w_i)
table:       v   + dp[i-1][c - w]
```

The difference is what c *is*. In the recursion, c is a running amount that
shrinks as you go deeper, like money in your pocket. In the table, c is not
running. It is a label on a column, the name of a question: "what if the bag were
size c?" dp[i][5] and dp[i][3] are two different, independent questions, and the
loop answers every one of them. Because the previous row already holds the answer
for *every* bag size, the recursive call f(i-1, c - w) turns into a lookup in
column c - w. Nothing needs to shrink; you just look somewhere else.

### 0-based items, 1-based rows

Python lists start at 0, and so does the input. The table rows do not, because row
0 has a job: it is "zero items allowed", the base case every other row is built
on. So row i means "the first i items are allowed", and the i-th item sits at
index i - 1 in the input. That is the whole reason for `items[i - 1]`.

You can avoid the shift by writing the table with row i meaning "items 0..i-1",
which is the same thing said differently. What you cannot avoid is the extra row.
Without it, row 1 would have nothing to read for its skip branch. If you ever see
`dp[i-1]` with i = 0, you have dropped row 0 and indexed row -1, which Python
silently allows; it reads the *last* row instead of raising an error.

### From two rows to one

Row i reads only row i-1. So keep one array dp of W+1 numbers. Before item i is
processed, it holds row i-1. We want to rewrite it, in place, so that afterwards
it holds row i.

The new dp[c] needs two old values: dp[c] itself (skip) and dp[c - w] (take). The
first is easy: you read dp[c] just before you overwrite it. The second is the
problem. c - w is to the **left** of c. So the whole question is:

> When I reach column c, has the cell w columns to my left already been
> overwritten this round?

If it has, it holds row i, not row i-1. Row i may already contain item i. Adding
item i on top of it puts item i in the bag twice.

Let us not argue about it in the abstract. Here is the array during one round, on
the main example. Before item C (w=4, v=5) it holds row 2:

| c | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| dp (= row 2) | 0 | 1 | 1 | 4 | 5 | 5 | 5 | 5 |

Go **right to left**. At c = 7 we read dp[3] = 4, which nobody has touched yet: it
is still row 2. New dp[7] = max(5, 4 + 5) = 9. At c = 6 we read dp[2] = 1, untouched:
dp[6] = 6. At c = 5, read dp[1] = 1: dp[5] = 6. At c = 4, read dp[0] = 0: dp[4] =
max(5, 5) = 5. Stop at c = w = 4, because smaller bags cannot hold C. The array is
now 0 1 1 4 5 6 6 9, which is exactly row 3.

Why did that work? Going right to left, every write happens at a column *to the
right* of every column we will still read. Writing at c can never spoil a read at
c - w, because c - w < c and we have not reached it yet. At any moment, the array
is two rows glued together: columns to the right of the cursor already hold the
new row, columns at and to the left of the cursor still hold the old row, and
the take branch only ever reads to the left.

### The subtle line, both ways

Now a case where the direction changes the answer. One item, w = 2, v = 5, limit
6, array starting at zeros. A `*` marks a cell already overwritten in this round.

**Right to left (correct).**

| step | reads | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|---|
| start | | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| c=6 | dp[4], old 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5* |
| c=5 | dp[3], old 0 | 0 | 0 | 0 | 0 | 0 | 5* | 5* |
| c=4 | dp[2], old 0 | 0 | 0 | 0 | 0 | 5* | 5* | 5* |
| c=3 | dp[1], old 0 | 0 | 0 | 0 | 5* | 5* | 5* | 5* |
| c=2 | dp[0], old 0 | 0 | 0 | 5* | 5* | 5* | 5* | 5* |

Every read lands on a cell without a star. Final: 0 0 5 5 5 5 5. One copy of the
item in any bag of size 2 or more. Correct.

**Left to right (wrong for 0/1).**

| step | reads | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|---|
| start | | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| c=2 | dp[0], old 0 | 0 | 0 | 5* | 0 | 0 | 0 | 0 |
| c=3 | dp[1], old 0 | 0 | 0 | 5* | 5* | 0 | 0 | 0 |
| c=4 | **dp[2], NEW 5** | 0 | 0 | 5* | 5* | 10* | 0 | 0 |
| c=5 | dp[3], NEW 5 | 0 | 0 | 5* | 5* | 10* | 10* | 0 |
| c=6 | dp[4], NEW 10 | 0 | 0 | 5* | 5* | 10* | 10* | 15* |

Look at the row c = 4. It reads dp[2], and dp[2] has a star: it was written two
steps ago and already contains the item. The new dp[4] = 5 + 5 = 10 means "the item,
plus a bag of 2 that already holds the item". That is the item twice. At c = 6 it
reads dp[4] = 10, the item twice, and adds it a third time: 15.

So the left-to-right loop does not compute garbage. It computes, exactly, the
best value when each item may be used **any number of times**. That is unbounded
knapsack, and the forward loop is its correct one-row implementation. The two
problems differ by one word in the statement and by the direction of one loop in
the code.

Read the rule a second way: in 0/1, the take branch must read the **previous**
row; in unbounded, it is allowed to read the **current** row, because after
taking one copy the item is still available. Right to left reads old values. Left
to right reads new ones. Choose the direction that reads the row you mean.

```python run
def show(dp, touched):
    return " ".join(("%2d*" if c in touched else "%2d ") % x for c, x in enumerate(dp))

def one_item(dp, w, v, order, trace=True):
    touched = set()
    for c in order:
        old = dp[c - w]
        state = "NEW" if (c - w) in touched else "old"
        dp[c] = max(dp[c], old + v)
        touched.add(c)
        if trace:
            print("  c=%d reads dp[%d] (%s %2d) -> %s" % (c, c - w, state, old, show(dp, touched)))
    return dp

W, w, v = 6, 2, 5
print("right to left, item w=2 v=5")
right = one_item([0] * (W + 1), w, v, range(W, w - 1, -1))
print("left to right, item w=2 v=5")
left = one_item([0] * (W + 1), w, v, range(w, W + 1))
assert right == [0, 0, 5, 5, 5, 5, 5]          # one copy, at most
assert left == [0, 0, 5, 5, 10, 10, 15]        # c // 2 copies: unbounded

# the same loops over several items, against the 2-D rows and the unbounded answer
items, W = [(1, 1), (3, 4), (4, 5), (5, 7)], 7
down, up = [0] * (W + 1), [0] * (W + 1)
for w, v in items:
    one_item(down, w, v, range(W, w - 1, -1), trace=False)
    one_item(up, w, v, range(w, W + 1), trace=False)
unbounded = [0] * (W + 1)
for c in range(W + 1):                          # any item, any number of times
    for w, v in items:
        if w <= c:
            unbounded[c] = max(unbounded[c], unbounded[c - w] + v)
print("right to left:", down)
print("left to right:", up, "= unbounded", unbounded)
assert down == [0, 1, 1, 4, 5, 7, 8, 9]         # row 4 of the 2-D table
assert up == unbounded and up[2] == 2           # A used twice in a bag of 2
assert down[7] == up[7] == 9                    # the corner hides the bug here
```

Look at the last two lines of output. On the four-item example the wrong loop
gives the *right* corner, 9. It is wrong at column 2 (value 2, which is A twice),
but if the test only asks for dp[7], it passes. The bug only shows when some
item can fit twice, that is, when 2w <= W, and the doubled item actually beats
the honest answer. Sample tests often miss that. This is why you must understand
the direction rather than test it.

The one-row version, then, is:

```python
def knapsack(items, W):
    dp = [0] * (W + 1)                  # row 0
    for w, v in items:                  # each item becomes the next row
        for c in range(W, w - 1, -1):   # right to left: reads stay in the old row
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[W]
```

Two details. The inner loop stops at w, not 0: for c < w the item does not fit, so
the new row equals the old row there, and leaving those cells alone is the
"copy from above". And the one-row version cannot reconstruct the items: the old
rows are gone, and the walk needs them. If you need the set, keep the 2-D table,
or keep a 2-D table of booleans `took[i][c]` alongside the one row, which costs n
x W bits rather than n x W integers.

### Memo or table?

Both are the same recurrence. Prefer the table (and the one-row form) when W is
moderate and you will visit most columns anyway. Prefer the memo when only a few
(i, c) pairs are reachable, for example when the weights are large and sparse, so
most columns would never be asked about. In Python, the memo recurses n levels
deep, so with n = 200 it is fine, and with n = 5,000 you would need to raise the
recursion limit or switch to the table.

## Why it is correct

:::proof The table holds the true optimum
**What we claim.** For every i from 0 to n and every c from 0 to W, dp[i][c]
equals OPT(i, c), defined as the largest total value of a set S of items chosen
from {1, ..., i} whose total weight is at most c. (The empty set always qualifies,
with value 0, so OPT is well defined.)

**Base case, i = 0.** The only set of items chosen from the empty collection is
the empty set. Its value is 0, so OPT(0, c) = 0. The code sets row 0 to zeros.
They agree.

**Inductive step.** Assume row i-1 is correct: dp[i-1][c'] = OPT(i-1, c') for every
c'. Fix a column c. Split all the legal sets for (i, c) into two groups that do not
overlap and together cover everything:

1. Sets that do **not** contain item i. These are exactly the legal sets for
   (i-1, c). The best of them is OPT(i-1, c), which is dp[i-1][c] by assumption.
   That is the skip value.
2. Sets that **do** contain item i. These exist only if w_i <= c. Remove item i
   from such a set and what remains is a set from {1..i-1} with weight at most
   c - w_i. Conversely, add item i to any such set and you get a legal set of this
   group. So the group's best value is v_i + OPT(i-1, c - w_i), which is
   v_i + dp[i-1][c - w_i]. That is the take value.

The best legal set is in one group or the other, so OPT(i, c) is the larger of the
two group bests (or just the first, when item i does not fit). That is exactly
what the code writes into dp[i][c]. So row i is correct.

**Two directions, said plainly.** The value is never too high: every number the
code produces is the value of a real legal set (the one you would get by following
its choices back). And it is never too low: the optimal set lies in group 1 or
group 2, and that group's value is one of the two numbers compared. Too high is
impossible and too low is impossible, so it is exact.

**Why "the rest must be optimal" is safe.** In group 2, could it pay to combine
item i with a *non-best* set for (i-1, c - w_i)? No: if a better set fitted in
c - w_i, swapping it in would give a better set for (i, c) that still contains item
i. So the best of group 2 always uses the best remainder.

**Termination.** The table is finite, (n+1)(W+1) cells, each computed once with
two reads.

**The one-row version.** Claim: when the descending loop reaches column c while
processing item i, the cells dp[0..c] still hold row i-1. True at the start of the
round (the whole array is row i-1). Each step writes only at the current c and
then moves to c-1, so cells at indices below the cursor have not been written this
round. The take branch reads index c - w <= c, which is below or at the cursor
(at, only if w = 0, and then it reads dp[c] before writing it). So every read sees
row i-1, the step computes exactly the 2-D formula, and when the round ends, the
array is row i. ∎
:::

The proof quietly used these assumptions. Each one is a place a variant can break
the method.

- **The items interact only through the shared limit.** Item i's value does not
  depend on which other items are in the bag. If it does (a bonus for taking two
  together, a penalty for a pair), the split into two groups no longer gives
  "v_i plus the best of the rest", and the state must grow.
- **Weights are non-negative integers.** They are column offsets. A fractional
  weight has no column; a negative weight points to the right, and the
  right-to-left argument fails.
- **The objective adds up and we take the max (or min).** Group 2's best is
  v_i + (best of the rest) because adding v_i preserves which remainder is best.
  For counting, max becomes +, and then the two groups must not overlap, which is
  why the "skip or take" split being disjoint matters there.
- **Order of items does not matter.** We processed items 1..n in input order, but
  any order gives the same OPT, because a set is a set. When the problem secretly
  depends on order (deadlines), you must fix the right order first (variation L).
- **"At most c" with every row starting from the empty set.** Row 0 is all zeros
  because the empty set fits every bag. For "exactly c" that is false, and the
  base row changes (variation B).

## What it costs

**Time.** There are (n+1) x (W+1) states. Each does constant work: one read
straight up, one read to the left, one compare. So the time is O(n·W). For
the bank's [[p:amazon-zero-one-knapsack|0/1 Knapsack]] constraints, n = 200 and
W = 10,000, that is about 2·10^6 cells. In Python, a few million simple steps
is comfortable.

**Space.** The full table is (n+1)(W+1) numbers: 2·10^6 integers for those
limits, which is fine. The one-row version uses W+1 numbers, O(W), and loses
reconstruction. The memo version uses one dictionary entry per *reached* state,
which is at most the same count but can be far fewer, at a higher cost per entry
(hashing a tuple and a dictionary slot are much heavier than a list cell).

**The brute force for comparison.** 2^n subsets, each summed in O(n) if done
naively, or 2^(n+1) - 1 recursive calls. Doubling with every item.

**The trap: pseudo-polynomial.** O(n·W) looks polynomial, but W is a number, not a
count of things in the input. Writing W takes about log2(W) bits. If W doubles,
the input grows by one bit and the work doubles. So the running time is
exponential in the size of the input, and that is consistent with knapsack being
NP-hard: nobody knows a method polynomial in n and log W. "Pseudo-polynomial"
means "polynomial in the numeric value", and the practical meaning is simple:
**the table is only as cheap as W is small.**

That is why constraints are the first thing to read. With W <= 10^4 or 10^5 and n
in the hundreds, the table is the intended solution. With W = 10^9, it is not:
10^9 columns of anything will not fit. Then one of these must be true, and the
constraints tell you which:

- the values are small, so index by value instead (variation F);
- n is at most about 40, so split in halves ([[meet-in-the-middle]], variation G);
- the weights or values have structure that makes a greedy exact (unit weights,
  powers of two).

**The forgotten costs.**

- The bitset version of subset sum (variation A) does the same O(n·W) work, but
  many columns per machine operation, because Python's big-integer shift and or
  run in C. It is the standard way to make feasibility fast in Python.
- Reconstruction is O(n) after the table, but the table itself is the price. If
  memory is tight, store one bit per cell for "took it".

## How to think about it

The template is short. What makes knapsack hard is recognising which knapsack
you are in. Ask these questions, in this order, every time.

1. **What are the items? What is one decision?** Usually "take this element or
   not". Sometimes an item is a group, a component, a string, a project.
2. **What is the shared resource?** Capacity, budget, time, a target sum, a count
   of picks, the number of ones and zeros you may use. This becomes the column.
3. **What am I computing?** Max value, min cost, number of ways, or just yes/no.
   This decides the operation in the cell (max, min, +, or) and the start values.
4. **"At most" or "exactly"?** At most: start every column at 0. Exactly: start
   column 0 at 0 and every other column at "impossible".
5. **How many copies of each item?** Once (right to left), unlimited (left to
   right), or k copies (binary splitting, variation E).
6. **Does order matter?** For counting: are [1, 2] and [2, 1] the same answer or
   two answers? For optimisation: does the constraint depend on the order you take
   things in (deadlines)? If so, sort by an exchange argument first.
7. **Which quantity is small?** n, W, the values, the sum of the weights? The small
   one becomes the index. The large one must never be an index. This single
   question is what separates knowing knapsack from knowing a template.
8. **Any extra constraint?** A second resource (another dimension), "exactly k
   items" (another dimension), one item per group (a loop order), dependencies (a
   tree).

Then, before writing any code, write four lines: **the state in words**, **the
transition and why its cases are complete and do not overlap**, **the start
values**, and **the answer cell**. If you cannot write those four lines, you do
not have the solution yet, and code will not find it for you.

### Telling it from its neighbours

- **Unbounded knapsack and coin change** ([[unbounded-knapsack]]). The same table
  with unlimited copies. The tell is "any number of times", "unlimited supply",
  "denominations". The loop goes left to right.
- **Counting DP** ([[counting-dp]]). When the cell sums instead of maximising, the
  split into cases must be disjoint, and loop order decides whether order of
  choices is counted (variation D).
- **Grid and two-index DP** ([[dp-2d]]). The knapsack table is a 2-D DP whose
  second index happens to be a resource. If the second index is a position in a
  second string, you are in [[dp-strings]] instead.
- **Greedy** ([[greedy]]). If you can prove a single rule is always safe
  ([[greedy-exchange]]), you do not need the table.
- **Backtracking** ([[backtracking]]). When the problem wants *every* subset that
  works, DP can count them or find one, but listing needs a search.
  [[p:pinterest-combination-sum-with-single-use|Combination Sum with Single-Use Values]]
  is subset sum that asks for all combinations, so it is backtracking.
- **Interval or partition DP** ([[partition-dp]]). "Partition into two sets" is
  knapsack. "Partition the array into contiguous pieces" is not; the pieces keep
  their order, and the state is a cut position.

## Variations

Fourteen variations, from the everyday to the rare. Each says what changes, why,
a three-line example you can check, and a problem from this bank that teaches it.
A to E and M are common in interviews and assessments. F, G, H, I, J are regular.
K and L are less common. N is rare outside competitive programming.

### A. Subset sum: can I hit the target exactly?

**What changes.** No values, only weights. The cell is a boolean: can some subset
of the first i numbers sum to exactly s? The take line becomes
`dp[s] = dp[s] or dp[s - x]`, the loop still goes right to left, and dp[0] = True
while every other start is False (exactly, not at most).

**Why.** "Is there a set" is "is the best value at least 0, among sets that hit
exactly s", and or-ing is the max of booleans.

**Speed-up.** Store the whole row as the bits of one integer: bit s is set when sum
s is reachable. Taking x shifts every reachable sum up by x, so one item is
`bits |= bits << x`. That is skip (keep bits) or take (shifted bits) for all
columns at once, and it does not need a loop direction at all, because the shift
reads the whole old row before the or writes.

**Example.** nums = [3, 34, 4, 12, 5, 2], target 9: true, 4 + 5. Target 30: false
(everything except 34 sums to 26). Note that the target is a sum, not a count.

**Bank.** [[p:confluent-positive-subset-sum|Positive Subset Sum]] (targets up to
20,000; the follow-up asks you to return the subset, which is the walk back from
the 2-D version), and [[p:apple-subset-sum-possible|Subset Sum Possible]].

### B. Exactly c versus at most c

**What changes.** Only the first row. "At most c": every column starts at 0,
because the empty bag fits every size. "Exactly c": column 0 starts at 0 and every
other column starts at -infinity for a max problem (or +infinity for a min problem),
meaning "no set has this weight yet". Every take must skip impossible sources.

**Why.** The meaning of a cell changes from "weight at most c" to "weight exactly
c", and the only set of weight exactly 0 at the start is the empty set. If you
start with zeros, a cell for c = 4 can claim value 5 while really holding a set of
weight 3.

**Example.** One item (w=3, v=5), W = 4. At most 4: answer 5. Exactly 4: impossible.
The zero-initialised "exactly" code returns 5 (see the Traps block).

**Bank.** [[p:oracle-coin-change-unbounded-and-single-use|Minimum Coins with Reusable or Single-Use Entries]]
asks for the fewest coins that make *exactly* the amount, with -1 when impossible,
so it starts at +infinity everywhere except 0. Its mode 1 is 0/1, its mode 0 is
unbounded, and the only difference in code is the loop direction.

### C. Unbounded: each item any number of times

**What changes.** The inner loop runs left to right. In 2-D terms, the take branch
reads dp[i][c - w] (the same row) instead of dp[i-1][c - w].

**Why.** After taking one copy of item i, item i is still available, so the
remaining problem is "items 1..i, room c - w", which is the current row. Left to
right reads current-row values. This is the "wrong" loop from earlier, now right.

**Example.** One item (w=2, v=5), W = 6: 15 (three copies). Coins [1, 2, 5],
amount 11, fewest coins: 3 (5 + 5 + 1).

**Bank.** [[p:bloomberg-coin-change|Coin Change]] (fewest coins, unlimited supply)
and mode 0 of [[p:oracle-coin-change-unbounded-and-single-use|Minimum Coins with Reusable or Single-Use Entries]].
The full treatment is [[unbounded-knapsack]].

### D. Counting ways: combinations versus orders

**What changes.** The cell holds a count, the max becomes a sum, and dp[0] = 1 (one
way to make 0: take nothing). For 0/1 counting, right to left as usual. For
unlimited coins, a new question appears: does [1, 2] count as different from
[2, 1]?

- **Coins outside, amount inside**: counts **combinations** (multisets).
- **Amount outside, coins inside**: counts **ordered sequences**.

**Why.** With coins outside, coin 1 is fully processed before coin 2 is ever
considered. So every way is built as "some 1s, then some 2s", in one fixed order,
and each multiset is built exactly once. With amount outside, dp[a] sums over
"which coin is the *last* one placed", for every coin, so [1, 2] (last coin 2) and
[2, 1] (last coin 1) are separate cases, and each ordering is counted. Neither
loop is wrong. They answer different questions, and the statement tells you
which.

**Example.** Coins [1, 2], amount 4. Combinations: {1,1,1,1}, {1,1,2}, {2,2} = 3.
Ordered: 1111, 112, 121, 211, 22 = 5.

```python run
from itertools import product

def combinations_count(coins, amount):
    ways = [1] + [0] * amount            # one way to make 0: take nothing
    for coin in coins:                   # coins OUTSIDE
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]
        print("  after coin %d: %s" % (coin, ways))
    return ways[amount]

def sequences_count(coins, amount):
    ways = [1] + [0] * amount
    for a in range(1, amount + 1):       # amount OUTSIDE
        for coin in coins:
            if coin <= a:
                ways[a] += ways[a - coin]   # coin is the LAST one placed
    print("  by amount:     %s" % ways)
    return ways[amount]

def enumerate_all(coins, amount):        # the truth, by listing sequences
    seqs = set()
    for k in range(amount + 1):
        for s in product(coins, repeat=k):
            if sum(s) == amount:
                seqs.add(s)
    return len({tuple(sorted(s)) for s in seqs}), len(seqs), sorted(seqs)

coins, amount = [1, 2], 4
print("coins outside (combinations)")
comb = combinations_count(coins, amount)
print("amount outside (ordered sequences)")
seq = sequences_count(coins, amount)
multisets, orders, listing = enumerate_all(coins, amount)
print("combinations", comb, "sequences", seq)
print("all sequences:", listing)
assert (comb, seq) == (multisets, orders) == (3, 5)

for coins, amount in [([1, 3], 4), ([2, 3, 5], 9), ([1, 2, 3], 6)]:
    m, o, _ = enumerate_all(coins, amount)
    assert combinations_count(coins, amount) == m
    assert sequences_count(coins, amount) == o
print("both loop orders match enumeration on three more inputs")
```

Trace the first table by hand. After coin 1: every amount has exactly one way, all
ones. After coin 2: ways[2] = 1 + ways[0] = 2 ({1,1}, {2}); ways[3] = 1 + ways[1] =
2; ways[4] = 1 + ways[2] = 3. Now the second: ways[3] = ways[2] + ways[1] = 2 + 1
= 3 (sequences ending in 1, plus sequences ending in 2), and ways[4] = ways[3] +
ways[2] = 3 + 2 = 5. That second recurrence is Fibonacci, and it should be:
ordered sums of 1s and 2s are the staircase problem.

**Bank.** Combinations: [[p:worldquant-count-unordered-coin-combinations|Count Unordered Coin Combinations]]
and [[p:bloomberg-coin-change-ii|Coin Change II]]. Orders:
[[p:pinterest-count-ordered-combination-sums|Count Ordered Combination Sums]],
whose statement says outright that different orders count separately. 0/1
counting (each element once): [[p:adobe-count-subsets-with-sum-k|Count Subsets with Sum K]],
where zeros in the input are the trap (see Traps).

### E. Bounded: item i available k_i times

**What changes.** Each item type has a count. The naive fix is to copy item i k_i
times and run 0/1, which costs O(W · sum of k_i). The standard fix is **binary
splitting**: replace k copies by bundles of 1, 2, 4, ..., and a remainder, each
bundle a single 0/1 item with its weight and value multiplied. Any count from 0 to k
is a sum of a subset of the bundles, and no subset of bundles exceeds k. So the
0/1 knapsack over bundles is the bounded knapsack, at O(W · sum of log k_i).

**Why.** 0/1 knapsack chooses subsets. Binary splitting turns "choose a count from
0 to k" into "choose a subset of about log k bundles", which 0/1 already does. (An
O(n·W) method with a monotonic deque per residue of c mod w exists; interviews
rarely need it.)

**Example.** k = 13 splits into 1, 2, 4, 6 (1+2+4 = 7, remainder 6). Then 5 = 1 + 4,
10 = 4 + 6, 13 = 1 + 2 + 4 + 6. Item (w=2, v=3) with 3 copies and W = 5: bundles
(2, 3) and (4, 6); the best is the bundle of two copies, value 6.

**Bank.** [[p:google-unit-weight-knapsack|Unit-Weight Knapsack with Limited Quantities]]
is bounded knapsack, and it is in this list because the table is the *wrong*
answer there: every unit weighs 1, the capacity is up to 10^9, and the optimum is
"sort by value, take the most valuable units first". Bounded knapsack with real
weights does not appear in this bank; when it does elsewhere, binary splitting is
the move.

### F. Swap the index: weights huge, values small

**What changes.** The roles of weight and value trade places. Index by value:
`least[val]` = the smallest total weight of a set with value exactly val. Start
least[0] = 0 and the rest at infinity; the take line is
`least[val] = min(least[val], least[val - v] + w)`, right to left over val. The
answer is the largest val with least[val] <= W.

**Why.** The table needs a small index. If W is 10^9 but n·max(v) is 10^5, the value
axis is small and the weight axis is not. This is checklist question 7 in action:
the state is still "which items are allowed, and something about the resource", but
the something becomes "value collected", with weight as the thing minimised.

**Example.** Items with weights 10^8, 6·10^7, 5·10^7, 3·10^7 and values 7, 4, 5, 3,
W = 10^8. The value axis has only 20 columns. The answer is 8 (the items of weight
5·10^7 and 3·10^7). The variations block below checks this against enumeration.

**Bank.** No problem in this bank needs the swap; it is here because interviews
elsewhere use it, typically as a follow-up: "what if the weights were up to 10^9?"

### G. Meet in the middle: n about 40, everything huge

**What changes.** No table at all. Split the items into two halves of about 20.
List all 2^20 (about a million) subset sums of each half. Sort one list. For every
sum s in the other, find the largest partner <= W - s by binary search or two
pointers.

**Why.** 2^40 is too many, but 2 · 2^20 is fine, and a pair of half-subsets is
exactly a subset. The limit can be 10^9 because it is never an index.

**Example.** Plates [5, 8, 13, 21], limit 30. Halves [5, 8] give sums {0, 5, 8, 13};
[13, 21] give {0, 13, 21, 34}. Best pair under 30: 8 + 21 = 29.

**Bank.** [[p:salesforce-weight-capacity|Maximum Barbell Weight]] (42 plates,
capacity 10^9) and [[p:dream11-subset-sum-target|Subset Sum to Target]] (30
signed numbers up to 10^9; negative values also rule out the table). The technique
has its own chapter, [[meet-in-the-middle]].

### H. Groups: at most (or exactly) one item from each group

**What changes.** Items come in groups and you may take one per group. Loop over
groups; inside, over capacity right to left; inside that, over the items of the
group: `dp[c] = max(dp[c], dp[c - w_j] + v_j)` for each j in the group.

**Why.** The capacity loop sits outside the item loop so that, for one capacity c,
all the options from this group read the *same* old row. If the item loop were
outside, the second item of a group would read a row already updated by the first,
and you could take two items from one group. "Exactly one per group" changes the
start: build a fresh row per group from the old row only, with no skip option,
and use -infinity (or 0 ways) for impossible.

**Example.** Two dice with faces 1..3, ordered outcomes summing to 4: group 1 is die 1,
group 2 is die 2, each group must contribute exactly one face. Outcomes (1,3),
(2,2), (3,1): 3 ways.

**Bank.** [[p:bloomberg-number-of-dice-rolls-with-target-sum|Number of Dice Rolls With Target Sum]]:
each die is a group, each face an item of weight equal to the face, exactly one
per group, counting modulo 10^9 + 7.

### I. Two or more resources

**What changes.** Each item consumes two (or three) resources, so the state becomes
dp[a][b] with one axis per resource. Both loops go right to left for 0/1.

**Why.** The future now needs to know how much of *each* resource is left; one
number cannot hold two independent limits. This is the unlocking question again,
answered with two numbers instead of one.

**Example.** Strings ["10", "0001", "111001", "1", "0"] with at most 5 zeros and 3
ones: take "10", "0001", "1", "0" (5 zeros, 3 ones), 4 strings. The value of
each item is 1.

**Bank.** [[p:amazon-binary-strings-bounded-subset|Largest Binary-String Subset Within Bit Budgets]]
(two budgets, value 1 per string) and [[p:morgan-stanley-three-resource-knapsack|Three-Resource 0/1 Knapsack]]
(three capacities of at most 40, so 41^3 states per item). A close relative is
[[p:apple-two-bag-knapsack|Maximum Weight in Two Bags]]: each item goes into bag 1,
bag 2, or neither, and the state is (room left in bag 1, room left in bag 2), with
three branches per item instead of two.

### J. Exactly k items (or at most k)

**What changes.** Add the number of items taken to the state: dp[j][s] = can (or how
many ways, or best value) j chosen items reach s. Taking an item moves from j-1 to
j. Loop j downward as well as s, for the same reason as always: read the
previous item's values.

**Why.** "How many items so far" is something the future needs to know when the
count is constrained, so it joins the state.

**Example.** nums [1, 2, 3, 4], k = 2, target 5: yes (1 + 4 or 2 + 3). k = 3, target 5:
no, since the three smallest already sum to 6.

**Bank.** [[p:jpmorgan-exact-k-subset|Find a Subset of Exactly K Elements with a Target Sum]]
(signed values, n <= 20, so a dictionary of reachable (j, s) pairs or plain
enumeration both work). [[p:pinterest-fixed-length-combination-sum|Fixed-Length Combination Sum]]
is the same shape but asks to list every combination, so it is backtracking.

### K. Tree knapsack: taking a node requires its parent

**What changes.** Items form a tree, and an item can be taken only if its parent is.
dp[v][c] = best value inside v's subtree using budget c, *given that v is taken*.
Merge children one at a time like knapsack: for each child, combine the current
table with the child's table, choosing how much budget the child's subtree gets.

**Why.** Once you know v is taken, its children's subtrees are independent of each
other except for the shared budget. That is knapsack again, with each child's
whole subtree acting as an item that can be "bought" at many different sizes.
Bounding each merge by the subtree sizes makes the total O(n·W) instead of
O(n·W^2).

**Example.** Root (cost 1, value 1) with children a (cost 2, value 5) and b (cost 2,
value 3), budget 3: root + a = 6. b alone is not allowed without the root.

**Bank.** [[p:google-tree-dependent-knapsack|Tree-Dependent Knapsack]] (200 nodes,
budget 2,000). The tree side is covered in [[tree-dp]].

### L. Sort first, then knapsack

**What changes.** When feasibility depends on the *order* in which chosen items
are done (each job must finish by its deadline), first sort by an exchange
argument (usually by deadline), then run knapsack in that order with "time used so
far" as the resource, and allow taking job i only if time + its duration <= its
deadline.

**Why.** Knapsack treats a choice as a set. A set of jobs is feasible exactly when
it is feasible in deadline order (swapping two adjacent out-of-order jobs never
hurts), so once the order is fixed, the set view is valid again.

**Example.** Unit jobs (deadline, profit): (1, 5), (1, 4), (2, 3). Sorted by
deadline, dp over slots used: take (1, 5) in slot 1, (2, 3) in slot 2, profit 8.
(1, 4) would need slot 1 too.

**Bank.** [[p:jpmorgan-job-scheduling|Unit Jobs with Deadlines and Profits]] is
the unit-duration case. Because every job takes one slot, a greedy (highest profit
first, latest free slot) also solves it, and with 1,000 jobs and deadlines up to
10,000 either works; the knapsack view is the one that survives when durations
differ.

### M. Disguised knapsack

Many statements never say "weight" or "value". The algebra that unmasks them is
the skill, and "Recognising it in a statement" works through it. The common ones:

- **Equal partition**: subset sum with target S/2, impossible when S is odd. Bank:
  [[p:expedia-partition-equal-subset-sum|Partition into Equal-Sum Subsets]].
- **Minimum difference**: the largest reachable sum s <= S/2 gives S - 2s. For
  [2, 7, 4, 1, 8, 1], S = 23, s = 11, difference 1. Bank:
  [[p:intuit-minimum-subset-sum-difference|Minimum Subset Sum Difference]].
- **Signs**: + or - before each number to reach T is counting subsets with sum
  (S + T)/2. No problem in this bank asks it directly; interviews elsewhere do.
- **Budgets.** Projects with costs and returns, tasks with time and reward, ad
  impressions with floor prices: 0/1 knapsack with new nouns. Bank:
  [[p:salesforce-budget-project-selection|Budget-Constrained Project Selection]],
  [[p:google-task-reward-under-time-budget|Maximum Task Reward Within a Time Budget]],
  [[p:inmobi-maximize-impression-value|Maximize Impression Value]].
- **Items you have to build first.** In
  [[p:intuit-friends-and-candies|Friends and Candies]] a whole friend group must be
  served or skipped together. Find the groups ([[union-find]]), then each group is
  one item with weight = its total demand and value = its size, and it is plain 0/1.

The variations block checks the bitset, the sign algebra, the minimum
difference, and the value-indexed swap from F:

```python run
from itertools import product, combinations

def reachable(nums):                     # subset sum as one big integer
    bits = 1                             # bit s set <=> sum s reachable
    for x in nums:
        bits |= bits << x                # skip (bits) or take (shifted)
    return bits

def count_subsets(nums, t):              # 0/1 counting, right to left
    ways = [1] + [0] * t
    for x in nums:
        for s in range(t, x - 1, -1):
            ways[s] += ways[s - x]
    return ways[t]

def target_sum(nums, T):                 # +/- signs: P - N = T, P + N = S
    S = sum(nums)
    if abs(T) > S or (S + T) % 2:
        return 0
    return count_subsets(nums, (S + T) // 2)

def min_difference(nums):                # partition: best subset sum <= S/2
    S, bits = sum(nums), reachable(nums)
    best = max(s for s in range(S // 2 + 1) if bits >> s & 1)
    return S - 2 * best

def by_value(items, W):                  # index by value when values are small
    INF = float("inf")
    V = sum(v for _, v in items)
    least = [0] + [INF] * V              # least[val] = min weight for value val
    for w, v in items:
        for val in range(V, v - 1, -1):
            least[val] = min(least[val], least[val - v] + w)
    return max(val for val in range(V + 1) if least[val] <= W)

nums = [3, 34, 4, 12, 5, 2]
bits = reachable(nums)
print("sum 9 reachable:", bool(bits >> 9 & 1), " sum 30 reachable:", bool(bits >> 30 & 1))
assert bits >> 9 & 1 and not bits >> 30 & 1

ones = [1, 1, 1, 1, 1]
signs = sum(1 for s in product([1, -1], repeat=5) if sum(a * b for a, b in zip(s, ones)) == 3)
print("ways to sign [1,1,1,1,1] to 3:", target_sum(ones, 3), "(enumerated:", signs, ")")
assert target_sum(ones, 3) == signs == 5 and target_sum(ones, 2) == 0

stones = [2, 7, 4, 1, 8, 1]
print("min partition difference of", stones, "=", min_difference(stones))
assert min_difference(stones) == 1

items = [(10**8, 7), (6 * 10**7, 4), (5 * 10**7, 5), (3 * 10**7, 3)]
best = max(sum(v for _, v in s) for k in range(5) for s in combinations(items, k)
           if sum(w for w, _ in s) <= 10**8)
print("weights near 1e8, values tiny: by_value ->", by_value(items, 10**8))
assert by_value(items, 10**8) == best == 8      # 5e7 + 3e7, values 5 + 3
```

### N. The advanced tools (rare)

These come up in competitive programming and in the occasional hard interview
follow-up. Know that they exist.

- **Top k subset sums.** With n = 40 and weights up to 10^9, the k largest subset
  sums come from a heap: start from the total, and generate "remove one more of
  the smallest items" moves in a canonical order so each subset is produced once.
  Bank: [[p:google-top-k-nonnegative-subset-sums|Top K Subset Sums of Nonnegative Weights]].
  Example: weights [1, 2, 3], k = 3: 6, 5, 4.
- **Few distinct weights.** Weights summing to S include at most about sqrt(2S)
  distinct values, so a bounded knapsack over distinct weights beats one over items.
- **Removing an item from a counting knapsack.** The counting row is the product of
  (1 + x^w) factors; dividing one out (a forward loop `ways[s] -= ways[s - w]`)
  removes that item in O(W).
- **Offline add and remove** by divide and conquer over time, and **max-plus
  convolution** for merging two rows, are the competitive-programming end.

## Recognising it in a statement

From most reliable to least:

1. **"Each item can be used at most once" plus a limit plus "maximise"**. This is
   the textbook 0/1. "Each array position may be selected at most once, equal values
   at different positions are separate choices" is the same sentence in careful
   wording, and several bank problems use exactly that.
2. **"Choose a subset whose sum is exactly / at most T"**, with T up to about 10^5.
   Subset sum.
3. **Two groups, every element in one of them, sums equal or close**. Partition,
   which is subset sum to S/2.
4. **"Budget", "capacity", "time limit", "points"**, with items that each cost
   something and give something, and no rule linking items to each other.
5. **Constraints with a small numeric total**: values or weights up to 10^4 and
   n up to a few hundred. A small *sum* is the strongest structural hint, because
   it is exactly the axis a table needs.
6. **Two limits on the same items** ("at most m zeros and n ones"). Multi-resource.
7. **"Number of ways to make the amount"**. Counting; read the statement for
   whether order matters.

### The disguises, with the algebra

**+/- signs to reach T.** "Assign + or - to each number so the expression equals
T." Let P be the sum of the numbers with +, N the sum with -. Then P - N = T, and
every number is in one of the two, so P + N = S. Add the two equations: 2P = S + T,
so P = (S + T)/2. The problem is now: count subsets with sum (S + T)/2. If S + T is
odd or |T| > S, the answer is 0. The signs vanished; what is left is choosing
which numbers get a plus.

**Split into two teams as evenly as possible.** If one team has sum s, the other has
S - s, and the difference is |S - 2s|. Minimising it is maximising s subject to
s <= S/2. That is "the largest reachable subset sum not above S/2": subset sum,
then a scan.

**Smash stones together; what is the smallest stone left?** Every sequence of
smashes ends with a signed sum of the original stones, and every split into two
signed groups can be produced, so it is the minimum difference above. The bank's
[[p:factset-last-stone-weight|Last Stone Weight]] is the *other* problem, the one
that always smashes the two heaviest; that one is a [[heap]] simulation, not
knapsack. The titles are similar and the techniques are not.

**"All or nothing" groups.** When people, files or tasks must be taken together
(friends, dependencies with no tree structure), merge each group into one item
first.

### Anti-signals: looks like knapsack, is not

The early section "When it is the wrong tool" has the reasons; here are the tells.

- **"Contiguous", "subarray", "window"**: an interval, not a subset.
  [[prefix-sums]] or [[sliding-window]].
- **All items weigh the same, or are worth the same**: sort and take a prefix.
- **Powers of two**: in [[p:jpmorgan-minimum-servers-for-exact-load|Minimum Servers for an Exact Load]]
  every capacity is a power of two and the load is up to 10^9. The binary digits of
  the load decide the answer; a table of 10^9 columns is neither possible nor needed.
- **A limit up to 10^9 and nothing small**: not the table. Look for n <= 40 or a
  greedy.
- **n <= 20 and a complicated scoring rule**: enumerate all 2^n subsets.
  [[p:palantir-optimize-discount-selection|Optimize Discount Selection Under a Point Budget]]
  has at most 20 discounts with stacking, caps and rounding, far easier to score
  subset by subset (about a million) than to fit into a knapsack cell.
- **"Return all subsets"**: backtracking.

## Traps

**1. Loop direction.** Symptom: answers that are too large, only on inputs where
some item fits twice. Left to right is unbounded. Right to left is 0/1. The
demonstration is in "From the idea to the code"; the habit is to say, out loud,
"the take reads the old row, so right to left".

**2. Exactly versus at most.** Symptom: the code returns a value for a target that
cannot be hit exactly, or "minimum coins" returns 0 for an impossible amount.
Start only column 0 at the neutral value; everything else is "impossible".

**3. Building on an impossible state.** Symptom: an impossible cell comes back to
life. With fixed-width integers, -INF + v can overflow and win every max; with a
finite sentinel such as 10^9, sentinel + 1 is no longer equal to the sentinel and
gets reported as an answer. Guard with `if dp[c - w] != NEG`.

**4. The same loop for 0/1 and unbounded coin problems.** Symptom: "fewest coins,
each coin once" returns a count that reuses a coin. This is trap 1 in min-form, and
[[p:oracle-coin-change-unbounded-and-single-use|Minimum Coins with Reusable or Single-Use Entries]]
exists to test it.

**5. Zeros in a counting knapsack.** Symptom: the count is off by a power of two. A
zero can be taken or skipped without changing the sum, so every zero doubles the
number of subsets. That is correct when subsets are chosen by position, and the
right-to-left loop handles it (the loop for x = 0 reads ways[s] before writing it,
so it doubles every cell once). It is wrong if the problem counts distinct
*values*, and it breaks code that starts the loop at s = 1 or skips zeros "as
harmless".

**6. Reconstructing from one row.** Symptom: no way to find the items. Keep the
2-D table, or a boolean `took[i][c]`.

**7. Combinations versus orders.** Symptom: a count too big or too small. Coins
outside counts multisets; amount outside counts sequences.

**8. Groups with the item loop outside.** Symptom: two items from one group.

**9. Building the table when W is 10^9.** Symptom: MemoryError, or a time limit
before the first item. Read the constraints before choosing the index.

The first, second and fifth traps, run:

```python run
NEG = float("-inf")

def best_exact_wrong(items, W):         # meant "fill exactly", initialised to 0
    dp = [0] * (W + 1)
    for w, v in items:
        for c in range(W, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[W]

def best_exact(items, W):               # only an empty bag of size 0 is "filled"
    dp = [0] + [NEG] * W
    for w, v in items:
        for c in range(W, w - 1, -1):
            if dp[c - w] != NEG:        # never build on an impossible state
                dp[c] = max(dp[c], dp[c - w] + v)
    return dp[W]

items = [(3, 5)]
print("fill exactly 4 with one item of weight 3:",
      "wrong ->", best_exact_wrong(items, 4), " right ->", best_exact(items, 4))
assert best_exact_wrong(items, 4) == 5 and best_exact(items, 4) == NEG

def min_coins_single_use(coins, amount, forward):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for x in coins:
        order = range(x, amount + 1) if forward else range(amount, x - 1, -1)
        for a in order:
            dp[a] = min(dp[a], dp[a - x] + 1)
    return dp[amount] if dp[amount] < INF else -1

coins = [5, 1, 1]                       # three physical coins
print("make 10 from the coins 5,1,1, each once:",
      "forward ->", min_coins_single_use(coins, 10, True),
      " backward ->", min_coins_single_use(coins, 10, False))
assert min_coins_single_use(coins, 10, True) == 2       # used the 5 twice
assert min_coins_single_use(coins, 10, False) == -1     # 5+1+1 = 7 < 10

def count_target(nums, t):
    ways = [1] + [0] * t
    for x in nums:
        for s in range(t, x - 1, -1):
            ways[s] += ways[s - x]
    return ways[t]

print("subsets of [0, 0, 2] with sum 2:", count_target([0, 0, 2], 2))
assert count_target([0, 0, 2], 2) == 4   # {2}, {0a,2}, {0b,2}, {0a,0b,2}
```

The forward loop makes 10 out of a single 5-coin used twice. The backward loop
correctly says 10 cannot be made from 5, 1 and 1. And [0, 0, 2] has four subsets
with sum 2 by position, because each zero doubles the count.

## What to memorise

The template:

```python
dp = [0] * (W + 1)                    # at most W; for "exactly", [0] + [NEG] * W
for w, v in items:
    for c in range(W, w - 1, -1):     # right to left: 0/1. Left to right: unbounded.
        dp[c] = max(dp[c], dp[c - w] + v)
answer = dp[W]
```

The sentence that turns a problem into it: **the state is (items still allowed,
resource left), and each item is skipped or taken.**

The question that finds the state: **what is the least the future needs to know
about the past?**

The habit: before typing, say which row the take branch must read. Old row, right
to left. Current row, left to right.

The numbers: n·W up to a few million is comfortable in Python; 10^9 in any axis
means that axis cannot be an index; n <= 40 suggests meet in the middle; n <= 20
suggests plain enumeration.

## Check yourself

:::check
Hand trace. Items A (w=2, v=3), B (w=3, v=4), C (w=4, v=5), W = 5. Fill the full
4 x 6 table, and for each cell of rows 2 and 3 name the two cells you compared.
Walk back to find the items. Then run the one-row version right to left and left
to right, and find the first cell where an item is used twice.
--
| | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| row 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| row 1 (+A) | 0 | 0 | 3 | 3 | 3 | 3 |
| row 2 (+B) | 0 | 0 | 3 | 4 | 4 | 7 |
| row 3 (+C) | 0 | 0 | 3 | 4 | 5 | 7 |

Row 2: c=0..2, B does not fit, copy. c=3: skip row1[3]=3, take row1[0]+4=4, so 4.
c=4: skip 3, take row1[1]+4=4, so 4. c=5: skip 3, take row1[2]+4=7, so 7.
Row 3: c=0..3 copy. c=4: skip row2[4]=4, take row2[0]+5=5, so 5. c=5: skip
row2[5]=7, take row2[1]+5=5, so 7.

Walk back from (3,5)=7: equal to (2,5)=7, so C skipped. (2,5)=7 differs from
(1,5)=3, B taken, column 5-3=2. (1,2)=3 differs from (0,2)=0, A taken. Items A
and B, weight 5, value 7.

Right to left gives 0 0 3 3 3 3, then 0 0 3 4 4 7, then 0 0 3 4 5 7: the rows of
the table.

Left to right, item A: c=2 reads dp[0]=0, writes 3; c=3 reads dp[1]=0, writes 3;
**c=4 reads dp[2], which was just written (3), and writes 6: A used twice.** c=5
reads dp[3]=3 (new), writes 6. After A: 0 0 3 3 6 6. After B: 0 0 3 4 6 7. After
C: 0 0 3 4 6 7. The corner is still 7 by coincidence, but dp[4] = 6 is A twice;
the true best for a bag of 4 is 5. A test asking for W = 4 would catch it.
:::

:::check
Hand trace. One item (w=1, v=1), W = 4, array [0, 0, 0, 0, 0]. What do the
right-to-left and left-to-right loops produce? In one sentence, what does the
left-to-right result mean in real life?
--
Right to left: c=4 reads dp[3]=0, writes 1; c=3 reads dp[2]=0, writes 1; then c=2
and c=1 the same. Result [0, 1, 1, 1, 1]: one item, in any bag that fits it.

Left to right: c=1 reads dp[0]=0, writes 1; c=2 reads dp[1]=1 (new), writes 2;
c=3 reads 2, writes 3; c=4 reads 3, writes 4. Result [0, 1, 2, 3, 4].

In real life, the second answer is what you get if the item is a coin of value 1
from an unlimited pile: a bag of size c holds c of them. It is the unbounded
knapsack, and for 0/1 it is wrong in every column from 2 up.
:::

:::check
Hand trace. Coins [1, 3], amount 4. Fill the counting array with coins outside,
then with the amount outside. Which number counts combinations, and which counts
ordered sequences? List what each counts.
--
Coins outside, start [1, 0, 0, 0, 0]. After coin 1: [1, 1, 1, 1, 1]. After coin 3:
ways[3] += ways[0] gives 2, ways[4] += ways[1] gives 2. Final [1, 1, 1, 2, 2]:
**2 combinations**, {1,1,1,1} and {1,3}.

Amount outside: ways[1] = ways[0] = 1; ways[2] = ways[1] = 1; ways[3] = ways[2] +
ways[0] = 2; ways[4] = ways[3] + ways[1] = 2 + 1 = 3. **3 sequences**: 1111, 13, 31.

The difference is the pair 13 and 31: the same multiset, two orders. Coins outside
only ever builds "the 1s, then the 3s", so it sees one of them.
:::

:::check
Why does the 2-D table not care which direction the inner loop runs, while the
1-D array does?
--
In the 2-D table, row i is written into a separate list from row i-1. Every read
of the take branch goes to dp[i-1][c - w], a cell that the current loop never
writes, so the order in which the columns of row i are filled cannot change any
read. Any order, even random, gives the same row.

In the 1-D array, the old row and the new row share the same cells. A read of
dp[c - w] sees the old value only if that cell has not been written yet this
round. Right to left guarantees it (all writes are to the right of all future
reads); left to right guarantees the opposite. The direction is how the 1-D code
remembers the row index that it no longer stores.
:::

:::check
Someone says: "I sorted the items by value per weight and took them greedily, and
it passed all the samples, so it is correct." Where are they wrong, and what is the
smallest input you would use to show it?
--
Passing samples shows the greedy is right on those inputs, not on all of them.
Greedy by ratio is exact only when items can be split; with whole items, a high
ratio item can leave a gap.

Limit 10, items (6, 13), (5, 10), (5, 10). Ratios 2.17, 2, 2. Greedy takes the
first (13), and nothing else fits: 13. The two others fill the bag exactly: 20.
:::

:::check
Someone says: "My left-to-right 1-D loop passed every test for 0/1 knapsack, so
the direction does not matter for these inputs." When are they right, and when
will they be caught?
--
They are right exactly when no item can be taken twice in any bag the answer
depends on. In the left-to-right loop, a cell c reads an already-updated cell
c - w only if c - w >= w, that is c >= 2w. If every item has 2w > W, no cell ever
reads a new value, and the loop happens to compute the 0/1 answer.

They are caught by the first light item (2w <= W) whose second copy beats the
honest answer: one item (w=2, v=5) with W=6 gives 15, not 5. Even then the corner
can hide it, as in the four-item example, so "it passed" is not evidence.
:::

:::check
Reduce this disguised problem. "Given nums = [1, 1, 1, 1, 1] and T = 3, count the
ways to put + or - in front of each number so the total is T." Do the algebra,
name the knapsack, and give the answer. Then say what happens for T = 2.
--
Let P be the sum of numbers with +, N with -. P - N = T and P + N = S = 5. So
2P = S + T = 8, P = 4. Count subsets with sum 4: 0/1 counting knapsack, target 4.

Five ones, choose which four get a plus: C(5, 4) = 5. The five expressions are
the ones with exactly one minus sign.

For T = 2, S + T = 7 is odd, so P would be 3.5. No subset sums to a half, the
answer is 0, and the code must check parity before indexing.
:::

:::check
Which quantity is small? For each, say what the DP index should be, or why
there is no table. (a) n = 100, W = 10^9, every value <= 100. (b) n = 40, weights
and W up to 10^9, values up to 10^9. (c) n = 200, weights <= 100, W <= 10^4,
values up to 10^9. (d) n = 10^5 item types, each of weight 1, W = 10^9.
--
(a) The total value is at most 100 x 100 = 10^4. Index by value:
least[val] = minimum weight for value val, 10^4 columns, then the largest val with
least[val] <= W. (Variation F.)

(b) Nothing numeric is small, but n is. Split into two halves of 20 items, list
2^20 sums per half, sort and combine. (Variation G.)

(c) The standard table: 200 x 10^4 = 2·10^6 cells, indexed by weight. Large values
are fine; they live inside cells, not on an axis.

(d) No table. Every unit weighs the same, so the best W units are the most
valuable ones: sort by value and take from the top, stopping at W or when the units
run out.
:::
