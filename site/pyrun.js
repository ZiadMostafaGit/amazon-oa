/* pyrun.js — the Python execution layer.
 *
 * Owns the Pyodide lifecycle and every Python harness; knows nothing about the
 * DOM. app.js drives it and renders what comes back. Everything runs in this
 * page: there is no server, and no code leaves the browser.
 */
window.PyRun = (function () {
  const URL_BASE = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';
  let py = null, loading = null;

  /* Shared Python side. Every entry point runs the user's code in a fresh
     namespace, deep-copies inputs so a mutating solution cannot poison later
     cases, and runs under a settrace deadline so `while True` cannot wedge the
     tab. Only pure-Python loops are interruptible that way — a hang inside a C
     builtin is not, which is inherent to running on the main thread. */
  const PY = String.raw`
import json, copy, sys, time, traceback, io, random
from contextlib import redirect_stdout

def _norm(v):
    if isinstance(v, (list, tuple)): return [_norm(x) for x in v]
    return v

def _load(code, fname):
    ns = {}
    exec(code, ns)
    fn = ns.get(fname)
    if not callable(fn):
        raise NameError('No function named %s(...) is defined.' % fname)
    return fn, ns

class _Deadline:
    """settrace-based wall-clock guard, armed per call."""
    def __init__(self, limit):
        self.limit = limit
    def __enter__(self):
        end = time.time() + self.limit
        n = [0]
        def guard(frame, event, arg):
            n[0] += 1
            if n[0] % 2000 == 0 and time.time() > end:
                raise TimeoutError('time limit exceeded (%gs)' % self.limit)
            return guard
        sys.settrace(guard)
        return self
    def __exit__(self, *a):
        sys.settrace(None)
        return False

def _call(fn, args, limit):
    """-> (ok, value, printed, error)"""
    buf = io.StringIO()
    try:
        with _Deadline(limit), redirect_stdout(buf):
            v = fn(*copy.deepcopy(args))
        return True, v, buf.getvalue(), None
    except Exception as e:
        return False, None, buf.getvalue(), '%s: %s' % (type(e).__name__, e)

# ---- fixed published cases -------------------------------------------------
def _run(user_code, fname, cases_json, limit):
    try:
        fn, _ = _load(user_code, fname)
    except Exception as e:
        tb = traceback.format_exc(limit=2) if not isinstance(e, NameError) else str(e)
        return json.dumps({'error': tb})
    out = []
    for c in json.loads(cases_json):
        ok, v, printed, err = _call(fn, c['in'], limit)
        out.append({'ok': bool(ok and _norm(v) == _norm(c['out'])),
                    'got': (repr(v) if ok else err)[:300],
                    'printed': printed[:600]})
    return json.dumps({'results': out})

# ---- randomised differential testing against the reference -----------------
def _diff(user_code, ref_code, gen_code, fname, trials, max_n, limit, budget):
    try:
        fn, _ = _load(user_code, fname)
    except Exception as e:
        tb = traceback.format_exc(limit=2) if not isinstance(e, NameError) else str(e)
        return json.dumps({'error': tb})
    try:
        ref, _ = _load(ref_code, fname)
    except Exception as e:
        return json.dumps({'error': 'reference solution failed to load: %s' % e})
    g = {}
    exec(gen_code, g)
    gen = g['gen']
    rng = random.Random()
    stop = time.time() + budget
    checked = 0
    for _ in range(trials):
        if time.time() > stop:
            break
        args = gen(rng, rng.randint(1, max_n))
        ok, got, printed, err = _call(fn, args, limit)
        if not ok:
            return json.dumps({'checked': checked, 'failed': True, 'crash': True,
                               'input': repr(args)[:400], 'got': err, 'expected': ''})
        rok, exp, _p, _e = _call(ref, args, limit * 4)
        if not rok:
            continue                      # reference cannot handle it; not the user's problem
        checked += 1
        if _norm(got) != _norm(exp):
            return json.dumps({'checked': checked, 'failed': True, 'crash': False,
                               'input': repr(args)[:400],
                               'got': repr(got)[:200], 'expected': repr(exp)[:200]})
    return json.dumps({'checked': checked, 'failed': False})

# ---- empirical complexity probe -------------------------------------------
def _complexity(user_code, gen_code, fname, sizes, limit):
    try:
        fn, _ = _load(user_code, fname)
    except Exception as e:
        tb = traceback.format_exc(limit=2) if not isinstance(e, NameError) else str(e)
        return json.dumps({'error': tb})
    g = {}
    exec(gen_code, g)
    gen = g['gen']
    rng = random.Random(12345)
    rows = []
    for n in sizes:
        args = gen(rng, n)
        size = 0
        for a in args:
            try: size = max(size, len(a))
            except TypeError: size = max(size, 1)
        t0 = time.time()
        ok, v, _p, err = _call(fn, args, limit)
        dt = time.time() - t0
        rows.append({'n': n, 'size': size, 'ms': round(dt * 1000, 1), 'ok': bool(ok), 'err': err})
        if not ok or dt > limit * 0.9:
            break
    return json.dumps({'rows': rows})

# ---- scratch pad -----------------------------------------------------------
def _snippet(user_code, snippet, limit):
    ns = {}
    buf = io.StringIO()
    try:
        with _Deadline(limit), redirect_stdout(buf):
            exec(user_code, ns)
            try:
                val = eval(compile(snippet, '<scratch>', 'eval'), ns)
            except SyntaxError:
                exec(compile(snippet, '<scratch>', 'exec'), ns)
                val = None
        return json.dumps({'printed': buf.getvalue()[:4000],
                           'value': '' if val is None else repr(val)[:2000]})
    except Exception as e:
        return json.dumps({'printed': buf.getvalue()[:4000],
                           'error': '%s: %s' % (type(e).__name__, e)})
`;

  function ready(onProgress) {
    if (py) return Promise.resolve(py);
    if (loading) return loading;
    onProgress && onProgress('Fetching the Python runtime (~10 MB, first run only)…');
    loading = new Promise((res, rej) => {
      const sc = document.createElement('script');
      sc.src = URL_BASE + 'pyodide.js';
      sc.onload = res;
      sc.onerror = () => rej(new Error('Could not fetch pyodide.js — are you online?'));
      document.head.appendChild(sc);
    }).then(() => window.loadPyodide({indexURL: URL_BASE}))
      .then((p) => { p.runPython(PY); py = p; return p; });
    return loading;
  }

  const call = (name, args) => JSON.parse(py.globals.get(name)(...args));

  return {
    ready: ready,
    loaded: () => !!py,
    tests:      (code, fn, cases, limit)        => call('_run',        [code, fn, JSON.stringify(cases), limit]),
    diff:       (code, ref, gen, fn, o)         => call('_diff',       [code, ref, gen, fn, o.trials, o.maxN, o.limit, o.budget]),
    complexity: (code, gen, fn, sizes, limit)   => call('_complexity', [code, gen, fn, sizes, limit]),
    snippet:    (code, text, limit)             => call('_snippet',    [code, text, limit])
  };
})();
