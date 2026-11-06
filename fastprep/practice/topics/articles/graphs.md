# Graphs: Representation

> A graph search is one loop, "take a node out of a container, put its unseen neighbours in", and the habit of marking a node the moment it is first discovered is what turns an exponential walk over paths into a linear walk over nodes; whether the container is a queue or a stack decides only the order, and the queue's order happens to be distance.

## The problem it solves

Here is a small road map. Eight towns, numbered 0 to 7, and seven two-way roads:

```
0-1   0-2   1-3   2-4   3-4   4-5   6-7
```

Three questions about it:

1. Can you drive from town 0 to town 5? Can you drive from 0 to 7?
2. Into how many separate groups do the roads split the towns?
3. What is the fewest number of roads you must drive from 0 to every other town?

These three questions are most of this chapter. The first is **reachability**,
the second is **counting connected components**, the third is **shortest paths
when every edge costs the same**. The bank has hundreds of problems that are one
of them in a costume: [[p:amazon-count-connected-components|Count Connected Components]]
is the second exactly, [[p:citadel-shortest-path-unweighted-graph|Shortest Path in an Unweighted Graph]]
is the third exactly, and [[p:goldman-sachs-number-of-islands|Number of Islands]]
is the second on a grid of land and water.

By eye the answers are easy. Yes to 5, no to 7. Two groups, {0, 1, 2, 3, 4, 5}
and {6, 7}. Distances 1 to towns 1 and 2, 2 to towns 3 and 4, 3 to town 5. The
point of the chapter is to get a program to do it on a map of 100,000 towns and
200,000 roads, which is the size [[p:citadel-shortest-path-unweighted-graph|the Citadel problem]]
allows, without the program looking at anything twice.

The first program a beginner writes for question 1 is "try every route". Start
at 0, follow a road, follow another, and so on, until you either arrive at 5 or
run out of roads. That is correct if you are careful not to go round in circles,
and we will see below that it is hopelessly slow: the number of routes grows
exponentially with the size of the map even when the number of towns does not.

The second program is "keep merging": start with every town in its own group,
and sweep over the roads again and again, merging the two groups at the ends of
each road, until a sweep changes nothing. That is correct too, and each sweep
costs a pass over all the roads, and on a long chain of towns you need about n
sweeps. With n = 10^5 and m = 2 x 10^5 that is 2 x 10^10 steps.

The method this chapter builds, graph search with a visited mark, answers all
three questions in one pass over the roads: about n + 2m steps, three hundred
thousand for the Citadel limits. It comes in two orders. With a queue it is
**breadth-first search** (BFS) and it gives distances. With a stack, or with
recursion, it is **depth-first search** (DFS) and it gives structure: components,
cycles, and the finishing order that [[topological-sort]] is built on. The two
have their own chapters, [[bfs]] and [[dfs]]; this one builds both from scratch,
because they are the same idea, and seeing them as one idea is what lets you
derive either on a blank page.

### Before any search: how the map is stored

A search asks one question over and over: "what are the neighbours of u?" So
store the graph in the shape that answers that question fastest, an
**adjacency list**: one list per node, holding the nodes it touches.

```
adj[0] = [1, 2]     adj[4] = [2, 3, 5]
adj[1] = [0, 3]     adj[5] = [4]
adj[2] = [0, 4]     adj[6] = [7]
adj[3] = [1, 4]     adj[7] = [6]
```

Two facts about it become bugs if you forget them. An undirected road is stored
**twice**, as 0 in adj[1] and 1 in adj[0]; nothing reminds you to add the second
one. And the 14 entries for 7 roads are not a coincidence: every road has two
ends, so the lengths of all the lists add up to exactly twice the number of
roads. That one fact, the **handshake lemma**, is why a search that walks every
list once costs n + 2m and not n times the largest list.

The alternatives are worth knowing by name. An **adjacency matrix** is an n x n
grid of 0s and 1s: it answers "is u next to v?" in one lookup, but listing u's
neighbours costs a full row of n cells, so a search over it costs n^2 however few
roads there are. An **edge list** is the input as given, and is fine for
algorithms that only sweep over all edges ([[minimum-spanning-tree]],
[[bellman-ford]]). An **implicit graph** stores nothing at all and computes the
neighbours when asked: a grid, where the neighbours of (r, c) are the four cells
next to it, or a set of words, where two words are neighbours if they differ in
one letter. Implicit graphs are where most interview graphs live, and the search
code does not care: it only ever asks for neighbours.

### When it is the wrong tool

- **The edges have different costs.** "Fewest roads" is BFS. "Least total
  distance" with roads of different lengths is not: BFS would count a 1 km road
  and a 100 km road as one step each. That is [[dijkstra]].
- **You only merge groups and ask "same group?"**, possibly with edges arriving
  over time. [[union-find]] does it with no adjacency list at all.
- **You need every path, not just whether one exists.** "List all routes from 0
  to 5" really is exponential, and the visited mark that makes search fast is
  exactly what you must give up. That is [[backtracking]].
- **The question counts graphs instead of exploring one.**
  [[p:ibm-drawing-edge|Drawing Edge]] asks how many simple graphs exist on n
  labelled nodes, with n up to 10^9. There are n(n-1)/2 possible edges, each in or
  out, so the answer is 2^(n(n-1)/2) mod 10^9 + 7, which is
  [[fast-exponentiation]]. The word "edge" is not a licence to build anything.

## Build it from the brute force

### Step 1: try every route

The honest brute force for "can I get from s to t?" follows roads one at a
time. From the current town, try each road out; if any of the attempts gets to t,
say yes.

```
walk(u):
    if u == t: return True
    for v in adj[u]:
        if walk(v): return True
    return False
```

Run it on the road map from s = 0, looking for t = 7. walk(0) tries road 0-1 and
calls walk(1). walk(1) tries its first road, 1-0, and calls walk(0). walk(0)
tries 0-1 again. The program never stops. Every undirected road is a two-step
loop, and a search that does not remember anything walks it forever.

The obvious repair is "do not step onto a town that is already on the route I am
walking". Keep a set of the towns on the current route, add u when you enter it,
remove it when you leave:

```
walk(u):
    if u == t: return True
    on_route.add(u)
    for v in adj[u]:
        if v not in on_route and walk(v): return True
    on_route.remove(u)
    return False
```

That terminates and is correct. It is also the brute force: it tries every
simple route out of s, one after another.

### Step 2: count it

How many simple routes are there? On some maps, a lot. Take the map in the
picture below: a start s, then a diamond (two towns side by side, both joined to
s and to a join town m1), then another diamond, then a third one ending at t.

<svg viewBox="0 0 520 250" role="img" aria-label="a chain of three diamonds from s to t: eight different paths, but the join nodes m1 and m2 are each reached by two of them, so they are shaded">
  <g>
    <line x1="53.4" y1="89.5" x2="96.6" y2="55.5"/>
    <line x1="53.4" y1="110.5" x2="96.6" y2="144.5"/>
    <line x1="123.4" y1="55.5" x2="166.6" y2="89.5"/>
    <line x1="123.4" y1="144.5" x2="166.6" y2="110.5"/>
    <line x1="193.4" y1="89.5" x2="236.6" y2="55.5"/>
    <line x1="193.4" y1="110.5" x2="236.6" y2="144.5"/>
    <line x1="263.4" y1="55.5" x2="306.6" y2="89.5"/>
    <line x1="263.4" y1="144.5" x2="306.6" y2="110.5"/>
    <line x1="333.4" y1="89.5" x2="376.6" y2="55.5"/>
    <line x1="333.4" y1="110.5" x2="376.6" y2="144.5"/>
    <line x1="403.4" y1="55.5" x2="446.6" y2="89.5"/>
    <line x1="403.4" y1="144.5" x2="446.6" y2="110.5"/>
    <circle cx="40" cy="100" r="17"/>
    <text x="40" y="105" text-anchor="middle">s</text>
    <circle cx="110" cy="45" r="17"/>
    <text x="110" y="50" text-anchor="middle">a1</text>
    <circle cx="110" cy="155" r="17"/>
    <text x="110" y="160" text-anchor="middle">b1</text>
    <circle class="fill" cx="180" cy="100" r="17"/>
    <text x="180" y="105" text-anchor="middle">m1</text>
    <circle cx="250" cy="45" r="17"/>
    <text x="250" y="50" text-anchor="middle">a2</text>
    <circle cx="250" cy="155" r="17"/>
    <text x="250" y="160" text-anchor="middle">b2</text>
    <circle class="fill" cx="320" cy="100" r="17"/>
    <text x="320" y="105" text-anchor="middle">m2</text>
    <circle cx="390" cy="45" r="17"/>
    <text x="390" y="50" text-anchor="middle">a3</text>
    <circle cx="390" cy="155" r="17"/>
    <text x="390" y="160" text-anchor="middle">b3</text>
    <circle cx="460" cy="100" r="17"/>
    <text x="460" y="105" text-anchor="middle">t</text>
    <text x="260" y="205" text-anchor="middle">every diamond doubles the paths: 2 x 2 x 2 = 8 from s to t</text>
    <text x="260" y="228" text-anchor="middle">shaded: one node, reached by two paths; what lies beyond it is the same either way</text>
  </g>
</svg>

From s to m1 there are 2 routes, over the top or the bottom. From m1 to m2, 2
more, independently. So from s to t there are 2 x 2 x 2 = 8 routes, on a map of
10 towns. With k diamonds in a row there are 2^k routes and only 3k + 1 towns.
Forty diamonds is 121 towns and about a trillion routes.

If t is reachable, the walk might be lucky and find it on the first route. If t
is *not* reachable (put t on a separate island), the walk has to fail on every
route before it can say no, and a "no" costs all 2^k of them. The program in
"From the idea to the code" counts the calls: on ten diamonds and an unreachable
target, the route-by-route walk makes several thousand calls on a map of 32
towns.

### Step 3: notice the waste

Look at m1 in the picture. The walk reaches it twice: once via the top town a1,
once via the bottom town b1. Each time, it then explores everything beyond m1:
both ways through the second diamond, both ways through the third. The second
exploration is a copy of the first. It cannot find anything the first did not,
because **what you can reach from m1 does not depend on how you got to m1.**

That sentence is the whole chapter, so say it again with the road map. You are
standing in town 4. Maybe you came 0, 2, 4. Maybe you came 0, 1, 3, 4. The set of
towns you can drive to from here is the same in both cases: the roads out of 4
do not know your history. So once you have explored from 4 one time, a second
visit can only repeat work.

### The question that unlocks it

The question to ask, on this problem and on every graph problem you meet:

**Once I have reached a node, what does the rest of the search need to know
about how I got there?**

For reachability and for components the answer is "nothing". Then a node needs
to be explored at most once, ever, and a single set of visited nodes replaces
the set of nodes on the current route. For fewest steps the answer is "only how
many steps it took", and we will see that if you explore in the right order, the
first time you reach a node is with the fewest steps, so again once is enough.
For a directed cycle the answer is "whether the node is still on the route I am
walking right now", which is why cycle detection keeps three marks instead of
one. And for the hard problems in the Variations, such as
[[p:mercor-shortest-path-in-grid-with-obstacles-elimination|a grid where you may break k walls]],
the answer is "how many walls I have left", and then a node of the search is the
pair (cell, walls left), not the cell.

The general rule, in one line: **a node of the search is whatever the future
needs to know**. Usually that is the town. Sometimes it is the town plus a
little more.

### Step 4: mark once, explore once

Replace "not on the current route" with "never seen before", and never remove
anything from the set:

```
seen = {s}
walk(u):
    for v in adj[u]:
        if v not in seen:
            seen.add(v)
            walk(v)
```

Now each node enters seen once, and is walked from once, and each walk looks at
the node's own list once. The total work is the number of nodes plus the total
length of the lists: n + 2m. On the diamond chain with an unreachable target, the
calls drop from thousands to 31, one per reachable town. This is **depth-first
search**: go as deep as you can along one road, and only when you are stuck,
back up and try the next.

Components come free. Loop over every node; if a node is not yet seen, it starts
a new component, so add one to the count and search from it. Everything that
search marks belongs to the same component, so no later loop iteration will
start from it again.

### You might think: "DFS with a visited set also gives the shortest distances."

It does not, and this is the most common wrong instinct about graph search.
DFS reaches every node, but the route it reaches it by is whatever route it
happened to try first.

The smallest counterexample is a triangle: roads 0-1, 1-2, 0-2, with adj[0] =
[1, 2]. DFS from 0 goes to 1 first, and from 1 it goes to 2, so it reaches 2
after two roads and marks it seen. When it comes back to 0 and looks at the road
0-2, town 2 is already seen, and it is skipped. If you record "depth at which DFS
found it", town 2 gets 2. The true distance is 1.

On the road map it happens too. With the stack-based DFS of the next section,
town 3 is first found from town 4, at the end of the route 0, 2, 4, 3: depth 3.
The true distance is 2, via 0, 1, 3.

What went wrong is the order. DFS dives along one route and marks everything on
it. By the time a short route to a town is tried, the town is already marked from
a long one. The visited mark is safe only if the first visit is the best one.

### You might think: "Then drop the visited set and keep the minimum depth."

That is correct, and it is the brute force again: without the mark, you
re-explore from every node once per route that reaches it, which on the diamond
chain is 2^k. The cure is not to give up the mark. It is to change the order, so
that the first visit *is* the best one.

### Step 5: explore in order of distance

Which order makes the first visit to every node the shortest? Visit everything
at distance 0, then everything at distance 1, then everything at distance 2, and
so on. Make the layers explicit:

- Layer 0 is {s}.
- Layer k + 1 is every node, not seen before, that is a neighbour of some node in
  layer k.

A node first appears in layer k + 1 exactly when it is one road from layer k and
was not in any earlier layer. Its distance is k + 1, no shorter route exists
(it would have put the node in an earlier layer), and it is correct to mark it
now and never look at it again.

You do not need to store the layers. A first-in, first-out queue keeps them in
order by itself: you take nodes from the front, and add their new neighbours at
the back. Every node of layer k is in the queue before any node of layer k + 1,
because layer k + 1 nodes are only added while layer k nodes are being taken
out. This is **breadth-first search**: spread out one ring at a time, like a
ripple.

### Step 6: one loop, two containers

Write both searches without recursion and they are the same program:

```
seen = {s}; box = [s]
while box:
    u = take one out of box
    for v in adj[u]:
        if v not in seen:
            seen.add(v)
            put v into box
```

If "take one out" takes the oldest (a queue), it is BFS. If it takes the newest
(a stack), it is a depth-first order. Everything else is identical, including the
cost, n + 2m, and including the one line that matters most, the place where
seen.add happens. That line gets its own demonstration in "From the idea to the
code", because putting it one line later breaks BFS in a way that passes most
tests.

### The technique in one sentence

**Graph search: keep a container of discovered-but-unexplored nodes, take one
out, and put each of its neighbours in the first time it is ever seen, marking it
at that moment; because what you can reach from a node does not depend on how
you got there, each node is explored once and the cost is n + 2m, and with a
first-in, first-out queue the nodes come out in order of distance.**

And the question that produced it, worth asking every time: **once I have
reached a node, what does the rest of the search need to know about how I got
there?** If the answer is "nothing", the node is the town. If it is "something",
the node is the town plus that something.

## Worked by hand

Get a pen. The road map from the start: nodes 0 to 7, roads 0-1, 0-2, 1-3, 2-4,
3-4, 4-5, 6-7, and the lists in the order given above (each node's neighbours in
increasing order). dist[v] = -1 means "not seen yet", so the dist array is also
the visited mark.

### BFS from 0

| step | take out | its neighbours | newly seen (dist) | queue after |
|---|---|---|---|---|
| start | | | 0 (0) | [0] |
| 1 | 0 | 1, 2 | 1 (1), 2 (1) | [1, 2] |
| 2 | 1 | 0, 3 | 3 (2) | [2, 3] |
| 3 | 2 | 0, 4 | 4 (2) | [3, 4] |
| 4 | 3 | 1, 4 | none | [4] |
| 5 | 4 | 2, 3, 5 | 5 (3) | [5] |
| 6 | 5 | 4 | none | [] |

Final dist = [0, 1, 1, 2, 2, 3, -1, -1].

Step 2, told in full:

> "I take town 1 off the front of the queue. Its distance is 1. Its neighbours
> are 0 and 3. Town 0 has a distance already (0), so it was seen, and I skip it.
> Town 3 has no distance yet, so this is the first time anyone has found it. I
> give it distance 1 + 1 = 2, because I found it one road from a town at
> distance 1, and I put it at the back of the queue. The queue was [2], and now it
> is [2, 3]: the last town of layer 1, then the first town of layer 2."

Step 4 is the one to stare at. Town 3 has neighbour 4, and 4 is not yet taken
out of the queue, but it already has a distance, 2, from step 3. So it is skipped.
Through 3, town 4 would have been at distance 3. Skipping it is correct because
it was first seen through a shorter route, and in BFS the first sighting is
always through a shortest route. If 4 were only marked when it was *taken out*,
step 4 would see it as unmarked and get its distance wrong. That is the subtle
line, and it is demonstrated in code below.

Here is the same run as a picture, nodes placed by the distance BFS gave them:

<svg viewBox="0 0 720 270" role="img" aria-label="the eight-node example drawn in BFS layers: node 0 at distance 0, nodes 1 and 2 at distance 1, nodes 3 and 4 at distance 2, node 5 at distance 3, and nodes 6 and 7 never reached from 0; the edge 3-4 joins two nodes in the same layer">
  <g>
    <line x1="95.8" y1="113.7" x2="214.2" y2="66.3"/>
    <line x1="95.8" y1="126.3" x2="214.2" y2="173.7"/>
    <line x1="247.0" y1="60.0" x2="363.0" y2="60.0"/>
    <line x1="247.0" y1="180.0" x2="363.0" y2="180.0"/>
    <line x1="380.0" y1="77.0" x2="380.0" y2="163.0" stroke-dasharray="5 4"/>
    <line x1="397.0" y1="180.0" x2="513.0" y2="180.0"/>
    <line x1="650.0" y1="77.0" x2="650.0" y2="163.0"/>
    <circle cx="80" cy="120" r="17"/>
    <text x="80" y="125" text-anchor="middle">0</text>
    <circle cx="230" cy="60" r="17"/>
    <text x="230" y="65" text-anchor="middle">1</text>
    <circle cx="230" cy="180" r="17"/>
    <text x="230" y="185" text-anchor="middle">2</text>
    <circle class="fill" cx="380" cy="60" r="17"/>
    <text x="380" y="65" text-anchor="middle">3</text>
    <circle class="fill" cx="380" cy="180" r="17"/>
    <text x="380" y="185" text-anchor="middle">4</text>
    <circle cx="530" cy="180" r="17"/>
    <text x="530" y="185" text-anchor="middle">5</text>
    <circle cx="650" cy="60" r="17"/>
    <text x="650" y="65" text-anchor="middle">6</text>
    <circle cx="650" cy="180" r="17"/>
    <text x="650" y="185" text-anchor="middle">7</text>
    <text x="80" y="232" text-anchor="middle">dist 0</text>
    <text x="230" y="232" text-anchor="middle">dist 1</text>
    <text x="380" y="232" text-anchor="middle">dist 2</text>
    <text x="530" y="232" text-anchor="middle">dist 3</text>
    <text x="650" y="232" text-anchor="middle">not reached</text>
    <text x="360" y="258" text-anchor="middle">dashed: 3-4 stays inside one layer, so it never shortens anything</text>
  </g>
</svg>

Every road either joins two neighbouring layers (0-1, 1-3, 4-5, ...) or stays
inside one layer (3-4). No road skips a layer. If one did, say a road from
layer 0 straight to layer 2, then the node at its far end would have been found
at step 1 and put in layer 1. That "no road skips a layer" is the reason the
layers are the distances, and it is the heart of the proof below.

Towns 6 and 7 never got a distance. To count components, loop v = 0..7: v = 0
is unseen, so count 1 and run the search above, which marks 0 to 5. v = 1..5 are
seen. v = 6 is unseen: count 2, search from it, mark 6 and 7. v = 7 is seen.
Two components.

### DFS from 0, with a stack

The same loop, but take from the back. Push neighbours in list order, so the
last neighbour pushed is the first explored.

| step | take out (top) | its neighbours | newly seen | stack after |
|---|---|---|---|---|
| start | | | 0 | [0] |
| 1 | 0 | 1, 2 | 1, 2 | [1, 2] |
| 2 | 2 | 0, 4 | 4 | [1, 4] |
| 3 | 4 | 2, 3, 5 | 3, 5 | [1, 3, 5] |
| 4 | 5 | 4 | none | [1, 3] |
| 5 | 3 | 1, 4 | none | [1] |
| 6 | 1 | 0, 3 | none | [] |

Taken out in the order 0, 2, 4, 5, 3, 1. Every reachable town was found, so for
reachability and components this works exactly as well as BFS, and it is
cheaper to write. But town 3 was discovered from 4, at the end of 0, 2, 4, 3, so
"the depth DFS found it at" is 3, and the truth is 2. The order of discovery
says nothing about distance. That is the counterexample from the derivation,
traced.

One more thing the table shows: the order is a consequence of the order inside
the lists. Had adj[0] been [2, 1], BFS would still give the same distances (the
layers do not depend on order), but its output order would differ, and DFS would
explore an entirely different route first. When a problem wants one specific
order, such as [[p:rippling-distributed-system-recovery|Distributed System Recovery]],
which wants each layer in increasing node number, the order is part of the
specification and you must enforce it yourself.

### A second trace: many sources at once

Now a grid. [[p:lyft-rotten-oranges-grid-bfs|Rotten Oranges]]: 0 is empty, 1 is
a fresh orange, 2 is rotten. Every minute, each rotten orange rots its fresh
neighbours up, down, left and right. How many minutes until nothing is fresh?

```
2 1 1
1 1 0
0 1 1
```

A grid is a graph you never build. The nodes are cells; the neighbours of (r, c)
are (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1), when they are inside the grid
and not empty. Code walks them with a direction array, `DIRS = [(-1,0), (1,0),
(0,-1), (0,1)]`, and a bounds check.

The minutes are the BFS layers. Minute 0 is the rotten cell (0,0). Minute 1 is
its fresh neighbours, (0,1) and (1,0). Minute 2 is their fresh neighbours not
already rotten: (0,2) from (0,1), and (1,1) from either. Minute 3: (2,1) from
(1,1). Minute 4: (2,2) from (2,1). Writing the minute each cell rots:

```
0 1 2
1 2 .
. 3 4
```

The answer is 4, the largest number. Cell (1,1) is worth a sentence: it is a
neighbour of both (0,1) and (1,0), which rot at the same minute. Whichever of the
two is taken out of the queue first marks it with minute 2; the other one sees
it marked and leaves it. Marking on discovery is what stops the second one from
adding it again.

Now the case this trace was chosen for, a single row with a rotten orange at
each end:

```
2 1 1 1 2
```

**You might think: run BFS from the first rotten orange, then from the second.**
From the left orange alone, the right-most fresh one rots at minute 3. But the
two rot *simultaneously*: the middle orange is reached at minute 2 from both
sides, and the whole row is rotten at minute 2. Running the searches one after
another answers a different question (what if only one were rotten).

**You might think: run a BFS from each rotten orange and take, per cell, the
minimum.** That is correct, and costs one full search per source. With k rotten
oranges on an R x C grid that is k x R x C.

The fix is to start all of them at once: put *every* source in the queue at
distance 0 before the loop starts. The queue is then layer 0 as usual, it just
has several nodes in it. On the row: minute 0 = {0, 4}, minute 1 = {1, 3},
minute 2 = {2}. Answer 2, in one search. This is **multi-source BFS**, and it is
the same algorithm as single-source BFS on a graph with an invisible extra node
joined to every source. The proof below covers it without change.

### Islands by hand

[[p:goldman-sachs-number-of-islands|Number of Islands]], second example:

```
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

Scan cells row by row. (0,0) is land and unseen: islands = 1, flood from it,
which marks (0,0), (0,1), (1,0), (1,1). The rest of rows 0 and 1 is water or
seen. (2,2) is land and unseen: islands = 2, the flood marks only (2,2), because
its four neighbours are water (the diagonal (3,3) does not count). (3,3) is land
and unseen: islands = 3, the flood marks (3,3) and (3,4). Answer 3. This is the
component count from the road map, with "neighbours" computed from coordinates.

## From the idea to the code

### First: the brute force and the cure, side by side

This block runs the route-by-route walk and the mark-once walk on the diamond
chain, counts their calls, and then checks that BFS distances agree with the
brute force "shortest of all simple routes" on a few hundred random small graphs.

```python run
from collections import deque
import random

def build(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)                  # an undirected road is stored twice
    return adj

def diamond_chain(k):
    edges, prev, nxt = [], 0, 1
    for _ in range(k):
        top, bottom, join = nxt, nxt + 1, nxt + 2
        edges += [(prev, top), (prev, bottom), (top, join), (bottom, join)]
        prev, nxt = join, nxt + 3
    return nxt + 1, edges                 # one extra node: an unreachable target

def walk_routes(adj, s, t):               # brute force: every simple route
    calls, on_route = 0, set()
    def walk(u):
        nonlocal calls
        calls += 1
        if u == t:
            return True
        on_route.add(u)
        found = any(v not in on_route and walk(v) for v in adj[u])
        on_route.discard(u)
        return found
    return walk(s), calls

def walk_marked(adj, s, t):               # the cure: mark once, never unmark
    calls, seen = 0, {s}
    def walk(u):
        nonlocal calls
        calls += 1
        if u == t:
            return True
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                if walk(v):
                    return True
        return False
    return walk(s), calls

for k in (3, 6, 10):
    n, edges = diamond_chain(k)
    adj = build(n, edges)
    (r1, c1), (r2, c2) = walk_routes(adj, 0, n - 1), walk_marked(adj, 0, n - 1)
    print("%2d diamonds, %2d nodes: routes walk %5d calls, marked walk %2d calls"
          % (k, n, c1, c2))
    assert r1 is r2 is False and c2 == n - 1 and c1 > 2 ** k

def bfs(adj, s):
    dist = [-1] * len(adj)
    dist[s], q = 0, deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

def shortest_by_routes(adj, s):           # min length over every simple route
    best, on_route = [-1] * len(adj), set()
    def walk(u, d):
        if best[u] == -1 or d < best[u]:
            best[u] = d
        on_route.add(u)
        for v in adj[u]:
            if v not in on_route:
                walk(v, d + 1)
        on_route.discard(u)
    walk(s, 0)
    return best

random.seed(7)
for _ in range(300):
    n = random.randint(1, 8)
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.35]
    adj = build(n, edges)
    assert bfs(adj, 0) == shortest_by_routes(adj, 0)
print("BFS == shortest over all simple routes on 300 random graphs")
```

Ten diamonds: about six thousand calls against 31. The marked walk makes one
call per node it can reach, whatever the shape, because a node enters `seen`
once and is walked from once.

### The direct version: BFS, DFS, components, islands

```python run
from collections import deque

def build(n, edges):
    adj = [[] for _ in range(n)]          # n from the statement, never from edges
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def bfs(adj, s):
    dist = [-1] * len(adj)                # -1 = not seen; dist doubles as the mark
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()                   # oldest first: layer by layer
        for v in adj[u]:
            if dist[v] == -1:             # first time anyone has seen v
                dist[v] = dist[u] + 1     # mark it NOW, with its distance
                q.append(v)
    return dist

def dfs_order(adj, s):
    seen, stack, order = {s}, [s], []
    while stack:
        u = stack.pop()                   # newest first: dive
        order.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return order

def count_components(n, adj):
    seen, count = [False] * n, 0
    for s in range(n):                    # every node, including isolated ones
        if not seen[s]:
            count += 1                    # s starts a component nobody reached
            seen[s], stack = True, [s]
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if not seen[v]:
                        seen[v] = True
                        stack.append(v)
    return count

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def num_islands(grid):
    R, C = len(grid), len(grid[0])
    seen, islands = set(), 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1" and (r, c) not in seen:
                islands += 1
                seen.add((r, c))
                stack = [(r, c)]
                while stack:
                    x, y = stack.pop()
                    for dx, dy in DIRS:   # the four edges of a cell, computed
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == "1" \
                                and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
    return islands

adj = build(8, [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4), (4, 5), (6, 7)])
print("adj      ", adj)
print("BFS dist ", bfs(adj, 0))
print("DFS order", dfs_order(adj, 0))
print("components", count_components(8, adj))
assert bfs(adj, 0) == [0, 1, 1, 2, 2, 3, -1, -1]
assert dfs_order(adj, 0) == [0, 2, 4, 5, 3, 1]
assert count_components(8, adj) == 2
adj10 = build(10, [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4), (4, 5), (6, 7)])
assert count_components(10, adj10) == 4      # nodes 8 and 9 are islands of one
tri = build(3, [(0, 1), (1, 2), (0, 2)])
assert bfs(tri, 0) == [0, 1, 1]
for g, want in ((["11110", "11010", "11000", "00000"], 1),
                (["11000", "11000", "00100", "00011"], 3), (["000", "000"], 0)):
    print(g, "islands", num_islands(g))
    assert num_islands(g) == want
```

### Each line, and which idea it is

| line | in plain words | in the derivation |
|---|---|---|
| `adj = [[] for _ in range(n)]` | one empty list per node | the stored form of "neighbours of u" |
| `adj[v].append(u)` | the road works both ways | undirected = two one-way entries |
| `dist = [-1] * len(adj)` | nobody is seen yet | the visited set, folded into the answer |
| `dist[s] = 0`, `q = deque([s])` | s is layer 0 | the base case: s is 0 roads from itself |
| `u = q.popleft()` | take the oldest discovered node | FIFO keeps layers in order |
| `if dist[v] == -1` | has anyone ever seen v? | "explore once": skip if seen |
| `dist[v] = dist[u] + 1` | one road further than u | v belongs to the next layer |
| `q.append(v)` | v waits behind the rest of this layer | the back of the queue is the next layer |
| `stack.pop()` | take the newest | the only change that makes it DFS |
| `for s in range(n): if not seen[s]` | anyone not reached starts a new group | components |
| `for dx, dy in DIRS` + bounds | the edges of a cell | an implicit graph |

Some boring confusions, settled.

**Why does dist double as the visited set?** Because "has a distance" and "has
been seen" are the same event in BFS: a node gets its distance at the moment it
is first seen, and never changes it. Using one array removes the chance of the
two disagreeing.

**Why is `seen[s] = True` set before the inner loop in `count_components`?**
Because s is discovered by the outer loop, not by a neighbour. If you forget it,
s is not marked, a neighbour pushes it again, and nothing worse happens than a
wasted push here; but in BFS forgetting `dist[s] = 0` would let a neighbour give
s distance 2.

**What about 1-based input?** [[p:inmobi-course-schedule|Course Schedule]] and
[[p:rippling-distributed-system-recovery|Distributed System Recovery]] number
nodes from 1. Either allocate n + 1 lists and never use list 0 (then the
component loop must run over 1..n, or node 0 counts as an extra component), or
subtract 1 when reading each edge. Pick one and do it in the builder.

**Is the stack version "real" DFS?** For reachability and components it does
everything DFS is needed for. It is not quite the recursive order: the
recursive version enters a node's first child completely before even looking at
the second, while the stack version marks all children at once. When the *order*
matters, for a post-order, for cycle detection, for [[topological-sort]], use
the recursive form (or a stack that stores "node, index of the next neighbour
to try"). Python's default recursion limit is about a thousand, so for 10^5
nodes either raise it or use that explicit form.

### The subtle line, both ways

In BFS, mark a node when it is **discovered** (put into the queue), not when it
is **taken out**. It looks like a matter of style. It is not.

Run both on the triangle 0-1, 0-2, 1-2 from s = 0, with dist set when a node is
pushed. A `*` marks the step that goes wrong.

```
Mark on discovery (right)                 Mark on take-out (wrong)
take 0: see 1 -> dist 1, see 2 -> dist 1  take 0, mark 0: 1 unmarked -> dist 1, push
                                                          2 unmarked -> dist 1, push
queue [1, 2]                              queue [1, 2]
take 1: 0 seen, 2 seen (dist 1) -> skip   take 1, mark 1: 0 marked, 2 NOT marked
                                                        -> dist[2] = 2, push   *
take 2: nothing new                       take 2, mark 2
                                          take 2 again (a duplicate): skip
final dist [0, 1, 1]                      final dist [0, 1, 2]   wrong
```

The wrong version goes wrong at the starred step. Town 2 was found at distance 1
and was sitting in the queue, but nothing said so, because the mark is only set
when a node leaves the queue. So town 1, taken out first, "discovers" it again
and overwrites the right distance with a worse one. Here is the same thing as a
single sentence: **between being discovered and being taken out, a node is
waiting in the queue, and the mark has to cover that waiting time.**

There is a correct way to mark on take-out: put (node, distance) pairs in the
queue, set the distance only when the node is taken out for the first time, and
skip later copies. That gives the right answer, and it lets the queue fill with
copies: each node can be pushed once per neighbour taken out before it. It is
the lazy style that [[dijkstra]] uses, where it is needed. In BFS it is just
waste. The block below shows the wrong distance, the copies, and the right
version, and checks the right one against the brute force.

```python run
from collections import deque
import random

def build(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def bfs_mark_on_discovery(adj, s):        # RIGHT
    dist, q, pushes = [-1] * len(adj), deque([s]), 1
    dist[s] = 0
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
                pushes += 1
    return dist, pushes

def bfs_mark_on_takeout(adj, s):          # WRONG: dist set at push, mark at pop
    dist, seen, q = [-1] * len(adj), set(), deque([s])
    dist[s] = 0
    while q:
        u = q.popleft()
        if u in seen:
            continue
        seen.add(u)
        for v in adj[u]:
            if v not in seen:             # v may already be waiting in the queue
                dist[v] = dist[u] + 1     # ...and this overwrites its distance
                q.append(v)
    return dist

def bfs_lazy(adj, s):                     # correct but wasteful: copies in the queue
    dist, q, pushes = [-1] * len(adj), deque([(s, 0)]), 1
    while q:
        u, d = q.popleft()
        if dist[u] != -1:
            continue                      # a stale copy
        dist[u] = d
        for v in adj[u]:
            if dist[v] == -1:
                q.append((v, d + 1))
                pushes += 1
    return dist, pushes

tri = build(3, [(0, 1), (0, 2), (1, 2)])
print("triangle, mark on discovery:", bfs_mark_on_discovery(tri, 0)[0])
print("triangle, mark on take-out :", bfs_mark_on_takeout(tri, 0), " <- town 2 wrong")
assert bfs_mark_on_discovery(tri, 0)[0] == [0, 1, 1]
assert bfs_mark_on_takeout(tri, 0) == [0, 1, 2]

R = C = 30                                # a 30 x 30 open grid, as a graph
cell = lambda r, c: r * C + c
edges = [(cell(r, c), cell(r, c + 1)) for r in range(R) for c in range(C - 1)]
edges += [(cell(r, c), cell(r + 1, c)) for r in range(R - 1) for c in range(C)]
grid = build(R * C, edges)
d1, p1 = bfs_mark_on_discovery(grid, 0)
d2, p2 = bfs_lazy(grid, 0)
wrong = bfs_mark_on_takeout(grid, 0)
print("30x30 grid: pushes on discovery %d, lazy %d; take-out version right? %s"
      % (p1, p2, wrong == d1))
assert d1 == d2 and p1 == R * C and p2 > p1
assert all(d1[cell(r, c)] == r + c for r in range(R) for c in range(C))
assert wrong == d1                        # a grid has no odd cycle: the bug hides

random.seed(3)
caught = 0
for _ in range(300):
    n = random.randint(1, 9)
    g = build(n, [(u, v) for u in range(n) for v in range(u + 1, n) if random.random() < 0.4])
    assert bfs_mark_on_discovery(g, 0)[0] == bfs_lazy(g, 0)[0]
    caught += bfs_mark_on_takeout(g, 0) != bfs_lazy(g, 0)[0]
print("300 random graphs: lazy always right; take-out version wrong on", caught)
assert caught > 0
```

On the grid every distance should be r + c, and the mark-on-discovery version
pushes each of the 900 cells exactly once. The lazy version gets the same
distances with nearly twice as many pushes.

And look at what the take-out version does on the grid: it is *right*. That is
not luck, and it is what makes this bug dangerous. The overwrite only happens
when two nodes in the *same layer* are joined by an edge, as 1 and 2 are in the
triangle: then the one taken out first re-discovers the other. A grid, a tree, a
path and a square have no such edge (their layers alternate like the squares of
a chessboard; these are the bipartite graphs of Variation G). So the wrong
version passes every grid test and every tree test, and fails only on graphs
with an odd cycle, which is a fair share of the random graphs above and of the
hidden tests of any problem on general graphs.

### Memo, recursion or loop?

For components and reachability, recursion reads best and fails at depth about
1000 in Python; a long chain of 10^5 nodes is a `RecursionError`. The stack
loop never fails. For BFS there is no recursive form worth writing. For cycle
detection and post-order you need the recursive shape; write it recursively for
small inputs and with an explicit (node, next-neighbour-index) stack for large
ones. The Variations show the recursive form.

## Why it is correct

Two claims: graph search marks exactly the nodes reachable from s, and BFS gives
each of them its true distance.

:::proof Search finds exactly what is reachable, and BFS layers are distances
**Words first.** d(v) is the true distance: the fewest roads on any route from s
to v, or "infinite" if there is none. A node is *reachable* if d(v) is finite.

**Claim 1. A node is marked if and only if it is reachable.**

*Only reachable nodes are marked.* s is marked first and is reachable. Every
other node v is marked while some marked node u is being explored and v is in
u's list, so there is a road u-v. Following the "who marked whom" links back from
v to s gives a route. So every marked node is reachable.

*Every reachable node is marked.* Suppose not, and take an unmarked reachable
node v with the shortest route from s. v is not s (s is marked), so the route has
a second-to-last node u, which is reachable with a shorter route, so by the
choice of v, u is marked. Every marked node is put into the container once, and
the loop runs until the container is empty, so u is taken out and its list is
walked. v is in that list. At that moment either v is already marked, or it is
marked now. Either way v is marked, which contradicts the choice of v.

**Claim 2 (BFS only). When the loop ends, dist[v] = d(v) for every reachable v.**

*Lemma: the queue is sorted, and spans at most one.* At every moment, the dist
values of the nodes in the queue, front to back, are non-decreasing, and the last
is at most the first plus one. At the start the queue is [s] with value 0. Each
step takes out the front node u with value D. The remaining values are all D or
D + 1, because they were between D and D + 1 before. Every node pushed in this
step gets value D + 1, at the back. So the queue is still sorted and still spans
at most one.

It follows that nodes are *taken out* in non-decreasing order of dist: all the 0s,
then all the 1s, then all the 2s.

*Now the distances.* Prove by induction on k: every node with d(v) = k gets
dist[v] = k, and no other node gets dist k.

Base, k = 0: only s has d = 0, and dist[s] = 0 is set before the loop. Every other
node gets dist[u] + 1 >= 1.

Step: suppose it is true for 0, 1, ..., k. Take v with d(v) = k + 1. On a
shortest route, the node before v, call it u, has d(u) = k, so by the induction
dist[u] = k. When u is taken out, v is either unmarked, and it gets k + 1 now; or
it was marked earlier, by some node w taken out before u. By the lemma, w was
taken out before u means dist[w] <= dist[u] = k, so dist[v] = dist[w] + 1 <= k + 1.
And dist[v] cannot be <= k, because the induction says the nodes with dist <= k
are exactly the nodes with d <= k, and d(v) = k + 1. So dist[v] = k + 1.

Conversely, a node v that gets dist k + 1 got it from a node w with dist k,
which by the induction has d(w) = k; the road w-v gives d(v) <= k + 1, and v is
not among the nodes with d <= k (those all have dist <= k), so d(v) = k + 1.

**Termination.** Each node is pushed at most once (only when unmarked, and it is
marked at the push), so the loop runs at most n times. ∎
:::

The assumptions the proof used, in plain words, because each one is a bug when
it fails:

- **The mark is set when a node is pushed.** "Each node is pushed at most once"
  and "dist[v] is set once and never changes" both depend on it. The subtle line,
  again.
- **The container in Claim 2 is first-in, first-out.** Claim 1 works for any
  container, which is why DFS is fine for reachability. Claim 2 used the sorted
  queue, and a stack is not sorted. That is the whole difference between "DFS
  finds everything" and "DFS finds shortest routes" (it does not).
- **Every road costs the same.** The step "dist[w] + 1" treats every road as one
  unit. With weights the lemma fails: a node one long road away is not "closer"
  than a node two short roads away. Then you need [[dijkstra]].
- **The graph does not change during the search.**
- **Multi-source is the same proof.** Put several sources at distance 0 and the
  lemma's starting queue is [s1, s2, ...] with all values 0, still sorted. The
  induction's base case becomes "the nodes with d = 0 are the sources", and d(v)
  becomes "distance to the nearest source". Nothing else changes.
- **Undirected or directed does not matter** as long as the lists hold the roads
  in the direction they can be driven. A directed graph's search marks what is
  reachable *following arrows*.

## What it costs

Count it. Each node is pushed at most once and taken out at most once: that is n
pushes and n pops. When a node u is taken out, the loop walks its list once,
deg(u) steps. Adding over all nodes:

```
total = sum over u of (1 + deg(u)) = n + sum of degrees = n + 2m
```

by the handshake lemma (every undirected road appears in two lists). For a
directed graph the sum of out-degrees is m, so n + m. Either way the cost is
**O(n + m)**, linear in the size of the input. You cannot do better, since you
must read the input. For the Citadel limits, n = 10^5 and m = 2 x 10^5, that is
half a million steps.

Note what the sum did *not* do: it is not n times the largest degree. A star with
one hub joined to 10^5 leaves has a hub of degree 10^5, but the total is still
about 3 x 10^5. Bound graph loops by summing, never by multiplying.

**Space.** The lists: n + 2m entries. The dist or seen array: n. The queue or
stack: at most n.

**The costs people forget.**

- **`list.pop(0)` is not a queue.** It shifts every remaining element, so each pop
  costs the length of the list, and BFS becomes O(n^2). Use `collections.deque`
  and `popleft()`.
- **The matrix.** If the input is an n x n matrix and you search it directly, each
  "neighbours of u" is a scan of n cells: O(n^2) whatever m is. Fine for n in the
  hundreds, impossible at 10^5.
- **Grids.** R x C cells, each with at most 4 neighbours: O(RC). A 300 x 300 grid
  (the Goldman Sachs limit) is 90,000 cells and at most 360,000 neighbour checks.
- **Generated neighbours.** In a word graph, "neighbours of a word" is computed by
  changing each of its L letters to each of 26 others and looking the result up in
  a set: 25L lookups, each hashing a string of length L. That is O(N x 25L x L)
  for N words. Comparing every pair of words instead is O(N^2 x L). Which is
  smaller depends on N against 25L; for three-letter city names
  ([[p:amazon-find-minimum-city-hops|Find Minimum City Hops]]) the generation
  side is 75 lookups per word.
- **State graphs.** When a node is (cell, walls left), the node count is R x C x
  (k + 1). For [[p:mercor-shortest-path-in-grid-with-obstacles-elimination|the Mercor grid]],
  40 x 40 x up to 1601 walls is about 2.5 million states, which is why the
  standard solution first caps k at R + C - 2 (a shortest route never needs to
  break more walls than its length): then it is 40 x 40 x 79, about 126,000.
- **Recursion.** A recursive DFS on a 10^5-node chain uses 10^5 stack frames.
  CPython stops at about 1000 by default.

## How to think about it

Questions to ask on every new problem that might be a graph, in this order:

1. **What are the nodes?** Towns, cells, words, people, accounts, states of a
   puzzle. If it is not obvious, it is often "the situation I am in", which is
   the unlocking question again.
2. **What are the edges, and are they given or generated?** An edge list means
   build an adjacency list. A grid or a rule ("differ in one letter") means write
   a neighbours function and build nothing.
3. **Directed or undirected?** "Bidirectional", "mutual", "friends" mean push
   both ways. "Depends on", "follows", "points to" mean one way, and the
   direction must match the statement's wording.
4. **What is being asked?** Reachable (any search), how many groups (search from
   every unseen node), how big the biggest group (search that counts), fewest
   steps (BFS), an order (DFS finishing order, see [[topological-sort]]), is
   there a cycle (DFS colours or Kahn's count).
5. **One source, or many?** Many sources with "nearest" or "simultaneous" means
   all of them in the queue at distance 0.
6. **Does a node need to remember more than where it is?** Keys collected, walls
   broken, the parity of the step, the direction you face. If yes, the node is a
   tuple, and the visited set is over tuples.
7. **How many nodes and edges, really?** For an implicit or state graph, compute
   it from the constraints before writing code. That number is the cost.
8. **Are the steps all the same cost?** If not, BFS is wrong; see [[dijkstra]].

Question 6 is where people get stuck, and it is the same question the knapsack
chapter calls "what is the least the future needs to know about the past".

### Telling it from its neighbours

- **BFS or DFS?** Fewest steps, nearest, minimum minutes or layers: BFS. Just
  reachability or counting: either, and DFS is shorter to write. Ordering,
  cycles, "finishes before": DFS.
- **Graph search or union-find?** If the edges all exist up front and you need
  distances or traversal, search. If edges arrive over time and you only need
  "same group?", [[union-find]].
- **BFS or Dijkstra?** All steps cost 1: BFS. Steps cost 0 or 1: a deque, pushing
  0-cost steps to the front (0-1 BFS). Arbitrary non-negative costs: [[dijkstra]].
- **Graph search or DP?** If the graph has no cycles and you want a best path, it
  is DP on a DAG ([[topological-sort]]). If it has cycles and every step costs 1,
  BFS. Grids where you may only move right and down are DAGs; grids where you
  may move in four directions are not.
- **Search or backtracking?** If you need *one* answer per node (reachable,
  distance), mark and never unmark. If you need *every* path or every
  arrangement, you unmark on the way back, and the cost is exponential by
  nature: [[backtracking]].

## Variations

Each of these keeps the loop and changes one thing. The bank problem named is
one that teaches the point.

### A. Count components, and measure them

**What changes:** an outer loop over all nodes, starting a search from each
unseen one. **Why:** a search from s marks exactly s's component (Claim 1), so
the number of searches started is the number of components. To measure a
component, count the nodes each search marks.

Example: n = 5, edges 0-1, 1-2, 3-4: searches start at 0 and at 3, so 2.
[[p:amazon-count-connected-components|Count Connected Components]] is exactly
this; remember the isolated nodes, which are components of size one.
[[p:intuit-maximum-island-area|Maximum Island Area]] counts cells per flood and
keeps the largest.

### B. A grid is a graph: direction arrays

**What changes:** no adjacency list; neighbours come from `DIRS` plus a bounds
check plus a "passable?" check. **Why:** the edges are implied by coordinates,
so storing them would cost memory and add nothing.

Example: `["11","01"]` is one island: (0,0)-(0,1) and (0,1)-(1,1) are land
neighbours. [[p:goldman-sachs-number-of-islands|Number of Islands]] teaches it.
Eight directions (diagonals count) is a different `DIRS`, and the statement
must say so; "diagonal contact does not join islands" in
[[p:intuit-maximum-island-area|Maximum Island Area]] says the opposite. Mark grid
cells in a 2-D boolean array or by overwriting the grid (`grid[r][c] = "0"`); a
set of tuples works and is slower.

### C. Fewest steps: BFS, and BFS by layers

**What changes:** a queue, and dist assigned at discovery. **Why:** the proof.

Example: [[p:citadel-shortest-path-unweighted-graph|Shortest Path in an Unweighted Graph]]:
edges 0-1, 1-2, 0-3, 3-4, 4-2, source 0, target 2: the answer is 2, via 1.

When you need to do something per layer (sort it, count it, stop after k
layers), process the queue one layer at a time: `for _ in range(len(q))` inside
the while loop takes exactly the current layer.
[[p:rippling-distributed-system-recovery|Distributed System Recovery]] wants
nodes in order of hops and, within a layer, by node number: BFS gives the
layers, and you sort each one. Note that sorting each layer's output is not the
same as sorting adjacency lists; with sorted lists the queue order within a
layer follows the parents' order, not the node numbers.

To recover the route, not just its length, store `parent[v] = u` at the moment v
is discovered, and walk parents back from the target.

### D. Multi-source BFS

**What changes:** the queue starts with every source at distance 0. **Why:**
"the distance to the nearest source" is the distance from one invisible
super-source joined to all of them, and putting all sources in layer 0 is BFS
from that super-source.

Example: row `2 1 1 1 2` rots in 2 minutes, not 3.
[[p:lyft-rotten-oranges-grid-bfs|Rotten Oranges]] teaches it, including the -1
for a fresh orange no search ever reaches (count the fresh ones and check they
all got a minute). [[p:doordash-closest-dashmart|Closest DashMart]] is the
same move used for queries: one BFS from all the DashMarts gives every cell its
distance, and each query becomes a lookup, instead of one BFS per query.

### E. Model it as a graph: states as nodes

**What changes:** you invent the nodes and generate the edges. **Why:** the
unlocking question. If the situation you are in is more than a position, the
node must say so.

Three levels, all in the bank:

- **The nodes are given, the edges are a rule.**
  [[p:amazon-find-minimum-city-hops|Find Minimum City Hops]]: cities are
  three-letter strings, joined if they differ in one position. BFS over the
  cities, generating each city's neighbours by trying all 25 x 3 one-letter
  changes against a set. ["abc","abd","acd"]: abc to abd to acd, 2 hops.
- **The same, in a new story.** [[p:benchling-minimum-genetic-mutation|Minimum Genetic Mutation]]:
  genes are 8-letter strings over ACGT, a mutation changes one letter, every
  intermediate must be in the bank. It is the previous problem with 8 x 3
  candidate neighbours instead of 3 x 25; recognising that is the skill.
- **The position is not enough.**
  [[p:mercor-shortest-path-in-grid-with-obstacles-elimination|Shortest Path with Obstacle Elimination]]:
  you may break up to k walls. Two arrivals at the same cell with different
  numbers of walls left have different futures, so the node is (row, col, walls
  left) and the visited set is over triples. Its first example, k = 1, has answer
  6; with a visited set over cells only, a route that wasted its wall arrives
  first, marks the cell, and blocks a later route that still has its wall.

The block after the next variation runs that last one both ways.

### F. Detect a cycle

**Undirected.** In a search, an edge to an already-seen node that is not the
node you came from closes a cycle. You must skip the parent once (or the road
you just walked would count). Simpler facts help too: a connected component
with c nodes has a cycle exactly when it has c or more edges; and repeatedly
deleting nodes of degree 1 ("peeling leaves") removes everything except the
cycles. [[p:belvedere-trading-distances-to-cycles|Distances to Cycles]] peels
leaves to find the cycle, then runs a multi-source BFS from all the cycle nodes
at once to get every distance. Two variations in one problem.

**Directed.** Here "seen before" is not enough, and it is the second subtle line
of the chapter. In the diamond a→b, a→c, b→d, c→d, the DFS from a reaches d via
b, finishes d, comes back, goes to c, and sees d again. d is seen, but there is no
cycle: d is finished, not an ancestor. A cycle is an edge to a node that is
**still on the current DFS route**. So DFS keeps three colours: white (never
seen), grey (entered, not finished: on the route), black (finished). An edge to a
grey node is a cycle. [[p:oracle-directed-graph-cycle-detection|Detect a Cycle in a Directed Graph]]
uses exactly this diamond as its example of "no cycle", and adds that a
self-loop counts (a node is grey while it scans its own edge to itself).

Directed cycle detection also falls out of [[topological-sort]]: Kahn's
algorithm removes every node exactly when there is no cycle. That chapter
derives it.

```python run
from collections import deque

def directed_cycle_two_marks(n, edges):     # WRONG: seen != on the route
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    seen = [False] * n
    def go(u):
        seen[u] = True
        for v in adj[u]:
            if seen[v] or go(v):
                return True
        return False
    return any(not seen[u] and go(u) for u in range(n))

def directed_cycle(n, edges):               # RIGHT: white 0, grey 1, black 2
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    colour = [0] * n
    def go(u):
        colour[u] = 1                       # on the route
        for v in adj[u]:
            if colour[v] == 1 or (colour[v] == 0 and go(v)):
                return True                 # an edge back into the route
        colour[u] = 2                       # finished: off the route for good
        return False
    return any(colour[u] == 0 and go(u) for u in range(n))

diamond = [(0, 1), (0, 2), (1, 3), (2, 3)]
print("diamond: two marks says", directed_cycle_two_marks(4, diamond),
      "| three colours say", directed_cycle(4, diamond))
assert directed_cycle_two_marks(4, diamond) and not directed_cycle(4, diamond)
assert directed_cycle(3, [(0, 1), (1, 2), (2, 0)])
assert directed_cycle(3, [(2, 2)]) and not directed_cycle(2, [(0, 1), (0, 1)])

def obstacle_bfs(grid, k, state_has_walls):
    R, C = len(grid), len(grid[0])
    start = (0, 0, k)
    seen = {start if state_has_walls else (0, 0)}
    q, steps = deque([start]), 0
    while q:
        for _ in range(len(q)):             # one layer = one step
            r, c, left = q.popleft()
            if (r, c) == (R - 1, C - 1):
                return steps
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    nl = left - grid[nr][nc]
                    key = (nr, nc, nl) if state_has_walls else (nr, nc)
                    if nl >= 0 and key not in seen:
                        seen.add(key)
                        q.append((nr, nc, nl))
        steps += 1
    return -1

g1 = [[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]]
g2 = [[0, 1, 1], [1, 1, 1], [1, 0, 0]]
print("Mercor example 1, node = (r, c, walls left):", obstacle_bfs(g1, 1, True))
print("Mercor example 2:", obstacle_bfs(g2, 1, True))
assert obstacle_bfs(g1, 1, True) == 6 and obstacle_bfs(g2, 1, True) == -1
trap = [[0, 0, 1], [1, 0, 1], [0, 1, 0]]
print("cells-only visited on a trap grid:", obstacle_bfs(trap, 1, False),
      "| with walls in the state:", obstacle_bfs(trap, 1, True))
assert obstacle_bfs(trap, 1, True) == 4 and obstacle_bfs(trap, 1, False) == -1

def distances_to_cycles(n, edges):          # peel leaves, then multi-source BFS
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    deg = [len(a) for a in adj]
    leaves = deque(v for v in range(n) if deg[v] == 1)
    gone = [False] * n
    while leaves:
        v = leaves.popleft()
        gone[v] = True
        for w in adj[v]:
            if not gone[w]:
                deg[w] -= 1
                if deg[w] == 1:
                    leaves.append(w)
    dist = [0 if not gone[v] else -1 for v in range(n)]
    q = deque(v for v in range(n) if not gone[v])   # every cycle node is a source
    while q:
        u = q.popleft()
        for w in adj[u]:
            if dist[w] == -1:
                dist[w] = dist[u] + 1
                q.append(w)
    return dist

print("Belvedere example:", distances_to_cycles(6, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5)]))
assert distances_to_cycles(6, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5)]) == [0, 0, 0, 1, 2, 3]
assert distances_to_cycles(7, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (5, 6)]) == [0, 0, 0, 0, 0, 0, 1]
```

The trap grid is worth tracing. It is 3 x 3, k = 1:

```
0 0 1
1 0 1
0 1 0
```

From (0, 0) the search can step right onto (0, 1) for free, or down onto the
wall (1, 0) by spending its one wall. Both are one step, and the wall step is
put into the queue first. At step 2 both reach the centre (1, 1), and the
wall-spender gets there first, with 0 walls left. With cells-only marking it
claims (1, 1). The honest route arrives a moment later, still holding its wall,
and is turned away. From the centre, every way to the goal crosses one wall, and
the only arrival that was let in has none left: -1. With the walls in the state,
(1, 1, 0) and (1, 1, 1) are different nodes, both survive, and the second one
breaks (1, 2) and reaches the goal in 4 steps.

### G. Bipartite check (two colours)

**What changes:** BFS or DFS assigns colour 0 to the start and the opposite
colour to each newly discovered neighbour; an edge between two nodes of the same
colour means "not bipartite". **Why:** a graph can be split into two sides with
every edge crossing exactly when it has no odd cycle, and BFS layers alternate
sides. Example: a triangle fails (0 and 2 are both one road from 0's colour); a
square passes. See [[bipartite]].

### H. Rarer forms

- **Bidirectional BFS.** Search from both ends and stop when the frontiers meet;
  each side goes half as deep, which matters when the branching factor is large
  (word ladders with long words). Rare in this bank.
- **0-1 BFS.** Edges cost 0 or 1: use a deque, and push a node reached by a 0-cost
  edge to the front. Each node is still settled once. Rare.
- **Representation variants.** A dictionary of lists for labelled nodes (or map
  labels to 0..n-1 first, then use lists); weighted lists of (neighbour, weight)
  pairs for [[dijkstra]]; flat arrays (one array of all neighbours back to back,
  plus a start index per node) for very large graphs; the reversed graph, for
  "who can reach t?" questions and for [[strongly-connected]].
- **Counting instead of searching.** [[p:ibm-drawing-edge|Drawing Edge]]: 
  2^(n(n-1)/2) mod p. No graph is built.

## Recognising it in a statement

Ordered by how much to trust the signal.

1. **"n nodes" (or cities, users, servers) and `edges[i] = [u, v]`.** A graph, given
   plainly. If n is given separately from the edges, isolated nodes exist and
   count.
2. **A grid of characters or 0/1 with "adjacent", "connected horizontally or
   vertically", "spreads", "island", "region".** Grid search with `DIRS`.
3. **"Minimum number of steps / moves / hops / minutes / transformations",** with
   every move the same cost. BFS. Add "from any of" or "simultaneously" and it is
   multi-source.
4. **"Number of groups / islands / provinces / clusters / connected".** Components.
5. **"Transform A into B one change at a time; each intermediate must be valid".**
   An implicit graph over the valid objects; BFS. This is the most common
   disguise in OAs.
6. **"Is it possible to reach / visit all / get out".** Reachability, any search.
7. **A small extra resource: "at most k", "with one key", "you may break".** A
   state graph: (position, resource left).
8. **"Cycle", "deadlock", "circular dependency".** DFS colours (directed), parent
   check or edge count (undirected), or Kahn's count.

**Constraints that confirm it.** n up to 10^5 and m up to 2 x 10^5: an O(n + m)
search, adjacency lists, no matrix. A grid up to 1000 x 1000: O(RC), mark in an
array, iterative (recursion will overflow). Strings of length 8 over 4 letters,
or 3 over 26: an implicit graph small enough to generate.

**Disguises.** "Friends of friends", "infection", "flood", "spread of a rumour",
"water flowing", "network recovery", "mutations", "a lock with wheels", "a
knight on a chessboard": all fewest-steps BFS on a graph the statement never
draws.

**Anti-signals.** Steps with different costs (Dijkstra). "Count the number of
graphs" (combinatorics, as in Drawing Edge). Edges arriving one at a time with
"are they connected now?" (union-find). "All paths" or "all arrangements"
(backtracking). A grid where you only move right and down (a DAG: DP, not BFS).
"Subarray" or "contiguous" (not a graph at all).

## Traps

**Marking on take-out in BFS.** Symptom: some distances are too large, only on
graphs with an odd cycle (a triangle, a pentagon); trees and grids pass. Shown in "The subtle line".

**DFS for shortest paths.** Symptom: correct on trees and paths, too large on
anything with two routes to a node. The triangle is the counterexample.

**`adj = [[]] * n`.** All n rows are one list object, so every node appears to
neighbour every edge endpoint. Symptom: components collapse to 1 or 2, no error.

**Storing an undirected edge once.** Symptom: reachability is right from some
starts and wrong from others; it hides whenever the search happens to start at
the right end.

**Taking the node set from the edges.** Symptom: component counts short by the
number of isolated nodes; samples pass because samples rarely have any.

**A visited set over positions when the state is bigger.** Symptom: -1 or too
large on mazes where the first arrival is the wrong one (the trap grid above).

**Two marks in directed cycle detection.** Symptom: a diamond reported as a
cycle. Use three colours.

**`list.pop(0)` as a queue, and recursion on big inputs.** Symptoms: time limit
on large tests that pass small ones; `RecursionError` on a long chain.

**Forgetting the unreachable case.** Rotten Oranges wants -1 if a fresh orange is
never reached; BFS just leaves it at -1 and the maximum over the reached ones
looks like a valid answer. Check every target got a distance.

```python run
def components(n, adj):
    seen, count = [False] * n, 0
    for s in range(n):
        if not seen[s]:
            count += 1
            seen[s], stack = True, [s]
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if not seen[v]:
                        seen[v] = True
                        stack.append(v)
    return count

def reachable(adj, s, t):
    seen, stack = {s}, [s]
    while stack:
        u = stack.pop()
        if u == t:
            return True
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return False

n, edges = 5, [(0, 1), (2, 3)]        # truth: {0,1}, {2,3}, {4}: 3 components

right = [[] for _ in range(n)]
for u, v in edges:
    right[u].append(v)
    right[v].append(u)

aliased = [[]] * n                    # bug 1: five names for ONE list
for u, v in edges:
    aliased[u].append(v)
    aliased[v].append(u)

one_way = [[] for _ in range(n)]      # bug 2: an undirected edge stored once
for u, v in edges:
    one_way[u].append(v)

labels = sorted({x for e in edges for x in e})   # bug 3: nodes taken from edges
idx = {x: i for i, x in enumerate(labels)}
inferred = [[] for _ in labels]
for u, v in edges:
    inferred[idx[u]].append(idx[v])
    inferred[idx[v]].append(idx[u])

print("correct            ", right, "-> components", components(n, right))
print("[[]] * n           ", aliased, "-> components", components(n, aliased))
print("one direction only  reachable(1 -> 0):", reachable(one_way, 1, 0),
      "| correct:", reachable(right, 1, 0))
print("nodes from edges   ", inferred, "-> components", components(len(labels), inferred))
assert components(n, right) == 3
assert components(n, aliased) == 2 and aliased[0] is aliased[4]
assert reachable(right, 1, 0) and not reachable(one_way, 1, 0)
assert components(len(labels), inferred) == 2     # node 4 never existed

def rot_minutes(grid):                # the -1 case must be checked explicitly
    from collections import deque
    R, C = len(grid), len(grid[0])
    q = deque((r, c) for r in range(R) for c in range(C) if grid[r][c] == 2)
    minute = {cell: 0 for cell in q}
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1 and (nr, nc) not in minute:
                minute[(nr, nc)] = minute[(r, c)] + 1
                q.append((nr, nc))
    fresh = sum(row.count(1) for row in grid)
    reached = len(minute) - sum(row.count(2) for row in grid)
    return max(minute.values(), default=0) if reached == fresh else -1

print("rotten oranges:", rot_minutes([[2, 1, 1], [1, 1, 0], [0, 1, 1]]),
      rot_minutes([[2, 1, 1], [0, 1, 1], [1, 0, 1]]), rot_minutes([[0, 2]]),
      rot_minutes([[2, 1, 1, 1, 2]]))
assert rot_minutes([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert rot_minutes([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
assert rot_minutes([[0, 2]]) == 0 and rot_minutes([[2, 1, 1, 1, 2]]) == 2
print("three build bugs, three wrong answers, and not one exception")
```

## What to memorise

**The template**, BFS, which with `pop()` instead of `popleft()` is DFS:

```
adj = [[] for _ in range(n)]            # n from the statement
for u, v in edges: adj[u].append(v); adj[v].append(u)
dist = [-1] * n; dist[s] = 0; q = deque([s])     # many sources: all at 0
while q:
    u = q.popleft()
    for v in adj[u]:                    # or: for dr, dc in DIRS, with bounds
        if dist[v] == -1:
            dist[v] = dist[u] + 1       # mark at discovery
            q.append(v)
```

**The sentence:** what you can reach from a node does not depend on how you got
there, so explore each node once; with a queue, the first visit is the shortest.

**The question:** once I have reached a node, what does the rest of the search
need to know about how I got there? That is what a node is.

**The habit:** mark when you push, never when you pop.

Numbers: O(n + m) with lists, O(n^2) with a matrix, O(RC) on a grid; the sum of
degrees is 2m; a component with c nodes and c or more edges has a cycle; the
recursion limit is about 1000.

## Check yourself

:::check
Hand trace. Undirected graph, n = 6, edges 0-1, 0-2, 1-3, 2-3, 3-4, 2-5, with each
list in increasing order. Run BFS from 0. Write the queue after every take-out
and the final dist. Then say which take-out sees a neighbour that is already
waiting in the queue.
--
adj: 0 [1, 2], 1 [0, 3], 2 [0, 3, 5], 3 [1, 2, 4], 4 [3], 5 [2].

Take 0: see 1 (1), 2 (1). Queue [1, 2].
Take 1: 0 seen; see 3 (2). Queue [2, 3].
Take 2: 0 seen; 3 already has dist 2 and is waiting in the queue, skip; see 5 (2).
Queue [3, 5].
Take 3: 1, 2 seen; see 4 (3). Queue [5, 4].
Take 5: 2 seen. Queue [4].
Take 4: 3 seen. Queue [].

dist = [0, 1, 1, 2, 3, 2]. The take-out of 2 finds 3 already waiting: 3 was
discovered from 1, and 2 would give it the same distance, 2, so nothing is lost;
with marking on take-out, 3 would be pushed a second time.
:::

:::check
Hand trace, multi-source. Grid (0 empty, 1 fresh, 2 rotten):

```
2 1 0 1
1 1 1 1
0 0 1 2
```

Write the minute each orange rots, and the answer.
--
Minute 0: the sources (0,0) and (2,3), both in the queue at the start.
Minute 1: from (0,0): (0,1), (1,0). From (2,3): (1,3), (2,2).
Minute 2: from (0,1): (1,1). From (1,3): (0,3), (1,2). (1,2) is also next to
(2,2); whichever is taken out first marks it, the other skips it.
Minute 3: nothing fresh is left to rot.

```
0 1 . 2
1 2 2 1
. . 1 0
```

Every fresh orange got a minute, so the answer is 2. A single BFS from (0,0)
alone would have said 5, the minute (0,3) is reached the long way round.
:::

:::check
Hand trace, directed cycles. Edges 0→1, 1→2, 0→2, 2→3, 3→1, lists in increasing
order. Run the three-colour DFS from 0 and write the colours when the cycle is
found. Which edge reports it? Then remove 3→1 and say which edge a two-mark DFS
would wrongly report.
--
Enter 0 (grey). Edge 0→1: 1 is white, enter 1 (grey). Edge 1→2: enter 2 (grey).
Edge 2→3: enter 3 (grey). Edge 3→1: 1 is grey, on the route 0, 1, 2, 3. Cycle
1→2→3→1, reported by the edge 3→1. Colours at that moment: 0, 1, 2, 3 all grey.

Without 3→1: 3 finishes (black), 2 finishes, 1 finishes, back at 0 the edge 0→2
reaches 2, which is black. Three colours: no cycle. Two marks: 2 is "seen", so
the edge 0→2 is reported as a cycle, and it is not one. 0→1→2 and 0→2 are two
routes to the same node, a diamond with one side shortened.
:::

:::check
Why must BFS mark a node when it is pushed, rather than when it is taken out?
Answer in terms of the proof, not of an example.
--
The proof's lemma needs every node to be pushed at most once and to keep the
distance it got at that push. A node sits in the queue between being discovered
and being taken out. If the mark is only set at take-out, any node taken out in
that window that also neighbours it sees it as unmarked and pushes it again,
with dist one more than the taker's. Since the taker can be in the same layer,
that overwrites a correct distance d with d + 1. The induction step "if v was
marked earlier, its distance is at most k + 1" relied on the mark being visible
from the moment of discovery.
:::

:::check
Someone says: "My DFS records the depth at which each node is first reached, and
it passed all the tree tests, so it computes shortest distances." Where are they
wrong, and what is the smallest graph that shows it?
--
On a tree there is exactly one route to each node, so any search finds the
shortest one; the tests had no second route to get wrong. DFS reaches a node by
whatever route it happens to dive along first, and the visited mark then
prevents a shorter route from improving it.

The triangle 0-1, 1-2, 0-2 with adj[0] = [1, 2] shows it: DFS from 0 goes to 1,
then from 1 to 2, recording depth 2. The edge 0-2 is then skipped because 2 is
seen. The true distance is 1. BFS's queue is what guarantees the first visit is
a shortest one.
:::

:::check
Reduce this disguised problem. "A lock has 4 wheels, each showing 0 to 9. One
move turns one wheel one notch up or down (9 wraps to 0). Some combinations are
forbidden. Starting at 0000, what is the fewest moves to reach a target?" Name
the nodes, the edges, the algorithm, and the worst-case size.
--
Nodes: the 10^4 combinations "0000" to "9999", minus the forbidden ones. Edges:
each combination has 8 neighbours (4 wheels, up or down), generated, not stored.
Every move costs 1, so BFS from "0000", with the forbidden set treated as
already seen (and "0000" itself checked first: if it is forbidden, the answer is
-1).

Size: at most 10^4 nodes and 8 x 10^4 edge checks, each building a 4-character
string. Tiny. The skill is seeing that "fewest moves between configurations" is
a shortest path on a graph whose nodes are configurations.
:::

:::check
Someone solves the obstacle-elimination grid with BFS over (row, col) and a
visited set of cells, and keeps "walls left" as extra data on each queue entry.
It passes the two examples. Where are they wrong?
--
The future from a cell depends on how many walls are left, so (cell, walls left)
is the node. With a visited set over cells, the first arrival at a cell claims
it, even if it got there by spending its wall, and a later arrival with walls to
spare is turned away. If the only way to the goal needs that spare wall later,
the answer becomes -1 or too long.

The 3 x 3 trap grid in the Variations shows it: the route that spends its wall
on (1, 0) reaches the centre at the same step as the route that kept its wall,
but it is first in the queue, so it claims the cell. The route with the wall to
spare is refused, and the answer becomes -1 instead of 4. The fix is the visited
set over (row, col, walls left), at most R x C x (k + 1) nodes, with k capped at
R + C - 2.
:::
