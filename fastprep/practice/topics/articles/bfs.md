# Breadth-first Search

> BFS is not "a way to visit every node". It is a way of growing a ball around a
> source one radius at a time, which is why the first time it touches a node, it
> has touched it by a shortest route.

## When you reach for it

You reach for BFS when the question is **how few steps**, and every step costs
the same.

That is the whole trigger, and it is worth saying what each half rules out. "How
few steps" means you want a distance, not just an answer to "can I get there" —
if all you need is reachability, [[dfs]] is three lines shorter and [[union-find]]
is faster still when the edges arrive over time. "Every step costs the same"
means unit weights: the moment one edge costs 3 and another costs 1, the ball
stops being a ball and you need [[dijkstra]].

Two hundred problems in this bank use BFS, which puts it at #21 of 150. They fall
into five shapes, and it is worth being able to name them:

- **Fewest edges in a plain graph.** *Shortest Path in an Unweighted Graph* is
  the bare statement — return the minimum number of edges from source to target,
  or -1. *Minimum Clicks Between Wiki Pages* is the same thing dressed as
  hyperlinks.
- **Levels of a tree.** *Binary Tree Level-Order Traversal by Levels*, *Binary
  Tree Right View*, *Check Whether All Leaves Are at the Same Level*. The distance
  is the depth, and the interesting object is the level itself, not the number.
- **Something spreading through a grid, per unit of time.** *Rotten Oranges /
  Grid Infection BFS*, *Minimum Time to Spread Through a Grid*, *Distance to the
  Nearest Supply Point*. One minute of spreading is exactly one BFS level.
- **A graph that does not exist in memory.** *Open the Lock*, *Word Ladder*,
  *Minimum Knight Moves*, *Coin Change*. Nobody hands you an adjacency list; a
  node is a state and the edges are the legal moves. This is the shape that wins
  interviews, and the one people fail to recognise.
- **Reachability and flood fill.** *Reachable Nodes in a Directed Graph*, *Finite
  Web Crawler*, *Number of Islands*. BFS is not required here — DFS does it — but
  BFS is iterative, so it cannot blow the stack on a 10⁵-node chain.

And the shapes where it is the wrong tool. Weighted edges: [[dijkstra]], or
[[bellman-ford]] if weights can be negative. Counting paths rather than measuring
the shortest one: that is a DP over the graph. All paths, or a path with a
property you can only check at the end: [[backtracking]]. The near-miss to keep in
mind is *Cheapest Flights Within K Stops* — "cheapest" has weights in it, so the
plain algorithm below does not apply, although a layered version does.

## The idea

Drop a stone in water at the source and watch the ripple.

At time 0 the wavefront is `{s}`. At time 1 it is everything one edge from `s`.
At time 2 it is everything two edges from `s` and not already wet. The ripple
never goes backwards, never skips a radius, and the time at which a node gets wet
*is* its distance from `s`. That is the entire algorithm; the rest is how you
store the wavefront.

You store it in a **queue**, first in first out ([[queue]]). The reason is
precise and worth stating once: nodes are discovered in nondecreasing order of
distance, so if you remove them in the order they arrived, you expand all of
distance `d` before any of distance `d + 1`. The queue therefore holds at most
two distinct distances at any instant — the tail of the current ring and the head
of the next one. Swap the queue for a stack and you get [[dfs]], which is a fine
algorithm that answers a different question. Swap it for a priority queue and you
get [[dijkstra]]. The container *is* the algorithm.

<svg viewBox="0 0 660 280" role="img" aria-label="a wavefront expanding in rings from a source, and a queue holding only two adjacent distances">
  <g>
    <circle class="fill" cx="160" cy="140" r="13"/>
    <text x="160" y="118" text-anchor="middle">s</text>
    <circle cx="160" cy="140" r="45"/>
    <circle cx="160" cy="140" r="85"/>
    <circle cx="160" cy="140" r="122"/>
    <text x="160" y="103" text-anchor="middle">1</text>
    <text x="160" y="63" text-anchor="middle">2</text>
    <text x="160" y="26" text-anchor="middle">3</text>
    <text x="160" y="275" text-anchor="middle">every node wet at time d is at distance d</text>
    <rect x="360" y="110" width="60" height="42" rx="4"/>
    <rect class="fill" x="420" y="110" width="60" height="42" rx="4"/>
    <rect class="fill" x="480" y="110" width="60" height="42" rx="4"/>
    <rect class="fill" x="540" y="110" width="60" height="42" rx="4"/>
    <text x="390" y="137" text-anchor="middle">d</text>
    <text x="450" y="137" text-anchor="middle">d</text>
    <text x="510" y="137" text-anchor="middle">d+1</text>
    <text x="570" y="137" text-anchor="middle">d+1</text>
    <text x="360" y="95" text-anchor="middle">head</text>
    <text x="600" y="95" text-anchor="middle">tail</text>
    <line x1="352" y1="131" x2="330" y2="131"/>
    <line x1="330" y1="131" x2="342" y2="124"/>
    <line x1="330" y1="131" x2="342" y2="138"/>
    <text x="480" y="180" text-anchor="middle">the queue is never more than two rings wide</text>
  </g>
</svg>

One detail decides whether your BFS is usable: **mark a node as seen when you
push it, not when you pop it.** A node with five neighbours in the current ring
would otherwise enter the queue five times. Marking at pop still gives the right
distances, as we will see — but it changes the queue from `O(V)` to `O(E)`.

## Worked by hand

Seven nodes, eight undirected edges, source `0`. Neighbours are scanned in
increasing order.

    edges: 0-1  0-2  1-3  2-3  2-4  3-5  4-5  5-6

Start with `dist[0] = 0`, everything else unset, queue `[0]`.

| step | pop | queue after pop | neighbours scanned | newly discovered | queue after pushes |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | `[]` | 1, 2 | 1 (d=1), 2 (d=1) | `[1, 2]` |
| 2 | 1 | `[2]` | 0, 3 | 3 (d=2) | `[2, 3]` |
| 3 | 2 | `[3]` | 0, 3, 4 | 4 (d=2) | `[3, 4]` |
| 4 | 3 | `[4]` | 1, 2, 5 | 5 (d=3) | `[4, 5]` |
| 5 | 4 | `[5]` | 2, 5 | — | `[5]` |
| 6 | 5 | `[]` | 3, 4, 6 | 6 (d=4) | `[6]` |
| 7 | 6 | `[]` | 5 | — | `[]` |

Final distances: `[0, 1, 1, 2, 2, 3, 4]`. The parent recorded at the moment of
discovery gives the tree `1←0, 2←0, 3←1, 4←2, 5←3, 6←5`, and walking parents back
from 6 gives the path `0 → 1 → 3 → 5 → 6`, four edges long, which matches
`dist[6] = 4`.

<svg viewBox="0 0 640 260" role="img" aria-label="the BFS tree drawn in levels, with two non-tree edges joining adjacent levels">
  <g>
    <circle class="fill" cx="60" cy="120" r="18"/>
    <text x="60" y="126" text-anchor="middle">0</text>
    <circle cx="180" cy="60" r="18"/>
    <text x="180" y="66" text-anchor="middle">1</text>
    <circle cx="180" cy="180" r="18"/>
    <text x="180" y="186" text-anchor="middle">2</text>
    <circle cx="300" cy="60" r="18"/>
    <text x="300" y="66" text-anchor="middle">3</text>
    <circle cx="300" cy="180" r="18"/>
    <text x="300" y="186" text-anchor="middle">4</text>
    <circle cx="420" cy="120" r="18"/>
    <text x="420" y="126" text-anchor="middle">5</text>
    <circle cx="540" cy="120" r="18"/>
    <text x="540" y="126" text-anchor="middle">6</text>
    <line x1="75" y1="109" x2="165" y2="71"/>
    <line x1="75" y1="131" x2="165" y2="169"/>
    <line x1="198" y1="60" x2="282" y2="60"/>
    <line x1="198" y1="180" x2="282" y2="180"/>
    <line x1="315" y1="71" x2="405" y2="109"/>
    <line x1="438" y1="120" x2="522" y2="120"/>
    <line x1="196" y1="168" x2="284" y2="72"/>
    <line x1="316" y1="169" x2="406" y2="131"/>
    <text x="238" y="125" text-anchor="middle">2-3</text>
    <text x="368" y="168" text-anchor="middle">4-5</text>
    <text x="60" y="230" text-anchor="middle">d=0</text>
    <text x="180" y="230" text-anchor="middle">d=1</text>
    <text x="300" y="230" text-anchor="middle">d=2</text>
    <text x="420" y="230" text-anchor="middle">d=3</text>
    <text x="540" y="230" text-anchor="middle">d=4</text>
  </g>
</svg>

Four things in that trace the code alone would not show you.

**The queue never held more than two distinct distances.** Look at the column:
`[1, 2]` is two nodes at distance 1; `[2, 3]` is a 1 and a 2; `[4, 5]` is a 2 and
a 3. That is not a coincidence of this graph, it is the invariant the proof below
is built on, and it is also why the "process a whole level at once" trick works:
at the top of an iteration, the queue is exactly one level, or one level plus the
beginning of the next.

**Step 3 discovered nothing when it looked at node 3.** Node 2 is adjacent to 3,
but 3 had already been marked in step 2, when node 1 pushed it. Had we marked
only on pop, node 3 would be sitting in the queue twice at this point. Its
distance would still come out as 2 — the first copy popped is the one that counts
— but the queue would be carrying garbage.

**Edges 2-3 and 4-5 are not in the tree, and both join adjacent levels.** That is
general for undirected graphs: no edge can join level `d` to level `d + 2`,
because its endpoint at level `d` would have discovered the other one at level
`d + 1`. So every non-tree edge either joins adjacent levels or joins two nodes in
the *same* level — and a same-level edge closes an odd cycle. If we added edge
1-2 here, nodes 1 and 2 are both at distance 1, and `0-1-2-0` is a triangle. That
single observation is the whole of *Check Bipartite Graph*, *Two-Color an
Undirected Graph* and *Possible Bipartition*: see [[bipartite]].

**No `dist` entry is ever overwritten.** Distances are final when discovered.
That is the practical difference from [[dijkstra]], which relaxes and revises, and
it is why BFS needs no priority queue.

## Why it is correct

Write `δ(s, v)` for the true minimum number of edges on any path from `s` to `v`,
and `∞` if there is none. The claim to prove is that the algorithm ends with
`dist[v] = δ(s, v)` for every `v`, and `dist[v]` unset exactly when `δ(s, v) = ∞`.

:::proof BFS computes δ
**The algorithm.** `dist[s] = 0`; queue `Q = [s]`. While `Q` is non-empty: pop
the front `u`; for each neighbour `v` of `u` with `dist[v]` unset, set
`dist[v] = dist[u] + 1` and push `v` at the back.

**Invariant.** At the top of every iteration, writing the queue as
`v₁, v₂, …, v_k` (front to back):

- **(Q1)** `dist[v₁] ≤ dist[v₂] ≤ … ≤ dist[v_k] ≤ dist[v₁] + 1`.
- **(Q2)** Every vertex whose `dist` is set is either in `Q` or has already been
  popped, and every already-popped vertex `u` satisfies `dist[u] ≤ dist[v₁]`.
- **(Q3)** For every vertex with `dist` set, there is a walk from `s` to it of
  exactly `dist[v]` edges. Hence `dist[v] ≥ δ(s, v)`.

*Base case.* `Q = [s]`, `dist[s] = 0`, nothing else is set and nothing has been
popped. (Q1) is a one-element chain; (Q2) is vacuous; (Q3) holds with the empty
walk.

*Inductive step.* Assume the invariant and pop `u = v₁`. The remaining queue is
`v₂, …, v_k`, which is still sorted, and every value pushed in this iteration is
`dist[u] + 1`. Two things must be checked. Sortedness at the join: (Q1) gave
`dist[v_k] ≤ dist[v₁] + 1 = dist[u] + 1`, so appending values equal to
`dist[u] + 1` keeps the sequence nondecreasing. The spread: the new front is `v₂`
with `dist[v₂] ≥ dist[u]`, and the new back holds `dist[u] + 1 ≤ dist[v₂] + 1`, so
(Q1) is restored. (If the queue empties on the pop, all pushed values are equal
and (Q1) is trivial.) For (Q2), `u` is now popped and `dist[u] ≤ dist[v₂]`, again
by sortedness, while the newly discovered vertices are in `Q`. For (Q3), each new
vertex `v` got `dist[u] + 1`, and a walk to `u` of `dist[u]` edges plus the edge
`u–v` is a walk to `v` of that length.

*Termination.* `dist[v]` is set at the instant `v` is pushed and is never unset,
and a vertex is pushed only when its `dist` is unset. So each vertex is pushed at
most once, there are at most `|V|` pushes, hence at most `|V|` pops, and the loop
ends.

**Main claim,** by strong induction on `d`: every `v` with `δ(s, v) = d` ends with
`dist[v] = d`.

*d = 0.* Only `s` has `δ = 0`, and `dist[s] = 0` is set before the loop.

*d → d + 1.* Let `δ(s, v) = d + 1` and let `u` be the vertex before `v` on some
shortest path, so `δ(s, u) = d` and `u–v` is an edge. By the induction hypothesis
`dist[u] = d`, so `u` was pushed, and by termination plus (Q2) every pushed vertex
is eventually popped. Consider the iteration that pops `u`. Either `dist[v]` is
still unset, and the algorithm sets it to `dist[u] + 1 = d + 1`; or it was set
earlier, when some vertex `w` popped before `u` discovered it, giving
`dist[v] = dist[w] + 1`. In the second case (Q2) at the time of `u`'s pop says
`dist[w] ≤ dist[u] = d`, so `dist[v] ≤ d + 1`; and (Q3) says
`dist[v] ≥ δ(s, v) = d + 1`. Both cases give `dist[v] = d + 1`.

*Unreachable vertices.* By (Q3), any vertex with `dist` set has a walk from `s`,
so a vertex with `δ(s, v) = ∞` is never discovered and its `dist` stays unset. ∎
:::

Now the assumptions, because that is where the bugs live.

- **Every edge costs exactly one.** The step `dist[v] = dist[u] + 1` and the
  spread bound in (Q1) both hard-code it. With weights 1 and 7, (Q1) collapses
  and a node can be discovered by a cheap-looking long route first. No amount of
  care with the queue repairs this; you need a different algorithm.
- **FIFO order.** (Q1) is a statement about a *queue*. A stack breaks it on the
  first branch, as the trap section demonstrates on a five-cycle.
- **`dist` is set at push time.** Termination counted pushes using exactly this.
  Set it at pop time instead and each vertex can be pushed once per incoming
  edge; the answers survive, the `O(V)` queue bound does not.
- **A node is a *state*, and two states are the same only if everything about
  them is the same.** The proof speaks of `v` in a graph; your `visited` set
  decides what `v` means. If the real state is "cell plus how many walls I may
  still break" and you dedupe on the cell alone, you are running a correct BFS on
  the wrong graph. See [[state-design]].
- **The graph is finite and does not change while you search it.** *Finite Web
  Crawler* says "finite" in its title for a reason.
- **Direction.** Nothing in the proof assumed symmetry, so directed graphs are
  fine — but `δ(s, v) ≠ δ(v, s)` there, and BFS from the wrong end answers the
  wrong question. *Directed Path Existence* punishes this.

## What it costs

Count pushes and count edge scans; everything else is bookkeeping.

**Pushes.** From the termination argument, each vertex is pushed at most once, so
there are at most `|V|` pushes and `|V|` pops, each `O(1)` on a deque.

**Edge scans.** A vertex's adjacency list is scanned exactly once, when it is
popped. Summing over all vertices, the total is `Σ_u deg(u)`, which is `2|E|` for
an undirected graph and `|E|` for a directed one.

So the running time is **Θ(V + E)** — and note that it is `V + E`, not `E`: a
graph with 10⁵ isolated vertices and no edges still costs 10⁵ to initialise
`dist`. *Shortest Path in an Unweighted Graph* states `n ≤ 10⁵` and
`edges ≤ 2·10⁵`, which is exactly the shape of an intended `Θ(V + E)` solution.

**Space.** `dist` and `parent` are `O(V)`. The queue is more interesting: by (Q1)
it holds at most two consecutive levels, so its peak size is
`max_d (|L_d| + |L_{d+1}|)`, where `L_d` is the set of vertices at distance `d`.
On an `R × C` grid the frontier of a ball is a diagonal band, so the queue stays
`O(R + C)` even though the grid has `R·C` cells — a useful thing to know when the
grid is large. On a star graph the first level is everything and the queue really
does reach `V`. The worst case is `O(V)`; the typical case is much less.

**The costs people forget.**

*Building the graph.* An edge list to adjacency list conversion is another
`Θ(V + E)`. If instead you are handed an adjacency **matrix**, scanning a row is
`Θ(V)` per pop whether or not the edges exist, so BFS becomes `Θ(V²)`. *Shortest
Distances From an Adjacency Matrix* is that problem, and `Θ(V²)` is the honest
answer there, not a failure.

*Hashing the state.* When nodes are tuples or strings — *Open the Lock*, *Word
Ladder*, *Minimum Knight Moves* on an unbounded board — every `visited` test
hashes an `L`-character object, so the real bound is `Θ((V + E)·L)`
([[hash-tables]]). That term usually dominates, and it is why *Word Ladder* is
solved by bucketing words under wildcard patterns (`h*t`), at `O(L²)` per word,
rather than comparing every pair at `O(V²L)`.

*The wrong queue.* `list.pop(0)` shifts every remaining element, so it costs
`O(V)` per pop and turns the search into `Θ(V²)`; `collections.deque` pops in
`O(1)`. That one line is the most common reason a correct BFS times out.

## The implementation

```python run
from collections import deque
import random


def bfs(n, adj, source):
    """Edge-distances from source, plus the BFS tree, on an unweighted graph."""
    dist = [-1] * n
    parent = [-1] * n
    dist[source] = 0
    q = deque([source])
    while q:
        u = q.popleft()                     # FIFO: all of ring d before ring d+1
        for v in adj[u]:
            if dist[v] == -1:               # first sighting is the shortest one
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)                 # marked BEFORE it enters the queue
    return dist, parent


def path(parent, target):
    out = []
    while target != -1:
        out.append(target)
        target = parent[target]
    return out[::-1]


n = 7
adj = [[] for _ in range(n)]
for a, b in [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6)]:
    adj[a].append(b)
    adj[b].append(a)

dist, parent = bfs(n, adj, 0)
print("distances from 0:", dist)
print("one shortest 0->6:", path(parent, 6))
assert dist == [0, 1, 1, 2, 2, 3, 4]
assert len(path(parent, 6)) - 1 == dist[6]


def relax_to_fixpoint(n, adj, s):
    """Obviously correct, obviously slow: relax every edge until nothing moves."""
    INF = float("inf")
    d = [INF] * n
    d[s] = 0
    for _ in range(n):
        for u in range(n):
            for v in adj[u]:
                d[v] = min(d[v], d[u] + 1)
    return [-1 if x == INF else x for x in d]


rng = random.Random(3)
for _ in range(300):
    m = rng.randint(1, 8)
    a = [[] for _ in range(m)]
    for _ in range(rng.randint(0, 14)):
        x, y = rng.randrange(m), rng.randrange(m)
        a[x].append(y)
        a[y].append(x)
    s = rng.randrange(m)
    assert bfs(m, a, s)[0] == relax_to_fixpoint(m, a, s), (m, a, s)
print("300 random graphs: BFS matches relaxation to a fixpoint")
```

Three lines carry the weight.

`if dist[v] == -1:` is doing two jobs at once — it is the visited test *and* the
distance, so there is no second array to keep in sync. Any sentinel works; `-1`
is convenient because most statements want `-1` for "unreachable" anyway.

`q.append(v)` comes *after* `dist[v]` is assigned, in the same branch. Reading
those two statements as one unit is the habit that prevents the commonest
performance bug in this topic. If you ever find yourself writing
`if v not in seen` at the top of the loop body rather than in the neighbour scan,
stop and ask which one you are doing.

`parent[v] = u` at discovery time is how you report a route rather than a number,
at the cost of one array — *Print a Shortest Graph Path*, *Web Crawler Shortest
Path Reconstruction*, *Find and Reconstruct a Binary-Matrix Path*. The tree
records *one* shortest path per node; for all of them you keep a list of parents,
and the count can be exponential.

## Variants you will meet

**Level-by-level BFS.** Snapshot `len(q)` before the inner loop and process
exactly that many nodes: everything you pop in that pass is one level. This is
how you answer "return the levels as a list of lists" (*Binary Tree Level-Order
Traversal by Levels*), "the rightmost node of each level" (*Binary Tree Right
View*), "alternate direction" (*Binary Tree Zigzag Level Order Traversal*), and
"how many minutes" (*Rotting Oranges*).

**Multi-source BFS.** Push *every* source at distance 0 before the loop starts,
and each cell learns its distance to the *nearest* source in one pass. The proof
needs no amendment: this is BFS from a virtual node joined to every source by a
free edge, and (Q1) holds initially because all the seeded values are equal.
*Rotten Oranges*, *Distance to the Nearest Supply Point* and *Distances to the
Nearest Infected Node* are this, and it has its own chapter:
[[multi-source-bfs]].

```python run
from collections import deque


def minutes_until_all_rot(grid):
    """0 empty, 1 fresh, 2 rotten. Minutes until nothing is fresh, else -1."""
    R, C = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                q.append((r, c))            # every source starts at distance 0
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):             # snapshot: exactly this level
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2        # mark on push, by mutating the grid
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes


def slow(grid):
    """min over sources of a single-source BFS, then the max over fresh cells."""
    R, C = len(grid), len(grid[0])
    INF = float("inf")
    best = [[INF] * C for _ in range(R)]
    for sr in range(R):
        for sc in range(C):
            if grid[sr][sc] != 2:
                continue
            seen = {(sr, sc): 0}
            q = deque([(sr, sc)])
            while q:
                r, c = q.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1 \
                            and (nr, nc) not in seen:
                        seen[(nr, nc)] = seen[(r, c)] + 1
                        q.append((nr, nc))
            for (r, c), d in seen.items():
                best[r][c] = min(best[r][c], d)
    worst = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1:
                if best[r][c] == INF:
                    return -1
                worst = max(worst, best[r][c])
    return worst


for g in ([[2, 1, 1], [1, 1, 0], [0, 1, 1]],
          [[2, 1, 1], [0, 1, 1], [1, 0, 1]],
          [[0, 2]], [[2, 2], [1, 1]]):
    expect = slow([row[:] for row in g])
    got = minutes_until_all_rot([row[:] for row in g])
    print(g, "->", got)
    assert got == expect, (g, got, expect)
print("multi-source level BFS agrees with one BFS per source, everywhere")
```

**Grid BFS.** The adjacency list is four (or eight) offsets computed on the fly;
the node id is `(r, c)` or `r * C + c`. *Number of Islands*, *Minimum Grid Moves*,
*The Maze*, *Minesweeper Board Update*. Full treatment in [[grid-bfs]], and the
component-counting side of it in [[flood-fill]].

**BFS over an implicit state graph.** The node is whatever you must know to
continue: a lock's four digits in *Open the Lock*, a word in *Word Ladder*, an
amount of money in *Coin Change* (each coin is an edge of length 1, so the fewest
coins is a shortest path), a square in *Minimum Knight Moves*. You never build the
graph; you write a `neighbours(state)` function. Choosing the state well is the
hard part — [[state-design]] and [[graph-modelling]].

**An extra dimension in the state.** *Shortest Path in a Grid with Obstacles
Elimination* has state `(r, c, k_left)`; *Shortest Path Visiting All Nodes* has
`(node, bitmask)`. The algorithm does not change — only what counts as "the same
node".

**0-1 BFS.** Edges of weight 0 or 1: use a deque, push a 0-edge to the *front* and
a 1-edge to the back ([[deque]]). Invariant (Q1) is preserved, so you get
Dijkstra's answer in `Θ(V + E)` with no heap. *Minimum Direction Violations* and
*Minimum Route Reversals to Warehouse Zero* — where travelling along an edge the
right way is free and reversing it costs 1 — are exactly this.

**Bidirectional BFS.** Search from both ends, stop when the frontiers touch: with
branching factor `b` and depth `d`, `b^d` states become about `2b^{d/2}`. On *Word
Ladder* that is the difference between comfortable and hopeless. The general
principle is [[meet-in-the-middle]].

**Kahn's algorithm.** Topological sort is BFS on in-degree: start from the nodes
with in-degree 0, and decrement as you remove. *Course Schedule*, *Course Schedule
II*, *Agent Task Dependency Tracker*. See [[topological-sort]].

**Double BFS for a tree diameter.** BFS from anywhere to find a farthest node
`a`, then BFS from `a`; the farthest node from `a` is the other end of a longest
path. *Find the Tree Diameter*, *Diameter of an Acyclic Undirected Graph*.

**Turning a tree into a graph.** *All Nodes Distance K in a Binary Tree* and
*Amount of Time to Infect a Tree* need to walk *upwards* as well as down. Add
parent links with one DFS, then BFS from the target. The trick is not the BFS; it
is noticing that a tree with parent pointers is an undirected graph of degree ≤ 3.

**Weighted graphs.** [[dijkstra]] is BFS with a priority queue, and the whole
family is laid out in [[shortest-path]].

## Recognising it in a statement

In rough order of how much you should trust the signal:

1. **"minimum number of moves / steps / edges / operations / transformations"**
   together with moves that all cost the same. *Minimum Moves*, *Minimum Knight
   Moves*, *Minimum Grid Moves*, *Determine the Edit Distance in a Word Ladder*.
2. **"level", "depth", "distance k", "by levels"** on a tree. *Nodes at a Given
   N-ary Tree Level*, *Binary Tree Nodes at Distance K*, *Count Levels*.
3. **Something spreading per unit of time.** "each minute", "each second", "until
   stable" — *Grid Infection Spread Until Stable*, *Virus Spread*, *Flight Delay
   Propagation*, *Malware Spread*. One tick equals one level.
4. **"nearest" / "closest"** with several candidate targets: multi-source BFS.
   *Closest DashMart*, *Nearby Fulfillment Centers with Inventory*, *Nearest
   Reachable Grid Corner*.
5. **A small set of legal moves from a configuration.** Knight jumps, turning a
   dial, changing one letter, doubling or decrementing a number — *Count
   Reachable Values by Halving and Decrementing*, *Smallest Binary-Digit
   Multiple*. If you can enumerate the moves, you have edges.
6. **Constraints in the `10⁵`–`10⁶` range with the graph given as an edge list.**
   That is the fingerprint of an intended `Θ(V + E)` traversal.

The anti-signals, which matter just as much:

- **Different edge costs.** "cheapest", "minimum total weight", "time varies per
  road". Go to [[dijkstra]]. *Cheapest Flights Within K Stops* is the trap: it
  looks like "within K steps" but the objective is a sum of costs.
- **"How many ways", "count the paths".** Counting is DP, not traversal, even
  when the graph is unweighted.
- **"Is there a path" and nothing more.** [[dfs]] is shorter, and if the edges
  arrive incrementally [[union-find]] is better.
- **"Longest path" in a general graph.** Not a traversal problem at all. In a
  *tree* it is the double-BFS diameter; in a DAG it is DP over a topological
  order; in a general graph it is NP-hard.
- **"Maximum depth of a binary tree".** *Maximum Depth of Binary Tree* and
  *Maximum Depth of an N-ary Tree* are in this bank's BFS list, but a three-line
  recursion answers them; reaching for a queue is showing off, not thinking.

## Traps

**A stack instead of a queue.** Symptom: reachability right, distances too large,
and small cases pass because short graphs hide it. Demonstrated below.

**Marking visited at pop.** Symptom: correct answers, then a memory or time
blow-up on dense input. Demonstrated below. The reason it survives correctness is
that the first copy of a node to be popped is the one that was pushed earliest,
which by (Q1) carries the smallest distance — but every other copy is dead weight.

**`list.pop(0)`.** Symptom: correct answers, quadratic time, a timeout at
`n = 10⁵`. Use `collections.deque`.

**Forgetting to mark the source.** Symptom: a neighbour rediscovers it, distances
shift by 2 around a cycle, or the loop never ends on a self-loop.

**Reading `len(q)` inside the level loop.** `for _ in range(len(q))` evaluates
`len(q)` once and is correct; `while len(q) > 0` inside the level, or a loop that
re-reads the length, drags the next level into the current one. Symptom: every
level after the first is wrong, usually merged with its successor.

**Deduping on a projection of the state.** In *Shortest Path in a Grid with
Obstacles Elimination* you may reach a cell in 4 steps having spent both
eliminations, or in 6 having spent none. If `visited` holds only the cell, the
cheap-but-poor arrival blocks the expensive-but-rich one and a route needing one
more elimination is reported unreachable. The state is `(r, c, k_left)`. Symptom:
`-1` where an answer plainly exists. Same bug, `(node, mask)`, in *Shortest Path
Visiting All Nodes*.

**Off-by-one between levels and edges.** A path with 4 edges visits 5 nodes; a
grid with nothing fresh answers 0, not -1. Decide up front whether you count nodes
or edges, and put it in the variable name.

**Reusing `visited` across separate searches — or failing to.** Counting islands
needs one shared `visited` across all the BFS calls; a fresh BFS per source needs
separate ones. Symptoms, respectively: islands counted twice, or every source
after the first reporting `-1`.

```python run
from collections import deque


def bfs_push_marked(n, adj, s):
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    pushes = 1
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
                pushes += 1
    return dist, pushes


def bfs_pop_marked(n, adj, s):
    dist = [-1] * n
    q = deque([(s, 0)])
    pushes = 1
    while q:
        u, d = q.popleft()
        if dist[u] != -1:                 # marked only now, at pop time
            continue
        dist[u] = d
        for v in adj[u]:
            if dist[v] == -1:
                q.append((v, d + 1))
                pushes += 1
    return dist, pushes


def lifo_search(n, adj, s):               # identical, except it is a stack
    dist = [-1] * n
    dist[s] = 0
    st = [s]
    while st:
        u = st.pop()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                st.append(v)
    return dist


cycle = [[] for _ in range(5)]            # 0-1-2-3-4-0, so dist(0, 2) = 2
for a, b in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]:
    cycle[a].append(b)
    cycle[b].append(a)
print("queue :", bfs_push_marked(5, cycle, 0)[0])
print("stack :", lifo_search(5, cycle, 0), "<- node 2 reported 3 edges away")
assert bfs_push_marked(5, cycle, 0)[0][2] == 2
assert lifo_search(5, cycle, 0)[2] == 3

k = 8                                     # complete graph: every pair adjacent
comp = [[v for v in range(k) if v != u] for u in range(k)]
d1, p1 = bfs_push_marked(k, comp, 0)
d2, p2 = bfs_pop_marked(k, comp, 0)
print("K8 distances identical:", d1 == d2, " pushes:", p1, "vs", p2)
assert d1 == d2 and p2 > 3 * p1
print("marking at pop is not wrong; it is expensive, and it scales with E")
```

The two failures are different in kind, and that is the point of running them side
by side. The stack gives a *wrong answer* with no warning. Marking at pop gives
the *right answer* and a queue that grows with the number of edges — a bug you
only meet on the large test, which is the worst kind.

## What to memorise

The template, which should come out of your fingers whole:

```python
from collections import deque

dist = {start: 0}
q = deque([start])
while q:
    u = q.popleft()
    for v in neighbours(u):
        if v not in dist:          # test and mark and record, in one place
            dist[v] = dist[u] + 1
            q.append(v)
```

And its level-wise sibling, for when the question is "how many rounds" or "give me
each level":

```python
while q:
    for _ in range(len(q)):        # snapshot the level before touching it
        u = q.popleft()
        ...
    rounds += 1
```

The sentence that turns a problem into it: *"What is the state, what are the
legal moves, and do they all cost the same?"* If you can answer all three, the
code is mechanical; if the third answer is no, you are in [[dijkstra]] territory.

The habit: **mark when you push.** Write the assignment to `dist` and the
`append` as one inseparable pair, and half the traps in this chapter cannot
happen.

Numbers worth carrying: `Θ(V + E)` time, `O(V)` space; the queue never holds more
than two levels; a path with `k` edges visits `k + 1` nodes; bidirectional search
turns `b^d` into roughly `2b^{d/2}`, so a branching factor of 25 and depth 6 goes
from about 2.4·10⁸ states to about 3·10⁴.

## Check yourself

:::check
Why does marking nodes at pop time still produce correct distances, and what
exactly does it cost?
--
Correct, because of invariant (Q1): the queue is sorted by distance, so among all
the copies of a node `v` sitting in the queue, the first one popped is the one
that was pushed earliest, and it carries the smallest `dist[u] + 1` of any of
them — which the main induction shows is `δ(s, v)`. Every later copy is skipped
by the `if dist[u] != -1: continue` guard.

The cost is that a node is pushed once per incoming edge scanned before it was
finalised, so the queue holds `Θ(E)` entries instead of `Θ(V)` — on a dense graph
of 10⁴ nodes, 10⁸ against 10⁴. It is a memory bug wearing the costume of a
correct program.
:::

:::check
Why can the queue never contain three distinct distance values at once, and what
practical technique does that fact license?
--
Invariant (Q1) says the values in the queue are nondecreasing from front to back
and the back is at most the front plus one. The inductive step is where it is
earned: popping the front `u` can only push values equal to `dist[u] + 1`, and
`dist[u]` was the minimum in the queue, so nothing three or more above the new
front can ever be appended.

It licenses the level-wise loop. If the queue holds exactly one level at the top
of a pass, then snapshotting `len(q)` and popping that many nodes empties that
level and appends only the next one — so the queue again holds exactly one level,
and the induction carries. That is what makes "how many minutes" answerable
without storing a distance per node.
:::

:::check
*Cheapest Flights Within K Stops* asks for the least-cost route using at most `K`
intermediate stops. Why does the BFS in this chapter not answer it, and what is
the smallest change that does?
--
Because the objective is a sum of edge prices, not a count of edges, so the
assumption "every edge costs 1" fails. Invariant (Q1) is then false: a node can be
discovered by a two-hop route costing 900 before a three-hop route costing 100 is
ever considered, and BFS never revises a distance once set.

The smallest honest change is to keep BFS's *layers* — they are exactly the
"at most K stops" constraint — but relax costs within each layer instead of
marking nodes visited: run `K + 1` rounds, and in each round compute
`best_next[v] = min(best[u] + price(u, v))` from the previous round's array. That
is Bellman-Ford restricted to `K + 1` edges ([[bellman-ford]]), and the layering,
not the queue, is what BFS contributed. A plain [[dijkstra]] answers the cheapest
route but cannot honour the stop limit unless the stop count goes into the state.
:::

:::check
In an undirected graph, BFS from `s` labels every node with a level. Prove that
if any edge joins two nodes in the *same* level, the graph contains an odd cycle —
and say why that makes BFS a bipartiteness test.
--
Let edge `u–v` have `dist[u] = dist[v] = d`. Walk the BFS tree from `u` up to the
root and from `v` up to the root; let `w` be the deepest node common to both
walks, at level `c`. The tree path `w → u` has `d - c` edges and so does
`w → v`, and adding the edge `u–v` closes a cycle of length `2(d - c) + 1`, which
is odd.

A graph is bipartite exactly when it has no odd cycle, so: colour each node by the
parity of its level, and check every edge. If no edge joins equal levels, the
parity colouring is a proper 2-colouring (every edge joins adjacent levels, which
have opposite parity); if some edge does, the odd cycle just constructed forbids
any 2-colouring. One BFS, one parity array — that is *Check Bipartite Graph* and
*Two-Color an Undirected Graph*. See [[bipartite]].
:::

:::check
Someone says: "BFS finds shortest paths, so the last node it pops is the farthest
node in the graph, and the path to it is the longest path." Where are they wrong,
and what is the piece of that claim that is genuinely true and useful?
--
Two errors. First, "farthest node in the graph" is wrong: the last node popped is
a node of maximum distance **from `s`**, which is `s`'s eccentricity, not the
graph's diameter. Start somewhere else and you may get a smaller number. Second,
"longest path" is wrong in a much deeper way: BFS measures *shortest* routes, so
`dist[v]` being large only says `v` is far by the best route. The longest *simple*
path in a general graph is NP-hard, and no traversal finds it.

The true and useful piece: in a **tree**, a node farthest from any starting node
is an endpoint of a diameter. So BFS from an arbitrary node to find `a`, then BFS
from `a`, and the maximum distance in the second run is the diameter. That is the
standard solution to *Find the Tree Diameter* and *Diameter of an Acyclic
Undirected Graph* — and it works only because a tree has exactly one simple path
between any two nodes, so "shortest" and "longest" coincide there.
:::
