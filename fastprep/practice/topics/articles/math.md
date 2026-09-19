# Maths for Interviews

> Almost no interview problem wants you to recall a formula. It wants you to
> notice that the answer depends on far less of the input than the input
> contains — a remainder, a count, a closed form — and to compute that instead.

## When you reach for it

Four hundred and sixty-eight problems in this bank are tagged with it, which
makes it #8 of 150 — and that breadth is the first thing to understand. Maths is
not an algorithm the way [[binary-search]] is an algorithm. It is the label that
gets attached when a problem offers no structure to hang itself on: no adjacency,
no ordering to exploit, no window sliding along anything. What is left is
arithmetic, and the question becomes *which* arithmetic.

Two shapes reliably mean "the intended solution is mathematical".

**The input is a number, not a collection.** *Sum Multiples of 3, 5, or 7 Below
N* gives you one integer `n` up to `10^9` and asks for a sum over the integers
below it. There is no array, and the only way to answer a question about `10^9`
objects in time is never to touch them individually. *Arrange Coins* is the same
shape in disguise: `10^5` independent queries, each a coin count up to `10^9`, so
each query must be `O(1)` or `O(log)` and laying rows one at a time is out.

**The input is a collection, but the property asked about is arithmetic.**
*Nums That Are Divisible by N* asks for the number of index pairs `i < j` with
`arr[i] + arr[j]` divisible by `N`. Up to `10^5` values means about `5 · 10^9`
pairs, so the pairs cannot be enumerated. But divisibility by `N` does not care
about `arr[i]`; it cares about `arr[i] mod N`, and at most `10^5` of those
actually occur. The values collapse into buckets, and the pair count falls out of
the bucket sizes without a single pair being built.

The tool is wrong when the problem has real structure and the arithmetic is only
the payload. A statement stuffed with averages, prices and percentages can still
be a [[sliding-window]] problem, a [[prefix-sums]] problem or a [[greedy]] one;
the numbers are what you compute, not how you compute.

One warning belongs here rather than buried in the traps: a formula that matches
the three sample cases is a conjecture, not a solution. Every technique below
comes with an argument for why it is right. Pattern-matching against the samples
comes with nothing, and the hidden tests are where that gets settled — see
[[pattern-recognition]].

This chapter is the map. The deep versions live in [[modular-arithmetic]],
[[number-theory]], [[primes]], [[combinatorics]], [[fast-exponentiation]],
[[inclusion-exclusion]], [[base-conversion]], [[geometry]],
[[numerical-stability]] and [[big-integers]]. What is here is the method that
they all instantiate, proved once on the single most common concrete shape in
this bank.

## The idea

Find something small that the answer depends on, and that survives the
operation the problem performs.

Written as a formula, you are looking for a map `φ` from values to something
smaller, with two properties: the answer is determined by `φ` of the input, and
`φ` commutes with the operation — `φ(a ⊕ b)` can be computed from `φ(a)` and
`φ(b)` alone, without ever seeing `a` or `b` again. Then you can throw the
inputs away as they arrive and carry only their images.

Remainders are the archetype. Take `φ(x) = x mod k`. Then

```
(a + b) mod k = ((a mod k) + (b mod k)) mod k
(a · b) mod k = ((a mod k) · (b mod k)) mod k
```

so sums and products of huge numbers can be computed entirely inside the range
`0 … k-1`. The picture to hold is a dial with `k` marks. Every integer snaps to
one mark, adding moves you around the dial by the other number's mark, and
numbers that land on the same mark are interchangeable for every question about
divisibility by `k`.

<svg viewBox="0 0 640 250" role="img" aria-label="a dial with five marks; the numbers 2, 7 and 12 all point at the same mark">
  <g>
    <circle cx="130" cy="125" r="78"/>
    <circle cx="130" cy="47" r="6"/>
    <circle cx="204" cy="101" r="6"/>
    <circle class="fill" cx="176" cy="188" r="8"/>
    <circle cx="84" cy="188" r="6"/>
    <circle cx="56" cy="101" r="6"/>
    <text x="130" y="28" text-anchor="middle">0</text>
    <text x="226" y="98" text-anchor="middle">1</text>
    <text x="190" y="216" text-anchor="middle">2</text>
    <text x="70" y="216" text-anchor="middle">3</text>
    <text x="32" y="98" text-anchor="middle">4</text>
    <text x="130" y="131" text-anchor="middle">k = 5</text>
    <text x="345" y="76">2</text>
    <text x="345" y="116">7</text>
    <text x="345" y="156">12</text>
    <line x1="338" y1="71" x2="292" y2="112"/>
    <line x1="338" y1="111" x2="292" y2="115"/>
    <line x1="338" y1="151" x2="292" y2="119"/>
    <line x1="288" y1="116" x2="196" y2="180"/>
    <line x1="196" y1="180" x2="208" y2="180"/>
    <line x1="196" y1="180" x2="202" y2="169"/>
    <text x="430" y="121">same mark, so</text>
    <text x="430" y="145">interchangeable for</text>
    <text x="430" y="169">every question about</text>
    <text x="430" y="193">divisibility by 5</text>
  </g>
</svg>

Two other maps do the same job later in this chapter. The decimal digit sum
survives addition modulo 9, which is why *Add Digits* has a closed form. And
`gcd(x, y)` canonicalises a pair, which is why *Sliding-Window Averages as
Reduced Fractions* can keep exact averages in two integers forever.

The rest of the chapter takes the remainder map seriously, because it turns up
most often and because its proof is the proof for all of them. Concretely:
whenever a statement asks about the divisibility of a **sum**, stop thinking
about the values and start thinking about the marks of the **prefix sums**. The
sum of `a[j..l-1]` is `S_l - S_j`, and `k` divides a difference exactly when the
two ends land on the same mark. "Count the subarrays whose sum is divisible by
`k`" becomes "count the pairs of prefixes sharing a mark" — a frequency count,
not a search.

## Worked by hand

Take `a = [2, 3, 4, 1, 5]` and `k = 5`, the shape of *Count Subarrays With Sum
Divisible by K*. Maintain a running sum reduced mod 5, a table `cnt` counting how
many prefixes have landed on each mark so far, and a running answer.

Seed `cnt = {0: 1}`. That entry is the empty prefix `S₀ = 0`: it is a genuine
prefix, not a trick, and it is the one people forget.

| step | element | `S` (reduced) | `cnt` before | `ans += cnt[S]` | `ans` | `cnt` after |
| --- | --- | --- | --- | --- | --- | --- |
| — | — | 0 | `{}` | — | 0 | `{0:1}` |
| 1 | 2 | 2 | `{0:1}` | +0 | 0 | `{0:1, 2:1}` |
| 2 | 3 | 0 | `{0:1, 2:1}` | +1 | 1 | `{0:2, 2:1}` |
| 3 | 4 | 4 | `{0:2, 2:1}` | +0 | 1 | `{0:2, 2:1, 4:1}` |
| 4 | 1 | 0 | `{0:2, 2:1, 4:1}` | +2 | 3 | `{0:3, 2:1, 4:1}` |
| 5 | 5 | 0 | `{0:3, 2:1, 4:1}` | +3 | 6 | `{0:4, 2:1, 4:1}` |

The answer is 6, and the six subarrays are `[2,3]`, `[2,3,4,1]`, `[2,3,4,1,5]`,
`[4,1]`, `[4,1,5]` and `[5]`. Count them by hand; they are all there.

<svg viewBox="0 0 660 200" role="img" aria-label="six prefix sums with their residues, and brackets joining two pairs of equal residues">
  <g>
    <rect x="40" y="58" width="72" height="34" rx="4"/>
    <rect x="140" y="58" width="72" height="34" rx="4"/>
    <rect x="240" y="58" width="72" height="34" rx="4"/>
    <rect x="340" y="58" width="72" height="34" rx="4"/>
    <rect x="440" y="58" width="72" height="34" rx="4"/>
    <rect x="540" y="58" width="72" height="34" rx="4"/>
    <text x="76" y="81" text-anchor="middle">0</text>
    <text x="176" y="81" text-anchor="middle">2</text>
    <text x="276" y="81" text-anchor="middle">5</text>
    <text x="376" y="81" text-anchor="middle">9</text>
    <text x="476" y="81" text-anchor="middle">10</text>
    <text x="576" y="81" text-anchor="middle">15</text>
    <text x="76" y="116" text-anchor="middle">r 0</text>
    <text x="176" y="116" text-anchor="middle">r 2</text>
    <text x="276" y="116" text-anchor="middle">r 0</text>
    <text x="376" y="116" text-anchor="middle">r 4</text>
    <text x="476" y="116" text-anchor="middle">r 0</text>
    <text x="576" y="116" text-anchor="middle">r 0</text>
    <line x1="76" y1="52" x2="76" y2="32"/>
    <line x1="76" y1="32" x2="276" y2="32"/>
    <line x1="276" y1="32" x2="276" y2="52"/>
    <text x="176" y="24" text-anchor="middle">equal marks, so a[0..1] sums to 5</text>
    <line x1="276" y1="128" x2="276" y2="148"/>
    <line x1="276" y1="148" x2="476" y2="148"/>
    <line x1="476" y1="148" x2="476" y2="128"/>
    <text x="376" y="168" text-anchor="middle">equal marks, so a[2..3] sums to 5</text>
    <text x="40" y="192">S₀ … S₅, each reduced mod 5</text>
  </g>
</svg>

Three things in that table are worth stopping on, and none of them are visible
in the finished code.

**The answer grows by `cnt[S]`, not by 1.** Step 5 adds 3 in one move. The loop
is not finding subarrays, it is counting *pairs of prefixes that agree*, and a
mark visited `c` times contributes `c(c-1)/2` pairs in total. That is why this is
linear: the quadratic number of subarrays is never built, only counted.

**The seed did real work at step 2.** `cnt[0]` was 1 before anything had been
processed, and step 2 consumed it to record `[2, 3]` — the subarray starting at
index 0. Every qualifying subarray beginning at the left edge is paid for by that
one entry. Remove it and you lose exactly those, silently.

**The running sum never exceeded 4.** The true prefix sums were 0, 2, 5, 9, 10,
15, but the algorithm only held their marks. Under the real constraints — `10^4`
elements up to `10^9` in absolute value — the true sums reach `10^13`, fine in 64
bits, and not fine at all if the elements were multiplied instead of added.
Reducing as you go is free here and essential elsewhere.

## Why it is correct

The informal version ("equal residues mean the difference is divisible") is the
right intuition and proves nothing about the loop. Here is the argument in full.

:::proof Counting subarrays whose sum is divisible by k
**Setup.** Let `a[0..n-1]` be integers and `k >= 1`. Define the prefix sums
`S₀ = 0` and `S_t = a[0] + … + a[t-1]` for `1 <= t <= n`. Write `x ≡ y (mod k)`
for `k | (x - y)`.

**Lemma 1 (subarrays are pairs of prefixes).** The map `(j, l) ↦ a[j..l-1]` is a
bijection between `{(j, l) : 0 <= j < l <= n}` and the non-empty contiguous
subarrays of `a`, and `sum(a[j..l-1]) = S_l - S_j`. A non-empty subarray is
determined by its first index `j` and one past its last index `l`, and `j < l`
exactly says it is non-empty; the sum identity telescopes from the definition
of `S`.

**Lemma 2 (divisibility is agreement).** `k | (S_l - S_j)` if and only if
`S_l ≡ S_j (mod k)`. This is the definition of `≡`, and `≡` is an equivalence
relation: reflexive since `k | 0`; symmetric since `k | d` implies `k | -d`; and
transitive since `k | (x-y)` and `k | (y-z)` give `k | (x-z)` by adding.

**Lemma 3 (canonical marks).** For every integer `x` there is exactly one
`r ∈ {0, …, k-1}` with `x ≡ r (mod k)` — existence and uniqueness are the
division algorithm, `x = qk + r` with `0 <= r < k` for a unique pair `(q, r)`.
Python's `x % k` returns that `r` for `k > 0`, including for negative `x`. Call
it the *mark* of `x`; Lemma 2 then reads: two integers have the same mark iff
their difference is divisible by `k`.

**The loop.** `cnt` is a table from marks to counts, initialised to `{0: 1}`;
`ans` starts at 0; `S` starts at 0. For `t = 1, 2, …, n` in order: set
`S ← (S + a[t-1]) mod k`, then `ans ← ans + cnt[S]`, then `cnt[S] ← cnt[S] + 1`.

Because reduction commutes with addition, the value of `S` at the top of
iteration `t` is the mark of the true prefix sum `S_t`. (Formally: if
`S = S_{t-1} mod k` then `(S + a[t-1]) mod k = (S_{t-1} + a[t-1]) mod k = S_t mod k`.)

**Invariant.** Immediately before iteration `t` (for `t = 1, …, n+1`):

- **(I1)** for every mark `r`, `cnt[r] = |{ j : 0 <= j <= t-1 and S_j ≡ r }|`;
- **(I2)** `ans = |{ (j, l) : 0 <= j < l <= t-1 and S_j ≡ S_l }|`.

**Base case (`t = 1`).** The only index `j` with `0 <= j <= 0` is `j = 0`, and
`S₀ = 0` has mark 0, so (I1) asks for `cnt = {0: 1}`, which is the seed. There is
no pair `j < l <= 0`, so (I2) asks for `ans = 0`, which it is.

**Inductive step.** Assume (I1) and (I2) hold before iteration `t <= n`. The
pairs `(j, l)` with `j < l <= t` split into those with `l <= t-1`, already
counted by (I2), and those with `l = t`, which are the `j <= t-1` satisfying
`S_j ≡ S_t`. By (I1) applied to the mark of `S_t` — which is the value `S` holds
after the update — that second set has size exactly `cnt[S]`. The two sets are
disjoint and the statement adds precisely `cnt[S]`, so (I2) holds before
iteration `t+1`. The subsequent `cnt[S] += 1` extends the index range in (I1)
from `j <= t-1` to `j <= t`, since `S_t` has mark `S` and no other count
changes. So (I1) holds before iteration `t+1`.

**Termination.** The loop body contains no branches back and the loop is a
bounded iteration over `n` elements, so it executes exactly `n` times and each
execution performs a fixed number of table operations. There is nothing to
diverge.

**Conclusion.** After iteration `n`, the invariant holds with `t = n+1`, so
`ans` counts the pairs `0 <= j < l <= n` with `S_j ≡ S_l`. By Lemma 2 those are
the pairs with `k | (S_l - S_j)`, and by Lemma 1 they correspond one-to-one with
the non-empty subarrays whose sum is divisible by `k`. ∎
:::

Now list what the proof leaned on, because that list is where the bugs live.

- **`k >= 1`, and `%` returns a canonical mark in `[0, k)`.** Lemma 3 is where
  the argument touches the machine. Python's `%` satisfies it; C, C++, Java, Go,
  Rust and JavaScript do not, because their `%` takes the sign of the dividend,
  so `-3 % 5` is `-2` there and `2` here. *Count Subarrays With Sum Divisible by
  K* allows elements down to `-10^9`, so the residues really do go negative and
  `-3` and `2` land in different buckets although they are congruent. The fix is
  `((x % k) + k) % k`, written by reflex.
- **The pairs are strict, `j < l`.** That is Lemma 1's "non-empty", and counting
  before incrementing is what enforces it: when `ans += cnt[S]` runs, the current
  prefix is not yet in `cnt`, so it cannot pair with itself.
- **The seed is an index, not a hack.** `j = 0` is in the index set of (I1) from
  the base case onwards. Dropping `cnt[0] = 1` loses every pair whose left end is
  the empty prefix — that is, every qualifying subarray starting at index 0.
- **Only addition and subtraction were used.** Nothing here extends to division:
  `(a / b) mod k` is not `((a mod k) / (b mod k)) mod k`, and usually is not even
  defined. See the self-check at the end and [[modular-arithmetic]].
- **`ans` must hold the count.** The invariant says nothing about the width of
  your integer type. With `n` prefixes on one mark, `ans` reaches `n(n+1)/2`,
  about `5 · 10^9` for `n = 10^5`, past a signed 32-bit integer. *Nums That Are
  Divisible by N* says "return the number of valid index pairs as a long" for
  exactly this reason.

:::note The same argument, one dimension down
*Nums That Are Divisible by N* asks about `a[i] + a[j]`, not a contiguous sum, so
there are no prefixes — but Lemma 3 still applies, and `(a[i] + a[j]) mod N = 0`
becomes `mark(a[j]) = (N - mark(a[i])) mod N`. The marks partition the indices, a
pair qualifies iff its two classes are complementary, and the count is a sum of
products of class sizes. No invariant is needed because nothing is scanned twice;
the counting argument alone does it, and it is in the implementation below.
:::

## What it costs

**The thing you are replacing.** The number of non-empty subarrays of an array
of length `n` is the number of pairs `0 <= j < l <= n`, which is
`C(n+1, 2) = n(n+1)/2 = Θ(n²)`. Summing each from scratch gives `Θ(n³)`; with
prefix sums, `Θ(n²)`. At the stated `n <= 10^4` that is `5 · 10^7` subarrays —
survivable in C, not in Python, and hopeless if `n` were `10^5`.

**The residue algorithm.** One pass. Per element: one addition, one modulo, one
table lookup and one increment, all `O(1)` (expected, for a hash table — see
[[hash-tables]]). Total `Θ(n)` time.

Space is `Θ(min(n + 1, k))`, and the `min` is the interesting half: you cannot
store more entries than there are marks, nor more than the `n + 1` prefixes you
inserted. So when `k` is small, use an array of `k` counters and delete the
hashing — for `k <= 10^4` that is 40 KB and strictly faster. When `k` is large —
*Nums That Are Divisible by N* allows `N <= 10^9` while `n <= 10^5` — an array of
`N` counters is four gigabytes of mostly zeros and a dictionary is the only
option, because at most `10^5` marks are ever occupied. The combining step then
iterates over occupied marks rather than over `0 … N-1`, which is `Θ(min(n, N))`
and not `Θ(N)`.

**The cost people forget** comes in three flavours.

*The modulo itself.* `%` compiles to an integer division, the slowest integer
instruction on every mainstream CPU by a wide margin. One per element is nothing;
one inside a doubly-nested loop where you could have reduced once is a real and
invisible slowdown. In Python there is a second effect: `%` on
arbitrary-precision integers costs time proportional to the number of digits, so
letting a running product grow to a million bits and reducing at the end is
quadratic work, not constant.

*Exponentiation without a modulus.* `a ** b` has about `b · log₂ a` bits, so
`2 ** (10**6)` is a million-bit integer: Python builds it slowly and a
fixed-width language produces garbage. `pow(a, b, m)` performs `Θ(log b)`
squarings and multiplications of numbers bounded by `m` — 60 rounds for
`b = 10^18`. See [[fast-exponentiation]].

*The `√n` bound on divisor enumeration.* If `d` divides `n` then so does `n/d`,
and if both members of that pair were strictly greater than `√n` their product
would exceed `n`. So every divisor pair has a member `<= √n`, and testing
`d = 1, 2, …, ⌊√n⌋` while recording both `d` and `n/d` finds every divisor in
`Θ(√n)` divisions. The same pairing makes `Θ(√n)` enough for a primality test,
since a composite must have a factor at most `√n`. For `n = 10^12` that is `10^6`
steps: cheap once, fatal in a loop over `10^5` values, which is when you switch
to a sieve ([[primes]]).

**Closed forms are not automatically free.** `n(n+1)/2` for `n = 10^9` is about
`5 · 10^17`, comfortably inside a signed 64-bit integer; `n(n+1)(2n+1)/6` for the
same `n` is about `3 · 10^26` and is not. *Sum Multiples of 3, 5, or 7 Below N*
states "the result fits in a signed 64-bit integer", which is the setter telling
you they checked and you should too. See [[big-integers]].

## The implementation

```python run
from collections import defaultdict
import random


def subarrays_divisible(a, k):
    """Count non-empty contiguous subarrays of a whose sum is divisible by k."""
    cnt = defaultdict(int)
    cnt[0] = 1                   # the empty prefix S_0 = 0 is a real index
    s = ans = 0
    for x in a:
        s = (s + x) % k          # reduce every step; s stays inside [0, k)
        ans += cnt[s]            # every earlier prefix sharing this mark
        cnt[s] += 1              # only now does this prefix become 'earlier'
    return ans


def pairs_with_sum_divisible(a, n):
    """Count pairs i < j with (a[i] + a[j]) % n == 0, without n buckets."""
    cnt = defaultdict(int)
    for x in a:
        cnt[x % n] += 1
    total = cnt[0] * (cnt[0] - 1) // 2          # 0 pairs with 0
    for r, c in cnt.items():
        comp = (n - r) % n
        if r == 0:
            continue
        if r < comp:                            # count each pair of marks once
            total += c * cnt.get(comp, 0)
        elif r == comp:                         # n even, r == n // 2
            total += c * (c - 1) // 2
    return total


def brute_sub(a, k):
    return sum(1 for i in range(len(a)) for j in range(i, len(a))
               if sum(a[i:j + 1]) % k == 0)


def brute_pairs(a, n):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a))
               if (a[i] + a[j]) % n == 0)


a, k = [2, 3, 4, 1, 5], 5
print("array", a, "  k =", k)
print("subarrays divisible by 5:", subarrays_divisible(a, k),
      " brute force:", brute_sub(a, k))
assert subarrays_divisible(a, k) == 6

b, n = [3, 1, 2, 6, 1, 2], 3
print("pairs summing to a multiple of 3:", pairs_with_sum_divisible(b, n),
      " brute force:", brute_pairs(b, n))

rng = random.Random(3)
for _ in range(500):
    m, k2 = rng.randint(0, 9), rng.randint(1, 7)
    arr = [rng.randint(-20, 20) for _ in range(m)]
    assert subarrays_divisible(arr, k2) == brute_sub(arr, k2), (arr, k2)
    assert pairs_with_sum_divisible(arr, k2) == brute_pairs(arr, k2), (arr, k2)
print("500 random arrays, negatives included, agree with brute force")

big = [10 ** 9] * 2000           # true prefix sums reach 2*10^12; s never exceeds 6
print("2000 copies of 10^9 with k = 7 ->", subarrays_divisible(big, 7), "subarrays")
assert subarrays_divisible(big, 7) == 285000
```

Four lines carry the chapter.

`cnt[0] = 1` is the base case of the invariant, transcribed. If you can say out
loud "`cnt[r]` is how many prefixes so far have mark `r`, and `S₀ = 0` is a
prefix", you will never forget it; if you memorised it as a rule, you will.

`s = (s + x) % k` reduces on every step rather than at the end. In Python the two
agree, because congruence is preserved by addition. In a fixed-width language
they do not: an unreduced sum overflows, and two's-complement overflow computes
modulo `2^64`, so the final `% k` gives the right answer only when `k` divides
`2^64`. Reduce as you go and the question never arises.

`ans += cnt[s]` sits *before* `cnt[s] += 1`, and that ordering is the `j < l` of
Lemma 1. It is the only place in the loop where the strictness of the inequality
is represented, which is why swapping two adjacent lines produces an answer
inflated by exactly `n`.

In `pairs_with_sum_divisible`, the guard `if r < comp` is what stops every
cross-mark pair being counted twice: marks `r` and `n - r` are complementary in
both directions, so you visit the unordered pair of marks once by fixing an
order. The two special cases are the marks that are their own complement:
`r = 0` always, and `r = n/2` when `n` is even. Both are counted with
`c(c-1)/2` instead of a product, because there both ends of the pair come from
the same class.

## Variants you will meet

**Counting pairs by mark.** Bucket by residue, then combine bucket sizes.
*Nums That Are Divisible by N* is the plain form; *Find Number of Interesting
Pairs* is disguised, since `|x - y| + |x + y|` equals `2·max(|x|, |y|)`, and once
you see that, the condition is a statement about one value per element. See
[[modular-arithmetic]].

**Prefix residues.** The variant proved above — *Count Subarrays With Sum
Divisible by K*. The same table indexed by the sum itself rather than its mark
solves "subarrays summing to exactly `t`"; see [[prefix-sums]].

**A closed form instead of a loop.** The multiples of `d` below `n` are
`d, 2d, …, md` with `m = ⌊(n-1)/d⌋`, summing to `d · m(m+1)/2`. *Sum Multiples of
3, 5, or 7 Below N* is that plus [[inclusion-exclusion]], because a multiple of
both 3 and 5 must not be counted twice. *Arrange Coins* inverts a series: the
largest `r` with `r(r+1)/2 <= c` is one quadratic formula or one
[[binary-search-on-answer]] — and the binary search is safer, because
`(-1 + √(8c+1))/2` in floating point is off by one near the boundary.

**Digit mathematics.** The digital root is `0` for `n = 0` and `1 + (n-1) mod 9`
otherwise, because `10 ≡ 1 (mod 9)` makes a number congruent to its digit sum
mod 9. *Add Digits*, *Sum Digits Until One* and *Most Frequent Reduced Digit* are
all this. Counting numbers *by* a digit property (*Count Numbers with Digit
Sum*) is a different animal and belongs to [[digit-dp]].

**gcd and lcm.** Euclid, `gcd(a, b) = gcd(b, a mod b)`, in `O(log min(a,b))`
steps. *Find Pair with Maximum GCD* and *Minimum Frames for Equal Chunks* use it
numerically; *Sliding-Window Averages as Reduced Fractions* uses it to keep a
fraction canonical; *Greatest Common Divisor of Strings* is the prettiest,
because the answer's length is `gcd(len(s1), len(s2))` and a numeric gcd solves a
string problem outright. See [[number-theory]].

**Primes and factorisation.** Trial division to `√n` for one number (*Find Out
Prime or Composite*), a sieve for many queries (*Prime String*, *Maximum Score
with Prime Jumps*). See [[primes]].

**Answers modulo `10^9 + 7`.** The statement is telling you the count is
astronomical and will never be constructed. Ordinary modular arithmetic, with one
wrinkle: division needs a modular inverse, which [[fast-exponentiation]] supplies
because the modulus is prime. *Count Divisible Permutations* and *Count Valid
A-B-C Sequences Under a Modulo-Four Rule* live here, next to [[combinatorics]]
and [[counting-dp]].

**Solving a congruence.** *Smallest Value for a Linear Expression Modulo* reduces
a 60,000-character expression to `ax + b ≡ p (mod m)` and asks for the smallest
non-negative `x`. Parsing is [[recursive-descent]]; solving is
[[modular-arithmetic]], and there is no solution unless `gcd(a, m)` divides
`p - b`.

**Number bases.** *Excel Sheet Column Title* is base 26 with digits `1..26`
rather than `0..25` — bijective numeration, which is where its off-by-one lives.
*HexSpeak*, *Double-Base Palindromes* and *Nth License Plate* are the same
conversion loop with different alphabets. See [[base-conversion]].

**Bit-level arithmetic.** *Power of Two Without Division* forbids `/` and
`Math.pow`, which is a pointed hint: `n > 0 and n & (n - 1) == 0`, because
subtracting one from a power of two flips its single set bit and everything below
it. See [[bit-manipulation]] and [[xor-tricks]].

**Exact arithmetic instead of floats.** *Return Exact Cash Register Change* hands
you decimal strings: parse to integer cents and never see a `double`.
*Sliding-Window Averages as Reduced Fractions* wants a numerator, a denominator
and a gcd. *Fraction to Recurring Decimal* needs the remainders themselves,
because a repeating block starts exactly when a remainder repeats. When floats
are unavoidable — *Streaming Entropy, Part 2: Numerically Stable Entropy*,
*Sliding-Window Means with IEEE Special Values* — see [[numerical-stability]].

**Integer geometry.** *Circles Relationship* compares `d²` against `(r₁ ± r₂)²`,
so no square root is taken and no precision is lost. *Triangle and Points* and
*Rasterize a Circle with Integer Pixels* are the same discipline. See
[[geometry]].

```python run
def sum_multiples_below(n, divisors=(3, 5, 7)):
    """Sum of the integers in [1, n-1] divisible by at least one divisor."""
    def series(d):                      # d + 2d + ... + md  with m = (n-1)//d
        m = (n - 1) // d
        return d * m * (m + 1) // 2

    def lcm(x, y):
        p, q = x, y
        while q:
            p, q = q, p % q             # Euclid
        return x // p * y

    p, q, r = divisors
    return (series(p) + series(q) + series(r)
            - series(lcm(p, q)) - series(lcm(p, r)) - series(lcm(q, r))
            + series(lcm(lcm(p, q), r)))


def digital_root(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


def slow_root(n):
    while n > 9:
        n = sum(int(ch) for ch in str(n))
    return n


def power_mod(base, exp, mod):
    """base**exp % mod. Invariant: result * base**exp is the original power."""
    result, base = 1 % mod, base % mod
    while exp:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


print("multiples of 3, 5 or 7 below 100 sum to", sum_multiples_below(100))
print("below 10^9 they sum to", sum_multiples_below(10 ** 9), "- computed in 7 terms")
for n in (1, 2, 10, 100, 1000, 12345):
    loop = sum(x for x in range(1, n) if x % 3 == 0 or x % 5 == 0 or x % 7 == 0)
    assert sum_multiples_below(n) == loop, n
print("the closed form agrees with the loop for every n tested up to 12345")

assert all(digital_root(v) == slow_root(v) for v in range(0, 5000))
print("digital_root matches repeated digit summing on 0..4999;",
      "digital_root(2**31 - 1) =", digital_root(2 ** 31 - 1))

M = 10 ** 9 + 7
assert power_mod(2, 10, 1000) == 24
assert all(power_mod(bb, ee, M) == pow(bb, ee, M)
           for bb in range(1, 20) for ee in range(0, 40))
print("3^(10^18) mod (10^9+7) =", power_mod(3, 10 ** 18, M),
      "in", (10 ** 18).bit_length(), "squarings, not 10^18 multiplications")
```

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"Return the answer modulo `10^9 + 7`."** Near-certain. The answer is
   astronomically large, so you are counting configurations rather than producing
   one — [[combinatorics]] or [[counting-dp]] with modular arithmetic underneath.
2. **"divisible by", "remainder", "a multiple of", "`x % k == 0`".** Bucket by
   residue. If the divisibility is of a *sum over a range*, bucket the prefix
   marks; if it is of a *pair or triple*, bucket the values.
3. **The entire input is one or two integers, bounded by `10^9` or more.** There
   is nothing to iterate, so the answer is a closed form, an `O(log n)` process,
   or a `Θ(√n)` scan. *Sum Multiples of 3, 5, or 7 Below N* cannot be a loop
   over `n`.
4. **"exact", "as a reduced fraction", "as a decimal string", or money.** You are
   being warned off floating point. Integers or rationals.
5. **"Return as a long", or "fits in a signed 64-bit integer".** A note about the
   *size* of the answer is a note about how many things are being counted, and so
   about the algorithm: nobody mentions 64 bits for an answer you could
   enumerate.
6. **Many queries against one cheap question.** *Arrange Coins* is `10^5` values
   each up to `10^9`: per query `O(1)` or `O(log)`, nothing per-unit.

The anti-signals:

- **Arithmetic in the statement is not a maths problem.** Averages, prices and
  percentages are usually payload. Ask what varies and what is searched over; if
  the answer is "a window over an array", it is [[sliding-window]] whatever the
  units are.
- **A small bound hiding in the constraints.** *Count Divisible Permutations*
  reads like number theory and caps `n` at 15, which is a bitmask over subsets,
  not a formula — see [[dp-bitmask]]. Read the constraints before reaching for
  cleverness.
- **A rule you inferred from the examples.** If you cannot say why a formula is
  true, you have a conjecture; brute-force it against every small input before
  submitting. See [[testing-your-code]].

## Traps

**The sign of `%`.** In Python `-3 % 5` is `2`. In C, C++, Java, Go, Rust and
JavaScript it is `-2`, because those languages truncate the quotient toward zero
rather than flooring it. Symptom: perfect on every all-positive sample, wrong on
the hidden tests containing negatives. Demonstrated below.

**Losing the empty prefix.** Symptom: the answer is short by exactly the number
of qualifying subarrays that start at index 0. Demonstrated below.

**Counting before you insert, or after.** `ans += cnt[s]` then `cnt[s] += 1` is
correct; reversed, every prefix pairs with itself. Symptom: an answer exactly
`n` too high.

**Overflow of the count, not of the data.** `C(10^5, 2)` is `4,999,950,000`,
more than double `2^31 - 1`. Symptom: a negative answer in a fixed-width
language. This is why *Nums That Are Divisible by N* says "as a long".

**`math.sqrt` on large integers.** `sqrt` goes through a 53-bit float, so
`int(math.sqrt(10**18 - 1))` rounds *up* to `10^9`, whose square exceeds the
input. Symptom: a loop bound one too large, or a perfect-square test that says
yes to a non-square. Use `math.isqrt`, which is exact.

**Floating point for money.** `0.1 + 0.2 != 0.3`. Symptom: one cent off, on one
test, once. Parse to integer cents.

**Dividing under a modulus.** `(a / b) % m` cannot be computed from `a % m` and
`b % m` by dividing; the last self-check has the counterexample.

**`int(x / y)` instead of `x // y`.** For negatives they differ — `int(-7/2)` is
`-3`, `-7 // 2` is `-4` — and for large integers `x / y` loses precision before
the truncation happens at all.

**Counting complementary marks twice.** Marks `r` and `n - r` see each other, so
an unguarded loop doubles every cross-class count while leaving the
self-complementary marks `0` and `n/2` alone. Symptom: an answer that is almost
exactly twice too large, which is worse than one that plainly is.

```python run
import math
from collections import defaultdict


def count(a, k, seed=True, c_style=False):
    cnt = defaultdict(int)
    if seed:
        cnt[0] = 1
    s = ans = 0
    for x in a:
        s += x
        r = int(math.fmod(s, k)) if c_style else s % k   # fmod keeps the sign
        ans += cnt[r]
        cnt[r] += 1
    return ans


a, k = [2, -3, 5, 1, -5], 5
truth = sum(1 for i in range(len(a)) for j in range(i, len(a))
            if sum(a[i:j + 1]) % k == 0)
print("array", a, "  k =", k, "  true answer:", truth)
print("correct               :", count(a, k))
print("C-style remainder     :", count(a, k, c_style=True),
      "<- -1 and 4 fall in different buckets")
print("no empty-prefix seed  :", count(a, k, seed=False),
      "<- loses the subarrays starting at index 0")
assert count(a, k) == truth
assert count(a, k, c_style=True) < truth
assert count(a, k, seed=False) < truth

print()
n = 10 ** 5
pairs = n * (n - 1) // 2
print("pairs among 10^5 items:", pairs, " exceeds 2^31-1 =", 2 ** 31 - 1, "?",
      pairs > 2 ** 31 - 1)
x = 10 ** 18 - 1
print("int(math.sqrt(x)) =", int(math.sqrt(x)), " math.isqrt(x) =", math.isqrt(x),
      " for x = 10^18 - 1")
assert int(math.sqrt(x)) ** 2 > x and math.isqrt(x) ** 2 <= x
print("0.1 + 0.2 == 0.3 ?", 0.1 + 0.2 == 0.3, " -> prices belong in integer cents")
assert 0.1 + 0.2 != 0.3
```

Both wrong variants return a number, both return it fast, and both would pass a
sample case made of small positive integers. That is the entire difficulty with
mathematical bugs: they do not crash.

## What to memorise

Very little. One loop, one question, one reflex.

**The loop**, which should come out of your fingers:

```python
cnt = defaultdict(int)
cnt[0] = 1                # the empty prefix is an index, not a special case
s = ans = 0
for x in a:
    s = (s + x) % k
    ans += cnt[s]         # count first: this enforces j < l
    cnt[s] += 1
```

**The question** that turns a statement into maths: *what is the smallest thing
about each input value that the answer actually depends on, and does it survive
the operation being performed?* If the answer is "its remainder", bucket by
remainder. If it is "nothing — the answer depends only on `n`", look for a closed
form. If it is "the whole value", this is not a maths problem.

**The reflex**: reduce as you go, and in any language whose `%` follows the sign
of the dividend, write `((x % k) + k) % k` without thinking about whether this
particular input can be negative.

Numbers worth carrying: `2^31 - 1 ≈ 2.1 · 10^9` and `2^63 - 1 ≈ 9.2 · 10^18`, so
a product of two values up to `3 · 10^9` still fits in 64 bits and a product of
three does not; `C(10^5, 2) ≈ 5 · 10^9`, past 32 bits; `10^9 + 7` is prime, which
is why modular inverses exist for it; `1 + 2 + … + n = n(n+1)/2`; the digital root
of `n > 0` is `1 + (n-1) mod 9`; all divisors of `n` are found in `⌊√n⌋`
divisions; `log₂(10^18) ≈ 60`, the number of squarings in a fast power.

## Check yourself

:::check
Why does `cnt` have to start as `{0: 1}` rather than empty? Answer in terms of
the invariant, not in terms of "it makes the tests pass".
--
Because invariant (I1) says `cnt[r]` counts the prefix indices `j <= t-1` whose
prefix sum has mark `r`, and before the first iteration that range is `j = 0`
alone. `S₀ = 0` is a prefix sum — the sum of no elements — and its mark is 0. So
`{0: 1}` is not a seed value chosen to fix an edge case; it is the base case of
the induction, transcribed.

Concretely, the pairs `(0, l)` are the subarrays `a[0..l-1]` that start at the
left edge. With an empty `cnt` those pairs can never form, so the answer is low
by the number of prefixes whose own sum is divisible by `k` — zero on many small
samples, not zero on the tests that matter.
:::

:::check
Someone says: "Python integers are arbitrary precision, so reducing inside the
loop is pointless. I will accumulate the true prefix sum and take `% k` only when
I need the bucket." Where are they right, where are they wrong, and what happens
to the same claim in Java?
--
They are right that the *value* is unaffected: congruence is preserved by
addition, so reducing at the end gives the same buckets and the same answer in
Python. They are wrong about cost, and badly wrong about portability.

Cost: the claim generalises in people's heads from sums to products, where it is
false. A running product of `10^4` values near `10^9` has about `300,000` bits,
and every later multiplication and every `%` costs time proportional to that
length. The same reasoning kills `a ** b` in favour of `pow(a, b, m)`.

Portability: in Java, C++ or Go the unreduced sum overflows, and
two's-complement overflow is itself a reduction — modulo `2^64`. So what you
compute is `(S mod 2^64) mod k`, which equals `S mod k` only when `k` divides
`2^64`, i.e. only when `k` is a power of two. On `k = 5` it is simply wrong, in a
way no exception reports.
:::

:::check
*Nums That Are Divisible by N* asks for the number of pairs `i < j` with
`arr[i] + arr[j]` divisible by `N`, for `n <= 10^5` and `N <= 10^9`. Derive the
formula from the bucket sizes, and say why you must not loop `r` from 0 to
`N - 1`.
--
Let `c_r` be the number of indices whose value has mark `r`. The marks partition
the indices, so every pair `(i, j)` falls in exactly one pair of classes. The
pair qualifies iff `mark(arr[i]) + mark(arr[j]) ≡ 0 (mod N)`, i.e. iff
`mark(arr[j]) = (N - mark(arr[i])) mod N`.

When `r` and its complement differ, every element of class `r` pairs with every
element of class `N - r`, giving `c_r · c_{N-r}`; fix an order (`r < N - r`) so
each unordered pair of classes is visited once. When a mark is its own
complement, both ends come from the same class and the count is
`C(c_r, 2) = c_r(c_r - 1)/2` instead. Exactly two marks are self-complementary:
`r = 0` always, and `r = N/2` when `N` is even.

You must not loop over `0 … N-1` because `N` can be `10^9` while the array holds
`10^5` elements: at most `10^5` marks are ever occupied, and an array of `N`
counters is four gigabytes of mostly zeros. Iterating the occupied marks of a
hash map makes the whole thing `Θ(n)`. The answer itself can reach
`C(10^5, 2) ≈ 5 · 10^9`, which is why the statement specifies a long.
:::

:::check
Someone claims: "`(a / b) mod m` is `((a mod m) / (b mod m)) mod m`, same as it
is for `+` and `*`." Give a counterexample and say what the correct statement is.
--
Counterexample: `a = 10`, `b = 5`, `m = 7`. The true value is `10 / 5 = 2`, and
`2 mod 7 = 2`. Their formula gives `(10 mod 7) / (5 mod 7) = 3 / 5`, which is not
even an integer.

The reason is structural. Reduction mod `m` is well defined on `+`, `-` and `×`
because replacing an operand by a congruent one leaves the result congruent.
Division is not an operation on the integers at all, so there is nothing for it
to be compatible with.

The correct statement replaces division by multiplication with a *modular
inverse*: `a / b mod m` means `a · b⁻¹ mod m`, where `b⁻¹` is the unique residue
with `b · b⁻¹ ≡ 1 (mod m)`. It exists iff `gcd(b, m) = 1` — here `5⁻¹ = 3`, and
`10 · 3 mod 7 = 2`, the right answer. When `m` is prime, as `10^9 + 7` is, every
non-zero `b` has one and Fermat's little theorem gives it as `pow(b, m - 2, m)`.
When `gcd(b, m) > 1` there is no inverse and the question has no answer in that
form. See [[modular-arithmetic]] and [[fast-exponentiation]].
:::

:::check
*Greatest Common Divisor of Strings* asks for the longest string `t` such that
both `str1` and `str2` are whole numbers of repetitions of `t`. Why must
`len(t)` divide `gcd(len(str1), len(str2))`, and what does that leave you to
check?
--
If `str1` is `p` copies of `t` then `len(str1) = p · len(t)`, so `len(t)` divides
`len(str1)`; likewise it divides `len(str2)`. A number dividing both lengths
divides their greatest common divisor, so `len(t)` divides `g = gcd(len(str1),
len(str2))`.

That bounds the answer's length by `g`, and a candidate of length `g` is forced
to be `str1[:g]`, since any `t` tiling `str1` must agree with it on the first
`len(t)` characters. So exactly one candidate needs testing: `c = str1[:g]`, with
`c * (len(str1) // g) == str1` and `c * (len(str2) // g) == str2`. If that fails,
nothing shorter works either, because every shorter common divisor would tile
`c`, and then `c` would tile both strings. Return the empty string.

The point to take away: one numeric fact — the gcd of two lengths — collapsed a
search over all substrings into a single equality test, in a problem that does
not look numeric at all.
:::
