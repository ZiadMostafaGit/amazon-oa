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
