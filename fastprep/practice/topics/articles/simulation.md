# Simulation Problems

> A simulation is easy to write and easy to get slow or wrong, because the only real decision in it is what to carry from one event to the next: the smallest state that answers every later question without looking back, updated so that each step reads the old state before it writes the new one.

## The problem it solves

Here is an assessment problem from this bank,
[[p:amazon-get-total-requests|Get Total Requests]]. An application runs on n
servers. Server i has an id, and the id is also how many requests it can handle.
Every day, one id is retired: *all* servers whose id equals `replaced[j]` are
swapped for servers with id `newId[j]`. After each day, report the total number
of requests the servers can handle, which is the sum of all ids.

Take the third sample:

| day | replace | servers after the day | total |
|---|---|---|---|
| start | | [2, 5, 2] | 9 |
| 1 | 2 becomes 3 | [3, 5, 3] | 11 |
| 2 | 5 becomes 1 | [3, 1, 3] | 7 |
| 3 | 3 becomes 5 | [5, 1, 5] | 11 |

The answer is [11, 7, 11]. Nothing in this problem is clever. There is no
recurrence, no proof of optimality, no choice to make. The statement tells you
exactly what happens on each day, and you can follow it with a pen.

That is the shape of a simulation: **a list of events, rules for what each event
does, and a question about what came out.** It is the most common shape in this
bank. About 1,500 problems here are simulations, which makes it the fifth most
common topic out of 150, and it covers ledgers, login systems, queues at a
counter, robots on a grid, game boards, rate limiters, allocators, parsers and
undo stacks.

The first solution anyone writes is the statement read aloud: keep the list of
servers, and each day walk the whole list, replace the matching ids, then walk
it again to add it up. It is correct. It is also too slow. The constraints say n
can be 10^5 and there are n days. Each day touches every server twice, so the
work is about 2 x 10^5 x 10^5 = 2 x 10^10 steps. In Python that is hours.

So the problem is not "what happens". The statement already says what happens.
The problem is **how to know what happens without redoing the past every time.**
That is what this chapter teaches: how to pick a state that makes each event
cheap, how to keep it correct, and how to keep the bookkeeping straight
(ties, empty input, the off-by-one at the edges) in the ten or so shapes that
simulations come in.

### When it is the wrong tool

Simulation answers "what happens". It never answers "what is best". Watch for
these:

- **There is a choice.** If the statement asks for the *maximum* profit or the
  *fewest* moves, and you get to decide what happens next, the branching is the
  real problem. That is [[greedy]], [[dynamic-programming]] or [[backtracking]].
  You can simulate a fixed policy. You cannot simulate a decision you have not
  made yet.
- **The horizon is astronomically long.** "After 10^18 steps" with a small state
  means the states must repeat. Find the cycle and jump
  ([[cycle-detection]]), or find a closed form ([[math]],
  [[matrix-exponentiation]]). The cost of a simulation is the number of events
  you process, so a timeline of 10^18 ticks cannot be walked.
- **Nothing changes.** If every operation is a query and nothing mutates, there
  is no state to carry. Sort the queries and answer them together
  ([[sweep-line]], [[prefix-sums]]).
- **A named structure is the whole problem.** "Least recently used", "the
  smallest so far", "a prefix of a word": the simulation around it is trivial and
  the real topic is [[lru-cache]], [[heap]] or [[trie]].

## Build it from the brute force

We start from the program a beginner writes, count what it does, find the waste,
and remove it. The fast version will appear at the end as the obvious fix.

### Step 1: write the statement down as code

Every simulation has the same skeleton: some state, one loop over the events,
and one transition per event.

```
state = the servers, as a list
for each day (old, new):
    for each server: if its id is old, make it new     # the rule
    output the sum of the list                         # the question
```

This is worth writing even when you know it is slow. It is the specification,
in a form a computer can run. Later we will test the fast version against it on
thousands of random inputs. In most algorithm topics the brute force is a
different algorithm. In simulation the brute force *is* the problem statement,
which is the reason testing against it is so cheap and so convincing.

### You might think: "There is no algorithm here. Just transcribe it."

That is half right. There is no insight to have, and the transcription above is
the correct answer to "what happens". But the problem has a second sentence,
the constraints, and the transcription fails it. With n = 10^5 servers and
10^5 days the loop is 2 x 10^10 steps.

The tiny counterexample is not a different output; it is a count. Take n = 4
servers [1, 2, 3, 4] and four days, each replacing an id that does not exist.
Nothing changes, the totals are [10, 10, 10, 10], and the literal loop still
touched 4 x 4 x 2 = 32 cells to learn that. The output had no news in it, and
the program paid full price for it every day.

### Step 2: count it

Write the cost per event. Day j costs n steps to replace and n steps to sum.
There are m = n days. Total 2nm. Nothing about the data makes it cheaper: even
a day that changes nothing pays 2n.

That is the first habit of this topic. **The cost of a simulation is the sum,
over events, of the cost of one event.** You never need anything fancier than
that sum. The question is always what one event costs you, and why.

### Step 3: notice the waste

Look at what one day really changes. Here are five days on eight servers:

| day | replace | servers after the day | cells that changed | cells the loop read |
|---|---|---|---|---|
| start | | [1, 2, 3, 4, 5, 6, 7, 8] | | |
| 1 | 3 becomes 9 | [1, 2, 9, 4, 5, 6, 7, 8] | 1 | 16 |
| 2 | 7 becomes 2 | [1, 2, 9, 4, 5, 6, 2, 8] | 1 | 16 |
| 3 | 2 becomes 6 | [1, 6, 9, 4, 5, 6, 6, 8] | 2 | 16 |
| 4 | 4 becomes 4 | [1, 6, 9, 4, 5, 6, 6, 8] | 0 | 16 |
| 5 | 6 becomes 1 | [1, 1, 9, 4, 5, 1, 1, 8] | 3 | 16 |

The loop reads 16 cells a day. It changes between 0 and 3. Two different wastes
are hiding in that table.

**Waste one: the sum is recomputed from scratch.** On day 1 the total was 36 and
one server went from 3 to 9. The new total is 36 + 6 = 42. You did not need to
add eight numbers to know that. You needed the old total and the change.

**Waste two: the replacement looks at every server, but only the *count* of
matching servers matters.** On day 5, three servers had id 6. Which three, at
which positions, does not matter to anything the problem ever asks. The
question is only ever "how many servers have id x?", because all of them are
replaced together, and the sum only depends on how many of each id there are.
The positions in the list are information the future never uses.

So the list is too much state (it remembers positions nobody asks about) and
the sum is too little (it is thrown away each day and rebuilt).

### The question that unlocks it

The general form of what we just did is one question, and it is the question
to ask on every simulation:

**What is the least the next event needs to know about everything that has
happened so far?**

Think of the events on a line. Cut the line anywhere. Everything left of the cut
has happened, and you are not allowed to look at it again. Everything right of
the cut is still coming. What you write on the cut is the state. It must be
enough for every event on the right to be answered without looking left, and
it should be no bigger than that.

<svg viewBox="0 0 660 200" role="img" aria-label="a timeline of events with a vertical cut: events to the left are processed and forgotten, the state sits on the cut, events to the right must be answered from the state alone">
  <g>
    <line x1="25" y1="100" x2="635" y2="100"/>
    <circle cx="70" cy="100" r="9"/>
    <circle cx="140" cy="100" r="9"/>
    <circle cx="210" cy="100" r="9"/>
    <circle cx="280" cy="100" r="9"/>
    <circle class="fill" cx="400" cy="100" r="9"/>
    <circle class="fill" cx="470" cy="100" r="9"/>
    <circle class="fill" cx="540" cy="100" r="9"/>
    <line x1="340" y1="30" x2="340" y2="170"/>
    <rect class="fill" x="295" y="50" width="90" height="30" rx="5"/>
    <text x="340" y="44" text-anchor="middle">state</text>
    <text x="175" y="140" text-anchor="middle">processed, then forgotten</text>
    <text x="175" y="158" text-anchor="middle">(never read again)</text>
    <text x="500" y="140" text-anchor="middle">still to come</text>
    <text x="500" y="158" text-anchor="middle">(answered from the state alone)</text>
    <text x="340" y="190" text-anchor="middle">each event moves the cut one step to the right</text>
  </g>
</svg>

That picture is abstract, so here it is with the real numbers from the sample,
cut after day 1. Left of the cut: the start [2, 5, 2] and day 1 (2 becomes 3).
Right of the cut: day 2 (5 becomes 1) and day 3 (3 becomes 5). On the cut:

<svg viewBox="0 0 660 210" role="img" aria-label="the same cut on the sample: the processed start list 2 5 2 and day 1, the state on the cut is count of 3 is 2, count of 5 is 1, total 11, and days 2 and 3 to the right read only that state">
  <g>
    <line x1="25" y1="120" x2="635" y2="120"/>
    <circle cx="80" cy="120" r="9"/>
    <circle cx="200" cy="120" r="9"/>
    <circle class="fill" cx="460" cy="120" r="9"/>
    <circle class="fill" cx="580" cy="120" r="9"/>
    <text x="80" y="150" text-anchor="middle">start</text>
    <text x="80" y="168" text-anchor="middle">[2, 5, 2]</text>
    <text x="200" y="150" text-anchor="middle">day 1</text>
    <text x="200" y="168" text-anchor="middle">2 becomes 3</text>
    <text x="460" y="150" text-anchor="middle">day 2</text>
    <text x="460" y="168" text-anchor="middle">5 becomes 1</text>
    <text x="580" y="150" text-anchor="middle">day 3</text>
    <text x="580" y="168" text-anchor="middle">3 becomes 5</text>
    <line x1="330" y1="20" x2="330" y2="190"/>
    <rect class="fill" x="235" y="32" width="190" height="56" rx="6"/>
    <text x="330" y="55" text-anchor="middle">count: {3: 2, 5: 1}</text>
    <text x="330" y="77" text-anchor="middle">total: 11</text>
    <text x="330" y="205" text-anchor="middle">day 2 needs count[5] = 1 and the total; nothing else</text>
  </g>
</svg>

Day 2 asks "how many servers have id 5?" (one) and "what was the total?" (11).
It moves that one server from 5 to 1, which changes the total by 1 x (1 - 5) =
-4, so the total is 7. It never needed to know that the list once said
[2, 5, 2], or which position the 5 was in.

### You might think: "The total is enough. Just keep one number."

It is not, and a two-line example shows why. Servers [1, 3] and servers [2, 2]
both have total 4. Now the day "replace 2 with 10" arrives. For [1, 3] nothing
happens and the total stays 4. For [2, 2] both servers change and the total
becomes 20. The same state (total 4) must give two different answers, so the
total alone cannot be the state. The state needs the counts, because the next
event asks about counts.

This is the general test for "too small". **If two different histories land on
the same state and some future event treats them differently, the state is
missing something.** Look for that pair of histories; it is how you find the
missing field.

### You might think: "Keep the counts, and recompute the total from them."

That is correct, and it is still too slow in the worst case. The sum over the
dictionary costs one step per distinct id, and there can be 10^5 distinct ids, so
we are back to 10^10 when every server is different. The fix is to keep the total
*alongside* the counts and update it in the same place the counts change. This
is "too big" in a good way: the total is redundant (it can be computed from the
counts), and we keep it anyway because it is cheap to maintain and expensive to
recompute.

Every redundant field creates a promise. Here the promise is

```
total == sum(id * count[id] for every id)
```

and it is now your job to keep it true at every write. Every simulation bug that
survives the samples is a promise like this one broken on some branch the
samples never took. Write the promise down as a comment. Later, write it as an
assert while you test.

### Step 4: the transition

With the state chosen, one day is three facts:

1. `moved = count[old]` servers change (zero if no server has that id).
2. They all join the group with id `new`. The group for `old` is now empty.
3. Each of them changes by `new - old`, so `total += moved * (new - old)`.

That is constant work per day, plus a dictionary lookup.

### The technique in one sentence

**Choose the smallest state that answers every later event without looking
back, keep any derived number next to the thing it is derived from, and make
each event a transition that reads the old state completely before it writes
the new one.** The question that finds the state is the one in bold above: what
is the least the next event needs to know about the past?

The last clause, "reads before it writes", sounds pedantic. It is the subtle line
of this topic, the one place where code that looks right is wrong, and it gets
its own demonstration below.

## Worked by hand

### The first trace: the sample, through the state

Sample 3 again: servers [2, 5, 2], days (2 becomes 3), (5 becomes 1), (3 becomes 5).

Start. Count the ids: two servers have id 2, one has id 5. Total 2 + 5 + 2 = 9.

| day | rule | moved = count[old] | count after | total change | total |
|---|---|---|---|---|---|
| start | | | {2: 2, 5: 1} | | 9 |
| 1 | 2 becomes 3 | count[2] = 2 | {5: 1, 3: 2} | 2 x (3 - 2) = +2 | 11 |
| 2 | 5 becomes 1 | count[5] = 1 | {3: 2, 1: 1} | 1 x (1 - 5) = -4 | 7 |
| 3 | 3 becomes 5 | count[3] = 2 | {1: 1, 5: 2} | 2 x (5 - 3) = +4 | 11 |

Output [11, 7, 11], the same as the literal table at the top of the chapter.

Day 3 in words: "The rule says every server with id 3 becomes 5. How many servers
have id 3? The count says two. I do not know where they are, and I do not need
to. Each of them goes up by 5 - 3 = 2, so the total goes up by 4, from 7 to 11.
Their group, id 3, is now empty, so I remove it. The group for id 5 had nobody (we
emptied it on day 2), so it becomes 2."

Check the promise after each row. After day 2: 3 x 2 + 1 x 1 = 7. Yes.

### The second trace: two groups merge

Sample 1 shows something the first trace did not: the new id can already exist.
Servers [20, 10], days (10 becomes 20), (20 becomes 1).

| day | rule | moved | count after | total change | total |
|---|---|---|---|---|---|
| start | | | {20: 1, 10: 1} | | 30 |
| 1 | 10 becomes 20 | 1 | {20: 2} | 1 x (20 - 10) = +10 | 40 |
| 2 | 20 becomes 1 | 2 | {1: 2} | 2 x (1 - 20) = -38 | 2 |

Look at day 1. The one server with id 10 joins the server already at id 20. The
group for 20 now has *two* members. Day 2 then moves both. If day 1 had written
`count[20] = 1` (overwrite) instead of `count[20] += 1` (join), day 2 would move
one server, report 21, and be wrong. In the list version this cannot happen,
because the two 20s are simply two cells. In the count version you must say
"join" explicitly. A compressed state is faster, and it makes you responsible for
facts the list kept for free.

### The third trace: old equals new

Nothing in the constraints forbids a day that replaces id 4 with id 4. Servers
[4, 4, 7], days (4 becomes 4), (4 becomes 1). The literal list: day 1 changes
nothing, total 15. Day 2 makes both 4s into 1s: [1, 1, 7], total 9.

Here is the state version with the steps of day 1 in the order a natural first
draft writes them: "add the old group to the new one, then empty the old one".

| step of day 1 | count[4] | total |
|---|---|---|
| before | 2 | 15 |
| moved = count[4] | 2 | 15 |
| count[4] = count[4] + moved | 4 | 15 |
| count[4] = 0 | **0** | 15 |
| total += 2 x (4 - 4) | 0 | 15 |

Day 1 reports 15, which is right. But the count of id 4 is now 0, and there are
really two servers with id 4. On day 2, "4 becomes 1" moves zero servers and
reports 15. The truth is 9. The bug happened on day 1 and showed up on day 2.
That is typical: a wrong state often gives a right answer today and a wrong
answer later, which is why the samples miss it.

What went wrong is one sentence. The step "empty the old group" was meant to
clear the *old* state, but it ran after the *new* state was written into the same
cell, so it erased the new state. Old and new were the same place. The fix is to
finish with the old state before writing the new: take the old group out first
(`moved = count.pop(old)`), then add it to the new group. With that order,
old == new is harmless: you remove the two servers from group 4, then put them
back into group 4.

## From the idea to the code

### The literal version and the state version, side by side

```python run
import random


def literal(server, replaced, new_id):
    """The statement, read aloud: rewrite the array every day, then add it up."""
    servers = list(server)                      # a copy: never edit the caller's list
    out = []
    for old, new in zip(replaced, new_id):      # one day = one event
        for i in range(len(servers)):           # look at every server ...
            if servers[i] == old:
                servers[i] = new                # ... and replace the matching ones
        out.append(sum(servers))                # ... and look at every server again
    return out


def with_state(server, replaced, new_id):
    """The same rules, carrying only what the next day needs."""
    count = {}                                  # id -> how many servers have it
    for x in server:
        count[x] = count.get(x, 0) + 1
    total = sum(server)                         # invariant: total == sum(id * count)
    out = []
    for old, new in zip(replaced, new_id):
        moved = count.pop(old, 0)               # READ the old group, and empty it
        if moved:
            count[new] = count.get(new, 0) + moved   # join (not overwrite) the new group
            total += moved * (new - old)        # each moved server changes by new - old
        out.append(total)
    return out


examples = [
    (([20, 10], [10, 20], [20, 1]), [40, 2]),
    (([3, 3], [3, 1], [1, 5]), [2, 10]),
    (([2, 5, 2], [2, 5, 3], [3, 1, 5]), [11, 7, 11]),
]
for args, want in examples:
    print(args, "->", with_state(*args))
    assert literal(*args) == with_state(*args) == want

rng = random.Random(7)
for _ in range(2000):
    n = rng.randint(1, 8)
    ids = [rng.randint(1, 5) for _ in range(n)]
    rep = [rng.randint(1, 6) for _ in range(n)]
    new = [rng.randint(1, 6) for _ in range(n)]     # old == new happens often here
    assert literal(ids, rep, new) == with_state(ids, rep, new), (ids, rep, new)
print("2000 random cases: the state version agrees with the literal one")

# the work each one does on the stated worst case, counted rather than timed
n = 10 ** 5
print("literal touches about", n * n * 2, "cells; the state version about", 3 * n)
big = [rng.randint(1, 9999) for _ in range(n)]
res = with_state(big, [rng.randint(1, 9999) for _ in range(n)],
                 [rng.randint(1, 9999) for _ in range(n)])
print("n = 100000 finished with the state version; last total:", res[-1])
```

### Each line, and which part of the idea it is

| line | in plain words | part of the idea |
|---|---|---|
| `count[x] = count.get(x, 0) + 1` | how many servers have each id | the state: counts, not positions |
| `total = sum(server)` | the one sum we ever compute in full | the redundant field, computed once |
| `for old, new in zip(...)` | one day at a time, in order | the loop over events |
| `moved = count.pop(old, 0)` | how many change, and empty their old group | read the old state first |
| `if moved:` | a missing id changes nothing | the "nothing happens" branch writes nothing |
| `count[new] = count.get(new, 0) + moved` | they join the new group | join, never overwrite |
| `total += moved * (new - old)` | the total moves by exactly the change | keeps the promise `total == sum(id * count)` |
| `out.append(total)` | answer from the state | the question is a read, never a scan |

Three lines carry the weight. `count.pop(old, 0)` is the subtle line: it reads
and clears the old group before anything new is written. `count.get(new, 0) +
moved` is the join from the second trace. And `total += ...` is the only place the
total changes, right next to the only place the counts change. If those two
writes were in different functions, the first rule you add later would update
one and forget the other.

Two boring confusions, settled.

**The `if moved:` guard.** Without it, a day that replaces a missing id would
create `count[new] = 0`, an empty group. That is harmless here (an empty group
contributes nothing), but it is a habit worth keeping: an event that changes
nothing should write nothing. In problems with "unknown user", "insufficient
funds", "booking rejected", the bug is always a failed event that wrote half of
its effect before failing.

**Why `list(server)` in the literal version.** The literal version edits the
list. Without the copy it would edit the caller's input, and the second function
called on the same input would see the edited list. Never mutate an input you
did not create, and a reference implementation least of all.

### The subtle line, both ways

The rule in the one-sentence summary was: **read the whole old state before
you write any of the new state.** Here it is on the input from the third trace.

```python run
def run(server, days, update, trace=True):
    count, total = {}, sum(server)
    for x in server:
        count[x] = count.get(x, 0) + 1
    out = []
    for old, new in days:
        total = update(count, total, old, new)
        out.append(total)
        if trace:
            print("   day %d -> %d: count %-14s total %d" % (old, new, dict(count), total))
    return out


def write_then_clear(count, total, old, new):     # looks fine, and is wrong
    moved = count.get(old, 0)
    count[new] = count.get(new, 0) + moved       # write the new group ...
    count[old] = 0                               # ... then clear the old one
    return total + moved * (new - old)


def clear_then_write(count, total, old, new):     # the order that is always right
    moved = count.pop(old, 0)                    # read and empty the old group first
    if moved:
        count[new] = count.get(new, 0) + moved
    return total + moved * (new - old)


server, days = [4, 4, 7], [(4, 4), (4, 1)]
print("clear, then write (right)")
right = run(server, days, clear_then_write)
print("write, then clear (wrong)")
wrong = run(server, days, write_then_clear)
assert right == [15, 9]          # day 2: two servers become 1, so 1 + 1 + 7
assert wrong == [15, 15]         # day 1 still looks right; day 2 is wrong
assert right[0] == wrong[0]      # the bug is invisible on the day it happens

# with old != new the two orders agree, which is why samples rarely catch it
for old, new in [(4, 7), (7, 2), (9, 4)]:
    assert run(server, [(old, new)], clear_then_write, False) == \
           run(server, [(old, new)], write_then_clear, False)
print("old != new: both orders agree; only old == new tells them apart")
```

Look at the printed count after day 1 of the wrong version: `{4: 0, 7: 1}`. The
total still says 15, the counts say 7. The promise `total == sum(id * count)` is
already broken, one day before any output is wrong. An assert of that promise
after every event would have stopped the program on day 1, at the line that
broke it. This is why you write the promise down.

Say the rule a second way. A transition is a function from the old state to the
new state. In maths, the new state is computed entirely from the old one; there
is no moment where the state is half old and half new. In code, you update
variables one at a time, so there *is* such a moment, and any read that happens
during it may see a value that is already new. The bug appears exactly when an
old value and a new value live in the same place: here, `count[old]` and
`count[new]` when old == new. On a grid, a cell and its neighbour when you update
in place (the Traps section shows that one). In knapsack, `dp[c - w]` when you
loop in the wrong direction. Same bug, three disguises.

The two safe ways to write any transition:

- **Read everything first, then write.** Compute every new value into local
  variables, then assign them. `moved = count.pop(old)` does this: the read and
  the clear happen together, before the write.
- **Write into a fresh copy.** Build the new state in a second structure and swap
  at the end. This is the standard for grids and boards ("double buffering").

### The general template

Every simulation in this chapter is this code, with a different state and
different handlers.

```python
def simulate(events):
    state = make_initial_state()          # the cut before the first event
    out = []
    for ev in events:                     # in the order the statement fixes
        kind, args = ev[0], ev[1:]
        result = HANDLERS[kind](state, *args)   # read old state, write new state
        if result is not None:
            out.append(result)            # only some events produce output
    return out
```

A dictionary of handlers rather than a chain of `if`s, because the multi-part
problems here (Part 1, Part 2, Part 3) grow by adding operations, and an `if`
chain grows by adding places to forget a counter.

## Why it is correct

What does it mean for the fast version to be "correct"? It means it prints what
the literal version prints, on every input. The literal version *is* the
specification. So the proof compares the two, step by step.

:::proof The state version produces the specified totals
**Setup.** Let A_j be the list of server ids after day j in the literal version
(A_0 is the input). Let count_j and total_j be the dictionary and total after day
j in the state version. Write #x(A) for the number of positions in A holding x.

**What we claim.** After every day j, for every id x, count_j[x] = #x(A_j) (with a
missing key meaning 0), and total_j = sum(A_j). Since both versions output the
total, they output the same numbers.

**Base case, j = 0.** The state version counts the input one element at a time,
so count_0[x] = #x(A_0) for every x, and it sets total_0 = sum(A_0). The claim
holds.

**Inductive step.** Assume the claim after day j - 1. Day j has rule (old, new).
Let k = #old(A_{j-1}), which by assumption equals count_{j-1}[old].

What the literal version does: every position holding `old` now holds `new`;
every other position is unchanged. So in A_j there are no positions holding old
(unless old == new), the positions holding new gained k, and the sum changed by
k x (new - old), because each of the k changed positions changed by exactly
new - old and no other position changed.

What the state version does: `moved = count.pop(old, 0)` sets moved = k and
removes the old group. If k = 0, nothing else happens, and indeed A_j = A_{j-1}.
If k > 0, it adds k to the group of `new` and adds k x (new - old) to the total.

Compare, id by id. For x different from old and new, neither version changes
anything. For x = old with old != new, both now have 0. For x = new with
old != new, both have the previous number plus k. For old == new, the state
version removed k and added k back, leaving k, and the literal list is unchanged,
also k. The totals both changed by k x (new - old). So the claim holds after day j.

**Conclusion.** By induction the claim holds after every day, and the outputs
are equal. Each day does a constant number of dictionary operations, so the loop
also finishes. ∎
:::

The proof has a shape you can reuse on every simulation, so it is worth naming.
There is a function that maps the literal world to the small state (here: from a
list to its counts and sum). Call it the **summary**. Two things must be true:

1. **The summary is enough to answer.** Every output can be computed from the
   summary alone. (The total is in the summary.)
2. **The summary moves with the events.** Summarising after the literal step
   gives the same thing as stepping the summary. (The inductive step above.)

If both hold, the fast simulation is correct, by exactly the induction above. If
the first fails, the state is too small. If the second fails, the transition is
wrong. "Too small" from Build it from the brute force is a failure of the first
condition: the total alone cannot answer "how many 2s are there?", which the next
transition needs.

The assumptions the proof used, in plain words, because each is a place a
variant breaks:

- **All servers with the old id are replaced together.** That is what lets
  positions be forgotten. If a rule said "replace the *first* server with id 3",
  position would matter again and the counts would not be enough.
- **The output depends only on the multiset of ids.** The total does. A question
  like "which server is third?" would not.
- **old == new is handled.** The proof had a separate line for it. The code
  handles it only because it reads (pops) before it writes.
- **Events happen in input order.** The induction is over days in order. Many
  statements fix the order explicitly ("process from left to right", "same-time
  arrivals in input order"); when they do, that sentence is part of the algorithm.

## What it costs

**The literal version.** Each day reads n cells to replace and n to sum, so m days
cost 2nm. With n = m = 10^5, about 2 x 10^10 steps. It does not finish.

**The state version.** Building the counts is n dictionary operations. Each day is
a pop, a get, a set, and some arithmetic: a constant number of operations. So the
total is O(n + m) expected time, about 3 x 10^5 steps for the worst case. The word
"expected" is there because dictionary operations are O(1) on average, not in the
worst case; for integer keys in Python that distinction never matters in
practice. See [[hash-tables]].

**Space.** The dictionary holds at most one key per distinct id, at most n keys.

**The general rule, and the costs people forget.** The cost of a simulation is a
sum over events of the cost of one event. Four things hide inside that sum.

- **A scan hiding in an event.** `sum(...)`, `len([x for x in ... if ...])`,
  `max(scores.values())`, `x in some_list`. Each looks like one line and costs
  the size of the state. One per event turns linear into quadratic. The fix is
  always the one in this chapter: keep the answer as a field and update it where
  the state changes.
- **Time steps versus events.** A loop that ticks the clock by one costs the
  length of the timeline, T. A loop that jumps from one event to the next costs
  the number of events, E. When T = 10^9 and E = 10^5, only one of those
  finishes. [[p:citadel-busy-intersection|Busy Intersection]] has arrival times up
  to 10^9; if both queues are empty, you jump the clock to the next arrival
  instead of ticking through the gap.
- **Amortised loops.** A `while` inside the event loop looks quadratic and often
  is not. In the queue problem in Variations, the inner loop that skips expired
  requests moves a pointer that only goes forward, so across the whole run it
  moves at most n times. The cost is a sum over the run, not a bound per event
  ([[amortized-analysis]]).
- **Copying the state for history.** Saving `dict(state)` after every event costs
  the size of the state each time. Store the event, not the state (Variation G).

## How to think about it

The template is short. The work is in deciding what goes in the state, and in
making the rules exact. Ask these questions, in this order, before writing code.

1. **What is one event?** Write its signature: `ADJUST(driver, delta)`,
   `day(old, new)`, `arrival(t)`, `command(ch)`. If the statement has a list of
   operation types, that list is your handler table.
2. **What does each event output, if anything?** Some events only write. Some
   only read. Often only one or two produce output.
3. **What is the least the next event needs to know about the past?** Name every
   field of the state, and for each, which event reads it. A field no event reads
   is waste. An event that needs something no field holds means the state is
   too small.
4. **Which fields are derived?** A total, a count, a "best so far", a "current
   maximum". Write the promise that ties each one to the primary fields, and make
   the single function that writes the primary field also update the derived one.
5. **What is the order?** Within one event: read the old state completely, then
   write. Between events: is it input order, time order, or priority order? At the
   same timestamp, which happens first, a departure or an arrival? A completion or
   a new request? The statement usually says. When it does not, ask.
6. **Simultaneous or one at a time?** "Every cell updates at once" (a board, a
   generation) means compute the new state from a frozen copy of the old one.
   "Process the requests in order" means each one sees the effect of the last.
7. **How does time move?** By ticks, or by jumps to the next event? Compare T, the
   length of the timeline, with E, the number of events.
8. **What do failed and odd events do?** Unknown id, duplicate registration,
   insufficient funds, a request with nothing in the queue, an empty input. The
   default for a failed event is: output the failure, change nothing.
9. **What exactly is the output format?** Strings with exact capitalisation, a
   `null` token, a comma-separated line. Simulations are graded on exact output.

Then, before coding, write down the state with one line per field and its promise,
and say for one event, in words, what it reads and what it writes. If you cannot,
you do not have the state yet.

### Telling it from its neighbours

- **State machines** ([[state-machines]]). A simulation whose state is one of a few
  named modes ("logged out", "logged in"; "open", "half-open", "closed") and whose
  events are symbols. Then the transition is a table, and drawing the table first
  catches the missing case.
- **Designing a data structure** ([[design-data-structure]]). The multi-part
  problems (an in-memory database, a banking system in four parts) are
  simulations whose state is a class you design. Each part adds a field and a rule.
- **Greedy and DP.** If the statement says "maximum", "minimum" or "fewest", and
  you choose the next step, it is not a simulation, even if it has a clock in it.
- **Matrix traversal** ([[matrix-traversal]]). Grid walks are simulations whose
  state is a position and a heading. The grid topics teach the movement; this one
  teaches the bookkeeping.
- **Parsing** ([[parsing]]). Many simulations start with turning text commands
  into events. If the hard part is the grammar (nested brackets, precedence), the
  topic is parsing; if the hard part is what the commands do, it is simulation.

## Variations

The roadmap lists five techniques for this node: stepping a state machine exactly
as described, walking a grid with direction arrays, parsing and tokenising a
string, processing events in time order, and keeping the bookkeeping straight.
Each is one or more of the variations below, and the folded-in topic, event logs
and replay, is G. A to E are everyday. F to H are regular. I and J are less common.

### A. A state machine stepped exactly as described

**What changes.** The state is a few named sets or modes, and every event has a
handful of outcomes, each with an exact message. The skill is listing every case.

**Why.** There is nothing to optimise; the risk is a missing branch. Write the
cases as a table before coding: for each command, the condition for success and
what changes on success, and the reminder that failure changes nothing.

**Example.** [[p:amazon-return-records|Return Records]]: `register`, `login`,
`logout`. The state is two things: a dictionary from username to password, and a
set of logged-in users. `login adam 1adam1` when the password is `1Adam1` fails
(passwords are case-sensitive) and, as the statement says, "a failed login does
not change an existing session". The case people miss: login of a user who is
already logged in also fails.

| command | succeeds when | on success |
|---|---|---|
| register u p | u not in passwords | passwords[u] = p |
| login u p | passwords.get(u) == p and u not in online | online.add(u) |
| logout u | u in online | online.remove(u) |

**Bank.** [[p:capital-one-leftmost-memory-block-allocator|Leftmost Memory Block Allocator]]
is a bigger table: an allocation id is consumed only on success, and erasing an
unknown or already-erased id outputs -1. Both rules are "failure changes nothing"
said twice.

### B. Walking a grid with direction arrays

**What changes.** The state is a position and a heading. A turn is arithmetic on
the heading; a move adds the heading's offset.

**Why.** Four `if heading == "N"` branches per command is four places to make a
sign error. Instead, store the headings in clockwise order, `"NESW"`, and the
offsets in two parallel arrays. Turning right is `d = (d + 1) % 4`, turning left is
`d = (d - 1) % 4` (in Python `%` is never negative), and moving is
`x += DX[d]; y += DY[d]`. The arrays are the only place a direction is described.

**Example.** [[p:shopify-mars-rover-robot-controller|Mars Rover Robot Controller]]:
start (0, 0) facing N, commands `MRMLM`. M goes to (0, 1). R faces E. M goes to
(1, 1). L faces N. M goes to (1, 2). Answer `1 2 N`.

**Two relatives.** A spiral walk ([[p:nike-spiral-matrix|Spiral Matrix]]) keeps
four shrinking boundaries, top, bottom, left, right, and walks one ring at a time.
The trap is the last ring when it is a single row or column: the bottom row must
be walked only if `top < bottom`, and the left column only if `left < right`,
or you walk the same cells back. And a rotation
([[p:visa-rotate-square-matrix-clockwise|Rotate a Square Matrix Clockwise]]) is not a
walk at all: it is a mapping, `out[r][c] = m[n-1-c][r]`, or "transpose, then
reverse each row". If you find yourself simulating cells moving one step at a
time to rotate, step back and write the index formula.
[[p:tiktok-sort-matrix-borders|Sort Matrix Borders]] reuses the spiral as a path
function: read one layer clockwise, sort the values, write them back along the
same path.

```python run
HEAD = "NESW"                       # clockwise, so "turn right" is +1
DX = [0, 1, 0, -1]                  # N: y + 1, E: x + 1, S: y - 1, W: x - 1
DY = [1, 0, -1, 0]


def rover(start, facing, commands):
    x, y = start
    d = HEAD.index(facing)
    for ch in commands:
        if ch == "R":
            d = (d + 1) % 4
        elif ch == "L":
            d = (d - 1) % 4         # Python's % is never negative: (0 - 1) % 4 == 3
        else:                       # "M": one step the way we face
            x, y = x + DX[d], y + DY[d]
    return "%d %d %s" % (x, y, HEAD[d])


def spiral(m):
    top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    out = []
    while top <= bottom and left <= right:
        out += [m[top][c] for c in range(left, right + 1)]               # top row
        out += [m[r][right] for r in range(top + 1, bottom + 1)]         # right column
        if top < bottom:                                                 # a 2nd row exists
            out += [m[bottom][c] for c in range(right - 1, left - 1, -1)]
        if left < right:                                                 # a 2nd column exists
            out += [m[r][left] for r in range(bottom - 1, top, -1)]
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return out


def rotate(m):                      # a mapping, not a walk: out[r][c] = m[n-1-c][r]
    n = len(m)
    return [[m[n - 1 - c][r] for c in range(n)] for r in range(n)]


print(rover([0, 0], "N", "MRMLM"))
assert rover([0, 0], "N", "MRMLM") == "1 2 N"
assert rover([0, 0], "N", "LLLL") == "0 0 N" and rover([0, 0], "N", "L") == "0 0 W"

grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print(spiral(grid))
assert spiral(grid) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
assert spiral([[1, 2, 3]]) == [1, 2, 3]                  # one row: no way back
assert spiral([[1], [2], [3]]) == [1, 2, 3]              # one column: no way up
for rows in range(1, 6):                                 # every cell exactly once
    for cols in range(1, 6):
        g = [[r * cols + c for c in range(cols)] for r in range(rows)]
        assert sorted(spiral(g)) == list(range(rows * cols)), (rows, cols)

sq = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(rotate(sq))
assert rotate(sq) == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
assert rotate(rotate(rotate(rotate(sq)))) == sq
transpose_then_flip = [list(row)[::-1] for row in zip(*sq)]
assert transpose_then_flip == rotate(sq)
print("rover, spiral and rotation agree with the examples and with themselves")
```

The loop over every rectangle from 1 x 1 to 5 x 5 is the test that matters for the
spiral. It checks the one property the guards exist for: every cell exactly once.
Delete either `if` and the 1 x 3 or 3 x 1 case fails.

### C. Parsing and tokenising the input

**What changes.** The events arrive as text, and turning text into events is half
the problem.

**Why.** Split on the separator, then check every token against exact rules, in a
small pure function per kind of token. A wrong parse looks like a wrong
simulation, and is much harder to find inside one.

**Example.** [[p:postman-validate-ip-address|Validate IP Address]]: IPv4 is exactly
four parts split on `.`, each all digits, no leading zero unless it is exactly `0`,
value at most 255. So `"172.16.254.1"` is IPv4, `"172.16.254.01"` is not (leading
zero), `"1.2.3"` is not (three parts), `"1..2.3"` is not (an empty part). The
order of checks matters: test "all digits" before converting to an integer, or
`int("+1")` will quietly accept a sign.

**Bank.** [[p:stripe-financial-account-ledger|Financial Account Ledger]] parses two
timestamp formats (`8` and `8,16`) and then applies cutoff and weekend rules; the
statement is long, and the way through it is one helper per rule, each tested
alone, so the main loop only says "parse, settle, apply".

### D. Processing events in time order

**What changes.** Events have timestamps, and the state includes a clock. The
cost question becomes: do I tick the clock, or jump it?

**Why.** Ticking is simple and costs the length of the timeline. Jumping costs the
number of events. And whichever you choose, the rule for *ties* (two things at
the same second) must be exactly the statement's.

**Example.** [[p:amazon-find-requests-in-queue|Find Requests in Queue]]: n requests
wait in a FIFO queue; request i expires at time wait[i] if not yet served. Each
second the front live request is served; it is still counted at that second and
leaves at the next. Report the queue length every second until it is empty. For
wait = [2, 2, 3, 1]:

| t | leaves now | expires now (wait == t) | in queue | served at t |
|---|---|---|---|---|
| 0 | | | 4 | request 0 |
| 1 | request 0 (served) | request 3 (wait 1) | 2 | request 1 |
| 2 | request 1 (served) | (requests 0 and 1 have wait 2, both already gone) | 1 | request 2 |
| 3 | request 2 (served) | | 0 | |

Output [4, 2, 1, 0]. The literal version removes expired requests by scanning the
queue every second, which is O(n) per second. The fast version asks the unlocking
question: what does second t need? Only which requests expire *at t*. So bucket
the requests by wait value once, and at second t look only at bucket t. A served
request is marked gone, so if it shows up in its expiry bucket later it is
skipped. The front pointer skips expired requests and only moves forward.

```python run
import random


def literal(wait):
    """Second by second, exactly as told: remove, count, serve."""
    queue = list(range(len(wait)))             # request indices, FIFO order
    out, t, served = [], 0, None
    while True:
        queue = [i for i in queue               # scan everyone, every second
                 if i != served and wait[i] > t]
        out.append(len(queue))
        if not queue:
            return out
        served = queue[0]                       # the front is processed at t
        t += 1


def bucketed(wait):
    """The same rules; each request is looked at O(1) times."""
    n = len(wait)
    expires = {}                                # second -> requests whose wait ends then
    for i, w in enumerate(wait):
        expires.setdefault(w, []).append(i)
    gone = [False] * n                          # served or expired
    alive, front, out, t, served = n, 0, [], 0, None
    while True:
        if served is not None:                  # last second's request leaves now
            alive -= 1
        for i in expires.get(t, ()):            # wait[i] == t: expired, unless served
            if not gone[i]:
                gone[i] = True
                alive -= 1
        out.append(alive)                       # count BEFORE serving: it counts at t
        if alive == 0:
            return out
        while gone[front]:                      # skip the expired at the front
            front += 1
        served, gone[front] = front, True       # serve the first live request
        t += 1


for wait, want in [([2, 2, 3, 1], [4, 2, 1, 0]), ([4, 4, 4], [3, 2, 1, 0]),
                   ([3, 1, 2, 1], [4, 1, 0]), ([1, 3, 1, 2], [4, 2, 0])]:
    print(wait, "->", bucketed(wait))
    assert literal(wait) == bucketed(wait) == want

rng = random.Random(11)
for _ in range(2000):
    w = [rng.randint(1, 7) for _ in range(rng.randint(1, 9))]
    assert literal(w) == bucketed(w), w
print("2000 random queues agree; the loop runs at most n + 1 seconds")
```

Why at most n + 1 seconds: every second either serves one request or ends the
loop, and there are n requests. Why the inner `while gone[front]` is cheap: front
only increases, and it can increase at most n times over the whole run.

**Ties, said explicitly.** In
[[p:roblox-event-id-check-completion-times|Event ID Check Completion Times]] a
check that finishes at the same second someone arrives is applied *first*: the
person already waiting starts, and the newcomer queues behind. Arrivals [0, 100,
300] with 300-second checks give finish times [300, 600, 900]: at t = 300 the first
check ends, the person from t = 100 starts, and the newcomer at 300 waits for 600.
Process "arrival first" instead and the newcomer sees one more person in the
queue than really there, which matters the moment the queue is near its limit.
In [[p:citadel-busy-intersection|Busy Intersection]] the priority at each second
depends on what happened the second before, so "previous second" is part of the
state, and idle gaps must be jumped, not ticked, because times go up to 10^9.

### E. Keeping the bookkeeping straight: counters instead of rescans

**What changes.** A question that sounds like it needs a scan ("is any row
complete?", "what is the total?") is answered from counters that each event
updates by a constant amount.

**Why.** That is the main derivation of this chapter in another costume.

**Example.** [[p:epic-first-mingo-line|First Completed Mingo Line]]: an n x n board
and a sequence of called numbers; report when a row, column or the main diagonal
is first complete. Rescanning the board after each call is n^2 per call, with up to
10^6 calls. Instead keep `row_hits[r]`, `col_hits[c]`, `diag_hits`, and a map from
value to cell. A call is three increments and three comparisons with n. The traps
are in the statement: a repeated call or a value not on the board still counts as
a call but marks nothing, so the increment must happen only the first time a cell
is marked.

**Ties and edges.** [[p:capital-one-rightmost-longest-character-run|Rightmost Longest Character Run]]:
on `"bbaacaa"` three runs have length 2, and the statement wants the rightmost,
`a2`. Comparing with `>` keeps the first maximum (`b2`), `>=` keeps the last. And
if you update the best only when a run ends, the last run never ends inside the
loop, so it must be closed after it. One character decides each of those.

### F. Round-robin with a queue

**What changes.** Units are handed out one at a time in a cycle, and some
participants drop out when satisfied.

**Why.** A queue models "go round again" exactly: pop the front, give one unit,
push it back if it still wants more.

**Example.** [[p:amazon-unfulfilled-bids-after-ranked-round-robin|Unfulfilled Bids after Ranked Round-Robin Allocation]]:
group bids by amount, highest first; within a group order by time then customer
id; give one unit per bid per cycle until the group is satisfied or stock runs
out. Since the total requested is at most 2 x 10^5, one unit per step is fine. If
it were 10^18 you would compute full cycles at once: with k bids still active and
s units left, s // k full cycles happen before anything changes.

### G. Event logs and replay (undo, redo, versions)

This is the topic folded into this chapter, and it turns the relation between
state and history around. Until now the state was the truth and the events were
thrown away. Here, **the log of events is the truth, and the state is what you
get by replaying the log from an empty start.** Everything follows from that.

- **Undo by replay.** Rebuild the state from the first k - 1 events. Always
  correct, costs O(k) per undo, and needs nothing special from the events.
- **Undo by inverse.** Store with each event the event that cancels it. O(1) per
  undo. `ADJUST(k, +5)` is cancelled by `ADJUST(k, -5)`. `SET(k, 7)` is cancelled
  by `SET(k, old)` only if you recorded `old` when you applied it. An event whose
  inverse you did not record cannot be undone without replay.
- **Redo** is a second stack. A new action clears it, because the future it
  described no longer exists.
- **Versioned reads.** "What was the value of key k at version v?" does not need a
  copy of the state per version. Keep, per key, a list of (version, value) pairs in
  increasing version order, and [[binary-search]] it. Memory is the number of
  writes, not versions times keys ([[persistent-structures]]).
- **Replay of a stream with duplicates.** If events can arrive twice, the
  transition must be idempotent or carry an id you deduplicate on.

```python run
import random


def apply_one(state, ev):
    """Apply ev to state; return the event that exactly undoes it."""
    kind, key, val = ev
    if kind == "ADJUST":
        state[key] = state.get(key, 0) + val
        return ("ADJUST", key, -val)
    old = state.get(key, 0)                 # SET is invertible only because we read this
    state[key] = val
    return ("SET", key, old)


class Ledger:
    def __init__(self):
        self.state, self.log, self.undone = {}, [], []

    def do(self, ev):
        self.log.append((ev, apply_one(self.state, ev)))
        self.undone.clear()                 # a new action kills the redo branch

    def undo(self):
        if self.log:
            ev, inv = self.log.pop()
            apply_one(self.state, inv)
            self.undone.append(ev)

    def redo(self):
        if self.undone:
            ev = self.undone.pop()
            self.log.append((ev, apply_one(self.state, ev)))

    def replay(self):                       # the state as a fold of the log
        s = {}
        for ev, _ in self.log:
            apply_one(s, ev)
        return s


def live(s):                                # a key holding 0 is the same as no key
    return {k: v for k, v in s.items() if v != 0}


led = Ledger()
for ev in [("ADJUST", "ana", 50), ("ADJUST", "bo", -20), ("SET", "ana", 7)]:
    led.do(ev)
print("after three events", led.state)
led.undo()
print("after one undo    ", led.state, " replayed:", led.replay())
assert led.state == {"ana": 50, "bo": -20}       # SET undone: ana is back to 50
led.redo()
assert led.state == {"ana": 7, "bo": -20}

rng = random.Random(3)
for _ in range(300):
    led = Ledger()
    for _ in range(rng.randint(0, 25)):
        r = rng.random()
        if r < 0.5:
            led.do((rng.choice(["ADJUST", "SET"]), rng.choice("abc"), rng.randint(-5, 5)))
        elif r < 0.8:
            led.undo()
        else:
            led.redo()
        assert live(led.state) == live(led.replay())
print("300 random do/undo/redo streams: the state always equals the replay of the log")
```

The replay is the reference implementation again, the same move as the literal
version of Get Total Requests: the slow, obviously correct version is kept to
test the fast one. Notice the `live` helper. After undoing every event, the
incrementally undone dictionary still holds keys mapped to 0, while the replay
never created them. They agree on every question the problem asks, and they are
different dictionaries. If a hidden test iterates your dictionary, that difference
is visible, so decide which one you mean.

### H. Lazy state: update only when someone looks

**What changes.** A quantity changes continuously (tokens refill, balances
accrue), but you only store its value at the last time you looked.

**Why.** No background ticking. Store `(value, last_time)`, and on each event add
`(now - last_time) x rate` before deciding. The clock advances only when an event
arrives. Rate limiters and token buckets are this ([[rate-limiting]]).

**Example.** A bucket of capacity 5 refilling 1 token per second, last seen at t = 2
with 1 token. A request at t = 6: refill to min(5, 1 + 4) = 5, take one, 4 left,
last time 6. Nothing ran between 2 and 6.

### I. Skipping ahead through a cycle (rare here)

**What changes.** The horizon T is huge, but the state space is small, so some
state must repeat.

**Why.** Record the step at which each state was first seen. When a state repeats
at step i, first seen at step j, the cycle length is i - j; skip
(T - i) // (i - j) whole cycles and simulate the remainder. This needs the state to
be hashable and complete; the proof's "summary is enough to answer" condition is
exactly what makes the skip legal. See [[cycle-detection]].

### J. Simulated concurrency (rare in assessments, common in design rounds)

Bounded queues, blocking caches, callback dispatch: you are asked to *simulate*
scheduling with a fake clock, not to start threads. The state is a set of waiters
and a deterministic rule for who wakes first. See [[concurrency]] and
[[producer-consumer]].

## Recognising it in a statement

Ordered by how much you should trust them.

1. **A list of typed operations, "process each in order".**
   `["ADJUST", driverId, delta]`, `"register user05 qwerty"`. The statement has
   handed you the handler table.
2. **A performance sentence attached to one operation.**
   [[p:rippling-driver-balance-ledger|Driver Balance Ledger]] ends with "the
   total-balance operation may be called very frequently, so it should not scan
   every driver on each call". That sentence names the field you must maintain.
   Read the last paragraph of every statement looking for it.
3. **"Part 1", "Part 2", "Part 3" in the title.** Staged problems are state
   design: each part adds a field and a rule. Write the dispatch table so a new
   part is a new handler.
4. **Rules written as bullets, with exceptions and an explicit tie-break.**
   "If an arrival occurs at the same time as a check finishes, apply that
   completion first." When the specification is this precise, it is the
   algorithm, and every clause is a branch.
5. **The vocabulary of time.** Ticks, rounds, turns, seconds, arrivals, cooldown,
   expiry, "at the moment of".
6. **The output is "the state after", or the values produced along the way**,
   rather than a maximum or a count of possibilities.
7. **Constraints that are large for the literal loop and small for one event.**
   10^5 events on 10^5 objects: the literal rescan is 10^10, so the problem is
   asking for a state that makes each event O(1) or O(log n).

**Disguised forms.** "Return the final position" (a walk), "how many requests
are in the queue at each second" (a queue with expiries), "which customers are
not fully served" (a round-robin), "return the matrix after every layer is sorted"
(a path function and a write-back). None says "simulate".

**Anti-signals.**

- **An optimum over choices**: "maximum", "minimum number of moves", "best
  order". That is search or optimisation.
- **A horizon with no matching event count**: 10^9 steps and n <= 100. Closed form,
  cycle, or exponentiation.
- **All queries and no updates**: answer offline, sorted.
- **A rule that depends on the whole future**: "a request is accepted if no later
  request..." cannot be decided at the moment it arrives. Process backwards or
  sort first.

## Traps

**Reading the state you are writing.** The subtle line. Symptom: the answer
depends on the order of statements inside one transition, or on the direction
you scanned a grid. On a board where "every cell updates at once", an in-place
update lets a cell see a neighbour that has already moved to the next
generation.

Here it is by hand on a row of five cells with the rule "a cell is on at the next
tick if it or a neighbour is on now". Start `1 0 0 0 0`. The right answer after
one tick is `1 1 0 0 0`: only cell 1 touches an on cell. A `*` marks a cell
written this tick.

| step, in place, left to right | reads | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|
| start | | 1 | 0 | 0 | 0 | 0 |
| cell 1 | cell 0, old 1 | 1 | 1* | 0 | 0 | 0 |
| cell 2 | **cell 1, NEW 1** | 1 | 1* | 1* | 0 | 0 |
| cell 3 | cell 2, NEW 1 | 1 | 1* | 1* | 1* | 0 |
| cell 4 | cell 3, NEW 1 | 1 | 1* | 1* | 1* | 1* |

At cell 2 the read lands on a starred cell. The infection crossed the whole row in
one tick. Scan right to left instead and you get `1 1 0 0 0`, the right answer,
by luck: the bug is still there, and a row that starts `0 0 0 0 1` exposes it.
Code that is only right in one scan direction is wrong. Use two grids.

**Overwriting where you meant to join.** `count[new] = moved` instead of
`count[new] += moved`. Symptom: right until two groups merge, as in the second
trace.

**A rejected event that still moved something.** The turned-away customer who
still advanced the clerk's clock; the failed allocation that still consumed an id.
Symptom: everything after the first failure is shifted. Make the failure branch
return before any write.

**A derived field that drifted.** A maintained total and the counts it
summarises; a "current best" and the scores. Symptom: correct for a hundred
operations, then wrong after a rare branch (a deletion, an overwrite, old ==
new). Cure: one function writes the primary field and updates the derived one in
the same place, and an assert of the promise during testing.

**`<` where the statement means `<=`.** "Expires when time = wait[i]" means a
request with wait 2 is gone at t = 2, so the live test is `wait[i] > t`. Symptom:
off by one only on inputs with ties.

**Mutating a collection while iterating it.** `for k in cache: if expired(k): del
cache[k]` raises an error on the first deletion. Collect the keys first, then
delete.

**Aliasing a snapshot.** `history.append(state)` stores a reference, so every
entry of the history is the final state. Append a copy, or better, append the
event.

**Exact output.** Lowercase `null`, "Logged In Successfully" with its capitals, a
comma-separated string. Symptom: a perfect algorithm marked wrong.

The in-place board, on real Game of Life rules, next to the two-grid version, and
the tie rule from Variation E:

```python run
def life_step(board, in_place):
    rows, cols = len(board), len(board[0])
    old = [row[:] for row in board]
    new = old if in_place else [row[:] for row in board]   # in place: read what we write
    for r in range(rows):
        for c in range(cols):
            live = sum(old[r + dr][c + dc]
                       for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                       if (dr or dc) and 0 <= r + dr < rows and 0 <= c + dc < cols)
            if old[r][c]:
                new[r][c] = 1 if live in (2, 3) else 0
            else:
                new[r][c] = 1 if live == 3 else 0
    return new


blinker = [[0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0]]
right = life_step(blinker, in_place=False)
wrong = life_step(blinker, in_place=True)
for name, b in (("two grids", right), ("one grid", wrong)):
    print(name)
    for row in b:
        print("   ", "".join(".#"[x] for x in row))
assert right[2] == [0, 1, 1, 1, 0] and sum(map(sum, right)) == 3   # the bar turns
assert sum(map(sum, wrong)) == 0                                   # everything died
assert life_step(right, False) == blinker                          # and turns back


def longest_run(s, tie_rightmost=True):
    best_ch, best_len, run = "", 0, 0
    for i, ch in enumerate(s):
        run = run + 1 if i and s[i - 1] == ch else 1
        if run > best_len or (tie_rightmost and run == best_len):
            best_ch, best_len = ch, run
    return best_ch + str(best_len)


print(longest_run("bbaacaa"), "(>= keeps the rightmost)",
      longest_run("bbaacaa", tie_rightmost=False), "(> keeps the leftmost)")
assert longest_run("bbaacaa") == "a2" and longest_run("bbaacaa", False) == "b2"
assert longest_run("bbacccdbbab") == "c3" and longest_run("z") == "z1"
```

Why the one-grid blinker dies, cell by cell in reading order. The top of the bar,
(1, 2), has one live neighbour, so it dies, and the code writes 0 there at once.
Then (2, 1), a dead cell, counts its neighbours: it should see three, (1, 2),
(2, 2) and (3, 2), and come alive. But (1, 2) already says 0, so it sees two and
stays dead. The same happens to (2, 3). The middle and the bottom then each have
too few neighbours and die. A pattern that should spin forever is wiped out in
one step, because one early write was read by four later cells.

The longest-run function updates the best at every character, not when a run
ends, which is the simplest way to never forget the last run.

## What to memorise

**The shape.** One state, one loop over events, one handler per event kind, each
handler reading the old state before writing the new one:

```python
state = initial()
out = []
for ev in events:
    result = HANDLERS[ev[0]](state, *ev[1:])
    if result is not None:
        out.append(result)
```

**The question.** *What is the least the next event needs to know about
everything that has happened so far?* Answer it field by field before typing. If
your answer contains "and then I look back at the earlier events", you have not
answered it.

**The habit.** Keep the literal version. It is two minutes of code, it is the
specification, and testing the fast version against it on a few thousand random
small inputs finds the old == new, the tie, and the failed-event bugs that the
samples do not contain. While testing, assert every derived field's promise
after every event.

**Numbers worth carrying.** 10^5 events with an O(n) scan inside each is 10^10
steps and does not finish; with O(1) per event it is 10^5. A ticking clock costs T,
an event-driven one costs E. A state space of size k run for more than k steps must
repeat.

## Check yourself

:::check
Trace the state version of Get Total Requests by hand on servers [3, 3, 8, 1],
with days (3 becomes 8), (9 becomes 2), (8 becomes 8), (8 becomes 1). Write the
count dictionary and the total after each day. Then run the "write the new
group, then clear the old" order on the same input and find the first day its
output is wrong.
--
Start: count {3: 2, 8: 1, 1: 1}, total 15.

Day 1, 3 becomes 8: moved = 2, count {8: 3, 1: 1}, total 15 + 2 x 5 = 25.
Day 2, 9 becomes 2: no server has id 9, moved = 0, nothing changes, total 25.
Day 3, 8 becomes 8: moved = 3, pop then add back, count {8: 3, 1: 1}, total
25 + 3 x 0 = 25.
Day 4, 8 becomes 1: moved = 3, count {1: 4}, total 25 + 3 x (1 - 8) = 4.

Output [25, 25, 25, 4]. Check: the literal list ends as [1, 1, 1, 1], sum 4.

The wrong order agrees on days 1 and 2. On day 3 it writes count[8] = 3 + 3 = 6
and then clears count[8] = 0; the total still says 25, so day 3 prints 25,
correct. On day 4 it moves count[8] = 0 servers and prints 25. The first wrong
output is day 4, but the state was already wrong after day 3.
:::

:::check
Trace [[p:amazon-find-requests-in-queue|Find Requests in Queue]] by hand for
wait = [1, 3, 1, 2]. For each second, write who leaves, who expires, the count,
and who is served.
--
t = 0: nobody leaves, nobody has wait 0. Count 4. Serve request 0.

t = 1: request 0 leaves (served at t = 0). Requests with wait 1 are 0 and 2;
request 0 is already gone, request 2 expires. Count 4 - 2 = 2 (requests 1 and 3).
Serve the front live request: request 1 (wait 3 > 1).

t = 2: request 1 leaves. Requests with wait 2: request 3, which was never served,
so it expires. Count 0. Stop.

Output [4, 2, 0]. Note that request 3 was in the queue at t = 1 but never reached
the front: request 1 took the only service slot that second.
:::

:::check
A rover starts at (2, 2) facing W and runs `LMMRMRRM`. Trace position and heading
after every command, using HEAD = "NESW", DX = [0, 1, 0, -1], DY = [1, 0, -1, 0].
--
W is index 3. L: (3 - 1) % 4 = 2, facing S. M: (2, 1). M: (2, 0). R: index 3,
facing W. M: (1, 0). R: index 0, facing N. R: index 1, facing E. M: (2, 0).

Final answer `2 0 E`. The turn from N to E is (0 + 1) % 4 = 1, and the turn from W
to S is (3 - 1) % 4 = 2; the arrays are the only place directions are described,
so no step needs an `if` on the heading.
:::

:::check
Write the spiral order of the 3 x 3 matrix [[1, 2, 3], [4, 5, 6], [7, 8, 9]] and of
the 2 x 3 matrix [[1, 2, 3], [4, 5, 6]]. For the 3 x 3, say what the boundaries
are on the second ring and which of the four edges are walked there.
--
3 x 3: 1, 2, 3, 6, 9, 8, 7, 4, then the second ring with top = bottom = 1 and
left = right = 1. The top row walks cell (1, 1), giving 5. The right column walks
rows top + 1 .. bottom, which is empty. `top < bottom` is false, so no bottom row;
`left < right` is false, so no left column. Answer 1, 2, 3, 6, 9, 8, 7, 4, 5.

2 x 3: top row 1, 2, 3; right column row 1: 6; bottom row right to left from
column 1: 5, 4; left column from row bottom - 1 = 0 down to top + 1 = 1, which is
empty. Answer 1, 2, 3, 6, 5, 4. The next ring has top = 1 > bottom = 0, so the loop
stops.
:::

:::check
Someone keeps only `total` for [[p:rippling-driver-balance-ledger|Driver Balance Ledger]]
and argues: "TOTAL is the expensive one, and I answer BALANCE by summing that
driver's ADJUST events, which I keep in a list." Where are they wrong, and what
is the right state?
--
They moved the scan rather than removing it. Summing a driver's adjustments on
each BALANCE costs the number of adjustments for that driver, and an adversary
can make every operation adjust one driver and then ask for its balance: O(n^2)
again.

The right state is a dictionary from driver to current balance, plus a total.
ADJUST(d, x) does balance[d] += x and total += x, in the same handler. BALANCE
reads balance.get(d, 0). TOTAL reads total. Every operation is O(1), and the
promise is total == sum(balance.values()). The unlocking question gives it
directly: BALANCE needs one driver's current number, TOTAL needs the sum, and
nothing needs the history.
:::

:::check
Why is "a dead cell with exactly three live neighbours comes alive" impossible to
implement correctly in place, in one grid of plain 0s and 1s scanned left to right, while
"replace every server with id 3 by id 8" is easy to do in place?
--
Because the board rule is simultaneous: every new cell is defined from the *old*
generation, and the old values of a cell are still needed by its neighbours
after the cell itself has been decided. With one grid, deciding a cell destroys
an old value someone else will read. You need a second grid, or an encoding that
keeps both (for example 2 = "was alive, now dead", 3 = "was dead, now alive", read
with `% 2` for the old value).

The server rule has no such dependency: whether a server becomes 8 depends only
on its own old id, not its neighbours, so overwriting it cannot spoil a later
read. The test for "can I update in place" is: does any later read need an old
value I am about to overwrite? In Get Total Requests that only happened in the
count version, when old == new, and the fix was to read before writing.
:::

:::check
A disguised one. "A garage holds at most 2 cars. Events, in order: `in A`, `in B`,
`in C`, `out C`, `out A`, `in C`, `out B`, `in D`. A car arriving when the garage is
full is turned away. Report the number of cars inside after every event." What is
the state, what does each event read and write, and what is the output? Which
event is the trap?
--
State: the set of plates inside (and its size). `in x` reads the size: if it is
2, x is turned away and *nothing is written*; otherwise x is added. `out x` reads
whether x is inside: if it is, remove it; if it is not (it was turned away, or never
came), nothing changes.

| event | inside after | count |
|---|---|---|
| in A | {A} | 1 |
| in B | {A, B} | 2 |
| in C | full, turned away | 2 |
| out C | C is not inside: no change | 2 |
| out A | {B} | 1 |
| in C | {B, C} | 2 |
| out B | {C} | 1 |
| in D | {C, D} | 2 |

Output [1, 2, 2, 2, 1, 2, 1, 2]. The trap is `out C` at step 4. A state that is only
a counter decrements it to 1, and from then on every count is one too low:
[1, 2, 2, 1, 0, 1, 0, 1]. Worse, the garage now believes it has room it does not
have, so a later arrival that should be turned away is let in. The counter
alone is "too small": two histories, "C inside" and "C turned away", both give
count 2, and `out C` treats them differently. The rejected event must write
nothing, and the later event about it must be able to tell.
:::
