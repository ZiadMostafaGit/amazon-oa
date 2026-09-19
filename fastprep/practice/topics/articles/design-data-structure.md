# Designing a Data Structure

> Designing a data structure is not inventing a container. It is deciding which
> facts to store more than once — once as the truth, once per question you need
> answered fast — and then proving that every operation puts all the copies back
> into agreement.

## When you reach for it

You reach for this topic when the input is not data but a **script**: an array
called `operations`, each row naming a command, and the instruction "return one
result for every operation, in order". Three hundred and sixty-five problems here
practise it, which puts it at #13 of 150 — one of the largest families you will
meet, and the one that behaves least like a puzzle and most like a small piece of
engineering.

The shape that makes it the right tool has two halves:

- **More than one question is asked of the same data.** *Insert, Delete, And Get
  Random In Constant Time* wants membership, deletion and uniform sampling;
  *Banking System, Part 2: Top Spenders* wants a balance by account *and* a
  ranking by total outflow. One container answers one of those questions well and
  the rest by scanning.
- **The operations are interleaved.** You cannot see the whole script before
  answering its first line. If you could, you would sort it and sweep once, and
  this would be an algorithm rather than a structure.

The wrong tool is the mirror image. One batch in, one number out, no operation
log: that is [[prefix-sums]] or a sweep, and a class buys nothing. A single query
pattern: a plain `dict` is the design, and a second index is a bug for no speed.

Three sub-topics live inside this chapter because they are the same skill wearing
different clothes.

**Iterators and generators** are structures whose data lives somewhere else; all
they own is a position. *Peeking Iterator*, *Stepped Iterator* and *Lazy K-Way
Union Iterator* are a one-slot buffer, a counter and a heap — three answers to
"what is the least state from which the rest of the sequence can be produced?".

**Pagination and cursors** are that same position, serialised and handed back to
you later: *Cursor-Based Pagination Over Sorted Logs* and *Stateful Paginated
Fetch N* turn on the difference between "the 3rd page" and "everything after this
item". **Designing an API surface** is the part people skip and the tests do not:
*Mutable Record Store with Error Results* is graded on whether your operations
are *total* — defined for every input, including the ones that fail.

## The idea

Here is the mental image. Keep **one ledger and as many indexes as you have
questions.**

The ledger is the truth: where a member of the collection actually lives, exactly
once. An index is a redundant copy of some fact about the ledger, kept only
because it makes one question fast — a dictionary from key to slot, a heap
ordered by priority, a linked list in recency order, a counter. Indexes are never
authoritative: if the ledger and an index disagree, the index is wrong.

Designing then has four steps, and they are always the same four:

1. **Name the ledger.** What is the collection, and where does one element live?
2. **List the questions.** One line per operation in the spec, with the required
   cost beside it.
3. **Add one index per question that the ledger answers too slowly.**
4. **Write the invariant** that says what "in agreement" means, in terms a
   program could check.

After that the code writes itself, because every operation has the same skeleton:
change the ledger, repair each index, return. The bugs live in step 4 being
unwritten — an index you forgot to repair on one of the paths.

<svg viewBox="0 0 660 230" role="img" aria-label="a dense array of values with a dictionary mapping each value to its slot">
  <g>
    <text x="20" y="28">ledger: a dense array, order meaningless</text>
    <rect class="fill" x="80" y="40" width="80" height="42" rx="4"/>
    <rect class="fill" x="180" y="40" width="80" height="42" rx="4"/>
    <rect class="fill" x="280" y="40" width="80" height="42" rx="4"/>
    <rect class="fill" x="380" y="40" width="80" height="42" rx="4"/>
    <text x="120" y="67" text-anchor="middle">7</text>
    <text x="220" y="67" text-anchor="middle">9</text>
    <text x="320" y="67" text-anchor="middle">3</text>
    <text x="420" y="67" text-anchor="middle">5</text>
    <text x="120" y="100" text-anchor="middle">0</text>
    <text x="220" y="100" text-anchor="middle">1</text>
    <text x="320" y="100" text-anchor="middle">2</text>
    <text x="420" y="100" text-anchor="middle">3</text>
    <line x1="120" y1="150" x2="120" y2="108"/>
    <line x1="220" y1="150" x2="220" y2="108"/>
    <line x1="320" y1="150" x2="320" y2="108"/>
    <line x1="420" y1="150" x2="420" y2="108"/>
    <text x="120" y="170" text-anchor="middle">7:0</text>
    <text x="220" y="170" text-anchor="middle">9:1</text>
    <text x="320" y="170" text-anchor="middle">3:2</text>
    <text x="420" y="170" text-anchor="middle">5:3</text>
    <text x="20" y="196">index: value to slot</text>
    <text x="20" y="220">invariant: vals[pos[x]] == x for every member x, and nothing else is stored</text>
  </g>
</svg>

An iterator is the same picture with the ledger removed. All that is left is the
index — here called a **cursor** — and the contract is that from the cursor alone
you can produce the rest of the sequence. That is why *Resumable List Iterator*
insists the caller "must not assume that a state is an array index": the cursor
is whatever the implementation needs, and for a k-way merge it is a whole heap of
per-source positions. A page token in *Stateful Paginated Fetch N* is that same
cursor, serialised and handed to a stranger.

## Worked by hand

Trace the set from *Insert, Delete, And Get Random In Constant Time*. The ledger
is a list `vals` holding the members with no holes; the index is a dict `pos`
from member to slot. `insert` appends and records the slot; `remove` moves the
**last** member into the vacated slot, keeping the ledger dense, then drops the
last slot.

Start with `vals = []`, `pos = {}`.

| step | operation | result | `vals` after | `pos` after |
| --- | --- | --- | --- | --- |
| 1 | insert 7 | true | `[7]` | `{7:0}` |
| 2 | insert 3 | true | `[7, 3]` | `{7:0, 3:1}` |
| 3 | insert 9 | true | `[7, 3, 9]` | `{7:0, 3:1, 9:2}` |
| 4 | insert 3 | false | `[7, 3, 9]` | `{7:0, 3:1, 9:2}` |
| 5 | remove 3 | true | `[7, 9]` | `{7:0, 9:1}` |
| 6 | remove 5 | false | `[7, 9]` | `{7:0, 9:1}` |
| 7 | insert 3 | true | `[7, 9, 3]` | `{7:0, 9:1, 3:2}` |
| 8 | remove 3 | true | `[7, 9]` | `{7:0, 9:1}` |

Four things in that table are invisible in the code.

**Step 5 moved an element nobody mentioned.** The command was `remove 3`, and the
element that moved was 9, from slot 2 to slot 1. A `remove` writes two dictionary
entries: it deletes the key for `x` and *rewrites* the key for whatever member
happened to be last. Every design of this kind has one operation that touches two
index entries, and that operation is where the bugs are.

**The order in `vals` is garbage.** After step 7 the list reads `[7, 9, 3]`,
neither insertion order nor sorted order; it is an artefact of which deletions
happened when. Nothing in the specification promised an order, so we were free to
destroy it — and that freedom is exactly what buys O(1) deletion. The moment a
later part of the problem asks for insertion order, this ledger stops being
adequate and you need a second index.

**Step 8 is the dangerous case, and it looks like the easy one.** Here `x = 3` is
*already* the last member, so "move the last member into the hole" moves 3 onto
itself. The general code survives that only if the two dictionary writes happen
in the right order — repair the mover's entry first, forget `x` second. Reverse
them and, when the mover *is* `x`, you delete the key and immediately re-add it:
the element comes back from the dead, pointing at a slot that no longer exists.

**Steps 4 and 6 returned false without touching anything.** The result array is
as much part of the answer as the state.

<svg viewBox="0 0 660 200" role="img" aria-label="removing an element by swapping the last element into the vacated slot and shrinking the array">
  <g>
    <rect class="fill" x="40" y="30" width="70" height="40" rx="4"/>
    <rect x="110" y="30" width="70" height="40" rx="4"/>
    <rect class="fill" x="180" y="30" width="70" height="40" rx="4"/>
    <rect class="fill" x="250" y="30" width="70" height="40" rx="4"/>
    <text x="75" y="56" text-anchor="middle">7</text>
    <text x="145" y="56" text-anchor="middle">3</text>
    <text x="215" y="56" text-anchor="middle">9</text>
    <text x="285" y="56" text-anchor="middle">5</text>
    <text x="145" y="22" text-anchor="middle">remove this</text>
    <text x="285" y="22" text-anchor="middle">last</text>
    <path d="M 285 82 C 285 120, 145 120, 145 84"/>
    <text x="215" y="140" text-anchor="middle">move last into the hole, then pop</text>
    <rect class="fill" x="420" y="30" width="70" height="40" rx="4"/>
    <rect class="fill" x="490" y="30" width="70" height="40" rx="4"/>
    <rect class="fill" x="560" y="30" width="70" height="40" rx="4"/>
    <text x="455" y="56" text-anchor="middle">7</text>
    <text x="525" y="56" text-anchor="middle">5</text>
    <text x="595" y="56" text-anchor="middle">9</text>
    <text x="525" y="90" text-anchor="middle">still dense: slots 0..n-1</text>
    <text x="40" y="180">two index writes: pos[5] = 1, then delete pos[3]</text>
  </g>
</svg>

## Why it is correct

An algorithm is proved with a loop invariant. A data structure is proved with a
**representation invariant**: a property of the stored fields, true between
operations, strong enough that the reported answers follow from it, and restored
by every operation. The proof is one case per operation, with the constructor as
the base case.

:::proof The ledger-and-index set answers exactly the set it was told to hold
**State.** A list `vals` and a dict `pos`. Write `n = len(vals)`.

**Abstraction function.** The set represented is
`A(vals, pos) = { vals[i] : 0 <= i < n }`. Everything reported must be a fact
about `A`.

**Representation invariant R.**

- **(R1)** `len(pos) == n`.
- **(R2)** For every `i` with `0 <= i < n`, `pos[vals[i]] == i`.
- **(R3)** The keys of `pos` are exactly the entries of `vals`.

R1 with R2 forces the entries of `vals` to be **distinct**: if
`vals[i] == vals[j]` then `pos` maps that value to both `i` and `j`, impossible
for a function unless `i == j`. So `|A| = n` and `A` is the key set of `pos` —
the consequence that makes every operation cheap, since membership is a dict
lookup and the slots are exactly `0 .. |A| - 1` with no holes.

**Base case.** After `__init__`, `vals = []` and `pos = {}`. R1 holds (`0 == 0`),
R2 and R3 hold vacuously, and `A = ∅`, which is the specified initial set.

**Case `insert(x)`, `x` already a member.** By R3, `x in pos` is true exactly when
`x ∈ A`, so the test is correct and returns false. Nothing is written, so R and
`A` are unchanged.

**Case `insert(x)`, `x` not a member.** Set `pos[x] = n` and append `x`, so
`vals' = vals + [x]`. R1: `pos` gained exactly one key, since `x` was not a key
by R3. R2: for `i < n` neither `vals[i]` nor its entry changed, and for `i = n`,
`pos[vals'[n]] = pos[x] = n`. R3: both sides gained exactly `x`. And
`A' = A ∪ {x}`.

**Case `remove(x)`, `x` not a member.** By R3 the lookup misses, nothing is
written, false is returned.

**Case `remove(x)`, `x` a member.** Let `i = pos[x]`, so `vals[i] == x` by R2,
and let `last = vals[n-1]`. The four writes are, in order:

```
vals[i] = last;   pos[last] = i;   vals.pop();   del pos[x]
```

*Sub-case `last != x`* (so `i < n - 1`). After the writes, `vals'` is `vals` with
slot `i` holding `last` and slot `n-1` gone, and `pos'` has lost the key `x` and
gained `pos'[last] = i`. Check R2 for each `j < n - 1`: if `j == i` then
`vals'[i] == last` and `pos'[last] == i`; if `j != i` then `vals'[j] == vals[j]`,
a value that is neither `x` (which sat only at slot `i`, by distinctness) nor
`last` (only at slot `n - 1`, now gone), so its entry was untouched and still
reads `j`. R1: `pos` lost one key, `n` dropped by one. R3: the entries of `vals'`
are those of `vals` minus `x`, and so are the keys. `A' = A \ {x}`.

*Sub-case `last == x`* (so `i = n - 1`). `vals[i] = last` writes `x` over `x`;
`pos[last] = i` writes `pos[x] = n - 1`, which it already was; `vals.pop()`
removes slot `n-1`; `del pos[x]` removes the key. Net effect: the last slot and
the key `x` are gone and nothing else moved, so R1, R2 and R3 hold and
`A' = A \ {x}`.

**Why the write order is forced.** One code path handles both sub-cases only
because `pos[last] = i` precedes `del pos[x]`. Swap them and, when `last == x`,
the deletion runs first and `pos[last] = i` re-inserts the key afterwards. That
violates R1 (`len(pos) = n`, `len(vals) = n - 1`) and R3, and `x in pos` now
reports a member `A` does not contain. No later operation repairs it.

**Case `get_random()`.** By R1–R3, slots `0 .. n-1` hold the `n` distinct members
of `A`, one each. Drawing `i` uniformly from `range(n)` therefore draws each
member with probability exactly `1/n`. This step uses **density** — that there
are no empty or tombstoned slots — and nothing else.

**Conclusion.** R holds initially, every operation restores it, and every
reported answer is a consequence of R about `A`, so the structure implements the
specified set. Each operation does a bounded number of writes and no loop, so
each terminates. ∎
:::

Now the assumptions, because that list is where the bugs live.

- **Keys are hashable and their hash never changes.** R3 is a claim about
  dictionary keys. If a member is mutated after insertion so that its hash moves,
  `pos` silently loses it and the invariant is false with no operation to blame
  ([[hash-tables]]).
- **Slots are internal names and the client never holds one.** `remove`
  reassigns slot numbers, so code that remembers "x is at index 3" across an
  operation is wrong.
- **Density.** Uniform sampling used R1–R3 completely. The moment you "delete" by
  marking a slot dead instead of compacting, `randrange(n)` can land on a corpse
  and sampling stops being uniform even though membership still works.
- **The invariant holds *between* operations, not during them.** After
  `vals[i] = last` and before `del pos[x]`, R is false. Single-threaded that
  window is invisible; under [[concurrency]] it is a torn read, which is why the
  concurrent variants here lock the whole operation rather than each write.
- **The randomness is uniform over `range(n)` and independent of the contents.**
  Nothing more is assumed; see [[randomized-algorithms]].

## What it costs

The cost of a data structure is not a number, it is a **vector**: one bound per
operation, plus space. Derive each.

**The append.** `insert` does one dict store and one list append, and the append
is O(1) *amortised*, not worst case: a dynamic array that doubles when full
copies `1 + 2 + 4 + … + 2^k` elements over `n` appends, a geometric sum less than
`2^{k+1} <= 2n`. Under two copies per append, with one individual append costing
Θ(n) ([[amortized-analysis]]).

**The dict.** Expected O(1) per lookup or store, because the load factor is held
below a constant so the expected chain length is constant; Θ(n) worst case under
colliding keys. On string keys — *Durable String Key-Value Store* — the hash
costs Θ(len(key)), the term omitted when people say "O(1)": `m` operations on
keys of length `L` is O(mL).

**The index tax.** Here is the law that makes design a trade rather than a free
lunch. If the structure keeps `t` indexes, each repairable in O(1), every write
does `t` repairs and the structure occupies Θ(t·n) words. Adding an index *never*
makes a write cheaper; it makes one read cheaper and every write and the memory
worse. A balance map plus a ranking heap plus a per-day histogram is three
repairs per transaction — a decision, not an accident.

**Amortisation across operations, by counting.** *Implement a Queue Using Two
Stacks*: push onto `in`; to pop, if `out` is empty, move everything from `in` to
`out`, then pop from `out`. A single pop can cost Θ(n). Count per element instead
of per operation: each element is pushed to `in` once, popped from `in` once,
pushed to `out` once and popped from `out` once — four unit operations in its
whole life and never a fifth, because an element never travels back. So `m`
operations on at most `m` elements cost at most `4m` units: O(1) amortised. The
aggregate argument is what makes the Θ(n) spike acceptable.

**Laziness, and why it is a complexity requirement.** *Lazy K-Way Union Iterator*
gives up to 200,000 values across as many sorted sources and forbids
materialising the merged sequence. Hold a heap of one pending value per non-empty
source: `next` pops the smallest and pushes that source's successor, so `n` calls
cost O(n log k) time and O(k) memory against O(n log n) and O(n) for
materialising. The lazy version is not faster; it is smaller, and that is the
requirement ([[k-way-merge]], [[heap]]).

**Pagination, and the cost of re-deriving order.** *Calendar Event System with
Pagination and Intersection* allows 10⁴ operations, any of which may be a `LIST`
wanting events sorted by start, end and name. Sorting inside `LIST` is O(n log n)
per call — 10⁴ sorts in the worst case. Keeping the collection ordered as it is
written moves that cost to the write path (O(log n) into an [[ordered-set]]) and
makes `LIST` O(pageSize) after a locate: same information, a different place to
pay for it.

**The costs people forget.** Copying on the way out — *Multiline Text Editor with
Cursor Movement* records "an independent snapshot of every line", O(n) per
`PRINT`. Unbounded growth — a hit counter that never evicts is O(total hits) in
memory when the question only asks about a window. And `list(some_dict)` inside
an "O(1)" method, which is Θ(n) every call.

## The implementation

```python run
import random


class IndexedSet:
    """Insert, remove and uniform sampling, each O(1) expected.

    ledger: vals - the members, dense, in no meaningful order
    index:  pos  - member -> its slot in vals
    invariant: len(pos) == len(vals) and vals[pos[x]] == x for every member
    """

    def __init__(self):
        self.vals = []
        self.pos = {}

    def check_rep(self):
        assert len(self.pos) == len(self.vals)
        for i, v in enumerate(self.vals):
            assert self.pos[v] == i, (v, i, self.pos.get(v))
        return True

    def insert(self, x):
        if x in self.pos:
            return False
        self.pos[x] = len(self.vals)
        self.vals.append(x)
        return True

    def remove(self, x):
        i = self.pos.get(x)
        if i is None:
            return False
        last = self.vals[-1]
        self.vals[i] = last          # move the last member into the hole
        self.pos[last] = i           # repair the mover's entry FIRST ...
        self.vals.pop()
        del self.pos[x]              # ... and only then forget x
        return True

    def get_random(self, rng):
        return self.vals[rng.randrange(len(self.vals))]


s = IndexedSet()
print("insert 7,3,9 ->", [s.insert(v) for v in (7, 3, 9)], s.vals)
print("insert 3 again ->", s.insert(3), "(already there)")
print("remove 3 ->", s.remove(3), "vals now", s.vals, "pos now", s.pos)
assert s.check_rep() and s.vals == [7, 9]
print("remove 9, the last slot ->", s.remove(9), "vals now", s.vals)
assert s.check_rep() and 9 not in s.pos

rng = random.Random(2024)
model = set(s.vals)
for _ in range(20000):                       # model-based test against `set`
    x = rng.randrange(12)
    if rng.random() < 0.5:
        assert s.insert(x) == (x not in model)
        model.add(x)
    else:
        assert s.remove(x) == (x in model)
        model.discard(x)
    assert s.check_rep() and set(s.vals) == model
print("20000 random ops match a plain set; invariant checked after each one")

s = IndexedSet()
for v in range(6):
    s.insert(v)
counts = [0] * 6
for _ in range(60000):
    counts[s.get_random(rng)] += 1
print("60000 draws from a 6-element set:", counts)
assert all(8000 < c < 12000 for c in counts), counts
```

Three pieces carry the weight.

`check_rep` is the invariant written as code. It is O(n) and no method calls it,
but calling it after every operation in a test turns "I think the indexes agree"
into a machine-checked claim, and it fails at the operation that broke the
structure rather than three operations later when a query returns nonsense.

The four lines of `remove` are in the only order that works, for the reason the
proof gave. Read them as "repair, then forget", and the `last == x` case needs no
special branch.

The loop over 20,000 random operations is **model-based testing**: run the fast
structure and an obviously-correct slow one side by side and assert they agree
after every step. For design problems this finds more bugs than any number of
hand-written cases, because the bugs live in rare interleavings —
delete-the-last-element, delete-then-reinsert — that you would not think to write
down ([[testing-your-code]]).

The second block is the cursor half of the chapter: a lazy reader over the kind
of token-paginated source *Stateful Paginated Fetch N* describes, with a counter
that makes laziness assertable rather than promised.

```python run
class PagedSource:
    """Immutable token-paginated source. Counts the pages it is asked for."""

    def __init__(self, pages):
        self.pages = pages                    # token -> (items, next_token)
        self.fetches = 0

    def fetch(self, token):
        self.fetches += 1
        return self.pages[token]


class Reader:
    """Stateful reader. Cursor = (token of the buffered page, offset in it)."""

    def __init__(self, source, start_token):
        self.src, self.token = source, start_token
        self.buf, self.i = [], 0

    def fetch_n(self, k):
        out = []
        while len(out) < k:
            if self.i < len(self.buf):        # serve from the buffer first
                take = min(k - len(out), len(self.buf) - self.i)
                out += self.buf[self.i:self.i + take]
                self.i += take
            elif self.token == "":            # no buffer, no next page: done
                break
            else:
                self.buf, self.token = self.src.fetch(self.token)
                self.i = 0
        return out


class Peeking:
    """One-slot lookahead. has_next may fetch; it must never consume."""

    def __init__(self, reader):
        self.r, self.slot = reader, []

    def _fill(self):
        if not self.slot:
            self.slot = self.r.fetch_n(1)

    def has_next(self):
        self._fill()
        return bool(self.slot)

    def peek(self):
        self._fill()
        return self.slot[0]

    def next(self):
        self._fill()
        return self.slot.pop()


pages = {"t1": ([1, 2, 3], "t2"), "t2": ([], "t3"), "t3": ([4, 5], "")}
src = PagedSource(pages)
r = Reader(src, "t1")
print("fetch_n(2) ->", r.fetch_n(2), " pages fetched:", src.fetches)
assert src.fetches == 1                       # page t3 was never touched
print("fetch_n(2) ->", r.fetch_n(2), " pages fetched:", src.fetches)
assert src.fetches == 3                       # empty page t2 skipped, not served
print("fetch_n(9) ->", r.fetch_n(9), " pages fetched:", src.fetches)
print("after exhaustion ->", r.fetch_n(4), " pages fetched:", src.fetches)
assert src.fetches == 3 and r.fetch_n(4) == []

src2 = PagedSource(pages)
p = Peeking(Reader(src2, "t1"))
print("has_next x3:", [p.has_next() for _ in range(3)], "fetches:", src2.fetches)
assert src2.fetches == 1
assert p.peek() == p.peek() == 1 and p.next() == 1 and p.peek() == 2
print("peek is repeatable; next consumes; drained:", [p.next() for _ in range(4)])
assert not p.has_next()
print("drained reader reports has_next:", p.has_next())
```

The assertion `src.fetches == 1` after the first `fetch_n(2)` is the interesting
line. It separates a reader that is lazy from one that merely returns the right
answers: nothing in the output would reveal that page `t3` had been downloaded,
and in the network version that hidden fetch is the bug. Note what laziness does
*not* mean — `has_next` on a lazy source must fetch a page to answer, and the
three consecutive calls fetch once between them. "Does not consume" and "does no
work" are different promises; *Lazy K-Way Union Iterator* and *Stepped Iterator*
ask only for the first.

## Variants you will meet

**Build the map itself.** Buckets plus chaining, with a hash and a modulus —
*Design Hash Map*, *Custom Hash Map Operations*. The design question is the
collision policy and the resize threshold ([[hash-tables]]).

**Dict plus doubly linked list.** The dict finds the node in O(1); the list gives
O(1) unlink and move-to-front. The recency structure, with its own chapter:
[[lru-cache]], built on [[linked-list]]. *File-Content LRU Cache* is it.

**Two stacks make a queue; two stacks make undo/redo.** Amortised O(1) as derived
above ([[stack]], [[queue]]). *Command Undo Data Structure* and *Billing Log with
Undo and Redo* store *inverse commands*.

**Heap-backed rankings.** *Streaming Top-K Frequent Elements*, *Fixed-K Kth
Largest Stream*: a size-k heap keeps the k-th best at the root ([[heap]],
[[top-k]]).

**Time-indexed stores.** Append `(timestamp, value)` in increasing time and
binary search the query — *Closest-Timestamp Key-Value Queries*, *Globally
Versioned Key-Value Store*. The index is sortedness by time, maintained for free
by the append ([[binary-search]]).

**Windows over time.** A deque of timestamps, evicting from the front anything
older than the window — *Recent Hit Counter*, *Sliding-Window Rate Limiter*. Each
timestamp is pushed once and popped once, so eviction is amortised O(1)
([[deque]], [[sliding-window]], [[rate-limiting]]).

**Snapshots and versions.** A version counter plus `(version, value)` per key, or
copy on write — *Snapshot Set Iterator*, *Cloud Storage File Versioning*
([[persistent-structures]]).

**Iterators over structure.** A stack of cursors flattens nesting (*Nested List
Iterator with Remove*); a stack of nodes is a paused in-order recursion
(*Binary Search Tree Iterator*, [[tree-traversal]]); a counter and a step is
*Stepped Iterator*; a one-slot buffer is *Peeking Iterator*.

**Generators are cursors the compiler wrote.** A Python `yield` function is a
resumable state machine and the shortest way to write most iterators. Its limit
is that its state is not yours: you cannot serialise, copy or restore it. Hence
*Resumable List Iterator*'s explicit `getState`/`setState` — once the cursor must
survive a process boundary, you name it yourself ([[state-machines]]).

**Offset pagination versus cursor pagination.** Offset (`pageSize`, `pageNum`, as
in *Calendar Event System with Pagination and Intersection*) is stateless and
stable only if the collection does not change between calls. Cursor pagination
(*Cursor-Based Pagination Over Sorted Logs*, *Stateful Paginated Fetch N*) hands
back an opaque token meaning "everything strictly after this item", and stays
correct under concurrent insertion. *Format a Centered Pagination Bar* is the
pure-offset arithmetic with no data at all.

**API surface as the actual problem.** *For All Intents And Purposes* parts 1–4
and *Banking Transaction Exceptions* grade the error taxonomy: which failures are
values, which are exceptions, what a no-op returns.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **The input is `operations`, and the output is "one result per operation".**
   As close to a giveaway as statements get, and it is the standard phrasing
   across this bank.
2. **A per-operation complexity requirement.** "each of the following operations
   in average constant time" (*Insert, Delete, And Get Random In Constant Time*)
   exists to rule out the one-container solution.
3. **Two or more questions asked of the same collection**, where the natural
   container answers one of them by scanning.
4. **Multi-part problems.** *Banking System, Part 1 / Part 2*, *For All Intents
   And Purposes* parts 1–4. Each part adds a query pattern to the same ledger.
5. **`next` / `hasNext` / `peek` / `getState` / `setState`.** An iterator. If
   `setState` is there, the cursor must be serialisable and must not be assumed
   to be an index.
6. **"page", "pageSize", "pageNum", "token", "cursor".** Pagination — cursor
   pagination specifically when a token comes back to you on the next call.
7. **A vocabulary of failures**: "returns false if", "ERROR_EXHAUSTED", "throws
   an illegal-remove error". Those cases are half the test suite.

The anti-signals:

- **One input, one output, no operation log.** Then it is an algorithm; a class
  is packaging, not design. *Product of the Maximum and Minimum in a Dataset* is
  one pass however it is titled.
- **The whole script is available up front and order does not matter.** Sort it
  and sweep. *Count Paginated Medical Records in a Range* looks like pagination
  and is a flat count over all pages — the pagination is scenery.
- **Only one query pattern.** A `dict` is the design. Extra indexes are extra
  invariants to break.

## Traps

**Repairing the index in the wrong order.** Symptom: everything passes until an
input removes the element that happens to be last, after which that element can
never be re-inserted. Demonstrated below.

**Repairing on one write path but not another.** Insert repairs the secondary
index; *overwrite* silently does not. Symptom: correct on fresh keys, wrong after
an update — every failing case contains the same key twice.

**Lazy deletion without a validity check.** Popping from a heap that may hold
stale entries, or sampling an array with tombstones. Symptom: the heap's top is
an element that was removed; sampling is no longer uniform.

**Iterator invalidation.** Mutating a collection while an iterator walks it.
*Nested List Iterator with Remove* spells out the fix: after removing inside the
row being scanned, move the cursor back so the element that shifted into the hole
is not skipped. Symptom: one element missing per removal.

**Reading the clock instead of taking the time as an argument.** Rate limiters
and hit counters here pass timestamps in; a real clock is untestable.

**`hasNext` with side effects.** An implementation that advances in order to
decide. Symptom: two consecutive `hasNext` calls disagree, or the next value is
not the one `hasNext` proved was there. Demonstrated below.

**Returning your internal containers.** The caller mutates the list you returned,
or keeps it and sees it change later — which is why *Multiline Text Editor with
Cursor Movement* asks for "an independent snapshot". Symptom: a result recorded
early in the run is different by the end.

```python run
def remove_wrong(vals, pos, x):
    """Same four writes, two of them swapped."""
    i = pos.get(x)
    if i is None:
        return False
    last = vals[-1]
    del pos[x]                    # forget x first ...
    vals[i] = last
    pos[last] = i                 # ... and resurrect it when last IS x
    vals.pop()
    return True


vals, pos = [7, 9], {7: 0, 9: 1}
print("before:", vals, pos)
remove_wrong(vals, pos, 9)        # 9 is the last element: the fatal case
print("after remove_wrong(9):", vals, pos, "<- 9 is still a key")
assert 9 in pos and len(pos) != len(vals)
print("is 9 a member?", 9 in pos, " can we re-insert it?", 9 not in pos)
print("slot it claims:", pos[9], "but vals has length", len(vals))


class BadIterator:
    """has_next that advances. The classic broken adapter."""

    def __init__(self, values):
        self.v, self.i = values, 0

    def has_next(self):
        ok = self.i < len(self.v)
        self.i += 1               # the bug: testing consumes
        return ok

    def next(self):
        self.i += 1
        return self.v[self.i - 1]


class GoodIterator:
    def __init__(self, values):
        self.v, self.i = values, 0

    def has_next(self):
        return self.i < len(self.v)

    def next(self):
        self.i += 1
        return self.v[self.i - 1]


bad, good = BadIterator([10, 20, 30]), GoodIterator([10, 20, 30])
print("bad : has_next ->", bad.has_next(), " next ->", bad.next(), "<- 10 vanished")
print("good: has_next ->", good.has_next(), " next ->", good.next())
assert bad.next() == 30 and good.next() == 20   # the bad one skips every other
twice = lambda it: [it.has_next(), it.has_next()]
print("bad : two has_next in a row ->", twice(BadIterator([10])))
print("good: two has_next in a row ->", twice(GoodIterator([10])))
assert twice(BadIterator([10])) == [True, False]
assert twice(GoodIterator([10])) == [True, True]
print("has_next must be a pure query, or a loop over it loses half the values")
```

The first failure is invisible in the returned value: `remove_wrong` returns
`True`, and the damage surfaces only on a later `insert` or sample. The second is
invisible to a test that never calls `has_next` twice in a row. Same lesson: a
design bug is usually a *state* bug, and a test that only inspects return values
will not see it.

## What to memorise

Almost nothing, because the content changes every time. Memorise the procedure.

**The recipe**, in four lines: name the ledger; list the questions with their
required costs; add one index per slow question; write the invariant that ties
the indexes to the ledger. Then every operation is "change the ledger, repair
each index, return what happened".

**The template** worth having in your fingers, because half the design problems
in this bank are a specialisation of it:

```python
class Thing:
    def __init__(self):
        self.items = []        # the ledger: the truth, dense
        self.where = {}        # an index: key -> slot

    def check_rep(self):       # the invariant, executable
        assert len(self.where) == len(self.items)
        for i, v in enumerate(self.items):
            assert self.where[v] == i
```

**The sentence** that turns a statement into a design: *"Which questions must be
fast, and what redundant copy makes each one fast?"* If every question is already
fast over one container, stop; an extra index is a liability.

**The habit**: write `check_rep` before the operation that is hard, and call it
after every step of a randomised test against an obviously-correct model. For
iterators: say out loud what your cursor is, and whether `has_next` may change
it. (It may not.)

Numbers worth carrying: list append and dict access are amortised/expected O(1),
with doubling costing under two copies per element; a lazy k-way merge is
O(log k) per `next` and O(k) memory; `t` indexes mean `t` repairs on every write
and Θ(t·n) space; and a per-call sort inside an operation that runs 10⁴ times is
the standard way to turn a correct design into a timeout.

## Check yourself

:::check
In `remove`, why must `pos[last] = i` be executed *before* `del pos[x]`, and what
exactly goes wrong if you swap them?
--
Because the two writes can refer to the same key. When the element being removed
is already the last one, `last` *is* `x`. Doing the deletion first removes the
key, and `pos[last] = i` then puts it straight back, pointing at slot `n - 1` — a
slot `vals.pop()` is about to destroy. That breaks R1 (`len(pos)` exceeds
`len(vals)`) and R3, and the symptoms surface much later: `insert(x)` returns
false forever for that value, and `vals[pos[x]]` is out of range.

In the correct order one code path handles both sub-cases without a branch:
`pos[last] = i` followed by `del pos[x]` is "write, then delete" on the same key,
which nets out to a delete.
:::

:::check
Someone says: "`get_random` doesn't need the array at all — just do
`random.choice(list(self.pos))`." Where are they wrong?
--
Not about uniformity — that expression does sample the members uniformly. They
are wrong about the cost, which is the entire specification.

`list(self.pos)` copies every key into a fresh list: Θ(n) time and Θ(n)
allocation per call. The problem asks for average constant time per operation, so
`m` samples become Θ(mn) — at 10⁵ operations on a 10⁵-element set, 10¹⁰ copies.

This is the most common way an "O(1)" method quietly becomes linear: an
innocent-looking conversion in the middle of it. The dense array exists so a
random member can be addressed by an integer — and deletion had to be redesigned
to keep that ability, which is the trade the structure is built around.
:::

:::check
A log is paginated by offset: page `p` means records `p·k` through `p·k + k - 1`
of the collection sorted by time. A client reads page 0, then a record older than
everything it has seen is inserted, then it reads page 1. Show concretely what
goes wrong, and why a cursor fixes it.
--
Take `k = 2` and records `[A, B, C, D]` in sort order. Page 0 returns `[A, B]`.
Now `Z` is inserted and sorts before `A`, so the collection is `[Z, A, B, C, D]`.
Page 1 is records 2 and 3, which are now `[B, C]`. The client has seen `B` twice
and, had the insertion been a deletion instead, it would have skipped a record
entirely.

The bug is that an offset names a *position in a list that moves*. A cursor names
a *record*: "everything strictly after B, in sort order". Insertions before `B`
do not change what comes after `B`, so the next page is `[C, D]` whatever else
happened. The cost is that a cursor cannot jump to "page 7" — offsets are
random-access and unstable, cursors are sequential and stable.
:::

:::check
*Resumable List Iterator* insists that "a caller must not assume that a state is
an array index", and that a saved state must still work after the original
iterator has advanced or been exhausted. Why are those two requirements really
the same requirement?
--
Both say the state is defined by *what it can reproduce*, not by how it is
stored.

If the caller could assume an index, the implementation could never change
representation — and it must, because the same interface has to cover a file
iterator (offset plus decoder state), a k-way merge (one position per source) and
a tree walk (a stack of nodes).

"Must still work after the original advanced" is the same point from the other
side: the state cannot be a *reference into the live iterator*, it has to be a
self-contained value. An index into an immutable array satisfies both by
accident, which is why the statement warns you not to rely on it.
:::

:::check
You are designing *Banking System, Part 2: Top Spenders* on top of a Part 1 that
stores a balance per account in a dict. Someone proposes keeping a max-heap of
`(spent, account)` and pushing a new entry on every transaction. What is right
about that, what is wrong, and what is the fix?
--
Right: the ranking question needs its own index, and a heap answers in O(log n)
what the dict answers in Θ(n).

Wrong: `spent` changes, and a binary heap cannot update a key it already holds.
Pushing a fresh entry leaves the old one in place, so the heap fills with stale
pairs and the top can name an account whose real total is smaller than a
competitor's. The ranking is right early and drifts as accounts are updated.

Two standard fixes, and choosing between them is the design decision: (a) *lazy
deletion with validation* — keep the pushes, and when you pop `(s, acct)` discard
it unless `s == spent[acct]`, correct because the true entry is always present
and everything above it is stale; (b) an [[ordered-set]] keyed by
`(spent, account)`, deleting the old key before inserting the new one. Option (a)
is less code and is correct only *with* the validation.
:::
