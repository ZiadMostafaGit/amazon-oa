# Prefix Sums and Difference Arrays

> Every range of an array is the difference of two prefixes, so n + 1 running totals computed once answer every range question, and a question about subarrays becomes a question about pairs of those totals.

## The problem it solves

You are given an array of numbers and a list of questions. Each question names two
positions, `l` and `r`, and asks for the sum of everything from `a[l]` to `a[r]`,
both ends included. That is
[[p:intuit-static-range-sums|Range Sum Queries]] exactly as this bank states it:
up to 200,000 numbers and up to 200,000 questions, every value between -10^9 and
10^9.

The first solution anyone writes is the honest one. For each question, walk from
`l` to `r` and add.

```python
def answer(a, queries):
    out = []
    for l, r in queries:
        s = 0
        for i in range(l, r + 1):
            s += a[i]
        out.append(s)
    return out
```

It is correct, and it is too slow. A question can cover the whole array, so one
question costs up to n additions, and q questions cost up to n times q. With
n = q = 200,000 that is 4 times 10^10 additions. A fast machine does a few
hundred million simple operations a second, so this runs for minutes. The limit
is a second or two.

This chapter builds a version that does n additions once, before any question is
read, and then answers each question with **one subtraction**. Total work: about
n + q, which is 400,000 instead of 40,000,000,000. The same idea, read
backwards, turns "add v to every position from l to r" from a loop into two
writes. And the same idea, read sideways, turns "how many subarrays have sum k"
from a double loop into one pass with a dictionary. Those three uses are most of
the topic.

Three hundred problems in this bank use prefix sums, which puts the topic at
\#29 of 150. Most are small: a running total that is the answer, a split point
where the left part balances the right part, a count of subarrays. A few are
disguised so well that the prefix sum is the whole insight.

### When it is the wrong tool

- **The array changes between questions.** A prefix total is a snapshot. Change
  `a[3]` and every total from position 4 onward is stale; fixing them costs O(n)
  per change. When updates and questions interleave, you want a
  [[fenwick-tree]] or a [[segment-tree]].
- **The question is a minimum, a maximum or a gcd over the range.** These have no
  "undo". Knowing the minimum of `a[0..9]` and the minimum of `a[0..3]` tells you
  nothing about the minimum of `a[4..9]`, because the small element may sit in the
  part you are throwing away. You want a [[sparse-table]], a [[segment-tree]] or a
  [[monotonic-deque]].
- **Every value is non-negative and you want one best window.** Then a
  [[sliding-window]] does the job with no extra array. Prefix sums still work, but
  the window is leaner. The moment a negative number is allowed, the window breaks
  and prefix sums are the tool; we will watch the window break below.

## Build it from the brute force

We will not start with the prefix array. We will start with the loop above, count
what it does, find the work it repeats, and remove that repetition. The prefix
array will appear at the end as the obvious thing to store.

### Step 1: count the brute force

Take a small array, the one used through the whole chapter:

| index | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| a | 3 | -1 | 4 | -1 | 5 | -9 |

Ask two questions: the sum of `a[1..4]` and the sum of `a[2..5]`.

- `a[1..4]` = -1 + 4 + (-1) + 5 = 7. Four additions.
- `a[2..5]` = 4 + (-1) + 5 + (-9) = -1. Four additions.

Eight additions for two questions. In general a question over a range of length
L costs L additions, and nothing in the loop remembers anything between
questions. Each question starts from zero.

### Step 2: notice the waste

Look at what the two questions shared.

<svg viewBox="0 0 680 230" role="img" aria-label="two range questions drawn as bars over the array 3, -1, 4, -1, 5, -9; the first covers indices 1 to 4, the second covers 2 to 5, and the shaded overlap 2 to 4 is added twice by the brute force">
  <g>
    <rect x="60" y="30" width="90" height="40" rx="4"/>
    <rect x="150" y="30" width="90" height="40" rx="4"/>
    <rect class="fill" x="240" y="30" width="90" height="40" rx="4"/>
    <rect class="fill" x="330" y="30" width="90" height="40" rx="4"/>
    <rect class="fill" x="420" y="30" width="90" height="40" rx="4"/>
    <rect x="510" y="30" width="90" height="40" rx="4"/>
    <text x="105" y="56" text-anchor="middle">3</text>
    <text x="195" y="56" text-anchor="middle">-1</text>
    <text x="285" y="56" text-anchor="middle">4</text>
    <text x="375" y="56" text-anchor="middle">-1</text>
    <text x="465" y="56" text-anchor="middle">5</text>
    <text x="555" y="56" text-anchor="middle">-9</text>
    <text x="105" y="20" text-anchor="middle">0</text>
    <text x="195" y="20" text-anchor="middle">1</text>
    <text x="285" y="20" text-anchor="middle">2</text>
    <text x="375" y="20" text-anchor="middle">3</text>
    <text x="465" y="20" text-anchor="middle">4</text>
    <text x="555" y="20" text-anchor="middle">5</text>
    <line x1="150" y1="100" x2="510" y2="100"/>
    <line x1="150" y1="92" x2="150" y2="108"/>
    <line x1="510" y1="92" x2="510" y2="108"/>
    <text x="330" y="125" text-anchor="middle">question 1: a[1..4] = 7, four additions</text>
    <line x1="240" y1="155" x2="600" y2="155"/>
    <line x1="240" y1="147" x2="240" y2="163"/>
    <line x1="600" y1="147" x2="600" y2="163"/>
    <text x="420" y="180" text-anchor="middle">question 2: a[2..5] = -1, four additions</text>
    <text x="340" y="215" text-anchor="middle">shaded: 4 + (-1) + 5 = 8 is added by both questions</text>
  </g>
</svg>

The shaded cells, 4, -1 and 5, were added up twice. With 200,000 questions over
200,000 numbers, most cells are covered by thousands of questions, and each
question adds them again. That repetition is the whole cost.

### You might think: "Cache the answer to each question."

A dictionary from (l, r) to the sum helps only if the same question is asked
twice. In the example the questions are different: (1, 4) and (2, 5). They
share work, not answers. There are n(n+1)/2 possible questions, about 2 times
10^10 for n = 200,000, so a table of every possible answer cannot even be built.
Caching answers is the wrong grain. We need to cache **pieces** that every
answer can be assembled from.

### You might think: "Precompute the sum of every block of 1000."

That is a real technique ([[sqrt-decomposition]]), and it brings a question down
to about 2 times sqrt(n) additions. It is also more work than the real answer,
which assembles every range from exactly **two** stored numbers. Keep looking.

### The question that unlocks it

So the question is not "how do I add faster". It is this:

**Which few numbers, computed once, can every range answer be built from?**

Try the simplest candidates. Store the sum of `a[0..r]` for every r, the sum of
everything from the start up to r. Call it the prefix total. There are only n
of them, and they are cheap: each is the previous one plus one element.

Now look at question 1 again. The sum of `a[1..4]` is "everything up to 4" minus
"everything up to 0":

- everything up to 4: 3 + (-1) + 4 + (-1) + 5 = 10
- everything up to 0: 3
- difference: 10 - 3 = 7. That is the answer.

It works because the part you subtract is exactly the part you did not want. The
range `a[1..4]` is "the road from the start to the end of cell 4" with "the road
from the start to the end of cell 0" cut off.

Say it a second way, as a picture of a road. Put a milestone at every boundary
between cells. The milestone tells you the distance travelled from the start.
The length of any stretch of road is the far milestone minus the near milestone.
You never measure a stretch; you read two signs and subtract.

That is the answer to the unlocking question: **n + 1 milestones.** One per
boundary, including the boundary before the first cell, whose milestone reads 0.

### You might think: "The sum of a[l..r] is pre[r] - pre[l]."

This is the most common first formula, and it is wrong by one cell. If `pre[r]`
means "sum of `a[0..r]`", then `pre[r] - pre[l]` removes `a[l]` too, which you
wanted to keep. The smallest counterexample is one element: `a = [5]`, question
(0, 0). The formula gives `pre[0] - pre[0] = 0`. The answer is 5.

The fix people reach for is `pre[r] - pre[l-1]`, which is right, but breaks when
l = 0, because `pre[-1]` does not exist (and in Python it silently reads the last
element, which is worse). So they add a special case. Every special case is a
place for a bug.

The clean fix is to put the milestones on the boundaries, as in the road
picture. Define

> P[i] = the sum of the **first i** elements, a[0] + ... + a[i-1].

So P[0] = 0 (the sum of no elements), P[1] = a[0], P[2] = a[0] + a[1], and
P[n] is the total. P has n + 1 entries, one per boundary. The range `a[l..r]`
starts at boundary l and ends at boundary r + 1, so

> sum of a[l..r] = P[r + 1] - P[l]

with no special case, ever. When l = 0 it reads `P[r+1] - P[0] = P[r+1] - 0`,
which is right because boundary 0 exists like any other.

### Step 3: build the milestones in one pass

P[i + 1] is P[i] plus one more element: `P[i + 1] = P[i] + a[i]`. So a single
loop from left to right fills P with n additions. That is the prefix sum.

### Step 4: the same idea, asked about subarrays

The second family of problems does not give you the ranges. It asks you to find
them. [[p:apple-subarray-sum-equals-k|Subarray Sum Equals K]]: how many
contiguous subarrays have sum exactly k?

The brute force tries every (l, r) pair. With P built, each pair costs one
subtraction, so the brute force is n(n+1)/2 subtractions: about 2 times 10^8 for
the bank's n = 20,000. That passes in C++ and is slow in Python. More important,
it still wastes work, and the waste has the same shape as before.

Fix the right end r. The question "how many l make `a[l..r]` sum to k?" becomes,
using the formula, "how many l make `P[r+1] - P[l] = k`?", which is "how many of
the earlier milestones P[0], ..., P[r] equal `P[r+1] - k`?" That is not a loop.
That is a lookup in a dictionary that counts how many times each milestone value
has appeared so far.

So scan left to right. At each position, compute the new milestone, ask the
dictionary how many earlier milestones equal `milestone - k`, add that to the
answer, then record the new milestone in the dictionary. One pass, O(n).

The unlocking question has a second form here, and it is the most reusable
sentence in the chapter: **a property of a subarray is a relation between two
milestones.** "Sum is k" is "the milestones differ by k". "Sum divisible by m"
is "the milestones have the same remainder mod m". "Equal numbers of X and Y" is
"the milestones of a +1/-1 balance are equal". Find the relation, and the
dictionary counts the pairs.

### You might think: "A sliding window does this in O(1) space."

A sliding window keeps a left and a right end and moves them forward: grow on the
right, and shrink from the left while the sum is too big. It is correct when every
number is non-negative, because then growing can only raise the sum and shrinking
can only lower it, so "too big" is always repaired by shrinking.

With a negative number the logic breaks. Take `a = [1, -1, 1]`, k = 1. The
subarrays with sum 1 are `[1]` at index 0, `[1]` at index 2, and `[1, -1, 1]`:
three. The window grows to index 0 (sum 1, count it), grows to index 1 (sum 0),
grows to index 2 (sum 1, count it). It never had a reason to shrink, so it never
looked at the subarray that starts at index 2. It reports 2. The negative number
made a longer window smaller, and the window's whole logic ("longer means
bigger") was false.

Prefix sums do not care about signs. The milestones go up and down, and the
dictionary does not mind.

### Step 5: the same idea, run backwards (the difference array)

The third family is the opposite asymmetry. Many **writes** over ranges, one read
at the end. [[p:google-range-booking-totals|Range Booking Totals]]: n time slots,
and each booking adds `units` to every slot from `start` to `end`. Report every
slot's total.

The brute force loops over the slots of each booking: up to n writes per booking,
n times the number of bookings in total. The waste is again visible. After all the
bookings, look at the final array and ask where it changes. Inside a booking's
range, neighbouring slots receive the same amount from it; the booking only makes
a difference at its two edges: it starts adding at `start`, and stops adding just
after `end`.

So store the **changes** instead of the values. Let D[i] be "how much slot i
differs from slot i - 1". A booking of v units over `[l, r]` changes exactly two
of those differences: slot l is v more than its left neighbour, and slot r + 1 is
v less than its left neighbour. Everything in between is unchanged, because both
neighbours got the same v. So a booking is two writes: `D[l] += v` and
`D[r+1] -= v`.

At the end, the value of slot i is the sum of all the differences up to it: a
prefix sum of D. The difference array and the prefix sum undo each other, the way
subtraction and addition do. That is why the two belong in one chapter.

### The technique in one sentence

**Store the running total at every boundary, P[i] = sum of the first i elements,
so that any range is P[r+1] - P[l], any subarray condition is a relation between
two of these totals, and any range update is two changes to the array whose
running total is the answer.**

And the question that produced it, worth asking on every new problem: **which few
numbers, computed once, can every range answer be built from?** For sums the
answer is the n + 1 boundary totals, and it works because subtraction undoes
addition.

## Worked by hand

### Trace 1: build P and answer three questions

`a = [3, -1, 4, -1, 5, -9]`. Start with P[0] = 0, then P[i + 1] = P[i] + a[i].

| step i | a[i] | computed | P so far |
|---|---|---|---|
| (start) | | P[0] = 0 | [0] |
| 0 | 3 | P[1] = 0 + 3 = 3 | [0, 3] |
| 1 | -1 | P[2] = 3 + (-1) = 2 | [0, 3, 2] |
| 2 | 4 | P[3] = 2 + 4 = 6 | [0, 3, 2, 6] |
| 3 | -1 | P[4] = 6 + (-1) = 5 | [0, 3, 2, 6, 5] |
| 4 | 5 | P[5] = 5 + 5 = 10 | [0, 3, 2, 6, 5, 10] |
| 5 | -9 | P[6] = 10 + (-9) = 1 | [0, 3, 2, 6, 5, 10, 1] |

Here is the same array with the milestones drawn where they live, on the
boundaries.

<svg viewBox="0 0 680 250" role="img" aria-label="the array 3, -1, 4, -1, 5, -9 with prefix milestones P0 to P6 on the boundaries between cells, reading 0, 3, 2, 6, 5, 10, 1, and a bracket showing that a[1..3] is P4 minus P1, 5 minus 3, equals 2">
  <g>
    <rect x="60" y="36" width="80" height="44" rx="4"/>
    <rect class="fill" x="140" y="36" width="80" height="44" rx="4"/>
    <rect class="fill" x="220" y="36" width="80" height="44" rx="4"/>
    <rect class="fill" x="300" y="36" width="80" height="44" rx="4"/>
    <rect x="380" y="36" width="80" height="44" rx="4"/>
    <rect x="460" y="36" width="80" height="44" rx="4"/>
    <text x="100" y="64" text-anchor="middle">3</text>
    <text x="180" y="64" text-anchor="middle">-1</text>
    <text x="260" y="64" text-anchor="middle">4</text>
    <text x="340" y="64" text-anchor="middle">-1</text>
    <text x="420" y="64" text-anchor="middle">5</text>
    <text x="500" y="64" text-anchor="middle">-9</text>
    <text x="20" y="64">a</text>
    <line x1="60" y1="84" x2="60" y2="112"/>
    <line x1="140" y1="84" x2="140" y2="112"/>
    <line x1="220" y1="84" x2="220" y2="112"/>
    <line x1="300" y1="84" x2="300" y2="112"/>
    <line x1="380" y1="84" x2="380" y2="112"/>
    <line x1="460" y1="84" x2="460" y2="112"/>
    <line x1="540" y1="84" x2="540" y2="112"/>
    <text x="60" y="128" text-anchor="middle">P0</text>
    <text x="140" y="128" text-anchor="middle">P1</text>
    <text x="220" y="128" text-anchor="middle">P2</text>
    <text x="300" y="128" text-anchor="middle">P3</text>
    <text x="380" y="128" text-anchor="middle">P4</text>
    <text x="460" y="128" text-anchor="middle">P5</text>
    <text x="540" y="128" text-anchor="middle">P6</text>
    <text x="60" y="148" text-anchor="middle">0</text>
    <text x="140" y="148" text-anchor="middle">3</text>
    <text x="220" y="148" text-anchor="middle">2</text>
    <text x="300" y="148" text-anchor="middle">6</text>
    <text x="380" y="148" text-anchor="middle">5</text>
    <text x="460" y="148" text-anchor="middle">10</text>
    <text x="540" y="148" text-anchor="middle">1</text>
    <text x="20" y="128">P</text>
    <line x1="140" y1="182" x2="380" y2="182"/>
    <line x1="140" y1="182" x2="140" y2="170"/>
    <line x1="380" y1="182" x2="380" y2="170"/>
    <text x="260" y="204" text-anchor="middle">a[1..3] starts at boundary 1, ends at boundary 4</text>
    <text x="260" y="228" text-anchor="middle">P4 - P1 = 5 - 3 = 2</text>
  </g>
</svg>

Now answer questions with no further additions.

| question | formula | arithmetic | check by hand |
|---|---|---|---|
| a[1..3] | P[4] - P[1] | 5 - 3 = 2 | -1 + 4 - 1 = 2 |
| a[1..4] | P[5] - P[1] | 10 - 3 = 7 | -1 + 4 - 1 + 5 = 7 |
| a[2..5] | P[6] - P[2] | 1 - 2 = -1 | 4 - 1 + 5 - 9 = -1 |
| a[0..5] | P[6] - P[0] | 1 - 0 = 1 | the whole array = 1 |
| a[4..4] | P[5] - P[4] | 10 - 5 = 5 | a[4] = 5 |

The story of one question in words: "I want `a[2..5]`. That stretch starts at
boundary 2 and ends at boundary 6. The milestone at boundary 6 says 1: the whole
array sums to 1. The milestone at boundary 2 says 2: the first two cells sum to 2.
Everything from boundary 2 to boundary 6 is the whole road minus the first two
cells, 1 - 2 = -1."

Two things the trace shows that the formula alone does not.

**Every question uses an index one larger than the one you would write first.**
`a[1..3]` uses P[4], not P[3]. If you say P[i] out loud as "the sum of the first i
elements", the +1 writes itself: the first 4 elements are `a[0..3]`.

**P goes up and down.** It reads 0, 3, 2, 6, 5, 10, 1. That is because the array
has negatives. This one fact rules out two tempting shortcuts: you cannot binary
search P for "the first prefix at least X", and you cannot assume a longer range
has a bigger sum. When every element is non-negative, P never decreases, and both
shortcuts become legal. The sign of the input decides which tools you may use.

### Trace 2: counting subarrays, where a milestone repeats

`a = [2, -2, 3, -3, 3]`, k = 3. Count the subarrays with sum 3. The dictionary
`seen` maps a milestone value to how many times it has appeared. It starts as
`{0: 1}`, because milestone P[0] = 0 exists before any element is read. At each
step: add the element to `run`, look up `run - k`, add the count to `total`, then
record `run`.

| step | x | run (new milestone) | look up run - 3 | found | total | seen after |
|---|---|---|---|---|---|---|
| start | | 0 | | | 0 | {0: 1} |
| 0 | 2 | 2 | -1 | 0 | 0 | {0: 1, 2: 1} |
| 1 | -2 | 0 | -3 | 0 | 0 | {0: 2, 2: 1} |
| 2 | 3 | 3 | 0 | 2 | 2 | {0: 2, 2: 1, 3: 1} |
| 3 | -3 | 0 | -3 | 0 | 2 | {0: 3, 2: 1, 3: 1} |
| 4 | 3 | 3 | 0 | 3 | 5 | {0: 3, 2: 1, 3: 2} |

The answer is 5. The story of step 4 in words: "I have read the whole array and my
milestone is 3. A subarray ending here sums to 3 exactly when it starts at a
boundary whose milestone is 3 - 3 = 0. The dictionary says milestone 0 has been
seen three times: at boundary 0, at boundary 2, and at boundary 4. Those are
three different subarrays: `a[0..4]`, `a[2..4]` and `a[4..4]`, each summing to 3."

Check the five by hand: `[2, -2, 3]`, `[3]` at index 2, `[2, -2, 3, -3, 3]`,
`[3, -3, 3]`, `[3]` at index 4. All sum to 3, and no other subarray does.

This trace shows two things the first one could not.

**The dictionary must count, not just remember.** Milestone 0 appears three
times. A set would answer "yes, 0 has been seen" and the step would add 1 instead
of 3. The answer would be 2 instead of 5.

**The seed `{0: 1}` is boundary 0.** Without it, step 2 finds one 0 instead of
two, and misses `a[0..2]`; step 4 misses `a[0..4]`. Every subarray that starts at
index 0 is lost. That is the same bug as forgetting P[0], in dictionary form.

### Trace 3: range writes with a difference array

The example from [[p:google-range-booking-totals|Range Booking Totals]]: n = 5
slots numbered 1 to 5, bookings `[1, 3, 4]`, `[2, 5, 2]`, `[4, 4, 7]` (start,
end, units). D gets slots 0 to 6: slots 1..5 are real, and slot 6 exists so that
a booking ending at slot 5 has somewhere to write its "stop".

| booking | writes | D[0..6] after |
|---|---|---|
| (start) | | [0, 0, 0, 0, 0, 0, 0] |
| [1, 3, 4] | D[1] += 4, D[4] -= 4 | [0, 4, 0, 0, -4, 0, 0] |
| [2, 5, 2] | D[2] += 2, D[6] -= 2 | [0, 4, 2, 0, -4, 0, -2] |
| [4, 4, 7] | D[4] += 7, D[5] -= 7 | [0, 4, 2, 0, 3, -7, -2] |

Now the running total of D over slots 1 to 5: 4, 4 + 2 = 6, 6 + 0 = 6, 6 + 3 =
9, 9 - 7 = 2. The answer is `[4, 6, 6, 9, 2]`, which is the expected output.

The story of slot 4 in words: "D[4] is 3. That means slot 4 holds 3 more than slot
3. Why? The first booking stopped before slot 4 (-4), and the third booking
started at slot 4 (+7). Slot 3 held 6, so slot 4 holds 9."

What this shows: the bookings never interacted. The third one did not need to know
about the first two; it wrote two cells and left. You can apply a million bookings
in any order before you look at the result.

## From the idea to the code

### The direct version, against the brute force

This block builds P, answers questions both ways, counts the additions each way,
and checks every possible range against the honest loop.

```python run
def build(a):
    P = [0] * (len(a) + 1)          # one milestone per boundary; P[0] = 0
    for i, x in enumerate(a):
        P[i + 1] = P[i] + x         # the first i+1 elements = first i, plus a[i]
    return P

def range_sum(P, l, r):             # a[l..r], both ends included
    return P[r + 1] - P[l]          # boundary r+1 minus boundary l

a = [3, -1, 4, -1, 5, -9]
P = build(a)
print("a =", a)
print("P =", P)
assert P == [0, 3, 2, 6, 5, 10, 1]

for l, r in [(1, 3), (1, 4), (2, 5), (0, 5), (4, 4)]:
    print("a[%d..%d] = P[%d] - P[%d] = %d" % (l, r, r + 1, l, range_sum(P, l, r)))
assert range_sum(P, 2, 5) == -1 and range_sum(P, 4, 4) == 5

n = len(a)
for l in range(n):                  # every range agrees with the honest loop
    for r in range(l, n):
        assert range_sum(P, l, r) == sum(a[l:r + 1])

# cost: q questions that each cover the whole array
import random
random.seed(7)
big = [random.randint(-10**9, 10**9) for _ in range(2000)]
queries = [(0, len(big) - 1)] * 2000
brute_adds = sum(r - l + 1 for l, r in queries)
fast_ops = len(big) + len(queries)  # n additions to build, 1 subtraction each
print("brute additions:", brute_adds, " prefix operations:", fast_ops)
assert brute_adds == 4_000_000 and fast_ops == 4_000
Pb = build(big)
assert range_sum(Pb, 0, 1999) == sum(big)
```

### Each line, and which part of the idea it is

| line | in words | which part of the derivation |
|---|---|---|
| `P = [0] * (len(a) + 1)` | one slot per boundary, n + 1 of them, all 0 | the milestones; P[0] = 0 is the boundary before the array |
| `P[i + 1] = P[i] + x` | the first i+1 elements are the first i, plus one more | Step 3, the one-pass build |
| `return P[r + 1] - P[l]` | far milestone minus near milestone | the answer to the unlocking question |

Three boring confusions, settled.

**P is indexed by boundaries, a by cells.** `a[i]` is cell i. `P[i]` is the
boundary *before* cell i, so it holds the sum of cells 0..i-1. That is why P[i]
does not include a[i]. It is not a convention you memorise; it is what a boundary
is.

**Why P[0] exists.** Because boundary 0 exists. It is the start of the road, and
the distance travelled there is 0. Deleting it means every range starting at 0 needs
a special case.

**What a cell of P does and does not store.** It stores one number, a total. It
does not store which elements produced it, and it does not store the element at
that position. You get an element back as `P[i+1] - P[i]`, which is the
difference array of P: the two operations undo each other.

### The counting version, and the line that has to come first

Here is the counting loop from Step 4, with its brute force. Look at the order of
the three lines inside the loop: update `run`, then look up, then insert.

```python run
def count_brute(a, k):
    n = len(a)
    return sum(1 for l in range(n) for r in range(l, n) if sum(a[l:r + 1]) == k)

def count_right(a, k):
    seen = {0: 1}                           # boundary 0, before any element
    run = total = 0
    for x in a:
        run += x                            # the new milestone
        total += seen.get(run - k, 0)       # earlier milestones only
        seen[run] = seen.get(run, 0) + 1    # now this one becomes "earlier"
    return total

def count_wrong(a, k):
    seen = {0: 1}
    run = total = 0
    for x in a:
        run += x
        seen[run] = seen.get(run, 0) + 1    # inserted BEFORE the lookup
        total += seen.get(run - k, 0)
    return total

def trace(a, k, insert_first):
    seen, run, total = {0: 1}, 0, 0
    for i, x in enumerate(a):
        run += x
        if insert_first:
            seen[run] = seen.get(run, 0) + 1
        found = seen.get(run - k, 0)
        total += found
        if not insert_first:
            seen[run] = seen.get(run, 0) + 1
        print("   step %d: run=%2d look up %2d found %d total %d  seen=%s"
              % (i, run, run - k, found, total, dict(sorted(seen.items()))))
    return total

a, k = [1, -1, 2], 0
print("a =", a, "k =", k, " brute:", count_brute(a, k))
print(" look up, then insert (right):")
r = trace(a, k, insert_first=False)
print(" insert, then look up (wrong):")
w = trace(a, k, insert_first=True)
assert r == count_brute(a, k) == 1 and w == 4
assert w - r == len(a)                       # one empty subarray per step

import random
random.seed(3)
for _ in range(300):
    b = [random.randint(-3, 3) for _ in range(random.randint(0, 9))]
    kk = random.randint(-4, 4)
    assert count_right(b, kk) == count_brute(b, kk)
    if kk != 0:                              # the wrong order hides when k != 0
        assert count_wrong(b, kk) == count_brute(b, kk)
print("right order matches brute force on 300 cases; wrong order fails only at k = 0")
assert count_right([2, -2, 3, -3, 3], 3) == 5
```

Read the two traces side by side. At step 0 the right version looks up 1 - 0 = 1,
finds nothing (only milestone 0 is recorded), and then records 1. The wrong version
records 1 first, then looks up 1 and finds the milestone **it just wrote**. That
cell is where it goes wrong. A match between milestone r+1 and itself is the range
from boundary r+1 to boundary r+1: the empty subarray. Its sum is 0, so it matches
exactly when k = 0.

So the wrong version accidentally counts every empty subarray too: one per step,
n extra in total. Here it reports 4 = 1 + 3. And because a milestone can only
match itself when `run - k == run`, the bug is invisible for every k other than 0.
It passes every test you are likely to write first. That is what makes it the
subtle line.

Say it a second way. The dictionary must hold the milestones *strictly to the
left* of the right end. "Look up, then insert" keeps that promise. "Insert, then
look up" breaks it by one cell.

### The difference array, and its own subtle line

The difference array has a similar one-character trap: `D[r + 1] -= v`, not
`D[r] -= v`. The second is not random noise. It computes something specific.

```python run
def apply_right(n, bookings):           # slots 1..n, bookings [start, end, units]
    D = [0] * (n + 2)                   # slot n+1 catches the "stop" of the last slot
    for l, r, v in bookings:
        D[l] += v
        D[r + 1] -= v                   # stop adding AFTER slot r
    out, run = [], 0
    for i in range(1, n + 1):
        run += D[i]
        out.append(run)
    return out

def apply_wrong(n, bookings):
    D = [0] * (n + 2)
    for l, r, v in bookings:
        D[l] += v
        D[r] -= v                       # stops adding AT slot r
    out, run = [], 0
    for i in range(1, n + 1):
        run += D[i]
        out.append(run)
    return out

def apply_naive(n, bookings):
    out = [0] * (n + 1)
    for l, r, v in bookings:
        for i in range(l, r + 1):
            out[i] += v
    return out[1:]

bookings = [[1, 3, 4], [2, 5, 2], [4, 4, 7]]
print("right:", apply_right(5, bookings))
print("wrong:", apply_wrong(5, bookings), "<- each booking loses its last slot")
assert apply_right(5, bookings) == apply_naive(5, bookings) == [4, 6, 6, 9, 2]
assert apply_wrong(5, bookings) == [4, 6, 2, 2, 0]

# what the wrong one really computes: half-open ranges [l, r)
half_open = apply_naive(5, [[l, r - 1, v] for l, r, v in bookings])
assert apply_wrong(5, bookings) == half_open
print("wrong == the right answer for ranges [l, r), end excluded")

# order of bookings never matters
assert apply_right(5, bookings[::-1]) == apply_right(5, bookings)
```

The wrong version gets slot 3 wrong first: it shows 2 instead of 6, because the
first booking stopped *at* slot 3 instead of after it. And the single-slot booking
`[4, 4, 7]` disappears entirely: +7 and -7 land in the same cell and cancel. What it
accidentally computes is the half-open version, ranges `[l, r)` with the end
excluded. If a problem says "from login day to the day before logout", that is the
right formula. Read the sentence, then choose `r` or `r + 1` on purpose.

## Why it is correct

:::proof Milestones answer ranges, count subarrays, and apply range writes
**What we claim.** (1) After the build loop, P[j] is the sum of the first j
elements for every j from 0 to n. (2) The sum of `a[l..r]` equals P[r+1] - P[l].
(3) The counting loop counts every subarray with sum k exactly once. (4) After the
difference writes, the running total of D at slot i equals the true value of slot i.

**Claim 1, by induction on j.** For j = 0, P[0] was set to 0, and the sum of the
first 0 elements is the empty sum, 0. Suppose P[j] is the sum of the first j
elements. The loop sets P[j+1] = P[j] + a[j], which is (a[0] + ... + a[j-1]) +
a[j], the sum of the first j+1 elements. Nothing writes P[j] again after that, so
every entry stays correct.

**Claim 2.** The first r+1 elements are `a[0..r]`. Split them into two blocks
that sit next to each other: the first l elements `a[0..l-1]`, and the rest,
`a[l..r]`. Adding the two blocks gives the whole, so P[r+1] = P[l] + S, where S is
the sum we want. Subtract P[l] from both sides: S = P[r+1] - P[l]. The step that
made this possible is "subtract from both sides", which needs subtraction to undo
addition. That is the only place the proof uses anything special about +.

**Claim 3.** Every non-empty subarray `a[l..r]` has exactly one start boundary l
and one end boundary r+1, with l < r+1, and by claim 2 its sum is k exactly when
P[r+1] - P[l] = k. So counting subarrays is the same as counting pairs of
boundaries (l, r+1) with l < r+1 and P[l] = P[r+1] - k. The loop handles each end
boundary r+1 once, at the step that reads a[r]. At the moment of the lookup, the
dictionary holds the values P[0], ..., P[r], each with its multiplicity, and
nothing else: P[0] from the seed, and P[1..r] from the inserts of earlier steps,
while P[r+1] has not been inserted yet. So the lookup returns exactly the number
of valid start boundaries for this end. Each pair is counted at its end boundary
and nowhere else, so each subarray is counted once.

**Claim 4.** A booking (l, r, v) should add v to every slot from l to r. It adds v
to D[l] and subtracts v from D[r+1]. The running total at slot i is D[1] + ... +
D[i]. That sum contains the +v if and only if l <= i, and contains the -v if and
only if r+1 <= i. So the booking contributes v when l <= i <= r, and v - v = 0 when
i > r, and nothing when i < l. Each booking contributes exactly its own range,
independent of every other booking, and the running total is the sum of all their
contributions. ∎
:::

In plain words: the milestones are right because each is the previous one plus one
step; a range is right because the whole road minus its first part is its second
part; the counter is right because each subarray is counted once at its right end,
using only milestones to its left; the difference array is right because a +v
and a -v cancel everywhere past the range.

The assumptions the proof used, and the bug each one produces when it fails:

- **Subtraction undoes the operation.** True for +, for XOR (each value is its own
  undo), and for addition mod m. False for min, max, gcd, and for multiplication
  when a zero is present. With no undo, claim 2 has no last step.
- **The array does not change after the build.** Claim 1 is about the array as it
  was during the loop.
- **P has n + 1 slots and D has room for r + 1.** Claim 2 reads P[r+1] with r up
  to n-1; claim 4 writes D[r+1] with r up to the last slot.
- **The dictionary holds only boundaries strictly to the left.** Claim 3, the
  moment of the lookup. Break it and you count empty subarrays.
- **The numbers are exact.** Claim 2 adds blocks in a different order from the
  honest loop. Integers do not care; floating-point numbers do, and long prefix
  totals of floats drift ([[numerical-stability]]).

## What it costs

**Build.** The loop body is one addition and one store, run n times: Θ(n) time,
n + 1 numbers of space.

**One question.** Two reads and a subtraction: Θ(1).

**q questions.** Θ(n + q), against up to Θ(n·q) for the honest loop. Per question,
the build adds n/q on average, so the average cost is 1 + n/q. For n = q = 2·10^5
that is 2 operations per question instead of up to 200,000. For q = 1 it is n + 1,
no better than the honest loop. Prefix sums pay off when there are many questions.

**Can you do better?** No, for static range sums. Any method must read every
element before answering: if it never reads a[i], then changing a[i] by 1 would
not change any of its answers, but the true answer to the question (i, i) would
change. So Ω(n) preparation is unavoidable, and Θ(n) build with Θ(1) per question
is optimal.

**Counting with a dictionary.** One pass, one lookup and one insert per element:
Θ(n) *expected* time, because a hash map is O(1) on average, not in the worst case
([[hash-tables]]). The dictionary holds at most n + 1 distinct milestones, so
Θ(n) space. This is where the hidden cost lives: a dictionary is many times
slower per operation than an array, so for n = 10^6 in Python the counting loop is
noticeably slower than the build, though still linear.

**Difference array.** Two writes per update, one pass at the end: Θ(n + k) for k
updates, against Θ(n·k) for the honest loop. [[p:amazon-maximum-user-traffic|Maximum User Traffic]]
has up to 10^5 users over up to 10^5 days: 10^10 for the loop, about 3·10^5 here.

**Two dimensions.** An r × c grid needs an (r+1) × (c+1) table, Θ(rc) to build and
Θ(1) per rectangle. The trap is memory, not time: a 10^4 × 10^4 grid is 10^8
numbers, which will not fit in the memory an OA gives you.

**The number that bites in other languages.** With n = 10^5 elements of size up to
10^9, a prefix total reaches 10^14. That is far past a 32-bit integer (about
2.1·10^9). Several problems in this bank say "use wide arithmetic for running
sums" for exactly this reason. Python's integers do not overflow
([[big-integers]]); Java's `int` and C++'s `int` do, silently.

## How to think about it

Ask these on every problem that might be this family, in order.

1. **Is the question about contiguous ranges?** "Subarray", "contiguous",
   "consecutive days", "from position l to r". If the word is "subsequence" or
   "subset", this is not the chapter.
2. **Reads or writes?** Many range reads on fixed data: prefix sums. Many range
   writes and one read at the end: difference array. Reads and writes mixed
   together: a [[fenwick-tree]] or [[segment-tree]], not this.
3. **What is the operation, and does it have an undo?** Sum, count of things
   (sum of 0/1 flags), XOR, sum mod m: yes. Min, max, gcd: no, so only "best to the
   left" and "best to the right" questions survive (the prefix-and-suffix
   variation), never arbitrary ranges.
4. **If the problem asks you to find subarrays: what relation between two
   milestones is the condition?** Write it as an equation in P[l] and P[r+1], then
   move everything about r to one side: "P[l] = P[r+1] - k", "P[l] mod m = P[r+1]
   mod m", "balance[l] = balance[r+1]". The left side is the dictionary key.
5. **What does the dictionary store per key?** A count, if you count subarrays. The
   first index where the key appeared, if you want the longest. The smallest value
   of some other prefix, if you want the best sum among valid subarrays.
6. **Seed the empty prefix, and look up before inserting.** `{0: 1}` for counts,
   `{0: -1}` for first indices. These two lines are where the bugs are.
7. **Sizes.** n + 1 slots for P; room for r + 1 in D; 64-bit totals.

### Telling it from its neighbours

- **Sliding window** wants non-negative values and one window at a time. Prefix
  sums want neither. If negatives are allowed and you need a count or a longest
  subarray with an exact sum, it is prefix sums plus a dictionary.
- **Kadane's algorithm** ([[kadane]]) is prefix sums in disguise: the best
  subarray ending at r is P[r+1] minus the smallest earlier milestone. Carry the
  minimum instead of a dictionary.
- **Fenwick tree** is prefix sums that tolerate updates, at a log factor per
  operation.
- **Sweep line** ([[sweep-line]]) is the difference array when the coordinates are
  large or not integers: sort the +v and -v events instead of indexing an array.

## Variations

Every variation below is the same milestone idea with one thing changed: the
operation, the key, what the dictionary stores, or the direction.

### A. Range sum in O(1) from a prefix array

The base case. Build once, answer each `[l, r]` with `P[r+1] - P[l]`.
[[p:intuit-static-range-sums|Range Sum Queries]] is it with no story.

A useful special case is the **split point**: the sum to the left of i is P[i] and
the sum to the right is `P[n] - P[i+1]`. [[p:expedia-equilibrium-index|Leftmost Equilibrium Index]]
wants the first i where those two are equal: `[1, 3, 5, 2, 2]` has total 13; at
i = 2 the left is 4 and the right is 13 - 9 = 4. You do not even need the array P:
carry the left sum in one variable and compute the right from the total.

Shapes made of row segments reduce to this too. In
[[p:hrt-maximum-rhombic-area-sum|Maximum Rhombic Area Sum]] a rhombus is a stack
of horizontal segments, and one prefix array per row turns each segment into a
subtraction.

### B. Prefix sum plus a hash map, to count subarrays with sum k

The derivation's Step 4: key `run - k`, store counts, seed `{0: 1}`, look up before
inserting. [[p:apple-subarray-sum-equals-k|Subarray Sum Equals K]] is the
canonical form, and its negative values are the reason a window fails.

**Change the operation to XOR.** [[p:inmobi-count-subarrays-with-given-xor|Count Subarrays With Given XOR]]:
XOR undoes itself, so the XOR of `a[l..r]` is `X[r+1] ^ X[l]`, and "equals k" is
"X[l] = X[r+1] ^ k". The loop is the same with `^` in place of both `+` and `-`
([[xor-tricks]]). Example: `[4, 2, 2, 6, 4]`, k = 6: four subarrays.

**Change "how many" to "the longest".** Store the *first* index at which each
milestone appeared, seed `{0: -1}`, and never overwrite an entry (the earliest start
gives the longest subarray). The answer at r is `r - first[run - k]`.

### C. Prefix of a parity, a mod or a balance

The relation between two milestones changes, and so the key changes.

**Mod.** A subarray sum is divisible by m exactly when the two milestones leave the
same remainder: `(P[r+1] - P[l]) % m == 0` is `P[r+1] % m == P[l] % m`. The key is
`run % m`. [[p:inmobi-count-subarrays-sum-divisible-by-k|Count Subarrays With Sum Divisible by K]]:
`[2, 3, 1]` with k = 2 has milestones 0, 2, 5, 6, remainders 0, 0, 1, 0. Remainder 0
appears three times, giving 3 pairs: `[2]`, `[3, 1]`, `[2, 3, 1]`. Python's `%` is
never negative for a positive m. In Java and C++, `-1 % 2` is -1, so write
`((run % m) + m) % m` or two equal remainders will look different.

**Balance.** "Equal numbers of X and Y" becomes: score X as +1 and Y as -1, and a
subarray is balanced when its score sums to 0, which is "the two milestones are
equal". [[p:amazon-get-max-skill-sum|Get Max Skill Sum]] adds a second prefix:
among balanced teams, maximise the skill sum. A balanced team from boundary l to
boundary r+1 has skill `S[r+1] - S[l]`, so for each balance value keep the
**smallest** skill milestone seen so far, and subtract it. Example: expertise
`[0, 0, 0, 1]`, skill `[10, 2, 3, 4]`: the only balanced teams are `[3, 4]`
(skill 7) and the empty team, so the answer is 7.

**Parity.** "An even number of vowels" or "every letter appears an even number of
times" is the same with a bitmask: flip bit c when letter c appears, and two equal
masks bound a subarray where every letter has even count. The XOR of the masks is
the parity of the counts.

**When the relation involves the length.** [[p:amazon-find-security-level|Find Security Level]]
(stretch, hard) flags a subarray when its sum mod k equals its length. Since a
remainder is below k, the length must be below k. Then
`(P[r+1] - P[l]) mod k = (r+1) - l` rearranges to
`(P[r+1] - (r+1)) mod k = (P[l] - l) mod k`: the key is `(P[i] - i) mod k`, and the
dictionary may only hold the last k - 1 boundaries, so you remove the oldest one as
you go. The insight is the algebra; the code is variation B with a moving window
over the dictionary.

### D. Difference array for range updates

The derivation's Step 5. `D[l] += v; D[r+1] -= v`, then one running total.
[[p:google-range-booking-totals|Range Booking Totals]] is it with 1-based slots.
[[p:amazon-maximum-user-traffic|Maximum User Traffic]] is it with v = 1 for every
user: each user covers a range of days, and after the running total you count how
many days reach the maximum.

**The difference array read as a cost.** "Fewest operations of the form *add 1 to
a range* to build a target array from zeros" is the sum of the positive steps
`max(0, t[i] - t[i-1])`: each rise in the target's difference array needs its own
operation to start there. `[3, 1, 4, 1, 5]` needs 3 + 3 + 4 = 10.

**Two dimensions (rare).** Adding v to a rectangle writes four corners: +v, -v,
-v, +v. Then a 2-D running total.

### E. Prefix and suffix arrays: everything except me, best to the left and right

When the operation has no undo, you can still answer "everything to my left" and
"everything to my right" by building one array from each end.

[[p:freshworks-product-of-array-except-self|Product of Array Except Self]]: the
product of everything except `a[i]` is (everything left of i) times (everything
right of i). Division would break on a zero, and the problem forbids it anyway. Two
passes, no division. `[1, 2, 3, 4]` gives left products `[1, 1, 2, 6]`, right
products `[24, 12, 4, 1]`, and the answer `[24, 12, 8, 6]`.

[[p:amazon-get-max-aggregate-temperature-change|Get Max Aggregate Temperature Change]]:
the value of day i is the larger of "sum of days up to i" and "sum of days from i
on". One prefix pass and the total give both in O(1) per day.

Prefix maximum and suffix minimum work the same way. "Can I split the array so that
everything on the left is at most everything on the right?" is "prefix max at i
<= suffix min at i+1".

### F. 2-D prefix sums

`P[i][j]` = the sum of the rectangle of rows 0..i-1 and columns 0..j-1, again with
an extra row and column of zeros for the boundaries. Build it with

`P[i+1][j+1] = a[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]`

(the cell, plus the rectangle above, plus the rectangle to the left, minus their
overlap, which was added twice). A rectangle with rows r0..r1 and columns c0..c1 is

`P[r1+1][c1+1] - P[r0][c1+1] - P[r1+1][c0] + P[r0][c0]`

subtract the strip above and the strip to the left, and add back the corner that
was subtracted twice. That is [[inclusion-exclusion]] with four terms.
[[p:rippling-matrix-block-sum|Matrix Block Sum]] asks, for every cell, the sum of
the square of radius r around it, clipped to the grid: one 2-D table and four
lookups per cell. [[p:imc-maximum-size-square-sub-matrix-with-sum-less-than-threshold|Maximum Size Square Sub-Matrix With Sum Less Than Threshold]]
(stretch) combines it with a search: with non-negative values, if a k × k square
fits under the threshold then so does a smaller one, so the side length can be
binary searched ([[binary-search]]), and each square is four lookups.

### G. Smaller variations worth knowing

- **Circular arrays.** The arc from i to j going forward is `P[j] - P[i]`; the
  other way round is the total minus that.
- **Prefix sums plus binary search.** When every value is non-negative, P never
  decreases, so "the first prefix that reaches X" is a binary search on P. Sorting
  first makes "the top k" a prefix.
- **Prefix counts of a predicate.** Replace each element by 1 if it passes a test
  and 0 otherwise; the prefix sum counts matches in any range
  ([[frequency-counting]]).
- **Running minimum of P.** The best subarray sum ending at r is P[r+1] minus the
  smallest earlier milestone. That is [[kadane]].

All of the counting and 2-D variations, run against brute force:

```python run
def count_div(a, m):                      # C: key is the remainder
    seen, run, total = {0: 1}, 0, 0
    for x in a:
        run += x
        total += seen.get(run % m, 0)
        seen[run % m] = seen.get(run % m, 0) + 1
    return total

def max_balanced_skill(expertise, skill):  # C: balance key, keep the min skill prefix
    best_start = {0: 0}                    # balance -> smallest skill milestone
    bal = run = best = 0
    for e, s in zip(expertise, skill):
        bal += 1 if e == 1 else -1
        run += s
        if bal in best_start:
            best = max(best, run - best_start[bal])
            best_start[bal] = min(best_start[bal], run)
        else:
            best_start[bal] = run
    return best

def except_self(a):                        # E: left products times right products
    n = len(a)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= a[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= a[i]
    return out

def block_sum(g, r):                       # F: 2-D milestones, four lookups
    R, C = len(g), len(g[0])
    P = [[0] * (C + 1) for _ in range(R + 1)]
    for i in range(R):
        for j in range(C):
            P[i + 1][j + 1] = g[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
    out = [[0] * C for _ in range(R)]
    for i in range(R):
        for j in range(C):
            r0, r1 = max(0, i - r), min(R - 1, i + r)
            c0, c1 = max(0, j - r), min(C - 1, j + r)
            out[i][j] = P[r1 + 1][c1 + 1] - P[r0][c1 + 1] - P[r1 + 1][c0] + P[r0][c0]
    return out

assert count_div([2, 3, 1], 2) == 3
assert max_balanced_skill([0, 0, 0, 1], [10, 2, 3, 4]) == 7
assert except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
assert block_sum(grid, 1) == [[12, 21, 16], [27, 45, 33], [24, 39, 28]]
print("divisible:", count_div([2, 3, 1], 2), " skill:", max_balanced_skill([0, 0, 0, 1], [10, 2, 3, 4]))
print("except self:", except_self([1, 2, 3, 4]), " block sum:", block_sum(grid, 1))

import random
random.seed(11)
for _ in range(300):
    n = random.randint(0, 8)
    a = [random.randint(-6, 6) for _ in range(n)]
    m = random.randint(1, 5)
    brute = sum(1 for l in range(n) for r in range(l, n) if sum(a[l:r + 1]) % m == 0)
    assert count_div(a, m) == brute
    ex = [random.randint(0, 1) for _ in range(n)]
    sk = [random.randint(0, 9) for _ in range(n)]
    bb = max([0] + [sum(sk[l:r + 1]) for l in range(n) for r in range(l, n)
                    if 2 * sum(ex[l:r + 1]) == r - l + 1])
    assert max_balanced_skill(ex, sk) == bb
print("mod and balance variants match brute force on 300 random cases")
```

## Recognising it in a statement

Ordered by how much you can trust the signal.

1. **"q queries, each [l, r], on an array that never changes"**, with n and q both
   large. n·q is dead and n + q is free. This is as close to a giveaway as the
   topic has.
2. **"Add v to every element from l to r", many times, then report the array or its
   maximum.** Difference array. If a question arrives between updates, it is a
   [[segment-tree]] instead.
3. **"Number of subarrays whose sum is k / is divisible by k / has XOR k", with
   negative values allowed.** Prefix plus dictionary. The negative values are the
   signal that a window will not work.
4. **"Equal number of X and Y in a contiguous block", "balanced", "as many 0s as
   1s".** Map to +1 and -1, then equal milestones.
5. **"Cumulative", "running balance", "balance after day i", "first index where the
   total drops to 0 or below".** The prefix sum is the answer itself.
6. **"Split into a left part and a right part such that ..."** Prefix from the left,
   total minus prefix for the right.
7. **"Except itself", "everything else", "best before i and best after i".** Prefix
   and suffix arrays.
8. **A brute force whose inner loop is a sum over a range.** Any repeated inner sum
   is a prefix sum waiting to be pulled out.
9. **The output is "long" or "use 64-bit" while n and the values are both large.**
   Someone is warning you that a long sum is involved.

### Disguised forms, with the algebra

- **"Remainder equals length"** (Find Security Level): move the length to the other
  side so that each side depends on one boundary only. The general move: rewrite
  the condition so that one side mentions only l and the other only r+1. What is
  left is the dictionary key.
- **"Average of the subarray is at least t"**: subtract t from every element; the
  condition becomes "sum is at least 0".
- **"Number of subarrays with exactly k odd numbers"**: replace each element by
  1 if odd and 0 if even; now it is "sum exactly k".
- **"Longest subarray with sum at most k" on non-negative data**: P never
  decreases, so it is a window or a binary search on P.

### Anti-signals: looks like prefix sums, is not

- **The aggregate is min, max or gcd over arbitrary ranges.** No undo. Sparse
  table or segment tree.
- **The array changes between questions.** The milestones go stale.
- **"Subsequence" or "subset"** instead of "subarray". Prefix sums need
  contiguity; a subset sum is [[knapsack]].
- **All values non-negative, one best window wanted.** A window is enough and
  shorter.

## Traps

**The +1.** `P[r] - P[l]` instead of `P[r+1] - P[l]`. Symptom: every answer is
short by exactly `a[r]`, and every single-element range returns 0.

**No P[0], or no seed `{0: 1}`.** Symptom: every answer is right except for ranges
or subarrays that start at index 0. Test l = 0 first, always.

**Insert before look up.** Symptom: correct for every k except 0, where the count is
too big by exactly n. Demonstrated above.

**A set instead of a counting dictionary.** Symptom: undercount whenever a milestone
repeats, which happens whenever the array contains a zero-sum stretch.

**D too short, or `D[r]` instead of `D[r+1]`.** Symptom: an index error on a range
that ends at the last slot, or every range losing its last slot.

**Negative remainders in Java or C++.** Symptom: correct on non-negative inputs,
undercounting with negatives, because -1 and 1 land in different buckets for m = 2.

**Overflow.** Symptom: correct on small inputs, negative sums on large ones.

**A sliding window over negative numbers.** Symptom: correct on the samples (which
are often all positive), wrong on the first hidden test with a negative. Here it is,
next to the right answer:

```python run
def window_count(a, k):                 # only valid when every a[i] >= 0
    l = s = total = 0
    for r, x in enumerate(a):
        s += x
        while s > k and l <= r:
            s -= a[l]
            l += 1
        if s == k:
            total += 1                  # counts one window per right end
    return total

def prefix_count(a, k):
    seen, run, total = {0: 1}, 0, 0
    for x in a:
        run += x
        total += seen.get(run - k, 0)
        seen[run] = seen.get(run, 0) + 1
    return total

def brute(a, k):
    n = len(a)
    return sum(1 for l in range(n) for r in range(l, n) if sum(a[l:r + 1]) == k)

a, k = [1, -1, 1], 1
print("a =", a, "k =", k)
print("window:", window_count(a, k), " prefix:", prefix_count(a, k), " truth:", brute(a, k))
assert window_count(a, k) == 2 and prefix_count(a, k) == brute(a, k) == 3

b = [1, 2, 3, 0, 3]                     # non-negative, but zeros break it too
print("b =", b, "k = 3  window:", window_count(b, 3), " prefix:", prefix_count(b, 3),
      " truth:", brute(b, 3))
assert prefix_count(b, 3) == brute(b, 3) == 5 and window_count(b, 3) == 4

c = [1, 2, 3, 4]                        # strictly positive: the window is fine
assert window_count(c, 5) == prefix_count(c, 5) == brute(c, 5)
print("strictly positive input: all three agree")
```

The second case is worth a look, because it has no negatives and the window still
fails. The subarrays of `[1, 2, 3, 0, 3]` that sum to 3 are `[1, 2]`, `[3]` at
index 2, `[3, 0]`, `[0, 3]` and `[3]` at index 4: five. The window finds four. At
the last step it shrinks until the sum is 3 and stops at `[0, 3]`, because that
already sums to 3; it never shrinks once more to `[3]`, which also sums to 3. With
a zero in the array, two different left ends give the same sum, and a window holds
only one left end per right end. So counting needs the dictionary even on
non-negative data. A window is safe for exact counts only when every value is
strictly positive.

## What to memorise

Two templates, one sentence, one habit.

```python
P = [0] * (n + 1)
for i in range(n):
    P[i + 1] = P[i] + a[i]           # sum of a[l..r] == P[r + 1] - P[l]

seen, run, total = {0: 1}, 0, 0      # count subarrays with sum k
for x in a:
    run += x
    total += seen.get(run - k, 0)    # look up first
    seen[run] = seen.get(run, 0) + 1 # then insert

D = [0] * (n + 1)                    # range add, read once
D[l] += v; D[r + 1] -= v             # then a running total over D[0..n-1]
```

**The sentence:** a range is the difference of two milestones, so a subarray
condition is a relation between two milestones; write the relation so one side
mentions only the left boundary, and that side is the dictionary key.

**The habit:** say P[i] out loud as "the sum of the first i elements", never "the
sum up to index i". The first phrasing makes P[r+1] - P[l] obvious and P[0] = 0
inevitable, and its dictionary form is writing `{0: 1}` before anything else.

Numbers to carry: 10^5 values of size 10^9 sum to 10^14, so 64-bit. n·q = 10^10 is
out of reach and n + q = 2·10^5 is nothing. A 10^4 × 10^4 2-D table is 10^8 cells
and will not fit.

## Check yourself

:::check
Trace by hand. `a = [4, -2, -2, 5, 1]`. Build P, then answer `a[1..3]`, `a[0..4]`
and `a[2..2]` with one subtraction each, naming the two boundaries you used.
--
P = [0, 4, 2, 0, 5, 6]. Each entry is the previous plus one element: 0, 0+4, 4-2,
2-2, 0+5, 5+1.

- `a[1..3]` starts at boundary 1, ends at boundary 4: P[4] - P[1] = 5 - 4 = 1.
  Check: -2 - 2 + 5 = 1.
- `a[0..4]`: P[5] - P[0] = 6 - 0 = 6, the whole array.
- `a[2..2]`: P[3] - P[2] = 0 - 2 = -2, which is a[2].

Notice P[3] = 0: the first three elements cancel. P is not monotone, so no binary
search on it.
:::

:::check
Trace by hand. `a = [1, 2, -3, 3, 0]`, k = 3. Run the counting loop with the
dictionary, writing `run`, the key you look up, what you find, the total, and the
dictionary after each step. Then list the subarrays you counted.
--
| step | x | run | look up | found | total | seen after |
|---|---|---|---|---|---|---|
| start | | 0 | | | 0 | {0: 1} |
| 0 | 1 | 1 | -2 | 0 | 0 | {0: 1, 1: 1} |
| 1 | 2 | 3 | 0 | 1 | 1 | {0: 1, 1: 1, 3: 1} |
| 2 | -3 | 0 | -3 | 0 | 1 | {0: 2, 1: 1, 3: 1} |
| 3 | 3 | 3 | 0 | 2 | 3 | {0: 2, 1: 1, 3: 2} |
| 4 | 0 | 3 | 0 | 2 | 5 | {0: 2, 1: 1, 3: 3} |

Total 5. Step 1 counts `[1, 2]` (from boundary 0). Step 3 counts `[1, 2, -3, 3]`
(boundary 0) and `[3]` (boundary 3). Step 4 counts `[1, 2, -3, 3, 0]` (boundary 0)
and `[3, 0]` (boundary 3). With "insert, then look up" the answer would be the
same, because k is not 0: the new milestone 3 is never equal to the key 3 - 3 = 0.
:::

:::check
Trace by hand. Six slots, indices 0 to 5, all starting at 0. Apply: add 2 to
`[0, 2]`, add 5 to `[2, 5]`, add -1 to `[1, 4]`. Write D (seven slots) after each
update, then the final array. Then say which slots come out wrong if you write
`D[r] -= v` instead of `D[r+1] -= v`.
--
| update | writes | D[0..6] |
|---|---|---|
| start | | [0, 0, 0, 0, 0, 0, 0] |
| +2 on [0, 2] | D[0] += 2, D[3] -= 2 | [2, 0, 0, -2, 0, 0, 0] |
| +5 on [2, 5] | D[2] += 5, D[6] -= 5 | [2, 0, 5, -2, 0, 0, -5] |
| -1 on [1, 4] | D[1] -= 1, D[5] += 1 | [2, -1, 5, -2, 0, 1, -5] |

Running total of D[0..5]: 2, 1, 6, 4, 4, 5. Check slot 2: covered by all three,
2 + 5 - 1 = 6.

With `D[r]`: the writes are D[0]+2, D[2]-2, D[2]+5, D[5]-5, D[1]-1, D[4]+1, giving
D = [2, -1, 3, 0, 1, -5, 0] and the array 2, 1, 4, 4, 5, 0. Slots 2, 4 and 5 are
wrong: they are the last slot of each update (2 for the first, 5 for the second,
4 for the third), and each one lost the update that ended there. It computed the
half-open ranges [l, r).
:::

:::check
Why must the counting loop look up `run - k` *before* inserting `run`? Answer in
terms of boundaries, and say exactly which inputs reveal the bug.
--
The lookup asks: how many start boundaries l, strictly to the left of the current
end boundary r+1, have P[l] = P[r+1] - k? The dictionary must therefore hold
P[0..r] and not P[r+1]. Inserting first adds P[r+1] itself, which allows l = r+1,
the empty subarray from a boundary to itself. Its sum is 0, so it matches only when
`run - k == run`, that is, when k = 0. Every k = 0 input is then overcounted by
exactly n, one empty subarray per step; every other k is unaffected, which is why
the bug survives casual testing.
:::

:::check
Someone says: "Prefix sums work for anything associative, so I will build a prefix
minimum array and answer range-minimum queries with it." Where are they wrong, and
what part of the claim is true?
--
The true part: the prefix minimum `M[i+1] = min(M[i], a[i])` is a correct array
and answers "the minimum of the first i elements", and with a suffix minimum it
answers split-point questions.

The wrong part is the range query. The proof's last step was "subtract P[l] from
both sides", which needs an undo, not just associativity. Min has no undo: the small
element may lie in the part you throw away. Concretely, `[1, 9, 9]` and `[1, 9, 1]`
have the same prefix minima (1, 1, 1) but the minimum of `a[1..2]` is 9 in one and 1
in the other. No arithmetic on the stored numbers can tell them apart. Range minima
need a [[sparse-table]] or a [[segment-tree]].
:::

:::check
Reduce this disguised problem. "Given a binary array, find the length of the longest
contiguous subarray with as many 0s as 1s." Then solve `[0, 1, 0, 0, 1, 1, 0]` by
hand.
--
Score 0 as -1 and 1 as +1. A subarray has equal counts exactly when its score sums
to 0, which is "two equal milestones". For the longest, store the first index where
each milestone appeared, seeded with milestone 0 at index -1 (boundary 0), and never
overwrite.

Scores: -1, +1, -1, -1, +1, +1, -1. Milestones after each element (index 0 to 6):
-1, 0, -1, -2, -1, 0, -1. First occurrences: 0 at -1, -1 at 0, -2 at 3.

- index 1: milestone 0, first at -1, length 2.
- index 5: milestone 0, first at -1, length 6.
- index 6: milestone -1, first at 0, length 6.

The answer is 6, for example `a[0..5] = [0, 1, 0, 0, 1, 1]`, three of each. Storing
counts instead of first indices would answer a different question: how many such
subarrays there are.
:::

:::check
A candidate says: "Sliding windows beat prefix sums: same time, O(1) space." Where
are they wrong?
--
They are right in one narrow case: one best window, on strictly positive (or, for
"at most k" questions, non-negative) values. There the window is linear time and
O(1) space, and better.

They are wrong in three ways. With **negatives**, extending a window can lower its
sum, so "shrink while too big" has nothing to work with; `[1, -1, 1]` with k = 1
shows the window reporting 2 instead of 3. With **zeros** and an exact count, several
left ends share a sum and a window holds only one of them. And with **many arbitrary
[l, r] questions**, a window answers one per pass, so q questions cost n·q, while the
prefix array answers each in one subtraction. They solve different problems that
overlap on positive single-window questions.
:::
