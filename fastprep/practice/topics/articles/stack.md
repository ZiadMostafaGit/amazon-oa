# Stacks

> A stack works because, at every moment, the next thing you read can only settle with the most recent thing that is still unsettled; keep the unsettled things in the order they arrived, and the one that matters is always on top.

## The problem it solves

Here are two strings of brackets:

```text
{[()()]}        ([)]
```

The first is valid: every bracket is closed by its own kind, and they close in the
reverse order of opening. The second is not. Each opener does have a closer of its
kind somewhere after it, but the `(` is opened before the `[` and closed before
it too. The pairs cross instead of nesting. That is
[[p:amazon-valid-parentheses|Valid Parentheses]], the defining stack problem, and
it appears under several companies in this bank.

The definition of "valid" contains its own brute force. A matched pair that sits
side by side, like `()` or `[]`, can be deleted without changing whether the
string is valid. So delete one, then look again, and keep going. If you end with
the empty string, it was valid. If you get stuck with something left, it was not.

```text
{[()()]}  ->  {[()]}  ->  {[]}  ->  {}  ->  (empty)      valid
([)]      ->  no adjacent matched pair anywhere           stuck: invalid
```

That is correct, and on short strings it is fine. On long ones it is slow. One pass
over the string finds and deletes the adjacent pairs, but deleting a pair can bring
two brackets together that were far apart, and you only notice on the next pass.
The worst input is deep nesting, `((((...))))` with n/2 of each. Every pass can
delete only the one pair in the middle, so there are n/2 passes, and each reads
the whole string. That is about n^2/4 character reads. At n = 10^5 that is
2.5 x 10^9.

What this chapter builds reads each character once and does at most one push or
one pop for it: 10^5 steps instead of 2.5 x 10^9. The tool is a stack, a list
where you only ever add at the end and remove from the end.

The shape to remember: **things open and must be closed, and whatever was opened
most recently must be closed first.** Brackets, nested function calls, undo,
"this character cancels the one right before it", expressions with parentheses,
nested `k[...]` groups. 346 problems in this bank use a stack, and most of them
are that shape in different words.

### When it is the wrong tool

- **The next thing to handle is the oldest, not the newest.** "Serve in arrival
  order", "process requests as they came", breadth-first search. That is a
  [[queue]].
- **You need the smallest or largest of what is present, after arbitrary
  removals.** That is a [[heap]] or an [[ordered-set]]. (A stack can carry the
  minimum of everything below each entry, but only because removals happen at the
  top. See variation D.)
- **There is only one kind of bracket and only a yes/no or a count.** Then every
  stack element is the same symbol, so the stack carries no information beyond its
  height, and an integer counter is enough.
  [[p:oracle-balance-parentheses|Balancing Parentheses]] is that problem.
- **Each element looks for the next bigger or smaller one.** That is still a
  stack, but a specific discipline with its own chapter: [[monotonic-stack]].
- **The things you match cross instead of nest.** Overlapping intervals are not
  brackets. That is [[sweep-line]] or [[intervals]].

## Build it from the brute force

We start from the repeated-deletion program, count it, find exactly where it
wastes work, and let the stack fall out as the cure.

### Step 1: the brute force, as code

```text
while some adjacent matched pair exists in s:
    delete it
valid if s is now empty
```

In Python, one pass is `s.replace("()", "").replace("[]", "").replace("{}", "")`,
and you repeat until the string stops changing. The first block in "From the idea
to the code" runs it next to the stack version (built in the next steps) and
counts how many characters each one reads.

### Step 2: count it

On `((((...))))` with n characters, each pass removes exactly one pair, the one in
the middle, because that is the only place a `(` touches a `)`. Then the next
innermost pair becomes adjacent, but this pass has already gone past it. So there
are n/2 passes, and the k-th pass reads n - 2k characters. The total is about
n^2/4.

### Step 3: notice the waste

Watch one pass on `(((())))`. It reads `(((`, finds nothing to delete, reaches the
middle `()`, deletes it. The string is now `((()))`. The next pass reads `((`
again from the start, finds nothing again, deletes the middle again.

The three `(` on the left were read in every single pass, and every time the
answer about them was the same: "nothing to delete here yet". They are waiting.
They can only ever be deleted by a `)` that arrives on their right. Rereading
them teaches you nothing.

Now look at what a deletion actually changes. Deleting a pair at positions j and
j+1 makes exactly one new pair of neighbours: the character just left of j and the
character just right of j+1. Nothing else in the string is newly adjacent. So
after a deletion, the only place a new match can appear is right there, at the
seam.

Put those two facts together. Read left to right, and keep the part you have
already read in its **reduced** form, with every possible deletion done. That
reduced part contains no adjacent matched pair; it is "stuck". When the next
character arrives, the only new neighbour pair it creates is (last character of
the reduced part, new character). Check that one pair. If it matches, delete both,
and the reduced part is stuck again. If it does not, append the new character.
Nothing else needs to be looked at, ever.

### The question that unlocks it

That is the question to ask on every problem in this family:

**When the next item arrives, which earlier item can it possibly interact with?**

For brackets, the answer is: only the most recent one that is still unresolved.
Everything older is either already resolved (deleted) or buried behind something
newer that is also unresolved. A `)` cannot reach past an unclosed `[` to close an
older `(`, because that would make the pairs cross.

So you keep the unresolved items in the order they arrived, and you only ever
touch the newest one. A list where you only touch the end is a stack: `append` to
add, `pop` to remove, `stack[-1]` to look.

Say it a second way. The reduced prefix is a pile of debts. Each opener is a debt:
"someone owes me a closer of my kind". Debts must be paid in the reverse order
they were taken on, because a closer for an old debt cannot arrive while a newer
debt is still open. So the only debt that the next closer can pay is the newest.
It is on top of the pile.

### You might think: "A counter is enough. +1 for an opener, -1 for a closer."

For one kind of bracket, that is right, and it is the best solution. For several
kinds, it is wrong. Take `([)]`. The counter goes 1, 2, 1, 0, never negative, ends
at zero, and says "valid". But the `)` arrives while the `[` is the most recent
open bracket, and a `)` cannot close a `[`.

The counter knows how many debts are open, but not **which** ones. When there is
only one kind, "how many" is all there is to know, which is why it works there.

### You might think: "Then keep one counter per kind."

Three counters, one each for `(`, `[`, `{`. On `([)]`: open `(`, open `[`, the `)`
finds an open `(` and closes it, the `]` finds an open `[` and closes it. All
counters end at zero. "Valid." Still wrong.

This is the subtler instinct, and it is the important one. The per-kind counters
check that each closer has **some** earlier opener of its kind. The real rule is
that each closer must match the **most recent** unresolved opener of any kind.
The `)` in `([)]` has an earlier `(`, but the most recent unresolved opener is the
`[`, and that is what it must close. The order between different kinds is exactly
the information the counters throw away, and it is exactly what the stack keeps.

### You might think: "After a deletion I have to look back to see if a new pair formed."

You do look, but you do not go back. After a match, you pop, and the new top is the
character that is now next to whatever comes next. That is the "seam" from step 3,
and it is always at the top. The next character will be compared with it
automatically. There is no backward scan, and no rereading.

A good test case for this: the string `AAWSWS` and the rule "delete every `AWS`
until none remain" ([[p:jpmorgan-get-final-string|Eliminate Substring]]). One
`str.replace` pass leaves `AWS`, because the second `AWS` only forms after the
first one is gone. The stack scan, traced in the next section, gets the empty
string in one pass.

### Step 4: what goes on the stack

The bracket scan pushes characters. Other problems push other things, and the
choice is the whole design:

- **the character**, when the question is "valid or not" or "what is left";
- **its index**, when the answer is about positions: which brackets to delete,
  the length of the longest valid run;
- **a context**, when an opener starts a new scope and the closer must restore the
  old one: the text built so far before a `k[`, the running sum before a `(`;
- **a (value, count) pair**, when equal neighbours merge into runs;
- **a (value, summary) pair**, when you must answer "the minimum of everything in
  the stack" in O(1): store, with each entry, the minimum of it and everything
  below it.

In every case the rule is the same: the stack holds what is still unresolved,
oldest at the bottom, newest on top, and the next item only interacts with the top.

### The technique in one sentence

**Scan left to right, keeping the unresolved part of what you have read on a
stack, oldest at the bottom; each new item is compared only with the top, which
either resolves it (pop, and the item below becomes the new top) or is left alone
(push the new item); at the end, the stack holds exactly what never got
resolved.**

And the question that produced it: **when the next item arrives, which earlier
item can it possibly interact with?** If the answer is "the most recent one still
open", it is a stack.

## Worked by hand

Get a pen. Here is the scan on `{[()()]}`, with the stack after every character.
The stack is written bottom to top, left to right, so the top is the last
character.

| step | char | it is | compared with top | action | stack after |
|---|---|---|---|---|---|
| 1 | `{` | opener | | push | `{` |
| 2 | `[` | opener | | push | `{[` |
| 3 | `(` | opener | | push | `{[(` |
| 4 | `)` | closer | top `(` matches | pop | `{[` |
| 5 | `(` | opener | | push | `{[(` |
| 6 | `)` | closer | top `(` matches | pop | `{[` |
| 7 | `]` | closer | top `[` matches | pop | `{` |
| 8 | `}` | closer | top `{` matches | pop | (empty) |

The stack ends empty: valid.

Tell step 7 in words, the way you would at a whiteboard. "I read `]`. It is a
closer, so it needs a `[`. Which open bracket can it close? Only the most recent
one that is still open, which is the top of the stack. The top is `[`. It
matches, so I pop it: that debt is paid. The stack is now just `{`, which is the
one bracket still open, and it is on top, ready for whatever comes next."

Now `([)]`:

| step | char | compared with top | action | stack after |
|---|---|---|---|---|
| 1 | `(` | | push | `(` |
| 2 | `[` | | push | `([` |
| 3 | `)` | top is `[`, needs `(` | **reject** | |

Tell step 3 in words. "I read `)`. The most recent open bracket is `[`. A `)`
cannot close a `[`. Could it close the older `(` underneath? No: that would mean
the `[` is closed after the `)`, which is the crossing the rule forbids. So the
string is invalid, and I can stop right here. Nothing that comes later can fix
it."

Look at the stack heights over time, because the picture shows the two ways to
fail.

<svg viewBox="0 0 660 230" role="img" aria-label="the stack height while scanning two bracket strings: the first rises and falls back to zero without going below it, so it is valid; the second dips below zero at its second closer and ends above zero">
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

The left curve is `(()())`. It rises with each opener, falls with each closer,
never goes below the axis, and finishes on it. The right curve is `())(`. At the
third character it would go below zero: a `)` with nothing open, the shaded dot.
And even if you ignored that, it finishes above zero: a `(` that is never closed.

So there are **two separate checks**, and they catch different strings:

- **during the scan**: a closer arrives and the stack is empty, or the top is the
  wrong kind. Reject.
- **at the end**: the stack is not empty. Some opener was never closed. Reject.

Forgetting the second check is the single most common bug in this topic. It
passes every balanced test, and only `((`-like inputs expose it. It gets its own
demonstration in the code section.

### A second trace: a cascade, where a deletion creates a new match

Now [[p:jpmorgan-get-final-string|Eliminate Substring]]: delete every `AWS`, and
keep going, because a deletion can bring new letters together. Input `AAWSWS`.
After each push, check whether the top three characters spell `AWS`.

| step | char | stack before | top three spell `AWS`? | stack after |
|---|---|---|---|---|
| 1 | `A` | (empty) | no, too short | `A` |
| 2 | `A` | `A` | no, `AA` | `AA` |
| 3 | `W` | `AA` | no, `AAW` | `AAW` |
| 4 | `S` | `AAW` | **yes**: `AWS` | `A` |
| 5 | `W` | `A` | no, `AW` | `AW` |
| 6 | `S` | `AW` | **yes**: `AWS` | (empty) |

The stack ends empty, so the answer is the empty string, which this problem asks
you to report as `"-1"`.

This trace shows something the first did not. In step 6, the `AWS` that was deleted
is made of the `A` from input position 0 and the `W` and `S` from positions 4 and
5. In the original string those letters were not next to each other. The deletion
in step 4 brought them together. And the scan never went back to look: after step
4 the `A` from position 0 was simply on top, which is exactly where the next
comparison happens.

Tell step 4 in words. "I push `S`. The top three are `A`, `W`, `S`, from input
positions 1, 2 and 3. That is the pattern, so I delete all three. The stack is now
`A`, the one from position 0. It is on top. It does not know it was ever buried;
it is just the newest unresolved letter, waiting for the next one."

Compare with `str.replace`: one pass over `AAWSWS` finds the `AWS` at positions 1
to 3, removes it, and moves on past it, giving `AWS`. You would have to loop until
the string stops changing, which is the quadratic brute force again.

### A third trace: positions instead of characters

[[p:doordash-minimum-parenthesis-removal-indices|Minimum Parenthesis Removals and Their Indices]]
asks for the **indices** of the brackets that cannot be matched. Push indices, not
characters. Input `())(()`:

| i | char | stack of indices before | action | stack after | orphans |
|---|---|---|---|---|---|
| 0 | `(` | | push 0 | 0 | |
| 1 | `)` | 0 | pop: 1 closes 0 | | |
| 2 | `)` | (empty) | nothing to close: orphan | | 2 |
| 3 | `(` | | push 3 | 3 | 2 |
| 4 | `(` | 3 | push 4 | 3, 4 | 2 |
| 5 | `)` | 3, 4 | pop: 5 closes 4 | 3 | 2 |

At the end, index 3 is still open. The unmatched indices are the orphan closer 2
and the leftover opener 3: answer [2, 3]. Delete those two and `()()` remains,
which is valid. The stack of characters could have said "invalid", but not
**where**.

## From the idea to the code

First the brute force and the two wrong instincts, run against the stack on the
same strings, with the work counted. Then the clean implementation.

```python run
import random

PAIRS = ["()", "[]", "{}"]

def valid_by_deletion(s):
    """The definition, run literally: delete adjacent pairs until none are left."""
    work = 0
    while True:
        work += len(s)                         # one pass reads the whole string
        t = s
        for p in PAIRS:
            t = t.replace(p, "")
        if t == s:
            return s == "", work
        s = t

def valid_by_counter(s):                       # wrong instinct 1: only the depth
    depth = 0
    for c in s:
        depth += 1 if c in "([{" else -1
        if depth < 0:
            return False
    return depth == 0

def valid_by_same_kind(s):                     # wrong instinct 2: one counter per kind
    open_count = {"(": 0, "[": 0, "{": 0}
    match = {")": "(", "]": "[", "}": "{"}
    for c in s:
        if c in open_count:
            open_count[c] += 1
        else:
            if open_count[match[c]] == 0:
                return False
            open_count[match[c]] -= 1
    return all(v == 0 for v in open_count.values())

def valid_by_stack(s):
    match, stack, work = {")": "(", "]": "[", "}": "{"}, [], 0
    for c in s:
        work += 1
        if c in match:
            if not stack or stack.pop() != match[c]:
                return False, work
        else:
            stack.append(c)
    return not stack, work

for t in ["([{}])", "([)]", "(("]:
    print("%-8s deletion %-5s counter %-5s per-kind %-5s stack %s" % (t, valid_by_deletion(t)[0],
          valid_by_counter(t), valid_by_same_kind(t), valid_by_stack(t)[0]))
assert valid_by_counter("([)]") and valid_by_same_kind("([)]")       # both fooled
assert not valid_by_deletion("([)]")[0] and not valid_by_stack("([)]")[0]

for n in (1000, 2000, 4000):
    nested = "(" * (n // 2) + ")" * (n // 2)   # one deletion per pass: the worst case
    (a, w1), (b, w2) = valid_by_deletion(nested), valid_by_stack(nested)
    assert a and b
    print("n=%5d  deletion reads %9d chars, stack reads %5d" % (n, w1, w2))
    assert w1 > n * n / 8 and w2 == n

rng = random.Random(1)
for _ in range(3000):
    t = "".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 10)))
    assert valid_by_deletion(t)[0] == valid_by_stack(t)[0], t
print("3000 random strings: the one-pass stack agrees with repeated deletion")
```

Look at the first table: the counter and the per-kind counters both accept `([)]`.
The repeated deletion and the stack both reject it. Then the work: on nested
strings the deletion reads about n^2/4 characters, and the stack reads exactly n.

Here is the scan written properly, with the hand trace asserted, plus the two
other traces from the previous section.

```python run
import random

def is_valid(s, log=None):
    match = {")": "(", "]": "[", "}": "{"}    # closer -> the opener it needs
    stack = []                                 # openers not yet closed, oldest first
    for c in s:
        if c in match:                         # a closer: it can only meet the top
            if not stack or stack.pop() != match[c]:
                return False                   # nothing open, or the wrong kind open
        else:
            stack.append(c)                    # an opener: a new debt
        if log is not None:
            log.append("".join(stack))
    return not stack                           # debts never paid make it invalid

log = []
print("{[()()]}", is_valid("{[()()]}", log), log)
assert log == ["{", "{[", "{[(", "{[", "{[(", "{[", "{", ""]

def unmatched(s):
    """Indices left over when each ')' takes the most recent unmatched '('."""
    stack, orphans = [], []
    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)                    # push WHERE, not what
        elif c == ")":
            if stack:
                stack.pop()
            else:
                orphans.append(i)              # a closer with nothing to close
    return sorted(orphans + stack)             # plus openers never closed

print("unmatched in '())(()' :", unmatched("())(()"))
assert unmatched("())(()") == [2, 3]

def eliminate(s, pat="AWS"):
    stack, k = [], len(pat)
    for c in s:
        stack.append(c)
        if len(stack) >= k and "".join(stack[-k:]) == pat:
            del stack[-k:]                     # the cascade needs no look-back
    return "".join(stack)

def by_repeated_deletion(s, pat="AWS"):
    while pat in s:
        s = s.replace(pat, "", 1)
    return s

print("one replace pass on AAWSWS:", repr("AAWSWS".replace("AWS", "")),
      "  stack:", repr(eliminate("AAWSWS")))
assert eliminate("AAWSWS") == "" and "AAWSWS".replace("AWS", "") == "AWS"
rng = random.Random(5)
for _ in range(2000):
    t = "".join(rng.choice("AWS") for _ in range(rng.randint(0, 14)))
    assert eliminate(t) == by_repeated_deletion(t), t
print("2000 random strings: one pass equals deleting until nothing is left")
```

### Each line, and which part of the idea it is

| line | in words | which step of the derivation |
|---|---|---|
| `match = {")": "(", ...}` | for each closer, the opener it needs | the matching rule |
| `stack = []` | the reduced prefix: openers not yet closed, oldest first | step 3 |
| `if c in match:` | a closer arrived: it can only settle with the top | the unlocking question |
| `if not stack` | nothing is open: this closer has no partner (the curve dips below zero) | failure 1 |
| `or stack.pop() != match[c]` | pop the newest open bracket; if it is the wrong kind, the pairs cross | failure 1, wrong kind |
| `stack.append(c)` | an opener: a new debt, now the newest | push |
| `return not stack` | anything left was opened and never closed | failure 2 |
| `stack.append(i)` in `unmatched` | push where, not what | step 4: positions |
| `del stack[-k:]` in `eliminate` | the pattern is on top: remove it, and the seam is the new top | the cascade |

Settle three boring confusions now.

**Why is `not stack` tested before `stack.pop()`?** Because Python's `or` stops
at the first true operand. If the stack is empty, `not stack` is true, the
condition is decided, and `pop()` is never called. Written the other way round,
`stack.pop() != match[c] or not stack`, the pop runs first and crashes with
`IndexError` on the input `)`.

**Is popping inside the condition safe?** Here, yes, because a mismatch returns
immediately and the popped value is never needed again. If the loop had to
continue after a mismatch (say, to count errors), you would peek with `stack[-1]`
first and pop separately.

**Does `eliminate` re-check after a deletion?** It does not need to. Before the
push, the stack contained no `AWS` anywhere (that is the invariant). Deleting the
top three leaves a prefix of that clean stack, which is still clean. So at most one
deletion can happen per character, and the `if` is enough. For some rules, like
the asteroids in variation C, one arrival can resolve several items in a row, and
then you need a `while`.

### The subtle line, both ways

The one line that carries the bracket scan is `return not stack`. The common wrong
version is `return True`: "I got to the end without rejecting, so it is valid". It
looks reasonable, it passes every balanced test, and it is wrong. The block also
shows the guard order from above.

Same inputs for both: `(()` and `(())`.

Right ending (`return not stack`):

- `(()`: `(` push, stack `(`. `(` push, stack `((`. `)` pops a `(`, stack `(`. End.
  The stack holds `(`: one opener never closed. **Invalid.**
- `(())`: same three steps, then `)` pops the last `(`. Stack empty. **Valid.**

Wrong ending (`return True`):

- `(()`: exactly the same three steps, stack `(` at the end. **This is the point
  where it goes wrong**: the leftover `(` is on the stack, and nobody looks at it.
  Returns **valid**.
- `(())`: valid, correct.

So the wrong version is right on every string whose stack happens to end empty,
which includes every valid string. The only inputs that catch it are the ones with
an unclosed opener at the end. In the height picture, it checks "never below zero"
but not "finishes on zero". What it actually computes is "is this a **prefix** of
some valid string?", a real and different question: `(()` is a fine beginning of
`(())`.

```python run
MATCH = {")": "(", "]": "[", "}": "{"}

def scan(s, ending, guard_first=True):
    stack, steps = [], []
    for c in s:
        if c in MATCH:
            if guard_first:
                bad = not stack or stack.pop() != MATCH[c]      # empty is tested first
            else:
                bad = stack.pop() != MATCH[c] or not stack      # pops before it looks
            if bad:
                steps.append("%s: reject" % c)
                return False, steps
        else:
            stack.append(c)
        steps.append("%s: [%s]" % (c, "".join(stack)))
    return (not stack if ending == "right" else True), steps

for s in ["(()", "(())"]:
    for ending in ("right", "wrong"):
        ok, steps = scan(s, ending)
        print("%-5s %-6s ending -> %-5s   %s" % (s, ending, ok, "  ".join(steps)))
assert scan("(()", "right")[0] is False
assert scan("(()", "wrong")[0] is True          # the leftover '(' was never looked at
assert scan("(())", "right")[0] is scan("(())", "wrong")[0] is True   # balanced tests pass

crashed = False
try:
    scan(")", "right", guard_first=False)
except IndexError as e:
    crashed = True
    print("guard second on ')':  IndexError:", e)
assert crashed
print("guard first on ')':  ", scan(")", "right")[0])
assert scan(")", "right")[0] is False
```

Notice that the stacks printed for `(()` are identical in both versions, step by
step. The scan is the same; only the last line differs. That is why reading the
loop carefully does not find this bug. You find it by asking what the stack holds
at the end, and what that means.

## Why it is correct

The informal argument, "the stack holds the unmatched openers", is a restatement,
not a proof. Here is a real one. It needs a precise definition of valid.

**Definition.** Deleting an adjacent matched pair (`()`, `[]` or `{}` sitting side
by side) is a *reduction*. A string is **valid** if some sequence of reductions
turns it into the empty string.

This matches "closed by the same kind, in reverse order". A non-empty valid string
always has an innermost pair, an opener immediately followed by its own closer, and
deleting it leaves a valid string. Conversely, inserting a matched pair side by
side into a valid string keeps it valid. So the two definitions describe the same
strings.

:::proof The scan accepts exactly the valid strings
**Fact 1: the end result of reducing does not depend on the order.** Two different
adjacent pairs in a string never share a character: a pair is an opener followed
by a closer, so for two pairs to overlap one character would have to be the closer
of the first pair and the opener of the second. So deleting one pair leaves the
other intact, and the two deletions can be done in either order with the same
result. Every reduction makes the string shorter, so reducing always stops. A
string that can be reduced in two different ways can therefore always be brought
back to a common result, and every string has exactly one fully reduced form.
Call it NF(s). Then s is valid exactly when NF(s) is empty.

**The invariant.** After the scan has read a prefix P without rejecting, the stack,
read bottom to top, is NF(P), and it contains only openers.

**Base case.** P is empty, the stack is empty, and NF of the empty string is empty.

**Step, opener.** The next character c is an opener. NF(P) followed by c is
openers only, so no pair can be deleted: it is fully reduced. That is NF(P + c),
and the scan pushes c. The invariant holds.

**Step, matching closer.** c is a closer and the top of the stack is its opener.
NF(P) + c ends with an adjacent matched pair. Delete it: what is left is NF(P)
without its top, a string of openers only, which is fully reduced. So it is
NF(P + c), and the scan pops. The invariant holds.

**Step, reject.** c is a closer and the stack is empty, or its top is an opener of
the wrong kind. Then NF(P) + c is fully reduced (openers only, then a closer that
does not match its left neighbour), so it is NF(P + c), and it contains the closer
c. We show that no continuation can ever remove c, so the scan is right to stop.
In any further reduction, c can only be deleted together with the character
directly to its left at that moment. If there is no character to its left, it can
never be deleted. If there is one, it is the opener x that does not match c. And x,
being an opener, can only be deleted together with the character directly to its
**right**, which is c, which does not match. Neither can go first, so neither ever
goes. Every extension of P + c has a non-empty reduced form, so it is invalid, and
in particular s is invalid.

**End.** If the scan reads all of s without rejecting, the stack is NF(s). It is
empty exactly when s is valid, which is what `return not stack` reports.

**Termination and count.** Each character is pushed at most once and popped at
most once, so the scan does at most 2n stack operations.
:::

The same proof covers more than brackets. Any rule of the form "delete this
pattern when it appears, until it no longer appears" works with the one-pass stack,
provided two occurrences of the pattern can never overlap. `AWS` cannot overlap
itself (no ending of `AWS` is also a beginning of it), and neither can `xy` for
two different characters. The pattern `aba` can overlap itself: in `ababa` the
occurrences at positions 0 to 2 and 2 to 4 share the middle `a`. Deleting the
first leaves `ba`, deleting the second leaves `ab`. Two different end results, so
"delete until none remain" does not even define a single answer, and Fact 1 is
exactly the step that fails.

Now say plainly what the proof leaned on, because that list is where bugs come
from.

- **Only the top can interact.** The proof used that a new character can only form
  a pair with its left neighbour in the reduced string. If a rule can fire in the
  middle of what you have kept (not at the seam), the stack is the wrong
  structure.
- **Patterns do not overlap.** That is Fact 1. Check it before trusting a one-pass
  cancellation.
- **The two failure checks.** The reject step and the end step are separate parts
  of the proof. Each one corresponds to a line of code, and dropping either one
  breaks a different set of inputs.
- **The stack is the whole state.** Nothing is remembered outside it. If you add a
  side variable (a running sum, a depth, a minimum), you have a second invariant,
  and every push and every pop must keep it true. That is where min stacks and
  calculators go wrong.
- **Nothing was said about speed.** If the answer is wrong, `pop(0)` and string
  concatenation are not the suspects. If it is slow, they are.

## What it costs

**Time.** Each character is pushed at most once. Each pop removes something that
was pushed earlier and is never pushed again. So over the whole run

```text
pops <= pushes <= n,   so stack operations <= 2n.
```

That is a counting argument over the whole run, which is why it holds even when a
single character causes many pops (an asteroid that destroys ten others in a
`while` loop). The ten pops are paid for by the ten earlier pushes. The scan is
O(n), and with a pattern of length k checked at every step, O(nk), which is O(n)
for the short patterns these problems use.

**Space.** O(n) in the worst case, and it really happens: on `((((...` nothing
cancels and the stack holds the whole input. If a problem demands O(1) extra
space, look for a counter (one bracket kind) or a two-pointer scan from the right
([[p:compare-strings|Backspace String Compare]] can be solved by walking both
strings backwards, counting pending backspaces in an integer).

**The list underneath.** `list.append` is O(1) **amortised**: the list
occasionally doubles its capacity and copies everything, but n appends copy fewer
than 2n elements in total (1 + 2 + 4 + ... + n < 2n), so the average stays
constant. See [[amortized-analysis]]. `list.pop()` from the end is O(1).

**The costs people forget.**

- **`pop(0)` or `insert(0, x)`.** Each is O(n), because every other element shifts.
  A stack grows and shrinks at the end. If you need both ends, use a [[deque]].
- **Building the answer with `out += c` inside the loop.** For strings this can
  copy the whole string each time, O(n^2) in the worst case. Keep a list and
  `"".join(stack)` once at the end.
- **`"".join(stack[-k:])` at every step** is O(k) per character. Fine for `AWS`.
  For a long pattern, compare characters one at a time from the top, or keep a
  matching state (as in [[string-matching]]).
- **Recursion you replaced.** Python's default recursion limit is about 1000
  frames. A tree or a nesting depth of 10^5 needs the explicit stack, which is why
  [[p:uber-find-file-paths-in-directory-tree|Find File Paths in a Directory Tree]]
  asks for one in the statement.
- **Repeated strings in an expression evaluator.** In Decode String, `cur * times`
  builds a new string of the decoded length. The total work is the size of the
  output, which the problem bounds (10^5 there).

## How to think about it

Before writing any code, answer these, in order.

1. **After reading a prefix, what is still unresolved?** Open brackets, letters
   that might still be cancelled, asteroids that might still be hit, numbers
   waiting for an operator, an outer context waiting for its `]`. Say it in words.
2. **Does the next item interact only with the most recent unresolved one?** If
   yes, it is a stack. If it interacts with the oldest, it is a queue. If with the
   smallest or largest, a heap. If with "the nearest one bigger than it", a
   monotonic stack.
3. **What exactly do I push?** The item, its index, a context tuple, a
   (value, count) pair, or a (value, running summary) pair. Decide by what the
   answer needs: positions need indices, a restore needs a context.
4. **What does a pop mean, in one sentence?** "This debt is paid", "this asteroid
   died", "this group is closed: glue it onto the outer text".
5. **Can one arrival resolve several items?** Then the comparison is a `while`,
   not an `if`. Asteroids: yes. Brackets: no. Removing `k` equal neighbours: one
   pop per run, but the run below may grow.
6. **What is left at the end, and what does it mean?** Unclosed brackets (invalid),
   survivors (the answer), the final value (the result). Never forget to look.
7. **Is it a yes/no over one kind of item?** Then the stack is only a height, and a
   counter does it in O(1) space.

### Telling it from its neighbours

- **Counter.** A stack whose elements are all identical. Use it when there is one
  kind; never when there are several.
- **Queue.** The other end. "First in, first out." If the next item to handle is
  the oldest, it is a queue.
- **Monotonic stack.** A stack with a rule about what may stay: before pushing,
  pop everything that the new item beats. It answers "the next greater element" for
  every position in O(n). Same data structure, different invariant
  ([[monotonic-stack]]).
- **Recursion.** Every recursive function uses the call stack. A nested structure
  (brackets, `k[...]`, parenthesised arithmetic) can be handled by a recursive
  function that calls itself at each opener and returns at each closer, or by an
  explicit stack that pushes at the opener and pops at the closer. They are the
  same algorithm. [[recursive-descent]] is the recursive form for real grammars.
- **Deque.** If you need to add or remove at both ends ([[deque]]).

## Variations

These are all the stack shapes that interviews and OAs ask, each with what changes,
why, a short example, and a problem from the bank.

### A. Match pairs (parentheses)

**What changes.** What you push (characters or indices) and what you do with
the leftovers.

**Why.** A closer can only close the most recent unresolved opener. The leftovers
at the end, plus the closers that found nothing, are exactly the unmatched
brackets.

**Example.** `(a)b)` with letters ignored: `(` push 0, `)` pops it, `)` at index 4
finds nothing: orphan. Remove index 4: `(a)b`.

**In the bank.**

- [[p:amazon-valid-parentheses|Valid Parentheses]]: the yes/no version, three
  kinds, so a real stack.
- [[p:meta-minimum-removal-for-balanced-parentheses|Minimum Removal for Balanced Parentheses]]:
  push indices; drop the orphan closers during the scan and the leftover openers at
  the end. Letters and digits are kept and skipped by the stack.
- [[p:doordash-minimum-parenthesis-removal-indices|Minimum Parenthesis Removals and Their Indices]]:
  the third trace above.
- [[p:headlands-exclusive-function-execution-times|Exclusive Function Execution Times]]:
  `start` and `end` logs are matched pairs on a call stack. The function on top owns
  the time between consecutive events. When a new function starts, charge the time
  so far to the old top; when one ends, charge it (the end second is inclusive)
  and pop.
- [[p:mathworks-longest-valid-parentheses|Longest Valid Parentheses]] (stretch):
  push indices, and keep at the bottom the index of the last unmatched `)` as a
  floor. After each pop, the current valid run is `i - stack[-1]`.
- [[p:oracle-balance-parentheses|Balancing Parentheses]]: one kind, so two
  counters: closers that found nothing, plus openers left at the end.

### B. Evaluate an expression (RPN, a calculator, nested groups)

**What changes.** The stack holds values, or saved contexts, instead of brackets.

**Reverse Polish notation.** Numbers are pushed. An operator pops its two operands
and pushes the result. The first value popped is the **right** operand.
`["4", "13", "5", "/", "+"]`: push 4, 13, 5; `/` pops 5 then 13, pushes
13 / 5 = 2; `+` pops 2 then 4, pushes 6. Answer 6.
[[p:atlassian-evaluate-reverse-polish-notation|Evaluate Reverse Polish Notation]];
[[p:retell-ai-stack-language-evaluator|Stack Language Evaluator]] adds `dup`,
`swap` and `drop`. Division "truncates toward zero" means `int(a / b)`, not
`a // b`: in Python, `-7 // 2` is -4, but the problem wants -3.

**Nested groups: push the outer context.** At an opener, the current work is
interrupted, so save it and start fresh. At the closer, the inner work is done, so
restore the outer work and combine. Decode String, `3[a2[c]]`:

| char | action | stack | cur | k |
|---|---|---|---|---|
| `3` | digit | | | 3 |
| `[` | push (cur, k) = ("", 3), reset | ("", 3) | | 0 |
| `a` | letter | ("", 3) | a | 0 |
| `2` | digit | ("", 3) | a | 2 |
| `[` | push ("a", 2), reset | ("", 3), ("a", 2) | | 0 |
| `c` | letter | same | c | 0 |
| `]` | pop ("a", 2): cur = "a" + "c" x 2 | ("", 3) | acc | |
| `]` | pop ("", 3): cur = "" + "acc" x 3 | | accaccacc | |

[[p:abridge-decode-string|Decode String]] is exactly this.

**Parentheses with + and -.** Same idea, with numbers. Keep a running `result`
and the `sign` of the next number. At `(`, push (result, sign) and start a fresh
result. At `)`, finish the inner result, pop (outer, outer_sign), and set
result = outer + outer_sign * inner. `1-(2-(3-4))`: at the inner `)`, the inner
result is 3 - 4 = -1, and the popped context is (2, -1), so 2 + (-1)(-1) = 3; at
the outer `)`, the popped context is (1, -1), so 1 - 3 = -2.
[[p:amazon-basic-calculator|Basic Calculator]] (stretch). With `*` and `/` and
precedence, you either use two stacks (values and operators) or write a
[[recursive-descent]] parser; see [[parsing]].

### C. Simulate with undo or collapse (asteroids, removing pairs)

**What changes.** An arrival may destroy several items on the stack in a row, so
the comparison is a `while` loop. Or the "stack" is a history that you move items
off and back on.

**Asteroid collision.** Survivors so far wait on the stack. Only a right-mover
followed by a left-mover can meet. A new left-mover fights the top while the top is
a right-mover: if the top is smaller, it dies (pop) and the fight continues with
the next one; if equal, both die; if bigger, the newcomer dies.
`[10, 2, -5]`: push 10, push 2; `-5` beats 2 (pop), then meets 10 and dies. Answer
`[10]`. [[p:microsoft-asteroid-collision|Asteroid Collision]];
[[p:mathwork-cars-left|Collision]] is the same with cars, directions, strengths,
and the answer as indices (so push indices).

**Cancellation rules.** [[p:wellsfargo-minimum-remaining-length|Minimum Remaining Length]]
deletes `AB` or `BB`: in both, a `B` cancels whatever is right before it. So a `B`
pops if the stack is non-empty, and everything else is pushed. Only the size
matters, so the stack can even be a counter. [[p:google-repeated-adjacent-pair-deletion|Repeated Adjacent Pair Deletion]]:
pop when the top equals the new character. [[p:compare-strings|Backspace String Compare]]:
`#` pops if it can. [[p:ibm-get-final-string|Get Final String]] and
[[p:jpmorgan-get-final-string|Eliminate Substring]]: a fixed pattern on top.

**Undo and redo.** [[p:netflix-undo-redo-command-history|Undo and Redo Command History]]
keeps two stacks: the active history and the undone commands. UNDO moves the top of
history to the redo stack; REDO moves it back; a new EXECUTE clears the redo
stack, because the undone future no longer follows from the present.
[[p:netflix-command-undo-data-structure|Command Undo Data Structure]] multiplies and
adds an integer, so store the previous state on the stack rather than trying to
invert a multiplication (by zero, say).

### D. A stack augmented with extra data (min stack)

**What changes.** Each entry carries, next to its value, a summary of itself and
everything below it.

**Why it works.** Entries only leave from the top. So the summary stored with an
entry stays correct for exactly as long as that entry is in the stack: nothing
below it can change while it is there. When it is popped, the entry below it
becomes the top, and its own summary is already correct.

**Example.** Push 5, 3, 7, 3, 1: entries (5,5), (3,3), (7,3), (3,3), (1,1). The
minimum is 1. Pop: top (3,3), minimum 3. Pop: (7,3), minimum 3. Pop: (3,3), 3.
Pop: (5,5), 5. Duplicates of the minimum are kept as separate entries, which is
why the second 3 matters.

**In the bank.** [[p:shopify-min-stack|Min Stack]] and
[[p:linkedin-minimum-stack-operations|Constant-Time Minimum Stack]].
[[p:drw-nested-database-transactions|Nested In-Memory Database Transactions]] is a
stack of dictionaries: BEGIN pushes an empty layer, SET writes into the top layer,
GET searches from the top down, ROLLBACK pops one layer, COMMIT applies them
oldest to newest. [[p:imc-adding-stack-2-0|Adding Stack 2.0]] has "add v to the
bottom i elements" in O(1): store a lazy increment at depth i, keep a running sum,
and when an entry is popped, pass its pending increment down to the entry below
it. It is the hardest member of this family, and it is the same principle: the
extra data is kept where the pops will find it.

### E. A stack of (value, count)

**What changes.** Instead of one entry per character, one entry per run of equal
characters: `[character, run length]`.

**Why.** "Remove k equal neighbours, repeatedly" with one entry per character
would need to look k deep at every step and recount after every removal. With
runs, the top entry already knows how long the current run is. When it reaches k,
pop it, and the run below becomes the top, ready to be extended by the next
character.

**Example.** `deeedbbcccbdaa`, k = 3:

| char | stack after |
|---|---|
| d | d1 |
| e | d1 e1 |
| e | d1 e2 |
| e | e3 removed: d1 |
| d | d2 |
| b | d2 b1 |
| b | d2 b2 |
| c | d2 b2 c1 |
| c | d2 b2 c2 |
| c | c3 removed: d2 b2 |
| b | b3 removed: d2 |
| d | d3 removed: (empty) |
| a | a1 |
| a | a2 |

Answer `aa`. Notice the cascade: removing `ccc` let the `b` runs on either side
join, and removing `bbb` let the `d` runs join.
[[p:attentive-remove-adjacent-duplicates-ii|Remove Adjacent Duplicates in String II]].

### F. A queue from two stacks (common in interviews, simple)

An inbox stack takes arrivals. An outbox stack serves departures. When the outbox
is empty and someone wants the front, pour the whole inbox into the outbox, which
reverses it, so the oldest is on top. Each element is moved at most once, so the
total cost is O(1) amortised per operation, though a single operation can cost
O(n). [[p:amazon-queue-using-two-stacks|Implement a Queue Using Two Stacks]].

### G. An explicit stack instead of recursion

Push the work you have not done yet; pop, do one piece, push its successors. For a
preorder traversal of a binary tree, pop a node, visit it, push its **right** child
and then its left child, so the left is popped first. The order you want to visit
is the reverse of the order you push.
[[p:uber-find-file-paths-in-directory-tree|Find File Paths in a Directory Tree]]
requires an explicit stack in the statement;
[[p:anduril-binary-tree-preorder-traversal|Binary Tree Preorder Traversal]] is the
smallest place to practise it. See [[tree-traversal]] and [[dfs]].

### H. Monotonic stack (own chapter)

Before pushing, pop everything the new item beats. Each item enters and leaves
once, so the scan is O(n), and each pop tells the popped item "this is your next
greater element". Daily temperatures, stock spans, the largest rectangle in a
histogram. This is common enough that it has its own chapter:
[[monotonic-stack]].

The block below runs variations B, C, D and E on the examples above.

```python run
def rpn(tokens):
    st = []
    for t in tokens:
        if t in "+-*/" and len(t) == 1:
            b = st.pop()                       # popped FIRST: the RIGHT operand
            a = st.pop()
            if t == "+": st.append(a + b)
            elif t == "-": st.append(a - b)
            elif t == "*": st.append(a * b)
            else: st.append(int(a / b))        # truncate toward zero, as the problem says
        else:
            st.append(int(t))
    return st[-1]

def decode(s):
    st, cur, k = [], "", 0                     # cur: text of the group we are inside
    for c in s:
        if c.isdigit():
            k = k * 10 + int(c)                # counts can have several digits
        elif c == "[":
            st.append((cur, k))                # save the OUTER context, start fresh
            cur, k = "", 0
        elif c == "]":
            outer, times = st.pop()            # restore it, glue the repeated group on
            cur = outer + cur * times
        else:
            cur += c
    return cur

def calculate(s):                              # + - and parentheses (Basic Calculator)
    st, result, sign, num = [], 0, 1, 0
    for c in s + "+":                          # a sentinel '+' flushes the last number
        if c.isdigit():
            num = num * 10 + int(c)
        elif c in "+-":
            result += sign * num
            num, sign = 0, (1 if c == "+" else -1)
        elif c == "(":
            st.append((result, sign))          # save what was outside, start fresh
            result, sign = 0, 1
        elif c == ")":
            result += sign * num
            num = 0
            outer, outer_sign = st.pop()
            result, sign = outer + outer_sign * result, 1
    return result

print("rpn 2 1 + 3 *        =", rpn(["2", "1", "+", "3", "*"]))
print("rpn 4 13 5 / +       =", rpn(["4", "13", "5", "/", "+"]))
print("rpn 6 -132 /         =", rpn(["6", "-132", "/"]))
assert rpn(["2", "1", "+", "3", "*"]) == 9 and rpn(["4", "13", "5", "/", "+"]) == 6
assert rpn(["6", "-132", "/"]) == 0            # -0.04 truncates to 0, not -1
print("decode 3[a2[c]]      =", decode("3[a2[c]]"))
assert decode("3[a2[c]]") == "accaccacc" and decode("2[ab]10[x]") == "abab" + "x" * 10
print("calc (1+(4+5+2)-3)+(6+8) =", calculate("(1+(4+5+2)-3)+(6+8)"))
assert calculate("(1+(4+5+2)-3)+(6+8)") == 23 and calculate("1-(2-(3-4))") == -2
for e in ["1-(2-(3-4))", "10-(3+4)-(1-(2))", "7", "(((5)))-5"]:
    assert calculate(e) == eval(e), e
print("calculator agrees with eval on nested minus signs")
```

```python run
def asteroids(row):
    st = []                                    # survivors so far, left to right
    for a in row:
        alive = True
        while alive and a < 0 and st and st[-1] > 0:   # only right-mover then left-mover meet
            if st[-1] < -a:
                st.pop()                       # the top dies; a keeps going: loop again
            elif st[-1] == -a:
                st.pop()
                alive = False                  # both die
            else:
                alive = False                  # a dies
        if alive:
            st.append(a)
    return st

def remove_k_dupes(s, k):
    st = []                                    # (character, length of its run)
    for c in s:
        if st and st[-1][0] == c:
            st[-1][1] += 1
            if st[-1][1] == k:
                st.pop()                       # the run vanishes; its neighbours meet
        else:
            st.append([c, 1])
    return "".join(c * n for c, n in st)

class MinStack:
    def __init__(self):
        self.st = []                           # (value, minimum of this entry and below)
    def push(self, x):
        self.st.append((x, min(x, self.st[-1][1]) if self.st else x))
    def pop(self):
        self.st.pop()
    def top(self):
        return self.st[-1][0]
    def get_min(self):
        return self.st[-1][1]

print("asteroids [5, 10, -5]   ->", asteroids([5, 10, -5]))
print("asteroids [10, 2, -5]   ->", asteroids([10, 2, -5]))
print("asteroids [8, -8]       ->", asteroids([8, -8]))
print("asteroids [-2, -1, 1, 2] ->", asteroids([-2, -1, 1, 2]))
assert asteroids([5, 10, -5]) == [5, 10] and asteroids([10, 2, -5]) == [10]
assert asteroids([8, -8]) == [] and asteroids([-2, -1, 1, 2]) == [-2, -1, 1, 2]
assert asteroids([1, 2, 3, -10]) == [-10]      # one left-mover eats three in a while loop

print("deeedbbcccbdaa, k=3     ->", remove_k_dupes("deeedbbcccbdaa", 3))
assert remove_k_dupes("deeedbbcccbdaa", 3) == "aa"

m, seen = MinStack(), []
for x in [5, 3, 7, 3, 1]:
    m.push(x)
    seen.append(m.get_min())
for _ in range(4):
    m.pop()
    seen.append(m.get_min())
print("min after pushes 5 3 7 3 1, then 4 pops:", seen)
assert seen == [5, 3, 3, 3, 1, 3, 3, 3, 5]
```

## Recognising it in a statement

Ordered by how much you should trust the signal.

1. **Explicit nesting.** Brackets, tags, `k[...]`, nested maps, directory trees, a
   group that "can itself contain more groups". Nesting is a stack.
2. **"The most recent", "the last unmatched", "the previous".** When the statement
   says "match each closing parenthesis with the most recent unmatched opening
   parenthesis", it has described a stack.
3. **Undo, revert, rollback, "go back".** The history of what you did is a stack by
   definition.
4. **Cancellation between neighbours, "until no more remain".** Backspaces,
   removing a substring, adjacent duplicates, colliding asteroids. The words *until
   no more remain* are the tell, and the stack turns that repetition into one pass.
5. **An expression, or a tiny instruction set with push and pop.** Postfix, a
   calculator with parentheses, a stack machine.
6. **"Use an explicit stack rather than recursion",** or a depth of 10^5 that would
   blow the recursion limit.
7. **Each element looks for the next bigger or smaller one.** Monotonic stack.

### Disguises

- **Logs with start and end events.** Function calls, transactions, spans. They nest,
  so they are brackets with names.
- **"Each X destroys the Y right before it."** `AB`/`BB` deletion is "every B
  cancels its left neighbour".
- **A string with counts and groups.** `3[a2[c]]`, chemical formulas like
  `Mg(OH)2`: each `(` or `[` saves a context.
- **A path to normalise.** `/a/./b/../../c` is a stack of directory names: `..`
  pops, `.` does nothing, a name pushes.

### Anti-signals: looks like a stack, is not

- **Arrival order.** "First come, first served", "in the order received", level
  order in a tree. [[queue]].
- **The smallest or largest after arbitrary removals.** [[heap]] or [[ordered-set]].
- **One bracket kind and a yes/no or a count.** A counter, O(1) space.
- **Crossing intervals.** "Do any two meetings overlap?" is about crossings, not
  nesting. [[intervals]].
- **"Remove the element in the middle."** A stack only touches one end.

## Traps

**Peeking or popping an empty stack.** Symptom: `IndexError` on the first input that
starts with a closer, or the first asteroid that moves left. The guard is always
`if stack and ...` before `stack[-1]`, written as one motion.

**Forgetting the final emptiness check.** Symptom: `((` is reported valid while
every balanced test passes. Demonstrated above.

**A counter where there are several kinds.** Symptom: `([)]` is accepted.
Demonstrated in the first block.

**Popping the operands in the wrong order.** In RPN, the first value popped is the
**right** operand. `10 4 -` means 10 - 4 = 6; pop them the wrong way round and you
compute 4 - 10 = -6. Symptom: subtraction and division are wrong, addition and
multiplication are right, so a test with only `+` and `*` passes.

**`//` where the problem says "truncate toward zero".** Python's `//` rounds toward
minus infinity. Symptom: wrong answers only when exactly one operand is negative.

**Pushing children in the wrong order in an explicit DFS.** Symptom: the traversal
comes out mirrored. A stack reverses what you put in, so push right before left.

**Storing values when the answer wants positions.** Symptom: you know the string is
invalid but cannot say which brackets to delete. Push `i`, not `s[i]`, whenever the
output is about where.

**`if` where a `while` is needed.** Asteroid `-10` against `[1, 2, 3]` must destroy
all three. An `if` destroys only the 3. Symptom: survivors that should be dead.

**Building the output with `+=` or using `pop(0)`.** Symptom: correct answers,
quadratic time, timeout at 10^5.

The block below demonstrates the operand order and the push order.

```python run
def rpn(tokens, right_first=True, show=True):
    st = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            if right_first:
                b = st.pop()
                a = st.pop()                   # a was pushed earlier: the LEFT operand
            else:
                a = st.pop()                   # wrong: treats the top as the left one
                b = st.pop()
            st.append({"+": a + b, "-": a - b, "*": a * b, "/": int(a / b) if b else 0}[t])
        else:
            st.append(int(t))
        if show:
            print("   %-3s -> %s" % (t, st))
    return st[-1]

print("tokens 10 4 -  (means 10 - 4), right operand popped first:")
good = rpn(["10", "4", "-"])
print("same tokens, left operand popped first:")
bad = rpn(["10", "4", "-"], right_first=False)
assert good == 6 and bad == -6
x, y = rpn(["2", "3", "*"], True, False), rpn(["2", "3", "*"], False, False)
print("2 3 * both ways:", x, y, "- a test made only of + and * cannot catch the bug")
assert x == y == 6

tree = {"A": ("B", "C"), "B": ("D", None), "C": (None, None), "D": (None, None)}

def preorder(root, right_pushed_first):
    st, out = [root], []
    while st:
        node = st.pop()
        out.append(node)
        left, right = tree[node]
        first, second = (right, left) if right_pushed_first else (left, right)
        for child in (first, second):
            if child:
                st.append(child)
    return out

print("preorder, push right then left:", preorder("A", True))
print("preorder, push left then right:", preorder("A", False))
assert preorder("A", True) == ["A", "B", "D", "C"]
assert preorder("A", False) == ["A", "C", "B", "D"]       # mirrored
```

## What to memorise

One loop, one sentence, one habit.

```text
stack = []
for x in items:
    while stack and resolves(stack[-1], x):    # 'if' when one arrival settles at most one
        stack.pop()                            # that debt is paid
    if x still needs to wait:
        stack.append(x)                        # a new debt, now the newest
# at the end, the stack is exactly what never got resolved; always look at it
```

**The sentence** that turns a problem into a stack: *"Is the next thing I must
settle always the most recent thing I have not settled?"* If yes, the only design
question left is what to push: the item, its index, a context, a (value, count), or
a (value, summary).

**The habit.** Before writing the loop, say in one sentence what the stack
contains, as a claim: "the opening brackets that are still unclosed, oldest at the
bottom". Every bug in this topic is that sentence being false at some moment: a
missing guard, a missing final check, an index pushed where a value was needed, a
context not restored. And write `if stack and` before every `stack[-1]`.

Numbers: at most 2n stack operations for n items, because pops cannot outnumber
pushes. `append` and `pop()` are O(1); `pop(0)` is O(n). Python's recursion limit
is about 1000, so nesting of 10^5 needs the explicit stack.

## Check yourself

:::check
Hand trace. Run the bracket scan on `{[]()}(` and on `[(])`, writing the stack after
every character. Which check rejects each string, the one during the scan or the
one at the end?
--
`{[]()}(`:

| char | action | stack |
|---|---|---|
| `{` | push | `{` |
| `[` | push | `{[` |
| `]` | top `[` matches: pop | `{` |
| `(` | push | `{(` |
| `)` | top `(` matches: pop | `{` |
| `}` | top `{` matches: pop | (empty) |
| `(` | push | `(` |

No rejection during the scan. At the end the stack holds `(`, so the **end check**
rejects it. A version with `return True` would accept it.

`[(])`:

| char | action | stack |
|---|---|---|
| `[` | push | `[` |
| `(` | push | `[(` |
| `]` | top is `(`, needs `[`: reject | |

Rejected **during the scan**, at the third character. A per-kind counter would
accept it, because each closer has an earlier opener of its own kind.
:::

:::check
Hand trace. Remove every `AWS` until none remain from `AWAWSSG`, using the stack
scan. Write the stack after every character. Then say what one `str.replace("AWS",
"")` pass gives and why it differs.
--
| char | stack before | top three `AWS`? | stack after |
|---|---|---|---|
| A | | no | A |
| W | A | no | AW |
| A | AW | no | AWA |
| W | AWA | no | AWAW |
| S | AWAW | **yes** (positions 2, 3, 4) | AW |
| S | AW | **yes** (positions 0, 1, 5) | (empty) |
| G | | no | G |

Answer `G`. One `str.replace` pass finds only the `AWS` at positions 2 to 4 and
gives `AWSG`, because the second `AWS` is made of the `A` and `W` at positions 0
and 1 and the `S` at position 5, which only become adjacent after the first
deletion. The stack sees it because, after the deletion, `AW` is simply on top.
:::

:::check
Hand trace. Asteroids `[3, 5, -6, 2, -1, 4]` (positive moves right, negative moves
left, the smaller one is destroyed, equal sizes both die). Write the stack after
each asteroid, and say how many pops the `-6` causes and why the total work is
still O(n).
--
| asteroid | what happens | stack |
|---|---|---|
| 3 | push | 3 |
| 5 | push | 3, 5 |
| -6 | meets 5: 5 < 6, pop. Meets 3: 3 < 6, pop. Stack empty: push | -6 |
| 2 | moving right, cannot meet a left-mover on its left: push | -6, 2 |
| -1 | meets 2: 2 > 1, the -1 dies | -6, 2 |
| 4 | push | -6, 2, 4 |

Answer `[-6, 2, 4]`. The `-6` causes two pops, in a `while` loop. The total is
still O(n) because every pop removes an asteroid that was pushed once, earlier, and
will never be pushed again: over the whole run there are at most n pops. The `-6`
"spent" the pushes of 3 and 5.
:::

:::check
Hand trace. Evaluate the RPN expression `["5", "1", "2", "+", "4", "*", "+", "3",
"-"]`, writing the stack after every token, and decode `2[a3[b]]c` with the
context stack.
--
| token | stack |
|---|---|
| 5 | 5 |
| 1 | 5, 1 |
| 2 | 5, 1, 2 |
| + | pop 2 (right), pop 1 (left): 5, 3 |
| 4 | 5, 3, 4 |
| * | pop 4, pop 3: 5, 12 |
| + | pop 12, pop 5: 17 |
| 3 | 17, 3 |
| - | pop 3 (right), pop 17 (left): 17 - 3 = 14 |

Answer 14. Popping in the wrong order would give 3 - 17 = -14 at the last step.

`2[a3[b]]c`: `2` sets k = 2. `[` pushes ("", 2). `a` makes cur = "a". `3` sets
k = 3. `[` pushes ("a", 3), cur = "". `b` makes cur = "b". `]` pops ("a", 3):
cur = "a" + "bbb" = "abbb". `]` pops ("", 2): cur = "" + "abbbabbb". `c` appends:
**"abbbabbbc"**.
:::

:::check
Why does the min stack store the minimum next to **every** entry, instead of
keeping one variable `current_min`? Give a sequence of operations that breaks the
one-variable version.
--
Because after a pop, the one variable has no way to know the new minimum. Push 3,
push 1: current_min = 1. Pop: the 1 is gone, so the minimum should be 3, but the
variable still says 1, and recomputing it means scanning the whole stack, O(n).

Storing (value, minimum of this entry and everything below) works because entries
leave only from the top. While an entry is in the stack, nothing below it can
change, so its stored minimum stays true. When the top is popped, the entry below
it becomes the top, and its stored minimum is already the right answer. Each
operation is O(1).
:::

:::check
Someone says: "Valid Parentheses does not need a stack: keep three counters, one
per bracket kind, and check that none goes negative and all end at zero." Where are
they wrong, and when is a counter genuinely enough?
--
They are wrong because the rule is not "each closer has some earlier opener of its
kind" but "each closer matches the most recent unresolved opener of any kind". On
`([)]` the three counters never go negative and all end at zero, so they accept it.
But the `)` arrives while `[` is the most recent open bracket, and the pairs cross.
The counters forget the order between different kinds, and the order is the whole
point.

A counter is genuinely enough when there is exactly one kind of bracket. Then every
stack element is the same symbol, so the stack's contents are determined by its
height, and the height is the counter. [[p:oracle-balance-parentheses|Balancing Parentheses]]
is that case: the answer is (closers that found nothing) + (openers left at the
end).
:::

:::check
Disguised problem. A string of `A` and `B`; you may repeatedly delete any `AB` or
`BB`. Return the shortest possible length. Reduce it to a stack scan, explain why
one pass is enough, and trace `BABBA`.
--
In both patterns, the second letter is `B`, and the first letter can be anything.
So the rule is really "a `B` may cancel whatever letter is directly before it".
Scan left to right: if the letter is `B` and the stack is non-empty, pop (cancel the
letter before it); otherwise push. The answer is the stack's size at the end. Since
only the size matters, an integer works as the stack.

One pass is enough by the same argument as the proof: after each step the stack has
no `AB` or `BB` in it (there is no `B` above anything at all, except possibly a `B`
at the very bottom), so a new deletion can only happen at the top, with the letter
that just arrived.

`BABBA`: `B` with an empty stack: push, [B]. `A`: push, [B, A]. `B`: pop the `A`
(that was an `AB`), [B]. `B`: pop the `B` (a `BB`), []. `A`: push, [A]. Length
**1**. This is [[p:wellsfargo-minimum-remaining-length|Minimum Remaining Length]].
:::
