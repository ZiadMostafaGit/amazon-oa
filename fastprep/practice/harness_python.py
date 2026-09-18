# Runs inside the sandbox. `parsing.py` has already been prepended, so
# parse_value / compare_output / ListNode / TreeNode are in scope.
# Input arrives on stdin after a marker line; the result leaves on stdout
# after another one, so a user's prints can never be mistaken for the verdict.

def _main():
    import base64, io, json, sys, traceback
    from contextlib import redirect_stdout

    payload = json.loads(base64.b64decode(_PAYLOAD_B64))
    code, cases = payload["code"], payload["cases"]
    fname, cap = payload["function"], payload["maxOutput"]

    def emit(obj):
        sys.stdout.write("\n#---RESULT:%s---\n" % _NONCE + json.dumps(obj))
        sys.stdout.flush()

    # 1. load the user's module in a namespace that already knows the node types
    ns = {"ListNode": ListNode, "TreeNode": TreeNode, "__name__": "__solution__"}
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            exec(compile(code, "<solution>", "exec"), ns)
    except BaseException:
        return emit({"error": "your code raised while loading:\n" +
                              traceback.format_exc(limit=6),
                     "stdout": buf.getvalue()[:cap]})

    fn = ns.get(fname)
    if not callable(fn):
        defined = sorted(k for k, v in ns.items() if callable(v) and not k.startswith("_")
                         and k not in ("ListNode", "TreeNode"))
        return emit({"error": "no function named %s(...) is defined.%s" %
                              (fname, ("  Found: " + ", ".join(defined)) if defined else "")})

    # 2. run every visible case
    results = []
    for case in cases:
        entry = {"id": case.get("id")}
        try:
            args = [parse_value(i["rawValue"], i["type"]) for i in case["inputs"]]
        except Exception as e:                      # a bad example, not the user's fault
            entry.update(ok=False, error="could not parse this example's input: %s" % e)
            results.append(entry)
            continue

        out = io.StringIO()
        try:
            with redirect_stdout(out):
                got = fn(*args)
        except BaseException:
            entry.update(ok=False, error=traceback.format_exc(limit=6),
                         stdout=out.getvalue()[:cap])
            results.append(entry)
            continue

        try:
            ok, got_s, exp_s = compare_output(got, case["expectedRaw"], case["outputType"])
            entry.update(ok=ok, got=got_s, expected=exp_s, stdout=out.getvalue()[:cap])
        except Exception as e:
            entry.update(ok=False, error="could not compare the result: %s" % e,
                         stdout=out.getvalue()[:cap])
        results.append(entry)

    emit({"results": results})


_main()
