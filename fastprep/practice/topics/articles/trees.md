# Trees: Vocabulary and Shapes

> A tree is a node plus a list of smaller trees, so almost every tree question is answered by deciding what a node must be told by its parent and what it must hand back to it, and then letting one walk carry both.

## The problem it solves

Here is a binary tree with nine nodes. The numbers are just names.

```
            1
          /   \
         2     3
        / \
       4   5
      /     \
     6       7
    /         \
   9           8
```

The question, from [[p:bloomberg-diameter-of-binary-tree|Diameter of a Binary Tree]]:
what is the largest number of edges on a path between any two nodes? A path may
go up and then down. It may not use a node twice. It does not have to pass
through the root.

Look at it for a moment before reading on. The answer is 6: the path
9, 6, 4, 2, 5, 7, 8 has seven nodes and six edges. Notice what it does not do.
It never touches the root. The longest path through node 1 is 9, 6, 4, 2, 1, 3,
which has five edges.

The first solution anyone writes is the honest one: try every pair of nodes,
find the path between them, keep the longest. Nine nodes have 36 pairs, and you
can find any one path in a few steps. For nine nodes that is fine. The bank's
version allows 100,000 nodes. That is about 5 x 10^9 pairs, and each path can be
100,000 edges long. Even the smarter brute force, a breadth-first search from
every node, is n searches of n steps each: 10^10 steps. Too slow by a factor of
ten thousand.

This chapter builds the method that answers this question, and almost every other
question about a tree, in one walk: each node is visited once, does a constant
amount of work, and the whole thing is 100,000 small steps. On the way it builds
the four ways information can move through a tree, because once you can name the
direction, the code writes itself:

- **up**, from children to parent, as a return value (heights, sizes, the
  diameter);
- **down**, from parent to children, as an argument (depths, path sums, the path
  so far);
- **both at once** (a value carried down and another returned up);
- **across**, one level at a time, with a queue (level order, the right side
  view).

Before any of that, the vocabulary and the shapes the input arrives in, because
every statement is written in those words and half the bugs are a word read
wrongly.

### The words, exactly

Take this smaller tree, rooted at A:

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

| word | meaning | in the picture |
| --- | --- | --- |
| root | the node with no parent | A |
| parent / child | joined by an edge, one level apart | B is the parent of D |
| siblings | same parent | D and E |
| ancestor / descendant | anywhere above / below on the path to the root | A is an ancestor of F |
| leaf | **no** children | D, E, F |
| internal node | at least one child | A, B, C |
| depth of v | number of edges from the root down to v | depth(E) = 2 |
| height of v | number of edges on the longest path from v down to a leaf | height(B) = 1 |
| size of v | number of nodes in v's subtree, v included | size(B) = 3 |
| level k | all nodes at depth k | level 1 is {B, C} |
| forest | several disjoint trees | remove A and you have two |

Two of those deserve a warning now, and they will come back as traps.

**Depth and height are not the same number read from opposite ends.** Depth is a
fact about a node's ancestors: you learn it by walking down from the root. Height
is a fact about a node's subtree: you learn it only after looking at everything
below. That difference, "known from above" against "known from below", is the
whole of this chapter in one sentence.

**The counting convention is a live hazard.** The table counts edges, so a lone
node has depth 0 and height 0. Many statements count nodes instead.
[[p:linkedin-maximum-depth-of-binary-tree|Maximum Depth of Binary Tree]] wants
"the number of nodes on the longest path from the root to a leaf", so a lone node
has depth 1 and an empty tree 0. The diameter problem counts edges. Neither is
right; the one in the statement is. The code in this chapter uses a node count
called `levels(v)`: the number of nodes on the longest downward path from v, with
`levels(None) = 0`. It equals height + 1, and it makes the empty tree a clean
base case.

The definition that everything else follows from is recursive on purpose:

**A tree is a node plus a list of trees hanging off it.**

Nothing there says "two". A binary tree is the case where the list has at most
two entries and they are named `left` and `right`. An N-ary tree is the general
case. A **forest** is the list with no node on top. Every fact in this chapter
holds for all three; the code just loops over children instead of naming two.

### The five ways a tree arrives

The tree is the same object each time. What changes is how much work you do
before the real algorithm starts.

1. **Linked nodes.** A `Node` with `left` and `right`, or `val` and `children`.
   Follow pointers from the root.
2. **Parent array.** `parent[i]` is i's parent, -1 at the root.
   [[p:inmobi-employee-subordinates|Employee Subordinates]] gives `bosses[i]`, the
   boss of employee i + 2: a parent array with an offset. Upward moves are free;
   downward moves need the array inverted first.
3. **Children lists.** `children[i]`, as in
   [[p:drw-count-balanced-tree-nodes|Count Balanced Nodes in a Rooted Tree]]. The
   inverse of the parent array, and the form almost every algorithm wants.
4. **Edge list.** Pairs `[parent, child]`, or undirected pairs plus "rooted at
   0". You build the adjacency and sometimes have to find the root: it is the one
   node that is never a child.
5. **Level-order array.** `[3, 9, 20, null, null, 15, 7]`, the way most binary
   tree problems in the bank show their input. Children are read off a queue, two
   entries per real node. A close cousin is the heap-indexed array, children of i
   at 2i + 1 and 2i + 2, which reserves a slot for every position, present or not.

Converting between them is mechanical and is the first five lines of a great many
solutions. Converting to children lists (or linked nodes) is usually right.

### When it is the wrong tool

- **A node with two parents.** Then it is a DAG. Subtrees overlap, a walk reaches
  the same node by two routes, and "visit each node once" stops being free. That
  is [[graphs]] territory, with a visited set or memoisation.
- **A cycle, or an edge count that is not n - 1.** A general graph with a wishful
  name. Reach for [[dfs]] or [[bfs]] with a visited set.
- **"Tree" said about the search space**, not the input. "Explore the tree of
  choices" is [[backtracking]]; that tree is never stored.
- **Distances between many arbitrary pairs.** One walk per query is too slow;
  that is [[lca]] with preprocessing.

## Build it from the brute force

We will not start with the clever walk. We will start with the slowest correct
program a beginner writes for the diameter, count it, find where its time goes,
and fix that one waste. The clever walk will appear at the end as the obvious
repair.

### Step 1: where can the longest path be?

Every path in a rooted tree has exactly one **highest node**: the node on the path
closest to the root. Walk along the path and watch the depth. It goes up for a
while (towards the root) and then down, and it can only turn once, because to
turn twice it would have to go down and then up again, and going up from a node
means going to its one parent, which is where you just came from. So a path is
"down the left side of some node v, and down the right side of v", where either
side may be empty. Call v the **bend**.

That turns one question about all pairs into one question per node:

> What is the longest path whose bend is v?

It goes as deep as possible into v's left subtree and as deep as possible into
v's right subtree. With `levels` counting nodes, the left arm has
`levels(v.left)` edges (one edge from v down to each node of the arm) and the
right arm `levels(v.right)`. So:

```
bend(v)     = levels(v.left) + levels(v.right)
levels(v)   = 1 + max(levels(v.left), levels(v.right)),   levels(None) = 0
diameter    = the largest bend(v) over every node v
```

On the example, bend(2) = levels(4) + levels(5) = 3 + 3 = 6. That is the answer.

### You might think: "The longest path goes through the root."

It feels right because the root is the "middle" of the tree. It is wrong, and
the example already shows it. bend(1) = levels(2) + levels(3) = 4 + 1 = 5, and
the true answer is 6.

Shrink the counterexample until it is obvious: a root with a single child, and
under that child two long arms. Every long path lives under the child. The root
can add only one edge, to itself, on one end. A path that bends at the root uses
the root's two sides, and here one side is empty.

So the answer is not a fact about the root. It is the best of a fact about
every node. That is the first lesson of tree recursion, and it is worth saying a
second way: **the thing the root returns and the thing the problem asks for are
not always the same.** Hold that sentence; it becomes the subtle line in the code.

### Step 2: the direct program, and its cost

Write it exactly as the formula reads. A function `levels` that walks a subtree.
A function `diameter` that, at every node, calls `levels` on both children, and
recurses into both children.

```python
def levels(node):
    if node is None:
        return 0
    return 1 + max(levels(node.left), levels(node.right))

def diameter_brute(node):
    if node is None:
        return 0
    here = levels(node.left) + levels(node.right)      # bend at this node
    return max(here, diameter_brute(node.left), diameter_brute(node.right))
```

It is correct. How slow is it? `levels(v)` visits every node of v's subtree, so
it costs size(v). `diameter_brute` calls it at every node, on both children, so
the total is the sum over all v of size(v.left) + size(v.right), which is about
the sum of all subtree sizes.

Count that sum a different way. A node u is inside the subtree of v exactly when
v is one of u's ancestors (or u itself). So u is counted once for each of its
ancestors: depth(u) + 1 times. The sum of subtree sizes equals the sum of
(depth + 1) over all nodes.

- On a balanced tree the depths are about log2 n, so the total is about n log2 n.
  Fine.
- On a chain, depths are 0, 1, 2, ..., n - 1, and the total is n(n+1)/2. For
  100,000 nodes that is 5 x 10^9. Too slow, and the bank's constraints say
  outright that the tree "may be skewed".

### Step 3: notice the waste

Where does the time go? Take node 6 in the example. `levels(6)` is computed when
node 4 asks for `levels(4.left)`. It is computed again inside `levels(4)`, when
node 2 asks for its left side. Again inside `levels(2)`, when the root asks. And
again when `diameter_brute` reaches node 4 itself. The same subtree, measured
over and over, and it gives the same answer every time, because nothing about the
subtree of 6 depends on who is asking.

| who asks | computes levels of | which walks |
| --- | --- | --- |
| node 1 (root) | 2 | 4, 6, 9, 5, 7, 8 |
| node 2 | 4 and 5 | 6, 9 and 7, 8 |
| node 4 | 6 | 9 |
| node 6 | 9 | nothing below |

Node 9 is walked by every one of its ancestors. On a chain of n nodes the bottom
node is walked n times.

And here is the observation that cures it. Each node, when it is asked for its
levels, needs exactly two numbers: the levels of its two children. And when it is
asked for its bend, it needs **the same two numbers**. The brute force computes
those numbers once for the bend, then throws them away, then computes them
again (inside the parent's `levels` call) for the height. If the node computed
the two numbers once, used them for its bend, and **returned** its own levels to
its parent, the parent would never have to walk down again.

### The question that unlocks it

That repair comes from one question, and it is the question to ask on every tree
problem:

**If each child handed me the answer for its own subtree, what would I need it
to hand me, and what do I hand my parent?**

For the diameter: each child hands me its `levels`. With those two numbers I can
score my bend, and I can compute my own `levels` to hand upward. Nothing else is
needed. The answer to "what do I hand my parent" is *not* the diameter; it is the
one number my parent needs in order to do the same job one level up.

Say it a second way. Pretend your function already works on smaller trees. That
is not wishful thinking; it is induction. The child's subtree is strictly smaller,
so by the time you need its answer, it is correct. Your only job is to say how two
correct child answers become a correct answer for you. If you cannot say that in
one sentence, the thing you are returning is the wrong thing, and you need to
return more (a pair, a triple) until you can.

There is a mirror question for information that flows the other way: **what
must my parent tell me that my subtree cannot know?** Depth is the standard
example. No node below you knows how far you are from the root. Your parent does,
so it passes `depth + 1` down as an argument.

### Step 4: one walk, children first

Now the program is forced. Visit the children before the node (that is what
**post-order** means: left, right, then the node), so that their answers exist
when the node needs them. Score the bend in a variable that lives outside the
recursion. Return the node's levels.

```python
def diameter(root):
    best = 0
    def walk(node):
        nonlocal best
        if node is None:
            return 0
        l = walk(node.left)          # children first
        r = walk(node.right)
        best = max(best, l + r)      # what the problem asks: the bend here
        return 1 + max(l, r)         # what the parent needs: my levels
    walk(root)
    return best
```

Each node is visited once. The two lines in the middle are the whole idea, and
they do two different jobs: one records an answer, one reports upward.

### The same move, in the other three directions

The diameter sent information up. The question "what do I hand my parent, and
what must it tell me" has four possible answers, and each one is a technique you
will use constantly.

- **Up only.** Maximum depth: `return 1 + max(walk(left), walk(right))`. Subtree
  size: `return 1 + sum(walk(c) for c in children)`. The answer is what the root
  returns.
- **Up, with a recorded best.** Diameter, balanced, maximum path sum. The root's
  return value is a helper; the answer is a maximum over all nodes.
- **Down.** Path sum: "is there a root-to-leaf path adding to T?" A node cannot
  answer from below, because the question depends on what the path above it has
  already used. So the parent passes the *remaining* target down:
  `walk(child, remaining - node.val)`. A leaf checks `remaining == node.val`.
- **Across.** "The values level by level": the answer depends on depth, not on
  any one subtree. A queue, processed one level at a time, gives exactly that.

### The technique in one sentence

**Treat a tree as a node plus smaller trees; decide what each call takes from its
parent and returns to its parent, trust the recursive calls on the children
because their trees are smaller, and the whole answer comes out of one walk that
visits each node once.**

And the question that produced it: **if each child handed me the answer for its
own subtree, what would I need it to hand me, and what do I hand my parent?**

## Worked by hand

Get a pen. The tree is the one from the start:

```
            1
          /   \
         2     3
        / \
       4   5
      /     \
     6       7
    /         \
   9           8
```

### Trace 1: the diameter, bottom-up

Post-order visits a node only after both of its subtrees are finished. For this
tree the order is 9, 6, 4, 8, 7, 5, 2, 3, 1. Each row is one node finishing: what
its children reported, the bend it scores, what it reports upward, and the best
bend seen so far.

| node | left reports | right reports | bend = l + r | returns 1 + max(l, r) | best so far |
| --- | --- | --- | --- | --- | --- |
| 9 | 0 (none) | 0 (none) | 0 | 1 | 0 |
| 6 | 1 (from 9) | 0 | 1 | 2 | 1 |
| 4 | 2 (from 6) | 0 | 2 | 3 | 2 |
| 8 | 0 | 0 | 0 | 1 | 2 |
| 7 | 0 | 1 (from 8) | 1 | 2 | 2 |
| 5 | 0 | 2 (from 7) | 2 | 3 | 2 |
| 2 | 3 (from 4) | 3 (from 5) | **6** | 4 | 6 |
| 3 | 0 | 0 | 0 | 1 | 6 |
| 1 | 4 (from 2) | 1 (from 3) | 5 | 5 | **6** |

Every cell can be checked with only the row's own children. Here is the row for
node 2, in words:

> "I am node 2. My left child, 4, reports 3: the longest path going down from 4
> has three nodes, 4, 6, 9. My right child, 5, reports 3: 5, 7, 8. A path that
> bends at me can run down the left as far as 9 and down the right as far as 8.
> Each of those six nodes hangs one edge below the node before it, so the path
> has 3 + 3 = 6 edges. I write 6 into `best`. But I report only 1 + max(3, 3) = 4
> to my parent. My parent can extend a path through me upward, and a path that
> continues up through my parent can use only one of my two arms, or it would
> pass through me twice."

Here is the same tree with the numbers each node reports, so you can see the
values move.

<svg viewBox="0 0 660 380" role="img" aria-label="the nine-node example tree; each node is labelled with the number it reports to its parent; node 2 is shaded and scores the bend 3 plus 3 equals 6; the longest path 9, 6, 4, 2, 5, 7, 8 is drawn with thick edges">
  <g>
    <line x1="306" y1="52" x2="214" y2="98"/>
    <line x1="334" y1="52" x2="426" y2="98"/>
    <line x1="186" y1="122" x2="134" y2="168" stroke-width="4"/>
    <line x1="214" y1="122" x2="266" y2="168" stroke-width="4"/>
    <line x1="106" y1="192" x2="94" y2="238" stroke-width="4"/>
    <line x1="294" y1="192" x2="326" y2="238" stroke-width="4"/>
    <line x1="74" y1="262" x2="58" y2="308" stroke-width="4"/>
    <line x1="354" y1="262" x2="386" y2="308" stroke-width="4"/>
    <circle cx="320" cy="40" r="18"/>
    <text x="320" y="46" text-anchor="middle">1</text>
    <circle class="fill" cx="200" cy="110" r="18"/>
    <text x="200" y="116" text-anchor="middle">2</text>
    <circle cx="440" cy="110" r="18"/>
    <text x="440" y="116" text-anchor="middle">3</text>
    <circle cx="120" cy="180" r="18"/>
    <text x="120" y="186" text-anchor="middle">4</text>
    <circle cx="280" cy="180" r="18"/>
    <text x="280" y="186" text-anchor="middle">5</text>
    <circle cx="80" cy="250" r="18"/>
    <text x="80" y="256" text-anchor="middle">6</text>
    <circle cx="340" cy="250" r="18"/>
    <text x="340" y="256" text-anchor="middle">7</text>
    <circle cx="50" cy="320" r="18"/>
    <text x="50" y="326" text-anchor="middle">9</text>
    <circle cx="400" cy="320" r="18"/>
    <text x="400" y="326" text-anchor="middle">8</text>
    <text x="346" y="36">returns 5, bend 4+1 = 5</text>
    <text x="226" y="100">returns 4</text>
    <text x="150" y="84">bend 3+3 = 6</text>
    <text x="466" y="116">returns 1</text>
    <text x="146" y="186">returns 3</text>
    <text x="306" y="186">returns 3</text>
    <text x="106" y="256">returns 2</text>
    <text x="366" y="256">returns 2</text>
    <text x="76" y="326">returns 1</text>
    <text x="426" y="326">returns 1</text>
    <text x="330" y="370" text-anchor="middle">thick edges: the diameter, 6 edges, bending at node 2, never touching the root</text>
  </g>
</svg>

Three things in that trace are worth more than the code that produced it.

**The answer is found in the middle of the walk, not at the end.** Best becomes 6
at node 2 and never changes. The root's own bend, 5, is smaller. If you returned
the root's bend you would be wrong; the table makes that visible in a way the
code never does.

**Each node does constant work.** It reads two numbers, adds, compares, returns.
No row looks further than its own children. That is why the walk is linear.

**What a node returns is "the part of my answer that can be extended".** A bend
cannot be extended upward, because it already uses both arms. A single arm can.
So the node scores the bend and returns the arm.

### Trace 2: information going down (path sum)

Now a question that cannot be answered from below.
[[p:salesforce-path-sum|Path Sum]]: is there a root-to-leaf path whose values add
to a target? Use the node names as their values, and target 22.

No node can answer this from its subtree alone, because whether 9 completes a
good path depends on what the path above it has already used. So the parent tells
the child how much is still needed. `walk(node, need)` means "the path from the
root to my parent has used up everything except `need`".

| call | node | need on arrival | need after me | leaf? | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 22 | 21 | no | ask 2, then 3 |
| 2 | 2 | 21 | 19 | no | ask 4, then 5 |
| 3 | 4 | 19 | 15 | no | ask 6 |
| 4 | 6 | 15 | 9 | no | ask 9 |
| 5 | 9 | 9 | 0 | yes | **true**: 1+2+4+6+9 = 22 |

The `or` short-circuits, so the calls for 5 and 3 never happen. Now the same
tree with target 3. At node 2 the need after subtracting is 3 - 1 - 2 = 0. The
path 1, 2 adds up to the target. But node 2 is not a leaf, and the statement says
the path must end at a leaf.

### You might think: "When the remaining sum hits 0, return true."

On target 3 that returns true, and the right answer is false: every root-to-leaf
path is 1+2+4+6+9 = 22, 1+2+5+7+8 = 23 or 1+3 = 4. The check belongs at a leaf
and only at a leaf. A second version of the same mistake is "stop early once the
sum goes over the target": values can be negative (this problem allows -1000), so
a path that has overshot can come back.

And a third, smaller version: a node with one child is **not** a leaf. Node 4 has
a missing right child, but `walk(None, ...)` must return false, not "the path
ended here". A missing child ends nothing.

### Trace 3: information going across (level order)

[[p:atlassian-binary-tree-level-order-traversal|Binary Tree Level Order Traversal]]
wants `[[1], [2, 3], [4, 5], [6, 7], [9, 8]]`. Depth-first walks go deep before
wide, so they meet node 9 before node 3. A **queue** goes wide first: a node's
children join the back, behind every node already waiting, which means behind
the rest of the node's own level.

The one extra idea is how to know where a level ends. At the start of each round
the queue holds exactly one whole level and nothing else. So read its length
**before** you start popping, and pop exactly that many.

| round | queue at start | width | popped (this level) | queue at end |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | 1 | [2, 3] |
| 2 | [2, 3] | 2 | 2, 3 | [4, 5] |
| 3 | [4, 5] | 2 | 4, 5 | [6, 7] |
| 4 | [6, 7] | 2 | 6, 7 | [9, 8] |
| 5 | [9, 8] | 2 | 9, 8 | [] |

Round 2, in words: "the queue holds 2 and 3, so this level has width 2. Pop 2,
write it down, push its children 4 and 5 to the back. Pop 3, write it down; it has
no children. I have popped 2 nodes, so the level is done: [2, 3]. What is left in
the queue, [4, 5], is exactly the next level."

That last sentence is an invariant: at the start of every round, the queue is
exactly one level. It is true at round 1 (only the root). If it is true at the
start of a round, then after popping that level's nodes and pushing their
children, the queue holds exactly the children of that level, which is the next
level. That is the entire proof that the grouping is right.

### You might think: "The right side view is the right spine."

[[p:bloomberg-binary-tree-right-side-view|Binary Tree Right Side View]] asks what
you see standing to the right of the tree. Following `right` pointers from the
root gives 1, 3, and stops, because 3 is a leaf. But at depth 2 you can see node
5; nothing to its right blocks it. The true view is the last node of each level:
1, 3, 5, 7, 8. The view is a level question, so it needs the level-order walk (or
a depth-first walk that carries the depth down), not a walk down one side.

## From the idea to the code

### The brute force against the walk, counted

The first program builds trees from the level-order arrays the bank uses, runs
the brute-force diameter and the post-order walk on the worked tree and on
chains, counts the work, and checks both against an honest all-pairs search on
random trees.

```python run
from collections import deque
import random

class Node:
    __slots__ = ("val", "left", "right")
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None

def build(level):                       # level-order list, None = no child
    vals = iter(level)
    root = Node(next(vals))
    q = deque([root])
    while q:
        node = q.popleft()
        for side in ("left", "right"):
            v = next(vals, "end")
            if v == "end":
                return root
            if v is not None:
                setattr(node, side, Node(v))
                q.append(getattr(node, side))
    return root

calls = 0
def levels(node):                       # nodes on the longest downward path
    global calls
    calls += 1
    if node is None:
        return 0
    return 1 + max(levels(node.left), levels(node.right))

def diameter_brute(root):               # every node re-measures its children
    if root is None:
        return 0
    here = levels(root.left) + levels(root.right)
    return max(here, diameter_brute(root.left), diameter_brute(root.right))

def diameter(root):                     # one post-order walk
    best, visits = 0, 0
    def walk(node):
        nonlocal best, visits
        visits += 1
        if node is None:
            return 0
        l = walk(node.left)             # children first ...
        r = walk(node.right)
        best = max(best, l + r)         # ... score the bend here ...
        return 1 + max(l, r)            # ... report one arm upward
    walk(root)
    return best, visits

def truth(root):                        # BFS from every node: the slow honest answer
    adj, stack = {}, [(root, None)]
    while stack:
        node, par = stack.pop()
        adj[node] = [x for x in (node.left, node.right, par) if x]
        stack += [(c, node) for c in (node.left, node.right) if c]
    best = 0
    for s in adj:
        dist, q = {s: 0}, deque([s])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in dist:
                    dist[w] = dist[u] + 1
                    q.append(w)
        best = max(best, max(dist.values()))
    return best

tree = build([1, 2, 3, 4, 5, None, None, 6, None, None, 7, 9, None, None, 8])
print("worked tree: diameter", diameter(tree)[0], "| bend at the root only:",
      levels(tree.left) + levels(tree.right))
assert diameter(tree)[0] == truth(tree) == diameter_brute(tree) == 6

for n in (100, 200, 400):               # a chain leaning left
    chain = build([0] + sum(([i, None] for i in range(1, n)), []))
    calls = 0
    d_brute = diameter_brute(chain)
    d, visits = diameter(chain)
    print("chain of %d: brute %6d levels() calls, walk %4d visits" % (n, calls, visits))
    assert d == d_brute == n - 1 and visits == 2 * n + 1

random.seed(7)
for _ in range(300):                    # random shapes agree with all-pairs BFS
    level = [random.choice([None, 1, 1, 1]) for _ in range(random.randint(1, 25))]
    level[0] = 1
    t = build(level)
    assert diameter(t)[0] == diameter_brute(t) == truth(t)
print("walk == brute == all-pairs BFS on 300 random trees")
```

Read the chain lines. Doubling n from 100 to 200 to 400 multiplies the brute
force's calls by four each time: quadratic. The walk's visits grow by two: it is
exactly 2n + 1, which is n real nodes plus n + 1 empty children (a binary tree
with n nodes has 2n child slots and n - 1 of them are used, so n + 1 are empty).

### Each line, and which part of the idea it is

| line | in plain words | which part of the idea |
| --- | --- | --- |
| `if node is None: return 0` | an empty tree has no levels | the base case; `levels(None) = 0` |
| `l = walk(node.left)` | ask the left child for its arm | trusting the smaller tree |
| `r = walk(node.right)` | ask the right child | same; both before using either |
| `best = max(best, l + r)` | a path bending here has l + r edges | what the **problem** asks |
| `return 1 + max(l, r)` | my longest arm, including me | what the **parent** needs |
| `walk(root); return best` | the answer is the best bend anywhere | not the root's return value |

Three boring confusions, settled now:

- **`best` is outside the recursion on purpose.** The answer is a maximum over
  all nodes; no single call owns it. `nonlocal` (or a one-element list, or a
  returned pair) is how a call writes to it. A plain local `best` inside `walk`
  would be a fresh variable in every call and would always end at 0.
- **The empty child returns 0, not -1.** That is the node-counting convention:
  levels of nothing is 0, levels of a leaf is 1. With the edge convention you
  would return -1 for None and the bend would be l + r + 2. Both are right. Mixing
  them is off by one or two.
- **A leaf needs no special case.** Both children are None, both return 0, the
  bend is 0 and the leaf returns 1. The base case on None does the work.

### The subtle line, both ways

The line that people get wrong is the `return`. It is tempting to return what you
just computed, the bend, perhaps plus one for the node itself: `return l + r + 1`,
"the number of nodes on the best path here". Here is the walk with the right line
and with that line, on the worked tree.

**Right: `return 1 + max(l, r)`.**

| node | left | right | bend | returns | best |
| --- | --- | --- | --- | --- | --- |
| 4 | 2 | 0 | 2 | 3 | 2 |
| 5 | 0 | 2 | 2 | 3 | 2 |
| 2 | 3 | 3 | 6 | **4** | 6 |
| 1 | 4 | 1 | 5 | 5 | **6** |

**Wrong: `return l + r + 1`.**

| node | left | right | bend | returns | best |
| --- | --- | --- | --- | --- | --- |
| 4 | 2 | 0 | 2 | 3 | 2 |
| 5 | 0 | 2 | 2 | 3 | 2 |
| 2 | 3 | 3 | 6 | **7** * | 6 |
| 1 | **7** * | 1 | 8 | 9 | **8** |

Every row below node 2 agrees, because a node with at most one child has
l + r + 1 = 1 + max(l, r) (one of l, r is 0). The first difference is at node 2,
the first node with two non-empty children: it reports 7 instead of 4. Then the
root believes there is a downward arm of 7 nodes on its left, adds the right arm,
and scores 8. No path of 8 edges exists. The "arm" of 7 was the whole bend at
node 2, 9-6-4-2-5-7-8, and the root has glued itself onto the middle of it, which
would put node 2 on the path with three neighbours.

What the wrong version computes is not a path at all: it is the number of edges
in a subtree shaped like a spider. And it hides well. It agrees with the right
version whenever no node below the root has two children, which is every chain
and every "V" made of two chains, the shapes people draw as examples.

```python run
from collections import deque

class Node:
    __slots__ = ("val", "left", "right")
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None

def build(level):
    vals = iter(level)
    root = Node(next(vals))
    q = deque([root])
    while q:
        node = q.popleft()
        for side in ("left", "right"):
            v = next(vals, "end")
            if v == "end":
                return root
            if v is not None:
                setattr(node, side, Node(v))
                q.append(getattr(node, side))
    return root

def diameter(root, wrong=False, log=None):
    best = 0
    def walk(node):
        nonlocal best
        if node is None:
            return 0
        l, r = walk(node.left), walk(node.right)
        best = max(best, l + r)                 # the bend: both arms
        up = l + r + 1 if wrong else 1 + max(l, r)
        if log is not None:
            log.append((node.val, l, r, l + r, up, best))
        return up
    walk(root)
    return best

tree = build([1, 2, 3, 4, 5, None, None, 6, None, None, 7, 9, None, None, 8])
for wrong in (False, True):
    log = []
    ans = diameter(tree, wrong, log)
    print("returns", "l + r + 1 (WRONG)" if wrong else "1 + max(l, r)")
    print("  node  left  right  bend  returns  best")
    for v, l, r, bend, up, best in log:
        print("  %4d  %4d  %5d  %4d  %7d  %4d" % (v, l, r, bend, up, best))
    print("  answer", ans)
    assert ans == (8 if wrong else 6)

# where the wrong line hides: no node below the root has two children
vee = build([1, 2, 3, 4, None, None, 5])          # two chains under the root
print("V shape:", diameter(vee), diameter(vee, wrong=True))
assert diameter(vee) == diameter(vee, wrong=True) == 4
small = build([1, 2, 3, 4, 5])                    # node 2 has two children
print("[1,2,3,4,5]:", diameter(small), diameter(small, wrong=True))
assert (diameter(small), diameter(small, wrong=True)) == (3, 4)
```

The rule, said twice. **Return what can be extended; record what is finished.**
Or: the return value is a promise to your parent ("here is a path starting at me
and going down"), and a bend cannot keep that promise, because it already goes
down twice.

The same shape decides [[p:google-balanced-binary-tree|Balanced Binary Tree]]. The
question at each node is "do my children's heights differ by at most one?", which
needs the children's heights, so heights are what you return. To report failure
without a second return value, return a sentinel such as -1 for "unbalanced
somewhere below", and check for it before using a child's height. The direct
version, which calls a separate `height` at every node, is the brute force from
Step 2 again, and it is quadratic on a chain for the same reason.

### Level order, and its subtle line

The level-order loop has one line that decides whether the levels come out right:
reading the queue's width once, before the round starts. In Python
`for _ in range(len(q))` evaluates `len(q)` once, so it is safe. The classic bug
is the C++ or Java loop `for (i = 0; i < q.size(); i++)`, which re-reads the size
every time round, while pops shrink the queue and pushes grow it. The program below
writes that bug in Python on purpose, next to the right loop, a depth-first
version that carries the depth down, and the right side view.

```python run
from collections import deque

class Node:
    __slots__ = ("val", "left", "right")
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None

def build(level):
    vals = iter(level)
    root = Node(next(vals))
    q = deque([root])
    while q:
        node = q.popleft()
        for side in ("left", "right"):
            v = next(vals, "end")
            if v == "end":
                return root
            if v is not None:
                setattr(node, side, Node(v))
                q.append(getattr(node, side))
    return root

def kids(node):
    return [c for c in (node.left, node.right) if c]

def by_levels(root):
    out, q = [], deque([root] if root else [])
    while q:
        width = len(q)                  # freeze: exactly one level is queued
        level = []
        for _ in range(width):
            node = q.popleft()
            level.append(node.val)
            q.extend(kids(node))        # the next level queues up behind
        out.append(level)
    return out

def by_levels_wrong(root):              # the C/Java bug: i < q.size() re-read
    out, q = [], deque([root])
    while q:
        level, i = [], 0
        while i < len(q):               # len(q) changes as nodes come and go
            node = q.popleft()
            i += 1
            level.append(node.val)
            q.extend(kids(node))
        out.append(level)
    return out

def by_depth_dfs(root):                 # the same answer, carrying depth down
    out = []
    def walk(node, d):
        if node is None:
            return
        if d == len(out):
            out.append([])
        out[d].append(node.val)
        walk(node.left, d + 1)          # left first keeps left-to-right order
        walk(node.right, d + 1)
    walk(root, 0)
    return out

tree = build([1, 2, 3, 4, 5, None, None, 6, None, None, 7, 9, None, None, 8])
right = by_levels(tree)
print("levels      :", right)
print("wrong length:", by_levels_wrong(tree))
print("dfs + depth :", by_depth_dfs(tree))
assert right == [[1], [2, 3], [4, 5], [6, 7], [9, 8]] == by_depth_dfs(tree)
assert by_levels_wrong(tree)[0] == [1, 2, 3]       # levels 0 and 1 merged

view = [level[-1] for level in right]
spine, node = [], tree
while node:
    spine.append(node.val)
    node = node.right
print("right view  :", view, "| right spine only:", spine)
assert view == [1, 3, 5, 7, 8] and spine == [1, 3]
```

Follow the wrong loop's first round by hand. The queue is [1], i = 0, 0 < 1: pop
1, push 2 and 3. Now i = 1 and the queue is [2, 3], so 1 < 2 is true: it pops 2,
which belongs to the next level. It pushes 4 and 5; i = 2, the queue is [3, 4, 5],
2 < 3: it pops 3 too. First "level": [1, 2, 3]. At the bottom the opposite happens:
pops shrink the queue faster than i grows, and the last level splits into [9] and
[8]. The fix is one word: **freeze** the width before the round.

The depth-first version gives the same lists. It is the "pass state down" idea:
the parent tells each child its depth, and the child files itself under that
depth. Use it when recursion is safe and you prefer it; use the queue when the
tree can be deep or when you need to stop at the first level that satisfies
something (the queue reaches shallow levels first, which is why the minimum depth
of a tree is a BFS question).

### Building a tree from two traversals

The last technique on the list runs the walk backwards. Given the preorder
(node, left subtree, right subtree) and the inorder (left subtree, node, right
subtree) of a tree with distinct values, rebuild the tree.
[[p:ebay-construct-tree-preorder-inorder|Construct a Binary Tree from Preorder and Inorder]]
is exactly this.

Derive it from what each order promises. Preorder's first value is the root,
always. Find that value in the inorder: everything to its left is the left
subtree, everything to its right is the right subtree. That tells you how many
nodes the left subtree has, and so where the right subtree starts in the preorder.
Recurse on both halves.

On the worked tree: preorder 1, 2, 4, 6, 9, 5, 7, 8, 3; inorder 9, 6, 4, 2, 5, 7,
8, 1, 3. The root is 1. In the inorder, 1 sits at position 7: seven values on its
left (9 6 4 2 5 7 8) form the left subtree, one value (3) the right. The next
preorder value, 2, is the root of the left subtree; 2 sits at position 3 of the
inorder, so 9 6 4 are its left subtree and 5 7 8 its right. And so on down.

Two lines need care. Finding the root in the inorder with a linear scan
(`inorder.index(v)`) costs the length of the slice each time, which is quadratic
on a chain; a dictionary from value to position, built once, makes it O(1). And
the order of the two recursive calls is not a style choice: if you read the
preorder with a moving pointer, the left subtree's values come next in the
preorder, so the left call must happen first.

```python run
class Node:
    __slots__ = ("val", "left", "right")
    def __init__(self, val):
        self.val, self.left, self.right = val, None, None

def preorder(n):
    return [] if n is None else [n.val] + preorder(n.left) + preorder(n.right)

def inorder(n):
    return [] if n is None else inorder(n.left) + [n.val] + inorder(n.right)

def rebuild(pre, ino, right_first=False):
    where = {v: i for i, v in enumerate(ino)}   # value -> inorder position, O(1)
    nxt = 0                                     # next unused preorder entry
    def make(lo, hi):                           # the subtree whose inorder is ino[lo:hi]
        nonlocal nxt
        if lo == hi:
            return None                         # empty slice: no subtree
        node = Node(pre[nxt])                   # preorder: the root comes first
        nxt += 1
        m = where[node.val]                     # left of m: left subtree; right: right
        if right_first:
            node.right = make(m + 1, hi)
            node.left = make(lo, m)
        else:
            node.left = make(lo, m)             # preorder lists the left subtree next
            node.right = make(m + 1, hi)
        return node
    return make(0, len(ino))

pre = [1, 2, 4, 6, 9, 5, 7, 8, 3]
ino = [9, 6, 4, 2, 5, 7, 8, 1, 3]
t = rebuild(pre, ino)
print("rebuilt  : pre", preorder(t), "in", inorder(t))
assert preorder(t) == pre and inorder(t) == ino
try:                                            # swap the two recursive calls
    bad = rebuild(pre, ino, right_first=True)
    outcome = "pre %s" % preorder(bad)
except IndexError:
    outcome = "IndexError: preorder ran out, slices no longer match"
print("right first:", outcome)
assert outcome.startswith("IndexError")

# preorder alone is ambiguous: 1 with child 2 on the left, or on the right
a, b = Node(1), Node(1)
a.left, b.right = Node(2), Node(2)
assert preorder(a) == preorder(b) == [1, 2] and inorder(a) != inorder(b)
print("pre [1,2]: inorder", inorder(a), "or", inorder(b), "- two different trees")

# the cost of finding the root with ino.index() instead of the map: a left chain
n = 400
pre_c, ino_c = list(range(n)), list(range(n - 1, -1, -1))
scanned = 0
def make_slow(lo, hi, nxt=[0]):
    global scanned
    if lo == hi:
        return None
    v = pre_c[nxt[0]]; nxt[0] += 1
    m = ino_c.index(v, lo, hi)
    scanned += m - lo + 1
    node = Node(v)
    node.left, node.right = make_slow(lo, m), make_slow(m + 1, hi)
    return node
make_slow(0, n)
print("left chain of %d: .index() scans %d cells; the map does %d lookups" % (n, scanned, n))
assert scanned == n * (n + 1) // 2
```

With the calls swapped, the right subtree of 1 (inorder slice [3]) takes the next
preorder value, 2, as its root, but 2 is not in that slice. From there the slices
stop meaning anything and the pointer runs off the end. The ambiguity check at the
bottom is why you need two traversals: preorder alone cannot say whether a lone
child is on the left or the right. A preorder with explicit null markers can, and
that is how trees are serialised ([[serialize-tree]]).

## Why it is correct

Two things need proving. First the structure: the facts about trees that every
walk in this chapter quietly uses, above all that a walk over children reaches
each node exactly once with no visited set. Then the walk itself: that the
post-order diameter returns the right numbers. The second proof is the template
for every "trust the children" recursion you will write.

:::proof Tree walks visit each node once, and the post-order walk finds the diameter
**Setup.** A tree is a finite, connected graph with no cycle. Root it at a node r.

**Fact 1: between two nodes there is exactly one simple path.** There is at least
one, because the graph is connected. Suppose there were two different ones from u
to v. Follow them from u until they first split, at a node x, and continue along
the first until it first meets the second again, at a node y. The two pieces from
x to y share only their ends, so together they form a cycle. There is no cycle, so
there were never two paths.

**Fact 2: every node except r has exactly one parent, and following parents from
any node reaches r.** Define the parent of v as the next node on the unique path
from v to r. Each step along parent pointers moves one edge closer to r along that
path, so the distance to r drops by one each time and the walk ends at r. Every
edge joins a node to its parent, and every non-root node has exactly one parent,
so there are exactly n - 1 edges.

**Fact 3: the subtrees of two different children are disjoint.** The subtree of v
is every node whose parent walk passes through v. If u were in the subtrees of two
children c1 and c2 of v, its parent walk would reach v once (distance only goes
down, so it cannot come back), arriving from exactly one node, c1 or c2, not both.
So the subtree of v is v itself plus the disjoint subtrees of its children.

**Fact 4: a recursion that calls itself on each child visits every node of the
subtree exactly once.** Induction on the size of the subtree. A leaf: one visit.
A node v whose children's calls each visit their own subtree exactly once: v is
visited once, by its own call, and by Fact 3 the children's subtrees do not
overlap, so nothing is visited twice, and together with v they cover v's subtree,
so nothing is missed. This is why no visited set is needed.

**The walk.** Claim: for every node v, `walk(v)` returns levels(v), the number of
nodes on the longest downward path from v, and when it returns, `best` is at least
the length of every path whose nodes all lie in v's subtree, and `best` is the
length of some real path.

*Base.* `walk(None)` returns 0, the levels of an empty tree, and changes nothing.

*Step.* Assume the claim for v's children (their subtrees are smaller). Then
l = levels(v.left) and r = levels(v.right).

- A downward path from v is v alone, or v followed by a downward path from one
  child. The longest has 1 + max(l, r) nodes, which is what `walk(v)` returns.
- Take any path P inside v's subtree. Its highest node is some node u (Step 1 of
  the derivation: a path rises then falls, so it has exactly one highest node).
  If u is not v, then P lies inside the subtree of one child of v, and by the
  assumption `best` was already at least its length when that child's call
  returned. If u is v, then P is a downward arm into the left subtree, plus v,
  plus a downward arm into the right subtree. Each arm is a downward path from a
  child, so the left arm has at most l nodes and the right arm at most r, and P has
  at most l + r edges. The line `best = max(best, l + r)` makes `best` at least
  that.
- `l + r` itself is the length of a real path: the longest left arm, v, and the
  longest right arm. Those two arms lie in different subtrees (Fact 3), so they
  share no node and the path is simple.

*Conclusion.* At the root, every path in the tree lies in the root's subtree, so
`best` is at least the diameter, and `best` is the length of a real path, so it is
at most the diameter. They are equal. The walk ends because each call recurses
only into strictly smaller subtrees. ∎
:::

The assumptions that argument used, in plain words, because that list is where
the bugs come from:

- **Finite, connected, no cycle.** Fact 1 needed "no cycle"; Fact 2 needed
  "connected". Take either away and the walk revisits nodes or misses them.
- **Exactly one parent per node.** Fact 3 is what makes "no visited set" safe.
  Give a node two parents and the subtrees overlap; the recursion still ends, but
  it walks the shared part once per parent, and a stack of such "diamonds" doubles
  the work at every layer.
- **The children's answers are complete before the node uses them.** That is
  what post-order buys. Read `l` before `walk(node.left)` has returned and you are
  using half an answer.
- **The returned value means exactly one thing.** The induction used "walk
  returns levels(v)" at the children. The wrong `return l + r + 1` breaks exactly
  this sentence, and the proof breaks at the same step the trace did.
- **Nothing used "two".** Replace left and right by a list of children and every
  step still holds; for the diameter you would combine the two largest child arms.
  So everything here is true of N-ary trees, and of each tree of a forest.

## What it costs

**Time: count the calls.** Fact 4 says each real node is visited once. In a
binary tree there are 2n child slots, n - 1 of them hold a node (one per edge),
so n + 1 are empty, and a recursion that calls itself on None makes exactly
n + (n + 1) = 2n + 1 calls. Each call does constant work besides its two
recursive calls. Total: Θ(n). The run block measured exactly 2n + 1.

As a recurrence, if the root's left subtree has k nodes:

```
T(n) = T(k) + T(n - 1 - k) + c,     T(0) = c
```

Guess T(n) = c(2n + 1) and check: c(2k + 1) + c(2(n - 1 - k) + 1) + c = c(2n + 1)
for every k. Unlike [[quicksort]], a lopsided split costs a walk nothing. The shape
of the tree never changes the total work.

**The brute force, for contrast.** Recomputing `levels` at every node costs the
sum of subtree sizes, which is the sum of (depth + 1) over all nodes: about
n log2 n for a balanced tree and n(n + 1)/2 for a chain. That is the hidden cost
of "call a helper at every node". Whenever a helper walks a subtree and you call it
from every node, you have written this sum. The cure is always the same: have the
walk return what the helper would compute.

**Space: the height, and the height is not log n.** The recursion holds one frame
per node on the current root-to-node path, so its peak is the height plus one.
Level i of a binary tree holds at most 2^i nodes, so a tree of height h holds at
most 2^(h+1) - 1 nodes, and

```
log2(n + 1) - 1  <=  h  <=  n - 1
```

At n = 100,000 that is anywhere from 16 to 99,999. CPython stops recursion at
about 1,000 frames by default. A recursive solution that passes every example and
dies on one hidden test with `RecursionError` is almost always a chain. Several
problems here say so in the constraints: "the tree may be skewed to a depth of
100000" in [[p:google-binary-tree-root-to-leaf-paths|All Root-to-Leaf Paths in a Binary Tree]].

**The queue's width.** Level-order BFS holds one level at a time, plus part of the
next. The widest level of a binary tree can hold about half the nodes (the bottom
level of a perfect tree has (n + 1)/2), so BFS costs Θ(n) memory in the worst case
where DFS costs Θ(h). On a chain the trade flips: the queue holds one node and the
recursion holds n. Pick the one whose bad case the input cannot produce.

**Costs people forget.**

- **Building the tree** from a level-order array is Θ(n) and allocates n objects.
  It is often the slowest part of a Python solution, and it is not optional.
- **Inverting a parent array** is Θ(n), and if the ids are strings you hash each
  one through a dictionary first.
- **Copying the path** at every leaf, as root-to-leaf paths requires, costs the
  path's length per leaf: up to Θ(n · h) in total output, which is the size of the
  answer and cannot be avoided, but copying at every *node* instead of every leaf
  can be.
- **`inorder.index(v)`** inside the rebuild is Θ(n) per call, Θ(n^2) on a chain.
  The dictionary is the fix.
- **Heap-indexed arrays** need 2^(h+1) - 1 slots, one per position. For a chain of
  60 nodes that is about 10^18. The representation, not the algorithm, explodes.

## How to think about it

Ask these on every tree problem, in this order, before writing code.

1. **What shape does the input arrive in?** Linked nodes, parent array, children
   lists, edge list, level-order array. Convert to linked nodes or children lists
   first; it is five lines and it removes a whole class of index bugs.
2. **Is it really a tree?** One parent per node, n - 1 edges, connected. If the
   statement promises it, believe it. If it does not, check, or treat it as a
   graph.
3. **Where is the root, and is there only one?** Several roots is a forest: loop
   over them, or add a virtual root whose children are the real roots.
4. **Which way does the information flow?** Does the answer at a node depend on
   its subtree (return it up), on its ancestors (pass it down), on both, or on its
   depth only (go across, by levels)?
5. **Write the contract in one sentence:** "walk(v, d) takes the depth d of v and
   returns the levels of v's subtree." If the sentence does not fit, you are
   returning the wrong thing. Return a pair, or a triple, until it does.
6. **Is the answer the root's return value, or a best over all nodes?** If the
   best structure (a path, a subtree) can sit anywhere, record it in an outer
   variable and return only the part a parent can extend.
7. **What are the base cases?** The empty tree; a leaf, meaning no children at
   all; a node with one child, which is not a leaf.
8. **Edges or nodes?** Read the statement's definition of depth, height, length.
   Write the convention in a comment above the function.
9. **How deep can it be?** If 10^5 is possible and the tree can be skewed, use an
   explicit stack or the reversed-preorder sweep in the Traps section.

### Telling it from its neighbours

- **Tree walk or graph search?** A tree walk needs no visited set because of
  Fact 3. A graph search ([[dfs]], [[bfs]]) does. If the statement gives
  undirected edges of a tree, you need only to remember the parent you came from,
  not a whole set.
- **DFS or BFS?** Use DFS (recursive or with a stack) for anything about subtrees
  or root-to-node paths. Use BFS for anything about levels, or for "the nearest"
  or "the shallowest" where you want to stop early. Level questions also have a
  DFS solution that carries the depth down.
- **A walk or a tree DP?** When the returned value is a small record per node and
  the node chooses among its children's records (rob this node or not, place a
  camera or not), the walk has become [[tree-dp]]. Same skeleton, more states.
- **A walk or a BST search?** If the tree has an ordering ([[bst]]), you often do
  not need to walk the whole tree: one comparison tells you which side to go to.
- **Traversal orders by name.** Preorder, inorder and postorder are the three
  moments a node can do its work: before its children, between them, after them.
  [[tree-traversal]] covers them and their iterative forms in full.

## Variations

### A. Return a value up: depth, size, counts

What changes: only what is returned and how children's values combine (max for
depth, sum for size, and so on). Why it works: each value is a fact about a
subtree, so the children's facts determine the parent's.

```
size(v)   = 1 + size(left) + size(right)
depth(v)  = 1 + max(depth(left), depth(right)),   depth(None) = 0
leaves(v) = 1 if v is a leaf, else leaves(left) + leaves(right)
```

[[p:linkedin-maximum-depth-of-binary-tree|Maximum Depth of Binary Tree]] is the
first line. [[p:inmobi-employee-subordinates|Employee Subordinates]] is subtree
size in disguise: an employee's subordinates are their subtree minus themselves,
and the input is a parent array of up to 2 x 10^5 people, deep enough that it
wants the iterative sweep in Traps.
[[p:drw-count-balanced-tree-nodes|Count Balanced Nodes in a Rooted Tree]] computes
sizes on an N-ary children list and then checks, at each node, whether all child
sizes are equal. [[p:atlassian-leaf-similar-trees|Leaf-Similar Trees]] returns
nothing but emits leaves into a list in left-to-right order; two trees are
leaf-similar if the lists match.

### B. Pass state down: depths, path sums, the path itself

What changes: the function takes an extra argument describing the path from the
root, and the answer is checked at a leaf (or at every node). Why: the needed fact
lives above the node, where the subtree cannot see it.

```
walk(v, need):   leaf -> need == v.val
                 else -> walk(left, need - v.val) or walk(right, need - v.val)
```

[[p:salesforce-path-sum|Path Sum]] is that. Collecting the paths themselves, as in
[[p:google-binary-tree-root-to-leaf-paths|All Root-to-Leaf Paths in a Binary Tree]],
carries a list down: append the node on entry, record a copy at a leaf, pop on the
way out. That append-recurse-pop shape is the same one [[backtracking]] uses, and
the copy is a trap demonstrated below. [[p:meta-sum-root-to-leaf-numbers|Sum Root-to-Leaf Numbers]]
passes `10 * value_so_far + digit` down.

### C. Both directions in one walk

What changes: the call takes something down and returns something up. Why: the
answer at a node needs both a fact from above and a fact from below. Example:
count the nodes that are larger than every ancestor ("good nodes"): pass the
maximum so far down, return the count up. Another: one walk that passes each
node its parent and its depth (both known from above) is all
[[p:amazon-classify-binary-tree-node-relationship|Classify Two Nodes as Siblings, Cousins, or Others]]
needs: same parent means siblings, same depth with different parents means
cousins.

### D. Level-order BFS

What changes: a queue, and the frozen width per round. Why: the answer is grouped
by depth, and a queue reaches nodes in order of depth.

- [[p:atlassian-binary-tree-level-order-traversal|Binary Tree Level Order Traversal]]:
  the template.
- [[p:bloomberg-binary-tree-right-side-view|Binary Tree Right Side View]]: keep
  the last node of each round.
- [[p:linkedin-binary-tree-zigzag-level-order|Binary Tree Zigzag Level Order Traversal]]:
  reverse every other level's list. Do not change the order you push children in;
  that breaks the next level.
- [[p:amazon-cousins-in-binary-tree-ii|Cousins in Binary Tree II]]: each node's
  new value is the sum of its level minus the sum of its own sibling group. One BFS
  computes level sums; a second pass (or the same one, done a level ahead) assigns.
  The trick is to see that "sum of cousins" is "level total minus my parent's
  children".

### E. Post-order combine, with a recorded best

What changes: the node returns one quantity and scores another. Why: the best
structure can bend at any node, and a bend cannot be extended upward.

- [[p:bloomberg-diameter-of-binary-tree|Diameter of a Binary Tree]]: return
  levels, score l + r.
- [[p:google-balanced-binary-tree|Balanced Binary Tree]]: return the height, or -1
  for "already unbalanced below"; fail if |l - r| > 1.
- [[p:arcesium-binary-tree-maximum-path-sum|Binary Tree Maximum Path Sum]]: the
  diameter with weights. Return `node.val + max(0, l, r)`, the best downward
  gain, where a negative arm is dropped by taking 0; score
  `node.val + max(0, l) + max(0, r)`. The answer can be a single negative node, so
  start `best` at minus infinity, not 0.
- [[p:google-maximum-leaf-to-leaf-path-sum|Maximum Sum Path Between Two Leaf Nodes]]:
  the same shape, but both ends must be real leaves, so a negative arm may not be
  dropped, and only a node with two children may score a bend. A one-child node
  must return through its only child.

### F. Build a tree from traversals

What changes: you consume a traversal and create nodes instead of visiting them.
Why it works: preorder (or postorder) names the root; inorder splits the rest into
left and right. [[p:ebay-construct-tree-preorder-inorder|Construct a Binary Tree from Preorder and Inorder]]
is the one to practise; [[p:amazon-construct-tree-level-inorder|Construct a Tree from Level-Order and Inorder Traversals]]
uses the level order to name roots instead. Preorder plus postorder is not enough
in general: a lone child could be on either side. A single preorder with null
markers is enough, and is how [[p:morgan-stanley-binary-tree-codec|Serialize and Deserialize a Binary Tree]]
works ([[serialize-tree]]).

### G. N-ary trees and forests

What changes: `for c in children[v]` instead of `left` and `right`. Combining
children means a sum, a max, or the two largest, over a list. Why it works: none of
the proof used "two". A forest of k trees on n nodes has n - k edges; handle it by
looping over the roots, or by inventing a virtual root above them, which is often
the shortest correct code. [[p:amazon-maximum-depth-of-nary-tree|Maximum Depth of an N-ary Tree]]
is variation A on a parent array.

Every N-ary tree is also a binary tree in disguise, the **left-child,
right-sibling** form: `left` points at the first child, `right` at the next
sibling. It loses nothing, not even the order of the children, and it lets binary
code run on any arity. The price is height: a node with k children becomes a chain
of length k.

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

### H. The preorder as an array: subtrees are contiguous blocks

What changes: you record the order nodes are first visited, and the size of each
subtree. Why it works: a depth-first walk enters a node and does not leave until
its whole subtree is done, so the subtree of v is exactly the block of size(v)
entries starting at v's position. [[p:imc-chain-of-command|Chain of Command]] is
this: the directive reaches people in preorder, so "the k-th person to hear it from
v" is one array lookup. Range questions about subtrees become range questions
about an array, which is where [[prefix-sums]] and [[segment-tree|segment trees]]
come in. Rare in interviews, common in OAs with large n.

### I. Deep trees: the iterative forms

What changes: an explicit stack replaces the call stack. Why: Python's recursion
limit. For top-down work (depth, path state), push `(node, state)` pairs on a
stack. For bottom-up work (sizes, heights, any post-order combine), take the
preorder with a stack, then loop over it **in reverse**: in a preorder every parent
comes before its whole subtree, so in the reversed list every child comes before
its parent, which is exactly the order post-order needs. That sweep is in the Traps
block. A true in-order iterative walk (needed for BSTs) is in [[tree-traversal]],
and the no-stack trick, [[morris-traversal]], is rare.

## Recognising it in a statement

Ordered by how much to trust them.

1. **The words root, leaf, subtree, depth, level, ancestor, parent.** They mean
   nothing outside a rooted tree.
2. **A parent column or array, `manager_id`, `bosses[i]`, `[parent, child]`
   pairs.** A tree spelled out as a table. Build children lists first.
3. **"n nodes and n - 1 edges, connected"**, with the word tree missing. That is a
   tree. Root it anywhere.
4. **Hierarchies from the real world:** an org chart, a file system, a comment
   thread, a reporting line, a taxonomy. Org charts are the favourite OA story.
5. **Nested output from flat input:** "return the hierarchy", "render the tree".
   Build children lists, then emit recursively.

Then the phrase tells you the direction:

| phrase | direction | technique |
| --- | --- | --- |
| "height", "depth of the tree", "size", "number of subordinates" | up | variation A |
| "root-to-leaf", "path from the root", "target sum along a path" | down | variation B |
| "level by level", "each level", "right side", "zigzag", "cousins" | across | variation D |
| "any two nodes", "may not pass through the root", "longest path", "balanced at every node" | up, with a recorded best | variation E |
| "given the preorder and inorder" | build | variation F |

The anti-signals, which matter more:

- **A node that can appear under two parents**, or edges that can form a cycle: a
  graph, needing a visited set.
- **"Tree" about the choices**, not the input: backtracking.
- **The tree has an ordering** ("left subtree values are smaller"): a [[bst]]
  question, where you can usually skip whole subtrees rather than walk them all.
- **Many distance or ancestor queries on one big tree:** preprocessing with [[lca]]
  or [[binary-lifting]], not one walk per query.

## Traps

**The recursion is right and dies anyway.** Symptom: every example passes, one
hidden case raises `RecursionError` or crashes the process. The constraint line
says 10^5 nodes and the tree can be a chain. Fix: an explicit stack, or the
reversed-preorder sweep.

**A shared path list.** Symptom: every recorded path comes out empty, or all of
them equal the last one. You appended the list object itself, and later appends
and pops changed it. Fix: record a copy (or a joined string) at the leaf, and pop
after the recursive calls.

Both traps, wrong and right, on real inputs:

```python run
import sys
sys.setrecursionlimit(1000)                 # CPython's default, as on most judges

# Trap 1: a recursion that is right and still dies on a deep tree
def subordinates_rec(bosses):
    n = len(bosses) + 1
    kids = [[] for _ in range(n + 1)]
    for i, b in enumerate(bosses):
        kids[b].append(i + 2)               # employee i+2 reports to b
    def size(v):
        return 1 + sum(size(c) for c in kids[v])
    return [size(v) - 1 for v in range(1, n + 1)]

def subordinates_iter(bosses):
    n = len(bosses) + 1
    kids = [[] for _ in range(n + 1)]
    for i, b in enumerate(bosses):
        kids[b].append(i + 2)
    order, stack = [], [1]
    while stack:                            # preorder: parent before child
        v = stack.pop()
        order.append(v)
        stack.extend(kids[v])
    size = [1] * (n + 1)
    for v in reversed(order):               # every child before its parent
        for c in kids[v]:
            size[v] += size[c]
    return [size[v] - 1 for v in range(1, n + 1)]

sample = [1, 1, 2, 2]                       # 1 -> 2, 3; 2 -> 4, 5
print("sample:", subordinates_iter(sample))
assert subordinates_iter(sample) == subordinates_rec(sample) == [4, 2, 0, 0, 0]
chain = list(range(1, 5000))                # employee i+1 reports to i
try:
    subordinates_rec(chain)
    print("recursive: survived")
except RecursionError:
    print("recursive: RecursionError at depth 5000 (limit %d)" % sys.getrecursionlimit())
ans = subordinates_iter(chain)
print("iterative: boss has", ans[0], "subordinates, last employee", ans[-1])
assert ans[0] == 4999 and ans[-1] == 0

# Trap 2: one path list shared by every answer
def paths_wrong(tree, v, path, out):
    path.append(v)
    if not tree.get(v):
        out.append(path)                    # stores the list itself
    for c in tree.get(v, []):
        paths_wrong(tree, c, path, out)
    path.pop()

def paths_right(tree, v, path, out):
    path.append(v)
    if not tree.get(v):
        out.append("->".join(map(str, path)))   # a snapshot, not the list
    for c in tree.get(v, []):
        paths_right(tree, c, path, out)
    path.pop()                              # undo before returning to the parent

tree = {1: [2, 3], 2: [4, 5]}
w, r = [], []
paths_wrong(tree, 1, [], w)
paths_right(tree, 1, [], r)
print("shared list:", w, "| snapshots:", r)
assert w == [[], [], []] and r == ["1->2->4", "1->2->5", "1->3"]
```

The shared list ends as three references to one empty list: by the time you print,
every pop has run. Nothing crashed, which is what makes it expensive to find.

**Returning the wrong thing.** Symptom: correct on chains and on the examples,
too large on bushy trees. You returned the bend instead of the arm. Demonstrated
in "From the idea to the code". The test: say what `walk` returns in one sentence,
and check that the `return` line computes exactly that.

**Answering at the root.** Symptom: wrong whenever the best path or subtree is off
to one side. Return the root's bend and you get 5 on the worked tree instead of 6.

**Checking the target at an internal node.** Symptom: true for a path that stops
in the middle of the tree. The check belongs at a leaf.

**Treating a one-child node as a leaf**, or **None as a leaf.** Symptom: minimum
depth comes out 1 on a tree whose root has one child; path sums accept paths that
end at a missing child. A leaf has no children at all. For minimum depth the
recursion must ignore an empty side rather than take min with its 0.

**Edges against nodes.** Symptom: every answer off by exactly one. Write the
convention above the function, from the statement's own words.

**Re-reading the queue length.** Symptom: the first two levels merge and the last
one splits. Freeze `width = len(q)` before the round.

**`[[]] * n` for children lists.** Symptom: every node appears to have every child.
It is n references to one list. Use `[[] for _ in range(n)]`.

**Trusting n - 1 edges as proof of a tree.** A triangle plus a lone node has
n - 1 edges and is neither connected nor acyclic. "Any two of connected, acyclic,
n - 1 edges" implies the third; one alone implies nothing.

**Forgetting a forest's other roots**, so one component is processed and the rest
dropped. And **keying a cache by node value**: two nodes can hold the same value.
Key by node or by index.

## What to memorise

The definition, because the recursion falls out of it: **a tree is a node plus a
list of trees.**

The sentence that turns a problem into code: **"walk(v) takes ___ from its parent
and returns ___ to its parent."** Fill both blanks before writing the body.

The habit: **return what can be extended, record what is finished.** If the answer
can sit anywhere in the tree, it goes in an outer variable, and the return value is
only the part a parent can build on.

The three templates:

```python
def walk(node):                       # up, with a recorded best
    nonlocal best
    if node is None:
        return 0
    l, r = walk(node.left), walk(node.right)
    best = max(best, l + r)           # finished: the bend here
    return 1 + max(l, r)              # extendable: one arm

def has_path(node, need):             # down
    if node is None:
        return False
    if node.left is None and node.right is None:
        return need == node.val       # check at a leaf, only at a leaf
    return has_path(node.left, need - node.val) or has_path(node.right, need - node.val)

q = deque([root])                     # across
while q:
    level = []
    for _ in range(len(q)):           # width frozen for this round
        node = q.popleft()
        level.append(node.val)
        q.extend(c for c in (node.left, node.right) if c)
    out.append(level)
```

Numbers worth carrying: n nodes, n - 1 edges; a binary tree with n nodes has
n + 1 empty child slots; height is between log2(n + 1) - 1 and n - 1; Python
recursion stops near 1,000 frames.

## Check yourself

:::check
Hand trace. The tree in level order is `[10, 5, 20, 3, 7, null, 30, null, null, 6, 8]`.
Draw it. Then fill the post-order table for the diameter: for each node in
post-order, the left and right reports, the bend, the return value and the best so
far. What is the diameter, and at which node does it bend?
--
The tree: 10 has children 5 and 20; 5 has 3 and 7; 20 has only a right child 30;
7 has 6 and 8. Post-order: 3, 6, 8, 7, 5, 30, 20, 10.

| node | left | right | bend | returns | best |
| --- | --- | --- | --- | --- | --- |
| 3 | 0 | 0 | 0 | 1 | 0 |
| 6 | 0 | 0 | 0 | 1 | 0 |
| 8 | 0 | 0 | 0 | 1 | 0 |
| 7 | 1 | 1 | 2 | 2 | 2 |
| 5 | 1 | 2 | 3 | 3 | 3 |
| 30 | 0 | 0 | 0 | 1 | 3 |
| 20 | 0 | 1 | 1 | 2 | 3 |
| 10 | 3 | 2 | **5** | 4 | **5** |

The diameter is 5 and it bends at the root this time: 6 (or 8), 7, 5, 10, 20, 30.
Node 5's bend (3 - 5 - 7 - 6) is only 3. Root bends happen; the point is that you
cannot assume them.
:::

:::check
Hand trace. Same tree, `[10, 5, 20, 3, 7, null, 30, null, null, 6, 8]`. Run
level-order BFS and write the queue at the start of every round, the width, and
the level produced. Then run the wrong loop that re-reads `len(q)` and write its
first level.
--
Right loop:

| round | queue at start | width | level |
| --- | --- | --- | --- |
| 1 | [10] | 1 | [10] |
| 2 | [5, 20] | 2 | [5, 20] |
| 3 | [3, 7, 30] | 3 | [3, 7, 30] |
| 4 | [6, 8] | 2 | [6, 8] |

The right side view is the last of each level: 10, 20, 30, 8. Note 8: it is not on
the right spine (10, 20, 30), but nothing at depth 3 is to its right.

Wrong loop, round 1: queue [10], i = 0 < 1, pop 10, push 5, 20; i = 1 < 2, pop 5,
push 3, 7; queue [20, 3, 7], i = 2 < 3, pop 20, push 30; queue [3, 7, 30], i = 3,
3 < 3 is false. First level: [10, 5, 20]. Two levels merged.
:::

:::check
Hand trace, information going down. The tree is `[5, 4, 8, 11, null, 13, 4, 7, 2]`
(so 11 has children 7 and 2; 8 has 13 and 4). Target 22. Write the `need` value on
arrival at each node the walk visits, in order, and stop when the answer is found.
Then answer the same question for target 9.
--
Target 22, left before right: 5 (need 22, after 17), 4 (17, after 13), 11 (13,
after 2), 7 (2, after -5: a leaf, -5 is not 0, false), 2 (2, after 0: a leaf,
**true**). The path 5 + 4 + 11 + 2 = 22. The walk stops there; 8 and its subtree are
never visited.

Target 9: the path 5, 4 adds to 9, but 4 is not a leaf (it has the child 11), so it
does not count. The leaves give 5+4+11+7 = 27, 5+4+11+2 = 22, 5+8+13 = 26,
5+8+4 = 17. None is 9: **false**. A solution that returns true when `need` hits 0
anywhere answers true here, which is the bug.
:::

:::check
Why does a depth-first walk over a tree need no `visited` set, while the same code
on a general graph does? Say exactly what goes wrong on an undirected graph with a
cycle, and on a DAG, if you leave the set out.
--
Because the subtrees of two different children are disjoint (Fact 3), so the
recursion can reach a node by only one route: through its one parent. That follows
from unique paths, which follows from "connected and acyclic".

Without the set, on an undirected graph with a cycle, the walk goes around the
cycle forever (and even without a cycle, it walks straight back along the edge it
came from, which is why tree code on undirected edges passes the parent along). On
a DAG it ends, but re-explores every shared part once per route into it; a stack of
k diamonds has 2^k routes to the bottom.
:::

:::check
Someone writes the diameter like this and says it passes the examples:

```
def walk(node):
    if node is None: return 0
    l, r = walk(node.left), walk(node.right)
    return max(l + r, l, r) + 1
```

and returns `walk(root) - 1`. Where are they wrong? Give the smallest tree on which
the answer is too large.
--
They return the bend (plus one) as if it could be extended. A parent then adds its
own edge onto a path that already goes down both sides of the child, which is not
a path.

It agrees with the right answer on every tree where no node below the root has
two children, because then l + r equals max(l, r). The smallest failure needs a
non-root node with two children: `[1, 2, null, 3, 4]`, a root whose only child 2
has two leaf children. The true diameter is 2 (3 - 2 - 4). Their walk: 3 and 4
return 1; node 2 returns max(2, 1, 1) + 1 = 3; the root returns max(3, 3, 0) + 1 =
4; minus 1 gives 3. Too large by one. The fix is to record `l + r` in an outer
variable and return `1 + max(l, r)`.
:::

:::check
Disguised problem. A company has employees 1..n; employee 1 is the director, and
`bosses[i]` is the boss of employee i + 2. For every employee, return the number of
people who report to them directly or indirectly. n can be 2 x 10^5. Reduce it to a
tree technique, say which direction the information flows, and say what goes wrong
with the obvious recursive solution.
--
It is subtree size: subordinates(v) = size(v) - 1, and size(v) = 1 + the sum of the
children's sizes. Information flows **up** (variation A). Build children lists from
the parent array (`kids[bosses[i]].append(i + 2)`), then compute sizes.

The obvious recursion is correct and can hit Python's recursion limit: the
hierarchy can be a chain 2 x 10^5 deep. Take a preorder with an explicit stack and
sweep it in reverse, adding each node's size into its parent; in reversed preorder
every child comes before its parent. Linear time, no recursion.
:::

:::check
Hand trace. Rebuild the tree from preorder `[3, 9, 20, 15, 7]` and inorder
`[9, 3, 15, 20, 7]`. At each step, write the root taken from the preorder, its
position in the inorder, and the left and right inorder slices. Then explain why
preorder `[1, 2, 3]` and postorder `[3, 2, 1]` do not determine a tree.
--
Root 3 (preorder[0]); in the inorder it is at position 1, so the left slice is [9]
and the right slice is [15, 20, 7]. Left: root 9 (preorder[1]), slice of one, no
children. Right: root 20 (preorder[2]), at inorder position 3, left slice [15],
right slice [7]. Then 15 (preorder[3]) and 7 (preorder[4]) as leaves. The tree is
3 with children 9 and 20; 20 with children 15 and 7.

For preorder 1, 2, 3 and postorder 3, 2, 1: the tree is a chain 1 - 2 - 3, but
each child could be a left child or a right child. Four different chains (left-left,
left-right, right-left, right-right) give exactly these two orders. Without the
inorder, nothing says which side a lone child is on.
:::
