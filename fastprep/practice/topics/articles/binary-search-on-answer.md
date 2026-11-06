# Binary Search on the Answer

> When finding the best value is hard but checking whether a given value is good enough is easy, and good enough stays good enough as you loosen it, you stop searching for the answer and binary search the candidates instead: thirty cheap yes/no checks replace one hard optimisation.

## The problem it solves

Koko has four piles of bananas, of sizes 1, 7, 10 and 15. She has 10 hours. Each
hour she picks one pile and eats up to k bananas from it; if the pile has fewer
than k left, she finishes it and waits out the rest of the hour. What is the
smallest whole speed k that lets her finish every pile in 10 hours?

That is [[p:amazon-koko-eating-bananas|Koko Eating Bananas]]. Read it again and
notice what kind of question it is. It does not ask you to arrange anything. It
asks for the smallest number with a property. And the property is easy to test for
any one number you pick:

- at speed 3, the piles take 1, 3, 4 and 5 hours (a pile of 10 at 3 per hour needs
  ⌈10/3⌉ = 4 hours), 13 hours in total. Too slow.
- at speed 4, they take 1, 2, 3 and 4 hours, 10 in total. Fits.

So the answer is at least 4 because 3 fails, and 4 works, so it is 4. The whole
difficulty is that we got lucky picking 3 and 4. We need a way to find the right
number without luck.

The first program anyone writes tries every speed from 1 upward and stops at the
first one that fits. That is correct. It is also too slow: in the real problem a
pile can hold 10^9 bananas, so the answer can be as large as 10^9, and each trial
costs a pass over 10^5 piles. That is 10^14 steps.

The second thing people try is a formula: "the total is 33 bananas over 10 hours,
so the speed is ⌈33/10⌉ = 4". Here it gives the right number, and that is an
accident. We will break it in a moment.

What this chapter builds is the method that answers Koko in about 30 trials
instead of 10^9, and the same method answers a whole family that looks nothing
alike: the smallest ship that delivers in d days, the largest gap between cows,
the highest saw blade, the fewest seconds for a set of processors. Each of them is
a [[binary-search]], over a list of candidate answers that never exists in memory.

### When it is the wrong tool

- **The property is not monotone.** If speed 5 works, speed 6 must work too, or
  the method fails. Most "minimise the maximum" problems have this property, but
  check it, because a problem where a bigger value can make things worse is not a
  search.
- **You can build the answer directly.** If sorting or a greedy rule produces the
  optimum in one pass, use it. Searching costs a log factor for nothing.
- **The check is as hard as the problem.** If "is X good enough?" needs a full
  dynamic program over X, the search multiplies that cost by 30. Sometimes that is
  still fine; sometimes the DP alone was the answer.
- **The word "feasibility" without an answer to search.** This bank tags several
  problems with feasibility that are a single yes/no question with nothing to
  optimise: [[p:intuit-course-schedule-feasibility|Can You Finish All Courses?]]
  is a cycle check ([[topological-sort]]), and
  [[p:apple-meeting-room-request-feasibility|Meeting Room Request Feasibility]] is
  a sort and an overlap scan ([[intervals]]). They are the "check" half of this
  chapter with no search around it.

About fifty problems in this bank are this technique, and many more use it as a
step. It is one of the highest-yield ideas in OA problems, because the statement
almost never says "binary search".

## Build it from the brute force

### Step 1: try every candidate

Write the check first, because everything else is built around it. At speed k, a
pile of p bananas takes ⌈p/k⌉ hours. The total is the sum over piles.

```
def hours(k):
    return sum(ceil(p / k) for p in piles)

for k in range(1, max(piles) + 1):    # every candidate speed, smallest first
    if hours(k) <= h:
        return k
```

Why stop at max(piles)? Because at that speed every pile takes exactly one hour,
so the total is the number of piles, and the problem guarantees h is at least that.
max(piles) always works. Speeds above it cannot do better than one hour per pile.

Count it. The loop tries up to max(piles) speeds, each costing one pass over n
piles. For n = 10^5 and piles up to 10^9: 10^14.

### Step 2: write the answers out

Run the check for every speed on our small case, piles [1, 7, 10, 15], h = 10:

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hours(k) | 33 | 18 | 13 | 10 | 8 | 8 | 7 | 6 | 6 | 5 | 5 | 5 | 5 | 5 | 4 |
| fits in 10? | no | no | no | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes |

Look at the bottom row. It is no, no, no, then yes forever. We have seen this row
before. It is exactly the shape that [[binary-search]] finds the boundary of: a
yes/no question that flips once. The scan in Step 1 is the linear scan for a first
bad version. Its waste is the same waste: every "no" at speed k is also a "no" for
every speed below k, and every "yes" is a yes for every speed above, and the scan
throws that away.

<svg viewBox="0 0 640 300" role="img" aria-label="bar chart of hours needed at each speed k from 1 to 15 for piles 1, 7, 10, 15: 33, 18, 13, 10, 8, 8, 7, 6, 6, 5, 5, 5, 5, 5, 4; a horizontal line marks the limit of 10 hours; bars from k = 4 onward are at or under the line and are shaded; underneath, a row of no no no yes yes ... shows the monotone answer">
  <g>
    <line x1="50" y1="230" x2="610" y2="230"/>
    <line x1="50" y1="170" x2="610" y2="170" stroke-dasharray="6 4"/>
    <text x="612" y="166" text-anchor="end">h = 10</text>
    <rect x="60" y="32" width="28" height="198"/>
    <rect x="96" y="122" width="28" height="108"/>
    <rect x="132" y="152" width="28" height="78"/>
    <rect class="fill" x="168" y="170" width="28" height="60"/>
    <rect class="fill" x="204" y="182" width="28" height="48"/>
    <rect class="fill" x="240" y="182" width="28" height="48"/>
    <rect class="fill" x="276" y="188" width="28" height="42"/>
    <rect class="fill" x="312" y="194" width="28" height="36"/>
    <rect class="fill" x="348" y="194" width="28" height="36"/>
    <rect class="fill" x="384" y="200" width="28" height="30"/>
    <rect class="fill" x="420" y="200" width="28" height="30"/>
    <rect class="fill" x="456" y="200" width="28" height="30"/>
    <rect class="fill" x="492" y="200" width="28" height="30"/>
    <rect class="fill" x="528" y="200" width="28" height="30"/>
    <rect class="fill" x="564" y="206" width="28" height="24"/>
    <text x="74" y="27" text-anchor="middle">33</text>
    <text x="110" y="117" text-anchor="middle">18</text>
    <text x="146" y="147" text-anchor="middle">13</text>
    <text x="182" y="162" text-anchor="middle">10</text>
    <text x="74" y="246" text-anchor="middle">1</text>
    <text x="110" y="246" text-anchor="middle">2</text>
    <text x="146" y="246" text-anchor="middle">3</text>
    <text x="182" y="246" text-anchor="middle">4</text>
    <text x="218" y="246" text-anchor="middle">5</text>
    <text x="254" y="246" text-anchor="middle">6</text>
    <text x="290" y="246" text-anchor="middle">7</text>
    <text x="326" y="246" text-anchor="middle">8</text>
    <text x="362" y="246" text-anchor="middle">9</text>
    <text x="398" y="246" text-anchor="middle">10</text>
    <text x="434" y="246" text-anchor="middle">11</text>
    <text x="470" y="246" text-anchor="middle">12</text>
    <text x="506" y="246" text-anchor="middle">13</text>
    <text x="542" y="246" text-anchor="middle">14</text>
    <text x="578" y="246" text-anchor="middle">15</text>
    <text x="30" y="246" text-anchor="middle">k</text>
    <text x="74" y="268" text-anchor="middle">no</text>
    <text x="110" y="268" text-anchor="middle">no</text>
    <text x="146" y="268" text-anchor="middle">no</text>
    <text x="182" y="268" text-anchor="middle">yes</text>
    <text x="380" y="268" text-anchor="middle">yes  yes  yes  ...  yes</text>
    <text x="320" y="292" text-anchor="middle">hours(k) never goes up as k grows, so "fits?" flips from no to yes once, at k = 4</text>
  </g>
</svg>

Notice that hours(k) is not strictly decreasing. Speeds 5 and 6 both take 8 hours,
and speeds 10 to 14 all take 5. That does not matter. The method needs only that
it never goes *up*, so that once the bar is under the line it stays under.

### The question that unlocks it

**If someone handed me a candidate answer, could I check it quickly, and does a
yes for one candidate mean a yes for every easier one?**

When both halves of that question are yes, you do not have to find the answer. You
only have to check candidates, and binary search decides which ones to check.

Say it a second way. The original problem is an optimisation: "the least speed
such that...". The trick is to turn it into a decision: "is speed X enough?". A
decision is often far easier than the optimisation, because the number X is fixed
and you can lean on it. And if the decision is monotone in X, about 30 decisions,
chosen by halving, give you the optimum.

### You might think: "Binary search needs a sorted array, and there is none here."

There is no array of speeds in memory. But the bottom row of the table is an array:
position k holds the answer to "does speed k fit?". Binary search never needed the
array to exist. It needs to be able to ask about position mid, and it needs the
answers to flip once. Here, asking about position mid means calling hours(mid). The
"array" has 10^9 positions and costs nothing to store.

### You might think: "Just compute it: total bananas divided by hours."

On [1, 7, 10, 15] with h = 10, ⌈33/10⌉ = 4 is right. Now take two piles of 5 and
h = 3. The formula says ⌈10/3⌉ = 4. At speed 4, each pile of 5 takes ⌈5/4⌉ = 2
hours, 4 in total. That is more than 3. The answer is 5 (one hour per pile, then a
spare hour).

The formula fails because the hours do not pool. A pile of 5 at speed 4 eats 4 in
the first hour and 1 in the second, and the 3 bananas of capacity left in that
second hour cannot be spent on the other pile. The average is only a lower bound.
Rounding per pile is what makes the problem non-linear, and it is why a formula
does not exist.

### You might think: "The check must find the best arrangement, so it is as hard as the problem."

The check answers an easier question, and the easier question is often greedy.

Take [[p:amazon-capacity-to-ship-packages-within-d-days|Capacity To Ship Packages Within D Days]].
Packages [1, 2, ..., 10] must be shipped in order; each day the ship carries a run
of packages whose weights add up to at most its capacity. What is the least
capacity that ships everything in 5 days?

Optimising directly means choosing where to cut the list into at most 5 runs to
make the heaviest run as light as possible. That is a real search over cut
positions (a [[partition-dp|partition DP]]). But the check, "can capacity 15 do it
in 5 days?", has a one-line answer: load each day as much as fits, then start the
next day. At capacity 15: [1, 2, 3, 4, 5] = 15, [6, 7] = 13, [8], [9], [10]. Five
days. Yes.

Why is "load as much as fits" the best way to use a fixed capacity? Because putting
a package on today's ship, when it fits, can never hurt: whatever tomorrow could
have done starting at that package, it can do starting one package later. Fixing
the capacity turned a hard choice into an obvious one. That is the second gift of
the decision version, and it is why the chapter's techniques include "a greedy
check inside the search". We prove the greedy in "Why it is correct".

### You might think: "Search over the values in the input."

Sometimes the answer is always one of the input values, and searching over the
sorted input works. Often it is not. For Koko, the answer for [1, 7, 10, 15] and
h = 10 is 4, which is not a pile size. A search over the sorted piles would only
try 1, 7, 10 and 15 and would return 7. Search over the range of possible answers,
not over the input, unless you have proven the answer is an input value.

### Step 3: the range, with honest ends

Binary search needs a known no and a known yes. Here they are values, not indices.

- **A known no.** Speed 0 eats nothing, so it never finishes. We will never call
  hours(0), which would divide by zero; 0 is a claim, exactly like the sentinel -1
  in [[binary-search]].
- **A known yes.** max(piles), as argued in Step 1.

So lo = 0, hi = max(piles), and the first yes is somewhere in 1..max(piles).

### Step 4: plug the check into the loop

```
lo, hi = 0, max(piles)          # lo: a speed that fails.  hi: a speed that works.
while hi - lo > 1:
    mid = lo + (hi - lo) // 2
    if hours(mid) <= h:
        hi = mid                # mid works: the answer is mid or smaller
    else:
        lo = mid                # mid fails: the answer is bigger
return hi
```

This is the [[binary-search]] template, letter for letter. The only new thing is
pred: instead of "a[mid] >= x" it is "hours(mid) <= h". Thirty calls of hours
instead of 10^9.

### Step 5: the other direction, maximise the minimum

Half the family asks for the largest value instead of the smallest. Take
[[p:peoplestrong-aggressive-cows|Aggressive Cows]]: stalls at positions 1, 2, 4,
8, 9, place 3 cows so that the closest two are as far apart as possible.

The decision version is "can I place 3 cows with every gap at least d?". Its
answers, for d = 0, 1, 2, ...:

| d | 0 | 1 | 2 | 3 | 4 | 5 | ... | 9 |
|---|---|---|---|---|---|---|---|---|
| 3 cows with gaps >= d? | yes | yes | yes | yes | no | no | ... | no |

Now the row reads yes, then no. Asking for more separation can only make it harder.
We want the **last yes**. Flip the meanings of the two pointers: lo is a known yes,
hi is a known no, and the loop moves lo on a yes. When they are adjacent, lo is the
last yes.

The two directions are the same idea, and you should be able to say which one you
have before writing a line:

- **Minimise the maximum** (capacity, speed, time, largest load): bigger values
  are easier. Answers read no...no yes...yes. Want the first yes.
- **Maximise the minimum** (gap, distance, length, height): bigger values are
  harder. Answers read yes...yes no...no. Want the last yes.

### The technique in one sentence

**Binary search on the answer: turn "find the best X" into "is X good enough?",
check that a yes for one X is a yes for every easier X, then binary search the
range of X with that check as the predicate.**

And the question that finds it, worth asking on every "minimise" or "maximise"
problem: **if someone handed me a candidate answer, could I check it quickly, and
would every easier candidate also pass?**

## Worked by hand

### Trace 1: Koko, the first yes

Piles [1, 7, 10, 15], h = 10. lo = 0 (known no), hi = 15 (known yes). At every
step, compute hours(mid) pile by pile. That is the part to do with a pen.

| step | lo | hi | mid | hours(mid), pile by pile | total | <= 10? | move |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 15 | 7 | 1 + 1 + 2 + 3 | 7 | yes | hi = 7 |
| 2 | 0 | 7 | 3 | 1 + 3 + 4 + 5 | 13 | no | lo = 3 |
| 3 | 3 | 7 | 5 | 1 + 2 + 2 + 3 | 8 | yes | hi = 5 |
| 4 | 3 | 5 | 4 | 1 + 2 + 3 + 4 | 10 | yes | hi = 4 |
| end | 3 | 4 | | | | | stop: answer 4 |

The story of step 2 in words: "I try speed 3. The pile of 1 takes one hour. The
pile of 7 takes ⌈7/3⌉ = 3 hours: 3, 3, then the last 1. The pile of 10 takes
⌈10/3⌉ = 4. The pile of 15 takes 5. Total 13, more than 10. So speed 3 fails, and
every slower speed fails too, because going slower can only add hours. lo moves to
3: I have proven that 3 is too slow."

And step 4: "lo = 3 is a proven failure, hi = 5 is a proven success. I try 4: 1 + 2
+ 3 + 4 = 10 hours, exactly the limit. It fits. Now 3 fails and 4 works, and they
are neighbours, so 4 is the least speed that works."

Four checks instead of up to fifteen. With piles up to 10^9 it is thirty checks
instead of up to a billion.

### Trace 2: ship packages, a greedy check inside every step

Weights [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], days = 5. The range is the interesting
part:

- **A known no:** max(weights) - 1 = 9. A ship of 9 cannot carry the package of 10
  at all.
- **A known yes:** sum(weights) = 55. One day, everything.

The check at capacity c: start day 1 with an empty ship; for each package, if it
does not fit on today's ship, start a new day; put it on. Count the days.

| step | lo | hi | mid | the greedy days at capacity mid | days | <= 5? | move |
|---|---|---|---|---|---|---|---|
| 1 | 9 | 55 | 32 | [1..7] = 28, [8, 9, 10] = 27 | 2 | yes | hi = 32 |
| 2 | 9 | 32 | 20 | [1..5] = 15, [6, 7] = 13, [8, 9] = 17, [10] | 4 | yes | hi = 20 |
| 3 | 9 | 20 | 14 | [1..4] = 10, [5, 6] = 11, [7], [8], [9], [10] | 6 | no | lo = 14 |
| 4 | 14 | 20 | 17 | [1..5] = 15, [6, 7] = 13, [8, 9] = 17, [10] | 4 | yes | hi = 17 |
| 5 | 14 | 17 | 15 | [1..5] = 15, [6, 7] = 13, [8], [9], [10] | 5 | yes | hi = 15 |
| end | 14 | 15 | | | | | stop: answer 15 |

The story of step 3: "Capacity 14. Day 1: 1, 2, 3, 4 make 10; the 5 would make 15,
too much, so day 1 ends at 10. Day 2: 5 and 6 make 11; the 7 would make 18, so day 2
ends. Day 3: 7, and the 8 would make 15, so day 3 is just 7. Then 8, 9 and 10 each
need their own day, because any two of them weigh more than 14. Six days. Too many."

Compare steps 3 and 5. Capacity 14 and capacity 15 differ by one unit, and that one
unit lets day 1 take the package of 5 too (1 + 2 + 3 + 4 + 5 = 15), which lets day 2
take 6 and 7 together, and so on. The check does not reason about any of that. It
just loads greedily, and the binary search finds the exact capacity where the
greedy count drops to 5.

### Trace 3: cows, the last yes

Stalls [1, 2, 4, 8, 9] (sort them first if they are not sorted), 3 cows. The check
at distance d: put a cow in the first stall; walk right and put a cow in every stall
that is at least d past the last cow; succeed if you placed 3.

- **A known yes:** d = 0. Any placement has gaps of at least 0.
- **A known no:** the span is 9 - 1 = 8, and 3 cows make 2 gaps, so the smallest gap
  is at most 8 / 2 = 4. Any d above that fails, and 9 certainly fails. Use hi = 9
  (or the tighter 5).

| step | lo | hi | mid | greedy placement at distance mid | cows | >= 3? | move |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 9 | 4 | 1, then 8 (2 and 4 are too close), then 9 is only 1 away | 2 | no | hi = 4 |
| 2 | 0 | 4 | 2 | 1, 4, 8 (9 is 1 away from 8) | 3 | yes | lo = 2 |
| 3 | 2 | 4 | 3 | 1, 4, 8 | 3 | yes | lo = 3 |
| end | 3 | 4 | | | | | stop: answer 3 |

Notice which pointer moves on a yes: lo. A yes at d means "d is achievable, so the
answer is d or more". That is the mirror of Koko, where a yes at k meant "the answer
is k or less". The answer is lo, the last yes: 3, with cows at 1, 4 and 8, gaps 3
and 4.

What do the traces show that the code would not? That the check is the whole
problem and the search is bookkeeping. Every row's real work is the middle column:
a greedy pass that you could do on paper. The search only decides which candidate to
hand it next. And it shows that the direction of the yes, toward smaller or toward
larger values, decides which pointer moves.

## From the idea to the code

### The direct version, next to the brute force

The program writes the Koko check, solves it by trying every speed and by binary
search, counts the checks each one makes, and confirms they agree on random inputs.

```python run
import random

def hours(piles, k):                       # the check: total hours at speed k
    return sum((p + k - 1) // k for p in piles)   # ceil(p / k) in integers

def brute(piles, h):                       # try every speed, smallest first
    checks = 0
    for k in range(1, max(piles) + 1):
        checks += 1
        if hours(piles, k) <= h:
            return k, checks

def first_true(lo, hi, pred):              # lo: known no, hi: known yes
    checks = 0
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        checks += 1
        if pred(mid):
            hi = mid
        else:
            lo = mid
    return hi, checks

def koko(piles, h):
    return first_true(0, max(piles), lambda k: hours(piles, k) <= h)

for piles, h in (([1, 7, 10, 15], 10), ([4, 9, 13], 8), ([8, 8, 8], 3), ([5, 5], 3)):
    print(piles, "h =", h, "-> brute", brute(piles, h), " search", koko(piles, h))
    assert brute(piles, h)[0] == koko(piles, h)[0]
assert koko([1, 7, 10, 15], 10)[0] == 4 and koko([5, 5], 3)[0] == 5
assert -(-sum([5, 5]) // 3) == 4           # the 'average' formula says 4: wrong

big = [10**9] * 10 + [1] * 10              # answers up to 10^9: brute is hopeless
k, checks = koko(big, 20)
print("piles up to 10^9: answer", k, "after", checks, "checks")
assert k == 10**9 and checks <= 30

random.seed(5)
for _ in range(300):
    piles = [random.randint(1, 40) for _ in range(random.randint(1, 6))]
    h = random.randint(len(piles), 3 * len(piles) + 10)
    assert koko(piles, h)[0] == brute(piles, h)[0]
print("search == brute force on 300 random cases")
```

### Each line, and which part of the idea it is

| line | in plain words | from which step |
|---|---|---|
| `hours(piles, k)` | the decision: is speed k enough? (it returns the hours, the caller compares) | Step 1, the check |
| `(p + k - 1) // k` | ⌈p/k⌉ without floats | Step 1 |
| `lo, hi = 0, max(piles)` | a speed proven too slow, a speed proven enough | Step 3 |
| `pred = hours(...) <= h` | "fits in h hours" | the unlocking question |
| `if pred(mid): hi = mid` | mid is enough, so the least enough speed is mid or below | Step 4 |
| `else: lo = mid` | mid is too slow, so is everything below it | Step 4 |
| `return hi` | the least speed that fits | Step 4 |

Settle the small confusions.

**lo and hi are values, not indices.** In [[binary-search]] they pointed into an
array. Here they are speeds. The loop does not know the difference, and that is the
point.

**Why lo = 0 and not 1?** Because lo must be a proven failure, and speed 1 might
succeed (one pile, lots of hours). Speed 0 fails by definition. It is never passed
to hours, which is good, because hours(0) divides by zero. The same honesty argument
as the sentinel -1.

**Why not the tightest possible range?** You may tighten it: a lower bound of
⌈sum/h⌉ - 1 is also a proven failure, since the average is a lower bound. It saves
a few iterations. It also adds a place for a bug. A loose honest range costs
log₂(range) checks, and log₂(10^9) is 30 whether the range is tight or not.

**Ceiling without floats.** `(p + k - 1) // k` and `-(-p // k)` are both ⌈p/k⌉ in
exact integer arithmetic. `math.ceil(p / k)` goes through a float and is wrong for
large p; see Traps.

**The check returns a number, and pred compares it.** Keep the check honest and
separate (hours, days, cows, wood), and put the comparison with the limit in one
place. Then the direction of the comparison is visible on one line, which is where
the next section's bug lives.

### The general shape, four problems at once

Every problem in this family is the same two functions: a check, and one of two
loops. The program below solves four of them that way and checks each against
trying every candidate.

```python run
import random

def first_true(lo, hi, ok):            # lo fails, hi works: least value that works
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if ok(mid): hi = mid
        else:       lo = mid
    return hi

def last_true(lo, hi, ok):             # lo works, hi fails: greatest value that works
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if ok(mid): lo = mid
        else:       hi = mid
    return lo

def ship_days(w, cap):                 # greedy: fill each day as much as fits
    days, load = 1, 0
    for x in w:
        if load + x > cap:
            days, load = days + 1, 0
        load += x
    return days

def cows_placed(stalls, d):            # greedy: each cow as far left as allowed
    count, last = 1, stalls[0]
    for s in stalls[1:]:
        if s - last >= d:
            count, last = count + 1, s
    return count

def wood(heights, saw):                # wood collected with the blade at height saw
    return sum(h - saw for h in heights if h > saw)

def ship(w, D):    return first_true(max(w) - 1, sum(w), lambda c: ship_days(w, c) <= D)
def cows(st, k):   st = sorted(st); return last_true(0, st[-1] - st[0] + 1, lambda d: cows_placed(st, d) >= k)
def saw(hs, M):    return last_true(-1, max(hs), lambda s: wood(hs, s) >= M)
def ribbon(rs, k): return last_true(0, max(rs) + 1, lambda L: sum(r // L for r in rs) >= k)

print("ship  [1..10] in 5 days ->", ship(list(range(1, 11)), 5))
print("cows  [1,2,4,8,9], 3     ->", cows([1, 2, 4, 8, 9], 3))
print("saw   [20,15,10,17], 7   ->", saw([20, 15, 10, 17], 7))
print("ribbon [9,7,5], 3        ->", ribbon([9, 7, 5], 3), " [7,5,9], 4 ->", ribbon([7, 5, 9], 4))
assert (ship(list(range(1, 11)), 5), cows([1, 2, 4, 8, 9], 3)) == (15, 3)
assert (saw([20, 15, 10, 17], 7), ribbon([9, 7, 5], 3), ribbon([7, 5, 9], 4)) == (15, 5, 4)

random.seed(11)                        # every one against 'try every candidate'
for _ in range(300):
    w = [random.randint(1, 9) for _ in range(random.randint(1, 7))]
    D = random.randint(1, len(w))
    assert ship(w, D) == min(c for c in range(max(w), sum(w) + 1) if ship_days(w, c) <= D)
    st = random.sample(range(30), random.randint(2, 7)); k = random.randint(2, len(st))
    assert cows(st, k) == max(d for d in range(0, 31) if cows_placed(sorted(st), d) >= k)
    hs = [random.randint(1, 20) for _ in range(random.randint(1, 5))]; M = random.randint(1, sum(hs))
    assert saw(hs, M) == max(s for s in range(0, 21) if wood(hs, s) >= M)
    rs = [random.randint(1, 20) for _ in range(random.randint(1, 4))]; k = random.randint(1, sum(rs))
    assert ribbon(rs, k) == max(L for L in range(1, 21) if sum(r // L for r in rs) >= k)
print("ship, cows, saw and ribbon agree with exhaustive search on 300 random cases each")
```

Look at the ranges, because each one is an argument:

- **ship:** max(w) - 1 fails (the heaviest package does not fit), sum(w) works (one
  day).
- **cows:** 0 works (any placement), span + 1 fails (no two stalls are that far
  apart).
- **saw:** -1 is an imaginary yes (the problem guarantees the wood exists, so the
  blade at 0 works too), max(heights) fails (the blade above every pole cuts
  nothing, and M >= 1).
- **ribbon:** 0 is an imaginary yes (the problem guarantees length 1 works),
  max + 1 fails (no ribbon is that long). The check is never called at 0, which
  would divide by zero.

### The subtle line, both ways

The line that bites is the one that decides the direction: which pointer moves on a
yes, and which pointer you return. It is one word in the code, and getting it
wrong does not crash. It returns a plausible number that is off by one, or the
untouched end of the range.

Here is Aggressive Cows done three ways. The right way is last_true. The first
wrong way pastes the minimise template unchanged, with the cows check as its
predicate. The second wrong way notices the direction is flipped, so it negates the
check to make it "no...no yes...yes" again, and then returns hi out of habit.


```python run
def cows_placed(stalls, d):
    count, last = 1, stalls[0]
    for s in stalls[1:]:
        if s - last >= d:
            count, last = count + 1, s
    return count

stalls, k = [1, 2, 4, 8, 9], 3
ok = lambda d: cows_placed(stalls, d) >= k
print("ok(d) for d = 0..9:", ["yes" if ok(d) else "no" for d in range(10)])

def trace(name, lo, hi, pred, move_lo_on_yes, answer):
    print(name)
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        y = pred(mid)
        if y == move_lo_on_yes: lo = mid
        else:                   hi = mid
        print("   mid=%d  pred=%-5s ->  lo=%d hi=%d" % (mid, y, lo, hi))
    a = lo if answer == "lo" else hi
    print("   returns", answer, "=", a)
    return a

right = trace("right: last_true, lo = known yes", 0, 9, ok, True, "lo")
wrong1 = trace("wrong 1: minimise template pasted as is", 0, 9, ok, False, "hi")
wrong2 = trace("wrong 2: negated check, but returns hi", 0, 9, lambda d: not ok(d), False, "hi")
assert right == 3          # cows at 1, 4, 8
assert wrong1 == 9         # never moved hi: the untouched end of the range
assert wrong2 == 4         # the first distance that FAILS: off by one
assert not ok(wrong2) and ok(wrong2 - 1)
print("right:", right, "| wrong 1:", wrong1, "| wrong 2:", wrong2, "(the first infeasible distance)")
```

Point at the exact step where each wrong one goes wrong.

- **Wrong 1**, first step: mid = 4, the check says no, and the minimise template
  treats a no as "too small, go right", so lo = 4. From then on every probe (6, 7,
  8) is above 3 and says no, and lo climbs to 8. It returns hi = 9, the end it
  started with. It assumed pred(lo) was a no at the start, and pred(0) is a yes: a
  dishonest sentinel. On a real input the symptom is "always returns the upper end
  of the range".
- **Wrong 2** searches correctly. Its predicate "cannot place 3 cows at distance d"
  is no for 0..3 and yes for 4..9, so it finds the first yes, 4, exactly. And 4 is
  the first distance that **fails**. The answer is the one before it: lo = 3. This
  is the off-by-one that passes the sample when the sample is generous and fails
  the hidden tests.

The cure is the same as in [[binary-search]]: say what lo and hi mean before you
write the loop. "Maximise the minimum: lo is a distance I have achieved, hi is one
I have proven impossible, I return lo." Once that sentence is said, the branch and
the return are forced.

## Why it is correct

Two things need proving, and they are different. The first is that binary search
over the candidates returns the optimum. The second is that the greedy check
answers the decision correctly. A wrong check makes a correct search return a wrong
answer, so both matter.

:::proof The search finds the optimum, and the greedy checks are exact
**Part 1: from decisions to the optimum.** Let ok(x) be the decision "x is good
enough" and suppose it is monotone: if ok(x) is true then ok(y) is true for every
y > x (the minimise case; the maximise case is the mirror image). Let x* be the
optimum, the least x with ok(x) true. Then ok is false for every x < x*, by
definition of "least", and true for every x >= x*, by monotonicity. So the answers
over the range read false...false true...true with the first true exactly at x*.
The binary search template returns the first true of such a row (proved in
[[binary-search]]: the invariant "ok(lo) false, ok(hi) true" holds at the start,
every step keeps it, the width shrinks, and at width 1, hi is a true with a false
just before it). So it returns x*.

**Part 2: the ship check is exact.** Fix a capacity c. Claim: loading each day as
much as fits uses the fewest days possible for capacity c.

Take any valid schedule S for capacity c, and let the greedy schedule be G. Say a
schedule has "shipped through package j" after day t if packages 1..j are all on
days 1..t. We show by induction on t: after t days, G has shipped through at least
as many packages as S.

- t = 1: S's first day is a run 1..s₁ with total at most c. G keeps loading until the
  next package does not fit, so G's first day is a run 1..g₁ with g₁ >= s₁ (G would
  not stop before s₁, since 1..s₁ fits).
- From t to t + 1: by induction, after t days G has shipped through g_t >= s_t. On day
  t + 1, S ships packages s_t + 1 .. s_{t+1}, total at most c. G starts at g_t + 1, which
  is at or after s_t + 1, so the packages g_t + 1 .. s_{t+1} are a part of S's day, and
  their total is also at most c. So G can load at least through s_{t+1}, and since it
  loads as much as fits, g_{t+1} >= s_{t+1}.

So if S finishes all n packages in D days, G has shipped through at least n after D
days: G uses at most D days. The greedy count is the minimum, and "greedy days <= D"
is exactly "some schedule fits in D days".

**Part 3: the cows check is exact.** Fix a distance d. Claim: placing each cow in
the leftmost stall at least d past the previous cow places the most cows possible.
Take any valid placement P at positions p₁ < p₂ < ... < p_m and the greedy placement
g₁ < g₂ < .... By induction, g_i <= p_i for every i that P has: g₁ is the first stall,
so g₁ <= p₁; if g_i <= p_i, then p_{i+1} >= p_i + d >= g_i + d, so p_{i+1} is a stall at
least d past g_i, and the greedy, which takes the leftmost such stall, picks
g_{i+1} <= p_{i+1}. So the greedy places a cow for every cow P places: it places at
least m. "Greedy count >= k" is exactly "some placement of k cows has every gap at
least d".

**Monotonicity of both checks.** A ship of capacity c + 1 can run the exact schedule
of capacity c, so ok(c) implies ok(c + 1). A placement whose gaps are all at least
d + 1 has all gaps at least d, so ok(d + 1) implies ok(d). ∎
:::

The two greedy proofs are the same argument, and it has a name: **greedy stays
ahead**. After each step the greedy is at least as far along as any other valid
solution, so it cannot finish later. It is the argument to reach for whenever a
check inside this search is a left-to-right scan ([[greedy-exchange]] has the
general form).

Now list the assumptions, because each one is a bug when it fails.

1. **Monotone decision.** Proved separately for each problem, in one sentence: "a
   bigger boat can copy the smaller boat's schedule". If you cannot say that
   sentence, do not search. A decision where loosening the limit can hurt (say,
   "exactly k groups" when you cannot always split a group further) is not
   monotone.
2. **The check decides the same question the search asks.** "Greedy days <= D" is
   the question only because the greedy is optimal for a fixed capacity. A greedy
   that is not optimal gives a check that says no when the answer is yes, and the
   search returns a value that is too large.
3. **Honest ends.** lo must really fail and hi must really succeed (or the
   reverse for maximise). A hi that is not feasible ("max(w)" as a known yes for
   shipping) makes the search return it even when it fails.
4. **The order of the input is the order the problem fixes.** The ship check
   relies on "packages in the given order". The cows check relies on sorted stalls,
   and sorting is allowed because the problem does not care which stall is which.
   Sorting packages would answer a different problem.

## What it costs

Two numbers multiply: the cost of one check and the number of checks.

**The number of checks** is ⌈log₂(hi - lo)⌉, the same count as in [[binary-search]]
with the width of the value range instead of the array length. That is why huge
ranges are not scary:

| range of candidate answers | checks |
|---|---|
| up to 10^6 | 20 |
| up to 10^9 (speeds, capacities, coordinates) | 30 |
| up to 10^18 (budgets, alloy units, products of two 10^9 numbers) | 60 |

**The cost of one check** is usually one pass over the input, O(n). So the total is
**O(n log R)**, with R the width of the range. For Koko, n = 10^5 and R = 10^9: 30
passes of 10^5 is 3 · 10^6 steps, against 10^14 for the scan. For shipping, R is the
sum of the weights, so the number of passes is the number of bits in that sum.

**The costs people forget:**

- **Sorting goes outside the loop.** The cows check needs sorted stalls. Sort once,
  O(n log n), before the search. Sorting inside the check makes it O(n log n · log R)
  for no reason.
- **A check that is itself expensive.** If the check is a BFS over a grid, a DP or
  a sort, the total is that cost times log R. [[p:imc-rock-jumping|Rock Jumping]]
  has a one-pass greedy check, so its search is O(n log 10^9). If its check had been
  a shortest-path search, it would have been O((n log n) · 30), still fine, but count
  it before you commit.
- **Huge intermediate numbers.** In [[p:microsoft-maximum-alloy-production|Maximum Alloy Production Within Budget]]
  the candidate can be near 10^18 and composition up to 10^9, so the cost of a
  candidate can be near 10^27 · 10^5. Python handles that exactly but slowly; Java
  and C++ overflow silently. Either way, stop summing the moment the running cost
  exceeds the budget. The check only needs "over or not", not the exact total.
- **Real numbers.** On a continuous range there is no width 1. The number of steps
  is log₂(R / ε) for a target precision ε, and a fixed count of about 60 to 100
  halvings covers any double. See variation E.

**A comparison worth knowing.** The same "split into at most D contiguous parts,
minimise the largest" problem has a [[partition-dp|DP]] solution at O(n² · D). The
search with a greedy check is O(n log(sum)). For n = 10^5 the DP is hopeless and the
search is instant. When the decision version is greedy, searching on the answer is
not a trick, it is the faster algorithm.

## How to think about it

### The checklist

Ask these on every "least", "most", "minimise the maximum" or "maximise the
minimum" problem.

1. **What is the answer, as a number?** A speed, a capacity, a distance, a time, a
   length, a height. If the answer is a set or an arrangement, find the number
   inside it ("the largest load among the students").
2. **Can I phrase the decision?** "Is X enough?", "can every gap be at least X?",
   "can it be done in X seconds?". Write it in words.
3. **Is the decision monotone, and in which direction?** One sentence: "a bigger X
   can copy any solution of a smaller X". That decides minimise (first yes) or
   maximise (last yes).
4. **How do I check a fixed X?** Fixing X usually makes it greedy: fill each bin as
   much as fits, place each item as early as allowed, give the biggest job to the
   biggest worker. Sometimes it is a count ("at least k things are <= X?"),
   sometimes a sum of independent costs, rarely a BFS or DP. Prove the greedy, or at
   least test it against brute force.
5. **What are the honest ends?** A value that certainly fails and one that
   certainly succeeds. Use sentinels (0, -1, max + 1) rather than values you would
   have to evaluate.
6. **Does check cost × log(range) fit?** n · 30 almost always does. n log n · 60
   usually does.
7. **Integer or real?** Integers: stop at width 1. Reals: a fixed number of halvings.

Steps 2 and 3 are the insight. Step 4 is the work. The search itself is the
template from [[binary-search]], unchanged.

### Telling it from its neighbours

- **[[greedy]].** If a greedy rule builds the optimum directly, there is nothing to
  search. Here the greedy only answers the decision for a fixed X. A useful test:
  "could I greedily build the best solution without knowing the target?" If not, but
  you could with the target fixed, search on the answer.
- **[[partition-dp]].** "Split into k contiguous parts, minimise the largest sum"
  is both. With non-negative values the decision is greedy and the search wins. If
  the cost of a part is not monotone in its length (negative numbers, a cost that
  can shrink), the greedy check breaks and the DP is the safe tool.
- **[[binary-search]].** Same loop, different space. If the candidates are
  positions in a sorted array, it is the plain chapter. If they are values that
  exist only as numbers, this one.
- **[[ternary-search]].** If the quantity you optimise first improves and then
  gets worse (unimodal), you are not looking for a flip of a yes/no question but for
  a peak. Different shape, different search.
- **[[two-pointers]] and [[sliding-window]].** "The longest window with at most k
  bad elements" can be a search on the length with a sliding check, but the
  two-pointer window answers it directly in O(n). When the window answers the
  optimisation directly, skip the log factor.

## Variations

The family is four techniques, each with the same skeleton. For each: what
changes, why, a small example, and the problems that teach it.

### A. Minimise the maximum (capacity, speed, time, load)

**What changes:** the answer is an upper limit on something (a speed, a load per
day, the largest group). Larger limits are easier. Search the first yes.
**Why it works:** a larger limit can run any schedule a smaller one ran.
**Example:** Koko [1, 7, 10, 15], h = 10: answer 4, as traced.

- [[p:amazon-koko-eating-bananas|Koko Eating Bananas]]: the canonical first one.
  The check is a sum of independent ceilings.
- [[p:amazon-capacity-to-ship-packages-within-d-days|Capacity To Ship Packages Within D Days]]:
  the check becomes a greedy scan; the range is [max(w), sum(w)].
- [[p:google-minimize-maximum-pages-allocation|Minimize the Maximum Pages Allocated]]:
  the same as shipping, with students for days, plus a twist: every student needs at
  least one book, so more students than books is impossible (-1). The greedy count
  of "at most k segments" is enough, because a split into fewer segments can always
  be split further while there are enough books.
- [[p:drw-minimize-maximum-group-difference|Minimize Maximum Group Difference]]: the
  story says "groups", but once the array is sorted, the best groups are runs of it
  (any group's range only gets smaller if you swap an outsider for an element in
  between). The check for "three groups with range <= D?" starts a group at the
  smallest uncovered value, covers everything up to it + D, and counts. Sorted
  [1, 3, 4, 5, 6, 7, 8, 11, 12] with D = 3: [1, 3, 4], [5, 6, 7, 8], [11, 12], three
  groups, yes; D = 2: [1, 3], [4, 5, 6], [7, 8], [11, 12], four, no. Answer 3.
- [[p:doordash-minimum-multi-rider-processing-speed|Minimum Processing Speed with Multiple Riders]]:
  search the speed, and inside the check pack consecutive orders per rider, where an
  order's time is itself a ceiling. A search wrapped around a ship-style check that
  is wrapped around a Koko-style cost.

### B. Maximise the minimum (distance, gap, length, height)

**What changes:** the answer is a lower limit that every part must meet. Larger
limits are harder. Search the last yes; lo is the known yes.
**Why it works:** a solution meeting a stricter limit meets every looser one.
**Example:** cows [1, 2, 4, 8, 9], 3 cows: answer 3, as traced.

- [[p:peoplestrong-aggressive-cows|Aggressive Cows]] and its onsite twin
  [[p:amazon-maximize-minimum-robot-distance|Maximize the Minimum Distance Between Robots]]:
  sort, then greedy placement.
- [[p:google-cut-ribbons-equal-length|Cut Ribbons to Maximize Equal Length]]: the
  check is a sum, Σ ⌊r/L⌋ >= k. [9, 7, 5], k = 3: L = 5 gives 1 + 1 + 1 = 3, yes;
  L = 6 gives 1 + 1 + 0 = 2, no. Answer 5.
- [[p:amazon-woodcut-saw-height|Maximum Saw Height for At Least M Cut Length]]: the
  highest blade that still collects M wood. [20, 15, 10, 17] with M = 7: blade 15
  collects 5 + 0 + 0 + 2 = 7, yes; blade 16 collects 4 + 0 + 0 + 1 = 5, no. Answer 15.
  "Maximise" here is a maximise-the-limit, and the monotone direction is "a higher
  blade collects less".
- [[p:microsoft-maximize-pipeline-throughput-under-budget|Maximize Pipeline Throughput Under a Scaling Budget]]:
  the pipeline's throughput is its slowest service, so "can every service reach T
  within the budget?" is the decision. Each service's cost to reach T is independent:
  (⌈T / throughput[i]⌉ - 1) · scalingCost[i] if positive. With throughput [3, 2, 5],
  costs [2, 5, 10] and budget 28: T = 6 costs 2 + 10 + 10 = 22, yes; T = 7 costs 4 +
  15 + 10 = 29, no. Answer 6. "Maximise the minimum" is the giveaway; the check is a
  sum, not a greedy.
- [[p:imc-rock-jumping|Rock Jumping]]: rising water only removes rocks, so "can I
  still cross at water level L?" is monotone. The check is one pass: because a jump
  costs the square of its length, splitting a jump at a rock never costs more
  ((a + b)² >= a² + b²), so the best crossing uses every rock still above water.
  Walk them left to right, fail if any gap exceeds maxJump, and add up the squares
  against maxEnergy.

### C. A greedy check inside the search

**What changes:** the check itself takes thought. Fixing the target turns an
optimisation into a decision that a greedy answers exactly.
**Why it works:** with the limit fixed, a local rule ("take it if it fits", "take it
as early as allowed") is optimal by a stays-ahead argument, as in the proof.
**Example:** [[p:microsoft-minimum-nonadjacent-capability|Minimum Non-Adjacent Selection Capability]].
Values [2, 3, 5, 9], choose at least 2 non-adjacent positions, minimise the largest
chosen value. Directly, this looks like a DP over "take or skip". But fix a
capability c and ask "can I choose 2 non-adjacent positions with values <= c?". Now
a greedy is exact: scan left to right and take every allowed position whose
neighbour on the left was not taken. At c = 3: position 0 (2) taken, position 1 (3)
is adjacent, skip, position 2 (5) too big, position 3 (9) too big: 1 position, no.
At c = 5: position 0 taken, 1 skipped, 2 (5) taken: 2 positions, yes. Answer 5.
Taking the earliest allowed position stays ahead, for the same reason the earliest
cow does. The search is what made the DP unnecessary.

- [[p:agoda-printing-within-days|Feasibility of Printing Within Given Days]] is
  this check alone, with the limit given: print chapters in order under a daily
  limit, is it within d days? It is the ship check with no search around it, and a
  good first exercise.
- [[p:rippling-find-minimum-time|Find Minimum Time]]: the hard one. First rephrase:
  a processor that runs j processes needs 2j - 1 seconds (run, pause, run, ...), so
  "time <= T" means "each processor runs at most ⌊(T + 1)/2⌋ processes". Then the
  check is a matching: sort processes and processors from biggest to smallest, and
  give the biggest processes to the biggest processors, j at a time. If some process
  lands on a processor too small for it, no. The search is over T; the insight is the
  rephrasing, and the greedy is the matching.

### D. Huge ranges

**What changes:** the answer can be up to 10^18 or more. Nothing in the loop
changes; you just need honest ends and a check that does not explode.
**Why it works:** log₂(10^18) is 60. Sixty passes over 10^5 values is fine.
**Example:** [[p:microsoft-maximum-alloy-production|Maximum Alloy Production Within Budget]].
To make u units, metal i costs max(0, composition[i] · u - stock[i]) · cost[i]. Sum it,
stopping as soon as the sum passes the budget, and compare. A known yes is u = 0
(costs nothing). A known no is anything above (max stock + budget) / min composition,
or simply 2 · 10^18 + 1 within the stated limits.

**When there is no obvious upper end,** find one by doubling: test 1, 2, 4, 8, ...
until the check fails, then search between the last two. It costs about
2 log₂(answer) checks.

### E. Real numbers

**What changes:** the answer is a real number, so there is no "width 1". You stop
after a fixed number of halvings.
**Why it works:** each halving divides the width by 2. Starting from width R, after t
halvings it is R / 2^t. For R = 10^12, 100 halvings leave 10^12 / 2^100 ≈ 8 · 10^-19,
far below anything a double can tell apart near the answer.
**Example:** [[p:citadel-square-root|Square Root Function]]: the square root of x
is the boundary of "m · m >= x" over m in [0, max(1, x)].

Why not `while hi - lo > 1e-12`? Because doubles are not evenly spaced. Near 10^6,
two neighbouring doubles are about 1.2 · 10^-10 apart. For x = 10^12 the root is 10^6,
and once lo and hi are neighbouring doubles, (lo + hi) / 2 rounds to one of them, the
width is stuck at 1.2 · 10^-10, and the loop never ends. The program shows it, with
a cap so it does end:

```python run
def sqrt_eps(x, eps, cap=2000):
    lo, hi, it = 0.0, max(1.0, x), 0
    while hi - lo > eps and it < cap:
        mid = (lo + hi) / 2
        if mid * mid >= x: hi = mid
        else:              lo = mid
        it += 1
    return hi, it, hi - lo

def sqrt_fixed(x, rounds=100):
    lo, hi = 0.0, max(1.0, x)               # m*m < x at lo (or x = 0), m*m >= x at hi
    for _ in range(rounds):
        mid = (lo + hi) / 2
        if mid * mid >= x: hi = mid
        else:              lo = mid
    return hi

r, it, width = sqrt_eps(1e12, 1e-12)
print("eps loop on 1e12: stopped by the cap after", it, "rounds, width stuck at", width)
assert it == 2000 and width > 1e-12        # it would have spun forever

for x in (0.0, 1e-6, 0.25, 2.0, 10.0, 12345.678, 1e12):
    r = sqrt_fixed(x)
    print("sqrt(%g) ~ %.9g" % (x, r))
    assert abs(r - x ** 0.5) <= 1e-6 * max(1.0, x ** 0.5)   # the problem's tolerance

def isqrt(n):                               # the integer follow-up: largest m, m*m <= n
    lo, hi = 0, n + 1                       # lo works, hi fails
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if mid * mid <= n: lo = mid
        else:              hi = mid
    return lo
assert [isqrt(n) for n in (0, 1, 3, 4, 15, 16, 10**18)] == [0, 1, 1, 2, 3, 4, 10**9]
print("integer square roots by last_true: ok")
```

The follow-up in that problem, "what if the input is an integer?", turns it back
into an integer search: the largest m with m · m <= n, a last-true search with no
precision question at all. [[p:google-cut-ribbons-equal-length|Cut Ribbons]] asks the
same follow-up the other way: with fractional lengths, the loop becomes a fixed count
of halvings and the check uses ⌊r / L⌋ on reals. See [[numerical-stability]] for why
floats behave this way.

### F. Counting predicates: the k-th smallest of something you cannot list

**What changes:** the decision is "are there at least k items <= v?", and the items
are too many to list (all pair sums, all pair distances, all cells of a sorted
matrix, all products a[i] · b[j]).
**Why it works:** the count of items <= v never decreases as v grows, so the k-th
smallest is the first v whose count reaches k.
**Example:** the 4th smallest of all sums a + b with a in [1, 3] and b in [2, 5]. The
sums are 3, 6, 5, 8. Count <= 5: two (3, 5); count <= 6: three; count <= 8: four. The
first v with count >= 4 is 8. Each count is a two-pointer or bisect pass, never a
list of all pairs. This is less common in OAs than A and B, and common in onsites.

### G. Rarer forms

- **Maximise an average or a ratio.** "The subarray of length at least L with the
  largest average": search the average λ over the reals; "is there one with average
  >= λ?" becomes "is there one with Σ (a[i] - λ) >= 0?", a prefix-sum check. Rare in
  this bank, a classic elsewhere.
- **Search on time in a simulation.** "The earliest day when k bouquets can be
  made": search the day, check by scanning which flowers have bloomed. The same
  shape as Rock Jumping.

## Recognising it in a statement

Signals, the most reliable first.

1. **"Minimise the maximum"** or **"maximise the minimum"**. Almost always this
   technique. The words name the two directions.
2. **"The minimum capacity / speed / time / size such that ..."**, **"the maximum
   length / distance / height such that ..."**. The answer is a number with a
   property, and the property is a decision.
3. **A huge answer range with a small n.** Values up to 10^9 or 10^18 and n up to
   10^5. The answer cannot be found by counting up, and O(n) per candidate suggests
   O(n log R).
4. **"Within d days", "at most k groups", "no more than h hours", "a budget of B".**
   A resource limit that the decision version compares against.
5. **The order is fixed or irrelevant.** "Packages are loaded in order" (fixed: a
   left-to-right greedy check) or "positions may arrive unsorted" (irrelevant: sort,
   then check).
6. **A sample explanation that says "X works but X - 1 does not".** The Koko,
   ship and pipeline samples all say exactly that. The problem setter is telling you
   the answer is a boundary.

**Disguised forms.**

- "Three groups with the smallest largest range": sort, then minimise the maximum
  range with a greedy cover.
- "The highest water level at which you can still cross": maximise a level with a
  crossing check.
- "The fewest seconds for processors with a pause between jobs": rewrite time as a
  job count per processor, then search.
- "The most alloy within a budget": maximise units with a sum-of-costs check.
- "Choose at least k non-adjacent items to minimise the largest one": the DP-looking
  min-max, with a greedy check.

**Anti-signals.**

- The decision is not monotone. "Split into exactly k parts" with a cost where
  more parts can be worse. Check the one-sentence argument.
- The answer is found by a direct greedy or sort, with no limit in the statement to
  test against ("the cheapest way to buy the most items").
- "Feasibility" with nothing to optimise: course schedule, meeting room overlap.
  That is just the check.
- The quantity first improves, then worsens: that is a peak, [[ternary-search]].

## Traps

**The wrong direction.** Symptom: the answer is off by one, or always the end of
the range. Cause: the minimise loop used for a maximise problem, or the right loop
returning the wrong pointer. Demonstrated above with the cows. Cure: say what lo
and hi mean before writing the loop.

**A dishonest end.** Symptom: wrong answer when the optimum is at the edge of the
range. Cause: hi = max(weights) for shipping (that capacity may need more than d
days, so it is not a known yes), or lo = 1 for a speed that might be 1. Cure: argue each
end in one sentence, and use sentinels you never evaluate.

**Checking the sentinel.** Symptom: ZeroDivisionError on speed 0, or a cows check
called with d = 0. Cause: a loop variant that evaluates lo or hi. Cure: the
half-open template never calls the predicate on lo or hi.

**A greedy check that is not optimal.** Symptom: the answer is too large, and
brute force on a small case disagrees. Cause: for example, the ship check
"closing" a day early, or the cows check measuring from the previous stall instead
of the previous cow. Cure: prove stays-ahead, or test against brute force on random
small inputs as the programs above do.

**Floats where integers belong.** Symptom: an answer off by one on large inputs
only. Cause: `math.ceil(p / k)` converts to a double, and above 2^53 doubles cannot
hold every integer. Cure: `(p + k - 1) // k`. The demonstration:

```python run
import math

def hours_float(piles, k):  return sum(math.ceil(p / k) for p in piles)
def hours_int(piles, k):    return sum((p + k - 1) // k for p in piles)

p = 10**17 + 1
print("ceil(p / 1) with floats :", math.ceil(p / 1))
print("ceil(p / 1) in integers :", (p + 1 - 1) // 1)
assert math.ceil(p / 1) != p and (p + 1 - 1) // 1 == p

piles = [10**17 + 1, 3]
for k in (1, 10**17):
    print("k =", k, " float hours:", hours_float(piles, k), " integer hours:", hours_int(piles, k))
assert hours_float(piles, 10**17) == 2 and hours_int(piles, 10**17) == 3
print("the float check says 2 hours where the truth is 3: a speed that fails looks like it fits")
```

At k = 10^17, the pile of 10^17 + 1 needs two hours: 10^17 bananas in the first, one
in the second. In floats, (10^17 + 1) / 10^17 rounds to exactly 1.0, the ceiling is 1,
and the check believes the pile takes one hour. The search would accept a speed
that does not work.

**An eps loop on reals.** Symptom: a time limit on large inputs only. Cure: a fixed
number of halvings. Demonstrated in variation E.

**Sorting inside the check.** Symptom: correct but slow. Cure: sort once, outside.

**Overflow in the check.** Symptom (Java, C++): a negative cost that "fits" the
budget. Cure: stop summing as soon as the sum passes the limit, and use 64-bit
integers. In Python the symptom is only slowness, with the same cure.

## What to memorise

**The two loops.** One template, two readings:

```python
# minimise: lo fails, hi works, answer hi       # maximise: lo works, hi fails, answer lo
while hi - lo > 1:                               while hi - lo > 1:
    mid = lo + (hi - lo) // 2                        mid = lo + (hi - lo) // 2
    if ok(mid): hi = mid                             if ok(mid): lo = mid
    else:       lo = mid                             else:       hi = mid
return hi                                        return lo
```

**The sentence that turns a problem into it:** *the answer is a number; can I check
whether a given number is good enough, and does good enough stay good enough as I
loosen it?*

**The question that finds it:** *if someone handed me a candidate answer, could I
check it quickly?*

**The habit:** before the loop, write three lines in words: the decision, its
direction ("bigger is easier" or "bigger is harder"), and the two honest ends with
the reason each one fails or succeeds.

**The numbers:** 30 checks for 10^9, 60 for 10^18, about 100 halvings for any real
range. Total cost: check cost × that number.

## Check yourself

:::check
Hand trace. Koko with piles [3, 6, 7, 11] and h = 8. Set the honest ends, then run
the search, writing hours(mid) pile by pile at every step.
--
lo = 0 (speed 0 never finishes), hi = 11 (one hour per pile, 4 <= 8).

| lo | hi | mid | hours, pile by pile | total | <= 8? | move |
|---|---|---|---|---|---|---|
| 0 | 11 | 5 | 1 + 2 + 2 + 3 | 8 | yes | hi = 5 |
| 0 | 5 | 2 | 2 + 3 + 4 + 6 | 15 | no | lo = 2 |
| 2 | 5 | 3 | 1 + 2 + 3 + 4 | 10 | no | lo = 3 |
| 3 | 5 | 4 | 1 + 2 + 2 + 3 | 8 | yes | hi = 4 |
| 3 | 4 | | | | | stop: answer 4 |

Speed 3 needs 10 hours, speed 4 needs 8. The answer is 4. Note that speed 4 and
speed 5 both take 8 hours: the bar stays flat, and the search still finds the first
yes.
:::

:::check
Hand trace. Ship weights [3, 2, 2, 4, 1, 4] within 3 days. Give the honest ends and
run the search with the greedy day count at every step.
--
lo = max - 1 = 3 (the package of 4 does not fit), hi = sum = 16.

| lo | hi | mid | greedy days at capacity mid | days | <= 3? | move |
|---|---|---|---|---|---|---|
| 3 | 16 | 9 | [3, 2, 2] = 7, [4, 1, 4] = 9 | 2 | yes | hi = 9 |
| 3 | 9 | 6 | [3, 2] = 5, [2, 4] = 6, [1, 4] = 5 | 3 | yes | hi = 6 |
| 3 | 6 | 4 | [3], [2, 2], [4], [1], [4] | 5 | no | lo = 4 |
| 4 | 6 | 5 | [3, 2], [2], [4, 1], [4] | 4 | no | lo = 5 |
| 5 | 6 | | | | | stop: answer 6 |

At capacity 5, the 2 after [3, 2] would make 7, so day 2 starts at the second 2, and
the 4 after it would make 6, so day 3 starts at 4; [4, 1] = 5, then 4 alone. Four days.
:::

:::check
Hand trace. Stalls [0, 3, 4, 7, 10, 9] and 4 cows. Sort, choose the honest ends, and
find the largest minimum gap.
--
Sorted: [0, 3, 4, 7, 9, 10]. lo = 0 works; hi = span + 1 = 11 fails. (Tighter: 3
gaps over a span of 10 means the smallest gap is at most 3, so 4 fails.)

| lo | hi | mid | greedy placement | cows | >= 4? | move |
|---|---|---|---|---|---|---|
| 0 | 11 | 5 | 0, 7 (3, 4 too close), then 9, 10 too close to 7 | 2 | no | hi = 5 |
| 0 | 5 | 2 | 0, 3, 7, 9 | 4 | yes | lo = 2 |
| 2 | 5 | 3 | 0, 3, 7, 10 | 4 | yes | lo = 3 |
| 3 | 5 | 4 | 0, 4, 9 | 3 | no | hi = 4 |
| 3 | 4 | | | | | stop: answer 3 |

At distance 3 the placement 0, 3, 7, 10 has gaps 3, 4, 3, so the minimum is 3. At 4, the
greedy places only three cows, and greedy placement is optimal, so no placement of
four exists.
:::

:::check
Why does the ship problem's check use a greedy, while the ship problem itself
cannot be solved by a greedy? What changed?
--
The optimisation asks where to cut the sequence so the heaviest day is as light as
possible. Without knowing the target weight, there is no local rule for when to end a
day: ending early wastes capacity now, ending late may overload a later day.

The decision fixes the capacity. With a known limit, "keep loading while the next
package fits" is never worse than ending the day early, because a schedule that ends
early can be turned into the greedy one day by day without using more days (the
stays-ahead argument). Fixing the number removed the only thing the greedy could
not know. That is the general pattern: binary search on the answer supplies the
missing target, and the target makes the greedy safe.
:::

:::check
Someone solves "maximise the minimum distance between k cows" with the minimise
template, using pred(d) = "fewer than k cows fit at distance d", and returns hi.
Their answer on [1, 2, 4, 8, 9], k = 3 is 4. Where are they wrong, and what one-word
fix gives 3?
--
Their search is correct for the question they asked: "fewer than 3 cows fit at
distance d" is no for d <= 3 and yes for d >= 4, and the first yes is 4. But 4 is the
first distance that fails. The answer to the problem is the last distance that works,
which is the last no of their predicate: lo, not hi.

The fix is to return lo (= 3). Equivalently, use the positive check "at least k cows
fit" with lo as the known yes and return lo. The bug is not in the search, it is in
which end of the boundary they reported.
:::

:::check
Someone claims: "binary search on the answer always needs the answer to be one of the
input values, so I sort the input and search over it." Give a counterexample and say
when their approach is actually fine.
--
Koko with piles [1, 7, 10, 15] and h = 10: the answer is speed 4, which is not a pile.
Searching only over 1, 7, 10, 15 returns 7, the first pile size that works, which is
not minimal.

Their approach is fine when you can prove the optimum is an input value. In
Minimum Non-Adjacent Selection Capability, the answer is the largest chosen value,
which is some values[i], so searching over the sorted distinct values gives the same
answer as searching over the whole range. Searching the range is always safe; searching
the input values needs that proof.
:::

:::check
Disguised problem. "n workers stand in a line with tasks of sizes t[0..n-1] that must
be done in order. You may hire at most m identical machines; each machine takes a
contiguous block of tasks and needs time equal to the block's total size. Return the
least time in which all tasks finish, the machines working at the same time." Reduce
it to this chapter: the decision, the direction, the ends, the check, the cost.
--
The finishing time is the largest block total, so the answer is the least T such that
the tasks can be cut into at most m contiguous blocks, each with total at most T.

- Decision: "can the tasks be cut into at most m blocks of total <= T?"
- Direction: bigger T is easier (any cut that works for T works for T + 1). Minimise:
  first yes.
- Ends: max(t) - 1 fails (the largest task fits in no block), sum(t) works (one block).
- Check: greedy, fill each block while the next task fits, count blocks, compare with m.
  This is the ship check with machines for days.
- Cost: O(n) per check, O(n log(sum t)) in total.

It is Capacity To Ship Packages wearing a different story, and the same as Minimize
the Maximum Pages Allocated.
:::
