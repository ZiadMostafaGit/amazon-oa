# Tries (Prefix Trees)

> A trie stores every prefix of every word exactly once, as a node you reach by spelling it from the root, so any question about "the words that begin with p" costs one step per letter of p, no matter how many words there are.

## The problem it solves

You are building the search box of a shop. The catalogue holds a hundred thousand
product names. Every time the customer types a letter, you must answer a question
about the text typed so far, which is a prefix: does any product start with it,
how many do, which three come first in alphabetical order. Products are added and
removed while the shop is open.

Take a tiny catalogue to have something to hold:

```
car   cat   card   do   dog
```

The customer types `c`, then `ca`, then `car`. The answers to "how many products
start with this?" are 3, 3, 2. The answer to "is this exactly a product?" is
no, no, yes.

The first solution anyone writes is to scan the list.

```python
def count_prefix(words, p):
    return sum(1 for w in words if w.startswith(p))
```

It is correct, and for five words it is instant. Now count it. One query reads
every stored word, and each comparison reads up to |p| letters. With N stored
words and Q queries, that is about N x Q x |p| letter comparisons. The bank's
[[p:bloomberg-implement-trie|Implement Trie]] allows 100,000 operations whose
strings total 500,000 letters. Split that as 50,000 short inserts followed by
50,000 queries, and the scan does 50,000 x 50,000 = 2.5 x 10^9 comparisons. That
does not finish in Python, and it does not finish quickly in any language.

The second solution is a hash set. It is the right tool for one question and the
wrong tool for the one we have.

- "Is `car` exactly a product?" A set of words answers it in one lookup. If that
  is all a problem asks, as in
  [[p:whatnot-exact-string-matching|Exact String Matching]], use the set and stop
  reading this chapter.
- "Does any product start with `ca`?" The set of words cannot say. `ca` is not in
  it, but `car` is. The set knows whole words only.

What this chapter builds answers every prefix question in time proportional to
the length of the prefix, independent of how many words are stored, supports
inserts and deletes in the same time, and turns out to be the backbone of several
other techniques: searching a dictionary inside a grid, matching many patterns in
one pass over a text, and finding the largest XOR of two numbers. It is a tree
([[trees]]) whose edges are labelled with characters ([[strings]]).

### When it is the wrong tool

- **Exact membership only.** A set of strings is simpler and uses far less
  memory. Reach for the trie only when prefixes matter.
- **The words never change and you only need prefix counts or ranges.** Sort the
  words once. All words starting with `ca` form one contiguous block of the
  sorted list, and two binary searches find its ends. That costs O(|p| log N) per
  query and almost no memory. The trie wins when words are inserted between
  queries, when you need wildcards, or when the "word" is a stream of bits.
- **One pattern, one text.** Searching a text for a single word is
  [[string-matching]] (KMP or Z). The trie version of that idea, Aho-Corasick, is
  for *many* patterns at once.
- **Substrings rather than prefixes.** "Does p occur anywhere inside some stored
  word?" A trie of the words cannot answer it. A trie of all *suffixes* can, and
  that idea grown up is a suffix array or automaton ([[suffix-structures]]).
- **Questions about order of keys, not their spelling.** "The smallest key
  greater than x" is an [[ordered-set]] question.

Sixty-four problems in this bank use a trie. They split into four families, and
each family is one technique of this chapter: the basic insert, search and
starts-with; counting the words with a prefix; a trie walked by a DFS to search
many words at once; and a trie over bits for the maximum XOR. The chapter also
covers Aho-Corasick, the multi-pattern matcher built on a trie.

## Build it from the brute force

We start from the scan, find exactly where it wastes work, and remove the waste.
The trie will appear at the end as the obvious data structure.

### Step 1: count the scan

The scan answers `count_prefix(words, "car")` by comparing `car` against all five
words.

| word | letters compared | starts with car? |
|---|---|---|
| car | c, a, r | yes |
| cat | c, a, t (mismatch) | no |
| card | c, a, r | yes |
| do | d (mismatch) | no |
| dog | d (mismatch) | no |

Eleven letter comparisons for one query. Look at what they were. `c` was compared
three times against three different words that all start with `c`. `a` three
times. The words `car` and `card` were each read in full, though `card` *is*
`car` plus a letter. The work is not proportional to the answer; it is
proportional to the whole catalogue, every single time.

### Step 2: notice the waste

The waste has one shape: **many words share the same beginning, and the scan
re-reads that shared beginning once per word.** Every word that starts with `ca`
makes the scan read `c` and `a` again.

So try the obvious cure for repeated work: compute every prefix once, ahead of
time, and store it. Make a dictionary from each prefix to the number of words
that start with it.

```
c:3  ca:3  car:2  card:1  cat:1  d:2  do:2  dog:1
```

A query is now one dictionary lookup. That is real progress. It is also our first
wrong instinct, so it gets a section.

### You might think: "Store every prefix in a hash map. Done."

It works, and it costs too much. A word of length L has L prefixes, of lengths
1, 2, ..., L. Stored as separate strings they hold 1 + 2 + ... + L = L(L+1)/2
letters. For `card` that is 10 letters to store a 4-letter word. The Bloomberg
problem allows words of length 1,000: one such word puts 500,500 letters into the
map, about five hundred times the word itself. And every lookup still hashes the
whole prefix, so a query of length |p| costs O(|p|) anyway.

Worse, the map has thrown information away. It knows that 2 words start with
`car`, but not which. Ask for "the three alphabetically first products that start
with `ca`", which is what a search box shows, and the map has nothing to offer:
the words below `ca` are not reachable from the entry for `ca`.

Look at the stored strings again, though. `card` is stored, and so is `car`, which
is `card` minus its last letter, and `ca`, which is `car` minus its last letter.
Every prefix is its parent prefix plus one letter. Those strings are not
independent at all; they form a tree.

### Step 3: share the prefixes

Draw each distinct prefix as a box, and connect each prefix to the prefix one
letter shorter. The empty prefix is at the top. Its children are `c` and `d`.
`c` has one child, `ca`. `ca` has two, `car` and `cat`. `car` has one, `card`.
On the other side, `d` has `do`, and `do` has `dog`.

Now the key move. A box does not need to store its whole string. The string is
spelled by the path from the top: to reach `card`, go `c`, then `a`, then `r`,
then `d`. So each box stores only a map from "next letter" to "child box". The
letters shared by many words are now stored once, on the shared part of the path,
which is exactly where the scan was wasting its time.

That tree is the trie. Its name comes from re*trie*val. Each node is a prefix.
Each edge is one letter. The node for a prefix p is found by starting at the root
and following the letters of p, one step per letter, and that walk is all a query
ever does.

### The question that unlocks it

Why could all those words share boxes? Because a prefix question does not care
about the rest of the word. `card` and `care` and `cart` are different words, but
to the question "does anything start with `car`?" they are the same: they all
pass through `car`. So ask, on every problem in this family:

**What do all the strings that begin with p have in common, and can I store that
once?**

The answer is the letters of p themselves, so the trie stores them once, as one
node, and everything that begins with p hangs underneath that node. Anything you
want to know about "the strings starting with p" (whether there are any, how many,
the best three) can be kept *at that node*, and a query becomes: walk to the node,
read what is written there.

Say it a second way. The scan treats the catalogue as N separate strings. The
trie treats it as one tree of shared beginnings. A query in the first picture
visits every string. In the second it visits only the |p| nodes on one path, and
never sees a word that does not start with p.

### You might think: "A leaf is the end of a word."

The tree has a problem. `car` is a word, and so is `card`. The walk for `car`
ends at a node, and that node has a child (`d`). The walk for `ca` also ends at
a node with children, and `ca` is *not* a word. Node shape cannot tell these
apart. "It is a word if the node is a leaf" gives the wrong answer for `car`.
"It is a word if the walk does not fall off" gives the wrong answer for `ca`.

So each node carries one more piece of information: a flag, `end`, that is true
exactly when some stored word ends at this node. Then:

- `search(w)`: walk w; the answer is "the walk did not fall off **and** the node
  has `end` set".
- `starts_with(p)`: walk p; the answer is "the walk did not fall off".

The two operations differ by one condition, and that condition is the subtle line
of the chapter. We will demonstrate it both ways in the code section.

### Step 4: keep the answers at the node

The question "how many words start with p" is now "how many `end` flags are in
the subtree under p's node". You could walk the subtree and count, but that costs
the size of the subtree, which can be the whole catalogue (p = `c` in a shop of
words starting with c).

The cure is the same as before: compute it once and store it. Every insert walks
a path from the root to its last node, and *the words that start with p are
exactly the words whose insert walk went through p's node*. So give each node a
counter, `through`, and add one to it on every node an insert walks through.
Then `count_prefix(p)` is: walk p, return `through`. Delete walks the same path
and subtracts one. The counter is maintained in O(L) per insert or delete and read
in O(|p|) per query.

That pattern generalises, and it is how you should think about every variation:
**whatever you want to know about the words below a node, keep it at the node,
and update it on the insert walk.** A count. The three best suggestions. The index
of the word that ends here. The largest value below.

### The technique in one sentence

A trie is a tree with one node per distinct prefix of the stored strings, reached
by walking the prefix's letters from the root, where each node stores a map from
next letter to child, an end marker, and whatever summary of "the strings below
me" the problem needs, so every operation costs one step per letter.

## Worked by hand

Insert `car`, `cat`, `card`, `do`, `dog` into an empty trie, in that order. Number
the nodes in the order they are created, root = 0. Each node has `kids` (letter to
node), `end` (how many stored words end here), and `through` (how many stored
words pass through here, including those ending here).

| step | insert | walk | new nodes | end set at |
|---|---|---|---|---|
| 1 | car | 0 -c-> **1** -a-> **2** -r-> **3** | 1 (c), 2 (ca), 3 (car) | 3 |
| 2 | cat | 0 -c-> 1 -a-> 2 -t-> **4** | 4 (cat) | 4 |
| 3 | card | 0 -c-> 1 -a-> 2 -r-> 3 -d-> **5** | 5 (card) | 5 |
| 4 | do | 0 -d-> **6** -o-> **7** | 6 (d), 7 (do) | 7 |
| 5 | dog | 0 -d-> 6 -o-> 7 -g-> **8** | 8 (dog) | 8 |

Bold numbers are nodes created in that step. Fifteen letters were inserted and
eight nodes were created (plus the root): six letters were shared.

The story of step 3, in words. "Insert `card`. At the root, is there a child for
`c`? Yes, node 1, made by `car`. Step into it and add 1 to its `through`, because
`card` passes through the prefix `c`. Is there a child for `a`? Yes, node 2. Step,
add 1. Child for `r`? Yes, node 3, which already has `end` = 1 because `car` ends
there. Step, add 1; `card` passes through `car` without ending there. Child for
`d`? No: no stored word so far starts with `card`. Create node 5, step into it,
add 1. The letters are used up, so set `end` = 1 on node 5."

Here is the result. The shaded nodes have `end` set. The number beside a node is
its `through`.

<svg viewBox="0 0 620 380" role="img" aria-label="the trie for car, cat, card, do, dog: the root has children c and d; c leads to a, which has children r and t; r has child d; d leads to o, which has child g. Shaded nodes, where a word ends, are r (car), t (cat), the d under r (card), o (do) and g (dog). Beside each node is the number of words passing through it: root 5, c 3, a 3, r 2, t 1, d under r 1, d 2, o 2, g 1">
  <g>
    <circle cx="310" cy="35" r="20"/>
    <text x="310" y="40" text-anchor="middle">root</text>
    <text x="340" y="40">5</text>
    <line x1="295" y1="49" x2="215" y2="96"/>
    <line x1="325" y1="49" x2="425" y2="96"/>
    <circle cx="200" cy="110" r="18"/>
    <text x="200" y="115" text-anchor="middle">c</text>
    <text x="226" y="115">3</text>
    <circle cx="440" cy="110" r="18"/>
    <text x="440" y="115" text-anchor="middle">d</text>
    <text x="466" y="115">2</text>
    <line x1="200" y1="128" x2="200" y2="167"/>
    <line x1="440" y1="128" x2="440" y2="167"/>
    <circle cx="200" cy="185" r="18"/>
    <text x="200" y="190" text-anchor="middle">a</text>
    <text x="226" y="190">3</text>
    <circle class="fill" cx="440" cy="185" r="18"/>
    <text x="440" y="190" text-anchor="middle">o</text>
    <text x="466" y="190">2</text>
    <text x="410" y="190" text-anchor="end">do</text>
    <line x1="188" y1="199" x2="142" y2="246"/>
    <line x1="212" y1="199" x2="258" y2="246"/>
    <line x1="440" y1="203" x2="440" y2="242"/>
    <circle class="fill" cx="130" cy="260" r="18"/>
    <text x="130" y="265" text-anchor="middle">r</text>
    <text x="156" y="265">2</text>
    <text x="100" y="265" text-anchor="end">car</text>
    <circle class="fill" cx="270" cy="260" r="18"/>
    <text x="270" y="265" text-anchor="middle">t</text>
    <text x="296" y="265">1</text>
    <text x="270" y="300" text-anchor="middle">cat</text>
    <circle class="fill" cx="440" cy="260" r="18"/>
    <text x="440" y="265" text-anchor="middle">g</text>
    <text x="466" y="265">1</text>
    <text x="440" y="300" text-anchor="middle">dog</text>
    <line x1="130" y1="278" x2="130" y2="312"/>
    <circle class="fill" cx="130" cy="330" r="18"/>
    <text x="130" y="335" text-anchor="middle">d</text>
    <text x="156" y="335">1</text>
    <text x="100" y="335" text-anchor="end">card</text>
    <text x="310" y="372" text-anchor="middle">shaded: a word ends here. number: words that pass through the node.</text>
  </g>
</svg>

Point at the picture and check one number of each kind. Node `a` (prefix `ca`)
says 3: the words through it are car, cat, card. Node `r` (prefix `car`) says 2:
car and card. It is shaded because car ends there, and it is not a leaf, because
card goes on. Node `d` on the right (prefix `d`) is not shaded: nobody stored the
one-letter word `d`.

Now the queries. Each is one walk.

| query | walk | node reached | answer | why |
|---|---|---|---|---|
| search ca | c, a | 2 | **false** | node exists, `end` = 0 |
| starts_with ca | c, a | 2 | **true** | node exists |
| count_prefix car | c, a, r | 3 | **2** | `through` of node 3 |
| search cards | c, a, r, d, then no `s` | none | **false** | fell off at `s` |
| search do | d, o | 7 | **true** | `end` = 1 |
| count_prefix "" | (no letters) | 0 | **5** | the root is the empty prefix |

Count the work. `count_prefix car` did three steps, against eleven comparisons
for the scan. More to the point, it would still do three steps with a million
stored words, because it never looks at a word that does not start with `car`.
The scan's cost grows with the catalogue; the walk's cost grows with the query.

### A second trace: deleting, and a delete that must do nothing

Start from the same trie. Delete `car`, then `cat`, then `ca`, then `dog`.

Delete is the insert walk in reverse: walk the word, subtract 1 from `through`
on every node, subtract 1 from `end` on the last one. One extra rule keeps the
tree small: if some node's `through` drops to 0, no stored word goes through it
any more, so cut it off from its parent, and everything below it goes with it.

| step | delete | first check | what changes | after |
|---|---|---|---|---|
| 1 | car | search car: true | root 5→4, c 3→2, a 3→2, r 2→1, end(r) 1→0 | r stays, card still needs it |
| 2 | cat | search cat: true | root 4→3, c 2→1, a 2→1, t 1→**0**: cut t | node 4 is gone |
| 3 | ca | search ca: **false** | nothing | unchanged |
| 4 | dog | search dog: true | root 3→2, d 2→1, o 2→1, g 1→**0**: cut g | node 8 is gone |

After step 1, look at node `r`: `end` = 0 and `through` = 1. So
`search("car")` is now false and `starts_with("car")` is still true, because
card is still stored. This is the end flag doing its job: the node outlives the
word that created it.

Step 3 is the case the first trace could not show. `ca` is a prefix of stored
words, so the walk for `ca` succeeds, but `ca` itself was never inserted. If the
delete walked and subtracted without asking first, it would take 1 from the
`through` of the root, of `c` and of `ca`, and set `end` at `ca` to -1. Then
`count_prefix("c")` would say 0 while card is plainly stored. The counts would
be wrong forever after, and nothing would crash. The one line `if not
search(word): return` is what protects every counter in the tree. It is the
second subtle line, and the code section shows it both ways.

At the end the trie holds `card` and `do`: `count_prefix("")` is 2,
`count_prefix("c")` is 1, `count_prefix("ca")` is 1.

## From the idea to the code

The trace already contains the whole implementation. A node is three fields.
Insert is the walk that creates missing children and adds to counters. Every
query is the walk that stops if a child is missing.

```python run
import random

class Node:
    __slots__ = ("kids", "end", "through")
    def __init__(self):
        self.kids = {}        # next character -> child node
        self.end = 0          # stored words that end exactly here
        self.through = 0      # stored words whose path passes through here

class Trie:
    def __init__(self):
        self.root = Node()
        self.nodes = 1

    def insert(self, word):
        node = self.root
        node.through += 1
        for ch in word:
            if ch not in node.kids:          # first word with this prefix
                node.kids[ch] = Node()
                self.nodes += 1
            node = node.kids[ch]
            node.through += 1
        node.end += 1

    def walk(self, s):                       # the node for prefix s, or None
        node = self.root
        for ch in s:
            node = node.kids.get(ch)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self.walk(word)
        return node is not None and node.end > 0

    def starts_with(self, prefix):
        node = self.walk(prefix)
        return node is not None and node.through > 0

    def count_prefix(self, prefix):
        node = self.walk(prefix)
        return node.through if node else 0

    def delete(self, word):
        if not self.search(word):            # absent: touch nothing
            return False
        node = self.root
        node.through -= 1
        for ch in word:
            child = node.kids[ch]
            child.through -= 1
            if child.through == 0:           # no stored word needs this branch
                del node.kids[ch]
                return True
            node = child
        node.end -= 1
        return True

t = Trie()
for w in ["car", "cat", "card", "do", "dog"]:
    t.insert(w)
print("nodes:", t.nodes, "for", sum(map(len, ["car", "cat", "card", "do", "dog"])), "letters")
print("search ca:", t.search("ca"), " starts_with ca:", t.starts_with("ca"),
      " count car:", t.count_prefix("car"), " count d:", t.count_prefix("d"))
assert t.nodes == 9 and not t.search("ca") and t.starts_with("ca")
assert t.count_prefix("car") == 2 and t.count_prefix("") == 5
t.delete("car")
print("after delete car: search car", t.search("car"), " starts_with car", t.starts_with("car"))
assert not t.search("car") and t.starts_with("car") and t.count_prefix("c") == 2

# against the brute force: a plain list of words, on random operations
random.seed(7)
for trial in range(300):
    t, bag = Trie(), []
    for _ in range(40):
        s = "".join(random.choice("ab") for _ in range(random.randint(0, 4)))
        op = random.choice(["insert", "insert", "delete", "query"])
        if op == "insert":
            t.insert(s); bag.append(s)
        elif op == "delete":
            assert t.delete(s) == (s in bag)
            if s in bag:
                bag.remove(s)
        assert t.search(s) == (s in bag)
        assert t.count_prefix(s) == sum(w.startswith(s) for w in bag)
        assert t.starts_with(s) == any(w.startswith(s) for w in bag)
print("300 random runs agree with scanning the list")
```

The random test at the bottom is the habit worth copying. The scan is slow, but
it is obviously right, so it is the perfect judge. Three hundred random runs over
the alphabet `{a, b}`, with short words, duplicates, the empty string, and deletes
of absent words, exercise every corner of the trie in a fraction of a second.

### Each line, and which part of the idea it is

| line | in plain words | idea |
|---|---|---|
| `self.kids = {}` | where to go for each next letter | the edges of the tree; the node's string is the path, not stored |
| `self.end = 0` | how many stored words stop here | the end flag, as a count so duplicates work |
| `self.through = 0` | how many stored words pass here | the summary kept at the node (Step 4) |
| `node.through += 1` before the loop | every word passes through the root | the root is the empty prefix, which every word has |
| `if ch not in node.kids: ... Node()` | no word so far had this prefix | the only place nodes are created |
| `node = node.kids[ch]` | step one letter down | following the path that spells the word |
| `node.end += 1` after the loop | the word stops at this node | marks the node as a word, not just a prefix |
| `node = node.kids.get(ch)`, `None` | the prefix is not in the tree | falling off: no stored word starts with this |
| `node is not None and node.end > 0` | reached it, and a word ends there | the difference between search and starts_with |
| `if not self.search(word)` in delete | do nothing for a word that is not stored | protects every counter on the path |
| `if child.through == 0: del` | nobody needs this branch any more | keeps the tree equal to the stored words |

Three boring confusions, settled.

**Where is the letter stored?** On the edge, which in code is the key in the
parent's `kids` dict. The child node does not know its own letter, and does not
need to. When you draw a trie with letters inside circles, as above, the letter in
a circle is the label of the edge coming into it. The root has no letter.

**Why does the root count?** The root is the node for the empty prefix, and every
word starts with the empty string. `count_prefix("")` = total words is not a
special case; it is the walk of zero steps. This matters in
[[p:google-dynamic-prefix-query-counts|Dynamic Prefix Query Counts]], whose
statement says an empty prefix matches every stored query.

**Why `end` is a count, not a boolean.** That same problem says duplicate queries
count separately. Insert `car` twice and delete it once: with a boolean, the
delete clears the flag and `car` vanishes although one copy remains. With a count,
`end` goes 2, 1, and the word is still there. If a problem says "repeated
insertion of the same word does not change behavior", as the Bloomberg one does,
a boolean is fine, but then delete must not decrement `through` for a word
inserted twice, and the count version is simply safer.

### The subtle lines, both ways

Two lines in a trie look optional and are not. The first is `and node.end > 0`
in search. The second is the existence check at the top of delete. Here are both,
right and wrong, on the same words.

```python run
class Node:
    def __init__(self):
        self.kids, self.end, self.through = {}, 0, 0

def insert(root, word):
    node = root
    node.through += 1
    for ch in word:
        node = node.kids.setdefault(ch, Node())
        node.through += 1
    node.end += 1

def walk(root, s):
    node = root
    for ch in s:
        node = node.kids.get(ch)
        if node is None:
            return None
    return node

def search_wrong(root, w):            # "I reached the node, so it is a word"
    return walk(root, w) is not None

def search_right(root, w):            # reached the node AND a word ends there
    node = walk(root, w)
    return node is not None and node.end > 0

def delete_wrong(root, word):         # decrements along the path, no check
    node = root
    node.through -= 1
    for ch in word:
        if ch not in node.kids:
            return                    # ran off the trie, but too late
        node = node.kids[ch]
        node.through -= 1
    node.end -= 1

def delete_right(root, word):
    if not search_right(root, word):  # the one line: is it really stored?
        return
    delete_wrong(root, word)          # now every step is safe

words = ["car", "card", "cat"]
for name, search in [("wrong", search_wrong), ("right", search_right)]:
    root = Node()
    for w in words:
        insert(root, w)
    print(name, {q: search(root, q) for q in ["c", "ca", "car", "card", "cards"]})
root = Node()
for w in words:
    insert(root, w)
assert search_wrong(root, "ca") and not search_right(root, "ca")
assert search_right(root, "car") and search_right(root, "card")

for name, delete in [("wrong", delete_wrong), ("right", delete_right)]:
    root = Node()
    for w in words:
        insert(root, w)
    delete(root, "ca")                # "ca" was never inserted
    counts = {p: walk(root, p).through for p in ["", "c", "ca", "car"]}
    print(name, "delete 'ca' ->", counts, " end at ca:", walk(root, "ca").end)
    if name == "wrong":
        assert counts == {"": 2, "c": 2, "ca": 2, "car": 2} and walk(root, "ca").end == -1
    else:
        assert counts == {"": 3, "c": 3, "ca": 3, "car": 2} and walk(root, "ca").end == 0
```

Read the first two output lines side by side. The wrong search says `c` and `ca`
are words. It has computed `starts_with`, exactly, under the name `search`. The
right one agrees with it on `car` and `card` and disagrees on every prefix that is
not itself a word. Notice that neither version is wrong on `cards`: falling off
the tree means "no" in both. So a test suite made only of stored words and of
strings that are not even prefixes will pass the wrong version. The test that
catches it is a proper prefix of a stored word. Always include one.

Now the delete lines. Three words are stored, and all three start with `ca`. After
the wrong delete of the absent word `ca`, the root says 2 words are stored, `c`
says 2, `ca` says 2, and `end` at `ca` is -1. Every one of those is a lie, and
the -1 is the fingerprint: a counter below zero means you subtracted for something
you never added. The right delete asks one question first and leaves the tree
exactly as it was.

A third line deserves a sentence. In `delete`, after cutting off a child whose
`through` became 0, the code returns at once. It does not decrement `end` on the
last node, because that node has just been cut off with everything below it, and
there is nothing left to correct. If you do not prune empty branches at all, the
code is still correct (counts of zero mean "absent"), but `starts_with` must then
test `through > 0`, not just "the node exists", which is why the full
implementation tests both.

### Dict or array of 26?

Many textbooks write `kids = [None] * 26` and index by `ord(ch) - ord('a')`. In C++
or Java that is faster than a hash map. In Python a list of 26 slots per node is
mostly empty slots: the trie above would hold 9 x 26 = 234 slots for 8 edges. A
dict holds only the edges that exist. Use the dict unless the alphabet is tiny
and fixed. The bitwise trie later in the chapter is that case: its alphabet is
{0, 1}, and a list of two slots is perfect.

## Why it is correct

A data structure is correct when every operation keeps a promise about what the
structure *means*. That promise is called the representation invariant. We state
it, check that a fresh trie keeps it, check that each operation that changes the
trie keeps it, and then the queries are correct because they just read it.

:::proof The trie answers every query as the scan would
**Notation.** Let B be the multiset of stored words (a word inserted twice is in B
twice). For a string p, the *node for p* is the node reached from the root by
following the letters of p, if every step exists.

**The invariant.** At every moment, all three of these hold.

1. (Shape) For every string p, the node for p exists if and only if p is a prefix
   of at least one word in B. (The root, the node for the empty string, always
   exists.)
2. (End) The node for p has `end` equal to the number of copies of p in B.
3. (Through) The node for p has `through` equal to the number of words in B that
   start with p, counting copies.

**The walk lemma.** `walk(p)` returns the node for p if it exists, and None
otherwise. By induction on the length of p. For the empty string the walk takes
zero steps and returns the root, which is the node for the empty string. For a
string p followed by a letter x: the walk first reaches the node for p (or has
already returned None, if that node does not exist, in which case the node for px
cannot exist either, because a path to it would pass through the node for p).
From the node for p, the node for px is the child under key x, if any; the walk
looks up exactly that key. ∎

**Start.** An empty trie is one root with no children and zero counters, and B is
empty. No non-empty string is a prefix of a word in an empty B, and no node other
than the root exists, so rule 1 holds (the root is allowed by definition). Every
count is 0, and B has 0 copies of anything and 0 words starting with anything, so
rules 2 and 3 hold. The invariant holds.

**Insert w.** Let w = x1 x2 ... xL. Adding w to B changes exactly these facts:
each prefix x1..xk (k = 0..L) of w becomes a prefix of a word in B (maybe it
already was); the number of words starting with x1..xk grows by 1 for each k from
0 to L, and for no other string; and the number of copies of w grows by 1. The
code walks the prefixes of w in order, creates the node for x1..xk exactly when it
is missing (so rule 1 holds afterwards, and no node for anything else is created),
adds 1 to `through` on each of the L+1 nodes on the path (rule 3), and adds 1 to
`end` on the last one (rule 2). Nothing else is touched.

**Delete w, when w is in B.** Removing one copy of w changes the counts in the
mirror way: `through` drops by 1 on the L+1 nodes for the prefixes of w, `end`
drops by 1 at the node for w. The code does exactly that. If some `through`
reaches 0 at the node for x1..xk, then by rule 3 no word in B starts with x1..xk
any more, so by rule 1 that node and every node below it (each of which is the
node for a longer string starting with x1..xk) must disappear, and cutting the
edge from the parent removes exactly that subtree. The counters inside the removed
subtree no longer matter, because those nodes are unreachable.

**Delete w, when w is not in B.** B does not change, so the trie must not change.
The code first runs `search(w)`; by the walk lemma and rule 2 it returns false
exactly when w has 0 copies in B, and then the code returns without writing.

**Queries.** By the walk lemma and the invariant: `search(w)` is true exactly when
the node for w exists and B holds at least one copy of w; `starts_with(p)` is true
exactly when the node for p exists with `through` > 0, that is, when some word in
B starts with p; `count_prefix(p)` returns the number of words in B starting with
p, or 0 if there is no node, which is also correct by rule 1. Each answer equals
what the scan over B computes.

**Termination.** Every operation is one loop over the letters of its argument. ∎
:::

The proof leaned on a few facts. Each is a place where a variation must take care.

- **A string is a sequence of symbols from a fixed alphabet, read in one
  direction.** The walk lemma reads p left to right. Questions about suffixes are
  answered by reversing the strings before inserting them (variation D), not by
  walking a prefix trie backwards.
- **The summary at a node is something an insert can update on its walk.**
  `through` changes by exactly 1 on exactly the path nodes. A summary like "the
  three alphabetically first words below me" also changes only on the path, so it
  is maintainable. A summary that depends on the whole tree (say, "my rank among
  all nodes") is not, and does not belong at the node.
- **Delete is only for stored words.** The invariant breaks the moment you
  subtract for a word you never added. The check costs one walk and is not
  optional.
- **Equal strings land on the same node.** That is why counts, not flags, are
  needed when duplicates are meaningful. Case-insensitive problems must normalise
  before inserting, or `Car` and `car` become two different paths.

## What it costs

**Time.** Insert, search, starts_with, count_prefix and delete each do one step
per letter of their argument, and each step is a dict lookup and maybe an
assignment, constant time on average. So each costs O(L), with L the length of the
argument. The number of stored words N does not appear. That is the whole point:
the scan was O(N·L) per query.

For [[p:bloomberg-implement-trie|Implement Trie]], the total length of all
operation strings is at most 500,000, so the total work is O(500,000) steps,
however the operations are split between inserts and queries.

**Space.** Each insert creates at most L new nodes, so the trie never has more
nodes than the total length of all inserted words, plus the root. Sharing makes it
smaller: the five words above have 15 letters and 8 nodes. The worst case is no
sharing at all (words with distinct first letters), when nodes = letters.

**The cost people forget: the constant.** A node in Python is an object with a
dict, and even a one-entry dict is around two hundred bytes, not one byte per letter.
A trie of 500,000 letters can easily take a hundred megabytes. It is the price of
generality. When memory matters, store the trie in flat lists (`kids` as a list of
dicts, `end` and `through` as lists of ints indexed by node number, as the
Aho-Corasick code below does), use `__slots__` on the node class as above, or
use a list of two for a binary alphabet. In C++ or Java the equivalent is an array
of 26 child indices per node, sized from the total length up front.

**Comparing with the alternatives.**

| approach | per query | per insert | memory | can enumerate words under p? |
|---|---|---|---|---|
| scan the list | O(N·len(p)) | O(1) | the words | yes, slowly |
| hash map of every prefix | O(len(p)) to hash | O(L^2) | O(sum of L^2) | no |
| sorted list, two binary searches | O(len(p) log N) | O(N) to shift | the words | yes, a slice |
| trie | O(len(p)) | O(L) | at most the letters, times a node's size | yes, a DFS below the node |

**Enumeration is output-sensitive.** "List every word starting with p" is the walk
to p's node, O(|p|), plus a DFS of the subtree below it. The subtree has at least
one node per letter of output that is not shared, so the DFS costs about the size
of the answer. If a problem only wants the first three (autocomplete), a DFS that
visits children in sorted order can stop after three words, or you can store the
best three at every node during insert, which makes each query O(|p|) at the price
of three entries per node.

**Bitwise trie.** Numbers are fixed-width strings of B bits (B = 30 for values up
to 10^9, since 2^30 is about 1.07 x 10^9). Insert and query are O(B), the trie has
at most N·B + 1 nodes, and with two children per node it is far cheaper per node
than the dict version.

**Aho-Corasick.** Building costs O(total pattern length) node steps plus the
failure links, which amortise to the same order; scanning a text of length n costs
O(n + number of matches reported). The brute force it replaces costs
O(n x longest pattern).

## How to think about it

The template is short. The skill is seeing what the "characters" are, which
direction the question points, and what to keep at a node. Ask these, in order,
on every problem that smells of prefixes.

1. **What is a character?** Letters, usually. But it can be a decimal digit
   ([[p:capital-one-longest-common-prefix-of-number-pairs|Longest Common Prefix of Number Pairs]]),
   a bit (the XOR problems), a path component such as `/a/b/c` split on slashes
   ([[p:google-design-file-system|Design File System]]), or a whole word of a
   multi-word company name. Whatever you walk one step at a time is the character.
2. **Which way does the question point?** Either the *query is a prefix of the
   stored strings* ("which products start with what I typed") and you walk the
   query and read the node at the end; or the *stored strings are prefixes of the
   query* ("does this word start with any stored prefix", "which tokens match at
   this position") and you walk the query and watch the `end` flags you pass on
   the way. Same trie, different reading.
3. **Prefix or suffix?** A suffix question is a prefix question about reversed
   strings.
4. **What does a node need to know about the strings below it?** An end marker
   always. Then whatever the query asks: a count, the word itself (so a DFS can
   report it), the best k, a maximum, an index. Update it on the insert walk.
5. **Is the query exact, or does it branch?** A wildcard, a grid, a set of
   possible next letters: then the walk becomes a DFS through the trie, with the
   trie pruning every dead prefix.
6. **Many patterns, one text?** Then the trie is the dictionary of patterns and
   failure links make it scan the text once: Aho-Corasick.
7. **Numbers and XOR?** A bitwise trie of fixed width, walked greedily from the
   top bit.
8. **Static or dynamic, and how big?** If nothing changes and you only count or
   list by prefix, sorted strings with binary search may be simpler. If memory is
   tight, flat arrays.

Before writing code, say three things out loud: **what a node represents**,
**what is stored at it**, and **what the walk does when a child is missing**. If
you can say those three, the code writes itself.

### Telling it from its neighbours

- **Hash set** ([[hash-tables]]): exact strings only. If you never ask about a
  prefix, the trie is overhead.
- **Sorted strings plus [[binary-search]]**: static prefix ranges, small memory.
  No wildcard, no XOR, slow inserts.
- **[[string-matching]] (KMP, Z)**: one pattern in one text. Aho-Corasick is its
  many-pattern generalisation; KMP's failure function is exactly an Aho-Corasick
  failure link on a trie that is a single path.
- **[[rolling-hash]]**: compares substrings in O(1) after preprocessing; good for
  "does this substring occur", weaker for "list everything with this prefix".
- **[[suffix-structures]]**: a trie of every suffix answers substring questions.
  For tiny texts, a plain trie of all suffixes is enough; past a few thousand
  characters, use a suffix array.
- **[[dp-strings]] such as word break**: the DP over positions is the algorithm.
  A trie only speeds up its inner loop, "which dictionary words start at
  position i", by walking forward from i once instead of testing every word.

## Variations

Thirteen variations, ordered roughly by how often you will meet them. A, B, C, D,
F and G are everyday interview material. E, H, I and J are regular in OAs. K and L
appear in design rounds and harder OAs. M is rare.

### A. Insert, search, starts_with (the core)

**What changes.** Nothing; this is the chapter's code. **Why.** Every other
variation is this plus something kept at the node or a different walk.

**Example.** Insert `dog`; search `do` is false, starts_with `do` true; insert
`do`; search `do` is true. That is exactly example 1 of
[[p:bloomberg-implement-trie|Implement Trie]]: `do` is first only a prefix, and
inserting it makes a later search succeed. Note that the second insert creates no
node: the path already exists, and only `end` changes.

### B. Counting: how many words start with p, and pair counts

**What changes.** The `through` counter, and `end` as a count. Delete with the
existence check.

**Why.** The words starting with p are the words whose insert walk passed p's
node.

**Example.** Insert `car`, `car`, `cat`; count `ca` = 3, count `car` = 2; delete
`car`; count `car` = 1. The bank's
[[p:google-dynamic-prefix-query-counts|Dynamic Prefix Query Counts]] is this
exactly, with duplicates and deletes of absent queries that must change nothing.

**A pair-counting twist.** "Count pairs i < j where one word is a prefix of the
other." Process the words in order. For each new word w, before inserting it, the
earlier words that are prefixes of w are the `end` counts on the nodes along w's
path (including its last node, which counts equal words); the earlier words that
w is a proper prefix of are `through` at w's node minus `end` there. Add both,
then insert w. One walk per word.
[[p:uber-word-pairs|Word Pairs]] is this.

### C. Autocomplete: the best k words under a prefix

**What changes.** Either store, at every node, the best k words below it (updated
on insert), or store the word at its end node and run a DFS below the query node
that visits children in sorted order and stops after k.

**Why.** All words starting with the typed text live under one node. As the user
types one more letter, the query node moves one step down, so you can keep the
current node between keystrokes instead of re-walking from the root.

**Example.** Products `mobile`, `mouse`, `moneypot`, `monitor`, `mousepad`, typed
`mou`: the node for `mou` has `mouse` and `mousepad` below it; sorted, those are the
suggestions. [[p:citadel-search-suggestions-prefix-tree|Search Suggestions with a Prefix Tree]]
asks for the first three alphabetically after every keystroke, and says that once
a prefix has no matches every longer prefix has none: in trie terms, once the walk
falls off, it stays off. [[p:pinterest-autocomplete-system|Autocomplete System]]
ranks by frequency and updates frequencies when a sentence is committed with `#`,
which is "insert again and update the summaries on the path".

### D. Suffixes: reverse, then it is a prefix problem

**What changes.** Insert each word reversed; query with the reversed suffix.

**Why.** "w ends with s" is "reverse(w) starts with reverse(s)".

**Example.** Words `seat`, `at`, `cat`: reversed `taes`, `ta`, `tac`. "Which words
end with `at`?" Walk `ta`: `through` = 3. The bank's
[[p:roblox-solution|Suffix Pairs]] is variation B's pair count on reversed words,
and [[p:anduril-add-word-suffix-search|Add Word and Suffix Search]] is search and
starts_with on reversed words.

### E. Stored strings as prefixes of the query: watch the flags on the way down

**What changes.** The walk reads the query, and the answer is about the `end`
flags it *passes*, not the node it ends on.

**Why.** "Does w start with any stored prefix?" is "does the walk for w pass a
node with `end` set before it falls off or ends?" "The longest dictionary token
matching at position i" is "walk the text from i and remember the last `end` node
you passed".

**Example.** Stored prefixes `ab`, `b`; words `abc`, `ba`, `ca`. `abc`: walk a
(no flag), b (flag): matches. `ba`: b (flag): matches. `ca`: falls off at c: no.
[[p:datadog-prefix-filter|Filter Words by Stored Prefixes]] is this;
[[p:google-longest-dictionary-tokenization|Longest Dictionary Tokenization]] and
[[p:anthropic-unknown-symbol-tokenizer|Longest-Match Tokenizer with Unknown Symbols]]
are longest-match, walking from each position; and
[[p:bloomberg-ip-prefix-store|IP Prefix Store]] is the same over a binary
alphabet, where an address is covered when its walk passes any stored prefix.
The trap in longest match is to stop at the *first* flag; you must keep walking
and remember the *last* one.

### F. Wildcard search: the walk branches

**What changes.** A `.` matches any one letter, so at a `.` the walk tries every
child. Search becomes a DFS over (position in pattern, trie node).

```python
def find(node, pattern, i):
    if i == len(pattern):
        return node.end > 0
    ch = pattern[i]
    if ch != ".":
        nxt = node.kids.get(ch)
        return nxt is not None and find(nxt, pattern, i + 1)
    return any(find(nxt, pattern, i + 1) for nxt in node.kids.values())
```

**Why.** A `.` is a prefix question with 26 possible prefixes, and the trie
answers all of them by having the children right there; letters that no stored
word uses are never tried.

**Example.** Stored `bad`, `dad`, `mad`. `.ad`: three children at the root, each
continues with a, d: true. `b..`: one child, then any, any: true. `..e`: every
two-letter path, none has an `e` child: false. The worst case is a pattern of all
dots, which visits every node of that depth.
[[p:amazon-wildcard-word-dictionary|Word Dictionary with Wildcard Find]] is this;
note that the `.` matches exactly one letter, so the length must match too, which
the `end` test at `i == len(pattern)` enforces.

### G. Word Search II: a grid DFS that walks the trie alongside

**What changes.** Instead of searching the grid once per word, put all words in a
trie and run one DFS from every cell, carrying the current trie node. Step to a
neighbour only if the trie has a child for its letter.

**Why.** Searching word by word re-explores the same grid paths for every word
sharing a prefix. With the trie, a grid path is abandoned the moment its letters
are not a prefix of *any* word, and one path serves every word with that prefix.
This is the [[backtracking]] grid search with the trie as its prune.

**Example.** Board `oa / et`, words `oat`, `eat`, `oe`. From `o`: trie has `o`;
neighbour `a` (prefix `oa`, in trie), then `t` (`oat`, a word: report); neighbour
`e` (`oe`, a word: report). From `e`: `ea`, `eat`: report. Every grid path that
is not a prefix of a word dies at its first step.

Two details decide whether it passes. Mark the cell on the way in and restore it
on the way out, so a path cannot reuse a cell but another path can. And when you
report a word, remove its end marker (or the word) from the trie, so a second grid
path spelling the same word does not report it again; that is shown in the Traps
section. [[p:amazon-word-search-ii|Word Search II]] is the bank's version.

### H. Trie as the prune of a backtracking search

**What changes.** A backtracking search builds a string piece by piece; the trie
answers "can this partial string still become something valid?" in O(1) per
letter by keeping the current node.

**Why.** Backtracking is only as fast as its prune, and "is this a prefix of some
dictionary word" is the most common prune there is.

**Example.** [[p:inmobi-word-squares|Word Squares]]: after placing rows `ball` and
`area`, the third row must start with the third letters of the rows so far,
`le`. A trie keyed by prefixes (with, at each node, the list of words below it)
hands you exactly the words that start with `le`, and nothing else is tried. Word
Break II ([[p:amazon-word-break-ii|Word Break II]]) uses the trie the same way: from
position i, walk the text forward through the trie and every `end` flag you pass
is a word that can be cut here.

### I. Bitwise trie: the maximum XOR

**What changes.** Insert each number as its bits from the most significant to the
least, always the same width B. To find the best partner for y, walk down, and at
each bit go to the child with the *opposite* bit if it exists, otherwise the
same bit.

**Why greedy is right here.** XOR is 1 at a bit exactly when the bits differ.
Bit b is worth 2^b, and 2^b is larger than all lower bits together
(2^(b-1) + ... + 1 = 2^b - 1). So making the top bit of the XOR 1 beats any
choice of the lower bits, and the walk can decide bits from the top down without
ever regretting a decision. This is the reason the trie must go *top bit first*.

```python run
import random

def max_xor(arr1, arr2, bits=30):
    root = [None, None]                      # a node is [child for 0, child for 1]
    for x in arr1:                           # insert every number, top bit first
        node = root
        for b in range(bits - 1, -1, -1):
            bit = (x >> b) & 1
            if node[bit] is None:
                node[bit] = [None, None]
            node = node[bit]
    best = 0
    for y in arr2:                           # for each y, walk toward the opposite bit
        node, got = root, 0
        for b in range(bits - 1, -1, -1):
            want = 1 - ((y >> b) & 1)        # this bit of the xor is 1 if we can go there
            if node[want] is not None:
                got |= 1 << b
                node = node[want]
            else:
                node = node[1 - want]        # forced: the other child must exist
        best = max(best, got)
    return best

def trace(arr1, y, bits):
    print("y = %d = %s" % (y, format(y, "0%db" % bits)))
    root = [None, None]
    for x in arr1:
        node = root
        for b in range(bits - 1, -1, -1):
            bit = (x >> b) & 1
            node[bit] = node[bit] or [None, None]
            node = node[bit]
    node, got, path = root, 0, ""
    for b in range(bits - 1, -1, -1):
        yb = (y >> b) & 1
        want = 1 - yb
        if node[want] is not None:
            got |= 1 << b; path += str(want); node = node[want]; note = "opposite bit exists"
        else:
            path += str(yb); node = node[yb]; note = "forced to the same bit"
        print("  bit %d: y has %d, want %d -> go %s (%s), xor so far %s"
              % (b, yb, want, path[-1], note, format(got >> b, "b")))
    print("  partner %s = %d, xor %d" % (path, int(path, 2), got))
    return got

g = trace([3, 10, 5, 25], 2, 5)              # 25 = 11001 is y's best partner
assert g == 2 ^ 25 == 27

random.seed(1)
for _ in range(200):
    a = [random.randrange(1 << 12) for _ in range(random.randint(1, 15))]
    b = [random.randrange(1 << 12) for _ in range(random.randint(1, 15))]
    assert max_xor(a, b) == max(x ^ y for x in a for y in b)
print("200 random pairs of arrays agree with trying every pair")
print(max_xor([3, 10, 5, 25, 2, 8], [3, 10, 5, 25, 2, 8]))
assert max_xor([3, 10, 5, 25, 2, 8], [3, 10, 5, 25, 2, 8]) == 28
```

Read the trace. The stored numbers are 3 = 00011, 10 = 01010, 5 = 00101,
25 = 11001, and y = 2 = 00010. At bit 4, y has 0, so we want a 1: only 25 starts
with 1, and we go there. That single step already guarantees an XOR of at least
16, more than any partner starting with 0 could ever give (at most 15). At bit 2,
y has 0 and we want 1, but the only number left on this path is 25, whose bit 2 is
0: forced. The walk ends at 25, and 2 XOR 25 = 27.

**The forced step is safe** because every stored number has exactly B bits, so
every node above the bottom has at least one child. Insert numbers with
different widths (say, using `bin(x)` without padding) and the alignment breaks:
the walk for 5 and for 25 would compare different bit positions.

**Bank.** [[p:inmobi-maximum-xor-between-two-arrays|Maximum XOR Between Two Arrays]]
is this exactly: insert one array, query with the other, O((n + m)·30) against the
pairwise O(n·m). [[p:tiktok-maximum-value|Maximum XOR Suffix]] is a story whose
appended values are XORs of subarrays; a subarray XOR is the XOR of two prefix
XORs, so the answer is the maximum XOR of two numbers from the list of prefix
XORs, and you insert each prefix XOR and query before inserting the next. More on
XOR identities in [[xor-tricks]].

### J. Digits and the longest common prefix

**What changes.** Characters are decimal digits. Insert every number of one array;
for each number of the other, walk as far as the trie allows. The depth reached is
the longest common prefix with *some* number of the first array.

**Why.** Two strings share a prefix of length k exactly when they reach the same
node at depth k.

**Example.** arr1 = [1, 10, 100], arr2 = [1000]: the walk of `1000` goes 1, 0, 0
and falls off at the last 0: depth 3. That is
[[p:capital-one-longest-common-prefix-of-number-pairs|Longest Common Prefix of Number Pairs]],
with 50,000 numbers per side: pairwise comparison would be 2.5 x 10^9 pairs.

### K. Path components as characters: file systems and nested keys

**What changes.** Split `/a/b/c` on `/`; each name is one "character". The node
stores the value of the path.

**Why.** "Create `/a/b/c` only if its parent exists" is "the walk of `/a/b` must
succeed, and `c` must not already be a child".

**Example.** create `/a` (ok), create `/a/b/c` (fails: `/a/b` does not exist),
create `/a/b`, get `/a/b` returns its value. See
[[p:google-design-file-system|Design File System]]. The same shape turns dotted keys
such as `a.b.c` into a nested map.

### L. Aho-Corasick: many patterns, one pass over the text

This one gets a full derivation, because it is the trie's most powerful use and
the one people know least.

**The problem.** A text, and a set of patterns. Report every occurrence of every
pattern. [[p:microsoft-streaming-stop-sequence-detection|Streaming Inference Stop Sequence Detection]]
reads a stream of model output and must stop the moment any of up to 200 stop
sequences finishes, even if the stop is split across chunks.

**The brute force with a trie.** Put the patterns in a trie. For each start
position i of the text, walk the trie from the root along `text[i], text[i+1],
...` and report every `end` flag you pass, until you fall off. That is correct.
It costs up to (longest pattern) steps per position, O(n·m) in all.

**The waste.** Patterns `he`, `she`, `his`, `hers`, text `ushers`. The walk from
position 1 reads `s`, `h`, `e` and reports `she`. Then the walk from position 2
starts over at the root and reads `h`, `e` again. We had *just read* those
letters. The walk from 1 knew that the text so far ends in `she`, and therefore
also ends in `he`. Starting over throws that knowledge away.

**The unlocking question, in this setting.** After the walk can go no further,
**what is the longest piece of what I have just read that could still be the
start of a match?** It is a suffix of the string I have read (because a match
must end where I am or later), and it must be a prefix of some pattern (or it
cannot start a match), so it is a node of the trie. Call that node the failure
link of the current node: for the node of string u, `fail(u)` is the node for the
longest proper suffix of u that is also in the trie.

For `she`, the proper suffixes are `he`, `e` and the empty string. `he` is in the
trie, so `fail(she) = he`. For `hers`, the suffixes are `ers`, `rs`, `s`: only `s`
is a node, so `fail(hers) = s`.

**The scan.** Keep one current node. For each text character: while the current
node has no child for it and is not the root, follow the failure link; then step
to the child if there is one, else stay at the root. At every node you land on,
report the patterns that end there.

**Output links.** One more subtlety. Landing on `she` means the text ends in
`she`, so it also ends in `he`, which is a pattern. The node `she` has `end` set
for `she` only. So each node's output list must include the outputs of its failure
link, and of that node's failure link, and so on. The code merges them when the
links are built.

**Building the links.** A failure link always points to a shallower node, so
compute them in breadth-first order (by depth). For a child t of node s by letter
c: start at `fail(s)` and follow failure links until you find a node with a child
c (or reach the root); that child is `fail(t)`. It is the same "fall back until
the next letter fits" rule as the scan, applied to the patterns themselves.

```python run
from collections import deque
import random

def build(patterns):
    kids, fail, out = [{}], [0], [[]]          # node 0 is the root
    for idx, p in enumerate(patterns):         # step 1: an ordinary trie
        s = 0
        for ch in p:
            if ch not in kids[s]:
                kids.append({}); fail.append(0); out.append([])
                kids[s][ch] = len(kids) - 1
            s = kids[s][ch]
        out[s].append(idx)
    q = deque(kids[0].values())                # depth 1: fail to the root
    while q:                                   # step 2: failure links, by depth
        s = q.popleft()
        for ch, t in kids[s].items():
            f = fail[s]
            while f and ch not in kids[f]:     # shorter and shorter suffixes
                f = fail[f]
            fail[t] = kids[f].get(ch, 0)
            out[t] = out[t] + out[fail[t]]     # patterns ending inside the suffix
            q.append(t)
    return kids, fail, out

def find_all(text, patterns):
    kids, fail, out = build(patterns)
    s, hits = 0, []
    for i, ch in enumerate(text):
        while s and ch not in kids[s]:         # mismatch: fall back, never re-read
            s = fail[s]
        s = kids[s].get(ch, 0)
        for idx in out[s]:
            hits.append((i - len(patterns[idx]) + 1, patterns[idx]))
    return sorted(hits)

def brute(text, patterns):
    return sorted((i, p) for p in set(patterns) for i in range(len(text))
                  if text.startswith(p, i))

pats = ["he", "she", "his", "hers"]
kids, fail, out = build(pats)
names = {0: ""}
for s in range(len(kids)):
    for ch, t in kids[s].items():
        names[t] = names[s] + ch
for s in range(1, len(kids)):
    print("node %-5s fail -> %-3r outputs %s" % (names[s], names[fail[s]], [pats[i] for i in out[s]]))
print("ushers:", find_all("ushers", pats))
assert find_all("ushers", pats) == [(1, "she"), (2, "he"), (2, "hers")]
assert names[fail[kids[kids[kids[0]["s"]]["h"]]["e"]]] == "he"

random.seed(3)
for _ in range(300):
    ps = list({"".join(random.choice("ab") for _ in range(random.randint(1, 4)))
               for _ in range(random.randint(1, 6))})
    text = "".join(random.choice("ab") for _ in range(random.randint(0, 30)))
    assert find_all(text, ps) == brute(text, ps)
print("300 random texts agree with checking every position")
```

The scan of `ushers`, step by step:

| i | char | node before | what happens | node after | report |
|---|---|---|---|---|---|
| 0 | u | root | no child u at the root | root | |
| 1 | s | root | child s | s | |
| 2 | h | s | child h | sh | |
| 3 | e | sh | child e | she | she (start 1), he (start 2) |
| 4 | r | she | no child r; fail to he; he has r | her | |
| 5 | s | her | child s | hers | hers (start 2) |

Step 4 is the one to understand. At `she` the next letter `r` has nowhere to go.
The brute force would restart at position 2 and re-read `h`, `e`. The failure link
says: "of what you have read, `he` is the longest part that could still begin a
match; you are already standing on it." From `he`, `r` fits. No text character was
read twice.

**Why it is fast.** Each text character moves the current node down by at most one
level. Each failure step moves it up by at least one level. Depth never goes below
0, so the total number of failure steps over the whole text is at most the number
of characters. The scan is O(n) plus the reports.

**It is KMP on a tree.** If there is one pattern, the trie is a single path, and
the failure link of the node at depth k is the length of the longest proper prefix
of the pattern that is also a suffix of its first k letters: KMP's failure
function, exactly.

**When to use it.** Many patterns with a large total text, or a stream where you
cannot look back. With few patterns and short texts, the trie walk from every
position, or even `str.find` per pattern, is fine and simpler.
[[p:susquehanna-company-ticker-trie|Extract Company Tickers from News]] uses a
trie of company names over *words* with longest match at each position, which is
variation E; Aho-Corasick is the tool when matches can overlap and must all be
found in one pass.

### M. Compressed tries (rare)

A chain of nodes with one child each, such as `c`-`a`-`r`-`d` in a trie holding only
`card`, can be stored as one edge labelled `card`. That is a radix tree or Patricia
trie. It saves memory when words share little, and it is how routers store IP
prefixes. Interviews almost never ask for it; mention it if memory comes up.

## Recognising it in a statement

Ordered by how reliable they are.

1. **"starts with", "prefix", "autocomplete", "type-ahead", "suggestions as the
   user types".** Nearly certain. Dozens of problems here say exactly this.
2. **Many strings stored, many queries, and queries interleaved with inserts or
   deletes.** The trie is the only one of the simple structures that does all
   three in O(L).
3. **A dictionary and a grid, or a dictionary and a backtracking search** ("find
   all words on the board", "form word squares", "split the string into
   dictionary words, all ways"). The trie is the prune.
4. **"Maximum XOR" of a pair**, or of a subarray. A bitwise trie, unless the
   problem is small enough to try every pair.
5. **A wildcard that matches one character.** Trie plus DFS.
6. **Many patterns searched in one text or stream**, "stop sequences", "banned
   words", "find all keywords". Aho-Corasick, or a trie walk from each position
   if the sizes are small.
7. **Hierarchical paths** (`/a/b/c`, `a.b.c`, domain names). A trie over
   components. For domains, the hierarchy runs right to left (`mail.google.com`
   has parent `google.com`), so split and reverse.

**The disguises.**

- "One string ends with the other" is a prefix question on reversed strings.
- "The longest common prefix of any pair across two arrays" is the depth one array
  reaches in the other's trie.
- "Pick two numbers with the most differing high bits" is maximum XOR.
- "Tokenise greedily with the longest matching token" is a trie walk from each
  position, remembering the last `end` passed.

**Anti-signals.**

- "Is this exact string present?" A set.
- "Longest common prefix of all the strings." No trie needed: compare the strings
  letter by letter, or compare only the smallest and largest after sorting.
- "Does p appear anywhere inside the text?" with one p: [[string-matching]].
- "Group words that are anagrams": a hash of sorted letters ([[anagrams]]), not a
  trie.
- The words never change and the question is only "how many start with p": a
  trie works, but sorted strings with binary search are simpler and lighter.

## Traps

**search that is really starts_with.** Symptom: proper prefixes of words are
reported as words. Only a test with a proper prefix catches it. Shown above.

**Deleting a word that is not there.** Symptom: counts that drift, an `end` of -1,
and wrong answers long after the bad delete. Check first. Shown above.

**A shared default dict.** This one is pure Python, and it is nasty because the
code looks perfect.

```python run
class BadNode:
    def __init__(self, kids={}):          # the default dict is built ONCE
        self.kids = kids
        self.end = False

class GoodNode:
    def __init__(self):
        self.kids = {}                    # a new dict for every node
        self.end = False

def build(Node, words):
    root = Node()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.kids:
                node.kids[ch] = Node()
            node = node.kids[ch]
        node.end = True
    return root

def starts_with(root, p):
    node = root
    for ch in p:
        if ch not in node.kids:
            return False
        node = node.kids[ch]
    return True

for Node in (BadNode, GoodNode):
    root = build(Node, ["ab"])
    probes = {p: starts_with(root, p) for p in ["a", "ab", "b", "ba", "aaaa"]}
    print(Node.__name__, probes)
bad, good = build(BadNode, ["ab"]), build(GoodNode, ["ab"])
assert starts_with(bad, "ba") and starts_with(bad, "aaaa")     # every node is the root
assert bad.kids["a"].kids is bad.kids                            # one shared dict
assert not starts_with(good, "ba") and starts_with(good, "ab")

# Word Search II: a found word must be removed, or a second path reports it again
def find_words(board, words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w
    R, C, found = len(board), len(board[0]), []
    def dfs(r, c, parent, remove):
        ch = board[r][c]
        node = parent.get(ch)
        if node is None:
            return
        if "$" in node:
            found.append(node["$"])
            if remove:
                del node["$"]                 # report each word once
        board[r][c] = "#"                     # mark: this path owns the cell
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                dfs(nr, nc, node, remove)
        board[r][c] = ch                      # unmark: other paths may use it
    for remove in (False, True):
        found.clear()
        for r in range(R):
            for c in range(C):
                dfs(r, c, root, remove)
        print("remove found words =", remove, "->", found)
    return found

board = [list("aa"), list("aa")]
assert find_words(board, ["aa"]) == ["aa"]
assert board == [list("aa"), list("aa")]       # every mark was undone
```

`def __init__(self, kids={})` creates the default dict once, when the class is
defined, and every node built without an argument shares it. So the "child" of the
root has the root's own dict as its children: the trie is one node with a loop on
it, and every string made of stored letters is a "prefix", including `ba` and
`aaaa`. Symptom: `starts_with` is true for nonsense. Never use a mutable default
argument; create the dict inside `__init__`.

**Word Search II reporting a word twice.** In the second half of that block, a
2 x 2 board of `a`s and the word `aa`: there are eight grid paths spelling `aa`
(each of four cells, times two neighbours). Without removing the found word, all
eight are reported. Symptom: duplicates in the output, or a timeout on boards full
of one letter. Remove the end marker when you report it; better still, also delete
trie nodes that have become empty so later searches stop earlier.

**Stopping a longest match at the first end flag.** Tokens `a` and `ab`, text
`ab`: the walk passes `a` (flag) and then `ab` (flag). Stopping at the first gives
`a` then an unknown `b`. Walk on and remember the last flag.

**Variable-width bitwise trie.** Inserting numbers by `bin(x)[2:]` puts 5 (`101`)
and 25 (`11001`) at different depths for the same bit. Symptom: wrong maximum XOR
on inputs with mixed magnitudes. Always walk a fixed B bits from the top.

**Forgetting Aho-Corasick output links.** Without `out[t] += out[fail[t]]`, the
scan of `ushers` reports `she` and `hers` and misses `he`, because `he` ends inside
`she`. Symptom: patterns that are suffixes of other patterns are never found.

**Not normalising.** "Case-insensitive" problems must lowercase before insert *and*
before every query. Symptom: `Car` is not found after inserting `car`.

**Deep recursion.** A recursive DFS over a trie recurses once per letter of depth.
With words of length 1,000 that is fine; with a single word of 100,000 letters it
exceeds Python's default limit of about 1,000 frames. Make insert and walk
iterative (as above, they naturally are), and use an explicit stack for any
subtree DFS on deep tries.

## What to memorise

The template:

```python
class Node:
    __slots__ = ("kids", "end", "through")
    def __init__(self):
        self.kids, self.end, self.through = {}, 0, 0

def insert(root, w):
    node = root; node.through += 1
    for ch in w:
        node = node.kids.setdefault(ch, Node())   # create on the way down
        node.through += 1
    node.end += 1

def walk(root, s):                                # node for s, or None
    node = root
    for ch in s:
        node = node.kids.get(ch)
        if node is None:
            return None
    return node
# search: node and node.end > 0      starts_with: node and node.through > 0
```

The sentence that turns a problem into it: **everything that starts with p lives
under one node, so keep what you need to know about those strings at that node.**

The question that finds the design: **what do all the strings that begin with p
have in common, and can I store that once?**

The habit: test every trie with a proper prefix of a stored word (search must say
no, starts_with must say yes) and with a delete of an absent word (nothing may
change).

The numbers: operations cost O(length), never O(number of words); nodes are at
most the total letters plus one; values up to 10^9 need 30 bits; Aho-Corasick scans
in O(text + matches).

## Check yourself

:::check
Hand trace. Insert `tea`, `ten`, `to`, `inn`, `in`, `tea` (yes, twice) into an
empty trie. Number the nodes in order of creation, root 0. Then give `end` and
`through` for every node, and answer: search `te`, starts_with `te`,
count_prefix `te`, count_prefix `""`, search `inn`.
--
Creation: tea makes 1 (t), 2 (te), 3 (tea). ten makes 4 (ten). to makes 5 (to).
inn makes 6 (i), 7 (in), 8 (inn). in makes nothing: the path exists, only `end`
at node 7 changes. The second tea makes nothing either.

| node | prefix | end | through |
|---|---|---|---|
| 0 | (root) | 0 | 6 |
| 1 | t | 0 | 4 (tea, ten, to, tea) |
| 2 | te | 0 | 3 |
| 3 | tea | 2 | 2 |
| 4 | ten | 1 | 1 |
| 5 | to | 1 | 1 |
| 6 | i | 0 | 2 |
| 7 | in | 1 | 2 (in, inn) |
| 8 | inn | 1 | 1 |

search `te`: node 2 exists, `end` = 0: false. starts_with `te`: true.
count_prefix `te`: 3 (tea twice and ten). count_prefix `""`: 6. search `inn`: true.
:::

:::check
Hand trace. Patterns `a`, `ab`, `bab`, `bc`, `bca`, `c`, `caa`. Build the trie,
then give the failure link and the output list of every node. Then scan the text
`abccab` and list each match with its start position.
--
Nodes (named by their string): a, ab, b, ba, bab, bc, bca, c, ca, caa.

| node | fail | why | outputs |
|---|---|---|---|
| a | root | depth 1 | a |
| b | root | depth 1 | |
| c | root | depth 1 | c |
| ab | b | suffix `b` is a node | ab |
| ba | a | suffix `a` | a |
| bc | c | suffix `c` | bc, c |
| ca | a | suffix `a` | a |
| bab | ab | suffix `ab` is a node | bab, ab |
| bca | ca | suffix `ca` is a node | bca, a |
| caa | a | suffixes `aa` (no), `a` (yes) | caa, a |

Scan `abccab`: i=0 `a`: root to a, report a@0. i=1 `b`: a to ab, report ab@0.
i=2 `c`: ab has no c; fail to b; b has c: bc, report bc@1, c@2. i=3 `c`: bc has
no c; fail to c; c has no c; fail to root; root has c: c, report c@3. i=4 `a`: c to
ca, report a@4. i=5 `b`: ca has no b; fail to a; a has b: ab, report ab@4.

Matches: a@0, ab@0, bc@1, c@2, c@3, a@4, ab@4. Check by hand against the text:
`abccab` contains `a` at 0 and 4, `ab` at 0 and 4, `bc` at 1, `c` at 2 and 3, and
no `bab`, `bca` or `caa`.
:::

:::check
Why must the bitwise trie for maximum XOR be built from the most significant bit
down, and what goes wrong if you build it from the least significant bit up?
--
The walk makes a greedy choice at every level: take the opposite bit if
possible. That is only safe if each decision dominates all later ones. From the
top, it does: getting bit b of the XOR to 1 is worth 2^b, more than all lower bits
together, 2^b - 1. So whatever happens below, a partner that wins the current bit
beats any partner that loses it.

From the bottom up, the first decision is about bit 0, worth 1. Winning it can
commit you to a branch whose numbers all lose the top bit. Example: stored 1 (01)
and 2 (10), query 0 (00). From the bottom: bit 0, want 1, go to 1's branch, and
the XOR is 1. From the top: bit 1, want 1, go to 2's branch, and the XOR is 2, which
is correct.
:::

:::check
Someone says: "A trie is pointless. A Python set of all prefixes gives
starts_with in O(1), which beats the trie's O(L)." Where are they wrong?
--
First, the set lookup is not O(1) in the length: hashing the query reads all |p|
characters, so both are O(|p|) per query. The trie is not slower.

Second, the set of all prefixes costs L(L+1)/2 characters per word of length L,
which for words of length 1,000 is about 500 times the input; inserts cost the
same. The trie costs at most L nodes per word, and shares them.

Third, the set loses structure. It can say whether p is a prefix, and with a
dict, how many words start with p, but not which ones: autocomplete, wildcards
(`.ad`), Word Search II pruning and maximum XOR all need to walk to the children
of a prefix, which a set of strings does not have.
:::

:::check
Someone implements autocomplete by walking to the node for the typed text and
returning a DFS of the whole subtree, sorted, cut to three. It passes the sample
and times out. What is the cost, and what are the two standard fixes?
--
Each query costs the size of the subtree below the typed prefix. After typing one
letter, that can be a large fraction of the whole catalogue, and the DFS then
sorts it, so a query can cost O(N log N) for N products. With 100,000 keystrokes
that is far too slow.

Fix 1: visit children in sorted letter order (and report a node's own word before
its children); the DFS then produces words in alphabetical order and can stop
after the third. It costs about the length of the three words plus the path.
Fix 2: store the best three words at every node during insert (each insert updates
the lists along its path); a query is then the walk plus reading one list. When
ranking is by frequency and frequencies change, fix 2 must update the lists on the
path of the changed sentence.

Also keep the current node between keystrokes, so typing one more letter is one
step, not a fresh walk from the root.
:::

:::check
Reduce this disguised problem. "Given an array of up to 10^5 integers below 2^30,
find the maximum XOR of any contiguous subarray." Name the steps and the trie.
--
Let P[0] = 0 and P[k] = a[0] XOR ... XOR a[k-1]. The XOR of a[i..j] is
P[j+1] XOR P[i], because the common part a[0..i-1] cancels. So the question is:
the maximum XOR of two numbers from the list P[0..n].

Insert P[0] into a 30-bit bitwise trie. For k = 1..n, query the trie with P[k]
(walk toward the opposite bit at each level, top first) to get the best partner
among earlier prefixes, update the answer, then insert P[k]. O(30 n) time against
O(n^2) pairwise. This is the shape behind
[[p:tiktok-maximum-value|Maximum XOR Suffix]].
:::

:::check
Hand trace. Stored words `bad`, `bat`, `cat`. Run the wildcard search for `.a.`
and for `b.d.`, listing every (node, position) the DFS visits.
--
`.a.`: at the root, position 0 is `.`, so try children b and c. Under b, position
1 is `a`: child a exists. Position 2 is `.`: try children d and t. At d, position 3
= end of pattern, and `bad` ends here: true. The search can stop (an `any` stops at
the first true). Visited: root, b, ba, bad.

`b.d.`: root, child b; position 1 `.`: try ba (the only child). Position 2 `d`: ba
has child d, go to bad. Position 3 `.`: bad has no children, so `any` of nothing is
false. Back up: no other child of b to try at position 1. Answer false. Visited:
root, b, ba, bad. The length rule is enforced for free: the pattern is four
characters, and no stored path is four deep.
:::
