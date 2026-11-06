# Binary Search Trees

> A binary search tree is binary search frozen into pointers: every node promises that everything on its left is smaller and everything on its right is larger, so one comparison throws away a whole subtree, and every operation costs the height of the tree instead of its size.

## The problem it solves

[[p:citadel-binary-search-tree-operations|Binary Search Tree Operations]] gives you
a stream of operations on a set of integers, starting empty: insert a key, search
for a key, delete a key, in any order. A real system asks more of the same set: list
the keys in sorted order, find the next key larger than x, find the k-th smallest,
sum the keys between two bounds.

There are two obvious first solutions, and each is good at half the job.

**An unsorted list.** Insert is an append: one step. Search has to look at every
key: n steps. Sorted order means sorting every time someone asks.

**A sorted list with binary search.** Search is fast: [[binary-search]] halves the
range each step, so a million keys take 20 comparisons. Sorted order, the next
larger key and the k-th smallest are all free, because the list is already in
order. But insert is slow. To put 5 into `[1, 3, 4, 6, 7, 8]` you find its place in
3 comparisons and then shift 6, 7, 8 one slot to the right to make room. In the
worst case every insert shifts everything: inserting 100,000 keys in decreasing
order shifts 0 + 1 + ... + 99,999, about 5 x 10^9 elements. Delete has the same
problem in reverse.

What we want is search like a sorted array and insert like a linked list. That is
exactly what a binary search tree gives, on one condition about its shape that this
chapter will make precise. It also gives the things a hash set cannot: order. A
hash set answers "is 5 here?" in constant time, but it cannot say what comes after
5, or how many keys are below 5, or what the keys are in order, without looking at
all of them.

This chapter builds the tree from binary search itself, then the five things
interviews ask of it: that **in-order traversal is sorted**, how to **validate**
it with bounds, how to **search and insert by the ordering**, the **lowest common
ancestor**, and the **k-th smallest**. It assumes [[trees]] (what a node, subtree,
height and post-order are) and [[binary-search]].

### When it is the wrong tool

- **You only ask "is x present?".** A hash set is simpler and faster. A BST earns
  its place only when order matters.
- **The keys never change.** A sorted array with binary search (Python's `bisect`)
  does every ordered query a BST does, with less code and better constants.
- **You only ever want the minimum.** A [[heap]] is simpler and its worst case is
  guaranteed.
- **You need guaranteed O(log n) and the input can arrive sorted.** A plain BST
  degrades to a chain (shown below). You need a self-balancing tree
  ([[balanced-bst]]) or an [[ordered-set]]. Python's standard library has neither,
  which is why Python solutions often use a sorted list and accept O(n) inserts,
  or a [[fenwick-tree]] over compressed keys.

## Build it from the brute force

### Step 1: look at what binary search actually does

Run binary search on the sorted array `[1, 3, 4, 6, 7, 8, 10, 13, 14]`. Whatever
you search for, the first comparison is with the middle, 7. If the target is
smaller, the next comparison is with the middle of the left half, 3; if larger,
with the middle of the right half, 10. And so on. Write down every comparison any
search could ever make, with an arrow from each comparison to the two that can
follow it:

```
                 7
            /         \
          3             10
        /   \         /    \
       1     4       8      13
              \              \
               6              14
```

That picture is a tree. Every search is a walk from the top down one path, going
left when the target is smaller and right when it is larger. Binary search on an
array **is** a walk down this tree; the array just hides the tree in its index
arithmetic. The midpoint formula `mid = (lo + hi) // 2` is how the array finds "the
left child" without storing a pointer.

### Step 2: count what insertion costs, and see why

Inserting into the array is slow because positions are implicit. Key 6 lives at
index 3 because exactly three keys are smaller. Insert 5, and now four keys are
smaller than 6, so 6 must move, and so must everything after it. The array spends
its time keeping "index = number of smaller keys" true for every key at once.

The tree does not need that. In the tree, 6 is reached by "right of 3, left of 7";
inserting 5 changes nothing about that route. So store the tree itself: each node
holds a key and two pointers. To insert 5, walk down as if searching for it: 5 < 7
go left, 5 > 3 go right, 5 > 4 go right, 5 < 6 go left, and there is no node
there. That empty spot is exactly where a search for 5 would end, so put 5 there as
a new leaf. Nothing moves. The cost is the length of one path.

### Step 3: what must be true for search to work?

Here is the question that defines the whole structure. When the search for 5
stands at node 7 and goes left, it never looks at 8, 10, 13, 14 again. Why is that
allowed?

**What does one comparison at this node let me throw away?**

The search compared 5 with 7 and threw away the entire right side. That is safe
only if *nothing* on the right side could be 5, which means every key in 7's right
subtree must be larger than 7 (and so larger than 5). Likewise every key in the
left subtree must be smaller than 7. So the rule a binary search tree must keep is
about whole subtrees, at every node:

> **The BST invariant:** for every node v, every key in v's left subtree is
> smaller than v's key, and every key in v's right subtree is larger.

With that invariant, one comparison at v discards one of v's subtrees completely,
and the search only ever walks one path. Without it, a discarded subtree might have
held the key, and the search is wrong.

Say it a second way. The invariant is not a fact about a node and its children. It
is a promise each node makes about **everything below it on each side**. A search
trusts that promise every time it turns.

### You might think: "It is enough that each left child is smaller and each right child is larger."

This is the most common wrong idea about BSTs, and it fails on a four-node tree:

```
        5
       / \
      3   8
       \
        6
```

Every node is correct compared with its children: 3 < 5, 8 > 5, 6 > 3. But 6 sits
in the **left** subtree of 5 and is larger than 5. Now search for 6. At 5: 6 > 5,
go right. At 8: 6 < 8, go left. Nothing there. The search says 6 is not in the
tree, and it is. The local check accepted a tree on which the very first operation
gives a wrong answer.

So validating a BST means checking that every node fits inside the range its
ancestors allow, not just that it compares correctly with its parent. Node 6 is
the right child of 3, so it must be larger than 3; and it is inside the left
subtree of 5, so it must be smaller than 5. It must lie in (3, 5). It does not.

### You might think: "A BST makes every operation O(log n)."

It makes every operation O(height). The height depends on the order the keys
arrived in. Insert 1, 2, 3, 4, 5 in that order: 2 > 1 goes right, 3 > 1 and 3 > 2
goes right again, and so on. The tree is a chain leaning right, of height 4, and
searching for 5 compares with every key. Inserting n sorted keys costs
0 + 1 + ... + (n - 1) = n(n - 1)/2 comparisons: exactly the sorted array's bad case,
come back in another form.

Keys that arrive in random order give a tree whose average depth is about
2 ln n, roughly 1.39 log2 n, so a random tree is fine. Keys that arrive sorted,
or nearly sorted, which real data often does, give a chain. That is the entire
reason balanced trees exist. The code below measures both.

### Step 4: the free gift, sorted order

Look at the invariant from a different side. At node v, every key on the left is
smaller than v and every key on the right is larger. So if you list the left
subtree's keys (in sorted order), then v, then the right subtree's keys (in sorted
order), the whole list is sorted. That listing is exactly **in-order traversal**:
left, node, right.

**In-order traversal of a BST visits the keys in increasing order.**

This one fact turns into four techniques: listing keys in order, the k-th smallest
(stop at the k-th key visited), an iterator that hands out keys one at a time, and
a second way to validate a BST (the in-order sequence must be strictly increasing).
It is also the reason the right way to think about a BST is "a sorted list, stored
as a tree".

### You might think: "The next larger key is the right child."

The successor of a key x is the smallest key larger than x. In the tree built in
the trace below, the successor of 3 is 4, which is not 3's right child (6) but the
leftmost node of 3's right subtree. And the successor of 7, which has no right
subtree at all, is 8: an **ancestor**, the last node where the path down to 7
turned left. So successor has two cases, and both fall out of in-order: the next
key after x in sorted order is either the smallest thing in x's right subtree, or,
if x has no right subtree, the nearest ancestor that x is to the left of.

The search-based version avoids the cases: walk down from the root as if searching
for x, and every time you go left (because x < node), remember that node as a
candidate. The last candidate remembered is the successor.

### The technique in one sentence

**A binary search tree keeps every key smaller than a node on its left and every
larger key on its right, so a search, an insert or a range query discards a whole
subtree at each comparison and walks one path, and an in-order walk lists the keys
in sorted order.**

And the question that unlocks every BST problem: **what does one comparison at
this node let me throw away?** If the answer is "one whole side", walk one path.
If the answer is "nothing", the problem is not using the ordering, and you are
walking the whole tree.

## Worked by hand

Get a pen. Every trace below uses one tree, built by inserting
**8, 3, 10, 1, 6, 14, 4, 7, 13** in that order into an empty tree.

### Trace 1: building it, one insert at a time

Each insert walks down from the root, comparing, until it falls off the tree;
the new key becomes a leaf at that spot.

| insert | path of comparisons | falls off at | comparisons |
| --- | --- | --- | --- |
| 8 | (empty tree) | becomes the root | 0 |
| 3 | 3 < 8 | left of 8 | 1 |
| 10 | 10 > 8 | right of 8 | 1 |
| 1 | 1 < 8, 1 < 3 | left of 3 | 2 |
| 6 | 6 < 8, 6 > 3 | right of 3 | 2 |
| 14 | 14 > 8, 14 > 10 | right of 10 | 2 |
| 4 | 4 < 8, 4 > 3, 4 < 6 | left of 6 | 3 |
| 7 | 7 < 8, 7 > 3, 7 > 6 | right of 6 | 3 |
| 13 | 13 > 8, 13 > 10, 13 < 14 | left of 14 | 3 |

Seventeen comparisons for nine keys. The row for 7, in words:

> "I am inserting 7. At the root, 7 < 8, so 7 belongs somewhere on 8's left; the
> whole right side, 10, 14, 13, is out of the question forever. At 3, 7 > 3, so I
> go right; 1 is out. At 6, 7 > 6, so I go right, and 6 has no right child. That
> empty spot is where a search for 7 would end, so 7 goes there. On the way I was
> told three things: smaller than 8, larger than 3, larger than 6. So 7 must lie
> in (6, 8), and it does."

That last sentence is the important one. Every turn on the way down narrows the
range the new key is allowed to be in. A left turn at a node sets an upper bound;
a right turn sets a lower bound. Here is the finished tree with each node's allowed
range written under it, and the search path for 7 shaded:

<svg viewBox="0 0 700 330" role="img" aria-label="the BST built from 8, 3, 10, 1, 6, 14, 4, 7, 13, each node labelled with the open interval its ancestors allow; the search path 8, 3, 6, 7 is shaded">
  <g>
    <line x1="326" y1="52" x2="194" y2="98" stroke-width="4"/>
    <line x1="354" y1="52" x2="486" y2="98"/>
    <line x1="166" y1="122" x2="114" y2="168"/>
    <line x1="194" y1="122" x2="246" y2="168" stroke-width="4"/>
    <line x1="514" y1="122" x2="586" y2="168"/>
    <line x1="252" y1="194" x2="218" y2="236"/>
    <line x1="268" y1="194" x2="302" y2="236" stroke-width="4"/>
    <line x1="592" y1="194" x2="568" y2="236"/>
    <circle class="fill" cx="340" cy="40" r="18"/>
    <text x="340" y="46" text-anchor="middle">8</text>
    <circle class="fill" cx="180" cy="110" r="18"/>
    <text x="180" y="116" text-anchor="middle">3</text>
    <circle cx="500" cy="110" r="18"/>
    <text x="500" y="116" text-anchor="middle">10</text>
    <circle cx="100" cy="180" r="18"/>
    <text x="100" y="186" text-anchor="middle">1</text>
    <circle class="fill" cx="260" cy="180" r="18"/>
    <text x="260" y="186" text-anchor="middle">6</text>
    <circle cx="600" cy="180" r="18"/>
    <text x="600" y="186" text-anchor="middle">14</text>
    <circle cx="210" cy="250" r="18"/>
    <text x="210" y="256" text-anchor="middle">4</text>
    <circle class="fill" cx="310" cy="250" r="18"/>
    <text x="310" y="256" text-anchor="middle">7</text>
    <circle cx="560" cy="250" r="18"/>
    <text x="560" y="256" text-anchor="middle">13</text>
    <text x="368" y="36">(-inf, +inf)</text>
    <text x="120" y="92" text-anchor="middle">(-inf, 8)</text>
    <text x="560" y="92" text-anchor="middle">(8, +inf)</text>
    <text x="100" y="218" text-anchor="middle">(-inf, 3)</text>
    <text x="300" y="168">(3, 8)</text>
    <text x="640" y="218" text-anchor="middle">(10, +inf)</text>
    <text x="190" y="288" text-anchor="middle">(3, 6)</text>
    <text x="330" y="288" text-anchor="middle">(6, 8)</text>
    <text x="560" y="288" text-anchor="middle">(10, 14)</text>
    <text x="350" y="322" text-anchor="middle">search 7: 7 &lt; 8 left, 7 &gt; 3 right, 7 &gt; 6 right, found. 10, 14, 13, 1, 4 never looked at.</text>
  </g>
</svg>

Read the ranges as a check on yourself. 4 is in (3, 6): larger than 3 because it
is on 3's right, smaller than 6 because it is on 6's left, and smaller than 8, which
the 6 already implies. 13 is in (10, 14). Each range is the parent's range, cut at
the parent's key: left child keeps the lower end and takes the parent as its upper
end; right child takes the parent as its lower end and keeps the upper end. That
is the whole of the bounds validation, drawn.

### Trace 2: searching, found and not found

**Search 7:** 8 (go left), 3 (go right), 6 (go right), 7 (found). Four nodes looked
at, out of nine.

**Search 5:** 8 (5 < 8, left), 3 (5 > 3, right), 6 (5 < 6, left), 4 (5 > 4,
right), and 4 has no right child. Not found, after four nodes. Notice that the
place a failed search stops is exactly where an insert of 5 would put it. Search
and insert are the same walk; insert just does something at the end.

### Trace 3: the same keys, in sorted order

Insert 1, 3, 4, 6, 7, 8, 10, 13, 14. Each key is larger than everything before it,
so each walk goes right at every node and falls off the bottom:

| insert | comparisons |
| --- | --- |
| 1 | 0 |
| 3 | 1 |
| 4 | 2 |
| 6 | 3 |
| ... | ... |
| 14 | 8 |

Thirty-six comparisons instead of seventeen, and a search for 14 now looks at all
nine nodes. Same keys, same set, different tree. The shape is decided by the
arrival order, and the cost of every later operation is decided by the shape.

### Trace 4: in-order, paused (the k-th smallest)

In-order means "left subtree, node, right subtree". To do it without recursion,
keep a stack of the nodes you have walked past on the way down-left, whose own
turn has not come yet. To get the next key: pop the top (nothing smaller remains
anywhere), then push the left spine of its right subtree.

Find the 4th smallest key.

| step | action | stack after (top on the right) | keys handed out |
| --- | --- | --- | --- |
| start | push left spine from 8: 8, 3, 1 | [8, 3, 1] | |
| 1 | pop 1; 1 has no right child | [8, 3] | 1 |
| 2 | pop 3; push left spine of 6: 6, 4 | [8, 6, 4] | 1, 3 |
| 3 | pop 4; no right child | [8, 6] | 1, 3, 4 |
| 4 | pop 6; push left spine of 7: 7 | [8, 7] | 1, 3, 4, **6** |

The 4th smallest is 6, and the walk stopped: 10, 13 and 14 were never touched.
Step 2, in words: "the stack's top is 3. Everything smaller than 3 (just 1) has
already been handed out, and nothing in 3's right subtree is smaller than 3, so 3
is next. After 3 come the keys in its right subtree, smallest first, and the
smallest key of a subtree is at the bottom of its left spine: 6, then 4. Push both;
4 is on top."

Two facts fall out of this trace. The stack never holds more than one path's worth
of nodes, so it is O(h) memory. And each node is pushed once and popped once over
the whole walk, so handing out all n keys costs O(n) in total, which is O(1) per
key on average. That is [[p:atlassian-binary-search-tree-iterator|Binary Search Tree Iterator]].

### Trace 5: validation with bounds, on the tree that fools the local check

The bad tree: 5 with children 3 and 8, and 6 as the right child of 3.

| node | allowed range (from ancestors) | key | verdict |
| --- | --- | --- | --- |
| 5 | (-inf, +inf) | 5 | ok |
| 3 | (-inf, 5): left of 5 | 3 | ok |
| 6 | (3, 5): right of 3, inside left of 5 | 6 | **fails**: 6 is not below 5 |

The local check compares 6 only with its parent 3 and says yes. The bounds check
carries the 5 down from the root and says no. The in-order check finds it too:
in-order is 3, 6, 5, 8, and 6 > 5 is a descent.

### Trace 6: the lowest common ancestor by splitting

The lowest common ancestor of p and q is the deepest node that has both in its
subtree (a node counts as its own ancestor). In a BST you can find it walking down
one path. Find LCA(4, 7):

| at | compare | action |
| --- | --- | --- |
| 8 | 4 < 8 and 7 < 8 | both on the left: go left |
| 3 | 4 > 3 and 7 > 3 | both on the right: go right |
| 6 | 4 < 6 < 7 | they split here: **6** |

At 6, in words: "4 is smaller than me, so it is in my left subtree; 7 is larger,
so it is in my right subtree. Any node below me is in one subtree or the other,
so it cannot be above both. I am the lowest node with both below me."

LCA(4, 3): at 8 both go left; at 3, one of them *is* 3. Stop: **3**. A node equal
to p or q is the split point, because the other one is below it.

## From the idea to the code

### The direct version: search, insert, delete

Search and insert are loops: one comparison, one step down, repeat. Delete needs
one idea more, so first the cases.

- **The node has no children.** Remove it.
- **It has one child.** Splice it out: its parent points straight at the child.
  The child's whole subtree was already on the correct side of the parent, so the
  invariant still holds.
- **It has two children.** You cannot splice; the parent has room for only one of
  them. Instead, find the key that should take this node's place: the **successor**,
  the smallest key in the right subtree (the leftmost node there). It is larger
  than everything on the left (it came from the right) and smaller than everything
  else on the right (it is the smallest there). Copy its key into this node, then
  delete the successor from the right subtree. The successor has no left child (it
  is leftmost), so that second delete is one of the easy cases.

```python run
import random

class Node:
    __slots__ = ("key", "left", "right")
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None

def search(root, key):
    node, steps = root, 0
    while node is not None:
        steps += 1
        if key == node.key:
            return True, steps
        node = node.left if key < node.key else node.right   # discard one side
    return False, steps

def insert(root, key):
    if root is None:
        return Node(key)
    node = root
    while True:
        if key == node.key:
            return root                       # a set: no duplicates
        side = "left" if key < node.key else "right"
        nxt = getattr(node, side)
        if nxt is None:
            setattr(node, side, Node(key))    # hang a leaf where the search fell off
            return root
        node = nxt

def delete(node, key):                        # returns the new root of this subtree
    if node is None:
        return None
    if key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:
        if node.left is None:                 # zero or one child: splice it out
            return node.right
        if node.right is None:
            return node.left
        succ = node.right                     # two children: the next larger key
        while succ.left is not None:
            succ = succ.left
        node.key = succ.key                   # take its key ...
        node.right = delete(node.right, succ.key)   # ... and remove it from the RIGHT
    return node

def inorder(node, out):
    if node is not None:
        inorder(node.left, out)
        out.append(node.key)
        inorder(node.right, out)
    return out

def height(node):                             # in edges; empty tree -1
    return -1 if node is None else 1 + max(height(node.left), height(node.right))

root = None
for k in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    root = insert(root, k)
print("inorder:", inorder(root, []))
print("search 7:", search(root, 7), " search 5:", search(root, 5))
assert inorder(root, []) == [1, 3, 4, 6, 7, 8, 10, 13, 14]
assert search(root, 7) == (True, 4) and search(root, 5) == (False, 4)
root = delete(root, 3)                        # two children: 4 takes its place
print("after deleting 3:", inorder(root, []), "new key at that spot:", root.left.key)
assert root.left.key == 4 and inorder(root, []) == [1, 4, 6, 7, 8, 10, 13, 14]

random.seed(3)
for trial in range(200):                      # against Python's set
    t, s = None, set()
    for _ in range(60):
        op, k = random.randint(0, 2), random.randint(0, 30)
        if op == 0:
            t = insert(t, k); s.add(k)
        elif op == 1:
            t = delete(t, k); s.discard(k)
        else:
            assert search(t, k)[0] == (k in s)
        assert inorder(t, []) == sorted(s)
print("insert/search/delete agree with set() on 200 random runs")

n = 512
keys = list(range(n))
shuffled = keys[:]
random.shuffle(shuffled)
t_sorted, t_random = None, None
for k in keys[:300]:                          # 300 sorted keys: a chain
    t_sorted = insert(t_sorted, k)
for k in shuffled:
    t_random = insert(t_random, k)
print("height, 300 keys inserted in order :", height(t_sorted))
print("height, %d keys in random order   :" % n, height(t_random), "(perfect would be 8)")
assert height(t_sorted) == 299 and height(t_random) < 4 * 9
```

The last two lines are the cost section in miniature. Three hundred sorted keys
make a tree of height 299, one node per level. Five hundred and twelve shuffled
keys make a tree of height in the low twenties; a perfect tree of that size has
height 8. Random is not perfect, but it is within a small constant factor of
log2 n. Sorted is n.

### Each line, and which part of the idea it is

| line | in plain words | which part of the idea |
| --- | --- | --- |
| `node = node.left if key < node.key else node.right` | go to the only side that can hold the key | one comparison discards a subtree |
| `if key == node.key: return root` | already present | a set; a multiset would count instead |
| `setattr(node, side, Node(key))` | the search fell off here, so the key belongs here | insert is a failed search plus one leaf |
| `if node.left is None: return node.right` | zero or one child: the child replaces me | splicing keeps every subtree on its side |
| `while succ.left is not None` | the leftmost node of my right subtree | the successor: next key in sorted order |
| `node.key = succ.key` | the successor's key moves into my node | it fits: above my left, below the rest of my right |
| `node.right = delete(node.right, succ.key)` | remove the original successor | must be the right subtree, and must be assigned |

Three confusions worth settling now:

- **Delete returns a node, and the caller assigns it.** `node.left = delete(...)`
  is how the parent learns that its child changed (because the child was spliced
  out, or the root itself was deleted). Forgetting the assignment is a real bug,
  demonstrated in Traps.
- **Insert does not rebalance.** The tree's shape is whatever the arrival order
  makes it. That is what "plain BST" means.
- **Duplicates need a policy.** The code above ignores a repeated insert (a set).
  A multiset either stores a count in the node, or sends equal keys consistently to
  one side (say, right), and then validation must allow equality on that side only.
  Most problems say "values are unique"; read for it.

### The subtle line, both ways: validation

The subtle line in BST code is the validation check, and the wrong version is the
one everybody writes first. Here are both, plus the in-order check, on the tree
from Trace 5. The program also runs a search for 6 on that tree, to show that the
tree the local check accepts really is broken.

```python run
class Node:
    __slots__ = ("key", "left", "right")
    def __init__(self, key, left=None, right=None):
        self.key, self.left, self.right = key, left, right

def search(node, key):
    while node is not None and node.key != key:
        node = node.left if key < node.key else node.right
    return node is not None

def valid_local(node):                       # WRONG: compares only with children
    if node is None:
        return True
    if node.left is not None and not node.left.key < node.key:
        return False
    if node.right is not None and not node.key < node.right.key:
        return False
    return valid_local(node.left) and valid_local(node.right)

def valid_bounds(node, lo=None, hi=None, log=None):
    if node is None:
        return True
    ok = (lo is None or lo < node.key) and (hi is None or node.key < hi)
    if log is not None:
        log.append("%2d must be in (%s, %s): %s" % (node.key,
                   "-inf" if lo is None else lo, "+inf" if hi is None else hi,
                   "ok" if ok else "FAILS"))
    if not ok:
        return False
    return (valid_bounds(node.left, lo, node.key, log) and    # left: below me
            valid_bounds(node.right, node.key, hi, log))      # right: above me

def valid_inorder(node):                     # the other right answer: strictly rising
    prev, stack = None, []
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None and not prev < node.key:
            return False
        prev, node = node.key, node.right
    return True

#        5
#       / \
#      3   8          6 is the right child of 3: bigger than 3, fine locally,
#       \             but it sits in the LEFT subtree of 5
#        6
bad = Node(5, Node(3, None, Node(6)), Node(8))
log = []
print("local check says:", valid_local(bad))
print("bounds check says:", valid_bounds(bad, log=log))
for line in log:
    print("   ", line)
print("inorder check says:", valid_inorder(bad))
print("and search for 6 finds it:", search(bad, 6))
assert valid_local(bad) and not valid_bounds(bad) and not valid_inorder(bad)
assert not search(bad, 6)                    # 6 > 5, so search goes right and misses

good = Node(8, Node(3, Node(1), Node(6, Node(4), Node(7))), Node(10, None, Node(14, Node(13))))
assert valid_local(good) and valid_bounds(good) and valid_inorder(good)
dup = Node(5, Node(5))                       # a duplicate: strict BSTs reject it
assert not valid_bounds(dup) and not valid_inorder(dup)
edge = Node(-2**31, None, Node(2**31 - 1))   # extremes are legal keys; None bounds cope
assert valid_bounds(edge)
print("good tree valid, duplicate rejected, 32-bit extremes accepted")
```

Point at the exact place the wrong version goes wrong. It checks 6 against 3 and
stops, because 3 is all it can see. The bounds version arrives at 6 carrying
(3, 5): the 3 from its parent, and the 5 from its grandparent, passed down through
the left turn at the root. That 5 is the information the local check never had.

What does the local check actually compute? "Every parent-child edge is in the
right order." That is a weaker property than a BST, and the gap between the two is
exactly the keys that are in the right place relative to their parent but the wrong
place relative to a higher ancestor. So the smallest counterexample needs a
grandparent and a zigzag: three nodes, 5, its left child 3, and 3's right child 6.
The 8 in the block's tree is only there to make it look ordinary.

Say the rule twice. **Each node must fit inside the interval its ancestors
allow, and the interval shrinks with every turn.** Or: going left sets the upper
bound to the current key; going right sets the lower bound to it; the other bound is
inherited unchanged.

Two smaller details in that block matter in interviews. The bounds start as
`None`, meaning "no bound", rather than the smallest and largest integers. In a
language with fixed-size integers, starting at `INT_MIN` and `INT_MAX` wrongly
rejects a tree that contains `INT_MIN` with a strict check; the last assert tests
exactly that. And the comparisons are strict (`<`), because the bank's validation
problems define a strict BST: [[p:amazon-validate-strict-binary-search-tree|Validate a Strict Binary Search Tree]]
says equal values are not allowed. A duplicate must fail.

### The ordered operations: iterator, k-th, successor, LCA

The next program is Traces 4 and 6 as code: the paused in-order walk (which is the
iterator and the k-th smallest), the successor by remembering left turns, the LCA
by splitting, and one more trick from the bank.

```python run
class Node:
    __slots__ = ("key", "left", "right")
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root

class Inorder:                               # an in-order walk you can pause
    def __init__(self, root):
        self.stack = []
        self._push_left(root)
    def _push_left(self, node):              # the left spine: smallest on top
        while node is not None:
            self.stack.append(node)
            node = node.left
    def has_next(self):
        return bool(self.stack)
    def next(self):
        node = self.stack.pop()              # nothing smaller is left anywhere
        self._push_left(node.right)          # its right subtree comes next
        return node.key

def kth_smallest(root, k):
    it = Inorder(root)
    for _ in range(k - 1):
        it.next()
    return it.next()

def successor(root, key):                    # next larger key, no parent pointers
    best, node = None, root
    while node is not None:
        if key < node.key:
            best, node = node.key, node.left # a candidate; look for a smaller one
        else:
            node = node.right                # node.key <= key: too small, go right
    return best

def lca(root, p, q):                         # the first node that splits p and q
    node = root
    while True:
        if p < node.key and q < node.key:
            node = node.left
        elif p > node.key and q > node.key:
            node = node.right
        else:
            return node.key                  # between them, or equal to one

def lca_by_insertion(order, p, q):           # no tree needed
    lo, hi = min(p, q), max(p, q)
    return next(x for x in order if lo <= x <= hi)

order = [8, 3, 10, 1, 6, 14, 4, 7, 13]
root = None
for k in order:
    root = insert(root, k)

it, seen = Inorder(root), []
while it.has_next():
    seen.append(it.next())
print("iterator:", seen)
assert seen == sorted(order)
print("4th smallest:", kth_smallest(root, 4))
assert kth_smallest(root, 4) == 6
print("successor of 3, 7, 14:", successor(root, 3), successor(root, 7), successor(root, 14))
assert (successor(root, 3), successor(root, 7), successor(root, 14)) == (4, 8, None)
for p, q, want in [(4, 7, 6), (4, 3, 3), (1, 13, 8), (13, 14, 14)]:
    assert lca(root, p, q) == lca_by_insertion(order, p, q) == want
print("lca(4,7) =", lca(root, 4, 7), "| lca(4,3) =", lca(root, 4, 3), "| lca(1,13) =", lca(root, 1, 13))

chain = list(range(1, 2001))                 # sorted insertion: a 2000-deep chain
print("inserted chain, lca(1500, 1999) =", lca_by_insertion(chain, 1500, 1999))
assert lca_by_insertion(chain, 1999, 1500) == 1500
```

Line by line, the parts that carry the idea:

- `self._push_left(node.right)` in `next` is the whole iterator. After a node is
  handed out, the next keys in sorted order are its right subtree's, smallest
  first, and the smallest is at the bottom of that subtree's left spine.
- `best, node = node.key, node.left` in `successor` is "this node is larger than
  the key, so it is a candidate; but something smaller and still larger than the key
  may be on its left". Every left turn improves the candidate, and the last one
  standing is the answer. Floor, ceiling and "closest value" are the same loop with
  the roles adjusted.
- The `else` in `lca` catches three situations at once: p < node < q, q < node <
  p, and node equal to one of them. All three mean "they do not go the same way from
  here".

The last function is a property worth knowing for
[[p:amazon-bst-lowest-common-ancestor|Lowest Common Ancestor in an Inserted BST]],
which gives you the insertion order instead of a tree. The LCA of p and q is the
**first inserted key that lies between them** (inclusive). Why: until a key in
[p, q] arrives, every inserted key is below both or above both, so p and q would
take the same turn at it. The first key x in [p, q] lands somewhere, and every later
key in the range, including p and q, follows the same path to x and then splits at
it. So no tree has to be built, which matters, because that problem allows
100,000 keys, and a sorted insertion order would build a 100,000-deep chain.

## Why it is correct

Everything above rests on one invariant. The proof shows three things: that the
invariant makes in-order sorted, that search is correct when the invariant holds,
and that insert and delete keep it holding. Validation by bounds is the invariant
checked directly, so its correctness comes along.

:::proof The BST invariant: what it gives, and why the operations keep it
**The invariant.** For every node v, every key in v's left subtree is less than
v.key, and every key in v's right subtree is greater than v.key.

**Claim 1: in-order lists the keys in increasing order.** Induction on the size of
the tree. An empty tree lists nothing, which is sorted. For a tree with root v,
in-order lists the left subtree, then v, then the right subtree. By the induction
hypothesis (both subtrees are smaller, and each is itself a BST, because the
invariant holds at all of their nodes) each part is sorted. By the invariant, every
key in the first part is less than v.key and every key in the last part is greater.
So the concatenation is sorted.

**Claim 2: search finds the key if and only if it is in the tree.** If search
returns "found", it has seen the key, so the key is there. For the other direction,
suppose key k is in the tree. Keep this statement true: *if k is in the tree, it is
in the subtree of the current node.* At the start the current node is the root, so
it is true. At a node v with k ≠ v.key: if k < v.key, then k is not in v's right
subtree (everything there is greater than v.key, so greater than k), and it is not
v, so it is in v's left subtree, and search moves there. The case k > v.key is the
mirror. So the statement stays true at every step. Every step moves one level down,
so search stops after at most height + 1 steps, either at a node holding k or at an
empty subtree. An empty subtree contains nothing, so by the statement k was not in
the tree. So if k is there, search finds it.

**Claim 3: insert keeps the invariant.** Insert of k walks the same path as a
search for k and attaches k as a leaf where the walk fell off. Take any ancestor a
of the new leaf. The walk went left at a exactly when k < a.key, and then the new
leaf is in a's left subtree; it went right exactly when k > a.key, and then the
leaf is in a's right subtree. So k is on the correct side of every ancestor. No
other node's subtree changed. The invariant still holds everywhere.

**Claim 4: delete keeps the invariant.** Removing a leaf removes a key from some
subtrees and adds none, so every "all keys on the left are smaller" statement stays
true. Splicing out a node v with one child c: every key of c's subtree was already
inside v's subtree, so it was already on the correct side of each of v's
ancestors; attaching c where v was keeps it on the same side. For two children:
let s be the smallest key in v's right subtree. Every key in v's left subtree is
less than v.key, which is less than s, so s may sit above the left subtree. Every
other key in v's right subtree is greater than s, because s is the smallest there,
so s may sit above the rest of the right subtree. And s was already in v's
subtree, so it is on the correct side of every ancestor of v. Writing s into v and
then deleting the original s (which has no left child, so it is one of the easy
cases) leaves the invariant true.

**Claim 5: the bounds check accepts exactly the BSTs.** Call node v's interval
(lo, hi) the one the check passes down: the root gets (-inf, +inf), a left child
gets (lo, v.key), a right child gets (v.key, hi). By induction down the tree, v's
interval is exactly "greater than every ancestor whose right subtree holds v, less
than every ancestor whose left subtree holds v", because each turn adds one such
condition and the interval keeps the tightest one. The BST invariant says exactly
that every node satisfies all of those conditions. So "every key lies inside its
interval" is a restatement of the invariant, node by node, and the check, which
tests every node, accepts precisely the trees for which it holds. ∎
:::

What that used, in plain words:

- **The invariant holds at every node, about whole subtrees.** Claim 2's step "k
  is not in the right subtree" needs *all* of the right subtree to be greater, not
  just the right child. That is the local-check bug, located in the proof.
- **Keys are comparable and the comparison is consistent.** Every claim used
  "k < v.key or k > v.key or equal", with the same answer every time. A comparator
  that is not a total order (it says a < b and b < a, or changes its mind) breaks
  Claim 2. [[p:apple-validate-bst-with-comparator|Validate a BST with a Custom Comparison]]
  is a reminder that the ordering is whatever the problem says it is.
- **No duplicates, or a stated policy for them.** The invariant is written with
  strict inequalities. With duplicates allowed on one side, every claim survives
  with a non-strict inequality on that side, and the bounds check must match it.
- **The delete's successor really is the minimum of the right subtree.** Claim 4's
  two-child case depended on that one fact. A "successor" found anywhere else
  breaks the invariant.
- **Nothing about the shape.** None of the claims mention balance. Correctness is
  free; speed is not. That is the next section.

## What it costs

**Every single-path operation costs O(h).** Search, insert, delete, successor,
floor, ceiling and the BST LCA each walk one root-to-node path, doing a constant
amount of work per node. Delete with two children walks down to v and then on down
to the successor, still one path. So the cost is at most h + 1 comparisons, where
h is the height.

**h is between log2 n and n - 1, and the arrival order decides.** A binary tree of
height h holds at most 2^(h+1) - 1 nodes, so h >= log2(n + 1) - 1, and a chain
reaches n - 1. Building a BST by inserting n keys costs the sum of the depths at
which they land:

- **Sorted input:** depths 0, 1, ..., n - 1, total n(n - 1)/2. For 100,000 keys,
  about 5 x 10^9 comparisons. This is the sorted array's insert cost, back again.
- **Random order:** the expected depth of a node is about 2 ln n, roughly
  1.39 log2 n, so building costs about 1.39 n log2 n comparisons, close to
  sorting. The tree's height is larger than the average depth, but still a small
  multiple of log2 n; the run block measured low twenties for 512 keys.

Count the sorted case a second way to see it is not bad luck: each new key is
larger than every key already in the tree, so it is compared with every node on the
right spine, and the right spine is the whole tree.

**Whole-tree operations cost O(n).** In-order listing visits each node once
(Θ(n)). Validation must look at every node, because one bad node anywhere makes the
answer false. The iterator hands out n keys with n pushes and n pops in total, so
any single `next()` can cost O(h) (it pushes a whole left spine), but the average
over all of them is O(1): **amortised** O(1).

**The k-th smallest by an in-order walk costs O(h + k):** the initial left spine,
then k pops, each with its pushes. For k near n that is O(n). If many k-th queries
come between updates, store in every node the size of its subtree. Then at node v
with left subtree size L: if k <= L, go left; if k = L + 1, the answer is v; else go
right looking for the (k - L - 1)-th. That is O(h) per query, at the price of
updating sizes on every insert and delete
([[p:salesforce-dynamic-order-statistic-bst|Dynamic Order-Statistic Binary Search Tree]]
asks for exactly this).

**Range queries cost O(h + m)**, where m is the number of keys reported: the walk
follows the two boundary paths and visits the m keys between them. In Trace 1's
tree, summing [4, 9] touches 8, 3, 6, 4, 7, 10 and skips 1, 13 and 14.

**The hidden costs.**

- **Recursion depth is h.** A recursive insert or validate on a chain of 10^5
  nodes hits Python's limit of about 1,000 frames. Search and insert are naturally
  loops; write them as loops.
- **Python has no built-in balanced tree.** `bisect.insort` on a list is O(n) per
  insert, but the shifting is one fast memory move, so for 10^5 operations it is
  usually acceptable. For truly dynamic ordered data with large n, compress the keys
  and use a [[fenwick-tree]], or implement a balanced tree.
- **A node per key.** Each Python object costs dozens of bytes; a sorted list of
  ints is several times smaller.

## How to think about it

On every problem that mentions a BST, or that needs order on a changing set:

1. **Is there an ordering I can use?** Is the tree given as a BST, or am I free to
   build one? If the tree is a plain binary tree, the BST tricks do not apply.
2. **Does one comparison throw away a side?** For search, insert, successor,
   floor, ceiling and LCA, yes: walk one path, O(h). For sums, validation or
   counting, no single side can be thrown away, but a range bound can still cut whole
   subtrees.
3. **Is the question about sorted order?** k-th smallest, "next", iterate, two
   keys that are out of order, closest values: in-order is sorted, so think of the
   tree as the sorted list it encodes.
4. **Strict or not, and duplicates?** Read the definition in the statement and
   write it as a comment: `lo < key < hi`, or `lo <= key < hi`.
5. **What information must come down, and what must come up?** Validation brings
   an interval down. "Largest BST subtree" brings (is-BST, min, max, sum) up. The
   [[trees]] question again.
6. **How tall can it get?** If the keys can arrive sorted, the tree can be a
   chain. Use loops, and if the cost matters, a balanced structure.
7. **One query or many?** Many queries on a fixed tree: flatten it once by
   in-order into a sorted array and use [[prefix-sums]] and [[binary-search]].
   Many queries with updates: augment the nodes (subtree sizes, sums).

### Telling it from its neighbours

- **BST or sorted array?** Same queries; the array has better constants and no
  shape problems, the tree has cheap inserts. Static data: array.
- **BST or hash set?** The hash set has no order. Only membership: hash set.
- **BST or heap?** A heap knows its minimum and nothing else in order; it cannot
  find the successor of an arbitrary key. Only the minimum (or maximum): heap.
- **BST LCA or binary-tree LCA?** With the ordering, one path down. Without it,
  the post-order question "which of my sides report a target?". Same name,
  different algorithm; see [[lca]].
- **Plain BST or balanced BST?** Interviews almost never ask you to write a
  red-black tree. They ask what goes wrong without one (sorted input, a chain) and
  what fixes it ([[balanced-bst]]).

## Variations

### A. Search, insert, delete

What changes: nothing but the action at the end of the walk. Why: all three are a
search. [[p:citadel-binary-search-tree-operations|Binary Search Tree Operations]]
asks for all three from scratch and explicitly forbids a library container.
[[p:tokopedia-delete-bst-node|Delete Node in a BST]] fixes the two-child rule
(successor, not predecessor), so that one output is correct; read for that, since
the predecessor (largest key on the left) is equally valid in general.

```
delete 3 from 8(3(1, 6(4, 7)), 10):  3 has two children; successor = 4
-> copy 4 into 3's node, delete 4 from the right subtree 6(4, 7)
-> 8(4(1, 6(-, 7)), 10)
```

### B. Floor, ceiling, successor, closest

What changes: what you remember on the way down. Why: every left turn passes a
key larger than the target (a ceiling candidate), every right turn passes a smaller
one (a floor candidate).

- Successor (smallest key > x): remember on left turns.
  [[p:charta-bst-inorder-successor|Inorder Successor in a Binary Search Tree]].
- Predecessor (largest key < x): remember on right turns.
- Closest value: remember the best |key - x| along the search path.
  [[p:roblox-closest-binary-search-tree-value-variant|Closest Binary Search Tree Value]]
  ties to the smaller value, so compare (distance, value) pairs.

```
tree 8(3(1, 6(4, 7)), 10(-, 14(13))), x = 5
path: 8 (left, ceiling 8), 3 (right, floor 3), 6 (left, ceiling 6), 4 (right, floor 4)
floor 4, ceiling 6, closest: |4-5| = |6-5| = 1, tie -> 4
```

### C. In-order is sorted

What changes: you walk the whole tree, or pause the walk. Why: the in-order
sequence is the sorted list of keys.

- **k-th smallest:** stop at the k-th key.
  [[p:amazon-kth-smallest-element-in-bst|Kth Smallest Element in a BST]].
- **Iterator:** the stack of the left spine.
  [[p:atlassian-binary-search-tree-iterator|Binary Search Tree Iterator]].
- **Convert to a sorted doubly linked list:** an in-order walk that links each
  node to the previous one, in place.
  [[p:apple-bst-to-circular-doubly-linked-list|BST to Sorted Circular Doubly Linked List]].
- **Two swapped keys:** the in-order sequence of a BST with two keys swapped has
  one descent (adjacent swap) or two; the first descent's larger key and the last
  descent's smaller key are the two to swap back.
  [[p:globalization-partners-recover-binary-search-tree|Recover Binary Search Tree]].

```
in-order 1 3 7 6 4 8: descents at 7>6 and 6>4 -> swap 7 and 4 -> 1 3 4 6 7 8
```

- **Closest values and many range queries:** flatten by in-order into a sorted
  list once, then use two pointers or binary search.
  [[p:linkedin-kth-closest-bst|Kth Closest Element in a BST]] expands two
  pointers outward from the target's insertion point;
  [[p:meta-repeated-bst-range-aggregates|Repeated BST Range Sum and Average]] adds
  prefix sums, so each of 200,000 queries is two binary searches.

### D. Validate with bounds, and build with bounds

What changes: an interval travels down. Why: the invariant is a statement about
ancestors, and the interval is the summary of all of them.

- [[p:atlassian-validate-binary-search-tree|Validate Binary Search Tree]] and
  [[p:amazon-validate-strict-binary-search-tree|Validate a Strict Binary Search Tree]]:
  the bounds check, or the in-order check.
- [[p:lyft-reconstruct-bst-from-preorder|Reconstruct a BST from Preorder]]: the
  same intervals used to **build**. Read the preorder with one pointer; a call with
  interval (lo, hi) takes the next value only if it fits, makes it a node, builds
  its left subtree with (lo, value) and its right with (value, hi). Each value is
  read once: O(n), against O(n^2) for inserting the values one by one into a chain.
- [[p:amazon-maximum-sum-bst|Maximum Sum BST in a Binary Tree]]: the bounds check
  turned upside down. In a plain binary tree, find the largest-sum subtree that is a
  BST. Each node needs to know whether its children are BSTs and their minimum and
  maximum keys, so each call returns (is_bst, min, max, sum), a post-order combine
  exactly like the diameter in [[trees]].

```
preorder 8 5 1 7 10 12: 8 (-inf, inf); 5 fits (-inf, 8); 1 fits (-inf, 5);
7 does not fit (-inf, 1) or (1, 5) -> back up; 7 fits (5, 8); 10 fits (8, inf) ...
```

### E. The lowest common ancestor, three ways

What changes: what the tree gives you. Why each works is different, which is why
they are worth seeing side by side.

- **A BST:** split point, one path down. O(h).
  [[p:peoplestrong-lowest-common-ancestor-bst|Lowest Common Ancestor in a BST]].
- **Only the insertion order of a BST:** the first inserted key between p and q.
  [[p:amazon-bst-lowest-common-ancestor|Lowest Common Ancestor in an Inserted BST]].
- **A plain binary tree:** no ordering, so no split. Post-order: a node returns
  "I found p or q (or both) below me"; the first node to get a yes from both sides,
  or that is a target with a yes below it, is the LCA.
  [[p:atlassian-lowest-common-ancestor-of-a-binary-tree|Lowest Common Ancestor of a Binary Tree]].
- **Parent pointers:** mark every ancestor of p, then climb from q until you hit a
  mark. [[p:blackrock-lowest-common-ancestor-parent-tree|Lowest Common Ancestor in a Parent Tree]].
  For many queries on one tree, [[binary-lifting]].

A use: the distance between two nodes is depth(p) + depth(q) - 2 depth(LCA).
[[p:google-shortest-path-between-bst-nodes|Shortest Path Between BST Nodes]] is that,
with depths found by searching.

### F. Ranges: sum and trim

What changes: the walk visits both sides when the node is inside the range and one
side when it is outside. Why: a node below the range has its whole left subtree
below the range too.

- [[p:meta-range-sum-of-bst|Range Sum of BST]]: if node < lo, only the right
  subtree can help; if node > hi, only the left; otherwise both, plus the node.
- [[p:google-trim-binary-search-tree-range|Trim a Binary Search Tree to a Range]]:
  the same three cases, returning a new subtree root. A node below the range is
  replaced by its trimmed right subtree, so the root itself can change.

### G. Build a balanced BST from sorted data

What changes: you choose the shape. Why: the middle key as the root splits the rest
evenly, and the same rule on each half gives height about log2 n.
[[p:expedia-build-perfect-bst|Build a Perfect Binary Search Tree]] is exactly this,
for key counts of the form 2^h - 1. The binary search picture in Step 1 is the same
rule applied to nine keys, which is why its bottom level is uneven.
[[p:salesforce-sorted-doubly-linked-list-to-balanced-bst|Sorted Doubly Linked List to Balanced BST In Place]]
does it on a list, by building the left half first while a pointer walks the list.

### H. Balanced trees and ordered sets (rare to implement)

AVL and red-black trees keep the height O(log n) by rotating after inserts and
deletes. You will be asked why they exist far more often than to write one. Their
chapter is [[balanced-bst]]; the library structures built on them, and what to use
in Python instead, are in [[ordered-set]].

## Recognising it in a statement

Ordered by how much to trust them.

1. **"Binary search tree"**, or "every value in the left subtree is smaller". The
   ordering is handed to you. Ask what one comparison throws away.
2. **"Validate", "is this a BST", "two nodes were swapped".** Bounds or in-order.
3. **"k-th smallest", "next larger", "in sorted order", "iterator".** In-order.
4. **"Insert, delete and query in sorted order", "next greater key that exists"**,
   on a changing set. A BST or an ordered set. In Python, `bisect` on a sorted list
   for moderate n.
5. **"Lowest common ancestor" with an ordering.** The split walk.
6. **"Sum of keys in [lo, hi]", "trim to a range".** Pruning by the ordering.

The disguises:

- **A preorder with "the values form a BST".** That is enough to rebuild the tree
  (Variation D); a plain binary tree would need a second traversal.
- **"Build the tree by inserting these values in order", then a query.** Often the
  query can be answered from the order itself (the LCA trick), without building a
  tree that may be a chain.
- **"Count, for each element, how many later elements are smaller."** Inserting
  from the right into a BST with subtree sizes answers it, but a [[fenwick-tree]] or
  [[merge-sort]] does it with a guaranteed bound.

Anti-signals:

- **A plain binary tree** in the statement. "Lowest common ancestor of a binary
  tree" without the word search is the post-order version.
- **Only membership.** Hash set.
- **Only the minimum or the top k.** [[heap]].
- **A static sorted array.** [[binary-search]] directly; there is nothing to gain
  from pointers.

## Traps

**Validating against children only.** Symptom: accepts trees on which search
fails; usually caught by one hidden test with a zigzag. Fix: carry (lo, hi) down,
or check that in-order is strictly increasing. Demonstrated above.

**Sentinel bounds that collide with real keys.** Symptom: a valid tree containing
the smallest or largest integer is rejected. Fix: use "no bound" (None, or a
separate flag), or a wider type than the keys.

**`<=` where the statement says strict, or the reverse.** Symptom: duplicates
accepted or rejected wrongly. Fix: copy the statement's definition into a comment
and make the comparisons match it.

**Pruning the wrong side in a range query.** Symptom: sums that are far too small,
no crash. When the node is below the range, its *left* subtree is all too small;
the right subtree can still hold keys in range. Flip the two and you discard the
only side that could help.

**Forgetting to assign the result of a recursive delete.** Symptom: the deleted key
is still there, or appears twice. `delete(node.right, key)` without `node.right =`
splices the node out of a subtree that nobody is pointing at any more, and when the
deleted node was the direct child, the parent still points at it.

Both of those, wrong and right, on real trees:

```python run
class Node:
    __slots__ = ("key", "left", "right")
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root

def keys(node):
    return [] if node is None else keys(node.left) + [node.key] + keys(node.right)

def range_sum(node, lo, hi, flipped=False, seen=None):
    if node is None:
        return 0
    if seen is not None:
        seen.append(node.key)
    if not flipped:
        if node.key < lo:                    # me and my whole LEFT side are too small
            return range_sum(node.right, lo, hi, flipped, seen)
        if node.key > hi:                    # me and my whole RIGHT side are too big
            return range_sum(node.left, lo, hi, flipped, seen)
    else:                                    # WRONG: skips the side that can still help
        if node.key < lo:
            return range_sum(node.left, lo, hi, flipped, seen)
        if node.key > hi:
            return range_sum(node.right, lo, hi, flipped, seen)
    return (node.key + range_sum(node.left, lo, hi, flipped, seen)
                     + range_sum(node.right, lo, hi, flipped, seen))

root = None
for k in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    root = insert(root, k)
seen = []
right = range_sum(root, 4, 9, seen=seen)
wrong = range_sum(root, 4, 9, flipped=True)
print("sum of keys in [4, 9]: right", right, "wrong", wrong, "| right visited", seen)
assert right == 4 + 6 + 7 + 8 == 25 and wrong != 25
assert 1 not in seen and 14 not in seen      # whole subtrees skipped safely

def delete(node, key, forget_assign=False):
    if node is None:
        return None
    if key < node.key:
        node.left = delete(node.left, key, forget_assign)
    elif key > node.key:
        node.right = delete(node.right, key, forget_assign)
    elif node.left is None:
        return node.right
    elif node.right is None:
        return node.left
    else:
        succ = node.right
        while succ.left is not None:
            succ = succ.left
        node.key = succ.key
        if forget_assign:
            delete(node.right, succ.key)     # WRONG: the spliced subtree is dropped
        else:
            node.right = delete(node.right, succ.key)
    return node

for forget in (False, True):
    t = None
    for k in [5, 3, 8, 9]:                   # 8 is 5's successor AND its right child
        t = insert(t, k)
    t = delete(t, 5, forget)
    print("delete 5,", "forgot to assign:" if forget else "assigned:     ", keys(t))
    assert keys(t) == ([3, 8, 8, 9] if forget else [3, 8, 9])
```

Look at the wrong range sum. At the root, 8 is in range, so it looks both ways. At
3, below the range, the flipped version goes *left*, to 1, which is smaller still,
and never reaches 6, 4 and 7. On the right side it does the mirror and never comes
back from 14. Total 8, only the root. The right version reaches every key in range
and still skips 1, 13 and 14 without looking.

The delete bug needs the successor to be the deleted node's own right child, as 8
is here. Then `delete(node.right, 8)` returns 9 (the splice), and nobody stores it:
5's node now holds 8 and still points at the old 8. Two 8s. When the successor is
deeper, the assignment that matters happens inside the recursive call, and the bug
hides.

**Recursion on a skewed tree.** Symptom: `RecursionError` on one hidden test. A BST
built from sorted input is a chain. Write search, insert, successor and LCA as loops
(they are one path, so they need no stack), and the in-order walk with an explicit
stack.

**Building the tree when you did not need to.** Symptom: time limit on
"insert these 10^5 values, then answer a question", because the values arrived
sorted and the tree is a chain. Ask whether the question can be answered from the
values (the LCA-by-insertion trick), or build a balanced tree from the sorted values
directly.

**Using the BST LCA on a plain binary tree.** Symptom: wrong answers whenever the
values are not ordered. The split walk is correct only under the invariant.

**Off-by-one in k.** "k-th smallest" is usually 1-based. The in-order walk's first
key is the 1st smallest.

**Changing the tree while an iterator is paused over it.** The iterator's stack
holds nodes; deleting one of them or inserting above them makes the stack describe
a tree that no longer exists. Finish iterating, or rebuild the iterator.

## What to memorise

The invariant, said the right way: **everything in the left subtree is smaller,
everything in the right subtree is larger, at every node.**

The sentence that turns a problem into a BST walk: **"What does one comparison at
this node let me throw away?"**

The habit that prevents the common bug: **carry the bounds down.** Any time a BST
condition has to be checked or used, it is a condition on an interval inherited
from all the ancestors, not on the parent.

The templates:

```python
node = root                               # search / insert / floor / ceiling: one path
while node is not None and node.key != key:
    node = node.left if key < node.key else node.right

def valid(node, lo=None, hi=None):        # validation: an interval comes down
    if node is None:
        return True
    if (lo is not None and node.key <= lo) or (hi is not None and node.key >= hi):
        return False
    return valid(node.left, lo, node.key) and valid(node.right, node.key, hi)

stack, node = [], root                    # in-order, paused: k-th, iterator
while stack or node:
    while node:
        stack.append(node)
        node = node.left
    node = stack.pop()
    ...                                   # node.key is the next key in sorted order
    node = node.right

while True:                               # LCA in a BST: the split point
    if p < node.key and q < node.key:   node = node.left
    elif p > node.key and q > node.key: node = node.right
    else: break
```

Numbers worth carrying: every single-path operation is O(h); h is about
1.39 log2 n on average for random insertion order and n - 1 for sorted order;
inserting n sorted keys costs n(n - 1)/2 comparisons; the iterator is amortised O(1)
per key with O(h) memory.

## Check yourself

:::check
Hand trace. Insert 50, 30, 70, 20, 40, 60, 80, 35, 45, 65 into an empty BST. Draw
the tree. Write the comparison path for the insert of 45, and the allowed interval
of every node. Then delete 30 and draw the result.
--
The tree: 50 has 30 and 70; 30 has 20 and 40; 70 has 60 and 80; 40 has 35 and 45;
60 has a right child 65.

Insert 45: 45 < 50 left, 45 > 30 right, 45 > 40 right, empty: 45 is 40's right
child. Three comparisons.

Intervals: 50 (-inf, +inf); 30 (-inf, 50); 70 (50, +inf); 20 (-inf, 30); 40
(30, 50); 35 (30, 40); 45 (40, 50); 60 (50, 70); 65 (60, 70); 80 (70, +inf).

Delete 30: two children. The successor is the leftmost node of 30's right subtree:
40, then left to 35, which has no left child. Copy 35 into 30's node; delete 35
from the right subtree (it is a leaf). Result: 50 has 35 and 70; 35 has 20 and 40;
40 has only 45. In-order: 20 35 40 45 50 60 65 70 80, still sorted.
:::

:::check
Hand trace. On the tree from the first exercise (before the delete), run the paused
in-order walk to find the 6th smallest key. Write the stack after every pop.
--
Start: push the left spine from 50: [50, 30, 20].

1. Pop 20 (1st). No right child. Stack [50, 30].
2. Pop 30 (2nd). Push the left spine of 40: 40, 35. Stack [50, 40, 35].
3. Pop 35 (3rd). Stack [50, 40].
4. Pop 40 (4th). Push the left spine of 45: 45. Stack [50, 45].
5. Pop 45 (5th). Stack [50].
6. Pop 50 (6th). **The answer is 50.** (It would push 70 and 60 next.)

Check against the sorted list 20 30 35 40 45 50 60 65 70 80: the 6th is 50. The
stack never held more than three nodes, one path's worth.
:::

:::check
Hand trace, both checks. Is this tree a BST? Run the local check and the bounds
check, and write each node's interval.

```
        10
       /  \
      5    15
          /  \
         6    20
```
--
Local check: 5 < 10, 15 > 10, 6 < 15, 20 > 15. Every edge is fine, so it says yes.

Bounds: 10 in (-inf, +inf) ok; 5 in (-inf, 10) ok; 15 in (10, +inf) ok; 6 in
(10, 15): **fails**, 6 is not greater than 10. Not a BST. In-order agrees:
5 10 6 15 20 has the descent 10 > 6.

The damage: search for 6 goes 10 (6 < 10, left) to 5 (6 > 5, right), finds nothing,
and reports 6 missing.
:::

:::check
Why is the iterator's `next()` called "amortised O(1)" when a single call can push
a whole left spine of h nodes? Give a tree and a call where one `next()` costs h.
--
Count over the whole iteration instead of per call. Every node is pushed exactly
once (when the walk passes it on some left spine) and popped exactly once (when it
is handed out). So n calls to `next()` do n pops and n pushes in total: O(n) for n
calls, O(1) each on average, whatever the shape.

A costly single call: the root has no left child and a right child r, and below r
hangs a chain of h - 1 left children. The call that returns the root pushes r and
that whole chain, h nodes, in one call. But those h nodes are then popped by the next
h calls, which push nothing. The expensive call pays in advance for the cheap ones.
:::

:::check
Someone says: "My BST is fine: I insert with the usual loop and every operation is
O(log n), because a binary tree with n nodes has height log n." Where are they
wrong, and what input breaks them?
--
A binary tree with n nodes has height *at least* about log2 n, not at most. The
height of a plain BST depends on the insertion order, and nothing in the insert
loop keeps it small.

Sorted input breaks it: inserting 1, 2, ..., n makes every key the right child of
the one before, a chain of height n - 1. Every search for a large key then compares
with every node, and building the tree costs n(n - 1)/2 comparisons, about
5 x 10^9 for n = 10^5. Random order gives an average depth of about 1.39 log2 n;
only a self-balancing tree ([[balanced-bst]]) guarantees O(log n) whatever the order.
:::

:::check
Disguised problem. You are given the values a BST was built from, in insertion
order (up to 10^5 of them, distinct), and two values p and q. Return the value of
their lowest common ancestor. Why can building the tree time out, and what is the
O(n) answer?
--
Building is a sequence of inserts, each O(depth). If the order is sorted, the tree
is a chain and building costs about n^2/2, around 5 x 10^9 steps. Recursion would
also exceed the stack limit.

The answer without a tree: scan the insertion order and return the first value x
with min(p, q) <= x <= max(p, q). Before x arrives, every inserted value is below
both or above both, so p and q would turn the same way at it; x then sits on both
of their paths, and they split there (or x is one of them). That is the split-point
rule, read off the order of arrival instead of the shape.
:::

:::check
Someone validates with the in-order check but writes it as "collect the in-order
list, then check `lst == sorted(lst)`". Where are they wrong, and what does it cost?
--
`lst == sorted(lst)` accepts duplicates: [5, 5] is equal to its sorted self. A
strict BST must reject a node equal to its parent, so the check must be
`all(a < b for a, b in zip(lst, lst[1:]))`.

Cost: it is correct apart from that, but sorting adds O(n log n) and the list adds
O(n) memory, when a single in-order walk that remembers only the previous key is
O(n) time and O(h) memory, and can stop at the first descent instead of walking
the whole tree.
:::
