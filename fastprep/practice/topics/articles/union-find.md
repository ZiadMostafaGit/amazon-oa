# Union-Find (Disjoint Set Union)

> Union-Find works because "are these two in the same group?" only needs every group to have one name, and a name can be reached by walking up a tree whose shape nobody cares about, so the structure is free to keep that tree flat.

## The problem it solves

Six people, numbered 0 to 5. Friendships arrive one at a time, and after each one
somebody asks a question.

| time | event | question asked |
|---|---|---|
| 1 | 0 and 1 become friends | are 0 and 1 in the same circle? |
| 2 | 2 and 3 become friends | how many circles are there? |
| 3 | 1 and 3 become friends | are 0 and 2 in the same circle? |
| 4 | 4 and 5 become friends | how many circles are there? |
| 5 | 0 and 2 become friends | did this friendship change anything? |

A "circle" means friends, friends of friends, and so on: a chain of friendships
connects you. The answers are yes; 4 circles ({0,1}, {2,3}, {4}, {5}); yes, through
0-1-3-2; 2 circles ({0,1,2,3}, {4,5}); and no, 0 and 2 were already in the same
circle, so the friendship at time 5 is redundant.

Look at time 3. Nobody said "0 and 2 are friends". The friendship 1-3 joined two
whole circles, and 0 and 2 came along. That is **transitivity**, and it is the
whole difficulty. A statement in this bank puts it in so many words: "membership is
transitive: members connected through any chain of direct relationships belong to
the same group". One new pair can change the answer for many pairs nobody
mentioned.

The first solution anyone writes is a search. Keep the friendships as a graph, and
for every question run a [[bfs]] or [[dfs]] from one person and see whether the
other is reached. That is correct. It is also slow when the questions keep coming.
A search touches every person and every friendship in the circle, so it costs up to
O(n + m) per question. [[p:bytedance-undirected-graph-path-existence|Path
Existence in an Undirected Graph]] allows n = 200,000 people and 200,000 edges; if
the edges and the questions are interleaved, 200,000 questions at 400,000 steps each
is 8·10^10 steps. No.

The second solution anyone writes is a label: give every person a circle number,
and when two circles merge, rewrite the number of everyone in one of them. The
question becomes "are the two labels equal?", which is one comparison. But a merge
now costs as many writes as the circle has members, and we will count below how bad
that gets.

Union-Find keeps the cheap question of the label and makes the merge cheap too. It
supports two operations on n items:

- `find(x)`: the name of the group x is in;
- `union(a, b)`: merge the group of a with the group of b.

Two items are in the same group exactly when `find` returns the same name for both.
With two small tricks, each operation costs, for every input a computer can hold,
at most a handful of steps.

### When it is the wrong tool

- **You need the path, or its length.** Union-Find knows that two items are
  connected and has forgotten how. "Shortest route", "fewest hops", "list the
  path": that is [[bfs]] or [[shortest-path]].
- **The relation is one-way.** "a follows b" is not symmetric. Union-Find treats
  every pair as two-way and gives a confident, wrong answer. Use
  [[strongly-connected]] or [[topological-sort]].
- **Things are removed, online.** A merge cannot be undone. If edges are deleted
  and you learn each deletion only when it happens, the structure has no answer.
  If you know all the deletions in advance, run time backwards (variation I).
- **One graph, one question.** If the whole graph is given at once and you are
  asked one thing about it, a [[dfs]] or [[flood-fill]] is just as fast and simpler
  to get right. Union-Find earns its place when the merges arrive over time, when
  you must process edges in a chosen order, or when you need a small fact about
  every group as it grows.

## Build it from the brute force

We will not start from the final structure. We will start from the label array a
beginner writes, find where it wastes work, and fix one waste at a time. The final
template will appear at the end as the obvious thing.

### Step 1: a label for everyone

Keep `label[x]`, the circle number of x. Start with `label = [0, 1, 2, 3, 4, 5]`:
everyone alone, named after themselves.

- "Are a and b in the same circle?" is `label[a] == label[b]`. One step.
- "a and b become friends": if the labels differ, every person whose label is
  `label[a]` gets the label `label[b]` instead.

On the example, after time 1 (0-1): `[1, 1, 2, 3, 4, 5]`. After time 2 (2-3):
`[1, 1, 3, 3, 4, 5]`. After time 3 (1-3): the old label of 1 is 1, so everyone
labelled 1 becomes 3: `[3, 3, 3, 3, 4, 5]`. The question "are 0 and 2 in the same
circle?" is `3 == 3`. Correct.

### You might think: "a merge only needs to relabel a and b"

This is the first instinct, and it is wrong. At time 3 the pair was (1, 3). Relabel
only person 1 to 3's label and you get `[1, 3, 3, 3, 4, 5]`. Person 0 still says 1.
Now "are 0 and 2 together?" answers `1 == 3`, false, and the truth is true.

The reason is transitivity again. The pair (1, 3) does not just move person 1. It
moves 1's whole circle, and person 0 is in it. A merge is an operation on two
**groups**, never on two people. Keep that sentence; it comes back as the most
common bug in the final code.

### Step 2: count it

Each question is one comparison. Each merge scans the array, so it is O(n), or at
best as many writes as the group being relabelled has members. How bad can that
be?

Merge person 1 into person 0's group, then person 2 into the group of 1, and so on,
always relabelling the big group to the newcomer's label:
`union(0,1), union(1,2), union(2,3), ...`. The k-th merge rewrites k people. The
total is 1 + 2 + ... + (n-1), about n²/2. For n = 200,000 that is 2·10^10 writes.
The questions are fast; the merges are hopeless.

### Step 3: notice the waste

Look at what the merge at time 3 actually did. It rewrote four cells,
`[1, 1, 3, 3]` to `[3, 3, 3, 3]`, and the only new fact was one sentence: "the
circle called 1 is now part of the circle called 3". Every member of circle 1 was
told the news individually. That is the waste: we wrote the same fact once per
member.

How else could the members find out? Instead of every member storing the *name*,
let every member store a **pointer to someone in the same circle who is closer to
the name**. The name itself is the person who points at themselves. To find your
circle's name, follow the pointers until they stop.

Then the merge at time 3 is one write. The name of 1's circle is 1, the name of 3's
circle is 3. Make 1 point at 3. Person 0 still points at 1, and 1 now points at 3,
so person 0 reaches 3 by walking two steps. Nobody else was touched, and everybody
in circle 1 now reaches the new name.

### The question that unlocks it

Why is that enough? Because a question never needs to know *which* circle a person
is in, as a number fixed forever. It only needs both people to arrive at the same
person when they look up. So ask:

**What is the least each item must store so that two items in the same group can
always find the same name?**

The answer is one pointer, toward the name. Not the name itself (that forces every
member to be rewritten on a merge), not the list of members (that is a copy of the
group), not the edges (that is the graph, which forces a search). One pointer per
item, and the agreement that the name is whoever points at themselves.

Say it a second way. The label array writes the answer down at every member. The
pointer array writes it down once, at the top, and lets each member look it up.
Moving the answer for a whole group then means changing one cell at the top.

The pointers form trees: one tree per group, with the name at the root. The array
is called `parent`, and `parent[x] = x` marks a root.

```
find(x):      while parent[x] != x: x = parent[x]     # walk to the root
              return x
union(a, b):  ra, rb = find(a), find(b)
              if ra != rb: parent[ra] = rb            # one write: hang a root under a root
```

### You might think: "the tree is the friendship graph"

It is not, and this matters more than anything else in the chapter. Look at what
the trees contain after the example. The friendship 2-3 became the pointer
`parent[2] = 3`. The friendship 1-3 became `parent[1] = 3`, not a link between 1
and 3 as people but between the two *roots*. If a later friendship joined 0 and 5,
it would become a pointer between the roots of their trees, which might be two
people who never met.

So the trees are not a record of who is friends with whom. They are a **naming
scheme**: the only promise is that every member of a group reaches the same root.
The shape of the tree, who points at whom inside it, is an accident of the order
the merges happened. And since nothing depends on the shape, we are free to change
it whenever that is convenient, as long as every member keeps reaching the same
root. Both speed-ups below are exactly that freedom.

### Step 4: count again, and find the new waste

A merge is now one write plus two finds. A find is a walk to the root, so its cost
is the depth of the tree. How deep can it get?

Feed the same bad sequence: `union(0,1), union(1,2), union(2,3), union(3,4),
union(4,5)`, with `parent[ra] = rb`. After `union(0,1)`: 0 points at 1. After
`union(1,2)`: root of 1 is 1, root of 2 is 2, so 1 points at 2. And so on. The
result is a chain, `0 -> 1 -> 2 -> 3 -> 4 -> 5`, and `find(0)` walks five steps. With
n items, a find costs n - 1 steps, and m finds cost m·n. We moved the waste from
the merge into the question, but the total is no better.

<svg viewBox="0 0 700 250" role="img" aria-label="the same five unions build two different trees: always hanging the first root under the second gives a chain 0 to 5 of depth five; hanging the smaller tree under the larger root gives a star with root 0 and every other node one step below it">
  <g>
    <text x="150" y="20" text-anchor="middle">parent[ra] = rb, always</text>
    <circle cx="40" cy="215" r="16"/>
    <text x="40" y="220" text-anchor="middle">0</text>
    <circle cx="85" cy="180" r="16"/>
    <text x="85" y="185" text-anchor="middle">1</text>
    <circle cx="130" cy="145" r="16"/>
    <text x="130" y="150" text-anchor="middle">2</text>
    <circle cx="175" cy="110" r="16"/>
    <text x="175" y="115" text-anchor="middle">3</text>
    <circle cx="220" cy="75" r="16"/>
    <text x="220" y="80" text-anchor="middle">4</text>
    <circle class="fill" cx="265" cy="40" r="16"/>
    <text x="265" y="45" text-anchor="middle">5</text>
    <line x1="52" y1="204" x2="73" y2="191"/>
    <line x1="97" y1="169" x2="118" y2="156"/>
    <line x1="142" y1="134" x2="163" y2="121"/>
    <line x1="187" y1="99" x2="208" y2="86"/>
    <line x1="232" y1="64" x2="253" y2="51"/>
    <text x="150" y="245" text-anchor="middle">find(0) walks 5 steps</text>
    <text x="520" y="20" text-anchor="middle">smaller tree under the larger root</text>
    <circle class="fill" cx="520" cy="70" r="16"/>
    <text x="520" y="75" text-anchor="middle">0</text>
    <circle cx="400" cy="170" r="16"/>
    <text x="400" y="175" text-anchor="middle">1</text>
    <circle cx="460" cy="170" r="16"/>
    <text x="460" y="175" text-anchor="middle">2</text>
    <circle cx="520" cy="170" r="16"/>
    <text x="520" y="175" text-anchor="middle">3</text>
    <circle cx="580" cy="170" r="16"/>
    <text x="580" y="175" text-anchor="middle">4</text>
    <circle cx="640" cy="170" r="16"/>
    <text x="640" y="175" text-anchor="middle">5</text>
    <line x1="408" y1="156" x2="510" y2="83"/>
    <line x1="465" y1="154" x2="512" y2="85"/>
    <line x1="520" y1="154" x2="520" y2="86"/>
    <line x1="575" y1="154" x2="528" y2="85"/>
    <line x1="632" y1="156" x2="530" y2="83"/>
    <text x="520" y="245" text-anchor="middle">every find walks at most 1 step</text>
  </g>
</svg>

The same five unions on the same six items, two trees. On the left, every merge
put the big tree under a newcomer, so everybody already in the tree got one step
deeper. On the right, every merge put the newcomer (a tree of size 1) under the big
tree's root, so only the newcomer got a step, and only one.

Concretely, after those five unions the left `parent` array is
`[1, 2, 3, 4, 5, 5]` and the right one is `[0, 0, 0, 0, 0, 0]`. Read the left one
from index 0: `parent[0] = 1`, `parent[1] = 2`, and so on to `parent[5] = 5`, five
reads. Read the right one: `parent[3] = 0`, `parent[0] = 0`, one read.

### Step 5: union by size

The fix is in the picture. When two trees merge, every node of the tree that goes
underneath gets one step deeper. So put the **smaller** tree underneath. Keep
`size[r]`, the number of items in the tree whose root is r, and hang the root of the
smaller tree under the root of the larger.

Why does that keep trees shallow? Follow one item x. Its depth grows by one only
when its tree goes under another tree, and with union by size, that other tree is
at least as big. So every time x gets one step deeper, the size of x's tree at least
doubles. Starting from size 1, it can double at most log₂ n times before it exceeds
n. So no item is ever deeper than log₂ n. For n = 200,000 that is 17 steps.

Say it a second way: to make a tree of depth d with union by size, you have to merge
two trees of depth d - 1, which needs at least twice as many items. Depth 1 needs 2
items, depth 2 needs 4, depth 17 needs 131,072. Depth costs items, exponentially.

There is a twin called **union by rank**: store an upper bound on the height
instead of the size, hang the shorter under the taller, and add one to the winner's
rank only on a tie. Same guarantee, same code shape. Size is more useful, because
problems ask for group sizes, and you get them for free.

### Step 6: path compression

One more waste. Every time you call `find(x)`, you walk from x to the root, and you
learn the root of every node on the way. Then you throw that knowledge away and
walk the same path next time.

Since the shape of the tree does not matter, keep the knowledge: while walking, point
nodes higher up. The simplest form is **path halving**: at each step, point the
current node at its grandparent, then move there.

```
while parent[x] != x:
    parent[x] = parent[parent[x]]    # skip one level
    x = parent[x]
```

On the chain `0 -> 1 -> 2 -> 3 -> 4 -> 5`, one `find(0)` re-points 0 at 2, 2 at 4,
and 4 at 5, and the array becomes `[2, 2, 4, 4, 5, 5]`: the walk from 0 is now three
steps instead of five, after a single call. A second `find(0)` makes it two. The
structure repairs itself as it is used.

With union by size and path compression together, the cost of m operations on n
items is O(m·α(n)), where α is the inverse Ackermann function. α(n) is at most 4
for any n that fits in the universe. Treat each operation as constant time; the
argument is in "What it costs".

Neither trick is needed for correct answers. Both only change which node points at
which, never which root a node reaches. That separation, correctness from the
pointers' meaning and speed from the pointers' shape, is the reason the structure
is so easy to extend.

### The technique in one sentence

**Name every group by one of its members, let every item point toward its group's
name, merge two groups by hanging the smaller name under the larger, and flatten
paths as you walk them.**

And the question that produced it: **what is the least each item must store so that
two items in the same group can always find the same name?** One pointer.

## Worked by hand

Seven items, 0 to 6, and six unions. Union by size; on a tie, the root of the first
argument stays on top. Path halving in `find`. `comps` counts the groups.

Start: `parent = [0, 1, 2, 3, 4, 5, 6]`, every size is 1, `comps = 7`.

| step | call | find(a) | find(b) | sizes | action | `parent` after | `comps` |
|---|---|---|---|---|---|---|---|
| 1 | union(1, 2) | 1 | 2 | 1 vs 1 | tie: 2 under 1, size[1] = 2 | `[0,1,1,3,4,5,6]` | 6 |
| 2 | union(3, 4) | 3 | 4 | 1 vs 1 | tie: 4 under 3, size[3] = 2 | `[0,1,1,3,3,5,6]` | 5 |
| 3 | union(2, 3) | 1 | 3 | 2 vs 2 | tie: 3 under 1, size[1] = 4 | `[0,1,1,1,3,5,6]` | 4 |
| 4 | union(5, 6) | 5 | 6 | 1 vs 1 | tie: 6 under 5, size[5] = 2 | `[0,1,1,1,3,5,5]` | 3 |
| 5 | union(0, 5) | 0 | 5 | 1 vs 2 | **0 under 5**, size[5] = 3 | `[5,1,1,1,3,5,5]` | 2 |
| 6 | union(1, 4) | 1 | 1 | | same root: nothing merges | `[5,1,1,1,1,5,5]` | 2 |

Every cell can be checked with a pen. Here is step 3 in words, the one that teaches
the most.

> The call is union(2, 3). I do not merge 2 and 3; I merge their **groups**. find(2):
> parent[2] = 1, parent[1] = 1, so the root is 1. find(3): parent[3] = 3, so 3 is
> its own root. Two different roots, so this is a real merge. Group 1 has size 2
> ({1, 2}), group 3 has size 2 ({3, 4}). A tie, so the first root, 1, stays on top,
> and I write parent[3] = 1. One write. Item 4 still points at 3, and 3 now points at
> 1, so 4 reaches 1 in two steps. size[1] becomes 4. There was one group fewer, so
> comps drops to 4.

Four more things in the table deserve a second look.

**Step 5 put the first argument underneath.** We called union(0, 5) and 5 ended up
the root: union by size cares which tree is larger, not which argument came first.
So never assume that a is still a name after union(a, b). Always ask `find`.

**Step 6 changed `parent` without merging anything.** find(1) is 1. find(4) walks
4 → 3 → 1, and halving rewrites `parent[4] = parent[parent[4]] = parent[3] = 1` on the
way. Both roots are 1, so nothing merges and comps stays 2, yet cell 4 moved. A
`find` is a read that writes. That is safe, because 4 reaches the same root before
and after, and it is why you cannot treat `parent` as a frozen record.

**Step 6 is also the answer to a whole family of problems.** "The union did
nothing" means the pair (1, 4) joined two items that were already connected. In
graph terms, the edge 1-4 closes a cycle; it is **redundant**. Redundant-edge
counting, cycle detection, and Kruskal's rule for skipping an edge are all this one
signal. That is why `union` should return whether it merged.

**You cannot recover the input from the final array.** The pair (2, 3) left no
2-to-3 pointer anywhere: `parent[2] = 1`, `parent[3] = 1`. The structure has kept
the grouping and thrown the edges away. That is the honest limit of the tool.

Here is the final forest, drawn from the array: root 1 with children 2, 3, 4; root 5
with children 0, 6. Group sizes 4 and 3, read at the roots: `size[1] = 4`,
`size[5] = 3`. Note that `size[3]` is still 2. It was correct when 3 was a root and
nobody updated it after 3 went underneath, because nobody needs to: a size is only
read at a root. Reading `size[3]` and believing it is a bug with a real symptom.

### A second trace: the chain, and what halving does to it

The first trace never built a deep tree, because union by size never lets it. To
see path halving work, switch union by size off and build the chain from Step 4:
`parent[ra] = rb`, unions (0,1), (1,2), (2,3), (3,4), (4,5). The array is
`[1, 2, 3, 4, 5, 5]`. Now call `find(0)` with halving and write down every step.

| x | parent[x] before | grandparent | write | `parent` after the write | next x |
|---|---|---|---|---|---|
| 0 | 1 | parent[1] = 2 | parent[0] = 2 | `[2, 2, 3, 4, 5, 5]` | 2 |
| 2 | 3 | parent[3] = 4 | parent[2] = 4 | `[2, 2, 4, 4, 5, 5]` | 4 |
| 4 | 5 | parent[5] = 5 | parent[4] = 5 | `[2, 2, 4, 4, 5, 5]` | 5 |
| 5 | 5 | | stop: 5 is a root | | |

The walk took three steps instead of five, because each step skipped a level.
After it, the depths of 0, 1, 2, 3, 4 are 3, 3, 2, 2, 1 instead of 5, 4, 3, 2, 1.
Call `find(0)` again: 0 → 2 → 4 → 5 with writes `parent[0] = 4` and `parent[4] = 5`,
array `[4, 2, 4, 4, 5, 5]`, and the next walk from 0 is two steps. Halving never
flattens everything at once. It halves the path you walked, every time you walk it,
and the proof in "What it costs" shows that this is enough.

The full version, **two-pass compression**, walks to the root first and then points
every node on the path straight at it: after one `find(0)` the array would be
`[5, 5, 5, 5, 5, 5]`. Same guarantee, but it needs either recursion (dangerous in
Python, see Traps) or a second loop. Halving is one line inside the loop you
already have. Use halving.

What the second trace shows that the first did not: compression changes cells you
never asked about (cell 2 moved during a find of 0), and it changes them only to
point at a node that is higher in the same tree. That second fact is the whole
reason it is safe.

## From the idea to the code

### The direct version: one pointer per item

First the structure as the derivation left it at Step 4: parent pointers, no
tricks. It gives correct answers, and the block measures how deep its trees get on
the bad input, so you can watch the cost appear.

```python run
def make(n):
    return list(range(n))                  # everyone is their own name

def find(parent, x):
    steps = 0
    while parent[x] != x:                  # walk until someone points at themselves
        x = parent[x]
        steps += 1
    return x, steps

def union(parent, a, b):
    ra, _ = find(parent, a)
    rb, _ = find(parent, b)
    if ra == rb:
        return False                       # already one group: nothing to do
    parent[ra] = rb                        # one write: a root under a root
    return True

# the six people from the opening
p = make(6)
answers = []
union(p, 0, 1); answers.append(find(p, 0)[0] == find(p, 1)[0])
union(p, 2, 3); answers.append(len({find(p, x)[0] for x in range(6)}))
union(p, 1, 3); answers.append(find(p, 0)[0] == find(p, 2)[0])
union(p, 4, 5); answers.append(len({find(p, x)[0] for x in range(6)}))
answers.append(union(p, 0, 2))             # did this friendship change anything?
print("answers:", answers)
assert answers == [True, 4, True, 2, False]

# the bad order: every union puts the big tree under a newcomer
n = 2000
p = make(n)
for i in range(n - 1):
    union(p, i, i + 1)
root, steps = find(p, 0)
print("chain of", n, "-> find(0) walks", steps, "steps")
assert steps == n - 1 and p[:6] == [1, 2, 3, 4, 5, 6]
total = sum(find(p, x)[1] for x in range(n))
print("asking every item once costs", total, "steps, about n^2/2 =", n * n // 2)
assert total == n * (n - 1) // 2
```

The answers are right; the cost is the chain. Two thousand items already cost two
million steps to ask about each one once. At 200,000 items that is 2·10^10.

### The optimised version: size and halving

```python run
import random

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))       # each item is its own root
        self.size = [1] * n                # read only at roots
        self.comps = n                     # number of groups

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                   # redundant: same group already
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra                # ra is now the larger root
        self.parent[rb] = ra               # hang the smaller root under it
        self.size[ra] += self.size[rb]
        self.comps -= 1
        return True

d = DSU(7)
for a, b in [(1, 2), (3, 4), (2, 3), (5, 6), (0, 5)]:
    assert d.union(a, b)
print("after five merges:", d.parent, "groups:", d.comps)
assert d.parent == [5, 1, 1, 1, 3, 5, 5] and d.comps == 2
print("union(1, 4) merged?", d.union(1, 4), "->", d.parent)
assert d.parent == [5, 1, 1, 1, 1, 5, 5] and d.comps == 2   # step 6 of the trace
assert d.size[d.find(4)] == 4 and d.size[d.find(0)] == 3
assert d.size[3] == 2                      # stale: 3 is not a root any more

def depth(parent, x):                      # walk without compressing
    steps = 0
    while parent[x] != x:
        x, steps = parent[x], steps + 1
    return steps

big = DSU(200000)                          # the bad order again
for i in range(199999):
    big.union(i, i + 1)
deepest = max(depth(big.parent, x) for x in range(200000))
print("200000 items in index order: deepest item is", deepest, "step from its root")
assert big.comps == 1 and deepest == 1

rng = random.Random(7)                     # cross-check against a graph search
for _ in range(300):
    n = rng.randint(1, 9)
    edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 12))]
    dsu, adj = DSU(n), [[] for _ in range(n)]
    for a, b in edges:
        dsu.union(a, b); adj[a].append(b); adj[b].append(a)
    comp = [-1] * n
    for s in range(n):
        if comp[s] < 0:
            comp[s], stack = s, [s]
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if comp[v] < 0:
                        comp[v] = s; stack.append(v)
    assert dsu.comps == len(set(comp))
    assert all((dsu.find(u) == dsu.find(v)) == (comp[u] == comp[v])
               for u in range(n) for v in range(n))
print("300 random graphs: group counts and every pairwise answer match a DFS")
```

The `depth` helper walks the parent pointers without compressing them, so it
measures the tree as it is. On the same input that made a chain of 2,000 in the direct
version, union by size keeps all 200,000 items one step from their root.

### Each line, and which part of the idea it is

| line | in plain words | in the derivation |
|---|---|---|
| `self.parent = list(range(n))` | everyone points at themselves | Step 1's "everyone alone, named after themselves" |
| `self.size = [1] * n` | every group has one member | Step 5's bookkeeping; meaningful only at roots |
| `self.comps = n` | n groups to start | the count the questions ask for |
| `while self.parent[x] != x` | not at a name yet | Step 3: follow pointers until they stop |
| `self.parent[x] = self.parent[self.parent[x]]` | skip a level on the way | Step 6, path halving |
| `ra, rb = self.find(a), self.find(b)` | find both **names** | "a merge is on two groups, never on two people" |
| `if ra == rb: return False` | same name: redundant | step 6 of the trace; the cycle signal |
| `if self.size[ra] < self.size[rb]: ra, rb = rb, ra` | make ra the larger | Step 5, union by size |
| `self.parent[rb] = ra` | the one write | Step 3's "the news is told once, at the top" |
| `self.size[ra] += self.size[rb]` | the new root's size | the merged group's size |
| `self.comps -= 1` | one group fewer | only reached when a real merge happened |

Three lines do the real work: the two finds, the equal-roots test, and the one
write. The rest is bookkeeping.

Settle three boring confusions now.

- **Items must be 0..n-1.** If the input numbers people 1..n, allocate n + 1 slots
  and ignore slot 0, or subtract 1 on the way in. If the items are strings (emails,
  user names), give each a number with a dictionary first. The structure only
  understands indices.
- **`find` is a loop, not a recursion.** The recursive version
  `return x if parent[x] == x else find(parent[x])` is pretty and dies with
  `RecursionError` in Python once a chain is deeper than the recursion limit (1,000 by
  default; a judge that raises it to 20,000 still loses to a chain of 10^5).
- **`size[x]` is not the size of x's group.** `size[find(x)]` is. The cell at a
  non-root is a fossil from when it was a root.

### The subtle line, both ways

The line that goes wrong is the write. The correct line is `parent[rb] = ra`, a
root under a root. The tempting one is `parent[b] = ra`: "b joins a's group". It
looks like the same thing. It is the "relabel only a and b" mistake from Step 1,
come back in the pointer version.

Take five items and three unions: (0, 1), (2, 3), (0, 3). Truth: {0, 1, 2, 3} is
one group and {4} is alone, two groups.

**Root under root (correct).**

| call | ra | rb | write | `parent` after |
|---|---|---|---|---|
| union(0, 1) | 0 | 1 | parent[1] = 0 | `[0, 0, 2, 3, 4]` |
| union(2, 3) | 2 | 3 | parent[3] = 2 | `[0, 0, 2, 2, 4]` |
| union(0, 3) | 0 | 2 | parent[**2**] = 0 | `[0, 0, 0, 2, 4]` |

Roots: 0 and 4. Every one of 0, 1, 2, 3 reaches 0 (item 3 by 3 → 2 → 0). Two groups.

**Element under root (wrong).**

| call | ra | b | write | `parent` after |
|---|---|---|---|---|
| union(0, 1) | 0 | 1 | parent[1] = 0 | `[0, 0, 2, 3, 4]` |
| union(2, 3) | 2 | 3 | parent[3] = 2 | `[0, 0, 2, 2, 4]` |
| union(0, 3) | 0 | 3 | parent[**3**] = 0 | `[0, 0, 2, 0, 4]` |

Look at the last row. Item 3 used to point at 2, its group's root. The write
re-pointed 3 at 0, and **nothing points at 2 any more except 2 itself**. Item 2 has
been cut out of its own group: roots are now 0, 2, 4. "Are 0 and 2 together?"
answers no. In the first two rows the two versions agree, because b happened to be
a root. The bug appears only when b is not a root, which is exactly when the groups
are interesting.

What does the wrong line compute? Not garbage: it computes "move the single item b
into a's group", which leaves b's former groupmates behind. That is the label
version's "relabel only b" bug, and the same counterexample shape (a group of two,
joined through its non-name member) kills both. A merge is on two groups.

```python run
def find(p, x):
    while p[x] != x:
        p[x] = p[p[x]]
        x = p[x]
    return x

def run(n, pairs, write_root, trace=True):
    p = list(range(n))
    for a, b in pairs:
        ra, rb = find(p, a), find(p, b)
        if ra != rb:
            target = rb if write_root else b          # the subtle line
            p[target] = ra
        if trace:
            print("   union(%d, %d): ra=%d rb=%d  write parent[%d] -> %s"
                  % (a, b, ra, rb, rb if write_root else b, p))
    snapshot = p[:]                                   # before any find compresses it
    return snapshot, sorted({find(p, x) for x in range(n)})

pairs = [(0, 1), (2, 3), (0, 3)]
print("root under root:")
good, good_roots = run(5, pairs, True)
print("element under root:")
bad, bad_roots = run(5, pairs, False)
print("roots:", good_roots, "vs", bad_roots)
assert good == [0, 0, 0, 2, 4] and good_roots == [0, 4]
assert bad == [0, 0, 2, 0, 4] and bad_roots == [0, 2, 4]   # 2 was cut off
assert find(good[:], 2) == find(good[:], 0) and find(bad[:], 2) != find(bad[:], 0)

# the wrong write is harmless whenever b happens to be a root
pairs2 = [(0, 1), (1, 2), (2, 3)]                          # b is always a fresh item
assert run(5, pairs2, True, False)[1] == run(5, pairs2, False, False)[1] == [0, 4]
print("chain-shaped input: both give", run(5, pairs2, False, False)[1], "(the samples pass)")
```

The last assert is the reason this bug survives: on inputs where every union brings
in a brand-new item, b is always its own root, and the two lines agree. Sample tests
are often exactly that shape.

### A second subtle line: count from the bool

`comps -= 1` must happen only when the roots differed. If you decrement for every
pair, a redundant pair (step 6 of the trace) lowers the count without merging
anything, and the count is now one too low forever. The habit that prevents it is
the `return True / return False`: let `union` say whether it merged, and update
every counter, every total, every Kruskal sum from that answer and nowhere else.
The Traps section demonstrates it.

## Why it is correct

A data structure is correct when two things hold: every operation keeps a stated
promise (the **invariant**), and the promise implies the answers it gives. So state
the promise first, then check each operation against it.

:::proof The forest names exactly the groups formed by the unions so far
**The setting.** Let P be the list of pairs passed to `union` so far. Say u and v
are **joined** if u = v, or a chain u = x0, x1, ..., xk = v exists with every
consecutive pair (x_i, x_{i+1}) in P (in either order). Being joined is the
grouping the problems ask about: it is transitive by construction.

**The promise.** At every moment:

1. **(Trees.)** Following `parent` from any item stops, after finitely many steps,
   at an item r with `parent[r] = r`. Call r the root of the item.
2. **(Names.)** Two items have the same root exactly when they are joined.
3. **(Counts.)** For every root r, `size[r]` is the number of items whose root is r,
   and `comps` is the number of roots.

**At the start.** `parent[x] = x` for all x: every item is a root, reached in zero
steps, so (1) holds. P is empty, so items are joined only to themselves, and items
have the same root only when they are the same item: (2) holds. Every root has one
item, `size` is all 1, and there are n roots with `comps = n`: (3) holds.

**`find(x)` keeps the promise.** Define the depth of an item as the number of
steps from it to its root, finite by (1). Each loop step moves x one level up, so the
loop ends after at most depth(x) steps, at x's root. The halving write sets
`parent[x]` to x's grandparent, which is in the same tree and strictly closer to the
root. Pointing an item at a strictly higher item of the same tree cannot create a
loop, and the item still reaches the same root. So every item's root is unchanged:
(1), (2) and (3) all still hold, and P did not change.

**`union(a, b)` keeps the promise.** It computes ra and rb, the roots of a and b.

*If ra = rb*, then by (2) a and b were already joined, and adding the pair (a, b) to P
joins nothing new: any chain using the new pair can be rerouted through the old
chain from a to b. Nothing is written, so all three parts still hold.

*If ra ≠ rb*, then a and b were not joined, and adding (a, b) merges exactly two
groups, the group of a and the group of b, and changes no other group. The code
writes `parent[rb] = ra` (after possibly swapping names so that ra is the larger).
rb was a root and now points into a different tree, so following pointers from any
item of rb's tree now continues to ra and stops: (1) holds and no loop was made,
because nothing in ra's tree points into rb's tree. Items of the two trees now all
have root ra, which is exactly the merged group, and no other item's root changed:
(2) holds. `size[ra]` becomes the sum of the two sizes, which is the merged group's
count; rb is no longer a root, so (3) says nothing about `size[rb]`; one root
disappeared and `comps` drops by one: (3) holds.

**So the answers are right.** By (2), `find(u) == find(v)` is true exactly when u
and v are joined by the pairs given so far, which, when the pairs are the edges of
an undirected graph, means "u and v are in the same connected component". By (3),
`comps` is the number of components and `size[find(x)]` is the size of x's.

**Termination.** Every loop in `find` runs at most depth(x) times, a finite number by
(1), and `union` is two finds and a constant number of writes. ∎
:::

The proof leaned on these facts. Each is a place a variant or a bug breaks the
method.

- **Only merges, never splits.** "Joined" only grows as P grows. Nothing in the
  argument survives deleting a pair. That is why deletions need time reversal.
- **The write links two roots.** The "no loop" step and the "exactly the merged
  group" step both used that rb was a root. `parent[b] = ra` for a non-root b breaks
  (2), as the demonstration showed.
- **`size` is promised only at roots.** Part (3) says nothing about `size[3]` after
  3 went underneath. Reading it is reading outside the promise.
- **`comps` drops only in the second case.** The first case writes nothing. A
  decrement there breaks (3), and no later step repairs it.
- **The relation is symmetric.** "Joined" uses pairs in either order. A one-way
  relation is not an equivalence, and the structure will silently make it two-way.
- **Union by size and compression never appeared as reasons.** They appear only as
  "possibly swapping" and "point at a higher item of the same tree", which were
  shown to keep the promise, not to create it. A structure without them is correct,
  only slow. If your answers are wrong, look elsewhere first.

## What it costs

Every operation is one or two walks up a tree plus a few writes. So the whole
question is: **how deep can the trees get?** Answer it three times, for three levels
of care.

**No tricks.** The chain from Step 4: unions in index order make a path of n items,
and a find at the bottom costs n - 1 steps. m operations can cost Θ(m·n). The
direct version's run measured exactly n(n-1)/2 for asking every item once. And note
that the bad order is not exotic: it is what an edge list sorted by index, or a line
of houses built left to right, produces.

**Union by size alone: O(log n) per operation, worst case.** The doubling argument
from Step 5, said carefully. Fix an item x. Its depth increases by exactly one when
the root above it is hung under another root, and union by size only does that when
the other tree is at least as large. After the merge, x's tree has at least twice
the items it had. So if x has been pushed down d times, its tree has at least 2^d
items. A tree has at most n items, so 2^d ≤ n and d ≤ log₂ n. No item is ever deeper
than log₂ n, and every find is O(log n), with no averaging needed.

**Union by size and path compression: O(α(n)) amortised.** This is the famous bound.
Here is why it is believable, in four facts. Use rank (an upper bound on height)
for the argument; size gives the same bound.

1. Ranks strictly increase going up any parent pointer. Linking keeps this, and
   compression only re-points an item at a higher ancestor, which has an even
   higher rank.
2. A non-root's rank never changes again.
3. A root of rank r has at least 2^r items under it (the doubling argument again),
   so at most n / 2^r items ever reach rank r, and no rank exceeds log₂ n.
4. Group the ranks into blocks that grow like towers of 2: {0}, {1}, {2}, {3, 4},
   {5..16}, {17..65536}, and so on. There are log* n blocks, the number of times you
   take a logarithm of n before reaching 1, which is 5 for any n below 2^65536.

Now charge every step of every find walk. A step from an item to a parent in a
**higher block** is charged to the find; a walk crosses each block once, so a find
pays at most log* n of these. A step to a parent in the **same block** is charged to
the item; after the walk, compression points that item at something of strictly
higher rank, so each such charge raises the rank of the item's parent, and once the
parent's rank leaves the block, this item is never charged in this block again. An
item whose rank sits in block (a, 2^a] can be charged at most 2^a times, and by fact
3 at most n / 2^a items have rank in that block, so the block costs at most n in
total, and all blocks together O(n log* n). So m operations cost
O((m + n) log* n). Tarjan's sharper count replaces log* with α, the inverse
Ackermann function, and proved it cannot be beaten by this kind of structure. α(n)
≤ 4 for every n you will ever see. Call it constant.

**Space.** Two integer arrays of n, plus a counter. If you carry extra data per root
(a min, a max, an edge count), one more array per fact.

**The costs people forget** are outside the structure.

- **Turning objects into indices.** [[p:oracle-accounts-merge|Accounts Merge]] hands
  you email strings. Every union first hashes two strings to get their indices
  ([[hash-tables]]). On string-heavy inputs the hashing costs more than the α.
- **Sorting.** When the edges must be processed by weight or by time (Kruskal,
  earliest connection), the union-find part is O(E·α) and the sort is O(E log E). The
  sort is the real cost.
- **Building edges that are not given.** In
  [[p:nutanix-min-cost-to-connect-all-points|Min Cost to Connect All Points]] every
  pair of points is a possible edge: 1,000 points make about 500,000 edges, which is
  fine. At 10^5 points, 5·10^9 edges are not, and
  [[p:tiktok-server-network-optimization|TikTok Server Network Optimization]] is
  about proving that only O(n) of them can matter.

## How to think about it

Ask these questions, in this order, on every problem that smells of groups.

1. **What are the items?** People, cells, accounts, variables, houses. Can I number
   them 0..n-1? If they are strings or coordinates, map them first. A grid cell (r, c)
   becomes r·cols + c.
2. **What is the "same group" relation, and is it an equivalence?** It must be
   symmetric (a with b means b with a) and transitive (chains count). If the
   statement says "directly or indirectly", "transitive", or "connected through",
   yes. If it is one-way, stop.
3. **Does the relation only grow?** Only merges: Union-Find. Deletions known in
   advance: reverse time. Deletions online: not this structure.
4. **What is asked?** "Same group?" (compare roots), "how many groups?" (the
   counter), "how big is this group?" (size at the root), "did this edge do
   anything?" (the bool), "when did everything connect?" (the moment comps hits 1).
5. **What does each group need to remember?** If the answer needs a fact about each
   group, a size, a min, a max, a sum, an edge count, it lives at the root and is
   combined in `union`. If it needs a fact about each item **relative to the
   group**, a ratio, a parity, an offset, it lives on the pointer (weighted DSU).
6. **Does the order of the pairs matter?** If the answer is "the first moment",
   "the cheapest way to connect", or "the best bottleneck", sort the pairs by the
   right key first and union in that order. That is Kruskal and its relatives.
7. **Is it really one static graph and one question?** Then a DFS is simpler. Use
   Union-Find when merges and questions interleave, or the processing order is
   chosen by you.

Then, before typing, write three lines: **what an item is**, **what one union
means**, and **which bool or root fact gives the answer**. If you cannot write them,
you do not have the reduction yet.

### Telling it from its neighbours

- **[[dfs]] / [[bfs]] / [[flood-fill]].** Same answers on a static graph, one pass.
  The tell for Union-Find is that the graph grows while you are asked about it, or
  that you add edges in a sorted order and stop at a moment.
- **[[minimum-spanning-tree]].** Kruskal is Union-Find plus a sort. If the problem
  says "connect everything as cheaply as possible", it is an MST, and the union-find
  bool decides each edge.
- **[[shortest-path]].** Anything that sums along a route. The near miss is a route
  whose cost is a **single** edge, the largest or smallest on it. Those
  "bottleneck" questions are answered by Union-Find in sorted order, or by a
  modified Dijkstra; see variation F.
- **[[bipartite]].** "Split into two sides so every pair is split" is a 2-colouring.
  A DFS colours it; a DSU with a parity bit on each pointer does it as pairs arrive.
- **[[topological-sort]] and [[strongly-connected]].** Directed relations. Never
  Union-Find.

## Variations

Eleven variations. A to F are the everyday ones, and every one of them appears in
this bank's interview problems. G and H are regular. I, J, K are less common, and K
is rare outside competitive programming.

### A. Count the groups as edges arrive

**What changes.** Nothing in the structure. Start `comps = n`, subtract one for every
union that returns True, read `comps` whenever asked.

**Why.** Each real merge turns two groups into one, so it lowers the count by
exactly one; a redundant pair changes nothing. The counter is a running total of
the bools.

**Example.** n = 4, pairs (0,1), (2,3), (1,0): counts 3, 2, 2. The third pair
returns False.

**Bank.** [[p:sambanova-number-of-provinces|Number of Provinces]] (the matrix
isConnected is the pair list; union every i < j with a 1, read comps),
[[p:amazon-count-connected-components|Count Connected Components]], and the online
version [[p:spacex-number-of-islands-ii|Number of Islands II]]: each new land cell
adds one island, then each union with an already-land neighbour that returns True
removes one. Repeated positions must change nothing, so check "already land" before
adding.

A disguise worth knowing: [[p:visa-minimum-score-path-between-cities|Minimum Score
of a Path Between Cities]] sounds like a shortest-path problem, but roads may be
reused, so any road in city 1's group can be visited on some route from 1 to n. The
answer is the smallest road weight in that group: union all roads, then take the
minimum over roads whose ends share city 1's root.

### B. Find the redundant edge

**What changes.** Use the bool. An edge whose union returns False joins two items
already in one group: it closes a cycle, and removing it disconnects nothing.

**Why.** By the proof's first case, a False union means a chain already joined the
two ends, so this edge plus that chain is a cycle.

**Example.** Edges (0,1), (1,2), (0,2), (3,4) on 5 items: the third returns False,
redundant. Components 2. To connect everything you need components - 1 = 1 more
edge, and you have 1 redundant edge to move, so the answer is 1.

**Bank.** [[p:inmobi-minimum-connection-changes|Minimum Connection Changes]] is
exactly that example: count redundant wires r and components c; you need c - 1 moves,
and it is possible exactly when r ≥ c - 1 (equivalently, total wires ≥ n - 1). The
related [[p:inmobi-minimum-edges-to-connect-components|Minimum Edges to Connect All
Components]] needs only c - 1. [[p:anyscale-redundant-connection-ii|Redundant
Connection II]] is the directed version, where a node may have two parents; it is
much harder and combines this test with in-degree reasoning.

### C. Union by rank and path compression

**What changes.** These are Steps 5 and 6 of the derivation. The variations are only
in how you write them.

- *Rank instead of size.* `rank[r]` is an upper bound on height; hang lower under
  higher, and on a tie add one to the winner. Same bounds. Use size when the problem
  asks about sizes, which is often.
- *Two-pass compression instead of halving.* Walk to the root, then a second loop
  re-points every node on the path at it. Same bound. Halving is one line.
- *Recursive compression.* `parent[x] = find(parent[x])`. Correct and elegant, and it
  crashes Python on a chain deeper than the recursion limit, before it has compressed
  anything.

**Why it matters which you use.** It does not for correctness. It does for
[[p:bytedance-undirected-graph-path-existence|Path Existence in an Undirected
Graph]], where 2·10^5 edges in an unlucky order give a chain unless one of the tricks
is on, and the recursive version fails on exactly that chain.

### D. Carry extra data at the root: sizes, minimums, counts

**What changes.** One more array per fact, initialised for single items, combined in
`union` next to the size, read only at `find(x)`.

**Why.** Any fact about a group that can be computed from the facts of its two halves
(a sum, a min, a max, a count) survives merging in O(1). The root is the group's one
address, so that is where the fact lives.

**Example.** Track `lo[r]` and `hi[r]`, the smallest and largest label. Items 0..5,
pairs (0,4), (4,2), (1,5). Groups {0,2,4} with lo 0, hi 4, and {1,5} with lo 1, hi 5,
and {3}. The largest hi - lo is 4.

**Bank.** That example is [[p:akuna-maximum-difference|Maximum Difference]].
[[p:atlassian-connected-sum|Connected Sum]] needs the size of every group (sum of
ceil(sqrt(size)) over the roots). [[p:roblox-longest-contiguous-house-segment|Longest
Contiguous House Segment]] unions each new house with its standing neighbours on the
line and keeps the best size seen so far. [[p:doordash-get-sizes-of-friends-groups|Get
Sizes of Friends Groups]] interleaves merges with size questions.
[[p:visa-minimum-unreachable-warehouses|Minimum Unreachable Warehouses]] carries an
edge count next to the vertex count: a group with edges = vertices - 1 is a tree and
must leave one warehouse unreachable, any other group can leave none.
[[p:amazon-count-complete-components|Count the Number of Complete Components]] uses
the same pair: a group of k items is complete exactly when it holds k(k-1)/2 edges.

Edge counts need one care: add one for **every** edge, including redundant ones,
because a redundant edge is still an edge of the group. So `edges[find(a)] += 1`
happens after the union, whether it merged or not, and the merge adds
`edges[ra] += edges[rb]`.

### E. Weighted union-find: a relation on every pointer

**What changes.** Each pointer carries a number: `w[x]` is how x relates to
`parent[x]`. For division, `w[x] = x / parent[x]`. `find` multiplies the weights
along the path to get x / root, and compression stores that product so the pointer
can go straight to the root.

**Why.** The relation is transitive in a way you can compute: if x / p = 2 and
p / root = 3, then x / root = 6. Two items with the same root can then be compared by
going through the root: c / d = (c / root) / (d / root).

**The merge.** Given a / b = v, with a / ra = wa and b / rb = wb, hang ra under rb
with weight ra / rb = (a / wa) / (b / wb) = v · wb / wa.

**Bank.** [[p:apple-evaluate-division|Evaluate Division]]. With a parity bit instead
of a ratio (x is on the same side as its parent, or the opposite side), the same
structure tests [[p:coupang-possible-bipartition|Possible Bipartition]] as dislikes
arrive: a dislike between two items of the same group with equal parity is a
contradiction.

```python run
def make():
    return {}, {}                                  # parent, weight (x / parent[x])

def find(parent, w, x):
    path = []
    while parent[x] != x:                          # walk up, remember the path
        path.append(x)
        x = parent[x]
    root = x
    for node in reversed(path):                    # nearest the root first
        p = parent[node]
        if p != root:
            w[node] *= w[p]                        # w[p] is already p / root
        parent[node] = root                        # compress
    return root

def add(parent, w, x):
    if x not in parent:
        parent[x], w[x] = x, 1.0

def union(parent, w, a, b, v):                     # a / b = v
    add(parent, w, a); add(parent, w, b)
    ra, rb = find(parent, w, a), find(parent, w, b)
    if ra != rb:
        parent[ra] = rb
        w[ra] = v * w[b] / w[a]                    # ra / rb

def query(parent, w, c, d):
    if c not in parent or d not in parent:
        return -1.0
    if find(parent, w, c) != find(parent, w, d):
        return -1.0
    return w[c] / w[d]                             # (c / root) / (d / root)

parent, w = make()
for (a, b), v in [(("a", "b"), 2.0), (("b", "c"), 3.0), (("x", "y"), 4.0), (("c", "y"), 0.5)]:
    union(parent, w, a, b, v)
for c, d, want in [("a", "c", 6.0), ("b", "a", 0.5), ("a", "y", 3.0), ("x", "a", 4 / 3),
                   ("a", "e", -1.0), ("e", "e", -1.0), ("x", "x", 1.0)]:
    got = query(parent, w, c, d)
    print("%s / %s = %.4f" % (c, d, got))
    assert abs(got - want) < 1e-9, (c, d, got)
```

Check one line by hand: a / b = 2 and b / c = 3 give a / c = 6. Then c / y = 0.5
links the two groups, so a / y = 6 · 0.5 = 3, and x / a = (x / y) / (a / y) = 4 / 3.

### F. Process the edges in sorted order: Kruskal and offline thresholds

**What changes.** The structure is the same. The order is yours: sort the pairs by a
key, union in that order, and read the answer at the right moment.

**Why.** Many questions are about the *first* moment something becomes connected, as
a threshold grows. Union-Find's groups only grow, so "connected after the first k
edges" is monotone in k, and one pass in sorted order meets every threshold in turn.

- **Minimum spanning tree (Kruskal).** Sort edges by weight, cheapest first; keep an
  edge exactly when union returns True; stop after n - 1 kept edges. The kept edges
  are a cheapest network that connects everything ([[minimum-spanning-tree]], with
  the exchange argument from [[greedy-exchange]]).
  [[p:nutanix-min-cost-to-connect-all-points|Min Cost to Connect All Points]] is
  Kruskal over all pairs of points.
- **Earliest moment of full connection.** Sort the events by time, union in order,
  report the time when `comps` reaches 1.
  [[p:uber-earliest-full-connection|Earliest Time All Users Are Connected]].
- **Best bottleneck.** "Over all routes from s to t, maximise the smallest edge on the
  route." Sort edges from strongest to weakest and union until s and t share a root;
  the edge that joined them is the answer, because every stronger edge was already
  in and still did not connect them.
  [[p:amazon-maximum-truck-weight|Maximum Truck Weight Between Two Cities]] is this.
- **Offline queries by threshold.** "For each query (u, v, limit), are u and v
  connected using only edges below limit?" Sort the queries by limit and the edges by
  weight, and sweep both together, adding edges up to each query's limit before
  answering it.

**Example.** Edges (0-1, 4), (1-2, 1), (0-2, 3), (2-3, 2). Kruskal takes 1-2 (1), 2-3
(2), 0-2 (3), and rejects 0-1 (4) because 0 and 1 already share a root. Total 6.

**Stretch.** [[p:tiktok-server-network-optimization|TikTok Server Network
Optimization]] is Kruskal on 10^5 points, after proving that only neighbours in
x-sorted order and in y-sorted order can be useful edges, which cuts the edge list
to 2(n - 1).

### G. A grid as a union-find

**What changes.** Items are cells, numbered r·cols + c. Union each land cell with its
land neighbours. Often you only need to look left and up, because the right and
down neighbours will look back at you.

**Example.** A 2 x 3 grid `110 / 011`: cells 0, 1, 4, 5 are land, and 1-4 are
vertical neighbours, so one island.

**Bank.** [[p:spacex-number-of-islands-ii|Number of Islands II]], where cells turn to
land one by one, which is the case where re-running a [[flood-fill]] after each
addition would be quadratic.

### H. "Next free slot" on a line

**What changes.** The meaning of the pointer. `parent[i]` is "the next index at or
after i that might be free". When slot i is taken, set `parent[i] = i + 1`. A `find`
then jumps over every run of taken slots at once, and halving keeps the jumps short.

**Why.** It is the same structure: taken slots are merged into the group of the next
free slot, and the root of any index is the first free slot at or after it.

**Example.** Requests 2, 2, 2, 1 with seats 1..: seat 2, then find(2) = 3, then
find(2) = 4, then seat 1. Assigned [2, 3, 4, 1].

**Bank.** [[p:inmobi-bus-station-seat-allotment|Bus Station Seat Allotment]] uses
this as its fast primitive, "the first free seat at or after x". Read it carefully:
people who find their seat taken go to the back of the queue, so they are not seated in
queue order. For requests [1, 1, 2] the answer is [1, 3, 2], not [1, 2, 3]: the third
person takes seat 2 before the second person comes back. The union-find answers the
lookup; the problem's work is getting the order of lookups right.

### I. Deletions known in advance: run time backwards

**What changes.** The order. Start from the final state, after every deletion, and
replay the deletions backwards as insertions. Union-Find handles insertions, and the
answers come out in reverse.

**Why.** A merge cannot be undone, but an un-deletion is a merge.

**Bank.** [[p:uber-counting-segments-after-house-removals|Counting Segments After
House Removals]]: houses on a line are removed one at a time; count the segments after
each removal.

```python run
def segments_after_removals(n, removals):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    alive = [True] * n
    for h in removals:
        alive[h] = False
    segs = 0                                   # the final state, built forwards
    for i in range(n):
        if alive[i]:
            segs += 1
            if i and alive[i - 1]:
                parent[find(i - 1)] = i
                segs -= 1
    ans = [0] * len(removals)
    for k in range(len(removals) - 1, -1, -1):
        ans[k] = segs                          # the state after removals[0..k]
        h = removals[k]                        # put it back
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

print("8 houses, remove 3, 5, 0, 6 ->", segments_after_removals(8, [3, 5, 0, 6]))
assert segments_after_removals(8, [3, 5, 0, 6]) == brute(8, [3, 5, 0, 6]) == [2, 3, 3, 3]
import random
rng = random.Random(11)
for _ in range(300):
    n = rng.randint(1, 10)
    order = list(range(n)); rng.shuffle(order)
    rem = order[:rng.randint(0, n)]
    assert segments_after_removals(n, rem) == brute(n, rem)
print("300 random schedules agree with a recount after every removal")
```

### J. Merging real member lists: small to large

**What changes.** Sometimes the answer needs the actual members of each group, not a
count. Keep a list at each root, and on a merge append the **smaller** list to the
larger.

**Why.** An item is moved only when its list joins a list at least as long, so its
list at least doubles each time it moves: at most log₂ n moves per item, O(n log n)
in total.

**Bank.** [[p:oracle-accounts-merge|Accounts Merge]] unions each account's emails
together, then groups emails by root at the end. (Collecting at the end, one pass over
all items, is simpler than small-to-large and just as fast when you only need the lists
once.)

### K. Undo: the rollback structure (rare)

**What changes.** Turn compression off, keep union by size (depth stays O(log n)), and
push every merge `(rb, ra, old size)` onto a stack, so the last merge can be undone by
popping. Compression must go, because it rewrites pointers that the undo would need.

**Why.** It is the tool for offline problems where edges appear and disappear
(divide and conquer over time). You will rarely meet it in an interview; know it
exists and why compression is incompatible with it.

## Recognising it in a statement

Ordered by how much to trust them.

1. **"Transitive", "directly or indirectly", "friends of friends", "through any
   chain".** The statement is telling you the relation is an equivalence and you
   must close it under chains. Close to a giveaway.
2. **Merges and questions interleaved.** "queryType is Friend or Total"; "after each
   addition, report". Offline you could traverse once; online you cannot.
3. **"How many groups / circles / provinces / islands / clusters"** with pairs given.
4. **"Minimum number of edges (or moves) to connect everything."** The answer is
   components - 1, possibly with a check on redundant edges.
5. **"The earliest time", "the first moment", "the largest weight such that still
   connected".** Sort by the key, union in order.
6. **An n x n symmetric 0/1 matrix.** An adjacency matrix; symmetric means two-way.
7. **"Connect all points at minimum cost".** Kruskal.

### The disguises

- **"Merge accounts that share an email."** The items are emails; each account says
  "all these emails are one group". Union the first email with each of the others.
- **"Equations a / b = 2, query c / d."** A weighted union-find, or a graph search
  per query. The ratio on each pointer is the trick.
- **"Can these dislikes be split into two groups?"** A parity union-find, or a
  2-colouring.
- **"Minimum score of a path, roads may be reused."** Not a path problem at all: the
  answer is a fact about city 1's component.
- **"The heaviest truck that can travel from s to t."** A bottleneck path: Kruskal from
  the strongest road down.
- **"Remove houses one at a time; count segments."** Deletions known in advance:
  reverse time.

### Anti-signals: looks like Union-Find, is not

- **Directed edges** ("a follows b", "prerequisite", "depends on"). Topological sort
  or SCC.
- **Distances.** "Fewest steps", "shortest", "minimum total weight of a route". BFS or
  Dijkstra; the group knows you are connected, not how far.
- **Online deletions.** No.
- **Contiguous pieces of an array.** "Groups" of adjacent elements that you choose
  are a partition DP or a greedy, not an equivalence that someone hands you.

## Traps

**Linking an element instead of a root.** `parent[b] = ra`. Symptom: groups split for
no visible reason, and only on inputs where b is not a root; chain-shaped samples pass.
Demonstrated in "The subtle line, both ways".

**Decrementing the counter on every pair.** Symptom: the count is too low, exactly by
the number of redundant pairs, and only on inputs that have a cycle. Demonstrated
below.

**Recursive `find` in Python.** Symptom: `RecursionError` at the recursion limit,
only on the large hidden tests (a chain of unions in index order). Write the loop.

**Reading `size[x]` instead of `size[find(x)]`.** Symptom: sizes frozen at the moment
x stopped being a root, too small.

**Keeping a root in a variable.** `r = find(x)`, then more unions, then using `r`.
Symptom: answers that depend on merge order, because r may no longer be a root. Only
`find` names a group.

**The off-by-one universe.** Items 1..n allocated as n slots. Symptom: an index error,
or, if you allocate n + 1 and forget slot 0, exactly one extra group in every count.

**Forgetting the lonely items.** Build the structure from n, not from the items that
appear in edges. "Every member belongs to exactly one group, including an isolated
member." Symptom: counts right on dense inputs and too low on sparse ones.

**Counting edges only on a merge.** In variation D, a redundant edge still belongs to
the group. Symptom: a triangle is reported as a tree.

**Treating a directed relation as two-way.** Symptom: everything looks connected.

```python run
def find(p, x):
    while p[x] != x:
        p[x] = p[p[x]]
        x = p[x]
    return x

def count(n, pairs, guarded):
    p, comps = list(range(n)), n
    for a, b in pairs:
        ra, rb = find(p, a), find(p, b)
        if guarded and ra == rb:
            continue                      # correct: no merge, no decrement
        p[rb] = ra
        comps -= 1
    return comps, len({find(p, x) for x in range(n)})

# a triangle 0-1-2 plus two lonely items: truth is 3 groups
pairs = [(0, 1), (1, 2), (0, 2)]
print("guarded   (counter, distinct roots):", count(5, pairs, True))
print("unguarded (counter, distinct roots):", count(5, pairs, False))
assert count(5, pairs, True) == (3, 3)
assert count(5, pairs, False) == (2, 3)   # the redundant edge was counted as a merge

# without a cycle the bug is invisible
tree = [(0, 1), (1, 2), (3, 4)]
assert count(5, tree, True) == count(5, tree, False) == (2, 2)
print("on a forest both agree:", count(5, tree, False))

# the recursive find, on the chain that unions in index order produce
import sys
def find_rec(p, x):
    return x if p[x] == x else find_rec(p, p[x])
chain = list(range(1, 50001)) + [50000]   # 0 -> 1 -> ... -> 50000
try:
    find_rec(chain, 0)
    crashed = False
except RecursionError:
    crashed = True
print("recursive find on a 50000-long chain crashes:", crashed,
      "(limit %d)" % sys.getrecursionlimit())
assert crashed and find(chain[:], 0) == 50000
```

The first assert is the important one: the counter and the forest disagree (2
versus 3), which is a cheap self-test you can add while debugging:
`comps == len({find(x) for x in range(n)})`.

## What to memorise

The template:

```python
parent, size, comps = list(range(n)), [1] * n, n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]      # halving
        x = parent[x]
    return x

def union(a, b):
    global comps
    ra, rb = find(a), find(b)
    if ra == rb:
        return False                       # redundant
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra                        # root under root
    size[ra] += size[rb]
    comps -= 1
    return True
```

The sentence that turns a problem into it: **"I am told, one pair at a time, that two
things belong together, the relation is two-way and only grows, and I am asked about
the groups."**

The question that built it: **what is the least each item must store so that two
items in the same group can find the same name?** One pointer toward the name.

The habit: **a merge is on two groups, so find both roots first, write root under
root, and update every counter from the bool `union` returns.**

The numbers: union by size alone caps depth at log₂ n (17 for 200,000); with
halving, treat every operation as constant; c groups need c - 1 edges to connect; a
complete group of k items has k(k-1)/2 edges; a tree on k items has k - 1.

## Check yourself

:::check
Hand trace. Eight items 0..7, union by size with ties keeping the first root, path
halving. Run union(0,1), union(2,3), union(4,5), union(6,7), union(1,3), union(5,7),
union(3,7), union(0,6). Write `parent`, the sizes at the roots and `comps` after every
call. Which call returns False? What is the deepest item at the end?
--
| call | roots | action | `parent` after | comps |
|---|---|---|---|---|
| union(0,1) | 0, 1 | 1 under 0, size[0]=2 | `[0,0,2,3,4,5,6,7]` | 7 |
| union(2,3) | 2, 3 | 3 under 2, size[2]=2 | `[0,0,2,2,4,5,6,7]` | 6 |
| union(4,5) | 4, 5 | 5 under 4, size[4]=2 | `[0,0,2,2,4,4,6,7]` | 5 |
| union(6,7) | 6, 7 | 7 under 6, size[6]=2 | `[0,0,2,2,4,4,6,6]` | 4 |
| union(1,3) | 0, 2 | tie: 2 under 0, size[0]=4 | `[0,0,0,2,4,4,6,6]` | 3 |
| union(5,7) | 4, 6 | tie: 6 under 4, size[4]=4 | `[0,0,0,2,4,4,4,6]` | 2 |
| union(3,7) | 0, 4 | tie: 4 under 0, size[0]=8 | see below | 1 |
| union(0,6) | 0, 0 | same root: False | | 1 |

In union(3,7), find(3) walks 3 → 2 → 0 and halving writes parent[3] = parent[2] = 0.
find(7) walks 7 → 6 → 4 and writes parent[7] = parent[6] = 4. Then parent[4] = 0.
Array: `[0,0,0,0,0,4,4,4]`. In union(0,6), find(6) walks 6 → 4 → 0 and writes
parent[6] = 0: `[0,0,0,0,0,4,0,4]`. The last call returns False.

Deepest items: 5 and 7, two steps (5 → 4 → 0, 7 → 4 → 0). Eight items, depth 2, well
under log₂ 8 = 3.
:::

:::check
Hand trace, the wrong way. Same eight items and calls as the previous exercise, but the
union writes `parent[b] = ra` (element under root, no size rule, ties as before). After
which call does the structure first disagree with the truth, and how?
--
The first four calls write parent[1]=0, parent[3]=2, parent[5]=4, parent[7]=6: b is a
root each time, so they agree with the correct version.

union(1,3): ra = find(1) = 0, and the write is parent[3] = 0, not parent[2] = 0. Item 2
still points at itself. Array `[0,0,2,0,4,4,6,6]`. The truth is {0,1,2,3} together, but 2
is now a root on its own: **the first disagreement, at the fifth call.** "Are 0 and 2
together?" now answers no.

The same thing happens again at union(5,7): parent[7] = 4, and 6 is cut off. The final
structure has more roots than the true single group.
:::

:::check
Why is path compression allowed to change `parent` during a `find`, which is supposed
to be a question, without corrupting any answer?
--
Because `parent` is a naming scheme, not a record of the input. The promise is only
that items of one group reach the same root and items of different groups do not.
Compression re-points an item at a higher item of the **same tree**, so the item still
reaches the same root, and no item's root changes. The tree's shape changes, but the
shape was never part of the promise.

Said the other way: if the trees stored the edges of the graph, compression would
destroy information. They do not. That is also why the rollback structure must turn
compression off: undoing a merge needs the old shape, and compression throws it away.
:::

:::check
Someone says: "Union by size is what makes union-find correct. Without it, groups
merge wrongly on large inputs." Where are they wrong, and what is the true version of
their worry?
--
They have mixed up correctness and speed. The proof never used union by size; it only
needed the write to link two different roots. Hanging the larger tree under the
smaller gives exactly the same groups, the same counts and the same answers.

The true worry is time. Without union by size (and without compression), unions in
index order build a chain, a find costs n - 1 steps, and 2·10^5 operations cost about
2·10^10 steps: a timeout, not a wrong answer. A wrong answer and a timeout send you to
different lines of code, which is why the distinction matters.
:::

:::check
Someone counts groups with `for a, b in edges: union(a, b); comps -= 1`, and it passes
the samples. When is it wrong, and by how much?
--
It is wrong whenever some edge joins two items already in one group, that is, whenever
the graph has a cycle (or a repeated edge). Each such edge lowers the count without
merging anything. The count is too low by exactly the number of redundant edges, which
is E - (n - true count). On a forest there are none, so samples shaped like trees pass.
The fix is to decrement only when `union` returns True.
:::

:::check
Reduce this disguised problem. "n servers, a list of cables (a, b, installed_at). Find
the earliest time at which every server can reach every other, or -1." Name the
structure, the order, the stopping rule, and why no binary search is needed.
--
Union-Find over the servers, with the cables sorted by installed_at. Union them in that
order; after each union that returns True, check whether comps == 1, and if so, report
this cable's time. If the list runs out with comps > 1, return -1.

No binary search is needed because the groups only grow: if everything is connected
after the first k cables, it stays connected after more. So the first prefix with
comps == 1 is the answer, and one pass meets every prefix in order. The sort is the
cost, O(E log E); the unions are O(E·α).
:::

:::check
A colleague wants to delete item v from its group with `parent[v] = v`. Give a
three-item example where this goes wrong, and say why no local fix exists.
--
Items 0, 1, 2 and edges 0-1 and 1-2. With union by size: union(0,1) writes
parent[1] = 0; union(1,2) finds roots 0 and 2 and writes parent[2] = 0. Now set
parent[1] = 1. The structure says {0, 2} and {1}. The truth, after removing item 1 and
its two edges, is {0}, {1}, {2}: 0 and 2 were joined only through 1.

With a different merge rule (first root under second) the same edges build the chain
0 → 1 → 2, and parent[1] = 1 now gives {0, 1} and {2}, a different wrong answer. So the
result depends on the tree's shape, which depends on merge order and compression, not on
the input.

No local fix exists because the structure never stored the edges. To know how the
remaining items should be grouped, you need to know which pairs joined them, and that
information is gone. Deletions need time reversal (if known in advance) or a rollback
structure.
:::

:::check
Evaluate by hand with weighted union-find: a / b = 2, b / c = 4, d / c = 0.5. What are
a / d and d / a, and which pointer weights do you use?
--
Process a / b = 2: parent[a] = b, w[a] = 2. Then b / c = 4: parent[b] = c, w[b] = 4.
Then d / c = 0.5: parent[d] = c, w[d] = 0.5.

find(a) walks a → b → c and multiplies: a / c = 2 · 4 = 8. find(d) is c directly:
d / c = 0.5. Same root c, so a / d = (a / c) / (d / c) = 8 / 0.5 = 16, and
d / a = 0.5 / 8 = 0.0625. Check without the structure: a = 2b, b = 4c, so a = 8c; d =
0.5c; a / d = 16.
:::
