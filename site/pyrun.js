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

# ---- plain "Run" button: execute the editor contents as a standalone script --
def _run_editor(user_code, limit):
    """Run the buffer top-to-bottom like a .py file; report stdout or the traceback."""
    buf = io.StringIO()
    try:
        with _Deadline(limit), redirect_stdout(buf):
            exec(user_code, {})
        return json.dumps({'printed': buf.getvalue()[:4000], 'error': None})
    except Exception as e:
        return json.dumps({'printed': buf.getvalue()[:4000],
                           'error': traceback.format_exc(limit=6)})
`;

  const BOOT_TIMEOUT = 180000;   // a cold 10 MB runtime on a slow line is normal

  function ready(onProgress) {
    if (py) return Promise.resolve(py);
    if (loading) return loading;

    /* Pyodide's loader swallows a failed wasm instantiation as console.warn
       calls and then hangs forever. Capture those so the failure is visible. */
    const bootLog = [];
    const origWarn = console.warn, origError = console.error;
    console.warn = (a, ...rest) => { bootLog.push([a].concat(rest).map(String).join(' ')); origWarn(a, ...rest); };
    console.error = (a, ...rest) => { bootLog.push([a].concat(rest).map(String).join(' ')); origError(a, ...rest); };
    const finish = () => { console.warn = origWarn; console.error = origError; };

    onProgress && onProgress('Fetching the Python runtime (~10 MB, first run only)…');

    /* Check the wasm before handing over to Pyodide. Its loader treats a
       broken response — a 404 page, a mangled status line, text/html instead
       of application/wasm — as a warning and then never resolves, which looks
       exactly like a hang. Failing here says what is actually wrong. */
    /* Preflight the wasm before handing over to Pyodide. Its loader turns a
       broken response - a 404 page, a mangled status line, a missing or wrong
       Content-Type - into a console warning and then never resolves, which on
       screen is indistinguishable from a slow download. Checking here turns
       that silent hang into one sentence saying what is actually wrong.

       Content-Type matters more than it looks: WebAssembly.instantiateStreaming
       refuses anything that is not application/wasm, so a server that omits it
       is the single most common cause of "Python never starts". */
    const WASM = URL_BASE + 'pyodide.asm.wasm';

    function checkType(r, method) {
      if (!r.ok && r.status !== 206) throw new Error(r.status + ' ' + r.statusText);
      const ct = (r.headers.get('content-type') || '').split(';')[0].trim();
      if (!ct) return false;                    /* undecided - caller looks closer */
      if (ct !== 'application/wasm' && ct !== 'application/octet-stream') {
        throw new Error('it is served as "' + ct + '" instead of application/wasm' +
                        ' (' + method + ')');
      }
      return true;
    }

    async function verifyRuntime() {
      let decided = false;
      try {
        decided = checkType(await fetch(WASM, {method: 'HEAD'}), 'HEAD');
      } catch (e) {
        if (/application\/wasm/.test(e.message)) throw e;   /* a real verdict */
        decided = false;                                    /* HEAD refused; look closer */
      }
      if (decided) return;

      const r = await fetch(WASM, {headers: {Range: 'bytes=0-7'}});
      if (!checkType(r, 'GET')) {
        if (r.body && r.body.cancel) r.body.cancel();
        throw new Error('it is served without a Content-Type of application/wasm, ' +
                        'so the browser refuses to compile it');
      }
      /* Read the body only when the range was honoured - otherwise this is the
         whole 10 MB and reading it would download the runtime twice. */
      if (r.status !== 206) { if (r.body && r.body.cancel) r.body.cancel(); return; }
      const b = new Uint8Array(await r.arrayBuffer());
      if (b.length >= 4 && !(b[0] === 0x00 && b[1] === 0x61 && b[2] === 0x73 && b[3] === 0x6d)) {
        throw new Error('the first bytes are not a WebAssembly module ' +
                        '(a proxy, or a cached error page, is rewriting it)');
      }
    }

    const preflight = location.protocol === 'file:'
      ? Promise.resolve()                       /* fetch() cannot see file:// */
      : verifyRuntime().catch((e) => {
          throw new Error('The Python runtime at ' + WASM + ' could not be loaded: ' +
                          ((e && e.message) || e) + '.\nIf you are offline, use the ' +
                          'Docker image, which ships the runtime.');
        });

    const boot = preflight.then(() => new Promise((res, rej) => {
      if (window.loadPyodide) return res();          /* script already on the page */
      const sc = document.createElement('script');
      sc.src = URL_BASE + 'pyodide.js';
      sc.onload = res;
      sc.onerror = () => rej(new Error('Could not fetch pyodide.js — are you online?'));
      document.head.appendChild(sc);
    })).then(() => {
      if (typeof window.loadPyodide !== 'function') {
        /* The script tag "loaded" but defined nothing: what came back from
           pyodide.js is not the loader. A server that mangles its responses
           (wrong MIME, a rewritten status line, an error page with a 200) ends
           up here, and the raw symptom - loadPyodide is not a function - says
           nothing useful about the cause. */
        throw new Error(URL_BASE + 'pyodide.js did not define loadPyodide, so what the ' +
                        'server returned for it is not the Pyodide loader. Check that ' +
                        URL_BASE + ' serves the real files with correct headers.');
      }
      return window.loadPyodide({indexURL: URL_BASE});
    }).then((p) => { p.runPython(PY); py = p; return p; });

    let timer = null;
    const timeout = new Promise((res, rej) => {
      timer = setTimeout(() => rej(new Error(
        bootLog.length
          ? 'Python failed to start. Console says:\n' + bootLog.join('\n')
          : 'Python still was not ready after ' + (BOOT_TIMEOUT / 1000) +
            ' s. Is ' + URL_BASE + ' reachable?')), BOOT_TIMEOUT);
    });

    /* A failed boot must not poison every later attempt: drop the memoised
       promise so pressing Run again really retries. */
    loading = Promise.race([boot, timeout]).then(
      (p) => { clearTimeout(timer); finish(); return p; },
      (e) => { clearTimeout(timer); finish(); loading = null; throw e; });
    return loading;
  }

  /* py.globals.get() hands back a PyProxy that JS must free itself; without
     the destroy() every Run leaked one. */
  function call(name, args) {
    const fn = py.globals.get(name);
    try {
      return JSON.parse(fn(...args));
    } finally {
      if (fn && fn.destroy) fn.destroy();
    }
  }

  return {
    ready: ready,
    loaded: () => !!py,
    tests:      (code, fn, cases, limit)        => call('_run',        [code, fn, JSON.stringify(cases), limit]),
    diff:       (code, ref, gen, fn, o)         => call('_diff',       [code, ref, gen, fn, o.trials, o.maxN, o.limit, o.budget]),
    complexity: (code, gen, fn, sizes, limit)   => call('_complexity', [code, gen, fn, sizes, limit]),
    snippet:    (code, text, limit)             => call('_snippet',    [code, text, limit]),
    run:        (code, limit)                   => call('_run_editor', [code, limit])
  };
})();
