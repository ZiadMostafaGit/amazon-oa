# Recognising the Pattern from the Statement

> Recognition is not recall. It is reading a statement for the three or four
> features that survive a change of story, and letting those features index a
> catalogue you already own.

## When you reach for it

Plainly, first: no problem in this collection practises this topic. The bank
tags each problem with the algorithm it needs, and "recognising the pattern" is
not an algorithm — it is what you do in the four minutes before you have one. It
is here because it is the highest-leverage skill in a timed interview, and
because every other chapter in this book is inert if you cannot tell which one
to open.

You reach for it at a specific moment: you have read the statement, you can say
in your own words what is being asked, and you still do not know what to type.
That is the moment. If you cannot yet restate the problem, you are not here —
you are in [[problem-decomposition]], and reaching for a pattern before you can
restate the problem is how people end up solving a neighbouring question very
efficiently.

The shape that makes this the right tool: the statement asks for one of a small
number of stock quantities (the longest something, the smallest maximum, the
k-th something, the number of ways), about one of a small number of stock
objects (array, string, tree, graph, interval, integer), under constraints that
were obviously chosen rather than discovered. Those three facts are a
fingerprint, and fingerprints are for looking up.

The shape that makes it the wrong tool: the problem is genuinely new. Then the
catalogue has no entry, and matching stops being retrieval and becomes
invention — you take the nearest-looking entry and bend the problem to fit it.
The honest move is to go to [[optimisation-path]]: write the brute force, see
what it wastes, remove the waste. Recognition is the fast path, not the only
path, and knowing which one you are on is part of the skill.

## The idea

A statement is not a puzzle to be solved from cold. It is a specimen to be
*keyed out*.

Biologists identifying an unfamiliar beetle do not flip through every beetle
they know. They use a dichotomous key: a short sequence of questions about
features — how many segments in the antenna, is the wing case fused — where each
answer discards most of the remaining possibilities. Nobody memorises the
beetles. They memorise the questions.

That is the whole mental image. You are not searching your memory for a problem
that looks like this one. You are asking a fixed, short list of questions about
the statement, and each answer cuts the catalogue down.

The questions are these, in this order:

1. **What is the object, and what may I do to it?** An array, a string, a tree,
   a graph, intervals, a number. And: may I reorder it? Must the answer be
   contiguous? Do I see the whole input at once? Is it mutable? Is extra space
   allowed?
2. **What exactly is asked for?** Not the story — the quantity. Existence, a
   count, an extremum, the object achieving it, all of them, the k-th, the
   smallest maximum, the lexicographically smallest, the number of ways.
3. **What does the budget allow?** Read `n` from the constraints and convert it
   into a permitted complexity class. This question does not need the statement
   at all, which makes it the most reliable of the three.
4. **What is the asymmetry?** The tiebreak. Every clean problem has something
   much easier than the thing being asked: checking an answer rather than
   building one, values that happen to live in `1..n`, a tiny `k` beside a huge
   `n`, everything appearing twice except one thing. That is where the intended
   solution hides.

<svg viewBox="0 0 640 300" role="img" aria-label="a funnel: three questions cutting a catalogue of 150 patterns down to one or two">
  <g>
    <rect x="40" y="26" width="560" height="30" rx="4"/>
    <text x="255" y="47">150 patterns</text>
    <line x1="320" y1="56" x2="320" y2="86"/>
    <text x="336" y="78">Q1  the object, and what I may do to it</text>
    <rect x="110" y="86" width="420" height="30" rx="4"/>
    <text x="290" y="107">≈ 30</text>
    <line x1="320" y1="116" x2="320" y2="146"/>
    <text x="336" y="138">Q2  the quantity actually asked for</text>
    <rect x="200" y="146" width="240" height="30" rx="4"/>
    <text x="300" y="167">≈ 6</text>
    <line x1="320" y1="176" x2="320" y2="206"/>
    <text x="336" y="198">Q3  what the constraint budget allows</text>
    <rect class="fill" x="280" y="206" width="80" height="30" rx="4"/>
    <text x="303" y="227">1–2</text>
    <text x="40" y="266">the questions multiply, so three of them</text>
    <text x="40" y="286">do the work of 150 separate comparisons</text>
  </g>
</svg>

The reason this works is that the questions are about *invariants of the
problem*, not about its vocabulary. A statement about delivery trucks and a
statement about server load can be the same problem; the trucks and the servers
are costume. What is not costume is that both ask for the smallest capacity that
makes something feasible, that feasibility is cheap to check, and that the
answer lives in a range of size `10^9`. Change the story, and those three facts
do not move.

## Worked by hand

Here is a statement. It is one I wrote for this chapter, not one from the bank:

> You are given `n` positive integers (`2 ≤ n ≤ 2·10^5`, each at most `10^9`)
> and an integer `k` with `1 ≤ k ≤ n`. Divide the sequence into exactly `k`
> contiguous groups. The cost of a division is the largest group sum. Return the
> smallest achievable cost.

Key it out. After each question, record which candidates survive.

| # | question | what the statement says | survivors |
| --- | --- | --- | --- |
| — | start | — | the whole catalogue |
| 1 | object, allowed operations | array of numbers; order is fixed ("contiguous"); read-only; whole input available | sliding window, prefix sums, Kadane, partition DP, binary search on answer, greedy |
| 2 | quantity asked for | a single number; the *smallest* possible *largest* group sum | partition DP, binary search on answer |
| 3 | budget | `n = 2·10^5`; `O(n²)` is `4·10^10`, out; `O(n log 10^9)` is `6·10^6`, fine | binary search on answer |
| 4 | asymmetry | "is there a division with cost ≤ X into at most k groups?" is one greedy pass | binary search on answer, confirmed |

Four questions, one survivor. Notice what each did.

Question 1 barely helped: it eliminated the tree, graph, string and geometry
families, which is most of the catalogue by count but none of the difficulty. Six
candidates is still six.

Question 2 did the real cutting, and it did it on five words. "Smallest
achievable largest" is a stock phrase; the quantity being minimised is itself a
maximum. Almost nothing in the catalogue produces that shape, which is exactly
why the phrase is worth so much.

Question 3 broke the remaining tie without looking at the statement's meaning at
all. Partition DP solves this problem correctly. It is also `O(n²k)` with `n` at
`2·10^5`, so it is a correct solution the setter has deliberately put out of
reach. The constraint line is the setter telling you which of two correct answers
they want, and it is the only part of a statement a story cannot rewrite.

Question 4 was not selection but *falsification*: having a candidate, I tried to
break it. The check "can I do it with cost ≤ X?" is a single pass — start a new
group whenever the next number would overflow `X` — and it is monotone in `X`,
because a bigger budget can copy any division a smaller one managed. Both had to
be true, and I confirmed them rather than assumed them.

And here is the thing the trace shows that the finished code never would: in step
4 I used the guarantee that the integers are **positive**. If they could be
negative, the greedy "start a new group when the next number would overflow the
budget" is not optimal, and the feasibility check is wrong even though the binary
search around it is fine. That word `positive` in the constraint line was
load-bearing, and I only noticed because I traced the argument instead of jumping
to the template.

Keep a running note of which sentences you have actually consumed. If one is
still unused when you finish, either it is a red herring or your pattern is
wrong. In interviews it is almost never a red herring.

## Why it is correct

"Correct" needs care here. There is no theorem that says a human will identify
the right pattern — recognition can simply fail. What *can* be proved is that
the procedure above spends its time in the right order: given a shortlist of
candidates, testing them in decreasing ratio of *how likely* to *how expensive
to test* minimises the expected time until you are holding the right one. That is
the claim, and it is an exchange argument.

:::proof The ratio rule for testing candidate patterns
**Setup.** You hold a shortlist of candidate patterns `P₁ … Pₙ`. Exactly one of
them is right. You believe `Pᵢ` is the right one with probability `pᵢ > 0`, where
`Σ pᵢ = 1`. Testing `Pᵢ` — writing down what it would require of the statement
and checking the statement against it — costs `cᵢ > 0` minutes, and the test is
exact: it answers yes if and only if `Pᵢ` is the right pattern. You test
candidates one at a time in some order `π` and stop at the first yes.

**Objective.** The expected time spent testing under order `π` is

    E(π) = Σ_k  p_{π(k)} · ( c_{π(1)} + c_{π(2)} + … + c_{π(k)} )

— if the right pattern sits at position `k`, you paid for the first `k` tests.

**Claim.** `E` is minimised by any order in which `pᵢ / cᵢ` is non-increasing.

**Exchange step.** Take any order `π` and any adjacent pair of positions, holding
`a` then `b`. Let `S` be the total cost of everything strictly before them; note
that `S` does not depend on the order of `a` and `b`, and neither does the cost
paid by any candidate after them, since `cₐ + c_b` is the same either way. So the
only terms that differ between `π` and the order `π'` obtained by swapping `a`
and `b` are the two contributed by `a` and `b` themselves:

    E(π)  − E(π')  =  [ pₐ(S + cₐ) + p_b(S + cₐ + c_b) ]
                    − [ p_b(S + c_b) + pₐ(S + c_b + cₐ) ]
                   =  p_b·cₐ − pₐ·c_b.

Everything else cancels. So swapping `a` and `b` strictly helps exactly when
`p_b·cₐ > pₐ·c_b`, that is, when `pₐ/cₐ < p_b/c_b`.

**Conclusion.** If an order is not sorted by non-increasing `pᵢ/cᵢ`, then some
*adjacent* pair is out of ratio order — otherwise the sequence of ratios would be
non-increasing everywhere — and swapping that pair strictly decreases `E`. Since
there are finitely many orders and each such swap strictly decreases a real
quantity, no non-sorted order can be optimal. Conversely all ratio-sorted orders
have equal cost, because the exchange difference `p_b cₐ − pₐ c_b` is zero for
adjacent ties. Hence the ratio-sorted orders are exactly the optimal ones. ∎

**Termination.** The procedure performs at most `n` tests. If all `n` fail, you
have not wasted the time: you have proved the problem is not in your catalogue,
which is the signal to stop searching and start deriving.
:::

Now the part that matters more than the proof — what the proof assumed, because
every assumption is a real failure mode with a name.

**Exactly one candidate is right.** Two patterns often both work, and then the
ratio rule is still fine — you want the cheapest correct one. The dangerous
direction is the other: the shortlist may contain *no* correct pattern, and
someone who has assumed otherwise will accept the least-bad fit rather than
conclude the list is exhausted. That is the most expensive recognition failure
there is, and it is why the termination clause above is written down.

**The test is exact.** The proof needs a test with no false positives. Human
tests are riddled with them: "yes, this is a sliding window" is a feeling, not a
test. The repair is to make the test falsifiable before you run it — name the
property the pattern *requires* ("the window predicate must be monotone: adding
an element can only make it worse"), then check the statement for that property
specifically. A test you cannot fail is not a test.

**Costs are fixed and independent of order.** The proof needs `cᵢ` not to change
depending on what you tested earlier. Often false, and pleasantly so: checking
monotonicity for [[binary-search-on-answer]] does most of the work of checking
the exchange property for a [[greedy-exchange|greedy]]. When tests share work,
the true optimisation is harder than a sort, and the practical advice becomes:
group candidates that share a test and pay for the shared part once.

**The probabilities are yours, and they are biased.** `pᵢ` is your belief, not a
fact, and it drifts towards whatever you practised most recently. The only cure
is measurement: log what you guessed and what it turned out to be.

## What it costs

Two different costs matter: how many questions recognition needs, and what a
wrong recognition costs you.

**How many questions.** Let the catalogue hold `K` patterns. A recognition
procedure that asks questions with binary answers can, after `q` questions, have
followed at most `2^q` distinct paths, and therefore can name at most `2^q`
distinct patterns. To distinguish all `K` you need `2^q ≥ K`, so

    q ≥ log₂ K.

With `K = 150` — the size of this book's catalogue — that is `log₂ 150 ≈ 7.2`, so
**eight yes/no questions suffice in principle**. This is the same counting
argument that gives the lower bound in [[binary-search]], and it has the same
moral: the catalogue being large is not the problem. Asking questions that do not
split it is.

A question with `m` possible answers is worth `log₂ m` bits, so the four
questions above are worth roughly: object and its permitted operations, maybe 5
distinguishable answers (2.3 bits); quantity asked for, maybe 6 (2.6 bits);
budget class, maybe 5 (2.3 bits). Total ≈ 7.2 bits — which is exactly the budget
needed. That is not a coincidence so much as a design target: the four questions
were chosen to be the ones that split the catalogue most evenly. A question like
"does the problem mention an array?" is nearly worthless not because arrays are
unimportant but because the answer is yes for most of the catalogue, so it
carries a fraction of a bit.

**What a wrong recognition costs.** This is the cost people forget, and it
dominates. Model one attempt as: `c` minutes to test the hypothesis, then `I`
minutes to implement it, and let `f` be the probability that you were wrong but
believed you were right. Attempts are independent-ish, so the number of attempts
until success is geometric with mean `1/(1−f)`, and

    E[total] ≈ (c + I) / (1 − f).

Put in numbers — any numbers — and the shape of the answer appears. With `c = 2`,
`I = 20`, `f = 0.30`: `22 / 0.7 ≈ 31.4` minutes. Now spend twice as long testing
and suppose that halves-and-halves-again your false positive rate: `c = 4`,
`f = 0.05`: `24 / 0.95 ≈ 25.3` minutes. You spent two extra minutes on doubt and
bought back six. The derivative is what matters: `∂E/∂c = 1/(1−f)` is about 1,
while `∂E/∂f = (c+I)/(1−f)²` is about 45. Effort spent reducing `f` is roughly
forty times better than effort spent reducing `c`. Falsify, do not hurry.

**Space.** You must hold one trigger sentence per pattern, not one
implementation per pattern — roughly `K` sentences. Implementations can be
re-derived from the idea in minutes; triggers cannot be re-derived at all.

**The budget arithmetic.** Converting `n` into a complexity class is the one
mechanical step, and the working convention — a convention, not a measurement —
is that around `10^8` elementary operations fit in a second. The useful part is
not the constant but which side of the line you are on: at `n = 2·10^5`, `n²` is
`4·10^10` and `n log n` is about `3.6·10^6`, four orders of magnitude apart. No
constant factor closes that.

## The implementation

The "implementation" of a recognition procedure is a key: a table of patterns,
each with the features it *requires*, and a rule for ordering the survivors. The
code below does no language understanding whatsoever. You answer the four
questions by hand; the code keeps the books.

```python run


# name, required features, prior, minutes to test, ops as a function of n
CATALOGUE = [
    ("sliding-window", {"object": {"array", "string"}, "span": {"contiguous"},
                        "asked": {"longest", "shortest"}, "shrinkable": {True}},
     0.12, 2.0, lambda n: n),
    ("kadane", {"object": {"array"}, "span": {"contiguous"},
                "asked": {"best-value"}}, 0.05, 1.5, lambda n: n),
    ("prefix-sums", {"object": {"array"}, "span": {"contiguous"},
                     "asked": {"count"}}, 0.08, 1.5, lambda n: n),
    ("binary-search-on-answer", {"object": {"array"}, "asked": {"minimax"},
                                 "checkable": {True}}, 0.06, 3.0,
     lambda n: n * 30),
    ("partition-dp", {"object": {"array"}, "span": {"contiguous"},
                      "asked": {"minimax", "best-value"}}, 0.03, 5.0,
     lambda n: n * n),
    ("meet-in-the-middle", {"object": {"array"}, "span": {"any-subset"},
                            "asked": {"closest"}}, 0.01, 4.0,
     lambda n: 2 ** min(n // 2, 64)),
    ("subsets", {"object": {"array"}, "span": {"any-subset"},
                 "asked": {"closest", "enumerate"}}, 0.03, 2.0,
     lambda n: 2 ** min(n, 64)),
    ("xor-tricks", {"object": {"array"}, "asked": {"the-odd-one"}},
     0.02, 1.0, lambda n: n),
]
BUDGET = 1e8

def key_out(f):
    """Return (ranked survivors, names cut by the budget alone)."""
    fits, too_slow = [], []
    for name, wants, prior, cost, ops in CATALOGUE:
        if any(f.get(k) not in v for k, v in wants.items()):
            continue                          # a required feature is absent
        if ops(f["n"]) > BUDGET:
            too_slow.append(name)             # right idea, wrong budget
        else:
            fits.append((prior / cost, name))
    fits.sort(reverse=True)
    return fits, too_slow

STATEMENTS = [
    ("split into k contiguous groups, minimise the largest group sum",
     {"object": "array", "span": "contiguous", "asked": "minimax",
      "checkable": True, "shrinkable": False, "n": 200000},
     "binary-search-on-answer"),
    ("longest substring with at most two distinct characters",
     {"object": "string", "span": "contiguous", "asked": "longest",
      "checkable": False, "shrinkable": True, "n": 100000}, "sliding-window"),
    ("largest sum of a contiguous block; values may be negative",
     {"object": "array", "span": "contiguous", "asked": "best-value",
      "checkable": False, "shrinkable": False, "n": 100000}, "kadane"),
    ("n <= 40; pick any subset whose sum is closest to a target",
     {"object": "array", "span": "any-subset", "asked": "closest",
      "checkable": False, "shrinkable": False, "n": 40}, "meet-in-the-middle"),
    ("every value appears twice except one; O(1) extra space",
     {"object": "array", "span": None, "asked": "the-odd-one",
      "checkable": False, "shrinkable": False, "n": 100000}, "xor-tricks"),
]

for text, feats, expected in STATEMENTS:
    ranked, cut = key_out(feats)
    print(text)
    print("   test in this order:", [n for _, n in ranked] or ["(nothing fits)"])
    if cut:
        print("   fits the features but blows the budget:", cut)
    assert ranked and ranked[0][1] == expected, (text, ranked)

ranked3, _ = key_out(STATEMENTS[2][1])
assert "sliding-window" not in [n for _, n in ranked3]
print("\nnegatives make the window non-shrinkable, so it is not a candidate")
```

Three lines are doing the real work.

`if any(f.get(k) not in v for k, v in wants.items())` is a **conjunction**. A
pattern survives only when *every* feature it requires is present. That is the
difference between a key and a keyword search: "subarray" alone means nothing;
"contiguous, longest, and shrinkable" means sliding window. Recognition failures
are almost always a missing conjunct.

`ops(f["n"]) > BUDGET` is question 3, and in the output you can watch it earn its
place twice. For the first statement, partition DP fits every feature and is cut
purely on `n²`. For the fourth, plain subset enumeration fits every feature and
is cut purely on `2⁴⁰`; [[meet-in-the-middle]] survives because `2²⁰` does not.
In both cases the features alone left two candidates and only the arithmetic
separated them.

`fits.sort(reverse=True)` on `(prior / cost, name)` is the ratio rule from the
proof. It is not ranking by likelihood — a very likely pattern that takes ten
minutes to rule out should sometimes wait behind a less likely one you can
dismiss in thirty seconds.

The `shrinkable` flag is the only feature in the table that is not a surface
property. It encodes "extending the window can only hurt, so shrinking from the
left can only help" — the monotonicity that licenses [[two-pointers]] at all.
With negatives that property fails, which is why the third statement gets
[[kadane]] and not [[sliding-window]]. A key is only as good as its least
superficial question.

Now the proof's ordering claim, checked by brute force rather than believed:

```python run
from itertools import permutations
import random

def expected_cost(order, p, c):
    total, spent = 0.0, 0.0
    for i in order:
        spent += c[i]
        total += p[i] * spent
    return total

random.seed(7)
for _ in range(300):
    n = 5
    raw = [random.randint(1, 9) for _ in range(n)]
    p = [x / sum(raw) for x in raw]
    c = [float(random.randint(1, 9)) for _ in range(n)]
    best = min(permutations(range(n)), key=lambda o: expected_cost(o, p, c))
    ratio = tuple(sorted(range(n), key=lambda i: -p[i] / c[i]))
    assert abs(expected_cost(ratio, p, c) - expected_cost(best, p, c)) < 1e-12
print("ratio order matched the brute-force optimum in 300/300 instances")

p = [0.5, 0.3, 0.2]
c = [6.0, 1.0, 1.0]
print("\nlikeliest-first :", expected_cost((0, 1, 2), p, c))
print("ratio-first     :", expected_cost(tuple(sorted(range(3),
      key=lambda i: -p[i] / c[i])), p, c))
assert expected_cost((1, 2, 0), p, c) < expected_cost((0, 1, 2), p, c)

print("\nfalse positives dominate:  E = (c + I) / (1 - f),  I = 20 min")
for c_test, f in ((2.0, 0.30), (2.0, 0.15), (4.0, 0.05)):
    print("   test %.0f min, wrong %2.0f%% of the time -> %5.1f min"
          % (c_test, 100 * f, (c_test + 20.0) / (1 - f)))
assert (4.0 + 20.0) / 0.95 < (2.0 + 20.0) / 0.70
print("doubling the checking time and cutting f from 30% to 5% is a clear win")
```

## Variants you will meet

Recognition arrives by several different routes, and it helps to know which one
you are on.

**By object.** The statement hands you a structure and the structure names the
family: parentheses and "nearest greater" hand you a [[monotonic-stack]],
prefixes of words hand you a [[trie]], "are these two things connected" over time
hands you [[union-find]].

**By quantity.** The asked-for thing names the family regardless of the object:
"minimise the maximum" is [[binary-search-on-answer]], "k-th largest" is
[[quickselect]] or [[top-k]], "number of ways" is [[counting-dp]].

**By budget.** The constraints alone name the family: `n ≤ 20` means subset
enumeration or [[dp-bitmask]], `n ≤ 40` means [[meet-in-the-middle]], `n ≤ 5000`
means an `O(n²)` DP is intended, `n ≥ 10^9` means the answer is arithmetic, not
iteration. See [[complexity-analysis]].

**By asymmetry.** The free guarantee names the family: values are a permutation
of `1..n` ([[cyclic-sort]]), everything pairs up except one thing
([[xor-tricks]]), checking is cheap but constructing is not
([[binary-search-on-answer]] again).

**By reduction, not recognition.** The problem is not in the catalogue but a
transformation of it is. Cities and roads become a graph; states and moves become
a graph; string edits become a grid. This is [[graph-modelling]] and
[[state-design]], and it separates people who have memorised patterns from people
who can use them.

**By elimination.** Sometimes the useful output is negative: no catalogue entry
fits, and that conclusion sends you to [[optimisation-path]] with a clear
conscience instead of forcing a template that will not hold.

**By failure and repair.** You recognise, implement, and the sample fails. Do not
start over: find which required feature the statement actually violated, then
search again with that feature explicit. See [[debugging]].

## Recognising it in a statement

Signals that you are looking at a keyed specimen rather than a novel problem,
ordered by how much they are worth:

- **A stock quantity, stated in stock words.** "Minimum number of…", "the
  smallest maximum", "the longest subarray such that…", "the number of ways to…",
  "the k-th smallest". These phrases are close to perfectly reliable, because
  they are how setters write when they have a known problem in mind.
- **Constraint numbers sitting exactly on a complexity boundary.** `n ≤ 20`,
  `n ≤ 40`, `n ≤ 5000`, `n ≤ 2·10^5`, `1 ≤ aᵢ ≤ 10^9`. Nobody picks 40 by
  accident. Constraints are the setter's handwriting, and they are the one part
  of a statement that cannot be disguised by a story.
- **A guarantee you did not need in order to state the problem.** All values
  positive; all values distinct; the array is a permutation of `1..n`; at most 26
  distinct characters; `k ≤ 10`. A free guarantee is never free — it exists
  because the intended solution consumes it.
- **A stock operation on a stock object.** "Contiguous", "in place", "O(1) extra
  space", "the tree is a BST", "the graph is a DAG", "sorted".
- **A gap between the examples and the constraints.** Examples with `n = 5`,
  constraints with `n = 10^5`. The gap is the whole problem, stated indirectly.

The anti-signals, which matter just as much:

- **Shared nouns without shared structure.** "Stock prices" appears in
  monotonic-stack problems, in DP problems and in plain scans. The noun is
  costume. If the only thing your candidate has in common with the statement is a
  word, you have matched nothing.
- **A long domain story, ordinary constraints, no stock quantity.** Usually
  [[simulation]] or [[design-data-structure]]: the difficulty is modelling the
  rules faithfully, and hunting for cleverness will cost you the interview.
- **A statement you cannot restate in one sentence.** Then the problem is
  comprehension, and recognition performed on a misread statement is worse than
  no recognition, because it comes with confidence. Back to
  [[problem-decomposition]].

## Traps

**Keyword matching instead of feature matching.** The most common failure by a
wide margin: one salient word triggers a pattern and the rest of the statement is
read as confirmation. The two statements below differ by one word and have
different answers.

```python run
def max_sum_subarray(a):            # contiguous run
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

def max_sum_subsequence(a):         # gaps allowed
    pos = [x for x in a if x > 0]
    return sum(pos) if pos else max(a)

S1 = "return the maximum sum of any contiguous subarray"
S2 = "return the maximum sum of any subsequence"

def keyword_guess(s):
    for word, pattern in (("maximum sum", "kadane"), ("sum", "prefix-sums")):
        if word in s:
            return pattern
    return "?"

def feature_guess(s):
    span = "contiguous" if ("contiguous" in s or "subarray" in s) else "any-subset"
    return {"contiguous": "kadane", "any-subset": "take-the-positives"}[span]

a = [3, -2, 5]
print("array", a)
print("  best contiguous sum :", max_sum_subarray(a), "  (3 + -2 + 5)")
print("  best subsequence sum:", max_sum_subsequence(a), "  (3 + 5, skipping -2)")
assert max_sum_subarray(a) == 6 and max_sum_subsequence(a) == 8

print("\nkeyword:", keyword_guess(S1), "/", keyword_guess(S2), " <- same guess, wrong")
print("feature:", feature_guess(S1), "/", feature_guess(S2), " <- different, right")
assert keyword_guess(S1) == keyword_guess(S2)
assert feature_guess(S1) != feature_guess(S2)
```

The symptom is an implementation that is clean, fast, passes your own mental test
and returns 6 where the grader wanted 8.

**Anchoring on the first candidate.** You name a pattern in ten seconds and then
spend four minutes gathering evidence for it. The symptom is that you never write
down a second candidate. The cure is procedural: produce at least two candidates
before testing any of them, and say what would make each of them wrong.

**Skipping the budget question.** You recognise a correct pattern that is one
complexity class too slow, and find out twenty minutes in. The symptom is a
solution that passes the samples and times out. The cure is to do question 3
first when the constraints look unusual — it takes ten seconds and needs no
understanding of the problem at all.

**Recognising the shape but not the twist.** It is a sliding window, but the
values can be negative. It is a BST, but there are duplicates. It is a shortest
path, but one edge weight is zero. The family is right and the member is wrong.
The symptom is failing exactly one sample case. The cure is question 4: after
naming the pattern, name the guarantee it needs and go find that guarantee in the
statement, literally, by pointing at the sentence.

**Matching the examples instead of the statement.** The worked example is small,
so you infer a rule it never claimed — that the array is sorted, that values are
distinct. The symptom is a solution that handles the samples and nothing else.
Examples illustrate; constraints legislate. See [[edge-cases]].

**Treating recognition as an answer.** "This is a heap problem" is a hypothesis,
not a plan. Until you can say what is in the heap, what the comparison is, and
why the top element is the one you want, you have recognised nothing. The symptom
is a confident sentence followed by a blank editor.

**Not stopping.** The shortlist runs out and you keep searching anyway, because
giving up on recognition feels like giving up on the problem. It is not. The
proof's termination clause is the permission slip: when the candidates are
exhausted, switch to brute force and improve from there.

## What to memorise

Four questions, one sentence, one habit.

**The questions**, in this order, every time:

```
1. object + allowed operations   (array/string/tree/graph/interval/number;
                                  reorder? contiguous? online? in place?)
2. the quantity asked for        (exists / count / extremum / the k-th /
                                  smallest maximum / lexicographically smallest)
3. the budget                    (n -> permitted complexity class)
4. the asymmetry                 (what is much easier than what is asked?)
```

**The sentence** that turns a statement into a candidate: *"What is much easier
here than the thing I have been asked for?"* Checking versus constructing gives
you binary search on the answer. A local decision versus a global one gives you
greedy. One more element versus the whole array again gives you a window or a
prefix. Every pattern in the catalogue is a way of exploiting one asymmetry, so
finding the asymmetry is finding the pattern.

**The habit**: after naming a candidate, say the sentence *"this would be wrong
if…"* and finish it. If you cannot finish it, you have not understood the
pattern well enough to use it. If you can finish it, go and check that specific
thing in the statement, by pointing at the sentence that rules it out. This one
habit is the `f` in the cost model, and `f` is worth forty times what speed is.

Numbers worth carrying: `log₂ 150 ≈ 7.2`, so eight good questions are enough;
`2²⁰ ≈ 10⁶`, so `n ≤ 20` means exponential is fine and `n ≤ 40` means half of it
is; `10^8` operations per second as a convention; and the boundaries `n ≤ 5000`
for `O(n²)` and `n ≤ 2·10^5` for `O(n log n)`.

## Check yourself

:::check
A statement gives `n ≤ 10^5`, asks for the length of the longest subarray whose
sum is at most `S`, and guarantees all values are positive. Key it out in four
questions, then say which guarantee you consumed and what breaks without it.
--
1. Object: array of numbers, contiguous span required, order fixed, read-only.
2. Quantity: the longest span satisfying a constraint — a stock sliding-window
   phrasing.
3. Budget: `n = 10^5` permits `O(n)` or `O(n log n)`; nothing here forces more.
4. Asymmetry: extending the window can only increase the sum, so a window that
   is too heavy can only be fixed by shrinking from the left. That is exactly the
   monotonicity two pointers need.

The consumed guarantee is **all values positive**. Without it the window sum is
not monotone in the window, shrinking from the left can *increase* the sum, and
the two-pointer scan is simply wrong — you would fall back to prefix sums plus a
search structure. Notice that the guarantee did not appear in questions 1–3 at
all. Question 4 is where guarantees get consumed, which is why skipping it is
how people produce fast wrong answers.
:::

:::check
Why is "does this problem involve an array?" a nearly worthless question, even
though almost every array problem answers yes?
--
Because the value of a question is the information it carries, and information is
about how evenly it splits the remaining candidates, not about how often it is
true. If nine tenths of the catalogue involves an array, then a yes answer
eliminates one tenth and carries `log₂(10/9) ≈ 0.15` bits — you would need about
fifty such questions to do the work of the eight from the counting argument in
"What it costs".

A good question is one whose answer you genuinely cannot predict before reading
the statement. "A number, or the object achieving it?" "Contiguous, or any
subset?" "Is checking cheaper than constructing?" Each splits the catalogue near
the middle, which is what makes it worth a whole bit.
:::

:::check
Someone says: "Testing the most likely pattern first is obviously optimal — why
would you ever check something you think is less likely?" Where are they wrong?
--
They are optimising the wrong quantity. The cost you pay is not "how many
candidates did I try" but "how many minutes did I spend", and those differ
whenever candidates cost different amounts to rule out.

The exchange argument makes it precise: swapping two adjacent candidates `a` then
`b` changes the expected cost by `p_b·cₐ − pₐ·c_b`, so `b` belongs first exactly
when `p_b/c_b > pₐ/cₐ`. Likelihood alone is only the right criterion when all the
costs are equal.

Concretely: candidate A is 50% likely and takes six minutes to rule out;
candidates B and C are 30% and 20% likely and take one minute each. Testing
A-B-C costs `0.5(6) + 0.3(7) + 0.2(8) = 6.7` minutes; testing B-C-A costs
`0.3(1) + 0.2(2) + 0.5(8) = 4.7`. The less likely candidates go first because
they are nearly free, and half the time they make the expensive test unnecessary.
The runnable block above computes exactly this pair of numbers.
:::

:::check
You are given a statement with `n ≤ 40` and asked for the subset whose sum is
closest to a target. A colleague says "subset sums, so it is DP over the sum,
like knapsack." Where are they wrong, and what question would have caught it?
--
They skipped question 3, and they read `n` while ignoring the *values*.

Knapsack-style DP over achievable sums costs `O(n · T)` where `T` is the target
or total — fine when values are small, hopeless when they are up to `10^9`, since
the DP table is indexed by sum. `n ≤ 40` is the tell: it is far too small for a
problem whose intended solution is linear in `n`, and far too large for `2ⁿ`. The
number 40 is chosen precisely so that `2^(n/2) = 2²⁰ ≈ 10⁶` is comfortable and
`2⁴⁰ ≈ 10¹²` is not, which is the signature of [[meet-in-the-middle]].

The catching question is the budget one, and specifically its second half: not
just "how big is `n`" but "what else is the complexity allowed to depend on".
Both patterns fit every feature of the statement; only the arithmetic separates
them, which is exactly what the key in "The implementation" demonstrates.
:::

:::check
Recognition can fail outright — the catalogue may not contain the problem. What
does the correctness argument in this chapter actually guarantee, and what does
it not?
--
It guarantees an *ordering*, nothing more: given a shortlist and honest estimates
of likelihood and testing cost, the ratio order minimises expected time to reach
the correct candidate, and the procedure terminates after at most `n` tests.

It does not guarantee that the shortlist contains the right pattern, and it
cannot — that depends on your catalogue, not on the procedure. This is why the
termination clause is stated as a result rather than a footnote: exhausting the
shortlist is a legitimate, informative outcome. It tells you the problem needs
deriving rather than recalling, and the correct next move is
[[optimisation-path]], not another lap through the catalogue.

So the two skills are separate and both needed. A large catalogue with no key is
slow; a good key over a small catalogue is fast and often empty-handed. Only the
pair is worth anything.
:::
