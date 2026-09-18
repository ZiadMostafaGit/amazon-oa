"""Which languages this machine can actually execute, and their starter code.

The bank ships Java starter code only (plus SQL/pandas for tabular problems).
Rather than pretend, the app probes the machine at startup and marks every
language either runnable or read-only, and the UI says which is which.

Python starter code is generated from `functionName` and the declared example
types, so the signature always matches what the runner will call.
"""

from __future__ import annotations

import shutil

import parsing

PY_HINT = {
    "int": "int", "long": "int", "Integer": "int", "Long": "int",
    "double": "float", "float": "float", "Double": "float", "Float": "float",
    "boolean": "bool", "Boolean": "bool",
    "String": "str", "char": "str", "Character": "str",
    "TreeNode": "Optional[TreeNode]", "ListNode": "Optional[ListNode]",
    "ListNode[]": "List[Optional[ListNode]]",
}


def py_type(t: str) -> str:
    t = (t or "").strip()
    if t in PY_HINT:
        return PY_HINT[t]
    el = parsing.element_type(t)
    if el is not None:
        return "List[%s]" % py_type(el)
    return "Any"


def python_starter(detail: dict) -> str:
    """A Python stub whose signature matches the first example's inputs."""
    fname = detail.get("functionName") or "solve"
    examples = detail.get("examples") or []
    params, ret = [], "Any"
    if examples:
        for item in examples[0].get("inputText") or []:
            params.append("%s: %s" % (item.get("inputName") or "arg",
                                      py_type(item.get("inputType"))))
        ret = py_type(examples[0].get("outputType"))
    sig = "def %s(%s) -> %s:" % (fname, ", ".join(params), ret)

    head = []
    body = " ".join(p for p in params)
    if "List[" in body or "List[" in ret:
        head.append("from typing import List, Optional, Any")
    elif "Optional[" in body or "Optional[" in ret or "Any" in (body + ret):
        head.append("from typing import Optional, Any")
    if "TreeNode" in body + ret:
        head += ["", "# TreeNode is provided by the runner:",
                 "#   class TreeNode: val, left, right"]
    if "ListNode" in body + ret:
        head += ["", "# ListNode is provided by the runner:",
                 "#   class ListNode: val, next"]
    lead = ("\n".join(head) + "\n\n\n") if head else ""
    return "%s%s\n    # write your code here\n    pass\n" % (lead, sig)


def catalogue(detail: dict) -> list[dict]:
    """Every language offered for this problem, with an honest `runnable` flag."""
    fmt = detail.get("practiceFormat")
    out = []
    if fmt == "tabular":
        tab = detail.get("tabular") or {}
        for lang in tab.get("languages") or []:
            lid = lang.get("id")
            starter = (lang.get("starterCode") or "").strip("\n")
            if lid in ("mysql", "postgresql"):
                out.append({
                    "id": lid,
                    "label": "MySQL" if lid == "mysql" else "PostgreSQL",
                    "mode": "sql", "runnable": True, "starter": starter,
                    "note": "Runs on SQLite, which is close but not identical to "
                            "%s. Dialect-only features (window frames, ILIKE, "
                            "date functions) may differ."
                            % ("MySQL" if lid == "mysql" else "PostgreSQL"),
                })
            elif lid == "pandas":
                out.append({
                    "id": "pandas", "label": "pandas", "mode": "python",
                    "runnable": _HAS_PANDAS, "starter": _dedent(starter),
                    "note": None if _HAS_PANDAS else
                            "pandas is not installed in this environment, so this "
                            "starter code is shown for reading only.",
                })
        # a dialect-neutral entry so there is always something runnable
        out.insert(0, {"id": "sqlite", "label": "SQL (SQLite)", "mode": "sql",
                       "runnable": True,
                       "starter": "-- Write your query below. It runs on SQLite.\n",
                       "note": "The visible cases are loaded into an in-memory "
                               "SQLite database built from the table schemas."})
        return out

    out.append({"id": "python", "label": "Python 3", "mode": "python",
                "runnable": True, "starter": python_starter(detail),
                "note": "Signature generated from this problem's example types; "
                        "the runner calls it with exactly these arguments."})
    if detail.get("starterCode"):
        out.append({"id": "java", "label": "Java", "mode": "java",
                    "runnable": _HAS_JAVA,
                    "starter": detail.get("starterCode"),
                    "note": None if _HAS_JAVA else
                            "No JDK on this machine, so the original Java starter "
                            "code is shown for reading only - switch to Python to run."})
    return out


def _dedent(code: str) -> str:
    lines = [l for l in (code or "").splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    pads = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    cut = min(pads) if pads else 0
    return "\n".join(l[cut:] if len(l) >= cut else l for l in lines)


def _probe_pandas() -> bool:
    try:
        import pandas  # noqa: F401
        return True
    except Exception:
        return False


_HAS_JAVA = bool(shutil.which("javac") and shutil.which("java"))
_HAS_PANDAS = _probe_pandas()


def environment() -> dict:
    import runner
    return {"sandbox": runner.sandbox_kind(), "java": _HAS_JAVA, "pandas": _HAS_PANDAS,
            "wallTimeout": runner.WALL_TIMEOUT, "cpuSeconds": runner.CPU_SECONDS,
            "memoryMB": runner.MEMORY_BYTES >> 20}
