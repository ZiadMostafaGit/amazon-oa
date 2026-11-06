# Two Pointers

> Two pointers works when one comparison can retire an element for good, so that instead of trying every pair you take n steps, each of which throws away a whole row of pairs you never had to look at.

## The problem it solves

Here is a sorted array and a target:

```
a      = [1, 3, 4, 6, 8, 11]
target = 10
```

Find two different positions whose values add up to 10. This is
[[p:london-stock-exchange-two-sum-sorted|Two Sum in a Sorted Array]], and it is
the problem the whole chapter grows out of. The answer is positions 2 and 3,
because 4 + 6 = 10.

The first solution anyone writes is the double loop: for every i, for every
j > i, test a[i] + a[j]. It is correct. It is also slow in a way that is easy to
count. Six elements have 6 * 5 / 2 = 15 pairs. A hundred thousand elements, the
limit in that problem, have about 5 * 10^9 pairs. A judge gives you about 10^8
simple steps per second, so the double loop needs most of a minute. It fails.

The second solution is a hash set: walk the array once, and for each value x ask
whether target - x has been seen. That is linear time, and for this exact
problem with an unsorted array it is the right tool ([[hash-tables]]). But it
spends O(n) memory, the problem asks for constant extra space, and, more
importantly, the hash trick only answers "is there a pair with this exact sum".
It does not answer "the pair whose sum is closest to 10", "how many pairs have
sum at most 10", "the two lines that hold the most water", or "is this string a
palindrome". All of those fall to the method in this chapter, and the hash set
does nothing for them.

What this chapter builds is a way to look at only n of the pairs and still be
sure of the answer. The trick is not "use two indices". Every double loop uses
two indices. The trick is that **one comparison can prove that one element is
finished**, that it cannot be part of any answer with any partner still left,
and so it can be crossed off for good. Cross off one element per step and you
are done in at most n steps.

That single idea shows up in six shapes, and this chapter teaches all six:

1. **Converging pointers on a sorted array**: pair sum, closest pair, pairs
   under a limit.
2. **Fix one element, two-pointer the rest**: 3Sum and its relatives.
3. **Reader and writer**: compact an array in place.
4. **Walk two sequences together**: merge, intersect, match.
5. **Move the side that cannot improve**: Container With Most Water, Trapping
   Rain Water.
6. **Compare from both ends**: palindromes.

### When it is the wrong tool

- **Unsorted, and the answer is original positions.** Sorting would make the
  sweep possible and destroy the positions. Use a hash map, or sort
  (value, index) pairs and accept the n log n.
- **The question is about a contiguous stretch whose quality depends on what is
  inside it**, such as "the longest substring with no repeated letter". That uses
  two indices that both move right, but the left one is chasing a property of
  the window, not retiring a partner. It is [[sliding-window]], the next chapter.
- **No comparison retires anything.** If knowing a[i] + a[j] tells you nothing
  about a[i] + a[j-1], there is no elimination, and two pointers is a double loop
  with extra steps. "Is there a pair whose product is a perfect square" is like
  this, even on sorted data.
- **The pointers move at different speeds along a linked structure**, to find a
  cycle or a middle. That is its own chapter, [[fast-slow-pointers]].

This bank has 432 problems that use two pointers, which makes it one of the most
common techniques there is. Most of them are one of the six shapes above with a
thin story on top.

## Build it from the brute force

We will start from the double loop and fix it one waste at a time. The two
pointer loop will appear at the end as the obvious repair, not as a trick.

### Step 1: the double loop, and what it actually computes

```python
def pair_brute(a, t):
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] + a[j] == t:
                return (i, j)
    return None
```

Every pair (i, j) with i < j is tried once. To see what that means, lay all the
sums out as a grid: row i, column j, one cell per pair. The cells with j <= i do
not exist (a pair needs two different positions), so the grid is a triangle.

| | j=1 (3) | j=2 (4) | j=3 (6) | j=4 (8) | j=5 (11) |
|---|---|---|---|---|---|
| **i=0 (1)** | 4 | 5 | 7 | 9 | 12 |
| **i=1 (3)** | | 7 | 9 | 11 | 14 |
| **i=2 (4)** | | | 10 | 12 | 15 |
| **i=3 (6)** | | | | 14 | 17 |
| **i=4 (8)** | | | | | 19 |

The double loop reads this table row by row, left to right, until it finds a 10.
Here it reads 4, 5, 7, 9, 12, 7, 9, 11, 14, 10: ten cells. In the worst case it
reads all fifteen.

### Step 2: count it

The triangle has n(n-1)/2 cells. The double loop's cost is the number of cells
it reads, and with no answer present it reads all of them. For n = 10^5 that is
about 5 * 10^9. There is nothing clever to tune: the loop is already as tight as
a loop can be. If it is to get faster, it has to read fewer cells.

### Step 3: notice the waste

Look at the grid again. Because the array is sorted, the grid is sorted too, in
both directions. Moving right along a row, the second value grows, so the sums
grow: 4, 5, 7, 9, 12. Moving down a column, the first value grows, so the sums
grow: 12, 14, 15, 17, 19.

Now look at one cell, the top right corner, row 0, column 5: 1 + 11 = 12. That is
too big. What does it tell us?

It is the *top* of column 5. Every other cell in column 5 is below it, and the
column grows downward. So every cell in column 5 is at least 12, and none of them
is 10. In words: 11 is too big even with the smallest partner it could have, 1,
so it is too big with every partner. **The element 11 is finished.** One
comparison, five cells ruled out.

The double loop does not know this. It will later read 14, 15, 17 and 19 in
column 5, one at a time, learning nothing it could not have known from the 12.

The mirror case works the same way. Row 0, column 4: 1 + 8 = 9, too small. That
cell is the *right end* of what is left of row 0 once column 5 is gone. The row
grows to the right, so every other surviving cell in row 0 is at most 9. The
element 1 is too small even with the largest partner it has left, 8, so it is
too small with every partner. **The element 1 is finished.**

That is the waste: the brute force reads cells one at a time, but a single cell,
read in the right place, settles a whole row or a whole column.

### The question that unlocks it

Every problem in this family turns on one question:

**When I look at this one pair, which element can I prove is useless with every
partner it has left?**

If the answer is "this one", cross it off and move its pointer. If the answer is
"I cannot prove anything about either", you do not have a two pointer problem.

Say it a second way. The double loop asks "is *this pair* the answer?". Two
pointers asks "is *this element* still worth keeping?". The first question has
n^2/2 instances. The second has n.

### Step 4: which cell to read

Reading the corner was not an accident. A cell retires a whole column only if it
is the *smallest* surviving cell in that column, and a whole row only if it is
the *largest* surviving cell in that row. The one cell that is both, the extreme
of its row and of its column at once, is the top right corner of what is left:
the smallest surviving first element with the largest surviving second element.

So keep two indices:

- lo, the smallest index not yet crossed off, and
- hi, the largest index not yet crossed off.

Read a[lo] + a[hi]. If it is too big, a[hi] is finished: hi moves down. If it is
too small, a[lo] is finished: lo moves up. If it is equal, you have the pair. The
surviving grid always has its corner at (lo, hi), so the next read is again the
one cell that can retire something.

### You might think: "When the sum is too small, it doesn't matter which pointer I move."

It does. Take a = [2, 3, 7, 9] and target 10. The only pair is 3 + 7.

- (0, 3): 2 + 9 = 11, too big. Move hi to 2.
- (0, 2): 2 + 7 = 9, too small.

Now suppose you move hi instead of lo, because "something has to move". You
reach (0, 1): 2 + 3 = 5, and you have thrown away the 7, which was in the
answer. The rule is not "make the sum change". The rule is "retire the element
you have proved useless". At (0, 2) you proved 2 is useless (too small with the
largest partner it has left). You proved nothing about 7: it was too big with 9
before, but 9 is gone and 7 has never been tried with 3.

Put differently: moving hi down when the sum is too small makes the sum *smaller*,
which is the wrong direction, and it also retires an element without a reason.
Both are fatal.

### You might think: "The array isn't sorted, so I'll sort it first and run the loop."

For "is there a pair", sorting first is fine. For "return the positions", it
silently returns the wrong positions. Take a = [3, 2, 4], target 6. The answer is
positions 1 and 2 (2 + 4). Sorted, the array is [2, 3, 4], and the sweep finds
positions 0 and 2 of the *sorted* array, which are values 2 and 4 but which, in
the original array, would point at 3 and 4. The sum is right, the answer is
wrong, and the bug only shows when the input was not already sorted. Either
carry the original index along with each value, or use a hash map.

### You might think: "The loop runs while lo <= hi, like binary search."

Binary search looks at a single index and needs lo <= hi so that a range of one
element still gets checked. Two pointers looks at a *pair*, and a pair needs two
different positions. With lo <= hi, the loop eventually reads a[lo] + a[lo], one
element added to itself. On a = [1, 3, 4, 6] with target 8, the sweep goes
(0,3)=7 small, (1,3)=9 big, (1,2)=7 small, (2,2)=8: "found". But 4 is in the array
only once. The correct answer is "no pair". The traps section runs this.

### Step 5: the same idea in the other five shapes

The converging loop is the clearest case, but the sentence "one comparison
retires an element for good" is what all six shapes share. Here is the brute
force each one replaces, and what gets retired.

- **3Sum.** Brute force: three nested loops, n^3 / 6 triples. Fix the first
  element; the other two are a sorted pair-sum problem. Each inner step retires
  one element *for this fixed first element*.
- **Reader and writer.** Brute force: build a second list of the elements you
  keep (O(n) memory), or delete from the middle of the list (each deletion
  shifts everything after it, O(n^2) time). Two pointers: a reader looks at
  every element once and is retired after one look; a writer marks where the
  kept part ends.
- **Merge two sorted lists.** Brute force: concatenate and sort, O((n+m) log(n+m)).
  Two pointers: compare the two fronts; the smaller one is the next output and
  is retired.
- **Container With Most Water.** Brute force: try all pairs of lines. Two
  pointers: the shorter of the two end lines cannot do better with any closer
  partner, so it is retired.
- **Palindrome.** Brute force for "is it a palindrome after deleting at most one
  character": try deleting each character, O(n^2). Two pointers: matching end
  characters are settled and retired from both ends at once.

In every case, the pointer only moves one way. A move never needs to be undone,
because the element left behind was *proved* finished, not guessed. That is also
the whole cost analysis: each pointer can only move n times.

### The technique in one sentence

**Two pointers: keep one index at each end of what is still undecided, compare
the two elements there, and move the pointer whose element the comparison has
proved can never be part of an answer; since nothing is ever reconsidered, the
work is the distance the pointers travel, at most n.**

And the question that produced it: **when I look at this pair, which element can
I prove is useless with every partner it has left?**

## Worked by hand

Get a pen. a = [1, 3, 4, 6, 8, 11], target 10, lo = 0, hi = 5.

| step | lo | hi | a[lo] | a[hi] | sum | verdict | move | what is retired |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 1 | 11 | 12 | too big | hi = 4 | 11, with all 5 partners |
| 2 | 0 | 4 | 1 | 8 | 9 | too small | lo = 1 | 1, with its 4 remaining partners |
| 3 | 1 | 4 | 3 | 8 | 11 | too big | hi = 3 | 8, with its 3 remaining partners |
| 4 | 1 | 3 | 3 | 6 | 9 | too small | lo = 2 | 3, with its 2 remaining partners |
| 5 | 2 | 3 | 4 | 6 | 10 | equal | stop | answer (2, 3) |

Step 3, told in full:

> "Elements 1 and 11 are gone. What is left is positions 1 to 4: 3, 4, 6, 8. I
> read the two ends, 3 and 8. Their sum is 11, one too many. 3 is the smallest
> thing still on the table, so 8 cannot do better with anyone else: 8 + 4 = 12
> and 8 + 6 = 14 are both bigger than 8 + 3. So 8 is finished, and I never need
> to read 8 + 4 or 8 + 6. hi moves from 4 to 3."

Five reads instead of fifteen. Here are the same five reads on the grid of sums,
so you can see what each one wiped out.

<svg viewBox="0 0 640 330" role="img" aria-label="the triangle of pair sums for the array 1, 3, 4, 6, 8, 11; the five cells the two pointer sweep reads are shaded and numbered 1 to 5 in the order they are read: 12 at row 0 column 5, 9 at row 0 column 4, 11 at row 1 column 4, 9 at row 1 column 3, and 10 at row 2 column 3; each read retires the rest of its column or its row">
  <g>
    <text x="155" y="30" text-anchor="middle">j=1 (3)</text>
    <text x="245" y="30" text-anchor="middle">j=2 (4)</text>
    <text x="335" y="30" text-anchor="middle">j=3 (6)</text>
    <text x="425" y="30" text-anchor="middle">j=4 (8)</text>
    <text x="515" y="30" text-anchor="middle">j=5 (11)</text>
    <text x="20" y="72">i=0 (1)</text>
    <text x="20" y="122">i=1 (3)</text>
    <text x="20" y="172">i=2 (4)</text>
    <text x="20" y="222">i=3 (6)</text>
    <text x="20" y="272">i=4 (8)</text>
    <rect x="110" y="45" width="90" height="50"/>
    <text x="155" y="76" text-anchor="middle">4</text>
    <rect x="200" y="45" width="90" height="50"/>
    <text x="245" y="76" text-anchor="middle">5</text>
    <rect x="290" y="45" width="90" height="50"/>
    <text x="335" y="76" text-anchor="middle">7</text>
    <rect class="fill" x="380" y="45" width="90" height="50"/>
    <text x="425" y="76" text-anchor="middle">9</text>
    <text x="460" y="60" text-anchor="end">2</text>
    <rect class="fill" x="470" y="45" width="90" height="50"/>
    <text x="515" y="76" text-anchor="middle">12</text>
    <text x="550" y="60" text-anchor="end">1</text>
    <rect x="200" y="95" width="90" height="50"/>
    <text x="245" y="126" text-anchor="middle">7</text>
    <rect class="fill" x="290" y="95" width="90" height="50"/>
    <text x="335" y="126" text-anchor="middle">9</text>
    <text x="370" y="110" text-anchor="end">4</text>
    <rect class="fill" x="380" y="95" width="90" height="50"/>
    <text x="425" y="126" text-anchor="middle">11</text>
    <text x="460" y="110" text-anchor="end">3</text>
    <rect x="470" y="95" width="90" height="50" stroke-dasharray="4 4"/>
    <text x="515" y="126" text-anchor="middle">14</text>
    <rect class="fill" x="290" y="145" width="90" height="50"/>
    <text x="335" y="176" text-anchor="middle">10</text>
    <text x="370" y="160" text-anchor="end">5</text>
    <rect x="380" y="145" width="90" height="50" stroke-dasharray="4 4"/>
    <text x="425" y="176" text-anchor="middle">12</text>
    <rect x="470" y="145" width="90" height="50" stroke-dasharray="4 4"/>
    <text x="515" y="176" text-anchor="middle">15</text>
    <rect x="380" y="195" width="90" height="50" stroke-dasharray="4 4"/>
    <text x="425" y="226" text-anchor="middle">14</text>
    <rect x="470" y="195" width="90" height="50" stroke-dasharray="4 4"/>
    <text x="515" y="226" text-anchor="middle">17</text>
    <rect x="470" y="245" width="90" height="50" stroke-dasharray="4 4"/>
    <text x="515" y="276" text-anchor="middle">19</text>
    <text x="320" y="318" text-anchor="middle">shaded: the 5 cells read, in order. dashed: cells never read, ruled out by a read above or to the left</text>
  </g>
</svg>

Read 1 (the 12) is the top of column 5, so it rules out every dashed cell under
it: 14, 15, 17, 19. Read 2 (the 9) is the right end of the surviving row 0, so it
rules out 4, 5 and 7 to its left. Read 3 (the 11) is the top of the surviving
column 4, ruling out 12 and 14 below it. Read 4 rules out the 7 to its left in
row 1. Read 5 is the answer. The staircase of shaded cells walks down and to the
left, and it can never turn back, because every cell it leaves behind is already
decided.

Two things in this trace are worth more than the answer.

**Each step retires a whole element, not a pair.** That is why there are at most
n - 1 steps: there are only n elements to retire, and the last one has no
partner left.

**Nothing in the trace ever goes back.** lo only rises and hi only falls. If your
plan for a problem needs lo to go back and reconsider something, the
elimination you thought you had is not real, and no amount of careful coding
will fix it.

### A second trace: an elimination with no sorting at all

[[p:amazon-container-with-most-water|Container With Most Water]]: heights
h = [1, 8, 6, 2, 5, 4, 8, 3, 7]. Pick two lines; the water they hold is the
distance between them times the shorter line. Find the most water.

The array is not sorted, and the score is not a sum. But ask the question anyway.
At the two ends, lines 0 (height 1) and 8 (height 7) hold 8 * 1 = 8. Which of
the two can I prove is finished?

The shorter one. Line 0 has height 1. With *any* partner j between them, the
width is smaller than 8, and the water level is at most 1 (the shorter line caps
it). So every other pair that uses line 0 holds less than 8 * 1. Line 0 cannot
beat what we just measured, with anyone. It is finished. The taller line, 7,
might still be part of something better with a taller partner, so we cannot
retire it.

| step | lo | hi | h[lo] | h[hi] | width | water | best | move (retire the shorter) |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 8 | 1 | 7 | 8 | 8 | 8 | lo = 1 |
| 2 | 1 | 8 | 8 | 7 | 7 | 49 | 49 | hi = 7 |
| 3 | 1 | 7 | 8 | 3 | 6 | 18 | 49 | hi = 6 |
| 4 | 1 | 6 | 8 | 8 | 5 | 40 | 49 | tie: hi = 5 |
| 5 | 1 | 5 | 8 | 4 | 4 | 16 | 49 | hi = 4 |
| 6 | 1 | 4 | 8 | 5 | 3 | 15 | 49 | hi = 3 |
| 7 | 1 | 3 | 8 | 2 | 2 | 4 | 49 | hi = 2 |
| 8 | 1 | 2 | 8 | 6 | 1 | 6 | 49 | hi = 1, stop |

The answer is 49, lines 1 and 8. This trace shows three things the first did not.

**Sorting is not the requirement.** Elimination is. Here it comes from the
structure of the score (capped by the shorter side, growing with width), not
from order in the array.

**The answer is recorded on the way, not at the end.** In pair sum we stopped on
equality. Here every pair we read is a candidate, so we update best at every
step, and the pointers keep going until they meet.

**Ties are safe either way.** At step 4 both lines have height 8. Every other
pair using line 1 is narrower and capped at 8, so it is worse than 40; the same
is true for line 6. Both are finished, so retiring either one loses nothing.

### You might think: "Move the taller line, it has more potential."

Try it on the same input. At step 1 the taller end is line 8 (height 7), so you
retire it and keep line 0, height 1. Every step after that keeps line 0, because
nothing is shorter than 1, and every pair you read holds at most width * 1. You
finish with 8. The true answer is 49. Retiring the taller line throws away the
one element that could still improve; retiring the shorter one throws away an
element that provably cannot.

### A third trace: reader and writer

[[p:gep-deduplicate-sorted-array-in-place|Deduplicate a Sorted Array In Place]]:
a = [0, 0, 1, 1, 1, 2, 3, 3]. Keep one copy of each value, in place.

Two indices, both moving right. r (reader) visits every position once. w
(writer) is the length of the finished prefix: a[0..w-1] is the answer so far.
Position 0 is always kept, so w starts at 1 and r at 1. A value is kept when it
differs from the last *kept* value, a[w-1]. A `*` marks a cell just written.

| r | a[r] | a[w-1] (last kept) | keep? | array after | w |
|---|---|---|---|---|---|
| start | | | | 0 0 1 1 1 2 3 3 | 1 |
| 1 | 0 | 0 | no | 0 0 1 1 1 2 3 3 | 1 |
| 2 | 1 | 0 | yes, a[1] = 1 | 0 1* 1 1 1 2 3 3 | 2 |
| 3 | 1 | 1 | no | 0 1 1 1 1 2 3 3 | 2 |
| 4 | 1 | 1 | no | 0 1 1 1 1 2 3 3 | 2 |
| 5 | 2 | 1 | yes, a[2] = 2 | 0 1 2* 1 1 2 3 3 | 3 |
| 6 | 3 | 2 | yes, a[3] = 3 | 0 1 2 3* 1 2 3 3 | 4 |
| 7 | 3 | 3 | no | 0 1 2 3 1 2 3 3 | 4 |

The answer is the first w = 4 cells: [0, 1, 2, 3]. The rest is leftover junk,
which the problem allows.

What is retired here? Each element, once the reader has looked at it. Its fate
is decided by one comparison with the last kept value, and nobody reads it again.
And notice the one fact that makes in place safe: **w is never ahead of r.** The
writer only ever writes into a cell the reader has already passed. You will see
in the next section what happens when a rule reads a cell the writer has already
changed.

## From the idea to the code

### The direct version: converging pair sum

The program below writes the double loop and the sweep side by side, counts how
many cells each reads, and checks the sweep against the double loop on hundreds of
random sorted arrays.

```python run
import random

def pair_brute(a, t):
    reads = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            reads += 1
            if a[i] + a[j] == t:
                return (i, j), reads
    return None, reads

def pair_sweep(a, t):
    lo, hi, reads = 0, len(a) - 1, 0     # the two ends of what is undecided
    while lo < hi:                       # a pair needs two different slots
        reads += 1
        s = a[lo] + a[hi]
        if s == t:
            return (lo, hi), reads
        if s < t:
            lo += 1                      # a[lo] fails even with the largest partner
        else:
            hi -= 1                      # a[hi] fails even with the smallest partner
    return None, reads

a = [1, 3, 4, 6, 8, 11]
print("brute:", pair_brute(a, 10), " sweep:", pair_sweep(a, 10))
assert pair_sweep(a, 10) == ((2, 3), 5) and pair_brute(a, 10) == ((2, 3), 10)
print("no pair for 13:", pair_brute(a, 13), pair_sweep(a, 13))
assert pair_sweep(a, 13)[0] is None and pair_brute(a, 13)[1] == 15

big = list(range(0, 200000, 2))          # 100,000 even numbers, target odd
_, reads = pair_sweep(big, 7)
print("n = 100000, no answer: sweep read", reads, "pairs; brute would read",
      len(big) * (len(big) - 1) // 2)
assert reads == len(big) - 1

rng = random.Random(7)
for _ in range(500):
    xs = sorted(rng.randint(-9, 9) for _ in range(rng.randint(0, 9)))
    t = rng.randint(-18, 18)
    got, _ = pair_sweep(xs, t)
    want, _ = pair_brute(xs, t)
    assert (got is None) == (want is None), (xs, t)
    if got:
        assert got[0] < got[1] and xs[got[0]] + xs[got[1]] == t
print("500 random sorted arrays: sweep finds a pair exactly when brute does")
```

On the hand example, 5 reads against 10. With no answer at n = 100,000, the
sweep reads 99,999 pairs and the double loop would read about 5 * 10^9.

### Each line, and which part of the idea it is

| line | in words | which part of the derivation |
|---|---|---|
| `lo, hi = 0, len(a) - 1` | nothing is crossed off yet | the full grid; its corner is (0, n-1) |
| `while lo < hi` | at least two elements are left, so a pair exists | a pair needs two different positions |
| `s = a[lo] + a[hi]` | read the corner cell | the one cell that is extreme in its row and its column |
| `if s == t: return` | the corner is the answer | |
| `if s < t: lo += 1` | a[lo] is too small with its biggest partner | cross off row lo |
| `else: hi -= 1` | a[hi] is too big with its smallest partner | cross off column hi |
| `return None` | everything is crossed off | the grid is empty, so no pair exists |

Settle the small confusions now.

- **lo and hi are not "a window".** The positions between them are "not yet
  ruled out", not "a candidate answer". The answer is always a *pair* (lo, hi),
  never the stretch between them. Reading the region as a window is how converging
  problems get solved with sliding-window code that fails.
- **What the pointers mean.** lo is "the smallest index not yet proved useless",
  hi is "the largest index not yet proved useless". Say it that way and the moves
  write themselves.
- **The equality branch is special.** The two "no" branches are justified by the
  sortedness argument. The "yes" branch is not a comparison, it is a result, and
  if you need *all* pairs or a *count*, it needs its own reasoning. Variation A
  covers that.

### The subtle line: which cell does the rule read?

In the converging loop the subtle line is `lo < hi`, and it gets a demonstration
in the traps. The reader and writer loop has a subtler one, and it is the same
lesson as the loop direction in knapsack: **are you reading a cell before or after
it was overwritten?**

Change the problem slightly: keep *at most two* copies of each value in a sorted
array. a = [1, 1, 1, 2, 2, 3]; the answer is [1, 1, 2, 2, 3].

A value a[r] should be kept if it is not the third copy of something. Two rules
look equally reasonable:

- **Rule W:** keep a[r] if it differs from a[w-2], the value *two places back in
  the output*.
- **Rule R:** keep a[r] if it differs from a[r-2], the value *two places back in
  the input*.

On a fresh copy of the input, rule R is correct: in a sorted array, a[r] equals
a[r-2] exactly when a[r] is the third (or later) copy. But we are writing in
place, and the cell a[r-2] may already have been overwritten by the writer. Watch.
Both start with w = 2 (the first two elements are always kept) and r = 2. `*`
marks a cell written in this step.

```
Rule W (compare with the output)          Rule R (compare with the input, in place)
start      1 1 1 2 2 3   w=2              start      1 1 1 2 2 3   w=2
r=2: 1 vs a[0]=1  skip                    r=2: 1 vs a[0]=1  skip
r=3: 2 vs a[1]=1  write a[2]=2            r=3: 2 vs a[1]=1  write a[2]=2
           1 1 2* 2 2 3  w=3                         1 1 2* 2 2 3  w=3
r=4: 2 vs a[1]=1  write a[3]=2            r=4: 2 vs a[2]=2  skip    <-- a[2] was 1, now 2
           1 1 2 2* 2 3  w=4                         1 1 2 2 2 3   w=3
r=5: 3 vs a[2]=2  write a[4]=3            r=5: 3 vs a[3]=2  write a[3]=3
           1 1 2 2 3* 3  w=5                         1 1 2 3* 2 3  w=4
result  [1, 1, 2, 2, 3]                   result  [1, 1, 2, 3]   one 2 lost
```

Point at the exact cell: at r = 4, rule R reads a[2] and expects the input value
1. But at r = 3 the writer put a 2 there. Rule R sees "2 vs 2, the third copy",
and skips the second 2, which was a real copy.

Why does it happen? The writer is behind the reader. The gap between them is
the number of elements dropped so far. Once one element has been dropped, cell
r - 2 is no longer an input cell the writer has not touched; it may be an output
cell. Rule R reads a cell whose meaning changed under it.

Rule W reads the output on purpose. "The last two values I kept" is exactly the
question, and a[w-2] always holds the answer, because the output prefix is never
rewritten once written.

And why did the "keep one copy" version, comparing with a[r-1], never show this
problem? Because cell r-1 can only be written while the reader is at r-1, and
then the writer writes into it only when w = r - 1, which is a copy of a value
onto itself. So a[r-1] is never changed before the reader arrives at r. It is
safe by luck, and the luck runs out at k = 2. Write the rule against the output,
a[w-k], and it is safe for every k.

The program runs both rules, printing the array after each step, and checks both
against a version that builds a fresh list.

```python run
import random

def keep_at_most(a, k, rule, show=False):
    a = list(a)
    w = min(k, len(a))                    # the first k are always kept
    for r in range(k, len(a)):
        ref = a[w - k] if rule == "W" else a[r - k]
        val = a[r]
        kept = val != ref
        if kept:
            a[w] = val
            w += 1
        if show:
            print("   r=%d  compare %d with %d  %-5s  %s  w=%d"
                  % (r, val, ref, "write" if kept else "skip", a, w))
    return a[:w]

def fresh(a, k):                          # the truth: build a new list
    out = []
    for x in a:
        if out[-k:].count(x) < k:
            out.append(x)
    return out

a = [1, 1, 1, 2, 2, 3]
print("rule W (a[w-2]):"); w_ans = keep_at_most(a, 2, "W", show=True)
print("rule R (a[r-2]):"); r_ans = keep_at_most(a, 2, "R", show=True)
print("W ->", w_ans, "  R ->", r_ans, "  truth ->", fresh(a, 2))
assert w_ans == fresh(a, 2) == [1, 1, 2, 2, 3]
assert r_ans == [1, 1, 2, 3]

rng = random.Random(3)
r_wrong = 0
for _ in range(400):
    xs = sorted(rng.randint(0, 4) for _ in range(rng.randint(0, 10)))
    for k in (1, 2, 3):
        assert keep_at_most(xs, k, "W") == fresh(xs, k)
        if k == 1:
            assert keep_at_most(xs, 1, "R") == fresh(xs, 1)   # safe by luck
        elif keep_at_most(xs, k, "R") != fresh(xs, k):
            r_wrong += 1
print("rule W always right; rule R right for k=1, wrong on", r_wrong, "cases for k=2,3")
assert r_wrong > 0
```

### The other shapes as code

Every shape is the same skeleton with a different "what is finished" rule. Merge
is worth writing out because of one detail: in
[[p:atlassian-merge-sorted-array|Merge Sorted Array]] the result must go into the
first array, which has empty slots at the end. Merge from the front and the first
write lands on a value of the first array that has not been read yet. Merge from
the *back* instead: the largest remaining value goes into the last free slot, and
the write position is always at or after both read positions, so nothing unread
is ever overwritten. It is the same "is the writer behind the reader" question as
above, answered by choosing the direction.

```python run
import random

def merge_into(nums1, m, nums2, n):
    i, j, w = m - 1, n - 1, m + n - 1     # read ends of both, write end
    while j >= 0:                         # once nums2 is used up, nums1 is in place
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[w] = nums1[i]; i -= 1   # the larger front is finished
        else:
            nums1[w] = nums2[j]; j -= 1
        w -= 1
    return nums1

def max_area(h):
    lo, hi, best = 0, len(h) - 1, 0
    while lo < hi:
        best = max(best, (hi - lo) * min(h[lo], h[hi]))
        if h[lo] < h[hi]:
            lo += 1                       # the shorter line cannot do better
        else:
            hi -= 1
    return best

def valid_palindrome_ii(s):               # delete at most one character
    def is_pal(lo, hi):
        while lo < hi:
            if s[lo] != s[hi]:
                return False
            lo += 1; hi -= 1
        return True
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if s[lo] != s[hi]:                # one of these two must be deleted
            return is_pal(lo + 1, hi) or is_pal(lo, hi - 1)
        lo += 1; hi -= 1                  # matching ends are settled
    return True

print(merge_into([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3))
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))
print(valid_palindrome_ii("abca"), valid_palindrome_ii("abc"))
assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
assert valid_palindrome_ii("abca") and not valid_palindrome_ii("abc")
rng = random.Random(5)
for _ in range(400):
    x = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
    y = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
    if x or y:
        assert merge_into(x + [0] * len(y), len(x), y, len(y)) == sorted(x + y)
    h = [rng.randint(0, 9) for _ in range(rng.randint(2, 9))]
    assert max_area(h) == max((j - i) * min(h[i], h[j])
                              for i in range(len(h)) for j in range(i + 1, len(h)))
    s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 7)))
    brute = any((s[:i] + s[i + 1:]) == (s[:i] + s[i + 1:])[::-1]
                for i in range(len(s))) or s == s[::-1]
    assert valid_palindrome_ii(s) == brute, s
print("merge, container and palindrome-II agree with brute force on 400 cases each")
```

Three lines in that block carry the ideas.

- `while j >= 0` in the merge. When nums2 runs out, whatever is left of nums1 is
  already in its final place, so the loop can stop. When nums1 runs out first, the
  `i >= 0` guard sends every remaining nums2 value to the front. Forgetting one of
  these is the "dropped tail" bug.
- `if h[lo] < h[hi]: lo += 1` in the container. That is the proof from the second
  trace, in one line.
- `return is_pal(lo + 1, hi) or is_pal(lo, hi - 1)` in Valid Palindrome II. At the
  first mismatch, one of the two characters must be deleted, and you do not know
  which, so you try both. Each try is a plain palindrome check of the middle, so
  the whole thing is at most three linear scans, not n of them. Everything before
  the mismatch is already matched and never needs to be looked at again.

## Why it is correct

The trace makes the sweep look obvious. A proof is worth writing anyway, because
"obvious" is exactly where the duplicate and empty-range bugs hide, and because
the proof's list of assumptions tells you which problems the sweep is allowed on.

:::proof The converging sweep finds a pair exactly when one exists
**What we want to show.** a[0..n-1] is sorted, smallest first. A pair (i, j) is
*good* when i < j and a[i] + a[j] = t. The sweep returns a good pair if one
exists, and returns "none" if none exists.

**The promise the loop keeps (the invariant).** At the top of every pass of the
loop: every good pair (i, j) of the whole array has lo <= i and j <= hi. In words:
nothing we crossed off was part of an answer.

**It is true at the start.** lo = 0 and hi = n-1, so every pair in the array has
lo <= i and j <= hi. Nothing has been crossed off.

**Each pass keeps it true.** Suppose the promise holds and lo < hi. Let
s = a[lo] + a[hi].

- If s = t, we return (lo, hi). It is good: lo < hi, and the sum is t.
- If s < t, we are about to cross off every pair whose first index is lo. Take any
  such pair still inside the range, (lo, j) with lo < j <= hi. The array is
  sorted, so a[j] <= a[hi], so a[lo] + a[j] <= a[lo] + a[hi] = s < t. Not good. So
  no good pair has first index lo, and moving lo to lo + 1 keeps the promise.
- If s > t, the mirror argument. Any pair (i, hi) with lo <= i < hi has
  a[i] >= a[lo], so a[i] + a[hi] >= s > t. Not good. Moving hi to hi - 1 keeps
  the promise.

**It stops.** The number hi - lo starts at n - 1, is never negative while the loop
runs, and goes down by exactly 1 on every pass that does not return. A
non-negative whole number cannot go down forever, so after at most n - 1 passes
the loop either returns or finds lo = hi.

**Why the answer is right when it stops.** If it returned, the pair is good. If
it stopped with lo = hi, the promise says every good pair has lo <= i < j <= hi =
lo, which is impossible, because there is no i < j between lo and lo. So no good
pair exists, and "none" is correct.
:::

The proof used five things. Each one is a place where a bug or a wrong problem
can sneak in.

1. **Sortedness, twice.** Once for a[j] <= a[hi] and once for a[i] >= a[lo]. On an
   unsorted array both eliminations are false, and the code still runs and still
   returns something.
2. **The combining operation grows with each argument.** The step
   a[lo] + a[j] <= a[lo] + a[hi] needs "bigger input, bigger output" in each
   argument. Addition has that. Multiplication with negative numbers does not.
   XOR does not. Swap + for one of those and the proof collapses even on sorted
   data.
3. **i < j, strictly.** The grid is a triangle. The loop condition lo < hi is what
   keeps the sweep inside it.
4. **A move crosses off a whole row or column.** A rule that retires an element
   because it "looks unpromising", without a proof that *every* remaining pair
   with it is bad, breaks the promise.
5. **The "yes" branch is not covered.** The argument justifies the two "no" moves.
   If you continue after a match, to count or to list, what you do on a match
   needs its own argument (Variation A).

:::note The same proof, other rules
Container With Most Water: if h[lo] < h[hi], then for any lo < j < hi,
area(lo, j) = (j - lo) * min(h[lo], h[j]) <= (j - lo) * h[lo] < (hi - lo) * h[lo]
= area(lo, hi). Every remaining pair with lo is worse than one we already recorded,
so retiring lo keeps the promise "the best pair is either recorded or still inside
the range". Reader and writer: the promise is "a[0..w-1] is exactly the kept
values among a[0..r-1], in order, and w <= r". Each step reads a[r] once, writes at
most once at w <= r, and so keeps both halves. Merge: the promise is "the output
holds the smallest values of both inputs, in order", and the smaller of two
fronts is the smallest value left anywhere, because each input is sorted.
:::

## What it costs

**Converging.** Use the number hi - lo. It starts at n - 1, never goes below 0,
and each pass of the loop lowers it by exactly 1. So there are at most n - 1
passes, each doing a constant amount of work: **O(n) time, O(1) extra space.**
Against the double loop's n(n-1)/2, at n = 10^5 that is 10^5 reads against
5 * 10^9.

**Reader and writer.** It looks like it could be worse, because many versions have
an inner loop:

```python
for r in range(n):
    while w < r and not ok(w, r):
        w += 1
```

That looks quadratic. It is linear, and the reason is a sum, not a per-pass bound.
w starts at 0, only goes up, and never passes n, so across the *whole* run the
inner body executes at most n times. Total work is (moves of r) + (moves of w),
at most 2n. You cannot bound one pass, but you can bound the total, because each
pointer move is paid for once and never undone. This is the same counting
argument as [[amortized-analysis]], and the next chapter, [[sliding-window]],
uses it on every page.

**Two sequences.** Each pass hands one element of one input to the output and never
takes it back, so there are at most n + m passes: **O(n + m)**.

**3Sum.** The outer index runs n - 2 times; for outer index i, the inner sweep
does at most n - i - 2 reads. The total is about n^2 / 2: **O(n^2)**. The sort
first is O(n log n), which is smaller, so it disappears into the n^2.

**The costs people forget.**

- **The sort.** If the input is not sorted, the sweep is the cheap part and the
  sort is O(n log n). On an unsorted "is there a pair" problem the hash set is
  O(n) and beats sort-then-sweep. Two pointers wins when the data is already
  sorted, when you need O(1) memory, or when the question is not an exact match.
- **The per-step work.** Valid Palindrome After Normalization skips characters
  that are not letters or digits. The skip loops are pointer moves, each character
  is skipped at most once, and the total stays linear. If a single step itself
  scans, the product comes back.
- **Building the output.** In Python, `out += s[i]` on a string in a loop copies the
  string every time, which is O(n^2). Append to a list and join once.
- **The output size.** 3Sum can have on the order of n^2 distinct triplets on
  adversarial input. The time bound already allows for it, but the memory does not come free.

## How to think about it

The template is short. The skill is seeing which element a comparison retires,
and proving it. Ask these questions, in order, on every new problem.

1. **What is the object?** A pair of positions in one array (converging), a
   position in each of two arrays (two sequences), a read slot and a write slot
   (reader and writer), or a pair of mirror positions (palindrome)?
2. **Is there an order I can lean on?** Already sorted, sortable without losing
   what the answer needs, or a score with built-in structure (capped by the
   shorter side)?
3. **The unlocking question: when I look at one pair, which element is finished,
   and can I prove it?** Write the proof in one line before writing code: "a[lo]
   + a[hi] < t and a[hi] is the largest partner left, so a[lo] is finished".
4. **What does each pointer mean, as a claim?** Not "left" and "right": "lo is the
   smallest index not yet proved useless"; "a[0..w-1] is the finished output".
5. **Find one, find the best, count, or list all distinct?** Find one: return on a
   match. Best: record at every read. Count: on a match, or on every "yes", count a
   whole block at once. List distinct: skip equal values after a match.
6. **Can the two pointers point at the same element?** If a pair needs two
   different elements, the loop is `lo < hi`.
7. **Am I writing in place?** Then the writer must never get ahead of unread data,
   and the rule must read the output, not a cell that may have been overwritten.
   If the free space is at the end, write from the end.
8. **Is the input really unsorted with positions required?** Then stop: hash map.

Before writing code, say three sentences: what each pointer means, which element
each comparison retires and why, and what happens on a match. If you cannot, the
code will not find them for you.

### Telling it from its neighbours

- **Hash map** ([[hash-tables]]). Exact pair sum on unsorted data, with original
  indices: O(n) time, O(n) space, no sort. Two pointers cannot do this without
  sorting (value, index) pairs.
- **Sliding window** ([[sliding-window]]). Both indices move right, and the answer
  is the stretch *between* them. The left index moves to restore a property of
  that stretch, not to retire a partner. Same variable names, different idea.
- **Binary search** ([[binary-search]]). For each a[lo], you could binary search for
  t - a[lo]: O(n log n). Two pointers is the same search done once for all lo at
  the same time, using the fact that the partner of a bigger lo is never to the
  right of the partner of a smaller one.
- **Fast and slow pointers** ([[fast-slow-pointers]]). Two pointers on a linked
  structure moving at different speeds, for cycles and midpoints.
- **Greedy** ([[greedy]]). Many "pair up the extremes" greedy problems, such as
  matching the largest with the smallest, are written as two pointers. The pointer
  moves are the greedy choices, and their proof is an exchange argument.

## Variations

Six techniques, then the rarer relatives. Each says what changes, why, a small
example you can check, and a problem from this bank that teaches it.

### A. Converging pointers on a sorted array (pair sum)

**What changes.** Only what you do with the corner cell.

- *Exact pair*: return on equality. [[p:london-stock-exchange-two-sum-sorted|Two Sum in a Sorted Array]]
  asks for 1-based positions, so add one to each index at the end.
- *Closest to t*: keep the best |s - t| seen; move as usual. If s = t, stop, nothing
  is closer.
- *Largest sum at most C*: if s <= C, record s and move lo up (a bigger a[lo]
  might still fit); else move hi down. 
- *Count pairs with sum at most C*: if a[lo] + a[hi] <= C, then a[lo] fits with
  *every* index from lo+1 to hi, because those partners are no bigger than a[hi].
  Add hi - lo in one step and move lo. Otherwise move hi.
- *Count pairs with sum exactly t*, with duplicates: on a match with a[lo] =
  a[hi], every pair in the range matches, add m(m-1)/2 for m = hi - lo + 1 and
  stop. Otherwise count the run of equal values at each end, p and q, add p * q,
  and jump past both runs.

**Why.** The two "no" moves are always the same proof. The only new reasoning is
what a "yes" lets you conclude about more than one pair at once.

**Example.** [1, 2, 3, 4, 5], pairs with sum at most 6: (lo=0, hi=4) 1+5=6 fits,
add 4 (1 with 2, 3, 4, 5); (1, 4) 2+5=7 no, hi=3; (1, 3) 2+4=6 fits, add 2 (2 with
3, 4); (2, 3) 3+4=7, hi=2; stop. Total 6.

**Two lists.** [[p:amazon-optimal-utilization|Optimal Utilization]] is pair sum at
most a capacity with one element from each of two lists. Sort the foreground apps
by memory going up and the background apps going down; then a background app that
overflows with the current foreground app overflows with every larger one, so it
is finished. The extra work is collecting *all* pairs that tie for the best sum,
which is the "count with duplicates" reasoning again.

### B. Fix one element, two-pointer the rest (3Sum)

**What changes.** An outer loop over the first element i, then a converging sweep
on i+1..n-1 for target -a[i]. To list each triplet once, skip equal values: skip
an i whose value equals the previous i's, and after a match move both pointers and
skip lo past values equal to the one just used.

**Why.** Fixing one element turns three free choices into one free choice plus a
sorted pair problem. Skipping equal values works because the array is sorted, so
equal values sit next to each other, and a triplet is identified by its values,
not its positions.

**Example.** [-1, 0, 1, 2, -1, -4] sorted is [-4, -1, -1, 0, 1, 2]. i=0 (-4): no
pair sums to 4. i=1 (-1): pairs summing to 1 in [-1, 0, 1, 2] are (-1, 2) and
(0, 1). i=2 (-1): same value as i=1, skip. Result [[-1, -1, 2], [-1, 0, 1]].

**Bank.** [[p:att-three-sum|3Sum]] is the plain version.
[[p:amazon-three-sum-closest|Three Sum Closest]] keeps the best distance instead of
listing; its tie rule picks the smaller sum, so compare (distance, sum) as a pair.
[[p:ibm-increasing-value-triplets-under-threshold|Increasing-Value Triplets Under a Threshold]]
counts triplets with sum at most t: once d[i] + d[lo] + d[hi] <= t, every hi'
between lo+1 and hi also fits, so add hi - lo and move lo. That turns an O(n^3)
count into O(n^2) with n up to 10^4. 4Sum is two fixed elements and one sweep,
O(n^3).

### C. Reader and writer (compact in place)

**What changes.** Both pointers move right. The reader r visits everything; the
writer w is the length of the kept prefix. Keep a[r] by writing it to a[w] and
moving w.

**Why.** The output is never longer than what has been read, so w <= r, and the
writer only overwrites cells the reader has finished with. The rule must read the
*output* (a[w-1], a[w-k]), as the subtle-line demonstration showed.

**Example.** Move all zeros to the end, keeping the order of the rest:
[0, 1, 0, 3, 12]. Write each non-zero to a[w]: [1, 3, 12], w = 3; then fill the
tail with zeros: [1, 3, 12, 0, 0]. If you *swap* a[w] and a[r] instead of copying,
the zeros travel to the back in the same single pass.

**Bank.** [[p:gep-deduplicate-sorted-array-in-place|Deduplicate a Sorted Array In Place]]
is the template. [[p:bloomberg-move-zeroes|Move Zeroes]] is the swap form.
[[p:bloomberg-sort-colors|Sort Colors]] uses three pointers: low (end of the 0s),
mid (the reader) and high (start of the 2s). A 0 at mid is swapped to low and both
advance; a 2 is swapped to high and only high moves, because the value that came
back from high has not been read yet. That last detail is the reader and writer
question again: never move past a cell you have not read.

### D. Walk two sequences together (merge)

**What changes.** One pointer per input. Compare the two fronts, hand the winner to
the output, advance its pointer. Flush whatever is left at the end.

**Why.** Each input is sorted, so its front is its smallest remaining value. The
smaller of the two fronts is the smallest value left anywhere, so it is finished:
it is the next output.

**Example.** [1, 4, 4, 9] and [2, 4, 10]: 1, 2, 4, 4, 4, 9, then the tail 10.

**Bank.** [[p:atlassian-merge-sorted-array|Merge Sorted Array]] is the merge, done
from the back. [[p:goldman-sachs-squares-of-a-sorted-array|Squares of a Sorted Array]]
is a disguised merge: in [-4, -1, 0, 3, 10] the squares of the negative part
decrease and the squares of the rest increase, so the largest square is always at
one of the two *ends*. Compare the ends, write the larger square at the back of the
output, move that end inward: O(n), no sort. [[p:amazon-get-max-pairs|Get Maximum Pairs]]
is two sorted arrays walked together as a greedy: frontend values must beat
backend values, so walk both sorted lists, and when the current frontend beats the
current backend pair them and advance both, else that frontend is too weak for
every remaining backend and is retired. Interval intersection and "is s a
subsequence of t" are the same walk with different rules for which pointer
advances ([[intervals]], [[merge-sort]], [[k-way-merge]] for more than two).

### E. Move the side that cannot improve (container)

**What changes.** The score is not a sum, but it still has a "weaker side" that
caps it. Retire the weaker side; record the score at every step.

**Why.** The second trace's argument: the weaker end with any closer partner is
narrower and no taller, so it cannot beat what was just measured.

**Example.** [[p:amazon-container-with-most-water|Container With Most Water]] on
[1, 8, 6, 2, 5, 4, 8, 3, 7] gives 49, as traced.

**Trapping Rain Water.** [[p:zolostays-trapping-rain-water|Trapping Rain Water]] is
the stretch rung. The water above position i is min(tallest bar to its left,
tallest bar to its right) - h[i]. That seems to need both maxima at every
position. Keep lmax (tallest bar the left pointer has passed, including h[lo])
and rmax (the same from the right). Move the side whose bar is lower. lmax only
ever grows while the left side is the lower one, so every value lmax has taken was
below some bar at or to the right of hi. That means the right cap of position lo is
at least lmax, so the smaller of the two caps is lmax, and the water at lo is
lmax - h[lo]: known now, without looking further. Settle lo and move it. When the
right side is lower, settle hi the same way. On [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1] the
total is 6. The only thing that changes from the container is *what* is settled:
here it is the water above one position, not a pair.

### F. Compare from both ends (palindromes)

**What changes.** The two pointers are mirror positions. If the characters match,
both are settled; move both inward. If they do not, the problem says what happens.

**Why.** A string is a palindrome exactly when every mirror pair matches, and each
mirror pair is checked once.

**Bank.** [[p:amazon-valid-palindrome|Valid Palindrome After Normalization]] lets
each pointer skip characters that are not letters or digits on its own, then
compares in lowercase: the pointers move independently, each by its own rule.
[[p:bloomberg-valid-palindrome-ii|Valid Palindrome II]] allows one deletion: at the
first mismatch try both deletions, as in the code above.
[[p:citadel-minimum-changes-palindromic-blocks|Minimum Changes for Palindromic Blocks]]
runs the mirror walk inside every block of length k and counts mismatched mirror
pairs, because each mismatched pair costs exactly one change (set one character to
the other) and matched pairs cost nothing. "abcaabba" with k = 4: block "abca" has
mirror pairs (a, a) and (b, c), so 1 change; "abba" needs 0. Total 1. For more
palindrome machinery see [[palindromes]].

### G. The rarer relatives

- **Closest pair across two sorted arrays.** One pointer in each; move the one
  pointing at the smaller value, because it cannot get closer to anything larger
  in the other list by staying.
- **Meet in the middle** ([[meet-in-the-middle]]). Enumerate subset sums of each
  half, sort both lists, and combine them with a converging sweep. The sweep is
  this chapter; the rest is that one.
- **k-sum in general.** Fix k - 2 elements, sweep the last two: O(n^(k-1)).
  Interviews stop at 4.
- **Partition around a pivot** (the core of quicksort and quickselect): two
  pointers from the ends swap misplaced elements. The same "never move past an
  unread cell" discipline as Sort Colors.

## Recognising it in a statement

Signals, most reliable first.

1. **"sorted" together with "pair", "two numbers", "triplet", "closest to",
   "at most".** Converging sweep, straight off the template. If the array is not
   sorted and the answer does not depend on positions, sorting first is allowed
   and usually intended.
2. **"in place", "O(1) extra space", "return the new length", "the first k
   elements are checked".** Reader and writer.
3. **Two sorted inputs and an output that is their merge, intersection, or a
   matching between them.** One pointer per input.
4. **"palindrome", "reads the same backwards".** Mirror pointers.
5. **"Choose two lines / two positions to maximise something capped by the weaker
   one, and growing with the distance".** Retire the weaker side.
6. **n up to 10^5 or 2 * 10^5 and an obvious algorithm over all pairs.** The
   constraint is asking for O(n) or O(n log n); if there is an order to exploit,
   the sweep is often the missing piece.

**Disguised forms.**

- **Squares of a sorted array** is a merge of two sorted sequences hiding in one
  array: the negative half (read backwards) and the non-negative half.
- **Pairing people into boats of capacity C, at most two per boat** is converging
  pointers: the heaviest person either shares with the lightest or goes alone,
  because if the lightest cannot fit with them, nobody can.
- **"Number of pairs (i, j) with a[i] + a[j] <= C" on unsorted data**: the answer
  does not depend on positions, so sort and count with hi - lo.
- **Get Maximum Pairs** reads like a matching problem; after sorting it is a merge
  walk.

**Anti-signals.**

- **"Return the indices" on unsorted input.** Hash map.
- **"Subarray" or "substring" with a condition on its contents** ("at most k
  distinct", "no repeats"). That is the window between two pointers, so
  [[sliding-window]].
- **"Sum of a subarray equals k" with negatives.** [[prefix-sums]] with a hash map.
- **The k-th smallest pair sum, or the top k pairs.** One extreme is not a ranking:
  that is a [[heap]] or a binary search on the answer.
- **A score that is not monotone in the moved pointer.** If moving lo can make a
  retired partner good again, there is nothing to stand on.

## Traps

**`while lo <= hi` in a converging loop.** Symptom: an element pairs with itself.
[1, 3, 4, 6] with target 8 reports (2, 2), using the single 4 twice.

**Moving only one pointer after a match while listing.** Symptom: the same
triplet appears several times, or the loop never ends on an all-equal range.

**Skipping duplicate indices instead of duplicate values.** Symptom: [-2, 0, 0, 2, 2]
yields (-2, 0, 2) twice even though both pointers moved. Walk past every equal
neighbour, at the outer index and at lo.

**Counting matches one pair at a time with duplicates.** Symptom: [1, 1, 1, 4, 4]
with target 5 counts 2 instead of 6, because moving both pointers after each match
skips the cross pairs. Count runs (p * q), as in Variation A.

**Sorting when the order or the positions are the answer.** Symptom: right values,
wrong indices; or a "keep the relative order" rule quietly broken.

**A compaction rule that reads an overwritten cell.** Symptom: correct for "keep
one copy", wrong for "keep two". Compare with the output, a[w-k].

**Merging from the front into the array that holds the answer.** Symptom: some
values duplicated and others lost, on inputs where the first array's values are
large. Merge from the back.

**Dropping the tail of a merge.** Symptom: output too short, only when one input
ends early. Flush both remainders, or loop until the second input is used up.

**Moving the wrong side in a dominance sweep.** Symptom: Container With Most
Water returns a small number because the short line is kept forever. Retire the
shorter line.

The program below demonstrates the first three traps next to their fixes.

```python run
def pair_loose(a, t):                     # WRONG: <= lets an element pair with itself
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        s = a[lo] + a[hi]
        if s == t:
            return (lo, hi)
        lo, hi = (lo + 1, hi) if s < t else (lo, hi - 1)
    return None

def pair_strict(a, t):                    # RIGHT
    lo, hi = 0, len(a) - 1
    while lo < hi:
        s = a[lo] + a[hi]
        if s == t:
            return (lo, hi)
        lo, hi = (lo + 1, hi) if s < t else (lo, hi - 1)
    return None

def three_sum(a, skip):
    a, out = sorted(a), []
    for i in range(len(a) - 2):
        if skip and i and a[i] == a[i - 1]:
            continue                      # same first value: same triplets again
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                out.append((a[i], a[lo], a[hi]))
                lo += 1; hi -= 1
                while skip and lo < hi and a[lo] == a[lo - 1]:
                    lo += 1               # same second value: same triplet again
    return out

def count_pairs(a, t, by_runs):
    lo, hi, total = 0, len(a) - 1, 0
    while lo < hi:
        s = a[lo] + a[hi]
        if s < t: lo += 1
        elif s > t: hi -= 1
        elif not by_runs:
            total += 1; lo += 1; hi -= 1  # WRONG with duplicates
        elif a[lo] == a[hi]:
            m = hi - lo + 1
            return total + m * (m - 1) // 2
        else:
            p = q = 1
            while a[lo + p] == a[lo]: p += 1
            while a[hi - q] == a[hi]: q += 1
            total += p * q; lo += p; hi -= q
    return total

a = [1, 3, 4, 6]
print("loose  (8):", pair_loose(a, 8), "   strict (8):", pair_strict(a, 8))
assert pair_loose(a, 8) == (2, 2) and pair_strict(a, 8) is None
nums = [-2, 0, 0, 2, 2, -2, 1, 1]
print("3Sum without skipping:", three_sum(nums, False))
print("3Sum with skipping   :", three_sum(nums, True))
assert len(three_sum(nums, True)) == len(set(three_sum(nums, False))) == 2
assert len(three_sum(nums, False)) == 6
d = [1, 1, 1, 4, 4]
truth = sum(d[i] + d[j] == 5 for i in range(5) for j in range(i + 1, 5))
print("pairs summing to 5 in", d, ": one at a time", count_pairs(d, 5, False),
      " by runs", count_pairs(d, 5, True), " truth", truth)
assert count_pairs(d, 5, False) == 2 and count_pairs(d, 5, True) == truth == 6
assert count_pairs([2, 2, 2, 2], 4, True) == 6
```

## What to memorise

Two skeletons, one question, one habit.

```python
lo, hi = 0, len(a) - 1           # converging
while lo < hi:
    if <a[lo] is proved useless with every partner left>:
        lo += 1
    else:                         # a[hi] is proved useless
        hi -= 1

w = 0                             # reader and writer
for r in range(len(a)):
    if keep(a[r], a[:w]):         # decide by the OUTPUT, never by an old input cell
        a[w] = a[r]
        w += 1                    # a[0..w-1] is the finished answer
```

**The sentence** that turns a problem into the first skeleton: "when I compare
these two, one of them is finished for every partner it has left". If you cannot
finish that sentence with a proof, you do not have a two pointer problem.

**The habit**: before running the loop, say what each pointer means as a claim.
"lo is the smallest index not yet proved useless." "a[0..w-1] is the part of the
answer I have committed to." The duplicate case and the in-place case are both
decided by that sentence.

**Numbers worth carrying**: n(n-1)/2 pairs against at most n - 1 reads; at n = 10^5
that is 5 * 10^9 against 10^5. Total pointer movement in any of these loops is at
most 2n. 3Sum is O(n^2), and the sort does not change that.

## Check yourself

:::check
Hand trace. a = [2, 5, 7, 9, 12, 15], target 17. Run the converging sweep. For
every step, write lo, hi, the sum, the move, and the element retired. How many
pairs exist, and how many did you read?
--
| step | lo | hi | a[lo] + a[hi] | verdict | move | retired |
|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 2 + 15 = 17 | equal | stop | |

A trick: the first read is the answer, (0, 5). So change the target to 16 and do
it again:

| step | lo | hi | sum | verdict | move | retired |
|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 2 + 15 = 17 | too big | hi = 4 | 15 |
| 2 | 0 | 4 | 2 + 12 = 14 | too small | lo = 1 | 2 |
| 3 | 1 | 4 | 5 + 12 = 17 | too big | hi = 3 | 12 |
| 4 | 1 | 3 | 5 + 9 = 14 | too small | lo = 2 | 5 |
| 5 | 2 | 3 | 7 + 9 = 16 | equal | stop | |

There are 6 * 5 / 2 = 15 pairs; the sweep read 5. At step 3, the reason 12 is
retired: 5 is the smallest value left, and 12 + 5 is already too big, so 12 + 7
and 12 + 9 are too big as well.
:::

:::check
Hand trace, the subtle line. Keep at most two copies of each value in place:
a = [1, 1, 1, 2, 2, 2]. Run rule W (compare with a[w-2]) and rule R (compare with
a[r-2]), writing the array after every write. Where does rule R go wrong? Then run
rule R on [3, 3, 3, 3, 5, 5, 5, 7] and explain why it gets lucky.
--
Both start with w = 2, r = 2.

Rule W: r=2: 1 vs a[0]=1, skip. r=3: 2 vs a[0]=1, write a[2]=2, array
1 1 2* 2 2 2, w=3. r=4: 2 vs a[1]=1, write a[3]=2, array 1 1 2 2* 2 2, w=4. r=5:
2 vs a[2]=2, skip (third 2). Result [1, 1, 2, 2], correct.

Rule R: r=2: 1 vs a[0]=1, skip. r=3: 2 vs a[1]=1, write a[2]=2, array
1 1 2* 2 2 2, w=3. r=4: 2 vs a[2], which *was* 1 and is now 2: skip. r=5: 2 vs
a[3]=2, skip. Result [1, 1, 2], one 2 short. The wrong read is a[2] at r = 4: the
writer changed it one step earlier.

On [3, 3, 3, 3, 5, 5, 5, 7] rule R returns [3, 3, 5, 5, 7], which is right. Follow
its reads: at r = 4 it reads a[2] and at r = 5 it reads a[3], each one *just
before* the writer overwrites that same cell; at r = 6 and r = 7 it reads a[4] and
a[5], which the writer has not reached. Every cell it read still held its input
value, so it behaved like the rule on a fresh copy. Whether that happens depends
on where the duplicates fall, which is why you argue about which cell is read,
not about examples. A wrong rule can pass a test by luck.
:::

:::check
Hand trace. Container With Most Water on h = [4, 3, 2, 1, 4]. Trace every step and
say what happens on the ties.
--
| step | lo | hi | h[lo], h[hi] | water | best | move |
|---|---|---|---|---|---|---|
| 1 | 0 | 4 | 4, 4 | 4 * 4 = 16 | 16 | tie, hi = 3 |
| 2 | 0 | 3 | 4, 1 | 3 * 1 = 3 | 16 | hi = 2 |
| 3 | 0 | 2 | 4, 2 | 2 * 2 = 4 | 16 | hi = 1 |
| 4 | 0 | 1 | 4, 3 | 1 * 3 = 3 | 16 | hi = 0, stop |

Answer 16. At the tie in step 1, both ends have height 4. Any other pair using
line 0 is narrower than 4 and holds water at most 4 high, so less than 16; the
same holds for line 4. Both are finished, so retiring either is safe. The answer
was found on the very first read, and the rest of the sweep only confirms nothing
beats it.
:::

:::check
Why is it safe, in Container With Most Water, to discard every pair that contains
the shorter end line, when you have measured only one of those pairs?
--
Because the water of any pair is width times the shorter line. Say h[lo] <= h[hi].
For any partner j strictly between them, the width j - lo is smaller than hi - lo,
and the height min(h[lo], h[j]) is at most h[lo]. So the water is less than
(hi - lo) * h[lo], which is exactly what we just measured. Every unmeasured pair
with lo is *bounded* by a pair already recorded. We did not measure them; we
proved they cannot win. That bound is what every converging two-pointer argument
needs, and it is why the taller line cannot be retired: a taller partner might
still raise its water level.
:::

:::check
Someone says: "Two pointers needs a sorted array." Where are they wrong, and what
is the correct statement?
--
They have mistaken the most common source of the property for the property.
The correct statement: **each move must retire an element, and you must be able to
prove that element is useless with every partner it has left.**

Sorting is one way to get that proof. But Container With Most Water and Trapping
Rain Water work on any heights, because the score is capped by the weaker side.
Palindrome checks compare mirror characters of unsorted text. Reader and writer
compaction, such as Move Zeroes, needs no order at all. And the reverse is also
true: a sorted array does not guarantee a two pointer solution. "Is there a pair
whose product is exactly P" with negative numbers allowed is sorted but has no
safe elimination, because a[lo] * a[hi] being too small says nothing reliable about
a[lo] * a[j] when signs can flip.
:::

:::check
Someone counts the pairs with a[i] + a[j] = 5 in a sorted array by running the
converging loop and, on every match, adding 1 and moving both pointers. On
[1, 2, 3, 4] they get 2, which is right. Where does it break, and what is the fix?
--
It breaks on duplicates. [1, 1, 1, 4, 4]: the true count is 3 * 2 = 6. The loop
reads (0, 4) match, count 1; (1, 3) match, count 2; then lo = hi = 2 and it stops.
It never pairs index 0 with index 3, or index 2 with either 4.

The "no" moves were justified by the sortedness proof. The "yes" move was not: on
a match, a[lo] is not useless, it may match again with an equal neighbour of a[hi].
The fix counts whole runs. If a[lo] = a[hi], every pair in the range matches: add
m(m-1)/2 with m = hi - lo + 1 and stop. Otherwise count p copies of a[lo] at the
left and q copies of a[hi] at the right, add p * q, and jump both pointers past
their runs.
:::

:::check
Disguised problem. You are given weights of people and a boat capacity C. Each
boat carries at most two people with total weight at most C. Find the fewest
boats. Reduce it to a two pointer sweep and justify the move. Then trace it on
weights [3, 2, 2, 1] with C = 3.
--
Sort the weights. Put lo at the lightest and hi at the heaviest. The heaviest
person must go in some boat. If the lightest can share with them
(w[lo] + w[hi] <= C), put them together: pairing the heaviest with anyone is at
least as good as leaving them alone, and the lightest is the easiest partner, and
any solution that pairs them differently can be swapped into this one without
using more boats. If even the lightest cannot share with them, nobody can, so the
heaviest is finished: they go alone. Either way hi moves down, one boat is used,
and lo moves up only when it was paired.

Sorted [1, 2, 2, 3], C = 3: (lo=0, hi=3) 1 + 3 = 4 > 3, 3 goes alone, boats 1,
hi = 2. (0, 2) 1 + 2 = 3 fits, boats 2, lo = 1, hi = 1. (1, 1): one person left,
alone, boats 3. Answer 3. The loop here is `while lo <= hi`, and that is not the
trap from earlier: lo = hi is one *person*, not one element paired with itself,
and they still need a boat. The meaning of the pointers decides the condition, not
habit.
:::
