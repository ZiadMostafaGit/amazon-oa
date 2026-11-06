# Hash Tables

> A hash table turns "search for it" into "compute where it would be", so any inner loop that is secretly asking "have I seen this exact thing before?" collapses into one step, and the whole skill is noticing that question and naming the key it is asked about.

## The problem it solves

Here is the problem that teaches it, [[p:vanguard-two-sum|Two Sum]]:

> Given nums and a target, return the two different indices whose values add up
> to the target. Exactly one such pair exists. Return the smaller index first.

For nums = [4, 1, 7, 6] and target 10 the answer is [0, 3], because 4 + 6 = 10.

Everyone's first solution is the double loop. For every position j, look at every
earlier position i and ask whether nums[i] + nums[j] equals the target.

```python
for j in range(len(nums)):
    for i in range(j):
        if nums[i] + nums[j] == target:
            return [i, j]
```

It is correct, and for four numbers it is instant. Count it, though. Position j
looks at j earlier positions, so the total is 0 + 1 + 2 + ... + (n-1) =
n(n-1)/2 checks in the worst case, when the pair sits at the very end. The bank's
limit for this problem is n = 10^5. That is about 5 x 10^9 checks, and Python does
roughly 10^7 simple steps a second. Eight minutes, against a time limit of a
second or two.

The second solution people reach for is to sort and walk two pointers inward. That
is a real technique ([[two-pointers]]), and it runs in O(n log n). But sorting moves
the values away from their indices, and this problem wants indices back. You can
repair that by sorting (value, index) pairs, and it works. What it does not do is
answer the question this chapter is about: why is the double loop slow, and what
is the smallest change that makes it fast?

The answer will be a dictionary, and you already know how to use one. The point
of this chapter is different. It is to see *why* the dictionary is the cure, to
see what it is made of so that its costs and failures stop being mysterious, and
to learn the half-dozen shapes in which the same cure appears: a set of what you
have seen, a map from value to index, a frequency count, a canonical key that
groups things, buckets indexed by a count, and the array itself used as the
table. The roadmap node for this chapter is exactly that list, and every item on
it gets a section below.

This topic is the third most used in the bank: 1,993 problems touch a hash table.
That is not because hashing is hard. It is because "have I seen this before?" is
the most common question an algorithm asks.

### When it is the wrong tool

A hash table remembers *what* it has seen and nothing about *order*. So it is the
wrong tool when order is the point.

- **You need the smallest, the k-th, the next larger, or everything in a range.**
  A hash table scatters keys on purpose and has thrown that information away. Sort
  ([[sorting]]) or keep an ordered structure ([[ordered-set]], [[balanced-bst]]).
- **The keys are a small dense range.** If every key is a lowercase letter or an
  integer in 0..n-1, a plain list indexed by the key is a hash table with a
  perfect hash and no collisions. It is faster and cannot go wrong. Variation F
  below turns this into a technique.
- **The input is already sorted.** Duplicates are then adjacent, and pairs with a
  given sum can be found with two pointers in O(1) extra space. A set would be
  correct and wasteful.
- **You need prefixes, not whole keys.** "Every word starting with ca" is a
  [[trie]]. A hash table only answers questions about exact keys.
- **You need a worst-case guarantee per operation.** A hash table is fast on
  average and Θ(n) per operation in the worst case. When a hard bound is
  required, you need a balanced tree.

One look-alike is *not* an exception. "Count the subarrays with sum k" is about
contiguous pieces, which sounds like order. But the standard solution is a hash
table whose key is a prefix sum ([[prefix-sums]]): the order lives in the scan,
and the table only answers "how many earlier prefixes had this exact value?" The
same split, scan for order and table for identity, runs through the whole chapter.

## Build it from the brute force

We will start from the double loop and change one thing at a time. The hash table
will appear as the answer to a specific complaint about the loop, not as a thing
you were told to use.

### Step 1: write the slow version and count it

The double loop above checks n(n-1)/2 pairs. For n = 2,000 that is 1,999,000
checks; for n = 10^5 it is about five billion. Doubling n quadruples the work.
This is the number we want to make smaller.

### Step 2: look at what the inner loop is doing

Fix one value of j and read the inner loop as a sentence. With j = 3 and
nums[3] = 6, it says: "Look at 4, then 1, then 7. Is any of them equal to
10 - 6 = 4?" The inner loop is not really looking at *pairs*. It is looking for
one specific number, the **complement** target - nums[j], among the numbers to
the left.

Now look at all the rows of work together, on [4, 1, 7, 6] with target 10:

<svg viewBox="0 0 640 230" role="img" aria-label="the inner loop of the brute force for nums 4, 1, 7, 6: row j=1 scans 4, row j=2 scans 4 and 1, row j=3 scans 4, 1 and 7; shaded cells were already read by an earlier row">
  <g>
    <text x="20" y="30">j</text>
    <text x="70" y="30">looking for</text>
    <text x="250" y="30">cells the inner loop reads</text>
    <text x="20" y="75">1</text>
    <text x="70" y="75">10 - 1 = 9</text>
    <rect x="250" y="52" width="60" height="36"/>
    <text x="280" y="76" text-anchor="middle">4</text>
    <text x="20" y="125">2</text>
    <text x="70" y="125">10 - 7 = 3</text>
    <rect class="fill" x="250" y="102" width="60" height="36"/>
    <text x="280" y="126" text-anchor="middle">4</text>
    <rect x="310" y="102" width="60" height="36"/>
    <text x="340" y="126" text-anchor="middle">1</text>
    <text x="20" y="175">3</text>
    <text x="70" y="175">10 - 6 = 4</text>
    <rect class="fill" x="250" y="152" width="60" height="36"/>
    <text x="280" y="176" text-anchor="middle">4</text>
    <rect class="fill" x="310" y="152" width="60" height="36"/>
    <text x="340" y="176" text-anchor="middle">1</text>
    <rect x="370" y="152" width="60" height="36"/>
    <text x="400" y="176" text-anchor="middle">7</text>
    <text x="450" y="176">found 4</text>
    <text x="20" y="218">Shaded: read again. Each row rereads everything the rows above it read.</text>
  </g>
</svg>

The shaded cells are the waste. Row 2 rereads the 4 that row 1 already read. Row 3
rereads the 4 and the 1. Each row asks a different question ("is 9 there?", "is 3
there?", "is 4 there?"), but every question is about the *same growing pile* of
numbers, and every row answers it by reading the whole pile from the start. With n
numbers, the last row reads n-1 cells to answer a yes-or-no question about one
value.

### The question that unlocks it

So here is the question to ask of every slow loop in this family:

**What is the inner loop searching for, and could I look it up by name instead of
searching for it?**

For Two Sum the inner loop searches for the value target - nums[j] among the
values already passed. If we kept those values in a structure that answers "is
the value v in here, and at which index?" in one step, the inner loop would
disappear. Each position would do one lookup and one insertion, and the total
would be about n steps instead of n²/2.

Say it a second way. The brute force treats the past as a list that must be
reread. The fix treats the past as a *lookup table* keyed by the thing you will
ask about. You are not making the search faster. You are arranging things so
that there is no search.

### You might think: "I will remember the past in a list, then check `need in seen`."

This is the most common first attempt, and it does not change the speed at all.

```python
seen = []
for j, x in enumerate(nums):
    if target - x in seen:      # looks like one step
        ...
    seen.append(x)
```

`in` on a Python list compares against every element until it finds a match. It is
the inner loop, written as one word. On the worst case below, the list version
makes exactly as many comparisons as the double loop: 1,999,000 for n = 2,000.
The structure holding the past has to be one where "is v in here?" does *not*
look at every element. A list cannot do that, because the only way to know what
is in a list is to read it.

### Step 3: the smallest structure that answers "is v here?" in one step

Suppose for a moment that every value is a small non-negative integer, say below
1,000. Then the answer is an array of booleans, `present = [False] * 1000`, and
"is v here?" is `present[v]`. One step, no search. The value *is* the address.
This is called **direct addressing**, and it is worth remembering on its own,
because when the values really are small it is the best possible table
(variation F uses it).

It fails when values are large. The constraints say values go up to 10^9 in
absolute value. An array with two billion slots, for a hundred thousand numbers,
is not going to be allocated.

The repair is to fold the huge range of possible values into a small array. Pick
a table size m, a bit bigger than the number of things you will store, and send
value v to slot **h(v) mod m**, where h is some function that turns a value into
an integer (for small integers, h(v) = v is fine). This slot is the key's
**home**. To find a key, compute its home and look there. You still never search
the whole table.

### You might think: "If m is big enough, two keys never share a home."

They do, and not by bad luck. There are 2 x 10^9 possible values and m slots with m
around 10^5. By the pigeonhole principle, enormous numbers of possible values
share every slot. Whether two of the values *you actually store* collide depends
on your data, and with n keys in m slots collisions start as soon as n is around
the square root of m (the birthday paradox: 23 people in 365 days already give
even odds of a shared birthday). So a hash table must have a plan for two keys
with the same home. The plan is the data structure.

The simplest plan is **chaining**. Each slot holds a short list, its *chain*, of
every stored key whose home is that slot. To look up v, compute its home and scan
that one chain. If the table is about as big as the number of keys, chains are
very short on average, usually zero, one or two entries, so the scan costs a
constant.

Here is the schematic, and right after it the same thing with real numbers.

<svg viewBox="0 0 640 200" role="img" aria-label="schematic of a hash table: a key goes through h of key mod m to a slot index; the slot holds a chain of the keys that share that home">
  <g>
    <rect x="20" y="70" width="80" height="40" rx="6"/>
    <text x="60" y="95" text-anchor="middle">key</text>
    <line x1="100" y1="90" x2="160" y2="90"/>
    <rect class="fill" x="160" y="70" width="140" height="40" rx="6"/>
    <text x="230" y="95" text-anchor="middle">h(key) mod m</text>
    <line x1="300" y1="90" x2="360" y2="90"/>
    <text x="330" y="80" text-anchor="middle">slot</text>
    <rect x="360" y="20" width="50" height="34"/>
    <rect x="360" y="54" width="50" height="34"/>
    <rect x="360" y="88" width="50" height="34"/>
    <rect x="360" y="122" width="50" height="34"/>
    <line x1="410" y1="105" x2="450" y2="105"/>
    <rect x="450" y="90" width="60" height="30" rx="4"/>
    <text x="480" y="110" text-anchor="middle">k1</text>
    <line x1="510" y1="105" x2="540" y2="105"/>
    <rect x="540" y="90" width="60" height="30" rx="4"/>
    <text x="570" y="110" text-anchor="middle">k2</text>
    <text x="20" y="185">compute the slot, then scan only that slot's chain</text>
  </g>
</svg>

Now real numbers. Table size m = 4, h(v) = v, and we store 12, 7, 20, 5 in that
order. 12 mod 4 = 0, 7 mod 4 = 3, 20 mod 4 = 0, 5 mod 4 = 1.

<svg viewBox="0 0 640 230" role="img" aria-label="a chained table with four slots after storing 12, 7, 20 and 5: slot 0 holds 12 then 20, slot 1 holds 5, slot 2 is empty, slot 3 holds 7; looking up 20 computes 20 mod 4 = 0 and compares with 12, then 20">
  <g>
    <text x="20" y="45">slot 0</text>
    <rect class="fill" x="90" y="25" width="50" height="32"/>
    <line x1="140" y1="41" x2="180" y2="41"/>
    <rect x="180" y="26" width="60" height="30" rx="4"/>
    <text x="210" y="46" text-anchor="middle">12</text>
    <line x1="240" y1="41" x2="270" y2="41"/>
    <rect x="270" y="26" width="60" height="30" rx="4"/>
    <text x="300" y="46" text-anchor="middle">20</text>
    <text x="20" y="90">slot 1</text>
    <rect x="90" y="70" width="50" height="32"/>
    <line x1="140" y1="86" x2="180" y2="86"/>
    <rect x="180" y="71" width="60" height="30" rx="4"/>
    <text x="210" y="91" text-anchor="middle">5</text>
    <text x="20" y="135">slot 2</text>
    <rect x="90" y="115" width="50" height="32"/>
    <text x="160" y="135">(empty chain)</text>
    <text x="20" y="180">slot 3</text>
    <rect x="90" y="160" width="50" height="32"/>
    <line x1="140" y1="176" x2="180" y2="176"/>
    <rect x="180" y="161" width="60" height="30" rx="4"/>
    <text x="210" y="181" text-anchor="middle">7</text>
    <text x="360" y="46">get(20): 20 mod 4 = 0,</text>
    <text x="360" y="68">compare 12 (no), 20 (yes)</text>
    <text x="360" y="135">get(14): 14 mod 4 = 2,</text>
    <text x="360" y="157">empty chain: absent, 0 compares</text>
    <text x="20" y="220">12 and 20 share a home. That is a collision, and the chain absorbs it.</text>
  </g>
</svg>

Looking up 20 costs two comparisons, not four, because we only read slot 0. Looking
up 14 costs zero comparisons: its home is slot 2, which is empty, so 14 is not
stored, and we know it without looking anywhere else. That is the entire trick.

One more piece. If we keep inserting without growing m, the chains grow, and with
n keys in m slots the average chain has n/m entries. The ratio α = n/m is the
**load factor**. So the table grows: when α passes some limit (1 in our
implementation, around 2/3 in Python's dict), allocate twice as many slots and
re-insert every key at its new home. That costs Θ(n) once, but it happens rarely
enough that the average cost per insertion stays constant. The argument is in
"What it costs".

### Step 4: put it back into Two Sum

Now the inner loop can go. Keep a dictionary `seen` from value to index, holding
the values to the left of the current position. At each position j:

1. Compute need = target - nums[j]. This is what the inner loop was looking for.
2. If need is in `seen`, the answer is [seen[need], j]. One lookup replaces the
   whole scan.
3. Otherwise put nums[j] -> j into `seen`, so that later positions can find it.

The order of steps 2 and 3 matters, and it is the subtle line of the chapter. It
gets its own demonstration in "From the idea to the code". For now, notice what the
order says: at the moment we look up, `seen` contains exactly the positions
*strictly to the left* of j. That is the same set of positions the inner loop
scanned.

### You might think: "A hash table is O(1), so whatever I put in it is free."

A lookup costs one hash computation plus a comparison or two, and each of those
costs as much as the key is big. For a small integer that is one machine step. For
a string of length L it is L steps. For a key you build inside the loop, like
`tuple(sorted(word))`, it is the cost of building it, here L log L. "O(1)" counts
*how many keys you touch*, not how much each touch costs. In *Group Anagrams*
(variation D) this is the difference between a key that costs L log L and one that
costs L.

### The technique in one sentence

**Keep the part of the input you have already passed in a table keyed by the
thing you will later ask about, so that each "have I seen it?" is a computed
address instead of a scan; the table finds a key's slot from the key itself, and a
short chain absorbs the keys that share a slot.**

And the question that finds the key, worth asking on every new problem: **what is
the inner loop searching for, and could I look it up by name instead?**

## Worked by hand

### Trace 1: Two Sum, one pass

nums = [4, 1, 7, 6], target = 10. Each row is one position. "map before" is the
dictionary at the moment of the lookup.

| j | x = nums[j] | need = 10 - x | map before | need in map? | map after |
|---|---|---|---|---|---|
| 0 | 4 | 6 | {} | no | {4: 0} |
| 1 | 1 | 9 | {4: 0} | no | {4: 0, 1: 1} |
| 2 | 7 | 3 | {4: 0, 1: 1} | no | {4: 0, 1: 1, 7: 2} |
| 3 | 6 | 4 | {4: 0, 1: 1, 7: 2} | **yes, at 0** | (stop) |

Answer [0, 3]. Four lookups and three insertions, against four pair checks for the
brute force on this tiny input. The gap only shows with size: on the worst case of
2,000 numbers in the next section, the brute force makes 1,999,000 checks and the
map makes 2,000 lookups.

The last row, told in words:

> "I am at position 3, holding a 6. For the pair to reach 10, its partner must be
> a 4. Has a 4 appeared to my left? I do not reread positions 0, 1 and 2. I ask
> the table: the home of 4 is computed from 4 itself, I look in that one slot, and
> the 4 is there, filed under index 0. So the answer is index 0 and me, index 3."

And the first row, because it shows why the empty table is not a special case:

> "I am at position 0, holding a 4. My partner would be a 6. Nothing is to my left,
> so the table is empty and the answer is no. I file myself, 4 -> 0, so that
> anyone to my right who needs a 4 will find me."

Look at what each row stores. The table does not hold pairs, sums or candidates.
It holds single values with their indices. A pair is formed only at the moment of
the lookup, out of the current value and one stored value. That is why one pass
suffices: every pair (i, j) with i < j is examined exactly once, at time j, when i
is already in the table.

### Trace 2: inside the table, with a collision

Now the table itself. Chaining, m = 4 slots, h(v) = v, and the operations
put 12, put 7, put 20, put 5, get 20, get 14, put 9.

| op | home = v mod 4 | chain read | result | slots 0 / 1 / 2 / 3 after |
|---|---|---|---|---|
| put 12 | 0 | [] | new key | [12] / [] / [] / [] |
| put 7 | 3 | [] | new key | [12] / [] / [] / [7] |
| put 20 | 0 | [12] | 12 is not 20, new key | [12, 20] / [] / [] / [7] |
| put 5 | 1 | [] | new key | [12, 20] / [5] / [] / [7] |
| get 20 | 0 | [12, 20] | found, 2 compares | unchanged |
| get 14 | 2 | [] | absent, 0 compares | unchanged |
| put 9 | 1 | [5] | new key, n = 5 > m = 4 | resize to m = 8 |

The third row is the collision: 20 and 12 share home 0, so 20 joins 12's chain.
Nothing breaks. The cost of the collision is one extra comparison for anyone who
later looks in slot 0.

The last row shows what the first trace could not: the table grows. After putting
9 there are 5 keys in 4 slots, α = 1.25, above our limit of 1. So we allocate 8
slots and re-insert every key at its *new* home, v mod 8:

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| chain | [] | [9] | [] | [] | [12, 20] | [5] | [] | [7] |

Every key moved: 5 went from slot 1 to slot 5, 7 from 3 to 7, 12 and 20 from 0 to
4. A key's slot depends on m, so after a resize the old positions mean nothing.
This is why you cannot keep "the index of a key inside the table" across
insertions, and why a resize must re-insert rather than copy.

(12 and 20 still share a chain after the resize, because 12 and 20 differ by 8,
a multiple of the new m. With h(v) = v, keys that differ by a multiple of m always
collide. Real hash functions mix the bits to avoid exactly this; see
[[hash-functions]].)

### Trace 3: the other family, and why deletion is hard there

The second way to handle collisions is **open addressing**: no chains, every key
lives in the array itself, and a key whose home is taken walks to the next slot,
then the next, wrapping around, until it finds a free one. This is linear probing.
It is what you write by hand when the problem forbids built-in maps, as
[[p:apple-design-hashmap|Design Hash Map]] does, and it is close to what Python's
dict does internally.

Eight slots, h(v) = v mod 8, insert 12, 20, 5, 28, 13:

| key | home | slots walked | lands at | table after |
|---|---|---|---|---|
| 12 | 4 | 4 (free) | 4 | `. . . . 12 . . .` |
| 20 | 4 | 4 (12), 5 | 5 | `. . . . 12 20 . .` |
| 5 | 5 | 5 (20), 6 | 6 | `. . . . 12 20 5 .` |
| 28 | 4 | 4, 5, 6, 7 | 7 | `. . . . 12 20 5 28` |
| 13 | 5 | 5, 6, 7, 0 | 0 | `13 . . . 12 20 5 28` |

A lookup walks the same path and stops at the first *empty* slot, concluding the
key is absent. Look up 28: start at 4, see 12, 20, 5, find 28 at slot 7. Four
probes, in a table five-eighths full.

Now delete 20 the obvious way, by emptying slot 5, and look up 28 again. Start at
4, see 12, reach slot 5, find it empty, and report that 28 is absent. It is sitting
untouched at slot 7.

<svg viewBox="0 0 660 230" role="img" aria-label="looking up key 28 after deleting key 20 from slot 5: with the slot blanked the walk from home slot 4 stops at the empty slot 5; with a tombstone the walk passes slot 5 and finds 28 at slot 7">
  <g>
    <text x="14" y="52">blanked</text>
    <rect x="140" y="26" width="70" height="42"/>
    <rect x="210" y="26" width="70" height="42"/>
    <rect x="280" y="26" width="70" height="42"/>
    <rect x="350" y="26" width="70" height="42"/>
    <text x="175" y="54" text-anchor="middle">12</text>
    <text x="315" y="54" text-anchor="middle">5</text>
    <text x="385" y="54" text-anchor="middle">28</text>
    <text x="175" y="88" text-anchor="middle">4</text>
    <text x="245" y="88" text-anchor="middle">5</text>
    <text x="315" y="88" text-anchor="middle">6</text>
    <text x="385" y="88" text-anchor="middle">7</text>
    <line x1="175" y1="18" x2="245" y2="18"/>
    <line x1="245" y1="18" x2="233" y2="12"/>
    <line x1="245" y1="18" x2="233" y2="24"/>
    <text x="440" y="54">empty: stop, "absent"</text>
    <text x="14" y="166">tombstone</text>
    <rect x="140" y="140" width="70" height="42"/>
    <rect class="fill" x="210" y="140" width="70" height="42"/>
    <rect x="280" y="140" width="70" height="42"/>
    <rect x="350" y="140" width="70" height="42"/>
    <text x="175" y="168" text-anchor="middle">12</text>
    <text x="245" y="168" text-anchor="middle">T</text>
    <text x="315" y="168" text-anchor="middle">5</text>
    <text x="385" y="168" text-anchor="middle">28</text>
    <text x="175" y="202" text-anchor="middle">4</text>
    <text x="245" y="202" text-anchor="middle">5</text>
    <text x="315" y="202" text-anchor="middle">6</text>
    <text x="385" y="202" text-anchor="middle">7</text>
    <line x1="175" y1="132" x2="385" y2="132"/>
    <line x1="385" y1="132" x2="373" y2="126"/>
    <line x1="385" y1="132" x2="373" y2="138"/>
    <text x="440" y="168">marked: walk on, find 28</text>
  </g>
</svg>

The trace shows something chaining never shows. In open addressing, a key's
findability depends on *other* slots: everything between its home and where it
actually sits must stay non-empty. Deleting 20 did not touch 28, and still made 28
unreachable. The fix is a **tombstone**: deletion writes a marker meaning "a key
used to be here, keep walking". Lookups pass through tombstones; insertions may
reuse them. The Traps section runs both versions.

## From the idea to the code

### The direct version, and the cure, side by side

The program below runs three versions of Two Sum: the double loop, the "remember
it in a list" attempt, and the dictionary. It counts the checks each one makes on
a worst case where the pair is at the end, and then compares the dictionary
against the brute force on random inputs.

```python run
import random

def two_sum_brute(nums, target):
    checks = 0
    for j in range(len(nums)):
        for i in range(j):                      # every earlier index
            checks += 1
            if nums[i] + nums[j] == target:
                return [i, j], checks
    return None, checks

def two_sum_list(nums, target):                 # "remember", but in a list
    seen, checks = [], 0
    for j, x in enumerate(nums):
        for i, y in enumerate(seen):            # `need in seen` hides this loop
            checks += 1
            if y == target - x:
                return [i, j], checks
        seen.append(x)
    return None, checks

def two_sum_map(nums, target):
    seen = {}                                   # value -> index, earlier only
    for j, x in enumerate(nums):
        need = target - x                       # the inner loop's question
        if need in seen:                        # one lookup replaces the scan
            return [seen[need], j], j + 1
        seen[x] = j                             # only now does x join "earlier"
    return None, len(nums)

print("[4,1,7,6], 10 ->", two_sum_brute([4, 1, 7, 6], 10), two_sum_map([4, 1, 7, 6], 10))
assert two_sum_map([4, 1, 7, 6], 10)[0] == [0, 3]
assert two_sum_map([5, 5], 10)[0] == [0, 1]
assert two_sum_map([-3, 4, 9, -1], 8)[0] == [2, 3]

n = 2000                                        # worst case: the pair is at the very end
nums = list(range(1, n - 1)) + [10**6, 10**6 + 1]
t = 2 * 10**6 + 1
for f in (two_sum_brute, two_sum_list, two_sum_map):
    ans, checks = f(nums, t)
    print("%-14s answer %s after %8d checks" % (f.__name__, ans, checks))
    assert ans == [n - 2, n - 1]
assert two_sum_brute(nums, t)[1] == n * (n - 1) // 2

rng = random.Random(7)
for _ in range(300):                            # random cases with one planted pair
    a = rng.sample(range(-50, 50), rng.randint(2, 12))
    i, j = sorted(rng.sample(range(len(a)), 2))
    tgt = a[i] + a[j]
    pairs = [[p, q] for q in range(len(a)) for p in range(q) if a[p] + a[q] == tgt]
    if len(pairs) == 1:
        assert two_sum_map(a, tgt)[0] == two_sum_brute(a, tgt)[0] == pairs[0]
print("one-pass map == brute force on every random case with a unique pair")
```

The list version makes exactly as many checks as the double loop, 1,999,000. It
moved the inner loop into a list scan and saved nothing. The dictionary makes
2,000 lookups. That is the whole chapter in three lines of output.

### Each line, and which part of the brute force it replaces

| line | in plain words | in the brute force |
|---|---|---|
| `seen = {}` | the values to my left, filed by value | the cells the inner loop would scan |
| `for j, x in enumerate(nums)` | visit each position once | the outer loop, unchanged |
| `need = target - x` | the one value that would complete a pair | the condition `nums[i] + nums[j] == target`, solved for nums[i] |
| `if need in seen` | is that value to my left? | the entire inner loop |
| `return [seen[need], j]` | the stored index, then mine | `return [i, j]` |
| `seen[x] = j` | file myself for those to my right | i growing to include j on the next round |

The third line is where the brute force turns into a lookup. The brute force tests
a condition on *pairs*, nums[i] + nums[j] == target. Solving that equation for the
unknown, nums[i] = target - nums[j], turns a test you must run on every i into a
single value you can look up. Almost every hashing trick has this step: rewrite
the condition so that the unknown side is one exact value. In Counting Pairs below
the condition a + k = b becomes "look up a + k". In the subarray-sum problems it
becomes "look up prefix - k".

Two boring confusions, settled.

**Why does the map store an index and not just a value?** Because this problem
returns indices. If it only asked "does a pair exist?", a set would do, and that
is [[p:capgemini-contains-duplicate|Contains Duplicate]]: the same loop with
`if x in seen: return True` and `seen.add(x)`. What you store as the value is
decided by what you must return.

**What happens with duplicates, like [5, 5] and target 10?** At j = 0, need is 5
and the map is empty: no. File 5 -> 0. At j = 1, need is 5, found at 0: answer
[0, 1]. The first 5 was filed before the second one looked. If a value appears
three times and the map overwrites its index, the map remembers the *latest*
earlier index. That is fine here because the problem promises one pair; when it
is not fine, store a list or a count.

### The subtle line, both ways

The line that decides whether the code is right is the position of `seen[x] = j`:
**look up first, then file yourself**. Here are the right order and the two wrong
ones on the same tiny input, nums = [3, 2, 4] and target 6. The answer is [1, 2]
(2 + 4).

**Right: look up, then store.**

| j | x | need | map at lookup | hit | then store |
|---|---|---|---|---|---|
| 0 | 3 | 3 | {} | none | {3: 0} |
| 1 | 2 | 4 | {3: 0} | none | {3: 0, 2: 1} |
| 2 | 4 | 2 | {3: 0, 2: 1} | **1** | return [1, 2] |

**Wrong: store, then look up.**

| j | x | stored first | need | map at lookup | hit |
|---|---|---|---|---|---|
| 0 | 3 | {3: 0}* | 3 | {3: 0}* | **0**, return [0, 0] |

The `*` marks the entry written this round. The very first lookup reads the entry
the same position just wrote. Position 0 needs a 3, and it is a 3, so it finds
itself. The function returns [0, 0], using one element twice, which the statement
forbids.

**Also wrong: build the whole map first, then scan.** `where = {x: j for j, x in
enumerate(nums)}` holds every position, left and right, including the current
one. On [3, 2, 4], position 0 asks for a 3, finds where[3] = 0, and returns [0, 0].
On the sample [5, 5] it happens to work: the comprehension overwrites where[5] with
the last index, 1, so position 0 finds 1. **The sample passes and the hidden test
fails.** That is the worst kind of bug, and it is why you should test Two Sum on an
input where target is twice some value that appears once.

```python run
def check_then_store(nums, target, log):
    seen = {}
    for j, x in enumerate(nums):
        need = target - x
        hit = seen.get(need)                    # read "earlier" BEFORE x joins it
        log.append((j, x, need, dict(seen), hit))
        if hit is not None:
            return [hit, j]
        seen[x] = j
    return None

def store_then_check(nums, target, log):
    seen = {}
    for j, x in enumerate(nums):
        seen[x] = j                             # x joins first ...
        need = target - x
        hit = seen.get(need)                    # ... so x can find itself
        log.append((j, x, need, dict(seen), hit))
        if hit is not None:
            return [hit, j]
    return None

def show(name, f, nums, target):
    log = []
    ans = f(nums, target, log)
    print(name, nums, "target", target)
    for j, x, need, seen, hit in log:
        print("   j=%d x=%d need=%d map=%-18s hit=%s" % (j, x, need, seen, hit))
    print("   ->", ans)
    return ans

assert show("right:", check_then_store, [3, 2, 4], 6) == [1, 2]
assert show("wrong:", store_then_check, [3, 2, 4], 6) == [0, 0]   # used 3 twice

def map_everything_first(nums, target):     # the third common version
    where = {x: j for j, x in enumerate(nums)} # last index of each value
    for i, x in enumerate(nums):
        if target - x in where:
            return [i, where[target - x]]
print("map first, [5,5] ->", map_everything_first([5, 5], 10), "(luck: 5 -> 1)")
print("map first, [3,2,4] ->", map_everything_first([3, 2, 4], 6))
assert map_everything_first([5, 5], 10) == [0, 1]                 # sample passes
assert map_everything_first([3, 2, 4], 6) == [0, 0]               # hidden test fails

def pairs_with_replacement(values, k):          # what store-then-check really counts
    s = set(values)
    return sum(1 for a in s if a + k in s)      # (a, a) is allowed when k = 0
print("Counting Pairs [1,2], k=0 ->", pairs_with_replacement([1, 2], 0))
assert pairs_with_replacement([1, 2], 0) == 2
assert pairs_with_replacement([1, 1, 1, 2], 1) == 1
```

Why does the order matter so much? Because the map *is* the inner loop's range. In
the brute force the inner loop ran over i < j, strictly less. "Look up, then
store" keeps the map equal to exactly {positions < j} at the moment of the lookup.
"Store, then look up" makes it {positions <= j}, which is the brute force with
`range(j + 1)` instead of `range(j)`. "Map everything first" makes it every
position, which is the brute force with both loops running over the whole array.

So the wrong versions are not random bugs. They compute a different, well-defined
thing: **pairs where an element may be paired with itself**. Sometimes that is
exactly what a problem wants. In [[p:amazon-count-pairs|Counting Pairs]] the
statement says that when k = 0 "each distinct value x contributes the pair (x, x);
one occurrence of x is sufficient". There, a set of all values and the question
"is a + k in the set?" is right, self-pairs included. The last lines of the block
show it: for [1, 2] and k = 0 the answer is 2. Read the statement, decide whether
an element may pair with itself, and then choose where the store goes. That is the
habit.

### Building the table yourself

Interviews sometimes forbid the built-in dictionary, as
[[p:apple-design-hashmap|Design Hash Map]] does. Here is a chained map written as
the derivation describes it: compute the home, scan one chain, double when the load
factor passes 1. It runs the problem's sample and then 20,000 random operations
against Python's dict.

```python run
import random

class ChainedMap:
    """Separate chaining: bucket h(k) mod m holds every live key with that home."""
    def __init__(self, m=4):
        self.buckets = [[] for _ in range(m)]
        self.n = 0                                  # live keys

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]   # compute, never search

    def put(self, key, value):
        b = self._bucket(key)
        for pair in b:
            if pair[0] == key:                      # already here: overwrite
                pair[1] = value
                return
        b.append([key, value])                      # new key: one more in this chain
        self.n += 1
        if self.n > len(self.buckets):              # load factor above 1: double
            self._resize(2 * len(self.buckets))

    def get(self, key, default=-1):
        for k, v in self._bucket(key):              # scan ONE chain, not the table
            if k == key:
                return v
        return default

    def remove(self, key):
        b = self._bucket(key)
        for i, pair in enumerate(b):
            if pair[0] == key:
                b.pop(i)
                self.n -= 1
                return True
        return False

    def _resize(self, m):
        old = [p for b in self.buckets for p in b]
        self.buckets = [[] for _ in range(m)]
        for k, v in old:                            # every key gets a NEW home
            self._bucket(k).append([k, v])

h = ChainedMap(4)
for k in (12, 7, 20, 5):
    h.put(k, k * 10)
print("m=4 buckets:", [[k for k, _ in b] for b in h.buckets])
assert [[k for k, _ in b] for b in h.buckets] == [[12, 20], [5], [], [7]]
h.put(9, 90)                                        # 5 keys > 4 buckets: resize
print("m=8 buckets:", [[k for k, _ in b] for b in h.buckets])
assert len(h.buckets) == 8 and h.get(20) == 200 and h.get(16) == -1

d, out = ChainedMap(), []
for op, k, v in zip(["put", "put", "get", "get", "put", "get", "remove", "get"],
                    [1, 2, 1, 3, 2, 2, 2, 2], [10, 20, 0, 0, 25, 0, 0, 0]):
    if op == "put": d.put(k, v)
    elif op == "get": out.append(d.get(k))
    else: d.remove(k)
print("Design Hash Map sample ->", out)
assert out == [10, -1, 25, -1]

rng, mine, ref = random.Random(3), ChainedMap(), {}
for _ in range(20000):
    k, v, r = rng.randrange(300), rng.randrange(1000), rng.random()
    if r < 0.5: mine.put(k, v); ref[k] = v
    elif r < 0.7: assert mine.remove(k) == (ref.pop(k, None) is not None)
    else: assert mine.get(k) == ref.get(k, -1)
    assert mine.n == len(ref)
print("20000 random ops agree with dict; m =", len(mine.buckets),
      "longest chain", max(len(b) for b in mine.buckets))
```

The lines that carry the idea:

| line | what it does | why it is written that way |
|---|---|---|
| `hash(key) % len(self.buckets)` | the home slot | the only place a key may live; every operation computes it the same way |
| `for pair in b: if pair[0] == key` | scan one chain | a collision means "same home", not "same key", so equality must still be checked |
| `pair[1] = value` then `return` | overwrite an existing key | without this, a second put adds a duplicate and `get` returns the stale one |
| `if self.n > len(self.buckets)` | keep α at most 1 | short chains are what make each scan constant |
| `_resize` re-inserts with `_bucket(k)` | new homes for everyone | the home depends on m, so copying chains across would file keys in the wrong slots |

The last line of output says the longest chain, after 20,000 random operations on
300 possible keys, has two entries. That is what "expected O(1)" looks like in
practice.

## Why it is correct

There are two things to prove: that the table answers questions correctly, and
that the one-pass Two Sum built on it returns the right pair. Each is a loop
invariant, a sentence that is true before every step and still true after it.

:::proof The chained table is a correct map, and one-pass Two Sum finds the pair
**Part 1: the table.**

*The invariant.* For every key k that has been put and not since removed, there is
exactly one entry (k, v) in the whole table, it sits in bucket h(k) mod m, and v is
the value of the most recent put of k. No other entries exist.

*Why it is enough.* `get(k)` scans bucket h(k) mod m. If k is live, the invariant
says its single entry is in that bucket, so the scan finds it and returns the
latest value. If k is not live, no entry for k exists anywhere, so the scan finds
none and returns the default. So if the invariant holds, every `get` is right.

*Base case.* An empty table has no entries and no live keys. The invariant holds.

*Each operation keeps it.*
- `put(k, v)` scans bucket h(k) mod m. If it finds k, it overwrites the value: still
  one entry, same bucket, now the latest value. If it does not find k, then by the
  invariant k has no entry anywhere (its only legal place is this bucket), so
  appending one creates exactly one entry in the right bucket.
- `remove(k)` scans the same bucket and deletes the entry if present. Afterwards k
  is not live and has no entry. No other key's entry moved.
- `resize` takes every entry out and puts each into bucket h(k) mod m' for the new
  m'. Each key still has one entry, now in its new home, with its value unchanged.
  Afterwards every later operation computes homes with m', so they agree.

*Conclusion.* The invariant holds after every operation, so every `get` is right.

**Part 2: one-pass Two Sum.**

*The invariant.* At the moment position j does its lookup, `seen` contains a key for
exactly the values at positions 0..j-1, and `seen[v]` is some position i < j with
nums[i] = v.

*Base case.* At j = 0 the map is empty and there are no earlier positions.

*Step.* Position j looks up and then, if it did not return, stores nums[j] -> j. So
at the lookup of position j + 1 the map holds the values of positions 0..j, each
mapped to a position at most j. The invariant holds for j + 1.

*It finds the pair.* Let the unique answer be (i*, j*) with i* < j*. Every position
j < j* that looks up and hits would have returned a pair (i, j) with i < j and
nums[i] + nums[j] = target. That would be a second answer, which the problem rules
out. So the loop reaches j*. There, need = target - nums[j*] = nums[i*], and since
i* < j*, the invariant says the value nums[i*] is in the map, filed under some
i < j* with nums[i] = nums[i*]. That (i, j*) is a valid pair, so by uniqueness it
is (i*, j*).

*It never uses an element twice.* The lookup at j sees only positions < j, so it
can never return j itself. ∎
:::

Now the assumptions the proof used, in plain words. Each one is a bug when it fails.

- **Equal keys compute the same home.** Part 1 said "k's only legal place is this
  bucket". If two equal keys could hash differently, `put` would miss the existing
  entry and create a second one. Python enforces this for built-in types; for your
  own classes, `__eq__` and `__hash__` must agree.
- **A key does not change while it is stored.** Its home was computed when it was
  put. If the key mutates, its home moves and its entry does not. This is why Python
  refuses lists as keys (a list can change) and accepts tuples.
- **Every operation computes the home the same way, with the current m.** That is
  why the resize must re-insert.
- **The lookup happens before the store.** Part 2's invariant says "positions
  0..j-1" at the lookup. Store first and it becomes "0..j", and the last step of the
  proof, "never returns j itself", is false.
- **The pair is unique.** The proof used uniqueness twice. If several pairs exist,
  the one-pass map returns the pair whose *right* end is smallest, which may not be
  the pair a tie rule asks for. A Two Sum variant with "lexicographically smallest
  pair" as its tie rule needs a different argument.

And the proof never mentions speed. A table whose hash sends every key to slot 0
satisfies every line above and answers every question correctly, slowly. So a hash
table that gives *wrong answers* is never a bad hash function. It is always a
broken key contract: a key that changed, or two equal keys that hash differently.

:::note The open-addressing invariant is about a path
For open addressing the invariant is different: "every slot between a key's home
and its actual position is non-empty". That is a statement about several slots at
once, which is why emptying one slot can break it for a key that was never
touched, as trace 3 showed. A tombstone keeps the slot non-empty, so the path
survives. Chaining has no such property, which is why deleting from a chain is just
a list removal.
:::

## What it costs

### The brute force

The double loop checks n(n-1)/2 pairs in the worst case, Θ(n²). For n = 10^5 that
is 5 x 10^9. The list version is the same Θ(n²), hidden inside `in`.

### One lookup in a chained table

Assume the hash spreads keys evenly: each key is equally likely to land in any of
the m slots, independently. This is a modelling assumption, and the end of this
section is about when it fails.

A lookup for an absent key scans one whole chain. For each of the n stored keys,
the chance it is in this particular chain is 1/m, so the expected chain length is
n times 1/m, which is α. The expected cost is 1 (computing the home) plus α
(the scan). A lookup for a present key scans half its chain on average, also
Θ(1 + α). Keep α below a constant, by resizing, and every operation is expected
Θ(1).

### The resizes

Each resize re-inserts all n keys, Θ(n) work. That sounds bad until you add them
up. Starting from m = 4 and doubling, a table that ends with n keys was resized at
sizes 4, 8, 16, ..., up to about n. The total work is

```
4 + 8 + 16 + ... + n  <  2n
```

because each term of a doubling series is bigger than all the earlier ones put
together. So n insertions cost at most 2n of resize work in total, an average of
2 per insertion: constant. This is the same argument that makes Python's
`list.append` cheap ([[amortized-analysis]]). It needs the table to grow by a
*factor*. Growing by a fixed number of slots each time gives a sum like
c + 2c + 3c + ... which is Θ(n²/c).

So the full statement is: **expected, amortised O(1) per operation**. "Expected"
because of the hashing assumption, "amortised" because of the resizes.

### One-pass Two Sum

n positions, each doing one lookup and at most one insertion: expected O(n) time.
The map holds at most n entries: O(n) space. That is the trade the technique always
makes. You pay memory for the past so you do not have to reread it.

### Open addressing

With linear probing the cost depends on how full the table is in a way that
surprises people. For an unsuccessful lookup, under the even-spreading assumption,
the probability that the first probe hits an occupied slot is about α, that the
first two do is about α², and so on. Adding up the chances of needing at least 1,
2, 3, ... probes gives

```
1 + α + α² + α³ + ...  =  1 / (1 - α)
```

| α | 0.5 | 0.75 | 0.9 | 0.99 |
|---|---|---|---|---|
| expected probes | 2 | 4 | 10 | 100 |

Half full costs 2 probes; 99% full costs 100. The cost does not grow evenly with
fullness; it explodes at the end. That is why open-addressed tables resize at half
to two-thirds full. (The exact analysis for linear probing gives a somewhat larger
number because runs merge, but the shape is the same.)

### The cost everyone forgets: the key

"O(1)" counts how many keys you touch. Each touch costs one hash computation and
one or two equality checks, and both cost as much as the key is long.

- An integer key: one machine step.
- A string of length L: Θ(L) to hash, Θ(L) to compare.
- A key built in the loop: the cost of building it. `tuple(sorted(word))` is
  Θ(L log L); a 26-count tuple is Θ(L + 26).

So the honest cost of a dictionary problem over strings is O(total characters), not
O(number of strings). Problems state a bound on the total length of all strings for
exactly this reason.

### The worst case

If every key lands in the same slot, the chain has n entries and each operation is
Θ(n), so building the table is Θ(n²). This happens with a bad hash on structured
data (h(v) = v with keys that are all multiples of m, as trace 2 hinted) or with an
attacker who picks colliding keys on purpose. That is why Python randomises its
string hash per process. It does not randomise integer hashes, so a hand-written
table with `v % m` and adversarial integers can be slow. In interview problems this
almost never matters; in a production service it does ([[hash-functions]],
[[randomized-algorithms]]).

## How to think about it

The code is short. What takes practice is seeing the lookup hiding in a problem.
Ask these, in order, on every new problem in this family.

1. **What would the brute force's inner loop search for?** Write the brute force in
   your head, then read its inner loop as a sentence: "is there an earlier value
   equal to target - x?", "has this word's letter count appeared before?", "is
   x - 1 present?". If the inner loop is a search for one exact thing, a table
   removes it.
2. **What is the key? Write it down as an expression.** `target - x`, `x`,
   `tuple(counts)`, `request_id`, `prefix_sum - k`, `nums[i] - i`. Most hashing bugs
   are not table bugs; they are the wrong key. Naming it out loud catches them.
3. **What is the value?** Nothing (a set), an index, a count, a list of members, a
   last-seen time. It is decided by what you must return or update.
4. **The past, or everything?** If the condition is about pairs i < j, build the
   table as you go and look up before storing. If you need facts about the whole
   input (total counts), build it in a first pass and use it in a second.
5. **May an element pair with itself?** Decide from the statement. This picks the
   position of the store.
6. **Are the keys a small dense range?** Letters, digits, values in 1..n, counts in
   0..n. Then a list indexed by the key replaces the dictionary, and sometimes the
   input array itself can be the table.
7. **Does the answer need order?** First, smallest, sorted output, k-th. The table
   gives identity; the order must come from the input scan or from a sort.
8. **How big is a key?** If keys are long strings or built tuples, the real cost is
   the total size of the keys.

Then, before code, write three lines: **the key**, **the value**, and **when the
store happens relative to the lookup**. If you cannot write those three lines, the
code will not find them for you.

### Telling it from its neighbours

- **[[sorting]] and [[two-pointers]].** Both can answer pair questions. Sorting
  costs n log n and gives you order for free; hashing costs n and gives you none.
  If the question only needs equality ("is this value present?"), hash. If it needs
  "closest", "smallest", or ranges, sort.
- **[[frequency-counting]] and [[anagrams]].** These are this chapter's variations C
  and D, deep enough to have their own chapters.
- **[[prefix-sums]].** "Subarray with sum k" is complement lookup where the key is a
  prefix sum. Same code shape as Two Sum, a different key.
- **[[sliding-window]].** A window often keeps a count map of what is inside it. The
  map answers identity; the window's two pointers supply order.
- **[[union-find]] and graphs.** When nodes are strings, a map from name to a small
  integer ("interning") lets array-based structures work on them.
- **[[trie]].** Prefix questions. A hash table only knows whole keys.

## Variations

Nine variations. Each says what changes, why, a small example you can check, and a
problem from the bank. A to E are everyday interview material. F is common in
"O(1) extra space" follow-ups. G is the systems variation this chapter must also
cover. H is less common, I is rare.

### A. A set to remember what you have seen

**What changes.** The value disappears. The table stores only keys, and the only
question is "is it here?".

**Why.** When the answer is yes or no, or when you only need to know whether a
neighbour exists, the index is dead weight.

**Example.** [[p:capgemini-contains-duplicate|Contains Duplicate]]: [1, 2, 3, 1].
After 1, 2, 3 the set is {1, 2, 3}; the fourth value 1 is already in it: true.
Same loop as Two Sum with the key x instead of target - x.

**A deeper example.** [[p:amazon-longest-consecutive-sequence|Longest Consecutive Sequence]]:
the longest run of consecutive integers among the values, in any order.
[100, 4, 200, 1, 3, 2] gives 4 (the run 1, 2, 3, 4). Put every value in a set. Then
for each value x, ask "is x - 1 present?". If yes, x is not the start of a run, so
skip it. If no, walk x + 1, x + 2, ... while they are present.

You might think this is O(n²), a loop inside a loop. It is not, and the reason is
the skip. A walk only starts at the first value of a run, and it visits each value
of that run once. Every value belongs to exactly one run, so all the walks together
visit each value once: n steps of walking in total, plus n checks of x - 1. On the
example, the walks are 1 -> 2 -> 3 -> 4 (three steps), 100 (none) and 200 (none):
three steps total, which the run block below asserts. Remove the
`if x - 1 in s: continue` and the same input on a run of length n costs
n + (n-1) + ... + 1 steps.

### B. A map from value to index: look up the complement

**What changes.** The key is not the current value but the value that would
*complete* it, obtained by solving the condition for the unknown.

**Why.** The condition is about pairs. Solving it for one side turns "test every
partner" into "look up the one partner that would work".

**Example.** Two Sum, the subject of this chapter.

**With duplicates and self-pairs.** [[p:amazon-count-pairs|Counting Pairs]]: count
distinct value pairs (a, b) with a + k = b. [1, 1, 1, 2] with k = 1 gives 1: three
copies of 1 still make one value pair (1, 2). So the table is a *set of distinct
values*, and the count is "how many a in the set have a + k in the set". When
k = 0 each value pairs with itself, as the statement allows, so the answer is the
number of distinct values. Here the "store everything first" order is correct.

**When the complement is a family.** [[p:hrt-count-one-swap-number-pairs|Count One-Swap Number Pairs]]
counts index pairs where one number turns into the other by swapping at most one
pair of digits. The partner is not one value but a small set: all numbers reachable
by one digit swap, at most about 45 for a ten-digit number. So for each number,
generate that set (plus the number itself), and look each one up in a frequency map
of the numbers to the left. The work is n times the size of the family, instead of
n². The key insight is the same: do not compare pairs, generate the partners and
look them up. Careful with the "each pair once" rule: a number with repeated digits
can reach the same partner by two different swaps, so put the generated partners in
a set before looking them up.

### C. Counting with a frequency map

**What changes.** The value is a tally. `cnt[x] = cnt.get(x, 0) + 1`, or
`collections.Counter`.

**Why.** Many questions only depend on *how many* copies of each value there are,
not where they are. Counting throws away positions and keeps exactly that.

**Example.** [[p:motive-valid-anagram|Valid Anagram]]: "anagram" and "nagaram" are
anagrams because both have a: 3, n: 1, g: 1, r: 1, m: 1. Two strings are anagrams
exactly when their counts are equal. Order of letters has disappeared, which is the
point. With only 26 letters, a list of 26 integers is the count map.

**Counting replaces repeated scanning.** [[p:amazon-replace-values-and-return-sums|Replace Values and Return Sums]]:
each transaction replaces every occurrence of one value with another, and you report
the sum. Rewriting the array is O(n) per transaction. But the sum only depends on
how many copies of each value exist. Keep `cnt` and the running `total`. For
transaction (old, new): let c = cnt[old]; total += c * (new - old); move the c
copies, cnt[new] += c, and delete cnt[old]. Example [1, 2, 1, 3], transactions
[1, 4], [2, 1], [4, 2]: counts {1: 2, 2: 1, 3: 1}, total 7. Replace 1 by 4:
total 7 + 2 x 3 = 13. Replace 2 by 1: 13 - 1 = 12. Replace 4 by 2: 12 + 2 x (-2) = 8.
Answers [13, 12, 8], matching the statement. Each transaction is O(1). Watch the
case old = new, where deleting cnt[old] after adding to cnt[new] deletes the copies
you just moved.

**Counting over a tiny alphabet.** [[p:google-maximum-elements-with-a-common-digit|Maximum Elements With a Common Digit]]:
two-digit numbers, choose the largest group that shares a digit. Fix the shared
digit d, one of 10, and count the numbers containing d (a number like 55 counts
once). The answer is the largest of the ten counts. [52, 25, 11, 52, 34, 55]: digit
5 is in 52, 25, 52, 55, so 4.

**Counting turns a hard question into arithmetic.** [[p:amazon-count-distinct-passwords|Count Distinct Passwords]]:
how many distinct strings can be made by reversing one substring? Reversing s[i..j]
where s[i] = s[j] gives the same string as reversing the shorter s[i+1..j-1], so
only reversals whose end letters differ produce something new, and each such pair
(i, j) produces a different string. So the answer is 1 (the original) plus the
number of pairs i < j with different letters, which is
C(n, 2) minus, for each letter, C(count, 2). "abc": 1 + 3 - 0 = 4. "abaa": a appears
3 times, b once, 1 + 6 - 3 = 4. Both match the statement. Twenty-six counts, no
strings built.

### D. A canonical key to group things

**What changes.** The key is a *signature* computed from the item, chosen so that
two items get the same signature exactly when they belong together.

**Why.** "Group items that are equivalent" is hashing on the equivalence class
rather than on the item. The whole art is the signature function.

**Example.** [[p:amazon-group-anagrams|Group Anagrams]]: ["eat", "tea", "tan",
"ate", "nat", "bat"]. The signature of "eat" is its 26 letter counts (one a, one e,
one t). "tea" and "ate" have the same counts, so the same key, so the same group.
Groups: {ate, eat, tea}, {bat}, {nat, tan}. The problem forbids sorting the letters
and asks for the count vector, which is the cheaper key: Θ(L) to build instead of
Θ(L log L). In Python the count list must become a tuple to be a key, because lists
can change and so cannot be hashed.

A good signature has two properties, and you should check both. **Equal items get
equal keys** (all anagrams of "eat" get the same counts). **Unequal items get
unequal keys** ("eat" and "tee" have different counts). A key that fails the first
splits a group; a key that fails the second merges two groups. The first letter of
a word, for instance, merges "eat" with "egg".

**A signature with arithmetic in it.** [[p:amazon-maximum-equal-parts-for-prefixes|Maximum Equal Parts for Prefixes]]:
for each prefix of a string of capital letters, the most pieces it can be cut into
with the same letter counts in every piece. A cut point must be an earlier prefix
whose count vector is the whole prefix's vector scaled down. Divide a count vector
by the gcd of its entries and you get its "shape": "AB" has counts (1, 1), "ABAB"
has (2, 2), and both have shape (1, 1). So the shape is a canonical key, and a map
from shape to the earlier prefixes with that shape finds the candidate cut points
directly. Same idea as anagrams: find the quantity that is equal exactly when things
belong together.

### E. Buckets indexed by frequency or value

**What changes.** After counting, you need the values ordered by their counts. The
counts are integers between 1 and n, so instead of sorting, you use the count as an
index into an array of n + 1 buckets.

**Why.** A sort costs O(m log m) for m distinct values. Buckets cost O(n), because the
key (a count) is a small integer and needs no comparison. This is direct addressing
from step 3 again, applied to counts instead of values.

**Example.** [[p:bloomberg-top-k-frequent-elements|Top K Frequent Elements]]:
[1, 1, 1, 2, 2, 3], k = 2. Counts {1: 3, 2: 2, 3: 1}. Buckets: bucket[3] = [1],
bucket[2] = [2], bucket[1] = [3]. Walk from bucket 6 down, collecting until k values:
1, then 2. Answer [1, 2]. With the bank's tie rule (equal counts: smaller value
first), sort inside each bucket. [4, 4, -1, -1, 2] with k = 2: bucket[2] = [4, -1],
sorted [-1, 4]: answer [-1, 4].

The variations A, C, D and E, run:

```python run
from collections import Counter, defaultdict

def longest_consecutive(nums):                 # A: a set of what exists
    s, best, steps = set(nums), 0, 0
    for x in s:
        if x - 1 in s:
            continue                           # not the start of a run: skip
        y = x
        while y + 1 in s:                      # walk the run once, from its start
            y += 1
            steps += 1
        best = max(best, y - x + 1)
    return best, steps

def top_k(nums, k):                            # E: buckets indexed by frequency
    cnt = Counter(nums)
    bucket = [[] for _ in range(len(nums) + 1)]   # a count is at most n
    for v, c in cnt.items():
        bucket[c].append(v)
    out = []
    for c in range(len(nums), 0, -1):          # highest frequency first
        for v in sorted(bucket[c]):            # tie rule: smaller value first
            if len(out) < k:
                out.append(v)
    return out

def group_anagrams(words):                     # D: a canonical key
    groups = defaultdict(list)
    for w in words:
        sig = [0] * 26
        for ch in w:
            sig[ord(ch) - 97] += 1
        groups[tuple(sig)].append(w)           # a list cannot be a key; a tuple can
    return sorted(sorted(g) for g in groups.values())

def replace_sums(entries, transactions):       # C: counts instead of rewriting
    cnt, total, out = Counter(entries), sum(entries), []
    for old, new in transactions:
        c = cnt.pop(old, 0)                    # take the copies out first ...
        total += c * (new - old)
        cnt[new] += c                          # ... so old == new is harmless
        out.append(total)
    return out

def distinct_passwords(s):                     # C: count pairs of different letters
    n = len(s)
    return 1 + n * (n - 1) // 2 - sum(c * (c - 1) // 2 for c in Counter(s).values())

def reversals_brute(s):
    return len({s[:i] + s[i:j + 1][::-1] + s[j + 1:]
                for i in range(len(s)) for j in range(i, len(s))})

print(longest_consecutive([100, 4, 200, 1, 3, 2]))
assert longest_consecutive([100, 4, 200, 1, 3, 2]) == (4, 3)
print(top_k([1, 1, 1, 2, 2, 3], 2), top_k([4, 4, -1, -1, 2], 2))
assert top_k([1, 1, 1, 2, 2, 3], 2) == [1, 2] and top_k([4, 4, -1, -1, 2], 2) == [-1, 4]
g = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
print(g)
assert g == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
print(replace_sums([1, 2, 1, 3], [[1, 4], [2, 1], [4, 2]]), replace_sums([5, 5], [[1, 2], [5, 1]]))
assert replace_sums([1, 2, 1, 3], [[1, 4], [2, 1], [4, 2]]) == [13, 12, 8]
assert replace_sums([5, 5], [[5, 5]]) == [10]
for s in ["abc", "abaa", "aabbc", "zzzz", "abcab"]:
    assert distinct_passwords(s) == reversals_brute(s)
print("distinct passwords:", distinct_passwords("abc"), distinct_passwords("abaa"), "(brute agrees)")
```

### F. The array index as the hash (in-place marking)

**What changes.** No dictionary at all. When the values are known to lie in 1..n
and the array has about n cells, the array itself is a direct-address table:
"value v has been seen" is recorded *in cell v*, usually by flipping its sign or by
swapping v into cell v - 1.

**Why.** The follow-up "use O(1) extra space" forbids a set. But the values are
small integers, which is exactly the case where direct addressing needs no hash,
and the array you were given has room. The sign bit of each cell is a free boolean,
because all values are positive.

**Example: sign marking.** [[p:spacex-duplicate-number|Find the Duplicate Number]]:
length n, values 1..n-1, one value appears twice. For each value v, look at cell
|v|. If it is already negative, v was seen before: v is the answer. Otherwise make
it negative. On [1, 3, 4, 2, 2]:

| step | v | cell abs(v) before | action | array after |
|---|---|---|---|---|
| 1 | 1 | a[1] = 3 | mark | [1, -3, 4, 2, 2] |
| 2 | -3, use 3 | a[3] = 2 | mark | [1, -3, 4, -2, 2] |
| 3 | 4 | a[4] = 2 | mark | [1, -3, 4, -2, -2] |
| 4 | -2, use 2 | a[2] = 4 | mark | [1, -3, -4, -2, -2] |
| 5 | -2, use 2 | a[2] = -4 | **already marked** | answer 2 |

Step 2 is why the code says `abs(v)`: by the time you read a value, an earlier step
may have negated it. Forget the abs and you index a negative position, which Python
does not reject; it silently reads from the end of the list (Traps shows it).

**Example: cyclic placement.** [[p:amazon-first-missing-positive|First Missing Positive]]:
the smallest positive integer not in the array, in O(1) extra space. The answer is
at most n + 1, so only values 1..n matter. Swap every value v in 1..n into cell
v - 1, its home, until each cell holds its own number or junk. Then the first cell i
that does not hold i + 1 gives the answer i + 1. [3, 4, -1, 1]: send 3 home (swap
with cell 2): [-1, 4, 3, 1]; -1 stays; 4 home: [-1, 1, 3, 4]; 1 home: [1, -1, 3, 4].
Cell 1 does not hold 2, so the answer is 2. Each swap puts one value in its final
home, so there are at most n swaps in total, and the whole thing is O(n). This is
[[cyclic-sort]].

```python run
def find_duplicate(nums):
    a = list(nums)
    for v in a:
        i = abs(v)                             # v may already carry a mark
        if a[i] < 0:
            return i                           # cell i was marked before: seen twice
        a[i] = -a[i]

def first_missing_positive(nums):
    a, n = list(nums), len(nums)
    for i in range(n):
        while 1 <= a[i] <= n and a[a[i] - 1] != a[i]:
            j = a[i] - 1
            a[i], a[j] = a[j], a[i]            # send value v home to index v-1
    return next((i + 1 for i in range(n) if a[i] != i + 1), n + 1)

for nums, want in [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3), ([1, 1], 1)]:
    got = find_duplicate(nums)
    print("duplicate in", nums, "->", got)
    assert got == want
for nums, want in [([1, 2, 0], 3), ([3, 4, -1, 1], 2), ([7, 8, 9], 1), ([1], 2)]:
    got = first_missing_positive(nums)
    print("first missing positive of", nums, "->", got)
    assert got == want
assert all(first_missing_positive(list(range(1, k + 1))) == k + 1 for k in range(6))
```

Note the condition `a[a[i] - 1] != a[i]` in the swap loop. It is the "already home"
test, and it is also what stops an infinite loop on duplicates: with [1, 1], the
second 1 sees that cell 0 already holds a 1 and stops.

### G. Idempotency and retries: the request id is the key

**What changes.** The items are events from a system that may deliver the same event
more than once. The key is an identifier of the *request*, and the table remembers
which requests were already applied, or when each was last seen.

**Why.** A client sends a payment, the network loses the reply, and the client sends
it again. If the server applies both, the customer pays twice. An operation is
**idempotent** when applying it twice has the same effect as applying it once.
`balance += amount` is not. "If this request id is not in my journal, apply it and
add it to the journal" is. A hash table keyed by request id turns an unreliable
stream of deliveries into a set of distinct requests.

The hard part is choosing the key, and it is a hashing question: two deliveries
must get the same key exactly when they are the same request. Key on
(user, amount) and two genuine purchases of the same coffee collapse into one. Key
on (user, amount, timestamp) and a retry with a fresh timestamp looks new. The
right key is an id the client generates once, before the first attempt, and
repeats on every retry. That is variation D's two properties again: equal requests
get equal keys, different requests get different keys.

**Example: counting retries.** [[p:ibm-request-retry-count|Request Retry Count]]:
logs of (requestId, timestamp), sorted by time. A retry is two consecutive logs of
the same id at most `gap` apart. Keep a map from id to the time of its previous log.
For each log, if the id is in the map and the difference is at most gap, count a
retry; then always update the map to this time. With gap 10, r1 at 100, 105, 200 and
r2 at 300, 302: r1 gives one retry (105 - 100), not two (200 - 105 = 95), and r2 gives
one: total 2. The map's value is "last seen", not "first seen", because the rule is
about *consecutive* logs.

**Example: dedup keeping the latest.** [[p:google-deduplicate-logs-keep-latest|Deduplicate Logs: Keep Latest]]:
keep, per message, the entry with the greatest timestamp, then sort the survivors.
The map is message -> best timestamp so far. Hashing finds the duplicates; a final
sort supplies the output order, because the map has none.

**Example: matching counts.** [[p:yelp-broken-customer-transactions|Identify Broken Customer Transactions]]:
a customer is broken when their number of started transactions differs from their
number of finished ones. Count +1 per start and -1 per finish in one map; the broken
names are the keys whose total is not zero, then sorted.

```python run
LOG = [("r1", "ann", -30), ("r2", "bob", -10), ("r1", "ann", -30),
       ("r3", "ann", +50), ("r2", "bob", -10), ("r1", "ann", -30)]

def apply_naive(records, bal):
    for _, user, delta in records:
        bal[user] = bal.get(user, 0) + delta
    return bal

def apply_once(records, bal, journal):
    for rid, user, delta in records:
        if rid in journal:
            continue                          # a retry, not a second request
        journal.add(rid)
        bal[user] = bal.get(user, 0) + delta
    return bal

print("naive    :", apply_naive(LOG, {"ann": 100, "bob": 100}))
journal = set()
once = apply_once(LOG, {"ann": 100, "bob": 100}, journal)
again = apply_once(LOG + LOG, dict(once), journal)
print("journal  :", once, "replayed:", again)
assert once == {"ann": 120, "bob": 90} and again == once   # idempotent

def retry_count(gap, ids, times):             # Request Retry Count
    last, retries = {}, 0                      # id -> time of its previous log
    for rid, t in zip(ids, times):
        if rid in last and t - last[rid] <= gap:
            retries += 1
        last[rid] = t                          # always move "previous" forward
    return retries

r = retry_count(10, ["r1", "r1", "r1", "r2", "r2"], [100, 105, 200, 300, 302])
print("retries  :", r)
assert r == 2

def keep_latest(timestamps, messages):         # Deduplicate Logs: Keep Latest
    best = {}
    for t, m in zip(timestamps, messages):
        if m not in best or t > best[m]:
            best[m] = t
    return ["%d|%s" % (t, m) for m, t in sorted(best.items(), key=lambda p: (p[1], p[0]))]

kl = keep_latest([30, 10, 20, 15, 20],
                 ["cache miss", "user login", "cache miss", "heartbeat", "user login"])
print("latest   :", kl)
assert kl == ["15|heartbeat", "20|user login", "30|cache miss"]
```

The naive version charges ann three times for r1 and bob twice for r2. The
journalled version applies each id once, and replaying the whole log again changes
nothing. The assert `again == once` is the definition of idempotency, executed.

### H. Writing the table yourself

**What changes.** The built-in map is forbidden, and the table is the answer.

**Why.** It tests whether you know what a hash table is: compute a home, handle
collisions, grow. [[p:apple-design-hashmap|Design Hash Map]] is this problem. Keys
are 0..10^6, so a direct-address array of 10^6 + 1 slots is also a legal answer, and
worth saying out loud before writing chaining. Chaining is the easier one to get
right; open addressing needs tombstones. Both are above.

### I. A hash table plus another structure (rare as a pure topic)

A hash map gives O(1) lookup and no order. Pair it with something that has order
and no lookup. A map plus a doubly linked list is an [[lru-cache]]. A map plus an
array gives "insert, delete, and pick a random element in O(1)". A map from window
contents to counts is a [[sliding-window]]. A rolling hash makes substrings keys in
O(1) per step ([[rolling-hash]]). A [[bloom-filter]] answers "have I seen it?" in a
few bits per item, at the price of occasional false yes. These have their own
chapters; here it is enough to know that "map plus X" is the usual answer to "I
need lookup *and* something else".

## Recognising it in a statement

In rough order of how much to trust them.

1. **You catch yourself writing a nested loop whose inner loop is a search.** "For
   each x, is there a y with property P?" where P pins y down to one value. This is
   the most reliable signal, and it comes from your own brute force, not from the
   statement.
2. **"distinct", "unique", "duplicate", "appears twice", "already seen", "first
   non-repeating".** Identity is the question, and identity is what a table indexes.
3. **"how many times", "frequency", "exactly once", "most common".** A count map.
4. **"group", "for each category", "anagram", "same pattern", "equivalent".** A
   canonical key. Spend your time on the key.
5. **A pair condition with a target: "sum to", "difference k", "a + k = b".** Solve
   for the partner and look it up.
6. **"retry", "duplicate request", "the same event may arrive more than once",
   "process each id once".** A journal keyed by the request id.
7. **Constraints: n up to 10^5 or 10^6 with values up to 10^9.** Too many for n², too
   sparse to index directly: hash. With values in 1..n and "O(1) extra space", the
   array is the table.

### Disguised forms

- **"Count pairs i < j with nums[j] - nums[i] = j - i."** Rewrite: nums[j] - j =
  nums[i] - i. The key is nums[x] - x, and the answer is, for each key, C(count, 2).
  The algebra that moves everything with i to one side and everything with j to the
  other is the insight.
- **"Is there a subarray with sum k?"** prefix[j] - prefix[i] = k, so look up
  prefix[j] - k among earlier prefixes ([[prefix-sums]]).
- **"Can the note be written from the magazine's letters?"** Count both, compare per
  letter.
- **"Two strings follow the same pattern."** A canonical key: replace each character
  by the index of its first appearance, so "egg" and "add" both become (0, 1, 1).

### Anti-signals: looks like hashing, is not

- **The answer is about order: k-th smallest, closest, sorted output, ranges.**
  Sort, or use an ordered structure.
- **"Subarray", "consecutive" with a non-sum condition** like "longest with at most
  k distinct": this is a window; the map is only a helper.
- **The input is sorted.** Two pointers, O(1) space.
- **"Prefix"** in the sense of word prefixes: a trie.

## Traps

**1. Storing before looking up.** Symptom: an element pairs with itself;
[3, 2, 4] with target 6 returns [0, 0]. Demonstrated above. Habit: say "look up the
past, then join it".

**2. `x in some_list`.** Symptom: correct and Θ(n²), a time-out on the big case
only. Use a set.

**3. Emptying a slot on delete in open addressing.** Symptom: a key you never
touched becomes unfindable after an unrelated delete. Write a tombstone.

**4. A key that is not hashable, or not stable.** Symptom: `TypeError: unhashable
type: 'list'`, or worse, an object you mutated after storing it that is now in the
dict and not findable. Convert to a tuple; never mutate a stored key.

**5. Reading a `defaultdict` to test membership.** Symptom: the number of distinct
keys grows during a loop that only reads. `d[k]` on a defaultdict *inserts* k. Use
`k in d` or `d.get(k)`.

**6. Equal values that look different.** In Python `1 == 1.0 == True`, so they are
one key. Symptom: three "different" keys collapse into one. Usually harmless, and
very confusing when it is not.

**7. Forgetting `abs` in sign marking.** Symptom: wrong answers with no error,
because a negative index reads from the end of the list.

**8. Expecting the map to supply order.** Python dicts keep insertion order, which
is a real guarantee, and it is not sorted order and not "order of last update".
Symptom: the right groups in the wrong order. If the output order matters, take it
from the input scan or sort at the end.

**9. Keying on the wrong thing.** Symptom: groups merged or split, retries counted as
new requests, two purchases counted as one. Check both properties: equal things,
equal keys; different things, different keys.

**10. Forgetting the key's cost.** Symptom: a time-out with long strings. Build cheap
keys (counts instead of sorted strings), and count total characters, not items.

Traps 3 to 7, run:

```python run
from collections import defaultdict
EMPTY, TOMB = None, "tomb"

def insert(t, k):
    i = k % len(t)
    while t[i] is not EMPTY:
        i = (i + 1) % len(t)
    t[i] = k

def lookup(t, k):
    i = k % len(t)
    for _ in range(len(t)):
        if t[i] is EMPTY:
            return False                       # an empty slot ends the run
        if t[i] == k:
            return True
        i = (i + 1) % len(t)
    return False

for tombstone in (False, True):
    t = [EMPTY] * 8
    for k in (12, 20, 5, 28, 13):
        insert(t, k)
    t[t.index(20)] = TOMB if tombstone else EMPTY   # delete 20
    print("delete 20 by %-9s %s  lookup(28) = %s"
          % ("tombstone" if tombstone else "blanking", t, lookup(t, 28)))
    assert lookup(t, 28) is tombstone          # blanking cut 28 off from home

d = defaultdict(int)
for w in ["a", "b"]:
    d[w] += 1
if d["zzz"] == 0:                              # a READ that inserts
    pass
print("defaultdict after a read:", dict(d))
assert len(d) == 3

try:
    {[1, 2]: "x"}
except TypeError as e:
    print("list as key ->", e)
assert {(1, 2): "x"}[(1, 2)] == "x"            # a tuple is the fix

same = {1: "int", 1.0: "float", True: "bool"}
print("1, 1.0, True as keys ->", same)
assert len(same) == 1                          # equal values, one key

a = [0, 2, 1, 1]                               # values 1..3, index 0 unused
i = a[1]; a[i] = -a[i]                         # mark 2: a[2] becomes -1
v = a[2]                                       # read a marked cell: v = -1
print("forgot abs(): a[%d] silently reads a[-1] =" % v, a[v])
assert a[v] == a[3]                            # Python wraps; no error raised
```

## What to memorise

The template, the complement form, since every other shape is a small edit of it:

```python
seen = {}                          # key -> what you must return later
for j, x in enumerate(nums):
    key = target - x               # write the key down as an expression
    if key in seen:                # look up the past ...
        return [seen[key], j]
    seen[x] = j                    # ... then join it
```

Set instead of map when you only need yes or no. Counter when you need how many.
A tuple signature when you are grouping. A list indexed by the key when keys are
small. The input array itself when values are 1..n and space is tight.

The question that finds it: **what is the inner loop searching for, and could I
look it up by name instead?**

The habit: before typing, write three things: the key, the value, and whether the
lookup comes before the store.

The numbers: expected O(1) per operation, amortised over doubling resizes; a chain
averages α = n/m keys; open addressing costs about 1/(1 - α) probes, so 2 at half
full and 10 at 90%; a key of length L costs Θ(L) to hash; the worst case is Θ(n)
per operation for every hash table.

## Check yourself

:::check
Hand trace. nums = [2, 11, 5, 7, 15], target 12. Run the one-pass Two Sum with
"look up, then store". Write the map before each lookup and the answer. Then run
"store, then look up" on nums = [6, 1, 5], target 12, and say what it returns and
why.
--
| j | x | need | map at lookup | hit |
|---|---|---|---|---|
| 0 | 2 | 10 | {} | no, store 2:0 |
| 1 | 11 | 1 | {2: 0} | no, store 11:1 |
| 2 | 5 | 7 | {2: 0, 11: 1} | no, store 5:2 |
| 3 | 7 | 5 | {2: 0, 11: 1, 5: 2} | **yes, 2** |

Answer [2, 3]: 5 + 7 = 12.

Store first on [6, 1, 5]: j = 0 stores 6:0, then needs 12 - 6 = 6, finds it at 0,
and returns [0, 0]. The 6 paired with itself. The right order would find no pair at
all here (6+1, 6+5 and 1+5 are 7, 11 and 6), so the wrong version has invented an
answer that does not exist.
:::

:::check
Hand trace. A chained table with m = 5 and h(v) = v. Insert 10, 3, 15, 8, 20 in
that order. Draw the chains. How many comparisons do get(20), get(8) and get(25)
make? Then the table doubles to m = 10: draw it again.
--
Homes mod 5: 10 -> 0, 3 -> 3, 15 -> 0, 8 -> 3, 20 -> 0.

| slot | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| chain | [10, 15, 20] | [] | [] | [3, 8] | [] |

get(20): slot 0, compare 10, 15, 20: 3 comparisons. get(8): slot 3, compare 3, 8:
2. get(25): slot 0, compare 10, 15, 20, none match: 3, absent.

After doubling, homes mod 10: 10 -> 0, 3 -> 3, 15 -> 5, 8 -> 8, 20 -> 0. Chains:
slot 0 [10, 20], slot 3 [3], slot 5 [15], slot 8 [8]. The chain at slot 0 is still
two long because 10 and 20 differ by 10 = m, the h(v) = v weakness from trace 2.
:::

:::check
Why does Longest Consecutive Sequence run in O(n) even though it has a while loop
inside a for loop? What single line is responsible, and what does the code cost
without it on the input [1, 2, 3, ..., n]?
--
The line `if x - 1 in s: continue`. It lets the while loop start only at values
that begin a run. Every value belongs to exactly one run and is stepped over once by
that run's walk, so all walks together take at most n steps, plus n membership
checks for x - 1. Total O(n).

Without the line, every value starts a walk to the end of its run. On 1..n the walk
from x takes n - x steps, so the total is (n-1) + (n-2) + ... + 0 = n(n-1)/2:
quadratic. The set did not change; what changed is that the same run was walked
from every one of its members.
:::

:::check
Someone says: "Group Anagrams with `key = ''.join(sorted(word))` is O(n), because
dictionary operations are O(1)." Where are they wrong, and what is the cost of the
two keys?
--
They count the dictionary operations and forget the key. Building
`''.join(sorted(word))` sorts the letters, Θ(L log L) for a word of length L, and
hashing the resulting string is another Θ(L). So the total is Θ(sum of L log L)
over the words, not O(n).

The 26-count key costs Θ(L) to build (one pass over the letters) plus Θ(26) to hash
the tuple, so Θ(total characters + 26n). Both keys are correct (equal exactly for
anagrams); the count key is cheaper, which is why the bank's version of the problem
asks for it.
:::

:::check
Someone says: "My one-pass Two Sum built the whole map first and passed all the
samples, including [5, 5] with target 10, so it is fine." Find an input where it
fails, and explain why the sample passed.
--
[3, 2, 4] with target 6. The map built first is {3: 0, 2: 1, 4: 2}. Position 0 needs
6 - 3 = 3, finds where[3] = 0, and returns [0, 0]: the 3 used twice. The right
answer is [1, 2].

The sample passed by luck. Building {5: 0} and then {5: 1}, the comprehension kept
the last index of 5, so position 0 found index 1, a different position holding the
same value. Any input where target is exactly twice a value that appears once
breaks it. The map must contain only positions strictly before the current one at
the moment of the lookup.
:::

:::check
Reduce this disguised problem. "Given nums, count the pairs i < j with
nums[j] - nums[i] = j - i." Do the algebra, name the key, and give the answer for
nums = [3, 1, 4, 5, 1, 7].
--
Move each index to the side of its own value: nums[j] - j = nums[i] - i. So two
positions pair exactly when they have the same value of nums[x] - x. That is the
key. Count the keys and add C(c, 2) for each count c; or, in one pass, add
`cnt[key]` before incrementing it (look up, then store).

Keys: 3-0 = 3, 1-1 = 0, 4-2 = 2, 5-3 = 2, 1-4 = -3, 7-5 = 2. Counts: {3: 1, 0: 1,
2: 3, -3: 1}. Answer C(3, 2) = 3: the pairs (2, 3), (2, 5), (3, 5). Check one:
nums[5] - nums[2] = 7 - 4 = 3 = 5 - 2.
:::

:::check
Hand trace the sign-marking duplicate finder on [3, 1, 3, 4, 2]. Write the array
after each step. Then explain why the values must be at least 1 for the trick to
work.
--
Step 1: v = 3, cell 3 holds 4, mark: [3, 1, 3, -4, 2].
Step 2: v = 1, cell 1 holds 1, mark: [3, -1, 3, -4, 2].
Step 3: v = 3, cell 3 holds -4, already negative: **the answer is 3**.

The mark is "this cell is negative". If a value could be 0, cell 0 holding 0 could
not be made negative, so "seen 0" could not be recorded. And a value that was
negative to begin with would look already marked. The trick needs every value to
be a positive number whose sign is free to use, and every value to be a valid index.
:::
