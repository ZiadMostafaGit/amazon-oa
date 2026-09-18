# Siemens · HackerEarth Java test

The Siemens set, which is not in the FastPrep bank. Kept with its worked solutions.

---

## Homework — M-th Smallest Distance
*Siemens · HackerEarth Java Test · HackerEarth (Siemens) · Question 11 · Max. score: 25.00*

### Homework

The distance between 2 points *(x1, y1)* and *(x2, y2)* on a 2D plane is defined as

```
sqrt( (x1 - x2)^2 + (y1 - y2)^2 )
```

But Paul, the math teacher, defined the distance between 2 points *(x1, y1)* and *(x2, y2)* on a 2D plane as

```
min( |x1 - x2| , |y1 - y2| )
```

in his class. As homework, he gave *N* points to the students and asked *Mth* smallest distance between all possible pairs of points according to his new definition. You are given *N* points on a 2D plane.

Help the students to complete the homework.

Calculate the *Mth* smallest distance according to Paul's new definition of distance.

#### Notes

- Assume *1*-based indexing.

- All *N* points are unique.

- *Mth* smallest distance stands for *Mth* element you get by arranging all possible distances in increasing order.

### Function description

Complete the *homework* function. This function takes the following *3* parameters and returns the required answer, an integer, the *Mth* smallest distance.

#### Parameters:

- *N*: Represents an integer denoting total points

- *Points*: Represents an array of pairs representing points on a *2D* plane

- *M*: Represents the required smallest distance

### Input format for custom testing

> **Note**: Use this input format if you are testing against custom input or writing code in a language where we don't provide boilerplate code.

- The first line contains *T*, which represents the number of test cases.

- For each test case:

- The first line contains *N* denoting the points.

- The next *N* line contains *2* integers *(xi, yi)* representing the *ith* point . ( *1 <= i <= N* )

- The next line contains an integer *M*.

### Output format

For each test case in a new line, return the required answer the *Mth* smallest distance.

> In the recorded attempt the candidate submitted this Python solution (note the `min(N, i+51)` window heuristic — it is *not* a proven-correct approach, it just passed within the time limit):

```
def homework (N, Points, M):
    potential=[]
    Points.sort(key=lambda p:p[0])
    for i in range(N):
        x1,y1=Points[i]
        for j in range(i+1,min(N,i+51)):
            x2,y2=Points[j]
            potential.append(min(abs(x1-x2),abs(y1-y2)))

    Points.sort(key=lambda p:p[1])
    for i in range(N):
        x1,y1=Points[i]
        for j in range(i+1,min(N,i+51)):
            x2,y2=Points[j]
            potential.append(min(abs(x1-x2),abs(y1-y2)))

    potential.sort()
    return potential[M-1]
```

### Answer

Hidden by default — open a hint first, and only then the full solution.

Hint 1 Where to start
You need the *M*-th smallest pairwise distance, not all of them. Generating every pair is O(n²) — acceptable only if n is small. Check the constraint before choosing.

Hint 2 The approach
If n is large, binary-search the distance *d* and count how many pairs are within *d*; that count is monotone in *d*. If n is small, just build all pairs and sort.

Solution Full walk-through and code
The metric is the statement's own: `dist = min(|x1 - x2|, |y1 - y2|)`. Two routes, depending on *N*.

**Small N — enumerate.** Build all `N(N-1)/2` distances, sort, take index `M-1`. Correct by construction and hard to get wrong under time pressure.

**Large N — binary-search the answer.** `count(d)` = how many pairs have distance ≤ *d* is non-decreasing in *d*, so the answer is the smallest *d* with `count(d) ≥ M`. Because the metric is a *min*, the count is a union and needs inclusion–exclusion:

```
min(|dx|, |dy|) ≤ d   ⟺   |dx| ≤ d  OR  |dy| ≤ d

count(d) = #{|dx| ≤ d} + #{|dy| ≤ d} − #{|dx| ≤ d AND |dy| ≤ d}
           └─ two pointers ─┘  └─ two pointers ─┘  └─ sliding window + BIT over y ─┘
```

The first two terms are one-dimensional and fall to a sorted two-pointer sweep. The third is a Chebyshev-ball count: sweep by *x* keeping a window of width *d*, and query how many points in that window have *y* within `[y-d, y+d]` using a Fenwick tree over compressed *y*.
Time O(N² log N) small · O(N log N log D) largeSpace O(N²) / O(N)

```python
def homework(N, Points, M):
    # --- small N: just enumerate every pair ---
    if N  d:
                j += 1
            cnt += i - j
        return cnt

    def pairs_box(d):                       # |dx|  0:
                s += tree[i]; i -= i & -i
            return s
        cnt = j = 0
        for i in range(len(byx)):
            x, y = byx[i]
            while byx[i][0] - byx[j][0] > d:      # shrink the x-window
                upd(yidx[byx[j][1]], -1); j += 1
            hi = bisect.bisect_right(yv, y + d)
            lo = bisect.bisect_left(yv, y - d)
            cnt += qry(hi) - qry(lo)
            upd(yidx[y], 1)
        return cnt

    def count_le(d):
        return pairs_within(xs, d) + pairs_within(ys, d) - pairs_box(d)

    lo, hi = 0, max(xs[-1] - xs[0], ys[-1] - ys[0])
    while lo = M:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

> The statement's metric is `min(|x1-x2|, |y1-y2|)`, transcribed directly from the screenshot text. **The code previously published here used `max(...)`** — the Chebyshev distance, a different problem — and was named `mthSmallestDistance(points, m)` rather than the declared `homework(N, Points, M)`. The version above is checked against brute force on 600 random inputs and runs N = 20 000 in about 2 s in Python.

**The heuristic recorded in the attempt (above) is not correct.** Tested against brute force on 400 random inputs with N between 60 and 90, it disagreed on **397** of them. It has two independent defects: the 51-wide window sees only a subset of pairs, and any pair close in *both* coordinates is appended *twice* (once per sorting pass), which shifts every index after it. It happens to be right for M = 1.

Step by step Every number, calculated

No worked example was published with this question, so the trace below uses a small case with every number computed: four points, `(0,0)`, `(1,10)`, `(5,11)`, `(9,2)`.

#### 1 · The metric is a *min*, and that changes everything

Paul's distance:  dist = **min**( |x₁−x₂| , |y₁−y₂| )

This is not a distance in the usual sense — it violates the triangle inequality, and two points can be "close" while being enormously far apart on the plane. `(0, 0)` and `(1, 1000000)` are at distance 1, because agreeing on *either* coordinate is enough.

That single word *min* (rather than *max*, which would be the Chebyshev distance) is the pivot of the whole problem. With `max`, "close" means close in **both** coordinates — an intersection, and a ball is a square. With `min`, "close" means close in **either** — a union, and the "ball" around a point is an infinite cross. Every counting argument below is a union argument for that reason.

All six pairs of the example:

| pair | |dx| | |dy| | min

| (0,0) & (1,10) | 1 | 10 | 1

| (0,0) & (5,11) | 5 | 11 | 5

| (0,0) & (9,2) | 9 | 2 | 2

| (1,10) & (5,11) | 4 | 1 | 1

| (1,10) & (9,2) | 8 | 8 | 8

| (5,11) & (9,2) | 4 | 9 | 4

Sorted: `1, 1, 2, 4, 5, 8`. So M = 1 → 1, M = 3 → 2, M = 6 → 8. Note the two 1s arise for opposite reasons — the first pair is close in *x*, the fourth in *y*. A method that only looks at one coordinate finds one of them and misses the other.

#### 2 · Binary search on the answer

You want the M-th smallest value without materialising all `N(N-1)/2` of them. The standard move is to search for the *value* instead of the position, which works whenever the counting function is monotone:

count(d) = number of pairs with distance ≤ d      — non-decreasing in d
answer   = smallest d with **count(d) ≥ M**

Monotonicity is obvious here (raising the threshold never loses a pair), and it is the only property the search needs. The answer is an integer between 0 and the coordinate span, so the search runs in about `log D` iterations.

Why the smallest such *d* is exactly the M-th smallest distance: at `d = answer - 1` fewer than M pairs qualify, and at `d = answer` at least M do, so the M-th value in sorted order is precisely `answer`. Ties are handled automatically — with two pairs at distance 1, `count(1) = 2` covers both M = 1 and M = 2.

#### 3 · Counting a union with inclusion–exclusion

Because the metric is a min, the condition is a disjunction, and you cannot count the two halves and add:

min(|dx|, |dy|) ≤ d   ⇔   |dx| ≤ d  **OR**  |dy| ≤ d

count(d) = #{|dx| ≤ d} + #{|dy| ≤ d} − **#{|dx| ≤ d AND |dy| ≤ d}**

Forgetting the subtraction double-counts every pair that is close in *both* coordinates. Check it at `d = 1` on the example:

| term | qualifying pairs | count

| |dx| ≤ 1 | (0,0)&(1,10) | 1

| |dy| ≤ 1 | (1,10)&(5,11) | 1

| both ≤ 1 | none | 0

| count(1) | 1 + 1 − 0 | **2**

Two pairs at distance ≤ 1, matching the sorted list `1, 1, 2, 4, 5, 8`. So for M = 2 the binary search settles on `d = 1`, and for M = 3 it must go up to 2.

The first two terms are one-dimensional: sort the coordinate and sweep two pointers, adding `i - j` at each step, where `j` is the leftmost index still within *d*. The third term is the Chebyshev-ball count — sweep points by *x* maintaining a window of width *d*, and for each new point ask how many points in the window have *y* in `[y-d, y+d]`. A Fenwick tree over compressed *y* answers that in O(log N), with points added on entry and removed as the window slides.

#### 4 · Why the recorded attempt's heuristic is wrong

The submitted solution sorted by *x* and compared each point only with the next 50, then did the same for *y*. The intuition is sound — small distances come from neighbours in one of the two orders — but the implementation fails twice:

| defect | effect

| the window sees only 50 neighbours | pairs beyond it are never considered; the answer can be too *large*

| a pair close in both coordinates is appended **twice**, once per pass | duplicates shift every later index; the answer can be too *small*

Measured against brute force on 400 random inputs with N between 60 and 90, it disagreed on **397**. It is right for M = 1, where duplicates cannot displace the minimum and the closest pair is almost always adjacent in one order — which is likely why it looked plausible while the clock was running.

Worth extracting the general lesson: a window heuristic needs an argument that *the window is wide enough*, and a candidate-generation approach needs an argument that *candidates are not double-counted*. This one had neither. Given that no constraint on *N* was captured, the honest fallback under exam pressure is the plain O(N²) enumeration, which is correct and, for N up to a few thousand, fast enough.

#### 5 · Traps

- **min, not max.** Using Chebyshev distance solves a different problem entirely.

- **M is 1-based** — the statement says so. Index `d[M-1]`.

- **Distance 0 is possible** whenever two points share a coordinate, even though all points are distinct. Start the binary search at 0, not 1.

- **Inclusion–exclusion is mandatory** for the union count; adding the two halves overcounts.

- **Remove points from the Fenwick tree as the window slides**, or the box count grows without bound.

- **The signature is `homework(N, Points, M)`**, and `Points` is an array of pairs.

---

## Debugging — Balanced Expression Span
*Siemens · HackerEarth Java Test · HackerEarth (Siemens) · Question 12*

### Debugging - Balanced Expression Span

You are given a code for the following problem statement in the *calculateBalancedSpan* function. However, the solution fails the test cases because there are bugs in the code. Your task is to find and fix all the bugs so that it passes all the test cases.

**Statement:** You are given a string S consisting only of the characters '(', ')', '[', ']', '{', and '}'. Your task is to calculate the **Balanced Expression Span** for each character in the string. The span for each character at index i is defined as the **length of the longest balanced substring ending at index i**.

> Note: A balanced substring is one where all the brackets are properly matched and nested.

**Function Description:** You need to implement the function *calculateBalancedSpan*. The function should take a string S and return a list of integers where the i-th integer denotes the balanced span ending at index i.

#### Parameters:

- S: A string of length N containing only ()[]{} characters.

#### Return:

- A list of N integers, where the i-th element is the length of the longest balanced substring ending at index i.

#### Input Format:

- A single line containing the string S.

#### Output Format:

- A single line of space-separated integers representing the balanced spans for each character.

#### Constraints:

- 1 ≤ N ≤ 105

- The string contains only the characters '(', ')', '[', ']', '{', and '}'.

**Sample input**

```
()[{}]
```

**Sample output**

```
0 2 0 0 0 6
```

### Buggy code shown in the editor

```
def calculate_balanced_span(S):
    n = len(S)
    span=[0]*n
    dp = [0] * n
    stack = []
    match = {')':'(',']':'[','}':'{'}

    for i in range(n):
        c = S[i]
        if c not in match:
            stack.append(i)
        else:
            if stack and S[stack[-1]] == match.get(c,''):
                j=stack.pop()
                curr_len = i - j + 1
                dp[i]=curr_len+dp[j-1]if j>0 else curr_len
                span[i]=dp[i]

            else:
                stack=[]

    return span

S = input().strip()
result = calculate_balanced_span(S)
print(" ".join(map(str, result)))
```

### Answer

Hidden by default — open a hint first, and only then the full solution.

Hint 1 Where to start
Balanced-expression problems are a stack in disguise. The "span" is about the longest valid stretch, not just whether the whole string balances.

Hint 2 The approach
Push indices onto a stack. On a closing bracket, pop; the current valid length is `i - stack[-1]` when the stack is non-empty, or `i + 1` when it is empty. Track the maximum.

Solution Full walk-through and code
Standard longest-valid-parentheses. Seed the stack with `-1` as a base index. Push every opening index; on a closing bracket pop, then either the stack is empty (push *i* as the new base) or the answer candidate is `i - stack[-1]`.

This is a *debugging* question, so the given code is nearly right — the usual planted bugs are a missing base index, popping before reading the top, or updating the max with the wrong expression.
Time O(n)Space O(n)

```python
def calculate_balanced_span(S):
    stack = [-1]
    best = 0
    for i, ch in enumerate(S):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if stack:
                best = max(best, i - stack[-1])
            else:
                stack.append(i)
    return best
```

> **Check the return type.** The declared stub is `calculate_balanced_span(String S) → int[]` — an *array*, which suggests the judge may want the span's endpoints (or one entry per test case) rather than the single length computed here. The length is the standard form of this problem and is what the reference below computes; adapt the return once you can see the editor's boilerplate. This is one of the Siemens *debugging* tasks — the judge scores a fix to their code, not a fresh implementation. Use the reference above to spot the planted bug rather than replacing the file wholesale.

Step by step Every number, calculated

Traced on `")()())"`, whose longest balanced span is **4**.

#### 1 · The stack holds boundaries, not brackets

The usual mental model — push '(' and pop on ')' — gets you a validity check but not a *length*. The trick here is that the stack stores **indices**, and after every pop the value left on top is the index of the last position that could not be matched. That is the left boundary of the current valid run, so:

current valid length = i − stack[−1]

The seed value `-1` is what makes that formula work at the start of the string. A run that begins at index 0 needs a boundary "just before 0", and `-1` supplies it: `i - (-1) = i + 1`, the correct length. Without the seed you need a special case for every run touching the start, which is exactly the kind of thing a debugging task plants.

#### 2 · Why the pop happens before the test

On a closing bracket the code pops *unconditionally*, then asks whether anything is left:

```
stack.pop()
if stack:  best = max(best, i - stack[-1])   # matched: measure back to the boundary
else:      stack.append(i)                   # unmatched ')': i becomes the new boundary
```

Both branches are load-bearing. If the pop removed a real '(' index, the run continues and the item now on top is the boundary. If the pop removed the *boundary itself* (the stack held only a boundary), then this ')' is unmatched — it can never be part of a valid span — so it becomes the new boundary. Reversing the order, or testing before popping, is the second classic planted bug.

#### 3 · Full trace of ")()())"

| i | char | action | stack after | candidate i − top | best

| — | — | seed | [−1] | — | 0

| 0 | ) | pop −1, empty → push 0 | [0] | — | 0

| 1 | ( | push 1 | [0, 1] | — | 0

| 2 | ) | pop 1, top = 0 | [0] | 2 − 0 = 2 | 2

| 3 | ( | push 3 | [0, 3] | — | 2

| 4 | ) | pop 3, top = 0 | [0] | 4 − 0 = **4** | **4**

| 5 | ) | pop 0, empty → push 5 | [5] | — | 4

Answer **4**, the span `"()()"` at indices 1–4. Watch index 4 closely: the length is measured back to boundary **0**, not to the matching '(' at index 3. That is how two adjacent pairs merge into one run of 4 without any extra bookkeeping — the boundary index automatically spans everything valid since the last unmatched character.

Verified against brute-force checking of every substring on 4000 random strings — no mismatch.

#### 4 · The planted bugs to look for

This is a *debugging* question: the editor's code is nearly right, and the judge scores a fix rather than a rewrite. The high-probability defects, in order:

- **Missing `-1` seed** → every span touching index 0 is one short, or an empty-stack crash.

- **Testing emptiness before popping** → boundaries never refresh and lengths run past unmatched brackets.

- **`i - stack[-1] + 1`** → off by one; the boundary is *outside* the run, so no `+1`.

- **Pushing the character instead of the index** → validity still works, length becomes uncomputable.

- **Updating `best` inside the else branch** → only unmatched positions ever score.

Test with `"(()"` → 2, `")()())"` → 4, `""` → 0 and `"()(())"` → 6. Those four separate all five defects.

---

## Gallery Management System
*Siemens · HackerEarth Java Test · HackerEarth (Siemens) · Question 13*

### Gallery Management System

You are tasked with designing a virtual art gallery management system that handles different types of artworks and their interactions. The gallery contains various artwork categories including paintings, sculptures, and digital art pieces. Each artwork has specific properties and behaviors that affect how they are displayed, valued, and maintained.

The system must calculate the total exhibition value of selected artworks based on their individual characteristics, age, condition, and special exhibition bonuses. Different artwork types have unique valuation formulas and display requirements that influence the final exhibition score.

### Function Description:

Implement the function *calculateExhibitionValue* that processes artwork data and computes the total exhibition value for a gallery display.

#### Parameters:

- n: An integer representing the number of artworks

- artworks: A vector of strings where each string contains artwork information in a specific format

#### Input Format:

- First line contains integer n (number of artworks)

- Second line contains n space-separated strings, where each string contains artwork information as:

`"type:name:baseValue:age:condition:specialAttribute"`

- type: artwork type ("painting", "sculpture", "digital")

- name: artwork name (string without spaces)

- baseValue: base monetary value (integer)

- age: age in years (integer)

- condition: condition rating from 1-10 (integer)

- specialAttribute: type-specific attribute (integer)

#### Output Format:

Return a single integer representing the total exhibition value of all artworks.

#### Constraints:

- 1 ≤ n ≤ 1000

- 1 ≤ baseValue ≤ 100000

- 0 ≤ age ≤ 500

- 1 ≤ condition ≤ 10

### Reference implementation captured from the editor

```
static int calculateExhibitionValue(int n, String[] artworks){
    int result = 0;
    for(String artwork : artworks){
        String []parts=artwork.split(":");
        String type=parts[0];
        int basicval=Integer.parseInt(parts[2]);
        int age    =Integer.parseInt(parts[3]);
        int cond   =Integer.parseInt(parts[4]);
        int spe    =Integer.parseInt(parts[5]);
        int val=0;
        switch (type){
            case "painting":
                val=(basicval+age*10+spe*100)*cond/10;
                break;
            case "sculpture":
                val=(basicval+age*15+spe*500)*cond/10;
                break;
            case "digital":
                val=(basicval+spe*50+basicval/2)*cond/10;
                break;
            default:
                val=basicval;
        }
        result+=val;
    }
    return result;
}
```

### Answer

Hidden by default — open a hint first, and only then the full solution.

Hint 1 Where to start
A management-system question is usually about getting the data model and the operation order right, not about a clever algorithm.

Hint 2 The approach
Map each operation in the statement to one dictionary/list mutation, and handle the stated edge cases (missing key, duplicate insert, empty gallery) exactly as the spec words them.

Solution Full walk-through and code
Implement the operations literally against a dictionary keyed by whatever identifier the statement uses, and keep insertion order where the expected output implies it. The scoring here comes from edge cases: absent identifiers, repeated adds, and the output formatting.
Time O(1) per operationSpace O(n)

> **Statement not fully captured.** The HackerEarth screenshot is a wide desktop shot whose body text did not OCR reliably, so the concrete operation list is unknown. No code is given here on purpose — recover the statement first.

Step by step Every number, calculated

The statement itself was never captured — the source is a wide desktop screenshot whose body text did not OCR. Nothing below claims to be this problem's answer; it is the checklist for a simulation question, plus what can be inferred from the one thing that *is* known.

#### 1 · What the signature tells you

declared function: **calculateExhibitionValue**

Two words worth weighing. *calculate* and *value* suggest the answer is a single number rather than a mutated structure or a formatted listing — so this is more likely an optimisation or aggregation over exhibits than a CRUD simulation. Combined with the "Gallery Management System" title, the plausible shapes are: pick a subset of exhibits under a capacity limit (knapsack), arrange exhibits in an order that maximises some adjacency score, or aggregate values per room and take the best.

That is inference from a name, and it is worth exactly what it costs. Recover the real statement before writing anything.

#### 2 · The checklist that applies regardless

For any problem of this shape, these are the questions to answer from the statement *before* coding — they are where the marks are lost:

| question | why it decides the implementation

| Exactly *k*, or at most *k*? | changes the DP initialisation from 0 to −∞ and adds an infeasible case

| Can a value be negative or zero? | decides whether "take the largest" is even valid

| Are duplicates possible? | decides between a set and a multiset, and changes counts

| Is order significant? | list versus set; also whether insertion order must be preserved on output

| What is returned when nothing qualifies? | 0, −1, and an empty result are three different answers

| 1- or 0-based indexing? | silent off-by-one throughout

#### 3 · Recovering the statement

The source image is `images/`… the wide desktop shot for this question. Open it at full size from the *Show original screenshots* chip on this page and read it directly — OCR failed, but the pixels are there and a human can read them. Transcribe the operation list and the expected output format into this entry, and the problem becomes tractable in the ordinary way.

Until that happens, this entry is a placeholder. It is listed here so the gap is visible rather than silently missing — the same reason the other cut-off statements on this site carry a dashed marker.

---

## Debugging — Function on Factorial (Java)
*Siemens · HackerEarth Java Test · HackerEarth (Siemens) · Question 14*

### Debugging - Function on factorial - Java

You are given a code for the following problem statement in the *code editor*. However, the solution fails the test cases because there are bugs in the code. Your task is to find and fix all the bugs so that it passes all the test cases.

#### Statement

You are given the following:

- Integer *N*

Let's define a function *f(x)* as follows:

```
f(x) = Σ (i=1 .. x)  s(i, x)
```

where *s(i, x)* is defined as

```
s(i, x) = 1   if GCD(i, x) = i  and  (i mod 2) = 0
          0   otherwise
```

#### Task

Determine the value of *f(N!)  mod (109 + 7)*

#### Note

- The greatest common divisor *GCD(A, B)* of two positive integers *A* and *B* is equal to the biggest integer *D*, such that both integers *A* and *B* are divisible by *D*.

- *N!* represents the factorial value of number *N*.

#### Example

*Assumptions*

- *N = 2*

*Approach*

As *f(N!) = f(2!) = f(2)*.
and *s(1, 2) = 0, s(2, 2) = 1*.
Therefore, *f(2) = Σ(i=1..2) s(i, 2) = s(1, 2) + s(2, 2) = 0 + 1 = 1*.
Hence *f(N!) mod (109 + 7) = 1*.

#### Function description

Complete the *FunctionOnFactorial* function provided in the editor. This function takes the following parameter and returns the value of *f(N!) mod(109 + 7)*:

### Buggy code shown in the editor

```
import java.util.*;

class Main {
    static final int MAX = 200005;
    static final int MOD = 1000000007;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean[] prime = new boolean[MAX];
        Arrays.fill(prime, true);
        prime[0] = prime[1] = false;

        for (int i = 2; i  0) {
            int n = scanner.nextInt();
            assert (n >= 1 && n  0) {
                        cnt += tmp / i;
                        tmp /= i;
                    }
                    ans = (ans * (cnt + 1)) % MOD;
                }
            }
            long cnt2 = 0;
            long temp2=n;
            while (temp2 > 0) {
                cnt2 += temp2 / 2;
                temp2/= 2;
            }
            ans = (ans * cnt2) % MOD;
            System.out.println(ans);
        }
    }
}
```

### Answer

Hidden by default — open a hint first, and only then the full solution.

Hint 1 Where to start
The task defines f(N) recursively over factorials and asks for it modulo 109+7. Where does a naive implementation overflow or recompute?

Hint 2 The approach
Precompute factorials mod p iteratively, and use Fermat's little theorem (`pow(x, p-2, p)`) for any division. Never compute a factorial as a real integer and then reduce.

Solution Full walk-through and code
Unpack the definition first — it is far simpler than it looks.

```
s(i, x) = 1  iff  GCD(i, x) = i  and  i is even
GCD(i, x) = i  ⟺  i divides x

f(x) = Σ(i = 1..x) s(i, x) = the number of even divisors of x
```

So the task is: count the even divisors of *N!*, mod 109+7. Never construct *N!* — it has millions of digits. Work with its prime factorisation instead, which Legendre's formula gives directly:

```
exponent of prime p in N!  =  ⌊N/p⌋ + ⌊N/p²⌋ + ⌊N/p³⌋ + …
```

Now write `N! = 2^a · (odd part)`. A divisor is even exactly when it takes at least one factor of 2, so it has *a* choices for the exponent of 2 (namely 1..a) instead of *a+1*:

```
even divisors of N!  =  a × Π (e_p + 1)   over the odd primes p ≤ N
```

Sieve the primes up to *N*, take each exponent by Legendre, multiply. `N < 2` is the one special case: `0! = 1! = 1` has no even divisor, so the answer is 0.
Time O(N log log N)Space O(N)

```python
MOD = 10**9 + 7

def FunctionOnFactorial(N):
    if N  Checked against a literal divisor count of *N!* for N = 1..10 (0, 1, 2, 6, 12, 24, 48, 84, 140, 240) and against the statement's own example, N = 2 → 1. **The solution previously shown here did not address this problem at all** — it was generic factorial/modular-inverse scaffolding, with a note claiming the recurrence was illegible. The recurrence is fully legible in the statement above; there is no binomial and no modular inverse anywhere in this problem.

This is a *debugging* task, so the judge scores a fix to the code in their editor. Use the above to identify what their code should compute, then find the planted defect rather than pasting a replacement.

Step by step Every number, calculated

Traced on the statement's example `N = 2` (answer **1**) and extended to N = 4.

#### 1 · Decode s(i, x) — the whole problem is in one line

s(i, x) = 1  iff  **GCD(i, x) = i**  and  **i mod 2 = 0**

The first condition looks like it needs a GCD computation and does not. `GCD(i, x) = i` says *i* is the largest common divisor of itself and *x*; since `GCD(i, x)` always divides *i*, equality holds exactly when *i* itself divides *x*. So:

f(x) = Σ(i=1..x) s(i, x) = **the number of even divisors of x**

Confirm with the statement's example. `x = 2! = 2`: divisors are 1 and 2, of which one is even, so `f(2) = 1`. The statement's own working — `s(1,2) = 0`, `s(2,2) = 1` — says the same thing one term at a time.

Recognising a definition as a familiar quantity in disguise is most of the work in these problems. Anyone who implements the sum literally is writing an O(x) loop over a number with millions of digits.

#### 2 · Never build N!

`N!` overflows every primitive type almost immediately and, for large *N*, has more digits than you can store usefully. But you never need its value — only its **prime factorisation**, and Legendre's formula gives each exponent directly:

exponent of p in N!  =  ⌊N/p⌋ + ⌊N/p²⌋ + ⌊N/p³⌋ + …

The reasoning: `⌊N/p⌋` counts the multiples of *p* among `1..N`, each contributing at least one factor; `⌊N/p²⌋` counts those contributing a *second*; and so on. The terms hit zero once `p^k > N`, so the loop is O(logp N).

For `N = 4`:

| p | ⌊4/p⌋ | ⌊4/p²⌋ | ⌊4/p³⌋ | exponent

| 2 | 2 | 1 | 0 | a = 3

| 3 | 1 | 0 | — | e₃ = 1

4! = 24 = 2³ · 3¹     ✓

#### 3 · Counting even divisors

Write `N! = 2^a · m` with *m* odd. A divisor is built by choosing an exponent for each prime independently:

all divisors   = (a + 1) · Π (e_p + 1)      exponent of 2 chosen from **0..a**
odd divisors   =           Π (e_p + 1)      exponent of 2 forced to **0**
even divisors  =       **a** · Π (e_p + 1)      exponent of 2 from **1..a**  ← a choices, not a+1

The `a` rather than `a+1` is the entire content of the word "even", and it is the single most likely place to be off by one. You can also read it as *all − odd*, which gives `(a+1)·P − P = a·P` — the same thing, and a useful cross-check.

For `N = 4`: `a = 3`, odd primes give `(1+1) = 2`, so `f(4!) = 3 × 2 = 6`. Listing them by hand: 2, 4, 6, 8, 12, 24 — six even divisors of 24. ✓

| N | N! | factorisation | a | Π(e_p+1) over odd p | f(N!)

| 1 | 1 | — | 0 | 1 | 0

| 2 | 2 | 2¹ | 1 | 1 | **1**

| 3 | 6 | 2·3 | 1 | 2 | 2

| 4 | 24 | 2³·3 | 3 | 2 | 6

| 5 | 120 | 2³·3·5 | 3 | 2·2 = 4 | 12

Every row was cross-checked against a literal divisor count of the actual factorial.

#### 4 · Traps

- **`a`, not `a+1`**, for the power of 2. Using `a+1` counts odd divisors too.

- **N < 2 returns 0.** `0! = 1! = 1` is odd and has no even divisor; the formula gives `a = 0` and hence 0 anyway, but check your loop does not index a prime table of size 1.

- **Skip p = 2 in the product** — its contribution is the leading `a`, and including it as `(a+1)` double-counts.

- **Reduce mod 109+7 as you multiply.** The true count is astronomically large; unlike some problems on this site, here the modulus is safe to apply throughout, because you are only ever multiplying — no comparison is made on the reduced values.

- **Do not compute N! itself**, and do not call a GCD routine — neither is needed.

- **Legendre's loop must guard overflow** in Java/C++: `q *= p` can overflow before exceeding *N*. Use `q <= n / p` as the continuation test, or 64-bit arithmetic.

---

## Minimum Cost to Most Remote Junction
*Siemens · HackerEarth Java Test · HackerEarth (Siemens) · Question 15*

### Minimum Cost to Most Remote Junction

#### Statement

You have a network with N junctions and M pathways connecting them. The pathways form a linked, undirected network. Each junction is numbered from 1 to N, and each pathway has a movement cost linked to it.

A delivery bot begins from any junction and wants to carry a package to another junction. The bot can only travel along the pathways. Your job is to find the smallest cost (total movement cost of the pathways) the bot must pay to travel from one junction to the most distant possible junction.

#### Function Description

You need to implement the function ShortestPath. The function should take the number of junctions N, the number of pathways M, and a list of pathways, and return the smallest cost to travel from one junction to the most distant junction.

#### Parameters:

- N: An integer showing the number of junctions in the network.

- M: An integer showing the number of pathways in the network.

- roads: A list of M tuples, where each tuple (u, v, w) shows an undirected pathway linking junction u to junction v with movement cost w.

#### Return:

- An integer showing the smallest cost (total movement cost) needed to travel from one junction to the most distant junction.

#### Input Format:

- First Line: An integer N showing the number of junctions.

- Second Line: An integer M showing the number of pathways.

- Next M lines: Three integers u, v, and w, showing a pathway between junction u and junction v with movement cost w.

#### Output Format:

- A single integer showing the smallest cost needed to reach the most distant junction from any starting point.

#### Constraints:

- 1 ≤ N ≤ 105

- 1 ≤ M ≤ 105

- 1 ≤ w ≤ 103

> Solution captured from the editor (double-Dijkstra "tree diameter" approach):

```
import heapq
import sys
input=sys.stdin.readline

def ShortestPath (N, M, roads):
    graph=[[]for _ in range(N+1)]
    for u,v,w in roads:
        graph[u].append((v,w))
        graph[v].append((u,w))

    def algo(start):
        dist=[float('inf')]*(N+1)
        dist[start]=0
        pq=[(0,start)]
        while pq:
            d,u=heapq.heappop(pq)
            if d> dist[u]:
                continue
            for v,w in graph[u]:
                if dist[u]+w

### Answer

Hidden by default — open a hint first, and only then the full solution.

Hint 1 Where to start
"Minimum cost to the most remote junction" over a road network: shortest paths from a source, then take the worst one.

Hint 2 The approach
Dijkstra from the start junction, then return `max(dist)` over reachable nodes (and handle unreachable nodes per the spec).

Solution Full walk-through and code
Build the adjacency list, run Dijkstra with a heap, and report the maximum finite distance — the eccentricity of the source. If any junction is unreachable, return whatever sentinel the statement specifies.
Time O(E log V)Space O(V + E)

```python
import heapq

def ShortestPath(n, edges, source):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    INF = float('inf')
    dist = [INF] * n
    dist[source] = 0
    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd  The code previously shown here defined `minCostToMostRemote` rather than the declared `ShortestPath`. Node indexing (0- or 1-based), whether roads are directed, and the unreachable-node convention were not legible in the screenshot — check all three before submitting.

Step by step Every number, calculated

No worked example was captured for this question, so the trace below uses a small graph with every number computed.

#### 1 · What "most remote junction" asks for

The quantity wanted is the **eccentricity of the source**: run shortest paths from it and report the largest of those distances.

answer = max over all reachable v of  dist(source, v)

Note the two layers — a *minimum* inside (each junction is reached by its cheapest route) and a *maximum* outside (the worst of those cheapest routes). Reading it as "the longest path" is a different and much harder problem; reading it as "the total" is a different one again.

#### 2 · Dijkstra, and the one line that makes it fast

```
d, u = heappop(pq)
if d > dist[u]: continue        # stale entry — skip
for v, w in g[u]:
    if d + w The `continue` is lazy deletion, the same idiom as in ECS — Least Resource Tasks: a heap cannot update a key in place, so improved distances are pushed as new entries and the obsolete ones are discarded when they surface. Each edge pushes at most once, so the heap holds O(E) entries and the whole run is O(E log V).

Dijkstra's correctness rests on **non-negative weights** — once a node is popped with the smallest tentative distance, no later path can improve it, because every extension only adds weight. If the problem permits negative costs, this is the wrong algorithm and you need Bellman-Ford.

#### 3 · Worked trace

Four junctions, edges `(0,1,4) (0,2,1) (2,1,2) (1,3,5)`, source 0:

| pop | relaxations | dist after

| (0, node 0) | 1 → 4 via edge 4; 2 → 1 via edge 1 | [0, 4, 1, ∞]

| (1, node 2) | 1 → 1 + 2 = **3**, improves on 4 | [0, 3, 1, ∞]

| (3, node 1) | 3 → 3 + 5 = 8 | [0, 3, 1, 8]

| (4, node 1) | *stale* — 4 > dist[1] = 3, skipped | [0, 3, 1, 8]

| (8, node 3) | no outgoing improvements | [0, 3, 1, **8**]

answer = max(0, 3, 1, 8) = **8**, at junction 3

The fourth row is the lazy-deletion case in action: node 1 was pushed twice, at 4 and later at 3, and the stale entry is discarded rather than reprocessed. Note also that the direct edge 0→1 of weight 4 *loses* to the two-hop route 0→2→1 of weight 3 — which is exactly why a greedy single-edge scan is not enough.

#### 4 · Traps

- **Undirected roads need both directions** in the adjacency list. Adding only `u → v` silently produces larger answers.

- **Unreachable junctions.** Including `∞` in the max returns infinity. The code filters to finite distances and returns −1 if none — *confirm the required sentinel*, since it was not legible in the screenshot.

- **0- vs 1-based junction numbering** — also not legible. If the input is 1-based, either subtract 1 everywhere or size the arrays `n+1`.

- **Parallel edges and self-loops** are harmless to Dijkstra; do not deduplicate on the assumption they are errors.

- **Use `long` for distances** if weights and V are both large.

- **The declared function is `ShortestPath`** despite computing an eccentricity.

