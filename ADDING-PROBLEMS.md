# Adding problems from screenshots

How the 41 entries in `site/problems.js` were made, written so you can repeat it when you sit
another assessment and come away with new screenshots. Nothing here needs a server or a build step.

The order matters. Transcribe first, *verify* second, and only write an explanation once the
solution has survived verification — the reverse order is how the eleven wrong solutions that were
found in this repo got written in the first place.

---

## 1 · Get the images in

Drop them anywhere in `images/`. Filenames are free-form — spaces and parentheses are fine, they are
URL-encoded at render time. Keep the originals untouched; every crop is a separate file.

## 2 · Read them, and do not trust OCR

Most of these screenshots defeated OCR: subscripts, watermarks, and wide desktop shots came back as
mush. Two failures were only caught by *looking* at the pixels:

- **Minimum Errors** — the STDIN block says `y = 3`, the FUNCTION block underneath says `y = 2`.
  The exam contradicts itself. The explanation's arithmetic (`2×1 + 3×2 = 8`) settles it.
- **Maximum Quality Score** — the header says `impactFactor = 3`, every row of its own table
  computes with `2`.

When a statement and its worked example disagree, **trust the arithmetic in the example**, record
both readings, and move on. Do not bend a correct algorithm to reproduce an impossible number.

## 3 · Write the entry

One object per problem in `site/problems.js`. Everything else — the rail, the drawer, deep links,
search, progress — is derived from this array, so nothing else needs touching.

```js
{
  id:'shortslug', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Code Question 1', title:'Human readable title',
  minutes:45, score:'Max. score: 100',
  images:['image30.png','image33.png'],          // [] if the text was pasted, not shot
  fn:{name:'solveIt', ret:'int', params:[['int','k'],['int[][]','segment']]},
  tests:[ /* section 5 */ ],
  gen:`def gen(rng, n): ...`,                    /* section 6 */
  body:`
<p>…statement as HTML…</p>
<div class="ans">…answer panels…</div>
`}
```

`fn` drives the generated Python stub and is what the test runner calls — **the name and parameter
order must match the exam's signature exactly.** Set `fn:null` for a non-coding entry. Type strings
that map to Python hints: `int`, `long`, `string`, `boolean`, `int[]`, `int[][]`, `string[]`,
`boolean[]`, `char[]`.

Useful classes already styled: `.oa` (tables), `.sample` (pre blocks), `.note`, `.warn`, `.frag`
(a dashed marker where the source ran out), `.locked` (paywalled), `.srcnote`, `.cases`/`.case`.

Keep entries of the same `section` adjacent so the flat numbering stays in order. The body is a JS
template literal: no backticks and no `${` inside it.

## 4 · Crop the figures

Every diagram a problem needs you to *see* is a real cropped file, never a CSS window onto the
original — that scheme was tried and all but one figure framed the wrong region.

```sh
ffmpeg -i images/image26.jpg -vf "crop=268:256:29:144" images/fig-drone-ring.png   # w:h:x:y
```

```html
<figure class="fig">
  <img loading="lazy" src="../images/fig-drone-ring.png" alt="The ring of m hubs"
       data-full="../images/image26.jpg" title="Click to open the full screenshot">
  <figcaption>The ring of m hubs — the drone starts at Hub 1</figcaption>
</figure>
```

## 5 · Verify the solution before you believe it

This is the step that matters, and it is not optional. Every solution in this repo is executed
against its published samples; that pass alone found solutions that failed **their own printed
examples**.

```sh
# extract a solution from problems.js and run it against the samples
python3 - <<'PY'
import re, html
src = open('site/problems.js').read()
i = src.index("id:'getmincost'"); j = src.index("\n`}", i)
code = html.unescape(re.findall(r'<pre class="sample"><code>(.*?)</code></pre>', src[i:j], re.S)[0])
ns = {}; exec(code, ns)
print(ns['getMinCost']([1,1,2,1,1]), 'expected 3')
PY
```

Then, where you can afford one, write a **brute force** and compare on thousands of random inputs.
Every real bug found in this repo was found this way, not by reading:

| Technique | What it caught |
|---|---|
| exhaustive enumeration of all choices | Min Cost to Make Stations Equal (wrong on 28% of inputs) |
| Dijkstra over reachable states | the same, independently |
| all 2^k wildcard assignments | Minimum Errors — a greedy that returned 40 against a true 24 |
| every interleaving of two strings | Merge Conflicts (confirmed correct) |
| all segment × strategy pairs | Maximum Quality Score (confirmed correct) |
| the O(n²) version as an oracle | Count Promotional Periods — correct but would time out |

If you cannot verify it, say so in an amber `.unsure` box inside the Solution panel and give no test
cases. An admitted gap is worth more than a confident guess.

## 6 · Add test cases and a generator

**Never hand-type expected outputs.** Write the inputs, run a solution you have verified, and record
what it returns. In the app, the ＋ Add tests button on any problem without cases scaffolds both
blocks from that problem's own signature.

```js
tests:[
  {in:[[1,1,2,1,1]], out:3},
  {in:[[1,1,3]],     out:1}
],
gen:`def gen(rng, n):
    m = max(1, n)
    return [[rng.randint(1, m) for _ in range(m)]]`,
```

`gen(rng, n)` returns one random argument list and must honour the statement's constraints — disjoint
segments, distinct values, a sum divisible by n, whatever the problem promises. `n` is a target input
size: small values are used for fuzzing, large ones for the Big-O probe. Validate a new generator
before trusting it:

```sh
# 300 random inputs must never make the reference raise
python3 - <<'PY'
import random, copy
rng = random.Random(1)
for _ in range(300):
    args = gen(rng, rng.randint(1, 9))
    reference(*copy.deepcopy(args))
PY
```

Once `gen` is present, **Random** fuzzes the user's code against the solution shown in the Solution
panel (it is read from the page at run time, so it can never drift), and **Big-O** times the solution
on growing inputs.

## 7 · Write the explanation last

Each answer is four collapsed panels: *Hint 1*, *Hint 2*, *Solution*, and *Step by step*. The last
one derives every formula, says where each `± 1` comes from, and traces the published sample
numerically to the stated answer, with the winning row highlighted:

```html
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary>
<div class="inner">
  <div class="step"><h4>1 · Heading</h4>
    <p>…</p>
    <div class="formula">monospace derivation</div>
  </div>
  <table class="trace">…<tr><td class="hit">winning row</td></tr></table>
</div></details>
```

Close with a **Traps** step. The traps are not decoration — they are where the marks go.

## 8 · Check it still parses

```sh
node -e "global.window={};require('./site/problems.js');
         const P=window.PROBLEMS;
         console.log(P.length+' entries, '+P.filter(p=>p.tests).length+' with tests');"
```

Then open `site/index.html` and read your new entry cold.
