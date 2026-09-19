# Stacks

> A stack is not a box you keep things in. It is the answer to one question —
> *which unfinished thing must I deal with first?* — and the answer is always:
> the most recent one.

## When you reach for it

You reach for a stack when the problem has **deferred obligations that must be
settled in reverse order of when they arose**. You open a bracket, and you owe a
closing one; if you open another before paying that debt, the second debt must be
paid first. That is the whole shape. Nesting, undo, recursion, and "cancel with
the thing immediately before me" are all the same shape wearing different words.

162 problems in this bank use a stack, which puts it at #26 of 150. They fall
into six families, and it is worth learning the families rather than the
problems:

- **Matching and nesting.** *Valid Parentheses* (five companies ask it here),
  *Balancing Parentheses*, *Rich Text Parser Part 1 (Validate Tokens)*,
  *Minimum Parenthesis Removals and Their Indices*.
- **Cancellation that cascades.** *Backspace String Compare*, *Compare Character
  Arrays with Backspaces*, *Eliminate Substring* and *Get Final String* — remove
  every occurrence of `AWS` until none remain.
- **Undo.** *Command Undo Data Structure*, *Simple Text Editor*. The history of
  what you did is a stack by definition.
- **Recursion made explicit.** *Find File Paths in a Directory Tree* and
  *Lowest Common Ancestor Implemented with Stack* both say, in the statement,
  to use a stack instead of recursion. *Binary Tree Preorder Traversal* is the
  same conversion.
- **Evaluation.** *Stack Language Evaluator*, *Stack Command Output*,
  *Flatten Nested Map Paths with a Stack* — a machine whose only memory is a
  stack is enough to evaluate postfix and to track nesting context.
- **Nearest smaller / greater.** *Final Price Discount*, *The Prom*. This family
  is large enough to have its own chapter: [[monotonic-stack]].

The tool is wrong when the obligation you must settle next is the **oldest**
one, not the newest — "serve customers in arrival order", "process the request
queue" — that is a [[queue]]. It is wrong when you need to reach into the middle
by value or by rank: "the smallest element currently present" under arbitrary
removals is a [[heap]] or an [[ordered-set]]. And it is wrong when the intervals
you are matching **cross** rather than nest; crossing structure is what
[[sweep-line]] is for, and no stack discipline can express it.

One honest anti-signal. If the statement has exactly one kind of bracket, a
single integer counter does the job, because a stack whose elements are all
identical carries no information beyond its height. *Balancing Parentheses* is
that problem. Reach for the real stack when the elements differ — bracket kinds,
indices, contexts, values.

## The idea

**Keep only the part of what you have read that is still unresolved, and keep it
in the order you opened it.**

That sentence is the chapter. The stack is not a copy of the input; it is the
*residue* of the input — the prefix you have read, with everything already
settled deleted from it. Whatever is still open sits in the stack, and the thing
you opened most recently sits on top, which is precisely where the next
character can reach.

Physically it is an array plus one index. `top` names the last occupied slot;
push writes at `top + 1` and increments; pop reads at `top` and decrements.
Nothing else moves. That is the entire reason both operations are O(1): every
other element keeps the index it already had.

<svg viewBox="0 0 660 190" role="img" aria-label="an array of six slots, four occupied, with a top index; push writes one slot right and pop reads at top">
  <g>
    <rect class="fill" x="40" y="60" width="70" height="46" rx="4"/>
    <rect class="fill" x="110" y="60" width="70" height="46" rx="4"/>
    <rect class="fill" x="180" y="60" width="70" height="46" rx="4"/>
    <rect class="fill" x="250" y="60" width="70" height="46" rx="4"/>
    <rect x="320" y="60" width="70" height="46" rx="4"/>
    <rect x="390" y="60" width="70" height="46" rx="4"/>
    <text x="75" y="88" text-anchor="middle">(</text>
    <text x="145" y="88" text-anchor="middle">[</text>
    <text x="215" y="88" text-anchor="middle">{</text>
    <text x="285" y="88" text-anchor="middle">(</text>
    <text x="40" y="40">bottom: opened first</text>
    <line x1="285" y1="128" x2="285" y2="110"/>
    <text x="285" y="146" text-anchor="middle">top</text>
    <line x1="355" y1="128" x2="355" y2="110"/>
    <text x="355" y="146" text-anchor="middle">push writes here</text>
    <text x="490" y="78">pop: read a[top], top -= 1</text>
    <text x="490" y="100">push: a[top+1] = x, top += 1</text>
    <text x="40" y="176">no other element ever moves — that is why both are O(1)</text>
  </g>
</svg>

The algorithmic move that follows from this picture is what I will call the
**scan-and-reduce loop**, and almost every stack problem in the bank is an
instance of it:

```python
stack = []
for c in s:
    if stack and cancels(stack[-1], c):
        stack.pop()          # the debt is settled; both characters disappear
    else:
        stack.append(c)      # a new debt
```

Read it as a rewriting machine. You have a rule — "`(` followed by `)` deletes
itself", "a letter followed by `#` deletes itself", "the three characters `AWS`
delete themselves" — and you apply it the instant it becomes applicable. The
stack always holds a string to which no rule applies.

That is a strong claim, and it is the one worth proving properly, because it
explains what the code does not: why a *single left-to-right pass* suffices even
when a deletion creates a brand-new match between characters that were far apart
in the input.

## Worked by hand

Take *Eliminate Substring*: remove every occurrence of `AWS` from a string, and
keep going until none remain, since a removal can bring new letters together.
Input `AAWSWS`.

The scan pushes each character and, after each push, checks whether the top three
characters spell `AWS`.

| step | char | stack before | top 3 spell `AWS`? | stack after |
| --- | --- | --- | --- | --- |
| 1 | `A` | `` | no (too short) | `A` |
| 2 | `A` | `A` | no (`AA`) | `AA` |
| 3 | `W` | `AA` | no (`AAW`) | `AAW` |
| 4 | `S` | `AAW` | **yes** (`AWS`) | `A` |
| 5 | `W` | `A` | no (`AW`) | `AW` |
| 6 | `S` | `AW` | **yes** (`AWS`) | `` |

The stack ends empty, so the answer is the empty string — which this problem asks
you to report as `"-1"`.

Three things in that trace are invisible in the code.

**The cascade is free.** Step 6 deleted an `AWS` whose `A` is at input position 0
and whose `S` is at input position 5 — three characters apart in the original
string, brought together by the deletion in step 4. The scan never went back to
look. It did not have to, because after step 4 the correct context for the next
comparison was already sitting at the top of the stack. A `str.replace` pass does
not have this property: one pass over `AAWSWS` produces `AWS`, not the empty
string, and you would have to loop until the string stops changing, which is
O(n²) on inputs built to make it so.

**At most one deletion fires per character.** Look at step 4: after removing the
three characters the stack is `A`, and we do *not* have to re-check. That is not
luck — the stack held no match before the push, so deleting a suffix leaves a
prefix of something already clean. The inner "keep reducing" loop that everybody
writes is, for a single pattern, never entered twice.

**The stack is a string, not a set.** Order is the information: a multiset of
pending characters could not tell `AW` from `WA` at step 6.

The same trace for brackets is worth drawing rather than tabulating, because the
picture explains the two ways a bracket string can fail:

<svg viewBox="0 0 660 230" role="img" aria-label="running balance of two bracket strings, one returning to zero and one dipping below zero">
  <g>
    <line x1="30" y1="140" x2="630" y2="140"/>
    <text x="30" y="36">stack height while scanning</text>
    <polyline points="40,140 95,110 150,80 205,110 260,80 315,110 370,140" fill="none"/>
    <text x="67" y="164" text-anchor="middle">(</text>
    <text x="122" y="164" text-anchor="middle">(</text>
    <text x="177" y="164" text-anchor="middle">)</text>
    <text x="232" y="164" text-anchor="middle">(</text>
    <text x="287" y="164" text-anchor="middle">)</text>
    <text x="342" y="164" text-anchor="middle">)</text>
    <text x="205" y="196" text-anchor="middle">ends at zero, never below: valid</text>
    <polyline points="430,140 470,110 510,140 550,170 590,140" fill="none"/>
    <circle class="fill" cx="550" cy="170" r="6"/>
    <text x="450" y="164" text-anchor="middle">(</text>
    <text x="490" y="164" text-anchor="middle">)</text>
    <text x="530" y="164" text-anchor="middle">)</text>
    <text x="570" y="164" text-anchor="middle">(</text>
    <text x="510" y="196" text-anchor="middle">dips below zero, and ends above it</text>
    <text x="510" y="216" text-anchor="middle">two independent ways to be invalid</text>
  </g>
</svg>

A string is valid when the curve never dips below the axis **and** finishes on
it. Dipping below is a `)` with nothing to close; finishing above is a `(` never
closed. Two different failures, two different checks, and forgetting the second
one is the single most common bug in this topic.

## Why it is correct

The informal argument — "the stack holds the unmatched brackets" — is a
restatement, not a proof. Here is the real statement, general enough to cover
brackets, backspaces and substring elimination at once.

:::proof The stack is always the fully reduced form of the prefix read so far
**Setup.** Fix an alphabet Σ and a finite set `R` of non-empty *patterns* over
Σ. To *reduce* a string, delete one occurrence of a pattern; the two remaining
halves concatenate. A string is *irreducible* if no pattern occurs in it as a
factor. Assume:

- **(A1)** no non-empty proper suffix of a pattern is a prefix of a pattern
  (patterns cannot partially overlap each other or themselves);
- **(A2)** no pattern occurs as a factor of another pattern.

Consider the algorithm: `S := ε`; for each character `c` of the input, append
`c` to `S`, then, if some pattern is a suffix of `S`, delete it.

**Uniqueness of normal forms.** Every rule shortens the string, so no infinite
reduction exists; the system terminates. If two distinct pattern occurrences
exist in one string, (A1) forbids a partial overlap and (A2) forbids one being
contained in the other, so they are disjoint; deleting either leaves the other
intact, and the two orders reach the same string. The system is therefore
locally confluent, and by Newman's lemma (terminating plus locally confluent
implies confluent) every string `w` has a *unique* irreducible form, written
`NF(w)`.

**Invariant.** After the algorithm has consumed `s[0..i)`, the stack — read
bottom to top as a string — equals `NF(s[0..i))`.

**Base case.** `i = 0`. The stack is `ε`, which is irreducible, and `NF(ε) = ε`.

**Inductive step.** Assume the stack holds `S = NF(s[0..i))` and let `c = s[i]`.
The algorithm forms `S·c` and looks for a pattern suffix. Two lemmas.

*Lemma 1 — only the top can fire.* Any occurrence of a pattern in `S·c` must
contain the final character: an occurrence avoiding it lies entirely inside `S`,
contradicting that `S` is irreducible. An occurrence containing the final
character of `S·c` is a suffix of it. So testing suffixes finds every applicable
rule, and by (A2) at most one pattern can be a suffix (two suffixes of the same
string are nested, and the shorter would be a factor of the longer). There is
never a choice to get wrong.

*Lemma 2 — one deletion is enough.* If pattern `p` is a suffix of `S·c`,
deleting it leaves a string that is a prefix of `S`. Every factor of a prefix of
`S` is a factor of `S`, and `S` is irreducible, so the result is irreducible. If
no pattern is a suffix, then by Lemma 1 `S·c` is already irreducible.

Either way the new stack `T` is irreducible, and it was obtained from `S·c` by
legal reductions. Since `S` was itself obtained from `s[0..i)` by legal
reductions, `T` is reachable from `s[0..i+1)`; being irreducible and reachable,
and normal forms being unique, `T = NF(s[0..i+1))`. The invariant is restored.

**Termination.** Each input character is pushed exactly once, and each deletion
removes characters that were pushed earlier and never returns them. So the number
of pops is at most the number of pushes, the outer loop runs exactly `n` times,
and the algorithm performs at most `2n` stack operations before halting.

**Conclusion.** At `i = n` the stack is `NF(s)`.

*For brackets*, take `R = {"()", "[]", "{}"}`, which satisfies (A1) and (A2). A
string is well-formed exactly when `NF(s) = ε`: every well-formed string contains
an innermost adjacent pair whose deletion leaves a well-formed string (induction
on length), and conversely a string reducible to `ε` is built from `ε` by
inserting matched pairs, which is well-formed. So "the stack is empty at the end"
is the correct and complete test. *For backspaces*, take
`R = {x# : x ∈ letters}`; the extra convention that a `#` against an empty text
disappears is the `if stack:` guard, and it too deletes a suffix (the empty one),
so the induction is unchanged. ∎
:::

Now name what the proof leaned on, because that list is where the bugs live.

- **(A1) and (A2) are real conditions, not boilerplate.** The pattern `aba`
  violates (A1), and on `ababa` the two deletion orders give `ba` and `ab`: two
  normal forms, so the task itself is ambiguous and the scan silently returns
  one of them. `AWS` has no such self-overlap, which is why *Eliminate Substring*
  is well posed.
- **Only suffixes are tested.** Lemma 1 is what licenses looking at the top and
  nowhere else. If your rule can fire in the middle of the residue — "delete any
  two adjacent equal letters *anywhere*, but only if the string is shorter than
  ten" — the induction collapses.
- **Reading strictly left to right, with no lookahead.** The invariant is about a
  prefix; a rule that depends on characters not yet read has no prefix to be an
  invariant about.
- **The stack is the whole state.** Nothing is remembered outside it. If you
  maintain a side counter — a running sum, a minimum, a depth — you have added a
  second invariant, and now every push and every pop must restore both. That is
  where min-stacks and *Adding Stack 2.0* go wrong.
- **Nothing in the proof mentioned speed.** Correctness does not depend on the
  array being amortised, on avoiding `pop(0)`, or on the pattern check being
  O(1). If the answer is wrong, those lines are not the suspect.

:::note Why "the most recent unmatched opener" is also the *minimum* removal
*Minimum Parenthesis Removals and Their Indices* asks for the indices the scan
leaves behind, and promises that their count is the minimum possible number of
deletions. That is a separate claim, and it is an exchange argument.

Deleting characters to make a bracket string valid is the same as choosing a set
of non-crossing matched pairs to keep, so minimum deletions equals
`n − 2·(maximum matching)`. Suppose an optimal solution matches a `)` at index
`j` with an opener at index `i′`, while the greedy would match it with the most
recent unmatched opener `i > i′`. If `i` is unmatched in the optimal solution,
replace `(i′, j)` by `(i, j)`: still `i < j`, same count. If `i` is matched in
the optimal solution to some `j″`, then `j″ > j` (because `i` is the most recent
unmatched opener before `j`, so everything the optimal solution paired with
`i` lies later), and we may swap to `(i, j)` and `(i′, j″)`, which is valid since
`i′ < i < j < j″`. Either way the count is unchanged and the solution agrees with
the greedy on one more position. Induct: the greedy attains the maximum.
:::

## What it costs

**The scan.** Each character of the input is pushed exactly once. Each pop
destroys an element that was pushed earlier and is never restored, so over the
whole run

```
pops ≤ pushes = n
```

and the total number of stack operations is at most `2n`. This is a counting
argument, not an amortised one — no potential function is needed, because the
bound is on the entire run, not on any individual step. With a pattern of length
`k`, each step also compares up to `k` characters, giving **Θ(nk)** time, which
is Θ(n) for the constant-length patterns every one of these problems uses.

**Space is Θ(n), and that is not negligible.** The worst case for
*Valid Parentheses* is `((((((…`, where nothing cancels and the stack holds the
entire input. If a statement demands O(1) extra space the stack formulation is
out: *Backspace String Compare* has a [[two-pointers|two-pointer]] alternative
that walks both strings from the right, counting pending deletions in an integer.

**The array underneath.** `list.append` is not literally O(1); it is amortised
O(1), and the derivation is worth carrying. A doubling array holding `n` elements
has been resized at sizes `1, 2, 4, …, 2^k ≤ n`, and each resize copies that many
elements, so the total copying is

```
1 + 2 + 4 + … + 2^k < 2^(k+1) ≤ 2n
```

Add the `n` writes and `n` pushes cost less than `3n` steps, i.e. at most 3 per
push. The same result with a potential function: let `Φ = 2·size − capacity`
(non-negative once the array is at least half full). An ordinary push has actual
cost 1 and raises `Φ` by 2, so its amortised cost is 3. A resizing push copies
`size` elements, actual cost `size + 1`, while `Φ` falls from `size` to 2, so its
amortised cost is `size + 1 + 2 − size = 3`. Constant either way. See
[[amortized-analysis]]. Shrinking must use hysteresis — halve the capacity only
when the array falls to a *quarter* full — or an alternating push/pop pair at the
boundary pays Θ(n) every time.

**The costs people forget**, in the order they cost people time:

- *Building the answer with `+=`.* `out = out + c` inside the loop copies the
  whole string each time: Θ(n²), a comfortable timeout at the `10^5` bound that
  *Eliminate Substring* and *The Prom* both carry. Collect into the list and call
  `''.join(stack)` once, which is Θ(n).
- *Using `pop(0)` or `insert(0, x)`.* Each is Θ(n) because every other element
  shifts; a stack must grow at the end. Something that needs both ends wants a
  [[deque]].
- *The recursion you avoided.* An explicit stack of integers costs a machine word
  each; a recursive call costs a frame — hundreds of bytes — and Python stops at
  about 1000 of them. That is precisely why *Find File Paths in a Directory Tree*
  specifies an explicit stack at 20000 paths. A per-character dictionary lookup
  is expected O(1) ([[hash-tables]]) but not free either.

## The implementation

```python run
import random


def valid_parentheses(s):
    """True iff every bracket is closed by its own kind, in order."""
    opener = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s:
        if c in opener:
            if not stack or stack.pop() != opener[c]:
                return False          # a ')' with nothing (or the wrong thing) under it
        else:
            stack.append(c)
    return not stack                  # leftovers are openers that were never closed


def unmatched_indices(s):
    """Indices left over when each ')' takes the most recent unmatched '('."""
    stack, orphans = [], []
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        elif stack:
            stack.pop()
        else:
            orphans.append(i)
    return sorted(orphans + stack)


def eliminate(s, pattern):
    """Delete every occurrence of `pattern`, cascading, in one pass."""
    k, stack = len(pattern), []
    for c in s:
        stack.append(c)
        if len(stack) >= k and ''.join(stack[-k:]) == pattern:
            del stack[-k:]
    return ''.join(stack)


def backspace(s):
    stack = []
    for c in s:
        if c == '#':
            if stack:
                stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)


for t in ["()[]{}", "([{}])", "([)]", "((", ")(", ""]:
    print("  valid(%-8r) = %s" % (t, valid_parentheses(t)))
assert valid_parentheses("([{}])") and valid_parentheses("")
assert not valid_parentheses("([)]") and not valid_parentheses("((")

print("unmatched indices of '())(()' :", unmatched_indices("())(()"))
assert unmatched_indices("())(()") == [2, 3]

print("str.replace once on 'AAWSWS' :", repr("AAWSWS".replace("AWS", "")))
print("the stack scan on  'AAWSWS'  :", repr(eliminate("AAWSWS", "AWS")))
assert eliminate("AAWSWS", "AWS") == ""


def by_repeated_deletion(s, p):       # the O(n^2) definition, as a reference
    while p in s:
        s = s.replace(p, "", 1)
    return s


rng = random.Random(5)
for _ in range(2000):
    t = "".join(rng.choice("AWS") for _ in range(rng.randint(0, 14)))
    assert eliminate(t, "AWS") == by_repeated_deletion(t, "AWS"), t
print("2000 random strings: one pass agrees with repeated deletion")

print("backspace('ab#c') =", repr(backspace("ab#c")), " backspace('###a') =", repr(backspace("###a")))
assert backspace("ab#c") == "ac" and backspace("###a") == "a"
assert backspace("a#c") == backspace("b#c")
```

Three lines are carrying the weight.

`if not stack or stack.pop() != opener[c]` does two jobs in one expression, and
the order matters. `not stack` is tested first, so `stack.pop()` never runs on an
empty list — Python's `or` short-circuits. Write the guard the other way round
and you get an `IndexError` on the input `")"`. Popping inside the condition is
safe here only because a mismatch returns immediately; if you had to continue,
you would peek with `stack[-1]` and pop separately.

`return not stack` is the second failure mode from the balance diagram. Delete
it and replace it with `return True` and every test with balanced prefixes still
passes; only `"(("` and its friends break. Half the wrong submissions to
*Valid Parentheses* are exactly this line.

`''.join(stack)` at the end, rather than a string accumulated in the loop, is the
difference between Θ(n) and Θ(n²) at the `10^5` bound.

## Variants you will meet

**Monotonic stack.** Maintain the stack in sorted order by popping everything
that the incoming element dominates. Each element enters and leaves once, so the
scan is still Θ(n), and what you get is "the nearest smaller element to the
right" for free. *Final Price Discount* asks for exactly that; *The Prom* pairs
each boy with the nearest unpaired girl ahead of him, which is the same scan with
the roles renamed. Full treatment in [[monotonic-stack]].

**Stack with an O(1) aggregate.** Push a pair — the value, and the running
minimum (or maximum, or sum) of everything at or below this position. Pop
discards both, so nothing is ever recomputed. *Stack with Constant-Time Middle
Queries* is the same trick with a different summary, and *Adding Stack 2.0* is
the cleverest member: `inc i v` cannot touch `i` elements in O(1), so it records
a lazy increment at depth `i` and pushes the debt down only on a pop.

**A queue from two stacks.** Arrivals go on one stack, departures come off the
other, and the outbox is refilled only when it runs dry — which reverses the
order exactly once. *Implement a Queue Using Two Stacks* appears twice in this
bank. The block below measures the amortised claim rather than asserting it. See
[[queue]] and [[amortized-analysis]].

```python run
import random
from collections import deque


class QueueFromTwoStacks:
    """FIFO out of two LIFOs. `inbox` takes arrivals, `outbox` serves them."""

    def __init__(self):
        self.inbox, self.outbox, self.moves = [], [], 0

    def push(self, x):
        self.inbox.append(x)

    def _expose_front(self):
        if not self.outbox:                       # only when the outbox is dry
            while self.inbox:
                self.outbox.append(self.inbox.pop())
                self.moves += 1

    def pop(self):
        self._expose_front()
        return self.outbox.pop()

    def peek(self):
        self._expose_front()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox


q = QueueFromTwoStacks()
for v in (1, 2, 3):
    q.push(v)
print("push 1,2,3 -> pop", q.pop(), "| peek", q.peek(), "| pop", q.pop())
assert q.peek() == 3 and not q.empty()

q, ref, pushes = QueueFromTwoStacks(), deque(), 0
rng = random.Random(4)
for _ in range(20000):
    if not ref or rng.random() < 0.5:
        v = rng.randrange(1000)
        q.push(v)
        ref.append(v)
        pushes += 1
    elif rng.random() < 0.5:
        assert q.pop() == ref.popleft()
    else:
        assert q.peek() == ref[0]
    assert q.empty() == (not ref)
print("20000 random operations agree with collections.deque")
print("pushes:", pushes, " transfers between the stacks:", q.moves,
      "-> at most one move per element")
assert q.moves <= pushes
```

**Undo, and undo with redo.** One stack of applied commands; `UNDO` pops and
inverts. *Command Undo Data Structure* multiplies and adds an integer, so store
the previous state rather than the operation — cheaper than inverting a
multiplication by zero. Redo is a second stack, and *Simple Text Editor* states
the rule that makes it one: typing after an undo clears the redo history.

**An explicit stack in place of recursion.** Push the work items you have not
done yet; pop, do a constant amount, push the successors. *Find File Paths in a
Directory Tree* and *Lowest Common Ancestor Implemented with Stack* require this
in the statement. Two things change versus recursion: you choose the order by
choosing the push order (for preorder over a binary tree, push the right child
first so the left is popped first), and local variables you relied on must become
part of the pushed item. See [[recursion]], [[dfs]] and [[tree-traversal]].

**Parsing with a stack of contexts.** Each opener pushes a context and each
closer pops it, and the stack read bottom-to-top *is* the path from the root.
*Flatten Nested Map Paths with a Stack* joins that path with dots to form
`parent.child.key=value`; *Convert Stack Samples to Trace Events* compares two
consecutive stacks, where the longest common prefix is exactly the set of calls
that stayed open. See [[parsing]], and [[recursive-descent]] when the grammar has
precedence rather than pure nesting.

**Postfix evaluation.** Operands push, operators pop their arity and push the
result. *Stack Language Evaluator* adds `dup`, `swap` and `drop`; *Stack Command
Output* is the two-instruction version. The pop order is the trap: the first
value popped is the **right** operand.

**Greedy with a stack.** *Lexicographically Minimum Stack Encryption* lets you
push the next input character or pop the top to the output, and asks for the
smallest possible output: pop while the top is at most the minimum of the unread
suffix. Precompute suffix minima, then one pass. The difficulty is entirely in
the [[greedy-exchange|exchange argument]] that justifies the rule.

**Batch deletion by predicate.** *Stack Batch Removal* drops every element below
or above a threshold. Each element is destroyed at most once, so the work is
amortised linear — but the elements removed need not be at the top, so this is no
longer a pure stack.

## Recognising it in a statement

Ordered by how much you should trust the signal.

1. **Explicit nesting.** Brackets, tags, nested maps, directory trees, a
   structure that "can itself contain more groups" — the phrase
   *Rich Text Parser Part 1* uses. Nesting is a stack; there is no second answer.
2. **"The most recent" / "the last unmatched".** *Minimum Parenthesis Removals*
   says "match each closing parenthesis with the most recent unmatched opening
   parenthesis" in the statement. That is the definition of a stack.
3. **Undo, or "revert exactly one previously executed command".**
4. **The statement tells you to use one.** "Traverse the tree with an explicit
   stack rather than recursion" — *Find File Paths in a Directory Tree* and
   *Lowest Common Ancestor Implemented with Stack* both do this, and the hidden
   requirement is the input size, which would blow a recursion limit.
5. **Cancellation between adjacent items, repeated until stable.** Backspaces,
   `AWS` removal, "remove adjacent duplicates". The words *until no more remain*
   are the tell, and the stack turns that repetition into one pass.
6. **"Nearest smaller/greater to the left/right"**, or a price/height/temperature
   array where each element looks for the next one that beats it —
   [[monotonic-stack]].
7. **Postfix or prefix expressions, or a tiny instruction set with `push`/`pop`.**
8. **A `10^5` bound on a process described as "repeat until nothing changes".**

The anti-signals:

- **Arrival order.** "First come, first served", "in the order received",
  BFS level order — [[queue]], not a stack. If you cannot decide, ask which end
  the next item comes from.
- **Access by rank or value.** "The k-th largest so far", "the minimum after
  arbitrary removals" — [[heap]] or [[ordered-set]].
- **One bracket kind and only a yes/no answer.** A counter is enough, and it uses
  O(1) space. *Balancing Parentheses* asks for the number of insertions, which is
  two counters: unmatched closers seen, plus openers left over.
- **Crossing rather than nesting.** Overlapping intervals, tags that interleave —
  [[sweep-line]] or [[intervals]].

## Traps

**Peeking or popping without checking for empty.** Symptom: `IndexError` on the
first input that starts with a closer. The guard is always `if stack and …`.

**Forgetting the final emptiness check.** Symptom: `"(("` is reported valid,
while every balanced test passes. Demonstrated below.

**A counter instead of a stack with several bracket kinds.** Symptom: `"([)]"` is
accepted. The counter knows the depth and not the kind. Demonstrated below.

**Building the output string inside the loop, or `pop(0)` where you meant
`pop()`.** Symptom for both: correct answers, quadratic time, timeout at `10^5`.

**Pushing children in the wrong order in an explicit DFS.** Symptom: the preorder
comes out mirrored. A stack reverses what you put in, so push right before left.

**Storing values when the answer wants positions.** *Minimum Parenthesis
Removals and Their Indices* asks for indices; a stack of characters cannot
produce them. Push `i`, not `s[i]`, whenever the output is about *where*.

**Keeping a reference to a popped element.** *Generic Stack Operation Sequence*
states it outright: a popped element must not stay readable through retained
internal storage. Implement `pop` as "read `a[size-1]`, then `size -= 1`" over a
fixed-capacity array without clearing the slot and the value is still there.

**Assuming a self-overlapping pattern behaves.** Removing `aba` from `ababa` has
two different answers. Check that the pattern has no proper border before
trusting the one-pass scan.

```python run
def by_counter(s):
    """Wrong once there is more than one kind: depth forgets the kind."""
    depth = 0
    for c in s:
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def forgets_the_end(s):
    opener = {')': '(', ']': '[', '}': '{'}
    st = []
    for c in s:
        if c in opener:
            if not st or st.pop() != opener[c]:
                return False
        else:
            st.append(c)
    return True                       # bug: openers left on the stack are ignored


def right(s):
    opener = {')': '(', ']': '[', '}': '{'}
    st = []
    for c in s:
        if c in opener:
            if not st or st.pop() != opener[c]:
                return False
        else:
            st.append(c)
    return not st


print("%-10s %9s %9s %9s" % ("input", "counter", "no-end", "correct"))
for t in ["()[]{}", "([{}])", "([)]", "((", "(()", ")(", ""]:
    print("%-10r %9s %9s %9s" % (t, by_counter(t), forgets_the_end(t), right(t)))

assert by_counter("([)]") and not right("([)]")
assert forgets_the_end("((") and not right("((")
assert all(by_counter(t) == right(t) for t in ["()[]{}", "((", ")(", ""])
print()
print("counter accepts '([)]': the depth is right, the kinds are not")
print("no-end  accepts '((' : underflow is checked, leftovers are not")
print("the two bugs fail on different inputs, so one test case catches neither")
```

## What to memorise

Almost nothing. One loop, one sentence, one habit.

**The loop**, which should come out of your fingers without thought:

```python
stack = []
for c in s:
    if stack and cancels(stack[-1], c):
        stack.pop()
    else:
        stack.append(c)
# stack now holds exactly what never got resolved, in order
```

**The sentence** that turns a problem into it: *"Is the next thing I have to
settle always the most recent thing I have not settled?"* If yes, the stack is
the structure and the only remaining question is what to push — a character, an
index, a context, or a pair of (value, running aggregate).

**The habit**: before writing the loop, say in one sentence what the stack
*contains*. Not "the characters" — the actual claim: "the opening brackets that
are still unclosed, oldest at the bottom". Every bug in this topic is that
sentence being false at some moment: a guard missing, a final check missing, an
index pushed where a value was needed. And write `if stack and …` before you write
`stack[-1]`, every time, as one motion.

Numbers worth carrying: a scan does at most `2n` stack operations, because pops
are bounded by pushes; `n` pushes into a doubling array copy fewer than `2n`
elements, so `append` is amortised O(1) with a constant near 3; Python's
recursion limit is about 1000, so any tree or graph with `10^5` nodes needs the
explicit stack; and `pop()` is O(1) while `pop(0)` is O(n).

## Check yourself

:::check
`"AAWSWS"` becomes the empty string after all `AWS` removals, but a single pass
of `str.replace` leaves `"AWS"`. Why does the one-pass stack scan get the right
answer without ever looking backwards?
--
Because the stack is not the input — it is the input with everything already
deleted removed. After a deletion, the characters that have become adjacent in
the *reduced* string are adjacent on the stack too, so the very next comparison
sees them.

Formally, that is Lemma 1 of the proof: the stack always holds an irreducible
string, so a new occurrence of the pattern can only be created at the boundary
where the new character lands. Checking the top is checking everywhere. A
`str.replace` pass works on the original string, where the surviving `A` at
position 0 and the `S` at position 5 are still three characters apart.
:::

:::check
Someone says: "*Valid Parentheses* does not need a stack — just count openers and
closers, and check the counter never goes negative and ends at zero." Where are
they wrong, and when are they right?
--
They are wrong as soon as there is more than one kind of bracket. The counter
records the depth and discards the kind, so `"([)]"` gives the balance sequence
1, 2, 1, 0 and is accepted, although no valid matching exists. The runnable trap
block above shows exactly this.

They are right when there is exactly one kind. Then every stack element is the
same symbol, so the stack carries no information beyond its height, and an
integer is a faithful — and O(1)-space — encoding of it. *Balancing Parentheses*
is that problem: the answer is (unmatched closers seen along the way) + (openers
left at the end), which is two counters and no stack at all.
:::

:::check
A colleague objects to the two-stack queue: "a single `pop` can move `n`
elements, so this is not an O(1) queue." Where are they wrong, and where are they
right?
--
Wrong about the total. Each element is transferred from the inbox to the outbox
at most once in its lifetime — the transfer only happens when the outbox is
empty, and an element never goes back. So over `m` operations the transfers total
at most the number of pushes, and the amortised cost per operation is O(1). The
runnable block measures this: transfers never exceed pushes.

Right about the individual operation. The worst case for one `pop` really is
Θ(n), and that matters whenever you care about the tail and not the average: a
latency budget per request, a real-time system, or an immutable/persistent
version of the structure where the expensive step could be forced repeatedly and
the amortised argument — which assumes each state is used once — stops being
valid.
:::

:::check
The correctness proof assumed (A1): no non-empty proper suffix of a pattern is a
prefix of a pattern. Construct an input that breaks the algorithm when (A1)
fails, and say what exactly goes wrong.
--
Pattern `aba`, input `ababa`. Its suffix `a` is also its prefix, so (A1) fails.
Deleting the occurrence at positions 0–2 leaves `ba`; deleting the one at 2–4
leaves `ab`. Both results are irreducible, so the normal form is not unique and
"remove every occurrence until none remain" does not specify a single answer.

The stack scan picks whichever occurrence completes first while reading left to
right — here, positions 0–2, leaving `ba`. It is not wrong so much as arbitrary:
the specification is ambiguous, and Newman's lemma no longer applies because
local confluence has failed. The practical lesson is to check that the pattern
has no proper border (as `AWS` does not) before trusting a one-pass reduction.
:::

:::check
You are converting a recursive preorder traversal to an explicit stack, and the
output comes out as root, right subtree, left subtree. What did you do, and why
does the fix look backwards?
--
You pushed the left child before the right child. A stack returns what you pushed
in reverse order, so the last one pushed — the right child — is popped first.

The fix is to push the right child first and the left child second, which reads
backwards but is right: the correct rule is that **the order you want to visit is
the reverse of the order you push**. This is the general shape of the
recursion-to-stack conversion. Recursion visits its calls in source order because
each call completes before the next begins; a stack has no such sequencing, so
you must reverse the pushes yourself. *Binary Tree Preorder Traversal* is the
smallest place to get this wrong.
:::
