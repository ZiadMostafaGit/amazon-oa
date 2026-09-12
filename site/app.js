(function () {
  const P = window.PROBLEMS;
  const KEY = 'amzoa:';
  const $ = (s) => document.querySelector(s);

  /* The ~10 MB runtime stays cached via immutable HTTP responses on /vendor/
     (see server.py), which is more robust than a service worker. Drop any
     service worker a previous version registered and purge its caches. */
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(
      (rs) => rs.forEach((r) => r.unregister())
    ).catch(() => {});
  }
  if ('caches' in window) {
    caches.keys().then(
      (keys) => Promise.all(keys.filter((k) => k.indexOf('amzoa') === 0)
                            .map((k) => caches.delete(k)))
    ).catch(() => {});
  }

  /* ---------- starter code stubs (Python only) ---------- */
  const PY_TYPE = {
    int:'int', long:'int', string:'str', boolean:'bool',
    'int[]':'List[int]', 'int[][]':'List[List[int]]',
    'string[]':'List[str]', 'boolean[]':'List[bool]', 'char[]':'List[str]'
  };

  function stub(p) {
    if (!p.fn) {
      return '# Scratch pad \u2014 this is a project/debugging question.\n' +
             '# Use this editor for notes, snippets, or the fix you plan to make.\n';
    }
    const f = p.fn;
    const params = f.params.map(x => x[1] + ': ' + (PY_TYPE[x[0]] || 'int'));
    const ret = PY_TYPE[f.ret] || 'int';
    const sig = `def ${f.name}(${params.join(', ')}) -> ${ret}:`;
    const needsTyping = /List\[/.test(params.join(',') + ret);
    return (needsTyping ? 'from typing import List\n\n\n' : '') +
           sig + '\n    pass\n';
  }

  /* ---------- state ---------- */
  const load = (k, d) => { try { const v = localStorage.getItem(KEY + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } };
  const save = (k, v) => { try { localStorage.setItem(KEY + k, JSON.stringify(v)); } catch (e) {} };

  /* ---------- server sync ---------- */
  /* localStorage alone is per-browser and dies with a cache wipe. When served
     by server.py (the Docker image), the whole amzoa:* state is mirrored to a
     JSON file through the state API, so code, notes and progress survive
     browser restarts and travel across devices. Plain file:// or no backend: no-op. */
  /* The API endpoint is DISCOVERED at run time: we probe every plausible URL
     and keep the first one that answers JSON. This works under a /site/
     reverse proxy, mounted at the site root, or on the container directly —
     no nginx routing trick needed. A badge next to the lib shows the result so
     a broken deployment is visible instead of silent. */
  const API_CANDIDATES = ['api/state', '../api/state', '/site/api/state', '/api/state']
    .map(u => { try { return new URL(u, location.href).toString(); } catch (e) { return u; } })
    .filter((v, i, a) => a.indexOf(v) === i);
  let apiURL = null;
  function syncInfo(t, cls) {
    const b = $('#sync');
    if (!b) return;
    b.textContent = t;
    b.className = cls || '';
    b.title = 'Server-side sync: ' + t;
  }
  async function probe(url) {
    const t = new AbortController();
    const to = setTimeout(() => t.abort(), 4000);
    try {
      const r = await fetch(url, {cache: 'no-store', signal: t.signal});
      if (r.ok && (r.headers.get('content-type') || '').includes('application/json')) {
        return await r.json();
      }
    } catch (e) {}
    finally { clearTimeout(to); }
    return null;
  }
  async function findApi() {
    for (const u of API_CANDIDATES) {
      const data = await probe(u);
      if (data) { apiURL = u; return data; }
    }
    apiURL = null;
    return null;
  }
  function collectState() {
    const out = {};
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k && k.startsWith(KEY)) out[k.slice(KEY.length)] = localStorage.getItem(k);
    }
    return out;
  }
  async function postState() {
    const cands = apiURL ? [apiURL] : API_CANDIDATES;
    for (const u of cands) {
      try {
        const r = await fetch(u, {method:'POST', headers:{'Content-Type':'application/json'},
                                  body:JSON.stringify(collectState())});
        if (r.ok) { syncInfo('☁ synced', 'ok'); return true; }
      } catch (e) {}
    }
    apiURL = null;                   /* force a fresh probe next time */
    syncInfo('☁ offline', 'bad');
    return false;
  }
  let pushTimer = null;
  function pushState() {
    clearTimeout(pushTimer);
    syncInfo('☁ saving…', 'busy');
    pushTimer = setTimeout(postState, 400);
  }
  async function pullState() {
    let data;
    try { data = await findApi(); } catch (e) { data = null; }
    if (!data) { syncInfo('☁ offline (local only)', 'bad'); return; }
    const keys = Object.keys(data);
    if (!keys.length) { pushState(); return; }          /* fresh server, seed it */

    /* Overlay the server copy onto localStorage WITHOUT reloading — a reload
       here is what caused an endless refresh when a proxy made the two never
       converge (applyFsz/applyEfs rewrite the keys pullState was deleting). */
    let diffs = 0;
    keys.forEach(k => {
      if (localStorage.getItem(KEY + k) !== data[k]) {
        localStorage.setItem(KEY + k, data[k]); diffs++;
      }
    });
    syncInfo('☁ synced', 'ok');
    if (!diffs) return;

    /* Server had something new: re-read the parts the user is looking at now. */
    if ('idx' in data && parseInt(data.idx, 10) !== idx && parseInt(data.idx, 10) < P.length) {
      idx = parseInt(data.idx, 10);
      location.hash = P[idx].id;
      render();
    } else {
      loadCode(); loadNotes(); renderStatusBtns(); renderRail(); renderDrawer(); renderNotesBtn();
      if (data['fsz']) { fsz = parseInt(data['fsz'], 10); applyFsz(); }
      if (data['efs']) { efs = parseInt(data['efs'], 10); applyEfs(); }
    }
  }

  let idx = Math.min(load('idx', 0), P.length - 1);
  const LANG = 'python';   // Python only \u2014 the editor is tuned for it

  /* Per-problem status: 'attempt' | 'solved' | 'review' (absent = not started).
     Migrated once from the older binary `touched` map. */
  let status = load('status', null);
  if (!status) {
    status = {};
    const t = load('touched', {});
    Object.keys(t).forEach(id => { status[id] = 'attempt'; });
    save('status', status);
  }
  const MARK = {attempt:'a', solved:'s', review:'r'};

  function setStatus(id, s) {
    if (status[id] === s) delete status[id]; else status[id] = s;   // click again to clear
    save('status', status);
    pushState();
    renderStatusBtns(); renderRail(); renderDrawer();
  }

  /* ---------- problem text size ---------- */
  let fsz = load('fsz', 17);
  function applyFsz() {
    fsz = Math.min(26, Math.max(13, fsz));
    document.documentElement.style.setProperty('--pfs', fsz + 'px');
    $('#fsVal').textContent = fsz;
    save('fsz', fsz);
    pushState();
  }
  $('#fsUp').onclick   = () => { fsz += 1; applyFsz(); };
  $('#fsDown').onclick = () => { fsz -= 1; applyFsz(); };
  applyFsz();

  /* ---------- editor ---------- */
  /* Python only. Everything below is tuned for one language rather than
     hedged across four: indentation, completion and the stub all assume it. */
  const ta = $('#code');
  let cm = null;

  /* --- indentation: real tab stops, not "always insert 4 spaces" --- */
  function indentUnit(c) { return c.getOption('indentUnit') || 4; }

  /* In vim normal/visual mode, Tab, Enter and Backspace are motions and must
     reach the vim keymap. extraKeys wins over keyMap, so hand them back. */
  function vimCommandMode(c) { return !!(c.state.vim && !c.state.vim.insertMode); }

  function tabKey(c) {
    if (vimCommandMode(c)) return CodeMirror.Pass;
    if (c.somethingSelected()) return c.indentSelection('add');
    const cur = c.getCursor(), n = indentUnit(c);
    const line = c.getLine(cur.line);
    const lead = (line.match(/^ */) || [''])[0].length;
    if (cur.ch <= lead) {
      /* Cursor is in the indent: grow the line's indentation to the next stop.
         Do NOT use cm.indentLine(..., 'add') here — CodeMirror forces
         indentation to 0 on any line with no non-whitespace character, so on a
         blank line inside a block it wipes the indent and sends the cursor to
         column 0 instead of indenting. Insert the spaces ourselves. */
      c.replaceRange(' '.repeat(n - (lead % n)),
                     CodeMirror.Pos(cur.line, 0), CodeMirror.Pos(cur.line, 0), '+input');
      return;
    }
    /* Past the text, Tab moves to the next tab stop. */
    c.replaceSelection(' '.repeat(n - (cur.ch % n)));
  }
  function shiftTabKey(c) {
    if (vimCommandMode(c)) return CodeMirror.Pass;
    c.indentSelection('subtract');
  }

  /* Backspace inside leading whitespace eats a whole indent level. */
  function backspaceKey(c) {
    if (vimCommandMode(c)) return CodeMirror.Pass;
    if (c.somethingSelected()) return CodeMirror.Pass;
    const cur = c.getCursor(), n = indentUnit(c);
    const before = c.getLine(cur.line).slice(0, cur.ch);
    if (cur.ch > 0 && /^ +$/.test(before) && before.length % n === 0) {
      c.replaceRange('', CodeMirror.Pos(cur.line, cur.ch - n), cur, '+delete');
      return;
    }
    return CodeMirror.Pass;
  }

  /* Python-aware indentation for a fresh line opened BELOW `fromLine`.
     Keeps the reference line's indentation, except a block opener (any
     statement ending in ':') opens one level deeper so the next line is ready
     to type a loop/def body. Tabs are counted using tabSize. */
  function indentBelow(cm, fromLine) {
    const unit = indentUnit(cm);
    const tab = cm.getOption('tabSize') || unit;
    const line = cm.getLine(fromLine) || '';
    const lead = (line.match(/^[ \t]*/) || [''])[0];
    const width = lead.replace(/\t/g, ' '.repeat(tab)).length;
    const body = line.slice(lead.length).replace(/#.*$/, '').trim();
    if (body && /:$/.test(body)) return width + unit;
    return width;
  }

  /* Enter indents after a colon (block opener) and, additionally, dedents
     after a statement that ends a block. */
  const BLOCK_EXIT = /^\s*(return|pass|break|continue|raise)\b/;
  function enterKey(c) {
    if (vimCommandMode(c)) return CodeMirror.Pass;
    c.execCommand('newlineAndIndent');
    const pos = c.getCursor();
    if (pos.line === 0) return;
    const tab = c.getOption('tabSize') || indentUnit(c);
    let ind = indentBelow(c, pos.line - 1);
    if (BLOCK_EXIT.test(c.getLine(pos.line - 1)) && ind >= indentUnit(c)) {
      ind -= indentUnit(c);
    }
    const newLine = c.getLine(pos.line);
    const raw = (newLine.match(/^[ \t]*/) || [''])[0];
    if (newLine.trim() === '' &&
        raw.replace(/\t/g, ' '.repeat(tab)).length !== ind) {
      c.replaceRange(' '.repeat(ind),
                     CodeMirror.Pos(pos.line, 0),
                     CodeMirror.Pos(pos.line, raw.length),
                     '+input');
    }
    c.setCursor(CodeMirror.Pos(pos.line, ind));
  }

  /* Vim's o/O inserts a bare "\n" and leaves the cursor at column 0 on the raw
     new line. Real vim keeps the current line's indentation on the opened line
     and drops the cursor right after it. newLineAndEnterInsertMode is only bound
     to o and O (normal mode), so override the action itself; the same name keeps
     `5o` repeat, `.` recording and macros working. */
  if (window.CodeMirror && window.CodeMirror.Vim) (function () {
    const Vim = window.CodeMirror.Vim;
    Vim.defineAction('newLineAndEnterInsertMode', function (cm, actionArgs, vim) {
      vim.insertMode = true;
      const after = !!actionArgs.after;
      const cur = cm.getCursor();
      let base, nl;
      if (cur.line === cm.firstLine() && !after) {
        cm.replaceRange('\n', new CodeMirror.Pos(cm.firstLine(), 0));
        base = cm.firstLine() + 1;
        nl = cm.firstLine();
      } else {
        base = after ? cur.line : cur.line - 1;
        const baseLine = cm.getLine(base) || '';
        cm.setCursor(new CodeMirror.Pos(base, baseLine.length));
        (CodeMirror.commands.newlineAndIndentContinueComment || CodeMirror.commands.newlineAndIndent)(cm);
        nl = base + 1;
      }
      const ind = after ? ' '.repeat(indentBelow(cm, base))
                        : (cm.getLine(cur.line) || '').match(/^[\t ]*/)[0];
      const got = (cm.getLine(nl) || '').match(/^[\t ]*/)[0];
      if (got !== ind) {
        cm.replaceRange(ind, new CodeMirror.Pos(nl, 0), new CodeMirror.Pos(nl, got.length), '+input');
      }
      cm.setCursor(new CodeMirror.Pos(nl, ind.length));
      this.enterInsertMode(cm, { repeat: actionArgs.repeat }, vim);
    });
  })();

  /* --- completion ---
     Backed by pyenv.js, generated from a real CPython stdlib: every builtin and
     keyword, all module names, the public members of 176 modules, and the methods
     of the built-in types. Falls back to a small inline set if pyenv.js is absent. */
  const ENV = window.PYENV || {builtins:[], keywords:[], modules:{}, methods:{}, allmodules:[]};
  const PY_KEYWORDS = ENV.keywords.length ? ENV.keywords.concat(ENV.softkeywords || [])
    : ('False None True and as assert async await break class continue def del elif else except ' +
       'finally for from global if import in is lambda nonlocal not or pass raise return try ' +
       'while with yield').split(' ');
  const PY_BUILTINS = ENV.builtins.length ? ENV.builtins.concat(['self'])
    : ('abs all any bool dict enumerate filter float int len list map max min print range set ' +
       'sorted str sum tuple zip self').split(' ');
  const MODULE_NAMES = ENV.allmodules.length ? ENV.allmodules : Object.keys(ENV.modules);
  /* every method of every builtin type, for a receiver we cannot resolve */
  const ANY_METHOD = (function () {
    const set = new Set();
    Object.keys(ENV.methods || {}).forEach(t => (ENV.methods[t] || []).forEach(m => set.add(m)));
    if (!set.size) 'append extend pop keys values items get add split join strip replace'
      .split(' ').forEach(m => set.add(m));
    return [...set].sort();
  })();

  /* the whole stdlib vocabulary — module members, builtins, methods — so an
     obscure name still completes even when nothing in the buffer hints at it */
  const ANY_NAME = (function () {
    const set = new Set(ENV.builtins || []);
    (ENV.keywords || []).forEach(w => set.add(w));
    (ENV.allmodules || []).forEach(w => set.add(w));
    Object.keys(ENV.modules || {}).forEach(mod => (ENV.modules[mod] || []).forEach(w => set.add(w)));
    Object.keys(ENV.methods || {}).forEach(t => (ENV.methods[t] || []).forEach(w => set.add(w)));
    return [...set];
  })();

  /* typed literals and calls we can infer, so `d.` on `d = {}` completes dict
     methods and `q.` on `q = deque()` completes deque methods */
  const TYPE_METHODS = {
    str: ENV.methods.str, list: ENV.methods.list, dict: ENV.methods.dict,
    set: ENV.methods.set, tuple: ENV.methods.tuple, int: ENV.methods.int,
    float: ENV.methods.float, bytes: ENV.methods.bytes,
    frozenset: ENV.methods.frozenset, complex: ENV.methods.complex
  };
  const KNOWN_CLASS = {
    Counter:     (ENV.methods.dict || []).concat(['most_common', 'subtract', 'elements', 'total']),
    defaultdict: (ENV.methods.dict || []).concat(['default_factory']),
    OrderedDict: (ENV.methods.dict || []).concat(['move_to_end', 'popitem']),
    deque:       (ENV.methods.list || []).concat(['appendleft', 'extendleft', 'popleft', 'rotate'])
  };
  /* Constructor calls and builtins whose result type we can pin down. */
  const CALL_TYPES = {
    list:'list', set:'set', dict:'dict', tuple:'tuple', sorted:'list', reversed:'list',
    bytes:'bytes', str:'str', int:'int', float:'float', frozenset:'frozenset'
  };
  /* `x = s.split(',')` makes x a list, `x = line.strip()` keeps it a str, and
     .copy() inherits the receiver's type. Used by varTypes below. */
  const RET_INHERIT = {};
  const METHOD_RET = {
    split:'list', splitlines:'list', rsplit:'list', partition:'list', rpartition:'list',
    keys:'list', values:'list', items:'list', groups:'list', reversed:'list',
    enumerate:'list', zip:'list', map:'list', filter:'list', findall:'list',
    join:'str', strip:'str', lstrip:'str', rstrip:'str', lower:'str', upper:'str',
    replace:'str', removeprefix:'str', removesuffix:'str', title:'str', capitalize:'str',
    casefold:'str', swapcase:'str', format:'str', expandtabs:'str', translate:'str', repr:'str',
    encode:'bytes', frombytes:'bytes', to_bytes:'bytes', decode:'str',
    copy: RET_INHERIT
  };
  function varTypes(text) {
    const t = {};
    const re = /^[ \t]*([A-Za-z_]\w*)\s*=\s*(.*)$/gm;
    let m;
    while ((m = re.exec(text))) {
      const v = m[1], rhs = m[2].trim();
      let ty = null;
      if (/^\[/ .test(rhs)) ty = 'list';
      else if (/^\{[^:}]*\}/.test(rhs)) ty = 'set';
      else if (/^\{/.test(rhs)) ty = 'dict';
      else if (/^[fFbB]?['"]/.test(rhs)) ty = /^b/i.test(rhs) ? 'bytes' : 'str';
      else if (/^-?\d+$/.test(rhs)) ty = 'int';
      else if (/^-?\d*\.\d+/.test(rhs) || /^\.\d+/.test(rhs)) ty = 'float';
      else { const call = rhs.match(/^([A-Za-z_]\w*)\s*\(/); if (call && KNOWN_CLASS[call[1]]) ty = call[1]; }
      if (!ty) { const f = rhs.match(/^(list|set|dict|tuple|sorted|reversed|bytes|str|int|float|frozenset)\s*\(/); if (f) ty = CALL_TYPES[f[1]]; }
      if (!ty) {
        const mc = rhs.match(/^(\w+)\.(\w+)\s*\(/);          // line.split(...) -> list, etc.
        if (mc && t[mc[1]]) {
          const r = METHOD_RET[mc[2]];
          if (r === RET_INHERIT) ty = t[mc[1]];
          else if (r) ty = r;
        }
      }
      if (ty) t[v] = ty;
    }

    /* Type annotations tell us more than any value: a stub already declares
       `def twoSum(nums: List[int], target: int)`, so nums completes list methods
       and target completes int methods before a single line is written. */
    const tyMap = (raw) => {
      const s = raw.replace(/\s/g, '');
      if (KNOWN_CLASS[s]) return s;                         // deque, Counter, defaultdict…
      if (/^(List|Deque)\[/.test(s)) return 'list';
      if (/^(Dict|DefaultDict)\[/.test(s)) return 'dict';
      if (/^(Set|FrozenSet|Counter\[)/.test(s)) return 'set';
      if (/^Tuple\[/.test(s)) return 'tuple';
      if (/^Optional\[/.test(s) || /^Union\[/.test(s)) return tyMap(s.slice(s.indexOf('[') + 1, -1));
      return ({str:'str', int:'int', float:'float', bool:'int', bytes:'bytes',
               list:'list', dict:'dict', set:'set', tuple:'tuple', frozenset:'frozenset', deque:'list'})[s] || null;
    };
    const dump = (name, raw) => { const ty = tyMap(raw); if (ty) t[name] = ty; };
    const defRe = /^[ \t]*def[ \t]+[A-Za-z_]\w*[ \t]*\(([^)]*)\)/gm;
    while ((m = defRe.exec(text))) {
      m[1].split(',').forEach(part => {
        const mm = part.match(/^\s*([A-Za-z_]\w*)\s*:\s*([A-Za-z_][\w\[\], .]*)/);
        if (mm) dump(mm[1], mm[2]);
      });
    }
    const annRe = /^[ \t]*([A-Za-z_]\w*)\s*:\s*([A-Za-z_][\w\[\], .]*?)\s*=\s*/gm;
    while ((m = annRe.exec(text))) dump(m[1], m[2]);
    return t;
  }
  function selfAttrs(text) {
    const set = new Set(), re = /self\.([A-Za-z_]\w*)/g;
    let m;
    while ((m = re.exec(text))) set.add(m[1]);
    return set.size ? [...set].sort() : null;
  }

  /* Resolve what sits before a dot: an imported module (np -> numpy), a known
     stdlib class, a variable we saw assigned a typed value, or `self`. */
  function resolveMembers(base, imports, text) {
    if (base === 'self') { const a = selfAttrs(text); if (a) return {list: a, kind: 'attr'}; return null; }
    const mod = imports.alias[base] || base;
    if (ENV.modules[mod]) return {list: ENV.modules[mod], kind: mod};
    if (KNOWN_CLASS[base]) return {list: KNOWN_CLASS[base], kind: 'obj'};
    const vt = varTypes(text)[base] || varTypes(text)[base.split('.').pop()];
    if (vt) { const l = TYPE_METHODS[vt] || KNOWN_CLASS[vt]; if (l) return {list: l.slice(), kind: vt}; }
    return null;
  }

  function bufferWords(c, skip) {
    const out = new Set(), re = /[A-Za-z_][A-Za-z0-9_]*/g;
    let m; const text = c.getValue();
    while ((m = re.exec(text))) if (m[0] !== skip && m[0].length > 1) out.add(m[0]);
    return out;
  }

  /* Typing the exact block keyword (then Tab/Esc open) gets a structure, not
     just the bare word. */
  const SNIPPETS = {
    def: 'def name(args):', class: 'class Name():',
    for: 'for i in range(n):', while: 'while cond:',
    with: 'with ctx as obj:', try: 'try:',
    except: 'except Exception as e:', finally: 'finally:',
    if: 'if cond:', elif: 'elif cond:', else: 'else:',
    main: 'if __name__ == "__main__":'
  };

  /* Names that only exist once their module is imported. Picking one of these
     from the completions in a buffer that lacks the import silently prepends
     the matching line — type `deque` + Enter and it starts working, no manual
     `from collections import deque`. */
  const NEED_IMPORT = {
    deque:'collections', Counter:'collections', defaultdict:'collections',
    OrderedDict:'collections', namedtuple:'collections',
    heapify:'heapq', heappush:'heapq', heappop:'heapq', heappushpop:'heapq',
    heapreplace:'heapq', nlargest:'heapq', nsmallest:'heapq',
    bisect_left:'bisect', bisect_right:'bisect', insort_left:'bisect', insort_right:'bisect',
    groupby:'itertools', permutations:'itertools', combinations:'itertools',
    combinations_with_replacement:'itertools', product:'itertools', accumulate:'itertools',
    chain:'itertools', islice:'itertools', takewhile:'itertools', dropwhile:'itertools',
    count:'itertools', cycle:'itertools', repeat:'itertools',
    lru_cache:'functools', cache:'functools', reduce:'functools', total_ordering:'functools',
    List:'typing', Dict:'typing', Set:'typing', Tuple:'typing', Optional:'typing',
    DefaultDict:'typing', Deque:'typing',
    gcd:'math', lcm:'math', comb:'math', perm:'math', factorial:'math', isqrt:'math',
    sqrt:'math', floor:'math', ceil:'math', inf:'math', nan:'math',
    log:'math', log2:'math', log10:'math', exp:'math', hypot:'math', dist:'math'
  };
  function moduleImported(text, mod) {
    return new RegExp('^[ \\t]*(from|import)[ \\t]+' + mod + '\\b', 'm').test(text);
  }
  function importLine(w) { return 'from ' + NEED_IMPORT[w] + ' import ' + w; }
  function makeAutoImport(w, from, to) {
    const mod = NEED_IMPORT[w], line = importLine(w);
    return (cm) => {
      cm.replaceRange(w, from, to, 'complete');
      if (!moduleImported(cm.getValue(), mod)) {
        cm.replaceRange(line + '\n', CodeMirror.Pos(0, 0), CodeMirror.Pos(0, 0), 'insert');
      }
    };
  }

  /* Resolve what a name refers to, by reading the buffer's own imports:
       import re                  -> re
       import numpy as np         -> np means numpy
       from collections import X  -> X is a plain name
     This is what makes `np.` complete when the user aliased the module. */
  function importMap(text) {
    const alias = {}, plain = [];
    const re1 = /^[ \t]*import[ \t]+([\w., \t]+)$/gm;
    const re2 = /^[ \t]*from[ \t]+([\w.]+)[ \t]+import[ \t]+([\w, \t*]+)$/gm;
    let m;
    while ((m = re1.exec(text))) {
      m[1].split(',').forEach(part => {
        const bits = part.trim().split(/\s+as\s+/);
        const mod = bits[0].trim(), as = (bits[1] || bits[0]).trim().split('.')[0];
        if (mod) { alias[as] = mod; plain.push(as); }
      });
    }
    while ((m = re2.exec(text))) {
      const mod = m[1].trim();
      m[2].split(',').forEach(part => {
        const bits = part.trim().split(/\s+as\s+/);
        const name = (bits[1] || bits[0]).trim();
        if (name && name !== '*') { plain.push(name); }
        else if (name === '*') (ENV.modules[mod] || []).forEach(x => plain.push(x));
      });
    }
    return {alias: alias, plain: plain};
  }

  function pythonHint(c) {
    const cur = c.getCursor(), line = c.getLine(cur.line);
    const tok = c.getTokenAt(cur);
    if (tok.type === 'comment' || tok.type === 'string') return null;   // never inside those

    let start = cur.ch;
    while (start && /[\w$]/.test(line.charAt(start - 1))) start--;
    const word = line.slice(start, cur.ch);
    const text = c.getValue();
    const imports = importMap(text);

    /* Entries carry a rank so that context beats brevity: a module's own members
       must outrank the generic method list, or `collections.` drowns in `add`,
       `get`, `pop`… and never reaches `defaultdict`. */
    let pool;
    const beforeWord = line.slice(0, start);
    const fromImport = /(^|\n)[ \t]*from[ \t]+([\w.]+)[ \t]+import[ \t]*$/.exec(beforeWord);
    const importCtx = /(^|\n)[ \t]*(import|from)[ \t][\w., \t]*$/.test(beforeWord);

    if (start > 0 && line.charAt(start - 1) === '.') {                  // member access
      let e = start - 1, s2 = e;
      while (s2 && /[\w$.]/.test(line.charAt(s2 - 1))) s2--;
      const base = line.slice(s2, e);
      const mem = resolveMembers(base, imports, text);
      pool = mem ? mem.list.map(w => [w, mem.kind, 0])
                 : ANY_METHOD.map(w => [w, 'method', 1]).concat(ANY_NAME.map(w => [w, 'attr', 2]));
    } else if (fromImport) {                                            // `from collections import `
      const mem = resolveMembers(fromImport[2], imports, text);
      pool = (mem ? mem.list.map(w => [w, 'import', 0]) : [])
        .concat(MODULE_NAMES.map(w => [w, 'module', 2]));
    } else if (importCtx) {                                             // after `import `
      pool = MODULE_NAMES.map(w => [w, 'module', 0]);
    } else {
      pool = PY_KEYWORDS.map(w => [w, 'kw', 0])
        .concat(PY_BUILTINS.map(w => [w, 'builtin', 0]))
        .concat(imports.plain.map(w => [w, 'import', 0]))
        .concat(MODULE_NAMES.map(w => [w, 'module', 2]))
        .concat([...bufferWords(c, word)].map(w => [w, 'local', 1]))
        .concat(ANY_NAME.map(w => [w, 'std', 3]));
      /* block keyword prefixes get their skeleton, so typing `de` already proposes
        `def name(args):` and the closer the word is to the keyword the higher it ranks */
      Object.keys(SNIPPETS)
        .filter(k => k.startsWith(word))
        .forEach(k => pool.unshift([SNIPPETS[k], 'snip', -2 + (k.length - word.length)]));
    }

    const seen = new Set(), list = [];
    const hfrom = CodeMirror.Pos(cur.line, start), hto = CodeMirror.Pos(cur.line, cur.ch);
    for (const [w, kind, rank] of pool) {
      if (w === word || seen.has(w) || !w.startsWith(word)) continue;
      seen.add(w);
      const item = { text: w, kind: kind, rank: rank, from: hfrom, to: hto,
        render(el) {
          el.appendChild(document.createTextNode(w));
          const b = document.createElement('span'); b.className = 'hk'; b.textContent = kind;
          el.appendChild(b);
        } };
      const mod = NEED_IMPORT[w];
      if (mod && kind !== 'attr' && kind !== 'method' && kind !== 'module' &&
          !moduleImported(text, mod)) item.hint = makeAutoImport(w, hfrom, hto);
      list.push(item);
    }
    if (!list.length) return null;
    list.sort((x, y) => x.rank - y.rank ||
                        x.text.length - y.text.length ||
                        x.text.localeCompare(y.text));
    return { list: list.slice(0, 50), from: hfrom, to: hto };
  }
  if (window.CodeMirror) CodeMirror.registerHelper('hint', 'python', pythonHint);

  if (window.CodeMirror) {
    cm = CodeMirror.fromTextArea(ta, {
      theme:'material-darker', mode:'python', lineNumbers:true,
      indentUnit:4, tabSize:4, indentWithTabs:false, smartIndent:true, electricChars:true,
      autoCloseBrackets:true, matchBrackets:true, styleActiveLine:true,
      lineWrapping:false, showCursorWhenSelecting:true,
      extraKeys:{
        Tab: tabKey, 'Shift-Tab': shiftTabKey, Backspace: backspaceKey, Enter: enterKey,
        'Ctrl-/': 'toggleComment', 'Cmd-/': 'toggleComment',
        'Ctrl-Enter': () => runTests(),
        'Shift-Ctrl-Enter': () => runScratch(),
        'Ctrl-F': 'findPersistent', 'Ctrl-G': 'findNext', 'Shift-Ctrl-G': 'findPrev',
        'Shift-Ctrl-F': 'replace',
        'Ctrl-Space': (c) => c.showHint({hint: pythonHint, completeSingle: false, closeOnUnfocus: true,
                   extraKeys: {Tab: (cm2, h) => h.pick()}}),
        'Shift-Ctrl-K': (c) => c.execCommand('deleteLine'),
        'Alt-Up': (c) => c.execCommand('swapLineUp'),
        'Alt-Down': (c) => c.execCommand('swapLineDown')
      }
    });

    /* Type-ahead completion: fires on word characters and after a dot, never on
       the first keystroke of a word (too noisy) and never while one is open. */
    cm.on('inputRead', (c, ch) => {
      if (c.state.completionActive) return;
      const t = ch.text && ch.text[0];
      if (!t) return;
      if (t === '.') { c.showHint({hint: pythonHint, completeSingle: false, closeOnUnfocus: true,
                   extraKeys: {Tab: (cm2, h) => h.pick()}}); return; }
      if (!/[A-Za-z_]/.test(t)) return;
      const cur = c.getCursor(), line = c.getLine(cur.line);
      let st = cur.ch;
      while (st && /[\w$]/.test(line.charAt(st - 1))) st--;
      if (cur.ch - st >= 1) c.showHint({hint: pythonHint, completeSingle: false, closeOnUnfocus: true,
                   extraKeys: {Tab: (cm2, h) => h.pick()}});
    });
  }

  /* ---------- in-browser test runner ----------
     All four modes go through PyRun (pyrun.js), which owns Pyodide and the
     Python harnesses. This block is only UI: buttons, panels, formatting. */
  const LIMIT = 5;                                  // seconds of Python per call

  const esc = (t) => String(t).replace(/[&<>]/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  const clip = (v, n) => { const t = typeof v === 'string' ? v : JSON.stringify(v);
                           return t && t.length > n ? t.slice(0, n) + '…' : t; };

  /* The reference is read out of the problem's own Solution panel, so the code
     the fuzzer trusts is always exactly the code the page shows. */
  function referenceOf(p) {
    const m = /<details class="sol">[\s\S]*?<pre class="sample"><code>([\s\S]*?)<\/code><\/pre>/
                .exec(p.body);
    if (!m) return null;
    const ta = document.createElement('textarea');
    ta.innerHTML = m[1];
    return ta.value;
  }

  function showTests(open) {
    $('#tests').classList.toggle('hidden', !open);
    if (cm) setTimeout(() => cm.refresh(), 0);
  }
  const testStatus = (h) => { $('#testsMeta').innerHTML = h; };
  const testBody   = (h) => { $('#testsBody').innerHTML = h; };
  const busy = (on) => ['#runBtn', '#diffBtn', '#cxBtn'].forEach(id => {
    const b = $(id); if (b) b.disabled = on || b.dataset.off === '1';
  });

  /* Every mode shares this shell: open the panel, load Python, run, report. */
  async function withPython(title, job) {
    showTests(true);
    busy(true);
    testStatus('');
    testBody('<div class="note">Starting…</div>');
    try {
      await window.PyRun.ready((m) => testBody('<div class="note">' + m + '</div>'));
      testBody('<div class="note">' + title + '</div>');
      job();
    } catch (e) {
      testStatus('<span class="bad">error</span>');
      testBody('<div class="err">' + esc((e && e.message) || e) + '</div>');
    } finally {
      busy(false);
    }
  }

  function printedBlock(t) {
    return t ? '<div class="printed"><span class="lbl">stdout</span>\n' + esc(t.replace(/\s+$/, '')) + '</div>' : '';
  }

  function runTests() {
    const p = P[idx];
    if (!p.tests) return;
    return withPython('Running ' + p.tests.length + ' cases…', () => {
      const res = window.PyRun.tests(getCode(), p.fn.name, p.tests, LIMIT);
      if (res.error) {
        testStatus('<span class="bad">did not run</span>');
        testBody('<div class="err">' + esc(res.error) + '</div>');
        return;
      }
      let passed = 0;
      const rows = res.results.map((r, i) => {
        if (r.ok) passed++;
        const t = p.tests[i];
        return '<div class="case ' + (r.ok ? 'ok' : 'no') + '">' +
          '<b>' + (r.ok ? '✓' : '✗') + ' case ' + (i + 1) + '</b>  ' +
          '<span class="lbl">in</span> ' + esc(clip(t.in, 90)) +
          (r.ok ? '' :
            '\n<span class="lbl">expected</span> <span class="exp">' + esc(clip(t.out, 90)) + '</span>' +
            '\n<span class="lbl">got     </span> <span class="got">' + esc(r.got) + '</span>') +
          printedBlock(r.printed) + '</div>';
      }).join('');
      const all = passed === res.results.length;
      testStatus('<span class="' + (all ? 'good' : 'bad') + '">' + passed + ' / ' +
                 res.results.length + ' passing</span>');
      testBody(rows);
      if (all && status[p.id] !== 'solved' && status[p.id] !== 'review') setStatus(p.id, 'solved');
    });
  }

  /* Randomised differential testing: your code vs the reference, on generated
     inputs, stopping at the first disagreement. This is the mode that catches
     "passed the samples, fails the hidden tests". */
  function runDiff() {
    const p = P[idx];
    if (!p.gen) return;
    const ref = referenceOf(p);
    if (!ref) { testStatus('<span class="bad">no reference</span>'); return; }
    return withPython('Fuzzing against the reference…', () => {
      const r = window.PyRun.diff(getCode(), ref, p.gen, p.fn.name,
                                 {trials: 2000, maxN: 9, limit: 2, budget: 8});
      if (r.error) {
        testStatus('<span class="bad">did not run</span>');
        testBody('<div class="err">' + esc(r.error) + '</div>');
        return;
      }
      if (!r.failed) {
        testStatus('<span class="good">agreed on ' + r.checked + ' random inputs</span>');
        testBody('<div class="case ok"><b>✓ no disagreement found</b>\n' +
          '<span class="lbl">Your code matched the reference on ' + r.checked +
          ' randomly generated inputs.</span>\n' +
          '<span class="lbl">This is evidence, not proof — the generator is random, not adversarial.</span></div>');
        return;
      }
      testStatus('<span class="bad">counterexample found</span>');
      testBody('<div class="case no"><b>✗ ' + (r.crash ? 'your code raised' : 'disagreement') +
        '</b> after ' + r.checked + ' inputs\n' +
        '<span class="lbl">input   </span> ' + esc(r.input) +
        (r.crash ? '\n<span class="lbl">error   </span> <span class="got">' + esc(r.got) + '</span>'
                 : '\n<span class="lbl">expected</span> <span class="exp">' + esc(r.expected) + '</span>' +
                   '\n<span class="lbl">got     </span> <span class="got">' + esc(r.got) + '</span>') +
        '</div><div class="note">Paste that input into Scratch to debug it.</div>');
    });
  }

  /* Empirical complexity. Timings are taken with the trace guard armed, so they
     are proportional to Python operations executed rather than raw wall time —
     which is what the growth ratio needs anyway. */
  function runComplexity() {
    const p = P[idx];
    if (!p.gen) return;
    return withPython('Timing on growing inputs…', () => {
      const r = window.PyRun.complexity(getCode(), p.gen, p.fn.name, [250, 500, 1000, 2000], LIMIT);
      if (r.error) {
        testStatus('<span class="bad">did not run</span>');
        testBody('<div class="err">' + esc(r.error) + '</div>');
        return;
      }
      const rows = r.rows;
      let html = '<table class="cx"><tr><th>requested n</th><th>actual size</th><th>time</th><th>× previous</th></tr>';
      rows.forEach((row, i) => {
        const prev = i ? rows[i - 1].ms : 0;
        const ratio = i && prev > 0.5 ? (row.ms / prev).toFixed(1) + '×' : '—';
        html += '<tr><td>' + row.n + '</td><td>' + row.size + '</td><td>' +
                (row.ok ? row.ms + ' ms' : '—') + '</td><td>' + ratio + '</td></tr>';
      });
      html += '</table>';
      const bad = rows.find(x => !x.ok);
      const grew = rows.length >= 2 && rows[rows.length - 1].size > rows[0].size * 1.5;
      let verdict;
      if (bad) verdict = 'Stopped: <b>' + esc(bad.err || 'too slow') + '</b> at n = ' + bad.n + '.';
      else if (!grew) verdict = 'Inconclusive — this problem\'s generator caps the input size, ' +
                                'so the sizes did not really grow.';
      else {
        const a = rows[rows.length - 2], b2 = rows[rows.length - 1];
        const rt = a.ms > 0.5 ? b2.ms / a.ms : 0;
        verdict = rt === 0 ? 'Too fast to measure — comfortably sub-quadratic.'
          : rt < 1.4 ? 'Doubling the input barely changed the time: looks <b>O(log n)</b> or dominated by overhead.'
          : rt < 3   ? 'Doubling the input roughly doubled the time: looks <b>O(n)</b> or <b>O(n log n)</b>.'
          : rt < 6   ? 'Doubling the input roughly quadrupled the time: looks <b>O(n²)</b>.'
                     : 'Time grew faster than 4× per doubling: <b>worse than O(n²)</b>.';
        verdict += ' Check that against the problem\'s constraint on n.';
      }
      testStatus(bad ? '<span class="bad">stopped early</span>' : '<span class="good">measured</span>');
      testBody('<div class="verdict">' + verdict + '</div>' + html +
               '<div class="note">Times are instrumented (a guard traces every line), so treat ' +
               'them as proportional to work done, not as real-world milliseconds.</div>');
    });
  }

  function runScratch() {
    const text = $('#scratchTa').value.trim();
    if (!text) return;
    return withPython('Running…', () => {
      const r = window.PyRun.snippet(getCode(), text, LIMIT);
      testStatus('<span class="' + (r.error ? 'bad' : 'good') + '">scratch</span>');
      testBody(
        (r.printed ? '<div class="case ok"><span class="lbl">stdout</span>\n' + esc(r.printed) + '</div>' : '') +
        (r.value   ? '<div class="case ok"><span class="lbl">value</span>  ' + esc(r.value) + '</div>' : '') +
        (r.error   ? '<div class="err">' + esc(r.error) + '</div>' : '') ||
        '<div class="note">(no output)</div>');
    });
  }

  /* The plain Run button: execute whatever is in the editor as a top-to-bottom
     script. No test cases, no function name, no generator — prints and errors
     land in the panel below. */
  function runDirect() {
    return withPython('Running the editor as a standalone script…', () => {
      const r = window.PyRun.run(getCode(), LIMIT);
      testStatus(r.error ? '<span class="bad">error</span>'
                         : '<span class="good">ran</span>');
      testBody((r.printed ? printedBlock(r.printed) : '') +
               (r.error ? '<div class="err">' + esc(r.error) + '</div>' : '') ||
               '<div class="note">Ran to completion with no output.</div>');
    });
  }

  /* ---------- "how do I add tests to this problem?" ----------
     Shown on problems that have none. Scaffolds a paste-ready block from the
     declared signature so the shape never has to be guessed. */
  const SAMPLE_ARG = {
    int:'1', long:'1', string:'"abc"', boolean:'true',
    'int[]':'[3, 1, 2]', 'int[][]':'[[1, 2], [3, 4]]',
    'string[]':'["a", "b"]', 'boolean[]':'[true, false]', 'char[]':'["a", "b"]'
  };

  function testScaffold(p) {
    const args = p.fn ? p.fn.params.map(x => SAMPLE_ARG[x[0]] || '1').join(', ') : '';
    const names = p.fn ? p.fn.params.map(x => x[1]).join(', ') : '';
    return {
      tests: '  tests:[\n' +
             '    {in:[' + args + '], out:0},\n' +
             '    {in:[' + args + '], out:0}\n' +
             '  ],',
      gen:   '  gen:`def gen(rng, n):\n' +
             '    # return a random argument list: [' + names + ']\n' +
             '    # n is the target input size — honour the problem\'s constraints here\n' +
             '    return [' + args.replace(/\[3, 1, 2\]/g, '[rng.randint(1, 9) for _ in range(max(1, n))]') + ']`,'
    };
  }

  function showTestHelp() {
    const p = P[idx], sc = testScaffold(p);
    const example = P.find(q => q.tests && q.id === 'getmincost') || P.find(q => q.tests);
    showTests(true);
    testStatus('<span class="bad">no verified cases</span>');
    testBody(
      '<div class="note">This problem has no test cases, because its correct answer could not be ' +
      'established from the source (see the amber note in the Solution panel). Here is how to add them.</div>' +

      '<div class="case ok"><b>1 · open <code>site/problems.js</code> and find this entry</b>\n' +
      '<span class="lbl">search for</span> ' + esc("id:'" + p.id + "'") + '\n' +
      '<span class="lbl">paste the blocks below just above its</span> body:`</div>' +

      '<div class="case ok"><b>2 · fixed cases</b>  <span class="lbl">one object per case; ' +
      'in[] is the argument list in declared order' + (p.fn ? ' (' +
        esc(p.fn.name + '(' + p.fn.params.map(x => x[1]).join(', ') + ')') + ')' : '') +
      '</span>\n\n' + esc(sc.tests) + '</div>' +

      '<div class="case ok"><b>3 · a generator, to unlock Random and Big-O</b>  ' +
      '<span class="lbl">plain Python returning one random argument list</span>\n\n' +
      esc(sc.gen) + '</div>' +

      (example ? '<div class="case ok"><b>4 · a real, working example</b>  ' +
        '<span class="lbl">from ' + esc(example.id) + '</span>\n\n' +
        esc('  tests:[\n' + example.tests.slice(0, 2).map(t =>
          '    {in:' + JSON.stringify(t.in) + ', out:' + JSON.stringify(t.out) + '}').join(',\n') +
          '\n  ],\n' + (example.gen ? '  gen:`' + example.gen + '`,' : '')) + '</div>' : '') +

      '<div class="case ok"><b>5 · never hand-type the expected values</b>\n' +
      '<span class="lbl">Write the inputs, paste a solution you trust into the editor, run it with ' +
      'Scratch, and copy what it returns. That is how every case in this repo was produced — ' +
      'hand-typed expectations are how wrong answers get enshrined.</span></div>' +

      '<div class="note">Reload the page after editing problems.js. Full guide: ADDING-PROBLEMS.md</div>');
  }

  $('#runBtn').onclick     = () => (P[idx].tests ? runTests() : showTestHelp());
  $('#runDirect').onclick  = runDirect;
  $('#diffBtn').onclick    = runDiff;
  $('#cxBtn').onclick      = runComplexity;
  $('#testsClose').onclick = () => showTests(false);
  $('#scratchBtn').onclick = () => {
    const open = $('#scratch').classList.toggle('hidden');
    if (!open) $('#scratchTa').focus();
    if (cm) setTimeout(() => cm.refresh(), 0);
  };
  $('#scratchClose').onclick = () => { $('#scratch').classList.add('hidden'); if (cm) cm.refresh(); };
  $('#scratchTa').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey && e.shiftKey) { e.preventDefault(); runScratch(); }
  });

  function syncRunBtn() {
    const p = P[idx], n = p.tests ? p.tests.length : 0;
    const setOff = (id, off, label, tip) => {
      const b = $(id);
      b.dataset.off = off ? '1' : '0';
      b.disabled = off;
      if (label) b.textContent = label;
      if (tip) b.title = tip;
    };
    setOff('#runBtn', false, n ? '▶ Run ' + n + ' tests' : '＋ Add tests',
           n ? 'Run the published cases (Ctrl-Enter). Python runs in this page.'
             : 'This problem has no verified cases — click to see how to add them');
    setOff('#diffBtn', !p.gen, null,
           p.gen ? 'Fuzz your code against the reference solution on random inputs'
                 : 'No reference/generator for this problem');
    setOff('#cxBtn', !p.gen, null,
           p.gen ? 'Time your solution on growing inputs to estimate its complexity'
                 : 'No input generator for this problem');
  }

  /* --- editor font size --- */
  let efs = load('efs', 14);
  function applyEfs() {
    efs = Math.min(22, Math.max(11, efs));
    document.documentElement.style.setProperty('--efs', efs + 'px');
    $('#efsVal').textContent = efs;
    save('efs', efs);
    pushState();
    if (cm) cm.refresh();
  }
  $('#efsUp').onclick   = () => { efs += 1; applyEfs(); };
  $('#efsDown').onclick = () => { efs -= 1; applyEfs(); };
  applyEfs();

  /* --- vim mode --- */
  let vimOn = load('vim', false);
  const vimBtn = $('#vimBtn');
  function paintVim(label) {
    vimBtn.setAttribute('aria-pressed', vimOn ? 'true' : 'false');
    vimBtn.textContent = vimOn ? ('Vim · ' + (label || 'normal')) : 'Vim';
  }
  function applyVim(focus) {
    if (!cm) return;
    cm.setOption('keyMap', vimOn ? 'vim' : 'default');
    save('vim', vimOn);
    pushState();
    paintVim();
    if (focus) cm.focus();
  }
  if (cm && window.CodeMirror && CodeMirror.Vim) {
    cm.on('vim-mode-change', (e) => {
      if (vimOn) paintVim(e.mode + (e.subMode ? ' ' + e.subMode : ''));
    });
    CodeMirror.Vim.defineEx('write', 'w', () => {   // :w flushes the autosave
      flushSaves(); $('#saved').textContent = 'Autosaved';
    });
  }
  vimBtn.onclick = () => { vimOn = !vimOn; applyVim(true); };
  applyVim(false);

  /* --- relative line numbers (vim-style: current line absolute, the rest how
        many lines away they are, so `5dd` / `3j` line up with the gutter) --- */
  let relNo = load('relno', true);
  const relBtn = $('#relnoBtn');
  function paintRel() {
    if (!relBtn) return;
    relBtn.setAttribute('aria-pressed', relNo ? 'true' : 'false');
    relBtn.textContent = relNo ? 'Rel no' : 'Abs no';
  }
  /* The gutter is re-painted by CodeMirror as absolute numbers; we only rewrite
     the visible copy. _lastSet detects a fresh repaint so _abs stays correct. */
  function relPatch() {
    if (!cm || !relNo) return;
    const curLine = cm.getCursor().line + 1;
    cm.display.lineDiv.querySelectorAll('.CodeMirror-linenumber').forEach(el => {
      const t = el.textContent;
      if (el._lastSet !== t) {
        const n = parseInt(t, 10);
        if (!isNaN(n) && /^\d+$/.test(t)) el._abs = n;
      }
      if (el._abs == null) return;
      const d = el._abs - curLine;
      const out = d === 0 ? String(el._abs) : String(Math.abs(d));
      el.textContent = out;
      el._lastSet = out;
    });
  }
  function relRestore() {
    if (!cm) return;
    cm.display.lineDiv.querySelectorAll('.CodeMirror-linenumber').forEach(el => {
      if (el._abs != null) el.textContent = String(el._abs);
      delete el._lastSet; delete el._abs;
    });
  }
  function applyRel(focus) {
    if (!cm) return;
    save('relno', relNo);
    if (relNo) relPatch(); else relRestore();
    paintRel();
    if (focus) cm.focus();
  }
  if (cm) {
    cm.on('cursorActivity', relPatch);
    cm.on('changes', relPatch);
    cm.on('scroll', relPatch);
  }
  if (relBtn) relBtn.onclick = () => { relNo = !relNo; applyRel(true); };
  applyRel(false);

  const getCode = () => cm ? cm.getValue() : ta.value;
  const setCode = (v) => { cm ? cm.setValue(v) : (ta.value = v); };

  /* A debounced write is bound to the problem it started in and flushed before we
     navigate — otherwise a keystroke 400 ms before "Next" lands on the wrong problem. */
  function saver(delay) {
    let t = null, job = null;
    const run = () => { t = null; const f = job; job = null; f && f(); };
    return { schedule(f) { job = f; clearTimeout(t); t = setTimeout(run, delay); },
             flush() { clearTimeout(t); run(); } };
  }
  const codeSaver = saver(450), noteSaver = saver(450);
  const flushSaves = () => { codeSaver.flush(); noteSaver.flush(); };

  function onEdit() {
    $('#saved').textContent = 'Saving…';
    const id = P[idx].id, lg = LANG, text = getCode();
    codeSaver.schedule(() => {
      save('code:' + id + ':' + lg, text);
      if (!status[id]) { status[id] = 'attempt'; save('status', status);
                         renderStatusBtns(); renderRail(); renderDrawer(); }
      pushState();
      $('#saved').textContent = 'Autosaved';
    });
  }
  /* cm.setValue (programmatic loads: opening a problem, resetting to the stub)
     must not count as "coding" — a problem only turns amber once you actually
     type. Real edits have origins like "+input"; loads arrive as "setValue". */
  if (cm) cm.on('change', (c, ch) => { if (!ch || ch.origin !== 'setValue') onEdit(); });
  else ta.addEventListener('input', onEdit);
  if (cm) cm.on('cursorActivity', () => {
    const c = cm.getCursor();
    save('cur:' + P[idx].id, {line: c.line, ch: c.ch});
  });

  function loadCode() {
    const saved = load('code:' + P[idx].id + ':' + LANG, null);
    setCode(saved === null ? stub(P[idx]) : saved);
    /* come back to where you left off, not to line 1 */
    if (cm) {
      const pos = load('cur:' + P[idx].id, null);
      if (pos && pos.line < cm.lineCount()) {
        cm.setCursor(pos);
        setTimeout(() => cm.scrollIntoView(null, 80), 0);
      }
    }
    $('#saved').textContent = 'Autosaved';
  }

  /* ---------- notes ---------- */
  const nta = $('#notesTa');
  nta.addEventListener('input', () => {
    const id = P[idx].id, text = nta.value;
    noteSaver.schedule(() => { save('notes:' + id, text); renderNotesBtn(); pushState(); });
  });
  function loadNotes() { nta.value = load('notes:' + P[idx].id, ''); renderNotesBtn(); }
  function renderNotesBtn() {
    const has = (load('notes:' + P[idx].id, '') || '').trim().length > 0;
    $('#notesBtn').innerHTML = 'Notes' + (has ? ' <span class="dot">•</span>' : '');
  }
  $('#notesBtn').onclick = () => {
    const n = $('#notes'), showing = n.classList.toggle('hidden');
    save('notesOpen', !showing);
    pushState();
    if (!showing) nta.focus();
    if (cm) cm.refresh();
  };
  if (load('notesOpen', false)) $('#notes').classList.remove('hidden');

  /* ---------- timer (kept per problem, so navigating away doesn't lose the clock) ---------- */
  let tState = null;
  const tKey = () => 'timer:' + P[idx].id;
  const tDurSel = $('#tDur');
  let tDefault = Math.min(240, Math.max(1, parseInt(load('tDefault', 30), 10) || 30));
  function applyTdur() { if (tDurSel) tDurSel.value = String(tDefault); }
  function timerLoad(p, opts) {
    tState = load('timer:' + p.id, null);
    if (!tState || (opts && opts.reset)) tState = { left: tDefault * 60, dur: tDefault, running: false };
    if (opts && opts.start) tState.running = true;
    save('timer:' + p.id, tState);
  }
  if (tDurSel) tDurSel.onchange = () => {
    let mins = parseInt(tDurSel.value, 10);
    if (isNaN(mins)) {                      // the "Custom…" option
      mins = parseInt(window.prompt('Timer length in minutes (1\u2013240):', String(tDefault)), 10);
      if (!mins || isNaN(mins)) { applyTdur(); return; }
    }
    tDefault = Math.min(240, Math.max(1, mins));
    save('tDefault', tDefault);
    applyTdur();
    timerLoad(P[idx], {reset:true}); tick();
  };
  applyTdur();
  function fmt(s) {
    if (s < 0) s = 0;
    const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60;
    return (h ? h + ':' + String(m).padStart(2, '0') : String(m)) + ':' + String(x).padStart(2, '0');
  }
  function tick() {
    if (!tState) return;
    if (tState.running && tState.left > 0) { tState.left--; save(tKey(), tState); }
    $('#tval').textContent = fmt(tState.left);
    const el = $('#timer');
    el.className = tState.left <= 0 ? 'over' : (tState.running ? '' : 'paused');
  }
  setInterval(tick, 1000);
  $('#timer').onclick = () => { if (tState) { tState.running = !tState.running; save(tKey(), tState); tick(); } };
  $('#tReset').onclick = () => { timerLoad(P[idx], {reset:true}); tick(); };

  /* ---------- drill: a random problem you haven't solved, clock running ---------- */
  function drill() {
    const pool = P.filter(p => status[p.id] === 'review');
    const rest = P.filter(p => status[p.id] !== 'solved' && status[p.id] !== 'review');
    const from = pool.length ? pool : (rest.length ? rest : P);
    const pick = from[Math.floor(Math.random() * from.length)];
    go(P.indexOf(pick), {reset:true, start:true});
  }
  $('#drill').onclick = drill;

  /* ---------- render ---------- */
  const SECTIONS = [...new Set(P.map(p => p.section))];

  /* ---------- smart search ---------- */
  /* Per-problem search index built once. Any word you type is matched against
     title, function name, section/platform, the whole transcribed statement,
     and your notes — then ranked so a title hit beats a body hit. */
  const SIDX = P.map(p => {
    const body = p.body.replace(/<[^>]*>/g, ' ');
    return {
      til: p.title.toLowerCase(),
      fn:  (p.fn ? p.fn.name : '').toLowerCase(),
      meta: (p.label + ' ' + p.section + ' ' + p.platform).toLowerCase(),
      body: body.toLowerCase()
    };
  });
  const SOURCE = p => p.section.startsWith('Siemens') ? 'siemens'
    : p.section.startsWith('FastPrep') ? 'fastprep' : 'amazon';
  const stMark = st => st === 'solved' ? '✓' : st === 'review' ? '↻' : '•';

  /* near-duplicates / same project: entries that belong to one multi-part
     project (e.g. the MovieDB debugging trio) are tagged with their siblings
     so "do I already have this?" finds the whole family, not just one entry */
  const PROJECT = {
    'moviedb-search': 'MovieDB', 'moviedb-recs': 'MovieDB', 'moviedb-recs-postmortem': 'MovieDB',
    'workflow-team': 'Workflow', 'workflow-issues': 'Workflow'
  };
  const SIBLING = P.map(p => {
    const fam = PROJECT[p.id];
    if (!fam) return [];
    return P.map(q => q !== p && PROJECT[q.id] === fam ? q : null).filter(Boolean);
  });

  const qtokens = q => q.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim().split(' ').filter(Boolean);

  /* relevance: per-word score by field (title highest, statement lowest); a
     whole-phrase match in the title adds a bonus. Returns null if nothing hit. */
  function score(p, i, tokens, phrase) {
    const s = SIDX[i];
    let sc = 0; const bits = new Set();
    tokens.forEach(t => {
      let w = 0;
      if (s.til.includes(t))        { w = 8; if (t.length > 2 && new RegExp('\\b' + t, '').test(s.til)) w += 2; }
      else if (s.fn.includes(t))    w = 7;
      else if (s.meta.includes(t))  w = 4;
      else if (s.body.includes(t))  w = 1;
      if (w) { sc += w; bits.add(t); }
    });
    if (!bits.size) return null;
    if (s.til.includes(phrase))   sc += 6;
    else if (s.meta.includes(phrase)) sc += 2;
    return {sc, bits: [...bits]};
  }

  const hl = (text, toks) => {
    let out = esc(text);
    toks.forEach(t => out = out.replace(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'),
                                        m => '<mark>' + m + '</mark>'));
    return out;
  };

  function snippet(i, toks) {
    const body = P[i].body.replace(/<[^>]*>/g, ' ');
    const t = toks[0];
    const k = body.toLowerCase().indexOf(t);
    if (k < 0) return '';
    const s0 = Math.max(0, k - 45), e0 = Math.min(body.length, k + t.length + 70);
    let sn = (s0 > 0 ? '…' : '') + body.slice(s0, e0) + (e0 < body.length ? '…' : '');
    toks.forEach(t => sn = sn.replace(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'),
                                      m => '<mark>' + m + '</mark>'));
    return sn;
  }

  function renderRail() {
    const cur = P[idx].section;
    const rail = $('#rail'); rail.innerHTML = '';
    SECTIONS.forEach(sec => {
      const lbl = document.createElement('div');
      lbl.className = 'rl' + (sec === cur ? ' cur' : '');
      lbl.title = sec;
      rail.appendChild(lbl);
      P.forEach((p, i) => {
        if (p.section !== sec) return;
        const st = status[p.id];
        const b = document.createElement('button');
        b.className = 'qdot' + (i === idx ? ' active' : '') + (st ? ' st-' + st : '');
        b.textContent = i + 1;
        b.title = p.title + (st ? ' — ' + st : '');
        b.onclick = () => go(i);
        rail.appendChild(b);
      });
    });
  }

  function renderStatusBtns() {
    const st = status[P[idx].id];
    $('#stAttempt').setAttribute('aria-pressed', st === 'attempt');
    $('#stSolved').setAttribute('aria-pressed', st === 'solved');
    $('#stReview').setAttribute('aria-pressed', st === 'review');
  }
  $('#stAttempt').onclick = () => setStatus(P[idx].id, 'attempt');
  $('#stSolved').onclick  = () => setStatus(P[idx].id, 'solved');
  $('#stReview').onclick  = () => setStatus(P[idx].id, 'review');

  /* ---------- drawer ---------- */
  let dq = '', dfilter = 'all', dsec = 'all';

  function counts(list) {
    const c = {solved:0, attempt:0, review:0, none:0};
    list.forEach(p => c[status[p.id] || 'none']++);
    return c;
  }

  function renderDrawer() {
    const d = $('#drawerList'); if (!d) return;

    const c = counts(P);
    const pct = (n) => (n / P.length * 100).toFixed(2) + '%';
    $('#pbar').innerHTML =
      `<i class="s" style="width:${pct(c.solved)}"></i>` +
      `<i class="a" style="width:${pct(c.attempt)}"></i>` +
      `<i class="r" style="width:${pct(c.review)}"></i>`;
    $('#legend').innerHTML =
      `<span class="s"><b>${c.solved}</b> solved</span>` +
      `<span class="a"><b>${c.attempt}</b> attempted</span>` +
      `<span class="r"><b>${c.review}</b> review</span>` +
      `<span><b>${c.none}</b> untouched</span>`;

    const q = dq.trim();
    const ph = q.toLowerCase();
    const toks = qtokens(q);
    const inStatus = p => dfilter === 'all' || (status[p.id] || 'none') === dfilter;
    const inSource = p => dsec === 'all' || SOURCE(p) === dsec;
    const sub = $('#dsub');
    const dupTag = i => {
      const fam = PROJECT[P[i].id] || '';
      if (!fam || !SIBLING[i].length) return '';
      const nums = SIBLING[i].map(s => P.indexOf(s) + 1).join(', #');
      return `<span class="dup">same <b>${esc(fam)}</b> project · also #${nums}</span>`;
    };

    d.innerHTML = '';
    let shown = 0;

    if (!q) {
      /* no query → classic grouped browser */
      SECTIONS.forEach(sec => {
        const rows = [];
        P.forEach((p, i) => {
          if (p.section !== sec || !inStatus(p) || !inSource(p)) return;
          const st = status[p.id];
          const b = document.createElement('button');
          b.className = 'it' + (i === idx ? ' active' : '');
          b.innerHTML = `${st ? `<span class="mk ${MARK[st]}">${stMark(st)}</span>` : ''}` +
                        `${i + 1}. ${esc(p.title)}<small>${p.label} · ${p.platform}</small>` + dupTag(i);
          b.onclick = () => { go(i); closeDrawer(); };
          rows.push(b);
        });
        if (!rows.length) return;
        shown += rows.length;
        const sc = counts(P.filter(p => p.section === sec));
        const h = document.createElement('div'); h.className = 'sec';
        h.innerHTML = `<span>${sec}</span><em>${sc.solved}/${P.filter(p => p.section === sec).length} solved</em>`;
        d.appendChild(h);
        rows.forEach(r => d.appendChild(r));
      });
      if (sub) sub.textContent = `${shown} of ${P.length} problems`;
      if (!shown) { if (sub) sub.textContent = 'no problems match those filters'; d.innerHTML = '<div class="none">Nothing matches those filters.</div>'; }
    } else {
      /* query → ranked results, best matches first */
      const res = [];
      P.forEach((p, i) => {
        if (!inStatus(p) || !inSource(p)) return;
        const r = score(p, i, toks, ph);
        if (r) res.push({i, ...r});
      });
      res.sort((a, b) => (b.sc - a.sc) || (a.i - b.i));
      if (sub) sub.textContent = `${res.length} match${res.length === 1 ? '' : 'es'} for “${esc(q)}”`;
      if (!res.length) {
        d.innerHTML = '<div class="none">No problem matches that. Try one word at a time, or a function name.</div>';
      }
      res.forEach(({i, bits}) => {
        const p = P[i]; const st = status[p.id];
        const b = document.createElement('button');
        b.className = 'it' + (i === idx ? ' active' : '');
        const sn = snippet(i, bits);
        b.innerHTML =
          `${st ? `<span class="mk ${MARK[st]}">${stMark(st)}</span>` : ''}` +
          `${i + 1}. ${hl(p.title, bits)}<small>${p.label} · ${p.platform}</small>` +
          (sn ? `<span class="hit">${sn}</span>` : '') + dupTag(i);
        b.onclick = () => { go(i); closeDrawer(); };
        d.appendChild(b);
      });
    }

    document.querySelectorAll('#drawer .filters button').forEach(b =>
      b.setAttribute('aria-pressed',
        b.dataset.f != null ? b.dataset.f === dfilter : b.dataset.s === dsec));
  }

  function openDrawer() {
    if ($('#drawer')) return;
    const scrim = document.createElement('div'); scrim.id = 'scrim'; scrim.onclick = closeDrawer;
    const d = document.createElement('div'); d.id = 'drawer';
    d.innerHTML =
      `<h2>All problems</h2><p class="sub" id="dsub">${P.length} items · search matches every word, ranked by relevance</p>` +
      `<div class="pbar" id="pbar"></div><div class="legend" id="legend"></div>` +
      `<div class="tools">` +
        `<input id="dq" placeholder="Search title, statement, function name, your notes…" autocomplete="off">` +
        `<div class="filters">` +
          `<button data-f="all">All</button>` +
          `<button data-f="none">Not started</button>` +
          `<button data-f="attempt">Attempted</button>` +
          `<button data-f="solved">Solved</button>` +
          `<button data-f="review">Review</button>` +
        `</div>` +
        `<div class="filters srcf">` +
          `<button data-s="all">Any source</button>` +
          `<button data-s="amazon">Amazon</button>` +
          `<button data-s="siemens">Siemens</button>` +
          `<button data-s="fastprep">FastPrep</button>` +
        `</div>` +
      `</div>` +
      `<div id="drawerList"></div>` +
      `<div class="dtools">` +
        `<button id="expBtn">Export progress</button>` +
        `<button id="impBtn">Import progress</button>` +
      `</div>`;
    document.body.append(scrim, d);

    const qi = $('#dq');
    qi.value = dq;
    qi.oninput = () => { dq = qi.value; renderDrawer(); };
    document.querySelectorAll('#drawer .filters button').forEach(b =>
      b.onclick = () => {
        if (b.dataset.f != null) dfilter = b.dataset.f; else dsec = b.dataset.s;
        renderDrawer();
      });
    $('#expBtn').onclick = exportProgress;
    $('#impBtn').onclick = importProgress;
    renderDrawer();
    qi.focus();
  }
  function closeDrawer() { const d = $('#drawer'), s = $('#scrim'); d && d.remove(); s && s.remove(); }
  $('#burger').onclick = () => ($('#drawer') ? closeDrawer() : openDrawer());

  /* ---------- export / import (everything lives in localStorage — back it up) ---------- */
  function exportProgress() {
    const out = {};
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k.startsWith(KEY)) out[k.slice(KEY.length)] = localStorage.getItem(k);
    }
    const blob = new Blob([JSON.stringify({v:1, saved:new Date().toISOString(), data:out}, null, 1)],
                          {type:'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'amazon-oa-progress-' + new Date().toISOString().slice(0, 10) + '.json';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }
  function importProgress() {
    const inp = document.createElement('input');
    inp.type = 'file'; inp.accept = 'application/json,.json';
    inp.onchange = () => {
      const f = inp.files[0]; if (!f) return;
      const r = new FileReader();
      r.onload = () => {
        let j; try { j = JSON.parse(r.result); } catch (e) { alert('Not a valid export file.'); return; }
        if (!j || !j.data) { alert('Not a valid export file.'); return; }
        if (!confirm('Replace all code, notes and progress in this browser with the file?')) return;
        for (let i = localStorage.length - 1; i >= 0; i--) {
          const k = localStorage.key(i);
          if (k.startsWith(KEY)) localStorage.removeItem(k);
        }
        Object.keys(j.data).forEach(k => localStorage.setItem(KEY + k, j.data[k]));
        location.reload();
      };
      r.readAsText(f);
    };
    inp.click();
  }

  const BOOKMARK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ddd" stroke-width="1.8"><path d="M6 3h12v18l-6-4.5L6 21z"/></svg>';

  function render(topts) {
    const p = P[idx];
    $('#topTitle').innerHTML = `<b>${p.section}</b> &nbsp;·&nbsp; ${p.label}`;
    $('#eyebrow').textContent = p.platform.startsWith('HackerEarth') ? 'Problem' : 'Question Description';
    $('#chipPlat').textContent = p.platform;
    $('#score').textContent = p.score || '';
    $('#chipShots').style.display = p.images.length ? '' : 'none';

    const shots = p.images.length ? `
      <div class="shots hidden" id="shots">
        <h3>Original screenshots</h3>
        ${p.images.map(f => `<img loading="lazy" src="../images/${encodeURIComponent(f)}" alt="${f}" title="${f}">`).join('')}
      </div>` : '';

    $('#pbody').innerHTML =
      (() => {
        const bare = p.label === 'Field notes' || p.label === 'Question Description'
                  || p.label === 'Attempt post-mortem';
        return `<div class="qtitle">${BOOKMARK}<h1>${bare ? p.title : p.label}</h1></div>` +
               (bare ? '' : `<div class="qsub">${p.title}</div>`);
      })() +
      p.body + shots;

    $('#left').scrollTop = 0;
    document.querySelectorAll('#pbody .bar').forEach(b => {
      b.onclick = () => b.classList.toggle('open');
    });
    document.querySelectorAll('#shots img').forEach(im => {
      im.onclick = () => lightbox(im.src);
    });
    document.querySelectorAll('#pbody .fig img[data-full]').forEach(el => {
      el.onclick = () => lightbox(el.dataset.full);
    });
    document.querySelectorAll('#pbody .vshot img').forEach(im => {
      im.onclick = () => lightbox(im.src);
    });

    timerLoad(p, topts); tick();
    loadCode(); loadNotes(); renderStatusBtns(); renderRail(); renderDrawer();
    syncRunBtn(); showTests(false);            // results belong to the problem you ran
    save('idx', idx);
  }

  function go(i, topts) {
    flushSaves();
    idx = (i + P.length) % P.length;
    if (location.hash.slice(1) !== P[idx].id) location.hash = P[idx].id;
    render(topts);
  }
  window.addEventListener('beforeunload', flushSaves);
  window.addEventListener('hashchange', () => {
    const j = P.findIndex(p => p.id === location.hash.slice(1));
    if (j >= 0 && j !== idx) { flushSaves(); idx = j; render(); }
  });

  /* ---------- misc UI ---------- */
  $('#chipShots').onclick = () => {
    const s = $('#shots'); if (!s) return;
    s.classList.toggle('hidden');
    $('#chipShots').textContent = s.classList.contains('hidden') ? 'Show original screenshots' : 'Hide original screenshots';
    if (!s.classList.contains('hidden')) s.scrollIntoView({behavior:'smooth'});
  };
  $('#prev').onclick = () => go(idx - 1);
  $('#next').onclick = () => go(idx + 1);
  $('#reset').onclick = () => { if (confirm('Discard your code for this problem and reload the stub?')) { setCode(stub(P[idx])); onEdit(); } };
  $('#copy').onclick = () => { navigator.clipboard.writeText(getCode()); $('#copy').textContent = 'Copied'; setTimeout(() => $('#copy').textContent = 'Copy', 1200); };

  function lightbox(src) {
    const d = document.createElement('div'); d.id = 'lightbox';
    d.innerHTML = `<img src="${src}">`;
    d.onclick = () => d.remove();
    document.body.appendChild(d);
  }

  /* resizer */
  (function () {
    const drag = $('#drag'), left = $('#left'), main = $('#main');
    let on = false;
    drag.onmousedown = (e) => { on = true; e.preventDefault(); document.body.style.userSelect = 'none'; };
    window.addEventListener('mousemove', (e) => {
      if (!on) return;
      const r = main.getBoundingClientRect();
      const pct = Math.min(78, Math.max(22, (e.clientX - r.left) / r.width * 100));
      left.style.flex = `0 0 ${pct}%`;
    });
    window.addEventListener('mouseup', () => { on = false; document.body.style.userSelect = ''; if (cm) cm.refresh(); });
  })();

  /* keyboard */
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { closeDrawer(); const l = $('#lightbox'); l && l.remove(); }
    if (e.ctrlKey && e.altKey && (e.key === 'v' || e.key === 'V')) {   // works inside the editor too
      e.preventDefault(); vimOn = !vimOn; applyVim(true); return;
    }
    if (e.ctrlKey && e.altKey && (e.key === 'r' || e.key === 'R')) {
      e.preventDefault(); relNo = !relNo; applyRel(true); return;
    }
    const inEditor = e.target.closest('.CodeMirror, textarea, input, select');
    if (inEditor) return;
    if (e.key === '/') { e.preventDefault(); openDrawer(); return; }
    if (e.key === 'd') { drill(); return; }
    if (e.key === '+' || e.key === '=') { fsz += 1; applyFsz(); return; }
    if (e.key === '-') { fsz -= 1; applyFsz(); return; }
    if (e.key === 'ArrowRight' || e.key === 'j') go(idx + 1);
    if (e.key === 'ArrowLeft' || e.key === 'k') go(idx - 1);
  });

  const h = P.findIndex(p => p.id === location.hash.slice(1));
  if (h >= 0) idx = h; else location.hash = P[idx].id;
  render();
  pullState();          // sync from server (code/notes/progress survive restarts)
})();
