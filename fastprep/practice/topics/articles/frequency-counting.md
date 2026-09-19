# Frequency Counting

> Counting is the easy part. The topic is the choice of what you write on the
> pigeonhole — and the trick of turning the map inside out so that the counts
> themselves become the index.

## When you reach for it

One hundred and ten problems in this bank use frequency counting, which puts it
at #33 of 150 — not because counting is hard, but because an enormous number of
questions turn out to be questions about a *multiset*: a bag of things where only
the tallies matter and the order does not.

The trigger, stated as a test you can apply: **shuffle the input. Does the answer
change?** If it does not, the answer is a function of the counts alone, and your
job is to build the count map and read the answer off it. *Sort Characters by
Frequency*, *Top K Frequent Elements*, *Group Anagrams*, *Word Frequency in a
Large Text* and *Frequency Equals Card Value* all pass that test.

Two families share the counter's machinery, which is why they are folded into
this chapter. **Grouping** is the same loop with a different payload: instead of
`count[k] += 1` you write `group[k].append(item)`, as in *Group Anagrams*, *Find
Duplicate Files in a Filesystem*, or *Email Log Processing, Grouping, and
Sorting*. **Bucketing** is the same loop with a *computed* key,
`bucket = value // width` — *Latency Bucket Counter* histograms latencies at a
fixed width, *Group Sparse Points by Distance Threshold* keys points by grid cell.

The tool is wrong when order or position is part of the answer. "Longest
substring with at most `k` distinct characters" uses a counter, but the algorithm
is [[sliding-window]] — the counter is a component, not the plan. And an answer
that must name a *position* is only half a counting problem: counts get you the
*which*, a second pass over the original order gets you the *where*.

One anti-signal is worth naming immediately, because the word is a trap. *Token
Bucket Request Decisions* and *Concurrent Token-Bucket Rate Limiter* have "bucket"
in the title and nothing to do with this chapter: a token bucket counts *permits
over time*, and those are [[rate-limiting]] and [[simulation]]. "Bucket" is a very
weak signal; "how many times does each" is a very strong one.

## The idea

Picture a wall of pigeonholes. You walk the input once, and for each item you
drop a pebble into the pigeonhole whose label matches that item. At the end, the
wall *is* the answer to every question of the form "how many".

That much is a loop anybody can write. The content of this topic is two
decisions the loop does not make for you.

**First: you choose what is written on the pigeonholes.** The label is
`key(item)`, and choosing it *is* the problem. For *Group Anagrams* it is a
canonical form — the word's letters sorted, so `eat` and `tea` land in the same
hole. For *Most Common Product Pair* it is an unordered pair written as a sorted
tuple, so `(A, B)` and `(B, A)` share a hole. For *Most Common N-Grams* it is a
window of `n` consecutive tokens. Every one of those is "count things", and every
one is really a question about what counts as the same thing.

**Second: once the wall is built, you can hang it the other way round.** The map
runs key → count, and counts are integers between 1 and `n`, so they can index an
array. Build `bucket[f] = the keys whose count is f`, and one descending walk over
that array visits keys in decreasing frequency without sorting anything. That
inversion is the difference between an `O(d log d)` answer and an `O(n + d)` one,
and it is the move "top k frequent" problems are testing for.

<svg viewBox="0 0 660 250" role="img" aria-label="a key-to-count map inverted into an array of buckets indexed by count">
  <g>
    <text x="20" y="28">key → count</text>
    <rect x="20" y="40" width="130" height="34" rx="4"/>
    <text x="40" y="63">a</text>
    <text x="120" y="63">2</text>
    <rect x="20" y="74" width="130" height="34" rx="4"/>
    <text x="40" y="97">b</text>
    <text x="120" y="97">3</text>
    <rect x="20" y="108" width="130" height="34" rx="4"/>
    <text x="40" y="131">c</text>
    <text x="120" y="131">3</text>
    <text x="20" y="175">one pass over</text>
    <text x="20" y="195">the input</text>
    <line x1="175" y1="90" x2="255" y2="90"/>
    <line x1="255" y1="90" x2="243" y2="83"/>
    <line x1="255" y1="90" x2="243" y2="97"/>
    <text x="178" y="76">invert</text>
    <text x="290" y="28">count → keys</text>
    <rect x="290" y="40" width="60" height="34" rx="4"/>
    <text x="313" y="63">0</text>
    <rect x="290" y="74" width="60" height="34" rx="4"/>
    <text x="313" y="97">1</text>
    <rect class="fill" x="290" y="108" width="60" height="34" rx="4"/>
    <text x="313" y="131">2</text>
    <rect class="fill" x="290" y="142" width="60" height="34" rx="4"/>
    <text x="313" y="165">3</text>
    <rect x="290" y="176" width="60" height="34" rx="4"/>
    <text x="313" y="199">…</text>
    <text x="370" y="131">[ a ]</text>
    <text x="370" y="165">[ b, c ]</text>
    <line x1="560" y1="165" x2="560" y2="60"/>
    <line x1="560" y1="60" x2="553" y2="72"/>
    <line x1="560" y1="60" x2="567" y2="72"/>
    <text x="440" y="60">read downward from n:</text>
    <text x="440" y="235">frequency order, no sort</text>
  </g>
</svg>

Grouping and bucketing are the same wall with a different payload and label rule.
Counting keeps a tally; grouping keeps the items; bucketing computes the label
arithmetically instead of taking it from the item. One loop, three uses.

## Worked by hand

Take *Sort Characters by Frequency* on `s = "bbacccab"`. The spec: higher
frequency first, all copies of a character contiguous, ties by smaller ASCII code.

Pass one builds the counter, starting empty.

| step | char | `C` after | note |
| --- | --- | --- | --- |
| 1 | b | `{b:1}` | new key |
| 2 | b | `{b:2}` | |
| 3 | a | `{b:2, a:1}` | new key |
| 4 | c | `{b:2, a:1, c:1}` | new key |
| 5 | c | `{b:2, a:1, c:2}` | |
| 6 | c | `{b:2, a:1, c:3}` | |
| 7 | a | `{b:2, a:2, c:3}` | |
| 8 | b | `{b:3, a:2, c:3}` | final |

Pass two inverts it. `n = 8`, so the bucket array spans `0 … 8`; two slots are
occupied.

| bucket index `f` | keys with count `f` |
| --- | --- |
| 8 … 4 | — |
| 3 | `b`, `c` |
| 2 | `a` |
| 1 | — |

Pass three reads the buckets downward, sorting inside each one: level 3 emits
`bbb` then `ccc`, level 2 emits `aa`. Result `bbbcccaa`, eight characters in and
eight out.

Four things in that trace are invisible in the code.

**The counter is complete after every step, not only at the end.** After step 3,
`{b:2, a:1}` is the exact answer for the prefix `bba`. Frequency counting is a
streaming algorithm by nature, which is what makes *First Unique Character in a
Stream* and *Suffix Maximum Frequency Queries* tractable: you never start over,
you only decide what to keep alongside the counts.

**The bucket array is mostly empty, and that is fine but not free.** Six of its
nine slots hold nothing, and the walk still visits them. For a 200,000-character
string over 62 distinct characters — the actual shape of *Sort Characters by
Frequency* — the walk visits 200,001 slots to find 62 keys. Hold that thought; it
comes back in the cost section as a reason to sort instead.

**The tie-break is not in the counter.** `b` and `c` both have count 3, and the
counter has no opinion about which comes first; the order comes from a *second*
key applied inside the bucket. That separation is why *Most Frequent Integer with
Smaller Tie-Break* and *Top K Frequent Elements with Larger-Value Tie Break* are
the same problem with one character changed, and why almost every bug here is a
tie-break bug rather than a counting bug.

**The input is gone.** From `{b:3, a:2, c:3}` you cannot recover `bbacccab`, or
even which character came first. The counter has deliberately thrown order away.
If the problem needs it back you must keep it separately — which is the whole
design of the frequency stack later in this chapter.

## Why it is correct

Two claims: that the counting loop computes the frequency function, and that the
bucket walk emits the keys in the required order. The second is where the content
is.

:::proof The counting pass and the bucket walk
**Setup.** Let `s = s₀ … s_{n-1}` be the input and `key` a total, deterministic
function from items to a set `K` on which equality is decidable. For
`0 ≤ t ≤ n` and `k ∈ K` define the prefix count

    cₜ(k) = |{ i : 0 ≤ i < t and key(sᵢ) = k }|.

The frequency function we want is `c_n`.

**Part 1 — the counting loop.**

*Invariant.* Before the iteration that processes `s_t`, the map `C` satisfies:
for every `k`, `k ∈ C` and `C[k] = cₜ(k)` if `cₜ(k) > 0`, and `k ∉ C` otherwise.

*Base case.* `t = 0`: `C` is empty and `c₀(k) = 0` for every `k`, since the index
set is empty. Both halves hold vacuously.

*Inductive step.* Assume the invariant before `s_t`. Let `k* = key(s_t)`. The
body performs `C[k*] = C.get(k*, 0) + 1`. For `k*`: the index set of `c_{t+1}(k*)`
is that of `cₜ(k*)` plus the single index `t`, so `c_{t+1}(k*) = cₜ(k*) + 1`; and
`C.get(k*, 0)` equals `cₜ(k*)` by the invariant (whether or not `k*` was present,
the two halves agree that the retrieved value is `cₜ(k*)`). So the new `C[k*]` is
`c_{t+1}(k*)`, and it is at least 1, so membership is correct. For any `k ≠ k*`:
index `t` does not belong to `k`'s set, so `c_{t+1}(k) = cₜ(k)`, and `C[k]` was
not touched. Invariant restored.

*Termination.* The loop runs over a finite sequence and performs exactly `n`
iterations. On exit `t = n`, so `C = c_n` restricted to the keys with positive
count. ∎ (Part 1)

**Part 2 — the bucket walk.** Let `K' = { k : c_n(k) > 0 }`, the keys present.
Every `k ∈ K'` satisfies `1 ≤ c_n(k) ≤ n`, the upper bound because the counted
index sets are subsets of `{0, …, n-1}`.

Define `B[f] = { k ∈ K' : c_n(k) = f }` for `f = 1 … n`. Because `c_n` is a
*function*, each `k ∈ K'` lies in exactly one `B[f]` — namely `f = c_n(k)`. So
the `B[f]` are pairwise disjoint and their union is `K'`: they are a partition.

The walk visits `f = n, n-1, …, 1` and emits `sorted(B[f])` under the tie-break
order `≺`, assumed to be a total order on `K`. Since the `B[f]` partition `K'`,
every key of `K'` is emitted exactly once and no other key is emitted.

Now take any two keys `k, k'` with `k` emitted before `k'`. Either they came from
different buckets, in which case `k` came from the bucket visited earlier, so
`c_n(k) > c_n(k')`; or they came from the same bucket, in which case
`c_n(k) = c_n(k')` and `k ≺ k'` because the bucket was emitted in sorted order.
That is precisely the specification "descending by count, ties ascending by `≺`".

*Termination.* The outer loop runs `n` times; the inner loops run
`Σ_f |B[f]| = |K'|` times in total. ∎
:::

Now say what that argument leaned on; every item is a bug someone has shipped.

- **`key` is a genuine function: total, deterministic, consistent with equality.**
  The inductive step used `key(s_t)` as one well-defined value. A mutable object
  as a key, or a hash that can disagree with `==`, silently splits one key into
  two and the invariant is false from that moment. See [[hash-tables]] and
  [[hash-functions]].
- **Each item contributes exactly one key.** The step `c_{t+1}(k*) = cₜ(k*) + 1`
  assumed one increment per item. Problems where an item contributes many — *Most
  Common Product Pair*, where a transaction of `m` products contributes `m(m-1)/2`
  pairs, or *Most Common N-Grams* — still work, but `n` in "counts lie in `1 … n`"
  now means the number of *contributions*. Size the bucket array from that.
- **Counts are integers in `1 … n`.** The only thing that makes the bucket array
  possible. Weighted counting, where an item contributes `w` rather than 1, breaks
  it and sends you back to sorting or a [[heap]].
- **`≺` is a total order.** "Ties by the smaller value" is one; "ties by whichever
  appeared first" is one only if you actually stored first-appearance indices. If
  the spec leaves ties unspecified, say so rather than guess.
- **The desired order is descending by count.** Nothing else in the proof cares.
  *Sort Error Codes by Frequency* wants *ascending* frequency: walk the buckets
  upward and the same proof goes through with the inequality flipped.

:::note The corollary that tells you when to stop
Part 1 proves `c_n(k) = |{i : key(sᵢ) = k}|`, and the cardinality of a set does
not change when you relabel its elements. So if `σ` is any permutation of
`0 … n-1` and `s'ᵢ = s_{σ(i)}`, then `c_n` is identical for `s` and `s'`.

Therefore **any algorithm whose entire state is the count map cannot distinguish
two inputs that are permutations of each other.** If a problem's answer *does*
differ between two such inputs, no cleverness with counters will solve it and you
must store something beside the counts. That is an impossibility argument, not a
heuristic, and it is why *Maximum Frequency Stack* needs a stack per frequency and
why an LFU cache needs a recency order inside each frequency class.
:::

## What it costs

**The counting pass.** `n` iterations. Each does one key computation, costing
`κ`, and one dictionary read-modify-write, costing expected `O(1)` amortised over
resizes ([[hash-tables]]). So the pass is expected `Θ(n·(κ + 1))`.

The `κ` is the part people drop, and it is often dominant. Hashing a string of
length `ℓ` is `Θ(ℓ)`, not `Θ(1)`; CPython caches a string's hash after the first
computation, but a freshly built tuple key is hashed from scratch every time. Two
consequences:

*Group Anagrams, key choice.* With `w` words of total length `L`, the
sorted-string key costs `Σᵢ ℓᵢ log ℓᵢ` comparisons; the 26-slot count-tuple key
costs `Θ(L)` to build plus `Θ(26)` to hash per word, so `Θ(L + 26w)`. Per word of
average length `ℓ = L/w` that is `ℓ log ℓ` against `ℓ + 26`, and the crossover
sits near `ℓ log₂ ℓ = 26`, around nine characters. Constants move the number; the
shape is the lesson. For short words the "slow" sorted key is genuinely faster,
and "always use the 26-tuple, it's O(L)" ignores a constant of 26.

*Most Common N-Grams.* An `n`-gram key is a tuple of `n` tokens, so building and
hashing every window costs `Θ(n)` each, `Θ(n·(T - n + 1))` in total for `T`
tokens. That is why the statement caps the sum of `n·(T - n + 1)` over the
requested lengths at 10⁶ — the constraint is the cost model written down. A
[[rolling-hash]] removes the `n` factor if you need it to.

**Space.** `Θ(d)` where `d` is the number of distinct keys, `d ≤ min(n, |K|)`.
For lowercase letters `d ≤ 26` whatever `n` is; for arbitrary strings `d` can be
`n`. In the n-gram case each key also *stores* `n` tokens, so memory is `Θ(d·n)`.
Counting is cheap in time and can still be the thing that exhausts memory.

**Getting frequency order out.** Three ways, and the comparison is not a formality.

| method | cost | notes |
| --- | --- | --- |
| sort the items | `Θ(d log d)` | ties free, via a compound key |
| heap of size `k` | `Θ(d log k)` | streaming-friendly, [[heap]] |
| bucket by count | `Θ(n + d)` | ties need an inner sort |

The bucket walk is `Θ(n + d)`, not `Θ(n·d)`, by a counting argument: the outer
loop makes `n + 1` constant-time visits, and the inner loops emit each of the `d`
keys exactly once because the buckets partition the key set. Summed over all
buckets the inner work is `d`, not `d` per bucket.

Now compare honestly. Buckets beat sorting only when `n + d < d log d`. With
`d = 62` distinct characters and `n = 200,000`, sorting costs about
`62 · 6 ≈ 370` comparisons while the bucket walk takes 200,001 steps — the
"linear" algorithm doing five hundred times the work. Buckets win when `d` is
close to `n`, which holds for *Top K Frequent Elements* on arbitrary integers and
not for *Sort Characters by Frequency*. The textbook answer and the fast answer
point in opposite directions, and the only way to tell is to write `n` and `d`
down separately.

**The amortised piece.** A counter over a [[sliding-window]] does up to two
dictionary operations per position — an insert on entry, a decrement or delete on
exit. Each element enters once and leaves at most once, so the whole scan is at
most `2n` operations, `Θ(n)` overall. *Query Type Frequency Window*, with its
600-second window over 2·10⁵ logs, is exactly this.

## The implementation

```python run
import random
from collections import Counter, defaultdict


def frequencies(seq, key=lambda x: x):
    """count[k] = number of items x in seq with key(x) == k."""
    count = defaultdict(int)
    for x in seq:
        count[key(x)] += 1
    return dict(count)


def sort_by_frequency(s):
    """Higher count first; ties by smaller character. Via bucket inversion."""
    count = frequencies(s)
    n = len(s)
    bucket = [[] for _ in range(n + 1)]          # counts live in 1..n
    for ch, f in count.items():
        bucket[f].append(ch)
    out = []
    for f in range(n, 0, -1):                    # descending count
        for ch in sorted(bucket[f]):             # the tie-break, inside a bucket
            out.append(ch * f)
    return "".join(out)


def reference(s):
    """The same spec, stated as one compound sort key."""
    c = Counter(s)
    return "".join(ch * f for ch, f in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))


s = "bbacccab"
print("input   ", s)
print("counts  ", frequencies(s))
print("buckets ", {f: sorted(ks) for f, ks in
                   ((f, [k for k, v in frequencies(s).items() if v == f]) for f in (2, 3))})
print("result  ", sort_by_frequency(s))
assert sort_by_frequency(s) == "bbbcccaa"

rng = random.Random(3)
for _ in range(500):
    t = "".join(rng.choice("abcdeAB9") for _ in range(rng.randint(0, 30)))
    got = sort_by_frequency(t)
    assert got == reference(t), (t, got)
    assert Counter(got) == Counter(t)            # same multiset, only reordered
print("500 random strings: buckets agree with the compound-key sort, multiset preserved")
```

Three lines carry the weight.

`count[key(x)] += 1` on a `defaultdict(int)` is the whole counting pass. Write it
this way, or as `count[k] = count.get(k, 0) + 1`, and never as
`if k in count: ... else: ...` — the two-branch version is where people forget to
initialise to 1 rather than 0. `Counter(seq)` does the same in C and is right when
the key is the item itself; `frequencies` earns its keep the moment the key is a
function, which is most of the time.

`bucket = [[] for _ in range(n + 1)]` is sized `n + 1`. The maximum possible count
is `n` — the whole input one repeated key — so `bucket[n]` must exist. A bucket
array of size `n` passes every sample test and raises `IndexError` on `"aaaa"`.

`for ch in sorted(bucket[f])` is the tie-break, deliberately kept a separate
expression from the counting. Change the spec to "ties by larger value" and you
change `sorted(...)` to `sorted(..., reverse=True)` and nothing else; fold the
tie-break into the counting loop and a one-word spec change becomes a rewrite.
See [[custom-comparators]].

## Variants you will meet

**Direct-address counting.** When the key domain is small and known, drop the
hash map for a list: `[0] * 26`, or `[0] * 65536` as *Fixed-Range Frequency Count*
instructs. No hashing, perfect cache behaviour, and iteration in key order for
free — [[counting-sort]] without the sort.

**Grouping.** `group[k].append(item)` instead of a tally. *Group Anagrams* (three
companies here) keys on a canonical form; *Goto Largest Bucket* keys on a bucket
name with a `set` of filenames as payload, so repeated creates collapse. See
[[anagrams]].

**Bucketing by arithmetic.** The label is computed, and clamped when the last
bucket overflows: `min(v // width, numOfBuckets - 1)` is *Latency Bucket Counter*
in one expression.

**Bucket by count.** The inversion in this chapter. *Top K Frequent Elements* and
*Stable Top K Frequent Words* are its home ground.

**Counting the counts.** Sometimes the interesting object is the histogram of the
histogram. *Frequency Equals Card Value* asks whether `count[x] == x` for some `x`
— a key compared against its own count. An LFU cache tracks how many keys have
frequency `f`, so it can find the minimum frequency in `O(1)`.

**Counter over a window.** Add on entry, subtract on exit, and *delete the key
when it reaches zero* if you also care about the number of distinct keys. *Query
Type Frequency Window* asks whether any 600-second window holds a type at least
`threshold` times. See [[sliding-window]].

**Counter as a signature.** Two strings are anagrams iff their counters are
equal; *String-Pair Frequency Similarity* relaxes that to "counts differ by at
most 3 per letter" — the same comparison with a tolerance. *Check Anagrams Without
Sorting* names the technique.

**Cumulative counts for sampling.** *Frequency-Weighted Next-Word Sampling* gives
each successor tickets equal to its frequency: prefix-sum the counts and
[[binary-search]] for the ticket. See [[prefix-sums]].

**Streaming.** *Streaming Top-K Frequent Elements* keeps the counter live and the
top `k` incremental with a [[heap]]. When the key space is too large to store
exactly, sketches replace exactness: [[streaming]], [[bloom-filter]].

**The frequency stack.** *Maximum Frequency Stack* (two companies here) is the
variant that demonstrates the corollary. Pops return the most frequent value,
ties by most recent — and recency is not a function of the counts. The fix is to
bucket by count and make each bucket a *stack*, so recency survives inside the
frequency class. The same idea with a recency-ordered structure per frequency is
an LFU cache ([[lru-cache]], [[design-data-structure]]).

```python run
import random
from collections import defaultdict


class FreqStack:
    """push(x); pop() removes the most frequent value, ties by most recent."""

    def __init__(self):
        self.count = defaultdict(int)     # value -> its current frequency
        self.group = defaultdict(list)    # frequency f -> stack of values that reached f
        self.maxfreq = 0

    def push(self, x):
        self.count[x] += 1
        f = self.count[x]
        self.group[f].append(x)           # x is recorded at EVERY level it passes
        if f > self.maxfreq:
            self.maxfreq = f

    def pop(self):
        x = self.group[self.maxfreq].pop()
        self.count[x] -= 1
        if not self.group[self.maxfreq]:
            self.maxfreq -= 1
        return x


def brute_pop(stack):
    """Same spec, done the slow honest way over a plain list of pushes."""
    cnt = {}
    for v in stack:
        cnt[v] = cnt.get(v, 0) + 1
    best = max(cnt.values())
    for i in range(len(stack) - 1, -1, -1):       # scan from the top
        if cnt[stack[i]] == best:
            return stack.pop(i)


fs, hist = FreqStack(), []
for x in [5, 7, 5, 7, 4, 5]:
    fs.push(x)
    hist.append(x)
print("pushed 5 7 5 7 4 5 -> counts", dict(fs.count), "levels", dict(fs.group))
got = [fs.pop() for _ in range(4)]
print("four pops:", got)
assert got == [5, 7, 5, 4]

rng = random.Random(17)
for _ in range(300):
    a, b, live = FreqStack(), [], []
    for _ in range(60):
        if live and rng.random() < 0.4:
            assert a.pop() == brute_pop(b), (live,)
            live.pop()
        else:
            v = rng.randrange(4)
            a.push(v)
            b.append(v)
            live.append(v)
print("300 random push/pop sequences agree with the brute-force definition")
```

The surprising line is `self.group[f].append(x)`: a value pushed three times
appears in the level-1, level-2 *and* level-3 stacks. That redundancy is the
point. When a pop knocks `x` back down from frequency 3 to 2, its level-2 entry is
already sitting there, in the right position relative to everything else that ever
reached level 2. Nothing has to be repaired.

<svg viewBox="0 0 560 230" role="img" aria-label="three stacks, one per frequency level, with a pointer at the highest occupied level">
  <g>
    <text x="30" y="30">f = 1</text>
    <text x="180" y="30">f = 2</text>
    <text x="330" y="30">f = 3</text>
    <rect x="20" y="150" width="80" height="34" rx="4"/>
    <text x="52" y="173">5</text>
    <rect x="20" y="116" width="80" height="34" rx="4"/>
    <text x="52" y="139">7</text>
    <rect x="20" y="82" width="80" height="34" rx="4"/>
    <text x="52" y="105">4</text>
    <rect x="170" y="150" width="80" height="34" rx="4"/>
    <text x="202" y="173">5</text>
    <rect x="170" y="116" width="80" height="34" rx="4"/>
    <text x="202" y="139">7</text>
    <rect class="fill" x="320" y="150" width="80" height="34" rx="4"/>
    <text x="352" y="173">5</text>
    <line x1="360" y1="128" x2="360" y2="146"/>
    <text x="410" y="124">maxfreq: pop here</text>
    <text x="20" y="215">every push writes one box, at its own new level</text>
  </g>
</svg>

## Recognising it in a statement

In descending order of how much you should trust the signal.

1. **"How many times does each X appear", "frequency of", "most common", "top k
   frequent".** Direct statements of the technique: *Word Frequency in a Large
   Text*, *Get Max Occurrences*, *Top Ten Most Frequent Words in a Book*.
2. **The permutation test passes.** Shuffle the input; if the answer is unchanged,
   it is a function of the counts. Reach for this when the statement is dressed
   up — *Most Common Three-Website Sequences* barely says "frequency", but a
   sequence's score is the number of distinct customers producing it, which is a
   count over a canonical key.
3. **"Group the X by Y", "histogram", "distribution", "anagram".** Grouping or
   bucketing. Give the key a name before you write anything.
4. **A tie-break clause on a frequency.** A statement needs that clause only if
   frequencies are being compared, so its presence is close to an admission.
   *Most Frequent Integer with Smaller Tie-Break* and *Top K Frequent Elements
   with Larger-Value Tie Break* differ only there.
5. **A small, explicitly stated key domain.** "values[i] < 65536", "only lowercase
   English letters", "there are only three possible commands" (*Command Frequency
   Counter*) — an invitation to use an array instead of a map.
6. **"Exactly once", "non-repeating", "duplicate", "distinct".** Count, then
   filter on the count. *First Non-Repeating Character*, *Count Values Appearing
   Exactly Once*, *First Unique Log Entry*.

The anti-signals:

- **"Contiguous", "subarray", "window", "consecutive".** Position matters, so the
  counter is at best a component. *Max Frequency Substring* counts substrings, but
  the length and unique-character limits make it a [[sliding-window]] enumeration
  whose inner bookkeeping happens to be a counter.
- **"Bucket" used for capacity rather than classification.** Token buckets are
  [[rate-limiting]].
- **"K-th largest value"** — [[quickselect]] or a [[heap]] on values, not on
  counts. Check whether "largest" ranks values or frequencies.
- **Recency or arrival order in the tie-break.** You need the counter *and*
  something order-aware: *Maximum Frequency Stack*, LFU caches.
- **The answer is an index.** Counts cannot produce one; plan the second pass.

## Traps

**Reversing the whole sort key instead of just the count.**
`sorted(keys, key=lambda k: (c[k], k), reverse=True)` reverses *both* components,
so ties come out descending when the spec almost always asks for ascending. The
symptom is maddening: counts right, grouping right, only the tied entries in the
wrong order — which a sample test without ties never catches. Demonstrated below.

**Trusting insertion order as a tie-break.** Python dicts preserve insertion
order, so `sorted(c, key=c.get, reverse=True)` breaks ties by first appearance.
Sometimes that is the spec — *Most Common N-Grams* wants the earliest first
occurrence — and then you should *say* so with an explicit index key rather than
lean on a language guarantee that does not exist elsewhere.

**Reading a `defaultdict` to test membership.** `if d[k] > 0` inserts `k` with
value 0. Symptom: `len(d)` grows during a read-only loop, the distinct-key count
is too large, and memory climbs on a long stream. `Counter` does not do this; its
`__missing__` returns 0 without storing. Demonstrated below.

**Forgetting to delete a key when its count hits zero.** In a window counter,
`c[k] -= 1` leaving `c[k] == 0` means `len(c)` counts keys no longer in the
window. Symptom: "at most `k` distinct" fires late and the window never shrinks.

**Sizing the bucket array `n` instead of `n + 1`.** `IndexError`, and only when
one key occupies the entire input.

**Not canonicalising the key.** *Most Common Product Pair* says `(A, B)` and
`(B, A)` are the same pair, and duplicates inside a transaction count once:
`tuple(sorted(pair))` for the first, `set(t)` before enumerating for the second.
Symptom: counts roughly double and the answer depends on listing order.

**Unhashable or mutable keys.** A list key raises `TypeError`; a key built from an
object that mutates afterwards corrupts the map silently. Tuples and strings.

```python run
from collections import Counter, defaultdict

s = "bbacccab"
c = Counter(s)                                   # {b: 3, a: 2, c: 3}
wrong = sorted(c, key=lambda k: (c[k], k), reverse=True)
right = sorted(c, key=lambda k: (-c[k], k))
print("counts        ", dict(c))
print("reverse=True  ", wrong, "<- ties descending: c before b")
print("negate count  ", right, "<- ties ascending: b before c, as specified")
assert wrong == ["c", "b", "a"] and right == ["b", "c", "a"]

d = defaultdict(int)
for ch in "aab":
    d[ch] += 1
present_d = [k for k in "abcd" if d[k] > 0]      # each miss INSERTS a zero
cnt = Counter("aab")
present_c = [k for k in "abcd" if cnt[k] > 0]    # Counter.__missing__ stores nothing
print("after probing a,b,c,d -> defaultdict holds", sorted(d), "Counter holds", sorted(cnt))
assert present_d == present_c == ["a", "b"]
assert len(d) == 4 and len(cnt) == 2

n = 4
small = [[] for _ in range(n)]                   # one short
try:
    small[Counter("aaaa")["a"]].append("a")
    raise SystemExit("unreachable")
except IndexError as e:
    print("bucket array of size n on 'aaaa' ->", type(e).__name__)
print("all three traps reproduced")
```

The first block is the important one. Both sorts are one line, both look
reasonable, both put the most frequent first, and only one matches a spec that
names a tie-break. Negate the count inside the key rather than reversing the sort.

## What to memorise

Very little. One loop, one inversion, one sentence, one habit.

**The loop**, which should need no thought:

```python
count = defaultdict(int)
for x in seq:
    count[key(x)] += 1
```

**The inversion**, for when the question is about frequency order:

```python
bucket = [[] for _ in range(n + 1)]        # counts live in 1..n
for k, f in count.items():
    bucket[f].append(k)
for f in range(n, 0, -1):                  # or range(1, n + 1) for ascending
    for k in sorted(bucket[f]):            # tie-break lives here, alone
        ...
```

**The sentence**: *"If I shuffled the input, would the answer change?"* No means
the answer is a function of the counts. Yes means you need the counts plus
something order-aware, and you should work out what before writing a line.

**The habit**: name the key function and the tie-break key, out loud, before the
loop. "The key is the word with its letters sorted. The tie-break is ascending
ASCII." Almost every bug here is one of those two sentences being wrong or never
spoken, not a mistake in the counting.

Numbers worth carrying: counts lie in `1 … n`, so they index an array of size
`n + 1`. Distinct keys `d ≤ min(n, |domain|)`. Bucket walk `Θ(n + d)`, sort
`Θ(d log d)`, heap-of-`k` `Θ(d log k)` — and when `d ≪ n` the sort wins despite
being asymptotically worse.

## Check yourself

:::check
*Sort Characters by Frequency* allows strings of up to 200,000 characters over an
alphabet of 62 symbols. The bucket walk is `Θ(n + d)` and the sort is
`Θ(d log d)`. Which should you write, and why is the asymptotically better
algorithm the wrong choice here?
--
Write the sort. Here `d ≤ 62` and `n = 200,000`, so the sort costs about
`62 · log₂ 62 ≈ 370` comparisons while the bucket walk visits 200,001 slots and
allocates a 200,001-element list to do it.

The asymptotics are not lying; they answer a different question. `Θ(n + d)` beats
`Θ(d log d)` only when `n + d < d log d`, which needs `d` to grow with `n`. That
happens for *Top K Frequent Elements* on arbitrary integers, where `d` can reach
`n`. It never happens over a fixed 62-symbol alphabet, where `d` is capped by a
constant. The habit worth keeping is to write `n` and `d` down separately instead
of calling both "the input size".
:::

:::check
Why does *Maximum Frequency Stack* need a stack per frequency level, rather than a
counter plus "the most recent value with the maximum count"? Tie the answer to
something proved earlier in this chapter.
--
Because the required answer is not a function of the counts, and the corollary to
Part 1 says a count map therefore cannot produce it. `c_n` is invariant under
permuting the input, so `push 5, push 7` and `push 7, push 5` give identical
counters — yet the spec says the first must pop 7 and the second must pop 5. No
algorithm whose state is the counter alone can distinguish them.

So recency must be stored, and the question is *where*. One global recency order
does not work either, because a pop changes a value's frequency and therefore
which class it competes in. A stack per frequency level does work: a value pushed
to level `f` sits in that level's stack in arrival order relative to every other
value that ever reached level `f`, which is exactly the comparison a pop at level
`f` makes. When `maxfreq` drops by one, the level below is already correct.
:::

:::check
A colleague writes `sorted(counts, key=lambda k: (counts[k], k), reverse=True)`
and says it sorts by descending frequency with ties broken by the smaller key,
"because Python's sort is stable and `reverse=True` preserves stability". Where
are they wrong?
--
The claim about stability is true and irrelevant. `reverse=True` really does
preserve the relative order of items that compare *equal* — but `(counts[k], k)`
is a compound key, so two entries with the same count are **not** equal; they
differ in the second component. Stability never comes into play. The comparison
itself orders them, and `reverse=True` reverses the whole comparison, second
component included, giving ties in *descending* key order.

The fix is to reverse only the component you mean to reverse, by negating it:
`key=lambda k: (-counts[k], k)`. When the primary key is non-numeric and negation
is unavailable, sort twice — ascending by the tie-break, then stably by the
primary — and *then* stability is doing real work.
:::

:::check
You are counting pairs for *Most Common Product Pair*: each transaction is a list
of products, every unordered pair within a transaction counts once, and duplicate
products inside a transaction count only once. Someone builds the key as
`(a, b)` in the order the products appear. Name the two independent bugs and say
what each one's symptom looks like.
--
**Bug 1: the key is not canonical.** `("A", "B")` and `("B", "A")` are different
tuples, so one real pair occupies two pigeonholes, each holding part of the true
count. Symptom: the reported count is too low and the winner is wrong whenever the
true winner appears in both orders. Fix: `tuple(sorted((a, b)))` — which is also
the required output format, since the spec asks for lexicographic order.

**Bug 2: duplicates within a transaction survive.** A transaction listing `A`
twice produces `(A, B)` twice, and produces the self-pair `(A, A)` that the spec
forbids. Symptom: inflated counts that depend on how the input happens to list
products. Fix: enumerate over `sorted(set(transaction))`.

They are independent — fixing the ordering does nothing about duplicates. This is
the proof's "each item contributes exactly one key" assumption being violated:
here a transaction of `m` products contributes `m(m-1)/2` keys, and the counting
is correct only once that set of keys is exactly right.
:::

:::check
*First Non-Repeating Character* asks for the first character of a string that
appears exactly once. The standard solution counts, then scans the string again.
Why must the second pass go over the string rather than over the counter — and
what changes when the input is a stream, as in *First Unique Character in a
Stream*?
--
Because the counter has thrown order away. The proof's corollary makes this
precise: `c_n` is unchanged by permuting the input and "first" is not, so no
function of the counter alone can return it. The original sequence is the only
place where "first" lives.

In CPython a dict iterates in insertion order, which here is first-occurrence
order, so iterating the counter happens to work. That is a language guarantee,
not an algorithmic one; it evaporates elsewhere and in any path that rebuilds the
map. Scan the string.

For a stream you cannot rescan, so you keep order explicitly: a queue of
candidates in arrival order beside the counter. On arrival, increment and append;
to answer a query, pop from the front while the front's count exceeds 1 and report
what is left. Each element is appended once and popped once, so the amortised cost
per event is `O(1)` even though one query may discard many candidates — the same
counting argument as the sliding-window counter.
:::
