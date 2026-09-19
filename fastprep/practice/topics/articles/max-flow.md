# Max Flow and Min Cut

> Max flow is not about pipes. It is about the fact that the most you can push
> through a network is exactly the cheapest way to cut it in two — so every
> "how many can I do at once" question is secretly a question about bottlenecks.

## When you reach for it

You reach for flow when several things compete for the same limited resources
and you are asked **how many can succeed simultaneously**. Not "what is the best
route" ([[dijkstra]]), not "are these connected" ([[union-find]]), but: every
road, machine and shift has a ceiling — how many demands can you satisfy at once.

The cleanest instance, and the one interviews actually ask, is **bipartite
matching**: two sets, a compatibility relation between them, pair them up so that
nobody appears twice, as many pairs as possible. *Maximum Programmer-Problem
Matching* in this bank is exactly it — a programmer is compatible with a problem
when their skills and its tags share a string, "each programmer and each problem
appears in at most one pair", maximise the pairs.

The mirror question is the other half of the topic: **what is the smallest
obstruction**. "Remove the fewest roads so the depot cannot reach the port."
Those are minimum cuts, and the theorem here says the two questions always have
the same numeric answer.

A word about this bank. The tag reports 114 problems, rank #31 of 150, which
would make max flow bread-and-butter. It is not, and the reason is the word
*matching*: almost all 114 are string pattern matching — *Wildcard Matching
with Stars*, *Is Regex Matching*, *Find a Submatrix Matching a Pattern* — where
the tools are [[dp-strings]] and [[string-matching]]. Treat the count as a
warning: most problems with "matching" in the title are not this topic, and
telling the difference is half the skill here.

It is the wrong tool when the pairing has structure a [[greedy|greedy rule]]
already exploits. *Assign Cookies With Matching Parity* is a genuine bipartite
matching — compatible when `s[j] >= g[i]` and the parities agree — on which flow
would be correct and hopeless: with 3·10⁴ per side the compatibility graph has up
to 9·10⁸ edges, while sorting each parity class and sweeping two pointers is
optimal. Flow is the tool when compatibility is **arbitrary**; when it is an
interval, a threshold or a prefix, look for something cheaper first.

## The idea

Think of the network as plumbing. Each directed edge is a pipe with a capacity,
`s` is the reservoir, `t` the drain, and every junction passes out exactly what
it takes in. You want the largest steady rate from `s` to `t`.

The naive plan is greedy: find any route from `s` to `t` with spare capacity,
push as much as the tightest pipe allows, repeat. It fails for the reason every
greedy fails — an early choice can block a later one. Send a unit down the middle
pipe and you may have stolen the only route someone else had.

The whole algorithm is one repair to that plan:

> Whenever you push `x` units along a pipe, grant yourself the standing right to
> push `x` units **back** along it later.

That is not cheating. Pushing a unit backwards along an edge that carries a unit
does not make a pipe flow uphill; it *cancels*, and what remains is a different,
still-legal routing of the same water. Instead of backtracking in the control
flow, the algorithm turns undoing into an ordinary forward move on a modified
graph.

That modified graph is the **residual graph**. For every edge `u → v` of
capacity `c` currently carrying `f`, it has

- a forward arc `u → v` of capacity `c − f` — what is left, and
- a backward arc `v → u` of capacity `f` — what can be taken back.

<svg viewBox="0 0 660 200" role="img" aria-label="a pipe carrying 2 of 3 units, redrawn as a forward residual arc of 1 and a backward residual arc of 2">
  <g>
    <circle cx="60" cy="70" r="20"/>
    <text x="60" y="76" text-anchor="middle">u</text>
    <circle cx="230" cy="70" r="20"/>
    <text x="230" y="76" text-anchor="middle">v</text>
    <line x1="80" y1="70" x2="208" y2="70"/>
    <line x1="210" y1="70" x2="197" y2="63"/>
    <line x1="210" y1="70" x2="197" y2="77"/>
    <text x="145" y="58" text-anchor="middle">flow 2 / cap 3</text>
    <text x="145" y="130" text-anchor="middle">the real pipe</text>
    <line x1="290" y1="70" x2="350" y2="70"/>
    <line x1="350" y1="70" x2="338" y2="63"/>
    <line x1="350" y1="70" x2="338" y2="77"/>
    <text x="320" y="55" text-anchor="middle">becomes</text>
    <circle cx="440" cy="70" r="20"/>
    <text x="440" y="76" text-anchor="middle">u</text>
    <circle cx="610" cy="70" r="20"/>
    <text x="610" y="76" text-anchor="middle">v</text>
    <line x1="460" y1="55" x2="588" y2="55"/>
    <line x1="590" y1="55" x2="577" y2="48"/>
    <line x1="590" y1="55" x2="577" y2="62"/>
    <text x="525" y="43" text-anchor="middle">1 left to give</text>
    <line x1="590" y1="90" x2="462" y2="90"/>
    <line x1="460" y1="90" x2="473" y2="83"/>
    <line x1="460" y1="90" x2="473" y2="97"/>
    <text x="525" y="112" text-anchor="middle">2 you may take back</text>
    <text x="525" y="150" text-anchor="middle">the residual graph</text>
  </g>
</svg>

Now the algorithm is three lines. **While there is a path from `s` to `t` in the
residual graph, push the bottleneck amount along it and update both arcs of
every edge you used.** Such a path is called an *augmenting path*. When none
exists, stop.

The second half of the idea is what "when none exists" means. Let `S` be the
vertices still reachable from `s` in the residual graph: `s ∈ S`, `t ∉ S`, and
every edge leaving `S` is completely full, or its forward arc would be open and
its head would be in `S`. So the flow exactly fills a wall separating `s` from
`t`. Everything travelling from `s` to `t` must cross that wall, so no flow can
beat its capacity and yours has met it — the largest flow and the cheapest wall,
found together. That is the max-flow min-cut theorem, and the stopping condition
is its proof.

## Worked by hand

Take a three-by-three version of *Maximum Programmer-Problem Matching*.
Programmers `A`, `B`, `C`; problems `X`, `Y`, `Z`; compatibility

```
A : X, Y, Z        B : X        C : X
```

Turn it into a network: a source `s` with a capacity-1 edge into each
programmer, a capacity-1 edge per compatible pair, and a capacity-1 edge from
each problem to the sink `t`. Every capacity is 1, so a unit of flow is a pair
and the flow value is the number of pairs; the edges out of `s` enforce "each
programmer at most once" and those into `t` "each problem at most once".

Search for augmenting paths with [[bfs]], exploring vertices in the order
`A, B, C` and `X, Y, Z`.

| round | residual layers from `s` | augmenting path | push | pairs after |
| --- | --- | --- | --- | --- |
| 1 | `{A,B,C}`, `{X,Y,Z}`, `{t}` | `s → A → X → t` | 1 | `X=A` |
| 2 | `{B,C}`, `{X}`, `{A}`, `{Y,Z}`, `{t}` | `s → B → X → A → Y → t` | 1 | `X=B`, `Y=A` |
| 3 | `{C}`, `{X}`, `{B}` — stuck | none | — | `X=B`, `Y=A` |

Maximum flow 2, so the answer is two pairs.

Round 2 is the whole chapter in one line. `s → A` is full, so the search starts
from `B` and `C`; both only reach `X`; `X → t` is full, so it cannot go forward —
but `X → A` is a *backward* arc carrying the unit `A` put there, so the search
walks it to `A`, which still has `Y` and `Z` open. Pushing one unit along
`s → B → X → A → Y → t` adds a unit on `B → X`, **subtracts** the unit on
`A → X`, and adds a unit on `A → Y`: `B` takes `X`, and `A`, displaced, moves to
`Y`. Nobody was unmatched on the way and the count went up by one. The
*alternating path* of matching theory and the *augmenting path* of flow theory
are the same object.

Round 3 is the second half. The search dies having reached `S = {s, C, X, B}`,
and the edges leaving `S` are `s → A` and `X → t`, total capacity 2 — the
certificate that 2 is optimal, produced by the search that failed. Read it in the
bipartite graph: `{A, X}` is a set of two vertices touching every compatible
pair, so two pairs is the most there can be. That equality is Kőnig's theorem,
and the cut is where it comes from.

<svg viewBox="0 0 640 260" role="img" aria-label="the bipartite instance as a flow network with the minimum cut crossing the s-to-A edge and the X-to-t edge">
  <g>
    <circle cx="45" cy="130" r="20"/>
    <text x="45" y="136" text-anchor="middle">s</text>
    <circle cx="220" cy="55" r="20"/>
    <text x="220" y="61" text-anchor="middle">A</text>
    <circle cx="220" cy="130" r="20"/>
    <text x="220" y="136" text-anchor="middle">B</text>
    <circle cx="220" cy="205" r="20"/>
    <text x="220" y="211" text-anchor="middle">C</text>
    <circle cx="420" cy="55" r="20"/>
    <text x="420" y="61" text-anchor="middle">X</text>
    <circle cx="420" cy="130" r="20"/>
    <text x="420" y="136" text-anchor="middle">Y</text>
    <circle cx="420" cy="205" r="20"/>
    <text x="420" y="211" text-anchor="middle">Z</text>
    <circle cx="595" cy="130" r="20"/>
    <text x="595" y="136" text-anchor="middle">t</text>
    <line x1="63" y1="118" x2="202" y2="66"/>
    <line x1="65" y1="130" x2="200" y2="130"/>
    <line x1="63" y1="142" x2="202" y2="194"/>
    <line x1="240" y1="55" x2="400" y2="55"/>
    <line x1="240" y1="63" x2="400" y2="122"/>
    <line x1="240" y1="70" x2="401" y2="192"/>
    <line x1="240" y1="122" x2="400" y2="63"/>
    <line x1="240" y1="196" x2="401" y2="70"/>
    <line x1="440" y1="66" x2="578" y2="118"/>
    <line x1="440" y1="130" x2="575" y2="130"/>
    <line x1="440" y1="194" x2="578" y2="142"/>
    <line x1="140" y1="20" x2="140" y2="100" stroke-dasharray="6 5"/>
    <line x1="140" y1="100" x2="500" y2="100" stroke-dasharray="6 5"/>
    <line x1="500" y1="100" x2="500" y2="20" stroke-dasharray="6 5"/>
    <text x="320" y="248" text-anchor="middle">the cut: s to A, and X to t — capacity 2</text>
  </g>
</svg>

Two things the trace shows that reading the code would not. First, the algorithm
never *revisits* a decision: there is no stack of choices, no undo log. The undo
is a forward edge in a graph that has been quietly rewritten, which is why the
implementation is a plain loop. Second, the failed search is not wasted work — it
is the proof of optimality. If you ever want to know *why* the answer is not
bigger, the answer is sitting in the set of vertices the last search reached.

## Why it is correct

State the objects precisely first. A network is a directed graph on `V` with a
capacity `c(u, v) >= 0` for every ordered pair (zero where there is no edge), a
source `s` and a sink `t`. Describe a flow by its **net** value on ordered
pairs: a function `f` with

- **skew symmetry** `f(u, v) = −f(v, u)`,
- **capacity** `f(u, v) <= c(u, v)`,
- **conservation** `Σ_v f(u, v) = 0` for every `u` outside `{s, t}`.

Its value is `|f| = Σ_v f(s, v)`. A **cut** `(S, T)` is a partition of `V` with
`s ∈ S` and `t ∈ T`; its capacity is `cap(S, T) = Σ_{u∈S, v∈T} c(u, v)`, counting
only the edges pointing out of `S`.

:::proof Ford-Fulkerson terminates at a flow whose value equals a cut's capacity
**Lemma (every cut measures the same flow).** For any flow `f` and any cut
`(S, T)`, `Σ_{u∈S, v∈T} f(u, v) = |f|`.

*Proof.* Start from `Σ_{u∈S} Σ_{v∈V} f(u, v)`. Conservation kills every term with
`u ≠ s`, leaving `Σ_v f(s, v) = |f|`. Now split the inner sum by whether `v` is
in `S` or in `T`. The part with both endpoints in `S` is zero: every unordered
pair `{u, v} ⊆ S` contributes `f(u, v) + f(v, u) = 0` by skew symmetry. What
remains is `Σ_{u∈S, v∈T} f(u, v)`. ∎

**Corollary (weak duality).** `|f| <= Σ_{u∈S,v∈T} c(u,v) = cap(S, T)` for every
flow and every cut. So max flow `<=` min cut, and any flow whose value equals
some cut's capacity is maximum while that cut is minimum.

**Invariant.** After every iteration, `f` is a feasible flow (skew-symmetric,
within capacity, conserving), and `|f|` is a non-negative integer.

**Base case.** `f ≡ 0` satisfies all three properties, and `|f| = 0`.

**Inductive step.** Suppose the invariant holds and the residual graph — arcs
`u → v` with residual capacity `c_f(u, v) = c(u, v) − f(u, v) > 0` — contains a
simple path `P` from `s` to `t`. Let `Δ = min` of `c_f` over the arcs of `P`;
`Δ > 0` by construction, and `Δ` is an integer because all capacities and all
current flows are. Augmenting means `f(u, v) += Δ` and `f(v, u) −= Δ` for each
arc of `P`.

*Skew symmetry* holds because both entries of each pair are updated together.
*Capacity* holds on each arc of `P`, since the new value
`f(u, v) + Δ <= f(u, v) + c_f(u, v) = c(u, v)`, and on its reverse, where
`f(v, u)` only decreases and so stays below the unchanged `c(v, u)`.
*Conservation*: an internal vertex `w` of `P` has exactly one in-arc `x → w` and
one out-arc `w → y` on `P`, because `P` is simple. The update adds `Δ` to
`f(w, y)` and adds `Δ` to `f(x, w)`, which is `−Δ` on `f(w, x)`, so `Σ_v f(w, v)`
changes by `Δ − Δ = 0`. Vertices off `P` are untouched, and `|f|` grows by
exactly `Δ` because `P` leaves `s` once.

**Termination.** With integer capacities, every iteration increases the integer
`|f|` by `Δ >= 1`, and by weak duality `|f| <= cap({s}, V∖{s})`, a finite
constant. So the loop runs at most that many times.

**Conclusion.** At exit no augmenting path exists. Let `S` be the vertices
reachable from `s` in the residual graph and `T = V ∖ S`; then `s ∈ S` and
`t ∈ T`, so `(S, T)` is a cut. For any `u ∈ S`, `v ∈ T` we must have
`c_f(u, v) = 0`, otherwise `v` would be reachable — that is, `f(u, v) = c(u, v)`.
Summing and applying the Lemma,

`|f| = Σ_{u∈S, v∈T} f(u, v) = Σ_{u∈S, v∈T} c(u, v) = cap(S, T)`.

By the corollary, `f` is a maximum flow and `(S, T)` is a minimum cut, and their
common value is the same number. ∎
:::

Two free consequences. The **integrality theorem**: every augmentation moved an
integer amount, so integer capacities give an integral maximum flow — which is
what makes matching work. And **Menger's theorem**: with every capacity 1, the
maximum flow is the number of edge-disjoint `s`–`t` paths and the minimum cut is
the fewest edges whose removal disconnects them.

Now the assumptions, because that list is where the bugs live.

- **Capacities are non-negative.** Used everywhere, including "`Δ > 0`".
- **Capacities are integers (or rationals).** Used *only* in termination, and
  not a formality: with irrational capacities Ford-Fulkerson can run forever and
  converge below the maximum. Edmonds-Karp needs no such assumption.
- **The residual graph has backward arcs.** Used in the Conclusion: without them
  "no augmenting path" does not imply the crossing edges are saturated, and the
  final equality collapses.
- **Conservation holds everywhere except `s` and `t`.** Nothing limits what
  passes *through* a vertex, so "each machine handles at most 3 jobs" is not
  expressible until you split the machine in two.
- **Net flow, not two independent numbers.** The Lemma's cancellation
  `f(u,v) + f(v,u) = 0` is why antiparallel edges need paired entries and not a
  `cap[u][v]` matrix, where a residual arc and a real reverse edge look alike.
- **The augmenting path is simple**, which conservation used as "one in-arc and
  one out-arc per internal vertex". BFS and DFS give that for free.
- **`s` has no incoming edges**, or `|f|` is the *net* outflow.

## What it costs

Each iteration is one graph search plus one walk back along the path, `O(E)` on
a connected network. So the cost is `O(E)` times the number of augmentations, and
the whole question is *how many augmentations*.

**With an arbitrary path chooser (Ford-Fulkerson).** The proof only promised
`Δ >= 1`, so the bound is the flow value itself: `O(E · f*)`. That is
**pseudo-polynomial** — linear in the *value* of the numbers, not in the bits
used to write them, so a capacity of `10⁹` is ten characters to type and a
billion iterations to run. The classic instance has four vertices: `s→a`, `s→b`,
`a→t`, `b→t` at capacity `1000`, plus a middle edge `a→b` at capacity `1`. The
answer is 2000, and a chooser alternating `s→a→b→t` with `s→b→a→t` (the second
using the backward arc) moves one unit per round, so it needs 2000 rounds. The
third code block runs both.

**With BFS (Edmonds-Karp).** Choosing the *shortest* augmenting path bounds the
iterations independently of the capacities. Write `d_f(v)` for the number of arcs
on the shortest residual path from `s` to `v`.

*Claim 1: `d_f(v)` never decreases.* Suppose some distance dropped after an
augmentation; among those take the `v` with the smallest new distance `d'(v)`,
and let `u` be its predecessor on a new shortest path, so `d'(v) = d'(u) + 1` and,
by minimality of `v`, `d'(u) >= d(u)`. If the arc `u → v` existed before, then
`d(v) <= d(u) + 1 <= d'(u) + 1 = d'(v)`, contradicting the drop. So `u → v` is
new, which happens only if the augmentation pushed along `v → u`; that path was a
shortest one, so `d(u) = d(v) + 1` and `d'(v) = d'(u) + 1 >= d(v) + 2 > d(v)`.
Contradiction either way.

*Claim 2: each arc is the bottleneck at most `V/2` times.* Call `u → v` critical
in a round when it is the tightest arc on the chosen path; it then vanishes from
the residual graph, and at that moment `d(u) = d(v) − 1`. It returns only when a
later round pushes along `v → u`, where `d'(v) = d'(u) − 1`, so by Claim 1
`d'(u) = d'(v) + 1 >= d(v) + 1 = d(u) + 2`. Between two criticalities of an arc,
`d(u)` grows by at least 2; distances stay below `V`, so an arc is critical at
most `V/2` times.

Every round makes at least one arc critical, so there are `O(VE)` rounds and
**Edmonds-Karp is `O(V E²)`** — with no reference to the capacities at all.

**Unit capacities (matching).** Here the simple bound beats the general one: the
flow value is at most `min(|L|, |R|) <= V`, so there are at most `V`
augmentations and the total is **`O(V E)`**. Hopcroft-Karp improves that to
`O(E √V)` by augmenting along a maximal set of shortest paths at once; Dinic's
algorithm, the same idea for general capacities, is `O(V² E)`.

**Space** is `O(V + E)`: parallel arrays `to` and `cap` of length `2E`, an
adjacency list of edge indices, and one `O(V)` parent array per round.

**The cost people forget** is building the graph. *Maximum Programmer-Problem
Matching* defines compatibility as "the skill list and the tag list share at
least one string", and comparing every programmer to every problem list-by-list
costs `O(n · m · k)`, which can dominate the flow. Invert it with a
[[hash-tables|hash map]] from tag to the problems carrying it. What you cannot
escape is the number of compatible pairs: if everyone shares a tag with
everything, `E = n·m` whatever you do.

## The implementation

Edmonds-Karp, with the min cut extracted from the final search, and a
brute-force check of the theorem on two hundred random networks.

```python run
from collections import deque
from itertools import combinations
import random


class Flow:
    """Edmonds-Karp: augment along a shortest residual path until stuck."""

    def __init__(self, n):
        self.n, self.to, self.cap = n, [], []
        self.adj = [[] for _ in range(n)]

    def add(self, u, v, c):
        self.adj[u].append(len(self.to)); self.to.append(v); self.cap.append(c)
        self.adj[v].append(len(self.to)); self.to.append(u); self.cap.append(0)

    def maxflow(self, s, t):
        total = 0
        while True:
            parent = [-1] * self.n            # the edge index used to enter v
            parent[s], q = -2, deque([s])
            while q and parent[t] == -1:
                u = q.popleft()
                for e in self.adj[u]:
                    if self.cap[e] > 0 and parent[self.to[e]] == -1:
                        parent[self.to[e]] = e
                        q.append(self.to[e])
            if parent[t] == -1:
                return total
            push, v = float("inf"), t         # the bottleneck, walking back
            while v != s:
                push = min(push, self.cap[parent[v]]); v = self.to[parent[v] ^ 1]
            v = t
            while v != s:
                e = parent[v]
                self.cap[e] -= push; self.cap[e ^ 1] += push; v = self.to[e ^ 1]
            total += push

    def reachable(self, s):
        seen, q = {s}, deque([s])             # residual-reachable: the cut side
        while q:
            for e in self.adj[q.popleft()]:
                if self.cap[e] > 0 and self.to[e] not in seen:
                    seen.add(self.to[e]); q.append(self.to[e])
        return seen


edges = [(0, 1, 3), (0, 2, 2), (1, 2, 5), (1, 3, 1), (2, 3, 3)]
g = Flow(4)
for u, v, c in edges:
    g.add(u, v, c)
val = g.maxflow(0, 3)
S = g.reachable(0)
cut = [(u, v, c) for u, v, c in edges if u in S and v not in S]
print("max flow s->t  :", val)
print("cut side S     :", sorted(S), "  cut edges:", cut)
print("cut capacity   :", sum(c for _, _, c in cut))
assert val == 4 and sum(c for _, _, c in cut) == val

rng = random.Random(5)
for _ in range(200):                          # the theorem, checked by brute force
    n = rng.randint(2, 6)
    es = [(u, v, rng.randint(1, 6)) for u in range(n) for v in range(n)
          if u != v and rng.random() < 0.5]
    g = Flow(n)
    for u, v, c in es:
        g.add(u, v, c)
    mid = list(range(1, n - 1))
    best = min(sum(c for u, v, c in es if u in A and v not in A)
               for k in range(len(mid) + 1)
               for A in [{0} | set(p) for p in combinations(mid, k)])
    assert g.maxflow(0, n - 1) == best, es
print("200 random networks: max flow equals the cheapest of all 2^(V-2) cuts")
```

Three lines carry the weight.

`self.cap[e ^ 1]` is the entire residual mechanism. Edges are added in pairs, so
the reverse of `e` is always `e ^ 1`; subtracting `push` from one and adding it
to the other is the skew-symmetric update of the proof, and "take back what you
pushed" costs nothing extra to represent.

`self.cap.append(0)` is the number you must get right: a directed edge's backward
arc starts empty, while an *undirected* edge of capacity `c` appends `c` — one
pipe usable either way.

`reachable(s)` is not an extra algorithm, it is the last BFS re-run. It hands you
the minimum cut as a side effect, and asserting that its capacity equals the flow
is the cheapest self-test you will write.

Now bipartite matching. You can feed it into the class above, and under time
pressure you should. But the specialisation is worth knowing, because it is what
flow reduces to once every capacity is 1: **for each left vertex, look for an
alternating path**. The recursion in `augment` *is* the residual back arc — "if
`v` is taken, ask its owner to move".

```python run
from itertools import permutations
import random


def max_matching(nL, nR, adj):
    """Kuhn's algorithm: one augmenting path per left vertex."""
    owner = [-1] * nR                        # owner[v] = left vertex holding v

    def augment(u, seen):
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                if owner[v] == -1 or augment(owner[v], seen):
                    owner[v] = u             # take v; its old owner moved on
                    return True
        return False

    return sum(augment(u, set()) for u in range(nL)), owner


def konig_cover(nL, nR, adj, owner):
    """Minimum vertex cover, built from a maximum matching."""
    held = [-1] * nL
    for v, u in enumerate(owner):
        if u != -1:
            held[u] = v
    free = [u for u in range(nL) if held[u] == -1]
    seen_L, seen_R, stack = set(free), set(), list(free)
    while stack:                             # alternating walk from unmatched left
        u = stack.pop()
        for v in adj[u]:
            if v != held[u] and v not in seen_R:
                seen_R.add(v)
                if owner[v] != -1 and owner[v] not in seen_L:
                    seen_L.add(owner[v]); stack.append(owner[v])
    return [("L", u) for u in range(nL) if u not in seen_L] + \
           [("R", v) for v in sorted(seen_R)]


L, R = ["A", "B", "C"], ["X", "Y", "Z"]
adj = [[0, 1, 2], [0], [0]]                  # A:{X,Y,Z}   B:{X}   C:{X}
size, owner = max_matching(3, 3, adj)
print("pairs           :", {R[v]: L[u] for v, u in enumerate(owner) if u != -1})
cover = konig_cover(3, 3, adj, owner)
print("maximum matching:", size, "  minimum vertex cover:",
      [(L if s == "L" else R)[i] for s, i in cover])
assert size == 2 and len(cover) == 2
all_edges = {(u, v) for u in range(3) for v in adj[u]}
covered = {(u, v) for u, v in all_edges if ("L", u) in cover or ("R", v) in cover}
assert covered == all_edges, "the cover misses an edge"

rng = random.Random(3)
for _ in range(300):                         # against brute force over all pairings
    nL, nR = rng.randint(1, 4), rng.randint(1, 4)
    a = [[v for v in range(nR) if rng.random() < 0.5] for _ in range(nL)]
    got, own = max_matching(nL, nR, a)
    best = 0
    for k in range(min(nL, nR), 0, -1):
        if any(all(r in a[l] for l, r in zip(left, right))
               for left in permutations(range(nL), k)
               for right in permutations(range(nR), k)):
            best = k
            break
    assert got == best and len(konig_cover(nL, nR, a, own)) == got, a
print("300 random bipartite graphs: matching = brute force = cover size")
```

The `seen` set is per augmenting search, not global — it prevents the recursion
from looping, and resetting it for each left vertex is what lets a right vertex
be re-examined in a later round. Sharing one `seen` across all rounds is a
popular and silent bug.

## Variants you will meet

**Bipartite matching.** The unit-capacity case above. See [[bipartite]] for how
to find the two sides when the problem does not hand them to you — and note that
if the graph is *not* bipartite none of this applies: general matching needs
Edmonds' blossom algorithm, which is not an interview answer.

**Vertex capacities.** Split `v` into `v_in → v_out` with an edge of the
vertex's capacity, incoming edges at `v_in` and outgoing from `v_out`. "At most
`k` jobs per machine" and "vertex-disjoint paths" are both this.

**Several sources or sinks.** Add a super-source with a large edge to each real
source, and symmetrically a super-sink; the code need not know.

**Minimum cut as the real question.** "Fewest edges to disconnect `a` from `b`"
sets all capacities to 1 and reports the flow; "which edges" reports the ones
leaving the residual-reachable set.

**Minimum path cover of a DAG.** The fewest vertex-disjoint paths covering every
vertex is `n − (maximum matching)` in the bipartite graph with a left and a right
copy of every vertex and an edge `u_L → v_R` per DAG edge. Pairs with
[[topological-sort]].

**Project selection / maximum closure.** Profitable tasks with prerequisite
costs: source to each profit, each cost to sink, infinite capacity along
dependencies. Maximum profit is `total profit − min cut`, and the cut chooses
what to abandon.

**Min-cost max-flow.** Edges gain a per-unit cost and you want the cheapest
maximum flow — the assignment problem, where the score of the pairs matters and
not only their number. Replace BFS by shortest paths with potentials
([[dijkstra]]) or by [[bellman-ford]]; the loop is unchanged.

**Dinic's algorithm.** Layer the residual graph by BFS, then push a blocking
flow through the layers with DFS. Same theory, far fewer BFS calls, `O(V² E)`.

**Feasibility plus [[binary-search-on-answer]].** "The largest `k` such that
every centre gets `k` staff" — parameterise the network by `k` and test whether
the flow saturates. Monotone, since a larger `k` only tightens the demands.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **"Each X is used at most once, each Y is used at most once, maximise the
   number of pairs."** The definition of bipartite matching, stated almost
   verbatim by *Maximum Programmer-Problem Matching*. The "at most once" on
   *both* sides is the signal; on one side only it is a greedy selection.
2. **Capacities plus simultaneity.** Numeric limits on edges, machines or
   shifts, and a total achieved *at once* rather than in sequence.
3. **"Fewest things to remove so that A can no longer reach B."** Minimum cut.
   "Remove" with a reachability goal is as close to a giveaway as this gets.
4. **Tiny bounds with a pairing flavour.** `n <= 200` where brute force is
   exponential is often a flow bound; `O(V E²)` does not survive `10⁵`, so large
   inputs argue *against* flow, not for it.
5. **A naturally two-sided conflict graph** — people and shifts, machines and
   jobs — with compatibility *listed* rather than computed from a rule.

The anti-signals, which in this bank matter more than the signals:

- **"Matching" meaning string matching.** *Wildcard Matching with Stars*, *Is
  Regex Matching* and *Find a Submatrix Matching a Pattern* dominate this bank
  and have nothing to do with flow. If the two things being matched are a text
  and a pattern rather than two sets of *entities*, stop: [[dp-strings]],
  [[string-matching]], [[matrix-traversal]].
- **"Report every valid pair."** *Lab and Consultation Appointment Matching*
  wants every lab-then-consultation journey within a 60-minute wait, sorted — all
  of them, not a maximum disjoint set. That is sorting and [[two-pointers]].
  Maximality is what makes a problem a flow problem.
- **Order matching.** *Price-Time Order Matching* and *Limit Order Book Matching
  Engine* pair buyers with sellers under a given price-time priority rule. The
  rule is given, so there is nothing to maximise: [[heap]]-driven [[simulation]].
- **A pairing rule that is a threshold or an interval.** *Assign Cookies With
  Matching Parity*, above: bipartite in form, but sort each parity class and
  sweep. Look for the structure before the machinery.
- **Counting disjoint pairs of equal values.** *Tally the Number of Friend Groups
  with K Sets of Matching Traits* counts subarrays holding `k` disjoint pairs of
  equal values — but two equal values are always pairable, so a window holds
  `Σ ⌊count(value)/2⌋` pairs: a [[frequency-counting|frequency count]] inside a
  [[sliding-window]], no graph.

## Traps

**Omitting the backward arcs, or giving them the wrong capacity.** Symptom: an
answer too small, and only on inputs needing a rematch — which small hand-made
tests usually do not have. Demonstrated below.

**Believing the saturated edges are the min cut.** In the network in the
implementation block the flow saturates `s → b`, `a → t` and `b → t`, three edges
totalling 6, while the minimum cut `{a → t, b → t}` costs 4. The cut is the edges
*leaving the residual-reachable set*, a strictly smaller collection. Symptom: an
answer too large on "which edges do I remove".

**Leaving the path choice to DFS on big capacities.** The answer is right, the
running time is `O(E · f*)`. Symptom: passes every sample, times out on
nine-digit capacities. Demonstrated below.

**Forgetting to split vertices with capacities.** Symptom: a flow routing five
units through a machine that handles three, with no error anywhere.

**Antiparallel edges in a matrix representation.** With `cap[u][v]` the residual
arc of `u → v` and the real edge `v → u` share a cell. Symptom: a flow larger
than the maximum.

**Sharing the `seen` set across augmenting searches in Kuhn.** Symptom: a
matching too small, varying with vertex order. And recursing in Kuhn on a deep
graph costs a stack frame per alternating-path step: `RecursionError` at a few
thousand vertices.

**Assuming the maximum flow is unique.** The *value* is unique; the flow, and
often the minimum cut, are not. Printing a specific assignment needs a tie-break
rule, and your output may legitimately differ from the sample.

```python run
adj = [[0, 1, 2], [0], [0]]                  # A:{X,Y,Z}   B:{X}   C:{X}


def no_undo(nL, adj, nR):
    """Every left vertex grabs a free partner. No residual, no rematch."""
    taken, size = [-1] * nR, 0
    for u in range(nL):
        for v in adj[u]:
            if taken[v] == -1:
                taken[v] = u; size += 1; break
    return size


def with_undo(nL, adj, nR):
    taken = [-1] * nR

    def aug(u, seen):
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                if taken[v] == -1 or aug(taken[v], seen):
                    taken[v] = u; return True
        return False

    return sum(aug(u, set()) for u in range(nL))


print("no backward arcs:", no_undo(3, adj, 3), "pairs   (A grabs X; B and C starve)")
print("with backward   :", with_undo(3, adj, 3), "pairs   (A steps aside to Y)")
assert no_undo(3, adj, 3) == 1 and with_undo(3, adj, 3) == 2


def push(res, path):
    """Send the bottleneck of `path` along it; return how much moved."""
    amount = min(res[u][v] for u, v in zip(path, path[1:]))
    for u, v in zip(path, path[1:]):
        res[u][v] -= amount; res[v][u] += amount
    return amount


def fresh():                                 # s=0, a=1, b=2, t=3
    res = [[0] * 4 for _ in range(4)]
    for u, v, c in [(0, 1, 1000), (0, 2, 1000), (1, 2, 1), (1, 3, 1000), (2, 3, 1000)]:
        res[u][v] = c
    return res


res, flow, rounds = fresh(), 0, 0
while True:                                  # always through the capacity-1 edge
    got = push(res, [0, 1, 2, 3]) or push(res, [0, 2, 1, 3])
    if not got:
        break
    flow += got; rounds += 1
print("unlucky path choice:", flow, "units in", rounds, "augmentations")

res, flow, rounds = fresh(), 0, 0
for p in ([0, 1, 3], [0, 2, 3]):             # the two shortest paths, as BFS finds them
    flow += push(res, p); rounds += 1
print("shortest paths     :", flow, "units in", rounds, "augmentations")
assert flow == 2000 and rounds == 2
```

## What to memorise

The template, which should come out of your fingers:

```python
to, cap, adj = [], [], [[] for _ in range(n)]

def add(u, v, c):                 # reverse arc is always at index ^ 1
    adj[u].append(len(to)); to.append(v); cap.append(c)
    adj[v].append(len(to)); to.append(u); cap.append(0)

# loop: BFS in the residual (cap[e] > 0), find the bottleneck, then
#       cap[e] -= push; cap[e ^ 1] += push   along the path
```

The sentence that turns a problem into it: *"Am I choosing a largest set of
things that compete for shared, capacity-limited resources — with compatibility
given as a list rather than a rule?"* If the compatibility is a rule (a
threshold, an interval, a prefix), look for a greedy first.

The habit: **always extract the cut.** Re-run the last BFS, sum the capacities
leaving the reachable set, assert it equals the flow. Four lines, and it catches
a missing reverse arc immediately.

The numbers: Edmonds-Karp `O(VE²)` with no assumption about capacities;
Ford-Fulkerson `O(E · f*)`, pseudo-polynomial; matching by augmenting paths
`O(VE)`, Hopcroft-Karp `O(E√V)`, Dinic `O(V²E)`. In a bipartite graph, maximum
matching = minimum vertex cover = `n −` maximum independent set; minimum path
cover of a DAG is `n −` maximum matching.

## Check yourself

:::check
Pushing flow "backwards" along an edge looks like cheating — water does not run
uphill. Why is the result still a legal flow, and what does the backward push
mean in the original network?
--
Because the update is on the *net* flow. Sending `Δ` along a backward arc
`v → u` means `f(u, v) := f(u, v) − Δ` with `Δ <= f(u, v)`, since that is the arc's
residual capacity, so the result stays inside `[0, c(u, v)]`; conservation holds
at `u` and `v` because each is an internal vertex of the path with one in-arc and
one out-arc.

Nothing runs uphill in the original network. The final flow is a different
routing: water that used to travel `u → v` leaves `u` by another exit, and `v`
gets the same total from a different supplier. "`A` gives up `X` and takes `Y`"
is that sentence in miniature.
:::

:::check
Someone says: "Edmonds-Karp is polynomial, and it is Ford-Fulkerson with BFS
instead of DFS. So Ford-Fulkerson is polynomial too — the search order cannot
change the complexity class." Where are they wrong?
--
In assuming the number of *iterations* is a property of the graph rather than of
the path choice. Ford-Fulkerson's bound is `O(E · f*)`: one unit per round in the
worst case, and `f*` can be as large as the capacities. Capacities are written in
binary, so five edges carrying `10⁹` make a two-dozen-character input that forces
a billion rounds — polynomial in the *values*, exponential in the input *length*.

BFS changes the accounting. The argument in *What it costs* never mentions a
capacity: residual distances never decrease, each arc is the bottleneck at most
`V/2` times, so there are `O(VE)` rounds whatever the numbers are. Same loop,
different theorem — and the third code block runs the same network in 2 rounds or
2000, depending only on the path chosen.
:::

:::check
A colleague computes a max flow and reports the minimum cut as "the set of
saturated edges". Give a concrete counterexample from this chapter and state the
correct rule.
--
Use the network in the implementation block: `s→a` 3, `s→b` 2, `a→b` 5,
`a→t` 1, `b→t` 3. The maximum flow is 4, routed as one unit `s→a→t`, one unit
`s→a→b→t` and two units `s→b→t`. That saturates `s→b`, `a→t` and `b→t` — three
edges of total capacity 6. Removing all three does disconnect `s` from `t`, but
it is not minimal: `{a→t, b→t}` costs 4 and disconnects them too.

The rule: let `S` be the vertices reachable from `s` in the *residual* graph
after the algorithm stops; the minimum cut is the edges from `S` to its
complement. Every such edge is saturated, but not every saturated edge crosses —
`s→b` is saturated with both ends inside `S`.
:::

:::check
In the worked example the maximum matching is 2 and the vertex cover `{A, X}`
also has size 2. Why must minimum vertex cover always equal maximum matching in
a bipartite graph — and why does the argument break on a triangle?
--
One direction holds in any graph: a matching's edges are pairwise disjoint, so a
cover needs a distinct vertex for each, giving `cover >= matching`.

The other direction is the min cut. Build the network with unit capacities on the
outer edges and infinite capacity on the middle ones. A finite cut can contain no
middle edge, so it is a set of `s → u` and `v → t` edges whose vertices must
touch every edge — otherwise an uncut path `s → u → v → t` survives. Finite cuts
and vertex covers are therefore the same objects of the same size, so min cut =
min cover; and since max flow = min cut = max matching, `matching = cover`.

On a triangle there is no two-sided arrangement and so no network to build — and
the conclusion is false: matching 1, cover 2. Every odd cycle breaks it, which is
exactly what non-bipartite means ([[bipartite]]).
:::

:::check
A scheduling problem says each of `m` technicians may take at most 3 jobs, and
each job needs one technician from a listed compatible set. You build the usual
matching network and get an answer that assigns five jobs to one technician.
What did you leave out, and what is the fix?
--
The model never contained the constraint. Conservation limits what passes
*through* a vertex only via its edges' capacities, and in the matching network
each technician has one incoming edge of capacity 1 — which encodes "at most one
job", not "at most three".

The fix is one number: raise `s → technician` from 1 to 3. Generally, when a
limit sits on a *vertex*, split it into `v_in → v_out` carrying that capacity,
with all incoming edges at `v_in` and all outgoing edges from `v_out`; in the
matching network `s → technician` already is that split edge, which is why the
one-line change works.

This also stops being a matching and becomes a general flow — and the
integrality theorem is what still assigns whole jobs to whole people.
:::
