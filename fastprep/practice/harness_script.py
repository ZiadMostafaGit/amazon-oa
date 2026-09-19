# Runs inside the sandbox: execute the editor's code the way `python file.py`
# would and report everything it printed. No cases, no function call - this is
# the one for `print` debugging.
#
# `__name__` is "__main__", so an `if __name__ == "__main__":` block runs here
# (under the test harness it deliberately does not). parsing.py has already
# been prepended, so ListNode/TreeNode and parse_value are in scope.

def _main():
    import base64, io, json, sys, traceback
    from contextlib import redirect_stderr, redirect_stdout

    payload = json.loads(base64.b64decode(_PAYLOAD_B64))
    code, cap = payload["code"], payload["maxOutput"]

    def emit(obj):
        sys.stdout.write("\n#---RESULT:%s---\n" % _NONCE + json.dumps(obj))
        sys.stdout.flush()

    given = {"ListNode": ListNode, "TreeNode": TreeNode, "parse_value": parse_value}
    ns = dict(given, __name__="__main__")
    out, err = io.StringIO(), io.StringIO()

    def defined():
        """What the run left behind, so the app can say 'you defined solve()
        but nothing called it' instead of just showing an empty box."""
        return sorted(k for k, v in ns.items()
                      if not k.startswith("_") and k not in given and callable(v))

    try:
        with redirect_stdout(out), redirect_stderr(err):
            exec(compile(code, "<your code>", "exec"), ns)
    except SystemExit as e:
        return emit({"printed": out.getvalue()[:cap], "stderr": err.getvalue()[:cap],
                     "exit": 0 if e.code is None else e.code, "defined": defined()})
    except BaseException as e:
        # drop this harness's own frame, so the traceback starts at the line
        # the reader actually wrote
        tb = e.__traceback__.tb_next if e.__traceback__ else None
        return emit({"printed": out.getvalue()[:cap], "stderr": err.getvalue()[:cap],
                     "error": "".join(traceback.format_exception(type(e), e, tb, limit=8)),
                     "defined": defined()})

    emit({"printed": out.getvalue()[:cap], "stderr": err.getvalue()[:cap],
          "defined": defined()})


_main()
