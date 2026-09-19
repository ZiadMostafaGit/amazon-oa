# Hash Tables

> A hash table is not a dictionary that happens to be fast. It is an ordinary
> array whose index you *compute from the key*, plus a written-down plan for
> what to do when two different keys compute the same index — and every bug,
> every cost and every design choice in it lives in that plan.

## When you reach for it

You reach for a hash table when the question you keep asking is *have I seen
this key before, and what is attached to it?* — and you do not care what order
the keys come back in.

That question is so common that this is the most used topic in the collection
after the two most generic ones: **957 of the problems here touch it, which is
#3 of 150**. It is worth seeing the shapes it arrives in, because they are only
about six, and once you can name them the code writes itself.

- **Membership and de-duplication.** *Deduplicate Logs: Keep First*,
  *Filter Duplicates While Preserving Order*, *Distinct Duplicate Values*. A set
  is a map whose values you never read.
- **Counting.** *Count Values Appearing Exactly Once*, *First Non-Repeating
  Character*, *First User to Log In Exactly Once*, *Request Retry Count*. The
  key is the thing, the value is a tally. This has its own chapter:
  [[frequency-counting]].
- **Association.** *Design Hash Map*, *Account Balance Manager Part 1 -
  Calculate Totals*, *Dynamic Path Accessor*. A key names a mutable cell.
- **Grouping by a derived key.** *Aggregate Values by Letter* groups by first
  letter; *Case-Preserving Dictionary Autocorrect* groups by the lowercased
  spelling while keeping the original. The interesting work is choosing the key,
  not using the table.
- **Complement lookup.** *All Pairs with Target Sum*: for each `x`, ask whether
  `target - x` has been seen. This is the trick that turns an `O(n²)` double
  loop into one pass.
- **Following links.** *Find the Root of a Directed Tree* and *Initial and Final
  Accounts in a Transfer Chain* both build a `child -> parent` map and then ask
  which key is never on the right-hand side.

And there is a seventh shape that is really a systems question wearing an
interview costume, which this chapter also has to cover: **idempotency and
retries**. A client sends a request, the network eats the reply, the client
sends it again. *Request Retry Count* and *Identify Broken Customer
Transactions* are that story. The cure is always a hash table keyed by a stable
request identifier, and the interesting part is choosing the key.

The tool is wrong when the question is secretly about *order*. If you need the
k-th smallest key, the next key above a value, a range, or the keys in sorted
order, a hash table has thrown exactly that information away and you want
[[ordered-set]] or [[balanced-bst]]. If you need to match by *prefix*, you want a
[[trie]]. If the keys are already a dense range `0 .. n-1`, an array is a hash
table with the identity hash and no collisions — faster, smaller and impossible
to get wrong; see [[cyclic-sort]] and [[counting-sort]]. And if the input is
already sorted, as in *Deduplicate a Sorted Array In Place*, duplicates are
adjacent and [[two-pointers]] solves it in `O(1)` space while the hash table
solution allocates a set it did not need.

## The idea

**Do not search for the key. Compute where it would be.**

Everything else follows. An array gives you `a[i]` in one step because the
address is arithmetic: base plus `i` times the element size. A hash table keeps
that property for keys that are not small integers by inserting one step in
front: run the key through a function `h` that produces an integer, reduce it
modulo the table size `m`, and call that the key's **home slot**. To find a key
you go straight to its home slot. You never scan.

The catch is counting. There are more possible keys than slots — usually
astronomically more; *Design Hash Map* allows a million distinct keys and you
would like a table of a few hundred. By the pigeonhole principle some pair of
keys must share a home slot. Collisions are not a rare accident to be engineered
away; they are a certainty, and the whole design is the answer to one question:
**when I arrive at an occupied slot, where do I look next?**

There are two answers, and they are the two families of hash table.

- **Chaining.** Each slot holds a list of the entries that landed there. Lookup
  hashes, then scans that one short list.
- **Open addressing.** Every entry lives in the table itself. If the home slot is
  taken, follow a deterministic **probe sequence** — with linear probing, simply
  the next slot, wrapping around — until you find the key or an empty slot.

<svg viewBox="0 0 690 190" role="img" aria-label="three keys hashed by k mod 8 to the same home slot 4, placed in the first free slots to its right">
  <g>
    <text x="16" y="46">12</text>
    <text x="16" y="82">20</text>
    <text x="16" y="118">28</text>
    <line x1="46" y1="40" x2="96" y2="72"/>
    <line x1="46" y1="76" x2="96" y2="80"/>
    <line x1="46" y1="112" x2="96" y2="88"/>
    <rect x="100" y="58" width="120" height="44" rx="6"/>
    <text x="114" y="86">k mod 8</text>
    <line x1="220" y1="80" x2="286" y2="80"/>
    <line x1="286" y1="80" x2="274" y2="73"/>
    <line x1="286" y1="80" x2="274" y2="87"/>
    <text x="238" y="70">home = 4</text>
    <rect x="290" y="58" width="45" height="44"/>
    <rect x="335" y="58" width="45" height="44"/>
    <rect x="380" y="58" width="45" height="44"/>
    <rect x="425" y="58" width="45" height="44"/>
    <rect class="fill" x="470" y="58" width="45" height="44"/>
    <rect x="515" y="58" width="45" height="44"/>
    <rect x="560" y="58" width="45" height="44"/>
    <rect x="605" y="58" width="45" height="44"/>
    <text x="482" y="86">12</text>
    <text x="527" y="86">20</text>
    <text x="572" y="86">28</text>
    <text x="308" y="126">0</text>
    <text x="353" y="126">1</text>
    <text x="398" y="126">2</text>
    <text x="443" y="126">3</text>
    <text x="488" y="126">4</text>
    <text x="533" y="126">5</text>
    <text x="578" y="126">6</text>
    <text x="623" y="126">7</text>
    <text x="290" y="160">one home slot, three keys, one contiguous run to walk</text>
  </g>
</svg>

The number that governs both families is the **load factor**, `α = n / m`: how
full the table is. Chaining's average chain length is `α`. Open addressing's run
lengths blow up as `α` approaches 1. So a hash table is not a static structure;
it is a structure that **grows**, doubling `m` and re-inserting everything
whenever `α` crosses a threshold. That resize is what "O(1)" is really hiding,
and it is why the honest statement is *amortised expected O(1)* — three
qualifiers, all of them earned.

## Worked by hand

Take an eight-slot table, `h(k) = k mod 8`, linear probing, and insert
`12, 20, 5, 28, 13` in that order. Empty slots are `.`.

| step | key | home | probes walked | lands at | table after |
| --- | --- | --- | --- | --- | --- |
| 1 | 12 | 4 | 4 (free) | 4 | `. . . . 12 . . .` |
| 2 | 20 | 4 | 4 (12), 5 | 5 | `. . . . 12 20 . .` |
| 3 | 5 | 5 | 5 (20), 6 | 6 | `. . . . 12 20 5 .` |
| 4 | 28 | 4 | 4 (12), 5 (20), 6 (5), 7 | 7 | `. . . . 12 20 5 28` |
| 5 | 13 | 5 | 5 (20), 6 (5), 7 (28), 0 | 0 | `13 . . . 12 20 5 28` |

Five keys, eight slots, `α = 0.625`. Now look up 28: start at 4, see 12, see 20,
see 5, find 28 at slot 7. **Four probes to find a key in a table that is only
five-eighths full.** Nothing went wrong; this is simply what linear probing
does.

Now delete 20 the obvious way — blank slot 5 — and look up 28 again. Start at 4,
see 12, arrive at slot 5, find it empty, and conclude that 28 is not in the
table. It is sitting untouched at slot 7.

<svg viewBox="0 0 660 230" role="img" aria-label="looking up key 28 after deleting key 20, with a blanked slot versus a tombstone">
  <g>
    <text x="14" y="52">blank</text>
    <rect x="140" y="26" width="70" height="42"/>
    <rect x="210" y="26" width="70" height="42"/>
    <rect x="280" y="26" width="70" height="42"/>
    <rect x="350" y="26" width="70" height="42"/>
    <text x="163" y="54">12</text>
    <text x="303" y="54">5</text>
    <text x="369" y="54">28</text>
    <text x="168" y="88">4</text>
    <text x="238" y="88">5</text>
    <text x="308" y="88">6</text>
    <text x="378" y="88">7</text>
    <line x1="175" y1="18" x2="245" y2="18"/>
    <line x1="245" y1="18" x2="233" y2="12"/>
    <line x1="245" y1="18" x2="233" y2="24"/>
    <text x="440" y="54">empty slot: stop, report absent</text>
    <text x="14" y="166">tomb</text>
    <rect x="140" y="140" width="70" height="42"/>
    <rect class="fill" x="210" y="140" width="70" height="42"/>
    <rect x="280" y="140" width="70" height="42"/>
    <rect x="350" y="140" width="70" height="42"/>
    <text x="163" y="168">12</text>
    <text x="303" y="168">5</text>
    <text x="369" y="168">28</text>
    <text x="168" y="202">4</text>
    <text x="238" y="202">5</text>
    <text x="308" y="202">6</text>
    <text x="378" y="202">7</text>
    <line x1="175" y1="132" x2="385" y2="132"/>
    <line x1="385" y1="132" x2="373" y2="126"/>
    <line x1="385" y1="132" x2="373" y2="138"/>
    <text x="440" y="168">marked, not empty: walk on, find 28</text>
  </g>
</svg>

Three things the trace shows that the code does not.

**The cost is about runs, not about fullness.** Step 5's key 13 walked four
slots even though three slots were free the whole time, because it started
inside the run that 12, 20, 5 and 28 had built. Linear probing makes runs merge:
two neighbouring clusters that touch become one long one, and the longer a run
gets the more likely a new key lands in it. This is *primary clustering*, and it
is the reason nobody runs open addressing above half full.

**A key's position depends on the whole insertion history.** Key 5 is not at
slot 5. If you had inserted `5` first it would be, and 20 would be elsewhere. So
you cannot reason about a slot in isolation; you can only reason about probe
sequences.

**Deletion is not the inverse of insertion.** This is the deep one. Insertion
maintained a property that spans several slots — *everything between a key's
home and its actual position is occupied* — and blanking a slot breaks that
property for keys that were never touched. The fix is to write a **tombstone**:
a marker that means "occupied once, keep walking", which lookups pass through
and insertions may overwrite. Keep that in mind, because the correctness proof
is exactly the statement that this multi-slot property is never broken.

## Why it is correct

State the representation invariant first. Notice that it is not a property of a
single slot — it is a property of a *path*.

:::proof An open-addressed table answers exactly the operations performed on it
**State.** An array `slot[0 .. m-1]`, each entry being `EMPTY`, `TOMB`, or a live
pair `(k, v)`. Counters: `live` = number of live pairs, `used` = number of
non-`EMPTY` slots. The probe sequence of a key is
`p(k, i) = (h(k) + i) mod m` for `i = 0, 1, 2, …`.

**Invariant.**

- **(I1)** For every live entry `(k, v)` at index `j`, if `j = p(k, t)` is the
  first occurrence of `j` in `k`'s probe sequence, then `slot[p(k, i)]` is
  non-`EMPTY` for every `i < t`. ("No empty slot separates a key from its
  home.")
- **(I2)** No key occurs in two live entries.
- **(I3)** `used < m`: at least one slot is `EMPTY`.

**Lemma (the walk decides).** Define `scan(k)`: walk `p(k, 0), p(k, 1), …`,
return the index on a key match, stop and report *absent* at the first `EMPTY`.
Because step 1 makes `p(k, ·)` a cyclic permutation of all `m` indices, and by
(I3) some slot is `EMPTY`, the walk halts within `m` steps. If `k` is live at
`j = p(k, t)`, then by (I1) no `EMPTY` appears before step `t`, so the walk
reaches `j` and returns it; by (I2) it cannot have matched some other copy of
`k` earlier. If `k` is not live, no index it visits holds `k`, so it reports
absent. So `scan` is correct in both directions — *given the invariant*.

**Base case.** A fresh table is all `EMPTY` with `live = used = 0`. (I1) and (I2)
are vacuous, and (I3) holds because `m ≥ 1`.

**`get(k)`** performs `scan` and writes nothing, so the invariant is trivially
preserved and by the lemma the answer is right.

**`put(k, v)`** runs `scan(k)`, remembering `f`, the index of the first `TOMB`
seen (if any). *It does not stop at that tombstone.* Two cases.

*The scan found `k` at `j`.* Overwrite `slot[j] = (k, v)`. No slot changes its
`EMPTY`/non-`EMPTY` status and no key set changes, so (I1)–(I3) hold, and the
stored value is the latest one.

*The scan reported absent, stopping at `EMPTY` index `e`.* Write the pair at
`f` if a tombstone was seen, otherwise at `e`; call it `d`. For the new entry,
every earlier index in `k`'s probe sequence was non-`EMPTY` when the scan passed
it, and `d ≤ e` in probe order, so (I1) holds for `k`. For every *other* live
entry, note that this write turns `EMPTY → pair` or `TOMB → pair`: it never
makes a slot `EMPTY`. A condition of the form "these slots are non-`EMPTY`" can
only become more true, so (I1) survives for everyone. (I2) holds because the
scan ran all the way to an `EMPTY` and found no `k`. (I3) is restored by the
resize rule below.

**`remove(k)`** runs `scan(k)` and, on a hit at `j`, writes `slot[j] = TOMB`. The
slot does not become `EMPTY`, so no other key's (I1) is disturbed — this is
precisely the step that blanking gets wrong. `k` is no longer live, so (I2) still
holds, and `used` is unchanged so (I3) holds.

**`rehash(m')`** collects the live pairs, allocates `m'` `EMPTY` slots with
`m' > live`, and inserts each pair at the first `EMPTY` index of its new probe
sequence. Each insertion establishes (I1) for its own key by construction and
cannot falsify anyone else's, (I2) holds because the collected keys were
distinct, and (I3) holds because `m' > live` leaves a gap. `put` calls `rehash`
whenever `used + 1` would reach `m / 2`, so (I3) is never violated.

**Conclusion.** Every operation preserves (I1)–(I3), the invariant holds
initially, and by the lemma `get(k)` returns the value of the most recent
`put(k, ·)` not followed by a `remove(k)`, and the absent marker otherwise. ∎
:::

Now the assumptions, because that is where the bugs are.

- **`k1 == k2` implies `h(k1) == h(k2)`.** The proof reads "the walk visits `k`'s
  probe sequence" as if the key determined the sequence. If two equal keys hash
  differently, one of them is unreachable and (I2) silently fails. The converse
  is harmless: unequal keys may share a hash, that is just a collision.
- **The key does not change while it is in the table.** Same clause, in time
  rather than in space. Mutate a key after insertion and its probe sequence moves
  while its entry does not.
- **Equality is reflexive.** `x == x` must be true, or the entry cannot even find
  itself. Floating-point `NaN` fails this, which is why a `NaN` key is a
  write-only key.
- **The probe sequence is a permutation of all `m` slots and is identical in
  `put`, `get` and `remove`.** Linear probing gives this for free. A stride `g`
  needs `gcd(g, m) = 1`; double hashing needs the secondary hash to be non-zero
  and coprime to `m`.
- **There is always an `EMPTY` slot.** Drop (I3) and a lookup for an absent key
  circles the table forever. This is why the resize check comes *before* the
  insert, not after.
- **`h` is deterministic for the lifetime of the table.** Per-process random
  seeding is fine; a hash persisted to disk and compared against a freshly seeded
  one is not.

And one thing the proof conspicuously never mentions: **speed**. Nothing above
assumed the hash spreads keys well. A table whose `h` returns `0` for everything
satisfies every clause and answers every query correctly, in `Θ(n)` per
operation. Correctness and performance are separate arguments here, which is why
a hash-table bug that produces *wrong answers* is never a bad hash function and
always a broken key contract.

:::note Chaining satisfies a simpler invariant
For chaining, (I1) collapses to "every live entry sits in the bucket list
`h(k) mod m`" and (I3) disappears entirely. That is the whole reason chaining
tolerates `α > 1` and needs no tombstones: deletion is a list removal, and it
cannot break a property that spans slots because no property spans slots. Open
addressing buys cache locality and pays for it with this invariant.
:::

## What it costs

Assume **simple uniform hashing**: each key is equally likely to hash to any of
the `m` slots, independently of the others. It is a modelling assumption, not a
fact, and the last part of this section is about what happens when it fails.

**Chaining, unsuccessful search.** Let `X_j` be 1 if key `j` hashes to the slot
we are searching. The chain length is `Σ_j X_j`, and `E[X_j] = 1/m`, so by
linearity the expected chain length is `n/m = α`. Total expected cost:
`1 + α` — one hash plus a scan of `α` entries on average.

**Chaining, successful search.** Average over the `n` keys, in insertion order.
When key `i` (0-indexed) was appended, the expected number of keys already in
its chain was `i/m`, and a successful search for it walks past exactly those.
So the expected probes are

```
1 + (1/n) · Σ_{i=0}^{n-1} i/m  =  1 + (n-1)/(2m)  =  1 + α/2 − α/(2n)
```

Both are `Θ(1 + α)`. Keep `α` bounded by a constant and both are `Θ(1)`.

**Open addressing, unsuccessful search.** Let `X` be the number of probes. The
walk takes at least `i` probes only if the first `i − 1` slots it touched were
occupied, which has probability

```
(n/m) · ((n-1)/(m-1)) · … · ((n-i+2)/(m-i+2))  ≤  α^(i-1)
```

since `(n - t)/(m - t) ≤ n/m` whenever `n ≤ m`. Using
`E[X] = Σ_{i≥1} P(X ≥ i)`,

```
E[X]  ≤  Σ_{i≥1} α^(i-1)  =  1/(1 − α)
```

That geometric series is the single most useful number in the topic:

| α | 0.5 | 0.75 | 0.9 | 0.95 | 0.99 |
| --- | --- | --- | --- | --- | --- |
| expected probes | 2 | 4 | 10 | 20 | 100 |

Half full costs two probes. Ninety-nine percent full costs a hundred. The cost
is not linear in fullness, it explodes at the end — which is why real libraries
resize somewhere between half and three-quarters full, and why the
implementation below resizes at `α = 1/2`.

**The resize is amortised away.** Growing costs `Θ(m)` work: every live entry is
rehashed. But if the table doubles each time, then inserting `n` keys from empty
triggers rehashes at sizes `m₀, 2m₀, 4m₀, …`, and the total rehash work is

```
m₀ + 2m₀ + 4m₀ + … + m_final  <  2 · m_final  =  O(n)
```

because a geometric series is dominated by its last term. Spread over `n`
inserts, that is `O(1)` amortised each — the same aggregate argument as a
growable array, treated properly in [[amortized-analysis]]. Note what the
argument needs: the table must grow by a constant *factor*. Grow by a constant
*amount* and the series becomes `Θ(n²/c)`.

**Tombstones need their own trigger.** A workload that alternates `put` and
`remove` keeps `live` small while `used` climbs, and lookups slow to a crawl
walking through markers. So the resize test must read `used`, not `live`, and
the new capacity must be chosen from `live`. A table can therefore rehash to a
*smaller* size, which surprises people.

**The cost everyone forgets is the hash itself.** `O(1)` counts *probes*, not
work. Hashing a string of length `L` is `Θ(L)`, and so is the equality check on
every collision. A map keyed by hundred-character words does hundreds of bytes
of work per lookup; *Case-Preserving Dictionary Autocorrect* bounds the total
dictionary at 9500 characters precisely because the honest complexity is
`O(total characters)`, not `O(number of words)`. The same applies to tuple keys,
frozen sets, and any key you build by concatenating strings inside a loop.

**Space.** Chaining: `m` slot pointers plus `n` nodes, each with a next pointer —
the pointer overhead often exceeds the payload. Open addressing: `m` slots of
which `(1 − α)·m` are deliberately empty, so at `α = 1/2` you are paying double
for the entries alone. Either way a hash table costs several times what the same
data costs in a flat array, which matters when the keys are `0 .. n-1` and an
array would have done.

**Worst case.** `Θ(n)` per operation, always, for every hash table. If `n` keys
share a hash, chaining degenerates to one linked list and open addressing to one
long run, and building the table costs `Θ(n²)`. This is not hypothetical: an
attacker who knows your hash function can generate colliding keys on purpose
(*hash flooding*), which is why modern runtimes seed their string hash randomly
per process — a [[randomized-algorithms]] answer to an adversary. The
non-adversarial version bites too: `h(k) = k mod 2^b` uses only the low bits, so
keys that are all multiples of 8 collapse into an eighth of the table. See
[[hash-functions]].

## The implementation

This is *Design Hash Map* — integer keys, integer values, `get` returns `-1` for
an absent key, and the storage is built by hand — written as the invariant
describes it.

```python run
import random

EMPTY, TOMB = None, ("tombstone",)


class HashMap:
    """Open addressing, linear probing, tombstones on delete, load factor <= 1/2."""

    def __init__(self, cap=8):
        self.slots = [EMPTY] * cap
        self.live = 0                       # real entries
        self.used = 0                       # entries + tombstones = non-EMPTY slots

    def _probe(self, key):
        m = len(self.slots)
        i = hash(key) % m
        for _ in range(m):
            yield i
            i = (i + 1) % m                 # step 1 visits every slot exactly once

    def _lookup(self, key):
        """(index holding key, or None) and (index we may write to)."""
        free = None
        for i in self._probe(key):
            e = self.slots[i]
            if e is EMPTY:
                return None, (i if free is None else free)
            if e is TOMB:
                free = i if free is None else free
            elif e[0] == key:
                return i, i
        return None, free

    def _rehash(self):
        entries = [e for e in self.slots if e is not EMPTY and e is not TOMB]
        m = 8
        while m < 4 * (len(entries) + 1):
            m *= 2
        self.slots = [EMPTY] * m
        self.live = self.used = len(entries)
        for e in entries:
            for i in self._probe(e[0]):
                if self.slots[i] is EMPTY:
                    self.slots[i] = e
                    break

    def put(self, key, value):
        if (self.used + 1) * 2 > len(self.slots):
            self._rehash()
        at, free = self._lookup(key)
        if at is not None:
            self.slots[at] = (key, value)
            return
        if self.slots[free] is EMPTY:
            self.used += 1
        self.live += 1
        self.slots[free] = (key, value)

    def get(self, key, default=-1):
        at, _ = self._lookup(key)
        return default if at is None else self.slots[at][1]

    def remove(self, key):
        at, _ = self._lookup(key)
        if at is None:
            return False
        self.slots[at] = TOMB
        self.live -= 1
        return True


h = HashMap()
for k in (12, 20, 5, 28, 13):
    h.put(k, k * 10)
print("after 5 puts: capacity", len(h.slots), "live", h.live)
print("get(28) ->", h.get(28), "  get(99) ->", h.get(99))
assert h.get(28) == 280 and h.get(99) == -1
h.remove(20)
print("after remove(20): get(20) ->", h.get(20), " get(28) ->", h.get(28))
assert h.get(20) == -1 and h.get(28) == 280      # the tombstone kept 28 reachable

rng = random.Random(3)
mine, ref = HashMap(), {}
for _ in range(20000):
    k, v, op = rng.randrange(60), rng.randrange(1000), rng.random()
    if op < 0.45:
        mine.put(k, v)
        ref[k] = v
    elif op < 0.65:
        assert mine.remove(k) == (ref.pop(k, None) is not None)
    else:
        assert mine.get(k) == ref.get(k, -1), k
    assert mine.live == len(ref)
print("20000 random ops agree with dict; final live", mine.live, "capacity", len(mine.slots))
```

Four lines carry the argument.

`i = (i + 1) % m` inside `_probe` is the probe sequence, and writing it as a
generator means `put`, `get` and `remove` physically cannot disagree about it.
The proof's lemma assumed they walk the same path; make that structural rather
than remembered.

`_lookup` returns two indices, and the reason is subtle: it must keep scanning
past the first tombstone. Stopping there would be faster and would break (I2) —
if the key already lives further down the run, you would insert a second copy of
it and every later `get` would return whichever the scan met first. Remember the
tombstone, keep walking, decide at the end.

`self.slots[at] = TOMB` in `remove`, rather than `EMPTY`, is the entire deletion
story, and the assert two lines above the random test is there to make the
consequence visible.

`if (self.used + 1) * 2 > len(self.slots)` reads `used`, so tombstones count
toward the resize trigger, while `_rehash` sizes the new table from the number
of *live* entries. A delete-heavy table therefore rebuilds itself at a sensible
size instead of growing forever.

:::note Why the random cross-check is the real test
The hand-written cases test the cases you thought of. Twenty thousand random
operations against `dict` test the ones you did not — in particular the
interleavings of `remove` and `put` that put a live key behind a tombstone. Any
hash table you write should be tested this way; it is the cheapest bug-finder in
this chapter. See [[testing-your-code]].
:::

## Variants you will meet

**Set instead of map.** Same structure, no value. Use it for membership and
de-duplication: *Filter Duplicates While Preserving Order* is `seen` plus an
output list; *Intersection of Two Lists* is one set and one scan.

**Counter.** Value is a tally. *First Non-Repeating Character* counts in one
pass, then rescans the original sequence in order to find the first key with
count 1 — the second pass is over the input, not the map, because the map has no
order to offer. Full treatment in [[frequency-counting]].

**Grouping by a canonical key.** Map `key(x) -> list of x`. The whole art is in
`key`: lowercase for *Case-Preserving Dictionary Autocorrect*, first letter for
*Aggregate Values by Letter*, the sorted letters for anagram grouping
([[anagrams]]).

**Complement lookup.** *All Pairs with Target Sum*: one pass, for each `x`
check whether `target - x` is in the map of what you have already seen. Note it
must be *already seen*, or you pair an element with itself.

**Chaining vs open addressing vs Robin Hood.** Chaining survives high load and
easy deletion; open addressing is cache-friendly; Robin Hood hashing reorders
entries so no key sits much further from home than its neighbours, flattening
the probe-length distribution. Double hashing replaces the `+1` step with a
second hash of the key, which removes primary clustering. All of it is
[[hash-functions]] territory.

**Hash map plus another structure.** A hash map gives `O(1)` lookup and no
ordering, so pair it with something that has ordering and no lookup. Map plus
doubly linked list is an [[lru-cache]]; map plus array is "insert, delete and
random element in `O(1)`"; map plus [[heap]] is a priority queue with decrease-key.
This composition is most of [[design-data-structure]].

**Interning.** Map each distinct object to a small integer so that array-based
structures can hold it. That is how string-keyed problems get fed to
[[union-find]] or to a graph adjacency list.

**Rolling hash.** Hash a sliding window in `O(1)` per step so substrings become
keys. See [[rolling-hash]] and [[string-matching]].

**Approximate membership.** If you can accept false positives and you need the
space, a [[bloom-filter]] answers "have I seen this?" in a few bits per element.

**Idempotency keys.** The systems variant, and the one this chapter owes you.

```python run
LOG = [("r1", "ann", -30), ("r2", "bob", -10), ("r1", "ann", -30),
       ("r3", "ann", +50), ("r2", "bob", -10), ("r1", "ann", -30)]


def apply_naive(records, balances):
    for _, user, delta in records:
        balances[user] = balances.get(user, 0) + delta
    return balances


def apply_once(records, balances, journal):
    """Apply each request id at most once, whatever the stream contains."""
    for rid, user, delta in records:
        if rid in journal:
            continue                      # a retry, not a second request
        journal.add(rid)
        balances[user] = balances.get(user, 0) + delta
    return balances


def dedup_keep_first(records):
    seen, out = set(), []
    for rec in records:
        if rec[0] not in seen:
            seen.add(rec[0])
            out.append(rec)
    return out


def dedup_keep_latest(records):
    last = {}
    for rec in records:
        last.pop(rec[0], None)            # drop the old position...
        last[rec[0]] = rec                # ...so the key lands at its latest one
    return list(last.values())


def retry_counts(records):
    n = {}
    for rec in records:
        n[rec[0]] = n.get(rec[0], 0) + 1
    return {rid: c - 1 for rid, c in n.items() if c > 1}


print("naive, one pass :", apply_naive(LOG, {"ann": 100, "bob": 100}))
print("naive, replayed :", apply_naive(LOG + LOG, {"ann": 100, "bob": 100}))

journal = set()
once = apply_once(LOG, {"ann": 100, "bob": 100}, journal)
print("journalled      :", once, " journal:", sorted(journal))
again = apply_once(LOG + LOG, dict(once), journal)
print("replayed again  :", again, "(unchanged)")
assert once == {"ann": 120, "bob": 90}
assert again == once, "replaying known ids must be a no-op"

print("keep first      :", [r[0] for r in dedup_keep_first(LOG)])
print("keep latest     :", [r[0] for r in dedup_keep_latest(LOG)])
print("retries per id  :", retry_counts(LOG))
assert [r[0] for r in dedup_keep_first(LOG)] == ["r1", "r2", "r3"]
assert [r[0] for r in dedup_keep_latest(LOG)] == ["r3", "r2", "r1"]
assert retry_counts(LOG) == {"r1": 2, "r2": 1}
```

An operation is **idempotent** when applying it twice has the same effect as
applying it once. `balances[user] += delta` is not; `if rid not in journal` makes
it so, by turning an unbounded stream of deliveries into a set of distinct
identifiers. The assert `again == once` is the definition, executed.

Two details in there are worth keeping. `dedup_keep_latest` pops before it
writes: a dictionary keeps a key at the position of its *first* insertion, so
without the `pop` you get the latest value at the earliest position — which is
right for *Deduplicate Logs: Keep Latest* only if the problem asks for the
original order, and wrong if it asks for the order of last appearance. Read that
sentence in the statement twice. And `retry_counts` subtracts one, because the
first delivery is not a retry; *Request Retry Count* is a counting problem whose
only difficulty is that off-by-one.

## Recognising it in a statement

In rough order of how much you should trust them.

1. **"distinct", "unique", "duplicate", "already seen", "first non-repeating".**
   Identity is the question, and identity is what a hash table indexes.
2. **A key-to-value association stated outright**, plus a sentinel for absence:
   "appends `-1` when the key is absent" in *Design Hash Map*, or "returns the
   value stored under the path" in *Dynamic Path Accessor*.
3. **"group by", "for each X, collect the Y"**, or an aggregation per category —
   *Aggregate Values by Letter*, *Account Balance Manager Part 1*.
4. **"how many times"**, "count occurrences", "exactly once", "at least twice" —
   *Count Values Appearing Exactly Once*, *First User to Log In Exactly Once*.
5. **Idempotency language**: "duplicate requests", "retries", "process each id
   once", "the same event may appear more than once". A journal keyed by the
   id is the whole solution.
6. **The constraints are asymmetric.** Keys up to `10^6` (or `10^9`) but at most
   `10^5` of them: the key space is too large to index directly and too sparse to
   sort profitably. *Design Hash Map* states exactly this shape.
7. **You catch yourself writing a nested loop whose inner loop is a search.**
   Almost every `O(n²)` scan for "is there another element with property P" is a
   hash table away from `O(n)`. See [[optimisation-path]].

Anti-signals — things that look like this and are not:

- **Order is part of the answer.** "k-th smallest", "next greater key", "all keys
  between a and b", "in sorted order". A hash table cannot help;
  [[ordered-set]] or sorting can.
- **The keys are a dense small range.** Twenty-six letters, or `0 .. n-1`. Use a
  list. It is faster, it has no hash, and *Validate 3x3 Digit Windows* — nine
  possible values — wants a bitmask or a small array, not a dict.
- **The input is sorted.** Duplicates are adjacent and pairs can be found by
  [[two-pointers]] in `O(1)` space. *Deduplicate a Sorted Array In Place* is
  about identity, but a set is the wrong implementation of it.
- **You need prefixes, not keys.** Autocomplete over prefixes is a [[trie]];
  *Case-Preserving Dictionary Autocorrect* only needs whole-word equality after
  case folding, which is why a map suffices there.
- **A worst-case guarantee is demanded.** Hash tables are expected-time
  structures. If the requirement is a hard bound per operation, you need a
  [[balanced-bst]].

## Traps

**Blanking a slot on delete.** Symptom: some key that you never touched becomes
invisible, and only after an unrelated deletion. Demonstrated below. Applies to
every open-addressed table you write by hand.

**Mutating a key after it is in the table.** Symptom: the key is visible in
`list(d)`, compares equal to your probe, and `probe in d` is `False`.
Demonstrated below. In Python, mutable types are unhashable to stop exactly this
— until you write `__hash__` yourself.

**Defining `__eq__` without `__hash__`.** Python then makes your class unhashable
(a clear failure) but if you write both and they disagree, the failure is silent:
two entries whose keys are equal. The contract is one-directional — equal implies
same hash — and it is your job.

**Values that are equal but look different.** In Python `1 == 1.0 == True`, so
`{1: "a", 1.0: "b", True: "c"}` is a single entry. Great for
*Median of Parsed Integer Strings* if you meant it, silently wrong if you were
keying on "the literal the user typed".

**Reading a `defaultdict` to test membership.** `d[k]` on a `defaultdict` *inserts*
`k`. Symptom: `len(d)` grows during a read-only loop and your count of distinct
keys is too high. Use `k in d` or `d.get(k)`.

**Mutating the dictionary while iterating it.** `RuntimeError: dictionary changed
size during iteration`, or, worse, a subtly wrong traversal if you iterate a
snapshot. Collect the keys to change first, then change them.

**Trusting insertion order as if it were sorted order.** Python preserves
insertion order, which is a genuine guarantee and tempting to over-read. It is
not sorted order, and it is not "order of last update" either — see the `pop`
trick above.

**Keying on the wrong thing for idempotency.** Deduplicating payments by
`(user, amount)` collapses two genuine identical purchases into one; deduplicating
by `(user, amount, timestamp)` fails to catch a retry that carries a new
timestamp. The key has to be an identifier the *client* generates once and
repeats on every retry. This is the entire design question behind
*Identify Broken Customer Transactions*.

**Assuming `O(1)` over the key length.** Covered in the cost section: a map keyed
by long strings is linear in the string, and building keys by concatenation in a
loop is quadratic.

```python run
EMPTY, TOMB = None, "tomb"


def insert(t, k):
    i = k % len(t)
    while t[i] is not EMPTY:
        i = (i + 1) % len(t)
    t[i] = k


def lookup(t, k):
    i, steps = k % len(t), 0
    while t[i] is not EMPTY and steps < len(t):
        if t[i] == k:
            return True
        i, steps = (i + 1) % len(t), steps + 1
    return False


def delete(t, k, tombstone):
    i, steps = k % len(t), 0
    while t[i] is not EMPTY and steps < len(t):
        if t[i] == k:
            t[i] = TOMB if tombstone else EMPTY
            return
        i, steps = (i + 1) % len(t), steps + 1


def build():
    t = [EMPTY] * 8
    for k in (12, 20, 5, 28, 13):
        insert(t, k)
    return t


print("table            ", build())
for tombstone in (False, True):
    t = build()
    delete(t, 20, tombstone)
    print("delete 20, tombstone=%-5s -> %s  lookup(28)=%s"
          % (tombstone, t, lookup(t, 28)))
    assert lookup(t, 28) is tombstone, "blanking the slot loses 28"
print("blanking loses a key that never moved; the marker keeps the run intact")


class Bag:
    def __init__(self, items):
        self.items = list(items)

    def __hash__(self):
        return hash(tuple(self.items))

    def __eq__(self, other):
        return isinstance(other, Bag) and self.items == other.items

    def __repr__(self):
        return "Bag(%r)" % self.items


b = Bag([1, 2])
d = {b: "first"}
b.items.append(3)                        # the key mutates while it sits in the table
probe, stored = Bag([1, 2, 3]), next(iter(d))
print()
print("the table holds", list(d), "and stored == probe is", stored == probe)
print("but 'probe in d' is", probe in d)
assert stored == probe and probe not in d
d[probe] = "second"
print("after d[probe] = 'second': len(d) =", len(d), "->", d)
assert len(d) == 2 and list(d)[0] == list(d)[1]
print("two live entries with equal keys: the hash moved, equality did not")
```

The first half is invariant (I1) failing: 28 never moved, and a write three
slots away made it unreachable. The second half is the equal-implies-same-hash
assumption failing: the table is internally consistent, it is your key that
lied.

## What to memorise

Very little. One loop, one sentence, one habit.

**The loop**, which is the whole structure:

```python
i = hash(key) % m
while slot[i] is not EMPTY:
    if slot[i].key == key:
        return slot[i]
    i = (i + 1) % m
```

with the three rules around it: *never write EMPTY on delete* (write a marker),
*never let the table fill past half*, and *never stop the scan at a marker*.

**The sentence** that turns a problem into a hash table: *"Am I repeatedly asking
whether I have seen this exact thing, or what is attached to it, and do I not
care about order?"* If yes to both, it is a hash table. If the second half is no,
it is a tree.

**The habit**: before you write the loop, write down the key. Literally, as an
expression — `word.lower()`, `tuple(sorted(word))`, `request_id`,
`(row // 3, col // 3)`. Most hash-table bugs in an interview are not table bugs;
they are the wrong key, and naming it out loud catches them before the code
exists.

Numbers worth carrying: expected probes at load `α` are `1 + α` for chaining and
`1/(1 − α)` for open addressing, so `α = 0.5` costs about 2 and `α = 0.9` costs
about 10; doubling on resize makes it `O(1)` amortised; hashing a length-`L` key
costs `Θ(L)`; and the worst case per operation is `Θ(n)`, for every hash table
ever written.

## Check yourself

:::check
Why does deleting an entry by setting its slot to `EMPTY` break an open-addressed
table, when the entry being deleted is not the one that goes missing?
--
Because the invariant that makes lookups work is not about a slot, it is about a
*path*. Invariant (I1) says: for a live key `k` stored at index `j`, every slot
between `k`'s home and `j` along its probe sequence is non-`EMPTY`. A lookup
relies on that — it stops at the first `EMPTY` and concludes the key is absent.

Writing `EMPTY` into the middle of a run falsifies (I1) for every key whose probe
sequence passes through that slot on its way to a later position. In the trace,
deleting 20 from slot 5 cut 28 (at slot 7) off from its home at slot 4. A
tombstone repairs this by being non-`EMPTY` — a lookup walks through it, while an
insert may reuse it — so (I1) is preserved by a delete that removes a key.
:::

:::check
Someone says: "A hash table is `O(1)`, so looking up a hundred-character word is
as cheap as looking up a small integer." Where are they wrong, and what is the
correct statement?
--
They are quoting a bound on the number of *probes* as if it were a bound on
*work*. Each probe requires computing `hash(key)` once and, on a collision or a
hit, an equality comparison. For a length-`L` string both are `Θ(L)`, so the
real cost of a lookup is `Θ(L)` plus `O(1)` expected probes — for a hundred-byte
key, a hundred times the work of an integer key, with no change in the
asymptotic label.

The correct statement is: **expected `O(1)` probes, each costing the price of
hashing and comparing one key.** That is why the sensible complexity for a
dictionary problem is written in terms of total input size — *Case-Preserving
Dictionary Autocorrect* is `O(total characters)`, and its constraint on total
dictionary characters exists for exactly that reason.
:::

:::check
You are given a stream of `(request_id, user, amount)` payment records in which
retries may repeat a record any number of times, and you must produce final
balances. A colleague proposes deduplicating on `(user, amount)` because "the
same person paying the same amount twice is obviously a duplicate". Where are
they wrong, and what is the right key?
--
Two things break. First, it rejects legitimate repeats: buying the same coffee
twice in a day produces two identical `(user, amount)` pairs and the second is
silently dropped, so the customer is undercharged. Second, it is not stable under
things that should not matter — if the client's retry attaches a fresh timestamp
or a new internal id, a key that includes those fields fails to recognise the
retry and the customer is charged twice.

The right key is an identifier the **client** generates once, before the first
attempt, and repeats unchanged on every retry — the `request_id` the stream
already carries. The dedup rule is then a single set membership test, and
correctness has a crisp statement: applying the function to a stream and to that
stream with arbitrary duplicates inserted gives the same state, which is what the
`again == once` assert in the implementation checks.
:::

:::check
Derive why the expected number of probes for an unsuccessful search in an
open-addressed table is at most `1/(1 − α)`, and use it to explain why growing
the table at `α = 0.9` rather than `α = 0.5` is a bad trade even though it saves
memory.
--
Let `X` be the number of probes. A search takes at least `i` probes only if its
first `i − 1` probes all hit occupied slots. Under uniform hashing that
probability is `(n/m)·((n−1)/(m−1))···`, and every factor is at most `n/m = α`
because `(n − t)/(m − t) ≤ n/m` for `n ≤ m`. So `P(X ≥ i) ≤ α^(i−1)`, and
`E[X] = Σ_{i ≥ 1} P(X ≥ i) ≤ Σ_{i ≥ 1} α^(i−1) = 1/(1 − α)`.

The function is flat and then vertical. Going from `α = 0.5` to `α = 0.9` saves
about 44% of the slots and multiplies the expected probe count by five — and each
of those extra probes is a cache miss, which is where the real time goes. Worse,
the variance grows with the mean, so the tail latency degrades faster than the
average. Memory is linear in `1/α`; time is proportional to `1/(1 − α)`. Trading
a linear saving for a hyperbolic cost is a bad deal in exactly the region people
are tempted by.
:::

:::check
*First Non-Repeating Character* asks for the first character in a string that
appears exactly once. Why does one pass building a counter not finish the job,
and what does the second pass have to iterate over?
--
A counter tells you *which* characters appear once; it cannot tell you which of
them came first, because a hash table has no order to offer. (Python dictionaries
do preserve insertion order, so iterating the counter happens to work there — but
it works for a language-specific reason, not an algorithmic one, and the same
code in a language with an unordered map returns an arbitrary answer. Relying on
it is a habit that will eventually cost you.)

The second pass must iterate **the original string**, in its own order, returning
the first character whose count is 1. That is the general shape of this family:
the hash table supplies the aggregate, the input supplies the order. Cost:
`O(n)` time and `O(k)` space for `k` distinct characters. The same structure
solves *First User to Log In Exactly Once* and *First Unique Log Entry*.
:::
