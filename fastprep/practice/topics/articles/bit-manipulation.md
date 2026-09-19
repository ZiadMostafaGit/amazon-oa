# Bit Manipulation

> Bit manipulation is not a bag of tricks to memorise. It is a single decision:
> to stop reading an integer as a magnitude and start reading it as a column of
> booleans that the machine updates all at once.

## When you reach for it

Ninety-seven problems in this bank use it, which puts it at #36 of 150. They are
not ninety-seven different ideas. They are six.

- **The number is a set.** A value's bits are membership flags over a small
  universe. *Count String Pairs With Disjoint Characters* turns each word into a
  26-bit mask and asks whether `ma & mb == 0`; *Maximum Unique-Character Word
  Subset* does the same and then searches over combinations of those masks.
- **The number is a multiset of coins.** *Minimum Tokens Remaining* exchanges two
  tokens on stack `i` for one on stack `i + 1`. Since `2 · 2ⁱ = 2ⁱ⁺¹`, the total
  `Σ A[i] · 2ⁱ` never changes, and the fewest tokens that can represent a value
  as a sum of powers of two is its popcount. The whole problem is one identity.
- **The columns are independent, so count them separately.** *Sum of XOR Across
  Cartesian Pairs* has 4 · 10⁸ pairs and thirty columns; *Single Number with
  Triplicates* counts each column modulo 3. Section *What it costs* derives the
  first one.
- **Cancellation.** XOR is its own inverse, so duplicates vanish: *Find the
  Missing Number from 1 to n*, *Missing and Repeated Number*, *Count Subarrays
  With Given XOR*. This family is large enough to have its own chapter,
  [[xor-tricks]].
- **The word has a fixed width and you must respect it.** *Swap Even and Odd
  Bits*, *Swap Adjacent Nibbles*, *Check Endianness Of A Byte Array*, *CIDR IPv4
  Range Iterator*. Here the bits are the specification, not a trick.
- **Greedy from the most significant bit.** *Find Y Value* spends its `maxSet`
  ones on the highest columns where `x` has zeros; *Get Max Or Sum* caps `k` at
  11 doublings, which is a loud hint that you try each element as the one that
  receives them.

The trigger, said once: **the problem cares about the bits, or the constraints
are small enough that a subset can be a number.** `n <= 20` next to "choose any
subset" means 2²⁰ ≈ 10⁶ masks and is practically an instruction. `values[i] <
1024` in *Maximum Profit Under a Bitwise OR Limit* means there are only 1024
reachable OR values, so the OR itself is the state.

It is the wrong tool when the numbers are only numbers. Sorting, sums,
comparisons and averages care about magnitude, and the bits of a magnitude carry
no exploitable structure. It is also wrong when the universe is large: a mask
over 10⁵ items does not exist, however tempting the word "subset" is. And
`x >> 1` instead of `x // 2` is not an optimisation; compilers have done that
substitution for decades.

## The idea

Write the operands one above the other so their bits line up in columns, indexed
from the right starting at 0. Then:

**`&`, `|`, `^` and `~` act on each column alone.** Column `b` of `a & c` is a
function of column `b` of `a` and column `b` of `c`, and of nothing else. Shifts
slide the columns sideways. Addition and subtraction are the outliers — a carry
leaves column `b` and lands in column `b + 1` — which is exactly why they are the
hard ones and why per-column reasoning falls apart the moment a `+` appears.

<svg viewBox="0 0 690 215" role="img" aria-label="bitwise operators act on each column independently while addition carries into the next column">
  <g>
    <text x="10" y="18">AND, OR, XOR: column b sees only column b</text>
    <rect x="20" y="30" width="38" height="26" rx="3"/>
    <rect x="62" y="30" width="38" height="26" rx="3"/>
    <rect x="104" y="30" width="38" height="26" rx="3"/>
    <rect class="fill" x="146" y="30" width="38" height="26" rx="3"/>
    <rect x="188" y="30" width="38" height="26" rx="3"/>
    <rect x="230" y="30" width="38" height="26" rx="3"/>
    <rect x="20" y="66" width="38" height="26" rx="3"/>
    <rect x="62" y="66" width="38" height="26" rx="3"/>
    <rect x="104" y="66" width="38" height="26" rx="3"/>
    <rect class="fill" x="146" y="66" width="38" height="26" rx="3"/>
    <rect x="188" y="66" width="38" height="26" rx="3"/>
    <rect x="230" y="66" width="38" height="26" rx="3"/>
    <line x1="14" y1="102" x2="274" y2="102"/>
    <rect x="20" y="112" width="38" height="26" rx="3"/>
    <rect x="62" y="112" width="38" height="26" rx="3"/>
    <rect x="104" y="112" width="38" height="26" rx="3"/>
    <rect class="fill" x="146" y="112" width="38" height="26" rx="3"/>
    <rect x="188" y="112" width="38" height="26" rx="3"/>
    <rect x="230" y="112" width="38" height="26" rx="3"/>
    <line x1="165" y1="24" x2="165" y2="146"/>
    <text x="14" y="168">one vertical slice is a whole self-contained problem</text>
    <text x="14" y="190">b = 5   4   3   2   1   0</text>
    <text x="400" y="18">addition: the carry crosses</text>
    <rect x="410" y="30" width="38" height="26" rx="3"/>
    <rect x="452" y="30" width="38" height="26" rx="3"/>
    <rect x="494" y="30" width="38" height="26" rx="3"/>
    <rect x="536" y="30" width="38" height="26" rx="3"/>
    <rect x="410" y="66" width="38" height="26" rx="3"/>
    <rect x="452" y="66" width="38" height="26" rx="3"/>
    <rect x="494" y="66" width="38" height="26" rx="3"/>
    <rect x="536" y="66" width="38" height="26" rx="3"/>
    <line x1="404" y1="102" x2="580" y2="102"/>
    <rect x="410" y="112" width="38" height="26" rx="3"/>
    <rect x="452" y="112" width="38" height="26" rx="3"/>
    <rect x="494" y="112" width="38" height="26" rx="3"/>
    <rect x="536" y="112" width="38" height="26" rx="3"/>
    <line x1="545" y1="60" x2="510" y2="26"/>
    <line x1="510" y1="26" x2="522" y2="30"/>
    <line x1="510" y1="26" x2="514" y2="38"/>
    <line x1="503" y1="60" x2="468" y2="26"/>
    <line x1="468" y1="26" x2="480" y2="30"/>
    <line x1="468" y1="26" x2="472" y2="38"/>
    <line x1="461" y1="60" x2="426" y2="26"/>
    <line x1="426" y1="26" x2="438" y2="30"/>
    <line x1="426" y1="26" x2="430" y2="38"/>
    <text x="400" y="168">column b is coupled to column b+1, so you</text>
    <text x="400" y="190">cannot solve the columns separately</text>
  </g>
</svg>

That picture pays for itself twice.

**Slicing.** If the quantity you want is a sum over columns — a total, a count, a
XOR — solve column `b` on its own, multiply by `2ᵇ`, and add. Thirty independent
one-bit problems are usually easier than one thirty-bit problem.

**Bundling.** A machine word is sixty-four parallel booleans, and a Python int is
as many as you like. A subset of a universe of size `n` *is* an integer in
`[0, 2ⁿ)`; union is `|`, intersection is `&`, symmetric difference is `^`,
membership is `(m >> i) & 1`. That is the bridge to [[subsets]] and
[[dp-bitmask]].

And one more sentence, which generates every identity in this chapter:

> For `x > 0`, subtracting 1 flips the lowest 1 to a 0 and turns every 0 below it
> into a 1. Everything above the lowest 1 is untouched.

## Worked by hand

Count the set bits of `156 = 10011100₂` with Kernighan's loop: while `x` is
non-zero, do `x &= x - 1` and add one to a counter. Eight columns are drawn for
legibility; the algorithm never asks how wide the word is.

| step | `x` | `x - 1` | `x & (x-1)` | bit cleared | count after |
| --- | --- | --- | --- | --- | --- |
| 1 | `10011100` | `10011011` | `10011000` | 2 (value 4) | 1 |
| 2 | `10011000` | `10010111` | `10010000` | 3 (value 8) | 2 |
| 3 | `10010000` | `10001111` | `10000000` | 4 (value 16) | 3 |
| 4 | `10000000` | `01111111` | `00000000` | 7 (value 128) | 4 |
| 5 | `00000000` | — | — | — | loop guard fails, stop |

Answer 4, which is right: `10011100` has ones at columns 2, 3, 4 and 7.

<svg viewBox="0 0 560 150" role="img" aria-label="x and x minus one aligned, showing the region at and below the lowest set bit where they differ">
  <g>
    <text x="10" y="30">x</text>
    <text x="60" y="30">1  0  0  1  1  0  0</text>
    <text class="fill" x="260" y="30">1  0  0</text>
    <text x="10" y="60">x-1</text>
    <text x="60" y="60">1  0  0  1  1  0  0</text>
    <text class="fill" x="260" y="60">0  1  1</text>
    <line x1="252" y1="12" x2="252" y2="72"/>
    <line x1="252" y1="72" x2="350" y2="72"/>
    <text x="256" y="95">complemented: the borrow ripple</text>
    <text x="60" y="95">identical above the lowest 1</text>
    <text x="10" y="128">AND keeps the identical part and kills the rest</text>
  </g>
</svg>

Four things the trace shows that the four lines of code do not.

**The loop ran four times, not eight.** The iteration count is the popcount, not
the width. That makes the cost data-dependent, and it is why this loop is the
right one for sparse values and the wrong one when you need a predictable bound.

**The bits came out lowest first.** Step 1 cleared column 2, then 3, then 4, then
7. The loop is therefore an *enumeration of the members of a set in increasing
order*, not only a counter. Replace the counter with `b = x & -x` and you have
`for each element of the mask`, which is the workhorse of [[subsets]].

**Look at the `x - 1` column.** Above the lowest 1 it is character-for-character
identical to `x`; at the lowest 1 and below it, it is the exact complement. That
is the borrow ripple, drawn. Every identity in the trap-avoidance table later —
`x & -x`, `x & (x+1)`, `x | (x+1)` — is that same observation with different
operands, and none of them is worth memorising once you can re-derive it in ten
seconds.

**Nothing in the trace mentioned a width.** Which is a gift: the loop works
unchanged on a 400-bit Python int. It is also the bug, because a negative Python
int has infinitely many leading ones, and step 5 never happens.

## Why it is correct

:::proof Kernighan's loop counts the set bits, in exactly that many iterations
**Notation.** For an integer `x >= 0` write `x = Σ_{b>=0} x_b · 2ᵇ` with each
`x_b ∈ {0,1}` and only finitely many non-zero; this representation is unique.
Define `pc(x) = Σ_b x_b`. The definition of bitwise AND is columnwise:
`(u & v)_b = u_b · v_b`.

**Lemma (the borrow ripple).** Let `x > 0` and let `k` be the least index with
`x_k = 1`. Then `(x-1)_b = x_b` for `b > k`, `(x-1)_k = 0`, and `(x-1)_b = 1` for
`b < k`.

*Proof.* By the choice of `k`, `x = Σ_{b>k} x_b 2ᵇ + 2ᵏ`. Hence
`x - 1 = Σ_{b>k} x_b 2ᵇ + (2ᵏ - 1) = Σ_{b>k} x_b 2ᵇ + Σ_{b<k} 2ᵇ`, using the
identity `2ᵏ - 1 = Σ_{b=0}^{k-1} 2ᵇ`. The right-hand side is a sum of distinct
powers of two, so by uniqueness of the binary representation those are the bits
of `x - 1`, and they are exactly as claimed. ∎

**Corollary.** `x & (x-1) = x - 2ᵏ`, and `pc(x & (x-1)) = pc(x) - 1`.

*Proof.* Columnwise. For `b > k`: `x_b · x_b = x_b`. At `b = k`: `1 · 0 = 0`. For
`b < k`: `x_b = 0` by minimality of `k`, so `0 · 1 = 0`. The result therefore has
precisely the bits of `x` strictly above `k`, which is `x - 2ᵏ`, and it has one
fewer set bit. ∎

**Invariant.** At the top of every iteration, with `c` the counter and `x` the
current value: `x >= 0` and `c + pc(x) = pc(x₀)`.

**Base case.** Before the first iteration `c = 0` and `x = x₀ >= 0`, so the sum is
`pc(x₀)`.

**Inductive step.** Assume the invariant and that the guard `x != 0` passes.
With `x >= 0` from the invariant, `x != 0` gives `x > 0`, so the lemma applies.
The body replaces `x` by `x - 2ᵏ`, which is `>= 0` and has popcount `pc(x) - 1`,
and increments `c`. The sum `c + pc(x)` is unchanged and `x >= 0` still holds, so
the invariant is restored.

**Termination.** `pc(x)` is a non-negative integer that strictly decreases on
every iteration, so the loop cannot run more than `pc(x₀)` times. It exits only
via the guard, that is with `x = 0`.

**Conclusion.** On exit `pc(x) = pc(0) = 0`, so the invariant reads
`c = pc(x₀)`. And since each iteration removed exactly one set bit, the number of
iterations is exactly `pc(x₀)`. ∎
:::

Now say out loud what that argument leaned on, because that list is the bug list.

- **`x >= 0`, and finitely many ones.** It is a precondition, not decoration. A
  negative Python int behaves like an infinite run of leading ones: `pc(x)` is not
  finite, the decreasing quantity does not exist, and the loop spins forever.
  Languages with a fixed width do terminate on negatives — and return the
  popcount of the two's-complement pattern, which is a different number from what
  the caller usually meant. Either way, decide the width before you write the
  loop.
- **Uniqueness of the binary representation.** Used to read the coefficients off
  in the lemma. Over the non-negative integers this is free. In a fixed width with
  wraparound you are working modulo `2^W`, the ripple lemma still holds
  bit-for-bit, but the arithmetic reading "`x - 2ᵏ`" is only correct mod `2^W`.
  That is the difference between reasoning about patterns and reasoning about
  values, and it is why *Check Endianness Of A Byte Array* pins the width in its
  first sentence.
- **AND is columnwise.** Never justified above, because it is the definition. But
  notice where the proof had to work: the lemma about `x - 1` needed a real
  argument precisely because subtraction is *not* columnwise. Any time you find
  yourself assuming that a `+` or a `-` respects column boundaries, stop.
- **No overflow.** Free in Python. In C or Java on a signed 32-bit type, `-x` at
  `INT_MIN` overflows, which makes the idiom `x & -x` undefined there; the fix is
  an unsigned type or `x & (~x + 1)`, not a comment.

:::note Derive, do not memorise
`x & -x` falls out of the same lemma. In two's complement `-x = ~x + 1`. The
trailing zeros of `x` are trailing ones in `~x`, so adding 1 ripples through
exactly those positions and stops at column `k`: the result agrees with `~x`
above `k`, is 1 at `k`, and is 0 below. ANDing with `x`, the columns above `k`
are `x_b · (1 - x_b) = 0`, column `k` is `1 · 1 = 1`, and below is `0`. So
`x & -x = 2ᵏ`. Two lines. Do it once with a pen and the identity stops being
folklore.
:::

## What it costs

Assume a word of `W` bits and values below `2^W`.

**Naive popcount** tests every column: `Θ(W)`, regardless of the value.

**Kernighan's loop** costs exactly `pc(x)` iterations, by the proof. Worst case
`W`, best case 0. The average over all `W`-bit values is a counting argument:
`Σ_{x < 2^W} pc(x) = W · 2^{W-1}`, because each of the `W` columns is set in
exactly half the values; dividing by `2^W` gives `W/2`. So half the naive loop on
average, and far better than that on sparse inputs.

**Popcount for a whole range at once** is a one-line dynamic program:
`dp[i] = dp[i >> 1] + (i & 1)`, because dropping the lowest bit of `i` leaves a
strictly smaller index. That is `Θ(N)` for every value up to `N`. *Cardinality
Sorting* sorts 10⁵ values below 10⁶ by popcount and can use either. *Count Pairs*
needs even less — only the histogram of popcounts, then `Σ c·(c-1)/2` over the
buckets, which turns a quadratic pair count into a linear one.

**`bin(x).count("1")`** builds a `W`-character string on the heap and scans it:
`Θ(W)` with a bad constant. Fine once, wrong inside a hot loop.

**Slicing beats pairing.** *Sum of XOR Across Cartesian Pairs* has
`|L|, |R| <= 2 · 10⁴`, so the direct double loop is `4 · 10⁸` XORs. Slice instead.
Column `b` of `a ^ c` is 1 exactly when `a` and `c` disagree there, so if `L` has
`p` values with bit `b` set and `R` has `q`, the number of disagreeing ordered
pairs is `p(|R| - q) + (|L| - p)q`, and that column contributes
`2ᵇ · [p(|R|-q) + (|L|-p)q]` to the total. Summing over `W = 30` columns costs
`Θ(W(|L| + |R|)) = 1.2 · 10⁶` bit reads — three hundred times less work, and the
runnable block below checks the two agree. Note what made it legal: the objective
was a *sum of column contributions*. Replace XOR by `+` in the statement and the
method dies, because carries make column `b` depend on column `b - 1`.

**Subsets and submasks.** Iterating all masks over `n` items is `2ⁿ`. Iterating
every submask of every mask is `Σ_{m} 2^{pc(m)} = Σ_k C(n,k) 2ᵏ = (1+2)ⁿ = 3ⁿ` by
the binomial theorem. That number decides feasibility: `3^16 ≈ 4.3 · 10⁷` is fine,
`3^20 ≈ 3.5 · 10⁹` is not, while `2^20 ≈ 10⁶` is comfortable. Carry both.

**Space.** A mask is one integer. A DP indexed by subsets of `n` items is `2ⁿ`
entries: at `n = 20` that is 10⁶ numbers, which Python will hold; at `n = 24` it
is 1.6 · 10⁷ and it will not.

**The cost people forget** is that Python integers are arbitrary precision.
CPython stores them in 30-bit digits, so an operation on a `B`-bit integer is
`Θ(B/30)`, not `O(1)`. Using an int as a bitset over 10⁶ elements is a genuine
technique — the loop runs in C and is often the fastest thing available — but its
honest complexity is `Θ(n/64)` per operation. Quote `O(1)` for a bitset only when
the universe fits in a word. See [[big-integers]].

## The implementation

```python run
def popcount(x):
    """Kernighan's loop: exactly one iteration per set bit."""
    assert x >= 0, "undefined for negatives: a Python int has no fixed width"
    c = 0
    while x:
        x &= x - 1                      # clear the lowest set bit
        c += 1
    return c


def lowest_bit(x):   return x & -x          # that bit as a power of two; 0 if x == 0
def drop_lowest(x):  return x & (x - 1)     # x without it
def is_pow2(n):      return n > 0 and n & (n - 1) == 0
def test(x, i):      return (x >> i) & 1
def set_(x, i):      return x | (1 << i)
def clear(x, i):     return x & ~(1 << i)
def flip(x, i):      return x ^ (1 << i)


n = 156
print("n           ", format(n, "08b"), n)
print("n - 1       ", format(n - 1, "08b"), n - 1, "  borrow ripples to the lowest 1")
print("n & (n - 1) ", format(drop_lowest(n), "08b"), drop_lowest(n), "  lowest 1 cleared")
print("n & -n      ", format(lowest_bit(n), "08b"), lowest_bit(n), "   lowest 1 isolated")
print("popcount(n) ", popcount(n))
print()

for x in range(1 << 12):
    assert popcount(x) == bin(x).count("1")
    assert lowest_bit(x) | drop_lowest(x) == x        # the split is exact
    assert lowest_bit(x) & drop_lowest(x) == 0        # and disjoint
    assert is_pow2(x) == (x > 0 and popcount(x) == 1)
    for i in range(12):
        assert test(set_(x, i), i) == 1 and test(clear(x, i), i) == 0
        assert flip(flip(x, i), i) == x
print("4096 values: popcount, the lowest-bit split, the power-of-two test and")
print("get/set/clear/flip all agree with their definitions")

powers = [x for x in range(1 << 12) if is_pow2(x)]
print("powers of two under 4096:", powers)
assert powers == [1 << k for k in range(12)]
assert not is_pow2(0) and not is_pow2(-8)
print("is_pow2(0) =", is_pow2(0), " is_pow2(-8) =", is_pow2(-8), "- the n > 0 guard earns its keep")
```

Three lines are doing the work.

`x &= x - 1` is the engine. It clears one bit per iteration, which is both the
correctness argument and the cost argument, and it is why the same four lines
answer "how many bits", "which bits" and "is this a power of two".

`x & -x` relies on Python's integers behaving like infinite two's complement, so
`-x` is well defined for every `x`. Ported to C or Java on a signed type it is
undefined at the minimum value; write `x & (~x + 1)` or use `unsigned`.

`n > 0 and n & (n - 1) == 0` is *Power of Two Without Division* and *Powers of 2*
exactly. Two details hide in it. The guard is not defensive programming: without
it, `0 & -1 == 0` reports that zero is a power of two, and every negative input
would need thinking about as well. And the precedence is a language fact worth
knowing — Python binds `&` tighter than `==`, so the expression means
`(n & (n-1)) == 0`, while C, C++ and Java bind `==` tighter and read the same
characters as `n & ((n-1) == 0)`, which is always 0. Parenthesise when you leave
Python.

The identities worth keeping to hand, all of them one application of the ripple
lemma:

| want | write |
| --- | --- |
| test / set / clear / flip bit `i` | `(x >> i) & 1` · `x \| (1 << i)` · `x & ~(1 << i)` · `x ^ (1 << i)` |
| lowest set bit, isolated | `x & -x` |
| lowest set bit, cleared | `x & (x - 1)` |
| lowest zero bit, set | `x \| (x + 1)` |
| trailing ones, cleared | `x & (x + 1)` |
| a mask of the low `k` bits | `(1 << k) - 1` |
| number of significant bits | `x.bit_length()` |
| flip only the significant bits | `x ^ ((1 << x.bit_length()) - 1)` |

That last row is *Invert Ad Visibility Bits*, and it is in the table because the
obvious `~x` is wrong; see *Traps*.

## Variants you will meet

**XOR as a cancelling group.** `a ^ a = 0`, `a ^ 0 = a`, and XOR is commutative
and associative, so a XOR over a multiset forgets everything except the parity of
each value's count. That gives *Find the Missing Number from 1 to n* in one pass
and no extra space. *Missing and Repeated Number* is the two-unknown version: XOR
everything to get `a ^ b`, take `lowest_bit` of that to find a column where the
two differ, and partition the input by that column so each side XORs down to one
answer. Full treatment in [[xor-tricks]].

**Prefix XOR.** `xor(l..r) = P[r] ^ P[l-1]`, exactly as prefix sums work for `+`,
because XOR has inverses. *Count Subarrays With Given XOR* then becomes "how many
earlier prefixes equal `P[r] ^ x`", which is a dictionary lookup: see
[[prefix-sums]] and [[hash-tables]].

**Per-column counting.** When every value contributes independently per column,
process the columns. *Single Number with Triplicates* counts each column modulo 3
and keeps the residue. The runnable block below does *Sum of XOR Across Cartesian
Pairs*.

**Masks as sets.** A 26-bit mask per word gives `ma & mb == 0` for "no shared
letter" — *Count String Pairs With Disjoint Characters*, *Maximum
Unique-Character Word Subset*. Enumerating the masks themselves is [[subsets]];
using a mask as a DP state is [[dp-bitmask]], which is how *Shortest Path
Visiting All Nodes* and *Minimum Stickers to Form a Target String* are solved.

**Submask enumeration.** `s = (s - 1) & m`, starting at `s = m` and stopping after
`s == 0`, visits every submask of `m` exactly once and in decreasing order. It is
the ripple lemma again, restricted to the bits of `m`.

**Greedy from the top bit.** When you may set bits and want the largest result,
decide the highest column first, because `2ᵇ > Σ_{j<b} 2ʲ`: one high bit beats
every combination of lower ones. *Find Y Value* spends its `maxSet` ones on the
highest columns where `x` has a zero. *Maximum XOR Between Two Arrays* is the
same greedy made searchable with a [[trie]] over the bits.

**Fixed-width surgery.** Paired masks and shifts move many fields at once:
`((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)` is *Swap Even and Odd Bits* in
one expression, and the nibble version with `0xF0F0F0F0` / `0x0F0F0F0F` is *Swap
Adjacent Nibbles*. *CIDR IPv4 Range Iterator* builds a prefix mask as
`(0xFFFFFFFF << (32 - p)) & 0xFFFFFFFF`; the network is `addr & mask` and the
broadcast is `addr | ~mask`, masked back to 32 bits.

**Arithmetic without arithmetic.** `a ^ b` is addition with the carries thrown
away and `(a & b) << 1` is the carries, so looping until the carry is zero adds
two numbers with no `+`. Binary exponentiation is the same idea for
multiplication and is its own chapter, [[fast-exponentiation]]. The XOR swap of
*Swap Two Numbers Without a Third Variable* belongs here too, along with its trap.

**The number as an invariant.** *Minimum Tokens Remaining* is the purest example
in the bank: the exchange preserves `Σ A[i] · 2ⁱ`, a sum of powers of two needs at
least `popcount` terms, and that bound is achievable. One line of bit manipulation
after one line of [[invariants|invariant-spotting]].

```python run
import random

WIDTH = 30                                    # values are below 2^30


def brute(left, right):
    return sum(a ^ b for a in left for b in right)


def by_column(left, right):
    """Sum of (a XOR b) over all ordered pairs, one bit column at a time."""
    total = 0
    for b in range(WIDTH):
        ones_l = sum((a >> b) & 1 for a in left)
        ones_r = sum((c >> b) & 1 for c in right)
        # column b of a ^ c is 1 exactly when the two operands disagree there
        disagree = ones_l * (len(right) - ones_r) + (len(left) - ones_l) * ones_r
        total += disagree << b
    return total


left, right = [5, 9, 3], [6, 2]
print("left =", left, "  right =", right)
print("   b   ones in left   ones in right   disagreeing pairs   contributes")
for b in range(4):
    ol = sum((a >> b) & 1 for a in left)
    orr = sum((c >> b) & 1 for c in right)
    d = ol * (len(right) - orr) + (len(left) - ol) * orr
    print("   %d         %d               %d                  %d               %4d"
          % (b, ol, orr, d, d << b))
print("column total:", by_column(left, right), "   brute force:", brute(left, right))
assert by_column(left, right) == brute(left, right)

rng = random.Random(20)
for _ in range(300):
    L = [rng.randrange(1 << WIDTH) for _ in range(rng.randint(1, 8))]
    R = [rng.randrange(1 << WIDTH) for _ in range(rng.randint(1, 8))]
    assert by_column(L, R) == brute(L, R), (L, R)
print("300 random instances agree with the quadratic answer")

n = m = 20000                                  # the stated limits
print("brute force: %d pair XORs" % (n * m))
print("by column  : %d bit reads, a factor of %d less"
      % (WIDTH * (n + m), (n * m) // (WIDTH * (n + m))))
```

## Recognising it in a statement

Ordered by how much you should trust them.

1. **The words "bitwise", XOR, AND, OR, "set bits", "binary representation"
   appear literally.** *Count Valid Bitwise Pairs* writes out a page of bitwise
   algebra that collapses, via `a|b = (a&b) + (a^b)`, to `A_i + (A_i ^ A_j) = K`.
   *Maximum Profit Under a Bitwise OR Limit* says it in the title.
2. **A tiny `n` next to a "choose a subset" verb.** `n <= 20` and "select any
   subset", "visit all nodes", "assign each item": 2ⁿ masks. The constraint is the
   algorithm.
3. **Values bounded by a small power of two.** `0 <= arr[i] < 2^20` in *Get
   Minimum Moves to Zero*, `values[i] < 1024` in *Maximum Profit Under a Bitwise
   OR Limit*. This is an instruction to index by *value* or by *column*, not by
   position.
4. **A universe of 26 letters, plus "distinct" or "no repeated character".**
   One int per word. *Count String Pairs With Disjoint Characters*.
5. **"Each element appears twice except one", "exactly one is missing", "even
   number of occurrences".** Parity, therefore XOR. *Find the Missing Number from
   1 to n*, *Missing and Repeated Number*, *Longest Substring with Even
   Occurrences*.
6. **Width vocabulary: "unsigned 32-bit", "nibble", "byte array", "endianness",
   "CIDR", "prefix length", "mask".** The bits are the problem domain, not a
   trick. *Check Endianness Of A Byte Array* and *CIDR IPv4 Range Iterator*.

The anti-signals:

- **The numbers are magnitudes.** If every operation is a comparison, a sum or a
  sort, bits buy nothing. "Power of two" appearing in a *constraint* is usually
  just a size, not a hint.
- **"Subset" with a large `n`.** 10⁵ items and "choose a subset" is a
  [[dynamic-programming]] or [[greedy]] problem. Masks stop existing somewhere
  around `n = 25`.
- **A shift that is not a bit shift.** *Minimum Right Shifts to Sort the Array*
  has "shift" in the title and no bit anywhere in it — the shift is of array
  positions. Read the object being shifted.
- **"Optimise this with bit tricks."** Replacing `% 2` with `& 1` or `* 2` with
  `<< 1` changes nothing that a compiler had not already done. If the bit
  manipulation is not changing the *complexity*, it is not the answer to the
  question.

## Traps

**`~x` is not "flip the bits of x".** In Python it is `-x - 1`, an integer with
infinitely many leading ones. *Invert Ad Visibility Bits* asks for the
significant bits only, which is `x ^ ((1 << x.bit_length()) - 1)`. Symptom: a
negative answer where a positive one was expected.

**A popcount that forgets the width.** `bin(-5).count("1")` returns 2, because
`bin` prints a minus sign and the magnitude; the 32-bit answer is 31. Symptom:
correct on the samples, wrong on any negative input. Mask first: `x & 0xFFFFFFFF`.

**Kernighan's loop on a negative.** It never terminates in Python. Symptom: a
hang, with no exception to read.

**Floating point instead of bits.** `math.log2(x).is_integer()` looks like a
power-of-two test and is wrong from `2⁴⁹ - 1` upward, where the double rounds to
exactly 49.0. Symptom: a single wrong answer on a large input, which no amount of
re-reading the loop will find. See [[numerical-stability]].

**XOR swap on the same storage.** `a[i] ^= a[j]; a[j] ^= a[i]; a[i] ^= a[j]`
works beautifully until `i == j`, where the first line zeroes the cell and the
value is gone. The interview problems *Swap Two Numbers Without a Third Variable*
and *Swap Two Integers Without a Temporary Variable* ask for this idiom; the
aliasing case is what the interviewer is waiting for. It is also not faster than
a temporary on any processor made this century.

**Assuming `+` respects columns.** The most expensive mistake in this chapter,
because it is invisible. A per-column count is valid for XOR, AND and OR
aggregates; the instant the objective contains a sum of the values, carries couple
the columns and the decomposition is simply false.

**Precedence, once you leave Python.** `x & 1 == 0` means `(x & 1) == 0` here and
`x & (1 == 0)` in C, C++ and Java — always zero, always silently.

**Fixed-width footguns elsewhere.** `1 << 31` overflows a signed 32-bit `int`
(write `1L`); shifting by 32 or more is undefined in C and is a shift by
`k mod 32` in Java; `>>` is arithmetic and `>>>` is logical. And `x & -x` on zero
returns 0, which is not a bit — guard before taking its `bit_length()`.

```python run
import math

# 1. ~n is not "flip the significant bits"
n = 156
mask = (1 << n.bit_length()) - 1
print("n          ", format(n, "08b"), n)
print("~n         ", ~n, "       <- Python ints carry infinitely many leading 1s")
print("n ^ mask   ", format(n ^ mask, "08b"), n ^ mask, "  <- flip the significant bits only")
assert ~n == -157 and n ^ mask == 99

# 2. a popcount that forgets the width
x = -5
print()
print("bin(-5)                ", bin(x), "-> count('1') =", bin(x).count("1"))
w = x & 0xFFFFFFFF
print("(-5) & 0xFFFFFFFF      ", format(w, "032b"), "-> popcount", bin(w).count("1"))
assert bin(x).count("1") == 2 and bin(w).count("1") == 31

# 3. a power-of-two test routed through floating point
bad = 2 ** 49 - 1
print()
print("is 2**49 - 1 a power of two?")
print("   math.log2(x).is_integer() ->", math.log2(bad).is_integer(),
      " because log2 returned", repr(math.log2(bad)))
print("   x > 0 and x & (x - 1) == 0 ->", bad > 0 and bad & (bad - 1) == 0)
assert math.log2(bad).is_integer() and bad & (bad - 1) != 0

# 4. the XOR swap, and the input that destroys a value
def xor_swap(a, i, j):
    a[i] ^= a[j]
    a[j] ^= a[i]
    a[i] ^= a[j]

arr = [7, 11, 3]
xor_swap(arr, 0, 1)
print()
print("xor_swap on two different slots:", arr)
assert arr == [11, 7, 3]
arr = [7, 11, 3]
xor_swap(arr, 2, 2)
print("xor_swap when i == j:           ", arr, "<- the 3 is gone")
assert arr[2] == 0
```

## What to memorise

One sentence, one loop, one habit.

**The sentence**, from which the whole identity table is re-derivable in seconds:
*subtracting 1 flips the lowest 1 and every 0 beneath it, and changes nothing
above.* If you remember this you never have to remember whether it was `x & (x-1)`
or `x & (x+1)` that clears the low bit.

**The loop**, worth typing from muscle memory:

```python
while x:
    b = x & -x          # the lowest set bit, isolated
    i = b.bit_length() - 1
    x &= x - 1          # drop it and continue
```

That is simultaneously a popcount, an iteration over the members of a set, and
the inner loop of half of [[dp-bitmask]].

**The habit**: before writing anything, say how wide the word is. "Thirty columns,
values below 2³⁰." "Thirty-two bits, unsigned." "Twenty-six letters." Almost every
bug in this chapter — `~x`, the popcount of a negative, the non-terminating loop,
the overflowing `1 << 31` — is the same bug: an operation applied at a width
nobody decided on.

Numbers worth carrying: `2¹⁰ ≈ 10³`, `2²⁰ ≈ 10⁶`, `2³⁰ ≈ 10⁹`, `2³¹ - 1 =
2147483647`; `3ⁿ` for all-submasks-of-all-masks, which is fine to about `n = 16`;
26 letters fit in one integer; and `2ᵇ > Σ_{j<b} 2ʲ`, the inequality that licenses
every greedy that starts at the top bit.

## Check yourself

:::check
Why does `n > 0 and n & (n - 1) == 0` test for a power of two — and what goes
wrong if you drop the `n > 0`?
--
By the corollary in the proof, for `n > 0` the expression `n & (n - 1)` equals
`n - 2ᵏ`, where `2ᵏ` is the lowest set bit. That is zero exactly when `n` has no
bits above `k`, that is when `n = 2ᵏ`, that is when `n` is a power of two. So the
test is not a trick; it is "clear the lowest set bit and see whether anything is
left".

Dropping the guard breaks two cases. `n = 0`: `0 & -1 == 0`, so zero is reported
as a power of two, and it is not. Negative `n`: in Python `-8 & -9 == -16`, which
is non-zero so the answer happens to be right, but in a fixed-width language the
pattern for `-2³¹` is a single set bit and the test reports true. *Power of Two
Without Division* states "every value less than or equal to 0 returns false" for
exactly this reason.
:::

:::check
Someone says: "use the XOR swap — it avoids a temporary, so it is faster and uses
less memory." Where are they wrong?
--
In three places, in increasing order of importance.

It is not faster. A compiler swaps two values in registers with no memory traffic
at all; the XOR version is three dependent instructions, each waiting on the
previous, where the ordinary swap is none. On a modern out-of-order core it is
strictly worse.

It does not save memory in any sense that matters. The "temporary" is a register,
not an allocation.

And it is wrong on an input the simple version handles: when the two operands are
the same storage location, `a[i] ^= a[i]` writes zero and the value is destroyed,
as the last runnable block shows. *Swap Two Numbers Without a Third Variable* asks
for the idiom, so write it — and write the `if i == j: return` guard next to it,
because that guard is the actual question.
:::

:::check
Derive the cost of "for every mask over `n` items, loop over all of its submasks",
and say what it implies about the largest `n` you can use.
--
A mask `m` with `pc(m) = k` has exactly `2ᵏ` submasks, since each of its set bits
is independently in or out. Grouping the masks by popcount, the total work is
`Σ_{m ⊆ [n]} 2^{pc(m)} = Σ_{k=0}^{n} C(n,k) · 2ᵏ`, and by the binomial theorem
that is `(1 + 2)ⁿ = 3ⁿ`.

An equivalent and prettier derivation: each of the `n` items is in neither `m` nor
the submask, in `m` only, or in both — three choices, independently, so `3ⁿ` pairs
`(submask, mask)`.

`3^16 ≈ 4.3 · 10⁷` is comfortable; `3^18 ≈ 3.9 · 10⁸` is borderline in C and
hopeless in Python; `3^20 ≈ 3.5 · 10⁹` is out. So a bitmask DP that enumerates
submasks lives at `n <= 16`, while one that only iterates masks and single bits is
`O(2ⁿ · n)` and reaches `n = 20`. Those two limits are different by a factor of
`(3/2)ⁿ`, and confusing them is the usual reason a [[dp-bitmask]] solution times
out.
:::

:::check
*Sum of XOR Across Cartesian Pairs* is solved in `Θ(30 · (|L| + |R|))` by counting
each bit column separately. Why does the identical method fail for the sum of
`left[i] + right[j]` over all pairs — and what is the honest way to do that one?
--
Because the column decomposition needs the objective to be a sum of independent
per-column contributions, and XOR provides that: column `b` of `a ^ c` is a
function of column `b` of `a` and column `b` of `c` alone, so the total is
`Σ_b 2ᵇ · (number of disagreeing pairs at b)`.

Addition does not provide it. Column `b` of `a + c` depends on the carry out of
column `b - 1`, which depends on every lower column. Counting ones per column and
weighting by `2ᵇ` would double-count precisely the places a carry fires.

The honest method for sums is not bit manipulation at all, it is algebra:
`Σ_i Σ_j (L[i] + R[j]) = |R| · ΣL + |L| · ΣR`, computed in `Θ(|L| + |R|)`. Which
is the useful lesson — reach for column slicing when the operator is bitwise, and
for distributivity when it is arithmetic.
:::

:::check
A candidate writes, for *Invert Ad Visibility Bits*, `return ~base10`, and says
"`~` is the bitwise complement, so this flips every bit". Where are they wrong,
and what is the correct expression?
--
`~` really is the bitwise complement — of an integer that, in Python, has
infinitely many leading zeros. Complementing turns them into infinitely many
leading ones, which is how Python represents negative numbers: `~156 == -157`.
Nothing is wrong with the operator; what is wrong is the unstated assumption that
the number has a width.

The problem defines the width for you: "beginning with the highest-order 1 bit".
That width is `base10.bit_length()`, so the mask of significant columns is
`(1 << base10.bit_length()) - 1` and the answer is
`base10 ^ ((1 << base10.bit_length()) - 1)`. For 156 that is `156 ^ 255 == 99`,
and `10011100` really has become `01100011`.

The same sentence fixes *Swap Even and Odd Bits* and *Swap Adjacent Nibbles*,
which specify 32 bits: do the shifts, then `& 0xFFFFFFFF`, because a Python `<<`
will happily carry a bit past column 31 that a hardware register would have
dropped.
:::
