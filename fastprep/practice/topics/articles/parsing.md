# Parsing and Tokenising

> Parsing is what you do when a string has a shape, and the discipline is to
> never let characters and meaning live in the same loop: one layer turns
> characters into tokens, a second turns tokens into structure, and neither ever
> looks back.

## When you reach for it

You reach for parsing when the input arrives as text and the *arrangement* of
the text carries information. Not "how many vowels are in this word" — that is a
scan, and it belongs to [[strings]]. Parsing is for input where some characters
are punctuation: they do not stand for themselves, they say how the other
characters are grouped.

143 problems in this bank involve it, which puts it at #27 of 150. It is the
most common non-algorithmic skill on the list, because every company's interview
eventually reaches for its own file format. They come in two families, and the
first question you should ask is which one you are holding.

**Flat records.** A line, a delimiter, some fields. *Message Latencies from CSV
Logs*, *Parse Query String*, *Parse Command-Line Tokens*, *Validate IP Address*,
*Compare Version Numbers*. The structure is one level deep. You need a scanner
and nothing else.

**Nested structures.** Something can contain something of its own kind. *Lisp
Expression Parser*, *Basic Calculator*, *Number of Atoms*, *Parse Indented YAML
Mappings*, *Rich Text Parser Part 2 (Parse Nested Groups)*. The structure has
unbounded depth, so a fixed number of loops cannot describe it. You need a stack,
explicit or in the shape of the call stack.

Here is the test that separates them, and it is the most useful single question
in this chapter. **Write down the legal inputs as a handful of rules. Does any
rule mention itself?** For *Validate IP Address*, the rules are "an address is
four segments separated by dots; a segment is one to three digits with no
leading zero unless it is exactly `0`". Nothing mentions itself: a single left-
to-right scan with a couple of counters is the whole solution. For *Lisp
Expression Parser*, "a list is `(`, zero or more expressions, `)`" and an
expression may be a list — the rule mentions itself, at arbitrary depth, and no
amount of `split` will save you.

The tool is wrong when the text has no grammar. If the question is "does this
pattern occur", you want [[string-matching]]. If it is "the longest substring
with some property", you want [[sliding-window]]. And if the delimiter genuinely
never appears inside a field and the statement says so, `split` is the correct
answer and building a parser is showing off. *Chemical Formula Weight* says the
formula contains no parentheses, which is the statement telling you, in so many
words, not to bring a stack.

## The idea

Two layers, and a one-way valve between them.

The **scanner** (or tokenizer, or lexer) reads characters and emits tokens. A
token is a pair: what kind of thing it is, and the text it was made of. `40`
becomes one `num` token, not two digits. `<=` becomes one `le` token, not a `<`
and an `=`. After this layer, the notion of "character" is gone.

The **parser** reads tokens and builds meaning — a value, a tree, a list of
records. It never looks at a character, never re-splits a token, never counts
spaces. Everything about whitespace, quoting and escaping was settled below it.

Both layers run on the same primitive: **a cursor that only moves forward**. And
every function that touches the cursor obeys one contract, which is the sentence
this whole chapter is built on:

> A parse function is entered with the cursor on the first symbol of the thing it
> recognises, and it returns with the cursor exactly one past the last symbol of
> that thing.

That is it. If every function keeps that promise, functions compose: a caller can
invoke a callee, and afterwards the cursor is in exactly the right place to carry
on, with no coordination and no cleanup.

<svg viewBox="0 0 660 230" role="img" aria-label="two-layer pipeline from characters to tokens to a value, with a forward-only cursor over the token array">
  <g>
    <text x="10" y="22">characters</text>
    <rect x="10" y="32" width="200" height="34" rx="4"/>
    <text x="24" y="55">2 * ( 3 + 4 0 )</text>
    <line x1="215" y1="49" x2="265" y2="49"/>
    <line x1="265" y1="49" x2="253" y2="43"/>
    <line x1="265" y1="49" x2="253" y2="55"/>
    <text x="272" y="45">scanner</text>
    <text x="272" y="62">(quotes, escapes,</text>
    <text x="272" y="78">numbers, spaces)</text>
    <text x="10" y="118">tokens</text>
    <rect class="fill" x="10" y="128" width="62" height="34" rx="4"/>
    <rect x="76" y="128" width="46" height="34" rx="4"/>
    <rect x="126" y="128" width="40" height="34" rx="4"/>
    <rect x="170" y="128" width="62" height="34" rx="4"/>
    <rect x="236" y="128" width="46" height="34" rx="4"/>
    <rect x="286" y="128" width="72" height="34" rx="4"/>
    <rect x="362" y="128" width="40" height="34" rx="4"/>
    <text x="20" y="151">num 2</text>
    <text x="94" y="151">*</text>
    <text x="141" y="151">(</text>
    <text x="180" y="151">num 3</text>
    <text x="254" y="151">+</text>
    <text x="296" y="151">num 40</text>
    <text x="377" y="151">)</text>
    <line x1="146" y1="196" x2="146" y2="168"/>
    <text x="96" y="214">cursor i, forward only</text>
    <line x1="412" y1="145" x2="462" y2="145"/>
    <line x1="462" y1="145" x2="450" y2="139"/>
    <line x1="462" y1="145" x2="450" y2="151"/>
    <text x="470" y="141">parser</text>
    <text x="470" y="158">(grouping, nesting,</text>
    <text x="470" y="174">precedence)</text>
    <text x="470" y="202">value: 86</text>
  </g>
</svg>

Once the layers are separated, writing the parser is transcription rather than
invention, because grammar notation and code are the same thing twice:

| in the grammar | in the code |
| --- | --- |
| one thing then another | two statements in a row |
| this **or** that | `if` on the next token |
| zero or more | a `while` loop |
| a rule that mentions itself | a recursive call, or a stack frame you push |

A grammar for arithmetic, with the precedence levels written as separate rules:

```
expr   := term (('+' | '-') term)*
term   := factor ('*' factor)*
factor := num | '(' expr ')'
```

Three rules, three functions. Nowhere in the code will there be a table of
operator precedences; the precedence is already there, encoded as *which
function calls which*.

## Worked by hand

Parse `2*(3+40)` with those three rules. The scanner has already run, so the
cursor walks a token array of length 7:

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| token | `num 2` | `*` | `(` | `num 3` | `+` | `num 40` | `)` |

`i` starts at 0. Read the table as a call trace: each row is one thing a function
did, and "returns" means it handed a value back to its caller.

| step | who | `i` before | token there | what it does | `i` after |
| --- | --- | --- | --- | --- | --- |
| 1 | `expr` | 0 | `num 2` | needs a `term` first, calls it | 0 |
| 2 | `term` | 0 | `num 2` | needs a `factor` first, calls it | 0 |
| 3 | `factor` | 0 | `num 2` | not `(`, so consume the number, **returns 2** | 1 |
| 4 | `term` | 1 | `*` | it is `*`: consume, call `factor` | 2 |
| 5 | `factor` | 2 | `(` | it is `(`: consume, call `expr` | 3 |
| 6 | `expr` | 3 | `num 3` | calls `term`, which calls `factor` | 3 |
| 7 | `factor` | 3 | `num 3` | consume, **returns 3** | 4 |
| 8 | `term` | 4 | `+` | not `*` — **returns 3** untouched | 4 |
| 9 | `expr` | 4 | `+` | it is `+`: consume, call `term` | 5 |
| 10 | `term` | 5 | `num 40` | via `factor`, **returns 40** | 6 |
| 11 | `expr` | 6 | `)` | not `+`/`-`: folds 3 + 40, **returns 43** | 6 |
| 12 | `factor` | 6 | `)` | expects `)`, consumes it, **returns 43** | 7 |
| 13 | `term` | 7 | end | not `*`: folds 2 × 43, **returns 86** | 7 |
| 14 | `expr` | 7 | end | not `+`/`-`: **returns 86** | 7 |

Four things in that table are worth more than the answer.

**Step 8 is where precedence lives.** `term` was sitting on a `+` and walked
away from it. It did not handle it, did not error, did not peek further — it
returned, leaving the `+` for whoever called it. That refusal is the entire
mechanism. `*` binds tighter than `+` because `term` is *willing* to consume `*`
and *unwilling* to consume `+`, and `term` is the one called from inside `expr`.
Swap the two rules and you swap the precedence, without touching a single
comparison.

**Values and positions travel on different channels.** Look at the two rightmost
columns against the "returns" notes: `i` only ever increases, flowing forward
through a cursor that every function shares. Values only ever flow *upward*,
along return edges. Nothing ever flows backwards or downwards. That separation is
why you can reason about one function at a time.

**Step 12 is the only validation in the whole trace.** Every other step either
consumed something it had already looked at, or declined. The single place the
parser can say "this input is malformed" is where a rule demands a specific token.
Given `2*(3+40`, step 12 finds the end of input instead of `)` and that is the
only place the error can surface. When a bracket error is reported at a strange
position, this is why.

**Count the frames at step 7.** The stack is `expr, term, factor, expr, term,
factor` — six frames for one level of parentheses. Three grammar levels means
roughly three frames per nesting level, so Python's default limit of 1000 frames
is reached at about 330 nested parentheses. An input of `"("*400` is not exotic;
it fits in any constraint that says `n <= 10^5`.

## Why it is correct

A parser is correct when it accepts exactly the strings the grammar derives, and
returns the value of the tree the grammar builds. Both halves need proof, and
both come from one induction.

:::proof Recursive descent computes the value of the unique parse tree
**Setup.** Let `t[0..n-1]` be the token array and let the grammar be the three
rules above. Write `E(i)`, `T(i)`, `F(i)` for the functions `expr`, `term`,
`factor` invoked with the cursor at `i`. Say that a token range `[i, j)` **is an
`A`** when the substring of tokens `t[i..j)` is derivable from nonterminal `A`.

**The contract (the invariant).** For each rule `A` and each position `i`: if
some range starting at `i` is an `A`, then `A(i)` terminates, returns the value of
the *longest* such range `[i, j)`, and leaves the cursor at `j`. If no range
starting at `i` is an `A`, `A(i)` raises.

**Measure.** Define `μ(i) = n - i`, the number of tokens left. Every call is made
at some cursor position; order the calls by `μ` at entry, breaking ties by the
rule's depth in the chain `expr > term > factor`. This pair `(μ, depth)` strictly
decreases at every call, which is what the induction will run on.

**Base case: `factor(i)` with `t[i]` a number.** No call is made. The function
consumes one token and returns its integer value, leaving the cursor at `i + 1`.
The only range starting at `i` derivable from `factor` via the `num` alternative
is `[i, i+1)`, and it is therefore the longest. Contract holds, with `μ`
decreasing by exactly 1.

**Inductive step, `factor(i)` with `t[i] = '('`.** It consumes `(`, so the inner
call `E(i+1)` has `μ = n - i - 1 < n - i`: strictly smaller, so the induction
hypothesis applies. If a range starting at `i` is a `factor` at all, then by the
grammar it must have the form `( e )` with `e` an `expr` starting at `i+1`; by
hypothesis `E(i+1)` returns that `expr`'s value and stops at some `j`. The rule
then demands `t[j] = ')'`; if it is not, no `factor` range started at `i`, and
raising is correct. Otherwise the returned value is the value of the inner
expression, the cursor is at `j + 1`, and `[i, j+1)` is the unique — hence
longest — `factor` range at `i`.

**Inductive step, `term(i)`.** It calls `F(i)`, which is a strictly smaller
`(μ, depth)` pair, getting a value `v` and a cursor `j`. Then, while `t[j] = '*'`,
it consumes the `*` (so `μ` drops) and calls `F(j+1)` (smaller `μ` still),
updating `v ← v × F(j+1)`. Each iteration consumes at least one token, so the loop
runs at most `n - i` times and terminates. On exit, `t[j]` is not `*`, so no
longer `term` range begins at `i`: any extension would have to continue with `*`.
The accumulated `v` is the left-nested product `((f₁ × f₂) × f₃) …`, which is the
value of the parse tree for a left-associative `*`.

**Inductive step, `expr(i)`.** Identical with `term` in place of `factor` and
`{+, -}` in place of `{*}`, folding left: `v ← v ± T(·)`.

**Termination.** Every call either consumes at least one token before its next
call, or descends one step in the fixed chain `expr → term → factor` whose length
is 3. So between any two token consumptions at most 3 calls occur, and the total
number of calls is at most `3(n + 1)`. Nothing runs forever.

**Uniqueness of the tree.** The grammar is unambiguous: at any position the rule
to apply is determined by one token of lookahead (`(` versus `num` in `factor`;
`*` versus anything else in `term`; `+`/`-` versus anything else in `expr`), and
the loops are maximal. So the range each function returns is forced, the tree is
unique, and the value the functions compute is the value of that tree. ∎
:::

Now name what the proof used, because that list is where the bugs live.

- **One token of lookahead decides every branch.** The uniqueness argument needed
  the alternatives of a rule to start with *different* tokens. When two can both
  begin with `num`, the `if` has nothing to go on and will confidently pick the
  wrong one. That property is called LL(1), and the fix when it fails is to factor
  the common prefix into a shared rule, not to add more `elif`s.
- **No rule is left-recursive.** If `expr := expr '+' term`, then `E(i)` calls
  `E(i)` with `μ` unchanged, and the measure does not decrease. That is not a
  slow parser; it is an immediate stack overflow. Left recursion is *always*
  rewritten as a loop, which is exactly what the `*` in `term (…)*` is.
- **Every loop iteration consumes at least one token.** Termination rested on it.
  A rule that can match the empty string, placed inside a `while`, spins forever
  — and it hangs rather than crashing, which makes it the hardest bug in this
  chapter to find.
- **The cursor never rewinds.** The proof treats failure as fatal. The moment you
  add backtracking — try one alternative, restore `i`, try another — the linear
  bound in the termination argument evaporates, and so does the guarantee that a
  function's effect on the cursor is a function of where it started.
- **The scanner is already correct, and does not depend on the parser.** The
  whole proof is stated over tokens. If `40` arrives as two tokens, or a quoted
  space arrives as a separator, nothing above is even about your input.
- **The input is valid, if the statement says so.** *Lisp Expression Parser*
  promises exactly one well-formed root expression. The proof describes what the
  code does on derivable input and says nothing about the rest. That is why
  validation is a separate job with its own problems — *Rich Text Parser Part 1
  (Validate Tokens)* exists precisely to be that job, before Part 2 parses.

## What it costs

Derive it in two pieces, because the two layers have different arguments.

**The scanner is Θ(n) by a counting argument, not by inspection.** The loop looks
like it might be quadratic: some branches contain an inner `while` that runs over
a run of digits or the inside of a quoted region. But each inner loop advances the
same cursor that the outer loop reads, and the cursor never rewinds, so every
character is examined by at most one inner loop plus a constant number of outer
tests. Summing token lengths gives `Σ|tokenₖ| ≤ n`. Total: **Θ(n)** time,
`Θ(number of tokens) = O(n)` space for the token list.

**The parser is Θ(n) for a fixed grammar, by the call count in the proof.** Let
`d` be the number of rules in the longest descent chain — here `d = 3`, one per
precedence level. Between two token consumptions there are at most `d` calls, and
there are at most `n` consumptions, so the number of calls is `O(d·n)`. Each call
does `O(1)` work of its own. Total **Θ(d·n)**, and `d` is a property of the
grammar, not the input, so **Θ(n)**.

As a recurrence: a parenthesised group costs `T(n) = T(n − 2) + O(1)`, and a
sequence of `k` operands costs `T(n) = Σ T(nᵢ) + O(k)` with `Σ nᵢ ≤ n`. Both give
`Θ(n)`. There is no `log` anywhere; if your parser is not linear, it is because of
something you added.

**Space is the recursion depth, and that is the number people get wrong.** The
token list is `O(n)`, but the call stack is `Θ(d · maxdepth)`, where `maxdepth` is
the nesting depth of the input. For `(((…1…)))` the depth is `Θ(n)`. Python's
default recursion limit is 1000 frames; with `d = 3` that is about 330 levels of
nesting before `RecursionError`. Any statement that allows adversarial nesting —
and *Basic Calculator*, *Number of Atoms* and *Decode Repeated Groups* all do —
argues for the explicit-stack form in the next section.

**The costs people forget**, all three of them in Python:

- *Slicing inside the loop.* `s = s[1:]` to "consume a character" copies the rest
  of the string every time: `n` iterations copying `O(n)` characters each is
  `Θ(n²)`. Symptom: correct answers, timeout at `n = 10⁵` and never at `n = 10³`.
  Move a cursor; never rebuild the input. Building output with `+=` on a string is
  the same cost with the same symptom — append to a list and `''.join` once.
- *Regex with nested quantifiers.* `(a+)+b` against a long run of `a`s makes
  Python's backtracking engine explore exponentially many splits. *Validating
  Magical Binary Strings with RegEx* is a legitimate regex problem — the language
  really is regular — but a regex for arithmetic nesting is not slow, it is
  impossible, for the reason given in the self-checks below.

## The implementation

```python run
import random

def tokenize(s):
    """Characters -> [(kind, text)]. Past this point there are no characters."""
    toks, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == " ":
            i += 1
        elif c.isascii() and c.isdigit():
            j = i
            while j < n and s[j].isascii() and s[j].isdigit():
                j += 1
            toks.append(("num", s[i:j]))          # ONE token, not j - i of them
            i = j
        elif c in "+-*()":
            toks.append((c, c))
            i += 1
        else:
            raise ValueError("stray %r at %d" % (c, i))
    return toks


class Parser:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i][0] if self.i < len(self.t) else "end"

    def take(self, kind):
        assert self.peek() == kind, "expected %s, saw %s" % (kind, self.peek())
        self.i += 1
        return self.t[self.i - 1][1]

    def expr(self):                                 # expr := term (('+'|'-') term)*
        v = self.term()
        while self.peek() in ("+", "-"):
            op = self.take(self.peek())
            rhs = self.term()
            v = v + rhs if op == "+" else v - rhs    # fold LEFT, never recurse right
        return v

    def term(self):                                 # term := factor ('*' factor)*
        v = self.factor()
        while self.peek() == "*":
            self.take("*")
            v = v * self.factor()
        return v

    def factor(self):                               # factor := num | '(' expr ')'
        if self.peek() == "(":
            self.take("(")
            v = self.expr()
            self.take(")")                          # the only structural check
            return v
        return int(self.take("num"))


def evaluate(s):
    p = Parser(tokenize(s))
    v = p.expr()
    assert p.peek() == "end", "trailing junk at token %d" % p.i
    return v


for text, want in [("2*(3+40)", 86), ("1-2-3", -4), ("2*3+4*5", 26), ("100", 100)]:
    print("%-10s = %d" % (text, evaluate(text)))
    assert evaluate(text) == want

try:
    evaluate("1+2)3")
    raise SystemExit("should have rejected")
except AssertionError as e:
    print("rejected '1+2)3':", e)

def gen(rng, depth):                                # random (text, value) pairs
    if depth == 0 or rng.random() < 0.35:
        v = rng.randint(0, 20)
        return str(v), v
    a, av = gen(rng, depth - 1)
    b, bv = gen(rng, depth - 1)
    op = rng.choice("+-*")
    return "(%s%s%s)" % (a, op, b), av + bv if op == "+" else av - bv if op == "-" else av * bv

rng = random.Random(3)
for _ in range(500):
    text, want = gen(rng, 5)
    assert evaluate(text) == want, text
print("500 random nested expressions evaluate exactly")
```

Three lines carry the weight.

`toks.append(("num", s[i:j]))` is the valve. It is the moment `40` stops being
two characters and becomes one thing. Every bug involving multi-character tokens
— `<=` split into two, a negative number read as an operator and a number, a
decimal point ending a number early — is a bug in this line, and it is
undebuggable from the parser, because by then the evidence is gone.

`while self.peek() in ("+", "-")` with `v = v + rhs` is the `*` of the grammar
rendered as a *left fold*. The tempting alternative — parse a term, see `-`,
recurse into `expr` for the rest — is shorter and gives `1-2-3 = 2`, because it
computes `1 - (2 - 3)`. Every left-associative operator must be a loop. Only
right-associative ones (exponentiation, assignment, the `?:` chain) recurse.

`assert p.peek() == "end"` is the line nobody writes and everybody needs. Without
it, `evaluate("1+2)3")` cheerfully returns 3: `expr` parsed a complete expression
and had no reason to look further. A parser that does not check it reached the end
is a parser that silently accepts garbage with a valid prefix — and interview
inputs are chosen to have exactly that shape.

## Variants you will meet

**Field splitting, done from the correct end.** *Large Responses* hands you an
Apache log line whose request portion contains spaces and quotes, and asks for the
byte count — the final whitespace-separated field. Splitting from the left
requires understanding the quoting; `rsplit(maxsplit=1)` requires understanding
nothing. When the mess is on one side and your field is on the other, split from
the clean side.

**Validate without building.** *Validate IP Address* and *Validate Typed CSV
Records* ask only for a verdict, so there is nothing to construct: you are running
a [[state-machines|state machine]] and reporting whether it ended in an accepting
state. Write the states down as a list before the code.

**Counting depth instead of parsing.** *Rich Text Parser Part 1 (Validate Tokens)*
needs only an integer: add one at `(`, subtract at `)`, fail if it ever goes
negative, fail if it is nonzero at the end. Part 2 of the same set needs the
actual nesting, and that needs a [[stack]]. The difference between a counter and a
stack is whether you must remember anything *about* the enclosing group, or only
that there is one.

**Explicit stack instead of recursion.** Every recursive descent has a mechanical
translation into a loop with a stack of frames, and it is the right choice when
the input can nest deeply or when you are in a language with a small stack.

```python run
def expand(s):
    """count(body) groups, nested: '2(a3(b))' -> 'abbbabbb'. No recursion."""
    stack, cur, num = [], [], 0
    for ch in s:
        if ch.isascii() and ch.isdigit():
            num = num * 10 + int(ch)                 # digits accumulate
        elif ch == "(":
            stack.append((cur, num if num else 1))   # push the ENCLOSING context
            cur, num = [], 0
        elif ch == ")":
            prev, k = stack.pop()
            prev.append("".join(cur) * k)            # fold the finished group up
            cur, num = prev, 0
        else:
            cur.append(ch)
    assert not stack, "unclosed ("
    return "".join(cur)


def expand_rec(s, i=0):
    """The same grammar by recursion, to show they agree - and where it breaks."""
    out, num = [], 0
    while i < len(s):
        ch = s[i]
        if ch.isascii() and ch.isdigit():
            num, i = num * 10 + int(ch), i + 1
        elif ch == "(":
            body, i = expand_rec(s, i + 1)
            out.append(body * (num if num else 1))
            num = 0
        elif ch == ")":
            return "".join(out), i + 1
        else:
            out.append(ch)
            i += 1
    return "".join(out), i


for t in ["2(a3(b))", "ab", "3(x)y", "2(2(z))"]:
    got = expand(t)
    assert got == expand_rec(t)[0]
    print("%-10s -> %s" % (t, got))

deep = "1(" * 3000 + "z" + ")" * 3000
print("nesting depth 3000, stack version:", repr(expand(deep)))
assert expand(deep) == "z"
try:
    expand_rec(deep)
    print("recursive version: survived")
except RecursionError:
    print("recursive version: RecursionError - same grammar, same answer, no stack")
```

The frame pushed at `(` holds the *enclosing* partial result and the repeat count,
not the group being opened. That is the general rule for turning recursion into a
stack: what you push is the caller's local state, because that is exactly what a
call frame saves.

**Parse to a tree, then evaluate.** Everything above evaluates while parsing,
which is fine when the answer is needed once. Build a tree instead when the
structure will be used more than once — *Predicate Expression Tree Evaluator* and
*Parse Boolean Rule Expressions* evaluate the same expression under different
variable bindings, and *Construct Binary Tree S-Expression* wants the tree itself.
See [[serialize-tree]] for the reverse direction.

**Indentation and depth prefixes as structure.** *Parse Indented YAML Mappings*
encodes nesting as two spaces per level; *Recover a Tree from Preorder Depth
Encoding* encodes it as a run of hyphens; *Render a Task Tree from CSV Rows* puts
it in a parent column. All three are the same algorithm: keep a stack whose height
*is* the current depth, pop until the stack height matches the new line's depth,
then attach. No brackets required — the depth number is the bracket.

**Parsing as step one of a graph problem.** *Spreadsheet Formula Dependencies* and
*Resolve Variable Equations with Dependency Errors* are [[topological-sort]]
problems wearing a parser as a hat. Parse the references, build edges, then run
the real algorithm; recognising that seam saves you from trying to detect cycles
inside the parser. *Compare Version Numbers* is the degenerate case — the parse is
trivial and the definition of "equal" is the whole problem.

**A tokenizer you are given.** The *Rich Text Parser* set hands you the token
array and says commas are dropped. When a statement gives you tokens, the first
layer is done and every character-level worry with it — so do not reintroduce one
by joining the tokens back into a string.

## Recognising it in a statement

Ordered by how much you should trust them.

1. **The statement contains a grammar.** A bulleted list of the form "a parameter
   has one of the following forms: …" is a grammar written in prose. *Parse Query
   String* and *Parse Command-Line Tokens* both do this literally. Transcribe the
   bullets into functions in the same order and you are most of the way done.
2. **"Nested", "may nest", "parenthesized group", "may contain more groups".**
   Unbounded depth, therefore a stack or recursion, therefore not `split` and not
   a regex.
3. **A worked example whose punctuation is doing work.** If the sample input has
   quotes, brackets, colons or equals signs in it, every one of those characters is
   a rule you must handle.
4. **"Valid", "well-formed", or a `Neither` return value.** A recogniser, not a
   builder. Enumerate the failure modes before writing anything.
5. **A separator that can also appear inside a field.** *Split a Log Outside
   Quotes* is this stated outright, and *Validate Typed CSV Records* implies it.
   The moment you read this, `split` is off the table.
6. **Sizes that rule out cleverness.** `n` up to `10⁵` with a nesting-capable
   grammar means one linear pass and an explicit stack, not a regex and not
   repeated scanning.

The anti-signals, which matter just as much:

- **The statement promises the simple case.** "The formula contains no
  parentheses" (*Chemical Formula Weight*), "the input is valid" (*Lisp Expression
  Parser*), "tokens are separated by one or more spaces" (*Stack Command Output*).
  Each of those is permission to delete code. Take it.
- **The text is homogeneous and the question is about a window or a count.** That
  is [[sliding-window]] or [[frequency-counting]], and a tokenizer will just be in
  the way.
- **Only one field is wanted, and it is at a fixed end.** Reach for `rsplit` or a
  slice, not a grammar.

## Traps

**Splitting on a delimiter that occurs inside a field.** Symptom: correct on every
sample case, wrong on one production-shaped record. Demonstrated below.

**A loop iteration that can consume nothing.** Symptom: a hang, not a wrong
answer — killed by the time limit with no output. It happens when a nullable rule
(`digits*` matching zero digits) sits inside a `while`. The cure is structural:
make consumption the first statement of every loop body.

**Unary minus.** `-3+4` and `5-3` use the same character for two different
tokens. The scanner cannot tell them apart from the character alone; the
disambiguation is "what came before" — a minus at the start of an expression, or
right after an operator or `(`, is unary. Symptom: a stray `expected num, saw -`,
or an answer off by twice the operand.

**Trusting `int()` and `isdigit()` to mean what the spec means.** `int(" 12 ")`
is 12, `int("+5")` is 5, `int("1_2")` is 123 — Python's parser accepts whitespace,
signs and underscores. And `str.isdigit()` is true for characters `int()` refuses.
Symptom: a validator that accepts inputs the statement lists as invalid.
Demonstrated below.

**Returning after the first complete parse.** Symptom: garbage after a valid
prefix is accepted. Cure: the end-of-input assertion in `evaluate`.

**Recursion depth.** Symptom: `RecursionError` only on the largest hidden test.
Cure: the stack version above, or raise the limit and know why you did.

**Rebuilding the string as you consume it.** Symptom: a timeout that scales
quadratically. Cure: a cursor.

```python run
def naive(line):
    return line.split(" ")

def scan(line):
    """Split on spaces outside double quotes; quotes group and are dropped."""
    out, cur, inq, quoted = [], [], False, False
    for ch in line:
        if ch == '"':
            inq, quoted = not inq, True          # '""' must yield one empty token
        elif ch == " " and not inq:
            if cur or quoted:
                out.append("".join(cur))
            cur, quoted = [], False
        else:
            cur.append(ch)
    if cur or quoted:
        out.append("".join(cur))
    return out

log = 'GET "/a b?x=1" 200  5120'
print("naive :", naive(log))
print("scan  :", scan(log))
assert scan(log) == ["GET", "/a b?x=1", "200", "5120"]
assert len(naive(log)) == 6 and len(scan(log)) == 4
assert scan('a "" b') == ["a", "", "b"]
print('scan(\'a "" b\') =', scan('a "" b'), "- the empty quoted field survives")

def is_int_lazy(f):
    try:
        int(f)
        return True
    except ValueError:
        return False

def is_int(f):                                    # "optional '-' then one or more digits"
    body = f[1:] if f.startswith("-") else f
    return bool(body) and all("0" <= c <= "9" for c in body)

print("%-8s %-8s %-8s %s" % ("field", "int()", "strict", "isdigit()"))
for f in [" 12 ", "+5", "1_2", "-7", "²", "١٢"]:
    print("%-8r %-8s %-8s %s" % (f, is_int_lazy(f), is_int(f), f.isdigit()))
    assert is_int(f) == (f == "-7")
assert is_int_lazy(" 12 ") and is_int_lazy("+5") and is_int_lazy("1_2")
assert "²".isdigit() and not is_int_lazy("²")     # isdigit says yes, int() raises
assert is_int_lazy("١٢")                          # int() parses Arabic-Indic digits
print("try/int accepts 4 strings the spec forbids; isdigit accepts 2 more")
```

The first half is *Split a Log Outside Quotes* in nine lines, and the assertion
`len(naive(log)) == 6` is the whole trap in one number: the naive split found six
fields where there are four, and it did so without raising anything.

The second half is *Validate Typed CSV Records*, whose `INTEGER` is "an optional
leading minus sign followed by one or more digits". `try: int(f)` is a different,
more generous predicate, and the difference is invisible until a test feeds it
`+5`. When a statement spells out a lexical rule, implement the rule; do not
delegate to a library function written to a different spec.

## What to memorise

**The contract**, which you should be able to say out loud before writing a line:
*a parse function starts on the first symbol of the thing it recognises and
returns with the cursor one past its last symbol.*

**The template**, in four pieces:

```python
toks = tokenize(s)        # 1. characters -> tokens. Quotes and numbers die here.
i = 0                     # 2. one cursor, forward only
def peek(): ...           #    peek / take(kind) / expect
def rule_A(): ...         # 3. one function per grammar rule; loops for '*',
def rule_B(): ...         #    calls for nesting, deeper function = tighter binding
assert peek() == "end"    # 4. and check you consumed everything
```

**The sentence** that turns a problem into this chapter: *"Can I write the legal
inputs as a handful of rules, and does any rule mention itself?"* No self-mention
means one scan and a state variable. Self-mention means a stack, and no `split`
or regex will ever be enough.

**The habit**: after the parse, assert the cursor reached the end. It costs one
line and it converts an entire class of silent wrong answers into a loud failure.

Numbers worth carrying: parsing a fixed grammar is `Θ(n)` time and
`Θ(nesting depth)` stack; Python gives you about 1000 frames, which is roughly
330 levels of nesting at three grammar rules per level; slicing the input inside
the loop turns `Θ(n)` into `Θ(n²)`.

## Check yourself

:::check
The parser contains no table of operator precedences, yet `2*3+4*5` evaluates to
26 rather than 70. Where is the precedence actually stored, and what one edit
would make `+` bind tighter than `*`?
--
It is stored in **which function calls which**. `expr` calls `term`, which calls
`factor`. Because `term` sits below `expr`, everything `term` consumes is gathered
into a single operand before `expr` ever sees it — so a `*` chain is always
finished before a `+` is considered. Equivalently: the rule furthest from the root
binds tightest.

The edit is to swap the two operator sets between the two rules: let `expr` loop
on `*` and `term` loop on `+`/`-`. Nothing else changes — same loops, same folds,
same number of lines. That such a small edit flips the semantics is the clearest
evidence that the call chain *is* the precedence table.
:::

:::check
Someone says: "I don't need a parser for *Rich Text Parser Part 2* — I'll write a
regex that matches balanced parentheses." Where are they wrong?
--
Balanced parentheses are not a regular language, so no finite automaton — and
therefore no true regular expression — can recognise them. The pumping lemma
makes it concrete: a machine with `k` states, fed `(ᵏ`, must revisit a state, so it
cannot distinguish `(ᵏ` from `(ᵏ⁺ʲ` and will accept a string with mismatched
depth. The missing ingredient is unbounded memory, which is exactly what a stack
or a recursion depth provides.

Two caveats worth stating, because the claim is not *always* wrong. Some regex
engines, Python's included through recursion or the `regex` package's extensions,
offer non-regular features that can match nesting — at which point you have a
parser with worse syntax and worse failure modes. And if the statement bounds the
depth, say at most two levels, then the language *is* regular and a regex is
legitimate, if ugly. The honest version of their sentence is "the depth is
bounded, so I can enumerate it", and they should say why they believe that.
:::

:::check
`1-2-3` should be `-4`. A candidate writes `expr` as: parse a term; if the next
token is `+` or `-`, consume it and recurse into `expr` for the right-hand side.
What does their code return, why, and which operators would the same code handle
correctly?
--
It returns 2. The recursion builds `1 - (2 - 3)` instead of `(1 - 2) - 3`,
because recursing on the right makes the *rest* of the expression a single operand
of the current operator. That is right-associativity, and `-` is not
right-associative.

The same code is correct for genuinely right-associative operators:
exponentiation (`2^3^2` is `2^9`), assignment (`a = b = c`), and the ternary
chain. The rule to carry: left-associative operators must be written as a loop
that folds into an accumulator; only right-associative ones recurse. And the
symptom to recognise is specific — the answer is right whenever there are fewer
than two operators of the same level, so a single sample case will not catch it.
:::

:::check
Why must the scanner, and not the parser, be the layer that knows about double
quotes? Answer in terms of the proof's assumptions.
--
The proof is stated entirely over the token array: "if some range of *tokens*
starting at `i` is derivable from `A`…". It says nothing about characters, which
means it is only about your actual input if the token array faithfully represents
it. Quoting decides where tokens begin and end — in *Split a Log Outside Quotes* a
space inside quotes is part of a token and a space outside it is a boundary — so
quoting is a statement about tokenisation, not about grammar.

Push it up into the parser and you break the layering in a specific way: the
parser would have to re-examine the characters inside tokens, which means the
token array is no longer the unit the cursor advances over, which means the
termination measure (`n − i` tokens remaining) no longer bounds the work. In
practice the symptom is that quoting rules end up duplicated in several parse
functions, and they disagree.
:::

:::check
A colleague's parser passes every sample for *Parse Query String* but fails a
hidden test. They add a re-scan: when a rule fails, reset the cursor and try the
next alternative. What have they given up, and what should they have done instead?
--
They have given up the linear-time guarantee and the ability to reason locally.
The termination and cost arguments both rested on the cursor never rewinding —
"between any two token consumptions at most `d` calls occur". With backtracking, a
position can be re-parsed once per alternative that reaches it, which on nested
choices compounds toward exponential, and a function's effect is no longer
determined by where it started.

The real bug is almost certainly that two alternatives share a prefix, so one
token of lookahead does not decide between them. *Parse Query String* has exactly
this shape: a parameter may be `key=value` or `!key`, and `!!key` and
`!key=value` are invalid. The fix is to look at the deciding token first — is the
first character `!`? — and then commit, with an explicit error for the invalid
combinations, instead of trying both and rewinding. Factoring the common prefix
out into one rule that handles both continuations is the general form of that fix.
:::
