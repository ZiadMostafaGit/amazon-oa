# Interval Problems

> Sorting intervals by the endpoint that fits the question turns a pile of pairs that all might clash with each other into a single walk along a line, where the past shrinks to one number (the end of the current block, the end of the last interval kept, or how many are open right now), and choosing which endpoint to sort by and what to remember is the entire technique.

## The problem it solves

Here are five closed intervals of integers. Each one could be a meeting, a process
that is running, or a range of bytes received:

```
[1, 4]   [6, 9]   [2, 3]   [8, 11]   [13, 15]
```

[[p:micro1-merge-intervals|Merge Intervals]] asks for their union, written as
the fewest disjoint intervals in increasing order. Draw them on a line and the
answer is visible: [1, 4] swallows [2, 3]; [6, 9] and [8, 11] overlap and become
[6, 11]; [13, 15] stands alone. The answer is

```
[1, 4]   [6, 11]   [13, 15]
```

Easy by eye. The question is how to do it for 10^5 intervals with endpoints up to
10^9, which is what the bank's version allows.

The first solution people write marks points. Make an array over the whole line,
set every covered point to 1, and read off the runs of 1s. For the example that is
15 cells. For endpoints up to 10^9 it is a billion cells, and with negative
endpoints down to -10^9 it is two billion. It does not fit.

The second solution compares pairs. Any two intervals that overlap get replaced
by their union; repeat until no two overlap. It is correct, but every round looks
at all pairs, n(n-1)/2 of them, and you may need up to n - 1 rounds. With 10^5
intervals even one round is 5 x 10^9 comparisons.

What this chapter builds is the one-pass method that sorts once and then looks at
each interval exactly once, in O(n log n). It then turns the same idea into the
other interval questions an interview asks: is any pair overlapping, insert one
interval, how many rooms do I need, how many can I keep, where do two schedules
meet. About 380 problems in this bank are interval problems; most of them are one
of those questions with a different noun.

The questions all have the same input, pairs (start, end) on one ordered axis,
and the answer depends on how the pairs sit relative to each other along that
axis. Time is the usual axis, but bytes in
[[p:roblox-track-received-byte-ranges|Track Received Byte Ranges]], positions on a
line of sprinklers, and memory addresses are the same thing.

### When it is the wrong tool

- **The intervals carry weights, and you want the heaviest conflict-free set.**
  [[p:amazon-cinema-shows|Cinema Shows]] asks for the largest total audience among
  screenings that do not overlap. One long screening with a huge audience can beat
  three short ones, so no sort-and-take rule works. That is
  [[dynamic-programming]] with a [[binary-search]] (Variation M).
- **The pairs are not ranges.** If (u, v) means "u is connected to v", there is
  nothing between u and v; that is [[graphs]] or [[union-find]].
- **Many queries against a fixed set.** "Which intervals contain point x?" asked
  10^5 times needs the queries sorted into the same sweep, or a
  [[segment-tree]].
- **The window is yours to choose.** "The longest subarray such that..." is an
  interval too, but you are not given it; that is [[sliding-window]] or
  [[two-pointers]].

## Build it from the brute force

We start with what a beginner writes, count it, find the waste, and remove it. The
sorted one-pass merge will come out at the end as the obvious fix.

### Step 1: when do two intervals overlap?

Everything rests on this test, so derive it rather than guess it. Two closed
intervals a = [a1, a2] and b = [b1, b2] fail to share a point in exactly two ways:
a ends before b starts (a2 < b1), or b ends before a starts (b2 < a1). There is no
third way to be apart. So they overlap exactly when neither happens:

```
overlap(a, b)  =  a1 <= b2  and  b1 <= a2
```

Read it as: each one starts before the other one ends.

### You might think: "they overlap if b's start lies inside a"

That is the test people write first: `a1 <= b1 <= a2`. Try a = [2, 3] and
b = [1, 10]. b's start, 1, is not inside [2, 3], so the test says no overlap. But
[2, 3] is entirely inside [1, 10]. The one-sided test misses the case where b
starts first.

Notice when the one-sided test *is* right: when you already know a1 <= b1, that
is, when a starts first. Then "b starts before a ends" is the whole test. That is
the first hint that sorting by start will make everything simpler: once the
intervals are in order of start, the two-sided test collapses to one comparison.

### Step 2: the brute force, and its cost

```
blocks = the intervals
repeat:
    find any two blocks that overlap
    replace them by [min of starts, max of ends]
until no two blocks overlap
```

Each search for an overlapping pair is up to n(n-1)/2 comparisons. Each merge
reduces the number of blocks by one, so there are at most n - 1 merges. Worst
case about n^3 / 2 comparisons. And even the cheapest possible input is expensive:
60 intervals where nothing overlaps cost 60 x 59 / 2 = 1,770 comparisons just to
learn that nothing needs doing. The runnable block below prints that number.

### Step 3: notice the waste

Most of those comparisons could never succeed. [1, 4] and [13, 15] are nowhere
near each other, and we compared them anyway. What would let us *know* two
intervals cannot meet without comparing them?

Sort by start: [1, 4], [2, 3], [6, 9], [8, 11], [13, 15]. Now walk left to right,
holding the union of what you have seen as a current block. Suppose the block is
[1, 4] and the next interval is [6, 9]. It starts at 6, after the block ends at 4.
Here is the key fact: **every interval after it starts at 6 or later too,
because the list is sorted.** So no interval still to come can reach back and touch
[1, 4]. The block is finished. We never compared [1, 4] with [8, 11] or [13, 15],
and we did not need to.

<svg viewBox="0 0 660 230" role="img" aria-label="a schematic: the current block from cs to ce, a vertical wall at ce, and the next interval in two cases; in the first it starts before the wall and extends the block, in the second it starts after the wall and every later interval also starts after it, so the block is final">
  <g>
    <line x1="30" y1="200" x2="640" y2="200"/>
    <rect class="fill" x="60" y="40" width="220" height="22" rx="4"/>
    <text x="170" y="32" text-anchor="middle">current block [cs, ce]</text>
    <line x1="280" y1="20" x2="280" y2="200"/>
    <text x="280" y="218" text-anchor="middle">ce</text>
    <rect x="200" y="90" width="160" height="18" rx="4"/>
    <text x="370" y="104">case 1: s &lt;= ce, so it joins: ce = max(ce, e)</text>
    <rect x="330" y="140" width="120" height="18" rx="4"/>
    <text x="460" y="154">case 2: s &gt; ce</text>
    <text x="460" y="176">every later start is &gt;= s,</text>
    <text x="460" y="192">so the block is final</text>
  </g>
</svg>

That is the abstract picture. Here it is on the real numbers, sorted:

<svg viewBox="0 0 660 240" role="img" aria-label="the five intervals as bars sorted by start, from 1 to 15; walls at 4 and 11 mark block ends that no later bar crosses; 2 to 3 sits inside 1 to 4, 8 to 11 extends 6 to 9">
  <g>
    <line x1="30" y1="205" x2="640" y2="205"/>
    <text x="30" y="225" text-anchor="middle">1</text>
    <text x="70" y="225" text-anchor="middle">2</text>
    <text x="150" y="225" text-anchor="middle">4</text>
    <text x="230" y="225" text-anchor="middle">6</text>
    <text x="310" y="225" text-anchor="middle">8</text>
    <text x="350" y="225" text-anchor="middle">9</text>
    <text x="430" y="225" text-anchor="middle">11</text>
    <text x="510" y="225" text-anchor="middle">13</text>
    <text x="590" y="225" text-anchor="middle">15</text>
    <rect class="fill" x="30" y="30" width="120" height="18" rx="4"/>
    <text x="160" y="44">[1,4] opens a block, ce = 4</text>
    <rect class="fill" x="70" y="62" width="40" height="18" rx="4"/>
    <text x="160" y="76">[2,3] inside it: ce stays 4</text>
    <rect class="fill" x="230" y="94" width="120" height="18" rx="4"/>
    <text x="360" y="108">[6,9]: 6 &gt; 4, close [1,4]</text>
    <rect class="fill" x="310" y="126" width="120" height="18" rx="4"/>
    <text x="440" y="140">[8,11]: 8 &lt;= 9, ce = 11</text>
    <rect class="fill" x="510" y="158" width="80" height="18" rx="4"/>
    <text x="300" y="172">[13,15]: 13 &gt; 11, close [6,11]</text>
    <line x1="150" y1="20" x2="150" y2="205"/>
    <line x1="430" y1="20" x2="430" y2="205"/>
  </g>
</svg>

The two vertical lines are walls. No bar that starts to the right of a wall ever
crosses back over it, because nothing later starts earlier.

### The question that unlocks it

**Once the intervals are sorted, what is the least I need to remember about the
ones I have already passed?**

For merging, the answer is one number: the end of the current block, ce (plus
its start, cs, only so we can print it). Not how many intervals are in the block,
not which ones, not where they ended individually. The next interval only asks
"do you reach as far as my start?", and only ce can answer that.

This question comes back in every variation, and its answer is always tiny:

| question | sort by | what you remember |
|---|---|---|
| merge, total coverage | start | the end of the current block |
| does any pair overlap | start | the end of the previous interval |
| most intervals with no overlap | end | the end of the last one kept |
| fewest rooms | start (or all endpoints) | the end times of the busy rooms (or just their count) |
| intersect two sorted lists | already sorted | one position in each list |

### You might think: "compare each interval with the previous one"

After sorting, it is tempting to compare each interval with the interval just
before it in the sorted list: "[6, 9] and [8, 11] overlap because 8 <= 9". Try
[1, 10], [2, 3], [4, 5]. [4, 5] against the previous interval [2, 3]: 4 > 3, so it
looks like a gap, and you close a block. But [4, 5] is inside [1, 10]. The previous
*interval* ended at 3; the current *block* ends at 10. You must compare with the
block, and the block's end is the largest end seen so far in it, not the last one.

The same mistake in code is one character: writing `ce = e` instead of
`ce = max(ce, e)` when an interval joins. On [1, 10], [2, 3], the block end would
drop from 10 to 3. The sort orders the starts; it promises nothing about the ends.
A later interval can end earlier.

### You might think: "sort by end, it's the same thing"

It is not, and the reason is the wall. Sorting by end gives [1, 2], [5, 6],
[1, 10] for the input [[5, 6], [1, 2], [1, 10]]. The walk opens [1, 2], then sees
[5, 6] start after 2 and closes [1, 2] as final. Then [1, 10] arrives and starts at
1, far to the *left* of the wall at 2. Sorted by end, a later interval can start
anywhere, so a closed block is not safe. The output would be [1, 2], [5, 10], and
the points 3 and 4, which are covered by [1, 10], are lost.

So: sorting by start is what makes "this block is final" true. That one guarantee
is the whole algorithm.

### You might think: "I can mark points, just with a dictionary"

A set of covered integers works for tiny ranges and dies on [0, 10^9]: one interval
puts a billion keys in the set. The merge never looks at points at all, only at
endpoints, which is why its cost depends on n and not on how long the intervals
are.

### The technique in one sentence

**Sort the intervals by start, carry one block, and for each interval either
extend the block to the larger end (if it starts at or before the block's end) or
close the block for good and open a new one (if it starts after); for every other
interval question, choose the sort key and the one remembered quantity the same
way.** The unlocking question is the bold one: after sorting, what is the least you
must remember about the intervals behind you?

## Worked by hand

### The first trace: the merge

Input [[1, 4], [6, 9], [2, 3], [8, 11], [13, 15]], closed. Sorted by start:
[1, 4], [2, 3], [6, 9], [8, 11], [13, 15]. `out` holds the finished blocks and
(cs, ce) is the block in hand.

| step | interval | block before | s <= ce? | action | block after | out |
|---|---|---|---|---|---|---|
| 1 | [1, 4] | none | | open the first block | (1, 4) | |
| 2 | [2, 3] | (1, 4) | 2 <= 4, yes | ce = max(4, 3) = 4 | (1, 4) | |
| 3 | [6, 9] | (1, 4) | 6 <= 4, no | close (1, 4), open | (6, 9) | [1, 4] |
| 4 | [8, 11] | (6, 9) | 8 <= 9, yes | ce = max(9, 11) = 11 | (6, 11) | [1, 4] |
| 5 | [13, 15] | (6, 11) | 13 <= 11, no | close (6, 11), open | (13, 15) | [1, 4], [6, 11] |
| end | | (13, 15) | | close the last block | | [1, 4], [6, 11], [13, 15] |

Step 4 in words: "The block so far is 6 to 9. The next interval starts at 8. Does
the block reach 8? Yes, it goes to 9. So they overlap, and the block now reaches as
far as the further of the two ends: max(9, 11) = 11. I do not need to remember that
[6, 9] and [8, 11] were two intervals. All the future asks is: how far right does
this block go? 11."

Step 2 in words: "[2, 3] starts at 2, inside the block. It ends at 3, which is
*less* than the block's end, 4. If I wrote ce = 3, the point 4 would fall out of the
block. The max keeps it."

Step 3 in words: "[6, 9] starts at 6, after the block's end at 4. Everything after
it in the list starts at 6 or later. So nothing can ever touch [1, 4] again. Write it
down and forget it."

And the final row: the loop ends with a block in hand that was never closed. That
last close is easy to forget, and it is the reason the code below writes the block
into `out` the moment it is opened rather than at the moment it is closed.

If the question is the total covered time, as in
[[p:ibm-process-execution-time|Process Execution Time]], where a process from 1 to
5 counts 5 units, sum the blocks inclusively: (4 - 1 + 1) + (11 - 6 + 1) +
(15 - 13 + 1) = 4 + 6 + 3 = 13.

### The second trace: the same intervals, seen as endpoints

The merge forgets everything but ce. There is a second way to look at the same
line that forgets even more: forget the intervals entirely and keep only their
endpoints, each tagged +1 where an interval opens and -1 where it closes. Walk the
tags in order with a running total. The total at any point is how many intervals
cover it.

Closed integer intervals need one adjustment first. [1, 4] covers the integers 1,
2, 3 and 4, so it is "open" from 1 up to, but not including, 5. Write it half-open
as [1, 5): +1 at 1, -1 at 5. Do that for all five:

| position | tag | running count | what happened |
|---|---|---|---|
| 1 | +1 | 1 | [1, 4] opens |
| 2 | +1 | 2 | [2, 3] opens: two intervals cover 2 |
| 4 | -1 | 1 | [2, 3] closed after 3 |
| 5 | -1 | 0 | [1, 4] closed after 4: the first block ends |
| 6 | +1 | 1 | [6, 9] opens |
| 8 | +1 | 2 | [8, 11] opens |
| 10 | -1 | 1 | [6, 9] closed after 9 |
| 12 | -1 | 0 | [8, 11] closed after 11: the second block ends |
| 13 | +1 | 1 | [13, 15] opens |
| 16 | -1 | 0 | the third block ends |

This table shows two things the first did not.

**The count returns to 0 exactly at the gaps between blocks.** It hits 0 after 4
and after 11, and the blocks are [1, 4], [6, 11], [13, 15]. So the merge is "the
stretches where the count is positive". The sweep and the merge are two views of
one walk.

**The largest count is the number of rooms.** The count peaks at 2. If the five
intervals were meetings, two rooms would be enough, and two would be needed: at
point 2, two meetings are both running. That is the claim behind
[[p:amazon-meeting-rooms-ii|Meeting Rooms II]], proved in Why it is correct.

Look at row 4 to see why the -1 goes at e + 1 and not at e. If [2, 3] closed at 3
instead of 4, the count at 3 would be 1, as if only one meeting were running at
minute 3. But [1, 4] and [2, 3] are both running during minute 3. Almost every wrong
answer in this family comes from one sentence: **decide whether an interval owns
its end point, and put the -1 just after the last point it owns.**

## From the idea to the code

### The brute force and the one-pass merge, side by side

```python run
import random


def overlap(a, b):
    """Closed intervals share a point unless one ends before the other starts."""
    return a[0] <= b[1] and b[0] <= a[1]


def merge_brute(intervals):
    """Keep merging any overlapping pair until no pair overlaps."""
    blocks = [list(iv) for iv in intervals]
    pairs_checked = 0
    changed = True
    while changed:
        changed = False
        for i in range(len(blocks)):
            for j in range(i + 1, len(blocks)):
                pairs_checked += 1
                if overlap(blocks[i], blocks[j]):
                    a, b = blocks[i], blocks.pop(j)
                    blocks[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    changed = True
                    break
            if changed:
                break
    return sorted(blocks), pairs_checked


def merge(intervals):
    """Sort by start; remember only the block being built."""
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:            # starts inside the current block
            out[-1][1] = max(out[-1][1], e)    # extend it; never shrink it
        else:
            out.append([s, e])                 # a gap: the old block is final
    return out


demo = [[1, 4], [6, 9], [2, 3], [8, 11], [13, 15]]
blocks, work = merge_brute(demo)
print("brute :", blocks, "after", work, "pair checks")
print("sorted:", merge(demo), "after", len(demo), "steps (plus the sort)")
assert blocks == merge(demo) == [[1, 4], [6, 11], [13, 15]]


def points(iv):                                # the slowest truth: mark every point
    return {x for s, e in iv for x in range(s, e + 1)}


rng = random.Random(4)
for _ in range(1000):
    iv = [[s, s + rng.randint(0, 5)] for s in
          (rng.randint(0, 20) for _ in range(rng.randint(0, 9)))]
    out = merge(iv)
    assert out == merge_brute(iv)[0], iv
    assert points(out) == points(iv), iv                        # same union
    assert all(out[k][1] < out[k + 1][0] for k in range(len(out) - 1))  # disjoint
print("1000 random inputs: same blocks as the brute force, same points, disjoint")

chain = [[2 * k, 2 * k + 1] for k in range(60)][::-1]          # nothing overlaps
print("60 disjoint intervals: brute force checks", merge_brute(chain)[1], "pairs")
```

### Each line, and which part of the idea it is

| line | in plain words | part of the idea |
|---|---|---|
| `for s, e in sorted(intervals)` | walk in order of start (ties by end) | the sort that makes "final" true |
| `if out and s <= out[-1][1]` | is there a block, and does it reach my start? | the one-sided overlap test, legal because starts are sorted |
| `out[-1][1] = max(out[-1][1], e)` | the block now reaches the further end | case 1 in the picture; the max is for nested intervals |
| `out.append([s, e])` | a gap: start a new block | case 2; the old block is final, no later interval can touch it |
| `return out` | the blocks, in order | the union |

Three settled confusions.

**Where is cs?** It is `out[-1][0]`, set once when the block opens and never
changed. Because starts are sorted, no later interval in the block can start
earlier, so the block's start never moves. Only its end does.

**Where is the final close?** There is none. The block is appended to `out` as soon
as it opens, and later intervals edit `out[-1]` in place. So when the loop ends, the
last block is already in `out`. Code that keeps (cs, ce) in two variables and appends
only on a gap must remember to append once more after the loop; that is the most
common way to drop the last block.

**Why `[s, e]` and not the input row?** `out.append(row)` would put the caller's own
list into the output, and the next `out[-1][1] = ...` would edit the caller's
input. Build a fresh list. Python's `sorted` copies the outer list, not the inner
ones.

### The subtle line, both ways

The line is `ce = max(ce, e)`. Here it is against `ce = e` on
[[1, 10], [2, 3], [4, 5], [11, 12]], and then the sort key changed from start to
end.

```python run
def merge_traced(intervals, extend, key=None, label="", show=True):
    if show:
        print(label)
    out = []
    for s, e in sorted(intervals, key=key):
        if out and s <= out[-1][1]:
            before = out[-1][1]
            out[-1][1] = extend(before, e)
            note = "merge: end %d -> %d" % (before, out[-1][1])
            if out[-1][1] < before:
                note += "   <- the block SHRANK"
        else:
            out.append([s, e])
            note = "new block"
        if show:
            print("   [%2d,%2d]  %-34s blocks %s" % (s, e, note, out))
    return out


nested = [[1, 10], [2, 3], [4, 5], [11, 12]]
right = merge_traced(nested, lambda ce, e: max(ce, e), label="ce = max(ce, e)  (right)")
wrong = merge_traced(nested, lambda ce, e: e, label="ce = e  (wrong)")
assert right == [[1, 10], [11, 12]]
assert wrong == [[1, 3], [4, 5], [11, 12]]          # points 6..10 have vanished

# the same bug is invisible when no interval sits inside another
plain = [[1, 4], [3, 6], [8, 9]]
assert merge_traced(plain, max, show=False) == \
       merge_traced(plain, lambda ce, e: e, show=False) == [[1, 6], [8, 9]]
print("no nesting: max and assign agree, so a sample without nesting cannot tell")

# sorting by END instead of start lets a later interval reach back over a closed block
late = [[5, 6], [1, 2], [1, 10]]
by_end = merge_traced(late, max, key=lambda p: p[1], label="sorted by end (wrong)")
assert by_end == [[1, 2], [5, 10]]                  # 3 and 4 are covered, and lost
assert merge_traced(late, max, label="sorted by start (right)") == [[1, 10]]
```

Here is the wrong run as a table, the way you would trace it on paper. A `*` marks
the block end that was overwritten.

| interval | test | ce = max(ce, e) | ce = e |
|---|---|---|---|
| [1, 10] | first | block (1, 10) | block (1, 10) |
| [2, 3] | 2 <= 10 | ce = max(10, 3) = 10 | ce = 3* |
| [4, 5] | 4 <= ce? | 4 <= 10: ce stays 10 | **4 <= 3 fails**: close (1, 3), open (4, 5) |
| [11, 12] | 11 <= ce? | 11 <= 10 fails: close (1, 10) | 11 <= 5 fails: close (4, 5) |
| result | | [1, 10], [11, 12] | [1, 3], [4, 5], [11, 12] |

Point at the row for [4, 5]. The wrong version compares 4 with 3, the end it
wrote one step earlier, which belonged to the *nested* interval [2, 3]. The real
block reaches 10. Everything after that row is built on a block end that is too
small, and the points 6 to 10 vanish from the answer.

What does the wrong version compute? It compares each interval with the end of
the *previous interval in sorted order* (whenever they touch), which is the "compare
with the previous one" instinct from the derivation. It is correct whenever no
interval ends inside the block it joins, and the middle assert shows that on such
inputs the two versions agree. That is why a sample like [[1, 3], [2, 6], [8, 10]]
passes with the bug.

Say it a second way. Sorting gives a guarantee about starts and nothing about
ends. The test `s <= ce` uses a start, which the sort controls. The update uses an
end, which the sort does not control, so the update must protect itself with a
max. Any time you write an update from sorted data, ask which half of each pair the
sort controls.

And the last trace in the output, sorted by end: [1, 2] is closed when [5, 6]
arrives, and then [1, 10], which starts at 1, arrives after the wall. That is the
wall from the picture being crossed, which can only happen when the sort key is not
the start.

### The convention line

The second subtle line is not in the merge loop but in its first character of
logic: `<=` or `<`. For closed intervals, [1, 2] and [2, 3] share the point 2, so
they overlap and merge, and the test is `s <= ce`. For half-open intervals
[1, 2) and [2, 3), the first is over at 2 when the second begins, so they do not
overlap, and the test is `s < ce`. For "adjacent integers join too", as in Track
Received Byte Ranges where [1, 3] and [4, 6] merge, the test is `s <= ce + 1`.
Three problems, three tests, one loop. Read the statement for which world you are
in, and write it as a comment on the first line of the function.

## Why it is correct

Three claims carry this chapter: the merge computes the union; the fewest rooms
equals the largest overlap; and keeping the earliest-ending interval is optimal.
All three go in one proof, in three parts.

:::proof The merge, the rooms count, and the earliest-end greedy
**Part 1: the merge computes the union.**

*Setup.* Intervals I_1, ..., I_n with I_k = [s_k, e_k], numbered so that
s_1 <= s_2 <= ... <= s_n. Their union is a set of points; it can be written in
exactly one way as disjoint maximal intervals with gaps between them. Call these
the components.

*Claim.* After the loop has handled I_1 to I_k, the list `out` is exactly the
components of I_1 ∪ ... ∪ I_k, in order. In particular the last entry's end, ce, is
the largest end among the intervals of the last component, and every earlier entry
ends strictly before the last entry starts.

*Base case.* After I_1, `out` = [[s_1, e_1]]. One interval is its own only
component.

*Step.* Assume the claim after k intervals, and let [s, e] = I_{k+1}. Because of
the sort, s >= s_k >= the last block's start cs. Two cases.

- If s <= ce, then s lies inside [cs, ce], so [s, e] and the last block share the
  point s. Their union is the single interval [cs, max(ce, e)]. It cannot touch any
  earlier entry, because those end before cs and [s, e] starts at s >= cs. So the
  components are the old ones with the last one extended to max(ce, e), which is
  exactly what the code writes.
- If s > ce, then [s, e] shares no point with the last block (it starts after the
  block ends) or with earlier entries (they end even sooner). It is a new component,
  separated by the non-empty gap from ce to s. The code appends it. The old last
  block can never change again: every later interval starts at s or later, so by
  the same argument it starts after ce too.

*Conclusion.* After n steps `out` is the components of the whole union. The loop
does constant work per interval, so it ends.

**Part 2: the fewest rooms equals the largest overlap.**

*Setup.* Meetings are half-open [s_k, e_k). A schedule puts each meeting in a room
so that two meetings in one room never share an instant. Let R be the fewest rooms
of any schedule, and M the largest number of meetings that all contain one instant.

*R >= M.* Take an instant x contained in M meetings. Any two of them share x, so no
two can share a room: at least M rooms.

*R <= M.* Hand out rooms in order of start time, giving each meeting any room that
is free at its start. Suppose a meeting starting at x finds every one of r open
rooms busy. Each busy room holds a meeting that started at or before x (it was
handed out earlier) and has not ended by x. So those r meetings and this one all
contain x: r + 1 <= M. A meeting opens a new room only when all r existing
rooms are busy, and then there are r + 1 <= M rooms. So the count never exceeds M.

So R = M, and M is what the +1/-1 sweep computes.

**Part 3: keeping the interval that ends first is optimal.**

*Setup.* We want the largest set of pairwise non-overlapping intervals. The greedy
sorts by end, keeps the first, discards everything that overlaps it, and repeats.

*Exchange.* Let g be the interval with the smallest end, and let O be any best set.
Let o be the member of O with the smallest end. Since g ends first of all,
end(g) <= end(o). Every other member of O starts after o ends (they do not overlap
o, and o ends first among them), so they start after g ends too. Replace o by g in
O: the set is still non-overlapping, and it is the same size, so it is still a
best set, and it contains g.

*Induction.* So some best set contains g. Remove g and every interval that overlaps
it; what is left of that best set is a best set for what is left of the input
(otherwise a bigger one plus g would beat it). Repeat. The greedy makes exactly
these choices, so it reaches a best size. ∎
:::

The assumptions, in plain words, each a place where a variant breaks the method.

- **Sorted by start (Part 1).** Used twice: to know the new interval cannot start
  before the block, and to know a closed block is final. Sorted by end, the second
  fails, as the trace showed.
- **The block end is the max of the ends, not the last end (Part 1).** The proof
  says "extended to max(ce, e)". Nothing else would be the union.
- **The overlap test matches the convention.** Part 1 used "s inside [cs, ce]
  means a shared point", true for closed intervals. For half-open ones, s = ce is
  not inside [cs, ce), and the test must be strict.
- **Rooms are interchangeable (Part 2).** The argument gave the meeting *any* free
  room. If a meeting may only use certain rooms, the lower bound still holds but the
  upper bound does not, and the answer can be larger than M.
- **Every interval is worth the same (Part 3).** The exchange swapped o for g and
  said "same size". If they had weights, the swap could lose value, and the greedy
  is wrong. That is Cinema Shows.
- **Well-formed input.** s <= e for closed, s < e for half-open. A backwards
  interval is empty and breaks every case.

## What it costs

**The walk.** One pass, constant work per interval, no inner loop, because the past
is summarised by ce. That is O(n).

**The sort.** O(n log n) comparisons, and it dominates. Total O(n log n) time.
Space: O(n) for the sorted copy and the output (the output can be as large as the
input when nothing overlaps).

**The brute force.** Up to n - 1 rounds of up to n^2 / 2 pair checks: O(n^3)
worst case, O(n^2) even when nothing overlaps. For 10^5 intervals the merge does
about 1.7 million comparisons in the sort and 10^5 steps in the walk.

**Is the log avoidable? Not with comparisons.** Given n numbers, make the
intervals [x, x]. Merging them outputs the distinct numbers in sorted order. So a
merge faster than sorting would sort faster than O(n log n) comparisons, which is
impossible. Merging is exactly as hard as sorting. The escape is to leave
comparisons behind: when the coordinates are small integers (minutes of a day, a
range up to 10^5), a difference array does the sweep in O(n + range) with no sort
(Variation I).

**The costs people forget.**

- **The heap version of rooms is also O(n log n)**, n pushes and up to n pops on a
  heap of size up to n. It is not faster than the sweep. Use it when you need to
  know *which* room each meeting gets, which the sweep cannot tell you.
- **Insert Interval is O(n) even though the position can be found in O(log n).**
  The answer is a whole new list, and copying the untouched intervals into it is
  O(n). An O(log n) insertion needs a structure updated in place (Variation F).
- **Online booking with a plain list** pays O(n) per insertion for shifting
  elements, so n bookings cost O(n^2). Fine for 1,000 bookings, as in
  [[p:uber-my-calendar-i|My Calendar I]], not for 10^5; then use a balanced tree or
  a sorted container ([[ordered-set]]).
- **Sorting with a `key=lambda`** calls the function once per element. Sorting the
  tuples directly is faster and sorts by start, then end, which is what the merge
  wants anyway.

## How to think about it

Ask these, in this order, on every problem in this family.

1. **What is an interval here, and does it own its end?** Closed [s, e] or
   half-open [s, e)? Integers or continuous time? Write it as the first comment:
   `# half-open [s, e), a meeting ending at t frees the room at t`. If the statement
   gives inclusive integer ends and you want half-open, convert once at the door:
   e becomes e + 1.
2. **Which question is it?** Union or coverage; is there any overlap; insert one;
   peak overlap or fewest resources; most non-overlapping or fewest removals; cover
   a target with the fewest; points that hit every interval; intersect two lists;
   accept or reject online. Each has a row in the table under the unlocking question.
3. **Which sort key?** Start, to build a union or a cover. End, to choose a subset
   or place points. All endpoints as events, to count what is simultaneous. The
   sentence to remember: *starts describe the union, ends choose the subset,
   endpoints count the crowd.*
4. **After sorting, what is the least I must remember?** One end, a counter, a heap
   of ends, two pointers. If your answer is "all the earlier intervals", the sort
   key is wrong or the problem is not this family.
5. **What happens at a tie?** Two intervals that touch at one point: overlap or
   not? At one instant where one meeting ends and another starts: which event is
   processed first? Write the rule, then check the code obeys it.
6. **Are the intervals weighted, or the resources different?** Then the greedy
   proofs fail; think DP or matching.
7. **Offline or online?** All intervals given up front means sort. One at a time,
   each accepted or rejected immediately, means a sorted structure and a neighbour
   check.
8. **How big are the coordinates?** Up to 10^5, or minutes of one day: a difference
   array, no sort. Up to 10^9 or 10^18: sort, never index by coordinate.

### Telling it from its neighbours

- **Sweep line** ([[sweep-line]]). The +1/-1 walk is the one-dimensional sweep.
  When the objects are rectangles or segments in a plane and you sweep one axis
  while keeping intervals on the other, it is that chapter.
- **Scheduling** ([[scheduling]]). Jobs with deadlines and durations, not fixed
  intervals: you choose *when* to run them. The earliest-deadline and
  exchange-argument ideas are related, but the intervals are not given.
- **Greedy and exchange arguments** ([[greedy]], [[greedy-exchange]]). Part 3 of the
  proof is the textbook exchange argument; the interval subset problems are the
  cleanest place to learn it.
- **Sorting with a key** ([[sorting]], [[custom-comparators]]). The whole technique
  is "pick the key". When the key is a tuple (end, then start), say why.
- **Heaps** ([[heap]]). The rooms problem with assignment is a heap of end times.
- **DP** ([[dynamic-programming]]). Weighted intervals.

## Variations

The roadmap names five techniques for this node: sort by start and merge; insert an
interval and test overlap; the most non-overlapping intervals by sorting by end;
the fewest rooms with a sweep or a heap of end times; and the line sweep with
+1/-1 events. A to F are the first two, G is the third, H the fourth, I the fifth.
J to L are harder relatives that appear in assessments, M is the weighted case,
and N collects the rare ones.

### A. Merge with adjacency

**What changes.** Ranges that are next to each other also join: [1, 3] and [4, 6]
become [1, 6]. The test becomes `s <= ce + 1`.

**Why.** For integer ranges, "no gap" means no missing integer between them, and 3
and 4 have none.

**Example.** Bytes [1, 3], [7, 9], [4, 6]: sorted [1, 3], [4, 6], [7, 9]; 4 <= 3 + 1
joins, 7 <= 6 + 1 joins: one range [1, 9].

**Bank.** [[p:roblox-track-received-byte-ranges|Track Received Byte Ranges]] asks
for the merged ranges after *every* chunk. With up to 2,000 chunks, re-merging the
sorted list each time (or inserting with Variation D) is fast enough; the endpoints
go up to 10^18, so only endpoint-based methods work.

### B. Total covered length

**What changes.** Merge, then add up the block lengths.

**Why.** Overlaps would be counted twice if you summed the raw intervals.

**Example.** [[p:ibm-process-execution-time|Process Execution Time]]: inclusive,
so [1, 5] is 5 units and the formula is e - s + 1. For continuous time, a meeting
from 1 to 5 o'clock is 4 hours: e - s. Same merge, different length formula; the
statement tells you which.

### C. Is there any overlap at all?

**What changes.** No output list; you only need to know whether some pair clashes.

**Why.** After sorting by start, if any two intervals overlap, then some *adjacent*
pair in sorted order overlaps. (If a and c overlap with b between them in the
sorted order, b starts between a's start and c's start, which is before a ends, so
a and b overlap.) So compare each interval with the one before it: the "previous
interval" comparison is exactly right here, because the first clash ends the
search.

**Example.** [[p:bytedance-meeting-rooms|Meeting Rooms]], half-open: [[0, 30],
[5, 10], [15, 20]] sorted, 5 < 30, clash, return false. [[7, 10], [2, 4]]: sorted,
7 < 4 fails, no clash, true. Touching meetings [1, 2), [2, 3) do not clash, so the
test is `s < previous end`.
[[p:apple-meeting-room-request-feasibility|Meeting Room Request Feasibility]] is the
same with an empty list allowed (answer true).

### D. Insert one interval into a sorted, disjoint list

**What changes.** The list is already merged. You add one interval and must
return the merged result.

**Why.** Because the list is sorted and disjoint, it splits into three runs: the
intervals that end before the new one starts (copy them), the ones that overlap it
(absorb them into [min of starts, max of ends]), and the ones that start after the
new one ends (copy them). No sort needed: O(n).

**Example.** [[p:amazon-insert-interval|Insert Interval]], closed: [[1, 2], [3, 5],
[6, 7], [8, 10], [12, 16]] plus [4, 8]. Run 1: [1, 2] ends at 2 < 4. Run 2: [3, 5]
starts at 3 <= 8, absorb to [3, 8]; [6, 7], absorb; [8, 10], 8 <= 8 (closed, so
touching counts), absorb to [3, 10]. Run 3: [12, 16]. Result [[1, 2], [3, 10],
[12, 16]].

### E. Intersect two sorted lists

**What changes.** Two lists, each sorted and disjoint; you want every overlap
between an interval of one and an interval of the other.

**Why.** The intersection of [a1, a2] and [b1, b2] is [max(a1, b1), min(a2, b2)],
non-empty when that start is at most that end. That is the overlap test of Step 1,
written as an interval. Then advance the pointer whose interval ends first: it
cannot meet anything later in the other list, because everything later there starts
after the current one, which already reaches at least as far.

**Example.** [[p:bytedance-interval-list-intersections|Intersect Two Sorted Interval Lists]]:
A = [[0, 2], [5, 10], [13, 23], [24, 25]], B = [[1, 5], [8, 12], [15, 24], [25, 26]].
Answer [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]. The one-point
intersections [5, 5], [24, 24] and [25, 25] exist because the intervals are closed.

### F. Online booking: accept or reject one at a time

**What changes.** Requests arrive one by one; each is accepted only if it clashes
with nothing accepted so far.

**Why.** Keep the accepted bookings sorted by start. They are disjoint, so a new
request can only clash with its two neighbours in that order: the last booking that
starts at or before it, and the first that starts after it. A binary search finds
them.

**Example.** [[p:uber-my-calendar-i|My Calendar I]], half-open: [10, 20) yes;
[15, 25) clashes with [10, 20), no; [20, 30) touches only, yes; [5, 10) yes;
[5, 11) clashes with [10, 20), no. Answer [true, false, true, true, false].

```python run
import bisect
import random


def insert(intervals, new):
    """Sorted, disjoint, closed intervals plus one more: three phases."""
    s, e = new
    out, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < s:          # 1. ends before new starts: copy
        out.append(list(intervals[i])); i += 1
    while i < n and intervals[i][0] <= e:         # 2. overlaps new: absorb
        s, e = min(s, intervals[i][0]), max(e, intervals[i][1]); i += 1
    out.append([s, e])
    out.extend(list(iv) for iv in intervals[i:])  # 3. starts after new ends: copy
    return out


def intersect(A, B):
    """Two sorted disjoint closed lists. Advance whichever interval ends first."""
    i = j = 0
    out = []
    while i < len(A) and j < len(B):
        lo, hi = max(A[i][0], B[j][0]), min(A[i][1], B[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if A[i][1] < B[j][1]:                     # A[i] can meet nothing later in B
            i += 1
        else:
            j += 1
    return out


def book_all(requests):
    """Half-open bookings, accepted only if they clash with nobody already booked."""
    starts, ends, answer = [], [], []
    for s, e in requests:
        k = bisect.bisect_right(starts, s)        # bookings starting at or before s
        ok = (k == 0 or ends[k - 1] <= s) and (k == len(starts) or e <= starts[k])
        if ok:                                    # only two neighbours can clash
            starts.insert(k, s); ends.insert(k, e)
        answer.append(ok)
    return answer


print(insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]))
assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
assert insert([], [5, 7]) == [[5, 7]] and insert([[1, 3]], [3, 4]) == [[1, 4]]
print(intersect([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]))
assert intersect([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]) \
    == [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
print(book_all([[10, 20], [15, 25], [20, 30], [5, 10], [5, 11]]))
assert book_all([[10, 20], [15, 25], [20, 30], [5, 10], [5, 11]]) == [True, False, True, True, False]

rng = random.Random(2)
for _ in range(500):
    pts = sorted(rng.sample(range(40), 2 * rng.randint(0, 6)))
    base = [pts[k:k + 2] for k in range(0, len(pts), 2)]
    a = rng.randint(0, 40); new = [a, a + rng.randint(0, 8)]
    covered = {x for s, e in base + [new] for x in range(s, e + 1)}
    got = insert(base, new)
    assert {x for s, e in got for x in range(s, e + 1)} == covered
    assert all(got[k][1] < got[k + 1][0] for k in range(len(got) - 1))
print("500 random inserts: same points as before plus the new one, still disjoint")
```

### G. The most intervals with no overlap (sort by end)

**What changes.** You choose a subset. Keep as many as possible with no two
overlapping, or equivalently remove as few as possible.

**Why.** Part 3 of the proof: the interval that ends first leaves the most room for
the rest, and swapping it into any best set costs nothing. So sort by end, keep an
interval if it starts at or after the end of the last one kept (for half-open), and
remember only that last end. Removals = n - kept.

**Example.** [[1, 100], [2, 3], [4, 5], [6, 7]]. By end: [2, 3], [4, 5], [6, 7]
kept, [1, 100] overlaps [2, 3] and is dropped. Kept 3, removals 1.

**The two wrong rules, with their counterexamples.** *Earliest start*: keeps
[1, 100] first, then nothing else fits: 1. *Shortest first*: on [[1, 5], [4, 7],
[6, 10]] it keeps [4, 7], the shortest, which overlaps both others: 1, while [1, 5]
and [6, 10] give 2. Only "ends first" has an exchange argument behind it.

**Bank.** [[p:bytedance-minimum-interval-removals|Minimum Removals for Non-Overlapping Intervals]]:
touching intervals are compatible, so the keep test is `s >= last_end`.

```python run
from itertools import combinations
import random


def keep_most(iv, key):
    """Greedy: walk in `key` order, keep each interval that starts at or after the
    end of the last kept one (half-open: touching is allowed)."""
    kept, last_end = [], float("-inf")
    for s, e in sorted(iv, key=key):
        if s >= last_end:
            kept.append([s, e])
            last_end = e
    return kept


by_end = lambda p: p[1]
by_start = lambda p: p[0]
by_length = lambda p: p[1] - p[0]


def best_brute(iv):
    for k in range(len(iv), 0, -1):
        for combo in combinations(sorted(iv), k):
            if all(combo[i][1] <= combo[i + 1][0] for i in range(k - 1)):
                return k
    return 0


long_first = [[1, 100], [2, 3], [4, 5], [6, 7]]
straddle = [[1, 5], [4, 7], [6, 10]]            # the short one sits across two long ones
for name, iv in (("long first", long_first), ("straddle", straddle)):
    print(name, iv)
    for label, key in (("end", by_end), ("start", by_start), ("length", by_length)):
        print("   by %-6s keeps %s" % (label, keep_most(iv, key)))
    print("   optimum", best_brute(iv))
assert len(keep_most(long_first, by_end)) == 3 and len(keep_most(long_first, by_start)) == 1
assert len(keep_most(straddle, by_end)) == 2 and len(keep_most(straddle, by_length)) == 1

rng = random.Random(9)
for _ in range(500):
    iv = [[s, s + rng.randint(1, 5)] for s in
          (rng.randint(0, 12) for _ in range(rng.randint(0, 7)))]
    assert len(keep_most(iv, by_end)) == best_brute(iv), iv
print("500 random inputs: sorting by end keeps as many as the best subset")
print("minimum removals for", long_first, "=", len(long_first) - len(keep_most(long_first, by_end)))
```

Each wrong rule is right on one of the two inputs and wrong on the other. That is
why "it passed the example" means nothing for a greedy, and why the random check
against every subset is the test to run.

### H. The fewest rooms: a sweep, or a heap of end times

**What changes.** You want the number of resources (rooms, machines, cars, cores)
so every interval gets one, with no two overlapping intervals sharing.

**Why.** Part 2 of the proof: the answer is the largest overlap. Two ways to
compute it.

- **The sweep.** +1 at every start, -1 at every end, sorted by time, running max.
  For half-open intervals, at equal times the -1 must come first: a meeting that
  ends at 10 frees its room for one that starts at 10. Sorting the pairs (t, delta)
  does that by itself, because -1 < +1.
- **The heap.** Sort by start. Keep a min-heap of the end times of busy rooms. For
  each meeting, if the earliest end is at or before its start, that room is free:
  pop it and reuse it. Otherwise open a new room. Push the meeting's end. The number
  of rooms opened is the answer, and the heap also tells you *which* room each
  meeting got.

**Example.** [[0, 30], [5, 10], [15, 20], [10, 15]], half-open. The sweep: 0 +1 (1),
5 +1 (2), 10 -1 (1), 10 +1 (2), 15 -1 (1), 15 +1 (2), 20 -1 (1), 30 -1 (0). Peak 2.

**The tie, both ways.** Meetings [0, 30) and [30, 60). With -1 first at t = 30 the
count goes 1, 0, 1: one room. With +1 first it goes 1, 2, 1: two rooms, and the
answer is wrong by one. For *closed* intervals the opposite is right, because both
meetings own the instant 30; convert to half-open with e + 1 and the tuple sort is
right again.

**Bank.** [[p:amazon-meeting-rooms-ii|Meeting Rooms II]] is the plain case.
[[p:jpmorgan-get-min-machines|Task Scheduling]] has inclusive ends ("runs from
start[i] through end[i]"), so a task ending at 5 and one starting at 5 need two
machines. [[p:google-minimum-cars-for-rental-requests|Minimum Cars for Rental Requests]]
wants the assignment itself: a heap of busy cars by return time plus a heap of free
car ids, so a freed car with the smallest id is reused first.

```python run
import heapq
import random


def rooms_sweep(meetings, show=False):
    """Half-open [s, e): +1 at s, -1 at e. At equal times -1 sorts first."""
    events = sorted([(s, +1) for s, _ in meetings] + [(e, -1) for _, e in meetings])
    cur = best = 0
    for t, d in events:
        cur += d
        best = max(best, cur)
        if show:
            print("   t=%2d %+d  in use %d  peak %d" % (t, d, cur, best))
    return best


def rooms_heap(meetings):
    """Sort by start; a min-heap holds (end time, room) for every busy room."""
    busy, opened, assigned = [], 0, []
    for s, e in sorted(meetings):
        if busy and busy[0][0] <= s:           # the room that frees first is free by s
            _, room = heapq.heappop(busy)      # reuse it
        else:
            room, opened = opened, opened + 1  # every busy room is still busy: open one
        heapq.heappush(busy, (e, room))
        assigned.append(room)
    return opened, assigned


def rooms_brute(meetings):                     # the most meetings covering one instant
    times = {t for m in meetings for t in m}
    return max((sum(s <= t < e for s, e in meetings) for t in times), default=0)


m = [[0, 30], [5, 10], [15, 20], [10, 15]]
print("sweep on", m)
assert rooms_sweep(m, show=True) == 2
print("heap: rooms and assignment (by start order)", rooms_heap(m))
assert rooms_heap(m)[0] == 2

touch = [[0, 30], [30, 60]]
wrong_order = sorted([(s, 1) for s, _ in touch] + [(e, -1) for _, e in touch],
                     key=lambda ev: (ev[0], -ev[1]))          # +1 before -1 at a tie
cur = peak = 0
for t, d in wrong_order:
    cur += d
    peak = max(peak, cur)
print("touching meetings: -1 first ->", rooms_sweep(touch), " +1 first ->", peak)
assert rooms_sweep(touch) == 1 and peak == 2

rng = random.Random(8)
for _ in range(1000):
    ms = [[s, s + rng.randint(1, 6)] for s in
          (rng.randint(0, 15) for _ in range(rng.randint(0, 9)))]
    assert rooms_sweep(ms) == rooms_heap(ms)[0] == rooms_brute(ms), ms
print("1000 random inputs: sweep == heap == the busiest instant")
```

In the heap output, the assignment [0, 1, 1, 1] reads: [0, 30) took room 0;
[5, 10) found room 0 busy until 30 and opened room 1; [10, 15) found room 1 free at
10 and reused it; [15, 20) reused room 1 again at 15.

### I. The +1/-1 sweep and the difference array

**What changes.** You want the count at every point, or the peak, and the
coordinates are small.

**Why.** The sweep sorted 2n events. When the coordinates are integers in a small
range, put the +1 and -1 directly into an array indexed by coordinate, then take a
running sum ([[prefix-sums]]). No sort: O(n + range).

**Example.** [[p:morgan-stanley-maximum-concurrent-processes|Maximum Concurrent Processes]],
inclusive minutes: [1, 3], [2, 4], [4, 5]. diff[1] += 1, diff[4] -= 1; diff[2] += 1,
diff[5] -= 1; diff[4] += 1, diff[6] -= 1. Running sums for minutes 1 to 5: 1, 2, 2, 2,
1. Peak 2. Minute 4 is shared by [2, 4] and [4, 5], and the -1 for [2, 4] sits at 5,
so minute 4 counts both.

### J. Points that hit every interval (stretch)

**What changes.** Choose the fewest points so every interval contains one (or two).

**Why.** Sort by end. The first interval to end must contain a point; the best place
for it is as far right as possible, at its end, because that point also hits the
most later intervals. Remember the last point placed; skip intervals that already
contain it.

**Example.** [1, 4], [2, 5], [6, 8]: sorted by end; place 4 (hits [1, 4] and
[2, 5]); [6, 8] does not contain 4, place 8. Two points.

**Bank.** [[p:smallest-set-covering-intervals|Smallest Set Covering Intervals]] needs
*two* points per interval: place them at e - 1 and e, and remember the two largest
points placed, because an interval may already contain one of them and need only one
more.

### K. Cover a target with the fewest intervals (stretch)

**What changes.** Choose the fewest intervals whose union covers [0, n].

**Why.** Sort by start. Among the intervals that start inside the part already
covered, take the one that reaches furthest. Remember the covered end and the best
reach so far. If no interval starting inside the covered part reaches further, there
is a gap: impossible.

**Example.** Target [0, 5], intervals [0, 2], [1, 4], [3, 5], [0, 1]. Covered up to 0;
starting at or before 0: [0, 2], [0, 1]; take [0, 2]. Covered to 2; starting at or
before 2: [1, 4]; take it. Covered to 4; [3, 5]; take it. Three intervals.

**Bank.** [[p:quince-minimum-sprinklers-to-cover-an-interval|Minimum Sprinklers to Cover an Interval]]:
sprinkler i covers [i - r, i + r], clipped to the target; then it is exactly this.

### L. One interval that overlaps all the others

**What changes.** Keep as many intervals as possible such that one of them
overlaps every other kept one.

**Why.** Try each interval as the centre. The intervals it does *not* overlap are
those ending before it starts plus those starting after it ends. With the ends and
starts each sorted, both counts are a [[binary-search]]: O(n log n) in total.

**Bank.** [[p:amazon-minimum-processes-to-drop-for-synchronization|Minimum Processes to Drop for Synchronization]]:
closed intervals, so "ends before it starts" is `end < start`, counted with
`bisect_left(sorted_ends, start)`, and "starts after it ends" is
`n - bisect_right(sorted_starts, end)`.

### M. Weighted intervals (not greedy)

**What changes.** Each interval has a value; maximise the total of a
non-overlapping set.

**Why.** The exchange in Part 3 breaks: swapping in the earliest-ending interval can
lose value. Sort by end and let best[i] be the best total using the first i
intervals; then best[i] = max(best[i - 1], value_i + best[p(i)]), where p(i) is the
number of intervals that end before interval i starts, found by binary search. That
is DP, the [[knapsack]] take-or-skip idea on a line.

**Bank.** [[p:amazon-cinema-shows|Cinema Shows]].

### N. Rare shapes

- **Gaps and free slots.** Merge the busy intervals, then output the space between
  consecutive blocks, plus before the first and after the last if the day has
  bounds. The bounds are where this is wrong first.
- **Circular time.** A task from 22:00 to 02:00 wraps midnight. Split it into
  [22:00, 24:00) and [00:00, 02:00), or sweep two copies of the day.
- **Many queries.** Sort the query points in with the endpoints and answer them
  during one sweep, or build a [[segment-tree]] or [[fenwick-tree]] over compressed
  coordinates.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **The input is pairs of endpoints.** "intervals[i] = [start_i, end_i]",
   "inclusive start and end times", "start < end for every interval". Two numbers per
   row and an order on them is the signal; the rest is which question.
2. **"Minimum number of rooms / machines / cars / chairs / cores."** The largest
   overlap. The most frequent shape here.
3. **"Overlap", "merge", "conflict", "at the same time", "concurrent".** Merge or
   peak count.
4. **"Non-overlapping", "the fewest to remove", "the most you can attend".**
   Sort by end.
5. **"Cover", "every point", "at least one in each".** Variations J and K.
6. **A range of something that is not time.** Bytes, card numbers, addresses,
   positions lit by a lamp, the reach of a sprinkler. The word "interval" may not
   appear.
7. **Constraint shapes.** n up to 10^5 with endpoints up to 10^9: sort and sweep.
   Endpoints up to 10^5 or a day of 1,440 minutes: a difference array, no sort.

**Disguised forms.** Sprinklers at positions with ranges are intervals
[i - r, i + r]. "Each show starts at start[i] and lasts duration[i]" is
[start, start + duration). A process "running from s through e" is closed, and
"up to, but not including" is half-open. "Arrows that burst balloons spanning
[x1, x2]" is points hitting intervals. Turning the story into pairs is the first
step, and deciding whether ends are owned is the second.

**Anti-signals.**

- **Weights or values on the intervals**: the greedy is wrong; DP.
- **Resources that are not interchangeable**: "meeting i may only use rooms in
  allowed[i]" is matching, not counting.
- **"Subarray" or "substring"**: you are choosing the window; [[sliding-window]].
- **Pairs that are relations**: (u, v) as an edge is a graph.

## Traps

**Assigning the block end instead of maximising it.** Symptom: nested intervals make
blocks shrink, points vanish, and the output can contain blocks that overlap. The
subtle-line block shows it.

**Sorting by the wrong endpoint.** By end for a merge: a later interval reaches back
over a closed block. By start for "most non-overlapping": one long early interval
eats the day. Symptom: passes samples, which are often already sorted by start.

**Getting the convention wrong at touching endpoints.** [1, 2] and [2, 3]: closed,
they overlap and need two rooms; half-open, they do not and need one. Symptom: off by
exactly one, only on inputs with a shared endpoint.

**The wrong tie order in the sweep.** For half-open intervals, a start processed
before an end at the same time counts one room too many. Symptom: [[0, 30], [30, 60]]
gives 2.

**The wrong length formula.** Inclusive integers: e - s + 1. Continuous time: e - s.
Symptom: every total off by the number of blocks.

**Forgetting the last block.** Code that appends a block only when a gap is found
must append once more after the loop. Symptom: the last block is missing, and an
input with one interval returns an empty list.

**Editing the caller's input.** `out.append(row)` then `out[-1][1] = ...` changes the
input list. Symptom: a second call on the same data gives a different answer.

**Empty input.** `merge([])` is `[]`, rooms for no meetings is 0, and
`max(...)` of an empty sequence raises. Symptom: a crash on the edge case the
constraints allow ("0 <= intervals.length").

## What to memorise

**The merge.**

```python
out = []
for s, e in sorted(intervals):          # by START
    if out and s <= out[-1][1]:         # '<' if half-open, '<= ce + 1' if adjacent joins
        out[-1][1] = max(out[-1][1], e) # the max is not optional
    else:
        out.append([s, e])              # a fresh list, not the caller's row
```

**The sweep.**

```python
events = sorted([(s, 1) for s, e in iv] + [(e, -1) for s, e in iv])   # half-open
cur = best = 0
for t, d in events:
    cur += d
    best = max(best, cur)
```

**The sentence.** *Starts describe the union, ends choose the subset, endpoints count
the crowd.* Then ask: after sorting, what is the least I must remember?

**The habit.** Write the convention as the first comment, `# closed [s, e]` or
`# half-open [s, e)`, and convert inclusive ends to half-open at the door with
e + 1. Then every test is `<` and every tie in the sweep sorts itself.

**Numbers worth carrying.** Merging costs O(n log n) and cannot do better with
comparisons. The fewest interchangeable resources equals the largest overlap. Two
closed intervals overlap exactly when max(starts) <= min(ends).

## Check yourself

:::check
Merge by hand, closed intervals: [[5, 8], [1, 9], [2, 6], [10, 12], [9, 9], [12, 14]].
Write the sorted order and, for each interval, the test, the action and the block
after it. Then run it again with `ce = e` and find the first interval where the
two runs differ, and the first output block that is wrong.
--
Sorted by start: [1, 9], [2, 6], [5, 8], [9, 9], [10, 12], [12, 14].

| interval | test | ce = max(ce, e) | block | ce = e | block |
|---|---|---|---|---|---|
| [1, 9] | first | open | (1, 9) | open | (1, 9) |
| [2, 6] | 2 <= ce | ce = max(9, 6) = 9 | (1, 9) | ce = 6* | (1, 6) |
| [5, 8] | 5 <= ce | ce = 9 | (1, 9) | ce = 8* | (1, 8) |
| [9, 9] | 9 <= ce? | 9 <= 9, ce = 9 | (1, 9) | **9 <= 8 fails**: close [1, 8] | (9, 9) |
| [10, 12] | 10 <= ce? | fails: close [1, 9] | (10, 12) | fails: close [9, 9] | (10, 12) |
| [12, 14] | 12 <= 12 | ce = 14 | (10, 14) | ce = 14 | (10, 14) |

Right: [[1, 9], [10, 14]]. Wrong: [[1, 8], [9, 9], [10, 14]].

The runs first differ at [2, 6], the nested interval, where the wrong one writes 6
over 9. Nothing is visible yet. The first wrong *output* is decided at [9, 9]: it
should join (1, 9) because the block reaches 9, but the wrong block only reaches 8,
so [1, 8] is closed and [9, 9] is split off. The bug happened two rows before it was
visible.
:::

:::check
Sweep by hand for rooms, half-open: [[1, 5], [2, 3], [3, 7], [5, 6], [6, 8]]. List the
events in sorted order with the running count, and give the answer. Then say what the
answer would be if the intervals were closed, and which instants change.
--
Events (time, delta) sorted, -1 before +1 at a tie: (1, +1) 1; (2, +1) 2; (3, -1) 1;
(3, +1) 2; (5, -1) 1; (5, +1) 2; (6, -1) 1; (6, +1) 2; (7, -1) 1; (8, -1) 0. Peak 2.

Closed: ends move to e + 1: [1, 6), [2, 4), [3, 8), [5, 7), [6, 9). Events: 1 +1 (1),
2 +1 (2), 3 +1 (3), 4 -1 (2), 5 +1 (3), 6 -1 (2), 6 +1 (3), 7 -1 (2), 8 -1 (1),
9 -1 (0). Peak 3. At instant 3, closed intervals [1, 5], [2, 3] and [3, 7] all contain
3, so three rooms are needed; half-open, [2, 3) is over at 3.
:::

:::check
Someone says: "To keep the most non-overlapping intervals, take the shortest ones
first; short intervals block the least." Where are they wrong?
--
Short does not mean out of the way. On [[1, 5], [4, 7], [6, 10]] (half-open), the
shortest is [4, 7], length 3, and it overlaps both others, so shortest-first keeps
1. Ending first keeps [1, 5] and [6, 10]: 2.

What makes earliest-end right is the exchange argument: the interval that ends
first can replace the first interval of any best set without creating a clash,
because everything else in that set starts after the replaced one ends, which is no
earlier than when ours ends. "Shortest" has no such swap: the shortest interval can
sit in the middle and clash with two that would both have fit.
:::

:::check
Why is it enough, for "can one person attend every meeting?", to compare each
meeting only with the one just before it in sorted order, when for merging that
same comparison is a bug?
--
Because the question is different. "Is there any clash?" stops at the first clash.
If there is no clash among adjacent pairs, then every meeting ends before the next
one starts, so the ends are increasing too, and the previous meeting's end *is* the
largest end so far. So "previous interval" and "current block" are the same thing
until the first clash, and after it we stop.

Merging does not stop at a clash. It continues with a block whose end may come from
an earlier, longer interval, so it must remember the largest end, not the last one.
:::

:::check
Insert [4, 9] into the closed, sorted, disjoint list [[1, 2], [3, 4], [6, 7],
[9, 12], [14, 15]] by hand, naming the three runs. Then do it again with half-open
intervals and the same numbers.
--
Closed. Run 1 (end < 4): [1, 2]. Run 2 (start <= 9): [3, 4] (4 >= 4, touches),
[6, 7], [9, 12] (9 <= 9, touches): absorb into [min(4, 3), max(9, 12)] = [3, 12].
Run 3: [14, 15]. Result [[1, 2], [3, 12], [14, 15]].

Half-open: [4, 9) does not touch [3, 4) (it ends at 4) or [9, 12) (it starts at 9).
Run 1 (end <= 4): [1, 2), [3, 4). Run 2 (start < 9): [6, 7), absorb: [4, 9). Run 3:
[9, 12), [14, 15). Result [[1, 2], [3, 4], [4, 9], [9, 12], [14, 15]]. The two tests
change from `end < s` / `start <= e` to `end <= s` / `start < e`.
:::

:::check
A disguised one. "A street has lamps; lamp i at position p[i] lights everything
within r[i] of it. Points q[j] are houses. For each house, how many lamps light it?"
n and the number of houses are up to 10^5, positions up to 10^9. Reduce it to this
chapter.
--
Each lamp is the closed interval [p - r, p + r]. A house is lit by every interval
containing it, so the answer for house q is the count at q in the +1/-1 sweep.

Events: +1 at p - r, -1 just after p + r (at p + r + 1 for integer positions), and a
query event at each q. Sort all of them by position, with the order at equal
positions chosen so a lamp starting at q counts and a lamp ending at q - 1 does not:
process -1, then +1, then queries. Walk with a running count and record it at each
query. O((n + m) log(n + m)). Coordinates up to 10^9 rule out a difference array
indexed by position; with positions up to 10^5 it would be the simpler choice.
:::

:::check
The heap version of Meeting Rooms II pops a room only when `busy[0][0] <= s`. What
does it compute if you write `<` instead, and for which statements is that the right
answer?
--
With `<`, a room whose meeting ends exactly when the new one starts is treated as
still busy, so touching meetings get different rooms. That is the answer for *closed*
intervals, where a meeting ending at 30 still owns the instant 30, as in Task
Scheduling ("runs from start through end"). With `<=` it is the half-open answer, as
in Meeting Rooms II and Minimum Cars for Rental Requests ("a car returned at time t may
be reused by a rental picked up at time t").

On [[0, 30], [30, 60]], `<=` gives 1 room and `<` gives 2. The same one character is
the tie order in the sweep and the `<` versus `<=` in the merge: all three are the
question "does an interval own its end?"
:::
