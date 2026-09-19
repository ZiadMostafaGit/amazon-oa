# Trees: Vocabulary and Shapes

> A tree is the promise that between any two nodes there is exactly one path.
> Every convenience trees give you — recursion with no visited set, a parent
> array, a subtree you can reason about on its own — is that one promise being
> spent.

## When you reach for it

You do not usually choose a tree; a tree is handed to you. Two hundred and
twenty-seven problems in this bank use this topic, which makes it #16 of 150, and
they are hardly ever disguised — *Maximum Depth of Binary Tree* and *Binary Tree
Right View* say it in the title.

What you do choose is the *representation* and the *direction of information
flow*. Before you can write [[tree-traversal|a traversal]], [[bst|a BST search]]
or [[tree-dp|a tree DP]] you need three kinds of fluency: the vocabulary, since
every statement is written in it and the words are not interchangeable; the
handful of forms a tree arrives in, since the same problem is three lines or
twenty depending on which one you get; and the structural facts that make tree
algorithms work at all — `n - 1` edges, unique paths, disjoint subtrees.

The shape that makes this the right tool: **each item has exactly one parent,
there are no cycles, and the question is about ancestry, depth, or an aggregate
over a subtree.** The hierarchy is often implicit — *Employee Subordinates* is a
table with a manager column, *Flat Comments to a Nested Tree* is a tree that
arrives flat and must be assembled before anything else can happen.

The shape that makes it the wrong tool is a node with two parents. Then you have
a DAG: subtrees overlap, recursion revisits nodes, and the whole edifice below
falls over. That is [[graphs]] territory, and its fixes — a visited set,
[[topological-sort]], memoisation — all repair exactly the property a tree gives
free. A "tree" with a cycle is worse still: a graph with a wishful name, which is
partly why *Create a Binary Tree from Parent-Child Descriptions* exists.

One more non-trigger: if the question is purely about distances between
arbitrary pairs, do not reflexively root the tree — *Distance Between Two Tree
Nodes* wants [[lca|an LCA]], and the rooting is scaffolding you may not need.

## The idea

Here is the mental image, and it is recursive on purpose:

**A tree is a node, plus a list of trees hanging off it.**

That is the whole definition. The node is the root; the list is its children,
each itself the root of a tree. Nothing there mentions two children, so it
defines N-ary trees natively; binary trees are the case where the list has length
at most 2, and a **forest** is the list itself with no node on top — the plural
of tree. *Maximum Depth of an N-ary Tree*, *Canonical N-Ary Tree Codec* and *Get
Components in Forest* are this definition with a different arity or no root.

The image to hold is below: levels going down, exactly one line into each node
from above, and any node you point at being itself the root of a smaller copy of
the same picture.

<svg viewBox="0 0 660 265" role="img" aria-label="a rooted tree of six nodes showing root, internal nodes, leaves, depth levels and the subtree of one node">
  <g>
    <line x1="291" y1="55" x2="209" y2="95"/>
    <line x1="309" y1="55" x2="391" y2="95"/>
    <line x1="191" y1="125" x2="149" y2="167"/>
    <line x1="209" y1="125" x2="246" y2="167"/>
    <line x1="400" y1="128" x2="400" y2="167"/>
    <rect x="352" y="80" width="98" height="130" rx="8" stroke-dasharray="5 5"/>
    <circle class="fill" cx="300" cy="40" r="18"/>
    <text x="300" y="46" text-anchor="middle">A</text>
    <circle cx="200" cy="112" r="18"/>
    <text x="200" y="118" text-anchor="middle">B</text>
    <circle cx="400" cy="112" r="18"/>
    <text x="400" y="118" text-anchor="middle">C</text>
    <circle cx="140" cy="185" r="18"/>
    <text x="140" y="191" text-anchor="middle">D</text>
    <circle cx="255" cy="185" r="18"/>
    <text x="255" y="191" text-anchor="middle">E</text>
    <circle cx="400" cy="185" r="18"/>
    <text x="400" y="191" text-anchor="middle">F</text>
    <text x="300" y="16" text-anchor="middle">root</text>
    <text x="45" y="46">depth 0</text>
    <text x="45" y="118">depth 1</text>
    <text x="45" y="191">depth 2</text>
    <text x="140" y="222" text-anchor="middle">leaf</text>
    <text x="255" y="222" text-anchor="middle">leaf</text>
    <text x="400" y="222" text-anchor="middle">leaf</text>
    <text x="470" y="150">subtree of C</text>
    <text x="45" y="250">6 nodes, 5 edges, height 2</text>
  </g>
</svg>

### The vocabulary, tightened

Sloppiness here is the source of a disproportionate number of wrong answers, so
be exact.

| word | meaning | in the picture |
| --- | --- | --- |
| root | the node with no parent | A |
| parent / child | adjacent, one level apart | B is the parent of D |
| siblings | same parent | D and E |
| ancestor / descendant | anywhere above / below on the path to the root | A is an ancestor of F |
| leaf | no children | D, E, F |
| internal node | at least one child | A, B, C |
| depth of `v` | number of **edges** from the root down to `v` | depth(E) = 2 |
| height of `v` | number of edges on the longest path from `v` down to a leaf | height(B) = 1 |
| height of the tree | height of the root | 2 |
| size of `v` | number of nodes in `v`'s subtree, including `v` | size(B) = 3 |
| level `k` | all nodes at depth `k` | level 1 is {B, C} |
| degree | number of children (in a rooted tree) | degree(A) = 2 |
| forest | a set of disjoint trees | remove A and you have two |

Two of those deserve a warning. **Depth and height are not the same number read
from opposite ends**: depth is a fact about a node's *ancestry*, height about its
*subtree*. Node C has depth 1 and height 1 here by coincidence.

And the counting convention is a live hazard. This chapter counts edges, so a
lone node has depth 0. Many statements count *nodes* — *Maximum Depth of an
N-ary Tree* says outright that "the root alone has depth 1". Neither convention
is right; the one in the statement is.

### The five ways a tree arrives

The tree is the same object each time; what changes is how much work you do
first.

1. **Linked nodes.** A `Node` with `left`/`right`, or `val`/`children`. Follow
   pointers from the root.
2. **Parent array.** `parent[i]` is `i`'s parent, `-1` at the root. *Maximum
   Depth of an N-ary Tree* hands you exactly this: cheap upward moves, no
   downward moves until you invert it.
3. **Children lists.** `children[i]`, left to right, as in *Nodes at a Given
   N-ary Tree Level*. The inverse of the parent array, and the form almost every
   algorithm wants.
4. **Edge list.** Pairs `[parent, child]`, or undirected pairs plus "rooted at
   0". You build the adjacency, and sometimes find the root — that is the whole
   job in *Find the Root of a Directed Tree*.
5. **Heap-indexed array.** Children of `i` at `2i + 1` and `2i + 2`, a sentinel
   for missing nodes. *Binary Tree Preorder Traversal* is posed this way, with
   `-1` meaning absent: no pointers at all, and no tolerance for skewed trees.

Converting between them is mechanical and is the first three lines of a great
many solutions. Converting *to* form 3 is usually right.

## Worked by hand

Take `parent = [-1, 0, 0, 1, 1, 2]` over nodes `0..5`. Inverted, that is
`children = [[1, 2], [3, 4], [5], [], [], []]` with root 0 — the tree in the
diagram, with A..F renamed 0..5. Walk it depth-first, writing down every *entry*
into a node and every *exit* from it.

| step | event | node | stack after | what becomes known |
| --- | --- | --- | --- | --- |
| 1 | enter | 0 | `[0]` | depth(0) = 0 |
| 2 | enter | 1 | `[0,1]` | depth(1) = 1 |
| 3 | enter | 3 | `[0,1,3]` | depth(3) = 2 |
| 4 | exit | 3 | `[0,1]` | height(3) = 0 (leaf) |
| 5 | enter | 4 | `[0,1,4]` | depth(4) = 2 |
| 6 | exit | 4 | `[0,1]` | height(4) = 0 |
| 7 | exit | 1 | `[0]` | height(1) = 1 + max(0, 0) |
| 8 | enter | 2 | `[0,2]` | depth(2) = 1 |
| 9 | enter | 5 | `[0,2,5]` | depth(5) = 2 |
| 10 | exit | 5 | `[0,2]` | height(5) = 0 |
| 11 | exit | 2 | `[0]` | height(2) = 1 |
| 12 | exit | 0 | `[]` | height(0) = 1 + max(1, 1) = 2 |

Final: `depth = [0, 1, 1, 2, 2, 2]`, `height = [2, 1, 1, 0, 0, 0]`.

Three things in that table are worth more than the code that produced it.

**Every node has exactly one enter and exactly one exit.** Twelve events, six
nodes, no visited set anywhere. That is not the code being careful; it is the
structure guaranteeing it, and the proof below is the guarantee.

**Depth flows down, height flows up.** `depth(c)` is known the instant you step
into `c`, from information you carried with you; `height(v)` is unknown until
every child has *finished*. This split is the most useful thing in the chapter.
Ask about a node's position in the hierarchy — *Check Whether All Leaves Are at
the Same Level*, *Tree Node Relationship*, *Binary Tree Right View* — and the
information travels down as an argument. Ask about its subtree —
*Leaf-to-Leaf Binary Tree Diameter*, *Maximum Sum of Non-Adjacent Tree Nodes* —
and it travels up as a return value. Need both, and one walk carries a parameter
down and a value up, which is exactly [[tree-dp]].

**The stack never held more than three nodes.** Not six. It holds one node per
level of the current path, so its peak is `height + 1` — about 17 frames for a
balanced tree of a hundred thousand nodes, a hundred thousand for a chain, and
Python stops you at about a thousand. Note too that node 2 has height 1 while the
tree has height 2: height is local to a subtree, and if you compute it with a
global variable you have confused it with depth.

## Why it is correct

Nothing above is an algorithm, so there is no loop invariant to state. What
needs proving is the *structure* — the facts that every tree algorithm in every
later chapter quietly assumes. They are not obvious, and the last of them is the
reason tree DFS needs no visited set.

:::proof A finite connected acyclic graph has unique paths, `n - 1` edges, and disjoint subtrees under any rooting
**Setup.** Let `G = (V, E)` be a finite undirected graph with `|V| = n >= 1`,
**connected** (some path joins every pair) and **acyclic** (no simple cycle).
Call such a `G` a tree.

**Claim 1 — between any `u, v` there is exactly one simple path.**
Existence is connectivity. For uniqueness, suppose `P ≠ Q` are simple `u`–`v`
paths, and let `x` be the last vertex where they still agree; they leave `x` by
different edges (if one were a prefix of the other, the longer would visit `v`
twice). Walk along `P` from `x` until you first hit a vertex that also lies on
`Q` after `x`; call it `y`, which exists because `v` qualifies. The `x`-to-`y`
sections of `P` and `Q` share only their endpoints and leave `x` differently, so
they are not both the single edge `x–y`; their union is a closed walk with at
least three distinct vertices and no repeats — a simple cycle. Contradiction.

**Claim 2 — if `n >= 2`, some vertex has degree 1 (a leaf exists).**
`G` is finite, so among all simple paths there is a longest, `v₀, …, v_k`, with
`k >= 1` by connectivity. Let `w` be a neighbour of `v_k`. If `w` is off the
path, `v₀, …, v_k, w` is a longer simple path — impossible. So `w = v_j`, and if
`j < k - 1` then `v_j, …, v_k, v_j` is a simple cycle — impossible. Hence
`w = v_{k-1}` is the only neighbour and `deg(v_k) = 1`.

**Claim 3 — `|E| = n - 1`.** Induction on `n`. *Base:* `n = 1`; acyclic forbids
self-loops, so `|E| = 0`. *Step:* take a leaf `ℓ` from Claim 2 and set
`G' = G - ℓ`. `G'` is acyclic, being a subgraph, and connected, since for
`u, v ≠ ℓ` the unique `u`–`v` path cannot pass *through* `ℓ` — passing through a
vertex uses two edges at it and `ℓ` has one. So `G'` is a tree on `n - 1`
vertices with `n - 2` edges, and `|E| = (n - 2) + 1 = n - 1`.

**Claim 4 — rooting is well defined and the parent walk terminates.**
Fix any `r ∈ V`. For `v ≠ r` define `parent(v)` as the second vertex on the
unique path from `v` to `r`, and `d(v)` as that path's length. Deleting the first
edge of that path leaves a simple path from `parent(v)` to `r`, which by Claim 1
*is* the unique such path; hence `d(parent(v)) = d(v) - 1`. So `d` strictly
decreases along parent pointers, the walk from any `v` reaches `r` in exactly
`d(v)` steps, and no cycle of parent pointers can exist. Each edge `{a, b}` is a
parent pair in exactly one direction: prefixing the `b`-to-`r` path with the edge
`a–b` either gives a simple path, so `parent(a) = b`, or repeats `a`, in which
case that path already contains `a`, its `b`-to-`a` prefix is by Claim 1 the edge
itself, and `parent(b) = a`. So the `n - 1` edges are exactly the `n - 1` pairs
`(v, parent(v))`: **a parent array is a complete description of a rooted tree, no
more and no less.**

**Claim 5 — subtrees of distinct children are disjoint, and a recursion over
children visits each node exactly once.** Define `subtree(v)` as the set of `u`
whose parent walk passes through `v`. Let `c₁ ≠ c₂` be children of `v` and
suppose `u ∈ subtree(c₁) ∩ subtree(c₂)`. The parent walk from `u` is a single
deterministic sequence with strictly decreasing `d`, so it visits `v` once and
arrives there from exactly one vertex — `c₁` or `c₂`, not both. Contradiction.
Hence `{v}` and the sets `subtree(c)` partition `subtree(v)`. Now induct on
`|subtree(v)|`: a call at a leaf makes 1 call; a call at `v` makes 1 plus
`|subtree(c)|` calls per child by the induction hypothesis, totalling
`1 + Σ_c |subtree(c)| = |subtree(v)|`. The recursion terminates, and from the
root it makes exactly `n` calls. ∎
:::

Now say plainly what that argument leaned on, because that list is where the
bugs live.

- **Finiteness.** Claim 2 picked a *longest* path, which needs a finite graph,
  and everything after it depends on Claim 2.
- **Connected *and* acyclic.** Claim 3 runs one way only. Four nodes with the
  three edges of a triangle plus a loner also have `n - 1` edges and are not a
  tree, so `len(edges) == n - 1` proves nothing on its own.
- **Exactly one parent per non-root.** This is where Claims 1 and 5 come from.
  Give a node two parents and subtrees overlap: the recursion still terminates
  but revisits nodes, and on a stack of diamonds that is exponential. It is the
  commonest way a "tree" problem turns into a wrong answer.
- **Claim 5 is the licence for "no visited set".** A theorem, not a convenience.
  [[dfs]] on a general graph needs the set because Claim 5 is false there.
- **Nothing used arity or order.** No step assumed two children or any bound on
  their number, so every fact holds verbatim for N-ary trees and, per component,
  for forests.
- **The rooting was a choice.** Parent, depth, height, subtree and leaf are
  properties of the pair (tree, root), not of the tree. Re-root and they all
  change — which is why rerooting is a named technique in [[tree-dp]].

## What it costs

Almost every tree algorithm costs `Θ(n)` time and `Θ(h)` stack. Both are worth
deriving rather than reciting.

**Time: a counting argument.** Claim 5 gives it exactly — one call per node, `n`
calls. Inside the call at `v` the loop body runs `deg(v)` times, and
`Σ_v deg(v) = n - 1` because Claim 4 matched children to edges one for one. Total
work: `n` calls plus `n - 1` iterations, `Θ(n)`, with the constant visible.

For a binary tree the count is sharper and mildly surprising. There are `2n`
child slots and `n - 1` are filled, so exactly `n + 1` are null: a recursion that
calls itself on `None` makes `n + (n + 1) = 2n + 1` calls, over half of which do
nothing. That is why the base case is the line to write first.

As a recurrence, on a binary tree whose root has a left subtree of `k` nodes:

```
T(n) = T(k) + T(n - 1 - k) + O(1),   T(0) = O(1)
```

Guess `T(n) = c(2n + 1)` and check: `c(2k+1) + c(2(n-1-k)+1) + c = c(2n+1)`,
which holds for every `k`. That is the point — unlike [[merge-sort]] or
[[quicksort]], an unbalanced split costs a traversal *nothing*. Shape affects the
stack, never the total.

**Space: the height, and the height is not `log n`.** The stack holds one frame
per node on the current root-to-node path, so its peak is `h + 1`. Level `i` of a
binary tree has at most `2^i` nodes, by induction, so
`n <= 2^0 + … + 2^h = 2^(h+1) - 1` and

```
h >= ceil(log2(n + 1)) - 1        and        h <= n - 1
```

the upper bound being a chain. Both ends are reachable, so `h` is anywhere from
about `log2 n` to `n - 1`. The practical numbers: *Binary Tree Level-Order
Traversal by Levels* allows `0 <= number of nodes <= 100000`. A balanced tree of
that size is 17 frames deep; a chain is 100 000, and CPython's default recursion
limit is about 1000. A recursive solution that works on every example and dies on
one hidden case is almost always this.

**Costs people forget.**

- *Inverting a parent array* is `Θ(n)` and allocates `n` lists — and if the node
  identifiers are strings you must intern them through a dictionary first, an
  expected `O(1)` hash per node ([[hash-tables]]) and a second structure to get
  wrong. *Flat Comments to a Nested Tree* and *Render a Task Tree from CSV Rows*
  spend most of their code here.
- *Heap indexing* costs `Θ(2^(h+1))` memory, not `Θ(n)`. Fine for a balanced
  tree; for a chain of 60 nodes it is a quintillion slots. The representation,
  not the algorithm, is what explodes.
- *Sorting children into a canonical order* adds `O(n log n)`, since
  `Σ deg(v) log deg(v) <= (Σ deg(v)) log n`.

## The implementation

Everything so far in one piece: invert a parent array, find the root of an edge
list, and compute every depth and height in one iterative pass.

```python run
def build(parent):
    """Children lists and the root, from a parent array (-1 marks the root)."""
    n = len(parent)
    children, root = [[] for _ in range(n)], -1
    for v, p in enumerate(parent):
        if p == -1:
            assert root == -1, "two roots: that is a forest, not a tree"
            root = v
        else:
            children[p].append(v)
    assert root != -1, "no root: the parent pointers contain a cycle"
    return root, children


def depths_and_heights(root, children):
    """One walk down, one sweep back. depth comes down; height goes up."""
    n = len(children)
    depth, height, order = [0] * n, [0] * n, []
    stack = [root]
    while stack:                       # preorder: a parent is popped before
        v = stack.pop()                # any of its children is pushed
        order.append(v)
        for c in children[v]:
            depth[c] = depth[v] + 1
            stack.append(c)
    for v in reversed(order):          # so reversed(order) sees every child
        for c in children[v]:          # before its parent
            height[v] = max(height[v], height[c] + 1)
    return depth, height, order


parent = [-1, 0, 0, 1, 1, 2]
root, children = build(parent)
depth, height, order = depths_and_heights(root, children)
print("children:", children, " root:", root)
print("node : ", " ".join("%2d" % v for v in range(len(parent))))
print("depth: ", " ".join("%2d" % d for d in depth))
print("height:", " ".join("%2d" % h for h in height))

assert depth == [0, 1, 1, 2, 2, 2] and height == [2, 1, 1, 0, 0, 0]
assert len(order) == len(set(order)) == len(parent)      # each node exactly once
assert sum(len(c) for c in children) == len(parent) - 1  # n - 1 edges
assert max(depth) == height[root]                        # deepest node, tree height

# the root of an edge list is the one id that is never a child
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
kids = {c for _, c in edges}
assert [v for v in range(6) if v not in kids] == [0]

def relation(a, b):                    # 'Tree Node Relationship', in three lines
    if parent[a] == parent[b]:
        return "siblings"
    return "cousins" if depth[a] == depth[b] else "others"

print("3 & 4:", relation(3, 4), "| 3 & 5:", relation(3, 5), "| 1 & 5:", relation(1, 5))
assert (relation(3, 4), relation(3, 5), relation(1, 5)) == ("siblings", "cousins", "others")
print("6 nodes, 5 edges, every depth and height from one pass")
```

Three lines carry the weight.

`for c in children[v]: depth[c] = depth[v] + 1` is the downward flow, written at
the moment of *pushing* rather than popping. The parent's depth is final by then,
and a node's depth is written exactly once — by its unique parent (Claim 4).

`for v in reversed(order)` removes the recursion entirely. In a preorder the
parent always appears before every node of its subtree, so reading the list
backwards guarantees every child is done before its parent. Any bottom-up tree
computation — subtree sums, sizes, heights, the whole of [[tree-dp]] — can be a
loop over `reversed(order)` instead of a post-order recursion, and then a chain
of `10^5` nodes is not a problem. Keep this in your pocket.

`assert root == -1` inside the loop is not decoration: a parent array with two
`-1`s is a forest, one with none contains a cycle, and both produce nonsense
several hundred lines later if you let them through here.

## Variants you will meet

**Binary trees.** Children named rather than listed: `left` and `right`. The
naming carries meaning — a single child is still *a left child or a right child*,
which is why *Binary Tree Right View* and the vertical-order problems have
answers at all.

**Binary search trees.** A binary tree plus an ordering invariant on values,
which turns a walk into a search: [[bst]]. *Validate Binary Search Tree* appears
four times here because the invariant is subtler than it looks.

**N-ary trees and forests.** Any number of children, possibly several roots.
Every structural fact above survives, and a forest of `k` trees on `n` nodes has
`n - k` edges. Handle a forest by looping over its roots, or by inventing a
virtual root whose children are the real ones — often the shortest correct code.

**Left-child / right-sibling.** Any N-ary tree is a binary tree in disguise:
`left` points at the first child, `right` at the next sibling. It is a bijection
between forests and binary trees, costs `O(n)`, and is how you reuse binary
machinery on arbitrary arity. The price is height, since a node with `k` children
becomes a chain of length `k`. Demonstrated below.

**Heap-indexed arrays.** No pointers at all: perfect for [[heap|binary heaps]]
and [[segment-tree|segment trees]], where completeness is guaranteed by
construction, and a trap everywhere else.

**Parent-pointer trees.** Each node knows its parent and nothing else. Upward
questions become trivial — *Lowest Common Ancestor with Parent Pointers* is a
depth-align-then-walk-up in ten lines — and downward questions need an inversion
first. [[union-find]] is the extreme case: parent pointers only, and the shape
deliberately meaningless.

**Tries.** Edges labelled with characters, so a path spells a string: [[trie]].

**Balanced trees.** Trees that rearrange themselves to keep `h = O(log n)`:
[[balanced-bst]] and [[ordered-set|the ordered sets]] built on them.

**Trees as tables.** An `(id, parent_id)` table with a recursive CTE or a
self-join — *Employee Subordinates* and *Classify Tree Nodes with SQL* are
traversals written in [[sql-joins|SQL]].

<svg viewBox="0 0 620 265" role="img" aria-label="a node with three children on the left, and the same tree on the right as a binary tree where left is the first child and right is the next sibling">
  <g>
    <line x1="98" y1="55" x2="52" y2="115"/>
    <line x1="110" y1="57" x2="110" y2="113"/>
    <line x1="122" y1="55" x2="168" y2="115"/>
    <circle class="fill" cx="110" cy="40" r="17"/>
    <text x="110" y="46" text-anchor="middle">1</text>
    <circle cx="40" cy="130" r="17"/>
    <text x="40" y="136" text-anchor="middle">2</text>
    <circle cx="110" cy="130" r="17"/>
    <text x="110" y="136" text-anchor="middle">3</text>
    <circle cx="180" cy="130" r="17"/>
    <text x="180" y="136" text-anchor="middle">4</text>
    <text x="110" y="180" text-anchor="middle">n-ary: three siblings</text>
    <line x1="245" y1="120" x2="315" y2="120"/>
    <line x1="315" y1="120" x2="303" y2="113"/>
    <line x1="315" y1="120" x2="303" y2="127"/>
    <text x="280" y="105" text-anchor="middle">LCRS</text>
    <line x1="389" y1="49" x2="356" y2="86"/>
    <line x1="358" y1="111" x2="407" y2="149"/>
    <line x1="433" y1="171" x2="482" y2="209"/>
    <circle class="fill" cx="400" cy="35" r="17"/>
    <text x="400" y="41" text-anchor="middle">1</text>
    <circle cx="345" cy="100" r="17"/>
    <text x="345" y="106" text-anchor="middle">2</text>
    <circle cx="420" cy="160" r="17"/>
    <text x="420" y="166" text-anchor="middle">3</text>
    <circle cx="495" cy="220" r="17"/>
    <text x="495" y="226" text-anchor="middle">4</text>
    <text x="330" y="225" text-anchor="middle">left = first child</text>
    <text x="330" y="248" text-anchor="middle">right = next sibling</text>
  </g>
</svg>

```python run
class BNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val, self.left, self.right = val, None, None


def to_binary(v, children):
    """Left-child / right-sibling: left = first child, right = next sibling."""
    node, prev = BNode(v), None
    for c in children[v]:
        child = to_binary(c, children)
        if prev is None:
            node.left = child          # the FIRST child becomes the left child
        else:
            prev.right = child         # every later one hangs off its predecessor
        prev = child
    return node


def to_nary(node, children):
    """Invert: the left child, then that child's right-sibling chain."""
    c = node.left
    while c is not None:
        children[node.val].append(c.val)
        to_nary(c, children)
        c = c.right


def bheight(node):
    return -1 if node is None else 1 + max(bheight(node.left), bheight(node.right))


def bcount(node):
    return 0 if node is None else 1 + bcount(node.left) + bcount(node.right)


original = [[1, 2, 3], [4, 5], [], [6], [], [], []]
binary = to_binary(0, original)
back = [[] for _ in original]
to_nary(binary, back)

print("n-ary children:", original)
print("round-tripped :", back)
assert back == original, "left-child/right-sibling must be a bijection"
assert bcount(binary) == len(original) == 7

depth = [0] * 7
for v in range(7):
    for c in original[v]:
        depth[c] = depth[v] + 1
nary_height = max(depth)
print("height as an n-ary tree :", nary_height, "(0 -> 1 -> 4)")
print("height as a binary tree :", bheight(binary), "(0 -> 1 -> 2 -> 3 -> 6)")
assert nary_height == 2 and bheight(binary) == 4
print("same 7 nodes, same information, deeper tree")
```

The round-trip assert is the interesting line: the transform loses nothing, not
even the *order* of the children, which is what *Canonical N-Ary Tree Codec*
depends on. The height comparison is the price — sibling chains become depth, so
a node with a thousand children becomes a thousand-deep binary subtree.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **A parent column, a `manager_id`, a `parent_id`, or `[parent, child]`
   pairs** — a tree spelled out: *Employee Subordinates*, *Create a Binary Tree
   from Parent-Child Descriptions*, *Find the Root of a Directed Tree*.
2. **"`n` nodes and `n - 1` edges, connected"** with the word tree never used.
   By Claim 3 backwards that *is* a tree: stop worrying about cycles and root it.
3. **The words root, leaf, depth, level, ancestor, subtree**, which mean nothing
   outside a rooted structure. "All leaves at the same level" (*Check Whether All
   Leaves Are at the Same Level*) is a depth question in disguise.
4. **Nesting in the output.** Flat input, hierarchical output: *Flat Comments to
   a Nested Tree*, *Dictionary Records to an Editable XML Tree*, *Render a Task
   Tree from CSV Rows*. Build children lists, find the roots, emit recursively.
5. **A filesystem, an org chart, a taxonomy, a comment thread, a tournament
   bracket** — real-world hierarchies, as in *Delete a Filesystem Tree* and
   *Second Minimum in a Tournament Tree*.
6. **"Each node has at most two children"** or indices `2i+1` / `2i+2` — a binary
   tree, possibly heap-indexed.

The anti-signals, which matter more:

- **A node that can appear under two parents.** A DAG: shared subproblems mean
  memoisation, and "visit every node once" is no longer free.
- **Edges that may form a cycle**, or an edge count that is not `n - 1` — a
  general [[graphs|graph]]; reach for [[dfs]] with a visited set.
- **"Undirected tree" with no root named.** Root it anywhere, but check whether
  you need to at all.
- **"Tree" said about the search space**, not the input: "explore the tree of
  possibilities" is [[backtracking]], and that tree is never materialised.

## Traps

**Recursion depth on a skewed tree.** Symptom: correct on every example,
`RecursionError` on one hidden case; the constraint line saying `10^5` nodes is
the warning. Fix: the `reversed(order)` sweep above.

**Assuming one parent per node, or taking `n - 1` edges as proof of treeness.**
Symptoms: counts that are too large, a traversal that takes seconds on a small
input, or a node that is never reached. Both are demonstrated below.

**Depth/height convention mismatch.** Symptom: every answer off by exactly one.
Write the convention as a comment above the function, checked against the
statement's words, before the body. Related: `height(None)` is `-1` under the
edge convention and `0` under the node convention, and `max()` of an empty
sequence raises.

**Treating a one-child node as a leaf.** A leaf has *no* children; for N-ary
that means an empty children list. This is the entire bug in most wrong answers
to *Minimum-Sum Root-to-Leaf Path*, where a node with one child ends no path.

**Mutating a shared children list.** `[[]] * n` gives `n` references to one list.
Symptom: every node appears to have every child.

**Forgetting that a forest has several roots**, so you process one component and
drop the rest. And **caching a subtree answer keyed by value**: two nodes can
hold the same value, so key by index.

```python run
import sys


def chain(n):
    children = [[] for _ in range(n)]
    for v in range(n - 1):
        children[v].append(v + 1)
    return children


def height_rec(v, children):
    if not children[v]:
        return 0
    return 1 + max(height_rec(c, children) for c in children[v])


def height_iter(root, children):
    depth, stack, best = {root: 0}, [root], 0
    while stack:
        v = stack.pop()
        best = max(best, depth[v])
        for c in children[v]:
            depth[c] = depth[v] + 1
            stack.append(c)
    return best


kids = chain(4000)
try:
    print("recursive height:", height_rec(0, kids))
except RecursionError:
    print("recursive height: RecursionError (limit is %d frames, the tree is 4000 deep)"
          % sys.getrecursionlimit())
print("iterative height:", height_iter(0, kids))
assert height_iter(0, kids) == 3999


def walk_count(root, children):
    seen, stack = 0, [root]
    while stack:
        v = stack.pop()
        seen += 1
        stack.extend(children[v])
    return seen


def validate(n, edges):
    """Is this edge list really a rooted tree on 0..n-1?"""
    if len(edges) != n - 1:
        return "has %d edges; a tree on %d nodes has %d" % (len(edges), n, n - 1)
    indeg, adj = [0] * n, [[] for _ in range(n)]
    for p, c in edges:
        indeg[c] += 1
        adj[p].append(c)
    if max(indeg) > 1:
        return "node %d has two parents: this is a DAG" % indeg.index(2)
    roots = [v for v in range(n) if indeg[v] == 0]
    if len(roots) != 1:
        return "found %d roots" % len(roots)
    if walk_count(roots[0], adj) != n:
        return "only %d of %d nodes reachable: a cycle sits off to one side" % (
            walk_count(roots[0], adj), n)
    return "a tree, rooted at %d" % roots[0]


diamond = [[1, 2], [3], [3], []]        # node 3 is a child of BOTH 1 and 2
print("4 distinct nodes; the tree walk reports", walk_count(0, diamond), "visits")
assert walk_count(0, diamond) == 5
print("  ", validate(5, [(0, 1), (0, 2), (1, 3), (2, 3)]))
print("  ", validate(4, [(1, 2), (2, 3), (3, 1)]))
print("  ", validate(4, [(0, 1), (0, 2), (1, 3)]))
assert validate(4, [(0, 1), (0, 2), (1, 3)]).startswith("a tree")
assert "two parents" in validate(5, [(0, 1), (0, 2), (1, 3), (2, 3)])
assert "cycle" in validate(4, [(1, 2), (2, 3), (3, 1)])
```

Look at the second `validate` failure carefully. Four nodes, three edges,
exactly one node with no parent and every other with exactly one — and still not
a tree, because 1, 2, 3 form a cycle that 0 cannot reach. Only reachability
catches it, which is Claim 3 reminding you it was never an "if and only if".

And the diamond: five visits over four nodes, no error, no infinite loop. Stack
diamonds and the visit count doubles per layer, so a "tree" of 60 nodes takes a
billion steps. The symptom is a timeout; the cause is a sentence in the statement
you did not verify.

## What to memorise

The definition, because everything else follows from it: **a tree is a node plus
a list of trees**. When stuck, rewrite the problem in those terms and the
recursion writes itself.

Five structural facts, worth knowing cold:

- `n` nodes, `n - 1` edges; a forest of `k` trees has `n - k`.
- Exactly one simple path between any two nodes.
- Subtrees of different children are disjoint — hence no visited set, and hence
  `Θ(n)` for a full traversal.
- `ceil(log2(n+1)) - 1 <= h <= n - 1` for a binary tree, so the stack is anywhere
  from 17 to 100 000 frames at `n = 10^5`.
- A binary tree with `n` nodes has `n + 1` null child slots.

The sentence that turns a problem into a tree problem: *"Does every item have
exactly one parent, and is the question about ancestry or about a subtree?"* The
first half tells you it is a tree; the second tells you which way information
flows.

The habit, worth more than any template: **before writing the body, say what
your function takes down and what it returns up** — "takes the depth so far,
returns the height of this subtree". If you cannot say it in one sentence, you
are about to mix the two directions and pass only symmetric test cases.

The template, which should come out of your fingers:

```python
root, children = -1, [[] for _ in range(n)]
for v, p in enumerate(parent):
    if p == -1:
        root = v
    else:
        children[p].append(v)

order, stack = [], [root]
while stack:
    v = stack.pop()
    order.append(v)
    for c in children[v]:
        depth[c] = depth[v] + 1
        stack.append(c)
for v in reversed(order):      # every child before its parent
    ...                        # bottom-up: sizes, heights, subtree sums
```

## Check yourself

:::check
Why does depth-first search on a tree need no `visited` set, while the identical
code on a general graph does?
--
Because of Claim 5: the subtrees of two distinct children are disjoint, so the
recursion can never reach a node by two routes. That follows from unique paths
(Claim 1), which follows from acyclicity plus connectivity — remove either
hypothesis and the guarantee is gone.

Be precise about what goes wrong without it. On an undirected graph with a
cycle, omitting the set loops forever, since you walk back along the edge you
came from; on a DAG it terminates but re-explores shared subgraphs, at a cost
exponential in the number of diamonds. A tree is the one structure where the
check is provably redundant.
:::

:::check
Someone says: "any graph with `n` nodes and `n - 1` edges is a tree — that is
the definition." Where are they wrong, and what is the correct statement?
--
They have taken one direction of Claim 3 for both. The proof shows
*tree ⟹ `n - 1` edges*, not the converse. Counterexample: four nodes, edges
`(1,2), (2,3), (3,1)`, node 0 isolated — three edges, and both cyclic and
disconnected.

The correct statement is the "any two of three" theorem: for a graph on `n`
vertices, any two of {connected, acyclic, `n - 1` edges} imply the third. So
`n - 1` edges plus connectivity is a tree, and `n - 1` edges alone is nothing.
In code that is the difference between the `len(edges) == n - 1` check and the
reachability check in the validator above.
:::

:::check
*Binary Tree Preorder Traversal* gives you a heap-indexed array. A colleague
proposes converting every tree in the bank to that form, because "it is just a
compact array". Where are they wrong?
--
Heap indexing reserves a slot for every *position* in a complete tree of that
height, not for every node: a tree of height `h` needs `2^(h+1) - 1` slots
however few nodes it contains.

For a balanced tree that is fine, `h ≈ log2 n` and the array is `Θ(n)`. For a
skewed one it is catastrophic — a right-leaning chain of 60 nodes has height 59
and needs about `1.15 × 10^18` slots. Since `h` can reach `n - 1`, the
representation is `Θ(2^n)` in the worst case.

So heap indexing is right when completeness is *guaranteed by construction* —
[[heap|binary heaps]], [[segment-tree|segment trees]] — and a trap for arbitrary
input trees. The bank's preorder problem gets away with it only because the
statement fixes and bounds the array itself.
:::

:::check
*Tree Node Relationship* asks you to classify two nodes of a tree rooted at 0 as
"siblings", "cousins", or "others". Why do `parent[]` and `depth[]` suffice, and
what would you need instead if the question asked how far apart the two nodes
are?
--
Siblings means equal parents; cousins means equal depth and different parents.
Both read only two arrays, each filled by one `Θ(n)` traversal, so every query is
`O(1)` after linear preprocessing.

Distance is a different kind of question: it is about the *path* between the
nodes, not their position relative to the root. By Claim 1 that path is unique,
and it climbs from `u` to the lowest common ancestor and back down to `v`, so
`dist(u, v) = depth(u) + depth(v) - 2·depth(lca(u, v))`. You therefore need an
[[lca]] — pointers walked up in lockstep for `O(h)`, or [[binary-lifting]] for
`O(log n)` per query. That formula is *Distance Between Two Tree Nodes*.
:::

:::check
You convert an N-ary tree to binary by left-child/right-sibling, run a binary
tree algorithm, and convert back. Which quantities are preserved by the round
trip, and which are not — and why does that make the transform useful for some
problems and useless for others?
--
Preserved: the nodes, their count, the parent/child relationships, and the
left-to-right order of children — the round-trip assert above checks exactly
this. Not preserved: depth and height, and so anything defined from them, since a
node with `k` children becomes a chain of `k` binary nodes and siblings that
shared a depth end up at `k` different depths.

So the transform is useful when the algorithm is structural — serialising
([[serialize-tree]]), comparing shapes, reusing binary code on arbitrary arity —
and wrong for anything level-based: a binary "nodes at depth `k`" routine run on
it answers a different question from *Nodes at a Given N-ary Tree Level*.
:::
