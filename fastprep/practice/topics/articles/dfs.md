# Depth-first Search

> Depth-first search is not a way of listing vertices. It is a way of laying a
> tree over a graph, and almost every DFS problem is a question about that tree
> rather than about the walk that built it.

## When you reach for it

Two hundred and twenty-one problems in this bank use depth-first search, which
makes it the seventeenth most-used topic of the hundred and fifty here. That is
not because DFS is glamorous. It is because a huge fraction of questions are
really one of four questions, and DFS answers all four in the same ten lines:

- **What can I reach?** *Directed Path Existence*, *Reachable Nodes in a Directed
  Graph*, *Path Existence in an Undirected Graph*, *Binary Matrix Top-to-Bottom
  Reachability*.
- **How do the things fall into groups?** *Count Connected Components*,
  *Connected Groups*, *Count Islands with DFS and BFS*, *Find Largest House
  Area*, *Count Connected Point Clusters*, *Flood Fill*.
- **What is true of each subtree?** *Employee Subordinates*, *Rocket Component
  Cost*, *Aggregate Machine Topology*, *Maximum Depth of Binary Tree*, *Balanced
  Tree Node Report*.
- **Enumerate the things along a path, or all the paths.** *Path Sum*,
  *Root-to-Node Path in a Binary Tree*, *Binary Tree Target-Sum Paths*,
  *Minimum-Sum Root-to-Leaf Path*, *DFS Subsequences of a String*.

The unifying shape: **the question is about structure, not about distance.**
DFS explores in an order that makes the current *path* an explicit object you
can carry, so anything phrased as "on the way down" or "having seen my whole
subtree" falls out for free.

The shape that makes it the wrong tool is a single word: **shortest**. DFS will
happily find *a* path between two grid cells; the first one it finds can be
absurdly long, and there is no cheap fix. "Fewest moves", "minimum number of
steps", "level by level" mean [[bfs]]; weighted edges mean [[dijkstra]]. Two
more anti-signals: if the edges arrive over time and you are asked connectivity
questions in between, re-running DFS after each edge is quadratic and
[[union-find]] is the structure; and if the graph is so deep that the recursion
stack is the constraint, you still use DFS, but you write it with an explicit
stack, which is the second half of this chapter.

## The idea

Walk as far as you can. When you are stuck, back up one step and try the next
unexplored door. Never enter a room twice.

That is the whole algorithm, and the rule "never enter a room twice" does
something to the walk worth noticing. The edges you actually *walked through* —
the edge that first led you into each vertex — form a tree: every visited vertex
has exactly one, except the one you started from. So DFS silently builds a
spanning tree of everything it reaches, the **DFS tree**. Every other edge is
then classified by where its endpoints sit in that tree, and that
classification is where the algorithm's power lives.

To make the classification precise, give every vertex a colour:

- **white** — not yet seen;
- **grey** — entered but not finished; equivalently, *on the current path*;
- **black** — finished; its whole subtree has been explored.

And give every vertex two timestamps from a clock that ticks on each event:
`tin[v]` when it turns grey, `tout[v]` when it turns black.

<svg viewBox="0 0 660 260" role="img" aria-label="a six-vertex directed graph with its DFS tree drawn solid, one back edge and two cross edges drawn dashed">
  <g>
    <circle class="fill" cx="120" cy="40" r="19"/>
    <text x="120" y="46" text-anchor="middle">0</text>
    <circle cx="55" cy="125" r="19"/>
    <text x="55" y="131" text-anchor="middle">1</text>
    <circle cx="200" cy="125" r="19"/>
    <text x="200" y="131" text-anchor="middle">2</text>
    <circle cx="55" cy="210" r="19"/>
    <text x="55" y="216" text-anchor="middle">3</text>
    <circle cx="200" cy="210" r="19"/>
    <text x="200" y="216" text-anchor="middle">4</text>
    <circle class="fill" cx="320" cy="125" r="19"/>
    <text x="320" y="131" text-anchor="middle">5</text>
    <line x1="107" y1="56" x2="68" y2="109"/>
    <line x1="133" y1="56" x2="187" y2="109"/>
    <line x1="55" y1="144" x2="55" y2="191"/>
    <line x1="200" y1="144" x2="200" y2="191"/>
    <path d="M 36 199 C -10 150 0 60 101 40" fill="none" stroke-dasharray="5 4"/>
    <path d="M 182 125 C 150 118 110 120 74 124" fill="none" stroke-dasharray="5 4"/>
    <path d="M 182 216 C 150 236 110 236 74 218" fill="none" stroke-dasharray="5 4"/>
    <path d="M 302 132 C 270 170 240 200 220 210" fill="none" stroke-dasharray="5 4"/>
    <text x="20" y="90">back</text>
    <text x="118" y="112">cross</text>
    <text x="118" y="250">cross</text>
    <text x="400" y="45">solid: tree edges, the walk itself</text>
    <text x="400" y="75">dashed: everything else</text>
    <text x="400" y="110">back edge -&gt; grey vertex -&gt; a cycle</text>
    <text x="400" y="140">cross edge -&gt; black vertex -&gt; no cycle</text>
    <text x="400" y="180">5 is a second root: DFS from 0</text>
    <text x="400" y="205">never reaches it</text>
  </g>
</svg>

Now the classification. Consider an edge `u → v` examined while `u` is grey:

- `v` is **white**: you walk it. Tree edge.
- `v` is **grey**: `v` is an ancestor of `u` on the current path, so the path
  from `v` down to `u` plus this edge is a **cycle**. Back edge.
- `v` is **black**: `v` is finished. Whatever it leads to has already been
  explored; this edge tells you nothing new about reachability and, crucially,
  cannot close a cycle. Forward or cross edge.

That three-way test is the entire content of directed cycle detection, of
[[topological-sort]] by finishing time, of [[strongly-connected|Tarjan's SCC]],
and of [[bridges-articulation|bridges and articulation points]]. They differ in
what they record, not in how they walk. Learn to see the colour, not the code.

## Worked by hand

Six vertices, directed, neighbours always taken in increasing order:

```
0: 1 2      1: 3      2: 1 4      3: 0      4: 3      5: 4
```

Start the outer loop at vertex 0, clock at 1, every event consuming one tick.

| step | event | current path (grey) | recorded |
| --- | --- | --- | --- |
| 1 | enter 0 | 0 | `tin[0]=1` |
| 2 | edge 0→1, white | 0 1 | `tin[1]=2`, tree edge |
| 3 | edge 1→3, white | 0 1 3 | `tin[3]=3`, tree edge |
| 4 | edge 3→0, **grey** | 0 1 3 | **back edge** — cycle 0→1→3→0 |
| 5 | leave 3 | 0 1 | `tout[3]=4` |
| 6 | leave 1 | 0 | `tout[1]=5` |
| 7 | edge 0→2, white | 0 2 | `tin[2]=6`, tree edge |
| 8 | edge 2→1, black | 0 2 | cross edge |
| 9 | edge 2→4, white | 0 2 4 | `tin[4]=7`, tree edge |
| 10 | edge 4→3, black | 0 2 4 | cross edge |
| 11 | leave 4 | 0 2 | `tout[4]=8` |
| 12 | leave 2 | 0 | `tout[2]=9` |
| 13 | leave 0 | — | `tout[0]=10` |
| 14 | outer loop finds 5 white | 5 | `tin[5]=11` |
| 15 | edge 5→4, black | 5 | cross edge |
| 16 | leave 5 | — | `tout[5]=12` |

The intervals `[tin, tout]` are

| vertex | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| interval | [1, 10] | [2, 5] | [6, 9] | [3, 4] | [7, 8] | [11, 12] |

Four things in that trace are not obvious from the code.

**The intervals nest or miss; they never overlap half-way.** `[2,5]` sits inside
`[1,10]`; `[3,4]` inside `[2,5]`; `[6,9]` is disjoint from `[2,5]`. That is
forced: an interval opens when a vertex becomes grey and closes when it becomes
black, and greys form a stack. This is the *parenthesis structure*, and it gives
you an O(1) ancestor test — `u` is an ancestor of `v` exactly when
`tin[u] < tin[v] <= tout[v] < tout[u]` — which is how subtree queries get
flattened into range queries over the `tin` order ([[fenwick-tree]],
[[segment-tree]]).

**Step 8 and step 10 look identical to step 4 if you only track "visited".** All
three edges point at a vertex DFS has already seen. Only one of them is a cycle.
A single boolean per vertex cannot tell them apart; you need grey versus black.
This is the single most common wrong answer in directed cycle detection, and the
traps section demonstrates it.

**The finishing order is 3, 1, 4, 2, 0, 5.** Reverse it: 5, 0, 2, 4, 1, 3. Check
each edge against that order — every one runs left to right except `3 → 0`,
which is precisely the back edge. Reverse finishing order is a topological order
whenever, and only whenever, there is no back edge. One traversal yields both
the cycle test and the ordering.

**Vertex 5 needed the outer loop.** Nothing reaches 5 from 0. A traversal
started at one vertex answers a reachability question; a traversal wrapped in
`for root in range(n)` answers a components question. *Connected Groups* insists
that "every member belongs to exactly one group, including an isolated member",
which is that outer loop spelled out in English.

## Why it is correct

There are two claims worth proving, and they are the two claims every DFS
problem rests on: that the traversal finds exactly the right set of vertices,
and that the grey test detects cycles exactly.

:::proof DFS from `s` marks exactly the vertices reachable from `s`, and halts
**The algorithm.** `visit(u)`: mark `u`; then for each `v` in `adj[u]` in order,
if `v` is unmarked, call `visit(v)`. Marks are set on entry and never cleared.

**Invariant (soundness).** *Every marked vertex is reachable from `s`, and the
chain of active calls spells a path from `s` to the vertex of the innermost
call.* Before the first mark, the only thing that will be marked is `s`, which is
reachable by the empty path, and the call chain is just `s`. Inductively,
suppose the invariant holds and `visit(u)` calls `visit(v)` for some `v ∈ adj[u]`.
By hypothesis there is a path `s ⇝ u` spelled by the call chain, and `u → v` is
an edge, so `s ⇝ u → v` is a path and the extended call chain spells it. No
other event marks a vertex. So at every moment, `marked ⊆ reach(s)`.

**Completeness.** Suppose some `v ∈ reach(s)` is unmarked when DFS returns. Take
a path `s = x₀ → x₁ → … → x_k = v` and let `i` be the largest index with `x_i`
marked at the end. Such an `i` exists because `x₀ = s` is marked, and `i < k`
because `x_k` is not. Since `x_i` was marked, `visit(x_i)` ran, and `visit` does
not return until its loop has examined every neighbour of `x_i`, including
`x_{i+1}`. At the moment the loop examined `x_{i+1}` there are two cases: it was
already marked, or it was unmarked and `visit(x_{i+1})` was called, which marks
it immediately. Either way `x_{i+1}` is marked at that moment, and since marks
are never cleared it is still marked at the end — contradicting the maximality
of `i`. So no such `v` exists and `reach(s) ⊆ marked`.

**Termination.** A call `visit(u)` is made only for an unmarked `u`, and marks
`u` before any recursive call. Marks are never cleared, so a vertex is the
argument of at most one call and there are at most `n` calls in total. Each call
performs `|adj[u]|` constant-time tests plus its recursive calls, and the number
of recursive calls is bounded by the same finite total. So the recursion tree is
finite and the algorithm halts. ∎
:::

:::proof A directed graph has a cycle iff DFS examines an edge into a grey vertex
**(⇐)** Suppose `visit(u)` examines `u → v` with `v` grey. Grey means `visit(v)`
has been entered and has not returned, so `visit(v)` is an ancestor of
`visit(u)` in the call tree — the calls form a stack, and only the calls on the
stack are unfinished. By the soundness invariant above, the chain of active calls
from `visit(v)` down to `visit(u)` spells a path `v ⇝ u` in the graph. Adding the
edge `u → v` closes it into a cycle.

**(⇒)** Suppose the graph has a cycle `C`. Every vertex of `C` is eventually
marked, since the outer loop starts a traversal at every unmarked vertex. Let `w`
be the vertex of `C` with the smallest `tin`, i.e. the first one to turn grey,
and let `p → w` be the edge of `C` entering `w`. Consider the moment `visit(w)`
is entered: at that instant `w` is grey, and every other vertex of `C` is still
white, because `w` was first. There is a path from `w` to `p` along `C`
consisting entirely of white vertices. By the white-path property — which is the
completeness argument above applied to the subgraph of vertices still white at
time `tin[w]` — every vertex on that path becomes a descendant of `w` in the DFS
tree, and in particular `visit(p)` is entered before `visit(w)` returns. So when
`visit(p)` examines the edge `p → w`, `w` is still grey, and that edge is
reported. ∎
:::

Now the assumptions, because that is where the bugs are.

- **Marks are set on entry, before the recursive calls.** Move the mark below
  the loop and the termination argument collapses outright: on a graph with a
  cycle nothing is marked in time and the recursion never ends.
- **Marks are never cleared.** [[backtracking]] is DFS that *does* clear marks on
  the way out, which is exactly why it is exponential rather than linear. The two
  algorithms differ by one line and by a factor that grows like the number of
  paths in the graph; know which one you are writing. Demonstrated in *Traps*.
- **The neighbour loop runs to completion.** The completeness argument used "a
  call does not return until it has examined every neighbour". A `return` placed
  inside the loop — very tempting when you are searching for one path — silently
  breaks it unless you are genuinely done with the whole search.
- **Grey and black are distinguishable.** The cycle proof uses "grey means on the
  current path". A single `visited` boolean collapses the two colours, and the
  (⇐) direction becomes false: an edge into a black vertex closes nothing.
- **The adjacency list is fixed while you walk it.** Mutating the graph mid-DFS
  invalidates both arguments. If you must mark cells of a grid by overwriting
  them, understand that you are mutating the *marks*, not the edges.
- **Undirected graphs need the parent edge excluded.** In an undirected graph
  every tree edge `u–v` appears again as `v–u` and its far endpoint is grey, so
  the (⇐) direction would report a cycle of length 2 that is not there. The fix
  is to ignore the edge you came in on — and to ignore it *by edge*, not by
  vertex, or two parallel edges between the same pair (a genuine cycle) will be
  missed.

## What it costs

Count events rather than quoting a result.

**Vertices.** By the termination argument, `visit` is entered at most once per
vertex, and the outer loop enters it at least once for every vertex. So exactly
`n` entries, each doing O(1) work on top of its loop: `Θ(n)`.

**Edges.** The body of `visit(u)` iterates over `adj[u]` once and does O(1) per
neighbour. Summing over all vertices, the total number of neighbour tests is
`Σ_u |adj[u]|`, which is `m` for a directed graph and `2m` for an undirected one
(each edge appears in two lists). So `Θ(m)`.

Total: **`Θ(n + m)`**, with the same bound as a recurrence if you prefer it:
`T(u) = c·(1 + deg(u)) + Σ_{children c} T(c)`, and summing that identity over the
DFS tree telescopes to `c·(n + Σ deg) = Θ(n + m)`.

Three corollaries people get wrong:

- **On an adjacency matrix it is `Θ(n²)`, not `Θ(n + m)`.** *Connected Groups*
  hands you an `N × N` symmetric matrix, so finding the neighbours of one vertex
  costs `N` regardless of how few there are. `Θ(N²)` is also optimal there, since
  you must read the matrix.
- **On a grid it is `Θ(R·C)`.** Cells are vertices, the four neighbours are the
  edges, so `n = RC` and `m ≤ 2RC`. *Flood Fill*, *Find Largest House Area* and
  *Count Islands with DFS and BFS* are linear in the number of cells.
- **A memoised DFS over a DAG is `Θ(n + m)` too**, because the memo is the mark:
  each state is expanded once. That is the whole identity between DFS and
  [[memoization]], and why *Reachable Nodes in a Directed Graph* is linear rather
  than path-counting.

**Space** is `Θ(n)` for the marks plus the depth of the recursion, which is the
length of the longest root-to-node path in the DFS tree — up to `n`. That second
term is not a footnote. Python's default recursion limit is 1000 frames; a
problem with `10⁵` vertices, and a grid whose free cells form a snake, will hit
it. Either raise the limit and the thread stack size, or write the loop with an
explicit stack. The iterative form in this chapter costs one tuple per vertex on
the stack — cheap, and it cannot blow up.

**The cost people forget** is the path list. Problems like *Root-to-Node Path in
a Binary Tree*, *Binary Tree Target-Sum Paths* and *Minimum-Sum Root-to-Leaf
Path* want the vertices along the current path. Passing `path + [u]` into each
call allocates a fresh list of length `d` at every node, giving `Θ(n·d)` time and
space, which on a degenerate tree is `Θ(n²)`. Push onto one shared list before
recursing and pop after, and the cost drops to `Θ(1)` per node — copy only when
you actually record an answer. Enumeration problems such as *DFS Subsequences of
a String* are exponential by nature, since the *output* has `2ⁿ` entries; that
cost belongs to the answer, not to the traversal.

## The implementation

The version worth owning is iterative, tracks colours and both timestamps, and
reports the back edges. Everything else in this chapter is a projection of it.

```python run
def dfs_forest(adj):
    """Iterative DFS over every vertex, in neighbour order.
    Returns tin, tout, the DFS-tree parent, and the edges into grey vertices."""
    n = len(adj)
    tin, tout, parent = [0] * n, [0] * n, [-1] * n
    state = [0] * n                      # 0 white, 1 grey (on the path), 2 black
    back, clock = [], 1
    for root in range(n):
        if state[root]:
            continue
        state[root], tin[root], clock = 1, clock, clock + 1
        stack = [(root, 0)]              # (vertex, neighbours already examined)
        while stack:
            u, i = stack.pop()
            if i < len(adj[u]):
                stack.append((u, i + 1))             # resume here afterwards
                v = adj[u][i]
                if state[v] == 0:
                    parent[v], state[v] = u, 1
                    tin[v], clock = clock, clock + 1
                    stack.append((v, 0))
                elif state[v] == 1:
                    back.append((u, v))              # grey: closes a cycle
            else:
                state[u], tout[u], clock = 2, clock, clock + 1
    return tin, tout, parent, back


adj = [[1, 2], [3], [1, 4], [0], [3], [4]]
tin, tout, parent, back = dfs_forest(adj)
print("tin ", tin, "\ntout", tout, "\nback edges", back)
assert tin == [1, 2, 6, 3, 7, 11] and tout == [10, 5, 9, 4, 8, 12]
assert back == [(3, 0)] and parent == [-1, 0, 0, 1, 2, -1]

# the parenthesis structure: intervals nest or are disjoint, never half-overlap
for u in range(6):
    for v in range(6):
        if u == v:
            continue
        a0, a1, b0, b1 = tin[u], tout[u], tin[v], tout[v]
        disjoint = a1 < b0 or b1 < a0
        nested = (a0 < b0 and b1 < a1) or (b0 < a0 and a1 < b1)
        assert disjoint or nested, (u, v)
print("intervals nest; 1 is an ancestor of 3:", tin[1] < tin[3] and tout[3] < tout[1])

chain = [[i + 1] for i in range(100000)] + [[]]      # a 100,001-vertex path
t_in, t_out, _, cyc = dfs_forest(chain)
print("depth-100001 chain: tin[last] =", t_in[-1], "back edges:", len(cyc))
assert t_in[-1] == 100001 and cyc == []
print("no RecursionError, because there is no recursion")
```

Three lines carry the weight.

`stack.append((u, i + 1))` before pushing the child is the whole trick of
turning recursion into a loop: the tuple *is* the stack frame, and `i` is the
program counter inside the neighbour loop. Pushing the parent back first and the
child second means the child is popped first, so neighbours are explored in
exactly the order a recursive version would take them. *Deterministic
Depth-First Graph Traversal* asks for a specified order, and this is how you
guarantee it; the naive "push all neighbours at once" form reverses them.

`elif state[v] == 1` is the cycle test, and it is an `elif` on purpose: white,
grey and black are three cases, not two. Replace `state` with a boolean `visited`
and you merge the last two, which makes every diamond look like a cycle.

`state[u], tout[u], clock = 2, clock, clock + 1` in the `else` branch is the
*post-order* moment — the instant when everything below `u` is known. Subtree
sums, heights, "is this subtree balanced", and low-link values are all computed
here, and nowhere else.

Here are the two shapes those post-order and grid projections take.

```python run
def subtree_totals(children, weight, root):
    """Post-order aggregate with no recursion: Employee Subordinates,
    Rocket Component Cost, Aggregate Machine Topology are all this."""
    total = [0] * len(children)
    stack = [(root, False)]                  # False = arriving, True = leaving
    while stack:
        u, leaving = stack.pop()
        if leaving:
            total[u] = weight[u] + sum(total[c] for c in children[u])
        else:
            stack.append((u, True))          # schedule the post-order visit
            for c in reversed(children[u]):
                stack.append((c, False))
    return total


children = [[1, 2], [3, 4], [5], [], [], []]
weight = [1, 10, 100, 2, 3, 5]
tot = subtree_totals(children, weight, 0)
print("subtree totals:", tot)
assert tot == [121, 15, 105, 2, 3, 5]


def island_sizes(grid):
    """Every maximal 4-connected blob of 1s, largest first. Flood Fill and
    Find Largest House Area are this with a different thing reported."""
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    sizes = []
    for r in range(R):
        for c in range(C):
            if grid[r][c] != 1 or seen[r][c]:
                continue
            seen[r][c], stack, size = True, [(r, c)], 0
            while stack:
                y, x = stack.pop()
                size += 1
                for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= ny < R and 0 <= nx < C and grid[ny][nx] == 1 \
                            and not seen[ny][nx]:
                        seen[ny][nx] = True          # mark on push, not on pop
                        stack.append((ny, nx))
            sizes.append(size)
    return sorted(sizes, reverse=True)


grid = [[1, 1, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 0, 1, 0, 0],
        [1, 0, 1, 1, 0]]
sizes = island_sizes(grid)
print("island sizes:", sizes, "-> islands:", len(sizes), " largest:", sizes[0])
assert sizes == [3, 3, 3, 1]
```

In `island_sizes`, `seen[ny][nx] = True` sits at the push, not at the pop. That
is not a style choice: it is the difference between each cell entering the stack
once and each cell entering it once per neighbour that points at it. The next
section shows what happens when the mark is taken away again on the way out.

## Variants you will meet

**Tree traversal.** Preorder, inorder and postorder are DFS on a tree with the
"do the work" line moved before, between or after the recursive calls.
*Binary Tree Preorder Traversal* gives the tree as a heap-indexed array, so the
children of `i` are `2i+1` and `2i+2` and there is no graph object at all. See
[[tree-traversal]], and [[morris-traversal]] for the O(1)-space version.

**Flood fill and grid DFS.** The graph is implicit: vertices are cells,
neighbours are the four or eight adjacent cells. [[flood-fill]], and
[[grid-bfs]] when the question turns to shortest.

**Connected components.** The outer loop plus a component id. Compare with
[[union-find]]: DFS wins when the graph is given once; union-find wins when the
edges arrive over time.

**Cycle detection.** Directed: an edge into a grey vertex. Undirected: an edge
into a visited vertex that is not the edge you arrived on. See
[[cycle-detection-graph]].

**Topological order by finishing time.** Reverse the order in which vertices
turn black. See [[topological-sort]].

**Backtracking.** DFS over a tree of *states* rather than of vertices, with the
mark undone on the way out. *DFS Subsequences of a String* is this: the state is
"which characters have I taken so far". See [[backtracking]], [[subsets]],
[[permutations]] and [[pruning]].

**Memoised DFS on a DAG.** Cache the answer for each vertex and you have
dynamic programming with the recursion written in the order you think in. See
[[memoization]] and [[tree-dp]].

**Low-link algorithms.** Keep, for each vertex, the smallest `tin` reachable by
going down tree edges and then up at most one back edge. That single extra number
gives bridges, articulation points and strongly connected components:
[[bridges-articulation]], [[strongly-connected]].

**Two-colouring.** Alternate a colour on every tree edge and check every non-tree
edge for a conflict: [[bipartite]].

**Euler tour / subtree flattening.** The pair `(tin, tout)` maps every subtree to
a contiguous range of the `tin` order, so "update a subtree, query a node" turns
into a range update on an array ([[fenwick-tree]], [[lca]]).

## Recognising it in a statement

In rough order of reliability:

1. **"Connected", "component", "group", "cluster", "island", "region".** The
   statement is asking for the partition into components, and DFS gives it in one
   pass. *Count Connected Components*, *Count Connected Point Clusters*, *Count
   Islands with DFS and BFS*.
2. **"Is there a path" / "can X reach Y" / "which nodes are reachable"**, with no
   mention of length or cost. *Directed Path Existence*, *Reachable Nodes in a
   Directed Graph*, *Binary Matrix Top-to-Bottom Reachability*.
3. **A per-node quantity defined in terms of everything below it** — count of
   subordinates, total cost of sub-components, depth, whether the subtree is
   balanced. That is the post-order slot. *Employee Subordinates*, *Rocket
   Component Cost*, *Balanced Tree Node Report*, *Maximum Depth of Binary Tree*.
4. **"All paths", "every subsequence", "list them in order".** Enumeration, so
   DFS with undo: *DFS Subsequences of a String*, *Binary Tree Target-Sum Paths*.
5. **A hierarchy given as parent pointers or a nesting, to be rendered or
   summed.** *Render a Stable Comment Hierarchy*, *Employee Subordinates*.
6. **The statement fixes the exploration order** ("visit the smaller-numbered
   neighbour first"). *Deterministic Depth-First Graph Traversal* — sort the
   adjacency lists and keep the iterative stack faithful to that order.
7. **`n` up to `10⁵` and the answer is structural.** Linear is the intended
   complexity, and DFS is the shortest linear traversal to write.

Anti-signals:

- **"Shortest", "minimum number of moves", "fewest", "nearest".** [[bfs]], or
  [[dijkstra]] with weights. DFS finds *a* path, not the short one.
- **"Level by level", "distance k from a node".** *All Nodes Distance K in a
  Binary Tree* uses DFS only to build parent pointers; the distance part is BFS.
- **Edges arriving over time, connectivity asked in between.** [[union-find]].
- **Depth possibly `10⁵` and a recursive solution.** Still DFS; just not
  recursive.

## Traps

**"Visited" is not "on the current path".** In a directed graph, meeting a
visited vertex means nothing on its own; meeting a *grey* one is a cycle. Symptom:
your cycle detector reports a cycle on a diamond `0→1→3, 0→2→3`, which is a DAG.
Demonstrated below.

**Clearing the mark on the way out.** A backtracking template pasted into a
reachability or counting problem visits one path instead of one vertex. Symptom:
correct answers that take exponential time, so the samples pass and the
submission times out. Its cousin — moving the mark *below* the neighbour loop —
is worse: on a cyclic graph the recursion never returns at all. Demonstrated
below.

**In an undirected graph, skipping the parent by vertex instead of by edge.**
Symptom: a graph with two parallel edges between the same pair — a genuine
2-cycle — is reported acyclic. Track the index of the edge you arrived on.

**Recursion depth.** Symptom: `RecursionError: maximum recursion depth exceeded`
at about 1000 frames, only on the large tests. A grid whose free cells form a
single snake, or a path graph, is the adversarial case.

**Rebuilding the path at every node.** `dfs(v, path + [v])` is `Θ(n·depth)`.
Push, recurse, pop, and copy only when you record an answer.

**Returning from inside the neighbour loop.** `return dfs(v)` on the first
neighbour abandons the rest of the loop. Write `if dfs(v): return True` when you
are searching for existence, and nothing at all when you are aggregating.

**Forgetting the outer loop, or the isolated vertices.** Symptom: the component
count is right on connected inputs and too low on sparse ones. *Connected Groups*
says explicitly that an isolated member is a group.

**Believing the first path found is the best one.** *Grid Pathfinding with
Obstacles (DFS)* is about existence. If a question asks for the shortest route,
DFS needs exhaustive search with undo, and BFS needs one pass.

```python run
# Trap 1: 'already visited' is not 'currently on the path'.
dag = [[1, 2], [3], [3], []]          # 0 -> 1 -> 3, 0 -> 2 -> 3: no cycle


def cycle_visited_only(adj):          # WRONG
    seen = set()

    def go(u):
        if u in seen:
            return True               # claims a cycle on any re-encounter
        seen.add(u)
        return any(go(v) for v in adj[u])

    return any(go(u) for u in range(len(adj)) if u not in seen)


def cycle_three_colours(adj):         # right
    state = [0] * len(adj)

    def go(u):
        state[u] = 1
        for v in adj[u]:
            if state[v] == 1 or (state[v] == 0 and go(v)):
                return True
        state[u] = 2
        return False

    return any(go(u) for u in range(len(adj)) if state[u] == 0)


print("diamond DAG - visited-only says cycle:", cycle_visited_only(dag))
print("diamond DAG - three colours say cycle:", cycle_three_colours(dag))
assert cycle_visited_only(dag) is True and cycle_three_colours(dag) is False
assert cycle_three_colours([[1], [2], [0]]) is True      # a real 3-cycle

# Trap 2: a mark that is cleared on the way out costs one visit per path.
n = 22
ladder = [[i + 1, i + 2] for i in range(n)] + [[], []]   # many walks 0 -> n+1
calls = [0, 0]


def keeps_the_mark(u, seen):           # DFS: one visit per vertex
    calls[0] += 1
    seen.add(u)
    for v in ladder[u]:
        if v not in seen:
            keeps_the_mark(v, seen)


def clears_the_mark(u, seen):          # backtracking template, wrong problem
    calls[1] += 1
    seen.add(u)
    for v in ladder[u]:
        if v not in seen:
            clears_the_mark(v, seen)
    seen.discard(u)                    # undo: u is white again for the next path


keeps_the_mark(0, set())
clears_the_mark(0, set())
print("vertices:", n + 2, " calls keeping the mark:", calls[0],
      " clearing it:", calls[1])
assert calls[0] == n + 2 and calls[1] > 100 * calls[0]
print("same reachable set, exponentially different work")
```

The first bug is wrong only on graphs that merge and re-merge; the second is
wrong only in the profiler. Neither shows up on a three-node example.

## What to memorise

One template, one sentence, one habit.

**The template**, recursive because that is what you will type under pressure,
with the three colours written in:

```python
state = [0] * n                 # 0 white, 1 grey (on the path), 2 black

def go(u):
    state[u] = 1
    # PRE-ORDER: what is true on the way in
    for v in adj[u]:
        if state[v] == 0:
            go(v)               # tree edge
        elif state[v] == 1:
            pass                # back edge -> cycle
        else:
            pass                # cross/forward edge -> nothing new
    state[u] = 2
    # POST-ORDER: everything below u is now known
```

And its iterative twin, for when depth can exceed a thousand: push `(u, 0)`, pop
`(u, i)`, re-push `(u, i+1)` then the child, and do the post-order work when
`i == len(adj[u])`.

**The sentence** that turns a problem into it: *"Is this question about what is
reachable, or about what is contained — rather than about how far?"* Reachable
and contained are DFS. How far is BFS.

**The habit**: *mark at the push, never at the pop, and never un-mark unless you
are deliberately backtracking*, and say out loud which of the two slots — pre-order or post-order — your answer belongs in. Nearly every
DFS bug is a mark in the wrong place or an aggregation in the wrong slot.

Numbers worth carrying: `Θ(V + E)` on an adjacency list, `Θ(V²)` on a matrix,
`Θ(RC)` on a grid; recursion depth up to `V`, against a default Python limit of
1000; a vertex's subtree is the contiguous `tin` range `[tin[u], tout[u]]`;
reverse finishing order is a topological order exactly when there are no back
edges.

## Check yourself

:::check
Why does an edge into a **grey** vertex prove a cycle, while an edge into a
**black** vertex proves nothing — given that both vertices have already been
seen?
--
Because grey means *unfinished*, and unfinished calls form a stack. If `v` is
grey when `visit(u)` examines `u → v`, then `visit(v)` is still on the call
stack, so it is an ancestor of `visit(u)`, and the active calls between them
spell an actual path `v ⇝ u` in the graph. Closing it with `u → v` gives a cycle.

If `v` is black, `visit(v)` has returned. It returned before `visit(u)` was even
entered or, at any rate, without `u` ever being on its path, so there is no
guaranteed `v ⇝ u` path — in the worked example `2 → 1` points at a finished
vertex and no cycle passes through it. The colour is not bookkeeping about the
past; it is a statement about the *present* call stack.
:::

:::check
Someone says: "DFS explores greedily as deep as possible, so if I keep a running
minimum over all the paths it finds, I get the shortest path — it is just BFS
with more code." Where are they wrong?
--
Two errors, one small and one fatal.

The small one: DFS with marks does not find "all the paths". It finds exactly one
path to each reachable vertex — the path in the DFS tree — because the second
time it meets a vertex it turns away. Taking a minimum over those gives the
minimum over one path per vertex, which is just that path's length.

The fatal one: to actually enumerate all paths you must clear the mark on the way
out, which is [[backtracking]], and then the number of paths can be exponential
in the number of vertices. A `10⁵`-vertex graph would need more steps than there
are atoms available. BFS is not "DFS with less code": it visits vertices in
non-decreasing distance order, which lets it stop at the first arrival and stay
linear. The orders are different, and only one of them is monotone in distance.
:::

:::check
You have `tin` and `tout` from one DFS. Give an O(1) test for "is `u` an
ancestor of `v` in the DFS tree", and say why it works.
--
`tin[u] < tin[v] and tout[v] < tout[u]` — the interval of `v` is strictly inside
the interval of `u`.

It works because of the parenthesis structure. `tin[x]` is written when `x`
becomes grey and `tout[x]` when it becomes black, and greys form a stack, so an
interval that opens while another is open must also close while the other is
still open. Hence for any two vertices the intervals are either disjoint or
properly nested, never crossing. Nesting is exactly the ancestor relation: `v`
was discovered during `visit(u)`, which happens precisely when `v` is reached
through `u`'s subtree.

This is what makes subtree queries into range queries: number the vertices by
`tin`, and `u`'s subtree is the contiguous block `[tin[u], tout[u]]`.
:::

:::check
Why is reverse finishing order a valid topological order on a DAG — and what
exactly goes wrong if the graph has a cycle?
--
Take any edge `u → v` and look at the moment it is examined, with `u` grey.
`v` is white, grey or black. White: DFS enters `v` now, so `v` finishes before
`u` does. Grey: that is a back edge, impossible in a DAG. Black: `v` finished
already, so again `tout[v] < tout[u]`. In both possible cases `tout[v] <
tout[u]`, so every edge points from a later-finishing vertex to an
earlier-finishing one, and listing vertices by decreasing `tout` puts every edge
left to right — the definition of a topological order.

With a cycle the grey case actually occurs, and for a back edge `u → v` we have
`tout[u] < tout[v]`, so that edge points backwards in the list. No ordering can
fix it: a cycle has no topological order at all. This is why the same traversal
that produces the order also produces the proof that one exists. See
[[topological-sort]].
:::

:::check
*Connected Groups* gives an `N × N` symmetric 0/1 matrix and asks for the number
of groups. A candidate writes DFS over the matrix and says it is `O(N + E)`
where `E` is the number of 1s. What is the real complexity, and is their
algorithm nevertheless optimal?
--
The real complexity is `Θ(N²)`. Finding the neighbours of a vertex in an
adjacency *matrix* means scanning a whole row of `N` entries, whether that row
holds one 1 or none, so the traversal does `N` work per vertex regardless of `E`.
`O(N + E)` is the adjacency-*list* bound, and the input is not a list.

It is nevertheless optimal, for a reason that has nothing to do with DFS: any
correct algorithm must read essentially the whole matrix. Flip one unread entry
from 0 to 1 and two groups may merge, changing the answer — so an algorithm that
skips entries can be forced to be wrong. `Θ(N²)` is a lower bound for the
problem, and DFS meets it. Building an adjacency list first would also cost
`Θ(N²)` and would not help.
:::
