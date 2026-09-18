#!/usr/bin/env python3
"""Generate extra test cases for problems that have a verified solution.

1,103 of the 3,533 problems publish exactly one example, which is thin for
practice: one example catches a misunderstanding, not an off-by-one. Where a
reference solution exists AND has passed every visible example, this mutates
those examples - keeping their vocabulary and shape - runs the reference over
the variants, and stores the pairs.

    python3 tools/cases.py                 # every verified problem missing cases
    python3 tools/cases.py <id> [<id>...]  # just these
    python3 tools/cases.py --count 8       # how many per problem (default 6)
    python3 tools/cases.py --force         # regenerate even if cases exist

These expectations are the REFERENCE's behaviour, not a judge's. That is why
only verified references are used, why the file records which solution produced
them, and why the app labels them as generated wherever they appear.
"""
import json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fpdb, runner, solutions

OUT = os.path.join(HERE, "solutions", "cases")


def generate(bank, pid: str, count: int = 6, budget: float = 8.0):
    d = bank.detail(pid)
    if not d or d.get("practiceFormat") == "tabular":
        return None, "not an algorithm problem"
    sol = solutions.get(pid)
    if not sol or not sol.get("verified"):
        return None, "no verified reference"
    cases = bank.runnable_cases(d)
    if not cases or not cases[0]["inputs"]:
        return None, "no declared inputs"
    out_type = (d.get("examples") or [{}])[0].get("outputType") or "int"
    r = runner.run_generate(sol["code"], d.get("functionName") or "solve",
                            cases[0]["inputs"], out_type, count=count, budget=budget,
                            examples=[c["inputs"] for c in cases])
    if r.get("error"):
        return None, r["error"].strip().splitlines()[-1][:120]
    if not r.get("cases"):
        return None, "generated nothing (%d tries, %d rejected)" % (r.get("tried", 0),
                                                                    r.get("rejected", 0))
    return {"problemId": pid, "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "from": "reference solution, verified %s" % (sol.get("checkedAt") or "?"),
            "rejected": r.get("rejected", 0), "cases": r["cases"]}, None


def main(argv) -> int:
    count, force, jobs, ids = 6, False, 8, []
    i = 0
    while i < len(argv):
        if argv[i] == "--count":
            count = int(argv[i + 1]); i += 2
        elif argv[i] == "--jobs":
            jobs = int(argv[i + 1]); i += 2
        elif argv[i] == "--force":
            force = True; i += 1
        else:
            ids.append(argv[i]); i += 1

    bank = fpdb.Bank()
    os.makedirs(OUT, exist_ok=True)
    if not ids:
        index = solutions._index()
        ids = sorted(pid for pid, v in index.items() if v.get("ok"))

    local = threading.local()

    def bank_for_thread():
        if not hasattr(local, "bank"):
            local.bank = fpdb.Bank()       # sqlite connections are per-thread
        return local.bank

    made = skipped = failed = 0
    lock = threading.Lock()
    done = [0]

    def one(pid):
        nonlocal made, skipped, failed
        path = os.path.join(OUT, pid + ".json")
        if os.path.exists(path) and not force:
            with lock:
                skipped += 1
            return
        data, why = generate(bank_for_thread(), pid, count)
        with lock:
            if data:
                with open(path, "w") as f:
                    json.dump(data, f, indent=1)
                made += 1
            else:
                failed += 1
                if failed <= 15:
                    print("  -- %-52s %s" % (pid, why))
            done[0] += 1
            if done[0] % 100 == 0:
                print("  %d/%d (%d written, %d skipped, %d without)"
                      % (done[0], len(ids), made, skipped, failed))

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        list(pool.map(one, ids))
    print("\n%d written, %d already had cases, %d could not be generated" % (made, skipped, failed))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
