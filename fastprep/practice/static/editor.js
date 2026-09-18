/* editor.js — the Python editor, lifted from the amazon-oa app.
 *
 * Real tab stops, Python-aware Enter/Backspace, a vim keymap whose o/O opens
 * an indented line like the real thing, relative line numbers, and completion
 * backed by pyenv.js (every builtin, all stdlib module members, the methods of
 * the built-in types).
 *
 * Nothing in here knows about problems, runs or the server: create() takes a
 * textarea and some callbacks and hands back a small handle.
 */
'use strict';

window.PyEditor = (function () {
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

  /* ---------------------------------------------------------------- create */
  function create(textarea, opts) {
    opts = opts || {};
    if (!window.CodeMirror) {                 /* vendored assets missing */
      return {
        cm: null,
        getValue: () => textarea.value,
        setValue: (v) => { textarea.value = v; },
        setReadOnly: (ro) => { textarea.readOnly = !!ro; },
        focus: () => textarea.focus(),
        refresh: () => {},
        setVim: () => false, setRelative: () => false, setFontSize: () => {},
        onModeChange: () => {},
      };
    }

    const cm = CodeMirror.fromTextArea(textarea, {
      theme: 'material-darker', mode: 'python', lineNumbers: true,
      indentUnit: 4, tabSize: 4, indentWithTabs: false, smartIndent: true,
      electricChars: true, autoCloseBrackets: true, matchBrackets: true,
      styleActiveLine: true, lineWrapping: false, showCursorWhenSelecting: true,
      extraKeys: {
        Tab: tabKey, 'Shift-Tab': shiftTabKey, Backspace: backspaceKey, Enter: enterKey,
        'Ctrl-/': 'toggleComment', 'Cmd-/': 'toggleComment',
        'Ctrl-Enter': () => opts.onRun && opts.onRun(),
        'Shift-Ctrl-Enter': () => opts.onScratch && opts.onScratch(),
        'Ctrl-F': 'findPersistent', 'Ctrl-G': 'findNext', 'Shift-Ctrl-G': 'findPrev',
        'Shift-Ctrl-F': 'replace',
        'Ctrl-Space': (c) => c.showHint({hint: pythonHint, completeSingle: false,
                     closeOnUnfocus: true, extraKeys: {Tab: (cm2, h) => h.pick()}}),
        'Shift-Ctrl-K': (c) => c.execCommand('deleteLine'),
        'Alt-Up': (c) => c.execCommand('swapLineUp'),
        'Alt-Down': (c) => c.execCommand('swapLineDown'),
      },
    });

    /* Type-ahead completion: fires on word characters and after a dot, never on
       the first keystroke of a word (too noisy) and never while one is open. */
    cm.on('inputRead', (c, ch) => {
      if (c.state.completionActive) return;
      const t = ch.text && ch.text[0];
      if (!t) return;
      const show = () => c.showHint({hint: pythonHint, completeSingle: false,
                     closeOnUnfocus: true, extraKeys: {Tab: (cm2, h) => h.pick()}});
      if (t === '.') { show(); return; }
      if (!/[A-Za-z_]/.test(t)) return;
      const cur = c.getCursor(), line = c.getLine(cur.line);
      let st = cur.ch;
      while (st && /[\w$]/.test(line.charAt(st - 1))) st--;
      if (cur.ch - st >= 1) show();
    });

    /* --- relative line numbers ---------------------------------------- */
    /* The gutter is repainted by CodeMirror with absolute numbers; only the
       visible copy is rewritten. _lastSet detects a fresh repaint so _abs
       stays correct. */
    let relative = !!opts.relative;
    const patchRel = () => {
      if (!relative) return;
      const cur = cm.getCursor().line + 1;
      cm.display.lineDiv.querySelectorAll('.CodeMirror-linenumber').forEach(el => {
        const t = el.textContent;
        if (el._lastSet !== t) {
          const n = parseInt(t, 10);
          if (!isNaN(n) && /^\d+$/.test(t)) el._abs = n;
        }
        if (el._abs == null) return;
        const d = el._abs - cur;
        const out = d === 0 ? String(el._abs) : String(Math.abs(d));
        el.textContent = out;
        el._lastSet = out;
      });
    };
    const restoreRel = () => {
      cm.display.lineDiv.querySelectorAll('.CodeMirror-linenumber').forEach(el => {
        if (el._abs != null) el.textContent = String(el._abs);
        delete el._lastSet; delete el._abs;
      });
    };
    cm.on('cursorActivity', patchRel);
    cm.on('changes', patchRel);
    cm.on('scroll', patchRel);

    if (opts.onChange) {
      cm.on('change', (c, ch) => { if (!ch || ch.origin !== 'setValue') opts.onChange(); });
    }
    if (opts.onModeChange && CodeMirror.Vim) {
      cm.on('vim-mode-change', (e) => opts.onModeChange(e.mode + (e.subMode ? ' ' + e.subMode : '')));
    }

    const handle = {
      cm: cm,
      getValue: () => cm.getValue(),
      setValue: (v) => { cm.setValue(v == null ? '' : v); },
      setReadOnly: (ro) => cm.setOption('readOnly', ro ? 'nocursor' : false),
      focus: () => cm.focus(),
      refresh: () => setTimeout(() => cm.refresh(), 0),
      setCursor: (pos) => { try { cm.setCursor(pos); } catch (e) {} },
      getCursor: () => cm.getCursor(),
      setVim: (on) => { cm.setOption('keyMap', on ? 'vim' : 'default'); return on; },
      setRelative: (on) => { relative = !!on; on ? patchRel() : restoreRel(); return relative; },
      setFontSize: (px) => {
        cm.getWrapperElement().style.fontSize = px + 'px';
        setTimeout(() => cm.refresh(), 0);
      },
    };
    if (opts.vim) handle.setVim(true);
    handle.setRelative(relative);
    handle.setFontSize(opts.fontSize || 14);
    return handle;
  }

  return { create: create, hint: pythonHint };
})();
