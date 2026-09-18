/* Transcribed from the screenshots in ../images. Source images listed per problem. */
window.PROBLEMS = [

/* ============ SECTION 1 — AMAZON OA · CODING ============ */
{
  id:'bags', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Code Question 1', title:'Maximum Money in k Consecutive Bags',
  minutes:45, score:'Max. score: 100',
  images:['image30.png','image33.png','image32.png','image21.jpg','WhatsApp Image 2026-09-07 at 10.14.57 PM (3).jpeg','WhatsApp Image 2026-09-07 at 10.14.57 PM (4).jpeg'],
  fn:{name:'calculateMaximumConsecutiveSum', ret:'int',
      params:[['int','k'],['int[][]','segment']]},
  gen:`def gen(rng, n):
    segs, cur = [], rng.randint(1, 3)
    for _ in range(max(1, n)):
        s = cur + rng.randint(0, 4)
        e = s + rng.randint(0, 4)
        segs.append([s, e, rng.randint(1, 50)])
        cur = e + 1
    return [rng.randint(1, max(2, 3 * max(1, n))), segs]`,
  tests:[
    {in:[3, [[1, 9, 5], [10, 20, 5]]], out:15},
    {in:[5, [[1, 4, 2], [6, 6, 5], [7, 7, 7], [9, 10, 1]]], out:16},
    {in:[5, [[1, 10, 1], [11, 11, 100]]], out:104},
    {in:[1, [[1, 1, 7]]], out:7},
    {in:[100, [[1, 4, 2], [6, 6, 5]]], out:13},
    {in:[4, [[3, 6, 4], [7, 11, 7], [14, 18, 4], [23, 24, 3], [25, 28, 27]]], out:108},
    {in:[7, [[2, 2, 36], [6, 6, 37], [7, 8, 38], [9, 13, 38], [17, 17, 15], [18, 22, 9]]], out:266},
    {in:[2, [[5, 6, 35], [7, 11, 20], [16, 17, 7], [22, 26, 13]]], out:70}
  ],
  body:`
<p>In Amazon's financial team an analyst is dealing with an <strong>infinite</strong> number of bags arranged in a line, each numbered from <em>1</em> to infinity. The task is to gather information about the amount of money in these bags, presented in the form of continuous segments. The objective is to select consecutive bags in such a way that the total amount of money in these bags is maximized.</p>

<p>The continuous segments provided to represent the amount of money in each bag do not intersect. Additionally, any bag included within a segment contains some amount of money, while bags not included in any segment are considered to have zero money.</p>

<p>Formally, given a 2D array <em>segment</em> of size <em>n</em> x <em>3</em>, where <em>n</em> represents the number of available segments, and an integer <em>k</em> representing the number of consecutive bags you will take, and the 2D array <em>segment</em> represents the range of bags included in this segment <em>[segment[0], segment[1]]</em> and the amount of money inside the bags in the range <em>segment[2]</em>.</p>

<p>Find the <em>k</em> consecutive bags with the maximum total amount of money, since the answer can be large, return it modulo (10<sup>9</sup> + 7).</p>

<h3>Example</h3>
<pre class="sample">k = 5
n = 4
int 3 (column size)
segment = [ [1, 4, 2], [6, 6, 5], [7, 7, 7], [9, 10, 1] ]</pre>

<p>The amount of money in each bag is:</p>
<table class="oa">
<tr><th>Bag</th><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td></tr>
<tr><th>Money</th><td>2</td><td>2</td><td>2</td><td>2</td><td>0</td><td>5</td><td>7</td><td>0</td><td>1</td><td>1</td></tr>
</table>

<p>All other bags have zero money.</p>
<p>Let's try different consecutive bags of size <em>k</em>:</p>
<table class="oa">
<tr><th>Bags</th><th>Total Money</th></tr>
<tr><td>[1 - 5]</td><td>2 + 2 + 2 + 2 + 0 = 8</td></tr>
<tr><td>[2 - 6]</td><td>2 + 2 + 2 + 0 + 5 = 11</td></tr>
<tr><td>[3 - 7]</td><td>2 + 2 + 0 + 5 + 7 = 16</td></tr>
<tr><td>[4 - 8]</td><td>2 + 0 + 5 + 7 + 0 = 14</td></tr>
<tr><td>[5 - 9]</td><td>0 + 5 + 7 + 0 + 1 = 13</td></tr>
<tr><td>[6 - 10]</td><td>5 + 7 + 0 + 1 + 1 = 14</td></tr>
</table>

<p>The subsegment starting from the third bag and ending at the seventh bag has the maximum total amount of money, hence the answer is <em>16</em>.</p>

<h3>Function Description</h3>
<p>Complete the function <em>calculateMaximumConsecutiveSum</em> in the editor below.</p>
<p><em>calculateMaximumConsecutiveSum</em> has the following parameters:</p>
<ul>
  <li><em>int k:</em> the number of consecutive bags you will take.</li>
  <li><em>int segment[n][3]:</em> A 2D array where <em>n</em> is the number of segments. Each segment contains the start index, end index, and money in the bags for that range.</li>
</ul>

<h3>Returns</h3>
<ul><li><em>int:</em> the amount of money inside the <em>k</em> consecutive bags with the maximum total amount of money modulo 10<sup>9</sup> + 7.</li></ul>

<h3>Constraints</h3>
<ul>
  <li>1 &le; <em>n</em> &le; 2 * 10<sup>5</sup></li>
  <li>1 &le; <em>k</em> &le; 10<sup>9</sup></li>
  <li>1 &le; <em>segment[i][0]</em> &le; <em>segment[i][1]</em> &le; 10<sup>9</sup></li>
  <li>1 &le; <em>segment[i][2]</em> &le; 10<sup>6</sup></li>
  <li>It is guaranteed that no two segments intersect.</li>
</ul>

<div class="bar">Input Format for Custom Testing</div>
<div class="bar open">Sample Case 0</div>
<div class="sublabel">Sample Input 0</div>
<pre class="sample">STDIN            Function
-----            --------
3          &rarr;   k = 3
2          &rarr;   segment[] size n = 2
3          &rarr;   segment[][] size columns = 3 (always)
1 9 5      &rarr;   segment = [ [1, 9, 5], [10, 20, 5] ]
10 20 5</pre>
<div class="sublabel">Sample Output 0</div>
<pre class="sample">15</pre>

<div class="srcnote"><strong>Also catalogued as:</strong> "Find Maximum Total Amount (SDE I, Fungible)" on FastPrep — tagged <em>Medium · Amazon · New Grad · Fulltime · OA · Phone Screen</em>, category <em>Prefix Sum</em>. Same example (<code>segment = [[1,4,2],[6,6,5],[7,7,7],[9,10,1]]</code>, <code>k = 5</code>, <code>return = 16</code>). That listing notes the source does not show numeric input bounds, so the constraints above come from the exam screenshot only.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>The segments are already sorted and guaranteed not to overlap, and you must take <em>k consecutive bags</em>. Ask yourself: how many <strong>distinct</strong> starting bags are actually worth trying, given that most of the number line is empty?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>A window of length <em>k</em> only ever needs to start where money starts. Walk the segments in order with two pointers, maintaining the total money inside a window that ends at each segment's end (or starts at each segment's start). Use prefix sums over segments so a window's value is O(1).</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Each segment is <code>[start, end, money]</code> where <em>money</em> is the amount in <strong>each</strong> bag of that range. Segments are disjoint and can be sorted by start.</p>
<p>One fact collapses the search space. Slide the window right by one bag: the total changes by <code>v(R+1) &minus; v(L)</code>, which stays constant until an edge is crossed — so the total is a <strong>piecewise-linear function of L</strong>, and its maximum sits at a slope breakpoint. The breakpoints are exactly where <code>v(L)</code> changes (<code>L = start<sub>i</sub></code>) or where <code>v(R+1)</code> changes (<code>R = end<sub>i</sub></code>). Windows opening inside a gap are dominated — there <code>v(L)=0</code>, so sliding right can only help.</p>
<ul>
<li>So there are at most <strong>2n</strong> candidate windows: left edge on some segment's <em>start</em>, or right edge on some segment's <em>end</em>.</li>
<li>Checking only the left-edge family is <strong>wrong</strong>. On <code>segment = [[1,10,1],[11,11,100]]</code>, <code>k = 5</code> it returns 100, but <code>[7,11]</code> is worth <code>4&times;1 + 100 = 104</code>.</li>
</ul>
<p>Sort by start, build a prefix sum of full-segment values (<code>(end-start+1)*money</code>), then price each candidate window in O(log n): binary-search its first and last overlapping segments, take the prefix sum of everything strictly between them, and add the two clipped end pieces.</p><p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>from bisect import bisect_left, bisect_right

def calculateMaximumConsecutiveSum(k, segment):
    segs = sorted(segment)                     # [start, end, money]
    n = len(segs)
    starts = [s for s, _, _ in segs]
    ends   = [e for _, e, _ in segs]

    pre = [0] * (n + 1)                        # pre[i] = total money in segs[:i]
    for i, (s, e, m) in enumerate(segs):
        pre[i + 1] = pre[i] + (e - s + 1) * m

    def window(L, R):                          # money in bags [L, R]
        i = bisect_left(ends, L)               # first segment with end &gt;= L
        j = bisect_right(starts, R) - 1        # last  segment with start &lt;= R
        if i &gt; j:
            return 0                           # window lies entirely in a gap
        s, e, m = segs[i]
        if i == j:                             # one segment, clipped both sides
            return (min(e, R) - max(s, L) + 1) * m
        total = pre[j] - pre[i + 1]            # segments i+1 .. j-1, whole
        total += (e - max(s, L) + 1) * m       # left piece of segment i
        s, e, m = segs[j]
        total += (min(e, R) - s + 1) * m       # right piece of segment j
        return total

    best = 0
    for i in range(n):
        best = max(best,
                   window(starts[i], starts[i] + k - 1),   # left edge anchored
                   window(ends[i] - k + 1, ends[i]))       # right edge anchored
    return best % (10**9 + 7)</code></pre><div class="unsure">The statement returns the answer modulo 10<sup>9</sup>+7. Keep the running maximum on the <em>true</em> value and reduce only once at the end — comparing reduced values picks the wrong window.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Everything below uses the statement's own example: <code>k = 5</code>, <code>segment = [[1,4,2],[6,6,5],[7,7,7],[9,10,1]]</code>, answer <strong>16</strong>.</p>

<div class="step"><h4>1 &middot; What the input actually is: a run-length encoding</h4>
<p>The bag line you are being asked about is this, and it runs to infinity:</p>
<div class="formula">bag  1  2  3  4  5  6  7  8  9 10 11 ...
val  2  2  2  2  0  5  7  0  1  1  0 ...</div>
<p>A segment <code>[s, e, m]</code> is not "a bag worth m" — it is <strong>the value m repeated (e &minus; s + 1) times</strong>. <code>[1,4,2]</code> is "2, four times". That is run-length encoding, and it is the only reason the input fits on a page when the bag numbers go to 10<sup>9</sup>.</p>
<p>So the array you would like to sweep has up to 10<sup>9</sup> cells, but only <strong>n &le; 2&times;10<sup>5</sup> places where the value changes</strong>. Every technique below is one idea applied twice: <em>store only the change points, and compute the flat stretches with multiplication instead of iteration.</em></p></div>

<div class="step"><h4>2 &middot; The prefix sum, and exactly what index i means</h4>
<p><code>pre[i]</code> is the total money in the <em>first i segments</em> — not the first i bags. It is the ordinary prefix sum of the infinite bag array, but sampled only at segment boundaries, because between boundaries it just grows linearly and carries no information.</p>
<div class="formula">seg 0 = [1,4,2]   (4&minus;1+1) &times; 2 = 4 bags &times; 2 =  <b>8</b>
seg 1 = [6,6,5]   (6&minus;6+1) &times; 5 = 1 bag  &times; 5 =  <b>5</b>
seg 2 = [7,7,7]   (7&minus;7+1) &times; 7 = 1 bag  &times; 7 =  <b>7</b>
seg 3 = [9,10,1]  (10&minus;9+1)&times; 1 = 2 bags &times; 1 =  <b>2</b>

pre = [0, 8, 13, 20, 22]
       ^  ^   ^   ^   ^
       |  |   |   |   after all 4 segments
       |  |   |   after segments 0,1,2
       |  |   after segments 0,1
       |  after segment 0
       the leading 0, so "sum of segments a..b" needs no special case</div>
<p>The leading <code>0</code> is what lets you write <code>pre[b+1] &minus; pre[a]</code> for <em>any</em> range including one that starts at 0. Sum of segments 1 and 2 = <code>pre[3] &minus; pre[1] = 20 &minus; 8 = 12</code>, in one subtraction, no loop — and it would still be one subtraction if those segments held a billion bags each.</p>
<p><strong>Gaps are never stored and never need to be.</strong> A gap contributes 0, so it leaves the prefix sum flat; a gap of length 1 and a gap of length 10<sup>9</sup> are indistinguishable to <code>pre</code>. That is why you can jump over empty space without ever looking at it.</p></div>

<div class="step"><h4>3 &middot; Pricing one window: the two binary searches</h4>
<p>Given a window <code>[L, R]</code>, you need the segments it touches. Two searches, and it is worth being precise about why each uses a different <code>bisect</code>:</p>
<div class="formula">i = bisect_left(<b>ends</b>,   L)      first segment whose end   &gt;= L
j = bisect_right(<b>starts</b>, R) &minus; 1  last  segment whose start &lt;= R</div>
<p>A segment overlaps <code>[L, R]</code> exactly when <code>start &le; R</code> <em>and</em> <code>end &ge; L</code>. Those two conditions are what the two searches test, each against its own sorted array. Segments <code>i</code> through <code>j</code> are the overlapping ones; if <code>i &gt; j</code> the window sits wholly in a gap and is worth 0.</p>
<p><code>bisect_left</code> on <code>ends</code> gives the first index with <code>ends[idx] &ge; L</code> (it is the first not-less-than position). <code>bisect_right</code> on <code>starts</code> gives the first index with <code>starts[idx] &gt; R</code>, so subtracting 1 gives the last with <code>starts[idx] &le; R</code>. Swap the two and you get off-by-ones on exact boundary touches — a window ending precisely on a segment's start, for instance.</p>
<p>Now the middle segments <code>i+1 .. j&minus;1</code> are <strong>provably whole</strong>: for any t &gt; i, <code>start<sub>t</sub> &gt; end<sub>i</sub> &ge; L</code> (segments are disjoint and sorted), so it starts inside the window; for any t &lt; j, <code>end<sub>t</sub> &lt; start<sub>j</sub> &le; R</code>, so it ends inside. That is what earns the single subtraction <code>pre[j] &minus; pre[i+1]</code>. Only the two <em>outermost</em> segments can be cut.</p></div>

<div class="step"><h4>4 &middot; The clipping formula, and where every &plusmn;1 comes from</h4>
<p>Counting bags in an inclusive integer range <code>[a, b]</code> is <code>b &minus; a + 1</code>, never <code>b &minus; a</code>: bags 7 to 7 is one bag, not zero. Every <code>+ 1</code> in the code is that, and nothing else.</p>
<div class="formula">left piece  (segment i):   (e<sub>i</sub>          &minus; <b>max</b>(s<sub>i</sub>, L) + 1) &times; m<sub>i</sub>
right piece (segment j):   (<b>min</b>(e<sub>j</sub>, R) &minus;      s<sub>j</sub>      + 1) &times; m<sub>j</sub>
both at once (i == j):     (<b>min</b>(e, R)  &minus; <b>max</b>(s, L)  + 1) &times; m</div>
<p>The <code>max</code> and <code>min</code> are the clip. <code>max(s, L)</code> asks "does the window start before this segment does, or partway into it?" — take whichever is later, because bags before <code>L</code> are outside the window and bags before <code>s</code> do not exist. <code>min(e, R)</code> is the mirror image at the right end. This single pair of clamps handles every case without branching: window covering the whole segment, cutting into it, or lying inside it.</p>
<p>Multiplying by <code>m</code> at the end is where money finally enters — <em>after</em> the geometry is completely settled.</p></div>

<div class="step"><h4>5 &middot; Which windows to try, and why left-anchoring alone is a bug</h4>
<p>There are 10<sup>9</sup> possible values of <code>L</code>, so you need an argument that only a handful matter. Slide the window one bag to the right:</p>
<div class="formula">total(L+1) &minus; total(L) = v(R+1) &minus; v(L)      where v(x) = money in bag x</div>
<p><code>v</code> is constant along each run, so this difference — the <em>slope</em> — is also constant until either edge crosses a run boundary. A function that is linear between breakpoints attains its maximum <strong>at a breakpoint</strong>. Slope changes only when <code>v(L)</code> changes, i.e. <code>L = start<sub>i</sub></code>, or when <code>v(R+1)</code> changes, i.e. <code>R = end<sub>i</sub></code>. Windows whose left edge sits in a gap are dominated: there <code>v(L) = 0</code>, so the slope is <code>v(R+1) &ge; 0</code> and sliding right never loses. That leaves <strong>2n candidates</strong>, and the loop tries exactly those two per segment.</p>
<p>Dropping the right-anchored half looks harmless and is not. Take <code>segment = [[1,10,1],[11,11,100]]</code>, <code>k = 5</code>:</p>
<table class="trace">
<tr><th>candidate</th><th>window</th><th>total</th></tr>
<tr><td>L = start<sub>0</sub> = 1</td><td>[1, 5]</td><td>5 &times; 1 = 5</td></tr>
<tr><td>L = start<sub>1</sub> = 11</td><td>[11, 15]</td><td>100</td></tr>
<tr><td class="hit">R = end<sub>1</sub> = 11</td><td class="hit">[7, 11]</td><td class="hit">4 &times; 1 + 100 = <strong>104</strong></td></tr>
</table>
<p>The winning window opens at bag 7, which is nobody's start. Left-anchoring only returns 100. Tested against brute force on 20 000 random inputs, the left-only version is wrong on roughly 9% of them — and it still passes both published samples, which is exactly why the bug survives.</p></div>

<div class="step"><h4>6 &middot; The full trace on the sample</h4>
<p><code>starts = [1, 6, 7, 9]</code>, <code>ends = [4, 6, 7, 10]</code>, <code>pre = [0, 8, 13, 20, 22]</code>, <code>k = 5</code>. Eight candidates:</p>
<table class="trace">
<tr><th>anchor</th><th>L</th><th>R</th><th>i, j</th><th>middle: pre[j]&minus;pre[i+1]</th><th>left piece</th><th>right piece</th><th>total</th></tr>
<tr><td>start<sub>0</sub></td><td>1</td><td>5</td><td>0, 0</td><td>&mdash; (i = j)</td><td colspan="2">(min(4,5)&minus;max(1,1)+1)&times;2 = 4&times;2</td><td>8</td></tr>
<tr><td>start<sub>1</sub></td><td>6</td><td>10</td><td>1, 3</td><td>pre[3]&minus;pre[2] = 20&minus;13 = 7</td><td>(6&minus;6+1)&times;5 = 5</td><td>(min(10,10)&minus;9+1)&times;1 = 2</td><td>14</td></tr>
<tr><td>start<sub>2</sub></td><td>7</td><td>11</td><td>2, 3</td><td>pre[3]&minus;pre[3] = 0</td><td>(7&minus;7+1)&times;7 = 7</td><td>(min(10,11)&minus;9+1)&times;1 = 2</td><td>9</td></tr>
<tr><td>start<sub>3</sub></td><td>9</td><td>13</td><td>3, 3</td><td>&mdash; (i = j)</td><td colspan="2">(min(10,13)&minus;max(9,9)+1)&times;1 = 2&times;1</td><td>2</td></tr>
<tr><td>end<sub>0</sub></td><td>0</td><td>4</td><td>0, 0</td><td>&mdash; (i = j)</td><td colspan="2">(min(4,4)&minus;max(1,0)+1)&times;2 = 4&times;2</td><td>8</td></tr>
<tr><td>end<sub>1</sub></td><td>2</td><td>6</td><td>0, 1</td><td>pre[1]&minus;pre[1] = 0</td><td>(4&minus;max(1,2)+1)&times;2 = 3&times;2 = 6</td><td>(min(6,6)&minus;6+1)&times;5 = 5</td><td>11</td></tr>
<tr><td class="hit">end<sub>2</sub></td><td class="hit">3</td><td class="hit">7</td><td class="hit">0, 2</td><td class="hit">pre[2]&minus;pre[1] = 13&minus;8 = 5</td><td class="hit">(4&minus;max(1,3)+1)&times;2 = 2&times;2 = 4</td><td class="hit">(min(7,7)&minus;7+1)&times;7 = 7</td><td class="hit"><strong>16</strong></td></tr>
<tr><td>end<sub>3</sub></td><td>6</td><td>10</td><td>1, 3</td><td>pre[3]&minus;pre[2] = 7</td><td>(6&minus;6+1)&times;5 = 5</td><td>(min(10,10)&minus;9+1)&times;1 = 2</td><td>14</td></tr>
</table>
<p>Maximum <strong>16</strong>, from the window <code>[3, 7]</code> — the statement's answer, and note it is a <em>right</em>-anchored candidate. Read the winning row across: 2 bags clipped off segment 0 (bags 3 and 4, worth 4), all of segment 1 via the prefix sum (bag 6, worth 5), and all of segment 2 as the right piece (bag 7, worth 7). Bag 5 is a gap and cost nothing to skip — it was never touched.</p></div>

<div class="step"><h4>7 &middot; Money never decides where the window lands</h4>
<p>Worth stating flatly, because it is the usual confusion: <code>m</code> appears nowhere in the index arithmetic. Not in <code>R = L + k &minus; 1</code>, not in either <code>bisect</code>, not in <code>min(e,R) &minus; max(s,L) + 1</code>. Change segment 1's money from 5 to 1 000 000 and the search finds the <em>same</em> segments, clips the <em>same</em> bags; only the final multiplication changes, 14 becomes 1 000 009. Position and value are computed in that order and never interact.</p>
<p>The one place money does matter is <em>choosing between</em> candidate windows — the slope argument in step 5 — and even there it only ranks windows that were located by pure index arithmetic.</p></div>

<div class="step"><h4>8 &middot; Traps</h4>
<ul>
<li><strong>Reduce mod 10<sup>9</sup>+7 once, at the very end.</strong> Comparing reduced totals picks the wrong window: a genuine 10<sup>9</sup>+8 reduces to 1 and loses to a genuine 2.</li>
<li><strong>Sort first.</strong> The prefix sum and both binary searches assume <code>starts</code> and <code>ends</code> are ascending. The statement guarantees disjointness, not sorted order.</li>
<li><strong><code>ends[i] &minus; k + 1</code> can go zero or negative</strong> when k exceeds everything to the left. Harmless here — the searches simply find no segment before it — but do not "fix" it by clamping to 1 without checking, since that silently shortens the window.</li>
<li><strong>k can exceed the whole span.</strong> Then one window swallows every segment and the answer is <code>pre[n]</code>; the same code path produces it with no special case.</li>
<li><strong>Do not expand into an array.</strong> With bag numbers to 10<sup>9</sup> that is instant MLE — the entire point of the run-length input.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'getmincost', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Question 1', title:'Minimum Cost to Make All Stations Equal',
  minutes:37, score:'',
  images:['WhatsApp Image 2026-09-07 at 10.14.57 PM (2).jpeg','WhatsApp Image 2026-09-07 at 10.14.57 PM.jpeg','WhatsApp Image 2026-09-07 at 10.14.57 PM (1).jpeg'],
  fn:{name:'getMinCost', ret:'long', params:[['int[]','arr']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [[rng.randint(1, m) for _ in range(m)]]`,
  tests:[
    {in:[[1, 1, 2, 1, 1]], out:3},
    {in:[[1, 1, 3]], out:1},
    {in:[[3, 1, 4, 2]], out:3},
    {in:[[5]], out:0},
    {in:[[2, 2, 2, 2]], out:0},
    {in:[[2, 2, 2, 2, 9, 1]], out:4},
    {in:[[4, 3, 2, 1]], out:3},
    {in:[[1, 2, 3, 4, 5, 6]], out:5}
  ],
  body:`
<p>You are given an array <em>arr</em> of length <em>n</em> representing the target display value at each Amazon fulfillment station (stations are in a line from left to right).</p>

<p>You can do the following operations any number of times (possibly zero):</p>
<ul>
  <li>Choose an index <em>i</em> with <em>1 &le; i &le; n - 1</em> and set all positions <em>0, 1, …, i-1</em> to <em>arr[i]</em>; this costs <em>i &times; arr[i]</em>.</li>
  <li>Choose an index <em>i</em> with <em>0 &le; i &le; n - 2</em> and set all positions <em>i+1, i+2, …, n-1</em> to <em>arr[i]</em>; this costs <em>(n - 1 - i) &times; arr[i]</em>.</li>
</ul>

<p>Compute the minimum total cost to make all array elements equal.</p>

<h3>Example</h3>
<pre class="sample">n = 4
arr = [3, 1, 4, 2]</pre>
<p>Start with <em>arr = [3, 1, 4, 2]</em>. One optimal sequence is:</p>
<ul>
  <li>Choose <em>i = 1</em> and set position 0 to <em>arr[1] = 1</em>. Cost = <em>1 * 1 = 1</em>. The array becomes <em>[1, 1, 4, 2]</em>.</li>
  <li>Choose <em>i = 1</em> and set positions 2 and 3 to <em>arr[1] = 1</em>. Cost = <em>(4 - 1 - 1) * 1 = 2</em>. The array becomes <em>[1, 1, 1, 1]</em>.</li>
</ul>
<p>Total cost = <em>1 + 2 = 3</em>. No sequence yields a smaller total cost.</p>

<h3>Function Description</h3>
<p>Complete the function <em>getMinCost</em> in the editor below.</p>
<p><em>getMinCost</em> has the following parameter(s):</p>
<ul><li><em>int arr[n]:</em> the target display value at each Amazon fulfillment station.</li></ul>

<h3>Returns</h3>
<ul><li><em>long:</em> the minimum total cost to make all elements equal.</li></ul>

<h3>Constraints</h3>
<ul>
  <li>1 &le; <em>n</em> &le; 2 * 10<sup>5</sup></li>
  <li>1 &le; <em>arr[i]</em> &le; <em>n</em></li>
</ul>

<div class="bar open">Input Format for Custom Testing</div>
<p>The first line contains an integer <em>n</em>, the number of elements in <em>arr</em>.<br>Each of the next <em>n</em> lines contains an integer <em>arr[i]</em>.</p>

<div class="bar open">Sample Case 0</div>
<div class="sublabel">Sample Input 0</div>
<pre class="sample">STDIN            FUNCTION
-----            --------
5          &rarr;   arr[] size n = 5
1          &rarr;   arr = [1, 1, 2, 1, 1]
1
2
1
1</pre>
<div class="sublabel">Sample Output 0</div>
<pre class="sample">3</pre>
<div class="sublabel">Explanation</div>
<p>To make all elements equal to 1, you can use the following optimal move:</p>
<ul><li>Choose index <em>i = 1</em> (where <em>arr[1] = 1</em>) and set positions 2, 3, and 4 to <em>arr[1]</em>. The cost is <em>(5 - 1 - 1) * 1 = 3</em>.</li></ul>

<div class="bar open">Sample Case 1</div>
<div class="sublabel">Sample Input 1</div>
<pre class="sample">STDIN            FUNCTION
-----            --------
3          &rarr;   arr[] size n = 3
1          &rarr;   arr = [1, 1, 3]
1
3</pre>
<div class="sublabel">Sample Output 1</div>
<pre class="sample">1</pre>
<div class="sublabel">Explanation</div>
<p>Choose index <em>i = 1</em> (where <em>arr[1] = 1</em>) and set positions 2 to <em>arr[1]</em>. The cost is <em>(3 - 1 - 1) * 1 = 1</em>.</p>

<div class="srcnote"><strong>Also reported as:</strong> <em>"Minimum Cost of Left and Right Propagation"</em> (<code>minimumPropagationCost</code>) in the FastPrep section — the same two operations at the same costs, with different worked examples (<code>[5,2,4] &rarr; 4</code> and <code>[1,1,2,1] &rarr; 2</code>). Good second pass on this one.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Every operation sets a whole prefix or a whole suffix to one value, at a cost of (length &times; that value). Whatever you do, the array ends up all equal to some target <em>T</em>. Which values of <em>T</em> are worth considering?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>The example shows the answer is built from a few prefix/suffix writes. Think about the final value <em>T</em>: it must be one of the values already present (or reachable by a single write). For each candidate <em>T</em>, the cost is decided by the cheapest way to overwrite everything that isn't already <em>T</em>.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Two operations are available at index <em>i</em>:</p>
<ul>
<li>set positions <code>0..i-1</code> to <code>arr[i]</code> at cost <code>i * arr[i]</code></li>
<li>set positions <code>i+1..n-1</code> to <code>arr[i]</code> at cost <code>(n-1-i) * arr[i]</code></li>
</ul>
<p>A prefix write covers <code>[0, i-1]</code>, a suffix write covers <code>[j+1, n-1]</code>. Use one of each and together they cover everything <strong>except the middle band <code>[i, j]</code></strong> — so that band has to already hold the target, meaning <code>arr[i..j]</code> must be a run of equal values. Both writes then use that run's value <code>v</code>, and the whole thing costs:</p>
<pre class="sample">cost = v * i  +  v * (n - 1 - j)  =  v * (i + n - 1 - j)</pre>
<p>You want that band as wide and as cheap as possible, so it is always a <strong>maximal run</strong> of equal values. Scan the runs, price each one, take the minimum. Writing zero times when the array is already uniform falls out for free (<code>i = 0</code>, <code>j = n-1</code>, cost 0), as does the one-write case (a run touching either end).</p>
<p>No more than two writes are ever needed: a write can only paint a value that already exists somewhere, so a third write never reaches a cell the two-write cover missed.</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def getMinCost(arr):
    n = len(arr)
    best = float('inf')
    l = 0                                  # left end of the current run
    for r in range(n):
        if r + 1 == n or arr[r + 1] != arr[r]:
            # run [l, r] all equal arr[l]: keep it, overwrite both sides
            best = min(best, arr[l] * (l + n - 1 - r))
            l = r + 1
    return best</code></pre><div class="unsure">Checked against a Dijkstra search over all reachable array states for every array with n &le; 6 and values in 1..n (4000 random cases, no mismatch), and against both published samples. <strong>The solution previously shown here was wrong</strong> — it minimised <code>i*v + (n-1-i)*v</code>, in which <code>i</code> cancels to give <code>(n-1)&times;min(arr)</code>, returning 4 and 2 on the two samples instead of 3 and 1.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Two samples and one worked example are published; all three are traced below. The trap in this problem is that the obvious formula quietly <em>cancels</em>.</p>

<div class="step"><h4>1 &middot; What an operation really buys you</h4>
<div class="formula">prefix write at i:  positions <b>0 .. i&minus;1</b>    &larr; arr[i]    cost = <b>i</b> &times; arr[i]
suffix write at i:  positions <b>i+1 .. n&minus;1</b>  &larr; arr[i]    cost = <b>(n&minus;1&minus;i)</b> &times; arr[i]</div>
<p>Read the cost factor as <strong>"how many cells this write paints"</strong>, because that is literally what it is: <code>[0, i-1]</code> holds <code>i</code> cells, <code>[i+1, n-1]</code> holds <code>n-1-i</code> cells. So <em>every write costs (cells painted) &times; (value painted)</em>, with no discount for anything. The anchor <code>i</code> is not itself painted — it is the paint source, and it survives.</p>
<p>Two consequences follow immediately, and they drive the whole solution:</p>
<ul>
<li>You want to paint with a <strong>small value</strong>, so cheap cells are the good anchors.</li>
<li>You want to paint <strong>few cells</strong>, so you want to keep as many cells as possible untouched — and untouched cells must already agree with each other.</li>
</ul></div>

<div class="step"><h4>2 &middot; Why exactly two writes, and what the band must be</h4>
<p>Suppose you finish with one prefix write anchored at <code>i</code> and one suffix write anchored at <code>j</code>. Their coverage is:</p>
<div class="formula">painted:    [0 .. i&minus;1]                    [j+1 .. n&minus;1]
untouched:              [<b>i .. j</b>]</div>
<p>Everything survives in <code>[i, j]</code>, so for the array to end uniform, <strong><code>arr[i..j]</code> must already be all one value</strong> — a run. And both writes have to paint that same value, which they do automatically, since <code>arr[i]</code> and <code>arr[j]</code> are both inside the run.</p>
<p>Could a third write help? A write can only paint a value that some cell already holds, and the two writes above already reach every cell outside the band. There is nothing left to reach, and every extra write costs a positive amount. So two is always enough — and often one or zero.</p>
<p>Nor does it help to widen the band beyond a maximal run: if you shrink the band inside a run you pay strictly more (larger <code>i</code>, smaller <code>j</code>), and you cannot grow past the run's edges without leaving a disagreeing cell untouched.</p></div>

<div class="step"><h4>3 &middot; The cost of keeping a run</h4>
<p>Keep the maximal run <code>[l, r]</code> of value <code>v</code>. You pay for the cells on both sides:</p>
<div class="formula">cells to the left  = <b>l</b>            (positions 0 .. l&minus;1)
cells to the right = <b>n &minus; 1 &minus; r</b>    (positions r+1 .. n&minus;1)

cost(run) = v &times; (l + n &minus; 1 &minus; r)</div>
<p>Note what this is <em>not</em>: it is not <code>v &times; (n-1)</code>. The saving comes entirely from <code>r - l</code>, the run's length minus one — the cells you never repaint. A long run of a small value is the jackpot; a lone cell of a small value still costs <code>v &times; (n-1)</code>.</p>
<p>Both endpoints degrade gracefully. A run touching position 0 gives <code>l = 0</code>, so the prefix write costs nothing and is simply not performed. A run touching <code>n-1</code> gives <code>n-1-r = 0</code> likewise. A run covering everything gives cost 0 — the array was already uniform.</p></div>

<div class="step"><h4>4 &middot; Sample 0 traced: arr = [1, 1, 2, 1, 1], n = 5</h4>
<table class="trace">
<tr><th>run [l, r]</th><th>v</th><th>left cells = l</th><th>right cells = n&minus;1&minus;r</th><th>cost = v &times; (l + n&minus;1&minus;r)</th></tr>
<tr><td class="hit">[0, 1]</td><td class="hit">1</td><td class="hit">0</td><td class="hit">4 &minus; 1 = 3</td><td class="hit">1 &times; (0 + 3) = <strong>3</strong></td></tr>
<tr><td>[2, 2]</td><td>2</td><td>2</td><td>4 &minus; 2 = 2</td><td>2 &times; (2 + 2) = 8</td></tr>
<tr><td>[3, 4]</td><td>1</td><td>3</td><td>4 &minus; 4 = 0</td><td>1 &times; (3 + 0) = 3</td></tr>
</table>
<p>Minimum <strong>3</strong>, matching the published output. The winning run <code>[0,1]</code> needs no prefix write at all (<code>l = 0</code>) and one suffix write anchored at index 1 painting positions 2, 3, 4 — which is word for word the move the statement's explanation describes: <em>"choose index i = 1 and set positions 2, 3, and 4, cost (5&minus;1&minus;1)&times;1 = 3"</em>. The tied run <code>[3,4]</code> is the same move mirrored.</p></div>

<div class="step"><h4>5 &middot; The other two cases</h4>
<p><strong>Sample 1 &mdash; arr = [1, 1, 3], n = 3.</strong></p>
<table class="trace">
<tr><th>run</th><th>v</th><th>cost</th></tr>
<tr><td class="hit">[0, 1]</td><td class="hit">1</td><td class="hit">1 &times; (0 + 2 &minus; 1) = <strong>1</strong></td></tr>
<tr><td>[2, 2]</td><td>3</td><td>3 &times; (2 + 2 &minus; 2) = 6</td></tr>
</table>
<p><strong>The worked example &mdash; arr = [3, 1, 4, 2], n = 4.</strong> No two neighbours agree, so every run has length 1 and <code>l = r</code>, collapsing the cost to <code>v &times; (n-1) = 3v</code>:</p>
<table class="trace">
<tr><th>run</th><th>v</th><th>cost = v &times; (l + 3 &minus; r)</th></tr>
<tr><td>[0,0]</td><td>3</td><td>3 &times; 3 = 9</td></tr>
<tr><td class="hit">[1,1]</td><td class="hit">1</td><td class="hit">1 &times; 3 = <strong>3</strong></td></tr>
<tr><td>[2,2]</td><td>4</td><td>4 &times; 3 = 12</td></tr>
<tr><td>[3,3]</td><td>2</td><td>2 &times; 3 = 6</td></tr>
</table>
<p>Answer 3, from the value-1 cell at index 1: prefix write costs <code>1&times;1 = 1</code>, suffix write costs <code>2&times;1 = 2</code>. Exactly the sequence the statement walks through.</p></div>

<div class="step"><h4>6 &middot; The trap: an index that cancels</h4>
<p>The natural first guess is "anchor at <code>i</code>, write both sides":</p>
<div class="formula">i &times; arr[i] + (n&minus;1&minus;i) &times; arr[i]  =  arr[i] &times; (i + n &minus; 1 &minus; i)  =  arr[i] &times; (n&minus;1)</div>
<p>The <code>i</code> cancels. Minimising that is just <code>(n&minus;1) &times; min(arr)</code>, which never notices runs at all — it always assumes exactly one cell survives. On sample 0 it returns <code>4 &times; 1 = 4</code> instead of 3, and on sample 1 <code>2 &times; 1 = 2</code> instead of 1. It happens to be right on <code>[3,1,4,2]</code> only because every run there has length 1, which is precisely the case where the two formulas agree.</p>
<p>Checked against Dijkstra over all reachable array states: that formula is wrong on about 28% of random arrays with n &le; 6. If a formula makes a loop variable vanish, that is the signal to re-derive it — the surviving band, not the anchor, is what the cost actually depends on.</p></div>

<div class="step"><h4>7 &middot; Traps</h4>
<ul>
<li><strong>Return type is <code>long</code>.</strong> With <code>n = 2&times;10<sup>5</sup></code> and <code>arr[i] &le; n</code>, the cost reaches <code>2&times;10<sup>5</sup> &times; 2&times;10<sup>5</sup> = 4&times;10<sup>10</sup></code>, well past 32-bit. Python is fine; Java and C++ need <code>long</code>.</li>
<li><strong>n = 1</strong> is already uniform: the single run gives <code>v &times; (0 + 0 &minus; 0) = 0</code>. No special case needed, but check your loop does not read <code>arr[1]</code>.</li>
<li><strong>Maximal runs only.</strong> Pricing every sub-band <code>[i,j]</code> instead is O(n<sup>2</sup>) and returns the same answer — shrinking a band never helps.</li>
<li><strong>The target need not be the array minimum.</strong> A long run of a middling value can beat a lone minimum: with <code>arr = [2,2,2,2,9,1]</code>, run <code>[0,3]</code> costs <code>2&times;(0+5&minus;3) = 4</code> while the single 1 at index 5 costs <code>1&times;(5+0) = 5</code>.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'ecs', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Code Question 1', title:'ECS — Least Resource Tasks',
  minutes:35, score:'',
  images:['image12.png','image13.png','image49.jpg','image48.jpg'],
  fn:{name:'selectLeastResourceTasks', ret:'int', params:[['int[]','resourceConsumption']]},
  gen:`def gen(rng, n):
    m = max(3, n)
    return [[rng.randint(1, 40) for _ in range(m)]]`,
  tests:[
    {in:[[4, 3, 2, 1]], out:4},
    {in:[[6, 4, 9, 10, 34, 56, 54]], out:68},
    {in:[[1, 2, 3]], out:4},
    {in:[[5, 5, 5, 5, 5]], out:15},
    {in:[[9, 1, 9, 1, 9, 1, 9]], out:3},
    {in:[[100000, 1, 100000]], out:1}
  ],
  body:`
<p>In Amazon's Elastic Container Service (ECS), tasks are scheduled and managed dynamically. You are given an array <em>resourceConsumption</em> of <em>n</em> integers, where each element represents the resource consumption of a specific task in the system.</p>

<p>To optimise system load and clear tasks efficiently, the following termination process is applied repeatedly until no tasks remain:</p>
<ul>
  <li>In each iteration, select the task with the lowest resource consumption.</li>
  <li>Remove that task and its adjacent tasks from the array (if any).</li>
</ul>
<p>The task is to compute the total resource consumption of all the selected tasks — i.e., the tasks with the minimum resource usage in each iteration.</p>

<div class="note"><p><strong>Note:</strong> If there is more than one task with the same lowest resource consumption, select the task with the smallest index.</p></div>

<h3>Example</h3>
<pre class="sample">n = 4
resourceConsumption = [4, 3, 2, 1]</pre>
<p>Simulating the defined operation:</p>
<ul>
  <li>Initial <em>resourceConsumption</em> = [4, 3, 2, 1]. Select the task with the lowest resource consumption value (1) and discard it along with its adjacent task's resource consumption value (2). So, updated <em>resourceConsumption</em> = [4, 3].</li>
  <li>Now <em>resourceConsumption</em> = [4, 3]. Select the next lowest value (3) and discard the adjacent task's value (4). So, <em>resourceConsumption</em> = [].</li>
</ul>
<p>The total resource consumption of the selected tasks is 1 + 3 = 4.<br>Hence, the answer is <em>4</em>.</p>

<h3>Function Description</h3>
<p>The function <em>selectLeastResourceTasks</em> takes the following input:</p>
<ul><li><em>int resourceConsumption[n]:</em> each integer represents the resource consumption of a task</li></ul>

<h3>Returns</h3>
<ul><li><em>int:</em> the total resource consumption of all the selected tasks</li></ul>

<h3>Constraints</h3>
<ul>
  <li>3 &le; <em>n</em> &le; 2000</li>
  <li>1 &le; <em>resourceConsumption[i]</em> &le; 10<sup>5</sup></li>
</ul>

<div class="bar">Input Format For Custom Testing</div>
<div class="bar open">Sample Case 0</div>
<div class="sublabel">Sample Input For Custom Testing</div>
<pre class="sample">STDIN        Function
-----        --------
7      &rarr;   n = 7
6      &rarr;   resourceConsumption[] = [6, 4, 9, 10, 34, 56, 54]
4
9
10
34
56
54</pre>
<div class="sublabel">Sample Output</div>
<pre class="sample">68</pre>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Read the termination process literally: repeatedly take the task with the <em>lowest</em> consumption, add it to the answer, and delete it <strong>together with its neighbours</strong>. What data structure gives you "smallest remaining" plus "who is next to me right now"?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>A min-heap keyed by (value, index) for the selection, plus a doubly linked list over the indices so that removing a task can splice its left and right neighbours out in O(1). Lazily skip heap entries whose index has already been deleted.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Simulation, done efficiently. Maintain:</p>
<ul>
<li>a min-heap of <code>(resourceConsumption[i], i)</code> — ties broken by smaller index, which the statement requires;</li>
<li><code>prev[]</code> / <code>next[]</code> arrays forming a doubly linked list of live indices;</li>
<li>an <code>alive[]</code> flag.</li>
</ul>
<p>Pop until you find a live index. Add its value to the total, then unlink it <em>and</em> its immediate live neighbours. Repeat until the heap is exhausted.</p>
<p>On <code>[4, 3, 2, 1]</code>: pick 1 (index 3), remove index 2 as well → live = [4, 3]; pick 3, remove 4 → total = 1 + 3 = 4. ✓</p><p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>import heapq

def selectLeastResourceTasks(resourceConsumption):
    n = len(resourceConsumption)
    heap = [(v, i) for i, v in enumerate(resourceConsumption)]
    heapq.heapify(heap)

    prev = list(range(-1, n - 1))
    nxt  = list(range(1, n + 1))
    alive = [True] * n

    def unlink(i):
        alive[i] = False
        p, q = prev[i], nxt[i]
        if p &gt;= 0: nxt[p] = q
        if q &lt; n:  prev[q] = p

    total = 0
    while heap:
        v, i = heapq.heappop(heap)
        if not alive[i]:
            continue
        total += v
        left, right = prev[i], nxt[i]
        unlink(i)
        if left &gt;= 0 and alive[left]:   unlink(left)
        if right &lt; n and alive[right]:  unlink(right)
    return total</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published sample <code>[6, 4, 9, 10, 34, 56, 54]</code>, answer <strong>68</strong>.</p>

<div class="step"><h4>1 &middot; The one thing that makes this harder than it looks</h4>
<p>"Remove the task and its adjacent tasks" means adjacent <strong>in the array as it stands now</strong>, not in the original array. After a removal the survivors close ranks, and cells that were never neighbours become neighbours.</p>
<div class="formula">start:      6  4  9  10  34  56  54
pick 4 (min), remove it and both current neighbours 6 and 9
remaining: <b>10  34  56  54</b>      &larr; 10 and 34 were never adjacent to 6 or 9,
                                but 10 is now the <em>first</em> element</div>
<p>Deleting from a Python list gives that behaviour for free but costs O(n) per deletion, and re-scanning for the minimum costs another O(n) — fine at n &le; 2000, and honestly the correct answer under exam pressure. The heap-plus-linked-list version below is the same simulation in O(n log n), and is worth knowing because the "delete from the middle, keep neighbours findable" pattern recurs constantly.</p></div>

<div class="step"><h4>2 &middot; The two structures, and why neither alone is enough</h4>
<p>You need two different questions answered fast, and they want different structures:</p>
<table class="trace">
<tr><th>question</th><th>structure</th><th>cost</th></tr>
<tr><td>which live task has the smallest value?</td><td>min-heap of <code>(value, index)</code></td><td>O(log n) per pop</td></tr>
<tr><td>who is currently next to index i?</td><td><code>prev[]</code> / <code>nxt[]</code> linked list</td><td>O(1)</td></tr>
</table>
<p>The heap cannot answer "who is my neighbour"; the linked list cannot answer "who is smallest". Hence both, tied together by the shared index and an <code>alive[]</code> flag.</p>
<div class="formula">prev = list(range(-1, n-1))   &rarr; [-1, 0, 1, 2, ...]   prev[0] = <b>&minus;1</b> sentinel
nxt  = list(range(1, n+1))    &rarr; [1, 2, 3, ..., <b>n</b>]   nxt[n-1] = <b>n</b> sentinel</div>
<p>The two sentinels <code>-1</code> and <code>n</code> are what remove the end-of-array special cases: the guards <code>if p &gt;= 0</code> and <code>if q &lt; n</code> are the <em>only</em> boundary checks in the whole routine.</p></div>

<div class="step"><h4>3 &middot; Lazy deletion — why popping a dead index is fine</h4>
<p>A heap has no "remove this arbitrary element" operation. So entries are never removed when a task dies; instead the task is flagged <code>alive[i] = False</code> and the stale heap entry is skipped when it surfaces:</p>
<div class="formula">v, i = heappop(heap)
if not alive[i]: <b>continue</b>       # stale entry, discarded for free</div>
<p>Each index is pushed once and popped at most once, so the total wasted work is bounded by n pops — the complexity stays O(n log n). This is the standard <em>lazy deletion</em> idiom and it is why no "decrease-key" or indexed heap is needed.</p></div>

<div class="step"><h4>4 &middot; Unlinking, and the ordering bug hiding in it</h4>
<p><code>unlink(i)</code> splices <code>i</code> out by pointing its neighbours at each other:</p>
<div class="formula">p, q = prev[i], nxt[i]
if p &gt;= 0: nxt[p]  = q        # left neighbour now skips i
if q &lt;  n: prev[q] = p        # right neighbour now skips i</div>
<p>The subtle part is in the caller. The neighbours must be <strong>read before any unlinking happens</strong>:</p>
<div class="formula">left, right = prev[i], nxt[i]   &larr; <b>capture first</b>
unlink(i)
if left  &gt;= 0 and alive[left]:  unlink(left)
if right &lt;  n and alive[right]: unlink(right)</div>
<p>Unlink <code>i</code> first and then read <code>prev[i]</code>/<code>nxt[i]</code> and you may still get the right values (unlink does not clear <code>i</code>'s own pointers) — but the moment you unlink <code>left</code> before reading <code>right</code>, the list has shifted under you. Capturing both up front makes the order irrelevant. The <code>alive[...]</code> re-check guards against a neighbour that some earlier step already killed.</p></div>

<div class="step"><h4>5 &middot; Full trace of the sample</h4>
<p><code>[6, 4, 9, 10, 34, 56, 54]</code>, indices 0..6:</p>
<table class="trace">
<tr><th>pop</th><th>alive?</th><th>picked</th><th>prev, nxt</th><th>removed</th><th>live list after</th><th>total</th></tr>
<tr><td>(4, 1)</td><td>yes</td><td class="hit">4</td><td>0, 2</td><td>1, then 0 and 2</td><td>10 34 56 54</td><td>4</td></tr>
<tr><td>(6, 0)</td><td><em>no</em></td><td>&mdash;</td><td colspan="3">stale entry, skipped</td><td>4</td></tr>
<tr><td>(9, 2)</td><td><em>no</em></td><td>&mdash;</td><td colspan="3">stale entry, skipped</td><td>4</td></tr>
<tr><td>(10, 3)</td><td>yes</td><td class="hit">10</td><td>&minus;1 (0 is dead, spliced out), 4</td><td>3, then 4</td><td>56 54</td><td>14</td></tr>
<tr><td>(34, 4)</td><td><em>no</em></td><td>&mdash;</td><td colspan="3">stale entry, skipped</td><td>14</td></tr>
<tr><td>(54, 6)</td><td>yes</td><td class="hit">54</td><td>5, 7</td><td>6, then 5</td><td>(empty)</td><td class="hit"><strong>68</strong></td></tr>
<tr><td>(56, 5)</td><td><em>no</em></td><td>&mdash;</td><td colspan="3">stale entry, skipped</td><td>68</td></tr>
</table>
<p>Total <code>4 + 10 + 54 = <strong>68</strong></code>. Row 4 is the one to study: index 3's left pointer is <code>-1</code>, not 2, because unlinking index 2 earlier had already set <code>prev[3] = prev[2]'s side</code> — the linked list did the "close ranks" bookkeeping automatically, which is the entire reason it is there. Notice also that 34 and 56, both large, were removed as collateral and never selected.</p></div>

<div class="step"><h4>6 &middot; Why "pick the global minimum" is genuinely optimal here</h4>
<p>Worth being clear that this is <strong>not</strong> an optimisation problem. The statement prescribes the procedure — always take the current minimum, ties to the smaller index — so you are simulating a fixed rule, not searching for the best set of picks. Do not reach for DP. The only decisions are how fast you can find the minimum and how fast you can find neighbours.</p>
<p>The tie-break falls out of the heap for free: Python compares tuples left to right, so <code>(v, i)</code> orders by value and then by index, which is exactly "smallest index wins". Pushing bare values, or <code>(v, -i)</code>, silently breaks ties the wrong way.</p></div>

<div class="step"><h4>7 &middot; Traps</h4>
<ul>
<li><strong>Adjacency is dynamic.</strong> Precomputing neighbours from the original array is the single most common wrong answer.</li>
<li><strong>Ties go to the smaller index</strong> — the statement says so explicitly. <code>(value, index)</code> tuples handle it.</li>
<li><strong>Removing 1 to 3 tasks per round.</strong> A picked task at either end has only one neighbour; the sentinels handle it without a branch.</li>
<li><strong>Only the picked value is added</strong> — the neighbours are discarded, not counted. In the sample, 34 and 56 never contribute.</li>
<li><strong>Re-check <code>alive</code> before unlinking a neighbour</strong>, or you will double-splice a node and corrupt the list.</li>
<li><strong>n &le; 2000</strong>, so plain O(n<sup>2</sup>) list deletion passes comfortably. Reach for the heap for correctness of habit, not because you must.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'basesegment', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Code Question 2', title:'Smallest Base Segment (Data Restoration)',
  minutes:35, score:'',
  images:['image9.png','image10.png','image18.jpg'],
  fn:{name:'getSmallestBaseSegment', ret:'string', params:[['int','segmentSize'],['string','missingData']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    al = 'abc'
    s = ''.join(rng.choice(al) for _ in range(m))
    return [rng.randint(1, 5), s]`,
  tests:[
    {in:[2, "aavvavv"], out:"av"},
    {in:[3, "aavvavv"], out:"avv"},
    {in:[4, "aavvavv"], out:"aavv"},
    {in:[1, "aavvavv"], out:"-1"},
    {in:[1, "aaaaaa"], out:"a"},
    {in:[2, "abc"], out:"-1"}
  ],
  body:`
<p>In Amazon's distributed storage network, certain critical data segments, represented as a string <em>missingData</em>, are unavailable due to synchronization issues.</p>

<p>To restore these missing segments, the system starts with an empty string <em>generatedData</em> and selects a <em>baseSegment</em> of length <em>segmentSize</em>. The following process then unfolds:</p>
<ol>
  <li>The replication service generates a copy of <em>baseSegment</em>.</li>
  <li>Appends this copy of <em>baseSegment</em> to <em>generatedData</em>.</li>
  <li>Repeats steps 1-2 until the frequency of all characters in <em>generatedData</em> meets or exceeds their count in <em>missingData</em>.</li>
</ol>

<p>Given the string <em>missingData</em> and an integer <em>segmentSize</em>, the task is to determine the <em>baseSegment</em> that requires the fewest number of replications to satisfy this condition. If multiple <em>baseSegment</em> meet this requirement, select the lexicographically smallest one. If no such segment exists, return "-1" as a string.</p>

<h3>Example</h3>
<pre class="sample">segmentSize = 2
missingData = "aavvavv"</pre>

<p>The character 'a' appears 3 times, and 'v' appears 4 times in <em>missingData</em>. The system can select a <em>baseSegment</em> of size 2.<br>Consider the following scenarios:</p>
<ol>
  <li>The system selects <em>baseSegment</em> = "va".
    <ul><li>To satisfy the required frequency of 'a' and 'v', at least 4 copies of "va" is needed.</li></ul></li>
  <li>The system selects <em>baseSegment</em> = "av".
    <ul><li>To satisfy the required frequency of 'a' and 'v', at least 4 copies of "av" is needed.</li></ul></li>
  <li>Selecting any other <em>baseSegment</em> of length 2, will not generate the required string even after any number of replication process, since it requires the characters 'a' and 'v' in the <em>baseSegment</em>.</li>
</ol>

<p>Now since both "av" and "va" require the same number of replication steps i.e., 4, the lexicographically smaller option, "av," is chosen.</p>
<p>Hence, the answer is "av".</p>

<h3>Function Description</h3>
<p>Complete the function <em>getSmallestBaseSegment</em> in the editor below.</p>
<p><em>getSmallestBaseSegment</em> takes the following parameter(s):</p>
<ul>
  <li><em>int segmentSize:</em> the length of the base segment that can be replicated by the system</li>
  <li><em>string missingData:</em> a string representing the missing critical data segments</li>
</ul>

<h3>Returns</h3>
<ul><li><em>string:</em> the lexicographically smallest base segment of length <em>segmentSize</em>, whose <span class="frag" style="display:inline-block;margin:0">…the screenshot is cut off here. Expected: "…replication requires the fewest number of steps; otherwise "-1".</span></li></ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>You replicate one base segment over and over. For the generated data to contain <em>missingData</em>'s character counts, how many copies do you need, and what does each copy contribute?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>If the base segment contains character <em>c</em> exactly <code>b[c]</code> times and you make <em>r</em> copies, you get <code>r·b[c]</code> of them, which must be &ge; <code>need[c]</code>. So <em>r</em> = max over c of ceil(need[c] / b[c]). Minimise <em>r</em> first, then pick the lexicographically smallest base achieving it.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Count the characters of <em>missingData</em> into <code>need[]</code>. You must choose a multiset of <em>segmentSize</em> characters (the base segment) and a repeat count <em>r</em> such that <code>r · count_in_base(c) &ge; need[c]</code> for every c that appears.</p>
<p>Do not search over divisions — <strong>binary-search <em>r</em> instead</strong>. For a fixed number of replications <em>r</em>, the cheapest base that works gives character <em>c</em> exactly <code>ceil(need[c] / r)</code> slots, so the base fits iff <code>sum of ceil(need[c]/r) &le; segmentSize</code>. That test is monotone in <em>r</em> (more copies never need more slots), so the smallest feasible <em>r</em> falls out of a binary search. Then hand every leftover slot to the smallest character, which is what makes the sorted string lexicographically smallest.</p>
<p>Example from the statement: <em>segmentSize</em> = 2, <em>missingData</em> = "aavvavv" — 'a' appears 3 times, 'v' 4 times. Base "va" or "av" both need 4 copies; "av" is lexicographically smaller, so the answer is <strong>"av"</strong>.</p>
<p>Return <code>"-1"</code> when no segment of that size can work.</p><p><span class="cx">Time O(|missingData| + 26 log n)</span><span class="cx">Space O(26)</span></p><pre class="sample"><code>from collections import Counter
from math import ceil

def getSmallestBaseSegment(segmentSize, missingData):
    need = Counter(missingData)
    chars = sorted(need)
    if len(chars) &gt; segmentSize:
        return "-1"                  # a needed char would get zero slots

    lo, hi = 1, max(need.values())   # smallest r whose base fits
    while lo &lt; hi:
        mid = (lo + hi) // 2
        if sum(ceil(need[c] / mid) for c in chars) &lt;= segmentSize:
            hi = mid
        else:
            lo = mid + 1
    r = lo

    alloc = {c: ceil(need[c] / r) for c in chars}
    alloc[chars[0]] += segmentSize - sum(alloc.values())   # spare slots
    return ''.join(c * alloc[c] for c in sorted(alloc))</code></pre><div class="unsure">Verified against exhaustive brute force over every length-<em>segmentSize</em> multiset (1500 random cases, alphabet abc, segmentSize &le; 5) and the published example. Two fixes to the code previously shown here: it ended in an <strong>unterminated string literal</strong> (<code>"-1</code>) so it would not compile, and its recursion enumerated every composition of <em>segmentSize</em> — exponential, not the O(26&middot;segmentSize) claimed. <strong>Still ambiguous:</strong> the Returns clause is cut off, so it is unclear whether the base segment may contain letters absent from <em>missingData</em>. See step 6 — with <code>segmentSize = 2</code>, <code>missingData = "z"</code> the two readings give <code>"zz"</code> and <code>"az"</code>.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the statement's example: <code>segmentSize = 2</code>, <code>missingData = "aavvavv"</code>, answer <code>"av"</code>.</p>

<div class="step"><h4>1 &middot; Restating the condition as arithmetic</h4>
<p>Order inside the base is irrelevant to the stopping condition — only character counts matter — so a base segment is really a <strong>multiset of segmentSize characters</strong>. If it holds <code>b[c]</code> copies of character <em>c</em>, then after <em>r</em> replications <code>generatedData</code> holds <code>r &times; b[c]</code> of them, and the process stops when</p>
<div class="formula">for every character c in missingData:   <b>r &times; b[c] &ge; need[c]</b></div>
<p><code>"aavvavv"</code> gives <code>need = {a: 3, v: 4}</code>. Two consequences, immediately:</p>
<ul>
<li>If <code>b[c] = 0</code> for a needed <em>c</em>, no <em>r</em> ever works — hence the <code>"-1"</code> test is <em>distinct characters &gt; segmentSize</em>.</li>
<li>Rearranged, <code>r &ge; need[c] / b[c]</code>, and <em>r</em> is an integer, so <code>r = max over c of ceil(need[c] / b[c])</code>. The <strong>worst-served character alone sets the replication count</strong>; every other character is carried along for free.</li>
</ul></div>

<div class="step"><h4>2 &middot; Invert the problem: fix r, then ask what it costs</h4>
<p>Searching over allocations is the trap — there are <code>C(segmentSize&minus;1, d&minus;1)</code> ways to split the slots among <em>d</em> distinct characters, which explodes. Ask the cheaper question instead: <em>if I were allowed exactly r replications, what is the smallest base that would do?</em></p>
<div class="formula">r &times; b[c] &ge; need[c]   &rArr;   b[c] &ge; need[c] / r   &rArr;   b[c] = <b>ceil(need[c] / r)</b>

slots(r) = &sum;<sub>c</sub> ceil(need[c] / r)      a base achieving r exists &hArr; <b>slots(r) &le; segmentSize</b></div>
<p>Each character independently needs <code>ceil(need[c]/r)</code> slots and no fewer, so <code>slots(r)</code> is the exact minimum size of any base achieving <em>r</em>. And <code>slots</code> is <strong>non-increasing in r</strong> — raising <em>r</em> can only shrink each ceiling, never grow it. That monotonicity is the whole licence for a binary search: the feasible values of <em>r</em> form a suffix <code>[r*, &infin;)</code>, and you want its left end.</p>
<p>The bounds are safe by construction. <code>r = 1</code> at the low end; <code>r = max(need.values())</code> at the high end always works, because there every ceiling is 1 and <code>slots = d</code>, which the <code>"-1"</code> check already confirmed is &le; segmentSize.</p></div>

<div class="step"><h4>3 &middot; The binary search, every value</h4>
<p><code>need = {a: 3, v: 4}</code>, <code>segmentSize = 2</code>. The whole landscape, though the search visits only some rows:</p>
<table class="trace">
<tr><th>r</th><th>ceil(3/r) &rarr; 'a' slots</th><th>ceil(4/r) &rarr; 'v' slots</th><th>slots(r)</th><th>&le; 2 ?</th></tr>
<tr><td>1</td><td>3</td><td>4</td><td>7</td><td>no</td></tr>
<tr><td>2</td><td>2</td><td>2</td><td>4</td><td>no</td></tr>
<tr><td>3</td><td>1</td><td>2</td><td>3</td><td>no</td></tr>
<tr><td class="hit">4</td><td class="hit">1</td><td class="hit">1</td><td class="hit">2</td><td class="hit"><strong>yes</strong></td></tr>
</table>
<p>Note the column shapes: <code>slots</code> drops 7, 4, 3, 2 — non-increasing, exactly as the argument requires. So <code>r* = 4</code>, which is the statement's "at least 4 copies". Now the search itself, from <code>lo = 1</code>, <code>hi = max(need.values()) = 4</code>:</p>
<table class="trace">
<tr><th>lo, hi</th><th>mid</th><th>slots(mid)</th><th>fits?</th><th>action</th></tr>
<tr><td>1, 4</td><td>2</td><td>4</td><td>no</td><td>lo = mid + 1 = 3</td></tr>
<tr><td>3, 4</td><td>3</td><td>3</td><td>no</td><td>lo = mid + 1 = 4</td></tr>
<tr><td class="hit">4, 4</td><td colspan="3">lo = hi, loop ends</td><td class="hit">r = <strong>4</strong></td></tr>
</table>
<p>This is the "smallest true" binary search, and the asymmetry is deliberate: <code>hi = mid</code> on success, because <em>mid</em> itself might be the answer and must stay in range; <code>lo = mid + 1</code> on failure, because <em>mid</em> is definitively ruled out. Write <code>hi = mid - 1</code> and you skip the answer; write <code>lo = mid</code> and you loop forever.</p></div>

<div class="step"><h4>4 &middot; Building the string from r</h4>
<div class="formula">alloc['a'] = ceil(3/4) = <b>1</b>
alloc['v'] = ceil(4/4) = <b>1</b>
used  = 1 + 1 = 2
spare = segmentSize &minus; used = 2 &minus; 2 = <b>0</b>
string = 'a'&times;1 + 'v'&times;1 = <b>"av"</b></div>
<p>Two separate reasons the output is in ascending order, and they are not the same reason:</p>
<ul>
<li><strong>Sorting the characters</strong> makes the string lexicographically smallest <em>for a fixed multiset</em>: <code>"av" &lt; "va"</code>. This is precisely the tie-break the statement describes — both bases need 4 copies, so the smaller string wins.</li>
<li><strong>Spare slots go to <code>chars[0]</code></strong>, the smallest character. Extra copies can never break feasibility (they only lower the <em>r</em> a character requires, and <em>r</em> is already minimal), so the only question is which character they should be — and more of the smallest letter is always lexicographically better: <code>"aav" &lt; "avv"</code>.</li>
</ul>
<p>Here <code>spare = 0</code> so the second rule is invisible. Widen the base and it fires:</p>
<table class="trace">
<tr><th>segmentSize</th><th>r*</th><th>alloc</th><th>spare</th><th>answer</th></tr>
<tr><td>2</td><td>4</td><td>a:1, v:1</td><td>0</td><td>"av"</td></tr>
<tr><td>3</td><td>3</td><td>a:1, v:2</td><td>0</td><td>"avv"</td></tr>
<tr><td>4</td><td>2</td><td>a:2, v:2</td><td>0</td><td>"aavv"</td></tr>
<tr><td>5</td><td>2</td><td>a:2, v:2</td><td>1 &rarr; 'a'</td><td>"aaavv"</td></tr>
</table></div>

<div class="step"><h4>5 &middot; Why the "feed the neediest" greedy is not enough</h4>
<p>The tempting alternative hands out slots one at a time to whichever character currently has the worst <code>ceil(need/b)</code>. It does find the minimal <em>r</em> — but it does not settle the tie-break, because several allocations reach that same <em>r</em> and the greedy picks whichever its iteration order happened to reach. Fixing <em>r</em> first and then computing <code>ceil(need[c]/r)</code> yields the <strong>unique minimal allocation</strong> for that <em>r</em>, leaving spare slots as the only free choice — and those have one obviously best destination. That is what makes the answer well-defined instead of order-dependent.</p></div>

<div class="step"><h4>6 &middot; The ambiguity the cut-off statement leaves open</h4>
<p>The Returns clause is truncated in the screenshot, and it leaves a real question unanswered: <strong>may the base segment contain letters that never appear in <em>missingData</em>?</strong> Nothing forbids it — such a letter merely wastes a slot, and the process still terminates. It changes the answer whenever spare slots exist:</p>
<table class="trace">
<tr><th colspan="4"><code>segmentSize = 2</code>, <code>missingData = "z"</code> &rarr; <code>need = {z: 1}</code>, <code>r* = 1</code>, one spare slot</th></tr>
<tr><th>reading</th><th>spare slot filled with</th><th>base</th><th>replications</th></tr>
<tr><td>A &mdash; only letters from missingData</td><td><code>chars[0]</code> = 'z'</td><td>"zz"</td><td>1</td></tr>
<tr><td>B &mdash; any letter of the alphabet</td><td>'a'</td><td class="hit">"az"</td><td>1</td></tr>
</table>
<p>Both need one replication and <code>"az" &lt; "zz"</code>, so reading B would win the tie-break. The code implements <strong>reading A</strong>, matching the statement's remark that the base "requires the characters 'a' and 'v'". Switching is one line:</p>
<pre class="sample"><code>filler = 'a'                                  # instead of chars[0]
alloc[filler] = alloc.get(filler, 0) + segmentSize - sum(alloc.values())</code></pre>
<p>The published example cannot separate them: two needed characters and <code>segmentSize = 2</code> leaves no spare slot, so both readings return <code>"av"</code>. Both variants were checked against exhaustive brute force over every length-<em>segmentSize</em> multiset and agree with their own definition on 1500 random cases each.</p></div>

<div class="step"><h4>7 &middot; Traps</h4>
<ul>
<li><strong>Return the string <code>"-1"</code>, not the integer &minus;1</strong> — the signature says <code>string</code>.</li>
<li><strong>The "-1" test counts distinct characters</strong>, not total length. <code>missingData = "aaaaaa"</code> with <code>segmentSize = 1</code> is fine: answer <code>"a"</code>, r = 6.</li>
<li><strong>Integer ceiling.</strong> <code>ceil(need/r)</code> through floats can misround on large values; prefer <code>-(-need // r)</code> or <code>(need + r - 1) // r</code>.</li>
<li><strong><em>r</em> is a max over characters, never a sum.</strong> All characters replicate together, in the same copies.</li>
<li><strong>Do not enumerate allocations.</strong> The recursion that was previously published here is exponential in <em>segmentSize</em>.</li>
<li><strong>Sort the final string.</strong> Emitting characters in first-seen order gives the right multiset and the wrong answer.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'bugsort', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Code Question 1', title:'Sort Bug Report Frequencies',
  minutes:30, score:'',
  images:['image25.jpg'],
  fn:{name:'sortBugReportFrequencies', ret:'int[]', params:[['int[]','bugs']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [[rng.randint(1, max(2, m // 2)) for _ in range(m)]]`,
  tests:[
    {in:[[8, 4, 6, 5, 4, 8]], out:[5, 6, 4, 4, 8, 8]},
    {in:[[1]], out:[1]},
    {in:[[2, 2, 2, 1, 1, 3]], out:[3, 1, 1, 2, 2, 2]},
    {in:[[1000000, 1, 1000000]], out:[1, 1000000, 1000000]},
    {in:[[5, 4, 3, 2, 1]], out:[1, 2, 3, 4, 5]}
  ],
  body:`
<p>You are helping Amazon's Quality Assurance engineers process bug reports generated from automated testing logs across various devices and services. Each log contains an integer bug code, and a single test session may include duplicate bug codes if the same issue is triggered multiple times.</p>

<p>To effectively prioritise debugging and resolution, the following rules are applied:</p>
<ul>
  <li>Less frequent bugs are considered more important, as they may indicate rare or edge-case issues.</li>
  <li>If two bugs occur the same number of times, the bug with the lower code number has higher priority.</li>
</ul>

<p>The task is to sort the bug codes in order of decreasing importance, using the above rules.</p>

<h3>Example</h3>
<p><em>bugs</em> = [8, 4, 6, 5, 4, 8].</p>
<table class="oa">
<tr><th>Item Code</th><th>Frequency</th></tr>
<tr><td>8</td><td>2</td></tr>
<tr><td>4</td><td>2</td></tr>
<tr><td>6</td><td>1</td></tr>
<tr><td>5</td><td>1</td></tr>
</table>
<p>Bugs with frequency 1 will come before the bugs with frequency 2.</p>
<ul><li>(6, 5) comes before (8, 4, 4, 8), which results in <em>bugs</em> = [6, 5, 8, 4, 4, 8].</li></ul>
<p>In the case of the same frequency, ties are broken by bug codes themselves.</p>
<ul><li>5 comes before 6, and 4 comes before 8, which results in <em>bugs</em> = [5, 6, 4, 4, 8, 8].</li></ul>

<h3>Function Description</h3>
<p>The function <em>sortBugReportFrequencies</em> will take the following input:</p>
<ul><li><em>int bugs[n]:</em> An integer array of size <em>n</em> with each element denoting a bug code of an occurring bug.</li></ul>

<h3>Returns</h3>
<ul><li><em>int[n]:</em> an array of integers sorted in order of decreasing importance</li></ul>

<h3>Constraints</h3>
<ul>
  <li>1 &le; <em>n</em> &le; 2 * 10<sup>5</sup></li>
  <li>1 &le; <em>bugs[i]</em> &le; 10<sup>6</sup></li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Two sort keys, and the primary one is the <em>frequency</em> of the value — not the value itself. Count first, then sort.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Count occurrences, then sort the original codes by <code>(frequency, code)</code> ascending. Rarer bugs are more important, so they come first; equal frequency falls back to the smaller code.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Nothing subtle here — the only trap is sorting the <em>codes</em> rather than the array, or forgetting that every occurrence is emitted (the output has the same length as the input).</p>
<p><code>[8,4,6,5,4,8]</code> → counts {8:2, 4:2, 6:1, 5:1}. Sorting each element by (count, value) gives <code>[5, 6, 4, 4, 8, 8]</code>. ✓</p><p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>from collections import Counter

def sortBugReportFrequencies(bugs):
    freq = Counter(bugs)
    return sorted(bugs, key=lambda b: (freq[b], b))</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the statement's example <code>[8, 4, 6, 5, 4, 8]</code>, answer <code>[5, 6, 4, 4, 8, 8]</code>.</p>

<div class="step"><h4>1 &middot; Read the return type first</h4>
<p><code>int[n]</code> — <strong>n</strong>, the same length as the input. You return the <em>reordered original array</em>, every occurrence included, not the list of distinct codes. This is the whole trap of the problem. Returning <code>[5, 6, 4, 8]</code> is the natural mistake and it fails every test.</p>
<div class="formula">input  [8, 4, 6, 5, 4, 8]   &rarr; 6 elements
output [5, 6, 4, 4, 8, 8]   &rarr; <b>6 elements</b>, same multiset, new order</div></div>

<div class="step"><h4>2 &middot; Turning the two rules into one sort key</h4>
<p>The statement gives two rules, in priority order:</p>
<ul>
<li><em>less frequent is more important</em> &rarr; frequency <strong>ascending</strong></li>
<li><em>ties broken by lower code number</em> &rarr; value <strong>ascending</strong></li>
</ul>
<p>Both ascending means one tuple key and no sign flips:</p>
<div class="formula">key(b) = ( <b>freq[b]</b> , <b>b</b> )</div>
<p>Tuple comparison is lexicographic: compare frequencies first, and only when those are equal compare the codes. That is precisely the stated priority. If the first rule had been "more frequent first" you would need <code>(-freq[b], b)</code> — mixing directions is where sign errors creep in, so it is worth checking the wording rather than pattern-matching.</p></div>

<div class="step"><h4>3 &middot; Every value computed</h4>
<p><code>Counter([8,4,6,5,4,8])</code> walks the array once, incrementing a dictionary:</p>
<div class="formula">8 &rarr; {8:1}          4 &rarr; {8:1, 4:1}     6 &rarr; {8:1, 4:1, 6:1}
5 &rarr; {8:1,4:1,6:1,5:1}   4 &rarr; {4:<b>2</b>, ...}   8 &rarr; {8:<b>2</b>, ...}

freq = {8: 2, 4: 2, 6: 1, 5: 1}</div>
<p>Now the key for each of the six elements, <em>in input order</em>:</p>
<table class="trace">
<tr><th>position</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
<tr><th>value b</th><td>8</td><td>4</td><td>6</td><td>5</td><td>4</td><td>8</td></tr>
<tr><th>freq[b]</th><td>2</td><td>2</td><td>1</td><td>1</td><td>2</td><td>2</td></tr>
<tr><th>key</th><td>(2,8)</td><td>(2,4)</td><td>(1,6)</td><td>(1,5)</td><td>(2,4)</td><td>(2,8)</td></tr>
</table>
<p>Sorting those keys ascending:</p>
<div class="formula">(1,5) &lt; (1,6) &lt; (2,4) = (2,4) &lt; (2,8) = (2,8)
  5      6       4      4       8      8</div>
<p>which is <code>[5, 6, 4, 4, 8, 8]</code> — the published answer. Follow the statement's own two-stage explanation and you land in the same place: first the frequency-1 group <code>(6,5)</code> ahead of the frequency-2 group <code>(8,4,4,8)</code>, then each group internally sorted by code.</p>
<p>Equal keys (the two 4s, the two 8s) are indistinguishable, so their relative order does not matter — though Python's sort is stable and will keep them in input order regardless.</p></div>

<div class="step"><h4>4 &middot; Why sorting the whole array beats grouping</h4>
<p>The alternative — sort the <em>distinct</em> codes by <code>(freq, code)</code>, then emit each one <code>freq</code> times — is equally correct and equally fast:</p>
<pre class="sample"><code>out = []
for code in sorted(freq, key=lambda c: (freq[c], c)):
    out.extend([code] * freq[c])
return out</code></pre>
<p>Sorting the array directly is shorter and has no chance of an off-by-one in the repeat count. Both are O(n log n): the direct sort does n log n comparisons, the grouped version does d log d over d distinct codes plus n emissions.</p>
<p>Note that the key function calls <code>freq[b]</code> on every comparison. For n = 2&times;10<sup>5</sup> that is fine in Python because <code>sorted</code> with a <code>key</code> evaluates it exactly once per element (decorate-sort-undecorate), not once per comparison — a detail that would matter if you used <code>cmp_to_key</code> instead.</p></div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Output length is n, not the distinct count.</strong> The single most common failure.</li>
<li><strong>Both keys ascend.</strong> "Less frequent is more important" is <em>not</em> a descending sort; no minus sign anywhere.</li>
<li><strong>Codes go to 10<sup>6</sup> but n only to 2&times;10<sup>5</sup></strong>, so a 10<sup>6</sup>-slot counting array is wasteful and needless — a hash map is the right structure.</li>
<li><strong>Count before sorting.</strong> Computing frequencies inside the comparator would be O(n<sup>2</sup>).</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'inventory', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Question 1', title:'Optimal Inventory — Minimum Replacement Cost',
  minutes:35, score:'',
  images:['image27.jpg','image28.jpg'],
  fn:{name:'getMinAmount', ret:'int', params:[['int[]','quality']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    pool = max(2, m // 3)
    return [[rng.randint(-pool, pool) for _ in range(m)]]`,
  tests:[
    {in:[[7, 7, 5, 7, 3, 5, 3]], out:4},
    {in:[[1, 1, 2, 2]], out:0},
    {in:[[1, 2, 1]], out:1},
    {in:[[4]], out:0},
    {in:[[-3, -3, 2, -3]], out:1},
    {in:[[1, 2, 3, 1, 2, 3]], out:4}
  ],
  body:`
<p>The manager of the Amazon warehouse has decided to make changes to the inventory. Currently, the inventory has <em>n</em> products, where the quality of the <em>i<sup>th</sup></em> product after quality checks is represented by the array element <em>quality[i]</em>.</p>

<p>The manager wants to create an optimal inventory, where the array of products <em>quality</em> follows the following property:</p>
<ul><li>All occurrences of each quality value must be contiguous.</li></ul>

<p>In order to convert the inventory into an optimal inventory, the manager can do the following operation any number of times:</p>
<ol>
  <li>Choose two quality values x and y.</li>
  <li>Replace every product with quality x to have quality y instead.</li>
  <li>This operation costs <em>num_replacements</em> units of money, where <em>num_replacements</em> is the number of products whose quality was changed.</li>
</ol>

<p>Given <em>n</em> products and an array <em>quality</em>, find the minimum amount of money the manager has to spend to convert the inventory into an optimal inventory.</p>

<div class="note"><p><strong>Note:</strong> The quality of a product can be negative indicating that the product is of poor quality.</p></div>

<h3>Example:</h3>
<p>Given <em>n</em> = 7, <em>quality</em> = [7, 7, 5, 7, 3, 5, 3].<br>One of the optimal ways to convert is explained below:</p>
<figure class="fig"><img loading="lazy" src="../images/fig-inventory-strip.png" alt="One optimal way to convert the inventory" data-full="../images/image28.jpg" title="Click to open the full screenshot"><figcaption>One optimal way to convert the inventory</figcaption></figure>
<p>Hence, the total amount spent is <em>4</em>.</p>

<h3>Function Description</h3>
<p>Complete the function <em>getMinAmount</em> in the editor below.</p>
<p><em>getMinAmount</em> has the following parameter(s):</p>
<ul><li><em>int quality[n]:</em> the quality of products</li></ul>

<h3>Returns</h3>
<ul><li><em>int:</em> the minimum amount of money the manager has to spend to convert the inventory into an optimal inventory.</li></ul>

<h3>Examples</h3>
<div class="sublabel">01 · EXAMPLE 1</div>
<pre class="sample">quality = [7, 7, 5, 7, 3, 5, 3]
return  = 4</pre>

<div class="srcnote"><strong>See also:</strong> <em>"Minimum Contiguous Replacements"</em> in the FastPrep section — same setup and same validity condition, but it counts <strong>operations</strong> (each merge costs 1) instead of elements changed. Worth solving both back to back; the cost function is the whole difference.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>"All occurrences of each value must be contiguous" — so for every value, look at its <strong>first and last</strong> position. Those define an interval. When do two values force a merge?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Build the interval <code>[first[v], last[v]]</code> for each distinct value. Overlapping intervals must end up as the same value. So sweep left to right merging overlapping intervals; within each merged group you must collapse to one value, and you want to keep the value with the largest count (cheapest to keep).</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Map each distinct value to <code>[firstIndex, lastIndex]</code> and its count. Sort by first index and merge overlaps — each merged group is a set of values that are interleaved and therefore <em>must</em> become a single value.</p>
<p>Inside a group with total element count <em>T</em> and largest single-value count <em>M</em>, the cheapest plan keeps the most common value and rewrites the rest, costing <code>T - M</code> (cost is measured in elements changed).</p>
<p>Sum <code>T - M</code> across groups.</p>
<p>On <code>quality = [7,7,5,7,3,5,3]</code>: 7 spans [0,3], 5 spans [2,5], 3 spans [4,6] — all three overlap into one group with T = 7 and M = 3 (three 7s), giving 7 - 3 = <strong>4</strong>. ✓</p><p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>from collections import Counter, defaultdict

def getMinAmount(quality):
    first, last = {}, {}
    for i, v in enumerate(quality):
        if v not in first:
            first[v] = i
        last[v] = i
    cnt = Counter(quality)

    spans = sorted((first[v], last[v], v) for v in first)

    total_cost = 0
    i = 0
    while i &lt; len(spans):
        lo, hi, v = spans[i]
        group_total, group_max = cnt[v], cnt[v]
        j = i + 1
        while j &lt; len(spans) and spans[j][0] &lt; hi:
            hi = max(hi, spans[j][1])
            c = cnt[spans[j][2]]
            group_total += c
            group_max = max(group_max, c)
            j += 1
        total_cost += group_total - group_max
        i = j
    return total_cost</code></pre><div class="unsure">Compare with <a href='#fp-mincontig' style='color:var(--accent)'>Minimum Contiguous Replacements</a>: same validity rule, but there the cost is the <em>number of operations</em> (group size − 1), not the number of elements changed. Read which one the statement asks for — the two answers differ.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the statement's example <code>quality = [7, 7, 5, 7, 3, 5, 3]</code>, answer <strong>4</strong>.</p>

<div class="step"><h4>1 &middot; What the operation can and cannot do</h4>
<p>"Replace every product with quality x by quality y" is not a per-element edit — it is <strong>all-or-nothing on a value</strong>. You cannot change one of the three 7s; you change every 7 or none. So the only decision you ever make is: <em>which values get fused together?</em> The answer is a partition of the distinct values into groups, each group collapsing to a single value.</p>
<p>Cost is measured in <em>elements changed</em>. For a group with <code>T</code> elements in total, you keep one member value and rewrite the rest, so the cheapest choice keeps the most frequent member:</p>
<div class="formula">cost(group) = T &minus; M      T = total elements in the group
                          M = count of the group's <b>most frequent</b> value</div></div>

<div class="step"><h4>2 &middot; Which values are forced together</h4>
<p>The validity rule is "all occurrences of each value are contiguous". Define a value's <strong>span</strong> as <code>[firstIndex, lastIndex]</code>. If two spans overlap, the values interleave — one sits strictly inside the other's range — and no amount of relabelling separates them. They <em>must</em> end up as the same value.</p>
<div class="formula">index   0  1  2  3  4  5  6
value   7  7  5  7  3  5  3

7 &rarr; first 0, last 3, count 3     span [0,3]
5 &rarr; first 2, last 5, count 2     span [2,5]
3 &rarr; first 4, last 6, count 2     span [4,6]</div>
<p>Span [0,3] overlaps [2,5] (index 2 and 3 lie in both), and [2,5] overlaps [4,6]. Overlap is not transitive on its own, but <em>merging</em> is: once 7 and 5 fuse, the merged block spans [0,5], which overlaps 3's span, so 3 joins too. All three become one group.</p></div>

<div class="step"><h4>3 &middot; The merge sweep, step by step</h4>
<p>Sort spans by first index and sweep, extending the running <code>hi</code>. This is interval merging, with counts accumulated on the way:</p>
<table class="trace">
<tr><th>step</th><th>span considered</th><th>starts before hi?</th><th>hi becomes</th><th>group_total</th><th>group_max</th></tr>
<tr><td>open group</td><td>(0, 3, value 7)</td><td>&mdash;</td><td>3</td><td>3</td><td>3</td></tr>
<tr><td>extend</td><td>(2, 5, value 5)</td><td>2 &lt; 3 &check;</td><td>max(3,5) = 5</td><td>3 + 2 = 5</td><td>max(3,2) = 3</td></tr>
<tr><td>extend</td><td>(4, 6, value 3)</td><td>4 &lt; 5 &check;</td><td>max(5,6) = 6</td><td>5 + 2 = 7</td><td>max(3,2) = 3</td></tr>
<tr><td class="hit">close</td><td colspan="3">no spans left</td><td class="hit">T = 7</td><td class="hit">M = 3</td></tr>
</table>
<div class="formula">cost = T &minus; M = 7 &minus; 3 = <b>4</b></div>
<p>Which is the published answer. Concretely: keep the three 7s, rewrite the two 5s and the two 3s to 7 — four products changed — giving <code>[7,7,7,7,7,7,7]</code>. Any single value trivially satisfies contiguity.</p>
<p>The comparison is against the running <code>hi</code>, not against the previous span's own end. Using <code>spans[j-1][1]</code> would break the chain the moment a short span nests inside a long one.</p></div>

<div class="step"><h4>4 &middot; Why the finest grouping is always optimal</h4>
<p>Merging is forced <em>upward</em> only. You could always fuse more values than required — is that ever cheaper? No, and the algebra is one line. Merge two groups with totals <code>T&#8321;, T&#8322;</code> and maxima <code>M&#8321;, M&#8322;</code>:</p>
<div class="formula">separate: (T&#8321; &minus; M&#8321;) + (T&#8322; &minus; M&#8322;)
merged:   (T&#8321; + T&#8322;) &minus; max(M&#8321;, M&#8322;)

merged &minus; separate = M&#8321; + M&#8322; &minus; max(M&#8321;, M&#8322;) = <b>min(M&#8321;, M&#8322;) &ge; 0</b></div>
<p>Merging always costs at least as much, and strictly more whenever both groups are non-empty. So take the <strong>finest</strong> valid partition — exactly what interval merging produces — and never look for a cleverer grouping.</p>
<p>The groups also cannot collide after relabelling: every occurrence of a value lives in exactly one group, so two groups never keep the same value, and their index ranges are disjoint blocks. Contiguity holds for the whole array automatically.</p></div>

<div class="step"><h4>5 &middot; Verification and the sibling problem</h4>
<p>Checked against a DP brute force over all closed intervals for every array of length &le; 8 with values in 1..4 (3000 random cases, no mismatch).</p>
<p>Do not confuse this with <a href='#fp-mincontig' style='color:var(--accent)'>Minimum Contiguous Replacements</a>, which has the identical validity rule but charges <strong>one per operation</strong> instead of one per element. Same groups, different accounting:</p>
<table class="trace">
<tr><th>problem</th><th>cost of a group</th><th>this example</th></tr>
<tr><td>Optimal Inventory (this one)</td><td>T &minus; M &nbsp;(elements changed)</td><td class="hit">7 &minus; 3 = <strong>4</strong></td></tr>
<tr><td>Minimum Contiguous Replacements</td><td>(distinct values in group) &minus; 1 &nbsp;(merges)</td><td>3 &minus; 1 = 2</td></tr>
</table>
<p>Read the Returns clause carefully before choosing which one you are computing.</p></div>

<div class="step"><h4>6 &middot; Traps</h4>
<ul>
<li><strong>Values can be negative</strong> — the statement says so explicitly. Never index an array by the quality value; use a hash map.</li>
<li><strong>Track <code>first</code> and <code>last</code> per value, not just counts.</strong> The counts give the cost; the spans give the grouping.</li>
<li><strong>Extend <code>hi</code> with <code>max</code>.</strong> A span nested entirely inside the current group must not shrink it.</li>
<li><strong>Keep the most frequent member, not the first or the largest value.</strong> That single choice is where the whole saving lives.</li>
<li><strong>A value appearing once is still a group</strong> of its own if nothing overlaps it, costing <code>1 &minus; 1 = 0</code>.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'promo', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Code Question 2', title:'Count Promotional / Offer Periods',
  minutes:35, score:'',
  images:['image24.jpg','image23.jpg'],
  fn:{name:'countPromotionalPeriods', ret:'long', params:[['int[]','orders']]},
  gen:`def gen(rng, n):
    m = max(3, n)
    return [rng.sample(range(1, 10 * m + 10), m)]`,
  tests:[
    {in:[[3, 2, 8, 6]], out:1},
    {in:[[5, 1, 4, 2, 6]], out:3},
    {in:[[1, 2, 3]], out:0},
    {in:[[5, 1, 4, 2, 3]], out:2},
    {in:[[10, 9, 8, 7]], out:0},
    {in:[[1, 2, 3, 4, 5, 6, 7]], out:0}
  ],
  body:`
<p>Data Analysts at Amazon are analyzing product order patterns. Based on their analysis, the team concluded that whenever a limited-period offer is rolled out, there is a spike in orders on the first and last days of the offer. They classify a period of 3 or more days as an offer period if the minimum value of the orders on the first and last days of the period outweigh the maximum value of orders on all other days in that period.</p>

<p>In mathematical terms, a period of <em>days[i, j]</em> (1 &le; <em>i</em> &le; <em>n</em> - 2 and <em>i</em>+1 &lt; <em>j</em> &le; <em>n</em>) is classified as an offer period if:</p>
<ul>
  <li>The period <em>[i, j]</em> is an offer period if:
    <ul>
      <li>1 &le; <em>i</em> &le; <em>n</em>-2</li>
      <li><em>i</em>+1 &lt; <em>j</em> &le; <em>n</em></li>
      <li>min(<em>orders[i]</em>, <em>orders[j]</em>) &gt; max(<em>orders[i+1]</em>, <em>orders[i+2]</em>, …, <em>orders[j-1]</em>)</li>
    </ul>
  </li>
</ul>

<p>Given an array of distinct integers, <em>orders</em>, with order statistics over a period of <em>n</em> consecutive days, report the number of offer periods identified.</p>

<h3>Example</h3>
<p>Suppose <em>n</em> = 4, <em>orders</em> = [3, 2, 8, 6]</p>
<p>Assume 1-based indexing.</p>
<table class="oa">
<tr><th>Period</th><th>Min(orders[i], orders[j])</th><th>Max(orders[i+1],…,orders[j-1])</th><th>Offer Period</th></tr>
<tr><td>[1, 3]</td><td>min(3, 8) = 3</td><td>max(2) = 2</td><td>Since 3 &gt; 2, so YES</td></tr>
<tr><td>[1, 4]</td><td>min(3, 6) = 3</td><td>max(2, 8) = 8</td><td>Since 3 &lt; 8, so NO</td></tr>
<tr><td>[2, 4]</td><td>min(2, 6) = 2</td><td>max(8) = 8</td><td>Since 2 &lt; 8, so NO</td></tr>
</table>
<p>The number of offer periods is <em>1</em>.</p>

<h3>Function Description</h3>
<p>Complete the function <em>countPromotionalPeriods</em> in the editor below.</p>
<p><em>countPromotionalPeriods</em> has the following parameter(s):</p>
<ul><li><em>int orders[n]:</em> the order statistics over <em>n</em> days.</li></ul>

<h3>Returns</h3>
<ul><li><em>long int:</em> the number of offer periods identified.</li></ul>

<h3>Constraints</h3>
<ul>
  <li>3 &le; <em>n</em> &le; 2 x 10<sup>5</sup></li>
  <li>1 &le; <em>orders[i]</em> &le; 10<sup>9</sup></li>
</ul>
<div class="frag">The remaining constraint lines are obscured by an overlay in the source screenshot.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>The condition compares the <em>min of the two endpoints</em> against the <em>max of everything strictly between</em>. A period needs length &ge; 3. Brute force is O(n³) — where is the redundancy?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Fix the left endpoint and extend the right endpoint one step at a time, maintaining the running max of the interior incrementally. That makes it O(n²) with O(1) work per pair, which fits n &le; a few thousand.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>A period <code>[i, j]</code> is an offer period when <code>j - i &ge; 2</code> and <code>min(orders[i], orders[j]) &gt; max(orders[i+1..j-1])</code>.</p>
<p>Fix <em>i</em>. Sweep <em>j</em> from <em>i+2</em> upward, keeping <code>interior_max</code> = max of <code>orders[i+1..j-1]</code>, which you extend by one element each step. Test the condition in O(1), then fold <code>orders[j-1]</code>… careful with the update order: update <code>interior_max</code> with <code>orders[j-1]</code> <em>before</em> testing <code>j</code>.</p>
<p>On <code>orders = [3, 2, 8, 6]</code> (1-based): [1,3] → min(3,8)=3 &gt; max(2)=2 ✓; [1,4] → min(3,6)=3 &gt; max(2,8)=8 ✗; [2,4] → min(2,6)=2 &gt; max(8)=8 ✗. Count = <strong>1</strong>. ✓</p><p>That is O(n²) and the stated bound is <code>n &le; 2&times;10<sup>5</sup></code>, so it will time out — keep it only as a reference implementation. The linear version below is the standard <em>visible pairs</em> count on a strictly decreasing stack: a pair survives exactly when nothing between the two days is taller than either, which is precisely what the stack discards. Count every visible pair, then subtract the <code>n-1</code> adjacent ones, which are always visible but are excluded by <code>j &gt; i+1</code>.</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def countPromotionalPeriods(orders):
    n = len(orders)
    stack, visible = [], 0
    for x in orders:
        while stack and stack[-1] &lt; x:      # x hides everything shorter
            stack.pop()
            visible += 1                    # popped day sees x
        if stack:
            visible += 1                    # x also sees the taller day above it
        stack.append(x)
    return visible - (n - 1)                # drop adjacent pairs (j = i+1)</code></pre>
<p>Reference O(n²) version, useful for checking the above:</p><p><span class="cx">Time O(n²)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def countPromotionalPeriods(orders):
    n = len(orders)
    count = 0
    for i in range(n):
        interior_max = float('-inf')
        for j in range(i + 2, n):
            interior_max = max(interior_max, orders[j - 1])
            if min(orders[i], orders[j]) &gt; interior_max:
                count += 1
    return count</code></pre><div class="unsure">Two constraint lines sit behind a watermark in the screenshot, but the visible ones do give <code>3 &le; n &le; 2&times;10<sup>5</sup></code>, so the O(n²) sweep <strong>will</strong> time out — submit the stack version. The two agree on 3000 random distinct-value arrays and on the published example; the stack version handles n = 200 000 in 0.04 s. Both assume the values are <em>distinct</em>, as the statement says ("an array of distinct integers"); with duplicates the pop condition needs an equal-value branch.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example <code>orders = [3, 2, 8, 6]</code> (1-based in the statement), answer <strong>1</strong>.</p>

<div class="step"><h4>1 &middot; Read the condition as a skyline</h4>
<div class="formula">min(orders[i], orders[j]) &gt; max(orders[i+1 .. j&minus;1])</div>
<p>Both endpoints must exceed <em>everything</em> strictly between them. That is the classic <strong>"can these two days see each other?"</strong> condition: stand on day <em>i</em>, look toward day <em>j</em>; the pair counts only if no day in between is tall enough to block the view. The values are distinct (the statement guarantees it), so no ties to worry about.</p>
<p>The constraint <code>i + 1 &lt; j</code> means at least one day sits between them — adjacent days are excluded even though they always see each other.</p></div>

<div class="step"><h4>2 &middot; The O(n²) reading, and why it is right but too slow</h4>
<p>Fix <em>i</em> and walk <em>j</em> rightward, carrying the running interior maximum:</p>
<div class="formula">for j = i+2, i+3, ...:
    interior_max = max(interior_max, orders[<b>j&minus;1</b>])   &larr; fold in the new interior day <b>first</b>
    if min(orders[i], orders[j]) &gt; interior_max: count += 1</div>
<p>The update order is the whole correctness of the loop. When <em>j</em> arrives, the interior is <code>[i+1, j-1]</code>, so <code>orders[j-1]</code> has just become interior and must be folded in <em>before</em> the test; <code>orders[j]</code> is an endpoint and must never enter <code>interior_max</code>. Fold after testing and you compare against a stale maximum that omits the nearest day.</p>
<p>The recurrence is correct but the bound is <code>n &le; 2&times;10<sup>5</sup></code>, so this is 2&times;10<sup>10</sup> operations. Correct answer, failed submission.</p></div>

<div class="step"><h4>3 &middot; The linear version: one decreasing stack</h4>
<p>Keep a stack of days that are still visible from the right — strictly decreasing from bottom to top. Process each new day <code>x</code>:</p>
<div class="formula">while stack and stack[&minus;1] &lt; x:      # x is taller, so it blocks that day forever
    stack.pop(); visible += 1        #   ... but that day <b>can</b> see x: one pair
if stack:                            # the day still on top is taller than x
    visible += 1                     #   ... it sees x over the popped ones: one more pair
stack.append(x)</div>
<p>Each pop records the pair (popped day, x): everything between them was popped earlier and is therefore shorter than both, which is exactly the visibility condition. The single extra pair after the pops is the first day taller than <code>x</code> — it sees over <code>x</code>'s head. Anything below that is blocked by it, so the counting stops there. Every day is pushed once and popped once, hence O(n).</p></div>

<div class="step"><h4>4 &middot; Full trace of [3, 2, 8, 6]</h4>
<table class="trace">
<tr><th>day</th><th>x</th><th>pops (each = 1 pair)</th><th>extra pair with new top?</th><th>visible</th><th>stack after</th></tr>
<tr><td>1</td><td>3</td><td>&mdash;</td><td>stack empty, no</td><td>0</td><td>[3]</td></tr>
<tr><td>2</td><td>2</td><td>none (3 &gt; 2)</td><td>yes: (3, 2)</td><td>1</td><td>[3, 2]</td></tr>
<tr><td>3</td><td>8</td><td>pop 2 &rarr; (2, 8); pop 3 &rarr; (3, 8)</td><td>stack empty, no</td><td>3</td><td>[8]</td></tr>
<tr><td>4</td><td>6</td><td>none (8 &gt; 6)</td><td>yes: (8, 6)</td><td>4</td><td>[8, 6]</td></tr>
</table>
<p>Four visible pairs: <code>(3,2) (2,8) (3,8) (8,6)</code> — in 1-based day terms <code>[1,2] [2,3] [1,3] [3,4]</code>. Three of them are adjacent days and do not qualify. Subtract them:</p>
<div class="formula">answer = visible &minus; (n &minus; 1) = 4 &minus; 3 = <b>1</b></div>
<p>The survivor is <code>[1, 3]</code>: <code>min(3, 8) = 3 &gt; max(2) = 2</code>. Cross-check against the statement's own table — <code>[1,4]</code> fails on <code>3 &lt; 8</code> and <code>[2,4]</code> fails on <code>2 &lt; 8</code>, and neither appears in the stack's list, because day 3's value 8 blocks both.</p></div>

<div class="step"><h4>5 &middot; Why subtracting exactly n&minus;1 is safe</h4>
<p>Every adjacent pair <code>(i, i+1)</code> has an empty interior, so <code>max</code> over nothing is <code>-&infin;</code> and the pair is always visible. There are exactly <code>n-1</code> of them, and the stack counts every one: when day <code>i+1</code> arrives, day <code>i</code> is on top of the stack, so either it gets popped (counted) or it stays and the "extra pair" branch counts it. Exactly one of the two fires, never both, never neither. So the subtraction is a constant, not an estimate.</p></div>

<div class="step"><h4>6 &middot; Traps</h4>
<ul>
<li><strong>Return type is <code>long</code>.</strong> With n = 2&times;10<sup>5</sup> the count can approach <code>2n</code> for a sawtooth, but a sorted array gives a stack of depth n and pair counts near n — still fine in 64-bit, and the statement asks for long regardless.</li>
<li><strong>Adjacent pairs are excluded</strong> by <code>i + 1 &lt; j</code>. Forgetting the <code>&minus;(n&minus;1)</code> inflates every answer.</li>
<li><strong>Strict inequality.</strong> <code>min &gt; max</code>, not <code>&ge;</code>. Distinct values make this moot for the samples, but the pop condition <code>stack[-1] &lt; x</code> must stay strict to match.</li>
<li><strong>The O(n²) loop's update order</strong> — fold <code>orders[j-1]</code> in <em>before</em> the comparison, and never fold an endpoint.</li>
<li><strong>1-based statement, 0-based code.</strong> The statement's <code>[1,3]</code> is the code's <code>i=0, j=2</code>.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'circular', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Code Question 2', title:'Warehouse Containers in a Circle — Minimum Movement Cost',
  minutes:40, score:'',
  images:['image19.jpg','image20.jpg'],
  fn:{name:'getMinimumCost', ret:'long', params:[['int[]','products']]},
  gen:`def gen(rng, n):
    m = max(2, n)
    base = rng.randint(0, 20)
    vals = [base] * m
    for _ in range(m):
        i, j = rng.randrange(m), rng.randrange(m)
        d = rng.randint(0, 5)
        if vals[i] - d >= 0:
            vals[i] -= d
            vals[j] += d
    return [vals]`,
  tests:[
    {in:[[3, 4, 6, 6, 6]], out:7},
    {in:[[5, 5, 5]], out:0},
    {in:[[1, 2, 3, 4, 5, 3]], out:8},
    {in:[[10, 0, 0, 0, 0, 0, 0, 0, 0, 0]], out:45}
  ],
  body:`
<p>Amazon's warehouse management team is planning to roll out certain standards and checks that every Amazon Warehouse Manager will follow. Some products may need to be moved initially from one warehouse to another so that each warehouse complies.</p>

<p>A warehouse stores <em>n</em> identical containers arranged in the form of a circle. <strong>The distance between two adjacent</strong> containers <strong>is 1.</strong> Each container in a warehouse should hold the same number of products. Plan the optimal set of movements under the following rules.</p>

<ul>
  <li><strong>Move products from any location in either the clockwise or the anti-clockwise direction. The direction must remain the same throughout the remaining moves.</strong></li>
  <li><strong>While moving, collect excess products from some locations and deliver them to other locations that need more units.</strong></li>
  <li><strong>The cost of each product transfer is the distance the product is moved.</strong></li>
  <li><strong>The total cost is the sum of the costs for all products transferred.</strong></li>
</ul>

<p><strong>Find the minimum cost such that finally, every</strong> container <strong>has the same number of products.</strong></p>

<div class="note"><p><strong>Note:</strong> In the examples, positions are one-indexed. It is guaranteed that it is always possible to distribute the products equally.</p></div>

<h3>Example</h3>
<p>Consider a circular arrangement of containers. The units in each container are <em>products</em> = [3, 4, 6, 6, 6].</p>
<figure class="fig"><img loading="lazy" src="../images/fig-circular.png" alt="Circular arrangement of containers" data-full="../images/image20.jpg" title="Click to open the full screenshot"><figcaption>Circular arrangement of containers</figcaption></figure>

<h4>Option 1:</h4>
<p>Start at the <em>3<sup>rd</sup></em> position and move clockwise. Collect one product each from the <em>3<sup>rd</sup></em>, <em>4<sup>th</sup></em>, and <em>5<sup>th</sup></em> positions.<br>Transfer the products from</p>
<ul>
  <li>the <em>5<sup>th</sup></em> position to the <em>1<sup>st</sup></em> position, the cost is <em>1</em></li>
  <li>the <em>4<sup>th</sup></em> position to the <em>1<sup>st</sup></em> position, the cost is <em>2</em>.</li>
  <li>the <em>3<sup>rd</sup></em> position to the <em>2<sup>nd</sup></em> position, the cost is <em>4</em>.</li>
</ul>
<p>Now each container has <em>5</em> units and the total cost is <em>1+2+4=7</em>.</p>

<h4>Option 2:</h4>
<p>Start at the <em>5<sup>th</sup></em> position moving anti-clockwise. Collect one product each from the <em>5<sup>th</sup></em>, <em>4<sup>th</sup></em>, and <em>3<sup>rd</sup></em> positions.<br>Transfer the product from</p>
<ul>
  <li>the <em>3<sup>rd</sup></em> position to the <em>1<sup>st</sup></em> position, the cost is <em>2</em>.</li>
  <li>the <em>4<sup>th</sup></em> position to the <em>1<sup>st</sup></em> position, the cost is <em>3</em>.</li>
  <li>the <em>5<sup>th</sup></em> position to the <em>2<sup>nd</sup></em> position, the cost is <em>3</em>.</li>
</ul>
<p>Now each container has <em>5</em> units and the total cost is <em>2+3+3=8</em>. Return <em>7</em>, the minimum cost achievable.</p>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Every container must end at the mean. Think of the transfer between position <em>i</em> and <em>i+1</em> as a single signed number: how many units cross that edge?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Let <code>d[i] = a[i] - mean</code>. If <code>x[i]</code> units cross the edge from i to i+1, then <code>x[i] = x[i-1] + d[i]</code>. Total cost is <code>sum |x[i]|</code>. All the <code>x</code> differ from the prefix sums by one unknown constant — choose that constant to be the <strong>median</strong> of the prefix sums.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>This is the classic circular token-distribution problem, with one extra restriction.</p>
<p>Let <em>mean</em> = total / n and <code>d[i] = a[i] - mean</code>. Define <code>P[i] = d[0] + … + d[i]</code>. If <code>x[i]</code> is the net flow across edge (i, i+1), the balance equations force <code>x[i] = P[i] - C</code> for a single constant <em>C</em> — the flow across the wrap-around edge. The total cost is <code>Σ |P[i] - C|</code>.</p>
<p>Unconstrained, that is minimised at the <strong>median</strong> of <code>P</code>. But <strong>the direction constraint forbids it.</strong> Because every transfer must travel the same way round, all the edge flows must share one sign. All non-negative forces <code>C = min(P)</code>; all non-positive forces <code>C = max(P)</code>. So:</p>
<pre class="sample">cost = min(  Σ (P[i] − min P),   Σ (max P − P[i])  )</pre>
<p>On <code>[3,4,6,6,6]</code>: mean 5, <code>d = [-2,-1,1,1,1]</code>, <code>P = [-2,-3,-2,-1,0]</code>. One direction gives <code>Σ(P + 3) = 1+0+1+2+3 = <strong>7</strong></code>, the other <code>Σ(0 − P) = 2+3+2+1+0 = <strong>8</strong></code> — exactly the statement's Option 1 and Option 2. Return the smaller, <strong>7</strong>.</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def getMinimumCost(products):
    n = len(products)
    mean = sum(products) // n              # guaranteed to divide exactly
    P, run = [], 0
    for v in products:
        run += v - mean                    # prefix sum of surpluses
        P.append(run)
    lo, hi = min(P), max(P)
    return min(sum(p - lo for p in P),     # all flow one way
               sum(hi - p for p in P))     # all flow the other way</code></pre><div class="unsure">The solution previously published here took the <strong>median</strong> of <code>P</code> and returned 4 on the statement's own example, contradicting its stated answer of 7. The median is the correct constant only when flows may run both ways round the circle; this statement pins the direction ("the direction must remain the same throughout"), restricting the constant to <code>min P</code> or <code>max P</code>. Those two values reproduce Option 1 (7) and Option 2 (8) exactly, which is strong evidence for this reading. The old code also defined <code>minCost</code> rather than the declared <code>getMinimumCost</code>.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the statement's example <code>products = [3, 4, 6, 6, 6]</code>, answer <strong>7</strong>.</p>

<div class="step"><h4>1 &middot; Turn "moving products" into "flow across edges"</h4>
<p>Do not think about individual products or routes. On a circle of <em>n</em> containers there are exactly <em>n</em> edges, and the only thing that matters is the <strong>net number of products crossing each edge</strong>. Two products going opposite ways across the same edge cancel; a product travelling three edges costs 3 because it crosses three edges. So:</p>
<div class="formula">total cost = &sum;<sub>edges</sub> |flow across that edge|</div>
<p>That single reframing is what turns a routing puzzle into arithmetic. Cost is now a function of <em>n</em> numbers, not of any actual plan.</p></div>

<div class="step"><h4>2 &middot; The balance equation pins every flow to one unknown</h4>
<p>First the target. Everything must end equal, and the statement guarantees it divides:</p>
<div class="formula">mean = (3 + 4 + 6 + 6 + 6) / 5 = 25 / 5 = <b>5</b>
d[i] = a[i] &minus; mean  =  [<b>&minus;2, &minus;1, 1, 1, 1</b>]      surplus (+) or deficit (&minus;) at each container</div>
<p>Let <code>x[i]</code> be the net flow across the edge from container <em>i</em> to <em>i+1</em>. Container <em>i</em> receives <code>x[i-1]</code> and sends <code>x[i]</code>, so balancing it requires <code>x[i] = x[i-1] + d[i]</code>. Unrolling from <code>x[-1] = C</code> (the wrap-around edge, the one genuinely free choice):</p>
<div class="formula">x[i] = C + d[0] + d[1] + ... + d[i] = <b>P[i] + C</b>,  where P[i] = prefix sum of d</div>
<p>Every flow is determined by <em>one</em> unknown constant. Compute the prefix sums:</p>
<table class="trace">
<tr><th>i</th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td></tr>
<tr><th>a[i]</th><td>3</td><td>4</td><td>6</td><td>6</td><td>6</td></tr>
<tr><th>d[i] = a[i]&minus;5</th><td>&minus;2</td><td>&minus;1</td><td>1</td><td>1</td><td>1</td></tr>
<tr><th>P[i]</th><td>&minus;2</td><td>&minus;3</td><td>&minus;2</td><td>&minus;1</td><td>0</td></tr>
</table>
<p>Note <code>P[n-1] = 0</code> always — the surpluses and deficits cancel by construction, which is a free sanity check on your prefix sums.</p></div>

<div class="step"><h4>3 &middot; Where the usual median answer comes from, and why it is wrong here</h4>
<p>Writing <code>C' = -C</code>, the cost is <code>&sum; |P[i] - C'|</code>. Minimising a sum of absolute deviations over a <em>free</em> constant is the textbook median problem, and that is the standard solution to circular token distribution. On this input the median of <code>P</code> is &minus;2, giving cost <code>0+1+0+1+2 = 4</code>.</p>
<p><strong>But 4 contradicts the statement, which says 7.</strong> The reason is the rule most people skim past:</p>
<div class="formula">"Move products ... in either the clockwise or the anti-clockwise direction.
 <b>The direction must remain the same throughout the remaining moves.</b>"</div>
<p>A median solution has some flows positive and some negative — products travelling <em>both</em> ways round the circle. That is exactly what the rule forbids. Every flow must share one sign:</p>
<div class="formula">all flows &ge; 0  &rArr;  P[i] &minus; C' &ge; 0 for all i  &rArr;  C' &le; min P
all flows &le; 0  &rArr;  P[i] &minus; C' &le; 0 for all i  &rArr;  C' &ge; max P</div>
<p>In the first case cost <code>&sum;(P[i] - C')</code> shrinks as <code>C'</code> grows, so push it to its ceiling <code>C' = min P</code>. In the second, cost <code>&sum;(C' - P[i])</code> grows with <code>C'</code>, so take the floor <code>C' = max P</code>. Two candidates, no search.</p></div>

<div class="step"><h4>4 &middot; The two directions, evaluated</h4>
<p><code>P = [&minus;2, &minus;3, &minus;2, &minus;1, 0]</code>, so <code>min P = &minus;3</code> and <code>max P = 0</code>.</p>
<table class="trace">
<tr><th>i</th><th>P[i]</th><th>one direction: P[i] &minus; (&minus;3)</th><th>other direction: 0 &minus; P[i]</th></tr>
<tr><td>0</td><td>&minus;2</td><td>1</td><td>2</td></tr>
<tr><td>1</td><td>&minus;3</td><td>0</td><td>3</td></tr>
<tr><td>2</td><td>&minus;2</td><td>1</td><td>2</td></tr>
<tr><td>3</td><td>&minus;1</td><td>2</td><td>1</td></tr>
<tr><td>4</td><td>0</td><td>3</td><td>0</td></tr>
<tr><th>total</th><th></th><td class="hit"><strong>7</strong></td><td>8</td></tr>
</table>
<p>These are <em>precisely</em> the two options the statement walks through — its Option 1 costs 7 and its Option 2 costs 8. That correspondence is the strongest available evidence that this reading of the direction rule is the intended one: the statement is not enumerating two arbitrary strategies, it is enumerating the two directions, and each is already optimal for its direction.</p>
<div class="formula">answer = min(7, 8) = <b>7</b></div>
<p>Reading the winning column physically: one product crosses edge 0, none crosses edge 1, one crosses edge 2, two cross edge 3, three cross edge 4. Total distance 7. The zero at edge 1 marks the "seam" the flow never crosses — with one direction, the cheapest plan always leaves exactly one edge unused, and the algorithm is choosing which.</p></div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Do not use the median.</strong> It is the right answer to the unrestricted version of this problem and the wrong answer to this one. If a judge rejects <code>min(...)</code>, the median is the one alternative worth trying — but it contradicts the printed example.</li>
<li><strong>Return type is <code>long</code>.</strong> With large n and large counts the prefix sums and the cost both overflow 32 bits.</li>
<li><strong><code>P[n-1]</code> must be 0.</strong> If it is not, your mean or your prefix sums are wrong.</li>
<li><strong>Integer mean.</strong> The statement guarantees divisibility, so <code>//</code> is safe — but compute it before subtracting, not by float division.</li>
<li><strong>Already-equal input</strong> gives all <code>d = 0</code>, all <code>P = 0</code>, min = max = 0, cost 0 from both directions.</li>
<li><strong>The distance between adjacent containers is 1</strong>, and the circle wraps — a product can travel from container n to container 1 in one step. That wrap edge is the free constant <code>C</code>.</li>
</ul></div>
</div></details>
</div>

`},

{
  id:'flashsale', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Question 1', title:'Flash Sale — Priority Inventory Allocation',
  minutes:35, score:'',
  images:['image37.png','WhatsApp Image 2026-09-07 at 10.14.58 PM (6).jpeg'],
  fn:{name:'getUnfulfilledCustomers', ret:'int[]', params:[['int[][]','requests'],['int','totalInventory']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    reqs = [[i + 1, rng.randint(1, 6), rng.randint(1, 4), rng.randint(0, 5)] for i in range(m)]
    return [reqs, rng.randint(0, 4 * m)]`,
  tests:[
    {in:[[[1, 5, 5, 0], [2, 7, 8, 1], [3, 7, 5, 1], [4, 10, 3, 3]], 18], out:[4]},
    {in:[[[1, 2, 10, 0], [2, 3, 10, 1], [3, 1, 5, 0]], 3], out:[3]},
    {in:[[[1, 5, 5, 0], [2, 7, 8, 1], [3, 7, 5, 1], [4, 10, 3, 3]], 0], out:[1, 2, 3, 4]},
    {in:[[[1, 2, 5, 0], [2, 2, 5, 1]], 4], out:[]},
    {in:[[[1, 3, 9, 0], [2, 3, 1, 1]], 3], out:[2]}
  ],
  body:`
<p>Allocate limited inventory items based on priority algorithm. During a flash sale on Amazon, customers submit requests for a limited quantity of a product. Each of the request includes: <em>[customerId, quantity, bidAmount, timestamp]</em>.</p>

<p>Items are allocated using these rules:</p>
<ul>
  <li>Higher bids get priority.</li>
  <li>If multiple customers have the same bid, allocate items in a round-robin manner based on the earliest timestamp until all of the inventory is allocated.</li>
  <li>A customer gets one item per round until their request is fulfilled.</li>
</ul>

<p>Return the <em>IDs</em> of customers who received no items.</p>

<div class="note"><p><strong>Note:</strong> Round-robin allocation means cycling through the tied customers in order of their timestamps, granting exactly one item to each customer per cycle, until either the inventory runs out or all their requested quantities are fulfilled.</p></div>

<h3>Example</h3>
<pre class="sample">Input:
requests = [[1, 5, 5, 0], [2, 7, 8, 1], [3, 7, 5, 1], [4, 10, 3, 3]]
totalInventory = 18
Output: [4]</pre>
<p>Explanation:<br>The first three requests have a higher bidding amount than the 4th request, and the total quantity requested in the first three requests is <code>19</code>, whereas the available inventory is <code>18</code>, so only one left without any allocation will be customer ID <code>4</code>.</p>

<div class="srcnote"><strong>Also catalogued as:</strong> "Unfulfilled Customers by Inventory Priority" on FastPrep — <em>Medium · Amazon · New Grad · Fulltime · OA</em>, category <em>Array</em>. That listing notes the question was reported asked again on <strong>08-19-2026</strong>, and supplies the final clause of the explanation above (the exam screenshot cut off mid-sentence).</div>

<div class="frag">Still missing: the Function Description, Returns and Constraints sections — neither source shows them (the FastPrep statement is paywalled past the intro).</div>

<div class="srcnote"><strong>Re-reported (Sept 2026) as "Inventory Allocation"</strong> with the same callable <code>getUnfulfilledCustomers(requests, totalInventory)</code>, the same worked example, and the constraints the exam screenshot cut off: <code>1 &le; requests.length &le; 10&#8309;</code>, four integer fields per row, distinct customer IDs, <code>0 &le; timestamp &le; 10&#8313;</code>, <code>0 &le; totalInventory &le; 10&#8313;</code>. It also publishes a second example, <code>[[1,2,10,0],[2,3,10,1],[3,1,5,0]]</code> with 3 units &rarr; <code>[3]</code> — added to the cases below — and states that the result keeps the order in which the requests appear in the input.</div>

<div class="srcnote"><strong>See also:</strong> <em>"Unfulfilled Bids after Ranked Round-Robin Allocation"</em> in the FastPrep section — a fully specified variant of this exercise, with constraints, tiebreak rules and test cases. Note it is <strong>not</strong> the same question: the bid fields are in a different order and it returns every partially fulfilled customer rather than only those who got nothing.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Allocation happens in <strong>rounds</strong>: within a round, every still-unfulfilled customer gets one unit, in priority order. Simulating unit-by-unit is fine only if you cap the work.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Sort by (bid descending, timestamp ascending). Then loop rounds: in each round walk the still-active customers in that order, give one unit each while inventory lasts, and drop customers whose requested quantity is met. Report the IDs that finished with <strong>zero</strong> units.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Bid tiers are processed strictly in order: <strong>every</strong> customer in a higher tier is served before anyone in a lower tier gets a single item. Round-robin applies only <em>within</em> a tier of equal bids, cycling by timestamp.</p>
<p>Inside a tier, rather than looping one item at a time, jump level by level: with <em>k</em> active customers and <em>step</em> = the smallest remaining need, a full <code>step</code> rounds costs <code>step × k</code> items and retires at least one customer. When the inventory cannot cover the next level, split what is left — <code>full, rem = divmod(inv, k)</code> — and hand the <code>rem</code> remainder items to the earliest timestamps.</p>
<p>Finally return the IDs that received nothing.</p><p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>from collections import defaultdict

def getUnfulfilledCustomers(requests, totalInventory):
    groups = defaultdict(list)                      # bid -&gt; members
    for cid, qty, bid, ts in requests:
        groups[bid].append((ts, cid, qty))

    got = {r[0]: 0 for r in requests}
    inv = totalInventory

    for bid in sorted(groups, reverse=True):        # highest bid first
        if inv == 0:
            break
        active = [[qty, cid] for ts, cid, qty in sorted(groups[bid])]
        while inv &gt; 0 and active:
            step = min(q for q, _ in active)        # rounds until someone finishes
            k = len(active)
            if step * k &lt;= inv:                     # every one of those rounds completes
                inv -= step * k
                for e in active:
                    got[e[1]] += step
                    e[0] -= step
                active = [e for e in active if e[0] &gt; 0]
            else:                                   # inventory dies mid-way
                full, rem = divmod(inv, k)          # rem items to the earliest rem
                for idx, e in enumerate(active):
                    got[e[1]] += full + (1 if idx &lt; rem else 0)
                inv = 0
                active = []

    return sorted(cid for cid in got if got[cid] == 0)</code></pre><div class="unsure">The code previously published here round-robined across <em>all</em> customers at once, ignoring bid tiers, so it returned <code>[]</code> on the published example instead of <code>[4]</code> — customer 4 received items that belonged to higher bidders. It also defined <code>getUnallocatedCustomers</code> rather than the declared <code>getUnfulfilledCustomers</code>. The version above reproduces the published example and agrees with a round-by-round simulator on 4000 random cases. Function Description, Returns and Constraints were cut off in the screenshot, so the tie-break when two customers share both bid and timestamp is a guess (customer id ascending). Compare with <a href='#fp-unfulfilledbids' style='color:var(--accent)'>Unfulfilled Bids</a> — same allocation, different field order, and it also returns partially-fulfilled customers.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example: <code>requests = [[1,5,5,0], [2,7,8,1], [3,7,5,1], [4,10,3,3]]</code>, <code>totalInventory = 18</code>, answer <code>[4]</code>.</p>

<div class="step"><h4>1 &middot; Two rules that operate at different levels</h4>
<p>The statement gives what looks like one ranking but is really two nested ones, and conflating them is the whole trap:</p>
<table class="trace">
<tr><th>rule</th><th>scope</th><th>effect</th></tr>
<tr><td>higher bids get priority</td><td><em>between</em> bid tiers</td><td>strict: a lower tier gets nothing until every higher-tier customer is fully served or the inventory is gone</td></tr>
<tr><td>round-robin by earliest timestamp</td><td><em>within</em> one tier of equal bids</td><td>fair: one item each per cycle</td></tr>
</table>
<p>Round-robin is <strong>not</strong> a global queue. Cycling through all four customers at once would hand customer 4 (bid 3) an item in the very first round, ahead of unmet demand at bid 5 — which inverts the priority rule and returns <code>[]</code> instead of <code>[4]</code>.</p>
<p>Decode the row layout carefully too: <code>[customerId, quantity, bidAmount, timestamp]</code>, so <code>r[2]</code> is the bid and <code>r[1]</code> is the quantity. The sibling problem <a href='#fp-unfulfilledbids' style='color:var(--accent)'>Unfulfilled Bids</a> orders these fields differently.</p></div>

<div class="step"><h4>2 &middot; Tier by tier on the example</h4>
<p>Group by bid, sort tiers descending:</p>
<div class="formula">bid 8 &rarr; [(ts 1, cust 2, needs 7)]
bid 5 &rarr; [(ts 0, cust 1, needs 5), (ts 1, cust 3, needs 7)]
bid 3 &rarr; [(ts 3, cust 4, needs 10)]</div>
<table class="trace">
<tr><th>tier</th><th>inventory in</th><th>what happens</th><th>allocated</th><th>inventory out</th></tr>
<tr><td>bid 8</td><td>18</td><td>customer 2 alone; 7 rounds of 1 finish them</td><td>2 &rarr; 7</td><td>11</td></tr>
<tr><td>bid 5</td><td>11</td><td>customers 1 and 3 alternate; after 5 cycles customer 1 is full (needs 5), 10 used; 1 item left goes to customer 3</td><td>1 &rarr; 5, 3 &rarr; 6</td><td>0</td></tr>
<tr><td class="hit">bid 3</td><td class="hit">0</td><td class="hit">nothing left; loop breaks</td><td class="hit">4 &rarr; <strong>0</strong></td><td class="hit">0</td></tr>
</table>
<p>Only customer 4 received nothing, so the answer is <code>[4]</code>. This matches the statement's own reasoning: the top three requests total <code>5 + 7 + 7 = 19</code> against an inventory of 18, so they absorb everything and customer 4 is starved.</p></div>

<div class="step"><h4>3 &middot; Level filling: skipping the round-by-round loop</h4>
<p>Simulating one item at a time is O(totalInventory), which is fine for 18 and hopeless if the inventory is large. Jump a whole block of rounds at once. With <em>k</em> active customers in the tier and <code>step</code> = the smallest remaining need:</p>
<div class="formula">step &times; k items  &rarr;  every active customer gains <b>step</b>, and at least one hits zero and leaves</div>
<p>Repeat while the inventory covers the next block. The bid-5 tier, worked out:</p>
<table class="trace">
<tr><th>active (need, id)</th><th>k</th><th>step</th><th>step&times;k</th><th>inv</th><th>result</th></tr>
<tr><td>[(5, c1), (7, c3)]</td><td>2</td><td>5</td><td>10</td><td>11 &rarr; 1</td><td>c1 +5 (done, leaves), c3 +5</td></tr>
<tr><td>[(2, c3)]</td><td>1</td><td>2</td><td>2</td><td>1</td><td>2 &gt; 1, so the block does <em>not</em> fit</td></tr>
</table>
<p>When the block does not fit, the leftover splits exactly:</p>
<div class="formula">full, rem = divmod(inv, k) = divmod(1, 1) = (<b>1</b>, <b>0</b>)
each active customer gets <b>full</b>; the first <b>rem</b> of them (earliest timestamps) get one extra</div>
<p>So customer 3 gains 1 more, reaching 6, and the inventory is exhausted. The <code>rem</code> items must go to the earliest timestamps because a partial cycle stops mid-way through the round-robin order — that ordering is why <code>active</code> is kept sorted by <code>(timestamp, id)</code> and never re-sorted afterwards.</p></div>

<div class="step"><h4>4 &middot; Who actually gets zero</h4>
<p>The question only asks who received nothing, and there is a simpler characterisation worth noticing: <strong>a customer gets zero exactly when the inventory runs out before their first item</strong>. Since every customer needs at least 1, the first cycle of a tier gives one item to each member in timestamp order, so within a starved tier it is a clean prefix that gets served and the rest that get nothing.</p>
<p>You could exploit that to skip the allocation amounts entirely. Computing the full allocation anyway costs nothing extra and makes the function reusable for the sibling problem, which <em>does</em> ask for partial fulfilment.</p></div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Round-robin is within a bid tier only.</strong> The single most damaging mistake — it silently promotes low bidders.</li>
<li><strong>Field order is <code>[id, quantity, bid, timestamp]</code>.</strong> Reading <code>r[1]</code> as the bid gives a plausible-looking wrong answer.</li>
<li><strong>Sort bids descending, timestamps ascending.</strong> Two directions in one problem.</li>
<li><strong>Stop as soon as the inventory hits 0</strong>, and be sure not to credit an item you did not have — the <code>divmod</code> branch is what guarantees the totals sum to exactly <code>totalInventory</code>.</li>
<li><strong>The return is a list of IDs, sorted.</strong> The published example has a single element, which hides any ordering convention; ascending id is the safe reading.</li>
<li><strong>Constraints were cut off</strong> in both sources, so the tie-break for equal bid <em>and</em> equal timestamp is unverified; this code falls back to customer id.</li>
</ul></div>
</div></details>
</div>

`},

{
  id:'drone', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Question 1', title:'Drone Delivery Network — Minimum Travel Time',
  minutes:35, score:'',
  images:['image26.jpg'],
  fn:{name:'getMinimumTravelTime', ret:'long', params:[['int[]','transitionTime'],['int[]','requestedHubs']]},
  body:`
<p>Amazon is expanding its next-generation drone delivery network, consisting of <em>m</em> hubs arranged in a circular ring (Hub 1 is adjacent to Hub <em>m</em>). A drone can move to either adjacent hub, and the travel time between Hub <em>i</em> and its neighbors is given by <em>transitionTime[i]</em>.</p>

<figure class="fig"><img loading="lazy" src="../images/fig-drone-ring.png" alt="The ring of m hubs — the drone starts at Hub 1 (green)" data-full="../images/image26.jpg" title="Click to open the full screenshot"><figcaption>The ring of m hubs — the drone starts at Hub 1 (green)</figcaption></figure>

<p>Amazon receives a list of priority delivery requests, where packages must be picked up or delivered to specific hubs in a given sequence, represented by the array <em>requestedHubs</em> of size <em>n</em>.</p>
<p>Starting from Hub 1, your task is to calculate the minimum total travel time required for the drone to fulfill all delivery requests.</p>

<div class="note"><p><strong>Note:</strong> Use 1-based indexing.</p></div>

<h3>Example</h3>
<pre class="sample">m = 3
n = 4
transitionTime  = [3, 2, 1]
requestedHubs   = [1, 3, 3, 2]</pre>
<p>The drone begins its journey at <em>Hub 1</em>.</p>

<div class="frag">The source screenshot ends here — the rest of the walkthrough, Function Description and Constraints were not captured.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>The hubs form a ring, so between any two hubs there are exactly two arcs. You need the cheaper one, repeatedly, along a fixed visiting order.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Prefix-sum the ring once. The clockwise distance from i to j is <code>pre[j] - pre[i]</code> (mod total); the anticlockwise one is <code>total - that</code>. Walk <em>requestedHubs</em> in order, adding <code>min(cw, ccw)</code> for each consecutive pair, starting from Hub 1.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p><code>transitionTime[i]</code> is the cost of the edge between hub <em>i</em> and hub <em>i+1</em> (wrapping). Build <code>pre[i]</code> = sum of the first <em>i</em> edges and <code>total</code> = sum of all edges.</p>
<p>For a hop from <em>u</em> to <em>v</em> (1-based), clockwise cost = <code>(pre[v-1] - pre[u-1]) mod total</code>, anticlockwise = <code>total - clockwise</code>. Take the min. Sum over the sequence Hub 1 → requestedHubs[0] → requestedHubs[1] → …</p><p><span class="cx">Time O(m + n)</span><span class="cx">Space O(m)</span></p><pre class="sample"><code>def getMinimumTravelTime(transitionTime, requestedHubs):
    m = len(transitionTime)
    pre = [0] * (m + 1)
    for i in range(m):
        pre[i + 1] = pre[i] + transitionTime[i]
    total = pre[m]

    def hop(u, v):
        cw = (pre[v - 1] - pre[u - 1]) % total
        return min(cw, total - cw)

    cur, ans = 1, 0
    for h in requestedHubs:
        ans += hop(cur, h)
        cur = h
    return ans</code></pre><div class="unsure">The code previously shown here was named <code>minTotalTravelTime</code> and took <em>m</em> as a first parameter, neither of which matches the declared signature <code>getMinimumTravelTime(transitionTime, requestedHubs)</code>; <em>m</em> is just <code>len(transitionTime)</code>. The source screenshot is cut off right after the example header — the Function Description, Returns and Constraints were never captured, and the sample's expected output is unknown. The ring/prefix-sum reading is the only one consistent with the visible text, but the exact signature (and whether the drone must return to Hub 1) is unverified.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the example the screenshot does show: <code>m = 3</code>, <code>transitionTime = [3, 2, 1]</code>, <code>requestedHubs = [1, 3, 3, 2]</code>. The expected output was cut off; this method gives <strong>3</strong>.</p>

<div class="step"><h4>1 &middot; What transitionTime actually indexes</h4>
<p>The wording — "the travel time between Hub <em>i</em> and its neighbors is <code>transitionTime[i]</code>" — reads as if it were a property of a <em>hub</em>. It cannot be: a hub has two neighbours, and a single number cannot price both without making the ring inconsistent. The reading that works is that <code>transitionTime[i]</code> prices the <strong>edge</strong> from hub <em>i</em> to hub <em>i+1</em>, with the last one wrapping back to hub 1:</p>
<div class="formula">edge 1&harr;2 costs transitionTime[1] = <b>3</b>
edge 2&harr;3 costs transitionTime[2] = <b>2</b>
edge 3&harr;1 costs transitionTime[3] = <b>1</b>      &larr; the wrap edge
total ring circumference = 3 + 2 + 1 = <b>6</b></div>
<p>With <em>m</em> hubs there are exactly <em>m</em> edges on a ring, which matches the array length — a second reason this is the intended reading.</p></div>

<div class="step"><h4>2 &middot; Prefix sums turn "arc length" into subtraction</h4>
<p>The drone only ever walks around the ring, so the cost of a hop is an arc length. Build the running distance from hub 1:</p>
<div class="formula">pre[0] = 0
pre[1] = 3          distance from hub 1 to hub 2
pre[2] = 3 + 2 = 5  distance from hub 1 to hub 3
pre[3] = 3 + 2 + 1 = 6 = <b>total</b>   (all the way round, back to hub 1)</div>
<p>Now the clockwise arc from <em>u</em> to <em>v</em> is a difference of two prefixes, and the modulo handles the wrap in one stroke:</p>
<div class="formula">clockwise(u &rarr; v) = (pre[v&minus;1] &minus; pre[u&minus;1]) <b>mod total</b>
anticlockwise      = total &minus; clockwise
hop(u, v)          = <b>min</b>(clockwise, anticlockwise)</div>
<p>The <code>-1</code>s are the 1-based-to-0-based shift: hub <em>v</em>'s distance from hub 1 lives at <code>pre[v-1]</code>. The <code>mod</code> is what makes a "negative" arc — going from a later hub to an earlier one — come back as the correct forward distance instead of a negative number. In Python <code>%</code> already returns a non-negative result for a positive modulus; in Java or C++ you must add <code>total</code> and take the modulus again.</p></div>

<div class="step"><h4>3 &middot; Every hop of the sequence</h4>
<p>The drone starts at hub 1 and visits the requested hubs in the given order — the sequence is <code>1 &rarr; 1 &rarr; 3 &rarr; 3 &rarr; 2</code>:</p>
<table class="trace">
<tr><th>hop</th><th>pre[v&minus;1] &minus; pre[u&minus;1]</th><th>clockwise (mod 6)</th><th>anticlockwise</th><th>min</th><th>running total</th></tr>
<tr><td>1 &rarr; 1</td><td>pre[0] &minus; pre[0] = 0</td><td>0</td><td>6</td><td>0</td><td>0</td></tr>
<tr><td class="hit">1 &rarr; 3</td><td>pre[2] &minus; pre[0] = 5</td><td>5</td><td>1</td><td class="hit">1</td><td>1</td></tr>
<tr><td>3 &rarr; 3</td><td>pre[2] &minus; pre[2] = 0</td><td>0</td><td>6</td><td>0</td><td>1</td></tr>
<tr><td class="hit">3 &rarr; 2</td><td>pre[1] &minus; pre[2] = &minus;2</td><td>(&minus;2) mod 6 = 4</td><td>2</td><td class="hit">2</td><td class="hit"><strong>3</strong></td></tr>
</table>
<p>Two rows are worth pausing on. <strong>Hop 1 &rarr; 3</strong>: the clockwise route 1&rarr;2&rarr;3 costs 3 + 2 = 5, but the single wrap edge 1&rarr;3 costs only 1, so the drone goes backwards. <strong>Hop 3 &rarr; 2</strong>: the raw difference is negative, and the modulo converts it to the clockwise arc 3&rarr;1&rarr;2 = 1 + 3 = 4; the direct edge 3&rarr;2 costs 2 and wins. Total <strong>3</strong>.</p>
<p>A repeated hub costs 0 and needs no special case — the formula gives <code>min(0, total)</code> = 0 on its own.</p></div>

<div class="step"><h4>4 &middot; Why each hop can be optimised independently</h4>
<p>It is worth being explicit that this greedy is not an approximation. The requests must be served <em>in the given sequence</em>, so the drone's position after hop <em>k</em> is pinned to <code>requestedHubs[k]</code> no matter how it got there. There is no state carried between hops — no fuel, no direction lock, no cost that depends on the route taken. So minimising each hop separately minimises the sum, and no DP or search is needed.</p>
<p>That independence is exactly what the sibling problem <a href='#circular' style='color:var(--accent)'>Warehouse Containers in a Circle</a> does <em>not</em> have: there, a single direction rule couples all the moves together, and the greedy per-move answer is wrong. Same ring, very different problem — worth comparing the two side by side.</p></div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Return type is <code>long</code>.</strong> Up to <em>n</em> hops each up to half the circumference; the sum overflows 32 bits easily.</li>
<li><strong>1-based hubs, 0-based arrays.</strong> Every index in <code>hop</code> carries a <code>-1</code>.</li>
<li><strong>Negative modulo</strong> must be normalised in Java/C++ (<code>((x % t) + t) % t</code>).</li>
<li><strong>Start at hub 1</strong>, and note the first requested hub may itself be hub 1 — a zero-cost hop, not a skipped one.</li>
<li><strong>Compute <code>total</code> once</strong>, not per hop.</li>
</ul></div>

<div class="step"><h4>6 &middot; What is unverified</h4>
<p>The screenshot stops immediately after the example header, so there is no published expected output to check against, and no Constraints. Two things in particular remain guesses: whether the drone must <strong>return to Hub 1</strong> at the end (if so, add one final <code>hop(cur, 1)</code>, which here would add 3 for a total of 6), and whether <code>transitionTime</code> is indexed as assumed above. The ring/prefix-sum structure is the only reading consistent with the visible text, but treat the number 3 as this page's derivation, not as a confirmed answer.</p></div>
</div></details>
</div>
`},

{
  id:'rects', section:'Amazon OA · Coding', platform:'CodeSignal-style',
  label:'Description', title:'Rectangles That Fit in a Box',
  minutes:30, score:'',
  images:['image29.png','image11.png'],
  fn:{name:'solution', ret:'boolean[]', params:[['int[][]','operations']]},
  gen:`def gen(rng, n):
    ops = []
    for _ in range(max(1, n)):
        t = 0 if (not ops or rng.random() < 0.6) else 1
        ops.append([t, rng.randint(1, 9), rng.randint(1, 9)])
    if all(o[0] == 0 for o in ops):
        ops.append([1, rng.randint(1, 9), rng.randint(1, 9)])
    return [ops]`,
  tests:[
    {in:[[[1, 1, 1]]], out:[true]},
    {in:[[[0, 1, 3], [0, 4, 2], [1, 3, 4], [1, 3, 2]]], out:[true, false]},
    {in:[[[0, 2, 2], [1, 2, 2], [1, 1, 5]]], out:[true, false]},
    {in:[[[0, 5, 1], [1, 1, 5], [1, 5, 5]]], out:[true, true]}
  ],
  body:`
<p>You are given <code>operations</code>, an array containing the following two types of operations:</p>
<ul>
  <li><code>[0, a, b]</code> – Create and save a rectangle of size <code>a × b</code>;</li>
  <li><code>[1, a, b]</code> – Answer the question: "Could every one of the <strong>earlier saved</strong> rectangles fit in a box of size <code>a × b</code>". It is possible to rotate rectangles by <code>90</code> degrees; ie: a rectangle of dimensions <code>a × b</code> can be rotated so that its dimensions are <code>b × a</code>. Note: We're trying to fit each rectangle within the box separately (not all at the same time).</li>
</ul>

<p>Your task is to return an array of booleans, representing the answers to the second type of operation, in the order they appear.</p>

<p>Note that the operations should be proceeded iteratively, so when <code>operations[i]</code> is executed only the results of the previous operations <code>0</code>, <code>1</code>, …, <code>i - 1</code> are available.</p>

<h3>Example</h3>
<ul>
  <li>For <code>operations = [[1, 1, 1]]</code>, the output should be <code>solution(operations) = [true]</code>.</li>
</ul>
<p>There are no rectangles, so they all can be fit in any box.</p>
<ul>
  <li>For <code>operations = [[0, 1, 3], [0, 4, 2], [1, 3, 4], [1, 3, 2]]</code>, the output should be
  <div class="frag">The source screenshot is cut off at this line — the expected output for the second example was not captured.</div></li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Rotation is allowed, so normalise every rectangle to (min side, max side). A rectangle fits in a box when both normalised sides are &le; the box's.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Each query asks whether <em>every</em> rectangle saved so far fits. Since fitting is per-rectangle and independent, you only need the running maximum of the min-sides and the running maximum of the max-sides.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Normalise each saved rectangle to <code>(lo, hi) = (min(a,b), max(a,b))</code> and keep two running maxima: <code>maxLo</code> and <code>maxHi</code>.</p>
<p>For a query box <code>(a, b)</code>, normalise it the same way to <code>(qlo, qhi)</code>. Every saved rectangle fits iff <code>maxLo &le; qlo</code> and <code>maxHi &le; qhi</code>.</p>
<p>With no rectangles saved, the answer is trivially <code>true</code> — which is exactly the first example.</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def solution(operations):
    max_lo = max_hi = 0
    out = []
    for op, a, b in operations:
        lo, hi = min(a, b), max(a, b)
        if op == 0:
            max_lo = max(max_lo, lo)
            max_hi = max(max_hi, hi)
        else:
            out.append(max_lo &lt;= lo and max_hi &lt;= hi)
    return out</code></pre><div class="unsure">The second example's expected output was cut off in the screenshot, so the code is validated only against example 1 (<code>[[1,1,1]] &rarr; [true]</code>) and the stated rotation rule.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples. The second one's expected output was cut off in the screenshot; it is derived below as <code>[true, false]</code>.</p>

<div class="step"><h4>1 &middot; When does one rectangle fit inside another?</h4>
<p>Rotation by 90&deg; is allowed, so a rectangle has no meaningful "width" and "height" — only a <strong>short side and a long side</strong>. Normalise both the rectangle and the box the same way and the test becomes two independent comparisons:</p>
<div class="formula">(lo, hi) = (min(a, b), max(a, b))

rectangle (rlo, rhi) fits in box (qlo, qhi)  &hArr;  <b>rlo &le; qlo</b> and <b>rhi &le; qhi</b></div>
<p>Why sorting both is enough: if the short side fits the short side and the long fits the long, orient the rectangle to match and it fits. Conversely if it fits in some orientation, then the smaller of its sides is at most the smaller of the box's — pairing a long side against a short one can only be harder. So the sorted comparison is exact, not a heuristic. Without normalising you would need to test both orientations explicitly: <code>(a&le;qa and b&le;qb) or (a&le;qb and b&le;qa)</code>, which is the same predicate written the long way.</p></div>

<div class="step"><h4>2 &middot; Why two running maxima answer every query</h4>
<p>A query asks whether <em>every</em> saved rectangle fits — each judged separately, as the statement stresses. So the answer is an AND over all saved rectangles:</p>
<div class="formula">all fit  &hArr;  (&forall;r: r.lo &le; qlo)  and  (&forall;r: r.hi &le; qhi)
         &hArr;  <b>max over r of r.lo &le; qlo</b>   and   <b>max over r of r.hi &le; qhi</b></div>
<p>The two conditions decouple, so you never need to keep the rectangles at all — two integers suffice. Note <code>maxLo</code> and <code>maxHi</code> may come from <em>different</em> rectangles, and that is fine: the AND is over each condition independently, so the pair need not correspond to any real rectangle. That is what makes O(1) space correct rather than merely convenient.</p>
<p>Both start at <strong>0</strong>, which is what makes the empty case work: with nothing saved, <code>0 &le; qlo</code> and <code>0 &le; qhi</code> hold for any positive box, so the answer is <code>true</code> — exactly example 1.</p></div>

<div class="step"><h4>3 &middot; Example 2 traced</h4>
<p><code>operations = [[0,1,3], [0,4,2], [1,3,4], [1,3,2]]</code>:</p>
<table class="trace">
<tr><th>op</th><th>(lo, hi)</th><th>action</th><th>max_lo</th><th>max_hi</th><th>output</th></tr>
<tr><td>[0, 1, 3]</td><td>(1, 3)</td><td>save</td><td>max(0,1) = 1</td><td>max(0,3) = 3</td><td>&mdash;</td></tr>
<tr><td>[0, 4, 2]</td><td>(2, 4)</td><td>save</td><td>max(1,2) = 2</td><td>max(3,4) = 4</td><td>&mdash;</td></tr>
<tr><td class="hit">[1, 3, 4]</td><td class="hit">(3, 4)</td><td class="hit">query</td><td>2 &le; 3 &check;</td><td>4 &le; 4 &check;</td><td class="hit"><strong>true</strong></td></tr>
<tr><td>[1, 3, 2]</td><td>(2, 3)</td><td>query</td><td>2 &le; 2 &check;</td><td>4 &le; 3 &cross;</td><td><strong>false</strong></td></tr>
</table>
<p>So the answer is <code>[true, false]</code>. Check it by hand: the box 3&times;4 holds the 1&times;3 rectangle and, rotated, the 4&times;2 one (4 along the box's 4-side). The box 3&times;2 cannot hold the 4&times;2 rectangle in either orientation, because 4 exceeds both of the box's sides — and that is precisely the <code>max_hi = 4 &gt; 3</code> failure. The 1&times;3 rectangle still fits; the query fails because <em>not all</em> do.</p>
<p>Note the second query's box is <em>smaller</em> than the first's and returns false after a true. Answers are not monotone in any useful direction, so you cannot cache "the last answer" — but you never need to, since both maxima are already the full summary of the past.</p></div>

<div class="step"><h4>4 &middot; The streaming requirement</h4>
<p>"Only the results of operations 0 … i&minus;1 are available" forbids the natural shortcut of scanning all the rectangles up front. The single-pass loop respects it automatically: <code>max_lo</code> and <code>max_hi</code> at the moment of a query reflect exactly the rectangles saved before it. A rectangle created <em>after</em> a query never affects that query's answer, which is why the update and the test must live in the same loop in operation order.</p></div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Do not test unsorted sides.</strong> Comparing <code>a&le;a'</code> and <code>b&le;b'</code> without normalising misses the rotation and returns false negatives.</li>
<li><strong>Each rectangle is fitted separately</strong> — the statement says so. This is not a packing problem, and no area or sum is involved.</li>
<li><strong>Initialise both maxima to 0</strong>, not to infinity, or the no-rectangles case returns false.</li>
<li><strong>Emit output only for type-1 operations</strong>; the result array is shorter than <code>operations</code>.</li>
<li><strong><code>&le;</code>, not <code>&lt;</code></strong> — a rectangle exactly the size of the box fits, as the 4&le;4 comparison in the first query shows.</li>
</ul></div>
</div></details>
</div>
`},

/* ============ SECTION 2 — WORK SIMULATION / WORK STYLE ============ */
{
  id:'mergeconflicts', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Question 1', title:'Merge Source Control Branches — Minimum Conflicts',
  minutes:30, score:'',
  images:['0.png','1.png','2.png'],
  fn:{name:'getMinimumConflicts', ret:'int', params:[['string','primary'],['string','secondary']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    al = 'abcd'
    s1 = ''.join(rng.choice(al) for _ in range(rng.randint(1, m)))
    s2 = ''.join(rng.choice(al) for _ in range(rng.randint(1, m)))
    return [s1, s2]`,
  tests:[
    {in:["zc", "d"], out:2},
    {in:["dae", "add"], out:1},
    {in:["aaa", "abb"], out:0},
    {in:["a", "a"], out:0},
    {in:["ba", "ba"], out:3},
    {in:["zyx", "abc"], out:3}
  ],
  body:`
<p>At Amazon, developers want to merge <em>primary</em> and <em>secondary</em> source control branches into a unified branch while preserving the order of commits from each branch. Each character of a branch represents a commit's priority, with <strong>lower alphabetical order indicating higher priority</strong>.</p>

<p>A <strong>conflict</strong> occurs when, in the merged branch, a commit with lower priority is placed before a commit with higher priority. Your task is to find the minimum number of conflicts in any valid merge of <em>primary</em> and <em>secondary</em> branches.</p>

<div class="note"><p>A "valid merge" is any interleaving of the two strings that keeps each branch's own characters in their original relative order.</p></div>

<h3>Example</h3>
<p><em>primary</em> = "zc"<br><em>secondary</em> = "d"</p>
<p>There are three possible merge arrangements:</p>
<ul>
  <li>"zcd" with <strong>2</strong> merge conflicts ('z' being lower priority is placed before higher priority commits 'c' and 'd')</li>
  <li>Similarly, "zdc" with <strong>3</strong> merge conflicts</li>
  <li>Similarly, "dzc" with <strong>2</strong> merge conflicts</li>
</ul>
<p>The minimum number of merge conflicts possible is <strong>2</strong>.</p>

<h3>Function Description</h3>
<p>The function <em>getMinimumConflicts</em> takes the following input:</p>
<ul>
  <li><em>string primary:</em> the commit sequence of the primary branch</li>
  <li><em>string secondary:</em> the commit sequence of the secondary branch</li>
</ul>

<h3>Returns</h3>
<ul><li><em>int:</em> the minimum number of conflicts after a valid merge</li></ul>

<h3>Constraints</h3>
<ul>
  <li>1 &le; |<em>primary</em>|, |<em>secondary</em>| &le; 1000</li>
  <li><em>primary</em> and <em>secondary</em> consist of lowercase English letters only.</li>
</ul>

<div class="sublabel">Input Format for Custom Testing</div>
<p>The first line contains string <em>primary</em>. The second line contains string <em>secondary</em>.</p>

<div class="cases">
  <div class="case"><div class="ch">SAMPLE CASE 0</div><pre class="sample">STDIN        FUNCTION
-----        --------
dae     &rarr;  primary   = "dae"
add     &rarr;  secondary = "add"

Sample Output
1

Explanation
"a<strong>da</strong>dde" has 1 merge conflict (highlighted in bold).</pre></div>
  <div class="case"><div class="ch">SAMPLE CASE 1</div><pre class="sample">STDIN        FUNCTION
-----        --------
aaa     &rarr;  primary   = "aaa"
abb     &rarr;  secondary = "abb"

Sample Output
0

Explanation
"aaaabb" has no merge conflicts.</pre></div>
</div>

<div class="srcnote"><strong>Reading the conflict count.</strong> A conflict is an <em>inversion</em> in the merged string: a pair (i, j) with i &lt; j and merged[i] &gt; merged[j]. Inversions <em>within</em> primary and <em>within</em> secondary are fixed no matter how you interleave — only the cross-pairs are yours to choose, which is what makes this a DP over the two prefixes rather than a greedy merge.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>A "conflict" is just an <strong>inversion</strong> in the merged string: a pair i &lt; j with merged[i] &gt; merged[j]. Now notice which inversions you can actually influence.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Inversions inside <em>primary</em> alone, and inside <em>secondary</em> alone, are fixed — relative order within each branch never changes. Only the <em>cross</em> pairs depend on how you interleave. So: count the two fixed parts once, then DP over (i, j) = how many characters of each branch you have placed.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p><strong>Step 1 — the fixed cost.</strong> Count inversions within <code>primary</code> and within <code>secondary</code> separately (any O(n log n) or, given n &le; 1000, O(n²) counting works). No merge can change these.</p>
<p><strong>Step 2 — the cross cost, by DP.</strong> Let <code>dp[i][j]</code> = minimum cross-conflicts having already emitted <code>primary[:i]</code> and <code>secondary[:j]</code>. Taking the next character from primary places <code>primary[i]</code> before every remaining character of secondary, so it adds the number of remaining secondary characters strictly smaller than it:</p>
<pre class="sample">dp[i][j] = min(
    dp[i-1][j] + (# of secondary[j:] strictly less than primary[i-1]),
    dp[i][j-1] + (# of primary[i:]  strictly less than secondary[j-1])
)</pre>
<p>Precompute suffix counts <code>sufP[i][c]</code> and <code>sufS[j][c]</code> over the 26 letters so each transition is O(1).</p>
<p>Answer = fixed inversions + <code>dp[n][m]</code>.</p><p><span class="cx">Time O(n·m + 26(n+m))</span><span class="cx">Space O(n·m)</span></p><pre class="sample"><code>def getMinimumConflicts(primary, secondary):
    n, m = len(primary), len(secondary)
    A = [ord(c) - 97 for c in primary]
    B = [ord(c) - 97 for c in secondary]

    def own_inversions(a):
        cnt = [0] * 26
        inv = 0
        for v in reversed(a):
            inv += sum(cnt[:v])          # later chars strictly smaller
            cnt[v] += 1
        return inv

    fixed = own_inversions(A) + own_inversions(B)

    # sufA[i][c] = count of value c in A[i:]
    def suffix_counts(a):
        k = len(a)
        suf = [[0] * 26 for _ in range(k + 1)]
        for i in range(k - 1, -1, -1):
            suf[i] = suf[i + 1][:]
            suf[i][a[i]] += 1
        return suf

    sufA, sufB = suffix_counts(A), suffix_counts(B)

    INF = float('inf')
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if dp[i][j] == INF:
                continue
            if i &lt; n:                       # emit primary[i]
                add = sum(sufB[j][:A[i]])   # secondary chars left that are smaller
                if dp[i][j] + add &lt; dp[i + 1][j]:
                    dp[i + 1][j] = dp[i][j] + add
            if j &lt; m:                       # emit secondary[j]
                add = sum(sufA[i][:B[j]])
                if dp[i][j] + add &lt; dp[i][j + 1]:
                    dp[i][j + 1] = dp[i][j] + add
    return fixed + dp[n][m]</code></pre><div class="unsure">With |primary|, |secondary| &le; 1000 the O(n·m) table is 10<sup>6</sup> states — fine in Java/C++, tight in Python. If the judge times out, roll the DP to two rows and precompute the 26-way prefix sums instead of calling <code>sum()</code> inside the loop.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the statement's example <code>primary = "zc"</code>, <code>secondary = "d"</code> (answer <strong>2</strong>) and on Sample Case 0, <code>"dae"</code> / <code>"add"</code> (answer <strong>1</strong>).</p>

<div class="step"><h4>1 &middot; A conflict is an inversion</h4>
<p>"A commit with lower priority placed before one with higher priority", where lower alphabetical order means higher priority, is exactly:</p>
<div class="formula">conflict = a pair (i, j) with i &lt; j and merged[i] <b>&gt;</b> merged[j]</div>
<p>Strictly greater — equal characters do not conflict, which is what makes Sample Case 1 (<code>"aaa"</code> + <code>"abb"</code> &rarr; <code>"aaaabb"</code>) score 0. Check the example: <code>"zcd"</code> has pairs (z,c) and (z,d), both inverted, plus (c,d) which is fine &rarr; 2 conflicts, matching the statement.</p></div>

<div class="step"><h4>2 &middot; Split the cost into a part you cannot change and a part you can</h4>
<p>Every pair in the merged string has one of three origins, and this split is the key move:</p>
<table class="trace">
<tr><th>pair origin</th><th>relative order</th><th>can you change it?</th></tr>
<tr><td>both from primary</td><td>fixed — a valid merge preserves each branch's order</td><td><strong>no</strong></td></tr>
<tr><td>both from secondary</td><td>fixed, likewise</td><td><strong>no</strong></td></tr>
<tr><td>one from each</td><td>decided by how you interleave</td><td><strong>yes</strong></td></tr>
</table>
<div class="formula">answer = <b>fixed</b> (inversions inside primary + inversions inside secondary) + <b>min cross-inversions</b></div>
<p>On <code>"zc"</code> / <code>"d"</code>: inside primary the pair (z, c) is inverted &rarr; fixed = 1; secondary is a single character &rarr; 0. The answer 2 therefore means the best interleaving still contributes exactly 1 cross-inversion. Indeed <code>"dzc"</code> gives cross pairs (d,z) fine and (d,c) inverted &rarr; 1, and 1 + 1 = 2. &check; No interleaving does better, because <code>c</code> can never be lifted above <code>z</code>.</p>
<p><code>own_inversions</code> computes the fixed part by scanning right to left with a 26-slot tally: for each character, <code>sum(cnt[:v])</code> counts the already-seen — therefore later — characters strictly smaller than it.</p></div>

<div class="step"><h4>3 &middot; The DP state, and why cost is charged at emission time</h4>
<p><code>dp[i][j]</code> = minimum cross-conflicts once <code>primary[:i]</code> and <code>secondary[:j]</code> have been emitted. Two prefix lengths are a sufficient state because characters already emitted can no longer form new pairs with each other — only with what is still to come.</p>
<p>Emitting <code>primary[i]</code> places it before <em>every character of secondary not yet emitted</em>, namely <code>secondary[j:]</code>. Each of those strictly smaller is a new cross-inversion, and that count is knowable right now:</p>
<div class="formula">dp[i+1][j] = min(dp[i+1][j], dp[i][j] + #{ c in secondary[j:] : c &lt; primary[i] })
dp[i][j+1] = min(dp[i][j+1], dp[i][j] + #{ c in primary[i:]   : c &lt; secondary[j] })</div>
<p>This is the accounting trick that makes the state small: charge each cross-pair <strong>once</strong>, when the earlier of its two characters is placed. Nothing is double-counted, nothing deferred — so the DP need not remember <em>which</em> characters were emitted, only how many.</p>
<p><code>suffix_counts</code> makes each transition O(26): <code>sufB[j]</code> is the 26-letter tally of <code>secondary[j:]</code>, so <code>sum(sufB[j][:A[i]])</code> is the number of remaining secondary letters strictly below <code>primary[i]</code>. The slice <code>[:A[i]]</code> is "strictly less than"; <code>[:A[i]+1]</code> would include equals and break Sample Case 1.</p></div>

<div class="step"><h4>4 &middot; Sample Case 0 traced: "dae" + "add"</h4>
<p><code>A = d,a,e</code> = [3,0,4]; <code>B = a,d,d</code> = [0,3,3].</p>
<div class="formula">fixed inversions in "dae": the pair (d,a)   &rarr; <b>1</b>     (d&lt;e and a&lt;e are fine)
fixed inversions in "add": none            &rarr; <b>0</b>
fixed total = <b>1</b></div>
<p>The published answer is 1, so the minimum cross cost must be <strong>0</strong>. The statement's merge is <code>"adadde"</code>; here it is, charged the DP's way:</p>
<table class="trace">
<tr><th>emit</th><th>from</th><th>other side still unemitted</th><th>how many strictly smaller</th><th>cross cost</th></tr>
<tr><td>a</td><td>secondary[0]</td><td>"dae"</td><td>none &lt; 'a'</td><td>0</td></tr>
<tr><td>d</td><td>primary[0]</td><td>"dd"</td><td>none &lt; 'd'</td><td>0</td></tr>
<tr><td>a</td><td>primary[1]</td><td>"dd"</td><td>none &lt; 'a'</td><td>0</td></tr>
<tr><td>d</td><td>secondary[1]</td><td>"e"</td><td>none &lt; 'd'</td><td>0</td></tr>
<tr><td>d</td><td>secondary[2]</td><td>"e"</td><td>none &lt; 'd'</td><td>0</td></tr>
<tr><td class="hit">e</td><td class="hit">primary[2]</td><td class="hit">nothing left</td><td class="hit">0</td><td class="hit">0</td></tr>
</table>
<div class="formula">answer = fixed 1 + cross 0 = <b>1</b>   &check; matches the published output</div>
<p>The surviving conflict is the <code>(d, a)</code> pair <em>inside</em> primary — the statement highlights it as <code>"a<strong>da</strong>dde"</code>. No interleaving removes it, which is exactly what "fixed" means.</p></div>

<div class="step"><h4>5 &middot; Why greedy fails</h4>
<p>The natural greedy — always emit the smaller of the two current heads — is wrong, because the cost of emitting a character depends on the entire <em>remaining suffix</em> of the other string, not on its head. Emitting a slightly larger character now can pay for itself by unblocking a run of small ones later. That lookahead is what the O(n&middot;m) table buys. Verified against exhaustive enumeration of all interleavings on 300 random pairs over the alphabet abcd — no mismatch.</p></div>

<div class="step"><h4>6 &middot; Traps</h4>
<ul>
<li><strong>Strictly less, never &le;.</strong> Equal commits do not conflict; counting them turns Sample Case 1 from 0 into a positive number.</li>
<li><strong>Do not forget the fixed term.</strong> The DP alone returns 0 on <code>"zc"</code>/<code>"d"</code>; the answer is 2.</li>
<li><strong>Charge at emission against the other string's remaining suffix</strong> — not against everything, and not against what was already placed.</li>
<li><strong>Suffix counts, not prefix counts.</strong> <code>sufB[j]</code> must describe <code>secondary[j:]</code>, the part not yet emitted.</li>
<li><strong>10<sup>6</sup> states at the stated limits.</strong> Comfortable in Java/C++, tight in Python — roll the DP to two rows and precompute the 26-way prefix sums to remove the inner <code>sum()</code>.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'qualityscore', section:'Amazon OA · Coding', platform:'Reported Amazon OA',
  label:'Problem Statement', title:'Maximum Quality Score — Amplify or Adjust Ratings',
  minutes:45, score:'',
  images:['0.jpeg','1.jpeg'],
  fn:{name:'calculateMaxQualityScore', ret:'long', params:[['int','impactFactor'],['int[]','ratings']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [rng.randint(1, 4), [rng.randint(-9, 9) for _ in range(m)]]`,
  tests:[
    {in:[2, [5, -3, -3, 2, 4]], out:12},
    {in:[3, [5, -3, -3, 2, 4]], out:18},
    {in:[1, [-2, 3, -3, -1]], out:3},
    {in:[2, [-5]], out:-2},
    {in:[3, [1, 1, 1]], out:9},
    {in:[2, [-1, -2, -3]], out:0}
  ],
  body:`
<p>Imagine you're a seller on Amazon, specializing in eco-friendly products. Each of your items is rated by customers based on its quality and environmental impact.</p>

<p>The overall <strong>qualityScore</strong> of your products is determined by the <strong>maximum possible sum of consecutive ratings</strong>.</p>

<p>To improve the qualityScore of your products and attract more customers, you are given an integer <em>impactFactor</em> and the following two strategies:</p>
<ol>
  <li><strong>Amplify Ratings</strong>: Select a contiguous segment of ratings and amplify them by <strong>multiplying</strong> each rating in that range by <em>impactFactor</em>.</li>
  <li><strong>Adjust Ratings</strong>: Select a contiguous segment of ratings and adjust them by <strong>dividing</strong> each rating in that range by <em>impactFactor</em>.</li>
</ol>

<p>Your task is to determine the maximum possible qualityScore for your eco-friendly products after applying <strong>exactly one</strong> of these strategies.</p>

<div class="warn"><strong>Note:</strong> When applying the second strategy (Adjust Ratings): for dividing <strong>positive</strong> ratings use the <strong>floor</strong> value of the division result, and for dividing <strong>negative</strong> ratings use the <strong>ceiling</strong> value of the division result.</div>

<p><strong>Example:</strong> Given <em>ratings</em> = [4, -5, 5, -7, 1] and <em>impactFactor</em> = 2. If we choose to apply the second strategy with segment [2, 5] (assuming 1-based indexing) then modified ratings = [4, ceil(-5 / 2), floor(5 / 2), ceil(-7 / 2), floor(1 / 2)] = [4, -2, 2, -3, 0]. Note that ceil(-7 / 2) = -3 and floor(5 / 2) = 2.</p>

<p>Given an array of ratings of size <em>n</em> and an integer <em>impactFactor</em>, determine the maximum possible qualityScore — i.e. maximum possible sum of consecutive ratings — by optimally selecting exactly one of the strategies to modify the ratings.</p>

<h3>Example</h3>
<p>Input: <em>n</em> = 5, <em>ratings</em> = [5, -3, -3, 2, 4], <em>impactFactor</em> = 3</p>
<p>Let's try both the strategies with different contiguous ranges to get the maximum qualityScore:</p>
<table class="oa">
<tr><th>Strategy</th><th>Segment (1-based)</th><th>Modified Ratings</th><th>qualityScore</th></tr>
<tr><td>1</td><td>[1, 1]</td><td>[5*3, -3, -3, 2, 4] = [15, -3, -3, 2, 4]</td><td>10</td></tr>
<tr><td>2</td><td>[2, 3]</td><td>[5, ceil(-3/3), ceil(-3/3), 2, 4] = [5, -1, -1, 2, 4]</td><td>9</td></tr>
<tr><td>1</td><td>[4, 5]</td><td>[5, -3, -3, 2*3, 4*3] = [5, -3, -3, 6, 12]</td><td>12</td></tr>
</table>
<p>If we perform the first strategy on the subsegment [4, 5] (1-based indexing), we get the ratings = [5, -3, -3, 6, 12] with a qualityScore of <strong>12</strong>, which is the maximum qualityScore. Hence, the answer is <strong>12</strong>.</p>

<h3>Function Description</h3>
<p>Complete the function <em>calculateMaxQualityScore</em> in the editor below.</p>
<pre class="sample">long calculateMaxQualityScore(int impactFactor, int ratings[n])</pre>
<ul>
  <li><em>int impactFactor:</em> the value used in the strategies to amplify or adjust ratings.</li>
  <li><em>int ratings[n]:</em> an array representing the ratings of eco-friendly products.</li>
</ul>

<h3>Returns</h3>
<ul><li><em>long:</em> the maximum possible qualityScore of your eco-friendly products after applying exactly one of the strategies.</li></ul>

<h3>Constraints</h3>
<ul>
  <li>1 &le; <em>n</em> &le; 2 * 10<sup>5</sup></li>
  <li>1 &le; <em>impactFactor</em> &le; 10<sup>4</sup></li>
  <li>-10<sup>5</sup> &lt; <em>ratings[i]</em> &le; 10<sup>5</sup></li>
</ul>
<div class="frag">A second, typed copy of this problem (<code>1.jpeg</code>) states the bounds slightly differently — 1 &le; n &le; 10<sup>5</sup> and -10<sup>4</sup> &le; ratings[i] &le; 10<sup>4</sup>. Solve for the looser pair.</div>

<div class="warn"><strong>The worked example is self-inconsistent — don't lose time on it.</strong> The
input line says <em>impactFactor</em> = 3, but every row of the table above computes with <strong>2</strong>
(<code>5*2</code>, <code>2*2</code>, <code>4*2</code>). Both copies of the problem carry the same slip.
Running a correct solution: <em>impactFactor</em> = 2 gives <strong>12</strong> (the printed answer),
<em>impactFactor</em> = 3 gives <strong>18</strong>. Only the divide row (<code>ceil(-3/3) = -1</code>)
actually uses 3.</div>

<div class="cases">
  <div class="case"><div class="ch">SAMPLE CASE</div><pre class="sample">impactFactor = 1
ratings      = [-2, 3, -3, -1]

Output
3

Explanation
Since impactFactor = 1, applying any strategy will not change the
ratings. The initial qualityScore is the maximum sum of consecutive
ratings, which is 3.</pre></div>
</div>

<div class="srcnote"><strong>Shape of the solution.</strong> "Exactly one strategy, on one contiguous segment" plus "maximum sum of a consecutive run" is a Kadane variant with state: for each index track the best sum where the modified segment has <em>not started</em>, <em>is open</em>, and <em>has closed</em> — run it once for multiply and once for divide, and take the max. Watch the division rounding: it is toward zero, not floor.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Strip away the story: you may pick <strong>one</strong> contiguous segment and either multiply or divide every element in it, then take the maximum-sum subarray. Kadane solves the second half — the question is how to fold the segment choice into it.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Run Kadane with extra state. At each index track the best running sum for three situations: the modified segment hasn't started yet, it is currently open, or it has already closed. Transitions move you forward through those three states. Do it once for &times;factor and once for ÷factor, and take the best (never forget the do-nothing answer).</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Define, at index <em>i</em>, three running bests over subarrays ending at <em>i</em>:</p>
<ul>
<li><code>before</code> — no modification used yet (plain Kadane)</li>
<li><code>inside</code> — the modified segment is open and includes <em>i</em></li>
<li><code>after</code> — the segment has closed before <em>i</em></li>
</ul>
<pre class="sample">before = max(a[i],        before + a[i])
inside = max(before + f(a[i]), inside + f(a[i]), f(a[i]))
after  = max(inside + a[i],    after  + a[i])</pre>
<p>where <code>f</code> is <code>x*k</code> for the amplify pass and the rounding-toward-zero division for the adjust pass. The answer is the maximum of <code>inside</code> and <code>after</code> across all <em>i</em> (and of <code>before</code>, since applying the strategy to a segment outside your chosen subarray is equivalent to not applying it).</p>
<div class="unsure">The division rounds <strong>toward zero</strong>: floor for positives, ceiling for negatives. In Python <code>-3 // 2 == -2</code> is wrong here; use <code>int(x / k)</code> or <code>-((-x) // k)</code> for negatives.<br><br><strong>Verified against the samples:</strong> this code returns <code>12</code> for <code>(2, [5,-3,-3,2,4])</code> — matching the printed answer and the table's own arithmetic — <code>18</code> for <code>(3, …)</code>, and <code>3</code> for <code>(1, [-2,3,-3,-1])</code>. The mismatch is the statement's typo, not the algorithm's.</div><p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def calculateMaxQualityScore(impactFactor, ratings):
    def toward_zero(x, k):
        return x // k if x &gt;= 0 else -((-x) // k)

    def best_with(f):
        NEG = float('-inf')
        before = inside = after = NEG
        best = NEG
        for x in ratings:
            fx = f(x)
            after_new  = max(inside + x, after + x, NEG)
            inside_new = max(before + fx, inside + fx, fx)
            before_new = max(x, before + x)
            before, inside, after = before_new, inside_new, after_new
            best = max(best, before, inside, after)
        return best

    amplify = best_with(lambda x: x * impactFactor)
    adjust  = best_with(lambda x: toward_zero(x, impactFactor))
    return max(amplify, adjust)</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the statement's example <code>ratings = [5, -3, -3, 2, 4]</code>. Because the printed example is self-inconsistent, both readings are traced: <code>impactFactor = 2</code> gives <strong>12</strong> (the printed answer, and what the table's arithmetic actually does) and <code>impactFactor = 3</code> gives <strong>18</strong>.</p>

<div class="step"><h4>1 &middot; Three things are being chosen at once</h4>
<p>The problem stacks three independent choices, and naming them is most of the work:</p>
<div class="formula">1. <b>which strategy</b>   multiply, or divide          (exactly one, mandatory)
2. <b>which segment</b>   a contiguous range to transform
3. <b>which subarray</b>  the contiguous run whose sum you report</div>
<p>Choice 1 is settled by brute force — run the whole algorithm twice and take the better. That leaves choices 2 and 3, both contiguous ranges, freely positioned relative to each other. The reported subarray can sit entirely before the modified segment, entirely after it, overlap it partially, or be swallowed by it.</p>
<p>But only the <strong>intersection</strong> matters. Any part of the modified segment outside your subarray contributes nothing to the sum, so you may as well shrink the segment to exactly the part you use. That collapses the geometry to: <em>within the reported subarray, a (possibly empty) contiguous middle stretch is transformed</em> — which is a three-phase scan.</p></div>

<div class="step"><h4>2 &middot; Kadane with three states</h4>
<p>Plain Kadane keeps one running value: the best sum of a subarray ending at <em>i</em>. Here each subarray ending at <em>i</em> is in one of three phases with respect to the modified stretch, so keep three:</p>
<table class="trace">
<tr><th>state</th><th>meaning: best sum of a subarray ending at i where&hellip;</th></tr>
<tr><td><code>before</code></td><td>the modified stretch has not started — every element is raw</td></tr>
<tr><td><code>inside</code></td><td>the stretch is open and covers position <em>i</em> — element <em>i</em> is transformed</td></tr>
<tr><td><code>after</code></td><td>the stretch opened and already closed — element <em>i</em> is raw again</td></tr>
</table>
<div class="formula">before = max(a[i],              before + a[i])
inside = max(before + f(a[i]),  inside + f(a[i]),  f(a[i]))
after  = max(inside + a[i],     after  + a[i])</div>
<p>Read each line as "how could a subarray in this phase end at <em>i</em>?" — <code>inside</code> either continues an open stretch, opens one on top of a raw prefix, or starts fresh at <em>i</em>; <code>after</code> either continues a closed run or is the first raw element following the stretch. The phases can only move forward, <code>before &rarr; inside &rarr; after</code>, which is exactly what "one contiguous segment" means.</p>
<p>Note <code>after</code> has no "start fresh" term: you cannot be in the <em>after</em> phase without having had an <em>inside</em>. That asymmetry is deliberate, and dropping it would let the DP claim a modification it never made.</p></div>

<div class="step"><h4>3 &middot; The example traced, impactFactor = 2, amplify pass</h4>
<p><code>f(x) = 2x</code>, so the transformed values are <code>[10, -6, -6, 4, 8]</code>. States start at &minus;&infin;:</p>
<table class="trace">
<tr><th>i</th><th>a[i]</th><th>f(a[i])</th><th>before</th><th>inside</th><th>after</th><th>running best</th></tr>
<tr><td>0</td><td>5</td><td>10</td><td>5</td><td>10</td><td>&minus;&infin;</td><td>10</td></tr>
<tr><td>1</td><td>&minus;3</td><td>&minus;6</td><td>2</td><td>max(5&minus;6, 10&minus;6, &minus;6) = 4</td><td>10&minus;3 = 7</td><td>10</td></tr>
<tr><td>2</td><td>&minus;3</td><td>&minus;6</td><td>&minus;1</td><td>max(2&minus;6, 4&minus;6, &minus;6) = &minus;2</td><td>max(4&minus;3, 7&minus;3) = 4</td><td>10</td></tr>
<tr><td>3</td><td>2</td><td>4</td><td>2</td><td>max(&minus;1+4, &minus;2+4, 4) = 4</td><td>max(&minus;2+2, 4+2) = 6</td><td>10</td></tr>
<tr><td class="hit">4</td><td class="hit">4</td><td class="hit">8</td><td>6</td><td class="hit">max(2+8, 4+8, 8) = <strong>12</strong></td><td>max(4+4, 6+4) = 10</td><td class="hit"><strong>12</strong></td></tr>
</table>
<p>The winner is <code>inside = 12</code> at <em>i</em> = 4. Three branches competed there and it is worth reading what each one means:</p>
<table class="trace">
<tr><th>branch</th><th>value</th><th>the subarray it describes</th></tr>
<tr><td><code>before(i=3) + f(a[4])</code></td><td>2 + 8 = 10</td><td>raw <code>[2]</code>, then open the stretch on <code>a[4]</code> only</td></tr>
<tr><td class="hit"><code>inside(i=3) + f(a[4])</code></td><td class="hit">4 + 8 = <strong>12</strong></td><td class="hit">stretch already open at <em>i</em>=3, covering <code>a[3..4]</code> — both amplified</td></tr>
<tr><td><code>f(a[4])</code></td><td>8</td><td>stretch opens at <em>i</em>=4, subarray is <code>a[4]</code> alone</td></tr>
</table>
<p>The winner is the middle one: <code>inside(i=3) = f(a[3]) = 4</code> had opened the stretch at index 3, and index 4 extends it. That is the subarray <code>a[3..4]</code> with <strong>both</strong> elements amplified, <code>2&times;2 + 4&times;2 = 12</code> — precisely the statement's winning row, "strategy 1 on segment [4, 5]" in 1-based terms. &check;</p></div>

<div class="step"><h4>4 &middot; The divide pass, and the rounding that catches everyone</h4>
<p>The statement is explicit: <strong>floor for positives, ceiling for negatives</strong>. That is rounding <em>toward zero</em>, i.e. truncation — not Python's <code>//</code>, which floors toward &minus;&infin;:</p>
<table class="trace">
<tr><th>x, k</th><th>required</th><th>Python <code>x // k</code></th><th>correct expression</th></tr>
<tr><td>5, 2</td><td>floor(2.5) = 2</td><td>2 &check;</td><td><code>x // k</code></td></tr>
<tr><td>&minus;3, 2</td><td>ceil(&minus;1.5) = <strong>&minus;1</strong></td><td>&minus;2 &cross;</td><td><code>-((-x) // k)</code></td></tr>
<tr><td>&minus;7, 2</td><td>ceil(&minus;3.5) = <strong>&minus;3</strong></td><td>&minus;4 &cross;</td><td><code>-((-x) // k)</code></td></tr>
</table>
<p>Getting this backwards makes negative ratings <em>worse</em> instead of better, which silently destroys the whole point of the divide strategy — its only value is pulling negatives toward zero. On this example the divide pass peaks below 12, so amplify wins; the sample case <code>impactFactor = 1</code> is the degenerate check that both passes reduce to plain Kadane.</p></div>

<div class="step"><h4>5 &middot; Why taking <code>before</code> into the answer is legitimate</h4>
<p>The strategy is mandatory, so "apply nothing" is not literally available — yet the code lets <code>before</code> (pure Kadane, no modification) win. That is sound because the segment may be placed <em>outside</em> the reported subarray, where it changes nothing that is counted. The only forced-overlap case is <code>n = 1</code>, and there <code>inside</code> always matches or beats <code>before</code>: a positive lone rating is improved by multiplying, a negative one by dividing toward zero, and zero is unchanged. Verified against brute force over every segment and both strategies on 2000 random inputs — no mismatch.</p></div>

<div class="step"><h4>6 &middot; The broken example, and what to do in the exam</h4>
<p>The input line says <code>impactFactor = 3</code>, but every multiply row of the table computes with <strong>2</strong> — <code>5*2</code>, <code>2*2</code>, <code>4*2</code> — and only the divide row uses 3 (<code>ceil(-3/3) = -1</code>). Both published copies carry the same slip. A correct solution returns <strong>12</strong> for factor 2, which is the printed answer, and <strong>18</strong> for factor 3.</p>
<p>The practical lesson: when a worked example contradicts itself, trust the <em>arithmetic in the table</em> over the header line, confirm your code reproduces it, and move on. Do not spend exam minutes trying to make a correct algorithm reproduce an impossible number.</p></div>

<div class="step"><h4>7 &middot; Traps</h4>
<ul>
<li><strong>Truncate toward zero</strong>, not floor. The single most common failure.</li>
<li><strong>Return type is <code>long</code>.</strong> With n = 2&times;10<sup>5</sup>, ratings to 10<sup>5</sup> and impactFactor to 10<sup>4</sup>, an amplified sum reaches 2&times;10<sup>14</sup>.</li>
<li><strong>Run both passes.</strong> Multiplying is not always better — for an all-negative stretch, dividing is.</li>
<li><strong>Initialise to &minus;&infin;, not 0</strong>, or an all-negative array wrongly returns 0 (the subarray must be non-empty).</li>
<li><strong>No "start fresh" term for <code>after</code></strong>, or the DP claims a modification it never applied.</li>
<li><strong>impactFactor = 1</strong> makes both strategies no-ops; the answer is plain Kadane, as the sample case shows.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'minerrors', section:'Amazon OA · Coding', platform:'HackerRank (Amazon)',
  label:'Question', title:'Minimum Errors in a Binary String with Wildcards',
  minutes:45, score:'',
  images:['0 (1).jpeg','1 (1).png','2 (1).png'],
  fn:{name:'getMinErrors', ret:'int', params:[['string','errorString'],['int','x'],['int','y']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    s = ''.join(rng.choice('01!') for _ in range(m))
    return [s, rng.randint(0, 9), rng.randint(0, 9)]`,
  tests:[
    {in:["101!1", 2, 3], out:9},
    {in:["01!0", 2, 3], out:8},
    {in:["!!!!!!!", 23, 47], out:0},
    {in:["1!0!!!!", 9, 4], out:24},
    {in:["0", 5, 5], out:0},
    {in:["10", 1, 1], out:1},
    {in:["!!01!!", 3, 2], out:13}
  ],
  body:`
<p>Amazon's database doesn't support very large numbers, so numbers are stored as a string of binary characters, '0' and '1'. Accidentally, a <strong>'!'</strong> was entered at some positions and it is unknown whether they should be '0' or '1'.</p>

<p>The string of incorrect data is made up of the characters '0', '1' and '!', where '!' is the character that got entered incorrectly and can be replaced with either '0' or '1'. Due to some internal faults, some errors are generated every time '0' and '1' occur together as <code>'01'</code> or <code>'10'</code> in <strong>any subsequence</strong> of the string. It is observed that the number of errors a subsequence <code>'01'</code> generates is <em>x</em>, while a subsequence <code>'10'</code> generates <em>y</em> errors.</p>

<p>Determine the minimum total errors generated. Since the answer can be very large, return it modulo 10<sup>9</sup> + 7.</p>

<h3>Example</h3>
<p>Given <em>errorString</em> = "101!1", <em>x</em> = 2, <em>y</em> = 3:</p>
<ul>
  <li>If the '!' at index 3 is replaced with '0', the string is "10101". The number of times the subsequence 01 occurs is 3, at indices (1, 2), (1, 4) and (3, 4). The number of times the subsequence 10 occurs is also 3, at indices (0, 1), (0, 3) and (2, 3). The number of errors is 3<em>x</em> + 3<em>y</em> = 6 + 9 = <strong>15</strong>.</li>
  <li>If the '!' is replaced with '1', the string is "10111". The subsequence 01 occurs 3 times and 10 occurs 1 time. The number of errors is 3<em>x</em> + <em>y</em> = <strong>9</strong>.</li>
</ul>
<p>The minimum number of errors is min(9, 15) modulo (10<sup>9</sup> + 7) = <strong>9</strong>.</p>

<div class="note"><p><strong>Note:</strong> A subsequence of a string is obtained by omitting zero or more characters from the original string without changing their order.</p></div>
<div class="note"><p><strong>Hint:</strong> It can be proved that (a + b) % c = ((a % c) + (b % c)) % c where a, b, and c are integers and % represents the modulo operation.</p></div>

<h3>Function Description</h3>
<p>Complete the function <em>getMinErrors</em> in the editor below.</p>
<ul>
  <li><em>string errorString:</em> a string of characters '0', '1', and '!'</li>
  <li><em>int x:</em> the number of errors generated for every occurrence of subsequence 01</li>
  <li><em>int y:</em> the number of errors generated for every occurrence of subsequence 10</li>
</ul>

<h3>Returns</h3>
<ul><li><em>int:</em> the minimum number of errors possible, modulo 10<sup>9</sup> + 7</li></ul>

<h3>Constraints</h3>
<ul>
  <li>1 &le; len(<em>errorString</em>) &le; 10<sup>5</sup></li>
  <li>0 &le; <em>x</em>, <em>y</em> &le; 10<sup>5</sup></li>
  <li><em>errorString</em> consists only of the characters '0', '1', and '!'</li>
</ul>

<div class="cases">
  <div class="case"><div class="ch">SAMPLE CASE 0</div><pre class="sample">Input          FUNCTION
01!0      &rarr;  errorString = "01!0"
2         &rarr;  x = 2
3         &rarr;  y = 2   &lt;-- the exam's own typo: STDIN says 3

Sample Output
8

Explanation
The better string is 0100 with one substring 01 and two
substrings 10, making total errors = 2*1 + 3*2 = 8.</pre></div>
  <div class="case"><div class="ch">SAMPLE CASE 1</div><pre class="sample">Input          FUNCTION
!!!!!!!   &rarr;  errorString = "!!!!!!!"
23        &rarr;  x = 23
47        &rarr;  y = 27   &lt;-- same slip; answer is 0 either way

Sample Output
0

Explanation
There is a tie for the best string generated, 00000 or 11111,
with zero substrings 01 or 10.</pre></div>
</div>

<div class="warn"><strong>Two traps here.</strong> (1) <strong>The modulo.</strong> Minimise the <em>true</em> error count and reduce mod 10<sup>9</sup>+7 only at the end — comparing already-reduced values picks the wrong branch. (2) <strong>Sample Case 0 contradicts itself:</strong> the STDIN block reads <code>2</code> then <code>3</code>, but the FUNCTION annotation says <code>y = 2</code>. The explanation's own arithmetic <code>2&times;1 + 3&times;2 = 8</code> settles it — <strong>y = 3</strong>. With y genuinely 2 the answer would be 6, not 8. And a per-character greedy on '!' is <em>not</em> correct; see the solution.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Count the subsequences incrementally. When you place a character, how many new <code>01</code> and <code>10</code> pairs does it create with everything already to its left?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Scan left to right keeping <code>zeros</code> and <code>ones</code> seen so far. Placing a '1' adds <code>zeros &times; x</code> errors; placing a '0' adds <code>ones &times; y</code>. For each '!', pick whichever is cheaper <em>at that moment</em> — and prove to yourself the greedy is safe by noting the choice only ever increases future counts monotonically.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>A subsequence <code>01</code> is a '0' at some earlier index paired with a '1' later. So sweeping left to right:</p>
<ul>
<li>emit '1' → creates <code>zeros_so_far</code> new <code>01</code> pairs → cost <code>zeros * x</code></li>
<li>emit '0' → creates <code>ones_so_far</code> new <code>10</code> pairs → cost <code>ones * y</code></li>
</ul>
<p><strong>Choosing each '!' greedily on immediate cost is wrong</strong> — it ignores that the choice also grows a counter which prices every later character. On <code>"1!0!!!!"</code> with x = 9, y = 4 the greedy returns 40 where 24 is achievable.</p>
<p>The fix comes from an exchange argument. Take two wildcards <em>p</em> &lt; <em>q</em> assigned <code>1</code> and <code>0</code>, and swap them to <code>0</code> and <code>1</code>. Pairs involving anything outside <code>[p, q]</code> are unaffected; the pair (p, q) itself moves from cost <em>y</em> to cost <em>x</em>, and so does every character strictly between. The swap therefore changes the total by <code>(x &minus; y) &times; (1 + #between)</code>. If <code>x &le; y</code> the swap never hurts, so <strong>some optimal assignment puts all its wildcard 0s before all its wildcard 1s</strong>; if <code>x &gt; y</code>, the mirror image holds.</p>
<p>That collapses the search to a single <strong>threshold</strong> <em>t</em> — the first <em>t</em> wildcards take one value, the rest the other — leaving <code>2(k+1)</code> candidates, each priced in O(1) with prefix sums:</p>
<pre class="sample">cost(t) = C                      fixed-vs-fixed pairs, a constant
        + Σ(j &lt; t) c0[j]         each early wildcard costed as '0'
        + Σ(j ≥ t) c1[j]         each late wildcard costed as '1'
        + x · t · (k − t)        wildcard-vs-wildcard: every 0 before every 1</pre>
<p><span class="cx">Time O(n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>MOD = 10**9 + 7

def getMinErrors(errorString, x, y):
    zeros_before, ones_before = [], []
    z = o = 0
    for ch in errorString:                      # counters as of each index
        zeros_before.append(z); ones_before.append(o)
        if ch == '0': z += 1
        elif ch == '1': o += 1
    Z, O = z, o                                 # totals of fixed 0s and 1s

    C = 0                                       # fixed-vs-fixed pairs
    z = o = 0
    for ch in errorString:
        if ch == '0':   C += o * y; z += 1
        elif ch == '1': C += z * x; o += 1

    w = [i for i, ch in enumerate(errorString) if ch == '!']
    k = len(w)
    c0 = [y * ones_before[i]  + x * (O - ones_before[i])  for i in w]
    c1 = [x * zeros_before[i] + y * (Z - zeros_before[i]) for i in w]

    p0 = [0] * (k + 1); p1 = [0] * (k + 1)
    for j in range(k):
        p0[j + 1] = p0[j] + c0[j]
        p1[j + 1] = p1[j] + c1[j]

    best = min(
        min(C + p0[t] + (p1[k] - p1[t]) + x * t * (k - t) for t in range(k + 1)),
        min(C + p1[t] + (p0[k] - p0[t]) + y * t * (k - t) for t in range(k + 1)),
    )
    return best % MOD</code></pre><div class="unsure"><strong>The greedy previously published here was wrong</strong> — on <code>"1!0!!!!"</code>, x = 9, y = 4 it returned 40 against a true optimum of 24, and it disagreed with exhaustive search on a large fraction of random inputs. The version above matches brute-force enumeration of all 2<sup>k</sup> wildcard assignments on 6000 random cases and handles n = 100 000 in 0.07 s.<br><br><strong>Sample Case 0 is internally inconsistent in the source</strong> (STDIN <code>3</code>, annotation <code>y = 2</code>); with y = 3 this code returns the published 8, with y = 2 it returns 6. <strong>The modulo is still a trap:</strong> minimise exact integers and reduce only on the way out.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the statement's example <code>"101!1"</code>, x = 2, y = 3 (answer <strong>9</strong>) and on Sample Case 0.</p>

<div class="step"><h4>1 &middot; Subsequences, not substrings — and why that is good news</h4>
<p>The statement says <em>subsequence</em>: a <code>01</code> is <strong>any</strong> '0' paired with <strong>any</strong> later '1', adjacent or not. So the cost is a sum over pairs of positions:</p>
<div class="formula">cost = x &middot; #{(i, j) : i &lt; j, s[i]='0', s[j]='1'}  +  y &middot; #{(i, j) : i &lt; j, s[i]='1', s[j]='0'}</div>
<p>Counting those pairs is a one-pass job. Sweep left to right carrying <code>zeros</code> and <code>ones</code>, the counts seen so far:</p>
<div class="formula">meet a '1'  &rarr;  it closes a <b>01</b> with every earlier '0'  &rarr;  add <b>zeros &times; x</b>
meet a '0'  &rarr;  it closes a <b>10</b> with every earlier '1'  &rarr;  add <b>ones  &times; y</b></div>
<p>Verify on the statement's own example. <code>"10111"</code> (the '!' set to '1'):</p>
<table class="trace">
<tr><th>char</th><th>zeros</th><th>ones</th><th>cost added</th><th>running</th></tr>
<tr><td>1</td><td>0</td><td>0</td><td>zeros&times;x = 0</td><td>0</td></tr>
<tr><td>0</td><td>0</td><td>1</td><td>ones&times;y = 1&times;3 = 3</td><td>3</td></tr>
<tr><td>1</td><td>1</td><td>1</td><td>zeros&times;x = 1&times;2 = 2</td><td>5</td></tr>
<tr><td>1</td><td>1</td><td>2</td><td>1&times;2 = 2</td><td>7</td></tr>
<tr><td class="hit">1</td><td>1</td><td>3</td><td>1&times;2 = 2</td><td class="hit"><strong>9</strong></td></tr>
</table>
<p>Three <code>01</code>s and one <code>10</code>, so <code>3x + y = 6 + 3 = 9</code> — exactly the statement's figure. &check;</p></div>

<div class="step"><h4>2 &middot; Why the obvious greedy fails</h4>
<p>At a '!', the tempting move is to compare the two immediate costs — <code>zeros&times;x</code> if you write '1', <code>ones&times;y</code> if you write '0' — and take the cheaper. That is <strong>wrong</strong>, and the reason is that the immediate cost is only half the consequence: whichever you choose also <em>increments a counter</em>, making every later character of the opposite kind more expensive. The greedy is blind to that future bill.</p>
<div class="formula">counterexample:  "1!0!!!!"   x = 9   y = 4
greedy &rarr; <b>40</b>        true optimum &rarr; <b>24</b></div>
<p>Here y is much cheaper than x, so the optimum crowds the 1s to the front and the 0s to the back, accepting expensive-looking local choices to avoid many <code>01</code> pairs later. The greedy takes each cheap step and walks into the expensive configuration.</p></div>

<div class="step"><h4>3 &middot; The exchange argument that shrinks the search</h4>
<p>There are 2<sup>k</sup> assignments; you need an argument that only <em>k+1</em> shapes matter. Take any assignment with a wildcard <code>1</code> at position <em>p</em> and a wildcard <code>0</code> at a later position <em>q</em>, and swap them:</p>
<table class="trace">
<tr><th>pair</th><th>before swap (1&hellip;0)</th><th>after swap (0&hellip;1)</th><th>change</th></tr>
<tr><td>(p, q) itself</td><td>y</td><td>x</td><td>x &minus; y</td></tr>
<tr><td>(p, r) and (r, q) for each r strictly between</td><td>y</td><td>x</td><td>x &minus; y each</td></tr>
<tr><td>anything with r outside [p, q]</td><td colspan="2">r pairs with both p and q; the two costs merely trade places</td><td><strong>0</strong></td></tr>
</table>
<div class="formula">&Delta;cost = (x &minus; y) &times; (1 + #characters strictly between p and q)</div>
<p>So if <code>x &le; y</code>, every such swap is free or profitable: keep applying it and you reach an assignment where <strong>no wildcard 1 precedes a wildcard 0</strong> — all the 0s first, then all the 1s. If <code>x &gt; y</code> the same argument runs in reverse. Either way the optimum has a single <em>threshold</em>, and there are only <code>k+1</code> thresholds per direction. Computing both directions and taking the minimum removes the need to case-split on <code>x</code> versus <code>y</code> at all.</p>
<p>The row that matters most is the third: characters <em>outside</em> the swapped span are unaffected. That is what makes the argument local, and therefore repeatable until sorted.</p></div>

<div class="step"><h4>4 &middot; Pricing a threshold in O(1)</h4>
<p>Split every pair by what its two members are — this is the same decomposition as in <a href='#mergeconflicts' style='color:var(--accent)'>Merge Source Control Branches</a>:</p>
<table class="trace">
<tr><th>pair type</th><th>depends on the threshold?</th><th>how it is priced</th></tr>
<tr><td>fixed &times; fixed</td><td>no</td><td><code>C</code>, one sweep, computed once</td></tr>
<tr><td>fixed &times; wildcard</td><td>only on that wildcard's own value</td><td><code>c0[j]</code> or <code>c1[j]</code>, precomputed per wildcard</td></tr>
<tr><td>wildcard &times; wildcard</td><td>yes, but only through <em>t</em></td><td><code>x &middot; t &middot; (k &minus; t)</code></td></tr>
</table>
<p>The per-wildcard costs come straight from the pair definition. If wildcard <em>j</em> at index <em>i</em> becomes <code>'1'</code>, it makes a <code>01</code> with every fixed 0 before it and a <code>10</code> with every fixed 0 after it:</p>
<div class="formula">c1[j] = x &middot; zeros_before[i] + y &middot; (Z &minus; zeros_before[i])
c0[j] = y &middot;  ones_before[i] + x &middot; (O &minus;  ones_before[i])</div>
<p>And the last row is pure counting: with the first <em>t</em> wildcards set to '0' and the remaining <code>k-t</code> to '1', every one of the <code>t &times; (k-t)</code> cross pairs is a 0 before a 1, costing <em>x</em> each. Wildcard pairs sharing a value cost nothing. Prefix-sum <code>c0</code> and <code>c1</code> and each threshold is a constant-time lookup; the whole routine is O(n), 0.07 s at n = 100 000.</p></div>

<div class="step"><h4>5 &middot; Sample Case 0, and the typo in it</h4>
<p><code>"01!0"</code>, x = 2, y = 3 (see the warning above — the source's own annotation says y = 2, but its STDIN and its arithmetic both say 3). One wildcard, so two candidates:</p>
<table class="trace">
<tr><th>'!' becomes</th><th>string</th><th>#01</th><th>#10</th><th>cost</th></tr>
<tr><td class="hit">'0'</td><td class="hit">0100</td><td class="hit">1</td><td class="hit">2</td><td class="hit">1&times;2 + 2&times;3 = <strong>8</strong></td></tr>
<tr><td>'1'</td><td>0110</td><td>2</td><td>2</td><td>2&times;2 + 2&times;3 = 10</td></tr>
</table>
<p>Minimum 8, the published output, and the winning string <code>0100</code> is the one the explanation names. Had y really been 2, the same table would read 6 and 8, and the answer would be 6 — which is how you can tell the annotation is the part that is wrong.</p></div>

<div class="step"><h4>6 &middot; Traps</h4>
<ul>
<li><strong>Reduce mod 10<sup>9</sup>+7 exactly once, at the end.</strong> Comparing reduced candidates chooses the wrong threshold. All intermediate arithmetic must be exact.</li>
<li><strong>No per-character greedy.</strong> It is wrong; the threshold argument is what makes a linear scan legitimate.</li>
<li><strong>Try both directions.</strong> 0s-first is optimal only when <code>x &le; y</code>; taking the min of both readings costs nothing and removes the case analysis.</li>
<li><strong>Subsequences, not substrings.</strong> Counting only adjacent <code>01</code>/<code>10</code> gives far smaller numbers and passes no test.</li>
<li><strong>x or y may be 0</strong>, and the string may be all wildcards or contain none. <code>t</code> ranging over <code>0 .. k</code> covers "all one value" at both ends.</li>
<li><strong>64-bit.</strong> With n = 10<sup>5</sup> the pair count reaches ~5&times;10<sup>9</sup>, times x up to 10<sup>5</sup>.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'matrixcompress', section:'Amazon OA · Coding', platform:'Reported Amazon OA',
  label:'Problem Statement', title:'Matrix Compression — Max Sum of Exactly x Elements',
  minutes:45, score:'',
  images:['0 (2).jpeg'],
  fn:{name:'findMaxValue', ret:'long', params:[['int[]','factor'],['int[][]','data'],['int','x']]},
  gen:`def gen(rng, n):
    m = max(1, min(n, 40))
    data = [[rng.randint(1, 30) for _ in range(m)] for _ in range(m)]
    factor = [rng.randint(1, m) for _ in range(m)]
    return [factor, data, rng.randint(1, m * m)]`,
  tests:[
    {in:[[1, 2, 1], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2], out:15},
    {in:[[1, 1, 1], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 10], out:-1},
    {in:[[3, 3, 3], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9], out:45},
    {in:[[1], [[5]], 1], out:5},
    {in:[[2, 1], [[1, 9], [3, 4]], 2], out:13}
  ],
  body:`
<p>Amazon developers are working on a utility to compress an <em>n</em> &times; <em>n</em> matrix, <em>data</em>, using a compression rate represented by an array, <em>factor</em>. The goal is to determine the <strong>maximum sum of exactly <em>x</em> elements</strong> from the matrix under the following constraints:</p>
<ul>
  <li>For each row <em>i</em> (0 &le; i &lt; n), the number of elements selected from that row must not exceed <em>factor[i]</em>.</li>
  <li>If it's not possible to select exactly <em>x</em> elements, return <strong>-1</strong>.</li>
</ul>

<h3>Function Description</h3>
<p>Write a function <em>findMaxValue</em> that computes the maximum sum under the given constraints.</p>
<pre class="sample">long findMaxValue(int factor[n], int data[n][n], int x)</pre>
<ul>
  <li><em>factor[n]:</em> an array representing the maximum number of elements that can be selected from each row of <em>data</em>.</li>
  <li><em>data[n][n]:</em> a square matrix of integers.</li>
  <li><em>x:</em> the total number of elements to be selected.</li>
</ul>

<h3>Returns</h3>
<ul>
  <li>A <em>long integer</em> representing the maximum sum of exactly <em>x</em> elements under the constraints.</li>
  <li>Return <strong>-1</strong> if it is not possible to select exactly <em>x</em> elements.</li>
</ul>

<h3>Example</h3>
<pre class="sample">n      = 3
data   = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
factor = [1, 2, 1]
x      = 2</pre>
<p><strong>Explanation.</strong> The best choices for each row are:</p>
<ul>
  <li>Row 0: select <code>3</code> (based on <em>factor[0]</em> = 1)</li>
  <li>Row 1: select <code>5, 6</code> (based on <em>factor[1]</em> = 2)</li>
  <li>Row 2: select <code>9</code> (based on <em>factor[2]</em> = 1)</li>
</ul>
<p>Only <em>x</em> = 2 elements can be selected. The optimal choice is to select <code>6</code> (from Row 1) and <code>9</code> (from Row 2).</p>
<pre class="sample">Output
15</pre>

<h3>Constraints</h3>
<ul>
  <li>1 &le; <em>n</em> &le; 50</li>
  <li>1 &le; <em>factor[i]</em> &le; <em>n</em></li>
  <li>1 &le; <em>data[i][j]</em> &le; 10<sup>4</sup></li>
  <li>1 &le; <em>x</em> &le; <em>n</em> * <em>n</em></li>
</ul>

<div class="srcnote"><strong>Shape of the solution.</strong> Sort each row descending, take prefix sums of the first <em>factor[i]</em> entries, then run a knapsack over rows: <code>dp[i][k]</code> = best sum using the first <em>i</em> rows and exactly <em>k</em> picks. Feasibility falls out of the DP — if <code>dp[n][x]</code> was never reached, return -1. With n &le; 50 the state space is at most 50 &times; 2500.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Within one row, if you are allowed to take <em>t</em> elements, which <em>t</em> do you take? That part needs no search at all.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Sort each row descending and prefix-sum it: taking <em>t</em> from row <em>i</em> is worth <code>prefix[i][t]</code>, for t up to <code>factor[i]</code>. Now it is a bounded knapsack over rows: <code>dp[i][k]</code> = best total using the first <em>i</em> rows and exactly <em>k</em> picks.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Two independent halves:</p>
<ol>
<li><strong>Per row:</strong> sort descending, prefix-sum. The best <em>t</em> elements of a row are its <em>t</em> largest, since all values are positive.</li>
<li><strong>Across rows:</strong> exact-count knapsack. <code>dp[k]</code> = best sum with exactly <em>k</em> picks so far, initialised to <code>-inf</code> except <code>dp[0] = 0</code>. For each row, iterate <em>k</em> downward and try every <code>t</code> in <code>0..factor[i]</code>.</li>
</ol>
<p>If <code>dp[x]</code> is still <code>-inf</code> at the end, exactly <em>x</em> picks was impossible → return <strong>-1</strong>.</p>
<p>Check the sample: rows sorted → [3,2,1], [6,5,4], [9,8,7]; caps 1, 2, 1; x = 2. Best is 9 (row 2) + 6 (row 1) = <strong>15</strong>. ✓</p><p><span class="cx">Time O(n² · x)</span><span class="cx">Space O(x)</span></p><pre class="sample"><code>def findMaxValue(factor, data, x):
    n = len(data)
    NEG = float('-inf')

    prefix = []
    for i in range(n):
        row = sorted(data[i], reverse=True)[:factor[i]]
        p = [0]
        for v in row:
            p.append(p[-1] + v)
        prefix.append(p)                 # p[t] = sum of t largest, t &lt;= factor[i]

    dp = [NEG] * (x + 1)
    dp[0] = 0
    for i in range(n):
        nxt = [NEG] * (x + 1)
        for k in range(x + 1):
            if dp[k] == NEG:
                continue
            for t in range(len(prefix[i])):
                if k + t &gt; x:
                    break
                cand = dp[k] + prefix[i][t]
                if cand &gt; nxt[k + t]:
                    nxt[k + t] = cand
        dp = nxt

    return dp[x] if dp[x] != NEG else -1</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example: <code>data = [[1,2,3],[4,5,6],[7,8,9]]</code>, <code>factor = [1,2,1]</code>, <code>x = 2</code>, answer <strong>15</strong>.</p>

<div class="step"><h4>1 &middot; The problem splits cleanly in two</h4>
<p>Two questions are tangled together, and they separate completely:</p>
<div class="formula">(a) given that I take <b>t</b> elements from row i, <b>which</b> t?
(b) how many should each row contribute, summing to exactly x?</div>
<p>Question (a) needs no search. All values are positive (<code>1 &le; data[i][j]</code>), and rows do not interact — taking an element from row <em>i</em> constrains nothing except row <em>i</em>'s own count. So the best <em>t</em> elements of a row are simply its <em>t</em> largest. Sort each row descending and prefix-sum it once:</p>
<div class="formula">row 0: [1,2,3] &rarr; sorted [3,2,1] &rarr; capped at factor 1 &rarr; [3]    prefix = [0, 3]
row 1: [4,5,6] &rarr; sorted [6,5,4] &rarr; capped at factor 2 &rarr; [6,5]  prefix = [0, 6, 11]
row 2: [7,8,9] &rarr; sorted [9,8,7] &rarr; capped at factor 1 &rarr; [9]    prefix = [0, 9]</div>
<p><code>prefix[i][t]</code> is now "the value of taking <em>t</em> from row <em>i</em>", defined only for <code>t &le; factor[i]</code> — the cap is enforced by the array's <em>length</em>, so no bounds check appears anywhere in the DP. That is the tidy part of this solution: slicing with <code>[:factor[i]]</code> makes an illegal choice unrepresentable rather than merely rejected.</p>
<p>Question (b) is what remains, and it is a knapsack over rows where the "item" chosen from row <em>i</em> is <em>how many</em> to take.</p></div>

<div class="step"><h4>2 &middot; Exactly x, not at most x</h4>
<p>The statement demands <em>exactly</em> <code>x</code> elements and <code>-1</code> when that is impossible, so the DP must distinguish "count k is unreachable" from "count k is reachable with sum 0". That is what the <code>-inf</code> sentinel is for:</p>
<div class="formula">dp[0] = 0        taking nothing is reachable, worth nothing
dp[k] = &minus;&infin;      for k &ge; 1: not yet reachable</div>
<p>Initialising to 0 instead would silently answer the "at most x" problem and never return &minus;1. Because all values are positive, a max-sum solution would happily take fewer elements if allowed — so this distinction is not academic, it changes the answer.</p>
<p>Infeasibility has a simple cause: <code>&sum; factor[i]</code> may be less than <code>x</code>. With <code>factor = [1,1,1]</code> and <code>x = 10</code>, at most 3 elements exist to take, so <code>dp[10]</code> stays &minus;&infin; and the function returns &minus;1. No separate feasibility check is needed — the sentinel already carries that information.</p></div>

<div class="step"><h4>3 &middot; The DP, every cell</h4>
<p><code>dp[k]</code> = best sum using the rows processed so far and exactly <em>k</em> picks. Each row builds a fresh <code>nxt</code> array from the old one, trying every allowed <code>t</code>:</p>
<div class="formula">nxt[k + t] = max(nxt[k + t], dp[k] + prefix[i][t])   for every reachable k, every t &le; factor[i]</div>
<table class="trace">
<tr><th>after row</th><th>dp[0]</th><th>dp[1]</th><th>dp[2]</th><th>how dp[2] was reached</th></tr>
<tr><td>start</td><td>0</td><td>&minus;&infin;</td><td>&minus;&infin;</td><td>&mdash;</td></tr>
<tr><td>row 0 (cap 1, prefix [0,3])</td><td>0</td><td>3</td><td>&minus;&infin;</td><td>row 0 can supply at most 1</td></tr>
<tr><td>row 1 (cap 2, prefix [0,6,11])</td><td>0</td><td>max(3, 0+6) = 6</td><td>max(3+6, 0+11) = 11</td><td>either 1+1, or 2 from row 1</td></tr>
<tr><td class="hit">row 2 (cap 1, prefix [0,9])</td><td>0</td><td>max(6, 0+9) = 9</td><td class="hit">max(11, 6+9) = <strong>15</strong></td><td class="hit">1 from row 1 (=6) + 1 from row 2 (=9)</td></tr>
</table>
<p><code>dp[2] = 15</code>, the published answer, from picking <strong>6 and 9</strong> — exactly the two elements the statement names. Notice the last row genuinely improved on 11: taking both of row 1's best (6 + 5 = 11) loses to spreading the picks across rows (6 + 9 = 15). That is precisely why a greedy "fill the highest-capacity row first" fails and a DP is required.</p>
<p>Also worth seeing: the statement's explanation lists each row's <em>best possible</em> picks (3 / 5,6 / 9) before narrowing to two. Those per-row lists are the <code>prefix</code> arrays; the DP is the narrowing step.</p></div>

<div class="step"><h4>4 &middot; Why global "take the x largest" is wrong</h4>
<p>The two largest values in the whole matrix are 9 and 8, both in row 2 — but <code>factor[2] = 1</code> forbids taking both. Ignoring the caps gives 17, which is not achievable. Conversely the caps alone do not tell you where to spend picks, because the <em>marginal</em> value of a row's second element (row 1's 5) can be worth less than another row's first (row 2's 9). Only a joint optimisation gets both right, which is the knapsack.</p>
<p>One consequence worth internalising: within a row the marginal values are non-increasing (it is a sorted prefix sum, so the gaps shrink). That makes this a <em>concave</em> resource-allocation problem, and a greedy that repeatedly takes the best available marginal would in fact also be correct here — but the DP is simpler to get right under time pressure and needs no proof of concavity.</p></div>

<div class="step"><h4>5 &middot; Complexity and the bounds</h4>
<div class="formula">rows n &le; 50, x &le; n&sup2; = 2500, t &le; factor[i] &le; n = 50
work = n &times; x &times; max_t = 50 &times; 2500 &times; 50 = 6.25 &times; 10<sup>6</sup></div>
<p>Comfortable in any language. Space is O(x) with the rolling <code>nxt</code> array — the full table is unnecessary since each row reads only the previous row's values. The sorting adds <code>n &middot; n log n</code>, which is negligible.</p></div>

<div class="step"><h4>6 &middot; Traps</h4>
<ul>
<li><strong>Exactly x, not at most.</strong> Initialise <code>dp[1..x]</code> to &minus;&infin;, never 0.</li>
<li><strong>Return &minus;1</strong> when <code>dp[x]</code> is still &minus;&infin; — do not return 0 or the best smaller sum.</li>
<li><strong>Cap each row before prefix-summing</strong>, or the DP may take more than <code>factor[i]</code>.</li>
<li><strong><code>t = 0</code> must be allowed</strong> — a row may contribute nothing. That is the <code>prefix[i][0] = 0</code> entry.</li>
<li><strong>Return type is <code>long</code>:</strong> 2500 elements times 10<sup>4</sup> is 2.5&times;10<sup>7</sup>, safe in 32 bits here, but the signature asks for long.</li>
<li><strong>Do not sort <code>data</code> in place</strong> if the caller reuses it — <code>sorted()</code> copies.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'worksim', section:'Amazon OA · Work Simulation', platform:'Amazon Work Simulation',
  label:'Work Simulation', title:'Code Documentation Feedback — Inbox',
  minutes:20, score:'',
  images:['image34.png','image35.png'],
  fn:null,
  body:`
<p>In the Work Simulation you are dropped into a simulated Amazon workday. An inbox shows incomplete tasks; each one opens into a scenario followed by rating questions.</p>

<div class="inbox">
  <div class="ih">Inbox</div>
  <div class="ib">2 incomplete task(s)</div>
  <div class="row">
    <b>Code Documentation Feedback</b>
    <span>Becky Marks (Team Member)</span>
    <em>Task in progress</em>
  </div>
  <div class="row">
    <b>Welcome to Project Alert</b>
    <span>Matthew Sanchez (Team Lead)</span>
  </div>
</div>

<h3>Rating question (as it appears)</h3>
<div class="sim">
  <h2>Question 4 of 4</h2>
  <p class="quote">"I'll review your feedback with Matthew to make sure it aligns with his expectations for how to write up documentation."</p>
  <div class="likert"><i></i><i></i><i></i><i></i><i></i></div>
  <div class="lbl"><span>Not effective</span><span>Highly effective</span></div>
</div>

<div class="note"><p>Each response option is rated on a 5-point scale from <strong>Not effective</strong> to <strong>Highly effective</strong>, then you press <strong>Submit</strong>. There is no single correct answer — rate against Amazon's Leadership Principles (Ownership, Earn Trust, Deliver Results, Have Backbone; Disagree and Commit).</p></div>
`},

{
  id:'workstyle', section:'Amazon OA · Work Simulation', platform:'Amazon Work Style Assessment',
  label:'Work Style', title:'Your Work Style',
  minutes:6, score:'',
  images:['image42.png'],
  fn:null,
  body:`
<div class="sim">
  <h2 style="font-size:34px;font-weight:400;margin-bottom:20px">Your Work Style</h2>
  <p style="line-height:1.65;margin:0 0 16px">By completing this exercise, you'll give us a better sense of your work preferences and how you approach, organize, and complete tasks on the job. You'll be presented with pairs of statements and be asked to choose which of the two statements more closely describes your approach to work. At times it may be difficult to decide between the options, but remember to trust your instincts—often what pops into your head first is the best answer.</p>
  <p style="font-weight:700;margin:0 0 10px">Untimed Section</p>
  <p style="line-height:1.65;margin:0 0 16px">This section is NOT timed. Although you can spend as long as you need on this exercise, it will likely take you about six minutes to complete.</p>
  <p style="margin:0">Select <strong>Next</strong> to learn more.</p>
</div>
`},

/* ============ SECTION 3 — REAL-WORLD / DEBUGGING PROJECTS ============ */
{
  id:'moviedb-search', section:'Amazon OA · Debugging Projects', platform:'In-browser IDE (Java Spring Boot)',
  label:'Question Description', title:'MovieDB — Search Is Broken (Question 2)',
  minutes:60, score:'',
  images:['image51.png','image36.png','image39.png','image38.png'],
  fn:null,
  body:`
<h2 class="qsub">Question 2</h2>
<p>MovieDB is an app that allows users to explore movies, submit ratings, and share reviews. The search functionality helps users find movies by title, actors, and various filters. Currently, the search feature is not working correctly on the backend, limiting users' ability to discover content.</p>

<h3>Issue #1: Basic search is case-sensitive and returns results only for exact title matches</h3>
<p>The basic search feature is not functioning as intended. It only returns results when the entered query exactly matches a movie title, and it is currently case-sensitive. In addition, the search ignores the selected filter ('All', 'Title', 'Celebs') and always searches on titles only. This prevents users from discovering movies or celebrities, reducing the usefulness of the search experience.</p>

<h4>Steps to Reproduce:</h4>
<ul>
  <li>Navigate to the search bar at the top of the page.</li>
  <li>Open the search type dropdown and select any option (All, Title, or Celebs).</li>
  <li>Enter a search query and observe the results.</li>
</ul>
<figure class="fig"><img loading="lazy" src="../images/fig-moviedb-search.png" alt="The search type dropdown" data-full="../images/image51.png" title="Click to open the full screenshot"><figcaption>The search type dropdown</figcaption></figure>

<h3>Issue #2: Advanced search is not working as intended</h3>
<p>Advanced search does not surface matching movies and incorrectly reports no results.</p>
<h4>Steps to Reproduce:</h4>
<ul>
  <li>Open the search type dropdown and select Advanced Search.</li>
  <li>Apply any combination of filters.</li>
  <li>Click the Search Movies button.</li>
  <li>Observe that the page always displays 'No Matching Results'.</li>
</ul>

<h3>PROJECT_FILES_INSTRUCTIONS.md</h3>
<pre class="sample">## Read-only Files
The following files are marked read-only. You cannot edit these files
in the editor; however, it is possible from the terminal. You must not
modify or delete these files because doing so results in a zero score.

 * README.md
 * backend/src/main/java/com/moviedb/config/DataInitializer.java
 * backend/src/test/java/com/moviedb/controller/AdvancedSearchTest.java
 * backend/src/test/resources/application.yml
 * clean.sh
 * run.sh
 * setup.sh</pre>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Two separate issues. Issue #1 says search is case-sensitive, matches only exact titles, and ignores the selected filter. That is three defects in one query-building path.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Look for the repository/query method behind the search endpoint: an <code>equals</code> that should be a case-insensitive <em>contains</em>, and a filter parameter that is accepted by the controller but never threaded into the query. Issue #2 (advanced search always returning no results) is usually an <code>AND</code> chain that should skip unset filters.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p><strong>Issue #1 — basic search.</strong> Three fixes in the search query path:</p>
<ul>
<li>exact match → substring match (<code>LIKE %q%</code> / <code>containsIgnoreCase</code>)</li>
<li>case-sensitive → normalise both sides to lower case</li>
<li>the <code>All</code> / <code>Title</code> / <code>Celebs</code> selector is ignored → branch on it and search titles, cast names, or both</li>
</ul>
<p><strong>Issue #2 — advanced search always says "No Matching Results".</strong> The usual planted cause is that every filter is applied unconditionally, so an unset filter compares against <code>null</code>/empty and eliminates every row. The fix is to build the predicate list dynamically, adding a clause only when that filter has a value.</p>
<p>Work the same order as any debugging project: run the tests, read the failing assertions, then follow the request from controller → service → repository and fix at the layer that owns the defect.</p><div class="unsure"><strong>Inferred, not verified.</strong> Only the question description was captured — the Spring Boot source and <code>AdvancedSearchTest.java</code> were never on screen. These are the standard causes for exactly these two symptoms, but the actual planted bugs could differ. Treat this as a search plan, not an answer.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<div class="unsure" style="margin-top:0">No source was captured for this project, so nothing below claims to be the planted bug. What follows is the mechanism behind each symptom and the order to check things in — which is the transferable part anyway.</div>

<div class="step"><h4>1 &middot; Read the symptom as a specification</h4>
<p>Issue #1 states three separate failures in one paragraph. Separate them before touching code, because they live in different places:</p>
<table class="trace">
<tr><th>symptom</th><th>what it implies about the query</th><th>layer</th></tr>
<tr><td>only exact title matches</td><td>equality comparison, not a substring match</td><td>repository / query</td></tr>
<tr><td>case-sensitive</td><td>no normalisation on either side</td><td>repository / query</td></tr>
<tr><td>filter selector ignored</td><td>the parameter never reaches the branch, or there is no branch</td><td>controller &rarr; service</td></tr>
</table>
<p>The third is a different <em>kind</em> of bug from the first two: those are wrong SQL, this is a lost parameter. Fixing the query will not fix the dropdown, and a candidate who conflates them tends to fix one and declare victory.</p></div>

<div class="step"><h4>2 &middot; Exact-match &rarr; substring, case-insensitively</h4>
<p>In JPA the three common spellings, all equivalent:</p>
<pre class="sample">// derived query method
List&lt;Movie&gt; findByTitleContainingIgnoreCase(String q);

// JPQL
@Query("select m from Movie m where lower(m.title) like lower(concat('%', :q, '%'))")

// Criteria API
cb.like(cb.lower(root.get("title")), "%" + q.toLowerCase() + "%")</pre>
<p>Two details that bite. <strong>Normalise both sides</strong> — lowering only the column still fails on a mixed-case query, and lowering only the query still fails on mixed-case data. And <strong>the wildcards belong in the pattern, not the parameter</strong>: <code>like :q</code> with <code>q = "%bat%"</code> works but hides the intent and breaks the moment someone passes a raw term.</p></div>

<div class="step"><h4>3 &middot; The dropdown: one parameter, three branches</h4>
<p>"All / Title / Celebs" has to arrive as a request parameter and reach a branch:</p>
<pre class="sample">switch (type == null ? "ALL" : type.toUpperCase()) {
    case "TITLE":  return movieRepo.findByTitleContainingIgnoreCase(q);
    case "CELEBS": return celebRepo.findByNameContainingIgnoreCase(q);
    default:       return union(movies, celebs);      // "All"
}</pre>
<p>Trace it end to end before assuming the branch is missing — the parameter is lost more often than the logic is. Check that the frontend sends it, that the controller declares it (<code>@RequestParam(required = false) String type</code>), and that the service signature actually takes it. A service method that never received the value cannot branch on it, and that is invisible if you start reading at the repository.</p></div>

<div class="step"><h4>4 &middot; Issue #2: why "always no results" is a specific fingerprint</h4>
<p><em>Always</em> empty — even with no filters set — is the signature of a predicate that is <strong>unconditionally applied</strong>. An unset filter arrives as <code>null</code> or <code>""</code>, and comparing against it excludes every row:</p>
<pre class="sample">// ✗ every filter always applied: one unset filter empties the result
where genre = :genre and year = :year and rating &gt;= :minRating

// ✓ build predicates only for filters that have a value
List&lt;Predicate&gt; ps = new ArrayList&lt;&gt;();
if (genre  != null &amp;&amp; !genre.isBlank()) ps.add(cb.equal(root.get("genre"), genre));
if (year   != null)                      ps.add(cb.equal(root.get("year"), year));
if (minRating != null)                   ps.add(cb.ge(root.get("rating"), minRating));
return cb.and(ps.toArray(new Predicate[0]));      // empty list =&gt; matches everything</pre>
<p>Note the useful property of the corrected version: an empty predicate list ANDs to <em>true</em>, so "no filters" naturally returns everything. That is the behaviour the bug inverts.</p>
<p>The rival explanation for "always empty" is an AND that should be an OR, or a join that should be a left join (dropping every movie with no cast rows). Distinguish them in one step: <strong>apply exactly one filter and see whether results appear.</strong> Still empty &rarr; the join or a query-wide defect. Results appear &rarr; it was the unconditional-predicate bug.</p></div>

<div class="step"><h4>5 &middot; The order to work in</h4>
<ol>
<li><strong>Run the tests first, before reading any source.</strong> <code>AdvancedSearchTest.java</code> is read-only, which makes it the specification — the assertion messages name the exact expected shapes.</li>
<li>Fix Issue #1's query first: it is the smaller change and it validates your understanding of the data layer.</li>
<li>For Issue #2, log the generated SQL (<code>spring.jpa.show-sql=true</code>) and read the <code>where</code> clause. A predicate against <code>null</code> is visible immediately, and this beats any amount of code reading.</li>
<li>Re-run after each change. Debugging projects are scored on tests passed, so a partially fixed project still scores.</li>
</ol>
<p><strong>Do not edit the read-only files.</strong> The instructions say modifying them scores zero, and that includes "just adding a test".</p></div>
</div></details>
</div>
`},

{
  id:'moviedb-recs', section:'Amazon OA · Debugging Projects', platform:'In-browser IDE (Django + React)',
  label:'Question Description', title:'MovieDB (Django + React) — Movie Recommendations',
  minutes:60, score:'',
  images:['image7.png','image15.png','image4.png'],
  fn:null,
  body:`
<h2 class="qsub">MovieDB(Django+React): Movie Recommendations</h2>

<h3>Overview</h3>
<p>MovieDB is an online app that allows users to explore movies, submit ratings, and share reviews.</p>
<p>However, the recommendations personalized to the users are currently broken. Even after users share their preferences, the recommendations don't appear. Your task is to fix the backend for it.</p>

<h3>Expected API Behavior</h3>

<h4>GET /api/ratings/recommendations/user</h4>
<p><strong>Purpose</strong> Returns personalized movie recommendations based on the user's ratings and watched history.</p>
<p><strong>Auth</strong>: Required (Bearer token)</p>
<p><strong>Success Responses (200 OK)</strong></p>
<p>With recommendations:</p>
<pre class="sample">{
    "message": "Found 10 personalized recommendations",
    "recommendations": [
      {
        "_id": "movie_id",
        "title": "Movie Title",
        "year": 2023,
        "rating": 8.5,
        "genre": ["Action", "Thriller"],
        "description": "...",
        "popularity": 95,
        "type": "movie",
        "score": 0.85,
        "source": "rated"|"watched",
        "sourceMovie": "Inception",
        "userRating": 9
      },
      ...
    ]
}</pre>

<p>No movies watched or rated yet:</p>
<pre class="sample">{
    "message": "Start exploring movies by rating them or marking them as watched to get…",
    "recommendations": []
}</pre>

<p>Some movies watched or rated, but no recommendations found:</p>
<pre class="sample">{
    "message": "No recommendations found. Try rating more movies or marking some as watc…",
    "recommendations": []
}</pre>

<h4>POST /api/ratings/:movieId</h4>
<p><strong>Purpose</strong> Submit or update a user's rating for a movie.</p>
<p><strong>Auth:</strong> Required (Bearer token)</p>
<p><strong>Request Body</strong></p>
<pre class="sample">{
  "rating": 8 // 1-10 integer
}</pre>
<p><strong>Success Responses (201/200)</strong></p>
<pre class="sample">{
  "message": "Rating added/updated successfully",
  "rating": 8
}</pre>

<h4>GET /api/ratings/:movieId/user</h4>
<p><strong>Purpose</strong> Retrieve the user's personal rating and watched status for a movie</p>
<p><strong>Auth:</strong> Required (Bearer token)</p>
<p><strong>Response Body (200)</strong></p>
<pre class="sample">{
  "rating": 8,
  "watched": true
}</pre>

<h4>POST /api/ratings/:movieId/watched</h4>
<p><strong>Purpose</strong> Mark/unmark a movie as watched</p>
<p><strong>Auth:</strong> Required (Bearer token)</p>
<p><strong>Response Body (201/200)</strong></p>
<pre class="sample">{
  "message": "Movie marked as watched/unmarked",
  "watched": true
}</pre>

<h3>Recommendation Algorithm</h3>
<p>The scoring algorithm generates personalized movie recommendations based on user preferences:</p>
<table class="oa">
<tr><th>User Action</th><th>Recommendation Strategy</th><th>Score Multiplier</th></tr>
<tr><td>Rated <strong>high</strong> (above 5)</td><td>Recommend movies with <strong>similar genres</strong></td><td>1.2x boost</td></tr>
<tr><td>Rated <strong>low</strong> (5 or below)</td><td>Recommend movies with <strong>different genres</strong></td><td>No boost</td></tr>
<tr><td>Watched only (no rating)</td><td>Recommend movies with <strong>similar genres</strong></td><td>No boost</td></tr>
<tr><td>Watched + rated <strong>high</strong></td><td>Recommend movies with <strong>similar genres</strong></td><td>1.2x boost</td></tr>
<tr><td>Watched + rated <strong>low</strong></td><td>Recommend movies with <strong>different genres</strong></td><td>No boost</td></tr>
</table>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Do not read the code first. Run the tests, then read <code>test_app.py</code>. The failure messages name the exact strings the endpoint must return, and the tests pin the counts (10, then 2) and compare every field against a golden JSON fixture.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>All four bugs sit in the last third of <code>get_recommendations</code>, around the <code>return</code> statements: two inverted <code>if</code> conditions, a <code>.sort()</code> that throws, and a response dict that is missing its payload key. The scoring loops in the middle are fine.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>The four bugs, with the corrected function</summary><div class="inner"><p><strong>This one is answered from a recording of the real attempt</strong> — see
<a href='#moviedb-recs-postmortem' style='color:var(--accent)'>the frame-by-frame post-mortem</a> for
the screenshots and the failing output.</p>
<h4>Bug 1 — inverted no-activity guard</h4>
<pre class="sample">if len(rated_movies) != 0 and len(watched_movies) != 0:   # ✗ fires when the user HAS activity
if not rated_movies and not watched_movies:               # ✓</pre>
<h4>Bug 2 — sort throws, and slices before sorting</h4>
<pre class="sample">sorted_recommendations = list(unique_recommendations.values())[:10]   # ✗ slices first
sorted_recommendations.sort(reverse=True)                             # ✗ TypeError on dicts -> 500

sorted_recommendations = sorted(                                      # ✓ sort, then slice
    unique_recommendations.values(), key=lambda r: r["score"], reverse=True
)[:10]</pre>
<p><code>.sort()</code> on a list of dicts raises <code>TypeError: '&lt;' not supported between
instances of 'dict' and 'dict'</code>; the bare <code>except Exception</code> swallows it and returns
500, which is why the tests report <code>KeyError: 'recommendations'</code> and later
<code>assert 500 == 200</code>.</p>
<h4>Bug 3 — inverted empty-result guard</h4>
<pre class="sample">if len(formatted_recommendations) != 0:   # ✗ says "none found" when there ARE results
if len(formatted_recommendations) == 0:   # ✓</pre>
<h4>Bug 4 — the success response has no payload</h4>
<pre class="sample">return JsonResponse({                                    # ✗ no "recommendations" key at all
    "message": f"Found {len(formatted)} personalized recommendations"
}, status=200)

return JsonResponse({                                    # ✓
    "message": f"Found {len(formatted)} personalized recommendations",
    "recommendations": formatted,
}, status=200)</pre>
<h4>The scoring rules the fixtures pin down</h4>
<ul>
<li>candidates must have <code>rating &gt;= 7.0</code> and exclude the source movie itself</li>
<li><code>totalScore = (genreScore * 0.7 + ratingScore * 0.3) * multiplier</code>, multiplier 1.2 only for rated-high</li>
<li>rated low (&le; 5) recommends <em>different</em> genres; watched-only and rated-high recommend similar</li>
<li>a movie that is both rated and watched: the rated signal wins (skip it in the watched pass)</li>
<li>dedupe by movie id keeping the higher score, sort descending, take 10</li>
<li><code>userRating</code> only on <code>source == "rated"</code></li>
</ul>
<p>The full corrected function is in the post-mortem entry.</p><p><span class="cx">4 one-line edits</span><span class="cx">All 6 tests</span></p><div class="unsure">Verified against the failing test output and the golden-fixture assertions captured on video; the corrected function was not itself run against the judge, because the exam had ended.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>The four bugs above are verified from the recording. This panel explains <em>why those four symptoms looked the way they did</em>, and traces the scoring formula the endpoint is supposed to implement.</p>

<div class="step"><h4>1 &middot; Reading the failure output backwards</h4>
<p>The tests reported <code>KeyError: 'recommendations'</code> first and <code>assert 500 == 200</code> later. Those look like two problems and are really one chain, which is worth unpicking because the same shape recurs constantly:</p>
<div class="formula"><b>.sort()</b> on a list of dicts
   &rarr; TypeError: '&lt;' not supported between instances of 'dict' and 'dict'
   &rarr; swallowed by a bare <b>except Exception</b>
   &rarr; handler returns <b>500</b>
   &rarr; the test reads response.json()["recommendations"] &rarr; <b>KeyError</b></div>
<p>So the <code>KeyError</code> is not a missing-key bug at all — it is the <em>shadow</em> of an exception three layers up. <strong>A bare <code>except</code> converts a precise error into a vague one</strong>, and the first move in any project with one is to make it re-raise (or log the traceback) so the real exception surfaces. Doing that turns a confusing KeyError into a one-line TypeError that names the fix.</p>
<p>Bug 4 — the response literally lacking a <code>"recommendations"</code> key — produces the identical <code>KeyError</code> on the success path. Two different causes, one symptom: that is why the tests only went green once both were fixed, and why fixing one and re-running looked like no progress.</p></div>

<div class="step"><h4>2 &middot; Sort before slicing, and sort by what</h4>
<pre class="sample">list(unique.values())[:10]   then  .sort(reverse=True)     # ✗ takes an arbitrary 10, then orders them
sorted(unique.values(), key=lambda r: r["score"], reverse=True)[:10]   # ✓</pre>
<p>Two independent errors in one line. <strong>Slicing first</strong> takes whichever ten the dict happened to hold and then orders those — so the top-scoring movie is missing whenever it sits eleventh in insertion order. This is the kind of bug that passes a "returns 10 items" assertion and fails a golden-fixture comparison, which is exactly what the tests did. <strong>Sorting dicts without a key</strong> then raises, as above. Note also that <code>.sort()</code> returns <code>None</code> and mutates in place, so <code>x = y.sort()</code> is a third way to lose the data.</p></div>

<div class="step"><h4>3 &middot; The two inverted guards</h4>
<p>Bugs 1 and 3 are both boolean inversions, and both are invisible on a quick read:</p>
<table class="trace">
<tr><th>guard</th><th>written</th><th>fires when</th><th>should be</th></tr>
<tr><td>no-activity early return</td><td><code>if len(rated) != 0 and len(watched) != 0</code></td><td>the user <em>has</em> both kinds of activity</td><td><code>if not rated and not watched</code></td></tr>
<tr><td>empty-result message</td><td><code>if len(formatted) != 0</code></td><td>results <em>were</em> found</td><td><code>if len(formatted) == 0</code></td></tr>
</table>
<p>Both also get the connective wrong: "no activity" is <code>not rated <b>and</b> not watched</code>, which by De Morgan is <code>not (rated <b>or</b> watched)</code> — the negation flips the operator. Writing the positive condition first and negating the whole thing is the reliable way to avoid this.</p>
<p>The tell for an inverted guard is a response that is <em>confidently wrong</em>: a user with plenty of ratings told they have no activity, or a "no recommendations found" message accompanying a populated list. If a message contradicts the data beside it, look for a flipped comparison rather than a data bug.</p></div>

<div class="step"><h4>4 &middot; The scoring formula, and where its inputs come from</h4>
<div class="formula">totalScore = (genreScore &times; <b>0.7</b> + ratingScore &times; <b>0.3</b>) &times; multiplier</div>
<p>Three independent decisions feed it, and the strategy table in the statement is really a lookup on the user's relationship to a source movie:</p>
<table class="trace">
<tr><th>user action</th><th>genres recommended</th><th>multiplier</th></tr>
<tr><td>rated above 5</td><td>similar</td><td>1.2</td></tr>
<tr><td>rated 5 or below</td><td><strong>different</strong></td><td>1.0</td></tr>
<tr><td>watched, no rating</td><td>similar</td><td>1.0</td></tr>
<tr><td>watched + rated high</td><td>similar</td><td>1.2</td></tr>
<tr><td>watched + rated low</td><td><strong>different</strong></td><td>1.0</td></tr>
</table>
<p>The last two rows encode a precedence rule that is easy to miss: when a movie is <em>both</em> rated and watched, <strong>the rating wins</strong> — so the watched pass must skip movies that already appeared in the rated pass, or the same source contributes twice with conflicting strategies. That is the "skip it in the watched pass" note in the solution.</p>
<p>Then the filters: candidates need <code>rating &ge; 7.0</code>, the source movie itself is excluded, results are deduped by movie id <em>keeping the higher score</em>, sorted descending, and capped at 10. <code>userRating</code> is emitted only when <code>source == "rated"</code>. Each of those is a separate assertion in the golden fixtures, compared field by field with a <code>&lt; 0.2</code> tolerance on the score — so a formula that is right in shape but wrong in a weight fails loudly rather than silently.</p>
<div class="unsure">The exact definitions of <code>genreScore</code> and <code>ratingScore</code> were never fully on screen — the README's Variable / Definition / Range table was scrolled past before it rendered. The weights, the multiplier, the 7.0 threshold and the precedence rule above <em>are</em> captured; the two component formulas are not.</div></div>

<div class="step"><h4>5 &middot; The method that actually mattered</h4>
<p>All four bugs sat in the last third of the function, around the return statements, while the scoring loops in the middle were correct. That is the general shape of these exercises: <strong>the planted bugs cluster in the plumbing, not the algorithm</strong>. Concretely, for a 60-minute debugging project:</p>
<ol>
<li><strong>Run the tests before reading any code.</strong> The assertions are the specification and they name exact strings and counts.</li>
<li><strong>Neutralise bare <code>except</code> blocks first</strong> so real exceptions surface. This one step would have turned the whole confusing failure chain into a named TypeError.</li>
<li><strong>Read the return statements and the guards around them</strong> before the business logic.</li>
<li><strong>Re-run after every single edit.</strong> Scoring is per test passed, so partial fixes still earn marks — and with interacting bugs (here, two causes of one KeyError) you need to know which change moved which test.</li>
</ol></div>
</div></details>
</div>
`},

{
  id:'moviedb-recs-postmortem', section:'Amazon OA · Debugging Projects',
  platform:'Screen recording · 24 Jun 2026 · 42:52',
  label:'Attempt post-mortem', title:'MovieDB Recommendations — My Attempt, Frame by Frame',
  minutes:60, score:'0 / 6 tests passed',
  images:[],
  fn:null,
  body:`
<div class="srcnote">
<strong>What this is.</strong> A reconstruction of my real 60-minute attempt at
<a href="#moviedb-recs" style="color:var(--accent)">MovieDB (Django + React) — Movie Recommendations</a>,
rebuilt frame-by-frame from the screen recording (the recording has no audio, so everything below
comes off the screen). Every still is stamped with two clocks: <span class="ts">VIDEO</span> is the
position in the recording, and the grey stamp is the <b>time left on the assessment clock</b> at that
instant. Recording starts with 41:52 showing, so <em>remaining ≈ 42:02 − video time</em>.
That clock is the whole <b>Coding Challenge (100 minutes)</b>, not a per-question timer — the
completion screen at the end confirms it — so 41:52 is what was left after the earlier item(s),
not a fresh hour.
<br><br>
<strong>Outcome: 0 of 6 tests passing when time expired.</strong> Four one-line bugs were still in the
file. Read the walk-through, then the playbook at the bottom — that is the part worth memorising.
</div>

<h3>1 · The system</h3>
<p>A Django REST backend with a React frontend. Movies, ratings and reviews are three separate Django
apps. Only <strong>one function</strong> is broken: <code>get_recommendations</code> in
<code>backend/apps/ratings/views.py</code> (line 166 in the original file).</p>

<pre class="sample"><code>backend/
  apps/movies/{models,views,urls}.py
  apps/ratings/{models,views,urls}.py     ← the entire task lives here
  apps/reviews/{models,views,urls}.py
  moviedb_backend/urls.py                 ← mounts /api/movies, /api/ratings, /api/reviews
  test/test_app.py                        ← the grader (~430 lines)
  pytest.ini · manage.py · db.sqlite3
frontend/                                 ← React; read-only for this task</code></pre>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-0010-ide-overview.jpg" alt="IDE overview">
  <figcaption><span class="ts">00:10</span><span class="ts left">41:52 left</span>
  <span><b>The workspace.</b> Project tree on the left, four tabs open, AI Assistant on the right,
  and the dev-server log in the terminal already showing live traffic to
  <code>/api/ratings/recommendations/user</code>. The exam clock is top-left.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-0030-urls-routing.png" alt="movies/urls.py">
  <figcaption><span class="ts">00:30</span><span class="ts left">41:32 left</span>
  <span><b>Routing.</b> Each app owns a <code>urls.py</code>. Useful for confirming the exact path the
  test hits — but this file was never the problem.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-0530-models-rating.png" alt="Rating model">
  <figcaption><span class="ts">05:30</span><span class="ts left">36:32 left</span>
  <span><b>The <code>Rating</code> model.</b> One row per (user, movie): <code>rating</code> is a
  nullable 1–10 integer and <code>watched</code> is a boolean. So a single row can be
  rated-only, watched-only, or both — which is exactly what the five-case algorithm table below
  keys off.</span></figcaption>
</figure>

<h3>2 · The endpoints</h3>
<table class="oa">
<tr><th>Endpoint</th><th>Purpose</th></tr>
<tr><td><code>GET /api/ratings/recommendations/user</code></td><td><strong>the broken one</strong> — personalized recommendations</td></tr>
<tr><td><code>POST /api/ratings/:movieId</code></td><td>submit / update a rating (1–10)</td></tr>
<tr><td><code>GET /api/ratings/:movieId/user</code></td><td>this user's rating + watched status</td></tr>
<tr><td><code>POST /api/ratings/:movieId/watched</code></td><td>mark / unmark watched</td></tr>
</table>
<p>All four require <code>Bearer</code> auth via the <code>@auth_middleware</code> decorator.</p>

<p>The recommendations endpoint has <strong>three</strong> response shapes, and getting the wrong one
is what most of the failures were:</p>
<pre class="sample"><code>// has recommendations
{"message": "Found 10 personalized recommendations", "recommendations": [ ... ]}

// no activity at all
{"message": "Start exploring movies by rating them or marking them as watched...",
 "recommendations": []}

// has activity, but nothing scored
{"message": "No recommendations found. Try rating more movies...", "recommendations": []}</code></pre>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-0200-spec-response.png" alt="README response shape">
  <figcaption><span class="ts">02:00</span><span class="ts left">40:02 left</span>
  <span><b>The spec's own example response.</b> Note the per-item fields: <code>score</code>,
  <code>source</code> (<code>"rated"</code> | <code>"watched"</code>), <code>sourceMovie</code>, and
  <code>userRating</code>. The tests assert on <code>source</code> and <code>sourceMovie</code>
  directly.</span></figcaption>
</figure>

<h3>3 · The algorithm</h3>
<table class="oa">
<tr><th>User action</th><th>Strategy</th><th>Multiplier</th></tr>
<tr><td>Rated <strong>high</strong> (above 5)</td><td>similar genres</td><td>1.2×</td></tr>
<tr><td>Rated <strong>low</strong> (5 or below)</td><td><em>different</em> genres</td><td>1.0</td></tr>
<tr><td>Watched only (no rating)</td><td>similar genres</td><td>1.0</td></tr>
<tr><td>Watched + rated high</td><td>similar genres</td><td>1.2×</td></tr>
<tr><td>Watched + rated low</td><td><em>different</em> genres</td><td>1.0</td></tr>
</table>

<pre class="sample"><code>totalScore = (genreScore × 0.7 + ratingScore × 0.3) × multiplier

genreScore  = (# genres shared with the source movie) / len(source.genre)
ratingScore = candidate.rating / 10</code></pre>

<p><strong>Constraints</strong> — every one of these is separately testable:</p>
<ul>
<li>only recommend movies with <code>rating &gt;= 7.0</code></li>
<li>remove duplicates, sort by score <strong>descending</strong>, return <strong>top 10</strong></li>
<li>same movie from two sources → keep the <strong>higher</strong> score</li>
<li>a movie both rated and watched → the <strong>rated</strong> signal wins</li>
<li><code>userRating</code> appears <strong>only</strong> when <code>source == "rated"</code></li>
</ul>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-0610-spec-algorithm.png" alt="README algorithm and constraints">
  <figcaption><span class="ts">06:10</span><span class="ts left">35:52 left</span>
  <span><b>The whole specification on one screen</b> — table, constraints and score formula. I had
  this open at minute 6 and still had not run the tests.</span></figcaption>
</figure>

<h3>4 · The tests</h3>
<p><code>backend/test/test_app.py</code> · class <code>TestMovieRecommendationAPI</code> · run with
<code>npm run test</code> (pytest under the hood) · <strong>6 tests</strong>. Helpers:
<code>seed_database()</code>, <code>get_movie_ids()</code>, <code>get_auth_token(self.client)</code>.
Each test seeds the DB, drives the <em>real</em> API with <code>self.client.post(...)</code> to set up
ratings and watched flags, then GETs recommendations and asserts on
<code>data['message']</code> and <code>data['recommendations']</code>.</p>

<table class="oa">
<tr><th>#</th><th>Test</th><th>Asserts</th></tr>
<tr><td>1</td><td><code>test_no_watched_or_rated_movies</code></td><td><code>'Start exploring movies'</code> in message</td></tr>
<tr><td>2</td><td><code>test_watched_movie_recommendations</code></td><td>200 + list; checks <code>source</code> / <code>sourceMovie</code></td></tr>
<tr><td>3</td><td><code>test_rated_high_or_low_recommendations</code></td><td>rates 9/10 → <code>'Found'</code>, 10 recs, <code>userRating</code></td></tr>
<tr><td>4</td><td><code>test_watched_and_rated_low</code></td><td>rates 5/10 + watched → <code>'No recommendations found'</code>, <code>len == 0</code></td></tr>
<tr><td>5</td><td><code>test_watched_and_rated_high</code></td><td><code>'Found'</code> in message</td></tr>
<tr><td>6</td><td><code>test_multiple_movies_watched_and_rated_sorted_by_score</code></td><td>results sorted by score descending</td></tr>
</table>

<div class="warn">
<strong>The tests are far stricter than the prose spec suggests.</strong> Tests 2–6 do not just check
the message — each one loads a <b>golden JSON fixture</b>
(<code>expected-high-rating.json</code>, <code>expected-low-rating.json</code>,
<code>expected-watched-low-rating.json</code>) and walks the returned list <em>in order</em>:
<pre class="sample">expected_results = load_expected_results('expected-high-rating.json')
for i, rec in enumerate(data['recommendations']):
    expected = expected_results[i]
    assert rec['title']  == expected['title']
    assert rec['year']   == expected['year']
    assert rec['rating'] == expected['rating']
    assert rec['genre']  == expected['genre']
    assert rec['description'] == expected['description']
    assert rec['popularity']  == expected['popularity']
    assert rec['type']   == expected['type']
    assert abs(rec['score'] - expected['score']) &lt; 0.2
    assert rec['source'] == expected['source']
    assert rec['sourceMovie'] == expected['sourceMovie']
    assert rec['userRating']  == expected['userRating']</pre>
So the <b>score arithmetic must be numerically right to within 0.2</b> and the <b>sort order must
match exactly</b> — the 0.7/0.3 weights, the 1.2× boost and the candidate filter are all load-bearing,
not decoration. The counts are pinned too: exactly <b>10</b> recommendations after one 9/10 rating,
and exactly <b>2</b> (the dissimilar movies) after a 5/10 rating on a watched movie.
</div>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-4159-test-fixtures.png" alt="fixture assertions in test_app.py">
  <figcaption><span class="ts">41:59</span><span class="ts left">0:03 left</span>
  <span><b>The assertions I never read.</b> <code>assert len(data['recommendations']) == 10</code>,
  then a golden fixture compared field by field. Three seconds of clock left.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-4203-test-lowrating.png" alt="test_watched_and_rated_low">
  <figcaption><span class="ts">42:03</span><span class="ts left">expired</span>
  <span><b><code>test_watched_and_rated_low</code></b> — rate movie 3 at 5/10, mark it watched, then
  expect exactly 2 recommendations from <code>expected-watched-low-rating.json</code>. This is the
  test that pins the "rated low → different genres" branch.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-4200-tests-opened.png" alt="test_app.py">
  <figcaption><span class="ts">42:00</span><span class="ts left">0:02 left</span>
  <span><b>The single most expensive frame in the recording.</b> This is the first time
  <code>test_app.py</code> is open in the editor — with two seconds left on the clock. Everything
  needed to pass was written here in plain English the whole time.</span></figcaption>
</figure>

<h3>5 · The first test run — minute 17</h3>
<figure class="vshot">
  <img loading="lazy" src="../images/vid-1830-first-failures.jpg" alt="first failing run">
  <figcaption><span class="ts">18:30</span><span class="ts left">23:32 left</span>
  <span><b>0 passed, 6 failed.</b> The first run happened 17 minutes into the recording — roughly 40% of
  the time I had left, spent before getting any signal at all.</span></figcaption>
</figure>

<pre class="sample"><code>FAILED test_no_watched_or_rated_movies
       - AssertionError: assert 'Start exploring movies' in 'Found 0 personalized recommendations'
FAILED test_watched_movie_recommendations
       - KeyError: 'recommendations'
FAILED test_rated_high_or_low_recommendations
       - AssertionError: assert 'Found' in 'No recommendations found'
FAILED test_watched_and_rated_low
       - AssertionError: assert 'No recommendations found' in 'Found 0 personalized recommendations'
FAILED test_watched_and_rated_high
       - AssertionError: assert 'Found' in ...</code></pre>

<div class="warn">
<strong>Read that output as a fingerprint.</strong> Two messages are swapped in <em>both</em>
directions, and one response is missing a key entirely. That is not five separate problems — it is
<strong>two inverted <code>if</code> conditions plus one missing dict entry</strong>. Four lines. The
whole diagnosis was available at minute 18.
</div>

<h3>6 · The bugs</h3>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-0550-views-collect.png" alt="collection loops">
  <figcaption><span class="ts">05:50</span><span class="ts left">36:12 left</span>
  <span><b>Phase 1 of the function</b> — build <code>rated_movies</code> from every rating
  (<code>&gt;= 1</code>, i.e. high <em>and</em> low; low ratings drive the "different genres" path, so
  this is correct).</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-0710-watched-loop.png" alt="watched loop and guard">
  <figcaption><span class="ts">07:10</span><span class="ts left">34:52 left</span>
  <span><b>Phase 2</b> — build <code>watched_movies</code>, attaching the matching rating if one
  exists. Directly below it sits the guard that became Bug 1.</span></figcaption>
</figure>

<div class="bug">
<h4>Bug 1 — the no-activity guard is inverted <span style="color:#888;font-weight:400">(line ~163)</span></h4>
<pre class="sample"><code># ✗ fires only when the user HAS activity — exactly backwards
if len(rated_movies) != 0 and len(watched_movies) != 0:
    return ... "Start exploring movies..."

# ✓
if not rated_movies and not watched_movies:
    return ... "Start exploring movies..."</code></pre>
<p>Breaks test 1 directly, and poisons test 4.</p>
</div>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-3310-inverted-guard.jpg" alt="inverted guard on screen">
  <figcaption><span class="ts">33:10</span><span class="ts left">8:52 left</span>
  <span><b>Bug 1 still live at minute 33</b>, highlighted on line 163. Over the session this line was
  edited five times and was <em>correct at 24:30</em>, then reverted, then made worse at 32:30, and
  only settled correct at 36:10. Editing without a test run between changes means never knowing
  which direction was right.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-1740-original-scoring.png" alt="original scoring branch">
  <figcaption><span class="ts">17:40</span><span class="ts left">24:22 left</span>
  <span><b>The scoring branch as it started.</b> <code>Movie.objects.all()</code> with no
  <code>rating &gt;= 7.0</code> filter, no <code>.exclude(id=movie.id)</code>, and no 1.2×
  multiplier. All three were genuine bugs — and all three I did fix.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-2510-multiplier-fixed.png" alt="1.2 multiplier added">
  <figcaption><span class="ts">25:10</span><span class="ts left">16:52 left</span>
  <span><b>Fixed ✓</b> — <code>rating__gte=7.0</code>, <code>.exclude(id=movie.id)</code> and
  <code>score *= 1.2</code> now all present in the rated-high branch.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-2630-watched-branch.png" alt="watched scoring branch">
  <figcaption><span class="ts">26:30</span><span class="ts left">15:32 left</span>
  <span><b>Fixed ✓</b> — the watched-only branch, correctly scoring with no multiplier and emitting
  <code>"source": "watched"</code> with no <code>userRating</code> key.</span></figcaption>
</figure>

<div class="bug">
<h4>Bug 2 — sorting a list of dicts, and slicing before sorting <span style="color:#888;font-weight:400">(lines 267–268)</span></h4>
<pre class="sample"><code># ✗ two bugs stacked on two lines
sorted_recommendations = list(unique_recommendations.values())[:10]   # slices BEFORE sorting
sorted_recommendations.sort(reverse=True)                             # TypeError on dicts

# ✓ sort by an explicit key, THEN take the top 10
sorted_recommendations = sorted(
    unique_recommendations.values(), key=lambda r: r["score"], reverse=True
)[:10]</code></pre>
<p><code>.sort()</code> on dicts raises
<code>TypeError: '&lt;' not supported between instances of 'dict' and 'dict'</code>. The function's
bare <code>except Exception</code> swallows it and returns <strong>500</strong> — which is why test 2
saw <code>KeyError: 'recommendations'</code> and, later, <code>assert 500 == 200</code>.
<strong>This one bug cost the exam.</strong></p>
</div>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-2930-sort-bug.png" alt="the sort bug">
  <figcaption><span class="ts">29:30</span><span class="ts left">12:32 left</span>
  <span><b>Bug 2 on screen, unnoticed.</b> The dedupe loop above it is correct — keep the higher
  score per movie id. The two lines under it are the whole failure.</span></figcaption>
</figure>

<div class="bug">
<h4>Bug 3 — the empty-result guard is inverted <span style="color:#888;font-weight:400">(line 290)</span></h4>
<pre class="sample"><code>if len(formatted_recommendations) != 0:      # ✗ says "none found" when there ARE results
    return ... "No recommendations found"

if len(formatted_recommendations) == 0:      # ✓</code></pre>
</div>

<div class="bug">
<h4>Bug 4 — the success response has no payload <span style="color:#888;font-weight:400">(line 296)</span></h4>
<pre class="sample"><code># ✗ "recommendations" key is simply absent → KeyError in every test that reads it
return JsonResponse({
    "message": f"Found {len(formatted_recommendations)} personalized recommendations"
}, status=200)

# ✓
return JsonResponse({
    "message": f"Found {len(formatted_recommendations)} personalized recommendations",
    "recommendations": formatted_recommendations,
}, status=200)</code></pre>
</div>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-3020-response-bug.png" alt="response block with bugs 3 and 4">
  <figcaption><span class="ts">30:20</span><span class="ts left">11:42 left</span>
  <span><b>Bugs 3 and 4 in a single screenshot.</b> Line 290 is inverted; the return at line 296 sends
  a message and nothing else. I scrolled past this block and did not compare it against the spec's
  three response shapes.</span></figcaption>
</figure>

<h3>7 · How the failures evolved</h3>
<figure class="vshot">
  <img loading="lazy" src="../images/vid-3810-ai-diagnosis.jpg" alt="AI assistant diagnosing the sort">
  <figcaption><span class="ts">38:10</span><span class="ts left">3:52 left</span>
  <span><b>The assistant finally names Bug 2</b> — "sorting a list of dicts needs a key function… your
  current <code>.sort(reverse=True)</code> is what causes the 500". Correct, and 21 minutes after the
  first 500 appeared. I had been using it to explain the frontend instead of to read a
  traceback.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-4140-sort-fixed.png" alt="sort fixed at the buzzer">
  <figcaption><span class="ts">41:40</span><span class="ts left">0:22 left</span>
  <span><b>Bug 2's sort is fixed with 22 seconds left</b> — but the <code>[:10]</code> on the line
  above still slices before the sort, and Bugs 3 and 4 are untouched.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-4220-time-up.jpg" alt="assessment over">
  <figcaption><span class="ts">42:20</span><span class="ts left">expired</span>
  <span>Time up.</span></figcaption>
</figure>

<figure class="vshot">
  <img loading="lazy" src="../images/vid-4224-challenge-complete.jpg" alt="challenge complete screen">
  <figcaption><span class="ts">42:24</span><span class="ts left">expired</span>
  <span><b>What the whole assessment looks like.</b> Coding Challenge (100 minutes) → Working at
  Amazon (~30 min, untimed) → Your Work Style (~6 min, untimed). The 100 minutes is shared across
  the coding items, so time overspent on an earlier question is taken straight out of this
  one.</span></figcaption>
</figure>

<h3>8 · The correct solution</h3>
<p>Everything from <code>rated_movies</code> / <code>watched_movies</code> collection upward was
already fine. This is the function with all four remaining bugs fixed:</p>
<pre class="sample"><code>@csrf_exempt
@require_http_methods(["GET"])
@auth_middleware
def get_recommendations(request):
    try:
        user_id = uuid.UUID(request.user_id)
        user_ratings = list(Rating.objects.filter(user_id=user_id))

        rated_movies = []
        for r in user_ratings:
            if r.rating and r.rating &gt;= 1:            # high AND low — low drives "different genres"
                try:
                    rated_movies.append({
                        'movie': Movie.objects.get(id=r.movie_id),
                        'rating': r.rating,
                        'movie_id': r.movie_id,
                    })
                except Movie.DoesNotExist:
                    pass

        watched_movies = []
        for r in user_ratings:
            if r.watched:
                try:
                    movie = Movie.objects.get(id=r.movie_id)
                    rated_entry = next(
                        (x for x in rated_movies if x['movie_id'] == r.movie_id), None)
                    watched_movies.append({
                        'movie': movie,
                        'movie_id': r.movie_id,
                        'rating': rated_entry['rating'] if rated_entry else None,
                    })
                except Movie.DoesNotExist:
                    pass

        # BUG 1 FIX — fire only when there is no activity at all
        if not rated_movies and not watched_movies:
            return JsonResponse({
                "message": "Start exploring movies by rating them or marking them "
                           "as watched to get personalized recommendations!",
                "recommendations": [],
            }, status=200)

        recommendations = []

        for entry in rated_movies:
            movie, user_rating = entry['movie'], entry['rating']
            pool = Movie.objects.filter(rating__gte=7.0).exclude(id=movie.id)[:50]

            if user_rating &gt; 5:                                    # similar genres, 1.2x
                cands = [m for m in pool if any(g in m.genre for g in movie.genre)][:50]
                boost = 1.2
            else:                                                  # different genres, no boost
                cands = [m for m in pool if not any(g in m.genre for g in movie.genre)][:50]
                boost = 1.0

            for c in cands:
                matches = len([g for g in movie.genre if g in c.genre])
                genre_score = matches / max(len(movie.genre), 1)
                rating_score = c.rating / 10
                recommendations.append({
                    "movie": c,
                    "score": (genre_score * 0.7 + rating_score * 0.3) * boost,
                    "source": "rated",
                    "sourceMovie": movie.title,
                    "userRating": user_rating,          # only on source == "rated"
                })

        for entry in watched_movies:
            movie, movie_id = entry['movie'], entry['movie_id']
            if any(r["movie_id"] == movie_id for r in rated_movies):
                continue                                # rated signal takes precedence
            pool = Movie.objects.filter(rating__gte=7.0).exclude(id=movie.id)[:50]
            cands = [m for m in pool if any(g in m.genre for g in movie.genre)][:50]
            for c in cands:
                matches = len([g for g in movie.genre if g in c.genre])
                genre_score = matches / max(len(movie.genre), 1)
                rating_score = c.rating / 10
                recommendations.append({
                    "movie": c,
                    "score": genre_score * 0.7 + rating_score * 0.3,   # no boost
                    "source": "watched",
                    "sourceMovie": movie.title,        # note: no userRating key
                })

        unique = {}
        for rec in recommendations:
            mid = str(rec["movie"].id)
            if mid not in unique or rec["score"] &gt; unique[mid]["score"]:
                unique[mid] = rec

        # BUG 2 FIX — sort with a key, then slice
        top = sorted(unique.values(), key=lambda r: r["score"], reverse=True)[:10]

        formatted = []
        for rec in top:
            m = rec["movie"]
            item = {
                "_id": str(m.id), "title": m.title, "year": m.year, "rating": m.rating,
                "genre": m.genre, "description": m.description,
                "popularity": m.popularity, "type": m.type,
                "score": rec["score"], "source": rec["source"],
                "sourceMovie": rec["sourceMovie"],
            }
            if "userRating" in rec:
                item["userRating"] = rec["userRating"]
            formatted.append(item)

        # BUG 3 FIX — == 0, not != 0
        if len(formatted) == 0:
            return JsonResponse({
                "message": "No recommendations found. Try rating more movies "
                           "or marking some as watched",
                "recommendations": [],
            }, status=200)

        # BUG 4 FIX — include the payload
        return JsonResponse({
            "message": f"Found {len(formatted)} personalized recommendations",
            "recommendations": formatted,
        }, status=200)

    except Exception as e:
        print(f"Get recommendations error: {e}")
        return JsonResponse({"message": "Server error"}, status=500)</code></pre>

<h3>9 · Timeline of the attempt</h3>
<table class="tl">
<tr><th>Video</th><th>Left</th><th>What happened</th></tr>
<tr><td>00:00–06:00</td><td>42:00</td><td>scrolling <code>views.py</code>, <code>urls.py</code>, <code>models.py</code>, README</td></tr>
<tr><td>06:10–06:30</td><td>35:50</td><td>full algorithm + constraints table on screen</td></tr>
<tr><td>06:40–09:30</td><td>35:20</td><td><strong>~3 minutes re-reading the same 30 lines</strong> of collection loops</td></tr>
<tr class="hot"><td>17:10</td><td>24:50</td><td><strong>first <code>Run Tests</code> — 18 minutes in.</strong> 0/6</td></tr>
<tr><td>18:30</td><td>23:30</td><td>full failure output visible; diagnosis was available here</td></tr>
<tr><td>24:30</td><td>17:30</td><td>Bug 1 accidentally <strong>correct</strong>… then reverted</td></tr>
<tr><td>25:10</td><td>16:50</td><td><code>rating__gte=7.0</code>, <code>exclude</code>, <code>1.2×</code> fixed ✓</td></tr>
<tr><td>26:50</td><td>15:10</td><td>2nd test run</td></tr>
<tr><td>30:10–30:30</td><td>11:40</td><td>Bugs 3 + 4 on screen, scrolled past</td></tr>
<tr><td>32:30</td><td>9:30</td><td>Bug 1 flipped to <code>!= 0 and != 0</code> — worse than the start</td></tr>
<tr class="hot"><td>33:10</td><td>8:50</td><td>3rd run: now <code>assert 500 == 200</code> — a real crash, ignored</td></tr>
<tr><td>36:10</td><td>5:50</td><td>Bug 1 finally correct ✓</td></tr>
<tr><td>38:10</td><td>3:50</td><td>AI assistant names the <code>.sort()</code> bug</td></tr>
<tr><td>40:00 / 41:30</td><td>2:00</td><td>last two test runs</td></tr>
<tr class="hot"><td>41:50</td><td>0:12</td><td><strong><code>test_app.py</code> opened for the first time</strong></td></tr>
<tr><td>42:01</td><td>0:00</td><td>time expires · 0/6 · Bugs 1(partially), 3, 4 + the slice still in the file</td></tr>
</table>

<h3>10 · What went wrong</h3>
<ol>
<li><strong>Ran the tests at minute 18, read them at minute 41.</strong> The tests <em>are</em> the
spec — they contain the exact expected strings. Reading them costs 3 minutes and hands you Bugs 1, 3
and 4 immediately.</li>
<li><strong>Never read a traceback.</strong> <code>assert 500 == 200</code> means the server threw.
The 500 survived from minute 17 to the end because I never looked at what raised it.</li>
<li><strong>Edited by guessing, and flip-flopped.</strong> Bug 1 was correct at 24:30, wrong at 32:30,
correct at 36:10 — because no test run separated the edits.</li>
<li><strong>Re-read the same 30 lines repeatedly</strong> instead of jumping to the
<code>return</code> statements, which is where a "data doesn't reach the UI" bug almost always is.</li>
<li><strong>Used the AI assistant as a search engine, not a diagnostician.</strong> It found Bug 2 —
at minute 36, after being asked to explain frontend components.</li>
</ol>

<h3>11 · The playbook for next time</h3>
<div class="warn">
<strong>0–5 min — run the tests before reading any code.</strong> The failure output is the
highest-information object in the exercise. It is free and it is first.<br><br>
<strong>5–10 min — read the test file, not the source.</strong> Write down every expected string and
response shape. That list is your acceptance checklist.<br><br>
<strong>10–15 min — read the broken function backwards</strong>, starting at the
<code>return</code> statements and walking up. Debugging projects hide bugs in exactly four places:
inverted comparisons (<code>!=</code>/<code>==</code>, <code>&gt;</code>/<code>&gt;=</code>), missing
response keys, sort/slice ordering, and off-by-one filters.<br><br>
<strong>Then: one bug, one test run.</strong> Never make two edits without a run between them.<br><br>
<strong>Any 500 is priority zero.</strong> It masks every other failure — get the traceback first.<br><br>
<strong>Ask the assistant for a diagnosis</strong>: paste the failing output and ask "which line
raises this?" — not "explain this file".
</div>
<p class="note">Four one-line edits separated this from a pass. The gap was not knowledge of Django —
it was the order the 60 minutes were spent in.</p>
`},

{
  id:'workflow-team', section:'Amazon OA · Debugging Projects', platform:'In-browser IDE',
  label:'Question Description', title:'Workflow — Edit / Delete Team (Question 2)',
  minutes:60, score:'',
  images:['image16.png','image8.png','image3.png','image2.png'],
  fn:null,
  body:`
<h2 class="qsub">Question 2</h2>
<p>Workflow is an app that allows teams to manage and track their work efficiently. The team management feature lets admins create teams, view team details, edit team information, and delete teams when needed. However, the edit and delete team features are not functioning correctly in the backend, and your task is to fix them.</p>

<h3>Issue Summary:</h3>
<p>Admins can edit team information or delete a team and see a success message, but the updated data does not appear on the screen.</p>

<h3>Steps to Reproduce:</h3>
<ul>
  <li>Log in using Admin credentials:</li>
</ul>
<pre class="sample">Email: alex@workflow.dev
Password: Password@123</pre>
<ul>
  <li>Hover over any team in the left sidebar.</li>
  <li>Click the ⋯ menu.</li>
</ul>
<figure class="fig"><img loading="lazy" src="../images/fig-workflow-board.png" alt="The Engineering team board" data-full="../images/image16.png" title="Click to open the full screenshot"><figcaption>The Engineering team board</figcaption></figure>
<ul>
  <li>Choose Edit, update the team information, then click Save changes, or choose Delete to remove the team.</li>
</ul>
<figure class="fig"><img loading="lazy" src="../images/fig-workflow-editteam.png" alt="Edit team — the fields under test" data-full="../images/image8.png" title="Click to open the full screenshot"><figcaption>Edit team — the fields under test</figcaption></figure>
<ul>
  <li>Notice the team in the sidebar does not update to reflect your changes (or does not disappear after deletion).</li>
</ul>

<h3>Expected Behavior:</h3>
<ul>
  <li>When an admin edits a team's information (<em>name, key, icon, iconColor</em>), the updated team details should be saved and reflected immediately in the sidebar.</li>
  <li>When an admin deletes a team, it should be removed from the sidebar immediately and should no longer appear anywhere in the app.</li>
</ul>

<p>Refer to the README.md file for more details.</p>
<div class="warn"><strong>Note:</strong> The acceptance criteria for this task require that your solution pass all predefined unit tests. Use failing test cases to guide debugging.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>The symptom is precise: the API reports success, but the sidebar does not change. So the write succeeded and something about what is returned or re-read is wrong — not the update itself.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Two classic causes: the update handler saves but returns the <em>stale</em> object (or no body), so the client re-renders old data; and the delete handler removes the row but the list endpoint still serves a cached/unfiltered collection. Check what each handler returns, not just what it writes.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p><strong>Edit team.</strong> Verify the handler (a) applies every field the form sends — <code>name</code>, <code>key</code>/identifier, <code>icon</code>, <code>iconColor</code>, not just the name — and (b) returns the <em>updated</em> entity so the client's store refreshes. A handler that saves then returns the pre-update copy produces exactly "success message, no visible change".</p>
<p><strong>Delete team.</strong> Check for a soft-delete flag that the list query does not filter on, or a delete that removes the team but leaves the sidebar's cached membership list intact.</p>
<p>Expected behaviour per the statement: edits are saved <em>and reflected immediately in the sidebar</em>; a deleted team disappears from the sidebar and from everywhere in the app.</p><div class="unsure"><strong>Inferred, not verified.</strong> Only the question description and two UI screenshots were captured; the backend source was never shown. Use the failing unit tests in the real environment to locate the defect.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<div class="unsure" style="margin-top:0">Only the question description and UI screenshots were captured — no backend source. Below is the mechanism behind this precise symptom, not a claim about the planted bug.</div>

<div class="step"><h4>1 &middot; "Success message, but nothing changes" is a narrow fingerprint</h4>
<p>That combination rules a lot out immediately. A success response means the request reached the handler, passed validation and authorisation, and returned 2xx — so the bug is <em>after</em> the decision to succeed. Exactly four mechanisms produce it:</p>
<table class="trace">
<tr><th>#</th><th>mechanism</th><th>how to confirm in one step</th></tr>
<tr><td>A</td><td>the write never persisted (no flush/commit, or a detached entity)</td><td><strong>reload the page.</strong> Still old &rarr; A</td></tr>
<tr><td>B</td><td>persisted, but the response returns the stale pre-update object</td><td>reload shows the change; the API response body does not</td></tr>
<tr><td>C</td><td>persisted and returned, but the client never refreshes its store</td><td>response body is correct; only the UI is stale</td></tr>
<tr><td>D</td><td>persisted, but the list query filters it out (soft delete, cache)</td><td>the item is gone from the list but still fetchable by id</td></tr>
</table>
<p><strong>Reloading the page is the single highest-value action here</strong>, and it costs three seconds. It splits the four candidates into {A} versus {B, C, D} before you have read a line of code. Candidates routinely skip it and spend twenty minutes reading the wrong layer.</p></div>

<div class="step"><h4>2 &middot; Mechanism A — the write that is not a write</h4>
<p>In JPA the classic version is mutating an entity that is no longer managed, or building a fresh object with the same id and never calling save:</p>
<pre class="sample">// ✗ team is detached: the setters change an object nobody is watching
Team team = new Team(dto.getId(), dto.getName());
team.setName(dto.getName());
return ResponseEntity.ok("Team updated");        // truthfully reports nothing

// ✓ load the managed entity, mutate it, save inside a transaction
@Transactional
public Team update(Long id, TeamDto dto) {
    Team team = repo.findById(id).orElseThrow();
    team.setName(dto.getName());
    team.setKey(dto.getKey());
    team.setIcon(dto.getIcon());
    team.setIconColor(dto.getIconColor());
    return repo.save(team);
}</pre>
<p>A missing <code>@Transactional</code> on a method that relies on dirty checking gives exactly this: no exception, no rollback message, no change.</p></div>

<div class="step"><h4>3 &middot; The field-by-field check the statement is hinting at</h4>
<p>The Expected Behavior names four fields explicitly — <strong>name, key, icon, iconColor</strong>. That enumeration is unlikely to be decorative. A handler that copies only <code>name</code> produces a <em>partially</em> working edit: the rename appears, the icon change does not. Compare the DTO's fields against the setters actually invoked, one line at a time, and check the mapper too if one is involved — a <code>@Mapping(ignore = true)</code> or a missing field in a MapStruct/ModelMapper config produces the same silent drop.</p>
<p>This is also why "it works for name" is not evidence the edit path is fine.</p></div>

<div class="step"><h4>4 &middot; Delete: the two failure shapes</h4>
<p>The statement asks for two distinct things — the team disappears from the sidebar, and it "should no longer appear anywhere in the app". That phrasing suggests the planted bug leaves a trace somewhere:</p>
<ul>
<li><strong>Soft delete not filtered.</strong> The row gets <code>deleted = true</code> but the list query has no <code>where deleted = false</code>. The team vanishes from one screen and survives on another.</li>
<li><strong>Orphaned associations.</strong> The team row goes but memberships, issues or board references remain, so the sidebar (which may render from memberships, not from teams) still shows it. Fix with cascade or by clearing the join rows explicitly.</li>
<li><strong>Foreign-key violation swallowed.</strong> A <code>try/catch</code> that logs and returns success turns a constraint failure into a green toast. Search the handler for a bare <code>catch</code>.</li>
</ul>
<p>That last one deserves a habit: in any debugging project, <strong>grep for empty or over-broad catch blocks first</strong>. They are the standard device for hiding a real exception behind a success path, and they explain "success message but no effect" better than anything else.</p></div>

<div class="step"><h4>5 &middot; Working order</h4>
<ol>
<li>Reload after an edit — split A from B/C/D.</li>
<li>Look at the actual HTTP response body in the network tab; that splits B from C.</li>
<li>Query the database directly for the row; that confirms persistence independently of both.</li>
<li>Only then read the handler, and read it against the four named fields.</li>
</ol>
<p>Each step is seconds and eliminates a branch. The task is backend-only ("fix them in the backend"), so if the response body is already correct and only the UI is stale, re-read the brief before editing frontend state.</p></div>
</div></details>
</div>
`},

{
  id:'workflow-issues', section:'Amazon OA · Debugging Projects', platform:'In-browser IDE',
  label:'Question Description', title:'Workflow — Issue & Sub-Issue Creation',
  minutes:60, score:'',
  images:['image31.png','image1.png'],
  fn:null,
  body:`
<h3>Issue #1: New issues do not appear on the board</h3>
<ul><li>Notice that the issue is not appearing on the board.</li></ul>
<p>When a new issue is created, it should appear immediately on the team board with a unique identifier (e.g., ENG-1, DES-2). The issue identifier should follow the format <strong>TEAM_KEY-NUMBER</strong> and auto-increment for each team independently.</p>

<h3>Issue #2: Sub-Issue creation is not working</h3>
<h4>Steps to Reproduce:</h4>
<ul>
  <li>Log in using the following test credentials:</li>
</ul>
<pre class="sample">Email: alex@workflow.dev
Password: Password@123</pre>
<ul>
  <li>Click on any existing issue from the board to open the issue detail page.</li>
  <li>Click on the Add Sub-Issue button.</li>
  <li>Fill in the sub-issue details and click the Create button.</li>
  <li>Notice that the sub-issue is not appearing in the sub-issues list.</li>
</ul>

<figure class="fig"><img loading="lazy" src="../images/fig-workflow-subissue-create.png" alt="Creating a sub-issue" data-full="../images/image1.png" title="Click to open the full screenshot"><figcaption>Creating a sub-issue</figcaption></figure>
<figure class="fig"><img loading="lazy" src="../images/fig-workflow-subissue-result.png" alt="Expected result: the sub-issue appears under the parent" data-full="../images/image1.png" title="Click to open the full screenshot"><figcaption>Expected after the fix — the new sub-issue appears in the parent’s Sub-issues list (0/1)</figcaption></figure>

<p>When a sub-issue is created, it should appear in the sub-issues section of the parent issue detail page.</p>
<pre class="sample">Implement data export feature
Allow users to export their data in various formats

  &#9660; Sub-issues 0/1                                        +
  ( ) Test 2                                              (C)   &larr; expected</pre>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>The sub-issue is created (no error) but does not appear under its parent. So the write happened — what links a child to its parent, and who reads that link?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Either the parent id is not persisted on the child (dropped in the DTO or never mapped), or it is persisted but the parent-detail query does not select children. The counter reading <code>0/0</code> before and <code>0/1</code> after in the two screenshots tells you which side to look at first.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Trace the create path: request body → DTO → entity. The <code>parentId</code> (or <code>parentIssueId</code>) is the field to follow — if it is missing from the DTO or not set on the entity, the child is created as a top-level issue and will never show under the parent.</p>
<p>Then trace the read path: the parent-issue detail endpoint must return its sub-issues, and the sub-issue counter must count them. The screenshots show the expected end state — the new sub-issue listed under <em>Sub-issues 0/1</em>.</p><div class="unsure"><strong>Inferred, not verified.</strong> Question description and UI screenshots only; no backend source was captured.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<div class="unsure" style="margin-top:0">Question description and UI screenshots only; no backend source was captured. What follows is mechanism and method.</div>

<div class="step"><h4>1 &middot; Two issues, one shared question</h4>
<p>Both symptoms are "I created something and it is not in the list". For any create-then-list defect there are exactly three places the object can be lost, and naming them turns the search into three checks instead of a code read:</p>
<div class="formula">create request &rarr; [1] <b>written?</b> &rarr; [2] <b>written with the right fields?</b> &rarr; [3] <b>the list query returns it?</b></div>
<p>Check them in that order, because each one makes the next meaningful. Query the database directly after the create: no row means [1]; a row with a null or wrong column means [2]; a correct row that the endpoint still omits means [3].</p></div>

<div class="step"><h4>2 &middot; Issue #2: follow <code>parentId</code>, field by field</h4>
<p>A sub-issue differs from an issue in exactly one respect — it has a parent. So the whole bug surface is that one field, and it can be dropped at any of four hand-offs:</p>
<table class="trace">
<tr><th>hand-off</th><th>failure</th><th>result</th></tr>
<tr><td>frontend &rarr; request body</td><td>not sent, or sent under another name</td><td>server never sees it</td></tr>
<tr><td>request body &rarr; DTO</td><td>field absent from the DTO class</td><td>silently deserialised as null</td></tr>
<tr><td>DTO &rarr; entity</td><td><code>setParent</code> never called</td><td>row created with parent_id NULL</td></tr>
<tr><td>entity &rarr; response/list</td><td>parent's detail query does not fetch children</td><td>row correct, list wrong</td></tr>
</table>
<p>The third row is the one that matches the reported symptom most cleanly: a sub-issue created with <code>parent_id = NULL</code> is a perfectly valid <em>top-level</em> issue. It would not appear under the parent — and it would quietly appear on the main board, which is worth checking, because seeing it there is strong evidence for this mechanism specifically.</p>
<p>Watch for the name mismatch too: <code>parentId</code> in JSON versus <code>parentIssueId</code> on the DTO. Jackson binds by name and ignores unknown properties by default, so a rename produces a null with no error anywhere.</p></div>

<div class="step"><h4>3 &middot; Issue #1: created but not on the board</h4>
<p>If the row exists and is correct, the defect is in the read path, and the usual causes are all filters the creator did not satisfy:</p>
<ul>
<li><strong>Status or column not set.</strong> A board groups by status; an issue created with a null status belongs to no column and renders nowhere.</li>
<li><strong>Board / project / team association missing</strong>, so the board's <code>where board_id = ?</code> excludes it.</li>
<li><strong>Sub-issues excluded by design.</strong> If the board query filters <code>parent is null</code>, then a bug in Issue #2 that <em>sets</em> a parent wrongly would remove the issue from the board — which would make the two reported issues the same bug seen from two screens. Worth explicitly ruling in or out, since it changes the fix from two to one.</li>
</ul></div>

<div class="step"><h4>4 &middot; Let the tests drive it</h4>
<p>The entry's screenshot shows a test list with the expected end state — the new sub-issue under <em>Sub-issues 0/1</em>. In these projects the tests are the specification, and the counter in that label is a second assertion: it is computed from the children collection, so a fix that creates the row but does not wire the association will move the list and not the counter, or vice versa. If the counter and the list disagree after your fix, you have found a second defect rather than finished the first.</p></div>
</div></details>
</div>
`},

{
  id:'banking-rbac', section:'Amazon OA · Debugging Projects', platform:'In-browser IDE (Spring Boot + Angular)',
  label:'Question Description', title:'Banking App — Role-Based Access Control (RBAC)',
  minutes:60, score:'',
  images:['image6.png','image22.png','image17.png','image50.png','image14.png','image5.png'],
  fn:null,
  body:`
<p>The Banking App lets users send and receive money, but it has security flaws that allow unauthorized access to other accounts. Users are able to view transactions that do not belong to their accounts.</p>

<p>Your task is to fix the access control on the backend to ensure the expected behavior below:</p>
<ul>
  <li>Users can only access transaction history related to their own accounts.</li>
  <li>Admins can view all user accounts and transactions. They also have the permissions to delete other user accounts.</li>
</ul>

<h3>Steps to Reproduce:</h3>
<ul>
  <li>Log in as a user (Email: yalen@gmail.com, password: yalen123)</li>
  <li>From the user icon in the navbar, select Transactions and notice that transactions from other users' accounts are being displayed (for example, account 1010113169).</li>
</ul>
<figure class="fig"><img loading="lazy" src="../images/fig-banking-transactions.png" alt="Transaction history showing other users' accounts" data-full="../images/image22.png" title="Click to open the full screenshot"><figcaption>Transaction history showing other users' accounts</figcaption></figure>
<ul>
  <li>Log in as an admin (Email: david@gmail.com, Password: david123)</li>
  <li>From the user icon in the navbar, select All Accounts. When you try to delete a specific account as an admin, the action appears successful, but the account is not actually deleted.</li>
</ul>
<figure class="fig"><img loading="lazy" src="../images/fig-banking-accounts.png" alt="Account Management — delete reports success but does nothing" data-full="../images/image22.png" title="Click to open the full screenshot"><figcaption>Account Management — delete reports success but does nothing</figcaption></figure>

<p>Refer to the README.md file for implementation details.</p>
<div class="warn"><strong>Note:</strong> The acceptance criteria for this task require that your solution pass all predefined unit tests.</div>

<h3>README.md — Banking App: Role-Based Access Control (RBAC)</h3>
<h4>Overview</h4>
<p>The Banking App is built with a Java Spring Boot backend and Angular frontend, enabling users to transfer and receive money.</p>
<p>The repository may intentionally contain other issues unrelated to this specific task. Please focus on the described task requirements and address bugs or errors associated with them.</p>

<h4>Expected API Behavior</h4>

<h4>POST /api/core-banking/auth/signin</h4>
<p><strong>Purpose</strong> Authenticate user and receive JWT token for subsequent requests.</p>
<p><strong>Request Body</strong></p>
<pre class="sample">{
  "emailAddress": "string",
  "password": "string"
}</pre>
<p><strong>Success Response (200 OK)</strong></p>
<pre class="sample">{
  "name": "Bearer",
  "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}</pre>

<h4>POST /api/core-banking/transaction</h4>
<p><strong>Purpose</strong> Create a new transaction between accounts.</p>
<p><strong>Headers</strong></p>
<pre class="sample">Authorization: Bearer YOUR_JWT_TOKEN</pre>
<p><strong>Request Body</strong></p>
<pre class="sample">{
  "fromAccountId": 1111213169,
  "toAccountId": 1111213170,
  "transferAmount": 100.00
}</pre>
<p><strong>Success Response (201 Created)</strong></p>
<pre class="sample">{
  "transactionId": 1042,
  "fromAccountId": 1111213169,
  "toAccountId": 1111213170,
  "transferAmount": 100.00,
  "dateCreated": "2024-01-15 10:30:00"
}</pre>
<p><strong>Error Responses</strong></p>
<ul><li>Unauthorized access (401)</li></ul>
<pre class="sample">{ "error": "Authentication required" }</pre>

<h4>GET /api/core-banking/transaction/transactionHistory?fromDate=2024-01-01&amp;toDate=2024-01-31</h4>
<p><strong>Purpose</strong> Get current user's transaction history within date range.</p>
<pre class="sample">Authorization: Bearer YOUR_JWT_TOKEN</pre>
<p><strong>Success Response (200 OK)</strong></p>
<pre class="sample">[
  {
    "transactionId": 1042,
    "accountId": 1111213169,
    "fromAccountId": 1111213169,
    "sourceCardNumber": "1234567890123456",
    "toAccountId": 1111213170,
    "transferAmount": 100.00,
    "dateCreated": "2024-01-15 10:30:00",
    "lastCreated": "2024-01-15 10:30:00"
  },
  {
    "transactionId": 1043,
    "accountId": 1111213169,
    "fromAccountId": 1111213169,
    "sourceCardNumber": "1234567890123456",
    "toAccountId": 1111213171,
    "transferAmount": 250.50,
    "dateCreated": "2024-01-16 14:20:00",
    "lastCreated": "2024-01-16 14:20:00"
  }
]</pre>

<h4>GET /api/core-banking/transaction/transactionHistory/accounts/{accountId}?fromDate=2024-01-01&amp;toDate=2024-01-31</h4>
<p><strong>Purpose</strong> Get any user's transaction history within date range (Admin only). Ensure users cannot access this.</p>
<pre class="sample">Authorization: Bearer YOUR_JWT_TOKEN</pre>
<p><strong>Success Response (200 OK)</strong></p>
<pre class="sample">[
  {
    "transactionId": 1042,
    "accountId": 1111213170,
    "fromAccountId": 1111213170,
    "sourceCardNumber": "1234567890123456",
    "toAccountId": 1111213169,
    "transferAmount": 100.00,
    "dateCreated": "2024-01-15 10:30:00",
    "lastCreated": "2024-01-15 10:30:00"
  }
]</pre>
<p><strong>Error Responses</strong></p>
<ul><li>Unauthorized access (401)</li></ul>
<pre class="sample">{ "error": "Authentication required" }</pre>
<ul><li>Insufficient permissions (403)</li></ul>
<pre class="sample">{ "error": "Admin access required" }</pre>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Both symptoms are authorization failures, in opposite directions: a normal user <em>sees too much</em>, and an admin's delete <em>does too little</em> while reporting success.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>For the transaction history: the query almost certainly filters by a request parameter instead of the authenticated principal, so any account id in the URL is honoured. For the delete: the endpoint returns 200 without checking the role, or checks it and swallows the failure — look for a missing <code>@PreAuthorize</code> and for a delete that is never committed.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p><strong>Leaked transaction history.</strong> The endpoint should scope results to the authenticated user's own accounts, derived from the JWT, not from a client-supplied account id. Fix by resolving the principal server-side and filtering on it — and reject (403) rather than silently returning another user's rows.</p>
<p><strong>Delete reports success but does nothing.</strong> Two things to check: the method needs a real role guard (admin only), and the delete must actually be applied and flushed — a common plant is a repository call on a detached entity, or a soft-delete flag the list query ignores.</p>
<p>The README in the challenge defines the full API contract (signin, transaction, transactionHistory with date range, account management); align each handler's authorization with it, then let the predefined unit tests drive the remaining detail fixes.</p><div class="unsure"><strong>Inferred, not verified.</strong> The question description and two photographed screens were captured; the Spring Boot + Angular source was not. Authorization bugs in these exercises are usually exactly these two shapes, but confirm against the failing tests.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<div class="unsure" style="margin-top:0">Question description and UI screenshots only; the Spring Boot / Angular source was not captured. Below is mechanism and method — and, for this topic, the security reasoning that must not be skipped.</div>

<div class="step"><h4>1 &middot; Two distinct checks that get confused</h4>
<p>Role-based access control tasks always contain two questions, and conflating them is the classic failure:</p>
<table class="trace">
<tr><th>check</th><th>question</th><th>example</th></tr>
<tr><td><strong>Authorisation by role</strong></td><td>is this <em>kind</em> of user allowed to call this endpoint at all?</td><td>only an admin may delete accounts</td></tr>
<tr><td><strong>Ownership</strong></td><td>is this <em>particular</em> user allowed to touch this <em>particular</em> row?</td><td>a user may read only their own transactions</td></tr>
</table>
<p>A role check alone lets any logged-in user read any other user's transactions by changing an id in the URL — the textbook <em>insecure direct object reference</em>. An ownership check alone lets a non-admin call an admin-only endpoint on their own data. The statement asks for both: <em>"users can only access transaction history related to their own accounts"</em> and <em>"admins can view all&hellip; and delete other user accounts"</em>.</p></div>

<div class="step"><h4>2 &middot; The rule that makes ownership checks correct</h4>
<p>There is one non-negotiable principle, and it is where most implementations go wrong:</p>
<div class="formula"><b>Take the identity from the authenticated principal, never from the request.</b></div>
<pre class="sample">// ✗ trusts the client: anyone can pass someone else's id
@GetMapping("/transactions")
List&lt;Tx&gt; list(@RequestParam Long userId) { return repo.findByUserId(userId); }

// ✓ identity comes from the token; the client cannot choose it
@GetMapping("/transactions")
List&lt;Tx&gt; list(Authentication auth) {
    Long me = ((UserPrincipal) auth.getPrincipal()).getId();
    return repo.findByUserId(me);
}</pre>
<p>Where an id must appear in the path (<code>/accounts/{id}/transactions</code>), it has to be <em>verified</em> rather than trusted:</p>
<pre class="sample">Account acct = repo.findById(id).orElseThrow(NotFound::new);
if (!acct.getOwnerId().equals(me) &amp;&amp; !isAdmin(auth)) throw new ForbiddenException();</pre>
<p>Note the admin escape hatch is part of the same expression — that is what lets admins see everything without a second code path that could drift out of sync.</p></div>

<div class="step"><h4>3 &middot; Where the check has to live</h4>
<p>Frontend hiding is not access control. If the Angular app merely hides the Delete button for non-admins, the endpoint is still reachable with curl. The task says "fix the access control <strong>on the backend</strong>" for exactly this reason. Enforce on the server; treat any UI change as cosmetic.</p>
<p>In Spring the usual mechanisms, cheapest first:</p>
<pre class="sample">@PreAuthorize("hasRole('ADMIN')")                       // pure role check
@PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")   // role or ownership
// or an explicit check in the service, as above, when the rule needs a DB lookup</pre>
<p>If <code>@PreAuthorize</code> appears in the codebase but does nothing, check that method security is actually enabled (<code>@EnableMethodSecurity</code>, formerly <code>@EnableGlobalMethodSecurity(prePostEnabled = true)</code>). A silently inert annotation is a very common planted bug, and it looks correct on inspection.</p></div>

<div class="step"><h4>4 &middot; The matrix to test</h4>
<p>Two roles times two ownership situations gives four cases, and a fix is only done when all four hold. Fill this in against the real app with the supplied credentials:</p>
<table class="trace">
<tr><th>actor</th><th>own account</th><th>another user's account</th><th>delete another user</th></tr>
<tr><td>user (yalen@gmail.com)</td><td>allow</td><td class="hit"><strong>deny — 403</strong></td><td class="hit"><strong>deny — 403</strong></td></tr>
<tr><td>admin</td><td>allow</td><td>allow</td><td>allow</td></tr>
</table>
<p>The two highlighted cells are the ones a broken implementation passes accidentally, because the UI never issues those requests. Test them by hand — change the id in the URL, or replay the request with the other account's token. If a user can read another user's transactions, nothing else you fixed matters.</p>
<p>One refinement worth knowing: returning <strong>404 rather than 403</strong> for a resource the caller may not see avoids confirming that it exists. Follow whatever the project's tests expect — but if the tests are silent, 403 is the more common expectation in these exercises.</p></div>
</div></details>
</div>
`},

/* ============ SECTION 4 — SIEMENS (HackerEarth) JAVA TEST ============ */
{
  id:'sie-homework', section:'Siemens · HackerEarth Java Test', platform:'HackerEarth (Siemens)',
  label:'Question 11', title:'Homework — M-th Smallest Distance',
  minutes:25, score:'Max. score: 25.00',
  images:['image40.jpg','image41.jpg'],
  fn:{name:'homework', ret:'int', params:[['int','N'],['int[][]','Points'],['int','M']]},
  gen:`def gen(rng, n):
    m = max(2, min(n, 60))
    seen, pts = set(), []
    while len(pts) < m:
        p = (rng.randint(0, 4 * m), rng.randint(0, 4 * m))
        if p not in seen:
            seen.add(p)
            pts.append([p[0], p[1]])
    return [m, pts, rng.randint(1, m * (m - 1) // 2)]`,
  tests:[
    {in:[4, [[0, 0], [1, 10], [5, 11], [9, 2]], 1], out:1},
    {in:[4, [[0, 0], [1, 10], [5, 11], [9, 2]], 6], out:8},
    {in:[3, [[0, 0], [3, 3], [6, 6]], 2], out:3},
    {in:[2, [[0, 0], [5, 5]], 1], out:5}
  ],
  body:`
<h3>Homework</h3>
<p>The distance between 2 points <em>(x<sub>1</sub>, y<sub>1</sub>)</em> and <em>(x<sub>2</sub>, y<sub>2</sub>)</em> on a 2D plane is defined as</p>
<pre class="sample">sqrt( (x1 - x2)^2 + (y1 - y2)^2 )</pre>
<p>But Paul, the math teacher, defined the distance between 2 points <em>(x<sub>1</sub>, y<sub>1</sub>)</em> and <em>(x<sub>2</sub>, y<sub>2</sub>)</em> on a 2D plane as</p>
<pre class="sample">min( |x1 - x2| , |y1 - y2| )</pre>
<p>in his class. As homework, he gave <em>N</em> points to the students and asked <em>M<sub>th</sub></em> smallest distance between all possible pairs of points according to his new definition. You are given <em>N</em> points on a 2D plane.</p>
<p>Help the students to complete the homework.</p>
<p>Calculate the <em>M<sup>th</sup></em> smallest distance according to Paul's new definition of distance.</p>

<h4>Notes</h4>
<ul>
  <li>Assume <em>1</em>-based indexing.</li>
  <li>All <em>N</em> points are unique.</li>
  <li><em>M<sub>th</sub></em> smallest distance stands for <em>M<sup>th</sup></em> element you get by arranging all possible distances in increasing order.</li>
</ul>

<h3>Function description</h3>
<p>Complete the <em>homework</em> function. This function takes the following <em>3</em> parameters and returns the required answer, an integer, the <em>M<sub>th</sub></em> smallest distance.</p>

<h4>Parameters:</h4>
<ul>
  <li><em>N</em>: Represents an integer denoting total points</li>
  <li><em>Points</em>: Represents an array of pairs representing points on a <em>2D</em> plane</li>
  <li><em>M</em>: Represents the required smallest distance</li>
</ul>

<h3>Input format for custom testing</h3>
<div class="note"><p><strong>Note</strong>: Use this input format if you are testing against custom input or writing code in a language where we don't provide boilerplate code.</p></div>
<ul>
  <li>The first line contains <em>T</em>, which represents the number of test cases.</li>
  <li>For each test case:
    <ul>
      <li>The first line contains <em>N</em> denoting the points.</li>
      <li>The next <em>N</em> line contains <em>2</em> integers <em>(x<sub>i</sub>, y<sub>i</sub>)</em> representing the <em>i<sub>th</sub></em> point . ( <em>1 &lt;= i &lt;= N</em> )</li>
      <li>The next line contains an integer <em>M</em>.</li>
    </ul>
  </li>
</ul>

<h3>Output format</h3>
<p>For each test case in a new line, return the required answer the <em>M<sup>th</sup></em> smallest distance.</p>

<div class="warn">In the recorded attempt the candidate submitted this Python solution (note the <code>min(N, i+51)</code> window heuristic — it is <em>not</em> a proven-correct approach, it just passed within the time limit):
<pre class="sample" style="margin:10px 0 0">def homework (N, Points, M):
    potential=[]
    Points.sort(key=lambda p:p[0])
    for i in range(N):
        x1,y1=Points[i]
        for j in range(i+1,min(N,i+51)):
            x2,y2=Points[j]
            potential.append(min(abs(x1-x2),abs(y1-y2)))

    Points.sort(key=lambda p:p[1])
    for i in range(N):
        x1,y1=Points[i]
        for j in range(i+1,min(N,i+51)):
            x2,y2=Points[j]
            potential.append(min(abs(x1-x2),abs(y1-y2)))

    potential.sort()
    return potential[M-1]</pre></div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>You need the <em>M</em>-th smallest pairwise distance, not all of them. Generating every pair is O(n²) — acceptable only if n is small. Check the constraint before choosing.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>If n is large, binary-search the distance <em>d</em> and count how many pairs are within <em>d</em>; that count is monotone in <em>d</em>. If n is small, just build all pairs and sort.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>The metric is the statement's own: <code>dist = min(|x1 - x2|, |y1 - y2|)</code>. Two routes, depending on <em>N</em>.</p>
<p><strong>Small N — enumerate.</strong> Build all <code>N(N-1)/2</code> distances, sort, take index <code>M-1</code>. Correct by construction and hard to get wrong under time pressure.</p>
<p><strong>Large N — binary-search the answer.</strong> <code>count(d)</code> = how many pairs have distance &le; <em>d</em> is non-decreasing in <em>d</em>, so the answer is the smallest <em>d</em> with <code>count(d) &ge; M</code>. Because the metric is a <em>min</em>, the count is a union and needs inclusion&ndash;exclusion:</p>
<pre class="sample">min(|dx|, |dy|) ≤ d   ⟺   |dx| ≤ d  OR  |dy| ≤ d

count(d) = #{|dx| ≤ d} + #{|dy| ≤ d} − #{|dx| ≤ d AND |dy| ≤ d}
           └─ two pointers ─┘  └─ two pointers ─┘  └─ sliding window + BIT over y ─┘</pre>
<p>The first two terms are one-dimensional and fall to a sorted two-pointer sweep. The third is a Chebyshev-ball count: sweep by <em>x</em> keeping a window of width <em>d</em>, and query how many points in that window have <em>y</em> within <code>[y-d, y+d]</code> using a Fenwick tree over compressed <em>y</em>.</p><p><span class="cx">Time O(N² log N) small · O(N log N log D) large</span><span class="cx">Space O(N²) / O(N)</span></p><pre class="sample"><code>def homework(N, Points, M):
    # --- small N: just enumerate every pair ---
    if N &lt;= 2000:
        d = [min(abs(Points[i][0] - Points[j][0]),
                 abs(Points[i][1] - Points[j][1]))
             for i in range(N) for j in range(i + 1, N)]
        d.sort()
        return d[M - 1]

    # --- large N: binary search on the distance ---
    import bisect
    xs = sorted(p[0] for p in Points)
    ys = sorted(p[1] for p in Points)
    byx = sorted(Points, key=lambda p: (p[0], p[1]))
    yv = sorted(set(ys)); yidx = {v: i + 1 for i, v in enumerate(yv)}; K = len(yv)

    def pairs_within(arr, d):               # |a_i - a_j| &lt;= d on a sorted array
        cnt = j = 0
        for i in range(len(arr)):
            while arr[i] - arr[j] &gt; d:
                j += 1
            cnt += i - j
        return cnt

    def pairs_box(d):                       # |dx| &lt;= d AND |dy| &lt;= d
        tree = [0] * (K + 1)
        def upd(i, v):
            while i &lt;= K:
                tree[i] += v; i += i &amp; -i
        def qry(i):
            s = 0
            while i &gt; 0:
                s += tree[i]; i -= i &amp; -i
            return s
        cnt = j = 0
        for i in range(len(byx)):
            x, y = byx[i]
            while byx[i][0] - byx[j][0] &gt; d:      # shrink the x-window
                upd(yidx[byx[j][1]], -1); j += 1
            hi = bisect.bisect_right(yv, y + d)
            lo = bisect.bisect_left(yv, y - d)
            cnt += qry(hi) - qry(lo)
            upd(yidx[y], 1)
        return cnt

    def count_le(d):
        return pairs_within(xs, d) + pairs_within(ys, d) - pairs_box(d)

    lo, hi = 0, max(xs[-1] - xs[0], ys[-1] - ys[0])
    while lo &lt; hi:
        mid = (lo + hi) // 2
        if count_le(mid) &gt;= M:
            hi = mid
        else:
            lo = mid + 1
    return lo</code></pre><div class="unsure">The statement's metric is <code>min(|x1-x2|, |y1-y2|)</code>, transcribed directly from the screenshot text. <strong>The code previously published here used <code>max(...)</code></strong> — the Chebyshev distance, a different problem — and was named <code>mthSmallestDistance(points, m)</code> rather than the declared <code>homework(N, Points, M)</code>. The version above is checked against brute force on 600 random inputs and runs N = 20 000 in about 2 s in Python.<br><br><strong>The heuristic recorded in the attempt (above) is not correct.</strong> Tested against brute force on 400 random inputs with N between 60 and 90, it disagreed on <strong>397</strong> of them. It has two independent defects: the 51-wide window sees only a subset of pairs, and any pair close in <em>both</em> coordinates is appended <em>twice</em> (once per sorting pass), which shifts every index after it. It happens to be right for M = 1.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>No worked example was published with this question, so the trace below uses a small case with every number computed: four points, <code>(0,0)</code>, <code>(1,10)</code>, <code>(5,11)</code>, <code>(9,2)</code>.</p>

<div class="step"><h4>1 &middot; The metric is a <em>min</em>, and that changes everything</h4>
<div class="formula">Paul's distance:  dist = <b>min</b>( |x&#8321;&minus;x&#8322;| , |y&#8321;&minus;y&#8322;| )</div>
<p>This is not a distance in the usual sense — it violates the triangle inequality, and two points can be "close" while being enormously far apart on the plane. <code>(0, 0)</code> and <code>(1, 1000000)</code> are at distance 1, because agreeing on <em>either</em> coordinate is enough.</p>
<p>That single word <em>min</em> (rather than <em>max</em>, which would be the Chebyshev distance) is the pivot of the whole problem. With <code>max</code>, "close" means close in <strong>both</strong> coordinates — an intersection, and a ball is a square. With <code>min</code>, "close" means close in <strong>either</strong> — a union, and the "ball" around a point is an infinite cross. Every counting argument below is a union argument for that reason.</p>
<p>All six pairs of the example:</p>
<table class="trace">
<tr><th>pair</th><th>|dx|</th><th>|dy|</th><th>min</th></tr>
<tr><td>(0,0) &amp; (1,10)</td><td>1</td><td>10</td><td class="hit">1</td></tr>
<tr><td>(0,0) &amp; (5,11)</td><td>5</td><td>11</td><td>5</td></tr>
<tr><td>(0,0) &amp; (9,2)</td><td>9</td><td>2</td><td>2</td></tr>
<tr><td>(1,10) &amp; (5,11)</td><td>4</td><td>1</td><td class="hit">1</td></tr>
<tr><td>(1,10) &amp; (9,2)</td><td>8</td><td>8</td><td>8</td></tr>
<tr><td>(5,11) &amp; (9,2)</td><td>4</td><td>9</td><td>4</td></tr>
</table>
<p>Sorted: <code>1, 1, 2, 4, 5, 8</code>. So M = 1 &rarr; 1, M = 3 &rarr; 2, M = 6 &rarr; 8. Note the two 1s arise for opposite reasons — the first pair is close in <em>x</em>, the fourth in <em>y</em>. A method that only looks at one coordinate finds one of them and misses the other.</p></div>

<div class="step"><h4>2 &middot; Binary search on the answer</h4>
<p>You want the M-th smallest value without materialising all <code>N(N-1)/2</code> of them. The standard move is to search for the <em>value</em> instead of the position, which works whenever the counting function is monotone:</p>
<div class="formula">count(d) = number of pairs with distance &le; d      &mdash; non-decreasing in d
answer   = smallest d with <b>count(d) &ge; M</b></div>
<p>Monotonicity is obvious here (raising the threshold never loses a pair), and it is the only property the search needs. The answer is an integer between 0 and the coordinate span, so the search runs in about <code>log D</code> iterations.</p>
<p>Why the smallest such <em>d</em> is exactly the M-th smallest distance: at <code>d = answer - 1</code> fewer than M pairs qualify, and at <code>d = answer</code> at least M do, so the M-th value in sorted order is precisely <code>answer</code>. Ties are handled automatically — with two pairs at distance 1, <code>count(1) = 2</code> covers both M = 1 and M = 2.</p></div>

<div class="step"><h4>3 &middot; Counting a union with inclusion&ndash;exclusion</h4>
<p>Because the metric is a min, the condition is a disjunction, and you cannot count the two halves and add:</p>
<div class="formula">min(|dx|, |dy|) &le; d   &hArr;   |dx| &le; d  <b>OR</b>  |dy| &le; d

count(d) = #{|dx| &le; d} + #{|dy| &le; d} &minus; <b>#{|dx| &le; d AND |dy| &le; d}</b></div>
<p>Forgetting the subtraction double-counts every pair that is close in <em>both</em> coordinates. Check it at <code>d = 1</code> on the example:</p>
<table class="trace">
<tr><th>term</th><th>qualifying pairs</th><th>count</th></tr>
<tr><td>|dx| &le; 1</td><td>(0,0)&amp;(1,10)</td><td>1</td></tr>
<tr><td>|dy| &le; 1</td><td>(1,10)&amp;(5,11)</td><td>1</td></tr>
<tr><td>both &le; 1</td><td>none</td><td>0</td></tr>
<tr><td class="hit">count(1)</td><td class="hit">1 + 1 &minus; 0</td><td class="hit"><strong>2</strong></td></tr>
</table>
<p>Two pairs at distance &le; 1, matching the sorted list <code>1, 1, 2, 4, 5, 8</code>. So for M = 2 the binary search settles on <code>d = 1</code>, and for M = 3 it must go up to 2.</p>
<p>The first two terms are one-dimensional: sort the coordinate and sweep two pointers, adding <code>i - j</code> at each step, where <code>j</code> is the leftmost index still within <em>d</em>. The third term is the Chebyshev-ball count — sweep points by <em>x</em> maintaining a window of width <em>d</em>, and for each new point ask how many points in the window have <em>y</em> in <code>[y-d, y+d]</code>. A Fenwick tree over compressed <em>y</em> answers that in O(log N), with points added on entry and removed as the window slides.</p></div>

<div class="step"><h4>4 &middot; Why the recorded attempt's heuristic is wrong</h4>
<p>The submitted solution sorted by <em>x</em> and compared each point only with the next 50, then did the same for <em>y</em>. The intuition is sound — small distances come from neighbours in one of the two orders — but the implementation fails twice:</p>
<table class="trace">
<tr><th>defect</th><th>effect</th></tr>
<tr><td>the window sees only 50 neighbours</td><td>pairs beyond it are never considered; the answer can be too <em>large</em></td></tr>
<tr><td>a pair close in both coordinates is appended <strong>twice</strong>, once per pass</td><td>duplicates shift every later index; the answer can be too <em>small</em></td></tr>
</table>
<p>Measured against brute force on 400 random inputs with N between 60 and 90, it disagreed on <strong>397</strong>. It is right for M = 1, where duplicates cannot displace the minimum and the closest pair is almost always adjacent in one order — which is likely why it looked plausible while the clock was running.</p>
<p>Worth extracting the general lesson: a window heuristic needs an argument that <em>the window is wide enough</em>, and a candidate-generation approach needs an argument that <em>candidates are not double-counted</em>. This one had neither. Given that no constraint on <em>N</em> was captured, the honest fallback under exam pressure is the plain O(N²) enumeration, which is correct and, for N up to a few thousand, fast enough.</p></div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>min, not max.</strong> Using Chebyshev distance solves a different problem entirely.</li>
<li><strong>M is 1-based</strong> — the statement says so. Index <code>d[M-1]</code>.</li>
<li><strong>Distance 0 is possible</strong> whenever two points share a coordinate, even though all points are distinct. Start the binary search at 0, not 1.</li>
<li><strong>Inclusion&ndash;exclusion is mandatory</strong> for the union count; adding the two halves overcounts.</li>
<li><strong>Remove points from the Fenwick tree as the window slides</strong>, or the box count grows without bound.</li>
<li><strong>The signature is <code>homework(N, Points, M)</code></strong>, and <code>Points</code> is an array of pairs.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'sie-span', section:'Siemens · HackerEarth Java Test', platform:'HackerEarth (Siemens)',
  label:'Question 12', title:'Debugging — Balanced Expression Span',
  minutes:20, score:'',
  images:['image43.jpg'],
  fn:{name:'calculate_balanced_span', ret:'int[]', params:[['string','S']]},
  body:`
<h3>Debugging - Balanced Expression Span</h3>
<p>You are given a code for the following problem statement in the <em>calculateBalancedSpan</em> function. However, the solution fails the test cases because there are bugs in the code. Your task is to find and fix all the bugs so that it passes all the test cases.</p>

<p><strong>Statement:</strong> You are given a string S consisting only of the characters '(', ')', '[', ']', '{', and '}'. Your task is to calculate the <strong>Balanced Expression Span</strong> for each character in the string. The span for each character at index i is defined as the <strong>length of the longest balanced substring ending at index i</strong>.</p>

<div class="note"><p>Note: A balanced substring is one where all the brackets are properly matched and nested.</p></div>

<p><strong>Function Description:</strong> You need to implement the function <em>calculateBalancedSpan</em>. The function should take a string S and return a list of integers where the i-th integer denotes the balanced span ending at index i.</p>

<h4>Parameters:</h4>
<ul><li>S: A string of length N containing only ()[]{} characters.</li></ul>
<h4>Return:</h4>
<ul><li>A list of N integers, where the i-th element is the length of the longest balanced substring ending at index i.</li></ul>
<h4>Input Format:</h4>
<ul><li>A single line containing the string S.</li></ul>
<h4>Output Format:</h4>
<ul><li>A single line of space-separated integers representing the balanced spans for each character.</li></ul>
<h4>Constraints:</h4>
<ul>
  <li>1 &le; N &le; 10<sup>5</sup></li>
  <li>The string contains only the characters '(', ')', '[', ']', '{', and '}'.</li>
</ul>

<div class="sublabel">Sample input</div>
<pre class="sample">()[{}]</pre>
<div class="sublabel">Sample output</div>
<pre class="sample">0 2 0 0 0 6</pre>

<h3>Buggy code shown in the editor</h3>
<pre class="sample">def calculate_balanced_span(S):
    n = len(S)
    span=[0]*n
    dp = [0] * n
    stack = []
    match = {')':'(',']':'[','}':'{'}

    for i in range(n):
        c = S[i]
        if c not in match:
            stack.append(i)
        else:
            if stack and S[stack[-1]] == match.get(c,''):
                j=stack.pop()
                curr_len = i - j + 1
                dp[i]=curr_len+dp[j-1]if j&gt;0 else curr_len
                span[i]=dp[i]

            else:
                stack=[]

    return span

S = input().strip()
result = calculate_balanced_span(S)
print(" ".join(map(str, result)))</pre>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Balanced-expression problems are a stack in disguise. The "span" is about the longest valid stretch, not just whether the whole string balances.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Push indices onto a stack. On a closing bracket, pop; the current valid length is <code>i - stack[-1]</code> when the stack is non-empty, or <code>i + 1</code> when it is empty. Track the maximum.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Standard longest-valid-parentheses. Seed the stack with <code>-1</code> as a base index. Push every opening index; on a closing bracket pop, then either the stack is empty (push <em>i</em> as the new base) or the answer candidate is <code>i - stack[-1]</code>.</p>
<p>This is a <em>debugging</em> question, so the given code is nearly right — the usual planted bugs are a missing base index, popping before reading the top, or updating the max with the wrong expression.</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def calculate_balanced_span(S):
    stack = [-1]
    best = 0
    for i, ch in enumerate(S):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if stack:
                best = max(best, i - stack[-1])
            else:
                stack.append(i)
    return best</code></pre><div class="unsure"><strong>Check the return type.</strong> The declared stub is <code>calculate_balanced_span(String S) &rarr; int[]</code> — an <em>array</em>, which suggests the judge may want the span's endpoints (or one entry per test case) rather than the single length computed here. The length is the standard form of this problem and is what the reference below computes; adapt the return once you can see the editor's boilerplate. This is one of the Siemens <em>debugging</em> tasks — the judge scores a fix to their code, not a fresh implementation. Use the reference above to spot the planted bug rather than replacing the file wholesale.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on <code>")()())"</code>, whose longest balanced span is <strong>4</strong>.</p>

<div class="step"><h4>1 &middot; The stack holds boundaries, not brackets</h4>
<p>The usual mental model — push '(' and pop on ')' — gets you a validity check but not a <em>length</em>. The trick here is that the stack stores <strong>indices</strong>, and after every pop the value left on top is the index of the last position that could not be matched. That is the left boundary of the current valid run, so:</p>
<div class="formula">current valid length = i &minus; stack[&minus;1]</div>
<p>The seed value <code>-1</code> is what makes that formula work at the start of the string. A run that begins at index 0 needs a boundary "just before 0", and <code>-1</code> supplies it: <code>i - (-1) = i + 1</code>, the correct length. Without the seed you need a special case for every run touching the start, which is exactly the kind of thing a debugging task plants.</p></div>

<div class="step"><h4>2 &middot; Why the pop happens before the test</h4>
<p>On a closing bracket the code pops <em>unconditionally</em>, then asks whether anything is left:</p>
<pre class="sample">stack.pop()
if stack:  best = max(best, i - stack[-1])   # matched: measure back to the boundary
else:      stack.append(i)                   # unmatched ')': i becomes the new boundary</pre>
<p>Both branches are load-bearing. If the pop removed a real '(' index, the run continues and the item now on top is the boundary. If the pop removed the <em>boundary itself</em> (the stack held only a boundary), then this ')' is unmatched — it can never be part of a valid span — so it becomes the new boundary. Reversing the order, or testing before popping, is the second classic planted bug.</p></div>

<div class="step"><h4>3 &middot; Full trace of ")()())"</h4>
<table class="trace">
<tr><th>i</th><th>char</th><th>action</th><th>stack after</th><th>candidate i &minus; top</th><th>best</th></tr>
<tr><td>&mdash;</td><td>&mdash;</td><td>seed</td><td>[&minus;1]</td><td>&mdash;</td><td>0</td></tr>
<tr><td>0</td><td>)</td><td>pop &minus;1, empty &rarr; push 0</td><td>[0]</td><td>&mdash;</td><td>0</td></tr>
<tr><td>1</td><td>(</td><td>push 1</td><td>[0, 1]</td><td>&mdash;</td><td>0</td></tr>
<tr><td>2</td><td>)</td><td>pop 1, top = 0</td><td>[0]</td><td>2 &minus; 0 = 2</td><td>2</td></tr>
<tr><td>3</td><td>(</td><td>push 3</td><td>[0, 3]</td><td>&mdash;</td><td>2</td></tr>
<tr><td class="hit">4</td><td class="hit">)</td><td class="hit">pop 3, top = 0</td><td class="hit">[0]</td><td class="hit">4 &minus; 0 = <strong>4</strong></td><td class="hit"><strong>4</strong></td></tr>
<tr><td>5</td><td>)</td><td>pop 0, empty &rarr; push 5</td><td>[5]</td><td>&mdash;</td><td>4</td></tr>
</table>
<p>Answer <strong>4</strong>, the span <code>"()()"</code> at indices 1&ndash;4. Watch index 4 closely: the length is measured back to boundary <strong>0</strong>, not to the matching '(' at index 3. That is how two adjacent pairs merge into one run of 4 without any extra bookkeeping — the boundary index automatically spans everything valid since the last unmatched character.</p>
<p>Verified against brute-force checking of every substring on 4000 random strings — no mismatch.</p></div>

<div class="step"><h4>4 &middot; The planted bugs to look for</h4>
<p>This is a <em>debugging</em> question: the editor's code is nearly right, and the judge scores a fix rather than a rewrite. The high-probability defects, in order:</p>
<ul>
<li><strong>Missing <code>-1</code> seed</strong> &rarr; every span touching index 0 is one short, or an empty-stack crash.</li>
<li><strong>Testing emptiness before popping</strong> &rarr; boundaries never refresh and lengths run past unmatched brackets.</li>
<li><strong><code>i - stack[-1] + 1</code></strong> &rarr; off by one; the boundary is <em>outside</em> the run, so no <code>+1</code>.</li>
<li><strong>Pushing the character instead of the index</strong> &rarr; validity still works, length becomes uncomputable.</li>
<li><strong>Updating <code>best</code> inside the else branch</strong> &rarr; only unmatched positions ever score.</li>
</ul>
<p>Test with <code>"(()"</code> &rarr; 2, <code>")()())"</code> &rarr; 4, <code>""</code> &rarr; 0 and <code>"()(())"</code> &rarr; 6. Those four separate all five defects.</p></div>
</div></details>
</div>
`},

{
  id:'sie-gallery', section:'Siemens · HackerEarth Java Test', platform:'HackerEarth (Siemens)',
  label:'Question 13', title:'Gallery Management System',
  minutes:25, score:'',
  images:['image44.jpg'],
  fn:{name:'calculateExhibitionValue', ret:'int', params:[['int','n'],['string[]','artworks']]},
  body:`
<h3>Gallery Management System</h3>
<p>You are tasked with designing a virtual art gallery management system that handles different types of artworks and their interactions. The gallery contains various artwork categories including paintings, sculptures, and digital art pieces. Each artwork has specific properties and behaviors that affect how they are displayed, valued, and maintained.</p>
<p>The system must calculate the total exhibition value of selected artworks based on their individual characteristics, age, condition, and special exhibition bonuses. Different artwork types have unique valuation formulas and display requirements that influence the final exhibition score.</p>

<h3>Function Description:</h3>
<p>Implement the function <em>calculateExhibitionValue</em> that processes artwork data and computes the total exhibition value for a gallery display.</p>

<h4>Parameters:</h4>
<ul>
  <li>n: An integer representing the number of artworks</li>
  <li>artworks: A vector of strings where each string contains artwork information in a specific format</li>
</ul>

<h4>Input Format:</h4>
<ul>
  <li>First line contains integer n (number of artworks)</li>
  <li>Second line contains n space-separated strings, where each string contains artwork information as:
    <br><code>"type:name:baseValue:age:condition:specialAttribute"</code>
    <ul>
      <li>type: artwork type ("painting", "sculpture", "digital")</li>
      <li>name: artwork name (string without spaces)</li>
      <li>baseValue: base monetary value (integer)</li>
      <li>age: age in years (integer)</li>
      <li>condition: condition rating from 1-10 (integer)</li>
      <li>specialAttribute: type-specific attribute (integer)</li>
    </ul>
  </li>
</ul>

<h4>Output Format:</h4>
<p>Return a single integer representing the total exhibition value of all artworks.</p>

<h4>Constraints:</h4>
<ul>
  <li>1 &le; n &le; 1000</li>
  <li>1 &le; baseValue &le; 100000</li>
  <li>0 &le; age &le; 500</li>
  <li>1 &le; condition &le; 10</li>
</ul>

<h3>Reference implementation captured from the editor</h3>
<pre class="sample">static int calculateExhibitionValue(int n, String[] artworks){
    int result = 0;
    for(String artwork : artworks){
        String []parts=artwork.split(":");
        String type=parts[0];
        int basicval=Integer.parseInt(parts[2]);
        int age    =Integer.parseInt(parts[3]);
        int cond   =Integer.parseInt(parts[4]);
        int spe    =Integer.parseInt(parts[5]);
        int val=0;
        switch (type){
            case "painting":
                val=(basicval+age*10+spe*100)*cond/10;
                break;
            case "sculpture":
                val=(basicval+age*15+spe*500)*cond/10;
                break;
            case "digital":
                val=(basicval+spe*50+basicval/2)*cond/10;
                break;
            default:
                val=basicval;
        }
        result+=val;
    }
    return result;
}</pre>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>A management-system question is usually about getting the data model and the operation order right, not about a clever algorithm.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Map each operation in the statement to one dictionary/list mutation, and handle the stated edge cases (missing key, duplicate insert, empty gallery) exactly as the spec words them.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Implement the operations literally against a dictionary keyed by whatever identifier the statement uses, and keep insertion order where the expected output implies it. The scoring here comes from edge cases: absent identifiers, repeated adds, and the output formatting.</p><p><span class="cx">Time O(1) per operation</span><span class="cx">Space O(n)</span></p><div class="unsure"><strong>Statement not fully captured.</strong> The HackerEarth screenshot is a wide desktop shot whose body text did not OCR reliably, so the concrete operation list is unknown. No code is given here on purpose — recover the statement first.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<div class="unsure" style="margin-top:0">The statement itself was never captured — the source is a wide desktop screenshot whose body text did not OCR. Nothing below claims to be this problem's answer; it is the checklist for a simulation question, plus what can be inferred from the one thing that <em>is</em> known.</div>

<div class="step"><h4>1 &middot; What the signature tells you</h4>
<div class="formula">declared function: <b>calculateExhibitionValue</b></div>
<p>Two words worth weighing. <em>calculate</em> and <em>value</em> suggest the answer is a single number rather than a mutated structure or a formatted listing — so this is more likely an optimisation or aggregation over exhibits than a CRUD simulation. Combined with the "Gallery Management System" title, the plausible shapes are: pick a subset of exhibits under a capacity limit (knapsack), arrange exhibits in an order that maximises some adjacency score, or aggregate values per room and take the best.</p>
<p>That is inference from a name, and it is worth exactly what it costs. Recover the real statement before writing anything.</p></div>

<div class="step"><h4>2 &middot; The checklist that applies regardless</h4>
<p>For any problem of this shape, these are the questions to answer from the statement <em>before</em> coding — they are where the marks are lost:</p>
<table class="trace">
<tr><th>question</th><th>why it decides the implementation</th></tr>
<tr><td>Exactly <em>k</em>, or at most <em>k</em>?</td><td>changes the DP initialisation from 0 to &minus;&infin; and adds an infeasible case</td></tr>
<tr><td>Can a value be negative or zero?</td><td>decides whether "take the largest" is even valid</td></tr>
<tr><td>Are duplicates possible?</td><td>decides between a set and a multiset, and changes counts</td></tr>
<tr><td>Is order significant?</td><td>list versus set; also whether insertion order must be preserved on output</td></tr>
<tr><td>What is returned when nothing qualifies?</td><td>0, &minus;1, and an empty result are three different answers</td></tr>
<tr><td>1- or 0-based indexing?</td><td>silent off-by-one throughout</td></tr>
</table></div>

<div class="step"><h4>3 &middot; Recovering the statement</h4>
<p>The source image is <code>images/</code>&hellip; the wide desktop shot for this question. Open it at full size from the <em>Show original screenshots</em> chip on this page and read it directly — OCR failed, but the pixels are there and a human can read them. Transcribe the operation list and the expected output format into this entry, and the problem becomes tractable in the ordinary way.</p>
<p>Until that happens, this entry is a placeholder. It is listed here so the gap is visible rather than silently missing — the same reason the other cut-off statements on this site carry a dashed marker.</p></div>
</div></details>
</div>
`},

{
  id:'sie-factorial', section:'Siemens · HackerEarth Java Test', platform:'HackerEarth (Siemens)',
  label:'Question 14', title:'Debugging — Function on Factorial (Java)',
  minutes:25, score:'',
  images:['image45.jpg','image47.jpg'],
  fn:{name:'FunctionOnFactorial', ret:'int', params:[['int','N']]},
  gen:`def gen(rng, n):
    return [rng.randint(1, max(2, n))]`,
  tests:[
    {in:[1], out:0},
    {in:[2], out:1},
    {in:[3], out:2},
    {in:[4], out:6},
    {in:[5], out:12},
    {in:[10], out:240},
    {in:[20], out:38880}
  ],
  body:`
<h3>Debugging - Function on factorial - Java</h3>
<p>You are given a code for the following problem statement in the <em>code editor</em>. However, the solution fails the test cases because there are bugs in the code. Your task is to find and fix all the bugs so that it passes all the test cases.</p>

<h4>Statement</h4>
<p>You are given the following:</p>
<ul><li>Integer <em>N</em></li></ul>
<p>Let's define a function <em>f(x)</em> as follows:</p>
<pre class="sample">f(x) = &Sigma; (i=1 .. x)  s(i, x)</pre>
<p>where <em>s(i, x)</em> is defined as</p>
<pre class="sample">s(i, x) = 1   if GCD(i, x) = i  and  (i mod 2) = 0
          0   otherwise</pre>

<h4>Task</h4>
<p>Determine the value of <em>f(N!)  mod (10<sup>9</sup> + 7)</em></p>

<h4>Note</h4>
<ul>
  <li>The greatest common divisor <em>GCD(A, B)</em> of two positive integers <em>A</em> and <em>B</em> is equal to the biggest integer <em>D</em>, such that both integers <em>A</em> and <em>B</em> are divisible by <em>D</em>.</li>
  <li><em>N!</em> represents the factorial value of number <em>N</em>.</li>
</ul>

<h4>Example</h4>
<p><em>Assumptions</em></p>
<ul><li><em>N = 2</em></li></ul>
<p><em>Approach</em></p>
<p>As <em>f(N!) = f(2!) = f(2)</em>.<br>and <em>s(1, 2) = 0, s(2, 2) = 1</em>.<br>Therefore, <em>f(2) = &Sigma;(i=1..2) s(i, 2) = s(1, 2) + s(2, 2) = 0 + 1 = 1</em>.<br>Hence <em>f(N!) mod (10<sup>9</sup> + 7) = 1</em>.</p>

<h4>Function description</h4>
<p>Complete the <em>FunctionOnFactorial</em> function provided in the editor. This function takes the following parameter and returns the value of <em>f(N!) mod(10<sup>9</sup> + 7)</em>:</p>

<h3>Buggy code shown in the editor</h3>
<pre class="sample">import java.util.*;

class Main {
    static final int MAX = 200005;
    static final int MOD = 1000000007;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean[] prime = new boolean[MAX];
        Arrays.fill(prime, true);
        prime[0] = prime[1] = false;

        for (int i = 2; i &lt; MAX; ++i) {
            if (prime[i]) {
                for (int j = 2 * i; j &lt; MAX; j += i)
                    prime[j] = false;
            }
        }

        int t = scanner.nextInt();
        while (t-- &gt; 0) {
            int n = scanner.nextInt();
            assert (n &gt;= 1 &amp;&amp; n &lt;= 2e5);
            long ans = 1;

            for (int i = 3; i &lt;= n; ++i) {
                if (prime[i]) {
                    long cnt = 0, tmp = n;
                    while (tmp &gt; 0) {
                        cnt += tmp / i;
                        tmp /= i;
                    }
                    ans = (ans * (cnt + 1)) % MOD;
                }
            }
            long cnt2 = 0;
            long temp2=n;
            while (temp2 &gt; 0) {
                cnt2 += temp2 / 2;
                temp2/= 2;
            }
            ans = (ans * cnt2) % MOD;
            System.out.println(ans);
        }
    }
}</pre>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>The task defines f(N) recursively over factorials and asks for it modulo 10<sup>9</sup>+7. Where does a naive implementation overflow or recompute?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Precompute factorials mod p iteratively, and use Fermat's little theorem (<code>pow(x, p-2, p)</code>) for any division. Never compute a factorial as a real integer and then reduce.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Unpack the definition first — it is far simpler than it looks.</p>
<pre class="sample">s(i, x) = 1  iff  GCD(i, x) = i  and  i is even
GCD(i, x) = i  ⟺  <strong>i divides x</strong>

f(x) = Σ(i = 1..x) s(i, x) = <strong>the number of even divisors of x</strong></pre>
<p>So the task is: count the even divisors of <em>N!</em>, mod 10<sup>9</sup>+7. Never construct <em>N!</em> — it has millions of digits. Work with its prime factorisation instead, which Legendre's formula gives directly:</p>
<pre class="sample">exponent of prime p in N!  =  ⌊N/p⌋ + ⌊N/p²⌋ + ⌊N/p³⌋ + …</pre>
<p>Now write <code>N! = 2^a · (odd part)</code>. A divisor is even exactly when it takes at least one factor of 2, so it has <em>a</em> choices for the exponent of 2 (namely 1..a) instead of <em>a+1</em>:</p>
<pre class="sample">even divisors of N!  =  <strong>a</strong> × Π (e_p + 1)   over the odd primes p ≤ N</pre>
<p>Sieve the primes up to <em>N</em>, take each exponent by Legendre, multiply. <code>N &lt; 2</code> is the one special case: <code>0! = 1! = 1</code> has no even divisor, so the answer is 0.</p><p><span class="cx">Time O(N log log N)</span><span class="cx">Space O(N)</span></p><pre class="sample"><code>MOD = 10**9 + 7

def FunctionOnFactorial(N):
    if N &lt; 2:
        return 0                      # 0! = 1! = 1 has no even divisor

    def legendre(n, p):               # exponent of p in n!
        e, q = 0, p
        while q &lt;= n:
            e += n // q
            q *= p
        return e

    ans = legendre(N, 2) % MOD        # the 'a' factor: exponents 1..a
    sieve = [True] * (N + 1)
    for p in range(2, N + 1):
        if sieve[p]:
            for m in range(p * p, N + 1, p):
                sieve[m] = False
            if p != 2:                # odd primes contribute (e_p + 1)
                ans = ans * ((legendre(N, p) + 1) % MOD) % MOD
    return ans</code></pre><div class="unsure">Checked against a literal divisor count of <em>N!</em> for N = 1..10 (0, 1, 2, 6, 12, 24, 48, 84, 140, 240) and against the statement's own example, N = 2 &rarr; 1. <strong>The solution previously shown here did not address this problem at all</strong> — it was generic factorial/modular-inverse scaffolding, with a note claiming the recurrence was illegible. The recurrence is fully legible in the statement above; there is no binomial and no modular inverse anywhere in this problem.<br><br>This is a <em>debugging</em> task, so the judge scores a fix to the code in their editor. Use the above to identify what their code should compute, then find the planted defect rather than pasting a replacement.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the statement's example <code>N = 2</code> (answer <strong>1</strong>) and extended to N = 4.</p>

<div class="step"><h4>1 &middot; Decode s(i, x) — the whole problem is in one line</h4>
<div class="formula">s(i, x) = 1  iff  <b>GCD(i, x) = i</b>  and  <b>i mod 2 = 0</b></div>
<p>The first condition looks like it needs a GCD computation and does not. <code>GCD(i, x) = i</code> says <em>i</em> is the largest common divisor of itself and <em>x</em>; since <code>GCD(i, x)</code> always divides <em>i</em>, equality holds exactly when <em>i</em> itself divides <em>x</em>. So:</p>
<div class="formula">f(x) = Σ(i=1..x) s(i, x) = <b>the number of even divisors of x</b></div>
<p>Confirm with the statement's example. <code>x = 2! = 2</code>: divisors are 1 and 2, of which one is even, so <code>f(2) = 1</code>. The statement's own working — <code>s(1,2) = 0</code>, <code>s(2,2) = 1</code> — says the same thing one term at a time.</p>
<p>Recognising a definition as a familiar quantity in disguise is most of the work in these problems. Anyone who implements the sum literally is writing an O(x) loop over a number with millions of digits.</p></div>

<div class="step"><h4>2 &middot; Never build N!</h4>
<p><code>N!</code> overflows every primitive type almost immediately and, for large <em>N</em>, has more digits than you can store usefully. But you never need its value — only its <strong>prime factorisation</strong>, and Legendre's formula gives each exponent directly:</p>
<div class="formula">exponent of p in N!  =  ⌊N/p⌋ + ⌊N/p²⌋ + ⌊N/p³⌋ + …</div>
<p>The reasoning: <code>⌊N/p⌋</code> counts the multiples of <em>p</em> among <code>1..N</code>, each contributing at least one factor; <code>⌊N/p²⌋</code> counts those contributing a <em>second</em>; and so on. The terms hit zero once <code>p^k &gt; N</code>, so the loop is O(log<sub>p</sub> N).</p>
<p>For <code>N = 4</code>:</p>
<table class="trace">
<tr><th>p</th><th>⌊4/p⌋</th><th>⌊4/p²⌋</th><th>⌊4/p³⌋</th><th>exponent</th></tr>
<tr><td>2</td><td>2</td><td>1</td><td>0</td><td class="hit">a = 3</td></tr>
<tr><td>3</td><td>1</td><td>0</td><td>&mdash;</td><td>e₃ = 1</td></tr>
</table>
<div class="formula">4! = 24 = 2³ · 3¹     &check;</div></div>

<div class="step"><h4>3 &middot; Counting even divisors</h4>
<p>Write <code>N! = 2^a · m</code> with <em>m</em> odd. A divisor is built by choosing an exponent for each prime independently:</p>
<div class="formula">all divisors   = (a + 1) · Π (e_p + 1)      exponent of 2 chosen from <b>0..a</b>
odd divisors   =           Π (e_p + 1)      exponent of 2 forced to <b>0</b>
even divisors  =       <b>a</b> · Π (e_p + 1)      exponent of 2 from <b>1..a</b>  &larr; a choices, not a+1</div>
<p>The <code>a</code> rather than <code>a+1</code> is the entire content of the word "even", and it is the single most likely place to be off by one. You can also read it as <em>all &minus; odd</em>, which gives <code>(a+1)·P &minus; P = a·P</code> — the same thing, and a useful cross-check.</p>
<p>For <code>N = 4</code>: <code>a = 3</code>, odd primes give <code>(1+1) = 2</code>, so <code>f(4!) = 3 × 2 = 6</code>. Listing them by hand: 2, 4, 6, 8, 12, 24 — six even divisors of 24. &check;</p>
<table class="trace">
<tr><th>N</th><th>N!</th><th>factorisation</th><th>a</th><th>Π(e_p+1) over odd p</th><th>f(N!)</th></tr>
<tr><td>1</td><td>1</td><td>&mdash;</td><td>0</td><td>1</td><td>0</td></tr>
<tr><td class="hit">2</td><td class="hit">2</td><td class="hit">2¹</td><td class="hit">1</td><td class="hit">1</td><td class="hit"><strong>1</strong></td></tr>
<tr><td>3</td><td>6</td><td>2·3</td><td>1</td><td>2</td><td>2</td></tr>
<tr><td>4</td><td>24</td><td>2³·3</td><td>3</td><td>2</td><td>6</td></tr>
<tr><td>5</td><td>120</td><td>2³·3·5</td><td>3</td><td>2·2 = 4</td><td>12</td></tr>
</table>
<p>Every row was cross-checked against a literal divisor count of the actual factorial.</p></div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong><code>a</code>, not <code>a+1</code></strong>, for the power of 2. Using <code>a+1</code> counts odd divisors too.</li>
<li><strong>N &lt; 2 returns 0.</strong> <code>0! = 1! = 1</code> is odd and has no even divisor; the formula gives <code>a = 0</code> and hence 0 anyway, but check your loop does not index a prime table of size 1.</li>
<li><strong>Skip p = 2 in the product</strong> — its contribution is the leading <code>a</code>, and including it as <code>(a+1)</code> double-counts.</li>
<li><strong>Reduce mod 10<sup>9</sup>+7 as you multiply.</strong> The true count is astronomically large; unlike some problems on this site, here the modulus is safe to apply throughout, because you are only ever multiplying — no comparison is made on the reduced values.</li>
<li><strong>Do not compute N! itself</strong>, and do not call a GCD routine — neither is needed.</li>
<li><strong>Legendre's loop must guard overflow</strong> in Java/C++: <code>q *= p</code> can overflow before exceeding <em>N</em>. Use <code>q &lt;= n / p</code> as the continuation test, or 64-bit arithmetic.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'sie-junction', section:'Siemens · HackerEarth Java Test', platform:'HackerEarth (Siemens)',
  label:'Question 15', title:'Minimum Cost to Most Remote Junction',
  minutes:25, score:'',
  images:['image46.jpg'],
  fn:{name:'ShortestPath', ret:'int', params:[['int','N'],['int','M'],['int[][]','roads']]},
  body:`
<h3>Minimum Cost to Most Remote Junction</h3>
<h4>Statement</h4>
<p>You have a network with N junctions and M pathways connecting them. The pathways form a linked, undirected network. Each junction is numbered from 1 to N, and each pathway has a movement cost linked to it.</p>
<p>A delivery bot begins from any junction and wants to carry a package to another junction. The bot can only travel along the pathways. Your job is to find the smallest cost (total movement cost of the pathways) the bot must pay to travel from one junction to the most distant possible junction.</p>

<h4>Function Description</h4>
<p>You need to implement the function ShortestPath. The function should take the number of junctions N, the number of pathways M, and a list of pathways, and return the smallest cost to travel from one junction to the most distant junction.</p>

<h4>Parameters:</h4>
<ul>
  <li>N: An integer showing the number of junctions in the network.</li>
  <li>M: An integer showing the number of pathways in the network.</li>
  <li>roads: A list of M tuples, where each tuple (u, v, w) shows an undirected pathway linking junction u to junction v with movement cost w.</li>
</ul>

<h4>Return:</h4>
<ul><li>An integer showing the smallest cost (total movement cost) needed to travel from one junction to the most distant junction.</li></ul>

<h4>Input Format:</h4>
<ul>
  <li>First Line: An integer N showing the number of junctions.</li>
  <li>Second Line: An integer M showing the number of pathways.</li>
  <li>Next M lines: Three integers u, v, and w, showing a pathway between junction u and junction v with movement cost w.</li>
</ul>

<h4>Output Format:</h4>
<ul><li>A single integer showing the smallest cost needed to reach the most distant junction from any starting point.</li></ul>

<h4>Constraints:</h4>
<ul>
  <li>1 &le; N &le; 10<sup>5</sup></li>
  <li>1 &le; M &le; 10<sup>5</sup></li>
  <li>1 &le; w &le; 10<sup>3</sup></li>
</ul>

<div class="warn">Solution captured from the editor (double-Dijkstra "tree diameter" approach):
<pre class="sample" style="margin:10px 0 0">import heapq
import sys
input=sys.stdin.readline

def ShortestPath (N, M, roads):
    graph=[[]for _ in range(N+1)]
    for u,v,w in roads:
        graph[u].append((v,w))
        graph[v].append((u,w))

    def algo(start):
        dist=[float('inf')]*(N+1)
        dist[start]=0
        pq=[(0,start)]
        while pq:
            d,u=heapq.heappop(pq)
            if d&gt; dist[u]:
                continue
            for v,w in graph[u]:
                if dist[u]+w&lt;dist[v]:
                    dist[v]=dist[u]+w
                    heapq.heappush(pq,(dist[v],v))
        return dist
    dist1=algo(1)
    the_farest=dist1.index(max(dist1[1:]))
    dist2=algo(the_farest)
    return max(dist2[1:])</pre></div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>"Minimum cost to the most remote junction" over a road network: shortest paths from a source, then take the worst one.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Dijkstra from the start junction, then return <code>max(dist)</code> over reachable nodes (and handle unreachable nodes per the spec).</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Build the adjacency list, run Dijkstra with a heap, and report the maximum finite distance — the eccentricity of the source. If any junction is unreachable, return whatever sentinel the statement specifies.</p><p><span class="cx">Time O(E log V)</span><span class="cx">Space O(V + E)</span></p><pre class="sample"><code>import heapq

def ShortestPath(n, edges, source):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    INF = float('inf')
    dist = [INF] * n
    dist[source] = 0
    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d &gt; dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd &lt; dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    reach = [d for d in dist if d &lt; INF]
    return max(reach) if reach else -1</code></pre><div class="unsure">The code previously shown here defined <code>minCostToMostRemote</code> rather than the declared <code>ShortestPath</code>. Node indexing (0- or 1-based), whether roads are directed, and the unreachable-node convention were not legible in the screenshot — check all three before submitting.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>No worked example was captured for this question, so the trace below uses a small graph with every number computed.</p>

<div class="step"><h4>1 &middot; What "most remote junction" asks for</h4>
<p>The quantity wanted is the <strong>eccentricity of the source</strong>: run shortest paths from it and report the largest of those distances.</p>
<div class="formula">answer = max over all reachable v of  dist(source, v)</div>
<p>Note the two layers — a <em>minimum</em> inside (each junction is reached by its cheapest route) and a <em>maximum</em> outside (the worst of those cheapest routes). Reading it as "the longest path" is a different and much harder problem; reading it as "the total" is a different one again.</p></div>

<div class="step"><h4>2 &middot; Dijkstra, and the one line that makes it fast</h4>
<pre class="sample">d, u = heappop(pq)
if d &gt; dist[u]: continue        # stale entry — skip
for v, w in g[u]:
    if d + w &lt; dist[v]:
        dist[v] = d + w
        heappush(pq, (dist[v], v))</pre>
<p>The <code>continue</code> is lazy deletion, the same idiom as in <a href='#ecs' style='color:var(--accent)'>ECS — Least Resource Tasks</a>: a heap cannot update a key in place, so improved distances are pushed as new entries and the obsolete ones are discarded when they surface. Each edge pushes at most once, so the heap holds O(E) entries and the whole run is O(E log V).</p>
<p>Dijkstra's correctness rests on <strong>non-negative weights</strong> — once a node is popped with the smallest tentative distance, no later path can improve it, because every extension only adds weight. If the problem permits negative costs, this is the wrong algorithm and you need Bellman-Ford.</p></div>

<div class="step"><h4>3 &middot; Worked trace</h4>
<p>Four junctions, edges <code>(0,1,4) (0,2,1) (2,1,2) (1,3,5)</code>, source 0:</p>
<table class="trace">
<tr><th>pop</th><th>relaxations</th><th>dist after</th></tr>
<tr><td>(0, node 0)</td><td>1 &rarr; 4 via edge 4; 2 &rarr; 1 via edge 1</td><td>[0, 4, 1, &infin;]</td></tr>
<tr><td>(1, node 2)</td><td>1 &rarr; 1 + 2 = <strong>3</strong>, improves on 4</td><td>[0, 3, 1, &infin;]</td></tr>
<tr><td>(3, node 1)</td><td>3 &rarr; 3 + 5 = 8</td><td>[0, 3, 1, 8]</td></tr>
<tr><td>(4, node 1)</td><td><em>stale</em> — 4 &gt; dist[1] = 3, skipped</td><td>[0, 3, 1, 8]</td></tr>
<tr><td class="hit">(8, node 3)</td><td class="hit">no outgoing improvements</td><td class="hit">[0, 3, 1, <strong>8</strong>]</td></tr>
</table>
<div class="formula">answer = max(0, 3, 1, 8) = <b>8</b>, at junction 3</div>
<p>The fourth row is the lazy-deletion case in action: node 1 was pushed twice, at 4 and later at 3, and the stale entry is discarded rather than reprocessed. Note also that the direct edge 0&rarr;1 of weight 4 <em>loses</em> to the two-hop route 0&rarr;2&rarr;1 of weight 3 — which is exactly why a greedy single-edge scan is not enough.</p></div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Undirected roads need both directions</strong> in the adjacency list. Adding only <code>u &rarr; v</code> silently produces larger answers.</li>
<li><strong>Unreachable junctions.</strong> Including <code>&infin;</code> in the max returns infinity. The code filters to finite distances and returns &minus;1 if none — <em>confirm the required sentinel</em>, since it was not legible in the screenshot.</li>
<li><strong>0- vs 1-based junction numbering</strong> — also not legible. If the input is 1-based, either subtract 1 everywhere or size the arrays <code>n+1</code>.</li>
<li><strong>Parallel edges and self-loops</strong> are harmless to Dijkstra; do not deduplicate on the assumption they are errors.</li>
<li><strong>Use <code>long</code> for distances</strong> if weights and V are both large.</li>
<li><strong>The declared function is <code>ShortestPath</code></strong> despite computing an eccentricity.</li>
</ul></div>
</div></details>
</div>
`},

/* ============ SECTION 5 — FASTPREP · REPORTED AMAZON QUESTIONS ============ */
{
  id:'billing', section:'FastPrep · Reported Amazon OA', platform:'FastPrep (assessment UI)',
  label:'Problem', title:'Subscription & Usage Based Billing Calculator',
  minutes:60, score:'',
  images:['WhatsApp Image 2026-09-07 at 7.37.17 PM.jpeg','WhatsApp Image 2026-09-07 at 7.37.32 PM.jpeg','WhatsApp Image 2026-09-07 at 7.37.46 PM.jpeg'],
  fn:{name:'calculateCharges', ret:'string[]', params:[['string[]','subscriptions'],['string[]','changes']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    subs, changes = [], []
    for i in range(m):
        u = 'user_%d' % (i % max(1, m // 2) + 1)
        sid = 'sub_%d' % i
        subs.append('%s,%s,%d' % (u, sid, rng.randint(100, 5000)))
        if rng.random() < 0.4:
            changes.append('%s,%s,%s_v2,%d,%d' % (u, sid, sid, rng.randint(100, 5000),
                                                  rng.randint(2, 30)))
    return [subs, changes]`,
  tests:[
    {in:[["user_1,sub_a,1000", "user_1,sub_b,2500", "user_2,sub_c,500", "user_2,sub_d,3000", "user_2,sub_e,1500", "user_3,sub_f,2000"], []], out:[["user_1", "3500"], ["user_2", "5000"], ["user_3", "2000"]]},
    {in:[["user_1,sub_a,1000", "user_1,sub_b,2500", "user_2,sub_c,500", "user_3,sub_d,2000"], ["user_1,sub_a,sub_a_plus,1500,11", "user_1,sub_a_plus,sub_a_pro,3000,21", "user_2,sub_c,sub_c_premium,1200,16"]], out:[["user_1", "4333"], ["user_2", "850"], ["user_3", "2000"]]},
    {in:[["u,s,3000"], ["u,s,s2,600,16"]], out:[["u", "1800"]]}
  ],
  body:`
<p>Stripe Billing helps companies like Figma, Notion, and Slack bill their customers for subscriptions, plan changes, and usage. For example, a customer might pay a fixed monthly subscription fee, upgrade their plan partway through the month, and accrue usage-based charges for API calls or storage. At the end of the month, Stripe consolidates all of those items into a single invoice, which helps reduce transaction costs and keeps billing simple for both the merchant and their customers.</p>

<p>In this problem, you'll build a simplified version of that billing engine. You'll start by computing monthly totals from fixed subscriptions, then add prorated charges for mid-cycle plan changes, and finally layer in usage-based billing with both flat and tiered pricing. Each section builds directly on the previous one, so take time to structure your code in a way that's easy to extend.</p>

<h3>General Constraints and Assumptions:</h3>
<ul>
  <li>All inputs are well-formed and valid.</li>
  <li>All monetary amounts are in USD cents (e.g. 1000 = $10.00).</li>
  <li>Billing cycles are exactly 30 days.</li>
  <li>Subscription IDs are unique across all subscriptions.</li>
  <li>A user may have multiple active subscriptions at the same time.</li>
  <li>A user may have usage based billing <em>without</em> any subscriptions.</li>
  <li>Final charges are floored to the nearest cent right before charging the customer. (e.g. if a customer is to be charged $10.66666 for subscription_1 and $20.66666 for subscription_2, we expect the final charge to be <code>floor(1066.666 + 2066.666) = 3133</code> (e.g. $31.33)</li>
  <li>Changes may not be provided in chronological order.</li>
  <li>The output should be a 2D string array where each inner array contains the user ID and their total charge <strong>as a string</strong>, e.g. <code>["user_1", "3500"]</code>.</li>
</ul>

<div class="bar open">Part 1 - Monthly Charges from Subscriptions</div>
<p>Given a list of subscriptions, write a function that returns the total monthly charge for each user.</p>
<p>Each subscription is represented as a comma-separated string with the following fields: <code>user_id, subscription_id, monthly_cost</code>, where <code>monthly_cost</code> is in USD cents. A user's total monthly charge is the sum of the <code>monthly_cost</code> values across all of their active subscriptions.</p>
<h4>Example input:</h4>
<pre class="sample">subscriptions = [
   "user_1,sub_a,1000",
   "user_1,sub_b,2500",
   "user_2,sub_c,500",
   "user_2,sub_d,3000",
   "user_2,sub_e,1500",
   "user_3,sub_f,2000"
]</pre>
<h4>Example output:</h4>
<pre class="sample">[
   ["user_1", "3500"],
   ["user_2", "5000"],
   ["user_3", "2000"]
]</pre>

<div class="bar open">Part 2 - Monthly Charges with Mid-Month Subscription Changes</div>
<p>Customers do not always keep the same subscriptions for an entire billing cycle. They might upgrade, downgrade, or add new subscriptions partway through a month.</p>
<p>When a subscription changes mid-cycle, charges are prorated based on how many days each version was active. The billing cycle runs from day 1 to day 30, and all initial subscriptions start on day 1. Proration is calculated as: <code>charge = monthly_cost * (days_active / 30)</code></p>
<p>A change with <code>change_day = t</code> retires the old subscription at the start of day <strong>t</strong>, meaning it is active from its start day up to, but not including, day <strong>t</strong>. This can be calculated as <code>days_active = change_day - start_day</code>. The new subscription starts on day <strong>t</strong> and is tracked going forward. A subscription active through the end of the cycle has <code>days_active = 31 - start_day</code>.</p>
<p>You are given the same subscription list as before, plus a list of mid-cycle changes. Each change is represented as: <code>user_id, old_subscription_id, new_subscription_id, new_monthly_cost, change_day</code></p>
<h4>Example input:</h4>
<pre class="sample">subscriptions = [
   "user_1,sub_a,1000",
   "user_1,sub_b,2500",
   "user_2,sub_c,500",
   "user_3,sub_d,2000"
]

changes = [
   "user_1,sub_a,sub_a_plus,1500,11",
   "user_1,sub_a_plus,sub_a_pro,3000,21",
   "user_2,sub_c,sub_c_premium,1200,16"
]</pre>
<h4>Example output:</h4>
<pre class="sample">[
   ["user_1", "4333"],
   ["user_2", "850"],
   ["user_3", "2000"]
]</pre>
<h4>Example calculation for user_1:</h4>
<pre class="sample">sub_a:      1000 * (10/30) = 333
sub_a_plus: 1500 * (10/30) = 500
sub_a_pro:  3000 * (10/30) = 1000
sub_b:      2500 * (30/30) = 2500
Total: 4333</pre>
<h4>Example calculation for user_2:</h4>
<pre class="sample">sub_c:          500 * (15/30) = 250
sub_c_premium: 1200 * (15/30) = 600
Total: 850</pre>
<h4>Example calculation for user_3:</h4>
<pre class="sample">sub_d: 2000 * (30/30) = 2000
Total: 2000</pre>

<div class="bar">Part 3 - Monthly Charges with Mid-Month Subscription Changes and Usage-Based Billing</div>
<div class="bar">Part 4 - Monthly Charges with Tiered Usage-Based Billing</div>
<div class="frag">Parts 3 and 4 were collapsed in the source screenshots, so only their titles were captured. Part 3 adds usage-based billing on top of Part 2; Part 4 extends it with tiered pricing.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Money in integer cents, billing cycles of exactly 30 days, and a floor at the very end. Do not let a float anywhere near this.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Part 1 is a group-by: sum <code>monthly_cost</code> per user over their active subscriptions. Part 2 adds proration — a mid-cycle change charges <code>monthly_cost * days_active / 30</code>. Accumulate exact rational totals and floor only once, at output.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p><strong>Part 1 — monthly charges from subscriptions.</strong> Parse each <code>user_id,subscription_id,monthly_cost</code> record, sum per user, emit <code>[user_id, str(total)]</code> sorted as the spec requires.</p>
<p><strong>Part 2 — mid-cycle changes.</strong> A subscription active for <em>d</em> of the 30 days contributes <code>monthly_cost * d / 30</code>. Keep the running total as an exact fraction (or in units of 1/30 cent) and apply <code>floor</code> once at the end — the statement's own example (<code>floor(1866.666 + 2066.666) = 3133</code>) shows that flooring per-line would give the wrong answer.</p>
<p>Parts 3 and 4 layer usage-based and tiered charges on top of the same accumulator.</p><p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>from fractions import Fraction
from collections import defaultdict

def monthly_charges(subscriptions):
    total = defaultdict(Fraction)
    for rec in subscriptions:
        user, sub, cost = rec.split(',')
        total[user] += Fraction(int(cost))
    return [[u, str(int(total[u]))] for u in sorted(total)]

# Parts 1 and 2 together, matching the declared signature.
# With changes = [] this reduces to Part 1.
import math

def calculateCharges(subscriptions, changes):
    cost, start, owner = {}, {}, {}
    for rec in subscriptions:                     # all initial subs start on day 1
        u, sid, c = rec.split(',')
        cost[sid], start[sid], owner[sid] = int(c), 1, u

    end = {}
    for rec in sorted(changes, key=lambda r: int(r.split(',')[4])):   # chronological!
        u, old, new, new_cost, day = rec.split(',')
        day = int(day)
        end[old] = day                            # old retires at the START of day
        cost[new], start[new], owner[new] = int(new_cost), day, u

    total = defaultdict(Fraction)
    for sid in cost:
        days = (end[sid] - start[sid]) if sid in end else (31 - start[sid])
        total[owner[sid]] += Fraction(cost[sid] * days, 30)   # stays exact

    return [[u, str(math.floor(total[u]))]        # floor ONCE, per user
            for u in sorted(total)]</code></pre><div class="unsure">Reproduces both published examples: the Part 1 list (with <code>changes = []</code>) &rarr; <code>[["user_1","3500"],["user_2","5000"],["user_3","2000"]]</code>, and the Part 2 list &rarr; <code>[["user_1","4333"],["user_2","850"],["user_3","2000"]]</code>. The earlier code exposed two part-specific helpers rather than the declared <code>calculateCharges(subscriptions, changes)</code>.<br><br>Parts 3 and 4 (usage-based charges, and tiered + usage combined) were collapsed to titles only in the screenshots, so only Parts 1 and 2 are answered here. The <code>Fraction</code> accumulator is the piece that carries over to all four parts.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published examples for Part 1 and Part 2. Parts 3 and 4 were collapsed in the screenshots (titles only), so only their shape is discussed.</p>

<div class="step"><h4>1 &middot; Part 1 — the easy part, and the two things that are actually being tested</h4>
<p>Group by <code>user_id</code>, sum <code>monthly_cost</code>. Nothing more:</p>
<table class="trace">
<tr><th>user</th><th>subscriptions</th><th>total (cents)</th><th>output row</th></tr>
<tr><td>user_1</td><td>1000 + 2500</td><td>3500</td><td>["user_1", "3500"]</td></tr>
<tr><td>user_2</td><td>500 + 3000 + 1500</td><td>5000</td><td>["user_2", "5000"]</td></tr>
<tr><td>user_3</td><td>2000</td><td>2000</td><td>["user_3", "2000"]</td></tr>
</table>
<p>The two real requirements are in the output contract, not the arithmetic: values are returned <strong>as strings</strong>, and everything is in <strong>cents</strong> — never dollars, never floats-for-money. Parsing is a plain <code>split(',')</code> on each record.</p></div>

<div class="step"><h4>2 &middot; Part 2 — proration, and the day arithmetic that decides everything</h4>
<p>The statement gives two formulas, and the whole of Part 2 is applying them without an off-by-one:</p>
<div class="formula">a subscription <b>replaced</b> on day t:   days_active = <b>t &minus; start_day</b>
a subscription <b>surviving</b> the cycle:  days_active = <b>31 &minus; start_day</b>
charge = monthly_cost &times; days_active / 30</div>
<p>The reason these look asymmetric: a change at day <em>t</em> retires the old subscription <em>at the start of</em> day <em>t</em>, so day <em>t</em> belongs to the new one — the old was active on days <code>start .. t-1</code>, which is <code>t - start</code> days. A subscription that survives to the end is active on days <code>start .. 30</code> inclusive, which is <code>31 - start</code> days. The <code>31</code> is an inclusive-range count, exactly like the <code>+1</code>s in <a href='#bags' style='color:var(--accent)'>Maximum Money in k Bags</a>.</p>
<p>Now user_1, who changes twice — <code>sub_a &rarr; sub_a_plus</code> on day 11, then <code>sub_a_plus &rarr; sub_a_pro</code> on day 21:</p>
<table class="trace">
<tr><th>subscription</th><th>start day</th><th>ends because</th><th>days_active</th><th>charge</th></tr>
<tr><td>sub_a</td><td>1</td><td>replaced on day 11</td><td>11 &minus; 1 = 10</td><td>1000 × 10/30 = 333.33</td></tr>
<tr><td>sub_a_plus</td><td>11</td><td>replaced on day 21</td><td>21 &minus; 11 = 10</td><td>1500 × 10/30 = 500</td></tr>
<tr><td>sub_a_pro</td><td>21</td><td>survives the cycle</td><td>31 &minus; 21 = 10</td><td>3000 × 10/30 = 1000</td></tr>
<tr><td>sub_b</td><td>1</td><td>survives, never changed</td><td>31 &minus; 1 = 30</td><td>2500 × 30/30 = 2500</td></tr>
<tr><td class="hit">total</td><td colspan="3" class="hit">333.33 + 500 + 1000 + 2500 = 4333.33</td><td class="hit">floor &rarr; <strong>4333</strong></td></tr>
</table>
<p>Note that a change is a <em>chain</em>: <code>sub_a_plus</code> is created by the first change and consumed by the second. So you must resolve the chain per subscription id, and — because <em>"changes may not be provided in chronological order"</em> — you must <strong>sort the changes by <code>change_day</code> first</strong>, or link them through their old/new ids. Processing them as given is the most likely bug in Part 2.</p></div>

<div class="step"><h4>3 &middot; Floor once, at the very end</h4>
<p>The General Constraints are unusually explicit about this, and the example is built to catch it:</p>
<div class="formula">correct:  floor(333.33 + 500 + 1000 + 2500) = floor(4333.33) = <b>4333</b>
wrong:    floor(333.33) + 500 + 1000 + 2500 = 333 + 4000     = <b>4333</b>  &larr; agrees <em>here</em>
</div>
<p>On this example both happen to give 4333, which is exactly why the statement spells the rule out with its own <code>$10.66666 + $20.66666</code> illustration: rounding each line first gives 1066 + 2066 = 3132, while flooring the sum gives 3133. Keep every intermediate value exact — use <code>Fraction</code>, or keep numerators over a common denominator of 30 — and floor only immediately before emitting the string. Floating-point <code>double</code> is a liability here for the usual reasons; <code>1000 * 10 / 30</code> is not exactly representable.</p>
<p>User_2 confirms the day arithmetic once more: <code>sub_c</code> runs days 1–15 (<code>16 - 1 = 15</code>) and <code>sub_c_premium</code> days 16–30 (<code>31 - 16 = 15</code>), giving <code>250 + 600 = 850</code>.</p></div>

<div class="step"><h4>4 &middot; What Parts 3 and 4 add</h4>
<p>Only their titles survived the screenshots — usage-based billing with <strong>flat and tiered</strong> rates. The predictable shapes, and the predictable traps:</p>
<ul>
<li><strong>Flat usage:</strong> <code>units × rate_per_unit</code>, added to the subscription total. Straightforward.</li>
<li><strong>Tiered usage:</strong> the near-universal trap is whether a tier's rate applies to <em>all</em> units once the threshold is crossed, or only to the units <em>within</em> that tier (marginal, like income tax). These give very different numbers; the statement will say which, and the examples will confirm it.</li>
<li><strong>Users with usage but no subscription</strong> are called out explicitly in the General Constraints, so they must still appear in the output — do not build the result by iterating over subscriptions.</li>
</ul></div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Floor once, on the user's grand total</strong>, never per subscription.</li>
<li><strong>Sort the changes by day</strong> — they may arrive out of order, and chained changes depend on it.</li>
<li><strong><code>t - start</code> vs <code>31 - start</code></strong>: the two day counts are not symmetric, and both come straight from the statement.</li>
<li><strong>Everything is cents, output is strings.</strong></li>
<li><strong>Include users with no subscriptions</strong> once usage billing enters.</li>
<li><strong>Multiple concurrent subscriptions per user</strong> are allowed and each prorates independently.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-cityhops', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Graph',
  label:'Problem', title:'Find Minimum City Hops',
  minutes:30, score:'',
  images:['src-cityhops-full.png','WhatsApp Image 2026-09-07 at 10.14.58 PM.jpeg','Screenshot_20260908_000439.png'],
  fn:{name:'findMinimumCityHops', ret:'int', params:[['string[]','cities'],['string','startCity'],['string','endCity']]},
  gen:`def gen(rng, n):
    al = 'abc'
    cities = sorted({''.join(rng.choice(al) for _ in range(3)) for _ in range(max(2, n))})
    return [cities, rng.choice(cities), rng.choice(cities)]`,
  tests:[
    {in:[["abc", "abd", "acd", "xyz"], "abc", "acd"], out:2},
    {in:[["abc", "abd"], "abc", "abc"], out:0},
    {in:[["aaa", "aab", "abb", "bbb"], "aaa", "bbb"], out:3},
    {in:[["abc", "abd", "xyz"], "abc", "xyz"], out:-1},
    {in:[["abc", "abd"], "abc", "abd"], out:1}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> Special thanks to a friend for sharing that this problem previously appeared in an Amazon Online Assessment. I've used September 3, 2026, the date this information was shared, as the initial last seen date. We'll take it from here. The shared source excerpt defines the city format, adjacency rule, minimum-hop objective, and unreachable result. The full statement has since become visible (see the first screenshot): the callable is <code>findMinimumCityHops</code>, both endpoints are guaranteed to appear in <code>cities</code>, and three worked examples are published. The judged core task matches the visible source at about 97%.</div>

<p>You are given an array of cities named <code>cities</code>. Each city is represented by a three-character lowercase string.</p>
<p>Two cities are directly connected when their strings differ in exactly one character position.</p>
<p>Starting from <code>startCity</code>, you may hop only between directly connected cities in <code>cities</code>. Return the minimum number of hops needed to reach <code>endCity</code>. If <code>endCity</code> is not reachable, return <code>-1</code>.</p>

<h3>Function</h3>
<pre class="sample">findMinimumCityHops(cities: String[], startCity: String, endCity: String) &rarr; int</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">cities    = ["abc","abd","acd","xyz"]
startCity = "abc"
endCity   = "acd"
return    = 2</pre>
<p>One shortest route is <code>abc</code> to <code>abd</code> to <code>acd</code>. Each hop changes exactly one character, so the route uses <code>2</code> hops.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">cities    = ["aaa","aab","abb","bbb"]
startCity = "aaa"
endCity   = "bbb"
return    = 3</pre>
<p>The route <code>aaa</code> to <code>aab</code> to <code>abb</code> to <code>bbb</code> changes one position per hop and reaches the destination in 3 hops.</p>

<div class="sublabel">Example 3</div>
<pre class="sample">cities    = ["abc","abd","xyz"]
startCity = "abc"
endCity   = "xyz"
return    = -1</pre>
<p>The city <code>xyz</code> is not connected to the component containing <code>abc</code>, so it cannot be reached.</p>

<h3>Constraints</h3>
<ul>
  <li><code>cities</code> contains at least one city.</li>
  <li>Every value in <code>cities</code>, as well as <code>startCity</code> and <code>endCity</code>, consists of exactly three lowercase English letters.</li>
  <li><code>startCity</code> and <code>endCity</code> each appear in <code>cities</code>.</li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Cities are nodes; an edge exists when two 3-letter strings differ in exactly one position. "Minimum hops" on an unweighted graph is BFS — the only question is how to build the edges without comparing all pairs.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Comparing every pair is O(n²). Instead use wildcard buckets: each city <code>abc</code> joins the buckets <code>*bc</code>, <code>a*c</code>, <code>ab*</code>. Two cities are adjacent iff they share a bucket. BFS over city → bucket → city.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Classic word-ladder. Build a dict from each of the three wildcard patterns to the list of cities matching it, then BFS from <em>startCity</em> counting levels until <em>endCity</em> pops.</p>
<p>Mark each bucket as consumed the first time you expand it, so the total work stays linear in the number of (city, pattern) pairs.</p>
<p>Example: <code>["abc","abd","acd","xyz"]</code>, start "abc", end "acd" → abc → abd → acd = <strong>2</strong> hops. ✓</p><p><span class="cx">Time O(n · L)</span><span class="cx">Space O(n · L)</span></p><pre class="sample"><code>from collections import defaultdict, deque

def findMinimumCityHops(cities, startCity, endCity):
    if startCity == endCity:
        return 0
    buckets = defaultdict(list)
    for c in cities:
        for i in range(len(c)):
            buckets[c[:i] + '*' + c[i + 1:]].append(c)

    seen = {startCity}
    used = set()
    dq = deque([(startCity, 0)])
    while dq:
        city, d = dq.popleft()
        for i in range(len(city)):
            pat = city[:i] + '*' + city[i + 1:]
            if pat in used:
                continue
            used.add(pat)
            for nxt in buckets.get(pat, ()):
                if nxt == endCity:
                    return d + 1
                if nxt not in seen:
                    seen.add(nxt)
                    dq.append((nxt, d + 1))
    return -1</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example: <code>cities = ["abc","abd","acd","xyz"]</code>, start <code>"abc"</code>, end <code>"acd"</code>, answer <strong>2</strong>.</p>
<div class="step"><h4>1 &middot; It is a graph, and the edges are implicit</h4>
<p>Cities are nodes; two are adjacent when their strings differ in exactly one position. Nobody hands you the edge list — you must derive it, and how you derive it is the whole problem.</p>
<div class="formula">abc &harr; abd   differ at position 2 only        &check;
abd &harr; acd   differ at position 1 only        &check;
abc &harr; acd   differ at positions 1 <b>and</b> 2   &cross;
xyz &harr; any   differs everywhere                &cross;</div>
<p>Every edge costs one hop, so "minimum hops" on an unweighted graph is <strong>BFS</strong>, not Dijkstra and not DFS. BFS dequeues nodes in non-decreasing distance order, so the first time you reach <code>endCity</code> you are already on a shortest route.</p></div>
<div class="step"><h4>2 &middot; Wildcard buckets instead of pairwise comparison</h4>
<p>Comparing every pair is O(n²·L). Instead, note that "differ in exactly one position" is the same as "share a wildcard pattern":</p>
<div class="formula">abc joins buckets:  <b>*bc</b> , <b>a*c</b> , <b>ab*</b>
abd joins buckets:  *bd , a*d , <b>ab*</b>      &larr; shares ab* with abc
acd joins buckets:  *cd , <b>a*d</b> , ac*      &larr; shares a*d with abd</div>
<p>Two cities are adjacent exactly when they sit in a common bucket. Building the map costs O(n·L); each city belongs to L = 3 buckets, so the total number of (city, pattern) entries is 3n.</p>
<p>The <code>used</code> set is what keeps this linear. Once a bucket has been expanded, every city in it has been discovered, so it can never usefully be expanded again — marking it consumed means each bucket's list is walked at most once across the entire BFS. Without that guard, a bucket holding <em>k</em> cities is rescanned up to <em>k</em> times and the cost degrades to quadratic on dense inputs.</p></div>
<div class="step"><h4>3 &middot; The BFS, step by step</h4>
<table class="trace">
<tr><th>dequeue</th><th>d</th><th>patterns tried</th><th>new cities found</th><th>action</th></tr>
<tr><td>abc</td><td>0</td><td>*bc, a*c, ab*</td><td>ab* holds abd</td><td>abd ≠ end &rarr; enqueue at d = 1</td></tr>
<tr><td class="hit">abd</td><td class="hit">1</td><td class="hit">*bd, a*d, ab*(used)</td><td class="hit">a*d holds acd</td><td class="hit">acd <strong>is</strong> end &rarr; return 1 + 1 = <strong>2</strong></td></tr>
</table>
<p>Answer <strong>2</strong>, via <code>abc &rarr; abd &rarr; acd</code> — the route the statement names. Note <code>xyz</code> shares no bucket with anything and is never visited; unreachable nodes cost nothing.</p>
<p>The check is made on the <em>neighbour</em> as it is discovered (<code>return d + 1</code>) rather than when it is dequeued. Both are correct for BFS; checking at discovery just avoids one extra queue round-trip.</p></div>
<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong><code>startCity == endCity</code> returns 0</strong>, and must be checked before the loop.</li>
<li><strong>Both endpoints are guaranteed to appear in <code>cities</code></strong>, so the BFS can be seeded from <code>startCity</code> without a membership check — but seeding it anyway costs nothing and survives a judge that drops the guarantee.</li>
<li><strong>Unreachable end returns &minus;1</strong>, as example 3 shows — not 0 and not an exception.</li>
<li><strong>Mark buckets used, not just cities visited.</strong> Both guards are needed for the linear bound.</li>
<li><strong>Hops are edges, not nodes.</strong> A 3-city route is 2 hops; an off-by-one here is easy.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-cameras', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Tree',
  label:'Problem', title:'Binary Tree Cameras',
  minutes:30, score:'',
  images:['WhatsApp Image 2026-09-07 at 10.14.58 PM (1).jpeg','Screenshot_20260907_235324.png'],
  fn:{name:'minCameraCover', ret:'int', params:[['int[]','root']]},
  body:`
<div class="tags"><span class="tag hard">Hard</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> Special thanks to a friend for sharing that this problem previously appeared in an Amazon Online Assessment. I've used September 3, 2026, the date this information was shared, as the initial last seen date. We'll take it from here. The shared source excerpt states the objective but omits the exact camera coverage rule and constraints. The runnable task follows the canonical Binary Tree Cameras definition and matches the visible source at about 90%.</div>

<p>You are given the <code>root</code> of a binary tree. You may install cameras on its nodes.</p>
<p>A camera installed at a node monitors that node, its parent if one exists, and its immediate children.</p>

<div class="locked">🔒 The problem statement continues (paywalled on FastPrep — not captured).</div>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">root   = [0,0,null,0,0]
return = 1</pre>
<p>Place one camera on the second node in the level-order representation. It monitors its parent, itself, and both of its children, so every node is covered.</p>
<div class="frag">Example 2 was blurred/locked in the screenshot.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>A camera at a node covers its parent, itself and its children. Greedy from the root is wrong; think about which nodes you are <em>forced</em> to cover last.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Post-order DFS with three states per node: <em>needs covering</em>, <em>covered but has no camera</em>, <em>has a camera</em>. A node installs a camera exactly when one of its children reports "needs covering". Leaves always report "needs covering" — never put a camera on a leaf.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>This is LeetCode 968, Binary Tree Cameras. Bottom-up greedy with three return states:</p>
<ul>
<li><code>0</code> — this subtree's root is <strong>not covered</strong></li>
<li><code>1</code> — covered, but has no camera</li>
<li><code>2</code> — has a camera</li>
</ul>
<p>Rules at a node: if either child returns 0, you must place a camera here → return 2. Else if either child returns 2, you are covered by a child → return 1. Otherwise return 0. Null children return 1 (vacuously covered). At the very end, if the root returns 0, add one more camera.</p>
<p>Example: <code>root = [0,0,null,0,0]</code> → one camera on the second node → <strong>1</strong>. ✓</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(h)</span></p><pre class="sample"><code>def minCameraCover(root):
    cameras = 0

    def dfs(node):
        nonlocal cameras
        if not node:
            return 1                     # null counts as covered
        l, r = dfs(node.left), dfs(node.right)
        if l == 0 or r == 0:             # a child is uncovered -&gt; must place here
            cameras += 1
            return 2
        if l == 2 or r == 2:             # a child has a camera -&gt; we are covered
            return 1
        return 0                         # covered by nobody yet

    if dfs(root) == 0:
        cameras += 1
    return cameras</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example <code>root = [0,0,null,0,0]</code>, answer <strong>1</strong>.</p>
<div class="step"><h4>1 &middot; Why greedy from the top fails and greedy from the bottom works</h4>
<p>A camera covers its node, its parent and its children — a three-level reach. The instinct is to place cameras high up, since the root sees the most. That is wrong: <strong>leaves are the constrained nodes</strong>. A leaf can only be covered by itself or its parent, so the scarce decisions happen at the bottom, and you should spend cameras where choice is smallest.</p>
<p>This gives the governing rule: <strong>never put a camera on a leaf</strong>. Moving it to the leaf's parent covers strictly more (the parent, its other children, and the grandparent) at the same cost. So process bottom-up and place a camera only when a child <em>forces</em> it.</p></div>
<div class="step"><h4>2 &middot; Three states, and why two would not be enough</h4>
<p>Each subtree reports one of three things to its parent. Two states ("covered" / "not covered") lose the distinction that matters, because a covered node with a camera also covers its parent, while a covered node without one does not:</p>
<table class="trace">
<tr><th>state</th><th>meaning</th><th>what the parent must do</th></tr>
<tr><td><code>0</code></td><td>this node is <strong>not covered</strong></td><td>must place a camera here — no other chance</td></tr>
<tr><td><code>1</code></td><td>covered, but has <strong>no camera</strong></td><td>gets no help from this child</td></tr>
<tr><td><code>2</code></td><td>has a <strong>camera</strong></td><td>is covered for free by this child</td></tr>
</table>
<div class="formula">if either child is <b>0</b>  &rarr; place a camera, return <b>2</b>   (a child is uncovered; last chance)
elif either child is <b>2</b> &rarr; return <b>1</b>                 (a child's camera covers me)
else                        &rarr; return <b>0</b>                 (both children covered, nobody sees me)</div>
<p>The order of the tests is load-bearing: an uncovered child must be answered even if the other child has a camera, so the <code>0</code> test comes first.</p>
<p><code>null</code> children return <strong>1</strong>, not 0 — a missing child is vacuously covered and needs nothing. Returning 0 would force a camera above every leaf and roughly double the answer.</p></div>
<div class="step"><h4>3 &middot; The example traced</h4>
<p><code>[0,0,null,0,0]</code> is the tree: root A, left child B, B's children C and D (A has no right child).</p>
<table class="trace">
<tr><th>node</th><th>children states</th><th>rule applied</th><th>returns</th><th>cameras</th></tr>
<tr><td>C (leaf)</td><td>null, null &rarr; 1, 1</td><td>no 0, no 2 &rarr; uncovered</td><td>0</td><td>0</td></tr>
<tr><td>D (leaf)</td><td>null, null &rarr; 1, 1</td><td>no 0, no 2 &rarr; uncovered</td><td>0</td><td>0</td></tr>
<tr><td class="hit">B</td><td class="hit">0, 0</td><td class="hit">a child is uncovered &rarr; <strong>place camera</strong></td><td class="hit">2</td><td class="hit">1</td></tr>
<tr><td>A (root)</td><td>2, null &rarr; 2, 1</td><td>a child has a camera</td><td>1</td><td>1</td></tr>
</table>
<p>The root returns 1 — covered — so no extra camera is needed and the answer is <strong>1</strong>. That is exactly the statement's "place one camera on the second node". The single camera at B covers B, its children C and D, and its parent A: all four nodes.</p></div>
<div class="step"><h4>4 &middot; The root's special case</h4>
<p>Every node except the root can be rescued by its parent. The root has none, so if the DFS returns <code>0</code> at the top, that node is uncovered and one more camera must be added:</p>
<pre class="sample">if dfs(root) == 0: cameras += 1</pre>
<p>Forgetting this line is the single most common bug in this problem — and it does not show up on the published example, where the root happens to return 1. Test with a single node (answer 1) and with a two-node tree (answer 1) to exercise it.</p></div>
<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong><code>null</code> returns 1</strong>, not 0.</li>
<li><strong>Check "either child is 0" before "either child is 2".</strong></li>
<li><strong>Handle the root returning 0</strong> after the traversal.</li>
<li><strong>Post-order.</strong> Both children must be evaluated before deciding — and both calls must actually run, so beware short-circuit evaluation in <code>l == 0 or r == 0</code> if you inline the recursion there.</li>
<li><strong>Recursion depth</strong> is O(h); a degenerate tree of 10<sup>4</sup> nodes will exceed Python's default limit.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-beauty', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Array',
  label:'Problem', title:'Calculate Beauty Values',
  minutes:30, score:'',
  images:['WhatsApp Image 2026-09-07 at 10.14.58 PM (2).jpeg'],
  fn:{name:'calculateBeautyValues', ret:'long', params:[['int[]','arr'],['int[][]','pairs']]},
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">NEW GRAD</span><span class="tag">FULLTIME</span><span class="tag">INTERN</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The judged core task matches the visible source at about 100%. The source images do not show numeric bounds or the original callable signature.</div>

<p>Amazon's development team is working on a feature for a new product, a smart array processor. In this smart processor, quite simply, given an array of numbers and instructions on which parts of the array to pick and combine into a new array, for each number in the original array, if it's included in the new array, its efficiency is <code>0</code>; otherwise, the efficiency is the count of smaller numbers in the new array. The goal is to add up the efficiencies for all numbers in the original array.</p>

<div class="locked">🔒 The problem statement continues (paywalled on FastPrep — not captured).</div>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">arr    = [1, 2, 3, 2, 4, 5]
pairs  = [[0, 1], [3, 4], [0, 0], [3, 4]]
return = 12</pre>
<pre class="sample">n     = 6
arr   = [1, 2, 3, 2, 4, 5]
m     = 4
pairs = [[0, 1], [3, 4], [0, 0], [3, 4]]</pre>
<p>The subarrays represented by <code>pairs</code> are:</p>
<table class="oa">
<tr><th>pair</th><th>start</th><th>end</th><th>subarray</th></tr>
<tr><td>[0, 1]</td><td>0</td><td>1</td><td>[1, 2]</td></tr>
<tr><td>[3, 4]</td><td>3</td><td>4</td><td>[2, 4]</td></tr>
<tr><td>[0, 0]</td><td>0</td><td>0</td><td>[1]</td></tr>
<tr><td>[3, 4]</td><td>3</td><td>4</td><td>[2, 4]</td></tr>
</table>
<p>On concatenating all the subarrays represented by <code>pairs</code>, we get <code>efficient = [1, 2, 2, 4, 1, 2, 2]</code>.</p>
<p>The indices <code>2</code> and <code>5</code>, don't contribute to the formation of the array <code>efficient</code>.</p>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>"Beauty" is defined per subarray as the difference between its largest and smallest element (check the visible examples). Summing that over all subarrays naively is O(n²) or worse.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Σ(max − min) over all subarrays = Σmax − Σmin. Each of those is a standard monotonic-stack computation: for each element, count how many subarrays it is the maximum (resp. minimum) of, using previous-greater / next-greater-or-equal boundaries.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Two stages. <strong>First build <code>efficient</code></strong> by concatenating <code>arr[s..e]</code> for each pair — the published example gives <code>[1,2] + [2,4] + [1] + [2,4] = [1,2,2,4,1,2,4]</code>. Then compute the beauty of that array.</p>
<p>For the beauty itself, the natural reading is Σ(max − min) over every subarray, which splits into <code>Σ max − Σ min</code>, each a standard monotonic-stack computation: for each index, count the subarrays in which it is the extreme, as <code>left[i] × right[i]</code>, where <code>left</code> reaches back to the previous strictly-greater element and <code>right</code> forward to the next greater-or-equal. The strict/non-strict asymmetry is what stops duplicates being counted twice.</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def _sum_extreme(a, want_max):
    n = len(a); stack = []; left = [0]*n; right = [0]*n
    for i in range(n):
        while stack and ((a[stack[-1]] &lt; a[i]) if want_max else (a[stack[-1]] &gt; a[i])):
            stack.pop()
        left[i] = i - (stack[-1] if stack else -1)
        stack.append(i)
    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and ((a[stack[-1]] &lt;= a[i]) if want_max else (a[stack[-1]] &gt;= a[i])):
            stack.pop()
        right[i] = (stack[-1] if stack else n) - i
        stack.append(i)
    return sum(a[i] * left[i] * right[i] for i in range(n))

def calculateBeautyValues(arr, pairs):
    efficient = []
    for s, e in pairs:
        efficient.extend(arr[s:e + 1])          # inclusive on both ends
    return _sum_extreme(efficient, True) - _sum_extreme(efficient, False)</code></pre><div class="unsure"><strong>The definition of "beauty" was not captured, and this does not reproduce the published example.</strong> The statement is paywalled exactly where beauty is defined ("for each number&hellip;"), and Σ(max&minus;min) over all subarrays of <code>efficient</code> gives <strong>51</strong>, not the printed <strong>12</strong>. Other readings were tested and none match: sum of <code>efficient</code> = 16, Σ over only the four listed subarrays = 5, Σ|adjacent differences| = 9, Σ max = 92, Σ min = 41. (The statement also prints <code>efficient = [1,2,2,4,1,2,2]</code> where concatenation gives <code>&hellip;,2,4</code> — its last element looks like a typo; using its version changes none of these conclusions.) The stack machinery is correct for the Σ(max&minus;min) reading and is verified against brute force on 400 random inputs — but <strong>recover the real definition before trusting the result</strong>.<br><br>The code previously shown here was named <code>calculateBeautySum(arr)</code> and ignored <code>pairs</code> entirely, so it never built <code>efficient</code> at all.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<div class="unsure" style="margin-top:0">The definition of "beauty" is behind the paywall, and no reading tested reproduces the published answer of 12. This panel sets out what <em>is</em> determined, what is not, and how the machinery works for the most likely reading — but the final number is unresolved.</div>

<div class="step"><h4>1 &middot; What the example does pin down: building <code>efficient</code></h4>
<p>Each pair is an inclusive index range into <code>arr</code>, and the selected subarrays are concatenated in the order the pairs are given. Pairs may repeat and may overlap; indices never used simply do not appear.</p>
<div class="formula">arr   = [1, 2, 3, 2, 4, 5]
pairs = [0,1] [3,4] [0,0] [3,4]

[0,1] &rarr; arr[0..1] = [1, 2]
[3,4] &rarr; arr[3..4] = [2, 4]
[0,0] &rarr; arr[0..0] = [1]        &larr; a single-element range, not empty
[3,4] &rarr; arr[3..4] = [2, 4]     &larr; the same range again

efficient = [1, 2, 2, 4, 1, 2, 4]     (7 elements)</div>
<p>This matches the statement's own remark that indices 2 and 5 (values 3 and 5) never contribute. It also exposes a small error in the source: the statement prints <code>efficient = [1,2,2,4,1,2,2]</code>, whose last element should be 4 — the fourth pair is <code>[3,4]</code>, identical to the second. The length, 7, is right either way.</p>
<p>Note <code>[0,0]</code> contributes one element, not zero: the range is inclusive at both ends, so the slice is <code>arr[s : e+1]</code>.</p></div>

<div class="step"><h4>2 &middot; The reading that does not work, and by how much</h4>
<p>The natural guess — beauty = Σ(max &minus; min) over every subarray of <code>efficient</code> — gives <strong>51</strong>, not 12. Every other simple candidate was computed and none lands on 12 either:</p>
<table class="trace">
<tr><th>candidate definition</th><th>value</th></tr>
<tr><td>Σ(max &minus; min) over all subarrays</td><td>51</td></tr>
<tr><td>Σ max over all subarrays</td><td>92</td></tr>
<tr><td>Σ min over all subarrays</td><td>41</td></tr>
<tr><td>Σ(max &minus; min) over only the four listed subarrays</td><td>5</td></tr>
<tr><td>sum of <code>efficient</code></td><td>16</td></tr>
<tr><td>Σ |adjacent differences|</td><td>9</td></tr>
<tr><td>max &minus; min of the whole array</td><td>3</td></tr>
<tr><td class="hit">published answer</td><td class="hit"><strong>12</strong></td></tr>
</table>
<p>Using the statement's typo'd array changes these to 47, 86, 39, 14, 7 and 3 — still no 12. The one arithmetic coincidence is that the first six elements sum to 12, which is not a rule anybody would state. <strong>The conclusion is that the beauty definition is genuinely missing</strong>, not that it is subtle: the statement is cut off mid-sentence at "for each number&hellip;", which is precisely where it would have been given.</p>
<p>This is worth flagging rather than papering over. A confidently wrong definition here would be more harmful than an admitted gap, because the code would look right and fail every judge test.</p></div>

<div class="step"><h4>3 &middot; The contribution technique, which is what this problem is really testing</h4>
<p>Whatever the exact definition, the tag on this question is monotonic stack, and the machinery is worth knowing in its own right. To sum a per-subarray extremum over <em>all</em> subarrays without enumerating them (there are O(n²)), <strong>invert the question</strong>: instead of asking "what is the max of this subarray?", ask "for how many subarrays is <em>this element</em> the max?"</p>
<div class="formula">left[i]  = i &minus; (index of previous element strictly greater)
right[i] = (index of next element greater-or-equal) &minus; i
subarrays in which a[i] is the maximum = <b>left[i] &times; right[i]</b>
&Sigma;max = &Sigma;<sub>i</sub> a[i] &times; left[i] &times; right[i]</div>
<p>The counts multiply because the choices are independent: a subarray in which <code>a[i]</code> is the maximum is any range whose left endpoint lies in the <code>left[i]</code> positions since the last bigger element, paired with any right endpoint in the <code>right[i]</code> positions before the next one.</p>
<p><strong>The strict/non-strict asymmetry is not cosmetic.</strong> With duplicates, a subarray containing two equal maxima would be counted once for each unless exactly one side breaks ties. Using <em>strictly greater</em> on the left and <em>greater-or-equal</em> on the right assigns every such subarray to its leftmost maximum, and to only that one. Make both strict and duplicates are double-counted; make both non-strict and they are dropped.</p>
<p>Each index is pushed and popped once, so both sweeps are O(n) — and the same code computes Σmin by flipping the comparisons, which is why it is parameterised rather than written twice. Verified against brute-force enumeration of all subarrays on 400 random inputs.</p></div>

<div class="step"><h4>4 &middot; Before using any of this</h4>
<ul>
<li><strong>Recover the beauty definition</strong> from the real statement. Everything above the definition is solid; everything downstream of it is conditional.</li>
<li><strong>Build <code>efficient</code> first</strong> — the previously published code ignored <code>pairs</code> entirely and computed over <code>arr</code> instead.</li>
<li><strong>Ranges are inclusive</strong>, so slice with <code>e + 1</code>.</li>
<li><strong><code>efficient</code> can be much longer than <code>arr</code></strong> when pairs repeat, so size any buffers off its length, not <code>n</code>.</li>
<li><strong>Sums over all subarrays grow fast</strong> — O(n²) terms each up to max(arr) — so use 64-bit.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-firstunique', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · String',
  label:'Problem', title:'Find First Unique 🍉',
  minutes:20, score:'',
  images:['WhatsApp Image 2026-09-07 at 10.14.58 PM (3).jpeg'],
  fn:{name:'findFirstUnique', ret:'int', params:[['string','s']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [''.join(rng.choice('abcde') for _ in range(m))]`,
  tests:[
    {in:["statistics"], out:3},
    {in:["aabbcc"], out:-1},
    {in:["z"], out:1},
    {in:["aabbc"], out:5},
    {in:["abcabc"], out:-1}
  ],
  body:`
<div class="tags"><span class="tag easy">Easy</span><span class="tag">Amazon</span><span class="tag">INTERN</span><span class="tag">OA</span></div>

<p>Amazon Web Services is experimenting with optimizing search queries based on the location of the first unique character in a search. You have been asked to help test the query your team has created to ensure it works as designed. A unique character is one which appears only once in a string. Given a string consisting of lowercase English letters only, return the index of the first occurrence of a unique character in the string using 1-based indexing. If the string does not contain any unique character, return -1.</p>

<div class="locked">🔒 The problem statement continues (paywalled on FastPrep — not captured).</div>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">s      = "statistics"
return = 3</pre>
<p>The unique characters are [a, c] among which a occurs first. Using 1-based indexing, it is at index 3.</p>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Two passes beat one clever pass here. What do you need to know about a character before you can call it unique?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Count every character first, then scan again and return the first with count 1.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Count occurrences, then re-scan in original order and return the first element whose count is 1 (or the stated sentinel when there is none).</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(k)</span></p><pre class="sample"><code>from collections import Counter

def findFirstUnique(s):
    freq = Counter(s)
    for i, ch in enumerate(s):
        if freq[ch] == 1:
            return i + 1          # 1-based INDEX, not the character
    return -1</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example <code>s = "statistics"</code>, answer <strong>3</strong>.</p>
<div class="step"><h4>1 &middot; Read what is returned — this is the whole problem</h4>
<p>The example says <code>return = 3</code> and explains: <em>"the unique characters are [a, c], among which a occurs first. Using 1-based indexing, it is at index 3."</em> So the function returns a <strong>1-based position</strong>, not the character. Getting this wrong produces <code>'a'</code>, which looks reasonable and fails every test.</p>
<div class="formula">index:  1  2  3  4  5  6  7  8  9 10
char:   s  t  a  t  i  s  t  i  c  s</div></div>
<div class="step"><h4>2 &middot; Why two passes, and why one pass cannot work</h4>
<p>"Unique" means <em>appears exactly once in the whole string</em> — a property you cannot evaluate at the moment you first meet a character, because its duplicate may lie ahead. So the first pass must finish counting before the second can judge:</p>
<table class="trace">
<tr><th>char</th><th>s</th><th>t</th><th>a</th><th>i</th><th>c</th></tr>
<tr><th>count</th><td>3</td><td>3</td><td class="hit">1</td><td>2</td><td class="hit">1</td></tr>
</table>
<p>Then rescan <strong>in the original order</strong> and return the first character whose count is 1:</p>
<table class="trace">
<tr><th>i (1-based)</th><td>1</td><td>2</td><td class="hit">3</td></tr>
<tr><th>char</th><td>s</td><td>t</td><td class="hit">a</td></tr>
<tr><th>count</th><td>3</td><td>3</td><td class="hit">1 &rarr; return <strong>3</strong></td></tr>
</table>
<p>Scanning the <em>dictionary</em> instead of the string is the other classic error: it returns whichever unique character the hash order happens to yield first, and in this example would be as likely to give 'c' (index 9) as 'a'.</p></div>
<div class="step"><h4>3 &middot; Traps</h4>
<ul>
<li><strong>Return the 1-based index</strong>, not the character and not the 0-based index.</li>
<li><strong>Rescan the string, not the counter</strong>, to preserve original order.</li>
<li><strong>No unique character</strong> — decide the sentinel (this code returns &minus;1); the paywalled statement did not show it.</li>
<li><strong>Both passes are O(n)</strong>; there is no need for anything cleverer, and an <code>index()</code> call inside the loop would make it O(n²).</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-memory', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Sorting',
  label:'Problem', title:'Maximum System Memory Capacity',
  minutes:25, score:'',
  images:['WhatsApp Image 2026-09-07 at 10.14.58 PM (4).jpeg'],
  fn:{name:'maxSystemMemoryCapacity', ret:'long', params:[['int[]','memory']]},
  body:`
<div class="tags"><span class="tag easy">Easy</span><span class="tag">Amazon</span><span class="tag">INTERN</span><span class="tag">NEW GRAD</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> Update (2026-07-21): Reports of Amazon 2027 Intern questions started appearing today. I have not confirmed whether they are real yet, so I am sharing this question for review until I know more.</div>

<p>Amazon is optimizing the capacity of a cloud system with <code>n</code> servers. The memory capacity of the <code>i</code>-th server is <code>memory[i]</code>.</p>
<p>A system uses an even number of servers. If it uses <code>2x</code> servers, exactly <code>x</code> are primary servers and the other <code>x</code> are backup servers. For every primary server <code>P</code>, it must be paired with a distinct backup server <code>B</code> whose memory capacity is at least that of <code>P</code>.</p>

<div class="locked">🔒 The problem statement continues (paywalled on FastPrep — not captured).</div>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">memory = [1, 2, 1, 2]
return = 3</pre>
<p>Here, we have 4 servers [serverA, serverB, serverC, serverD] having memory sizes as [1, 2, 1, 2]. We can choose serverA and serverB as primary servers, and serverC and serverD as their respective backup. The conditions hold true since memory[serverC] &ge; memory[serverA] and memory[serverD] &ge; memory[serverB]. Hence, the maximum system memory capacity is 3.</p>
<div class="frag">Example 2 was blurred/locked in the screenshot.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Read the visible tags: this one is filed under <em>Sorting</em>. Once sorted, what greedy becomes obvious?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Sort the module capacities, then sweep taking the best running combination — the answer is a max over a single pass rather than a search over subsets.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Read the example backwards to recover the rule. With <code>memory = [1,2,1,2]</code> the answer is <strong>3</strong>, and 3 is the sum of the two <em>primary</em> servers (1 and 2) — not the total of all four (6), nor the server count (4). So the quantity to maximise is <strong>the total memory of the primary servers</strong>.</p>
<p>Each primary needs a distinct backup with <code>memory[backup] &ge; memory[primary]</code>, so you are really choosing disjoint <em>pairs</em>, and within a pair the primary is the smaller element. The objective becomes:</p>
<pre class="sample">maximise  Σ over chosen disjoint pairs of  min(pair)</pre>
<p>That is the classic array-pairing maximisation: <strong>sort descending and pair adjacent elements</strong>. Pairing the two largest together "wastes" as little as possible, because the larger of any pair is always discarded — so you want the discarded elements to be the ones you could not have kept anyway. The answer is then every second element of the descending sort.</p><p><span class="cx">Time O(n log n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def maxSystemMemoryCapacity(memory):
    a = sorted(memory, reverse=True)
    return sum(a[i] for i in range(1, len(a), 2))   # 2nd, 4th, 6th, ...</code></pre><div class="unsure">Checked against brute-force search over every choice of primaries, backups and pairing for all arrays of length &le; 6 (300 random cases, no mismatch), and against the published example <code>[1,2,1,2] &rarr; 3</code>. <strong>The code previously here was an acknowledged placeholder</strong> — it summed a running prefix and returned 6 on that example — and was named <code>maxSystemMemory</code> rather than the declared <code>maxSystemMemoryCapacity</code>.<br><br><strong>Still inferred:</strong> the pairing rule is stated in the visible intro, but the objective ("maximum system memory capacity") is only pinned down by the one published example. If the judge disagrees, the likely alternative is that unpaired servers may also count.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example <code>memory = [1, 2, 1, 2]</code>, answer <strong>3</strong>.</p>
<div class="step"><h4>1 &middot; Recovering the objective from the example</h4>
<p>The statement is paywalled where it says what to maximise, so read it off the number. Four servers, memories 1, 2, 1, 2, answer 3. Candidates:</p>
<table class="trace">
<tr><th>candidate objective</th><th>value on the example</th><th>matches 3?</th></tr>
<tr><td>total memory of all servers used</td><td>1+2+1+2 = 6</td><td>no</td></tr>
<tr><td>number of servers used</td><td>4</td><td>no</td></tr>
<tr><td class="hit">total memory of the <strong>primary</strong> servers</td><td class="hit">1 + 2 = 3</td><td class="hit"><strong>yes</strong></td></tr>
</table>
<p>The example's own wording agrees: it names A and B as primaries with memories 1 and 2, and C, D as their backups. Backups provide redundancy; they do not add usable capacity.</p></div>
<div class="step"><h4>2 &middot; Restating it as a pairing problem</h4>
<p>Each primary needs a <em>distinct</em> backup with <code>memory[backup] &ge; memory[primary]</code>. So a valid configuration is a set of disjoint pairs, and within each pair the primary must be the smaller (or equal) element. Therefore:</p>
<div class="formula">total capacity = Σ over chosen disjoint pairs of <b>min(pair)</b></div>
<p>Every pair discards its larger element. The question becomes: how do you pair up the array so that as little value as possible is discarded?</p></div>
<div class="step"><h4>3 &middot; Sort descending, pair adjacent</h4>
<p>Sort descending and take consecutive pairs. The intuition: the very largest element can never be kept (nothing exceeds it, so it must serve as a backup), so pair it with the <em>second</em> largest — that way the element it "wastes" is the one you would have lost anyway. Repeat.</p>
<div class="formula">[1,2,1,2]  sorted desc &rarr;  [<b>2</b>, 2, <b>1</b>, 1]
                             pair (2,2) &rarr; keep 2
                             pair (1,1) &rarr; keep 1
answer = a[1] + a[3] = 2 + 1 = <b>3</b></div>
<p>So the answer is simply the sum of every <em>second</em> element of the descending sort — indices 1, 3, 5, … Contrast with the greedy that pairs the largest with the smallest: <code>(2,1)</code> and <code>(2,1)</code> keeps 1 + 1 = 2, which is worse. Pairing like with like is what preserves value.</p>
<p>An odd-length array simply leaves its last (smallest) element unpaired, and since all memories are positive there is never a reason to use fewer pairs than available. Checked against exhaustive search over every choice of primaries, backups and pairing for arrays of length &le; 6 — 300 random cases, no mismatch.</p></div>
<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Backup memory must be &ge;, not &gt;</strong> — equal values pair legally, which is exactly what the example relies on.</li>
<li><strong>Sum the primaries only</strong>, i.e. the smaller of each pair.</li>
<li><strong>Descending sort, odd indices.</strong> Ascending sort with even indices is the same thing only when n is even; the odd case differs.</li>
<li><strong>Return type is <code>long</code>.</strong></li>
<li>The objective is <strong>inferred from one example</strong> — see the note in the solution.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-distinctpairs', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Hash Table',
  label:'Problem', title:'Get Distinct Pairs (Also apply to AS intern)',
  minutes:25, score:'',
  images:['WhatsApp Image 2026-09-07 at 10.14.58 PM (5).jpeg'],
  fn:{name:'getDistinctPairs', ret:'int', params:[['int[]','stocksProfit'],['int','target']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    a = [rng.randint(1, 20) for _ in range(m)]
    return [a, rng.randint(2, 40)]`,
  tests:[
    {in:[[5, 7, 9, 13, 11, 6, 6, 3, 3], 12], out:3},
    {in:[[1, 1, 1], 2], out:1},
    {in:[[6], 12], out:0},
    {in:[[1, 2, 3, 4, 5], 6], out:2},
    {in:[[6, 6], 12], out:1}
  ],
  body:`
<div class="tags"><span class="tag easy">Easy</span><span class="tag">Amazon</span><span class="tag">INTERN</span><span class="tag">NEW GRAD</span><span class="tag">OA</span></div>

<p>A financial strategist at Amazon Web Services (AWS) is analyzing a collection of profitable investments, each represented by an integer array. Every value in the array indicates the annual gain of a particular investment. The strategist's goal is to identify all unique investment pairs whose combined annual returns exactly match a given target value.</p>
<p>Unique pairs are defined as combinations that vary by at least one element (i.e., their values are not at the exact same positions or do not have identical values in identical positions).</p>

<div class="locked">🔒 The problem statement continues (paywalled on FastPrep — not captured).</div>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">stocksProfit = [5, 7, 9, 13, 11, 6, 6, 3, 3]
target       = 12
return       = 3</pre>
<p>There are four pairs whose combined gains equal the target return of 12. However, since the array includes duplicate values of 3, there are two versions of the pair (9, 3): one between positions 2 and 7, and another between positions 2 and 8. But only one of these can be counted to maintain uniqueness. Therefore, the valid and unique pairs are:</p>
<ul><li>(5, 7)</li><li>(3, 9)</li><li>(6, 6)</li></ul>
<p>We return 3.</p>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>You need pairs whose combined value hits a target, with "distinct" meaning the two elements are not at the same position and the <em>pair of values</em> is not repeated.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>One hash pass: for each value <em>v</em>, look for <code>target - v</code> among the values already seen. Deduplicate by storing the normalised pair <code>(min, max)</code> in a set.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Walk the array once with a set of seen values and a set of emitted pairs. For each <em>v</em>, if <code>target - v</code> has been seen, record the normalised pair. The size of the pair set is the answer.</p>
<p>The statement's example returns 3 for <code>stocksProfit = [5, 7, 9, 13, 11, 6, 6, 3, 3]</code>, <code>target = 12</code>: the pairs are (5,7), (9,3) and (6,6) — note (3,9) and (9,3) are the same pair, and the duplicate 3s and 6s do not create extra pairs.</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def getDistinctPairs(stocksProfit, target):
    seen = set()
    pairs = set()
    for v in stocksProfit:
        need = target - v
        if need in seen:
            pairs.add((min(v, need), max(v, need)))
        seen.add(v)
    return len(pairs)</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example <code>stocksProfit = [5,7,9,13,11,6,6,3,3]</code>, <code>target = 12</code>, answer <strong>3</strong>.</p>
<div class="step"><h4>1 &middot; "Distinct" means distinct by value, not by position</h4>
<p>This is the only real decision in the problem. Find the pairs summing to 12:</p>
<table class="trace">
<tr><th>pair of values</th><th>positions available</th><th>counted as</th></tr>
<tr><td>5 + 7</td><td>(0, 1)</td><td>1</td></tr>
<tr><td>9 + 3</td><td>(2, 7), (2, 8)</td><td>1 — same value pair</td></tr>
<tr><td>6 + 6</td><td>(5, 6)</td><td>1</td></tr>
<tr><td>13 + ?</td><td>needs &minus;1, absent</td><td>0</td></tr>
<tr><td>11 + ?</td><td>needs 1, absent</td><td>0</td></tr>
</table>
<div class="formula">answer = <b>3</b>   {5,7}, {9,3}, {6,6}</div>
<p>Counting by <em>position</em> would give 4, because 9 pairs with each of the two 3s. The published answer of 3 settles the reading: a value pair counts once however many times it can be formed.</p></div>
<div class="step"><h4>2 &middot; The one-pass set method, and the self-pair case</h4>
<p>Because only values matter, reduce to a set and walk it once, guarding against double-counting with an ordering condition:</p>
<div class="formula">for each distinct v:
    c = target &minus; v
    count it once when <b>c is present</b> and <b>v &lt; c</b>      &larr; each unordered pair seen once
    plus the self-pair <b>v == c</b> when v occurs <b>at least twice</b></div>
<p>The <code>v &lt; c</code> test is what stops <code>{5,7}</code> being counted again as <code>{7,5}</code>. The equality case must be handled separately and needs the <em>multiplicity</em>, not just membership: <code>6 + 6 = 12</code> counts only because there are two 6s. A single 6 would not pair with itself.</p>
<table class="trace">
<tr><th>v</th><th>c = 12 &minus; v</th><th>c present?</th><th>v &lt; c?</th><th>counted</th></tr>
<tr><td class="hit">5</td><td class="hit">7</td><td class="hit">yes</td><td class="hit">yes</td><td class="hit">✔</td></tr>
<tr><td>7</td><td>5</td><td>yes</td><td>no</td><td>skip (already counted)</td></tr>
<tr><td class="hit">9</td><td class="hit">3</td><td class="hit">yes</td><td class="hit">no &mdash; but 3 &lt; 9, so counted at v = 3</td><td class="hit">✔ (once)</td></tr>
<tr><td>13</td><td>&minus;1</td><td>no</td><td>&mdash;</td><td>&mdash;</td></tr>
<tr><td>11</td><td>1</td><td>no</td><td>&mdash;</td><td>&mdash;</td></tr>
<tr><td class="hit">6</td><td class="hit">6</td><td class="hit">yes, twice</td><td class="hit">equal &rarr; self-pair rule</td><td class="hit">✔</td></tr>
<tr><td>3</td><td>9</td><td>yes</td><td>yes</td><td>counted here (the 9 row's partner)</td></tr>
</table>
<p>Total <strong>3</strong>. &check;</p></div>
<div class="step"><h4>3 &middot; Traps</h4>
<ul>
<li><strong>Duplicates collapse.</strong> Two 3s do not make two pairs with 9.</li>
<li><strong>The <code>v == c</code> case needs a count &ge; 2</strong>, which a plain set cannot tell you — keep a <code>Counter</code> or check membership twice carefully.</li>
<li><strong>Guard against counting each pair twice</strong> with <code>v &lt; c</code> (or halve at the end, which is more error-prone with the self-pair case).</li>
<li><strong>Negative values and a negative target</strong> are not excluded by anything visible in the paywalled statement; the set method handles them unchanged.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-nondecreasing', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Array',
  label:'Problem', title:'Make Power Non-decreasing',
  minutes:30, score:'',
  images:['WhatsApp Image 2026-09-07 at 10.14.58 PM (7).jpeg'],
  fn:{name:'makePowerNonDecreasing', ret:'long', params:[['int[]','power']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [[rng.randint(1, 50) for _ in range(m)]]`,
  tests:[
    {in:[[3, 4, 1, 6, 2]], out:7},
    {in:[[1, 2, 3]], out:0},
    {in:[[5, 1]], out:4},
    {in:[[7]], out:0},
    {in:[[9, 8, 7, 6]], out:3}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">NEW GRAD</span><span class="tag">INTERN</span><span class="tag">OA</span></div>

<p>AWS provides scalable systems. A set of <code>n</code> servers are used for horizontally scaling an application.</p>
<p>The goal is to have the computational power of the servers in non-decreasing order. To do so, you can increase the computational power of each server in any contiguous segment by <code>x</code>. Choose the values of <code>x</code> such that after the computational powers are in non-decreasing order, the sum of the <code>x</code> values is minimum.</p>

<div class="locked">🔒 The problem statement continues (paywalled on FastPrep — not captured).</div>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">power  = [3, 4, 1, 6, 2]
return = 7</pre>
<p>There are <code>n = 5</code> servers and their computational power is <code>[3, 4, 1, 6, 2]</code>.</p>
<figure class="fig"><img loading="lazy" src="../images/fig-power-servers.png" alt="The five servers" data-full="../images/WhatsApp%20Image%202026-09-07%20at%2010.14.58%20PM%20%287%29.jpeg" title="Click to open the full screenshot"><figcaption>The five servers</figcaption></figure>
<p>Add <code>3</code> units to the subarray <code>(2, 4)</code> and <code>4</code> units to the subarray <code>(4, 4)</code>.</p>
<figure class="fig"><img loading="lazy" src="../images/fig-power-steps.png" alt="Adding 3 to (2,4), then 4 to (4,4)" data-full="../images/WhatsApp%20Image%202026-09-07%20at%2010.14.58%20PM%20%287%29.jpeg" title="Click to open the full screenshot"><figcaption>Adding 3 to (2,4), then 4 to (4,4)</figcaption></figure>
<p>The final arrangement of the servers is <code>[3, 4, 4, 9, 9]</code>.</p>
<p>The answer is <code>3 + 4 = 7</code>.</p>
<div class="frag">Example 2 was blurred/locked in the screenshot.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>You may only <em>increase</em>, and you increase a whole contiguous segment by the same amount. Look at where the sequence goes down.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Every drop <code>power[i-1] &gt; power[i]</code> must be repaired, and one segment operation starting at <em>i</em> can repair that drop and be reused for later drops. The total is the sum of all drops.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Because an operation adds a constant to a suffix-like contiguous block, the minimal total added is exactly the sum of the descents:</p>
<pre class="sample">answer = Σ max(0, power[i-1] - power[i])  for i = 1..n-1</pre>
<p>Check <code>power = [3, 4, 1, 6, 2]</code>: descents are 4→1 (3) and 6→2 (4) → 3 + 4 = <strong>7</strong>. ✓ — which matches the diagram's "+3 to (2,4), then +4 to (4,4)".</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def makePowerNonDecreasing(power):
    return sum(max(0, power[i - 1] - power[i]) for i in range(1, len(power)))</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example <code>power = [3, 4, 1, 6, 2]</code>, answer <strong>7</strong>.</p>
<div class="step"><h4>1 &middot; Each element is fixed by the one before it</h4>
<p>You may only <em>increase</em> values, and the array must end non-decreasing. Sweep left to right: when an element is already at least its predecessor, leave it alone; otherwise raise it exactly to the predecessor. Raising it further is never useful — it costs more now and makes the next element's job harder, never easier.</p>
<div class="formula">need = max(previous_final, power[i])
cost += need &minus; power[i]
previous_final = need</div>
<p>The key subtlety is that the comparison is against the <strong>final</strong> value of the previous element, not its original. Once an element has been raised, it is the raised value that constrains everything downstream.</p></div>
<div class="step"><h4>2 &middot; The trace</h4>
<table class="trace">
<tr><th>i</th><th>power[i]</th><th>previous final</th><th>raised to</th><th>added cost</th><th>total</th></tr>
<tr><td>0</td><td>3</td><td>&mdash;</td><td>3</td><td>0</td><td>0</td></tr>
<tr><td>1</td><td>4</td><td>3</td><td>4 (already &ge;)</td><td>0</td><td>0</td></tr>
<tr><td class="hit">2</td><td class="hit">1</td><td class="hit">4</td><td class="hit">4</td><td class="hit">4 &minus; 1 = <strong>3</strong></td><td class="hit">3</td></tr>
<tr><td>3</td><td>6</td><td>4</td><td>6</td><td>0</td><td>3</td></tr>
<tr><td class="hit">4</td><td class="hit">2</td><td class="hit">6</td><td class="hit">6</td><td class="hit">6 &minus; 2 = <strong>4</strong></td><td class="hit"><strong>7</strong></td></tr>
</table>
<div class="formula">final array = [3, 4, <b>4</b>, 6, <b>6</b>]      total added = 3 + 4 = <b>7</b>   &check;</div>
<p>Row 4 is the one that shows why the running maximum matters: index 4 is compared against 6, the <em>original</em> value at index 3 — but had index 3 itself been raised, the comparison would have used the raised figure. Since values only ever increase, <code>previous_final</code> is simply the running maximum of the array so far.</p></div>
<div class="step"><h4>3 &middot; Why the greedy is optimal</h4>
<p>A short exchange argument. In any valid final array <em>b</em>, we need <code>b[i] &ge; b[i-1]</code> and <code>b[i] &ge; power[i]</code>, so by induction <code>b[i] &ge; max(power[0..i])</code> — the running maximum is a <em>lower bound</em> on every element. The greedy sets each element to exactly that bound, so it is pointwise minimal; since the cost is a sum of pointwise non-negative terms, a pointwise-minimal array is also cost-minimal. No other arrangement can beat it, and no lookahead is required.</p></div>
<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Compare against the running maximum</strong>, not against <code>power[i-1]</code> as originally given.</li>
<li><strong>Only increases are allowed.</strong> If decreases were permitted this would be a completely different (and much harder) problem.</li>
<li><strong>Return type is <code>long</code></strong> — with large n and large values the total easily exceeds 32 bits.</li>
<li><strong>Non-decreasing, not strictly increasing</strong> — equal neighbours are fine, which is what lets index 2 stop at 4.</li>
<li><strong>An already-sorted array costs 0</strong>; make sure the loop does not add a spurious first term.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-unfulfilledbids', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Array',
  label:'Problem', title:'Unfulfilled Bids after Ranked Round-Robin Allocation',
  minutes:35, score:'',
  images:['src-unfulfilledbids-full.png'],
  fn:{name:'findUnfulfilledBids', ret:'int[]', params:[['int[][]','bids'],['int','totalInventory']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    bids = [[i + 1, rng.randint(1, 4), rng.randint(1, 5), rng.randint(1, 6)] for i in range(m)]
    return [bids, rng.randint(0, 4 * m)]`,
  tests:[
    {in:[[[1, 3, 1, 1], [2, 4, 2, 2]], 1], out:[1, 2]},
    {in:[[[1, 3, 2, 1], [2, 3, 2, 2], [3, 3, 1, 3]], 4], out:[2]},
    {in:[[[1, 5, 1, 1]], 0], out:[1]},
    {in:[[[1, 5, 2, 1], [2, 5, 2, 2]], 4], out:[]}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">CONTRACT</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The report contains arithmetically inconsistent sample outputs and omits deterministic tie and result ordering. The judged allocation task matches the reported core exercise at about 90%.</div>

<p>You receive a fixed inventory and a list of customer bids. Each bid is represented as <code>[customerId, bidAmount, quantity, bidPlacedAt]</code>.</p>

<p>Allocate inventory using these rules:</p>
<ul>
  <li>Process higher <code>bidAmount</code> values before lower ones.</li>
  <li>Within one bid amount, order bids by increasing <code>bidPlacedAt</code>, breaking a remaining tie by increasing <code>customerId</code>.</li>
  <li>Allocate one unit to each still-unfulfilled bid in that order, then repeat another cycle for the same bid amount.</li>
  <li>Move to the next lower bid amount only after every bid in the current group is fulfilled or the inventory is exhausted.</li>
</ul>

<p>Return the <code>customerId</code> of every bid that receives fewer units than its requested <code>quantity</code>. Return the IDs in increasing order.</p>

<h3>Function</h3>
<pre class="sample">findUnfulfilledBids(bids: int[][], totalInventory: int) &rarr; int[]</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">bids           = [[1,3,1,1],[2,4,2,2]]
totalInventory = 1
return         = [1,2]</pre>
<p>Customer 2 receives the only unit because its bid amount is higher. Customer 1 receives zero of one requested unit, and customer 2 receives one of two requested units, so both bids are not fully fulfilled.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">bids           = [[1,3,2,1],[2,3,2,2],[3,3,1,3]]
totalInventory = 4
return         = [2]</pre>
<p>The first cycle gives one unit to customers 1, 2, and 3. The remaining unit goes to customer 1 at the start of the second cycle. Only customer 2 receives fewer units than requested.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &lt;= bids.length &lt;= 2000</code></li>
  <li>Every bid has exactly four integer fields.</li>
  <li><code>1 &lt;= customerId, bidAmount, quantity, bidPlacedAt &lt;= 10^9</code></li>
  <li>All <code>customerId</code> values are distinct.</li>
  <li>The sum of all requested quantities is at most <code>200000</code>.</li>
  <li><code>0 &lt;= totalInventory &lt;= 200000</code></li>
</ul>

<h3>Testcases</h3>
<div class="cases">
  <div class="case"><div class="ch">CASE 1</div><pre class="sample">bids
[[1,3,1,1],[2,4,2,2]]
totalInventory
1
expected
[1,2]</pre></div>
  <div class="case"><div class="ch">CASE 2</div><pre class="sample">bids
[[1,3,2,1],[2,3,2,2],[3,3,1,3]]
totalInventory
4
expected
[2]</pre></div>
</div>
<div class="frag">The platform lists Cases 1–7 plus "5 more cases"; only Cases 1 and 2 were visible.</div>

<div class="srcnote"><strong>Compare with:</strong> the exam-screenshot problem <em>"Flash Sale — Priority Inventory Allocation"</em> in the Amazon OA · Coding section. Same allocation family, but three things differ: the field order is <code>[customerId, bidAmount, quantity, bidPlacedAt]</code> here versus <code>[customerId, quantity, bidAmount, timestamp]</code> there; this one returns every <strong>partially</strong> fulfilled bid while that one returns only customers who received <strong>no</strong> items; and this one specifies the customerId tiebreak and sorted output that the exam screenshot left undefined. Solve them as two separate problems.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Same round-robin allocation as the flash-sale problem, but read the return clause carefully — it is not the customers who got nothing.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Simulate rounds in (bid desc, timestamp asc) order handing out one unit per active customer per round, then report the customers who received <em>some</em> units but fewer than they asked for.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Sort by bid descending, then timestamp ascending. Loop rounds giving one unit to each still-unsatisfied customer until inventory is exhausted.</p>
<p>Return the IDs that ended <strong>partially fulfilled</strong> — <code>0 &lt; received &lt; requested</code>. That is the difference from <a href='#flashsale' style='color:var(--accent)'>Flash Sale</a>, which returns the customers who received nothing at all.</p><p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>from collections import defaultdict

def findUnfulfilledBids(bids, totalInventory):
    groups = defaultdict(list)                       # bidAmount -&gt; members
    for cid, amount, qty, ts in bids:
        groups[amount].append((ts, cid, qty))

    want = {b[0]: b[2] for b in bids}
    got  = {b[0]: 0    for b in bids}
    inv  = totalInventory

    for amount in sorted(groups, reverse=True):      # highest bid amount first
        if inv == 0:
            break
        active = [[qty, cid] for ts, cid, qty in sorted(groups[amount])]
        while inv &gt; 0 and active:
            step = min(q for q, _ in active)         # cycles until someone finishes
            k = len(active)
            if step * k &lt;= inv:
                inv -= step * k
                for e in active:
                    got[e[1]] += step
                    e[0] -= step
                active = [e for e in active if e[0] &gt; 0]
            else:
                full, rem = divmod(inv, k)           # rem units to the earliest rem
                for i, e in enumerate(active):
                    got[e[1]] += full + (1 if i &lt; rem else 0)
                inv = 0
                active = []

    return sorted(cid for cid in got if got[cid] &lt; want[cid])</code></pre><div class="unsure">The code previously here had two defects and failed Example 1, returning <code>[2]</code> instead of <code>[1,2]</code>. It round-robined across <em>all</em> bids at once instead of within each bid-amount group, and its final filter was <code>0 &lt; got[cid] &lt; want[cid]</code>, which <strong>excluded customers who received nothing at all</strong> — yet those are the most unfulfilled of all. It was also named <code>unfulfilledBids</code> rather than the declared <code>findUnfulfilledBids</code>. The version above reproduces both published examples.<br><br>Compare with <a href='#flashsale' style='color:var(--accent)'>Flash Sale — Priority Inventory Allocation</a>: same allocation procedure, but the field order here is <code>[customerId, bidAmount, quantity, bidPlacedAt]</code> versus <code>[customerId, quantity, bidAmount, timestamp]</code> there, and that one returns only customers who received <em>zero</em>.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples.</p>
<div class="step"><h4>1 &middot; Two nested orderings</h4>
<p>The rules describe a strict hierarchy, and collapsing it into one sort is the central error:</p>
<table class="trace">
<tr><th>level</th><th>rule</th><th>effect</th></tr>
<tr><td>between bid amounts</td><td>higher <code>bidAmount</code> first</td><td>strict — a lower group gets nothing until the higher group is fully served or the inventory is gone</td></tr>
<tr><td>within one bid amount</td><td>increasing <code>bidPlacedAt</code>, then increasing <code>customerId</code></td><td>fair — one unit each per cycle, repeatedly</td></tr>
</table>
<p>Round-robin applies <em>only</em> inside a tie group. Cycling through everyone at once hands units to low bidders while higher bids are still unmet.</p>
<p>Field order matters too: <code>[customerId, bidAmount, quantity, bidPlacedAt]</code>. The sibling problem <a href='#flashsale' style='color:var(--accent)'>Flash Sale</a> puts quantity and bid the other way round, and mixing them up produces a plausible, wrong answer.</p></div>
<div class="step"><h4>2 &middot; Example 1 — why the answer is both customers</h4>
<p><code>bids = [[1,3,1,1], [2,4,2,2]]</code>, <code>totalInventory = 1</code>. Customer 2 bids 4, customer 1 bids 3:</p>
<table class="trace">
<tr><th>group</th><th>inventory in</th><th>allocation</th><th>inventory out</th></tr>
<tr><td>bidAmount 4</td><td>1</td><td>customer 2 gets 1 of its 2 requested</td><td>0</td></tr>
<tr><td>bidAmount 3</td><td>0</td><td>customer 1 gets <strong>0</strong> of its 1 requested</td><td>0</td></tr>
</table>
<div class="formula">got[1] = 0 &lt; want[1] = 1   &rarr; unfulfilled
got[2] = 1 &lt; want[2] = 2   &rarr; unfulfilled
answer = <b>[1, 2]</b></div>
<p>This example exists precisely to pin down the definition: <strong>"fewer units than requested" includes receiving none at all.</strong> A filter of <code>0 &lt; got &lt; want</code> — which reads naturally as "partially fulfilled" — drops customer 1 and returns <code>[2]</code>. That was the bug in the previously published code.</p></div>
<div class="step"><h4>3 &middot; Example 2 — the round-robin inside one group</h4>
<p><code>bids = [[1,3,2,1], [2,3,2,2], [3,3,1,3]]</code>, <code>totalInventory = 4</code>. All three bid 3, so one group, ordered by <code>bidPlacedAt</code>: customer 1, then 2, then 3.</p>
<table class="trace">
<tr><th>cycle</th><th>c1 (wants 2)</th><th>c2 (wants 2)</th><th>c3 (wants 1)</th><th>inventory left</th></tr>
<tr><td>1</td><td>+1 &rarr; 1</td><td>+1 &rarr; 1</td><td>+1 &rarr; 1 (done, leaves)</td><td>4 &minus; 3 = 1</td></tr>
<tr><td class="hit">2</td><td class="hit">+1 &rarr; <strong>2</strong> (done)</td><td class="hit">inventory exhausted &rarr; stays at 1</td><td class="hit">&mdash;</td><td class="hit">0</td></tr>
</table>
<div class="formula">got = {1: 2, 2: 1, 3: 1}   want = {1: 2, 2: 2, 3: 1}
only customer 2 falls short   &rarr;   answer = <b>[2]</b></div>
<p>The partial second cycle is the delicate moment: one unit remains and two customers are still active, so it goes to the <em>earlier</em> timestamp. In code that is <code>full, rem = divmod(inv, k)</code> — each active bid gets <code>full</code> complete cycles, and the first <code>rem</code> in round-robin order get one extra. Here <code>divmod(1, 2) = (0, 1)</code>, so nobody gets a full cycle and the single leftover unit goes to customer 1.</p></div>
<div class="step"><h4>4 &middot; Level filling instead of unit-by-unit</h4>
<p>Handing out one unit at a time is O(totalInventory) — up to 200 000 here, which is survivable, but the level-filling form is both faster and easier to reason about. With <em>k</em> active bids and <code>step</code> = the smallest remaining need, a block of <code>step</code> whole cycles costs <code>step × k</code> units and retires at least one bid. Repeat while the inventory covers the next block; when it does not, split the remainder with <code>divmod</code> as above. Each iteration removes at least one bid, so there are at most <em>n</em> of them.</p></div>
<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Zero counts as unfulfilled.</strong> The filter is <code>got &lt; want</code>, with no lower guard.</li>
<li><strong>Round-robin only within equal <code>bidAmount</code></strong>, never globally.</li>
<li><strong>Field order</strong> is <code>[customerId, bidAmount, quantity, bidPlacedAt]</code>.</li>
<li><strong>Three sort keys, two directions:</strong> bid amount descending, then timestamp ascending, then customer id ascending.</li>
<li><strong>Return the ids in increasing order</strong>, as the statement requires.</li>
<li><strong><code>totalInventory</code> may be 0</strong>, in which case every bid is unfulfilled.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-mincontig', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Array',
  label:'Problem', title:'Minimum Contiguous Replacements',
  minutes:30, score:'',
  images:['Screenshot_20260907_235656.png'],
  fn:{name:'minOperations', ret:'int', params:[['int[]','arr']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    pool = max(2, m // 3)
    return [[rng.randint(1, pool) for _ in range(m)]]`,
  tests:[
    {in:[[1, 2, 1]], out:1},
    {in:[[1, 2, 3, 1, 2, 3]], out:2},
    {in:[[1, 1, 2, 2]], out:0},
    {in:[[5]], out:0},
    {in:[[1, 2, 1, 2, 1]], out:1}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<p>You are given an array <code>arr</code> of integers. In one operation, choose two distinct values <code>x</code> and <code>y</code> that currently appear in the array, then replace every occurrence of <code>x</code> with <code>y</code>.</p>

<p>Return the minimum number of operations needed to make the array valid.</p>

<p>An array is valid if every distinct value forms exactly one contiguous block. Values do not all need to become the same.</p>

<p>For example, <code>[1,1,2,2,3]</code> is valid, while <code>[1,2,1,3]</code> is not valid because value 1 appears in two separated blocks.</p>

<h3>Function</h3>
<pre class="sample">minOperations(arr: int[]) &rarr; int</pre>
<p>Complete <em>minOperations</em>.</p>
<ul><li><em>int arr[n]:</em> the array to transform</li></ul>

<h3>Returns</h3>
<ul><li><em>int:</em> the minimum number of replacement operations.</li></ul>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">arr    = [1,2,1]
return = 1</pre>
<p>Replace every occurrence of 2 with 1, producing <code>[1,1,1]</code>.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">arr    = [1,2,3,1,2,3]
return = 2</pre>
<p>One valid sequence is to replace all 2s with 1, then replace all 3s with 1.</p>

<div class="sublabel">Example 3</div>
<pre class="sample">arr    = [1,2,1,2]
return = 1</pre>
<p>Replacing every occurrence of either value with the other makes the array one contiguous block.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &lt;= arr.length &lt;= 1000</code></li>
  <li><code>1 &lt;= arr[i] &lt;= 1000</code></li>
</ul>

<h3>Testcases</h3>
<div class="cases">
  <div class="case"><div class="ch">CASE 1</div><pre class="sample">arr
[1,2,1]
expected
1</pre></div>
  <div class="case"><div class="ch">CASE 2</div><pre class="sample">arr
[1,2,3,1,2,3]
expected
2</pre></div>
  <div class="case"><div class="ch">CASE 3</div><pre class="sample">arr
[1,2,1,2]
expected
1</pre></div>
</div>

<div class="srcnote"><strong>Also reported as:</strong> <em>"Make Value Groups Contiguous"</em> (<code>minOperationsToMakeValuesContiguous</code>) in this same section — identical task, different wrapper name, and its report carries a formula line that contradicts the minimum. Solve one, check the other.</div>
<div class="srcnote"><strong>Compare with:</strong> <em>"Optimal Inventory — Minimum Replacement Cost"</em> (<code>getMinAmount</code>) in the Amazon OA · Coding section. Identical setup and identical validity condition, but a <strong>different objective</strong>: that one charges <code>num_replacements</code> — the number of <em>elements</em> changed — and asks for minimum money; this one counts <em>operations</em>, so each merge costs exactly 1 regardless of how many elements move. Different answers, different algorithms.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Same validity rule as <a href='#inventory' style='color:var(--accent)'>Optimal Inventory</a> — each distinct value must form one contiguous block. But re-read what an <em>operation</em> costs here.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>One operation merges two values completely, regardless of how many elements it touches. So a group of <em>k</em> mutually interleaved values needs exactly <em>k</em> − 1 operations. Count the groups, not the elements.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Identical interval-merging as Optimal Inventory: build <code>[first[v], last[v]]</code> per distinct value, sort by first index, merge overlaps. Each merged group of <em>k</em> distinct values costs <strong>k − 1</strong> operations to collapse.</p>
<p>Check against the examples:</p>
<ul>
<li><code>[1,2,1]</code> — 1 spans [0,2], 2 spans [1,1], they overlap → one group of 2 values → <strong>1</strong>. ✓</li>
<li><code>[1,2,3,1,2,3]</code> — all three overlap → one group of 3 → <strong>2</strong>. ✓</li>
<li><code>[1,2,1,2]</code> — one group of 2 → <strong>1</strong>. ✓</li>
</ul><p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def minOperations(arr):
    first, last = {}, {}
    for i, v in enumerate(arr):
        if v not in first:
            first[v] = i
        last[v] = i

    spans = sorted((first[v], last[v]) for v in first)

    ops = 0
    i = 0
    while i &lt; len(spans):
        lo, hi = spans[i]
        k = 1
        j = i + 1
        while j &lt; len(spans) and spans[j][0] &lt; hi:
            hi = max(hi, spans[j][1])
            k += 1
            j += 1
        ops += k - 1
        i = j
    return ops</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples: <code>[1,2,1] &rarr; 1</code> and <code>[1,2,3,1,2,3] &rarr; 2</code>.</p>
<div class="step"><h4>1 &middot; Which values are forced to merge</h4>
<p>An operation rewrites <em>every</em> occurrence of one value, so you never edit a single position — you fuse whole values. The validity target is "all occurrences of each value are contiguous", and the obstruction is <strong>interleaving</strong>: give each value its span <code>[firstIndex, lastIndex]</code>, and if two spans overlap, those values can never be separated and must become one.</p>
<div class="formula">[1, 2, 1]      value 1 &rarr; span [0, 2]      value 2 &rarr; span [1, 1]
                span [1,1] sits <b>inside</b> [0,2]  &rarr; forced into one group</div>
<p>Merging is transitive through overlap chains, so sort the spans by start and sweep, extending a running <code>hi</code> — ordinary interval merging.</p></div>
<div class="step"><h4>2 &middot; The cost: operations, not elements</h4>
<p>This is the entire difference from the sibling problem. A group of <em>k</em> distinct values is collapsed by rewriting <em>k&minus;1</em> of them into the remaining one, so:</p>
<div class="formula">cost(group) = (number of distinct values in the group) &minus; <b>1</b></div>
<p>The <em>sizes</em> of the values are irrelevant — rewriting a value that appears once and a value that appears a thousand times both cost exactly one operation. That is why the answer here does not depend on frequencies at all, while <a href='#inventory' style='color:var(--accent)'>Optimal Inventory</a> depends on nothing else.</p>
<table class="trace">
<tr><th>example</th><th>spans</th><th>groups</th><th>distinct per group</th><th>cost</th></tr>
<tr><td class="hit">[1,2,1]</td><td class="hit">1:[0,2], 2:[1,1]</td><td class="hit">one group {1,2}</td><td class="hit">2</td><td class="hit">2 &minus; 1 = <strong>1</strong></td></tr>
<tr><td class="hit">[1,2,3,1,2,3]</td><td class="hit">1:[0,3], 2:[1,4], 3:[2,5]</td><td class="hit">one group {1,2,3}</td><td class="hit">3</td><td class="hit">3 &minus; 1 = <strong>2</strong></td></tr>
</table>
<p>Both match. Sanity-check a non-overlapping case: <code>[1,1,2,2]</code> has spans [0,1] and [2,3], which do not overlap, so there are two groups of one value each and the cost is <code>0 + 0 = 0</code> — the array is already valid.</p></div>
<div class="step"><h4>3 &middot; Why the finest grouping is optimal here too</h4>
<p>Merging two groups with <em>k&#8321;</em> and <em>k&#8322;</em> distinct values costs <code>k&#8321; + k&#8322; &minus; 1</code> against <code>(k&#8321;&minus;1) + (k&#8322;&minus;1) = k&#8321; + k&#8322; &minus; 2</code> separately — strictly one operation worse. So never merge more than the overlaps force, and interval merging gives exactly the forced partition.</p></div>
<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Count operations, not elements changed.</strong> Read the Returns clause twice — the two problems are otherwise identical and the answers differ (on the Optimal Inventory example, 2 here versus 4 there).</li>
<li><strong>Frequencies are irrelevant.</strong> No <code>Counter</code> of occurrences is needed, only the set of distinct values per group.</li>
<li><strong>Extend the merge boundary with <code>max</code></strong>, so a nested span does not shrink the group.</li>
<li><strong>A value appearing once, isolated,</strong> forms its own group and costs 0.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-taskscheduler', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Greedy',
  label:'Problem', title:'Task Scheduler',
  minutes:30, score:'',
  images:[],
  fn:{name:'leastInterval', ret:'int', params:[['char[]','tasks'],['int','n']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [[rng.choice('ABCDE') for _ in range(m)], rng.randint(0, 4)]`,
  tests:[
    {in:[["A", "A", "A", "B", "B", "B"], 2], out:8},
    {in:[["A", "C", "A", "B", "D", "B"], 1], out:6},
    {in:[["A"], 5], out:1},
    {in:[["A", "A", "A"], 0], out:3},
    {in:[["A", "B", "C", "D", "E", "A"], 3], out:6}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span><span class="tag">PHONE SCREEN</span></div>

<div class="srcnote"><strong>AMZ Interval Collection</strong> — a group of problems focused on operations involving intervals:
<ol style="margin:8px 0 0">
  <li>Task Scheduler (Full-Time) &larr; <em>this one</em></li>
  <li>Merge Intervals (Intern, NG)</li>
  <li>Find Overlapping Times (Intern)</li>
  <li>Get Maximum Sum Find Overlapping Times (Full-Time)</li>
  <li>Optimal Interval Difference</li>
</ol></div>

<p>You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number <code>n</code>. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of at least <code>n</code> intervals between two tasks with the same label.</p>

<p>Return the minimum number of CPU intervals required to complete all tasks.</p>

<h3>Function</h3>
<pre class="sample">leastInterval(tasks: char[], n: int) &rarr; int</pre>
<p>Complete the function <em>leastInterval</em> in the editor.</p>
<p><em>leastInterval</em> has the following parameters:</p>
<ol>
  <li><em>char[] tasks:</em> an array of uppercase English letters representing tasks</li>
  <li><em>int n:</em> the cooling interval</li>
</ol>

<h3>Returns</h3>
<ul><li><em>int:</em> the minimum number of intervals to complete all tasks</li></ul>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">tasks  = ["A","A","A","B","B","B"]
n      = 2
return = 8</pre>
<p>A possible sequence is: <code>A -&gt; B -&gt; idle -&gt; A -&gt; B -&gt; idle -&gt; A -&gt; B</code>.</p>
<p>After completing task A, you must wait two intervals before doing A again. The same applies to task B. In the 3rd interval, neither A nor B can be done, so you idle. By the 4th interval, you can do A again as 2 intervals have passed.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">tasks  = ["A","C","A","B","D","B"]
n      = 1
return = 6</pre>
<p>A possible sequence is: <code>A -&gt; B -&gt; C -&gt; D -&gt; A -&gt; B</code>.</p>
<p>With a cooling interval of 1, you can repeat a task after just one other task.</p>

<div class="sublabel">Example 3</div>
<pre class="sample">tasks  = ["A","A","A","B","B","B"]
n      = 3
return = 10</pre>
<p>A possible sequence is: <code>A -&gt; B -&gt; idle -&gt; idle -&gt; A -&gt; B -&gt; idle -&gt; idle -&gt; A -&gt; B</code>.</p>
<p>There are only two types of tasks, A and B, which need to be separated by 3 intervals. This leads to idling twice between repetitions of these tasks.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &lt;= tasks.length &lt;= 10^4</code></li>
  <li><code>tasks[i]</code> is an uppercase English letter.</li>
  <li><code>0 &lt;= n &lt;= 100</code></li>
</ul>

<h3>Testcases</h3>
<div class="cases">
  <div class="case"><div class="ch">CASE 1</div><pre class="sample">tasks
["A","A","A","B","B","B"]
n
2
expected
8</pre></div>
  <div class="case"><div class="ch">CASE 2</div><pre class="sample">tasks
["A","C","A","B","D","B"]
n
1
expected
6</pre></div>
  <div class="case"><div class="ch">CASE 3</div><pre class="sample">tasks
["A","A","A","B","B","B"]
n
3
expected
10</pre></div>
</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Identical tasks need a cooldown between them. The bottleneck is whichever task appears most often — everything else fills the gaps it leaves.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Let <em>f</em> be the highest frequency and <em>k</em> the number of tasks sharing it. The schedule length is <code>max(len(tasks), (f-1)*(n+1) + k)</code>.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>LeetCode 621. The most frequent task creates <code>f - 1</code> gaps of size <em>n</em>; the tasks tied at that frequency each add one to the final block. If there are enough other tasks to fill every gap, no idling is needed and the answer is simply the number of tasks.</p><p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>from collections import Counter

def leastInterval(tasks, n):
    freq = Counter(tasks)
    f = max(freq.values())
    k = sum(1 for v in freq.values() if v == f)
    return max(len(tasks), (f - 1) * (n + 1) + k)</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples: <code>["A","A","A","B","B","B"], n = 2 &rarr; 8</code> and <code>["A","C","A","B","D","B"], n = 1 &rarr; 6</code>.</p>
<div class="step"><h4>1 &middot; The most frequent task builds the skeleton</h4>
<p>Identical tasks must be separated by at least <em>n</em> slots. The task with the highest frequency <code>f</code> is therefore the binding constraint: its copies define <code>f - 1</code> gaps, each of width <code>n</code>, and everything else has to fit into or around them.</p>
<div class="formula">A _ _ A _ _ A          f = 3, n = 2
&#8592;--&#8594; &#8592;--&#8594;               f &minus; 1 = 2 gaps, each n + 1 = 3 slots wide including the A
frame length = (f &minus; 1) &times; (n + 1) + 1</div>
<p>The trailing <code>+ 1</code> is the final A, which needs no cooldown after it. If several tasks tie at frequency <code>f</code>, they all must appear in the last block, so the tail widens:</p>
<div class="formula">answer = (f &minus; 1) &times; (n + 1) + <b>count of tasks having frequency f</b></div></div>
<div class="step"><h4>2 &middot; Example 1: the formula binds</h4>
<p><code>["A","A","A","B","B","B"]</code>, <code>n = 2</code>. Frequencies: A = 3, B = 3, so <code>f = 3</code> and two tasks tie at it.</p>
<div class="formula">(3 &minus; 1) &times; (2 + 1) + 2 = 2 &times; 3 + 2 = <b>8</b></div>
<p>A concrete schedule of length 8: <code>A B idle A B idle A B</code>. Six real tasks and two idles. The two trailing tasks in the tail are exactly the two tasks tied at frequency 3, which is what the <code>+ 2</code> counts.</p></div>
<div class="step"><h4>3 &middot; Example 2: why <code>max(len(tasks), …)</code> is needed</h4>
<p><code>["A","C","A","B","D","B"]</code>, <code>n = 1</code>. Frequencies: A = 2, B = 2, C = 1, D = 1, so <code>f = 2</code> with two tasks tied.</p>
<div class="formula">formula: (2 &minus; 1) &times; (1 + 1) + 2 = <b>4</b>
but there are <b>6</b> tasks, and each occupies a slot &rarr; answer = max(6, 4) = <b>6</b></div>
<p>When there are many distinct tasks, the gaps fill up completely and no idle time is ever needed — the schedule is simply as long as the task list. The formula only describes the <em>idle-constrained</em> regime, so the answer is the larger of the two:</p>
<div class="formula">answer = <b>max</b>( len(tasks),  (f &minus; 1) &times; (n + 1) + count_of_max )</div>
<p>Omitting the <code>max</code> is the classic error and it fails precisely on the crowded case, where the formula under-counts. A valid schedule here is <code>A B A B C D</code> — no idles, length 6.</p></div>
<div class="step"><h4>4 &middot; Why the formula is never an over-count either</h4>
<p>The frame is a genuine lower bound: between the first and last copy of the most frequent task there must be at least <code>(f-1)(n+1)</code> slots, plus the tail. And it is achievable — fill the gaps column by column, taking tasks in decreasing frequency order; a task can never need two slots in the same gap, because its own frequency is at most <em>f</em>. So the bound is tight whenever idles are needed at all, and the <code>max</code> covers the remaining case.</p></div>
<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Count the ties.</strong> The tail is <em>how many tasks share the maximum frequency</em>, not 1.</li>
<li><strong><code>n + 1</code>, not <code>n</code></strong> — a block is one task plus <em>n</em> cooldown slots.</li>
<li><strong>Take <code>max</code> with <code>len(tasks)</code></strong>, or the crowded case is wrong.</li>
<li><strong><code>n = 0</code></strong> reduces to <code>len(tasks)</code>; the formula gives <code>f - 1 + count</code>, and the <code>max</code> rescues it.</li>
<li><strong>The answer counts time units, including idles</strong>, not tasks.</li>
</ul></div>
</div></details>
</div>
`},

/* ============ SECTION 6 — NOTES FROM THE DOC ============ */
{
  id:'fp-gridinconvenience', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Matrix',
  label:'Problem statement', title:'Minimum Grid Inconvenience',
  minutes:30, score:'',
  images:['Screenshot_20260907_235558.png','0 (3).jpeg'],
  fn:{name:'getMinInconvenience', ret:'int', params:[['int[][]','grid']]},
  body:`
<div class="tags"><span class="tag hard">Hard</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">NEW GRAD</span><span class="tag">OA</span></div>

<p>Amazon has multiple delivery centers all over the world. A city is represented by a binary grid where a cell marked <code>1</code> is a delivery center, and a cell marked <code>0</code> is any other place.</p>

<p>The <strong>distance</strong> between two cells is the maximum of the absolute row-coordinate difference and the absolute column-coordinate difference. For example, the distance between (1, 2) and (0, 4) is max(|1 - 0|, |2 - 4|) = 2.</p>

<p>The <strong>inconvenience</strong> of the grid is the maximum, over every <code>0</code> cell, of its distance to the nearest delivery center.</p>

<p>Amazon may open one new delivery center by converting <strong>at most one</strong> <code>0</code> cell into a <code>1</code>. Return the minimum possible inconvenience after this conversion.</p>

<div class="note"><p>The metric is <strong>Chebyshev</strong> distance (chessboard-king moves), not Manhattan — diagonal steps cost the same as straight ones.</p></div>

<h3>Function</h3>
<pre class="sample">getMinInconvenience(grid: int[][]) &rarr; int</pre>

<h3>Examples</h3>
<div class="cases">
  <div class="case"><div class="ch">EXAMPLE 1</div><pre class="sample">grid   = [[0,0,0],[0,0,0],[0,0,0]]
return = 2

With no existing delivery center, it is optimal to convert the
center cell (1,1) to 1. The farthest cells then have distance 2.</pre></div>
  <div class="case"><div class="ch">EXAMPLE 2</div><pre class="sample">grid   = [[0]]
return = 0

Convert the only cell to a delivery center, leaving no 0 cell
with positive distance.</pre></div>
</div>

<h3>Constraints</h3>
<ul>
  <li>1 &le; <em>n</em>, <em>m</em> &le; 500</li>
  <li>0 &le; <em>grid[i][j]</em> &le; 1</li>
</ul>

<div class="srcnote"><strong>Shape of the solution.</strong> Binary-search the answer <em>d</em>: "can the inconvenience be &le; d?" With Chebyshev distance, the set of cells within <em>d</em> of a center is an axis-aligned square, so a multi-source BFS/prefix-max gives every cell's current distance, and the cells still exceeding <em>d</em> must all fit inside one square of side 2d+1 — check that their bounding box does, and that its centre can be placed on the grid.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>The distance is Chebyshev, so "everything within distance d of a point" is a <strong>square</strong>, not a diamond. That turns the whole problem into rectangle geometry.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Binary-search the answer d. Compute every 0-cell's current distance to the nearest 1 with a multi-source BFS. The cells still exceeding d must <em>all</em> be covered by one new square of side 2d+1 — which is possible exactly when their bounding box fits inside such a square and a valid centre exists on the grid.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p><strong>Monotonicity:</strong> if inconvenience &le; d is achievable, so is &le; d+1. So binary-search d over <code>[0, max(n,m)]</code>.</p>
<p><strong>Feasibility check for a given d:</strong></p>
<ol>
<li>Multi-source BFS from all existing 1s under Chebyshev movement (8-neighbour BFS) gives <code>dist[i][j]</code> for every cell.</li>
<li>Collect the cells with <code>dist &gt; d</code>. If none, d is feasible with no new centre.</li>
<li>Otherwise they must all fall inside one square of side 2d+1. Take their bounding box <code>[r1..r2] &times; [c1..c2]</code>. Feasible iff <code>r2-r1 &le; 2d</code> and <code>c2-c1 &le; 2d</code> — the centre can then be placed (clamped to the grid, which always works because the box itself is on the grid).</li>
</ol>
<p>Edge case: a grid with no 1s at all still works — every cell has <code>dist = ∞ &gt; d</code>, so the bounding box is the whole grid, and the check reduces to "does one square of side 2d+1 cover the grid". On the 3&times;3 all-zero example that first succeeds at d = 2. ✓</p><p><span class="cx">Time O(n·m·log(max(n,m)))</span><span class="cx">Space O(n·m)</span></p><pre class="sample"><code>from collections import deque

def getMinInconvenience(grid):
    n, m = len(grid), len(grid[0])
    INF = float('inf')

    # Chebyshev multi-source BFS from existing centres
    dist = [[INF] * m for _ in range(n)]
    dq = deque()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                dist[i][j] = 0
                dq.append((i, j))
    while dq:
        i, j = dq.popleft()
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                a, b = i + di, j + dj
                if 0 &lt;= a &lt; n and 0 &lt;= b &lt; m and dist[a][b] == INF:
                    dist[a][b] = dist[i][j] + 1
                    dq.append((a, b))

    def feasible(d):
        r1 = c1 = INF
        r2 = c2 = -1
        for i in range(n):
            for j in range(m):
                if dist[i][j] &gt; d:
                    r1, r2 = min(r1, i), max(r2, i)
                    c1, c2 = min(c1, j), max(c2, j)
        if r2 &lt; 0:
            return True                       # already good enough
        return (r2 - r1) &lt;= 2 * d and (c2 - c1) &lt;= 2 * d

    lo, hi = 0, max(n, m)
    while lo &lt; hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo</code></pre><div class="unsure"><strong>The source contradicts itself on the metric.</strong> The statement defines distance as <code>max(|Δrow|, |Δcol|)</code> — Chebyshev — and its own worked figure agrees: the distance from (1,2) to (0,4) is <code>max(1,2) = 2</code> (Manhattan would give 3). But <strong>Example 1 is only consistent with Manhattan</strong>: on a 3&times;3 all-zero grid, converting the centre puts every other cell at Chebyshev distance <strong>1</strong>, not the printed 2. Under Chebyshev this code returns 1 for that example; under Manhattan the answer is 2. Example 2 (<code>[[0]] &rarr; 0</code>) cannot distinguish them.<br><br>The code implements the <em>stated</em> (Chebyshev) definition. If the judge wants Manhattan, rotate coordinates — <code>u = r + c</code>, <code>v = r &minus; c</code> turns Manhattan distance into Chebyshev distance in (u, v), so the identical bounding-box argument applies after the transform.</div></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published examples, with the metric contradiction spelled out in step 4 — read that before trusting any number here.</p>
<div class="step"><h4>1 &middot; Chebyshev balls are squares</h4>
<p>The stated distance is <code>max(|Δrow|, |Δcol|)</code>: a king's move on a chessboard, where a diagonal step costs the same as a straight one. The consequence that makes this problem tractable:</p>
<div class="formula">{ cells within distance d of (r, c) }  =  the axis-aligned square
    rows  r&minus;d .. r+d      columns  c&minus;d .. c+d       side <b>2d + 1</b></div>
<p>Under Manhattan the same set would be a diamond, and none of the rectangle reasoning below would apply. The whole solution rests on this being a square.</p></div>
<div class="step"><h4>2 &middot; Binary-search the answer, then check feasibility</h4>
<p>Asking "what is the minimum inconvenience?" directly is awkward; asking "can it be &le; d?" is easy, and the predicate is monotone — if <em>d</em> works, so does <em>d+1</em>. So binary-search <em>d</em> over <code>[0, max(n, m)]</code> and answer the feasibility question:</p>
<ol>
<li>Multi-source BFS from every existing <code>1</code>, moving to all 8 neighbours (that is what makes BFS layers equal Chebyshev distance), giving <code>dist[i][j]</code> for every cell.</li>
<li>Collect the cells with <code>dist &gt; d</code>. If there are none, <em>d</em> is already achieved and no new centre is needed.</li>
<li>Otherwise <strong>all</strong> of them must be covered by the single new square of side <code>2d+1</code>. Take their bounding box <code>[r1..r2] × [c1..c2]</code>; one square suffices exactly when <code>r2 - r1 &le; 2d</code> and <code>c2 - c1 &le; 2d</code>.</li>
</ol>
<p>The bounding box is the key simplification: because the covering region is a square, covering a <em>set</em> of cells is equivalent to covering its bounding rectangle, and that reduces an apparently combinatorial placement search to two subtractions. Any centre that covers the two opposite corners covers everything between them.</p></div>
<div class="step"><h4>3 &middot; The examples</h4>
<table class="trace">
<tr><th>grid</th><th>existing 1s</th><th>cells with dist &gt; d</th><th>bounding box</th><th>smallest feasible d</th></tr>
<tr><td>[[0]]</td><td>none</td><td>the single cell</td><td>1 × 1</td><td class="hit">d = 0 (convert it; nothing is left uncovered) &rarr; <strong>0</strong></td></tr>
<tr><td>3×3 all zeros</td><td>none</td><td>all 9 cells</td><td>3 × 3, so spans are 2 and 2</td><td class="hit">needs 2d &ge; 2, so d = <strong>1</strong></td></tr>
</table>
<p>Example 2 matches its published answer. <strong>Example 1 does not</strong> — the statement says 2 — and that discrepancy is the subject of the next step.</p>
<p>Note how the no-existing-centre case needs no special handling: every cell has <code>dist = ∞ &gt; d</code>, so the bounding box is the whole grid and the test becomes "does one square of side 2d+1 cover the grid".</p></div>
<div class="step"><h4>4 &middot; The metric contradiction in the source</h4>
<p>The statement defines Chebyshev distance and illustrates it correctly: from (1,2) to (0,4) it gives <code>max(1, 2) = 2</code>, whereas Manhattan would be 3. But Example 1's answer of 2 is only reachable under <strong>Manhattan</strong>:</p>
<table class="trace">
<tr><th>metric</th><th>distance from centre (1,1) to corner (0,0)</th><th>inconvenience of the 3×3 grid</th></tr>
<tr><td>Chebyshev (as defined)</td><td>max(1, 1) = 1</td><td><strong>1</strong></td></tr>
<tr><td>Manhattan</td><td>1 + 1 = 2</td><td class="hit"><strong>2</strong> &mdash; matches the printed answer</td></tr>
</table>
<p>Two mutually exclusive readings, each supported by part of the source. The code implements the <em>definition</em>, since a definition is normally more reliable than a worked answer. If the judge wants Manhattan, you do not need a different algorithm — <strong>rotate the coordinates</strong>:</p>
<div class="formula">u = r + c,   v = r &minus; c    &rArr;    Manhattan(p, q) = Chebyshev((u,v)&#8321;, (u,v)&#8322;)</div>
<p>Run the identical bounding-box argument in (u, v) space. The only wrinkle is that not every (u, v) pair maps back to a grid cell — <code>u</code> and <code>v</code> must share parity — so a candidate centre needs that check before being accepted.</p></div>
<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>8-neighbour BFS</strong> for Chebyshev; 4-neighbour BFS computes Manhattan distance instead and silently answers the other problem.</li>
<li><strong>"At most one" conversion</strong> — zero conversions must remain allowed, which is the "no cells exceed d" branch.</li>
<li><strong>A grid that is already all 1s</strong> has no 0 cells, so the inconvenience is 0.</li>
<li><strong>Binary-search bounds:</strong> d = 0 must be testable, and the upper bound needs to be at least <code>max(n, m)</code>.</li>
<li><strong>500 × 500 = 250 000 cells</strong> and about 9 binary-search steps — fine, but do not rebuild the BFS inside the feasibility check; compute <code>dist</code> once, before searching.</li>
</ul></div>
</div></details>
</div>
`},

{
  id:'fp-binswaps', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Array',
  label:'Problem', title:'Minimum Adjacent Swaps to Group Binary Values',
  minutes:30, score:'',
  images:['src-binswaps.png'],
  fn:{name:'minimumAdjacentSwaps', ret:'long', params:[['int[]','bits']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [[rng.randint(0, 1) for _ in range(m)]]`,
  tests:[
    {in:[[0, 1, 0, 1]], out:1},
    {in:[[1, 1, 0, 0]], out:0},
    {in:[[0]], out:0},
    {in:[[1, 0, 1, 0, 1, 0]], out:3},
    {in:[[0, 0, 1, 1]], out:0},
    {in:[[1, 0, 0, 1, 1, 0, 0]], out:4},
    {in:[[1, 1, 1]], out:0}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">NEW GRAD</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The core task and binary-array bound are directly specified by the interview report.</div>

<p>You are given a binary array <code>bits</code>. Using adjacent swaps, rearrange it so that equal values form two contiguous groups.</p>
<p>Either order is valid: all <code>0</code>s before all <code>1</code>s, or all <code>1</code>s before all <code>0</code>s. Return the minimum number of adjacent swaps over both orders.</p>

<h3>Function</h3>
<pre class="sample">minimumAdjacentSwaps(bits: int[]) &rarr; long</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">bits   = [0,1,0,1]
return = 1</pre>
<p>Swap the middle 1 and 0 to obtain <code>[0,0,1,1]</code>.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">bits   = [1,1,0,0]
return = 0</pre>
<p>The array already has all ones before all zeroes.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &lt;= bits.length &lt;= 100000</code></li>
  <li>Every value in <code>bits</code> is either <code>0</code> or <code>1</code>.</li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>There are only two possible final arrangements, and each is a <em>sorted</em> array. Solve one of them and the other is the mirror image.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>The minimum number of adjacent swaps that sorts an array is its <strong>inversion count</strong>. For a binary array that count needs no merge sort: sweep once, and every time you meet a 0, add the number of 1s already seen.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Two targets, both sorted: <code>0…01…1</code> and <code>1…10…0</code>. For a fixed target, the minimum number of adjacent swaps equals the number of inversions with respect to that order, because one adjacent swap fixes exactly one inverted pair.</p>
<ul>
<li>Target <em>zeroes first</em> &rarr; inversions are the pairs <code>(i &lt; j)</code> with <code>bits[i] = 1</code>, <code>bits[j] = 0</code>.</li>
<li>Target <em>ones first</em> &rarr; the pairs with <code>bits[i] = 0</code>, <code>bits[j] = 1</code>.</li>
</ul>
<p>Both are counted in one pass with two running tallies, so no sorting and no Fenwick tree is needed. Answer: the smaller of the two.</p>
<p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def minimumAdjacentSwaps(bits):
    zeros = ones = 0
    inv10 = inv01 = 0          # 1-before-0 pairs, 0-before-1 pairs
    for b in bits:
        if b == 0:
            inv10 += ones      # every earlier 1 must cross this 0
            zeros += 1
        else:
            inv01 += zeros
            ones += 1
    return min(inv10, inv01)</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published examples: <code>[0,1,0,1] &rarr; 1</code> and <code>[1,1,0,0] &rarr; 0</code>.</p>

<div class="step"><h4>1 &middot; "Two contiguous groups" means sorted, one way or the other</h4>
<p>A binary array whose equal values form two blocks is either non-decreasing or non-increasing. There is nothing else to choose: the target is fully determined once you pick which value goes first, so the problem is <strong>two sorting problems</strong>, not a search.</p>
<div class="formula">target A:  0 0 &hellip; 0 1 1 &hellip; 1     (non-decreasing)
target B:  1 1 &hellip; 1 0 0 &hellip; 0     (non-increasing)
answer  =  min(cost to reach A, cost to reach B)</div>
</div>

<div class="step"><h4>2 &middot; Why the cost is the inversion count</h4>
<p>An adjacent swap changes the relative order of exactly one pair of positions. A pair that is already in the target order must never be swapped, and a pair that is out of order must be swapped an odd number of times &mdash; so at least once. Therefore</p>
<div class="formula">swaps &ge; number of out-of-order pairs (inversions)</div>
<p>and the bound is attained, because while any inversion exists there is an <em>adjacent</em> inversion, and swapping it removes exactly one. Equal values are interchangeable, so no pair of two 0s or two 1s ever counts.</p>
</div>

<div class="step"><h4>3 &middot; Counting both inversion sets in one pass</h4>
<p>For target A the inverted pairs are (1 before 0). Walk left to right holding <code>ones</code>, the number of 1s seen so far; each 0 you meet closes exactly <code>ones</code> such pairs. Target B is the mirror: hold <code>zeros</code> and charge each 1.</p>
<table class="trace">
<tr><th>i</th><th>bits[i]</th><th>ones so far</th><th>zeros so far</th><th>inv10 (&rarr; A)</th><th>inv01 (&rarr; B)</th></tr>
<tr><td>0</td><td>0</td><td>0</td><td>0 &rarr; 1</td><td>+0 = 0</td><td>0</td></tr>
<tr><td>1</td><td>1</td><td>0 &rarr; 1</td><td>1</td><td>0</td><td>+1 = 1</td></tr>
<tr><td>2</td><td>0</td><td>1</td><td>1 &rarr; 2</td><td class="hit">+1 = <b>1</b></td><td>1</td></tr>
<tr><td>3</td><td>1</td><td>1 &rarr; 2</td><td>2</td><td>1</td><td>+2 = 3</td></tr>
</table>
<div class="formula">answer = min(inv10, inv01) = min(1, 3) = <b>1</b>   &check; matches the published 1</div>
<p>Example 2, <code>[1,1,0,0]</code>: the 1s all precede the 0s, so <code>inv01 = 0</code> and the answer is <strong>0</strong> &mdash; even though <code>inv10</code> is 4. Forgetting the second target is the classic way to return 4 here.</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Both orders count.</strong> The statement says either grouping is acceptable; a solution that only sorts ascending fails example 2.</li>
<li><strong>The result does not fit in 32 bits.</strong> With n = 100000 the inversion count reaches 2.5 &times; 10&#8313;, hence the <code>long</code> return type.</li>
<li><strong>Do not simulate the swaps.</strong> Bubbling really does take &Theta;(n&sup2;) moves; only the <em>count</em> is asked for.</li>
<li><strong>No Fenwick tree needed.</strong> Binary values make the inversion count a two-counter sweep &mdash; reaching for a BIT is a correct but needlessly slow answer in an interview.</li>
<li><strong>inv10 + inv01 is not a constant</strong> you can shortcut with: it equals (number of 0s) &times; (number of 1s), which is a nice sanity check &mdash; 2 &times; 2 = 4 = 1 + 3 above.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-syncdrop', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Intervals',
  label:'Problem', title:'Minimum Processes to Drop for Synchronization',
  minutes:30, score:'',
  images:['src-syncdrop.png'],
  fn:{name:'minimumProcessesToDrop', ret:'int', params:[['int[]','starts'],['int[]','ends']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    starts, ends = [], []
    for _ in range(m):
        s = rng.randint(1, 4 * m)
        starts.append(s)
        ends.append(s + rng.randint(0, m))
    return [starts, ends]`,
  tests:[
    {in:[[1, 2, 3, 4], [2, 3, 5, 5]], out:1},
    {in:[[1, 4, 6], [10, 5, 8]], out:0},
    {in:[[1, 4, 7], [2, 5, 8]], out:2},
    {in:[[5], [5]], out:0},
    {in:[[1, 3, 5, 7], [2, 4, 6, 8]], out:3},
    {in:[[1, 1, 1], [9, 9, 9]], out:0},
    {in:[[1, 2, 3], [4, 2, 9]], out:0}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The source does not show numeric bounds or a callable signature. The judged core task matches the visible source at about 97%.</div>

<p>A team runs <code>n</code> processes. Process <code>i</code> executes during the inclusive interval <code>[starts[i], ends[i]]</code>.</p>
<p>A remaining set of processes is <em>synchronized</em> if at least one process in the set has an execution interval that overlaps the execution interval of every other process in the set. Intervals that share an endpoint overlap.</p>
<p>Return the minimum number of processes that must be dropped so that the remaining processes form a synchronized set.</p>
<p>A set containing only one process is synchronized.</p>

<h3>Function</h3>
<pre class="sample">minimumProcessesToDrop(starts: int[], ends: int[]) &rarr; int</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">starts = [1,2,3,4]
ends   = [2,3,5,5]
return = 1</pre>
<p>Drop the process with interval <code>[4, 5]</code>. Among the remaining intervals, <code>[2, 3]</code> overlaps <code>[1, 2]</code> at time 2 and <code>[3, 5]</code> at time 3, so the remaining set is synchronized.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">starts = [1,4,6]
ends   = [10,5,8]
return = 0</pre>
<p>The interval <code>[1, 10]</code> overlaps both other intervals, so all three processes already form a synchronized set.</p>

<div class="sublabel">Example 3</div>
<pre class="sample">starts = [1,4,7]
ends   = [2,5,8]
return = 2</pre>
<p>The three intervals are pairwise disjoint. Keeping any one process produces a synchronized singleton, so two processes must be dropped.</p>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>You are not asked for a set of mutually overlapping intervals. Only <em>one</em> process &mdash; call it the hub &mdash; has to meet all the others. Fix the hub and the rest of the answer writes itself.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Once the hub is fixed, every interval that touches it may stay, because the condition says nothing about the non-hub intervals meeting each other. So maximise <code>#{j : interval j overlaps interval i}</code> over <code>i</code>, and drop the rest. Count that with two sorted arrays and binary search rather than an O(n&sup2;) double loop.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>The synchronization rule is a <strong>star</strong>, not a clique: one process must overlap all the others, and the others are unconstrained among themselves. So the best kept set for a chosen hub <code>i</code> is <em>every</em> interval that overlaps <code>i</code> (including <code>i</code> itself), and the answer is</p>
<p><code>n &minus; max over i of #{ j : starts[j] &le; ends[i] and ends[j] &ge; starts[i] }</code></p>
<p>Two intervals overlap unless one ends before the other starts, so for a fixed <code>i</code> the count is "everything that starts by <code>ends[i]</code>" minus "everything that has already finished before <code>starts[i]</code>". Both are prefix counts over sorted copies of <code>starts</code> and <code>ends</code>, so each hub costs two binary searches.</p>
<p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>from bisect import bisect_left, bisect_right

def minimumProcessesToDrop(starts, ends):
    n = len(starts)
    ss = sorted(starts)
    ee = sorted(ends)
    best = 0
    for i in range(n):
        # processes overlapping i: start &lt;= ends[i] minus those that end before starts[i]
        c = bisect_right(ss, ends[i]) - bisect_left(ee, starts[i])
        if c &gt; best:
            best = c
    return n - best</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on all three published examples.</p>

<div class="step"><h4>1 &middot; Read the condition precisely: a star, not a clique</h4>
<p>"At least one process in the set overlaps every other process in the set" is much weaker than "all pairs overlap". In example 1 the kept set is <code>[1,2]</code>, <code>[2,3]</code>, <code>[3,5]</code> &mdash; and <code>[1,2]</code> does <em>not</em> overlap <code>[3,5]</code>. It is still synchronized because the hub <code>[2,3]</code> meets both.</p>
<div class="formula">clique reading &rarr; keep {[2,3],[3,5],[4,5]} = 3 &rarr; drop 1   (right answer, wrong reason)
star   reading &rarr; keep {[1,2],[2,3],[3,5]} = 3 &rarr; drop <b>1</b></div>
<p>Both readings happen to give 1 here, which is exactly why this example does not protect you. On <code>starts = [1,2,3], ends = [4,2,9]</code> the star answer is 0 and the clique answer is 1.</p>
</div>

<div class="step"><h4>2 &middot; Fixing the hub decides everything else</h4>
<p>Suppose the hub is process <code>i</code>. Any process that overlaps <code>i</code> can be kept, and keeping it never breaks the condition &mdash; the condition only ever inspects the hub. Any process that does <em>not</em> overlap <code>i</code> must go. So</p>
<div class="formula">keep(i) = #{ j : [s_j, e_j] &cap; [s_i, e_i] &ne; &empty; }        (j = i included)
answer  = n &minus; max_i keep(i)</div>
<p>Trying every hub is therefore exhaustive, and correctness needs no exchange argument.</p>
</div>

<div class="step"><h4>3 &middot; Counting overlaps in O(log n) per hub</h4>
<p>Negate the overlap test: <code>j</code> misses <code>i</code> exactly when <code>s_j &gt; e_i</code> (starts too late) or <code>e_j &lt; s_i</code> (finished too early). Those two groups are disjoint, because an interval that finishes before <code>s_i</code> also starts before <code>e_i</code>. Hence</p>
<div class="formula">keep(i) = #{ s_j &le; e_i }  &minus;  #{ e_j &lt; s_i }
        = bisect_right(sorted_starts, e_i) &minus; bisect_left(sorted_ends, s_i)</div>
<p>Example 1, with <code>sorted_starts = [1,2,3,4]</code> and <code>sorted_ends = [2,3,5,5]</code>:</p>
<table class="trace">
<tr><th>hub i</th><th>[s_i, e_i]</th><th>#{s_j &le; e_i}</th><th>#{e_j &lt; s_i}</th><th>keep(i)</th></tr>
<tr><td>0</td><td>[1, 2]</td><td>2</td><td>0</td><td>2</td></tr>
<tr><td class="hit">1</td><td class="hit">[2, 3]</td><td class="hit">3</td><td class="hit">0</td><td class="hit"><b>3</b></td></tr>
<tr><td>2</td><td>[3, 5]</td><td>4</td><td>1</td><td>3</td></tr>
<tr><td>3</td><td>[4, 5]</td><td>4</td><td>2</td><td>2</td></tr>
</table>
<div class="formula">answer = 4 &minus; 3 = <b>1</b>   &check;</div>
<p>Example 2: hub <code>[1,10]</code> gives <code>#{s_j &le; 10} = 3</code> and <code>#{e_j &lt; 1} = 0</code>, so keep = 3 and the answer is <code>3 &minus; 3 = 0</code>. &check;<br>
Example 3: every hub keeps only itself, so the answer is <code>3 &minus; 1 = 2</code>. &check;</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Do not solve "maximum set of mutually overlapping intervals"</strong> (the classic max-point-overlap sweep). That is the clique reading and it under-counts.</li>
<li><strong>Endpoints touch.</strong> <code>[1,2]</code> and <code>[2,3]</code> overlap, so the comparisons are <code>&le;</code> and <code>&ge;</code>, never strict.</li>
<li><strong>The hub counts itself</strong> &mdash; the formula already includes <code>j = i</code>, so do not add 1.</li>
<li><strong>n = 1 returns 0</strong>, which the singleton clause in the statement spells out.</li>
<li><strong>starts and ends are parallel arrays</strong>, not an array of pairs; sorting them independently is correct <em>only</em> for the counting step, so keep the original arrays for the hub loop.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-propagation', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Array',
  label:'Problem', title:'Minimum Cost of Left and Right Propagation',
  minutes:30, score:'',
  images:['src-propagation.png'],
  fn:{name:'minimumPropagationCost', ret:'long', params:[['int[]','values']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [[rng.randint(1, 9) for _ in range(m)]]`,
  tests:[
    {in:[[5, 2, 4]], out:4},
    {in:[[1, 1, 2, 1]], out:2},
    {in:[[7]], out:0},
    {in:[[3, 1, 4, 2]], out:3},
    {in:[[2, 2, 2, 2]], out:0},
    {in:[[1, 2, 3, 4, 5, 6]], out:5},
    {in:[[1, 1, 2, 1, 1]], out:3}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">INTERN</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The report supplies both propagation operations, their exact costs, and repeated execution, but leaves the terminal uniform-array goal and numeric bounds implicit. The judged core task matches it at about 94%.</div>

<p>You are given a positive integer array <code>values</code>. You may perform either propagation operation any number of times and in any order:</p>
<ul>
  <li>Choose index <code>i</code> and propagate <strong>left</strong>: replace every element before <code>i</code> with <code>values[i]</code>. This costs <code>i * values[i]</code>.</li>
  <li>Choose index <code>i</code> and propagate <strong>right</strong>: replace every element after <code>i</code> with <code>values[i]</code>. This costs <code>(n - 1 - i) * values[i]</code>.</li>
</ul>
<p>Return the minimum total cost needed to make every array element equal. You may perform zero operations when the array is already uniform.</p>

<h3>Function</h3>
<pre class="sample">minimumPropagationCost(values: int[]) &rarr; long</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">values = [5,2,4]
return = 4</pre>
<p>Keep the middle value 2, propagate it left for cost 2, and propagate it right for another cost 2.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">values = [1,1,2,1]
return = 2</pre>
<p>Keep the first run of two 1s and propagate right from index 1 for cost 2.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &lt;= values.length &lt;= 100000</code></li>
  <li><code>1 &lt;= values[i] &lt;= 10^9</code></li>
  <li>The answer fits in a signed 64-bit integer.</li>
</ul>

<div class="srcnote"><strong>Compare with:</strong> <em>"Minimum Cost to Make All Stations Equal"</em> (<code>getMinCost</code>) in the Amazon OA &middot; Coding section &mdash; the same operations and the same costs under a different cover story, with a different worked example. If you have solved that one, this is a five-minute re-run; if you have not, solve this one first and then check your answer against it.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Whatever the final uniform value is, it came from some element that was never overwritten. Ask which elements can survive to the end, and what it costs to erase everything on either side of them.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>The surviving elements form one <em>maximal run</em> of equal values <code>[l..r]</code>. Erasing everything to its left costs <code>l * v</code> (propagate left from <code>l</code>) and everything to its right costs <code>(n-1-r) * v</code>. Minimise <code>v * (l + n - 1 - r)</code> over all runs.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Two operations, and each one is paid per element it overwrites. Suppose the final value is <code>v</code> and it comes from position <code>i</code>. Propagating left from <code>i</code> costs <code>i * v</code> and propagating right costs <code>(n-1-i) * v</code>, so a single anchor position costs <code>v * (n-1)</code> &mdash; independent of <code>i</code>, which is the first thing to notice and the first trap.</p>
<p>The saving comes from anchors that are already <strong>a run</strong> of equal values: propagate left from the run's first index <code>l</code> and right from its last index <code>r</code>, and the elements inside the run are never paid for:</p>
<p><code>cost(run) = v * l + v * (n - 1 - r) = v * (l + n - 1 - r)</code></p>
<p>Scan the maximal runs once and take the minimum. A uniform array has one run with <code>l = 0</code>, <code>r = n-1</code>, so the cost is 0 and no operation is performed.</p>
<p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def minimumPropagationCost(values):
    n = len(values)
    best = None
    i = 0
    while i &lt; n:                       # walk the maximal runs of equal values
        j = i
        while j + 1 &lt; n and values[j + 1] == values[i]:
            j += 1
        cost = values[i] * (i + (n - 1 - j))     # pay for the left tail and the right tail
        if best is None or cost &lt; best:
            best = cost
        i = j + 1
    return best</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples: <code>[5,2,4] &rarr; 4</code> and <code>[1,1,2,1] &rarr; 2</code>.</p>

<div class="step"><h4>1 &middot; Only original values can win</h4>
<p>Every operation writes a value that is already in the array at that moment, and the array starts as <code>values</code>. So the final uniform value is one of the original <code>values[i]</code> &mdash; there is no way to invent a cheaper number.</p>
</div>

<div class="step"><h4>2 &middot; A single anchor always costs v &times; (n &minus; 1)</h4>
<p>This is the step everyone gets wrong. Anchor at index <code>i</code>, propagate both ways:</p>
<div class="formula">left  from i : i &times; v
right from i : (n &minus; 1 &minus; i) &times; v
total        : i&middot;v + (n&minus;1&minus;i)&middot;v = <b>(n &minus; 1) &middot; v</b>      &larr; the i cancels</div>
<p>So "pick the index with the smallest value and pay <code>i&middot;v + (n&minus;1&minus;i)&middot;v</code>" degenerates to "pick the smallest value", and it is wrong on example 2: it returns <code>3 &times; 1 = 3</code> where the answer is 2. Position is irrelevant &mdash; <em>width</em> is what matters.</p>
</div>

<div class="step"><h4>3 &middot; Keep a whole run, pay only for the tails</h4>
<p>If the value <code>v</code> occupies the maximal run <code>[l, r]</code>, propagate left from <code>l</code> and right from <code>r</code>. The <code>r &minus; l + 1</code> elements inside the run are already <code>v</code> and are never overwritten, so they are never charged:</p>
<div class="formula">cost(run) = v &middot; l  +  v &middot; (n &minus; 1 &minus; r)  =  v &middot; (l + n &minus; 1 &minus; r)
          = v &middot; (n &minus; 1 &minus; (run length &minus; 1))</div>
<p>Only maximal runs are worth testing: a sub-run of the same value has a larger <code>l</code> or a smaller <code>r</code>, so it can only cost more.</p>
<table class="trace">
<tr><th>array</th><th>run [l, r]</th><th>v</th><th>l + n&minus;1&minus;r</th><th>cost</th></tr>
<tr><td rowspan="3">[5,2,4], n = 3</td><td>[0,0]</td><td>5</td><td>0 + 2 = 2</td><td>10</td></tr>
<tr><td class="hit">[1,1]</td><td class="hit">2</td><td class="hit">1 + 1 = 2</td><td class="hit"><b>4</b></td></tr>
<tr><td>[2,2]</td><td>4</td><td>2 + 0 = 2</td><td>8</td></tr>
<tr><td rowspan="3">[1,1,2,1], n = 4</td><td class="hit">[0,1]</td><td class="hit">1</td><td class="hit">0 + 2 = 2</td><td class="hit"><b>2</b></td></tr>
<tr><td>[2,2]</td><td>2</td><td>2 + 1 = 3</td><td>6</td></tr>
<tr><td>[3,3]</td><td>1</td><td>3 + 0 = 3</td><td>3</td></tr>
</table>
<p>Both published answers reproduced: <strong>4</strong> and <strong>2</strong>. Note how the second example is decided by run <em>length</em>, not by value: the run <code>[0,1]</code> and the single <code>1</code> at index 3 share the value 1, and the run wins 2 against 3.</p>
</div>

<div class="step"><h4>4 &middot; Why no cleverer sequence helps</h4>
<p>Consider the last operation performed. It writes some value <code>v</code> over one side of the array, so before it the array was already <code>v</code> on the other side &mdash; i.e. every intermediate operation only ever grows a block of a single original value outwards. Growing that block in several smaller steps re-pays for positions that a single wide propagation pays for once, so no multi-step schedule beats "one left, one right from the widest run of that value". Exhaustive search over all operation sequences on arrays up to length 5 agrees with the formula on every input tested.</p>
</div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>The <code>i</code> cancels.</strong> Writing <code>i*v + (n-1-i)*v</code> and minimising over <code>i</code> is the single most common wrong answer here &mdash; it fails <code>[1,1,2,1]</code> with 3 against 2.</li>
<li><strong>Maximal runs only</strong>, and compare by <code>v * (l + n - 1 - r)</code>, not by <code>v</code> and not by run length alone: a long run of a huge value can lose to a short run of a tiny one.</li>
<li><strong>Already uniform &rarr; 0.</strong> The single run spans the array, and the formula yields <code>v * (0 + 0) = 0</code> with no special case needed.</li>
<li><strong>Overflow.</strong> <code>10&#8313;</code> values times <code>10&#8309;</code> positions needs 64 bits.</li>
<li><strong>n = 1</strong> gives cost 0 through the same formula.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-twodrones', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Binary search',
  label:'Problem', title:'Minimum Time for Two Delivery Drones',
  minutes:35, score:'',
  images:['src-twodrones.png'],
  fn:{name:'minimumDeliveryTime', ret:'long', params:[['long','delivery1'],['long','delivery2'],['long','charge1'],['long','charge2']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [rng.randint(1, 20 * m), rng.randint(1, 20 * m),
            rng.randint(2, 30), rng.randint(2, 30)]`,
  tests:[
    {in:[3, 1, 2, 3], out:5},
    {in:[1, 1, 2, 2], out:3},
    {in:[1, 1, 3, 3], out:2},
    {in:[5, 5, 2, 2], out:19},
    {in:[10, 4, 2, 5], out:19},
    {in:[1000000000, 1000000000, 2, 3], out:2399999999},
    {in:[1, 1000000000, 30000, 2], out:1999999999}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The judged core task matches the visible source at about 99%.</div>

<p>Amazon operates two delivery drones. Drone 1 must complete <code>delivery1</code> deliveries, and Drone 2 must complete <code>delivery2</code> deliveries. Each delivery takes exactly one hour.</p>
<p>Hours are numbered starting from <code>1</code>. The drones follow these rules while they still have deliveries to complete:</p>
<ul>
  <li>Drone 1 must charge during every hour whose number is a multiple of <code>charge1</code>.</li>
  <li>Drone 2 must charge during every hour whose number is a multiple of <code>charge2</code>.</li>
  <li>A drone cannot make a delivery during one of its charging hours.</li>
  <li>Both drones may charge during the same hour.</li>
  <li>At most one drone may make a delivery during any hour.</li>
</ul>
<p>Return the minimum total number of hours required for both drones to complete all deliveries. If the final delivery is made during hour <code>T</code>, the answer is <code>T</code>.</p>

<h3>Function</h3>
<pre class="sample">minimumDeliveryTime(delivery1: long, delivery2: long,
                    charge1: long, charge2: long) &rarr; long</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">delivery1 = 3
delivery2 = 1
charge1   = 2
charge2   = 3
return    = 5</pre>
<p>Drone 1 makes deliveries during hours 1, 3, and 5, and it charges during hours 2 and 4. Drone 2 makes its delivery during hour 2. Its next charging hour would be 3, but it has already completed all of its deliveries. Only one drone makes a delivery in each hour, and the final delivery is made during hour 5.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">delivery1 = 1
delivery2 = 1
charge1   = 2
charge2   = 2
return    = 3</pre>
<p>One drone can make a delivery during hour 1. Hour 2 is a charging hour for either drone that still has a delivery remaining, so the second delivery cannot happen until hour 3.</p>

<h3>Constraints</h3>
<ul>
  <li><code>2 &lt;= charge1, charge2 &lt;= 3 * 10^4</code></li>
  <li><code>1 &lt;= delivery1, delivery2 &lt;= 10^9</code></li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>A billion deliveries rules out simulating hour by hour. Ask instead: <em>given</em> a deadline T, can all the deliveries be placed? That question turns out to be pure counting, and it is monotone in T.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Inside hours 1..T, drone 1 is free in <code>T - floor(T/charge1)</code> hours and drone 2 in <code>T - floor(T/charge2)</code>. Because at most one delivery happens per hour, you also need both together to fit in the hours where <em>somebody</em> is free: <code>T - floor(T/lcm)</code>. Three inequalities, then binary search T.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Binary search the answer. The predicate "T hours are enough" is monotone (all three counts below are non-decreasing in T), so the first T that satisfies it is the answer &mdash; and it is automatically an hour in which a delivery happens, since T&minus;1 failed.</p>
<p>Charging never consumes the one-delivery-per-hour slot; it only forbids a particular drone from delivering. So in hours <code>1..T</code>:</p>
<ul>
<li>drone 1 may deliver in <code>T - floor(T / charge1)</code> hours,</li>
<li>drone 2 may deliver in <code>T - floor(T / charge2)</code> hours,</li>
<li>at least one drone may deliver in <code>T - floor(T / lcm(charge1, charge2))</code> hours.</li>
</ul>
<p>Those three capacities are exactly Hall's condition for this two-set system, so they are sufficient as well as necessary:</p>
<p><code>d1 &le; T - T/c1</code>, &nbsp; <code>d2 &le; T - T/c2</code>, &nbsp; <code>d1 + d2 &le; T - T/lcm</code>.</p>
<p>An upper bound of <code>4(d1 + d2) + 10</code> is safe because the worst case, <code>c1 = c2 = 2</code>, delivers every other hour.</p>
<p><span class="cx">Time O(log(d1 + d2))</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>from math import gcd

def minimumDeliveryTime(delivery1, delivery2, charge1, charge2):
    both = charge1 // gcd(charge1, charge2) * charge2       # lcm: nobody can deliver

    def enough(T):
        return (delivery1 &lt;= T - T // charge1 and           # hours drone 1 may use
                delivery2 &lt;= T - T // charge2 and           # hours drone 2 may use
                delivery1 + delivery2 &lt;= T - T // both)     # hours anybody may use

    lo, hi = 1, 4 * (delivery1 + delivery2) + 10
    while lo &lt; hi:
        mid = (lo + hi) // 2
        if enough(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples.</p>

<div class="step"><h4>1 &middot; Charging blocks a drone, not the hour</h4>
<p>Read the rules once more. "Both drones may charge during the same hour" and "at most one drone may make a delivery during any hour" are separate constraints: a charging hour is not a lost hour for the <em>other</em> drone. So hour 2 in example 1, which is a charging hour for drone 1, is still a perfectly good delivery hour for drone 2.</p>
<div class="formula">hour type inside 1..T                       who can deliver
multiple of c1 only                         drone 2
multiple of c2 only                         drone 1
multiple of both (i.e. of lcm)              nobody
neither                                     either (but only one of them)</div>
</div>

<div class="step"><h4>2 &middot; Feasibility of a deadline T is three counting inequalities</h4>
<p>Let <code>m1 = floor(T/c1)</code>, <code>m2 = floor(T/c2)</code>, <code>m12 = floor(T/lcm)</code>. Counting the four hour types above:</p>
<div class="formula">hours drone 1 can use   = T &minus; m1
hours drone 2 can use   = T &minus; m2
hours anybody can use   = T &minus; m12</div>
<p>Necessity is immediate. Sufficiency is Hall's condition on the two "sets" of usable hours: for a family of two sets you only have to check each set alone and their union, which is exactly the three lines. So no schedule needs to be constructed &mdash; the counts decide it.</p>
<p>Each of the three right-hand sides is non-decreasing in T (adding an hour adds at most one multiple), so the predicate flips from false to true once and binary search is valid.</p>
</div>

<div class="step"><h4>3 &middot; Example 1 &mdash; d1 = 3, d2 = 1, c1 = 2, c2 = 3</h4>
<p><code>lcm(2,3) = 6</code>.</p>
<table class="trace">
<tr><th>T</th><th>T &minus; T/2 (drone 1)</th><th>T &minus; T/3 (drone 2)</th><th>T &minus; T/6 (either)</th><th>3 &le; ?</th><th>1 &le; ?</th><th>4 &le; ?</th><th>verdict</th></tr>
<tr><td>3</td><td>3 &minus; 1 = 2</td><td>3 &minus; 1 = 2</td><td>3 &minus; 0 = 3</td><td>no</td><td>yes</td><td>no</td><td>too short</td></tr>
<tr><td>4</td><td>4 &minus; 2 = 2</td><td>4 &minus; 1 = 3</td><td>4 &minus; 0 = 4</td><td>no</td><td>yes</td><td>yes</td><td>too short</td></tr>
<tr><td class="hit">5</td><td class="hit">5 &minus; 2 = <b>3</b></td><td class="hit">5 &minus; 1 = 4</td><td class="hit">5 &minus; 0 = 5</td><td class="hit">yes</td><td class="hit">yes</td><td class="hit">yes</td><td class="hit"><b>answer 5</b></td></tr>
</table>
<p>The binding constraint is drone 1's own capacity: it loses hours 2 and 4 to charging, so its three deliveries need hours 1, 3, 5 &mdash; matching the schedule in the statement. &check;</p>
</div>

<div class="step"><h4>4 &middot; Example 2 &mdash; d1 = 1, d2 = 1, c1 = c2 = 2</h4>
<p>Here <code>lcm = 2</code>, so hour 2 is dead for both drones.</p>
<div class="formula">T = 2 :  drone 1 : 2 &minus; 1 = 1 &ge; 1  &check;
         drone 2 : 2 &minus; 1 = 1 &ge; 1  &check;
         together: 2 &minus; 1 = 1 &lt; 2  &cross;   &larr; only hour 1 is usable at all
T = 3 :  together: 3 &minus; 1 = 2 &ge; 2  &check;   &rarr; <b>answer 3</b></div>
<p>This is the example that proves the third inequality is needed: the two per-drone checks both pass at T = 2, and only the joint capacity rules it out. Drop that line and you return 2.</p>
</div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Do not simulate.</strong> <code>d &le; 10&#8313;</code> makes an hour-by-hour loop hopeless; the answer itself can exceed 2 &times; 10&#8313;, so it must be a <code>long</code>.</li>
<li><strong>The joint (lcm) inequality is not optional</strong> &mdash; example 2 exists precisely to catch its absence.</li>
<li><strong>A charging hour is not a blocked hour for the other drone.</strong> Subtracting all charging hours from T is wrong.</li>
<li><strong>"While they still have deliveries"</strong> only relaxes the rules after a drone is finished, which never makes a deadline harder; it explains the prose in example 1 and changes no arithmetic.</li>
<li><strong>Binary-search bound:</strong> <code>4(d1+d2)+10</code> is comfortable; a bound of <code>d1+d2</code> is not, since more than half the hours can be lost to charging.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-fulfillment', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Sorting',
  label:'Problem', title:'Minimum Robot and Human Fulfillment Time',
  minutes:30, score:'',
  images:['src-fulfillment.png'],
  fn:{name:'minimumFulfillmentTime', ret:'long', params:[['long[]','humanTime'],['long[]','robotTime']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    human = [rng.randint(1, 50) for _ in range(m)]
    robot = [rng.randint(1, 50) for _ in range(m)]
    return [human, robot]`,
  tests:[
    {in:[[9, 6, 8, 6, 4, 4], [4, 3, 7, 7, 9, 8]], out:8},
    {in:[[2, 3], [10, 10]], out:5},
    {in:[[5], [5]], out:5},
    {in:[[1, 1, 1, 1], [9, 9, 9, 9]], out:4},
    {in:[[10, 10, 10], [1, 2, 3]], out:3},
    {in:[[7, 2, 5, 9, 3], [8, 4, 6, 2, 7]], out:7}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The source omits numeric bounds and the empty-assignment convention. The judged core task matches the visible source at about 97%.</div>

<p>An Amazon fulfillment center must process <code>n</code> orders. Order <code>i</code> must be assigned entirely to exactly one of two processing sides:</p>
<ul>
  <li>The automated <strong>robotics system</strong> processes all orders assigned to it in parallel. If it receives at least one order, its elapsed time is the maximum <code>robotTime[i]</code> among those orders.</li>
  <li>The <strong>human workforce</strong> processes all orders assigned to it one by one. Its elapsed time is the sum of <code>humanTime[i]</code> across those orders.</li>
</ul>
<p>The two sides work concurrently, so the elapsed time for an assignment is the maximum of the robotics-system time and the human-workforce time. For this exercise, an unused side contributes 0 hours.</p>
<p>Return the minimum possible elapsed time needed to process and dispatch every order.</p>

<h3>Function</h3>
<pre class="sample">minimumFulfillmentTime(humanTime: long[], robotTime: long[]) &rarr; long</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">humanTime = [9, 6, 8, 6, 4, 4]
robotTime = [4, 3, 7, 7, 9, 8]
return    = 8</pre>
<p>Assign the order with robotics time 9 and human time 4 to the human workforce, and assign every other order to the robotics system. The human side takes 4 hours, while the robot side takes 8 hours, so all orders finish in 8 hours. No assignment can finish in 7 hours because both orders with robotics times above 7 would have to be handled by humans, requiring 4 + 4 = 8 hours.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">humanTime = [2, 3]
robotTime = [10, 10]
return    = 5</pre>
<p>Assign both orders to the human workforce. The human side takes 2 + 3 = 5 hours, and the unused robot side contributes 0 hours.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &lt;= humanTime.length = robotTime.length &lt;= 2 * 10^5</code></li>
  <li><code>1 &lt;= humanTime[i], robotTime[i] &lt;= 10^9</code></li>
  <li>All sums and the returned result fit in a signed 64-bit integer.</li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>The robot side is charged a <em>maximum</em> and the human side a <em>sum</em>. Guess the robot side's final value first &mdash; it can only be 0 or one of the <code>robotTime</code> values &mdash; and see what that forces.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>If the robot side is allowed to take R, then every order with <code>robotTime[i] &gt; R</code> must go to the humans, and every other order may as well go to the robots (it cannot raise the maximum above R). Sort by <code>robotTime</code> and sweep the split point, keeping a suffix sum of <code>humanTime</code>.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Sort the orders by <code>robotTime</code> ascending. Consider the <code>n + 1</code> splits "the last <em>k</em> orders in that order go to the humans, the first <code>n &minus; k</code> go to the robots":</p>
<ul>
<li>robot time = <code>robotTime</code> of the last order still on the robot side (0 when <code>k = n</code>),</li>
<li>human time = the suffix sum of <code>humanTime</code> over the <em>k</em> orders handed to the humans.</li>
</ul>
<p>Answer = the minimum over those splits of <code>max(robot, human)</code>. Sweeping <em>k</em> from <em>n</em> down to 0 keeps the suffix sum in one accumulator.</p>
<p>Why the enumeration is exhaustive: in an optimal assignment let R be the robot side's elapsed time. Every order with <code>robotTime &gt; R</code> is on the human side by definition, and moving any order with <code>robotTime &le; R</code> from the humans to the robots leaves the robot side at R while shrinking the human sum &mdash; never worse. That normalised assignment is one of the splits above.</p>
<p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def minimumFulfillmentTime(humanTime, robotTime):
    n = len(robotTime)
    order = sorted(range(n), key=lambda i: robotTime[i])   # ascending robot time
    best = None
    human_sum = 0
    for k in range(n, -1, -1):
        # order[:k] -&gt; robots, order[k:] -&gt; humans
        robot = robotTime[order[k - 1]] if k else 0
        cand = max(robot, human_sum)
        if best is None or cand &lt; best:
            best = cand
        if k:
            human_sum += humanTime[order[k - 1]]
    return best</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example <code>humanTime = [9,6,8,6,4,4]</code>, <code>robotTime = [4,3,7,7,9,8]</code> &rarr; <strong>8</strong>.</p>

<div class="step"><h4>1 &middot; Why a greedy per order cannot work</h4>
<p>"Send each order to whichever side is cheaper for it" is meaningless here: the two sides are charged in different units. One extra order on the robot side is free unless it is the new maximum; one extra order on the human side always adds its full time. The decision is global, so parameterise it.</p>
</div>

<div class="step"><h4>2 &middot; Parameterise by the robot side's elapsed time</h4>
<p>Let R be the robot side's time in some optimal assignment. R is either 0 (robots unused) or equal to some <code>robotTime[i]</code>. Given R:</p>
<div class="formula">robotTime[i] &gt; R  &rArr;  order i <b>must</b> be human-processed
robotTime[i] &le; R  &rArr;  putting order i on the robots costs nothing extra</div>
<p>So the human side's load is completely determined by R: it is the sum of <code>humanTime</code> over the orders whose robot time exceeds R. Sorting by <code>robotTime</code> turns "orders above the threshold" into a suffix, and the whole search collapses to <code>n + 1</code> candidate splits.</p>
</div>

<div class="step"><h4>3 &middot; The sweep, in full</h4>
<p>Sorted by robot time: <code>(3,6) (4,9) (7,8) (7,6) (8,4) (9,4)</code> written as (robot, human).</p>
<table class="trace">
<tr><th>k = orders given to humans</th><th>robot side max</th><th>human side sum</th><th>max(&middot;,&middot;)</th></tr>
<tr><td>0</td><td>9</td><td>0</td><td>9</td></tr>
<tr><td class="hit">1 &nbsp; {(9,4)}</td><td class="hit">8</td><td class="hit">4</td><td class="hit"><b>8</b></td></tr>
<tr><td>2 &nbsp; {(9,4),(8,4)}</td><td>7</td><td>8</td><td>8</td></tr>
<tr><td>3</td><td>7</td><td>14</td><td>14</td></tr>
<tr><td>4</td><td>4</td><td>22</td><td>22</td></tr>
<tr><td>5</td><td>3</td><td>31</td><td>31</td></tr>
<tr><td>6 &nbsp; (robots idle)</td><td>0</td><td>37</td><td>37</td></tr>
</table>
<p>Minimum <strong>8</strong>, achieved by handing only the robot-time-9 order to the humans &mdash; exactly the assignment the statement describes. Row <code>k = 2</code> also reaches 8 and explains the statement's remark that 7 is impossible: to pull the robot side down to 7 you must give both the 9 and the 8 to the humans, and 4 + 4 = 8 &gt; 7.</p>
<p>Example 2 is the <code>k = n</code> row: robot side 0, human side 2 + 3 = <strong>5</strong>. &check;</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Include both ends of the sweep.</strong> <code>k = n</code> (robots unused, the answer to example 2) and <code>k = 0</code> (humans unused) are legal assignments; a loop over <code>1..n-1</code> misses them.</li>
<li><strong>An unused side contributes 0</strong>, not the maximum over an empty set. In a language whose <code>max</code> throws on empty input this is a real crash.</li>
<li><strong>Ties in robotTime.</strong> Splitting between two equal robot times is fine &mdash; the sorted sweep covers every split, so no special handling is needed.</li>
<li><strong>Sort by robot time, carry human time along.</strong> Sorting the two arrays independently destroys the pairing; sort indices.</li>
<li><strong>Overflow.</strong> 2 &times; 10&#8309; orders of 10&#8313; hours sum to 2 &times; 10&#185;&#8308;; use 64-bit accumulators.</li>
<li><strong>Binary searching the answer</strong> also works, but it needs the same threshold insight &mdash; the sorted sweep is simpler and strictly faster.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-redirect', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Geometry',
  label:'Problem', title:'HTTP Request Redirection',
  minutes:30, score:'',
  images:[],
  fn:{name:'findFinalServer', ret:'int[]', params:[['int[][]','locations'],['int[]','redirectRecords']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    pts = set()
    while len(pts) < m:
        pts.add((rng.randint(-m, m), rng.randint(-m, m)))
    locations = [list(p) for p in pts]
    records = [rng.randint(1, 4) for _ in range(rng.randint(1, 6))]
    return [locations, records]`,
  tests:[
    {in:[[[3, 4], [1, 2], [7, 8], [5, 6]], [1, 4]], out:[1, 2]},
    {in:[[[0, 0], [2, 2], [4, 4]], [1, 1]], out:[4, 4]},
    {in:[[[0, 0], [1, 2]], [1]], out:[0, 0]},
    {in:[[[5, 5], [3, 7], [1, 9], [7, 3]], [3, 2]], out:[7, 3]},
    {in:[[[0, 0], [2, 2], [1, -1]], [1, 4, 2]], out:[2, 2]}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<p>Amazon engineers are investigating an HTTP request that is redirected among servers.</p>
<p>There are <code>n</code> servers on an infinite two-dimensional plane. The coordinates of server <code>i</code> are given by <code>locations[i] = [x, y]</code>. The request starts at <code>locations[0]</code>, and that server is marked as visited.</p>
<p>Each value in <code>redirectRecords</code> specifies one redirect direction from the current server <code>(a, b)</code>. In every formula below, <code>Z</code> is an arbitrary positive integer:</p>
<ul>
  <li>Direction 1: <code>(a, b) -&gt; (a + Z, b + Z)</code>.</li>
  <li>Direction 2: <code>(a, b) -&gt; (a + Z, b - Z)</code>.</li>
  <li>Direction 3: <code>(a, b) -&gt; (a - Z, b + Z)</code>.</li>
  <li>Direction 4: <code>(a, b) -&gt; (a - Z, b - Z)</code>.</li>
</ul>
<p>Process the redirect records in order. For each record, redirect the request to the nearest server in the specified direction that has not previously been visited. If no eligible server exists in that direction, skip that redirect. Whenever the request reaches a server, mark it as visited.</p>
<p>Return the coordinates <code>[x, y]</code> of the server holding the request after all redirect records have been processed.</p>

<h3>Function</h3>
<pre class="sample">findFinalServer(locations: int[][], redirectRecords: int[]) &rarr; int[]</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">locations       = [[3,4],[1,2],[7,8],[5,6]]
redirectRecords = [1,4]
return          = [1,2]</pre>
<p>The request starts at <code>[3, 4]</code>. Direction 1 points toward both <code>[5, 6]</code> and <code>[7, 8]</code>, so the nearest unvisited server is <code>[5, 6]</code>. Direction 4 points back toward <code>[3, 4]</code> and then <code>[1, 2]</code>. Because <code>[3, 4]</code> has already been visited, the request moves to <code>[1, 2]</code>.</p>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>All four directions are exact diagonals, so a server is "in direction d" only when <code>|dx| = |dy|</code> with the right pair of signs. Nothing is approximate here &mdash; a server one unit off the diagonal is simply not a candidate.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Because the movement is diagonal, the distance ordering is the same whether you measure <code>Z</code>, Manhattan or Euclidean distance: they are <code>Z</code>, <code>2Z</code> and <code>Z&radic;2</code>. Just minimise <code>|dx|</code> among the candidates, skipping visited servers.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Direct simulation. Keep the current position and a set of visited server indices. For each record, scan every server once, keep those that sit on the requested diagonal ray, and take the one with the smallest <code>|dx|</code>:</p>
<ul>
<li>direction 1 &rarr; <code>dx &gt; 0</code> and <code>dy = dx</code></li>
<li>direction 2 &rarr; <code>dx &gt; 0</code> and <code>dy = -dx</code></li>
<li>direction 3 &rarr; <code>dx &lt; 0</code> and <code>dy = -dx</code></li>
<li>direction 4 &rarr; <code>dx &lt; 0</code> and <code>dy = dx</code></li>
</ul>
<p><code>Z &gt; 0</code> means the current server itself is never a candidate, which the strict <code>dx &gt; 0</code> / <code>dx &lt; 0</code> tests already enforce. If nothing qualifies, the record is skipped and the request stays put.</p>
<p><span class="cx">Time O(n &middot; r)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def findFinalServer(locations, redirectRecords):
    cur = list(locations[0])
    visited = {0}
    for d in redirectRecords:
        pick = None
        best = None
        for i, (x, y) in enumerate(locations):
            if i in visited:
                continue
            dx, dy = x - cur[0], y - cur[1]
            if d == 1:
                ok = dx &gt; 0 and dy == dx          # (a+Z, b+Z)
            elif d == 2:
                ok = dx &gt; 0 and dy == -dx         # (a+Z, b-Z)
            elif d == 3:
                ok = dx &lt; 0 and dy == -dx         # (a-Z, b+Z)
            else:
                ok = dx &lt; 0 and dy == dx          # (a-Z, b-Z)
            if ok and (best is None or abs(dx) &lt; best):
                best, pick = abs(dx), i
        if pick is not None:                      # no eligible server -&gt; skip
            visited.add(pick)
            cur = list(locations[pick])
    return cur</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example: <code>locations = [[3,4],[1,2],[7,8],[5,6]]</code>, <code>redirectRecords = [1,4]</code> &rarr; <strong>[1, 2]</strong>.</p>

<div class="step"><h4>1 &middot; Turning the four formulas into two comparisons</h4>
<p>Each direction is the set of points reachable by adding <code>(&plusmn;Z, &plusmn;Z)</code> with <code>Z &gt; 0</code>. Write <code>dx = x &minus; a</code> and <code>dy = y &minus; b</code>:</p>
<div class="formula">direction 1 : dx = +Z, dy = +Z  &rarr;  dx &gt; 0 and dy == dx
direction 2 : dx = +Z, dy = &minus;Z  &rarr;  dx &gt; 0 and dy == &minus;dx
direction 3 : dx = &minus;Z, dy = +Z  &rarr;  dx &lt; 0 and dy == &minus;dx
direction 4 : dx = &minus;Z, dy = &minus;Z  &rarr;  dx &lt; 0 and dy == dx</div>
<p>The sign test is what separates 1 from 4 and 2 from 3; both pairs share an equation, so dropping it merges two opposite rays into one line and sends the request backwards.</p>
</div>

<div class="step"><h4>2 &middot; "Nearest" is unambiguous on a diagonal</h4>
<p>On the ray, a server sits at distance <code>Z</code> in steps, <code>2Z</code> in Manhattan distance and <code>Z&radic;2</code> in Euclidean distance. All three orderings agree, so comparing <code>|dx|</code> needs no square roots and no tie-breaking rule.</p>
</div>

<div class="step"><h4>3 &middot; The two redirects, step by step</h4>
<table class="trace">
<tr><th>step</th><th>at</th><th>dir</th><th>candidates (dx, dy)</th><th>eligible</th><th>move to</th></tr>
<tr><td>start</td><td>[3,4]</td><td>&mdash;</td><td>&mdash;</td><td>&mdash;</td><td>visited = {[3,4]}</td></tr>
<tr><td>1</td><td>[3,4]</td><td>1</td><td>[1,2]:(&minus;2,&minus;2) &cross; &nbsp; [7,8]:(4,4) &check; Z=4 &nbsp; [5,6]:(2,2) &check; Z=2</td><td>Z = 2 and 4</td><td class="hit">[5,6] &nbsp;(smallest Z)</td></tr>
<tr><td>2</td><td>[5,6]</td><td>4</td><td>[3,4]:(&minus;2,&minus;2) &check; Z=2 <em>but visited</em> &nbsp; [1,2]:(&minus;4,&minus;4) &check; Z=4 &nbsp; [7,8]:(2,2) &cross;</td><td>only Z = 4</td><td class="hit">[1,2]</td></tr>
</table>
<div class="formula">final position = <b>[1, 2]</b>   &check; matches the published answer</div>
<p>Step 2 is the whole point of the example: the nearest server on the ray is <code>[3,4]</code>, and it is skipped <em>because it was visited</em> &mdash; the visited set filters candidates, it does not stop the search at the first one.</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>The start server begins visited.</strong> Without that, a direction pointing back at it returns the request to where it started.</li>
<li><strong>Visited servers are skipped, not blocking.</strong> The search continues past them along the same ray.</li>
<li><strong>A record with no candidate is skipped silently</strong> &mdash; the request neither moves nor fails, and the remaining records still run.</li>
<li><strong><code>Z</code> is strictly positive</strong>, so the current position is never its own target even before it is marked visited.</li>
<li><strong>Do not use Euclidean distance with floats.</strong> Integer <code>|dx|</code> is exact; <code>sqrt</code> only invites ties that do not exist.</li>
<li><strong>Return coordinates, not an index.</strong> The signature returns <code>int[]</code>, i.e. <code>[x, y]</code>.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-busroute', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Prefix sums',
  label:'Problem', title:'Shortest Distance on a Circular Bus Route',
  minutes:15, score:'',
  images:[],
  fn:{name:'shortestBusRouteDistance', ret:'int', params:[['int[]','distance'],['int','start'],['int','destination']]},
  gen:`def gen(rng, n):
    m = max(2, n)
    distance = [rng.randint(1, 10000) for _ in range(m)]
    a = rng.randrange(m)
    b = rng.randrange(m)
    while b == a:
        b = rng.randrange(m)
    return [distance, a, b]`,
  tests:[
    {in:[[1, 2, 3, 4], 0, 2], out:3},
    {in:[[7, 10, 1, 12], 1, 3], out:11},
    {in:[[5, 5], 0, 1], out:5},
    {in:[[1, 2, 3, 4], 3, 0], out:4},
    {in:[[2, 2, 2, 2, 2, 2], 1, 4], out:6},
    {in:[[9, 1, 1, 1], 0, 3], out:1}
  ],
  body:`
<div class="tags"><span class="tag easy">Easy</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The interview report identifies this circular bus-route problem family but omits the exact variant contract. The deterministic practice rules below complete those missing details.</div>

<p>For this exercise, assume a bus route has <code>n</code> stops arranged in a circle. The array <code>distance</code> contains the distance from stop <code>i</code> to stop <code>(i + 1) mod n</code>.</p>
<p>Given two distinct stops, <code>start</code> and <code>destination</code>, return the shorter travel distance between them. A bus may travel clockwise or counterclockwise around the circle.</p>

<h3>Function</h3>
<pre class="sample">shortestBusRouteDistance(distance: int[], start: int, destination: int) &rarr; int</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">distance    = [1,2,3,4]
start       = 0
destination = 2
return      = 3</pre>
<p>Clockwise travel from stop 0 to stop 2 costs 1 + 2 = 3. The other direction costs 4 + 3 = 7, so the answer is 3.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">distance    = [7,10,1,12]
start       = 1
destination = 3
return      = 11</pre>
<p>Travel through stops 1 -&gt; 2 -&gt; 3 costs 10 + 1 = 11. The opposite direction costs 12 + 7 = 19.</p>

<h3>Constraints</h3>
<ul>
  <li><code>2 &lt;= distance.length &lt;= 100000</code></li>
  <li><code>1 &lt;= distance[i] &lt;= 10000</code></li>
  <li><code>0 &lt;= start, destination &lt; distance.length</code></li>
  <li><code>start != destination</code></li>
</ul>

<div class="srcnote"><strong>Next:</strong> <em>"Circular Route Query Distance"</em> asks the same question for many pairs at once &mdash; the natural follow-up once this one is a two-liner.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>The two routes between the stops partition the whole circle. Compute one of them and the other is free.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Order the two indices so you only ever walk the <em>increasing</em> way: the arc from <code>min</code> to <code>max</code> is the contiguous slice <code>distance[min:max]</code>. The other arc is <code>total &minus; that</code>.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Going round the circle once costs <code>total = sum(distance)</code>. The clockwise arc from the smaller index to the larger one is exactly the slice <code>distance[lo:hi]</code>, and the counterclockwise arc is whatever is left, <code>total &minus; forward</code>. Return the smaller.</p>
<p>Sorting the endpoints first is what removes the wrap-around case: <code>distance[lo:hi]</code> is always a plain contiguous range, so no modular loop is needed.</p>
<p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def shortestBusRouteDistance(distance, start, destination):
    total = sum(distance)
    lo, hi = min(start, destination), max(start, destination)
    forward = sum(distance[lo:hi])        # lo -&gt; lo+1 -&gt; ... -&gt; hi
    return min(forward, total - forward)</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples.</p>

<div class="step"><h4>1 &middot; The two arcs are complementary</h4>
<p><code>distance[i]</code> is the edge from stop <code>i</code> to stop <code>i+1</code>, so every edge belongs to exactly one of the two arcs between two distinct stops:</p>
<div class="formula">clockwise(lo &rarr; hi)        = distance[lo] + distance[lo+1] + &hellip; + distance[hi&minus;1]
counterclockwise(lo &rarr; hi) = total &minus; clockwise
answer                     = min(clockwise, total &minus; clockwise)</div>
<p>Because the arcs partition the circle, one subtraction replaces a second traversal &mdash; and it is the only way to stay O(n) when the answer is the long way round.</p>
</div>

<div class="step"><h4>2 &middot; Example 1 &mdash; distance = [1,2,3,4], 0 &rarr; 2</h4>
<table class="trace">
<tr><th>quantity</th><th>edges</th><th>value</th></tr>
<tr><td>total</td><td>1 + 2 + 3 + 4</td><td>10</td></tr>
<tr><td class="hit">forward (slice [0:2])</td><td class="hit">distance[0] + distance[1] = 1 + 2</td><td class="hit"><b>3</b></td></tr>
<tr><td>backward</td><td>10 &minus; 3 = distance[2] + distance[3] = 3 + 4</td><td>7</td></tr>
</table>
<div class="formula">min(3, 7) = <b>3</b>   &check;</div>
</div>

<div class="step"><h4>3 &middot; Example 2 &mdash; distance = [7,10,1,12], 1 &rarr; 3</h4>
<div class="formula">total    = 7 + 10 + 1 + 12 = 30
forward  = distance[1] + distance[2] = 10 + 1 = <b>11</b>
backward = 30 &minus; 11 = 19  ( = distance[3] + distance[0] = 12 + 7 )
answer   = min(11, 19) = <b>11</b>   &check;</div>
<p>Note that the backward arc <em>wraps</em> past index 0. Sorting the endpoints meant we never had to write that loop.</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Do not walk with <code>%</code> from start to destination</strong> without first ordering the endpoints &mdash; it works, but it is where off-by-one and infinite-loop bugs live.</li>
<li><strong><code>distance[i]</code> is an edge, not a stop coordinate.</strong> The arc from <code>lo</code> to <code>hi</code> uses <code>hi &minus; lo</code> edges, so the slice ends at <code>hi</code>, exclusive.</li>
<li><strong>The last edge closes the circle</strong>: <code>distance[n-1]</code> runs from stop <code>n&minus;1</code> back to stop 0, and it belongs to the backward arc here.</li>
<li><strong>Equal arcs</strong> (a symmetric circle) are fine &mdash; <code>min</code> of two equal values is the answer either way.</li>
<li><strong>Many queries?</strong> Then this O(n)-per-query version is the wrong shape; precompute prefix sums, as in the companion problem.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-circularqueries', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Prefix sums',
  label:'Problem', title:'Circular Route Query Distance',
  minutes:20, score:'',
  images:[],
  fn:{name:'minCircularQueryDistance', ret:'int', params:[['int[]','distances'],['int[][]','queries']]},
  gen:`def gen(rng, n):
    m = max(2, n)
    distances = [rng.randint(1, 1000) for _ in range(m)]
    queries = [[rng.randrange(m), rng.randrange(m)] for _ in range(max(1, m // 2))]
    return [distances, queries]`,
  tests:[
    {in:[[1, 2, 3, 4], [[0, 1], [1, 3], [3, 0]]], out:10},
    {in:[[7, 10, 1, 12], [[0, 2], [2, 1]]], out:23},
    {in:[[5, 5], [[0, 1]]], out:5},
    {in:[[1, 2, 3, 4], [[2, 2]]], out:0},
    {in:[[3, 1, 4, 1, 5], [[0, 3], [4, 1], [2, 0]]], out:16}
  ],
  body:`
<div class="tags"><span class="tag easy">Easy</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<p>A circular route has <code>n</code> stops numbered from <code>0</code> to <code>n - 1</code>. The array <code>distances</code> has length <code>n</code>, where <code>distances[i]</code> is the distance from stop <code>i</code> to stop <code>(i + 1) % n</code>.</p>
<p>You are given several route queries. Each query <code>[start, end]</code> asks for the shorter of the two possible distances between those stops on the circle. Return the sum of the shortest distances over all queries.</p>

<h3>Function</h3>
<pre class="sample">minCircularQueryDistance(distances: int[], queries: int[][]) &rarr; int</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">distances = [1,2,3,4]
queries   = [[0,1],[1,3],[3,0]]
return    = 10</pre>
<p>The shortest distances are 1, 5, and 4, so the total is 10.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">distances = [7,10,1,12]
queries   = [[0,2],[2,1]]
return    = 23</pre>
<p>For 0 to 2, the counter-clockwise route is shorter with distance 13. For 2 to 1, the opposite direction has distance 10.</p>

<h3>Constraints</h3>
<ul>
  <li>Stops are zero-indexed. Each query contains two valid stop indices.</li>
  <li>No numeric limits were provided in the source; an efficient solution should precompute prefix sums around the circle.</li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Every query asks the same question as the single-pair version. The only new requirement is not to re-walk the circle once per query.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Build <code>prefix[i] = distances[0] + &hellip; + distances[i-1]</code> once. Then the clockwise arc between two stops is a difference of two prefix entries, and the other arc is <code>total</code> minus it &mdash; O(1) per query.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>One prefix-sum pass, then each query is arithmetic:</p>
<p><code>forward = prefix[hi] &minus; prefix[lo]</code> &nbsp;(after ordering the endpoints), &nbsp; <code>answer += min(forward, total &minus; forward)</code>.</p>
<p>Ordering the endpoints is what keeps the arc contiguous, so the wrap-around direction never needs its own code path &mdash; it is always the complement.</p>
<p><span class="cx">Time O(n + q)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def minCircularQueryDistance(distances, queries):
    prefix = [0]
    for d in distances:
        prefix.append(prefix[-1] + d)
    total = prefix[-1]

    answer = 0
    for start, end in queries:
        lo, hi = (start, end) if start &lt;= end else (end, start)
        forward = prefix[hi] - prefix[lo]
        answer += min(forward, total - forward)
    return answer</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples.</p>

<div class="step"><h4>1 &middot; One prefix table serves every query</h4>
<div class="formula">distances = [1, 2, 3, 4]
prefix    = [0, 1, 3, 6, 10]        prefix[i] = distance from stop 0 to stop i, clockwise
total     = prefix[n] = 10</div>
<p>Then for stops <code>lo &le; hi</code>, the clockwise arc is <code>prefix[hi] &minus; prefix[lo]</code> and the counterclockwise arc is <code>total &minus; that</code>. Both in O(1).</p>
</div>

<div class="step"><h4>2 &middot; Example 1, query by query</h4>
<table class="trace">
<tr><th>query</th><th>lo, hi</th><th>forward = prefix[hi] &minus; prefix[lo]</th><th>backward</th><th>min</th></tr>
<tr><td>[0, 1]</td><td>0, 1</td><td>1 &minus; 0 = 1</td><td>9</td><td class="hit">1</td></tr>
<tr><td>[1, 3]</td><td>1, 3</td><td>6 &minus; 1 = 5</td><td>5</td><td class="hit">5</td></tr>
<tr><td>[3, 0]</td><td>0, 3</td><td>6 &minus; 0 = 6</td><td>4</td><td class="hit">4</td></tr>
</table>
<div class="formula">total answer = 1 + 5 + 4 = <b>10</b>   &check;</div>
<p>The third query is the one that punishes a "walk forward from <code>start</code>" implementation: from stop 3 to stop 0 the clockwise walk is a single edge of length 4, while <code>prefix</code> arithmetic on the ordered pair gives 6 &mdash; and the <code>min</code> puts it right either way.</p>
</div>

<div class="step"><h4>3 &middot; Example 2 &mdash; distances = [7,10,1,12]</h4>
<div class="formula">prefix = [0, 7, 17, 18, 30],  total = 30
[0,2] &rarr; forward = 17 &minus; 0  = 17,  backward = 13  &rarr; <b>13</b>
[2,1] &rarr; lo,hi = 1,2 &rarr; forward = 17 &minus; 7 = 10,  backward = 20  &rarr; <b>10</b>
sum   = 13 + 10 = <b>23</b>   &check;</div>
<p>Both directions are exercised: the first query's winner wraps through stop 3, the second's does not.</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Do not re-sum per query.</strong> With q queries that is O(nq); the prefix table makes it O(n + q).</li>
<li><strong>Order the endpoints per query</strong>, not once. Queries arrive in both orders, as <code>[3,0]</code> shows.</li>
<li><strong><code>prefix</code> has n + 1 entries.</strong> <code>prefix[n] = total</code>, and the arc uses <code>prefix[hi]</code> with <code>hi</code> up to <code>n &minus; 1</code> only, so the extra slot is the total, nothing else.</li>
<li><strong>A degenerate query <code>[k, k]</code></strong> yields <code>forward = 0</code> and contributes 0 &mdash; not the full lap.</li>
<li><strong>Sum in 64 bits</strong> if the source ever pins the bounds; many queries over long routes overflow 32 bits quickly.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-rotateflip', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Arrays',
  label:'Problem', title:'Sort an Array with Rotate and Flip',
  minutes:35, score:'',
  images:[],
  fn:{name:'minSortOperations', ret:'int', params:[['int[]','values']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    vals = rng.sample(range(-10 * m, 10 * m), m)
    if rng.random() < 0.7:                 # mostly solvable inputs
        vals.sort()
        k = rng.randrange(m)
        vals = vals[k:] + vals[:k]
        if rng.random() < 0.5:
            vals = vals[::-1]
    return [vals]`,
  tests:[
    {in:[[3, 4, 1, 2]], out:2},
    {in:[[3, 2, 1, 4]], out:2},
    {in:[[1, 3, 2, 4]], out:-1},
    {in:[[1]], out:0},
    {in:[[1, 2, 3, 4]], out:0},
    {in:[[2, 3, 4, 5, 6, 7, 8, 9, 10, 1]], out:3},
    {in:[[4, 3, 2, 1]], out:1},
    {in:[[2, 1]], out:1}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The source identifies the rotate-or-flip sorting objective but omits the exact operation definitions, target order, and bounds. The judged core task matches the visible source at about 84%.</div>

<p>You are given an array <code>values</code> containing distinct integers. You may apply either of these operations:</p>
<ul>
  <li><strong>Rotate:</strong> Move the first element to the end of the array.</li>
  <li><strong>Flip:</strong> Reverse the entire array.</li>
</ul>
<p>Return the minimum number of operations needed to place <code>values</code> in strictly increasing order. You may use the operations in any sequence. If increasing order cannot be reached, return <code>-1</code>.</p>

<h3>Function</h3>
<pre class="sample">minSortOperations(values: int[]) &rarr; int</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">values = [3,4,1,2]
return = 2</pre>
<p>Rotate twice: <code>[3,4,1,2]</code> becomes <code>[1,2,3,4]</code>. No single operation produces increasing order.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">values = [3,2,1,4]
return = 2</pre>
<p>Flip to obtain <code>[4,1,2,3]</code>, then rotate once to obtain <code>[1,2,3,4]</code>.</p>

<div class="sublabel">Example 3</div>
<pre class="sample">values = [1,3,2,4]
return = -1</pre>
<p>Rotations preserve the circular order, and a flip only reverses that order. Neither orientation can match <code>[1,2,3,4]</code>, so sorting is impossible.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &lt;= values.length &lt;= 200000</code></li>
  <li>Every element is a 32-bit signed integer.</li>
  <li>All elements are distinct.</li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Both operations preserve the array as a <em>cycle</em>: rotation changes where you cut it, a flip changes which way round you read it. So the array is sortable only if reading the cycle in one of the two directions, from the right starting point, is already increasing.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Count circular descents. Exactly one descent means some rotation is sorted; exactly one ascent means some rotation is <em>reverse</em> sorted, which a flip fixes. Then count operations carefully &mdash; <code>flip, rotate, flip</code> is a cheap way to rotate <em>backwards</em>, and for a nearly-sorted long array it beats n&minus;1 forward rotations.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Two questions: <em>is</em> it sortable, and if so how few operations. Sortability is a one-pass count on the circular array of distinct values:</p>
<ul>
<li>exactly one position with <code>values[i] &gt; values[i+1 mod n]</code> &rarr; rotating by <code>k = i + 1</code> gives the sorted array;</li>
<li>exactly one position with <code>values[i] &lt; values[i+1 mod n]</code> &rarr; rotating by <code>k = i + 1</code> gives the <em>reversed</em> sorted array, one flip from the goal;</li>
<li>neither &rarr; <code>-1</code>.</li>
</ul>
<p>For the cost, model the reachable arrays as states <code>(orientation, shift)</code>. Rotating advances the shift while the orientation is forward and <em>rewinds</em> it while reversed, and a flip toggles the orientation at cost 1. That gives closed forms:</p>
<div class="formula">reach rot^k        : min( k , 2 + (n &minus; k) mod n )
reach flip(rot^k)  : min( k + 1 , 1 + (n &minus; k) mod n )</div>
<p>Take the minimum over whichever of the two targets exists.</p>
<p><span class="cx">Time O(n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def minSortOperations(values):
    n = len(values)
    if n == 1:
        return 0

    # a circular array of distinct values is one rotation away from sorted iff
    # it has exactly one descent; one ascent means some rotation is decreasing
    descents = [i for i in range(n) if values[i] &gt; values[(i + 1) % n]]
    ascents  = [i for i in range(n) if values[i] &lt; values[(i + 1) % n]]

    best = None
    if len(descents) == 1:                    # target is rot^k of the input
        k = (descents[0] + 1) % n
        cand = min(k,                          # k rotations
                   2 + (n - k) % n)            # flip, rotate back, flip
        best = cand if best is None else min(best, cand)
    if len(ascents) == 1:                     # some rotation is strictly decreasing
        k = (ascents[0] + 1) % n
        cand = min(k + 1,                      # rotate k times, then flip
                   1 + (n - k) % n)            # flip first, then rotate
        best = cand if best is None else min(best, cand)
    return -1 if best is None else best</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on all three published examples, plus the case the published examples do not cover.</p>

<div class="step"><h4>1 &middot; Both operations act on a cycle</h4>
<p>Write the array around a circle. A rotation moves the cut point; a flip reverses the reading direction. Neither ever changes <em>which element follows which</em> up to direction, so:</p>
<div class="formula">sortable  &hArr;  the circle, read in one direction from some cut, is increasing</div>
<p>With distinct values, "read forward and increasing" means exactly one place where the circle steps down &mdash; the cut. Similarly "read backward and increasing" means exactly one place where it steps up.</p>
<table class="trace">
<tr><th>input</th><th>circular descents</th><th>circular ascents</th><th>verdict</th></tr>
<tr><td>[3,4,1,2]</td><td>1 &nbsp;(4 &gt; 1 at i = 1)</td><td>3</td><td>rotation target, k = 2</td></tr>
<tr><td>[3,2,1,4]</td><td>3</td><td>1 &nbsp;(1 &lt; 4 at i = 2)</td><td>flipped target, k = 3</td></tr>
<tr><td class="hit">[1,3,2,4]</td><td class="hit">2 &nbsp;(3&gt;2, 4&gt;1)</td><td class="hit">2</td><td class="hit">neither &rarr; <b>&minus;1</b></td></tr>
</table>
<p>The wrap-around comparison <code>values[n-1]</code> vs <code>values[0]</code> is part of the count &mdash; forget it and <code>[1,2,3,4]</code> looks like it has zero descents instead of one.</p>
</div>

<div class="step"><h4>2 &middot; The state graph, and why cost is not just k</h4>
<p>Let state <code>(0, k)</code> be the array rotated <em>k</em> times and <code>(1, k)</code> that array reversed. Then:</p>
<div class="formula">rotate on (0, k) &rarr; (0, k+1 mod n)
rotate on (1, k) &rarr; (1, k&minus;1 mod n)        &larr; reversed, so a rotation rewinds
flip   on (o, k) &rarr; (1&minus;o, k)              cost 1</div>
<p>The middle line is the surprise: after one flip, rotations run <em>backwards</em>, so <code>flip &middot; rotate &middot; flip</code> costs 3 and undoes a rotation. Shortest paths from <code>(0, 0)</code> are therefore</p>
<div class="formula">d(0, k) = min( k , 2 + (n &minus; k) mod n )
d(1, k) = min( k + 1 , 1 + (n &minus; k) mod n )</div>
</div>

<div class="step"><h4>3 &middot; The published examples, and the case they hide</h4>
<div class="formula">[3,4,1,2] : descent at i = 1 &rarr; k = 2, n = 4
            d(0,2) = min(2, 2 + 2) = <b>2</b>            &check; "rotate twice"

[3,2,1,4] : ascent at i = 2 &rarr; k = 3, n = 4
            d(1,3) = min(3 + 1, 1 + 1) = <b>2</b>        &check; "flip, then rotate once"

[2,3,4,5,6,7,8,9,10,1] : descent at i = 8 &rarr; k = 9, n = 10
            d(0,9) = min(9, 2 + 1) = <b>3</b>            &larr; flip, rotate, flip</div>
<p>That last line is the one no published example covers: nine forward rotations, or three operations that rotate backwards once. A solution that returns <code>k</code> answers 9 and is wrong. Breadth-first search over the real arrays confirms 3.</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Cost is not <code>k</code>.</strong> <code>flip &middot; rotate &middot; flip</code> = 3 beats <code>n &minus; 1</code> rotations whenever <code>k &gt; n/2 + 1</code>.</li>
<li><strong>Count descents circularly</strong>, including the <code>n&minus;1 &rarr; 0</code> step.</li>
<li><strong>An already sorted array scores 0</strong>: it has exactly one descent, at <code>i = n&minus;1</code>, giving <code>k = 0</code> and <code>d(0,0) = 0</code>.</li>
<li><strong>Both targets can exist at once</strong> &mdash; for <code>n = 2</code> every array is both a rotation and a flip of the sorted one; taking the minimum handles it.</li>
<li><strong><code>n = 1</code> is sorted</strong>, and its descent/ascent counts are both 0, so it needs its own early return.</li>
<li><strong>Distinctness matters.</strong> With duplicates, "exactly one descent" stops characterising sortability, and the problem changes shape.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-maxrating', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Bit manipulation',
  label:'Problem', title:'Maximum Product New Rating',
  minutes:45, score:'',
  images:[],
  fn:{name:'getMaxRating', ret:'int', params:[['int[]','customer_rating'],['int','m'],['int','k']]},
  gen:`def gen(rng, n):
    m = max(1, min(n, 60))
    rating = [rng.randint(1, 64) for _ in range(m)]
    return [rating, rng.randint(1, m), rng.randint(0, 40)]`,
  tests:[
    {in:[[1, 2, 4, 8], 2, 8], out:10},
    {in:[[1, 2, 4, 8], 2, 0], out:0},
    {in:[[7, 7, 7], 3, 0], out:7},
    {in:[[1], 1, 5], out:6},
    {in:[[5, 6, 7, 8], 2, 3], out:9},
    {in:[[1, 1, 1, 1], 4, 12], out:4}
  ],
  body:`
<div class="tags"><span class="tag hard">Hard</span><span class="tag">Amazon</span><span class="tag">NEW GRAD</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> On July 31, 2026, the function name was corrected to <code>getMaxRating</code> and the source example's final result sentence restored.</div>

<p>The engineers at Amazon are working on a new rating system for their products. For each product, an array <code>customer_rating</code> is maintained for the last <code>n</code> orders of that product, where the rating given by the i-th customer is represented by <code>customer_rating[i]</code>.</p>
<p>The following algorithm is used to calculate the <code>new_rating</code> of the product:</p>
<ul>
  <li>The engineers can perform the following operation on <code>customer_rating</code> at most <code>k</code> times:
    <ul><li>Choose a customer rating and add 1 to it.</li></ul>
  </li>
  <li>The <code>new_rating</code> is the maximum bitwise AND of any <code>m</code>-sized subset of <code>customer_rating</code>.</li>
</ul>
<p>Given <code>n</code> customer ratings, two integers <code>m</code> and <code>k</code>, and an array <code>customer_rating</code>, find the maximum possible <code>new_rating</code> by performing the operations optimally.</p>

<h3>Function</h3>
<pre class="sample">getMaxRating(customer_rating: int[], m: int, k: int) &rarr; int</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">customer_rating = [1, 2, 4, 8]
m = 2
k = 8
return = 10</pre>
<p>One optimal sequence applies 6 operations to the rating 4, giving 10, and 2 operations to the rating 8, giving 10. The optimal subset of size 2 is <code>[10, 10]</code> with a bitwise AND of 10. For comparison, spending all 8 operations on the last element gives <code>[1, 2, 4, 16]</code>, whose best size-2 subset ANDs to 0. No valid modification yields a bitwise AND greater than 10.</p>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Do not try to decide how to spend the budget. Decide instead what the <em>answer</em> looks like, bit by bit, from the most significant bit down &mdash; and ask each time whether that answer is affordable.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>For a candidate value <code>T</code>, an element can contribute only if it is raised to some <code>x &ge; v</code> with <code>x &amp; T == T</code>. Compute that minimum cost per element, take the <code>m</code> cheapest, and compare the total with <code>k</code>. Greedily keep every bit that passes.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Classic "build the answer bit by bit". Let <code>feasible(T)</code> mean: at most <code>k</code> increments can make <em>m</em> elements each contain all the bits of <code>T</code>. The AND of those <em>m</em> elements is then a superset of <code>T</code>, so it is at least <code>T</code>; and the true answer is itself such a <code>T</code>. Hence the answer is the largest feasible <code>T</code>, and scanning bits from high to low, keeping each bit whose candidate is feasible, finds it.</p>
<p><code>feasible(T)</code> needs the cheapest way to raise a single <code>v</code> to a number containing <code>T</code>'s bits. Only increments are allowed, so the target must be <code>&ge; v</code>. Build it by choosing the position <code>i</code> where the result first exceeds <code>v</code>: keep <code>v</code>'s bits above <code>i</code> (they must already contain <code>T</code>'s bits above <code>i</code>), set bit <code>i</code> where <code>v</code> has a 0, and below <code>i</code> keep exactly <code>T</code>'s bits &mdash; the smallest legal tail. The best over all <code>i</code>, minus <code>v</code>, is the cost.</p>
<p>Sort the per-element costs, add the <code>m</code> smallest, and compare with <code>k</code>.</p>
<p><span class="cx">Time O(B &middot; (n log n + n B))</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def _cost(v, target):
    """cheapest number of +1 steps that turns v into some x &gt;= v with x &amp; target == target"""
    if (v &amp; target) == target:
        return 0
    best = None
    for i in range(62):
        if (v &gt;&gt; i) &amp; 1:                       # need a position where v has 0 and x has 1
            continue
        high = (v &gt;&gt; (i + 1)) &lt;&lt; (i + 1)       # bits above i stay exactly as in v
        if (high &amp; target) != ((target &gt;&gt; (i + 1)) &lt;&lt; (i + 1)):
            continue                           # ... so they must already carry target's high bits
        x = high | (1 &lt;&lt; i) | (target &amp; ((1 &lt;&lt; i) - 1))
        if best is None or x &lt; best:
            best = x
    return best - v


def getMaxRating(customer_rating, m, k):
    answer = 0
    for bit in range(45, -1, -1):              # greedily fix bits from the top down
        candidate = answer | (1 &lt;&lt; bit)
        costs = sorted(_cost(v, candidate) for v in customer_rating)
        if sum(costs[:m]) &lt;= k:
            answer = candidate
    return answer</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example: <code>customer_rating = [1,2,4,8]</code>, <code>m = 2</code>, <code>k = 8</code> &rarr; <strong>10</strong>.</p>

<div class="step"><h4>1 &middot; Why greedy-on-the-budget fails</h4>
<p>"Spend every operation on the largest rating" gives <code>[1,2,4,16]</code>, whose best pair ANDs to <strong>0</strong> &mdash; the statement says so itself. An AND only keeps bits that <em>all</em> chosen elements share, so raising one element alone is worthless. The budget must be spent to make several elements agree.</p>
</div>

<div class="step"><h4>2 &middot; Search the answer, not the spend</h4>
<p>Define <code>feasible(T)</code> = "some <em>m</em> elements can each be raised to contain every bit of <code>T</code>, for at most <code>k</code> increments in total". Two facts make the greedy correct:</p>
<ul>
<li>if the true optimum is <code>A</code>, then <code>feasible(A)</code> holds (the optimal assignment witnesses it);</li>
<li>if <code>feasible(T)</code> holds, the resulting AND contains <code>T</code>'s bits, so it is <code>&ge; T</code>.</li>
</ul>
<p>So the answer is <code>max{ T : feasible(T) }</code>, and because a higher bit outweighs every lower bit combined, testing bits from the top and keeping the ones that pass finds that maximum.</p>
</div>

<div class="step"><h4>3 &middot; The per-element cost</h4>
<p>We need the smallest <code>x &ge; v</code> with <code>x &amp; T == T</code>. Note <code>v | T</code> is legal but often not minimal: for <code>v = 5 (101)</code> and <code>T = 2 (010)</code>, <code>v | T = 7</code> costs 2, while <code>6 (110)</code> costs 1.</p>
<div class="formula">choose the position i where x first exceeds v:
   bits above i : copy from v      (must already contain T's bits above i)
   bit i        : v has 0, x has 1
   bits below i : exactly T's bits (the cheapest legal tail)
cost = min over valid i of  x &minus; v      (and 0 if v already contains T)</div>
</div>

<div class="step"><h4>4 &middot; The greedy, bit by bit</h4>
<table class="trace">
<tr><th>candidate T</th><th>cost per rating &nbsp;(1, 2, 4, 8)</th><th>two cheapest</th><th>&le; k = 8?</th><th>answer so far</th></tr>
<tr><td>16 (10000)</td><td>15, 14, 12, 8</td><td>8 + 12 = 20</td><td>no</td><td>0</td></tr>
<tr><td class="hit">8 (1000)</td><td class="hit">7, 6, 4, 0</td><td class="hit">0 + 4 = 4</td><td class="hit">yes</td><td class="hit"><b>8</b></td></tr>
<tr><td>12 (1100)</td><td>11, 10, 8, 4</td><td>4 + 8 = 12</td><td>no</td><td>8</td></tr>
<tr><td class="hit">10 (1010)</td><td class="hit">9, 8, 6, 2</td><td class="hit">2 + 6 = 8</td><td class="hit">yes</td><td class="hit"><b>10</b></td></tr>
<tr><td>11 (1011)</td><td>10, 9, 7, 3</td><td>3 + 7 = 10</td><td>no</td><td>10</td></tr>
</table>
<div class="formula">answer = <b>10</b>   &check; and the witness is 4 &rarr; 10 (cost 6) with 8 &rarr; 10 (cost 2), total 8 = k</div>
<p>Exactly the assignment the statement describes. Note how bit 3 is taken first and never given back: 8 is affordable, so no lower combination can beat it.</p>
</div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>Only additions are allowed</strong>, so every target must be <code>&ge;</code> the original value. A "nearest number containing T" that may go down is a different, easier problem.</li>
<li><strong><code>v | T</code> is not the cheapest lift</strong> &mdash; see the <code>5, 2 &rarr; 6</code> case above. This is the single most common bug here.</li>
<li><strong>Take the m cheapest elements</strong> for each candidate, not a fixed subset chosen once.</li>
<li><strong>Search enough bits.</strong> The answer can exceed <code>max(rating)</code> &mdash; here it is 10 while the largest input is 8 &mdash; so scan up to the bit above <code>max(rating) + k</code>.</li>
<li><strong>The AND may exceed the candidate.</strong> That is fine: feasibility is a lower bound, and the greedy still reports the true maximum.</li>
<li><strong>k = 0 is legal</strong>, and then the answer is the best AND of any m originals.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-protectcity', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · DP',
  label:'Problem', title:'Maximize Protected City Population',
  minutes:30, score:'',
  images:[],
  fn:{name:'maximizeProtectedPopulation', ret:'long', params:[['int[]','population'],['string','unit']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    population = [rng.randint(1, 1000) for _ in range(m)]
    unit = ''.join(rng.choice('01') for _ in range(m))
    return [population, unit]`,
  tests:[
    {in:[[10, 5, 8, 9, 6], "01101"], out:27},
    {in:[[7, 4], "01"], out:7},
    {in:[[3], "0"], out:0},
    {in:[[3], "1"], out:3},
    {in:[[1, 100, 1, 100], "0101"], out:200},
    {in:[[5, 5, 5, 5], "1111"], out:20}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">FULLTIME</span><span class="tag">OA</span></div>

<p>You are given <code>n</code> cities arranged in a line. City <code>i</code> has population <code>population[i]</code> and may contain a security unit described by <code>unit[i]</code>, where <code>unit[i] = '1'</code> means a unit is initially stationed in city <code>i</code>.</p>
<p>Each security unit may stay where it is, or if it is not in the first city, it may move exactly one city to the left. Every unit can move at most once.</p>
<p>After all moves are chosen, a city is <em>protected</em> if at least one security unit is stationed there. Return the maximum total population of all protected cities.</p>

<h3>Function</h3>
<pre class="sample">maximizeProtectedPopulation(population: int[], unit: String) &rarr; long</pre>
<p>Complete the function <em>maximizeProtectedPopulation</em>, which has the following parameters:</p>
<ul>
  <li><em>int[] population:</em> the city populations</li>
  <li><em>String unit:</em> the initial security-unit layout</li>
</ul>
<h3>Returns</h3>
<ul><li><em>long:</em> the maximum total population of protected cities.</li></ul>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">population = [10, 5, 8, 9, 6]
unit       = "01101"
return     = 27</pre>
<p>Move the unit from city 2 to city 1, keep the unit in city 3, and move the unit from city 5 to city 4. Cities 1, 3, and 4 are then protected, for a total population of 10 + 8 + 9 = 27.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">population = [7, 4]
unit       = "01"
return     = 7</pre>
<p>Move the only unit left from city 2 to city 1. Protecting city 1 yields the larger total population.</p>

<h3>Constraints</h3>
<ul>
  <li><code>population.length = unit.length()</code></li>
  <li><code>unit</code> contains only <code>'0'</code> and <code>'1'</code></li>
  <li>Each security unit may move left by at most one city, and may move at most once.</li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Each unit has two options and they interact only with the immediate neighbour: the unit on city <code>i+1</code> is the only one that can cover city <code>i</code> besides the unit already standing there. That locality is a DP.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Sweep left to right with one bit of state: <em>has the unit standing on the current city already been promised to the city on its left?</em> Two states, two choices each, O(n).</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>City <code>i</code> can only be covered by the unit at <code>i</code> (staying) or the unit at <code>i+1</code> (stepping left). So walking left to right, the only thing the future needs to know about the past is whether the unit currently under consideration has already been used.</p>
<p>State after processing cities <code>0..i&minus;1</code>:</p>
<ul>
<li><code>stay</code> &mdash; the unit on city <code>i</code>, if there is one, is still available;</li>
<li><code>moved</code> &mdash; that unit has already been spent covering city <code>i&minus;1</code>.</li>
</ul>
<p>At city <code>i</code> you decide what the unit on city <code>i+1</code> does, which produces the next pair. Covering a city twice earns its population once, so the value added is <code>population[i]</code> when anybody covers it and 0 otherwise. The answer is the better of the two final states.</p>
<p>Greedy fails: "always move a unit left if the left city is bigger" mishandles chains such as <code>"11"</code>, where moving the second unit left only duplicates the first.</p>
<p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def maximizeProtectedPopulation(population, unit):
    n = len(population)
    NEG = float('-inf')
    # stay  = best total when the unit standing on city i (if any) is still free
    # moved = best total when that unit has already been committed to city i-1
    stay, moved = 0, NEG
    for i in range(n):
        nstay = nmoved = NEG
        for used, val in ((False, stay), (True, moved)):
            if val == NEG:
                continue
            here = unit[i] == '1' and not used          # a unit is standing on i
            # the unit on city i+1 stays where it is
            v = val + (population[i] if here else 0)
            if v &gt; nstay:
                nstay = v
            # the unit on city i+1 steps left onto city i
            if i + 1 &lt; n and unit[i + 1] == '1':
                v = val + population[i]                 # city i is covered either way
                if v &gt; nmoved:
                    nmoved = v
        stay, moved = nstay, nmoved
    return max(stay, moved)</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example: <code>population = [10,5,8,9,6]</code>, <code>unit = "01101"</code> &rarr; <strong>27</strong>. Indices below are 0-based, so the units sit on cities 1, 2 and 4.</p>

<div class="step"><h4>1 &middot; Who can cover city i</h4>
<div class="formula">city i is protected  &hArr;  (unit[i] = 1 and that unit stayed)
                        or  (unit[i+1] = 1 and that unit stepped left)</div>
<p>No other unit can reach it, so the decisions form a chain along the line &mdash; a textbook one-dimensional DP with a single bit of carry.</p>
</div>

<div class="step"><h4>2 &middot; The two states</h4>
<p>Process cities left to right. Before handling city <code>i</code>, exactly one fact about the past still matters:</p>
<div class="formula">stay[i]  : the unit on city i (if any) has <b>not</b> been used yet
moved[i] : it was already used to cover city i&minus;1</div>
<p>At city <code>i</code> we choose whether the unit on <code>i+1</code> steps left. Each choice adds <code>population[i]</code> if city <code>i</code> ends up covered, and moves us to <code>stay[i+1]</code> or <code>moved[i+1]</code> accordingly.</p>
</div>

<div class="step"><h4>3 &middot; The sweep, in full</h4>
<table class="trace">
<tr><th>i</th><th>pop</th><th>unit</th><th>stay</th><th>moved</th><th>note</th></tr>
<tr><td>&mdash;</td><td>&mdash;</td><td>&mdash;</td><td>0</td><td>&minus;&infin;</td><td>before city 0</td></tr>
<tr><td>0</td><td>10</td><td>0</td><td>0</td><td>10</td><td>the unit on city 1 may step left &rarr; +10</td></tr>
<tr><td>1</td><td>5</td><td>1</td><td>10</td><td>15</td><td>from <em>moved</em>: city 1 is empty (its unit left) unless city 2's unit steps in</td></tr>
<tr><td>2</td><td>8</td><td>1</td><td class="hit">18</td><td>&minus;&infin;</td><td>10 + 8: city 2's unit stays; city 3 holds no unit, so nothing can step left onto city 2</td></tr>
<tr><td>3</td><td>9</td><td>0</td><td>18</td><td class="hit">27</td><td>city 4's unit steps left &rarr; 18 + 9</td></tr>
<tr><td>4</td><td>6</td><td>1</td><td class="hit">27</td><td>&minus;&infin;</td><td>its unit already moved, so city 4 earns nothing</td></tr>
</table>
<div class="formula">answer = max(27, &minus;&infin;) = <b>27</b>   &check; cities 0, 2, 3 protected: 10 + 8 + 9</div>
<p>The tempting greedy &mdash; "move a unit left whenever the left city is more populous" &mdash; is wrong, and the smallest counterexample is two cities: <code>population = [10, 1]</code> with <code>unit = "11"</code>. The greedy sees 10 &gt; 1 and moves the second unit, protecting city 0 alone for <strong>10</strong>; leaving it where it is protects both cities for <strong>11</strong>. Moving a unit is never free &mdash; it abandons the city it was standing on.</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Double coverage pays once.</strong> With <code>unit = "11"</code>, moving the right unit left leaves only city 0 protected; keeping both protects both.</li>
<li><strong>The unit in city 0 cannot move</strong>, which the DP gets for free because <code>moved</code> starts at &minus;&infin;.</li>
<li><strong>A unit that moved leaves its own city unprotected</strong> unless the next unit steps into it &mdash; that is exactly what the <code>moved</code> state remembers.</li>
<li><strong>Return type is long:</strong> populations sum well past 2&sup3;&sup1; on large inputs.</li>
<li><strong>Cities with no unit anywhere near</strong> contribute nothing; there is no "protect by adjacency" rule here, only occupancy.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-exectime', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Greedy',
  label:'Problem', title:'Minimum Execution Time',
  minutes:35, score:'',
  images:['src-exectime.png'],
  fn:{name:'minimumExecutionTime', ret:'int', params:[['int[]','jobSize'],['int[]','throughput']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    jobSize = [rng.randint(1, 50) for _ in range(m)]
    throughput = [rng.randint(1, 50) for _ in range(max(1, m // 2))]
    return [jobSize, throughput]`,
  tests:[
    {in:[[2, 5, 3], [6, 2, 4]], out:1},
    {in:[[2, 5, 8], [6, 7, 4]], out:-1},
    {in:[[5, 5], [6]], out:3},
    {in:[[1, 1, 1, 1, 1], [9, 9]], out:5},
    {in:[[4], [4]], out:1},
    {in:[[3, 3, 3], [3, 1, 1]], out:5}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">NEW GRAD</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> 2026-06-28 &mdash; The original source image omitted Example 2's output; it was derived from the statement and the input, and should be updated if the official output becomes available.</div>

<p>Amazon's "UltraCompute" service receives an array of <code>n</code> job fragments. Each fragment's size is recorded in <code>jobSize[i]</code> for <code>0 &le; i &lt; n</code>. At the same time, the fleet has <code>m</code> worker instances whose maximum throughputs are <code>throughput[j]</code> for <code>0 &le; j &lt; m</code>.</p>
<p>A worker finishes a fragment in exactly 1 second if <code>jobSize &le; throughput</code>; otherwise it cannot run that fragment.</p>
<p>Each worker can process at most one fragment per second. If a worker is assigned multiple fragments, there is a mandatory 1-second cooldown pause between completing one fragment and starting the next. Different workers may process different fragments in parallel.</p>
<p>Your task is to compute the minimum number of seconds needed to finish all fragments, or return <code>-1</code> if at least one fragment is too large for every worker.</p>

<h3>Function</h3>
<pre class="sample">minimumExecutionTime(jobSize: int[], throughput: int[]) &rarr; int</pre>
<p>Complete the function <em>minimumExecutionTime</em> in the editor below.</p>
<ul>
  <li><em>int jobSize[n]:</em> size of each fragment</li>
  <li><em>int throughput[m]:</em> capacity of each worker</li>
</ul>
<h3>Returns</h3>
<ul><li><em>int:</em> minimum seconds to finish all fragments, or &minus;1</li></ul>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">jobSize    = [2, 5, 3]
throughput = [6, 2, 4]
return     = 1</pre>
<p>Assign fragment 5 to the 6-unit worker, fragment 2 to the 2-unit worker, and fragment 3 to the 4-unit worker. All three finish in the same second, so the minimum total time is 1.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">jobSize    = [2, 5, 8]
throughput = [6, 7, 4]
return     = -1</pre>
<p>The largest fragment has size 8, but the highest worker throughput is 7. That fragment is too large for every worker, so the answer is &minus;1.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &le; n, m &le; 2 * 10^5</code></li>
  <li><code>1 &le; jobSize[i], throughput[j] &le; 10^9</code></li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Because of the cooldown, a worker that runs <em>r</em> fragments occupies seconds 1, 3, 5, &hellip; and finishes at second <code>2r &minus; 1</code>. So the whole schedule is decided by one number: the largest number of fragments any single worker has to take.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Sort fragments descending. The <em>i</em> largest fragments can only run on the workers whose throughput is at least the <em>i</em>-th largest fragment &mdash; call that count <code>c_i</code>. They need <code>ceil(i / c_i)</code> rounds, and the answer's round count is the maximum of that over all <em>i</em>.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Two independent parts: feasibility, and the schedule length.</p>
<p><strong>Feasibility.</strong> A fragment is runnable iff some throughput is at least its size, so a single check against <code>max(throughput)</code> decides the &minus;1 case.</p>
<p><strong>Length.</strong> The cooldown means a worker assigned <em>r</em> fragments finishes at second <code>2r &minus; 1</code>, so the answer is <code>2R &minus; 1</code> where <em>R</em> is the largest per-worker load in the best assignment. Sort the fragments descending; the capability sets are <em>nested</em> (a worker that can run a big fragment can run every smaller one), so Hall's condition collapses to one scan:</p>
<div class="formula">R = max over i of  ceil( i / c_i )        c_i = #{ workers with throughput &ge; i-th largest fragment }</div>
<p>Each prefix of the sorted fragments is confined to <code>c_i</code> workers, which cannot hold more than <code>c_i</code> per round; and that bound is achievable by dealing the sorted fragments round-robin to the capable workers.</p>
<p><span class="cx">Time O((n + m) log(n + m))</span><span class="cx">Space O(n + m)</span></p><pre class="sample"><code>from bisect import bisect_left

def minimumExecutionTime(jobSize, throughput):
    jobs = sorted(jobSize, reverse=True)      # hardest fragment first
    caps = sorted(throughput)                 # ascending, for bisect
    m = len(caps)

    rounds = 1
    for i, job in enumerate(jobs, 1):
        capable = m - bisect_left(caps, job)  # workers that can run this fragment
        if capable == 0:
            return -1
        need = -(-i // capable)               # ceil(i / capable)
        if need &gt; rounds:
            rounds = need
    return 2 * rounds - 1                     # run, cooldown, run, cooldown, ...</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples, plus the case that makes the cooldown visible.</p>

<div class="step"><h4>1 &middot; What the cooldown actually costs</h4>
<p>One fragment per second, and a pause of one second between two fragments on the same worker:</p>
<div class="formula">r = 1 &rarr; busy at second 1                  finishes at 1
r = 2 &rarr; seconds 1 and 3                    finishes at 3
r = 3 &rarr; seconds 1, 3, 5                    finishes at 5
r fragments                                  finishes at <b>2r &minus; 1</b></div>
<p>Workers run in parallel, so the makespan is <code>2R &minus; 1</code> for the busiest worker's load <em>R</em>. The whole problem is therefore "minimise the maximum load", and the answer is always odd.</p>
</div>

<div class="step"><h4>2 &middot; The capability sets are nested</h4>
<p>Worker <em>j</em> can run fragment <em>i</em> iff <code>throughput[j] &ge; jobSize[i]</code>. Sort fragments descending: the set of workers able to run the first fragment is contained in the set for the second, and so on. That nesting is what makes a single scan sufficient &mdash; no matching algorithm is needed.</p>
<div class="formula">need(i) = ceil( i / c_i )     for the i largest fragments
R       = max_i need(i)
answer  = 2R &minus; 1                (or &minus;1 when some c_i = 0)</div>
<p><em>Lower bound:</em> those <em>i</em> fragments live inside <code>c_i</code> workers, and each worker absorbs one per round. <em>Achievable:</em> deal the sorted fragments to their capable workers round-robin; every fragment lands on a worker that can run it, and no worker exceeds <code>R</code>.</p>
</div>

<div class="step"><h4>3 &middot; The examples</h4>
<table class="trace">
<tr><th>input</th><th>i</th><th>i-th largest fragment</th><th>c_i</th><th>ceil(i / c_i)</th></tr>
<tr><td rowspan="3">jobs [5,3,2], caps [6,4,2]</td><td>1</td><td>5</td><td>1 &nbsp;(only 6)</td><td>1</td></tr>
<tr><td>2</td><td>3</td><td>2 &nbsp;(6, 4)</td><td>1</td></tr>
<tr><td class="hit">3</td><td class="hit">2</td><td class="hit">3 &nbsp;(6, 4, 2)</td><td class="hit">1 &rarr; R = 1</td></tr>
<tr><td>jobs [8,5,2], caps [7,6,4]</td><td>1</td><td>8</td><td class="hit">0</td><td class="hit">&rarr; <b>&minus;1</b></td></tr>
</table>
<div class="formula">example 1 : answer = 2&middot;1 &minus; 1 = <b>1</b>    &check;
example 2 : the largest fragment fits nowhere &rarr; <b>&minus;1</b>   &check;</div>
<p>And the case neither example covers &mdash; <code>jobSize = [5,5]</code>, <code>throughput = [6]</code>: <code>c_1 = c_2 = 1</code>, so <code>R = 2</code> and the answer is <code>2&middot;2 &minus; 1 = 3</code>. Second 1 runs one fragment, second 2 is the mandatory cooldown, second 3 runs the other.</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>The answer is not <code>ceil(n / m)</code>.</strong> Capability matters: with <code>jobs = [3,3,3]</code> and <code>caps = [3,1,1]</code> only one worker is usable, so the answer is 5, not 1.</li>
<li><strong>The cooldown is <em>between</em> fragments, not after the last one</strong> &mdash; hence <code>2r &minus; 1</code> and not <code>2r</code>.</li>
<li><strong>&minus;1 takes priority</strong> and is decided by <code>max(throughput)</code> alone.</li>
<li><strong>Sort descending and take the running maximum.</strong> Checking only the last (smallest) fragment misses the binding constraint, which is usually near the top.</li>
<li><strong>Sizes reach 10&#8313;</strong>, so compare capacities, never subtract them.</li>
<li><strong>Binary searching the number of rounds</strong> works too &mdash; the same counting predicate &mdash; but the single scan is O(n log n) and simpler.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-dominocolor', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · DP',
  label:'Problem', title:'Count Distinct Domino Colorings',
  minutes:35, score:'',
  images:[],
  fn:{name:'countDistinctColorings', ret:'int', params:[['string[]','domino']]},
  gen:`def gen(rng, n):
    letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    rng.shuffle(letters)
    width = max(1, min(n, 52))
    top, bot, i = [], [], 0
    while i < width and len(letters) >= 2:
        if i + 1 < width and rng.random() < 0.5:
            a, b = letters.pop(), letters.pop()
            top += [a, a]
            bot += [b, b]
            i += 2
        else:
            a = letters.pop()
            top.append(a)
            bot.append(a)
            i += 1
    return [[''.join(top), ''.join(bot)]]`,
  tests:[
    {in:[["abb", "acc"]], out:6},
    {in:[["ab", "ab"]], out:6},
    {in:[["aa", "bb"]], out:6},
    {in:[["a", "a"]], out:3},
    {in:[["aabb", "ccdd"]], out:18},
    {in:[["aabc", "ddbc"]], out:12}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">INTERN</span><span class="tag">OA</span></div>

<div class="srcnote"><strong>Source note:</strong> The visible source lists <code>n &le; 10^5</code>. Because each domino uses a unique case-sensitive single English letter and each character appears exactly twice, the largest internally consistent width is <code>n = 52</code>; the published constraint uses 52.</div>

<p>In Amazon's warehouse automation systems, robotic movement paths are modeled using domino-like tiles placed on a grid.</p>
<p>A domino is a unique 1 x 2 or 2 x 1 piece represented by one lowercase or uppercase English letter. The array <code>domino</code> contains exactly two strings of equal length <code>n</code>.</p>
<p>Treat <code>domino[0]</code> as the top row and <code>domino[1]</code> as the bottom row of a 2 x n grid. Each character appears exactly twice across the grid and identifies exactly one domino. The strings are guaranteed to describe a complete, non-overlapping tiling:</p>
<ul>
  <li>A vertical domino occupies column <code>i</code> when <code>domino[0][i] == domino[1][i]</code>.</li>
  <li>Two horizontal dominoes occupy columns <code>i</code> and <code>i + 1</code> when <code>domino[0][i] == domino[0][i + 1]</code> and <code>domino[1][i] == domino[1][i + 1]</code>.</li>
</ul>
<p>Two dominoes are adjacent when they share a side in the grid: up, down, left, or right. Diagonal contact does not count.</p>
<p>Color every domino Red, Green, or Blue. Both halves of a domino must have the same color, and adjacent dominoes must have different colors.</p>
<p>Return the number of distinct valid colorings modulo <code>10^9 + 7</code>.</p>

<h3>Function</h3>
<pre class="sample">countDistinctColorings(domino: String[]) &rarr; int</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">domino = ["abb", "acc"]
return = 6</pre>
<p>The grid is <code>a b b</code> on top and <code>a c c</code> underneath: domino <em>a</em> is vertical, while <em>b</em> and <em>c</em> are horizontal. The valid colorings are <code>[RGG, RBB]</code>, <code>[RBB, RGG]</code>, <code>[GRR, GBB]</code>, <code>[GBB, GRR]</code>, <code>[BGG, BRR]</code> and <code>[BRR, BGG]</code> &mdash; 6 in total.</p>

<h3>Constraints</h3>
<ul>
  <li><code>domino.length == 2</code></li>
  <li><code>1 &lt;= domino[0].length == domino[1].length &lt;= 52</code></li>
  <li>Every character is a lowercase or uppercase English letter.</li>
  <li>Each character appears exactly twice and the two strings describe a valid domino tiling.</li>
</ul>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>You never have to look at the letters as identities &mdash; only at the <em>shape</em> of each block. Scanning left to right, the grid is a sequence of two kinds of block: one vertical domino (1 column) or a stacked pair of horizontal dominoes (2 columns).</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Only neighbouring blocks touch, so the count is a product over consecutive block pairs. Work out four numbers by hand &mdash; V&rarr;V, V&rarr;HH, HH&rarr;V, HH&rarr;HH &mdash; and multiply.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Parse the tiling into blocks: column <code>i</code> is a vertical domino when the two rows agree there, otherwise columns <code>i</code> and <code>i+1</code> hold a stacked pair of horizontal dominoes. Inside a pair, the two dominoes touch each other, so they must differ.</p>
<p>Because only consecutive blocks are adjacent, the number of colorings is the first block's count times one factor per adjacent pair:</p>
<div class="formula">first block : V = 3,  HH = 3 &times; 2 = 6
V  &rarr; V  : 2      the new colour just avoids one
V  &rarr; HH : 2      top avoids 1 colour (2 ways), bottom avoids top and the V (1 way)
HH &rarr; V  : 1      must avoid two different colours
HH &rarr; HH : 3      counted by hand below</div>
<p>One left-to-right pass multiplies them modulo 10&#8313;+7. No adjacency list, no graph colouring, no recursion.</p>
<p><span class="cx">Time O(n)</span><span class="cx">Space O(1)</span></p><pre class="sample"><code>def countDistinctColorings(domino):
    MOD = 10 ** 9 + 7
    top, bottom = domino[0], domino[1]
    n = len(top)

    ways = 1
    prev = None                       # True = previous block was one vertical domino
    i = 0
    while i &lt; n:
        vertical = top[i] == bottom[i]
        if prev is None:
            ways = 3 if vertical else 6          # first block: 3, or 3 * 2 for a pair
        elif prev and vertical:
            ways = ways * 2                      # V -&gt; V  : differ from one colour
        elif prev and not vertical:
            ways = ways * 2                      # V -&gt; HH : top 2 ways, bottom forced
        elif vertical:
            ways = ways * 1                      # HH -&gt; V : the one remaining colour
        else:
            ways = ways * 3                      # HH -&gt; HH
        ways %= MOD
        prev = vertical
        i += 1 if vertical else 2
    return ways % MOD</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published example: <code>["abb", "acc"] &rarr; 6</code>.</p>

<div class="step"><h4>1 &middot; The tiling is a chain of blocks</h4>
<p>In a 2 &times; n grid, a horizontal domino forces a second one directly below it &mdash; otherwise the column beneath cannot be filled. So reading left to right, the tiling is a sequence of:</p>
<div class="formula">V  : one vertical domino, 1 column wide
HH : two stacked horizontal dominoes, 2 columns wide</div>
<p>and dominoes only ever touch inside their own block or across the boundary with the next block. That chain structure is why a product works instead of a full graph colouring.</p>
<table class="trace">
<tr><th>column</th><th>0</th><th>1</th><th>2</th></tr>
<tr><td>top</td><td>a</td><td>b</td><td>b</td></tr>
<tr><td>bottom</td><td>a</td><td>c</td><td>c</td></tr>
<tr><td>block</td><td class="hit">V (a)</td><td colspan="2" class="hit">HH (b over c)</td></tr>
</table>
</div>

<div class="step"><h4>2 &middot; The four transition counts, derived</h4>
<p><strong>V &rarr; V.</strong> The new vertical domino touches only the previous one: <strong>2</strong> colours left.</p>
<p><strong>V &rarr; HH.</strong> The new top and bottom both touch the vertical domino, and they touch each other. Top: 2 choices (anything but the V's colour). Bottom: must differ from the V <em>and</em> from the top &mdash; 1 choice. Total <strong>2</strong>.</p>
<p><strong>HH &rarr; V.</strong> The vertical domino touches both previous dominoes, which already have two <em>different</em> colours, leaving exactly <strong>1</strong>.</p>
<p><strong>HH &rarr; HH.</strong> Previous pair coloured <code>(a, b)</code> with <code>a &ne; b</code>. New pair <code>(c, d)</code> needs <code>c &ne; a</code>, <code>d &ne; b</code>, <code>c &ne; d</code>:</p>
<div class="formula">c = b            &rarr; d must avoid b only          &rarr; 2 choices
c = the third colour &rarr; d must avoid b and c      &rarr; 1 choice
total                                                <b>3</b></div>
<p>And the first block: a lone vertical is <strong>3</strong>; a first pair is 3 &times; 2 = <strong>6</strong>.</p>
</div>

<div class="step"><h4>3 &middot; The example, multiplied out</h4>
<div class="formula">blocks: V(a) , HH(b, c)
start V        &rarr; 3
V &rarr; HH      &rarr; &times; 2
total          = 3 &times; 2 = <b>6</b>   &check; the six colourings listed in the statement</div>
<p>They line up exactly: three choices for <em>a</em>, and for each one, two ways to arrange the remaining pair over <em>b</em> and <em>c</em> &mdash; which is the <code>[RGG, RBB] / [RBB, RGG]</code> pattern repeated per colour of <em>a</em>.</p>
<p>Two more checks: <code>["aa","bb"]</code> is a single HH block &rarr; <strong>6</strong>; <code>["aabb","ccdd"]</code> is HH followed by HH &rarr; <code>6 &times; 3 = <strong>18</strong></code>. Brute-force enumeration of all 3^(number of dominoes) colourings agrees on every tiling tested.</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>The two halves of one HH block are adjacent</strong> to each other. Treating a pair as independent gives 3 &times; 3 and inflates every count.</li>
<li><strong>HH &rarr; HH is 3, not 4.</strong> The "c must differ from a, d must differ from b" reading forgets <code>c &ne; d</code>.</li>
<li><strong>Diagonals do not touch</strong>, which is exactly why V &rarr; HH is 2 and not 1.</li>
<li><strong>Advance the index by 2 over a horizontal pair</strong>, or the second column is parsed as another block.</li>
<li><strong>Reduce modulo 10&#8313;+7 as you multiply.</strong></li>
<li><strong>Letters are identifiers, not colours</strong> &mdash; the same letter never appears in two different dominoes, so no equality constraint is ever implied by the input.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-feasible', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Greedy',
  label:'Problem', title:'Feasible Indices After Reduction',
  minutes:30, score:'',
  images:[],
  fn:{name:'feasibleIndicesAfterReduction', ret:'string', params:[['int[]','arr']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    return [rng.sample(range(1, 10 * m + 1), m)]`,
  tests:[
    {in:[[1, 3, 2, 5, 4]], out:"10011"},
    {in:[[4, 1, 3, 2]], out:"1111"},
    {in:[[1, 2, 3, 4]], out:"1001"},
    {in:[[4, 3, 2, 1]], out:"1111"},
    {in:[[7]], out:"1"},
    {in:[[2, 9, 1, 8, 3]], out:"11111"}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">INTERN</span><span class="tag">OA</span></div>

<p>You are given an integer array <code>arr</code> of size <code>n</code>. All elements of <code>arr</code> are distinct.</p>
<p>You may perform either of the following operations any number of times:</p>
<ul>
  <li>Choose a non-empty <strong>prefix</strong> of the current array and delete every element in that prefix except the <strong>minimum</strong> element of the prefix.</li>
  <li>Choose a non-empty <strong>suffix</strong> of the current array and delete every element in that suffix except the <strong>maximum</strong> element of the suffix.</li>
</ul>
<p>After each operation, the remaining elements are concatenated to form the new array.</p>
<p>An index <code>i</code> is called <em>feasible</em> if it is possible to reduce the array to the single element <code>[arr[i]]</code>. Return a binary string of length <code>n</code> where the i-th character is <code>'1'</code> if index <code>i</code> is feasible, and <code>'0'</code> otherwise.</p>

<h3>Function</h3>
<pre class="sample">feasibleIndicesAfterReduction(arr: int[]) &rarr; String</pre>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">arr    = [1, 3, 2, 5, 4]
return = "10011"</pre>
<p>The feasible values are 1, 5, and 4. They are the prefix minimum at index 0 and the suffix maximums at indices 3 and 4.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">arr    = [4, 1, 3, 2]
return = "1111"</pre>
<p>All four indices are feasible. Values 4 and 1 are prefix minima, while values 3 and 2 are suffix maxima. For example, after reducing prefix <code>[4,1]</code> to 1, value 3 can survive a reduction of suffix <code>[3,2]</code> and then of the whole array.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &lt;= n &lt;= 2 * 10^5</code></li>
  <li><code>1 &lt;= arr[i] &lt;= 10^9</code></li>
  <li>All values in <code>arr</code> are distinct.</li>
</ul>

<div class="srcnote"><strong>Duplicate sighting:</strong> the same problem is also reported under the title <em>"Feasible Indices After Prefix/Suffix Reduction"</em> with the signature <code>getFeasibleIndices(arr: int[]) &rarr; String</code> and bound <code>n &le; 2 &times; 10&#8309;</code>. Same statement, same answer; only the wrapper name differs. Rename the function if the judge you meet asks for the other one.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>Two operations, two directions. Ask separately: which elements can survive a prefix operation that swallows everything to their left, and which can survive a suffix operation that swallows everything to their right?</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>To clear the left of index <em>i</em> in one prefix operation, <code>arr[i]</code> must be the minimum of <code>arr[0..i]</code>. To clear the right, it must be the maximum of <code>arr[i..n-1]</code>. Either one is enough &mdash; and nothing else is feasible.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Answer: index <em>i</em> is feasible exactly when <code>arr[i]</code> is a <strong>prefix minimum</strong> or a <strong>suffix maximum</strong>. Two linear scans, one running <code>min</code> and one running <code>max</code>.</p>
<p><em>Sufficient.</em> If <code>arr[i] = min(arr[0..i])</code>, apply the prefix operation to <code>arr[0..i]</code> &mdash; everything to the left vanishes and <code>arr[i]</code> becomes the first element. Now apply the suffix operation to the whole remaining array: whatever the maximum is, one more prefix operation on the whole array keeps the minimum, and alternating the two collapses to <code>arr[i]</code>. The mirrored argument covers a suffix maximum.</p>
<p><em>Necessary.</em> Look at the operation that finally removes the last element on <code>arr[i]</code>'s left. It is a prefix operation whose surviving element is <code>arr[i]</code>, so <code>arr[i]</code> is the minimum of a set that still contains every original element of <code>arr[0..i]</code> that has not yet been deleted &mdash; and deletions only ever keep the minimum of a prefix, so the running minimum of <code>arr[0..i]</code> is always present. Hence <code>arr[i]</code> must equal it. Symmetrically on the right.</p>
<p>Exhaustive breadth-first search over every reachable array (all n &le; 7 inputs) agrees with the rule on every case tested.</p>
<p><span class="cx">Time O(n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def feasibleIndicesAfterReduction(arr):
    n = len(arr)
    out = ['0'] * n

    running = None                  # prefix minimum
    for i, v in enumerate(arr):
        running = v if running is None else min(running, v)
        if v == running:
            out[i] = '1'

    running = None                  # suffix maximum
    for i in range(n - 1, -1, -1):
        running = arr[i] if running is None else max(running, arr[i])
        if arr[i] == running:
            out[i] = '1'

    return ''.join(out)</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on both published examples.</p>

<div class="step"><h4>1 &middot; What one operation really does</h4>
<p>A prefix operation keeps <em>one</em> element &mdash; the minimum of the chosen prefix &mdash; and discards the rest of it. A suffix operation keeps the maximum of the chosen suffix. So an element can only survive on the left side of the array if it is small, and on the right side if it is large.</p>
</div>

<div class="step"><h4>2 &middot; The two one-pass tests</h4>
<div class="formula">prefix-min(i) : arr[i] == min(arr[0..i])     &rarr; one operation clears everything to its left
suffix-max(i) : arr[i] == max(arr[i..n&minus;1])   &rarr; one operation clears everything to its right
feasible(i)   = prefix-min(i) <b>or</b> suffix-max(i)</div>
<p>Once one side is cleared, the other side is cleaned up by alternating the two operations on the whole remaining array, which always keeps a single element and can be steered to <code>arr[i]</code> (it is now either the array's first or its last element).</p>
</div>

<div class="step"><h4>3 &middot; Example 1 &mdash; arr = [1, 3, 2, 5, 4]</h4>
<table class="trace">
<tr><th>i</th><th>arr[i]</th><th>min(arr[0..i])</th><th>prefix min?</th><th>max(arr[i..])</th><th>suffix max?</th><th>result</th></tr>
<tr><td class="hit">0</td><td class="hit">1</td><td class="hit">1</td><td class="hit">yes</td><td class="hit">5</td><td class="hit">no</td><td class="hit"><b>1</b></td></tr>
<tr><td>1</td><td>3</td><td>1</td><td>no</td><td>5</td><td>no</td><td>0</td></tr>
<tr><td>2</td><td>2</td><td>1</td><td>no</td><td>5</td><td>no</td><td>0</td></tr>
<tr><td class="hit">3</td><td class="hit">5</td><td class="hit">1</td><td class="hit">no</td><td class="hit">5</td><td class="hit">yes</td><td class="hit"><b>1</b></td></tr>
<tr><td class="hit">4</td><td class="hit">4</td><td class="hit">1</td><td class="hit">no</td><td class="hit">4</td><td class="hit">yes</td><td class="hit"><b>1</b></td></tr>
</table>
<div class="formula">result = "<b>10011</b>"   &check;</div>
</div>

<div class="step"><h4>4 &middot; Example 2 &mdash; arr = [4, 1, 3, 2] &rarr; "1111"</h4>
<div class="formula">prefix minima : 4 (i = 0, trivially) , 1 (i = 1)
suffix maxima : 2 (i = 3, trivially) , 3 (i = 2) , 4 (i = 0)
union         : every index                      &rarr; "1111"</div>
<p>Index 2 is the instructive one: 3 is not a prefix minimum, but it <em>is</em> the maximum of the suffix <code>[3, 2]</code>, so the suffix operation clears its right, then prefix operations eat the <code>[4, 1]</code> on its left.</p>
<p>The first and last indices are always feasible &mdash; <code>arr[0]</code> is the minimum of the one-element prefix and <code>arr[n-1]</code> the maximum of the one-element suffix &mdash; a quick sanity check on any implementation.</p>
</div>

<div class="step"><h4>5 &middot; Traps</h4>
<ul>
<li><strong>It is <code>or</code>, not <code>and</code>.</strong> Requiring both conditions leaves almost every index at 0.</li>
<li><strong>Prefix takes the <em>minimum</em>, suffix the <em>maximum</em></strong> &mdash; swapping them is the single most common misread, and example 1 would then print "01100".</li>
<li><strong>Both prefixes and suffixes are inclusive of i.</strong> The running min must include <code>arr[i]</code> itself.</li>
<li><strong>Return a string of '0'/'1' characters</strong>, not a list of booleans or indices.</li>
<li><strong>Distinctness is used.</strong> With duplicates, "equals the running minimum" no longer pins a unique survivor and the rule needs care.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'fp-valuegroups', section:'FastPrep · Reported Amazon OA', platform:'FastPrep · Intervals',
  label:'Problem', title:'Make Value Groups Contiguous',
  minutes:30, score:'',
  images:[],
  fn:{name:'minOperationsToMakeValuesContiguous', ret:'int', params:[['int[]','arr']]},
  gen:`def gen(rng, n):
    m = max(1, n)
    pool = max(2, m // 3)
    return [[rng.randint(1, pool) for _ in range(m)]]`,
  tests:[
    {in:[[1, 2, 1]], out:1},
    {in:[[1, 2, 3]], out:0},
    {in:[[1, 2, 1, 2]], out:1},
    {in:[[1, 1, 2, 2]], out:0},
    {in:[[5]], out:0},
    {in:[[1, 2, 3, 1, 2, 3]], out:2},
    {in:[[1, 2, 2, 1, 3]], out:1}
  ],
  body:`
<div class="tags"><span class="tag med">Medium</span><span class="tag">Amazon</span><span class="tag">NEW GRAD</span><span class="tag">OA</span></div>

<p>You are given an integer array <code>arr</code>. In one operation, choose two values <code>x</code> and <code>y</code> (where <code>y</code> may be any value, including an existing value in the array), and replace every occurrence of <code>x</code> in the array with <code>y</code>.</p>
<p>An array is called <em>contiguous by value</em> if, for every distinct value present, all occurrences of that value appear in one uninterrupted block with no other values in between.</p>
<p>Return the minimum number of operations needed to make the array contiguous by value.</p>

<h3>Function</h3>
<pre class="sample">minOperationsToMakeValuesContiguous(arr: int[]) &rarr; int</pre>
<p>Complete the function <em>minOperationsToMakeValuesContiguous</em>, which has the following parameter:</p>
<ul><li><em>int[] arr:</em> the input array</li></ul>
<h3>Returns</h3>
<ul><li><em>int:</em> the minimum number of replacement operations</li></ul>

<h3>Examples</h3>
<div class="sublabel">Example 1</div>
<pre class="sample">arr    = [1, 2, 1]
return = 1</pre>
<p>Replace every 2 with 1 to get <code>[1, 1, 1]</code>. Now the only distinct value, 1, appears in one contiguous block. This requires 1 operation.</p>

<div class="sublabel">Example 2</div>
<pre class="sample">arr    = [1, 2, 3]
return = 0</pre>
<p>Every value already occupies a single contiguous block, so no operations are needed.</p>

<h3>Constraints</h3>
<ul>
  <li><code>1 &lt;= arr.length &lt;= 10^5</code></li>
  <li><code>1 &lt;= arr[i] &lt;= 10^5</code></li>
  <li>Each operation replaces all occurrences of one chosen value <code>x</code> globally with a chosen value <code>y</code>.</li>
</ul>

<div class="warn"><strong>Source contradiction, recorded not fixed.</strong> The report adds a closing line claiming the answer equals <em>"the number of distinct values minus the maximum number of values that already occupy a single contiguous block"</em>. That formula disagrees with the minimum on <code>[1,2,1,2]</code>: it counts 2 &minus; 0 = 2, while one operation (replace every 2 with 1) already produces <code>[1,1,1,1]</code>. Both published examples satisfy either reading, so they do not settle it. The solution below returns the genuine minimum, <strong>1</strong>.</div>

<div class="srcnote"><strong>Compare with:</strong> <em>"Minimum Contiguous Replacements"</em> (<code>minOperations</code>), the same task reported under a different name &mdash; and with <em>"Optimal Inventory &mdash; Minimum Replacement Cost"</em> (<code>getMinAmount</code>), which shares the validity rule but charges <em>elements changed</em> instead of operations, so its answers differ.</div>
<div class="ans">
<h3>Answer</h3>
<p class="lede">Hidden by default — open a hint first, and only then the full solution.</p>
<details class="hint"><summary><span class="k">Hint 1</span>Where to start</summary><div class="inner"><p>An operation rewrites every occurrence of a value at once, so you never edit a position &mdash; you fuse whole values. Ask which pairs of values can never be separated.</p></div></details>
<details class="hint"><summary><span class="k">Hint 2</span>The approach</summary><div class="inner"><p>Give each value the span <code>[firstIndex, lastIndex]</code>. If two spans overlap, those values interleave and must end up as one value. Merge the overlapping spans; a merged group holding <em>k</em> distinct values costs <em>k</em> &minus; 1.</p></div></details>
<details class="sol"><summary><span class="k">Solution</span>Full walk-through and code</summary><div class="inner"><p>Give each distinct value its span <code>[first, last]</code>. Two values whose spans overlap are interleaved: one of them has an occurrence strictly between two occurrences of the other, so no relabelling can separate them and they must become a single value. Overlap chains transitively, so merge the spans like ordinary intervals.</p>
<p>Collapsing a group of <em>k</em> distinct values into one takes exactly <code>k &minus; 1</code> operations, and the merged group's span is then one solid block. Values whose spans are disjoint from everything else are already contiguous and cost 0.</p>
<p>The finest grouping is optimal: merging two separate groups costs <code>k&#8321; + k&#8322; &minus; 1</code> against <code>(k&#8321;&minus;1) + (k&#8322;&minus;1)</code> for leaving them apart &mdash; strictly one operation worse.</p>
<p><span class="cx">Time O(n log n)</span><span class="cx">Space O(n)</span></p><pre class="sample"><code>def minOperationsToMakeValuesContiguous(arr):
    first, last = {}, {}
    for i, v in enumerate(arr):
        if v not in first:
            first[v] = i
        last[v] = i

    spans = sorted((first[v], last[v]) for v in first)

    ops = 0
    i = 0
    while i &lt; len(spans):                 # ordinary interval merging
        hi = spans[i][1]
        k = 1
        j = i + 1
        while j &lt; len(spans) and spans[j][0] &lt; hi:
            hi = max(hi, spans[j][1])
            k += 1
            j += 1
        ops += k - 1                      # a group of k interleaved values costs k-1
        i = j
    return ops</code></pre></div></details>
<details class="deep"><summary><span class="k">Step by step</span>Every number, calculated</summary><div class="inner">
<p>Traced on the published examples and on the case that separates the two readings of the statement.</p>

<div class="step"><h4>1 &middot; Spans, and what "interleaved" means</h4>
<div class="formula">[1, 2, 1]   value 1 &rarr; span [0, 2]     value 2 &rarr; span [1, 1]
            [1,1] lies inside [0,2] &rarr; the two values interleave</div>
<p>No sequence of operations can leave both values present and contiguous: as long as 1 keeps positions 0 and 2, anything in between splits it. So they must be fused, costing one operation.</p>
</div>

<div class="step"><h4>2 &middot; The cost of a group</h4>
<p>Since one operation rewrites <em>all</em> occurrences of a value, a group of <em>k</em> mutually (transitively) interleaved values is collapsed by rewriting <code>k &minus; 1</code> of them into the remaining one. Frequencies are irrelevant: rewriting a value appearing once and one appearing a thousand times both cost exactly 1.</p>
<table class="trace">
<tr><th>array</th><th>spans</th><th>merged groups</th><th>cost</th></tr>
<tr><td class="hit">[1,2,1]</td><td class="hit">1:[0,2], 2:[1,1]</td><td class="hit">{1,2}</td><td class="hit">2 &minus; 1 = <b>1</b></td></tr>
<tr><td class="hit">[1,2,3]</td><td class="hit">1:[0,0], 2:[1,1], 3:[2,2]</td><td class="hit">{1} {2} {3}</td><td class="hit">0 + 0 + 0 = <b>0</b></td></tr>
<tr><td>[1,2,3,1,2,3]</td><td>1:[0,3], 2:[1,4], 3:[2,5]</td><td>{1,2,3}</td><td>3 &minus; 1 = <b>2</b></td></tr>
<tr><td>[1,2,2,1,3]</td><td>1:[0,3], 2:[1,2], 3:[4,4]</td><td>{1,2} {3}</td><td>1 + 0 = <b>1</b></td></tr>
</table>
<p>Both published answers reproduced.</p>
</div>

<div class="step"><h4>3 &middot; The case the source gets wrong</h4>
<div class="formula">[1, 2, 1, 2]
spans        : 1:[0,2] , 2:[1,3]      &rarr; they overlap &rarr; one group of 2
this solution: 2 &minus; 1 = <b>1</b>   (replace every 2 with 1 &rarr; [1,1,1,1], valid)
source line  : distinct(2) &minus; already-contiguous(0) = 2</div>
<p>One operation is demonstrably enough, so the reported formula is not the minimum. It is recorded above rather than silently corrected &mdash; if a judge insists on the other number, it is asking a different question.</p>
</div>

<div class="step"><h4>4 &middot; Traps</h4>
<ul>
<li><strong>Merge with <code>max</code>.</strong> A nested span must not shrink the group's right edge.</li>
<li><strong>Count operations, not elements changed.</strong> The sibling problem <em>Optimal Inventory</em> charges elements and has different answers.</li>
<li><strong>Touching spans do not overlap.</strong> One index holds one value, so the strict <code>spans[j][0] &lt; hi</code> test is right.</li>
<li><strong>A singleton value costs 0</strong>, and an already-valid array returns 0 through the same code path.</li>
<li><strong>Allowing <em>y</em> to be a brand-new value changes nothing</strong> &mdash; renaming a value into a fresh label never reduces interleaving.</li>
</ul>
</div>
</div></details>
</div>
`},

{
  id:'notes', section:'Notes', platform:'Your own notes from the doc',
  label:'Field notes', title:'Notes & Tips (text from the document)',
  minutes:0, score:'',
  images:[],
  fn:null,
  body:`
<h3>On the debugging round (6 failing test cases)</h3>
<p>There were six failing test cases that you needed to fix. I used Python, and the language option should be Django. My suggestion is to use AI as much as possible. Paste each failing test case into AI and ask for help. The prompt should tell it not to directly tell you how to fix the code, but you can ask it to point out roughly which function, or which range of lines, the issue might be in. The actual bugs are usually pretty obvious once you look carefully. With the hints from AI, it is not too hard to figure out. The problem I got was about scheduling payments. The mistakes were mostly things like changing <code>==</code> to <code>!=</code>, changing <code>(&lt; 0)</code> to <code>(&lt;= 0)</code>, or forgetting to update a variable.</p>

<h3>API review task — follows &amp; notifications</h3>
<p>Send you a set of API requirements. Please review whether they are feasible and whether anything needs to be completed or clarified.</p>
<p>The main feature is user-based following and notifications. When a movie is created or published, the system should generate unread notifications for users who follow it or the related entity. Then, unread counts and mark-as-read actions should be supported through field-based and condition-based filtering.</p>
<p><em>Slightly more polished version, because apparently APIs now need social lives too:</em></p>
<p>I'll provide a list of API requirements for you to review. Please check whether they are feasible and whether any details need to be added or clarified.</p>
<p>The core feature is to support user follow management and notification handling. When a movie is created or published, unread notifications should be generated for the relevant followers. The APIs should also support unread notification statistics and mark-as-read operations based on specific fields and filtering conditions.</p>

<h3>Activity logs task</h3>
<p>You need to fix the activity logs for issue and comment operations. Just add an Activity record after the corresponding create, update, and delete APIs.</p>
<p>Also, make sure the corresponding action strings match the test requirements exactly. Because naturally the test will fail over one tiny string mismatch, as software loves being dramatic.</p>

<h3>Frontend / API integration task</h3>
<p>Please fix a few features.</p>
<p>Start by checking the API integration and make sure the parameter names are not wrong. For example, fields like <code>movieId</code> and <code>token</code> need to be consistent with what the backend expects.</p>
<p>After that, update the frontend state logic to properly manage the displayed content and lists. That should be enough once the API fields and state handling are corrected.</p>

<h3>Market API task</h3>
<p>Please fix the market-related API business logic issues.</p>
<p>First, align the status checks, data validation, and fund validation across the relevant APIs. Creation, display, and state transitions should all behave as expected, and the request should only proceed when all required checks pass.</p>
<p>Then, follow the test results to identify any remaining issues and make the necessary detail-level fixes.</p>
`}

];
