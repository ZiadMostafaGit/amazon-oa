# How a chapter is written

One file per topic: `topics/articles/<slug>.md`. The reader is someone who can
program, is preparing for interviews, and wants to *understand* the topic rather
than collect snippets. Assume they are smart and know nothing about this
particular subject.

The model chapter is `topics/articles/binary-search.md`. Read it before writing.
Match its voice: direct, concrete, no filler, no "in today's fast-paced world",
no exclamation marks, no emoji. Explain like a good textbook, not like a blog.

## The outline is fixed

These eleven `##` headings, spelled exactly like this, in this order:

```
# <the canon title, exactly>

> One sentence: what this topic really is. Not a definition — the insight.

## When you reach for it
## The idea
## Worked by hand
## Why it is correct
## What it costs
## The implementation
## Variants you will meet
## Recognising it in a statement
## Traps
## What to memorise
## Check yourself
```

`###` subheadings inside a section are fine. Nothing may be added before the
lede or after `## Check yourself`.

What each section owes the reader:

- **When you reach for it** — the trigger. The shape of a problem that makes
  this the right tool, and the shape that makes it the wrong one.
- **The idea** — the one mental image. Build it before any code. If you can say
  it in a sentence, say it in a sentence.
- **Worked by hand** — a small concrete instance traced step by step, usually as
  a table of the state after each step. The reader must be able to follow with a
  pen. Then say what the trace shows that the code alone would not.
- **Why it is correct** — a real argument in a `:::proof` block: the invariant,
  the base case, the inductive step, and why it terminates (or, for a data
  structure, why each operation preserves the representation invariant; for a
  greedy, an exchange argument; for a DP, why the recurrence covers every
  optimal solution). After the proof, say in plain words which assumptions it
  used — that list is where bugs come from.
- **What it costs** — derive the complexity, do not assert it. Include the
  recurrence or the counting argument, the space, and the cost of the thing
  people forget (a predicate, a copy, a hash).
- **The implementation** — clean, idiomatic Python, in a ```python run block,
  with asserts and prints so running it proves the claims. Explain the two or
  three lines that are doing the real work, and why they are written that way.
- **Variants you will meet** — the family. Each variant: one line on what
  changes, and a `[[link]]` if it has its own chapter.
- **Recognising it in a statement** — the phrases, constraints and asymmetries
  that give it away, ordered by how reliable they are. Include the anti-signal:
  what looks like this topic but is not.
- **Traps** — the specific ways people get it wrong, each with the symptom.
  Prefer traps you can demonstrate; a small wrong-vs-right ```python run block
  is worth three paragraphs.
- **What to memorise** — deliberately short. The template worth typing from
  muscle memory, the sentence that turns a problem into it, and the one habit
  that prevents the common bug. Plus any numbers worth carrying.
- **Check yourself** — three to six `:::check` blocks. Real questions with real
  answers, not trivia. At least one should ask *why*, and at least one should be
  a "someone claims X — where are they wrong".

## The dialect

Plain Markdown, plus:

    ```python run          a code block that is EXECUTED by the verifier
    ```python              a fragment, not executed (use sparingly)
    :::proof Title         the correctness argument
    :::note Title          an aside worth keeping
    :::warn Title          a trap worth shouting
    :::example Title       a worked example set apart
    :::check               a self-check; text, then a line with `--`,
                           then the answer
    :::                    closes any of the above
    [[topic-slug]]         a link to another chapter
    [[topic-slug|words]]   the same, with your own words
    <svg viewBox="...">    a diagram, inline, no external files

Tables, lists, blockquotes and `---` rules work as usual. Raw HTML other than
`<svg>` is escaped, and scripts and event handlers are stripped.

### Runnable code

Every ```python run block is executed in the same sandbox the practice editor
uses: no network, no filesystem, a few seconds of CPU. It must

- run standalone (no imports of project files, nothing from another block),
- print something a reader would want to see, and
- `assert` the claims the prose makes, so a broken chapter fails loudly.

Stdlib only. Keep each block under ~60 lines. Two or three runnable blocks per
chapter is the right number: the implementation, a variant, and a
wrong-vs-right demonstration.

### Diagrams

At least one inline `<svg>`, with a `viewBox` so it scales, and an
`aria-label`. Do not set colours: the stylesheet draws strokes in the ink
colour, `<text>` in the foreground colour, and anything with `class="fill"` in
the accent. Keep them schematic — a pointer walking an array, a tree with three
levels, a state machine with four nodes. A diagram that needs a paragraph to
explain is not a diagram.

## Length and honesty

3,000–5,000 words of prose (code and SVG do not count). Depth comes from
explaining *why*, not from padding.

The brief you are given says how many problems in this bank use the topic. Use
it:

- Many problems: name two or three of them by title where they illustrate a
  point ("*Stock Span I* is this with the comparison flipped").
- Marked RARE (zero problems here): say so plainly in the first section — "no
  problem in this collection uses this; it is here because interviews elsewhere
  do" — and then teach it properly anyway.

Never claim a problem exists that you have not seen in the brief. Never invent
a company, a constraint or a benchmark number.

## The gate

    python3 tools/brief_topic.py <slug>       # read this first
    python3 tools/verify_topic.py <slug>      # must print "1/1 chapters pass"

The verifier checks the outline, the lede, the word count, the proof block, the
diagram, the self-checks, that every `[[link]]` names a real topic, and that
every runnable block actually runs and prints. Fix what it reports and run it
again. A chapter is not done until it passes.

---

# Version 2: the tutor chapter

Every chapter that is the main chapter of a roadmap node is written this way. The
model is a real tutoring conversation about 0/1 knapsack that a learner said
finally made it click (summarised below). The reader is the same person as
above, with one addition: **they want to be able to derive the technique on a
blank page, not recognise it.** A chapter has failed if, after reading it, they can
type the template but cannot say why each line is there.

## What made the model work, and what each chapter owes the reader

1. **It is derived, never handed down.** Start from the brute force a beginner
   would actually write. Show where it is slow (count it), notice the waste (draw
   it), and only then name the technique as the cure for that waste. The final
   template must appear as the *last* step of a derivation the reader watched,
   e.g. recursion, then memo, then table, then the compressed array.
2. **It names the question that unlocks it.** Knapsack: "what is the least the
   future needs to know about the past?" Answer: (items left, capacity left), so
   the state is (i, c). Each chapter has such a question; state it in bold, early,
   and come back to it.
3. **It corrects the wrong first instincts out loud.** Write "You might think X"
   for the two or three wrong ideas a learner really has, and kill each one
   with a tiny concrete counterexample. From the model: "the answer for limit 5 is
   the answer for limit 4 plus something" (no, you forget which items you used);
   "take it whenever it fits" (limit 10, items (6,13),(5,10),(5,10): greedy gets
   13, best is 20). These are the most valuable paragraphs in the chapter.
4. **Every trace uses real numbers, and every step says why.** Not "the
   algorithm proceeds": a table whose every cell can be checked with a pen, plus
   the story of at least one cell in words ("bag of size 5, item B (w=3,v=4)
   allowed: if I put B in, 2 units are left; the best for 2 units with the
   earlier items is already in the row above, column 2; add 4."). Show the
   recursion tree with the repeated subproblem circled, so the reader sees where
   the speed comes from.
5. **Abstract pictures are followed by concrete ones.** The model's first arrow
   diagram confused the reader, and the version that worked pointed at actual
   columns with actual values. If you draw a schematic, follow it immediately with
   the same thing on real numbers.
6. **Code is mapped back to the idea, line by line.** After the code, a short
   table or list: each line, in plain words, and which branch of the recursion it
   is ("line 3 is the skip branch; lines 4-5 are the take branch"). Settle the
   boring confusions explicitly, such as 0-based input vs a 1-based dp row, why
   row 0 exists, and what a cell does and does not store.
7. **The subtle line gets its own demonstration.** For knapsack it is the loop
   direction in the 1-D version. Show the right way and the wrong way on the same
   tiny input, with the array after every step and a `*` on overwritten cells,
   and point at the exact cell where the wrong one goes wrong. Then say what the
   wrong version accidentally computes (here: unbounded knapsack). Every
   technique has one or two lines like this. Find them.
8. **It gives a thinking checklist.** A short numbered list of questions to ask
   on every new problem of this family (what are the items, what is the shared
   resource, max/min/count/feasible, 0/1 or unbounded or k copies, does order
   matter, *which quantity is small*). The checklist is the transferable part.
9. **It covers the family, not just the textbook case.** Every variation an
   interview or OA can ask, each with: what changes in the state or loop, *why*,
   a three-line example, and a bank problem that teaches it as a `[[p:id|Title]]`
   link (only ids you saw in the brief). Say which variations are rare.
10. **It ends with exercises the reader does by hand.** At least two `:::check`
    blocks are traces ("fill this 4x6 table; then do the 1-D version both ways
    and find the cell where an item is used twice"), with the full answer
    after `--`.

## The outline (exact headings, this order)

```
# <the canon title, exactly>

> One sentence: the insight, not a definition.

## The problem it solves
## Build it from the brute force
## Worked by hand
## From the idea to the code
## Why it is correct
## What it costs
## How to think about it
## Variations
## Recognising it in a statement
## Traps
## What to memorise
## Check yourself
```

- **The problem it solves**: one concrete motivating problem, the naive
  solution and why it is too slow or wrong, and when this is the wrong tool.
- **Build it from the brute force**: points 1-3 above. Ends with the technique
  stated in one sentence and the unlocking question in bold.
- **Worked by hand**: points 4-5. One full trace, plus a second trace on a case
  that shows something the first did not (a skip that beats a take, an
  overwrite, a tie).
- **From the idea to the code**: the derivation's last steps as code
  (```python run blocks with asserts): the direct version first, then the
  optimised one. Points 6-7 live here.
- **Why it is correct**: a `:::proof` block, written so a reader who has never
  seen a proof can follow it, and then the assumptions it used in plain words.
- **What it costs**: derived. Name the trap, such as pseudo-polynomial or the
  hidden log.
- **How to think about it**: point 8, the checklist, plus how to tell
  this technique from its neighbours.
- **Variations**: point 9.
- **Recognising it in a statement**: phrases and constraints, ordered by
  reliability, plus disguised forms (the algebra that turns "+/- signs to reach
  T" into subset sum), plus anti-signals.
- **Traps**: each with its symptom, at least one wrong-vs-right run block.
- **What to memorise**: short. The template, the one sentence, the one habit.
- **Check yourself**: 5-8 `:::check` blocks: hand traces, a "why",
  "someone claims X: where are they wrong", and a disguised problem to reduce.

Length: 4,500-13,000 words of prose. At least three ```python run blocks, at
least one inline `<svg>`. The voice is unchanged: direct, concrete, no filler.
The model is a patient tutor at a whiteboard, not a reference manual. Short
sentences. When a point is hard, say it twice, in two different ways.
`tools/verify_topic.py` recognises this outline by its second heading and
holds it to these rules.
