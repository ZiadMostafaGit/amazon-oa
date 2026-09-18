# Runs inside the sandbox: generate inputs from the declared types, run the
# reference over them, and hand back the pairs that survived. parsing.py and
# gen.py are prepended, so parse_value / to_jsonable / args_for are in scope.

def _main():
    import base64, copy, io, json, random, sys, time, traceback
    from contextlib import redirect_stdout

    payload = json.loads(base64.b64decode(_PAYLOAD_B64))
    ref_code, fname = payload["reference"], payload["function"]
    inputs, out_type = payload["inputs"], payload["outputType"]
    want, budget = payload["count"], payload["budget"]

    def emit(obj):
        sys.stdout.write("\n#---RESULT:%s---\n" % _NONCE + json.dumps(obj))
        sys.stdout.flush()

    ns = {"ListNode": ListNode, "TreeNode": TreeNode, "__name__": "__reference__"}
    try:
        with redirect_stdout(io.StringIO()):
            exec(compile(ref_code, "<reference>", "exec"), ns)
        ref = ns.get(fname)
        if not callable(ref):
            raise NameError("no function named %s" % fname)
    except BaseException:
        return emit({"error": traceback.format_exc(limit=3)})

    # the parsed example inputs, to mutate rather than invent from nothing
    seeds = []
    for ex in payload.get("examples") or []:
        try:
            seeds.append([parse_value(i["rawValue"], i["type"]) for i in ex])
        except Exception:
            pass

    seed_keys = {json.dumps(to_jsonable(s), sort_keys=True) for s in seeds}

    rng = random.Random(payload.get("seed") or 99)
    stop = time.time() + budget
    out, seen, rejected = [], set(), 0
    tries = 0
    while len(out) < want and tries < want * 25 and time.time() < stop:
        tries += 1
        size = 3 + (tries % 5)                       # a spread of shapes, all small
        # mostly mutate a real example (keeps the problem's vocabulary and
        # structure); occasionally generate from the types alone, for variety
        if seeds and rng.random() < 0.75:
            raw = variant_of(rng.choice(seeds), rng)
        else:
            raw = args_for(inputs, rng, size)
        key = json.dumps(to_jsonable(raw), sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        if key in seed_keys:            # identical to a published example: no news
            continue
        try:
            with redirect_stdout(io.StringIO()):
                value = ref(*copy.deepcopy(raw))
        except BaseException:
            rejected += 1                            # not a valid input for this problem
            continue
        try:
            expected = format_value(to_jsonable(value, out_type), out_type)
            values = [format_value(to_jsonable(v), inputs[i].get("type"))
                      for i, v in enumerate(raw)]
        except BaseException:
            rejected += 1
            continue
        if len(expected) > 400 or any(len(v) > 400 for v in values):
            continue                                 # unreadable in a test-case list
        out.append({"inputs": [{"name": inputs[i].get("name"),
                                "type": inputs[i].get("type"),
                                "rawValue": values[i]} for i in range(len(inputs))],
                    "expectedRaw": expected})

    emit({"cases": out, "rejected": rejected, "tried": tries})


_main()
