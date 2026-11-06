# Shortest Paths: the Map

> Every shortest-path algorithm repeats one move, "if going through u is a cheaper way to reach v, write that down", and the algorithms differ only in the order they make that move, an order that is safe because of what the edge weights promise.

## The problem it solves

Five towns, A to E, and two-way roads with travel times in minutes:

| road | A-B | A-C | C-B | B-D | C-D | D-E | C-E |
|---|---|---|---|---|---|---|---|
| minutes | 4 | 1 | 2 | 1 | 5 | 3 | 8 |

You live in A. How long does it take to reach each town?

The answers are A 0, C 1, B 3, D 4, E 7. B is reached by A-C-B (1 + 2), not by the
direct road (4). D is reached by A-C-B-D (1 + 2 + 1), not by A-C-D (6). E is reached
by A-C-B-D-E (7), four roads long, not by the two-road route A-C-E (9).

That last answer is the whole subject in miniature. **The cheapest route is not the
one with the fewest roads.** So the first tool a beginner reaches for, [[bfs]], is
wrong here. BFS visits towns in order of how many roads away they are: it reaches B
and C at one road, and D and E at two. It reaches E by the road C-E and would report
9, and the truth is 7, along a route of four roads that BFS never prefers.

The second tool a beginner reaches for is to try every route. From A, walk every
path that does not repeat a town, add up the minutes, and keep the smallest per
town. That is correct, and for five towns it is fine. It stops being fine fast. With
n towns all joined to each other, the number of routes from one town to another that
never repeat a town is (n-2)! · (1 + 1/1! + 1/2! + ...), about 2.7 · (n-2)!. For 12
towns that is about 9.8 million routes; for 20 towns, about 1.7·10^16. The bank's
plain shortest-path problem,
[[p:visa-dijkstra-weighted-undirected-graph|Dijkstra Shortest Paths in a Weighted
Undirected Graph]], allows 100,000 towns and 200,000 roads.

This chapter is called "the map" because shortest paths are a family, and the
family is organised by **what the weights promise**. Here is the map. The rest of
the chapter derives every entry.

| what the weights are | algorithm | cost |
|---|---|---|
| all equal (or no weights) | [[bfs]] | O(V + E) |
| only 0 and 1 | 0-1 BFS (a deque) | O(V + E) |
| any non-negative numbers | [[dijkstra]] (a heap) | O((V + E) log V) |
| some negative, or "at most k edges" | [[bellman-ford]] | O(V · E), or O(k · E) |
| you need every pair, V up to ~400 | [[floyd-warshall]] | O(V³) |
| the graph has no cycles (a DAG) | relax in [[topological-sort]] order | O(V + E) |

### When it is the wrong tool

- **The graph is a grid you may only cross right and down.** Then there are no
  cycles, and a [[dp-2d]] table over the cells is simpler. As soon as moves go in all
  four directions, cycles appear and you need this chapter.
  [[p:visa-minimum-cost-weighted-grid-path|Minimum-Cost Path Through a Weighted
  Grid]] is exactly the four-direction case.
- **The question is whether a route exists, not how long it is.** That is
  connectivity: [[dfs]], [[bfs]], or [[union-find]].
- **The route's cost is its single worst edge, and you have every edge up front.**
  That is a bottleneck path; it has a Dijkstra form (variation D) and a Union-Find
  form, and both are fine.
- **You want the longest simple path in a general graph.** That is NP-hard. No
  version of this chapter solves it. (In a DAG it is easy; see variation I.)

## Build it from the brute force

We will start from the slowest correct program, find its waste, and fix it one step
at a time. Dijkstra, Bellman-Ford and 0-1 BFS will each appear as the cure for a
specific waste, under a specific promise about the weights.

### Step 1: try every route

The brute force is a [[backtracking]] walk: from the current town, try every road to a
town not yet on this route, and when you arrive somewhere, compare the total with the
best seen for that town.

```
walk(town, cost, on_route):
    best[town] = min(best[town], cost)
    for (next, minutes) in roads[town]:
        if next not in on_route:
            walk(next, cost + minutes, on_route + {next})
```

It is correct because every route that does not repeat a town is tried, and a
cheapest route never needs to repeat a town when no weight is negative (a repeat
would be a loop, and a loop costs at least 0). Count it as above: about 2.7 · (n-2)!
routes on a fully connected graph. Factorial.

### Step 2: notice the waste

On our map, the walk reaches C twice from A: directly (cost 1) and via B (cost 4 + 2
= 6). From each arrival at C it then explores everything beyond C again: C-D, C-E,
C-B and all their continuations. But think about what the second arrival at C can
possibly achieve. Any route that continues from C after arriving at cost 6 has a
twin that continues the same way after arriving at cost 1, and the twin is 5
cheaper. The expensive arrival is useless.

### The question that unlocks it

That observation is the whole field. Ask:

**What does the rest of the route need to know about how you got here?**

The answer: only **where you are**. Not which towns you passed, not in what order.
The roads out of C are the same whichever way you came in. And among all the ways of
getting to C, only the cheapest matters, because anything that can be done after an
expensive arrival can be done after the cheap one, for less.

So the state is the town, and each town needs one number:

> dist[v] = the cost of the cheapest route from the start to v.

That is the same move as in [[knapsack]], where the question was "what is the least
the future needs to know about the past?" and the answer collapsed 2^n subsets into
(items, capacity) states. Here it collapses factorially many routes into V towns.

Say it a second way. The brute force carries the whole history of the route. The
future reads only the last line of that history, "I am at C, it cost me 1", and of
all the histories ending at C, only the cheapest one is worth continuing.

When the state needs more than the town, the same question tells you what to add.
If you may use a discount at most twice, the future needs to know how many you have
left, so the state is (town, discounts left). That is variation E, and it is still
this chapter.

### The equation, and why it is not a recursion

If dist[v] is the cheapest route to v, then the last road of that route came from
some neighbour u, and the part before it was a cheapest route to u. So:

```
dist[start] = 0
dist[v]     = min over roads (u -> v, w) of dist[u] + w
```

Every shortest-path algorithm is a way of solving this equation. In knapsack, the
same kind of equation was solved by recursion with a memo, because each state
depended on strictly smaller states. Here that fails.

### You might think: "memoise it like a DP"

Write `dist(v) = min(dist(u) + w for each road u-v)` as a memoised recursion and call
`dist(B)`. It asks `dist(A)`, `dist(C)` and `dist(D)`. `dist(C)` asks `dist(B)`,
which is still being computed. The recursion either loops forever or, if you return
"infinity" for a state in progress, returns an answer computed from a placeholder.
The roads go both ways, so the states depend on each other in a cycle. There is no
"smaller first" order to fill a table in.

### You might think: "a DFS with a visited set will do it"

This is the most common wrong first program. Run a DFS from A, mark each town visited
the first time you reach it, and record the cost at that moment. Suppose A's list has
the road to B first. The DFS goes A-B (cost 4) and marks B. B's first road leads to C,
so it goes B-C (4 + 2 = 6) and marks C. From C it goes to D (6 + 5 = 11), from D to E
(14). When it finally backs up to A and tries the road A-C, cost 1, C is already
visited, and the road is refused. Final: B 4, C 6, D 11, E 14. The truth is 3, 1, 4, 7.
Even C, one road of cost 1 from home, was frozen at 6.

The bug is in the word "first". DFS reaches a town first by whatever road it happened
to try first, and that is not the cheapest. Marking it visited freezes a wrong answer.
A visited set is right for BFS on unweighted graphs, because there the first arrival
is provably the closest. With weights, "first arrival" and "cheapest arrival" are
different things, and **the entire job of a shortest-path algorithm is to know when
they coincide.**

### Step 3: the move that every algorithm shares

We cannot solve the equation in one pass, but we can approach it. Start with the
promise "dist[v] is the cost of some real route to v, or infinity", and improve it
one road at a time:

```
relax(u -> v, w):
    if dist[u] + w < dist[v]:
        dist[v] = dist[u] + w          # a cheaper route to v: through u
```

This is called **relaxing** the road. It never makes dist wrong: if dist[u] is the
cost of a real route to u, then dist[u] + w is the cost of a real route to v. It can
only lower values, never raise them, and never below the truth. So if we relax
enough roads in a good enough order, dist reaches the true costs and stops changing.

The question is the order. There are three good answers.

### Step 4: relax everything, again and again (Bellman-Ford)

The simplest order is no order: relax every road, then do it again, until a whole
pass changes nothing. How many passes can it take?

Look at the passes carefully, keeping the values from the start of each pass apart
from the ones being written (we will see in a moment why that matters):

- After pass 1, every town reachable by **one** road has the cost of its cheapest
  one-road route.
- After pass 2, every town has the cost of its cheapest route **using at most two
  roads**, because such a route is a route of at most one road followed by one more
  road, and pass 2 relaxed that last road from a value pass 1 had already fixed.
- After pass i, dist[v] is the cheapest route using at most i roads.

A cheapest route never repeats a town (no negative loops to gain from), so it uses at
most V - 1 roads. So V - 1 passes are enough. Each pass touches every road once:
**O(V · E)**. That is Bellman-Ford. It is slow, but it asks nothing of the weights
except that there is no loop of negative total cost, and it has a superpower the
others lack: pass i is exactly "at most i roads". That is why it solves "cheapest
flight with at most k stops" (variation C).

On our map, the passes give:

| after pass | A | B | C | D | E | new routes found |
|---|---|---|---|---|---|---|
| 0 | 0 | ∞ | ∞ | ∞ | ∞ | |
| 1 | 0 | 4 | 1 | ∞ | ∞ | A-B, A-C |
| 2 | 0 | 3 | 1 | 5 | 9 | A-C-B, A-B-D, A-C-E |
| 3 | 0 | 3 | 1 | 4 | 8 | A-C-B-D, A-B-D-E |
| 4 | 0 | 3 | 1 | 4 | 7 | A-C-B-D-E |

The answer for E improves in every pass, because its cheapest route has four roads.
Pass 4 is V - 1, and it is the last one that can change anything.

### Step 5: notice the waste again

Bellman-Ford relaxes every road in every pass, even roads out of towns whose value has
not changed, and even roads out of towns that are already final. A is final from the
start, and its roads are relaxed four times. C is final after pass 1. What we would
love is an order where **every town is relaxed from exactly once, at a moment when its
value is already final**. Then each road is relaxed once, and the work is about E.

When is a value certainly final? Look at the table after pass 1: B 4, C 1. C is the
smallest value not yet known to be final. Could some other route to C be cheaper than
1? Any other route leaves A by some road and passes through some town other than C
first. The only such towns are reached at cost at least 4 (B). If the remaining roads
cost nothing or more, that route costs at least 4, which is not less than 1. So C is
final at 1.

That argument is the whole of Dijkstra. Among the towns not yet final, **the one with
the smallest current value is final**, provided that no road has negative cost. Any
other route to it would have to leave the final set through some other non-final
town, which already costs at least as much, and then travel roads that cannot make it
cheaper.

So: repeatedly take the non-final town with the smallest value, declare it final,
and relax its roads once. To find "the smallest value" fast, keep the candidates in a
[[heap]]. That is Dijkstra's algorithm.

### You might think: "Dijkstra is BFS with a heap, so mark a town done when you push it"

Push means "I found some route to it"; pop means "this is the cheapest candidate
left". Only the pop is final. On our map, popping A pushes B at 4 and C at 1. If you
mark B done at the push, then when C is popped and finds C-B costing 1 + 2 = 3, B is
already done, and B stays 4. That is the DFS bug again, with a heap around it. Mark a
town final when it is **popped**, and skip any later pop of a town already final.

### You might think: "negative weights are fine, the heap will sort it out"

Roads A→B 2, A→C 3, C→B −2, B→D 1. Dijkstra pops A, pushes B 2 and C 3. It pops B at 2
and declares it final, relaxes B→D: D = 3. It pops C at 3 and finds C→B costs 1, less
than 2, but B is final, so the improvement is either refused or written without ever
being passed on to D. D stays 3; the truth is 1 + 1 = 2.

The proof "any other route already costs at least as much" assumed that roads cannot
make a route cheaper. A negative road breaks exactly that sentence. With negative
weights, use Bellman-Ford.

(If you drop the "final" rule and simply re-push a town whenever its value drops,
the code above gives the right D on this input. But it is no longer Dijkstra: a town
can be popped many times, and there are graphs where this takes exponential time.
Do not rely on it.)

### Step 6: when the weights are only 0 and 1, the heap is overkill (0-1 BFS)

Dijkstra pops values in non-decreasing order. Suppose every road costs 0 or 1. When
the smallest value in the heap is d, every value in it is d or d + 1: anything pushed
came from a popped town at most d, plus 0 or 1. Two distinct values do not need a heap.
A **deque** keeps them in order for free: a road of cost 0 gives a value d, equal to
the front, so push it on the **front**; a road of cost 1 gives d + 1, push it on the
**back**. The deque stays sorted, every operation is O(1), and the whole thing is
O(V + E). That is 0-1 BFS.

And when every road costs 1, every push goes on the back: that is plain BFS with a
queue. BFS, 0-1 BFS and Dijkstra are one algorithm with three different containers.

### The technique in one sentence

**Keep the best-known cost to every node, and improve it by relaxing edges, in an
order that the weights make safe: smallest-first with a heap when weights are
non-negative, a deque when they are 0 or 1, and round after round when they may be
negative or the number of edges is limited.**

The question that produced it: **what does the rest of the route need to know about
how you got here?** Only where you are (plus whatever extra the rules make the future
depend on), and only the cheapest way of getting there.

## Worked by hand

### Dijkstra on the five towns

<svg viewBox="0 0 640 260" role="img" aria-label="five towns: A at the left, B above and C below in the middle-left, D in the middle-right, E at the right. Roads A-B 4, A-C 1, C-B 2, B-D 1, C-D 5, D-E 3, C-E 8. The cheapest-route tree A-C, C-B, B-D, D-E is drawn thick; the other roads are dashed. Final costs: A 0, C 1, B 3, D 4, E 7.">
  <g>
    <line x1="60" y1="130" x2="230" y2="50" stroke-dasharray="6 5"/>
    <line x1="60" y1="130" x2="230" y2="210" stroke-width="4"/>
    <line x1="230" y1="210" x2="230" y2="50" stroke-width="4"/>
    <line x1="230" y1="50" x2="400" y2="130" stroke-width="4"/>
    <line x1="230" y1="210" x2="400" y2="130" stroke-dasharray="6 5"/>
    <line x1="400" y1="130" x2="570" y2="130" stroke-width="4"/>
    <line x1="230" y1="210" x2="570" y2="130" stroke-dasharray="6 5"/>
    <circle class="fill" cx="60" cy="130" r="20"/>
    <text x="60" y="136" text-anchor="middle">A</text>
    <circle cx="230" cy="50" r="20"/>
    <text x="230" y="56" text-anchor="middle">B</text>
    <circle cx="230" cy="210" r="20"/>
    <text x="230" y="216" text-anchor="middle">C</text>
    <circle cx="400" cy="130" r="20"/>
    <text x="400" y="136" text-anchor="middle">D</text>
    <circle cx="570" cy="130" r="20"/>
    <text x="570" y="136" text-anchor="middle">E</text>
    <text x="135" y="80" text-anchor="middle">4</text>
    <text x="135" y="190" text-anchor="middle">1</text>
    <text x="245" y="135">2</text>
    <text x="320" y="80" text-anchor="middle">1</text>
    <text x="305" y="160" text-anchor="middle">5</text>
    <text x="485" y="120" text-anchor="middle">3</text>
    <text x="470" y="185" text-anchor="middle">8</text>
    <text x="60" y="172" text-anchor="middle">0</text>
    <text x="230" y="20" text-anchor="middle">3</text>
    <text x="230" y="250" text-anchor="middle">1</text>
    <text x="400" y="100" text-anchor="middle">4</text>
    <text x="570" y="100" text-anchor="middle">7</text>
  </g>
</svg>

The picture shows the end state: the thick roads are the cheapest-route tree, and the
number next to each town is its final cost. Now the same thing as it happens, with
the heap after every pop. Each heap entry is (cost, town). "Stale" means the popped
cost is larger than the town's current dist, so the entry is an old, beaten offer.

| pop | final? | relaxations (dist[u] + w vs dist[v]) | dist A B C D E | heap after |
|---|---|---|---|---|
| (0, A) | A = 0 | B: 0+4 < ∞, write 4. C: 0+1 < ∞, write 1 | 0 4 1 ∞ ∞ | (1,C) (4,B) |
| (1, C) | C = 1 | A: 1+1 not < 0. B: 1+2 = 3 < 4, write 3. D: 1+5 = 6 < ∞. E: 1+8 = 9 < ∞ | 0 3 1 6 9 | (3,B) (4,B) (6,D) (9,E) |
| (3, B) | B = 3 | A: no. C: no. D: 3+1 = 4 < 6, write 4 | 0 3 1 4 9 | (4,B) (4,D) (6,D) (9,E) |
| (4, B) | stale: 4 > 3 | skip | 0 3 1 4 9 | (4,D) (6,D) (9,E) |
| (4, D) | D = 4 | B: no. C: 4+5 not < 1. E: 4+3 = 7 < 9, write 7 | 0 3 1 4 7 | (6,D) (7,E) (9,E) |
| (6, D) | stale: 6 > 4 | skip | 0 3 1 4 7 | (7,E) (9,E) |
| (7, E) | E = 7 | C: no. D: no | 0 3 1 4 7 | (9,E) |
| (9, E) | stale: 9 > 7 | skip | 0 3 1 4 7 | empty |

Here is the second pop in words, because it is the step that beats the direct road.

> I pop (1, C). Nothing in the heap is smaller than 1, and every road costs at least 0,
> so no route can reach C for less than 1: C is final. Now I look at C's roads, once.
> The road to B costs 2, so going through C reaches B for 1 + 2 = 3. B's best so far
> is 4, from the direct road. 3 is less, so I write dist[B] = 3 and push (3, B). I do
> not remove the old (4, B) from the heap; it is too expensive to find. It will come
> out later, I will see that 4 is more than dist[B], and I will throw it away.

Three things the trace shows that the code alone would not.

**The heap holds offers, not towns.** B was in the heap twice, at 4 and at 3. The
cheaper one comes out first and wins; the dearer one is popped later and discarded by
the line `if d > dist[u]: continue`. Removing it early would need a heap with a
"decrease key" operation; Python's `heapq` has none, so we leave it and skip it.

**Towns become final in order of cost, not of distance in roads.** The order is A,
C, B, D, E: costs 0, 1, 3, 4, 7, always non-decreasing. E, four roads away, comes last,
and its first offer (9, via the direct C-E road) was beaten before it was ever popped.

**The final dist values are the same as Bellman-Ford's pass 4.** Same equation, same
answer, but Dijkstra relaxed every road out of each town exactly once: 14 relaxations
(the sum of the degrees), against Bellman-Ford's 4 passes of 14.

### A second trace: at most k flights, and why each round must read the old values

Four airports, one-way flights with prices:

| flight | 0→1 | 1→2 | 2→0 | 1→3 | 2→3 |
|---|---|---|---|---|---|
| price | 100 | 100 | 100 | 600 | 200 |

Cheapest from 0 to 3 **with at most one stop**, that is, at most two flights. The
routes are 0→1→3 (700, two flights) and 0→1→2→3 (400, three flights, too many). The
answer is 700. This is [[p:inmobi-cheapest-flights-within-k-stops|Cheapest Flights
Within K Stops]].

Bellman-Ford's pass i is "cheapest with at most i flights", so run k + 1 = 2 passes and
read dist[3]. But only if each pass reads the values from **before** the pass. Here
are both ways, relaxing the flights in the order listed. A `*` marks a value written in
this pass.

**Reading a copy from before the pass (correct).**

| pass | reads from | 0→1 | 1→2 | 2→0 | 1→3 | 2→3 | dist after |
|---|---|---|---|---|---|---|---|
| 1 | [0, ∞, ∞, ∞] | 0+100: dist[1] = 100* | prev[1] = ∞: no | ∞: no | prev[1] = ∞: no | ∞: no | [0, 100*, ∞, ∞] |
| 2 | [0, 100, ∞, ∞] | 100 not < 100 | 100+100: dist[2] = 200* | prev[2] = ∞: no | 100+600: dist[3] = 700* | prev[2] = ∞: no | [0, 100, 200*, 700*] |

**Reading the array as it is being written (wrong here).**

| pass | 0→1 | 1→2 | 2→0 | 1→3 | 2→3 | dist after |
|---|---|---|---|---|---|---|
| 1 | dist[1] = 100* | **reads dist[1] = 100, written a moment ago**: dist[2] = 200* | no | dist[3] = 700* | **reads dist[2] = 200***: dist[3] = 400* | [0, 100*, 200*, 400*] |
| 2 | no change | no change | no | no | no | [0, 100, 200, 400] |

Point at the second column of the wrong table. In pass 1, the relaxation of 1→2 reads
dist[1], and dist[1] has a star: it was written by the flight 0→1 in the same pass. So
"one flight" has already become "two flights". Then 2→3 reads dist[2], which has a
star, and the pass has chained three flights. After one pass, the in-place version
reports 400, a three-flight route, and no later pass can take it back.

So the in-place loop does not compute garbage. It computes the cheapest route with
**no limit** on the number of flights, sometimes reaching it in fewer passes. For plain
Bellman-Ford that is a free speed-up, and the in-place version is the normal one. For
"at most k edges" it is the bug. This is the same line as the loop direction in the
one-row knapsack: the update must read the previous round, and in a single array you
only get the previous round if you protect it. Here, by copying.

### A third, short trace: 0-1 BFS

[[p:google-minimum-direction-violations|Minimum Direction Violations]]: every listed
road is one-way, driving with it costs 0 and against it costs 1. Roads 0→1, 2→1, 2→3,
4→0, 3→4; from 0 to 3. Deque entries are (cost, node).

| pop | relaxations | dist 0..4 | deque after |
|---|---|---|---|
| (0, 0) | 0→1 with the road: 0, **front**. 0→4 against 4→0: 1, back | 0 0 ∞ ∞ 1 | (0,1) (1,4) |
| (0, 1) | 1→2 against 2→1: 1, back | 0 0 1 ∞ 1 | (1,4) (1,2) |
| (1, 4) | 4→3 against 3→4: 2, back | 0 0 1 2 1 | (1,2) (2,3) |
| (1, 2) | 2→3 with the road: 1 + 0 = 1 < 2, **front** | 0 0 1 1 1 | (1,3) (2,3) |
| (1, 3) | nothing cheaper | 0 0 1 1 1 | (2,3) |
| (2, 3) | stale: 2 > 1 | | empty |

Answer 1: 0→1 with the road, 1→2 against one road, 2→3 with the road. Look at the
fourth pop: the 0-cost relaxation put (1, 3) on the front, ahead of the older (2, 3),
and the deque stayed sorted without any comparison. That is the whole trick.

## From the idea to the code

### The direct versions: brute force, the wrong DFS, and Bellman-Ford

```python run
INF = float("inf")
NAMES = "ABCDE"
ROADS = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3), (2, 4, 8)]

def adjacency(n, roads):
    adj = [[] for _ in range(n)]
    for u, v, w in roads:
        adj[u].append((v, w)); adj[v].append((u, w))       # two-way roads
    return adj

def every_route(adj, s):                                   # Step 1: the brute force
    best, routes = [INF] * len(adj), [0]
    def walk(u, cost, seen):
        routes[0] += 1
        best[u] = min(best[u], cost)
        for v, w in adj[u]:
            if v not in seen:
                walk(v, cost + w, seen | {v})
    walk(s, 0, {s})
    return best, routes[0]

def dfs_first_arrival(adj, s):                             # the wrong instinct
    dist, seen = [INF] * len(adj), {s}
    dist[s] = 0
    def go(u):
        for v, w in adj[u]:
            if v not in seen:
                seen.add(v); dist[v] = dist[u] + w; go(v)
    go(s)
    return dist

def bellman_ford(n, roads, s):                             # Step 4
    arcs = [(u, v, w) for u, v, w in roads] + [(v, u, w) for u, v, w in roads]
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):                                 # at most n-1 roads per route
        changed = False
        for u, v, w in arcs:
            if dist[u] + w < dist[v]:                      # relax
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break                                          # a pass changed nothing: done
    return dist

adj = adjacency(5, ROADS)
truth, count = every_route(adj, 0)
print("brute force :", dict(zip(NAMES, truth)), "after", count, "partial routes")
print("DFS, first  :", dict(zip(NAMES, dfs_first_arrival(adj, 0))))
print("Bellman-Ford:", dict(zip(NAMES, bellman_ford(5, ROADS, 0))))
assert truth == [0, 3, 1, 4, 7] == bellman_ford(5, ROADS, 0)
assert dfs_first_arrival(adj, 0) == [0, 4, 6, 11, 14]     # froze A-B, A-B-C, ...

for n in range(3, 10):                                     # the factorial, measured
    full = [(u, v, 1) for u in range(n) for v in range(u + 1, n)]
    _, c = every_route(adjacency(n, full), 0)
    print("complete graph on", n, "towns:", c, "partial routes")
assert c == 109601                                         # n = 9: 1 + 8 + 8*7 + ... + 8!
```

The DFS line is the instinct from the derivation, run: it reached B first by the
direct road and froze it at 4, then reached C through B and froze it at 6, and
everything beyond inherited the error. The last
loop shows the brute force's count: 109,601 partial routes for nine towns, growing by a
factor of about n each time.

### The optimised version: Dijkstra with a heap

```python run
import heapq, random

def dijkstra(adj, s, trace=None):
    dist = [float("inf")] * len(adj)
    dist[s] = 0
    heap = [(0, s)]                                  # offers: (cost, node)
    while heap:
        d, u = heapq.heappop(heap)                   # the cheapest offer left
        if d > dist[u]:
            if trace is not None: trace.append((d, u, "stale"))
            continue                                 # an old, beaten offer
        if trace is not None: trace.append((d, u, "final"))
        for v, w in adj[u]:                          # u is final: relax its edges once
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist

def adjacency(n, roads):
    adj = [[] for _ in range(n)]
    for u, v, w in roads:
        adj[u].append((v, w)); adj[v].append((u, w))
    return adj

ROADS = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3), (2, 4, 8)]
adj = adjacency(5, ROADS)
for lst in adj:
    lst.sort()                                       # same neighbour order as the table
trace = []
dist = dijkstra(adj, 0, trace)
for d, u, what in trace:
    print("pop (%d, %s): %s" % (d, "ABCDE"[u], what))
print("dist:", dict(zip("ABCDE", dist)))
assert dist == [0, 3, 1, 4, 7]
assert [("ABCDE"[u], what) for _, u, what in trace] == [
    ("A", "final"), ("C", "final"), ("B", "final"), ("B", "stale"),
    ("D", "final"), ("D", "stale"), ("E", "final"), ("E", "stale")]

def bellman_ford(n, roads, s):
    dist = [float("inf")] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in roads:
            for a, b in ((u, v), (v, u)):
                if dist[a] + w < dist[b]:
                    dist[b] = dist[a] + w
    return dist

rng = random.Random(3)
for _ in range(400):                                 # agree on random graphs
    n = rng.randint(1, 8)
    roads = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9))
             for _ in range(rng.randint(0, 14))]
    assert dijkstra(adjacency(n, roads), 0) == bellman_ford(n, roads, 0), roads
print("400 random graphs with weights 0..9: Dijkstra equals Bellman-Ford")
```

### Each line, and which part of the idea it is

| line | in plain words | in the derivation |
|---|---|---|
| `dist = [inf] * n; dist[s] = 0` | nothing reached yet, except the start at 0 | the promise: every value is a real route or ∞ |
| `heap = [(0, s)]` | the only offer is "start, for free" | candidates for "smallest non-final" |
| `d, u = heapq.heappop(heap)` | the cheapest offer left | Step 5: the smallest non-final value is final |
| `if d > dist[u]: continue` | this offer was beaten after it was made | lazy deletion; also how "already final" is detected |
| `for v, w in adj[u]` | u is final, relax its edges, once | each edge is relaxed from its final end only |
| `if d + w < dist[v]` | does going through u beat v's best? | the relaxation from Step 3 |
| `dist[v] = d + w; heappush(...)` | write it down, and offer it | a new, cheaper offer for v |

Three lines do the work: the pop, the stale check, and the relaxation. Settle the
boring confusions now.

- **Where is the "visited" set?** It is `dist` itself. A node is final exactly when an
  offer equal to its dist is popped. The first such pop processes it; any later pop
  of that node has `d > dist[u]`, or equal if a tie was pushed twice, and in the tie
  case relaxing again changes nothing, so it is harmless. If you prefer, keep a
  `done` array and `continue` when `done[u]`; set it right after the pop, never at
  push time.
- **Why `d + w` and not `dist[u] + w`?** After the stale check they are equal. Using d
  makes it obvious that you are extending the popped offer.
- **Why push `(dist[v], v)` and not `(v, dist[v])`?** The heap orders tuples by their
  first element. The cost must come first.
- **What about unreachable nodes?** They stay at infinity. Convert to -1 only at the
  end, if the problem asks; never put -1 into dist, because -1 is less than every
  real cost and would be "relaxed" from.

### The subtle line, both ways: copy the previous round

Bellman-Ford's "at most k edges" depends on one line, `prev = dist[:]`. The second
trace showed it on paper. Here it is run, with the array after every relaxation and a
`*` on values written during the current pass.

```python run
INF = float("inf")
FLIGHTS = [(0, 1, 100), (1, 2, 100), (2, 0, 100), (1, 3, 600), (2, 3, 200)]

def show(d, fresh):
    return "[" + ", ".join(("inf" if x == INF else str(x)) + ("*" if i in fresh else "")
                           for i, x in enumerate(d)) + "]"

def at_most(n, flights, src, edges, copy, trace=True):
    dist = [INF] * n
    dist[src] = 0
    for p in range(1, edges + 1):
        prev = dist[:] if copy else dist         # THE line: read the old round, or not
        fresh = set()
        for u, v, w in flights:
            if prev[u] + w < dist[v]:
                dist[v] = prev[u] + w
                fresh.add(v)
                if trace:
                    tag = "NEW" if (not copy and u in fresh) else "old"
                    print("  pass %d  %d->%d reads %s dist[%d]  -> %s"
                          % (p, u, v, tag, u, show(dist, fresh)))
    return dist

print("copy the previous pass (correct for 'at most 2 flights'):")
good = at_most(4, FLIGHTS, 0, 2, True)
print("update in place:")
bad = at_most(4, FLIGHTS, 0, 2, False)
assert good[3] == 700                            # 0->1->3, two flights
assert bad[3] == 400                             # 0->1->2->3, three flights: too many

def unlimited(n, flights, src):                  # plain Bellman-Ford, no limit
    dist = [INF] * n
    dist[src] = 0
    for _ in range(n - 1):
        for u, v, w in flights:
            dist[v] = min(dist[v], dist[u] + w)
    return dist

print("no limit at all:", unlimited(4, FLIGHTS, 0))
assert bad == unlimited(4, FLIGHTS, 0)           # in place = the unlimited answer
assert at_most(4, FLIGHTS, 0, 3, True, False)[3] == 400   # allow 3 flights: now legal
```

Read the in-place output. In pass 1, the line for 1→2 says it reads a NEW value of
dist[1]: that is the moment one pass became two flights. The final asserts say what the
wrong version computes: exactly the unlimited answer. And with a limit of three
flights, the correct version reaches 400 too, because now the three-flight route is
allowed.

There is a second subtle line, in Dijkstra: where a node becomes final. It must be at
the pop, not at the push. The DFS demonstration in the first block is that bug in its
purest form, and the Traps section runs the "mark at push" version on the same map.

### 0-1 BFS, and the three containers

```python run
from collections import deque
import heapq, random

def zero_one_bfs(n, roads, s, trace=False):
    adj = [[] for _ in range(n)]
    for u, v in roads:
        adj[u].append((v, 0))                    # with the road: free
        adj[v].append((u, 1))                    # against it: one violation
    dist = [float("inf")] * n
    dist[s] = 0
    dq = deque([(0, s)])
    while dq:
        d, u = dq.popleft()
        if d > dist[u]:
            continue                             # stale, as in Dijkstra
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                if w == 0:
                    dq.appendleft((dist[v], v))  # same cost as the front: front
                else:
                    dq.append((dist[v], v))      # one more: back
        if trace:
            print("  pop", u, "dist", dist, "deque", list(dq))
    return dist

roads = [(0, 1), (2, 1), (2, 3), (4, 0), (3, 4)]
dist = zero_one_bfs(5, roads, 0, trace=True)
print("violations from 0 to 3:", dist[3])
assert dist == [0, 0, 1, 1, 1]

def dijkstra(n, roads, s):
    adj = [[] for _ in range(n)]
    for u, v in roads:
        adj[u].append((v, 0)); adj[v].append((u, 1))
    dist, heap = [float("inf")] * n, [(0, s)]
    dist[s] = 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist

rng = random.Random(5)
for _ in range(300):
    n = rng.randint(1, 9)
    rs = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 15))]
    assert zero_one_bfs(n, rs, 0) == dijkstra(n, rs, 0)
print("300 random 0/1 graphs: the deque gives Dijkstra's answers")
```

### Which one to type

Dijkstra with a heap is the default; it handles every non-negative case, including 0/1,
at the price of a log. Type 0-1 BFS when the weights are exactly 0 and 1 and the graph
is large (a grid of 10^6 cells), or when the interviewer asks for linear time. Type
Bellman-Ford only for negative weights or a limit on the number of edges. And type plain
BFS whenever every edge costs the same; it is Dijkstra with the heap replaced by a
queue, because every offer goes on the back.

## Why it is correct

:::proof Dijkstra settles every node at its true distance; Bellman-Ford's pass i is "at most i edges"
**Words.** Let δ(v) be the true cost of a cheapest path from s to v (∞ if none). A node
is **final** once it has been popped with d = dist[v] for the first time.

**Fact 1: dist never goes below the truth.** At the start, dist[s] = 0 = δ(s) and every
other value is ∞. Each write sets dist[v] = dist[u] + w where dist[u] is the cost of a
real path to u, so dist[v] is the cost of a real path to v, and no real path costs less
than δ(v). So dist[v] ≥ δ(v) always. This holds for every algorithm in the chapter,
with any weights.

**Claim (Dijkstra, weights ≥ 0): when u becomes final, dist[u] = δ(u).**

Suppose not, and let u be the **first** node that becomes final with dist[u] > δ(u).
Then u ≠ s (s is final at 0 = δ(s)), and u is reachable, so take a cheapest path P from
s to u. Walk along P from s. s is final; u is not yet final. So somewhere P steps from a
final node x to a non-final node y for the first time (possibly y = u).

- x became final before u, so by the choice of u, dist[x] = δ(x). When x became final,
  the algorithm relaxed the edge x→y, so from then on dist[y] ≤ δ(x) + w(x, y).
- The part of P from s to y is a cheapest path to y (a cheaper one could replace it and
  make P cheaper). So δ(x) + w(x, y) = δ(y). Together: dist[y] ≤ δ(y), and by Fact 1,
  dist[y] = δ(y). So the heap holds an offer (δ(y), y).
- The rest of P, from y to u, has no negative edges, so δ(y) ≤ δ(u). **This is the only
  place non-negativity is used.**
- u was popped while (δ(y), y) was still in the heap (y is not final yet; if y = u, this
  is u's own offer), and the heap pops the smallest, so dist[u] ≤ δ(y).

Chain them: dist[u] ≤ δ(y) ≤ δ(u) < dist[u]. A number cannot be less than itself, so no
such u exists. Every node is final at its true distance, and since every reachable node
eventually receives an offer and is popped, every reachable node becomes final.

**Termination.** Each relaxation that pushes lowers some dist value, and a node pushes
offers only when it is final, which happens once per node. So there are at most E
pushes, and the loop pops each at most once.

**Claim (Bellman-Ford with a copy): after pass i, dist[v] = the cheapest cost of a walk
from s to v using at most i edges** (call it δ_i(v)).

*Base, i = 0.* dist[s] = 0 and all others ∞: with zero edges you can only be at s.

*Step.* Assume after pass i - 1, dist = δ_{i-1}. A walk of at most i edges to v is either
a walk of at most i - 1 edges (cost δ_{i-1}(v), which dist[v] already holds), or a walk
of at most i - 1 edges to some u followed by the edge u→v (best cost δ_{i-1}(u) + w).
Pass i reads `prev[u]`, which is δ_{i-1}(u), for every edge into v, and keeps the
minimum. So after the pass, dist[v] = δ_i(v). The copy is what makes `prev` equal to
δ_{i-1}: without it, prev[u] might already be δ_i(u), and the pass would allow i + 1
edges or more.

*Consequence.* If no cycle has negative total cost, a cheapest walk can drop any cycle
without getting dearer, so some cheapest walk is a simple path with at most V - 1 edges:
δ_{V-1} = δ. Hence V - 1 passes suffice. If a V-th pass still lowers some value, some
walk with V edges beats every shorter one, so it repeats a node and contains a cycle
of negative cost reachable from s.

**0-1 BFS** is Dijkstra with a different container. If the deque is sorted with values in
{d, d+1} when an offer of value d is popped, then a 0-edge offer has value d and goes to
the front, a 1-edge offer has value d + 1 and goes to the back, and the deque is still
sorted with values in {d, d+1} (or {d+1, d+2} once the d's run out). So it always pops
the smallest offer, which is all the Dijkstra proof used. ∎
:::

The proofs used these assumptions. Each is where a variant breaks or a bug hides.

- **The future depends only on the node.** The cheapest-path-to-y step ("a cheaper way
  to y could replace it") assumes the rest of the route does not care how you reached y.
  If it does (discounts left, flights used, fuel price), the node is not the state, and
  you must enlarge it until the sentence is true again (variation E).
- **Extending a route never makes it cheaper.** That is "weights ≥ 0" for sums, and it is
  exactly what other cost rules need too: for a route's cost being its largest edge
  (max(d, w) ≥ d), or a product of probabilities at most 1 (p · q ≤ p), the same proof
  works with the heap ordered the right way (variation D).
- **Costs combine by adding (or by another operation that respects order).** The step
  "δ(x) + w = δ(y)" needs the subpath of a best path to be best. If the cost could
  reward a worse prefix, it fails.
- **For Bellman-Ford's limit, each pass reads only the previous pass.** That is the copy.
- **For Bellman-Ford's V - 1, no negative cycle is reachable.** Otherwise there is no
  shortest walk at all; costs fall forever.

## What it costs

**Dijkstra with a binary heap and lazy deletion.** Count the pushes. A push happens only
during a relaxation from a node at the moment it becomes final, and each node becomes
final once, so each directed edge pushes at most once: at most E pushes (2E for an
undirected graph stored both ways), plus the start. Each push and each pop costs
O(log of the heap size), and the heap holds at most E + 1 entries, so log E ≤ 2 log V.
Total: **O((V + E) log V)**. For the bank's 10^5 nodes and 2·10^5 edges, that is about
4·10^5 heap operations of ~18 levels each, comfortable in Python.

**The hidden log, and when to avoid it.** On a dense graph, E is about V², and the heap
version costs O(V² log V). The original array version of Dijkstra, which scans all
non-final nodes for the minimum, costs O(V²) and is faster there. With V = 1,000 points
all joined to each other, that is the difference between 10^6 and 2·10^7 steps.

**Bellman-Ford.** V - 1 passes over E edges: **O(V · E)**. For V = 10^5 and E = 2·10^5
that is 2·10^10, hopeless; it is a tool for small graphs or for the "at most k edges"
case, where it is **O(k · E)** plus O(V) per pass for the copy. Cheapest Flights has
V ≤ 100 and at most V(V-1)/2 flights, so at most 100 passes of 4,950 flights: half a
million steps.

**0-1 BFS and BFS.** Each edge is relaxed at most twice in total and each deque
operation is O(1): **O(V + E)**.

**State graphs.** When the state is (node, extra), the number of states is V times the
number of values of the extra, and the edges multiply the same way. Discounts up to 20
on 10^4 nodes and 5·10^4 edges give 2.1·10^5 states and about 2·10^6 directed
transitions, with a log on top. Always multiply this out before you choose a state.

**Space.** The graph as adjacency lists, O(V + E); dist, O(V); the heap, O(E) in the lazy
version.

**The costs people forget.**

- **Building the graph.** For a grid, do not build adjacency lists; compute the four
  neighbours on the fly. For "points that are connected if close", building the edges
  can be the real cost.
- **Tuple pushes in Python.** Each heap push allocates a tuple. On 10^6 operations that
  matters; it is still fine for 10^5-scale graphs.
- **Infinity.** `float("inf")` mixes floats and ints in the heap. That is fine in Python;
  in a typed language, use a large integer and beware of INF + w overflowing.

## How to think about it

Ask these, in this order, on every problem that asks for a cheapest, fastest, or fewest.

1. **What are the nodes?** Towns, cells, airports, or states such as (cell, keys held),
   (city, discounts left), (lock combination). The unlocking question decides:
   **what does the rest of the route need to know about how I got here?** Everything it
   needs goes into the node.
2. **What are the edges, and what does each cost?** A move, a flight, a turn of a dial.
   Is the graph directed? Are costs on edges, or on entering a node (then it is the cost
   of every edge into that node)?
3. **What do the weights promise?** All equal: BFS. Only 0 and 1: 0-1 BFS. Non-negative:
   Dijkstra. Some negative: Bellman-Ford. This one question picks the algorithm.
4. **Is there a limit on the number of edges?** "At most k stops": Bellman-Ford with k + 1
   copied passes, or Dijkstra over (node, edges used).
5. **How does a route's cost combine?** Sum: the usual. Largest edge (minimise the worst):
   Dijkstra with max. Smallest edge (maximise the weakest): Dijkstra with min and a max-heap.
   Product of probabilities: Dijkstra with a max-heap. Check that extending a route can
   never improve it; if it can, the greedy pop order is unsafe.
6. **One source, one target, all pairs, or many sources?** Many sources: push them all at
   cost 0 (a super-source). One target and many sources: reverse the edges and run from
   the target. All pairs with V ≤ 400: [[floyd-warshall]].
7. **What is the size?** Multiply V and E by the state factor. Then check the cost table
   above.

Then, before typing, write four lines: **the node in words**, **the edges and their
costs**, **the start values**, and **which dist value is the answer**. If any of them is
unclear, code will not make it clear.

### Telling it from its neighbours

- **[[bfs]].** Shortest paths when every edge costs the same. If someone gives you
  weights that are all 1, do not reach for a heap.
- **[[dp-2d]] and other DPs.** If the moves only go forward (right and down, or along a
  DAG), there is no cycle, and a table in a fixed order is the shortest-path algorithm.
  [[topological-sort]] gives that order for a general DAG.
- **[[union-find]] and [[minimum-spanning-tree]].** A minimax path (minimise the largest
  edge) between two nodes always lies on a minimum spanning tree, and Kruskal's order
  answers it: add edges cheapest first until the two nodes connect. So variation D has
  two correct solutions.
- **[[binary-search-on-answer]].** "Minimise the largest edge" can also be solved by
  guessing a limit and checking reachability with BFS. Slower by a log, but sometimes
  simpler when the check is complicated.
- **[[minimum-spanning-tree]] itself.** "Connect everything as cheaply as possible" is not
  a shortest path. The MST minimises the total of the chosen edges; shortest paths
  minimise the cost of each route from the source. Prim's algorithm looks like Dijkstra,
  with dist[v] = w instead of dist[u] + w.

## Variations

Eleven variations. A to E are the core of interview and assessment problems, and every
one has a problem in this bank. F, G, H are regular. I and J are less common. K is rare.

### A. Dijkstra with a heap: the default

**What changes.** Nothing; this is the template. The usual disguises are in the edges: a
grid where entering a cell costs its value, or an edge list with a twist.

**Why.** Non-negative costs are what make "smallest offer is final" true.

**Example.** A 2 x 2 grid [[1, 3], [1, 1]] where entering a cell costs its value,
including the start: right then down costs 1 + 3 + 1 = 5, down then right costs 1 + 1 + 1
= 3. Dijkstra from the top-left starts at dist 1 (the start cell's own cost) and finishes
at 3.

**Bank.** [[p:visa-dijkstra-weighted-undirected-graph|Dijkstra Shortest Paths in a
Weighted Undirected Graph]] is the template with parallel edges and self-loops (both
harmless). [[p:visa-minimum-cost-weighted-grid-path|Minimum-Cost Path Through a Weighted
Grid]] is the grid version, with -1 for blocked cells: skip them as neighbours, and
check that both endpoints are open. [[p:salesforce-path-with-maximum-probability|Path With
Maximum Probability]] multiplies probabilities and wants the largest: push negated values
(or use a max-heap), relax with `p * q > best[v]`, and the proof still works because
multiplying by a number in [0, 1] never increases a probability.

### B. 0-1 BFS: only two costs

**What changes.** A deque instead of a heap; cost-0 relaxations go on the front, cost-1 on
the back.

**Why.** The live offers only ever take two values, d and d + 1.

**Example.** The direction-violation trace above. Another common shape: a grid where each
cell has an arrow, following the arrow costs 0 and changing it costs 1.

**Bank.** [[p:google-minimum-direction-violations|Minimum Direction Violations]] (with the
road 0, against it 1), and [[p:google-minimum-teleporter-repairs|Minimum Teleporter
Repairs]], where the cost sits on the **departure** node: every edge leaving a broken
country costs 1, every other edge 0. Moving the cost onto the edges is the whole
modelling step.

### C. Bellman-Ford, and "at most k edges"

**What changes.** Passes over all edges. For a limit of k edges (k - 1 stops), exactly k
passes, each reading a copy of the previous one.

**Why.** Pass i is exactly "at most i edges" when it reads the previous pass (the proof).

**Example.** The flights trace: 700 with at most two flights, 400 with three.

**Bank.** [[p:inmobi-cheapest-flights-within-k-stops|Cheapest Flights Within K Stops]],
with k stops meaning k + 1 flights.

**Negative edges and negative cycles.** The other use of Bellman-Ford. Run V - 1 passes; if
a V-th pass still improves anything, a negative cycle is reachable from the source and
"shortest" is undefined there. No problem in this bank needs negative weights; it is
here because the interview follow-up "what if weights can be negative?" is common, and
the answer is "Dijkstra's proof breaks at one line; use Bellman-Ford, O(V · E), and
detect negative cycles with one extra pass".

**An alternative for the limit.** Dijkstra over states (node, flights used), with
flights used ≤ k + 1. It is faster on large sparse graphs and needs care: a state with
more flights but lower cost is not dominated, so you cannot keep one dist per node.

### D. Minimax and maximin paths: the route is as bad as its worst edge

**What changes.** The cost of a route is not a sum but its largest edge (or its smallest,
for "the strongest bridge"). Relax with `max(d, w)` instead of `d + w`. For a maximin,
use a max-heap and `min(d, w)`.

**Why.** Extending a route can never lower its maximum: max(d, w) ≥ d. That is the
"extending never helps" assumption, so the Dijkstra proof goes through unchanged.

**Example.** Edges 1-2 weight 5, 2-3 weight 1, 1-3 weight 7. The sum-cheapest route from 1
to 3 is 1-2-3 (6) with worst edge 5; the direct road has worst edge 7. Minimax answer 5.

**Bank.** [[p:walmart-minimum-stress-path|Minimum Stress Path]] is that example's shape:
the stress of a path is its heaviest edge. [[p:google-swim-in-rising-water|Swim in Rising
Water]] is the grid form, where the cost is the tallest cell you touch, so dist[start] is
the start cell's height and relaxation is max(d, height[v]).
[[p:amazon-find-safest-path-in-grid|Find the Safest Path in a Grid]] is the maximin form,
after a [[multi-source-bfs]] from every thief computes each cell's safeness.

The same questions have a Union-Find answer (add edges from cheapest up until the
endpoints connect), and a binary-search answer (guess the limit, check with BFS). All
three are correct; Dijkstra is the one that needs no sort and no second idea.

### E. Dijkstra over states: the node plus what the future needs

**What changes.** The node becomes a tuple. Every transition says how the extra part
changes. dist is indexed by the whole state.

**Why.** The unlocking question. If the rest of the route depends on something besides the
node, two arrivals at the same node are not interchangeable, and the proof's "replace the
prefix with a cheaper one" step fails until that something is in the state.

**Example.** Roads 0-1 (10), 1-2 (10), 0-2 (25), one discount that halves one road
(rounded down). Without the discount: 20. With it: 0-2 at 12, or 0-1-2 at 5 + 10 = 15. The
state (node, discounts used) finds 12: from (0, 0), taking 0-2 discounted leads to
(2, 1) at cost 12.

**Bank.** [[p:skyscanner-minimum-path-with-discounts|Minimum Path Cost with Edge
Discounts]] is exactly that, with up to 20 discounts. [[p:microsoft-minimum-fuel-cost|Minimum
Fuel Cost Between Cities]] is a harder stretch: with an unlimited tank, you always pay the
cheapest price seen so far for every unit, so the state is (city, cheapest price so far).

```python run
import heapq

def minimax(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w)); adj[v].append((u, w))
    best = [float("inf")] * n
    best[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > best[u]:
            continue
        for v, w in adj[u]:
            nd = max(d, w)                         # the route is as bad as its worst edge
            if nd < best[v]:
                best[v] = nd
                heapq.heappush(heap, (nd, v))
    return best[t]

def with_discounts(n, edges, s, t, k):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w)); adj[v].append((u, w))
    INF = float("inf")
    dist = [[INF] * (k + 1) for _ in range(n)]     # dist[node][discounts used]
    dist[s][0] = 0
    heap = [(0, s, 0)]
    while heap:
        d, u, used = heapq.heappop(heap)
        if d > dist[u][used]:
            continue
        if u == t:
            return d                               # the first pop of any (t, *) is best
        for v, w in adj[u]:
            for nd, nu in ((d + w, used), (d + w // 2, used + 1)):
                if nu <= k and nd < dist[v][nu]:
                    dist[v][nu] = nd
                    heapq.heappush(heap, (nd, v, nu))
    return -1

E1 = [(0, 1, 5), (1, 2, 1), (0, 2, 7)]
print("minimax 0 -> 2:", minimax(3, E1, 0, 2))
assert minimax(3, E1, 0, 2) == 5                   # via 0-1-2, worst edge 5, not 7

E2 = [(0, 1, 10), (1, 2, 10), (0, 2, 25)]
for k in range(3):
    print("discounts", k, "->", with_discounts(3, E2, 0, 2, k))
assert [with_discounts(3, E2, 0, 2, k) for k in range(3)] == [20, 12, 10]
```

Check the last value by hand: two discounts allow 0-1-2 at 5 + 5 = 10, which beats 0-2 at
12. With one discount, 0-2 halved (12) beats 0-1-2 with one road halved (15). Note what the
state buys: with one discount, there are two arrivals at node 1, cost 5 with the discount
spent and cost 10 with it still in hand. They are different situations, because only the
second can halve a later road. A dist per node would keep the 5 and forget that the 10
exists; dist[node][used] keeps both.

### F. Many sources, one target, and the reversed graph

**What changes.** For "distance to the nearest of several sources", push every source at
cost 0 before starting. For "every node's distance to one target" on a directed graph,
reverse every edge and run once from the target.

**Why.** A super-source joined to every source by free edges is equivalent, and pushing
them all at 0 is what its first pop would do. Reversing edges turns paths into the target
into paths out of it.

**Example.** Two hospitals, at nodes 0 and 4 of a line 0-1-2-3-4 with unit roads: every
node's distance to the nearest hospital is [0, 1, 2, 1, 0], in one run.

**Bank.** The follow-ups of [[p:google-minimum-direction-violations|Minimum Direction
Violations]] ask for exactly this super-source and super-sink.
[[p:amazon-find-safest-path-in-grid|Find the Safest Path in a Grid]] uses the unweighted
form, [[multi-source-bfs]].

### G. Which edges lie on a shortest path: the shortest-path DAG

**What changes.** Run Dijkstra once; then an edge u→v of weight w is on some shortest path
from the source exactly when dist[u] + w = dist[v]. Those edges form a DAG, and you can
count shortest paths or collect predecessors by walking it in order of dist.

**Why.** A path is shortest exactly when every edge on it is "tight", that is, satisfies
the equality.

**Example.** On the five towns, tight edges: A-C (0 + 1 = 1), C-B (1 + 2 = 3), B-D (3 + 1 = 4),
D-E (4 + 3 = 7). A-B is not tight (0 + 4 ≠ 3). One shortest path to each town.

**Bank.** [[p:mathworks-shortest-route-possible-predecessors|Cities on Shortest Delivery
Routes]]: for each city, count the cities that lie on at least one shortest route to it,
which is a walk backwards over tight edges.

### H. Recovering the route

**What changes.** Keep `parent[v] = u` whenever a relaxation through u improves v. At the
end, walk parent pointers back from the target and reverse.

**Why.** The last improving relaxation of v is the last edge of its final cheapest route.

**Example.** Five towns: parent B = C, D = B, E = D, C = A. From E: E, D, B, C, A, reversed
A-C-B-D-E.

### I. Directed acyclic graphs: relax in topological order

**What changes.** No heap. Sort the nodes topologically and relax each node's edges once, in
that order. Negative weights are fine, and the **longest** path is just as easy (flip
min to max).

**Why.** In topological order, every edge into v has been relaxed before v is used, which is
the Bellman-Ford argument done in one pass.

**Example.** Tasks with durations and prerequisites: the earliest finish time is a longest
path in the DAG. That is [[topological-sort]]'s scheduling variant.

### J. All pairs: Floyd-Warshall

**What changes.** A V x V table, and a triple loop over an intermediate node k, then i, then j:
`d[i][j] = min(d[i][j], d[i][k] + d[k][j])`.

**Why.** After round k, d[i][j] is the best path using only intermediates from 0..k. The
k loop must be outermost; that is its subtle line.

**When.** V ≤ about 400, or many queries between arbitrary pairs. Otherwise, run Dijkstra
from each source that is actually asked about. See [[floyd-warshall]].

### K. The rare tools

- **Dial's algorithm.** Weights are small integers up to C: an array of C + 1 buckets
  replaces the heap, O(V·C + E).
- **A\*.** Dijkstra with the heap ordered by dist plus an estimate of the remaining cost
  that never overestimates; it explores fewer nodes toward one target. Common in games,
  rare in interviews.
- **Johnson's algorithm.** All pairs with negative edges: one Bellman-Ford to re-weight,
  then Dijkstra from every node.
- **Bidirectional search.** Run from both ends and stop when the frontiers meet; same
  answers, often far fewer nodes.

## Recognising it in a statement

Ordered by how reliable they are.

1. **"Minimum cost / time / price / effort to get from X to Y"** with weighted moves.
   Shortest path. Now read the weights to choose which.
2. **"At most k stops / edges / moves"** next to a cost. Bellman-Ford's passes, or a state
   with a counter.
3. **"Changing direction / breaking a wall / repairing costs 1, otherwise free".** 0-1 BFS.
4. **"The cost of a path is its maximum (or minimum) edge or cell".** Minimax Dijkstra
   (or Union-Find in sorted order).
5. **"You may use a coupon / discount / key / power-up at most k times".** State Dijkstra:
   (node, uses left).
6. **"Fewest moves", unweighted.** BFS, not Dijkstra.
7. **"Probability of success along the path is the product".** Dijkstra with a max-heap.

### Disguises

- **The nodes are not given.** A lock with four dials (each state is a node, each turn is
  an edge), words that differ by one letter, cells with a set of keys held. Build the
  graph in your head, not in memory: generate neighbours on the fly.
- **The cost is on nodes, not edges.** Entering a cell costs its value: put the cost on
  every edge into that cell, and do not forget the start cell.
- **"Earliest arrival" with timetables.** Dijkstra where relaxing an edge means waiting for
  the next departure, then travelling; still non-decreasing.
- **"Reach the target with the least fuel, buying fuel along the way".** A state graph,
  (city, something about fuel).

### Anti-signals: looks like shortest paths, is not

- **Moves only right and down.** No cycles: a grid DP.
- **"Is there a route at all?"** Connectivity, not distance.
- **"Connect all the cities as cheaply as possible".** Minimum spanning tree. The answer is
  a set of edges whose total is small, not a route.
- **"Minimum score of a path, roads may be revisited".** If revisiting is allowed and the
  score is a single edge, the answer is a fact about a whole component:
  [[p:visa-minimum-score-path-between-cities|Minimum Score of a Path Between Cities]] is
  [[union-find]] in disguise.
- **"Longest path" in a general graph.** Not solvable this way. In a DAG, yes.

## Traps

**Marking a node final when it is pushed.** Symptom: some distances too high, exactly
those where a cheaper route was found after the first offer. Demonstrated below.

**Forgetting the stale check.** Without `if d > dist[u]: continue`, every old offer
re-relaxes all of its node's edges. The answers stay correct (an old offer can never beat
a newer one), but the work can grow far beyond E log V. Symptom: a timeout on large dense
tests only. Demonstrated below by counting relaxations.

**Dijkstra with a negative edge.** Symptom: wrong answers downstream of the negative edge.
Demonstrated below.

**In-place Bellman-Ford with an edge limit.** Symptom: answers that use too many edges,
often cheaper than the expected output. Demonstrated in "The subtle line, both ways".

**Off-by-one in the limit.** "k stops" is k + 1 edges. Symptom: -1 where an answer exists,
or an answer one flight too long.

**Pushing (node, cost) instead of (cost, node).** The heap orders by node number. Symptom:
plausible but wrong distances; the code is no longer Dijkstra.

**-1 for unreachable, inside dist.** Symptom: unreachable nodes become the cheapest of all.
Keep infinity and convert at the end.

**Forgetting the start cell's own cost** in node-cost grids. Symptom: every answer short
by exactly the start value.

**Returning at the first push of the target** instead of the first pop. Symptom: a route
that is cheaper than any offer popped so far, but not the cheapest. The first **pop** of
the target is final; a push is only an offer.

**A state that is too small.** Using dist[node] when the future depends on more. Symptom:
answers too high, because an arrival with a better "extra" was thrown away for being more
expensive. Shown in variation E.

```python run
import heapq

def adjacency(n, arcs, directed):
    adj = [[] for _ in range(n)]
    for u, v, w in arcs:
        adj[u].append((v, w))
        if not directed:
            adj[v].append((u, w))
    return adj

def dijkstra(adj, s, mark_at_push=False, stale_check=True, final_set=False):
    dist, done, work = [float("inf")] * len(adj), [False] * len(adj), 0
    dist[s] = 0
    heap = [(0, s)]
    if mark_at_push: done[s] = True
    while heap:
        d, u = heapq.heappop(heap)
        if stale_check and d > dist[u]: continue
        if final_set:
            if done[u]: continue
            done[u] = True
        for v, w in adj[u]:
            work += 1
            if mark_at_push and done[v]: continue           # the bug: frozen at push
            if final_set and done[v]: continue              # a final node is not reopened
            if d + w < dist[v]:
                dist[v] = d + w
                if mark_at_push: done[v] = True
                heapq.heappush(heap, (dist[v], v))
    return dist, work

towns = adjacency(5, [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3), (2, 4, 8)], False)
right, _ = dijkstra(towns, 0)
wrong, _ = dijkstra(towns, 0, mark_at_push=True)
print("final at pop :", right)
print("final at push:", wrong, "<- B frozen at 4, D at 6, E at 9")
assert right == [0, 3, 1, 4, 7] and wrong == [0, 4, 1, 6, 9]

neg = adjacency(4, [(0, 1, 2), (0, 2, 3), (2, 1, -2), (1, 3, 1)], True)
got, _ = dijkstra(neg, 0, final_set=True)
print("negative edge, final set:", got, "(true distance to 3 is 2)")
assert got[3] == 3

n = 400                                       # stale check off: same answers, more work
dense = adjacency(n, [(u, v, (u * 7 + v * 13) % 50 + 1)
                      for u in range(n) for v in range(u + 1, n)], False)
a, work_on = dijkstra(dense, 0)
b, work_off = dijkstra(dense, 0, stale_check=False)
print("dense graph, relaxations with stale check:", work_on, " without:", work_off)
assert a == b and work_off > 2 * work_on
```

## What to memorise

The template:

```python
import heapq
def dijkstra(adj, s):
    dist = [float("inf")] * len(adj)
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                        # stale offer
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist
```

And the two edits that turn it into its siblings: a deque with `appendleft` for cost 0
and `append` for cost 1 (0-1 BFS); and, for at most k edges, k passes of
`prev = dist[:]` then `for u, v, w in edges: dist[v] = min(dist[v], prev[u] + w)`
(Bellman-Ford).

The sentence that turns a problem into it: **the nodes are whatever the future needs to
know, the edges are the moves, and the weights choose the algorithm.**

The question: **what does the rest of the route need to know about how I got here?**

The habit: **a node is final when it is popped, never when it is pushed; and a round of
Bellman-Ford reads the previous round.**

The numbers: V + E around 10^5 to 10^6 is fine for Dijkstra in Python; V · E above about
10^8 rules out Bellman-Ford; V ≤ 400 allows Floyd-Warshall; "k stops" is k + 1 edges.

## Check yourself

:::check
Hand trace. Directed roads S→A 2, S→B 5, A→B 1, A→C 6, B→C 2, C→D 1, B→D 7. Run Dijkstra
from S with a heap. Write each pop, whether it is final or stale, every relaxation, and the
heap after each pop. Then give the shortest route to D.
--
| pop | final? | relaxations | dist S A B C D | heap after |
|---|---|---|---|---|
| (0,S) | S=0 | A: 2. B: 5 | 0 2 5 ∞ ∞ | (2,A) (5,B) |
| (2,A) | A=2 | B: 2+1=3 < 5, write 3. C: 2+6=8 | 0 2 3 8 ∞ | (3,B) (5,B) (8,C) |
| (3,B) | B=3 | C: 3+2=5 < 8, write 5. D: 3+7=10 | 0 2 3 5 10 | (5,B) (5,C) (8,C) (10,D) |
| (5,B) | stale (5 > 3) | | | (5,C) (8,C) (10,D) |
| (5,C) | C=5 | D: 5+1=6 < 10, write 6 | 0 2 3 5 6 | (6,D) (8,C) (10,D) |
| (6,D) | D=6 | none | | (8,C) (10,D) |
| (8,C) | stale | | | (10,D) |
| (10,D) | stale | | | empty |

Route to D: S→A→B→C→D, cost 2 + 1 + 2 + 1 = 6. Parent pointers: D from C, C from B, B from
A, A from S.
:::

:::check
Hand trace, both ways. Same directed roads as the previous exercise. Find the cheapest
route from S to D **using at most 2 roads** with Bellman-Ford, relaxing the edges in the
order S→A, S→B, A→B, A→C, B→C, C→D, B→D. Do it once with a copy of the previous pass and
once in place. Where does the in-place version first use too many roads?
--
With a copy. Pass 1 reads [0, ∞, ∞, ∞, ∞]: A = 2, B = 5, nothing else (all other sources
are ∞ in the copy). Pass 2 reads [0, 2, 5, ∞, ∞]: S→A, S→B no change; A→B: 2+1 = 3, write
B = 3; A→C: 2+6 = 8, write C = 8; B→C reads prev B = 5: 7 < 8, write C = 7; C→D reads
prev C = ∞: no; B→D reads prev B = 5: 12. Answer **12** (S→B→D, two roads).

In place. Pass 1: S→A: A = 2. S→B: B = 5. **A→B reads A = 2, written in this pass**: B = 3,
already two roads in pass 1. A→C: C = 8. B→C reads B = 3 (new): C = 5. C→D reads C = 5: D = 6.
B→D: 3+7 = 10, no. After one pass D = 6, a four-road route. Pass 2 changes nothing. The
in-place version answers 6, the unlimited shortest path, and the first excess is the
relaxation of A→B in pass 1.
:::

:::check
Hand trace, 0-1 BFS. A 1 x 4 row of cells with arrows: R R L R (each cell points right or
left). Moving to a neighbour in the arrow's direction costs 0, against it costs 1. From
cell 0 to cell 3, trace the deque. What is the answer?
--
Start deque (0, cell 0), dist [0, ∞, ∞, ∞]. Pop cell 0 (arrow R): cell 1 with the arrow,
cost 0, push front. Deque (0,1). Pop cell 1 (R): cell 2 cost 0, front; cell 0 against, 1,
not better. Deque (0,2). Pop cell 2 (arrow L): cell 1 with the arrow, 0, not better; cell 3
against the arrow, cost 1, push back. Deque (1,3). Pop cell 3: final at 1. Answer **1**: you
must override cell 2's arrow once.
:::

:::check
Why does Dijkstra's proof need non-negative weights, and which single sentence of it fails
with a negative edge? Give the smallest example you can.
--
The proof finds a non-final node y on a cheapest path to u and says δ(y) ≤ δ(u), because the
rest of the path from y to u cannot make the cost go down. That needs every remaining edge
to cost at least 0. With a negative edge, the rest of the path can lower the cost, so a node
popped at a value can later be reached more cheaply through a node that was still in the
heap with a larger value.

Smallest example: S→A 1, S→B 2, B→A −2. Dijkstra pops S, then A at 1 and declares it final;
then B at 2 finds A at 0. If A is final, the answer for A stays 1; the truth is 0.
:::

:::check
Someone says: "My Dijkstra marks nodes visited when I push them, like BFS. It passed all the
samples, so it is fine." Where are they wrong, and what input exposes it?
--
In BFS every edge costs the same, so the first time a node is reached is the cheapest, and
marking at push is safe. With weights, a node can first be reached by an expensive edge and
later by a cheaper two-edge route; marking at push freezes the expensive value.

Exposing input: A→B 4, A→C 1, C→B 2. Push B at 4 and mark it; C is popped and finds B at 3,
but B is marked. The answer for B is 4, the truth 3. Samples often have a unique route per
node or happen to push the cheapest first, so they pass.
:::

:::check
Someone says: "For cheapest flights with at most k stops I will just run Dijkstra and stop
when I have used k + 1 flights." Where are they wrong?
--
Dijkstra keeps one value per node: the cheapest arrival, whatever its number of flights.
With a limit, the cheapest arrival might have used up the flights, while a dearer arrival
with fewer flights is the one that can still continue. Keeping only the cheapest throws
the useful one away.

Example: flights 0→1 100, 1→2 100, 0→2 500, 2→3 100, at most two flights (k = 1). Node-only
Dijkstra settles 2 at 200 by 0→1→2, two flights. From there 2→3 would be a third flight, so
it is refused. The other arrival at 2, the direct flight at 500 with one flight used, is a
stale offer (500 > 200) and is skipped. The code reports 3 as unreachable; the answer is
0→2→3 at 600.

The fix is either Bellman-Ford's k + 1 copied passes, or Dijkstra over states (city,
flights used), where the two arrivals at city 2 are different states and both survive.
:::

:::check
Reduce this disguised problem. "A grid of 0s and 1s, 1 is a wall. You may walk up, down,
left, right through open cells, and you may knock down at most 2 walls. Find the fewest
moves from the top-left to the bottom-right." What are the nodes, the edges and their
costs, and which algorithm runs on them?
--
The future needs to know where you are and how many knock-downs you have left. Nodes are
(row, col, walls left), with walls left in 0..2: three copies of the grid.

Edges: a move to an open neighbour keeps walls left and costs 1; a move into a wall
neighbour costs 1 and decreases walls left by one (only if it is at least 1).

Every edge costs 1, so plain BFS over the states gives the fewest moves; the answer is the
smallest distance over the three copies of the bottom-right cell. If the problem instead
asked for the fewest walls knocked down with unlimited moves, the costs would be 0 (open)
and 1 (wall) on the grid itself, and it would be 0-1 BFS.
:::

:::check
Which algorithm, and why? (a) 10^5 nodes, 2·10^5 edges, weights 1..10^9. (b) A 1000 x 1000
grid, moves cost 0 or 1. (c) 100 cities, flights with prices, at most 5 stops. (d) 300 nodes,
answer 10^4 queries "distance from u to v". (e) Weights may be negative, 500 nodes, 5,000 edges,
and you must report if a negative cycle is reachable.
--
(a) Dijkstra with a heap: non-negative weights, about 3·10^5 log operations.

(b) 0-1 BFS: 10^6 cells and about 4·10^6 edges; the deque makes it linear, where a heap would add
a log factor of about 20.

(c) Bellman-Ford with 6 copied passes (5 stops = 6 flights): 6 x E, tiny.

(d) Floyd-Warshall: 300³ = 2.7·10^7 steps once, then every query is a table lookup. (Dijkstra
from every node is also fine.)

(e) Bellman-Ford: 499 passes over 5,000 edges, about 2.5·10^6 relaxations, and a 500th pass that
still improves something proves a reachable negative cycle.
:::
