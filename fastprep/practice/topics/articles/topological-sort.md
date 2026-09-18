# Topological Sort

> A topological sort is not a sorting algorithm. It is the act of flattening a
> partial order into a total one, and the only way it can fail is that what you
> were given was never an order at all.

## When you reach for it

You reach for it when the input describes a **"must happen before"** relation
and the output has to be a single sequence that honours all of it. Compile these
modules; install these packages; take these courses; deploy these services; run
these agent tasks. The relation is directed — `a` before `b` is not the same
claim as `b` before `a` — and the question is: lay everything on a line so that
no arrow ever points backwards.

Fifty-seven problems in this bank are this topic, which makes it one of the
densest single ideas in the graph section. *Course Schedule* and *Course
Schedule II* are the canonical pair, and the industrial rewrites are everywhere:
*Compilation Order with Topological Sort*, *Microservice Deployment Order*,
*Package Dependency Order*, *Dependency-Aware Agent Task Scheduler*. Once you
can see past the story, they are the same six lines.

There are two further shapes that are secretly the same tool.

**"Is it even possible?"** *Course Schedule*, *Detect a Cycle in a Directed
Graph*, *Evaluate Formulas with Cycle Detection* do not want the order at all —
they want to know whether one exists. A topological sort that runs to completion
is a proof of acyclicity; one that stalls is a proof of a cycle. You get the
decision for free from the same run, which is why [[cycle-detection-graph]] and
this chapter are two views of one algorithm.

**"When can each thing finish?"** *Minimum Completion Time for DAG
Dependencies*, *Minimum Time to Complete Target Courses*, *Earliest Dataset
Readiness in a Pipeline*, *Task Processor: Dependencies and Deadlines*. Here the
order is not the answer, it is the *evaluation schedule* for a dynamic program.
That is the second half of this chapter.

And the shapes that make it the wrong tool. If the edges are undirected, there is
no "before" to respect — you want [[flood-fill]], [[bipartite]] or
[[union-find]]. If the graph has cycles and you still need an answer, the cycles
are the object of study, not an error: contract them first with
[[strongly-connected]]. If the question asks for *all* valid orders rather than
one, no linear algorithm exists — the count can be exponential, and you are in
backtracking territory. And if the only constraint is a key you can compare, then
you want [[sorting]]; the word "order" in a statement is not a signal on its own.

## The idea

**Repeatedly remove everything that owes nothing.**

That is the whole algorithm. Give every vertex a counter: how many of its
prerequisites are still outstanding. A vertex whose counter is zero is *ready* —
nothing is stopping it. Emit any ready vertex, cross it off every dependent's
list, and whoever drops to zero becomes ready in turn. Stop when nothing is
ready. If you emitted everything, you have an order. If you did not, whatever is
left is stuck behind itself: a cycle.

The counter is the in-degree, and the algorithm is Kahn's. But think of it as
debt, not as degree. `indeg[v]` is not a property of the picture, it is the
number of promises still owed to `v`, and it only ever goes down.

The picture worth holding is two pictures. On the left, the dependency graph,
drawn however it fell out. On the right, the same vertices on a line, in the
order you emitted them. A topological order is exactly a placement on that line
under which every edge points rightwards.

<svg viewBox="0 0 560 310" role="img" aria-label="a six node directed acyclic graph, and the same six nodes laid out on a line so that every edge points to the right">
  <text x="18" y="20">a depends on d; c depends on a and b; f depends on c and e</text>
  <line x1="79" y1="58" x2="139" y2="46"/>
  <polygon class="fill" points="149,44 140,51 138,41"/>
  <line x1="78" y1="68" x2="140" y2="91"/>
  <polygon class="fill" points="150,95 138,96 142,86"/>
  <line x1="188" y1="45" x2="254" y2="63"/>
  <polygon class="fill" points="265,66 253,68 256,59"/>
  <line x1="188" y1="97" x2="254" y2="80"/>
  <polygon class="fill" points="265,77 255,85 253,75"/>
  <line x1="303" y1="79" x2="370" y2="103"/>
  <polygon class="fill" points="380,107 368,108 372,98"/>
  <line x1="79" y1="153" x2="368" y2="118"/>
  <polygon class="fill" points="379,117 369,123 368,113"/>
  <circle cx="60" cy="62" r="19"/>
  <text x="60" y="67" text-anchor="middle">d</text>
  <circle cx="170" cy="40" r="19"/>
  <text x="170" y="45" text-anchor="middle">a</text>
  <circle cx="170" cy="102" r="19"/>
  <text x="170" y="107" text-anchor="middle">b</text>
  <circle cx="285" cy="72" r="19"/>
  <text x="285" y="77" text-anchor="middle">c</text>
  <circle cx="60" cy="155" r="19"/>
  <text x="60" y="160" text-anchor="middle">e</text>
  <circle cx="400" cy="114" r="19"/>
  <text x="400" y="119" text-anchor="middle">f</text>
  <text x="18" y="205">the same six, laid on a line: now every arrow points right</text>
  <path d="M 59 261 Q 94 220 119 250"/>
  <polygon class="fill" points="126,259 116,254 123,247"/>
  <path d="M 59 261 Q 129 220 186 254"/>
  <polygon class="fill" points="196,260 184,259 189,250"/>
  <path d="M 129 261 Q 199 220 256 254"/>
  <polygon class="fill" points="266,260 254,259 259,250"/>
  <path d="M 199 261 Q 234 220 259 250"/>
  <polygon class="fill" points="266,259 256,254 263,247"/>
  <path d="M 269 261 Q 339 220 396 254"/>
  <polygon class="fill" points="406,260 394,259 399,250"/>
  <path d="M 339 261 Q 374 220 399 250"/>
  <polygon class="fill" points="406,259 396,254 403,247"/>
  <rect x="30" y="262" width="58" height="34" rx="4"/>
  <text x="59" y="284" text-anchor="middle">d</text>
  <rect x="100" y="262" width="58" height="34" rx="4"/>
  <text x="129" y="284" text-anchor="middle">a</text>
  <rect x="170" y="262" width="58" height="34" rx="4"/>
  <text x="199" y="284" text-anchor="middle">b</text>
  <rect x="240" y="262" width="58" height="34" rx="4"/>
  <text x="269" y="284" text-anchor="middle">c</text>
  <rect x="310" y="262" width="58" height="34" rx="4"/>
  <text x="339" y="284" text-anchor="middle">e</text>
  <rect x="380" y="262" width="58" height="34" rx="4"/>
  <text x="409" y="284" text-anchor="middle">f</text>
</svg>

Notice that the flattening is not unique. `e` could have gone first, or last but
one, or anywhere before `f`. The graph pins down a *partial* order: it says `d`
is before `a`, and says nothing about `d` versus `e`. Every topological sort is a
choice of one total order that is consistent with the partial one, and that
freedom is where the tie-break rules in real statements live.

## Worked by hand

Six tasks, `a` through `f`. The dependency pairs, written `(prerequisite,
dependent)`, are

```
(d, a)   (d, b)   (a, c)   (b, c)   (c, f)   (e, f)
```

so the initial debts are `a:1  b:1  c:2  d:0  e:0  f:2`. We will use the
tie-break that half the problems in this bank ask for: **when several tasks are
ready, take the smallest**. That means the ready set is a min-heap.

Start: ready `{d, e}`, output empty.

| step | pop | debts paid down | ready after | output so far |
| --- | --- | --- | --- | --- |
| 1 | `d` | `a` 1→0, `b` 1→0 | `{a, b, e}` | `d` |
| 2 | `a` | `c` 2→1 | `{b, e}` | `d a` |
| 3 | `b` | `c` 1→0 | `{c, e}` | `d a b` |
| 4 | `c` | `f` 2→1 | `{e}` | `d a b c` |
| 5 | `e` | `f` 1→0 | `{f}` | `d a b c e` |
| 6 | `f` | — | `{}` | `d a b c e f` |

Six emitted, six vertices, so the graph is acyclic and `d a b c e f` is a valid
order. Check a few edges against it by eye: `d` before `a` and `b`, yes; `a` and
`b` before `c`, yes; `c` and `e` before `f`, yes.

Three things the trace shows that the code does not.

**Each debt is paid exactly once.** Look down the middle column: every one of the
six edges appears once and only once, on the step where its tail was popped.
That is not a coincidence, it is the reason the whole run is linear, and it is
the reason a vertex is pushed at most once — its counter crosses zero at most
once because it never goes up.

**The ready set held several vertices for most of the run.** At step 2 it held
three. Any of them could have been emitted. We took `a` because of the
tie-break, not because the graph demanded it; `e` was ready from the very first
moment and did not come out until step 5. Being ready is not being urgent, and
being emitted early is not being important.

**The output is not sorted.** It begins `d a b`. If you had sorted the result
alphabetically you would get `a b c d e f`, which puts `a` before `d` and breaks
the very first dependency. This is why the name "topological sort" misleads
people: nothing is being compared to anything.

:::note The tie-break is where the problem's personality lives
*Lexicographically Smallest Dependency Order* and *Compilation Order with
Topological Sort* want a min-heap, as above. *Task Dependency Ordering* wants a
plain FIFO queue seeded in input order. *Topological Sort with Secondary
Ordering* wants a heap keyed by first appearance in the input rather than by the
name itself. All three are the identical algorithm with a different container
for the ready set — and, as the proof below shows, correctness does not care
which one you use.
:::

## Why it is correct

The loose argument — "we only emit things whose prerequisites are done, so it
works" — is nearly the real one, but it hides the two claims that actually need
proving: that a vertex is never emitted twice, and that stalling means a cycle
rather than bad luck.

:::proof Kahn's algorithm produces a topological order, and stalls only on a cycle
**Setup.** `G = (V, E)` is a directed graph, `n = |V|`, `m = |E|`. The algorithm
maintains an output list `L` (initially empty), an integer `deg[v]` for each
vertex (initially the in-degree of `v`), and a ready set `R` (initially all `v`
with in-degree 0). Each iteration removes some `v` from `R`, appends it to `L`,
and for every edge `(v, w)` decrements `deg[w]`, pushing `w` into `R` if
`deg[w]` becomes 0. It halts when `R` is empty.

**Invariant.** At the top of every iteration:

- **I1.** For every `v` not in `L`, `deg[v]` equals the number of edges `(u, v)`
  whose tail `u` is not in `L`.
- **I2.** `R` is exactly the set of vertices not in `L` with `deg[v] = 0`.
- **I3.** For every edge `(u, v)` with `v` in `L`, the tail `u` is also in `L`
  and appears strictly earlier.

**Base case.** `L` is empty, so I1 says `deg[v]` is the full in-degree, which is
how it was initialised; I2 says `R` is the set of in-degree-0 vertices, which is
how it was seeded; I3 is vacuous because no vertex is in `L`.

**Inductive step.** Suppose the invariant holds and we pop `v` from `R` and
append it to `L`.

*I3 is restored.* By I2, `deg[v] = 0`, and by I1 that means the number of edges
`(u, v)` with `u` outside `L` is zero — so every in-neighbour of `v` was already
in `L`, hence strictly earlier. For every other vertex already in `L` the claim
is unchanged, since `L` only grew at the end.

*I1 is restored.* The only vertex that changed sides is `v`. For a vertex `w`
not in `L`, the count of in-edges from outside `L` drops by exactly the number of
edges `(v, w)`, and the algorithm decrements `deg[w]` exactly once per such edge.
Every other vertex's count is untouched.

*I2 is restored.* No `deg` value increases, so no vertex silently becomes ready
without the loop noticing; the loop pushes precisely those `w` whose `deg`
reached 0 during this step, and `v` itself left both `R` and the "not in `L`"
side.

**A vertex is appended at most once.** `deg[w]` starts at the in-degree and is
decremented once per in-edge, never incremented. A strictly decreasing integer
sequence passes through 0 at most once, so `w` is pushed at most once, popped at
most once, appended at most once.

**Termination.** Each iteration appends one vertex to `L`, and by the previous
paragraph no vertex is appended twice, so there are at most `n` iterations. The
loop ends.

**Stalling implies a cycle.** Suppose the loop ends with `S = V \ L` non-empty.
`R` is empty, so by I2 every `v` in `S` has `deg[v] > 0`, and by I1 that means
every `v` in `S` has an in-neighbour that is also in `S`. Start at any `v₀` in
`S` and walk backwards: `v₁` an in-neighbour of `v₀` inside `S`, `v₂` an
in-neighbour of `v₁`, and so on forever. `S` is finite, so some vertex repeats,
say `vᵢ = vⱼ` with `i < j`; the walk between them, reversed, is a directed cycle.

**A cycle implies stalling.** Conversely, suppose `C` is a directed cycle and
some vertex of `C` reaches `L`. Take the first such vertex `v` in `L`'s order.
Its predecessor `u` on `C` is an in-neighbour, so by I3 `u` is in `L` and
earlier — contradicting that `v` was first. So no vertex of a cycle is ever
emitted, and `|L| < n`.

**Conclusion.** If `|L| = n`, then `L` is a permutation of `V` and I3 says every
edge runs forward in `L`: a topological order. And `|L| = n` holds if and only if
`G` is acyclic. ∎
:::

Now read the proof for what it *used*, because that list is where the bugs are.

It used **I1's accounting**: `deg[v]` must equal the number of in-edges from
un-emitted vertices. A duplicate edge `(u, v)` listed twice must contribute 2 to
`deg[v]` and be decremented twice — or be de-duplicated in both places. Count it
once and decrement twice and `deg[v]` goes to `-1`, an `== 0` test never fires,
and the algorithm reports a phantom cycle.

It used **every vertex being present**. If you seed `R` by scanning the edge list
instead of the vertex list, an isolated vertex has no in-edges and no out-edges,
never enters `R`, and `|L| < n` — another phantom cycle. *Course Schedule*
numbers courses `0..numCourses-1` precisely so you can seed by range.

It used **nothing at all about how `R` chooses**. The word "some `v` from `R`"
appears once, and no later step depends on which. That is the licence to make `R`
a stack, a FIFO queue, or a min-heap without re-proving anything.

It used **a static graph**. Adding an edge mid-run breaks I1 immediately.

And note what is *not* assumed: connectivity, a single source, distinct labels,
or that the graph is acyclic. Acyclicity is a conclusion here, not a hypothesis.

## What it costs

Count the work in three piles.

**Building.** Reading `m` pairs and appending to adjacency lists is `m`
constant-time appends; allocating `deg` and the adjacency map is `n` slots.
`Θ(n + m)`.

**Seeding.** One pass over `V`. `Θ(n)`.

**The main loop.** Per-iteration cost is *not* constant — popping `v` costs
`O(1)` but relaxing costs `O(outdeg(v))`. So aggregate instead of bounding each
step. By the proof, each vertex is popped at most once, so the loop runs at most
`n` times and the total relaxation work is

```
Σ over emitted v of outdeg(v)  ≤  Σ over all v of outdeg(v)  =  m
```

because the out-degrees of all vertices partition the edge set. Every edge is
touched exactly once, on the step its tail is popped — which is what the middle
column of the hand trace showed. Total `Θ(n + m)`, and that is a tight bound, not
just an upper one: you must at minimum read the input.

**Space.** Adjacency `Θ(n + m)`, `deg` and the output `Θ(n)`, and `R` holds at
most `n` vertices. `Θ(n + m)` overall.

The costs people forget:

- **The container.** With a plain queue or stack, pushes and pops are `O(1)` and
  the total stays `Θ(n + m)`. With a min-heap for a lexicographic tie-break there
  are at most `n` pushes and `n` pops at `O(log n)` each, giving `Θ(m + n log n)`.
  With string keys the comparisons are not `O(1)` either — comparing two
  length-`k` module names is `O(k)`.
- **The hashing.** *Compilation Order* gives you up to `2·10⁵` string module
  names. Every edge costs two dictionary lookups, each hashing a string. That
  constant dwarfs the arithmetic; interning names to integers once, up front, is
  the standard fix.
- **Membership tests written as list scans.** `if w in adj[v]` inside the loop
  turns `Θ(n + m)` into `Θ(n·m)`. Never test edge membership; the algorithm does
  not need to.
- **Recursion depth**, for the DFS formulation: `Θ(n)` stack frames, and CPython
  defaults to about a thousand. A chain of `10⁵` courses is a `RecursionError`,
  not a wrong answer, which at least fails loudly.

The DAG dynamic program in the next section adds nothing asymptotically: it does
`O(1)` work per edge on top of the sort, so it is `Θ(n + m)` as well.

## The implementation

Kahn's algorithm with the lexicographic tie-break, plus a validity checker, plus
a brute-force cross-check so the claim "this is the *smallest* valid order" is
tested rather than asserted.

```python run
import heapq
from itertools import permutations


def topo_order(nodes, edges):
    """Lexicographically smallest topological order, or None if there is a cycle.
    edges are (prerequisite, dependent) pairs."""
    adj = {v: [] for v in nodes}
    indeg = {v: 0 for v in nodes}
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    ready = [v for v in nodes if indeg[v] == 0]   # seed from NODES, not from edges
    heapq.heapify(ready)
    order = []
    while ready:
        v = heapq.heappop(ready)
        order.append(v)
        for w in adj[v]:
            indeg[w] -= 1                          # pay one debt
            if indeg[w] == 0:                      # == 0 fires exactly once per vertex
                heapq.heappush(ready, w)
    return order if len(order) == len(nodes) else None


def respects(nodes, edges, order):
    if order is None or sorted(order) != sorted(nodes):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[u] < pos[v] for u, v in edges)


nodes = list("abcdef")
edges = [("d", "a"), ("d", "b"), ("a", "c"), ("b", "c"), ("c", "f"), ("e", "f")]
got = topo_order(nodes, edges)
print("order      ", got)
assert got == ["d", "a", "b", "c", "e", "f"] and respects(nodes, edges, got)

best = min(p for p in permutations(sorted(nodes)) if respects(nodes, edges, p))
print("brute force", list(best), "(smallest of all 720 permutations that work)")
assert list(best) == got

print("isolated z ", topo_order(nodes + ["z"], edges))
print("3-cycle    ", topo_order(list("xyz"), [("x", "y"), ("y", "z"), ("z", "x")]))
print("self loop  ", topo_order(["p"], [("p", "p")]))
print("empty graph", topo_order([], []))
assert topo_order(list("xyz"), [("x", "y"), ("y", "z"), ("z", "x")]) is None
assert topo_order(["p"], [("p", "p")]) is None and topo_order([], []) == []
print("all checks pass")
```

Three lines are doing the real work.

`indeg[w] -= 1` then `if indeg[w] == 0` is the entire algorithm. Write `== 0`,
never `<= 0`: if your counting is right they are the same, and if your counting
is wrong `<= 0` pushes the same vertex twice and produces a longer-than-`n`
output that the final length check then misreads. `== 0` turns a counting bug
into a visible cycle report instead of silent duplication.

`ready = [v for v in nodes if indeg[v] == 0]` iterates the *vertex* list. Every
vertex that appears in no pair — an isolated module, an optional course — must
still be seeded, or it never appears and the run looks like a cycle.

`len(order) == len(nodes)` is the cycle test, and it is the only one you need.
Not "did the heap empty" (it always does), not "is some in-degree still
positive" (equivalent but an extra pass). The count is the certificate: by the
proof, short output and cycle are the same event.

The self-loop case is worth staring at. `("p", "p")` gives `p` in-degree 1, so it
is never ready, so the output is empty, so the function returns `None`. A
one-vertex cycle needs no special handling, which is a good sign the abstraction
is right.

## Variants you will meet

**DFS with reverse post-order.** Run [[dfs]]; when a vertex *finishes* — after
all its descendants are done — push it onto a list; reverse the list at the end.
This is correct because a vertex finishes only after everything reachable from it
has finished, so it lands ahead of all of them once reversed. It needs three
colours, not two, to detect cycles (see Traps), and it recurses to depth `n`.

**DP on a DAG.** The order is not the answer; it is the sequence in which to
evaluate a recurrence. Because every edge points forward in a topological order,
a state that depends only on its in-neighbours is *final* the moment you reach
it — no memo table, no recursion, one pass. This is the cheapest kind of
[[dynamic-programming]] there is, and it is why the longest path, which is
NP-hard in general digraphs, is linear on a DAG.

```python run
from collections import deque

nodes = list("abcdef")
edges = [("d", "a"), ("d", "b"), ("a", "c"), ("b", "c"), ("c", "f"), ("e", "f")]
dur = {"a": 3, "b": 2, "c": 4, "d": 1, "e": 6, "f": 2}

adj = {v: [] for v in nodes}
indeg = {v: 0 for v in nodes}
for u, v in edges:
    adj[u].append(v)
    indeg[v] += 1

q = deque(v for v in nodes if indeg[v] == 0)
left, order = dict(indeg), []
while q:
    v = q.popleft()
    order.append(v)
    for w in adj[v]:
        left[w] -= 1
        if left[w] == 0:
            q.append(w)
assert len(order) == len(nodes), "not a DAG"

finish = dict(dur)                                       # earliest finish of each task
ways = {v: (1 if indeg[v] == 0 else 0) for v in nodes}   # paths from a source to v
for v in order:                       # v is final the first time we read it
    for w in adj[v]:
        finish[w] = max(finish[w], finish[v] + dur[w])
        ways[w] += ways[v]

print("topological order ", order)
print("earliest finish   ", [(v, finish[v]) for v in sorted(finish)])
print("project done at   ", max(finish.values()), "with unlimited parallelism")
print("paths from a source to f:", ways["f"])


def paths_from(u):
    out = [ [u] ]
    for w in adj[u]:
        for p in paths_from(w):
            out.append([u] + p)
    return out

every = [p for u in nodes if indeg[u] == 0 for p in paths_from(u)]
heaviest = max(every, key=lambda p: sum(dur[x] for x in p))
print("brute force: heaviest chain", "->".join(heaviest), "=", sum(dur[x] for x in heaviest))
assert max(finish.values()) == sum(dur[x] for x in heaviest) == 10
assert ways["f"] == sum(1 for p in every if p[-1] == "f") == 3
print("DP agrees with brute force on both")
```

That is *Minimum Completion Time for DAG Dependencies* in nine lines, and the
same skeleton answers *Minimum Time to Complete Target Courses* and *Earliest
Dataset Readiness in a Pipeline*. Swap `max` for `min` and you get earliest
start; swap it for `+` and you get path counting, as `ways` shows; drop the
weights and you get longest chain, which is what *Longest Chain Booking* wants
once the "fits after" relation is drawn as edges.

**Shortest paths on a DAG.** Relax edges in topological order and you get
single-source shortest paths in `Θ(n + m)`, **even with negative weights** —
faster than [[dijkstra]] and without [[bellman-ford]]'s `O(nm)`. The reason is
the same one: no vertex can be improved after you leave it, because nothing
behind it is left. See [[shortest-path]].

**Level (layered) sort.** Instead of popping one vertex, pop the whole current
ready set as a batch, then the next batch. Batch `k` is everything that can run
in round `k` with unlimited parallelism, and the number of batches is the length
of the longest chain. This is the right shape for "minimum number of semesters".

**Restricted to what matters.** *Package Dependency Order* asks only for a target
package and its transitive dependencies. Do a reverse reachability search from
the target first, then topologically sort the induced subgraph. Sorting the whole
graph and filtering also works but reads the parts you did not need.

**Filtering before sorting.** *Course Schedule with Broken Courses* marks some
vertices dead and propagates death forward before ordering the survivors — a
reachability pass, then a sort. The same two-phase shape appears in *Effective
Role Privileges* and *ACL Inheritance with Local-Only Deny Rules*, where the
inheritance graph must be evaluated in dependency order.

**Condensation.** A general digraph has no topological order, but its
[[strongly-connected]] components do: contract each SCC to a vertex and the
result is always a DAG. Every "order these things, but some of them are mutually
dependent" problem is this.

**Uniqueness.** The order is unique exactly when `|R| = 1` at every step —
equivalently, when consecutive vertices in the output are joined by an edge,
equivalently when the DAG has a Hamiltonian path. Checking is one extra line
inside the loop.

## Recognising it in a statement

By reliability, strongest first:

- **"must be completed before"**, **"depends on"**, **"prerequisite"**,
  **"install / compile / deploy order"**, paired with **"return one valid
  order"**. That is the literal definition.
- **"return an empty array if it is impossible"** attached to a dependency
  story. Impossible means cyclic, and the length check is the detector.
- **Directed pairs plus the word "acyclic"** in the constraints — the setter is
  telling you which algorithm they want.
- **"lexicographically smallest order"** *plus* dependencies. Not a sort: Kahn
  with a heap. Sorting the output of a topological sort destroys it.
- **Durations or times on tasks, and "earliest / minimum total time"** — DAG DP,
  with `max` over in-neighbours.
- **"minimum number of rounds/semesters/waves"** — the layered variant.
- Constraint lines in the shape `1 <= n <= 2·10^5`, `0 <= edges <= 3·10^5`. The
  only thing that fits is linear in `n + m`.

Anti-signals — things that look like this and are not:

- Undirected "conflicts" or "cannot be in the same group": that is 2-colouring,
  [[bipartite]].
- Cycles in an undirected graph: [[union-find]] or [[dfs]], and the meaning of
  "cycle" is different.
- A cycle in a functional graph, where every node has exactly one successor:
  [[cycle-detection]], Floyd's tortoise and hare, `O(1)` space.
- "Order these by a key" with no relation between items: just [[sorting]].
- "Count the valid orders" — that is counting linear extensions, `#P`-complete,
  and no interview wants it beyond `n ≈ 20` with [[dp-bitmask]].
- A relation that is not transitive, such as "a is two units taller than b".
  The DAG structure may still be there, but the answer is constraint
  propagation over it, not the order itself.

## Traps

**The edges point the wrong way.** The single most common bug, and the
*Topological Sort with Secondary Ordering* statement calls it out by name: given
a row `["Hair", "Head"]` meaning Hair depends on Head, the edge must be
`Head → Hair`. Build it backwards and you produce a perfectly valid topological
order of the reversed graph, which is the exact opposite of what was asked.
Symptom: the output looks plausible and is wrong on every non-symmetric test.
The cure is a naming discipline — call the pair `(before, after)` or
`(prereq, dependent)` in the code, never `(a, b)` — and then hand-check one edge
against the output before submitting.

**Seeding from the edges instead of the vertices.** Isolated vertices vanish, the
length check fails, and you report a cycle in an acyclic graph.

**Duplicate edges.** If the input may repeat a pair, either count it twice in
both `indeg` and the adjacency list, or de-duplicate in both. Half-doing it drives
a counter negative and the `== 0` test never fires. Symptom: a phantom cycle that
disappears when you de-duplicate the input.

**Two-state DFS.** A single `visited` set cannot distinguish "this vertex is an
ancestor on my current stack" from "this vertex finished long ago on a different
branch". You need three states. The next block shows a diamond — no cycle
anywhere — reported as cyclic.

**Recursion depth.** The DFS formulation needs `n` frames. Convert to an explicit
stack, or use Kahn, when `n` can reach `10⁵`.

**Sorting the output.** "Lexicographically smallest topological order" is not
"topological order, then sorted". The tie-break has to happen *inside* the loop,
over the ready set only.

**Wrong direction in the DP.** Relaxing `finish[v]` from `v`'s *out*-neighbours
while walking the topological order forwards reads values that are not final
yet. Forward order pushes to out-neighbours; pulling from in-neighbours needs the
reverse adjacency.

```python run
def build(nodes, edges):
    adj = {v: [] for v in nodes}
    for u, v in edges:
        adj[u].append(v)
    return adj


def cycle_seen_only(nodes, adj):
    """WRONG: one 'seen' set cannot tell 'still on the stack' from 'finished'."""
    seen = set()

    def go(u):
        if u in seen:
            return True                     # "been here before, so it must be a cycle"
        seen.add(u)
        return any(go(w) for w in adj[u])

    return any(go(u) for u in nodes if u not in seen)


def dfs_topo(nodes, adj):
    """RIGHT: white = untouched, grey = on the stack, black = finished."""
    colour = {v: 0 for v in nodes}
    post = []

    def go(u):
        colour[u] = 1
        for w in adj[u]:
            if colour[w] == 1:              # grey: an edge back into the live stack
                return True
            if colour[w] == 0 and go(w):
                return True
        colour[u] = 2
        post.append(u)                      # finished: everything after u is placed
        return False

    for u in nodes:
        if colour[u] == 0 and go(u):
            return None
    post.reverse()
    return post


diamond = (["a", "b", "c", "d"], [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")])
adj = build(*diamond)
print("diamond, seen-only DFS says cycle?", cycle_seen_only(diamond[0], adj), "<- wrong")
print("diamond, three-colour DFS order  ", dfs_topo(diamond[0], adj))
assert cycle_seen_only(diamond[0], adj) is True
assert dfs_topo(diamond[0], adj) is not None

tri = (["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
print("triangle, three-colour DFS       ", dfs_topo(tri[0], build(*tri)), "(a real cycle)")
assert dfs_topo(tri[0], build(*tri)) is None

small = ([0, 1, 2], [(1, 2)])
print("nodes 0,1,2 with only 1->2, DFS  ", dfs_topo(small[0], build(*small)))
assert dfs_topo(small[0], build(*small)) == [1, 2, 0]
print("valid, but the lexicographically smallest order is [0, 1, 2]")
```

## What to memorise

The template, typed without thinking:

```python
indeg = {v: 0 for v in nodes}
for before, after in edges:
    adj[before].append(after)
    indeg[after] += 1
ready = [v for v in nodes if indeg[v] == 0]     # seed from nodes
order = []
while ready:
    v = pop(ready)                              # queue / stack / heap: your choice
    order.append(v)
    for w in adj[v]:
        indeg[w] -= 1
        if indeg[w] == 0:
            ready.push(w)
return order if len(order) == len(nodes) else []
```

The sentence that turns a problem into it: *"Is there a 'must come before'
relation, and do I need one line that respects all of it?"* If yes, the only
remaining decisions are which container `ready` is and what you compute while
you drain it.

The habit that prevents the common bug: after writing the graph build, read one
dependency out loud — "a depends on d, so the edge is `d → a`, so `indeg[a]`
goes up" — and check it against the statement's own wording before writing
anything else.

Numbers worth carrying: `Θ(n + m)` with a queue or stack, `Θ(m + n log n)` with
a heap. Recursion depth `n`, which is fatal past about a thousand in Python.
`len(order) == n` is the cycle test, and it is the only one.

## Check yourself

:::check
The correctness proof never says which vertex to take out of the ready set. Why
not, and what does that freedom buy you?
--
Because no later step of the proof refers to the choice. The invariants I1, I2
and I3 are restored by *popping some zero-debt vertex*, whichever it is: I3 only
needs `deg[v] = 0` at the moment of the pop, and I1 and I2 only care that
counters go down and that anything hitting zero is pushed.

What it buys you is that the entire family of problems collapses to one
algorithm. A FIFO queue gives a stable, input-order result (*Task Dependency
Ordering*); a min-heap gives the lexicographically smallest (*Lexicographically
Smallest Dependency Order*); a heap keyed by first appearance gives the Roblox
variant; a stack gives something depth-first-ish. Same proof, four problems. It
also tells you that the ordering constraint and the tie-break are independent —
the in-degree bookkeeping enforces the dependencies, the container only picks
among options that are all already legal.
:::

:::check
Someone says: "to get the lexicographically smallest topological order, run DFS
starting from the smallest unvisited vertex each time and reverse the post-order.
That visits small vertices first, so the result is smallest." Where are they
wrong?
--
The construction is a valid topological sort but not the smallest one, and the
last runnable block shows the minimal counterexample: three vertices `0, 1, 2`
with the single edge `1 → 2`.

DFS from `0` finishes `0` immediately, so `0` is the *first* vertex pushed onto
the post-order list — which means it ends up *last* after reversing. The result
is `[1, 2, 0]`. The lexicographically smallest valid order is `[0, 1, 2]`, since
`0` is unconstrained.

The flaw is that reverse post-order rewards vertices that finish *late*, and
finishing late is not the same as starting early. A vertex with no descendants
finishes instantly and is therefore pushed to the back. Greedy smallest-first
needs a structure that lets you reconsider at every step — the ready heap does,
a DFS that must run one branch to completion does not.
:::

:::check
Finding the longest path in a general directed graph is NP-hard, yet the DAG
block computes the heaviest chain in `Θ(n + m)`. What exactly makes the problem
easy here, and what breaks in a graph with a cycle?
--
Two things, and they are the same thing seen twice.

First, on a DAG every path is automatically simple — no vertex can repeat,
because repeating one would give a cycle. So "longest path" and "longest simple
path" coincide, and the hard constraint in the general problem (do not reuse a
vertex) costs nothing to enforce.

Second, that gives an optimal-substructure recurrence with no cross-talk:
`best[v] = w(v) + max(best[u])` over in-neighbours `u`. A topological order lets
you evaluate it in one pass, because when you reach `v` every `u` with an edge
into `v` has already been finalised and nothing later can improve it.

In a cyclic graph both collapse. The recurrence becomes circular — `best[v]`
depends on `best[u]` depends on `best[v]` — and there is no evaluation order that
finalises anything. Forbidding reuse re-introduces the constraint you would have
to carry in the state, which is the `2ⁿ` subset in [[dp-bitmask]], and that is
the hardness.
:::

:::check
Prove that popping the smallest ready vertex at every step really yields the
lexicographically smallest topological order. (An exchange argument is enough.)
--
Let `G` be the greedy output and `X` any valid topological order, and let `i` be
the first position where they differ, so they agree on positions `0..i-1`. Write
`g = G[i]` and `x = X[i]`.

At step `i` the greedy had exactly the vertices not yet emitted whose
prerequisites were all in the common prefix — and by the invariant that set is
precisely the ready set. Both `g` and `x` are in it: `x` because `X` is valid and
its first `i` entries are the same prefix, `g` by construction. Greedy takes the
smallest, so `g <= x`, and since they differ, `g < x`.

Now build `X'` from `X` by deleting `g` from wherever it appears later and
inserting it at position `i`. `X'` is still a valid topological order: nothing
before position `i` moved, `g`'s prerequisites are all in the prefix so it is
legal at `i`, and everything that was between `i` and `g`'s old position shifts
one place later, which can only move vertices further from their prerequisites.
And `X'` is lexicographically smaller than `X`, because they agree up to `i-1`
and `X'[i] = g < x = X[i]`.

So any order that deviates from greedy at its first difference can be strictly
improved. Hence no valid order is smaller than `G`, and `G` is the minimum. The
brute force in the implementation block checks this over all 720 permutations of
the six-vertex example.
:::

:::check
You run Kahn on a dependency graph of 8 tasks and get 5 in the output. A
colleague says: "so 3 tasks are stuck, but maybe they are just waiting on
something outside the graph — we should not call it a cycle." Are they right?
--
No, not if the graph is the whole input. The proof's stalling argument is
constructive: when the ready set empties with `S` non-empty, every vertex in `S`
has `deg > 0`, and `deg` counts only in-edges from vertices *still in* `S`.
Following those in-edges backwards inside a finite set must revisit a vertex,
and that revisit exhibits a directed cycle. There is nowhere else for the
blockage to come from.

Where the colleague could be right is one level up, in the modelling. If the edge
list mentions a prerequisite that was never added to the vertex list — a course
outside `0..n-1`, a module name only ever seen on the right-hand side — then the
graph you built is not the graph you meant, and the "cycle" is a data bug. That
is why the vertex set must be constructed deliberately: either every name seen
anywhere becomes a vertex, or unknown names are rejected up front. Silently
raising an in-degree for a vertex that will never be popped is the same failure
as forgetting to seed isolated ones, in mirror image.
:::
