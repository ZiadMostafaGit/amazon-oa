# Combinatorics and Counting

> Counting is not a bag of formulas. It is the craft of describing a process
> that builds every object you want exactly once — and then noticing, when it
> builds each of them twice, that you may divide.

## When you reach for it

You reach for counting when the answer is a **number**, the objects counted are
far too many to list, and the statement never asks you to show one. "How many
ways", "count the number of", "return the result modulo 10^9 + 7" — that last
phrase is the loudest signal in the genre, because a modulus is needed only when
the true answer does not fit in a machine word, which puts enumeration out of
reach before you start.

Ninety-three problems here are counting problems — #37 of 150 — in a handful of
shapes:

- **Arrangements** — *Unique String Permutations*, *Generate Circular Student
  Arrangements*, *Valid Times on a Digital Clock*.
- **Selections** — *Count Teams*, *Find Max Number of Pairs*, *Get Triplet Count*.
- **Strings or numbers with a property** — *Count Four-Digit Codes with Sum S*,
  *Count 3 Sister Numbers*, *Ashley Loves Numbers (Financial Engineer)*.
- **Configurations of a structure** — *Drawing Edge* (simple graphs on `n`
  labelled vertices), *Coloring Houses*, *Count Paths from the Top Left to the
  Bottom Right*.
- **Contribution** — *Subarray Sum*: not "how many subarrays" but "add something
  up over all of them".
- **Existence without construction** — the pigeonhole side of the subject, and
  the reason *Arrange Packages With Compatible Adjacent Weights* has a one-line
  answer.

The tool is wrong in two situations. When the statement asks you to *produce* the
objects — *Alternating Parity Permutations* appears here twice, once asking for
the count and once for the list in lexicographic order, and the second is
[[backtracking]], not arithmetic. And, more subtly, when the choices constrain
each other in a way that has no closed form: *Coloring Houses* is still counting,
but the count comes out of a recurrence rather than a product. That is
[[counting-dp]], and knowing when you have crossed the line is most of the
skill.

## The idea

Here is the whole subject in one sentence.

**To count a set, describe a machine that builds each of its elements exactly
once, and count the machine's runs.**

Everything else is a consequence, and there are only three consequences worth
naming.

The **sum rule**: if the set splits into cases that do not overlap and leave
nothing out, add the case counts.

The **product rule**: if each element is built by a sequence of choices, and at
each stage the *number* of available options is the same no matter what was
chosen earlier, multiply the option counts.

The **division rule**: if the machine builds every element exactly `d` times,
the number of elements is (number of runs) / `d`.

The product rule has a subtlety worth ten minutes of your life: it does not
require the options to be the same at each stage, only *how many* of them there
are. *Count 3 Sister Numbers* wants three-digit numbers with three distinct
digits. The leading digit has 9 options (1 through 9), the second has 9 (all ten
minus the one used), the third has 8. The available digits differ wildly down
different branches, but the counts are 9, 9, 8 on every branch, so the answer is
9·9·8 = 648. That freedom is what makes the rule useful rather than trivial.

<svg viewBox="0 0 640 250" role="img" aria-label="a decision tree choosing two of three letters in order, six leaves grouped into three unordered pairs">
  <g>
    <circle class="fill" cx="320" cy="28" r="14"/>
    <circle cx="120" cy="110" r="16"/>
    <text x="120" y="116" text-anchor="middle">A</text>
    <circle cx="320" cy="110" r="16"/>
    <text x="320" y="116" text-anchor="middle">B</text>
    <circle cx="520" cy="110" r="16"/>
    <text x="520" y="116" text-anchor="middle">C</text>
    <line x1="310" y1="40" x2="130" y2="98"/>
    <line x1="320" y1="42" x2="320" y2="94"/>
    <line x1="330" y1="40" x2="510" y2="98"/>
    <circle cx="60" cy="190" r="16"/>
    <text x="60" y="196" text-anchor="middle">B</text>
    <circle cx="180" cy="190" r="16"/>
    <text x="180" y="196" text-anchor="middle">C</text>
    <circle cx="260" cy="190" r="16"/>
    <text x="260" y="196" text-anchor="middle">A</text>
    <circle cx="380" cy="190" r="16"/>
    <text x="380" y="196" text-anchor="middle">C</text>
    <circle cx="460" cy="190" r="16"/>
    <text x="460" y="196" text-anchor="middle">A</text>
    <circle cx="580" cy="190" r="16"/>
    <text x="580" y="196" text-anchor="middle">B</text>
    <line x1="112" y1="124" x2="68" y2="176"/>
    <line x1="128" y1="124" x2="172" y2="176"/>
    <line x1="312" y1="124" x2="268" y2="176"/>
    <line x1="328" y1="124" x2="372" y2="176"/>
    <line x1="512" y1="124" x2="468" y2="176"/>
    <line x1="528" y1="124" x2="572" y2="176"/>
    <text x="320" y="235" text-anchor="middle">3 x 2 = 6 runs; every 2-set is built exactly twice; 6 / 2 = 3</text>
  </g>
</svg>

The division rule carries a precondition that is easy to skip: *every* element
must be built the same number of times. Six ordered pairs give three unordered
pairs because each is built exactly twice. The moment the multiplicity varies
from element to element, division is simply wrong — and no amount of staring at
the formula reveals it.

## Worked by hand

Take *Count Four-Digit Codes with Sum S*: how many strings `d1 d2 d3 d4` over the
digits 0–9 have `d1 + d2 + d3 + d4 = S`? The statement tells us the answer for
`S = 4` is 35, so we have something to check against.

Count it twice and watch the two answers agree.

**First way: the sum rule, splitting on the leading digit.** Fix `d1`; the rest
is the same problem with three digits and a smaller target. For small totals the
cap of 9 never binds, and the number of `(d2, d3, d4)` summing to `r` turns out
to be `C(r + 2, 2)` — justified in a moment.

| `d1` | remaining `r` | `(d2, d3, d4)` with sum `r` | count |
| --- | --- | --- | --- |
| 0 | 4 | 004, 013, 022, …, 400 | `C(6,2)` = 15 |
| 1 | 3 | 003, 012, 021, …, 300 | `C(5,2)` = 10 |
| 2 | 2 | 002, 011, 020, 101, 110, 200 | `C(4,2)` = 6 |
| 3 | 1 | 001, 010, 100 | `C(3,2)` = 3 |
| 4 | 0 | 000 | `C(2,2)` = 1 |
| | | | **35** |

The five cases are disjoint (two codes with different `d1` are different codes)
and exhaustive (`d1` cannot exceed 4 without the sum overshooting), so the sum
rule applies and the total is 15 + 10 + 6 + 3 + 1 = 35.

**Second way: one bijection, no cases at all.** Lay out `S = 4` identical stars
in a row and insert 3 bars among them. Reading the four gaps left to right gives
four digits summing to 4:

<svg viewBox="0 0 640 150" role="img" aria-label="four stars and three bars in seven slots, encoding the digit tuple two one zero one">
  <g>
    <rect class="fill" x="40" y="30" width="60" height="50" rx="5"/>
    <rect class="fill" x="110" y="30" width="60" height="50" rx="5"/>
    <rect x="180" y="30" width="60" height="50" rx="5"/>
    <rect class="fill" x="250" y="30" width="60" height="50" rx="5"/>
    <rect x="320" y="30" width="60" height="50" rx="5"/>
    <rect x="390" y="30" width="60" height="50" rx="5"/>
    <rect class="fill" x="460" y="30" width="60" height="50" rx="5"/>
    <text x="70" y="62" text-anchor="middle">*</text>
    <text x="140" y="62" text-anchor="middle">*</text>
    <text x="210" y="62" text-anchor="middle">|</text>
    <text x="280" y="62" text-anchor="middle">*</text>
    <text x="350" y="62" text-anchor="middle">|</text>
    <text x="420" y="62" text-anchor="middle">|</text>
    <text x="490" y="62" text-anchor="middle">*</text>
    <text x="70" y="22" text-anchor="middle">1</text>
    <text x="140" y="22" text-anchor="middle">2</text>
    <text x="210" y="22" text-anchor="middle">3</text>
    <text x="280" y="22" text-anchor="middle">4</text>
    <text x="350" y="22" text-anchor="middle">5</text>
    <text x="420" y="22" text-anchor="middle">6</text>
    <text x="490" y="22" text-anchor="middle">7</text>
    <text x="40" y="110">bars at {3, 5, 6}  ->  code 2 1 0 1</text>
    <text x="40" y="135">choose 3 of 7 slots: C(7,3) = 35</text>
  </g>
</svg>

Every code corresponds to exactly one choice of 3 bar-slots out of 7, and every
such choice gives back exactly one code, so the count is `C(7, 3) = 35`. Same
answer, no case analysis, and the general formula falls out: the number of
four-digit codes summing to `S` is `C(S + 3, 3)` — *as long as no digit needs to
exceed 9*.

Three things the trace shows that the code would not.

**The two methods are the same identity in disguise.** `C(6,2) + C(5,2) +
C(4,2) + C(3,2) + C(2,2) = C(7,3)` is the hockey-stick identity — here not
something to memorise but a description of what we just did: sorting the 35
bar-placements by where the first bar went.

**The cap is invisible at `S = 4` and decisive at `S = 12`.** No digit can reach
10 when the total is 4, so the formula is exact there. At `S = 12` the naive
`C(15, 3) = 455` counts tuples like `(11, 1, 0, 0)` that are not codes; the true
answer is 415. The gap of 40 is `4 · C(5, 3)`: pick which digit is illegal, hand
it 10 units up front, distribute the remaining 2 freely. That correction is
[[inclusion-exclusion]], the most commonly missing piece of a counting solution.

**The bijection is the proof.** The case analysis convinces; the bijection
explains. Once you have seen stars and bars you never re-derive it — you check
that the problem really is "distribute `S` identical units into `k` labelled
boxes with no upper limit", and write the formula down.

## Why it is correct

Counting proofs are chains, not loop invariants: a few rules, each proved once,
composed into a formula. Here is the chain for `C(n, k)`, ending at the
stars-and-bars theorem used above.

:::proof From the sum rule to stars and bars
**Rule 0 (sum rule).** If a finite set `X` is the disjoint union of
`X_1, …, X_m`, then `|X| = Σ |X_i|`. This is the definition of cardinality for
finite sets; nothing to prove.

**Rule 1 (product rule).** Let `X` be a set of sequences `(c_1, …, c_k)` such
that for every legal prefix `(c_1, …, c_i)` the number of legal continuations
`c_{i+1}` is exactly `n_{i+1}`, independent of the prefix. Then
`|X| = n_1 · n_2 · … · n_k`.

*Induction on `k`.* Base `k = 0`: one empty sequence, and the empty product is 1.
Step: the legal sequences of length `k + 1` partition by their first `k` entries
into `|X_k|` classes — disjoint, since different prefixes give different
sequences — each of exactly `n_{k+1}` members. By Rule 0 the size is
`|X_k| · n_{k+1} = n_1 · … · n_{k+1}`. ∎

**Rule 2 (falling factorial).** The number of ordered sequences of `m` *distinct*
elements drawn from an `n`-set is `P(n, m) = n(n-1)…(n-m+1)`.

Apply Rule 1: after `i` distinct picks there are exactly `n - i` continuations,
because `i` elements are used up. *Which* elements are used depends on the
prefix; how many does not. That is exactly the hypothesis Rule 1 needs.

**Rule 3 (division rule).** If `f : A → B` is surjective and every `b ∈ B` has
exactly `d` preimages, then `|B| = |A| / d`.

*Proof.* The fibres `f⁻¹(b)` are pairwise disjoint and cover `A`, so by Rule 0
`|A| = Σ_{b ∈ B} |f⁻¹(b)| = |B| · d`. ∎

**Theorem A.** The number of `k`-subsets of an `n`-set is
`C(n, k) = P(n, k) / k! = n! / (k!(n-k)!)`.

*Proof.* Let `A` be the ordered sequences of `k` distinct elements, `B` the
`k`-subsets, `f` the map "forget the order". `f` is surjective. Every subset has
exactly `P(k, k) = k!` preimages by Rule 2 applied to the subset itself, and
crucially that number depends only on `k`, so it is the same for every subset.
Rule 3 gives `|B| = P(n, k) / k!`. ∎

**Theorem B (stars and bars).** The number of tuples `(x_1, …, x_k)` of
non-negative integers with `x_1 + … + x_k = n` is `C(n + k - 1, k - 1)`.

*Proof by explicit bijection.* Let `T` be the set of such tuples and `S` the set
of `(k-1)`-subsets of `{1, 2, …, n + k - 1}`. Define
`φ(x_1, …, x_k) = {b_1, …, b_{k-1}}` where `b_i = x_1 + … + x_i + i`.

*Well defined.* `b_1 = x_1 + 1 ≥ 1`, `b_{i+1} - b_i = x_{i+1} + 1 ≥ 1` (so the
`b_i` are strictly increasing), and `b_{k-1} = n - x_k + k - 1 ≤ n + k - 1`.

*Injective.* From the set, sorted as `b_1 < … < b_{k-1}`, recover `x_1 = b_1 - 1`,
`x_i = b_i - b_{i-1} - 1` for `2 ≤ i ≤ k-1`, and `x_k = n + k - 1 - b_{k-1}`.
Distinct tuples therefore have distinct images.

*Surjective.* For any `b_1 < … < b_{k-1}` in range those formulas give
non-negative integers (each difference is at least 1), and their sum telescopes
to `(b_1 - 1) + Σ_{i=2}^{k-1}(b_i - b_{i-1} - 1) + (n + k - 1 - b_{k-1}) = n`.
Every element of `S` is hit.

A bijection preserves cardinality, so `|T| = |S| = C(n + k - 1, k - 1)` by
Theorem A. ∎
:::

Now say plainly what that chain leaned on — the assumptions are where the bugs
live.

- **The sum rule needs disjoint *and* exhaustive cases.** Overlapping cases
  double-count; that is the entire motivation for [[inclusion-exclusion]].
  Splitting on "the first digit" is safe, because a code has one first digit.
  Splitting on "contains a 7" is not.
- **The product rule needs a constant *count* of continuations, not constant
  options.** Distinct digits works (9, 9, 8 on every branch). *Increasing* digits
  does not: after choosing 1 there are 8 continuations, after choosing 7 there are
  2. The moment the count varies by branch, the rule is void.
- **The division rule needs *uniform* fibres.** Every `k`-subset had exactly the
  same `k!` orderings. If some objects have internal symmetry that others lack,
  the fibres differ and dividing by anything is meaningless.
- **Stars and bars needs unbounded parts.** The bijection allows `x_i` as large
  as `n`, so with digits capped at 9 the theorem applies only while the cap cannot
  bind.
- **"Distinct" must be defined by the statement, not by you.** *Drawing Edge*
  says the vertices are *labelled* and that two graphs differ when at least one
  unordered pair differs. That sentence is the whole problem: it makes the answer
  `2^{C(n,2)}`, one free binary choice per pair. Counting graphs up to isomorphism
  instead has no closed form at all.

## What it costs

Counting replaces an enumeration whose cost *is* the answer with arithmetic
whose cost is linear or logarithmic. The first complexity worth stating is the
one you are avoiding: listing the 20-subsets of 40 elements costs
`C(40, 20) ≈ 1.38 × 10^11` steps; computing that number costs 20
multiplications.

**Exact `C(n, k)` by the multiplicative loop.** Iterate
`res = res * (n - i) // (i + 1)` for `i = 0 … k-1`: `k` iterations, one multiply
and one exact divide each, so `Θ(k)` arithmetic operations, halved by taking
`k = min(k, n - k)`. It stays in the integers because of an invariant — after
step `i` the value is `C(n, i+1)`, and `C(n, i) · (n - i) / (i + 1) = C(n, i+1)`
is an identity between integers, so the division never has a remainder. Doing all
the multiplications first is still correct but makes the intermediates
`n!`-sized.

**The cost everyone forgets: the numbers are not O(1).** `C(n, k) ≤ 2^n`, so the
result has `O(n)` bits, and multiplying an `O(n)`-bit number by a small integer
costs `O(n / w)` words — the "`Θ(k)`" loop is really `Θ(k · n / w)`. At
`n = 10^5` the answer has about 30,000 digits ([[big-integers]]). This is one
reason problems impose a modulus.

**Under a modulus.** Precompute `fact[0..n]` in `n` multiplications, then
`inv_fact[n] = pow(fact[n], p-2, p)` — one modular exponentiation, `Θ(log p)`
multiplications by Fermat's little theorem ([[modular-arithmetic]],
[[fast-exponentiation]]) — and walk downwards with
`inv_fact[i-1] = inv_fact[i] * i % p`. Total `Θ(n + log p)` preprocessing, `Θ(1)`
per query. Inverting each factorial separately would cost `Θ(n log p)`; the
backward recurrence is the trick worth knowing.

**Pascal's triangle.** Row `i` has `i + 1` entries, each one addition, so rows
`0…n` cost `Σ (i+1) = (n+1)(n+2)/2 = Θ(n²)` additions and `Θ(n)` space with a
rolling row. Slower, but it needs no division, which makes it the only option
when the modulus is composite.

**Closed form versus size of input.** *Drawing Edge* allows `n` up to `10^9`, so
the exponent in `2^{n(n-1)/2} mod (10^9+7)` is about `5 × 10^17`: nothing to
enumerate, nothing to tabulate. Fast exponentiation costs `Θ(log n)` modular
multiplications, around 60. An `O(n)` solution here is not slow, it is
impossible.

**Inclusion–exclusion.** In general `m` constraints cost `2^m` terms. The capped
stars-and-bars correction is cheap because the events are symmetric: there is one
term per *number* `j` of overflowing variables, and `j` runs only while
`j · (cap + 1) ≤ S`. For four digits capped at 9 that is at most 4 terms, not
16.

## The implementation

One small toolkit, and *Count Four-Digit Codes with Sum S* solved exactly, in
closed form, checked against brute force over all 10,000 codes.

```python run
def n_choose_k(n, k):
    """Exact binomial coefficient, integer arithmetic only."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)                       # C(n,k) == C(n,n-k); halve the work
    res = 1
    for i in range(k):
        res = res * (n - i) // (i + 1)      # exact: this value is C(n, i+1)
    return res


def compositions_capped(total, parts, cap):
    """Tuples of `parts` integers in [0, cap] summing to `total`.
    Stars and bars, minus the tuples where some part overflows."""
    out = 0
    for j in range(parts + 1):
        rest = total - j * (cap + 1)
        if rest < 0:
            break
        sign = -1 if j % 2 else 1
        out += sign * n_choose_k(parts, j) * n_choose_k(rest + parts - 1, parts - 1)
    return out


# the loop invariant, checked explicitly
r = 1
for i in range(8):
    r = r * (12 - i) // (i + 1)
    assert r == n_choose_k(12, i + 1), i
print("invariant holds: after step i the accumulator is C(12, i+1)")

print("C(7,3) =", n_choose_k(7, 3), " C(40,20) =", n_choose_k(40, 20))
assert n_choose_k(7, 3) == 35 and n_choose_k(40, 20) == 137846528820

# brute force over every four-digit code, for every target sum
brute = [0] * 37
for a in range(10):
    for b in range(10):
        for c in range(10):
            for d in range(10):
                brute[a + b + c + d] += 1

for S in range(37):
    assert compositions_capped(S, 4, 9) == brute[S], S
print("closed form matches brute force for every S in 0..36")
print("S = 4  ->", compositions_capped(4, 4, 9), "(the statement says 35)")
print("S = 12 ->", compositions_capped(12, 4, 9),
      "; ignoring the cap would give", n_choose_k(15, 3))
print("sum over all S =", sum(brute), "= 10**4, as it must be")
assert sum(brute) == 10000 and compositions_capped(4, 4, 9) == 35


MOD = 10 ** 9 + 7
N = 2000
fact = [1] * (N + 1)
for i in range(1, N + 1):
    fact[i] = fact[i - 1] * i % MOD
inv_fact = [1] * (N + 1)
inv_fact[N] = pow(fact[N], MOD - 2, MOD)          # one Fermat inversion...
for i in range(N, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD       # ...then all the rest for free

def n_choose_k_mod(n, k):
    if k < 0 or k > n:
        return 0
    return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD

assert all(n_choose_k_mod(30, k) == n_choose_k(30, k) % MOD for k in range(31))
print("modular C(n,k) agrees with the exact one on row 30")
print("Drawing Edge, n = 10**9 ->", pow(2, 10**9 * (10**9 - 1) // 2, MOD))
```

Three lines carry the weight.

`res = res * (n - i) // (i + 1)` is the whole exact binomial. It works because
the accumulator is always a binomial coefficient, never a fraction — the invariant
asserted in the block is the reason `//` is safe. Multiply before you divide.

`inv_fact[i - 1] = inv_fact[i] * i % MOD` turns `n` modular inversions into one.
It is the identity `1/(i-1)! = i · 1/i!` read backwards. Anyone who calls `pow`
inside the loop has written an `O(n log p)` preprocessing step for no reason.

`pow(2, 10**9 * (10**9 - 1) // 2, MOD)` is *Drawing Edge* in one expression:
`C(n, 2)` independent binary choices, one per unordered pair, with the exponent
computed as an ordinary integer and only then fed to modular exponentiation.

## Variants you will meet

**Permutations of a multiset.** `n! / (c_1! c_2! … c_m!)` when letters repeat:
the machine that permutes positions builds each distinct string exactly `∏ c_i!`
times, uniformly, which licenses the division. *Unique String Permutations* is
this directly. Generation rather than counting is [[permutations]].

**Circular arrangements.** `n` people round a table: `(n-1)!`, because the `n`
rotations of a seating are the same seating — a uniform fibre of size `n`.
*Generate Circular Student Arrangements* lives here; check whether reflections
count as identical too, which divides by another 2.

**Lattice paths.** A monotone path across an `m × n` grid is a sequence of `m-1`
downs and `n-1` rights, so there are `C(m+n-2, m-1)` of them. *Count Paths from
the Top Left to the Bottom Right* is the formula; add obstacles and it dies,
replaced by [[dp-2d]].

**Complementary counting.** *Count 2x2 Submatrices by Black Cells* has up to
`10^5` rows and columns, so its `(rows-1)(cols-1)` blocks cannot be visited — but
at most 500 cells are black, each touching at most 4 blocks. Bucket those few
blocks and subtract from the total to get the count for zero.

**Counting by contribution.** Instead of "how many objects have property P", ask
"for each small thing, in how many objects does it appear", and sum. *Subarray
Sum* wants the total of all subarray sums; there are `n(n+1)/2` subarrays, but
`a[i]` appears in exactly `(i+1)(n-i)` of them — a left endpoint at or before `i`,
a right endpoint at or after it — so the answer is `Σ a[i](i+1)(n-i)` in one
pass.

```python run
def total_of_all_subarray_sums(a):
    n = len(a)
    return sum(a[i] * (i + 1) * (n - i) for i in range(n))


def brute(a):
    n = len(a)
    return sum(sum(a[i:j + 1]) for i in range(n) for j in range(i, n))


import random
rng = random.Random(5)
for _ in range(300):
    n = rng.randint(1, 9)
    a = [rng.randint(-9, 9) for _ in range(n)]
    assert total_of_all_subarray_sums(a) == brute(a), a
print("300 random arrays: contribution formula equals the O(n^2) recount")

a = [1, 2, 3, 4]
print("array", a)
for i in range(4):
    print("  a[%d]=%d appears in (%d)(%d) = %2d subarrays"
          % (i, a[i], i + 1, 4 - i, (i + 1) * (4 - i)))
print("total of all subarray sums =", total_of_all_subarray_sums(a))
assert total_of_all_subarray_sums(a) == brute(a) == 50
```

**Derangements.** Permutations with no fixed point:
`D(n) = (n-1)(D(n-1) + D(n-2))`, from `D(0) = 1`, `D(1) = 0` — 1, 0, 1, 2, 9, 44,
265, … That is *Count Array Derangements*; the closed form `n! Σ (-1)^i / i!` is
[[inclusion-exclusion]] applied to "position `i` is fixed".

**Choose-two everywhere.** `C(c, 2) = c(c-1)/2` is the bank's most reused
formula: *Find Max Number of Pairs* groups by digit length and counts pairs inside
each group, *Drawing Edge* raises 2 to this power. *Count Teams* wants the
binomial *sum* `Σ_{k ≥ minPlayers} C(m, k)`, where knowing the whole row sums to
`2^m` turns it into a subtraction.

**When the product rule fails: a recurrence.** *Coloring Houses*, *Count Good
Strings*, *Strings With No k Consecutive Identical Characters* and *Can You Count
the Bit Strings?* all constrain choices that are far apart, so the continuation
count varies by branch and the answer becomes a recurrence: [[counting-dp]], with
[[dp-1d]] as machinery.

### Pigeonhole and counting arguments

The other half of the subject uses counting to prove something *must exist*,
without producing it.

**Pigeonhole principle.** If `n` objects go into `m` boxes and `n > m`, some box
holds at least two. The proof is the sum rule read backwards: if every box held at
most one the total would be at most `m < n`. The averaging form is stronger and
just as easy — some box holds at least `⌈n/m⌉`, since otherwise the total is at
most `m(⌈n/m⌉ - 1) < n`.

Three ways it shows up.

*Existence without construction.* Among the `n+1` prefix sums of an array of
length `n`, two are congruent modulo `n` — `n+1` objects, `n` residue boxes — so
the subarray between them has a sum divisible by `n`. The argument proves such a
subarray exists but never says where; finding it is a separate `O(n)` pass with a
dictionary ([[prefix-sums]]).

*Impossibility.* *Arrange Packages With Compatible Adjacent Weights* asks whether
packages of weight 0–9 can be lined up so every adjacent pair sums to under 10.
Call a package *heavy* if its weight is at least 5. Two heavy packages side by
side sum to at least 10, so no two may be adjacent — and in a row of `n`
positions a set with no two adjacent has size at most `⌈n/2⌉`. More than `⌈n/2⌉`
heavy packages therefore makes the answer "no" immediately, with nothing searched.

*Bounding a state space.* A process with `k` distinct states, run for `k+1`
steps, must repeat a state and so is eventually periodic. That is the counting
argument underneath [[cycle-detection]], and the reason "simulate until something
repeats" has a bound at all.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"Modulo 10^9 + 7", or "the answer can be very large".** Nearly conclusive:
   the count is too big for 64 bits, so it is computed rather than enumerated, and
   you will need [[modular-arithmetic]].
2. **"How many ways", "count the number of", "return the count".** The word
   *count* with no request for the objects themselves.
3. **A definition of when two objects are *different*.** *Drawing Edge*: "two
   graphs are different when at least one pair of vertices has a different edge
   choice." *Valid Times on a Digital Clock*: "equal arrangements caused by
   repeated digits count only once." That sentence names the equivalence relation
   you are counting classes of. It is never filler.
4. **A huge bound on a structural parameter.** `1 <= n <= 10^9` in a counting
   question means closed form: no array of that length, no DP table.
5. **A tiny bound.** `1 <= n <= 11` in *Alternating Parity Permutations* makes
   `11! ≈ 4 × 10^7` affordable, and brute force is the intended answer. Small
   limits are permission, not a challenge.
6. **"Sum over all subarrays / subsets / pairs".** A counting problem in disguise:
   count how often each element contributes.

The anti-signals:

- **"Return all …", "print them in lexicographic order", "list every".** You must
  generate, so use [[backtracking]] or [[subsets]]; the count only tells you
  whether generation is affordable.
- **Choices that constrain each other unboundedly.** Adjacency rules, "no three
  in a row", running totals that must stay non-negative — the option count varies
  by branch, the product rule dies, and you are in [[counting-dp]].
- **"The most / the fewest you can achieve".** Optimisation in a counting
  costume: [[greedy]] or [[dynamic-programming]].
- **Counting up to relabelling.** For symmetry classes of *unlabelled* objects the
  fibres differ, the division rule does not apply, and elementary formulas will be
  wrong.

## Traps

**Ordered when the problem means unordered, or the reverse.** Symptom: the answer
is exactly `2×` (or `k!×`) the expected one, on every test. Name the objects out
loud: a *pair of players* is unordered, a *first and second place* is not.

**Off-by-one in stars and bars.** `k` boxes need `k - 1` bars in `n + k - 1`
slots. Check `S = 0` (answer 1) and `S = 1` (answer `k`) before trusting it.

**Forgetting the upper bound on a part.** Symptom: correct for small inputs,
too large for big ones — exactly the shape that passes the sample and fails the
submission. Demonstrated below.

**Dividing when the fibres are not uniform.** Symptom: an answer that is not even
an integer, or one that is an integer and silently wrong. Demonstrated below.

**Dividing under a modulus with `//`.** `(a // b) % p` is not `a * inverse(b) % p`.
Symptom: wildly wrong numbers. Use `pow(b, p - 2, p)` for prime `p`; for a
composite modulus avoid division and build Pascal's triangle.

**Reducing an exponent modulo `p`.** `2^e mod p` is *not* `2^(e mod p) mod p`.
Fermat's little theorem reduces exponents modulo `p - 1`, not `p`, and only when
the base is not a multiple of `p`. In *Drawing Edge* the exponent fits in 64 bits
anyway, but the intermediate `n(n-1) ≈ 10^18` sits close enough to the ceiling
that halving first is the safer order ([[big-integers]]).

**Leading zeros.** Count all arrangements, then subtract those beginning with 0 —
the same formula on a smaller multiset. *Unique Digit Permutations Without Leading
Zero* hinges on it.

**Treating a pigeonhole argument as constructive.** It proves existence only.
Symptom: a proof that a solution exists, followed by a brute-force search to find
it, because the argument gave no location.

```python run
from math import comb
from itertools import product

# TRAP 1: forgetting the cap on each digit
S = 12
uncapped = comb(S + 3, 3)
capped = sum((-1) ** j * comb(4, j) * comb(S - 10 * j + 3, 3)
             for j in range(2) if S - 10 * j >= 0)
truth = sum(1 for c in product(range(10), repeat=4) if sum(c) == S)
print("digit sum 12:  uncapped C(15,3) =", uncapped,
      " corrected =", capped, " truth =", truth)
assert uncapped == 455 and capped == truth == 415
print("  the naive formula counts tuples like (11,1,0,0), which are not codes")

# TRAP 2: dividing when the overcount is not uniform
bag = [1, 1, 2]
ordered = [(bag[i], bag[j]) for i in range(3) for j in range(3) if i != j]
print("\nbag", bag, "-> ordered index pairs:", len(ordered))
print("  'divide by 2' says", len(ordered) // 2, "distinct value pairs")
distinct = {tuple(sorted(p)) for p in ordered}
print("  the truth is", len(distinct), ":", sorted(distinct))
assert len(ordered) == 6 and len(distinct) == 2
from collections import Counter
fibres = Counter(tuple(sorted(p)) for p in ordered)
print("  fibre sizes:", dict(fibres), "- not all equal, so division is void")
assert set(fibres.values()) == {4, 2}

# the same division IS valid when the fibres are uniform
people = ["a", "b", "c", "d"]
ordered_pairs = [(x, y) for x in people for y in people if x != y]
unordered = {frozenset(p) for p in ordered_pairs}
print("\n4 distinct people: ordered", len(ordered_pairs),
      "/ 2 =", len(ordered_pairs) // 2, "== C(4,2) =", comb(4, 2))
assert len(unordered) == len(ordered_pairs) // 2 == comb(4, 2) == 6
```

Trap 2 is the one worth staring at. Both computations divide six by two, and only
one is allowed. With four distinct people every unordered pair came from exactly
two ordered pairs — uniform fibres, Rule 3 applies. With the bag `[1, 1, 2]` the
pair `(1, 2)` came from four ordered index pairs and `(1, 1)` from two, so
`6 / 2 = 3` answers no question at all. No formula warns you; only the sentence
"is every object built the same number of times?" does.

## What to memorise

Three rules, one sentence, one habit.

**The rules.** Sum rule: disjoint cases add. Product rule: independent stages
multiply, where "independent" means the *number* of continuations is constant.
Division rule: if every object is built exactly `d` times, divide by `d`.

**The sentence** that turns a problem into arithmetic: *"Describe a machine that
builds every one of these objects exactly once."* If the machine builds each
object the same number of times, divide. If it builds some objects more often
than others, you do not have a formula — you have a recurrence.

**The habit.** Before trusting any closed form, compute the smallest cases by
hand — `n = 1`, `S = 0` — and then the *boundary of the assumption*, the first
input where a cap can bind. A counting bug produces a plausible number, never a
crash, so hand-verification is the only detector you have.

Numbers worth carrying: `C(n,2) = n(n-1)/2`; an `n`-set has `2^n` subsets and
`n!` orderings; `21!` is the first factorial past `2^63`; `C(40,20) ≈ 1.4 ×
10^11`; `10^9 + 7` is prime, so `pow(x, p-2, p)` inverts; row `n` of Pascal's
triangle sums to `2^n`.

## Check yourself

:::check
Why is `C(n, k) = n! / (k!(n-k)!)` a *theorem* rather than a definition — and
where does the `k!` come from?
--
What is proved is that an arithmetic expression counts a set: the `k`-element
subsets of an `n`-set.

The argument is a double count. Ordered sequences of `k` distinct elements number
`P(n,k) = n!/(n-k)!`, valid because after `i` picks exactly `n-i` elements remain
whichever `i` were picked. Forget the order: each `k`-subset arises from exactly
`k!` of those sequences, its own orderings, so the fibres are uniform and Rule 3
gives `P(n,k)/k!`.

The `k!` is the fibre size, and its not varying from subset to subset is the whole
justification for dividing.
:::

:::check
Someone says: "*Count Four-Digit Codes with Sum S* is just stars and bars — the
answer is `C(S+3, 3)`, so for `S = 12` it is `C(15,3) = 455`." Where are they
wrong, and what is the correct answer?
--
They have used a theorem outside its hypotheses. Stars and bars counts
non-negative solutions of `x1 + x2 + x3 + x4 = S` with **no upper bound on any
part**. Digits are capped at 9, and among those 455 tuples are `(12,0,0,0)`,
`(11,1,0,0)` and others that are not codes.

Correct it with [[inclusion-exclusion]]. Let `A_i` be the solutions with
`x_i ≥ 10`; substituting `x_i' = x_i - 10` gives `|A_i| = C(S-10+3, 3) = 10`, and
there are 4 choices of `i`. Two parts cannot both reach 10 when `S = 12`, so the
higher terms vanish: `455 - 40 = 415`.

Their formula is exactly right for `S ≤ 9`, which is why the bug survives the
sample case `S = 4`. The habit that catches it is testing the formula at the first
input where the assumption can break — here `S = 10`.
:::

:::check
*Drawing Edge* gives `n` up to `10^9` and asks for the number of simple
undirected graphs on `n` labelled vertices, modulo `10^9 + 7`. What do you
compute, and why would reducing the exponent modulo `10^9 + 7` be wrong?
--
Each of the `C(n,2) = n(n-1)/2` unordered pairs independently has an edge or does
not, and the statement says two graphs differ when any one pair differs. Two
options per pair, independent of the others, so the product rule gives
`2^{n(n-1)/2}` — about 60 squarings by fast exponentiation.

Reducing the exponent modulo `p` is wrong because exponents do not live in the
same ring as the base. Fermat's little theorem gives `2^{p-1} ≡ 1 (mod p)`, so
exponents reduce modulo **`p - 1`**, not `p`. Using `p` shifts every exponent by
an unpredictable amount and returns a plausible wrong number. Here no reduction
is needed at all: the exponent fits in 64 bits.
:::

:::check
Show that every array of `n` integers has a non-empty contiguous subarray whose
sum is divisible by `n`. Then say precisely what the argument does *not* give you.
--
Let `P_0 = 0` and `P_i = a_0 + … + a_{i-1}`: that is `n + 1` prefix sums, each
with a residue in `{0, …, n-1}` — `n` boxes. Pigeonhole forces `P_i ≡ P_j (mod n)`
for some `i < j`, and then `P_j - P_i = a_i + … + a_{j-1}` is divisible by `n` and
non-empty.

What it does not give: *which* subarray. The proof never names `i` and `j`, only
asserts a collision must occur; locating it is a separate `O(n)` pass keeping a
dictionary from residue to earliest index ([[prefix-sums]], [[hash-tables]]). Nor
does it generalise — replace `n` by any `m > n` and `n + 1` objects no longer
outnumber the boxes.
:::

:::check
*Coloring Houses* wants colourings of `n` houses with three colours where no two
adjacent houses share a colour **and** houses equidistant from the two ends
differ. Why does the product rule give `3 · 2^{n-1}` for the first condition, and
why does the second break the method?
--
Build the row left to right. House 1 has 3 options; every later house must avoid
exactly one colour, its left neighbour's, so it has exactly 2. The *set* of
allowed colours depends on what came before, but the *count* is 2 on every
branch — precisely the hypothesis the product rule needs. Hence `3 · 2^{n-1}`.

The second condition pairs house `i` with house `n+1-i` at the far end, so by the
time you reach `n+1-i` the number of colours still available depends on a house
far back in the construction order. The continuation count now varies by branch
and the hypothesis fails.

The repair is to change the construction order: walk in from both ends a pair at
a time, carrying as state how the current pair relates to the previous one. The
count then obeys a recurrence over a constant number of states — [[counting-dp]],
mechanically [[state-design]].
:::
