# Sliding Window

> A sliding window works because, when shrinking a window can only help, the best left end for each right end never moves backwards, so one forward sweep of two ends replaces the search over all n^2/2 subarrays.

## The problem it solves

Here is a string:

```
s = "abcabcbb"
```

Find the length of the longest substring with no repeated character. This is
[[p:akuna-longest-substring-without-repeating-characters|Longest Substring Without Repeating Characters]],
one of the most asked problems in this bank, and it is the problem the whole
chapter grows out of. The answer is 3: "abc" (several times), "bca", "cab". The
substring "abca" has two a's, so 4 is impossible.

A substring is a *contiguous* piece: it has a start and an end, and it contains
everything in between. That is the whole difference between this chapter and the
previous one. In [[two-pointers]] the answer was a pair of positions. Here the
answer is the stretch *between* two positions, and what makes it good or bad is
what is inside it.

The first solution anyone writes tries every substring. There are n(n+1)/2 of
them, about 3 * 10^9 for a string of 80,000 characters, and checking each for
repeats costs up to its length more. That is O(n^3), hopeless. The better first
solution, from each start extend the end until a repeat appears, is O(n^2): still
about 3 * 10^9 steps at that size, still too slow.

What this chapter builds does it in at most 2n steps. Both ends of the window move
only forward. The right end adds one character per step; the left end moves only
when the window has become bad, and only far enough to make it good again. Neither
end ever goes back. The whole chapter is about *why* the left end never needs to go
back, and what to do in the problems where it would.

The technique has six forms, and this chapter teaches all of them:

1. **Fixed-size window**: every window of exactly k elements.
2. **Variable window, the longest valid**: grow, and shrink while invalid.
3. **Variable window, the shortest valid**: grow until valid, then shrink while
   still valid.
4. **Window with a frequency map**: distinct counts, anagrams, replacements.
5. **Exactly k = at most k minus at most k-1**: counting windows with an exact
   condition.
6. **Window maximum with a monotonic deque**: when the window's aggregate cannot be
   undone.

### When it is the wrong tool

- **The answer is not contiguous.** "Subsequence", "any k elements", "you may
  reorder". A window has no way to skip an element in the middle. Usually
  [[sorting]], [[greedy]] or [[dynamic-programming]].
- **Shrinking does not reliably help.** With negative numbers, "sum at most k" is
  not a window problem: dropping a negative element *raises* the sum. Those need
  [[prefix-sums]], with a [[monotonic-deque]] or binary search.
- **Maximum subarray sum with negatives.** Contiguous, but there is no condition
  to restore by shrinking. That is [[kadane]].
- **Random range queries.** "For each of q queries, the sum of a[l..r]" is not a
  sweep; it is [[prefix-sums]] or a [[segment-tree]].

This bank has 385 problems that use a sliding window. Most are one of the six forms
above with a story on top.

## Build it from the brute force

We start from the slowest correct program and fix one waste at a time. The window
appears at the end as the obvious repair.

### Step 1: try every start

The natural first program: for each start l, walk the end r forward while the
substring stays free of repeats. Keep a set of the characters seen since l.

```python
def longest_brute(s):
    best = 0
    for l in range(len(s)):
        seen = set()
        r = l
        while r < len(s) and s[r] not in seen:
            seen.add(s[r])
            r += 1
        best = max(best, r - l)         # s[l..r-1] is the longest valid from l
    return best
```

Run it on "abcabcbb". For each start, the furthest valid end R(l):

| start l | longest valid from l | R(l) | length | characters added |
|---|---|---|---|---|
| 0 | abc | 2 | 3 | a b c, then a repeats |
| 1 | bca | 3 | 3 | b c a, then b repeats |
| 2 | cab | 4 | 3 | c a b, then c repeats |
| 3 | abc | 5 | 3 | a b c, then b repeats |
| 4 | bc | 5 | 2 | b c, then b repeats |
| 5 | cb | 6 | 2 | c b, then b repeats |
| 6 | b | 6 | 1 | b, then b repeats |
| 7 | b | 7 | 1 | b, then the string ends |

Answer 3.

### Step 2: count it

Each start adds characters until a repeat. In the worst case (all characters
different) start l adds n - l characters, for n + (n-1) + ... + 1 = n(n+1)/2 adds
in total: O(n^2). On "abcabcbb" the column "characters added" sums to 18 adds for
8 characters. With n = 80,000 it is about 3 * 10^9.

### Step 3: notice the waste

Look at rows 0 and 1. Start 0 added a, b, c and stopped because the next a was a
repeat. Start 1 then threw the set away and added b and c *again*, before getting
to anything new.

But we already knew that "bc" is free of repeats. It is inside "abc", and "abc"
was free of repeats. Every piece of a string with no repeats has no repeats. So
start 1 did not need to rediscover b and c. It only needed to remove the a, and
then try to add the character that stopped start 0.

The same waste is in every row. Start 2 re-adds a and b; start 3 re-adds b and c.
Look at the column R(l): 2, 3, 4, 5, 5, 6, 6, 7. **It never goes down.** The
furthest end reachable from a later start is never before the furthest end from an
earlier start. So the brute force keeps walking r back to l and forward again,
over ground it has already proved is fine.

Why does R never go down? Because of the sentence above: if s[l..R(l)] is valid,
then s[l+1..R(l)], which is a piece of it, is valid too. So from start l + 1 you
can reach at least R(l). The end never needs to move back.

### The question that unlocks it

Every problem in this family turns on one question:

**If a window is valid, is every smaller window inside it also valid?**

When the answer is yes (the condition is *hereditary*: it is inherited by every
piece), the ends never need to move backwards, and one sweep is enough. When the
answer is no, the sweep is not allowed, and you need a different tool or a
rewrite of the condition.

Say it a second way. A window that went bad can only be repaired by making it
*shorter*, because a longer window that contains the bad one is bad too. And it can
be made shorter only from the left, because the right end is where we are adding.
So the left end moves forward until the window is good again, and it never has a
reason to move back.

"No repeated character" is hereditary: take characters away and you cannot create
a repeat. "At most k zeros" is hereditary. "Sum at most k, all values
non-negative" is hereditary. "At least k distinct values" is *not* (remove things
and you may drop below k); it is the mirror kind, where *growing* helps, and it
gets the mirror template. "Sum at most k, with negatives" is neither, and no
window works.

### You might think: "When the window breaks, start a new window at r."

That is the restart instinct: as soon as s[r] is a repeat, throw the window away
and begin again at r. Try s = "abcbde". At r = 3 the b repeats. Restart at 3:
the window becomes "b", then "bd", "bde": length 3. The best before the restart
was "abc", also 3. So the answer would be 3.

The truth is 4: "cbde". The repeat was the b at position 1, so only positions 0
and 1 had to go. The c at position 2 was fine, and the restart threw it away. The
left end should move *just past the earlier copy* of the repeated character, not
all the way to r. Moving it too far loses windows; not moving it far enough keeps a
bad one.

### You might think: "Shrinking by one step is enough."

The window broke because one character was added, so removing one character
should fix it. Not so. The removed character is the leftmost one, which may not be
the one causing the problem. In "abcabcbb" at r = 6, the window "abcb" has the
repeated b; dropping the a at the left gives "bcb", still bad. You must drop the b
as well: two steps. The repair is a loop, `while` the window is bad, not a single
`if`. The subtle-line section shows exactly what the `if` version gets wrong, and
why it sometimes, dangerously, gets the right answer anyway.

### You might think: "This works for any limit on a sum."

It works when shrinking can only help. Take a = [3, -3, 1] and the condition "sum
at most 2". The whole array has sum 1, so the answer is 3. The window: r = 0, sum
3, bad, drop the 3, l = 1. Then r = 1 and r = 2 give windows [-3] and [-3, 1], at
most length 2. The window says 2. It threw away position 0 forever because [3]
alone was bad, but [3, -3, 1] was good. A *longer* window containing a bad one was
good, so the question above has the answer no, and the sweep is not allowed.

### Step 4: never move the end backwards

The cure for the waste is to keep the work we already did. Keep one window
s[l..r] and a record of what is inside it (here, a count of each character). Then:

- To move to the next end, add s[r] to the record.
- If the window is now bad, remove s[l] from the record and move l forward, and
  repeat until it is good.
- Now s[l..r] is the longest valid window that ends at r. Record its length.

Neither end ever goes back. r goes from 0 to n - 1 once. l goes from 0 towards n,
once, in total over the whole run. So the total work is at most n adds and n
removes, plus the checks.

```python
l = 0
for r in range(n):
    add(a[r])                 # the right end eats one element
    while not valid():        # the window went bad: repair it from the left
        remove(a[l])
        l += 1
    best = max(best, r - l + 1)
```

### The technique in one sentence

**Sliding window: when validity is inherited by every smaller window, the smallest
valid left end never moves backwards as the right end advances, so keep one window,
grow it on the right, shrink it on the left while it is invalid, and read the answer
after each repair; each end moves at most n times in total.**

And the question that produced it: **if a window is valid, is every smaller window
inside it also valid?**

## Worked by hand

Get a pen. s = "abcabcbb". The record is a count of each character in the window;
the window is bad when some count is 2.

| r | s[r] | counts after adding | removals (while bad) | l | window | length | best |
|---|---|---|---|---|---|---|---|
| 0 | a | a1 | | 0 | a | 1 | 1 |
| 1 | b | a1 b1 | | 0 | ab | 2 | 2 |
| 2 | c | a1 b1 c1 | | 0 | abc | 3 | 3 |
| 3 | a | a2 b1 c1 | drop a: a1 | 1 | bca | 3 | 3 |
| 4 | b | a1 b2 c1 | drop b: b1 | 2 | cab | 3 | 3 |
| 5 | c | a1 b1 c2 | drop c: c1 | 3 | abc | 3 | 3 |
| 6 | b | a1 b2 c1 | drop a: a0; still b2; drop b: b1 | 5 | cb | 2 | 3 |
| 7 | b | b2 c1 | drop c: c0; still b2; drop b: b1 | 7 | b | 1 | 3 |

Row 6, told in full:

> "The window is abc, positions 3 to 5. I add the b at position 6: now b appears
> twice, so the window abcb is bad. I remove from the left. Out goes the a at
> position 3; the window is bcb, and b still appears twice, still bad. Out goes the
> b at position 4; the window is cb, positions 5 to 6, and every count is 1. Good.
> This is the longest valid window that ends at position 6, because I only removed
> what I had to. Its length is 2, which does not beat 3."

Here are all eight windows, one per right end, on the real string. Each bar is the
window s[l..r] after the repair.

<svg viewBox="0 0 640 330" role="img" aria-label="the string a b c a b c b b, and below it, for each right end r from 0 to 7, the window after repair drawn as a bar from l to r; the bars have lengths 1, 2, 3, 3, 3, 3, 2, 1, the four bars of length 3 are shaded, and both ends of the bars only move right">
  <g>
    <rect x="120" y="20" width="60" height="34"/>
    <text x="150" y="43" text-anchor="middle">a</text>
    <rect x="180" y="20" width="60" height="34"/>
    <text x="210" y="43" text-anchor="middle">b</text>
    <rect x="240" y="20" width="60" height="34"/>
    <text x="270" y="43" text-anchor="middle">c</text>
    <rect x="300" y="20" width="60" height="34"/>
    <text x="330" y="43" text-anchor="middle">a</text>
    <rect x="360" y="20" width="60" height="34"/>
    <text x="390" y="43" text-anchor="middle">b</text>
    <rect x="420" y="20" width="60" height="34"/>
    <text x="450" y="43" text-anchor="middle">c</text>
    <rect x="480" y="20" width="60" height="34"/>
    <text x="510" y="43" text-anchor="middle">b</text>
    <rect x="540" y="20" width="60" height="34"/>
    <text x="570" y="43" text-anchor="middle">b</text>
    <text x="20" y="84">r=0  l=0</text>
    <rect x="124" y="70" width="52" height="20"/>
    <text x="20" y="114">r=1  l=0</text>
    <rect x="124" y="100" width="112" height="20"/>
    <text x="20" y="144">r=2  l=0</text>
    <rect class="fill" x="124" y="130" width="172" height="20"/>
    <text x="20" y="174">r=3  l=1</text>
    <rect class="fill" x="184" y="160" width="172" height="20"/>
    <text x="20" y="204">r=4  l=2</text>
    <rect class="fill" x="244" y="190" width="172" height="20"/>
    <text x="20" y="234">r=5  l=3</text>
    <rect class="fill" x="304" y="220" width="172" height="20"/>
    <text x="20" y="264">r=6  l=5</text>
    <rect x="424" y="250" width="112" height="20"/>
    <text x="20" y="294">r=7  l=7</text>
    <rect x="544" y="280" width="52" height="20"/>
    <text x="320" y="322" text-anchor="middle">each bar starts at or right of the one above it: the left end never moves back</text>
  </g>
</svg>

Four things in that trace are worth more than the answer.

**Row 6 removed twice, and so did row 7.** That is the `while`. The character that
causes the trouble is not always the one at the left edge.

**The window was briefly bad.** Between "add" and the end of the removals, the
window held a repeat. Validity is not kept at every moment; it is *restored* before
the answer is read. That is why `best` is updated after the loop, never inside.

**The left end moved 7 times in total, over 8 steps.** Not 7 per step: 7 for the
whole run. The inner loop looks like it might make the sweep quadratic, and the
trace shows why it cannot: l has only n places to go, ever.

**Most windows were never looked at.** There are 36 substrings. The sweep looked at
8 of them, one per right end. It never tested "abcab", for example. It did not need
to: "abca" was already bad, and "abcab" contains it. The trace cannot prove that
skipping them was safe; the proof section does.

### A second trace: counting windows, and a removal that is not enough

Now a different question on s = "aabcbb": how many substrings have *at most 2
distinct characters*? This is the counting form, and it shows something the first
trace did not: once the window [l, r] is the longest valid window ending at r, every
window [l', r] with l <= l' <= r is valid too (they are pieces of it). So exactly
r - l + 1 valid windows end at r, and you can count them all in one step.

The record is a count per character; the window is bad when more than 2 characters
have a non-zero count.

| r | s[r] | counts after adding | removals | l | window | valid windows ending at r | total |
|---|---|---|---|---|---|---|---|
| 0 | a | a1 | | 0 | a | 1 | 1 |
| 1 | a | a2 | | 0 | aa | 2 | 3 |
| 2 | b | a2 b1 | | 0 | aab | 3 | 6 |
| 3 | c | a2 b1 c1 | drop a: a1, still 3 kinds; drop a: a0, gone | 2 | bc | 2 | 8 |
| 4 | b | b2 c1 | | 2 | bcb | 3 | 11 |
| 5 | b | b3 c1 | | 2 | bcbb | 4 | 15 |

Total 15. Row 3 is the one to stare at. After the first removal the count of a is
1, not 0, so the window still holds three kinds of character. A single removal did
not repair it, and if you had counted at that point you would have counted the
window "abc", which is bad. Notice also that when a count reaches 0, the character
must leave the record entirely, or "how many kinds" will still count it.

You can check the 15 by hand: there are 21 substrings of "aabcbb", and the 6 bad
ones are exactly those containing all of a, b and c: "aabc", "abc", "aabcb",
"abcb", "aabcbb", "abcbb".

## From the idea to the code

### The direct version, and the window, side by side

The program below writes the "every start" brute force and the window, counts the
characters each one adds, and checks the window against the brute force on random
strings.

```python run
import random

def longest_brute(s):
    best = adds = 0
    for l in range(len(s)):
        seen, r = set(), l
        while r < len(s) and s[r] not in seen:
            seen.add(s[r]); adds += 1
            r += 1
        best = max(best, r - l)
    return best, adds

def longest_window(s):
    count, l, best, adds = {}, 0, 0, 0
    for r, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1     # the right end eats s[r]
        adds += 1
        while count[ch] > 1:                 # bad: only s[r] can be the repeat
            count[s[l]] -= 1                 # the left end gives up s[l]
            l += 1
        best = max(best, r - l + 1)          # longest valid window ending at r
    return best, adds

for s in ["abcabcbb", "abcbde", "bbbbb", ""]:
    print(repr(s), "brute:", longest_brute(s), " window:", longest_window(s))
assert longest_window("abcabcbb") == (3, 8) and longest_brute("abcabcbb") == (3, 18)
assert longest_window("abcbde")[0] == 4

s = "".join(chr(97 + i % 26) for i in range(20000))   # every window of 26 is valid
print("n = 20000: window adds", longest_window(s)[1], "; brute adds", longest_brute(s)[1])
assert longest_window(s)[1] == 20000 and longest_brute(s)[1] > 500000

rng = random.Random(1)
for _ in range(500):
    t = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 12)))
    assert longest_window(t)[0] == longest_brute(t)[0], t
print("500 random strings: the window agrees with the brute force")
```

On "abcabcbb" the window adds 8 characters and the brute force 18. On 20,000
characters the window adds 20,000; the brute force adds over half a million.

One detail in the code is specific to this problem. The check `while count[ch] > 1`
looks only at the character just added. That is allowed because the window was
valid before s[r] came in, so if it is bad now, s[r] must be the repeat. In general
the test is "is the window valid", and here that reduces to one count.

### Each line, and which part of the idea it is

| line | in words | which part of the derivation |
|---|---|---|
| `count, l = {}, 0` | the window is empty, and the empty window is valid | the start of the sweep |
| `for r, ch in enumerate(s)` | each step moves the right end forward by one | r never goes back |
| `count[ch] += 1` | put s[r] into the record | "add" |
| `while count[ch] > 1` | the window is bad; repair it | the repair is a loop, not one step |
| `count[s[l]] -= 1; l += 1` | take s[l] out of the record, move the left end | "remove"; l never goes back |
| `best = max(best, r - l + 1)` | the longest valid window ending at r | read only after the repair |

Settle the small confusions now.

- **What the record stores.** It describes exactly the window s[l..r], no more and
  no less. Every add and every remove must keep that true. A record that still
  mentions characters that have left is the most common bug in this chapter.
- **What l means.** Not "the left pointer": l is *the smallest start for which the
  window ending at r is valid*. Say that sentence, and the position of the `best`
  line follows from it.
- **Inclusive ends.** The window is s[l..r] with both ends included, so its length
  is r - l + 1. If you prefer r to be one past the end, the length is r - l. Pick
  one per function and do not mix them.
- **The empty window.** When l = r + 1 the window is empty. The empty window must
  count as valid, because that is what stops the removal loop: it cannot remove
  past r.

### The subtle lines, both ways

Two lines decide whether a window is correct: the **`while`** that repairs, and
**where the answer is read**. Both are easy to get wrong in a way that passes most
tests.

**First: `while` versus `if`.** Use the counting question from the second trace
("how many substrings have at most 2 distinct characters") on "aabcbb", once with
a `while` and once with an `if` that removes at most one character. The `*` marks a
window that is still bad when it is counted.

```
while (correct)                              if (wrong)
r=0 a     l=0  window a      +1  total 1     r=0 a     l=0  window a       +1  total 1
r=1 a     l=0  window aa     +2  total 3     r=1 a     l=0  window aa      +2  total 3
r=2 b     l=0  window aab    +3  total 6     r=2 b     l=0  window aab     +3  total 6
r=3 c     drop a, drop a                     r=3 c     drop a (only once)
          l=2  window bc     +2  total 8               l=1  window abc*    +3  total 9
r=4 b     l=2  window bcb    +3  total 11    r=4 b     still 3 kinds, drop a
                                                       l=2  window bcb     +3  total 12
r=5 b     l=2  window bcbb   +4  total 15    r=5 b     l=2  window bcbb    +4  total 16
```

Point at the exact row: r = 3. The `if` version removed one a, the window "abc"
still held three kinds of character, and it counted 3 windows ending at r = 3 when
only 2 are valid. Every later row is right again, because the next step happened
to remove the other a. The total is off by one: 16 instead of 15.

Now the dangerous part. Ask the `if` version for the *longest* valid window, and it
says 4, which is right. That is not luck in the details; it is a known fact. With
an `if`, the window never gets shorter, it only slides: when it is bad, one add and
one remove keep its length. It grows only on a step where it ends up valid. So the
largest length it ever reaches is a length that some valid window had. The length
survives; the window itself, the count, and anything else read from l, do not.
That is why the bug survives the first problem someone learns it on and then fails
the second.

**Second: where the answer is read.** For the longest valid window, the answer is
read *after* the repair loop, when the window is valid. For the shortest valid
window (the mirror form, Variation C), the answer is read *inside* the loop, before
each removal, because the loop runs while the window is valid and each pass is a
valid window one shorter than the last. Put it after the loop and you measure a
window that has just become invalid.

The program runs both versions of each line and prints the counts.

```python run
def count_at_most_2(s, use_while, show=False):
    count, l, total, longest = {}, 0, 0, 0
    for r, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        while len(count) > 2:
            count[s[l]] -= 1
            if count[s[l]] == 0:
                del count[s[l]]              # a character with count 0 is gone
            l += 1
            if not use_while:
                break                        # the bug: repair at most one step
        total += r - l + 1
        longest = max(longest, r - l + 1)
        if show:
            bad = "*" if len(set(s[l:r + 1])) > 2 else " "
            print("   r=%d l=%d window %-5s%s +%d total %d" % (r, l, s[l:r + 1], bad, r - l + 1, total))
    return total, longest

def shortest_with_3_kinds(a, read_inside):
    count, l, best = {}, 0, None
    for r, x in enumerate(a):
        count[x] = count.get(x, 0) + 1
        while len(count) >= 3:               # valid: shrink while it stays valid
            if read_inside and (best is None or r - l + 1 < best):
                best = r - l + 1             # every pass is a valid window
            count[a[l]] -= 1
            if count[a[l]] == 0:
                del count[a[l]]
            l += 1
        if not read_inside and l > 0 and (best is None or r - l + 1 < best):
            best = r - l + 1                 # WRONG: this window just became invalid
    return best

s = "aabcbb"
truth = sum(len(set(s[i:j + 1])) <= 2 for i in range(len(s)) for j in range(i, len(s)))
print("while:"); good = count_at_most_2(s, True, show=True)
print("if:");    bad = count_at_most_2(s, False, show=True)
print("truth", truth, "| while (count, longest)", good, "| if", bad)
assert good == (15, 4) and bad == (16, 4) and truth == 15

a = [1, 2, 1, 3, 2]
want = min(j - i + 1 for i in range(5) for j in range(i, 5) if len(set(a[i:j + 1])) >= 3)
print("shortest window with 3 kinds in", a, ": read inside", shortest_with_3_kinds(a, True),
      " read after", shortest_with_3_kinds(a, False), " truth", want)
assert shortest_with_3_kinds(a, True) == want == 3
assert shortest_with_3_kinds(a, False) == 2
```

The shortest-window output shows the second line both ways: read inside, the
answer is 3 ("2, 1, 3"); read after, it reports 2, the length of a window that has
only two kinds of value, because the loop has just removed the element that made it
valid.

## Why it is correct

The trace shows the sweep working. It does not show that the windows it skipped
were safe to skip. That needs the one property we named, and the proof shows
exactly where it is used.

:::proof The sweep finds, for every right end, the smallest valid left end
**Words.** A window is a pair (l, r) meaning a[l..r]; when l = r + 1 it is empty.
"Valid" is a yes or no property of a window. For each right end r, let L(r) be the
smallest l for which (l, r) is valid. We assume two things:

- **(H) Shrinking keeps validity.** If (l, r) is valid, every window inside it is
  valid: (l', r') with l <= l' and r' <= r.
- **(E) The empty window is valid.**

By (E), (r + 1, r) is valid, so L(r) exists and L(r) <= r + 1.

**First fact: L never goes down.** Take any r. The window (L(r+1), r+1) is valid.
The window (L(r+1), r) is inside it, so by (H) it is valid too (if L(r+1) = r + 1
it is the empty window, valid by (E)). So L(r+1) is one of the left ends that work
for r, and L(r), the smallest of them, is at most L(r+1).

**The promise the loop keeps.** When step r reads the answer (after its removals),
the variable l equals L(r).

**Step 0 and every later step.** Suppose that when step r begins, l = L(r - 1) (at
r = 0, l = 0, and nothing smaller exists). Step r adds a[r] and then removes from the
left while the window is invalid.

- *The removals stop.* Each pass moves l forward by one. Once l reaches r + 1 the
  window is empty and valid by (E), so the loop has stopped by then.
- *Where they stop is L(r).* Let l* be the value where the loop stops. (l*, r) is
  valid, because that is the loop's exit condition. Every smaller start is invalid:
  a start between L(r-1) and l* - 1 was tested by the loop and found invalid. A
  start l' smaller than L(r-1) is invalid as well, because if (l', r) were valid,
  then by (H) its piece (l', r-1) would be valid, and that contradicts L(r-1) being
  the smallest valid start for r - 1. So l* is the smallest valid start: l* = L(r).

**Why the answer is right.** The longest valid window ending at r is (L(r), r),
because any valid (l, r) has l >= L(r). The sweep records r - L(r) + 1 for every r,
so the largest of them is the longest valid window of all. For counting, the valid
windows ending at r are exactly the starts L(r), ..., r: each is a piece of
(L(r), r), so valid by (H), and nothing smaller is valid. That is r - L(r) + 1 of them.

**It stops.** r takes n values. l only increases and never passes n. So the whole
sweep does at most n adds and n removes.
:::

Now say plainly what the proof used, because that list is where the bugs come from.

1. **(H) does all the work, twice.** Once to show L never goes down, once to show
   that a start the sweep has passed can never become valid again. Without (H) the
   algorithm is not slow, it is *wrong*: the [3, -3, 1] example is exactly a start
   (position 0) that was invalid for one right end and valid for a later one.
2. **(E), the empty window is valid.** It is what stops the removal loop from
   running past r. If you build "the window is non-empty" into the validity test,
   the loop has no stop. Put non-emptiness in the answer, never in the test.
3. **The record describes exactly the window.** The proof talks about "the window
   (l, r)"; the code only knows its record. A count map that keeps characters with
   count 0 describes a bigger window than the real one.
4. **The test is cheap.** The proof does not need it, but the running time does. A
   test that rescans the window is correct and quadratic.
5. **Nothing says "longest".** The proof gives you L(r) for every r. Longest,
   counting, and "does a valid window of length k exist" all read that same fact.

## What it costs

The inner `while` looks like it makes the sweep O(n^2). It does not, and the reason
is worth deriving rather than memorising.

Let d_r be the number of removals in step r. Step r does 1 add, d_r removes, and
d_r + 1 tests, so it costs about 1 + d_r units. The total is

    (1 + d_0) + (1 + d_1) + ... + (1 + d_(n-1)) = n + (d_0 + d_1 + ... + d_(n-1)).

Each removal moves l forward by one. l starts at 0, never goes back, and never
passes n. So the sum of all the d_r is at most n, whatever the input. The total is
at most 2n: **O(n)**.

Say it a second way. You cannot bound one step: the very first bad step might
remove almost everything. But you can bound the total, because every removal is
paid for by one move of l, and l can only move n times. This is the standard
amortised argument ([[amortized-analysis]]), and it is the same one used for the
reader and writer in [[two-pointers]].

**The constant hiding in "one unit".** One unit is an add, a remove or a test. With
an array of 26 counts, those are true O(1). With a dictionary they are O(1) on
average with a real constant ([[hash-tables]]). For lowercase or uppercase letters
only, a list of 26 is faster and simpler.

**Space.** O(1) for a running sum or a single counter. O(alphabet) for a count
array. O(distinct values in the window) for a dictionary. O(k) for the deque in
Variation F.

**The two costs people forget.**

- **Recomputing the test from scratch.** `len(set(s[l:r+1]))` inside the loop is a
  slice copy and a scan, O(n) per step, and the sweep is O(n^2) again. The record
  exists so the test can be answered in O(1).
- **An aggregate that cannot be undone.** A sum can be undone: subtract the element
  that leaves. A maximum cannot: when the maximum leaves, the running maximum does
  not know what was second. Recomputing `max(a[l:r+1])` per window is O(nk). That
  is why the window maximum is its own variation with its own structure.

## How to think about it

The template is six lines. The skill is deciding which window you are in, and
whether a window is allowed at all. Ask these questions, in order, on every new
problem.

1. **Is the answer contiguous?** Subarray, substring, consecutive days, a time
   range. If elements may be skipped or reordered, stop: not a window.
2. **Is the length fixed?** "Every window of size k", "each 3 x 3 block", "the last
   60 seconds". Then there is no decision: add one, remove one (Variation A).
3. **What is asked: the longest, the shortest, a count, or every window's value?**
4. **The unlocking question: if a window is valid, is every smaller window inside it
   valid?** Yes: longest-valid template, shrink while invalid. No, but *growing*
   keeps validity ("at least k", "contains all of t"): shortest-valid template,
   shrink while valid. Neither: no window; look for [[prefix-sums]].
5. **What record makes add, remove and the test O(1)?** A sum, a count of zeros, a
   count per character plus a number of distinct keys, a "missing" counter.
6. **Is the condition "exactly k"?** Then count at most k, minus at most k - 1
   (Variation E).
7. **Can the window's aggregate be undone?** Sum, count: yes. Maximum, minimum: no,
   use a monotonic deque (Variation F). Median: a heavier structure.
8. **Are there negative numbers in a sum condition?** Then (H) fails. Not a window.

Before writing code, say three sentences: what makes a window valid, what the record
is, and what l means ("the smallest start for which the window ending at r is
valid"). If you cannot, code will not find them for you.

### Telling it from its neighbours

- **Two pointers** ([[two-pointers]]). Converging pointers look for a *pair*; the
  stretch between them is just "not yet ruled out". In a window the stretch between
  the pointers *is* the candidate answer. If the question is about what is inside,
  it is a window.
- **Prefix sums with a hash map** ([[prefix-sums]]). "Count subarrays with sum
  exactly k", especially with negatives, is prefix sums: sum(l..r) = P[r+1] - P[l],
  and a hash map counts earlier prefixes. With only non-negative values, a window
  (Variation E) also works.
- **Kadane** ([[kadane]]). Best sum of any subarray, with negatives. Contiguous, but
  nothing to restore by shrinking.
- **Monotonic deque** ([[monotonic-deque]]). The window maximum or minimum. Also the
  tool for "shortest subarray with sum at least k" when values can be negative,
  over prefix sums instead of over the array.
- **Binary search on the answer.** "Is there a valid window of length m?" is often
  monotone in m and can be tested with a fixed window, but the variable window is
  usually simpler and a log factor faster.

## Variations

Six techniques, then the rarer relatives. Each says what changes, why, a small
example you can check, and a problem from this bank that teaches it.

### A. Fixed-size window

**What changes.** No validity test and no inner loop: the left end is always
r - k + 1. Add a[r]; once r >= k, remove a[r - k]; once r >= k - 1, the window is
full, so read the answer.

**Why.** The length is fixed, so the start is known. What makes it a sliding window
and not k work per window is that only two elements change between neighbouring
windows.

**Example.** a = [1, 3, 2, 6, -1, 4, 1, 8, 2], k = 5: the first window sums to 11.
Slide: remove 1, add 4: 14. Remove 3, add 1: 12. Remove 2, add 8: 18. Remove 6,
add 2: 14. Averages 2.2, 2.8, 2.4, 3.6, 2.8.

**Bank.** [[p:jump-trading-fixed-window-rolling-mean|Fixed-Window Rolling Mean]] is
the template. If the input is a stream, the same two lines run behind a
[[queue]] that holds the last k values.

### B. Variable window, the longest valid (shrink while invalid)

**What changes.** The template from the derivation. Only the record and the test
change from problem to problem.

**Why.** Validity is inherited by smaller windows, so the proof applies.

**Example.** "Flip at most k zeros to ones; longest run of ones." Rephrase it: the
longest window containing at most k zeros. [1,1,1,0,0,0,1,1,1,1,0], k = 2: the
record is the number of zeros in the window; the answer is 6 (positions 4 to 9,
flipping the zeros at 4 and 5).

**Bank.** [[p:akuna-longest-substring-without-repeating-characters|Longest Substring Without Repeating Characters]]
is the template; a common speed-up stores the last position of each character and
jumps l straight past the earlier copy, which is the same window with the removals
done in one step. [[p:inmobi-max-consecutive-ones-iii|Max Consecutive Ones III]] is
the example above: the work is the rephrasing, from "flip" to "at most k zeros in
the window".

Several problems need a step *before* the window. In
[[p:salesforce-maximum-requests-in-window|Maximum Requests in Window]] the
timestamps are not in order; sort them, and the requests inside any time window
become a contiguous run, so it is the longest window whose last minus first
timestamp fits the window length (read the statement for whether the boundary
counts). [[p:amazon-get-minimum-boxes|Get Minimum Boxes]] is the same idea: order
does not matter, so sort the boxes, and the kept boxes may as well be a contiguous
run of the sorted list (if you keep a smallest and a largest, you may as well keep
everything between). Find the longest window with max <= capacity * min, which in a
sorted window is last <= capacity * first; unload the rest.
[[p:amazon-get-max-alternating-music|Get Max Alternating Music]] fixes each of the
two possible alternating patterns ("0101..." and "1010...") and finds the longest
window with at most k positions that disagree with it. The stretch rung,
[[p:amazon-get-max-consecutive-on|Max Consecutive ON Servers]], allows k *segment*
flips: one flip can clear a whole run of zeros at once, so the budget counts runs
of zeros inside the window, not zeros.

### C. Variable window, the shortest valid (shrink while valid)

**What changes.** The condition is the mirror kind: *growing* keeps it ("at least k
distinct", "contains every character of t", "sum at least S with positive values").
Grow until valid; then, while still valid, read the answer and remove from the
left.

**Why.** For each right end r, let the window start as far right as it can while
still being valid. Growing keeps validity, so that latest valid start never moves
back as r grows, which is the same staircase as before, read from the other side.
The answer for r is read on every valid window in the loop, the last of which is
the shortest valid window ending at r.

**Example.** [[p:microsoft-minimum-length-good-subarray|Minimum Length Good Subarray]]:
the shortest subarray with at least k distinct values. [1, 2, 1, 3, 2], k = 3: grow
to [1, 2, 1, 3] (valid, length 4), shrink to [2, 1, 3] (valid, length 3), shrink to
[1, 3] (invalid), stop; grow with 2: [1, 3, 2] is valid, length 3, shrink to [3, 2],
invalid. Answer 3.

**Bank.** [[p:linkedin-minimum-window-substring|Minimum Window Substring]] is the
hardest rung. The record is a "need" count per character of t, plus a single number
`missing`, how many characters of t are still not covered. Adding a character that
was still needed lowers `missing`; removing one that becomes needed raises it.
Validity is `missing == 0`, an O(1) test, and that is the whole trick.

### D. Window with a frequency map (distinct counts, anagrams)

**What changes.** The record is a count per value, and the test reads it: the
number of distinct keys, whether the counts equal a target's counts, or the
largest count.

**Why.** Many conditions on the *contents* of a window depend only on how many of
each value it holds, not on the order. Counts are easy to update by one in each
direction.

**Examples.**

- *Anagrams.* [[p:amazon-anagram-start-indices|All Anagram Start Indices]]: a fixed
  window of length len(p) carrying 26 letter counts. A window is an anagram of p
  when its counts equal p's counts. Only two counts change per slide, so keep a
  number `matches` of letters whose counts agree, and update it as those two
  counts change. s = "cbaebabacd", p = "abc": starts 0 ("cba") and 6 ("bac").
- *Replacements.* [[p:digitalocean-longest-repeating-character-replacement|Longest Repeating Character Replacement]]:
  change at most k characters so the window is all one letter. The window can be
  made uniform by changing everything except its most frequent letter, so it is
  valid when (length - largest count) <= k. "AABABBA", k = 1: answer 4 ("AABA"
  with its B changed, or "BABB" with its A changed). Reading the largest count from 26 counters each
  step is O(26) and safe.
- *Counting with a "contains all" condition.* [[p:snowflake-vowel-substring|Vowel Substring]]
  counts substrings made only of vowels that contain all five. A consonant splits
  the string into vowel-only stretches. Inside one, for each right end, find the
  latest start that still contains all five vowels (a shortest-valid window); every
  start before it, back to the beginning of the stretch, also works, so add that
  many.

### E. Exactly k = at most k minus at most k - 1

**What changes.** You count windows that satisfy "exactly k" by running the counting
window twice: atMost(k) - atMost(k - 1).

**Why.** "Exactly k" is not inherited by smaller windows (remove something and you
may drop to k - 1), so no single window works. But "at most k" is inherited, and
the windows with at most k are exactly the windows with at most k - 1 plus the
windows with exactly k, two separate groups. Subtract.

**Example.** [[p:atlassian-beautiful-subarrays|Beautiful Subarrays]]: count
subarrays with exactly k odd numbers. [1, 1, 2, 1, 1], k = 3. Windows with at most
3 odd: ending at r = 0..4, the counts are 1, 2, 3, 4, 4, total 14. With at most 2
odd: 1, 2, 3, 3, 3, total 12. Exactly 3: 14 - 12 = 2, which are [1, 1, 2, 1] and
[1, 2, 1, 1].

**Guard.** atMost(-1) must return 0, because no window has at most -1 of anything.
Without the guard, "exactly 0" calls a window whose test can never pass, and the
empty-window assumption (E) breaks.

### F. Window maximum with a monotonic deque

**What changes.** The record is a deque of *indices* whose values decrease from
front to back. To add a[i], pop from the back every index with a value <= a[i], then
push i. Pop from the front if it has left the window. The front is the maximum.

**Why.** A maximum cannot be undone, so you need a record that already knows what
comes second. If j < i and a[j] <= a[i], then a[j] can never again be the maximum of
any window: every future window that contains j also contains i, which is at least
as large and stays longer. So j can be thrown away for good. What remains are only
the elements that might still win, in decreasing order.

**Example.** [1, 3, -1, -3, 5, 3, 6, 7], k = 3. The deque (as values) after each
index: [1]; [3] (1 popped by 3); [3, -1], max 3; [3, -1, -3], max 3; [5] (everything
popped by 5), max 5; [5, 3], max 5; [6], max 6; [7], max 7. Maxima 3, 3, 5, 5, 6, 7.

**Bank.** [[p:amazon-sliding-window-maximum|Sliding Window Maximum]] is the
template. [[p:juspay-minimum-of-window-maxima|Minimum of Fixed-Window Maxima]] folds
the maxima into a running minimum; for the example above it is 3. Each index is
pushed once and popped at most once, so the sweep is O(n) by the same counting as
the removal loop. The full treatment is [[monotonic-deque]].

### G. The rarer relatives

- **Windows over time.** "The last 60 seconds": the left end is driven by the clock.
  Keep a deque of timestamps and pop from the front while the front is too old.
  Rate limiters and hit counters ([[rate-limiting]]). The detail that costs points:
  whether the interval is (t - 60, t] or [t - 60, t].
- **Order statistics in a window.** The median or the k-th smallest of each window
  needs two heaps or an ordered structure ([[median-maintenance]], [[ordered-set]]).
- **Exact pattern matching.** A window of length len(p) compared for *equality*, not
  as an anagram, uses a [[rolling-hash]] or [[string-matching]].
- **When (H) fails: prefix sums.** "Shortest subarray with sum at least k" with
  negatives: rewrite the sum as P[r+1] - P[l] and keep a monotonic deque over the
  prefix sums. Not a window over the array.
- **Two windows.** "Two non-overlapping windows with the largest total": the best
  window ending at or before each index, the best starting after it, combined at the
  split point.

The program below runs the shortest-valid, frequency-map, exactly-k and deque forms
against brute force.

```python run
from collections import deque
import random

def min_window(s, t):
    need, missing, l, best = {}, len(t), 0, (len(s) + 1, 0)
    for ch in t:
        need[ch] = need.get(ch, 0) + 1
    for r, ch in enumerate(s):
        if need.get(ch, 0) > 0:
            missing -= 1                     # this copy was really needed
        need[ch] = need.get(ch, 0) - 1
        while missing == 0:                  # valid: read, then shrink
            if r - l + 1 < best[0]:
                best = (r - l + 1, l)
            need[s[l]] += 1
            if need[s[l]] > 0:
                missing += 1
            l += 1
    return "" if best[0] > len(s) else s[best[1]:best[1] + best[0]]

def anagram_starts(s, p):
    k, cnt, out = len(p), [0] * 26, []
    for ch in p:
        cnt[ord(ch) - 97] -= 1               # window minus p; all zero = anagram
    for r, ch in enumerate(s):
        cnt[ord(ch) - 97] += 1
        if r >= k:
            cnt[ord(s[r - k]) - 97] -= 1     # fixed size: remove exactly one
        if r >= k - 1 and not any(cnt):
            out.append(r - k + 1)
    return out

def at_most_odd(a, k):
    if k < 0:
        return 0
    l = odd = total = 0
    for r, x in enumerate(a):
        odd += x % 2
        while odd > k:
            odd -= a[l] % 2
            l += 1
        total += r - l + 1                   # every start l..r is valid
    return total

def window_max(a, k):
    dq, out = deque(), []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()                         # can never be a maximum again
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()                     # left the window
        if i >= k - 1:
            out.append(a[dq[0]])
    return out

print(min_window("ADOBECODEBANC", "ABC"), anagram_starts("cbaebabacd", "abc"))
b = [1, 1, 2, 1, 1]
print("exactly 3 odd:", at_most_odd(b, 3), "-", at_most_odd(b, 2), "=", at_most_odd(b, 3) - at_most_odd(b, 2))
m = window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
print("window maxima:", m, " min of them:", min(m))
assert min_window("ADOBECODEBANC", "ABC") == "BANC" and anagram_starts("cbaebabacd", "abc") == [0, 6]
assert at_most_odd(b, 3) - at_most_odd(b, 2) == 2 and m == [3, 3, 5, 5, 6, 7]
rng = random.Random(4)
for _ in range(300):
    a = [rng.randint(0, 9) for _ in range(rng.randint(1, 10))]
    k = rng.randint(0, 4)
    exact = sum(sum(x % 2 for x in a[i:j + 1]) == k for i in range(len(a)) for j in range(i, len(a)))
    assert at_most_odd(a, k) - at_most_odd(a, k - 1) == exact
    w = rng.randint(1, len(a))
    assert window_max(a, w) == [max(a[i:i + w]) for i in range(len(a) - w + 1)]
print("exactly-k and window maximum agree with brute force on 300 random arrays")
```

## Recognising it in a statement

Signals, most reliable first.

1. **"contiguous", "subarray", "substring", "consecutive"** together with
   *longest*, *shortest*, *maximum*, *minimum* or *count*. The word "subsequence"
   instead rules it out.
2. **"at most k ..."**: distinct values, zeros, replacements, flips, cost. "At most"
   is the inherited condition handed to you in words.
3. **A size in the input.** k, "every block of 3", "60 seconds", "the last 15
   minutes". Fixed-size form.
4. **"at least k ..." or "contains all of ..."** with *shortest*. The mirror form.
5. **"count the subarrays with exactly k ..."**. Two counting windows, subtracted.
6. **"the maximum (or minimum) of every window of size k"**. Deque.
7. **n up to 10^5 or 2 * 10^5 and an obvious loop over all subarrays.** The
   constraint is asking for O(n) or O(n log n).

**Disguised forms.**

- **"Flip at most k bits", "replace at most k characters", "delete at most k
  elements to get the longest run".** Rephrase as "the longest window with at most
  k of the bad kind". The rephrasing is the whole problem.
- **"Remove the fewest elements so that the rest satisfy a range condition", where
  order does not matter.** Sort, and the kept part is a contiguous window of the
  sorted array. Answer n minus the longest valid window (Get Minimum Boxes).
- **"The most events in any time interval of length W".** Sort the times; window
  over the sorted list.
- **"Is some permutation of p a substring of s".** A fixed window with counts.

**Anti-signals.**

- **Negative numbers and a sum limit.** (H) fails. Prefix sums.
- **Maximum subarray sum.** Kadane.
- **The elements may be reordered or skipped, and the order matters for the answer.**
  Not contiguous. If the order does not matter, sorting may create a window; if it
  does, it is not a window.
- **Queries on arbitrary ranges.** Prefix sums or a segment tree.

## Traps

**`if` instead of `while` in the repair.** Symptom: counts and anything read from l
are wrong, while the longest length is right, which hides the bug.

**Characters with count 0 left in the record.** Symptom: the number of distinct
keys never falls, the removal loop cannot stop, and l runs past r into an index
error, or the window shrinks to nothing and the answer is too small.

**Reading the answer in the wrong place.** Longest: after the repair. Shortest:
inside the loop, before each removal. Anywhere else measures a bad window.

**Validity that includes "non-empty".** Symptom: the removal loop has no stopping
point. The empty window must pass the test.

**A running maximum treated as removable.** Symptom: right while the maximum stays
inside the window, wrong after it leaves. Use a deque.

**Restarting the window at r.** Symptom: answers too small on inputs like "abcbde",
where the left end should move just past the earlier copy.

**Assuming (H) because last week's problem had it.** Symptom: wrong answers as soon
as a negative number appears. Demonstrated below.

**Off by one on the length.** r - l + 1 with both ends included; r - l if r is one
past the end. One convention per function.

**Exactly k without the guard.** Symptom: "exactly 0" crashes or loops, because
atMost(-1) has no valid window, not even the empty one.

```python run
def longest_sum_at_most(a, k):            # assumes removing lowers the sum
    total = l = best = 0
    for r, x in enumerate(a):
        total += x
        while total > k:
            total -= a[l]
            l += 1
        best = max(best, r - l + 1)
    return best

def brute_longest(a, k):
    return max([j - i + 1 for i in range(len(a)) for j in range(i, len(a))
                if sum(a[i:j + 1]) <= k] or [0])

for a, k in ([1, 2, 1, 0, 1, 1], 4), ([3, -3, 1], 2):
    w, b = longest_sum_at_most(a, k), brute_longest(a, k)
    print(a, "k =", k, " window:", w, " truth:", b, "  <- (H) broken" if w != b else "")
assert longest_sum_at_most([1, 2, 1, 0, 1, 1], 4) == brute_longest([1, 2, 1, 0, 1, 1], 4) == 4
assert longest_sum_at_most([3, -3, 1], 2) == 2 and brute_longest([3, -3, 1], 2) == 3

def distinct_le_2_keeps_zeros(s):         # WRONG: never deletes count-0 keys
    count, l, best = {}, 0, 0
    for r, ch in enumerate(s):
        count[ch] = count.get(ch, 0) + 1
        while len(count) > 2 and l <= r:  # without l <= r this would run off the end
            count[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best

print("'aabcbb', at most 2 distinct, count-0 keys kept:", distinct_le_2_keeps_zeros("aabcbb"),
      " truth: 4")
assert distinct_le_2_keeps_zeros("aabcbb") == 3
```

The first half of that output is the chapter's lesson in three numbers. [3, -3, 1]
has sum 1, so the whole array is a valid window of length 3. The sweep rejected
position 0 at the very first step, because [3] alone had sum 3, and it never came
back. The code is fine; the assumption is wrong. The second half shows the count-0
bug: after "c" arrives, the record still holds "a" with count 0, so it believes the
window has three kinds of character forever, and it shrinks the window to nothing
on every step.

## What to memorise

One skeleton, its mirror, one question, one habit.

```python
l = 0                                  # longest valid: shrink while invalid
for r in range(n):
    add(a[r])
    while not valid():
        remove(a[l]); l += 1
    best = max(best, r - l + 1)        # or: total += r - l + 1

l = 0                                  # shortest valid: shrink while valid
for r in range(n):
    add(a[r])
    while valid():
        best = min(best, r - l + 1)    # read BEFORE removing
        remove(a[l]); l += 1
```

**The sentence** that turns a problem into it: "if a window is valid, every smaller
window inside it is valid, so the left end never moves back".

**The habit**: say what l means before you write the `best` line. "l is the
smallest start for which the window ending at r is valid." The position of the read,
the `while`, and the count r - l + 1 all follow from that sentence.

**Numbers worth carrying**: n(n+1)/2 subarrays against at most 2n pointer moves;
r - l + 1 valid windows end at r; exactly(k) = atMost(k) - atMost(k - 1).

## Check yourself

:::check
Hand trace. s = "pwwkew", longest substring without a repeated character. Fill the
table: r, s[r], removals, l, window, best.
--
| r | s[r] | removals | l | window | best |
|---|---|---|---|---|---|
| 0 | p | | 0 | p | 1 |
| 1 | w | | 0 | pw | 2 |
| 2 | w | drop p (w still twice), drop w | 2 | w | 2 |
| 3 | k | | 2 | wk | 2 |
| 4 | e | | 2 | wke | 3 |
| 5 | w | drop w | 3 | kew | 3 |

Answer 3 ("wke" or "kew"). Row 2 needs two removals: the repeated w is not the
character at the left edge. Note that "pwke" is not an answer: it is a subsequence,
not a substring.
:::

:::check
Hand trace, the subtle line. Count the substrings of "abaccc" with at most 2
distinct characters, once with `while` and once with `if` (remove at most one
character per step). Which row first differs, and what are the two totals? What
does each version say is the longest valid length?
--
With `while`:

| r | s[r] | removals | l | window | +count | total |
|---|---|---|---|---|---|---|
| 0 | a | | 0 | a | 1 | 1 |
| 1 | b | | 0 | ab | 2 | 3 |
| 2 | a | | 0 | aba | 3 | 6 |
| 3 | c | drop a (a1 b1 c1, still 3 kinds), drop b (a1 c1) | 2 | ac | 2 | 8 |
| 4 | c | | 2 | acc | 3 | 11 |
| 5 | c | | 2 | accc | 4 | 15 |

With `if`, row 3 drops only the first a; the window "bac" still has three kinds
and is counted as 3: total 9. Row 4: add c, still a, b, c present; drop b, l = 2,
window "acc", +3, total 12. Row 5: +4, total 16.

The first different row is r = 3: 2 versus 3, the extra one being the bad window
"bac". Totals 15 (correct) and 16. Both versions say the longest is 4 ("accc"),
which is why the `if` bug survives problems that only ask for the length.
:::

:::check
Hand trace, the deque. Window maximum of a = [4, 2, 12, 3, 5, 1, 7], k = 3. Write
the deque (as values) after each index, and the maxima.
--
| i | a[i] | pops from the back | pop from the front | deque (values) | max |
|---|---|---|---|---|---|
| 0 | 4 | | | 4 | |
| 1 | 2 | | | 4, 2 | |
| 2 | 12 | 2, 4 | | 12 | 12 |
| 3 | 3 | | | 12, 3 | 12 |
| 4 | 5 | 3 | | 12, 5 | 12 |
| 5 | 1 | | 12 (index 2 left the window) | 5, 1 | 5 |
| 6 | 7 | 1, 5 | | 7 | 7 |

Maxima [12, 12, 12, 5, 7]. Check against brute force: windows [4,2,12], [2,12,3],
[12,3,5], [3,5,1], [5,1,7] have maxima 12, 12, 12, 5, 7. At i = 5, the 12 is popped
from the front because its index 2 is at most i - k = 2.
:::

:::check
Why is the left end allowed never to move backwards? Give the argument, not the
slogan.
--
Because validity is inherited by smaller windows, and that forces L(r), the
smallest valid start for right end r, never to go down. The argument: the window
(L(r+1), r+1) is valid; the window (L(r+1), r) is a piece of it, so it is valid too;
so L(r+1) is a valid start for r, and L(r), the smallest valid start for r, is at
most L(r+1).

The consequence is the algorithm: when r moves to r + 1, the start we are looking
for is at or to the right of where l already is, so moving l forward finds it, and
moving back is never needed. Without inheritance there is no such argument, and
[3, -3, 1] with "sum at most 2" shows there is no such truth either.
:::

:::check
Someone says: "A sliding window finds the maximum-sum subarray in O(n)." Where are
they wrong, and what is the correct statement?
--
They assumed the window's condition is inherited where there is none. "This window
has a large sum" is not a yes or no condition you can restore by shrinking, and
removing a negative element *raises* the sum, so there is nothing for the left end
to do. With only non-negative values the answer is the whole array, so the problem
is only interesting in the case the window cannot handle.

The correct statement: maximum-sum subarray with any signs is [[kadane]],
cur = max(x, cur + x), also O(n) but a different algorithm with a different proof.
The nearby true statement: the *longest* subarray with sum at most k is a window
when every value is non-negative, and is not when values can be negative.
:::

:::check
Someone counts subarrays with *exactly* 2 distinct values by running the counting
window with the test "at most 2 distinct" and adding r - l + 1. On [1, 2] they get
3, but the answer is 1. What did they count, and what is the fix? Work it on
[1, 2, 1, 3].
--
They counted subarrays with *at most* 2 distinct values, which includes the ones
with exactly 1: on [1, 2] those are [1], [2] and [1, 2], so 3, of which only [1, 2]
has exactly 2. "Exactly 2" is not inherited by smaller windows, so it cannot be the
window's test.

The fix: exactly(2) = atMost(2) - atMost(1). On [1, 2, 1, 3]:

- atMost(2): ending at r = 0..3, the windows have l = 0, 0, 0, 2 (at r = 3, [1, 2, 1, 3]
  has 3 kinds; drop 1, drop 2, leaving [1, 3]). Counts 1 + 2 + 3 + 2 = 8.
- atMost(1): l = 0, 1, 2, 3. Counts 1 + 1 + 1 + 1 = 4.

Exactly 2: 8 - 4 = 4. They are [1, 2], [2, 1], [1, 2, 1] and [1, 3].
:::

:::check
Disguised problem. Boxes [7, 1, 3, 9, 2, 4, 8], capacity 2. Unload the fewest boxes
so that the remaining ones satisfy max <= capacity * min. Reduce it to a window and
solve it by hand.
--
The order of the boxes does not matter, only which ones stay. Sort: [1, 2, 3, 4, 7,
8, 9]. If you keep a smallest box x and a largest box y, every box between them in
sorted order also satisfies x <= box <= y, so keeping it never breaks the condition.
So the kept boxes may as well be a contiguous run of the sorted list, and the
condition on a run is last <= 2 * first. Removing from either end of a valid run
keeps it valid, so it is a longest-valid window.

Sweep: r = 0 (1): ok, length 1. r = 1 (2): 2 <= 2, length 2. r = 2 (3): 3 > 2,
drop 1, [2, 3], length 2. r = 3 (4): 4 <= 4, [2, 3, 4], length 3. r = 4 (7): 7 > 4,
drop 2; 7 > 6, drop 3; 7 <= 8, [4, 7], length 2. r = 5 (8): 8 <= 8, [4, 7, 8],
length 3. r = 6 (9): 9 > 8, drop 4; 9 <= 14, [7, 8, 9], length 3. Longest 3, so
unload 7 - 3 = 4 boxes.
:::
