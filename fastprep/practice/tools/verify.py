#!/usr/bin/env python3
"""Run a stored solution against its problem's visible examples, in the sandbox.

    python3 tools/verify.py <problem-id> [path]   # one problem
    python3 tools/verify.py --all                 # every stored solution
    python3 tools/verify.py --manifest            # coverage against MANIFEST.json

Exit code 0 only when every visible example passes. This is the gate for a
solution being kept: the bank has no hidden tests, so passing every visible
example is the strongest check available, and a solution that fails one is
worse than no solution at all.
"""
import glob, json, os, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fpdb, runner

SOLUTIONS = os.path.join(HERE, "solutions")


def solution_path(pid: str, fmt: str = "algorithm") -> str:
    return os.path.join(SOLUTIONS, pid + (".sql" if fmt == "tabular" else ".py"))


def verify(bank: fpdb.Bank, pid: str, path: str | None = None, quiet: bool = False):
    d = bank.detail(pid)
    if not d:
        return False, "no such problem"
    fmt = d.get("practiceFormat")
    path = path or solution_path(pid, fmt)
    if not os.path.exists(path):
        return False, "no solution file (%s)" % os.path.relpath(path, HERE)
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    if not code.strip():
        return False, "solution file is empty"

    if fmt == "tabular":
        res = runner.run_sql(code, d.get("tabular") or {})
    else:
        cases = bank.runnable_cases(d)
        if not cases:
            return False, "problem has no visible examples"
        res = runner.run_python(code, cases, d.get("functionName") or "solve")

    if res.get("error") and not res.get("results"):
        return False, res["error"].strip().splitlines()[-1][:160]
    results = res.get("results") or []
    passed = sum(1 for r in results if r.get("ok"))
    if passed == len(results) and results:
        return True, "%d/%d" % (passed, len(results))
    first = next((r for r in results if not r.get("ok")), {})
    detail = first.get("error") or ("got %s, expected %s" % (first.get("got"), first.get("expected")))
    return False, "%d/%d — case %s: %s" % (passed, len(results), first.get("id"),
                                           str(detail).replace("\n", " ")[:160])


_local = __import__("threading").local()


def sqlite_bank():
    """One read-only connection per thread: sqlite3 objects are not shareable."""
    if not hasattr(_local, "bank"):
        _local.bank = fpdb.Bank()
    return _local.bank


def main(argv) -> int:
    bank = fpdb.Bank()
    if argv and argv[0] == "--manifest":
        man = json.load(open(os.path.join(SOLUTIONS, "MANIFEST.json")))
        have = miss = bad = 0
        broken = []
        for p in man["problems"]:
            path = solution_path(p["id"], p["format"])
            if not os.path.exists(path):
                miss += 1
                continue
            ok, msg = verify(bank, p["id"], path)
            if ok:
                have += 1
            else:
                bad += 1
                broken.append((p["id"], msg))
        print("manifest %d: %d verified, %d failing, %d missing"
              % (man["count"], have, bad, miss))
        for pid, msg in broken[:40]:
            print("  FAIL %-50s %s" % (pid, msg))
        return 0 if not bad else 1

    if argv and argv[0] == "--all":
        files = sorted(glob.glob(os.path.join(SOLUTIONS, "*.py")) +
                       glob.glob(os.path.join(SOLUTIONS, "*.sql")))
        ok_n = bad_n = 0
        index = {}
        stamp = __import__("time").strftime("%Y-%m-%dT%H:%M:%S")
        quiet = "--quiet" in argv[1:]
        jobs = 8
        if "--jobs" in argv:
            jobs = int(argv[argv.index("--jobs") + 1])

        def one(path):
            pid = os.path.splitext(os.path.basename(path))[0]
            # each verify spawns its own sandbox, so threads here are fine
            return (pid, path) + verify(sqlite_bank(), pid, path)

        with ThreadPoolExecutor(max_workers=jobs) as pool:
            for pid, path, ok, msg in pool.map(one, files):
                if not (quiet and ok):
                    print("%-5s %-52s %s" % ("ok" if ok else "FAIL", pid, msg))
                index[pid] = {"ok": bool(ok), "cases": msg if ok else None,
                              "note": None if ok else msg, "checkedAt": stamp}
                ok_n += ok
                bad_n += not ok
        # the app reads this to decide whether it may offer a solution at all
        with open(os.path.join(SOLUTIONS, "VERIFIED.json"), "w") as f:
            json.dump({"checkedAt": stamp, "verified": ok_n, "failing": bad_n,
                       "problems": index}, f, indent=1, sort_keys=True)
        print("\n%d verified, %d failing -> solutions/VERIFIED.json" % (ok_n, bad_n))
        return 0 if not bad_n else 1

    if not argv:
        print(__doc__)
        return 2
    pid = argv[0]
    ok, msg = verify(bank, pid, argv[1] if len(argv) > 1 else None)
    print("%-5s %s  %s" % ("ok" if ok else "FAIL", pid, msg))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
