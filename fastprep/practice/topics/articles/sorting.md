# Sorting: the Landscape

> Sorting is rarely the answer itself; it is the n log n you pay once so that a question about the whole set becomes a question about neighbours, and the real skill is choosing the order, written as a key, that makes your question local.

## The problem it solves

Here is the problem that teaches it, [[p:akuna-minimum-absolute-difference-pairs|Minimum Absolute Difference Pairs]]:

> Given n distinct integers, return every pair whose absolute difference is the
> smallest among all pairs. Write each pair smaller value first, and list the
> pairs in ascending order.

For [6, 2, 4, 10] the smallest difference is 2, and it is achieved twice:
[[2, 4], [4, 6]].

The first solution anyone writes tries every pair.

```python
best, pairs = None, []
for i in range(n):
    for j in range(i + 1, n):
        d = abs(a[i] - a[j])
        ...                      # keep the smallest d and every pair that has it
```

It is correct. Count it: n(n-1)/2 pairs. The bank allows n = 10^5, which is about
5 x 10^9 pairs, minutes of work in Python against a limit of a second or two.

The second idea people try is to only compare elements that sit next to each other
in the input: (6, 2), (2, 4), (4, 10). That is n - 1 checks, and it is wrong. The
differences are 4, 2 and 6, so it finds (2, 4) and misses (4, 6), whose two values
are not neighbours in the input. In the input, nearness of *position* tells you
nothing about nearness of *value*.

But that wrong idea is one step from the right one. If the values were arranged so
that position *did* reflect value, comparing neighbours would be enough. That
arrangement is sorted order: [2, 4, 6, 10]. Now the neighbour gaps are 2, 2 and 4,
and the two pairs with gap 2 are exactly the answer. One sort, O(n log n), and one
pass, n - 1 checks.

That is what this chapter is about. Sorting is almost never what a problem asks
for. It is a move you make so that the thing the problem does ask for becomes
easy to read off: the closest pair is adjacent, equal items are together, the
smallest is first, the k-th largest is at a known index, a greedy rule becomes
safe. The roadmap node lists five shapes of this move: compare neighbours after
sorting; sort by a key, a tuple or a comparator; sort indices to keep original
positions; count instead of comparing when values are small; and sort first so a
greedy or two-pointer scan becomes valid. Each has a section below. This chapter
also explains how fast sorting itself can be, and proves that no comparison sort
can beat n log n.

Sorting is the fourth most used topic in the bank: 1,641 problems use it. That is
not because sorting is hard. It is because it is the step before the interesting
step in so many problems.

### When it is the wrong tool

- **Order carries meaning.** Subarrays, substrings, streaks, "in the order they
  arrive". Sorting destroys positions, so it destroys the problem. [[sliding-window]],
  [[prefix-sums]] and [[kadane]] live on the side where you may not reorder.
- **The input is already sorted.** [[p:goldman-sachs-squares-of-a-sorted-array|Squares of a Sorted Array]]
  hands you sorted data and expects O(n) with [[two-pointers]]. Calling `sorted`
  gives the right answer in the wrong time, and that gap is what the question tests.
- **You only need a few elements.** The largest one is a single pass. The k largest
  are a size-k heap in O(n log k) ([[top-k]]), or [[quickselect]] in O(n) expected.
- **You only need equality, not order.** "Are there duplicates?", "group the
  anagrams": a hash table answers in O(n) ([[hash-tables]]). Sorting also works, in
  O(n log n), because it puts equal items together; it just does more than you need.
- **The data arrives over time.** You cannot sort a stream you have not finished
  reading. Use a [[heap]] or [[median-maintenance]].

## Build it from the brute force

We start from the all-pairs loop and remove the waste one step at a time. The sort
will appear as the cure for a specific complaint about that loop.

### Step 1: count the brute force

All pairs: n(n-1)/2 checks. For n = 2,000 that is 1,999,000. Doubling n quadruples
it. That is the number to shrink.

### Step 2: notice the waste

Take seven values: [10, 1, 7, 4, 13, 5, 2]. The brute force checks 21 pairs. Among
them is the pair (1, 5), difference 4. Is there any way (1, 5) could be the closest
pair?

No. The value 2 lies between 1 and 5, and also 4. Whenever some value c lies
strictly between a and b, both (a, c) and (c, b) are closer than (a, b). So (a, b)
can never be the answer, and checking it was wasted work. The same goes for every
pair that has another value between them. The only pairs that might be the answer
are pairs with *nothing between them*: pairs of values that would be next to each
other if you lined the values up.

Here is the picture, first in general and then with the real numbers.

<svg viewBox="0 0 640 170" role="img" aria-label="schematic: values a, c, d, b on a number line; the gap from a to b is the sum of the three neighbour gaps a to c, c to d, d to b, so it is at least as big as each of them">
  <g>
    <line x1="40" y1="90" x2="600" y2="90"/>
    <circle class="fill" cx="100" cy="90" r="7"/>
    <circle cx="240" cy="90" r="7"/>
    <circle cx="330" cy="90" r="7"/>
    <circle class="fill" cx="520" cy="90" r="7"/>
    <text x="100" y="120" text-anchor="middle">a</text>
    <text x="240" y="120" text-anchor="middle">c</text>
    <text x="330" y="120" text-anchor="middle">d</text>
    <text x="520" y="120" text-anchor="middle">b</text>
    <path d="M100 80 Q170 50 240 80" fill="none"/>
    <path d="M240 80 Q285 55 330 80" fill="none"/>
    <path d="M330 80 Q425 45 520 80" fill="none"/>
    <path d="M100 80 Q310 -10 520 80" fill="none" stroke-dasharray="6 5"/>
    <text x="170" y="60" text-anchor="middle">g1</text>
    <text x="285" y="62" text-anchor="middle">g2</text>
    <text x="425" y="56" text-anchor="middle">g3</text>
    <text x="310" y="25" text-anchor="middle">b - a = g1 + g2 + g3</text>
    <text x="320" y="155" text-anchor="middle">a pair with values between them is never closer than its own neighbour gaps</text>
  </g>
</svg>

Now the seven values, in sorted order, with every neighbour gap written in:

<svg viewBox="0 0 660 190" role="img" aria-label="the values 1, 2, 4, 5, 7, 10, 13 on a number line with neighbour gaps 1, 2, 1, 2, 3, 3; the gaps 1 to 2 and 4 to 5 are shaded as the smallest; the dashed arc from 1 to 5 has difference 4, the sum of gaps 1, 2 and 1">
  <g>
    <line x1="20" y1="110" x2="640" y2="110"/>
    <circle cx="50" cy="110" r="6"/>
    <circle cx="90" cy="110" r="6"/>
    <circle cx="170" cy="110" r="6"/>
    <circle cx="210" cy="110" r="6"/>
    <circle cx="290" cy="110" r="6"/>
    <circle cx="410" cy="110" r="6"/>
    <circle cx="530" cy="110" r="6"/>
    <text x="50" y="138" text-anchor="middle">1</text>
    <text x="90" y="138" text-anchor="middle">2</text>
    <text x="170" y="138" text-anchor="middle">4</text>
    <text x="210" y="138" text-anchor="middle">5</text>
    <text x="290" y="138" text-anchor="middle">7</text>
    <text x="410" y="138" text-anchor="middle">10</text>
    <text x="530" y="138" text-anchor="middle">13</text>
    <rect class="fill" x="56" y="96" width="28" height="8"/>
    <rect class="fill" x="176" y="96" width="28" height="8"/>
    <text x="70" y="88" text-anchor="middle">1</text>
    <text x="130" y="88" text-anchor="middle">2</text>
    <text x="190" y="88" text-anchor="middle">1</text>
    <text x="250" y="88" text-anchor="middle">2</text>
    <text x="350" y="88" text-anchor="middle">3</text>
    <text x="470" y="88" text-anchor="middle">3</text>
    <path d="M50 100 Q130 20 210 100" fill="none" stroke-dasharray="6 5"/>
    <text x="130" y="40" text-anchor="middle">(1, 5): 4 = 1 + 2 + 1</text>
    <text x="330" y="175" text-anchor="middle">shaded: the smallest neighbour gaps, the answer [[1, 2], [4, 5]]</text>
  </g>
</svg>

The dashed pair (1, 5) has difference 4, and that 4 is literally 1 + 2 + 1, the
three neighbour gaps it spans. It cannot be smaller than any of them. Every
non-neighbour pair is like this. Out of 21 pairs, only the 6 neighbour pairs can
be the answer, and for n = 10^5 it is 99,999 out of five billion.

### The question that unlocks it

Two questions, asked in this order, unlock every problem in this family:

**Would the answer change if I shuffled the input? If not, in what order does the
answer become something I can read off neighbours?**

The first half is the permission. The closest pair of values does not depend on
where the values sit, so you may reorder them however you like, for free. The
second half is the design. Of all the orders you could pick, choose the one in
which the answer is *local*: next to each other, at the ends, at a known index.

Say it a second way. A brute force over pairs is slow because it does not know
which pairs matter. An order is a way of *telling* it which pairs matter: in sorted
order, only neighbours do. You pay n log n once to buy that knowledge, and every
question after it gets cheaper.

### You might think: "Sorting is cheap, so I can always sort."

Sorting is cheap, but it is not free of side effects. It throws away positions.

If the problem wants positions back, a plain sort loses them. Take
[[p:meta-kth-largest-original-index|Kth Largest Element: Return Its Original Index]]:
return the original index of the k-th largest entry, with equal values ranked by
smaller index first. nums = [5, 5, 5, 2], k = 2. The answer is index 1 (the fives
take ranks 1, 2, 3 in index order 0, 1, 2). A common attempt sorts the values to
get [5, 5, 5, 2], takes the second one, 5, and calls `nums.index(5)`, which returns
0, the *first* 5. With duplicates, a value does not tell you which position it came
from. The fix is to sort the **positions**, not the values:
`sorted(range(n), key=lambda i: (-nums[i], i))`. Each position carries its value
into the sort and its own identity out of it.

And if the problem is about a sequence (a subarray, a streak, "before" and
"after"), shuffling changes the answer, the first half of the unlocking question
says no, and sorting is simply wrong.

### You might think: "Neighbours in the input are close enough."

Already killed above, but it is worth one more line because it comes back in
disguise: [6, 2, 4, 10] checked by input neighbours finds (2, 4) and misses (4, 6).
The neighbour trick needs neighbours *in the order where position reflects value*.
That is the whole job of the sort.

### Step 3: sort, then scan neighbours

The cure:

1. Sort the values: s = sorted(a).
2. The smallest difference is the smallest neighbour gap,
   min(s[i+1] - s[i]).
3. The answer is every neighbour pair with that gap, and since s is sorted they come
   out smaller value first and in ascending order, which is exactly the output
   format the problem asks for.

Notice that last point. The sort did not just make the search cheap; it also
produced the required output order for free. That happens often.

### Step 4: "sorted" by what? The key

"Sort" always means "sort by something". For plain integers the something is the
value. For everything else you must say it, and saying it is most of the work.
Python lets you say it as a **key**: a function from an item to a value that Python
already knows how to compare.

The most useful fact here is that Python compares tuples **lexicographically**: it
compares first components, and only if they are equal does it look at the second,
and so on. So an English ordering rule, "first by A, then by B, then by C", is
exactly the tuple (A, B, C). [[p:akuna-items-sort|Items Sort]] says "ascending, first
by the frequency of each value, then by the value itself", and the key is
`(freq[v], v)`. "Descending" on a number is a minus sign: `(-points, -goal_diff,
-scored, index)` for [[p:capital-one-rank-football-teams|Rank Football Teams]].

### You might think: "A comparator is the general tool, so I should start with one."

A comparator is a function that takes two items and says which comes first. It is
more general than a key, and you need it only when the order is *not* "compare some
value of each item". [[p:linkedin-largest-number|Largest Number]] is the classic:
arrange numbers to form the largest concatenation. The rule is "a before b when the
string a+b is bigger than b+a". That compares a *pair*, and no single value of a
alone captures it.

The tempting shortcut is to sort the numbers as strings, descending. On
[3, 30, 34, 5, 9] that gives 9, 5, 34, 30, 3 and the string "9534303". The right
answer is "9534330". The problem is "3" versus "30": as strings "30" > "3", but
"3" + "30" = "330" beats "30" + "3" = "303". So the pairwise rule is needed here.
But it is slower (Python calls back into your function on every comparison) and
easier to get wrong, so reach for it only when no key exists.

### The technique in one sentence

**If the answer does not depend on the input's order, choose the order that makes
it local: write the ordering rule as a key (a tuple, read left to right from the
English), sort once, and read the answer off neighbours, ends or fixed indices;
sort positions instead of values when you must report where things came from.**

And the question to ask on every new problem: **would the answer change if I
shuffled the input, and if not, in what order does it become local?**

## Worked by hand

### Trace 1: closest pairs, on seven values

a = [10, 1, 7, 4, 13, 5, 2]. Sorted: s = [1, 2, 4, 5, 7, 10, 13]. Now walk the
neighbours once, keeping the best gap so far and the pairs that achieve it.

| i | pair (s[i], s[i+1]) | gap | best before | what happens | pairs after |
|---|---|---|---|---|---|
| 0 | (1, 2) | 1 | none | first gap: best = 1 | [[1, 2]] |
| 1 | (2, 4) | 2 | 1 | larger: ignore | [[1, 2]] |
| 2 | (4, 5) | 1 | 1 | equal: append | [[1, 2], [4, 5]] |
| 3 | (5, 7) | 2 | 1 | larger: ignore | [[1, 2], [4, 5]] |
| 4 | (7, 10) | 3 | 1 | larger: ignore | [[1, 2], [4, 5]] |
| 5 | (10, 13) | 3 | 1 | larger: ignore | [[1, 2], [4, 5]] |

Answer [[1, 2], [4, 5]], after 6 checks instead of 21.

Row 2, told in words:

> "I am looking at 4 and 5, which are next to each other in sorted order, so
> nothing lies between them. Their gap is 1. The best I have seen is also 1, from
> the pair (1, 2). A tie, so this pair belongs in the answer too. I do not need to
> compare 4 with 1, 7 or 13: each of those has 5 or 2 in between, so it is
> farther."

And one cell that would have gone wrong with a careless loop. Suppose the gaps had
been 3, 3, 1 instead. After two rows the list holds two pairs with gap 3. At the
third row the gap 1 is *strictly smaller*, so the list must be **replaced**, not
appended to. Forgetting the reset returns old pairs with a gap that is not minimal.
The code below sidesteps this by computing the minimum first and collecting in a
second pass.

### Trace 2: a two-level key, and what the second level is for

[[p:akuna-items-sort|Items Sort]]: [4, 5, 6, 5, 4, 3], ascending by frequency, then by
value. First count: 4 appears 2 times, 5 two, 6 one, 3 one. Then attach the key
(frequency, value) to each element:

| element | 4 | 5 | 6 | 5 | 4 | 3 |
|---|---|---|---|---|---|---|
| key | (2, 4) | (2, 5) | (1, 6) | (2, 5) | (2, 4) | (1, 3) |

Sort the keys: (1, 3), (1, 6), (2, 4), (2, 4), (2, 5), (2, 5). Read off the
elements: [3, 6, 4, 4, 5, 5], which matches the statement.

Two comparisons, told in words:

> "(1, 6) against (2, 4): the first components are 1 and 2. They differ, so that
> decides it: (1, 6) first. Python never looks at 6 or 4. The value only matters
> when the frequencies tie."
>
> "(2, 4) against (2, 5): the first components tie at 2. Only now does Python look
> at the second components, 4 against 5, and puts (2, 4) first. Without the second
> component, the fours and fives could come out interleaved as 4, 5, 4, 5, which
> is a valid sort by frequency and the wrong answer."

That last sentence is what this trace shows that the first did not. With distinct
integers there are no ties, so "sorted" has one meaning. As soon as keys can tie,
*the tie rule is part of the specification*, and it must be in the key. The next
section shows the bug you get when it is in the key the wrong way.

## From the idea to the code

### The direct version, and the cure, side by side

The program runs the all-pairs brute force and the sort-then-neighbours version,
counts their checks on 2,000 random distinct values, and compares their answers on
300 random arrays.

```python run
import random

def min_pairs_brute(a):
    checks, best, pairs = 0, None, []
    for i in range(len(a)):
        for j in range(i + 1, len(a)):          # every pair, once
            checks += 1
            x, y = sorted((a[i], a[j]))
            d = y - x
            if best is None or d < best:
                best, pairs = d, [[x, y]]
            elif d == best:
                pairs.append([x, y])
    return sorted(pairs), checks

def min_pairs_sorted(a):
    s = sorted(a)                               # pay n log n once
    best = min(s[i + 1] - s[i] for i in range(len(s) - 1))   # only neighbours
    pairs = [[s[i], s[i + 1]] for i in range(len(s) - 1)
             if s[i + 1] - s[i] == best]       # already in ascending order
    return pairs, len(s) - 1

for a in ([6, 2, 4, 10], [4, -2, -1, 3], [10, 1, 7, 4, 13, 5, 2]):
    print(a, "->", min_pairs_sorted(a)[0])
    assert min_pairs_sorted(a)[0] == min_pairs_brute(a)[0]
assert min_pairs_sorted([6, 2, 4, 10])[0] == [[2, 4], [4, 6]]
assert min_pairs_sorted([10, 1, 7, 4, 13, 5, 2])[0] == [[1, 2], [4, 5]]

big = random.Random(1).sample(range(-2 * 10**6, 2 * 10**6), 2000)
(pb, cb), (ps, cs) = min_pairs_brute(big), min_pairs_sorted(big)
print("n = 2000: brute %d pair checks, sorted %d neighbour checks" % (cb, cs))
assert pb == ps and cb == 2000 * 1999 // 2

rng = random.Random(5)
for _ in range(300):
    a = rng.sample(range(-40, 40), rng.randint(2, 10))
    assert min_pairs_sorted(a)[0] == min_pairs_brute(a)[0]
print("sorted neighbours == all pairs on 300 random arrays")
```

### Each line, and which part of the brute force it replaces

| line | in plain words | in the brute force |
|---|---|---|
| `s = sorted(a)` | line the values up | (nothing: this is the new idea) |
| `range(len(s) - 1)` | only neighbour pairs (i, i+1) | the inner loop `for j in range(i + 1, n)`, cut down to j = i + 1 |
| `s[i + 1] - s[i]` | the gap, with no `abs` | `abs(a[i] - a[j])`; in sorted order the right one is never smaller |
| `best = min(...)` | the smallest neighbour gap | the running minimum over all pairs |
| `if s[i + 1] - s[i] == best` | keep every tie | `elif d == best: pairs.append(...)` |
| (no final sort) | output already ascending | `sorted(pairs)` at the end |

The second line is where the brute force shrinks. The inner loop ran j over every
later index; the proof below says only j = i + 1 can matter, so the inner loop
disappears and the work drops from n²/2 to n. Note what replaced it: not a smarter
loop, but a **precondition**. The code is only right because the line above it
sorted. Swap those two lines' roles and nothing works. That is the general shape:
sorting establishes a fact, and the scan relies on it.

Two boring confusions, settled.

**Why no `abs`?** Because s[i+1] >= s[i] after sorting, the difference is never
negative. With `abs` the code would still work; without the sort, dropping `abs`
would be a bug. The missing `abs` is a small reminder of which line is doing the
work.

**`sorted(a)` or `a.sort()`?** `sorted(a)` returns a new list and leaves a alone.
`a.sort()` sorts a in place and returns `None`. Use `sorted` when you still need the
original order, or when you are not sure; it costs one extra list.

### The subtle line, both ways

The line that decides whether a sorting solution is right is usually the **tie
rule**. Here it is in [[p:meta-kth-largest-original-index|Kth Largest Element: Return Its Original Index]]:
rank entries by larger value first, and equal values by smaller original index
first. The key that says exactly that is

```python
order = sorted(range(n), key=lambda i: (-nums[i], i))     # value desc, index asc
```

The tempting alternative is to write the key "naturally" and flip it:

```python
order = sorted(range(n), key=lambda i: (nums[i], i), reverse=True)
```

`reverse=True` reverses the *whole* comparison. It turns value-ascending into
value-descending, which you wanted, and also turns index-ascending into
index-descending, which you did not. On nums = [3, 2, 3, 1, 2, 4, 5, 5, 6]:

| rank | right: key (-v, i) | wrong: (v, i), reverse=True |
|---|---|---|
| 1 | i=8 (v=6) | i=8 (v=6) |
| 2 | i=6 (v=5) | i=7 (v=5) * |
| 3 | i=7 (v=5) | i=6 (v=5) * |
| 4 | i=5 (v=4) | i=5 (v=4) |
| 5 | i=0 (v=3) | i=2 (v=3) * |
| 6 | i=2 (v=3) | i=0 (v=3) * |
| 7 | i=1 (v=2) | i=4 (v=2) * |
| 8 | i=4 (v=2) | i=1 (v=2) * |
| 9 | i=3 (v=1) | i=3 (v=1) |

A `*` marks every rank where they disagree: every rank inside a group of equal
values. Look at rank 4, the one the bank's sample asks for (k = 4, answer 5). Value 4
appears once, so both versions give index 5. **The sample passes and the hidden
test with k = 2 fails**: the right answer is 6, the wrong code says 7.

What does the wrong version compute? Ties broken by *larger* index first. That is a
legitimate order, just not this problem's. Two more facts finish the picture, and
the run block checks both. `sorted(..., key=lambda i: nums[i], reverse=True)`, with
the value alone in the key, is *right*: Python's `reverse=True` keeps equal
elements in their original order, so the index tie is left alone. And sorting
ascending and then reversing the list with `[::-1]` is *wrong*, because reversing a
list reverses everything, ties included.

```python run
nums = [3, 2, 3, 1, 2, 4, 5, 5, 6]
idx = range(len(nums))

right = sorted(idx, key=lambda i: (-nums[i], i))          # value desc, index asc
wrong = sorted(idx, key=lambda i: (nums[i], i), reverse=True)  # flips BOTH keys
also = sorted(idx, key=lambda i: nums[i], reverse=True)   # flips the value only

print("rank  right(-v, i)  wrong (v, i) reversed")
for r, (a, b) in enumerate(zip(right, wrong), 1):
    mark = "" if a == b else "   <- differs"
    print("%4d   i=%d (v=%d)    i=%d (v=%d)%s" % (r, a, nums[a], b, nums[b], mark))

assert right == [8, 6, 7, 5, 0, 2, 1, 4, 3]
assert wrong == [8, 7, 6, 5, 2, 0, 4, 1, 3]
assert right[4 - 1] == wrong[4 - 1] == 5     # the sample (k = 4) cannot tell them apart
assert right[2 - 1] == 6 and wrong[2 - 1] == 7   # k = 2 can
assert also == right                         # reverse=True keeps ties stable
assert sorted(idx, key=lambda i: nums[i])[::-1] == wrong   # reversing AFTER does not

def kth_largest_index(nums, k):
    return sorted(range(len(nums)), key=lambda i: (-nums[i], i))[k - 1]
assert kth_largest_index([3, 2, 1, 5, 6, 4], 2) == 3
assert kth_largest_index([5, 5, 5, 2], 2) == 1
assert kth_largest_index([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 5
print("kth_largest_index passes the three samples")
```

The habit that prevents this: **write each tie-break with its own direction inside
the key, and do not use `reverse=True` on a tuple.** Put a minus sign on the
components that go descending. If a descending component is a string, which cannot
be negated, use the stable multi-pass sort shown next.

### The key vocabulary

In an interview you will almost never write a sorting algorithm. You will write a
key. This block is the vocabulary: a two-level key, a four-level key with negation,
a custom alphabet, a pairwise comparator, mixed directions on a string, and a sorted
copy kept beside the original.

```python run
from collections import Counter
from functools import cmp_to_key

# "by frequency ascending, then by value ascending" -> the sentence IS the tuple
items = [4, 5, 6, 5, 4, 3]
freq = Counter(items)
by_freq = sorted(items, key=lambda v: (freq[v], v))
print("Items Sort       :", by_freq)
assert by_freq == [3, 6, 4, 4, 5, 5]

# four tie-breaks, three of them "more is better": negate the numbers
def top_two(wins, draws, scored, conceded):
    pts = [3 * w + d for w, d in zip(wins, draws)]
    gd = [s - c for s, c in zip(scored, conceded)]
    order = sorted(range(len(wins)), key=lambda i: (-pts[i], -gd[i], -scored[i], i))
    return order[:2]
print("Rank Teams       :", top_two([3, 2, 3], [0, 4, 0], [8, 10, 7], [3, 4, 1]),
      top_two([2, 2, 2, 2], [1, 1, 1, 1], [5, 6, 6, 6], [2, 4, 3, 3]))
assert top_two([3, 2, 3], [0, 4, 0], [8, 10, 7], [3, 4, 1]) == [1, 2]
assert top_two([2, 2, 2, 2], [1, 1, 1, 1], [5, 6, 6, 6], [2, 4, 3, 3]) == [2, 3]

# a custom alphabet is a rank table; lists already put a prefix first
order = "9AacB"
rank = {ch: r for r, ch in enumerate(order)}
arr = ["BBBBa", "BBBB9", "B9ca", "Aa999", "B9A", "B", "B9A"]
custom = sorted(arr, key=lambda s: [rank[ch] for ch in s])
print("Custom Sort      :", custom)
assert custom == ["Aa999", "B", "B9A", "B9A", "B9ca", "BBBB9", "BBBBa"]

# an order that is only defined pairwise: a before b when a+b beats b+a
def largest_number(nums):
    s = [str(x) for x in nums]
    s.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)))
    return "0" if s[0] == "0" else "".join(s)
naive = "".join(sorted(map(str, [3, 30, 34, 5, 9]), reverse=True))
print("Largest Number   :", largest_number([3, 30, 34, 5, 9]), " naive string sort:", naive)
assert largest_number([3, 30, 34, 5, 9]) == "9534330" and naive == "9534303"
assert largest_number([10, 2]) == "210" and largest_number([0, 0]) == "0"

# mixed directions on a string key: least significant first, lean on stability
rows = [("A9", 3, False), ("B2", 7, True), ("C1", 3, False), ("A1", 7, False), ("B1", 7, True)]
t = sorted(rows, key=lambda r: r[0])                   # sku ascending
t = sorted(t, key=lambda r: r[1], reverse=True)        # aisle descending
t = sorted(t, key=lambda r: r[2])                      # non-frozen first
one = sorted(rows, key=lambda r: (r[2], -r[1], r[0]))
print("three passes     :", [r[0] for r in t])
assert t == one

# when the answer compares against sorted order, keep the original
heights = [1, 1, 4, 2, 1, 3]
target = sorted(heights)                               # a copy: heights survives
print("out of place     :", sum(h != g for h, g in zip(heights, target)))
assert sum(h != g for h, g in zip(heights, target)) == 3
```

What each part is doing, and why it is written that way:

| piece | what it says | why this form |
|---|---|---|
| `(freq[v], v)` | frequency, then value | tuples compare left to right, so the order of components is the priority |
| `(-pts[i], -gd[i], -scored[i], i)` | three descending numbers, then index ascending | a minus sign flips one component without touching the others |
| `[rank[ch] for ch in s]` | the custom alphabet's position of each letter | a list of ranks compares like a word, and a shorter prefix comes first, as the statement requires |
| `cmp_to_key(...)` | a before b when a+b > b+a | the order is defined on pairs, so no single value per item exists |
| three `sorted` passes, least important first | mixed directions with a string | each stable pass keeps the order of the previous pass among its ties |
| `target = sorted(heights)` | a sorted copy | [[p:concentric-ai-count-students-outside-sorted-positions|Count Students Outside Their Sorted Positions]] compares each position against sorted order; sorting in place would compare the array with itself and always answer 0 |

The three-pass trick deserves one more sentence, because it is how radix sort works.
A **stable** sort keeps equal elements in the order they came in. After pass 1 the
rows are in SKU order. Pass 2 sorts by aisle; among rows with the same aisle, it
keeps pass 1's order, so they stay in SKU order. Pass 3 sorts by frozen; among rows
with the same frozen flag, it keeps pass 2's order, which was aisle-then-SKU. So the
final order is frozen, then aisle, then SKU: the *last* pass is the most important
key. Python's sort is stable, always, which is what makes this legal.

## Why it is correct

Three things need proving: that the closest pair is a neighbour pair, that a tuple
key sorts by the English rule it transcribes, and that a greedy run on sorted data
can be optimal. The third is the template for every "sort first so a greedy becomes
valid" problem.

:::proof Sorting makes these answers local
**Part 1: the closest pairs are neighbour pairs.**

Let s[0] < s[1] < ... < s[n-1] be the distinct values in sorted order, and let
g[t] = s[t+1] - s[t] be the neighbour gaps. Every gap is positive, because the values
are distinct.

Take any pair i < j. Its difference is a sum of the gaps it spans:

s[j] - s[i] = g[i] + g[i+1] + ... + g[j-1].

Every term is positive, so the sum is at least as large as each single term. In
particular it is at least the smallest neighbour gap, call it G. So no pair has a
difference below G, and the neighbour pair with gap G achieves it: the minimum
difference over all pairs is exactly G.

Now which pairs achieve G? If j = i + 1, the pair is a neighbour pair, and it
achieves G exactly when g[i] = G. If j > i + 1, the sum has at least two positive
terms, so it is strictly larger than either term, which is at least G. So it is
strictly larger than G. Therefore **the pairs with difference G are exactly the
neighbour pairs with gap G**. The scan finds all of them and no others.

**Part 2: a tuple key sorts by the rule it transcribes.**

The rule "by A, then by B" means: x comes before y if A(x) < A(y), or if A(x) = A(y)
and B(x) < B(y). Python compares the tuples (A(x), B(x)) and (A(y), B(y)) by looking
at the first components; if they differ, that decides; if equal, it compares the
second. That is the rule, word for word. By the same argument, a tuple of k
components is "by the first, then the second, ..., then the k-th". Negating a
numeric component reverses that component's comparison only, because -a < -b exactly
when a > b, and equality is unchanged, so later components are consulted in exactly
the same cases.

**Part 3: on sorted data, the greedy "anchor the lowest, take all that fit" is
optimal.**

The problem: [[p:amazon-group-students|Group Students]] asks for the fewest classes
such that within a class, levels differ by at most d. The greedy: sort; the lowest
remaining level x starts a class; that class takes every remaining level up to
x + d; repeat.

*The greedy's classes are valid.* Each class starts at its smallest member x and
takes only levels up to x + d, so its max minus min is at most d.

*No valid grouping uses fewer.* Call the level that starts each greedy class an
**anchor**, and let the anchors be x1 < x2 < ... < xK. Class t takes every remaining
level up to x_t + d, so the next anchor is the first level beyond that:
x_(t+1) > x_t + d. Therefore *any two anchors differ by more than d*, and no valid
class, in any grouping, can contain two of them. Every grouping must put the K
anchors into K different classes, so it has at least K classes.

*Conclusion.* The greedy uses K classes, and every valid grouping uses at least K.
The greedy is optimal.

Sorting was used in one place: the anchor is the *smallest* remaining level, so
"everything up to x + d" is exactly what can share a class with it, and the next
anchor is more than d above it. Without sorting, the first unplaced item is not the
smallest, and both facts fail. ∎
:::

Now the assumptions, in plain words. Each is a bug when it fails.

- **Part 1 used distinct values.** With duplicates, a gap can be 0, and then a
  non-neighbour pair such as the first and third of three equal values also has
  difference 0. The minimum is still the smallest neighbour gap, but "exactly the
  neighbour pairs" is no longer true: with values [5, 5, 5], the pairs with difference
  0 are three, and only two are neighbours. The bank's problem says the values are
  distinct, which is why the scan is complete.
- **The comparison must be a consistent order.** Part 2 assumed that "<" on each
  component is a real order: if a < b and b < c then a < c. A comparator that says
  "equal if within 5" breaks this (0 and 4 are "equal", 4 and 8 are "equal", 0 and 8
  are not), and then no sorted output exists. The Traps section runs one.
- **Keys must not change during the sort.** The proof compares keys at different
  times as if they were fixed.
- **Stability is a property of the algorithm, not of "sortedness".** Part 2 says
  nothing about elements with *equal* keys. Python's sort keeps them in input order;
  C++'s `std::sort` and a quicksort you write do not. If a tie order matters, put it
  in the key.
- **Part 3 used that a class is a range of values.** The greedy is optimal because
  the constraint (max minus min at most d) only depends on the ends of a sorted run.
  A constraint that depends on the members in another way ("at most 3 per class") can
  break it.

## What it costs

### The brute force and the cure

All pairs: n(n-1)/2 checks, Θ(n²). Sort then neighbours: one sort, Θ(n log n), plus
n - 1 checks, Θ(n). Total Θ(n log n). For n = 10^5, log2(n) is about 17, so the sort
is about 1.7 x 10^6 comparisons. The brute force was 5 x 10^9.

The rest of this section answers the question every interviewer eventually asks:
why n log n? Where does the log come from, and can you do better?

### Insertion sort: Θ(n + inversions)

The sort a person does by hand with playing cards: take the next card and slide it
left past every bigger card. On [5, 2, 4, 1, 3]:

| pass | element | comparisons | slides | array after |
|---|---|---|---|---|
| 1 | 2 | 1 (5 > 2) | 1 | [2, 5, 4, 1, 3] |
| 2 | 4 | 2 (5 > 4, then 2 < 4: stop) | 1 | [2, 4, 5, 1, 3] |
| 3 | 1 | 3 (5, 4, 2 all > 1) | 3 | [1, 2, 4, 5, 3] |
| 4 | 3 | 3 (5 > 3, 4 > 3, then 2 < 3: stop) | 2 | [1, 2, 3, 4, 5] |

Seven slides. Now count the **inversions** of the input, the pairs that are in the
wrong order: (5,2), (5,4), (5,1), (5,3), (2,1), (4,1), (4,3). Seven. That is not a
coincidence. A slide swaps two neighbours that are out of order, which fixes exactly
that one pair and leaves every other pair's order unchanged. So a sort that only
swaps neighbours does exactly one slide per inversion. A reversed array of n
elements has n(n-1)/2 inversions, so insertion sort is Θ(n²) in the worst case. A
sorted array has none, so insertion sort is Θ(n) on it, one failed comparison per
pass. That is why Python's built-in sort uses it on short, nearly sorted runs.

### Merge sort: Θ(n log n)

To beat n², an element must be able to move far in one step. [[merge-sort]] splits
the array in half, sorts each half, and merges the two sorted halves by repeatedly
taking the smaller front element. The merge is one linear pass. So

```
T(n) = 2 T(n/2) + n,   T(1) = 0
```

Unroll it instead of quoting a theorem. At depth k of the recursion there are 2^k
pieces of size n/2^k, and merging them all costs 2^k x n/2^k = n. Every level costs
n. The pieces reach size 1 at depth log2 n. Total: n per level times log2 n levels.

<svg viewBox="0 0 640 210" role="img" aria-label="recursion tree of merge sort with four levels: one piece of size n, two of n/2, four of n/4, eight of n/8; each level totals n work, and there are log n levels">
  <g>
    <rect class="fill" x="60" y="20" width="512" height="26" rx="4"/>
    <text x="316" y="38" text-anchor="middle">n</text>
    <rect class="fill" x="60" y="62" width="250" height="26" rx="4"/>
    <rect class="fill" x="322" y="62" width="250" height="26" rx="4"/>
    <text x="316" y="80" text-anchor="middle">n/2 + n/2 = n</text>
    <rect class="fill" x="60" y="104" width="119" height="26" rx="4"/>
    <rect class="fill" x="191" y="104" width="119" height="26" rx="4"/>
    <rect class="fill" x="322" y="104" width="119" height="26" rx="4"/>
    <rect class="fill" x="453" y="104" width="119" height="26" rx="4"/>
    <text x="316" y="122" text-anchor="middle">4 pieces, still n</text>
    <rect class="fill" x="60" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="126" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="192" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="258" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="324" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="390" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="456" y="146" width="54" height="26" rx="4"/>
    <rect class="fill" x="518" y="146" width="54" height="26" rx="4"/>
    <text x="316" y="164" text-anchor="middle">8 pieces, still n</text>
    <text x="316" y="196" text-anchor="middle">log n levels, n per level</text>
  </g>
</svg>

[[quicksort]] has the same recurrence when its pivot splits evenly, and
T(n) = T(n-1) + n = Θ(n²) when the pivot is always the smallest. Heapsort is
Θ(n log n) always ([[heap]]).

### The floor: no comparison sort beats log2(n!)

Can a cleverer comparison sort beat n log n? No, and the argument is short enough
to give at a whiteboard. Picture any comparison sort as a game of twenty questions.
At the start, any of the n! orderings of the input is possible. Each comparison
"is x < y?" has two answers, so it splits the remaining possibilities into two
groups, and the algorithm continues with one of them. It can stop only when one
ordering remains. The algorithm is a **decision tree**: each node is a comparison,
each leaf is an output.

<svg viewBox="0 0 700 280" role="img" aria-label="decision tree of comparisons sorting three elements a, b, c: the root asks a less than b, the second level asks b less than c or a less than c, and there are six leaves, one per ordering, so some path has three comparisons">
  <g>
    <rect class="fill" x="300" y="12" width="90" height="30" rx="6"/>
    <text x="345" y="32" text-anchor="middle">a &lt; b ?</text>
    <line x1="320" y1="42" x2="185" y2="86"/>
    <line x1="370" y1="42" x2="515" y2="86"/>
    <text x="235" y="68">yes</text>
    <text x="450" y="68">no</text>
    <rect class="fill" x="140" y="86" width="90" height="30" rx="6"/>
    <text x="185" y="106" text-anchor="middle">b &lt; c ?</text>
    <rect class="fill" x="470" y="86" width="90" height="30" rx="6"/>
    <text x="515" y="106" text-anchor="middle">a &lt; c ?</text>
    <line x1="160" y1="116" x2="80" y2="164"/>
    <line x1="210" y1="116" x2="280" y2="164"/>
    <line x1="490" y1="116" x2="420" y2="164"/>
    <line x1="540" y1="116" x2="620" y2="164"/>
    <text x="80" y="182" text-anchor="middle">a b c</text>
    <rect class="fill" x="240" y="164" width="90" height="30" rx="6"/>
    <text x="285" y="184" text-anchor="middle">a &lt; c ?</text>
    <text x="420" y="182" text-anchor="middle">b a c</text>
    <rect class="fill" x="575" y="164" width="90" height="30" rx="6"/>
    <text x="620" y="184" text-anchor="middle">b &lt; c ?</text>
    <line x1="262" y1="194" x2="210" y2="238"/>
    <line x1="308" y1="194" x2="355" y2="238"/>
    <line x1="598" y1="194" x2="548" y2="238"/>
    <line x1="643" y1="194" x2="690" y2="238"/>
    <text x="205" y="256" text-anchor="middle">a c b</text>
    <text x="358" y="256" text-anchor="middle">c a b</text>
    <text x="545" y="256" text-anchor="middle">b c a</text>
    <text x="688" y="256" text-anchor="middle">c b a</text>
    <text x="20" y="274">6 leaves, so some path is at least 3 long</text>
  </g>
</svg>

With three elements there are 3! = 6 orderings, so the tree has 6 leaves, and a
binary tree with 6 leaves must have a path of 3 comparisons. That is the whole
argument; the proof makes it general.

:::proof No comparison sort uses fewer than log2(n!) comparisons in the worst case
Fix a deterministic algorithm that learns about its input only by comparing pairs of
elements. Run it on each of the n! orderings of n distinct values, and draw its
decision tree.

*Different orderings end at different leaves.* If two different orderings reached
the same leaf, the algorithm asked the same questions, got the same answers, and
produced the same rearrangement for both. But the correct rearrangement differs for
two different orderings of distinct values, so it would be wrong on one of them. So a
correct algorithm has at least n! leaves.

*A binary tree of height h has at most 2^h leaves.* Height 0 is one leaf. A tree of
height h is a root with at most two subtrees of height at most h - 1, each with at
most 2^(h-1) leaves, so at most 2^h in total.

*Combine.* 2^h >= n!, so h >= log2(n!). The height is the number of comparisons on
the longest path, the worst case.

*And log2(n!) grows like n log n.* Keep only the larger half of the factors of n!:
the n/2 factors from n/2 to n are each at least n/2, and the rest are at least 1. So
n! >= (n/2)^(n/2), and log2(n!) >= (n/2) log2(n/2), which grows like n log2 n. ∎
:::

The assumption that matters is in the first sentence: the algorithm learns
**only** by comparing. Counting sort does not compare. It uses the value as an array
index, and one indexing step distinguishes k outcomes instead of two. That is how it
runs in O(n + k), and it is not a contradiction of the bound; it is outside its
model. Variation D uses this.

The program below sorts all 5,040 orderings of seven elements with insertion sort
and merge sort, checks that insertion sort's slides always equal the inversions,
and checks merge sort's worst case against the bound ceil(log2(7!)) = 13.

```python run
from itertools import permutations
from math import factorial, log2, ceil

def insertion_sort(a, stats):
    a = list(a)
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0:
            stats["cmp"] += 1
            if a[j] <= key:                     # strict '>' to move = stable
                break
            a[j + 1] = a[j]; stats["slide"] += 1; j -= 1
        a[j + 1] = key
    return a

def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])

st = {"cmp": 0, "slide": 0}
print("insertion sort [5,2,4,1,3] ->", insertion_sort([5, 2, 4, 1, 3], st), st)
assert st == {"cmp": 9, "slide": 7} and inversions([5, 2, 4, 1, 3]) == 7

def merge_sort(a, cmps):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    left, right = merge_sort(a[:m], cmps), merge_sort(a[m:], cmps)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        cmps[0] += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

n = 7
worst_ins = worst_mrg = 0
for p in permutations(range(n)):
    s, c = {"cmp": 0, "slide": 0}, [0]
    assert insertion_sort(p, s) == merge_sort(list(p), c) == list(range(n))
    assert s["slide"] == inversions(p)          # one slide per inversion, always
    worst_ins, worst_mrg = max(worst_ins, s["cmp"]), max(worst_mrg, c[0])
bound = ceil(log2(factorial(n)))
print("n=7: %d orderings, bound ceil(log2(7!)) = %d" % (factorial(n), bound))
print("worst comparisons: insertion %d, merge %d" % (worst_ins, worst_mrg))
assert worst_ins == n * (n - 1) // 2 and worst_mrg >= bound
```

Merge sort's worst case on seven elements is 14 comparisons, one above the floor of
13. Insertion sort's is 21, which is 7 x 6 / 2, the reversed array.

### The costs people forget

- **The key runs n times, not n log n times.** Python computes each key once and
  caches it. But a key is not free: `key=lambda w: sorted(w)` costs L log L per word.
- **Comparing strings or tuples is not O(1).** It costs up to the length of the
  shorter one. Sorting n strings of length L is O(n L log n). Problems that sort
  strings bound the total length for this reason.
- **`cmp_to_key` is slow.** It calls your Python function on every one of the
  n log n comparisons, against the key's n calls. Fine for n = 100, as in Largest
  Number; noticeable at 10^6.
- **Sorting inside a loop.** Re-sorting after each of n updates is O(n² log n). If
  the order must be maintained under updates, use a [[heap]] or an [[ordered-set]].
- **Space.** `sorted` makes a new list, Θ(n). Python's sort itself needs up to n/2
  extra slots for merging.

Two numbers worth carrying: log2(10^5) is about 17, and log2(10^6) is about 20.
Sorting 2 x 10^5 items is a few million comparisons, nothing.

## How to think about it

Ask these, in order, on every problem where sorting might help.

1. **Would the answer change if I shuffled the input?** If yes, the order is part of
   the problem: do not sort the data (you may still sort a *copy*, or sort indices).
   If no, you may choose any order you like.
2. **After sorting, what becomes local?** The closest pair is adjacent. Equal items
   are together. The smallest and largest are at the ends. The k-th largest is at
   index n - k. Items "within d of each other" form contiguous runs. Name the fact you
   will use, because the scan after the sort relies on it.
3. **Sorted by what? Write the rule in English, then transcribe it into a tuple,
   left to right.** One component per "then by". A minus sign on numeric components
   that go descending.
4. **What about ties?** If the statement gives a tie rule, it goes in the key. If it
   says "preserve input order", you need a stable sort (Python's is) or the index in
   the key. Never use `reverse=True` on a tuple.
5. **Do I need original positions?** Then sort `range(n)` with a key that reads the
   arrays, or sort (value, index) pairs.
6. **Is the order defined only on pairs?** Then a comparator (`cmp_to_key`), and
   check it is a consistent order.
7. **Are the values small, or can they be capped?** Letters, scores 0..100, colours
   0..2, counts up to n. Then count instead of comparing: O(n + k).
8. **Do I need it all sorted?** Only the top k: a heap. Only the k-th: quickselect.
   Already sorted: do not sort.

Then, before code, write three lines: **the key**, **the fact that sorting makes
true**, and **the scan that uses it**. The third line is the actual algorithm; the
sort is its precondition.

### Telling it from its neighbours

- **[[hash-tables]].** Both put equal things together. A hash table does it in O(n)
  and gives you no order; sorting does it in O(n log n) and gives you all of it. If
  you only need "same or not", hash. If you need "closest", "smallest" or "in order",
  sort.
- **[[two-pointers]].** Often the scan *after* a sort: pair the smallest with the
  largest, move one end inward. The sort is what makes the pointer moves safe.
- **[[greedy]] and [[greedy-exchange]].** A greedy usually needs to process items in
  a particular order, and the exchange argument that proves it is also the argument
  for the sort key. "Earliest deadline first" is a sort key with a proof attached.
- **[[binary-search]].** Needs sorted data; sorting once lets you search many times.
- **[[intervals]] and [[sweep-line]].** Sort by start time, then sweep. The sort is
  one line; choosing start versus end is the insight.
- **[[heap]] and [[top-k]].** When you need only part of the order, or the data
  changes.
- **[[counting-sort]], [[merge-sort]], [[quicksort]], [[quickselect]].** The
  algorithms themselves, each with its own chapter.

## Variations

Eight variations, from the everyday to the rare. A to E and G are the node's
techniques and common in assessments. F is the stability question, which hides
inside many of them. H is the set of algorithms you may be asked to write by hand,
less common in OAs than in onsite interviews.

### A. Sort, then compare neighbours

**What changes.** Nothing beyond the main derivation: sort, then a single pass over
(s[i], s[i+1]).

**Why.** In sorted order, any property defined by "how far apart two values are"
is decided by neighbours (Part 1 of the proof).

**Example.** The closest pairs, above. And
[[p:vanguard-picking-tickets|Picking Tickets]]: choose as many tickets as possible
so that, sorted, neighbouring values differ by at most 1. Sorted, the chosen tickets
must be a contiguous run of the sorted array (skipping a ticket in the middle never
helps, since keeping it cannot create a gap larger than 1). So sort and find the
longest run with every neighbour difference at most 1. [8, 5, 4, 8, 4] sorts to
[4, 4, 5, 8, 8]: runs [4, 4, 5] and [8, 8], answer 3.

### B. Sort by a key, a tuple, or a comparator

**What changes.** The order is given by a rule in the statement, and the work is
transcribing it.

**Why.** Python's tuple comparison is the English "first by, then by" (Part 2 of the
proof).

**Examples.** [[p:akuna-items-sort|Items Sort]], (frequency, value).
[[p:capital-one-rank-football-teams|Rank Football Teams]]: more points, then larger
goal difference, then more goals, then smaller index, which is
(-points, -gd, -scored, i); team 1 with 10 points beats teams 0 and 2 with 9, and
team 2's goal difference 6 beats team 0's 5, so the top two are [1, 2].
[[p:amazon-custom-sort-string|Custom Sort String]]: a custom alphabet becomes a
dictionary from character to rank, and each string becomes the list of its ranks.
[[p:linkedin-largest-number|Largest Number]]: the pairwise rule a + b > b + a, and
the edge case where every number is 0 (return "0", not "000").

**Why the Largest Number rule is a real order.** A comparator must be consistent: if
a before b and b before c, then a before c. For a + b > b + a this is true but not
obvious. Think of each digit string x as a repeating decimal: "a before b" turns out
to mean the infinite string aaaa... is bigger than bbbb..., and comparing infinite
strings is a genuine order. You do not need to prove it in an interview, but you
should know that "a comparator that looks reasonable" is not automatically an order
(Traps shows one that is not).

### C. Sort indices to keep original positions

**What changes.** You sort `range(n)`, and the key looks up the data. Or you sort
(value, index) pairs.

**Why.** The output is about positions, or the tie rule mentions positions, or there
are parallel arrays that must move together.

**Examples.** [[p:meta-kth-largest-original-index|Kth Largest Element: Return Its Original Index]],
the subtle-line demonstration above. [[p:capital-one-rank-football-teams|Rank Football Teams]],
four parallel arrays: sort indices, and every array is read through the index.
[[p:tcs-array-rank-transform|Array Rank Transform]]: replace each value by its rank
among the distinct values, in the original order. Sort the distinct values, build a
map value -> rank, then rewrite the original array through the map. [40, 10, 20, 30]
becomes [4, 1, 2, 3]. The sort computes the ranks; the original array supplies the
output order.

### D. Counting sort when the values are small

**What changes.** No comparisons. Count how many times each value occurs, in an array
indexed by the value, then read the counts back in order.

**Why.** If values lie in 0..k-1, one pass of counting and one pass over k buckets
sorts in O(n + k), below the comparison floor, because indexing by a value is not a
comparison.

**The stable version.** To sort records (not just numbers) by a small key, turn the
counts into starting positions: key 0's block starts at 0, key 1's block starts after
all the 0s, and so on. Then walk the input in order and drop each record at its key's
next free position. Because the input is walked in order, equal keys keep their
order: the sort is stable, which is what radix sort needs.

**Examples.**
- [[p:infosys-sort-colors|Sort Colors]]: values 0, 1, 2 only, constant extra space,
  no library sort. Counting and rewriting works in two passes. The one-pass version
  is the Dutch national flag: keep three regions, 0s at the front, 2s at the back,
  1s in the middle, and an unknown region shrinking between them. The subtle line is
  that after swapping a 2 to the back you must **not** advance the middle pointer,
  because the value you swapped in has not been looked at yet.
- [[p:nutanix-num-players|Number of Players]]: scores 0..100, competition ranking
  (ties share a rank, the next rank skips). A player's rank is 1 plus the number of
  strictly higher scores. 101 buckets, walk from 100 down keeping "how many are above
  me". [100, 50, 50, 25] with k = 3: ranks 1, 2, 2, 4, so 3 players level up. Score 0
  never levels up.
- [[p:amazon-find-encrypted-password|Find Encrypted Password]]: the smallest
  palindrome made from the letters. Count the 26 letters; the first half is each
  letter, in alphabetical order, repeated count/2 times; the odd letter (at most one,
  since the input is a palindrome) goes in the middle; the second half is the mirror.
  "babab": a: 2, b: 3, half "ab", middle "b", answer "abbba".
- [[p:amazon-maximum-rating-threshold-count|Maximum Rating Threshold Count]]: the
  largest k with at least k ratings of at least k (the h-index). Ratings go up to
  10^9, which looks too big to count. But k can never exceed n, so a rating above n is
  as good as a rating of exactly n. **Cap every value at n**, and counting sort over
  0..n works. Walk k from n down, accumulating how many ratings are at least k, and
  stop at the first k where that count reaches k. [3, 0, 6, 1, 5]: at k = 3 the
  ratings 3, 5, 6 make three: answer 3.

```python run
def counting_sort(pairs, k):
    """Stable sort of (key, payload) with 0 <= key < k, without one comparison."""
    count = [0] * k
    for key, _ in pairs:
        count[key] += 1
    start, s = [0] * k, 0
    for v in range(k):                          # where each key's block begins
        start[v], s = s, s + count[v]
    out = [None] * len(pairs)
    for item in pairs:                          # input order -> stable
        out[start[item[0]]] = item
        start[item[0]] += 1
    return out

data = [(2, "a"), (0, "b"), (2, "c"), (1, "d"), (0, "e"), (2, "f")]
print("counting sort :", counting_sort(data, 3))
assert counting_sort(data, 3) == sorted(data, key=lambda p: p[0])

def sort_colors(a):                             # Dutch flag: 0s | 1s | unknown | 2s
    lo, mid, hi = 0, 0, len(a) - 1
    while mid <= hi:
        if a[mid] == 0:
            a[lo], a[mid] = a[mid], a[lo]; lo += 1; mid += 1
        elif a[mid] == 1:
            mid += 1
        else:
            a[mid], a[hi] = a[hi], a[mid]; hi -= 1   # do NOT advance mid
    return a
print("sort colors   :", sort_colors([2, 0, 2, 1, 1, 0]))
assert sort_colors([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]

def num_players(k, scores):                     # scores 0..100: 101 buckets
    cnt = [0] * 101
    for s in scores:
        cnt[s] += 1
    above, ok = 0, 0
    for s in range(100, 0, -1):                 # score 0 never levels up
        if above + 1 <= k:                      # rank = 1 + number strictly above
            ok += cnt[s]
        above += cnt[s]
    return ok
assert [num_players(3, [100, 50, 50, 25]), num_players(4, [20, 40, 60, 80, 100]),
        num_players(4, [2, 2, 3, 4, 5])] == [3, 4, 5]

def max_threshold(ratings):                     # cap at n: k can never exceed n
    n = len(ratings)
    cnt = [0] * (n + 1)
    for r in ratings:
        cnt[min(r, n)] += 1
    at_least = 0
    for k in range(n, 0, -1):
        at_least += cnt[k]                      # ratings >= k
        if at_least >= k:
            return k
    return 0
assert [max_threshold([3, 0, 6, 1, 5]), max_threshold([1, 1, 1]), max_threshold([0, 0, 0, 0])] == [3, 1, 0]

def smallest_palindrome(p):                     # 26 buckets, read in order
    cnt = [0] * 26
    for ch in p:
        cnt[ord(ch) - 97] += 1
    half = "".join(chr(97 + c) * (cnt[c] // 2) for c in range(26))
    mid = "".join(chr(97 + c) for c in range(26) if cnt[c] % 2)
    return half + mid + half[::-1]
print("palindromes   :", [smallest_palindrome(p) for p in ("babab", "yxxy", "ded")])
assert [smallest_palindrome(p) for p in ("babab", "yxxy", "ded")] == ["abbba", "xyyx", "ded"]
```

### E. Sort first, so a greedy or two-pointer scan becomes valid

**What changes.** The sort is not the answer and not even the main idea. It is the
precondition that makes a simple rule correct.

**Why.** Many greedy rules talk about "the smallest remaining" or "the largest
remaining". On sorted data those are at known places, and the proof (Part 3 above)
usually needs the remaining items to form a contiguous run.

**Examples.**
- [[p:amazon-group-students|Group Students]]: the greedy proved in Part 3.
  [1, 4, 7, 3, 4] with spread 2 sorts to [1, 3, 4, 4, 7]: class {1, 3} (up to 3),
  class {4, 4} (up to 6), class {7}. Three classes.
- [[p:amazon-find-unique-values|Find Unique Values]]: repeatedly pair the highest and
  lowest remaining developer, and count distinct pair averages. After sorting, the
  pairs are simply (s[i], s[n-1-i]): two pointers from both ends. Compare *sums*
  instead of averages: two pairs have equal averages exactly when they have equal
  sums, and integer sums avoid floating point. [1, 4, 1, 3, 5, 6] sorts to
  [1, 1, 3, 4, 5, 6], pairs (1, 6), (1, 5), (3, 4), sums 7, 6, 7: two distinct.
- [[p:google-min-amplitude|Min Amplitude]]: the smallest max-minus-min after changing
  up to 3 elements. Changing an element is as good as deleting it (set it equal to a
  survivor). Deleting 3 elements to shrink the range only ever means deleting from the
  ends of the sorted array: i from the bottom and 3 - i from the top, for i = 0..3.
  Four candidates, after one sort. [-1, 3, -1, 8, 5, 4] sorts to
  [-1, -1, 3, 4, 5, 8]; dropping two from the bottom and one from the top leaves
  [3, 4, 5], range 2.
- [[p:amazon-stable-robot-configurations|Stable Robot Configurations]] (stretch). With
  k robots operating, an operating robot needs threshold at most k - 1, and a standby
  robot needs threshold greater than k. So the operating set is forced: exactly the
  robots with threshold below k, there must be exactly k of them, and none may have
  threshold equal to k. On the sorted thresholds a, that is: a[k-1] < k (if k > 0) and
  a[k] > k (if k < n). Try every k from 0 to n, each an O(1) check. 2^n configurations
  collapse to n + 1 checks, because sorting turns "which robots" into "how many".

```python run
from itertools import product

def min_classes(levels, spread):                # Group Students
    a, i, classes = sorted(levels), 0, 0
    while i < len(a):
        lo = a[i]                               # lowest left MUST be in some class
        classes += 1
        while i < len(a) and a[i] - lo <= spread:
            i += 1                              # take everything that fits with it
    return classes

def min_classes_brute(levels, spread):          # try every labelling
    n = len(levels)
    for k in range(1, n + 1):
        for lab in product(range(k), repeat=n):
            groups = [[levels[i] for i in range(n) if lab[i] == g] for g in range(k)]
            if all(max(g) - min(g) <= spread for g in groups if g):
                return k
assert min_classes([1, 4, 7, 3, 4], 2) == 3
for lv, sp in [([1, 4, 7, 3, 4], 2), ([5, 1, 9, 2, 6, 3], 3), ([2, 2, 8, 5], 0)]:
    assert min_classes(lv, sp) == min_classes_brute(lv, sp)

def unique_averages(exp):                       # Find Unique Values
    a, n = sorted(exp), len(exp)
    return len({a[i] + a[n - 1 - i] for i in range(n // 2)})   # sums, no floats
assert [unique_averages([1, 4, 1, 3, 5, 6]), unique_averages([1] * 6),
        unique_averages([1, 100, 10, 1000])] == [2, 1, 2]

def min_amplitude(A):                           # change up to 3 elements
    if len(A) <= 4:
        return 0
    a = sorted(A)
    return min(a[len(a) - 4 + i] - a[i] for i in range(4))   # drop i low, 3-i high
assert min_amplitude([-1, 3, -1, 8, 5, 4]) == 2 and min_amplitude([10, 10, 3, 4, 10]) == 0

def stable_configs(t):                          # Stable Robot Configurations
    a, n = sorted(t), len(t)
    return sum(1 for k in range(n + 1)           # k robots operating
               if (k == 0 or a[k - 1] < k) and (k == n or a[k] > k))

def stable_brute(t):
    n, good = len(t), 0
    for on in product((0, 1), repeat=n):
        k = sum(on)
        good += all((k - 1 >= t[i]) if on[i] else (k < t[i]) for i in range(n))
    return good
assert stable_configs([6, 0, 3, 3, 6, 7, 2, 7]) == 3 == stable_brute([6, 0, 3, 3, 6, 7, 2, 7])
for t in ([0, 0], [1, 1], [2, 0, 1], [3, 3, 3], [0, 2, 2, 4]):
    assert stable_configs(t) == stable_brute(t), t

def picking_tickets(tickets):                   # sort, then compare neighbours
    a, best, run = sorted(tickets), 1, 1
    for i in range(1, len(a)):
        run = run + 1 if a[i] - a[i - 1] <= 1 else 1
        best = max(best, run)
    return best
assert picking_tickets([8, 5, 4, 8, 4]) == 3 and picking_tickets([3, 1, 2]) == 3
print("group students, unique averages, min amplitude, robots, tickets: all agree")
```

Each greedy above is checked against a brute force that tries every grouping or
every configuration. That habit, a tiny brute force beside the clever version, is
the cheapest way to find out that a greedy is wrong before an interviewer does.

### F. Stability: "preserve their original order"

**What changes.** The statement says equal keys keep their input order.

**Why.** It is a demand for a **stable** sort. Python's `sorted` is stable, so a key
on the coordinate alone is enough. In a language whose default sort is not stable,
add the index as the last key component.

**Example.** [[p:figma-sort-documents-left-to-right|Sort Documents Left to Right]]:
order documents by left coordinate, ties in input order. [header 40, sidebar 10,
card-a 25, card-b 25] gives sidebar, card-a, card-b, header. card-a stays before
card-b because it came first. Stability is also what makes the three-pass
mixed-direction sort and radix sort work.

### G. Sort, then two pointers or binary search

**What changes.** After sorting, a pair problem becomes a two-ended walk
([[two-pointers]]), or each query becomes a binary search ([[binary-search]]).

**Why.** In sorted order, moving the left pointer right can only increase a sum and
moving the right pointer left can only decrease it, so each step rules out a whole
row of pairs. That is the same "the order tells you which pairs matter" idea as the
neighbour scan, with two neighbours moving.

**Example.** "Count pairs with sum at most T": sort, put pointers at both ends; if
s[lo] + s[hi] <= T, then s[lo] pairs with every element from lo + 1 to hi, so add
hi - lo and move lo right; otherwise move hi left. O(n log n) for the sort, O(n) for
the walk. This has its own chapter.

### H. The algorithms themselves (onsite more than OA)

You may be asked to write one. Each has its own chapter.

- **[[merge-sort]]**: split, sort halves, merge. Stable, Θ(n log n) always, Θ(n)
  extra space. Its merge step, instrumented, counts inversions in O(n log n)
  ([[inversion-count]]).
- **[[quicksort]]**: partition around a pivot, recurse. In place, fast in practice,
  Θ(n²) on a bad pivot sequence; randomise the pivot.
- **[[quickselect]]**: quicksort that recurses into one side only, giving the k-th
  smallest in O(n) expected.
- **Heapsort**: build a heap, pop n times. In place, Θ(n log n) always, not stable
  ([[heap]]).
- **[[counting-sort]] and radix sort**: variation D; radix chains d stable counting
  passes, one per digit, least significant first.
- **[[cyclic-sort]]**: when the values are a permutation of 1..n, swap each into its
  index in O(n).
- **[[k-way-merge]]**: merge k sorted lists with a heap of size k; external sorting
  (data bigger than memory) is sort chunks, then k-way merge. Rare in interviews.

## Recognising it in a statement

Ordered by how much to trust them.

1. **The output names an order with tie-breakers.** "Sorted by X, then by Y", "more
   points ranks first; if equal, ...". Transcribe it into a tuple. This is the most
   common sorting signal in the bank.
2. **"Preserve the original order" for ties.** A stable sort.
3. **The question is about a set, not a sequence.** "Any pair", "the closest", "the
   k-th largest", "choose a subset", "you may reorder". Nothing refers to position,
   so position is yours to choose.
4. **An obvious all-pairs scan with n up to 10^5.** After sorting, the pairs worth
   examining are neighbours, or reachable by two pointers.
5. **"Median", "rank", "percentile", "k-th".** Defined on sorted order whether or
   not you build it.
6. **A greedy that talks about "smallest remaining" or "largest remaining".** Sort
   first, then prove the greedy (an exchange argument).
7. **Small value ranges in the constraints.** Scores 0..100, letters, colours 0..2,
   or values that can be capped at n. Counting sort.

### Disguised forms

- **"Change up to k elements to minimise the range."** Changing equals deleting, and
  deleting only helps at the ends of the sorted array (Min Amplitude).
- **"How many configurations are stable?"** If the condition depends only on *how
  many* are chosen, sorting turns "which ones" into "how many" (Stable Robots).
- **"The largest k with at least k values at least k."** Sort descending, or count
  with values capped at n (the h-index).
- **"Can these be arranged so that ...?"** If the arrangement is free, sorted order
  is usually the best or the only candidate to check. Two arrays where every a[i] must
  beat b[i] after rearranging: sort both, compare position by position.

### Anti-signals: looks like sorting, is not

- **"Subarray", "substring", "consecutive", "in the order given".** Sorting changes
  the answer.
- **The input is stated to be sorted.** Use it; do not re-sort.
- **"Without sorting"** in the statement, or a constant-space requirement on a
  three-value array. Count or partition.
- **Only the extremes are wanted.** One pass, or a heap.
- **Only equality matters.** A hash table, O(n).

## Traps

**1. `reverse=True` on a tuple key.** Symptom: correct on samples, wrong on ties.
Demonstrated above. Negate the numeric components instead, or use stable passes.

**2. Sorting the values when you needed positions.** Symptom: `nums.index(v)`
returns the first occurrence, so duplicates all map to the same index. Sort indices.

**3. Sorting the array you still needed.** Symptom: "count the positions that differ
from sorted order" always answers 0, because you compared the sorted array with
itself. Sort a copy.

**4. Digits stored as text.** Symptom: "10" sorts before "9", because strings compare
character by character. Use `key=int`.

**5. `list.sort()` returns `None`.** Symptom: `TypeError` or `AttributeError` on
`None` one line later. `sorted(x)` returns the list; `x.sort()` does not.

**6. A comparator that is not an order.** Symptom: an unsorted result and no error.
"Equal if within 5" is the classic: 0 ~ 4 and 4 ~ 8 but 0 < 8. Sort by the raw value
and apply the tolerance afterwards, when grouping.

**7. Forgetting to reset the answer list when a strictly better gap appears.**
Symptom: stale pairs with a larger gap in the output. Compute the minimum first, or
reset on strict improvement.

**8. Advancing the middle pointer after a swap with the back in Sort Colors.**
Symptom: a 2 or 0 left in the middle. The value swapped in is unexamined.

**9. Assuming stability you were not given.** Python and Java's object sort are
stable; C++'s `std::sort` and a hand-written quicksort are not. Put the tie in the
key.

**10. Averages as floats.** Symptom: two equal averages that compare unequal after
division, in other languages or with very large values. Compare sums, or cross-multiply.

Traps 2 to 6, run:

```python run
from functools import cmp_to_key

tokens = ["10", "9", "100", "23"]               # digits, but typed as text
print("as text  :", sorted(tokens), " as numbers:", sorted(tokens, key=int))
assert sorted(tokens) == ["10", "100", "23", "9"]

ranked = [3, 1, 2].sort()                       # sorts in place, returns None
print("sort() returns:", ranked)
assert ranked is None

nums = [5, 5, 5, 2]                             # sort values, then hunt for indices
wrong = [nums.index(v) for v in sorted(nums, reverse=True)]
right = sorted(range(len(nums)), key=lambda i: (-nums[i], i))
print("index() after sort:", wrong, " sorted indices:", right)
assert wrong == [0, 0, 0, 3] and right == [0, 1, 2, 3]

def close_enough(a, b, tol=5):                  # "equal" if within 5: not an order
    return -1 if a < b - tol else (1 if b < a - tol else 0)
out = sorted([8, 4, 0, 12, 3], key=cmp_to_key(close_enough))
print("tolerance comparator:", out)
assert out != sorted(out)                       # not sorted, and no error raised

heights = [1, 3, 2]
heights.sort()                                  # destroyed the reference
print("in-place sort, then compare to itself:", sum(h != t for h, t in zip(heights, sorted(heights))))
assert sum(h != t for h, t in zip(heights, sorted(heights))) == 0   # always 0
```

## What to memorise

The template:

```python
order = sorted(range(n), key=lambda i: (-score[i], name[i], i))  # the English, left to right
s = sorted(a)
for i in range(len(s) - 1):          # after sorting, neighbours decide
    gap = s[i + 1] - s[i]
```

And for mixed directions on a string, stable passes, least important first:

```python
t = sorted(rows, key=lambda r: r.name)
t = sorted(t, key=lambda r: r.city, reverse=True)
t = sorted(t, key=lambda r: r.group)
```

The question: **would the answer change if I shuffled the input, and if not, in what
order does it become local?**

The habit: write the ordering rule in English, one "then by" per component, then
transcribe it left to right into a tuple, with a minus sign on each descending
number. Never `reverse=True` on a tuple.

The numbers: Θ(n log n) is the floor for comparison sorts, because log2(n!) is about
n log2 n; log2(10^5) is about 17; counting sort is O(n + k) when values are below k;
insertion sort is Θ(n + inversions); a reversed array has n(n-1)/2 inversions;
Python's sort is stable and linear on already sorted input.

## Check yourself

:::check
Hand trace. a = [15, 3, 9, 20, 4, 11, 8]. Sort it, write every neighbour gap, and
give the closest pairs. Then count how many pairs the brute force would check, and
explain in one sentence why (3, 8) can never be the answer.
--
Sorted: [3, 4, 8, 9, 11, 15, 20]. Gaps: 4-3 = 1, 8-4 = 4, 9-8 = 1, 11-9 = 2,
15-11 = 4, 20-15 = 5. Smallest gap 1, achieved by (3, 4) and (8, 9). Answer
[[3, 4], [8, 9]].

The brute force checks 7 x 6 / 2 = 21 pairs; the scan checks 6.

(3, 8) has difference 5 = 1 + 4, the sum of the gaps from 3 to 4 and 4 to 8. The
value 4 lies between them, so (3, 4) is closer: a pair with anything between it is
never the closest.
:::

:::check
Hand trace. Sort the teams of [[p:capital-one-rank-football-teams|Rank Football Teams]]'s
second sample: wins [2, 2, 2, 2], draws [1, 1, 1, 1], scored [5, 6, 6, 6], conceded
[2, 4, 3, 3]. Write each team's key (-points, -gd, -scored, index), sort the keys,
and give the top two. Then say what `reverse=True` with the key
(points, gd, scored, index) would return.
--
Points are 3 x 2 + 1 = 7 for everyone. Goal differences: 3, 2, 3, 3. Keys:
team 0 (-7, -3, -5, 0), team 1 (-7, -2, -6, 1), team 2 (-7, -3, -6, 2),
team 3 (-7, -3, -6, 3).

Sorted: (-7, -3, -6, 2), (-7, -3, -6, 3), (-7, -3, -5, 0), (-7, -2, -6, 1). The
first component ties; the second puts teams 0, 2, 3 (gd 3) before team 1; the third
puts teams 2 and 3 (scored 6) before team 0; the fourth puts 2 before 3. Top two:
[2, 3].

With (points, gd, scored, index) and reverse=True, the index is reversed too: teams
2 and 3 tie on everything else, and the larger index comes first, giving [3, 2].
Wrong, and only on the full tie.
:::

:::check
Hand trace. Run counting sort's stable placement on the records (1, "p"), (0, "q"),
(1, "r"), (2, "s"), (0, "t") with keys in 0..2. Write the counts, the starting
positions, and the output array after each record is placed.
--
Counts: key 0 twice, key 1 twice, key 2 once: [2, 2, 1]. Starting positions: key 0
at 0, key 1 at 2, key 2 at 4: start = [0, 2, 4].

- (1, "p"): goes to start[1] = 2, start becomes [0, 3, 4]. out = [_, _, p, _, _].
- (0, "q"): goes to 0, start [1, 3, 4]. out = [q, _, p, _, _].
- (1, "r"): goes to 3, start [1, 4, 4]. out = [q, _, p, r, _].
- (2, "s"): goes to 4, start [1, 4, 5]. out = [q, _, p, r, s].
- (0, "t"): goes to 1, start [2, 4, 5]. out = [q, t, p, r, s].

Final: (0, q), (0, t), (1, p), (1, r), (2, s). Equal keys keep input order (q before
t, p before r) because the input was walked front to back: stable.
:::

:::check
Why is the n log n lower bound not contradicted by counting sort, which runs in
O(n + k)? And when is counting sort a bad idea anyway?
--
The bound is about algorithms that learn only by comparing two elements, each
comparison giving one of two answers. The proof counts the leaves of that binary
decision tree. Counting sort never compares: it uses a value as an array index, and
one indexing step can lead to any of k places. It is outside the model, so the bound
says nothing about it.

It is a bad idea when k is much larger than n: sorting 10^5 values drawn from 0..10^9
would need a billion counters. Then compare-sort, or use radix sort (several stable
counting passes on digits), or cap the values when the problem allows it, as the
h-index problem does at n.
:::

:::check
Someone says: "My Kth Largest Original Index solution uses
`sorted(range(n), key=lambda i: (nums[i], i), reverse=True)` and passes all three
samples, so it is right." Where are they wrong, and what is the smallest input that
shows it?
--
`reverse=True` reverses the whole tuple comparison, so ties in value are broken by
*larger* index first, while the problem says smaller index first. The samples pass
because at the ranks they ask about, the value is not tied (or, in [5, 5, 5, 2] with
k = 2, the middle 5 is index 1 in both orders).

Smallest failing input: nums = [7, 7], k = 1. The right answer is index 0; the code
returns index 1. Fix: key `(-nums[i], i)`, or key `nums[i]` alone with
`reverse=True`, which Python keeps stable.
:::

:::check
Someone says: "Group Students is just a greedy, so I can process the levels in input
order: start a class with the first unplaced trainee, add everyone within the spread
of them." Give a counterexample, and say which line of the proof needs the sort.
--
Two ways it breaks. Taken literally ("within the spread of the first one"), [3, 1, 5]
with spread 2 puts 1 and 5 with 3, since each is within 2 of 3, but 5 - 1 = 4: the
class is invalid.

Repaired to "add a trainee if the class stays within the spread", it is valid but
not optimal. [2, 3, 1, 4] with spread 1: 2 starts a class and takes 3; 1 and 4 no
longer fit (3 - 1 = 2, 4 - 2 = 2); then {1} and {4}: 3 classes. Sorted, the greedy
makes {1, 2} and {3, 4}: 2 classes.

The proof needs the sort at "the anchor is the smallest remaining level". That is
what makes "within d of the anchor" the same as "max minus min at most d", and what
makes consecutive anchors more than d apart, which is the whole lower bound. In input
order the anchor 2 was not the smallest, and the 1 was stranded.
:::

:::check
Reduce this disguised problem. "You may change at most 2 elements of
[9, 1, 14, 6, 3, 7] to any values. What is the smallest possible max minus min?"
Say why only the ends of the sorted array matter, list the candidates, and give the
answer.
--
Changing an element to a value already present is as good as deleting it, and it is
never worse to do so. Deleting elements can only shrink the range if you delete from
the extremes: deleting a middle value leaves the max and min unchanged. So delete i
from the bottom and 2 - i from the top, for i = 0, 1, 2.

Sorted: [1, 3, 6, 7, 9, 14]. Candidates: drop 0 low and 2 high, range 7 - 1 = 6;
drop 1 low and 1 high, range 9 - 3 = 6; drop 2 low and 0 high, range 14 - 6 = 8.
Answer 6.
:::
