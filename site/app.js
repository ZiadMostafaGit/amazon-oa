(function () {
  const P = window.PROBLEMS;
  const KEY = 'amzoa:';
  const $ = (s) => document.querySelector(s);

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
     JSON file through the /api/state endpoint, so code, notes and progress
     survive browser restarts and travel across devices. Offline/nginx-only: no-op. */
  /* Resolve the API path relative to the page (site/api/state) instead of an
     absolute /api/state, so it works when a reverse proxy mounts the app under
     a prefix like /site/ — with an absolute path the proxy never sees it. */
  const API_URL = new URL('api/state', location.href).toString();
  let pushTimer = null;
  function pushState() {
    clearTimeout(pushTimer);
    pushTimer = setTimeout(() => {
      const out = {};
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (k && k.startsWith(KEY)) out[k.slice(KEY.length)] = localStorage.getItem(k);
      }
      fetch(API_URL, {method:'POST', headers:{'Content-Type':'application/json'},
                      body:JSON.stringify(out)}).catch(() => {});
    }, 400);
  }
  function pullState() {
    fetch(API_URL, {cache:'no-store'})
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(data => {
        if (!data || typeof data !== 'object') return;
        const keys = Object.keys(data);
        if (!keys.length) { pushState(); return; }      /* fresh server, seed it */
        let diffs = 0;
        keys.forEach(k => {
          if (localStorage.getItem(KEY + k) !== data[k]) { localStorage.setItem(KEY + k, data[k]); diffs++; }
        });
        for (let i = localStorage.length - 1; i >= 0; i--) {
          const lk = localStorage.key(i);
          if (lk && lk.startsWith(KEY) && !(lk.slice(KEY.length) in data)) {
            localStorage.removeItem(lk); diffs++;
          }
        }
        if (diffs) location.reload();                    /* server differs → reinit from it */
      })
      .catch(() => {});
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

  /* Enter indents after a colon (the mode does that) and, additionally,
     dedents after a statement that ends a block. */
  const BLOCK_EXIT = /^\s*(return|pass|break|continue|raise)\b/;
  function enterKey(c) {
    if (vimCommandMode(c)) return CodeMirror.Pass;
    c.execCommand('newlineAndIndent');
    const pos = c.getCursor();
    if (pos.line === 0) return;
    if (!BLOCK_EXIT.test(c.getLine(pos.line - 1))) return;
    const ind = (c.getLine(pos.line).match(/^ */) || [''])[0].length;
    if (ind >= indentUnit(c)) c.indentLine(pos.line, 'subtract');
  }

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

  function membersOf(base, imports) {
    const mod = imports.alias[base] || base;          // np -> numpy, re -> re
    if (ENV.modules[mod]) return {list: ENV.modules[mod], kind: mod};
    return null;
  }

  function bufferWords(c, skip) {
    const out = new Set(), re = /[A-Za-z_][A-Za-z0-9_]*/g;
    let m; const text = c.getValue();
    while ((m = re.exec(text))) if (m[0] !== skip && m[0].length > 1) out.add(m[0]);
    return out;
  }

  /* Registered as a CodeMirror helper so it is reachable as CodeMirror.hint.python
     (idiomatic, and it makes the completer testable from outside the closure). */
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
    const importCtx = /(^|\n)[ \t]*(import|from)[ \t][\w., \t]*$/.test(beforeWord);

    if (start > 0 && line.charAt(start - 1) === '.') {                  // member access
      let e = start - 1, s2 = e;
      while (s2 && /[\w$.]/.test(line.charAt(s2 - 1))) s2--;
      const base = line.slice(s2, e);
      const mem = membersOf(base, imports) || membersOf(base.split('.').pop(), imports);
      pool = (mem ? mem.list.map(w => [w, mem.kind, 0]) : [])
        .concat(ANY_METHOD.map(w => [w, 'method', mem ? 2 : 0]));
    } else if (importCtx) {                                             // after `import `
      pool = MODULE_NAMES.map(w => [w, 'module', 0]);
    } else {
      pool = PY_KEYWORDS.map(w => [w, 'kw', 0])
        .concat(PY_BUILTINS.map(w => [w, 'builtin', 0]))
        .concat(imports.plain.map(w => [w, 'import', 0]))
        .concat(MODULE_NAMES.map(w => [w, 'module', 2]))
        .concat([...bufferWords(c, word)].map(w => [w, 'local', 1]));
    }

    const seen = new Set(), list = [];
    for (const [w, kind, rank] of pool) {
      if (w === word || seen.has(w) || !w.startsWith(word)) continue;
      seen.add(w);
      list.push({ text: w, kind: kind, rank: rank,
        render(el) {
          el.appendChild(document.createTextNode(w));
          const b = document.createElement('span'); b.className = 'hk'; b.textContent = kind;
          el.appendChild(b);
        } });
    }
    if (!list.length) return null;
    list.sort((x, y) => x.rank - y.rank ||
                        x.text.length - y.text.length ||
                        x.text.localeCompare(y.text));
    return { list: list.slice(0, 50),
             from: CodeMirror.Pos(cur.line, start),
             to:   CodeMirror.Pos(cur.line, cur.ch) };
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
      if (cur.ch - st >= 2) c.showHint({hint: pythonHint, completeSingle: false, closeOnUnfocus: true,
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
  cm ? cm.on('change', onEdit) : ta.addEventListener('input', onEdit);
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
  function timerLoad(p, opts) {
    tState = load('timer:' + p.id, null);
    if (!tState || (opts && opts.reset)) tState = { left: (p.minutes || 30) * 60, running: false };
    if (opts && opts.start) tState.running = true;
    save('timer:' + p.id, tState);
  }
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
  /* plain-text index of each problem, built once, so drawer search covers the statement */
  const HAY = P.map(p => (p.title + ' ' + p.label + ' ' + p.section + ' ' + p.platform + ' ' +
      (p.fn ? p.fn.name : '') + ' ' + p.body.replace(/<[^>]*>/g, ' ')).toLowerCase());

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
  let dq = '', dfilter = 'all';

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

    const q = dq.trim().toLowerCase();
    const match = (p, i) =>
      (dfilter === 'all' || (status[p.id] || 'none') === dfilter) &&
      (!q || HAY[i].includes(q) || (load('notes:' + p.id, '') || '').toLowerCase().includes(q));

    d.innerHTML = '';
    let shown = 0;
    SECTIONS.forEach(sec => {
      const rows = [];
      P.forEach((p, i) => {
        if (p.section !== sec || !match(p, i)) return;
        const st = status[p.id];
        const b = document.createElement('button');
        b.className = 'it' + (i === idx ? ' active' : '');
        b.innerHTML = `${st ? `<span class="mk ${MARK[st]}">${st === 'solved' ? '✓' : st === 'review' ? '↻' : '•'}</span>` : ''}` +
                      `${i + 1}. ${p.title}<small>${p.label} · ${p.platform}</small>`;
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
    if (!shown) d.innerHTML = '<div class="none">Nothing matches that.</div>';

    document.querySelectorAll('#drawer .filters button').forEach(b =>
      b.setAttribute('aria-pressed', b.dataset.f === dfilter));
  }

  function openDrawer() {
    if ($('#drawer')) return;
    const scrim = document.createElement('div'); scrim.id = 'scrim'; scrim.onclick = closeDrawer;
    const d = document.createElement('div'); d.id = 'drawer';
    d.innerHTML =
      `<h2>All problems</h2><p class="sub">${P.length} items · click a status again to clear it</p>` +
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
      b.onclick = () => { dfilter = b.dataset.f; renderDrawer(); });
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
