# Sliding Window

> A sliding window is not two pointers that happen to move. It is the discovery
> that the best left endpoint never goes backwards, so the whole quadratic search
> over subarrays collapses into one pass.

## When you reach for it

You reach for a sliding window when the answer is a **contiguous** stretch of an
array or string, and the property that makes a stretch acceptable gets *easier*
as the stretch gets shorter.

That second half is the real condition, and it has a name worth knowing:
the property must be **hereditary** (downward-closed). If `[l, r]` is acceptable
then every window inside it is acceptable too. "At most two distinct characters"
is hereditary — throw elements away and the distinct count cannot rise. "At most
`k` zeros" is hereditary. "Sum at most `k`, all values non-negative" is
hereditary. Whenever you have that, a window that has gone bad can only be
repaired by moving the left end right, never left, and that single fact is the
entire algorithm.

209 problems in this bank use it, #19 of 150 — one of the highest-yield patterns
there is. They come in five shapes, worth telling apart on sight:

- **A window of fixed size `k`.** *Sliding Window Average*, *Fixed-Window Rolling
  Mean*, *Validate 3x3 Digit Windows*. No decisions: add one, drop one.
- **The longest valid window.** *Longest Substring Without Repeating Characters*
  (which ten different companies in this bank ask), *Max Consecutive Ones III*,
  *Longest Repeating Character Replacement*, *Maximum Candies with At Most Two
  Types in a Line*.
- **The shortest valid window.** *Minimum Window Substring*, *Minimum Parking Roof
  Length*. Same two pointers, mirrored loop.
- **Counting windows.** *Get Stable Periods Count*, *Count the Number of Good
  Subarrays*, *Subarray Counting*. One extra line: `total += r - l + 1`.
- **A window over time rather than over indices.** *Sliding-Window Rate Limiter*,
  *Rolling Hit Counter*, *15-Minute Chat Session Tracker*. The window is "the last
  60 seconds", the array is a stream, and the structure is a queue.

The tool is wrong in two situations, and both are common enough to be worth
memorising as anti-signals.

**The property is not hereditary.** *Longest Subarray with Sum at Most K*
(Google, hard) spells the trap out in its own statement: "the array may contain
positive, zero, and negative values, so a standard positive-only sliding window
is not sufficient". With a negative in the array, dropping an element can *raise*
the sum, so shrinking is not guaranteed to repair anything, and the left pointer
genuinely might have to go back. Those problems need [[prefix-sums]] plus a
[[monotonic-deque]] or a binary search, not a window.

**The thing you want is not contiguous.** "Subsequence", "any `k` elements",
"reorder freely" — each breaks the one structural assumption a window has. And
*Find Largest Sum Contiguous Subarray* is contiguous yet still not a window
problem: maximum sum with negatives allowed is [[kadane]].

## The idea

Picture a caterpillar on the array. The head moves forward one cell per step,
eating the new element. When the caterpillar becomes too long to be legal, the
tail moves forward until it is legal again. Neither end ever reverses.

<svg viewBox="0 0 660 200" role="img" aria-label="a window over an array whose left and right ends both move only to the right">
  <g>
    <rect x="30" y="62" width="60" height="46" rx="4"/>
    <rect x="90" y="62" width="60" height="46" rx="4"/>
    <rect x="150" y="62" width="60" height="46" rx="4"/>
    <rect class="fill" x="210" y="62" width="60" height="46" rx="4"/>
    <rect class="fill" x="270" y="62" width="60" height="46" rx="4"/>
    <rect class="fill" x="330" y="62" width="60" height="46" rx="4"/>
    <rect class="fill" x="390" y="62" width="60" height="46" rx="4"/>
    <rect x="450" y="62" width="60" height="46" rx="4"/>
    <rect x="510" y="62" width="60" height="46" rx="4"/>
    <line x1="210" y1="120" x2="210" y2="140"/>
    <text x="210" y="160" text-anchor="middle">l</text>
    <line x1="420" y1="120" x2="420" y2="140"/>
    <text x="420" y="160" text-anchor="middle">r</text>
    <line x1="200" y1="40" x2="268" y2="40"/>
    <line x1="268" y1="40" x2="256" y2="33"/>
    <line x1="268" y1="40" x2="256" y2="47"/>
    <text x="150" y="30" text-anchor="middle">drop a[l]</text>
    <line x1="410" y1="40" x2="478" y2="40"/>
    <line x1="478" y1="40" x2="466" y2="33"/>
    <line x1="478" y1="40" x2="466" y2="47"/>
    <text x="540" y="30" text-anchor="middle">add a[r]</text>
    <text x="30" y="188">the shaded cells are the current window; neither end ever moves left</text>
  </g>
</svg>

Written down, the longest-window form is six lines:

```python
l = 0
for r in range(n):
    add(a[r])
    while not ok():
        drop(a[l])
        l += 1
    best = max(best, r - l + 1)
```

It looks like nothing. Count what it replaces: there are `n(n+1)/2` subarrays,
and the window examines exactly `n` of them — one per right endpoint — yet still
gets the right answer. The justification is a single claim:

> For each right endpoint `r`, let `L(r)` be the smallest left endpoint such that
> `[L(r), r]` is valid. Then `L` is non-decreasing in `r`.

If `L` never goes down, the left pointer never needs to rewind, and one forward
sweep discovers every `L(r)`. Drawn, the claim is a staircase that only climbs:

<svg viewBox="0 0 480 230" role="img" aria-label="L of r plotted against r, a step function that never decreases">
  <g>
    <line x1="40" y1="190" x2="450" y2="190"/>
    <line x1="40" y1="200" x2="40" y2="40"/>
    <text x="455" y="195">r</text>
    <text x="10" y="35">L(r)</text>
    <line x1="40" y1="190" x2="180" y2="190"/>
    <line x1="180" y1="190" x2="180" y2="130"/>
    <line x1="180" y1="130" x2="330" y2="130"/>
    <line x1="330" y1="130" x2="330" y2="70"/>
    <line x1="330" y1="70" x2="430" y2="70"/>
    <circle class="fill" cx="40" cy="190" r="4"/>
    <circle class="fill" cx="90" cy="190" r="4"/>
    <circle class="fill" cx="140" cy="190" r="4"/>
    <circle class="fill" cx="190" cy="130" r="4"/>
    <circle class="fill" cx="240" cy="130" r="4"/>
    <circle class="fill" cx="290" cy="130" r="4"/>
    <circle class="fill" cx="340" cy="70" r="4"/>
    <circle class="fill" cx="390" cy="70" r="4"/>
    <text x="40" y="220">the left end climbs or waits; it is never asked to come back down</text>
  </g>
</svg>

Every variant here is that staircase wearing a different hat. A fixed-size window
is the case `L(r) = r - k + 1`. The shortest-window form reads the *last* valid `l`
rather than the first. The counting form notices that the valid windows ending at
`r` are exactly `[L(r), r] … [r, r]`, so there are `r - L(r) + 1` of them.

## Worked by hand

Take `s = "aabcbb"` and the rule "at most 2 distinct characters" — the shape of
*Longest Substring With At Most Two Distinct Characters* and of *Maximum Candies
with At Most Two Types in a Line*. The window state is a frequency map, and the
test is `len(counts) <= 2`.

Start with `l = 0`, an empty map and `best = 0`.

| r | `s[r]` | counts after add | evictions | l | window | len | best |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | a | `{a:1}` | — | 0 | `a` | 1 | 1 |
| 1 | a | `{a:2}` | — | 0 | `aa` | 2 | 2 |
| 2 | b | `{a:2, b:1}` | — | 0 | `aab` | 3 | 3 |
| 3 | c | `{a:2, b:1, c:1}` | drop `a` → `{a:1,b:1,c:1}`, still 3; drop `a` → `{b:1,c:1}` | 2 | `bc` | 2 | 3 |
| 4 | b | `{b:2, c:1}` | — | 2 | `bcb` | 3 | 3 |
| 5 | b | `{b:3, c:1}` | — | 2 | `bcbb` | 4 | 4 |

The answer is 4, the window `bcbb`. Four things in that table are worth a second
look, and none of them is visible in the code.

**Row 3 evicted twice.** The inner construct is a `while`, not an `if`, and this
row proves it: after dropping the first `a` the map still held three keys, because
`a` had multiplicity 2. Writing `if` survives most small tests precisely because
most rows need zero or one eviction.

**The window was briefly illegal.** Between "add `c`" and the end of the eviction
loop, `aabc` held three distinct characters. Validity is not maintained
continuously; it is *restored* before `best` is read. That is why
`best = max(best, r - l + 1)` sits after the `while`.

**The left pointer moved 2 positions in total, over six iterations.** Not 2 per
iteration — 2 for the whole run. The inner loop looks quadratic and is not, and
the trace shows why: `l` has only `n` places to go, ever.

**Four windows were never tested.** `[0,4]`, `[1,4]`, `[0,5]`, `[1,5]` were
silently declared hopeless. The trace cannot justify that; only the proof can.

## Why it is correct

:::proof The left endpoint is monotone, and the sweep finds it
**Setup.** Fix an array `a[0..n-1]` and a predicate `P` on windows, where a
window is a pair `(l, r)` with `0 <= l <= r + 1 <= n` (so `l = r + 1` denotes the
empty window). Assume:

- **(H) Hereditary.** If `P(l, r)` holds and `l <= l' <= r' + 1` with `r' <= r`,
  then `P(l', r')` holds. In words: every sub-window of a valid window is valid.
- **(E) Empty is valid.** `P(r + 1, r)` holds for every `r`.

Define `L(r) = min{ l : P(l, r) }`. By (E) the set is non-empty, so `L(r)` is
well defined and `L(r) <= r + 1`.

**Lemma (monotonicity).** `L(r) <= L(r + 1)` for every `r`.

*Proof.* Let `l* = L(r + 1)`, so `P(l*, r + 1)` holds. If `l* > r`, then
`L(r) <= r + 1 <= l*` and we are done. Otherwise `l* <= r`, and applying (H) to
the valid window `(l*, r + 1)` with `l' = l*`, `r' = r` gives `P(l*, r)`. Hence
`l*` belongs to the set whose minimum is `L(r)`, so `L(r) <= l*`. ∎

**Invariant.** Let `l_r` be the value of the variable `l` at the moment `best` is
updated in iteration `r`. Claim: `l_r = L(r)`, and after that update
`best = max{ r' - L(r') + 1 : r' <= r }`.

**Base case.** Before the loop, `l = 0` and `best = 0`. Take the convention
`L(-1) = 0`, which is consistent: the only window ending at `-1` is the empty one.

**Inductive step.** Suppose `l = L(r - 1)` when iteration `r` begins. Iteration
`r` calls `add(a[r])`, so the state now describes the window `(l, r)`, and then
runs `while not P(l, r): drop(a[l]); l += 1`.

*The loop stops.* Each pass increases `l` by one, and by (E) the test `P(l, r)`
is true once `l` reaches `r + 1`. So the loop performs at most `r + 1 - L(r - 1)`
passes and exits with `P(l, r)` true.

*The exit value is minimal.* Let `l_r` be the value on exit. We must rule out
every smaller `l'`.

- For `L(r - 1) <= l' < l_r`: the loop body ran while the variable held `l'`,
  which happens only when the test `P(l', r)` evaluated false.
- For `l' < L(r - 1)`: by the inductive hypothesis `l' < L(r - 1)` means
  `P(l', r - 1)` is false. If `P(l', r)` were true, (H) with `r' = r - 1` would
  give `P(l', r - 1)` — a contradiction. So `P(l', r)` is false.

Every `l' < l_r` fails, and `l_r` succeeds, so `l_r = L(r)`. The update
`best = max(best, r - l_r + 1)` therefore extends the maximum to include `r`.

**Termination of the whole loop.** `r` runs over `0..n-1`; `l` only increases and
is bounded above by `n`. Both are monotone and bounded, so the algorithm halts.

**Conclusion.** On exit, `best = max{ r - L(r) + 1 : 0 <= r < n }`. Any valid
window `(a, b)` satisfies `a >= L(b)` by minimality, so its length
`b - a + 1 <= b - L(b) + 1 <= best`; and `best` is itself the length of some valid
window. So `best` is the length of the longest valid window. ∎
:::

Now say plainly what that proof used, because that list is where the bugs live.

- **Heredity (H) is doing everything.** It is used twice: once for the
  monotonicity lemma, once to show old left endpoints stay dead. Lose it and the
  algorithm does not become slow — it becomes *wrong*. Concretely: `a = [3, -3, 1]`
  with "sum at most 2". The window `[0, 0]` is invalid (sum 3) so `l` moves to 1
  and never returns; but `[0, 2]` has sum 1 and is valid, length 3. The sweep
  reports 2. This is exactly why *Longest Subarray with Sum at Most K* is filed as
  hard and needs a different tool.
- **The empty window must be valid (E).** It is the sentinel that stops the inner
  loop, the analogue of the sentinel indices in [[binary-search]]. If your
  predicate is "the window is non-empty and has at most `k` distinct", the loop
  will march `l` past `r` and index out of bounds. Put the non-emptiness in the
  *answer*, never in the *test*.
- **`add` and `drop` must be exact inverses.** The proof assumed the state after
  `add(a[r])` describes `(l, r)` and the state after `drop(a[l])` describes
  `(l+1, r)`. A frequency map that leaves zero-count keys behind violates this:
  `len(counts)` then reports characters that are no longer in the window.
- **The test must be readable from the state in O(1).** The proof does not need
  this; the running time does. A predicate that rescans the window is correct and
  quadratic.
- **Nothing here mentions "longest".** The proof establishes `l = L(r)` at every
  step; what you do with that fact is a separate decision, which is why one
  skeleton solves four problem shapes.

## What it costs

Derive it rather than asserting it, because the inner `while` genuinely looks
quadratic and the reason it is not is the interesting part.

Let `s_r` be the number of evictions performed in iteration `r`. The actual work
of iteration `r` is `1` add, `s_r` drops, and `s_r + 1` predicate evaluations, so
it is `Θ(1 + s_r)` unit operations. Total work is
`Σ_r (1 + s_r) = n + Σ_r s_r`.

Now bound `Σ_r s_r`. Each eviction increases `l` by exactly one, `l` starts at 0,
`l` never decreases, and `l <= n` always. So `Σ_r s_r = l_final <= n`. Total work
is at most `2n` operations: **Θ(n)**.

The same thing as a potential-function argument, which generalises better. Let
`Φ = n - l`. Then `Φ >= 0` always, `Φ` starts at `n`, and iteration `r` changes it
by `-s_r`. The amortised cost is

    â_r = (1 + s_r) + ΔΦ = (1 + s_r) - s_r = 1

so each iteration costs 1 amortised unit and the total is
`Σ â_r + Φ_start - Φ_end <= n + n = 2n`. This is the standard shape of an
[[amortized-analysis]] proof: an individual iteration may cost `Θ(n)` — the very
first one can evict everything — but no sequence of iterations can.

**With the constant.** Each unit is one `add`, one `drop` or one test. For an
integer counter those are genuinely O(1); for a hash map they are *expected* O(1)
with a real constant on top ([[hash-tables]]). That constant is what people
forget when `n = 2·10⁵`, the bound *Longest Subarray Without Repeated Values* and
*Shortest Subarray with Sum at Least K* both ship with.

**Space.** O(1) for a numeric aggregate. O(σ) for an alphabet-indexed count array
— 26 or 128 slots, and for *Longest Repeating Character Replacement* (uppercase
only) a 26-slot list beats a dict by a wide margin. O(min(n, σ)) for a dict.
O(k) for the deque forms.

**The two costs people forget entirely.** First, recomputing the predicate from
scratch: `len(set(a[l:r+1]))` inside the loop is `Θ(n)` per iteration and turns
the whole thing back into `Θ(n²)` — plus a slice copy, so it is `Θ(n²)` space
traffic too. Second, the window aggregate that cannot be maintained
incrementally. `max` is the canonical example: you can add to a running maximum
in O(1) but you cannot remove from one, because the maximum does not remember
what was second. That is not a small inconvenience; it is why *Sliding Window
Maximum* is a separate, harder problem needing a [[monotonic-deque]], and why the
naive `max(a[l:r+1])` per window is `Θ(nk)`.

## The implementation

The skeleton is worth writing once as a driver with three callbacks, because it
makes visible that the only thing that changes between problems is the state.

```python run
from collections import Counter
import random


def longest_window(n, add, drop, ok):
    """Longest valid window, given a state maintained by add(i) / drop(i).
    Requires: every sub-window of a valid window is valid, and the empty
    window is valid."""
    best = l = 0
    for r in range(n):
        add(r)
        while not ok():          # the window is momentarily illegal
            drop(l)
            l += 1
        best = max(best, r - l + 1)
    return best


def at_most_k_distinct(s, k):
    cnt = Counter()

    def add(i):
        cnt[s[i]] += 1

    def drop(i):
        cnt[s[i]] -= 1
        if cnt[s[i]] == 0:
            del cnt[s[i]]                    # or len(cnt) lies about the window

    return longest_window(len(s), add, drop, lambda: len(cnt) <= k)


def longest_all_distinct(a):
    cnt, dups = Counter(), [0]               # dups = values appearing twice or more

    def add(i):
        cnt[a[i]] += 1
        if cnt[a[i]] == 2:
            dups[0] += 1

    def drop(i):
        if cnt[a[i]] == 2:
            dups[0] -= 1
        cnt[a[i]] -= 1

    return longest_window(len(a), add, drop, lambda: dups[0] == 0)


def max_consecutive_ones(nums, k):
    zeros = [0]                              # flip at most k zeros
    return longest_window(len(nums),
                          lambda i: zeros.__setitem__(0, zeros[0] + (nums[i] == 0)),
                          lambda i: zeros.__setitem__(0, zeros[0] - (nums[i] == 0)),
                          lambda: zeros[0] <= k)


def brute(s, k):
    return max([j - i for i in range(len(s) + 1) for j in range(i, len(s) + 1)
                if len(set(s[i:j])) <= k] or [0])


print("at most 2 distinct in 'aabcbb' :", at_most_k_distinct("aabcbb", 2), "(window 'bcbb')")
print("no repeats in 'abcabcbb'       :", longest_all_distinct("abcabcbb"))
print("ones after 2 flips             :", max_consecutive_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2))
assert at_most_k_distinct("aabcbb", 2) == 4
assert longest_all_distinct("abcabcbb") == 3
assert max_consecutive_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6

rng = random.Random(5)
for _ in range(400):
    s = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 11)))
    k = rng.randint(0, 4)
    assert at_most_k_distinct(s, k) == brute(s, k), (s, k)
print("400 random strings agree with the O(n^3) recount")
```

Three details are doing the real work.

`while not ok()` and not `if not ok()`. Row 3 of the hand trace is the reason.
There is a subtlety that catches good candidates out: for the *longest* problem
the `if` version returns the same number, because the window then never shrinks
and `best` still equals the largest length ever reached legally. It is wrong the
moment you need the window itself, or a count — as the next block shows.

`del cnt[s[i]]` when the count hits zero. `len(cnt)` is the predicate; a key
sitting at zero is a character that has left the window still voting on the
answer. Leave it in and the window shrinks forever, `l` walks past `r`, and you
get an `IndexError` on `s[l]` — a crash, on some inputs only.

`best = max(best, r - l + 1)` sits *after* the `while`. Inside the loop it would
measure illegal windows; before the loop it would measure the pre-eviction window.
The position of this line is the invariant made concrete.

## Variants you will meet

**Fixed size `k`.** There is no inner loop, because `L(r) = r - k + 1` is known in
advance: add `a[r]`, and if `r >= k` drop `a[r - k]`. *Sliding Window Average* and
*Fixed-Window Rolling Mean* are this with a running sum; its follow-up ("design
an API if the input is a stream") is the same recurrence behind a [[queue]].

**Shortest valid window.** The predicate flips from hereditary to *upward*-closed:
adding elements can only help, so you grow until valid and then shrink while
*still* valid, recording as you shrink. *Minimum Window Substring* and *Minimum
Parking Roof Length* are the two canonical instances.

**Counting windows.** When `l = L(r)`, the valid windows ending at `r` are exactly
`[L(r), r] … [r, r]`, so `total += r - l + 1` counts them all in O(1). *Get Stable
Periods Count* ("no more than `k` distinct values over the period", answer modulo
`10⁹+7`) and *Count the Number of Good Subarrays* are this line.

**Exactly `k`, via two at-mosts.** "Exactly `k` distinct" is not hereditary — drop
an element and you may fall to `k-1`. But
`exactly(k) = atMost(k) - atMost(k-1)`, and both terms are hereditary. This
subtraction is the single most reusable trick in the family.

**Maximum or minimum over the window.** The aggregate is not removable, so keep a
[[monotonic-deque]] of indices whose values are decreasing; the front is the
maximum, and indices falling out of range are popped. *Sliding Window Maximum*,
*Maximum of Window Minimums* and *Minimum of Fixed-Window Maxima* are all this.
The related [[monotonic-stack]] answers the same question offline.

**Order statistics over the window.** Median or `k`-th smallest needs more than a
deque: an [[ordered-set]], a Fenwick tree over values, or two heaps
([[median-maintenance]]). *Find Kth Minimum Vulnerability* and *Kth Smallest in
Subarray* are these.

**Windows over time.** The window is "the last `W` seconds" and the left end is
driven by the clock, not by a predicate: keep a deque of timestamps and evict from
the front while `now - front >= W`. *Sliding-Window Rate Limiter*, *Per-Client
Sliding-Window Rate Limiter*, *Rolling Hit Counter* and *Chat Event Counts in
Recent Window* are this ([[rate-limiting]], [[design-data-structure]]). Two
details these statements care about: the interval is usually half-open — Amazon's
*Sliding-Window Rate Limiter* says `(timestamp - 60, timestamp]` — and rejected
requests must not be recorded.

**Fixed-length pattern matching.** A window of length `len(pattern)` whose
frequency map is compared against the pattern's solves *All Anagram Start Indices*
and *Find First Anagram Index* in O(n). For exact equality instead of anagram
equality — *Find Sliding-Window Pattern Start Indices* — use a [[rolling-hash]] or
[[string-matching]].

**When heredity fails: prefix sums plus a deque.** With negatives, let
`pre[i] = a[0] + … + a[i-1]` and rewrite "the sum of `[l, r]` is at least `k`" as
`pre[r+1] - pre[l] >= k`. A monotone deque over `pre` answers *Shortest Subarray
with Sum at Least K*, and *Longest Subarray with Sum at Most K* falls to the same
machinery. [[prefix-sums]] first, then a deque or a binary search.

**Two windows.** *Maximize Sum of Two Non-Overlapping Fragments* and *Maximum Sum
of Two Sign-Flipping Windows* sweep twice — best window ending at or before each
index, best starting at or after — then combine at the split point.

```python run
from collections import Counter, deque


def min_window(s, t):
    """Shortest substring of s containing all of t with multiplicity."""
    need, missing = Counter(t), len(t)
    best, l = (len(s) + 1, 0, 0), 0
    for r, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1                 # this copy was actually needed
        need[ch] -= 1
        while missing == 0:              # valid: shrink while it stays valid
            if r - l + 1 < best[0]:
                best = (r - l + 1, l, r + 1)
            need[s[l]] += 1
            if need[s[l]] > 0:
                missing += 1
            l += 1
    return s[best[1]:best[2]]


def count_at_most_k_distinct(a, k):
    if k < 0:
        return 0                         # guard: exactly(0) subtracts atMost(-1)
    cnt, l, total = Counter(), 0, 0
    for r, x in enumerate(a):
        cnt[x] += 1
        while len(cnt) > k:
            cnt[a[l]] -= 1
            if cnt[a[l]] == 0:
                del cnt[a[l]]
            l += 1
        total += r - l + 1               # windows ending at r: [l..r] .. [r..r]
    return total


def count_exactly_k_distinct(a, k):
    return count_at_most_k_distinct(a, k) - count_at_most_k_distinct(a, k - 1)


def window_max(a, k):
    """Maximum of every length-k window. max cannot be removed from a running
    aggregate, so keep indices whose values are strictly decreasing."""
    dq, out = deque(), []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(a[dq[0]])
    return out


print("min_window('ADOBECODEBANC', 'ABC') =", repr(min_window("ADOBECODEBANC", "ABC")))
assert min_window("ADOBECODEBANC", "ABC") == "BANC"
s = list("aabcbb")
print("subarrays of 'aabcbb' with <=2 distinct :", count_at_most_k_distinct(s, 2))
print("subarrays of 'aabcbb' with  =2 distinct :", count_exactly_k_distinct(s, 2))
assert count_at_most_k_distinct(s, 2) == 15 and count_exactly_k_distinct(s, 2) == 7
assert count_at_most_k_distinct(s, 0) == 0
a = [1, 3, -1, -3, 5, 3, 6, 7]
print("window_max(k=3) :", window_max(a, 3))
assert window_max(a, 3) == [max(a[i:i + 3]) for i in range(len(a) - 2)]
print("deque result matches the O(n*k) recount")
```

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"contiguous", "substring", "subarray", "consecutive"** together with
   *longest*, *shortest*, *maximum* or *count*. The word "subsequence" instead
   kills it outright.
2. **"at most `k` …"** — distinct values, replacements, zeros, deletions, cost.
   The phrase "at most" is a gift: it is heredity handed to you in words.
   *Max Consecutive Ones III*, *Longest Substring with At Most K Distinct
   Characters*, *Longest Repeating Character Replacement* (at most `k`
   replacements) all read this way.
3. **A window size in the input** — `k`, "every 3x3 block", "60 seconds",
   "the last 15 minutes". Fixed-size form, no inner loop.
4. **"within the last W seconds", "in the current window", "rate limit"** — the
   time-window form. Expect a stream, a per-key dictionary of deques, and an
   argument about open versus closed endpoints.
5. **`n <= 10⁵` or `2·10⁵` with an obvious `O(n²)` enumeration of subarrays.**
   The constraint is naming the intended complexity.
6. **"count the number of subarrays such that …"** with an at-most condition.
   `total += r - l + 1`, or the `atMost(k) - atMost(k-1)` subtraction.

The anti-signals, which matter more than the signals because they are what stops
you writing a confident wrong answer:

- **Negative numbers plus a sum threshold.** Heredity is gone. Reach for
  [[prefix-sums]] and a [[monotonic-deque]].
- **Maximum subarray sum with negatives.** That is [[kadane]], not a window —
  *Find Largest Sum Contiguous Subarray* and *Maximum Subarray* live there.
- **The condition improves when you add elements.** "At least `k` distinct", "sum
  at least `k`" — you want the shortest-window form, or the whole thing inverts.
- **Elements may be reordered or skipped.** Not contiguous, not a window; usually
  [[sorting]], [[greedy]] or [[dynamic-programming]].
- **A "window" that must be recomputed per query at arbitrary positions.** A
  sliding window is a sweep; random-access range queries want [[prefix-sums]] or a
  [[segment-tree]].

## Traps

**`if` instead of `while` in the eviction loop.** Symptom for longest-window
problems: none — the answer is still right, which is precisely what makes it
dangerous. Symptom for counting or for returning the window itself: silently too
large. Demonstrated below.

**Zero-count keys left in the frequency map.** Symptom: `len(cnt)` never falls,
the inner loop cannot exit, and `l` overruns `r` into an `IndexError`.

**Reading the answer in the wrong place.** Before the `while` it measures the
previous window; inside, an illegal one. It goes after.

**Putting non-emptiness into the predicate.** "Non-empty and at most `k`
distinct" makes the empty window invalid, assumption (E) fails, and the inner loop
has no stopping condition.

**Using `max` or `min` as a removable aggregate.** Symptom: correct on inputs
where the maximum never leaves the window, wrong as soon as it does. Use a deque.

**Shrinking a fixed-size window with a `while`.** For fixed `k` the drop is
unconditional: `if r >= k: drop(r - k)`. A `while` here is a second mechanism that
will eventually disagree with the first.

**Off-by-one in the length.** `r - l + 1` inclusive, `r - l` if `r` is exclusive.
One convention per function.

**Half-open time windows.** `(t - 60, t]` and `[t - 60, t]` differ on exactly the
requests that are 60 seconds old, which is exactly the case the tests cover.
*Sliding-Window Rate Limiter* states the half-open form explicitly; read it.

**Assuming heredity because last week's problem had it.** Demonstrated below.

```python run
from collections import Counter


def count_le_2_distinct(s, use_while):
    cnt, l, total, longest = Counter(), 0, 0, 0
    for r, ch in enumerate(s):
        cnt[ch] += 1
        while len(cnt) > 2:
            cnt[s[l]] -= 1
            if cnt[s[l]] == 0:
                del cnt[s[l]]
            l += 1
            if not use_while:
                break                      # the bug: evict at most once
        total += r - l + 1
        longest = max(longest, r - l + 1)
    return total, longest, (l, r)


def brute_count(s):
    return sum(1 for i in range(len(s)) for j in range(i, len(s))
               if len(set(s[i:j + 1])) <= 2)


s = "aabcbb"
right = count_le_2_distinct(s, True)
buggy = count_le_2_distinct(s, False)
print("truth   count =", brute_count(s))
print("while:  count, longest, final window =", right)
print("if   :  count, longest, final window =", buggy)
assert right[0] == brute_count(s) == 15 and buggy[0] == 16
assert right[1] == buggy[1] == 4              # the LENGTH survives the bug
print("the 'if' version gets the longest length right and the count wrong\n")


def longest_sum_at_most(a, k):
    tot = l = best = 0
    for r, x in enumerate(a):
        tot += x
        while tot > k:                     # assumes dropping lowers the sum
            tot -= a[l]
            l += 1
        best = max(best, r - l + 1)
    return best


def brute_longest(a, k):
    return max([j - i + 1 for i in range(len(a)) for j in range(i, len(a))
                if sum(a[i:j + 1]) <= k] or [0])


for a, k in ([1, 2, 1, 0, 1, 1], 4), ([3, -3, 1], 2):
    w, b = longest_sum_at_most(a, k), brute_longest(a, k)
    print("a =", a, " k =", k, " window:", w, " truth:", b,
          "  <-- heredity broken" if w != b else "")
assert longest_sum_at_most([1, 2, 1, 0, 1, 1], 4) == brute_longest([1, 2, 1, 0, 1, 1], 4)
assert longest_sum_at_most([3, -3, 1], 2) == 2 and brute_longest([3, -3, 1], 2) == 3
print("one negative number is enough to make the window answer wrong")
```

The second half of that output is the whole lesson of the chapter in three
elements. `[3, -3, 1]` has sum 1, so the entire array is a valid window of length
3. The sweep rejected index 0 at the very first step, because `[0, 0]` alone had
sum 3, and monotonicity then forbade it from ever reconsidering. The algorithm is
not buggy; the assumption is.

## What to memorise

Very little. One skeleton, one question, one habit.

**The skeleton**, which should come out of your fingers without thought:

```python
l = 0
for r in range(n):
    add(a[r])
    while not ok():
        drop(a[l])
        l += 1
    best = max(best, r - l + 1)     # longest
    # total += r - l + 1            # counting
```

**The question** that turns a problem into it: *"If a window is acceptable, is
every window inside it acceptable?"* If yes, the left pointer never rewinds and
this template applies. If no — negatives with a sum bound, "exactly `k`",
"at least `k`" — either rewrite the predicate as an at-most, or leave for
[[prefix-sums]] and a deque.

**The habit**: after writing the loop, say out loud what `l` means. Not "the left
pointer" — the actual claim: *"`l` is the smallest index for which `[l, r]` is
still legal."* If you cannot say it, you will put `best` in the wrong place.

Numbers worth carrying: total pointer movement is at most `2n`, so the window is
linear regardless of how the inner loop looks; there are `n(n+1)/2` subarrays, so
`n = 2·10⁵` makes anything quadratic impossible; the number of valid windows
ending at `r` is `r - L(r) + 1`; and `exactly(k) = atMost(k) - atMost(k-1)`.

## Check yourself

:::check
Why is the left pointer allowed never to move backwards? Give the argument, not
the slogan.
--
Because validity is hereditary, and heredity forces `L(r)`, the smallest legal
left endpoint for right endpoint `r`, to be non-decreasing.

The one-line proof: take `l* = L(r+1)`, so `[l*, r+1]` is valid. The window
`[l*, r]` sits inside `[l*, r+1]`, so by heredity it is valid too, which means
`L(r) <= l*= L(r+1)`.

The consequence is the algorithm. When the sweep moves from `r` to `r+1`, the
answer it is looking for is at or to the right of where it already is, so a
forward scan finds it and a backward scan is never needed. Remove heredity and
the lemma has no proof — and, as `[3, -3, 1]` with "sum at most 2" shows, no
truth either.
:::

:::check
A candidate says: "a sliding window finds the maximum-sum contiguous subarray in
O(n)". Where are they wrong, and what is the correct statement?
--
They have assumed heredity where there is none. "The sum is large" does not
survive shrinking — dropping a negative element *increases* the sum — so there is
no predicate to evict against and no monotone `L(r)` to sweep for. With all values
non-negative the answer is trivially the whole array, so the question is only
interesting in exactly the case the window cannot handle.

The correct statement is that maximum-sum contiguous subarray with arbitrary signs
is [[kadane]]: a one-line dynamic program, `cur = max(x, cur + x)`, which is also
O(n) but is a different algorithm with a different correctness argument. In this
bank, *Find Largest Sum Contiguous Subarray* and *Maximum Subarray* are Kadane
problems; *Max Consecutive Ones III* is a window problem. The word "contiguous"
appears in all three.

The nearby true statement: *longest* subarray with sum at most `k` **is** a
window when all values are non-negative, and is not when they are not.
:::

:::check
"Count the subarrays containing exactly `k` distinct values" cannot be done by a
single window. Why not, and what is the standard repair?
--
Why not: the predicate "exactly `k` distinct" is not hereditary. `[1, 2, 3]` has
exactly 3 distinct values, but its sub-window `[1, 2]` has 2, so validity is not
inherited downwards. Without heredity there is no monotone `L(r)`, and the inner
eviction loop has nothing coherent to evict against — for a given `r` the set of
valid `l` is not even an interval in general.

The repair is to express the non-hereditary predicate as a difference of two
hereditary ones:

    exactly(k) = atMost(k) - atMost(k-1)

Both `atMost` runs are ordinary windows, each `Θ(n)`, and each counts with
`total += r - l + 1`. The subtraction is valid because the subarrays with at most
`k` distinct values are exactly those with at most `k-1` plus those with exactly
`k`, and the two sets are disjoint.

The same subtraction handles "exactly `k` odd numbers", "exactly `k` zeros" and
anything else counting something.
:::

:::check
The inner loop is `while not ok(): drop(a[l]); l += 1`. There is no bounds check
on `l`. Why can it not run off the end of the array — and what would make it?
--
Because of assumption (E) in the proof: the empty window is valid. Each pass
increases `l` by one, so after at most `r + 1 - l` passes we reach `l = r + 1`,
at which point the window is empty and `ok()` is true by (E). The loop must exit
before `l` exceeds `r + 1`, and `r + 1 <= n`, so `a[l]` is never read out of
range.

What breaks it: writing a predicate that is false on the empty window. Two ways
people do this by accident. First, "the window is non-empty and has at most `k`
distinct characters" — the non-emptiness belongs in what you report, not in the
test. Second, and far more common, forgetting `del cnt[ch]` when a count reaches
zero: then `len(cnt)` counts characters that have already left, `ok()` stays false
even for the empty window, and the loop keeps incrementing `l` until `a[l]`
raises. The symptom is a crash on some inputs and correct answers on others,
which is why it survives casual testing.
:::

:::check
For *Sliding Window Maximum* you want the maximum of every length-`k` window. Why
not keep a running maximum the way you keep a running sum, and what does the
deque know that the running maximum does not?
--
A running sum works because addition has an inverse: `sum - a[l]` undoes
`sum + a[l]`. Maximum has no inverse. If the element leaving the window is the
current maximum, the new maximum is the largest of the remaining `k-1` elements,
and a single number cannot tell you what that is — it has forgotten everything
except the winner.

The deque stores the only elements that could ever be the answer: indices inside
the window whose values strictly decrease. An element is dropped from the back
when a later, at-least-as-large element arrives, which is sound because that
later element dominates it in every future window — it survives longer and is
never smaller. So the deque holds exactly the not-yet-dominated candidates, the
front is the maximum, and popping the front when it falls out of range exposes the
next candidate in O(1). Each index is pushed and popped once, so the sweep is
`Θ(n)` by the accounting argument used above for `l`. See [[monotonic-deque]].
:::

:::check
You are implementing *Sliding-Window Rate Limiter*: requests arrive in
non-decreasing timestamp order, and a request is accepted when that user has
fewer than 100 accepted requests in `(t - 60, t]`. Sketch the structure, and name
the two details most likely to cost you the problem.
--
One dictionary from user id to a deque of that user's *accepted* timestamps. For
each incoming `(user, t)`: pop from the front while `front <= t - 60`; if fewer
than 100 entries remain, accept and append `t`, else reject. Each timestamp is
appended and popped at most once, so the work is `Θ(requests)` amortised and the
memory is 100 entries per active user.

The two details:

**The interval is half-open.** `(t - 60, t]` means a request exactly 60 seconds
old has expired. The eviction test is therefore `front <= t - 60`, not
`front < t - 60`. Getting this wrong changes the answer only for requests at the
boundary — which is what the tests are made of.

**Rejected requests must not be recorded.** The statement says rejected requests
do not consume capacity. Appending them anyway makes a user who is over the limit
stay over the limit forever, so the bug shows up as a burst of correct behaviour
followed by permanent rejection.

:::
