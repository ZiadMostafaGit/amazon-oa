# Morris Traversal (O(1) space)

> Every tree is carrying the pointers you need to find your way back up — they
> are just pointing at nothing. Morris traversal borrows them for a moment,
> walks home along them, and puts them back.

## When you reach for it

Start with the honest disclaimer: **no problem in this collection uses Morris
traversal.** It ranks #143 of 150 here, and the count is zero. It is in this
book because interviews elsewhere ask for it, and because it is the cleanest
example in all of tree algorithms of a trick that buys space by temporarily
lying about the data structure. Read it for the idea, not for the drill.

Where it does appear, it appears in one of three shapes.

**The explicit follow-up.** You write the stack-based iterative in-order walk,
the interviewer nods, and asks: "that is O(h) extra space — can you do it in
O(1)?" There is exactly one answer, and this is it.

**The constraint written into the statement.** "Traverse the tree using
constant extra space." "Find the k-th smallest element in a BST without
recursion and without an auxiliary data structure." "Two nodes of a BST were
swapped by mistake; recover the tree in O(1) space." Those are Morris
questions wearing a costume.

**The environment that cannot afford a stack.** An unbalanced BST built from
sorted input is a path: a million nodes, height a million. The recursive walk
dies on the call stack; the explicit-stack walk allocates a million frames'
worth of list. Morris uses two pointers whatever the shape. This is real in
garbage collectors, which must walk the object graph precisely when there is no
memory left to allocate a stack in.

And the shape that makes it the **wrong** tool, which matters more:

- **The tree is read-only, shared, or concurrently visited.** Morris *writes to
  the tree*. Mid-traversal the structure is not a tree at all — it contains
  cycles. Any other thread reading it during that window sees a corrupt
  structure, and any code that walks it will loop forever.
- **You want to stop early.** The whole correctness story depends on running to
  completion so every borrowed pointer is returned. An early `return` leaves the
  tree damaged. There is a fix, and it is not free; see Traps.
- **The height is genuinely logarithmic and `n` is modest.** O(log n) stack on a
  balanced tree of a million nodes is twenty pointers. Morris trades that for a
  bigger constant factor on every node. It is a different trade, not a strictly
  better one.
- **The visit body can raise.** An exception thrown out of the middle of the
  loop is an early exit with extra steps.

## The idea

Ask why the recursive in-order walk needs a stack at all. It is not to remember
the nodes — the tree already stores those. It is to remember *one thing*: after
I finish the left subtree of `x`, where do I go back to? The stack is a list of
"return here next" notes, and its depth is the height of the tree.

Now ask where such a note could live. In-order, the node immediately before `x`
is the **rightmost node of `x`'s left subtree** — call it `pred(x)` — which is
exactly where the left subtree's walk will end. And because it is the rightmost
node of a subtree, its right pointer is `None`. It is carrying a spare field at
precisely the place where we will need the note.

So: before descending into the left subtree of `x`, set `pred(x).right = x`.
That is the **thread** — a temporary back edge. Walk the left subtree. When the
walk runs off the right end of it, it does not fall into `None`; it steps onto
the thread and arrives back at `x`. Cut the thread, restore the `None`, visit
`x`, and move right.

<svg viewBox="0 0 520 250" role="img" aria-label="a five-node tree with a dashed thread from the rightmost node of the left subtree back up to the root">
  <g>
    <circle class="fill" cx="250" cy="40" r="20"/>
    <circle cx="150" cy="118" r="20"/>
    <circle cx="380" cy="118" r="20"/>
    <circle cx="80" cy="196" r="20"/>
    <circle class="fill" cx="215" cy="196" r="20"/>
    <text x="245" y="45">4</text>
    <text x="145" y="123">2</text>
    <text x="375" y="123">5</text>
    <text x="75" y="201">1</text>
    <text x="210" y="201">3</text>
    <line x1="235" y1="55" x2="165" y2="103"/>
    <line x1="266" y1="55" x2="364" y2="103"/>
    <line x1="137" y1="134" x2="93" y2="181"/>
    <line x1="164" y1="134" x2="201" y2="181"/>
    <path d="M232 186 C 300 170, 300 80, 268 52" stroke-dasharray="6 5"/>
    <text x="305" y="176">thread: pred(4).right = 4</text>
    <text x="20" y="232">3 is the rightmost node of 4's left subtree, so its right pointer was free</text>
  </g>
</svg>

One sentence: **the last node of the left subtree has a spare right pointer, and
it is exactly the node whose in-order successor is the node we came from — so
point it there, use it once, and take it back.**

The loop that falls out of this is eight lines and has three branches:

```python
while cur is not None:
    if cur.left is None:
        visit(cur); cur = cur.right        # nothing to the left; go on
    else:
        pred = rightmost(cur.left, stop_at=cur)
        if pred.right is None:
            pred.right = cur; cur = cur.left     # first time here: thread and descend
        else:
            pred.right = None; visit(cur); cur = cur.right   # came back: unthread and go on
```

The `stop_at=cur` is not decoration. Once the thread exists, walking right from
`cur.left` will hit `cur` itself rather than `None`, so the search for the
rightmost node must stop on *either* condition. That double condition is the
whole reason the algorithm can tell "I am arriving for the first time" from "I
am arriving back".

## Worked by hand

Take this tree, which is a BST on 1..5:

```
        4
      /   \
     2     5
    / \
   1   3
```

In-order it is `1 2 3 4 5`. Run the loop with a pen. In the table, "pred found"
is the node the inner right-spine walk lands on, and "thread state" is what that
node's right pointer held when we got there.

| step | cur | has left? | pred found | thread state | action | output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | yes | 3 | `None` | set `3.right = 4`; `cur = 2` | — |
| 2 | 2 | yes | 1 | `None` | set `1.right = 2`; `cur = 1` | — |
| 3 | 1 | no | — | — | visit 1; `cur = 1.right = 2` (a thread) | 1 |
| 4 | 2 | yes | 1 | `is cur` | cut `1.right`; visit 2; `cur = 3` | 1 2 |
| 5 | 3 | no | — | — | visit 3; `cur = 3.right = 4` (a thread) | 1 2 3 |
| 6 | 4 | yes | 3 | `is cur` | cut `3.right`; visit 4; `cur = 5` | 1 2 3 4 |
| 7 | 5 | no | — | — | visit 5; `cur = 5.right = None` | 1 2 3 4 5 |
| 8 | `None` | — | — | — | loop ends | 1 2 3 4 5 |

Four things in that trace are worth more than the code.

**Nodes with a left child are entered twice; nodes without are entered once.**
Node 4 appears at steps 1 and 6, node 2 at steps 2 and 4: once going down, once
coming back. That is the recursive walk's two-visit pattern, except the second
visit arrives through the data structure rather than through a stack frame.

**The visit happens on the second entry, not the first.** That single choice is
what makes it in-order; move it into the thread-creating branch and you get
preorder. There is no third entry, which is why postorder needs its own trick.

**The thread is created and destroyed by the same node.** Step 1 creates
`3.right = 4`; step 6 destroys it. Step 2 creates `1.right = 2`; step 4 destroys
it. They are perfectly paired, and they nest: the inner pair opens and closes
entirely inside the outer pair. If you drew them as brackets you would get
`[ ( ) ]`. That nesting is the shadow of the stack we deleted.

**At step 5 the structure is not a tree.** Node 3's right pointer points at its
ancestor 4: a cycle `4 → 2 → 3 → 4`. Anything else reading the tree at that
moment — a debugger's pretty-printer, another thread, a recursive `__repr__` —
will spin. The algorithm is correct because it guarantees to clean up, not
because it never makes a mess.

## Why it is correct

The informal story ("we leave a breadcrumb and follow it back") explains the
mechanism, not the result. Two things need proving: the output is the in-order
sequence, and the tree that comes out is pointer-for-pointer the tree that went
in. They are proved together, because each depends on the other.

First a definition. For a node `r`, write `sub(r)` for its subtree, `inorder(r)`
for the in-order list of `sub(r)`, and `m(r)` for the **rightmost node** of
`sub(r)`: start at `r` and follow `right` pointers while they are non-null.

:::proof Morris in-order visits `inorder(root)` and restores the tree
**Lemma A.** `m(r)` is the last node of `inorder(r)`, and in the original tree
`m(r).right is None`.

*Proof.* Induction on `|sub(r)|`. If `r.right is None` then `inorder(r) =
inorder(r.left) ++ [r]`, whose last element is `r = m(r)`, and `r.right` is
null. Otherwise `inorder(r) = inorder(r.left) ++ [r] ++ inorder(r.right)`, whose
last element is the last of `inorder(r.right)`, which by induction is
`m(r.right) = m(r)`, and that node's right pointer is null by induction. ∎

**Lemma B.** If `x` has a left child, the node immediately before `x` in
`inorder(x)` is `m(x.left)`.

*Proof.* `inorder(x) = inorder(x.left) ++ [x] ++ inorder(x.right)`, so the node
before `x` is the last of `inorder(x.left)`, which is `m(x.left)` by Lemma A. ∎

**The phase claim.** Fix a node `r` and a pointer value `e` (a node, or `None`).
Say the structure is *`r`-ready with exit `e`* when `sub(r)` is exactly as in
the original tree, except that `m(r).right` holds `e` instead of `None`.

> Claim: started with `cur = r` in a structure that is `r`-ready with exit `e`,
> the loop performs finitely many iterations, appends exactly `inorder(r)` to
> the output, leaves the structure `r`-ready with exit `e` again, and the first
> moment `cur` becomes `e` is the end of that phase. Nothing outside `sub(r)` is
> read or written during the phase.

**Proof by strong induction on `n = |sub(r)|`.**

*Base / left-empty case: `r.left is None`.* The loop takes the first branch:
visit `r`, then `cur = r.right`. If `r` has no right child then `m(r) = r`, so
`r.right` holds `e` and `cur` becomes `e` immediately; the output was `[r] =
inorder(r)`, and nothing was written. Otherwise let `R = r.right`. Since the
only altered pointer in `sub(r)` is at `m(r) = m(R)`, the structure is `R`-ready
with exit `e`, and `|sub(R)| < n`, so the induction hypothesis applies: the
remaining iterations emit `inorder(R)`, restore, and end at `e`. Total output
`[r] ++ inorder(R) = inorder(r)`. ✓

*Inductive case: `r` has a left child `L`.* Let `P = m(L)`, which by Lemma B is
`r`'s in-order predecessor. Note `P ∈ sub(L)`, and `sub(L)` is untouched: the
only altered pointer in `sub(r)` is at `m(r)`, and `m(r)` is `m(r.right)` or `r`
itself, never inside `sub(L)`.

1. *First entry.* The inner walk starts at `L` and follows right pointers. In an
   untouched `sub(L)` those are original pointers, so it stops at `P` with
   `P.right is None` (Lemma A). Since `None` is not `cur`, we take the
   thread-creating branch: `P.right = r`, `cur = L`.
2. *The left phase.* Now `sub(L)` is exactly original except `m(L).right = r` —
   that is, `L`-ready with exit `r`. As `|sub(L)| < n`, the hypothesis gives:
   finitely many iterations, output `inorder(L)`, `sub(L)` left `L`-ready with
   exit `r`, and the phase ends the first time `cur` becomes `r`.
3. *Second entry.* `cur = r` again. `r.left` is still `L`, so the inner walk runs
   again. `sub(L)` is in the same state as at the end of step 1, so the walk
   again reaches `P`, this time stopping because `P.right is cur`. We take the
   second branch: `P.right = None` — `sub(L)` is now fully original — visit `r`,
   and `cur = r.right`.
4. *The right phase.* If `r` has no right child, `m(r) = r`, so `cur` is now `e`
   and the phase ends with output `inorder(L) ++ [r] = inorder(r)` and `sub(r)`
   restored apart from `m(r).right = e`. ✓ If `r` has a right child `R`, then
   `sub(R)` is original except `m(R).right = m(r).right = e`, i.e. `R`-ready
   with exit `e`; by the hypothesis the rest emits `inorder(R)` and ends at `e`.
   Output: `inorder(L) ++ [r] ++ inorder(R) = inorder(r)`. ✓

Every step above reads or writes only `cur`, `cur.left`, and nodes on a right
spine inside `sub(cur.left)` — all within `sub(r)`. Finiteness: each case is a
constant number of iterations plus at most two sub-phases, each finite by the
hypothesis, so the phase is finite.

**The theorem.** Apply the claim with `r = root` and `e = None`. The whole tree
is trivially `root`-ready with exit `None` (Lemma A says `m(root).right` is
already null). So the loop terminates, outputs exactly `inorder(root)`, and
leaves every pointer as it found it. ∎
:::

Now say plainly what that proof leaned on, because that list is where the bugs
come from.

- **It is a tree.** One parent per node, no cycles, finite. If the input already
  contains a back edge, the right-spine walk need not terminate and Lemma A is
  false.
- **The rightmost node's right pointer is genuinely null.** That is Lemma A, and
  it is only true of an unmodified tree. Run two Morris traversals at once on
  the same tree and the second one finds a thread where it expected null.
- **The thread test is by identity, not by value.** "Stopping because
  `P.right is cur`" distinguishes a borrowed pointer from a real edge purely by
  *which object* it points to. Where `==` on nodes means value equality, using
  it here makes the loop mistake a real subtree edge for its own thread.
- **The traversal runs to completion.** Steps 1 and 3 of the inductive case are
  a matched pair. Leave the loop between them and `P.right = r` survives.
- **Nobody else touches the tree.** Not another thread, not the visit callback,
  not a `print` that walks the structure.

:::note Why there is no third visit
A node with a left child is entered exactly twice: on the way down, and on the
way back from the left subtree. In-order needs the second, preorder the first.
Postorder needs a visit *after the right subtree* — a third moment this loop
does not have, because when we leave `r` to the right we never return to `r`.
:::

## What it costs

Derive it, do not assert it. Two things get counted: outer iterations, and the
steps inside the predecessor search.

**Outer iterations.** Each iteration takes exactly one of three branches:

- (A) `cur.left is None`: visit, move right.
- (B) thread created, move left.
- (C) thread destroyed, visit, move right.

Branches A and C are the only ones that visit, and the theorem says each of the
`n` nodes is visited exactly once, so A and C together run exactly `n` times.
Branch B runs once per node that has a left child — the proof's inductive case
executes step 1 exactly once per such node — so at most `n - 1` times. Total
iterations: at most `2n - 1`.

**Inner steps.** Branch B and branch C each walk the right spine of `cur.left`,
from `cur.left` down to `pred(cur)`. Let `d(x)` be the number of right edges on
that spine for a node `x` with a left child. The search runs twice for each such
`x`, so the total inner work is `2 · Σ d(x)`.

The counting argument is: **the spines are disjoint.** Suppose a right edge
`u → u.right` lies on the spine of `x.left` and also on the spine of `y.left`.
"`u` is on the spine of `x.left`" means `x.left` is reachable from... more
usefully, it means `x.left` is the topmost node of the maximal chain of right
edges containing `u`. That chain is determined by `u` alone: walk up from `u`
through right-edges-from-parent as far as you can, and the node you stop at is
`x.left`. So `x.left` is unique, and since a node has a single parent, `x` is
unique. Each right edge therefore belongs to at most one spine, giving
`Σ d(x) ≤ (number of right edges) ≤ n - 1`, hence at most `2(n - 1)` inner
steps in the whole traversal.

**Total.** `(2n - 1) + 2(n - 1) = 4n - 3` pointer moves, i.e. **Θ(n) time**.
Every node must be reported, so Ω(n) is forced and Morris meets it: it does not
asymptotically pay for the space it saves.

**Space.** Two local pointers, `cur` and `pred`, plus whatever the visit does.
That is **O(1) extra**, and it is O(1) for every shape of tree, where the stack
walk is O(h): O(log n) balanced, O(n) for a path. This is the entire point.

Three costs people forget.

**It is not free constant-factor-wise.** Morris touches each node up to four
times against roughly two for the stack walk, and its inner loop is a pointer
chase with a branch on each step. Expect it to be slower per node; you are
buying space.

**It costs `2L` writes**, where `L` is the number of nodes with a left child:
one to plant each thread, one to cut it. A traversal that used to be read-only
now dirties cache lines and, in copy-on-write memory, can fault pages in.

**"O(1) space" means O(1) *extra*.** If you collect the values into a list, that
list is O(n) and no traversal can avoid it. The claim is about the traversal's
own bookkeeping.

## The implementation

```python run
class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def morris_inorder(root):
    """In-order values of the tree, using O(1) extra space."""
    out, cur = [], root
    while cur is not None:
        if cur.left is None:
            out.append(cur.val)           # nothing to the left: this node is next
            cur = cur.right               # a real edge, or a thread we planted
        else:
            pred = cur.left               # walk to the rightmost node of the left subtree
            while pred.right is not None and pred.right is not cur:
                pred = pred.right
            if pred.right is None:
                pred.right = cur          # borrow the spare pointer, then descend
                cur = cur.left
            else:
                pred.right = None         # give it back, exactly as we found it
                out.append(cur.val)
                cur = cur.right
    return out


def recursive_inorder(node, out=None):
    out = [] if out is None else out
    if node is not None:
        recursive_inorder(node.left, out)
        out.append(node.val)
        recursive_inorder(node.right, out)
    return out


def shape(node):
    """A string that changes if any pointer in the tree changes."""
    return "." if node is None else "(%s %s %s)" % (node.val, shape(node.left), shape(node.right))


def bst_insert(root, v):
    if root is None:
        return Node(v)
    if v < root.val:
        root.left = bst_insert(root.left, v)
    else:
        root.right = bst_insert(root.right, v)
    return root


t = None
for v in (4, 2, 5, 1, 3):
    t = bst_insert(t, v)
before = shape(t)
print("tree      ", before)
print("morris    ", morris_inorder(t))
print("recursive ", recursive_inorder(t))
print("restored  ", shape(t) == before)
assert morris_inorder(t) == [1, 2, 3, 4, 5] and shape(t) == before

import random
rng = random.Random(7)
for _ in range(300):
    root, vals = None, [rng.randrange(60) for _ in range(rng.randrange(0, 25))]
    for v in vals:
        root = bst_insert(root, v)
    snap = shape(root)
    assert morris_inorder(root) == recursive_inorder(root) == sorted(vals)
    assert shape(root) == snap, "tree not restored"
print("300 random trees: same order as recursion, and every tree restored")
```

Three lines are doing the real work.

`while pred.right is not None and pred.right is not cur:` — the two conditions
are the two ways the spine can end, and the algorithm's entire state machine
lives in which one fired. `is not None` means "this is the first visit, the
pointer is still free"; `is not cur` means "I have been here, that is my own
thread". Drop the second condition and the walk follows the thread back up to
`cur`, then down the left spine again, forever.

`pred.right = cur` and `pred.right = None` — write them as a pair, in the same
sitting. Every bug in this algorithm that is not a missing loop condition is a
thread that was planted and not cut.

`out.append(cur.val)` sits in the *unthreading* branch. That placement is the
in-order/preorder switch, and it is worth saying out loud when you write it:
"visit on the way back, because the left subtree owes me its output first."

The `shape` check is not decoration either. Half of getting Morris right is
proving restoration, and the cheap way to do that is to fingerprint the
structure before and after and compare.

## Variants you will meet

**Morris preorder.** Move the visit from the unthreading branch to the
thread-creating branch, and to the `cur.left is None` branch. Nothing else
changes. See [[tree-traversal]] for the recursive family this mirrors.

**Morris postorder.** Needs a third visiting moment the loop does not have; the
usual construction reverses the right spine of the left subtree in place,
outputs it backwards, and reverses it again. O(1) space, but bulky.

**Recover a BST with two swapped nodes.** Morris in-order while remembering the
previous value; the two places where the sequence goes down are the swapped
nodes. Constant space end to end, which is the point of the question. See
[[bst]].

**K-th smallest in a BST, constant space.** Morris in-order with a counter —
with the early-exit caveat in Traps, which is really the interesting half of the
question.

**Flatten a tree into a right-leaning chain.** Same predecessor step, but
instead of restoring the thread you keep it and clear `cur.left`. The result is
a degenerate tree that is really a [[linked-list]], produced in O(1) space.

**Threaded binary trees (Perlis–Thornton).** Make the threads *permanent*:
every null right pointer stores the in-order successor, with one bit per node
saying whether it is a child or a thread. In-order iteration is then O(1) per
step with no traversal state at all. Morris is that idea rebuilt on the fly and
thrown away.

**The stack version it replaces.** Push-left-spine, pop, visit, go right —
O(h) space, no writes, early exit allowed. See [[tree-traversal]] and [[stack]].
The choice between the two is the actual interview content.

```python run
import sys


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def morris_preorder(root):
    out, cur = [], root
    while cur is not None:
        if cur.left is None:
            out.append(cur.val)
            cur = cur.right
        else:
            pred = cur.left
            while pred.right is not None and pred.right is not cur:
                pred = pred.right
            if pred.right is None:
                out.append(cur.val)       # THE ONLY CHANGE: visit on the way down
                pred.right = cur
                cur = cur.left
            else:
                pred.right = None
                cur = cur.right
    return out


def morris_inorder(root):
    out, cur = [], root
    while cur is not None:
        if cur.left is None:
            out.append(cur.val)
            cur = cur.right
        else:
            pred = cur.left
            while pred.right is not None and pred.right is not cur:
                pred = pred.right
            if pred.right is None:
                pred.right = cur
                cur = cur.left
            else:
                pred.right = None
                out.append(cur.val)
                cur = cur.right
    return out


def rec_preorder(n, out):
    if n is not None:
        out.append(n.val)
        rec_preorder(n.left, out)
        rec_preorder(n.right, out)
    return out


t = Node(4, Node(2, Node(1), Node(3)), Node(5))
print("morris preorder   ", morris_preorder(t))
print("recursive preorder", rec_preorder(t, []))
assert morris_preorder(t) == rec_preorder(t, []) == [4, 2, 1, 3, 5]

# a 2000-deep left chain: height == n, so O(h) space is O(n)
sys.setrecursionlimit(1000)               # CPython's own default
DEPTH = 2000
chain = Node(1)
for v in range(2, DEPTH + 1):
    chain = Node(v, chain)
try:
    rec_preorder(chain, [])
    print("recursion survived (limit was raised?)")
except RecursionError:
    print("recursive walk of a %d-deep chain: RecursionError" % DEPTH)
vals = morris_inorder(chain)
print("morris walked the same chain:", vals[:4], "...", vals[-2:], "n =", len(vals))
assert vals == list(range(1, DEPTH + 1))
```

## Recognising it in a statement

In rough order of how much they should move you:

- **"O(1) extra space" or "constant additional space" attached to a tree
  traversal.** This is the giveaway. There is no other technique that does it.
- **"without recursion and without using a stack / queue / any auxiliary data
  structure"** — the interviewer has spelled out both alternatives to rule them
  out.
- **"You may modify the tree, but it must be the same when you are done."** That
  sentence exists only to permit threading.
- **A follow-up after you have already given an O(h) solution.** The question
  "can you do better on space?" on a tree problem has exactly one intended
  answer.
- **A degenerate-tree constraint**: a large `n` with no balance guarantee. That
  is the case where O(h) is secretly O(n).

The anti-signals, which matter because "O(1) space" is a phrase with many
owners:

- **"O(1) space" on an array or a string** is [[two-pointers]], not this.
- **"O(1) space" on a linked list** is [[fast-slow-pointers]]. Same philosophy
  — use the structure's own pointers instead of memory — different technique.
- **A read-only or shared tree, or immutable nodes.** The answer is parent
  pointers if the nodes have them, or an honest O(h) stack with the trade-off
  stated.
- **Only the multiset of values is needed, not the order.** Any walk does.
- **Balanced tree, small `n`, clarity valued.** "Morris does this in O(1) space
  but at a constant-factor and mutability cost; for `h = 20` I would ship the
  stack version" is a better answer than the code.

## Traps

**Leaving the loop early.** The commonest way to break it, and not a style
issue: the tree is left containing a cycle. The demonstration below returns the
right answer and hands back a corrupted tree.

**Dropping the `pred.right is not cur` condition.** The inner walk then follows
its own thread up to `cur` and back down forever. Symptom: a hang, and only on
trees where some node's left child has a right child.

**Using `==` instead of `is`.** With a `Node` that defines value equality, or
an overridden `equals` in Java, `pred.right == cur` can be true for a node that
is not `cur`. The loop stops early, decides a real edge is a thread, nulls it,
and *deletes a subtree*. Symptom: missing nodes, and a smaller tree afterwards.

**Visiting in the wrong branch.** Visit on thread creation and you have silently
written preorder. Symptom: the output is a valid traversal, just not the one
asked for — which is why this survives a careless test.

**Mutating the tree inside the visit.** The proof assumes `sub(cur)` is
unchanged between the first and second entry to a node; a visit that rotates or
reparents anything invalidates the pending threads.

**Claiming O(1) space while building an O(n) result list.** Say "O(1) auxiliary
space beyond the output" and you have said something true.

**Letting anything else read the tree mid-traversal.** Up to `h` back edges are
live at once, and an exception thrown from inside the loop makes them
permanent.

```python run
class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build():
    return Node(4, Node(2, Node(1), Node(3)), Node(5))


def shape(n):
    return "." if n is None else "(%s %s %s)" % (n.val, shape(n.left), shape(n.right))


def has_cycle(root):
    """Iterative, id-based, so it terminates even on a corrupted tree."""
    seen, stack = set(), [root]
    while stack:
        n = stack.pop()
        if n is None:
            continue
        if id(n) in seen:
            return True
        seen.add(id(n))
        stack.append(n.left)
        stack.append(n.right)
    return False


def kth_smallest(root, k, bail_out):
    cur, seen, ans = root, 0, None
    while cur is not None:
        if cur.left is None:
            seen += 1
            if seen == k:
                ans = cur.val
                if bail_out:
                    return ans                 # <-- threads still planted
            cur = cur.right
        else:
            pred = cur.left
            while pred.right is not None and pred.right is not cur:
                pred = pred.right
            if pred.right is None:
                pred.right = cur
                cur = cur.left
            else:
                pred.right = None
                seen += 1
                if seen == k:
                    ans = cur.val
                    if bail_out:
                        return ans             # <-- same problem
                cur = cur.right
    return ans


t = build()
intact = shape(t)
print("wrong: kth_smallest(2) returned", kth_smallest(t, 2, bail_out=True), "- the right answer")
node3 = t.left.right
print("       but node 3's right pointer now points at node", node3.right.val)
print("       tree contains a cycle:", has_cycle(t))
assert node3.right is t and has_cycle(t)

t2 = build()
print("right: kth_smallest(2) returned", kth_smallest(t2, 2, bail_out=False))
print("       shape afterwards:", shape(t2), "| unchanged:", shape(t2) == intact)
assert shape(t2) == intact and not has_cycle(t2)
print("the cure: record the answer, let the loop finish, then return")
```

:::warn Early exit is not free
Letting the loop run to the end restores the tree, but it costs Θ(n) even when
`k` is 1 — you lose the "stop after k" saving that made the question
interesting. The alternative is to cut the outstanding threads explicitly: from
the node you stopped at, keep running the *unthreading* half of the loop with
the visiting turned off until `cur` is null. That is what the `bail_out=False`
version does implicitly. There is no O(k) constant-space version that also
leaves the tree intact, and saying so is a better answer than pretending
otherwise.
:::

## What to memorise

Not the code — the reason the code exists.

**The sentence** that generates everything: *"The rightmost node of my left
subtree is my in-order predecessor, and its right pointer is null, so it can
hold a note that says 'come back to me'."*

**The template**, which is worth being able to type without thinking:

```python
cur = root
while cur:
    if not cur.left:
        visit(cur); cur = cur.right
    else:
        p = cur.left
        while p.right and p.right is not cur:
            p = p.right
        if p.right is None:
            p.right = cur; cur = cur.left        # thread, descend
        else:
            p.right = None; visit(cur); cur = cur.right   # unthread, visit, go on
```

**The habit**: type `p.right = None` in the same breath as `p.right = cur`, and
never write a `return` inside the loop. Those two reflexes prevent every
corruption bug this algorithm has.

**The numbers**: at most `2n` outer iterations and `2(n-1)` inner steps, so
`Θ(n)` time; `O(1)` extra space against the stack walk's `O(h)`, where `h` is
`log n` if you are lucky and `n` if you are not; up to `2(n-1)` writes into a
structure that used to be read-only. And one boundary fact worth carrying:
*in-order* is the only order you get for free; preorder is one moved line, and
postorder is a different algorithm.

## Check yourself

:::check
Why is the right pointer of `pred(x)` guaranteed to be free — why can we be sure
we are not overwriting a real child?
--
Because `pred(x)` is defined as the *rightmost* node of `x`'s left subtree: the
node you reach by starting at `x.left` and following right pointers until there
are none. "Until there are none" is exactly the statement that its right pointer
is null. If it had a right child, the walk would not have stopped there.

This is Lemma A in the proof, and it is worth noticing that the lemma is about
the *unmodified* tree. Run two Morris traversals over the same tree
concurrently and the second one finds a non-null right pointer where it expected
null — the guarantee comes from exclusive access, not from the shape of trees.
:::

:::check
Someone says: "Morris is O(n log n), not O(n). For each of the `n` nodes you
search for its in-order predecessor, and that search walks a spine of length up
to the height, so it is `n` searches times `O(h)`." Where are they wrong?
--
The bound is real but it is not tight, and the fix is a counting argument rather
than a sharper per-search bound.

Consider a right edge `u → u.right`. It is stepped over during the predecessor
search for node `x` only if `u` lies on the right spine of `x.left`. Given `u`,
that `x` is uniquely determined: walk up from `u` through right-edges-from-parent
as far as you can; the node you stop at is `x.left`, and `x` is its parent. So
each right edge belongs to the spine of exactly one node, and the spines are
disjoint. The total length of all spines is therefore at most the number of
right edges, which is at most `n - 1`. Each spine is walked twice — once to
plant the thread, once to cut it — so all the searches together cost at most
`2(n - 1)` steps, not `n · h`.

The pattern is the standard one: a worst case that cannot happen to every node
at once. The same reasoning is why the total work of the "push the whole left
spine" step in the stack-based traversal is also linear.
:::

:::check
Exactly one line moves to turn Morris in-order into Morris preorder. Which one,
and why is there no analogous one-line change for postorder?
--
Move the `visit(cur)` from the unthreading branch to the thread-creating branch
(and keep the one in the `cur.left is None` branch). Preorder wants the node
before its left subtree, which is precisely the moment we plant the thread.

There is no postorder equivalent because a node is entered only twice as `cur`:
once going down into the left subtree, once returning from it. Postorder needs a
third moment — after the right subtree has finished — and when the loop leaves a
node to the right, it never comes back to that node. The usual O(1)-space
postorder recovers the missing output by, at each unthreading, walking the right
spine of the left subtree backwards using an in-place reversal. That is a
different algorithm that happens to share the threading trick.
:::

:::check
You write a constant-space "k-th smallest in a BST" using Morris, and return as
soon as the counter hits `k`. The tests pass. What is broken, and what does the
damage actually look like?
--
Every thread planted for an ancestor you have not yet returned to is still in
the tree. For the tree `4(2(1,3),5)` with `k = 2`, the loop returns while
`3.right` still points at `4`, so the structure contains the cycle
`4 → 2 → 3 → 4`. It is no longer a tree: a recursive traversal of it will not
terminate, a recursive `__repr__` will raise, a reference-counted free will
leak, and any later Morris run will misread that thread as its own.

The tests pass because they check the returned value, and the returned value is
correct. Corruption of a caller's data structure is invisible to a test that
only inspects the return value — which is the general lesson.

The repair is to let the loop run to completion with visiting switched off after
the answer is found (or equivalently, keep unthreading until `cur` is null).
That costs Θ(n) even for `k = 1`, so the early-exit saving is gone. Stating that
trade-off is part of the right answer.
:::

:::check
Why must the inner loop test `pred.right is not cur` rather than
`pred.right != cur`, and what goes wrong if you use the value comparison in a
language where nodes compare by value?
--
The test is asking a question about *which object* a pointer refers to: "is this
pointer the thread I planted, pointing back at the node I am standing on?" Only
identity answers that. Value equality answers a different question — "does this
pointer refer to a node that looks like the one I am standing on?" — and in a
tree with duplicate keys, or a `Node` with a structural `__eq__`, two different
nodes can look the same.

The failure is not a wrong answer, it is destruction. Suppose the spine walk
reaches a node `p` whose genuine right child `c` happens to compare equal to
`cur`. The loop stops early at `p`, takes the "thread already exists" branch,
and executes `p.right = None` — silently detaching `c` and everything below it.
The traversal then reports fewer nodes than the tree contains, and the caller's
tree has lost a subtree permanently. In Python the default `Node` has identity
equality so `==` happens to work, which is exactly why the habit of writing `is`
matters: it is the version that survives being translated into Java or C++.
:::
