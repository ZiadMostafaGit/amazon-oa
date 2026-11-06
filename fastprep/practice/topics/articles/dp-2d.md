# Two-dimensional DP and Grids

> When the future depends on two positions, a cell on a board or how far you have got in each of two sequences, the state is that pair, and every two-sequence problem (common subsequence, edit distance, palindromes) turns out to be a cheapest or longest path through a grid whose cells only look up, left and diagonally back.

## The problem it solves

Here is a 3 x 3 grid of costs. You start at the top-left cell and must reach the
bottom-right cell, moving one cell right or one cell down at each step. You pay
the cost of every cell you stand on, both ends included. What is the cheapest
route?

| | col 0 | col 1 | col 2 |
|---|---|---|---|
| row 0 | 1 | 3 | 1 |
| row 1 | 1 | 5 | 1 |
| row 2 | 4 | 2 | 1 |

This is *Minimum Path Sum*, and the bank has it from Amazon, Bloomberg and
Goldman Sachs, for example [[p:amazon-minimum-path-sum|Minimum Path Sum]]. The
answer here is 7: right, right, down, down, paying 1 + 3 + 1 + 1 + 1.

The first solution anyone writes is to try every route. A route is a sequence of
2 rights and 2 downs in some order, so there are C(4, 2) = 6 of them. Add up each,
keep the cheapest. Fine for 3 x 3.

It stops being fine quickly. A route through an m x n grid is a choice of which
m-1 of its m+n-2 moves go down, so there are C(m+n-2, m-1) routes. For 10 x 10
that is 48,620. For 20 x 20 it is about 3.5·10^10. The bank's version allows 500 x
500, and C(998, 499) has about 300 digits.

The second solution anyone writes is a rule: **"from each cell, step to the
cheaper of the two neighbours."** From the start (1), right costs 3 and down costs
1, so go down. From there, right costs 5 and down costs 4, so go down again. Then
right is forced twice: 2, then 1. Total 1 + 1 + 4 + 2 + 1 = 9. The best is 7.
The cheap step down led into a corner where every way out was expensive, and the
rule could not see that coming.

What this chapter builds is the method from [[dynamic-programming]], applied when
the state needs two numbers. For the grid it gives the exact answer with one
small step per cell: 250,000 steps for 500 x 500. Then the same idea, with no new
machinery, solves problems that do not look like grids at all: the longest common
subsequence of two strings, the edit distance between them, and the longest
palindrome inside one string. The trick is to see that **a pair of positions is a
cell**, and that each of those problems is a path through a table of cells.

That chapter's ideas (state, transition, base case, order, rolling the table) are
assumed here. If "what is the least the future needs to know about the past?"
is not yet a familiar question, read it first.

### When it is the wrong tool

- **Moves in all four directions.** If you may step up and left as well as down
  and right, routes can loop, and there is no order in which every cell's
  neighbours are finished first. That is a shortest path problem: [[grid-bfs]] for
  equal step costs, [[dijkstra]] for cell costs.
- **A formula exists.** Counting routes on an open grid is C(m+n-2, m-1)
  ([[combinatorics]]). The table is still the right first step when cells can be
  blocked, but on an open grid the formula is O(m) with no table.
- **The strings are huge and the answer is tiny.** "Are these two strings at most
  one edit apart?" is a single left-to-right scan with two pointers. Building a
  10^5 x 10^5 table to answer it would be 10^10 cells.
- **One sequence has unique values.** The longest common subsequence of two
  sequences where one has no repeats is a longest *increasing* subsequence in
  disguise, solvable in O(n log n) ([[lis]]). An Amazon problem in the bank is
  exactly this (variation F).

## Build it from the brute force

We start with the slowest correct program, as always, and remove its waste. The
grid comes first because it is the easiest to picture. Then we will see that two
strings are a grid too.

### Step 1: the last move

"Try every route" can be written as decisions, and the trick, as in the 1-D
chapter, is to look at the **last** decision. Every route that ends at cell (r, c)
arrived there by one of two moves:

- from the cell **above**, (r-1, c), with a down move, or
- from the cell to the **left**, (r, c-1), with a right move.

Every route falls into exactly one of those groups. In either case, the part of
the route before the last move is a route from the start to that neighbour. So
let

> f(r, c) = the cheapest cost of a route from the start (0, 0) to the cell (r, c),
> both ends included.

Then

```
f(r, c) = grid[r][c] + min( f(r-1, c),     came from above
                            f(r, c-1) )    came from the left
f(0, 0) = grid[0][0]
a neighbour outside the grid counts as +infinity (no route comes from there)
```

The answer is f(m-1, n-1).

Read it in words: the cheapest way to stand on (r, c) is to pay for (r, c), plus
the cheapest way to stand on whichever neighbour is cheaper to reach. The
recursion does not decide "go right" or "go down" at the start, as the greedy
rule did. It decides at the **end**, when both alternatives are fully known.

### You might think: "Step to the cheaper neighbour."

We just saw this fail: it gave 9, and the best is 7. The general reason is worth
saying once. The greedy compares the next cell. The recursion compares **whole
routes** to the next cell. The cell (1, 0) costs only 1, but every route through it
must then pay 5 or 4, and the greedy never asked about that.

There is a second, subtler version of this mistake: "go in the direction whose
*row or column* is cheaper overall". It fails for the same reason, because what
matters is the cheapest route, not an average over cells you will not visit.

### You might think: "The state has to remember the route so far."

It feels as if a path problem needs the path. It needs much less. Once you stand
on (r, c), which cells will you visit next? That depends on (r, c) and nothing
else: the remaining moves are some rights and downs from here to the corner, and
which ones are allowed does not depend on how you arrived. And the cost of the
future is the sum of the future cells, which also does not depend on how you
arrived.

So two routes that both stand on (r, c) have the same best future. Only the
cheaper of the two can be part of an optimal route, and that is exactly what the
min keeps.

### You might think: "One index is enough: how many steps I have taken."

Every route reaches the corner in exactly m+n-2 steps, so "step k" looks like a
natural 1-D state. But two routes at step 2 can stand on (0, 2), (1, 1) or (2, 0),
three different places with three different futures. The step count does not say
where you are. The least the future needs is the cell: two numbers.

### Step 2: count it

How many calls does the plain recursion make? On the first row and first column a
cell has one neighbour, so the calls form a chain. Elsewhere, calls(r, c) = 1 +
calls(r-1, c) + calls(r, c-1). For the 3 x 3 grid that gives calls(1, 1) = 5,
calls(1, 2) = calls(2, 1) = 9, and calls(2, 2) = 19. Nineteen calls for nine cells.
The count grows like the number of routes, C(m+n, m), because the recursion
**is** the list of routes, read backwards from the corner: every path from the root
of its call tree to a leaf is one route.

### Step 3: notice the waste

Here is the top of the call tree for the corner of the 3 x 3 grid.

<svg viewBox="0 0 760 300" role="img" aria-label="the call tree of f(2,2) for minimum path sum on a 3 by 3 grid: f(1,2) and f(2,1) both call f(1,1), so f(1,1) appears twice and is shaded, and the second copy's subtree is dashed">
  <g>
    <rect x="340" y="15" width="80" height="30" rx="4"/>
    <text x="380" y="35" text-anchor="middle">f(2,2)</text>
    <rect x="160" y="90" width="80" height="30" rx="4"/>
    <text x="200" y="110" text-anchor="middle">f(1,2)</text>
    <rect x="520" y="90" width="80" height="30" rx="4"/>
    <text x="560" y="110" text-anchor="middle">f(2,1)</text>
    <rect x="60" y="165" width="80" height="30" rx="4"/>
    <text x="100" y="185" text-anchor="middle">f(0,2)</text>
    <rect class="fill" x="250" y="165" width="80" height="30" rx="4"/>
    <text x="290" y="185" text-anchor="middle">f(1,1)</text>
    <rect class="fill" x="430" y="165" width="80" height="30" rx="4"/>
    <text x="470" y="185" text-anchor="middle">f(1,1)</text>
    <rect x="620" y="165" width="80" height="30" rx="4"/>
    <text x="660" y="185" text-anchor="middle">f(2,0)</text>
    <rect x="60" y="240" width="80" height="30" rx="4"/>
    <text x="100" y="260" text-anchor="middle">f(0,1)</text>
    <rect x="200" y="240" width="80" height="30" rx="4"/>
    <text x="240" y="260" text-anchor="middle">f(0,1)</text>
    <rect x="300" y="240" width="80" height="30" rx="4"/>
    <text x="340" y="260" text-anchor="middle">f(1,0)</text>
    <rect x="390" y="240" width="80" height="30" rx="4" stroke-dasharray="5 4"/>
    <text x="430" y="260" text-anchor="middle">f(0,1)</text>
    <rect x="490" y="240" width="80" height="30" rx="4" stroke-dasharray="5 4"/>
    <text x="530" y="260" text-anchor="middle">f(1,0)</text>
    <rect x="620" y="240" width="80" height="30" rx="4"/>
    <text x="660" y="260" text-anchor="middle">f(1,0)</text>
    <line x1="360" y1="45" x2="210" y2="90"/>
    <line x1="400" y1="45" x2="550" y2="90"/>
    <line x1="185" y1="120" x2="110" y2="165"/>
    <line x1="215" y1="120" x2="285" y2="165"/>
    <line x1="545" y1="120" x2="475" y2="165"/>
    <line x1="575" y1="120" x2="655" y2="165"/>
    <line x1="100" y1="195" x2="100" y2="240"/>
    <line x1="280" y1="195" x2="245" y2="240"/>
    <line x1="300" y1="195" x2="335" y2="240"/>
    <line x1="460" y1="195" x2="435" y2="240" stroke-dasharray="5 4"/>
    <line x1="480" y1="195" x2="525" y2="240" stroke-dasharray="5 4"/>
    <line x1="660" y1="195" x2="660" y2="240"/>
    <text x="270" y="62" text-anchor="end">from above</text>
    <text x="490" y="62">from the left</text>
    <text x="380" y="292" text-anchor="middle">Shaded: one cell, reached twice. Every f(0,1) and f(1,0) still continues to f(0,0).</text>
  </g>
</svg>

The two shaded boxes are the same question: "what is the cheapest route to the
centre cell?" One copy was asked on the way to (1, 2), the other on the way to
(2, 1). The answer is 7 (the route 1, 1, 5) both times, and the tree computes it twice. f(0, 1) is computed three times and
f(1, 0) three times. In a 500 x 500 grid the tree has around 10^300 boxes, and
they can only carry 250,000 different labels.

### The question that unlocks it

Why did two different questions collapse into one? Because the future of a route
does not care how the route got to the centre cell. It cares about one thing:
where it is now.

**What is the least the future needs to know about the past?**

For the grid: the cell, (r, c). Two numbers. Not the route, not the cost so far.

That question is the whole chapter. Every problem in it is answered by finding
the **two** numbers that describe "where I am", and they are not always row and
column.

- For a grid, the two numbers are the row and the column.
- For **two sequences** (compare a string with another string), the two numbers
  are how far along you are in each: "I have dealt with the first i characters of
  the first string and the first j of the second."
- For **one sequence with two ends** (is this substring a palindrome?), the two
  numbers are the left and right ends of the piece still under consideration.

Say it a second way. The 1-D chapter's state was "how far along the line am I".
Here there are two lines, or one line read from both ends, and the state is "how
far along each". The table has a row for each position on the first line and a
column for each position on the second.

### Step 4 and 5: memo, then table

Cache f(r, c) the first time it is computed, and the recursion does 9 real
computations instead of 19 calls; in general m·n instead of C(m+n, m).

Then drop the recursion. f(r, c) needs f(r-1, c) (the row above) and f(r, c-1)
(the cell to the left). So fill the table **row by row, left to right inside each
row**: when you reach (r, c), the whole row above is done and the cell to your left
is done. Every arrow of the recurrence points up or left, so this order is legal.

### Step 6: one row is enough

Row r reads only row r-1. Keep one array of n numbers. Before processing row r it
holds row r-1; we rewrite it in place, left to right. When we reach column c:

- dp[c] has not been rewritten yet in this row, so it still holds row r-1: the
  cell **above**. That is the "from above" branch.
- dp[c-1] has just been rewritten, so it holds row r: the cell **to the left**.
  That is the "from the left" branch.

So `dp[c] = grid[r][c] + min(dp[c], dp[c-1])`, scanned left to right, reads exactly
the two cells it should. Here, unlike 0/1 [[knapsack]], we *want* the new value on
the left. The direction is right for the same reason the knapsack direction is
right: it makes each read see the row the recurrence names.

### Step 7: two strings are a grid

Now a problem that does not look like a grid. Given two strings, what is the
length of their **longest common subsequence** (LCS)? A subsequence keeps the
order of characters but may skip some. "ACE" is a subsequence of "ABCDE". The LCS
of "ABCBD" and "BDCAB" is 3 ("BCB").

The brute force: list every subsequence of the first string (2^n of them), check
each against the second (O(m) with two pointers), keep the longest. For two strings
of 500 characters, 2^500 is hopeless.

Look at the last decision again. Compare the **last characters** of the two
strings, a[n-1] and b[m-1].

- **They are equal.** Then they can be matched with each other, and the rest of
  the LCS is the LCS of the two strings without their last characters. (It is not
  obvious that matching them is always safe. The proof shows it.)
- **They differ.** Then they cannot be matched with each other, so in any common
  subsequence at least one of them is unused. If a[n-1] is unused, the answer is the
  LCS of a without its last character, with all of b. If b[m-1] is unused, the
  other way round. Take the better.

The state is "the first i characters of a, the first j of b". Let

> L(i, j) = the length of the LCS of a[:i] and b[:j].

```
L(i, j) = L(i-1, j-1) + 1                 if a[i-1] == b[j-1]
L(i, j) = max( L(i-1, j), L(i, j-1) )     otherwise
L(0, j) = L(i, 0) = 0                     an empty string has no common subsequence
```

The answer is L(n, m).

Look at the shape of the arrows. L(i, j) reads (i-1, j-1), (i-1, j) and (i, j-1):
the diagonal, above, and left. **It is a grid.** Row i is "i characters of a
used", column j is "j characters of b used", and the three cases are three moves:

- a **down** move drops a character of a (it is not in the LCS),
- a **right** move drops a character of b,
- a **diagonal** move, allowed only when the two characters are equal, matches
  them and scores 1.

The LCS is the route from (0, 0) to (n, m) with the **most diagonal moves**. The
same grid with a cost on every move, where the diagonal is free for equal
characters and costs 1 otherwise, and the down and right moves cost 1, gives the
**edit distance**: the cheapest route. Delete is down, insert is right, replace or
keep is diagonal. That one picture, two strings as the two edges of a grid, is the
key idea of this chapter.

### You might think: "On a mismatch, drop both characters."

It is tempting: they do not match, so neither is useful, so go to L(i-1, j-1).
Counterexample: a = "AB", b = "BA". The last characters, B and A, differ. Dropping
both leaves "A" and "B", which share nothing: answer 0. But the LCS is 1, "A" or
"B". The B at the end of a was useless *at the end of b*, but it matches the B at
the start of b. Dropping only one side keeps that possibility alive; dropping both
throws it away.

### You might think: "Match each character to its first occurrence in the other string."

A greedy: walk through a, and for each character find its next occurrence in b
after the last match. Counterexample: a = "ABCD", b = "BCDA". The greedy matches
a's A with b's last character, and then nothing is left in b: length 1. Skipping
the A gives "BCD", length 3. The greedy commits to the first match it sees, and an
early match can use up the part of b that later characters needed.

### You might think: "When the characters match, I should still try not matching them."

This instinct is *safe*, just unnecessary. Taking max(L(i-1, j-1) + 1, L(i-1, j),
L(i, j-1)) on a match gives the same numbers. The proof below shows why: dropping a
character from one string reduces the LCS by at most one, so L(i-1, j) and
L(i, j-1) can never beat L(i-1, j-1) + 1. Knowing this is useful, because in
problems where matching is *not* always safe (a weighted version, or one where
characters have costs) the three-way max is the correct form, and you should know
which one you are writing.

### Step 8: one string, both ends

The third kind of pair: positions in one string, read from both ends. What is the
length of the longest **palindromic subsequence** of s? Look at the two end
characters of the piece s[i..j].

- **They are equal**: wrap them around the best palindrome strictly inside:
  P(i, j) = P(i+1, j-1) + 2.
- **They differ**: at least one end is not used: P(i, j) = max(P(i+1, j),
  P(i, j-1)).
- **One character** is a palindrome of length 1; an empty piece has length 0.

This is LCS's recurrence with the two strings replaced by "the left end moving
right" and "the right end moving left". The arrows now point **inward** (i+1,
j-1), not up and left, and that changes the fill order: a piece can only be solved
after the shorter pieces inside it. Variation H and the Traps block show what
happens if you fill it in the usual order.

### The technique in one sentence

**2-D DP: when the future depends on two positions (a cell; how far along each of
two sequences; the two ends of one sequence), the state is the pair; each cell is
built from a few neighbours (above, left, diagonal, or the piece one shorter) that
are already filled, so the table is filled in an order where every arrow points to
a finished cell.**

And the question that produced it: **what is the least the future needs to know
about the past?** In this chapter the answer is always two numbers.

## Worked by hand

### Trace 1: the grid

Get a pen. The grid from the start, and the table f(r, c) beside it, filled row by
row:

| grid | 0 | 1 | 2 | | f | 0 | 1 | 2 |
|---|---|---|---|---|---|---|---|---|
| row 0 | 1 | 3 | 1 | | row 0 | 1 | 4 | 5 |
| row 1 | 1 | 5 | 1 | | row 1 | 2 | 7 | 6 |
| row 2 | 4 | 2 | 1 | | row 2 | 6 | 8 | **7** |

**Row 0** has no cell above, so every cell comes from the left: 1, 1 + 3 = 4,
4 + 1 = 5. **Column 0** has no cell to the left: 1, 1 + 1 = 2, 2 + 4 = 6.

**f(1, 1)**, told in full:

> "I am answering: what is the cheapest way to stand on the centre cell, cost 5?
> I arrived either from above, from (0, 1), whose cheapest route costs 4, or from
> the left, from (1, 0), whose cheapest route costs 2. Both answers are already in
> the table. The cheaper is 2. I pay 5 for this cell: 2 + 5 = 7."

**f(1, 2)**: cell cost 1; above f(0, 2) = 5, left f(1, 1) = 7. 1 + 5 = 6.
**f(2, 1)**: cell cost 2; above f(1, 1) = 7, left f(2, 0) = 6. 2 + 6 = 8.
**f(2, 2)**: cell cost 1; above f(1, 2) = 6, left f(2, 1) = 8. 1 + 6 = **7**.

Walk back to find the route: at (2, 2) the 6 came from above, go to (1, 2); the 6
there came from above (5 against 7), go to (0, 2); row 0 comes from the left all
the way. Route: (0,0), (0,1), (0,2), (1,2), (2,2). Right, right, down, down. 1 + 3
+ 1 + 1 + 1 = 7.

Notice f(1, 0) = 2. The greedy went there, and it really is the cheapest cell to
reach in row 1, column 0. The table agrees with the greedy *about that cell*. It
just never commits to it: f(2, 2) only uses f(1, 0) if a route through it wins, and
it does not.

### Trace 2: the longest common subsequence

a = "ABCBD" down the side, b = "BDCAB" across the top. Row 0 and column 0 are the
empty prefixes, all 0.

| | "" | B | D | C | A | B |
|---|---|---|---|---|---|---|
| "" | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 0 | 0 | 1 | 1 |
| B | 0 | 1 | 1 | 1 | 1 | 2 |
| C | 0 | 1 | 1 | **2** | 2 | 2 |
| B | 0 | 1 | 1 | 2 | 2 | 3 |
| D | 0 | 1 | 2 | 2 | 2 | **3** |

Each cell asks one question first: are the row letter and the column letter
equal?

- **Equal**: the cell is the diagonal (up and left) plus 1.
- **Different**: the cell is the larger of the cell above and the cell to the left.

The cell L(3, 3), row C, column C, told in full:

> "I am answering: what is the LCS of 'ABC' and 'BDC'? Their last letters are both
> C. I match them. What is left is 'AB' against 'BD', and that question was already
> answered one row up and one column left: L(2, 2) = 1 (the B). So 1 + 1 = 2."

And the cell to its right, L(3, 4), row C, column A: C and A differ. Either the C
of a is unused (look up: L(2, 4) = 1, the LCS of "AB" and "BDCA") or the A of b is
unused (look left: L(3, 3) = 2, "ABC" against "BDC"). The larger is 2.

<svg viewBox="0 0 640 250" role="img" aria-label="four cells of the LCS table for ABCBD and BDCAB: L(2,2)=1 on the diagonal, L(2,3)=1 above, L(3,2)=1 to the left; the cell L(3,3) for C against C is a match, so it takes the diagonal plus one and becomes 2">
  <g>
    <text x="235" y="35" text-anchor="middle">col D (j=2)</text>
    <text x="355" y="35" text-anchor="middle">col C (j=3)</text>
    <text x="110" y="95" text-anchor="end">row B (i=2)</text>
    <text x="110" y="185" text-anchor="end">row C (i=3)</text>
    <rect class="fill" x="180" y="60" width="110" height="60"/>
    <text x="235" y="95" text-anchor="middle">1</text>
    <rect x="300" y="60" width="110" height="60"/>
    <text x="355" y="95" text-anchor="middle">1</text>
    <rect x="180" y="150" width="110" height="60"/>
    <text x="235" y="185" text-anchor="middle">1</text>
    <rect x="300" y="150" width="110" height="60"/>
    <text x="355" y="185" text-anchor="middle">2</text>
    <line x1="290" y1="120" x2="310" y2="148"/>
    <polyline points="300,144 310,148 309,138"/>
    <line x1="355" y1="120" x2="355" y2="148" stroke-dasharray="4 4"/>
    <line x1="290" y1="180" x2="298" y2="180" stroke-dasharray="4 4"/>
    <text x="430" y="95">above: drop C of a</text>
    <text x="430" y="185">C = C: diagonal + 1</text>
    <text x="320" y="238" text-anchor="middle">shaded: the cell a match reads. Dashed: the cells a mismatch would read.</text>
  </g>
</svg>

The diagonal is "both letters used up". It is the only move that scores, and it is
allowed only when the letters are equal.

**Getting the subsequence back.** Start at the corner L(5, 5) = 3 and retrace
which case produced each cell:

1. (5, 5): D against B, different. Above is 3, left is 2. The 3 came from above:
   go up to (4, 5).
2. (4, 5): B against B, equal. Take **B**, go diagonally to (3, 4).
3. (3, 4): C against A, different. Above 1, left 2: go left to (3, 3).
4. (3, 3): C against C, equal. Take **C**, go diagonally to (2, 2).
5. (2, 2): B against D, different. Above L(1, 2) = 0, left L(2, 1) = 1: go left to
   (2, 1).
6. (2, 1): B against B, equal. Take **B**, go to (1, 0). Column 0: stop.

The letters were collected backwards: B, C, B. Reversed, "BCB". Check it: in
"ABCBD" at positions 1, 2, 3; in "BDCAB" at positions 0, 2, 4. On ties between above
and left (there are none on this walk) either choice gives a valid LCS, and a tie
rule is where you would encode "the lexicographically smallest one".

### Trace 3: edit distance, the same grid with prices

Turn "horse" into "ros" using single-character inserts, deletes and replaces,
each costing 1. D(i, j) = the fewest operations turning a[:i] into b[:j].

```
D(i, j) = D(i-1, j-1)                     if a[i-1] == b[j-1]   keep it, free
D(i, j) = 1 + min( D(i-1, j),             delete a[i-1]
                   D(i, j-1),             insert b[j-1]
                   D(i-1, j-1) )          replace a[i-1] by b[j-1]
D(i, 0) = i     delete all i characters
D(0, j) = j     insert all j characters
```

| | "" | r | o | s |
|---|---|---|---|---|
| "" | 0 | 1 | 2 | 3 |
| h | 1 | 1 | 2 | 3 |
| o | 2 | 2 | 1 | 2 |
| r | 3 | 2 | 2 | 2 |
| s | 4 | 3 | 3 | 2 |
| e | 5 | 4 | 4 | **3** |

What is new compared with the LCS: **row 0 and column 0 are not zeros**. Turning
"hor" into the empty string takes three deletes, so D(3, 0) = 3. Turning the empty
string into "ro" takes two inserts. These edges are the base cases, and getting
them wrong is the most common edit distance bug (see Traps).

The cell D(1, 1), h against r, in full:

> "Turn 'h' into 'r'. They differ, so I pay 1 for one of three last operations.
> Delete the h, and then turn '' into 'r': D(0, 1) = 1, total 2. Insert the r at the
> end, and then turn 'h' into '': D(1, 0) = 1, total 2. Replace h by r, and then
> turn '' into '': D(0, 0) = 0, total 1. The cheapest is 1."

D(2, 2), o against o: equal, so it costs nothing more than turning "h" into "r":
D(1, 1) = 1.

Walking back from (5, 3) = 3 gives the operations: e against s differ, and above
(4, 3) = 2 plus 1 = 3, so **delete e**. (4, 3): s = s, **keep s**, diagonal to
(3, 2). (3, 2): r against o differ; above (2, 2) = 1 plus 1 = 2, so **delete r**.
(2, 2): o = o, **keep o**. (1, 1): h against r, the diagonal gave 1, so **replace h
by r**. Read forwards: replace h by r, keep o, delete r, keep s, delete e. Three
operations: horse, rorse, rose, ros.

What this trace shows that the LCS trace did not: the grid is the same, the
moves are the same, and the meaning changed entirely because of **what each move
costs** and **what the edges mean**. That is "design the state" in practice: the
state (i, j) is identical, and the problem lives in the transition and the base
cases.

## From the idea to the code

### The grid: all the steps, measured

```python run
from itertools import combinations
import random

def brute(g):
    calls = 0
    def f(r, c):                      # cheapest route from (0,0) to (r,c)
        nonlocal calls
        calls += 1
        if r == 0 and c == 0:
            return g[0][0]
        best = float("inf")
        if r > 0:
            best = min(best, f(r - 1, c))     # came from above
        if c > 0:
            best = min(best, f(r, c - 1))     # came from the left
        return g[r][c] + best
    return f(len(g) - 1, len(g[0]) - 1), calls

def table(g):
    m, n = len(g), len(g[0])
    INF = float("inf")
    f = [[INF] * n for _ in range(m)]
    for r in range(m):                # rows top to bottom
        for c in range(n):            # left to right: up and left are done
            if r == 0 and c == 0:
                f[r][c] = g[0][0]
                continue
            up = f[r - 1][c] if r > 0 else INF
            left = f[r][c - 1] if c > 0 else INF
            f[r][c] = g[r][c] + min(up, left)
    return f

def one_row(g):
    n = len(g[0])
    dp = [float("inf")] * n           # "row -1": nothing comes from above row 0
    dp[0] = 0
    for row in g:
        dp[0] += row[0]                       # column 0: only from above
        for c in range(1, n):                 # left to right
            dp[c] = row[c] + min(dp[c],       # old value: the cell above
                                 dp[c - 1])   # new value: the cell to the left
    return dp[-1]

def every_route(g):                   # the truth: try every set of down moves
    m, n = len(g), len(g[0])
    best = float("inf")
    for downs in combinations(range(m + n - 2), m - 1):
        r = c = 0
        total = g[0][0]
        for step in range(m + n - 2):
            if step in downs: r += 1
            else: c += 1
            total += g[r][c]
        best = min(best, total)
    return best

g = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
for row in table(g):
    print(row)
print("brute (answer, calls):", brute(g), " one row:", one_row(g))
assert table(g) == [[1, 4, 5], [2, 7, 6], [6, 8, 7]]
assert brute(g) == (7, 19) and one_row(g) == every_route(g) == 7
rng = random.Random(2)
for _ in range(300):
    m, n = rng.randint(1, 5), rng.randint(1, 5)
    G = [[rng.randint(0, 9) for _ in range(n)] for _ in range(m)]
    assert table(G)[-1][-1] == one_row(G) == brute(G)[0] == every_route(G)
big = [[rng.randint(0, 9) for _ in range(9)] for _ in range(9)]
print("9 x 9: brute calls", brute(big)[1], "for", 81, "cells")
```

On the 3 x 3 grid the brute force makes 19 calls for 9 cells, as counted above. On
9 x 9 it makes over a hundred thousand for 81 cells.

### Each line, and which part of the recursion it is

| line | in plain words | in the recursion |
|---|---|---|
| `for r in range(m)` / `for c in range(n)` | rows top to bottom, each left to right | "solve the neighbours first": up and left are finished |
| `f[r][c] = g[0][0]` at the start | the start cell costs itself | the base case f(0, 0) |
| `up = f[r-1][c] if r > 0 else INF` | the cheapest route ending just above; none in row 0 | "came from above", f(r-1, c) |
| `left = f[r][c-1] if c > 0 else INF` | the cheapest route ending just left; none in column 0 | "came from the left", f(r, c-1) |
| `g[r][c] + min(up, left)` | pay for this cell, plus the cheaper way in | the recurrence |
| `f[-1][-1]` | the corner | f(m-1, n-1) |

Two boring confusions. **Infinity, not zero, outside the grid**: a 0 would mean
"there is a free route that comes from above row 0", and the min would happily take
it. **What a cell stores**: one number, the cheapest cost to reach it. Not the
route, and not "the cost so far along the route I am following": every cell is the
answer to its own question, independent of any particular route.

In the one-row version, `dp[0] = 0` before the first row and infinity elsewhere is
a small trick: it makes row 0 come out as running sums from the left, because the
"above" of row 0 is infinity everywhere except a zero above the start.

### The LCS, and its one subtle line

The full table is a direct transcription of the recurrence. The one-row version
is where the subtle line lives.

L(i, j) reads three cells: above (i-1, j), left (i, j-1), and **diagonal** (i-1,
j-1). In one row scanned left to right, when you reach column j:

- dp[j] still holds row i-1: that is **above**. Good.
- dp[j-1] already holds row i: that is **left**. Good.
- The **diagonal**, row i-1 column j-1, was in dp[j-1] a moment ago, and it has
  just been overwritten.

So you must save it before overwriting. A variable `diag` carries "the old value of
the cell to my left" one step to the right. Forget it, and the match case reads
dp[j-1], which is L(i, j-1): a value from the **current** row.

What does that compute? On a match it adds 1 to a cell that may already have used
a[i-1]. So one character of a can be matched with several characters of b. Here is
a = "A", b = "AAA", one row, with `*` for a value already rewritten in this row:

**Right (saving the diagonal).**

| j | b[j-1] | reads diag (old) | dp after |
|---|---|---|---|
| start | | | 0 0 0 0 |
| 1 | A | 0 | 0 1* 0 0 |
| 2 | A | 0 (old dp[1]) | 0 1* 1* 0 |
| 3 | A | 0 (old dp[2]) | 0 1* 1* 1* |

**Wrong (reading dp[j-1] on a match).**

| j | b[j-1] | reads dp[j-1] | dp after |
|---|---|---|---|
| start | | | 0 0 0 0 |
| 1 | A | 0 | 0 1* 0 0 |
| 2 | A | **1*** | 0 1* 2* 0 |
| 3 | A | 2* | 0 1* 2* 3* |

At j = 2 the wrong version reads dp[1] = 1, which is "the single A of a, already
matched with the first A of b", and adds another match. The one A is used twice,
then three times. The answer 3 is impossible: a has only one character.

It is the same bug as the left-to-right 0/1 knapsack, in different clothes. There,
an item was taken twice because the take branch read the current row. Here, a
character is matched twice because the match branch read the current row. In both,
the fix is to make the read see the row the recurrence names: the knapsack by
scanning the other way, the LCS by carrying the old value in a variable.

```python run
def lcs_table(a, b):
    n, m = len(a), len(b)
    L = [[0] * (m + 1) for _ in range(n + 1)]     # row 0, column 0: empty prefixes
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1      # diagonal: match both
            else:
                L[i][j] = max(L[i - 1][j],         # up: drop a[i-1]
                              L[i][j - 1])         # left: drop b[j-1]
    return L

def walk_back(L, a, b):
    i, j, out = len(a), len(b), []
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1]); i -= 1; j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))

def lcs_row(a, b, save_diag=True):
    dp = [0] * (len(b) + 1)
    for ch in a:
        diag = 0                                   # old dp[j-1], i.e. L(i-1, j-1)
        for j in range(1, len(b) + 1):
            above = dp[j]                          # still row i-1
            if ch == b[j - 1]:
                dp[j] = (diag if save_diag else dp[j - 1]) + 1
            else:
                dp[j] = max(above, dp[j - 1])
            diag = above                           # becomes the next cell's diagonal
    return dp[-1]

L = lcs_table("ABCBD", "BDCAB")
for row in L:
    print(row)
print("LCS:", walk_back(L, "ABCBD", "BDCAB"))
assert L[5][5] == 3 and walk_back(L, "ABCBD", "BDCAB") == "BCB"
assert L[3][3] == L[2][2] + 1 == 2 and L[3][4] == max(L[2][4], L[3][3]) == 2
assert lcs_table("AB", "BA")[2][2] == 1 and lcs_table("ABCD", "BCDA")[4][4] == 3

print("a='A', b='AAA': right", lcs_row("A", "AAA"), " wrong", lcs_row("A", "AAA", False))
assert lcs_row("A", "AAA") == 1 and lcs_row("A", "AAA", False) == 3

import random
rng = random.Random(4)
for _ in range(300):
    a = "".join(rng.choice("ABC") for _ in range(rng.randint(0, 8)))
    b = "".join(rng.choice("ABC") for _ in range(rng.randint(0, 8)))
    assert lcs_row(a, b) == lcs_table(a, b)[-1][-1]
    w = walk_back(lcs_table(a, b), a, b)
    it = iter(b)                                    # w really is in both
    assert len(w) == lcs_row(a, b) and all(c in it for c in w)
print("one row with diag == full table, on 300 random pairs")
```

The `diag = above` line is the subtle one. It runs after the cell is written, and
it saves the value that was in dp[j] *before* this row touched it, so that the next
column, j+1, finds its diagonal there. Read it a second way: at every moment, the
three variables hold three different rows' worth of information, above (old), left
(new), diagonal (old), and the code has to keep them apart by hand.

### Edit distance: the same skeleton, with prices and edges

```python run
def edit_distance(a, b):
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i                       # delete all i characters
    for j in range(m + 1):
        D[0][j] = j                       # insert all j characters
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                D[i][j] = D[i - 1][j - 1]                 # keep: free
            else:
                D[i][j] = 1 + min(D[i - 1][j],            # delete a[i-1]
                                  D[i][j - 1],            # insert b[j-1]
                                  D[i - 1][j - 1])        # replace
    return D

def operations(D, a, b):
    i, j, ops = len(a), len(b), []
    while i or j:
        if i and j and a[i - 1] == b[j - 1] and D[i][j] == D[i - 1][j - 1]:
            ops.append("keep " + a[i - 1]); i -= 1; j -= 1
        elif i and j and D[i][j] == D[i - 1][j - 1] + 1:
            ops.append("replace %s by %s" % (a[i - 1], b[j - 1])); i -= 1; j -= 1
        elif i and D[i][j] == D[i - 1][j] + 1:
            ops.append("delete " + a[i - 1]); i -= 1
        else:
            ops.append("insert " + b[j - 1]); j -= 1
    return ops[::-1]

D = edit_distance("horse", "ros")
for row in D:
    print(row)
ops = operations(D, "horse", "ros")
print(ops)
assert D[5][3] == 3 and D[1][1] == 1 and D[2][2] == 1
assert sum(not o.startswith("keep") for o in ops) == 3
assert edit_distance("intention", "execution")[-1][-1] == 5
assert edit_distance("", "abc")[-1][-1] == 3 and edit_distance("abc", "")[-1][-1] == 3
```

The edit distance code is the LCS code with three changes, and each is a line you
can point at: the edges are i and j instead of 0; a match copies the diagonal
instead of adding 1; a mismatch takes 1 + the min of three cells instead of the max
of two. The state did not change at all.

## Why it is correct

The grid recurrence is the 1-D argument with two indices: every route to (r, c)
ends with a move from above or from the left, the rest of the route is a route to
that neighbour, and the cheapest route must use the cheapest route to its
neighbour (or swap it in and be cheaper). The interesting proof is the LCS, because
of the one claim we made without justifying it: **when the last characters are
equal, matching them is always safe.**

:::proof The LCS recurrence is exact
**What we claim.** For all i in 0..n and j in 0..m, the table value L(i, j) equals
OPT(i, j), the length of a longest common subsequence of a[:i] and b[:j].

**Base cases.** If i = 0 or j = 0, one of the strings is empty, so the only common
subsequence is the empty one: OPT = 0. The table's row 0 and column 0 are 0.

**A small fact first.** Removing one character from the end of one string lowers
the LCS by at most 1: OPT(i, j) <= OPT(i, j-1) + 1. Proof: take a longest common
subsequence S of a[:i] and b[:j]. If it does not use b[j-1], it is already a
common subsequence of a[:i] and b[:j-1]. If it does, b[j-1] must be matched to
S's last character (nothing in S comes after it); remove that last character and
what remains is common to a[:i] and b[:j-1], with length |S| - 1. Either way
OPT(i, j-1) >= |S| - 1. The same holds with the roles of a and b swapped.

**Inductive step.** Fix i, j >= 1 and assume the claim for all smaller pairs (any
pair with a smaller i, or the same i and a smaller j). Let x = a[i-1], y = b[j-1].

*Case x != y.* Take any common subsequence S of a[:i] and b[:j]. If S used both x
and y, both would have to be S's last character (each is the last of its string),
so x = y, which is false. So S misses x or misses y. If it misses x, S is a common
subsequence of a[:i-1] and b[:j], so |S| <= OPT(i-1, j). If it misses y, |S| <=
OPT(i, j-1). So OPT(i, j) <= max(OPT(i-1, j), OPT(i, j-1)). And the other direction
is immediate: a common subsequence of a shorter prefix is also one of the longer
prefix. So OPT(i, j) = max of the two, which by the hypothesis is what the table
stores.

*Case x = y.* First, OPT(i, j) >= OPT(i-1, j-1) + 1: take a longest common
subsequence of a[:i-1] and b[:j-1] and append x, matched to a[i-1] and b[j-1]; it is
still in order in both strings. Second, OPT(i, j) <= OPT(i-1, j-1) + 1. Take a
longest S and look at how it uses the two last characters. If S uses neither x in a
nor y in b at its end, S is common to a[:i-1] and b[:j-1], and |S| <=
OPT(i-1, j-1). If S's last character is matched to both, removing it leaves a
common subsequence of a[:i-1] and b[:j-1], so |S| <= OPT(i-1, j-1) + 1. If S uses
exactly one of them, say a[i-1] but not b[j-1], then S is common to a[:i] and
b[:j-1]; its last character is a[i-1] = x, matched somewhere in b[:j-1]. Rematch
that last character to b[j-1] instead (also equal to x, and later than any position
S used in b), and S becomes a common subsequence of the same length whose last
character uses both x and y.
Removing it leaves a common subsequence of a[:i-1] and b[:j-1], so again |S| <=
OPT(i-1, j-1) + 1. The case "b[j-1] but not a[i-1]" is symmetric. So OPT(i, j) =
OPT(i-1, j-1) + 1, which is what the table stores.

**Why the three-way max changes nothing.** By the small fact, OPT(i-1, j) <=
OPT(i-1, j-1) + 1 and OPT(i, j-1) <= OPT(i-1, j-1) + 1, so on a match the other two
cells can tie the diagonal plus one but never beat it.

**Order.** The loops fill rows in increasing i, and within a row increasing j, so
(i-1, j-1), (i-1, j) and (i, j-1) are filled before (i, j). The table has (n+1)(m+1)
cells, each computed once. ∎
:::

The middle of the proof, the rematching, is the heart of it, and it is an exchange
argument: **if an optimal answer uses one of the two equal last characters but not
the other, slide its match over to the other one; nothing breaks, and now both are
used.** So some optimal answer always matches the equal last characters with each
other, and the recurrence is allowed to commit to that.

The edit distance proof has the same skeleton: the last operation in an optimal
edit script either touches a[i-1] (delete), produces b[j-1] (insert), or turns
a[i-1] into b[j-1] (replace or keep), and the rest of the script is an optimal
script for the smaller pair. The palindrome proof is the LCS proof with "the last
character of b" replaced by "the first character of the piece".

The assumptions the proofs used, each a place where a variation changes the
method:

- **Moves only go right and down (or the indices only shrink).** That is what
  makes the dependency graph acyclic and the row-by-row order legal. Allow a move
  up and the grid has cycles: use [[dijkstra]].
- **The cost of a route is the sum of its parts.** "Minimise the largest cell on the
  route" also works (replace + with max). "Keep the health above zero along the
  route" does not work forward, because the future depends on two numbers about the
  past (the lowest point and the current total). Dungeon Game (variation C) fixes
  it by running backwards.
- **Matching equal characters is free and always safe.** True for plain LCS. With
  weights on characters, or a cost for each match, the rematching argument still
  works, but with a gap penalty or a limit on matches it may not, and the safe form
  is the max over all three cells.
- **The prefix is the right state.** For a *contiguous* common piece (longest
  common substring), the prefix state is wrong for the same reason as in Kadane:
  the state must say where the piece ends (variation F).

## What it costs

**Time.** Number of states times work per state, as always.

| problem | states | work per state | time |
|---|---|---|---|
| grid paths or costs, m x n | m·n | O(1) | O(m·n) |
| LCS, edit distance, lengths n and m | (n+1)(m+1) | O(1) | O(n·m) |
| palindromic subsequence, length n | n²/2 | O(1) | O(n²) |
| palindromic substrings, boolean table | n²/2 | O(1) | O(n²) |

For the bank's limits: a 500 x 500 grid is 250,000 cells; LCS of two strings of
500 is 250,000; a palindrome table on 2,000 characters is about 2 million cells.
Plain Python does a few million simple cell updates per second, so all of these are
fine. Two strings of 10^5 are 10^10 cells and are not, in any language: the
intended solution must be something else (a two-pointer scan for "one edit apart",
an LIS when one side has unique values, a band of width k when the distance is
known to be at most k, O(n·k)).

**Space.** The full table is O(n·m). Rolling to one row is O(m), or O(min(n, m)) if
you put the shorter string across the top. Rolling loses reconstruction: the walk
back reads cells from earlier rows. If you need the actual subsequence or edit
script with linear memory, Hirschberg's algorithm splits the problem in half
recursively and recovers it in O(n·m) time and O(m) space. It is rare in interviews;
knowing it exists is enough.

**The costs people forget.**

- **Slicing strings in the inner loop.** `a[:i] == b[:j]` or `s[i:j+1] ==
  s[i:j+1][::-1]` inside a double loop is O(n) per cell, which turns O(n²) into
  O(n³). Compare single characters; let the table remember the rest.
- **Lists of lists in Python.** `L[i-1][j-1]` is two index operations. In a hot loop,
  binding `prev = L[i-1]` and `cur = L[i]` once per row is a measurable win.
- **The brute force for comparison.** C(m+n, m) routes; 2^n subsequences; 3^(n+m)
  edit scripts. The DP is the difference between those and n·m.

## How to think about it

Ask these questions, in this order, on every new problem of this family.

1. **What are the two things?** A board (row and column). Two sequences (a position
   in each). One sequence read from both ends (a left and a right end). A sequence
   and a small pattern (a position in each: "how much of the pattern have I
   matched?"). Naming the two things names the two indices.
2. **What does one step consume?** On a grid, one cell. On two strings: one
   character of a, one of b, or one of each. On one string from both ends: the left
   end, the right end, or both. Each kind of step is one neighbour of the cell.
3. **Prefix, suffix, or "ending exactly here"?** "The first i and the first j" is the
   default for subsequences and alignments. If the answer must be **contiguous** in
   one of the strings, the state must say where it ends, and the answer becomes a
   max over the table instead of the corner.
4. **What is the cell computing?** Max (LCS, palindromes), min (edit distance, path
   cost), a count (number of paths, number of occurrences), yes/no (interleaving,
   is this piece a palindrome). That decides the operation and the value for
   "impossible".
5. **What do the edges mean?** Row 0 and column 0 are the empty prefix. Say in words
   what the answer is when one side is empty: 0 for LCS, i or j for edit distance,
   1 path along an edge of an open grid, infinity for a cost grid outside its border.
6. **Which way do the arrows point?** Up, left and diagonal: fill row by row, left to
   right. Inward, (i+1, j-1): fill by increasing length, or i from the bottom up.
   Down and right (a problem solved from the end, such as Dungeon Game): fill from
   the bottom-right corner backwards. Write the arrows down before writing loops.
7. **Which cell is the answer?** The corner, a max over the table, or a whole row.
8. **Do I need the path?** Keep the table and walk back. If not, roll it to one row,
   and decide which old values (above, diagonal) you must keep.

Then, before writing code, write the four lines: **the state in words**, **the cases
of the last step**, **the edges**, **the answer cell**.

### Telling it from its neighbours

- **1-D DP** ([[dynamic-programming]]). If one index really is enough, use it. Most
  2-D problems here began as "I tried one index and the future needed a second
  number".
- **Knapsack** ([[knapsack]]). Also a 2-D table, but the second index is a resource
  (capacity left), not a position. The tell is a limit that all choices draw from.
- **DP on strings in depth** ([[dp-strings]]). Regular-expression matching, wildcard
  patterns, distinct subsequences and the rest of the string family build on the
  LCS grid of this chapter.
- **Interval DP** ([[partition-dp]]). The palindrome table's state, (i, j) on one
  sequence, is the start of interval DP. When a cell needs to try every split point
  k between i and j (burst balloons, matrix-chain order), the transition costs O(n)
  and the total O(n³). That is the next node.
- **Shortest paths on grids** ([[grid-bfs]], [[dijkstra]]). Any move in any
  direction, or obstacles you route around in all directions: no acyclic order, so
  no table.
- **Palindromes as a string topic** ([[palindromes]]). The longest palindromic
  *substring* has O(n²) DP, O(n²)-time O(1)-space expansion around centres, and
  O(n) [[manachers]]. The subsequence version needs the DP.

## Variations

Each says what changes, why, a small example, and problems from this bank. A, B, F,
G and H are the core of interviews and online assessments. C, D, E and I are
regular. J is rare.

### A. Counting paths on a grid

**What changes.** The cell holds a count, min becomes +. paths(r, c) = paths(r-1, c)
+ paths(r, c-1), with 1 along the top row and the left column (one straight route).
A blocked cell holds 0 and contributes nothing.

**Why.** Every route into (r, c) came from above or from the left, never both, so
the counts add with no double counting.

**Example.** 3 x 3: rows 1 1 1 / 1 2 3 / 1 3 6, answer 6 = C(4, 2). 3 x 7: 28. Block
the centre of a 3 x 3 and the answer is 2 (around the left edge or the top edge).

**Bank.** [[p:peoplestrong-unique-paths|Unique Paths Through a Grid]] and
[[p:bloomberg-unique-paths|Unique Paths]]. On an open grid the formula C(m+n-2,
m-1) answers it with no table; the table is the version that survives obstacles and
costs.

### B. Costs on a grid, in other shapes

**What changes.** The predecessors. Minimum path sum has two (above, left). A
**triangle** has two in the row above, at the same column and one to the left. A
**falling path** that may move down-left, down or down-right has three. The rule is
always the same: list the cells you can arrive from, take the best, add this cell.

**Triangle, bottom-up.** Starting at the top of a triangle and moving to the same
or the next column in the row below, the edge cases (the first and last entry of
each row have only one parent) disappear if you go the other way: start from the
bottom row and let best[c] = t[r][c] + min(best[c], best[c+1]). The answer is
best[0]. Triangle 2 / 3 4 / 6 5 7 / 4 1 8 3: from the bottom, 4 1 8 3 becomes 7 6 10,
then 9 10, then 11. Path 2, 3, 5, 1.

**Bank.** [[p:amazon-minimum-path-sum|Minimum Path Sum]] (the main example),
[[p:expedia-triangle-minimum-path-sum|Triangle Minimum Path Sum]] (bottom-up, with
negative values allowed),
[[p:scale-ai-minimum-falling-path-sum|Minimum Falling Path Sum]] (three predecessors,
any start in the top row, answer is the min of the last row).

### C. Running it backwards: Dungeon Game

**What changes.** The direction. A knight walks right and down; negative cells
hurt, positive cells heal; health must stay at least 1 everywhere. What is the
smallest starting health?

**You might think: run it forward, keeping the best "lowest health so far".** The
forward state needs **two** numbers: the lowest point of the route so far, and the
current total. Neither alone decides which incoming route is better. Grid
[[-3, -4, 3], [1, -4, -4]]: the last cell can be entered from the left by a route
with (lowest -6, total -6), or from above by a route with (lowest -7, total -4). The
first looks safer. The last cell, -4, punishes its smaller total: -10 against -8. Forward keeping "the best lowest
point" says 11; the truth is 9.

**The fix.** Ask the question from the other end: need[r][c] = the least health you
must have when entering (r, c) to survive from here to the end. That depends only on
the future, which is one number:

```
need[r][c] = max(1, min(need[r+1][c], need[r][c+1]) - dungeon[r][c])
```

Fill from the bottom-right corner backwards. The state that failed forward works
backward because the future of a cell is a single number and the past is not.

**Bank.** [[p:tekion-dungeon-game|Dungeon Game]]. The lesson is general: if the
forward state needs two numbers and the backward state needs one, go backward.

### D. A shape that ends at a cell: maximal square

**What changes.** The state is "the largest all-ones square whose **bottom-right
corner** is (r, c)". A square of side k ending at (r, c) needs squares of side k-1
ending above, to the left and diagonally. So side[r][c] = 1 + min(side[r-1][c],
side[r][c-1], side[r-1][c-1]) when the cell is 1, else 0. The answer is the largest
side, squared.

**Why "ending at".** As in Kadane, the shape must be contiguous, so the state must
pin down where it ends.

**Example.** Rows 0 1 1 1 / 1 1 1 1 / 0 1 1 1 give side 0 1 1 1 / 1 1 2 2 / 0 1 2 3.
The largest square has side 3, area 9. And the sum of all the sides, 15, is the
number of all-ones squares, because a cell with side k is the bottom-right corner of
exactly k squares (sides 1 to k).

**Bank.** [[p:amazon-maximal-square|Maximal Square]] (largest area) and
[[p:google-count-all-one-squares|Count All-One Squares]] (the sum of the table).

### E. Adding a layer

**What changes.** The story adds a choice, so the state adds a dimension.
[[p:infosys-minimum-path-sum-with-grid-switches|Minimum Path Sum With Grid Switches]]
gives two grids and lets you switch between them at any cell for a fee. The state is
(which grid, row, column): best[g][r][c] = the cheapest way to stand on (r, c) using
grid g. First compute each layer from above and left as usual, then allow a switch
at the same cell: best[g][r][c] = min(best[g][r][c], best[1-g][r][c] + fee). It is
still a grid; there are just two numbers per cell.

### F. The LCS family

**What changes.** The question asked of the same grid.

- **Longest common subsequence.**
  [[p:morgan-stanley-longest-common-subsequence|Longest Common Subsequence]]: the
  main example.
- **Longest common substring** (contiguous). The state must end at both
  positions: C(i, j) = the length of the longest common piece ending exactly at
  a[i-1] and b[j-1]. On a match, C(i-1, j-1) + 1. On a mismatch, **0**: a contiguous
  piece cannot survive a mismatch. The answer is the max over the table. "ABAB" and
  "BABA": LCS 3, longest common substring 3 ("ABA" or "BAB"); "ABCD" and "ACBD": LCS
  3, substring 1. [[p:xai-longest-common-substring|Longest Common Substring]].
- **Shortest common supersequence length** = n + m - LCS. **Delete-only distance**
  (fewest deletions from both to make them equal) = n + m - 2·LCS. Both are "the
  LCS is what you keep".
- **An OA story.** [[p:amazon-minimum-insertions|Minimum Insertions to Make List a Subsequence]]
  is a length minus an LCS. Because one list has unique values, map each value to its
  position in that list and the LCS becomes a longest increasing subsequence of the
  mapped positions, O(n log n) instead of O(n·m).
- **Interleaving.** Is s3 an interleaving of s1 and s2?
  [[p:amazon-interleaving-string|Interleaving String]]. There are three strings, but
  only two indices: if i characters of s1 and j of s2 are used, then exactly i + j
  characters of s3 are, so the third index is implied. ok[i][j] = (ok[i-1][j] and
  s1[i-1] == s3[i+j-1]) or (ok[i][j-1] and s2[j-1] == s3[i+j-1]). This is "the least
  the future needs to know" at its sharpest: a third number that looks necessary
  and is not.

### G. The edit distance family

**What changes.** The prices of the moves.

- **Edit distance**, all costs 1: [[p:astrotalk-edit-distance|Edit Distance]].
- **Weighted** costs (insert 2, delete 1, replace 3): the same recurrence with
  those numbers in place of the 1s, and the edges become i·delete and j·insert.
- **No replace**: only insert and delete; the answer is n + m - 2·LCS.
- **"At most one edit apart?"** Do not build the table.
  [[p:expedia-at-most-one-edit-apart|Strings at Most One Edit Apart]] is a single
  scan: walk both strings until the first difference, then compare the rest with
  one character skipped on the longer side (or on both for equal lengths). O(n).
- **Banded.** If the distance is known to be at most k, only cells with |i - j| <= k
  can be on an optimal route, so fill a band of width 2k + 1: O(n·k). Rare.

### H. Palindromes: DP over (i, j) of one string

**What changes.** The two indices are the two ends of one string, and the arrows
point inward.

**Longest palindromic subsequence.** P(i, j) for the piece s[i..j], both ends
included: P(i, i) = 1; if s[i] == s[j], P(i, j) = P(i+1, j-1) + 2; else max(P(i+1,
j), P(i, j-1)). The answer is P(0, n-1). For "bbbab":

| i \ j | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 (b) | 1 | 2 | 3 | 3 | **4** |
| 1 (b) | | 1 | 2 | 2 | 3 |
| 2 (b) | | | 1 | 1 | 3 |
| 3 (a) | | | | 1 | 1 |
| 4 (b) | | | | | 1 |

P(0, 4): b and b are equal, wrap them around P(1, 3) = 2 ("bb" inside "bba"): 4,
"bbbb". P(0, 3): b and a differ: max(P(1, 3) = 2, P(0, 2) = 3) = 3.

**The order.** P(i, j) reads row i+1. So rows must be filled from the **bottom
up** (i from n-1 down to 0), with j increasing inside each row. Equivalently, fill by
length: all pieces of length 1, then 2, then 3. Filling i upward reads rows that are
still empty, and the Traps block shows the damage.

**Two identities worth knowing.** P(s) = LCS(s, reversed s), so you can reuse the
LCS code. And the fewest insertions that make s a palindrome is n - P(s): keep the
longest palindromic subsequence, and insert a mirror for every other character.
"mbadm": P = 3 ("mam" or "mdm"), so 2 insertions ("mbdadbm").

**Palindromic substrings.** Is s[i..j] a palindrome? pal[i][j] = (s[i] == s[j]) and
(j - i < 2 or pal[i+1][j-1]). The count of true cells is the number of palindromic
substrings: "aaa" has 6. Here the DP is O(n²) time **and** O(n²) space, and the
expansion around each of the 2n-1 centres is O(n²) time and O(1) space, which is
usually the better interview answer.

**Bank.** [[p:goldman-sachs-longest-palindromic-subsequence|Longest Palindromic Subsequence]],
[[p:bloomberg-minimum-insertions-to-make-palindrome|Minimum Insertions to Make a Palindrome]]
(n - P, with n up to 2,000),
[[p:amazon-count-substrings|Palindromic Substrings]], and a stretch,
[[p:microsoft-longest-palindrome-from-two-words|Longest Palindrome from Two Words]]:
run the palindrome table on word1 + word2, but only accept answers whose outer
matching pair has its left end in word1 and its right end in word2, so both words
contribute.

### I. Designing the state for two sequences

The textbook problems give you the state. The interesting ones make you find it.
The recipe is always the same: **one index per sequence, each meaning "how much of
it is dealt with"**, and then ask what extra rule forces an extra fact.

- **Count the occurrences of a short pattern as a subsequence.**
  [[p:stanley-get-subsequence-count|String Subsequences]]: count how many times a
  3-letter s1 appears as a subsequence of s2 (up to 5·10^5 letters). The state is
  (position in s2, how much of s1 is matched), and since s1 is tiny, keep one count
  per matched length: ways[k] = the number of ways to match s1[:k] so far, ways[0] =
  1. For each character of s2, for k from 3 **down to** 1, if s1[k-1] equals it,
  ways[k] += ways[k-1]. The downward loop is the 0/1 knapsack direction, for the same
  reason: one character of s2 must not fill two slots of s1. With s1 = "AAB" and s2 =
  "AB", downward gives 0, upward gives 1 (the one A counted as both As).
- **Different rules for the two strings.**
  [[p:wellsfargo-longest-subsequence-substring|Longest Subsequence That Is a Substring]]:
  the longest subsequence of x that is a *contiguous* substring of y. Subsequence in
  x means "prefix of x" is fine; substring in y means the state must say where in y
  the piece ends. So W(i, j) = the longest piece of y ending exactly at j that is a
  subsequence of x[:i]. A match extends the diagonal: W(i-1, j-1) + 1. Otherwise, the
  character of x is skipped: W(i-1, j), which **carries down** instead of resetting
  (x may skip letters; y may not). The answer is the max over the table. The two rules
  produce two different behaviours on a mismatch, in the same table.
- **Counting substrings that avoid a pattern.**
  [[p:phonepe-substrings-without-target-subsequence|Substrings Without a Target Subsequence]]:
  for each end position of s, keep, for each k, the latest start from which
  target[:k] can still be matched up to here (updated for k from high to low, again
  so one character does not fill two slots). The substrings ending here that contain
  the target are the ones starting at or before the latest start for the whole
  target; the rest are counted.

**Why.** In each of these, the first instinct (one index per string, a plain
table) is close, and the problem's twist decides one detail: a tiny pattern turns a
dimension into a short array; a "contiguous" rule turns the state into "ending at";
a counting rule forces a loop direction.

### J. Rare: what to recognise and not to implement

- **Hirschberg**: the LCS or edit script in linear space, by divide and conquer.
- **Bit-parallel LCS**: 64 columns per machine word; competitive programming only.
- **Regular-expression matching** with `.` and `*`, and wildcard matching with `?`
  and `*`: the LCS grid with a star that can consume zero or more characters, so a
  cell may read from the same row. [[dp-strings]] covers them.

## Recognising it in a statement

Ordered by how reliable they are.

1. **"Move only right or down"** on a grid, with "minimum cost", "maximum gold" or
   "how many paths". Grid DP, almost certainly.
2. **Two strings and a word from this list**: "common subsequence", "edit",
   "insert, delete, replace", "transform", "align", "interleave". The two-string
   grid.
3. **"Longest palindromic subsequence"**, "minimum insertions / deletions to make a
   palindrome". The (i, j) table on one string.
4. **Two lengths up to a few thousand** (n, m <= 1000 to 5000). The setter is
   telling you n·m fits.
5. **"Largest square / rectangle of ones"**, "count squares". The "ending at this
   corner" table.
6. **A pattern that is short and a text that is long** ("count the times this
   3-letter word appears as a subsequence"). A tiny second dimension: one counter per
   pattern position.

**Disguised forms.**

- **"Fewest insertions to make it a palindrome"** = n - (longest palindromic
  subsequence) = n - LCS(s, reversed s).
- **"Fewest deletions to make two strings equal"** = n + m - 2·LCS.
- **"The two lists share elements; fewest insertions so one becomes a subsequence
  of the other"** = a length minus an LCS, and with unique values, an LIS.
- **"Can these two schedules be merged into this one, keeping each one's order?"**
  is Interleaving String.
- **"Longest chain of matching moves between two logs"** is an LCS with a custom
  equality.

**Anti-signals.**

- **Four-direction moves**, or "shortest number of steps" with walls: BFS, not DP.
- **"Substring" when you expected "subsequence"**: the state must end at a
  position, and the answer is a max, not the corner. Read the word twice.
- **Lengths up to 10^5 or more with two strings**: not the table. Look for a scan,
  a hash, an LIS, or a bound on the answer.
- **"Is s a subsequence of t?"** with no optimisation: two pointers, O(n + m).

## Traps

**1. Zeros outside the grid in a min problem.** Symptom: the answer is too small,
because a route "came from" a free cell above row 0. Use infinity, or fill row 0
and column 0 separately.

**2. Edit distance edges set to 0.** Symptom: "abc" to "" gives 0. Row 0 is j
inserts and column 0 is i deletes. The LCS has zero edges; edit distance does not,
and copying the LCS skeleton is how this bug is born.

**3. Losing the diagonal when rolling the LCS.** Symptom: an LCS longer than the
shorter string. Save the old dp[j-1] in a variable before overwriting it. The
demonstration is in "From the idea to the code".

**4. Filling the palindrome table in the wrong order.** Symptom: answers that are
too small, often stuck at 2. P(i, j) reads row i+1, so i must go downward.

**5. Subsequence versus substring.** Symptom: the longest common "substring" code
returns the LCS (too big), or the other way round. A substring resets to 0 on a
mismatch and is read as a max over all cells.

**6. Off-by-one between the table and the strings.** Symptom: an IndexError, or a
comparison of the wrong characters. Row i means "the first i characters", so the
character for row i is a[i-1]. Row 0 exists for the empty prefix.

**7. Forward DP where the future needs one number and the past needs two.**
Symptom: Dungeon Game answers that are slightly too high. Go backward.

**8. The pattern loop in the wrong direction when counting subsequence
occurrences.** Symptom: counts that are too high for patterns with repeated
letters. Go from the last slot down.

Traps 2, 4, 5 and 7, run:

```python run
def edit(a, b, edges=True):
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    if edges:
        for i in range(n + 1): D[i][0] = i
        for j in range(m + 1): D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            same = a[i - 1] == b[j - 1]
            D[i][j] = D[i - 1][j - 1] if same else 1 + min(D[i - 1][j], D[i][j - 1], D[i - 1][j - 1])
    return D[n][m]

print("'abc' -> '': edges", edit("abc", ""), " zero edges", edit("abc", "", False))
assert edit("abc", "") == 3 and edit("abc", "", False) == 0
assert edit("xabc", "abc") == 1 and edit("xabc", "abc", False) == 0   # free deletes

def lps(s, i_downward=True):
    n = len(s)
    P = [[0] * n for _ in range(n)]
    rows = range(n - 1, -1, -1) if i_downward else range(n)
    for i in rows:
        P[i][i] = 1
        for j in range(i + 1, n):
            P[i][j] = P[i + 1][j - 1] + 2 if s[i] == s[j] else max(P[i + 1][j], P[i][j - 1])
    return P[0][n - 1]

for s, want in [("bbbab", 4), ("agbdba", 5), ("racecar", 7)]:
    print("LPS %-8s right %d  i upward %d" % (s, lps(s), lps(s, False)))
    assert lps(s) == want and lps(s, False) == 2      # row i+1 was still all zeros

def common(a, b, contiguous):
    best, C = 0, [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                C[i][j] = C[i - 1][j - 1] + 1
            else:
                C[i][j] = 0 if contiguous else max(C[i - 1][j], C[i][j - 1])
            best = max(best, C[i][j])
    return best

print("ABCD vs ACBD: subsequence", common("ABCD", "ACBD", False), " substring", common("ABCD", "ACBD", True))
assert common("ABCD", "ACBD", False) == 3 and common("ABCD", "ACBD", True) == 1

def dungeon(d):                           # backward: need[r][c] on entering (r, c)
    R, Cn = len(d), len(d[0])
    INF = float("inf")
    need = [[INF] * (Cn + 1) for _ in range(R + 1)]
    need[R][Cn - 1] = need[R - 1][Cn] = 1
    for r in range(R - 1, -1, -1):
        for c in range(Cn - 1, -1, -1):
            need[r][c] = max(1, min(need[r + 1][c], need[r][c + 1]) - d[r][c])
    return need[0][0]

def dungeon_forward(d):                   # keeps only the route with the best low point
    R, Cn = len(d), len(d[0])
    st = [[None] * Cn for _ in range(R)]  # (lowest prefix so far, total so far)
    for r in range(R):
        for c in range(Cn):
            ins = [st[r - 1][c]] * (r > 0) + [st[r][c - 1]] * (c > 0)
            low, tot = max(ins) if ins else (0, 0)
            tot += d[r][c]
            st[r][c] = (min(low, tot), tot)
    return 1 - st[-1][-1][0]

g = [[-3, -4, 3], [1, -4, -4]]
print("dungeon", g, ": backward", dungeon(g), " forward", dungeon_forward(g))
assert dungeon(g) == 9 and dungeon_forward(g) == 11
assert dungeon([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]) == 7
```

The palindrome line is worth reading twice. With i going upward, P(0, 2) for "bbb"
reads P(1, 1), which is still 0 because row 1 has not been visited yet. So it
computes 0 + 2 = 2, and every later cell builds on that. The code runs, prints a
plausible number, and is wrong on every input longer than two.

## What to memorise

The template, which is the LCS grid with the three moves:

```python
L = [[0] * (m + 1) for _ in range(n + 1)]        # row 0, column 0: empty prefixes
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if a[i - 1] == b[j - 1]:
            L[i][j] = L[i - 1][j - 1] + 1          # diagonal: use both
        else:
            L[i][j] = max(L[i - 1][j], L[i][j - 1])  # drop one side
answer = L[n][m]
```

Edit distance: edges i and j, a match copies the diagonal, a mismatch is 1 + the
min of three. Palindromes: i from the bottom up, wrap equal ends around the inside.

The sentence that turns a problem into it: **the state is how far along each of the
two things I am; the last step consumes one of them, or both.**

The question that finds the state: **what is the least the future needs to know
about the past?** Here, two numbers.

The habit: before typing the loops, write the arrows (up, left, diagonal, or
inward) and the meaning of row 0 and column 0. The arrows give the fill order; the
edges give the base cases. Most bugs in this chapter are one of those two.

The numbers: n·m up to a few million cells is fine in Python. 10^5 by 10^5 is never
a table.

## Check yourself

:::check
Hand trace. Grid rows 1 2 5 / 3 2 1 / 4 3 1, moving right or down, minimum path
sum. Fill the table, say for f(1, 1) and f(2, 2) which neighbour won, and walk back
for the route. What does "step to the cheaper neighbour" give?
--
| f | 0 | 1 | 2 |
|---|---|---|---|
| row 0 | 1 | 3 | 8 |
| row 1 | 4 | 5 | 6 |
| row 2 | 8 | 8 | 7 |

Row 0: 1, 1+2 = 3, 3+5 = 8. Column 0: 1, 1+3 = 4, 4+4 = 8. f(1, 1) = 2 + min(above
3, left 4) = 5, from above. f(1, 2) = 1 + min(8, 5) = 6, from the left. f(2, 1) = 3
+ min(5, 8) = 8, from above. f(2, 2) = 1 + min(above 6, left 8) = 7, from above.

Walk back: (2,2) from (1,2), from (1,1), from (0,1), from (0,0). Route 1, 2, 2, 1, 1
= 7: right, down, right, down.

The greedy: from 1, right (2) beats down (3); from the 2, down (2) beats right (5);
from the centre 2, right (1) beats down (3); then down (1). 1 + 2 + 2 + 1 + 1 = 7.
Here the greedy happens to be right, which is why one sample test never proves a
greedy.
:::

:::check
Hand trace. Fill the LCS table for a = "AGCAT" (rows) and b = "GAC" (columns). Walk
back to find one LCS. Is there a second LCS of the same length?
--
| | "" | G | A | C |
|---|---|---|---|---|
| "" | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 1 | 1 |
| G | 0 | 1 | 1 | 1 |
| C | 0 | 1 | 1 | 2 |
| A | 0 | 1 | 2 | 2 |
| T | 0 | 1 | 2 | 2 |

For example (3, 3): C = C, so the diagonal L(2, 2) = 1 plus 1 = 2. (4, 2): A = A,
L(3, 1) + 1 = 2. (4, 3): A against C, max(above 2, left 2) = 2, a tie.

Walk back from (5, 3) = 2: T against C, above (4, 3) = 2, go up. (4, 3): A against
C, tie; preferring up, go to (3, 3). C = C: take C, go to (2, 2). G against A: above
(1, 2) = 1 and left (2, 1) = 1 tie; up to (1, 2). A = A: take A. Result "AC".

Yes: "GA" is also common (G at a[1], A at a[3]; G at b[0], A at b[1]), and "GC".
The tie at (4, 3) and (2, 2) is where the walks diverge: preferring left at (4, 3)
leads to (4, 2), A = A, then (3, 1), up to (2, 1), G = G: "GA".
:::

:::check
Hand trace. Edit distance from "cat" to "cut", then from "sun" to "snu". Fill both
tables and give the operations.
--
"cat" to "cut":

| | "" | c | u | t |
|---|---|---|---|---|
| "" | 0 | 1 | 2 | 3 |
| c | 1 | 0 | 1 | 2 |
| a | 2 | 1 | 1 | 2 |
| t | 3 | 2 | 2 | 1 |

Distance 1: keep c, replace a by u, keep t.

"sun" to "snu":

| | "" | s | n | u |
|---|---|---|---|---|
| "" | 0 | 1 | 2 | 3 |
| s | 1 | 0 | 1 | 2 |
| u | 2 | 1 | 1 | 1 |
| n | 3 | 2 | 1 | 2 |

Distance 2. For example (2, 3): u = u, copy the diagonal (1, 2) = 1. (3, 3): n
against u, 1 + min(above 1, left 1, diagonal 1) = 2. One script: keep s, insert n
(s, n so far), keep u, delete n. Swapping two neighbours costs 2 in plain edit
distance; a variant that allows transpositions (Damerau) would make it 1.
:::

:::check
Hand trace. Longest palindromic subsequence of "agbdba". Fill the table in the
right order and give the palindrome. Then say what the fewest insertions to make
"agbdba" a palindrome is, and why.
--
Filling i from the bottom up (the cells with j > i):

| i \ j | 0 a | 1 g | 2 b | 3 d | 4 b | 5 a |
|---|---|---|---|---|---|---|
| 0 a | 1 | 1 | 1 | 1 | 3 | 5 |
| 1 g | | 1 | 1 | 1 | 3 | 3 |
| 2 b | | | 1 | 1 | 3 | 3 |
| 3 d | | | | 1 | 1 | 1 |
| 4 b | | | | | 1 | 1 |
| 5 a | | | | | | 1 |

P(2, 4): b = b, wrap around P(3, 3) = 1: 3 ("bdb"). P(0, 5): a = a, wrap around
P(1, 4) = 3: 5, "abdba".

Fewest insertions: 6 - 5 = 1. Keep "abdba" and insert a mirror for the g: "agbdbga".
Every character outside the longest palindromic subsequence needs a partner, and
characters inside it already have one.
:::

:::check
Why does the LCS go to L(i-1, j) or L(i, j-1) on a mismatch, and never to
L(i-1, j-1)? And why is it safe, on a match, to go only to L(i-1, j-1) + 1?
--
On a mismatch, at most one of the two last characters can be unused for sure; the
other might still match something earlier. "AB" against "BA": the B of a is useless
at the end of b, but matches b's first letter. Going to L(i-1, j-1) throws away both
and gives 0; going to L(i, j-1) keeps a's B and gives 1. Also, L(i-1, j-1) is never
larger than either of the other two, so it adds nothing.

On a match, the proof's exchange argument: if an optimal answer used only one of
the two equal last characters, you could slide that match over to the other one,
because both are the last in their string and equal. So some optimal answer matches
them together, and the rest is the LCS of the shorter prefixes.
:::

:::check
Someone rolls the LCS into one row and writes `dp[j] = dp[j-1] + 1` on a match,
"because dp[j-1] is the diagonal". Where are they wrong, and what input catches it?
--
In one row scanned left to right, dp[j-1] has already been overwritten with row i:
it is L(i, j-1), the cell to the left, not the diagonal L(i-1, j-1). Adding 1 to it
can match a[i-1] a second time.

a = "A", b = "AAA" catches it: the right answer is 1, the wrong code gives 3, which
is longer than a. Any input where one string has a letter once and the other has it
several times in a row will do. The fix is to save the old dp[j] in a variable
before writing it, and use that as the next column's diagonal.
:::

:::check
Someone says: "Dungeon Game is a minimum path sum; run it forward from the start
and keep, at each cell, the route with the highest lowest-point." Where are they
wrong?
--
The forward state needs two facts about the past, the lowest point so far and the
current total, and keeping the route that is best on one of them can throw away the
route that is best for the future. On [[-3, -4, 3], [1, -4, -4]], the last cell can be
entered from the left by a route with (lowest -6, total -6) or from above by one with
(lowest -7, total -4); the final -4 makes the first need 11 and the second 9.

Backwards, the future of a cell is one number: the least health needed on entering
it. need[r][c] = max(1, min(need below, need right) - cell). That state is
sufficient, so the DP is exact. When the past needs two numbers and the future
needs one, run the DP from the end.
:::

:::check
Reduce this disguised problem. "Given two strings, return the fewest characters you
must delete, from either string, to make them equal. word1 = 'sea', word2 = 'eat'."
Name the technique, give the formula, and the answer.
--
What survives in both is a common subsequence, and to delete as little as possible
you keep the longest one. So the answer is n + m - 2·LCS.

LCS("sea", "eat") = 2 ("ea"). The answer is 3 + 3 - 4 = 2: delete s from "sea" and
t from "eat". It is the LCS grid of this chapter, or equally edit distance with only
insert and delete allowed.
:::
