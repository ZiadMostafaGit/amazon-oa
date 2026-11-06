# Binary Heaps and Priority Queues

> A heap answers one question, "who is next?", after every change, and it is fast because it refuses to know anything else: it keeps only one fact per element, "I am no smaller than my parent", instead of the whole sorted order.

## The problem it solves

You have four ropes, of lengths 4, 3, 2 and 6. You may join any two ropes into
one, and a join costs the sum of the two lengths. The joined rope has that
combined length and can be joined again. You want one rope at the end, for the
least total cost. That is [[p:inmobi-connect-n-ropes-minimum-cost|Connect N Ropes With Minimum Cost]].

The rule that works (and we will see why in the variations) is: always join the
two shortest ropes you have right now. On 4, 3, 2, 6:

| round | ropes before | join | cost | ropes after |
|---|---|---|---|---|
| 1 | 4, 3, 2, 6 | 2 + 3 | 5 | 4, 6, 5 |
| 2 | 4, 6, 5 | 4 + 5 | 9 | 6, 9 |
| 3 | 6, 9 | 6 + 9 | 15 | 15 |

Total 5 + 9 + 15 = 29.

Look at what each round needs. It asks "which two are smallest?", takes them out,
and puts a **new** rope back in. The new rope is not one of the original lengths,
so you could not have known where it fits before the round started. The set of
ropes changes between every question.

The first program anyone writes keeps the ropes in a plain list. Finding the
smallest is a scan of the whole list, and it happens twice per round, so each
round costs about 2n steps and the whole run costs about n^2. The statement allows
10^5 ropes. That is 10^10 steps, far beyond a time limit.

The second program keeps the list sorted, so the two smallest are always at one
end and can be taken for free. Now the cost moves to the insert. The joined rope
must go into the right place, and Python's `bisect` finds that place in log n
steps, but then every element after it must shift one cell to make room. That is
up to n moves per insert, and again about n^2 for the run.

So the brute force has two extremes, and each one pays O(n) somewhere: the
unsorted list pays on every "find the smallest", the sorted list pays on every
"put this back". What this chapter builds is a structure where **both** costs are
about log2 n: 17 steps for 10^5 elements instead of 10^5. That structure is a
binary heap, and the interface it provides, "insert" and "remove the smallest",
is called a priority queue.

The shape to remember: **a set that keeps changing, and a question about its
extreme that keeps being asked.** 415 problems in this bank use a heap, and
almost all of them have that shape somewhere inside.

### When it is the wrong tool

- **The set never changes.** If the elements are all known and nothing is added
  back, sort once and walk the sorted list. It is simpler and no slower.
- **You want the k-th element once.** From a fixed array,
  [[quickselect]] is expected O(n). A heap of size k is O(n log k), which is
  close and often fine, but it is not the best.
- **You ask about rank, not the extreme.** "How many elements are below x?",
  "what is the next value above x?", "what is the 37th smallest right now?" A heap
  cannot answer any of these. That is an [[ordered-set]] or a [[fenwick-tree]].
- **You must delete an element in the middle.** A heap has no "remove this
  value" operation. There is a workaround (lazy deletion, in the variations),
  but if the problem is mostly arbitrary deletions, a heap is the wrong base.
- **The extreme of a sliding window.** The maximum of every window of size k is
  O(n) with a [[monotonic-deque]], better than the O(n log n) of a heap.

## Build it from the brute force

We will not start from a tree. We will start from the two lists a beginner writes,
look at exactly what each one wastes, and let the heap appear as the obvious
middle ground.

### Step 1: the two brute forces, and their bill

Both lists support the same two operations: `insert(x)` and `pop_min()`.

| | insert | pop_min | n of each |
|---|---|---|---|
| unsorted list | append: O(1) | scan for the min: O(n) | O(n^2) |
| sorted list | find slot, shift the rest: O(n) | take the end: O(1) | O(n^2) |

The program below runs the ropes problem with both, counts the work, and checks
that both get the same answer. Run it and look at the "per rope" columns: they
double when n doubles. Work per operation that grows with n is the signature of a
quadratic algorithm.

```python run
import bisect
import heapq
import random

def ropes_unsorted(ropes):
    """Brute force 1: a plain list. Insert is O(1), finding the min is a scan."""
    pool, cost, work = list(ropes), 0, 0
    while len(pool) > 1:
        pair = 0
        for _ in range(2):
            i = min(range(len(pool)), key=pool.__getitem__)   # scan everything
            work += len(pool)
            pair += pool.pop(i)
        cost += pair
        pool.append(pair)                                     # cheap insert
    return cost, work

def ropes_sorted(ropes):
    """Brute force 2: keep the list sorted. Min is free, insert shifts."""
    pool, cost, work = sorted(-x for x in ropes), 0, 0       # negated: smallest rope last
    while len(pool) > 1:
        pair = -pool.pop() - pool.pop()                       # O(1): the two smallest
        cost += pair
        i = bisect.bisect_left(pool, -pair)                   # O(log n) to find the slot
        work += len(pool) - i + 1                             # but every cell after it shifts
        pool.insert(i, -pair)
    return cost, work

def ropes_sort_once(ropes):
    """Wrong instinct: sort once and fold left. The joined rope never re-enters."""
    xs = sorted(ropes)
    cost, cur = 0, xs[0]
    for x in xs[1:]:
        cur += x
        cost += cur
    return cost

def ropes_heap(ropes):
    h = list(ropes)
    heapq.heapify(h)
    cost = 0
    while len(h) > 1:
        pair = heapq.heappop(h) + heapq.heappop(h)
        cost += pair
        heapq.heappush(h, pair)        # the joined rope goes back into the order
    return cost

print("[1,1,1,1]: sort once and fold ->", ropes_sort_once([1, 1, 1, 1]),
      "  re-enter the order ->", ropes_heap([1, 1, 1, 1]))
assert ropes_sort_once([1, 1, 1, 1]) == 9 and ropes_heap([1, 1, 1, 1]) == 8
print("ropes [4, 3, 2, 6]:", ropes_unsorted([4, 3, 2, 6])[0], ropes_sorted([4, 3, 2, 6])[0])
assert ropes_unsorted([4, 3, 2, 6])[0] == ropes_sorted([4, 3, 2, 6])[0] == 5 + 9 + 15

rng = random.Random(2)
for n in (500, 1000, 2000):
    xs = [rng.randint(1, 10**4) for _ in range(n)]
    (c1, w1), (c2, w2) = ropes_unsorted(xs), ropes_sorted(xs)
    assert c1 == c2 == ropes_heap(xs)
    print("n=%5d  unsorted scan work %9d (%5.0f per rope)   sorted shifts %8d (%5.0f per rope)"
          % (n, w1, w1 / n, w2, w2 / n))
    assert w1 > n * n / 2 and w2 > n * n / 8   # both grow like n squared
print("doubling n roughly quadruples the scan: one side of the design always pays O(n)")
```

### You might think: "Just sort once, then go through the ropes in order."

This is the most common first instinct, and the block above kills it. Sort
[1, 1, 1, 1], then fold from the left: 1 + 1 = 2 (cost 2), 2 + 1 = 3 (cost 3),
3 + 1 = 4 (cost 4). Total 9. But the best is 8: join 1 + 1 (cost 2), join the
other 1 + 1 (cost 2), join 2 + 2 (cost 4).

What went wrong is that the joined rope of length 2 is, after the first round,
**not the smallest rope any more**: two ropes of length 1 are still waiting. The
fold-left keeps joining onto the growing rope because the sorted order was
computed once, before the 2 existed. A sorted list built at the start is a
promise about the elements you had at the start. Every insertion breaks the
promise. That is why this problem is not a sort.

### Step 2: notice the waste

Look at what the sorted list knows. For four ropes 2, 3, 4, 6, it knows that 2 is
smallest, but also that 4 comes before 6, that 3 comes before 4, and so on: the
relative order of every one of the 4 x 3 / 2 = 6 pairs. For n elements that is
n(n-1)/2 facts. Each insert must keep all of them true, which is why it must
find the exact slot and shift everything after it.

How many of those facts does the ropes problem ever use? Only one: which element
is smallest. The relation between the 4 and the 6 is never asked about until one
of them becomes the smallest, and by then several new ropes may have arrived and
changed the picture anyway. The sorted list is paying, on every insert, to keep
an answer to questions nobody will ask.

The unsorted list has the opposite problem. It knows nothing, so each "who is
smallest?" starts from zero, and the scan learns the order of everything it
looks at and then forgets it all.

### The question that unlocks it

So the question to ask, on this problem and every problem in the family, is:

**What is the least the structure must know so that it can always say who is
next, and stay that way cheaply after a change?**

Not the whole order, and not nothing. Something in between, which can be repaired
with a small amount of work when one element arrives or leaves.

Here is the answer. Arrange the elements in a tree, and keep exactly one fact per
element: **every element is no smaller than its parent.** Call this the heap
order. Nothing is said about two siblings, or about two elements in different
branches.

Is that enough to find the smallest? Yes. Start at any element and walk up to the
root. Each step goes to the parent, which is no larger. So the root is no larger
than anything below it, which is everything. The minimum is at the root, always.

Say it a second way. Picture a knockout tournament. The champion is known, and
everyone has lost to somebody one round above them. But nobody has ranked the
runners-up against each other, because nobody needed to. A heap is a tournament
that is never fully played out: the champion is certain, and the rest are only
as ordered as the champion's position requires.

### Step 3: choose the tree so that it costs nothing to store

Any tree with the heap order has its minimum at the root. To make the repairs
cheap we want the tree as short as possible, and to make it cheap to store we
want no pointers at all. Both come from one choice: a **complete** binary tree,
where every level is full except possibly the last, and the last is filled from
the left.

Number the nodes level by level, left to right, starting at 0. The root is 0, its
children 1 and 2, theirs 3, 4, 5, 6, and so on. Then a node's relatives are
arithmetic:

```text
parent(i) = (i - 1) // 2      left(i) = 2i + 1      right(i) = 2i + 2
```

The tree is just a Python list, read in that order. Here is the heap that holds
1, 2, 8, 5, 3:

<svg viewBox="0 0 660 300" role="img" aria-label="a five-node min-heap drawn as a tree above the array that stores it in level order: 1 at the root, 2 and 8 below it, 5 and 3 below the 2; the array reads 1, 2, 8, 5, 3 at indices 0 to 4">
  <g>
    <circle class="fill" cx="330" cy="40" r="22"/>
    <text x="330" y="46" text-anchor="middle">1</text>
    <circle cx="190" cy="115" r="22"/>
    <text x="190" y="121" text-anchor="middle">2</text>
    <circle cx="470" cy="115" r="22"/>
    <text x="470" y="121" text-anchor="middle">8</text>
    <circle cx="120" cy="185" r="22"/>
    <text x="120" y="191" text-anchor="middle">5</text>
    <circle cx="260" cy="185" r="22"/>
    <text x="260" y="191" text-anchor="middle">3</text>
    <line x1="203" y1="97" x2="317" y2="58"/>
    <line x1="457" y1="97" x2="343" y2="58"/>
    <line x1="133" y1="167" x2="177" y2="133"/>
    <line x1="247" y1="167" x2="203" y2="133"/>
    <rect x="180" y="225" width="60" height="38" rx="4"/>
    <rect x="240" y="225" width="60" height="38" rx="4"/>
    <rect x="300" y="225" width="60" height="38" rx="4"/>
    <rect x="360" y="225" width="60" height="38" rx="4"/>
    <rect x="420" y="225" width="60" height="38" rx="4"/>
    <text x="210" y="250" text-anchor="middle">1</text>
    <text x="270" y="250" text-anchor="middle">2</text>
    <text x="330" y="250" text-anchor="middle">8</text>
    <text x="390" y="250" text-anchor="middle">5</text>
    <text x="450" y="250" text-anchor="middle">3</text>
    <text x="210" y="283" text-anchor="middle">0</text>
    <text x="270" y="283" text-anchor="middle">1</text>
    <text x="330" y="283" text-anchor="middle">2</text>
    <text x="390" y="283" text-anchor="middle">3</text>
    <text x="450" y="283" text-anchor="middle">4</text>
    <text x="20" y="250">value</text>
    <text x="20" y="283">index</text>
    <text x="20" y="40">every node is</text>
    <text x="20" y="62">no smaller than</text>
    <text x="20" y="84">its parent</text>
  </g>
</svg>

Check the arithmetic on real cells. Index 1 holds 2; its children are 2*1+1 = 3
and 2*1+2 = 4, which hold 5 and 3. Both are at least 2. Index 4 holds 3; its
parent is (4-1)//2 = 1, which holds 2. Index 2 holds 8 and has children 5 and 6,
which do not exist (the list has only 5 cells), so 8 is a leaf.

Notice what the list is **not**. It is not sorted: index 2 holds 8, index 3 holds
5. The last cell is not the maximum: it holds 3, and the maximum 8 is in the
middle. Only the four parent-child pairs are constrained: (1,2), (1,8), (2,5),
(2,3). That is n - 1 = 4 facts, against the 10 a sorted list would keep.

### Step 4: insert, by asking where a new element can go

A new element has to occupy a cell. If it goes anywhere but the end of the list,
the cells after it shift and every parent-child relation renumbers, which
destroys the tree. So it goes at the end, the next free cell in the bottom level.
That keeps the tree complete.

Has it broken the heap order? Only possibly with its own parent: every other pair
is untouched. If it is smaller than its parent, swap them. Now it may be smaller
than its new parent, so check again. It walks up, one level per step, and stops
when its parent is no larger, or when it reaches the root. This is **sift up**.
At most one step per level, and there are about log2 n levels.

### Step 5: remove the minimum, by asking which cell can disappear

The minimum is at the root, so that is the value we return. But the list must
get one cell shorter, and the only cell that can vanish without renumbering
anything is the **last** one. So take the last element, put it in the root's
place, and shrink the list by one.

Now the root probably holds something too big. Compare it with its two children.
If it is no larger than both, it can stay. Otherwise swap it with the **smaller**
of the two children, and repeat from its new position. It walks down until both
its children are no smaller, or it reaches a leaf. This is **sift down**. Again
at most one step per level.

### You might think: "When the root leaves, just promote the smaller child, and keep promoting."

It sounds natural: the root is gone, the smaller child is the new minimum, so
move it up, then fill its hole with its smaller child, and so on down to a leaf.
The values come out in the right order. The shape does not.

Take the heap [1, 2, 3, 4, 5, 6, 7]. Remove 1. Promote 2 (from index 1) to index
0. Fill index 1 with the smaller of its children 4 and 5: the 4, from index 3.
Index 3 is a leaf, so the hole stops there. The list is now
[2, 4, 3, _, 5, 6, 7], with a hole at index 3 and a value still at index 6. The
tree is no longer complete. The arithmetic `2i + 1` now points at holes, and the
next insert, which goes at the end, makes it worse. The hole always ends at
whatever leaf the promotions lead to, which is almost never the last cell.

Moving the last element to the root first looks wasteful (it is probably large
and will sink straight back down), but it is the only move that keeps the shape,
and the shape is what makes the arithmetic legal.

### You might think: "When sifting down, swap with any child that is smaller."

Take the root 5 with children 1 and 2: the list [5, 1, 2]. Both children are
smaller than 5. Swap with the 2 and you get [2, 1, 5]: the 2 is now the parent of
the 1, and 2 > 1. The heap order is broken at a pair the operation was not even
looking at. Swap with the 1 and you get [1, 5, 2]: correct.

The reason is simple once said. Whatever moves up becomes the parent of **both**
children, so it must be no larger than both. Only the smaller child has that
property. This is the one line in the whole structure that cannot be paraphrased,
and it gets its own demonstration below.

### Step 6: building from a full list, in linear time

If you already have all n elements, you can push them one by one, at up to
log2 n steps each. There is a better way. Leaves are already valid heaps of one
element. So go through every **parent**, from the last parent back to the root,
and sift each one down. When you reach a node, both of its subtrees are already
valid heaps (they were finished earlier, because their indices are larger), so
one sift down makes the whole subtree valid.

The surprise, which we will count in "What it costs", is that this is O(n), not
O(n log n). Half the nodes are leaves and do nothing, a quarter can fall at most
one level, and only the root can fall the whole height.

### The technique in one sentence

**A binary heap keeps the elements in a complete binary tree stored as a list,
with every element no smaller than its parent; the minimum is therefore at index
0, and each change (append and sift up, or move the last to the root and sift
down into the smaller child) repairs only one root-to-leaf path, so it costs
O(log n).**

And the question that produced it: **what is the least the structure must know to
say who is next, and stay that way cheaply?** The answer is one fact per element,
"no smaller than my parent", instead of the order of every pair.

## Worked by hand

Get a pen. Start with an empty min-heap and push 5, 1, 8, 3, 2 in that order, then
pop twice. The "comparisons" column is every comparison actually made.

| step | operation | comparisons | list after |
|---|---|---|---|
| 1 | push 5 | none: it is the root | [5] |
| 2 | push 1 | 1 at index 1 vs parent 5 at index 0: smaller, swap | [1, 5] |
| 3 | push 8 | 8 at index 2 vs parent 1: not smaller, stop | [1, 5, 8] |
| 4 | push 3 | 3 at index 3 vs parent 5 (index 1): swap. 3 at index 1 vs 1: stop | [1, 3, 8, 5] |
| 5 | push 2 | 2 at index 4 vs parent 3 (index 1): swap. 2 at index 1 vs 1: stop | [1, 2, 8, 5, 3] |
| 6 | pop, returns 1 | last cell 3 to the root: [3, 2, 8, 5]. Children 2 and 8, smaller is 2; 3 > 2, swap. Now at index 1, child index 3 holds 5; 3 < 5, stop | [2, 3, 8, 5] |
| 7 | pop, returns 2 | last cell 5 to the root: [5, 3, 8]. Children 3 and 8, smaller is 3; 5 > 3, swap. Index 1 has no children | [3, 5, 8] |

Tell step 4 in words, the way you would at a whiteboard. "The heap is [1, 5, 8]
and 3 arrives. The next free cell is index 3, so 3 goes there. Its parent is
(3-1)//2 = 1, which holds 5. Is 3 smaller than 5? Yes, so the 5 is in the wrong
place above it: swap. Now 3 is at index 1, its parent is index 0, which holds 1.
Is 3 smaller than 1? No. Stop. Every other pair was never touched."

Tell step 6 in words. "I return the 1 at the root. The list must lose a cell, and
the only one it can lose is the last, so the 3 from index 4 moves to index 0 and
the list becomes [3, 2, 8, 5]. Now the root 3 has children at indices 1 and 2,
holding 2 and 8. The smaller is 2. Is 3 bigger than 2? Yes, so swap: [2, 3, 8, 5].
The 3 is now at index 1. Its children would be 3 and 4; only index 3 exists,
holding 5. Is 3 bigger than 5? No. Stop."

Four things in that trace are worth a second look, and none of them is visible in
the code.

**The 8 never moved.** It landed at index 2 in step 3 and is still there after
step 7. It is the largest value, one level below the root, and nobody cares,
because no question about it was ever asked. The heap does no work that a
question did not force.

**The list is never sorted, at any moment.** After step 5 it is [1, 2, 8, 5, 3].
If you ever write `heap[-1]` expecting the maximum, this is the counterexample:
the last cell holds 3.

**Push and pop are not the same price.** Going up, each level costs one
comparison (with the parent). Going down, each level costs two (first the
children against each other, then the winner against the sinking value). So a
pop costs about twice a push.

**The value that went to the root in step 6 came from the end of the list**, not
from a child. It is the only move that keeps the tree complete.

### The same idea on the picture: which child to sink into

Here is a pop drawn as trees, so you can point at the cells. The heap was
[1, 3, 2, 4, 5, 6]. The 1 has been returned and the last cell, 6, has moved to the
root, giving [6, 3, 2, 4, 5]: the left tree. Both children of the 6 are smaller
than it, so it must sink. The middle tree sinks it into the smaller child; the
right tree into the left child, which is the tempting shortcut.

<svg viewBox="0 0 760 300" role="img" aria-label="sifting down the root 6 in the list 6, 3, 2, 4, 5: swapping with the smaller child 2 gives a valid heap; swapping with the left child 3 puts 3 above 2 and breaks the order">
  <g>
    <circle class="fill" cx="120" cy="60" r="20"/>
    <text x="120" y="66" text-anchor="middle">6</text>
    <circle cx="70" cy="135" r="20"/>
    <text x="70" y="141" text-anchor="middle">3</text>
    <circle cx="170" cy="135" r="20"/>
    <text x="170" y="141" text-anchor="middle">2</text>
    <circle cx="40" cy="210" r="20"/>
    <text x="40" y="216" text-anchor="middle">4</text>
    <circle cx="100" cy="210" r="20"/>
    <text x="100" y="216" text-anchor="middle">5</text>
    <line x1="82" y1="118" x2="108" y2="77"/>
    <line x1="158" y1="118" x2="132" y2="77"/>
    <line x1="48" y1="192" x2="62" y2="153"/>
    <line x1="92" y1="192" x2="78" y2="153"/>
    <text x="110" y="265" text-anchor="middle">6 moved up from the end</text>
    <circle class="fill" cx="390" cy="60" r="20"/>
    <text x="390" y="66" text-anchor="middle">2</text>
    <circle cx="340" cy="135" r="20"/>
    <text x="340" y="141" text-anchor="middle">3</text>
    <circle cx="440" cy="135" r="20"/>
    <text x="440" y="141" text-anchor="middle">6</text>
    <circle cx="310" cy="210" r="20"/>
    <text x="310" y="216" text-anchor="middle">4</text>
    <circle cx="370" cy="210" r="20"/>
    <text x="370" y="216" text-anchor="middle">5</text>
    <line x1="352" y1="118" x2="378" y2="77"/>
    <line x1="428" y1="118" x2="402" y2="77"/>
    <line x1="318" y1="192" x2="332" y2="153"/>
    <line x1="362" y1="192" x2="348" y2="153"/>
    <text x="390" y="265" text-anchor="middle">into the smaller child: valid</text>
    <circle class="fill" cx="650" cy="60" r="20"/>
    <text x="650" y="66" text-anchor="middle">3</text>
    <circle cx="600" cy="135" r="20"/>
    <text x="600" y="141" text-anchor="middle">6</text>
    <circle cx="700" cy="135" r="20"/>
    <text x="700" y="141" text-anchor="middle">2</text>
    <circle cx="570" cy="210" r="20"/>
    <text x="570" y="216" text-anchor="middle">4</text>
    <circle cx="630" cy="210" r="20"/>
    <text x="630" y="216" text-anchor="middle">5</text>
    <line x1="612" y1="118" x2="638" y2="77"/>
    <line x1="688" y1="118" x2="662" y2="77" stroke-dasharray="5 4"/>
    <line x1="578" y1="192" x2="592" y2="153"/>
    <line x1="622" y1="192" x2="608" y2="153"/>
    <text x="650" y="265" text-anchor="middle">into the left child: 3 above 2</text>
    <text x="650" y="287" text-anchor="middle">the dashed edge is broken</text>
  </g>
</svg>

In the middle tree, the 2 that moved up is no larger than 3 (its new left child)
and no larger than 6 (the value it traded with). Every edge holds, and the 6 at
index 2 has no children, so the walk is over. In the right tree, the 3 that moved
up is fine against the 6, but it is now the parent of the 2, and 3 > 2. That edge,
dashed, is broken, and the sift will never come back to fix it, because it keeps
going down the left side. The next pop will return 3 while 2 is still in the heap.
We will run exactly this case in the code section.

### A second trace: the ropes, on the heap itself

Now the motivating problem, with the heap list shown after every operation. Start
with [4, 3, 2, 6] and heapify it: the only parent with children is index 1 (value
3, child 6, fine) and index 0 (value 4, children 3 and 2, smaller is 2, swap). The
heap is [2, 3, 4, 6].

| operation | what happens | heap after | cost so far |
|---|---|---|---|
| pop | returns 2; 6 to the root, children 3 and 4, swap with 3 | [3, 6, 4] | |
| pop | returns 3; 4 to the root, child 6, 4 < 6, stop | [4, 6] | |
| push 5 | 5 at index 2, parent 4, stop | [4, 6, 5] | 5 |
| pop | returns 4; 5 to the root, child 6, stop | [5, 6] | |
| pop | returns 5; 6 to the root, no children | [6] | |
| push 9 | 9 at index 1, parent 6, stop | [6, 9] | 14 |
| pop | returns 6 | [9] | |
| pop | returns 9 | [] | |
| push 15 | | [15] | 29 |

This trace shows something the first did not: the **pushed value was never one
of the inputs.** The 5 and the 9 did not exist when the heap was built, and each
landed somewhere in the middle of the order (5 is between 4 and 6). A sorted list
would have had to shift to admit them; the heap admitted each with one
comparison.

### A third trace: building in one pass

Take [5, 1, 8, 3, 2, 7] already in memory. There are 6 elements, so the parents
are indices 0, 1 and 2 (that is, up to 6//2 - 1 = 2). Sift down each, starting
from the last parent.

| i | value at i | its children | action | list after |
|---|---|---|---|---|
| 2 | 8 | index 5 only: 7 | 8 > 7, swap down | [5, 1, 7, 3, 2, 8] |
| 1 | 1 | 3 and 2, smaller is 2 | 1 is no larger, stop | [5, 1, 7, 3, 2, 8] |
| 0 | 5 | 1 and 7, smaller is 1 | 5 > 1, swap to index 1 | [1, 5, 7, 3, 2, 8] |
| (cont.) | 5 at index 1 | 3 and 2, smaller is 2 | 5 > 2, swap to index 4 | [1, 2, 7, 3, 5, 8] |

Three swaps for six elements. Indices 3, 4 and 5 were never touched as starting
points: they are leaves, and a single element is already a heap. That is the
whole reason bottom-up building is cheap.

## From the idea to the code

Here is the derivation as code: the two repairs, the two operations built from
them, and the bottom-up build. The block also replays the first hand trace and
asserts every list in the table, then checks 500 random lists against `sorted`.

```python run
import heapq
import random

def sift_up(a, i):
    while i > 0:
        p = (i - 1) // 2               # the parent of i
        if a[p] <= a[i]:               # parent no larger: the order holds, stop
            break
        a[p], a[i] = a[i], a[p]        # too small for this spot: trade with parent
        i = p

def sift_down(a, i, n):
    while True:
        c = 2 * i + 1                  # the left child
        if c >= n:                     # no children: a leaf, stop
            break
        if c + 1 < n and a[c + 1] < a[c]:
            c += 1                     # THE line: go to the SMALLER child
        if a[i] <= a[c]:               # no larger than both children: stop
            break
        a[i], a[c] = a[c], a[i]
        i = c

def push(a, x):
    a.append(x)                        # the only free cell that keeps the shape
    sift_up(a, len(a) - 1)

def pop(a):
    top = a[0]
    last = a.pop()                     # the only cell we can remove: the last one
    if a:
        a[0] = last                    # it fills the root's hole
        sift_down(a, 0, len(a))
    return top

def heapify(a):
    for i in range(len(a) // 2 - 1, -1, -1):   # every parent, last one first
        sift_down(a, i, len(a))

def is_heap(a):
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))

h, after = [], []
for x in [5, 1, 8, 3, 2]:
    push(h, x)
    after.append(list(h))
print("pushes 5,1,8,3,2:", after)
assert after == [[5], [1, 5], [1, 5, 8], [1, 3, 8, 5], [1, 2, 8, 5, 3]]
first = pop(h); print("pop ->", first, h)
assert first == 1 and h == [2, 3, 8, 5]
second = pop(h); print("pop ->", second, h)
assert second == 2 and h == [3, 5, 8]

rng = random.Random(7)
for _ in range(500):
    xs = [rng.randint(-30, 30) for _ in range(rng.randint(0, 20))]
    a = []
    for x in xs:
        push(a, x)
        assert is_heap(a)
    assert [pop(a) for _ in xs] == sorted(xs)       # draining a heap sorts
    b = list(xs)
    heapify(b)
    assert is_heap(b) and [pop(b) for _ in xs] == sorted(xs)
    c = list(xs)
    heapq.heapify(c)                                 # the library agrees on every pop
    assert [heapq.heappop(c) for _ in xs] == sorted(xs)
print("500 random lists: every push keeps the order, pops come out sorted, heapify works")
```

### Each line, and which part of the idea it is

| line | in words | which step of the derivation |
|---|---|---|
| `p = (i - 1) // 2` | where my parent lives | the index arithmetic of step 3 |
| `if a[p] <= a[i]: break` | my parent is no larger, so the only pair I could break is fine | the stopping rule of sift up |
| `a[p], a[i] = a[i], a[p]` | I am too small for this level; trade places with the parent | one level of the walk up |
| `c = 2 * i + 1` | my left child | arithmetic again |
| `if c >= n: break` | no children: I am a leaf, nothing below can be broken | sift down reached the bottom |
| `if c + 1 < n and a[c + 1] < a[c]: c += 1` | if a right child exists and is smaller, look at it instead | **the smaller-child rule** |
| `if a[i] <= a[c]: break` | I am no larger than the smaller child, so no larger than both | the stopping rule of sift down |
| `a.append(x)` then `sift_up` | the only cell that keeps the shape, then repair | step 4 |
| `last = a.pop()`, `a[0] = last`, `sift_down` | the only cell that can vanish, moved to the hole | step 5 |
| `range(len(a) // 2 - 1, -1, -1)` | every parent, the last one first | step 6 |

Settle three boring confusions now, so they never cost you a bug.

**Why `(i - 1) // 2` and not `i // 2`?** Because the root is at index 0. Some
books put the root at index 1, and then the parent is `i // 2` and the children
are `2i` and `2i + 1`. Both work. Mixing them does not: with root 0 and
`parent = i // 2`, index 2 would think its parent is index 1, its own sibling.

**Why does `pop` handle the one-element list separately?** Because `a.pop()`
removes the last cell, which is also the root. If the list is now empty there is
no hole to fill, and `a[0] = last` would crash. The `if a:` is that case.

**Why `len(a) // 2 - 1` in heapify?** The last cell is n - 1, and its parent is
(n - 2) // 2 = n // 2 - 1. Every index after that has no children, because its
left child 2i + 1 would be at least n.

### Python's heapq

In real code you use the standard library: `heapq.heappush(h, x)`,
`heapq.heappop(h)`, `heapq.heapify(h)`, and `h[0]` to peek. It is the same
structure on a plain list, written in C. Two more are worth knowing:
`heapq.heapreplace(h, x)` pops the minimum and pushes x in one sift down, and
`heapq.heappushpop(h, x)` pushes then pops, returning x immediately if it is
smaller than the root. Both save a walk.

`heapq` is a **min**-heap only. For a max-heap, push `-x` and negate on the way
out. For anything with a tie-break, push a tuple: Python compares tuples left to
right, so `(priority, arrival_index, item)` means "smallest priority first, then
earliest arrival", and the item is never compared because the index is unique.

### The subtle line, both ways

The one line that carries the structure is
`if c + 1 < n and a[c + 1] < a[c]: c += 1`: compare the two children first, and
sink into the smaller one. The common wrong version is to look at the left child
only, and swap whenever it beats the sinking value. It is shorter, it passes
small tests, and it is wrong.

Same input for both: the heap [1, 3, 2, 4, 5, 6]. Pop once.

Right (smaller child):

- The 1 leaves, the last cell 6 moves to the root: [6, 3, 2, 4, 5].
- Root 6, children 3 and 2. The smaller is 2, at index 2. 6 > 2, swap:
  [2, 3, 6, 4, 5].
- The 6 is at index 2, whose children would be 5 and 6: none exist. Stop.
- Valid heap. The next pop returns 2, the true minimum.

Wrong (left child only):

- Same start: [6, 3, 2, 4, 5].
- Root 6, left child 3. 6 > 3, swap: [3, 6, 2, 4, 5]. **This is the step that
  goes wrong.** The 3 is now the parent of the 2 at index 2, and 3 > 2.
- The 6 at index 1, left child 4 at index 3. 6 > 4, swap: [3, 4, 2, 6, 5].
- The list is not a heap. The next pop returns **3**, while 2 is still inside.

What the wrong version actually computes is "a list whose leftmost path is
sorted". The right subtree is never consulted, so any small value that happens to
sit on the right side is invisible to the root. The block below runs both and
asserts each list.

```python run
def sift_down(a, i, rule, log):
    n = len(a)
    while True:
        c = 2 * i + 1
        if c >= n:
            break
        if rule == "smaller child" and c + 1 < n and a[c + 1] < a[c]:
            c += 1                      # right: compare the children first
        # rule == "left child": take the left child whenever it beats a[i]
        if a[i] <= a[c]:
            break
        a[i], a[c] = a[c], a[i]
        log.append("swap %d<->%d  %s" % (i, c, a))
        i = c

def pop(a, rule, log):
    top, last = a[0], a.pop()
    if a:
        a[0] = last
        log.append("last to root %s" % a)
        sift_down(a, 0, rule, log)
    return top

def is_heap(a):
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))

for rule in ("smaller child", "left child"):
    a, log = [1, 3, 2, 4, 5, 6], []
    first = pop(a, rule, log)
    ok = is_heap(a)
    second = pop(a, rule, [])
    print("%-13s pop %d: %s" % (rule, first, " | ".join(log)))
    print("%-13s heap after? %s   next pop returns %d" % ("", ok, second))
    if rule == "smaller child":
        assert ok and second == 2
    else:
        assert not ok and second == 3       # 2 was still inside, at index 2

# the smallest possible witness: three cells
a = [5, 2, 1]
sift_down(a, 0, "left child", [])
print("left-child rule on [5, 2, 1] gives", a, "-> heap?", is_heap(a))
assert a == [2, 5, 1] and not is_heap(a)
```

The three-cell witness [5, 2, 1] is worth keeping in your head: the left child
2 beats 5, so the wrong rule swaps, and 2 ends up above 1. If a sift down you
wrote ever gets this case wrong, it is the smaller-child line.

### Max-heaps, and the build the problem dictates

Some problems spell out the exact procedure because they grade the list itself.
[[p:rippling-build-max-heap|Build a Max Heap]] asks for the list after bottom-up
construction with a max-heap, and fixes the tie rule: swap with the larger child
only when it is strictly greater, and prefer the left child when the two are
equal. [[p:goldman-sachs-heap-insertion|Insert into a Min-Heap]] says "swap with
its parent while it is strictly smaller... equal values do not swap". With `<=`
in place of `<` you still get a valid heap, but a different list, and the grader
compares lists. When a problem returns the heap's contents, the comparison
operator is part of the specification.

## Why it is correct

A data structure is correct when every operation keeps its invariant true, and
the invariant implies the answer it reports. Here the invariant is the heap
order, and the answer is "the minimum is at index 0".

:::proof Every operation keeps the heap order, so a[0] is always the minimum
**The invariant (H).** For every index i from 1 to n - 1, `a[parent(i)] <= a[i]`.
The shape is automatic: the elements occupy indices 0 to n - 1 with no gaps,
because we only ever append at the end and remove from the end.

**Why (H) gives the minimum at the root.** Take any index i. Follow parents from
i up to 0. Each step goes to a value no larger than the one before, by (H). So
`a[0] <= a[i]`. Since i was arbitrary, a[0] is the minimum. Nothing is claimed
about siblings or about which leaf is largest.

**Base case.** A list of 0 or 1 elements has no parent-child pairs, so (H) holds.

**Push.** Append x at index m = n. Every old pair is untouched, so at most the
new pair (parent(m), m) is broken. Now follow x up. At each moment x sits at some
index i, and two things are true:

- (a) every pair is fine except possibly (parent(i), i), the one just above x;
- (b) if i has a parent p, then a[p] is no larger than each child of i. (Think of
  it as "my grandchildren are fine with my parent".)

At the start, i = m is a fresh leaf with no children, so (b) says nothing, and (a)
is what we just argued.

If `a[parent(i)] <= x`, the one doubtful pair is fine, so (H) holds everywhere;
stop. Otherwise let p = parent(i) and w = a[p], so w > x. Swap: now x is at p and
w is at i. Check every pair that changed:

- (p, i): x above w, and x < w. Fine.
- (p, s), where s is the sibling of i: before the swap w <= a[s] by (H), and
  x < w, so x <= a[s]. Fine.
- (i, c) for each child c of i: w is now above c. Fact (b) said exactly that the
  old a[p], which is w, is no larger than each child of i. Fine. **This is where
  (b) earns its place.**
- (parent(p), p): the new doubtful pair, just above x. That is (a) at p.

And (b) at p: the children of p are now i (holding w) and s. Let g = parent(p).
Before the swap the pair (g, p) was fine, so a[g] <= w, and w <= a[s]. So a[g] is
no larger than either child of p.

Each swap moves x up one level, so the walk ends, at the stop test or at the root,
which has no parent and so no doubtful pair. (H) holds.

**Pop.** Return a[0], which is the minimum by the claim above. Move the last
element x to index 0 and shrink. Now the only pairs that can be broken are
(0, c) for the children c of the root. Follow x down: at each moment x is at some
index i, and the only pairs that can be broken are (i, c) for the children of i.
Call this "bad pairs only below x". Also, the parent of i (if any) is no larger
than every child of i; this holds at the start because i = 0 has no parent, and
we keep it below.

If i has no children, nothing is bad; stop. Otherwise let m be the child with the
**smaller** value v. If x <= v, then x <= both children, nothing is bad; stop.
Otherwise swap x and v. Check every pair that changed:

- (parent(i), i): now v is at i. By the extra fact, the parent of i is no larger
  than every child of i, including v. Fine.
- (i, o), where o is the other child: v <= a[o] **because m was the smaller
  child**. This is the only place the word "smaller" is used, and the proof (and
  the code) fails without it.
- (i, m): v above x, and v < x. Fine.
- (m, c) for the children of m: the new possibly bad pairs, below x. And the extra
  fact holds at m: its parent is now v, and v <= a[c] for m's children because
  that was (H) before the swap.

Each swap moves x down a level, so the walk ends at a leaf or at the stop test.
(H) holds.

**Heapify.** Process i from n//2 - 1 down to 0, sifting each down. Claim: when we
reach i, both subtrees of i already satisfy (H). True at the start, because every
index above n//2 - 1 is a leaf. True at each later step, because the children of
i have larger indices and were finished earlier. Sifting down at i is exactly the
pop argument applied to the subtree at i (a root that may be too big, sitting on
two valid heaps), so the subtree at i satisfies (H) afterwards. At i = 0 the whole
list does.
:::

Now say plainly what the proof leaned on, because that list is where the bugs
come from.

- **A comparison that is consistent.** The minimum argument chained `<=` from a
  leaf to the root, which needs transitivity. Floats that may be NaN, or a
  comparator that changes its mind, make the heap return the wrong element with
  no error.
- **Keys do not change while stored.** If you push an object and then modify the
  field it is ordered by, nothing repairs the heap. A later pop is not the
  minimum.
- **Only the ends are edited.** The shape held because we appended at the end and
  removed the end. `del h[i]` or `h.remove(x)` renumbers every later cell and
  destroys the tree. (If you must, re-heapify afterwards, at O(n).)
- **The smaller child.** Used exactly once, and the operation is wrong without it.
- **Nothing about siblings, or about `h[-1]`.** The proof never ordered siblings.
  The only extra fact you get for free: every parent is no larger than its
  children, so the maximum of a min-heap is always a leaf, somewhere in indices
  n//2 to n - 1. A range of n/2 cells, not a position.
- **Ties are not ordered.** Equal keys come out in whatever order the swaps left
  them. A heap is not stable. If the problem has a tie rule, it must be in the key.

## What it costs

Everything follows from the height. A complete binary tree with n nodes has every
level full except the last. Level 0 has 1 node, level 1 has 2, level k has 2^k.
If the tree has height h (levels 0 to h), the first h levels alone hold
2^h - 1 nodes and the last level at least one more, so n >= 2^h and
h <= log2 n. For n = 10^5, h = 16.

**Push**: sift up does at most h iterations, one comparison each. O(log n).

**Pop**: sift down does at most h iterations, two comparisons each. O(log n),
about twice a push.

**Peek** (`h[0]`): O(1).

**Heapify, bottom-up: O(n), not O(n log n).** Do not guess this; count it. A node
at height j (j levels above the leaves) can fall at most j levels. About n/2
nodes are leaves (height 0), about n/4 have height 1, n/8 have height 2, and so on.
The total number of moves is at most

```text
(n/4)*1 + (n/8)*2 + (n/16)*3 + ...  =  (n/2) * (1/2 + 2/4 + 3/8 + ...)  =  (n/2) * 2  =  n
```

using the series 1/2 + 2/4 + 3/8 + ... = 2. Fewer than one move per element.

**Building by n pushes is O(n log n).** The i-th push can climb log2 i levels,
and on an increasing input into a max-heap (or a decreasing one into a min-heap)
every push climbs all the way. The total is log2 1 + log2 2 + ... + log2 n =
log2(n!), which is about n log2 n.

Why the difference, when both build the same kind of object? A push's cost is the
node's **depth** (distance to the root), and most nodes are deep. A sift down's
cost is the node's **height** (distance to the leaves), and most nodes are short.
The block below counts comparisons for both and for heapsort.

```python run
CMPS = [0]


def sift_down_max(a, i, n):
    x = a[i]
    while True:
        c = 2 * i + 1
        if c >= n:
            break
        if c + 1 < n:
            CMPS[0] += 1
            if a[c + 1] > a[c]:
                c += 1
        CMPS[0] += 1
        if x >= a[c]:
            break
        a[i] = a[c]
        i = c
    a[i] = x


def heapsort(xs):
    a, n = list(xs), len(xs)
    for i in range(n // 2 - 1, -1, -1):          # linear build
        sift_down_max(a, i, n)
    build = CMPS[0]
    for end in range(n - 1, 0, -1):              # n-1 extractions
        a[0], a[end] = a[end], a[0]
        sift_down_max(a, 0, end)
    return a, build


def build_by_push(xs):
    a = []
    for x in xs:
        a.append(x)
        i = len(a) - 1
        while i > 0:
            p = (i - 1) >> 1
            CMPS[0] += 1
            if a[p] >= a[i]:
                break
            a[i], a[p] = a[p], a[i]
            i = p
    return a


print("%8s %12s %7s %14s %7s" % ("n", "heapify", "/n", "n pushes", "/n"))
for n in (1000, 4000, 16000):
    xs = list(range(n))                          # worst case for max-heap pushes
    CMPS[0] = 0
    _, build = heapsort(xs)
    CMPS[0] = 0
    build_by_push(xs)
    pushes = CMPS[0]
    print("%8d %12d %7.2f %14d %7.2f" % (n, build, build / n, pushes, pushes / n))
    assert build < 3 * n, "bottom-up heapify must stay linear"
    assert pushes > 4 * n, "repeated pushing must not"

import math
import random
rng = random.Random(3)
data = [rng.randrange(1000) for _ in range(400)]
CMPS[0] = 0
out, _ = heapsort(data)
assert out == sorted(data)
bound = 2 * 400 * math.log2(400)                 # two comparisons per level per pop
print("heapsort of 400 ints matches sorted(); comparisons =", CMPS[0],
      " 2*n*log2(n) =", int(bound))
assert CMPS[0] < bound
```

The "/n" column for heapify stays flat at 2.0 as n grows sixteenfold; the push
column grows with log2 n. (The block counts comparisons, and a sift down spends
two per level, so "fewer than one move per element" shows up here as "fewer than
two comparisons per element".)

**A heap of size k.** When you only keep the k best of n elements, every push and
pop is on a heap of size k, so the whole run is O(n log k) time and O(k) space.
For k = 10 and n = 2 x 10^5, that is log2 10 = 3.3 steps per element against
log2(2 x 10^5) = 17.6 for sorting everything, and ten records in memory instead of
200,000. That is the whole point of [[p:citadel-top-ten-trades-by-notional|Top Ten Trades by Notional Value]].

**The hidden costs.**

- **The comparison is O(1) only if the key is.** Push `(priority, name)` and
  equal priorities fall through to comparing names, character by character. A key
  that is a class with `__lt__` is an interpreted call on every comparison.
- **The number of rounds, not the heap.** A simulation that pops and pushes once
  per step costs O(m log n) for m steps. If m is 10^9, the heap is not the
  bottleneck; the loop is. [[p:amazon-sum-max-plus-min-after-decrement-operations|Sum Max Plus Min After Decrement Operations]]
  starts as a pop-max, push-max-minus-one loop, but its request count is too large
  to simulate one step at a time, and you have to batch equal values with
  arithmetic.
- **Sorting at the start.** Many heap solutions sort the input by time first
  (events, tasks, trips). That O(n log n) is usually the largest term.

## How to think about it

Before writing any code on a new problem, answer these, in order.

1. **What is "next"?** Name the key in words: the shortest rope, the earliest end
   time, the largest notional, the smallest head among k lists. If you cannot say
   what is next, you do not have a heap problem yet.
2. **Does the set change between questions?** If nothing is ever added after the
   start, and you only take from the front, sorting is enough. A heap is for
   "take one, then something new arrives or something comes back".
3. **What goes back in after a pop?** The joined rope, the stone's remainder, the
   same item type at its next price, the next element of the same list, the same
   server at its new free time. Most heap problems are this loop: pop the best,
   change it, push it back.
4. **Min or max: what do I want to throw away?** The root is the only element you
   can reach. Put at the root what you will remove next. For the k largest, you
   remove the weakest survivor, so the root is the smallest: a **min**-heap. That
   feels backwards, which is why it is the most common heap bug.
5. **What is the full ordering rule, including ties?** Write the tuple:
   `(key, tie_break, unique_id)`. Ties must be in the key, because the heap does
   not remember insertion order.
6. **How big does the heap need to be?** All n elements, k of them, one per
   stream, or only the currently active ones? The size decides the log.
7. **Do I need to remove something that is not the root?** Then plan lazy
   deletion (push the new version, skip stale entries when they surface), or use
   a different structure.

### Telling it from its neighbours

- **Sorting.** If the order is fixed after the first look, sort. A heap is a sort
  that you can interleave with insertions.
- **Quickselect.** One question ("the k-th largest") on a fixed array: expected
  O(n), no heap. [[p:cognizant-kth-largest-element|Kth Largest Element in an Array]]
  is solvable both ways.
- **Ordered set / balanced BST.** If you need the minimum and the maximum, or the
  predecessor of x, or to delete arbitrary values, a heap is the wrong
  abstraction. A sorted container does all of these in O(log n).
- **Monotonic deque.** The extreme of a sliding window. Elements leave in arrival
  order, which a deque handles in O(1).
- **Buckets.** If keys are small integers (frequencies up to n, ages 0 to 120), an
  array of buckets gives the extreme with no comparisons at all. Top k frequent can
  be done with buckets in O(n).
- **Greedy.** Many heap problems are greedy algorithms, and the heap is only how
  you find the greedy choice fast. Proving the greedy is right is a separate job
  ([[greedy-exchange]]).

## Variations

Every heap problem in an interview or an OA is one of these. Each says what
changes, why, a tiny example, and a problem from the bank that teaches it.

### A. Top k with a heap of size k

**What changes.** The heap never holds more than k elements. For the k largest,
keep a min-heap: when a new element beats the root, replace the root.

**Why.** The root is the weakest of the current top k, the one that would be
pushed out first. Every element smaller than it can never be in the answer, so it
is discarded with one comparison.

**Example.** nums = [7, 2, 9, 4, 9, 1, 8], k = 3. The heap goes [7], [2, 7],
[2, 7, 9], then 4 beats the root 2: [4, 7, 9]; 9 beats 4: [7, 9, 9]; 1 does not
beat 7; 8 beats 7: [8, 9, 9]. The root, 8, is the third largest.

**In the bank.** [[p:cognizant-kth-largest-element|Kth Largest Element in an Array]]
is exactly this, with the answer at the root.
[[p:ericsson-top-k-frequent-elements|Top K Frequent Elements]] counts first, then
keeps a size-k heap keyed by frequency, and its tie rule ("the smaller value comes
first") must be in the tuple, with the polarity right: the root must be the worst
candidate, the lowest frequency and, among equals, the larger value.
[[p:uber-top-k-using-priority-queue|Top-K Using a Priority Queue]] states the
expected O(n log k) in the statement.

### B. Repeatedly take the best and push back the rest (simulate)

**What changes.** Nothing in the heap. The work is in seeing that the problem is
a loop of "pop the extreme, transform it, push the result back".

**Why a heap and not one sort.** The pushed-back value is new, and its position in
the order depends on what happened before. That is exactly the [1, 1, 1, 1] ropes
counterexample.

**Example.** Chocolates of weight [30, 20, 25], d = 4 days, each day eat half of
one (rounding the eaten part down) to minimise the remaining total. Max-heap: eat
from 30 (15 left), then 25 (13 left), then 20 (10 left), then 15 (8 left). Remaining
8 + 10 + 13 = 31.

**In the bank.** This is the largest family.

- [[p:inmobi-connect-n-ropes-minimum-cost|Connect N Ropes With Minimum Cost]]: pop
  two, push their sum. (It is also Huffman coding: [[huffman]].)
- [[p:snowflake-find-min-weight|Minimum Total Weight]]: the chocolates above.
  Always halve the current heaviest.
- [[p:ibm-get-maximum-amount|Get Maximum Amount]]: each sale takes the type with
  the most stock and pushes it back with one less.
- [[p:get-minimum-cost|Get Minimum Cost]]: buy the globally cheapest next unit m
  times; popping a type pushes back the same type at its next price.
- [[p:amazon-package-delivery-system|Package Delivery System]]: the heaviest package
  goes to the truck with the most capacity, and that truck's halved capacity goes
  back into the heap.
- [[p:amazon-reorganize-string|Reorganize a String]]: most frequent letter first,
  but the letter you just placed is held out for one step and pushed back after
  the next placement. A heap with a one-step cooldown.
- [[p:uber-minimum-refueling-stops|Minimum Refueling Stops]] (stretch): decide
  late. Drive as far as you can, keeping every station you passed in a max-heap of
  fuel, and only when you are stuck, pop the best one and count a stop.
- [[p:amazon-sum-max-plus-min-after-decrement-operations|Sum Max Plus Min After Decrement Operations]]
  (stretch): the loop is clear, but the number of steps is too large, so the
  simulation must be batched.

### C. Merge k sorted lists

**What changes.** The heap holds one element per list: the current head. Each
entry is `(value, list_id, position)`.

**Why.** The next output is the smallest of the k heads. After it is taken, only
that list's head changes, so you push that list's next element. The heap never
holds more than k entries, so each step is O(log k), and N total elements cost
O(N log k).

**Example.** [1, 4, 7], [2, 5], [3, 6, 9]. Heap of heads (1, 2, 3). Pop 1, push 4:
heads (2, 3, 4). Pop 2, push 5. Pop 3, push 6. Pop 4, push 7. Pop 5 (list 2 is
now empty, push nothing). Pop 6, push 9. Pop 7, pop 9. Output
1 2 3 4 5 6 7 9.

**In the bank.** [[p:the-walt-disney-company-merge-k-sorted-lists|Merge K Sorted Linked Lists]],
and [[p:meta-merge-three-sorted-arrays|Merge Three Sorted Arrays]] (which also
drops duplicates: compare with the last value written). The general pattern has
its own chapter: [[k-way-merge]].

### D. Two heaps for a running median

**What changes.** Two heaps facing each other. A max-heap holds the smaller half,
a min-heap the larger half, and their sizes differ by at most one.

**Why.** The median is the boundary between the halves, and each heap's root is
exactly one side of that boundary. Each add is a push and at most one move
between the heaps.

**Example.** Add 5: low [5], median 5. Add 15: it is above 5, goes high [15];
median (5 + 15) / 2 = 10. Add 1: low [5, 1], high [15]; median 5. Add 3: low gets
it, [5, 3, 1], too big, move 5 to high: low [3, 1], high [5, 15]; median
(3 + 5) / 2 = 4.

**In the bank.** [[p:intuit-find-median-from-data-stream|Find Median from Data Stream]].
The topic has its own chapter: [[median-maintenance]]. The sliding-window version
([[p:bloomberg-sliding-window-median|Sliding Window Median]]) also needs lazy
deletion (variation F), because elements leave the window from the middle of the
heaps.

### E. A heap of events or end times (scheduling)

**What changes.** Sort the jobs by start time. The heap holds the **end times**
of whatever is currently running (or the free times of servers). Before each new
start, pop everything that has ended.

**Why.** The only running thing that could have finished by the next start is the
one that ends earliest. The set of running things changes at every step, which is
the heap trigger.

**Example.** Meetings (0, 30), (5, 10), (15, 20). At 0: heap [30], size 1. At 5:
30 has not ended, push 10, heap [10, 30], size 2. At 15: 10 has ended, pop it;
push 20, heap [20, 30], size 2. The largest size seen is 2 rooms.

**In the bank.** [[p:snowflake-minimum-station-bus-fleet|Minimum Bus Fleet Across Stations]]
is this with one heap per station: a bus that finished at the origin by the
departure time can be reused, otherwise a new bus is needed.
[[p:amazon-meeting-rooms-ii|Meeting Rooms II]] and
[[p:google-meeting-rooms-ii|Minimum Number of Chairs]] are the plain version.
[[p:roblox-single-threaded-cpu|Single-Threaded CPU]] uses two orders at once: tasks
sorted by arrival, and a heap of available tasks keyed by (processing time,
index). See also [[scheduling]] and [[intervals]].

### F. Lazy deletion

**What changes.** You never remove an element from the middle. When an element
becomes invalid (its value changed, or it left a window), you leave it in the heap
and record that it is stale. When a stale entry reaches the root, you pop and
discard it.

**Why.** Every entry is pushed once and popped once, so the total cost stays
O(log n) per operation. The heap may be larger than the live set, but never larger
than the number of pushes.

**Example.** Dijkstra's algorithm pushes (distance, node) whenever it finds a
shorter path, and on pop writes `if d > dist[node]: continue`. The old, longer
entries are discarded when they surface. See [[dijkstra]].

**Rare in this bank** outside shortest paths and sliding-window medians. The
alternative is an **indexed heap** that tracks each item's position and supports
"decrease key"; you will almost never need to write one.

### G. Heapify and heapsort

**What changes.** No priority queue at all: the heap is a tool for sorting in
place.

**How.** Build a **max**-heap in place (bottom-up, O(n)). Then repeat: swap the
root (the largest) with the last cell of the heap part, shrink the heap part by
one, and sift the new root down within the shrunken part. The sorted part grows
from the back.

**Example.** [3, 1, 2]: heapify to [3, 1, 2]. Swap root and last: [2, 1, 3], heap
part [2, 1]; sift down: fine. Swap: [1, 2, 3]. Sorted.

**Why it matters.** O(n log n) in the worst case, O(1) extra memory. Quicksort's
worst case is O(n^2); merge sort needs O(n) extra memory. Heapsort is the
guarantee that library sorts fall back to. Its weaknesses are poor cache behaviour
and instability ([[sorting]]).

**In the bank.** [[p:rippling-build-max-heap|Build a Max Heap]] grades the exact
list after bottom-up construction, with the tie rule fixed.
[[p:rippling-validate-max-heap|Validate a Max Heap]] checks both halves of the
definition: the tree must be **complete** (fill level by level, left to right, no
gaps) and every parent must be at least its children. Most wrong answers check
only the order. [[p:goldman-sachs-heap-insertion|Insert into a Min-Heap]] grades a
single sift up.

### H. d-ary heaps (rare)

Each node has d children. The height drops to log_d n, so pushes are cheaper; pops
compare d children per level, so they cost more. Used when pushes dominate (some
Dijkstra implementations). You will not need it in an interview, but you may be
asked why one would choose d = 4.

The block below runs variations A to E on the small examples above and checks the
median and the merge against `statistics.median` and `sorted` on random inputs.

```python run
import heapq
from collections import Counter
import random, statistics

def running_medians(stream):
    low, high, out = [], [], []          # low: max-heap (negated), high: min-heap
    for x in stream:
        if low and x > -low[0]:
            heapq.heappush(high, x)
        else:
            heapq.heappush(low, -x)
        if len(low) > len(high) + 1:     # rebalance: low may hold one extra
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
        out.append(-low[0] if len(low) > len(high) else (-low[0] + high[0]) / 2)
    return out

def merge_k(lists):
    h = [(xs[0], j, 0) for j, xs in enumerate(lists) if xs]   # one head per list
    heapq.heapify(h)
    out = []
    while h:
        v, j, i = heapq.heappop(h)
        out.append(v)
        if i + 1 < len(lists[j]):
            heapq.heappush(h, (lists[j][i + 1], j, i + 1))     # that list's next
    return out

def rooms(meetings):
    ends, best = [], 0                   # end times of meetings now running
    for s, e in sorted(meetings):
        while ends and ends[0] <= s:     # those rooms are free again
            heapq.heappop(ends)
        heapq.heappush(ends, e)
        best = max(best, len(ends))
    return best

def top_k_frequent(nums, k):
    h = []
    for v, f in Counter(nums).items():
        heapq.heappush(h, (f, -v))       # the root is the WORST: lowest f, then largest v
        if len(h) > k:
            heapq.heappop(h)
    return [-nv for f, nv in sorted(h, key=lambda t: (-t[0], -t[1]))]

print("medians of 5 15 1 3 :", running_medians([5, 15, 1, 3]))
assert running_medians([5, 15, 1, 3]) == [5, 10.0, 5, 4.0]
print("merge [1,4,7] [2,5] [3,6,9]:", merge_k([[1, 4, 7], [2, 5], [3, 6, 9]]))
assert merge_k([[1, 4, 7], [2, 5], [3, 6, 9]]) == [1, 2, 3, 4, 5, 6, 7, 9]
print("rooms for (0,30) (5,10) (15,20):", rooms([(0, 30), (5, 10), (15, 20)]))
assert rooms([(0, 30), (5, 10), (15, 20)]) == 2
print("top 2 frequent of 1 1 1 2 2 3 3:", top_k_frequent([1, 1, 1, 2, 2, 3, 3], 2))
assert top_k_frequent([1, 1, 1, 2, 2, 3, 3], 2) == [1, 2]   # 2 and 3 tie; smaller wins

rng = random.Random(3)
for _ in range(200):
    xs = [rng.randint(-50, 50) for _ in range(rng.randint(1, 30))]
    assert running_medians(xs) == [statistics.median(xs[:i + 1]) for i in range(len(xs))]
    ls = [sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 6))) for _ in range(4)]
    assert merge_k(ls) == sorted(sum(ls, []))
print("200 random cases agree with statistics.median and sorted()")
```

## Recognising it in a statement

Ordered by how much you should trust the signal.

1. **"Repeatedly take the largest (or smallest), then put something back."** A
   loop whose body both removes an extreme and inserts a new value. Smash the two
   heaviest stones and put back the difference
   ([[p:factset-last-stone-weight|Last Stone Weight]]); join the two shortest
   ropes; halve the heaviest chocolate.
2. **A stated O(n log k), or a memory bound of O(k).** When a statement names the
   complexity, it has named the structure. "A heap that retains at most ten
   candidates" is a direct instruction.
3. **"The next to become free", "the least loaded", "the earliest deadline", "the
   cheapest available".** A superlative over a set that is mutated as you go.
4. **"The minimum number of rooms / buses / machines / chairs at the same time."**
   A sweep in start order with a heap of end times; the answer is the heap's
   largest size.
5. **A stream, or "after each operation, report..."** You cannot re-sort after
   every event, and you may not be able to store the whole input.
6. **Several sorted inputs, one sorted output.** k-way merge.
7. **An explicit tie-break inside a process.** "If several are available, pick the
   one with the smallest processing time, then the smallest index." That is a
   tuple key in a heap.

### Disguises

- **"Minimum cost to combine everything", where combining creates a new item.**
  Ropes, files, sticks, Huffman. The cost of a combination depends on items that
  did not exist at the start, so it is a heap, not a sort.
- **"Decide later" greedy.** "You may refuel at stations you have passed." Keep the
  options you skipped in a heap, and take the best one only when you are forced.
  The same shape appears in "the most courses you can take before their
  deadlines": keep the courses taken in a max-heap of durations, and when the
  deadline is exceeded, drop the longest.
- **"Buy m items, each type gets more expensive as you buy it."** Each type is a
  sorted stream of prices, so this is a k-way merge where you stop after m pops.

### Anti-signals: looks like a heap, is not

- **The set never changes and there is one question.** Sort, or quickselect.
- **"How many are less than x", "the element of rank r", "the next value above x".**
  [[ordered-set]], [[fenwick-tree]], or a sorted list with [[binary-search]].
- **"Remove this particular element"** as a frequent operation.
- **A sliding window maximum.** [[monotonic-deque]] in O(n).
- **"Return the elements sorted."** A heap does not hold sorted data. Draining it
  does, and that is heapsort, which `sorted()` beats in practice.
- **"The two largest" once, from a fixed array.** Two variables and one pass.

## Traps

**Wrong polarity for top k.** For the k **largest**, keep a **min**-heap, so the
weakest survivor is at the root and is what you evict. With a max-heap capped at
k, each eviction throws away the largest seen so far, and you end with the k
smallest. Symptom: the answer is the k smallest, and tests where k = n still pass.

**A tie reaches a payload that cannot be compared.** `(priority, some_dict)` works
until two priorities are equal; then Python compares the dicts and raises
`TypeError`. Symptom: a crash on some inputs, never on the samples. Fix: put a
unique, comparable tie-breaker (an index or a counter) between the key and the
payload.

**Reading `h[-1]` as the maximum, or `h[:k]` as the k smallest.** Only `h[0]` has
a meaning. Symptom: correct on inputs of size 1 to 3, wrong beyond.

**Forgetting to negate back** after using `-x` for a max-heap. Symptom: negative
answers, or the right answer with the wrong sign.

**Mutating a key already in the heap, or `h.remove(x)` without re-heapifying.**
Symptom: silently wrong pops, no exception.

**Pushing everything, then popping k.** O(n log n) time and O(n) memory when the
statement wanted O(n log k) and O(k). Symptom: passes small tests, then times out
or runs out of memory on the largest one.

**Peeking or popping an empty heap.** Guard with `if h:`. In a simulation loop
this fires on the very last iteration, or when the input is empty.

**`<=` where the statement says `<`.** When the grader compares the list itself,
an equal-value swap gives a valid heap with the wrong layout. Your own "is it a
heap" checker passes; the grader does not.

**Simulating 10^9 steps.** The heap makes each step O(log n), but 10^9 steps are
still too many. Look for batches of identical steps.

The block below demonstrates the first three.

```python run
import heapq

nums = [7, 2, 9, 4, 9, 1, 8]
k = 3


def top_k_right(nums, k):
    h = []                                   # MIN-heap holding the k largest
    for x in nums:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)          # one sift_down, not a pop plus a push
    return sorted(h, reverse=True)


def top_k_wrong(nums, k):
    h = []                                   # MAX-heap, capped at k
    for x in nums:
        heapq.heappush(h, -x)
        if len(h) > k:
            heapq.heappop(h)                 # evicts the LARGEST seen so far
    return sorted((-v for v in h), reverse=True)


print("nums                         ", nums)
print("k largest, min-heap of size k:", top_k_right(nums, k))
print("k largest, max-heap of size k:", top_k_wrong(nums, k), "<- the k smallest")
assert top_k_right(nums, k) == [9, 9, 8]
assert top_k_wrong(nums, k) == [4, 2, 1]

h = [5, 1, 8, 3, 2]
heapq.heapify(h)
print("heapified                    ", h, " h[-1] =", h[-1], " max =", max(h))
assert h[0] == min(h) and h != sorted(h)

tasks = [(2, {"id": "a"}), (2, {"id": "c"}), (1, {"id": "b"})]
try:
    bad = []
    for pr, payload in tasks:
        heapq.heappush(bad, (pr, payload))
    print("no error raised")
except TypeError as e:
    print("pushing (priority, dict):     TypeError:", e)

good = []
for seq, (pr, payload) in enumerate(tasks):
    heapq.heappush(good, (pr, seq, payload))   # seq is unique: ties stop here
order = [heapq.heappop(good)[2]["id"] for _ in range(len(good))]
print("with a sequence tiebreak:     ", order)
assert order == ["b", "a", "c"]
```

## What to memorise

The arithmetic, the two repairs, and one sentence.

```text
parent(i) = (i - 1) // 2      left(i) = 2i + 1      right(i) = 2i + 2
push:    append, then walk up while smaller than the parent
pop:     take a[0], move the last cell to 0, walk down into the SMALLER child
heapify: sift down every index from n//2 - 1 back to 0     (O(n))
```

**The sentence** that turns a problem into a heap: *"Do I keep needing the
extreme of a set that keeps changing?"* If the set is static, sort. If the
question is about rank, not the extreme, it is not a heap.

**The habit.** Write the entry as a tuple that is exactly the ordering rule, read
left to right, ending in something unique: `(-notional, arrival_index, trade_id)`
says "largest notional first, ties to whoever came first", and never falls
through to the payload. Decide min or max by asking *what will I throw away
next?*, and put that at the root.

Numbers: log2(10^5) is about 17, log2(10^6) about 20. Push and pop O(log n), pop
about twice a push, peek O(1), heapify O(n), heapsort O(n log n) in place, a
size-k heap over n items O(n log k) time and O(k) space.

## Check yourself

:::check
Hand trace. Push 7, 3, 9, 1, 5, 4 into an empty min-heap, writing the list after
each push and every swap. Then pop twice, writing the list after each pop.
--
| operation | swaps | list after |
|---|---|---|
| push 7 | none | [7] |
| push 3 | 3 (index 1) vs parent 7: swap | [3, 7] |
| push 9 | 9 vs parent 3: stop | [3, 7, 9] |
| push 1 | 1 (index 3) vs parent 7 (index 1): swap; vs 3 (index 0): swap | [1, 3, 9, 7] |
| push 5 | 5 (index 4) vs parent 3 (index 1): stop | [1, 3, 9, 7, 5] |
| push 4 | 4 (index 5) vs parent 9 (index 2): swap; vs 1: stop | [1, 3, 4, 7, 5, 9] |

Pop returns 1. The last cell 9 moves to the root: [9, 3, 4, 7, 5]. Children 3 and
4, smaller is 3: swap, [3, 9, 4, 7, 5]. The 9 at index 1 has children 7 and 5,
smaller is 5: swap, [3, 5, 4, 7, 9]. Index 4 is a leaf. Result [3, 5, 4, 7, 9].

Pop returns 3. The last cell 9 moves to the root: [9, 5, 4, 7]. Children 5 and 4,
smaller is 4: swap, [4, 5, 9, 7]. Index 2 has no children (its left child would be
index 5). Result [4, 5, 9, 7].

Note that in the first pop the 9 went down the left side and then the right side:
the path is chosen by the smaller child at every level, not fixed in advance.
:::

:::check
Hand trace. Heapify [9, 4, 7, 1, 8, 2] into a min-heap bottom-up. Which indices do
you start from, and how many swaps are there in total? Then build a **max**-heap
from [3, 9, 2, 1, 4, 5] the same way.
--
Six elements, so the parents are indices 2, 1, 0 (from 6//2 - 1 = 2 down).

- i = 2, value 7, only child index 5 holds 2: swap. [9, 4, 2, 1, 8, 7].
- i = 1, value 4, children 1 and 8, smaller is 1: swap. [9, 1, 2, 4, 8, 7]. Index
  3 is a leaf.
- i = 0, value 9, children 1 and 2, smaller is 1: swap. [1, 9, 2, 4, 8, 7]. Now at
  index 1, children 4 and 8, smaller is 4: swap. [1, 4, 2, 9, 8, 7].

Four swaps. Result [1, 4, 2, 9, 8, 7].

Max-heap from [3, 9, 2, 1, 4, 5], sinking into the **larger** child:

- i = 2, value 2, child index 5 holds 5: swap. [3, 9, 5, 1, 4, 2].
- i = 1, value 9, children 1 and 4: 9 is larger than both, stop.
- i = 0, value 3, children 9 and 5, larger is 9: swap. [9, 3, 5, 1, 4, 2]. Now at
  index 1, children 1 and 4, larger is 4: swap. [9, 4, 5, 1, 3, 2].

Result [9, 4, 5, 1, 3, 2].
:::

:::check
Why is bottom-up heapify O(n) while n pushes are O(n log n), when both build a
valid heap of the same elements?
--
Because they pay for different distances. A push starts at the bottom and may
climb to the root, so it pays the node's depth, and most nodes are deep: half of
them are leaves at depth about log2 n. Total about log2(n!) = Theta(n log n).

A sift down starts at a node and may fall to the bottom, so it pays the node's
height, and most nodes are short: half are leaves and pay nothing, a quarter pay
at most 1, an eighth at most 2. Total (n/4)*1 + (n/8)*2 + ... = n.

The catch: this only helps when you already have all n elements. A heap fed by a
stream must push.
:::

:::check
Someone says: "A min-heap's list is sorted enough. `h[0]` is the minimum, so
`h[-1]` is the maximum, and `h[:3]` is the three smallest." Where are they wrong,
and what can you actually say about where the maximum is?
--
The first claim is right; the other two are wrong, because the heap order only
constrains parent-child pairs. [1, 2, 8, 5, 3] is a valid min-heap: its last cell
holds 3, not the maximum 8, and its first three cells 1, 2, 8 are not the three
smallest (those are 1, 2, 3).

What you can say: every parent is no larger than its children, so no parent can be
a strict maximum. The maximum is therefore a leaf, at some index from n//2 to
n - 1. That is a range of about n/2 cells, not a position. To get the three
smallest, pop three times, O(3 log n).
:::

:::check
To return the k largest elements of a long stream you keep a heap of size k.
Should it be a min-heap or a max-heap? Why does the other one give a wrong answer
rather than a slow one? Trace both on [7, 2, 9, 4, 9, 1, 8] with k = 3.
--
A **min**-heap. It holds the k best seen so far, and when a new element arrives
you must decide whether it evicts the weakest of them, so the weakest must be
reachable: at the root.

Min-heap trace: [7], [2, 7], [2, 7, 9]; 4 > 2, replace: [4, 7, 9]; 9 > 4: [7, 9, 9];
1 < 7, skip; 8 > 7: [8, 9, 9]. Answer 9, 9, 8.

A max-heap capped at k pushes each element and pops the root when the size exceeds
k. The root is the largest, so each eviction throws away the best element seen so
far. It ends holding 1, 2, 4: the three smallest. That is a wrong answer, not a slow
one. The rule: **the root is what you are prepared to discard.**
:::

:::check
In `sift_down`, someone writes: "if the left child is smaller than me, swap with
it; otherwise if the right child is smaller, swap with that." Give a three-element
input where this breaks the heap, and say which pair is broken and why the proof
needed the smaller child.
--
[5, 2, 1]. The left child 2 is smaller than 5, so they swap: [2, 5, 1]. Now the
root 2 is the parent of 1 at index 2, and 2 > 1. The broken pair is (0, 2), which
the operation never looked at.

The value that moves up becomes the parent of both children, so it must be no
larger than both. Only the smaller child has that property. In the proof, this is
the check of the pair (i, o) with the other child o: "v <= a[o] because m was the
smaller child". It is the only place the word "smaller" appears, so it is the one
line that cannot be paraphrased.
:::

:::check
Disguised problem. "There are n piles of stones. Each turn, choose a pile with x
stones and remove floor(x / 2) of them. After exactly k turns, what is the least
possible total?" Reduce it to a heap problem, say which kind of heap, and trace
[5, 4, 9] with k = 2.
--
Each turn removes floor(x / 2), which is largest when x is largest, and removing
from one pile never makes another pile's option worse. So the greedy choice is
always the current largest pile, and after the turn that pile, now smaller, goes
back into the competition. "Take the extreme, transform it, push it back" is a
max-heap simulation (variation B). In Python, push the negated sizes.

Trace: piles [5, 4, 9], total 18. Turn 1: the largest is 9, remove 4, it becomes
5. Piles 5, 4, 5. Turn 2: the largest is 5 (either one), remove 2, it becomes 3.
Piles 3, 4, 5. Total 12.

This is [[p:snowflake-remove-stones-to-minimize-the-total|Remove Stones to Minimize the Total]].
Cost O(n + k log n): heapify, then k pop-and-push rounds (use `heapreplace` for
one walk per round).
:::
