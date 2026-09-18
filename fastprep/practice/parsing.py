"""Parse FastPrep example values, and compare a solution's output against them.

Every `inputText[].inputValue` and `examples[].outputText` in the bank is a
string. This module turns those strings into Python values according to the
declared `inputType` / `outputType`, serialises values back, and compares a
candidate answer with the expected one.

It is the part of the app most likely to be quietly wrong, so:
  * the type grammar below is derived from every type that actually occurs in
    the database (28 input types, 27 output types), not from guesswork;
  * `tests/test_parsing.py` unit-tests it, and `tests/test_corpus.py` runs it
    over all 3533 problems and fails if a single example does not round-trip.

Known shapes, all observed in the data:
  int 5 | long 10 | double 1.5 | float 3.89 | boolean true | char "J"
  String "hit"                           (outputs may be bare: b)
  int[] [16,17,4] | int[][] [[0,7]] | int[][][] [[[0,2]]]
  String[] ["a"] | String[][] [["v1","Maple"]] | char[][] [["1","0"]]
  List<Integer> [1,2] | List<List<String>> [["java"], ["python"]]
  TreeNode [3,9,20,null,null,15,7]       (level order, LeetCode encoding)
  ListNode [1,2,3] | ListNode[] [[1,4,5],[1,3,4]]
"""

from __future__ import annotations

import json
import math
import re

# --------------------------------------------------------------------------
# type grammar
# --------------------------------------------------------------------------
_LIST_RE = re.compile(r"^List<(.+)>$")
_ARRAY_RE = re.compile(r"^(.*)\[\]$")

INT_TYPES = {"int", "long", "Integer", "Long"}
REAL_TYPES = {"double", "float", "Double", "Float"}
BOOL_TYPES = {"boolean", "Boolean"}
CHAR_TYPES = {"char", "Character"}
STR_TYPES = {"String"}
NODE_TYPES = {"TreeNode", "ListNode", "ListNode[]"}   # ListNode[] is atomic: see element_type


class ParseError(ValueError):
    """Raised when a value cannot be read as its declared type."""


def element_type(t: str) -> str | None:
    """int[] -> int, List<String> -> String, int[][] -> int[]. None if scalar."""
    t = (t or "").strip()
    m = _LIST_RE.match(t)
    if m:
        return m.group(1).strip()
    m = _ARRAY_RE.match(t)
    if m and t not in ("ListNode[]",):
        return m.group(1).strip()
    return None


def base_type(t: str) -> str:
    """Strip every [] / List<> layer: int[][] -> int, List<List<String>> -> String."""
    seen = 0
    while True:
        e = element_type(t)
        if e is None or seen > 8:
            return (t or "").strip()
        t, seen = e, seen + 1


def depth(t: str) -> int:
    """Nesting depth: int -> 0, int[] -> 1, List<List<Integer>> -> 2."""
    n = 0
    while True:
        e = element_type(t)
        if e is None or n > 8:
            return n
        t, n = e, n + 1


# --------------------------------------------------------------------------
# linked lists and trees
# --------------------------------------------------------------------------
class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

    def __repr__(self):
        return "ListNode(%r)" % (encode_linked_list(self),)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

    def __repr__(self):
        return "TreeNode(%r)" % (encode_tree(self),)


def build_linked_list(values):
    head = tail = None
    for v in values or []:
        node = ListNode(v)
        if head is None:
            head = tail = node
        else:
            tail.next = node
            tail = node
    return head


def encode_linked_list(head):
    out, seen = [], set()
    while head is not None:
        if id(head) in seen:            # a cycle would otherwise hang the runner
            out.append("<cycle>")
            break
        seen.add(id(head))
        out.append(getattr(head, "val", None))
        head = getattr(head, "next", None)
    return out


def build_tree(values):
    """LeetCode level-order encoding: children of a present node consume the
    next two slots; `null` marks an absent node and contributes no children."""
    vals = list(values or [])
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals):
            v = vals[i]; i += 1
            if v is not None:
                node.left = TreeNode(v)
                queue.append(node.left)
        if i < len(vals):
            v = vals[i]; i += 1
            if v is not None:
                node.right = TreeNode(v)
                queue.append(node.right)
    return root


def encode_tree(root):
    """Inverse of build_tree, with trailing nulls trimmed so that the encoding
    of a rebuilt tree equals the encoding it came from."""
    if root is None:
        return []
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
            continue
        out.append(getattr(node, "val", None))
        queue.append(getattr(node, "left", None))
        queue.append(getattr(node, "right", None))
    while out and out[-1] is None:
        out.pop()
    return out


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------
# Java numeric literals leak into a few values: `9000606388L`, and in principle
# 1_000_000 or 2.5f. Only ever applied to a value whose declared base type is
# numeric, so a string like "2C 2D 3F" is never touched.
_NUM_SUFFIX_RE = re.compile(r"(?<=\d)[LlFfDd]\b")
_NUM_UNDERSCORE_RE = re.compile(r"(?<=\d)_(?=\d)")


def _json_loads(raw: str, typ: str):
    """json.loads with narrowly-scoped repairs for the dialects in this bank.

    The repairs are deliberately timid: a value that is already valid JSON is
    never rewritten, and the Python-literal repair only runs when the text
    contains no double-quoted string at all, so `["None"]` keeps its string.
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError as first:
        pass

    if base_type(typ) in (INT_TYPES | REAL_TYPES):
        repaired = _NUM_UNDERSCORE_RE.sub("", _NUM_SUFFIX_RE.sub("", raw))
        if repaired != raw:
            try:
                return json.loads(repaired)
            except json.JSONDecodeError:
                pass

    if '"' not in raw:                      # no string content to damage
        repaired = raw.replace("'", '"') if "'" in raw else raw
        repaired = re.sub(r"\bNone\b", "null", repaired)
        repaired = re.sub(r"\bTrue\b", "true", repaired)
        repaired = re.sub(r"\bFalse\b", "false", repaired)
        if repaired != raw:
            try:
                return json.loads(repaired)
            except json.JSONDecodeError:
                pass

    raise ParseError("%s is not valid JSON for type %s" % (raw[:60], typ))


def _coerce(value, typ: str):
    """Recursively force a decoded JSON value into its declared type."""
    t = (typ or "").strip()
    el = element_type(t)

    if el is not None:                                   # array / List<...>
        if value is None:
            return None
        if not isinstance(value, (list, tuple)):
            raise ParseError("expected a list for %s, got %r" % (t, value))
        return [_coerce(v, el) for v in value]

    if value is None:
        return None
    if t in INT_TYPES:
        if isinstance(value, bool):
            raise ParseError("expected %s, got boolean" % t)
        if isinstance(value, float):
            if not float(value).is_integer():
                raise ParseError("expected %s, got %r" % (t, value))
            return int(value)
        try:
            return int(value.strip()) if isinstance(value, str) else int(value)
        except (TypeError, ValueError):
            raise ParseError("expected %s, got %r" % (t, value))
    if t in REAL_TYPES:
        if isinstance(value, bool):
            raise ParseError("expected %s, got boolean" % t)
        try:
            return float(value)
        except (TypeError, ValueError):
            raise ParseError("expected %s, got %r" % (t, value))
    if t in BOOL_TYPES:
        if isinstance(value, bool):
            return value
        if isinstance(value, str) and value.strip().lower() in ("true", "false"):
            return value.strip().lower() == "true"
        raise ParseError("expected %s, got %r" % (t, value))
    if t in CHAR_TYPES or t in STR_TYPES:
        if isinstance(value, str):
            return value
        return json.dumps(value) if isinstance(value, (list, dict)) else str(value)
    return value                                          # unknown scalar: as-is


def parse_value(raw, typ: str):
    """Parse one inputValue/outputText string into a Python value.

    TreeNode / ListNode / ListNode[] become real node objects; everything else
    becomes ints, floats, bools, strings and (nested) lists.
    """
    t = (typ or "").strip()
    if raw is None:
        return None
    if not isinstance(raw, str):          # already decoded (tabular cases)
        return raw
    s = raw.strip()

    if t == "TreeNode":
        return build_tree(_coerce(_json_loads(s or "[]", t), "Integer[]"))
    if t == "ListNode":
        return build_linked_list(_coerce(_json_loads(s or "[]", t), "Integer[]"))
    if t == "ListNode[]":
        rows = _coerce(_json_loads(s or "[]", t), "Integer[][]")
        return [build_linked_list(r) for r in rows]

    if t in STR_TYPES or t in CHAR_TYPES:
        # Strings are normally quoted; some outputs (notably char) are bare.
        if s.startswith('"') and s.endswith('"') and len(s) >= 2:
            return _coerce(_json_loads(s, t), t)
        if element_type(t) is None:
            return s
    if t in BOOL_TYPES and s.lower() in ("true", "false"):
        return s.lower() == "true"
    if not s:
        return [] if element_type(t) is not None else None
    return _coerce(_json_loads(s, t), t)


def parse_inputs(example: dict) -> list:
    """The positional argument list for one example, in declared order."""
    out = []
    for item in example.get("inputText") or []:
        out.append(parse_value(item.get("inputValue"), item.get("inputType")))
    return out


# --------------------------------------------------------------------------
# serialising and comparing
# --------------------------------------------------------------------------
def to_jsonable(value, typ: str | None = None):
    """Python value -> JSON-safe value, so results can cross the wire."""
    if isinstance(value, ListNode):
        return encode_linked_list(value)
    if isinstance(value, TreeNode):
        return encode_tree(value)
    if isinstance(value, (list, tuple)):
        el = element_type(typ) if typ else None
        return [to_jsonable(v, el) for v in value]
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return str(value)
        return value
    if isinstance(value, (int, str, bool)) or value is None:
        return value
    if hasattr(value, "val") and hasattr(value, "next"):        # duck-typed node
        return encode_linked_list(value)
    if hasattr(value, "val") and hasattr(value, "left"):
        return encode_tree(value)
    return str(value)


def format_value(value, typ: str | None = None) -> str:
    """Compact display form, matching how the bank writes its examples."""
    v = to_jsonable(value, typ)
    if isinstance(v, str) and (typ in STR_TYPES or typ in CHAR_TYPES):
        return json.dumps(v)
    return json.dumps(v, ensure_ascii=False)


_TOL = 1e-6


def values_equal(got, expected, typ: str | None = None) -> bool:
    """Structural comparison. Numbers compare with a relative tolerance, so a
    float answer is not failed for its last binary digit; ints stay exact."""
    if isinstance(got, bool) or isinstance(expected, bool):
        return bool(got) == bool(expected) and isinstance(got, bool) == isinstance(expected, bool)
    if isinstance(expected, float) or isinstance(got, float):
        try:
            g, e = float(got), float(expected)
        except (TypeError, ValueError):
            return False
        if math.isnan(g) and math.isnan(e):
            return True
        return abs(g - e) <= max(_TOL, _TOL * abs(e))
    if isinstance(expected, (int,)) and isinstance(got, (int,)):
        return got == expected
    if isinstance(expected, str) or isinstance(got, str):
        if isinstance(got, str) and isinstance(expected, str):
            return got == expected
        return str(got) == str(expected)
    if isinstance(expected, (list, tuple)):
        if not isinstance(got, (list, tuple)) or len(got) != len(expected):
            return False
        el = element_type(typ) if typ else None
        return all(values_equal(g, e, el) for g, e in zip(got, expected))
    if expected is None or got is None:
        return expected is None and got is None
    return got == expected


def compare_output(got, expected_raw: str, out_type: str):
    """(ok, got_display, expected_display). `got` is whatever the user returned."""
    expected = parse_value(expected_raw, out_type)
    got_j = to_jsonable(got, out_type)
    exp_j = to_jsonable(expected, out_type)
    return (values_equal(got_j, exp_j, out_type),
            format_value(got_j, out_type),
            format_value(exp_j, out_type))
