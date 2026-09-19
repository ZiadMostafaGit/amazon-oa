# Modular Arithmetic

> Modular arithmetic is not "take the remainder at the end". It is a smaller
> number system that addition, subtraction and multiplication respect exactly —
> which is why you are allowed to shrink every intermediate value, and why
> division is suddenly a research project.

## When you reach for it

There are two completely different reasons a statement says *modulo*, and
confusing them wastes a lot of time.

**Reason one: the answer is too big to write down, so the setter asks for a
fingerprint of it.** The tell is a sentence bolted onto the end of an otherwise
ordinary counting question — "Since the number of ways can be very large, return
the result modulo 10^9 + 7", which is how *Process Scheduling* phrases it. The
modulus has nothing to do with the problem; it is packaging. It tells you the
answer is a *count*, that the count is astronomical, and that you are not
expected to enumerate anything. *Drawing Edge* asks for the number of simple
undirected graphs on `n` labelled vertices with `n <= 10^9`; the answer is
`2^(n(n-1)/2)`, a number with roughly `10^17` digits. You will never hold it.
You will hold its residue.

**Reason two: the modulus is part of the physics of the problem.** A Caesar
cipher wraps within A–Z, so the alphabet *is* `Z/26` — *Caesar Cipher with a
Precomputed Alphabet* hands you a shift as large as `10^9` and tells you to
normalise it once modulo 26. A bus route is a circle, so stop indices live in
`Z/n` — *Shortest Distance on a Circular Bus Route* gives `distance[i]` as the
gap from stop `i` to stop `(i + 1) mod n`. A checksum is a byte, so it lives in
`Z/256`. Parity is `Z/2`. Here the modulus is the question, not the packaging.

A third use is rarer and more powerful: **the residue is the state**. *Count
Valid A-B-C Sequences Under a Modulo-Four Rule* builds a string of length
`n <= 10^18` where the running cost mod 4 decides which letters are legal. The
cost is unbounded; the cost mod 4 has four values. That collapse is what makes
the problem finite, and it is the same move as [[digit-dp]] or any
[[state-design|state-compression]] argument.

One hundred and six problems in this bank use the topic, #35 of 150. But it is
the wrong tool the moment the question asks you to *compare* things. Residues
have no order: `3` and `10^9 + 10` are the same element of `Z/(10^9+7)`, so
"which is larger" is meaningless. If a problem asks for a maximum, the maximum is
taken over honest integers and only the reported value is reduced. And if you
need the exact digits of a huge number — see [[big-integers]] — the modulus
throws away precisely what you want.

## The idea

Fix a modulus `m > 0`. Say `a ≡ b (mod m)` when `m` divides `a - b`. This
chops the integers into `m` buckets, called **residue classes**: everything that
leaves the same remainder when divided by `m` goes in one bucket.

The single fact that makes the whole subject work:

> The bucket of `a + b`, of `a - b` and of `a * b` depends only on the bucket of
> `a` and the bucket of `b`, not on which members of those buckets you picked.

That is a *ring homomorphism*, and you should picture it as a commuting square:
do the arithmetic then shrink, or shrink then do the arithmetic, and you land in
the same place.

<svg viewBox="0 0 580 250" role="img" aria-label="commuting square: reducing before multiplying gives the same residue as reducing after">
  <g>
    <rect x="20" y="25" width="200" height="50" rx="6"/>
    <text x="120" y="55" text-anchor="middle">a = 47,  b = 38</text>
    <rect x="350" y="25" width="200" height="50" rx="6"/>
    <text x="450" y="55" text-anchor="middle">a * b = 1786</text>
    <rect class="fill" x="20" y="175" width="200" height="50" rx="6"/>
    <text x="120" y="205" text-anchor="middle">5,  3</text>
    <rect class="fill" x="350" y="175" width="200" height="50" rx="6"/>
    <text x="450" y="205" text-anchor="middle">5 * 3 = 15 = 1</text>
    <line x1="228" y1="50" x2="342" y2="50"/>
    <line x1="342" y1="50" x2="330" y2="44"/>
    <line x1="342" y1="50" x2="330" y2="56"/>
    <text x="285" y="38" text-anchor="middle">multiply</text>
    <line x1="228" y1="200" x2="342" y2="200"/>
    <line x1="342" y1="200" x2="330" y2="194"/>
    <line x1="342" y1="200" x2="330" y2="206"/>
    <text x="285" y="190" text-anchor="middle">multiply</text>
    <line x1="120" y1="82" x2="120" y2="168"/>
    <line x1="120" y1="168" x2="114" y2="156"/>
    <line x1="120" y1="168" x2="126" y2="156"/>
    <text x="70" y="130" text-anchor="middle">mod 7</text>
    <line x1="450" y1="82" x2="450" y2="168"/>
    <line x1="450" y1="168" x2="444" y2="156"/>
    <line x1="450" y1="168" x2="456" y2="156"/>
    <text x="505" y="130" text-anchor="middle">mod 7</text>
    <text x="285" y="245" text-anchor="middle">both routes end at 1: the square commutes</text>
  </g>
</svg>

Both routes reach `1`: `1786 = 7 * 255 + 1`, and `5 * 3 = 15 = 7 * 2 + 1`. That
is a theorem, proved below, and it is the licence to write
`total = total * k % MOD` inside a loop instead of building a thousand-digit
integer and reducing it once at the end.

The second image worth carrying is the clock. `Z/m` is a ring of `m` positions;
adding `k` walks `k` steps clockwise and falls off nothing.

<svg viewBox="0 0 320 300" role="img" aria-label="a seven-position clock showing 5 plus 4 landing on 2">
  <g>
    <circle cx="160" cy="150" r="105" fill="none"/>
    <circle cx="160" cy="45" r="15"/>
    <text x="160" y="51" text-anchor="middle">0</text>
    <circle cx="242" cy="85" r="15"/>
    <text x="242" y="91" text-anchor="middle">1</text>
    <circle class="fill" cx="262" cy="173" r="15"/>
    <text x="262" y="179" text-anchor="middle">2</text>
    <circle cx="206" cy="245" r="15"/>
    <text x="206" y="251" text-anchor="middle">3</text>
    <circle cx="114" cy="245" r="15"/>
    <text x="114" y="251" text-anchor="middle">4</text>
    <circle class="fill" cx="58" cy="173" r="15"/>
    <text x="58" y="179" text-anchor="middle">5</text>
    <circle cx="78" cy="85" r="15"/>
    <text x="78" y="91" text-anchor="middle">6</text>
    <text x="160" y="150" text-anchor="middle">5 + 4 = 2</text>
    <text x="160" y="172" text-anchor="middle">(mod 7)</text>
    <text x="160" y="295" text-anchor="middle">no largest element, no order</text>
  </g>
</svg>

The clock also makes the limitation visible. There is no "biggest hour": asking
which of two positions is larger is asking which way round the dial you started
counting, and the ring does not remember.

And it shows where division goes wrong. Mod 6, multiplying by 2 sends
`0, 1, 2, 3, 4, 5` to `0, 2, 4, 0, 2, 4`: three positions are never hit and the
others are hit twice, so there is no way to undo it. Mod 7, multiplying by 2
sends `0..6` to `0, 2, 4, 6, 1, 3, 5` — every position exactly once, so the undo
exists and is itself a multiplication. That difference is the whole theory of the
**modular inverse**, and the condition separating the two cases is
`gcd(a, m) = 1`.

## Worked by hand

Two traces. The first shows why reducing early is safe; the second computes an
inverse, the one operation you cannot do by staring.

### Reduce early, reduce often

Compute `P = 3 * 5 * 9 * 11 * 14` modulo 7, two ways at once.

| step | factor | exact running product | exact mod 7 | reduced running product |
| --- | --- | --- | --- | --- |
| 0 | — | 1 | 1 | 1 |
| 1 | 3 | 3 | 3 | `1*3 % 7` = 3 |
| 2 | 5 | 15 | 1 | `3*5 % 7` = 1 |
| 3 | 9 | 135 | 2 | `1*9 % 7` = 2 |
| 4 | 11 | 1485 | 1 | `2*11 % 7` = 1 |
| 5 | 14 | 20790 | 0 | `1*14 % 7` = 0 |

Three things to take from those five rows.

**The last two columns agree on every line, not just the last.** That is the
commuting square applied once per step. The reduced column is not an
approximation of the exact one; it is the exact one seen through the mod-7 lens,
and the lens does not distort.

**The reduced column never exceeded `6 * 14 = 84`, while the exact column reached
20790 after five factors.** Push it to a hundred thousand factors and the exact
column has close to a million digits while the reduced column still fits in a
machine word. The bound is worth memorising: two operands in `[0, m)` have a
product of at most `(m-1)^2 < m^2`. Every "will this overflow?" question about
modular code reduces to "does `m^2` fit?".

**Row 5 landed on 0, which is not the same as "the product is zero".** 20790 is a
healthy number that happens to be a multiple of 7. A residue of 0 means
"divisible by the modulus", never "empty". Code that branches on `answer == 0` to
mean "no such thing exists" is broken — and only on inputs where the true count
is an exact multiple of the modulus.

### Finding an inverse: extended Euclid on 17 mod 43

We want `x` with `17x ≡ 1 (mod 43)`. Run the Euclidean algorithm on `(17, 43)`
while carrying, for each remainder `r`, a pair `(s, t)` with
`r = 17s + 43t`. Start with the two obvious rows: `17 = 17*1 + 43*0` and
`43 = 17*0 + 43*1`.

| row | `r` | `s` | `t` | check `17s + 43t` | quotient used |
| --- | --- | --- | --- | --- | --- |
| A | 17 | 1 | 0 | 17 | — |
| B | 43 | 0 | 1 | 43 | — |
| C = B − 2·A | 9 | −2 | 1 | −34 + 43 = 9 | `43 // 17 = 2` |
| D = A − 1·C | 8 | 3 | −1 | 51 − 43 = 8 | `17 // 9 = 1` |
| E = C − 1·D | 1 | −5 | 2 | −85 + 86 = 1 | `9 // 8 = 1` |
| F = D − 8·E | 0 | 43 | −17 | 0 | `8 // 1 = 8` |

Row E says `17 * (-5) + 43 * 2 = 1`. Reduce mod 43 and the `43 * 2` term
vanishes: `17 * (-5) ≡ 1 (mod 43)`, so `x = -5 mod 43 = 38`. Check by hand:
`17 * 38 = 646 = 43 * 15 + 1`. Correct.

What the trace shows that the code does not. First, the `t` column is dead
weight: it is never read, because every use of the identity is taken mod `m`,
which kills the `m * t` term. Real implementations drop it. Second, the algorithm
stops at remainder 1, and the *only* reason it reaches 1 is that
`gcd(17, 43) = 1`. Ask instead for the inverse of 6 mod 9 and the remainders run
`9, 6, 3, 0`, giving `6s + 9t = 3` — an identity that can never be scaled to 1,
because the left side is always a multiple of 3. The algorithm does not fail; it
politely returns the wrong `g`, and checking it is your job. Third, `s`
alternates in sign and grows, so the final `x % m` is not cosmetic.

## Why it is correct

Two theorems. The first licenses reducing at every step; the second says when
division exists.

:::proof Reducing early never changes the residue
**Setup.** Fix `m >= 1`. Write `a ≡ b` for `m | (a - b)`. Let an *expression* be
a finite binary tree whose leaves are integer literals and whose internal nodes
are `+`, `-` or `*`. Let `val(E)` be its ordinary integer value and `R(E)` the
value computed bottom-up, replacing every intermediate result by its canonical
representative in `{0, ..., m-1}`.

**Lemma (compatibility).** If `a ≡ a'` and `b ≡ b'`, then `a + b ≡ a' + b'`,
`a - b ≡ a' - b'` and `a*b ≡ a'*b'`.
*Proof.* Write `a = a' + sm`, `b = b' + tm`. Then
`a ± b = (a' ± b') + (s ± t)m`, and
`a*b = (a' + sm)(b' + tm) = a'b' + m(a't + b's + stm)`. Each differs from the
primed version by a multiple of `m`. ∎

**Claim.** For every expression `E`: `R(E) ≡ val(E) (mod m)` and
`0 <= R(E) < m`. **By induction on the height of `E`.**

*Base, height 0.* `E` is a literal `k`, so `R(E) = k mod m`, which lies in
`[0, m)` by definition and differs from `k` by `m * (k div m)`.

*Step.* Let `E = E₁ ⊕ E₂` with `⊕ ∈ {+, -, *}`, both subtrees of smaller height.
By the induction hypothesis `R(E₁) ≡ val(E₁)` and `R(E₂) ≡ val(E₂)`, both in
range. The lemma gives `R(E₁) ⊕ R(E₂) ≡ val(E₁) ⊕ val(E₂) = val(E)`. The final
reduction swaps that for another member of the same class inside `[0, m)`, and
congruence is transitive, so the claim holds for `E`.

**Termination.** The tree is finite: one operation and one reduction per internal
node, then stop.

**Conclusion.** Reducing after every operation yields the canonical
representative of the exact answer's class. A loop that only accumulates with
`+`, `-` and `*` is such a tree — a left-leaning spine, one internal node per
iteration — so this covers `for x in xs: total = total * x % m`. ∎
:::

:::proof `a` has a multiplicative inverse mod `m` exactly when `gcd(a, m) = 1`
**Loop invariant of extended Euclid.** The algorithm keeps pairs `(r, s)` with
the invariant `r ≡ a*s (mod m)`, starting from `(a mod m, 1)` and `(m, 0)`. The
step replaces `(r_prev, s_prev), (r, s)` by `(r, s), (r_prev - q*r, s_prev - q*s)`
with `q = r_prev // r`. The new first component satisfies
`r_prev - q*r ≡ a*s_prev - q*(a*s) = a*(s_prev - q*s)`, so the invariant is
preserved; it holds initially because `a ≡ a*1` and `m ≡ 0 ≡ a*0`. The `r` values
are the remainder sequence of the ordinary Euclidean algorithm — strictly
decreasing and non-negative, hence terminating — whose last nonzero value is
`g = gcd(a, m)`. There the invariant reads `g ≡ a*s (mod m)`.

**(⇐)** If `g = 1`, the invariant gives `a*s ≡ 1 (mod m)`, so `s mod m` is an
inverse.

**(⇒)** If `a*x ≡ 1 (mod m)` then `a*x - 1 = k*m`, so any common divisor `d` of
`a` and `m` divides `a*x - k*m = 1`, forcing `d = 1`.

**Uniqueness.** If `a*x ≡ 1` and `a*y ≡ 1` then
`x ≡ x*(a*y) = (x*a)*y ≡ y (mod m)`.

**Fermat's little theorem.** Let `p` be prime and `p ∤ a`. Consider
`f(x) = a*x mod p` on `S = {1, ..., p-1}`. It lands in `S`: `a*x ≡ 0` would give
`p | a*x`, and `p` prime forces `p | a` or `p | x`, both excluded. It is
injective: `a*x ≡ a*y` gives `p | a*(x - y)`, and `p ∤ a` forces `p | (x - y)`,
so `x = y` in `[1, p-1]`. An injective map from a finite set to itself is a
bijection, so `f` permutes `S`. Multiply everything:

    ∏_{x∈S} (a*x) ≡ ∏_{x∈S} x   (mod p)
    a^(p-1) * (p-1)! ≡ (p-1)!   (mod p)

Every factor of `(p-1)!` is coprime to `p`, so `(p-1)!` is too, and by the first
part it is invertible; cancelling it leaves `a^(p-1) ≡ 1 (mod p)`. Hence
`a * a^(p-2) ≡ 1`, and `a^(p-2) mod p` is the inverse. ∎
:::

Now the assumptions, because that list is where the bugs live.

- **`m` is fixed and positive throughout.** Every step used the same `m`. Mixing
  two moduli in one expression — a hash mod `2^64` fed into a count mod
  `10^9+7` — is meaningless, and nothing will warn you.
- **Only `+`, `-` and `*`.** The lemma covers exactly those three. It is false
  for `//`, for comparison, for `max`, for `abs`, and for "is this zero".
- **The representative is the canonical one in `[0, m)`.** Python's `%` gives
  that even for negative left operands: `-7 % 26 == 19`, exactly what a Caesar
  decryption wants. C, C++, Java, Go and Rust return `-7`, and half the modular
  bugs in those languages are this line.
- **Exponents are not residues.** `a^e` means `e` multiplications; `e` lives in
  the exponent world, where the modulus is `p - 1` (Fermat), not `p`.
- **Fermat needs `p` prime *and* `p ∤ a`.** For `a ≡ 0` there is no inverse and
  `pow(0, p-2, p) = 0`, a silently wrong answer.
- **Cancellation needs primality.** In `Z/6`, `2*3 ≡ 0` with neither factor zero.
  You may not cancel a common factor from a congruence unless it is invertible.

## What it costs

**One operation.** Values stay in `[0, m)`, so an addition produces a value in
`[0, 2m)` and a multiplication a value in `[0, (m-1)^2]`. Each is one machine
operation plus one reduction. That gives the sizing rule: you need `m^2` to fit
in your word. With `m = 10^9 + 7`, `m^2 ≈ 1.000000014 * 10^18`, comfortably below
`2^63 - 1 ≈ 9.22 * 10^18`. That is *why* the constant is about `10^9` and not
about `10^18`.

It also gives a cheap trick: after an addition the value is below `2m`, so the
reduction is a conditional subtract, `if x >= m: x -= m`, rather than a division
— and division is the slowest integer instruction on any CPU. After a
multiplication you must divide.

**A sequence of `n` operations, reduced early**, costs `Θ(n)` word operations and
`O(1)` space beyond the accumulator.

**The same sequence, reduced at the end**, is where the derivation pays. After
`k` multiplications by numbers of size about `m`, the accumulator has about
`k * log m` digits, and schoolbook multiplication of a `d`-digit number by a
fixed-size one costs `Θ(d)`. The total is
`Θ(Σ_{k=1..n} k log m) = Θ(n² log m)` digit operations against `Θ(n)` for the
reduced version. In Python that turns a linear loop quadratic; in a fixed-width
language it never gets that far, because the value silently wraps.

**Extended Euclid** runs in `O(log m)` iterations. The argument: after two steps
the remainder at least halves. Let `r₀ > r₁ > r₂` be consecutive remainders with
`r₂ = r₀ mod r₁`. If `r₁ <= r₀/2` then `r₂ < r₁ <= r₀/2`. If `r₁ > r₀/2` then
`r₀ // r₁ = 1`, so `r₂ = r₀ - r₁ < r₀/2`. Either way `r₂ < r₀/2`: the remainder
halves every two steps and the loop runs at most `2 log₂ m` times. (Lamé's
sharper `log_φ m ≈ 1.44 log₂ m` is attained on consecutive Fibonacci numbers.)

**Fermat's inverse** is `pow(a, p-2, p)`: `O(log p)` modular multiplications by
[[fast-exponentiation]] — at most `2 * 30 = 60` for `p = 10^9 + 7`. Same order as
Euclid, more multiplications but no divisions, one line instead of ten. Fermat
when the modulus is a known prime; Euclid when it is not.

**Binomials mod `p`.** Precompute `fact[0..N]` in `N` multiplications. For the
inverse factorials, do *not* run `N` exponentiations (`O(N log p)`); compute
`invfact[N]` once and walk backwards with `invfact[i-1] = invfact[i] * i`, which
is correct because `1/(i-1)! = i/i!`. That is `O(N)` precompute, `O(log p)` once,
`O(1)` per query, `O(N)` space. The same prefix-product trick inverts any `n`
values for the price of one inversion and `3n` multiplications.

**The cost people forget** is the `%` in the innermost loop of a
[[counting-dp]]. A DP with `10^6` states and 10 transitions each performs `10^7`
divisions, often the dominant term. The fix is to accumulate a whole transition
in a wide temporary and reduce once per state — legal precisely because
`10 * (10^9 + 6)` is far below `2^63`. That inequality, written out, is the crisp
answer to "how many `%` may I skip"; everything else is superstition.

## The implementation

```python run
from math import comb

MOD = 10**9 + 7


def egcd(a, b):
    """Return (g, x, y) with a*x + b*y == g == gcd(a, b)."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def inv_euclid(a, m):
    """Inverse of a mod m for any m, provided gcd(a, m) == 1."""
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("no inverse: gcd(%d, %d) = %d" % (a, m, g))
    return x % m


def inv_fermat(a, p):
    """Inverse of a mod p, for PRIME p and a not divisible by p."""
    return pow(a % p, p - 2, p)


for a in range(1, 40):
    assert inv_euclid(a, MOD) == inv_fermat(a, MOD)
    assert a * inv_euclid(a, MOD) % MOD == 1
print("Euclid and Fermat agree on a = 1..39, and a * inv(a) == 1 every time")
print("inv(3)  =", inv_fermat(3, MOD), "-> 3 * inv(3) % MOD =", 3 * inv_fermat(3, MOD) % MOD)

N = 2000
fact = [1] * (N + 1)
for i in range(1, N + 1):
    fact[i] = fact[i - 1] * i % MOD
invfact = [1] * (N + 1)
invfact[N] = inv_fermat(fact[N], MOD)
for i in range(N, 0, -1):                       # 1/(i-1)! = i * 1/i!
    invfact[i - 1] = invfact[i] * i % MOD


def nCr(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD


for n, r in [(0, 0), (5, 2), (10, 3), (52, 5), (1999, 7), (2000, 1000)]:
    assert nCr(n, r) == comb(n, r) % MOD, (n, r)
print("nCr matches math.comb mod p for every pair tested, up to C(2000,1000)")
print("C(2000,1000) mod p =", nCr(2000, 1000))

# Drawing Edge: 2^(n(n-1)/2) graphs on n labelled vertices, n up to 10^9
print("drawing_edge(4)     =", pow(2, 4 * 3 // 2, MOD), "(2^6 = 64)")
assert pow(2, 4 * 3 // 2, MOD) == 64
print("drawing_edge(10**9) =", pow(2, 10**9 * (10**9 - 1) // 2, MOD))
```

Three lines carry the weight.

`old_r, r = r, old_r - q * r`, with the two coefficient rows beside it, is the
whole extended Euclid: one Euclidean step applied simultaneously to the remainder
and to its Bézout coefficients — the loop invariant of the second proof,
transcribed. The `t` row exists only so the returned triple can be
sanity-checked; drop it in a contest.

`invfact[i - 1] = invfact[i] * i % MOD` turns `O(N log p)` into `O(N)`. It looks
backwards and it is: invert the *largest* factorial once, then multiply your way
down. Everyone's first version calls `pow` inside the loop, which on `N = 10^6`
is thirty million modular multiplications instead of one million.

`pow(2, 10**9 * (10**9 - 1) // 2, MOD)` shows that Python's three-argument `pow`
is the whole of [[fast-exponentiation]]: an exponent near `5 * 10^17` costs about
sixty modular multiplications. In C++ that exponent overflows a 32-bit int, which
is the actual difficulty of *Drawing Edge*.

### The variant worth having ready: a linear congruence

*Smallest Value for a Linear Expression Modulo* gives an expression that
distributes to `A*x + B` and asks for the smallest non-negative `x` with
`A*x + B ≡ p (mod m)`, where `m <= 10^6` is **not** promised to be prime. Fermat
is unavailable. This is the general solver.

```python run
def egcd(a, b):
    old_r, r, old_s, s = a, b, 1, 0
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_r, old_s


def solve_linear(a, b, m):
    """Smallest x >= 0 with a*x == b (mod m), or None if there is none."""
    a %= m
    b %= m
    g, s = egcd(a, m)                 # g = gcd(a, m) = a*s + m*t
    if b % g:
        return None                   # a*x is always a multiple of g
    period = m // g                   # solutions are one class mod m//g
    return (s % period) * (b // g) % period


def brute(a, b, m):
    for x in range(m):
        if a * x % m == b % m:
            return x
    return None


print("solve 6x == 9 (mod 15) ->", solve_linear(6, 9, 15), " brute:", brute(6, 9, 15))
print("solve 6x == 7 (mod 15) ->", solve_linear(6, 7, 15), " brute:", brute(6, 7, 15))
print("solve 17x == 1 (mod 43)->", solve_linear(17, 1, 43), " brute:", brute(17, 1, 43))

for m in range(1, 41):
    for a in range(0, m + 3):
        for b in range(0, m + 3):
            got, want = solve_linear(a, b, m), brute(a, b, m)
            assert got == want, (a, b, m, got, want)
print("exhaustive check: every (a, b) for every modulus 1..40 matches brute force")
```

The `b % g` test is the entire difference between this and an inverse. `a*x mod m`
can only land on multiples of `g = gcd(a, m)`, so a target that is not a multiple
of `g` is unreachable — exactly the mod-6 clock from *The idea*, where doubling
never reaches an odd position. When it is reachable there are `g` solutions
spread evenly around the dial, and the smallest is the representative mod `m/g`,
which is why the final `%` uses `period` and not `m`.

## Variants you will meet

**Modular inverse by Fermat.** `pow(a, p - 2, p)`, prime `p` only. One line, and
the reason `10^9 + 7` is chosen prime rather than round.

**Modular inverse by extended Euclid.** Any modulus, needs `gcd(a, m) = 1`. In
Python 3.8+ this is `pow(a, -1, m)`, which raises `ValueError` when no inverse
exists — a feature, since the alternative is a silent wrong answer.

**Euler's theorem.** `a^φ(m) ≡ 1 (mod m)` whenever `gcd(a, m) = 1`, with `φ(m)`
the count of integers below `m` coprime to it. Fermat is the case `m = p`,
`φ(p) = p - 1`. This is how exponent towers reduce for composite moduli. See
[[number-theory]] and [[primes]].

**Chinese Remainder Theorem.** Residues modulo pairwise-coprime `m₁, m₂, ...`
determine the residue modulo their product, constructively — used to split a
composite modulus into prime powers, and to recover an exact integer from several
fingerprints.

**Fast exponentiation, and matrix exponentiation.** `a^e mod m` in `O(log e)`
([[fast-exponentiation]]). For a linear recurrence the same trick applies to a
transfer matrix: *Count Valid A-B-C Sequences Under a Modulo-Four Rule* has four
states (the cost mod 4) and `n <= 10^18`, so the only reachable solution is a
`4 x 4` matrix raised to the `n`-th power. See [[matrix-exponentiation]].

**Counting DP with a modulus.** The bulk of the 106 problems here — *Domino and
Tromino Tiling*, *Knight Dialer Sequences*, *Coloring Houses* — are a
[[counting-dp]] where every `+=` is followed by `% MOD`. The modulus adds nothing
to the thinking; it just tells you the recurrence is the whole answer. When the
question is "how many ways sum to something divisible by `k`", the running sum
mod `k` becomes a DP dimension of size `k` rather than of size `sum`.

**Wrap-around indexing.** `(i + 1) % n` to walk a ring, `(c - 'a' + shift) % 26`
for a cipher. *Shortest Distance on a Circular Bus Route* and *Batch Caesar
Cipher* are pure instances. Parity is the degenerate case, `Z/2`, where
everything collapses to [[bit-manipulation]] or [[xor-tricks]]: `a % 2` is
`a & 1` and addition mod 2 is `^`. *Plus Mult Array* is a mod-2 problem wearing a
long statement.

**Modular hashing.** A rolling hash is a polynomial evaluated mod a large prime;
*URL Hashing* maps each block's character sum mod `m` to an index. Collisions are
the price and two moduli at once are the defence. A checksum mod 256 — *Chunked
Byte Stream Checksums* — is the same idea with a power-of-two modulus, where
reduction is a mask. See [[rolling-hash]], [[hash-functions]],
[[base-conversion]].

## Recognising it in a statement

In descending order of reliability.

1. **"modulo 10^9 + 7", "modulo 998244353", "since the answer may be large".**
   Near-certain. It also tells you three things for free: the answer is a
   *count*; the intended solution is a formula or a DP, never an enumeration; and
   whatever you compute must never be compared, only combined.
2. **A "count the ways" question with `n <= 10^9` or `n <= 10^18`.** The loop
   over `n` is not allowed either: look for a closed form with
   [[fast-exponentiation]] (*Drawing Edge*) or a linear recurrence with
   [[matrix-exponentiation]] (*Count Valid A-B-C Sequences Under a Modulo-Four
   Rule*).
3. **Explicit wrap-around language** — "arranged in a circle", "wraps within A
   through Z", "the distance from stop `i` to stop `(i + 1) mod n`", "unsigned
   byte". The modulus is physical and small: 26, 60, 256, `n`.
4. **"divisible by `k`", "congruent to `r` modulo `k`", "leaves remainder".**
   Residue as state. Expect a DP dimension of size `k`.
5. **A closed form containing a division** — `n(n-1)/2`, a binomial, an average —
   returned modulo a prime. You need an inverse, in `Z/p`, not `//`.
6. **A modulus given as input and not promised prime**, as in *Smallest Value for
   a Linear Expression Modulo* with `1 <= m <= 10^6`. That omission *is* the
   problem: Fermat is off the table, `gcd` handling is on.

The anti-signals:

- **The question asks for a maximum, a minimum or a sort of the quantities being
  reduced.** "Return the maximum, modulo `10^9+7`" means the maximum is taken
  over exact values and only the winner is reduced. A `max` over residues is a
  bug with no symptom on small tests.
- **"Modulo" used only to test divisibility**, as in *Encryption Validity*, where
  `element modulo divisor == 0` counts divisors. That is arithmetic, not a
  residue system; nothing here applies.
- **The exact digits are wanted** — "how many digits", "the leading three
  digits". Reducing destroys exactly that. See [[big-integers]].

## Traps

**Reducing something you are about to compare.** Correct on small inputs, wrong
once any intermediate exceeds the modulus — so, at `10^9 + 7`, wrong only on the
largest test.

**Using `//` for division.** `(a // b) % m` is not `a * inv(b) % m`, and the two
agree by accident whenever `b` divides `a` exactly, so the samples pass.

**Reducing an exponent by `p` instead of `p - 1`.** A type error the language
cannot catch.

**Applying Fermat to a composite modulus, or to `a ≡ 0`.** `pow(a, m-2, m)`
returns a number, and it is almost never an inverse.

**Forgetting that Python's `%` is non-negative and C's is not**, or the reverse:
`((x % m) + m) % m` is harmless noise in Python, and omitting it in C++ produces
negative array indices.

**Reducing too late.** A quadratic slowdown in Python; silent overflow in a
fixed-width language.

**Treating a zero residue as an empty answer.**

```python run
MOD = 10**9 + 7

# 1. mod does not commute with max / comparison
a, b = MOD + 1, 7
print("max(a, b) % MOD          =", max(a, b) % MOD, "(reduce the winner: correct)")
print("max(a % MOD, b % MOD)    =", max(a % MOD, b % MOD), "<- picked the wrong number")
assert max(a % MOD, b % MOD) != max(a, b) % MOD

# 2. floor division is not modular division
num, den = 10, 4
wrong = (num // den) % MOD
right = num * pow(den, MOD - 2, MOD) % MOD
print("(10 // 4) % MOD          =", wrong, "<- meaningless")
print("10 * inv(4) % MOD        =", right, " check: right * 4 % MOD =", right * den % MOD)
assert right * den % MOD == num % MOD and wrong != right

# 3. exponents reduce mod p-1, not mod p
e = 10**18
print("pow(2, e, MOD)           =", pow(2, e, MOD), "(reference)")
print("pow(2, e % MOD, MOD)     =", pow(2, e % MOD, MOD), "<- wrong modulus for the exponent")
print("pow(2, e % (MOD-1), MOD) =", pow(2, e % (MOD - 1), MOD), "<- Fermat, correct")
assert pow(2, e % (MOD - 1), MOD) == pow(2, e, MOD)
assert pow(2, e % MOD, MOD) != pow(2, e, MOD)

# 4. residue 0 does not mean "no such object"
true_count = 3 * MOD
print("true count", true_count, "reports as", true_count % MOD, "- same as a genuinely empty answer")
assert true_count % MOD == 0 and true_count != 0

# 5. Fermat on a composite modulus returns a plausible-looking lie
m, a2 = 15, 2
fake = pow(a2, m - 2, m)
real = pow(a2, -1, m)
print("pow(2, 13, 15) =", fake, "but 2 *", fake, "% 15 =", a2 * fake % m, "!= 1")
print("the real inverse is", real, "since 2 *", real, "% 15 =", a2 * real % m)
assert a2 * fake % m != 1 and a2 * real % m == 1
print("five ways to be wrong, all of them silent")
```

Each of the five is silent: no exception, no warning, a plausible number. Number
3 bites hardest, because the code *looks* careful — it reduces everything in
sight, including the one quantity that must not be reduced that way.

## What to memorise

**The kit**, which should come out of your fingers without thought:

```python
MOD = 10**9 + 7

total = (total + x) % MOD          # or: total += x;  if total >= MOD: total -= MOD
total = total * x % MOD
diff  = (a - b) % MOD              # already non-negative in Python
p     = pow(a, e, MOD)             # fast exponentiation, O(log e)
i     = pow(a, MOD - 2, MOD)       # inverse, prime modulus only
j     = pow(a, -1, m)              # inverse, any modulus, raises if gcd != 1
```

**The sentence** that decides everything: *"Congruence survives `+`, `-` and
`*`. It does not survive `//`, `/`, `<`, `max`, `abs` or `== 0`. Anything in the
first list I may reduce whenever I like; anything in the second must happen
before the reduction, or not at all."*

**The habit**: reduce at the point of *assignment*, never at the point of return.
Every line that writes to an accumulator ends in `% MOD`. Then there is no such
thing as "a value I forgot to reduce", and the overflow question never arises.

Numbers worth carrying:

- `10^9 + 7` is prime, and `(10^9 + 7)^2 ≈ 10^18` fits in a signed 64-bit word
  (limit `≈ 9.22 * 10^18`). That is the entire reason for its size.
- `998244353` is the other common one: prime, and `119 * 2^23 + 1`, which makes
  it friendly to number-theoretic transforms.
- `φ(p) = p - 1`, so exponents reduce mod `p - 1`.
- `log₂(10^9) ≈ 30`, so `pow(a, e, 10^9+7)` is about sixty multiplications.
- The physical moduli: 2 (parity), 26 (letters), 60 (minutes), 256 (a byte),
  `n` (a ring).

## Check yourself

:::check
Why may you reduce modulo `m` after every multiplication, but not after a
floor division — and what exactly breaks?
--
Because the compatibility lemma is proved for `+`, `-` and `*` only, and it is
*false* for `//`. The lemma says the result's class depends only on the inputs'
classes; for `//` it depends on more.

Counterexample mod 7: `14 ≡ 0` and `21 ≡ 0`, the same class, yet `14 // 2 = 7 ≡ 0`
while `21 // 2 = 10 ≡ 3`. Same input classes, different output classes, so there
is no well-defined operation to reduce with. Modular division is a different
operation — multiplication by the inverse — and it exists only when
`gcd(divisor, m) = 1`.
:::

:::check
Someone says: "`10^9 + 7` is used because it is the largest prime that fits in a
32-bit integer." Where are they wrong, and what is the real reason?
--
Wrong on the fact and wrong on the reason.

On the fact: the largest prime below `2^31` is `2^31 - 1 = 2147483647`, itself
prime (a Mersenne prime), which is more than twice as large. So `10^9 + 7` is not
the largest anything.

On the reason: the constraint is not that `m` fits in a word, it is that `m^2`
fits, because the natural intermediate of a modular multiply is a product of two
values below `m`. `(10^9 + 7)^2 ≈ 10^18` sits safely under the signed 64-bit
limit `≈ 9.22 * 10^18`; `(2^31 - 1)^2 ≈ 4.6 * 10^18` would also fit, but with far
less headroom for the `a*b + c` patterns of DP inner loops. Primality is the
second requirement, and it is what buys Fermat and therefore an inverse for every
nonzero residue.
:::

:::check
*Drawing Edge* wants `2^(n(n-1)/2) mod (10^9 + 7)` with `n` up to `10^9`. A
candidate writes `pow(2, (n * (n-1) // 2) % (10**9 + 7), 10**9 + 7)`. Are they
right, and if not, what is the correct reduction?
--
They are wrong. The exponent counts multiplications; by Fermat,
`2^(p-1) ≡ 1 (mod p)` since `p` is prime and `p ∤ 2`, so exponents reduce modulo
`p - 1`, not `p`. The correct line is `pow(2, E % (MOD - 1), MOD)` with
`E = n*(n-1)//2`.

In Python even that is unnecessary: `E` is at most about `5 * 10^17`, and
`pow(2, E, MOD)` costs about sixty multiplications regardless. The reduction
matters only in a fixed-width language — where `n * (n - 1)` overflows 32 bits
long before `n` reaches `10^9`, and that overflow, not the modular arithmetic, is
the real trap here.
:::

:::check
Given `gcd(a, m) = g > 1`, when does `a*x ≡ b (mod m)` have a solution, how many
are there modulo `m`, and which one do you return?
--
A solution exists **iff `g | b`**. Forwards: `b = a*x - k*m` and `g` divides both
terms on the right. Backwards: Bézout gives `s, t` with `a*s + m*t = g`, and
scaling by `b/g` gives `a*(s*b/g) ≡ b (mod m)`.

There are then exactly `g` solutions modulo `m`. If `x₀` is one, `a*(x₀ + d) ≡ b`
iff `m | a*d` iff `(m/g) | d`, so the solution set is
`x₀, x₀ + m/g, ..., x₀ + (g-1)m/g` and the smallest non-negative one is
`x₀ mod (m/g)`.

That is the shape of *Smallest Value for a Linear Expression Modulo*: after
distributing, the expression is `A*x + B`, so you solve `A*x ≡ (p - B) (mod m)`
and return the smallest root. Since `m` there is only `1 <= m <= 10^6` and never
promised prime, the `gcd` case analysis is not optional.
:::

:::check
You solve a counting problem, print the answer mod `10^9 + 7`, and get 0. A
teammate concludes the configuration is impossible. Why is that reasoning
unsound, and is there any way to test emptiness from residues?
--
Because 0 is the residue of every multiple of the modulus, not just of zero. A
true count of `10^9 + 7`, or any other multiple, reports as 0. The map from
counts to residues is massively many-to-one and deliberately keeps only a
fingerprint.

No number of extra moduli makes it certain either: `k` coprime moduli pin the
count down only modulo their product (Chinese Remainder Theorem), which still
cannot distinguish 0 from that product. If the problem genuinely needs "does one
exist", that is a separate reachability or feasibility check, run without any
modulus. The lesson generalises: never branch on a reduced value. Branch on the
structure; reduce only the number you report.
:::

