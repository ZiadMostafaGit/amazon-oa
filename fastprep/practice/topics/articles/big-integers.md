# Big Integers and Overflow

> Overflow is not an error the machine reports. It is a silent change of number
> system — from the integers to the integers modulo 2⁶⁴ — and the whole skill is
> knowing where your answer leaves the range in which the two still agree.

## When you reach for it

This is the most common topic in this bank that is never the *algorithm*. Two
hundred and fourteen problems here touch it, which puts it at #18 of 150, and in
almost none of them is "big integers" the technique you are being tested on. It
is the constraint you have to honour while doing something else. The statement
says it out loud and then moves on:

- *Get Success Value* — "Each success value is at most 10¹⁴ and requires a 64-bit
  integer."
- *Allocate Workers for a Production Ratio* — "total \* firstRatio and total \*
  secondRatio fit in a signed 64-bit integer."
- *Count Power Products in Range* — "Implementations should avoid overflow when
  generating powers of 3 and 5."
- *Best Average Student Score* — "Compare averages exactly; do not rely on
  floating-point rounding."

Each one is a problem setter telling you where their reference solution nearly
broke. The first: your accumulator must be wider than your elements. The second:
the *intermediate* product is the dangerous value, not the answer. The third: the
loop that generates candidates will run past the ceiling unless you stop it. The
fourth: there is a division in the obvious solution and you must not perform it.

So the trigger is not a phrase. It is an arithmetic question you ask about every
problem, whether or not the statement raises it: **what is the largest magnitude
any intermediate value takes, and does it fit in the width I am computing in?**
Multiply the constraint bounds together before you write a line. If `n ≤ 10⁵` and
`|values| ≤ 10⁹`, a sum reaches 10¹⁴ — fine in 64 bits, catastrophic in 32. If
two values of 10⁹ get multiplied, that is 10¹⁸, which fits in a signed 64-bit
integer with less than a factor of ten to spare. Multiply a third and you are out
by eight orders of magnitude.

The tool is the wrong one in two neighbouring cases. If the statement says
"return the answer modulo 10⁹ + 7", you are not fighting overflow — you have been
handed a different ring to compute in, and that is [[modular-arithmetic]]. If the
quantities are genuinely real-valued — an average you must *report*, a distance,
a probability — the question is about representable precision rather than range,
and that is [[numerical-stability]]. The distinction is worth holding: range
errors wrap, precision errors drift, and the fixes have nothing in common.

One honest note, because you are probably writing Python. Python's `int` is
arbitrary precision, so you cannot overflow it — and the chapter still applies,
for three reasons developed below: the constraint line tells you what algorithm
was intended; a Python `int` is not free, so leaning on unbounded integers can go
quadratic; and `float` is still fixed width, so every `/`, `**` and `math.sqrt`
lets the problem back in through the back door.

## The idea

**A fixed-width integer is a clock face.**

An n-bit register has 2ⁿ distinct states, arranged in a cycle. Adding 1 moves one
position clockwise; adding `k` moves `k` positions; subtracting moves the other
way; multiplying is repeated movement. When you walk past the end you do not fall
off — you arrive back where you started. The hardware has no notion of "too big".
It has 2ⁿ positions and it counts around them.

That picture explains the whole topic, because a cycle of 2ⁿ positions under
addition and multiplication *is* the ring **Z/2ⁿZ**. Fixed-width arithmetic is
not broken arithmetic; it is exact arithmetic in a different number system.

The signed/unsigned question is then just a labelling choice. The same wheel, the
same 2ⁿ positions; you only choose where to cut it when reading a position back
out as an integer. Unsigned reads the positions as `0 … 2ⁿ − 1`. Signed cuts the
wheel at the halfway point and reads the far half as negative, so the positions
run `0, 1, …, 2ⁿ⁻¹ − 1, −2ⁿ⁻¹, …, −1`. "Overflow" means: the true answer walked
past the cut.

<svg viewBox="0 0 440 280" role="img" aria-label="a clock face of two-to-the-n positions, with the cut between the largest positive value and the most negative value">
  <g>
    <circle cx="220" cy="140" r="95" fill="none"/>
    <circle class="fill" cx="220" cy="45" r="5"/>
    <text x="220" y="30" text-anchor="middle">0</text>
    <circle class="fill" cx="315" cy="140" r="5"/>
    <text x="330" y="145">growing</text>
    <circle class="fill" cx="125" cy="140" r="5"/>
    <text x="110" y="145" text-anchor="end">negative</text>
    <circle class="fill" cx="220" cy="235" r="5"/>
    <line x1="220" y1="215" x2="220" y2="262"/>
    <text x="220" y="277" text-anchor="middle">the cut</text>
    <text x="300" y="215">2^(n-1) - 1</text>
    <text x="140" y="215" text-anchor="end">-2^(n-1)</text>
    <line x1="268" y1="222" x2="300" y2="246"/>
    <line x1="300" y1="246" x2="286" y2="245"/>
    <line x1="300" y1="246" x2="297" y2="233"/>
    <text x="360" y="255" text-anchor="middle">a + b</text>
    <text x="360" y="272" text-anchor="middle">walks past it</text>
  </g>
</svg>

The second half of the idea is what happens when a language refuses to have a
cut at all. Python's `int` stores a number as an **array of limbs**: base-2³⁰
digits, least significant first, plus a sign. There is no wheel, only a longer
and longer array. Every operation is schoolbook arithmetic on that array, so the
cost of `a + b` is proportional to the number of limbs, and the cost of `a * b`
is worse than that.

<svg viewBox="0 0 560 130" role="img" aria-label="a Python integer drawn as an array of thirty-bit limbs with place values">
  <g>
    <rect x="30" y="35" width="110" height="42" rx="4"/>
    <rect x="150" y="35" width="110" height="42" rx="4"/>
    <rect x="270" y="35" width="110" height="42" rx="4"/>
    <rect x="390" y="35" width="110" height="42" rx="4"/>
    <text x="85" y="61" text-anchor="middle">limb 0</text>
    <text x="205" y="61" text-anchor="middle">limb 1</text>
    <text x="325" y="61" text-anchor="middle">limb 2</text>
    <text x="445" y="61" text-anchor="middle">limb 3</text>
    <text x="85" y="97" text-anchor="middle">x 1</text>
    <text x="205" y="97" text-anchor="middle">x 2^30</text>
    <text x="325" y="97" text-anchor="middle">x 2^60</text>
    <text x="445" y="97" text-anchor="middle">x 2^90</text>
    <text x="30" y="25">30 bits each; d limbs cost O(d) to add, O(d^2) to multiply</text>
    <text x="30" y="120">no cut, no wrap - but no constant-time arithmetic either</text>
  </g>
</svg>

So there are exactly two cost models in this chapter, and you must know which one
you are in. On the wheel, arithmetic is free and range is scarce. In the limb
array, range is free and arithmetic is not.

## Worked by hand

Take an 8-bit signed register: 256 positions, cut so it holds `−128 … 127`. Add
the four values `50, 60, 40, −70` one at a time, keeping two columns — the true
running sum in ordinary integers, and what the register actually holds. Also
track the largest running sum seen so far, because that is the quantity a
[[kadane|maximum-subarray]] or [[prefix-sums|prefix-sum]] solution really wants.

Wrapping is arithmetic modulo 256, read back with the cut at 128: a stored
position `p` reads as `p` if `p < 128`, otherwise `p − 256`.

| step | add | true sum | int8 register | equal? | max prefix (true / int8) |
| --- | --- | --- | --- | --- | --- |
| 1 | +50 | 50 | 50 | yes | 50 / 50 |
| 2 | +60 | 110 | 110 | yes | 110 / 110 |
| 3 | +40 | 150 | 150 − 256 = **−106** | **no** | 150 / 110 |
| 4 | −70 | 80 | −106 − 70 = −176, +256 = **80** | yes | 150 / 110 |

Three things fall out of that table, and none of them is visible in the code.

**The overflow healed itself.** At step 3 the register held −106 while the truth
was 150 — a difference of exactly 256. At step 4 both read 80. The final sum is
*correct*, despite an intermediate being wildly wrong. This is not luck: 150 and
−106 are the same position on the wheel, so every later addition moves both by
the same amount and they land together. That is the theorem the next section
proves, and it is why you cannot find overflow bugs by printing intermediates and
squinting — the intermediates lie and the answer is often still right.

**The comparison did not heal.** The maximum prefix sum is 150 in truth and 110
in the register, and no later step repairs it, because `max` is a *decision*
taken on the value, not an addition applied to it. The moment you compare, sort,
branch, index or divide, the wheel and the integers part company permanently. So
the bug does not appear where the overflow happened; it appears at the next
comparison, possibly a thousand lines later. *Longest Subarray with Sum at Most
K* and *Maximum Subarray Sum* are exactly this shape: running sums compared
against a bound.

**Nothing was reported.** No exception, no warning. The register did precisely
what it is built to do. If you want to be told, you must ask *before* the
operation, never after — a point the traps section demonstrates.

## Why it is correct

The claim to prove is not "overflow is bad". It is the sharper, more useful
statement: for `+`, `−` and `×`, fixed-width arithmetic never loses information
about the true value *modulo the width*, so intermediate overflow is harmless and
only the final magnitude matters.

:::proof Fixed-width arithmetic computes the true value modulo 2ⁿ
**Setup.** Let `W = 2ⁿ` and let the register hold one of the residue classes of
`Z/WZ`, written as a pattern in `{0, …, W − 1}`. The hardware's add, subtract and
multiply are defined to produce the low `n` bits of the exact result, which is
precisely reduction modulo `W`. Let `E` be an arithmetic expression built from
integer literals and the operators `+`, `−`, `×`. Write `val(E)` for its value in
`Z` and `reg(E)` for the pattern the machine ends up holding.

**Invariant.** For every subexpression `E`: `reg(E) ≡ val(E) (mod W)`.

**Base case.** `E` is a literal `v` with `−W/2 ≤ v < W/2`. The compiler stores
the pattern `v mod W`, so `reg(E) ≡ val(E)`.

**Inductive step.** Suppose `E = A ∘ B` with `∘ ∈ {+, −, ×}`, and by induction
`reg(A) ≡ val(A)` and `reg(B) ≡ val(B)` modulo `W`. The machine computes
`reg(E) = (reg(A) ∘ reg(B)) mod W`. The quotient map `π : Z → Z/WZ` is a ring
homomorphism — reduction commutes with addition, subtraction and multiplication —
so

  `π(val(E)) = π(val(A)) ∘ π(val(B)) = π(reg(A)) ∘ π(reg(B)) = π(reg(E))`,

which is the invariant for `E`. Structural induction over the finite expression
tree gives the invariant at the root; the recursion terminates because each
subexpression is strictly smaller than its parent.

**Decoding.** The signed read-back is the map `dec : {0, …, W − 1} → Z` with
`dec(p) = p` if `p < W/2` and `p − W` otherwise. It is a bijection onto
`[−W/2, W/2 − 1]`, and it is the identity on any integer already in that
interval. Hence `dec(reg(E))` is the unique integer in `[−W/2, W/2 − 1]`
congruent to `val(E)` modulo `W`.

**Conclusion.** `dec(reg(E)) = val(E)` **if and only if** `val(E)` lies in
`[−2ⁿ⁻¹, 2ⁿ⁻¹ − 1]`. The values of the intermediate subexpressions are
irrelevant: they may be arbitrarily far outside the range without affecting the
final answer, and conversely no sequence of in-range intermediates can rescue a
final value that is out of range. ∎
:::

Now name what that argument leaned on, because the assumptions are where the
bugs live.

- **Only `+`, `−`, `×`.** Those three are the ring operations, and only they
  commute with reduction. Integer division does not: `150 // 4 = 37` but
  `(−106) // 4 = −27`, and the two are not congruent modulo 256. Shifts, `%`,
  `abs`, comparison, `min`/`max`, array indexing and any `if` on the value all
  break the invariant at the point you use them.
- **A single width throughout.** The proof used one `W`. Mix a 32-bit value into
  a 64-bit expression and there is a hidden reduction modulo 2³² in the middle;
  the surviving guarantee is congruence modulo the *smallest* width that appeared,
  not the largest. This is the `long total = a * b;` bug, where `a` and `b` are
  `int` and the multiplication has already wrapped before the widening assignment
  runs.
- **Literals start in range.** A constant the source writes as `3000000000` in a
  32-bit context is already a different number before any operation happens.
- **The machine wraps, and the language lets it.** On the hardware this is
  universally true. In *languages*, it is guaranteed for Java, C#'s `unchecked`,
  Go, Rust's `wrapping_*` operations, and C/C++ *unsigned* types. It is
  emphatically not guaranteed for signed overflow in C and C++, which is
  undefined behaviour: the compiler is allowed to assume it never occurs, and
  will delete a test like `if (a + b < a)` written afterwards, because under that
  assumption the test can never fire. The theorem above is about the wheel; a
  language standard can decline to describe the wheel.
- **The final value is what you check.** The proof says intermediate overflow is
  harmless, which sounds like permission. It is not. It is harmless *only* for a
  straight-line expression in `+`, `−`, `×` whose result you then use as a number.
  A loop that compares as it goes — which is almost every loop you will write — is
  outside the theorem's scope from the first comparison onwards.

## What it costs

Two cost models, as promised. Do both derivations at least once.

### On the wheel: counting bits before you write code

Every operation is a constant number of machine instructions, so the
"complexity" of fixed-width arithmetic is really a *sizing* question, answered by
a counting argument on bits.

Adding `n` values each of magnitude at most `V` gives a result of magnitude at
most `nV`, so the accumulator needs `⌈log₂(nV)⌉ + 1` bits including the sign. With
`n = 10⁵` and `V = 10⁹`, that is `log₂(10¹⁴) ≈ 46.5`, so 48 bits: comfortable in
64, impossible in 32. This is precisely the bound *Get Success Value* states for
you — "at most 10¹⁴ and requires a 64-bit integer" — and it is the derivation
behind almost every "fits in a signed 64-bit integer" line in this bank.

Multiplying `k` values each at most `V` needs `k·log₂ V + 1` bits, which grows
*linearly in the number of factors*. That is why products are the usual culprit.
Two values of 10⁹ need 60 bits and fit. Three need 90 and do not. *Allocate
Workers for a Production Ratio* has `total ≤ 10⁹` and `firstRatio ≤ 10⁹` and
tells you the product fits — meaning the intended solution forms `total *
firstRatio` and then divides, and you must do the multiply in 64-bit width, not
32.

Counting pairs has the same shape: `n = 2·10⁵` on each side of *Count Cross-Array
Target-Sum Pairs* means up to `4·10¹⁰` matching pairs, ten times past the 32-bit
ceiling, though every individual value is a 32-bit integer. The count overflows,
not the data.

Three numbers make all of this arithmetic mental: `2³¹ − 1 ≈ 2.15·10⁹`,
`2⁶³ − 1 ≈ 9.22·10¹⁸`, and `2⁵³ ≈ 9.01·10¹⁵` (the last is where a double stops
representing consecutive integers).

### In the limb array: when Python's integers are not free

A `b`-bit number occupies `d = ⌈b/30⌉ limbs`. Addition and comparison are `Θ(d)`;
schoolbook multiplication of a `d₁`-limb by a `d₂`-limb number is `Θ(d₁d₂)`, with
CPython switching to Karatsuba above a few dozen limbs for `Θ(d^1.585)`.
Conversion between decimal text and binary limbs is quadratic in the digit count,
which is why recent CPython refuses `int(s)` beyond a few thousand digits unless
you raise the limit explicitly.

That turns some innocent loops quadratic. Computing `n!` by repeated
multiplication: after `k` steps the accumulator has `Θ(k log k)` bits, i.e.
`Θ(k log k)` limbs up to the constant `1/30`, and multiplying it by a
machine-sized factor costs that many limb operations. Summing,

  `Σ_{k=1}^{n} Θ(k log k) = Θ(n² log n)`

limb operations, not `Θ(n)`. Iterating Fibonacci is the same story without the
log: `F_n` has about `0.694n` bits, so the `k`-th addition costs `Θ(k)` and the
total is `Θ(n²)`. If a problem wants `F_{10⁶}` exactly, the bignum arithmetic —
not the loop — is the algorithm you must think about.

**Space** in the fixed-width model is a word per value; in the limb model it is
`b/8` bytes plus a per-object header of a couple of dozen bytes in CPython.

**The cost people forget** is the silent conversion. `a / b` on two `int`s in
Python 3 produces a `float` — an unconditional truncation to 53 bits of mantissa,
regardless of how careful everything upstream was. So does `math.sqrt`, so does
`x ** 0.5`, so does `sum()` the moment one float enters the list, and so does
handing an `int` to anything that formats it as a decimal number. Each of those
is `O(1)` and each of them can cost you the answer.

## The implementation

There is no single algorithm to implement, so what follows is the toolkit: a
simulator for the wheel (so you can *see* the wrap you are reasoning about), the
invariant from the proof asserted at every step, and the one predicate worth
memorising — an overflow test that runs *before* the multiplication.

```python run
def wrap(x, bits):
    """What an n-bit two's-complement register holds after you store x in it."""
    m = 1 << bits
    x &= m - 1                               # the hardware keeps only x mod 2^bits
    return x - m if x >= (m >> 1) else x     # the top half is read back as negative


true = stored = 0
max_true = max_stored = 0
print("  add     true    int8   equal")
for v in (50, 60, 40, -70):
    true += v
    stored = wrap(stored + v, 8)
    max_true = max(max_true, true)
    max_stored = max(max_stored, stored)
    assert (true - stored) % 256 == 0        # the invariant: congruent mod 2^8
    print("%+5d %8d %7d   %s" % (v, true, stored, true == stored))

assert true == stored == 80
assert (max_true, max_stored) == (150, 110)
print("sum of all four : true %d, int8 %d  -> equal, the wrap cancelled" % (true, stored))
print("max prefix sum  : true %d, int8 %d  -> NOT equal, the compare did not" %
      (max_true, max_stored))
print()

LIMIT = (1 << 63) - 1


def mul_overflows(a, b, limit=LIMIT):
    """For a, b >= 0: is a*b > limit?  Decided without ever forming a*b."""
    return b != 0 and a > limit // b


for a in range(40):                          # exhaustive check against the truth
    for b in range(40):
        assert mul_overflows(a, b, 255) == (a * b > 255), (a, b)
print("mul_overflows matches reality on all 1600 pairs below 40, limit 255")
print("10^9  * 10^9 exceeds int64?", mul_overflows(10**9, 10**9))
print("10^10 * 10^9 exceeds int64?", mul_overflows(10**10, 10**9))
assert not mul_overflows(10**9, 10**9) and mul_overflows(10**10, 10**9)
```

Three lines are doing the work.

`x &= m - 1` is the whole of fixed-width arithmetic: keep the low `n` bits, which
is reduction modulo 2ⁿ. Everything else in `wrap` is the *reading* convention,
not the arithmetic.

`assert (true - stored) % 256 == 0` is the proof's invariant, checked at runtime.
It must hold after every `+`, `−` or `×`, and it is the first thing to break when
you accidentally use `//`.

`return b != 0 and a > limit // b` is the overflow test that actually works. It
is correct because for integers `a, b > 0`, `a·b ≤ limit` holds exactly when
`a ≤ limit/b`, and since `a` is an integer that is exactly `a ≤ ⌊limit/b⌋`.
Everything on the right-hand side is computed with one division on values already
known to be in range, so the test itself can never overflow. Contrast with the
tempting `if a * b > limit` — which has already overflowed by the time it is
evaluated — or the after-the-fact `if product < 0`, which the traps section shows
missing a genuine overflow outright.

## Variants you will meet

**Deliberate wrapping.** Hashing wants the wheel. A polynomial rolling hash
multiplies and adds without bound and reduces to a fixed width on purpose —
[[rolling-hash]] and [[hash-functions]]. In Python you must add the mask
yourself, the one place where an unbounded `int` is a bug rather than a
convenience.

**Modulo the problem asks for.** "Return the answer modulo 10⁹ + 7" moves you into
[[modular-arithmetic]]. The base fact from this chapter: `10⁹ + 7` squared is
about `10¹⁸`, which is why that modulus is chosen — a product of two reduced
residues still fits in a signed 64-bit integer. A modulus near `4·10⁹` would not.

**Wider intermediates.** C++ has `__int128`, Java has `BigInteger`, Python has
nothing to do. The pattern to recognise is "multiply, then divide": *Allocate
Workers for a Production Ratio* wants
`total * firstRatio / (firstRatio + secondRatio)`, where the product overflows 32
bits but the quotient does not. Widen for the middle, narrow at the end.

**Exact comparison instead of division.** To decide `a₁/b₁ > a₂/b₂` with positive
denominators, compare `a₁·b₂` against `a₂·b₁`. No division, no float, exact.
*Best Average Student Score* is this instruction made explicit, and
*Sliding-Window Averages as Reduced Fractions* takes it further by asking for the
reduced fraction itself, which is a `gcd` away.

**Fixed point instead of floating point.** Money is counted in integer cents.
*Basic Item Discounts* states prices in cents and specifies the rounding rule for
the one place a division is unavoidable; *Financial Account Ledger* keeps exact
integer balances for the same reason. The move: multiply the unit away until
everything is an integer.

**Ceiling division without floats.** `⌈a/b⌉` is `-(-a // b)` in Python, or
`(a + b - 1) // b` for non-negative `a` — the latter can itself overflow in fixed
width when `a` is near the ceiling. *Cluster Size on Disk* has `fileSize ≤ 10¹⁸`
and asks for exactly this, and its bound is chosen so that a float round-trip is
visibly lossy.

**Big integers as strings.** When the value genuinely exceeds any machine type
and the language will not help, you implement schoolbook arithmetic over digit
arrays yourself. *Base36 Square Root* and *Reverse Base36 Number* live in this
territory; see [[base-conversion]] for the digit handling and
[[fast-exponentiation]] for making powers cheap.

**Sentinels that overflow.** A DP or shortest-path table seeded with a large
"infinity" constant will compute `INF + w` somewhere. In fixed width that wraps
to a small number and wins the `min`, so your unreachable node reports a negative
distance. *Shortest Distances From an Adjacency Matrix* and the Floyd–Warshall
relaxation in general ([[floyd-warshall]], [[dijkstra]]) need either a guard or a
sentinel small enough that `2·INF` still fits.

```python run
import math

def ceil_div(a, b):
    """Smallest integer >= a/b for b > 0.  No float ever appears."""
    return -(-a // b)


def better(t1, c1, t2, c2):
    """Is total1/count1 strictly greater than total2/count2?  Integers only."""
    return t1 * c2 > t2 * c1


x = 10**18 - 1
print("math.isqrt(10^18 - 1)      :", math.isqrt(x))
print("int(math.sqrt(10^18 - 1))  :", int(math.sqrt(x)), "<- one too many")
assert math.isqrt(x) == 999999999 and int(math.sqrt(x)) == 10**9

print("float cannot tell 10^18 from 10^18 + 1 :", float(10**18) == float(10**18 + 1))
assert float(10**18) == float(10**18 + 1)

a = (1, 3)                                    # student A: total 1 over 3 scores
b = (333333333333333333, 10**18)              # student B: a hair below 1/3
print("compared as floats         :", a[0] / a[1] == b[0] / b[1], "(they look equal)")
print("compared exactly           :", better(*a, *b), "(A really is larger)")
assert a[0] / a[1] == b[0] / b[1]
assert better(*a, *b) and not better(*b, *a)

n = ceil_div(10**18, 3)
print("ceil_div(10^18, 3)         :", n)
assert 3 * n >= 10**18 > 3 * (n - 1)
print("Python floors: -7 // 2 =", -7 // 2, "; C truncates toward zero: -7 / 2 = -3")
assert -7 // 2 == -4
```

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"fits in a signed 64-bit integer", "requires a 64-bit integer", "long" in the
   signature.** This is the giveaway, and it is everywhere in this bank —
   *Get Success Value* returns `long[q]`, *Count Power Products in Range* takes
   `long low`. The setter has done the bit count for you and is telling you the
   answer to it.
2. **An explicit instruction to avoid overflow or to avoid floating point.**
   *Count Power Products in Range* says "avoid overflow when generating powers";
   *Best Average Student Score* says "compare averages exactly". Both name the
   exact line where a naive solution fails.
3. **Two constraint bounds that multiply past a ceiling.** `n ≤ 10⁵` with
   `|v| ≤ 10⁹` and any kind of sum; `n ≤ 2·10⁵` on both sides and a *count of
   pairs*; a bound stated as `10¹⁸`, which is a deliberate flag that one more
   multiplication is fatal.
4. **A quantity that is a product of inputs, or a ratio of two sums.** Notional
   value (price × quantity), area, total cost, weighted average. *Top Ten Trades
   by Notional Value* and *Moving Cost by Volume and Category* are products of two
   input columns; the danger is the product, not the list.
5. **Exact counting over a large search space.** *Count Staircase Ways* caps `n`
   at 90 and *Climb Stairs with One, Two, or Three Steps* caps it at 50, which
   are not algorithmic limits — they are the largest `n` whose answer fits in 64
   bits. A suspiciously small, oddly specific bound on a counting problem is a
   range constraint wearing a disguise.
6. **Money, bytes, nanosecond timestamps, view counts.** Domains where the
   natural unit is small and the totals are not.

The anti-signals:

- **"modulo 10⁹ + 7"** means the setter has already removed the range problem;
  your job is [[modular-arithmetic]], and the only overflow question left is
  whether the product of two residues fits.
- **Decimals, tolerances, "within 10⁻⁶"** point at [[numerical-stability]]. Range
  is not the issue; representable precision is.
- **`n ≤ 1000` with values under 10⁴.** Do the multiplication: 10⁷ fits in 32
  bits with room. Not every problem with numbers in it is this topic, and padding
  every variable to the widest type is not a substitute for the bit count.

## Traps

**The multiplication happens before the assignment.** `long total = a * b;` with
`int a, b` computes `a * b` in 32-bit width and widens the already-wrapped
result. The cast belongs on an operand: `(long)a * b`. Symptom: correct on the
samples, wrong on the large test, and the printed value looks like a plausible
small number.

**Checking for overflow after the fact.** `if (a * b < 0)` catches only the wraps
that happen to land in the negative half — a coin flip — and in C or C++ it is
undefined behaviour the compiler may optimise away entirely. Check before, with a
division.

**`(lo + hi) / 2`.** The classic, and the reason [[binary-search]] insists on
`lo + (hi - lo) / 2`. Both indices are valid, their sum is not.

**`abs` of the most negative value.** There are 2ⁿ patterns and the signed range
is asymmetric: `−2ⁿ⁻¹` has no positive counterpart, so `abs(INT_MIN)` is
`INT_MIN`. Any "take the absolute difference" routine that negates rather than
subtracting carefully can hit it.

**Float sneaking into an integer computation.** `int(x ** 0.5)`, `math.sqrt`,
`sum(a) / len(a)` and sorting by a float key all truncate to 53 bits. Past
`2⁵³ ≈ 9·10¹⁵` a double cannot represent consecutive integers, so the error is an
integer off by one — the worst kind. Use `math.isqrt`, integer division and
cross-multiplication.

**Floor versus truncation.** Python's `//` floors toward −∞, C's `/` truncates
toward zero. `-7 // 2` is `-4` in Python and `-3` in C. Every ceiling-division
idiom you remember from another language is wrong here by one, on negatives.

**Growing an unbounded integer inside a hot loop.** In Python, forgetting the
`% MOD` in a rolling hash or a DP does not produce a wrong answer; it produces a
timeout, as the limbs pile up and every operation gets slower.

```python run
def wrap32(x):
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x >= (1 << 31) else x


MAX32 = (1 << 31) - 1
MIN32 = -(1 << 31)

lo, hi = 1_500_000_000, 2_000_000_000        # both are valid 32-bit indices
print("(lo + hi) // 2 in 32 bits   :", wrap32(wrap32(lo + hi) // 2), "<- a negative index")
print("lo + (hi - lo) // 2         :", wrap32(lo + wrap32(hi - lo) // 2), "<- correct")
assert wrap32(lo + hi) < 0
assert wrap32(lo + wrap32(hi - lo) // 2) == (lo + hi) // 2

print("abs(INT32_MIN) in 32 bits   :", wrap32(-MIN32), "<- still negative")
assert wrap32(-MIN32) == MIN32

a = b = 100_000                              # a genuine overflow that looks fine
prod = wrap32(a * b)
print("100000 * 100000 in 32 bits  :", prod, "(true value", a * b, ")")
print("  check after,  prod < 0    :", prod < 0, "<- misses it entirely")
print("  check before, a > MAX//b  :", a > MAX32 // b, "<- catches it")
assert prod > 0 and prod != a * b and a > MAX32 // b

big = 10**18 - 1                             # and the float back door
print("int(big ** 0.5) vs isqrt    :", int(big ** 0.5), "vs 999999999")
assert int(big ** 0.5) != 999999999
print("every one of these is silent at run time")
```

The third case is worth sitting with. `100000 * 100000` is `10¹⁰`, which wraps to
`1410065408` — positive, plausible, about a seventh of the truth. A sign check
sees nothing wrong. Only the division test, asked before the multiplication,
reports it.

## What to memorise

**The sentence** that turns a constraint line into an implementation decision:
*"What is the largest magnitude any intermediate takes, and does it fit?"* Do the
multiplication of bounds on paper before the first line of code, not after the
first wrong answer.

**The numbers**, which make that sentence answerable in your head:

| ceiling | value | reached by |
| --- | --- | --- |
| `2³¹ − 1` | ≈ 2.15 · 10⁹ | two values of 10⁹ added |
| `2⁵³` | ≈ 9.01 · 10¹⁵ | the last integer a double represents exactly |
| `2⁶³ − 1` | ≈ 9.22 · 10¹⁸ | two values of 10⁹ multiplied (10¹⁸ — just fits) |

Plus: 10⁵ terms of 10⁹ sum to 10¹⁴, safe; `(10⁹ + 7)²` is about 10¹⁸, safe;
three factors of 10⁹ is 10²⁷, hopeless.

**The three templates**, worth typing from muscle memory:

```python
if b and a > LIMIT // b: ...      # overflow test, before the multiply
q = -(-a // b)                    # ceiling division, no float
a1 * b2 > a2 * b1                 # compare a1/b1 against a2/b2, exactly
```

**The habit**: never divide when you can cross-multiply, and never call a
floating-point function on a value you intend to use as an exact integer. If a
`/`, a `sqrt` or a `**` appears in code whose answer is an integer, treat it as a
bug until you have proved the operands are under 2⁵³.

## Check yourself

:::check
An array of 32-bit values is summed in a 32-bit accumulator, and the true total
is 5. Several intermediate partial sums overflowed. Is the printed answer 5? Now
the same loop instead reports the largest partial sum it saw. Is *that* answer
right? Explain both from the same principle.
--
The total is 5, correct. The maximum is not.

Both follow from the invariant proved above: the register always holds a value
congruent to the truth modulo 2³². For the running total, every step is an
addition, so the congruence survives to the end; the final true value 5 is inside
the representable range, and the decode map is a bijection that is the identity
there, so the register must read exactly 5.

The maximum is a *comparison*, and comparison is not a ring operation — it does
not commute with reduction modulo 2³². Two values congruent modulo 2³² can sit on
opposite sides of the cut, so the register's idea of "larger" is unrelated to the
truth once anything has wrapped. The overflow is invisible in the sum and fatal
in the max, from the same theorem.
:::

:::check
Someone says: "I write Python, and Python integers are arbitrary precision, so
overflow is not something I have to think about." Where are they wrong?
--
They are right about one thing and wrong about three.

Right: `int` arithmetic in Python will not wrap. You will not produce the C bug.

Wrong, first, because `float` is still 64-bit. `a / b`, `x ** 0.5`, `math.sqrt`
and any comparison on a float key truncate to a 53-bit mantissa. Past
`2⁵³ ≈ 9·10¹⁵` a double cannot hold consecutive integers, so
`int(math.sqrt(10**18 - 1))` is off by one. The problems that say "compare
exactly, do not rely on floating point" are aimed precisely at this.

Wrong, second, because arbitrary precision is not free. A `d`-limb integer costs
`Θ(d)` to add and up to `Θ(d²)` to multiply, so forgetting a `% MOD` in a rolling
hash or a counting DP turns a linear loop quadratic. In Python the symptom of an
overflow bug is a timeout rather than a wrong answer.

Wrong, third, because plenty of problems ask you to *emulate* fixed width: hash
functions, checksums, base-36 arithmetic. There you write the mask yourself.
:::

:::check
You must decide which of two students has the higher mean score. Row counts are
up to 2·10⁵ and each score is a signed 32-bit integer. Show that comparing
`t1 * c2` against `t2 * c1` cannot overflow a signed 64-bit integer, and say why
that bound is the thing you should check rather than the code.
--
Do the bound and it fails. The two students share at most `2·10⁵` rows, so the
worst case is both counts near 10⁵. Then `|t1| ≤ 10⁵ · (2³¹ − 1) ≈ 2.15·10¹⁴` and
`c2 ≈ 10⁵`, giving `|t1 · c2| ≈ 2.15·10¹⁹` — past `2⁶³ − 1 ≈ 9.22·10¹⁸`. The
naive cross-multiplication does **not** fit in a signed 64-bit integer, and only
the arithmetic tells you so.

In a 64-bit language the repair is to reduce each fraction by its `gcd` first, or
to compare in 128-bit width. In Python the products are exact and cost a couple
of extra limbs.

That is the whole point of the exercise: the bound is a two-line calculation done
*before* choosing the technique, and here it rules the technique out. Writing the
code first and testing it on samples would never have raised the question.
:::

:::check
Why does `a > LIMIT // b` correctly decide whether `a * b` exceeds `LIMIT`, for
positive `a` and `b` — and why is it safe to evaluate?
--
For real numbers, `a·b > L` iff `a > L/b` (dividing by the positive `b` preserves
the inequality). Since `a` is an integer, `a > L/b` iff `a > ⌊L/b⌋`: the only
values of `a` between `⌊L/b⌋` and `L/b` are non-integers, so no integer is
misclassified at the boundary. And `⌊L/b⌋` is exactly what integer division
computes.

It is safe because every quantity evaluated is already in range. `L` is the type's
maximum, `b` is an input known to fit, and `L // b ≤ L`. Nothing in the test can
itself overflow — which is the property `if (a * b > L)` lacks, since it must
first compute the very value it is trying to avoid computing.
:::

:::check
A DP table is initialised to `INF = 2_000_000_000` and relaxed with
`dp[j] = min(dp[j], dp[i] + w)`. Weights are at most 10⁶ and the code runs in
32-bit width. What goes wrong, what is the symptom, and give two fixes.
--
`dp[i] + w` is computed even when `dp[i]` is the sentinel. `2·10⁹ + 10⁶` exceeds
`2³¹ − 1 ≈ 2.15·10⁹`, so it wraps to roughly `−2.15·10⁹`. That negative value
wins the `min`, and the sentinel — which was supposed to mean "unreachable" —
becomes the smallest cost in the table.

The symptom is distinctive: large negative distances appearing for exactly the
nodes that are unreachable, and, worse, those wrong values propagating into
reachable nodes through later relaxations, so the corruption spreads. It never
shows up on connected sample graphs.

Two fixes. Guard the relaxation — `if dp[i] < INF: …` — which is what
[[floyd-warshall]] needs, since it relaxes through every intermediate vertex. Or
pick a sentinel with headroom, so that `INF + w` still fits and the arithmetic
stays correct even when it is meaningless.
:::
