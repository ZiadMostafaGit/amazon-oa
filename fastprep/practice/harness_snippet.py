# Runs inside the sandbox: exec the editor's code, then evaluate the snippet
# against it. parsing.py has already been prepended, so ListNode/TreeNode and
# parse_value are in scope for ad-hoc calls.

def _main():
    import base64, io, json, sys, traceback
    from contextlib import redirect_stdout

    payload = json.loads(base64.b64decode(_PAYLOAD_B64))
    code, snippet, cap = payload["code"], payload["snippet"], payload["maxOutput"]

    def emit(obj):
        sys.stdout.write("\n#---RESULT:%s---\n" % _NONCE + json.dumps(obj))
        sys.stdout.flush()

    ns = {"ListNode": ListNode, "TreeNode": TreeNode, "parse_value": parse_value,
          "__name__": "__scratch__"}
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            exec(compile(code, "<solution>", "exec"), ns)
    except BaseException:
        return emit({"error": "your code raised while loading:\n" + traceback.format_exc(limit=6),
                     "printed": buf.getvalue()[:cap]})

    out = io.StringIO()
    try:
        with redirect_stdout(out):
            try:
                value = eval(compile(snippet, "<scratch>", "eval"), ns)
            except SyntaxError:
                exec(compile(snippet, "<scratch>", "exec"), ns)
                value = None
        emit({"printed": out.getvalue()[:cap],
              "value": "" if value is None else repr(to_jsonable(value))[:2000]})
    except BaseException as e:
        emit({"printed": out.getvalue()[:cap],
              "error": "%s: %s" % (type(e).__name__, e)})


_main()
