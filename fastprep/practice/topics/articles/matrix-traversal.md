# Matrix Traversal

> A matrix problem is rarely about the numbers in the matrix. It is about the
> index pairs: the order in which you enumerate them, and the permutation of
> them you are being asked to perform.

## When you reach for it

Three hundred and twelve problems in this bank use matrix traversal, which puts
it at #14 of 150 topics — a grid is the cheapest way to give a problem structure
a flat array cannot: two independent coordinates, four or eight neighbours, and
a boundary.

You reach for it when the input is a rectangular grid and the answer depends on
*where* a value sits, not only on what it is. Three families cover almost all of
them.

- **Enumerate the cells in a prescribed order.** Spiral (*Spiral Matrix
  Traversal*, *Generate a Spiral Matrix*), by concentric ring (*Sort Matrix
  Borders*, *Sort Concentric Matrix Rings*), by diagonal (*Diagonal Matrix
  Iterator*), or row-major with the border left out (*Traverse Interior Matrix
  Cells in Row-Major Order*).
- **Rearrange the cells by a coordinate map.** Rotate, transpose, reflect:
  *Rotate Matrix*, *Rotate Image*, *Transform Binary Matrix*, *Matrix
  Transformation*. The values are never inspected; only their addresses change.
- **Walk from a cell to its neighbours.** *Trace an Eight-Direction Robot Until
  Blocked*, *Rover Move*, *Cleaning Robot*. Here the grid is a map and the walk
  is a simulation.

The wrong-tool signal matters more, because a great many grid problems are not
about traversal at all — the grid is merely how a graph or a DP table was drawn.

- Shortest route, fewest moves, earliest time something spreads? [[grid-bfs]] —
  *Rotten Oranges / Grid Infection BFS*, *Minimum Time to Spread Through a Grid*.
  The traversal is only the adjacency relation; the algorithm is the queue.
- Connected regions, islands, areas? [[flood-fill]] — *Number of Islands*,
  *Max Area of Island*.
- Best path under a cost, moving only right and down? [[dp-2d]] — *Minimum Path
  Sum*, *Maximum-Value Grid Path*.
- Many queries for the sum of a sub-rectangle? [[prefix-sums]] — *Matrix Region
  Sum*, *Sub-matrix Sums*.
- Rows and columns already sorted? Scanning is the mistake: *Search a Row-Major
  Sorted Matrix* is [[binary-search]] over the flattened index, and *Staircase
  Search In A Sorted Matrix* walks in from a corner in O(m + n).

What survives those subtractions — the order, the coordinate algebra, the
bounds — is this chapter, and it is also the part of all those other algorithms
where the bugs actually live.

## The idea

Two mental images, one per half of the topic, both about addresses rather than
values.

### Enumerating is shrinking a region

Do not think of a traversal as a path. Think of it as a *set of cells you have
not visited yet*, which every step must make smaller, and which must be a shape
you can describe in a few integers.

For the spiral that shape is a rectangle, and the few integers are its four
walls: `top`, `bottom`, `left`, `right`. One turn around the spiral is four
passes — the top row left to right, the right column top to bottom, the bottom
row right to left, the left column bottom to top — and after each pass the wall
you just consumed moves inward by one. The unvisited region is always a
rectangle, it always shrinks, and the spiral finishes when it is empty.

<svg viewBox="0 0 420 240" role="img" aria-label="a four by five grid with the spiral path drawn through the cell centres and the four walls labelled">
  <g>
    <line x1="100" y1="40" x2="300" y2="40"/>
    <line x1="100" y1="80" x2="300" y2="80"/>
    <line x1="100" y1="120" x2="300" y2="120"/>
    <line x1="100" y1="160" x2="300" y2="160"/>
    <line x1="100" y1="200" x2="300" y2="200"/>
    <line x1="100" y1="40" x2="100" y2="200"/>
    <line x1="140" y1="40" x2="140" y2="200"/>
    <line x1="180" y1="40" x2="180" y2="200"/>
    <line x1="220" y1="40" x2="220" y2="200"/>
    <line x1="260" y1="40" x2="260" y2="200"/>
    <line x1="300" y1="40" x2="300" y2="200"/>
    <polyline points="120,60 280,60 280,180 120,180 120,100 240,100 240,140 160,140" fill="none" stroke-width="3"/>
    <circle class="fill" cx="120" cy="60" r="6"/>
    <circle class="fill" cx="160" cy="140" r="6"/>
    <text x="200" y="28" text-anchor="middle">top</text>
    <text x="200" y="220" text-anchor="middle">bottom</text>
    <text x="94" y="124" text-anchor="end">left</text>
    <text x="306" y="124">right</text>
    <text x="200" y="236" text-anchor="middle">every pass consumes one wall and moves it inward</text>
  </g>
</svg>

The same stance handles the rest of the family: a ring traversal is this with
the loop stopped after one turn, a diagonal traversal keeps `r + c` constant, an
interior scan is row-major with the region shrunk once at the start. Name the
region, then check that every step removes part of it and adds nothing back.

### Rearranging is following a permutation

A rotation does not compute anything. It is a bijection on the `n²` addresses.
Take a quarter turn clockwise: it carries the top-left corner to the top-right,
and in general the cell at row `i`, column `j` lands at row `j`, column
`n - 1 - i`. Call that map `σ(i, j) = (j, n - 1 - i)`.

Because `σ` is a permutation, it splits the addresses into disjoint cycles, and
applying it in place means moving one whole cycle at a time: stash one cell in a
temporary, shift the other three, drop the temporary at the end. Apply `σ` four
times and you are back where you started, so every cycle has length 1, 2 or 4,
and the only fixed point is the centre of an odd-sized matrix. That is why an
in-place rotation is a double loop over `n // 2` rows and `(n + 1) // 2`
columns: that rectangle holds exactly one representative of every 4-cycle.

<svg viewBox="0 0 360 240" role="img" aria-label="a four by four grid with four marked cells forming one rotation cycle joined by arrows">
  <g>
    <line x1="80" y1="40" x2="240" y2="40"/>
    <line x1="80" y1="80" x2="240" y2="80"/>
    <line x1="80" y1="120" x2="240" y2="120"/>
    <line x1="80" y1="160" x2="240" y2="160"/>
    <line x1="80" y1="200" x2="240" y2="200"/>
    <line x1="80" y1="40" x2="80" y2="200"/>
    <line x1="120" y1="40" x2="120" y2="200"/>
    <line x1="160" y1="40" x2="160" y2="200"/>
    <line x1="200" y1="40" x2="200" y2="200"/>
    <line x1="240" y1="40" x2="240" y2="200"/>
    <line x1="146" y1="66" x2="214" y2="94"/>
    <line x1="214" y1="94" x2="200" y2="90"/>
    <line x1="214" y1="94" x2="206" y2="82"/>
    <line x1="222" y1="112" x2="188" y2="168"/>
    <line x1="188" y1="168" x2="192" y2="154"/>
    <line x1="188" y1="168" x2="201" y2="162"/>
    <line x1="194" y1="176" x2="126" y2="148"/>
    <line x1="126" y1="148" x2="140" y2="152"/>
    <line x1="126" y1="148" x2="134" y2="160"/>
    <line x1="118" y1="128" x2="152" y2="72"/>
    <line x1="152" y1="72" x2="148" y2="86"/>
    <line x1="152" y1="72" x2="139" y2="78"/>
    <circle class="fill" cx="140" cy="60" r="11"/>
    <circle class="fill" cx="220" cy="100" r="11"/>
    <circle class="fill" cx="180" cy="180" r="11"/>
    <circle class="fill" cx="100" cy="140" r="11"/>
    <text x="180" y="232" text-anchor="middle">(0,1) to (1,3) to (3,2) to (2,0) and back: one cycle, one temporary</text>
  </g>
</svg>

Hold both pictures at once and most matrix problems become mechanical: decide
whether you are *listing* addresses in an order or *permuting* them by a map,
then write down the region or the map.

## Worked by hand

Spiral order on a 3 x 4 grid. The values are 1 to 12 in row-major order:

```
 1  2  3  4
 5  6  7  8
 9 10 11 12
```

Start with `top, bottom, left, right = 0, 2, 0, 3`. Each row of the table is one
pass, and shows the walls *after* that pass.

| step | pass | cells emitted | top | bottom | left | right |
| --- | --- | --- | --- | --- | --- | --- |
| — | start | — | 0 | 2 | 0 | 3 |
| 1 | top row, left to right | 1 2 3 4 | 1 | 2 | 0 | 3 |
| 2 | right column, top to bottom | 8 12 | 1 | 2 | 0 | 2 |
| 3 | bottom row, right to left (guard `1 <= 2` holds) | 11 10 9 | 1 | 1 | 0 | 2 |
| 4 | left column, bottom to top (guard `0 <= 2` holds) | 5 | 1 | 1 | 1 | 2 |
| 5 | top row, left to right | 6 7 | 2 | 1 | 1 | 2 |
| 6 | right column, top to bottom | — (empty range) | 2 | 1 | 1 | 1 |
| 7 | bottom row — guard `2 <= 1` **fails**, skipped | — | 2 | 1 | 1 | 1 |
| 8 | left column, bottom to top (guard `1 <= 1` holds) | — (empty range) | 2 | 1 | 2 | 1 |
| — | loop test: `top > bottom`, stop | — | 2 | 1 | 2 | 1 |

Reading off: `1 2 3 4 8 12 11 10 9 5 6 7`. Twelve cells, each once.

Three things in that trace are not visible in the code.

**Step 7 is the whole reason the guards exist.** The loop condition was checked
before step 5 and it held: the rectangle was the single row `[1..1] x [1..2]`,
containing cells 6 and 7. Step 5 then emitted that row and moved `top` past it,
leaving the rectangle empty *in the middle of the iteration*. The unguarded
bottom-row pass would have walked row `bottom = 1` from column 1 to column 1 and
emitted cell 6 a second time. A loop condition tested only at the top cannot
protect you from a body that invalidates it four times on purpose.

**Steps 6 and 8 emitted nothing, and that is fine.** An empty `range` is not a
bug and needs no guard. The guard exists to avoid *repeated* work, not empty
work; conflating the two is how people end up with four guards, or one in the
wrong place.

**The work is wildly unbalanced.** The first turn emitted 10 of the 12 cells, the
second 2. Rings shrink by two in each dimension, so the number of turns — about
`min(m, n) / 2` — tells you almost nothing about the running time. You have to
count cells, which the next section does.

## Why it is correct

Two claims deserve proofs: that the spiral enumeration visits every cell exactly
once, and that the rotation identity everybody memorises is true.

:::proof The spiral loop emits every cell exactly once
**Setup.** An `m x n` grid with `m, n >= 1`, cells `(r, c)` with `0 <= r < m`
and `0 <= c < n`. The algorithm keeps four integers and a list `out`. Write

    R = { (r, c) : top <= r <= bottom, left <= c <= right }

for the rectangle the walls delimit; `R` is empty when `top > bottom` or
`left > right`.

**Invariant.** At the top of each iteration, `out` is a repetition-free list of
exactly the cells of the grid that are *not* in `R`.

**Base case.** `top, bottom, left, right = 0, m-1, 0, n-1`, so `R` is the whole
grid and `out = []` is exactly the set of cells outside it.

**Inductive step.** Assume the invariant and that the loop test passed, so `R` is
non-empty. Let `R₀` be that rectangle and follow the four passes through the
shrinking sequence `R₀ ⊇ R₁ ⊇ R₂ ⊇ R₃ ⊇ R₄`.

*Pass 1* appends `(top, c)` for `left <= c <= right`: the top row of `R₀`,
non-empty because `R₀` has at least one column. It then increments `top`, so
`R₁ = R₀` minus that row. Each appended cell was in `R₀`, hence by the invariant
not already in `out`, and the values of `c` are distinct, so nothing is appended
twice. Afterwards `out` is exactly the complement of `R₁`.

*Pass 2* appends the right column of `R₁` — possibly empty, if pass 1 removed the
only row — then decrements `right`, giving `R₂ = R₁` minus that column.

*Pass 3* is guarded by `top <= bottom`, which says precisely that `R₂` still has
rows. If it holds, the pass appends the bottom row of `R₂`, right to left, and
sets `R₃ = R₂` minus that row: same argument again. If it fails, then `R₁` and
`R₂` have no rows at all, so `R₂` is empty, and the row indexed by `bottom` is
the row pass 1 already emitted — appending it would repeat cells. Skipping
leaves `R₃ = R₂` and the invariant untouched.

*Pass 4* is the mirror image, guarded by `left <= right`, which says `R₃` still
has columns.

At the end of the body the invariant holds for `R₄`.

**Termination.** Pass 1 always removes a row containing at least one cell, and no
pass puts a cell back into `R`. So `|R|` is a non-negative integer that strictly
decreases on every iteration, starting from `mn`: the loop runs at most `mn`
times and stops.

**Conclusion.** The loop exits when `top > bottom` or `left > right`, i.e. when
`R = ∅`. The invariant then reads: `out` is a repetition-free list of every cell
of the grid. ∎
:::

:::proof Rotating clockwise is transposing, then reversing each row
**The map.** A quarter turn clockwise carries the top-left corner to the
top-right, and in general takes the cell at row `i`, column `j` to row `j`,
column `n - 1 - i`. So if `B` is the rotation of the `n x n` matrix `A`, then
`B[j][n-1-i] = A[i][j]` for all `i, j`. Substitute `r = j` and `c = n - 1 - i`
— a bijection of `{0..n-1}²` with inverse `i = n - 1 - c`, `j = r` — to get the
*read* form:

    B[r][c] = A[n-1-c][r].

**The identity.** Define `T(A)[r][c] = A[c][r]` (transpose) and
`Rev(A)[r][c] = A[r][n-1-c]` (reverse each row). Then

    Rev(T(A))[r][c] = T(A)[r][n-1-c] = A[n-1-c][r] = B[r][c].

So transposing and then reversing each row is exactly a clockwise quarter turn.
Order matters: `T(Rev(A))[r][c] = Rev(A)[c][r] = A[c][n-1-r]`, which is the
*counter*-clockwise turn. The two operations do not commute.

**Cycle structure.** The forward map is `σ(i, j) = (j, n-1-i)`. Applying it
four times gives `(i, j) → (j, n-1-i) → (n-1-i, n-1-j) → (n-1-j, i) → (i, j)`,
so `σ⁴` is the identity and every orbit has size 1, 2 or 4. A fixed point needs
`i = j` and `j = n-1-i`, i.e. `i = j = (n-1)/2`, which exists only for odd `n`
and is the centre. An orbit of size 2 needs `σ²(i, j) = (n-1-i, n-1-j) = (i, j)`,
which forces the same centre. Every other orbit therefore has size exactly 4. ∎
:::

Now the assumptions, because that list is where the bugs come from.

- **The matrix is rectangular.** The invariant names a rectangle of addresses. A
  ragged list of lists — rows of different lengths — makes `R` meaningless, and
  Python will happily index the short rows until one is too short.
- **The guards are re-evaluated between passes.** The invariant is claimed at the
  top of the loop only. The body breaks it four times on purpose, and the guards
  are the repairs.
- **The passes run in cyclic order, each starting where the last stopped.** The
  proof is about *sets*, so it survives shuffling the four passes. What does not
  survive is that the output is a connected walk. If your problem cares about
  that, it is a separate property and deserves a separate test.
- **Nobody writes to the matrix while it is being read.** The invariant is about
  addresses, so a write cannot make a cell appear twice. It can make the value
  you emit be the *new* one. That is the *Set Matrix Zeroes* bug exactly.
- **The rotation proof assumed `m = n`.** A rotation of a rectangular matrix
  changes its shape, so there is nowhere for the extra addresses to live and no
  in-place version exists. Cisco's *Rotate Matrix* spells out that N and M are
  always equal; that note is in the statement because the code depends on it.
- **The rotation proof applies the map once, to the original.** Applying a
  sequence of transforms one at a time is correct but costs `O(q · n²)` for `q`
  queries. *Matrix Transformation* is built on that gap.

## What it costs

Count the spiral exactly rather than asymptotically. Let `W(m, n)` be the number
of cells emitted. Each turn emits the perimeter of the current rectangle and
shrinks it by one on every side, so

    W(m, n) = perim(m, n) + W(m - 2, n - 2)

with `W(m, n) = 0` when `m <= 0` or `n <= 0`, and the degenerate bases
`W(1, n) = n` and `W(m, 1) = m`. For `m, n >= 2` the perimeter of an `m x n`
rectangle is `2m + 2n - 4`, and

    mn - (m - 2)(n - 2) = mn - (mn - 2m - 2n + 4) = 2m + 2n - 4 = perim(m, n).

So by induction `W(m, n) = (mn - (m-2)(n-2)) + (m-2)(n-2) = mn`. The recurrence
does not merely give `Θ(mn)`; it gives `mn` on the nose, which is the sanity
check your test should assert. Iterations number `⌈min(m, n) / 2⌉`, each doing
`O(1)` wall arithmetic, so the total is `Θ(mn)`.

That is optimal, by an adversary argument. Suppose an algorithm prints all `mn`
values in spiral order without ever reading cell `(r, c)`. Run it again with that
one cell changed: it performs the same reads, takes the same branches and prints
the same thing, but the correct answer now differs in one position. Every cell
must be read. The only escape is to change the representation, which is what
*Sparse Matrix Multiplication* does: iterate the stored non-zeros, not the
addresses.

**Space.** The traversal is four integers, `O(1)`; the output list is `Θ(mn)`,
but that is output, not workspace. An in-place rotation needs one temporary per
4-cycle. A rectangular rotation must allocate `Θ(mn)`, because the shape
changes.

**The costs people forget.**

- *A `visited` set of tuples.* Every probe builds a `(r, c)` tuple and hashes two
  integers — asymptotically identical to a list of lists of booleans and several
  times slower, which on a `1000 x 1000` grid decides whether you finish. See
  [[hash-tables]].
- *`zip(*matrix)` and `matrix[::-1]`.* Both are `Θ(mn)` copies. Fine once,
  ruinous inside a loop over queries — which is the entire point of folding the
  transforms in *Matrix Transformation*.
- *Bounds checks.* A four-neighbour walk performs `4mn` comparisons. Padding the
  grid with a ring of blocked sentinel cells costs `Θ(m + n)` memory and removes
  every one of them, along with a whole class of bug.
- *Column-major order.* Same `Θ(mn)`, worse locality: every step touches a
  different row object. Prefer row-major when the problem lets you choose.

## The implementation

```python run
def spiral_cells(m, n):
    """Coordinates of an m x n grid in clockwise spiral order from (0, 0)."""
    top, bottom, left, right = 0, m - 1, 0, n - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):          # top row, left to right
            out.append((top, c))
        top += 1
        for r in range(top, bottom + 1):          # right column, top to bottom
            out.append((r, right))
        right -= 1
        if top <= bottom:                         # the rectangle may be empty now
            for c in range(right, left - 1, -1):  # bottom row, right to left
                out.append((bottom, c))
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):  # left column, bottom to top
                out.append((r, left))
            left += 1
    return out


def spiral(matrix):
    if not matrix or not matrix[0]:
        return []
    m, n = len(matrix), len(matrix[0])
    return [matrix[r][c] for r, c in spiral_cells(m, n)]


grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print("3x4 spiral:", spiral(grid))
assert spiral(grid) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]

for m in range(1, 8):
    for n in range(1, 8):
        cells = spiral_cells(m, n)
        assert len(cells) == m * n, (m, n)            # the recurrence said mn
        assert len(set(cells)) == m * n, (m, n)       # every cell exactly once
        for (r1, c1), (r2, c2) in zip(cells, cells[1:]):
            assert abs(r1 - r2) + abs(c1 - c2) == 1   # and it really is a walk
print("shapes 1x1 .. 7x7: each cell emitted once, consecutive cells adjacent")
print("degenerate inputs:", spiral([]), spiral([[]]), spiral([[7, 9]]))
```

Three decisions in there are doing the work.

`spiral_cells` returns **addresses, not values**. The order you visit cells in
and what you do when you get there are separate concerns, and fusing them costs
you every problem that writes back. *Sort Matrix Borders* and *Sort Concentric
Matrix Borders Clockwise* read a ring, sort it, and write it back **along the
same traversal order** — three lines with a coordinate list, a rewrite without
one.

The two `if` guards are the ones the proof needed, and nothing else in the body
is conditional. Resist the urge to add a third.

The adjacency assertion is the interesting one. A test that only checks "every
cell exactly once" is passed by row-major order, by column-major order and by a
random shuffle. Checking that consecutive cells share an edge is what makes it a
test of *spiral* order rather than of set equality.

## Variants you will meet

**Row-major and the flattening.** `idx = r * cols + c`, with
`r, c = divmod(idx, cols)` to go back — the bridge from a grid to every
one-dimensional technique. *Search a Row-Major Sorted Matrix* is
[[binary-search]] over `idx`; grid connectivity in [[union-find]] uses it to give
each cell an integer name.

**Interior only.** `for r in range(1, m - 1)` inside `for c in range(1, n - 1)`
is all of *Traverse Interior Matrix Cells in Row-Major Order*; the only thing to
get wrong is a grid with fewer than three rows, where the range must come out
empty rather than negative.

**Rings and borders.** Ring `k` is the boundary of `[k, m-1-k] x [k, n-1-k]`,
and there are `⌈min(m, n) / 2⌉` of them. Read a ring into a list, transform it,
write it back in the same order: *Sort Matrix Borders*, *Sort Concentric Matrix
Rings*.

**Diagonals.** Cells on a down-right diagonal share `r - c`; cells on an
up-right diagonal share `r + c`. There are `m + n - 1` of each, indexed by
`r - c + n - 1` and `r + c`. *Diagonal Matrix Iterator* and *Sorted Extended
Matrix Diagonals* enumerate those buckets.

**The eight symmetries.** Rotations by 0, 90, 180, 270 and the four reflections
form a group of exactly eight elements, each of them "maybe swap the two axes,
then maybe flip each one". Composing two gives another of the eight, so a long
list of transform queries collapses to one transform applied once — turning
*Matrix Transformation* from `O(q n²)` into `O(q + n²)`, which is why its
statement mentions efficiency at all. *Transform Binary Matrix* is the same fold
with a fixed script: rotate, then optionally flip vertically, then horizontally.

```python run
import random

# Every symmetry of a square is "maybe swap the axes, then maybe flip each one".
ALL = [(s, a, b) for s in (0, 1) for a in (0, 1) for b in (0, 1)]
IDENT, ROT_CW, MAIN_DIAG, ANTI_DIAG = (0, 0, 0), (1, 1, 0), (1, 0, 0), (1, 1, 1)


def source(t, n):
    """Where out[r][c] reads from, under transform t on an n x n matrix."""
    s, fr, fc = t

    def f(r, c):
        i, j = (c, r) if s else (r, c)
        return (n - 1 - i if fr else i, n - 1 - j if fc else j)
    return f


def apply_to(m, t):
    n, f = len(m), source(t, len(m))
    return [[m[f(r, c)[0]][f(r, c)[1]] for c in range(n)] for r in range(n)]


def compose(g, h):
    """The single transform equal to 'do g, then do h'."""
    fg, fh = source(g, 3), source(h, 3)
    want = {(r, c): fg(*fh(r, c)) for r in range(3) for c in range(3)}
    for t in ALL:
        ft = source(t, 3)
        if all(ft(r, c) == want[(r, c)] for r in range(3) for c in range(3)):
            return t
    raise AssertionError("the eight are not closed under composition")


for g in ALL:
    for h in ALL:
        assert compose(g, h) in ALL
print("the 8 transforms are closed under composition (64 products checked)")
print("four clockwise turns are the identity:",
      compose(compose(ROT_CW, ROT_CW), compose(ROT_CW, ROT_CW)) == IDENT)
print("main diagonal then anti diagonal gives", compose(MAIN_DIAG, ANTI_DIAG),
      "= flip both axes = rotate by 180")

rng = random.Random(3)
for n in (1, 2, 5, 6):
    mat = [[rng.randrange(100) for _ in range(n)] for _ in range(n)]
    queries = [rng.choice([ROT_CW, MAIN_DIAG, ANTI_DIAG]) for _ in range(200)]
    slow = mat
    for q in queries:
        slow = apply_to(slow, q)             # 200 full rewrites of the matrix
    folded = IDENT
    for q in queries:
        folded = compose(folded, q)          # 200 constant-time products
    assert apply_to(mat, folded) == slow, n
print("200 queries folded into one transform agree with 200 rewrites, n = 1,2,5,6")
```

`compose` identifies the product by checking it on a `3 x 3` grid. That is
enough: each of the eight maps is the same formula for every `n`, and two
distinct triples already disagree on a `3 x 3`, so agreement there pins down the
element for all sizes. The loop over all 64 products is the proof that the set is
closed — the fact the whole optimisation rests on.

**Neighbour walks.** `DIRS4 = ((1,0), (-1,0), (0,1), (0,-1))`, plus the four
diagonals for the eight-way version. *Number of Islands* and *Count Islands with
Eight-Direction Adjacency* differ by exactly that list.

**Spirals that are not rectangles.** *Generate a Spiral Matrix* writes `1..n²`
along the same walk instead of reading. *Spiral Matrix with Obstacles* breaks the
four-wall model outright: once a cell can be blocked the unvisited region is no
longer a rectangle, and the invariant says nothing. Switch models — carry a
direction, step, and turn right whenever the next cell is blocked, visited or off
the grid.

**Simultaneous update.** In *Infection Spread / Cellular Automata* and *Grid
Infection Spread Until Stable*, every cell's new state depends on its
neighbours' *old* states. Either double-buffer, or encode both generations in one
cell — `state + 2 * next_state` — and divide out at the end. That is
[[simulation]] discipline, and it is where grid simulations die.

**The grid as something else.** Weighted moves make it [[dijkstra]]
(*Minimum-Cost Path Through a Weighted Grid*); unweighted moves [[grid-bfs]];
regions [[flood-fill]]; a right-and-down cost [[dp-2d]]; repeated rectangle sums
[[prefix-sums]].

## Recognising it in a statement

In rough order of reliability:

1. **A named order**: "spiral", "clockwise", "layer", "ring", "border",
   "diagonal", "concentric". The order *is* the problem.
2. **A named transform**: "rotate by 90/180/270", "flip vertically", "reflect
   along the main diagonal", "in place" — *Transform Binary Matrix* names three
   in one sentence. Reach for the coordinate map, not for a picture.
3. **A robot with a heading**: a rover, a cleaner, a laser, a rule for turning.
   *Rover Move* and *Cleaning Robot* are simulations whose whole difficulty is
   the bounds check.
4. **A fixed-size window**: "every 3 x 3 block", "each 2 x 2 submatrix" —
   *Validate 3x3 Digit Windows*, *Count 2x2 Submatrices by Black Cells*. A double
   loop over the top-left corners, with the range bound the only hard part.
5. **The constraint line.** `n, m <= 1000` means `mn <= 10⁶` and an `O(mn)` scan
   is intended; if the product can reach `10⁸`, something must be precomputed.

Anti-signals, which are just as useful:

- "minimum number of moves", "shortest", "earliest time" — [[grid-bfs]] or
  [[multi-source-bfs]]; the traversal is only how you list neighbours.
- "connected", "region", "island", "area" — [[flood-fill]].
- "each row is sorted and each column is sorted" — searching, not scanning.
- The grid is decoration. *Find Elements Largest in Row Smallest in Column* looks
  two-dimensional and is answered by one pass for row maxima, one for column
  minima, and an intersection. When the answer depends only on per-row and
  per-column aggregates, no interesting traversal exists.

## Traps

:::warn Square test cases hide half of this topic's bugs
Swapped `(r, c)`, a transposed direction array, a missing spiral guard, a rotate
that indexes with the wrong dimension — every one of these passes on an `n x n`
input and fails on a rectangle. Test a `3 x 4` and a `4 x 3` before you believe
anything.
:::

**`grid = [[0] * n] * m`.** The outer `*` copies the *reference* to one row, so
all `m` rows are the same list. Symptom: one write changes a whole column.

**A bounds check missing its lower half.** `if r + dr < m and c + dc < n` looks
symmetric enough to trust, but in Python a negative index does not raise — it
wraps to the other end of the row. Symptom: no crash, just answers that are wrong
near the top and left edges.

**A spiral without the mid-loop guards.** Symptom: some cells emitted twice, on
some shapes — and which shapes is the nasty part, below.

**Mutating while traversing.** In *Set Matrix Zeroes* the naive "when you see a
zero, zero its row and column" plants new zeros that the rest of the scan reads
as input, and the whole matrix goes to zero. Fix it in two phases: collect the
rows and columns to clear, then clear them.

**The in-place rotation's loop bounds.** `range(n // 2)` for rows and
`range((n + 1) // 2)` for columns is not a typo: those bounds hit exactly one
representative per 4-cycle. `n // 2` for both misses the middle column on odd
`n`; `(n + 1) // 2` for both processes some cycles twice, rotating part of the
matrix by 180 degrees.

**Reading a ring one way and writing it back another.** Read clockwise, sort,
write back row by row, and the ring is scrambled.

```python run
from collections import Counter


def spiral_unguarded(m, n):
    """The same four passes, with the two mid-loop guards removed."""
    top, bottom, left, right = 0, m - 1, 0, n - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append((top, c))
        top += 1
        for r in range(top, bottom + 1):
            out.append((r, right))
        right -= 1
        for c in range(right, left - 1, -1):
            out.append((bottom, c))
        bottom -= 1
        for r in range(bottom, top - 1, -1):
            out.append((r, left))
        left += 1
    return out


for shape in [(2, 2), (5, 5), (3, 4), (3, 1)]:
    cells = spiral_unguarded(*shape)
    dupes = [c for c, k in Counter(cells).items() if k > 1]
    print("unguarded %dx%d: emitted %2d, expected %2d, repeats %s"
          % (shape[0], shape[1], len(cells), shape[0] * shape[1], dupes or "none"))
assert len(set(spiral_unguarded(5, 5))) == 25       # every square input passes
assert (1, 1) in [c for c, k in Counter(spiral_unguarded(3, 4)).items() if k > 1]

# Python's negative indices turn a missing lower bound into a silent wrong answer.
g = [[1, 2], [3, 4]]
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def neighbours_bad(g, r, c):
    m, n = len(g), len(g[0])
    return sum(g[r + dr][c + dc] for dr, dc in DIRS if r + dr < m and c + dc < n)


def neighbours_ok(g, r, c):
    m, n = len(g), len(g[0])
    return sum(g[r + dr][c + dc] for dr, dc in DIRS
               if 0 <= r + dr < m and 0 <= c + dc < n)


print("neighbour sum of (0,0):", neighbours_bad(g, 0, 0), "without '0 <=', ",
      neighbours_ok(g, 0, 0), "with it (the true answer is 3 + 2)")
assert neighbours_bad(g, 0, 0) == 10 and neighbours_ok(g, 0, 0) == 5

aliased = [[0] * 3] * 3
fresh = [[0] * 3 for _ in range(3)]
aliased[0][0] = fresh[0][0] = 1
print("[[0]*3]*3     ->", aliased, "<- one write, three rows changed")
print("comprehension ->", fresh)
assert aliased[1][0] == 1 and fresh[1][0] == 0
```

Look hard at the first block of output. The unguarded spiral is correct on
`2 x 2`, on `5 x 5`, and in fact on **every** square matrix, because a square
runs out of rows and columns on the same pass and the extra passes come out as
empty ranges. It breaks on `3 x 4` and on `3 x 1`. If your only test is a square,
this bug ships.

## What to memorise

Very little, and none of it is a formula you look up.

The four-pass spiral, which should come out of your fingers whole:

```python
top, bottom, left, right = 0, m - 1, 0, n - 1
while top <= bottom and left <= right:
    for c in range(left, right + 1): visit(top, c)
    top += 1
    for r in range(top, bottom + 1): visit(r, right)
    right -= 1
    if top <= bottom:
        for c in range(right, left - 1, -1): visit(bottom, c)
        bottom -= 1
    if left <= right:
        for r in range(bottom, top - 1, -1): visit(r, left)
        left += 1
```

The sentence that classifies a matrix problem: *"Am I listing addresses in an
order, or permuting them by a map?"* Listing means naming the unvisited region
and shrinking it; permuting means writing down where `out[r][c]` reads from and
then either allocating or following the cycles.

The habit: **write the bounds test once, as a named helper**, always with both
halves — `0 <= r < m and 0 <= c < n`. You cannot forget the `0 <=` in a function
you only wrote once.

Numbers worth carrying: a clockwise turn reads `A[n-1-c][r]`, 180 degrees reads
`A[n-1-r][n-1-c]`; there are `⌈min(m, n) / 2⌉` rings and `m + n - 1` diagonals
each way; `1000 x 1000` is `10⁶` cells — one comfortable pass in Python, not
ten.

## Check yourself

:::check
The spiral loop already tests `top <= bottom and left <= right` at the top. Why
are two more guards needed inside the body — and why does removing them still
give correct output for every square matrix?
--
Because the body deliberately breaks the loop condition. Each pass moves a wall
inward, so after the first two passes the rectangle may already be empty. Row
`bottom` is then a row that pass 1 has *already emitted*, and the third pass
would emit part of it again. The loop condition, checked only at the top, cannot
see a state that arises in the middle.

Squares hide it because a square shrinks symmetrically: the rectangle is `k x k`
at the start of every turn. When `k = 1`, pass 1 consumes the last row and leaves
`top > bottom`; pass 2's range is empty and drops `right` to `left - 1`; the
unguarded pass 3 then iterates `range(left-1, left-1, -1)`, which is empty, and
so is pass 4. Nothing repeats — by luck, not by design. On a `3 x 4` the two
dimensions run out on different passes and the luck runs out with them.
:::

:::check
A candidate says: "To rotate clockwise, transpose and reverse each row — or
reverse each row and transpose, it is the same two operations either way."
Where are they wrong?
--
Function composition is not commutative, and these two do not commute.

With `T(A)[r][c] = A[c][r]` and `Rev(A)[r][c] = A[r][n-1-c]`:

- `Rev(T(A))[r][c] = A[n-1-c][r]` — a clockwise quarter turn.
- `T(Rev(A))[r][c] = A[c][n-1-r]` — a **counter**-clockwise quarter turn.

They differ by a 180-degree rotation, so the mistake is not subtle in its
consequences and is completely invisible on a symmetric test input. The one-line
check: on `[[1, 2], [3, 4]]`, clockwise must put 3 in the top-left; if your 1
ends up there you have the other one.

The related true statement, worth keeping: reversing the *order of the rows*
(`A[::-1]`) and then transposing also gives clockwise. Two different recipes for
the same map — which is exactly why saying "reverse the rows" out loud is
dangerous.
:::

:::check
Why does an in-place clockwise rotation loop over `range(n // 2)` for rows and
`range((n + 1) // 2)` for columns, rather than `n // 2` for both?
--
Because the loop must visit exactly one cell from each 4-cycle of the map
`σ(i, j) = (j, n-1-i)`, and the asymmetric rectangle is exactly a set of
representatives.

For even `n` there are `n²/4` cycles and `n//2 = (n+1)//2`, so the two forms
agree. For odd `n` the centre is a fixed point and the remaining `n² - 1` cells
form `(n² - 1)/4` cycles. The rectangle `n//2` by `(n+1)//2` has
`((n-1)/2)·((n+1)/2) = (n² - 1)/4` cells — precisely one per cycle. Using
`n // 2` for both gives `(n-1)²/4` cells, too few, and a column of the matrix
never moves. Using `(n+1)//2` for both gives `(n+1)²/4`, too many: some cycles
get two representatives and are rotated twice.

Check it on `n = 3`: the correct rectangle is rows `{0}` by columns `{0, 1}` —
two cycles, eight cells, plus the centre that stays put. Total nine.
:::

:::check
Someone wants to solve *Set Matrix Zeroes* in one pass: "whenever I read a zero,
I zero out its row and column immediately". What goes wrong, and why does the
`O(1)`-space fix need an extra flag?
--
The zeros it writes are indistinguishable from the zeros that were in the input.
The scan reaches one of its own marks later, treats it as an original, and clears
another row and column. On most inputs the whole matrix ends up zero. This is the
assumption "nobody writes to the matrix while it is being read" from the proof
section, failing in the most literal way.

The two-phase fix collects the rows and columns first, then clears — `O(m + n)`
extra space. To reach `O(1)`, store those two sets *inside* row 0 and column 0 as
marks. The clash is the shared cell `A[0][0]`, which would have to mean both "row
0 is zeroed" and "column 0 is zeroed", so one of the two facts goes in a separate
boolean and row 0 and column 0 are handled last, after the interior has finished
reading their marks.
:::

:::check
Why must any algorithm that prints an `m x n` matrix in spiral order read all
`mn` cells — and what kind of problem escapes that bound?
--
An adversary argument. Suppose an algorithm prints the correct spiral order for
some input `A` without ever reading cell `(r, c)`. Build `A'` identical to `A`
except at `(r, c)`, where the value is different. The algorithm performs exactly
the same reads on `A'`, so it takes the same branches and prints the same output
— but the correct output for `A'` differs in the position where `(r, c)` appears.
So it is wrong on `A'`. Hence no correct algorithm can skip a cell, and `Ω(mn)`
is a lower bound that `Θ(mn)` meets.

The escape is not a faster algorithm but a different input. If the matrix arrives
as a list of non-zero entries rather than as `mn` cells — the setting of *Sparse
Matrix Multiplication* — the input size is the number of non-zeros and the bound
is in terms of *that*. When a grid bound looks unbeatable, attack the
representation, not the loop.
:::
