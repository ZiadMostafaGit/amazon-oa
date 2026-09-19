# Modelling a Problem as a Graph

> Modelling is the part of a graph problem you do before you know it is a graph
> problem: deciding what counts as a place you can be, and what counts as a step.

## When you reach for it

Ninety-one problems in this bank are solved by modelling — rank #38 of 150 — and
the striking thing about the list is how few of them contain the word *graph*.
There are spreadsheets, package managers, chess horses, dice, currency
conversions, linked lists, agent schedulers and a mouse looking for cheese. The
graph is never in the input. It is something you decide to see.

So the trigger is not a shape in the data, it is a shape in the **question**.
Graph algorithms answer a small, fixed set of questions, and if the problem asks
one of them, modelling is the move:

- *Can this happen at all?* — reachability. *Binary Matrix Top-to-Bottom
  Reachability*, *Xiangqi Horse Reachability*, *Repeated-Roll Teleporter
  Reachability*.
- *What is the fewest number of steps?* — [[bfs]] on unit-cost edges. *Minimum
  Clicks Between Wiki Pages*, *Find Minimum City Hops*, *Nearest Reachable Grid
  Corner*.
- *What is the cheapest route?* — [[dijkstra]], or [[bellman-ford]] if costs can
  be negative. *Minimum-Cost Path Through a Weighted Grid*, *Minimize Commute*.
- *In what order may these be done?* — [[topological-sort]] on a DAG. *Package
  Dependency Order*, *Compilation Order with Topological Sort*, *Microservice
  Deployment Order*.
- *Which of these belong together?* — components, [[union-find]] or
  [[flood-fill]]. *Record Linkage Part 3 - Full Connected Component*, *Minimum
  Edges to Connect All Components*.
- *Is there a contradiction?* — a cycle. *Evaluate Formulas with Cycle
  Detection*, *Resolve Variable Equations with Dependency Errors*.

If you are asking one of those six questions about things that relate in pairs,
you have a graph, whether or not anybody drew one.

The tool is wrong in three situations, each with a near-miss look.

**The question is about a set, not a walk.** "Choose a subset maximising value
under a weight limit" is not reachability; the implied graph is exponential and
the structure that matters is overlapping subproblems, so it is
[[dynamic-programming]]. The dividing line is whether the answer describes a
*route through* the data or a *selection from* it.

**The relation is not between two things.** "A task becomes ready when *all* of
its prerequisites are done" constrains a whole set of predecessors at once. You
can still draw the edges, but plain traversal gets it wrong — see the AND/OR
distinction in Traps.

**There is nothing to model.** *Reachable Nodes in a Directed Graph* hands you an
adjacency list and asks which vertices are reachable: read [[graphs]] and [[dfs]]
and you are finished. This chapter is about the other case, where the adjacency
list does not exist and never will.

## The idea

**A graph is a function from a state to its successors. Everything else is
bookkeeping.**

That is the whole insight, and it has a practical form. Before writing any code,
answer three questions in one sentence each:

1. **What is a node?** The complete description of "where you are" — complete
   meaning: everything a future move might depend on.
2. **When is there an edge?** The rule that turns one node into its successors.
3. **What graph question is being asked?** One of the six above.

Answer those and the algorithm is somebody else's problem; you call BFS and go
home. Get question 1 wrong and no algorithm will save you.

The reason question 1 is the hard one is that a node is a *deliberate loss of
information*. When you say "the node is the square the horse stands on", you are
declaring that two games which arrived at that square by different routes are the
same thing and may be treated interchangeably. That declaration is what makes the
search finite: the horse has infinitely many move sequences and only ninety
squares. It is also, when it is false, the source of every wrong answer in this
chapter.

<svg viewBox="0 0 640 215" role="img" aria-label="two different histories arriving at the same node, which then fans out to the same successors">
  <g>
    <circle cx="60" cy="105" r="18"/>
    <text x="60" y="111" text-anchor="middle">s</text>
    <circle cx="175" cy="50" r="18"/>
    <text x="175" y="56" text-anchor="middle">a</text>
    <circle cx="175" cy="160" r="18"/>
    <text x="175" y="166" text-anchor="middle">b</text>
    <circle class="fill" cx="310" cy="105" r="18"/>
    <text x="310" y="111" text-anchor="middle">x</text>
    <circle cx="450" cy="50" r="18"/>
    <text x="450" y="56" text-anchor="middle">y</text>
    <circle cx="450" cy="160" r="18"/>
    <text x="450" y="166" text-anchor="middle">z</text>
    <line x1="76" y1="96" x2="158" y2="60"/>
    <line x1="76" y1="114" x2="158" y2="150"/>
    <line x1="192" y1="60" x2="294" y2="95"/>
    <line x1="192" y1="150" x2="294" y2="115"/>
    <line x1="327" y1="95" x2="433" y2="60"/>
    <line x1="327" y1="115" x2="433" y2="150"/>
    <text x="175" y="25" text-anchor="middle">one history</text>
    <text x="175" y="197" text-anchor="middle">another history</text>
    <text x="310" y="150" text-anchor="middle">one node</text>
    <text x="520" y="105">same options</text>
    <text x="20" y="211">the collapse is legal only if the future cannot tell the two histories apart</text>
  </g>
</svg>

Once the node is chosen, notice what you do *not* have to do: build the graph.
Nothing in BFS needs an adjacency list; it needs a queue, a visited set, and the
ability to ask a node for its neighbours. If that ability is a two-line function,
the graph is implicit and costs no memory at all. *Count Reachable Values by
Halving and Decrementing* has up to 10⁹ as its start value; nobody is allocating
an array of a billion vertices, and nobody needs to.

## Worked by hand

Take *Count Reachable Values by Halving and Decrementing* with `num = 6` and
`steps = 3`. From any value you may halve it if it is even, or subtract one if it
is positive. How many distinct nonnegative values can appear, using at most three
operations?

The model: **a node is a value**; there is an edge `v → v/2` when `v` is even and
positive, and an edge `v → v - 1` when `v` is positive; the question is "which
nodes are within distance 3 of node 6", which is BFS stopped after three layers.

Run it. `frontier` is the set discovered at exactly that distance; `seen` is
everything discovered so far.

| layer | frontier | expansions | new | `seen` after |
| --- | --- | --- | --- | --- |
| 0 | {6} | — | — | {6} |
| 1 | {3, 5} | 6 → 3 (halve), 6 → 5 (minus) | 3, 5 | {3, 5, 6} |
| 2 | {2, 4} | 3 → 2; 5 → 4 | 2, 4 | {2, 3, 4, 5, 6} |
| 3 | {1} | 2 → 1, 2 → 1; 4 → 2 *seen*, 4 → 3 *seen* | 1 | {1, 2, 3, 4, 5, 6} |

Six distinct values. Three things in that table are worth a slow second look.

**Layer 3 did almost nothing.** Four expansions produced one new value: two
collided with values already found, and the two edges out of 2 both landed on 1,
since halving 2 and decrementing 2 agree. Those collisions are the entire reason
the problem is tractable. Push the trace to the real constraints — `num = 10⁹`,
`steps = 60` — and there are up to 2⁶⁰ operation sequences, about 10¹⁸, while the
runnable block below counts the distinct values at 1191. Enumerating sequences is
impossible; enumerating states is instant. The model is the optimisation.

**The layers are the answer to "at most `steps`".** Because every operation costs
exactly one step, the layer a value first appears in is the *minimum* number of
operations that reaches it, so "reachable within `steps`" is "appears in layers 0
through `steps`" and cutting the expansion off at the limit is correct rather than
a heuristic. If halving cost two steps and decrementing one, this would collapse
and you would need [[dijkstra]] — for a reason that has nothing to do with the
problem sounding like a shortest-path question.

**The graph was never built.** No vertex list, no edge list, no adjacency array.
At `num = 10⁹` the vertices are integers up to a billion; we touched 1191.

<svg viewBox="0 0 640 200" role="img" aria-label="BFS layers from 6 under halving and decrementing, showing two edges from 2 landing on the same value">
  <g>
    <text x="45" y="25" text-anchor="middle">layer 0</text>
    <text x="195" y="25" text-anchor="middle">layer 1</text>
    <text x="345" y="25" text-anchor="middle">layer 2</text>
    <text x="495" y="25" text-anchor="middle">layer 3</text>
    <circle class="fill" cx="45" cy="105" r="18"/>
    <text x="45" y="111" text-anchor="middle">6</text>
    <circle cx="195" cy="60" r="18"/>
    <text x="195" y="66" text-anchor="middle">3</text>
    <circle cx="195" cy="150" r="18"/>
    <text x="195" y="156" text-anchor="middle">5</text>
    <circle cx="345" cy="60" r="18"/>
    <text x="345" y="66" text-anchor="middle">2</text>
    <circle cx="345" cy="150" r="18"/>
    <text x="345" y="156" text-anchor="middle">4</text>
    <circle class="fill" cx="495" cy="105" r="18"/>
    <text x="495" y="111" text-anchor="middle">1</text>
    <line x1="62" y1="96" x2="178" y2="70"/>
    <line x1="62" y1="114" x2="178" y2="140"/>
    <line x1="212" y1="60" x2="328" y2="60"/>
    <line x1="212" y1="150" x2="328" y2="150"/>
    <line x1="362" y1="68" x2="479" y2="98"/>
    <line x1="361" y1="70" x2="478" y2="100"/>
    <line x1="332" y1="132" x2="346" y2="80"/>
    <line x1="329" y1="141" x2="212" y2="70"/>
    <text x="418" y="72">both edges from 2</text>
    <text x="300" y="192">the dashed-looking pair back into layer 2 are edges that found nothing new</text>
  </g>
</svg>

## Why it is correct

An algorithm is correct against a specification. A *model* is correct against the
problem, and that is a different kind of claim: it says the graph you invented and
the world the statement describes have the same answers. Here is the theorem that
makes it precise, and it is the only theorem in this chapter.

:::proof A model is correct when it is a congruence
**Setup.** The statement defines a set of configurations `C` (full, honest
descriptions of the world: the horse's square *and* every obstacle *and* whatever
else exists), a start configuration `c₀`, a transition relation `→` on `C`
(one legal move), and a goal set `G ⊆ C`. The question is whether some `g ∈ G` is
reachable from `c₀`, and in how few transitions.

Your model is a function `f : C → V` mapping each configuration to a node. Build
the graph `Γ = (V, E)` with `(u, v) ∈ E` exactly when there exist configurations
`c, c'` with `f(c) = u`, `f(c') = v` and `c → c'`.

**The two conditions.**

- **(A) Congruence.** If `f(c) = f(d)` and `c → c'`, then there is a `d'` with
  `d → d'` and `f(d') = f(c')`. In words: configurations you called the same node
  must offer the same moves, up to `f`.
- **(B) Observability.** `G` is a union of fibres of `f`: if `f(c) = f(d)` then
  `c ∈ G` iff `d ∈ G`. In words: the node alone must decide whether you have won.

**Claim 1 (no lost paths).** Every legal run maps to a walk. Induction on the run
length `k`. For `k = 0` the walk is the single node `f(c₀)`. For the step, assume
`c₀ → … → c_k` maps to a walk ending at `f(c_k)`; if `c_k → c_{k+1}` then by the
definition of `E` the pair `(f(c_k), f(c_{k+1}))` is an edge, so appending it
extends the walk. Hence `dist_Γ(f(c₀), f(c_k)) ≤ k`. No transition can vanish,
and the graph never reports "unreachable" for something the world can do.

**Claim 2 (no phantom paths).** Every walk lifts to a legal run — and this is
where (A) earns its keep. Claim: for every walk `v₀ → v₁ → … → v_k` in `Γ` and
every configuration `d₀` with `f(d₀) = v₀`, there is a run
`d₀ → d₁ → … → d_k` with `f(d_i) = v_i`. Induction on `k`. For `k = 0`, take the
empty run. For the step, suppose `d₀ … d_{k-1}` has been built with
`f(d_{k-1}) = v_{k-1}`. The edge `(v_{k-1}, v_k)` exists, so by the definition of
`E` there are configurations `c, c'` with `f(c) = v_{k-1}`, `c → c'` and
`f(c') = v_k`. Now `f(d_{k-1}) = v_{k-1} = f(c)`, so (A) applies to the
transition `c → c'` and gives a `d_k` with `d_{k-1} → d_k` and
`f(d_k) = f(c') = v_k`. The run extends. Hence `dist_C(c₀, G) ≤ dist_Γ(f(c₀), f(G))`.

**Conclusion.** Combining the two claims, `dist_C(c₀, G) = dist_Γ(f(c₀), f(G))`,
where both are `∞` together. By (B), `f(G)` is a well-defined set of nodes that a
search can test for, so running BFS on `Γ` from `f(c₀)` and stopping at the first
node in `f(G)` answers the original question exactly — both the yes/no and the
minimum number of moves. Termination of the search additionally requires the set
of nodes reachable from `f(c₀)` to be finite. ∎
:::

Now say plainly what that proof leaned on, because the assumptions are where the
bugs live.

- **The node records everything a move depends on (A).** A horse whose legal moves
  depend on which squares are blocked is fine — the obstacles never change, so they
  can live outside the node. A traveller with a fuel tank is not: two visits to the
  same city with different fuel offer different moves, so fuel belongs *in* the
  node.
- **The node records everything the goal depends on (B).** "Reach the exit carrying
  all three keys" is not a question about the exit cell.
- **Every edge costs the same.** BFS layers equal minimum move counts only under
  unit cost. The proof says nothing about *weighted* distance unless the weights
  come along in the edge definition.
- **The reachable node set is finite.** The horse has 90 squares; the halving graph
  has ≤ 10⁹ nodes but only 1191 reachable in 60 layers. If both the state space and
  the depth are unbounded, you have a model, not an algorithm.
- **Nothing outside the node changes.** The moment a transition mutates something
  you left out of the node, (A) is false. This is the commonest failure of all, and
  it is invisible in small tests.

Those two failure directions have names worth keeping. A model that loses paths
is **too pessimistic** — it answers "impossible" or reports a distance that is too
large. A model that invents paths is **too optimistic** — it returns a route the
rules forbid. Both are shown running side by side in Traps.

## What it costs

BFS and DFS cost `Θ(|V| + |E|)`. That is not the interesting part, because in a
modelled graph `|V|` and `|E|` are not given to you — you chose them, when you
chose the node.

Let the node be a tuple of `k` coordinates with sizes `n₁, n₂, …, n_k`, and let
every node have at most `b` successors. Then

    |V| = n₁ · n₂ · … · n_k        |E| ≤ b · |V|

and the search costs `Θ(b · n₁ · n₂ · … · n_k)`. Two consequences follow
immediately and neither is obvious from "BFS is linear".

**Every coordinate multiplies.** A 500 × 500 grid is 250,000 nodes and, at four
neighbours each, a million edges — comfortable. Add "how many walls you have
broken, up to 1" and it is 500,000 nodes; add "which of 5 keys you hold" and it is
250,000 · 2⁵ = 8 million, still fine; add "how many of 60 steps you have used" and
it is 15 million and you are in trouble. That budget is computable before you write
a line ([[state-design]] is the chapter on spending it).

**The branching factor is a multiplier, not an exponent.** A depth-`d` search
without deduplication explores `b^d` sequences. With a visited set every node is
expanded at most once, so the work is `b · |V|` regardless of `d`. In the halving
problem that is `2⁶⁰ ≈ 10¹⁸` sequences against 1191 states. The visited set is not
an optimisation; it is the algorithm.

**Which side to precompute.** *Directed Graph Reachability Queries* gives `n ≤ 500`
vertices, up to 10⁵ edges and up to 10⁵ queries. One BFS per query costs
`10⁵ · (500 + 10⁵) ≈ 10¹⁰` — hopeless. One BFS per *source vertex* costs
`500 · (500 + 10⁵) ≈ 5 · 10⁷`, fills a 500 × 500 reachability table and answers
each query in `O(1)`. The model did not change; only the decision about what to
enumerate. When queries outnumber vertices, enumerate vertices.

Two costs people forget. **Interning**: adjacency arrays and visited bitsets want
integer nodes, and statements hand you strings — *Service Dependency Load Factors*
names services, *Spreadsheet Formula Dependencies* names cells — so every lookup is
a hash ([[hash-tables]]), and on string-heavy inputs that dominates the traversal.
**Hashing the node itself**: a visited `set` of `(r, c, b)` tuples hashes a tuple
per edge, where encoding the node as `(r * C + c) * 2 + b` and indexing a list of
booleans costs one line and is routinely several times faster.

## The implementation

There is no "graph modelling algorithm". There is one traversal, written once,
and a different `neighbours` function per problem. Here it is driving two of the
models named above — and note that the second one, the Xiangqi horse, has a move
rule nobody would describe as a graph.

```python run
from collections import deque

JUMPS = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
ROWS, COLS = 10, 9


def explore(starts, neighbours, limit=None):
    """Every node reachable from `starts`, with its distance in moves.
    The graph IS the function `neighbours`; no edge is ever stored."""
    dist = {s: 0 for s in starts}
    q = deque(starts)
    while q:
        u = q.popleft()
        if limit is not None and dist[u] == limit:
            continue
        for v in neighbours(u):
            if v not in dist:                 # mark on push, never on pop
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def value_moves(v):                           # node = the current value
    if v > 0 and v % 2 == 0:
        yield v // 2
    if v > 0:
        yield v - 1


def horse_moves(obstacles):                   # node = a square, as r*COLS + c
    def moves(sq):
        r, c = divmod(sq, COLS)
        for dr, dc in JUMPS:
            leg = (r + dr // 2, c) if abs(dr) == 2 else (r, c + dc // 2)
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if leg not in obstacles and (nr, nc) not in obstacles:
                    yield nr * COLS + nc
    return moves


reach = explore([6], value_moves, limit=3)
print("num=6, steps=3 ->", sorted(reach), "=", len(reach), "distinct values")
assert sorted(reach) == [1, 2, 3, 4, 5, 6]

big = explore([10 ** 9], value_moves, limit=60)
print("num=10**9, steps=60 ->", len(big), "distinct values, from up to 2**60 sequences")
assert len(big) == 1191

free = explore([0], horse_moves(set()))
print("horse from (0,0), empty board ->", len(free), "squares, farthest =", max(free.values()))
assert len(free) == ROWS * COLS

trapped = explore([0], horse_moves({(1, 0), (0, 1)}))
print("horse from (0,0), legs (1,0) and (0,1) blocked ->", len(trapped), "square")
assert trapped == {0: 0}
print("one traversal, two graphs, neither of them built")
```

Three lines carry the weight.

`for v in neighbours(u)` is the entire abstraction. `explore` does not know whether
it is walking a dependency DAG, a chessboard or the integers; it knows how to ask.
The consequence is that the only thing you can get wrong on a new problem is the
model, which is exactly where you want the risk concentrated.

`if v not in dist` marks a node **when it is pushed**, not when it is popped.
Marking on pop lets the same node enter the queue once per incoming edge, and on a
dense graph the queue grows to `O(E)`. Setting `dist[v] = dist[u] + 1` on the same
line makes the first arrival the shortest, which is valid only because every edge
costs 1.

`leg = (r + dr // 2, c) if abs(dr) == 2 else (r, c + dc // 2)` is the model. The
Xiangqi horse is blocked by a piece on the square it *passes through*, not the one
it lands on, so the test for "is there an edge" reads a cell that is neither
endpoint. The trapped case asserts exactly this: blocking `(1, 0)` and `(0, 1)`,
which are not destinations of any move, immobilises the horse completely. A model
that checked only destinations would report it roaming free.

## Variants you will meet

The catalogue below is the real content of this topic: a small number of modelling
moves that recur endlessly.

**The graph is given.** Pairs of ids, an adjacency list, a matrix. Build it and
traverse it — [[graphs]] for representation, [[dfs]] and [[bfs]] for the walk.

**The graph is a rule.** No edge list exists; `neighbours` is a function. *Xiangqi
Horse Reachability*, *Repeated-Roll Teleporter Reachability* (from square `s` you
may go to `s + d` for each die face `d`, then follow one teleporter without
chaining), *Knight Dialer Sequences*, *Count Reachable Values by Halving and
Decrementing*.

**The grid is the graph.** Cell = node, four or eight neighbours = edges, blocked
cells simply have no edges. *Binary Matrix Top-to-Bottom Reachability*, *Nearest
Reachable Grid Corner*, *Grid Pathfinding with Obstacles (DFS)*. See [[grid-bfs]].

**State augmentation — the product graph.** Node = position × everything else that
changes: fuel, keys held, walls broken, moves used mod `k`, whose turn it is. The
node set is the Cartesian product, which is why "everything else" must be small.
This is the move that rescues most "but it depends on what I did earlier" problems;
[[state-design]] is the chapter on doing it well.

<svg viewBox="0 0 640 240" role="img" aria-label="a product graph drawn as two copies of the same line of cells, one per number of walls broken, with a one-way edge between the layers">
  <g>
    <text x="35" y="70">b = 0</text>
    <text x="35" y="185">b = 1</text>
    <circle cx="160" cy="65" r="17"/>
    <text x="160" y="71" text-anchor="middle">A</text>
    <circle cx="280" cy="65" r="17"/>
    <text x="280" y="71" text-anchor="middle">B</text>
    <circle cx="400" cy="65" r="17"/>
    <text x="400" y="71" text-anchor="middle">C</text>
    <circle cx="520" cy="65" r="17"/>
    <text x="520" y="71" text-anchor="middle">D</text>
    <circle cx="160" cy="180" r="17"/>
    <text x="160" y="186" text-anchor="middle">A</text>
    <circle cx="280" cy="180" r="17"/>
    <text x="280" y="186" text-anchor="middle">B</text>
    <circle cx="400" cy="180" r="17"/>
    <text x="400" y="186" text-anchor="middle">C</text>
    <circle class="fill" cx="520" cy="180" r="17"/>
    <text x="520" y="186" text-anchor="middle">D</text>
    <line x1="177" y1="65" x2="263" y2="65"/>
    <line x1="297" y1="65" x2="383" y2="65"/>
    <line x1="177" y1="180" x2="263" y2="180"/>
    <line x1="297" y1="180" x2="383" y2="180"/>
    <line x1="417" y1="180" x2="503" y2="180"/>
    <line x1="414" y1="80" x2="508" y2="166"/>
    <line x1="508" y1="166" x2="494" y2="164"/>
    <line x1="508" y1="166" x2="503" y2="152"/>
    <line x1="460" y1="40" x2="460" y2="92"/>
    <text x="460" y="30" text-anchor="middle">wall</text>
    <text x="560" y="120">break it</text>
    <text x="20" y="228">two floors, one staircase, and it only goes down</text>
  </g>
</svg>

**Super source and super sink.** Many possible starts become one virtual node with
zero-cost edges to all of them, and the search runs once instead of once per start.
*Closest DashMart*, *Distance to the Nearest Supply Point* and *Minimum-Cost
Meeting City* are this; see [[multi-source-bfs]].

**Reverse the edges.** "Which nodes can reach me" is "which nodes can I reach" on
the transpose. Cheap, and it turns a per-target search into one search. It is also
how a parent array becomes a tree — *Validate a Tree From Its Parent Array*.

**A tree is a graph once you add parent pointers.** *Binary Tree Nodes at Distance
K* is unsolvable while you think of a tree as pointing downwards, and trivial the
moment you walk it once to record parents and then run BFS on the undirected
version. The model change is the whole solution.

**A linked list is a graph with out-degree one.** *Find the Intersection Node of
Two Linked Lists* is "where do two paths in a functional graph merge"; *Linked List
Cycle Entry Node* and *Detect and Break a Linked-List Cycle* are the cycle question
on the same graph ([[cycle-detection]]).

**Constraints become edges.** "`u` before `v`" is a directed edge and the question
is [[topological-sort]]. "`a` equals `b`" is an undirected edge and the question is
components ([[union-find]]). "`a` differs from `b`" is an edge and the question is
2-colouring ([[bipartite]]). Read the constraint, write the arrow.

**Transform the weight.** Multiplicative costs become additive under a logarithm,
so "the best conversion rate" becomes a shortest path and "a profitable cycle"
becomes a negative cycle — *Maximum Currency Conversion with Arbitrage* is
[[bellman-ford]] wearing a hat.

**Dependency DAG plus an aggregation.** Once the edges are in place, the
topological order lets you compute anything that flows along edges in one sweep:
earliest finish time (*Minimum Completion Time for DAG Dependencies*), a formula's
value (*Spreadsheet Formula Evaluator*), or a count of paths. The last one is
*Service Dependency Load Factors*, below, and it shows the one subtlety: the sweep
must run on the **reachable** subgraph, not the whole graph.

```python run
from collections import deque


def loads(names, deps, entry):
    """One unit of load enters `entry`; every service passes each unit it gets
    to each of its dependencies. Report the load of every reachable service."""
    out = [[] for _ in names]
    for u, v in deps:
        out[u].append(v)

    seen, stack = {entry}, [entry]               # 1. keep only what entry reaches
    while stack:
        u = stack.pop()
        for v in out[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)

    indeg = {u: 0 for u in seen}                 # 2. indegree INSIDE that subgraph
    for u in seen:
        for v in out[u]:
            indeg[v] += 1

    load = {u: 0 for u in seen}
    load[entry] = 1
    q = deque(u for u in seen if indeg[u] == 0)
    done = 0
    while q:                                     # 3. one topological sweep
        u = q.popleft()
        done += 1
        for v in out[u]:
            load[v] += load[u]
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    assert done == len(seen), "the reachable subgraph must be acyclic"
    return sorted("%s %d" % (names[u], load[u]) for u in seen)


names = ["api", "auth", "cache", "db", "batch"]
deps = [(0, 1), (0, 2), (1, 3), (2, 3), (4, 0)]   # a diamond, plus batch -> api
print("loads from api  :", loads(names, deps, 0))
assert loads(names, deps, 0) == ["api 1", "auth 1", "cache 1", "db 2"]

glob = [0] * len(names)                           # what a GLOBAL indegree would say
for _, v in deps:
    glob[v] += 1
print("global indegrees:", dict(zip(names, glob)))
print("global ready set:", [names[u] for u in range(len(names)) if glob[u] == 0],
      "- the sweep would start at batch and api would never be ready")
assert glob[0] == 1
print("db carries 2 because two distinct paths deliver a unit into it")
```

Restricting to the reachable set is not tidiness. Within it, `entry` is the unique
source — any other reachable node has an in-edge from a reachable node, and `entry`
itself cannot have one without a cycle — so the ready queue starts as exactly
`{entry}`, which is what makes `load[entry] = 1` the right initial condition.
Globally, `api` has an incoming edge from the unreachable `batch`, its indegree
never falls to zero on its own, and the sweep begins in the wrong place with the
wrong numbers.

## Recognising it in a statement

Ordered by how much to trust them.

1. **An operational move rule.** "You may replace the value with half of itself",
   "the horse travels two cells along one axis and one along the other", "after
   each roll, if the landing square is a teleporter source, move once to its
   destination". A statement that describes what you may *do* rather than what you
   *have* is handing you the `neighbours` function verbatim.
2. **"Reachable", "can you get to", "is there a way".** The word *reachable* is in
   six titles in this bank. It means: node, edge, BFS or DFS, done.
3. **"Depends on", "prerequisite", "must finish before", "blocked by".** A DAG and
   [[topological-sort]]. If the statement also says a cycle is possible and asks
   you to report it, cycle detection is half the answer — *Resolve Variable
   Equations with Dependency Errors* returns `["Cyclic Dependency"]`.
4. **A list of pairs.** `[[u, v], …]` is an edge list. The only question left is
   whether it is directed, which the wording of one sentence decides.
5. **"Minimum number of steps / moves / clicks / hops"** with every step costing
   the same. BFS. If the steps have different costs, the same model with
   [[dijkstra]].
6. **A small bound on an odd extra quantity.** "at most one wall", "up to 5 keys",
   "at most `k` refuels". Small bounds on something that is not position are an
   invitation to put it in the node; the bound is there so the product stays small.
7. **"Transitive", "indirectly", "eventually".** Closure of a relation — traversal,
   or [[union-find]] if the relation is symmetric.

The anti-signals:

- **The answer is a chosen subset, not a route.** *Positive Subset Sum* and
  *Tree-Dependent Knapsack* have graph-shaped inputs and DP-shaped questions.
- **Weights on the edges and a plain BFS queue.** The model may be right while the
  algorithm is wrong; see [[shortest-path]] for the map of which one to use.
- **"All of" rather than "any of".** Explained next, because it is a trap more
  than a signal.
- **The graph is already built.** No modelling to do; go straight to the traversal.

## Traps

**The node is too small.** The defining bug of this topic. Symptom: the answer is
too pessimistic on some inputs and correct on most, so it passes the samples. Demo
below.

**The node is too big.** Adding a coordinate the transitions never read is not
wrong, just expensive — every extra coordinate multiplies `|V|`. Symptom: a correct
solution that times out, which is a much nicer bug to have than the previous one.

**AND semantics treated as OR.** Reachability is an OR: one incoming edge is
enough. Dependency readiness is an AND: *every* predecessor must be done. Run BFS
from the set of tasks with no prerequisites and you will happily mark a task ready
the moment one of its three prerequisites finishes. The fix is indegree counting —
[[topological-sort]] — where a node is enqueued only when its counter hits zero.
*Agent Task Dependency Tracker* is the clearest illustration because it needs both
closures on the same graph: a BLOCKED task becomes READY only when *all* its
dependencies have SUCCEEDED (AND), but a FAILED task fails everything that depends
on it *directly or indirectly* (OR, a plain forward traversal).

**Edge direction, chosen by coin flip.** The conventions genuinely differ between
problems: *Package Dependency Order* gives pairs `[package, dependency]`, while
*Lexicographically Smallest Dependency Order* gives `[before, after]`. These are
opposite. Symptom: a perfectly valid topological order of the reversed graph, which
is the exact reverse of the answer — and which passes any test whose dependency
chain happens to be symmetric. Read the sentence, not the variable names, and write
one comment saying which way your arrows point.

**Marking visited on pop.** Symptom: correct answers, memory blowup, and a
mysterious timeout on dense graphs. Mark on push.

**Recursive DFS on a deep model.** Python's default limit is about 1000 frames.
*Reachable Nodes in a Directed Graph* allows 100,000 vertices and warns in its own
follow-up about "thousands of vertices in a long chain". Symptom: `RecursionError`
on exactly one hidden test. Write the explicit stack ([[recursion]]).

**Forgetting the nodes with no edges.** Build the node set from `n`, not from the
edge list. Symptom: components miscounted on sparse inputs.

**Working on the whole graph when the question is about part of it.** *Service
Dependency Load Factors* says to omit unreachable services and that their
dependencies contribute nothing; *Package Dependency Order* asks only for the
target and its transitive dependencies. Restrict first, then sweep.

The first trap, demonstrated. Four models of the same problem — a grid where you
may break at most one wall — run through one BFS. Only the last is right.

```python run
from collections import deque


def walk(grid, target, cap, key):
    """Fewest steps to `target`, allowed to break at most `cap` walls.
    `key(r, c, b)` decides WHAT COUNTS AS THE SAME NODE - that is the model."""
    R, C = len(grid), len(grid[0])
    seen, q = {key(0, 0, 0)}, deque([(0, 0, 0, 0)])
    while q:
        r, c, b, d = q.popleft()
        if (r, c) == target:
            return d
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if not (0 <= nr < R and 0 <= nc < C):
                continue
            nb = b + (grid[nr][nc] == "#")
            if nb > cap:
                continue
            if key(nr, nc, nb) not in seen:
                seen.add(key(nr, nc, nb))
                q.append((nr, nc, nb, d + 1))
    return None


cell = lambda r, c, b: (r, c)              # the cell alone
full = lambda r, c, b: (r, c, b)           # the cell AND the budget already spent

grid = [".#..#.",
        "...###"]
target = (0, 5)

print("grid:", *grid, sep="\n  ")
print("no breaking allowed     node=(r,c)   cap=0 :", walk(grid, target, 0, cell))
print("walls ignored entirely  node=(r,c)   cap=99:", walk(grid, target, 99, cell))
print("budget kept, not in key node=(r,c)   cap=1 :", walk(grid, target, 1, cell))
print("budget in the key       node=(r,c,b) cap=1 :", walk(grid, target, 1, full))

assert walk(grid, target, 0, cell) is None       # lost path: too pessimistic
assert walk(grid, target, 99, cell) == 5         # phantom path: it broke two walls
assert walk(grid, target, 1, cell) is None       # lost path, and far subtler
assert walk(grid, target, 1, full) == 7          # the truth
print()
print("truth = 7: take the long way along row 1 to reach (0,2) with the break")
print("unspent, then spend it on the wall at (0,4).  node=(r,c) arrives at (0,2)")
print("two steps sooner having already spent it, marks the cell, and discards")
print("the only arrival that could have finished.")
```

The third line is the one to stare at. The budget *was* enforced — no run ever
breaks two walls — and the answer is still wrong, because enforcing a constraint
and recording it in the node are different things. Configuration "(0,2) with a
break left" and configuration "(0,2) with none left" offer different moves, so
condition (A) of the proof is violated, claim 2 fails, and a real path disappears.
The visited set is not a cache you may key however you like; it is the statement
`f(c) = f(d)`, and BFS believes you.

## What to memorise

Not code. Three questions, one habit, one number.

**The three questions**, asked in this order before anything is typed:

1. What is a node? (Say it as a noun phrase: "a square, plus how many walls I have
   broken".)
2. When is there an edge? (Say it as a sentence: "from `(r, c, b)` to each
   orthogonal neighbour, with `b` increased if that cell is a wall, provided
   `b ≤ 1`".)
3. Which of the six questions is being asked — reachable, fewest steps, cheapest,
   an order, which clump, is there a cycle?

**The template** that consumes those answers, which should need no thought:

```python
dist = {start: 0}
q = deque([start])
while q:
    u = q.popleft()
    for v in neighbours(u):
        if v not in dist:
            dist[v] = dist[u] + 1
            q.append(v)
```

**The habit**: after naming the node, say out loud — *"two configurations with the
same node have the same legal moves and the same answer."* If you cannot say it
honestly, something a move depends on is missing from the node, and no amount of
debugging the traversal will find it.

Numbers worth carrying: the cost is `b · |V|`, and `|V|` is the product of your
coordinates; a `k`-bit mask in the node multiplies the work by `2^k`; a 500 × 500
grid is 250k nodes and 1M edges, which is comfortable; deduplication turns `b^d`
sequences into `b · |V|` expansions, which is the whole reason any of this works.

## Check yourself

:::check
In the halving-and-decrementing trace, why is "reachable in at most `steps`
operations" exactly the same as "appears in BFS layers 0 through `steps`"? Which
property of the model is doing the work, and what would break it?
--
Because every operation is one edge and every edge costs one step, so the BFS
layer in which a value first appears is the *minimum* number of operations that
produces it. A value in layer `L` is reachable in `L ≤ steps` operations; a value
first appearing in layer `L > steps` cannot be produced in fewer, so it is out.

The property doing the work is **uniform edge cost**, which is what makes BFS
layers equal distances. If halving cost one step and decrementing cost two, the
first arrival would no longer be the cheapest and the frontier would be in the
wrong order; you would need [[dijkstra]], or a 0-1 deque, on exactly the same
graph. Notice that nothing about the *problem statement* changes — only the edge
weights — which is why the cost model is worth checking separately from the model.
:::

:::check
Someone says: "the horse may make any number of moves, so the set of possible move
sequences is infinite and a search can never finish." Where are they wrong?
--
They are confusing sequences with states. The set of move sequences is indeed
infinite; the set of *nodes* is 90, one per square of a 10 × 9 board. Since the
legal moves out of a square depend only on that square and the fixed obstacles —
condition (A) of the proof — a sequence that returns to a square it has already
visited can be truncated without changing what is reachable afterwards.

The visited set is what converts that observation into a terminating algorithm:
each node is expanded at most once, so the search does at most `90 · 8` work no
matter how long the paths are. The correct version of their worry is the finiteness
assumption in the proof — if the node had included, say, "number of moves made so
far", the node set really would be infinite and the search would not terminate.
:::

:::check
In the wall-breaking demo, the model `node = (r, c)` with a budget of one enforces
the budget correctly on every path it explores, and yet it reports "unreachable"
for a grid where a 7-step route exists. Explain the failure in terms of the two
claims in the proof, and say which claim fails.
--
Claim 2 (no phantom paths) is fine — every walk the search takes is a legal route,
because the budget check `nb > cap` is real. **Claim 1, no lost paths, fails**, and
it fails because condition (A) is violated.

The abstraction maps the configuration "at (0,2) with one break left" and the
configuration "at (0,2) with none left" to the same node. But those two
configurations do not offer the same moves: only the first can cross the wall at
(0,4). So `f` is not a congruence. BFS reaches the cell first along the shorter
route, which has already spent the break, marks the node, and when the longer,
break-preserving route arrives two steps later it is discarded as "already seen".
The winning run exists in the world and has no corresponding walk in the graph.

The fix is to stop lying: make the node `(r, c, b)`, so the two configurations are
two nodes, and the collapse becomes true.
:::

:::check
You are given task dependency pairs and must output a valid order. One statement
gives pairs as `[package, dependency]` and another as `[before, after]`. For each,
which way does your edge point if you intend to run indegree-counting
([[topological-sort]]), and what symptom tells you that you got it backwards?
--
The edge must point from the thing that comes first to the thing that waits, so
that a node's indegree counts the things it is still waiting for.

- `[before, after]` (*Lexicographically Smallest Dependency Order*): edge
  `before → after`, used as given.
- `[package, dependency]` (*Package Dependency Order*): the dependency comes
  first, so the edge is `dependency → package` — the pair reversed.

The symptom of getting it backwards is not a crash and not an empty result: you
get a perfectly valid topological order *of the reversed graph*, which is a
plausible-looking list in exactly the wrong order. It also survives any test whose
dependency chain is symmetric, which is why the mistake reaches production. Assert
on one asymmetric example — "b needs a" must put `a` first — before trusting it.
:::

:::check
A task becomes runnable when all of its prerequisites are done. Why can you not
compute the set of eventually-runnable tasks with a plain BFS from the tasks that
have no prerequisites, and what is the smallest change that makes it correct?
--
Because BFS computes an **OR**-closure: it marks a node the first time *any* edge
reaches it. Readiness is an **AND** over all incoming edges. With prerequisites
`{a, b, c}` for task `t`, a plain BFS marks `t` as soon as `a` is processed, and
everything downstream of `t` inherits the mistake.

The smallest change is to give each node a counter initialised to its indegree, and
to enqueue a node only when processing an incoming edge drives its counter to zero.
That is Kahn's algorithm, and it is BFS with one extra array.

Both closures are useful and can coexist on one graph: *Agent Task Dependency
Tracker* promotes BLOCKED to READY only when every dependency has SUCCEEDED (AND),
but propagates FAILED to everything that depends on the failed task directly or
indirectly (OR). Using the wrong one of the two is not a small error — it produces
answers that are confidently, plausibly wrong.
:::

