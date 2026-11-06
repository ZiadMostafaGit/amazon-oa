# Binary Search

> Binary search is not about sorted arrays: it is about a yes/no question whose answers flip from no to yes exactly once, so that every probe clears a whole side at once, and the only thing you ever look for is the place where it flips.

## The problem it solves

You are given a list of software versions in the order they were released. At
some point a bug crept in, and every version from then on is bad. The list is a
million long:

```
version:  0      1      2      3      4      5      6      7    ...  999999
bad?:     False  False  False  False  False  False  True   True ...  True
```

Find the first bad version. That is [[p:meta-first-bad-version-array|First Bad Version in a Monotone Array]],
and the first thing anyone writes is a scan from the left:

```
for i in range(n):
    if bad[i]:
        return i
return -1
```

It is correct. It is also slow in a way that matters. If the bug arrived late,
the scan looks at almost a million versions. In the original form of this
problem, "is version i bad?" is not an array lookup but a call to a test suite
that takes minutes. A million calls is a month.

The same shape shows up in plainer clothes. [[p:adobe-count-occurrences-in-sorted-array|Count Occurrences in a Sorted Array]]
gives a sorted array of up to 10^5 numbers and asks how many times x appears. A
scan answers it in 10^5 steps. Now ask it 10^5 times, once per query, as the
bigger OA problems do, and the scan costs 10^10 steps. Binary search answers each
query in 17.

What this chapter builds is a way to find the flip point in about log₂(n)
questions: 20 for a million, 30 for a billion. It is built from one idea, and it
fits in six lines. The danger is not the idea; it is the six lines, which are
famously easy to get almost right. So we will derive every one of them and give
each a meaning you can say out loud.

### When it is the wrong tool

- **One query on unsorted data.** Sorting costs n log n, a scan costs n. If you
  search once, scan. Sorting to binary search pays off only when you will ask many
  questions of the same data.
- **Exact membership with no order needed.** "Is x in the set?" is a
  [[hash-tables|hash set]] at O(1) per query. Binary search wins when you need
  order: the first value at least x, the count below x, the neighbour of x.
- **The question is not monotone.** In a sorted array, "is a[i] even?" goes
  yes, no, no, yes, no in no pattern. Sortedness does not help at all.
- **No random access.** On a linked list, reaching the middle costs n/2 steps,
  so a binary search costs as much as a scan.
- **The data keeps changing.** Inserting into a sorted Python list is O(n),
  because everything after the insert point shifts. With many inserts mixed
  with queries, use a balanced tree or an [[ordered-set]].

Over 500 problems in this bank use binary search somewhere. Most of them use it
as a step: a bisect inside a bigger loop, a lookup after a sort. Learning it well
once pays out everywhere.

## Build it from the brute force

### Step 1: the scan, and what it costs

The scan asks "is version i bad?" for i = 0, 1, 2, ... and stops at the first
yes. If the first bad version is at index b, it asks b + 1 questions. In the worst
case, b = n - 1 or nothing is bad, it asks all n.

Take a small case so we can count: ten versions, first bad at index 6.

```
index:  0  1  2  3  4  5  6  7  8  9
bad?:   F  F  F  F  F  F  T  T  T  T
```

The scan asks seven questions: indices 0 through 6.

### Step 2: notice the waste

Look at what the scan learns from asking about index 3. It hears "False". What
does it now know? That version 3 is good. That is all it uses.

But it could know much more. The problem promised that once a version is bad,
every later version is bad. Turn that around: if version 3 is good, then versions
0, 1 and 2 must be good too, because a bad one among them would have made 3 bad.
One answer of "False" at index 3 tells you the answer at four indices.

The same holds the other way. If you ask about index 8 and hear "True", then 9 is
bad too. And more importantly, the first bad version is at 8 or to its left. Every
index to the right of 8 is now irrelevant.

So each question, if the answers are monotone, does not tell you about one index.
It tells you about a whole side. The scan throws that away by always asking about
the index right next to the ones it already knows.

### The question that unlocks it

**What does one probe tell me about the positions I did not look at?**

When the answers have the shape no, no, ..., no, yes, ..., yes, the answer is: a
"no" at index i settles every index left of i, and a "yes" at index i settles
every index right of i. A probe is a cut. One side of the cut is decided, and the
first yes is on the other side.

Say it a second way. Before any probe, the first yes could be at any of the n
positions (or nowhere). After a probe at i, it is either in the part left of i or
in the part right of i, and you know which. The probe's value is how much it
shrinks the set of positions that are still possible.

### Step 3: where to probe

If each probe cuts the possible positions into two parts and keeps one, where
should you cut? You do not know in advance which part you will keep, because you
do not know the answer. So plan for the worse one.

Cut at a quarter of the way: if the answer is in the left quarter, great, but if
it is in the right three quarters, you have only removed 25%. Cut in the middle:
whichever side you keep, it is half. The middle is the only cut whose worse side
is as small as possible. That is the entire reason binary search probes the
middle, and it is why the name says "binary": each probe halves.

Halving from n down to one possible position takes about log₂(n) probes. For ten
versions, four. For a million, twenty.

### You might think: "Binary search finds a value in the array, so stop when you hit it."

This is the version most people learn first, and it answers a smaller question
than the one you usually have. Try it on [[p:grammarly-first-target-index|First Target Index]]:
the array is [1, 2, 2, 2, 4] and you want the first index holding 2.

The "stop on a hit" search probes the middle, index 2, sees a 2, and returns 2.
But the first 2 is at index 1. The search found a 2. It did not find the first
one, and it cannot, because it stopped looking the moment the middle matched.

The cure is to stop thinking of binary search as "find the target" and to think
of it as "find the boundary". Ask the monotone question "is a[i] >= 2?". Its
answers on [1, 2, 2, 2, 4] are no, yes, yes, yes, yes. The first yes is index 1:
exactly the first 2. A hit in the middle is just one more "yes". It moves the
search left; it does not end it.

### You might think: "The array must be sorted."

Sortedness is one way to get a monotone question. It is not the only one, and it
is not what binary search needs. Two small counterexamples.

[[p:blinkit-find-peak-element|Find a Peak Element]]: [1, 3, 7, 9, 4, 2] is not
sorted. But ask "is a[i] > a[i+1]?", which means "am I already going downhill?".
The answers for i = 0..4 are no, no, no, yes, yes. Monotone. The first yes is
index 3, the peak, value 9.

[[p:arista-networks-first-missing-number-in-consecutive-array|First Missing Number in a Consecutive Array]]:
[11, 12, 14, 15, 16] has no repeated value to find. But if nothing were missing,
a[i] would be a[0] + i. Ask "is a[i] > a[0] + i?", meaning "has a gap already
happened at or before i?". Answers: no, no, yes, yes, yes. The first yes is index
2, so the missing number is a[0] + 2 = 13. The array is sorted here, but the
question we search is not about the array's values at all. It is a fact we
derived.

And the other direction: a sorted array with a non-monotone question gives binary
search nothing. [2, 3, 4, 5] is sorted, and "is a[i] even?" answers yes, no, yes,
no.

The correct statement is: **the question must be monotone over the range you
search.** Sorted data is the most common reason it is.

### You might think: "lo and hi are just the ends of the range; fix the +1 and -1 until the tests pass."

This instinct produces the most binary search bugs. Here is the classic one. You
want the last index whose value is at most 3 in [2, 3, 5, 5, 5, 8, 13] (the answer
is index 1). You write:

```
lo, hi = 0, 6
while lo < hi:
    mid = (lo + hi) // 2
    if a[mid] <= 3: lo = mid        # mid could be the answer, keep it
    else:           hi = mid - 1
```

Step 1: mid = 3, a[3] = 5, too big, hi = 2. Step 2: mid = 1, a[1] = 3, fine, lo =
1. Step 3: lo = 1, hi = 2, mid = (1 + 2) // 2 = 1, fine, lo = 1. Nothing changed.
Step 4 is step 3 again, forever.

The fix is not a lucky +1 somewhere. The fix is to give lo and hi meanings that
the loop can never break, and to let those meanings decide every line. That is
the next step.

### Step 4: give the two pointers meanings

Name the question pred(i): "is the answer at i yes?". Keep two indices, lo and
hi, and promise two facts at every moment:

- **pred(lo) is no.** lo is a position I have proven is before the boundary.
- **pred(hi) is yes.** hi is a position I have proven is at or after the
  boundary.

Since every no comes before every yes, the boundary, the first yes, is somewhere
in lo+1 .. hi. When hi = lo + 1 there is only one candidate left: hi itself. It
is a yes with a no immediately to its left. It is the first yes.

How do we start, before any probe? We need a known no and a known yes. Use
imaginary positions just outside the array: lo = -1 and hi = n. Pretend pred(-1)
is no and pred(n) is yes. We will never actually ask about them, because we only
ever probe strictly between lo and hi. They are claims, not array reads.
Returning hi = n at the end then has an honest meaning: "no real index said yes".

### Step 5: one probe, and which pointer moves

Probe the middle, mid, strictly between lo and hi.

- pred(mid) is yes. Then mid is a known yes, and it is at least as far left as
  hi. Move hi to mid. Both facts still hold.
- pred(mid) is no. Then mid is a known no, at least as far right as lo. Move lo
  to mid. Both facts still hold.

There is no third case and no "+1". The pointer that moves is the one whose fact
mid just proved. When the loop ends, hi is the first yes and lo is the last no.
Both are answers to useful questions, and you get both for free.

### Step 6: the loop

```
lo, hi = -1, n
while hi - lo > 1:              # some index strictly between them is undecided
    mid = lo + (hi - lo) // 2   # strictly between lo and hi
    if pred(mid):
        hi = mid                # mid is a known yes
    else:
        lo = mid                # mid is a known no
return hi                       # first yes (n means none); lo is the last no
```

Every line of it came from a step above. The condition says "stop when nothing is
left between the two facts". The midpoint is the cut with the smallest worse side.
The branches move whichever pointer mid just earned.

### The technique in one sentence

**Binary search: keep a known "no" and a known "yes" of a monotone question,
probe strictly between them, and move whichever one the probe proves, until they
are adjacent; the yes is the first yes.**

And the question to ask on every new problem: **what does one probe tell me
about the positions I did not look at?** If the answer is "a whole side", you
can halve.

## Worked by hand

Get a pen. The array has seven values and duplicates on purpose:

```
index:  0  1  2  3  4  5  6
a:      2  3  5  5  5  8  13
```

We want the first index with a[i] >= 5. That is called the **lower bound** of 5.
Before searching, write the answers out so you know what the search should find:

```
a[i] >= 5 ?   no no yes yes yes yes yes      first yes: index 2
a[i] >  5 ?   no no no  no  no  yes yes      first yes: index 5
```

The second row is the **upper bound** of 5: the first value strictly greater. The
two rows differ in exactly the three positions that hold 5, and the boundaries
are 2 and 5. Keep that picture: the lower bound is where the run of 5s starts,
the upper bound is just past where it ends.

<svg viewBox="0 0 640 210" role="img" aria-label="the array 2 3 5 5 5 8 13 with two rows of answers: for a[i] >= 5 the yes cells start at index 2, for a[i] > 5 they start at index 5; the cells holding 5 are shaded, and the gap between the two boundaries is the count of 5s">
  <g>
    <text x="20" y="22">index</text>
    <text x="125" y="22" text-anchor="middle">0</text>
    <text x="195" y="22" text-anchor="middle">1</text>
    <text x="265" y="22" text-anchor="middle">2</text>
    <text x="335" y="22" text-anchor="middle">3</text>
    <text x="405" y="22" text-anchor="middle">4</text>
    <text x="475" y="22" text-anchor="middle">5</text>
    <text x="545" y="22" text-anchor="middle">6</text>
    <text x="20" y="57">a[i]</text>
    <rect x="90" y="35" width="70" height="34" rx="4"/>
    <rect x="160" y="35" width="70" height="34" rx="4"/>
    <rect class="fill" x="230" y="35" width="70" height="34" rx="4"/>
    <rect class="fill" x="300" y="35" width="70" height="34" rx="4"/>
    <rect class="fill" x="370" y="35" width="70" height="34" rx="4"/>
    <rect x="440" y="35" width="70" height="34" rx="4"/>
    <rect x="510" y="35" width="70" height="34" rx="4"/>
    <text x="125" y="57" text-anchor="middle">2</text>
    <text x="195" y="57" text-anchor="middle">3</text>
    <text x="265" y="57" text-anchor="middle">5</text>
    <text x="335" y="57" text-anchor="middle">5</text>
    <text x="405" y="57" text-anchor="middle">5</text>
    <text x="475" y="57" text-anchor="middle">8</text>
    <text x="545" y="57" text-anchor="middle">13</text>
    <text x="20" y="102">&gt;= 5</text>
    <text x="125" y="102" text-anchor="middle">no</text>
    <text x="195" y="102" text-anchor="middle">no</text>
    <text x="265" y="102" text-anchor="middle">yes</text>
    <text x="335" y="102" text-anchor="middle">yes</text>
    <text x="405" y="102" text-anchor="middle">yes</text>
    <text x="475" y="102" text-anchor="middle">yes</text>
    <text x="545" y="102" text-anchor="middle">yes</text>
    <line x1="230" y1="80" x2="230" y2="112"/>
    <text x="20" y="142">&gt; 5</text>
    <text x="125" y="142" text-anchor="middle">no</text>
    <text x="195" y="142" text-anchor="middle">no</text>
    <text x="265" y="142" text-anchor="middle">no</text>
    <text x="335" y="142" text-anchor="middle">no</text>
    <text x="405" y="142" text-anchor="middle">no</text>
    <text x="475" y="142" text-anchor="middle">yes</text>
    <text x="545" y="142" text-anchor="middle">yes</text>
    <line x1="440" y1="120" x2="440" y2="152"/>
    <text x="230" y="178" text-anchor="middle">lower bound = 2</text>
    <text x="440" y="178" text-anchor="middle">upper bound = 5</text>
    <text x="320" y="202" text-anchor="middle">the shaded run of 5s is exactly the cells between the two boundaries: 5 - 2 = 3 copies</text>
  </g>
</svg>

### Trace 1: lower bound of 5

Start with lo = -1 (an imaginary no) and hi = 7 (an imaginary yes). The midpoint
is lo + (hi - lo) // 2.

| step | lo | hi | mid | a[mid] | a[mid] >= 5? | move | why |
|---|---|---|---|---|---|---|---|
| 1 | -1 | 7 | 3 | 5 | yes | hi = 3 | index 3 is a yes, so the first yes is at 3 or left of it |
| 2 | -1 | 3 | 1 | 3 | no | lo = 1 | index 1 is a no, so 0 and 1 are both no |
| 3 | 1 | 3 | 2 | 5 | yes | hi = 2 | index 2 is a yes |
| end | 1 | 2 | | | | stop | hi - lo = 1: nothing is left between them |

Answer: hi = 2.

Tell the story of step 1 in words. "The window holds indices 0 to 6, seven
candidates. I probe the middle one, index 3. It holds 5, and 5 >= 5, so index 3
says yes. I do not stop, even though I found a 5: there might be a 5 further
left. What I have learned is that the first yes is at 3 or before it, so indices
4, 5, 6 are out. hi moves to 3. Three candidates are left: 0, 1, 2."

And step 2: "lo is -1, hi is 3. The middle is -1 + 4 // 2 = 1. a[1] = 3, and 3 is
not >= 5, so index 1 is a no. Since every no comes before every yes, index 0 is a
no too. lo moves to 1. Only index 2 is undecided."

Step 3 decides index 2. Now lo = 1 is a proven no and hi = 2 is a proven yes, and
they are neighbours. There is no index between them left to doubt. That is the
moment the answer is known, and it is exactly what the loop condition
hi - lo > 1 tests.

Three probes for seven values. The scan would have used three as well here
(indices 0, 1, 2), but the scan's count grows with the answer and the search's
does not: for the lower bound of 99, the scan reads all seven values and the
search still reads three.

### Trace 2: upper bound of 5, and a value that is not there

Same array, same loop, one character changed in the question: a[mid] > 5.

| step | lo | hi | mid | a[mid] | a[mid] > 5? | move |
|---|---|---|---|---|---|---|
| 1 | -1 | 7 | 3 | 5 | no | lo = 3 |
| 2 | 3 | 7 | 5 | 8 | yes | hi = 5 |
| 3 | 3 | 5 | 4 | 5 | no | lo = 4 |
| end | 4 | 5 | | | | stop |

Answer: hi = 5. Look at step 1 and compare it with trace 1. The same probe, index
3, the same value, 5. In trace 1 it said yes and the search went left. Here it says
no and the search goes right. That single comparison decides whether a tie sends
you to the start of the run or past its end. This is the line to be careful with,
and we will come back to it.

So the number of 5s is upper bound minus lower bound: 5 - 2 = 3. That is the
whole of [[p:swiggy-first-and-last-occurrence|First and Last Occurrence]]: the
first 5 is at the lower bound, 2, and the last is one before the upper bound, 4.

Now a value that is absent. The lower bound of 4:

| step | lo | hi | mid | a[mid] | a[mid] >= 4? | move |
|---|---|---|---|---|---|---|
| 1 | -1 | 7 | 3 | 5 | yes | hi = 3 |
| 2 | -1 | 3 | 1 | 3 | no | lo = 1 |
| 3 | 1 | 3 | 2 | 5 | yes | hi = 2 |
| end | 1 | 2 | | | | stop |

Answer 2, the same as for 5. Of course: 4 is not in the array, so "at least 4"
and "at least 5" pick out the same cells. Index 2 is where 4 would go if you
inserted it and kept the array sorted. That is why the lower bound is also called
the **insertion point**, and why "does 4 exist?" is answered by one extra check:
is a[2] equal to 4? It is not.

And the lower bound of 99: every probe says no, lo climbs (3, then 5, then 6), and
the loop ends with lo = 6, hi = 7. The answer is 7, which is not an index. It is
the imaginary yes we started with, and it means "nothing in the array is >= 99".
No special case was written for it. It fell out of the meanings.

What do the traces show that the code alone would not? Three things. The search
never stops on a hit: in trace 1 it found a 5 at step 1 and kept going, and that
is what made it find the first 5. The imaginary positions -1 and 7 were never read:
mid was always strictly between lo and hi. And the absent value needed no special
case: its answer is the insertion point, and "past the end" is n.

## From the idea to the code

### The direct version, next to the scan

The program below writes the loop from Step 6 as a function first_true, builds
the lower and upper bound on it, and checks everything against the scan and
against Python's own bisect module. It also counts probes, so you can see the
log₂ growth instead of taking it on trust.

```python run
from bisect import bisect_left, bisect_right
import random

def first_true(lo, hi, pred):
    """Smallest x in (lo, hi] with pred(x) true. Caller promises pred(lo)
    is false and pred(hi) is true (either may be an imaginary sentinel)."""
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid
    return hi

def lower_bound(a, x):            # first index with a[i] >= x, or len(a)
    return first_true(-1, len(a), lambda i: a[i] >= x)

def upper_bound(a, x):            # first index with a[i] > x, or len(a)
    return first_true(-1, len(a), lambda i: a[i] > x)

def scan_first(n, pred):          # the brute force
    for i in range(n):
        if pred(i):
            return i
    return n

a = [2, 3, 5, 5, 5, 8, 13]
print("lower_bound(5) =", lower_bound(a, 5), " upper_bound(5) =", upper_bound(a, 5))
print("count of 5s    =", upper_bound(a, 5) - lower_bound(a, 5))
print("lower_bound(4) =", lower_bound(a, 4), " lower_bound(99) =", lower_bound(a, 99))
assert (lower_bound(a, 5), upper_bound(a, 5), lower_bound(a, 4), lower_bound(a, 99)) == (2, 5, 2, 7)

for x in range(0, 16):            # agree with the standard library everywhere
    assert lower_bound(a, x) == bisect_left(a, x) == scan_first(7, lambda i: a[i] >= x)
    assert upper_bound(a, x) == bisect_right(a, x)
assert lower_bound([], 5) == 0    # empty array: no special case needed

for n in (10, 1000, 10**6):       # count the probes in the worst case
    probes = 0
    def bad(i):
        global probes
        probes += 1
        return i >= n - 1         # the first bad version is the very last one
    assert first_true(-1, n, bad) == n - 1
    print("n = %-8d first bad = %-7d probes: binary %2d, scan %d" % (n, n - 1, probes, n))
    assert probes <= n.bit_length() + 1

random.seed(7)
for _ in range(300):              # random sorted arrays with many duplicates
    arr = sorted(random.randint(0, 9) for _ in range(random.randint(0, 12)))
    x = random.randint(-1, 10)
    assert lower_bound(arr, x) == bisect_left(arr, x)
    assert upper_bound(arr, x) == bisect_right(arr, x)
print("agrees with bisect and the scan on 300 random arrays")
```

A million versions, twenty probes. The scan would make a million. That ratio is
the reason the chapter exists.

### Each line, and which part of the idea it is

| line | in plain words | from which step |
|---|---|---|
| `first_true(lo, hi, pred)` with lo = -1, hi = n | a known no and a known yes, both imaginary | Step 4, the meanings |
| `while hi - lo > 1` | some index strictly between them is still undecided | Step 4: adjacent means done |
| `mid = lo + (hi - lo) // 2` | cut in the middle, strictly inside | Step 3, where to probe |
| `if pred(mid): hi = mid` | mid proved to be a yes; it is the new known yes | Step 5 |
| `else: lo = mid` | mid proved to be a no; it is the new known no | Step 5 |
| `return hi` | the first yes; n means "none" | Step 4 |

Settle the small confusions now, before they cost you an interview.

**Why lo = -1 and not 0?** Because lo must be a known no, and index 0 might be a
yes (for example, the lower bound of 1 in [2, 3, 5] is index 0). -1 is a position
that is a no by definition. It is never read, so it cannot crash.

**Why hi = n and not n - 1?** Because hi must be a known yes, and the last index
might be a no (the lower bound of 99). n is a yes by definition, it is never
read, and returning it means "none".

**Why is mid never -1 or n?** For hi - lo >= 2, (hi - lo) // 2 is at least 1 and
at most hi - lo - 1, so lo < mid < hi. Inside the loop, mid is always a real index
from 0 to n - 1. That is also why the pointers can never get stuck: each step
moves one of them by at least 1 toward the other.

**What about `(lo + hi) // 2`?** In Python they are the same, because integers do
not overflow. In Java, C++ or Rust, lo + hi can exceed the largest int when the
indices are large, wrap to a negative number, and send mid off the array. That
bug sat in the JDK's own binary search for years. Write `lo + (hi - lo) // 2`
everywhere, so your fingers do it when it matters. See [[big-integers]].

**Where is "equal"?** There is no equality branch. Equality is inside pred: `>=`
puts equal values on the yes side, `>` puts them on the no side. That is the whole
difference between the lower and the upper bound. To answer "is x present?", take
the lower bound i and check `i < n and a[i] == x`, which is one place for a bug
instead of a second loop.

**What does Python give me?** `bisect_left(a, x)` is the lower bound and
`bisect_right(a, x)` is the upper bound, written in C. Use them when the question
is about a sorted list's values. Write the loop yourself when the question is
something else (a derived predicate, a rotation, a peak), or when the
interviewer asks you to.

### The four counting questions, each one bisect

Everything "how many" on a sorted array is a difference of two bounds, and it is
worth having the table in your head:

| question | answer | example on [2, 3, 5, 5, 5, 8, 13] |
|---|---|---|
| how many < x | bisect_left(a, x) | x = 5: 2 |
| how many <= x | bisect_right(a, x) | x = 5: 5 |
| how many > x | n - bisect_right(a, x) | x = 5: 2 |
| how many in [L, R] | bisect_right(a, R) - bisect_left(a, L) | [3, 8]: 6 - 1 = 5 |
| the predecessor (last value <= x) | index bisect_right(a, x) - 1, if >= 0 | x = 7: index 4, value 5 |
| the ceiling (first value >= x) | index bisect_left(a, x), if < n | x = 6: index 5, value 8 |

The reason "how many < x" is bisect_left: the lower bound is the first index
whose value is at least x, so every index before it holds a value less than x,
and there are exactly that many indices before it. Read it again with "<= x" and
bisect_right and it is the same sentence.

[[p:atlassian-time-based-key-value-store|Time Based Key-Value Store]] is the
predecessor row: each get asks for the latest timestamp not after t, which is
index bisect_right(ts, t) - 1. [[p:peoplestrong-ceiling-in-sorted-array|Ceiling Value in a Sorted Array]]
is the ceiling row.

### The subtle line, both ways

There is one line in binary search that bites, and it is not the midpoint. It is
the pair "what does pred say about mid, and what does each branch assign". Get it
right by meaning and the loop is correct. Get it right by trial and it works on
your three tests and spins on the fourth.

Go back to the bug from Build it. The question is the last index with a[i] <= 3 in
[2, 3, 5, 5, 5, 8, 13]; the answer is 1. The wrong version keeps both ends inside
the window, uses `lo = mid` for "mid might be the answer", and rounds the midpoint
down. The right version asks the half-open template for the first index where
a[i] > 3 and reads off lo, the last no. The program prints the state after every
step of both, with the wrong one capped at eight steps so it cannot run forever.

```python run
a = [2, 3, 5, 5, 5, 8, 13]
t = 3                                   # want the LAST index with a[i] <= 3: index 1

def wrong_last_le(a, t, cap=8):
    lo, hi, steps = 0, len(a) - 1, []
    while lo < hi and len(steps) < cap:
        mid = (lo + hi) // 2            # rounds DOWN, so mid can equal lo
        if a[mid] <= t:
            lo = mid                    # 'mid might be it, keep it'
        else:
            hi = mid - 1
        steps.append((mid, lo, hi))
    return lo, steps, lo < hi           # still running?

def right_last_le(a, t):
    lo, hi, steps = -1, len(a), []      # lo: known 'a[i] <= t', hi: known 'a[i] > t'
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2       # strictly between lo and hi
        if a[mid] > t:
            hi = mid
        else:
            lo = mid
        steps.append((mid, lo, hi))
    return lo, steps                    # lo is the last 'no' of 'a[i] > t'

ans, steps, stuck = wrong_last_le(a, t)
print("wrong:  (mid, lo, hi) after each step")
for s in steps:
    print("       ", s, "*" if s[0] == s[1] else "")
print("        stuck after %d steps: %s" % (len(steps), stuck))
assert stuck and steps[-1] == steps[-2] == (1, 1, 2)

ans, steps = right_last_le(a, t)
print("right:  (mid, lo, hi) after each step")
for s in steps:
    print("       ", s)
print("        answer lo =", ans)
assert ans == 1 and len(steps) == 3

for t in range(0, 15):                  # the right one is right everywhere
    expect = max([i for i in range(len(a)) if a[i] <= t], default=-1)
    assert right_last_le(a, t)[0] == expect
print("right version matches a scan for t = 0..14 (including -1 for 'none')")
```

Point at the exact step where the wrong one dies: the first `*` row, (1, 1, 2). The
window is lo = 1, hi = 2, two candidates. The midpoint rounds down to 1, which is
lo itself. a[1] = 3 is <= 3, so it assigns lo = 1, which is where lo already was.
Nothing moved, so the next step is the same step. The loop's only promise was that
the window shrinks, and when mid equals lo and the branch assigns lo = mid, it
does not.

The right one cannot do this. Its mid is always strictly between lo and hi, so
each assignment moves a pointer by at least one. And it never had to think about
"is mid still a candidate, keep it or skip it?", because lo and hi are not
candidates. They are proven facts. The candidates are strictly between them.

What does the wrong version accidentally compute? Nothing, it never returns. A
"fixed" version that rounds up instead (mid = (lo + hi + 1) // 2) is correct, and
you will see it in other people's code. It works for the same reason the half-open
one does: it makes mid differ from the pointer that the branch might assign. If you
use the closed style, that is the rule: **round the midpoint toward the pointer
that the yes branch does not assign.** If you use the half-open style, you never
need the rule.

The second half of the subtle line is the comparison inside pred. Trace 1 and
Trace 2 are that demonstration: `>=` and `>` take the same probe at index 3, see
the same 5, and send the search in opposite directions. Neither is wrong. They
answer different questions, and the only way to choose is to write the question in
words first: "the first index whose value is at least x" is `>=`; "the first index
whose value is more than x" is `>`.

### Recursion, if you prefer it

The loop is a tail recursion, and it can be written as one:

```
def first_true_rec(lo, hi, pred):
    if hi - lo <= 1:
        return hi
    mid = lo + (hi - lo) // 2
    return first_true_rec(lo, mid, pred) if pred(mid) else first_true_rec(mid, hi, pred)
```

The depth is log₂ n, about 30 at most, so the stack is not a concern. The concern
is the one people add without thinking: passing `a[mid:]` or `a[:mid]` instead of
indices. A slice copies, so each level costs O(n) and the "binary search" costs
O(n) overall. Pass indices, never slices.

## Why it is correct

The informal reason, "we halve until one is left", explains the speed. It does not
explain why the one that is left is the right one. The proof does.

:::proof first_true returns the first yes
**What we are given.** pred is a yes/no question on the integers lo₀ .. hi₀ that is
**monotone**: once it says yes at some x, it says yes at every larger x. The caller
guarantees that pred(lo₀) is no and pred(hi₀) is yes (either may be an imaginary
position that is no or yes by definition and is never evaluated).

**The invariant.** At the top of every pass through the loop, three things hold:
pred(lo) is no, pred(hi) is yes, and lo < hi.

**It holds at the start.** Before the first pass, lo = lo₀ and hi = hi₀, so the
first two facts are the caller's guarantee. And lo₀ < hi₀, because a no can only sit
to the left of a yes when the question is monotone.

**One pass keeps it.** Suppose the invariant holds and the loop runs, so
hi - lo >= 2. Let d = hi - lo. The midpoint is mid = lo + d // 2. Since d >= 2, d // 2
is at least 1, so mid >= lo + 1. And d // 2 <= d - 1 for every d >= 2, so mid <= hi - 1.
So lo < mid < hi: mid is a real position strictly inside. Now two cases.

- pred(mid) is yes. The code sets hi = mid. The new hi is a yes because we just
  asked. lo did not move, so it is still a no. And lo < mid, so lo < hi.
- pred(mid) is no. The code sets lo = mid. The new lo is a no because we just
  asked. hi did not move, so it is still a yes. And mid < hi, so lo < hi.

Either way, all three facts hold again.

**It stops.** The width hi - lo is a whole number. After a pass it is either d // 2
or d - d // 2, and for d >= 2 both are at least 1 and at most d - 1. So every pass
makes the width strictly smaller while keeping it at least 1. A whole number cannot
shrink forever, so the loop ends, and it ends exactly when the width is 1.

**Why the answer is right.** At the end, pred(lo) is no, pred(hi) is yes, and
hi = lo + 1. Every position left of hi is at most lo, and since pred(lo) is no and
the question is monotone, every one of them is a no. So hi is a yes with only noes
to its left: it is the first yes. In the same way, lo is the last no. ∎
:::

Now read the proof again and list what it used. That list is where the bugs come
from.

1. **Monotonicity.** Used twice: to say a no sits left of a yes at the start, and
   to say every position left of a no is a no at the end. If the question is not
   monotone over the whole range (a rotated array asked "a[i] >= x?"), the loop
   still runs, still takes log n steps, and returns a position that is a yes next
   to a no, which is not the first yes.
2. **mid strictly between lo and hi.** Used for termination. The closed-window
   bug above is exactly this assumption failing: mid = lo, the branch assigns
   lo = mid, the width does not change.
3. **The sentinels are honest.** If you start with lo = 0 and index 0 is actually a
   yes, the invariant is false from the first moment, and the answer can never be
   0. Start lo where you can prove a no, which usually means -1.
4. **pred is deterministic and cheap enough.** Asked twice about the same
   position, it must say the same thing. A predicate that depends on mutable
   state that changes during the search breaks every step of the argument.

Most binary search bugs are not off-by-ones. They are one of these four quietly
failing, and the off-by-one is just the symptom.

## What it costs

Count the passes. The window starts with width w = hi₀ - lo₀, which is n + 1 for the
sentinels -1 and n. Each pass replaces the width d by at most ⌈d/2⌉. After k passes
the width is at most ⌈w / 2^k⌉, and the loop stops at width 1. So the number of
passes is the smallest k with 2^k >= w, which is ⌈log₂(n + 1)⌉.

| n | passes | check against the traces |
|---|---|---|
| 7 | ⌈log₂ 8⌉ = 3 | three probes in every trace above |
| 10 | ⌈log₂ 11⌉ = 4 | four probes for ten versions |
| 10^5 | 17 | |
| 10^6 | 20 | twenty probes, as the program printed |
| 10^9 | 30 | |

Each pass does O(1) work plus one call to pred. So the cost is **Θ(log n) calls to
pred**, and O(1) extra space. As a recurrence: T(w) = T(w/2) + O(1), which unrolls
to log₂ w terms of O(1).

**The cost people forget is pred.** If pred is an array lookup, a search is
Θ(log n). If pred is a whole simulation that costs C, it is Θ(C log n). In the
original First Bad Version, C is a test run, and the point of binary search is that
log n test runs is affordable where n is not. In [[binary-search-on-answer]] the
predicate is a greedy pass over the input, and the total is O(n log range).

**The cost of getting sorted.** Binary search needs the monotone shape to exist
already. If you must sort first, that is O(n log n) once. Against q queries, the
scan costs q · n and sort-then-search costs n log n + q log n. For n = 10^6, sorting
is about 2 · 10^7 steps and one scan is 10^6, so sorting pays after about twenty
queries. [[p:amazon-find-sum-of-beauties|Find Sum of Beauties]] is the typical
shape: build a list, sort it once, then answer many "how many are smaller than x"
questions with bisect_left.

**The cost of inserting.** `bisect.insort` finds the spot in O(log n) and then
shifts the tail of the list in O(n). A loop of n inserts is O(n²). Python's list
shift is a fast memmove, so this is fine up to about 10^5 inserts and painful past
that. For many inserts with many queries, use a balanced structure.

**A floor you cannot beat.** Any method that learns only by comparing the target
with array entries gets one bit per comparison. A search over n sorted values must
tell apart n + 1 outcomes (before the first value, between any two, after the last).
k bits tell apart at most 2^k outcomes, so k >= log₂(n + 1). Binary search meets this
exactly, so in the comparison model there is nothing faster to look for. Hash
tables beat it only by not comparing at all.

## How to think about it

### The checklist

Ask these on every problem that might be a binary search, in this order.

1. **What is the yes/no question?** Write it in words before any code: "is
   version i bad", "is a[i] at least x", "has a gap happened by index i", "am I
   past the peak". If you cannot write it, you are not ready to search.
2. **Is it monotone over the whole range, and in which direction?** Argue it in
   one sentence: "a[i] >= x is monotone because a is sorted". If it goes yes then
   no, flip it ("a[i] < x") or search for the last yes instead.
3. **Do I want the first yes or the last no?** They come out of the same loop: hi
   and lo. "Last value at most x" is the last no of "a[i] > x".
4. **What are the sentinels, and what does returning one mean?** -1 and n by
   default. What does the problem want when hi = n comes back: -1, the length, an
   empty string? Decide now.
5. **What is a probe worth?** O(1) for an array lookup; a full pass for a
   feasibility check. Multiply by log of the range.
6. **What is the search space?** An array's indices (this chapter), a range of
   candidate answers that exists only as numbers ([[binary-search-on-answer]]),
   or two dimensions (the matrix variations below).
7. **What happens with duplicates and with no answer at all?** Run the plan in
   your head on [x, x, x] and on [].

Questions 1 and 2 are where the thinking is. Everything after them is
transcription.

### Telling it from its neighbours

- **[[two-pointers]].** "Two numbers in a sorted array that sum to T" can be a
  binary search for T - a[i] for every i, O(n log n), or two pointers from both
  ends, O(n). When both ends of a pair move monotonically, two pointers wins.
- **[[hash-tables]].** Exact lookups with no order: hash. Anything with "first",
  "at least", "closest", "how many below": binary search.
- **[[ternary-search]].** For a function that rises then falls, ternary search
  finds the top. On integers you do not need it: "is f(i) > f(i+1)?" is monotone,
  and a binary search finds the first i where it holds. That is the peak problem.
- **[[binary-search-on-answer]].** Same loop, different space: the positions are
  candidate answers (a speed, a capacity, a distance), not array indices, and pred
  is a feasibility check.
- **[[bst]] and [[ordered-set]].** A binary search tree is a binary search that
  has been frozen into pointers so that inserts stay cheap. If the data changes
  between queries, that is what you want.
- **[[search-rotated]].** A rotated array is not monotone under "a[i] >= x", but it
  is under a different question. That chapter goes deeper; the variations below
  cover what interviews ask.

## Variations

Every variation is the same loop. What changes is the question you put in pred and
the range you put in lo and hi. For each one: what changes, why, a tiny example,
and a bank problem to practise on.

### A. The bare boundary: first true, last false

**What changes:** nothing. pred is given to you, or is one comparison.
**Why it works:** the problem promises monotonicity.
**Example:** [False, False, True, True] gives 2. [True, True] gives 0 (hi moves to
mid every time; lo stays at the sentinel -1). [False, False] gives 2 = n, which
the problem wants as -1.

Practise on [[p:meta-first-bad-version-array|First Bad Version in a Monotone Array]],
then [[p:grammarly-first-target-index|First Target Index]] (lower bound, then one
equality check to turn "insertion point" into "found or -1").

### B. A derived question: monotone without being the data

**What changes:** pred is not "compare a[i] with x" but a fact you derived about
position i.
**Why it works:** binary search needs only that the answers to pred flip once.
**Examples:**

- Missing number in [11, 12, 14, 15, 16]: pred(i) = a[i] > a[0] + i. Answers
  F F T T T, first true 2, missing value a[0] + 2 = 13. Before the gap every value
  sits exactly where it would without a gap; after it, every value is shifted by
  at least one. That "shifted yet?" fact is monotone.
  [[p:arista-networks-first-missing-number-in-consecutive-array|First Missing Number in a Consecutive Array]].
- Single element in [1, 1, 2, 3, 3, 4, 4, 8, 8]: before the single value, every
  pair starts at an even index (1 sits at 0 and 1). After it, every pair is pushed
  one step right and starts at an odd index (3 sits at 3 and 4). So, for even i,
  ask "is a[i] != a[i+1]?": it is no while the pairs are still aligned and yes from
  the single value on. For i = 0: 1 vs 1, no. For
  i = 2: 2 vs 3, yes. For i = 4: 3 vs 4, yes. The first yes among even indices is 2,
  and a[2] = 2 is the answer. Search over even indices only: i = 2k, and binary
  search over k. [[p:atlassian-single-element-in-a-sorted-array|Single Element in a Sorted Array]].
- Peak in [1, 3, 7, 9, 4, 2]: pred(i) = a[i] > a[i+1] for i in 0..n-2, with i = n - 1
  as the sentinel yes (the last element is always "downhill" from nothing).
  Answers F F F T T, first true 3. [[p:blinkit-find-peak-element|Find a Peak Element]].
  When there can be several peaks, the same search still returns a peak, just not
  necessarily a particular one: wherever lo is "still climbing" and hi is "going
  down", there is a top between them.

### C. Lower bound, upper bound and counting with bisect

**What changes:** pred is `a[i] >= x` or `a[i] > x`, and the answer is used as a
count or a neighbour rather than a position.
**Why:** an index in a sorted array is a count: the number of entries before it.
**Example:** in [2, 3, 5, 5, 5, 8, 13], "how many are at most 6" is
bisect_right(a, 6) = 5.

The practice ladder here is all small stories around one bisect call.
[[p:swiggy-first-and-last-occurrence|First and Last Occurrence]] is the two bounds.
[[p:tiktok-debugger-breakpoint-actions|Debugger Breakpoint Actions]] hides
bisect_right on the sorted breakpoints: "continue from line x" goes to the first
breakpoint strictly after x. [[p:tiktok-next-shuttle-wait-time|Wait Until the Next Shuttle]]
converts HH:MM to minutes and then takes bisect_left, because a shuttle leaving
exactly now still counts; if the statement had said "strictly after now", it
would be bisect_right, and that one word is the entire edge case.
[[p:atlassian-time-based-key-value-store|Time Based Key-Value Store]] is the
predecessor: bisect_right(ts, t) - 1, with -1 meaning "no value yet".
[[p:two-sigma-linear-interpolator|Linear Interpolator]] uses a bisect on the
sorted knots to find the segment around x, and then interpolates.

### D. A rotated sorted array

**What changes:** [4, 5, 6, 7, 0, 1, 2] was sorted and then rotated. "a[i] >= x" is
no longer monotone. You must find a different question that is.
**Why it works:** a rotated array is two sorted runs, and every value in the first
run is larger than every value in the second.

**The minimum.** Compare each element with the last one. Elements of the first run
are bigger than the last element; elements of the second run are at most it. So
pred(i) = a[i] <= a[n-1] reads F F F F T T T. The first true is the start of the
second run, the minimum. Index n - 1 is always a yes (a[n-1] <= a[n-1]), so it can be
the starting hi; lo = -1.

| step | lo | hi | mid | a[mid] | a[mid] <= 2? | move |
|---|---|---|---|---|---|---|
| 1 | -1 | 6 | 2 | 6 | no | lo = 2 |
| 2 | 2 | 6 | 4 | 0 | yes | hi = 4 |
| 3 | 2 | 4 | 3 | 7 | no | lo = 3 |
| end | 3 | 4 | | | | min at 4, value 0 |

Why compare with the last element and not the first? With the first, an unrotated
array [1, 2, 3] answers "a[i] < a[0]?" with F F F, and the search returns n, which
you must then special-case to 0. With the last, the unrotated array answers
T T T and the search returns 0 directly. Same idea, one fewer special case.
[[p:goldman-sachs-minimum-in-rotated-sorted-array|Minimum in a Rotated Sorted Array]].

**Searching for a target, in two passes.** Find the start p of the second run
with the search above. Now the array is two sorted lists, a[0..p-1] and a[p..n-1].
If p = 0 or x < a[0], x can only be in the second; otherwise it can only be in the
first. Lower bound inside that one. Three lines on top of the minimum search, and
each line is something you have already proven.

**Searching for a target, in one pass.** The version in
[[p:amazon-search-rotated-sorted-array|Search in a Rotated Sorted Array]]
editorials: at every mid, at least one of the two halves [lo..mid] and [mid..hi]
is sorted, and you can tell which by comparing a[lo] with a[mid]. If the left half
is sorted and x lies within its range, keep the left half; otherwise keep the right.
It is shorter, and it has a trap in the comparison (see Traps). Both versions are
in the program below.

**With duplicates** ([2, 2, 2, 0, 2]), a[lo] = a[mid] = a[hi] tells you nothing about
which side is sorted, and the only safe move is to shrink by one. The worst case
becomes O(n). It is rare, and the chapter [[search-rotated]] has it.

### E. A sorted matrix

Two different promises, two different algorithms. Read the statement carefully to
tell which one you have.

**Rows continue one another** ("the first value of each row is larger than the
last value of the previous row"). Then the matrix, read row by row, is one sorted
list of m · c values. Binary search over k in 0..m·c-1 and read the cell at
row k // c, column k % c. O(log(m·c)). In
[[p:amazon-search-row-major-sorted-matrix|Search a Row-Major Sorted Matrix]],
the matrix `[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]` has c = 4, and k = 5 is row 1,
column 1, value 11.

**Only rows and columns are sorted** (each row left to right, each column top to
bottom, but row 2 may start below the end of row 1). There is no single sorted
order to binary search. Start at the top-right corner. If the value there is bigger
than x, everything below it in that column is bigger still, so the whole column is
out: move left. If it is smaller, everything left of it in that row is smaller still,
so the whole row is out: move down. Each step removes a row or a column, so it
takes at most m + c steps. This is not halving, but it is the same thought as the
unlocking question: a single comparison settles a whole line of cells you never
look at. [[p:goldman-sachs-staircase-search|Staircase Search In A Sorted Matrix]].

(Binary searching each row separately is also correct, at O(m log c). It is fine
when one dimension is tiny, and it is the answer interviewers do not want.)

The program below runs the rotated searches and both matrix searches, and checks
each against a brute-force scan on random inputs.

```python run
import random
from bisect import bisect_left

def first_true(lo, hi, pred):
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if pred(mid): hi = mid
        else:         lo = mid
    return hi

def rotated_min_index(a):             # a[i] <= a[-1]:  F..F T..T
    return first_true(-1, len(a) - 1, lambda i: a[i] <= a[-1])

def rotated_search_two_pass(a, x):
    p, n = rotated_min_index(a), len(a)
    lo, hi = (p, n) if (p == 0 or x < a[0]) else (0, p)
    i = lo + bisect_left(a[lo:hi], x) if hi > lo else lo   # (slice only for brevity)
    return i if i < hi and a[i] == x else -1

def rotated_search_one_pass(a, x):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[lo] <= a[mid]:           # left half [lo..mid] is sorted
            if a[lo] <= x < a[mid]: hi = mid - 1
            else:                   lo = mid + 1
        else:                         # right half [mid..hi] is sorted
            if a[mid] < x <= a[hi]: lo = mid + 1
            else:                   hi = mid - 1
    return -1

def matrix_flat(m, x):                # rows continue one another
    if not m: return False
    r, c = len(m), len(m[0])
    k = first_true(-1, r * c, lambda k: m[k // c][k % c] >= x)
    return k < r * c and m[k // c][k % c] == x

def staircase(m, x):                  # rows and columns sorted, nothing more
    i, j = 0, len(m[0]) - 1
    while i < len(m) and j >= 0:
        if m[i][j] == x: return True
        if m[i][j] > x: j -= 1        # whole column j is too big below here
        else:           i += 1        # whole row i is too small left of here
    return False

a = [4, 5, 6, 7, 0, 1, 2]
print("rotated", a, "min at", rotated_min_index(a), "| find 0:",
      rotated_search_two_pass(a, 0), rotated_search_one_pass(a, 0))
assert rotated_min_index(a) == 4 and rotated_min_index([1, 2, 3]) == 0
M = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
print("row-major find 3:", matrix_flat(M, 3), " find 13:", matrix_flat(M, 13))
assert matrix_flat(M, 3) and not matrix_flat(M, 13)

random.seed(3)
for _ in range(400):
    s = sorted(random.sample(range(50), random.randint(1, 9)))
    r = random.randrange(len(s))
    a = s[r:] + s[:r]                 # a random rotation
    assert a[rotated_min_index(a)] == min(a)
    for x in range(-1, 51):
        want = a.index(x) if x in a else -1
        assert rotated_search_two_pass(a, x) == want == rotated_search_one_pass(a, x)
    rows, cols = random.randint(1, 4), random.randint(1, 4)
    g = [[random.randint(0, 3) for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):             # make rows and columns nondecreasing
        for j in range(cols):
            g[i][j] += max(g[i-1][j] if i else 0, g[i][j-1] if j else 0)
    for x in range(0, 30):
        assert staircase(g, x) == any(x in row for row in g)
print("rotated (both ways) and staircase agree with a scan on 400 random cases")
```

### F. No upper end: exponential search

**What changes:** you do not know n (a stream, an API, an "infinite" sorted array).
**Why it works:** first find any known yes by doubling: probe 1, 2, 4, 8, ... until
pred says yes at 2^j. The previous probe 2^(j-1) is a known no. Now binary search
between them.
**Example:** first bad at 37: probes 1, 2, 4, 8, 16, 32 say no, 64 says yes. Search
(32, 64]: five more probes. Total about 2 log₂(answer), and the cost depends on the
answer, not on a length nobody told you. This is rare in OAs and a common follow-up
in phone screens.

### G. The search space is not an array

When the positions you search are candidate answers (a speed, a capacity, a
distance, a time) and pred is "can it be done with this much?", the loop is
unchanged and the problem looks nothing like a search. This is the most important
variation in interviews, and it has its own chapter:
[[binary-search-on-answer]]. The same chapter covers searching over real numbers,
where the loop stops after a fixed number of halvings instead of at width 1.

### H. Rarer uses worth recognising

- **Inside another algorithm.** The O(n log n) longest increasing subsequence
  keeps a sorted list of "smallest tail of an increasing run of each length" and
  does one bisect_left per element ([[lis]]).
- **k-th smallest of something too big to list.** The k-th smallest value in a
  sorted matrix, or the k-th smallest pair distance: binary search over the value,
  with pred "at least k things are <= v?". That is a counting predicate, and it is
  the bridge to [[binary-search-on-answer]].
- **bisect with a key.** Since Python 3.10, `bisect_left(a, x, key=f)` searches a
  list sorted by f. Before that, search a parallel list of keys.

## Recognising it in a statement

Signals, the most reliable first.

1. **"Sorted" plus "first", "last", "count", "how many", "closest",
   "insert".** Lower or upper bound, often just one bisect.
2. **"O(log n)" in the statement.** The problem is telling you. A sorted array,
   a rotation, a peak, a matrix.
3. **"Once X happens, it stays X"**, "every version after a bad one is bad",
   "non-decreasing", "the water only rises". Someone is describing a monotone
   question in words.
4. **Many queries against fixed data.** q up to 10^5 and n up to 10^5 with a
   "how many below x" or "latest before t" query: sort once, bisect per query.
5. **Constraints that want n log n**, where the obvious solution is n² and one
   factor of n is a scan you could replace by a search.
6. **"Minimum capacity", "least speed", "smallest k such that", "maximise the
   minimum".** That is the search-on-the-answer family.

**Disguised forms.** A problem rarely says "binary search". It says:

- "Find the missing number in a sorted run": derived pred a[i] > a[0] + i.
- "Every element appears twice except one, sorted, logarithmic time": pair parity.
- "Strictly greater than both neighbours, logarithmic time": am-I-downhill.
- "Latest value before time t": predecessor, bisect_right - 1.
- "Next departure at or after now": ceiling, bisect_left.

**Anti-signals.**

- The question is not monotone: "an index where a[i] equals i in an array with
  duplicates" (with distinct sorted integers it is monotone, a[i] - i never
  decreases; with duplicates it can).
- Contiguous sums with negative numbers. A prefix sum is sorted only if every
  element is non-negative. With negatives, "first prefix sum at least T" is not a
  binary search ([[prefix-sums]]).
- One query, unsorted: scan.
- A linked list: no random access, no speedup.

## Traps

**Stopping on a hit.** Symptom: "first occurrence" is right on arrays without
duplicates and wrong on [1, 2, 2, 2, 4]. Cure: search the boundary of a[i] >= x
and check equality after.

**A window that does not shrink.** Symptom: time limit exceeded on a two-element
window, often only for some targets. Cause: mid = lo and the branch assigns
lo = mid. Cure: the half-open template, or round mid toward the pointer the yes
branch does not assign. Demonstrated above.

**Dishonest sentinels.** Symptom: the answer can never be index 0, or can never be
"none". Cause: lo = 0 when index 0 might be a yes, or hi = n - 1 when nothing might
be a yes. Cure: -1 and n, never read.

**`>=` where you meant `>`.** Symptom: off by the whole run of duplicates. Cure:
write the question in words first.

**Non-monotone predicate.** Symptom: correct on sorted tests, wrong on rotated or
shifted ones. Cure: check the shape (write out pred on a small example, as in
Worked by hand) before coding.

**Slicing in a recursive search.** Symptom: correct but O(n), times out on 10^6.
Cure: pass indices.

**`(lo + hi) / 2` in a language with fixed-size ints.** Symptom: negative index or
crash at around 2^30. Cure: lo + (hi - lo) / 2.

**The rotated search comparison.** In the one-pass rotated search, "is the left
half sorted?" must be `a[lo] <= a[mid]`, not `<`. When the window has two elements,
lo and mid are the same index, the left half is one element, and one element is
sorted. With `<`, the code decides the left half is not sorted, treats the right
half as sorted when it is not, and can throw the target away. The demonstration:

```python run
def search(a, x, left_sorted):
    lo, hi = 0, len(a) - 1
    trace = []
    while lo <= hi:
        mid = (lo + hi) // 2
        trace.append((lo, mid, hi))
        if a[mid] == x:
            return mid, trace
        if left_sorted(a[lo], a[mid]):
            if a[lo] <= x < a[mid]: hi = mid - 1
            else:                   lo = mid + 1
        else:
            if a[mid] < x <= a[hi]: lo = mid + 1
            else:                   hi = mid - 1
    return -1, trace

a, x = [3, 1], 1
wrong = search(a, x, lambda l, m: l < m)
right = search(a, x, lambda l, m: l <= m)
print("a =", a, "x =", x)
print("with  < :", wrong[0], " (lo, mid, hi) steps:", wrong[1])
print("with <= :", right[0], " (lo, mid, hi) steps:", right[1])
assert wrong[0] == -1 and right[0] == 1

# the < version fails on many rotated arrays; the <= version on none
import itertools
fails = 0
for n in range(1, 8):
    base = list(range(10, 10 + n))
    for r in range(n):
        arr = base[r:] + base[:r]
        for v in arr:
            assert search(arr, v, lambda l, m: l <= m)[0] == arr.index(v)
            fails += search(arr, v, lambda l, m: l < m)[0] != arr.index(v)
print("'<' version wrong on", fails, "of the (array, target) pairs; '<=' on none")
assert fails > 0
```

Point at the failing step: lo = 0, mid = 0, hi = 1. a[0] = 3 is not 1. With `<`,
3 < 3 is false, so the code believes the right half [mid..hi] = [3, 1] is sorted,
checks whether 1 lies in (3, 1], decides it does not, and sets hi = -1. The target
was in the half it discarded.

## What to memorise

**The template.** Type it from memory until you cannot get it wrong:

```python
lo, hi = -1, n                  # lo: a known no.  hi: a known yes.
while hi - lo > 1:
    mid = lo + (hi - lo) // 2   # strictly between: the loop always shrinks
    if pred(mid):
        hi = mid
    else:
        lo = mid
# hi: first yes (n means none).  lo: last no (-1 means none).
```

And its library names: `bisect_left(a, x)` is the first yes of a[i] >= x;
`bisect_right(a, x)` is the first yes of a[i] > x.

**The sentence that turns a problem into it:** *what yes/no question about a
position is no at the start, yes at the end, and flips exactly once?*

**The question that finds that sentence:** *what does one probe tell me about the
positions I did not look at?*

**The habit:** before writing the loop, say what lo and hi mean as facts, not as
"left" and "right". "lo is an index I have proven is too small." If you cannot say
it, the loop is guesswork.

**The numbers:** log₂ 10^5 ≈ 17, log₂ 10^6 ≈ 20, log₂ 10^9 ≈ 30, log₂ 10^18 ≈ 60.

## Check yourself

:::check
Hand trace. a = [1, 4, 4, 4, 6, 9, 9, 12] (n = 8). Run the template for the lower
bound of 9 and for the upper bound of 4, writing lo, hi, mid and the answer to
pred at every step. Then say how many 4s there are using one more search.
--
Lower bound of 9 (pred: a[mid] >= 9), lo = -1, hi = 8:

| lo | hi | mid | a[mid] | >= 9? | move |
|---|---|---|---|---|---|
| -1 | 8 | 3 | 4 | no | lo = 3 |
| 3 | 8 | 5 | 9 | yes | hi = 5 |
| 3 | 5 | 4 | 6 | no | lo = 4 |
| 4 | 5 | | | | stop, answer 5 |

Upper bound of 4 (pred: a[mid] > 4), lo = -1, hi = 8:

| lo | hi | mid | a[mid] | > 4? | move |
|---|---|---|---|---|---|
| -1 | 8 | 3 | 4 | no | lo = 3 |
| 3 | 8 | 5 | 9 | yes | hi = 5 |
| 3 | 5 | 4 | 6 | yes | hi = 4 |
| 3 | 4 | | | | stop, answer 4 |

The lower bound of 4 is 1 (a[0] = 1 < 4, a[1] = 4). Count of 4s = 4 - 1 = 3: indices
1, 2, 3.
:::

:::check
Hand trace. The rotated array [6, 8, 9, 11, 2, 3, 5] (n = 7). Find the minimum with
pred(i) = a[i] <= a[6]. Then find the index of 3 with the two-pass method.
--
a[6] = 5. pred answers: 6 no, 8 no, 9 no, 11 no, 2 yes, 3 yes, 5 yes. lo = -1,
hi = 6 (index 6 is always a yes).

| lo | hi | mid | a[mid] | <= 5? | move |
|---|---|---|---|---|---|
| -1 | 6 | 2 | 9 | no | lo = 2 |
| 2 | 6 | 4 | 2 | yes | hi = 4 |
| 2 | 4 | 3 | 11 | no | lo = 3 |
| 3 | 4 | | | | stop: p = 4, minimum 2 |

Two passes: p = 4, and x = 3 < a[0] = 6, so 3 can only be in the second run,
a[4..6] = [2, 3, 5]. Its lower bound of 3 is offset 1, so index 4 + 1 = 5, and
a[5] = 3. Found at 5.
:::

:::check
Someone writes `lo, hi = 0, n - 1` and `while lo < hi: mid = (lo + hi) // 2; if
a[mid] < x: lo = mid + 1 else: hi = mid` and returns lo as the lower bound. Is it
correct? Where does it differ from the half-open template?
--
It always terminates: mid rounds down, so mid < hi, and the yes branch assigns hi =
mid (a strict decrease) while the no branch assigns lo = mid + 1 (a strict
increase). It finds the first index with a[i] >= x correctly whenever such an index
exists.

It differs when nothing is >= x. Its hi starts at n - 1, which it treats as a known
yes without checking. For a = [1, 2] and x = 5 it returns 1, an index whose value
is 2, not 5 and not >= 5. The half-open template returns n = 2, meaning "none". The
closed version needs either hi = n (then it is the same template in different
clothes) or a final check of a[lo] >= x. The bug is a dishonest sentinel.
:::

:::check
Why does the half-open template never need a `mid + 1` or `mid - 1`, while the
closed `while lo <= hi` template does?
--
In the half-open template, lo and hi are not candidates: they are positions whose
answers are already proven (a no and a yes). After probing mid, mid's answer is
proven too, so it becomes the new lo or hi exactly. Nothing is excluded or kept
"by one".

In the closed template, lo and hi are the ends of the set of candidates still in
doubt. After probing mid, mid is no longer in doubt, so it must be excluded from
the candidates, and that is the + 1 or - 1. The two templates are equally correct;
the difference is what the pointers mean. The +-1 is the price of meaning
"candidate" instead of "proven".
:::

:::check
A candidate says "this array isn't sorted, so we can't binary search it" about
[1, 3, 7, 9, 4, 2] and the task "return the index of the peak". Where are they
wrong? Give the predicate and the search.
--
Binary search needs a monotone question, not a sorted array. pred(i) = "a[i] >
a[i+1]" (am I already going down?) for i = 0..4, with index 5 as the sentinel yes,
answers no, no, no, yes, yes: monotone, because the array rises then falls.

lo = -1, hi = 5. mid = 2: 7 > 9? no, lo = 2. mid = 3: 9 > 4? yes, hi = 3. Stop:
the peak is index 3, value 9. Three probes, no sorting anywhere.
:::

:::check
Disguised problem. Logs are sorted by timestamp. For each of 10^5 queries "how many
log lines fall in the window [L, R]", the obvious solution scans. Reduce it to the
template, and give the cost.
--
The count of timestamps in [L, R] is (the number <= R) minus (the number < L), that
is bisect_right(ts, R) - bisect_left(ts, L). Each query is two binary searches,
O(log n), so 10^5 queries over 10^5 lines cost about 2 · 10^5 · 17 ≈ 3.4 million
steps instead of 10^10. If the logs did not arrive sorted, sort once at O(n log n)
first. The pitfall is the endpoints: "in [L, R]" includes both, which is why the
right end uses bisect_right and the left end uses bisect_left.
:::

:::check
You must find the first bad version, and checking one version takes ten minutes.
There are 1,000 versions. How long does the scan take in the worst case, and how
long does binary search take? What property of the problem makes the second
possible?
--
The scan checks up to 1,000 versions: 10,000 minutes, about a week. Binary search
checks ⌈log₂ 1001⌉ = 10 versions: 100 minutes.

It is possible because "is version i bad?" is monotone: a good version proves that
every earlier version is good, and a bad version proves that the answer is at or
before it. So each check settles a whole side of the remaining versions, and the
middle check settles half of them whatever the answer is.
:::
