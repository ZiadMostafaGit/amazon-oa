# Greedy Algorithms

> A greedy algorithm is a recursion in which one branch provably always wins, so you take that branch and never explore the others; the whole skill is finding the choice you can prove you will never regret.

## The problem it solves

You are given a list of meetings, each with a start and an end time, and one room.
Some meetings overlap. You must cancel some so that no two of the survivors
overlap; a meeting that ends at 3 and one that starts at 3 do not overlap. What is
the fewest you can cancel? That is
[[p:bytedance-minimum-interval-removals|Minimum Interval Removals]] as this bank
states it, with up to 100,000 intervals.

Cancelling the fewest is the same as keeping the most, so the real question is:
**what is the largest set of intervals that pairwise do not overlap?** Take these
six:

| name | start | end |
|---|---|---|
| p | 1 | 4 |
| q | 2 | 3 |
| r | 3 | 5 |
| s | 0 | 6 |
| t | 5 | 7 |
| u | 4 | 8 |

The best you can keep is three, q (2,3), r (3,5) and t (5,7), so the answer is
"cancel three".

The first solution anyone writes is to try every subset. Six intervals have
2^6 = 64 subsets. Check each for overlaps, keep the largest legal one. Correct, and
for six intervals fine. For 100,000 intervals it is 2^100000 subsets, a number with
about 30,000 digits.

The second solution anyone writes is a rule: "sort by something, then take each
interval if it still fits". That is a greedy algorithm, and it can be exactly
right, in O(n log n), or plausibly wrong, depending entirely on the "something".
Sort by start time and take what fits: you take s (0,6) first, the room is busy
until 6, and no other interval starts at 6 or later. You keep one interval. Sort by length and take what fits: q (length 1), then r (2), then t (2),
which happens to give three here, and we will break it with three intervals in a
moment. Sort by **end** time and take what fits: always optimal, and this chapter
derives why rather than asserting it.

Greedy is the sixth most common topic in this bank: 1,089 problems use it. Most of
them are short to code and the difficulty is all in choosing the rule and knowing it
is right. That is what the chapter is about.

### When it is the wrong tool

- **The items carry values or weights, and there is a budget.** Give each meeting a
  profit and maximise the total profit: now three cheap meetings can lose to one
  valuable one, and no sort order fixes that. That is weighted interval scheduling,
  a [[dp-1d|DP]]. Knapsack is the same story ([[knapsack]]).
- **The coins, costs or rules are arbitrary.** "Fewest coins to make an amount" is
  greedy for real currency and wrong for coins `[1, 3, 4]` and amount 6 (greedy pays
  4 + 1 + 1, the best is 3 + 3).
  [[p:amd-minimum-coin-change|Minimum Coin Change]] gives you arbitrary coins, so it
  is a DP.
- **You must count the ways.** Greedy finds one best answer; counting is
  [[counting-dp]] or [[combinatorics]].
- **A choice now changes what later choices are worth, in a way one number cannot
  describe.** Then the state of the problem is bigger than a greedy can carry, and
  you need [[dynamic-programming]].

## Build it from the brute force

We will start from the slowest correct program, make it faster the way the
[[knapsack]] chapter did, and then notice something knapsack does not have: one of
the branches always wins. The greedy is what is left when you delete the branches
that never win.

### Step 1: one decision at a time

Sort the intervals by start time, so a kept set is always listed left to right.
Then a set is legal exactly when each kept interval starts at or after the end of
the previous kept one. Walk the list and decide, for each interval, keep or skip.

> f(i, last) = the most intervals I can still keep from intervals i..n-1, if the
> room is busy until time `last`.

```
f(i, last) = f(i+1, last)                         skip interval i
f(i, last) = max(that, 1 + f(i+1, end_i))         keep it, only if start_i >= last
f(n, last) = 0                                    no intervals left
```

This is the same take-or-skip recursion as knapsack. Each call makes up to two
calls, so it is up to 2^n calls, the subsets again.

### Step 2: remember answers

The state is (i, last), and `last` is always either "nothing yet" or the end of
some interval, so there are at most n(n+1) distinct states. Memoise them and the
cost drops from 2^n to about n^2. For n = 100,000 that is 10^10, still too slow,
but the memo has taught us what the state is: **one number, the time the room
becomes free.** Nothing else about the past matters. Which intervals you kept, how
many, in what order: the future does not care. It cares when the room is free.

### Step 3: ask the question a different way

Instead of "keep or skip interval i", ask "which interval do I keep *first*?" Let

> g(T) = the most intervals I can keep, using only intervals that start at or after
> time T.

The first kept interval x must start at or after T, and after it the room is free
from `end_x`, so

```
g(T) = max over every x with start_x >= T of  1 + g(end_x)
g(T) = 0 if no interval starts at or after T
```

This recursion has one branch per candidate, which looks worse than two. But look at
what the branches compare. Every branch adds 1 and then asks g of an end time. The
branches differ only in **which end time** they pass to g.

### Step 4: notice that one branch always wins

Here is the observation the whole chapter rests on. **g never gets bigger when T
gets bigger.** If the room is free from time 5, every plan that works from time 7
also works from time 5: the same intervals still start late enough. So having the
room free earlier can never hurt you: g(5) >= g(7).

Now go back to the max. Among the candidates x with `start_x >= T`, let m be the
one with the smallest end. For every other candidate y, `end_m <= end_y`, so
`g(end_m) >= g(end_y)`, so `1 + g(end_m) >= 1 + g(end_y)`. The branch through m is
at least as good as every other branch. You do not need to compute the others.

That is the greedy: **at each step, keep the interval that ends first among those
that still fit.** The max over n branches has collapsed to one branch, and the
recursion has become a loop.

### The question that unlocks it

The knapsack chapter's question was "what is the least the future needs to know
about the past?" Greedy asks that first (here: when the room is free), and then a
second, sharper question:

**Which choice can I prove I will never regret?**

"Never regret" has a precise meaning: there is an optimal solution that makes this
choice. If you can prove that, you can make the choice, shrink the problem, and ask
again. For interval selection the answer is "the interval that ends first", and the
proof is the four lines of Step 4: ending first leaves the room free earliest, and
free earlier is never worse.

Say it a second way. A DP explores every branch because it cannot tell which one
wins. A greedy is a DP where you *can* tell, in advance and for every state, which
branch wins. The proof that tells you is the algorithm. The code is a formality.

### You might think: "Take the shortest interval first. It wastes the least time."

Three intervals: (0,5), (4,6), (5,10). The shortest is (4,6), length 2. Take it, and
both others overlap it: you keep one. The best is (0,5) and (5,10): two.

Short is not what matters. What matters is how early the room becomes free, and a
short interval that starts late frees the room late. Length is a property of the
interval; "free from when" is the property of the **state**. A good greedy key is
made of the quantity the state is made of.

### You might think: "Take the one that starts first. Get going early."

Four intervals: (0,10), (1,2), (3,4), (5,6). The earliest start is (0,10). Take it,
and every other interval overlaps it: you keep one. The best is the other three.

Starting early is no use if you also end late. The rule looks at the wrong end of
the interval.

### You might think: "Take the one that conflicts with the fewest others."

This one is clever and survives many hand examples. It is still wrong. Eleven
intervals:

| interval | (0,3) | (0,4) | (1,2) | (1,3) | (2,6) | (4,8) | (7,10) | (8,11) | (9,11) | (10,13) | (10,14) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| conflicts | 4 | 4 | 3 | 4 | 4 | **2** | 3 | 4 | 4 | 3 | 3 |

(4,8) has the fewest conflicts, two: it overlaps only (2,6) and (7,10). So the rule
takes it, and that removes exactly the two "bridges" that a good solution needs. The
best is four: (1,2), (2,6), (7,10), (10,13). The fewest-conflicts rule keeps three,
however it breaks ties (the program in the Traps section checks every tie-break).

The lesson is not "this rule is bad". It is that **a rule that sounds reasonable
and passes small examples is the default outcome in this topic, and it is often
wrong.** The only defences are a proof like Step 4, or a brute-force comparison on
hundreds of small random inputs. Preferably both.

### You might think: "Greedy means: at each step, take the best-looking thing."

That is a description of every greedy, right and wrong ones alike. "Best-looking"
is not a rule until you say *best by what measure*, and the measure is the entire
algorithm. Shortest, earliest start, fewest conflicts and earliest end are all "the
best-looking thing" by some measure, and only one of them is correct. The question
is never "is this a greedy problem?" It is "is *this rule* never regretted?"

### The technique in one sentence

**A greedy algorithm finds a choice that some optimal solution always makes, proves
it (usually by showing the chosen option leaves the remaining problem no harder than
any other option would), makes it, and repeats on the smaller problem, so a
recursion with many branches becomes one pass with a single number of state.**

And the question: **which choice can I prove I will never regret?**

## Worked by hand

### Trace 1: earliest end on the six intervals

Sort by end: q (2,3), p (1,4), r (3,5), s (0,6), t (5,7), u (4,8). Keep an interval
when its start is at or after `last_end`, the time the room becomes free.

| step | interval | last_end before | start >= last_end? | action | kept |
|---|---|---|---|---|---|
| 1 | q (2,3) | none | yes | keep, last_end = 3 | 1 |
| 2 | p (1,4) | 3 | 1 < 3, no | skip | 1 |
| 3 | r (3,5) | 3 | 3 >= 3, yes | keep, last_end = 5 | 2 |
| 4 | s (0,6) | 5 | 0 < 5, no | skip | 2 |
| 5 | t (5,7) | 5 | 5 >= 5, yes | keep, last_end = 7 | 3 |
| 6 | u (4,8) | 7 | 4 < 7, no | skip | 3 |

Three kept, so three cancelled.

<svg viewBox="0 0 660 190" role="img" aria-label="six intervals drawn on a timeline from 0 to 8; the three kept by the earliest-end greedy, (2,3), (3,5) and (5,7), are shaded, and (1,4), (0,6) and (4,8) overlap them">
  <g>
    <line x1="40" y1="165" x2="620" y2="165"/>
    <text x="40" y="185">0</text>
    <text x="330" y="185">4</text>
    <text x="610" y="185">8</text>
    <rect class="fill" x="185" y="14" width="72" height="16" rx="6"/>
    <text x="270" y="27">q (2,3) kept</text>
    <rect x="113" y="42" width="217" height="16" rx="6"/>
    <text x="345" y="55">p (1,4) overlaps q</text>
    <rect class="fill" x="257" y="70" width="145" height="16" rx="6"/>
    <text x="415" y="83">r (3,5) kept</text>
    <rect x="40" y="98" width="362" height="16" rx="6"/>
    <text x="415" y="111">s (0,6) overlaps</text>
    <rect class="fill" x="402" y="126" width="145" height="16" rx="6"/>
    <text x="560" y="139">t (5,7) kept</text>
    <line x1="257" y1="8" x2="257" y2="170"/>
    <line x1="402" y1="64" x2="402" y2="170"/>
  </g>
</svg>

The story of step 3 in words: "The room is free from 3. The next interval in end
order is r, which starts at 3. Touching is allowed, so it fits. Every interval I
have not looked at yet ends at 5 or later, so none of them could free the room
sooner than r does. Keeping r leaves the room free from 5, which is the earliest any
choice could leave it."

Three things this trace shows that the code does not.

**The state is one number.** `last_end` is the entire memory of the algorithm.
Everything about steps 1 to 5 that could matter to step 6 is "the room is free from
7". When you cannot squeeze the past into one number like this, you probably do not
have a greedy.

**Skipping is never a decision.** At step 2, p is skipped because it does not fit,
not because it was judged worse. Every interval that fits is taken. All the
judgement is in the sort; the loop is mechanical.

**The proof is about the number kept, not the set.** Many optimal sets can exist;
which one comes back depends on how ties in the sort were broken. If a problem asks
for one specific optimal set (the lexicographically smallest, say), that needs a
separate argument.

### Trace 2: bending an optimal solution into the greedy one

The first trace showed the greedy working. This one shows *why*, on real numbers,
by taking a different optimal solution and turning it into the greedy's, one swap at
a time, without ever making it worse.

Six intervals: A (1,3), B (2,4), C (3,6), D (4,7), E (6,9), F (7,10). The greedy by
end keeps A (free from 3), skips B (starts 2), keeps C (starts 3, free from 6), skips
D (starts 4), keeps E (starts 6, free from 9), skips F (starts 7). Greedy: {A, C, E}.

Another optimal solution exists: {B, D, F}. B ends at 4, D starts at 4; D ends at 7,
F starts at 7. Also three. Line the two up, in end order, and repair the optimal one
from the left.

<svg viewBox="0 0 660 220" role="img" aria-label="three rows of three boxes: the optimal solution B D F, the greedy solution A C E, and after the first swap A D F; the first position where they differ is marked, and swapping B for A keeps the set legal and the same size">
  <g>
    <text x="10" y="35">OPT</text>
    <rect x="90" y="15" width="80" height="30" rx="4"/>
    <rect x="190" y="15" width="80" height="30" rx="4"/>
    <rect x="290" y="15" width="80" height="30" rx="4"/>
    <text x="130" y="35" text-anchor="middle">B (2,4)</text>
    <text x="230" y="35" text-anchor="middle">D (4,7)</text>
    <text x="330" y="35" text-anchor="middle">F (7,10)</text>
    <text x="10" y="95">GREEDY</text>
    <rect class="fill" x="90" y="75" width="80" height="30" rx="4"/>
    <rect class="fill" x="190" y="75" width="80" height="30" rx="4"/>
    <rect class="fill" x="290" y="75" width="80" height="30" rx="4"/>
    <text x="130" y="95" text-anchor="middle">A (1,3)</text>
    <text x="230" y="95" text-anchor="middle">C (3,6)</text>
    <text x="330" y="95" text-anchor="middle">E (6,9)</text>
    <line x1="130" y1="48" x2="130" y2="72"/>
    <text x="390" y="62">first difference: B vs A</text>
    <text x="390" y="80">A ends at 3, B at 4: A ends no later</text>
    <text x="10" y="175">OPT'</text>
    <rect class="fill" x="90" y="155" width="80" height="30" rx="4"/>
    <rect x="190" y="155" width="80" height="30" rx="4"/>
    <rect x="290" y="155" width="80" height="30" rx="4"/>
    <text x="130" y="175" text-anchor="middle">A (1,3)</text>
    <text x="230" y="175" text-anchor="middle">D (4,7)</text>
    <text x="330" y="175" text-anchor="middle">F (7,10)</text>
    <text x="390" y="168">D starts at 4 >= 3: still legal</text>
    <text x="390" y="186">still three intervals</text>
  </g>
</svg>

| round | current optimal set | first position that differs | greedy's choice there | why the swap is legal | after the swap |
|---|---|---|---|---|---|
| 1 | B, D, F | 1: B (2,4) | A (1,3) | A ends at 3 <= 4, and D starts at 4 >= 3 | A, D, F |
| 2 | A, D, F | 2: D (4,7) | C (3,6) | C starts at 3 >= 3 (after A), ends at 6 <= 7, F starts at 7 >= 6 | A, C, F |
| 3 | A, C, F | 3: F (7,10) | E (6,9) | E starts at 6 >= 6, ends at 9 <= 10, nothing after it | A, C, E |

After three swaps the optimal set *is* the greedy set, and it never lost an interval.
So the greedy set is optimal.

Read round 1 in words: "The optimal set's first interval is B, ending at 4. Mine is
A, ending at 3. Replace B by A. Does anything break? Everything after B in the
optimal set started at 4 or later, because it had to fit after B. A ends at 3, which
is earlier, so all of those still fit. The size is unchanged." That sentence works
for any input, not just this one, because it uses only one fact: the greedy's choice
ends no later than the choice it replaces. That is the **exchange argument**, and it
is the general tool for proving a greedy.

The same table read by columns gives the other proof style, **greedy stays ahead**:
after j picks, the greedy's room is free no later than the optimal solution's. Here:
3 <= 4, 6 <= 7, 9 <= 10. If the greedy is always at least as far ahead, it can never
run out of room before the other one does.

## From the idea to the code

### The derivation as code: brute force, memo, "first kept", greedy

This block runs every stage of the derivation on the same inputs, counts the work,
and checks Step 4's claim directly: in g(T), the branch through the earliest-ending
candidate is always a best branch.

```python run
import random
from functools import lru_cache

def brute(iv):                                   # Step 1: keep or skip, 2^n calls
    iv = sorted(iv)                              # by start
    calls = 0
    def f(i, last):
        nonlocal calls
        calls += 1
        if i == len(iv):
            return 0
        best = f(i + 1, last)                    # skip interval i
        s, e = iv[i]
        if last is None or s >= last:            # keep it, if it fits
            best = max(best, 1 + f(i + 1, e))
        return best
    return f(0, None), calls

def first_kept(iv):                              # Step 3: g(T), one branch per candidate
    ends = sorted(set(e for _, e in iv))
    @lru_cache(maxsize=None)
    def g(T):
        cands = [(s, e) for s, e in iv if T is None or s >= T]
        if not cands:
            return 0
        values = {c: 1 + g(c[1]) for c in cands}
        earliest = min(cands, key=lambda c: c[1])
        assert values[earliest] == max(values.values())   # Step 4: it always wins
        return max(values.values())
    return g(None)

def greedy(iv):                                  # Step 4 as a loop
    kept, last_end = 0, None
    for s, e in sorted(iv, key=lambda c: c[1]):  # by END
        if last_end is None or s >= last_end:
            kept += 1
            last_end = e
    return kept

six = [(1, 4), (2, 3), (3, 5), (0, 6), (5, 7), (4, 8)]
print("six intervals:", "brute (best, calls) =", brute(six),
      " first_kept =", first_kept(six), " greedy =", greedy(six))
assert brute(six)[0] == first_kept(six) == greedy(six) == 3

random.seed(5)
for _ in range(300):
    n = random.randint(0, 9)
    iv = []
    for _ in range(n):
        s = random.randrange(0, 15)
        iv.append((s, s + random.randint(1, 5)))
    assert brute(iv)[0] == first_kept(iv) == greedy(iv), iv
big = [(s, s + random.randint(1, 5)) for s in (random.randrange(0, 40) for _ in range(18))]
print("18 intervals: brute calls =", brute(big)[1], " greedy steps =", len(big))
print("300 random cases: all three agree, and the earliest end always wins in g(T)")
```

On six intervals the brute force already makes dozens of calls; on eighteen it makes
thousands; the greedy looks at each interval once. And the `assert` inside g is Step
4 checked on three hundred inputs: in every state, the earliest-ending candidate's
branch is the maximum.

### Each line, and which part of the recursion it is

| line in `greedy` | in words | which part of the derivation |
|---|---|---|
| `sorted(iv, key=lambda c: c[1])` | look at intervals in order of end | puts the winning branch of g(T) first, every time |
| `if last_end is None or s >= last_end` | does it fit after the room is free? | the "start_x >= T" condition of g |
| `kept += 1` | count it | the "1 +" of g |
| `last_end = e` | the room is free from e | the recursive call g(end_x) |
| (no else branch) | an interval that does not fit is passed over | candidates that are not legal for this T |

Two confusions, settled.

**Why is there no "skip" branch?** In the keep-or-skip recursion, skipping an
interval that fits was a real option. In the greedy, every interval that fits is
kept. That is safe because the intervals arrive in end order: when an interval fits,
it is the earliest-ending legal candidate, which is the branch Step 4 proved best.
Skipping it could only mean choosing a later-ending interval instead, which is never
better.

**Why does sorting by end make the scan find the right candidate?** g(T) wants the
smallest end among intervals starting at or after T. In end order, the first interval
you meet that starts at or after T is exactly that. Intervals passed over earlier are
gone for good, and correctly so: they started before some earlier `last_end`, and
`last_end` only grows, so they will never fit.

### The subtle line, both ways

The one line that decides everything is the sort key. Here is the same loop with
`c[1]` (end) and with `c[0]` (start), on the four intervals from the "starts first"
counterexample, with the state after every step.

```python run
def run(iv, key, label):
    print(label)
    kept, last_end = [], None
    for s, e in sorted(iv, key=key):
        fits = last_end is None or s >= last_end
        if fits:
            kept.append((s, e))
            last_end = e
        print("   (%d,%2d)  fits=%-5s  last_end=%s  kept=%s" % (s, e, fits, last_end, kept))
    return kept

iv = [(0, 10), (1, 2), (3, 4), (5, 6)]
right = run(iv, lambda c: c[1], "sorted by END (right)")
wrong = run(iv, lambda c: c[0], "sorted by START (wrong)")
assert len(right) == 3 and len(wrong) == 1

# the comparison is the other subtle line: >= (touching allowed) vs > (touching conflicts)
def count(iv, strict):
    k, last = 0, None
    for s, e in sorted(iv, key=lambda c: c[1]):
        if last is None or (s > last if strict else s >= last):
            k += 1
            last = e
    return k

chain = [(1, 2), (2, 3), (3, 4), (4, 5)]
print("touching chain:", chain, " >= keeps", count(chain, False), "  > keeps", count(chain, True))
assert count(chain, False) == 4 and count(chain, True) == 2

# what '>' really computes: the answer for closed intervals [s, e], where touching overlaps
from itertools import combinations
def closed_best(iv):
    for k in range(len(iv), -1, -1):
        for c in combinations(sorted(iv), k):
            if all(b[0] > a[1] for a, b in zip(c, c[1:])):
                return k
assert count(chain, True) == closed_best(chain)
print("'>' is not wrong, it answers the closed-interval question")
```

Read the wrong trace. Its first step takes (0,10), because 0 is the smallest start,
and sets `last_end = 10`. That cell is where it goes wrong: the room is now busy
until 10, and every remaining interval starts before 10. The right trace's first step
takes (1,2) and sets `last_end = 2`, the earliest the room could possibly be free.

What the wrong version accidentally computes is nothing useful. That is the danger:
it runs, it terminates, it returns a legal set, and nothing inside the loop can tell
you it is wrong. Only the proof, or a brute-force comparison, catches it.

The second subtle line is the comparison. `s >= last_end` says "an interval may
start exactly when the previous ends". `s > last_end` says it may not. On the chain
(1,2), (2,3), (3,4), (4,5) the first keeps four and the second keeps two. Neither is
a bug in itself: `>` is the correct answer for **closed** intervals, where a meeting
from 1 to 2 and one from 2 to 3 share the moment 2. The statement decides which one
you need. Minimum Interval Removals says touching intervals are compatible, so it is
`>=`. Read that sentence before you type the comparison.

## Why it is correct

:::proof Keeping the earliest-ending interval that fits is optimal
**Setup.** Intervals (s, e) with s < e. Two intervals are compatible when one starts
at or after the other ends. A feasible set is a set of pairwise compatible
intervals; list any feasible set in increasing order of end. The greedy scans the
intervals in increasing order of end and keeps one exactly when its start is at or
after the end of the last kept one. Call its picks g_1, ..., g_k, in order.

**Claim (greedy stays ahead).** Let o_1, ..., o_m be any feasible set, in order of
end. Then for every j from 1 to m, the greedy made at least j picks, and
end(g_j) <= end(o_j).

**Base case, j = 1.** The greedy's first pick is the first interval in end order,
which has the smallest end of all intervals. o_1 is one of the intervals, so
end(g_1) <= end(o_1).

**Inductive step.** Suppose the greedy made at least j picks and end(g_j) <= end(o_j),
and suppose o_{j+1} exists. Since o_j and o_{j+1} are compatible and o_{j+1} ends
later, start(o_{j+1}) >= end(o_j) >= end(g_j). So o_{j+1} fits after g_j. It also
ends after g_j does (it ends after it starts, which is at or after end(g_j)), so the
scan has not yet reached it when it picks g_j. Therefore the scan, continuing after
g_j, meets at least one interval that fits, namely o_{j+1}, and picks the first one
that fits. That pick is g_{j+1}, it exists, and because the scan meets intervals in
order of end and o_{j+1} would have been taken if nothing earlier fitted,
end(g_{j+1}) <= end(o_{j+1}).

**Conclusion.** Suppose some feasible set had m > k intervals. Apply the claim at
j = k: the greedy is at or ahead after k picks. Since o_{k+1} exists, the inductive
step says the greedy makes a (k+1)-th pick, but it made only k. Contradiction. So no
feasible set is larger than the greedy's, and the greedy is optimal.

**Termination.** The scan visits each interval once and does constant work per
visit. ∎
:::

:::note The same proof as an exchange
Let O be any optimal set, and g_1 the interval with the smallest end overall. Let
o_1 be the earliest-ending member of O. Then end(g_1) <= end(o_1), and every other
member of O starts at or after end(o_1) >= end(g_1), so replacing o_1 by g_1 gives a
set that is still feasible and has the same size. So some optimal solution starts
with the greedy's choice. Remove g_1 and everything that overlaps it, and the rest is
the same problem, smaller. Repeat. This is the form you use when there is no natural
"ahead" to measure: find the first place an optimal solution disagrees with you, and
show the swap does no harm. See [[greedy-exchange]].
:::

In plain words: being free earlier is never worse, so ending first is never wrong;
and if the greedy is always free at least as early as any other plan after the same
number of picks, no other plan can fit more.

The assumptions it used, and what breaks without each:

- **Whether an interval fits depends only on when the room is free.** Add "at most
  three meetings per morning" and the state is no longer one number; the step "o_{j+1}
  fits after g_j" fails.
- **Every interval is worth the same, one.** The conclusion compared counts. With
  profits, swapping o_1 for g_1 keeps the count but can lower the total. This is the
  most common way a correct greedy becomes a wrong one.
- **Ties do not matter.** The proof only used <=, so any tie-break works. In other
  greedies ties do matter, and then the tie-break needs its own argument.
- **Nothing is forced.** "Interval 4 must be kept" breaks the base case.
- **The compatibility rule matches the comparison.** Touching allowed means >=;
  touching forbidden means >. The proof goes through either way with the matching
  definition, but the answers differ.

## What it costs

**Sort, then one pass.** The pass does constant work per interval, so

    T(n) = sort + n · O(1) = Θ(n log n) + Θ(n) = Θ(n log n).

The sort is the whole cost. If the input already arrives in the right order (by
time, by position, by index), the greedy is Θ(n), and you should say so.

**Compare with what it replaced.** Brute force 2^n; keep-or-skip with a memo, about
n^2 states. The greedy is not a faster way to fill the memo. It is the observation
that only one state per step is ever on the optimal path, so you never compute the
others.

**Space.** O(1) beyond the sort if you only count; O(k) to return the kept items.

**Heap greedies cost differently.** When the "best so far" changes as you go (the
furthest-building and refuelling variations below), the best is kept in a [[heap]].
Each element is pushed once and popped at most once, each at O(log n), so Θ(n log n)
again, with Θ(n) space. The hidden log is in the heap, not a sort.

**Scan greedies can cost Θ(n).** Jump Game II and Gas Station sort nothing: the
order is the array. One pass, O(1) per element.

**The cost people forget.**

- *The comparator.* Sorting with a key computed inside a comparison function
  computes it O(n log n) times; compute it once into a tuple ([[custom-comparators]]).
  A comparator over strings, as in Largest Number, costs the string length per
  comparison.
- *An outer search.* When the greedy is the feasibility check inside a
  [[binary-search-on-answer]], it runs once per candidate answer: O(n log R) in
  total, not O(n).
- *The verification.* Not runtime, but the cost you should pay anyway: a brute force
  on inputs of size eight and a few hundred random comparisons. Fifteen lines, and the
  only thing between a plausible greedy and a wrong submission.

## How to think about it

Ask these on every optimisation problem that might be greedy.

1. **What is one decision?** Keep this interval; put this box on the truck; jump from
   here; start the trip at this station; pair these two people.
2. **After a decision, what does the future need to know?** If it is one number
   (when the room is free, how far I can reach, how much fuel I have, how many slots
   are left), a greedy is possible. If it is a set or two numbers that trade off,
   think [[dynamic-programming]] first.
3. **List the candidate rules, and try to break each one with two or three items.**
   Smallest, largest, earliest start, earliest end, best ratio, most frequent. Most
   wrong rules die on an example of size three. The rule that survives is the one to
   prove.
4. **Prove it with one of two arguments.** *Exchange*: take an optimal solution that
   disagrees with your first choice and swap your choice in; show it stays legal and
   no worse. *Stays ahead*: show that after j steps your state is at least as good as
   any other plan's after j steps. If one will not go through, try the other before
   giving up.
5. **For an ordering problem, swap two neighbours.** If two adjacent items i, j in an
   order contribute differently depending on which comes first, write both totals and
   subtract. The condition for "i before j" is your sort key. Largest Number, Two City
   and Smith's rule all come out of this.
6. **Does a past choice ever need to be revised?** If the best decision at step i
   depends on what you will see later, but only through "what was the biggest one so
   far", keep the past choices in a heap and revise the worst one when you learn more
   (the furthest-building and refuelling pattern).
7. **Before trusting it, run it against a brute force** on a few hundred random inputs
   of size up to eight.

### Telling it from its neighbours

- **DP** explores all branches; greedy proves one branch wins. If you cannot write the
  feasibility test against one number of state, you probably need the DP.
- **Binary search on the answer** often wraps a greedy: the greedy answers "is
  this value achievable?" and the search finds the best value
  ([[binary-search-on-answer]]).
- **Two pointers** ([[two-pointers]]) is often a greedy in disguise: "move the pointer
  at the shorter wall" is "discard the option that can never be part of a better
  answer".
- **Sorting** ([[sorting]]) is the greedy's usual first line, but the sort is
  not the algorithm. The key is.

## Variations

Every variation below is the same move, find the never-regretted choice, with a
different reason it is never regretted. Each names the technique, what changes, why,
a small example, and a bank problem.

### A. Sort, then take the locally best

The simplest case: the items are interchangeable except for one number, and each one
uses the same amount of the shared resource. Then the best k items are just the k
largest. [[p:roblox-maximum-units-on-truck|Maximum Units on a Truck]]: every box
takes one slot, so fill the truck with the boxes holding the most units. Box types
(count, units) = (1, 3), (2, 2), (3, 1), capacity 4: take one box of 3, two of 2, one
of 1, total 8.

Why it is never regretted: if the truck holds a box with fewer units while a box with
more is left behind, swap them. Same slots, more units. That is an exchange argument
in one sentence. [[p:amazon-get-maximum-sum|Get Maximum Sum]] is the same thing behind
a step that first adds up totals per type in a hash map, then takes the k largest.

The moment items use *different* amounts of the resource, this breaks: that is the
knapsack, and value-per-weight is not safe unless items can be cut (fractional
knapsack is greedy; 0/1 knapsack is not).

### B. Track the furthest reach so far

Nothing is sorted. The array is the order, and the state is "how far can I get".

[[p:navi-jump-game-ii|Jump Game II]]: `nums[i]` is how far you may jump from i; find
the fewest jumps to the end. Think of it as levels: the indices reachable with one
jump, then with two, and so on. You do not need to know *which* index of the current
level to jump from; you only need the furthest index any of them reaches. That one
number is the next level's end.

Trace `[2, 3, 1, 1, 4]`: jumps = 0, level end = 0, furthest = 0.

| i | nums[i] | furthest = max(furthest, i + nums[i]) | i == level end? | jumps | level end |
|---|---|---|---|---|---|
| 0 | 2 | 2 | yes | 1 | 2 |
| 1 | 3 | 4 | no | 1 | 2 |
| 2 | 1 | 4 | yes | 2 | 4 |
| 3 | 1 | 4 | no (the loop stops before the last index) | 2 | 4 |

Two jumps (0 to 1, 1 to 4). Why never regretted: after j jumps, the greedy's reach is
at least as far as any plan's reach after j jumps (stays ahead).

[[p:bloomberg-partition-labels|Partition Labels]] is the same in a string. Cut the
string into as many parts as possible so that each letter is in one part only. The
current part must extend to the last occurrence of every letter in it, so carry
"furthest last occurrence seen so far" and cut when the index reaches it.
`"ababcbacadefegdehijhklij"` gives parts of length 9, 7, 8.

### C. A running balance that resets

[[p:ebay-gas-station|Gas Station]]: stations on a circle, `gas[i]` fuel at each, and
`cost[i]` to drive to the next. Find the station from which you can go all the way
round. Brute force tries every start and drives: O(n^2).

The greedy: drive from station 0 with a running balance of `gas - cost`. When the
balance goes negative at station j, start over from j + 1 with balance 0.

Why it is never regretted, which is the interesting part: suppose you started at s
and ran dry at j. Could any start between s and j work? No. You arrived at each of
those stations with a balance of at least 0, because you had not run dry yet.
Starting there with 0 instead is no better than arriving with something, so you would
also run dry by j. One failure rules out a whole block of starts at once. And a valid
start exists exactly when the total of `gas - cost` is at least 0.

Trace gas `[1, 2, 3, 4, 5]`, cost `[3, 4, 5, 1, 2]`: differences -2, -2, -2, 3, 3,
total 0, so a start exists. Balance: -2 (reset, start 1), -2 (reset, start 2), -2
(reset, start 3), 3, 6. The answer is station 3.

This is the same reset as [[kadane]]: a running sum that is thrown away the moment it
goes negative, because a negative head never helps whatever follows.

### D. Pair the extremes

Sort, then pair the smallest with the largest.
[[p:expedia-efficient-teams|Efficient Teams]]: split everyone into teams of two with
equal total skill. After sorting, the smallest person must go with someone, and the
total is fixed, so their partner must be the largest. Repeat from both ends. `[3, 2,
5, 1, 3, 4]` sorts to `[1, 2, 3, 3, 4, 5]`, pairs (1,5), (2,4), (3,3), all summing to
6; the sum of products is 5 + 8 + 9 = 22. If any pair has a different sum, it is
impossible (-1).

Why never regretted: the smallest and the largest are the two items with the fewest
options. Settling them first cannot block anything, because any other partner would
leave a pair that is worse or impossible. The classic "boats with two people and a
weight limit" is the same: the heaviest person either fits with the lightest, or with
nobody.

[[p:amazon-maximum-capacity|Maximum Capacity]] pairs neighbours instead: sort memory
in decreasing order and pair positions (0,1), (2,3), ..., each pair's smaller value
being a primary. `[1, 2, 1, 2]` sorts to `[2, 2, 1, 1]`, primaries 2 and 1, total 3.
Pairing the extremes would waste the large values as backups.

### E. Prove the order with an exchange argument

When the answer is an **order** of the items, compare two neighbours. Only their
relative order changes when you swap them; everything before and after is untouched.
So "i before j is better" is a condition on i and j alone, and that condition is the
sort comparator.

[[p:linkedin-largest-number|Largest Number]]: arrange numbers so that their
concatenation is the largest. For neighbours a and b, a before b gives the string
a + b, b before a gives b + a, and the rest of the string is the same. So a goes first
when a + b > b + a as strings. `[3, 30, 34, 5, 9]` gives "9534330". Notice that the
obvious key, "sort as strings, descending", puts 30 before 3 and gives "...303...",
which is smaller than "...330...". The pairwise test is the key.

[[p:infosys-two-city-candidate-assignment-cost|Two City Candidate Assignment Cost]]:
send half the people to city A and half to B, minimising total cost. Swap two people
across cities: the change in cost is (a_i - b_i) - (a_j - b_j). So the people with the
smallest `a - b` (who save the most by going to A) go to A. Costs `[[10,20], [30,200],
[400,50], [30,20]]`: differences -10, -170, 350, 10; sorted -170, -10, 10, 350; the
first two go to A (30 + 10), the rest to B (20 + 50); total 110.

[[p:amazon-bring-servers-down|Bring Servers Down]] (stretch) is the same argument after
a translation: turn the story into "each server costs its request rate for every
second it stays alive", compare two adjacent servers in the kill order, and the swap
condition is a ratio rule (Smith's rule, derived in the last-but-one check below).
The hard part is the translation, not the exchange.

### F. Greedy with a counter, or a heap of the best so far

Two different shapes share this heading.

**A counter, when only frequencies matter.**
[[p:google-task-scheduler-with-cooldown|Task Scheduler with Cooldown]]: tasks of some
types, one per time unit, and two tasks of the same type need `cooldown` units
between them. The most frequent type, appearing f times, forces a skeleton of f - 1
blocks of length cooldown + 1, plus a last block holding every type that also appears
f times. So the answer is `max(len(tasks), (f - 1) * (cooldown + 1) + count_of_types_with_f)`.
Tasks `[1, 1, 1, 2, 2, 2]`, cooldown 2: f = 3, two types reach it, (3 - 1) · 3 + 2 = 8:
`1 2 _ 1 2 _ 1 2`.

The same "the most frequent thing decides" appears in
[[p:amazon-min-operation|Min Operation]] (ship pairs of different locations: the answer
is the larger of the top frequency and half of n, rounded up) and
[[p:amazon-get-max-increments|Get Max Increments]] (the most common value forces the
number of increasing runs, giving n minus the top frequency).

**A heap, when you must revise an earlier choice.**
[[p:bloomberg-furthest-building-you-can-reach|Furthest Building You Can Reach]]:
walk along buildings; each climb costs its height in sandbags, or one rope covers any
climb. How far can you go? You do not know at a climb whether it is big enough to
deserve a rope, because the bigger climbs may come later. So do not decide. Give every
climb a rope tentatively, keeping the climbs that have ropes in a min-heap. When you
have used more ropes than you own, take the *smallest* roped climb back and pay for it
in sandbags. Ropes always sit on the biggest climbs so far, which is exactly where
they should be.

Trace heights `[4, 2, 7, 6, 9, 14, 12]`, 5 sandbags, 1 rope. Climbs: 2 to 7 (5), 6 to
9 (3), 9 to 14 (5). Climb 5: heap [5], ropes used 1, fine. Climb 3: heap [3, 5], two
ropes but only one: pop 3, pay 3 sandbags, 2 left. Climb 5: heap [5, 5], pop 5, pay 5
sandbags, but only 2 left: stop. You reach index 4.

[[p:bloomberg-minimum-refueling-stops|Minimum Refueling Stops]] (stretch) is the same
idea: drive past stations without deciding, push their fuel onto a max-heap, and when
the tank runs dry, retroactively "stop" at the biggest station you passed. Target 100,
start fuel 10, stations (10, 60), (20, 30), (30, 30), (60, 40): run dry at 10, take
60 (now at 70 of range), run dry at 70, take the biggest left, 40 (from the station at
60), reach 110: two stops. [[p:amazon-make-array-distinct|Make Array Distinct]] uses a
heap the same way: sweep values upward, and at each value the most expensive waiting
item stays while the cheaper ones move on.

### G. Smaller variations worth knowing

- **Merge the two smallest, repeatedly.** Connecting ropes or building a Huffman code:
  the two smallest are the ones you will pay for most often, so merge them while they
  are cheap ([[huffman]], with a [[heap]]).
- **Greedy as the check inside a binary search.** "Minimise the largest" or "maximise
  the smallest" statements: the greedy checks whether a candidate value is achievable
  ([[binary-search-on-answer]]).
- **Lexicographic greedy.** "Smallest string after removing k characters": fix the
  leftmost position first, because an improvement there outweighs anything after it.
  A [[monotonic-stack]] makes "the best character I can still afford here" cheap.
- **Interval families.** Merging, fewest arrows to burst balloons, fewest rooms: the
  sort-by-end and sweep ideas of this chapter, developed in [[intervals]],
  [[sweep-line]] and [[scheduling]].

Several of these, each checked against an exhaustive answer:

```python run
import heapq, random
from itertools import permutations, combinations

def jump(nums):                                  # B: furthest reach, level by level
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps, end = jumps + 1, far
    return jumps

def gas_station(gas, cost):                      # C: a balance that resets
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start, tank = i + 1, 0
    return start

def largest(nums):                               # E: the pairwise key a+b vs b+a
    from functools import cmp_to_key
    s = sorted(map(str, nums), key=cmp_to_key(lambda a, b: (b + a > a + b) - (b + a < a + b)))
    return "0" if s[0] == "0" else "".join(s)

def two_city(costs):                             # E: sort by a - b
    c = sorted(costs, key=lambda x: x[0] - x[1])
    h = len(c) // 2
    return sum(x[0] for x in c[:h]) + sum(x[1] for x in c[h:])

def furthest(h, bags, ropes):                    # F: heap of roped climbs
    heap = []
    for i in range(len(h) - 1):
        d = h[i + 1] - h[i]
        if d > 0:
            heapq.heappush(heap, d)
            if len(heap) > ropes:
                bags -= heapq.heappop(heap)      # the smallest climb pays in sandbags
                if bags < 0:
                    return i
    return len(h) - 1

assert jump([2, 3, 1, 1, 4]) == 2
assert gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
assert largest([3, 30, 34, 5, 9]) == "9534330"
assert two_city([[10, 20], [30, 200], [400, 50], [30, 20]]) == 110
assert furthest([4, 2, 7, 6, 9, 14, 12], 5, 1) == 4
print("examples: jump 2, gas 3, largest 9534330, two city 110, furthest 4")

rng = random.Random(2)
for _ in range(200):
    n = rng.randint(1, 6)
    nums = [rng.randint(1, 3) for _ in range(n)]
    best = {0: 0}; frontier = [0]                # BFS: the exhaustive fewest jumps
    while frontier:
        nxt = []
        for i in frontier:
            for j in range(i + 1, min(n, i + nums[i] + 1)):
                if j not in best:
                    best[j] = best[i] + 1; nxt.append(j)
        frontier = nxt
    assert jump(nums) == best[n - 1]
    g = [rng.randint(0, 5) for _ in range(n)]; c = [rng.randint(0, 5) for _ in range(n)]
    def ok(s):
        t = 0
        for k in range(n):
            t += g[(s + k) % n] - c[(s + k) % n]
            if t < 0: return False
        return True
    starts = [s for s in range(n) if ok(s)]
    assert (gas_station(g, c) in starts) if starts else gas_station(g, c) == -1
    xs = [rng.randint(0, 120) for _ in range(min(n, 5))]
    assert largest(xs) == str(int(max("".join(map(str, p)) for p in permutations(xs))))
    m = 2 * rng.randint(1, 3); cs = [[rng.randint(0, 9), rng.randint(0, 9)] for _ in range(m)]
    assert two_city(cs) == min(sum(cs[i][0] if i in A else cs[i][1] for i in range(m))
                               for A in map(set, combinations(range(m), m // 2)))
print("200 random cases: each greedy matches the exhaustive answer")
```

## Recognising it in a statement

Ordered by how much you can trust the signal.

1. **"Minimum number of operations / removals / moves" or "maximum number of
   items", where every item counts the same.** Counting objectives with
   interchangeable items are greedy's home ground.
2. **"In any order" or "you may rearrange".** An explicit licence to sort. Then ask
   which key.
3. **A natural order (time, position, index) and one running quantity (the time you
   are free, the furthest reach, the fuel in the tank).** A scan greedy.
4. **The answer is an arrangement or an order.** Compare two neighbours and get a
   comparator.
5. **"Pair up", "teams of two", "each with exactly one partner".** Sort and pair from
   the ends, or neighbours.
6. **"Use at most k of something powerful" (ropes, ladders, free passes) while walking
   forward.** A heap of the k best uses so far.
7. **n up to 10^5 or 2·10^5 with an optimisation objective.** Exhaustive search and an
   O(n^2) DP are both out, so the intended solution is probably O(n log n): a sort and
   a sweep, a heap, or a binary search on the answer. Weak on its own.

### Disguised forms

- **"Minimum removals so that nothing overlaps"** is "maximum kept", interval selection.
- **"Fewest platforms / rooms / chairs"** is the maximum overlap, a sweep
  ([[sweep-line]]).
- **"Make the array strictly increasing with fewest increments"** is a left-to-right
  greedy: each element becomes the smallest value it is allowed to be, because a
  smaller value never constrains the future more.
- **A story about killing servers, serving customers, or finishing jobs with
  penalties** is often a weighted completion time, and the order comes from a
  two-neighbour swap.

### Anti-signals: looks greedy, is not

- **Values together with a budget.** "Maximise profit with capacity W", "at most k
  removals while maximising a value". Two quantities that trade off are the signature
  of a DP table.
- **Arbitrary denominations or costs.** Custom coin systems are DP.
- **"Count the number of ways".**
- **Your feasibility test needs more than one number of history.** If you cannot
  write `if fits(state, item)` with a single-number state, stop.
- **A small example breaks every rule you try.** That is the problem telling you it
  is a DP.

## Traps

**Sorting by the intuitive key instead of the provable one.** Symptom: correct on the
samples, wrong when one long interval swallows several short ones.

**Trusting the samples.** Greedy failures are usually uncommon, not obvious; the
fewest-conflicts rule needs eleven intervals to fail. Symptom: a confident
submission, a wrong answer on a hidden test. Cure: the brute-force loop.

**A greedy that is right only for special inputs.** Largest coin first is right for
real currency and wrong for `[1, 3, 4]`. Symptom: off by one coin on a few amounts.

**The wrong comparison at the boundary.** `>=` versus `>`. Symptom: wrong only on
inputs where an interval starts exactly when another ends.

**Ties broken in a way that matters.** If two orders of equal-key items give different
answers, the proof has a hole. A correct greedy either ignores ties or has an argument
for its tie-break.

**Comparing strings as numbers, or numbers as strings.** In Largest Number, sorting
the strings descending puts "30" before "3". Symptom: "303" where "330" belongs.

**Money in floating point.** Work in integer cents ([[numerical-stability]]).

**Backtracking by accident.** "Try this, and if it fails go back" is
[[backtracking]], and its cost is not n log n.

Here are the coin trap and the fewest-conflicts trap, run:

```python run
def coins_greedy(coins, amount):
    n = 0
    for c in sorted(coins, reverse=True):
        n += amount // c
        amount %= c
    return n if amount == 0 else None

def coins_dp(coins, amount):                     # the exhaustive answer, as a DP
    INF = float("inf")
    best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                best[a] = min(best[a], best[a - c] + 1)
    return None if best[amount] == INF else best[amount]

print("[1,3,4], 6: greedy", coins_greedy([1, 3, 4], 6), " best", coins_dp([1, 3, 4], 6))
assert coins_greedy([1, 3, 4], 6) == 3 and coins_dp([1, 3, 4], 6) == 2
assert all(coins_greedy([1, 5, 10, 25], a) == coins_dp([1, 5, 10, 25], a) for a in range(300))
print("[1,5,10,25]: greedy is optimal for every amount below 300")

from functools import lru_cache
def overlap(a, b):
    return a[0] < b[1] and b[0] < a[1]

def fewest_conflicts_best_tiebreak(iv):          # the BEST this rule can do, any tie-break
    @lru_cache(maxsize=None)
    def go(left):
        if not left:
            return 0
        conf = {x: sum(overlap(x, y) for y in left if y != x) for x in left}
        low = min(conf.values())
        return max(1 + go(tuple(y for y in left if y != x and not overlap(x, y)))
                   for x in left if conf[x] == low)
    return go(tuple(sorted(iv)))

def earliest_end(iv):
    k, last = 0, None
    for s, e in sorted(iv, key=lambda c: c[1]):
        if last is None or s >= last:
            k, last = k + 1, e
    return k

eleven = [(0, 3), (0, 4), (1, 2), (1, 3), (2, 6), (4, 8),
          (7, 10), (8, 11), (9, 11), (10, 13), (10, 14)]
print("eleven intervals: fewest-conflicts keeps", fewest_conflicts_best_tiebreak(eleven),
      " earliest-end keeps", earliest_end(eleven))
assert fewest_conflicts_best_tiebreak(eleven) == 3 and earliest_end(eleven) == 4
```

The coin block shows the same code being right on one input family and wrong on
another. Nothing in the code tells you which family you are in. Only the statement
does: real currency is designed so that largest-first works; a made-up list of coins
is not, and [[p:amd-minimum-coin-change|Minimum Coin Change]] is a DP.

## What to memorise

A shape, a sentence, a habit.

```python
items.sort(key=...)              # the key is the whole algorithm
state = initial                  # ONE number: free-from time, reach, fuel, slots left
for it in items:
    if fits(state, it):          # a test against that one number
        take(it)
        state = update(state, it)
```

For a revisable choice, the same loop with a heap of the choices made so far, popping
the worst one when you are over budget.

**The sentence:** which choice can I prove I will never regret? Prove it by swapping
it into any optimal solution (exchange), or by showing that after every step my state
is at least as good as any other plan's (stays ahead).

**The habit:** write the brute force first, on inputs of size up to eight, and compare
a few hundred random cases before you trust the greedy. In this topic a plausible
wrong rule is the default.

Worth carrying: sort plus sweep is Θ(n log n) and the sort is the whole cost. A second
quantity that trades off with the first (a budget and a value) means DP until proven
otherwise. For an ordering, swap two neighbours and read off the comparator.

## Check yourself

:::check
Trace by hand. Intervals (5,9), (1,3), (2,5), (8,10), (3,6), (6,8), (0,2), touching
allowed. Sort by end, run the greedy with `last_end`, and give the number kept. Then
run "sort by start" and say at which step it first takes something the right greedy
does not.
--
By end: (0,2), (1,3), (2,5), (3,6), (6,8), (5,9), (8,10).

| interval | last_end before | fits? | last_end after |
|---|---|---|---|
| (0,2) | none | yes | 2 |
| (1,3) | 2 | 1 < 2, no | 2 |
| (2,5) | 2 | yes | 5 |
| (3,6) | 5 | no | 5 |
| (6,8) | 5 | yes | 8 |
| (5,9) | 8 | no | 8 |
| (8,10) | 8 | yes | 10 |

Four kept: (0,2), (2,5), (6,8), (8,10).

By start: (0,2), (1,3), (2,5), (3,6), (5,9), (6,8), (8,10). It keeps (0,2), skips
(1,3), keeps (2,5), skips (3,6), then takes **(5,9)**, which the right greedy never
takes, setting last_end = 9. Now (6,8) and (8,10) do not fit. It keeps three. The
mistake is the step where it took an interval ending at 9 when one ending at 8 was
available.
:::

:::check
Trace by hand. Jump Game II on `[3, 1, 4, 1, 1, 1, 2, 1]`. Write `furthest`, the level
end and the jump count after each index, and give the answer.
--
| i | nums[i] | furthest | i == level end? | jumps | level end |
|---|---|---|---|---|---|
| 0 | 3 | 3 | yes | 1 | 3 |
| 1 | 1 | 3 | no | 1 | 3 |
| 2 | 4 | 6 | no | 1 | 3 |
| 3 | 1 | 6 | yes | 2 | 6 |
| 4 | 1 | 6 | no | 2 | 6 |
| 5 | 1 | 6 | no | 2 | 6 |
| 6 | 2 | 8 | yes | 3 | 8 |

The loop stops before the last index (7). Answer 3: 0 to 2, 2 to 6, 6 to 7. Note that
the greedy did not decide at index 0 *where* to jump; it only learned that one jump
reaches up to 3, and the second jump's level was the furthest any of 1, 2, 3 reaches.
:::

:::check
Why does sorting by earliest end work when sorting by shortest length does not? Answer
in terms of the state, not with an example.
--
The state of the algorithm is one number, the time the room becomes free, and the only
effect of a choice on the future is to set that number. The future can do at least as
much from an earlier free time as from a later one (anything that fits after a later
time fits after an earlier one). So the choice that sets the smallest free time is
never worse than any other: that is the whole proof. The earliest end *is* the smallest
free time. Length is a property of the interval that does not appear in the state at
all: a short interval that starts late sets a late free time. A good greedy key is made
of the quantity the state is made of.
:::

:::check
Someone says: "Gas Station is O(n^2): you have to try every start, because a start
that fails tells you nothing about the others." Where are they wrong?
--
A failure tells you a lot. If you start at s and the balance first goes negative at j,
then you reached every station k between s and j with a balance of at least 0. Starting
at k with balance 0 is no better than arriving at k with a non-negative balance, so a
trip starting at k also fails by j. One failed drive rules out every start from s to j,
so the next candidate is j + 1, and the whole scan is one pass: O(n). Together with
"a start exists exactly when the total of gas - cost is at least 0", this gives the
answer without ever retrying a start.
:::

:::check
Attach a profit to each interval and ask for the maximum total profit of a compatible
set. Point at the exact step of the proof that fails, and give a three-interval
counterexample.
--
"Greedy stays ahead" still holds: the greedy's j-th pick still ends no later than any
other plan's j-th pick, because that is a statement about end times. What fails is the
conclusion, which turned "at least as many picks" into "optimal". With profits, more
picks can be worth less. The exchange version fails at the swap: replacing o_1 by g_1
keeps the set legal and the same size, but can lower its profit.

Counterexample: (0,1) profit 1, (1,2) profit 1, (0,2) profit 10. Earliest end keeps the
first two, profit 2; the best is the third alone, profit 10. The replacement is a DP:
sort by end, and for each interval either skip it or take it plus the best up to the
last interval that ends by its start (found by [[binary-search]]).
:::

:::check
Derive the sort key for this ordering problem by swapping two neighbours. Jobs have a
processing time t and a weight w; jobs run one after another, and a job finishing at
time C costs w · C. Minimise the total cost. Then order the jobs (t, w) = (3, 1),
(1, 2), (2, 2).
--
Take two neighbours i then j, starting at time S. Everything before and after them is
unaffected by their order. i first costs w_i(S + t_i) + w_j(S + t_i + t_j); j first
costs w_j(S + t_j) + w_i(S + t_j + t_i). Subtract: i first minus j first =
w_j·t_i - w_i·t_j. So i should go first when w_j·t_i < w_i·t_j, that is, when
t_i / w_i < t_j / w_j. Sort by t / w, smallest first (Smith's rule).

Ratios: (3,1) is 3, (1,2) is 0.5, (2,2) is 1. Order (1,2), (2,2), (3,1). Completion
times 1, 3, 6; cost 2·1 + 2·3 + 1·6 = 14. The order (3,1), (1,2), (2,2) would cost
1·3 + 2·4 + 2·6 = 23. This is the shape of [[p:amazon-bring-servers-down|Bring Servers Down]]
once its story is translated.
:::

:::check
Reduce this disguised problem. "You walk a road and can refuel at any station you
pass, taking all its fuel. Minimise the number of stops." Why is "stop whenever the next
station is out of reach" wrong, and what replaces it?
--
"Stop when forced" means: at each station, stop only if you cannot reach the next
point without fuel from here. It commits to the *nearest* station at the moment of
need, when the station you want is the *biggest* one you have passed. Start fuel 10,
stations (5, 30) and (10, 1), target 40. At 5 you can still reach 10, so you do not
stop. At 10 you are empty and must stop, taking 1 unit: you reach 11, and are stuck.
Stopping at 5 instead gives 30 units, reaching 40 with one stop.

The fix is the revisable greedy: drive as far as the fuel allows, pushing every station
you pass onto a max-heap without stopping. When you cannot reach the next point, pop
the biggest station you passed and count one stop, as if you had stopped there. Each
stop is the one that adds the most range, and a stop at a station you have already
passed is legal because the order of refuelling does not matter, only which stations
you used. That is variation F, [[p:bloomberg-minimum-refueling-stops|Minimum Refueling Stops]].
:::
