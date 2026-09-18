# Runs inside the sandbox: the user's code and the reference, on generated
# inputs, stopping at the first disagreement. parsing.py and gen.py have been
# prepended, so parse_value / to_jsonable / values_equal / gen are in scope.

def _main():
    import base64, copy, io, json, random, sys, time, traceback
    from contextlib import redirect_stdout

    payload = json.loads(base64.b64decode(_PAYLOAD_B64))
    user_code, ref_code = payload["code"], payload["reference"]
    fname, inputs = payload["function"], payload["inputs"]
    trials, budget, out_type = payload["trials"], payload["budget"], payload["outputType"]

    def emit(obj):
        sys.stdout.write("\n#---RESULT:%s---\n" % _NONCE + json.dumps(obj))
        sys.stdout.flush()

    def load(code, label):
        ns = {"ListNode": ListNode, "TreeNode": TreeNode, "__name__": "__" + label + "__"}
        with redirect_stdout(io.StringIO()):
            exec(compile(code, "<" + label + ">", "exec"), ns)
        fn = ns.get(fname)
        if not callable(fn):
            raise NameError("no function named %s in the %s" % (fname, label))
        return fn

    try:
        user = load(user_code, "solution")
    except BaseException:
        return emit({"error": "your code:\n" + traceback.format_exc(limit=4)})
    try:
        ref = load(ref_code, "reference")
    except BaseException:
        return emit({"error": "the stored reference failed to load: " +
                              traceback.format_exc(limit=2)})

    rng = random.Random(payload.get("seed") or 1234)
    stop = time.time() + budget
    checked = skipped = 0
    for _ in range(trials):
        if time.time() > stop:
            break
        raw = gen_args(inputs, rng)
        try:
            with redirect_stdout(io.StringIO()):
                expected = ref(*copy.deepcopy(raw))
        except BaseException:
            skipped += 1              # the reference rejects it: not a real input
            continue
        try:
            with redirect_stdout(io.StringIO()):
                got = user(*copy.deepcopy(raw))
        except BaseException:
            return emit({"checked": checked, "skipped": skipped, "failed": True, "crash": True,
                         "input": json.dumps(to_jsonable(raw))[:400],
                         "inputValues": [json.dumps(to_jsonable(v)) for v in raw],
                         "got": traceback.format_exc(limit=4)[-400:], "expected": ""})
        checked += 1
        if not values_equal(to_jsonable(got, out_type), to_jsonable(expected, out_type), out_type):
            return emit({"checked": checked, "skipped": skipped, "failed": True, "crash": False,
                         "input": json.dumps(to_jsonable(raw))[:400],
                         "inputValues": [json.dumps(to_jsonable(v)) for v in raw],
                         "got": format_value(to_jsonable(got, out_type), out_type)[:300],
                         "expected": format_value(to_jsonable(expected, out_type), out_type)[:300]})
    emit({"checked": checked, "skipped": skipped, "failed": False})


_main()
