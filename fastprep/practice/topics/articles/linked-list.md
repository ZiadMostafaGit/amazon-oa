# Linked Lists

> A linked list is a chain you can only walk forwards and only hold by the links you have named, so every algorithm on it comes down to one discipline: before you overwrite a pointer, make sure every node you will still need has another name.

## The problem it solves

Here is a singly linked list holding 1, 2, 3, 4, 5:

```
head -> [1] -> [2] -> [3] -> [4] -> [5] -> None
```

Each box is a node with two fields: a value and `next`, a reference to the following
node. The list as a whole is just the reference to the first node, `head`. There is
no index, no length field and no way to go backwards. To reach the fourth node you
start at `head` and follow `next` three times.

The first task everyone meets is [[p:the-walt-disney-company-reverse-linked-list|Reverse Linked List]]:
reverse the list *by changing the next pointers*, keeping every node's value where
it is, and return the new head.

```
head -> [5] -> [4] -> [3] -> [2] -> [1] -> None
```

Someone who thinks in arrays writes the array solution: swap the first and last,
then the second and second-to-last, and so on. On a list, "the i-th node" costs i
steps to reach, so each swap is a walk, and the total is about n^2/2 steps. For 500
nodes that is fine. For the 10^5 nodes of a list problem like
[[p:bloomberg-remove-linked-list-elements|Remove Linked List Elements]] it is
5·10^9 steps. And it swaps values, which the statement forbids: the nodes must move,
not their contents.

The second solution copies the nodes into a Python list, relinks them backwards, and
returns the last one. That is correct and O(n). It also uses O(n) extra memory for
something the list already has, and interviewers ask for O(1) on purpose: the point
of the question is whether you can rewire a chain without dropping it.

What this chapter builds is the way of working that does every list task in one pass
and O(1) extra space: reversing, merging, deleting, finding the middle or the k-th
from the end, detecting a cycle. And it builds the one structure where a linked list
is genuinely the best tool, not an exercise: the hash map plus doubly linked list
behind an LRU cache.

### When it is the wrong tool

- **You need random access.** "The value at position i" for many i is an array's
  job. If the input arrives as a list but you are allowed O(n) memory and the task
  is about positions, copying to an array first is honest and often clearer.
- **The "list" is really an array in disguise.** Several bank problems pass the list
  as an array of values, or as an array `next` of successor indices. Read whether
  you must build and rewire nodes, or whether the array is simply the data. A `next`
  array with a cycle question is cycle detection on a functional graph
  ([[cycle-detection]]), which the same pointer tricks solve.
- **Sorting, searching, sums.** A list is a poor container for binary search or
  prefix sums. Those want contiguous memory.
- **Most "cache" design problems are mostly hash maps.** Many problems tagged
  linked list in this bank are LRU, LFU or TTL caches. The list is one part; the
  map does the finding ([[hash-tables]], [[lru-cache]]).

Two hundred and twenty-two problems in this bank are tagged linked list. Most are
small exercises of the same five moves, and the sections below name them.

## Build it from the brute force

We start with the array-shaped solutions a beginner writes, count them, find the
waste, and the in-place pointer moves will appear as the way to stop wasting.

### Step 1: what you can and cannot do

You hold some nodes by name: `head`, and any variable you assign. From a named node
you can reach its successor (`node.next`), and the successor's successor, and so on.
You **cannot** reach a predecessor. A node that no name reaches, directly or by
following `next`, is gone: Python will collect it, and you will never find it again.

Every operation is one of two things:

- **Move a name**: `curr = curr.next`. Nothing in the list changes. A name slides
  forwards.
- **Change a link**: `curr.next = something`. The list changes. The old target of
  `curr.next` is no longer reachable *through curr*.

The second kind is where every bug lives, and it is the subject of this chapter.

### Step 2: the array-thinking brute force, counted

Write `get(i)`: start at head, follow next i times. Then reverse by swapping values
`get(i)` and `get(n-1-i)` for i < n/2. Each pair costs about i + (n-1-i) = n-1 steps
of walking. With n/2 pairs, the total is about n^2/2. On 10^5 nodes, 5·10^9.

The waste is obvious once named: every `get` starts from the head. The walk to node
i+1 repeats the walk to node i and adds one step. The list is designed to be walked
once, in order, and this solution walks it n times.

### Step 3: the copy-out solution, and what it wastes

Walk once and put every *node* (not value) into a Python list `nodes`. Now
`nodes[i]` is O(1). Relink:

```
nodes[0].next = None
for i in 1..n-1: nodes[i].next = nodes[i-1]
return nodes[n-1]
```

On 1, 2, 3, 4, 5: node 2 now points to node 1, node 3 to node 2, and so on; node 1
points to None and node 5 is the new head. It is correct, one pass to copy, one pass
to relink: O(n) time, O(n) space.

Now look at what the relinking loop actually reads. At step i it touches `nodes[i]`
and `nodes[i-1]`, and nothing else. When it moves on to i+1, `nodes[i-1]` is never
read again. The array holds n references, and at every moment the loop needs two of
them. The other n-2 are dead weight.

Why did we need the array at all? Because of the one thing a list cannot do: go back.
When we are at node i and want to point it at node i-1, we must still know node
i-1. And because changing `node.next` destroys the only link to node i+1, we must
also know node i+1 *before* we change it. The array was a clumsy way to remember
two nodes: the one behind and the one ahead.

### The question that unlocks it

Here is the question to ask before every pointer assignment, on every list problem:

**Which nodes must I still be able to reach after this assignment, and does each of
them have a name?**

For reversal, at the moment we set `curr.next = prev`:

- We need `prev`, the node behind, because that is where `curr.next` will point. It
  must have a name, since there is no link back to it.
- We need the node ahead, `curr.next` before the assignment, because the rest of the
  list hangs from it, and the assignment is about to cut the only link to it. So we
  name it first: `nxt = curr.next`.
- After the assignment, `curr` is the new front of the reversed part, so `prev`
  becomes `curr`, and `nxt` becomes the new `curr`.

Say it a second way. A linked list is a rope of knots that you hold only by your
hands. Changing `curr.next` is cutting the rope just after a knot. Before you cut,
grab the piece you are about to drop.

### Step 4: three names instead of an array

The array version used `nodes[i-1]`, `nodes[i]` and, implicitly, the way to get to
`nodes[i+1]`. Replace them with three names: `prev`, `curr`, `nxt`.

```
prev, curr = None, head
while curr:
    nxt = curr.next      # name the rest before cutting
    curr.next = prev     # cut and turn this one link around
    prev = curr          # the reversed part now starts at curr
    curr = nxt           # step into the rest
return prev
```

Four lines, one pass, O(1) extra space. The array is gone because we noticed that
only two of its entries were ever alive at once. That is exactly the move from a 2-D
table to one row in dynamic programming: keep what the future reads, drop the rest.

### You might think: "Just swap the values."

Swapping values is sometimes allowed and sometimes forbidden, and it is never the
same thing. The nodes *are* the data in many real uses: other structures hold
references to them. In an LRU cache, a hash map maps each key to its node. If you
reverse by swapping values, `map[7]` still points to the same node object, but that
node now holds the value of key 3. Every lookup after the reversal is wrong. The
statement's "change the next pointers, keep the values" is protecting exactly this.

### You might think: "`curr.next = prev`, then `curr = curr.next`."

This is the most natural wrong order, and it walks backwards. After `curr.next =
prev`, the field `curr.next` *is* prev. So `curr = curr.next` moves curr back to the
node it just came from, or to None on the first step. On [1, 2, 3], the first
iteration sets node 1's next to None and then sets curr to None, so the loop ends
and returns node 1 alone. Nodes 2 and 3 are unreachable. The list has lost
everything but its head, and there is no error message. The fix is the first line of
the loop: read `curr.next` *before* you overwrite it.

### You might think: "To delete a node, set it to the next one."

`node = node.next` moves a *name*. It does not change the list. If you write a helper
`remove_first(head)` that does `head = head.next`, the caller's list is unchanged,
because the helper rebound its own local name. To delete a node from a singly
linked list you must change the `next` field of the node **before** it:
`prev.next = prev.next.next`. Deletion is a predecessor's job. That one fact
produces the next technique.

### Step 5: the head has no predecessor, so invent one

Deleting needs the node before. The head has no node before it. So every deletion
routine written naively has two cases: "delete the head" (move `head`) and "delete
anything else" (`prev.next = prev.next.next`). Merging has the same split: "the
first node of the result" versus "every later node".

The cure is a **dummy head**: a throwaway node placed before the real head.

```
dummy = Node(0); dummy.next = head
```

Now every real node, including the first, has a predecessor. Deletion is one case.
Building a new list is one case: start a `tail` at the dummy and append. At the end,
the answer is `dummy.next`, which is the true head whether or not the old head
survived. The dummy is the answer to the unlocking question for the head: "after I
delete the first node, how do I still reach the list?" Through the dummy.

### Step 6: no going back, so carry the past with you

The remaining classic tasks are about positions you cannot index: the middle, the
k-th from the end, the start of a cycle. You cannot walk backwards, and counting the
length first costs a second pass. The fix is again a second name that walks with the
first: **two pointers**, either a fixed number of nodes apart (a gap of k) or moving
at different speeds (fast and slow). They are derived in the variations below. The
idea is always the same: the information you would want to look back for is carried
along by a name that is behind you.

### The technique in one sentence

**Linked lists: walk once with a few named pointers, and before every change to a
`next` field, give a name to every node that change would make unreachable; use a
dummy so the head has a predecessor, and a second pointer to carry positions you
cannot go back for.**

And the question that produces every move: **which nodes must I still reach after
this assignment, and does each of them have a name?**

## Worked by hand

Get a pen. Reverse [1, 2, 3, 4]. Write the state *after* each iteration: the three
names, and the two separate chains that exist at that moment, the reversed part
(starting at prev) and the untouched rest (starting at curr).

| step | nxt | link changed | prev | curr | reversed part | rest |
|---|---|---|---|---|---|---|
| start | - | - | None | 1 | (empty) | 1 -> 2 -> 3 -> 4 |
| 1 | 2 | 1.next = None | 1 | 2 | 1 | 2 -> 3 -> 4 |
| 2 | 3 | 2.next = 1 | 2 | 3 | 2 -> 1 | 3 -> 4 |
| 3 | 4 | 3.next = 2 | 3 | 4 | 3 -> 2 -> 1 | 4 |
| 4 | None | 4.next = 3 | 4 | None | 4 -> 3 -> 2 -> 1 | (empty) |

curr is None, so the loop stops and returns prev, node 4. The list is
4 -> 3 -> 2 -> 1.

Step 2, told in full:

> "curr is node 2, prev is node 1, and node 1 already points to None, so the
> reversed part is just [1]. I want node 2 to point back at node 1. But node 2's next
> is node 3, and that link is the only way to reach 3 and 4. So first I name it: nxt
> = node 3. Now I can cut: node 2's next becomes node 1. The reversed part is
> 2 -> 1. Node 2 is its new front, so prev = node 2. The rest still starts at node 3,
> which I saved: curr = node 3."

Here is the moment just before step 2's cut, as a picture.

<svg viewBox="0 0 620 210" role="img" aria-label="nodes 1, 2, 3, 4 in a row; node 1 points to None; node 2 points to node 3; prev names node 1, curr names node 2, nxt names node 3, which is shaded because it must be named before node 2's link to it is cut; a dashed arrow shows node 2's new link back to node 1">
  <g>
    <rect x="40" y="70" width="70" height="40" rx="4"/>
    <text x="75" y="95" text-anchor="middle">1</text>
    <rect x="190" y="70" width="70" height="40" rx="4"/>
    <text x="225" y="95" text-anchor="middle">2</text>
    <rect class="fill" x="340" y="70" width="70" height="40" rx="4"/>
    <text x="375" y="95" text-anchor="middle">3</text>
    <rect x="490" y="70" width="70" height="40" rx="4"/>
    <text x="525" y="95" text-anchor="middle">4</text>
    <line x1="260" y1="90" x2="338" y2="90"/>
    <polygon points="338,90 328,85 328,95"/>
    <line x1="410" y1="90" x2="488" y2="90"/>
    <polygon points="488,90 478,85 478,95"/>
    <line x1="560" y1="90" x2="600" y2="90"/>
    <text x="604" y="95">x</text>
    <line x1="40" y1="90" x2="12" y2="90"/>
    <text x="8" y="80" text-anchor="start">None</text>
    <path d="M 205 112 Q 150 160 95 112" fill="none" stroke-dasharray="5 4"/>
    <polygon points="95,112 97,124 105,117"/>
    <text x="150" y="168" text-anchor="middle">new link: 2.next = 1</text>
    <text x="75" y="45" text-anchor="middle">prev</text>
    <line x1="75" y1="50" x2="75" y2="68"/>
    <text x="225" y="45" text-anchor="middle">curr</text>
    <line x1="225" y1="50" x2="225" y2="68"/>
    <text x="375" y="45" text-anchor="middle">nxt</text>
    <line x1="375" y1="50" x2="375" y2="68"/>
    <text x="300" y="80" text-anchor="middle">cut</text>
    <text x="310" y="200" text-anchor="middle">Shaded: the node that the cut would orphan. It is named first.</text>
  </g>
</svg>

Three things the trace shows that the code alone would not:

1. **At every moment there are exactly two chains, and together they hold every
   node.** The reversed part grows by one at the front, the rest shrinks by one at the
   front. Nothing is ever in neither, which is the whole correctness argument.
2. **prev is never "the previous node of the original list" in any lasting sense.**
   It is the front of the reversed part. That is why the function returns prev, not
   curr.
3. **The first iteration sets node 1's next to None.** The old head becomes the new
   tail, and the None that ends the new list comes from the initial `prev = None`. If
   you started with prev = head, node 1 would point to itself.

### A second trace: deleting with a dummy, including the head and a run

Remove every 6 from [6, 1, 6, 6, 2], as in
[[p:bloomberg-remove-linked-list-elements|Remove Linked List Elements]]. Put a dummy
D in front, and walk a pointer `prev` that always sits on a node we are keeping. At
each step, look at `prev.next`. If it is a 6, bypass it; otherwise move prev forward.

| step | prev | prev.next | action | list from D |
|---|---|---|---|---|
| 1 | D | 6 (first) | bypass: D.next = 1 | D -> 1 -> 6 -> 6 -> 2 |
| 2 | D | 1 | keep: prev = 1 | same |
| 3 | 1 | 6 (third) | bypass: 1.next = 6 (fourth) | D -> 1 -> 6 -> 2 |
| 4 | 1 | 6 (fourth) | bypass: 1.next = 2 | D -> 1 -> 2 |
| 5 | 1 | 2 | keep: prev = 2 | same |
| 6 | 2 | None | stop | answer D.next: 1 -> 2 |

Two cells to stare at. Step 1 deleted the **head**, and nothing special happened: D
was its predecessor. Without the dummy, step 1 would be a separate branch that moves
`head`. Step 3 to step 4: after bypassing, prev did **not** move. The node now after
prev is new and has not been checked yet, and it is another 6. If the code moved prev
forward after every bypass, it would step onto the fourth node's position, skip
checking it, and leave a 6 in the list. "Bypass or advance, never both" is the
deletion version of "save before you cut". It gets its own run below.

## From the idea to the code

### The direct version, against the brute force

The program builds real nodes, reverses them three ways (the get(i) value-swapper,
the copy-out relinker and the three-pointer loop), counts the walking each does, and
checks that the in-place version moves nodes, not values.

```python run
import random

class Node:
    __slots__ = ("val", "next")
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

def build(vals):
    head = None
    for v in reversed(vals):
        head = Node(v, head)
    return head

def to_list(head, limit=10**6):
    out = []
    while head and len(out) < limit:
        out.append(head.val); head = head.next
    return out

def reverse_by_get(head):              # array thinking: O(n^2) walking, swaps values
    steps, n, node = 0, 0, head
    while node: n += 1; node = node.next
    def get(i):
        nonlocal steps
        node = head
        for _ in range(i): node = node.next; steps += 1
        return node
    for i in range(n // 2):
        a, b = get(i), get(n - 1 - i)
        a.val, b.val = b.val, a.val
    return head, steps

def reverse_copy(head):                # O(n) space: an array of nodes
    nodes = []
    while head: nodes.append(head); head = head.next
    if not nodes: return None
    nodes[0].next = None
    for i in range(1, len(nodes)): nodes[i].next = nodes[i - 1]
    return nodes[-1]

def reverse(head):                     # O(1) space: three names
    prev, curr = None, head
    while curr:
        nxt = curr.next                # name the rest before cutting
        curr.next = prev               # turn this link around
        prev, curr = curr, nxt         # grow the reversed part, step into the rest
    return prev

h = build([1, 2, 3, 4, 5]); first = h
r = reverse(h)
print("reversed:", to_list(r))
assert to_list(r) == [5, 4, 3, 2, 1] and first.next is None and first.val == 1
assert reverse(None) is None and to_list(reverse(build([7]))) == [7]

for n in (100, 1000):
    _, steps = reverse_by_get(build(list(range(n))))
    print("n=%d: get(i) swapping walks %d steps; the loop walks %d" % (n, steps, n))
    assert steps > n * n // 3

random.seed(3)
for _ in range(300):
    vals = [random.randint(0, 9) for _ in range(random.randint(0, 12))]
    assert to_list(reverse(build(vals))) == vals[::-1]
    assert to_list(reverse_copy(build(vals))) == vals[::-1]
print("in-place reverse == copy-out reverse == vals[::-1] on 300 random lists")
```

### Each line, and which part of the idea it is

| line | in plain words | in the idea |
|---|---|---|
| `prev, curr = None, head` | the reversed part is empty; the rest is everything | the two chains at the start |
| `while curr` | there is still something in the rest | stop when the rest is empty |
| `nxt = curr.next` | name the rest of the rest | "save before you cut" |
| `curr.next = prev` | turn this one link around | the only line that changes the list |
| `prev = curr` | the reversed part now starts here | grow the reversed chain at its front |
| `curr = nxt` | step into the saved rest | shrink the rest at its front |
| `return prev` | the front of the reversed part | the new head |

One line changes the list. One line protects it. The other three move names.

Three boring confusions, settled:

- **`prev = None` is the new tail's None.** The old head ends the reversed list, and
  it must point to None. The initial prev supplies it.
- **The loop does not need the length.** It stops when curr becomes None, which is
  when the rest is empty.
- **Tuple assignment is a trap here.** `prev, curr = curr, nxt` is safe: the right
  side is evaluated first. A one-line reversal such as
  `curr.next, prev, curr = prev, curr, curr.next` also happens to work, but reorder its
  targets to `prev, curr, curr.next = curr, curr.next, prev` and it breaks, because the
  targets are assigned left to right and `curr.next` is then the *new* curr's field.
  Nobody reading either line can tell which is which. Write the four lines.

### The subtle line, both ways

The line is the order of `nxt = curr.next` and `curr.next = prev`. The same subtlety
appears in deletion as "bypass, or advance, never both". The program runs both wrong
and right versions on the same small inputs and prints the state after each step.

```python run
class Node:
    __slots__ = ("val", "next")
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

def build(vals):
    head = None
    for v in reversed(vals): head = Node(v, head)
    return head

def to_list(head):
    out = []
    while head: out.append(head.val); head = head.next
    return out

def reverse(head, save_first):
    prev, curr, step = None, head, 0
    while curr:
        step += 1
        if save_first:
            nxt = curr.next; curr.next = prev; prev = curr; curr = nxt
        else:                                  # cut first, then read the cut field
            curr.next = prev; prev = curr; curr = curr.next
        print("   step %d: reversed %s, rest %s" % (step, to_list(prev), to_list(curr)))
    return prev

print("save first:"); right = to_list(reverse(build([1, 2, 3]), True))
print("cut first:");  wrong = to_list(reverse(build([1, 2, 3]), False))
assert right == [3, 2, 1] and wrong == [1]        # nodes 2 and 3 are lost

def remove(head, target, advance_always):
    dummy = Node(0, head); prev = dummy
    while prev and prev.next:
        if prev.next.val == target:
            prev.next = prev.next.next             # bypass
            if advance_always:
                prev = prev.next                   # wrong: the new prev.next is unchecked
        else:
            prev = prev.next                       # advance
    return dummy.next

vals = [6, 1, 6, 6, 2]
good, bad = to_list(remove(build(vals), 6, False)), to_list(remove(build(vals), 6, True))
print("remove 6 from", vals, ": bypass-or-advance", good, " bypass-and-advance", bad)
assert good == [1, 2] and bad == [1, 6, 2]
```

Point at the exact steps. In the reversal, "cut first" prints `step 1: reversed [1],
rest []`: node 1's next became None, and then `curr = curr.next` read that None. The
loop ended after one node. Nothing crashed; nodes 2 and 3 are simply unreachable.

In the deletion, "bypass and advance" goes wrong at the run 6, 6. Standing on node 1,
it bypasses the first of the two 6s, so node 1 now points to the second 6, and then it
advances onto that second 6 without ever asking whether it should be deleted. The
second 6 becomes prev, which means it is treated as a keeper. The output [1, 6, 2] is
what happens when a pointer moves onto a node it never looked at. (The head 6 was
removed correctly: the problem is only ever the node right after a bypass.)

What the wrong reversal computes is "detach the head": it returns the first node alone.
What the wrong deletion computes is "remove every target that does not directly follow
another removed node", which passes every test without two targets in a row.

## Why it is correct

:::proof In-place reversal, and Floyd's cycle detection
**Reversal. What we claim.** For a finite list a_1 -> a_2 -> ... -> a_n -> None, the
loop returns a_n, and the links become a_n -> a_(n-1) -> ... -> a_1 -> None.

**The invariant.** Before each iteration, after k nodes have been processed:

1. prev is the head of the chain a_k -> a_(k-1) -> ... -> a_1 -> None (empty when
   k = 0, prev = None);
2. curr is the head of the untouched chain a_(k+1) -> ... -> a_n -> None (None when
   k = n);
3. every node is in exactly one of the two chains.

**Base case, k = 0.** prev = None is the empty chain; curr = head is the whole
original list; every node is in the second chain.

**Inductive step.** Suppose the invariant holds with curr = a_(k+1). The loop saves
nxt = a_(k+1).next = a_(k+2) (or None). It sets a_(k+1).next = prev, which makes
a_(k+1) -> a_k -> ... -> a_1 -> None. It sets prev = a_(k+1) and curr = nxt =
a_(k+2). Now (1) holds for k+1, (2) holds because a_(k+2) onward was never touched
(only a_(k+1)'s field changed, and it was read first), and (3) holds because a_(k+1)
moved from the second chain to the first and nothing else moved.

**Termination.** Each iteration moves one node from the finite second chain to the
first. After n iterations curr = None, the loop stops, and by (1) prev is a_n at the
front of the fully reversed chain.

**Floyd's cycle detection. What we claim.** Move slow one step and fast two steps per
round from the head. If the list has no cycle, fast reaches None. If it has a cycle,
they land on the same node, and then a pointer from the head and a pointer from the
meeting node, both moving one step, meet exactly at the first node of the cycle.

**No cycle.** fast moves forwards along a finite chain and must reach its end.

**They meet.** Let the tail before the cycle have mu nodes and the cycle have lambda
nodes. After mu rounds slow enters the cycle; fast is already in it. From then on,
measure the distance d from fast forward to slow along the cycle (0 <= d < lambda).
Each round slow moves 1 and fast moves 2, so d shrinks by exactly 1. It cannot jump
from 1 to past 0, because it changes by exactly one. So within lambda rounds, d = 0:
they are on the same node. In particular slow has not completed a full lap of the
cycle when they meet.

**The entry.** Say the meeting node is a steps into the cycle, 0 <= a < lambda.
Slow walked mu + a steps. Fast walked twice that, 2(mu + a), and also mu + a plus
some whole number m >= 1 of laps: 2(mu + a) = mu + a + m·lambda. So mu + a =
m·lambda, that is mu = m·lambda - a. A pointer that starts at the meeting node and
walks mu steps reaches position a + mu = m·lambda, which is position 0 of the cycle:
the entry. A pointer from the head that walks mu steps also reaches the entry, by the
definition of mu. They move in lockstep, and before mu steps the head pointer is
still in the tail, where the other pointer never is, so the first node where they
coincide is the entry. ∎
:::

The arguments quietly used these assumptions. Each is a place a variant can break.

- **The list is finite and, for reversal, acyclic.** On a list with a cycle, part (3)
  of the invariant fails the moment curr walks back into nodes already in the reversed
  part. Surprisingly the loop still ends, but it returns the *original* head with the
  cycle's direction flipped, not a reversed list. The bank's reversal problems all say
  "acyclic"; if yours does not, detect the cycle first.
- **Only the field just read is written.** The reversal proof needed that a_(k+2)'s
  chain was untouched. A variant that writes two fields per step (reversing in pairs,
  in groups of k) needs every field read before any of them is written.
- **Nobody else holds references that expect the old order.** Rewiring nodes in place
  is invisible to code that only follows next from the head. A hash map of nodes, as in
  LRU, survives rewiring (the nodes are the same objects) but not value swapping.
- **Steps are of size 1 and 2.** The "d shrinks by exactly 1" argument is why the
  speeds are 1 and 2. With speeds 1 and 3 the gap shrinks by 2 per round, so on a
  cycle of even length with an odd starting gap it jumps over 0 forever and the
  pointers never meet.

## What it costs

**Time.** Every technique here walks the list a constant number of times. Reversal:
n iterations of four assignments. Merging two lists of lengths m and n: at most m + n
comparisons, each followed by one link. Deletion: each node is looked at once, bypassed
or passed. Middle: n/2 rounds of the fast pointer moving two. k-th from the end: n + 1
steps of the lead pointer, n + 1 - k of the trailer. All O(n).

**Floyd's rounds.** At most mu rounds to bring slow into the cycle and fewer than
lambda more to meet, so at most mu + lambda < n + 1 rounds, each three pointer moves.
Then at most mu more for the entry. O(n) time, O(1) space, which is the reason to use
it: the obvious alternative is a set of visited nodes, O(n) space.

**Space.** All of the moves are O(1): a handful of names. The dummy node is one extra
node. The copy-out solutions are O(n).

**The brute force for comparison.** get(i)-style code on a list is O(n) per access and
O(n^2) per pass. The trap is not obvious in Python because `get(i)` is a function call
that looks as cheap as `a[i]`.

**The forgotten costs.**

- **Recursion.** A recursive reversal is elegant and uses O(n) stack. Python's default
  recursion limit is 1000, so a 10^5-node list raises `RecursionError`. Lists are long
  and thin; walk them with loops.
- **`len(list)`.** A singly linked list has no length field. Computing it is a full
  pass. That is fine once; it is O(n^2) if done inside a loop.
- **Python overhead.** Each node is an object. A 10^5-node list is 10^5 allocations, and
  pointer-chasing is several times slower than walking a Python list. This matters only
  for performance, not correctness. `__slots__` on the node class saves memory.
- **The LRU hash map.** O(1) "expected": hashing a key is cheap but not free, and the
  map dominates the cost, not the list.

## How to think about it

Linked list problems are rarely hard because of an idea. They are hard because one
wrong assignment silently drops half the list. So the thinking is mostly a drawing
discipline. Ask these, in order, every time.

1. **Draw three or four nodes, before and after.** Boxes and arrows. Write the
   target picture next to the start picture. Most list problems are solved at this step
   and only typed afterwards.
2. **List the links that change.** Every arrow that differs between the two pictures
   is one assignment to some `.next`. Count them.
3. **For each assignment, ask the question: which nodes must I still reach after it,
   and does each have a name?** Name them first. This decides the order of lines.
4. **Can the head change?** Deleting the head, inserting before it, merging, splitting,
   reversing a prefix: use a dummy and return `dummy.next`.
5. **Do I need a node behind me?** Deletion needs the predecessor: walk with `prev`
   and look at `prev.next` instead of standing on the node to delete.
6. **Do I need a position measured from the end or the middle?** Two pointers. From
   the end: a gap of k. The middle: speeds 1 and 2. A loop: speeds 1 and 2, then the
   head trick for the entry.
7. **Do I need to find a node by key in O(1), or remove one from the middle in O(1)?**
   A hash map from key to node, and a doubly linked list so the node can unlink itself
   without searching for its predecessor.
8. **Edge cases, always the same five:** empty list, one node, two nodes, the
   operation at the head, the operation at the tail. Trace each on paper.
9. **Does the new tail end in None?** Every rearrangement creates a new last node.
   Its `next` still points wherever it used to. Set it to None, or you have built a
   cycle.

Then, before writing code, write the before-and-after picture and the order of the
assignments. If you cannot write the order, the code will drop a node.

### Telling it from its neighbours

- **Arrays** ([[arrays]]). If the task is about positions, and O(n) memory is allowed,
  an array may be simpler. A list wins only when you insert and delete in the middle at
  a known node, in O(1), or when the problem insists on in-place rewiring.
- **Two pointers** ([[two-pointers]]). On arrays, two pointers usually come from both
  ends. On lists, both start at the head (you cannot start at the end), and they differ
  by a gap or a speed.
- **Fast and slow pointers** ([[fast-slow-pointers]]). The next chapter. It goes deeper
  into Floyd's algorithm, cycle length, and the functional-graph version (the `next`
  array problems).
- **Cycle detection in general** ([[cycle-detection]]). A list cycle is the simplest
  case. In graphs, use colours or a visited set.
- **Stacks** ([[stack]]). Checking a palindrome with a stack of values is O(n) space;
  reversing the second half in place is O(1). Interviews ask for the second.
- **Heaps and merging** ([[heap]], [[k-way-merge]]). Merging two lists is the dummy
  pattern; merging k lists adds a heap to choose the next node.
- **Sorting** ([[merge-sort]]). Merge sort is the natural sort for a list: split at the
  middle with fast/slow, sort each half, merge with a dummy. No random access needed.
- **LRU caches** ([[lru-cache]], [[design-data-structure]]). The list is the recency
  order; the map is the index into it.

## Variations

Ten variations, covering the five moves and the reordering problems that combine
them. Each says what changes, why, and which bank problem teaches it.

### A. Reverse the whole list

[[p:the-walt-disney-company-reverse-linked-list|Reverse Linked List]]. The three-
pointer loop above. The recursive version, for completeness: reverse the rest, then
hang the current node at the end of the reversed rest.

```
def rev(node):
    if node is None or node.next is None: return node
    new_head = rev(node.next)
    node.next.next = node     # my old successor is now the tail; put me after it
    node.next = None          # I am the new tail
    return new_head
```

The line `node.next.next = node` reads well once you know that `node.next` still
points to the old successor, which, after the recursive call, is the last node of the
reversed rest. Use the loop in practice: the recursion is O(n) deep.

### B. Reverse a part: a prefix, a sublist, groups of k

To reverse only a section, you need two extra names: the node **before** the section
(to attach the new front) and the section's **first** node (which becomes its last and
must be attached to whatever follows).

```
before = node before the section (the dummy if the section starts at the head)
first  = before.next
reverse exactly k nodes starting at first, ending with prev = new front, curr = after
before.next = prev        # attach the new front
first.next  = curr        # the old first is now the last; attach the rest
```

[[p:peoplestrong-reverse-nodes-in-k-groups|Reverse Linked-List Nodes in Groups of K]]
repeats this: probe k nodes ahead to check a full group exists (a short final group
stays as it is), reverse it, stitch, and set `before = first` for the next group. On
[1, 2, 3, 4, 5] with k = 2: [2, 1, 4, 3, 5]. The probe is the part people forget; it is
the "do I have a name for the next k nodes" question asked before touching any of them.

[[p:adobe-alternate-divisible-linked-list-prefix|Alternate Divisible Nodes After Reversing a Prefix]]
reverses only the first k nodes (the same stitch with `before` = dummy), then splits
and weaves, combining three moves in one OA problem.

### C. A dummy head to merge

[[p:the-walt-disney-company-merge-two-sorted-lists|Merge Two Sorted Lists]]. Keep a
`tail` that starts at a dummy. While both lists are non-empty, attach the smaller front
node to `tail`, advance that list, advance `tail`. When one runs out, attach the other
whole (it is already sorted and linked).

On [1, 3, 5] and [1, 2, 6]: take 1 (first list, on a tie take the first list, which
keeps the merge stable), 1, 2, 3, 5, then attach [6]. No node is created; only links
change. Without the dummy, the first attachment is a special case ("the result is
empty, so this node becomes the head"), and that special case is where bugs hide.

### D. A dummy head to delete, and to split into chains

[[p:bloomberg-remove-linked-list-elements|Remove Linked List Elements]] is the second
trace: walk `prev` from the dummy, bypass or advance.
[[p:amazon-linked-list-queue-operations|Linked-List Queue with Delete and Deduplication]]
does the same inside a hand-built queue, with an extra duty: if the deleted node was the
tail, the queue's `tail` reference must move to `prev`. Deleting the tail and forgetting
the tail reference is the classic bug of every list with a tail pointer.

**Splitting** is the dummy pattern twice. To move every third node to the end, as in
[[p:adobe-group-third-linked-list-nodes|Group Every Third Linked-List Node]], keep two
dummies and two tails, route each node to one chain by its position, then attach the
second chain to the end of the first and **set the last node's next to None**. On
[1, 2, 3, 4, 5, 6, 7]: the chains are 1, 2, 4, 5, 7 and 3, 6, giving
[1, 2, 4, 5, 7, 3, 6]. The final None matters: node 6 used to point to 7, and without
the cut, 7 -> 3 -> 6 -> 7 is a cycle.

### E. Fast and slow pointers: the middle

[[p:nvidia-middle-node-linked-list|Middle Node Of A Linked List]]. Start slow and fast at
the head. While `fast and fast.next`: slow moves one, fast moves two. When fast can no
longer move two, slow is at the middle.

Why: after r rounds slow is at position r and fast at 2r (0-based). The loop stops when
2r reaches the last node or runs off, so r is about n/2. Writing (slow, fast) as node values, on [1, 2, 3, 4, 5]: (1, 1),
(2, 3), (3, 5), then fast.next is None, stop: slow at 3. On [1, 2, 3, 4, 5, 6]: (1, 1), (2, 3),
(3, 5), (4, None): slow at 4, the **second** middle, which is what that problem asks
for. For the **first** middle (needed when you split a list into two halves for merge
sort), start fast at head.next instead. Decide which middle you need before writing the
loop condition.

### F. Fast and slow pointers: a cycle and its entry

[[p:google-detect-linked-list-cycle|Detect a Linked-List Cycle]]: run slow and fast; if
fast reaches None, no cycle; if they meet, cycle. The list arrives as an array `next` of
successor indices, so "move one" is `i = nxt[i]`. The proof is above.

[[p:google-linked-list-cycle-entry|Linked List Cycle Entry Node]]: after they meet, put
one pointer back at the head, keep the other at the meeting node, and move both one step
at a time. They meet at the entry. With next = [1, 2, 3, 4, 2] (0 -> 1 -> 2 -> 3 -> 4 ->
2): slow 1, 2, 3; fast 2, 4, 3; they meet at 3 after 3 rounds. Phase two: head pointer
0 -> 1 -> 2, meeting pointer 3 -> 4 -> 2. Entry: node 2. Here mu = 2 and lambda = 3, and
mu = 1·3 - 1 with a = 1, as the proof says. The [[fast-slow-pointers]] chapter takes
this further.

### G. A gap of k: the k-th from the end

[[p:mygate-remove-nth-node-from-end|Remove the Nth Node from the End]]. You cannot walk
back from the end. But if a lead pointer is k nodes ahead of a trailing one, then when the
lead falls off the end, the trailer is k nodes from the end. The gap carries the
"distance from the end" that you could not compute without a second pass.

To delete the n-th from the end you need its **predecessor**, so start both at a dummy
and move the lead n + 1 steps first. On [10, 20, 30, 40, 50], n = 2: lead goes D -> 10 ->
20 -> 30 (three steps). Then both move until lead is None: (40, 10), (50, 20),
(None, 30). The trailer is on 30, whose next, 40, is the 2nd from the end. Bypass:
[10, 20, 30, 50]. With n = 5 (the head), the trailer stays on the dummy and the bypass
removes the head with no special case.

### H. Reordering: combining the moves

The reordering problems are the moves in sequence. Each step is one you already know.

- **Palindrome in O(1) space**:
  [[p:omnissa-build-and-check-palindrome-list|Build and Check a Palindrome Linked List]].
  Find the middle (E), reverse the second half (A), walk both halves comparing values,
  and, politely, reverse the second half back. On [1, 2, 3, 2, 1]: middle 3, second half
  reversed is 1 -> 2 -> 3, compare 1 = 1, 2 = 2, done.
- **Reorder L0, Ln, L1, Ln-1, ...**: middle, reverse the second half, then weave the two
  halves one node from each, with the cut at the middle set to None first.
- **Odd-even and every-k-th grouping**: two dummy chains (D).
- **Reverse in groups**: B.

The habit for every combined problem: write the stages as a list of named moves before
writing any code. "Middle, cut, reverse, weave" is four small functions, each of which you
can test alone.

### I. A hash map plus a doubly linked list: the LRU cache

[[p:amazon-lru-query-result-cache|LRU Cache for Query Results]]: a cache of fixed
capacity, `get(key)` and `put(key, value)` in O(1), evicting the least recently used key
when full. Derive it from the operations.

- **Find a key in O(1)**: a hash map. Nothing else does that.
- **Know which key is least recently used**: keep the keys in recency order. An array
  would need O(n) to move a key to the front. A linked list moves a node to the front in
  O(1), *if* you already hold the node, which the map gives you.
- **Remove a node from the middle in O(1)**: in a singly linked list, removing needs the
  predecessor, which costs a search. So each node also stores `prev`: a doubly linked
  list, where a node can unlink itself: `node.prev.next = node.next; node.next.prev =
  node.prev`.
- **No special cases at the ends**: two sentinels, a head and a tail, that are never
  removed. The most recent node sits right after head; the least recent right before
  tail. This is the dummy-head idea at both ends.

The map stores key -> node; the node stores key and value (the key so that eviction can
delete it from the map). get: look up, move to front, return. put: if present, update
and move to front; else insert at front, and if over capacity, remove the node before
tail and delete its key from the map.

```python run
class DNode:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=None, val=None):
        self.key, self.val, self.prev, self.next = key, val, None, None

class LRU:
    def __init__(self, capacity):
        self.cap, self.map = capacity, {}
        self.head, self.tail = DNode(), DNode()          # sentinels, never removed
        self.head.next, self.tail.prev = self.tail, self.head
    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev
    def _push_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node                       # old first points back to node
        self.head.next = node
    def get(self, key):
        node = self.map.get(key)
        if node is None: return -1
        self._unlink(node); self._push_front(node)       # now most recent
        return node.val
    def put(self, key, val):
        if key in self.map:
            node = self.map[key]; node.val = val; self._unlink(node)
        else:
            node = DNode(key, val); self.map[key] = node
            if len(self.map) > self.cap:
                lru = self.tail.prev                     # least recent, before the sentinel
                self._unlink(lru); del self.map[lru.key]
        self._push_front(node)
    def order(self):                                     # most recent first
        out, n = [], self.head.next
        while n is not self.tail: out.append(n.key); n = n.next
        return out

c = LRU(2); log = []
for op in [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 2), ("get", 3)]:
    r = c.put(op[1], op[2]) if op[0] == "put" else c.get(op[1])
    log.append(r); print("%-12s -> %-4s order %s" % (op, r, c.order()))
assert log == [None, None, 1, None, -1, 3] and c.order() == [3, 1]

def faults(pages, cap):                                  # LRU page faults, same structure
    if cap == 0: return len(pages)
    c, f = LRU(cap), 0
    for p in pages:
        if c.get(p) == -1: f += 1; c.put(p, True)
    return f
print("page faults for [1,2,1,3,2], capacity 2:", faults([1, 2, 1, 3, 2], 2))
assert faults([1, 2, 1, 3, 2], 2) == 4 and faults([5, 5], 0) == 2
```

Read `_push_front` with the unlocking question. It changes four links. The node's own two
fields are set first, from `self.head.next`, while that still names the old first node.
Then the old first node's `prev` is pointed back at the new node, *still through
`self.head.next`*, which has not changed yet. Only then is `self.head.next` overwritten.
Swap the last two lines and `self.head.next.prev = node` sets the new node's prev to
itself, and the old first node keeps pointing back at the head: the backward chain is
broken, and the next eviction removes the wrong node.

[[p:expedia-lru-page-faults|LRU Page Faults]] is this cache in disguise: a page fault is
a get that misses. The `faults` function above is the whole solution. Capacity 0 is the
edge case: every access faults.

In Python, `collections.OrderedDict` with `move_to_end` and `popitem(last=False)` is an
LRU in four lines, and it is built from exactly this: a hash map and a doubly linked
list. Interviews usually want you to build it.

### J. Others you may meet (rare)

- **Intersection of two lists**: walk both; when a pointer ends, restart it at the other
  list's head. After at most m + n steps they meet at the shared node or both reach None,
  because both walk m + n in total.
- **Copy a list with random pointers**: a map from old node to new node, or the
  interleaving trick (insert each copy right after its original, set randoms, then
  split).
- **Add two numbers stored as lists**: walk both with a carry, building the result after
  a dummy.
- **Sort a list**: merge sort with fast/slow to split and the dummy merge.
- **Flatten a multilevel list**: a stack, or recursion, splicing each child chain in.

None of these needs a new move. Each is the question, asked at a different link.

## Recognising it in a statement

From most reliable to least:

1. **"Given the head of a linked list"**, **"by changing the next pointers"**,
   **"reuse the nodes"**, **"in place"**, **"O(1) extra space"**. Direct. The last two
   rule out the copy-to-array escape.
2. **"Reverse"**, **"reorder"**, **"rotate"**, **"swap pairs"**, **"in groups of k"**.
   Reversal and stitching.
3. **"Merge"**, **"remove all nodes with"**, **"delete duplicates"**, **"partition
   around x"**, **"odd and even positions"**. Dummy heads, often two.
4. **"Middle"**, **"palindrome"** (on a list), **"split into halves"**. Fast and slow.
5. **"n-th from the end"**, **"last k nodes"**. A gap of k.
6. **"Cycle"**, **"loop"**, **"revisits a node"**, **"first node of the cycle"**, often
   with a `next` array. Floyd.
7. **"Least recently used"**, **"evict"**, **"O(1) get and put"**, **"page faults"**,
   **"most recent first"**. Hash map plus doubly linked list.

### Disguises

**An array of successors.** "next[i] is the index after i; -1 means null" is a linked
list without node objects. Every pointer trick works with `i = next[i]` as the step. A
repeated-function problem ("apply f repeatedly from x; when do values repeat?") is the
same list, defined by a function.

**A queue or deque built by hand.** "Do not use a library container" means the list is
the container: head, tail, and a node class. Every delete must update tail if it removes
the last node.

**A cache with a counted cost.** Page faults, cache misses, "how many times did we fetch
from disk". It is an LRU, and the count is the number of misses.

### Anti-signals: looks like this, is not

- **"The list is given as an array, return an integer"** with no instruction to rewire.
  [[p:jpmorgan-binary-list-to-decimal|Binary Linked List to Decimal]] passes the bits as
  an array and says node allocation is outside the contract. It is a fold over an array:
  value = 2·value + bit.
- **Cache problems with frequency or time-to-live rules.** LFU needs a map of frequency
  buckets, TTL needs expiry times; the linked list may appear, but the design is about
  the maps.
- **"Shopping cart" or "process queries" stories** that only add, count and look up:
  hash maps.

## Traps

**1. Cutting before saving.** Symptom: the result has one node, or a short prefix, and
no error. Read `curr.next` into a name before you overwrite it.

**2. Advancing after a deletion.** Symptom: runs of the target value survive, one in
each run of two. Bypass or advance, never both.

**3. Special-casing the head, or returning the old head.** Symptom: deleting the first
node fails, or the function returns a node that is no longer in the list. Use a dummy and
return `dummy.next`.

**4. Not ending the new tail.** Symptom: an infinite loop when printing the result, or
a time limit. After any rearrangement, set the last node's next to None.

**5. `fast.next.next` on a short list.** Symptom: `AttributeError: 'NoneType' object has
no attribute 'next'`. The loop condition is `while fast and fast.next`, in that order.

**6. The gap off by one.** Symptom: deletes the neighbour of the right node. To delete
the n-th from the end, the trailer must stop on its predecessor: start at the dummy and
lead by n + 1.

**7. Rebinding a name inside a helper.** Symptom: the caller's list is unchanged.
`head = head.next` in a function changes only the function's variable. Return the new
head and have the caller assign it.

**8. Recursion on long lists.** Symptom: `RecursionError` at around 1000 nodes. Loops.

**9. LRU: forgetting the map.** Symptom: evicted keys still "found", or the cache grows.
Evicting a node must also delete its key from the map; updating an existing key must
move its node, not insert a second one.

The fourth, fifth and sixth traps, run:

```python run
class Node:
    __slots__ = ("val", "next")
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

def build(vals):
    head = None
    for v in reversed(vals): head = Node(v, head)
    return head

def to_list(head, limit=50):
    out = []
    while head and len(out) < limit: out.append(head.val); head = head.next
    return out

def group_third(head, cut_tail):
    d1, d2 = Node(0), Node(0); t1, t2 = d1, d2
    pos, node = 1, head
    while node:
        if pos % 3: t1.next = node; t1 = node
        else:       t2.next = node; t2 = node
        node, pos = node.next, pos + 1
    if cut_tail: t2.next = None                   # the new tail must end the list
    t1.next = d2.next
    return d1.next

ok = to_list(group_third(build([1, 2, 3, 4, 5, 6, 7]), True))
loop = to_list(group_third(build([1, 2, 3, 4, 5, 6, 7]), False), limit=12)
print("every third to the end:", ok, " without the cut (12 shown):", loop)
assert ok == [1, 2, 4, 5, 7, 3, 6] and len(loop) == 12   # 6 still points to 7: a cycle

def middle(head):
    slow = fast = head
    while fast and fast.next:                     # fast first, then fast.next
        slow, fast = slow.next, fast.next.next
    return slow.val

def middle_wrong(head):
    slow = fast = head
    while fast.next:                              # forgets fast itself can be None
        slow, fast = slow.next, fast.next.next
    return slow.val

print("middles:", middle(build([1, 2, 3, 4, 5])), middle(build([1, 2, 3, 4, 5, 6])))
assert middle(build([1, 2, 3, 4, 5])) == 3 and middle(build([1, 2, 3, 4, 5, 6])) == 4
try:
    middle_wrong(build([1, 2, 3, 4]))
    raise SystemExit("expected a crash")
except AttributeError as e:
    print("wrong loop condition on 4 nodes:", type(e).__name__)

def remove_nth_from_end(head, n, lead_by):
    dummy = Node(0, head); lead = trail = dummy
    for _ in range(lead_by): lead = lead.next
    while lead: lead, trail = lead.next, trail.next
    trail.next = trail.next.next
    return to_list(dummy.next)

right, off = remove_nth_from_end(build([10, 20, 30, 40, 50]), 2, 3), \
             remove_nth_from_end(build([10, 20, 30, 40, 50]), 2, 2)
print("remove 2nd from end: lead n+1 ->", right, "  lead n ->", off)
assert right == [10, 20, 30, 50] and off == [10, 20, 30, 40]
assert remove_nth_from_end(build([10, 20, 30, 40, 50]), 5, 6) == [20, 30, 40, 50]
```

Without the cut, the printed list is 1, 2, 4, 5, 7, 3, 6, 7, 3, 6, ... : node 6 kept its
old link to 7. With a lead of n instead of n + 1, the trailer stops on the node to delete
instead of its predecessor, and the last node is removed instead of the 2nd from the end.
And removing the 5th from the end of five nodes, the head, needs no special case because
the trailer can stop on the dummy.

## What to memorise

The four templates:

```python
# reverse
prev, curr = None, head
while curr:
    nxt = curr.next; curr.next = prev; prev = curr; curr = nxt
head = prev

# delete with a dummy: bypass or advance, never both
dummy = Node(0, head); prev = dummy
while prev.next:
    if bad(prev.next): prev.next = prev.next.next
    else:              prev = prev.next
head = dummy.next

# middle (second middle); start fast = head.next for the first middle
slow = fast = head
while fast and fast.next: slow, fast = slow.next, fast.next.next

# n-th from the end: lead by n + 1 from a dummy, then move both
```

The sentence that turns a problem into it: **draw before and after, list the links that
change, and order the assignments so that nothing is cut before it is named.**

The question behind every line: **which nodes must I still reach after this assignment,
and does each of them have a name?**

The habit: on paper, trace the empty list, one node, two nodes, the head and the tail.
Then check that the new tail ends in None.

The facts: Floyd meets in fewer than mu + lambda rounds, and the entry is found by
restarting one pointer at the head; LRU is a map from key to node plus a doubly linked
list with two sentinels; recursion on a list is O(n) deep.

## Check yourself

:::check
Hand trace. Reverse [1, 2, 3] with the three-pointer loop. After each iteration write
nxt, prev, curr, the reversed part and the rest. Then do the same with the lines in the
order `curr.next = prev; prev = curr; curr = curr.next` and say where the nodes go.
--
| step | nxt | prev | curr | reversed | rest |
|---|---|---|---|---|---|
| start | - | None | 1 | empty | 1 -> 2 -> 3 |
| 1 | 2 | 1 | 2 | 1 | 2 -> 3 |
| 2 | 3 | 2 | 3 | 2 -> 1 | 3 |
| 3 | None | 3 | None | 3 -> 2 -> 1 | empty |

Return node 3: 3 -> 2 -> 1.

Wrong order, step 1: node 1's next becomes None (prev was None), prev = node 1, and
curr = node 1's next, which is now None. The loop ends and returns node 1 alone. Nodes 2
and 3 still point 2 -> 3, but no name reaches them: they are lost.
:::

:::check
Hand trace. Remove the 2nd node from the end of [10, 20, 30, 40, 50] with a dummy D and a
lead of n + 1 = 3. Write lead and trail after every move. Then repeat for n = 5 and say
why no special case is needed.
--
Lead moves D -> 10 -> 20 -> 30. Then both move: (lead 40, trail 10), (50, 20),
(None, 30). Trail is on 30; trail.next is 40, the 2nd from the end. Set 30.next = 50.
Result [10, 20, 30, 50].

n = 5: lead moves 6 steps from D: 10, 20, 30, 40, 50, None. The while loop never runs;
trail is still on D. D.next = D.next.next removes 10, the head, and the answer is
D.next = 20 -> 30 -> 40 -> 50. The dummy is the head's predecessor, so removing the head
is the same line as removing anything else.
:::

:::check
Hand trace. A list is given as next = [1, 2, 3, 4, 5, 3] (node 5 points back to node 3).
Run Floyd: slow and fast positions per round until they meet, then phase two. What are
mu and lambda, and does the formula mu = m·lambda - a hold?
--
The path is 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 3 -> ... so mu = 3 (nodes 0, 1, 2) and the
cycle is 3, 4, 5, lambda = 3.

Round 1: slow 1, fast 2. Round 2: slow 2, fast 4. Round 3: slow 3, fast 4 -> 5 -> 3 = 3.
They meet at node 3 after 3 rounds.

Phase two: head pointer at 0, meeting pointer at 3. Move both: (1, 4), (2, 5), (3, 3).
They meet at node 3, the entry.

The meeting node is a = 0 steps into the cycle, and mu = 3 = 1·3 - 0, with m = 1. It
holds. (Here the meeting happens to be at the entry itself, so phase two walks a full
lap from the meeting point while the head pointer walks the tail.)
:::

:::check
Hand trace. An LRU cache of capacity 2 receives put(1, 1), put(2, 2), get(1), put(3, 3),
get(2), put(4, 4), get(1), get(3), get(4). Give each return value and the recency order
(most recent first) after each operation.
--
put(1,1): [1]. put(2,2): [2, 1]. get(1) = 1: [1, 2]. put(3,3): over capacity, evict the
least recent, 2: [3, 1]. get(2) = -1: [3, 1]. put(4,4): evict 1: [4, 3]. get(1) = -1:
[4, 3]. get(3) = 3: [3, 4]. get(4) = 4: [4, 3].

Returns: null, null, 1, null, -1, null, -1, 3, 4. The get(1) after put(3,3) is what saved
key 1 the first time; with no get in between, put(3,3) would have evicted 1 instead.
:::

:::check
Why does a dummy head remove the special case for deleting the first node? Answer
without code, in terms of what deletion needs.
--
Deleting a node from a singly linked list means changing the next field of the node
before it, because that is the only link that leads to it. Every node except the first
has a node before it; the first does not, so deleting it needs a different action
(moving the head name instead of changing a field). A dummy node placed before the head
gives the first node a predecessor too. Now every node has one, and deletion is always
the same assignment. The answer is read from the dummy's next, which is correct whether
or not the original head survived.
:::

:::check
Someone says: "In Floyd's algorithm the fast pointer moves two nodes at a time, so on a
cycle of odd length it can jump over the slow pointer and they may never meet." Where
are they wrong?
--
Measure the distance from fast forward to slow along the cycle once both are inside.
Each round, slow adds 1 to it and fast removes 2, so it changes by exactly 1, always
downwards. A quantity that drops by exactly 1 each round cannot skip a value: it must hit
0, and it does so within lambda rounds. Jumping over would need the gap to change by 2 or
more in one round. The length of the cycle, odd or even, does not enter the argument.
:::

:::check
Someone writes a function to drop the first node:
`def drop_first(head): head = head.next`. They call `drop_first(h)` and print h, and the
first node is still there. Explain, and fix it.
--
`head` inside the function is a local name. `head = head.next` moves that name; it does
not change any node, and it does not change the caller's name h. The list itself never
changed, because no `.next` field was assigned.

Fix: return the new head, `def drop_first(head): return head.next`, and call
`h = drop_first(h)`. In general, any operation that can change which node is first must
return the new first node (or work through a dummy that the caller can read).
:::

:::check
Reduce this disguised problem. "Given a list L0 -> L1 -> ... -> Ln, reorder it in place
to L0 -> Ln -> L1 -> Ln-1 -> L2 -> ... without changing values." Name the moves, in
order, and run them on [1, 2, 3, 4, 5].
--
Three moves: find the middle with fast and slow (first middle, so the first half is not
shorter), cut the list there and reverse the second half in place, then weave the two
halves taking one node from each.

[1, 2, 3, 4, 5]: the middle is 3. Cut after 3: first half 1 -> 2 -> 3 -> None, second
half 4 -> 5. Reverse the second half: 5 -> 4. Weave: 1, 5, 2, 4, 3. Result
[1, 5, 2, 4, 3].

The cut is the step people skip; without it, node 3 still points to 4, and the weave
creates a cycle.
:::
