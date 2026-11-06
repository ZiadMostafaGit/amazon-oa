# Monotonic Stack

> A monotonic stack works because the moment a bigger element arrives, every smaller element waiting behind it has its answer and can be thrown away for good, so each element enters once and leaves once, and n "nearest bigger" questions cost about 2n steps instead of n^2.

## The problem it solves

You are given a row of daily temperatures:

| day | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| temp | 73 | 74 | 75 | 71 | 69 | 72 | 76 | 73 |

For every day, how many days do you wait until a strictly warmer day? Day 0 (73)
waits 1 day for 74. Day 2 (75) waits 4 days, past 71, 69 and 72, for 76. Day 6
(76) never gets a warmer day, so its answer is 0. The full answer is
[1, 1, 4, 2, 1, 1, 0, 0]. That is [[p:ebay-daily-temperatures|Daily Temperatures]],
and it is the same question as [[p:amazon-next-greater-element-to-right|Next Greater Element to the Right]],
which asks for the warmer value itself instead of the distance to it.

Every problem in this chapter is, underneath, this one question: **for each
position, where is the nearest position on one side whose value beats mine?**
"Beats" can mean greater, smaller, greater-or-equal or smaller-or-equal. "One
side" can be left or right. The answer can be the value, the index, or the
distance.

The first solution anyone writes is the honest one. For each day, walk to the
right until you find a warmer day.

```
for i in 0..n-1:
    for j in i+1..n-1:
        if temp[j] > temp[i]: answer[i] = j - i; break
```

It is correct. It is also quadratic in the bad case. Take a strictly decreasing
row, [100, 99, 98, ..., 1]. Nobody ever finds a warmer day, so every scan runs to
the end: n-1 steps, then n-2, then n-3, a total of n(n-1)/2. The bank's version
of this problem allows 10^5 days. That is about 5 * 10^9 comparisons, which is far
beyond any time limit, and in Python it would take more than an hour.

What this chapter builds does the same job in at most about 3n simple steps, for
any input. It is a plain [[stack]] used with one discipline: the values on it
are always sorted. The sorting is not something you do. It is something that
happens by itself, once you throw away what can never be an answer again.

### When it is the wrong tool

The monotonic stack answers "nearest beater on one side". It is not a general
range-query structure.

- **Arbitrary ranges.** "What is the maximum of a[l..r]?" for many unrelated
  (l, r) pairs is a [[sparse-table]] or a [[segment-tree]] question. A stack
  only answers questions whose boundary is "the nearest one that beats me".
- **A window that slides.** "The maximum of every window of size k" looks
  similar, but old elements must also leave from the *bottom* when they fall
  out of the window. That needs removal at both ends: a [[monotonic-deque]].
- **"Next greater" by value, not by position.** "The smallest value in the array
  that is bigger than mine" ignores where things are. Sort, or use a sorted
  structure. The stack is about the nearest *position*.
- **Titles that lie.** In this bank, *Next Greater Element III* and *Next Greater
  Numerically Balanced Number* say "next greater", but they ask for the next
  larger number made from digits. Those are next-permutation and enumeration
  problems. Nothing in them is a nearest-beater query.
- **Everything to the right, not the nearest.** "Is my building taller than
  every building to its right?" needs only the maximum of the suffix, a single
  number kept from right to left. A stack would work but is overkill.

Twenty-nine problems in this bank are tagged monotonic stack, and many more hide
it: stock spans, histograms, discounts, "sum over all subarrays of the minimum",
"remove k digits to make the smallest number". The sections below name them where
they teach something.

## Build it from the brute force

We will not start with the stack. We start with the double loop, count it, find
the waste, and the stack will appear as the obvious way to stop wasting.

### Step 1: the honest double loop

For position i, scan j = i+1, i+2, ... and stop at the first a[j] > a[i]. Here
it is on a row designed to be bad for it, [6, 5, 4, 3, 2, 1, 7]:

| i | value | scanned | answer |
|---|---|---|---|
| 0 | 6 | 5, 4, 3, 2, 1, 7 | 7 |
| 1 | 5 | 4, 3, 2, 1, 7 | 7 |
| 2 | 4 | 3, 2, 1, 7 | 7 |
| 3 | 3 | 2, 1, 7 | 7 |
| 4 | 2 | 1, 7 | 7 |
| 5 | 1 | 7 | 7 |
| 6 | 7 | (nothing) | -1 |

### Step 2: count it

The scans have lengths 6, 5, 4, 3, 2, 1, 0: 21 comparisons for 7 elements. In
general n(n-1)/2. Each element walks over every element after it until a winner
appears, and in a falling row the winner appears late.

### Step 3: notice the waste

Look at the table column "scanned". The number 7 was discovered six separate
times, once per scan. Each scan walked over the same falling run 5, 4, 3, 2, 1,
asked each of them "are you bigger than me?", heard "no", and moved on. The
answers to those questions never changed between scans. We kept asking them
because each scan starts from scratch.

Turn the question around. Instead of each element going out to look for its
answer, let each new element arrive and ask: **who was I the answer for?** When 7
arrives at position 6, it is the first bigger element for everyone in 6, 5, 4, 3,
2, 1 at once, because each of them has been waiting with no answer so far and 7 is
bigger than all of them. One arrival settles six questions.

So keep a **waiting room**: the earlier positions that do not have their answer
yet. When a new element x arrives, every waiting element smaller than x gets x as
its answer and leaves the room. Then x itself sits down to wait.

Why is x really the *first* bigger element for each of them, and not just *a*
bigger one? Because they were still waiting. If anything between them and x had
been bigger, that element would have answered them when it arrived, and they
would have left the room then. Still being in the room means "nothing bigger has
come yet". So the first bigger thing to come is x.

### The question that unlocks it

That is the whole technique, but it has a second half that makes it fast. Ask it
in bold, because it is the question for every problem in this family:

**When a new element arrives, which old elements does it make useless forever?**

Here the answer is: every waiting element smaller than the newcomer. They have
their answer, nothing later can change it, so they are done. Throwing them away is
not an approximation. They will never be looked at again by anyone.

Say it a second way. A waiting element is a question that has not been answered.
An arriving element is a candidate answer. The room only ever holds open
questions, and each question is closed exactly once.

### Step 4: what does the waiting room look like?

Here is the observation that turns the room into a stack. **The waiting room is
always sorted: from oldest to newest, the values never go up.**

Why? Suppose two elements were both waiting, an older a and a newer b, with a < b.
When b arrived, it was bigger than a, and a was waiting. So b answered a, and a
left. Contradiction. So among waiting elements, every newer one is less than or
equal to every older one. The room is a falling (non-increasing) staircase.

Now look at what an arrival x does to a falling staircase. The elements smaller
than x are exactly the newest ones, a run at the end. As soon as you meet a
waiting element that is at least x, every older one is at least that, so at least
x too, and none of them is answered. So you only ever remove from the newest end,
and you stop at the first one that survives.

Removing from the newest end and adding at the newest end: that is a stack. The
newest waiting element is the top.

Here is the moment day 5 (72) arrives in the temperature example. Days 0 and 1
left long ago (74 answered 73, 75 answered 74). The room holds days 2, 3, 4, with
75, 71, 69, a falling staircase.

<svg viewBox="0 0 560 300" role="img" aria-label="bars for the temperatures 73, 74, 75, 71, 69 on days 0 to 4 and the arriving 72 on day 5; days 0 and 1 are dashed because they already left the stack; the stack holds 75, 71, 69 as a falling staircase; 69 and 71 are shaded because 72 pops them, giving answers of 1 day and 2 days; 75 stays because it is not smaller than 72">
  <g>
    <line x1="20" y1="230" x2="540" y2="230"/>
    <rect x="40" y="100" width="50" height="130" stroke-dasharray="5 4"/>
    <rect x="110" y="90" width="50" height="140" stroke-dasharray="5 4"/>
    <rect x="180" y="80" width="50" height="150"/>
    <rect class="fill" x="250" y="120" width="50" height="110"/>
    <rect class="fill" x="320" y="140" width="50" height="90"/>
    <rect x="410" y="110" width="50" height="120" stroke-width="3"/>
    <text x="65" y="94" text-anchor="middle">73</text>
    <text x="135" y="84" text-anchor="middle">74</text>
    <text x="205" y="74" text-anchor="middle">75</text>
    <text x="275" y="114" text-anchor="middle">71</text>
    <text x="345" y="134" text-anchor="middle">69</text>
    <text x="435" y="104" text-anchor="middle">72</text>
    <text x="65" y="250" text-anchor="middle">day 0</text>
    <text x="135" y="250" text-anchor="middle">day 1</text>
    <text x="205" y="250" text-anchor="middle">day 2</text>
    <text x="275" y="250" text-anchor="middle">day 3</text>
    <text x="345" y="250" text-anchor="middle">day 4</text>
    <text x="435" y="250" text-anchor="middle">day 5</text>
    <line x1="405" y1="160" x2="375" y2="175"/>
    <line x1="405" y1="150" x2="305" y2="150"/>
    <text x="345" y="196" text-anchor="middle">wait 1</text>
    <text x="275" y="196" text-anchor="middle">wait 2</text>
    <text x="205" y="196" text-anchor="middle">stays</text>
    <text x="280" y="275" text-anchor="middle">dashed: already answered. Solid: the stack, bottom 75, top 69.</text>
    <text x="280" y="292" text-anchor="middle">72 pops the shaded bars (69, then 71), stops at 75, and is pushed.</text>
  </g>
</svg>

The picture is the whole algorithm. 72 looks at the top, 69: smaller, so 69's
answer is day 5, a wait of 5 - 4 = 1. Pop. The new top is 71: smaller, a wait of
5 - 3 = 2. Pop. The new top is 75: not smaller, stop, and nobody below 75 can be
smaller either, because the staircase falls. Push 72. The room is now 75, 72,
still falling.

### You might think: "The next greater element is the maximum to my right."

The maximum to the right is *a* greater element, often not the *first* one. Take
[3, 5, 9]. The maximum to the right of 3 is 9. The next greater element of 3 is
5, which comes first. Suffix maxima answer "is anything to my right bigger?" in
O(n), and that is a different question. The word "next" means nearest, and the
nearest beater is not the biggest one.

### You might think: "I only need to remember one candidate."

The instinct: scan from the right and keep only "the last bigger element I saw".
Try [3, 1, 4], scanning from the right. At 4, nothing is to the right: answer -1,
remember 4. At 1, the remembered 4 is bigger: answer 4. Now the nearest element is
1, so remember 1. At 3, the remembered 1 is not bigger. With one candidate, you
would answer -1. The true answer for 3 is 4, which you forgot.

The problem is that 1 is the nearest element but is too small to help 3, while 4
is farther but big enough. You must keep both: the near small one for the small
questions, the far big one for the big questions. In general you must keep a whole
chain of them, each farther one bigger than the nearer ones. That chain is the
stack, seen from the right-to-left side.

### You might think: "A while loop inside a for loop is O(n^2)."

The loop looks quadratic, so people distrust it. Count differently. Do not count
per arrival; count per element. Every index is pushed exactly once. Every pop
removes an index that was pushed, and a removed index never comes back. So there
are at most n pops over the *whole run*, no matter how they are spread out. In
[6, 5, 4, 3, 2, 1, 7], the first six arrivals pop nothing and the seventh pops six.
Total pops: 6, not 21. One arrival can pop a lot, but only because earlier
arrivals popped nothing. The work is n pushes, at most n pops, and one failed
comparison per arrival to end its loop: at most 3n.

### Step 5: store positions, not values

The waiting room must remember *where* each waiting element sits, because the
answer is often a distance (days to wait) or an index, and because the same value
can appear twice. So push the index i and read the value as a[i]. With indices, the
answer for a popped j is a[i] (the value), i (the index) or i - j (the distance),
whichever the problem asks for.

### The technique in one sentence

**Monotonic stack: scan once; keep the positions still waiting for their answer on
a stack, which stays sorted because a newcomer pops every waiting element it beats,
and each pop is the moment that element learns its nearest beater.**

And the question that produced it, worth asking on every new problem: **when a new
element arrives, which old elements does it make useless forever?**

## Worked by hand

Get a pen. Temperatures [73, 74, 75, 71, 69, 72, 76, 73], next strictly warmer day.
The stack is written bottom to top as day:temp. "Pops" lists each popped day and
the answer it receives.

| i | temp | pops (day gets answer) | stack after push |
|---|---|---|---|
| 0 | 73 | none, stack empty | 0:73 |
| 1 | 74 | day 0 (73 < 74): wait 1 | 1:74 |
| 2 | 75 | day 1 (74 < 75): wait 1 | 2:75 |
| 3 | 71 | none, 75 is not < 71 | 2:75, 3:71 |
| 4 | 69 | none, 71 is not < 69 | 2:75, 3:71, 4:69 |
| 5 | 72 | day 4 (69): wait 1; day 3 (71): wait 2; stop at 75 | 2:75, 5:72 |
| 6 | 76 | day 5 (72): wait 1; day 2 (75): wait 4 | 6:76 |
| 7 | 73 | none, 76 is not < 73 | 6:76, 7:73 |
| end | | days 6 and 7 never popped: 0 | |

Answer: [1, 1, 4, 2, 1, 1, 0, 0]. Check it against the statement: day 2 waits 4
days for 76, as we said at the start.

Read the row for i = 6 in words:

> "76 arrives on day 6. The top is day 5, temperature 72. Day 5 has been waiting
> for something warmer than 72, and 76 is warmer, and nothing between day 5 and
> day 6 could have answered it because there is nothing between them. So day 5
> waits 6 - 5 = 1 day. Pop it. The new top is day 2 at 75. It has been waiting
> since day 2, through 71, 69 and 72, none of which beat 75 (if one had, day 2
> would have left already). 76 beats it, so day 2 waits 6 - 2 = 4 days. Pop it.
> The stack is empty. Push day 6."

Three things the trace shows that the code alone would not:

1. **The stack falls from bottom to top in every row.** 75, 71, 69 is falling;
   75, 72 is falling. Nobody sorted it. Each push lands on something not smaller
   than itself, because everything smaller was just popped.
2. **Day 2's answer arrived four steps after day 2 was pushed.** It sat under
   71 and 69 and 72 the whole time. The stack let it wait without being looked at:
   days 3, 4 and 5 compared only against their own top, never against 75 except
   once each to stop.
3. **Total pops: 6. Total pushes: 8.** The two that remain at the end are the ones
   with no answer. Work is proportional to n, as the counting argument promised.

### A second trace: a tie

The bank's example for [[p:amazon-next-greater-element-to-right|Next Greater Element to the Right]]
is [2, 1, 2, 4, 3] with answer [4, 2, 4, -1, -1], and it has a trap: two 2s.
"Strictly greater" means the second 2 is *not* an answer for the first.

| i | value | pops | stack after push |
|---|---|---|---|
| 0 | 2 | none | 0:2 |
| 1 | 1 | none, 2 is not < 1 | 0:2, 1:1 |
| 2 | 2 | 1:1 (1 < 2), gets 2. Then top is 0:2: is 2 < 2? No. Stop | 0:2, 2:2 |
| 3 | 4 | 2:2 gets 4; 0:2 gets 4 | 3:4 |
| 4 | 3 | none, 4 is not < 3 | 3:4, 4:3 |

The cell to stare at is i = 2. The newcomer 2 meets the waiting 2 and does *not*
pop it, because 2 < 2 is false. So the stack ends that step as 2, 2: two equal
values, one on top of the other. The staircase is falling-or-flat, not strictly
falling. That flat step is what lets the first 2 keep waiting until 4 arrives, and
that is why its answer is 4, not 2.

If the comparison were `<=` instead of `<`, the second 2 would pop the first and
hand it the answer 2. That would be the answer to a different question, "next
greater *or equal*". The comparison operator is the one line of this technique
that decides which question you are answering. It gets its own demonstration in
the next section.

## From the idea to the code

### The direct version, against the brute force

The program below is the waiting room as code. It also counts the work of both
versions, and checks the stack against the double loop on many random arrays,
including ones with lots of repeated values.

```python run
import random

def brute(a):                       # the honest double loop
    steps, ans = 0, [-1] * len(a)
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            steps += 1
            if a[j] > a[i]:
                ans[i] = a[j]
                break
    return ans, steps

def next_greater(a):
    steps, ans = 0, [-1] * len(a)   # -1: still waiting at the end
    stack = []                      # indices still waiting, values falling
    for i, x in enumerate(a):
        while stack and a[stack[-1]] < x:   # x beats the top: the top is answered
            steps += 1
            ans[stack.pop()] = x
        steps += 1                  # the comparison that ended the loop, or none
        stack.append(i)             # x waits for its own answer
    return ans, steps

print("temps:", next_greater([73, 74, 75, 71, 69, 72, 76, 73])[0])
print("ties: ", next_greater([2, 1, 2, 4, 3])[0])
assert next_greater([2, 1, 2, 4, 3])[0] == [4, 2, 4, -1, -1]
assert next_greater([3, 1, 4])[0] == [4, 4, -1]      # one candidate is not enough
assert next_greater([3, 5, 9])[0] == [5, 9, -1]      # nearest, not the maximum

for n in (10, 100, 1000):
    falling = list(range(n, 0, -1)) + [n + 1]        # the brute force's worst row
    (b, bs), (s, ss) = brute(falling), next_greater(falling)
    assert b == s
    print("falling row, n=%d: brute %d steps, stack %d steps" % (n + 1, bs, ss))
    assert ss <= 3 * (n + 1)

random.seed(7)
for _ in range(500):
    a = [random.randint(0, 4) for _ in range(random.randint(0, 12))]
    assert next_greater(a)[0] == brute(a)[0]
print("stack == double loop on 500 random arrays with many ties")
```

On the falling row of 1001 elements, the double loop needs about half a million
steps and the stack about two thousand. The ratio grows with n.

### Each line, and which part of the idea it is

| line | in plain words | in the idea |
|---|---|---|
| `ans = [-1] * len(a)` | everyone starts with "no answer" | an element that never leaves the room keeps -1 |
| `stack = []` | the waiting room, newest on top | the open questions |
| `for i, x in enumerate(a)` | the next element arrives | a candidate answer |
| `while stack and a[stack[-1]] < x` | does x beat the newest open question? | "who was I the answer for?" |
| `ans[stack.pop()] = x` | close that question with x | the pop is the moment of answering |
| loop stops | the top is at least x | everyone below is at least x too: the staircase falls |
| `stack.append(i)` | x waits for its own answer | x is now an open question |

Two lines do the real work: the `while` condition, which is where the problem's
meaning lives (greater or smaller, strict or not), and the pop, which is where the
answer is written. The rest is scaffolding.

Three boring confusions, settled:

- **The stack holds indices, the condition reads values.** `a[stack[-1]]` is the
  value of the top. Pushing values instead of indices works only when the answer is
  a value and you never need a distance.
- **The answer is written for the popped element, not for x.** The current element
  does not learn its own next greater element in its own iteration. It learns it
  later, when it is popped, or never.
- **The stack being empty is not special.** An empty stack means "no open
  questions"; the loop does nothing and x is pushed.

### The other direction: scan from the right

There is a second way to write the same thing, and some people find it more
natural. Scan from right to left. Now the stack holds **candidates**: elements to
my right that could still be the next greater element of someone to my left. For
each i, pop every candidate that is not bigger than a[i] (it is hidden behind
a[i] for everyone further left: anyone smaller than that candidate is also smaller
than a[i], which is nearer). Whatever is on top after popping is a[i]'s answer.
Then push a[i] as a candidate.

```
for i from n-1 down to 0:
    while stack and a[stack[-1]] <= a[i]: stack.pop()   # hidden behind a[i]
    ans[i] = a[stack[-1]] if stack else -1
    stack.append(i)
```

Both versions are correct and both are O(n). The left-to-right one answers at pop
time; the right-to-left one answers at push time. Notice the operator flipped from
`<` to `<=`: in the right-to-left version we pop the elements that *cannot* answer,
and an equal value cannot answer "strictly greater". The comparison is always
"pop what is useless", and what is useless depends on the question. That is why
you should derive the operator, not memorise it.

The one-sentence version of the duality, worth carrying: **a pop tells the popped
element its answer on the newcomer's side; the top left after popping is the
newcomer's answer on the other side.**

### The subtle line, both ways

The line is the comparison in the `while`. Run [2, 1, 2, 4, 3] with `<`, then with
`<=`, and print the stack after every step. A `*` marks an answer the second
version gets wrong.

```python run
def run(a, pop_if):
    ans, stack = [-1] * len(a), []
    for i, x in enumerate(a):
        popped = []
        while stack and pop_if(a[stack[-1]], x):
            j = stack.pop()
            ans[j] = x
            popped.append("%d:%d" % (j, a[j]))
        stack.append(i)
        print("   i=%d x=%d pops %-10s stack %s"
              % (i, x, ",".join(popped) or "-", [a[j] for j in stack]))
    return ans

a = [2, 1, 2, 4, 3]
print("pop while top < x  (strictly greater):")
right = run(a, lambda top, x: top < x)
print("pop while top <= x (greater or equal):")
wrong = run(a, lambda top, x: top <= x)
print("right:", right)
print("wrong:", " ".join(str(w) + ("*" if w != r else "") for w, r in zip(wrong, right)))
assert right == [4, 2, 4, -1, -1]
assert wrong == [2, 2, 4, -1, -1]           # index 0 got the equal 2

def next_ge(a):                              # what <= accidentally computes
    return [next((y for y in a[i + 1:] if y >= a[i]), -1) for i in range(len(a))]
assert wrong == next_ge(a)
print("the <= version is exactly 'next greater-or-equal'")
```

Point at the exact step: `i=2 x=2`. With `<`, the stack goes from [2, 1] to
[2, 2]: the 1 is popped and the old 2 stays, still waiting. With `<=`, the stack
goes from [2, 1] to [2]: the old 2 is popped too, and receives the answer 2. That
single cell is the bug. Every later step is the same in both runs.

What the wrong version computes is not garbage. It is the correct answer to
"next greater **or equal**". That is a real question, and some problems ask for
it: [[p:uber-shopkeeper-final-price|Shopkeeper Final Price]] wants the next price
that is *equal or lower*, so there you pop while `top >= x`. The operator is not a
detail. It is the problem statement, translated.

The rule that settles it every time: **pop exactly the elements for which the
newcomer is a valid answer.** If "valid" means strictly greater, pop on `<`. If it
means greater or equal, pop on `<=`. Say the sentence before you type the symbol.

## Why it is correct

:::proof The stack version finds every next greater element
**What we claim.** For an array a[0..n-1], the left-to-right algorithm sets ans[j]
to a[k], where k is the smallest index greater than j with a[k] > a[j], and to -1 if
there is no such k.

**The invariant.** Just before element i is processed:

1. (Membership) The stack holds exactly the indices j < i such that no k with
   j < k < i has a[k] > a[j]. In words: the elements that have no answer *yet*.
2. (Order) Read from bottom to top, their values never increase.
3. (Answers) Every index j < i that is *not* on the stack already has the correct
   ans[j].

**Base case, i = 0.** The stack is empty, there are no j < 0, and all three
statements hold trivially.

**Inductive step.** Assume the invariant before i. Let x = a[i].

Take any j on the stack with a[j] < x. By (1), nothing strictly between j and i is
bigger than a[j]. And a[i] is bigger. So i is the first index after j with a bigger
value, and the correct ans[j] is x. The algorithm does pop such j and writes x.

Take any j on the stack with a[j] >= x. Then x does not answer j, and j still has
no answer among indices up to i. So j must stay on the stack, and it does, provided
the loop does not reach it, which is the next point.

By (2), the values on the stack fall from bottom to top. So the elements with
a[j] < x form a block at the top, and the first element that is at least x has only
elements at least as big beneath it. The `while` loop pops exactly that top block
and stops at the first survivor. So it pops exactly the elements whose answer is x,
no more and no fewer.

After the pops, push i. (1) holds for i+1: the survivors still have no answer up to
i, the popped ones are gone, and i itself has nothing after it yet. (2) holds: the
survivor below i has value at least x, and the rest was already in order. (3) holds:
the popped indices just got their correct answer, and older answers were not
touched.

**The end.** After i = n-1, by (1) the indices left on the stack are exactly those
with no bigger element anywhere after them. Their ans is the initial -1, which is
correct. By (3), everyone else is correct.

**Termination and count.** The for loop runs n times. Each iteration of the while
loop pops one index, each index is pushed once, so the while body runs at most n
times in total. ∎
:::

The proof quietly used these assumptions. Each is a place a variant can break it.

- **"Beats" is a consistent order.** The stop rule ("the first survivor protects
  everything below it") needs transitivity: if the survivor is at least x, and
  everything below is at least the survivor, then everything below is at least x.
  Numbers compare that way. A "beats" relation that is not transitive (rock, paper,
  scissors) would break the stop rule.
- **The answer is the nearest one.** Membership (1) is about the *first* beater.
  If a problem wanted the second greater element, or the greatest one within a
  distance, the waiting room would need a different rule.
- **Elements only arrive; nothing leaves from the middle or the far end.** If
  elements also expire (a sliding window), the oldest can disappear while buried at
  the bottom, and a stack cannot remove it. That is why window problems use a
  [[monotonic-deque]].
- **The strictness in the code matches the strictness in the claim.** The proof
  used "a[j] < x means x answers j". If the problem means "greater or equal", the
  same proof goes through with `<=`, and only with `<=`.

## What it costs

**Time.** Count operations by element, not by loop. Every index is pushed exactly
once: n pushes. Every pop removes a pushed index, and an index is never pushed
again: at most n pops. Every iteration of the for loop ends its while loop with one
failed test (or an empty stack): n tests. Total at most 3n, so O(n). This is an
**amortised** bound: a single arrival can cost up to n pops, but the total over the
run cannot exceed n pops, because pops are paid for by earlier pushes. The worst
single step and the total are different things, and the total is what the time
limit sees.

**Space.** The stack can hold every index at once: a non-increasing array (for next
greater) never pops anything, so the stack ends with all n indices. O(n) extra
space, plus the answer array.

**The brute force for comparison.** n(n-1)/2 comparisons on a falling row: 5·10^9
for n = 10^5. The stack does at most 3·10^5 steps on the same row.

**The forgotten costs.**

- **Circular arrays** double the scan: 2n arrivals, still at most n pushes if you
  push only on the first lap (variation C).
- **Two-sided queries** (previous and next smaller) are either two passes or one
  pass that reads both from the same pop (variation D). Still O(n), but it is easy to
  write two passes with inconsistent tie rules, which is a correctness cost, not a
  time cost.
- **Contribution sums** multiply three numbers per element. In Python the integers
  do not overflow; in fixed-width languages the products need 64-bit integers, and
  problems usually ask for the answer modulo 10^9 + 7.
- **Strings.** For "remove k digits", building the answer with `+=` on a string
  inside the loop is quadratic in many languages. Use a list as the stack and join
  once.

## How to think about it

The code is ten lines. What makes the problems hard is seeing that they are nearest-
beater questions at all, and then choosing the four symbols correctly. Ask these in
order, every time.

1. **What is each element asking for?** Phrase it as "the nearest ___ on my ___
   side that is ___ than me". If you cannot fill those blanks, it is not this
   technique yet.
2. **Which side?** Right: the answer arrives when the element is *popped* (scan
   left to right). Left: the answer is the *top after popping* when the element
   arrives (also left to right). You can get both sides from one pass.
3. **Greater or smaller?** For "next greater", the stack falls (bottom big, top
   small). For "next smaller", it rises. The stack's order is always the opposite of
   what you are looking for, because whatever you are looking for pops everything
   else.
4. **Strict or not?** "Strictly warmer", "cheaper", "taller" are strict.
   "At least", "equal or lower", "no higher" are not. This picks `<` or `<=`. Say
   the sentence "pop exactly the elements the newcomer answers", then write the
   symbol.
5. **Values, indices or distances?** Distances and widths need indices on the
   stack. When in doubt, push indices; values are one lookup away.
6. **What happens to the elements still on the stack at the end?** They never got
   an answer. Is that -1, 0, the array length (for a "right boundary"), or full
   price? Often a sentinel at the end (a value that beats everything) flushes them
   with a uniform rule.
7. **Is it circular, online, or two-sided?** Circular: two laps. Online: the same
   loop, one arrival per call. Two-sided: both answers from the same pass, with one
   strict side and one non-strict side if you are counting.
8. **Is the real question about boundaries?** Histograms, spans and "sum over all
   subarrays" are not about the next greater element itself. They use it as the
   *edge* of a region where the element is the minimum or maximum. If a problem says
   "for every subarray" and n is 10^5, look for an element whose region you can
   bound by its nearest beaters.

Then, before writing code, write three lines: **what each element is asking, which
comparison pops, and what the leftovers get.**

### Telling it from its neighbours

- **Plain stack** ([[stack]]). Parentheses and expression evaluation use a stack
  too, but its contents are not sorted, and pops are triggered by a matching symbol,
  not by a comparison of size.
- **Monotonic deque** ([[monotonic-deque]]). The same sorted structure, plus
  removal at the old end when an element ages out of a window. The tell: "every
  window of size k", "within the last k".
- **Two pointers** ([[two-pointers]]). Trapping rain water can be solved with a
  monotonic stack or with two pointers from both ends. When the question is about
  pairs at the two ends of a range, not about nearest beaters, two pointers is
  usually simpler.
- **Greedy** ([[greedy]]). "Remove k digits" is a greedy argument (an earlier
  bigger digit is always worth deleting); the stack is just its memory. The proof
  is a greedy proof, the code is a stack.
- **Range-query structures** ([[sparse-table]], [[segment-tree]]). If the ranges are
  arbitrary, a stack cannot help. If each element's range is "until something beats
  me", the stack builds all the ranges in O(n) and you may not need a range
  structure at all.
- **Prefix sums** ([[prefix-sums]]). "Sum over subarrays" with a fixed formula is
  prefix sums. "Sum over subarrays of the minimum" is contribution counting with a
  stack. The minimum is what changes the tool.

## Variations

Nine variations, from the everyday to the rare. Each says what changes, why, and
which bank problem teaches it.

### A. The four directions: next or previous, greater or smaller

All four are the same loop, scanning left to right. Only the comparison and the
place where you read the answer change.

| question | pop while | the answer is written |
|---|---|---|
| next strictly greater (to the right) | `a[top] < x` | for each popped index: x |
| next strictly smaller (to the right) | `a[top] > x` | for each popped index: x |
| previous strictly greater (to the left) | `a[top] <= x` | for x: the top after popping |
| previous strictly smaller (to the left) | `a[top] >= x` | for x: the top after popping |

Why does "previous" pop on the non-strict comparison? Because for the previous
greater, an equal element to my left is *not* a valid answer for me, and it is also
useless for everyone after me (I am nearer and just as big). Useless means popped.

Example, next smaller: [[p:amazon-next-smaller-ticket-price|Next Smaller Ticket Price]]
has prices [8, 4, 6, 2, 3] and answer [4, 2, 2, -1, -1]. 4 pops 8 (8 gets 4); 6
pops nothing; 2 pops 6 and 4 (both get 2); 3 pops nothing. The stack rises from
bottom to top, the mirror of the temperatures.

"Equal or lower" is the non-strict version: [[p:uber-shopkeeper-final-price|Shopkeeper Final Price]]
discounts each item by the first later price that is *equal or lower*, so it pops
while `a[top] >= x`. Prices [2, 3, 1, 2, 4, 2]: the 2 at index 3 is discounted by
the equal 2 at index 5, final price 0. With a strict comparison it would wrongly
stay at full price.

### B. Distances and spans: store the index

The answer is a distance, so the stack must hold indices.
[[p:ebay-daily-temperatures|Daily Temperatures]] writes `ans[j] = i - j` at the pop.

The **span** looks backwards: for each day, how many consecutive days ending today
had a price at most today's? That is "the distance to the previous strictly
greater price". In [[p:tokopedia-stock-span|Online Stock Span]], prices
[100, 80, 60, 70, 60, 75, 85] give spans [1, 1, 1, 2, 1, 4, 6]. For 75 on day 5:
the stack holds days 0, 1, 3, 4 (100, 80, 70, 60; day 2's 60 was popped by 70).
Pop 60 (day 4) and 70 (day 3), stop at 80 (day 1); the span is 5 - 1 = 4.

The problem is **online**: prices come one call at a time and you return the span
immediately. Indices still work (keep a counter), but there is a neat form that
stores (price, span) pairs. When a price arrives, its span starts at 1 and it pops
every pair with price <= its own, adding their spans: each popped pair stands for a
block of days that were all at most that price, and so at most today's.

```
span = 1
while stack and stack[-1].price <= price:
    span += stack.pop().span
stack.push((price, span))
```

Trace: 100 (1), 80 (1), 60 (1), 70 pops (60, 1): span 2; 60 (1); 75 pops (60, 1)
and (70, 2): span 1 + 1 + 2 = 4; 85 pops (75, 4) and (80, 1): span 6. The stack of
pairs is the waiting room with each popped day folded into the day that beat it.

### C. Circular arrays: walk twice, push once

In [[p:amazon-next-greater-element-ii|Next Greater Element in a Circular Array]], the
search wraps from the end to the start. The answer for any element is at most one
full lap away, so walk the indices 0, 1, ..., 2n-1 and use `i % n`. On the first
lap, push. On the second lap, only pop: the second lap's job is to answer the
leftovers from the first lap, not to create new open questions.

[3, 8, 4, 1, 2]: after the first lap the stack is 8, 4, 2 (1 was popped by 2,
3 by 8). The second lap meets 3: pops 2 (gets 3). Then 8: pops 4 (gets 8). The 8
stays to the end: -1. Answer [8, -1, 8, 2, 3].

Why not push on the second lap? It is harmless for correctness here but doubles the
stack and the work, and in variants that count things it double-counts. Push once.

### D. Both sides at once, and the nearer of the two

Some problems need the nearest beater on *both* sides.
[[p:amazon-predict-answer|Predict Answer]] asks, for a day i, the nearest day
before or after with a strictly lower price, preferring the earlier day on a tie in
distance. Compute previous smaller and next smaller (two passes, or one pass that
reads both), then compare the two distances.

One pass gives both, with one catch about ties. With `pop while a[top] >= x`, a
popped index j learns "the first later element <= me" (not strictly smaller), and
x learns "the previous element strictly smaller than me". If you need strict on
both sides, use two passes. If you need one strict and one non-strict, one pass is
exactly right, and that is the setting of the next two variations.

### E. The largest rectangle in a histogram

This is the hardest classic and the one that most needs deriving.
[[p:airwallex-largest-rectangle-in-histogram|Largest Rectangle in Histogram]]:
bars of width 1 and heights [2, 1, 5, 6, 2, 3]. What is the largest rectangle
inside the bars? The answer is 10: height 5, over the bars 5 and 6.

**Brute force.** Try every pair (l, r), take the minimum height in between, area =
min * (r - l + 1). With a running minimum that is O(n^2): 5·10^9 for n = 10^5. Too
slow.

**The observation.** Look at the best rectangle. Its height is limited by its
lowest bar; call that bar j. Could the rectangle be wider? Only if the bars just
outside it are at least h[j]. In the best rectangle they are not (or it would not
be the best). So the best rectangle, for its lowest bar j, runs from just after
the **previous smaller bar** to just before the **next smaller bar**. Every bar j
has exactly one such "widest rectangle at height h[j]", and the answer is the
largest of these n rectangles. We went from n^2 candidates to n.

That is the unlocking question again, in a new costume. For bar j, the left and
right walls are its nearest smaller bars on each side. Both come from one stack.

**The stack.** Keep a rising stack (for "smaller"). When bar i arrives and pops bar
j (because h[i] < h[j] or equal, see below), we learn two things at once: the right
wall of j is i, and the left wall of j is the bar now on top of the stack (it is the
previous smaller bar, because the stack rises). So the width is
`i - stack[-1] - 1`, or `i` if the stack is empty. Add a sentinel bar of height 0
at the end so every bar is popped.

<svg viewBox="0 0 560 290" role="img" aria-label="histogram with heights 2, 1, 5, 6, 2, 3 at indices 0 to 5; the rectangle of height 5 over indices 2 and 3 is shaded; the left wall is index 1, height 1, which is on the stack under bar 2; the right wall is index 4, height 2, the bar that pops bar 2; width is 4 minus 1 minus 1 equals 2 and area is 10">
  <g>
    <line x1="20" y1="230" x2="540" y2="230"/>
    <rect x="40" y="170" width="60" height="60"/>
    <rect x="110" y="200" width="60" height="30" stroke-width="3"/>
    <rect class="fill" x="180" y="80" width="130" height="150"/>
    <rect x="180" y="80" width="60" height="150"/>
    <rect x="250" y="50" width="60" height="180"/>
    <rect x="320" y="170" width="60" height="60" stroke-width="3"/>
    <rect x="390" y="140" width="60" height="90"/>
    <text x="70" y="162" text-anchor="middle">2</text>
    <text x="140" y="192" text-anchor="middle">1</text>
    <text x="210" y="72" text-anchor="middle">5</text>
    <text x="280" y="42" text-anchor="middle">6</text>
    <text x="350" y="162" text-anchor="middle">2</text>
    <text x="420" y="132" text-anchor="middle">3</text>
    <text x="70" y="250" text-anchor="middle">0</text>
    <text x="140" y="250" text-anchor="middle">1</text>
    <text x="210" y="250" text-anchor="middle">2</text>
    <text x="280" y="250" text-anchor="middle">3</text>
    <text x="350" y="250" text-anchor="middle">4</text>
    <text x="420" y="250" text-anchor="middle">5</text>
    <text x="245" y="160" text-anchor="middle">5 x 2 = 10</text>
    <text x="280" y="272" text-anchor="middle">left wall: bar 1 (on the stack below bar 2). Right wall: bar 4 (pops bar 2).</text>
    <text x="280" y="288" text-anchor="middle">width = 4 - 1 - 1 = 2</text>
  </g>
</svg>

The same moment on the stack, with real numbers. Before bar 4 (height 2) arrives,
the stack holds bars 1, 2, 3 with heights 1, 5, 6, rising.

| i | h | pops: bar (height), left wall = new top, width, area | stack after |
|---|---|---|---|
| 0 | 2 | none | 0(2) |
| 1 | 1 | bar 0 (2): stack empty, width 1, area 2 | 1(1) |
| 2 | 5 | none | 1(1), 2(5) |
| 3 | 6 | none | 1(1), 2(5), 3(6) |
| 4 | 2 | bar 3 (6): wall 2, width 4-2-1 = 1, area 6; bar 2 (5): wall 1, width 4-1-1 = 2, **area 10** | 1(1), 4(2) |
| 5 | 3 | none | 1(1), 4(2), 5(3) |
| 6 | 0 (sentinel) | bar 5 (3): wall 4, width 1, area 3; bar 4 (2): wall 1, width 4, area 8; bar 1 (1): empty, width 6, area 6 | 6(0) |

Best: 10. Read the bold cell in words: "bar 2 has height 5. It is popped by bar 4,
height 2, so the rectangle of height 5 cannot reach bar 4: the right wall is 4.
Under bar 2 on the stack is bar 1, height 1, so it cannot reach bar 1 either: the
left wall is 1. Between the walls lie bars 2 and 3. Width 2, area 10."

**Ties.** With `pop while h[top] >= x`, an equal bar pops its equal twin early,
giving the twin a too-short width. That is fine: the *last* equal bar in the run
survives until a strictly smaller bar comes, and its left wall is the strictly
smaller bar before the whole run, so it gets the full width. The maximum is still
found. With heights [2, 4, 2, 1], bar 0 (2) is popped by bar 2 (2) with width 2, an
underestimate, but bar 2 is later popped by bar 3 (1) with width 3 and area 6, the
true best. For a *maximum*, a tie rule only needs to give the right width to one
member of each run. For a *sum*, it must give the right share to exactly one, which
is variation F.

**Disguises.** [[p:google-maximal-rectangle-in-binary-matrix|Maximal Rectangle in a Binary Matrix]]:
for each row, let h[c] be the number of consecutive 1s ending at that row in column
c. Every all-ones rectangle has a bottom row, and in that row it is a histogram
rectangle. So run the histogram stack once per row: O(rows x cols).
[[p:visa-largest-square-area-in-cityscape|Largest Square Area in Cityscape]] asks
for the largest square under a skyline. A square of side s fits under a run of
width w whose lowest bar is h exactly when s <= min(h, w). So for each popped bar,
the best square is min(h, width)^2. The stack is unchanged; only the area formula
changes.

### F. Contribution: sum over all subarrays of the minimum

[[p:nvidia-sum-of-subarray-minimums|Sum of Subarray Minimums]]: for [3, 1, 2, 4],
add up the minimum of every subarray. There are n(n+1)/2 = 10 subarrays, and the
answer is 17.

**Brute force.** Enumerate subarrays with a running minimum: O(n^2). With n =
3·10^4 that is 4.5·10^8, too slow in Python.

**Turn the sum inside out.** Instead of "for each subarray, its minimum", ask "for
each element, in how many subarrays is it the minimum?" Then the answer is the sum
of a[i] times that count. For element i, a subarray [l, r] has a[i] as its minimum
when it contains i and does not reach past i's nearest smaller elements. If the
previous smaller is at p and the next smaller is at q, then l can be any of
p+1..i (that is i - p choices) and r any of i..q-1 (q - i choices). The count is
(i - p) * (q - i).

For [3, 1, 2, 4]: element 1 at index 1 has p = -1, q = 4: 2 * 3 = 6 subarrays,
contributing 6. Element 3 at index 0: p = -1, q = 1: 1 * 1 = 1, contributes 3.
Element 2 at index 2: p = 1, q = 4: 1 * 2 = 2, contributes 4. Element 4 at index 3:
p = 2, q = 4: 1, contributes 4. Total 6 + 3 + 4 + 4 = 17.

**The subtle line again, sharper.** With duplicates, a subarray can have two equal
minimums. It must be counted once, so exactly one of them must claim it. Make one
side strict and the other non-strict: p = previous *strictly* smaller, q = next
smaller *or equal*. Then each subarray is credited to its rightmost minimum. Both
strict counts the subarray twice; both non-strict counts it zero times. The run
block in "Traps" shows all three on [2, 2]. This is the line that separates a
correct contribution solution from one that passes the samples.

The same idea with a weight: [[p:amazon-sum-of-max-subarrays|Sum of Max of Subarrays]]
adds max times length over all subarrays ([4, 2, 1, 2] gives 59). The count
becomes a sum of lengths over the (i - p) x (q - i) choices of l and r, which has a
closed form, but the boundaries p and q come from the same stack.
[[p:count-maximum-profitable-groups|Count Maximum Profitable Groups]] counts groups
whose first or last month is the maximum: for each month as the first, the groups
reach until the next strictly greater month, and the mirror for the last; correct
for the groups counted from both ends. Same boundaries, different arithmetic.

### G. Lexicographically smallest: remove k digits

[[p:amazon-remove-k-digits|Remove K Digits]]: delete exactly k digits from "1432219",
k = 3, keeping the order, to make the smallest number. Answer "1219".

**The greedy, derived.** Compare two numbers of the same length: the first position
where they differ decides. So the leftmost digits matter most. Look at any adjacent
pair where an earlier digit is bigger than the next one, like 4 then 3. Deleting the
4 moves the 3 into its place, and the number gets smaller at that position, which
beats anything that happens further right. So: **while you may still delete, and the
previous kept digit is bigger than the current one, delete the previous one.** The
kept digits form a non-decreasing stack.

Trace, k = 3: 1 (stack 1); 4 (14); 3 pops 4 (13, k = 2); 2 pops 3 (12, k = 1);
2 (122); 1 pops 2 (121, k = 0); 9 (1219). If deletions remain at the end, cut them
from the right end (the stack is non-decreasing, so the biggest digits are last).
Strip leading zeros, and return "0" for an empty result.

The difference from the other variations: the pop is limited by a budget (k), not
only by a comparison. The "useless forever" question still decides what is popped.

The same pattern with a different budget: in [[p:erase-pairs|Erase Pairs]], pairs of
equal letters can be erased anywhere, so what is left is one copy of each letter with
an odd count, and the choice is which copy to keep. Pop a bigger letter from the top
when another copy of it is still to come; the "budget" is the remaining count of that
letter. This is the same as the classic "remove duplicate letters" problem.

### H. A stack-driven recurrence (rare, stretch)

[[p:virtu-financial-maximum-sum-of-heights|Maximum Sum of Heights]] asks for the best
mountain under a ceiling. For a peak at i, the left side is a non-decreasing staircase
capped by the ceilings. If j is the previous index with a smaller ceiling, then every
position between j and i is capped at maxHeights[i], and to the left of j the best
is whatever it was for a peak at j. So left[i] = left[j] + maxHeights[i] * (i - j).
The stack gives j; a DP ([[dynamic-programming]]) gives the rest. The same from the
right, then the best left[i] + right[i] - maxHeights[i]. Rare, but it shows the
stack as the boundary-finder inside a bigger algorithm.

### I. Others you may meet (rare)

- **Trapping rain water** with a stack: each pop of a lower bar between two higher
  walls adds a layer of water. The two-pointer solution is more common.
- **The 132 pattern**: scan from the right with a falling stack; the popped values
  are candidates for the "2".
- **Maximum width ramp**: a falling stack of candidate left ends, then a scan from
  the right that pops while the right end is at least the top.
- **Next greater on a stream**: the left-to-right version is already online. Each
  arrival pops and reports answers immediately.

## Recognising it in a statement

From most reliable to least:

1. **"The next / previous / nearest element that is greater / smaller / warmer /
   cheaper / taller."** Direct. Fill the blanks of "the nearest ___ on my ___ side
   that is ___", and you have the comparison.
2. **"How many days until", "how far", "the span", "consecutive days before
   today with price at most"**. Distances to the nearest beater: store indices.
3. **"For every subarray, the minimum (or maximum)", with n around 10^5.** n^2
   subarrays is too many, so the sum must be reorganised per element:
   contribution counting with nearest-smaller boundaries.
4. **"Largest rectangle", "skyline", "bars of width 1", "consecutive buildings".**
   A histogram. Also a 0/1 matrix asking for the largest all-ones rectangle.
5. **"Remove k characters to get the smallest (or largest) result, keeping order."**
   A greedy with a monotonic stack as memory.
6. **"Circular", "wrapping around".** Two laps.
7. **Online: "each call returns the answer for the price just added".** Stock span,
   next greater on a stream.

### Disguises, with the translation

**A discount from the first later item that is not more expensive.** "Each item is
sold at its price minus the price of the first item to its right with equal or
lower price." Translation: next smaller-or-equal to the right; pop while
`a[top] >= x`; leftovers pay full price.

**"Can see" problems.** "A person can see everyone to their right up to and including
the first person taller than them." The boundary is the next greater element; the
count is a distance, or the number of pops each element performs.

**Every rectangle in a binary matrix.** Fix the bottom row; the column heights are a
histogram.

### Anti-signals: looks like this, is not

- **"Next greater number using the same digits"** (*Next Greater Element III*):
  next permutation, not a stack.
- **"Maximum of every window of size k"**: the deque, because elements expire.
- **"Is it greater than everything to its right?"**: a suffix maximum, one number.
- **"Sum of a subarray equals k"**: [[prefix-sums]] with a hash map. Sums are
  linear; minimums are not, which is why minimums need the stack.
- **"For arbitrary queries (l, r), the minimum"**: a [[sparse-table]].

## Traps

**1. The wrong strictness.** Symptom: wrong answers only when the input has repeated
values; samples without ties pass. Say "pop exactly the elements the newcomer
answers" and derive the symbol. The demonstration is in "From the idea to the code".

**2. Pushing values when you need distances.** Symptom: you cannot compute "days
until" or widths at the pop. Push indices.

**3. The histogram width from the popped index.** Symptom: rectangles too narrow,
on inputs where a low bar's rectangle extends to the left over bars that were popped
earlier. The left wall is the *new top* after the pop, not the popped bar itself:
width = `i - stack[-1] - 1`, not `i - j`.

**4. Forgetting the leftovers.** Symptom: the histogram returns too small an area on
a rising input such as [1, 2, 3], because no bar was ever popped. Add a sentinel of
height 0 at the end, or process the remaining stack after the loop.

**5. The same strictness on both sides of a contribution count.** Symptom: sum of
subarray minimums too big (both strict: ties double-counted) or too small (both
non-strict: ties never counted). One strict side, one non-strict.

**6. Remove k digits: leftover budget and leading zeros.** Symptom: "112" with k = 1
returns "112" instead of "11" (no pop ever happened, the budget was never spent), and
"10200" with k = 1 returns "0200" instead of "200".

**7. Circular arrays with one lap.** Symptom: elements near the end get -1 although a
bigger element exists at the start.

The third, fourth, fifth and sixth traps, run:

```python run
def hist(h, wrong_width=False, sentinel=True):
    hh = h + [0] if sentinel else h
    best, stack = 0, []
    for i, x in enumerate(hh):
        while stack and hh[stack[-1]] >= x:
            j = stack.pop()
            if wrong_width:
                width = i - j                          # forgets the bars popped before j
            else:
                width = i - stack[-1] - 1 if stack else i   # left wall = new top
            best = max(best, hh[j] * width)
        stack.append(i)
    return best

def hist_brute(h):
    return max((min(h[l:r + 1]) * (r - l + 1)
                for l in range(len(h)) for r in range(l, len(h))), default=0)

print("[2,1,2]: right", hist([2, 1, 2]), " wrong width", hist([2, 1, 2], wrong_width=True))
assert hist([2, 1, 2]) == hist_brute([2, 1, 2]) == 3 and hist([2, 1, 2], True) == 2
print("[1,2,3]: with sentinel", hist([1, 2, 3]), " without", hist([1, 2, 3], sentinel=False))
assert hist([1, 2, 3]) == 4 and hist([1, 2, 3], sentinel=False) == 0
assert all(hist(h) == hist_brute(h) for h in ([2, 1, 5, 6, 2, 3], [2, 4, 2, 1], [3, 3, 3]))

def sum_mins(a, left_strict, right_strict):
    n, total = len(a), 0
    for i in range(n):                                 # boundaries by scanning, for clarity
        p = i - 1
        while p >= 0 and (a[p] >= a[i] if left_strict else a[p] > a[i]):
            p -= 1
        q = i + 1
        while q < n and (a[q] >= a[i] if right_strict else a[q] > a[i]):
            q += 1
        total += a[i] * (i - p) * (q - i)
    return total

a = [2, 2]                                             # subarrays [2], [2], [2,2]: 6
both_strict, both_loose, mixed = sum_mins(a, True, True), sum_mins(a, False, False), sum_mins(a, True, False)
print("sum of mins of [2,2]: both strict", both_strict, " both non-strict", both_loose, " mixed", mixed)
assert (both_strict, both_loose, mixed) == (8, 4, 6)
assert sum_mins([3, 1, 2, 4], True, False) == 17

def remove_k(num, k, finish=True):
    stack = []
    for d in num:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    if finish:
        stack = stack[:len(stack) - k]                 # spend the leftover budget
        return "".join(stack).lstrip("0") or "0"
    return "".join(stack)

print("remove_k:", remove_k("1432219", 3), remove_k("112", 1), remove_k("10200", 1),
      " unfinished:", remove_k("112", 1, False), remove_k("10200", 1, False))
assert remove_k("1432219", 3) == "1219" and remove_k("112", 1) == "11"
assert remove_k("10200", 1) == "200" and remove_k("10", 2) == "0"
```

On [2, 1, 2] the wrong width pops bar 1 (height 1) at the sentinel and computes width
3 - 1 = 2, forgetting bar 0 to its left, which was popped long ago but is still part of
height 1's rectangle. The true width is 3. In `sum_mins`, the "strict" flag means the
boundary is the first strictly smaller element (equal elements are skipped over). The
mixed rule gives 6, the true sum.

The contribution code above finds the boundaries by scanning, to keep the strictness
readable. The real solution gets p and q from one stack pass: pop while
`a[top] >= x`, so each popped j gets q = i (next smaller-or-equal), and each
arriving i gets p = the top after popping (previous strictly smaller). One pass, the
mixed rule, for free.

## What to memorise

The template:

```python
ans = [-1] * len(a)
stack = []                          # indices still waiting; values sorted
for i, x in enumerate(a):
    while stack and a[stack[-1]] < x:   # pop exactly those x answers
        ans[stack.pop()] = x            # right-side answer, at the pop
    # left-side answer for x, if needed: stack[-1] if stack else -1
    stack.append(i)
```

The sentence that turns a problem into it: **each element asks for its nearest
beater on one side; the stack holds the elements still waiting, and a pop is the
moment of answering.**

The question that finds the pop rule: **when a new element arrives, which old
elements does it make useless forever?**

The habit: before typing the comparison, say "pop exactly the elements the newcomer
answers", and decide strict or not from the statement. For counting, make one side
strict and the other not.

The numbers: at most n pushes and n pops, so about 3n steps; the stack can hold all
n indices; for histograms add a 0 sentinel; for circular arrays walk 2n and push
on the first n.

## Check yourself

:::check
Hand trace. Next strictly greater element of [4, 1, 3, 2, 5], left to right. Write
the stack (as values) after each step and the answers each pop writes. How many pops
in total?
--
| i | x | pops | stack after |
|---|---|---|---|
| 0 | 4 | none | 4 |
| 1 | 1 | none | 4, 1 |
| 2 | 3 | 1 gets 3 | 4, 3 |
| 3 | 2 | none | 4, 3, 2 |
| 4 | 5 | 2 gets 5, 3 gets 5, 4 gets 5 | 5 |

Answer [5, 3, 5, 5, -1]. Four pops, five pushes. 5 is left on the stack and keeps
-1. Notice that 4 sat at the bottom from step 0 to step 4 and was never compared at
all until 5 arrived: the loops at steps 2 and 3 stopped at 3 or never started. That is
where the savings come from.
:::

:::check
Hand trace. Largest rectangle in the histogram [2, 4, 2, 1], popping while
`h[top] >= x`, with a sentinel 0 at the end. For every pop, write the left wall,
the width and the area. Which pop underestimates, and why is the answer still right?
--
| i | h | pops | stack after |
|---|---|---|---|
| 0 | 2 | none | 0(2) |
| 1 | 4 | none | 0(2), 1(4) |
| 2 | 2 | bar 1 (4): wall 0, width 1, area 4; bar 0 (2): empty, width 2, area 4 | 2(2) |
| 3 | 1 | bar 2 (2): empty, width 3, area 6 | 3(1) |
| 4 | 0 | bar 3 (1): empty, width 4, area 4 | 4(0) |

Answer 6. Bar 0 (height 2) is popped by its equal twin, bar 2, and gets width 2,
although the height-2 rectangle really spans bars 0, 1, 2 (width 3). That is an
underestimate. It does no harm because bar 2, the last of the equal run, is popped
later by a strictly smaller bar (1), with the empty stack as its left wall, and gets
the full width 3, area 6. For a maximum, one correct member per run is enough.
:::

:::check
Hand trace. Remove k = 2 digits from "52143" to make the smallest number. Show the
stack and the remaining budget after each digit. Then do "1234", k = 2.
--
5: stack 5, k 2. 2: pops 5 (k 1), stack 2. 1: pops 2 (k 0), stack 1. 4: stack 14.
3: k is 0, no pop, stack 143. Answer "143".

Check by reasoning: the first digit of the answer must be the smallest digit among
the first k+1 = 3 digits (5, 2, 1), which is 1. Then nothing else may be removed,
so "143".

"1234", k = 2: no digit is ever smaller than the one before it, so nothing is
popped, and the stack is 1234 with k = 2 left. Cut 2 from the right end: "12".
:::

:::check
Why must the stack of waiting elements be sorted? Give the argument without
mentioning code, and say what would go wrong in the stop rule if it were not.
--
If an older waiting element a were smaller than a newer waiting element b, then
when b arrived it was bigger than a, and a was still waiting, so b was a's answer
and a would have left. So no such pair exists: newer waiting elements are never
bigger than older ones.

The stop rule ("stop at the first top that is not beaten") relies on this. Because
everything below the survivor is at least as big as the survivor, nothing below can
be beaten either. If the stack were not sorted, a small element could hide under a
big one, the loop would stop at the big one, and the small one would miss its
answer.
:::

:::check
Someone says: "The while loop can pop n elements, and it runs inside a for loop of n
iterations, so the monotonic stack is O(n^2) in the worst case." Where are they
wrong? Use [6, 5, 4, 3, 2, 1, 7] to show it.
--
They multiplied the worst case of one iteration by the number of iterations, but the
worst cases cannot all happen. Pops are limited by pushes: every pop removes an index
pushed earlier, and each index is pushed once, so the total number of pops over the
whole run is at most n.

On [6, 5, 4, 3, 2, 1, 7], the first six iterations pop nothing and the last pops six.
Total pops 6, total pushes 7, plus one stopping comparison per iteration. The one
expensive iteration is paid for by the six cheap ones before it.
:::

:::check
Someone computes the sum of subarray minimums with "previous strictly smaller" and
"next strictly smaller" on both sides, and it passes the samples. Give the smallest
input that breaks it, the wrong and the right answer, and the fix.
--
[2, 2]. The subarrays are [2], [2], [2, 2], so the true sum is 6. With strictly
smaller on both sides, index 0 has p = -1 and q = 2 (nothing strictly smaller to the
right): 2 * 1 * 2 = 4. Index 1 has p = -1, q = 2: 2 * 2 * 1 = 4. Total 8. The
subarray [2, 2] was credited to both of its minimums.

Fix: one side strict, one not. Previous strictly smaller and next smaller-or-equal
give index 0: q = 1, 2 * 1 * 1 = 2; index 1: 2 * 2 * 1 = 4; total 6. Each subarray
is credited to its rightmost minimum. The samples passed because they had no repeated
values.
:::

:::check
Reduce this disguised problem. "Items are sold left to right. Each item's price is
reduced by the price of the first item to its right whose price is equal or lower; if
none exists it is sold at full price. Prices [2, 3, 1, 2, 4, 2]. Give the final prices,
their sum, and the full-price indices." Name the query, the pop rule and what the
leftovers get.
--
The query is the next smaller-or-equal element to the right. Scan left to right, pop
while `a[top] >= x`, and the popped item's discount is x. Leftovers get no discount.

Discounts: 2 gets 1 (index 2), 3 gets 1, 1 gets none, 2 (index 3) gets 2 (index 5,
equal), 4 gets 2, 2 (index 5) gets none. Final prices [1, 2, 1, 0, 2, 2], sum 8,
full price at indices 2 and 5.

With the strict rule (`>`), index 3 would not be discounted by the equal 2 and would
wrongly appear at full price.
:::

:::check
"For each window of k consecutive days, report the maximum." A friend proposes a
monotonic stack. What exactly goes wrong, and what fixes it?
--
The stack can only remove from the top (the newest end). In a window, the oldest
element must also leave when it falls out of the window, even if nobody has beaten it,
and the oldest element is at the bottom. A stack cannot remove from the bottom.

Keep the same sorted structure but allow removal from both ends: a deque. Pop from
the back while the newcomer beats the back (the stack rule), and pop from the front
while the front's index is outside the window. The front is then the window's
maximum. That is the [[monotonic-deque]].
:::
