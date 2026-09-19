# Queues and Ring Buffers

> A queue is not a list you happen to remove from the front of. It is the claim
> that arrival order is part of the answer — and a ring buffer is the trick that
> makes keeping that order cost nothing, by moving two indices instead of the
> data.

## When you reach for it

You reach for a queue when the order in which things arrived determines the order
in which they must be dealt with, and the two ends of that order do different
jobs: new work joins at one end, the next decision is made at the other.

One hundred and fifteen problems in this bank use it, #30 of 150. They come in a
handful of recognisable shapes.

- **The queue is the specification.** *Implement a Queue Using Two Stacks* asks
  for it directly. *Perform Queries* ships packages in groups of three "in the
  order they entered". *Process Queue* and *Find Requests in Queue* are the same
  contract with different nouns.
- **A simulation with waiting.** One server, a line in front of it, arrivals on
  a clock: *Queue Check-in Simulation with Capacity Limit*, *ATM Queue Exit
  Order*, *Busy Intersection*, *Customer Checkout Duration*. The queue holds the
  people who have arrived but have not yet been served.
- **A trailing time window.** Only recent events count: *Recent Hit Counter*
  counts hits in `(t - 300, t]`, *Sliding-Window Rate Limiter* and *Per-Client
  Sliding-Window Rate Limiter* do the same with a quota attached. Old events
  leave from the front, in arrival order, because time is a queue.
- **The last `k` things.** *Tail N Lines* and *Implement tail -n* want the final
  `n` lines of a file you may not want to store; *Ring Buffer Operations* and
  *Fixed-Window Rolling Mean* keep a fixed-size window over a stream. The queue
  is bounded on purpose and the bound is the algorithm.
- **A frontier.** *Shortest Path in an Unweighted Graph* and *Binary Tree
  Level-Order Traversal by Levels* use a queue to hold "seen but not yet
  expanded". Breadth-first search is a queue with a graph attached: that is
  [[bfs]]'s chapter, but the reason it works is here.
- **Round robin.** *Chess Tournament* sends each loser "to the end of the queue";
  *Ad Rotation Scheduler With Cooldown* parks an advertiser until its cooldown
  expires. Rotation is a read immediately re-enqueued.

The tool is wrong when the order you need is not arrival order. If the next item
out is the smallest or the highest-priority, you want a [[heap]] — and the word
*queue* in a title is not evidence: *Implement a Min-Priority Queue* and *Top-K
Using a Priority Queue* are heap problems wearing the name. If you need the
maximum of the current window rather than its oldest member, you want a
[[monotonic-deque]]. If the most recent item comes out first, that is a
[[stack]]. And if items must be removed from the *middle* — *Linked-List Queue
with Delete and Deduplication* — a bare array queue cannot do it.

## The idea

Write onto an endless tape. Keep two positions: `head`, the oldest item you have
not yet consumed, and `tail`, the next blank cell. Enqueue writes at `tail` and
advances it. Dequeue reads at `head` and advances it. Neither index ever moves
backwards, and no element is ever moved.

That is the whole structure, and the important half is the last clause. The naive
alternative — a list you `append` to and `pop(0)` from — slides every surviving
element down one slot on every removal. The contents are identical; the work is
not.

The tape cannot really be endless. But only the cells between `head` and `tail`
are live at any moment, so if the queue never holds more than `C` items, the live
window is never wider than `C`. Take a tape of exactly `C` cells and bend it into
a circle: after cell `C - 1` comes cell `0`. Both indices advance modulo `C` and
chase each other around the ring forever. That is a **ring buffer**, and it is
why a queue is not merely correct but free.

<svg viewBox="0 0 620 200" role="img" aria-label="an array of eight cells with head and tail markers and an arrow wrapping from the last cell back to the first">
  <g>
    <path d="M 548 58 C 596 4, 16 4, 40 54" fill="none"/>
    <line x1="40" y1="56" x2="33" y2="44"/>
    <line x1="40" y1="56" x2="48" y2="45"/>
    <text x="300" y="24" text-anchor="middle">after cell C-1 comes cell 0</text>
    <rect class="fill" x="40" y="60" width="60" height="44" rx="4"/>
    <rect class="fill" x="104" y="60" width="60" height="44" rx="4"/>
    <rect x="168" y="60" width="60" height="44" rx="4"/>
    <rect x="232" y="60" width="60" height="44" rx="4"/>
    <rect x="296" y="60" width="60" height="44" rx="4"/>
    <rect class="fill" x="360" y="60" width="60" height="44" rx="4"/>
    <rect class="fill" x="424" y="60" width="60" height="44" rx="4"/>
    <rect class="fill" x="488" y="60" width="60" height="44" rx="4"/>
    <text x="70" y="88" text-anchor="middle">0</text>
    <text x="134" y="88" text-anchor="middle">1</text>
    <text x="198" y="88" text-anchor="middle">2</text>
    <text x="262" y="88" text-anchor="middle">3</text>
    <text x="326" y="88" text-anchor="middle">4</text>
    <text x="390" y="88" text-anchor="middle">5</text>
    <text x="454" y="88" text-anchor="middle">6</text>
    <text x="518" y="88" text-anchor="middle">7</text>
    <line x1="198" y1="138" x2="198" y2="108"/>
    <line x1="390" y1="138" x2="390" y2="108"/>
    <text x="198" y="156" text-anchor="middle">tail: next blank</text>
    <text x="390" y="156" text-anchor="middle">head: oldest live</text>
    <text x="300" y="186" text-anchor="middle">live window = 5 shaded cells, wrapping; size says how many</text>
  </g>
</svg>

One refinement before any code. You can store `head` and `tail`, or `head` and
`size` with `tail = (head + size) mod C` derived. Prefer the second: with two
indices, `head == tail` means both "empty" and "completely full", and nothing in
the array can tell you which, because the cells outside the live window still
hold the stale values of items dequeued long ago.

## Worked by hand

A ring buffer of capacity `C = 4`. `head` and `size` are the state; `tail` is
shown only because it is what you would picture. `_` is a never-written cell, and
*stale* values — dequeued but still physically present — are in parentheses.

| step | operation | head | size | tail | `buf` | returns |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | (new) | 0 | 0 | 0 | `[_, _, _, _]` | — |
| 1 | push A | 0 | 1 | 1 | `[A, _, _, _]` | ok |
| 2 | push B | 0 | 2 | 2 | `[A, B, _, _]` | ok |
| 3 | pop | 1 | 1 | 2 | `[(A), B, _, _]` | A |
| 4 | push C | 1 | 2 | 3 | `[(A), B, C, _]` | ok |
| 5 | push D | 1 | 3 | 0 | `[(A), B, C, D]` | ok |
| 6 | push E | 1 | 4 | 1 | `[E, B, C, D]` | ok |
| 7 | push F | 1 | 4 | 1 | `[E, B, C, D]` | **refused** |
| 8 | pop | 2 | 3 | 1 | `[E, (B), C, D]` | B |
| 9 | push F | 2 | 4 | 2 | `[E, F, C, D]` | ok |

Follow the arithmetic once with a pen. Every push writes at `(head + size) mod 4`
and every pop reads at `head`; there is no other index computation anywhere.

Four things in that table are worth more than the code that produces them.

**Step 6 overwrote a live-looking value.** The write went to cell 0, which still
held `A`. That is not a bug, it is the point: `A` was consumed at step 3 and its
cell was free for reuse. But it means you cannot look at `buf` and see the queue.
Never print the buffer, never search it, never take its length as the queue's
length.

**Steps 0 and 6 have the same two indices and opposite meanings.** At step 0,
`head = tail = 0` and the queue is empty. At step 6, `head = tail = 1` and the
queue is completely full. Any implementation that infers emptiness from
`head == tail` gets one of those two wrong. That is the single most common ring
buffer bug and it is demonstrated in Traps.

**Step 7 is a policy, not a fact.** The structure knows only `size == C`. What to
do is the problem's business: *Queue Check-in Simulation with Capacity Limit*
turns the refusal into a `null` for the person who walked away, *Bounded
Token-Bucket Request Queue* rejects the request, *Bounded Producer–Consumer
Queue* blocks the producer, a growable queue resizes. Decide which you are
writing before you write `push`.

**Row 9 reads back the specification.** Enqueued: `A B C D E F`. Dequeued: `A B`.
Live window, from head and wrapping: cells 2, 3, 0, 1 hold `C D E F`. Concatenate
the dequeued sequence with the live window and you get the enqueued sequence
exactly. That identity — not the pointer arithmetic — is what we are about to
prove, and it held after every row of the table.

## Why it is correct

A data structure is correct when every operation preserves its representation
invariant and the invariant implies the behaviour promised. So state the
invariant as the promise itself.

:::proof The ring buffer implements FIFO
**State.** An array `buf` of length `C >= 1`, an index `head` and a count `size`.
Define the **abstract queue** as the sequence

    q = ( buf[(head + i) mod C] : i = 0, 1, …, size - 1 ).

Let `E` be the sequence of values passed to successful pushes and `D` the
sequence of values returned by pops, both in operation order, and write `·` for
concatenation and `ε` for the empty sequence.

**Invariant.** After every operation:

- **(I1)** `0 <= head < C` and `0 <= size <= C`.
- **(I2)** the `size` indices `(head + i) mod C`, for `0 <= i < size`, are
  pairwise distinct.
- **(I3)** `D · q = E`.

**Lemma (no aliasing).** If `0 <= i < j < s` and `s <= C`, then
`(head + i) mod C ≠ (head + j) mod C`. Suppose they were equal. Then `C` divides
`j - i`. But `0 < j - i < s <= C`, and no multiple of `C` lies strictly between
`0` and `C`. Contradiction. Note the single hypothesis: `s <= C`. This is the
only place the capacity bound is used, and it is therefore the only thing
standing between you and silent corruption.

**Base case.** After construction, `head = 0` and `size = 0`. (I1) holds. (I2) is
vacuous. `q`, `D` and `E` are all empty, so (I3) reads `ε · ε = ε`.

**Step: `push(x)`, taken only when `size < C`.** The write index is
`t = (head + size) mod C`, which lies in `[0, C)` so the write is in bounds.
Apply the lemma with `s = size + 1 <= C`: for every `i < size`, `t` differs from
`(head + i) mod C`, so the write destroys no live value. Afterwards `head` is
unchanged and `size' = size + 1 <= C`, giving (I1); (I2) is the lemma at `s`. The
new window is the old window with `x` appended, because index `size` of the new
window is exactly the cell just written: `q' = q · x`. Since `E' = E · x` and
`D' = D`, we get `D' · q' = D · q · x = E · x = E'`, which is (I3).

**Step: `pop()`, taken only when `size > 0`.** It returns `v = buf[head]`, which
is `q[0]` by definition of `q` at `i = 0`, then sets `head' = (head + 1) mod C`
and `size' = size - 1`. (I1): the modulo keeps `head'` in range and
`size' >= 0`. The new window is
`( buf[(head + 1 + i) mod C] : i < size - 1 ) = q[1:]`, a contiguous
sub-window of the old one, so its indices are a subset of a pairwise-distinct set
and (I2) holds. Finally `D' = D · q[0]` and `q' = q[1:]`, so
`D' · q' = D · q[0] · q[1:] = D · q = E = E'`, which is (I3).

**Conclusion.** (I3) says that at every moment the values returned so far are a
*prefix* of the values enqueued so far, in the same order, and that the live
window is precisely the remaining suffix. In particular the `k`-th pop returns
the `k`-th push, which is the definition of first-in-first-out. Each operation
performs a bounded number of additions, comparisons, one modulo and at most two
array accesses, so each terminates. ∎
:::

Now say plainly what that argument leaned on, because that list is where the bugs
live.

- **`size < C` is checked before every push.** It is the lemma's only hypothesis.
  Drop the check and a push aliases the head cell: the queue silently returns an
  element that was overwritten, and the corruption appears far from its cause.
- **`size > 0` is checked before every pop.** Nothing in the proof describes
  popping an empty queue. Decide whether it raises or returns a sentinel, because
  a `None` returned from an empty queue will be pushed somewhere and crash three
  functions away.
- **`C >= 1`.** `mod 0` is undefined, and a capacity-zero queue is a special case
  no one tests.
- **Indices move only forward, by one, modulo `C`.** Every step of the proof is
  about that one motion. Code that reaches into `buf` directly, or removes from
  the middle, gets no guarantee from it.
- **The abstract queue is defined by `(head, size)`, never by the array's
  contents.** Setting `buf[head] = None` on pop releases the reference for the
  garbage collector, but correctness never depended on it — and *relying* on a
  `None` to mean empty breaks the moment someone enqueues a legitimate `None`.
- **One operation at a time.** Two pushes that both read `size` before either
  writes will both compute the same `t`. That is the whole subject of
  [[producer-consumer]] and *Bounded Producer–Consumer Queue*.

## What it costs

**The ring buffer itself.** `push` and `pop` each execute a fixed sequence of
instructions with no loop and no allocation: a comparison, an addition, a modulo,
one array store or load. That is **Θ(1) worst case**, not amortised — there is no
rare expensive operation to amortise over. Space is `C` slots plus two integers,
independent of how many items pass through. For *Tail N Lines*, where the file
may be enormous and only the last `n` lines are wanted, that independence *is*
the solution: `O(n)` memory, one pass.

**The naive queue, derived.** Using a Python list with `append` and `pop(0)`
gives the same answers. `pop(0)` removes the first element and then shifts every
survivor down one slot. Push `n` items and pop them all: the `k`-th pop leaves
`n - k` survivors to move, so the total element movement is

    Σ (k = 1 … n) (n - k) = n(n-1)/2 = Θ(n²).

*Queue Check-in Simulation with Capacity Limit* allows `n` up to `2 × 10⁵`, where
that formula gives just under `2 × 10¹⁰` element moves. The algorithm is right,
the output is right, and the submission times out. This is the most common way a
queue problem is failed.

**A growable queue.** If `C` is unknown, double the buffer when it fills,
re-linearising the window into the new array. Growing from empty to `n` items
copies `1 + 2 + 4 + … + 2^k` elements with `2^k < n`, a geometric sum below `2n`,
so `n` pushes cost under `3n`: **amortised O(1)**, with an occasional `Θ(n)`
push. See [[amortized-analysis]].

**The queue from two stacks.** *Implement a Queue Using Two Stacks* keeps an `in`
stack and an `out` stack. Push goes onto `in`; pop takes from `out`, and when
`out` is empty it first pours the whole of `in` into it, reversing the order and
so restoring FIFO. A single pop can therefore cost `Θ(n)`. Over `m` operations it
is still linear, by either of two arguments.

*Counting.* Each element is pushed onto `in` once, popped off `in` at most once,
pushed onto `out` at most once and popped off `out` at most once: four touches
per element, ever, so total work over `m` operations is `O(m)`.

*Potential.* Let `Φ = 2·|in|`, which is non-negative and starts at zero. A push
costs 1 and raises `Φ` by 2: amortised 3. A pop with `out` non-empty costs 1 and
changes nothing: amortised 1. A pop that must pour `k` elements costs `2k + 1`
and lowers `Φ` by `2k`: amortised 1. Every operation is amortised `O(1)`, so `m`
operations cost `O(m)`.

**The cost people forget** is the expiry loop, and it is worth being precise
because it looks quadratic and is not. In *Recent Hit Counter*, every query pops
all timestamps at or before `t - 300` before answering. A `while` inside a `for`
sets off alarms — but each timestamp is pushed exactly once and popped at most
once, so the total number of iterations of the inner `while`, summed over the
entire run, is bounded by the number of pushes. The whole algorithm is `Θ(n)`.
This same accounting is what makes [[sliding-window]] and [[monotonic-deque]]
linear, and it is the argument to give out loud in an interview the moment
someone points at your nested loop.

One smaller cost that is easy to miss: `x in queue` is `Θ(size)`, so dedupe needs
a companion set ([[hash-tables]]), never a scan.

## The implementation

```python run
import random


class RingQueue:
    """Fixed-capacity FIFO. Every operation is O(1) worst case."""

    __slots__ = ("buf", "head", "size")

    def __init__(self, cap):
        assert cap >= 1
        self.buf = [None] * cap
        self.head = 0                                    # oldest live cell
        self.size = 0                                    # tail is derived

    def push(self, x):
        if self.size == len(self.buf):
            return False                                 # policy: refuse
        self.buf[(self.head + self.size) % len(self.buf)] = x
        self.size += 1
        return True

    def pop(self):
        if self.size == 0:
            raise IndexError("pop from an empty queue")
        v = self.buf[self.head]
        self.buf[self.head] = None                       # release the reference
        self.head = (self.head + 1) % len(self.buf)
        self.size -= 1
        return v

    def peek(self):
        if self.size == 0:
            raise IndexError("peek at an empty queue")
        return self.buf[self.head]

    def snapshot(self):
        cap = len(self.buf)
        return [self.buf[(self.head + i) % cap] for i in range(self.size)]


q = RingQueue(4)                                         # replay the hand trace
for v in "AB":
    assert q.push(v)
assert q.pop() == "A"
for v in "CDE":
    assert q.push(v)
print("after step 6: head =", q.head, " size =", q.size, " window =", q.snapshot())
assert q.push("F") is False and q.size == 4              # step 7: refused
assert q.pop() == "B" and q.push("F")                    # steps 8 and 9
print("after step 9: head =", q.head, " size =", q.size, " window =", q.snapshot())
assert q.snapshot() == ["C", "D", "E", "F"]

rng = random.Random(4)                                   # FIFO against a model
for _ in range(300):
    cap = rng.randint(1, 6)
    r, model, enq, deq = RingQueue(cap), [], [], []
    for _ in range(60):
        if rng.random() < 0.55:
            x = rng.randrange(100)
            ok = r.push(x)
            assert ok == (len(model) < cap)
            if ok:
                model.append(x)
                enq.append(x)
        elif model:
            got = r.pop()
            assert got == model.pop(0)
            deq.append(got)
        assert r.snapshot() == model
        assert deq + model == enq                        # invariant (I3)
print("300 random runs: FIFO order and D + q == E held after every operation")
```

Three lines carry the weight.

`self.buf[(self.head + self.size) % len(self.buf)] = x` is the whole write path:
`head + size` is the derived tail, and the modulo bends the tape into a ring.
Keeping `size` rather than a stored `tail` means this is the *only* place tail
arithmetic appears, so there is exactly one place to get it wrong.

`if self.size == len(self.buf): return False` is the lemma's hypothesis, enforced.
Returning a boolean rather than raising is deliberate: the caller almost always
has to do something with the refusal — emit `null`, drop the request, count a
rejection — and a return value makes that a normal branch.

`assert deq + model == enq` in the test loop is invariant (I3) written as code. A
test that only checks the values coming out is weaker; this one checks the
*relationship* the proof established, after every operation, which is why it
catches an off-by-one in the wrap immediately rather than fifty pushes later.

Do not write this class unless the problem forbids the library.
`collections.deque` is a structure of linked blocks with `O(1)` `append` and
`popleft`, and the right answer to "which queue do I use" in Python is almost
always `deque`. Write `RingQueue` when the capacity is fixed and part of the
problem — *Ring Buffer Operations* — or when you are asked for it.

Here is the second shape, the expiry queue that most of the time-window problems
in this bank reduce to, with the amortisation instrumented so you can see it.

```python run
from collections import deque
import random


def hit_counts(kinds, times, window=300):
    """kind 0: record a hit at times[i].  kind 1: how many hits in (t-window, t]."""
    q, out, pops = deque(), [], 0
    for kind, t in zip(kinds, times):
        while q and q[0] <= t - window:          # everything strictly older leaves
            q.popleft()
            pops += 1
        if kind == 0:
            q.append(t)
        else:
            out.append(len(q))
    return out, pops


def brute(kinds, times, window=300):
    hits, out = [], []
    for kind, t in zip(kinds, times):
        if kind == 0:
            hits.append(t)
        else:
            out.append(sum(1 for h in hits if t - window < h <= t))
    return out


ks = [0, 0, 1, 0, 1, 1]
ts = [1, 2, 3, 301, 302, 400]
print("answers:", hit_counts(ks, ts)[0], " brute force:", brute(ks, ts))
assert hit_counts(ks, ts)[0] == brute(ks, ts)

rng = random.Random(9)
worst = 0
for _ in range(200):
    n = rng.randint(1, 120)
    t, kinds, times = 1, [], []
    for _ in range(n):
        t += rng.choice([0, 1, 40, 200, 500])
        kinds.append(rng.randint(0, 1))
        times.append(t)
    got, pops = hit_counts(kinds, times)
    assert got == brute(kinds, times)
    hits = sum(1 for k in kinds if k == 0)
    assert pops <= hits                          # each hit leaves at most once
    worst = max(worst, pops)
print("200 random streams agree with the recount; most inner-loop pops seen:", worst)
print("the while-inside-a-for is linear: total pops <= total pushes, always")
```

The comparison `q[0] <= t - window` is the line to read twice. The window is
half-open, `(t - window, t]`, so a hit at exactly `t - window` is *out*. Writing
`<` there keeps one stale entry and inflates counts by one — a bug invisible to
any test whose timestamps miss the boundary.

## Variants you will meet

**Deque.** Both ends open. A ring buffer supports it with no extra machinery —
push-front writes at `(head - 1) mod C` and decrements `head`. See [[deque]].

**Monotonic deque.** A deque kept ordered by discarding dominated entries, so the
front is the window's maximum. *Sliding Window Maximum*, *Maximum of Window
Minimums* and *Shortest Subarray with Sum at Least K* are this, not a plain
queue. See [[monotonic-deque]].

**BFS frontier.** A queue of nodes to expand gives shortest paths in unweighted
graphs, because the queue keeps nodes in non-decreasing distance order for free.
*Shortest Path in an Unweighted Graph* is the bare version; see [[bfs]],
[[grid-bfs]] and [[multi-source-bfs]], where the queue simply starts with several
sources.

**Level-by-level traversal.** Snapshot `k = len(queue)` and pop exactly `k` nodes:
those are one level. *Binary Tree Level-Order Traversal by Levels* wants them
grouped; in *Binary Tree Zigzag Level Order Traversal* the zigzag lives in how
you *emit* each level, not in how you traverse. See [[tree-traversal]].

**Kahn's topological sort.** A queue of nodes whose in-degree has reached zero.
*Task Dependency Ordering* is this. See [[topological-sort]].

**Queue from two stacks.** Costed above; the amortised classic. *Implement a
Queue Using Two Stacks* appears twice in this bank.

<svg viewBox="0 0 560 210" role="img" aria-label="two stacks, the in-stack poured into the out-stack, reversing the order">
  <g>
    <rect x="60" y="150" width="76" height="30" rx="3"/>
    <rect x="60" y="118" width="76" height="30" rx="3"/>
    <rect x="60" y="86" width="76" height="30" rx="3"/>
    <text x="98" y="171" text-anchor="middle">A</text>
    <text x="98" y="139" text-anchor="middle">B</text>
    <text x="98" y="107" text-anchor="middle">C</text>
    <line x1="98" y1="50" x2="98" y2="80"/>
    <line x1="98" y1="80" x2="91" y2="69"/>
    <line x1="98" y1="80" x2="105" y2="69"/>
    <text x="98" y="42" text-anchor="middle">push</text>
    <text x="98" y="200" text-anchor="middle">in</text>
    <line x1="170" y1="120" x2="300" y2="120"/>
    <line x1="300" y1="120" x2="288" y2="113"/>
    <line x1="300" y1="120" x2="288" y2="127"/>
    <text x="235" y="104" text-anchor="middle">pour once</text>
    <rect class="fill" x="340" y="150" width="76" height="30" rx="3"/>
    <rect class="fill" x="340" y="118" width="76" height="30" rx="3"/>
    <rect class="fill" x="340" y="86" width="76" height="30" rx="3"/>
    <text x="378" y="171" text-anchor="middle">C</text>
    <text x="378" y="139" text-anchor="middle">B</text>
    <text x="378" y="107" text-anchor="middle">A</text>
    <line x1="378" y1="80" x2="378" y2="50"/>
    <line x1="378" y1="50" x2="371" y2="61"/>
    <line x1="378" y1="50" x2="385" y2="61"/>
    <text x="378" y="42" text-anchor="middle">pop = front</text>
    <text x="378" y="200" text-anchor="middle">out</text>
  </g>
</svg>

**Lazy deletion.** When entries become invalid but you cannot reach into the
middle, leave them and skip them at the front. *First Unique Character in a
Stream* and *First Unique ID in a Stream* keep a queue of candidates plus a count
per key: on query, pop while the front's count exceeds one. Each entry is
discarded at most once, so the run stays linear.

**FIFO eviction.** A fixed-size cache evicting the oldest *inserted* entry is a
ring buffer plus a dictionary — *Get Minimum Time for DNS Resolution* hinges on
which order the statement names. Evicting the least recently *used* entry is a
different policy and structure: [[lru-cache]].

**Bounded blocking queue.** Capacity plus blocking on both ends: *Bounded
Producer–Consumer Queue*, *Concurrent Buffered File Logger*. See
[[producer-consumer]].

**Sliding-window rate limiting.** One expiry queue per key; the key's queue
length is its recent request count. *Per-Client Sliding-Window Rate Limiter*,
*Sliding-Window Rate Limiter*. See [[rate-limiting]] and [[streaming]].

**Round robin with a cooldown.** Serve the front, then re-enqueue it with a
"ready at" time — *Ad Rotation Scheduler With Cooldown*. When items wait on a
clock rather than on their turn, the waiting set stops being FIFO and becomes a
[[heap]]; deciding which of the two the statement describes is the problem.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **Order words: "in the order they entered", "first come first served",
   "goes to the end of the line".** *Perform Queries* and *Chess Tournament* say
   it outright. As close to a giveaway as statements get.
2. **A trailing window over timestamps**, written as `(t - 300, t]` or "in the
   last 60 seconds", with the timestamps non-decreasing. Non-decreasing is the
   crucial half: it means expiry happens at the front, in order, which is what
   makes a queue sufficient.
3. **A fixed capacity with a stated overflow rule** — refuse, drop the oldest,
   block. *Queue Check-in Simulation with Capacity Limit*, *Ring Buffer
   Operations*.
4. **"The last n"** of a stream you should not store whole: *Tail N Lines*,
   *Fixed-Window Rolling Mean*, *Sliding Window Average*.
5. **"Minimum number of edges", "fewest steps", "level by level"** on an
   unweighted graph or a tree: a BFS frontier.
6. **A simulation clock plus a single server**, or **dependencies that become
   ready over time**: the waiting set is FIFO in both.

The anti-signals, which matter more:

- **"Priority", "largest", "smallest", "most important".** The next item out is
  chosen by value, not by age. [[heap]].
- **"Maximum/minimum of each window".** [[monotonic-deque]]. A plain queue gives
  you the window but not its extreme in `O(1)`.
- **"Most recently used"** — recency of *access*, not of insertion;
  [[lru-cache]]. **"Undo", "most recent unmatched"** — [[stack]].
- **Removal from the middle, or deduplication inside the queue.** *Linked-List
  Queue with Delete and Deduplication* needs linked nodes plus a dictionary from
  key to node; an array-backed queue cannot delete an interior element in `O(1)`.
  Lazy deletion is the other escape, and only works if invalid entries eventually
  reach the front.
- **The word "queue" in the title.** *Implement a Min-Priority Queue* is a heap.
  Read the ordering rule, not the noun.

## Traps

**`list.pop(0)`.** The symptom is uniquely unhelpful: every sample passes and the
full input times out. Derived above as `Θ(n²)`. Use `collections.deque`, or an
index that walks forward over a list you never shrink.

**Inferring empty from `head == tail`.** Symptom: a count that is wrong only when
the buffer is exactly full, which small tests never reach. Keep `size`.

**Forgetting the `% C`.** In Python, an `IndexError` on the first wrap — or,
worse, a negative index silently reading from the far end when you implement
push-front. In C it is memory corruption.

**Popping an empty queue.** In a simulation the queue empties whenever the server
idles between arrivals: a branch reached on almost every real input and almost no
hand-written test.

**Not snapshotting `len(queue)` for level-order.** `for _ in range(len(q))` is
fine because Python evaluates `len(q)` once; re-reading the length after
appending children mixes two levels into one. The symptom is a first level that
is right and everything after it wrong.

**Marking visited on dequeue instead of enqueue in BFS.** A node reachable from
many neighbours is enqueued many times and every copy is expanded. The distances
still come out right, which is what makes this so persistent; the running time
does not.

**`if` instead of `while` in the expiry loop.** Removes one stale entry per query
instead of all of them. Symptom: counts too high, but only after a gap in the
timestamps. And `(t - 300, t]` is not `[t - 300, t]` — transcribe the statement's
brackets.

The first two are worth seeing run.

```python run
def moves_using_list_as_queue(n):
    """Count element moves when a list is used as a queue: pop(0) shifts the rest."""
    lst, moves = list(range(n)), 0
    while lst:
        lst.pop(0)
        moves += len(lst)                 # every survivor slid down one slot
    return moves


n = 1000
print("list-as-queue moves for n =", n, ":", moves_using_list_as_queue(n))
assert moves_using_list_as_queue(n) == n * (n - 1) // 2
print("the formula n(n-1)/2 at n = 200000 predicts", 200000 * 199999 // 2, "moves")
print("a ring buffer does the same work in", 2 * 200000, "index updates\n")


class Ambiguous:                          # head and tail, no size: the classic bug
    def __init__(self, cap):
        self.buf, self.head, self.tail = [None] * cap, 0, 0

    def push(self, x):
        self.buf[self.tail] = x
        self.tail = (self.tail + 1) % len(self.buf)

    def empty(self):
        return self.head == self.tail


class Safe:
    def __init__(self, cap):
        self.buf, self.head, self.size = [None] * cap, 0, 0

    def push(self, x):
        if self.size == len(self.buf):
            return False
        self.buf[(self.head + self.size) % len(self.buf)] = x
        self.size += 1
        return True

    def empty(self):
        return self.size == 0


bad, good = Ambiguous(4), Safe(4)
for v in "WXYZ":
    bad.push(v)
    assert good.push(v)
print("after four pushes into capacity 4:")
print("   head/tail version says empty? ", bad.empty(), "  <- it is completely full")
print("   head/size version says empty? ", good.empty())
assert bad.empty() is True and good.empty() is False
bad.push("!")                             # a fifth push, unchecked
print("   fifth push into the full buffer overwrote the front:", bad.buf)
assert bad.buf[0] == "!" and good.push("!") is False
print("   the safe version refused it instead")
```

Two failures, one root cause. The ambiguous version cannot represent "full", so
it cannot detect overflow, so it overwrites the oldest live element and reports
that it holds nothing. Nothing raises, and the corruption surfaces several
operations later, when a pop returns a value that was never at the front.

## What to memorise

The template, five lines, typed without thinking:

```python
from collections import deque
q = deque()
q.append(x)        # enqueue at the back
q.popleft()        # dequeue from the front   -- O(1), unlike list.pop(0)
q[0]               # peek at the front
```

And the fixed-capacity form, when the capacity is part of the problem:

```python
buf, head, size = [None] * cap, 0, 0
# push:  if size < cap: buf[(head + size) % cap] = x; size += 1
# pop:   v = buf[head]; head = (head + 1) % cap; size -= 1
```

The sentence that turns a problem into it: *"Is the next thing I must deal with
the thing that has been waiting longest?"* If yes, it is a queue. If the next
thing is chosen by value, it is a heap; if it is the newest, a stack.

The habit: **say what `head` and `size` mean before you write the loop.** Not
"start and length" — the actual claim: "`head` is the index of the oldest item I
have not consumed; `size` is how many live items there are; the tail is derived
and stored nowhere." A queue whose fields you cannot describe in one sentence
each will be wrong at the wrap, or at the boundary between empty and full.

Numbers worth carrying. `list.pop(0)` is `Θ(n)` and `deque.popleft()` is `O(1)`;
draining `2 × 10⁵` items from the front of a list costs about `2 × 10¹⁰` element
moves, a timeout, against `2 × 10⁵` steps on a deque. Each element is pushed once
and popped once, so a `while` nested inside a `for` that only ever pops is still
linear. And the two-stack queue touches each element at most four times, which is
why its amortised cost is constant though one pop can be `Θ(n)`.

## Check yourself

:::check
The ring buffer stores `head` and `size`, and derives `tail`. But `head` and
`tail` together seem to determine the state just as well. Why is the `size`
version strictly better, and what exactly does the other one lose?
--
Because the pair `(head, tail)` can take only `C` distinct *differences* modulo
`C`, while the queue has `C + 1` distinct sizes: `0, 1, …, C`. By the pigeonhole
principle two sizes must collide, and the two that collide are `0` and `C` —
empty and full both give `head == tail`. The representation is not injective, so
no amount of cleverness in `empty()` can be right in both cases.

What you lose is the ability to detect overflow — exactly the hypothesis
`size <= C` that the aliasing lemma depends on. The loss is not cosmetic: the
structure can no longer enforce the one condition its correctness rests on. The
traditional workaround, wasting one cell so that full means
`(tail + 1) mod C == head`, restores injectivity at the price of a slot. Keeping
`size` costs one integer and no subtlety.
:::

:::check
Someone says: "a queue built from two stacks has a pop that costs `Θ(n)`, so over
`m` operations the worst case is `Θ(mn)`. It is a toy, not a real structure."
Where are they wrong?
--
They are right about the single operation and wrong about the sequence, because
the expensive pops cannot happen often.

The counting argument settles it: an element is pushed onto `in` once, moved to
`out` once, popped off `out` once, and never returns to `in`. Total movement
across the entire run is at most three per element, hence `O(m)` for `m`
operations, hence `O(1)` amortised. A `Θ(n)` pour happens only after `n` pushes
have paid for it. The potential function `Φ = 2·|in|` makes the same point
mechanically: push costs 3 amortised, every pop costs 1.

Where their worry is legitimate: amortised is not worst case *per operation*. If
a single request has a latency budget, an occasional `Θ(n)` pause matters even
though throughput is fine. That is an argument for a ring buffer, which is `O(1)`
worst case — not an argument against the amortised analysis.
:::

:::check
*Recent Hit Counter* processes up to `2 × 10⁵` operations, and the solution has a
`while` loop nested inside the main `for` loop. A single query can pop tens of
thousands of timestamps. Why is the algorithm still `Θ(n)` and not `Θ(n²)`?
--
Because the inner loop's iterations are paid for by the outer loop's pushes, not
by its queries.

Each timestamp enters the queue exactly once, on the operation that records it,
and leaves at most once, when some later query finds it expired; after that no
query can pop it again. So the total number of inner-loop iterations over the
whole run is at most the number of hits recorded, at most `n`. Add the `O(1)`
work per operation and the total is `Θ(n)`.

The general form — bound the inner loop by the number of items that can ever be
removed, not by the number of times you enter it — is the standard accounting
behind sliding windows, monotonic deques and the two-stack queue. The runnable
block above asserts it: total pops never exceeded total pushes across 200
random streams.
:::

:::check
In BFS, why does marking a node visited when you *dequeue* it still produce
correct shortest distances, and what does it break?
--
It stays correct because the queue remains in non-decreasing distance order: the
first time any node is dequeued, it is dequeued at its true distance, so the
distance recorded is right.

What it breaks is the size of the queue. A node can be enqueued once per
neighbour expanded before it is dequeued — nothing prevents the duplicates,
because the guard is only checked on the way out. The queue grows to `Θ(E)`
entries and each duplicate is expanded again, so the work becomes `Θ(V·E)`
instead of `Θ(V + E)`, and memory blows up first.

The fix is one line in the right place: mark visited at *enqueue* time, so each
node enters the queue at most once. The symptom of getting it wrong is a correct
answer that times out — which is why it survives review so often.
:::

:::check
You are writing *Queue Check-in Simulation with Capacity Limit*: arrivals are
non-decreasing, service takes 30 seconds, and anyone arriving when more than 10
people are already in the system walks away. Why is a queue the right structure
here, and what exactly has to be in it?
--
A queue is right because the person served next is always the one waiting longest
— arrival order is the service order, stated in the problem — and because "the
number of people currently in the system" is exactly the queue's length, which
you need at every arrival.

What goes in it is the subtle part: the queue holds those who have arrived and
not yet *finished* being served, not merely those who have not yet started,
because the capacity rule counts "waiting or being served". So at each arrival at
time `t`, first drain from the front everyone whose service completed by `t`, and
only then compare the length against the limit. Completion times come from one
running clock: service starts at the later of the arrival and the previous
completion, and ends 30 seconds later.

Both halves of this chapter appear: the drain loop is the expiry pattern — linear
overall, because each person is removed once — and the capacity check is the
`size == C` test, with the refusal turned into a `null` rather than an exception.
:::
