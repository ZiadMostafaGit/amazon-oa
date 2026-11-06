# Topological Sort

> Something with no unfinished prerequisites can always go next and can never be a wrong choice, so you keep a count of what each task still owes, take any task that owes nothing, pay its dependents' debts, and repeat; when nothing owes nothing but tasks remain, the leftovers are a cycle.

## The problem it solves

Six tasks, a to f, and six rules of the form "this must be done before that":

```
d before a     d before b     a before c
b before c     c before f     e before f
```

Put all six tasks in a single line so that every rule is respected. One answer
is `d a b c e f`. Another is `e d b a c f`. Many orders work, and the job is to
find one, or to say that none exists.

That is topological sort. The rules are a directed graph: an arrow u → v for
each "u before v", and a valid line is an order of the nodes in which every
arrow points forward. [[p:inmobi-course-schedule|Course Schedule]] asks only
whether such an order exists. [[p:chainalysis-lexicographically-smallest-course-order|Course Schedule II]]
asks for one, and when several tasks could go next, the smallest. And once you
have the order, a second family opens up: [[p:headlands-dependency-job-schedule|Earliest Dependency Schedule]]
gives each task a duration and asks when each one can start if any number can
run at once. The order is then not the answer but the sequence in which to
compute the answer.

<svg viewBox="0 0 520 220" role="img" aria-label="six tasks: d before a and b, a and b before c, c and e before f; d and e owe nothing at the start and are shaded">
  <g>
    <line x1="76.6" y1="66.2" x2="163.7" y2="46.1"/>
    <polygon class="fill" points="173.4,43.8 164.8,50.9 162.6,41.2"/>
    <line x1="75.9" y1="76.1" x2="164.8" y2="110.3"/>
    <polygon class="fill" points="174.1,113.9 163.0,115.0 166.6,105.6"/>
    <line x1="206.2" y1="45.0" x2="294.2" y2="72.1"/>
    <polygon class="fill" points="303.8,75.0 292.7,76.8 295.7,67.3"/>
    <line x1="206.2" y1="115.0" x2="294.2" y2="87.9"/>
    <polygon class="fill" points="303.8,85.0 295.7,92.7 292.7,83.2"/>
    <line x1="335.4" y1="87.1" x2="425.5" y2="128.7"/>
    <polygon class="fill" points="434.6,132.9 423.4,133.2 427.6,124.1"/>
    <line x1="76.9" y1="168.7" x2="423.1" y2="142.1"/>
    <polygon class="fill" points="433.1,141.3 423.5,147.1 422.7,137.1"/>
    <circle class="fill" cx="60" cy="70" r="17"/>
    <text x="60" y="75" text-anchor="middle">d</text>
    <circle class="fill" cx="60" cy="170" r="17"/>
    <text x="60" y="175" text-anchor="middle">e</text>
    <circle cx="190" cy="40" r="17"/>
    <text x="190" y="45" text-anchor="middle">a</text>
    <circle cx="190" cy="120" r="17"/>
    <text x="190" y="125" text-anchor="middle">b</text>
    <circle cx="320" cy="80" r="17"/>
    <text x="320" y="85" text-anchor="middle">c</text>
    <circle cx="450" cy="140" r="17"/>
    <text x="450" y="145" text-anchor="middle">f</text>
    <text x="260" y="210" text-anchor="middle">shaded: in-degree 0 at the start, so either may go first</text>
  </g>
</svg>

The first solution anyone writes is "try every order". Six tasks have 6! = 720
orders. Check each against the six rules, keep one that passes. Correct, and
fine for six. Ten tasks have 3.6 million orders, twenty have 2.4 x 10^18, and
[[p:chainalysis-lexicographically-smallest-course-order|Course Schedule II]]
allows 2000 courses.

The second solution anyone writes is a sort. Two popular keys, both wrong.

- **"Sort by the number of prerequisites: tasks that need nothing first, tasks
  that need the most last."** Three tasks, c before b, b before a. c needs 0,
  b needs 1, a needs 1. Sorted by count and then by name: c, a, b. But a needs
  b. The count says how many rules point at a task, not how *deep* it is.
- **"Sort alphabetically, or by id."** On the six tasks, `a b c d e f` puts a
  before d, and d must come first. The order the rules ask for has nothing to do
  with the names.

What this chapter builds is exact like the brute force and runs in one pass over
the rules: n + m steps for n tasks and m rules. It comes in two forms that are
worth knowing equally: **Kahn's algorithm**, which repeatedly removes a task
that owes nothing, and **DFS post-order**, which places a task only after
everything it depends on. It rests on [[graphs]] for the representation and on
[[dfs]] for the second form.

### When it is the wrong tool

- **The relation has no direction.** "a conflicts with b" or "a and b are
  connected" does not say which comes first. That is [[bipartite]],
  [[union-find]] or plain search, not an order.
- **The cycles are the point.** If the graph has cycles and you still need an
  answer ("group mutually dependent modules"), contract the cycles first with
  [[strongly-connected]], then sort the result.
- **You must list or count every valid order.** There can be n! of them (no
  rules at all). Listing them is [[backtracking]]; counting them is hard in
  general and only feasible with [[dp-bitmask]] for about 20 tasks.
- **The order is by a key.** "Process by deadline" with no relation between
  tasks is [[sorting]]. The word "order" alone does not mean this chapter.

## Build it from the brute force

### Step 1: build the line one position at a time

"Try every order" can be written as a sequence of decisions: choose the first
task, then the second, and so on. At each position, try every task not yet
placed, and back up if you get stuck. That is [[backtracking]], and it is the
brute force in a more useful shape, because now we can ask a sharper question
than "is this whole order valid?". We can ask: **which tasks are allowed to go
first?**

A task can go first only if no rule says something must come before it. In the
six-task example that is d and e. a cannot go first (d must precede it), and
neither can b, c or f. Call a task with no unfinished prerequisites **ready**.

Now place d. What is left is the same kind of problem, smaller: five tasks, and
the rules that do not mention d. In that smaller problem, which tasks are ready?
a and b no longer have any prerequisite left, so a, b and e are. Place one, and
again what is left is the same problem, smaller.

So the brute force becomes: "repeatedly choose a ready task and place it". The
only question left is which ready task to choose, and whether a bad choice can
get you stuck.

### You might think: "If I choose the wrong ready task, I may have to back up."

This is the instinct that makes people reach for backtracking, and it is wrong.
Choosing a ready task can never make the rest impossible.

Here is why, in words. Suppose a valid order for the remaining tasks exists, and
t is ready. Take that valid order and move t to the front. Every rule that
involves t says "something before t" or "t before something". There are no rules
of the first kind left (t is ready). Rules of the second kind are still satisfied
with t at the front, since t is now before everything. All other rules are
untouched, because the relative order of the other tasks did not change. So
there is still a valid order that starts with t.

Say it a second way. Doing a ready task only ever *removes* obstacles: it
satisfies rules, it never creates any. A task that was going to be possible is
still possible. So no choice among ready tasks is a mistake, and you never need
to back up. Backtracking collapses into a single greedy pass.

This also explains why so many problems specify a tie rule
([[p:chainalysis-lexicographically-smallest-course-order|Course Schedule II]]:
"choose the smallest numbered course next"). Any ready task is correct, so the
problem has to tell you which one it wants, if it wants a single answer.

### You might think: "A task that cannot be placed now just has to wait for luck."

Suppose at some point no task is ready, but tasks remain. Every remaining task
has a prerequisite that is also remaining. Pick any of them, x. It needs some
remaining y. y needs some remaining z. Keep walking back. There are finitely
many tasks, so you must eventually return to one you have already seen, and the
tasks between the two visits form a loop: x needs y needs z needs x. That is a
**cycle**, and no order can satisfy it, because each of them would have to come
before itself.

So "stuck" is not bad luck. Stuck means "there is a cycle among the leftovers",
and "nothing ever got stuck" means "there is no cycle". The same loop that
builds the order decides whether one exists. That is how
[[p:inmobi-course-schedule|Course Schedule]] is answered: run the loop and check
whether every course was placed.

### Step 2: count it

The greedy is now correct. How fast is it, written plainly?

```
while tasks remain:
    for each remaining task t:                    # find a ready one
        if no rule (u before t) has u remaining:  # scan every rule
            place t; break
    else: report a cycle
```

Finding one ready task scans the remaining tasks and, for each, the rules: up to
n x m work. Doing that n times is n^2 x m in the worst case, and even a smarter
"for each task, scan its own incoming rules" is n x (n + m) over the run. For
2000 courses and 5000 rules that is around 10^7, survivable; for 10^5 tasks and
2 x 10^5 rules it is 3 x 10^10, not.

### Step 3: notice the waste

Every round, the plain version re-counts, for every remaining task, how many of
its prerequisites are still unfinished. But between one round and the next,
exactly one task was placed. Only the tasks that depended on *that* task can
have changed. Everything else is recounted for nothing.

On the six tasks: after placing d, the counts of a and b drop by one. The counts
of c, e and f are what they were. Recomputing them is pure repetition.

### The question that unlocks it

Ask, every time a task is placed:

**What can go first, right now, and what does placing it unlock?**

The first half is the greedy: anything that owes nothing. The second half is
what makes it fast: placing a task only changes the tasks that were waiting for
it, so only they need to be looked at. Keep, for every task, a number
`indeg[t]`, how many of its prerequisites are still unfinished. It starts as the
number of arrows into t (its **in-degree**). Placing u lowers it by one for each
arrow u → v. When a number reaches 0, that task has just become ready, so put it
in a container of ready tasks. The container is never searched; things are put
in exactly when they become ready.

Think of `indeg[t]` as a debt, not as a property of the picture. It is the
number of promises still owed to t, and it only ever goes down.

### Step 4: the loop, with the counter

```
indeg[v] = number of arrows into v
ready    = every v with indeg[v] == 0         # from ALL tasks, not from the rules
order    = []
while ready:
    u = take any task out of ready
    order.append(u)
    for v in out[u]:                          # every arrow u -> v
        indeg[v] -= 1                         # pay one debt
        if indeg[v] == 0:                     # v just became ready
            ready.add(v)
if len(order) < n: there is a cycle
```

Each task enters `ready` once (its debt crosses zero once, since it only goes
down) and leaves once, and when it leaves, each of its arrows is looked at once.
The total is n + m. This is **Kahn's algorithm**.

The container can be anything. A queue gives one order, a stack another, a
min-heap gives the smallest order (Course Schedule II), a heap keyed by first
appearance in the input gives "input order". The choice never affects
correctness, only which of the valid answers you get. That is the "any ready
task is safe" argument, written as code.

### Step 5: the other way round, from the end

There is a second derivation, which starts from the opposite question: **what
can go last?** Anything that nothing else depends on. Equivalently: a task can be
placed once everything that must come *after* it has been placed, if you build
the line from the right.

That is what [[dfs]] gives you for free. Run DFS along the arrows. A node
**finishes** when the DFS has explored everything reachable from it. Everything
that must come after u is reachable from u, so it all finishes before u does.
Write nodes down in the order they finish (**post-order**), and you have a line
in which every task appears after everything that depends on it. Reverse it, and
every task appears before everything that depends on it: a topological order.

### You might think: "DFS visits a task before the tasks after it, so the visiting order is already topological."

No. The order DFS *enters* nodes (pre-order) is not topological. The smallest
counterexample: rules a before c, and b before c. DFS from a enters a, then c.
Then from b it enters b. Pre-order: a, c, b. But b must come before c.

What went wrong: entering c says only that *some* prerequisite of c (a) was
entered first, not that *all* of them were. Finishing is different. c finishes
when everything after c is done, and that is the guarantee we need. Post-order
from a and then b: c finishes, then a, then b, giving [c, a, b]; reversed,
[b, a, c], which is valid. The one line that differs between the wrong and the
right version is *where* the node is written down: before its neighbours are
explored, or after. It gets its own demonstration in code.

DFS also needs three marks, not two, to detect a cycle: an arrow to a node that
is **still being explored** (on the current route) is a cycle; an arrow to a node
that is **finished** is not. The [[graphs]] chapter derives this; the diamond
a→b, a→c, b→d, c→d is the case a single visited mark gets wrong.

### Step 6: use the order to compute something

Once tasks are in topological order, any quantity defined by "the value of v
depends on the values of its prerequisites" can be computed in one left-to-right
pass, because when you reach v, every prerequisite is already done and will
never change. With durations and unlimited workers:

```
finish[v] = duration[v] + max(finish[u] for every prerequisite u of v)
```

(and just duration[v] if v has none). That is the earliest time each task can
finish, and the largest finish is the length of the whole project. It is the
longest path in the graph, weighted by durations: the **critical path**. In a
general graph the longest simple path is a famously hard problem. On a graph
with no cycles it is this one pass. This is [[dynamic-programming]] where the
topological order is the evaluation order, and it is called **DP on a DAG** (a
DAG is a directed acyclic graph).

### The technique in one sentence

**Topological sort: keep, for every task, the number of unfinished
prerequisites; repeatedly take any task whose number is zero, place it, and lower
the numbers of the tasks waiting on it; since doing a ready task never creates
an obstacle, any choice is safe, and if the ready set empties early the
leftovers contain a cycle.**

And the question that produced it: **what can go first right now, and what does
placing it unlock?**

## Worked by hand

Get a pen. The six tasks: arrows d→a, d→b, a→c, b→c, c→f, e→f. Starting debts:

```
a:1  b:1  c:2  d:0  e:0  f:2
```

The six debts add up to 6, one per arrow. That is a useful check: the in-degrees
always add up to the number of rules.

### Kahn's algorithm, smallest ready task first

The ready set is a min-heap, so the smallest name comes out.

| step | take out | debts paid | ready after | order so far |
|---|---|---|---|---|
| start | | | {d, e} | |
| 1 | d | a 1→0, b 1→0 | {a, b, e} | d |
| 2 | a | c 2→1 | {b, e} | d a |
| 3 | b | c 1→0 | {c, e} | d a b |
| 4 | c | f 2→1 | {e} | d a b c |
| 5 | e | f 1→0 | {f} | d a b c e |
| 6 | f | none | {} | d a b c e f |

Six tasks placed out of six, so there is no cycle, and `d a b c e f` is valid.

Step 3, told in full:

> "The ready set is {b, e}. The smallest is b, so I take it and write it down.
> Which tasks were waiting for b? Only c. c owed two things, a and b; a was paid
> at step 2, so c owed one, and now that b is done it owes zero. c has just
> become ready, so it goes into the ready set, which is now {c, e}. Nothing else
> changed: e still owes nothing, as it has since the start, and f still owes two."

Three things the table shows that the code hides.

**Every arrow was paid exactly once.** Read down the "debts paid" column: d→a,
d→b, a→c, b→c, c→f, e→f, each once, at the step its tail was taken out. That is
why the run costs n + m.

**e was ready from the start and came out at step 5.** Being ready is not being
urgent. Under the smallest-first rule, a, b and c went ahead of it because they
are smaller and became ready in time.

**The output is not sorted.** It starts `d a b`, because d had to come first.
Sorting the output would destroy it.

### The same graph with a plain queue

Seed the queue with the ready tasks in name order: [d, e].

| take out | debts paid | queue after | order |
|---|---|---|---|
| d | a→0, b→0 | [e, a, b] | d |
| e | f 2→1 | [a, b] | d e |
| a | c 2→1 | [b] | d e a |
| b | c→0 | [c] | d e a b |
| c | f→0 | [f] | d e a b c |
| f | | [] | d e a b c f |

A different valid order, `d e a b c f`. The queue processes tasks in waves:
first everything ready at the start (d, e), then everything those unlocked
(a, b), and so on. That wave structure is a variation of its own (stages).

### A run that gets stuck

Four tasks: p→x, x→y, y→z, z→x. Debts: p 0, x 2, y 1, z 1.

| take out | debts paid | ready after | order |
|---|---|---|---|
| start | | {p} | |
| p | x 2→1 | {} | p |

The ready set is empty, and only 1 of the 4 tasks was placed. Look at the
leftovers {x, y, z} and their debts: x owes 1 (to z), y owes 1 (to x), z owes 1
(to y). Every leftover owes something to another leftover. Walk back from x: x
waits on z, z waits on y, y waits on x. There is the cycle x → y → z → x, found
by the exact argument from the derivation.

Note what the in-degree of x was: 2. One debt came from p, outside the cycle, and
it was paid. The other came from z, inside the cycle, and could never be paid.
That is the general shape: a cycle's debts are owed in a ring.

### DFS post-order, by hand

Same six tasks, out-lists in rule order: d [a, b], a [c], b [c], c [f], e [f].
Start a DFS from each task in name order, skipping finished ones. "enter" is the
pre-order, "finish" is the post-order.

```
enter a
  enter c
    enter f
    finish f                      post: f
  finish c                        post: f c
finish a                          post: f c a
enter b
  c is finished, skip
finish b                          post: f c a b
(c is finished)
enter d
  a, b finished, skip
finish d                          post: f c a b d
enter e
  f finished, skip
finish e                          post: f c a b d e
(f is finished)
```

Post-order f c a b d e, reversed: **e d b a c f**. Check the rules: d before a
and b, yes; a and b before c, yes; c and e before f, yes. A third valid order.

And the pre-order, the order nodes were *entered*: a, c, f, b, d, e. It breaks
four of the six rules: d→a, d→b, b→c and e→f. This is the counterexample from the
derivation, on the real example.

### A second trace: what the order is for

Durations: a 3, b 2, c 4, d 1, e 6, f 2, unlimited workers. Walk the order
`d a b c e f` once, and for each task push its finish time to its dependents:
`finish[v] = max(finish[v], finish[u] + dur[v])`, starting from `finish[v] =
dur[v]`.

| take | finish[u] | pushes | finish after |
|---|---|---|---|
| start | | | a3 b2 c4 d1 e6 f2 |
| d | 1 | a = max(3, 1+3) = 4; b = max(2, 1+2) = 3 | a4 b3 c4 d1 e6 f2 |
| a | 4 | c = max(4, 4+4) = 8 | c8 |
| b | 3 | c = max(8, 3+4) = 8 | c8 (no change) |
| c | 8 | f = max(2, 8+2) = 10 | f10 |
| e | 6 | f = max(10, 6+2) = 10 | f10 (no change) |
| f | 10 | none | |

Finish times a 4, b 3, c 8, d 1, e 6, f 10. Start times (finish minus duration):
a 1, b 1, c 4, d 0, e 0, f 8. The project ends at 10.

The cell to stare at is c. It waits for a (done at 4) and b (done at 3). b's push
at step 3 changes nothing, because a's was later. c starts at 4, the *latest*
finish among its prerequisites, not the sum, because a and b run at the same
time. The chain that set the answer is d → a → c → f, 1 + 3 + 4 + 2 = 10: the
critical path. e, six units long, has slack: it could start as late as time 2
and nothing would move.

Why it had to be in topological order: when the pass reaches c, both a and b
have already pushed. If c were processed before b, c's finish would be computed
before b's contribution arrived. Here that would have been harmless by luck, but
make b take 10 and it would not be.

## From the idea to the code

### First: the brute force and the counter

This block compares the brute force over all orders with Kahn's algorithm, and
counts the work of the "rescan every round" version against the counter version
on a long chain.

```python run
from itertools import permutations
from collections import deque
import random

def valid(order, n, edges):
    pos = {v: i for i, v in enumerate(order)}
    return len(order) == n and all(pos[u] < pos[v] for u, v in edges)

def kahn(n, edges):
    out, indeg = [[] for _ in range(n)], [0] * n
    for u, v in edges:
        out[u].append(v)
        indeg[v] += 1
    ready = deque(v for v in range(n) if indeg[v] == 0)
    order, work = [], 0
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in out[u]:
            work += 1
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return (order if len(order) == n else None), work

def rescan(n, edges):                       # the plain greedy: recount every round
    placed, order, work = set(), [], 0
    while len(order) < n:
        for t in range(n):
            if t in placed:
                continue
            work += len(edges)              # scan every rule to see if t is ready
            if all(u in placed for u, v in edges if v == t):
                placed.add(t)
                order.append(t)
                break
        else:
            return None, work
    return order, work

tasks = "abcdef"
E = [(3, 0), (3, 1), (0, 2), (1, 2), (2, 5), (4, 5)]      # d->a, d->b, a->c, ...
good = [p for p in permutations(range(6)) if valid(p, 6, E)]
print("valid orders of the six tasks:", len(good), "of 720")
assert len(good) == 10
order, _ = kahn(6, E)
print("Kahn (queue):", " ".join(tasks[v] for v in order))
assert valid(order, 6, E) and tuple(order) in good

n = 120
chain = [(i + 1, i) for i in range(n - 1)]   # n-1 before n-2 before ... before 0
_, w_kahn = kahn(n, chain)
_, w_scan = rescan(n, chain)
print("chain of %d: counter work %d, rescanning work %d" % (n, w_kahn, w_scan))
assert w_kahn == n - 1 and w_scan > 1000 * w_kahn

random.seed(5)
for _ in range(300):                        # Kahn finds an order iff one exists
    n = random.randint(1, 6)
    E2 = [(u, v) for u in range(n) for v in range(n) if u != v and random.random() < 0.25]
    got, _ = kahn(n, E2)
    exists = any(valid(p, n, E2) for p in permutations(range(n)))
    assert (got is not None) == exists and (got is None or valid(got, n, E2))
print("Kahn == brute force on 300 random graphs, with and without cycles")
```

The six tasks have 10 valid orders out of 720. Kahn finds one of them in six
steps. On the chain, the rescanning version's work grows like n^3 (n rounds, up
to n tasks scanned per round, m rules per scan), and the counter's is n - 1.

### The direct version: Kahn with a heap, and DFS post-order

```python run
import heapq

def topo_kahn(nodes, rules):
    """rules are (before, after). Smallest ready task first. None on a cycle."""
    out = {v: [] for v in nodes}
    indeg = {v: 0 for v in nodes}
    for before, after in rules:
        out[before].append(after)
        indeg[after] += 1
    ready = [v for v in nodes if indeg[v] == 0]   # seed from ALL nodes
    heapq.heapify(ready)
    order = []
    while ready:
        u = heapq.heappop(ready)                  # any ready task is safe
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1                         # pay one debt
            if indeg[v] == 0:                     # crosses zero exactly once
                heapq.heappush(ready, v)
    return order if len(order) == len(nodes) else None

def topo_dfs(nodes, rules):
    """Reverse post-order. None on a cycle. White 0, grey 1, black 2."""
    out = {v: [] for v in nodes}
    for before, after in rules:
        out[before].append(after)
    colour = {v: 0 for v in nodes}
    post = []
    def finish_from(u):
        colour[u] = 1                             # on the current route
        for v in out[u]:
            if colour[v] == 1:
                return False                      # an arrow back into the route
            if colour[v] == 0 and not finish_from(v):
                return False
        colour[u] = 2
        post.append(u)                            # written down AFTER its successors
        return True
    for u in nodes:
        if colour[u] == 0 and not finish_from(u):
            return None
    return post[::-1]

def respects(order, nodes, rules):
    pos = {v: i for i, v in enumerate(order)}
    return sorted(order) == sorted(nodes) and all(pos[a] < pos[b] for a, b in rules)

nodes = list("abcdef")
rules = [("d", "a"), ("d", "b"), ("a", "c"), ("b", "c"), ("c", "f"), ("e", "f")]
k, d = topo_kahn(nodes, rules), topo_dfs(nodes, rules)
print("Kahn, smallest first:", " ".join(k))
print("DFS reverse post-order:", " ".join(d))
assert k == list("dabcef") and d == list("edbacf")
assert respects(k, nodes, rules) and respects(d, nodes, rules)

cyc = [("p", "x"), ("x", "y"), ("y", "z"), ("z", "x")]
print("stuck graph:", topo_kahn(list("pxyz"), cyc), topo_dfs(list("pxyz"), cyc))
assert topo_kahn(list("pxyz"), cyc) is None and topo_dfs(list("pxyz"), cyc) is None
assert topo_kahn(["s"], [("s", "s")]) is None                  # a self-loop
assert topo_kahn(list("abz"), [("a", "b")]) == ["a", "b", "z"]  # isolated z kept
print("diamond:", topo_dfs(list("abcd"), [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]))
assert topo_dfs(list("abcd"), [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]) is not None
```

### Each line, and which idea it is

| line | in plain words | in the derivation |
|---|---|---|
| `for before, after in rules` | name the pair by its meaning | the arrow points before → after |
| `out[before].append(after)` | who is waiting on `before` | "what does placing it unlock" |
| `indeg[after] += 1` | one more debt for `after` | the counter replaces the rescan |
| `ready = [v for v in nodes if ...]` | everything that owes nothing at the start | "what can go first"; from nodes, so isolated tasks are kept |
| `heappop(ready)` | take one ready task | any choice is safe; the heap is the tie rule |
| `indeg[v] -= 1` | one debt of v is paid | only the tasks waiting on u change |
| `if indeg[v] == 0` | v just became ready | it crosses zero once, so it is pushed once |
| `len(order) == len(nodes)` | did everything get placed? | stuck means cycle |
| `colour[u] = 1` ... `colour[u] = 2` | on the route, then finished | three marks: grey arrows are cycles |
| `post.append(u)` after the loop | write u once all its successors are written | post-order |
| `post[::-1]` | flip it | "what can go last", read from the right |

Some boring confusions, settled.

**Which way does the arrow point?** Whatever the statement calls the pair, draw
the arrow from the thing that must happen first to the thing that waits. In
[[p:inmobi-course-schedule|Course Schedule]] a pair is `[course, prerequisite]`,
so the arrow is prerequisite → course, the *reverse* of the pair's order. In
[[p:headlands-dependency-job-schedule|Earliest Dependency Schedule]] a pair is
`[before, after]`, in the natural order. In
[[p:applied-intuition-compilation-order-topological-sort|Compilation Order]] a
pair `[a, b]` means "a depends on b", so b → a. Name the variables by meaning
(`before, after`) at the moment you unpack the pair, and the rest of the code
cannot get it wrong.

**`== 0`, not `<= 0`.** If the counting is right they are the same. If it is
wrong (a duplicate rule counted once and paid twice), `<= 0` pushes a task twice
and produces an order with a repeat; `== 0` never pushes it at all, and the
length check reports the problem. Prefer the version that fails loudly.

**Why seed from the nodes?** A task in no rule has in-degree 0 and must appear in
the order. If you collect nodes from the rules, it does not exist, and in
problems where the task list is given separately (Course Schedule numbers them 1
to numCourses) the length check then compares against the wrong n.

**1-based numbering.** [[p:inmobi-course-schedule|Course Schedule]] numbers
courses 1 to numCourses: either allocate numCourses + 1 slots and seed from
range(1, numCourses + 1), or subtract one on reading.

**Recursion.** `topo_dfs` is recursive, so a chain of 10^5 tasks needs 10^5
frames, beyond CPython's default limit of about 1000. Kahn's loop has no such
limit, which is one reason it is the default in interviews.

### The subtle line, both ways

In the DFS version the whole difference between right and wrong is one line:
where the node is written down. Before its successors are explored (pre-order)
is wrong. After (post-order), then reversed, is right.

On the rules a → c, b → c, nodes visited in the order a, b, c:

```
Pre-order (wrong)                     Post-order, reversed (right)
enter a      write a      [a]         enter a
  enter c    write c      [a c]         enter c, finish c  write c  [c]
enter b      write b      [a c b]     finish a             write a  [c a]
                                      enter b (c is done)
                                      finish b             write b  [c a b]
result a c b                          reversed: b a c
c is written before b   *             every task after all its prerequisites
```

The starred line is where pre-order goes wrong. When c was entered, only one of
its prerequisites, a, had been seen. b had not been reached yet, because it is
not reachable from a at all. Entering a node says "one route led here", not
"everything that must precede it is done". Finishing says something much
stronger: everything that must come *after* the node is already written. Put
plainly: **pre-order follows one route; post-order waits for all of them.**

There is a second form of the same line. If your arrows point the other way,
from a task to the things it needs ("package → dependency", as in
[[p:amazon-package-dependency-order|Package Dependency Order]]), then the
post-order itself, *not reversed*, is the install order: a package is written
only after all its dependencies are. Reverse it and you get it backwards. The
rule is: post-order lists each node after everything its arrows lead to. Decide
which way your arrows point, and reverse only if they point from "before" to
"after".

```python run
def orders(nodes, arrows):
    out = {v: [] for v in nodes}
    for u, v in arrows:
        out[u].append(v)
    seen, pre, post = set(), [], []
    def go(u):
        seen.add(u)
        pre.append(u)                       # written when entered
        for v in out[u]:
            if v not in seen:
                go(v)
        post.append(u)                      # written when finished
    for u in nodes:
        if u not in seen:
            go(u)
    return pre, post

def respects(order, rules):
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[a] < pos[b] for a, b in rules)

rules = [("a", "c"), ("b", "c")]            # (before, after)
pre, post = orders(list("abc"), rules)
print("pre-order:", pre, "valid?", respects(pre, rules))
print("post-order reversed:", post[::-1], "valid?", respects(post[::-1], rules))
assert pre == ["a", "c", "b"] and not respects(pre, rules)
assert post[::-1] == ["b", "a", "c"] and respects(post[::-1], rules)

six = [("d", "a"), ("d", "b"), ("a", "c"), ("b", "c"), ("c", "f"), ("e", "f")]
pre, post = orders(list("abcdef"), six)
bad = [(a, b) for a, b in six if pre.index(a) > pre.index(b)]
print("six tasks, pre-order", "".join(pre), "breaks", bad)
print("six tasks, reversed post-order", "".join(post[::-1]))
assert bad == [("d", "a"), ("d", "b"), ("b", "c"), ("e", "f")]
assert respects(post[::-1], six)

# arrows from a package to what it needs: post-order itself is the install order
needs = [("app", "lib"), ("app", "log"), ("lib", "core"), ("log", "core")]
_, post = orders(["app", "lib", "log", "core"], needs)
install = post                               # NOT reversed
print("install order:", install)
assert all(install.index(dep) < install.index(pkg) for pkg, dep in needs)
assert not all(post[::-1].index(dep) < post[::-1].index(pkg) for pkg, dep in needs)
```

### DP on the DAG: the order put to work

```python run
from collections import deque
from itertools import permutations

def kahn(n, rules):
    out, indeg = [[] for _ in range(n)], [0] * n
    for u, v in rules:
        out[u].append(v)
        indeg[v] += 1
    q = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order, out

def schedule(dur, rules):                     # earliest start and finish
    order, out = kahn(len(dur), rules)
    start = [0] * len(dur)
    for u in order:                           # u is final when we reach it
        for v in out[u]:
            start[v] = max(start[v], start[u] + dur[u])
    flat = []
    for i in range(len(dur)):
        flat += [start[i], start[i] + dur[i]]
    return flat

def longest_path_edges(n, rules):             # the most edges on any path
    order, out = kahn(n, rules)
    best = [0] * n                            # an isolated node: length 0
    for u in order:
        for v in out[u]:
            best[v] = max(best[v], best[u] + 1)
    return max(best, default=0)

def stages(n, rules):                         # Kahn one whole wave at a time
    out, indeg = [[] for _ in range(n)], [0] * n
    for u, v in rules:
        out[u].append(v)
        indeg[v] += 1
    wave, result = sorted(v for v in range(n) if indeg[v] == 0), []
    while wave:
        result.append(wave)
        nxt = []
        for u in wave:
            for v in out[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    nxt.append(v)
        wave = sorted(nxt)
    return result

#        a  b  c  d  e  f      rules: d->a, d->b, a->c, b->c, c->f, e->f
dur   = [3, 2, 4, 1, 6, 2]
rules = [(3, 0), (3, 1), (0, 2), (1, 2), (2, 5), (4, 5)]
flat = schedule(dur, rules)
print("start/finish:", [(chr(97 + i), flat[2 * i], flat[2 * i + 1]) for i in range(6)])
assert flat == [1, 4, 1, 3, 4, 8, 0, 1, 0, 6, 8, 10]

def heaviest_chain(dur, rules):               # brute force over every path
    out = [[] for _ in dur]
    for u, v in rules:
        out[u].append(v)
    def best_from(u):
        return dur[u] + max((best_from(v) for v in out[u]), default=0)
    return max(best_from(u) for u in range(len(dur)))
assert max(flat[1::2]) == heaviest_chain(dur, rules) == 10
print("project length", max(flat[1::2]), "= heaviest chain d-a-c-f")

print("longest path (edges):", longest_path_edges(6, rules))
print("stages:", [[chr(97 + v) for v in w] for w in stages(6, rules)])
assert longest_path_edges(6, rules) == 3
assert stages(6, rules) == [[3, 4], [0, 1], [2], [5]]
assert len(stages(6, rules)) == longest_path_edges(6, rules) + 1
```

The stages list is the queue's waves, made explicit: [d, e], then [a, b], then
[c], then [f]. Four waves, and the longest path has 3 edges, 4 nodes. That is not
a coincidence: a task's wave number is the number of edges on the longest chain
of prerequisites leading to it, which is the DP above with every duration equal
to 1.

## Why it is correct

:::proof Kahn's algorithm places every task exactly when there is no cycle, and the result respects every rule
**Setup.** A directed graph with n nodes and m arrows. The algorithm keeps an
output list L (empty at the start), a number deg[v] for every node (the in-degree
at the start), and a ready set R (every node with in-degree 0 at the start). Each
step removes some node u from R, appends it to L, and for every arrow u → v
lowers deg[v] by one, adding v to R if deg[v] becomes 0. It stops when R is
empty.

**Invariant.** At the start of every step:

- **(I1)** for every node v not in L, deg[v] is the number of arrows into v whose
  tail is not in L;
- **(I2)** R is exactly the set of nodes not in L with deg[v] = 0;
- **(I3)** for every arrow u → v with v in L, u is in L too, and earlier.

**At the start** L is empty: deg is the full in-degree, which is (I1); R is the
in-degree-0 nodes, which is (I2); (I3) says nothing because L is empty.

**One step keeps the invariant.** Take u out of R and append it to L.

*(I3).* By (I2), deg[u] = 0, and by (I1) that means no arrow into u has its tail
outside L. So every prerequisite of u is already in L, earlier than u. For the
nodes already in L nothing changed.

*(I1).* Only u moved into L. For a node v not in L, the arrows into v with tail
outside L lose exactly the arrows u → v, and the algorithm lowers deg[v] once per
such arrow. Nothing else changes.

*(I2).* No deg ever goes up, so no node becomes ready without the algorithm
seeing it reach 0 in this step, and those are exactly the ones it adds. u has
left R and joined L.

**No node is placed twice.** deg[v] starts at the in-degree and only goes down,
one per arrow into v. A number that only goes down passes through 0 at most
once, so v is added to R at most once, and placed at most once. So the loop runs
at most n times and stops.

**If the loop stops with nodes left over, there is a cycle.** Let S be the
nodes not in L. R is empty, so by (I2) every v in S has deg[v] > 0, and by (I1)
every v in S has an arrow into it from another node of S. Start at any v0 in S
and step backwards along such arrows: v1 → v0, v2 → v1, and so on, staying in S.
S is finite, so some node repeats, and the stretch between its two visits, read
forwards, is a directed cycle.

**If there is a cycle, the loop stops with nodes left over.** Suppose some node
of a cycle C is placed, and let v be the first one placed. Its predecessor u on C
has an arrow u → v, so by (I3) u was placed earlier, which contradicts v being
first. So no node of C is ever placed.

**Conclusion.** The loop places all n nodes exactly when the graph has no cycle,
and then (I3) says every arrow points forward in L: L is a topological order. ∎

**And for DFS post-order.** Take any arrow u → v in a graph with no cycle. When
the DFS scans this arrow from u, u is grey. If v is white, the DFS enters v from
u, and v finishes before u does. If v is black, v has already finished, before
u. v cannot be grey: grey nodes are exactly the current route, so v grey would
mean a route from v to u, and with the arrow u → v a cycle. So in every case v
finishes before u, v comes before u in post-order, and after u in the reversed
post-order. Every arrow points forward. ∎
:::

The assumptions the proof used, in plain words, because each one is a bug when it
fails:

- **(I1)'s accounting.** deg[v] must equal the number of unplaced prerequisites. A
  duplicated rule must add 2 and be paid twice, or be removed from both counts.
  Half-doing it (dedupe the list but not the count) leaves a debt nobody pays,
  and a phantom cycle.
- **Every node is seeded.** The start of the proof says R holds *every* node with
  in-degree 0. Seeding from the rules loses isolated nodes.
- **Nothing about which node comes out of R.** The proof says "some node u". That
  is the licence for the heap, the queue, the stack, or any tie rule a problem
  wants, without re-proving anything.
- **The graph does not change during the run.**
- **Not assumed:** that the graph is connected, has one source, or is acyclic.
  Acyclicity is a conclusion of the run, not a precondition.

The lexicographic claim (a min-heap gives the smallest valid order) needs one
more argument, an exchange, and it is a Check yourself question.

## What it costs

Count it in three piles.

**Building.** Each rule appends to one list and adds to one counter: m steps.
The counters and lists for n nodes: n. So O(n + m).

**Seeding.** One pass over the nodes: n.

**The loop.** Each node is taken out at most once (the proof). When u is taken
out, the loop walks its out-list, out-degree(u) steps. The sum of out-degrees is
exactly m, because every arrow has one tail. So the loop is n + m, and the whole
run is **O(n + m)**.

The DP on top (finish times, longest path, path counts) does O(1) work per arrow
in one more pass: still O(n + m).

**The costs people forget.**

- **The heap.** A min-heap for "smallest ready first" makes each push and pop
  O(log n): O(m + n log n). With string names, a comparison costs up to the
  length of the strings. [[p:applied-intuition-compilation-order-topological-sort|Compilation Order]]
  has up to 2 x 10^5 modules; still fine, but it is not linear.
- **String keys.** A dictionary lookup hashes the string. Map names to integers
  once, solve on arrays, map back at the end, when the graph is large.
- **Rescanning.** "Find a ready task" by scanning the nodes each round is n
  rounds of n: O(n^2) at least. The counter exists to remove exactly this.
- **Edge membership tests.** `if v in out[u]` on a list is a scan; you never need
  it in Kahn's algorithm. If the input can repeat rules, dedupe with a set of
  pairs, once, up front.
- **Recursion depth** in the DFS form: n frames. A chain of 10^5 tasks is a
  `RecursionError`.
- **Large numbers.** [[p:headlands-dependency-job-schedule|Earliest Dependency Schedule]]
  has durations up to 10^9 and paths up to 10^14. Python does not care; in Java
  or C++ use 64-bit integers.

## How to think about it

On every problem that might be this, ask:

1. **Is there a "must happen before" relation?** Prerequisites, dependencies,
   "requires", "after", a recipe needing ingredients, a word order implying a
   letter order. If the relation has no direction, this is not the chapter.
2. **Which way do the arrows go?** Write one rule out loud in the statement's
   words and draw its arrow: "[course, prerequisite]: the prerequisite comes
   first, so prerequisite → course". Then name the unpacked variables by meaning.
3. **What is the node set?** Given separately (seed from it), or only "the names
   mentioned" ([[p:intuit-earliest-workflow-stages|Earliest Concurrent Workflow Stages]]:
   "include exactly the names mentioned")?
4. **What is the question?** Possible at all (length check), one order (any
   container), a specific order (the tie rule picks the container), stages (whole
   waves), a time or a longest chain (DP in the order), a subset (only what a
   target needs).
5. **Is there a tie rule?** Smallest: min-heap. Input order: queue seeded in input
   order, or heap keyed by position. None: anything.
6. **Can there be a cycle, and what should happen then?** Empty list,
   "IMPOSSIBLE", false. The length check is the detector either way.
7. **Do I need to build the graph myself?** Alien Dictionary hides the rules in
   adjacent words; a grid with "strictly increasing" moves hides a DAG in its
   values.

### Telling it from its neighbours

- **Kahn or DFS?** Kahn when you need a tie rule, waves, or no recursion; it is
  the safer interview default. DFS when you start from one target and want only
  what it needs ([[p:amazon-package-dependency-order|Package Dependency Order]]),
  or when the code is already a DFS.
- **Topological sort or BFS?** Both use a queue. BFS on an undirected graph
  measures distance; Kahn's queue on a directed graph releases a node only when
  *all* its arrows in are paid, not when the first one arrives. A node in Kahn's
  wave k is the end of a *longest* chain of length k, where BFS layer k is the
  end of a *shortest* path of length k.
- **DAG DP or Dijkstra?** Shortest paths in a DAG are one pass in topological
  order, even with negative weights. [[dijkstra]] is for graphs with cycles and
  non-negative weights.
- **Cycle detection: here or in [[graphs]]?** Both. Kahn's count says *whether*
  there is a cycle; the DFS colours also give you the arrow that closes it, so you
  can print the cycle by walking the grey route.

## Variations

### A. Course Schedule: is there an order at all?

**What changes:** nothing; you return `len(order) == n` instead of the order.
**Why:** the proof's two directions: everything placed exactly when there is no
cycle. Example: courses 1, 2, pairs [2, 1] and [1, 2]: both owe 1, nothing is
ever ready, 0 of 2 placed, false.
[[p:inmobi-course-schedule|Course Schedule]] is the plain form, with pairs
`[course, prerequisite]` and courses numbered from 1.

### B. A specific order: the tie rule picks the container

**What changes:** the ready set is a min-heap (or a heap keyed by whatever the
statement says). **Why:** any ready task is safe, so the tie rule is free to pick;
the exchange argument in Check yourself shows smallest-first gives the smallest
order. Example: no rules, nodes 2, 0, 1: the heap gives 0, 1, 2.
[[p:chainalysis-lexicographically-smallest-course-order|Course Schedule II]] is
integers with "smallest first";
[[p:applied-intuition-compilation-order-topological-sort|Compilation Order]] is
strings, with `["IMPOSSIBLE"]` on a cycle and pairs `[module, prerequisite]` that
point the opposite way to the arrow.

**Never sort the output instead.** The smallest valid order is not the sorted
list, which is usually not valid. The choice has to happen inside the loop, among
ready tasks only.

### C. Cycle detection by count

**What changes:** you only care whether `len(order) < n`. **Why:** stuck means
cycle. Example: 0 hates 1, 1 hates 2, 2 hates 0: nothing has in-degree 0, so
nothing is placed, so there is a cycle.
[[p:arcesium-detect-cycle-in-directed-hate-graph|Detect a Cycle in Directed Hate Relationships]]
is this in a story. If you also need the cycle itself, the leftover nodes contain
it, and walking back along unpaid arrows from any of them finds it (the trace
above); or use DFS colours and read the grey route.

### D. DFS post-order, and only what a target needs

**What changes:** DFS from the target only, along "needs" arrows, writing each
node when it finishes. **Why:** post-order writes a node after everything it
needs, and starting from the target visits only the target's transitive
dependencies. A grey node met again means a cycle among the needed packages, and
a cycle elsewhere in the input does not matter. Example: app needs lib and log,
both need core: post-order core, lib, log, app (with lib before log because it is
listed first). [[p:amazon-package-dependency-order|Package Dependency Order]]
teaches exactly this, with "process dependencies in the order they appear in the
input pairs" as its tie rule, which is the order of the out-lists.

### E. Stages: Kahn one wave at a time

**What changes:** take the whole ready set as one batch, then collect everything
that batch unlocks as the next batch. **Why:** a task's earliest stage is one
more than the latest stage of its prerequisites, which is the DP "longest chain
ending here", and the waves compute exactly that. Example: d, e | a, b | c | f.
[[p:intuit-earliest-workflow-stages|Earliest Concurrent Workflow Stages]] asks for
the waves, each sorted, over "exactly the names mentioned", with repeated pairs
counted once. "Minimum number of semesters" is the number of waves.

### F. Longest path and scheduling with durations: DP on a DAG

**What changes:** a second pass in topological order computing
`finish[v] = dur[v] + max(finish[u])` over prerequisites, or `best[v] =
max(best[u] + 1)` for the longest chain in edges. **Why:** in topological order
every prerequisite is final before v is reached. Example: the six tasks finish at
10, along d-a-c-f.

- [[p:suno-longest-dag-path|Longest Path in a Directed Acyclic Graph]]: edges
  only, an isolated node is a path of length 0.
- [[p:headlands-dependency-job-schedule|Earliest Dependency Schedule]]: durations,
  unlimited workers, return start and finish per job.
- [[p:meta-minimum-time-target-courses|Minimum Time to Complete Target Courses]]:
  the same, restricted to the targets and their prerequisites. The answer is the
  largest finish among the targets; courses outside the closure cannot raise it,
  so you may compute all finishes and take the maximum over targets, or first
  restrict the graph with a reverse search from the targets.

Other DP shapes in the same pass: **count paths** (`ways[v] += ways[u]`),
**shortest path from a source** (`dist[v] = min(dist[v], dist[u] + w)`, correct
even with negative weights, since nothing behind you can change), **latest start
without delaying the project** (a backward pass in reverse order).

### G. In-degree as "missing ingredients"

**What changes:** the nodes are of two kinds (supplies and recipes), and only
recipes have debts. **Why:** a recipe is ready when every ingredient is
available, which is in-degree 0 in the graph ingredient → recipe. Supplies seed
the queue; each recipe made is a new supply. Example: supplies [yeast, flour],
bread needs yeast and flour, sandwich needs bread and meat: bread's debt goes 2,
1, 0, it is made; sandwich's goes 2, 1 and stops, because meat is never
supplied. [[p:bloomberg-find-all-possible-recipes-from-given-supplies|Find All Possible Recipes from Given Supplies]].
A recipe in a cycle, or needing something that never appears, simply never
reaches 0, and that is the right answer, not an error.

### H. Backwards: peel leaves by out-degree

**What changes:** count *out*-degrees, start from nodes with none (leaves), and
pay the debts of their parents. **Why:** it is Kahn's algorithm on the reversed
graph. Example: edges 0 → 1, 0 → 2: leaves [1, 2], then [0].
[[p:vercel-leaves-to-root-order|Order DAG Nodes from Leaves to Roots]] wants the
leaf layers in ascending order, and an empty answer if a cycle stops the peeling.

### I. Build the graph yourself: Alien Dictionary

**What changes:** the rules are hidden in the input. **Why:** in a sorted list of
words, two adjacent words first differ at some position, and the letter of the
first word there must come before the letter of the second. That is one arrow per
adjacent pair, at most. Example: ["wrt", "wrf", "er", "ett", "rftt"] gives t → f,
w → e, r → t, e → r; Kahn gives w e r t f. Two traps: a word followed by its own
proper prefix ("abc" then "ab") is invalid, return ""; and every letter that
appears must be a node even if it is in no rule.
[[p:intuit-alien-dictionary|Alien Dictionary]] wants the smallest valid order:
heap.

### J. A hidden DAG: increasing paths in a grid

**What changes:** the arrows are "move to a strictly larger neighbour". **Why:**
values strictly increase along every arrow, so no arrow sequence can return to
its start: the graph is a DAG without anyone saying so. The longest increasing
path is the number of Kahn waves (start from cells with no smaller neighbour), or
a memoised DFS. Example: [[1, 2], [4, 3]]: 1 → 2 → 3 → 4, four cells, four waves.
[[p:doordash-longest-increasing-matrix-path|Longest Increasing Path in a Matrix]].

### K. Rarer

- **Is the order unique?** Exactly when the ready set never holds more than one
  task. One check per step.
- **All orders, or how many.** Backtracking over the ready set; exponential.
  Counting with bitmask DP for n up to about 20.
- **Condensation.** Contract each strongly connected component to one node; the
  result is always a DAG, and you sort that ([[strongly-connected]]).

## Recognising it in a statement

Strongest signals first.

1. **"prerequisite", "depends on", "must be completed before", "requires"** plus
   **"return an order" or "is it possible to finish all"**. The definition.
2. **"If it is impossible, return an empty array / false / IMPOSSIBLE"** in a
   dependency story. Impossible means a cycle.
3. **"The graph is acyclic" in the constraints, with directed pairs.** The setter
   is telling you an order exists, so the question is what to compute along it.
4. **"Lexicographically smallest order" with dependencies.** Kahn with a heap.
5. **Durations plus "earliest", "minimum total time", "in parallel", "unlimited
   workers".** DAG DP with max over prerequisites.
6. **"Minimum number of semesters / rounds / stages".** Waves.
7. **"Install / build / compile X and everything it needs".** DFS from X.

**Disguises.** Alien dictionary (letter order from word order). Recipes and
supplies. Spreadsheet cells that refer to other cells (evaluate in dependency
order, a cycle is an error). Build systems. Course plans. A grid path that must
strictly increase (a hidden DAG). Any "evaluate these formulas" with references.

**Constraint lines.** n up to 10^5 and m up to 2 x 10^5: only O(n + m) fits,
which rules out anything that rescans.

**Anti-signals.** Undirected "conflicts" (bipartite). "Can these be grouped"
(union-find). A cycle in a graph where each node has exactly one successor
(that is [[cycle-detection]] with two pointers). A key you can compare ("by
deadline", "by priority") with no relation between items ([[sorting]]). Counting
all orders.

## Traps

**The arrows point the wrong way.** Symptom: a perfectly valid order of the
*reversed* graph, so the output looks plausible and every rule is broken. Course
Schedule's `[course, prerequisite]` and Compilation Order's `[module,
prerequisite]` both put the dependent first. Fix: unpack as `after, before = pair`
when the statement says so, and check one rule against your output by hand.

**Seeding from the rules instead of the nodes.** Symptom: an acyclic input
reported as a cycle, or a missing node in the output. The isolated task is the
test.

**Duplicate rules counted once and paid twice** (or the reverse). Symptom: a
phantom cycle that disappears when the input is deduplicated.

**Two marks in the DFS version.** Symptom: a diamond reported as a cycle.

**Pre-order instead of post-order.** Symptom: correct on chains (where they
agree), wrong as soon as a node has two prerequisites.

**Reversing when you should not, or not reversing when you should.** Symptom:
the exact reverse of a right answer. Decide which way the arrows point.

**Sorting the output for "smallest order".** Symptom: an output that breaks
rules.

**DP in the wrong order.** Computing finish times in input order or node order.
Symptom: correct when the input happens to be listed in dependency order, which
samples often are.

```python run
import heapq

def kahn_smallest(n, before_after):
    out, indeg = [[] for _ in range(n)], [0] * n
    for b, a in before_after:
        out[b].append(a)
        indeg[a] += 1
    ready = [v for v in range(n) if indeg[v] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        u = heapq.heappop(ready)
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(ready, v)
    return order if len(order) == n else []

def ok(order, before_after):
    pos = {v: i for i, v in enumerate(order)}
    return bool(order) and all(pos[b] < pos[a] for b, a in before_after)

# Course Schedule II style input: [course, prerequisite]
n, pairs = 4, [[1, 0], [2, 0], [3, 1], [3, 2]]
wrong = kahn_smallest(n, [(c, p) for c, p in pairs])       # arrow course -> prereq
right = kahn_smallest(n, [(p, c) for c, p in pairs])       # arrow prereq -> course
rules = [(p, c) for c, p in pairs]
print("arrows backwards:", wrong, "valid?", ok(wrong, rules))
print("arrows right    :", right, "valid?", ok(right, rules))
assert wrong == [3, 1, 2, 0] and not ok(wrong, rules)
assert right == [0, 1, 2, 3] and ok(right, rules)

# seeding from the rules loses an isolated course, and looks like a cycle
mentioned = sorted({x for pr in rules for x in pr})
print("courses 0..4 with 4 isolated:", kahn_smallest(5, rules),
      "| nodes taken from rules: n =", len(mentioned))
assert kahn_smallest(5, rules) == [0, 1, 2, 3, 4] and len(mentioned) == 4

# "smallest order" by sorting the output breaks a rule
rules2 = [(2, 0)]                                           # 2 before 0
print("sorted output:", sorted(range(3)), "valid?", ok([0, 1, 2], rules2),
      "| heap:", kahn_smallest(3, rules2))
assert kahn_smallest(3, rules2) == [1, 2, 0] and not ok([0, 1, 2], rules2)

# a duplicate rule deduplicated in the lists but not in the count
dup = [(0, 1), (0, 1)]
out, indeg = {0: [1], 1: []}, {0: 0, 1: 2}                 # half-deduplicated
ready, order = [0], []
while ready:
    u = ready.pop()
    order.append(u)
    for v in out[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            ready.append(v)
print("half-deduplicated duplicate rule:", order, "-> reported as a cycle")
assert order == [0] and kahn_smallest(2, dup) == [0, 1]

# DP in node order instead of topological order
dur, r3 = [5, 1, 2], [(2, 0), (0, 1)]                       # 2 -> 0 -> 1
fin_bad = list(dur)
for u in range(3):                                          # node order: wrong
    for b, a in r3:
        if b == u:
            fin_bad[a] = max(fin_bad[a], fin_bad[b] + dur[a])
fin = list(dur)
for u in kahn_smallest(3, r3):                              # topological order
    for b, a in r3:
        if b == u:
            fin[a] = max(fin[a], fin[b] + dur[a])
print("finish in node order:", fin_bad, "| in topological order:", fin)
assert fin == [7, 8, 2] and fin_bad != fin
```

## What to memorise

**The template:**

```
out = {v: [] for v in nodes}; indeg = {v: 0 for v in nodes}
for before, after in rules:            # name the pair by meaning
    out[before].append(after); indeg[after] += 1
ready = [v for v in nodes if indeg[v] == 0]    # queue, stack or heap
order = []
while ready:
    u = take(ready); order.append(u)
    for v in out[u]:
        indeg[v] -= 1
        if indeg[v] == 0: put(ready, v)
return order if len(order) == len(nodes) else CYCLE
```

**The sentence:** a task that owes nothing can always go next and can never be a
wrong choice; when nothing owes nothing, the leftovers hold a cycle.

**The question:** what can go first right now, and what does placing it unlock?

**The habit:** after building the graph, read one rule aloud in the statement's
words and check the arrow, before writing anything else.

Numbers: O(n + m) with a queue, O(m + n log n) with a heap; in-degrees sum to m;
the number of Kahn waves is the longest chain in nodes; DFS needs n frames.

## Check yourself

:::check
Hand trace. Tasks 0 to 5, rules (before, after): 5→2, 5→0, 4→0, 4→1, 2→3, 3→1.
Run Kahn's algorithm with a min-heap. Write the debts at the start, then the
ready set and the order after every step.
--
Out-lists: 5 [2, 0], 4 [0, 1], 2 [3], 3 [1]. Debts: 0:2, 1:2, 2:1, 3:1, 4:0, 5:0.

Ready {4, 5}. Take 4: 0 2→1, 1 2→1. Ready {5}. Order 4.
Take 5: 2 1→0 (ready), 0 1→0 (ready). Ready {0, 2}. Order 4 5.
Take 0: no arrows out. Ready {2}. Order 4 5 0.
Take 2: 3 1→0. Ready {3}. Order 4 5 0 2.
Take 3: 1 1→0. Ready {1}. Order 4 5 0 2 3.
Take 1. Order 4 5 0 2 3 1.

Six of six placed: no cycle. Check: 5 before 2 and 0, 4 before 0 and 1, 2 before
3, 3 before 1. All hold.
:::

:::check
Hand trace, DFS. Same rules as the previous question, out-lists in the order
given, DFS started from nodes 0, 1, 2, ... in that order. Write the post-order,
reverse it, and confirm it is valid. Then write the pre-order and find a rule it
breaks.
--
Start 0: no arrows out, finish 0. post [0].
Start 1: finish 1. post [0, 1].
Start 2: enter 3, 3 → 1 is finished, finish 3, finish 2. post [0, 1, 3, 2].
3 is done. Start 4: 0 and 1 finished, finish 4. post [0, 1, 3, 2, 4].
Start 5: 2 and 0 finished, finish 5. post [0, 1, 3, 2, 4, 5].

Reversed: 5 4 2 3 1 0. 5 before 2 and 0, 4 before 0 and 1, 2 before 3, 3 before
1: valid.

Pre-order: 0, 1, 2, 3, 4, 5. It breaks 5→0 (0 is first), and also 4→0, 4→1,
5→2, 3→1. Pre-order here is just the order the outer loop started nodes, and
the outer loop does not know about rules.
:::

:::check
Hand trace, DP on the DAG. Durations: 0:2, 1:3, 2:1, 3:4, 4:2, 5:1, rules as in
the first question, unlimited workers. Using the order 4 5 0 2 3 1, compute the
earliest finish of every task and the project length. Which chain is critical?
--
Start with finish = duration: 0:2, 1:3, 2:1, 3:4, 4:2, 5:1.
Take 4 (finish 2): 0 = max(2, 2 + 2) = 4; 1 = max(3, 2 + 3) = 5.
Take 5 (finish 1): 2 = max(1, 1 + 1) = 2; 0 = max(4, 1 + 2) = 4.
Take 0 (finish 4): no arrows.
Take 2 (finish 2): 3 = max(4, 2 + 4) = 6.
Take 3 (finish 6): 1 = max(5, 6 + 3) = 9.
Take 1 (finish 9).

Finishes 0:4, 1:9, 2:2, 3:6, 4:2, 5:1. Project length 9, along 5 → 2 → 3 → 1
(1 + 1 + 4 + 3 = 9). The chain 4 → 1 (2 + 3 = 5) has 4 units of slack.
:::

:::check
Prove that taking the smallest ready task at every step gives the
lexicographically smallest topological order.
--
Let G be the greedy's order and X any valid order, and let i be the first
position where they differ. Up to i - 1 they agree, so at step i the greedy's
ready set is exactly the set of tasks whose prerequisites all lie in that common
prefix. X[i] is in it (X is valid), and G[i] is the smallest member, so
G[i] < X[i].

Build X' from X by moving G[i] from its later position to position i. X' is
valid: positions before i did not change; G[i]'s prerequisites are all in the
prefix, so it is legal at i; and the tasks between i and G[i]'s old position each
moved one place later, which can only move them further from their
prerequisites. X' is smaller than X (same prefix, smaller element at i). So any
order that differs from G can be made strictly smaller, and no valid order is
smaller than G.
:::

:::check
Someone says: "To check for a cycle, I run DFS with a visited set, and if I ever
reach a visited node, there is a cycle. It passed the tests." Where are they
wrong, and what is the smallest input that shows it?
--
Reaching a visited node only means two routes lead to it. It is a cycle only if
that node is still on the current route (grey), not if it finished earlier on
another branch (black).

The diamond a→b, a→c, b→d, c→d: DFS from a finishes d through b, then reaches d
again through c. Visited, so they report a cycle; there is none, and Kahn places
all four. Their tests probably only had chains, cycles, and trees, where the
mistake cannot show. Three colours, or Kahn's count, fix it.
:::

:::check
Someone runs Kahn on 8 tasks and gets 5 in the output. A colleague says: "the 3
left over may just be waiting on something outside the graph; it is not
necessarily a cycle." Are they right?
--
Not if the graph is the whole input. When the ready set empties, every leftover
task has a positive debt, and the debt counts only unplaced prerequisites, which
are leftovers too. Walking back along unpaid arrows inside a finite set must
revisit a task, and that is a cycle. There is nowhere else for the blockage to
come from.

The colleague could be right one level up: if a rule mentions a task that was
never added to the node list, the graph you built is not the one you meant. Then
the "cycle" is a modelling bug. Build the node set deliberately: every name seen
anywhere, or reject unknown names up front.
:::

:::check
Reduce this disguised problem. "A spreadsheet has cells A1..A5. Each cell is a
number or a sum of other cells: A1 = 3, A2 = A1 + A4, A3 = A2 + A1, A4 = 5,
A5 = A3 + A5. Evaluate every cell, or report the ones that cannot be evaluated."
--
Nodes: the cells. Arrows: from each referenced cell to the cell that uses it:
A1 → A2, A4 → A2, A2 → A3, A1 → A3, A3 → A5, A5 → A5. Evaluate in topological
order, with the formula as the DP step.

Debts: A1 0, A2 2, A3 2, A4 0, A5 2. Ready {A1, A4}. A1 = 3: A2 → 1, A3 → 1.
A4 = 5: A2 → 0. A2 = 8: A3 → 0. A3 = 11: A5 → 1. Stuck: A5 still owes 1, to itself.
A5 refers to itself, a cycle of length one, and cannot be evaluated; everything
else can. Cells left over after Kahn are exactly the cells in or downstream of a
cycle.
:::
