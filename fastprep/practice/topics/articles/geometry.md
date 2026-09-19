# Computational Geometry Basics

> Planar geometry in an interview is almost never about angles or square roots:
> it is about two integer quantities — the cross product, which says *which
> side*, and the squared distance, which says *how far* — and about refusing to
> compute anything else.

## When you reach for it

A hundred and thirty-seven problems in this bank are geometric, which puts the
topic at #28 of 150. That number is misleading if you picture trigonometry. Read
the statements and the same handful of shapes appear over and over:

- **Extremes of a coordinate set.** *Bounding Box from Coordinates* and
  *Coordinate Bounding Box* want `minX, minY, maxX - minX, maxY - minY`: one
  pass, four running extremes.
- **A distance threshold.** *Open Restaurants in a City Range* says "squared
  Euclidean distance from the city center is at most `radius * radius`";
  *Group Sparse Points by Distance Threshold* says "strictly less than `k * k`".
  The setter has already done you the favour of squaring both sides.
- **A ranking by distance.** *K Closest Points to a Target*, *Top K Frequent
  Closest Points*. One line of geometry; the problem is selection ([[top-k]]).
- **Which side / on a line / inside a shape.** *Max Points on a Line*,
  *Do They Belong?*, *Triangle and Points*. This is the cross product, and
  nothing else.
- **Circles.** *Circles Relationship* classifies two circles into five cases;
  *Detonate Bombs with Chain Reactions* uses "centre within radius" as a graph
  edge. Both are comparisons of `d²` against `(r₁ ± r₂)²`.
- **Counting lattice points under a curve.** *Cyber Beacon Detection* counts
  integer `(x, y)` with `(x - bx)² + (y - by)² <= r²` inside a rectangle;
  *Spreading Fire (Intuit India)* counts points untouched by growing circles.
- **A metric that is not Euclidean.** *Best Meeting Point* and *Minimum Weighted
  Manhattan Travel Cost* use `|Δx| + |Δy|`; *Maximum Rhombic Area Sum* defines
  its region by Manhattan radius. These separate into two one-dimensional
  problems, which Euclidean distance never does.

The trigger, then, is: **the input is coordinates, and the question is about
position rather than about steps between cells.** That last clause is the
important half. A grid where you walk to the four neighbours is not geometry; the
coordinates are labels there, and the tool is [[grid-bfs]] or
[[matrix-traversal]].

Three anti-signals worth holding on to. *Optimal Lamp Coordinate* mentions a
radius and a number line and is a pure [[sliding-window]] problem. *Rectangle Fit
Queries* sounds like packing and reduces to the maximum smaller side and the
maximum larger side across all saved rectangles; nothing is ever placed anywhere.
And when the question is about ordering events along one axis, you want
[[intervals]] and [[sweep-line]], geometry's one-dimensional cousins.

The prerequisite is [[math]]: coordinates, gcd, and the fact that squaring is
monotone on non-negative numbers. After this, [[convex-hull]] and [[sweep-line]]
are the natural continuations, and both are built out of the primitive below.

## The idea

Stand at `A`, face `B`. Is `C` to your left, to your right, or dead ahead?

One number answers that question, for every `A`, `B`, `C`, with two
multiplications and three subtractions and no division:

```python
def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
```

Positive means `C` is to the left of the ray `A → B`; negative means right; zero
means the three points are collinear. The magnitude is twice the area of triangle
`ABC`, which is a second answer for free.

<svg viewBox="0 0 640 230" role="img" aria-label="a directed ray from A to B, with one point on its left giving a positive cross product, one on its right giving a negative one, and one on the line giving zero">
  <g>
    <line x1="80" y1="170" x2="470" y2="28"/>
    <circle class="fill" cx="80" cy="170" r="7"/>
    <text x="62" y="192">A</text>
    <circle class="fill" cx="300" cy="90" r="7"/>
    <text x="296" y="112">B</text>
    <line x1="300" y1="90" x2="318" y2="98"/>
    <line x1="300" y1="90" x2="312" y2="79"/>
    <circle cx="170" cy="55" r="7"/>
    <text x="120" y="45">C left: cross &gt; 0</text>
    <circle cx="330" cy="185" r="7"/>
    <text x="300" y="207">C right: cross &lt; 0</text>
    <circle cx="470" cy="28" r="7"/>
    <text x="486" y="33">on the line: cross = 0</text>
    <text x="20" y="20">cross(A,B,C) = (Bx-Ax)(Cy-Ay) - (By-Ay)(Cx-Ax)</text>
  </g>
</svg>

The second primitive is even smaller. To compare distances, never take a square
root:

```python
def dist2(a, b):
    dx, dy = a[0] - b[0], a[1] - b[1]
    return dx * dx + dy * dy
```

`sqrt` is monotone on non-negative numbers, so `|PQ| < |RS|` if and only if
`dist2(P, Q) < dist2(R, S)`. Every ordering, threshold and minimum is preserved.
What you give up is the *value*, and almost no problem wants the value. When one
does — *Request Routing System* and its Haversine great-circle distance — that is
the moment to switch to floating point deliberately and read
[[numerical-stability]].

So: **one sign and one comparison.** Both are exact integer arithmetic on integer
input, which means no epsilon, no tolerance, no "works on the samples". The rest
of this chapter is those two functions wearing different hats.

## Worked by hand

Take the triangle `A = (0, 0)`, `B = (4, 0)`, `C = (1, 3)` and ask whether each
of three points lies inside it, with the boundary counting as inside — the exact
rule *Do They Belong?* and *Triangle and Points* both state.

First the triangle itself: `s = cross(A, B, C) = (4)(3) − (0)(1) = 12`. Non-zero,
so the triangle is non-degenerate, and `12 / 2 = 6` is its area. Now walk the
three edges in order `A→B`, `B→C`, `C→A` for each query point.

| point | `cross(A,B,P)` | `cross(B,C,P)` | `cross(C,A,P)` | sum | signs vs `s = 12` | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `p = (1,1)` | 4 | 6 | 2 | 12 | all positive | inside |
| `q = (3,3)` | 12 | −6 | 6 | 12 | one negative | outside |
| `m = (2,0)` | 0 | 6 | 6 | 12 | one zero, rest positive | on the boundary → inside |

Work one cell with a pen to trust the rest. For `q = (3, 3)` and edge `B→C`:
`(Cx − Bx)(qy − By) − (Cy − By)(qx − Bx) = (−3)(3) − (3)(−1) = −6`. Negative:
`q` is on the far side of line `BC` from where `A` sits, and one bad edge is
enough.

Three things in that table are not visible in the code.

**The row sums are all 12.** That is the identity
`cross(B,C,P) + cross(C,A,P) + cross(A,B,P) = cross(A,B,C)`, which holds for
*every* `P` in the plane: the three numbers are the barycentric coordinates of
`P` scaled by `s`, and those sum to one. A free assertion in your tests, and the
backbone of the proof below.

**`m` lands on the boundary as a clean zero, not a near-zero.** With integer
input there is no "close to the edge"; the number is `0` or it is not. Whether a
point on an edge counts becomes a choice between `>=` and `>`, decided by reading
the statement rather than by choosing a tolerance.

**Nothing in the table assumed the triangle was listed counter-clockwise.** It
happens to be, so `s > 0` and "inside" reads as "all three non-negative". Hand it
`A, C, B` instead and every cross flips sign, including `s`; comparing each cross
against the sign of `s` rather than against zero is what makes the test immune to
vertex order. A test written as "all three are `>= 0`" is correct on half of all
inputs — exactly the kind of bug that survives the sample cases.

## Why it is correct

The triangle test looks like a recipe. It is a theorem, and the theorem explains
why the recipe has the exact shape it has.

:::proof The sign of the cross product decides the side, and three signs decide the triangle
**Notation.** For points `A`, `B`, `P` write
`f_{AB}(P) = (Bx − Ax)(Py − Ay) − (By − Ay)(Px − Ax)`, and abbreviate
`u = Bx − Ax`, `v = By − Ay`.

**Lemma 1 (it is affine).** Expanding,
`f_{AB}(P) = u·Py − v·Px + (v·Ax − u·Ay)`, which is a linear function of
`(Px, Py)` plus a constant. Affine functions commute with affine combinations:
if `α + β + γ = 1` then `f(αX + βY + γZ) = α f(X) + β f(Y) + γ f(Z)`.

**Lemma 2 (its zero set is exactly the line `AB`).** Assume `A ≠ B`, so
`(u, v) ≠ (0, 0)`. Parameterise the plane by `P = A + t(B − A) + s(−v, u)`; the
two direction vectors are non-zero and perpendicular, hence a basis, so every `P`
has unique `(t, s)`. Substituting,
`f_{AB}(P) = u(t·v + s·u) − v(t·u − s·v) = s(u² + v²)`.
Since `u² + v² > 0`, the sign of `f_{AB}(P)` is the sign of `s`. So `f_{AB}`
vanishes exactly on `s = 0`, which is the line through `A` and `B`, and it is
strictly positive on one open half-plane and strictly negative on the other.

**Theorem.** Let `s = f_{AB}(C)` and suppose `s ≠ 0`. Then `P` lies in the closed
triangle `ABC` — the convex hull of `{A, B, C}` — if and only if all three of
`s·f_{AB}(P)`, `s·f_{BC}(P)`, `s·f_{CA}(P)` are `>= 0`.

**Proof.** Because `s ≠ 0`, `C` is off the line `AB` by Lemma 2, so `A`, `B`, `C`
are affinely independent and every point `P` of the plane has *unique*
barycentric coordinates `(α, β, γ)` with `α + β + γ = 1` and
`P = αA + βB + γC`. By definition, the convex hull of `{A, B, C}` is exactly the
set of points whose barycentric coordinates are all non-negative.

Evaluate `f_{AB}` at such a `P`. By Lemma 1,
`f_{AB}(P) = α f_{AB}(A) + β f_{AB}(B) + γ f_{AB}(C) = α·0 + β·0 + γ·s = γs`,
using `f_{AB}(A) = f_{AB}(B) = 0` from Lemma 2. The cross product is invariant
under cyclic rotation of its three arguments — all three spellings equal the
determinant of the two edge vectors — so `f_{BC}(A) = f_{CA}(B) = s`, and the
same computation gives `f_{BC}(P) = αs` and `f_{CA}(P) = βs`.

Therefore `s·f_{BC}(P) = αs²`, `s·f_{CA}(P) = βs²`, `s·f_{AB}(P) = γs²`, and
since `s² > 0`, the three tested conditions are *equivalent* to `α >= 0`,
`β >= 0`, `γ >= 0`. That is precisely membership of the closed hull. ∎

**Corollary.** Adding the three identities gives
`f_{BC}(P) + f_{CA}(P) + f_{AB}(P) = (α + β + γ)s = s` for every `P`: the row
sums in the trace above. And `|s| / 2` is the triangle's area, since `α, β, γ`
are the ratios of the three sub-triangle areas to the whole.
:::

Now name what the argument leaned on, because that list is where the bugs live.

- **The signs must be exact.** Lemma 2 gives a strict trichotomy: positive,
  negative, or exactly zero. In floating point a true value of `1` can round to
  `0.0` — demonstrated below — and the trichotomy collapses. This is the
  assumption that breaks most often, and it breaks silently.
- **`s ≠ 0`.** Affine independence is what makes barycentric coordinates exist
  and be unique. On a degenerate triangle the test is not merely inaccurate, it
  is meaningless: the naive `all three >= 0` version reports *every* point in the
  plane as inside. That is why *Do They Belong?* and *Triangle and Points* both
  make "is this even a triangle?" their first return value.
- **Closed, not open.** The theorem is about `>= 0`. Swap in `> 0` and you get
  the open triangle, excluding edges and vertices. Both are one-character changes
  and both are correct answers to *different* statements.
- **Normalising by `s`, not assuming an orientation.** The proof multiplied by
  `s` for exactly this reason. Nothing anywhere assumed counter-clockwise input.
- **Two dimensions.** The cross product of two planar vectors is a scalar. In
  three dimensions it is a vector and none of this reads across, which is why
  *Starlink Beam Planner* works with dot products instead.

## What it costs

**The primitives.** `cross` is two multiplications and three subtractions;
`dist2` is two multiplications, one addition and two subtractions. Both are
`O(1)` — but only while the integers stay machine-sized. With coordinates bounded
by `10⁹`, a difference is at most `2 × 10⁹`, a product at most `4 × 10¹⁸`, and a
cross product at most `8 × 10¹⁸`, which fits under `2⁶³ − 1 ≈ 9.22 × 10¹⁸` with
about 13% to spare. That is why so many statements here end with "use signed
64-bit arithmetic for squared distances". Python has no such limit, but the cost
is no longer constant once the numbers leave a machine word ([[big-integers]]);
cubes of `10⁹`-sized coordinates do leave it.

**Brute force over pairs.** Every "compare all points" algorithm costs
`C(n, 2) = n(n − 1)/2 ≈ n²/2` primitive evaluations. Put the constraints into
that formula and the intended solution announces itself:

| problem | `n` | pairs | verdict |
| --- | --- | --- | --- |
| *Max Points on a Line* | 300 | 44,850 | brute force over pairs is free |
| *Count Connected Point Clusters* | 2,000 | ~2 × 10⁶ | fine — the report notes the interviewer preferred it |
| *Closest Pair of Points* | 100,000 | 5 × 10⁹ | hopeless |

**Max points on a line.** For each of the `n` anchors, classify the other
`n − 1` points by the direction of the vector to them and take the largest
bucket: `Θ(n²)` directions, each reduced by a gcd at `O(log C)` and hashed
([[hash-tables]]), so `Θ(n² log C)` time and `O(n)` space. Testing every triple
instead is `C(n, 3) ≈ n³/6`, which at `n = 300` is 4.5 million against 90
thousand.

**Closest pair by sweeping.** Sort by `x`, then scan left to right keeping a
window of the points whose `x` is within the current best distance `δ`, stored
sorted by `y`. For each new point, only active points whose `y` is within `δ` can
beat the record. How many can there be? Every pair of active points is at
distance at least `δ`, or the record would already be smaller. The candidate
region is a rectangle `δ` wide and `2δ` tall; cut it into eight squares of side
`δ/2`, each of diameter `δ/√2 ≈ 0.707δ < δ`, so each holds at most one active
point. **At most 8 candidates per point**, independent of `n` — the demo below
prints the observed maximum, which is 2 on random input.

The total is one sort at `O(n log n)`, plus `n` window lookups at `O(log n)`
each, plus at most `8n` distance evaluations: `O(n log n)` time, `O(n)` space.
The classic divide-and-conquer version ([[divide-and-conquer]]) reaches the same
bound through `T(n) = 2T(n/2) + O(n) = Θ(n log n)`; the sweep is the same strip
lemma with the recursion unrolled.

<svg viewBox="0 0 640 240" role="img" aria-label="a sweep line at the current point, a window one delta wide and two delta tall behind it, and discarded points further left">
  <g>
    <line x1="430" y1="15" x2="430" y2="225"/>
    <text x="440" y="30">sweep line</text>
    <rect x="330" y="70" width="100" height="100" rx="3"/>
    <circle class="fill" cx="430" cy="120" r="7"/>
    <text x="437" y="140">p</text>
    <circle cx="360" cy="95" r="6"/>
    <circle cx="405" cy="150" r="6"/>
    <circle cx="345" cy="160" r="6"/>
    <text x="300" y="60">window: d wide, 2d tall</text>
    <text x="300" y="195">at most 8 points fit here</text>
    <circle cx="120" cy="60" r="6"/>
    <circle cx="190" cy="130" r="6"/>
    <circle cx="90" cy="180" r="6"/>
    <circle cx="230" cy="40" r="6"/>
    <text x="80" y="220">dropped: x too far left to ever help</text>
  </g>
</svg>

**The cost people forget.** A `sqrt` is tens of cycles *and* returns an inexact
double, so you pay twice; `atan2`, the reflex for angular problems such as
*Maximum Visible Drones*, costs more again and makes every later comparison
approximate. And in *Cyber Beacon Detection* the rectangle is at most `2 × 10⁵`
wide but the radius reaches `10⁹`, so looping over both axes is `10¹⁴` steps: you
must iterate the bounded axis and close the other in `O(1)` with an integer
square root, for `O(width)` total.

## The implementation

The primitives, the triangle test, and — because prose claiming that a sign test
equals hull membership deserves evidence — a check of every lattice point in a
window against exact rational barycentric coordinates.

```python run
from fractions import Fraction


def cross(a, b, c):
    """Twice the signed area of triangle abc. >0 iff c is left of ray a->b."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def dist2(a, b):
    dx, dy = a[0] - b[0], a[1] - b[1]
    return dx * dx + dy * dy


def inside(a, b, c, p):
    """True iff p lies in the CLOSED triangle abc. Rejects a degenerate abc."""
    s = cross(a, b, c)
    if s == 0:
        raise ValueError("degenerate triangle: the test would accept everything")
    return (s * cross(a, b, p) >= 0 and
            s * cross(b, c, p) >= 0 and
            s * cross(c, a, p) >= 0)


def barycentric(a, b, c, p):
    """Exact (alpha, beta, gamma) with p = alpha*a + beta*b + gamma*c."""
    s = cross(a, b, c)
    return (Fraction(cross(b, c, p), s),
            Fraction(cross(c, a, p), s),
            Fraction(cross(a, b, p), s))


A, B, C = (0, 0), (4, 0), (1, 3)
print("2 * area of ABC =", cross(A, B, C), " area =", Fraction(abs(cross(A, B, C)), 2))
for p in [(1, 1), (3, 3), (2, 0)]:
    print(p, "inside:", inside(A, B, C, p), " barycentric:", barycentric(A, B, C, p))

for x in range(-3, 8):                       # every lattice point around it
    for y in range(-3, 6):
        al, be, ga = barycentric(A, B, C, (x, y))
        assert al + be + ga == 1                                     # corollary
        assert inside(A, B, C, (x, y)) == (al >= 0 and be >= 0 and ga >= 0)
print("99 lattice points: the sign test agrees with exact rational membership")

assert inside(A, B, C, (0, 0)) and inside(A, B, C, (1, 2))           # vertex, edge
assert inside(C, B, A, (1, 1)) is True                               # reversed order
try:
    inside((0, 0), (2, 2), (5, 5), (1, 1))
except ValueError as e:
    print("degenerate input rejected:", e)
print("squared distances:", dist2((0, 0), (3, 4)), dist2((0, 0), (5, 0)), "-> equal? ",
      dist2((0, 0), (3, 4)) == dist2((0, 0), (5, 0)))
```

Three lines carry the weight.

`s * cross(a, b, p) >= 0` rather than `cross(a, b, p) >= 0`. That multiplication
is the whole orientation-independence argument from the proof, compressed into
one character; `inside(C, B, A, ...)` agreeing with `inside(A, B, C, ...)` is the
assert that proves it.

`raise ValueError` on `s == 0` rather than returning `False`. A degenerate
triangle is not a triangle that contains nothing; it is an input for which the
question has no answer, and the caller must decide what to report — scenario `0`
in *Do They Belong?*, return code `1` in *Triangle and Points*.

`Fraction(cross(b, c, p), s)` is the reference implementation: worth keeping in
your tests even though you would never ship it. It comes from the proof rather
than from the code under test, so when the two agree on ninety-nine points the
agreement means something.

## Variants you will meet

**Orientation and the convex hull.** Sort the points, then walk them keeping only
left turns — the turn test is `cross(...) > 0`. See [[convex-hull]].

**Segment intersection.** `AB` and `CD` cross properly when `C` and `D` are on
opposite sides of line `AB` *and* `A` and `B` are on opposite sides of line `CD`:
four cross products, two sign comparisons. The collinear case (all four zero)
degenerates into a one-dimensional overlap test per axis. Many segments at once
is a [[sweep-line]] problem.

**Point in a polygon.** Ray casting: shoot a ray right from `P` and count the
edges it crosses, `O(n)` per query, inside iff the count is odd. For a convex
polygon, [[binary-search]] on the angular wedge from vertex zero gives `O(log n)`
per query after an `O(n)` setup.

**Polygon area and lattice points.** The shoelace formula sums `cross` over
consecutive vertices about any origin; the triangle case is `s` above. Pick's
theorem turns that area into an interior lattice count: `A = i + b/2 − 1`.

**Circles.** Everything is a comparison of `d² = dist2(c₁, c₂)` with `(r₁ + r₂)²`
and `(r₁ − r₂)²`. Greater than the first: disjoint outside. Equal: touching.
Between: intersecting. Below the second: one inside the other, concentric when
`d² = 0`. *Circles Relationship* is that five-way ladder, in integers.

**Manhattan and Chebyshev.** `|Δx| + |Δy|` separates: the total cost over many
points is the `x`-cost plus the `y`-cost, so each axis is an independent
one-dimensional problem, each minimised at a median. That is all of *Best Meeting
Point*. The rotation `(u, v) = (x + y, x − y)` turns Manhattan distance into
Chebyshev distance `max(|Δu|, |Δv|)`, converting a diamond into an axis-aligned
square — the manoeuvre behind *Maximum Rhombic Area Sum*, where a rhombus of
cells becomes a shape you can sum with diagonal [[prefix-sums]].

**Distance thresholds as graph edges.** *Count Connected Point Clusters*,
*Group Sparse Points by Distance Threshold* and *Detonate Bombs with Chain
Reactions* build a graph whose edge predicate is geometric, then ask a pure graph
question. The geometry is one line; the answer is [[union-find]] or [[bfs]].
Watch the direction: *Detonate Bombs* gives each bomb its own radius, so its
edges are one-way.

**Angular sweeps.** *Maximum Visible Drones* asks for the densest sector of a
given angular width. Sort the directions, append the list again with `+360°`, and
run [[two-pointers]] over it. Drones coincident with the viewer are a separate,
always-counted bucket — a case the statement calls out explicitly, and the kind
of thing angular code gets wrong first.

**Lattice counting under a circle.** For each `x` in the bounded range, the valid
`y` form one interval `[cy − h, cy + h]` with `h = isqrt(r² − (x − cx)²)`, cut
down to the rectangle's `y`-range. *Cyber Beacon Detection* and *Spreading Fire
(Intuit India)* are this loop.

**Integer rasterisation.** *Rasterize a Circle with Integer Pixels* walks the
midpoint algorithm, updating a decision variable by additions only and mirroring
each pixel into eight octants. Geometry with not one division in it, which is the
reason the technique exists.

**Three dimensions.** *Starlink Beam Planner* constrains angles between vectors,
and angles between vectors are dot products: "at most 45°" becomes `u·v >= 0`
together with `2(u·v)² >= |u|²|v|²`. Squaring keeps it exact, but only after you
have checked the sign, since squaring destroys it.

```python run
import bisect, math, random


def closest_sq(points):
    """Smallest squared distance between two entries. Integer arithmetic only."""
    P = sorted(points)                            # by x, then y
    best = (P[0][0] - P[1][0]) ** 2 + (P[0][1] - P[1][1]) ** 2
    active = [(P[0][1], P[0][0])]                 # the x-window, kept sorted by y
    left, worst_probe = 0, 0
    for x, y in P[1:]:
        if best == 0:
            break                                 # duplicates: cannot do better
        while (x - P[left][0]) ** 2 > best:       # too far left to ever help
            active.pop(bisect.bisect_left(active, (P[left][1], P[left][0])))
            left += 1
        d = math.isqrt(best)                      # |dy| > d  =>  dy*dy > best
        i, probes = bisect.bisect_left(active, (y - d,)), 0
        while i < len(active) and active[i][0] <= y + d:
            qy, qx = active[i]
            best = min(best, (x - qx) ** 2 + (y - qy) ** 2)
            i, probes = i + 1, probes + 1
        worst_probe = max(worst_probe, probes)
        bisect.insort(active, (y, x))
    return best, worst_probe


def brute(pts):
    n = len(pts)
    return min((pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2
               for i in range(n) for j in range(i + 1, n))


pts = [(0, 0), (3, 4), (1, 1), (7, 7), (2, 2), (-5, 3)]
print(pts, "-> closest squared distance", closest_sq(pts)[0], "(brute force:", brute(pts), ")")

rng = random.Random(5)
for _ in range(300):
    n = rng.randint(2, 30)
    p = [(rng.randint(-20, 20), rng.randint(-20, 20)) for _ in range(n)]
    assert closest_sq(p)[0] == brute(p), p
print("300 random sets agree with the O(n^2) recount")

big = [(rng.randrange(10 ** 9), rng.randrange(10 ** 9)) for _ in range(20000)]
ans, probes = closest_sq(big)
print("20000 points:", ans, "- most candidates any single point examined:", probes)
assert probes <= 8
print("the 8-point packing bound held, as the cost argument requires")
```

The `if best == 0: break` is not a micro-optimisation. The packing argument
needed `δ > 0`; when repeated coordinates drive `best` to zero the window
collapses and every duplicate becomes a candidate, turning the sweep quadratic.
*Closest Pair of Points* states that "different entries may represent the same
coordinates", so this is a stated case, not a hypothetical.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **The statement itself says "squared Euclidean distance".** *K Closest Points
   to a Target*, *Closest Pair of Points* and *Group Sparse Points by Distance
   Threshold* all do. The setter is telling you the answer is exact integer
   arithmetic and that `sqrt` is a trap.
2. **"Use signed 64-bit arithmetic" in the constraints**, with coordinates up to
   `10⁹`. That line exists because a product of coordinates overflowed for
   somebody, which means products of coordinates are central.
3. **"Lies inside", "on the boundary", "collinear", "one straight line", "which
   side".** Cross products, every time.
4. **"Within distance r", "at most radius", "strictly less than k".** Compare
   squares. Note the third phrasing is strict and the second is not.
5. **Manhattan distance spelled out as `|r − x| + |c − y|`.** Separate the axes
   immediately; the problem is now two one-dimensional problems and probably a
   median or a prefix sum.
6. **Small `n` with coordinates** — 300 in *Max Points on a Line*, 200 in
   *Maximum Points in a Perimeter-Bounded Rectangle*, 100 in *Detonate Bombs*.
   The intended solution is `O(n²)` or `O(n³)` over candidates *defined by the
   input points*: an optimal rectangle can always be slid until its edges touch
   given points, so only `O(n²)` rectangles are worth trying.

Anti-signals, which matter as much:

- **The coordinates are cell indices and you move between neighbours.** That is
  [[grid-bfs]] or [[flood-fill]]: distance means path length, not geometry.
- **One dimension only.** *Optimal Lamp Coordinate* has a radius and a coordinate
  array and is a [[sliding-window]] problem.
- **Shapes that are never placed.** *Rectangle Fit Queries* compares sorted
  dimension pairs; no position is ever involved.
- **"Closest k"** — the distance is trivial and the work is selection
  ([[quickselect]], [[heap]], and [[custom-comparators]] for the tie-breaks these
  statements spell out in painful detail).

## Traps

**Taking a square root to compare.** Symptom: wrong answers only on large
coordinates or on exact ties, because two distances differing by one unit in the
last place of a double compare equal. Never call `sqrt` inside a comparison; if
you need a distance *value*, compute it once at the end.

**Floating point anywhere near a sign test.** Demonstrated below: three points
whose true cross product is `1` are reported collinear by doubles, because the
intermediate products are around `10¹⁸` and doubles are exact only to
`2⁵³ ≈ 9 × 10¹⁵`.

**Slopes as `dy / dx`.** Two bugs in one: division by zero on vertical lines, and
the float problem above. Use the reduced integer vector `(dx/g, dy/g)` with a
normalised sign, so `(1, 2)` and `(−1, −2)` hash to one key — otherwise each line
is counted as two directions and every answer comes out too small.

**Degenerate input.** Zero-area triangles, zero-radius circles, all points
identical. The sign test on a degenerate triangle accepts the entire plane; the
closest-pair sweep degrades to quadratic on duplicates. Both are one-line
guards, and both are stated cases in this bank rather than exotic ones.

**`int(math.sqrt(n))` instead of `math.isqrt(n)`.** For `n = 10¹⁸ − 1` the true
floor is `999999999` and the float version returns `1000000000` — off by one, on
exactly the lattice-counting problems where a single miscounted column ruins the
answer.

**Mixing up strict and non-strict thresholds.** *Open Restaurants in a City
Range* says "at most `radius * radius`"; *Group Sparse Points by Distance
Threshold* says "strictly less than `k * k`". Symptom: off-by-one counts that
appear only when a point sits exactly on the circle — which random tests rarely
produce and graders always do.

**Assuming the points are distinct.** *Count Connected Point Clusters* keeps
duplicate coordinates as separate points at distance `0`; *Top K Frequent Closest
Points* folds them into one. Opposite conventions, same-looking input.

```python run
import math
from collections import Counter


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def direction(dx, dy):
    """Canonical key for the line direction (dx, dy): reduced and sign-normalised."""
    g = math.gcd(abs(dx), abs(dy))
    dx, dy = dx // g, dy // g
    if dx < 0 or (dx == 0 and dy < 0):
        dx, dy = -dx, -dy
    return (dx, dy)


def max_on_line(points, use_float):
    best = 1
    for i, (ax, ay) in enumerate(points):
        seen = Counter()
        for j, (bx, by) in enumerate(points):
            if i == j:
                continue
            if use_float:
                key = (by - ay) / (bx - ax) if bx != ax else float("inf")
            else:
                key = direction(bx - ax, by - ay)
            seen[key] += 1
            best = max(best, seen[key] + 1)
    return best


P = [(0, 0), (10 ** 9, 10 ** 9 - 1), (10 ** 9 + 1, 10 ** 9)]
print("the three points:", P)
print("exact cross product:", cross(*P), "-> NOT collinear")
fx = (float(P[1][0]) * P[2][1]) - (float(P[1][1]) * P[2][0])
print("the same cross in doubles:", fx, "-> claims collinear")
assert cross(*P) == 1 and fx == 0.0

print("max points on a line, float slopes :", max_on_line(P, True), "(wrong)")
print("max points on a line, exact vectors:", max_on_line(P, False), "(right)")
assert max_on_line(P, True) == 3 and max_on_line(P, False) == 2

n = 10 ** 18 - 1
print("int(math.sqrt(n)) =", int(math.sqrt(n)), " math.isqrt(n) =", math.isqrt(n))
assert math.isqrt(n) ** 2 <= n < (math.isqrt(n) + 1) ** 2
assert int(math.sqrt(n)) != math.isqrt(n)
print("the float answer is one too large: it would count a whole extra lattice row")
```

Both wrong answers here are *plausible* ones. The float-slope version is the code
everybody writes first and is correct on every small hand-made test; it fails
only on large coordinates, which is exactly when the grader starts paying
attention.

## What to memorise

Two functions, one sentence, one habit.

```python
def cross(a, b, c):                     # sign: which side.  |value|: 2 * area
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def dist2(a, b):                        # order-preserving, exact, no sqrt
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
```

**The sentence** that turns a problem into them: *"Can I replace this question
about shape with the sign of a cross product or a comparison of two squared
distances?"* Side, collinearity, turning, area and containment are the first;
nearness, thresholds and ranking are the second. If neither fits, you have left
exact arithmetic, and you should say so out loud before you type.

**The habit**: before writing any comparison, ask what happens when the value is
exactly zero. Zero cross means collinear — the triangle is not a triangle, the
hull has a flat edge. Zero distance means duplicate points. Every geometry bug
worth the name is a zero that was assumed away.

Numbers worth carrying: coordinates up to `10⁹` give cross products up to
`8 × 10¹⁸`, which fits in a signed 64-bit integer but only just; a double is
exact only to `2⁵³ ≈ 9 × 10¹⁵`, so a product of two `10⁹` coordinates is already
past it. `n = 2000` points is 2 million pairs and fine; `n = 10⁵` is 5 billion
and is not.

## Check yourself

:::check
Why does comparing `s * cross(a, b, p) >= 0` for all three edges test membership
of the triangle, rather than just testing three unrelated half-planes?
--
Because the three quantities are not unrelated: they are the barycentric
coordinates of `p` scaled by the same constant `s`. The proof shows
`cross(a, b, p) = γs`, `cross(b, c, p) = αs`, `cross(c, a, p) = βs` where
`p = αa + βb + γc` and `α + β + γ = 1`.

Multiplying by `s` turns each test into `αs² >= 0`, and since `s² > 0` that is
just `α >= 0`. So the three conditions together say exactly "all barycentric
coordinates are non-negative", which is the definition of the convex hull of the
three vertices. The barycentric reading is what makes the intersection of three
half-planes provably *equal* to the triangle rather than merely a superset.
:::

:::check
Someone says: "I sort points by `math.sqrt(x*x + y*y)` because squared distances
would give a different order — squaring is not order-preserving." Where are they
wrong, and is there any case where they have a point?
--
They are wrong about the mathematics. Squaring *is* strictly increasing on
non-negative numbers, and a Euclidean distance is never negative, so
`d₁ < d₂ ⟺ d₁² < d₂²`. Any ordering, extremum or threshold computed from
squared distances is identical to the one computed from distances — and the
squared version is exact integer arithmetic, while `sqrt` returns a rounded
double that on large coordinates reports two genuinely different distances as
equal, breaking the tie rules *K Closest Points to a Target* spells out.

Where they would have a point: if the problem asks for the *value* — a sum of
distances, say, since `sqrt(a) + sqrt(b)` is not recoverable from `a + b`. The
great-circle distances in *Request Routing System* really do need floating point.
The rule is: compute roots for output, never for comparison.
:::

:::check
*Cyber Beacon Detection* counts integer points inside both a rectangle and a
circle, with `x2 - x1 <= 2 * 10⁵` but the radius up to `10⁹`. Give an algorithm
and its cost, and say why the obvious double loop fails.
--
The rectangle is narrow in `x` and unbounded in `y`, and the radius is huge, so
the region can hold on the order of `10¹⁴` points: you cannot enumerate them, and
you cannot loop over `y` because nothing bounds its range.

Loop over `x` from `x1` to `x2` — at most `2 × 10⁵` iterations. For a fixed `x`,
let `rem = r² − (x − bx)²`. If `rem < 0` the column is empty. Otherwise the
circle admits exactly the `y` with `|y − by| <= sqrt(rem)`, that is
`y ∈ [by − h, by + h]` with `h = isqrt(rem)`. Intersect with `[y1, y2]` and add
`max(0, min(hi₁, hi₂) − max(lo₁, lo₂) + 1)`.

Cost: `O(x2 − x1)` iterations, each `O(1)` given an integer square root. Use
`math.isqrt`, not `int(math.sqrt(...))`: at `10¹⁸` the float version is off by
one, and an off-by-one in `h` miscounts two whole rows in that column.
:::

:::check
*Best Meeting Point* asks for the cell minimising the total Manhattan distance to
all homes. Why can you solve the rows and the columns independently, and why is a
median optimal in each?
--
**Separability.** The cost `Σᵢ (|rᵢ − x| + |cᵢ − y|)` splits as
`Σᵢ |rᵢ − x| + Σᵢ |cᵢ − y|`; the first sum depends only on `x`, the second only
on `y`, so minimising the total is minimising each independently. This is a
property of the `L¹` metric. The Euclidean cost `Σ √((rᵢ−x)² + (cᵢ−y)²)` does not
split, which is why its version of this problem — the geometric median — has no
closed form at all.

**Median.** Let `f(x) = Σ |rᵢ − x|`. Moving `x` right by one changes `f` by
`(#{rᵢ <= x} − #{rᵢ > x})`: homes at or left of `x` get one unit further, homes
strictly right get one unit nearer. That difference is non-decreasing in `x`, so
`f` is convex and piecewise linear, and its slope first turns non-negative
exactly when half the homes lie at or below `x` — the median. Note it is the
median of the *multiset of home coordinates*, not the middle of the grid.
:::

:::check
A candidate solving *Max Points on a Line* writes: "for each pair of points,
count how many of the other points are collinear with them — `O(n³)`, but
`n <= 300` so it passes." Where are they wrong about the algorithm, and where are
they right?
--
They are right that it passes: `C(300, 3) ≈ 4.5 × 10⁶` cross products is a
second or so even in Python, and a correct slow answer beats an incorrect fast
one.

They are wrong that it is the natural algorithm. Fix one anchor and the question
becomes "which of the other `n − 1` points lie in the same *direction* from the
anchor?", which a hash map answers in one pass — `O(n²)` total, fifty times fewer
operations, and it hands you the lines themselves rather than just a count.

They are also at risk on a detail their version hides. The direction key must be
a gcd-reduced vector with a normalised sign, so that `(2, 4)`, `(1, 2)` and
`(−1, −2)` are one key. Get that wrong and the map splits each line in two and
the reported maximum is silently too small.
:::

:::check
Why is *Detonate Bombs with Chain Reactions* not a union-find problem, even
though *Count Connected Point Clusters* — which also connects points by a
distance threshold — is?
--
Because the relation is not symmetric. In *Count Connected Point Clusters* two
points are connected when their distance is at most one global `r`, so "`i`
connects to `j`" and "`j` connects to `i`" are the same statement — an
equivalence relation, which is what [[union-find]] maintains.

In *Detonate Bombs* each bomb has its *own* radius. Bomb `i` detonates `j` when
`dist2(i, j) <= radiusᵢ²`, and that can hold while `dist2(j, i) <= radiusⱼ²`
fails — a big bomb reaches a small one that cannot reach back. Merging the two
into one set would claim a chain that does not exist.

The right shape is a directed graph with `O(n²)` edges (`n <= 100`, so 10,000
edge tests) and a traversal from each starting bomb, taking the largest reachable
set: `O(n³)`, about `10⁶` operations here.
:::
