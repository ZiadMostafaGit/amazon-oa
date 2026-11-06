# Dynamic Programming: the Method

> Dynamic programming is what happens when a brute force that tries every sequence of decisions keeps asking the same few questions about the future, so you answer each question once, write it down, and the exponential tree collapses into a short list of situations.

## The problem it solves

A street has five houses. House i holds some money:

| house | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| money | 2 | 7 | 9 | 3 | 1 |

You may take the money from any set of houses, with one rule: never two
neighbours. Houses 1 and 3 together are fine. Houses 2 and 3 are not. What is the
most you can collect?

This is *House Robber*, and the bank has it from several companies, for example
[[p:inmobi-house-robber|House Robber I]]. It is the problem this chapter is built
around, because it is the smallest problem with a real decision in it, and
because every other technique in one-dimensional DP is the same method with a
different question at each position.

The first solution anyone writes is to try everything. A choice of houses is a
yes or no for each of the five, so there are 2^5 = 32 candidate sets. Throw away
the ones that contain two neighbours, add up the rest, keep the largest. The
winner is houses 1, 3 and 5: 2 + 9 + 1 = 12. For five houses that is fine.

It stops being fine quickly. The number of legal sets grows like the Fibonacci
numbers, about 1.618^n. Forty houses give over a hundred million legal sets.
The bank's version allows 10^5 houses, and
already 1.618^100 is a number with 21 digits.

The second solution anyone writes is a rule of thumb. Three are popular, and all
three are wrong.

- **"Take the richest house, cross out its neighbours, repeat."** On 3, 4, 3 it
  takes the 4, which crosses out both 3s: total 4. Taking both 3s gives 6.
- **"Take every other house: the odd ones or the even ones, whichever is
  bigger."** On 2, 1, 1, 2 the odd houses give 2 + 1 = 3 and the even houses give
  1 + 2 = 3. The best is houses 1 and 4: 2 + 2 = 4. Skipping *two* houses in a row
  is sometimes right, and alternating never does it.
- **"Walk left to right and take a house whenever its neighbour was not
  taken."** On 1, 5, 1 it takes the first 1, which forbids the 5: total 2. The
  best is 5.

Each rule fails for the same reason. Taking a house has a consequence (a
neighbour becomes forbidden), and whether that consequence is worth it depends on
houses the rule has not looked at yet. A rule that decides now, from what it can
see now, cannot know.

What this chapter builds is a method that is exact like the brute force and fast
like a single loop: for a street of n houses it does about n small steps. The
method is called dynamic programming. It is not a trick for this problem. It is a
procedure that takes any brute force of the form "make a decision, then solve
what is left" and removes its waste. After the derivation, the same procedure
produces climbing stairs, the fewest coins for an amount, the number of ways to
decode a string of digits, word break, the best subarray (Kadane), and the longest
increasing subsequence. They are all in "Variations", and each one is the method
with a different answer to one question.

### When it is the wrong tool

DP pays for itself only when the brute force asks the same question many times.
When that is not true, something else is better.

- **A safe local rule exists, and you can prove it.** "Pick the meeting that ends
  first" is provably optimal for fitting the most meetings into a room. Then the
  greedy is shorter, faster and needs no table ([[greedy]], and
  [[greedy-exchange]] for the proof). The coin problem in "Variations" is the
  cautionary tale: the greedy is right for ordinary currency and wrong for coins
  1, 3, 4, and only a proof tells the two apart.
- **The subproblems never repeat.** Merge sort splits an array in half and sorts
  each half. The halves are disjoint, so no question is asked twice, and a cache
  would only waste memory. That is [[divide-and-conquer]].
- **You must list every solution, not count or optimise them.** "Return all the
  ways to split this string into dictionary words" can have exponentially many
  answers, and no table makes printing them cheaper. That is [[backtracking]].
- **The future depends on the whole past.** If what you may do next depends on
  the exact set of things you did before, and that set can be anything, the
  number of situations is the number of histories, and nothing collapses.

## Build it from the brute force

We will not start with a table. We will start with the slowest correct program a
beginner would write, and remove its waste one step at a time. The table, and
then the two-variable loop, will appear at the end as the obvious thing to do.

### Step 1: one decision at a time

"Try every legal set" can be written as a sequence of decisions. Look at the last
house. Either you rob it, or you do not. Every legal set falls into exactly one of
those two groups.

- If you **skip** the last house, the rest of your choice is some legal set of
  the other houses. Nothing else changes.
- If you **rob** the last house, you collect its money, and its neighbour, the
  second-to-last house, is forbidden. The rest of your choice is some legal set of
  the houses before that neighbour.

Write that as a function. Let

> f(i) = the most money I can collect from the first i houses alone.

Then, with x_i the money in house i:

```
f(i) = max( f(i-1),            skip house i
            x_i + f(i-2) )     rob house i: house i-1 is off limits
f(0) = 0                       no houses: nothing to collect
f(1) = x_1                     one house: rob it
```

The answer is f(n).

Read the rob branch slowly, because it is where the rule lives. Robbing house i
does two things: it collects x_i now, and it removes house i-1 from play. The
"i-2" is not a formula you memorise. It is the neighbour rule, written as an
index. The function never has to remember "did I rob the previous house?",
because it never puts itself in a position where the answer matters: after a rob
it jumps over the neighbour.

### You might think: "One call is enough. Rob it if the neighbour is free."

This is the most common first instinct, and it is the third greedy rule from
above in recursive clothes. It makes one decision per house, and the decision is
made before the future is known.

The counterexample is three houses: 1, 5, 1. Left to right, "rob it if you can"
robs house 1 (value 1), which makes house 2 off limits, then robs house 3. Total 2.
The best is house 2 alone, 5. Going right to left does not save it either: it robs
house 3 first and forbids the 5 the same way.

So sometimes the right move is to skip a house you are allowed to rob. You cannot
know, at that moment, whether this is one of those times, because it depends on
houses you have not looked at. That is why the recursion tries **both** and keeps
the better result. Two calls are not a style. They are the whole point: the
recursion postpones the decision until both consequences are known.

### You might think: "I need to remember which houses I robbed."

A natural worry: the rule is about neighbours, so surely the function needs the
set of robbed houses, or at least "was the previous one robbed?", as an argument.

It needs much less. Look at what the future can actually see. Once you have
decided about houses i+1..n, what is left is a choice among houses 1..i, and the
only thing about the past that can affect that choice is whether house i+1 was
robbed (because then house i is forbidden). The rest of the past (which houses
further right were robbed, how much money is already in the bag) changes nothing
about which sets of houses 1..i are legal, and nothing about how good each is.

The recursion handles even that one fact without storing it: if house i+1 was
robbed, the call jumps straight to f(i-1) and never asks about house i. So a single
number, i, is the whole state. We will come back to this, because it is the
question that unlocks every DP.

### You might think: "f(i) is the best when I rob house i."

That is a different, legal definition, and mixing it up with ours is a classic
bug. Call it g(i) = the most money from a legal set of the first i houses that
**includes** house i. Then g(i) = x_i + max(g(j)) over j <= i-2, and the answer
is the largest g(i) over all i, not g(n).

On 1, 5, 1: g(1) = 1, g(2) = 5, g(3) = 1 + g(1) = 2. Returning g(3) gives 2,
which is wrong. The answer is max(1, 5, 2) = 5.

Both definitions work. They have different transitions and a different answer
cell, and the bug is to use the transition of one with the answer cell of the
other. The habit that prevents it: **write the definition of f in one English
sentence before writing any code, and read the answer cell off that sentence.**
"Best from the first i houses" means the answer is f(n). "Best that robs house i"
means the answer is a max over all i. Later in this chapter the "ends at i"
definition is the right one (Kadane, LIS), so you need both in your hands.

### Step 2: count it

How slow is the two-call recursion? Each call with i >= 2 makes two calls, one
with i-1 and one with i-2. Let C(i) be the number of calls made to compute f(i).
Then C(0) = C(1) = 1 and

```
C(i) = 1 + C(i-1) + C(i-2)
```

That gives 1, 1, 3, 5, 9, 15, 25, 41, ... which grows like the Fibonacci numbers,
about 1.618^i. (Add 1 to every term and you get exactly twice the Fibonacci
numbers.) For 100 houses that is more than 10^21 calls. The recursion is correct
and exactly as slow as listing the sets, which makes sense: it *is* the list of
sets, written as a tree. Every path from the root to a leaf is one legal set.

So far we have only rewritten the brute force. The question is where its time
goes.

### Step 3: notice the waste

Here is the whole tree for five houses, f(5). The left child of each box is
"skip" (i-1), the right child is "rob" (i-2).

<svg viewBox="0 0 760 360" role="img" aria-label="the recursion tree of f(5) for house robber: f(3) appears twice and is shaded, f(2) appears three times, and the subtrees under the repeated copies are dashed; 15 calls in total">
  <g>
    <rect x="345" y="15" width="70" height="30" rx="4"/>
    <text x="380" y="35" text-anchor="middle">f(5)</text>
    <rect x="165" y="90" width="70" height="30" rx="4"/>
    <text x="200" y="110" text-anchor="middle">f(4)</text>
    <rect class="fill" x="545" y="90" width="70" height="30" rx="4"/>
    <text x="580" y="110" text-anchor="middle">f(3)</text>
    <rect class="fill" x="75" y="165" width="70" height="30" rx="4"/>
    <text x="110" y="185" text-anchor="middle">f(3)</text>
    <rect x="255" y="165" width="70" height="30" rx="4"/>
    <text x="290" y="185" text-anchor="middle">f(2)</text>
    <rect x="465" y="165" width="70" height="30" rx="4" stroke-dasharray="5 4"/>
    <text x="500" y="185" text-anchor="middle">f(2)</text>
    <rect x="625" y="165" width="70" height="30" rx="4" stroke-dasharray="5 4"/>
    <text x="660" y="185" text-anchor="middle">f(1)</text>
    <rect x="30" y="240" width="60" height="30" rx="4"/>
    <text x="60" y="260" text-anchor="middle">f(2)</text>
    <rect x="130" y="240" width="60" height="30" rx="4"/>
    <text x="160" y="260" text-anchor="middle">f(1)</text>
    <rect x="225" y="240" width="60" height="30" rx="4"/>
    <text x="255" y="260" text-anchor="middle">f(1)</text>
    <rect x="300" y="240" width="60" height="30" rx="4"/>
    <text x="330" y="260" text-anchor="middle">f(0)</text>
    <rect x="430" y="240" width="60" height="30" rx="4" stroke-dasharray="5 4"/>
    <text x="460" y="260" text-anchor="middle">f(1)</text>
    <rect x="510" y="240" width="60" height="30" rx="4" stroke-dasharray="5 4"/>
    <text x="540" y="260" text-anchor="middle">f(0)</text>
    <rect x="5" y="310" width="50" height="30" rx="4"/>
    <text x="30" y="330" text-anchor="middle">f(1)</text>
    <rect x="70" y="310" width="50" height="30" rx="4"/>
    <text x="95" y="330" text-anchor="middle">f(0)</text>
    <line x1="365" y1="45" x2="210" y2="90"/>
    <line x1="395" y1="45" x2="570" y2="90"/>
    <line x1="190" y1="120" x2="120" y2="165"/>
    <line x1="210" y1="120" x2="280" y2="165"/>
    <line x1="570" y1="120" x2="510" y2="165" stroke-dasharray="5 4"/>
    <line x1="590" y1="120" x2="650" y2="165" stroke-dasharray="5 4"/>
    <line x1="100" y1="195" x2="65" y2="240"/>
    <line x1="120" y1="195" x2="155" y2="240"/>
    <line x1="280" y1="195" x2="260" y2="240"/>
    <line x1="300" y1="195" x2="325" y2="240"/>
    <line x1="490" y1="195" x2="465" y2="240" stroke-dasharray="5 4"/>
    <line x1="510" y1="195" x2="535" y2="240" stroke-dasharray="5 4"/>
    <line x1="55" y1="270" x2="35" y2="310"/>
    <line x1="65" y1="270" x2="90" y2="310"/>
    <text x="270" y="62" text-anchor="end">skip 5</text>
    <text x="490" y="62">rob 5</text>
    <text x="610" y="300">dashed: work done twice</text>
    <text x="380" y="355" text-anchor="middle">Shaded: the same question, f(3), asked by "skip 5, skip 4" and by "rob 5".</text>
  </g>
</svg>

Fifteen boxes, as C(5) predicted. Look at the two shaded boxes. Both say f(3).
One was reached by "skip house 5, skip house 4". The other by "rob house 5". Those
are different histories: different houses robbed, different money in the bag
(0 versus 1). But the question each asks about the *future* is identical: "the
first three houses are still undecided, and I may use any legal set of them. What
is the most I can add?" The answer is 11 (houses 1 and 3) in both. The tree
computes it twice, and the dashed subtree under the second copy is pure
repetition. f(2) is computed three times, f(1) five times.

In this tiny tree the waste is about half. With 100 houses it is almost
everything: the tree has around 10^21 boxes, but the boxes can only say f(0)
through f(100). That is 101 different labels. Nearly the whole tree is the same
101 questions asked over and over.

### The question that unlocks it

Why did two different histories collapse into one box? Because the future does
not care how you got there. It does not care which houses further right were
robbed, or how much money is in the bag. It cares about one thing: which houses
are still undecided.

That is the question to ask on every DP problem, in this chapter and every one
after it:

**What is the least the future needs to know about the past?**

For House Robber the answer is i: "houses 1..i are undecided, and house i is
allowed" (the rob branch made sure of that by jumping over the neighbour). The
money already collected is *not* part of the state, because the future adds to it
whatever is best, regardless of what it is. Two paths with different money and the
same i have the same best future, so you solve that future once and add it to
each.

Say it a second way. The past is a long story: "I looked at house 5 and robbed it,
so I skipped house 4." The future only reads the last line of the story: "three
houses left." Dynamic programming is the decision to stop telling the story and
keep only that last line. The state is the last line. If two stories end with the
same last line, they share a future.

When the answer to the question is small (a single index here; an index and a
capacity in [[knapsack]]; two indices in [[dp-2d]]), DP works. When the answer is
"the whole history", it does not.

### Step 4: remember answers (memoisation)

The cure for asking the same question twice is to write down the answer the first
time. Keep a dictionary, or a list, from i to f(i). Before computing f(i), look it
up. After computing it, store it.

The recursion is unchanged. Only the bookkeeping is new. Each distinct i is
computed once, with O(1) work besides its two lookups, so f(n) costs n+1
computations instead of 1.618^n calls. That is the whole speed-up, and it came
from nothing cleverer than not recomputing.

### Step 5: fill the answers in order (the table)

The memo still lets recursion decide the order of work: f(5) asks f(4), which asks
f(3), down to f(0). We can do the same work without recursion if we compute the
answers in an order where everything a cell needs is already known.

What does f(i) need? f(i-1) and f(i-2). Both have smaller indices. So compute
f(0), then f(1), then f(2), and so on: every lookup finds its answer ready. Store
them in a list dp of n+1 numbers, and you have the table. The loop direction is not
a style choice. It is the evaluation order, and it is legal because **every arrow
in the recursion points to a smaller index**.

### Step 6: keep only what is still needed

dp[i] reads only dp[i-1] and dp[i-2]. Once dp[i] is written, dp[i-2] is never read
again. So two variables are enough: the last answer and the one before it. Doing
that correctly needs exactly one subtle line, the order in which the two variables
are updated, and it gets its own demonstration in "From the idea to the code".

### The method in one sentence

**Dynamic programming: write the brute force as "make one decision, then solve
what is left"; notice that "what is left" is described by a small state; solve each
state once, in an order where everything it needs is already solved.**

That sentence has four parts, and every DP you will ever write answers them, in
this order:

1. **The state.** What does dp[i] mean, in one English sentence? (The least the
   future needs to know.)
2. **The transition.** How is dp[i] built from smaller states? (The last
   decision, and its cases.)
3. **The base cases.** Which states are known without asking anything?
4. **The order and the answer.** In what order are the states filled, and which
   cell is the answer?

And the question that produces the first answer, worth asking again on every new
problem: **what is the least the future needs to know about the past?**

## Worked by hand

Get a pen. Houses 2, 7, 9, 3, 1. The table has one cell per state, dp[0] to dp[5],
and dp[i] is "the best from the first i houses".

| i | house i | skip: dp[i-1] | rob: x_i + dp[i-2] | dp[i] | decision |
|---|---|---|---|---|---|
| 0 | none | | | 0 | base |
| 1 | 2 | dp[0] = 0 | 2 + 0 = 2 | 2 | rob |
| 2 | 7 | dp[1] = 2 | 7 + dp[0] = 7 | 7 | rob |
| 3 | 9 | dp[2] = 7 | 9 + dp[1] = 11 | 11 | rob |
| 4 | 3 | dp[3] = 11 | 3 + dp[2] = 10 | 11 | skip |
| 5 | 1 | dp[4] = 11 | 1 + dp[3] = 12 | **12** | rob |

For dp[1] there is no dp[-1]; robbing the only house means adding nothing from
before, so treat the missing cell as 0.

Every cell is the larger of two numbers, and both come from the cells just before
it:

- **skip**: the cell one to the left.
- **rob**: the cell two to the left, plus this house's money.

Here is the story of one cell, dp[3], told in full:

> "I am answering the question for the first three houses: 2, 7, 9. If I skip house
> 3, the best is whatever the first two houses can do on their own. That question
> was already answered: dp[2] = 7. If I rob house 3, I collect 9, and house 2 is
> forbidden, so the rest must come from the first house alone. That was answered
> too: dp[1] = 2. Rob gives 9 + 2 = 11. The larger of 7 and 11 is 11."

And the same cell as a picture, with the real numbers in it:

<svg viewBox="0 0 640 220" role="img" aria-label="the dp array for houses 2, 7, 9, 3, 1; cell dp[3] reads dp[2] = 7 for skip and dp[1] = 2 for rob, plus 9, giving 11">
  <g>
    <text x="85" y="40" text-anchor="middle">dp[0]</text>
    <text x="175" y="40" text-anchor="middle">dp[1]</text>
    <text x="265" y="40" text-anchor="middle">dp[2]</text>
    <text x="355" y="40" text-anchor="middle">dp[3]</text>
    <text x="445" y="40" text-anchor="middle">dp[4]</text>
    <text x="535" y="40" text-anchor="middle">dp[5]</text>
    <text x="85" y="160" text-anchor="middle">none</text>
    <text x="175" y="160" text-anchor="middle">house 2</text>
    <text x="265" y="160" text-anchor="middle">house 7</text>
    <text x="355" y="160" text-anchor="middle">house 9</text>
    <text x="445" y="160" text-anchor="middle">house 3</text>
    <text x="535" y="160" text-anchor="middle">house 1</text>
    <rect x="40" y="100" width="90" height="40"/>
    <text x="85" y="126" text-anchor="middle">0</text>
    <rect class="fill" x="130" y="100" width="90" height="40"/>
    <text x="175" y="126" text-anchor="middle">2</text>
    <rect class="fill" x="220" y="100" width="90" height="40"/>
    <text x="265" y="126" text-anchor="middle">7</text>
    <rect x="310" y="100" width="90" height="40"/>
    <text x="355" y="126" text-anchor="middle">11</text>
    <rect x="400" y="100" width="90" height="40" stroke-dasharray="4 4"/>
    <rect x="490" y="100" width="90" height="40" stroke-dasharray="4 4"/>
    <path d="M 265 100 Q 310 72 350 98"/>
    <polyline points="342,94 350,98 344,90"/>
    <path d="M 175 100 Q 265 45 355 98"/>
    <polyline points="347,95 355,98 350,90"/>
    <text x="300" y="80" text-anchor="middle">skip: 7</text>
    <text x="210" y="62" text-anchor="middle">rob: 2 + 9 = 11</text>
    <text x="320" y="200" text-anchor="middle">dp[3] = max(skip 7, rob 11) = 11; the dashed cells are not computed yet</text>
  </g>
</svg>

Skip means "look one cell left". Rob means "look two cells left, then add this
house". It jumps two because the neighbour is off limits.

**dp[4]**, house 3: skip gives dp[3] = 11. Rob gives 3 + dp[2] = 3 + 7 = 10. Skip
wins. This is the first time a house that is allowed is left alone: robbing house
4 would forbid house 3, the 9, and the 3 is not worth the 9.

**dp[5]**, house 1: skip gives 11, rob gives 1 + dp[3] = 1 + 11 = 12. Rob wins:
**12**.

### Getting the houses back

The table holds amounts, not sets. To find the houses, walk backward from the end
and ask, at each cell, "did this house change the answer?"

1. dp[5] = 12, dp[4] = 11. Different, so house 5 was robbed. Robbing jumps two:
   go to dp[3].
2. dp[3] = 11, dp[2] = 7. Different, so house 3 was robbed. Go to dp[1].
3. dp[1] = 2, dp[0] = 0. Different, so house 1 was robbed. Go to dp[-1]: done.

Robbed: houses 1, 3, 5, the 2, the 9 and the 1. Total 12. When the two cells are
equal, the walk says "skip": an optimal set without this house exists, so skipping
is safe. That is also where you would encode a tie rule if a problem wanted a
particular optimal set.

### A second trace: skipping two in a row

Now the input that beat the "odd or even houses" rule: 2, 1, 1, 2.

| i | house i | skip: dp[i-1] | rob: x_i + dp[i-2] | dp[i] | decision |
|---|---|---|---|---|---|
| 0 | none | | | 0 | base |
| 1 | 2 | 0 | 2 + 0 = 2 | 2 | rob |
| 2 | 1 | 2 | 1 + 0 = 1 | 2 | skip |
| 3 | 1 | 2 | 1 + 2 = 3 | 3 | rob |
| 4 | 2 | 3 | 2 + dp[2] = 2 + 2 = **4** | **4** | rob |

Look at the last cell. The rob branch reads dp[2] = 2. What is in dp[2]? The best
of the first two houses, which is house 1 alone: dp[2] *already decided to skip
house 2*. So "rob house 4, plus dp[2]" is houses 1 and 4, with houses 2 and 3 both
skipped.

Nobody wrote a rule that says "you may skip two in a row". The table did not need
one. dp[2] kept, for the first two houses, the best answer for that situation,
whatever it was, and it happened to be a skip. Walk back to confirm: dp[4] = 4
differs from dp[3] = 3, so house 4 is robbed, jump to dp[2]. dp[2] = 2 equals
dp[1] = 2: house 2 skipped, step to dp[1]. dp[1] = 2 differs from dp[0]: house 1
robbed. Houses 1 and 4.

This is what the trace shows and the code hides: **the table never commits early**.
Every cell is the best answer for its own situation, stored side by side with the
others. The greedy rules each had one plan and stuck with it. The table keeps
every situation's best plan, and when a new house arrives, it picks whichever
earlier situation gives the best total.

## From the idea to the code

### All four steps, measured

The program below writes the derivation out: the two-call brute force with a call
counter, the memo with a state counter, the table, and the two-variable loop. It
checks all four against plain enumeration of every legal set.

```python run
from itertools import product
import random

def brute(x):
    calls = 0
    def f(i):                         # best from the first i houses
        nonlocal calls
        calls += 1
        if i == 0:
            return 0
        if i == 1:
            return max(0, x[0])
        return max(f(i - 1),              # skip house i
                   x[i - 1] + f(i - 2))   # rob house i, jump the neighbour
    return f(len(x)), calls

def memo(x):
    seen = {}
    def f(i):
        if i in seen:
            return seen[i]
        if i <= 1:
            ans = 0 if i == 0 else max(0, x[0])
        else:
            ans = max(f(i - 1), x[i - 1] + f(i - 2))
        seen[i] = ans
        return ans
    return f(len(x)), len(seen)

def table(x):
    n = len(x)
    dp = [0] * (n + 1)                # dp[0] = 0: no houses
    for i in range(1, n + 1):         # smaller i first: every read is ready
        two_back = dp[i - 2] if i >= 2 else 0
        dp[i] = max(dp[i - 1], x[i - 1] + two_back)
    return dp

def rolling(x):
    prev2, prev1 = 0, 0               # dp[i-2], dp[i-1]
    for v in x:
        prev2, prev1 = prev1, max(prev1, prev2 + v)
    return prev1

def every_set(x):                     # the truth, by enumeration
    best = 0
    for pick in product([0, 1], repeat=len(x)):
        if all(not (pick[i] and pick[i + 1]) for i in range(len(x) - 1)):
            best = max(best, sum(v for v, p in zip(x, pick) if p))
    return best

houses = [2, 7, 9, 3, 1]
print("dp table:", table(houses))
print("brute (answer, calls):", brute(houses), " memo (answer, states):", memo(houses))
assert table(houses) == [0, 2, 7, 11, 11, 12]
assert brute(houses) == (12, 15) and memo(houses) == (12, 6)
assert table([2, 1, 1, 2])[-1] == 4 and rolling([1, 5, 1]) == 5

r7 = random.Random(7)
street = [r7.randint(0, 50) for _ in range(25)]
(b, calls), (m, states) = brute(street), memo(street)
print("25 houses: brute calls", calls, " memo states", states)
assert b == m == rolling(street) and states == 26 and calls > 100000

rng = random.Random(1)
for _ in range(300):
    x = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
    assert table(x)[-1] == rolling(x) == memo(x)[0] == every_set(x)
print("table == rolling == memo == every legal set, on 300 random streets")
```

The brute force makes 15 calls on five houses (the 15 boxes in the picture) and
the memo solves 6 states (f(0) to f(5)). On 25 houses the brute force makes over
two hundred thousand calls and the memo still solves 26. Add 25 more houses and
the first number multiplies by about 1.618^25, roughly 170,000. The second
number goes to 51.

### Each line, and which part of the recursion it is

Take the table version:

| line | in plain words | in the recursion |
|---|---|---|
| `dp = [0] * (n + 1)` | one cell per state, n+1 of them, all 0 | dp[0] = 0 is the base case f(0) |
| `for i in range(1, n + 1)` | solve the first 1 house, then 2, then 3 ... | "smaller i first": every cell read is already final |
| `two_back = dp[i - 2] if i >= 2 else 0` | the best before the neighbour; nothing before house 1 | the f(i-2) of the rob branch, with f(-1) = 0 |
| `dp[i - 1]` | the best if house i is left alone | the skip branch, f(i-1) |
| `x[i - 1] + two_back` | house i's money plus the best before its neighbour | the rob branch, x_i + f(i-2) |
| `max(...)` | keep the better plan | the max of the two branches |
| `return dp` and read `dp[n]` | the last cell | f(n) |

Three lines do the real work: the skip read, the rob read, and the max. The rest
is scaffolding.

### Three boring confusions, settled

**Why does dp have n+1 cells when there are n houses?** Because dp[0] has a job. It
is "zero houses", the base case every other cell is built on. Row 0 of a knapsack
table, the empty prefix of a string, the amount 0 in coin change: there is almost
always one extra cell for "nothing yet", and it is almost always the base case.

**Why x[i-1]?** dp[i] means "the first i houses", so the i-th house is the last one
of them, and Python lists start at 0: the i-th house is x[i-1]. You can avoid the
shift by defining dp[i] as "houses 0..i", which is the same thing said differently;
what you cannot avoid is deciding, in words, which one you mean.

**What does a cell store?** One number: the best total. It does not store which
houses achieved it, and it does not store "was house i robbed?". Both can be
recovered by comparing neighbouring cells, as in the walk back, and the walk back
needs the whole table.

### The subtle line: updating the two variables

The rolling version has one line that is easy to get wrong:

```python
prev2, prev1 = prev1, max(prev1, prev2 + v)
```

Before the line, prev2 holds dp[i-2] and prev1 holds dp[i-1]. After it, prev2
must hold dp[i-1] and prev1 must hold dp[i]. The new dp[i] needs the **old** prev2.
Python's tuple assignment evaluates the whole right side first, using the old
values, and only then assigns, so it is correct.

Now the version people write when they translate it to two lines:

```python
prev2 = prev1
prev1 = max(prev1, prev2 + v)      # prev2 is already the NEW value
```

After the first line, prev2 is dp[i-1], not dp[i-2]. The second line computes
max(dp[i-1], dp[i-1] + v): the money of house i added to a plan that may already
contain house i-1. That is robbing neighbours.

Here are both on houses 2, 7, 9, 3, 1, with the values after each house. A `*`
marks a value that has already been overwritten for this house when it is read.

**Right (tuple assignment, or a temporary).**

| house | reads prev2 | reads prev1 | new prev1 = max(prev1, prev2 + v) | prev2, prev1 after |
|---|---|---|---|---|
| start | | | | 0, 0 |
| 2 | 0 | 0 | max(0, 0+2) = 2 | 0, 2 |
| 7 | 0 | 2 | max(2, 0+7) = 7 | 2, 7 |
| 9 | 2 | 7 | max(7, 2+9) = 11 | 7, 11 |
| 3 | 7 | 11 | max(11, 7+3) = 11 | 11, 11 |
| 1 | 11 | 11 | max(11, 11+1) = 12 | 11, 12 |

**Wrong (prev2 overwritten first).**

| house | prev2 after line 1 | reads prev2 | new prev1 | prev2, prev1 after |
|---|---|---|---|---|
| start | | | | 0, 0 |
| 2 | 0 | 0* | max(0, 0+2) = 2 | 0, 2 |
| 7 | 2 | **2*** | max(2, 2+7) = **9** | 2, 9 |
| 9 | 9 | 9* | max(9, 9+9) = 18 | 9, 18 |
| 3 | 18 | 18* | 21 | 18, 21 |
| 1 | 21 | 21* | 22 | 21, 22 |

Look at the row for house 7. The right version reads prev2 = 0 (the best before
house 1, which is nothing) and says "rob 7 alone: 7". The wrong version reads
prev2 = 2, which is the plan that *robbed house 1*, and adds 7 to it: houses 1 and
2 together, neighbours. From there on it adds every house to the previous plan.

So the wrong version does not compute garbage. It computes, exactly, the sum of
all non-negative houses: 2 + 7 + 9 + 3 + 1 = 22. It is the answer to the problem
without the neighbour rule. The two versions differ by one word in the statement
("no two adjacent") and by the order of two assignments in the code.

Read the rule a second way: the rob branch must read the state from **before the
neighbour**. In the table that is dp[i-2], a cell two to the left, and nobody can
spoil it. In two variables it is "the old prev2", and it survives only if you read
it before you overwrite it.

```python run
def right(x, trace=False):
    prev2, prev1 = 0, 0
    for v in x:
        prev2, prev1 = prev1, max(prev1, prev2 + v)   # right side uses OLD values
        if trace:
            print("  house %d -> prev2 %2d, prev1 %2d" % (v, prev2, prev1))
    return prev1

def wrong(x, trace=False):
    prev2, prev1 = 0, 0
    for v in x:
        prev2 = prev1                                 # dp[i-2] is lost here
        prev1 = max(prev1, prev2 + v)
        if trace:
            print("  house %d -> prev2 %2d, prev1 %2d" % (v, prev2, prev1))
    return prev1

def with_temp(x):                                     # the same fix, spelled out
    prev2, prev1 = 0, 0
    for v in x:
        new = max(prev1, prev2 + v)
        prev2 = prev1
        prev1 = new
    return prev1

houses = [2, 7, 9, 3, 1]
print("right:"); r = right(houses, True)
print("wrong:"); w = wrong(houses, True)
assert r == 12 and with_temp(houses) == 12
assert w == 22 == sum(houses)            # it robbed every house: no neighbour rule

import random
rng = random.Random(3)
for _ in range(300):
    x = [rng.randint(-5, 9) for _ in range(rng.randint(0, 10))]
    assert wrong(x) == sum(v for v in x if v > 0)     # what it really computes
    assert right(x) == with_temp(x)
print("the wrong loop always returns the sum of the positive houses")
```

The last loop is the point. On 300 random streets, the wrong version returns the
sum of the positive houses every time. A bug that computes a different, simpler
problem is much harder to spot than a crash, because on many small tests the two
answers coincide (any street where the best plan happens to be "all positive
houses", such as 5, 0, 5).

### Memo or table?

Both are the same recurrence. The table is faster in Python, has no recursion
limit, and allows rolling variables. The memo needs no evaluation order (the call
stack finds one) and computes only the states the answer actually reaches, which
matters when most states are never asked about. For a line of n houses every state
is reached, so the table wins. Python's default recursion limit is about a
thousand frames; a memo over 10^5 houses raises `RecursionError`. Convert to the
table rather than raising the limit. [[memoization]] compares the two at length.

## Why it is correct

:::proof The table holds the true optimum
**What we claim.** For every i from 0 to n, dp[i] equals OPT(i), defined as the
largest total money of a set S of houses chosen from {1, ..., i} with no two
consecutive. (The empty set always qualifies, with total 0, so OPT is well
defined. The money values are taken to be non-negative, as in the problem.)

**Base cases.** OPT(0) = 0: the only set of houses from none is the empty set. The
code sets dp[0] = 0. For i = 1 the legal sets are {} and {1}, so OPT(1) =
max(0, x_1), which is what the code computes with the missing dp[-1] taken as 0.

**Inductive step.** Fix i >= 2 and assume dp[j] = OPT(j) for every j < i. Split
all legal sets for the first i houses into two groups that do not overlap and
together cover everything:

1. Sets that do **not** contain house i. These are exactly the legal sets of the
   first i-1 houses. The best of them is OPT(i-1) = dp[i-1]. That is the skip
   value.
2. Sets that **do** contain house i. Such a set cannot contain house i-1 (they
   are neighbours). Remove house i and what remains is a legal set of the first i-2
   houses. Conversely, add house i to any legal set of the first i-2 houses and the
   result is legal (house i-1 is not in it, so house i has no neighbour in it). So
   the sets of group 2 are exactly "a legal set of the first i-2 houses, plus house
   i", and the best of them is x_i + OPT(i-2) = x_i + dp[i-2]. That is the rob
   value.

The best legal set is in one group or the other, so OPT(i) is the larger of the two
group bests. That is exactly what the code writes into dp[i].

**Why "the rest must be optimal" is safe.** In group 2, could it pay to combine
house i with a *worse* set of the first i-2 houses? No: if a better set existed
there, swapping it in would give a better set for i that still contains house i.
So the best of group 2 always uses the best remainder. This is called optimal
substructure, and here it holds because the total is a sum: improving one part of
a sum improves the sum.

**Two directions, said plainly.** The value is never too high: every number the
code produces is the total of a real legal set (follow the choices back). It is
never too low: the optimal set lies in group 1 or group 2, and that group's best
is one of the two numbers compared. So it is exact.

**Order and termination.** The loop computes dp[1], dp[2], ... in increasing
order, and dp[i] reads only dp[i-1] and dp[i-2], which are already final. There
are n+1 cells, each computed once. ∎
:::

The proof is the method in miniature, and every DP proof you will write is this
paragraph with different nouns: **take an arbitrary optimal solution, look at its
last decision, delete it, and observe that what remains is an optimal solution to
a smaller state the recurrence already considered.** If every optimal solution's
last decision is one of your branches, the recurrence cannot miss the optimum. If
some optimal solution's last decision is not one of your branches, the recurrence
is wrong, and no amount of debugging the loop will help.

The proof quietly used these assumptions. Each is a place where a variation breaks
the method or changes it.

- **The state is enough.** Group 2 needed only "the first i-2 houses are free".
  That is true because the only interaction between houses is the neighbour rule.
  Add a rule like "at most k houses in total" and i is no longer enough: the
  future also needs to know how many you have used, so the state grows to (i, k).
  That is what happens in [[knapsack]].
- **The groups do not overlap.** For a max it would not matter if a set were in
  both groups; it would just be offered twice. For a **count** it matters: a
  counting DP adds the groups, and an object in both is counted twice. The
  counting variations below need cases that are disjoint, not just complete.
- **The objective adds up, and max respects it.** "Best of the rest, plus x_i" is
  only right because a better rest is a better whole. For an average, a ratio, or a
  product with negative numbers, that is false, and the state needs more
  information (maximum product subarray keeps both the largest and the smallest).
- **Every arrow points to a smaller index.** That is what made the loop order
  legal. If a transition could point to the same or a larger state (a cycle), the
  recurrence would be an equation, not a definition, and you would need a shortest
  path algorithm such as [[bellman-ford]] instead of a loop.
- **The values are final when read.** This is a property of the code, not the
  maths, and the two-variable bug above is a violation of it.

## What it costs

**The brute force.** C(i) = 1 + C(i-1) + C(i-2) calls, which is about 1.618^n. Every
new house multiplies the work by 1.618.

**The DP.** The cost of every dynamic program is the same sentence:

> total time = (number of states) x (work per state)

because each state is computed once and every other visit is a lookup. House
Robber has n+1 states and each does a constant amount of work (two reads, an add,
a compare), so the time is O(n). The table uses O(n) space and the rolling version
O(1).

Apply the same sentence to the variations, and you get their costs without
memorising them:

| problem | states | work per state | time |
|---|---|---|---|
| house robber, climbing stairs | n | O(1) | O(n) |
| fewest coins, amount A, k coins | A + 1 | k | O(A·k) |
| decode ways | n + 1 | O(1) (two splits) | O(n) |
| word break, longest word L | n + 1 | L slices of length up to L | O(n·L²) |
| Kadane | n | O(1) | O(n) |
| LIS, the direct way | n | up to n | O(n²) |
| LIS, with the tails array | n | one binary search | O(n log n) |

**The costs people forget.**

- **The work inside a transition.** "n states, O(1) each" is often a lie. Word
  break with `s[j:i] in words` builds a new string of length i - j for every pair,
  so the honest per-state cost is the total length of the slices, not the number
  of them. A DP that slices, sorts, or builds a tuple inside the loop pays for it
  on every state.
- **The key.** A dictionary keyed by tuples hashes every component on every
  lookup. A list indexed by integers does not. At 10^6 states that difference is a
  timeout, and the O() hides it.
- **Recursion depth.** A memo over 10^5 positions is 10^5 nested calls; Python
  stops at about a thousand.
- **Pseudo-polynomial.** O(A·k) for coins looks polynomial, but A is a *number*, not
  a count of things in the input. If A doubles, the input grows by one bit and the
  work doubles. A constraint like `amount <= 10^4` is the problem setter telling you
  the intended state space; `amount <= 10^9` is telling you that the amount must
  not be an index. [[knapsack]] treats this properly.

## How to think about it

The template is short. What makes DP hard is choosing the state, and that is a
habit, not a memory. Ask these questions, in this order, on every new problem.

1. **What does the brute force look like as a sequence of decisions?** Write it
   in words: "at each house, rob or skip"; "at each position, the next letter uses
   one digit or two"; "for the next coin, which denomination". If you cannot write
   the brute force, you cannot write the DP.
2. **What is the last decision, and what are its cases?** The cases must cover
   every solution. For a count they must also not overlap.
3. **What is the least the future needs to know about the past?** That is the
   state. Usually it is "how far along I am" (an index) plus whatever else a rule
   needs: the last colour used, whether the previous city is covered, the amount
   left. Each extra fact is an extra dimension, so add only what a rule forces you
   to.
4. **Is the state "the first i elements" or "ending exactly at i"?** "First i"
   (a prefix) is right when the solution is any subset or split of the prefix:
   house robber, decode ways, word break, coins. "Ending at i" is right when the
   solution must be contiguous or must be extended by its last element: the best
   subarray (Kadane), the longest increasing subsequence. With "ending at i", the
   answer is the max over all i, not the last cell.
5. **What am I computing?** Max, min, a count, or yes/no. This decides the
   operation in the cell (max, min, +, or) and the value for "impossible" (-inf,
   +inf, 0, False). The value for "impossible" must never be confused with a real
   answer: 0 coins is a real answer for amount 0, and a wrong one for an amount you
   cannot make.
6. **What are the base cases?** The states with nothing before them: the empty
   prefix, the amount 0, the first element. Say what each means in words.
7. **In what order do the arrows point?** If every transition reads smaller
   indices, fill left to right. Check it explicitly for every new recurrence.
8. **Which cell is the answer, and can I keep less?** dp[n], or a max over all
   cells. If each cell reads only a fixed number of cells back, roll it into that
   many variables, and then watch the update order.

Then, before writing any code, write four lines: **the state in words**, **the
transition and why its cases are complete (and disjoint, for counts)**, **the base
cases**, and **the answer cell**. If you cannot write those four lines, you do not
have the solution yet, and code will not find it for you.

### Telling it from its neighbours

- **Greedy** ([[greedy]]). A greedy is a DP where one branch is always provably
  best, so the other branch never needs computing. If you can prove that (an
  exchange argument), use the greedy. If you cannot, try a counterexample with
  three elements first; the ones in this chapter took three houses and three coins.
- **Divide and conquer** ([[divide-and-conquer]]). The same "solve smaller
  problems" shape, with subproblems that do not repeat. If your recursion tree has
  no repeated label, memoising buys nothing.
- **Backtracking** ([[backtracking]]). Explores the same tree, but keeps the path,
  because it must output the solutions themselves. DP throws the path away and
  keeps only the state, which is why it can count or optimise but cannot list.
- **Knapsack** ([[knapsack]]). One-dimensional DP whose state needs a second
  number, a shared resource such as capacity. The tell is a limit that all
  choices draw from.
- **Two-dimensional DP** ([[dp-2d]]). When the state is two positions: a cell in a
  grid, or a position in each of two strings.
- **Shortest paths** ([[shortest-path]]). DP on a graph whose arrows can form a
  cycle. Without cycles, the two are the same thing.

## Variations

Each variation below is the same four answers (state, transition, base, order)
with something changed. Each says what changes, why, a small example you can
check, and problems from this bank that teach it. A to F are the everyday core of
interviews and online assessments. G is common in interviews. H is rare outside
competitive programming, and is here so you recognise it.

### A. Recursion, then memo, then table: climbing stairs

**What changes.** Nothing is optimised; the question is "how many ways". You climb
n steps, one or two at a time. The last move was a 1-step (from n-1) or a 2-step
(from n-2), so ways(n) = ways(n-1) + ways(n-2), with ways(0) = 1 (one way to climb
nothing: do nothing) and ways(1) = 1.

**Why.** The last move splits every sequence into two groups that do not overlap
(a sequence ends in 1 or in 2, never both), so the counts add. The recursion tree
is exactly the House Robber tree: f(n) calls f(n-1) and f(n-2). Same waste, same
cure, same two-variable loop. House Robber is climbing stairs with a max where this
has a plus.

**Example.** n = 4: ways are 1, 1, 2, 3, 5 for n = 0..4. The five sequences are
1111, 112, 121, 211, 22. With steps of 1, 2 or 3, ways(n) = ways(n-1) + ways(n-2) +
ways(n-3): 1, 1, 2, 4, 7.

**Bank.** [[p:expedia-climbing-stairs|Climbing Stairs]] is the warm-up; derive it
three ways (recursion, memo, two variables) and count the calls.
[[p:agoda-climbing-stairs-one-two-three|Climb Stairs with One, Two, or Three Steps]]
widens the window to three. [[p:jpmorgan-fibonacci-number|Fibonacci Number]] is the
same recurrence with different base cases.

### B. Take or skip on a line: the House Robber family

**What changes.** The main example of this chapter. The variations keep the line
and change the rule about neighbours, which changes the state.

- **A circle.** The first and last houses are neighbours. Solve two lines: houses
  1..n-1, and houses 2..n, and take the better. Every legal circular choice misses
  house 1 or house n (it cannot contain both), so one of the two lines contains it.
  [[p:digitalocean-house-robber-ii|Maximum Value from Circular Houses]]. On 2, 3, 2
  the line answer is 4 (both 2s), the circle answer is 3.
- **A disguise.** "Take x, and every x-1 and x+1 disappears" looks like nothing
  of the sort. Bucket by value: total[v] = v times the count of v. Taking value v
  forbids v-1 and v+1, which are its neighbours on the number line. That is House
  Robber on the array total[0..max].
  [[p:morgan-stanley-delete-and-earn|Delete and Earn]]: [2, 2, 3, 3, 3, 4] becomes
  total = [0, 0, 4, 9, 4], and robbing gives max(4 + 4, 9) = 9.
- **A small extra state.** When the rule is "neighbours must differ" instead of
  "neighbours cannot both be taken", the future needs to know the previous choice.
  [[p:shopify-paint-house|Paint House]]: best[i][c] = the cheapest way to paint the
  first i houses with house i painted colour c, and best[i][c] = cost[i][c] +
  min(best[i-1][d] for d != c). The state is (position, last colour): still a line,
  with three numbers per position instead of one.
- **An Amazon OA story.** [[p:amazon-maximize-protected-city-population|Maximize Protected City Population]]
  lets each unit stay or move one city left. Scan left to right; each unit's
  decision is stay or move, and the state records whether the previous city is
  already protected. It is a two-state line DP of exactly this kind (on the sample,
  populations 10, 5, 8, 9, 6 with units in cities 2, 3, 5, the best is 27).

**Why.** All of these are the same question, "what is the least the future needs
to know?", with a different answer: nothing beyond the index (robber), the index
plus the last colour (paint house), the index plus a coverage flag (cities).

### C. The minimum cost to reach a target: frog jump and fewest coins

**What changes.** The cell holds a minimum. The base is the start (cost 0), and
everything you cannot reach yet is +infinity, not 0.

**Frog jump.** From stone i you jump to i+1 or i+2, paying the height difference.
cost[i] = min(cost[i-1] + |h[i] - h[i-1]|, cost[i-2] + |h[i] - h[i-2]|). It is
climbing stairs with a min and a price on each arrow.
[[p:mygate-frog-jump|Frog Jump: Minimum Energy]]. Heights 10, 30, 40, 20: costs
0, 20, 30, 30. The cheapest way to the last stone is 10, 30, 20, paying 20 + 10;
going through the 40 would pay 30 + 20 = 50.

**Fewest coins.** coins = {1, 3, 4}, amount 6, unlimited coins. The last coin used
was 1, 3 or 4, so best[a] = 1 + min(best[a-1], best[a-3], best[a-4]), skipping
coins larger than a, with best[0] = 0.

| a | via 1 | via 3 | via 4 | best[a] |
|---|---|---|---|---|
| 0 | | | | 0 |
| 1 | 0+1 | | | 1 |
| 2 | 1+1 | | | 2 |
| 3 | 2+1 | 0+1 | | 1 |
| 4 | 1+1 | 1+1 | 0+1 | 1 |
| 5 | 1+1 | 2+1 | 1+1 | 2 |
| 6 | 2+1 | **1+1** | 2+1 | **2** |

"Take the largest coin that fits" takes 4, then 1, then 1: three coins. The table
says 3 + 3: two coins. The greedy commits to the biggest first step; the table
compares the consequences of every first step, which is exactly what the greedy
refuses to do. [[p:amd-minimum-coin-change|Minimum Coins for an Amount]] asks for
-1 when the amount cannot be made, which is why the start must be infinity.

**A weighted window.** [[p:microsoft-minimum-jump-cost|Minimum Jump Cost]]: jumps
of length up to k, cost[i] = c[i] + min of the previous k costs. Direct, that is
O(n·k); variation H makes it O(n).

**Why.** Coins are unlimited, so "amount left" is the whole state: which coins were
already used does not change what you may use next. If each coin could be used
only once, the state would also need "which coins are still allowed", and that is
[[knapsack]]. The unlimited form has its own chapter, [[unbounded-knapsack]].

### D. Count the ways: decode ways

**What changes.** The cell holds a count, the max becomes a sum, and the cases must
not overlap. The base is 1 for the empty prefix: there is exactly one way to decode
nothing.

**Decode ways.** A digit string, 1 = A, ..., 26 = Z. The last letter of a decoding
used either the last digit alone or the last two digits. So

```
ways[i] = (ways[i-1]  if s[i-1] is 1..9)
        + (ways[i-2]  if s[i-2:i] is 10..26)
ways[0] = 1
```

The two cases cannot overlap (a decoding's last letter has one length), so adding
is safe.

**Example.** "226": ways = 1, 1, 2, 3. The decodings are 2 2 6, 22 6, 2 26. "2101":
ways[1] = 1 ("2"); ways[2]: "1" alone gives ways[1] = 1, "21" gives ways[0] = 1,
total 2; ways[3]: "0" alone is invalid, "10" gives ways[1] = 1, so 1; ways[4]: "1"
gives ways[3] = 1, "01" is invalid (leading zero), so 1. One decoding: 2 10 1.

The zeros are where everyone loses points. A "0" can only be the second digit of
10 or 20. "06" is not 6. "30" has no decoding at all, and the code must return 0,
not crash and not return 1.

**Bank.** [[p:de-shaw-decode-ways|Decode Ways]] is the classic.
[[p:squadstack-weighted-decode-ways|Minimum-Cost Digit String Decoding]] keeps the
same two splits and asks for the cheapest decoding: the plus becomes a min, the 1
becomes 0, and the 0 for "impossible" becomes infinity. Same skeleton, different
operation; seeing them side by side is the best way to learn which parts are the
method and which are the problem.
[[p:atlassian-dice-roll-simulation|Dice Roll Simulation]] is a stretch: the state
needs the last face and how many times in a row it has appeared, and the count is
modulo 10^9 + 7. [[counting-dp]] treats counting properly.

### E. DP over prefixes with a dictionary: word break

**What changes.** The number of cases per state is not fixed. ok[i] is true when
the first i characters can be split into dictionary words. The last word of such a
split ends at i and starts at some j, so

```
ok[i] = any( ok[j] and s[j:i] in words  for j in 0..i-1 )
ok[0] = True
```

**Why.** The future after position j does not care how the first j characters were
split, only *that* they were. So "j characters done" is the state, and the last
word is the decision.

**Example.** s = "applepenapple", words = {apple, pen}. ok[5] (apple), ok[8]
(apple + pen), ok[13] (ok[8] and "apple"): True. s = "catsandog", words = {cats,
dog, sand, and, cat}: ok[3], ok[4], ok[7] are true, but no word ends at 9 starting
at a true position ("og", "dog" from 6 where ok[6] is false), so False.

**Cost.** Only words up to the longest length L can match, so try j from i-L to i-1:
n·L slices of length up to L. With a set of words, O(n·L²).

**Bank.** [[p:meta-word-break-reusable-dictionary|Word Break with a Reusable Dictionary]].
Note the boundary: [[p:amazon-word-break-ii|Word Break II]] asks for every
sentence, which can be exponentially many; the DP can tell you which positions are
worth exploring, but listing is [[backtracking]].

### F. Kadane: the best subarray ending here

**What changes.** The answer must be contiguous, so "the best within the first i"
is the wrong state. Why: knowing the best subarray *somewhere* in the first i
elements tells you nothing about whether element i+1 can extend it, because that
subarray might not end at i. The state must be "the best subarray that **ends
exactly at i**". Then the last decision is: does the subarray ending at i also
contain i-1, or does it start fresh at i?

```
end[i] = max(x[i], end[i-1] + x[i])      extend, or restart
answer = max over all i of end[i]
```

Say it a second way: if the best run ending at i-1 is negative, it can only hurt
whatever comes next, so drop it and start again.

**Example.** -2, 1, -3, 4, -1, 2, 1, -5, 4. end = -2, 1, -2, 4, 3, 5, 6, 1, 5. The
best is 6 (4, -1, 2, 1). Note that end[8] = 5 is not the answer; the answer is the
max over all cells, because the definition says "ends at i".

**Bank.** [[p:omnissa-maximum-subarray-sum|Maximum Subarray Sum]], which insists on
at least one element even when all are negative (the trap below).
[[p:jpmorgan-best-time-to-buy-and-sell-stock|Best Time to Buy and Sell Stock]] is
the same shape: the best sale on day i is price[i] minus the lowest price before
it, and that lowest price is a one-number state carried along.
[[p:google-maximum-product-subarray|Maximum Product Subarray]] breaks the "a better
part is a better whole" assumption: a very negative product can become the best
after one more negative number, so the state keeps both the largest and the
smallest product ending at i. The full chapter is [[kadane]].

### G. The longest increasing subsequence

**What changes.** A subsequence may skip elements, but its last element decides
what can come next: only something larger. So the state is "ending at i" again:
lis[i] = the length of the longest strictly increasing subsequence that ends at
element i.

```
lis[i] = 1 + max( lis[j]  for j < i with x[j] < x[i] ),   or 1 if there is none
answer = max over all i of lis[i]
```

**Example.** 3, 1, 4, 1, 5, 9, 2, 6. lis = 1, 1, 2, 1, 3, 4, 2, 4. The answer is 4,
for example 1, 4, 5, 9 or 3, 4, 5, 6. Element 9 has lis 4 because 5 before it has
lis 3; element 2 has lis 2 because only the 1s are smaller.

**The speed-up.** The direct DP is O(n²): every i looks at every j before it. The
faster version keeps an array tails, where tails[k] is the smallest possible last
element of an increasing subsequence of length k+1 seen so far. Smaller tails are
better, because more future elements can extend them. Each new x replaces the first
tail that is >= x (found by binary search), or is appended if x beats them all.
The length of tails is the answer.

On 3, 1, 4, 1, 5, 9, 2, 6: [3], [1], [1, 4], [1, 4], [1, 4, 5], [1, 4, 5, 9],
[1, 2, 5, 9], [1, 2, 5, 6]. Length 4. Note that [1, 2, 5, 6] is not a subsequence
of the input in that order of discovery (the 2 came after the 9); tails is a list
of best endings per length, not a solution. To recover a real subsequence, store a
parent pointer per element.

The one subtle line is `bisect_left` versus `bisect_right`. Strictly increasing
uses `bisect_left`: an equal element replaces its equal, so equal values never
extend each other. `bisect_right` puts it after its equal and computes the longest
**non-decreasing** subsequence. On 1, 2, 2, 3 the first gives 3 and the second 4.
The Traps block shows it.

**Bank.** [[p:salesforce-longest-increasing-subsequence|Longest Increasing Subsequence]]:
derive the O(n²) table, then the tails array.
[[p:squarepoint-longest-subsequence-from-two-arrays|Longest Increasing Subsequence from Two Arrays]]
offers two values per index; both are tried against tails as it was before the
index, so the two values do not chain into each other (the same "read the old
state" rule as the two-variable bug).
[[p:google-russian-doll-envelopes|Russian Doll Envelopes]] sorts by one dimension
and runs LIS on the other. The full chapter is [[lis]].

### H. Making the transition cheaper (rare)

When states × work per state is too big, the states are usually fine and the
transition is the problem. The inner min or max is a query over a structured set
of earlier states, so answer it with a data structure instead of a loop.

- **A sliding window of states: monotonic deque.** cost[i] = c[i] + min(cost[i-k
  .. i-1]). Keep the indices of the window in a deque with increasing cost; the
  front is the minimum. Each index enters and leaves once, so O(n·k) becomes O(n).
  [[p:microsoft-minimum-jump-cost|Minimum Jump Cost]] is exactly this; see
  [[monotonic-deque]], and the run block below.
- **Lines: the convex hull trick.** dp[i] = min over j of (dp[j] + b_j · x_i). Each j
  is a line y = b_j·x + dp[j], and the query asks for the lowest line at x_i, a point
  on the lower envelope of the lines. Maintaining the envelope makes O(n²) into
  O(n log n), or O(n) when slopes and queries are sorted. It is a
  [[convex-hull]] in disguise. Rare in interviews; recognise the form and move on.
- **"The best over earlier states with a smaller key": a tree.** LIS variants with
  extra conditions use a [[segment-tree]] or [[fenwick-tree]] keyed by value.
- **A huge index with a linear recurrence: matrix power.** ways(n) for n = 10^18
  steps is a 2 x 2 matrix raised to the n-th power, O(log n) multiplications. See
  [[matrix-exponentiation]].

```python run
from collections import deque
import random

def by_scan(c, k):                    # cost[i] = c[i] + min(cost[i-k .. i-1]); cost[0] = 0
    n, ops = len(c), 0
    cost = [0] + [0] * n
    for i in range(1, n + 1):
        lo = max(0, i - k)
        ops += i - lo
        cost[i] = c[i - 1] + min(cost[lo:i])
    return cost[n], ops

def by_deque(c, k):
    n, ops = len(c), 0
    cost = [0] * (n + 1)
    dq = deque([0])                   # indices, cost increasing from front to back
    for i in range(1, n + 1):
        while dq[0] < i - k:          # fell out of the window
            dq.popleft(); ops += 1
        cost[i] = c[i - 1] + cost[dq[0]]
        while dq and cost[dq[-1]] >= cost[i]:
            dq.pop(); ops += 1        # never better again: older and not cheaper
        dq.append(i); ops += 1
    return cost[n], ops

print("points cost 3 1 4 1 5, k=2:", by_scan([3, 1, 4, 1, 5], 2)[0])
assert by_scan([3, 1, 4, 1, 5], 2)[0] == by_deque([3, 1, 4, 1, 5], 2)[0] == 7
rng = random.Random(5)
for _ in range(300):
    c = [rng.randint(0, 20) for _ in range(rng.randint(1, 25))]
    k = rng.randint(1, 6)
    assert by_scan(c, k)[0] == by_deque(c, k)[0]
big = [rng.randint(0, 1000) for _ in range(3000)]
(a, o1), (b, o2) = by_scan(big, 500), by_deque(big, 500)
print("n=3000, k=500: scan steps", o1, " deque steps", o2)
assert a == b and o2 * 50 < o1
```

On 3, 1, 4, 1, 5 with jumps of at most 2: land on the 1, the 1 and the 5, total 7.
On 3,000 points with k = 500, the deque does a few thousand steps against about a
million and a half.

### Where one dimension runs out

Two shapes need more than one index, and they are the next chapters.

- **A shared resource.** "Choose items, each at most once, total weight at most W."
  The future needs to know which items are left *and* how much room is left: the
  state is (i, c). That is [[knapsack]], and it is the natural next chapter: the
  same take-or-skip as House Robber, with the room as a second index.
- **Two positions.** A grid, or two strings to compare. The state is (row, column)
  or (position in the first string, position in the second): [[dp-2d]].

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"Return the number of ways ...", especially "modulo 10^9 + 7".** The modulus
   exists because the count is astronomical, so nobody expects you to list. Count
   with DP: climbing stairs, decode ways, dice sequences.
2. **"Minimum cost / maximum value" over a sequence of choices where one choice
   restricts the next.** No two adjacent, neighbours differ, a jump of at most k:
   House Robber, Paint House, Frog Jump.
3. **"Fewest X to make exactly Y" with unlimited X.** Coins, perfect squares,
   stamps: minimum cost to reach a target, indexed by the target.
4. **"Can the string be split / decoded / segmented ..."** A prefix DP: the state
   is how many characters are done.
5. **"Contiguous subarray" with "maximum sum / product / profit".** Kadane: the
   state ends at i.
6. **"Subsequence" and "increasing" (or "chain", "nested", "stack boxes").** LIS,
   possibly after sorting.
7. **A brute force you can describe as "try every choice at every step", and an
   argument list that is short.** Write that recursion. If its arguments repeat,
   you already have the state.

**Disguised forms.**

- **"Pick numbers; picking x deletes every x-1 and x+1."** Bucket by value, and it
  is House Robber on the number line (variation B).
- **"A circle of ..."** with a neighbour rule: two lines, drop one end each.
- **"Best time to buy and sell once."** Kadane on day-to-day differences, or a
  running minimum: the same one-number state.
- **"Minimum number of perfect squares that sum to n."** Fewest coins, where the
  coins are 1, 4, 9, 16, ...
- **"Longest chain of pairs / nested envelopes."** Sort, then LIS.

**Anti-signals: looks like DP, is not.**

- **A provably safe local rule.** Meeting rooms by earliest end, coins for an
  ordinary currency: [[greedy]]. Prove it or break it with a three-element
  example.
- **"Return all ..."**: [[backtracking]]. DP can count them or find one.
- **Subarray *sums equal to k* (counting).** That is [[prefix-sums]] with a hash
  map, not Kadane; there is no max to take.
- **Shortest path with moves in every direction.** Arrows form cycles, so no fill
  order exists: [[bfs]] for unit steps, [[dijkstra]] for weights.
- **n <= 20 and a complicated rule.** Enumerate the 2^n choices directly.

## Traps

**1. Using the transition of one definition and the answer of another.** Symptom:
right on most tests, wrong when the best answer does not touch the last element.
"Ends at i" needs a max over all i. "First i" reads dp[n]. Write the sentence.

**2. Overwriting a value before you read it.** Symptom: the two-variable House
Robber returns the sum of all houses. Use tuple assignment or a temporary. This is
the demonstration in "From the idea to the code", and the same bug appears in
every rolled DP.

**3. "Impossible" initialised as 0.** Symptom: fewest coins returns 0 for an amount
that cannot be made, or a too-small number that secretly builds on an impossible
amount. 0 means "possible, at no cost". Start every unreachable state at infinity,
and turn infinity into -1 only at the end.

**4. Kadane's best starting at 0.** Symptom: an all-negative array returns 0, the
empty subarray, which the problem forbids. Start best at the first element (or at
-infinity) and let end[0] = x[0].

**5. Zeros in decode ways.** Symptom: "10" returns 2, or "30" returns 1, or "06"
returns 1. A one-digit code must be 1..9; a two-digit code must be 10..26, which
excludes a leading zero.

**6. bisect_right in a strict LIS.** Symptom: answers one too long on inputs with
repeated values. Strict uses bisect_left.

**7. A memo key that includes the running total.** Symptom: a memo that is correct
and still exponential. f(i, money_so_far) almost never sees the same pair twice,
so the cache never hits. The money collected so far is not something the future
needs; leave it out of the state and add it on the way back.

**8. A memo that recurses 10^5 deep.** Symptom: `RecursionError`. Use the table.

The third to sixth traps, run:

```python run
from bisect import bisect_left, bisect_right
INF = float("inf")

def coins_wrong(coins, amount):          # unreachable starts at 0
    best = [0] * (amount + 1)
    for a in range(1, amount + 1):
        best[a] = 1 + min((best[a - c] for c in coins if c <= a), default=0)
    return best[amount]

def coins_right(coins, amount):
    best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return best[amount] if best[amount] < INF else -1

print("coins {2}, amount 3: wrong", coins_wrong([2], 3), " right", coins_right([2], 3))
assert coins_wrong([2], 3) == 2 and coins_right([2], 3) == -1   # 3 is odd: impossible
assert coins_right([1, 3, 4], 6) == 2

def kadane(x, best_start):
    end, best = 0, best_start
    for v in x:
        end = max(v, end + v)            # extend or restart
        best = max(best, end)
    return best

print("all negative [-3, -1, -2]: best=0 start ->", kadane([-3, -1, -2], 0),
      " best=-inf start ->", kadane([-3, -1, -2], -INF))
assert kadane([-3, -1, -2], 0) == 0 and kadane([-3, -1, -2], -INF) == -1
assert kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4], -INF) == 6

def decode(s):
    ways = [1] + [0] * len(s)
    for i in range(1, len(s) + 1):
        if s[i - 1] != "0":
            ways[i] += ways[i - 1]                   # last letter: one digit
        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
            ways[i] += ways[i - 2]                   # last letter: two digits
    return ways[-1]

for s, want in [("226", 3), ("2101", 1), ("10", 1), ("30", 0), ("06", 0), ("11106", 2)]:
    assert decode(s) == want, s
print("decode ways: 226 ->", decode("226"), " 30 ->", decode("30"), " 06 ->", decode("06"))

def lis(x, bis):
    tails = []
    for v in x:
        k = bis(tails, v)
        if k == len(tails):
            tails.append(v)
        else:
            tails[k] = v
    return len(tails)

print("1 2 2 3: bisect_left", lis([1, 2, 2, 3], bisect_left),
      " bisect_right", lis([1, 2, 2, 3], bisect_right))
assert lis([1, 2, 2, 3], bisect_left) == 3      # strictly increasing: 1 2 3
assert lis([1, 2, 2, 3], bisect_right) == 4     # non-decreasing: 1 2 2 3
assert lis([3, 1, 4, 1, 5, 9, 2, 6], bisect_left) == 4
```

Look at the first line of output. With coins {2} and amount 3, the zero-started
table says 2: it built best[3] = 1 + best[1], and best[1] was 1 + "nothing", a 0
that meant "impossible" and was read as "free". The infinity version says -1.

## What to memorise

The procedure, not a template, because the state is different every time:

1. **State**, in one sentence: what dp[i] means. "First i" or "ends at i".
2. **Transition**: the last decision and its cases (complete; disjoint for counts).
3. **Base cases**: the empty prefix, the amount 0, the first element.
4. **Order and answer**: arrows point to smaller indices, so fill upward; dp[n] or
   a max over all cells.

The House Robber skeleton, which is most of the chapter in five lines:

```python
prev2, prev1 = 0, 0                      # dp[i-2], dp[i-1]
for v in x:
    prev2, prev1 = prev1, max(prev1,     # skip
                              prev2 + v) # take: jump the neighbour
answer = prev1
```

The question that finds the state: **what is the least the future needs to know
about the past?**

The sentence that proves it: **take an optimal solution, delete its last decision,
and what remains is an optimal solution to a smaller state.**

The habit: before typing, say what "impossible" is (-inf, +inf, 0, False) and make
sure it can never be mistaken for a real answer.

The numbers: states × work per state. Up to a few million is comfortable in Python;
10^8 is not. A recursion deeper than about a thousand needs the table.

## Check yourself

:::check
Hand trace. Houses 5, 3, 4, 11, 2. Fill dp[0..5], and for each cell write the skip
and rob values you compared. Walk back to find the houses. Then run the wrong
two-variable loop (prev2 overwritten first) and say what it returns and why.
--
| i | house | skip | rob | dp[i] |
|---|---|---|---|---|
| 0 | | | | 0 |
| 1 | 5 | 0 | 5 + 0 = 5 | 5 |
| 2 | 3 | 5 | 3 + 0 = 3 | 5 |
| 3 | 4 | 5 | 4 + 5 = 9 | 9 |
| 4 | 11 | 9 | 11 + 5 = 16 | 16 |
| 5 | 2 | 16 | 2 + 9 = 11 | 16 |

Walk back: dp[5] = 16 equals dp[4], so house 5 is skipped; step to dp[4]. dp[4] =
16 differs from dp[3] = 9, so house 4 (11) is robbed; jump to dp[2]. dp[2] = 5
equals dp[1], house 2 skipped; step to dp[1]. dp[1] = 5 differs from dp[0], house 1
robbed. Houses 1 and 4: 5 + 11 = 16. Houses 2 and 3 are both skipped, two in a row.

The wrong loop returns 5 + 3 + 4 + 11 + 2 = 25, the sum of every house, because
after `prev2 = prev1` the rob branch adds each house to a plan that may already
contain its neighbour.
:::

:::check
Hand trace. Coins {1, 5, 6, 9}, amount 11, unlimited supply, fewest coins. Fill
best[0..11]. What does "take the largest coin that fits" give, and where in the
table can you see it lose?
--
best = 0, 1, 2, 3, 4, 1, 1, 2, 3, 1, 2, 2 for amounts 0..11.

For example best[7] = min(best[6] + 1, best[2] + 1, best[1] + 1) = 2 (6 + 1);
best[8] = min(best[7] + 1, best[3] + 1, best[2] + 1) = 3; best[10] =
min(best[9] + 1, best[5] + 1, best[4] + 1, best[1] + 1) = 2; best[11] =
min(best[10] + 1, best[6] + 1, best[5] + 1, best[2] + 1) = 2, via 5 + 6.

The greedy takes 9, then 1, then 1: three coins. In the table, the 9 branch of
best[11] is best[2] + 1 = 3, and the 6 branch is best[5] + 1 = 2. The greedy only
ever looks at the 9 branch.
:::

:::check
Hand trace. Decode "11106". Fill ways[0..5], saying for each position whether the
one-digit and the two-digit split are valid. List the decodings.
--
ways[0] = 1. ways[1]: "1" valid, so 1. ways[2]: "1" valid (ways[1] = 1), "11" valid
(ways[0] = 1), so 2. ways[3]: "1" valid (2), "11" valid (1), so 3. ways[4]: "0"
alone is invalid, "10" valid (ways[2] = 2), so 2. ways[5]: "6" valid (ways[4] = 2),
"06" invalid (leading zero), so 2.

The two decodings: 1 1 10 6 (AAJF) and 11 10 6 (KJF). The 0 forced "10" to stay
together, which is why ways[4] dropped from 3 to 2.
:::

:::check
Hand trace. Run the tails array on 0, 8, 4, 12, 2, 10, 6, 14, 1, 9, writing tails
after each element. What is the LIS length? Is the final tails array an increasing
subsequence of the input? Then fill the O(n²) lis[i] for the same input and check
it agrees.
--
tails: [0], [0, 8], [0, 4], [0, 4, 12], [0, 2, 12], [0, 2, 10], [0, 2, 6],
[0, 2, 6, 14], [0, 1, 6, 14], [0, 1, 6, 9]. Length 4.

[0, 1, 6, 9] is not a subsequence of the input: the 1 comes after the 6. Each entry
is only the smallest ending seen so far for that length. A real LIS of length 4 is
0, 4, 6, 9 or 0, 8, 12, 14.

lis = 1, 2, 2, 3, 2, 3, 3, 4, 2, 4. The maximum is 4, as expected.
:::

:::check
Why must Kadane's state be "the best subarray ending exactly at i", when House
Robber's state can be "the best within the first i"? Give an input where a
"best within the first i" recurrence for subarrays goes wrong.
--
Because a subarray must be contiguous. To extend a subarray with element i+1, it
has to end at element i. "The best subarray within the first i" may end anywhere,
so it says nothing about whether element i+1 can be attached. House Robber's sets
may skip elements, so any legal set of the first i-2 houses can have house i added.

Try best[i] = max(best[i-1], best[i-1] + x[i]) on 5, -10, 5. best = 5, 5, 10: it
"extends" the subarray [5] with a later 5 across the -10, which is not
contiguous. The true answer is 5. Kadane's end = 5, -5, 5 and the max over all is
5.
:::

:::check
Someone memoises House Robber as f(i, collected), where collected is the money so
far, and says "it is memoised, so it is O(n)". Where are they wrong?
--
The memo is correct, but almost never hits. Two different histories that reach
the same i almost always have different collected amounts, so (i, collected) is a
new key nearly every time, and the run stays exponential.

The collected amount is not something the future needs: the best future from i is
the same whatever is already in the bag. The fix is to leave it out of the state
and return "the best I can add from here", adding each house's money on the way
back up. The count of distinct keys is the cost; count them before blaming Python.
:::

:::check
Someone says "fewest coins is a greedy: always take the largest coin that fits. It
works for 1, 5, 10, 25." Where are they wrong, and what is the smallest coin set
that shows it?
--
It works for some coin sets (those called canonical, which ordinary currencies are
designed to be) and fails for others. Passing on 1, 5, 10, 25 proves nothing about
other inputs.

Coins {1, 3, 4}, amount 6: greedy takes 4, 1, 1, three coins; the best is 3 + 3,
two. The DP compares the consequences of every first coin (best[5], best[3],
best[2]), and the greedy only looks at one of them.
:::

:::check
Reduce this disguised problem. "nums = [3, 4, 2, 3, 3]. Repeatedly pick an element
x, earn x points, and delete every element equal to x-1 or x+1. Maximise the
points." Name the technique, build the array it runs on, and give the answer.
--
Bucket by value: earning from one x and then picking the remaining copies of x
costs nothing extra, so take all copies of a value or none. total[v] = v x
count(v): total[2] = 2, total[3] = 9, total[4] = 4, so the array over values 0..4
is [0, 0, 2, 9, 4].

Taking value v forbids v-1 and v+1: neighbours on the number line. That is House
Robber on [0, 0, 2, 9, 4]: dp = 0, 0, 0, 2, 9, 9 (for 4: skip 9, rob 4 + 2 = 6).
Answer 9: take the three 3s, which deletes the 2 and the 4.
:::
