# Recursive ID3-style decision tree: entropy/information-gain split search over observed thresholds.
import math
from typing import List, Optional, Any


def _entropy(labels: List[int]) -> float:
    n = len(labels)
    if n == 0:
        return 0.0
    counts = {}
    for y in labels:
        counts[y] = counts.get(y, 0) + 1
    e = 0.0
    for c in counts.values():
        p = c / n
        e -= p * math.log2(p)
    return e


def _majority(labels: List[int]) -> int:
    counts = {}
    for y in labels:
        counts[y] = counts.get(y, 0) + 1
    best = None
    best_c = -1
    for lab in sorted(counts):
        if counts[lab] > best_c:
            best_c = counts[lab]
            best = lab
    return best


def _build(rows: List[List[float]], labels: List[int]):
    n = len(rows)
    if n == 0:
        return ('leaf', 0)
    parent_e = _entropy(labels)
    if parent_e == 0.0:
        return ('leaf', labels[0])

    nfeat = len(rows[0])
    best_gain = 0.0
    best_feat = -1
    best_thr = None
    for f in range(nfeat):
        vals = sorted(set(r[f] for r in rows))
        if len(vals) < 2:
            continue
        # every non-maximum observed value is a candidate threshold
        for thr in vals[:-1]:
            left_labels = []
            right_labels = []
            for i in range(n):
                if rows[i][f] <= thr:
                    left_labels.append(labels[i])
                else:
                    right_labels.append(labels[i])
            l, r = len(left_labels), len(right_labels)
            if l == 0 or r == 0:
                continue
            gain = parent_e - (l / n * _entropy(left_labels) + r / n * _entropy(right_labels))
            if gain > best_gain + 1e-12:
                best_gain = gain
                best_feat = f
                best_thr = thr

    if best_feat < 0 or best_gain <= 0:
        return ('leaf', _majority(labels))

    lr, ll, rr, rl = [], [], [], []
    for i in range(n):
        if rows[i][best_feat] <= best_thr:
            lr.append(rows[i])
            ll.append(labels[i])
        else:
            rr.append(rows[i])
            rl.append(labels[i])
    return ('node', best_feat, best_thr, _build(lr, ll), _build(rr, rl))


def _predict(tree, row: List[float]) -> int:
    while tree[0] != 'leaf':
        _, f, thr, left, right = tree
        tree = left if row[f] <= thr else right
    return tree[1]


def decisionTreePredictions(xTrain: List[List[float]], yTrain: List[int], xTest: List[List[float]]) -> List[int]:
    tree = _build(list(xTrain), list(yTrain))
    return [_predict(tree, row) for row in xTest]
