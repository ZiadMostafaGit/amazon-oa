# Union-Find (Disjoint Set Union)

> Union-Find is not a graph algorithm. It is a way of maintaining an equivalence
> relation while it is still being built, so that "are these two things already
> the same thing?" stays cheap no matter how many merges have happened.

## When you reach for it

You reach for Union-Find when a problem hands you a pile of items and a stream
of statements of the form *these two belong together*, and then asks you
something about the resulting grouping.

The grouping is an **equivalence relation**: reflexive (everything is with
itself), symmetric (if `a` is with `b` then `b` is with `a`), transitive (if `a`
is with `b` and `b` is with `c` then `a` is with `c`). That third property is the
one that hurts. A statement that says "membership is transitive: members
connected through any chain of direct relationships belong to the same group" —
which is exactly how *Connected Groups* phrases it — is telling you that you
cannot process the pairs independently. Merging 2 with 3 can retroactively put 1
and 4 in the same group, and you are not allowed to rescan everything to notice.

Sixty-one problems in this bank use it, which puts it at #49 of 150. They fall
into a small number of shapes:

- **Count the groups** — *Count Connected Components*, *Count Friend Circles*,
  *Find Circle Number*.
- **Measure the groups** — *Get Sizes of Friends Groups*, *Largest Tree Size in a
  Forest*, *Product Category Group Sizes*.
- **Answer queries interleaved with merges** — *Path Existence in an Undirected
  Graph*; *Get Sizes of Friends Groups* alternates `Friend` (merge) with `Total`
  (ask).
- **Detect the redundant edge** — *Redundant Connection II*, *Minimum Connection
  Changes*: an edge whose endpoints are already together closes a cycle.
- **Merge records by shared keys** — *Accounts Merge*, *Group Linked Merchant
  Records*, *Sentence Equivalence with Synonyms*.
- **Find the moment things connect** — *Earliest Time All Users Are Connected*.

The tool is wrong when the question is not about equivalence. If you need the
*path* between two nodes, or its length, you need [[bfs]] or [[dijkstra]] —
Union-Find knows that two nodes are related and has forgotten how. If the graph
is directed, Union-Find will treat every edge as bidirectional and give you a
confidently wrong answer; you want [[strongly-connected]] or
[[topological-sort]]. And if edges are *removed* as well as added, merges being
irreversible by construction, the structure has no answer at all — unless you can
run time backwards, which is the last variant here and how *Counting Segments
After House Removals* is solved.

One honest anti-signal: if the graph is given once, in full, and you are asked a
single question about it at the end, a plain DFS or BFS is simpler and exactly as
fast. *Count Islands in a Binary Grid* is a legitimate Union-Find problem and
also a five-line [[flood-fill]]. Reach for Union-Find when the merges arrive
*over time* and the questions are interleaved with them — that is where the
alternative degrades to re-running a traversal after every edge.

## The idea

Give every group a **name**, and make the name be one of its members.

That is the whole trick. If each group has a designated representative, then
"are `a` and `b` in the same group?" becomes "do `a` and `b` have the same
representative?", which is a comparison of two values. The only work left is
finding your representative, and merging two groups into one.

So store a single array, `parent`, where `parent[x]` is some other member of
`x`'s group — a member that is, in a vague sense, "closer to the name". A
representative is a node that points at itself. Following `parent` from any node
therefore walks upward through a rooted tree and stops at the root, and the root
is the group's name. The array holds a **forest**: one tree per group.

Merging two groups is then a single write. Find both roots; make one point at
the other. Every member of the absorbed tree now reaches the new root by walking
one extra step, and no other memory has to change.

<svg viewBox="0 0 680 235" role="img" aria-label="two parent-pointer trees, and the result of hanging the smaller root under the larger">
  <g>
    <circle class="fill" cx="70" cy="45" r="18"/>
    <text x="70" y="51" text-anchor="middle">1</text>
    <circle cx="30" cy="115" r="18"/>
    <text x="30" y="121" text-anchor="middle">2</text>
    <circle cx="110" cy="115" r="18"/>
    <text x="110" y="121" text-anchor="middle">3</text>
    <circle cx="110" cy="185" r="18"/>
    <text x="110" y="191" text-anchor="middle">4</text>
    <line x1="40" y1="100" x2="62" y2="60"/>
    <line x1="106" y1="100" x2="78" y2="60"/>
    <line x1="110" y1="167" x2="110" y2="133"/>
    <text x="70" y="220" text-anchor="middle">size 4</text>
    <circle class="fill" cx="225" cy="45" r="18"/>
    <text x="225" y="51" text-anchor="middle">5</text>
    <circle cx="225" cy="115" r="18"/>
    <text x="225" y="121" text-anchor="middle">6</text>
    <line x1="225" y1="97" x2="225" y2="63"/>
    <text x="225" y="220" text-anchor="middle">size 2</text>
    <line x1="290" y1="115" x2="350" y2="115"/>
    <line x1="350" y1="115" x2="338" y2="108"/>
    <line x1="350" y1="115" x2="338" y2="122"/>
    <text x="320" y="100" text-anchor="middle">union</text>
    <circle class="fill" cx="480" cy="45" r="18"/>
    <text x="480" y="51" text-anchor="middle">1</text>
    <circle cx="410" cy="115" r="18"/>
    <text x="410" y="121" text-anchor="middle">2</text>
    <circle cx="480" cy="115" r="18"/>
    <text x="480" y="121" text-anchor="middle">3</text>
    <circle cx="555" cy="115" r="18"/>
    <text x="555" y="121" text-anchor="middle">5</text>
    <circle cx="480" cy="185" r="18"/>
    <text x="480" y="191" text-anchor="middle">4</text>
    <circle cx="555" cy="185" r="18"/>
    <text x="555" y="191" text-anchor="middle">6</text>
    <line x1="420" y1="100" x2="470" y2="60"/>
    <line x1="480" y1="97" x2="480" y2="63"/>
    <line x1="545" y1="100" x2="495" y2="60"/>
    <line x1="480" y1="167" x2="480" y2="133"/>
    <line x1="555" y1="167" x2="555" y2="133"/>
    <text x="480" y="220" text-anchor="middle">size 6, one write</text>
  </g>
</svg>

Here is the part that people miss, and it is the reason this structure is fast:
**the forest is not the graph**. It is a naming scheme. The edges of the input
graph are not stored anywhere; the tree shape is an artefact of the order the
merges happened in. Since nothing depends on the shape, we are free to rewrite it
however we like, as long as every node keeps reaching the same root.

That freedom buys two optimisations, and both are free to implement:

- **Union by size.** When merging, hang the *smaller* tree under the larger
  root. Nobody in the larger tree gets deeper.
- **Path compression.** Having walked from `x` up to root `r`, re-point the
  nodes you passed directly at `r`. The next walk from any of them is one step.

Neither is needed for correctness. Both together turn a potentially linear walk
into something indistinguishable from constant time.

## Worked by hand

Seven members, `0` through `6`, and six pairings. Union by size, with ties broken
by keeping the first root; path compression by *halving* (each node on the walk
is re-pointed at its grandparent). `comps` counts the groups.

Start: `parent = [0, 1, 2, 3, 4, 5, 6]`, every `size` is 1, `comps = 7`.

| step | operation | roots found | action | `parent` after | changed sizes | `comps` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | union(1, 2) | 1, 2 | tie, 2 under 1 | `[0,1,1,3,4,5,6]` | size[1] = 2 | 6 |
| 2 | union(3, 4) | 3, 4 | tie, 4 under 3 | `[0,1,1,3,3,5,6]` | size[3] = 2 | 5 |
| 3 | union(2, 3) | 1, 3 | tie (2 vs 2), 3 under 1 | `[0,1,1,1,3,5,6]` | size[1] = 4 | 4 |
| 4 | union(5, 6) | 5, 6 | tie, 6 under 5 | `[0,1,1,1,3,5,5]` | size[5] = 2 | 3 |
| 5 | union(0, 5) | 0, 5 | 1 < 2, so **0 under 5** | `[5,1,1,1,3,5,5]` | size[5] = 3 | 2 |
| 6 | union(1, 4) | 1, 1 | already together | `[5,1,1,1,1,5,5]` | — | 2 |

Final state: two groups, `{1, 2, 3, 4}` and `{0, 5, 6}`.

Four things in that table are worth a second look.

**Step 5 reversed the arguments.** We called `union(0, 5)`, and 5's root ended up
on top. Union by size does not care which argument you wrote first; it cares
which tree is bigger. If you want to know "the group containing 0", you must ask
`find(0)` — you may not assume 0 is still its own name.

**Step 6 changed `parent` without changing anything.** The roots were equal, so
no merge happened and `comps` stayed at 2 — yet `parent[4]` moved from 3 to 1,
because `find(4)` walked `4 → 3 → 1` and compression halved the path. The
structure reorganises itself during a read. A `find` is not a const operation.

**Step 6 is also the answer to a whole class of problems.** "The union did
nothing" means the edge `(1, 4)` connects two nodes that were already connected —
that is, it closes a cycle. *Redundant Connection II* and *Minimum Connection
Changes* are built on exactly this signal, and so is Kruskal's algorithm, which
skips an edge precisely when `union` reports no merge.

**The forest is not the input.** Try to recover the six pairs from the final
array. You cannot: the edge `(2, 3)` left no 2–3 link anywhere, since
`parent[2] = parent[3] = 1`. The structure has thrown the graph away and kept only
its partition into components — the honest boundary of the tool.

Here is what the compression in step 6 did, drawn:

<svg viewBox="0 0 640 190" role="img" aria-label="path compression flattening a chain of length two into two direct children of the root">
  <g>
    <circle class="fill" cx="90" cy="35" r="17"/>
    <text x="90" y="41" text-anchor="middle">1</text>
    <circle cx="45" cy="100" r="17"/>
    <text x="45" y="106" text-anchor="middle">2</text>
    <circle cx="135" cy="100" r="17"/>
    <text x="135" y="106" text-anchor="middle">3</text>
    <circle cx="135" cy="165" r="17"/>
    <text x="135" y="171" text-anchor="middle">4</text>
    <line x1="54" y1="86" x2="81" y2="50"/>
    <line x1="130" y1="86" x2="99" y2="50"/>
    <line x1="135" y1="148" x2="135" y2="117"/>
    <text x="90" y="185" text-anchor="middle">before find(4)</text>
    <line x1="230" y1="100" x2="300" y2="100"/>
    <line x1="300" y1="100" x2="288" y2="93"/>
    <line x1="300" y1="100" x2="288" y2="107"/>
    <text x="265" y="85" text-anchor="middle">find(4)</text>
    <circle class="fill" cx="470" cy="35" r="17"/>
    <text x="470" y="41" text-anchor="middle">1</text>
    <circle cx="395" cy="110" r="17"/>
    <text x="395" y="116" text-anchor="middle">2</text>
    <circle cx="470" cy="110" r="17"/>
    <text x="470" y="116" text-anchor="middle">3</text>
    <circle cx="545" cy="110" r="17"/>
    <text x="545" y="116" text-anchor="middle">4</text>
    <line x1="404" y1="95" x2="461" y2="50"/>
    <line x1="470" y1="93" x2="470" y2="52"/>
    <line x1="536" y1="95" x2="479" y2="50"/>
    <text x="470" y="185" text-anchor="middle">after: everyone one step from the name</text>
  </g>
</svg>

## Why it is correct

A data structure is correct when every operation preserves its representation
invariant and the invariant implies the answers it reports. So state the
invariant first, precisely, and then check the two operations against it.

:::proof The forest represents exactly the merges performed so far
**State.** Arrays `parent[0..n-1]` and `size[0..n-1]`, and a counter `comps`.
Let `E` be the multiset of pairs passed to `union` so far, and let `~E` be the
finest equivalence relation containing `E` — that is, `u ~E v` iff `u = v` or
there is a chain `u = x₀, x₁, …, x_k = v` with each consecutive pair in `E`.

**Invariant.** After any sequence of operations:

- **(I1)** Following `parent` from any node reaches, in finitely many steps, a
  node `r` with `parent[r] = r`. Equivalently: the functional graph of `parent`
  is a forest of rooted trees whose roots are self-loops.
- **(I2)** For all `u, v`: `root(u) = root(v)` if and only if `u ~E v`.
- **(I3)** For every root `r`, `size[r]` is the number of nodes in `r`'s tree,
  and `comps` is the number of roots.

**Base case.** After `__init__`, `parent[x] = x` for all `x`, so every node is
its own root and (I1) holds with zero steps. `E` is empty, so `~E` is equality,
and `root(u) = root(v)` iff `u = v`: (I2) holds. Every tree is a singleton,
`size[x] = 1`, and there are `n` roots with `comps = n`: (I3) holds.

**Step: `find(x)`.** By (I1) the walk terminates; define `depth(v)` as the number
of parent steps from `v` to its root, which is well defined and finite, and
strictly decreases with each step, so the loop runs exactly `depth(x)` times and
returns that root `r`. Compression then sets `parent[v] = r'` for some nodes `v`
on the walk, where `r'` is a proper ancestor of `v` (its grandparent, or the root
itself). This cannot create a cycle: an ancestor of `v` in a rooted tree has
strictly smaller depth, and a pointer from `v` to a strictly-shallower node keeps
the graph acyclic. So (I1) holds. Each moved `v` had root `r` before and has root
`r` after, and no other node's root changed, so the partition into trees is
unchanged and (I2) and (I3) hold. `E` did not change.

**Step: `union(a, b)`.** Let `ra = find(a)`, `rb = find(b)`, both roots by the
previous step. `E` gains the pair `(a, b)`, so the new relation `~E'` is `~E`
with the classes of `a` and `b` merged, and no other change.

*Case `ra = rb`.* By (I2), `a ~E b` already, so `~E' = ~E`. Nothing is written.
All three parts hold unchanged.

*Case `ra ≠ rb`.* By (I2) these are two distinct trees, and no node of `ra`'s
tree points into `rb`'s tree or vice versa. We write `parent[rb] = ra` (after
possibly swapping so that `size[ra] >= size[rb]`). Since `rb` was a root and now
points at a node of a different tree, the result is still a forest — we have
attached one whole tree below the root of another, creating no cycle. (I1) holds.
The set of nodes reaching `ra` is now the union of the two former trees, and every
other tree is untouched, so the new partition is exactly the old one with the
classes of `a` and `b` merged, which is `~E'`: (I2) holds. Finally
`size[ra] += size[rb]` makes `size[ra]` the count of the merged tree, `rb` is no
longer a root so its stale `size` is never read, one root disappeared, and
`comps -= 1` accounts for it: (I3) holds.

**Conclusion.** (I2) says `connected(u, v)` — implemented as
`find(u) == find(v)` — returns true exactly when `u` and `v` are joined by a
chain of the pairs supplied so far. When those pairs are the edges of an
undirected graph, that is precisely "`u` and `v` are in the same connected
component", and by (I3) `comps` is the number of components. ∎
:::

Now name what the proof leaned on, because that list is where the bugs live.

- **Only merges, never splits.** `~E` is the closure of the pairs supplied *so
  far*, and every operation only adds pairs, so the partition only gets coarser.
  Nothing in the argument survives an attempt to remove an edge.
- **`union` links roots, not elements.** The no-cycle and "two whole trees" steps
  both used the fact that `rb` was a root. Writing `parent[b] = ra` for a non-root
  `b` silently cuts `b` out of its old tree and breaks (I2).
- **`size` is read only at roots.** (I3) claims nothing else. `size[3]` after step
  3 of the trace is 2, which is not the size of anything.
- **`comps` is decremented only in the merging case.** The `ra = rb` case changes
  nothing; a decrement there breaks (I3) and nothing later repairs it.
- **Correctness never mentioned union by size or compression.** They enter the
  proof only as "possibly swapping" and "re-point at an ancestor" — shown to
  preserve the invariant, not to establish it. A Union-Find with neither heuristic
  is *correct*, only slow. If your answers are wrong, they are not the suspect.

## What it costs

Every operation is a walk up a tree plus O(1) writes, so the whole question is
**how tall can the trees get**. Answer it three times, for three levels of care.

**Neither heuristic.** Attach `rb` under `ra` always, no compression. Then
`union(0,1), union(1,2), union(2,3), …` builds a chain: after the `k`-th union a
`find` at the deep end costs `Θ(k)`, so `m` operations cost `Θ(mn)`. That is not a
pathological input you will never see; it is what a sorted edge list produces.

**Union by size alone.** Claim: every tree has height at most `log₂ n`.

The argument is a doubling count, and it is about a single node. Fix a node `v`
and let `S(v)` be the size of the tree containing it. `depth(v)` increases by
exactly 1 when the root above `v` is hung under another root — and union by size
does that only when the other tree is at least as large. So each time `depth(v)`
goes up by one, `S(v)` at least doubles. Initially `depth(v) = 0` and `S(v) = 1`;
at all times `S(v) <= n`. After `d` increments, `S(v) >= 2^d`, so `2^d <= n` and
`d <= log₂ n`. Every `find` is therefore `O(log n)`, worst case, deterministically
— no amortisation needed.

**Union by size and path compression.** The bound drops to nearly constant, and
the derivation is worth seeing once because "it is `O(α(n))`, trust me" teaches
nothing.

For this analysis use union by *rank* (link the shorter tree under the taller,
increment the winner's rank on a tie); union by size gives the same bounds, since
a root of rank `r` always has at least `2^r` nodes. Three facts:

1. Rank strictly increases along any `parent` pointer. Linking makes this true and
   compression preserves it, since it moves a node to an ancestor.
2. Once a node stops being a root, its rank is frozen. Only roots get incremented.
3. At most `n / 2^r` nodes ever reach rank `r`: such a node had `2^r` descendants
   when it got there, and those sets are disjoint across nodes of equal rank. So
   the maximum rank is at most `log₂ n`.

Now chop the ranks `0 … log₂ n` into blocks `(a, 2^a]`: `{0}`, `{1}`, `{2}`,
`{3, 4}`, `{5, …, 16}`, `{17, …, 65536}`, and so on. The number of blocks is
`log* n` — the number of times you take a logarithm before reaching 1 — which is
at most 5 for any `n` a computer can address.

Charge each step of each `find` walk to one of two accounts:

- If the node's parent lies in a **higher block**, charge the step to the
  operation. A walk crosses each block at most once, so this costs at most
  `log* n` per `find`.
- If the node's parent lies in the **same block**, charge the step to the node.
  After the walk, compression re-points that node at something strictly higher in
  rank. So each such charge strictly increases the node's parent's rank, and once
  that rank leaves the block the node can never be charged in this account again.
  A node whose rank is in block `(a, 2^a]` therefore absorbs at most `2^a`
  charges, and by fact 3 there are at most `Σ_{r > a} n/2^r <= n/2^a` such nodes.
  Total for the block: `n/2^a · 2^a = n`. Over `log* n` blocks: `O(n log* n)`.

So `m` operations cost `O((m + n) log* n)`. Tarjan's sharper analysis replaces
`log*` with the inverse Ackermann function `α(n)`, and he also proved a matching
lower bound for a restricted class of pointer-based algorithms — so this is not a
bound waiting to be improved. For every `n` you will ever run on, `α(n) <= 4`.
Treat a Union-Find operation as constant time and you will never be wrong by more
than a small factor.

**Space** is two integer arrays: `2n` words, plus the `comps` counter. No
recursion if you write `find` as a loop.

**The cost people forget** is the one outside the structure. Two of them:

- *Turning your objects into indices.* Union-Find works on `0 … n-1`. *Accounts
  Merge* and *Group Linked Merchant Records* hand you strings, which you must
  intern through a dictionary: an expected-O(1) hash per operation and a second
  structure to get wrong ([[hash-tables]]). On string-heavy inputs the hashing
  genuinely dominates the `α(n)`.
- *Sorting the edges.* Kruskal's Union-Find part is `O(E α(V))`; the sort is
  `O(E log E)` and is the real cost. See [[minimum-spanning-tree]].

## The implementation

```python run
import random


class DSU:
    """Disjoint sets over 0..n-1. Union by size, path halving."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # halve the path
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                   # already together
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra                                # smaller under larger
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def group_size(self, x):
        return self.size[self.find(x)]


d = DSU(7)
for a, b in [(1, 2), (3, 4), (2, 3), (5, 6), (0, 5)]:
    assert d.union(a, b) is True
print("parent after 5 merges:", d.parent, "-> components:", d.components)
assert d.components == 2
print("union(1, 4) merged anything?", d.union(1, 4), "(they were already one group)")
assert d.components == 2
print("group_size(4) =", d.group_size(4), " group_size(0) =", d.group_size(0))
assert d.group_size(4) == 4 and d.group_size(0) == 3
assert d.connected(2, 4) and not d.connected(2, 6)

rng = random.Random(7)
for _ in range(400):                       # cross-check against a DFS traversal
    n = rng.randint(1, 9)
    edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 12))]
    dsu, adj = DSU(n), [[] for _ in range(n)]
    for a, b in edges:
        dsu.union(a, b)
        adj[a].append(b)
        adj[b].append(a)
    comp, ncomp = [-1] * n, 0
    for s in range(n):
        if comp[s] < 0:
            stack, comp[s] = [s], ncomp
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if comp[v] < 0:
                        comp[v] = ncomp
                        stack.append(v)
            ncomp += 1
    assert dsu.components == ncomp, (n, edges)
    for u in range(n):
        for v in range(n):
            assert dsu.connected(u, v) == (comp[u] == comp[v]), (n, edges, u, v)
print("400 random graphs: counts and all pairwise queries match DFS")
```

Three lines carry the weight.

`self.parent[x] = self.parent[self.parent[x]]` is **path halving**: while walking
up, point each node at its grandparent. It compresses in a single pass, needs no
second loop and no recursion, and achieves the same `O(α(n))` amortised bound as
full two-pass compression. Prefer it. The recursive `find` that everybody writes
first — `return x if parent[x] == x else find(parent[x])` — is elegant and will
raise `RecursionError` on a chain of a hundred thousand nodes before compression
has had a chance to flatten it.

`if self.size[ra] < self.size[rb]: ra, rb = rb, ra` is the entire union-by-size
heuristic, written as a swap so that the code after it does not need to branch.
Note that it is a swap of *roots*, not of the original arguments — the caller's
`a` and `b` have already served their purpose.

`return False` when the roots coincide is the most useful line in the class. It
keeps `components` honest and it is a free answer to "is this edge redundant?",
"does it create a cycle?" and "should Kruskal take it?". Always return the bool,
and update every counter from it rather than from the loop.

## Variants you will meet

**Union by rank instead of size.** Same asymptotics, one less useful number. Use
size: `group_size` comes free, and *Get Sizes of Friends Groups* and *Largest Tree
Size in a Forest* ask for it directly. Compression with no union heuristic at all
is correct and amortised `O(log n)` — acceptable, but the heuristic is two lines.

**Extra data hung on the root.** Anything that is a commutative, associative
aggregate over a set can live at the root and be combined during `union`: the
size, the minimum or maximum element, a count of edges (used by *Count the Number
of Complete Components*, where a component with `k` nodes is complete iff it has
`k(k-1)/2` edges), a sum, a parity. Merge it in the same place you merge `size`.

**Small-to-large merging of collections.** When the aggregate is a set and cannot
be combined in O(1), merge the smaller collection into the larger. Each element
moves only when its collection at least doubles, so it moves `O(log n)` times,
`O(n log n)` in total. That is how you keep the real member lists for *Accounts
Merge* or *Group Transitive String Aliases*.

**Kruskal's minimum spanning tree.** Sort the edges by weight; take an edge iff
`union` returns `True`. The `True` is the cycle test. See
[[minimum-spanning-tree]], and the [[greedy-exchange|exchange argument]] that
proves it optimal.

**Grid connectivity.** Map cell `(r, c)` to `r * cols + c` and union with the
neighbours already filled. *Number of Islands II* — add land one cell at a time
and report the island count after each addition — is the problem this variant
exists for, and the case where re-running [[flood-fill]] each time is too slow.

**Parity / weighted DSU.** Store, alongside `parent[x]`, the relation between `x`
and its parent — a parity bit, an offset, a ratio. `find` accumulates it along the
path and compression rewrites it relative to the root. A parity bit decides
2-colourability incrementally ([[bipartite]]); an integer offset answers "how much
more than `b` is `a`?" under merging constraints.

**"Next free slot" on a line.** Set `parent[i]` to the next index at or after `i`
that is still available; taking slot `i` sets `parent[i] = i + 1`. Each `find`
then jumps straight past a run of taken slots, and the total cost of `n`
assignments is near-linear. *Bus Station Seat Allotment* and *Doctor Appointment
Slot Assignment* are this pattern, not the connectivity pattern.

**Rollback DSU.** Drop path compression, keep union by size (height stays
`O(log n)`), and push each `(rb, ra, old_size)` onto a stack so a union can be
undone. Compression has to go because it destroys the information needed to undo.
This is the ingredient for offline dynamic connectivity ([[persistent-structures]]).

**Time reversed.** Deletions are impossible going forwards and trivial going
backwards. If all the deletions are known in advance, start from the final state
and add things back.

```python run
def segments_after_removals(n, removals):
    """Houses 0..n-1 all stand; removals[k] demolishes one. After each removal,
    how many contiguous runs of standing houses remain? Deletion is impossible
    in a DSU, so build the final state and replay time backwards."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    alive = [True] * n
    for h in removals:
        alive[h] = False

    segs = 0                                   # the state after every removal
    for i in range(n):
        if alive[i]:
            segs += 1
            if i and alive[i - 1]:
                parent[find(i - 1)] = i        # i is a fresh root; merge left
                segs -= 1

    ans = [0] * len(removals)
    for k in range(len(removals) - 1, -1, -1):
        ans[k] = segs                          # state after removals[0..k]
        h = removals[k]                        # put it back to reach state k-1
        alive[h], segs = True, segs + 1
        for nb in (h - 1, h + 1):
            if 0 <= nb < n and alive[nb]:
                ra, rb = find(h), find(nb)
                if ra != rb:
                    parent[rb] = ra
                    segs -= 1
    return ans


def brute(n, removals):
    alive, out = [True] * n, []
    for h in removals:
        alive[h] = False
        out.append(sum(1 for i in range(n) if alive[i] and (i == 0 or not alive[i - 1])))
    return out


print("n=8, remove 3,5,0,6 ->", segments_after_removals(8, [3, 5, 0, 6]))
print("brute force         ->", brute(8, [3, 5, 0, 6]))

import random
rng = random.Random(11)
for _ in range(300):
    n = rng.randint(1, 10)
    order = list(range(n))
    rng.shuffle(order)
    rem = order[:rng.randint(0, n)]
    assert segments_after_removals(n, rem) == brute(n, rem), (n, rem)
print("300 random removal schedules agree with the O(n*m) recount")
```

## Recognising it in a statement

Ordered by how much you should trust them.

1. **The word "transitive", or a chain of "friends of friends".** *Connected
   Groups* says membership is transitive in so many words; *Group Transitive
   String Aliases* puts it in the title. As close to a giveaway as statements get.
2. **Merges and questions interleaved.** "queryType is either `Friend` or
   `Total`" in *Get Sizes of Friends Groups*. Offline you could traverse; online
   you cannot.
3. **"How many groups / circles / clusters / components"** with edges given as
   pairs — *Count Friend Circles*, *Find Circle Number*, *Count Connected Point
   Clusters*.
4. **"Minimum edges to connect everything."** The answer is always
   `components - 1`, and the only work is counting components. *Minimum Edges to
   Connect All Components* is literally this.
5. **An `n × n` symmetric 0/1 matrix of relations** — an adjacency matrix in
   disguise, and symmetric means equivalence.
6. **"Earliest time at which everything is connected."** Sort the events by time,
   union in order, stop when `components == 1` and report that timestamp.
   *Earliest Time All Users Are Connected* and *Earliest Time of Full Connection*.
   Note you do *not* need [[binary-search-on-answer]] here — one pass suffices,
   because the components counter is monotone.

The anti-signals:

- **Directed edges.** Union-Find cannot represent one-way relations. If the
  statement says "a follows b" and does not say the relation is symmetric, stop.
- **Deletions arriving online.** If an edge can be removed and you do not know the
  removals in advance, this structure is the wrong shape. Look for a rollback or
  time-reversal formulation, or a different structure entirely.
- **Anything about distances or paths.** "Shortest", "fewest steps", "the route" —
  that is [[bfs]] or [[dijkstra]]. The classic near-miss is *Minimum Score of a
  Path Between Cities*, which sounds like a path problem and is really "the
  minimum edge weight in the component containing city 1" — the Union-Find part is
  finding the component, and the "path" is a red herring.
- **One static graph, one question.** Use [[dfs]]; it is shorter.

## Traps

**Linking an element instead of a root.** `parent[b] = find(a)` looks fine and
quietly splits `b` away from its old group. Symptom: the component counter and
the actual number of distinct roots disagree, and pairs that should be connected
are not. Demonstrated below.

**Decrementing the counter unconditionally.** Symptom: the count is too low,
sometimes zero or negative, and only on inputs that contain a redundant edge — so
the sample cases pass. Demonstrated below.

**Recursive `find` on deep input.** Symptom: `RecursionError` at around 1000
frames in Python, a stack overflow elsewhere, and only on adversarial inputs like
a chain of unions in index order.

**Reading `size[x]` instead of `size[find(x)]`.** Symptom: sizes that are too
small and never change after a node stops being a root.

**Caching a root.** `r = dsu.find(x)`, used later, is wrong: the next union can
make `r` a non-root. Symptom: wrong answers that depend on merge order. Roots are
not stable names; only `find` is.

**Off-by-one on the universe.** *Get Sizes of Friends Groups* numbers students
`1` to `n`. Allocate `n + 1` slots and ignore index 0, or subtract one everywhere
— but pick one and be consistent. Symptom: exactly one extra component, every
time.

**Forgetting the isolated elements.** "Every member belongs to exactly one group,
including an isolated member" — a node with no edges is a component. Build the DSU
from `n`, not from the edge list. Symptom: the count is right on dense inputs and
low on sparse ones.

**Assuming the structure remembers edges.** It does not. Keep adjacency
separately if you need it.

```python run
def find(p, x):
    while p[x] != x:
        p[x] = p[p[x]]
        x = p[x]
    return x


def run(n, edges, link_roots, guard):
    p, comps = list(range(n)), n
    for a, b in edges:
        ra, rb = find(p, a), find(p, b)
        if ra == rb and guard:
            continue                       # correct: no merge, no decrement
        p[rb if link_roots else b] = ra    # bug 1 writes through the element
        comps -= 1
    roots = len({find(p, x) for x in range(n)})
    return comps, roots


# A: 5 nodes, edges make {0,1,2,3} and {4}. Truth: 2 components.
n, edges = 5, [(0, 1), (2, 3), (0, 3)]
print("A  counter, distinct roots")
print("   correct        ", run(n, edges, True, True))
print("   linking element", run(n, edges, False, True), "<- counter and forest disagree")
assert run(n, edges, True, True) == (2, 2)
assert run(n, edges, False, True) == (2, 3)      # the forest lost the 2-3 link

# B: a triangle plus two loners. Truth: 3 components; edge (0,2) is redundant.
n, edges = 5, [(0, 1), (1, 2), (0, 2)]
print("B  counter, distinct roots")
print("   correct        ", run(n, edges, True, True))
print("   always counting", run(n, edges, True, False), "<- one too few, silently")
assert run(n, edges, True, True) == (3, 3)
assert run(n, edges, True, False) == (2, 3)
print("both bugs are invisible until an input contains a redundant edge")
```

In case A the counter says 2 while the forest holds 3 roots: the structure
contradicts itself, which is the cleanest possible symptom and the reason
`comps == len({find(x) for x in range(n)})` is worth asserting in a test. In case
B the forest is right and the counter is wrong. Two different bugs, and the final
number alone cannot tell them apart.

## What to memorise

The template, which should come out of your fingers without thought:

```python
parent = list(range(n))
size = [1] * n
comps = n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    global comps
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    comps -= 1
    return True
```

The sentence that turns a problem into it: *"Am I being told, one pair at a time,
that two things are the same, and asked about the resulting grouping?"* If the
relation is symmetric and only ever grows, the answer is yes.

The habit: **let `union` return a bool, and update every counter from that bool.**
Component counts, Kruskal's edge selection, redundant-edge detection and cycle
detection are all the same `if union(a, b):`. A counter maintained anywhere else
will eventually be maintained wrongly.

Numbers worth carrying: union by size alone caps height at `log₂ n`; with
compression the amortised cost is `α(n) <= 4` for any real `n`, so call it
constant; connecting `c` components needs exactly `c - 1` edges; a complete
component on `k` nodes has `k(k-1)/2` edges.

## Check yourself

:::check
Path compression rewrites `parent` during a `find`, which is supposed to be a
read. Why does that not corrupt the structure — and what property of the
representation makes it safe?
--
Because `parent` is a *naming scheme*, not a record of the input. The invariant
claims only that (I1) it is a forest and (I2) two nodes reach the same root
exactly when they have been merged. Compression re-points `v` at a proper
ancestor: same tree, same root, so (I2) is untouched; and a pointer to a strictly
shallower node cannot create a cycle, so (I1) is untouched.

What makes it safe is that the tree *shape* is not part of the specification. Any
forest with the right partition into trees represents the same state. That is why
we are free to pick the shape that is fastest — and also why rollback DSU must
switch compression off: once you have thrown the old shape away, you cannot
restore it.
:::

:::check
Someone says: "I can't use `union` without union by size — without it the
structure gives wrong answers on large inputs." Where are they wrong, and what is
the correct version of their worry?
--
They have merged correctness and performance. The proof of the invariant never
used union by size; it only needed `union` to link two *roots* of two *different*
trees. A DSU that always writes `parent[rb] = ra` returns exactly the same answers
as one that compares sizes first. Only the running time differs.

The correct worry: without either heuristic the trees can become chains, and a
`find` costs `Θ(n)`, so `m` operations cost `Θ(mn)` — on 10⁵ unions in index
order that is 10¹⁰ steps, a timeout, not a wrong answer. Diagnosing a timeout and
diagnosing a wrong answer send you to different lines of code, which is exactly
why the distinction is worth keeping.
:::

:::check
*Minimum Edges to Connect All Components* asks for the fewest edges needed to make
the whole graph connected. Why is the answer `components - 1`, and why is it
always achievable?
--
**Lower bound.** Adding one edge merges at most two components, so it reduces the
component count by at most one. Starting at `c` and needing to reach 1 requires at
least `c - 1` additions. (This is invariant (I3) read as a potential function:
`comps` drops by 0 or 1 per edge, never more.)

**Achievability.** Pick any representative from each component and chain them:
`r₁–r₂`, `r₂–r₃`, …, `r_{c-1}–r_c`. Each of those `c - 1` edges joins two
components that were distinct at that moment, so each one does reduce the count by
exactly one, ending at 1.

So the whole problem reduces to counting components, which is one pass of
`union` over the given edges and then reading `comps`.
:::

:::check
A colleague wants to remove node `v` from its group and says "easy — just set
`parent[v] = v` again". Where are they wrong?
--
In at least two places.

First, if `v` is not a root, its group does not lose `v`'s subtree: every
descendant of `v` still walks up through `v`, and they all now land on the new
root `v`. So the operation silently splits off an arbitrary set of nodes — whichever
ones happened to be below `v`, which depends on merge order and on which `find`s
have compressed which paths. It is not even deterministic from the input.

Second, and more fundamentally, the structure does not store the edges. Removing
`v` should leave the *remaining* nodes grouped according to the remaining edges,
and the DSU has no idea what those edges are. There is no local fix, which is why
deletion problems are handled by reversing time (*Counting Segments After House
Removals*) or by a rollback DSU over a divide-and-conquer on the timeline.
:::

:::check
You have `n` users and a list of `(u, v, t)` friendship events. Give an algorithm
for the earliest time at which every user is connected to every other, and justify
the stopping rule.
--
Sort the events by `t`, feed them to a DSU in that order, and return the `t` of
the first event whose `union` returns `True` and leaves `components == 1`. If the
list runs out with `components > 1`, report that it never happens.

The stopping rule is justified by monotonicity: `components` never increases,
because `union` either does nothing or decreases it by one. So the set of prefixes
whose graph is connected is upward-closed, and the first prefix reaching
`components == 1` is the earliest. No binary search is needed — the single pass
visits every candidate in order at O(α(n)) each, and the sort dominates at
`O(E log E)`. This is *Earliest Time All Users Are Connected*.
:::
