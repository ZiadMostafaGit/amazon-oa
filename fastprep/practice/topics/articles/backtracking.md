# Backtracking

> Backtracking is not "try everything". It is a depth-first walk over a tree of
> partial answers, and the algorithm you are actually designing is the rule that
> lets you refuse to walk into a subtree.

## When you reach for it

You reach for backtracking when the answer is a **sequence of choices**, the
number of options at each choice is small, and you can judge a *partial* answer
before it is finished.

A hundred and sixty-eight problems here use it, which puts it at #24 of 150.
They arrive in four shapes, and the shape decides what the recursion returns, so
know which one you are in before writing a line.

- **Enumerate everything** — *Generate Parentheses*, *Work Schedule*,
  *Letter Combinations of a Phone Number*: the function returns nothing and
  appends to a list.
- **Count** — *Beautiful Arrangement*, *Count Unordered Coin Combinations*: it
  returns an integer and materialises nothing, which is the door to memoisation.
- **Find one, then stop** — *Sudoku Puzzle Solver*, *Word Search*: it returns a
  bool and every caller must short-circuit on `True`.
- **Optimise** — *Optimal Account Balancing*, *Partition into Equal-Sum Groups*:
  it returns the best value found, and the prune becomes a bound against the best
  answer so far.

The trigger that is almost never wrong is in the constraint block. *Generate
Parentheses* says `1 <= n <= 8`; *Beautiful Arrangement*, `1 <= n <= 15`;
*Expression Add Operators*, at most 10 digits; *Optimal Account Balancing*, at
most 8 transactions; *Word Search*, a 6 × 6 board. Those numbers are not modest
by accident. They are the setter telling you that an exponential search is the
intended solution and that the input has been sized to fit it.

The tool is wrong in three situations. If `n` runs to 10⁵ and the question is
"how many ways", the subproblems overlap and you want [[dynamic-programming]].
If the object can be built by a rule that never needs revisiting, you want
[[greedy]]. And if the count asked for is astronomically large, enumerating is
impossible by definition, however clever the pruning: *Count Ordered Combination
Sums* wants a number, and the recursion that produces it must never build a
list.

The boundary with [[dfs]] is worth stating plainly, since the words get used
interchangeably. DFS is the traversal; backtracking is DFS over a tree of
*partial solutions you construct as you go*, with the construction undone on the
way back up. *Root-to-Node Path in a Binary Tree* is the hinge case: the tree is
given, so it is a DFS, but the path you accumulate is built and unbuilt exactly
as backtracking does it.

## The idea

Picture a tree. The root is the empty answer. The children of a node are the
ways to extend it by one more choice. The leaves are complete answers, some
valid and some not. Every problem in this chapter is "walk that tree".

Now the two observations that turn a picture into an algorithm.

**You never build the tree.** At any instant you are standing at exactly one
node, and the only state you hold is the path from the root to it — one list,
one board, one `used` array. Going down a child is a *mutation* of that state;
coming back up is the mirror mutation. Three lines:

```python
apply(choice)
explore()
undo(choice)
```

That is the entire method. The "backtrack" in the name is the third line, and
the reason memory is O(depth) rather than O(number of nodes).

**You never enter a subtree that cannot contain an answer.** Before descending
into `path + [c]`, ask whether any valid answer starts with that prefix. If
provably none does, skip the child — and with it every descendant, which is where
the savings are. For *Generate Parentheses* the rule is two comparisons: never
open more than `n`, never close more than you have opened. For *Sudoku Puzzle
Solver* it is "this digit already appears in the row, column or box".

<svg viewBox="0 0 700 330" role="img" aria-label="search tree for well-formed parentheses with two pairs, showing pruned branches as crosses">
  <g>
    <text x="300" y="26" text-anchor="middle">empty</text>
    <line x1="292" y1="34" x2="222" y2="80"/>
    <line x1="312" y1="34" x2="392" y2="80"/>
    <text x="215" y="94" text-anchor="middle">(</text>
    <text x="400" y="94" text-anchor="middle">) &#215;</text>
    <line x1="208" y1="102" x2="140" y2="146"/>
    <line x1="224" y1="102" x2="320" y2="146"/>
    <text x="132" y="160" text-anchor="middle">((</text>
    <text x="330" y="160" text-anchor="middle">()</text>
    <line x1="126" y1="168" x2="70" y2="212"/>
    <line x1="140" y1="168" x2="196" y2="212"/>
    <text x="62" y="226" text-anchor="middle">(()</text>
    <text x="206" y="226" text-anchor="middle">((( &#215;</text>
    <line x1="324" y1="168" x2="286" y2="212"/>
    <line x1="338" y1="168" x2="410" y2="212"/>
    <text x="278" y="226" text-anchor="middle">()(</text>
    <text x="420" y="226" text-anchor="middle">()) &#215;</text>
    <line x1="58" y1="234" x2="40" y2="278"/>
    <line x1="70" y1="234" x2="128" y2="278"/>
    <rect class="fill" x="6" y="286" width="62" height="26" rx="4"/>
    <text x="37" y="304" text-anchor="middle">(())</text>
    <text x="140" y="304" text-anchor="middle">(()( &#215;</text>
    <line x1="274" y1="234" x2="250" y2="278"/>
    <line x1="286" y1="234" x2="346" y2="278"/>
    <rect class="fill" x="220" y="286" width="62" height="26" rx="4"/>
    <text x="251" y="304" text-anchor="middle">()()</text>
    <text x="358" y="304" text-anchor="middle">()(( &#215;</text>
    <text x="500" y="160">&#215; = pruned before the call:</text>
    <text x="500" y="182">no descendant can be</text>
    <text x="500" y="204">well formed, so the whole</text>
    <text x="500" y="226">subtree is never entered</text>
  </g>
</svg>

Eight nodes are visited; generating all `2⁴ = 16` strings and filtering would
visit thirty-one. The gap is the chapter.

## Worked by hand

*Generate Parentheses* with `n = 2`. State: the list `path`, plus two counters
`o` (parentheses opened so far) and `c` (closed so far). At each node we try `(`
then `)`, in that order, which is why the output comes out lexicographically
sorted for free. A child is rejected if it would make `o > n` or `c > o`.

| # | path on entry | o, c | try `(` | try `)` | what happens |
| --- | --- | --- | --- | --- | --- |
| 1 | `` | 0,0 | o→1 ≤ 2, take | c→1 > o=0, **cut** | descend into `(` |
| 2 | `(` | 1,0 | o→2 ≤ 2, take | c→1 ≤ o=1, take | two live children |
| 3 | `((` | 2,0 | o→3 > 2, **cut** | c→1 ≤ 2, take | one live child |
| 4 | `(()` | 2,1 | o→3 > 2, **cut** | c→2 ≤ 2, take | one live child |
| 5 | `(())` | 2,2 | — | — | length 4: **emit `(())`** |
| — | back up to #2, `path` is `(` again | 1,0 | — | — | undo restored the state |
| 6 | `()` | 1,1 | o→2 ≤ 2, take | c→2 > o=1, **cut** | one live child |
| 7 | `()(` | 2,1 | o→3 > 2, **cut** | c→2 ≤ 2, take | one live child |
| 8 | `()()` | 2,2 | — | — | length 4: **emit `()()`** |

Two answers, eight nodes, six cuts. Three things show up that the code does not
say out loud.

**The cut happens before the call, not at the leaf.** Row 3 rejects `(((`
without creating that string. Descending and discovering the problem at depth 4
would have cost the whole subtree below `(((` — two more nodes here,
`2^(2n−k)` in general. Testing a child costs O(1); testing a leaf costs
everything underneath it.

**The state is one object, rewound.** Between rows 5 and 6, `path` goes from
`(())` back to `(` with no copy and no rebuilt string: `pop()` ran three times as
three calls returned. The parent at row 2 finds its state exactly as it left it,
which is the only reason it can try its second child at all.

**The counters are redundant but not free.** `o` and `c` could be recomputed
from `path` in O(depth) at every node; passing them as arguments makes each test
O(1). Carrying the summary of the prefix rather than re-deriving it is the
biggest constant-factor decision in any backtracking solution, and it is why
*Sudoku Puzzle Solver* wants row, column and box masks rather than an
`is_valid(board)` sweep.

## Why it is correct

The argument has three parts: the state really is rewound, the enumeration
misses nothing, and it produces nothing twice. All three are inductions over the
recursion tree.

:::proof `explore` emits exactly the valid completions of its prefix, once each

**Setup.** Fix a finite depth `L`. A *partial answer* is a sequence
`p = (c₁,…,c_k)` with `k ≤ L`. For each partial `p` with `k < L` let `C(p)` be a
finite ordered list of allowed next choices, and let the *children* of `p` be
`p·c` for `c ∈ C(p)`. A partial of length `L` is *complete*. Let `valid` be a
predicate on complete answers, and let `Sol(p)` be the set of complete valid
answers having `p` as a prefix. The procedure is

```
explore(p):            # the machine state represents p
    if |p| = L:  if valid(p): emit p;  return
    for c in C(p):
        if not feasible(p·c): continue
        apply(c); explore(p·c); undo(c)
```

Two hypotheses are required of the problem, not of the code:

- **(H1) Necessity of the prune.** `Sol(q) ≠ ∅ ⇒ feasible(q)`. Equivalently, an
  infeasible partial has no valid completion.
- **(H2) The children cover and separate.** Every element of `Sol(p)` has, as its
  `(k+1)`-th entry, some `c ∈ C(p)`; and no two distinct `c, c' ∈ C(p)` are equal,
  so the sets `Sol(p·c)` are pairwise disjoint and their union over `c ∈ C(p)` is
  `Sol(p)`.

Also **(H3)**: `apply(c)` followed by `undo(c)` is the identity on the machine
state, and `apply(c)` makes the state represent `p·c` when it represented `p`.

**Lemma (restoration).** `explore(p)` returns with the machine state equal to
what it was on entry. *Induction on the height `L − |p|`.* At height 0 nothing is
written. At height `h+1`, the body performs, for each surviving child, `apply(c)`,
then a call of height `h` — which by the induction hypothesis restores the state
it was given — then `undo(c)`. By (H3) the pair cancels, so each loop iteration
is state-neutral and so is the whole loop. ∎

**Theorem.** If the state represents `p` on entry, `explore(p)` emits every
element of `Sol(p)` exactly once, and emits nothing else.

*Induction on `L − |p|`.*

*Base, `|p| = L`.* There are no children. `Sol(p)` is `{p}` if `valid(p)` and `∅`
otherwise, which is exactly what the branch emits.

*Step, `|p| < L`.* Consider a child `c ∈ C(p)`.

- If `feasible(p·c)` is false, we skip it. By (H1) in contrapositive,
  `Sol(p·c) = ∅`, so nothing that should be emitted is lost.
- Otherwise we call `explore(p·c)`. By the restoration lemma the state represents
  `p·c` at that moment — earlier siblings left no residue — so the induction
  hypothesis applies: the call emits exactly `Sol(p·c)`, once each.

Summing over children, the emitted multiset is `⋃_{c ∈ C(p)} Sol(p·c)`. By (H2)
that union is `Sol(p)`, and the parts are disjoint, so no element is emitted
twice. Nothing outside `Sol(p)` is emitted, because everything emitted deeper is
in some `Sol(p·c) ⊆ Sol(p)`.

**Termination.** `|p|` strictly increases with depth and is capped at `L`, and
each `C(p)` is finite, so the recursion tree is finite: at most
`1 + b + … + b^L` nodes where `b = max |C(p)|`. A depth-first walk of a finite
tree halts. ∎
:::

Now the part worth more than the proof: what it leaned on. Every backtracking bug
is one of these five hypotheses failing quietly.

- **(H1) is necessity, not sufficiency.** The prune may keep hopeless branches;
  it may never cut a hopeful one. "Sum already exceeds the target, stop" is
  necessary when every candidate is positive and *not* necessary the moment a
  negative appears — which is precisely why this bank carries *Combination Sum II
  With Negative Values* and *Count Ordered Combination Sums with Negative Values*
  as separate problems. The symptom of a too-aggressive prune is missing answers
  on inputs your samples do not contain.
- **(H2) coverage** fails when `C(p)` forgets an option: an index skipped, a
  digit not tried, a direction not walked. Symptom: too few answers, and usually
  only for some inputs.
- **(H2) separation** fails when two different choices build the same object. The
  classic is permuting `"aab"`: choosing the first `a` and choosing the second `a`
  yield the same string. Symptom: duplicates, in exactly the count that the
  multiplicities predict. *Unique String Permutations* exists to make you handle
  this.
- **(H3) exact undo.** Whatever `apply` touched — the path, a `used` flag, a
  running sum, a board cell, a set of seen values — `undo` must restore all of it.
  A half-restored state does not crash; it makes a sibling explore a subtree that
  is not its own.
- **Bounded depth.** The recursion tree is finite only because `|p|` grows. Allow
  a choice that does not consume anything — reusing a candidate of value 0 in a
  combination sum, say — and the induction has no measure to decrease on.

One thing the proof does *not* use: it never says `feasible` is sufficient. A
backtracker with `feasible = True` everywhere is correct, only slow. If your
answers are wrong, the prune is the suspect; if they are right and late, it is
the cure.

## What it costs

Let `b` bound the number of children of a node, `d` the depth, `w` the work at an
internal node and `ℓ` the work at a leaf. With no pruning, the cost of a node
with `k` levels below it satisfies

```
T(0) = ℓ
T(k) = w + b·T(k-1)
```

Unrolling, `T(d) = w·(b^d − 1)/(b − 1) + b^d·ℓ = Θ(b^d·(w + ℓ))`. Two readings
of that formula matter.

**The leaf work is not free.** For enumeration, `ℓ` is `path[:]` or
`"".join(path)`, which is `Θ(d)`. So *Subsets* on `n` elements is `Θ(n·2ⁿ)`, not
`Θ(2ⁿ)`. That is not a defect: the output itself has total size
`Σ_k C(n,k)·k = n·2^{n−1}` characters, so no algorithm can do better. The same
goes for permutations, where the branching shrinks by one per level:
`T(k) = Θ(k) + k·T(k−1)` with `T(0) = Θ(n)` gives `Θ(n·n!)`, and the output is
`n·n!` symbols. **Enumeration is output-sensitive; the only thing you control is
the overhead per answer.**

**Pruning changes the base, not the shape.** In the worst case the bound is still
`b^d` — pruning is a data-dependent saving and proves no better asymptotic
bound in general. But look at what it buys concretely. For `n = 8` pairs of
parentheses the unpruned tree has `2⁹ − 1 = 511` internal nodes over
`2¹⁶ = 65536` leaves; the runnable block below measures the pruned walk at 6,917
nodes for 1,430 answers, against 131,071 nodes unpruned. That is 4.8 nodes per
answer instead of 92, and the ratio grows: the Catalan number `C_n` is about
`4ⁿ/n^{1.5}`, so the unpruned-to-pruned ratio grows like `n^{1.5}`.

A sharper statement is available when the prune is not merely necessary but also
**sufficient** — when every feasible partial really does extend to some answer,
as it does for parentheses. Then every node lies on a root-to-leaf path ending in
an answer, so

```
nodes ≤ (number of answers) × (depth + 1)
```

and the total time is `O(answers × depth × per-node work)`. Such an algorithm has
*polynomial delay*: the gap between consecutive answers is polynomial, so it
starts printing immediately and never stalls. Generate-and-filter has no such
guarantee, and that, not the constant factor, is why it is the wrong shape.

**Space is `O(d)`**, plus the output. The recursion stack holds `d` frames, the
path holds `d` entries, and the tree is never materialised. This is the one
resource where backtracking beats breadth-first search outright, and it is the
entire motivation for iterative deepening below.

Three costs people forget. Rebuilding the state instead of mutating it —
`explore(path + [c])` — allocates at every node and turns `Θ(bᵈ)` into `Θ(bᵈ·d)`.
Re-validating from scratch multiplies `w` by `Θ(n)`. And deduplicating at the end
with a `set` pays to build and hash every duplicate: for *Unique String
Permutations* on a string of many repeats that is `n!` work to report far fewer
answers, where the skip rule costs `Θ(distinct answers × n)`.

## The implementation

The template and one full instantiation, with the node counts the section above
quoted, and a brute-force cross-check so the claims are not just claims.

```python run
def generate(n, prune=True):
    """All well-formed sequences of n pairs, lexicographically. Counts nodes."""
    res, path, nodes = [], [], 0

    def well_formed(s):
        bal = 0
        for ch in s:
            bal += 1 if ch == "(" else -1
            if bal < 0:
                return False
        return bal == 0

    def explore(opened, closed):
        nonlocal nodes
        nodes += 1
        if len(path) == 2 * n:                     # complete: test and record
            s = "".join(path)
            if well_formed(s):
                res.append(s)
            return
        for ch in "()":                            # "(" first -> sorted output
            o, c = opened + (ch == "("), closed + (ch == ")")
            if prune and (o > n or c > o):         # (H1): no completion below
                continue
            path.append(ch)                        # apply
            explore(o, c)                          # recurse
            path.pop()                             # undo, exactly
    explore(0, 0)
    return res, nodes


def catalan(n):
    c = 1
    for k in range(n):
        c = c * 2 * (2 * k + 1) // (k + 2)
    return c


print(" n  answers   pruned nodes   blind nodes   blind/pruned   nodes/answer")
for n in range(1, 9):
    good, gn = generate(n, True)
    blind, bn = generate(n, False)
    assert good == blind, n                  # pruning changed nothing but speed
    assert good == sorted(good), n           # "(" before ")" gives sorted output
    assert len(good) == catalan(n), n        # the count is the Catalan number
    assert gn <= len(good) * (2 * n + 1)     # sufficient prune => bounded delay
    print("%2d %8d %14d %13d %14.1f %14.1f"
          % (n, len(good), gn, bn, bn / gn, gn / len(good)))
print()
print("n=3 ->", generate(3)[0])
```

Three lines are doing the real work.

`path.append(ch) … path.pop()` are written as a matched pair with the recursion
between them. Type them together, always, before you type anything else in the
loop body; a `pop` added later is a `pop` that will one day be added to the wrong
branch.

`if prune and (o > n or c > o): continue` tests the *child*, using counters the
child would have, and rejects it without constructing it. Notice it is a
statement about `o` and `c` alone — not about `path` — which is what makes it
O(1). Every good backtracking solution has a line like this, and finding it is
the actual problem-solving step.

`for ch in "()"` fixes the child order, and because `(` sorts before `)` the
answers come out in lexicographic order with no sort at the end. *Generate
Parentheses* and *Combination Sum with Reusable Values* both ask for
lexicographic output; walking the tree in sorted order is free, sorting 1,430
strings afterwards is not.

The `assert good == blind` line is the proof executed: pruning is a performance
decision and must not move a single answer. Make that assertion while developing
— write the blind version, then prune, then diff — and (H1) stops being something
you merely hope for.

## Variants you will meet

**Subsets.** Two children per element, take or leave: depth `n`, `2ⁿ` leaves.
*Subsets*, *Enumerate All Subsequences*, *Sorted Subsets of a String*. See
[[subsets]].

**Permutations.** Children are the unused elements, tracked with a `used` array
or by swapping in place: depth `n`, `n!` leaves. *Permutations*, *Beautiful
Arrangement* (which adds the divisibility test as its prune and wants a count).
See [[permutations]].

**Combinations, via a start index.** The difference between the three Pinterest
problems in this bank is one argument. `explore(i)` — may reuse the current
candidate — is *Combination Sum with Reusable Values*. `explore(i + 1)` — each
value once — is *Combination Sum with Single-Use Values*. `explore(0)` — order
matters, so `(2,3)` and `(3,2)` are different — is *Count Ordered Combination
Sums*, while *Count Unordered Coin Combinations* is the same recursion with the
start index restored. One character; four different problems.

**Assignment into bins.** *Partition into Equal-Sum Groups*, *Optimal Account
Balancing*: place item `i` into one of `k` groups. Symmetry breaking is essential
here — two empty groups are interchangeable, so only ever try the *first* empty
one, cutting `k!` duplicate labellings down to one.

**Grid walks with a visited mark.** *Word Search*, *Enumerate Right-and-Down
Matrix Paths*. `apply` writes a sentinel into the cell and `undo` writes the
letter back. *Word Search II* adds a [[trie]] so the prune becomes "no word has
this prefix", collapsing a search over a whole dictionary into one walk.

**Constraint search.** *Sudoku Puzzle Solver*. Two ideas beyond the template:
keep row, column and box bitmasks so legality is O(1) ([[bit-manipulation]]), and
pick the *most constrained* empty cell next. Variable ordering cannot change
correctness — (H2) says nothing about the order of `C(p)` — and routinely changes
the running time by orders of magnitude.

**Backtracking plus memoisation.** When the recursion returns a value depending
only on a *suffix* of the state, cache it. *Word Break II* memoises on the start
index; *Beautiful Arrangement* memoises on the set of used values, which is
[[dp-bitmask]] with `n ≤ 15` chosen so `2¹⁵` states fit. This is the bridge out
of exponential time, and why [[memoization]] is the chapter to read next.

**Branch and bound.** For the optimisation shape, carry the best answer found so
far and prune any partial whose optimistic bound cannot beat it. The prune is
still necessary in the sense of (H1) — it discards only partials that provably
cannot *improve* — which is why the argument survives with `Sol` redefined as
"completions strictly better than the incumbent".

### Iterative deepening

Depth-first search uses `O(d)` memory but can dive down the wrong branch forever
and gives no guarantee about finding the *shallowest* answer. Breadth-first
search finds the shallowest but stores a frontier that is `O(b^d)`. Iterative
deepening buys both: run a depth-limited DFS with limit 0, then 1, then 2, until
one succeeds.

It looks wasteful — the limit-`d` pass redoes everything the limit-`(d−1)` pass
did — and it is not. In a uniform `b`-ary tree, a search to limit `k` visits
`N(k) = (b^{k+1} − 1)/(b − 1)` nodes, so the total is

```
Σ_{k=0}^{d} N(k) = Σ_{i=0}^{d} (d + 1 − i)·b^i ≤ b^d · Σ_{j≥0} (j+1)·b^{−j}
                 = b^d · (b/(b−1))²
```

while the final pass alone costs `N(d) ≈ b^d · b/(b−1)`. The ratio is at most
`b/(b−1)`: twice the work for a binary branching, 11% extra for `b = 10`. The
repetition is a geometric tail, and the deepest level — which holds most of the
tree — is visited only once.

```python run
from collections import deque

LIMIT = 4096

def moves(x):                       # from x you may double it or subtract one
    if 2 * x <= LIMIT:
        yield 2 * x
    if x - 1 >= 1:
        yield x - 1

def bfs(start, goal):
    seen, q, peak = {start}, deque([(start, 0)]), 1
    while q:
        peak = max(peak, len(q))
        x, d = q.popleft()
        if x == goal:
            return d, peak
        for y in moves(x):
            if y not in seen:
                seen.add(y)
                q.append((y, d + 1))
    return None, peak

def dls(x, left, goal, path, stat):          # depth-limited DFS, O(depth) memory
    stat[0] += 1
    if x == goal:
        return True
    if left == 0:
        return False
    for y in moves(x):
        path.append(y)
        if dls(y, left - 1, goal, path, stat):
            return True
        path.pop()                            # undo, as always
    return False

def iddfs(start, goal, cap=30):
    total = 0
    for depth in range(cap + 1):
        path, stat = [start], [0]
        found = dls(start, depth, goal, path, stat)
        total += stat[0]
        if found:
            return depth, total, path
    return None

def full_tree(start, depth):                  # nodes in one exhaustive pass
    stat = [0]
    dls(start, depth, None, [start], stat)
    return stat[0]

for start, goal in [(1, 31), (3, 7), (1, 100)]:
    d, peak = bfs(start, goal)
    dd, total, path = iddfs(start, goal)
    one = full_tree(start, d)
    assert dd == d                            # same shallowest answer as BFS
    assert len(path) == d + 1 and path[0] == start and path[-1] == goal
    assert total <= 2 * one                   # the b/(b-1) bound, b = 2
    print("%4d -> %4d  depth %2d | bfs peak frontier %3d | iddfs deepest stack %2d"
          % (start, goal, d, peak, len(path)))
    print("            iddfs visited %5d nodes vs %5d for one full pass (x%.2f)"
          % (total, one, total / one))
    print("            path", path)
```

Reach for it when the state space is too large to store a visited set, the answer
is shallow, and you want the shortest solution. **IDA\*** — iterative deepening
on `g + h` with an admissible heuristic rather than on depth — is how puzzle
solvers are actually written. When the state space *is* small enough to hold,
plain [[bfs]] is simpler and visits each state once: *Open the Lock* has only 10⁴
states, so BFS wins there and iterative deepening would only re-expand.

## Recognising it in a statement

Ordered by how much to trust them.

1. **A tiny explicit bound on `n`.** `n ≤ 8`, `n ≤ 10`, `n ≤ 15`, a 9 × 9 board,
   a 6 × 6 grid. Combined with any question at all, this is the strongest signal
   in the chapter. Nobody caps `n` at 8 for a linear algorithm.
2. **"Return all / every / each distinct …"** followed by sequence-shaped
   objects: schedules, combinations, expressions, paths, squares. *Work
   Schedule*, *Factor Combinations*, *Word Squares*.
3. **The answer is described by a rule that a prefix can already violate.**
   "well-formed", "nondecreasing", "no leading zero", "each cell used at most
   once", "sums to the target". That rule is your `feasible`; if you can evaluate
   it on a prefix, you have a backtracking problem.
4. **"Use each … exactly once".** A `used` mask and a permutation-shaped search.
   *Enumerate Valid Clock Times* uses each of four digits exactly once;
   *Expression Add Operators* uses each digit once and in order.
5. **"In lexicographic order".** Weak on its own, but it pairs with enumeration
   and tells you to order `C(p)` rather than sort at the end.

The anti-signals, which are just as useful:

- **A large `n` with a counting question.** "How many ways, `n ≤ 10⁵`" is
  [[dynamic-programming]]; an answer wanted modulo something is a second tell.
- **"Minimum / maximum" with polynomial structure.** *Coin Change* is in this
  bank and yields to DP; backtracking gets the right answer and times out.
- **`n ≤ 20` with a count or an optimum but no request to list.** That is
  [[dp-bitmask]] territory: the search tree has `n!` leaves but only `2ⁿ` distinct
  states, and memoising collapses one into the other.
- **"Does a path exist" on a plain graph.** That is [[dfs]] or [[bfs]] with a
  permanent visited set. The distinction: in *Word Search* a cell may be reused by
  a *different* path, so the mark must be undone; in reachability it may not, so
  the mark must not be. Undoing a visited mark in a reachability search turns a
  linear algorithm into an exponential one.

## Traps

**Forgetting to undo one of the things you applied.** The path is obvious; the
`used` flag, the running sum and the board cell are not. Symptom, when it is the
`used` array: the search produces exactly one answer and then unwinds to nothing,
because every element stays consumed forever.

**Appending the mutable path itself.** `res.append(path)` stores a reference, so
by the end every entry is the same list — and that list is empty. Symptom: the
right *number* of results, all identical and usually empty.

**No deduplication with repeated input values.** Two indices holding the same
letter are different choices producing the same object, breaking (H2)'s
separation clause. Symptom: each distinct answer appears `∏ (multiplicity!)`
times.

```python run
from itertools import permutations as itertools_permutations

def permute(s, skip_dups=True, unmark=True, copy=True):
    """Distinct permutations, with three switches for three classic bugs."""
    a = sorted(s)                       # sorting puts equal values adjacent
    n, used, res, path = len(a), [False] * len(s), [], []

    def go():
        if len(path) == n:
            res.append(path[:] if copy else path)      # bug 3: no copy
            return
        for i in range(n):
            if used[i]:
                continue
            if skip_dups and i and a[i] == a[i - 1] and not used[i - 1]:
                continue                                # bug 2: no skip rule
            used[i] = True
            path.append(a[i])
            go()
            path.pop()
            if unmark:
                used[i] = False                         # bug 1: no unmark
    go()
    return ["".join(p) for p in res]

s = "aab"
truth = sorted({"".join(p) for p in itertools_permutations(s)})
print("correct           ", permute(s))
print("no skip rule      ", permute(s, skip_dups=False), "<- each answer twice")
print("never unmark used ", permute(s, unmark=False), "<- one answer, then nothing")
print("append, no copy   ", permute(s, copy=False), "<- 3 aliases of one empty list")
assert permute(s) == truth
assert len(permute(s, skip_dups=False)) == 6 and len(truth) == 3
assert len(permute(s, unmark=False)) == 1
assert set(permute(s, copy=False)) == {""}
print("distinct permutations of 'aabb':", permute("aabb"))
assert permute("aabb") == sorted({"".join(p) for p in itertools_permutations("aabb")})
```

**A prune that is not necessary.** "Stop when the sum exceeds the target" is
sound with positive candidates and unsound the moment a negative appears — the
trap *Combination Sum II With Negative Values* is built around. Symptom: missing
answers, only on inputs holding the offending values.

**An unbounded recursion.** Reusing a candidate of value 0, or any choice that
consumes nothing, removes the measure termination needs. Symptom:
`RecursionError`, not a wrong answer.

**Python's recursion limit.** About a thousand frames by default. A path search
on a 100 × 100 grid can reach ten thousand: use an explicit stack, or raise the
limit knowingly.

**Validating only at the leaf.** Correct by the proof — `feasible ≡ True` is
allowed — and catastrophically slow. Symptom: right answers, timeout.

**Recomputing the summary from scratch.** Rescanning the prefix for its sum,
balance or used set turns O(1) node work into O(depth). Symptom: a correct-looking
solution a factor of `n` too slow.

**Sharing a visited mark across independent starts.** *Word Search* restarts
from every cell; if the grid is not fully restored between starts, later ones
search a maze the earlier ones dug. Symptom: the answer depends on where the scan
began.

## What to memorise

The template, which should come out of your fingers without thought:

```python
def explore(state):
    if complete(state):
        record(state)          # or: return True / return count / update best
        return
    for choice in choices(state):
        if not feasible(state, choice):
            continue           # test the CHILD, before constructing it
        apply(choice)
        explore(state)
        undo(choice)           # restore everything apply touched
```

The sentence that turns a problem into it: *"Is the answer a sequence of small
choices, where I can rule out a partial answer before it is finished?"* If yes,
the search is mechanical and the design work is all in the `feasible` line.

The habit: **type `apply` and `undo` as one gesture, mirrored, and put the
recursion between them afterwards.** Every state-restoration bug in this chapter
comes from writing them at different moments.

The rule that keeps you honest: *the prune may keep hopeless branches; it may
never cut a hopeful one.* When in doubt, diff against the unpruned version on
small inputs.

Numbers worth carrying. `8! = 40,320`; `10! = 3,628,800`; `12! = 479,001,600` —
so `n!` enumeration is comfortable to about `n = 10` and hopeless past 12.
`2²⁰ ≈ 10⁶` and `2²⁵ ≈ 3.4 × 10⁷` — subset enumeration is comfortable to about
`n = 20`, and if `n ≤ 20` with a count rather than a list, think [[dp-bitmask]].
Iterative deepening costs at most a factor `b/(b−1)` over a single pass.

## Check yourself

:::check
The proof requires `Sol(q) ≠ ∅ ⇒ feasible(q)`. Why that direction, and what
exactly goes wrong if you have the implication the other way round?
--
The code uses the prune in contrapositive: it skips `q` when `feasible(q)` is
false, and the step is sound only because "not feasible" implies "no completion".
So the requirement is that feasibility is **necessary** for having a solution
below you.

The converse — `feasible(q) ⇒ Sol(q) ≠ ∅` — is sufficiency, and it is never
required for correctness. It is a *performance* property: if it happens to hold,
every node you enter leads to at least one answer, the tree has at most
`answers × (depth + 1)` nodes, and the enumeration runs with polynomial delay.

Implement a test that rejects some hopeful branches and you get silently missing
answers — usually not in the sample cases, because samples tend to be the inputs
where the over-eager rule happens to be safe.
:::

:::check
Someone says: "pruning does not change the complexity — it is `O(bᵈ)` with or
without, so it is a micro-optimisation." Where are they wrong?
--
They are right about the worst-case bound and wrong about everything that follows
from it.

First, the worst-case bound is not the running time; it is an upper bound that
pruning is not *guaranteed* to improve. For real inputs it routinely does, by
factors that grow with `n`. The runnable block measures *Generate Parentheses* at
`n = 8`: 6,917 nodes pruned against 131,071 blind, and since the Catalan number
grows like `4ⁿ/n^{1.5}` while the blind tree grows like `4ⁿ`, the ratio grows
like `n^{1.5}` without bound.

Second, for some problems pruning changes the class outright. A blind *Sudoku
Puzzle Solver* tries 9 digits in each of up to 81 cells and will not finish; with
the row/column/box test most cells have one or two candidates and the search
finishes at once. Same code, same `O(9⁸¹)` bound, different universe.

Third, the delay. Without a prune that is also sufficient there is no bound at
all on the time between consecutive answers — a property a user notices, and one
no asymptotic statement about the total captures.
:::

:::check
The duplicate-permutation skip rule is
`if i and a[i] == a[i-1] and not used[i-1]: continue`. Why is the condition
`not used[i-1]` rather than `used[i-1]`, given that both versions deduplicate
correctly?
--
Both do produce each distinct permutation exactly once, so this is a speed
question, not a correctness one.

The rule fixes a canonical order for equal values: a run of identical values must
be consumed left to right. `not used[i-1]` says "the previous copy has not been
taken, so taking this one uses them out of order — skip", and it fires at the
*top* of the branch, before any descent, so the whole duplicate subtree is cut.

`used[i-1]` enforces the opposite convention and, as written, allows the branch
to begin and only rejects it deeper, after work has been done. Instrumenting both
on `"aaab"` gives 14 nodes for the `not used[i-1]` form against 32 for the other,
and on `"aabb"` 19 against 33. Same answers, roughly twice the tree.

The prerequisite either way is the `sorted` call: equal values must be adjacent
for "the previous copy" to mean anything.
:::

:::check
*Combination Sum with Reusable Values* and *Count Ordered Combination Sums* have
almost the same recursion. Which argument differs, and why does it turn a set of
combinations into a count of sequences?
--
The start index. Writing `explore(i, …)` for the child — may pick candidate `i`
again, never an earlier one — enumerates each multiset once, in nondecreasing
order. Writing `explore(i + 1, …)` forbids reuse and enumerates each subset once.
Writing `explore(0, …)` allows any candidate at any step and enumerates ordered
sequences, so `(2, 3)` and `(3, 2)` are both produced.

In the proof's language, the start index is how `C(p)` is chosen so (H2)'s
separation clause holds for *multisets*: each multiset becomes reachable by
exactly one path, its sorted one. Drop it and each is reached once per
arrangement — a bug if you want combinations, the specification if you want
compositions. *Count Unordered Coin Combinations* wants the start index; *Count
Ordered Combination Sums* wants it gone.
:::

:::check
You have a puzzle with roughly 10¹² reachable states, a branching factor of 4,
and a solution you believe is at most 14 moves deep. BFS or iterative deepening,
and what is the cost of the choice?
--
Iterative deepening. BFS would need a frontier and a visited set holding a
significant fraction of `4¹⁴ ≈ 2.7 × 10⁸` states, and at tens of bytes each that
is tens of gigabytes. Iterative deepening holds one path: 14 frames.

The cost is re-expansion. The bound derived above is `b/(b−1) = 4/3`, so the
whole sequence of passes costs at most about 33% more node expansions than a
single exhaustive pass to depth 14 — and it still returns a shallowest solution,
because the first limit at which any solution is found is by construction the
minimum depth.

The trade is explicit: you spend time to save memory, and you give up duplicate
detection with no visited set. If the state graph has short cycles, check only
that a state does not repeat *on the current path* — `O(depth)`, which preserves
the memory bound where a global visited set would not.
:::
