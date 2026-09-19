# Scheduling and Deadlines

> A scheduling problem is never really about time. It is about which single
> commitment, out of all the ones you have already made, expires first — and
> that is a question a min-heap answers in one look.

## When you reach for it

You reach for this chapter when a statement hands you **things that occupy a
resource for a stretch of time** and asks either *how many resources do I need*
or *what order do I run them in*.

One hundred and nine problems in this bank are scheduling problems, which puts
the topic at #34 of 150. They separate into a few shapes worth learning in place
of the problems.

- **Count the resources.** *Meeting Rooms II*, *Minimum Meeting Rooms*,
  *Get Minimum Cores*, *Minimum Classrooms for Courses*, *Get Minimum Dock Bays*,
  *Chairs Requirement*. Intervals in, one integer out: the maximum number of
  intervals alive at one instant, which is what this chapter's core algorithm
  computes.
- **Assign to a named resource.** *Meeting Room Scheduler* wants the
  lowest-numbered free room; *API Call Thread Pool Schedule* the worker with the
  earliest available time, ties to the smallest id; *Schedule Requests to
  Servers* the least busy server in an allowed prefix. You must say *which*.
- **Run in deadline order.** *Task Scheduler with Dependencies* and *Task
  Processor: Dependencies and Deadlines* consume the available task with the
  earliest deadline — the half of the chapter its second word refers to.
- **Respect a gap between repeats.** *Task Scheduler*, *Minimum Days for
  Fixed-Order Tasks with Cooldown*, *Priority Job Scheduler with Cooldowns*,
  *Ad Rotation Scheduler With Cooldown*. The resource is the same every time;
  what is scarce is separation.
- **Select a profitable subset.** *Maximum Profit in Job Scheduling*, *Cinema
  Shows*, *Max Sum of Non-Overlapping Intervals*. These look like the others and
  are not greedy at all; the variants section says where the line falls.

The tool is wrong when the constraint is not *time overlap* but *precedence*.
Nine of the problems listed under this topic are *Course Schedule* variants, and
none has a clock in it: "take B before A" is an edge in a directed graph, and the
technique is [[topological-sort]]. The word *schedule* in a title tells you
nothing; the phrase *[start, end)* tells you everything.

It is also wrong when the resource is not interchangeable. The proof below
depends on any meeting fitting in any room; *Minimum Meeting Rooms with
Assignments* and *Schedule Requests to Servers* restrict which resource each
request may use, and the counting argument stops being achievable.

Prerequisites: [[greedy]] reasoning, and a [[heap]] as a black box that hands you
the minimum in O(log n). Everything else is built here.

## The idea

Put the meetings on a timeline and ask a different question from the one the
statement asks. Not "which meeting goes in which room", but **"at the busiest
instant of the day, how many meetings are running at once?"**

<svg viewBox="0 0 620 250" role="img" aria-label="five meetings drawn as bars on a timeline, with the overlap count profile underneath peaking at two">
  <g>
    <line x1="40" y1="182" x2="600" y2="182"/>
    <text x="36" y="200">0</text>
    <text x="156" y="200">10</text>
    <text x="276" y="200">20</text>
    <text x="396" y="200">30</text>
    <text x="516" y="200">40</text>
    <rect class="fill" x="40" y="20" width="360" height="18" rx="4"/>
    <text x="405" y="34">(0, 30)</text>
    <rect class="fill" x="100" y="48" width="60" height="18" rx="4"/>
    <text x="165" y="62">(5, 10)</text>
    <rect class="fill" x="220" y="76" width="60" height="18" rx="4"/>
    <text x="285" y="90">(15, 20)</text>
    <rect class="fill" x="340" y="104" width="180" height="18" rx="4"/>
    <text x="525" y="118">(25, 40)</text>
    <rect class="fill" x="400" y="132" width="180" height="18" rx="4"/>
    <text x="400" y="166">(30, 45) starts as (0, 30) ends</text>
    <polyline fill="none" points="40,235 100,235 100,218 160,218 160,235 220,235 220,218 280,218 280,235 340,235 340,218 520,218 520,235 580,235"/>
    <text x="40" y="250">one alive</text>
    <text x="150" y="212">two alive — and two is the answer</text>
  </g>
</svg>

Once you ask it that way, the algorithm writes itself. Walk the meetings in
order of start time. Keep a bag holding, for each room opened so far, **only the
time that room next becomes free** — the identity of the meeting sitting in it is
information you will never use again. For the next meeting you need one fact: has
any room freed up by now? Since you only care whether *some* room qualifies, you
only ever need to look at the room that frees up **earliest**. If that one is
free, reuse it. If even that one is busy, every room is busy, and you open a new
one.

"Give me the smallest element of a changing multiset" is the definition of a
min-heap. That is why scheduling and heaps travel together, and why a chapter on
scheduling has to be, in part, a chapter on heaps.

The same picture covers the second half of the topic. When jobs carry deadlines
instead of start times, the bag holds *jobs waiting to run* rather than *rooms in
use*, and the interesting element is again the extreme one: the nearest deadline.
Both halves are one reflex — **sort by the key that makes the future irrelevant,
and keep a heap of the commitments the past has locked in.**

## Worked by hand

Five meetings, half-open, already sorted by start:
`(0, 30), (5, 10), (15, 20), (25, 40), (30, 45)`.

`busy` is the heap of end times; its minimum is written first. "Free?" asks
whether `min(busy) <= s`, which is the half-open rule: a room whose meeting ends
at exactly 30 is available to a meeting starting at 30.

| step | meeting | `busy` before | `min` | free? | action | `busy` after | rooms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | (0, 30) | `[]` | — | no rooms yet | open a room | `[30]` | 1 |
| 2 | (5, 10) | `[30]` | 30 | 30 ≤ 5 is false | open a room | `[10, 30]` | 2 |
| 3 | (15, 20) | `[10, 30]` | 10 | 10 ≤ 15, yes | reuse: pop 10, push 20 | `[20, 30]` | 2 |
| 4 | (25, 40) | `[20, 30]` | 20 | 20 ≤ 25, yes | reuse: pop 20, push 40 | `[30, 40]` | 2 |
| 5 | (30, 45) | `[30, 40]` | 30 | 30 ≤ 30, yes | reuse: pop 30, push 45 | `[40, 45]` | 2 |

Answer: two rooms.

Four things in that table are worth a second look, and none of them is visible
in the code.

**The heap never shrinks.** A reuse pops one end time and pushes another, so the
size is unchanged; an open grows it by one. The size is therefore
non-decreasing, which is why the final `len(busy)` is also the *maximum* number
of rooms ever in use. If you find yourself maintaining a separate `best`
variable, you have not noticed this.

**Step 5 is the whole problem.** `30 <= 30` is true, so `(0, 30)` and `(30, 45)`
share a room. Flip that `<=` to `<` and the answer becomes 3. Every *Meeting
Rooms II* statement in this bank spends a sentence on precisely this case —
"an interval that ends exactly when another starts does not count as a
conflict" — because it is the only ambiguity in the problem, and because
*Get Minimum Cores* states the opposite convention: its processes run from
`start[i]` through `end[i]` **inclusive**, so there the same two intervals do
collide.

**Room identity is invented, not recorded.** The heap held `[20, 30]` after step
3; nothing in it says which room is which, and nothing ever asks. When a
statement does ask — *Meeting Room Scheduler* wants the lowest-numbered available
room — this algorithm is not sufficient as written.

**Step 2 decided the answer.** Rooms went from 1 to 2 at time 5 and never moved
again, though three more meetings arrived. The answer is fixed by the single
busiest instant; the rest of the work only confirms that no instant is busier.

<svg viewBox="0 0 560 120" role="img" aria-label="the heap of end times after each step, with the minimum on the left">
  <g>
    <text x="10" y="35">after 2</text>
    <rect class="fill" x="80" y="18" width="46" height="26" rx="4"/>
    <text x="95" y="36">10</text>
    <rect x="130" y="18" width="46" height="26" rx="4"/>
    <text x="145" y="36">30</text>
    <text x="200" y="36">min = 10, the next room to free up</text>
    <text x="10" y="80">after 5</text>
    <rect class="fill" x="80" y="63" width="46" height="26" rx="4"/>
    <text x="95" y="81">40</text>
    <rect x="130" y="63" width="46" height="26" rx="4"/>
    <text x="145" y="81">45</text>
    <text x="200" y="81">same size: no room was ever added after step 2</text>
  </g>
</svg>

## Why it is correct

Two claims need proving, and they are separate. First, that counting the busiest
instant gives the right number of rooms — that is the algorithm above. Second,
that when jobs carry deadlines, running them in deadline order is the right
choice — that is the classical result the second half of this topic rests on.

:::proof The heap sweep uses exactly as many rooms as the busiest instant needs
**Setup.** Meetings `(s_i, e_i)` with `s_i < e_i`, occupying the half-open
interval `[s_i, e_i)`, processed in nondecreasing `s`. Write
`alive_k(t) = |{ i <= k : s_i <= t < e_i }|` for the number of the first `k`
meetings running at instant `t`, and `r_k` for the heap's size after `k` steps.

**Invariant.** After processing `k` meetings:

- **(I1)** There is an assignment of meetings `1..k` to `r_k` rooms such that no
  two meetings in the same room overlap, and the heap holds exactly the end time
  of the *last* meeting placed in each room.
- **(I2)** `r_k = max_{j <= k} alive_k(s_j)`, with `r_0 = 0`.

**Base case.** `k = 0`: no meetings, no rooms, empty heap, and the maximum over
an empty set is 0. Both parts hold.

**A standing consequence of (I1).** For any instant `t`, two meetings in the same
room cannot both be running at `t`, since they do not overlap. So at most one
meeting per room is alive at `t`, giving `alive_k(t) <= r_k` for **every** `t` —
not just the start times. Keep this; it is used twice.

**Inductive step.** Let meeting `k+1` be `(s, e)`, and note `s >= s_j` for all
`j <= k` because the input is sorted. Let `m` be the heap's minimum.

*Case `m <= s` (reuse).* The room `R` whose last end time is `m` is free at `s`:
its last meeting ends at `m <= s`, and every earlier meeting in `R` ended sooner
still, since a meeting is placed in a room only when that room's end time is at
most its start, so end times within a room strictly increase. Placing `k+1` in
`R` keeps (I1), with `m` replaced by `e`, and `r_{k+1} = r_k`. For (I2): the
standing consequence gives `alive_{k+1}(s_j) <= r_k` for every `j <= k+1`, so the
maximum cannot exceed `r_k`; and it is at least `r_k`, because whichever earlier
step last raised the size to `r_k` made `alive` equal `r_k` at some start time
(next case), and adding meetings never decreases `alive`.

*Case `m > s` (open).* Every room's last meeting ends after `s` and started at or
before `s`, so **every one of the `r_k` rooms holds a meeting alive at `s`**.
Together with meeting `k+1` itself, `alive_{k+1}(s) >= r_k + 1`. The standing
consequence applied to the new assignment gives `alive_{k+1}(s) <= r_k + 1`, so
it equals `r_k + 1`. The algorithm sets `r_{k+1} = r_k + 1`, which matches, and
no start time can beat it, again by the standing consequence. (I1) holds because
the new meeting went into a brand-new room.

**Termination.** The loop performs exactly one iteration per meeting, so it ends
after `n` of them.

**Conclusion.** (I1) exhibits a legal assignment using `r_n` rooms, so `r_n` is
achievable. For the lower bound: at the instant `t*` maximising `alive_n`, all
`alive_n(t*)` meetings run simultaneously and pairwise overlap, so *any* legal
assignment gives them distinct rooms and uses at least `alive_n(t*)` rooms.
Finally `alive_n` is constant on each interval between consecutive endpoints and
only ever increases at a start time, so its maximum is attained at some `s_j`,
which by (I2) is `r_n`. Achievable and not improvable: `r_n` is optimal. ∎
:::

:::proof Earliest deadline first is optimal for meeting deadlines
**Setup.** `n` jobs, job `i` taking `p_i > 0` time and due at `d_i`, all
available from time 0, one machine, no preemption. A schedule is an order; the
job in position `k` finishes at the sum of the durations up to and including it.
The schedule is *feasible* if every job finishes at or before its deadline.

**Claim.** If any order is feasible, then the order by nondecreasing deadline is
feasible.

**Exchange.** Let `σ` be a feasible order that is not sorted by deadline. Then
some adjacent pair is inverted: job `a` immediately followed by job `b` with
`d_a > d_b`. Say `a` starts at `t`. Feasibility gives `t + p_a <= d_a` and
`t + p_a + p_b <= d_b`. Swap them. Now `b` finishes at
`t + p_b <= t + p_a + p_b <= d_b`, so `b` is on time; and `a` finishes at
`t + p_b + p_a`, which is the same instant `b` finished at before, so it is
`<= d_b < d_a` and `a` is on time. Every other job occupies exactly the same slot
as before, because the pair still fills `[t, t + p_a + p_b]`. The swapped order
is feasible.

**Termination.** Each such swap fixes one inverted adjacent pair and changes the
relative order of no other pair, so the number of inversions with respect to
deadline order drops by exactly one. It is a non-negative integer, so after
finitely many swaps no inverted adjacent pair remains — the order is sorted by
deadline — and feasibility survived every step. ∎
:::

Now name what the two proofs leaned on, because that list is where the bugs live.

- **The input is processed in nondecreasing start order.** Used twice: to claim
  every room's last meeting started at or before `s`, and to claim end times
  inside a room increase. Unsorted input returns a number that is too large,
  silently.
- **Half-open intervals, matched by `<=`.** The "free at `s`" step reads
  `m <= s`. Under closed intervals that step is false and the test must be `m < s`.
- **`s_i < e_i`.** A zero-length meeting is alive at no instant, so `alive` never
  counts it, yet the algorithm still gives it a room — the two halves of the
  conclusion disagree on it. Check whether the constraints allow it.
- **Rooms are interchangeable.** The lower bound survives when requests are
  restricted to particular rooms, but (I1) — the achievability half — collapses,
  and the true answer can be larger.
- **Every meeting is scheduled.** If you may reject requests, as *Meeting Room
  Scheduler* does when all rooms are taken, the objective has changed.
- **In the deadline proof, everything is released at time 0.** With release
  times, non-preemptive earliest-deadline-first is *not* optimal — the machine
  may have to idle deliberately to wait for an urgent job. With preemption it
  becomes optimal again. That assumption is quietly load-bearing.

## What it costs

Take the room-counting algorithm apart.

**Sorting.** `sorted(intervals)` is `Θ(n log n)` comparisons on tuples — the
dominant term, and the *only* superlinear part.

**The heap.** Count operations rather than assert a bound. Each meeting performs
exactly one heap operation — a `heapreplace` (reuse) or a `heappush` (open) —
so there are exactly `n` operations, never `2n`. Each costs `O(log r)` where `r`
is the current heap size, and `r <= R`, the answer. Total heap work:
`Θ(n log R)`. Since `R <= n`, the whole algorithm is
`Θ(n log n + n log R) = Θ(n log n)`.

That decomposition pays off when the sort disappears. When the statement
promises sorted input — as *Meeting Room Scheduler* does — the cost drops to
`Θ(n log R)`, effectively linear for a handful of rooms. It also explains why
`heapreplace` is written rather than `heappop` then `heappush`: both are
`O(log r)`, but `heapreplace` does one sift-down instead of a sift-down plus a
sift-up.

**Space.** `Θ(R)` for the heap plus `Θ(n)` for the sorted copy. At the
`n = 2 * 10^6` limit of *Minimum Meeting Rooms* that copy is not a rounding
error; `list.sort()` avoids it if you may destroy the input.

**The two-array sweep** — sort the starts, sort the ends, walk both with a
counter — is the same `Θ(n log n)` with a smaller constant and no heap. Prefer it
when the answer is just a count. It cannot say *which* meeting is in which room,
because it separated the starts from their ends; that pairing is exactly what the
heap keeps.

**The cost people forget** is the coordinate range, and two problems here differ
on it instructively. *Get Minimum Cores* has `n <= 10^5` but times up to `10^9`:
a per-time-unit difference array would need `10^9` cells, so sorting's
`Θ(n log n)` is the floor. *Minimum Meeting Rooms* has `n <= 2 * 10^6` and times
bounded by `2 * 10^6`, where a difference array over the time axis runs in
`Θ(T + n)` and beats sorting outright — about `4 * 10^6` array writes against
`4 * 10^7` comparisons. Same question, different constraint line, different
intended algorithm.

For the deadline half, earliest-deadline-first costs the sort, `Θ(n log n)`, and
nothing else. In its online form — jobs become available as dependencies clear,
and deadlines can be revised — each event pushes at most one heap entry, so with
`m` operations the heap holds `O(m)` entries and the total is `O(m log m)`.

## The implementation

```python run
import heapq
import random


def min_rooms(intervals):
    """Fewest rooms for half-open meetings [start, end)."""
    busy = []                                     # end times of the rooms in use
    for s, e in sorted(intervals):
        if busy and busy[0] <= s:                 # the earliest room is free
            heapq.heapreplace(busy, e)            # reuse it: one sift, not two
        else:
            heapq.heappush(busy, e)               # every room is still occupied
    return len(busy)


def min_rooms_sweep(intervals):
    """Same answer with two sorted arrays and no heap."""
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    i = j = live = best = 0
    while i < len(starts):
        if starts[i] < ends[j]:                   # a meeting opens before one closes
            live += 1
            best = max(best, live)
            i += 1
        else:
            live -= 1
            j += 1
    return best


def max_overlap(intervals):
    """The definition, not an algorithm: most meetings alive at any instant."""
    return max((sum(1 for s, e in intervals if s <= t < e) for t, _ in intervals),
               default=0)


demo = [(0, 30), (5, 10), (15, 20), (25, 40), (30, 45)]
print("meetings      ", demo)
print("heap answer   ", min_rooms(demo))
print("sweep answer  ", min_rooms_sweep(demo))
print("max overlap   ", max_overlap(demo), "(the lower bound the proof uses)")
assert min_rooms(demo) == min_rooms_sweep(demo) == max_overlap(demo) == 2
assert min_rooms([]) == 0

rng = random.Random(3)
for _ in range(500):
    iv = []
    for _ in range(rng.randint(0, 9)):
        s = rng.randrange(0, 12)
        iv.append((s, s + rng.randint(1, 6)))
    assert min_rooms(iv) == max_overlap(iv), iv
    assert min_rooms_sweep(iv) == max_overlap(iv), iv
print("500 random inputs: heap = sweep = max overlap, every time")
```

Three lines carry the argument.

`if busy and busy[0] <= s` is the entire greedy decision, and `busy[0]` is the
only element of the heap the algorithm ever inspects. Everything the proof says
about "some room is free" was reduced to "the earliest-freeing room is free",
which is legitimate because if the minimum end time exceeds `s` then so does
every other.

`heapq.heapreplace(busy, e)` keeps the heap size fixed, which is what makes
`return len(busy)` correct. `heappop` then `heappush` gives the same answer more
slowly; `heappush` then `heappop` can pop the element just pushed. Here that
cannot happen, since `e > s >= busy[0]` — but relying on it is how people end up
with a "free room" that has not freed yet.

`return len(busy)` rather than a tracked maximum. It is correct only because the
size never decreases, as the trace showed. Stating that out loud once is cheaper
than maintaining an extra variable forever.

The random cross-check is against `max_overlap`, which is the *definition*
transcribed. Testing an optimised algorithm against the definition, rather than
against a second optimised algorithm, is the habit that catches shared
misconceptions.

## Variants you will meet

**Naming the resource, not just counting it.** Carry two heaps: free ids, and
`(end_time, id)` pairs for the busy ones. Before each request, move everything
whose `end_time` has arrived from busy to free, then pop the smallest free id.
That is *Meeting Room Scheduler* (reject with `-1` when free is empty) and
*API Call Thread Pool Schedule* (never reject: if free is empty, pop the busy
one with the earliest end). *Worker Task Assignment Part 1* keys on total
workload instead of end time; *Schedule Requests to Servers* restricts each
request to servers `0..requests[i]`.

**Closed instead of half-open intervals.** *Get Minimum Cores* runs processes
from `start[i]` through `end[i]` inclusive. Do not flip `<=` to `<`; replace each
`e` by `e + 1` and keep one tested code path. See [[intervals]].

**No times at all, just events.** *Chairs Requirement* gives a string of arrivals
and departures. Nothing to sort: walk it, `+1` on arrival, `-1` on departure,
report the running maximum. The degenerate case of the sweep, and a reminder that
the heap is an optimisation, not the idea.

**Maximum number of non-overlapping meetings.** Opposite question, opposite sort
key: order by *end* and take greedily. The exchange argument is in
[[greedy-exchange]]; sorting by start fails, as the traps below show.

**Weighted selection.** *Maximum Profit in Job Scheduling*, *Cinema Shows* and
*Max Sum of Non-Overlapping Intervals* want maximum total value, and no greedy
works: one fat job can beat any number of thin ones. Sort by end time and run a
[[dp-1d]] recurrence `best[i] = max(best[i-1], profit_i + best[p(i)])`, with
`p(i)` the last job ending at or before job `i` starts, found by
[[binary-search]]. `Θ(n log n)`.

**Deadlines, offline.** Sort by deadline and run; that is the second proof. If
not every job fits, the extension is a *regret heap*: in deadline order, take
every job, and whenever the running time passes the current deadline, evict the
longest job taken so far.

**Deadlines, online.** *Task Scheduler with Dependencies* interleaves `ADD`,
`CONSUME` and `UPDATE`. Keep a min-heap of `(deadline, id)` for tasks whose
dependencies are all consumed, and handle `UPDATE` by pushing a new entry and
leaving the old one to rot — then skip stale tops at pop time.

```python run
import heapq
import itertools
import random


def edf(jobs):
    """jobs = [(duration, deadline)], all released at time 0, one machine, no
    preemption. Run earliest deadline first; return the finishing times, or
    None as soon as some job misses its deadline."""
    t, finish = 0, []
    for p, d in sorted(jobs, key=lambda j: j[1]):
        t += p
        finish.append(t)
        if t > d:
            return None
    return finish


def some_order_works(jobs):
    """Brute force: is ANY order feasible?"""
    for order in itertools.permutations(jobs):
        t = 0
        for p, d in order:
            t += p
            if t > d:
                break
        else:
            return True
    return False


tight = [(4, 4), (1, 5)]
print("jobs (duration, deadline):", tight)
print("earliest deadline first  -> finishes at", edf(tight))
assert edf(tight) == [4, 5]

t = 0
for p, d in sorted(tight):                       # shortest job first
    t += p
    if t > d:
        print("shortest job first       -> misses deadline", d, "at time", t)
        break

rng = random.Random(5)
for _ in range(2000):
    jobs = [(rng.randint(1, 5), rng.randint(1, 14)) for _ in range(rng.randint(0, 6))]
    assert (edf(jobs) is not None) == some_order_works(jobs), jobs
print("2000 random job sets: EDF succeeds exactly when some order does")


def consume_by_deadline(ops):
    """The online form: a lazy heap keyed by (deadline, id). UPDATE leaves a
    stale entry behind, so pop until the top matches the live deadline."""
    live, heap, out = {}, [], []
    for op in ops:
        if op[0] in ("ADD", "UPDATE"):
            live[op[1]] = op[2]
            heapq.heappush(heap, (op[2], op[1]))
        else:
            while heap and live.get(heap[0][1]) != heap[0][0]:
                heapq.heappop(heap)              # stale: this deadline was replaced
            out.append(heapq.heappop(heap)[1] if heap else "NONE")
            live.pop(out[-1], None)
    return out


ops = [("ADD", "a", 9), ("ADD", "b", 3), ("UPDATE", "b", 20),
       ("CONSUME",), ("CONSUME",), ("CONSUME",)]
print("lazy-deletion consume order:", consume_by_deadline(ops))
assert consume_by_deadline(ops) == ["a", "b", "NONE"]
```

**Cooldowns.** The resource is the label itself. *Minimum Days for Fixed-Order
Tasks with Cooldown* forbids reordering: keep a dictionary of the last day each
id ran and jump the clock forward, no heap. *Task Scheduler* allows reordering
and has a closed form: with `M` copies of the commonest label and `K` labels tied
at `M`, the answer is `max(len(tasks), (M - 1) * (n + 1) + K)`. *Priority Job
Scheduler with Cooldowns* needs two heaps — eligible jobs by `(-priority, id)`,
sleeping jobs by wake time — moving jobs across as the clock ticks. See
[[rate-limiting]].

**Precedence, not overlap.** *Course Schedule*, *Course Schedule II* and
*Dependency-Aware Agent Task Scheduler* are [[topological-sort]]. *Task Scheduler
with Dependencies* is both at once: topological availability, heap ordering.

**Partitioning a sequence into days.** *Minimum Effort Task Schedule* keeps tasks
in order and splits them into `deadline` consecutive groups, minimising the sum
of group maxima. Order is fixed, so there is no greedy choice to make: it is
[[partition-dp]], `Θ(n^2 d)`.

**Feasibility by binary search.** When the question is "the minimum capacity /
speed / number of days" rather than an interval count, the schedule becomes a
predicate and you search over the answer. See [[binary-search-on-answer]].

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"the minimum number of rooms / cores / machines / chairs / servers / dock
   bays required"**, with intervals as input. This is the core algorithm, every
   time. The nouns change; the problem does not.
2. **An explicit sentence about touching intervals** — "a meeting that ends at
   time `t` and another that starts at `t` do not overlap". That sentence exists
   because the setter knows the tie is the whole difficulty, and its exact
   wording decides `<=` versus `<`.
3. **"assign to the earliest available worker; break ties by smallest id"** — two
   heaps, one free and one busy.
4. **"at least `n` intervals between two tasks with the same label"**, or the
   word *cooldown* — spacing, not overlap.
5. **"the task with the earliest deadline"**, or operations named `CONSUME` /
   `UPDATE` — earliest-deadline-first with a lazy heap.
6. **Both `start` and `duration` given as separate arrays.** Someone is nudging
   you to compute `end = start + duration` and stop thinking about durations.
   *Cinema Shows* does this.

The anti-signals, which matter more here than in most chapters because the
vocabulary of scheduling is used by problems that are not scheduling problems:

- **Prerequisites, dependencies, "before".** A directed edge, not a time
  interval. [[topological-sort]].
- **A title containing "Schedule" and a body containing no times.** *Filter and
  Sort Scheduled Tasks* is a three-key sort, so [[custom-comparators]];
  *Process Scheduling* counts arrangements with no process in consecutive slots,
  a recurrence; *Work Schedule* enumerates digit strings with a given sum, so
  [[backtracking]].
- **"Maximum total profit / volume."** Not greedy. [[dynamic-programming]].
- **A fixed order you may not change.** If tasks must run in the given sequence,
  there is no scheduling decision left — only simulation of the clock.

## Traps

**The tie rule.** Half-open input with a `<` test, or closed input with `<=`.
Symptom: the answer is off by one only on inputs where some meeting ends exactly
when another begins — so the sample case usually passes. Demonstrated below.

**Forgetting to sort.** Symptom: an answer that is too large and that changes
when you shuffle the input. Unsorted input breaks the proof at its first step.

**Sorting by end time when counting rooms.** A plausible confusion, because the
*other* classic interval greedy does sort by end. Counting resources sorts by
start; selecting non-overlapping intervals sorts by end. Demonstrated below.

**Using a max-heap.** Symptom: rooms are opened almost every time and the answer
approaches `n`. With the *latest* end time on top, "is a room free" is answered by
the room least likely to be free.

**Pushing before popping.** `heappush(busy, e)` then `heappop(busy)` can return
`e` itself. Impossible in this exact algorithm, but not in the worker-assignment
variant, where it hands the next task to a worker who has not started yet.

**Reading `len(busy)` in the wrong variant.** The core heap never shrinks, so its
length is the answer; the two-heap assignment variant does shrink, because
workers move to the free pool. Carrying the habit across is a silent wrong
answer.

**Ignoring the empty input.** Several *Meeting Rooms II* statements say "return 0
when intervals is empty", which means a test does it.

**Assuming the coordinates are small.** `-2147483648 <= start < end <=
2147483647` in the Uber and Walmart *Meeting Rooms II* rules out any array indexed
by time, and the negative bound rules out a sentinel of `0`.

**Stale heap entries after an update.** If a deadline can change, the old
`(deadline, id)` pair is still in the heap, and a task gets consumed at its old
urgency. Fix with lazy deletion, as in the second runnable block.

```python run
import heapq


def rooms(intervals, touching_is_free):
    busy = []
    for s, e in sorted(intervals):
        free = busy and (busy[0] <= s if touching_is_free else busy[0] < s)
        if free:
            heapq.heapreplace(busy, e)
        else:
            heapq.heappush(busy, e)
    return len(busy)


demo = [(0, 30), (5, 10), (15, 20), (25, 40), (30, 45)]
print("A. the tie rule, on", demo)
print("   half-open [s, e), '<=' :", rooms(demo, True), " correct")
print("   closed    [s, e], '<'  :", rooms(demo, False),
      " one room too many for a half-open statement")
assert rooms(demo, True) == 2 and rooms(demo, False) == 3

# Closed intervals (a process runs THROUGH end[i]) are the same code on e + 1.
closed = [(1, 2), (2, 3), (3, 4)]
print("   closed inputs, shifted :", rooms([(s, e + 1) for s, e in closed], True),
      "cores for", closed, "- shifting beats flipping the test")
assert rooms([(s, e + 1) for s, e in closed], True) == 2

print()
print("B. choosing the most non-overlapping meetings")
iv = [(1, 10), (2, 3), (4, 5), (6, 7)]


def pick(intervals, key):
    taken, last_end = [], float("-inf")
    for s, e in sorted(intervals, key=key):
        if s >= last_end:
            taken.append((s, e))
            last_end = e
    return taken


print("   meetings          ", iv)
print("   sorted by end     ", pick(iv, lambda x: x[1]), "-> 3 meetings, optimal")
print("   sorted by start   ", pick(iv, lambda x: x[0]), "-> 1, the long one ate the day")
assert len(pick(iv, lambda x: x[1])) == 3
assert len(pick(iv, lambda x: x[0])) == 1

print()
print("C. counting rooms sorts by START; picking meetings sorts by END.")
print("   Same data, opposite keys, because the questions are opposite:")
print("   'how many resources must I buy' vs 'how much can one resource hold'.")
```

## What to memorise

One template, one sentence, one habit.

**The template**, which should come out of your fingers without thought:

```python
import heapq

def min_rooms(intervals):
    busy = []                        # end times of the rooms in use
    for s, e in sorted(intervals):   # by start time
        if busy and busy[0] <= s:    # <= for half-open, < for closed
            heapq.heapreplace(busy, e)
        else:
            heapq.heappush(busy, e)
    return len(busy)                 # the heap never shrinks
```

**The sentence** that turns a statement into it: *"Sort by when each commitment
begins, keep a heap of when the commitments end, and the only question you ever
ask the past is whether the earliest one has finished."*

**The habit**: before writing the loop, copy the statement's own sentence about
touching intervals into a comment, and write the comparison from that comment
rather than from memory. Half the wrong answers on this topic are one character,
and the problem chooses that character, not you.

Numbers worth carrying:

- Minimum resources equals the maximum number of intervals alive at one instant,
  and that maximum is always attained at some *start* time.
- `n` meetings cost exactly `n` heap operations — never `2n`.
- Counting resources sorts by start; picking non-overlapping intervals sorts by
  end; maximising value is not a sort at all.
- *Task Scheduler* with `M` copies of the commonest label, `K` labels tied at
  `M`, gap `n`: `max(len(tasks), (M - 1) * (n + 1) + K)`.
- A difference array beats sorting only when the time range is comparable to `n`.

## Check yourself

:::check
Why can the algorithm never open more rooms than the busiest instant needs? Give
the reason, not the loop.
--
Because a room is opened only in the `m > s` case, and in that case the heap's
minimum end time exceeds `s` — meaning *every* open room's last meeting is still
running at `s`. Each of those `r` meetings started at or before `s` (the input is
sorted) and ends after `s`, so each is alive at `s`; they sit in distinct rooms,
so they are distinct meetings; and the arriving meeting is alive at `s` too.
That is `r + 1` meetings simultaneously alive at one instant.

So every time the room count rises to `r + 1`, an instant exists at which
`r + 1` meetings genuinely overlap — and no assignment whatsoever can serve
`r + 1` pairwise-overlapping meetings with `r` rooms. The count is not merely
small; each increment carries its own proof of necessity.
:::

:::check
Someone says: "the classic interval greedy sorts by end time, so *Meeting Rooms
II* should sort by end time too." Where are they wrong?
--
They have merged two different questions that happen to share an input type.

Sorting by end time is right for *selecting* a maximum set of mutually
non-overlapping intervals for **one** resource: finishing early leaves the most
room for what follows. Sorting by start time is right for *counting* the
resources needed to run **all** the intervals: the event that can force a new
resource is an arrival, and arrivals must be considered in the order they happen.

The runnable block in the traps section shows both on data where each key gives
the wrong answer to the other question. The test to apply: am I dropping
intervals, or keeping all of them? If none may be dropped, sort by start.
:::


:::check
*Cinema Shows* asks for the maximum total audience over non-overlapping
screenings. Why can you not sort by end time and take greedily, as you would for
"the most non-overlapping meetings"?
--
Because the objective is no longer the count. The greedy for maximum *count*
rests on an exchange argument: replacing the first chosen interval with the one
that ends earliest never hurts, since finishing earlier can only widen what
remains. That compares two options worth **one each**. When intervals carry
different values the swap can lose more than the extra room recovers — one
screening with an audience of 1000 outweighs three with 10.

The right tool is dynamic programming over end times:
`best[i] = max(best[i-1], volume_i + best[p(i)])`, with `p(i)` the last screening
finishing at or before screening `i` starts, located by binary search.
`Θ(n log n)`, and it keeps *both* options at each step instead of committing.
See [[dp-1d]]; the failure here is why [[greedy-exchange]] arguments must be
checked rather than assumed.
:::

:::check
In the online scheduler, a task's deadline is updated after it was pushed into
the heap. Why is deleting the old entry the wrong instinct, and what does the
lazy version cost?
--
A binary heap supports "give me the minimum", not "find this element". Locating
the stale pair means a linear scan, and removing it from the middle means
repairing the heap by hand — `O(n)` per update, and a bug factory.

Lazy deletion keeps the live deadline in a dictionary, pushes a *new* entry on
every update and leaves the old one in place; at pop time you discard any top
that disagrees with the dictionary. The heap then holds one entry per operation
rather than one per task, so memory is `O(m)` and a pop may discard several
stale tops — but each entry is pushed once and discarded at most once, so the
total discarding work is `O(m log m)` across the whole run. That amortised
argument is why the unbounded-looking inner `while` is cheap.
:::

:::check
You are given 2,000,000 meetings with times between 1 and 2,000,000, and asked
only for the number of rooms. What would you write, and why not the heap?
--
A difference array over the time axis: `delta[s] += 1`, `delta[e] -= 1` for each
meeting (half-open, so the decrement lands exactly on the end), then one prefix
scan taking the running maximum. `Θ(T + n)` with `T = 2 * 10^6`.

The heap version is `Θ(n log n)`, roughly `4 * 10^7` tuple comparisons at this
size, plus a sorted copy of two million tuples. It is not *wrong* — it is the
general algorithm, and the only option when times reach `10^9`, as in *Get
Minimum Cores*. The point is that the constraint line, not the title, chooses
between them.
:::
