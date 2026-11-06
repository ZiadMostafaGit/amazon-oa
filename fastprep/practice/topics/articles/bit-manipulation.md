# Bit Manipulation

> Most of these problems need far less than the numbers themselves: a parity per bit column, one bit as a set member, a remainder, a common divisor. Keep only that summary and the hard problem becomes a one-line loop.

## The problem it solves

Here is the problem that opens this chapter, from the bank:
[[p:chubb-unique-element-among-pairs|Find the Unique Element Among Pairs]].
You get an array in which every value appears exactly twice except one, which
appears once. Return the one.

```
nums = [4, 1, 2, 1, 2]      answer: 4
```

Up to 200,001 numbers, each between -10^9 and 10^9. The interviewer's follow-up
is always the same: now do it in O(1) extra space.

The first solutions anyone writes are all correct, and all of them are worth
writing down, because the technique is what is left after we remove their
waste.

- **Count by brute force.** For each value, scan the whole array and count its
  copies. Return the one with count 1. That is n scans of n numbers: n^2, which
  for 2·10^5 is 4·10^10 steps. Too slow.
- **Count with a dictionary.** One pass, a hash map from value to count, then
  find the count of 1. O(n) time, but O(n) memory: 10^5 distinct keys.
- **Sort, then look at neighbours.** After sorting, pairs sit next to each other,
  and the single value is the first position where `a[i] != a[i+1]` at an even
  index. O(n log n), and it either destroys the input or copies it.

The method this chapter builds uses one integer of memory and one pass:
`acc ^= x` for every x. By the end of the next section you will be able to derive
that line yourself, and the two lines that follow from it for harder versions.

### Why this chapter is about more than XOR

The roadmap node for this chapter is called *Bits & Maths*, and it has five
techniques: XOR cancels pairs, a bitmask as a set, counting bits and powers of
two, gcd with lcm and modular arithmetic, and primes with a sieve. They look like
five unrelated tricks. They are one habit applied to five kinds of summary.

- XOR keeps the **parity** of each bit column and forgets everything else.
- A bitmask keeps **membership**, one bit per element of a small universe.
- `n & (n - 1)` keeps **everything except the lowest set bit**.
- Modular arithmetic keeps the **remainder** and forgets the size.
- gcd keeps **what two numbers have in common**, and the sieve keeps **the
  smallest prime factor**, for every number at once.

In each case the brute force carries the whole number, or the whole history,
around. The answer depended on a small piece of it. The fast solution carries
only that piece. Two hundred and three problems in this bank are tagged bit
manipulation, and many more are "maths" problems that turn out to be the same
move.

### When it is the wrong tool

- **The numbers are magnitudes.** Sorting, sums, averages, comparisons. The bits
  of a magnitude carry no exploitable structure, and `x >> 1` instead of `x // 2`
  is not an optimisation: compilers have done that substitution for decades.
- **There is a carry.** Bitwise operators work on each column alone. Addition
  does not: a carry leaves column b and lands in column b+1. Any argument that
  treats columns separately dies the moment the objective contains a `+`.
- **The universe is large.** A bitmask over 10^5 items is not a "set in one
  integer"; it is a 10^5-bit number, and a subset DP over it does not exist.
  Masks stop being a technique somewhere around n = 20 to 25.
- **The answer needs order or position.** XOR forgets order completely. If the
  problem asks *where* the single element was, or which came first, a summary
  that commutes cannot answer it.

## Build it from the brute force

We start from the dictionary solution, because it is correct and nobody argues
with it, and we remove one waste at a time.

### Step 1: the dictionary

```
counts = {}
for x in nums: counts[x] = counts.get(x, 0) + 1
return the x with counts[x] == 1
```

On `[4, 1, 2, 1, 2]` the dictionary ends as `{4: 1, 1: 2, 2: 2}`. It stores, for
every value, the exact number of times it appeared. Count the memory: one entry
per distinct value, n/2 + 1 of them.

### Step 2: notice the first waste

Look at what the final step actually reads. It does not care whether a count is
2 or 4 or 1000. It asks one question: is the count 1, or is it 2? Under the
promise of the problem ("every other value appears exactly twice"), the only
thing that separates the answer from everything else is that its count is
**odd**.

So the counts are overkill. A count can be replaced by a single bit, its parity.
Instead of a dictionary of counts, keep a set of values seen an odd number of
times: add x when you see it, remove x when you see it again.

```
start  {}
see 4  {4}
see 1  {4, 1}
see 2  {4, 1, 2}
see 1  {4, 2}        the second 1 cancels the first
see 2  {4}           the second 2 cancels the first
```

The set ends with exactly the answer in it. That is already a real idea:
**pairs cancel**. But the set still has up to n/2 members in the middle of the
pass, so the memory is still O(n).

### You might think: "Just add everything up and subtract."

For [[p:gep-missing-number|Find the Missing Number from 1 to n]] that is exactly
right: the sum 1 + ... + n minus the sum of the array is the missing value. So it
is tempting to try it here. Sum of the array: 4 + 1 + 2 + 1 + 2 = 10. Then what?
You would need to subtract "twice the sum of the paired values", and you do not
know which values are paired without the set you were trying to avoid. The known
version, `2 * sum(set(nums)) - sum(nums)`, works: 2 · (4 + 1 + 2) - 10 = 4. But it
builds a set. The sum trick needs a *known* reference total, and here there is
none.

### Step 3: the leap, look at the columns instead of the values

Here is the move that makes this chapter. We are keeping one parity bit **per
value**, and there are too many values. What if we kept one parity bit **per bit
column** instead? There are only about 32 columns, however many values there
are.

Write the numbers in binary, one under the other, so that their bits line up:

| value | bit 2 (fours) | bit 1 (twos) | bit 0 (ones) |
|---|---|---|---|
| 4 | 1 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 1 | 0 |
| **ones in the column** | 1 | 2 | 2 |
| **odd?** | 1 | 0 | 0 |

Read the last row as a binary number: 100, which is 4. The answer.

Say why, slowly, because the whole chapter rests on it. Take any one column. The
value 1 appears twice, so whatever its bit in this column is, it contributes that
bit twice: either 0 + 0 or 1 + 1. Either way, an even number of ones. The same is
true for 2, and for every other paired value. So the paired values add an even
number of ones to **every** column. The single value adds its own bit, once. An
even number plus the single value's bit is odd exactly when the single value's
bit is 1. So the parity of column b is bit b of the answer.

Said the other way round: the paired values cannot change the parity of any
column, because they always arrive twice. Whatever parity is left was put there
by the value that arrived once.

<svg viewBox="0 0 600 300" role="img" aria-label="the values 4, 1, 2, 1, 2 written in binary under each other in three columns; the paired values contribute two ones to the columns they touch, drawn dashed; only column 2 has an odd count of ones, so the parity row reads 100, which is 4">
  <g>
    <text x="172" y="24" text-anchor="middle">bit 2</text>
    <text x="232" y="24" text-anchor="middle">bit 1</text>
    <text x="292" y="24" text-anchor="middle">bit 0</text>
    <text x="120" y="54" text-anchor="end">4</text>
    <rect class="fill" x="150" y="36" width="44" height="26" rx="3"/>
    <text x="172" y="54" text-anchor="middle">1</text>
    <rect x="210" y="36" width="44" height="26" rx="3"/>
    <text x="232" y="54" text-anchor="middle">0</text>
    <rect x="270" y="36" width="44" height="26" rx="3"/>
    <text x="292" y="54" text-anchor="middle">0</text>
    <text x="120" y="86" text-anchor="end">1</text>
    <rect x="150" y="68" width="44" height="26" rx="3"/>
    <text x="172" y="86" text-anchor="middle">0</text>
    <rect x="210" y="68" width="44" height="26" rx="3"/>
    <text x="232" y="86" text-anchor="middle">0</text>
    <rect x="270" y="68" width="44" height="26" rx="3" stroke-dasharray="5 4"/>
    <text x="292" y="86" text-anchor="middle">1</text>
    <text x="120" y="118" text-anchor="end">2</text>
    <rect x="150" y="100" width="44" height="26" rx="3"/>
    <text x="172" y="118" text-anchor="middle">0</text>
    <rect x="210" y="100" width="44" height="26" rx="3" stroke-dasharray="5 4"/>
    <text x="232" y="118" text-anchor="middle">1</text>
    <rect x="270" y="100" width="44" height="26" rx="3"/>
    <text x="292" y="118" text-anchor="middle">0</text>
    <text x="120" y="150" text-anchor="end">1</text>
    <rect x="150" y="132" width="44" height="26" rx="3"/>
    <text x="172" y="150" text-anchor="middle">0</text>
    <rect x="210" y="132" width="44" height="26" rx="3"/>
    <text x="232" y="150" text-anchor="middle">0</text>
    <rect x="270" y="132" width="44" height="26" rx="3" stroke-dasharray="5 4"/>
    <text x="292" y="150" text-anchor="middle">1</text>
    <text x="120" y="182" text-anchor="end">2</text>
    <rect x="150" y="164" width="44" height="26" rx="3"/>
    <text x="172" y="182" text-anchor="middle">0</text>
    <rect x="210" y="164" width="44" height="26" rx="3" stroke-dasharray="5 4"/>
    <text x="232" y="182" text-anchor="middle">1</text>
    <rect x="270" y="164" width="44" height="26" rx="3"/>
    <text x="292" y="182" text-anchor="middle">0</text>
    <line x1="140" y1="202" x2="324" y2="202"/>
    <text x="120" y="226" text-anchor="end">ones</text>
    <text x="172" y="226" text-anchor="middle">1</text>
    <text x="232" y="226" text-anchor="middle">2</text>
    <text x="292" y="226" text-anchor="middle">2</text>
    <text x="120" y="258" text-anchor="end">odd?</text>
    <rect class="fill" x="150" y="240" width="44" height="26" rx="3"/>
    <text x="172" y="258" text-anchor="middle">1</text>
    <rect x="210" y="240" width="44" height="26" rx="3"/>
    <text x="232" y="258" text-anchor="middle">0</text>
    <rect x="270" y="240" width="44" height="26" rx="3"/>
    <text x="292" y="258" text-anchor="middle">0</text>
    <text x="345" y="80">dashed: a pair puts two 1s</text>
    <text x="345" y="102">in each column it touches,</text>
    <text x="345" y="124">so it never changes a parity</text>
    <text x="345" y="258">parity row 100 = 4</text>
  </g>
</svg>

### Step 4: one bit per column, all columns at once

The column table costs 32 counters, one per column. That is O(1) memory already,
and a correct solution. But look at what we do with each counter: we only ever
need it mod 2. So each column needs one bit, "odd so far" or "even so far". When
a new number arrives with a 1 in column b, that bit flips. When it arrives with a
0, the bit stays.

"Flip where the new number has a 1, keep where it has a 0" is exactly the
definition of exclusive or, column by column:

| acc bit | x bit | acc ^ x |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

XOR is **addition in each column with the carry thrown away**. 1 + 1 = 2, which is
0 with a carry; drop the carry and you get 0. That is why it computes parity. And
the machine does it for all 64 columns in one instruction. So the 32 counters
collapse into a single integer, and the whole algorithm is:

```
acc = 0
for x in nums: acc ^= x
return acc
```

We did not invent XOR as a trick. We asked for parity per column and XOR is the
name of that operation.

### You might think: "XOR finds the duplicate."

People remember "XOR and duplicates" and apply it to any array with repeats. Try
`[1, 2, 4, 4]`, where 4 is the duplicate. 1 ^ 2 ^ 4 ^ 4 = 1 ^ 2 = 3. Not 4. XOR
removes every value that appears an even number of times and keeps the XOR of
those that appear an odd number of times. Here that is 1 and 2, mixed together
into 3. XOR answers "what is left after pairs cancel", which is the opposite of
"which one is paired". To find a duplicate with XOR you have to arrange for the
duplicate to be the odd one out, which is what
[[p:commvault-missing-and-repeated-number|Missing and Repeated Number]] does by
XOR-ing in 1..n as well (variation A).

### You might think: "It works for triplicates too."

[[p:goldman-sachs-single-number-ii|Single Number with Triplicates]]: every value
appears three times except one. Try `[5, 3, 5, 5]`. 5 ^ 3 ^ 5 ^ 5 = 5 ^ 3 = 6. The
answer is 3. Three copies of 5 are odd, so they do not cancel.

But the derivation tells you exactly what to do instead, and this is the payoff
of deriving rather than memorising. XOR was "count each column mod 2" because the
copies came in twos. With threes, **count each column mod 3**:

| value | bit 2 | bit 1 | bit 0 |
|---|---|---|---|
| 5 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 |
| 5 | 1 | 0 | 1 |
| 5 | 1 | 0 | 1 |
| ones | 3 | 1 | 4 |
| mod 3 | 0 | 1 | 1 |

011 is 3. The tripled values put a multiple of three ones into every column. The
idea survives; only the modulus changed. Someone who learned "XOR the array" has
nothing to say about this problem. Someone who learned "the pairs contribute a
multiple of 2 to every column" has the answer in one line.

### You might think: "Then I can count columns for sums too."

The column argument needs every column to be its own little problem. XOR, AND and
OR give you that: bit b of `a ^ c` depends only on bit b of a and bit b of c. Plus
does not. 1 + 1 in column 0 gives 0 there and a carry into column 1. Take
`a = 1, c = 1`: the per-column parity of their bits says column 0 has two ones,
so it is 0, and column 1 has none, so it is 0, giving 0. But 1 + 1 = 2. The carry
went into a column the counting never looked at. Whenever an argument splits a
number into columns, check that no `+` or `-` crosses them.

### The technique, and the question that unlocks it

The whole derivation was one question asked twice: what does the answer really
depend on? First the answer was "the parity of each value's count", which
replaced counts with bits. Then "the parity of each bit column", which replaced
values with columns. Each step threw away information the answer never needed.

**What is the smallest summary of these numbers that the answer still depends
on?**

That is the question to ask on every problem in this chapter. For the single
element it is the parity of each column, and XOR keeps exactly that. For a subset
problem with n = 20 it is "which elements are in", and one integer of 20 bits
holds exactly that. For "how many ways, modulo 10^9 + 7" it is the remainder, and
modular arithmetic keeps exactly that. For "can these two lengths tile each
other" it is the gcd.

The technique in one sentence: **read an integer as a row of independent bit
columns (or as a remainder, or as a set of factors), find the summary the answer
depends on, and update only that summary as the input streams by.**

## Worked by hand

### Trace 1: the accumulator on [4, 1, 2, 1, 2]

The column table above is the picture. The code does not build that table; it
keeps one running integer. Here is what that integer looks like after every step,
in binary, so you can check each column with a pen.

| step | x | x in binary | acc before | acc after | what happened |
|---|---|---|---|---|---|
| 0 | | | | 000 | start: every column even |
| 1 | 4 | 100 | 000 | 100 | column 2 becomes odd |
| 2 | 1 | 001 | 100 | 101 | column 0 becomes odd |
| 3 | 2 | 010 | 101 | 111 | column 1 becomes odd |
| 4 | 1 | 001 | 111 | 110 | column 0 back to even |
| 5 | 2 | 010 | 110 | 100 | column 1 back to even |

Final: 100 = 4.

Tell step 4 as a story. The accumulator is 111: every column has seen an odd
number of ones so far. The new number is 1, binary 001, so it has a one only in
column 0. Column 0 had seen one 1 (from the first 1); now it has seen two, so it
goes back to even, and its bit turns off. Columns 1 and 2 receive a 0 from this
number, so their parity does not change. 111 becomes 110.

Notice two things the trace shows that the code does not. First, in the middle of
the pass the accumulator holds **garbage**: 111 = 7 is not a value in the array.
It is the XOR of everything seen so far, 4 ^ 1 ^ 2, and it only becomes meaningful
once every pair has been completed. Second, the order did not matter. The second
1 arrived two steps after the first and still cancelled it. XOR is commutative and
associative, so the pairs do not need to be adjacent, or even in the same half of
the array.

### Trace 2: two singles, and why one accumulator is not enough

[[p:zomato-two-unique-numbers|Find the Two Unique Numbers]]: every value appears
twice except two, which appear once. Take `[1, 2, 1, 3, 2, 5]`; the answer is 3
and 5.

XOR everything: 1 ^ 2 ^ 1 ^ 3 ^ 2 ^ 5. The 1s cancel, the 2s cancel, and what is
left is 3 ^ 5:

```
3 = 011
5 = 101
    ---
    110  = 6
```

6 is neither answer. It is the two answers mixed together, and from 6 alone you
cannot tell 3 ^ 5 from 1 ^ 7 or 2 ^ 4. One accumulator has lost information we
need. This is the case the first trace could not show: **the summary can be too
small**, and then you have to ask the unlocking question again. What do we know
about 3 and 5 from 6?

Read 6 as columns. A 1 in column b of `a ^ b` means a and b *disagree* in column b.
6 = 110 says 3 and 5 disagree in columns 1 and 2, and agree in column 0. Pick one
column where they disagree, say column 1 (value 2), the lowest set bit of 6. Now
split the whole array by that column:

| x | binary | bit 1 set? | group |
|---|---|---|---|
| 1 | 001 | no | B |
| 2 | 010 | yes | A |
| 1 | 001 | no | B |
| 3 | 011 | yes | A |
| 2 | 010 | yes | A |
| 5 | 101 | no | B |

Group A is `[2, 3, 2]`; group B is `[1, 1, 5]`. Two facts make this work:

- **Each pair lands in one group.** Both copies of 2 have the same bits, so they
  agree on column 1 and go to the same side. The same for 1. So inside each group
  every paired value is still paired.
- **The two singles land in different groups.** We chose a column where they
  disagree, so one has a 1 there and the other a 0.

So each group is the first problem again: pairs plus exactly one single. XOR group
A: 2 ^ 3 ^ 2 = 3. XOR group B: 1 ^ 1 ^ 5 = 5. The answer is [3, 5].

The column must be one where the singles differ. That is the subtle line of this
chapter, and the next section shows what happens if you pick the wrong one.

## From the idea to the code

### The derivation, as code

The block below has every step of the derivation as its own function, so you can
see them agree: the dictionary, the parity set, the column counts, and the single
accumulator. It prints the column table and the accumulator trace from the
previous section.

```python run
from collections import Counter
import random

def by_counting(nums):                 # step 1: the dictionary
    return next(v for v, c in Counter(nums).items() if c == 1)

def by_parity_set(nums):               # step 2: keep only odd or even, per value
    odd = set()
    for x in nums:
        odd ^= {x}                     # add if absent, remove if present
    (v,) = odd
    return v

def by_columns(nums, width):           # step 3: count ones per column, keep parity
    result = 0
    for b in range(width):
        ones = sum((x >> b) & 1 for x in nums)
        if ones % 2 == 1:
            result |= 1 << b
    return result

def by_xor(nums):                      # step 4: one parity bit per column, all at once
    acc = 0
    for x in nums:
        acc ^= x
    return acc

nums = [4, 1, 2, 1, 2]
print("value  b2 b1 b0")
for x in nums:
    print("%5d   %d  %d  %d" % (x, x >> 2 & 1, x >> 1 & 1, x & 1))
ones = [sum(x >> b & 1 for x in nums) for b in (2, 1, 0)]
print("ones   ", "  ".join(map(str, ones)), "  -> parity", "".join(str(o % 2) for o in ones))

acc = 0
for x in nums:
    before, acc = acc, acc ^ x
    print("x=%d  %s ^ %s = %s" % (x, format(before, "03b"), format(x, "03b"), format(acc, "03b")))
assert acc == 4 == by_counting(nums) == by_parity_set(nums) == by_columns(nums, 3)

rng = random.Random(7)
for _ in range(500):
    pairs = rng.sample(range(-10**9, 10**9), rng.randint(0, 20))
    single = rng.choice([v for v in range(-50, 50) if v not in pairs])
    arr = pairs * 2 + [single]
    rng.shuffle(arr)
    assert by_xor(arr) == by_counting(arr) == by_parity_set(arr) == single
print("500 shuffled arrays, negatives included: all four methods agree")
assert by_xor([1, 2, 4, 4]) == 3        # "XOR finds the duplicate" is false
assert by_xor([5, 3, 5, 5]) == 6        # and it does not handle triplicates
```

### Each line, and which step of the derivation it is

| line | in plain words | step |
|---|---|---|
| `Counter(nums)` | exact count per value | step 1, the brute force |
| `odd ^= {x}` | toggle membership: pairs cancel | step 2, counts replaced by parity |
| `(x >> b) & 1` | read column b of x | step 3, values replaced by columns |
| `ones % 2` | only the parity of the column matters | step 3 |
| `acc = 0` | every column starts even | the empty array has XOR 0 |
| `acc ^= x` | flip each column where x has a 1 | step 4, all 32 parities at once |
| `return acc` | the parity row, read as a number | the answer |

Settle three boring confusions now.

**Why `acc` starts at 0.** 0 has every column even, which is the truth before any
number is seen. It is also the identity of XOR: `0 ^ x = x`. Starting anywhere
else adds a stray value that nothing will cancel.

**What `acc` holds in the middle.** Not a value from the array. It is the XOR of
the prefix seen so far. It means nothing until every pair is complete.

**Negative numbers.** The bank's version allows -10^9. In Python, XOR on negative
integers behaves as if every number had infinitely many leading copies of its
sign bit, and the parity argument still holds column by column, including those
infinite columns: a pair of negatives cancels its infinite ones too. So `by_xor`
is right on negatives with no change, and the test above includes them. The
column counter is a different story: `by_columns(nums, 3)` reads only three
columns. For negatives you must decide a width and fix the sign at the end; the
triplicates block in *Variations* shows how.

### The subtle line, both ways

For two singles, the split column is the line that matters:

```
diff = xor of everything          # a ^ b
low  = diff & -diff               # a column where a and b differ
```

`diff & -diff` isolates the lowest set bit of `diff` (the *Variations* section
derives why). Any set bit of `diff` would do, because every set bit is a column
where the two singles disagree. The tempting wrong version picks a fixed column,
usually column 0, "split into odd and even numbers". That works whenever one
single is odd and the other is even. Our example has 3 and 5. Both are odd.

```python run
def two_singles(nums, pick):
    diff = 0
    for x in nums:
        diff ^= x
    low = pick(diff)
    a = b = 0
    print("   diff = %s, split on column value %d" % (format(diff, "03b"), low))
    for x in nums:
        side = "A" if x & low else "B"
        if x & low:
            a ^= x
        else:
            b ^= x
        print("   x=%d (%s) -> group %s   A=%d  B=%d" % (x, format(x, "03b"), side, a, b))
    return sorted([a, b])

nums = [1, 2, 1, 3, 2, 5]

print("RIGHT: split on the lowest set bit of a ^ b")
right = two_singles(nums, lambda d: d & -d)
print("   answer", right)

print("WRONG: split on column 0 (odd versus even)")
wrong = two_singles(nums, lambda d: 1)
print("   answer", wrong)

assert right == [3, 5]
assert wrong == [0, 6]          # both singles fell into group A and mixed again
# what the wrong version computes: when both singles share column 0,
# one group gets a ^ b and the other gets 0
assert wrong == sorted([3 ^ 5, 0])
# with one odd and one even single it happens to work, which is why tests miss it
assert two_singles([1, 4, 1, 7, 7, 9], lambda d: 1) == [4, 9]
```

Look at the wrong trace at x = 3. Group A already holds 1 ^ 1 = 0 from the two 1s
(both odd, so both went to A, which is fine: they cancelled). Then 3 arrives,
odd, goes to A. Then 5 arrives, odd, goes to A as well. That is the exact moment
it goes wrong: two singles in one group, and the group's XOR is 3 ^ 5 = 6 again.
Group B received only the 2s, which cancelled to 0. The wrong version computes
`[a ^ b, 0]`: it has done a lot of work to give back the number it started with.

The last assertion is the reason this bug survives testing. If the samples happen
to have one even and one odd single, splitting on column 0 is right. The general
rule is "split on a column where they differ", and `diff & -diff` is a column
where they differ by construction, because `diff` has a 1 exactly in those
columns. `diff` is never 0 here, because the singles are distinct, so a set bit
always exists.

## Why it is correct

:::proof XOR keeps exactly the values of odd multiplicity, and the split separates two singles
**Notation.** For an integer x >= 0 write bit b of x as x_b, so that
x = sum over b of x_b · 2^b with each x_b in {0, 1}. This representation is unique.
XOR is defined column by column: (u ^ v)_b = (u_b + v_b) mod 2. (For negative
numbers in Python, the same holds with infinitely many columns, and the argument
below goes through unchanged, because it never looks at more than one column at a
time.)

**Claim 1. For any list of integers, bit b of their XOR equals the number of
list elements with bit b set, taken mod 2.**

By induction on the length of the list. The empty list has XOR 0, so every bit is
0, and the count of elements with bit b set is 0, which is 0 mod 2. Suppose the
claim holds for a list L with XOR acc, and append x. The new XOR is acc ^ x. Its bit
b is (acc_b + x_b) mod 2. By the assumption, acc_b = (count in L) mod 2. So the new
bit is (count in L + x_b) mod 2, and count in L + x_b is exactly the count in the
longer list. The claim holds for the longer list.

**Claim 2. If every value in the list appears an even number of times except one
value s that appears an odd number of times, the XOR is s.**

Fix a column b. Group the elements by value. A value v that appears k times
contributes k · v_b ones to column b. For the paired values k is even, so k · v_b is
even. For s, k is odd, so k · s_b is odd when s_b = 1 and 0 when s_b = 0. The total
count in column b is therefore (even) + k · s_b, which is odd exactly when s_b = 1.
By Claim 1, bit b of the XOR is 1 exactly when s_b = 1. This holds for every column,
so the XOR and s agree in every bit, and by uniqueness of binary representation
they are the same number.

The same argument with "mod 3" in place of "mod 2" proves the triplicates method:
tripled values contribute 3 · v_b ones to each column, a multiple of three, so the
count mod 3 is s_b.

**Claim 3. In the two-singles problem with singles a and b, a != b, let d = a ^ b
and let c be any column with d_c = 1. Splitting the list by bit c, then XOR-ing each
side, gives a and b.**

d is not 0, since a != b and uniqueness of binary representation says two
different numbers differ in some column; so a column c with d_c = 1 exists. By
the definition of XOR, d_c = 1 means a_c != b_c, so a and b fall on different
sides. Every other value appears twice, and both copies have the same bit c, so
both copies fall on the same side. Each side is therefore a list in which every
value appears an even number of times except one single. By Claim 2, each side's
XOR is its single. ∎
:::

Now say in plain words what the proof leaned on, because each assumption is a
place the method breaks.

- **The multiplicities.** Claim 2 needs the paired values to appear an even
  number of times and the target an odd number. If the promise in the statement
  is broken (a value appears three times in a "pairs" problem), XOR silently
  returns the XOR of all odd-count values. It never raises an error.
- **Columns do not interact.** The whole proof works one column at a time. That is
  only legal because XOR has no carry. Change the operator to `+` and Claim 1 is
  false.
- **The split column must have d_c = 1.** Claim 3 used it to put the singles on
  different sides. Column 0 has that property only when exactly one single is odd.
- **Order is irrelevant.** Claim 1 is an induction over the list in any order, and
  the result does not depend on it, because addition mod 2 is commutative. That is
  also why XOR can never tell you *where* something was.
- **Uniqueness of binary representation.** Used to go from "agree in every bit" to
  "equal". It is free for integers. It is the reason a fixed width matters in other
  languages: in 32 bits, the pattern for -1 and the number 2^32 - 1 are the same
  bits, and which one you meant is a decision, not a fact.

## What it costs

**The XOR pass.** One XOR per element: O(n) time. One integer of memory: O(1)
space. For the 200,001 numbers of the opening problem that is 200,001 machine
operations.

**The brute forces, for comparison.** Nested counting is n · n = 4·10^10 steps
at that size. The dictionary is O(n) time but stores up to 10^5 keys, and each
step hashes. Sorting is O(n log n), about 3.5·10^6 comparisons, and moves the
data.

**The column counter.** W columns times n numbers: O(nW). With W = 32 that is 32
times the XOR pass, still linear and still O(1) memory. It is the price of
generality: it handles "mod 3" and any other modulus, while XOR handles only
"mod 2". Use XOR when the copies come in twos, the counter otherwise.

**The hidden cost: Python integers are not words.** CPython stores an int in
30-bit digits. An operation on a B-bit integer costs about B/30 steps, not one.
For values below 2^30 that is one digit and XOR is genuinely O(1). For a bitmask
over 10^6 elements, every `|` and `&` touches 33,000 digits. That can still be
the fastest thing available, because the loop runs in C, but quote its cost
honestly: O(n/30) per operation, not O(1). See [[big-integers]].

**Subsets and submasks.** Iterating all masks of n elements is 2^n. Iterating
every submask of every mask is 3^n, derived in *Check yourself*. 2^20 is about
10^6, comfortable. 3^16 is about 4.3·10^7, fine. 3^20 is 3.5·10^9, hopeless. Those
two numbers decide whether a mask solution is allowed at all.

**The maths half.** Derived in their variations below: Euclid's gcd is
O(log min(a, b)) divisions; fast exponentiation is O(log e) multiplications; the
sieve up to N is O(N log log N), which for N = 5·10^6 is a few times N; trial
division of one number up to 10^12 is up to 10^6 steps.

The trap in this section is the word "O(1)". It is true for one machine word. It
is false for a Python integer that has grown to millions of bits, and for a mask
over a universe that is not small.

## How to think about it

Ask these questions, in this order, on every problem that smells of bits or
numbers.

1. **What is the smallest summary of the input that the answer depends on?**
   Parity? A count mod k? Membership? A remainder? A common divisor? Say it in
   words before writing anything.
2. **Does the operation work column by column?** XOR, AND, OR: yes, so you may
   reason about one column and multiply by 2^b. Plus, minus, times: no, there are
   carries.
3. **What width are we in?** "Values below 2^30", "signed 32-bit", "26 lowercase
   letters", "n <= 20". Decide the width out loud. Almost every bug in this
   chapter is an operation applied at a width nobody chose.
4. **Is a mask a set here?** If the universe is small (letters, n <= 20 items),
   one integer is a subset, and union, intersection and difference are single
   operators.
5. **Is it a pair-cancellation problem in disguise?** "Appears twice except",
   "missing one", "even number of occurrences", "subarray XOR equals k".
6. **Does the answer only need a remainder?** "Modulo 10^9 + 7", "divisible by x",
   "last digit". Then reduce early and often, and remember division is special.
7. **Do the numbers share structure?** "Tile", "repeat", "period", "both
   divisible": gcd and lcm. "Prime", "factor", "divisors of every value up to
   10^5": a sieve.
8. **Is there a greedy from the top bit?** If you want the largest result and may
   set bits, the highest column beats all lower ones combined, because 2^b is
   larger than 2^(b-1) + ... + 1 = 2^b - 1.

Then, before coding, write two lines: **the summary in words** and **how one new
input element updates it**. For the opening problem: "the parity of each column;
a new number flips the columns where it has ones". If you can write those two
lines, the code is a loop.

### Telling it from its neighbours

- **Frequency counting** ([[frequency-counting]], [[hash-tables]]). The dictionary
  is always the safe first solution. Bits win only when the summary is smaller
  than the counts, or when O(1) memory is required.
- **XOR properties** ([[xor-tricks]]). That chapter goes deeper on the algebra of
  XOR: prefix XOR, XOR of ranges, linear bases. This chapter is where it is
  derived.
- **Prefix sums** ([[prefix-sums]]). Prefix XOR is the same idea with `^` instead
  of `+`, because XOR has an inverse (itself).
- **Subset enumeration and bitmask DP** ([[subsets]], [[dp-bitmask]]). A mask as a
  set is the bridge. Enumerating them is [[subsets]]; using one as a DP state is
  [[dp-bitmask]].
- **Maths** ([[math]], [[number-theory]], [[modular-arithmetic]], [[primes]],
  [[fast-exponentiation]]). Each of those has its own chapter. The variations below
  derive the core of each from its brute force, which is the part interviews ask.

## Variations

Nine variations. A to F are the bits half of the node, G to I the maths half.
Each says what changes, why, a tiny example, and a bank problem that teaches it.

### A. XOR cancels pairs: missing, repeated, prefix XOR

**What changes:** you arrange for the target to be the one value with odd
multiplicity.

- *Missing number.* [[p:gep-missing-number|Find the Missing Number from 1 to n]]:
  XOR the array with 1, 2, ..., n. Every present value now appears twice and
  cancels; the missing value appears once. `[1, 2, 4, 5]`, n = 5: XOR of 1..5 is
  1, XOR of the array is 2, and 1 ^ 2 = 3. (The sum version also works here,
  because the reference total is known.)
- *Missing and repeated.*
  [[p:commvault-missing-and-repeated-number|Missing and Repeated Number]]: XOR the
  array with 1..n. The repeated value r now appears three times (odd) and the
  missing value m once (odd); everything else twice. So the XOR is r ^ m, and you
  are in Trace 2: split on a set bit, then one more pass decides which of the two
  results is the repeated one (it is the one present in the array).
- *Two singles.* [[p:zomato-two-unique-numbers|Find the Two Unique Numbers]],
  Trace 2.
- *Prefix XOR.* Let P[i] = a[0] ^ ... ^ a[i-1]. Then the XOR of a[l..r] is
  P[r+1] ^ P[l], because the common prefix appears twice and cancels. "Count
  subarrays with XOR exactly x" becomes "for each r, how many earlier prefixes
  equal P[r+1] ^ x", a dictionary lookup:
  [[p:inmobi-count-subarrays-with-given-xor|Count Subarrays With Given XOR]]. This
  is [[prefix-sums]] with `^` in place of `+`.

### B. Count each column modulo k

**What changes:** XOR is "mod 2 per column". When copies come in k's, keep a count
per column and take it mod k. **Why:** k copies of a value contribute k · v_b ones
to column b, a multiple of k.
[[p:goldman-sachs-single-number-ii|Single Number with Triplicates]] is k = 3. The
same per-column thinking solves
[[p:ibm-sum-xor-cartesian-pairs|Sum of XOR Across Cartesian Pairs]]: column b of
`a ^ c` is 1 exactly when a and c disagree there, so if the left array has p
values with bit b set and the right has q, that column contributes
2^b · (p · (|R| - q) + (|L| - p) · q). That turns 4·10^8 pair XORs into 30 passes.

The one thing to get right with negatives is the width. The bank's triplicates
problem says "fits in a signed 32-bit integer", so count 32 columns, and if the
rebuilt bit 31 is set, the number was negative: subtract 2^32.

```python run
def single_of_triplicates(nums, width=32):
    result = 0
    for b in range(width):
        ones = sum((x >> b) & 1 for x in nums)   # Python: x >> b on a negative keeps its sign
        if ones % 3:
            result |= 1 << b
    if result >> (width - 1) & 1:                 # bit 31 set: it was negative
        result -= 1 << width
    return result

def xor_pairs_sum(left, right, width=30):
    total = 0
    for b in range(width):
        p = sum(a >> b & 1 for a in left)
        q = sum(c >> b & 1 for c in right)
        total += (p * (len(right) - q) + (len(left) - p) * q) << b
    return total

print("[5, 3, 5, 5]")
for b in (2, 1, 0):
    ones = sum(x >> b & 1 for x in [5, 3, 5, 5])
    print("  column %d: %d ones, mod 3 = %d" % (b, ones, ones % 3))
assert single_of_triplicates([5, 3, 5, 5]) == 3
assert single_of_triplicates([-4, 7, -4, -4]) == 7
assert single_of_triplicates([7, -4, 7, 7]) == -4
print("single of triplicates:", single_of_triplicates([5, 3, 5, 5]),
      single_of_triplicates([7, -4, 7, 7]))

# without the sign fix, -4 comes back as its 32-bit pattern
def no_sign_fix(nums):
    return sum(1 << b for b in range(32) if sum(x >> b & 1 for x in nums) % 3)
print("without the sign fix:", no_sign_fix([7, -4, 7, 7]), "= 2**32 - 4")
assert no_sign_fix([7, -4, 7, 7]) == 2**32 - 4

L, R = [5, 9, 3], [6, 2]
brute = sum(a ^ c for a in L for c in R)
print("sum of XOR over pairs:", xor_pairs_sum(L, R), "brute force:", brute)
assert xor_pairs_sum(L, R) == brute == 42
```

### C. A bitmask as a set

**What changes:** the integer is no longer a value. Bit i means "element i is in
the set". **Why it works:** a subset of n elements is n yes/no answers, and an
n-bit integer is n yes/no answers. The correspondence is exact: the integers 0 to
2^n - 1 are exactly the subsets.

Derive it from the brute force. The recursive way to list subsets decides
element 0 (in or out), then element 1, and so on: a binary tree of depth n whose
leaves are the subsets. Write each leaf's decisions as bits and the leaves, left
to right, are the numbers 0, 1, 2, ..., 2^n - 1. So the recursion is the same as
counting:

```
for mask in range(1 << n):
    subset = [nums[i] for i in range(n) if mask >> i & 1]
```

[[p:google-subsets|Subsets]] asks for exactly this order. With nums = [1, 2, 3]:
mask 5 = 101 means elements 0 and 2, the subset [1, 3]; mask 6 = 110 is [2, 3].

The operations you need, all one operator each:

| set operation | on masks |
|---|---|
| is i in s | `s >> i & 1` |
| add i | `s \| (1 << i)` |
| remove i | `s & ~(1 << i)` |
| toggle i | `s ^ (1 << i)` |
| union, intersection | `s \| t`, `s & t` |
| disjoint | `s & t == 0` |
| size | `bin(s).count("1")` or `s.bit_count()` |
| every submask of m | `s = m; while s: ...; s = (s - 1) & m` (then visit 0) |

Three disguises in the bank:

- *Letters as a set.*
  [[p:netflix-count-disjoint-character-string-pairs|Count String Pairs With Disjoint Characters]]:
  one 26-bit mask per word, and "share no character" is `ma & mb == 0`.
  [[p:meta-maximum-unique-character-word-subset|Maximum Unique-Character Word Subset]]
  has at most 16 words, so it tries all 2^16 subsets of words, or backtracks with
  the union mask.
- *Parities as a set.*
  [[p:deloitte-lonest-substring-with-even-occurrences|Longest Substring with Even Occurrences]]
  combines A and C: the mask after prefix i has bit c set when letter c has
  appeared an odd number of times so far. A substring between two prefixes with
  the **same** mask has every letter an even number of times. "abba": the prefix
  masks are 0, 1 (a), 3 (ab), 1 (abb), 0 (abba). Mask 0 appears before the start
  and at the end, so the whole string, length 4, qualifies. Store the first index
  of each mask and the answer is the longest gap.
- *Masks as DP states.* Visiting all nodes, assigning tasks to people: the mask
  says which are done. That is [[dp-bitmask]], and it is why `n <= 20` in a
  constraint is practically an instruction.

### D. Counting bits and powers of two

**What changes:** the question is about the bits themselves: how many, which is
lowest, is there only one.

Start from the brute force: test each column, `sum(x >> b & 1 for b in range(32))`.
That is always 32 steps. The waste is in the zero columns, which we test and
ignore. The cure is one fact about subtracting 1:

> For x > 0, x - 1 flips the lowest 1 of x to 0 and every 0 below it to 1.
> Everything above the lowest 1 is unchanged.

<svg viewBox="0 0 560 150" role="img" aria-label="x = 1001100 and x minus one = 1001011 aligned; above the lowest set bit they are identical, at and below it x minus one is the complement, so x AND x minus one clears exactly the lowest set bit">
  <g>
    <text x="10" y="30">x</text>
    <text x="60" y="30">1  0  0  1</text>
    <text class="fill" x="170" y="30">1  0  0</text>
    <text x="10" y="60">x-1</text>
    <text x="60" y="60">1  0  0  1</text>
    <text class="fill" x="170" y="60">0  1  1</text>
    <line x1="162" y1="12" x2="162" y2="72"/>
    <line x1="162" y1="72" x2="250" y2="72"/>
    <text x="166" y="95">complemented: the borrow</text>
    <text x="40" y="95">identical above</text>
    <text x="10" y="128">AND keeps the identical part and clears the rest: x &amp; (x-1) = 1001000</text>
  </g>
</svg>

It is the borrow you learned in school: subtracting 1 from 1001100 borrows from the
lowest 1 and leaves 1001011. AND the two together. Above the lowest 1 they agree,
so those bits survive. At and below it they are complements, so everything there
becomes 0. **`x & (x - 1)` is x with its lowest set bit cleared.** Four consequences:

- **Kernighan's popcount.** `while x: x &= x - 1; count += 1` runs once per set
  bit, not once per column. 44 = 101100 → 101000 → 100000 → 0: three iterations,
  popcount 3.
- **Power of two.** A positive number is a power of two exactly when it has one set
  bit, that is when clearing the lowest leaves nothing: `n > 0 and n & (n - 1) == 0`.
  [[p:arm-power-of-two-check|Power of Two Without Division]]. The `n > 0` is not
  decoration: 0 & -1 = 0, so without it zero passes.
- **The lowest set bit itself.** `x & -x`. In two's complement -x = ~x + 1; the
  +1 ripples through the trailing ones of ~x (the trailing zeros of x) and stops at
  the lowest 1 of x. So -x agrees with x at that bit and below and is the
  complement above it. AND keeps that bit alone. This is the split column of
  Trace 2 and the step of a [[fenwick-tree]].
- **Counting bits for every number at once.**
  [[p:goodscore-counting-bits|Counting Bits]] wants popcounts for 0..n with n up to
  10^6. Do not run Kernighan 10^6 times. Note that i >> 1 is i with its lowest
  column dropped, a smaller number whose count you already know:
  `bits[i] = bits[i >> 1] + (i & 1)`. 0..8: 0 1 1 2 1 2 2 3 1. Check bits[6]:
  6 >> 1 = 3, bits[3] = 2, and 6 is even, so 2.

Two more from the bank, each one sentence once you see the bits:

- [[p:jpmorgan-invert-ad-visibility|Invert Ad Visibility Bits]]: flip only the
  significant bits. `~x` is wrong in Python (it is -x - 1, with infinitely many
  leading ones). The mask of the significant columns is `(1 << x.bit_length()) - 1`,
  so the answer is `x ^ ((1 << x.bit_length()) - 1)`. 30 = 11110 becomes 00001 = 1.
- [[p:uber-minimum-operations-to-reduce-to-zero|Minimum Operations To Reduce To Zero]]:
  add or subtract any power of two. An isolated 1 costs one subtraction. A run of
  two or more 1s is cheaper to round up: 0111 + 0001 = 1000, one operation, and
  the run became a single 1 one column higher. 6 = 110 costs 2, 21 = 10101 costs 3,
  7 = 111 costs 2 (8 - 1). It is rated stretch for a reason: the proof that this
  greedy is optimal takes care.

```python run
def popcount_kernighan(x):
    assert x >= 0
    steps = []
    while x:
        steps.append(format(x, "b"))
        x &= x - 1
    return len(steps), steps

def count_bits(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits

def is_pow2(n):
    return n > 0 and n & (n - 1) == 0

c, steps = popcount_kernighan(44)
print("44:", " -> ".join(steps), "-> 0  (%d iterations)" % c)
assert c == 3
print("count_bits(8):", count_bits(8))
assert count_bits(8) == [0, 1, 1, 2, 1, 2, 2, 3, 1]
assert all(count_bits(4096)[i] == bin(i).count("1") for i in range(4097))
assert [k for k in range(-4, 70) if is_pow2(k)] == [1, 2, 4, 8, 16, 32, 64]
assert (0 & (0 - 1)) == 0              # why the n > 0 guard is needed
for x in (12, 44, 96, 7):
    print("x=%3d  x & -x = %2d   x & (x-1) = %3d" % (x, x & -x, x & (x - 1)))
    assert (x & -x) | (x & (x - 1)) == x and (x & -x) & (x & (x - 1)) == 0
x = 30
print("invert significant bits of 30:", x ^ ((1 << x.bit_length()) - 1), " ~30 =", ~x)
assert x ^ ((1 << x.bit_length()) - 1) == 1 and ~x == -31
```

### E. Greedy from the top bit

**What changes:** you choose bits to maximise (or minimise) a result. **Why it
works:** 2^b is larger than all lower powers together, 2^b - 1, so getting column
b right matters more than every column below it. Decide the highest column first
and never revisit it. [[p:ibm-find-y-value|Find Y Value]] spends a limited budget
of set bits on the highest columns where x has zeros. Maximum-XOR-pair problems use
the same greedy with a [[trie]] over the bits, so that "is there a number whose
bit b is the opposite of mine" is one step down the trie. Rare in OAs, common in
contests.

### F. Fixed-width surgery (rare)

Some problems are about hardware words: swap even and odd bits, extract a register
field, check endianness, build a CIDR mask. Here the bits are the specification,
not a trick. The rules: decide the width, build masks like `0x55555555` (the even
columns) and `0xAAAAAAAA` (the odd ones), shift, and AND with `0xFFFFFFFF` at the
end, because Python's `<<` never drops bits that a 32-bit register would. Rare
outside hardware companies, and pure mechanics once the width is fixed.

### G. gcd and lcm: Euclid, derived

**The summary:** what two numbers have in common. **The problem:**
[[p:jpmorgan-greatest-common-divisor|Greatest Common Divisor]], two numbers up to
10^9.

*Brute force:* try every d from min(a, b) down to 1 and return the first that
divides both. For 48 and 18 that tries 18, 17, ..., 6: thirteen tries. For two
numbers near 10^9 that are coprime it tries 10^9 of them. Too slow.

*Notice the waste.* We test d against a and b separately, as if a and b had
nothing to do with each other. But if d divides a and d divides b, then d divides
a - b. And the other way: if d divides a - b and b, it divides a = (a - b) + b. So
**a and b have exactly the same common divisors as a - b and b.** The pair got
smaller and the answer did not change. That is the unlocking question again: the
answer depends only on the set of common divisors, and that set survives
replacing a by a - b.

*Subtract repeatedly:* gcd(48, 18) = gcd(30, 18) = gcd(12, 18). Subtracting 18
until the result drops below 18 is the same as taking the remainder, 48 mod 18 =
12. So **gcd(a, b) = gcd(b, a mod b)**, and gcd(a, 0) = a because every number
divides 0.

```
gcd(252, 105):  252 mod 105 = 42   ->  gcd(105, 42)
                105 mod 42  = 21   ->  gcd(42, 21)
                42  mod 21  = 0    ->  gcd(21, 0) = 21
```

*Cost.* After two steps the larger number at least halves: if b <= a/2, then
a mod b < b <= a/2; if b > a/2, then a mod b = a - b < a/2. So at most about
2 · log2(10^9), roughly 60 steps, instead of 10^9.

*You might think lcm(a, b) = a · b.* lcm(4, 6) is 12, not 24. a · b counts the
common part twice. Since a · b = gcd · lcm (each prime's exponents: min plus max
equals the sum), **lcm(a, b) = a // gcd(a, b) * b**. Divide first: in a language
with fixed-width integers, a · b overflows long before the lcm does.

*Disguises.* [[p:atlassian-greatest-common-divisor-of-strings|Greatest Common Divisor of Strings]]:
a common "divisor string" exists only if s1 + s2 == s2 + s1, and then its length
is gcd(len(s1), len(s2)); Euclid's subtraction step works on strings too.
[[p:zscaler-sum-divisors-of-array-gcd|Sum of Divisors of the Array GCD]]: the gcd of
an array is the gcd folded left to right, gcd(gcd(a, b), c), and the divisors of
one number up to 10^9 are found in pairs (d, g/d) for d up to sqrt(g).

### H. Modular arithmetic: keep the remainder

**The summary:** the remainder mod m. **The problem:**
[[p:ibm-drawing-edge|Drawing Edge]]: the number of simple graphs on n labelled
vertices, modulo 10^9 + 7, for n up to 10^9. Each of the n(n-1)/2 possible edges is
in or out, so the answer is 2^(n(n-1)/2). The exponent is about 5·10^17.

*Brute force:* compute 2^e and then take the remainder. 2^(5·10^17) has 5·10^17
bits. No computer holds it.

*Notice the waste:* we only need the remainder, and the remainder of a product
depends only on the remainders of the factors: (a · b) mod m = ((a mod m) ·
(b mod m)) mod m. The same holds for + and -. So reduce after every operation and
no number ever exceeds m^2. That is what "modulo 10^9 + 7" in a statement is
telling you to do.

*Second waste:* even reduced, multiplying by 2 e times is 5·10^17 steps. But
2^13 = 2^8 · 2^4 · 2^1, because 13 = 1101 in binary. Square the base repeatedly
(2, 2^2, 2^4, 2^8, ...) and multiply in the squares where the exponent has a 1
bit. That is O(log e) multiplications, about 60 here. Bits again: **fast
exponentiation reads the exponent's binary digits.** Hand trace, 3^13 mod 7:
3^1 = 3, 3^2 = 9 ≡ 2, 3^4 ≡ 2^2 = 4, 3^8 ≡ 4^2 = 16 ≡ 2; 13 = 8 + 4 + 1, so the
answer is 2 · 4 · 3 = 24 ≡ 3. Python's `pow(b, e, m)` does exactly this. Full
treatment in [[fast-exponentiation]].

*You might think you can divide.* (12 / 4) mod 7 = 3. But 12 mod 7 = 5 and
4 mod 7 = 4, and 5 / 4 is not an integer. Division does not survive reduction.
What survives is multiplying by an **inverse**: a number y with 4 · y ≡ 1 (mod 7).
y = 2, since 8 ≡ 1. Then 5 · 2 = 10 ≡ 3. Correct. When m is prime and a is not a
multiple of m, Fermat's little theorem gives a^(m-1) ≡ 1, so the inverse is
a^(m-2) mod m, one `pow` call. This is why the modulus is almost always the prime
10^9 + 7. [[p:expedia-product-except-self-modulo|Product Except Self Modulo 1000000007]]
forbids division and allows zeros, and zeros have no inverse at all, so prefix
and suffix products are the honest solution there.

*You might think you can reduce the exponent mod m.* 2^7 mod 7 = 128 mod 7 = 2.
Reducing 7 mod 7 gives 2^0 = 1. Wrong. Exponents live in a different world: by
Fermat, they may be reduced mod m - 1 (when the base is not a multiple of m):
7 mod 6 = 1, and 2^1 = 2. Correct. In Python you rarely need this, because
`pow(2, e, m)` takes a huge e directly.

*Remainders as buckets.* [[p:get-discount-pairs|Get Discount Pairs]]: count pairs
whose sum is divisible by x. Whether a + b is divisible by x depends only on
a mod x and b mod x, so bucket the prices by remainder and pair bucket r with
bucket (x - r) mod x. Prices [31, 25, 85, 29, 35] with x = 60 have remainders
31, 25, 25, 29, 35. Pairs: 31 with 29, and each 25 with 35: three. Careful with
r = 0 (and r = x/2 when x is even): those buckets pair with themselves, c · (c-1)/2.

*Negative remainders.* In Python `-3 % 7 == 4`, always in [0, m). In C, C++ and
Java it is -3. When you subtract mod m in those languages, write
`((a - b) % m + m) % m`.

### I. Primes and the sieve

**The summary:** the smallest prime factor of every number up to N. **The
problem:** [[p:microsoft-primes-less-than-n|Find All Primes Less Than N]], N up to
5·10^6.

*Brute force 1:* test each k by trying every divisor 2..k-1. That is about N^2/2
steps. 10^13.

*Notice the first waste:* divisors come in pairs, d and k/d, and one of them is at
most sqrt(k). So if k has no divisor in 2..sqrt(k), it has none at all. Test
`d * d <= k`. Now N · sqrt(N), about 10^10 for N = 5·10^6. Still too slow, but fine
for one number: [[p:microsoft-sum-distinct-prime-divisors|Sum of Distinct Prime Divisors]]
factors one n up to 10^12 by trial division up to 10^6.

*Notice the second waste:* trial division asks each number "who divides you?"
independently, and the same divisor 3 is tried against every number. Turn it
around: each prime p **announces** its multiples. Start with every number marked
prime. Take the smallest unmarked number p; it is prime, because nothing smaller
divides it. Cross out 2p, 3p, 4p, ... The next unmarked number is the next prime.
That is the sieve of Eratosthenes.

*Start at p · p.* Any multiple k · p with k < p has a prime factor smaller than p
(a factor of k), so a smaller prime already crossed it out. So crossing starts at
p^2, and once p^2 > N there is nothing left to cross. Hand trace up to 30:

| p | crosses out (starting at p^2) |
|---|---|
| 2 | 4 6 8 10 12 14 16 18 20 22 24 26 28 30 |
| 3 | 9 15 21 27 (12, 18, 24, 30 already gone) |
| 5 | 25 (30 already gone) |
| 7 | 49 > 30: stop |

Left: 2 3 5 7 11 13 17 19 23 29.

*Cost.* Prime p crosses about N/p numbers, and the sum of 1/p over primes up to N
grows like log log N, so the total is O(N log log N): for N = 5·10^6, a few times
N. Space: one flag per number.

*The smallest-prime-factor sieve.* Store, instead of a flag, the first prime that
crossed each number out. Then any k <= N factors in O(log k) steps: divide by
spf[k], repeat. [[p:maven-securities-prime-factor-visitation|Prime Factor Visitation]]
needs the distinct prime factors of 10^5 values, which is this. It also uses
variation A: flipping the bulbs of the same prime twice cancels, so only the
parity of each prime's count matters.
[[p:microsoft-maximum-score-with-prime-jumps|Maximum Score with Prime Jumps]] uses
the sieve only to list the allowed jump lengths, then a DP does the real work.

*You might think 1 is prime.* It is not: a prime has exactly two divisors. The
sieve must mark 0 and 1 as not prime by hand.
[[p:adobe-numbers-with-exactly-three-divisors|Numbers with Exactly Three Divisors]]
is a nice disguise: exactly three divisors means p^2 for a prime p (divisors 1, p,
p^2), so the test is "is it a perfect square of a prime", and a sieve up to
sqrt(10^9), about 31,623, answers it.

```python run
def gcd_brute(a, b):
    for d in range(min(a, b), 0, -1):
        if a % d == 0 and b % d == 0:
            return d

def gcd(a, b, trace=False):
    while b:
        if trace:
            print("   gcd(%d, %d): %d mod %d = %d" % (a, b, a, b, a % b))
        a, b = b, a % b
    return a

def sieve(n):                         # flags for 0..n inclusive
    is_p = [False, False] + [True] * (n - 1)
    p = 2
    while p * p <= n:
        if is_p[p]:
            for k in range(p * p, n + 1, p):
                is_p[k] = False
        p += 1
    return [k for k in range(n + 1) if is_p[k]]

print("Euclid on 252, 105")
assert gcd(252, 105, trace=True) == 21 == gcd_brute(252, 105)
assert all(gcd(a, b) == gcd_brute(a, b) for a in range(1, 60) for b in range(1, 60))
lcm = lambda a, b: a // gcd(a, b) * b
assert lcm(4, 6) == 12 != 4 * 6
print("primes up to 30:", sieve(30))
assert sieve(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
trial = lambda k: k > 1 and all(k % d for d in range(2, int(k ** 0.5) + 1))
assert sieve(2000) == [k for k in range(2001) if trial(k)]

M = 10**9 + 7
assert pow(3, 13, 7) == 3 and pow(2, 6, M) == 64        # 3^13 mod 7; Drawing Edge with n = 4
inv4 = pow(4, 7 - 2, 7)                                  # Fermat inverse mod 7
print("12/4 mod 7 via the inverse of 4:", (12 % 7) * inv4 % 7, " inverse =", inv4)
assert inv4 == 2 and (12 % 7) * inv4 % 7 == (12 // 4) % 7
assert pow(2, 7 % 6, 7) == pow(2, 7, 7) != pow(2, 7 % 7, 7)  # exponents reduce mod m-1
n = 10**9
e = n * (n - 1) // 2
assert pow(2, e, M) == pow(2, e % (M - 1), M)
print("Drawing Edge, n = 10^9:", pow(2, e, M))
```

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"Every element appears twice except", "exactly one is missing", "appears an
   odd number of times", "every letter an even number of times".** Parity. XOR, or a
   parity mask. Very reliable.
2. **The words XOR, AND, OR, "bitwise", "set bits", "binary representation" in the
   statement.** The problem cares about bits. Then ask whether the operator works
   per column, and if it does, think one column at a time.
3. **A tiny n next to "subset", "choose any", "visit all", "assign each".** n <= 20
   means 2^n masks. n <= 16 next to "for every subset, every sub-subset" means 3^n.
   The constraint is the algorithm.
4. **"Modulo 10^9 + 7", "the answer may be large".** Reduce after every operation.
   If you need to divide, you need an inverse.
5. **"Divisible by", "remainder", "last digit", "every k-th".** Bucket by remainder.
6. **"Prime", "factor", "divisors", with many values up to 10^5 or 10^6.** A sieve,
   probably the smallest-prime-factor version. With one value up to 10^12, trial
   division to the square root.
7. **"Repeat", "tile", "period", "both divide", "common length".** gcd and lcm.
8. **"Power of two", "add or subtract 2^i", "doubling".** Read the binary form.
   (But see the anti-signal: "power of two" in a constraint is just a size.)
9. **Width words: "unsigned 32-bit", "byte", "nibble", "register", "mask", "CIDR".**
   Fixed-width surgery.

### Disguises

- **"Count subarrays whose XOR is k".** Prefix XOR plus a dictionary, because
  XOR(l..r) = P[r+1] ^ P[l]. Exactly the prefix-sum trick.
- **"Longest substring where every vowel appears an even number of times".** A
  parity mask over the vowels, then "longest gap between equal masks".
- **"Minimum tokens after exchanging two on stack i for one on stack i+1".**
  [[p:microsoft-minimum-tokens-remaining|Minimum Tokens Remaining]]: the exchange
  keeps the total value Σ A[i] · 2^i fixed, and the fewest powers of two that sum to
  a number is its popcount. One invariant, one popcount.
- **"Sort by number of ones, then by value".**
  [[p:oracle-cardinality-sort|Cardinality Sorting]]: a popcount as the sort key.
- **"Number of graphs, strings, colourings: each of k independent choices is
  yes/no".** 2^k mod p. Fast exponentiation.

### Anti-signals: looks like this chapter, is not

- **"Subset" with n = 10^5.** No mask exists. That is [[dynamic-programming]] or
  [[greedy]].
- **"Shift" of an array.** "Minimum right shifts to sort" shifts positions, not bits.
- **Sums of values.** "Sum of a + b over all pairs" is algebra (|R| · ΣL + |L| · ΣR),
  not columns, because of carries.
- **"Optimise with bit tricks".** Replacing `% 2` with `& 1` changes nothing a
  compiler had not already done. If the bits are not changing the complexity, they
  are not the answer.

## Traps

**XOR on a broken promise.** The input has a value three times, or two singles,
and the code returns a mix. Symptom: a plausible-looking wrong number, never an
error. Fix: re-read the multiplicities, and use variation B or Trace 2.

**Splitting on a fixed column.** Shown above: `x & 1` instead of `diff & -diff`.
Symptom: correct whenever one single is odd and one is even, `[a ^ b, 0]` otherwise.

**`~x` as "flip the bits".** In Python it is -x - 1. Symptom: a negative answer
where a positive one was expected. Fix: XOR with a mask of the width you mean.

**Popcount of a negative.** `bin(-5).count("1")` is 2 (it counts the magnitude),
and Kernighan's loop on a negative never ends in Python. Symptom: a hang, or a
wrong count on negative inputs only. Fix: `x & 0xFFFFFFFF` first, if 32 bits is
what you mean.

**The square root boundary.** Trial division with `d * d < k` instead of
`d * d <= k`, or a sieve whose outer loop stops at `p * p < n` when the array goes
up to n inclusive. Symptom: exactly the squares of primes, 4, 9, 25, 49, are reported
prime. The block below shows it.

**Dividing under a modulus.** `(a // b) % m` after a and b were already reduced.
Symptom: right on small tests (nothing was reduced yet), wrong on large ones.
Fix: multiply by `pow(b, m - 2, m)`, and only when m is prime and b mod m is not 0.

**Reducing an exponent mod m.** It must be mod m - 1 (Fermat), and only when the
base is coprime to m. Or let `pow` take the full exponent.

**lcm by multiplication.** `a * b // gcd(a, b)` is right in Python but overflows
in 64 bits for a, b near 10^10. Write `a // gcd(a, b) * b`.

**Precedence outside Python.** `x & 1 == 0` means `(x & 1) == 0` in Python and
`x & (1 == 0)` in C, C++ and Java, which is always 0. Parenthesise.

**`1 << 31` in Java or C.** Overflows a signed 32-bit int. Use `1L << 31`.
Shifting by 32 or more is undefined in C and taken mod 32 in Java.

```python run
import math

def is_prime_wrong(k):
    if k < 2:
        return False
    d = 2
    while d * d < k:                  # the bug: stops before testing d = sqrt(k)
        if k % d == 0:
            return False
        d += 1
    return True

def is_prime_right(k):
    if k < 2:
        return False
    d = 2
    while d * d <= k:
        if k % d == 0:
            return False
        d += 1
    return True

bad = [k for k in range(2, 60) if is_prime_wrong(k) != is_prime_right(k)]
print("numbers the '<' version calls prime by mistake:", bad)
print("trace of the wrong version on 9: d=2, 2*2=4 < 9, 9 % 2 = 1; d=3, 3*3=9 < 9 is false, stop -> 'prime'")
assert bad == [4, 9, 25, 49]                     # exactly the squares of primes
assert all(math.isqrt(k) ** 2 == k for k in bad)

# ~x is not "flip the significant bits"
x = 156
print("~156 =", ~x, "  156 ^ 255 =", x ^ ((1 << x.bit_length()) - 1))
assert ~x == -157 and x ^ 255 == 99

# a popcount that forgets the width
print("bin(-5).count('1') =", bin(-5).count("1"), "  as 32 bits:", bin(-5 & 0xFFFFFFFF).count("1"))
assert bin(-5).count("1") == 2 and bin(-5 & 0xFFFFFFFF).count("1") == 31

# dividing after reducing
m = 7
a, b = 12, 4
wrong = (a % m) // (b % m)
right = (a % m) * pow(b, m - 2, m) % m
print("(12/4) mod 7: reduce-then-divide gives", wrong, " inverse gives", right, " truth", (a // b) % m)
assert wrong != (a // b) % m and right == (a // b) % m
```

## What to memorise

**The sentence.** Ask what the smallest summary of the input is that the answer
depends on, and keep only that: a parity per column (XOR), membership (a mask),
a remainder (mod), a common part (gcd), a smallest factor (sieve).

**The two templates.**

```
acc = 0
for x in nums: acc ^= x            # pairs cancel; acc is the odd one out

low = diff & -diff                 # a column where the two singles differ
```

**The identities**, all from one fact (x - 1 flips the lowest 1 and the zeros
below it): `x & (x - 1)` clears the lowest set bit; `x & -x` isolates it;
`n > 0 and n & (n - 1) == 0` is a power of two; `bits[i] = bits[i >> 1] + (i & 1)`.

**The maths core.** `gcd(a, b) = gcd(b, a % b)`; `lcm = a // gcd * b`; reduce mod m
after every + - *; divide by multiplying with `pow(b, m - 2, m)` for prime m; sieve
from p * p while `p * p <= n`.

**The one habit.** Say the width before you write a bit operation: "30 columns",
"signed 32-bit", "26 letters", "n <= 20". The bugs in this chapter (`~x`, negative
popcount, `1 << 31`, the sign of a rebuilt number) are all one bug: a width nobody
chose.

**Numbers to carry.** 2^10 ≈ 10^3, 2^20 ≈ 10^6, 2^30 ≈ 10^9; 3^16 ≈ 4·10^7;
Euclid takes about 2 log2 of the smaller number; the sieve up to 10^7 is fine.

## Check yourself

:::check
Trace `acc ^= x` by hand on `[7, 3, 5, 3, 7]`. Write acc in binary after every
step, and say in words what happens to each column at the step where the second 3
arrives.
--
| step | x | binary | acc after |
|---|---|---|---|
| 1 | 7 | 111 | 111 |
| 2 | 3 | 011 | 100 |
| 3 | 5 | 101 | 001 |
| 4 | 3 | 011 | 010 |
| 5 | 7 | 111 | 101 |

Final 101 = 5, the single value. At step 4 the accumulator is 001 and the new
number is 011. Column 0: it had seen ones from 7, 3 and 5, three of them (odd,
bit 1); the second 3 brings a fourth, so it goes even, bit 0. Column 1: it had seen
ones from 7 and 3, two (even, bit 0); the second 3 makes three, odd, bit 1.
Column 2: the 3 has a 0 there, so nothing changes, bit 0. 001 becomes 010. Note
that 010 = 2 is not in the array: mid-pass, acc is a running XOR, not a value.
:::

:::check
Find the two singles in `[4, 9, 4, 6, 1, 1]` by hand: compute the XOR of everything,
its lowest set bit, the two groups and their XORs. Then do it again splitting on
column 0 and say whether it works and why.
--
The pairs (4, 4) and (1, 1) cancel, so the XOR is 9 ^ 6: 1001 ^ 0110 = 1111 = 15.
Its lowest set bit is 1 (column 0). Split by column 0: odd numbers 9, 1, 1 give
9 ^ 1 ^ 1 = 9; even numbers 4, 4, 6 give 6. Answer [6, 9].

Splitting on column 0 is therefore the same split here, and it works, because 9 is
odd and 6 is even, so they disagree in column 0. This is exactly why the buggy
"odd versus even" version passes some tests. With `[1, 2, 1, 3, 2, 5]` the singles
3 and 5 are both odd, column 0 is not a column where they differ (3 ^ 5 = 110 has a
0 there), and the split puts both into one group.
:::

:::check
Someone says: "To find the repeated number in an array, XOR all the elements; the
duplicates cancel and you are left with it." Where are they wrong, and how does
*Missing and Repeated Number* actually use XOR?
--
Duplicates cancel, so XOR removes the repeated value instead of finding it. What is
left is the XOR of the values with odd multiplicity. In `[1, 2, 4, 4]` that is
1 ^ 2 = 3, a number that is not even in the array.

To find a repeated value r with XOR you need r to be the odd one out. *Missing and
Repeated Number* has values from 1 to n with r twice and m missing. XOR the array
with 1, 2, ..., n: now r appears three times, m once, and every other value twice.
The result is r ^ m. That is the two-singles problem: split on a set bit of r ^ m,
XOR each group (array elements and 1..n together), and get r and m in some order;
one more pass over the array tells which one is present, and that one is r.
:::

:::check
Fill in the sieve of Eratosthenes up to 50 by hand: for each prime p you use, list
the first number you cross out and say why you can start there. When do you stop,
and why is it safe to stop?
--
p = 2: start at 4 and cross 4, 6, ..., 50. p = 3: start at 9 (6 was crossed by 2),
cross 9, 15, 21, 27, 33, 39, 45 that are not already gone. p = 5: start at 25
(10, 15, 20 already gone, each has a factor 2 or 3), cross 25, 35. p = 7: start at
49 (14, 21, 28, 35, 42 already gone), cross 49. Next candidate p = 11: 121 > 50, stop.

Starting at p^2 is safe because any k · p with k < p has a prime factor of k smaller
than p, which already crossed it out. Stopping when p^2 > N is safe for the same
reason: every composite c <= N has a prime factor at most sqrt(c) <= sqrt(N), so it
was crossed out by a prime we already used.

The primes up to 50: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 (fifteen of them).
Note that 49 = 7^2 is only removed because the loop runs while p · p <= 50; a loop
written `p * p < 49` for N = 49 would wrongly keep 49.
:::

:::check
Run Euclid by hand on gcd(1071, 462), then give lcm(1071, 462). Why does each step
not change the answer?
--
1071 mod 462 = 147 (1071 = 2 · 462 + 147). 462 mod 147 = 21 (462 = 3 · 147 + 21).
147 mod 21 = 0. So gcd = 21.

lcm = 1071 // 21 · 462 = 51 · 462 = 23,562.

Each step replaces (a, b) with (b, a mod b). Every common divisor d of a and b
divides a - q·b = a mod b, so it is a common divisor of b and a mod b. And every
common divisor of b and a mod b divides a = q·b + (a mod b). So the two pairs have
exactly the same set of common divisors, and in particular the same greatest one.
:::

:::check
Derive the cost of "for every mask over n items, loop over all of its submasks", and
say what it means for the largest n you can afford.
--
A mask with k set bits has 2^k submasks, since each of its bits is independently in
or out. There are C(n, k) masks with k bits. So the total is the sum over k of
C(n, k) · 2^k, which by the binomial theorem is (1 + 2)^n = 3^n.

A shorter way to see it: for each item there are three possibilities, in neither
the mask nor the submask, in the mask only, or in both. Independently for n items:
3^n pairs.

3^16 ≈ 4.3·10^7 is comfortable; 3^20 ≈ 3.5·10^9 is not. Iterating only masks and
single bits is 2^n · n, fine at n = 20. A submask DP lives around n <= 16. Confusing
the two is the usual reason a bitmask solution times out.
:::

:::check
Disguised problem: given a string of lowercase letters, find the longest substring
in which every letter appears an even number of times. Reduce it to this chapter,
then run your method by hand on "xyyxzz".
--
Keep a 26-bit mask: bit c is the parity of letter c in the prefix so far (variation
C used as variation A). The substring s[i..j-1] has every letter even exactly when
the prefix masks at i and j are equal, because XOR-ing the two prefixes cancels the
common part and leaves the parities of the substring, which must all be 0. So
record the first index where each mask appears, and for every later index with the
same mask, the gap is a candidate.

With x = bit 0, y = bit 1, z = bit 2, the prefix masks of "xyyxzz" at positions
0..6 are: 0, 1 (x), 3 (xy), 1 (xyy), 0 (xyyx), 4 (xyyxz), 0 (xyyxzz). Mask 0 first
appears at position 0 and appears again at 6: length 6, the whole string. Mask 1
appears at 1 and 3: "yy", length 2. The answer is 6. That is
*Longest Substring with Even Occurrences*, O(n) time with a dictionary of at most
2^26 masks, in practice at most n + 1.
:::
