# Kadane's Algorithm

> Every subarray ends somewhere. Kadane never searches for a subarray — it walks
> the array asking one question at each position, "what is the best run ending
> right here?", and that question answers itself from the position before.

## When you reach for it

The shape is narrow and it is easy to spot. You are given a sequence. You must
choose a **contiguous** stretch of it — a subarray, not a subset and not a
subsequence — and the score of a stretch is the **sum** of its elements. You
want the best score. Nothing constrains which stretch you may pick: any start,
any end, any length.

That is the whole trigger. Six problems in this bank are exactly it or a short
walk from it — *Maximum Subarray Sum* appears three times over (from Safe
Security, from Omnissa, and as *Maximum Subarray* from Squarepoint Capital),
and then it starts mutating: *Maximum Subarray Sum with Equal Endpoints*,
*Maximum Subarray Sum with Length at Most K*, *Maximum Subarray Sum After
Swaps*. The topic sits at rank #96 of 150 by problem count here, which
undersells it: it is small, it is asked constantly, and its recurrence is the
cleanest example of one-dimensional DP you will meet. If [[dp-1d]] ever felt
abstract, this is the concrete case to hold on to.

The shapes that make it the **wrong** tool are worth learning at the same time,
because they look almost identical on the page:

- **"subsequence" instead of "subarray."** If you may skip elements, the answer
  to "maximum sum" is trivially the sum of the positives, and to anything harder
  (longest increasing, for instance) it is a different DP entirely.
- **A cap or a floor on the length.** "At most K elements" breaks the recurrence
  in a way we will prove precisely below; that is Oracle's *Maximum Subarray Sum
  with Length at Most K*, and it is rated hard for exactly this reason.
- **A constraint tying the two ends together.** *Maximum Subarray Sum with Equal
  Endpoints* demands `nums[i] == nums[j]`. The stretch is still contiguous, but
  the choice of end no longer summarises the past in one number.
- **Product instead of sum.** Multiplication is not monotone in the way addition
  is — a negative factor turns your worst running value into your best — so one
  carried number is not enough.
- **All elements are positive.** Then the answer is the whole array, and if the
  problem is still interesting it is really a [[sliding-window]] problem in
  disguise ("longest window with sum at most S").

## The idea

Hold one number in your hand as you walk left to right. Call it the **carry**:
the largest sum of any subarray that ends exactly at the element you are
standing on.

At each new element `x` you face precisely one decision, and it has exactly two
options:

- **extend** the run you were already building, scoring `carry + x`; or
- **start over** at `x`, scoring `x` alone.

There is no third option, because every subarray ending at the current position
either has length one or has a predecessor ending at the previous position. So
the new carry is `max(x, carry + x)`, and — rearranged — that is
`x + max(carry, 0)`: *take this element, and bring the past along only if the
past is worth bringing*.

<svg viewBox="0 0 560 190" role="img" aria-label="the two-option decision at each position: extend the previous run or start fresh">
  <g>
    <rect x="30" y="30" width="180" height="46" rx="6"/>
    <text x="48" y="58">carry at i-1</text>
    <rect x="30" y="112" width="180" height="46" rx="6"/>
    <text x="52" y="140">nothing (start over)</text>
    <rect class="fill" x="360" y="70" width="170" height="46" rx="6"/>
    <text x="380" y="98">carry at i</text>
    <line x1="210" y1="53" x2="360" y2="86"/>
    <line x1="210" y1="135" x2="360" y2="102"/>
    <text x="232" y="52">+ a[i]</text>
    <text x="238" y="150">a[i] alone</text>
    <text x="30" y="182">one number in, one number out; the winner is the larger</text>
  </g>
</svg>

Alongside the carry, keep a second number: the best carry you have ever seen.
The carry can and will fall — a big negative element flattens it — but the
record of the best never does. At the end, the record is the answer.

That is it. Two numbers, one pass, no array of DP states at all.

:::note Why the carry is enough
The carry is a *summary* of everything to the left. The reason one number
suffices is that adding `a[i]` shifts the sum of every candidate subarray ending
at `i-1` by the same amount. A common shift preserves order, so the best
candidate before the shift is still the best candidate after it. Whenever you
meet a Kadane-like problem that will not collapse to one number, it is because
that common-shift property has been broken.
:::

## Worked by hand

Take the array that every textbook uses, because it exercises every branch:

```
index   0   1   2   3   4   5   6   7   8
value  -2   1  -3   4  -1   2   1  -5   4
```

Initialise with the first element: `carry = -2`, `best = -2`, and remember that
the current run started at index 0. Then walk.

| i | a[i] | carry + a[i] | a[i] | decision | carry | run starts at | best |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | -2 | — | — | initialise | -2 | 0 | -2 |
| 1 | 1 | -1 | 1 | start over | 1 | 1 | 1 |
| 2 | -3 | -2 | -3 | extend | -2 | 1 | 1 |
| 3 | 4 | 2 | 4 | start over | 4 | 3 | 4 |
| 4 | -1 | 3 | -1 | extend | 3 | 3 | 4 |
| 5 | 2 | 5 | 2 | extend | 5 | 3 | 5 |
| 6 | 1 | 6 | 1 | extend | 6 | 3 | **6** |
| 7 | -5 | 1 | -5 | extend | 1 | 3 | 6 |
| 8 | 4 | 5 | 4 | extend | 5 | 3 | 6 |

The answer is 6, from `a[3..6] = [4, -1, 2, 1]`.

<svg viewBox="0 0 580 170" role="img" aria-label="the nine-element array with the winning stretch from index 3 to index 6 highlighted">
  <g>
    <rect x="20" y="40" width="60" height="40" rx="4"/>
    <rect x="80" y="40" width="60" height="40" rx="4"/>
    <rect x="140" y="40" width="60" height="40" rx="4"/>
    <rect class="fill" x="200" y="40" width="60" height="40" rx="4"/>
    <rect class="fill" x="260" y="40" width="60" height="40" rx="4"/>
    <rect class="fill" x="320" y="40" width="60" height="40" rx="4"/>
    <rect class="fill" x="380" y="40" width="60" height="40" rx="4"/>
    <rect x="440" y="40" width="60" height="40" rx="4"/>
    <rect x="500" y="40" width="60" height="40" rx="4"/>
    <text x="38" y="65">-2</text>
    <text x="105" y="65">1</text>
    <text x="158" y="65">-3</text>
    <text x="225" y="65">4</text>
    <text x="278" y="65">-1</text>
    <text x="345" y="65">2</text>
    <text x="405" y="65">1</text>
    <text x="458" y="65">-5</text>
    <text x="525" y="65">4</text>
    <line x1="200" y1="92" x2="440" y2="92"/>
    <line x1="200" y1="92" x2="200" y2="104"/>
    <line x1="440" y1="92" x2="440" y2="104"/>
    <text x="256" y="120">sum = 6</text>
    <line x1="230" y1="30" x2="230" y2="14"/>
    <text x="150" y="12">carry restarts here</text>
    <text x="20" y="152">indices 7 and 8 are visited but never improve the record</text>
  </g>
</svg>

Four things the trace shows that the code alone does not.

**The carry restarts only twice**, at indices 1 and 3, and both times for the
same reason: the carry it would have extended was negative. `carry + x < x`
holds exactly when `carry < 0`. So "start over when the running sum has gone
negative" and "take the larger of the two options" are the same rule wearing
different clothes. The second phrasing is better because it survives into
variants where the first one does not.

**The best answer is found in the middle and then abandoned.** At index 7 the
carry drops from 6 to 1 and never recovers. If you returned the carry instead of
the record you would report 5. This is the single most common bug in the
algorithm, and the trace makes it obvious in a way that reading code does not.

**The carry is allowed to be negative.** At index 2 it is -2 and we keep it
rather than resetting to zero, because at that moment -2 genuinely is the best
sum of a subarray ending at index 2 — every candidate there is bad, and the
algorithm's job is to report the truth, not a convenient zero. Clamping the
carry at zero is a different algorithm that answers a different question, and we
will see it break in **Traps**.

**The run's start index comes free.** You only update it on the step where you
start over. No second pass, no storing the whole DP table. Squarepoint's
*Maximum Subarray* and Safe Security's *Maximum Subarray Sum* both ask only for
the sum, but interviewers follow up with "which subarray?" often enough that you
should be able to add this line without thinking.

## Why it is correct

Write `sum(j..i)` for `a[j] + a[j+1] + … + a[i]`, and define, for each index `i`,

    E(i) = max { sum(j..i) : 0 <= j <= i }

— the best subarray ending exactly at `i`. The claim is that Kadane computes
every `E(i)` in order and that the answer is the largest of them.

:::proof Correctness of Kadane's algorithm
**Claim 1 (the recurrence).** `E(0) = a[0]`, and for `i >= 1`,

    E(i) = max( a[i],  E(i-1) + a[i] ).

*Proof.* Let `S_i` be the set of non-empty subarrays ending at `i`, that is
`{ [j..i] : 0 <= j <= i }`. Partition `S_i` by whether `j = i`:

- the single subarray `[i..i]`, of sum `a[i]`;
- the subarrays `[j..i]` with `j < i`.

For the second group, `sum(j..i) = sum(j..i-1) + a[i]`, and the map
`[j..i] ↦ [j..i-1]` is a bijection from that group onto `S_{i-1}`: it is defined
for every `j < i`, it is injective, and every element of `S_{i-1}` is hit. A
bijection that shifts every value by the same constant `a[i]` preserves the
maximum, so the best sum in the second group is `E(i-1) + a[i]`. The maximum
over a partition is the maximum of the parts' maxima, which gives the claim.
When `i = 0` the second group is empty, leaving `E(0) = a[0]`. ∎

**Claim 2 (the global answer).** Every non-empty subarray ends at exactly one
index, so the set of all non-empty subarrays is the *disjoint* union
`S_0 ∪ S_1 ∪ … ∪ S_{n-1}`. Hence

    max over all non-empty subarrays  =  max { E(i) : 0 <= i < n }. ∎

**Invariant.** Immediately after the loop body has processed index `i`:

    cur  = E(i)          and          best = max { E(k) : 0 <= k <= i }.

**Base case.** Before the loop, `cur = best = a[0]`. By Claim 1, `E(0) = a[0]`,
and the maximum over the single index 0 is `a[0]`. The invariant holds for
`i = 0`.

**Inductive step.** Suppose the invariant holds after index `i-1`, so on entry
to the body for index `i` we have `cur = E(i-1)` and
`best = max{E(k) : k <= i-1}`. The body computes

    cur'  = max(a[i], cur + a[i]) = max(a[i], E(i-1) + a[i]) = E(i)

by Claim 1 and the induction hypothesis, and then

    best' = max(best, cur') = max( max{E(k) : k <= i-1}, E(i) )
          = max{E(k) : k <= i}.

Both halves of the invariant are restored.

**Termination.** The loop is a bounded iteration over `i = 1 … n-1`; the body
changes no loop variable and contains no inner loop, so it performs exactly
`n-1` iterations and stops.

**Conclusion.** On exit the invariant holds for `i = n-1`, so
`best = max{E(k) : 0 <= k <= n-1}`, which by Claim 2 is the maximum sum over all
non-empty subarrays. ∎
:::

Now read the proof again and list what it actually leaned on, because that list
is where every variant and every bug lives.

1. **Additivity with a shift that does not depend on the start.**
   `sum(j..i) = sum(j..i-1) + a[i]` for *every* `j`. This is the one load-bearing
   fact. It is why a single number can summarise an unbounded number of
   candidates. Replace sums with products and the shift becomes a multiplication
   by `a[i]`, which reverses order when `a[i] < 0` — the maximum of the shifted
   set is then the image of the *minimum*, not the maximum, and one carried
   number no longer suffices.
2. **Non-emptiness.** The maximum is over non-empty subarrays, which is why the
   base case is `E(0) = a[0]` and not `0`. Omnissa's statement spells this out:
   "You must select at least one element, even when all values are negative."
   If the empty subarray were allowed, the answer would be `max(0, …)` and the
   initialiser would change.
3. **No constraint on the start index `j`.** The bijection in Claim 1 requires
   that *every* subarray ending at `i-1` can be legally extended to one ending at
   `i`. Cap the length at `K` and this fails: a length-`K` subarray ending at
   `i-1` has no extension, so `E(i-1)` may be achieved by a candidate that is not
   available any more, and the recurrence reports a sum no legal subarray has.
4. **Exact arithmetic.** The invariant is a statement about integers. A fixed
   width accumulator that silently wraps makes the invariant false while the
   program still runs and still returns something.
5. **The array is read in place, left to right.** Nothing in the proof permits
   reordering. Infosys' *Maximum Subarray Sum After Swaps* changes this premise,
   and the title alone should stop your fingers before they type
   `cur = max(x, cur + x)`.

:::note The same algorithm wearing prefix sums
Let `P[0] = 0` and `P[k] = a[0] + … + a[k-1]`. Then
`sum(j..i) = P[i+1] - P[j]`, so `E(i) = P[i+1] - min{ P[j] : 0 <= j <= i }`, and
the answer is `max over i of that`. Kadane is exactly this computation with the
running minimum of `P` folded into a single variable. The two views are
interchangeable, and the prefix view is the one that generalises: it is how you
attack *Maximum Subarray Sum with Equal Endpoints* and *…with Length at Most K*.
See [[prefix-sums]].
:::

## What it costs

**Time.** The loop runs `n-1` times. Each iteration performs one addition, two
comparisons and at most three assignments — a fixed amount of work with no
hidden allocation, no hashing, no copying of slices. Total: **Θ(n)**, with a
constant small enough that the pass is memory-bound rather than compute-bound.

That number only impresses once you count what it replaced. A non-empty subarray
is determined by its pair of endpoints `0 <= j <= i < n`, so there are

    C(n+1, 2) = n(n+1)/2

of them. Summing each one from scratch costs its length, so the naive triple
loop does

    Σ (over lengths L = 1..n) L · (n - L + 1)  =  n(n+1)(n+2)/6  =  Θ(n³)

additions. Precomputing prefix sums makes each subarray's sum O(1) and drops
this to **Θ(n²)** — for Omnissa's `n <= 20000` that is 2·10⁸ pairs, already too
slow, and for Google's `n <= 100000` it is 5·10⁹, hopeless. Kadane evaluates
`n` of those `n(n+1)/2` candidates explicitly and *proves away* the rest: at
index `i` it discards every subarray ending at `i` except the best one, and
Claim 1 is the proof that discarding them is safe.

The divide-and-conquer solution is worth costing too, because it is the answer
interviewers expect when they say "now do it recursively". Split the array in
half; the best subarray lies entirely left, entirely right, or straddles the
midpoint, and the straddling case is a linear scan outward from the middle. That
gives

    T(n) = 2 T(n/2) + Θ(n),      T(1) = Θ(1)

which is the merge-sort recurrence: `a = 2`, `b = 2`, `f(n) = Θ(n) = Θ(n^{log_b a})`,
so case 2 of the master theorem gives **Θ(n log n)**. Strictly worse than
Kadane, and it needs `Θ(log n)` stack. See [[divide-and-conquer]].

**Space.** Θ(1). Two integers, or five if you want the endpoints. Nothing scales
with `n` — you can run Kadane over a stream you are not allowed to store.

**The lower bound**, which tells you to stop optimising. Suppose an algorithm
returns an answer without reading `a[i]` for some `i`. Set `a[i]` to a value
larger than the sum of the absolute values of the whole array; the true answer
changes, but the algorithm's output cannot, so it is wrong on one of the two
inputs. Every correct algorithm must read every element: **Ω(n)**. Kadane meets
it.

**The cost people forget** is the width of the accumulator. In Omnissa's
constraints, `n <= 20000` and `|nums[i]| <= 10^6`, so a subarray sum can reach
2·10¹⁰ — comfortably past the 2.1·10⁹ ceiling of a signed 32-bit integer, which
is why the statement says "signed 64-bit". In the Google problem it is worse:
`10^5 · 10^9 = 10^14`. Python's integers are unbounded so this is free here (see
[[big-integers]]), but in C++ or Java an `int` accumulator turns a correct
algorithm into a wrong one without a single warning.

## The implementation

```python run
import random


def max_subarray(a):
    """Largest sum of a non-empty contiguous subarray, with its endpoints."""
    cur = best = a[0]
    cur_start = best_lo = best_hi = 0
    for i in range(1, len(a)):
        x = a[i]
        if cur + x < x:                    # extending is worse than starting over
            cur, cur_start = x, i
        else:
            cur = cur + x
        if cur > best:                     # the record only ever moves up
            best, best_lo, best_hi = cur, cur_start, i
    return best, best_lo, best_hi


def brute(a):
    return max(sum(a[i:j + 1]) for i in range(len(a)) for j in range(i, len(a)))


a = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
s, lo, hi = max_subarray(a)
print("array    ", a)
print("best sum ", s, "from a[%d..%d] =" % (lo, hi), a[lo:hi + 1])
assert (s, lo, hi) == (6, 3, 6)

neg = [-8, -3, -6, -2, -5]
s2, lo2, hi2 = max_subarray(neg)
print("all negative", neg, "->", s2, "= the least bad single element, a[%d]" % lo2)
assert s2 == -2 == brute(neg)

one = [7]
print("single element", one, "->", max_subarray(one))
assert max_subarray(one) == (7, 0, 0)

random.seed(7)
for _ in range(500):
    n = random.randint(1, 9)
    arr = [random.randint(-9, 9) for _ in range(n)]
    s, lo, hi = max_subarray(arr)
    assert s == brute(arr), arr
    assert s == sum(arr[lo:hi + 1]), arr
print("500 random arrays: the sum matches brute force AND the endpoints are real")
```

Three lines are doing the work.

`cur = best = a[0]`, with the loop starting at index 1. This is the whole
handling of the "all values negative" case. Initialising to `0` or to
`-infinity` and looping from index 0 is a live choice — `-infinity` is fine,
`0` is a bug — but seeding with the first element states the non-emptiness
assumption in the code itself, where you can see it.

`if cur + x < x` rather than `if cur < 0`. The two conditions are algebraically
identical, and the second is shorter. Prefer the first anyway: it is the literal
transcription of "compare the two candidates", so when a variant changes what
the candidates are — a product, a capped length, a second dimension — the line
you have to edit is already in the right shape.

`if cur > best` **after** `cur` has been updated, never before. The record must
be taken on the new carry; taking it on the old one loses the last element's
contribution. And the comparison is strict, so `best_lo`/`best_hi` report the
*earliest* optimal subarray when there are ties. Which tie an interviewer wants
is worth one question before you start.

The random cross-check against `brute` is not decoration. Kadane is four lines
and every one of them has a plausible-looking wrong version; a differential test
against an obviously-correct quadratic reference is the cheapest way to know
which version you actually typed ([[testing-your-code]]).

## Variants you will meet

**Minimum subarray sum.** Negate every element, run Kadane, negate the result.
Do not write a second copy of the loop with the comparisons flipped.

**Empty subarray allowed.** Initialise `cur = best = 0` and loop from index 0.
The answer is then never negative. Check the statement: Omnissa's forbids this
explicitly, and most do.

**Maximum product subarray.** A negative element swaps the roles of your best
and worst running values, so carry both: the largest and the smallest product
ending here, each chosen from `{x, hi·x, lo·x}`. This is the clearest
illustration of assumption 1 from the proof failing.

**Circular array.** The best stretch may wrap around the end. Either it does not
wrap, in which case ordinary Kadane finds it, or it does, in which case its
complement is a non-wrapping subarray and the answer is `total − (minimum
subarray sum)`. The edge case is an all-negative array, where the minimum
subarray is the whole array and its complement is empty — which the statement
forbids, so fall back to the linear answer.

```python run
def max_subarray(a):
    cur = best = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def max_product(a):
    """A negative factor flips the order, so carry the minimum as well."""
    hi = lo = best = a[0]
    for x in a[1:]:
        cands = (x, hi * x, lo * x)
        hi, lo = max(cands), min(cands)
        best = max(best, hi)
    return best


def max_circular(a):
    total, best_lin = sum(a), max_subarray(a)
    worst = -max_subarray([-x for x in a])       # minimum subarray sum
    if worst == total:                           # its complement would be empty
        return best_lin
    return max(best_lin, total - worst)


def brute_circular(a):
    n = len(a)
    return max(sum(a[i:i + L]) if i + L <= n else sum(a[i:]) + sum(a[:i + L - n])
               for i in range(n) for L in range(1, n + 1))


print("product  [2, 3, -2, 4]  ->", max_product([2, 3, -2, 4]), "(2 * 3; the -2 poisons any run containing it)")
print("product  [-2, 3, -4]    ->", max_product([-2, 3, -4]), "(all three: two negatives)")
print("product  [-2, 0, -1]    ->", max_product([-2, 0, -1]), "(the zero is the best you can do)")
assert max_product([2, 3, -2, 4]) == 6
assert max_product([-2, 3, -4]) == 24
assert max_product([-2, 0, -1]) == 0

print("circular [5, -3, 5]     ->", max_circular([5, -3, 5]), "(wraps: 5 + 5)")
print("circular [-3, -2, -3]   ->", max_circular([-3, -2, -3]), "(all negative: no wrap)")
import random
random.seed(11)
for _ in range(400):
    arr = [random.randint(-6, 6) for _ in range(random.randint(1, 8))]
    assert max_circular(arr) == brute_circular(arr), arr
print("400 random arrays: circular Kadane matches brute force")
```

**Length at most K.** Oracle's *Maximum Subarray Sum with Length at Most K*.
Assumption 3 of the proof is gone, so go back to the prefix-sum view:
`answer = max over i of ( P[i+1] − min{ P[j] : i+1−K <= j <= i } )`. That inner
term is a sliding-window minimum, which a [[monotonic-deque]] delivers in
amortised O(1) per step, for O(n) overall. Kadane is the special case `K = n`,
where the window never evicts anything and the deque collapses to one variable.

**Equal endpoints.** Google's *Maximum Subarray Sum with Equal Endpoints*
requires `nums[i] == nums[j]`. Prefix sums again: for each `j`, you want
`P[j+1] − min{ P[i] : i <= j and nums[i] == nums[j] }`, so keep a hash map from
value to the smallest prefix sum seen at a position holding that value, and
update it as you go ([[hash-tables]]). One pass, O(n). The lesson is structural:
when the constraint couples the two ends, the carry stops being a single number
and becomes one number *per key*.

**After swaps.** Infosys' *Maximum Subarray Sum After Swaps* changes assumption
5 — the array is no longer fixed in place. Read that statement twice; what
exactly may be swapped, and how many times, decides whether this is a greedy
rearrangement, a [[sorting]] problem, or something else entirely.

**Maximum sum rectangle in a matrix.** Fix a top row and a bottom row, collapse
the rows between them into a single array of column sums, and run Kadane on it.
`O(rows² · cols)`. This is the classic reason to actually know Kadane rather
than to know that `max subarray` has a library call. See [[dp-2d]].

**Two (or k) non-overlapping subarrays.** Compute `bestPrefix[i]` by a forward
Kadane and `bestSuffix[i]` by a backward one, then take
`max over i of bestPrefix[i] + bestSuffix[i+1]`. For general `k` it becomes a
two-dimensional DP over (index, subarrays used).

**As a DP table.** Everything above is [[dp-1d]] with the table thrown away.
Writing `E` as a full array first, then noticing that entry `i` reads only entry
`i-1`, is the standard route from recurrence to O(1) space.

## Recognising it in a statement

Signals, in descending order of reliability:

- **"contiguous subarray"** together with **"sum"** and **"maximum" /
  "largest"**. That is the phrase triple; all three of this bank's plain
  *Maximum Subarray Sum* problems contain it verbatim. If you see it, write the
  four lines.
- **"You must select at least one element, even when all values are negative."**
  This sentence exists only because the writer knows about the zero-initialised
  bug. It is a tell that they are testing precisely that.
- **"return the sum"** rather than "return the indices" — the problem is scored
  on the value, so no reconstruction is needed, though it is free anyway.
- **Constraints around `10^5`–`10^6` with an obvious `O(n²)` pair-scan.** The
  intended solution is linear, and for a maximum-over-all-windows question that
  almost always means a carry.
- **The array contains both positive and negative values, and this is stressed.**
  If everything were positive the problem would be trivial; the mix is the
  problem.

The anti-signals, which matter more:

- **"subsequence", "any elements", "not necessarily adjacent"** — not this.
- **"exactly k elements", "at least k", "at most k"** — the recurrence does not
  survive; prefix sums plus a window minimum do.
- **"product", "bitwise AND", "maximum element of the window"** — the score is
  not additive with a start-independent shift, so recheck assumption 1 before
  reusing the shape. A non-invertible score usually needs a [[monotonic-deque]]
  or a [[segment-tree]] instead.
- **"after rearranging / swapping / removing one element"** — a different
  problem that happens to mention subarrays. Removing at most one element, for
  instance, needs two carries (with a deletion and without).

## Traps

**Returning the carry instead of the record.** The symptom is an answer that is
correct whenever the best stretch happens to touch the last element, and too
small otherwise. It passes the first sample and fails the second.

**Zero-initialising on an all-negative array.** The symptom is a returned `0` on
inputs where every element is negative — a wrong answer that looks suspiciously
tidy. Note that `cur = max(0, cur + x)` has the same effect even if `best`
starts at `a[0]`: the carry can never be negative, so `best` can only be raised
by a non-negative carry.

:::warn The two initialisers are not interchangeable
`cur = best = a[0]` answers "best non-empty subarray". `cur = best = 0` answers
"best possibly-empty subarray". They differ on exactly one class of input — all
negative — which is exactly the class the test suite will contain.
:::

```python run
def right(a):
    cur = best = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def wrong_zero_init(a):            # silently allows the empty subarray
    cur = best = 0
    for x in a:
        cur = max(0, cur + x)
        best = max(best, cur)
    return best


def wrong_returns_cur(a):          # forgets the best may end mid-array
    cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
    return cur


def wrong_product(a):              # Kadane's shape, wrong algebra
    cur = best = a[0]
    for x in a[1:]:
        cur = max(x, cur * x)
        best = max(best, cur)
    return best


neg = [-4, -1, -7]
print("all negative       ", neg)
print("  right            ", right(neg))
print("  zero-initialised ", wrong_zero_init(neg), "<- the empty subarray, which the statement forbids")
assert right(neg) == -1 and wrong_zero_init(neg) == 0

tail = [3, 4, -20, 1]
print("best is not at the end", tail)
print("  right            ", right(tail))
print("  returns the carry", wrong_returns_cur(tail), "<- only the run that survived to index 3")
assert right(tail) == 7 and wrong_returns_cur(tail) == 1

prod = [-2, 3, -4]
print("product            ", prod, "-> the answer is 24 = (-2) * 3 * (-4)")
print("  Kadane's shape   ", wrong_product(prod), "<- it discarded the negative it needed")
assert wrong_product(prod) == 3
```

**Off-by-one in the reported start index.** Tracking the start with
`if cur < 0: cur, start = 0, i + 1` sets it *before* consuming `a[i]`, a
different convention from the implementation above. Mixing the two gives an
index one to the left of the truth, which still produces a plausible slice. Test
the endpoints, not just the sum.

**Overflow in a fixed-width language.** Symptom: correct on samples, wrong on
the large hidden test, often with a large negative output. Cure: declare the
accumulator 64-bit before you write the loop, not after the verdict.

**Reusing the recurrence under a new constraint without rechecking the proof.**
Length caps, equal endpoints, at-most-one-deletion, circularity — each one
invalidates a specific line of Claim 1. The fastest way to know which is to ask
"is every subarray ending at `i-1` still legally extendable, and does extending
still add the same constant to all of them?" If either answer is no, the carry
must grow — into two carries, or a deque, or a map.

**Assuming the empty array is impossible.** Every statement here promises
`1 <= nums.length`, so `a[0]` is safe. When a wrapper function does not promise
it, `max_subarray([])` raises `IndexError`. Decide and document rather than
discover ([[edge-cases]]).

## What to memorise

The template, which should take you ten seconds:

```python
cur = best = a[0]
for x in a[1:]:
    cur = max(x, cur + x)     # extend, or start over here
    best = max(best, cur)     # the record never falls
return best
```

The sentence that turns a problem into it: *"What is the best answer that ends
exactly at position i, and can it be computed from the best answer ending at
i-1 alone?"* If yes, you have a carry and the pass is linear. If it needs two
numbers, carry two. If it needs a whole window of numbers, you have a
[[monotonic-deque]] problem instead.

The habit: **say out loud whether the empty subarray is allowed before you type
the initialiser.** That single sentence removes the most common wrong answer in
the topic.

Three numbers worth carrying: there are `n(n+1)/2` subarrays, so a pair-scan is
quadratic and dies around `n = 10^4`; the divide-and-conquer version is
`Θ(n log n)` and is the right answer to "do it recursively"; and a sum of
`10^5` elements of magnitude `10^9` is `10^14`, which needs 64 bits.

## Check yourself

:::check
Why does the algorithm keep a separate `best`, instead of simply returning `cur`
at the end? Answer in terms of the invariant, not in terms of a failing example.
--
The invariant says `cur = E(i)` — the best subarray ending *exactly* at the
current index. But Claim 2 says the answer is `max{E(i)}` over all `i`, not
`E(n-1)`. Returning `cur` answers the question "what is the best subarray ending
at the last position?", which is a strictly harder constraint than the problem
asks for, so it can only under-report.

`best` is the running maximum that turns the pointwise quantity `E(i)` into the
global one. On `[3, 4, -20, 1]` the gap is `7` versus `1`.
:::

:::check
Someone says: "Length at most K is easy — just reset the carry whenever the
current run reaches K elements." Where exactly are they wrong?
--
They are wrong at Claim 1's bijection. The recurrence is valid only because
every subarray ending at `i-1` can be extended to one ending at `i`. Under a cap
of `K`, the subarray achieving `E(i-1)` might already have length `K`, so it has
no extension — but the second-best candidate ending at `i-1`, of length `K-1`,
does. Their fix throws away that candidate too: resetting at length `K`
discards *all* runs, including short ones that started later and are still
legal.

Concretely with `K = 2` and `a = [5, 1, 5]`: the best legal answer is `6`
(`[1, 5]` or `[5, 1]`). A carry that resets after two elements builds `5`, then
`6`, then resets to `5` — it never considers `[1, 5]` as a continuation from a
shorter run. The correct approach abandons the single carry entirely:
`max over i of P[i+1] − min{P[j] : i+1−K <= j <= i}`, with the window minimum
kept by a [[monotonic-deque]].
:::

:::check
Someone claims Kadane extends to maximum *product* by changing `+` to `*`:
`cur = max(x, cur * x)`. Give a three-element counterexample and name the
assumption from the proof that they broke.
--
`[-2, 3, -4]`. The true answer is `24`, the product of all three. Their version
computes `cur = -2`, then `max(3, -6) = 3`, then `max(-4, -12) = -4`, and reports
`3`.

They broke assumption 1: the shift applied to every candidate must preserve
order. Adding `a[i]` shifts all candidate sums by the same constant, and
addition is order-preserving. Multiplying by `a[i]` is order-preserving only
when `a[i] > 0`; when `a[i] < 0` it *reverses* the order, so the new maximum is
the image of the old **minimum**. The repair is to carry both the running
maximum and the running minimum, as `max_product` does above.
:::

:::check
On a circular array, why is the answer `max(kadane(a), total − minSubarray(a))`,
and which input makes the second term a trap?
--
An optimal circular subarray either wraps around the boundary or it does not. If
it does not, it is an ordinary subarray and `kadane(a)` finds it. If it does,
then the elements it *omits* form a contiguous non-wrapping block, and its own
sum is `total` minus that block's sum. To maximise the wrapping subarray you
minimise the omitted block, giving `total − minSubarray(a)`. The two cases are
exhaustive, so the maximum of the two is the answer.

The trap is an all-negative array, say `[-3, -2, -3]`. There, `minSubarray` is
the whole array, so `total − minSubarray = 0` — which corresponds to omitting
everything, i.e. the empty subarray. Since a non-empty answer is required, guard
with "if the minimum subarray is the entire array, return the linear answer".
:::

:::check
You run Kadane on an array of `10^5` integers each up to `10^9` in magnitude,
in a language where `int` is 32 bits, and you get a large negative answer on an
array containing large positives. What happened, and why did the algorithm's
correctness proof not protect you?
--
The accumulator overflowed. A subarray sum can reach `10^5 · 10^9 = 10^14`,
which does not fit in a signed 32-bit integer, so `cur + x` wrapped around to a
negative value.

The proof did not protect you because it is a statement about the integers: it
proves `cur = E(i)` where `E(i)` is defined by exact arithmetic. That is
assumption 4. Wrapping arithmetic silently implements a different function than
the one the proof reasons about, so the conclusion simply does not apply to the
program you ran. This is the general lesson about correctness proofs — they
transfer to code only as far as the code implements the model, and machine
integers are not integers. Python is exempt here ([[big-integers]]), which is
precisely why it is easy to forget.
:::

:::check
The trace in **Worked by hand** restarted the carry exactly when the previous
carry was negative. Prove that `max(x, cur + x) = x` if and only if `cur <= 0`,
and explain why the implementation still prefers to write the comparison as
`cur + x < x`.
--
`cur + x <= x` is equivalent to `cur <= 0` by subtracting `x` from both sides —
valid for every `x`, positive or negative, since addition is order-preserving
over the integers. So the "extend" branch wins exactly when `cur > 0`, ties
being irrelevant to the value (though they do affect which start index you
report).

The implementation still writes `cur + x < x` because that form states the
decision being made — *compare the two candidates* — rather than a simplified
consequence of it. When a variant changes the candidate set (a product, a second
carry, a length cap), the line already has the right shape and the edit is
local. The `cur < 0` form is a shortcut that happens to be true for this
particular score function, and shortcuts are what you carry into a variant by
mistake.
:::
