"""Run untrusted user code against a problem's visible examples.

Threat model: the code in the editor is hostile. It never runs in the server
process, never touches the problem database, and never reaches the network.

Isolation, strongest available first:
  1. bubblewrap (`bwrap`): a new user/pid/net/ipc/uts namespace, no network
     interface at all, the filesystem reduced to a read-only /usr (+ /lib,
     /etc/ssl for nothing in particular) and a private tmpfs. The payload is
     fed on stdin, so the child sees no path into the host.
  2. bubblewrap sharing the host's network: everything above except the
     network namespace. Some machines - a container without CAP_NET_ADMIN, a
     hardened kernel, a locked-down systemd unit - let bwrap make every other
     namespace but refuse to let the sandbox bring up its own loopback:
         bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
     There, a full sandbox is not a stricter option, it is a broken one: every
     run dies before your code starts. So we keep the rest and say plainly
     that the network is not sealed off.
  3. plain subprocess: same resource limits and timeout, but only the OS user
     separates it from your files. The app says so in the UI and the README;
     it is a fallback for machines without bwrap, not an equivalent.

Which of the three is in force is decided by RUNNING bwrap once and looking,
not by `which bwrap`: whether the binary exists says nothing about whether
this kernel, container or unit will let it do its job.

In both cases the child gets RLIMIT_CPU, RLIMIT_AS, RLIMIT_NOFILE,
RLIMIT_NPROC and RLIMIT_FSIZE, a wall-clock timeout enforced by the parent,
and its output is capped. The child is killed by process group on timeout.
"""

from __future__ import annotations

import base64
import json
import os
import re
import resource
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

# --- limits ---------------------------------------------------------------
WALL_TIMEOUT = 10          # seconds, parent-enforced
CPU_SECONDS = 8            # RLIMIT_CPU, child-enforced
MEMORY_BYTES = 768 << 20   # RLIMIT_AS
MAX_OUTPUT = 64_000        # bytes of stdout kept per run
MAX_CODE = 200_000         # characters of user code accepted

BWRAP = shutil.which("bwrap")

# Namespace flags, strongest first. `--share-net` is bwrap's own escape hatch
# for "--unshare-all, but not the network", which is exactly the machine that
# cannot set up a loopback inside a fresh net namespace.
_TIERS = [("bubblewrap", []), ("bubblewrap-shared-net", ["--share-net"])]
_SANDBOX = None          # ("bubblewrap" | "bubblewrap-shared-net" | "subprocess", [flags])


def _works(flags: list) -> bool:
    """Can bwrap actually start a sandbox here, with these flags?"""
    python = sys.executable or "python3"
    argv = _bwrap_argv(python, flags)[:-1] + ["-c", "pass"]
    try:
        p = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return False
    return p.returncode == 0


def _sandbox() -> tuple:
    """The best tier that works on this machine, worked out once and kept."""
    global _SANDBOX
    if _SANDBOX is None:
        _SANDBOX = ("subprocess", [])
        if BWRAP:
            for kind, flags in _TIERS:
                if _works(flags):
                    _SANDBOX = (kind, flags)
                    break
    return _SANDBOX


def demote_sandbox() -> str:
    """Forget what we decided and work it out again.

    A sandbox can stop working while the app is up - a container is reconfigured,
    a namespace limit is reached - and the first run to hit it should not be the
    only one that ever tells you.
    """
    global _SANDBOX
    _SANDBOX = None
    return sandbox_kind()


def sandbox_kind() -> str:
    return _sandbox()[0]


def sandbox_note() -> str:
    """One sentence for the banner, the badge and the README."""
    kind = sandbox_kind()
    if kind == "bubblewrap":
        return ("bubblewrap: new user/pid/net/ipc namespaces, no network interface, "
                "read-only /usr, private tmpfs")
    if kind == "bubblewrap-shared-net":
        return ("bubblewrap, but this machine will not let the sandbox create its own "
                "network namespace, so your code SHARES this host's network. Everything "
                "else - filesystem, pids, ipc - is still isolated")
    return ("no bubblewrap here, so only resource limits and a timeout separate your "
            "code from your files")


# The limits are applied by the child itself, not by preexec_fn on the parent
# side: bwrap has to clone new namespaces before it execs anything, and an
# RLIMIT_NPROC inherited from the parent makes that clone fail with EAGAIN.
# Soft and hard are set to the same value, so the user's code cannot raise them
# back (an unprivileged process may only lower a hard limit).
LIMIT_PREAMBLE = """import resource as _r, sys as _s
for _lim, _val in ((_r.RLIMIT_CPU, %(cpu)d), (_r.RLIMIT_AS, %(mem)d),
                   (_r.RLIMIT_NOFILE, 256), (_r.RLIMIT_FSIZE, %(fsize)d),
                   (_r.RLIMIT_CORE, 0), (getattr(_r, 'RLIMIT_NPROC', None), 256)):
    if _lim is None:
        continue
    try:
        _r.setrlimit(_lim, (_val, _val))
    except (ValueError, OSError):
        pass
_s.setrecursionlimit(20000)
del _r, _lim, _val
""" % {"cpu": CPU_SECONDS, "mem": MEMORY_BYTES, "fsize": 16 << 20}


def _preexec(limit_here: bool):
    """Runs in the forked child, before exec."""
    def fn():
        os.setsid()                  # own process group: the parent kills it whole
        if limit_here:               # only safe when we exec python directly
            resource.setrlimit(resource.RLIMIT_CPU, (CPU_SECONDS, CPU_SECONDS))
            resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))
            resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
            resource.setrlimit(resource.RLIMIT_FSIZE, (16 << 20, 16 << 20))
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    return fn


def _bwrap_argv(python: str, flags: list | None = None) -> list[str]:
    argv = [BWRAP,
            "--unshare-all",          # no network, pid, ipc, uts, cgroup, user
            ] + list(flags or []) + [
            "--die-with-parent",
            "--new-session",          # no terminal to inject into
            "--clearenv",
            "--setenv", "PATH", "/usr/bin",
            "--setenv", "HOME", "/tmp",
            "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
            "--setenv", "PYTHONHASHSEED", "0",
            "--proc", "/proc",
            "--dev", "/dev",
            "--tmpfs", "/tmp",
            "--chdir", "/tmp"]
    for path in ("/usr", "/lib", "/lib64", "/bin", "/sbin", "/etc/alternatives"):
        if os.path.exists(path):
            argv += ["--ro-bind", path, path]
    return argv + [python, "-I", "-S", "-"]


_FUTURE_RE = re.compile(r"^from __future__ import .*$", re.M)


def _assemble(source: str, payload: dict, nonce: str) -> str:
    """Build the one program the sandbox runs.

    The payload (user code + cases) travels as a base64 literal inside the
    source rather than on stdin: `python -` reads stdin to EOF as the program
    itself, so nothing is left for the program to read. base64 also means no
    quoting or escaping question, whatever the user typed.

    `from __future__` imports must stay on the very first lines, so any that
    the embedded modules carry are hoisted.
    """
    futures = _FUTURE_RE.findall(source)
    body = _FUTURE_RE.sub("", source)
    blob = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")
    return "".join([
        "\n".join(futures), "\n",
        LIMIT_PREAMBLE,
        "_PAYLOAD_B64 = '", blob, "'\n",
        "_NONCE = '", nonce, "'\n",
        body,
    ])


# bwrap prints its own failures on stderr and exits before the program it was
# asked to run ever starts. Those have nothing to do with the code in the
# editor, and must never be reported as if they did.
_BWRAP_FAILED = re.compile(r"^bwrap:", re.M)


def _run_child(source: str, payload: dict, _retry: bool = True) -> dict:
    """Execute `source` over `payload` inside the sandbox. Returns its JSON."""
    kind, flags = _sandbox()
    nonce = secrets.token_hex(8)
    python = sys.executable or "python3"
    argv = _bwrap_argv(python, flags) if kind.startswith("bubblewrap") \
        else [python, "-I", "-S", "-"]
    program = _assemble(source, payload, nonce)

    try:
        proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            preexec_fn=_preexec(limit_here=not BWRAP), close_fds=True,
            cwd=tempfile.gettempdir(),
            env={"PATH": "/usr/bin", "HOME": "/tmp", "PYTHONDONTWRITEBYTECODE": "1"})
    except OSError as e:
        return {"error": "could not start the sandbox: %s" % e}

    try:
        out, err = proc.communicate(program.encode(), timeout=WALL_TIMEOUT)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            proc.kill()
        proc.communicate()
        return {"timeout": True,
                "error": "took longer than %d s and was killed" % WALL_TIMEOUT}

    text = out.decode("utf-8", "replace")
    tag = "\n#---RESULT:%s---\n" % nonce
    marker = text.rfind(tag)
    if marker >= 0:
        try:
            return json.loads(text[marker + len(tag):])
        except json.JSONDecodeError as e:
            return {"error": "malformed result from the sandbox: %s" % e}

    # No verdict: the child died. Say why, in the user's terms.
    rc = proc.returncode or 0
    stderr_text = err.decode("utf-8", "replace")

    # The sandbox itself never started. Work out what this machine will allow
    # and run it again - once - so one bad tier does not break every run until
    # someone restarts the server.
    if _BWRAP_FAILED.search(stderr_text):
        if _retry:
            demote_sandbox()
            if sandbox_kind() != kind:
                return _run_child(source, payload, _retry=False)
        return {"sandboxError": True,
                "error": "Your code never ran: this machine would not let the "
                         "sandbox start.\n\n" + stderr_text.strip()[-2000:]}

    sig = -rc if rc < 0 else (rc - 128 if rc > 128 else 0)
    detail = stderr_text[-2000:].strip()
    if sig == signal.SIGXCPU:
        return {"timeout": True,
                "error": "your code used more than %d s of CPU and was stopped" % CPU_SECONDS}
    if sig == signal.SIGKILL:
        return {"timeout": True,
                "error": "your code was killed - it hit the %d s CPU limit, the %d MB memory "
                         "limit, or killed its own process" % (CPU_SECONDS, MEMORY_BYTES >> 20)}
    if sig:
        return {"error": "the sandbox stopped your code with signal %d%s"
                         % (sig, ("\n" + detail) if detail else "")}
    return {"error": detail or "your code exited without returning a result "
                               "(did it call sys.exit()?)"}


# --------------------------------------------------------------------------
# the harnesses that run inside the sandbox
# --------------------------------------------------------------------------
def _harness(kind: str) -> str:
    with open(os.path.join(HERE, "harness_%s.py" % kind), "r", encoding="utf-8") as f:
        return f.read()


def run_python(code: str, cases: list, function_name: str) -> dict:
    """cases: [{id, inputs:[{name,type,rawValue}], outputType, expectedRaw}]"""
    if len(code) > MAX_CODE:
        return {"error": "the editor holds more than %d characters" % MAX_CODE}
    parsing_src = open(os.path.join(HERE, "parsing.py"), "r", encoding="utf-8").read()
    payload = {"code": code, "cases": cases, "function": function_name,
               "maxOutput": MAX_OUTPUT}
    return _run_child(parsing_src + "\n\n" + _harness("python"), payload)


def run_diff(code: str, reference: str, function: str, inputs: list,
             out_type: str, trials: int = 300, budget: float = 6.0, seed: int = 1234) -> dict:
    """Fuzz the user's code against a stored reference on generated inputs.

    Only useful where a verified reference exists, which is the whole point of
    the solution store: without one there is nothing to disagree with.
    """
    if len(code) > MAX_CODE:
        return {"error": "the editor holds more than %d characters" % MAX_CODE}
    with open(os.path.join(HERE, "parsing.py"), "r", encoding="utf-8") as f:
        parsing_src = f.read()
    with open(os.path.join(HERE, "gen.py"), "r", encoding="utf-8") as f:
        gen_src = f.read()
    # The sandbox runs ONE flat program, so gen.py's `import parsing` has no
    # module to find: drop it and unqualify the references it guards.
    gen_src = gen_src.replace("import parsing\n", "").replace("parsing.", "")
    src = [parsing_src, gen_src]
    glue = "\ndef gen_args(inputs, rng):\n    return args_for(inputs, rng)\n"
    payload = {"code": code, "reference": reference, "function": function,
               "inputs": inputs, "outputType": out_type, "trials": trials,
               "budget": budget, "seed": seed, "maxOutput": MAX_OUTPUT}
    return _run_child("\n\n".join(src) + glue + _harness("diff"), payload)


def run_generate(reference: str, function: str, inputs: list, out_type: str,
                 count: int = 6, budget: float = 6.0, seed: int = 99,
                 examples: list | None = None) -> dict:
    """Generate extra test cases by running a verified reference over random
    inputs. The expected values are that reference's behaviour - which is why
    only verified references are ever used, and why the app labels them."""
    with open(os.path.join(HERE, "parsing.py"), "r", encoding="utf-8") as f:
        parsing_src = f.read()
    with open(os.path.join(HERE, "gen.py"), "r", encoding="utf-8") as f:
        gen_src = f.read().replace("import parsing\n", "").replace("parsing.", "")
    payload = {"reference": reference, "function": function, "inputs": inputs,
               "outputType": out_type, "count": count, "budget": budget, "seed": seed,
               "examples": examples or [], "maxOutput": MAX_OUTPUT}
    return _run_child(parsing_src + "\n\n" + gen_src + "\n\n" + _harness("gen"), payload)


def run_script(code: str) -> dict:
    """Run the editor's code as a program and report what it printed.

    The plain `python file.py` of this app: no cases, no function call, no
    expression to type - it exists so a `print` put in to check a loop can
    actually be read.
    """
    if len(code) > MAX_CODE:
        return {"error": "the editor holds more than %d characters" % MAX_CODE}
    parsing_src = open(os.path.join(HERE, "parsing.py"), "r", encoding="utf-8").read()
    payload = {"code": code, "maxOutput": MAX_OUTPUT}
    return _run_child(parsing_src + "\n\n" + _harness("script"), payload)


def run_snippet(code: str, snippet: str) -> dict:
    """Load the editor's code, then evaluate one expression or statement against
    it - the scratch pad. Same sandbox, same limits."""
    if len(code) + len(snippet) > MAX_CODE:
        return {"error": "the editor holds more than %d characters" % MAX_CODE}
    parsing_src = open(os.path.join(HERE, "parsing.py"), "r", encoding="utf-8").read()
    payload = {"code": code, "snippet": snippet, "maxOutput": MAX_OUTPUT}
    return _run_child(parsing_src + "\n\n" + _harness("snippet"), payload)


def run_sql(query: str, tabular: dict) -> dict:
    """Run one SQL statement per visible case against an in-memory SQLite db."""
    if len(query) > MAX_CODE:
        return {"error": "the editor holds more than %d characters" % MAX_CODE}
    payload = {"query": query, "tabular": tabular, "maxOutput": MAX_OUTPUT}
    return _run_child(_harness("sql"), payload)
