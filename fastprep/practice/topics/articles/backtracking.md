# Backtracking

> Backtracking walks the tree of partial answers depth first, holding one shared partial answer that it extends on the way down and restores on the way up, and the design work is choosing the children so that every answer has exactly one path and refusing every subtree that cannot finish.

## The problem it solves

Coins of 2, 3 and 5 cents, as many of each as you like. List every way to make 8
cents, each way once. Order inside a way does not matter: 2 + 3 + 3 and 3 + 2 + 3
are the same way.

The answer is three ways: 2 + 2 + 2 + 2, 2 + 3 + 3, and 3 + 5. That is
[[p:bamtech-media-combination-sum|Combination Sum]], and its relatives
[[p:pinterest-combination-sum-with-reuse|Combination Sum with Reusable Values]]
and [[p:expedia-combination-sum-ii|Combination Sum II]].

The first program a beginner tries is nested loops: a loop for the first coin, a
loop inside it for the second coin, and so on. Then they hit the wall that this
chapter exists to climb. **How many loops?** For 8 cents the longest way uses four
coins, so four loops. For 15 cents, seven. The depth of the loop nest depends on
the input, and you cannot write a variable number of nested loops.

The second program fixes that with a library: generate every sequence of coins up
to the longest possible length, keep the ones that sum to 8, sort each one, throw
duplicates into a set. With three coins and lengths 0 to 4 there are
1 + 3 + 9 + 27 + 81 = 121 sequences, to find three answers. It is correct. Now
count it for 15 cents: lengths up to 7, 3,280 sequences, for 7 answers. Each extra
coin in the longest way triples the work, and nearly all of it is spent on two
kinds of junk: sequences that went over the target long before they ended
(5 + 5 is already 10), and reorderings of answers already found (3 + 5 and 5 + 3).

What this chapter builds is the method that removes both kinds of junk while
keeping the brute force's guarantee of finding everything. It visits 13 partial
answers for 8 cents and 47 for 15 cents. It is the general way to enumerate
anything that is built by a sequence of small choices: subsets, permutations,
combinations, placements on a board, paths in a grid, partitions of a string. It
is the most common technique in this bank after the basic data structures: 339
problems use it.

It is [[recursion]] used as a loop of variable depth, and it is [[dfs]] over a
tree that is never built.

### What the function returns: four shapes

Backtracking problems ask for one of four things, and the shape decides what the
recursive function returns. Know which one you are in before you write a line.

- **Enumerate every answer.** [[p:the-walt-disney-company-generate-parentheses|Generate Parentheses]],
  [[p:atlassian-permutations|Permutations]], Combination Sum. The function
  returns nothing and appends a copy of each complete answer to a list.
- **Count the answers.** [[p:mathworks-beautiful-arrangement|Beautiful Arrangement]].
  The function returns a number, and nothing is ever materialised. That is the
  door to memoisation.
- **Find one, or decide whether one exists.** [[p:microsoft-word-search|Word Search]],
  [[p:confluent-sudoku-puzzle-solver|Sudoku Puzzle Solver]],
  [[p:adobe-graph-m-coloring|Graph M-Coloring]]. The function returns a bool, and
  every caller must stop as soon as a child says yes.
- **Optimise.** [[p:adobe-longest-fruit-path|Longest Fruit Path]],
  [[p:pinterest-optimal-account-balancing|Optimal Account Balancing]]. The function
  returns or updates the best value found, and pruning becomes "this branch cannot
  beat the best so far".

### When it is the wrong tool

- **The count is huge and the subproblems repeat.** "How many ways to make
  10,000 cents" is a number with many digits; you cannot list the ways, and you
  do not need to. The same (amount left, coins allowed) question is asked
  millions of times: that is [[dynamic-programming]], here
  [[unbounded-knapsack]].
- **A rule builds the answer without ever revisiting a choice.** Then it is
  [[greedy]], and the search is wasted.
- **The shortest sequence of moves in a small state space.** "Fewest moves to open
  the lock" with 10^4 lock states is [[bfs]]: it visits each state once, and
  backtracking would re-explore the same states along different paths.
  [[p:amazon-open-the-lock|Open the Lock]] is this.
- **n up to about 20, and the question is a count or an optimum, not a list.** The
  search tree may have n! leaves, but only 2^n distinct "sets used so far"; memoise
  on the set and you are in [[dp-bitmask]].

The reliable sign that backtracking is intended is in the constraints. Generate
Parentheses says n <= 8. Permutations, at most 8 values. Word Search, a 6 x 6
board. Combination Sum II, 20 candidates and a target of 30. Nobody caps n at 8 for
a linear algorithm; the setter is telling you the exponential search fits.

## Build it from the brute force

We start where the beginner got stuck, with nested loops, and fix one problem at a
time. The template appears at the end.

### Step 1: a loop nest of variable depth

Take the purest version of the wall. [[p:atlassian-letter-combinations-of-a-phone-number|Letter Combinations of a Phone Number]]:
digit 2 is `abc`, digit 3 is `def`, and for the input `23` you list every string
made of one letter for each digit: `ad ae af bd be bf cd ce cf`.

For two digits, two loops:

```python
for x in "abc":
    for y in "def":
        out.append(x + y)
```

For three digits, three loops. The loops are all the same: "for each letter of
digit k, fix it, then do the remaining digits". A function that does "digit k and
everything after it" is exactly one loop that calls itself for the next digit:

```python
def explore(k, so_far):
    if k == len(digits):              # every digit has a letter: one answer
        out.append(so_far)
        return
    for ch in keys[digits[k]]:        # the k-th loop
        explore(k + 1, so_far + ch)   # the loops nested inside it
```

That is the first idea of backtracking: **the recursion is the loop nest, one
level of recursion per level of nesting, and the depth is decided at run time.**
The call `explore(k, ...)` is "I am inside the k-th loop".

### Step 2: one shared partial answer, extended and restored

`so_far + ch` builds a new string at every call. That is correct, and it copies the
whole partial answer at every node. The usual form keeps one list, `path`, shared
by all calls. Going into a child appends its choice. Coming back removes it.

```python
def explore(k):
    if k == len(digits):
        out.append("".join(path))     # record a copy of the shared path
        return
    for ch in keys[digits[k]]:
        path.append(ch)               # choose
        explore(k + 1)                # explore
        path.pop()                    # un-choose
```

Choose, explore, un-choose. The third line is the "back" in backtracking: after
the subtree under `ch` is finished, the path must be exactly what it was before,
so that the next letter `ch` is tried from the same position.

### You might think: "The recursion returns, so I do not need the pop."

The recursion returns, but the list is shared, and returning does not shrink it.
Without `path.pop()`, the code above on `23` records:

```
ad  ade  adef  adefbd  adefbde  adefbdef  adefbdefcd  adefbdefcde  adefbdefcdef
```

The first answer is right. Then `e` is appended to a path that still holds `a, d`,
and the base case (which tests `k`, not the length) records `ade`. Every later
answer carries all the earlier choices. The rule is absolute: **whatever you
changed on the way in, you change back on the way out**, and it applies to every
piece of shared state, not just the path: a `used` flag, a running sum, a mark on a
grid cell.

### Step 3: the tree, and the question that unlocks it

Back to the coins. Draw what the search does as a tree. The root is the empty
partial answer. Each child adds one more coin. A node whose coins sum to 8 is an
answer. That is a tree of **partial answers**, and every backtracking problem is
"walk this tree, depth first, and report the good leaves".

The tree is never built. At any moment the program stands at one node, and the
only thing it holds is the path from the root to that node. That is why it needs
memory proportional to the depth, not to the size of the tree.

What decides the shape of the tree is what you allow as children. That is the
whole design, and it comes from one question:

**What is one decision, and what must the partial answer remember so that the next
decision offers only legal, new options?**

For the phone letters, a decision is "the letter for digit k", and the partial
answer must remember k. For the coins, a decision is "the next coin". Read on to
see what the partial answer must remember there: it is not just the coins so far.

### Step 4: the first waste, the same answer in many orders

If the children of every node are "any of 2, 3, 5", the tree contains 2, 3, 3 and
3, 2, 3 and 3, 3, 2: one answer, three paths. Generate-and-filter found every
answer once per ordering and then paid a set to forget the orderings.

### You might think: "Generate everything and remove duplicates with a set."

It gives the right answers. Count what it pays. For coins [3, 4, 7, 8] and target
20, generate-and-filter builds 5,461 sequences for 7 answers. A set at the end does
not save any of that work; it only hides it. And the set must hash every duplicate,
so for a problem whose answers have many orderings, it spends most of its time
building things it will throw away.

The cure is to make each answer reachable by exactly one path. Pick one canonical
order for the coins inside an answer, say nondecreasing, and only ever build paths
in that order. Then 3, 2, 3 is never built, because 2 after 3 goes down. In the
tree, this means: **after choosing coin number i, the children may only choose coin
number i or later.** The partial answer must remember a start index.

That answers the unlocking question for coins: a decision is "the next coin", and
the partial answer must remember (the index of the last coin chosen, the amount
still missing). The start index removes orderings. The amount left is the next
fix.

### Step 5: the second waste, prefixes that can never finish

The path 5, 5 already sums to 10, more than 8. Every extension of it sums to more
than 10. Generate-and-filter builds all of them and tests each at the end. The
cure is to test the *child* before stepping into it: if adding coin c would exceed
the amount left, do not go there. That one test removes the child and its entire
subtree.

Sort the coins first, and it gets better: if coin c is too big, every coin after it
is bigger, so the loop can `break` instead of `continue`.

This is the second idea of backtracking, and the one that makes it fast: **reject a
partial answer the moment you can prove that no completion of it is valid.** The
rule that does it is called the prune.

### You might think: "Pruning is only a speed-up. It cannot change the answers."

It can, and the way it fails is silent. A prune is safe only if it never rejects a
partial answer that could still be completed. "Stop when the sum exceeds the target"
is safe here only because every coin is positive, so sums only grow.

Take candidates [3, -1] and target 2, each used at most once, processed in the given
order. The only answer is {3, -1}. The search chooses 3, sees the sum 3 exceeds 2,
and cuts the branch. The branch held the only answer. No error, no crash: just a
missing answer, on exactly the inputs that contain a negative value.
[[p:bytedance-combination-sum-ii-negative-values|Combination Sum II With Negative Values]]
exists to catch this. The rule to remember: **a prune may keep a hopeless branch; it
may never cut a hopeful one.**

### You might think: "A combination is a permutation with the order ignored, so I loop over all candidates at every level and sort at the end."

That is generate-and-filter again, with the duplicates removed by sorting. The
difference between a combination search and a permutation search is not in what you
do at the end. It is in the children. Permutations: any value not yet used, so
remember a `used` array. Combinations: any value at or after the start index, so
remember the index. One remembers a set, the other a position, and that is the
whole difference.

### Step 6: the third waste, equal values in the input

Combination Sum II gives candidates with repeats, such as [1, 1, 2], each position
usable once, target 3. Positions 0 and 1 hold the same value. The start index keeps
orderings out, but choosing "the 1 at position 0, then 2" and "the 1 at position 1,
then 2" are different paths to the same combination [1, 2]. Sort the candidates so
equal values sit together, and at each node, among the children, try each *value*
once: skip a candidate equal to the previous candidate *at the same level*. That
one line is the subtle line of this chapter, and the code section shows it right
and wrong.

### The technique in one sentence

Backtracking is a depth-first walk over the tree of partial answers, keeping one
shared partial answer that each step extends (choose), recurses on (explore) and
restores (un-choose), with children defined so that each answer has exactly one
path, and with a prune that rejects a child the moment it provably cannot be
completed.

## Worked by hand

Coins [2, 3, 5] (sorted), target 8, reuse allowed. A node is (path, left), and its
children are the coins from the start index on. The prune: if coin c > left, stop
the loop (every later coin is bigger).

| # | path | left | start | children tried | what happens |
|---|---|---|---|---|---|
| 1 | [] | 8 | 0 | 2, 3, 5 | all fit |
| 2 | [2] | 6 | 0 | 2, 3, 5 | all fit (5 <= 6) |
| 3 | [2,2] | 4 | 0 | 2, 3, then 5 > 4 **break** | two children |
| 4 | [2,2,2] | 2 | 0 | 2, then 3 > 2 **break** | one child |
| 5 | [2,2,2,2] | 0 | 0 | | **record [2,2,2,2]** |
| 6 | [2,2,3] | 1 | 1 | 3 > 1 **break** | dead end |
| 7 | [2,3] | 3 | 1 | 3, then 5 > 3 **break** | one child |
| 8 | [2,3,3] | 0 | 1 | | **record [2,3,3]** |
| 9 | [2,5] | 1 | 2 | 5 > 1 **break** | dead end |
| 10 | [3] | 5 | 1 | 3, 5 | the 2 is never offered |
| 11 | [3,3] | 2 | 1 | 3 > 2 **break** | dead end |
| 12 | [3,5] | 0 | 2 | | **record [3,5]** |
| 13 | [5] | 3 | 2 | 5 > 3 **break** | dead end |

Thirteen nodes, three answers, against 121 sequences for generate-and-filter.

The story of row 10, in words. "I am back at the root, and its first child, the
subtree of everything starting with 2, is finished. The path is empty again,
because every call below popped what it pushed. The next child is coin 3, at index
1. I push 3; the amount left is 5. Now this node's children start at index 1, not
0. That is what stops me from building 3, 2, 3: any answer that contains a 2 starts
with 2 in nondecreasing order, so it was already found in the subtree of row 2. The
children are 3 (left 2) and 5 (left 0, an answer)."

The story of row 3. "Path [2, 2], 4 left. Try 2: fits. Try 3: fits. Try 5: 5 > 4.
Because the coins are sorted, 5 and everything after it are too big, so I stop the
loop. I never create the node [2, 2, 5], and I never create anything below it."

Here is the same tree. Each box shows the path, then the amount left. Shaded boxes
are answers. The children that the prune refused are not drawn at all, which is the
point: they cost one comparison each and nothing else.

<svg viewBox="0 0 700 380" role="img" aria-label="the backtracking tree for coins 2, 3, 5 and target 8 with a start index: root with 8 left has children 2 (6 left), 3 (5 left) and 5 (3 left); 2 has children 2,2 (4 left), 2,3 (3 left), 2,5 (1 left); 2,2 has children 2,2,2 (2 left) and 2,2,3 (1 left); 2,2,2 has child 2,2,2,2 (0 left, an answer); 2,3 has child 2,3,3 (0 left, an answer); 3 has children 3,3 (2 left) and 3,5 (0 left, an answer); 5 has no children. Thirteen nodes, three shaded answers">
  <g>
    <rect x="315" y="10" width="70" height="34" rx="4"/>
    <text x="350" y="32" text-anchor="middle">[] 8</text>
    <line x1="335" y1="44" x2="200" y2="84"/>
    <line x1="350" y1="44" x2="470" y2="84"/>
    <line x1="365" y1="44" x2="620" y2="84"/>
    <rect x="160" y="84" width="80" height="34" rx="4"/>
    <text x="200" y="106" text-anchor="middle">[2] 6</text>
    <rect x="430" y="84" width="80" height="34" rx="4"/>
    <text x="470" y="106" text-anchor="middle">[3] 5</text>
    <rect x="580" y="84" width="80" height="34" rx="4"/>
    <text x="620" y="106" text-anchor="middle">[5] 3</text>
    <line x1="185" y1="118" x2="90" y2="164"/>
    <line x1="200" y1="118" x2="225" y2="164"/>
    <line x1="215" y1="118" x2="340" y2="164"/>
    <line x1="460" y1="118" x2="440" y2="164"/>
    <line x1="480" y1="118" x2="560" y2="164"/>
    <rect x="45" y="164" width="90" height="34" rx="4"/>
    <text x="90" y="186" text-anchor="middle">[2,2] 4</text>
    <rect x="180" y="164" width="90" height="34" rx="4"/>
    <text x="225" y="186" text-anchor="middle">[2,3] 3</text>
    <rect x="295" y="164" width="90" height="34" rx="4"/>
    <text x="340" y="186" text-anchor="middle">[2,5] 1</text>
    <rect x="395" y="164" width="90" height="34" rx="4"/>
    <text x="440" y="186" text-anchor="middle">[3,3] 2</text>
    <rect class="fill" x="515" y="164" width="90" height="34" rx="4"/>
    <text x="560" y="186" text-anchor="middle">[3,5] 0</text>
    <line x1="80" y1="198" x2="55" y2="244"/>
    <line x1="100" y1="198" x2="160" y2="244"/>
    <line x1="225" y1="198" x2="270" y2="244"/>
    <rect x="5" y="244" width="100" height="34" rx="4"/>
    <text x="55" y="266" text-anchor="middle">[2,2,2] 2</text>
    <rect x="115" y="244" width="100" height="34" rx="4"/>
    <text x="165" y="266" text-anchor="middle">[2,2,3] 1</text>
    <rect class="fill" x="225" y="244" width="100" height="34" rx="4"/>
    <text x="275" y="266" text-anchor="middle">[2,3,3] 0</text>
    <line x1="55" y1="278" x2="65" y2="314"/>
    <rect class="fill" x="5" y="314" width="120" height="34" rx="4"/>
    <text x="65" y="336" text-anchor="middle">[2,2,2,2] 0</text>
    <text x="440" y="300" text-anchor="middle">box: path, then amount left</text>
    <text x="440" y="322" text-anchor="middle">shaded: an answer (0 left)</text>
    <text x="440" y="344" text-anchor="middle">children start at the parent's last coin;</text>
    <text x="440" y="366" text-anchor="middle">a coin bigger than what is left is never entered</text>
  </g>
</svg>

Look at what the tree shows that the code alone would not.

**The 3-subtree has no 2 in it.** Under [3], the only children are 3 and 5. Every
combination containing a 2 lives under [2]. So the start index does not just remove
duplicates at the end; it decides, in advance, which part of the tree owns each
answer.

**The state is rewound between siblings.** When the walk moves from [2,2,2,2] up
and over to [2,2,3], the path goes from four coins back to two and then to three.
No copy is made. Every call pops exactly what it pushed, so the parent [2,2] finds
its path exactly as it left it and can try its next child.

**The prune happens before the call.** Row 3 refuses 5 without creating [2,2,5].
Had the test been "at the start of each call, if left < 0, return", the node would
have been created, entered and abandoned, which costs a call per refused child.
Testing the child is one comparison.

### A second trace: equal values in the input

Candidates [1, 1, 2] (sorted), each position used at most once, target 3. Now the
children of a node start at the position *after* the last one chosen, and we watch
what happens with and without the skip rule: "skip position i if i > start and
a[i] == a[i-1]".

**Without the skip rule.**

| # | path (positions) | left | start | children | what happens |
|---|---|---|---|---|---|
| 1 | [] | 3 | 0 | pos 0 (1), pos 1 (1), pos 2 (2) | |
| 2 | [1] via pos 0 | 2 | 1 | pos 1 (1), pos 2 (2) | |
| 3 | [1,1] | 1 | 2 | pos 2: 2 > 1, break | dead end |
| 4 | [1,2] via pos 0, 2 | 0 | 3 | | **record [1,2]** |
| 5 | [1] via pos 1 | 2 | 2 | pos 2 (2) | the same situation as row 2, minus one option |
| 6 | [1,2] via pos 1, 2 | 0 | 3 | | **record [1,2] again** |
| 7 | [2] | 1 | 3 | none | dead end |

Rows 2 and 5 are both "path [1], 2 left". Row 5 can only produce things that row 2
already produced, because row 2 had every option row 5 has, and one more. The
answer [1, 2] is recorded twice.

**With the skip rule.** Rows 1 to 4 are the same. At the root, the next child is
position 1: i = 1 > start = 0 and a[1] = a[0] = 1, so it is **skipped**: "I have
already explored everything that starts with a 1 at this level." Rows 5 and 6 never
happen. Then [2] (dead end). One record.

And look at row 2's child, position 1. There i = 1, start = 1, so i > start is
false, and the second 1 *is* allowed as the second element. That is how [1, 1, ...]
combinations survive: equal values may sit at different levels of one path, but not
at the same level of two sibling paths. Hold on to that sentence; the code section
breaks it on purpose.

## From the idea to the code

The trace is the code. Here it is with a node counter, next to generate-and-filter,
so that the claims about counts are checked rather than asserted.

```python run
from itertools import product

def combination_sum(cands, target):
    cands = sorted(cands)
    res, path, nodes = [], [], 0
    def explore(start, left):                 # a node: the path so far, `left` to go
        nonlocal nodes
        nodes += 1
        if left == 0:                         # complete: record a COPY
            res.append(path[:])
            return
        for i in range(start, len(cands)):    # children: candidates from `start` on
            c = cands[i]
            if c > left:                      # sorted, so every later one is too big
                break
            path.append(c)                    # choose
            explore(i, left - c)              # explore (i, not i+1: reuse allowed)
            path.pop()                        # un-choose
    explore(0, target)
    return res, nodes

def generate_and_filter(cands, target):       # every sequence, then test
    longest, nodes, found = target // min(cands), 0, set()
    for length in range(longest + 1):
        for seq in product(cands, repeat=length):
            nodes += 1
            if sum(seq) == target:
                found.add(tuple(sorted(seq)))
    return sorted(list(t) for t in found), nodes

got, n1 = combination_sum([2, 3, 5], 8)
want, n2 = generate_and_filter([2, 3, 5], 8)
print("backtracking:", got, "nodes", n1)
print("generate and filter:", want, "sequences", n2)
assert got == want == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
assert n1 == 13 and n2 == 121

for cands, target in [([2, 3, 6, 7], 7), ([2, 3, 5], 15), ([3, 4, 7, 8], 20)]:
    got, n1 = combination_sum(cands, target)
    want, n2 = generate_and_filter(cands, target)
    assert got == want
    print("%-14s target %2d: %2d answers, %4d nodes against %6d sequences"
          % (cands, target, len(got), n1, n2))
```

Two things to notice in the output. The answers are identical, which is the proof
executed: the start index and the prune changed nothing but the speed. And the gap
grows with the target, from 13 against 121 to 57 against 5,461. The answers come
out sorted for free, because the children are tried in sorted order: the walk
visits the tree left to right, and the leftmost answers are the lexicographically
smallest. Combination Sum asks for lexicographic order; walking in order costs
nothing, sorting at the end costs a sort.

### Each line, and which part of the idea it is

| line | in plain words | idea |
|---|---|---|
| `cands = sorted(cands)` | small coins first | makes the `break` valid and the output sorted |
| `def explore(start, left)` | "I am at a node" | the node is (path, start, left); `path` is shared, the rest are arguments |
| `if left == 0: res.append(path[:])` | a complete answer | the leaf; record a copy, because `path` will keep changing |
| `for i in range(start, ...)` | the children | only coins at or after the last one: one path per answer |
| `if c > left: break` | refuse this child and all later ones | the prune, tested on the child before entering it |
| `path.append(c)` | choose | step down one edge |
| `explore(i, left - c)` | explore | the subtree below; `i` again because reuse is allowed |
| `path.pop()` | un-choose | step back up; the path is as it was before `append` |

Four boring confusions, settled.

**Why `path[:]` and not `path`?** `res.append(path)` stores a reference to the one
shared list. At the end of the search that list is empty (every push was popped),
so `res` holds several references to the same empty list. The Traps section shows
it. Record a copy, or a tuple, or a joined string.

**Why are `start` and `left` arguments, while `path` is shared?** Integers passed
as arguments restore themselves: when the call returns, the caller's `left` is
still its own `left`. A list is mutable and shared, so it needs the explicit pop.
You could pass `path + [c]` instead and skip the pop, at the price of copying the
path at every node. Both are correct; the shared list is the standard, and
the argument version is a good way to debug.

**Why is there no `if left < 0: return`?** Because no child with c > left is ever
entered, `left` never goes negative. The check at the top of the call would also
work, but it pays a call for every refused child, and it is a different place to
put the prune, not an extra safety net.

**Why `break` and not `continue`?** Because the coins are sorted. If 5 does not fit,
7 does not either. `continue` would also be correct, just slower. With *unsorted*
candidates, `break` is wrong: it would skip a small coin that comes after a big one.

### The subtle lines, both ways

The template has one argument and one line that look like details and decide what
the search means. The argument is the start index of the child. The line is the
duplicate skip. Here are both, varied on purpose.

```python run
def search(cands, target, next_start, skip=None):
    """next_start(i) says where the child's loop begins; skip picks the dup rule."""
    a, res, path = sorted(cands), [], []
    def explore(start, left):
        if left == 0:
            res.append(tuple(path))
            return
        for i in range(start, len(a)):
            if a[i] > left:
                break
            if skip == "i > start" and i > start and a[i] == a[i - 1]:
                continue                      # same value already tried at this depth
            if skip == "i > 0" and i > 0 and a[i] == a[i - 1]:
                continue                      # WRONG: also forbids a second copy below
            path.append(a[i])
            explore(next_start(i), left - a[i])
            path.pop()
    explore(0, target)
    return res

# one argument decides what is being counted
reuse   = search([1, 2], 3, lambda i: i)      # stay on i: may take it again
once    = search([1, 2], 3, lambda i: i + 1)  # move past i: each value once
ordered = search([1, 2], 3, lambda i: 0)      # restart at 0: order matters
print("explore(i)  ", reuse)
print("explore(i+1)", once)
print("explore(0)  ", ordered)
assert reuse == [(1, 1, 1), (1, 2)]
assert once == [(1, 2)]
assert ordered == [(1, 1, 1), (1, 2), (2, 1)]

# the duplicate-skip line, three ways, on [1, 1, 2] with each position used once
for target in (3, 4):
    for rule in (None, "i > 0", "i > start"):
        print("target %d, skip %-11s ->" % (target, rule), search([1, 1, 2], target, lambda i: i + 1, rule))
assert search([1, 1, 2], 3, lambda i: i + 1) == [(1, 2), (1, 2)]          # duplicate
assert search([1, 1, 2], 4, lambda i: i + 1, "i > 0") == []                # lost (1,1,2)
assert search([1, 1, 2], 3, lambda i: i + 1, "i > start") == [(1, 2)]
assert search([1, 1, 2], 4, lambda i: i + 1, "i > start") == [(1, 1, 2)]
```

**The start index.** Candidates [1, 2], target 3. Three calls differ in one
character.

- `explore(i, ...)`: the child may pick the same candidate again, never an earlier
  one. Each multiset once: (1, 1, 1) and (1, 2). Combination Sum with reuse.
- `explore(i + 1, ...)`: the child must move past it. Each subset once: (1, 2).
  Each position used at most once.
- `explore(0, ...)`: the child may pick anything. (1, 2) and (2, 1) are both built.
  That is not a bug if the problem counts *sequences*: it is
  [[p:pinterest-count-ordered-combination-sums-with-negative-values|Count Ordered Combination Sums with Negative Values]]'s
  shape (minus the negatives). It is a bug if the problem wants combinations.

The same three meanings appear in knapsack's coin-change counting, where the loop
order decides combinations against sequences; here it is one argument. Say it a
second way: the start index is how the code remembers "I have finished with every
candidate before this one". Restart at 0 and you have forgotten it.

**The skip line.** Candidates [1, 1, 2], each position once.

- No skip, target 3: (1, 2) twice. That is the duplicate from the second trace.
- Skip with `i > 0`, target 4: **nothing**. The true answer is (1, 1, 2). Here is
  the exact moment it is lost. The root picks position 0 (the first 1). Its child
  loop starts at position 1. Position 1 holds a 1, equal to position 0, and
  `i > 0` is true, so it is skipped. But it should not be: this is not a sibling
  repeating the root's choice, it is the *next level* taking the second copy. The
  path [1, 1] is never built, and (1, 1, 2) dies with it.
- Skip with `i > start`, both targets: (1, 2) once, and (1, 1, 2). At the root,
  start = 0, so position 1 is skipped (a sibling repeat). At the child, start = 1,
  so position 1 is the first option of that level and is allowed.

What does the wrong `i > 0` version accidentally compute? It never takes a second
copy of any value, anywhere. So it computes the combinations of the *distinct
values* {1, 2}, each at most once: the answer for the input with the duplicates
removed. Like the wrong loop direction in knapsack, it does not produce garbage. It
solves a different problem, one that agrees with the right answer whenever no
answer uses a value twice, which is why samples often miss it.

The rule in one line: **equal values may appear on different levels of one path;
they may not appear at the same level of two sibling paths.** `i > start` means "I
am not the first option at this level", which is exactly "a sibling has already
tried this value".

## Why it is correct

The method is simple enough that people skip the argument, and then cannot say why
a prune or a skip rule broke their answers. The argument has three parts. The state
is really restored. The search misses nothing. It produces nothing twice. Each part
names one condition on your code, and each condition is a class of bugs.

:::proof The search reports every valid answer exactly once
**Setup.** A partial answer is a sequence p of choices. For each partial answer the
code defines a list of children, the allowed next choices. Some partial answers are
complete. Write Sol(p) for the set of valid complete answers that the search *should*
report below p, that is, those that begin with p. The goal is to show that
`explore(p)` reports exactly Sol(p), each element once.

The code is correct if three conditions hold. They are conditions on how *you*
defined the children, the prune and the undo.

- **(C1) The prune is necessary.** If the code refuses a child q, then Sol(q) is
  empty. A refused child never had an answer below it.
- **(C2) The children cover and separate.** Every answer in Sol(p) goes through
  exactly one child of p. Cover: none is unreachable. Separate: none is reachable
  through two children.
- **(C3) Undo is exact.** Choose followed by un-choose leaves all shared state as it
  was.

**Lemma (restoration).** When `explore(p)` returns, the shared state is exactly as
it was when it was called. By induction on how many levels lie below p. If p is
complete, the call writes nothing (recording a copy changes no shared state). If not,
each loop iteration does choose, then a call that, by the induction hypothesis,
restores what it was given, then un-choose, which by (C3) cancels choose. Every
iteration leaves the state as it found it, so the whole loop does too. ∎

**Theorem.** If the shared state represents p when `explore(p)` is called, the call
reports every element of Sol(p) exactly once and nothing else. By induction on the
levels below p.

*Base: p is complete.* Sol(p) is {p} if p is valid and empty otherwise, and the code
records p exactly when it is valid.

*Step.* Look at each child q of p. If the prune refuses q, then by (C1) Sol(q) is
empty, so nothing is lost. Otherwise the code chooses q and calls `explore(q)`. By
the restoration lemma, the earlier siblings left no trace, so the state represents q
exactly, and by the induction hypothesis the call reports Sol(q), each once. Adding
up over all children, the call reports the union of the Sol(q). By (C2), that union
is Sol(p) and the pieces do not overlap, so each element of Sol(p) is reported once.
Nothing outside Sol(p) is reported, because everything reported below q begins with
q, which begins with p.

**Termination.** Each step down adds one choice, the depth is bounded (the target
shrinks by at least the smallest positive coin, a permutation has n slots, a grid
path has at most R x C cells), and each node has finitely many children. A finite
tree walked depth first is finished in finitely many steps. ∎
:::

The proof is worth more for its list of conditions than for its conclusion. Every
backtracking bug is one of these failing quietly.

- **(C1), a prune that is not necessary.** "Stop when the sum exceeds the target" is
  necessary when all values are positive, and not otherwise. Symptom: missing
  answers, only on inputs your samples do not contain. Note the direction: the
  prune must be *necessary* for an answer below, never required to be *sufficient*.
  A prune that keeps hopeless branches is merely slow. `prune = never` is correct.
- **(C2) cover fails** when the children forget an option: an index skipped, a
  direction not tried, the skip rule written as `i > 0`. Symptom: too few answers.
- **(C2) separation fails** when two children lead to the same answer: no start
  index for combinations, no skip rule for equal values, two empty bins treated as
  different. Symptom: duplicates, in exactly the numbers the multiplicities predict.
- **(C3) fails** when un-choose forgets something choose did: the pop, the `used`
  flag, the grid mark, a running sum kept in a shared variable. Symptom: siblings
  explore a subtree that is not theirs, and the answers depend on visiting order.
- **Termination fails** when a choice consumes nothing: a coin of value 0 with reuse
  allowed, a grid path that may revisit a cell. Symptom: `RecursionError`.

## What it costs

**The recurrence.** Let b be the most children a node has and d the depth. With no
prune, a node with k levels below it costs T(k) = w + b·T(k-1), with T(0) = l, where
w is the work at an inner node and l the work at a leaf. Unrolled,
T(d) = Θ(b^d · (w + l)). The tree has about b^d leaves, and each is visited.

**The families, counted.**

- Subsets of n elements: two children per level (in or out), depth n, 2^n leaves.
  Recording a subset copies up to n elements, so Θ(n · 2^n) in all.
- Permutations of n elements: n children at the top, n-1 below, and so on: n!
  leaves. With the copy at each leaf, Θ(n · n!).
- Combinations of k out of n: C(n, k) leaves, each copied in Θ(k).
- Grid word search: from each of R·C cells, at most 4 then 3 choices per step (you
  cannot step back onto the cell you came from), so O(R·C · 3^L) for a word of
  length L.

**Enumeration is output-sensitive.** The total size of all subsets of n elements is
n · 2^(n-1) numbers, so no algorithm that lists them can be faster than Θ(n · 2^n).
For enumeration problems, the only thing you control is the overhead per answer:
how many dead nodes you visit per answer reported.

**Pruning changes the constant, sometimes enormously, rarely the worst case.** In the
worst case a prune may never fire, and the bound stays b^d. On real inputs it fires
constantly. Generate Parentheses with n = 8 has 2^16 = 65,536 strings of length 16.
With the prune "never open more than n, never close more than you have opened" the
walk visits 6,917 nodes for 1,430 answers, against 131,071 nodes for the full tree
of strings; the block in variation F measures this.

**When the prune is also sufficient.** If every partial answer that survives the
prune really can be completed (as for parentheses: any prefix with opens <= n and
closes <= opens can be finished), then every visited node lies on a path to some
answer, and

```
nodes visited <= (number of answers) x (depth + 1)
```

The search then has *polynomial delay*: the time between two consecutive answers is
at most a polynomial. Generate-and-filter has no such bound; it may grind through
millions of dead sequences between two answers.

**Space is O(d)** plus the output: the call stack has d frames, the path has d
entries, and the tree is never stored. This is where backtracking beats breadth-first
search outright, and it is the reason iterative deepening (variation J) exists.

**The costs people forget.**

- Building a new path at each node (`explore(path + [c])`) multiplies the work by
  the depth.
- Re-checking validity from scratch at every node ("is this board still legal?")
  multiplies the inner work by the size of the board. Keep running summaries: the
  amount left, sets of used columns and diagonals, bitmasks of digits used in each
  row.
- Deduplicating at the end with a set pays to build and hash every duplicate. For
  the permutations of a string with many repeated letters, that is n! work for far
  fewer answers.
- Python's recursion limit is about 1,000 frames. A path search that can go
  10,000 deep needs an explicit stack or a raised limit.

**Numbers worth carrying.** 8! = 40,320, 10! = 3,628,800, 12! = 479,001,600: listing
permutations is comfortable up to about 10 and hopeless past 12. 2^20 is about 10^6
and 2^25 about 3.4 x 10^7: subsets are comfortable up to about 20.

## How to think about it

The template is ten lines. What makes backtracking hard is designing the tree. Ask
these, in order.

1. **What is one decision?** The letter for this digit. Whether this element is in.
   Which unused value goes in this slot. Which candidate comes next. Which neighbour
   to step to. Where the next piece of the string ends. Write it as a sentence.
2. **What must the partial answer remember so that the next decision offers only
   legal, new options?** An index (subsets, phone letters), a `used` array
   (permutations), a start index (combinations), the amount left (sums), the visited
   cells (grids), counters (opens and closes), sets of attacked columns and
   diagonals (queens).
3. **Which of the four shapes?** List, count, find one, optimise. That fixes the
   return type and whether callers must stop early.
4. **Does order inside an answer matter?** Yes: permutations, children are "anything
   unused". No: combinations, children are "from the start index on".
5. **Can the input contain equal values?** Then sort, and skip a value equal to the
   previous one at the same level (`i > start`), or, for permutations, skip a copy
   whose previous equal copy is unused.
6. **What can a partial answer already violate?** That is the prune. Then check it
   is necessary: could any completion of a refused child still be valid? Negative
   numbers, zero values and "may stop at any time" rules are where it breaks.
7. **How big is the tree?** b^d, n!, 2^n. If it is too big and the question is a
   count or an optimum, look for repeated states: if the future depends only on a
   small summary (the start index, the set used), memoise on it
   ([[memoization]], [[dp-bitmask]]).
8. **In which order should children be tried?** For sorted output, in sorted order.
   For a find-one search, the most constrained choice first (the Sudoku cell with
   fewest candidates), which never changes correctness and often changes the running
   time by orders of magnitude.

Before writing code, write three lines: **the decision**, **the state that
defines the children**, and **the prune with its reason for being safe**. If you
cannot write the third line's reason, you do not yet know whether your prune is a
bug.

### Telling it from its neighbours

- **[[dfs]]** is the traversal of a graph that exists. Backtracking is DFS over a
  tree of partial answers that you construct and destroy as you go. The tell is the
  undo: in plain reachability, a visited mark is permanent; in backtracking, it is
  removed on the way back, because another path may use that cell.
- **[[dynamic-programming]]** is backtracking where the future depends on a small
  summary of the past, so the same subtree is reached many times and can be solved
  once. If you only need a count or an optimum, ask whether two different partial
  answers can have the same future. If yes, memoise.
- **[[greedy]]** commits to each choice forever. Backtracking keeps the right to
  undo. If you can prove the first choice is always safe, you do not need the
  search.
- **[[bfs]]** finds the fewest moves and needs memory for the whole frontier.
  Backtracking (and iterative deepening) uses memory for one path.
- **[[subsets]]**, **[[permutations]]** and **[[pruning]]** each have their own
  chapter; they are the three most common shapes of this one.

## Variations

Ten variations. A to F are the six techniques of this chapter's roadmap node, and
every interview uses them. G and H are regular. I and J are less common; J (iterative
deepening) is rare in interviews but is the standard way to search huge state spaces
with little memory.

### A. Choose, explore, un-choose: a fixed set of options per level

**What changes.** Nothing; this is the template with an index as the state.
**Why.** Each level is one position of the answer, and the options at a level do
not depend on earlier choices.

**Example.** Digits `23`: level 0 chooses from `abc`, level 1 from `def`, nine
leaves. [[p:atlassian-letter-combinations-of-a-phone-number|Letter Combinations of a Phone Number]].
The choice need not be a character. In
[[p:expedia-palindrome-partitions|All Palindrome Partitions]] the decision is "where
does the next piece end": from position i, try every end j such that text[i..j] is a
palindrome, push that piece, recurse from j + 1, pop. For `aab`: pieces `a` then
`a` then `b`; or `aa` then `b`. The piece `aab` is refused because it is not a
palindrome, and that refusal is the prune.

### B. Subsets: include or exclude

**What changes.** The decision at level i is "is element i in?". Two children.
Depth n, 2^n leaves. Or, equivalently, the start-index form: every node is an
answer, and its children add one element from the start index on.

**Why two forms.** The include/exclude tree has answers only at the leaves, depth
exactly n. The start-index tree has an answer at every node and n + 1 levels of
sizes. Both list each subset once; they list them in different orders, and a
problem that fixes the order (such as [[p:temu-subsets|Subsets]], which wants
shorter subsets first) may favour one, or need a sort.

```python run
from itertools import combinations, permutations

def subsets_in_out(nums):                    # one level per element: in or out
    res, path = [], []
    def explore(i):
        if i == len(nums):
            res.append(path[:])
            return
        path.append(nums[i]); explore(i + 1); path.pop()     # in
        explore(i + 1)                                       # out
    explore(0)
    return res

def subsets_start(nums):                     # every node is an answer
    res, path = [], []
    def explore(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i]); explore(i + 1); path.pop()
    explore(0)
    return res

def perms(nums):                             # every slot: any value not yet used
    res, path, used = [], [], [False] * len(nums)
    def explore():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True; path.append(nums[i])             # choose
            explore()
            path.pop(); used[i] = False                      # un-choose both
    explore()
    return res

nums = [1, 2, 3]
a, b = subsets_in_out(nums), subsets_start(nums)
print("in/out order:   ", a)
print("start-index:    ", b)
truth = sorted(list(c) for k in range(4) for c in combinations(nums, k))
assert sorted(a) == sorted(b) == truth and len(a) == 8
p = perms(nums)
print("permutations:   ", p)
assert p == [list(x) for x in permutations(nums)] and len(p) == 6
```

**With a prune.** [[p:meta-maximum-unique-character-word-subset|Maximum Unique-Character Word Subset]]
includes or excludes each word, and a word may be included only if it shares no
letter with the words already in. Keep the letters used as a 26-bit mask; the test
is one AND ([[bit-manipulation]]). Sixteen words, 2^16 leaves at most, far fewer
after the prune. Words that repeat a letter internally are refused before the search.
See [[subsets]].

### C. Permutations: a `used` array

**What changes.** The decision at level k is "which value goes in slot k", and the
options are the values not yet used. The state is a boolean per position, set on
choose and cleared on un-choose. Both must be undone: the pop and the flag.

**Why.** A permutation uses every value once in some order, so the only thing the
future needs to know is which values are still free.

**Example.** [1, 2, 3]: 3 choices for slot 0, 2 for slot 1, 1 for slot 2: 6 leaves,
in lexicographic order if the values are sorted. That is
[[p:atlassian-permutations|Permutations]].

**With equal values.** Sort, then skip value i if it equals value i-1 and value
i-1 is *not* used: "the copies of equal values must be used left to right". For
`aab` this gives 3 permutations instead of 6.
[[p:amazon-unique-string-permutations|Unique String Permutations]] and
[[p:microsoft-enumerate-valid-clock-times|Enumerate Valid Clock Times]] (four digits,
each used once, then a filter for valid times) both need it.

**With a rule checked at placement.** [[p:goldman-sachs-alternating-parity-permutations|Alternating Parity Permutations]]:
a value may go in slot k only if its parity differs from slot k-1. Checking the rule
when placing, not at the leaf, means a bad prefix like 1, 3 is never extended. See
[[permutations]].

### D. Combinations: a start index, and skipping duplicates

**What changes.** The children start at the start index. `explore(i)` for reuse,
`explore(i + 1)` for single use. With repeated values: sort, and
`if i > start and a[i] == a[i-1]: continue`.

**Why.** Shown in the code section: the start index gives each multiset one path
(its sorted one), and the skip rule makes equal values interchangeable at one level.

**Example.** [10, 1, 2, 7, 6, 1, 5], target 8, single use: sorted
[1, 1, 2, 5, 6, 7, 10], answers [1, 1, 6], [1, 2, 5], [1, 7], [2, 6].
[[p:expedia-combination-sum-ii|Combination Sum II]],
[[p:pinterest-combination-sum-with-single-use|Combination Sum with Single-Use Values]]
and [[p:pinterest-combination-sum-with-reuse|Combination Sum with Reusable Values]]
are the three standard forms.

**With negative values.** The "c > left: break" prune is no longer necessary, so it
must go. Without it, the depth is bounded only by the number of positions (each used
once), so the search is the full 2^n subset tree with the skip rule. That is
[[p:bytedance-combination-sum-ii-negative-values|Combination Sum II With Negative Values]],
with at most 16 candidates: 65,536 subsets, which is fine.

### E. Search a grid for a word: mark on the way in, unmark on the way out

**What changes.** The decision is "which neighbour next". The state is the current
cell, the position in the word, and which cells this path has used. Mark a cell
when the path enters it; restore it when the path leaves.

**Why the unmark.** A cell may not be used twice *by one path*. A different path may
use it. If the mark stays after a failed attempt, later attempts find their cells
already taken.

```python run
def exist(board, word, restore=True):
    board = [row[:] for row in board]
    R, C = len(board), len(board[0])
    def dfs(r, c, k):                         # can word[k:] start at (r, c)?
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        board[r][c] = "#"                     # choose: this path owns the cell
        found = any(dfs(r + dr, c + dc, k + 1)
                    for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)))
        if restore:
            board[r][c] = word[k]             # un-choose: give the cell back
        return found
    hit = any(dfs(r, c, 0) for r in range(R) for c in range(C))
    return hit, ["".join(row) for row in board]

board = [list("AA"), list("AB")]
right = exist(board, "AAA")
wrong = exist(board, "AAA", restore=False)
print("restore marks:", right)
print("never restore:", wrong)
assert right == (True, ["AA", "AB"])          # top-right, left, down
assert wrong[0] is False                      # the failed tries from (0,0) ate the cells

big = [list("ABCE"), list("SFCS"), list("ADEE")]
for w, ok in [("ABCCED", True), ("SEE", True), ("ABCB", False)]:
    assert exist(big, w)[0] == ok
    print("%-7s %s" % (w, ok))
```

Trace the wrong version on the board `AA / AB` and the word `AAA`. It starts at the
top-left A and marks it. It steps right to the top-right A and marks it; from there
the only unmarked neighbour is B, so it fails, and the mark stays. Back at the
top-left, it steps down to the bottom-left A and marks it; its neighbours are B and
the marked top-left, so it fails, and the mark stays. Now three cells are `#`. The
real answer, top-right, then top-left, then bottom-left, starts at a cell that is
already marked. The search says no. The right version unmarks after each failure,
and the second start finds the path at once.

**Example.** [[p:microsoft-word-search|Word Search]] on a board of at most 6 x 6.
[[p:adobe-longest-fruit-path|Longest Fruit Path]] is the same walk without a word:
explore every simple path through fruit cells, with mark and unmark, and keep the
longest (the optimise shape). [[p:amazon-word-search-ii|Word Search II]] searches for
many words at once by walking a [[trie]] alongside the grid, so a path dies as soon
as its letters are a prefix of no word.

### F. Prune early: reject the child, not the leaf

**What changes.** The test that refuses a child is the whole algorithm. Find the
strongest rule you can prove necessary, and make it O(1) by carrying summaries.

**Why.** A refused child costs one test; a child entered costs its whole subtree.

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
            if prune and (o > n or c > o):         # (C1): no completion below
                continue
            path.append(ch)                        # choose
            explore(o, c)                          # explore
            path.pop()                             # un-choose
    explore(0, 0)
    return res, nodes

def catalan(n):
    c = 1
    for k in range(n):
        c = c * 2 * (2 * k + 1) // (k + 2)
    return c

print(" n  answers   pruned nodes   blind nodes   nodes/answer")
for n in range(1, 9):
    good, gn = generate(n, True)
    blind, bn = generate(n, False)
    assert good == blind, n                  # pruning changed nothing but speed
    assert good == sorted(good), n           # "(" before ")" gives sorted output
    assert len(good) == catalan(n), n        # the count is the Catalan number
    assert gn <= len(good) * (2 * n + 1)     # sufficient prune => bounded delay
    print("%2d %8d %14d %13d %14.1f" % (n, len(good), gn, bn, gn / len(good)))
print("n=3 ->", generate(3)[0])
```

The prune for [[p:the-walt-disney-company-generate-parentheses|Generate Parentheses]]
is two comparisons on two counters: never open more than n, never close more than
you have opened. The line `assert good == blind` is the habit worth stealing: write
the blind version, write the pruned one, and compare them on small inputs. If they
differ, your prune is not necessary.

**N-Queens.** [[p:intuit-n-queens|N-Queens]] places one queen per row; the decision
is the column. A column is refused if it is attacked: keep three sets, the used
columns, the used `row - col` diagonals and the used `row + col` anti-diagonals, so
the test is three lookups. For n = 8 the blind tree has 8^8 = 16.7 million leaves;
the pruned search visits a couple of thousand nodes.

**Graph colouring.** [[p:adobe-graph-m-coloring|Graph M-Coloring]] colours vertices
in order and refuses a colour that a coloured neighbour already has.

**Sudoku.** [[p:confluent-sudoku-puzzle-solver|Sudoku Puzzle Solver]] keeps, for each
row, column and box, the set of digits used, so a cell's candidates are found in O(1),
and fills the empty cell with the *fewest* candidates first. A cell with one
candidate is forced, so the search goes down without branching; a cell with zero
candidates means the current partial board is dead, and the search backs up at once.
Choosing the most constrained cell first does not change the answers, because (C2)
says nothing about the order of choices; it changes which choices are made early,
when a mistake is cheap to discover.

### G. Assignment into groups: break the symmetry

**What changes.** The decision is "which group does item i go into". With k groups,
k children per item.

**Why symmetry matters.** Empty groups are interchangeable. Putting the first item
into group 1 or into group 2 produces mirror-image subtrees, k! copies of every
answer in all. The fix: only ever try the *first* empty group, and skip a group whose
current sum equals that of a group already tried at this level.

**Example.** Partition [4, 3, 2, 3, 5, 2, 1] into 4 groups of sum 5: sort descending
(big items fail fast), place 5 alone, 4 with 1, 3 with 2, 3 with 2.
[[p:palo-alto-networks-equal-sum-groups|Partition into Equal-Sum Groups]] searches the
number of groups too. [[p:pinterest-optimal-account-balancing|Optimal Account Balancing]]
is a search over who settles with whom, with the same symmetry problem.

### H. Backtracking with memoisation

**What changes.** If the function returns a value (a count, a list of completions)
that depends only on a small part of the state, cache it on that part.

**Why.** Two different partial answers with the same future do the same work twice.
This is exactly how [[dynamic-programming]] is born from a search.

**Example.** [[p:amazon-word-break-ii|Word Break II]]: the sentences that complete
`s[i:]` depend only on i, not on how `s[:i]` was split. Memoise on i, and the search
does each suffix once. [[p:mathworks-beautiful-arrangement|Beautiful Arrangement]]
counts permutations with a divisibility rule; the count of ways to fill the remaining
slots depends only on the set of values used, so memoising on a bitmask gives
[[dp-bitmask]], with n <= 15 so that 2^15 sets fit.

### I. Branch and bound (optimisation)

**What changes.** Carry the best answer found so far. Refuse a child whose optimistic
estimate cannot beat it.

**Why it is still correct.** Redefine Sol(p) as "answers below p strictly better than
the best so far". The bound refuses only children with no such answer, so (C1) still
holds.

**Example.** Longest Fruit Path on a 4 x 4 grid: if the current length plus the number
of fruit cells not yet visited is no more than the best found, stop. Account
balancing: if the transfers made so far already reach the best count, stop.

### J. Iterative deepening (rare in interviews)

**The problem it solves.** Depth-first search uses O(depth) memory but can dive down a
wrong branch for a very long time, and it does not find the *shallowest* answer first.
Breadth-first search finds the shallowest answer, but stores the whole frontier, which
is O(b^d). Iterative deepening gets both: run a depth-limited backtracking search with
limit 0, then 1, then 2, and so on, until one succeeds.

**Why the repetition is cheap.** The pass with limit d redoes everything the pass with
limit d-1 did. In a tree with b children per node, the pass to depth k visits about
b^k · b/(b-1) nodes. Summing all passes from 0 to d gives at most b/(b-1) times the
last pass: twice the work for b = 2, about 11% extra for b = 10. Most of a tree lives
in its deepest level, and the deepest level is visited once.

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
        path.pop()                            # un-choose, as always
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

The first limit at which a solution appears is, by construction, the shallowest
depth that has one, so iterative deepening returns a shortest solution, like BFS,
while holding one path, like DFS. With no visited set, it cannot detect that two
paths reach the same state; to avoid looping, check only that a state does not repeat
*on the current path*, which costs O(depth) and keeps the memory bound. Reach for it
when the state space is far too big to store and the answer is shallow. When the
states fit in memory, as in Open the Lock's 10^4 states, plain [[bfs]] is simpler
and visits each state once. IDA*, which deepens on "moves so far plus an optimistic
estimate of moves left", is how puzzle solvers are written.

## Recognising it in a statement

Ordered by how much to trust them.

1. **A tiny explicit bound.** n <= 8, n <= 10, n <= 15, a 9 x 9 board, a 6 x 6 grid,
   at most 16 candidates. Combined with almost any question, this is the strongest
   signal there is.
2. **"Return all", "every", "each distinct"** followed by sequence-shaped objects:
   schedules, combinations, expressions, paths, partitions, boards.
   [[p:snowflake-find-schedules|Work Schedule]] and
   [[p:linkedin-factor-combinations|Factor Combinations]] are typical.
3. **A rule that a prefix can already violate.** "Balanced", "nondecreasing", "no
   leading zero", "each cell used at most once", "no two queens attack", "sums to the
   target" with positive values. That rule is your prune.
4. **"Use each exactly once."** A `used` array and a permutation-shaped search.
5. **"In lexicographic order."** Weak alone, but it pairs with enumeration and tells
   you to try children in sorted order rather than sort at the end.

**Disguises.**

- "Place +, - or * between digits so the expression equals the target"
  ([[p:pinterest-expression-add-operators|Expression Add Operators]]): a decision per
  gap between digits, with the running value and the last term as the state.
- "Split the string into pieces that each satisfy X": the decision is where the next
  piece ends (variation A).
- "Assign people to tasks / items to bins under constraints": variation G.
- "Is there a way to fill the board": the find-one shape with the most constrained
  cell first.

**Anti-signals.**

- **A large n with a counting question.** "How many ways, n <= 10^5" or "modulo
  10^9 + 7" is [[dynamic-programming]].
- **"Minimum number of coins"** with large amounts: DP. Backtracking finds the right
  answer and times out.
- **n <= 20 with a count or an optimum but no list**: [[dp-bitmask]].
- **"Does a path exist" in a plain graph**: [[dfs]] or [[bfs]] with a permanent visited
  set. Undoing the visited mark in a reachability search turns a linear algorithm
  into an exponential one; undo it only when different paths may legitimately reuse a
  cell.

## Traps

**Forgetting to undo one of the things choose changed.** The pop is obvious; the
`used` flag, the grid mark and the running sum are not. Symptom with a `used` array:
the search produces exactly one answer and then nothing, because every value stays
used forever. Symptom with a grid mark: the answer depends on which start cell was
tried first (shown in variation E).

**Appending the shared path itself.** `res.append(path)` stores a reference. Symptom:
the right *number* of results, all identical, usually all empty.

**Duplicates from equal input values.** Two positions with the same value are
different choices that build the same answer. Symptom: each distinct answer appears
as many times as the multiplicities allow, for instance twice for `aab`.

```python run
from itertools import permutations as itertools_permutations

def permute(s, skip_dups=True, unmark=True, copy=True):
    """Distinct permutations, with three switches for three classic bugs."""
    a = sorted(s)                       # sorting puts equal values side by side
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

**The skip rule at the wrong level.** `i > 0` instead of `i > start` in combinations.
Symptom: answers that use a value twice (like [1, 1, 6]) disappear. Shown in the code
section.

**A prune that is not necessary.** "Stop when the sum exceeds the target" with
negative values. Symptom: missing answers, only on inputs with negatives. Compare
against the unpruned search on small random inputs.

**`break` on unsorted input.** The `break` in "if c > left: break" is valid only
because the candidates are sorted. Forget the sort and a small candidate after a big
one is never tried. Symptom: missing answers that depend on the input order.

**Validating only at the leaf.** Correct by the proof (a prune that never fires is
allowed) and hopelessly slow. Symptom: right answers on samples, timeout on the real
sizes.

**Recomputing the summary from scratch.** Rescanning the path for its sum, or the
board for conflicts, at every node. Symptom: a correct solution a factor of n too slow.

**An unbounded recursion.** A choice that consumes nothing, such as a 0-valued
candidate with reuse allowed. Symptom: `RecursionError`.

**A caller that ignores a child's "found".** In the find-one shape, `dfs(child)`
returns True and the caller keeps looping. Symptom: correct answers, far too slow, or
a board overwritten after the solution was found.

## What to memorise

The template:

```python
def explore(state):
    if complete(state):
        record(copy_of(state))      # or: return True / count += 1 / update best
        return
    for choice in children(state):  # the design: one path per answer
        if not feasible(state, choice):
            continue                # test the CHILD; break if the order allows
        apply(choice)               # choose
        explore(state)              # explore
        undo(choice)                # un-choose: restore everything apply changed
```

The sentence that turns a problem into it: **the answer is a sequence of small
choices, and I can reject a partial answer before it is finished.**

The question that designs the tree: **what is one decision, and what must the partial
answer remember so that the next decision offers only legal, new options?** Index for
fixed levels, `used` for permutations, start index for combinations, marks for grids.

The habit: type `apply` and `undo` together, as a mirrored pair, before writing the
recursive call between them. And diff the pruned search against the unpruned one on
small inputs.

The rule: **a prune may keep a hopeless branch; it may never cut a hopeful one.**

The numbers: n! is fine to about n = 10; 2^n to about n = 20; iterative deepening
costs at most b/(b-1) times one full pass.

## Check yourself

:::check
Hand trace. Candidates [1, 2, 2], each position used at most once, target 3, with
the rule "skip i if i > start and a[i] == a[i-1]" and the prune "break if a[i] >
left". List every node the search visits, in order, with (path, left, start), and
say where the skip fires. Then do it again without the skip rule.
--
With the skip: (1) [] left 3, start 0. (2) [1] left 2, start 1. (3) [1,2] via
position 1, left 0: record. Back at [1], position 2: i = 2 > start = 1 and a[2] =
a[1], **skip**. (4) [2] via position 1, left 1, start 2: position 2 holds 2 > 1,
break. Back at the root, position 2: i = 2 > 0 and a[2] = a[1], **skip**. Four nodes,
one answer, [1, 2].

Without the skip: [], [1], [1,2] (record), [1,2'] (record again), [2] (dead), [2']
(start 3: no children). Six nodes, [1, 2] twice. Notice [2] and [2'] are the same
situation, "2 used, 1 left", and the second can only repeat the first.
:::

:::check
Hand trace. Distinct permutations of `aab` with the `used` array and the rule "skip
position i if a[i] == a[i-1] and not used[i-1]". Sorted, positions 0, 1, 2 hold a, a,
b. List every node, and every skip with its reason.
--
Root. Position 0 (a): used = {0}. Path [a]: position 0 used; position 1: a[1] = a[0]
and used[0] is true, so **not** skipped: path [a, a], then position 2: [a, a, b],
record `aab`. Back at [a]: position 2 (b): [a, b], then position 1: a[1] = a[0] and
used[0] is true, allowed: [a, b, a], record `aba`.

Back at the root, position 1: a[1] = a[0] and used[0] is **false**: skip, because a
path starting with the second `a` would repeat everything that started with the
first. Position 2 (b): [b]. Then position 0: [b, a]; then position 1, allowed because
used[0]: [b, a, a], record `baa`. Back at [b], position 1: used[0] is false, skip.

Nine nodes (root, a, aa, aab, ab, aba, b, ba, baa), three answers, two skips at the
root's level and one at [b]'s level. The rule's meaning: equal letters are always
used left to right, so each distinct string has one path.
:::

:::check
Hand trace. Board `ABCE / SFCS / ADEE`, word `ABCB`. Run Word Search with mark and
unmark from the top-left A, trying neighbours right, down, left, up. Where does it
fail, and why is the answer false?
--
(0,0) A matches, mark it. Right: (0,1) B matches, mark. Right: (0,2) C matches, mark.
Now we need B. Right: (0,3) is E. Down: (1,2) is C. Left: (0,1) is marked, because
this very path used it. Up: off the board. Fail, unmark (0,2). Back at (0,1): down
(1,1) F, left (0,0) marked, up off the board. Fail, unmark. Back at (0,0): down (1,0)
is S. Fail, unmark.

The other A at (2,0) has neighbours S and D, so it fails at once. Answer false. The
only B next to that C is the B the path already used, and the mark is what forbids
reusing it. Every mark is undone, so the board is unchanged at the end.
:::

:::check
Why must a prune be necessary but never needs to be sufficient? Say what goes wrong
in each direction.
--
The code uses the prune as "if this child fails the test, there is nothing below
it". That is only true if passing the test is *necessary* for having an answer
below. If the prune refuses a child that does have an answer below, the answer is
silently lost.

Sufficiency is the converse: "if the child passes, there is an answer below". The
proof never uses it. A prune that lets hopeless children through only costs time;
the search enters them, finds nothing, and comes back. In the extreme, a prune that
never fires gives the correct, slow brute force. Sufficiency is a speed property: when
it holds, every visited node leads to an answer, so the work is bounded by answers x
depth.
:::

:::check
Someone says: "Pruning never changes the complexity. It is O(b^d) with or without, so
it is a micro-optimisation." Where are they wrong?
--
They are right that the worst-case bound is the same, and wrong that this makes the
prune unimportant. The bound is a ceiling, not the running time.

Generate Parentheses for n = 8: 131,071 nodes blind, 6,917 pruned, and the ratio
grows with n. N-Queens for n = 8: 16.7 million leaves blind, a couple of thousand
nodes pruned. Sudoku without the row, column and box test tries up to 9 digits in
each of dozens of cells and does not finish; with it, most cells have one or two
candidates and it finishes at once.

And a prune that is also sufficient gives a guarantee the blind search lacks: the
time between two answers is bounded by the depth, so the search never grinds through
millions of dead strings between two results.
:::

:::check
Someone writes Combination Sum II with `if i > 0 and a[i] == a[i-1]: continue` and it
passes the sample [10, 1, 2, 7, 6, 5], target 8. Give an input where it fails, and say
what the wrong version computes.
--
The sample has no repeated value, so the skip line never fires and the code behaves
like the right one. It fails as soon as an answer must use one value twice. Take
[2, 5, 2, 1, 2], target 5, sorted [1, 2, 2, 2, 5]. The right answers are [1, 2, 2]
and [5]. With `i > 0`, the path [1, 2] (the 2 at position 1) tries the 2 at position
2 as its next element: a[2] = a[1] and 2 > 0, so it is skipped, and [1, 2, 2] is
lost. The wrong version returns only [5].

What it computes is the answer for the set of distinct values, each used at most
once, because no level may ever take a value equal to the previous position's, not
even as the first option of a new level. The fix is `i > start`: skip only a value
that a sibling at this level has already tried.
:::

:::check
Reduce this disguised problem. "Given a string of digits like `105` and a target 5,
insert `+`, `-` or nothing between digits so the expression equals the target; list
all expressions. The string has at most 10 digits." Name the decision, the state, the
size of the tree, and one prune.
--
Decision: at each position, how long is the next number (one digit, two, ...) and,
for every number but the first, which sign goes before it. Equivalently, for each of
the 9 gaps, one of `+`, `-`, nothing: 3^9 = 19,683 leaves at most, which is small.

State: the index into the string, the value of the expression so far, and the path
(the expression text). With `*` allowed (as in the full
[[p:pinterest-expression-add-operators|Expression Add Operators]]), also the last term,
so a multiplication can undo it: value - last + last * next.

Prune: a number may not have a leading zero, so after a `0` at the start of a number,
the only allowed length is 1. That rule is necessary (such numbers are invalid), so it
is safe. For `105`, target 5: `1*0+5` and `10-5`; with only `+` and `-`, just `10-5`.
:::
