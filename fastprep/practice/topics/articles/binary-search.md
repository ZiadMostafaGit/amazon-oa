# Binary Search

> Binary search is not about sorted arrays. It is about a question whose answer
> flips from no to yes exactly once, and about finding the place where it flips.

## When you reach for it

You reach for binary search when you can ask a yes/no question about a position,
and the answers, read left to right, look like this:

```
no  no  no  no  yes  yes  yes
                 ^
                 the boundary you want
```

That shape has a name: the question is **monotone**. Once it says yes, it never
goes back to no. Sortedness is one way to get that shape — in a sorted array,
"is `a[i] >= target`?" turns from no to yes exactly once — but it is only one
way. "Can we finish all deliveries in `d` days with a truck of capacity `c`?"
has the same shape in `c`, and no array is sorted anywhere in sight. That second
reading is the one that wins interviews, and it has its own chapter:
[[binary-search-on-answer]].

So the trigger is not the word *sorted*. The trigger is: **I can test a
candidate answer quickly, and the test is monotone.** Everything else is
bookkeeping.

## The idea

Keep a window that is known to contain the boundary, and throw away half of it
on every step.

To keep the bookkeeping honest, do not think in terms of "the answer might be
anywhere in `[lo, hi]`". Think in terms of two facts you refuse to break:

- `lo` is an index where the answer is **no** (or a sentinel just left of the array);
- `hi` is an index where the answer is **yes** (or a sentinel just right of it).

The boundary is trapped strictly between them. Every step tests the midpoint and
moves whichever pointer keeps both facts true. When `hi - lo == 1` there is
nothing left between them, and `hi` is the first yes.

<svg viewBox="0 0 640 150" role="img" aria-label="predicate array with lo and hi bracketing the boundary">
  <g>
    <rect class="fill" x="20" y="40" width="70" height="40" rx="4"/>
    <rect class="fill" x="90" y="40" width="70" height="40" rx="4"/>
    <rect class="fill" x="160" y="40" width="70" height="40" rx="4"/>
    <rect x="230" y="40" width="70" height="40" rx="4"/>
    <rect x="300" y="40" width="70" height="40" rx="4"/>
    <rect x="370" y="40" width="70" height="40" rx="4"/>
    <rect x="440" y="40" width="70" height="40" rx="4"/>
    <text x="48" y="65">no</text>
    <text x="118" y="65">no</text>
    <text x="188" y="65">no</text>
    <text x="255" y="65">yes</text>
    <text x="325" y="65">yes</text>
    <text x="395" y="65">yes</text>
    <text x="465" y="65">yes</text>
    <line x1="230" y1="20" x2="230" y2="95"/>
    <text x="180" y="18">boundary</text>
    <text x="150" y="112">lo (a no)</text>
    <text x="300" y="112">hi (a yes)</text>
    <line x1="195" y1="118" x2="195" y2="86"/>
    <line x1="335" y1="118" x2="335" y2="86"/>
    <text x="20" y="140">the window shrinks; the two facts never break</text>
  </g>
</svg>

Written down, that is four lines:

```python
def first_true(lo, hi, pred):
    """Smallest x in (lo, hi] with pred(x) true, given pred(lo) false."""
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid
    return hi
```

Everything in this chapter is that loop wearing a different hat.

## Worked by hand

Take `a = [2, 3, 5, 5, 8, 13]` and the question "is `a[i] >= 5`?". The answers
are `no no yes yes yes yes`, so the boundary is index 2 and that is what we
should get back.

Set the sentinels: `lo = -1` (conceptually a no, left of everything) and
`hi = 6` (conceptually a yes, right of everything).

| step | lo | hi | mid | `a[mid]` | `a[mid] >= 5`? | move |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | -1 | 6 | 2 | 5 | yes | `hi = 2` |
| 2 | -1 | 2 | 0 | 2 | no | `lo = 0` |
| 3 | 0 | 2 | 1 | 3 | no | `lo = 1` |
| 4 | 1 | 2 | — | — | — | `hi - lo == 1`, stop |

Answer: `hi = 2`. Correct.

Notice three things while they are fresh.

First, `mid` was never equal to `hi`, and never equal to `lo`, so neither
pointer could get stuck. That is a property of `lo + (hi - lo) // 2` on a window
of width at least 2, and it is exactly why this template cannot loop forever.

Second, the sentinels are allowed to be *outside* the array. We never read
`a[-1]` or `a[6]`; we only ever read `a[mid]`, and `mid` is strictly between the
two. The sentinels are claims, not memory.

Third, the loop did not stop early when it found a 5 at index 2. It could not:
there might be an earlier 5. A binary search that returns as soon as it sees a
match answers a different question — *does the value exist?* — and cannot answer
*where does the run of 5s begin?*.

## Why it is correct

The informal argument ("we halve, so we get there") explains the speed, not the
answer. Here is the real one.

:::proof Correctness of `first_true`
**Setup.** Let `pred` be monotone on the integers `lo₀ .. hi₀`: if `pred(x)` is
true then `pred(y)` is true for every `y > x` in range. Assume the caller
guarantees `pred(lo₀)` is false and `pred(hi₀)` is true.

**Invariant.** At the top of every iteration: `pred(lo)` is false, `pred(hi)` is
true, and `lo < hi`.

**Base case.** Before the first iteration the invariant is exactly the caller's
precondition, and `lo₀ < hi₀` because a false index must sit left of a true one
under monotonicity.

**Inductive step.** Assume the invariant holds and `hi - lo > 1`. Then
`mid = lo + (hi - lo) // 2` satisfies `lo < mid < hi`: from `hi - lo >= 2` we get
`(hi - lo) // 2 >= 1`, so `mid >= lo + 1`; and `(hi - lo) // 2 <= (hi - lo) - 1`
for `hi - lo >= 2`, so `mid <= hi - 1`. Two cases:

- `pred(mid)` is true. We set `hi = mid`. Now `pred(hi)` is true by the test,
  `pred(lo)` is still false because `lo` did not move, and `lo < hi` because
  `lo < mid`. Invariant restored.
- `pred(mid)` is false. We set `lo = mid`. Now `pred(lo)` is false by the test,
  `pred(hi)` is still true, and `lo < hi` because `mid < hi`. Invariant restored.

**Termination.** In both branches the new window width is either
`mid - lo = (hi - lo) // 2` or `hi - mid = hi - lo - (hi - lo) // 2`, and for
`hi - lo >= 2` both are at least 1 and at most `hi - lo - 1`. The width is a
positive integer that strictly decreases, so it cannot decrease forever: the
loop ends, and it ends with `hi - lo == 1`.

**Conclusion.** On exit, `pred(lo)` is false, `pred(hi)` is true and
`hi = lo + 1`. So `hi` is a true index with a false index immediately to its
left: it is the smallest true index in range. ∎
:::

Read the proof once more with an eye on what it *needs*. It needs monotonicity —
used to claim the sentinels bracket a boundary at all. It needs the midpoint to
land strictly inside — used for termination. It needs `pred` to be deterministic
— asked twice, it must answer the same. Break any of those three and the code
still compiles and still runs in logarithmic time and still returns something
wrong. Most binary search bugs are one of these three assumptions quietly
failing, not an off-by-one.

:::note Where the false precondition comes from
If you cannot promise `pred(lo₀)` is false, use a sentinel index `-1` and never
evaluate it, as above. If you cannot promise `pred(hi₀)` is true — maybe nothing
in the array is `>= target` — then run with `hi₀ = n` and interpret a returned
`n` as "no such element". The invariant is then about the *virtual* index `n`,
where the predicate is defined to be true. That is not a hack; it is the reason
`bisect_left` can return `len(a)`.
:::

## What it costs

Each iteration does O(1) work plus one call to `pred`, and at least halves the
window. Starting from width `w = hi₀ - lo₀`, after `k` iterations the width is at
most `w / 2ᵏ`; the loop stops at width 1, so `k <= log₂ w`. The cost is
**Θ(log n) predicate calls**, with `n` the size of the search range, and O(1)
extra space. If `pred` itself costs `C`, the total is `Θ(C log n)` — the part
people forget when the predicate is a whole simulation.

Equivalently, as a recurrence: `T(w) = T(w/2) + O(1)`, whose solution is
`O(log w)` — case 2 of the master theorem with `a = 1`, `b = 2`, `f(w) = O(1)`.

And a lower bound, which is worth knowing because it tells you when *not* to
look for something faster: an algorithm that only compares the target against
array entries learns one bit per comparison, and must distinguish `n + 1`
possible answers (before the first element, between any two, after the last).
Distinguishing `n + 1` outcomes needs at least `log₂(n + 1)` bits, so no
comparison-based search beats `⌈log₂(n + 1)⌉` comparisons in the worst case.
Binary search meets it. You cannot do better without leaving the comparison
model — which is exactly what hashing ([[hash-tables]], O(1) expected) and
interpolation search (O(log log n) on uniform data) do.

## The implementation

Here is the template with the two standard specialisations, plus a check against
Python's own `bisect` so the claim is not just words. The reader is invited to
edit and run it.

```python run
from bisect import bisect_left, bisect_right


def first_true(lo, hi, pred):
    """Smallest x in (lo, hi] with pred(x) true. Caller: pred(lo) is false."""
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid
    return hi


def lower_bound(a, target):
    """First index whose value is >= target; len(a) if there is none."""
    return first_true(-1, len(a), lambda i: a[i] >= target)


def upper_bound(a, target):
    """First index whose value is > target; len(a) if there is none."""
    return first_true(-1, len(a), lambda i: a[i] > target)


def contains(a, target):
    i = lower_bound(a, target)
    return i < len(a) and a[i] == target


a = [2, 3, 5, 5, 5, 8, 13]
print("array          ", a)
print("lower_bound(5) ", lower_bound(a, 5), " count of 5s:", upper_bound(a, 5) - lower_bound(a, 5))
print("lower_bound(4) ", lower_bound(a, 4), "(insertion point for 4)")
print("lower_bound(99)", lower_bound(a, 99), "(past the end: 99 is not there)")
print("contains(8)    ", contains(a, 8), " contains(7):", contains(a, 7))

# agree with the standard library on every value that matters, including the
# ones between elements and outside the range
for t in range(0, 15):
    assert lower_bound(a, t) == bisect_left(a, t), t
    assert upper_bound(a, t) == bisect_right(a, t), t
print("agrees with bisect on 0..14")
```

Three details in there are doing real work.

`lo + (hi - lo) // 2` rather than `(lo + hi) // 2`. In Python integers do not
overflow, so the two are the same; in C++, Java or Rust they are not, and
`(lo + hi)` can wrap negative for large indices. This is the famous bug that sat
in the JDK's `Arrays.binarySearch` for nine years. Write the safe form always, so
your fingers write it when the language does care. (See [[big-integers]].)

`lower_bound` and `upper_bound` differ by a single character: `>=` versus `>`.
Every "count the occurrences", "find the first/last position", "insert while
keeping sorted" question is one of these two, and the difference between them is
that character. Do not memorise four functions; memorise one template and the
character.

`contains` is built on top rather than beside. A separate exact-match loop is a
second place for an off-by-one to live.

For the record, the exact-match form people usually learn first — the one with
`while lo <= hi` and three branches — is correct too. It is just a different
tradeoff: it stops early on a hit, but it cannot answer boundary questions, and
its three-way structure has twice the surface area for mistakes. If you keep one
template in your head, keep the half-open one.

## Variants you will meet

**Lower bound / upper bound.** Covered above. In Python, reach for
`bisect_left` / `bisect_right` when you are allowed to; they are the same thing
in C.

**Binary search on the answer.** The predicate is not a lookup, it is a
feasibility simulation: "with capacity `c`, do we finish in `d` days?" Search
over the answer space instead of over an array. This is the highest-yield
variant in interviews and has its own chapter: [[binary-search-on-answer]].

**Rotated sorted array.** The array is sorted then rotated, so the global
predicate is not monotone. The fix is to recover monotonicity locally: at each
step, one of the two halves is properly sorted, and you can decide in O(1)
whether the target lies inside it. See [[search-rotated]].

**Peak finding in a bitonic array.** "Is `a[i] < a[i+1]`?" is monotone — true
while climbing, false after the peak — even though the array is not sorted. This
is the clearest proof that the predicate, not the data, is what must be monotone.

```python run
def peak(a):
    """Index of a peak in an array that rises then falls."""
    lo, hi = -1, len(a) - 1          # pred(i) = "a[i] > a[i+1]"; true at the end
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if a[mid] > a[mid + 1]:
            hi = mid
        else:
            lo = mid
    return hi


for arr in ([1, 3, 7, 9, 4, 2], [5, 4, 3], [1, 2, 3, 9], [4]):
    i = peak(arr)
    print(arr, "-> peak at", i, "value", arr[i])
    assert (i == 0 or arr[i - 1] < arr[i]) and (i == len(arr) - 1 or arr[i] > arr[i + 1])
print("all peaks verified")
```

**Search on a real interval.** When the answer is a float, `hi - lo > 1` becomes
`hi - lo > eps` or, more robustly, a fixed count of iterations — 100 rounds
halves the interval by a factor of `2¹⁰⁰`, which is beyond double precision, so
it always converges and never spins. See [[numerical-stability]].

**Two-dimensional and implicit spaces.** A row-sorted, column-sorted matrix, or
"the k-th smallest sum of two sorted arrays", are binary searches over a value
range with a counting predicate. The array you search may not exist in memory at
all — only the predicate has to.

**Searching an unbounded range.** No `hi` to start with? Double: try 1, 2, 4, 8…
until the predicate turns true, then binary search the last interval. Finding the
bound costs `O(log answer)` and the search another `O(log answer)`. This is how
you binary search an infinite stream or an API with unknown length.

## Recognising it in a statement

Signals, roughly in order of reliability:

- **"minimise the maximum"**, **"maximise the minimum"**, **"smallest `k` such
  that…"**, **"the minimum capacity/speed/time to…"** — almost always
  [[binary-search-on-answer]].
- **"sorted"** plus **"find / insert / count"** — lower or upper bound.
- **"first position where…"**, **"last position where…"** — the boundary form,
  straight off the template.
- The constraint line reads `1 <= n <= 10^5` but the obvious algorithm is
  `O(n²)`, and there is a natural candidate answer you can *test* in `O(n)` or
  `O(n log n)`. `n log n` is the shape of the intended solution, and the `log` is
  often a binary search.
- The answer is an integer in a known range, and checking one is easy while
  constructing one is hard. Testing beats constructing — that asymmetry is the
  whole hint.

And the anti-signal: if the property you need is not monotone — "is there an
element exactly equal to the average?" — binary search does not apply, however
sorted the array is.

## Traps

**Losing monotonicity without noticing.** The predicate must be monotone *over
the range you search*. `a[mid] >= target` is monotone only if `a` is sorted;
after a rotation it is not. Check the shape, not the vibe.

**`lo = mid` with an inclusive window.** In a `while lo < hi` loop with
`mid = (lo + hi) // 2`, assigning `lo = mid` can leave `lo` unchanged when
`hi = lo + 1`, and the loop spins forever. The half-open template avoids this by
construction: it exits at width 1 and `mid` is always strictly inside. If you
insist on a different template, prove the window shrinks — do not hope.

**Returning `mid` on a hit.** Fine for "does it exist", wrong for "where does it
start". Duplicates are where this bites.

**Forgetting the empty and the out-of-range answer.** `lower_bound` on an empty
array must return 0; on a target larger than everything, `len(a)`. Both fall out
of the sentinels if you use them, and both need a special case if you do not.

**An expensive predicate inside the loop.** `O(log n)` calls to an `O(n log n)`
check is `O(n log²n)`, which can be slower than a linear scan for small `n`.
Cost the predicate before you celebrate.

**Floating point equality.** `while lo < hi` on floats can never terminate.
Fixed iteration count, always.

**Mixing up the two bounds under pressure.** The cure is not more memorisation;
it is writing the predicate down in words first — "the first index where the
value is at least the target" — and then transcribing it literally.

```python run
# the three classic wrong answers, side by side with the right one
a = [1, 2, 2, 2, 3]

def wrong_returns_any_hit(a, t):          # answers a different question
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == t:
            return mid                     # which 2 is this?
        if a[mid] < t:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def right(a, t):
    lo, hi = -1, len(a)
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if a[mid] >= t:
            hi = mid
        else:
            lo = mid
    return hi

print("array            ", a)
print("first index of 2 :", right(a, 2), "(correct)")
print("'any hit' returns:", wrong_returns_any_hit(a, 2), "- a 2, but not the first one")
print("insert point of 4:", right(a, 4), "= len(a), meaning 'past the end'")
assert right(a, 2) == 1 and right(a, 4) == len(a) and right([], 1) == 0
print("empty array      :", right([], 1), "(no crash, no special case)")
```

## What to memorise

Almost nothing. One template, one sentence, one habit.

**The template**, which you should be able to type without thinking:

```python
lo, hi = -1, n            # lo: a known 'no'.  hi: a known 'yes'.
while hi - lo > 1:
    mid = lo + (hi - lo) // 2
    if pred(mid):
        hi = mid
    else:
        lo = mid
# hi is the first yes; lo is the last no
```

**The sentence** that turns a problem into that template: *"What yes/no question
about a candidate answer is false at the bottom, true at the top, and cheap to
check?"* If you can answer that, the code is mechanical. If you cannot, binary
search is not the tool.

**The habit**: after writing the loop, say out loud what `lo` and `hi` mean.
Not "left and right" — the actual claim: "`lo` is an index I have proven is too
small". If you cannot say it, the loop is guesswork, and it will be wrong on
duplicates or on the empty case.

Two numbers worth carrying: `log₂(10⁶) ≈ 20` and `log₂(10⁹) ≈ 30`. A binary
search over a billion candidates is thirty predicate calls. That is why
"minimise the maximum over `10⁹` possible answers" is not scary.

## Check yourself

:::check
The array is `[1, 3, 3, 3, 7]` and you want the number of 3s using only the
template. What two calls do you make, and why is the answer their difference?
--
`upper_bound(a, 3) - lower_bound(a, 3)` — that is `4 - 1 = 3`.

`lower_bound` is the first index with value `>= 3`, i.e. where the run of 3s
begins. `upper_bound` is the first index with value `> 3`, i.e. one past where
the run ends. The elements between them are exactly the 3s, and in a sorted
array they are contiguous, so subtracting the indices counts them.
:::

:::check
Someone writes `while lo < hi:` with `mid = (lo + hi) // 2` and, in one branch,
`lo = mid`. Give a concrete input where this never terminates, and explain it in
terms of the termination argument in the proof.
--
Take `lo = 0`, `hi = 1`. Then `mid = 0`, and if the branch taken is `lo = mid`,
`lo` stays 0 and `hi` stays 1 — the state is unchanged, so the same branch is
taken forever.

The proof's termination step required the window width to *strictly* decrease,
which it guaranteed by showing `lo < mid < hi`. With `hi - lo == 1` there is no
integer strictly between them, so `mid` collides with `lo` and the width does not
move. The half-open template dodges this by stopping at width 1 — it never enters
the body in that state.
:::

:::check
You are asked for the smallest boat capacity that ships all packages within `d`
days, packages must be shipped in order. Why is binary search valid here, and
what exactly is the predicate?
--
The predicate is `feasible(c)` = "with capacity `c`, greedily filling the boat in
order, are the packages shipped in at most `d` days?"

It is monotone: a bigger boat can copy any schedule a smaller boat used (and
possibly do better), so if `c` works then every `c' > c` works. That is the only
property binary search needs — the array of answers is `no … no yes … yes`.

The search range is `[max(weights), sum(weights)]`: below the largest package
nothing fits, and the total always works in one day. Each `feasible` call is
`O(n)`, so the whole thing is `O(n log(sum))`. Full treatment in
[[binary-search-on-answer]].
:::

:::check
Why can no comparison-based algorithm beat `⌈log₂(n + 1)⌉` comparisons for
searching a sorted array of `n` elements?
--
Each comparison has two outcomes, so after `k` comparisons the algorithm can
have followed at most `2ᵏ` distinct execution paths and therefore can produce at
most `2ᵏ` distinct answers. A search must distinguish `n + 1` outcomes — the
target could belong before element 0, between any adjacent pair, or after the
last. So `2ᵏ >= n + 1`, giving `k >= log₂(n + 1)`.

This is an information argument, not a cleverness argument: it holds for any
algorithm in the comparison model, no matter how it chooses its probes. Beating
it requires a different model — hashing uses the key's value directly,
interpolation search assumes a distribution.
:::

:::check
A candidate says "the array has to be sorted for binary search to work". Where
is that wrong, and what is the correct statement?
--
It confuses a common source of the property with the property itself. The
correct statement is: **the predicate must be monotone over the search range**.

Sorted data makes `a[i] >= t` monotone, which is why the two get conflated. But
peak-finding in a bitonic array, searching a rotated array after recovering local
order, and binary search on a feasibility check over an answer range all work on
unsorted — or entirely virtual — data. Conversely, a sorted array with a
non-monotone predicate ("is `a[i]` even?") gives binary search nothing to bite.
:::
