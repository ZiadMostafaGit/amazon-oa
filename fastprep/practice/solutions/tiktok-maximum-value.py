# Appending the suffix XOR from i makes the new total prefix XOR equal to the old prefix P[i], so the set of
# prefix XOR values never changes. Every value ever in the array is P[a] ^ P[b] for two prefixes, and every such
# pair (a subarray XOR) can be produced. So the answer is the maximum XOR of two prefix values: a bitwise trie.
from typing import List

BITS = 30


def maximumValue(arr: List[int]) -> int:
    trie = [[0, 0]]          # node -> [child for bit 0, child for bit 1]; 0 means absent (node 0 is the root)

    def insert(x):
        node = 0
        for b in range(BITS - 1, -1, -1):
            bit = (x >> b) & 1
            if trie[node][bit] == 0:
                trie.append([0, 0])
                trie[node][bit] = len(trie) - 1
            node = trie[node][bit]

    def best_with(x):
        node, res = 0, 0
        for b in range(BITS - 1, -1, -1):
            want = 1 - ((x >> b) & 1)
            if trie[node][want]:
                res |= 1 << b
                node = trie[node][want]
            else:
                node = trie[node][1 - want]
        return res

    best = 0
    prefix = 0
    insert(0)
    for v in arr:
        prefix ^= v
        best = max(best, best_with(prefix))
        insert(prefix)
    return best
