/* FastPrep practice - browse, read, and run against the visible examples.
 *
 * No framework and no build step: the statements are already HTML, the data is
 * already local, and one file is easier to read than a toolchain. */
'use strict';

const $ = (s, r) => (r || document).querySelector(s);
const el = (tag, cls, txt) => { const n = document.createElement(tag);
  if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; };
const esc = (s) => String(s == null ? '' : s)
  .replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* ------------------------------------------------------------------ state */
const MULTI = ['company', 'difficulty', 'platform', 'format', 'stage', 'topic',
               'employment', 'role'];
const SINGLE = ['q', 'sort', 'dir', 'seenFrom', 'seenTo', 'seenOnFrom', 'seenOnTo',
                'minSeen', 'maxSeen', 'status'];
const FLAGS = ['hasImages', 'bookmarked', 'hasNotes', 'hasSolution'];

const state = {
  filters: Object.fromEntries(MULTI.map(k => [k, new Set()])),
  q: '', sort: 'recent', dir: '', seenFrom: '', seenTo: '', seenOnFrom: '', seenOnTo: '',
  minSeen: '', maxSeen: '', status: '', hasImages: false, bookmarked: false, hasNotes: false,
  hasSolution: false, solutionStats: null,
  offset: 0, limit: 50, total: 0, items: [], current: null, facets: null,
  env: null, lang: null, dirty: false,
  editor: null, editorKey: '', buffers: {},
  vim: localStorage.getItem('fp:vim') === '1',
  relno: localStorage.getItem('fp:relno') !== '0',
  fontSize: parseInt(localStorage.getItem('fp:fs') || '14', 10),
  showCaseForm: false,
  topic: '', studyOpen: false, topics: null,
};

const remember = (k, v) => { try { localStorage.setItem('fp:' + k, v); } catch (e) {} };

function queryString(extra) {
  const p = new URLSearchParams();
  MULTI.forEach(k => state.filters[k].forEach(v => p.append(k, v)));
  SINGLE.forEach(k => { if (state[k]) p.set(k, state[k]); });
  FLAGS.forEach(k => { if (state[k]) p.set(k, '1'); });
  Object.entries(extra || {}).forEach(([k, v]) => p.set(k, v));
  return p.toString();
}

/* The app must work wherever it is mounted: served at /, or behind a proxy at
   /site/, or anywhere else. So every request resolves against the page itself
   rather than the domain root - a leading slash would leave the mount point. */
const url = (path) => new URL(String(path).replace(/^\//, ''), document.baseURI).toString();

async function api(path, opts) {
  const r = await fetch(url(path), opts);
  const body = await r.json().catch(() => ({ error: r.statusText }));
  if (!r.ok) throw new Error(body.error || ('HTTP ' + r.status));
  return body;
}

/* ------------------------------------------------------------- url syncing */
function pushUrl() {
  const extra = state.current ? { id: state.current.id } : {};
  /* 'topic' is already a bank-tag filter, so the study space uses its own key */
  if (state.topic) extra.study = state.topic;
  else if (state.studyOpen) extra.study = 'all';
  const qs = queryString(extra);
  history.replaceState(null, '', qs ? '?' + qs : location.pathname);
}
function readUrl() {
  const p = new URLSearchParams(location.search);
  MULTI.forEach(k => p.getAll(k).forEach(v => state.filters[k].add(v)));
  SINGLE.forEach(k => { if (p.get(k)) state[k] = p.get(k); });
  FLAGS.forEach(k => { if (p.get(k)) state[k] = true; });
  const study = p.get('study') || '';
  state.wantTopic = study && study !== 'all' ? study : '';
  state.wantTopicList = study === 'all';
  return p.get('id');
}

/* ----------------------------------------------------------------- filters */
const FACET_TITLES = {
  stage: 'Stage', difficulty: 'Difficulty', company: 'Company', topic: 'Topic',
  employment: 'Employment type', role: 'Target role', platform: 'Assessment platform',
  format: 'Practice format',
};
const FACET_ORDER = ['stage', 'difficulty', 'company', 'topic', 'employment',
                     'role', 'platform', 'format'];
const UNSET = '__unset__';
const optLabel = (v) => v.value === UNSET ? '(not set)' : String(v.value);

function facetBlock(key, values) {
  const open = state.filters[key].size > 0 || ['stage', 'difficulty'].includes(key);
  const d = el('details', 'facet');
  d.open = open;
  const sum = el('summary');
  sum.append(el('span', null, FACET_TITLES[key] || key));
  const badge = el('span', 'n', state.filters[key].size ? String(state.filters[key].size) : '');
  sum.append(badge);
  d.append(sum);

  const box = el('div', 'opts');
  let filterInput = null;
  if (values.length > 12) {
    filterInput = el('input');
    filterInput.type = 'text';
    filterInput.placeholder = 'filter ' + (FACET_TITLES[key] || key).toLowerCase() + '…';
    d.append(filterInput);
  }
  const render = (needle) => {
    box.textContent = '';
    const n = (needle || '').toLowerCase();
    values.filter(v => !n || optLabel(v).toLowerCase().includes(n))
          .slice(0, 400)
          .forEach(v => {
      const lab = el('label', 'opt');
      const cb = el('input'); cb.type = 'checkbox'; cb.checked = state.filters[key].has(v.value);
      cb.onchange = () => {
        cb.checked ? state.filters[key].add(v.value) : state.filters[key].delete(v.value);
        badge.textContent = state.filters[key].size ? String(state.filters[key].size) : '';
        reload();
      };
      lab.append(cb, el('span', v.unset ? 'unset' : null, optLabel(v)),
                 el('span', 'n', String(v.count)));
      box.append(lab);
    });
  };
  render('');
  if (filterInput) filterInput.oninput = () => render(filterInput.value);
  d.append(box);
  return d;
}

function renderFilters() {
  const host = $('#facets');
  host.textContent = '';
  const f = state.facets;

  FACET_ORDER.forEach(k => { if (f[k] && f[k].length) host.append(facetBlock(k, f[k])); });

  /* dates + counts */
  const d = el('details', 'facet'); d.open = !!(state.seenFrom || state.seenTo ||
    state.seenOnFrom || state.seenOnTo || state.minSeen);
  const s = el('summary'); s.append(el('span', null, 'When it was seen')); d.append(s);
  const mk = (label, key, type) => {
    const wrap = el('div');
    wrap.append(el('div', 'hint', label));
    const i = el('input'); i.type = type; i.value = state[key] || '';
    i.onchange = () => { state[key] = i.value; reload(); };
    wrap.append(i); return wrap;
  };
  const r1 = el('div', 'row2');
  r1.append(mk('newest sighting from', 'seenFrom', 'date'),
            mk('to', 'seenTo', 'date'));
  const r2 = el('div', 'row2');
  r2.append(mk('seen on any date from', 'seenOnFrom', 'date'),
            mk('to', 'seenOnTo', 'date'));
  const r3 = el('div', 'row2');
  r3.append(mk('seen at least N times', 'minSeen', 'number'),
            mk('and at most', 'maxSeen', 'number'));
  d.append(r1, r2, r3);
  d.append(el('div', 'hint', 'The bank spans ' + (f.meta.earliest || '?') + ' to ' +
                             (f.meta.latest || '?') + '.'));
  host.append(d);

  /* my progress */
  const p = el('details', 'facet'); p.open = !!(state.status || state.bookmarked || state.hasNotes);
  const ps = el('summary'); ps.append(el('span', null, 'My progress')); p.append(ps);
  const opts = el('div', 'opts');
  [['', 'any'], ['none', 'not started'], ['attempted', 'attempted'],
   ['solved', 'solved'], ['review', 'review']].forEach(([v, label]) => {
    const lab = el('label', 'opt');
    const rb = el('input'); rb.type = 'radio'; rb.name = 'status'; rb.checked = state.status === v;
    rb.onchange = () => { state.status = v; reload(); };
    const n = (f.progress || {})[v === '' ? '' : v];
    lab.append(rb, el('span', null, label), el('span', 'n', n != null ? String(n) : ''));
    opts.append(lab);
  });
  [['bookmarked', 'bookmarked only'], ['hasNotes', 'has notes'],
   ['hasImages', 'has source screenshots'],
   ['hasSolution', 'has a reference solution']].forEach(([key, label]) => {
    const lab = el('label', 'opt');
    const cb = el('input'); cb.type = 'checkbox'; cb.checked = !!state[key];
    cb.onchange = () => { state[key] = cb.checked; reload(); };
    lab.append(cb, el('span', null, label));
    if (key === 'hasImages') lab.append(el('span', 'n', String(f.meta.withImages)));
    if (key === 'hasSolution' && f.meta.withSolutions != null) {
      lab.append(el('span', 'n', String(f.meta.withSolutions)));
    }
    opts.append(lab);
  });
  p.append(opts);
  host.append(p);
}

function renderChips() {
  const host = $('#activeChips');
  host.textContent = '';
  const add = (label, value, clear) => {
    const c = el('span', 'chip');
    c.append(el('b', null, label + ':'), el('span', null, String(value)));
    const x = el('button', null, '×'); x.onclick = () => { clear(); reload(); };
    c.append(x); host.append(c);
  };
  MULTI.forEach(k => state.filters[k].forEach(v =>
    add(FACET_TITLES[k] || k, v === UNSET ? '(not set)' : v,
        () => state.filters[k].delete(v))));
  [['q', 'search'], ['seenFrom', 'seen ≥'], ['seenTo', 'seen ≤'],
   ['seenOnFrom', 'any sighting ≥'], ['seenOnTo', 'any sighting ≤'],
   ['minSeen', 'seen ≥ n times'], ['maxSeen', 'seen ≤ n times'],
   ['status', 'status']].forEach(([k, label]) => {
    if (state[k]) add(label, state[k], () => { state[k] = ''; if (k === 'q') $('#q').value = ''; });
  });
  FLAGS.forEach(k => { if (state[k]) add(k, 'yes', () => { state[k] = false; }); });
}


/* ------------------------------------------------------------ custom cases */
function renderCases() {
  const d = state.current;
  const host = $('#casesHost');
  if (!host) return;
  host.textContent = '';
  const params = ((d.cases && d.cases[0] ? d.cases[0].inputs : []) || []);
  const generated = d.generatedCases || [];

  /* what this problem actually has to test against */
  const tally = el('div', 'hint');
  tally.innerHTML =
    '<b>' + (d.cases || []).length + '</b> published example' +
    ((d.cases || []).length === 1 ? '' : 's') +
    (generated.length ? ' · <b>' + generated.length + '</b> generated' : '') +
    ((d.customCases || []).length ? ' · <b>' + (d.customCases || []).length + '</b> of yours' : '') +
    '. ▶ Run tests runs all of them.';
  host.append(tally);

  if (generated.length) {
    const box = el('details', 'disclosure');
    const sum = el('summary');
    sum.append(el('span', 'stamp pending', 'generated'),
               el('span', null, generated.length + ' extra cases'),
               el('span', 'hint', 'mutations of this problem\u2019s own examples, ' +
                  'answered by the verified reference solution'));
    box.append(sum);
    const inner = el('div', 'inner');
    inner.append(el('div', 'hint',
      'These encode the reference solution\u2019s behaviour, not a judge\u2019s. They are useful ' +
      'for catching off-by-one errors the single published example cannot.'));
    generated.slice(0, 12).forEach(c => {
      const row = el('div', 'casecard');
      const kv = el('div', 'kv');
      (c.inputs || []).forEach(i => {
        kv.append(el('div', 'k', (i.name || '?')), el('div', 'v', i.rawValue));
      });
      kv.append(el('div', 'k', '→ expected'), el('div', 'v', c.expectedRaw));
      row.append(kv);
      inner.append(row);
    });
    if (generated.length > 12) {
      inner.append(el('div', 'hint', '…and ' + (generated.length - 12) + ' more.'));
    }
    box.append(inner);
    host.append(box);
  }

  if (d.practiceFormat === 'tabular') {
    host.append(el('div', 'hint',
      'Custom cases are for algorithm problems; a tabular problem runs against its own visible cases.'));
    return;
  }

  (d.customCases || []).forEach(c => {
    const row = el('div', 'casecard');
    const grow = el('div', 'grow');
    const kv = el('div', 'kv');
    (c.inputs || []).forEach(i => {
      kv.append(el('div', 'k', (i.name || '?') + ' (' + (i.type || '?') + ')'),
                el('div', 'v', i.rawValue));
    });
    kv.append(el('div', 'k', '→ expected'),
              el('div', 'v', c.expectedRaw || '(none — just show what my code returns)'));
    grow.append(kv);
    if (c.note) grow.append(el('div', 'hint', c.note));
    const del = el('button', 'btn ghost', 'Delete');
    del.onclick = async () => {
      await api('api/cases/' + encodeURIComponent(d.id), {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'delete', caseId: c.caseId }),
      });
      const fresh = await api('api/problems/' + encodeURIComponent(d.id));
      state.current.customCases = fresh.customCases;
      renderCases(); paintMyCases();
    };
    row.append(grow, del);
    host.append(row);
  });

  if (!state.showCaseForm) {
    const add = el('button', 'btn', '＋ Add a test case');
    add.disabled = !params.length;
    add.title = params.length ? '' : 'This problem declares no inputs to vary';
    add.onclick = () => { state.showCaseForm = true; renderCases(); };
    host.append(add);
    if (!(d.customCases || []).length) {
      host.append(el('div', 'hint',
        'Your own cases run alongside the published examples and are kept in progress.db.'));
    }
    return;
  }

  const form = el('div', 'caseform');
  const fields = params.map(p => {
    const lab = el('label', null, p.name + '  (' + p.type + ')');
    const inp = el('input');
    inp.value = p.rawValue || '';
    inp.placeholder = p.rawValue || '';
    form.append(lab, inp);
    return { name: p.name, type: p.type, input: inp };
  });
  const expLab = el('label', null, 'expected output  (leave empty to just see what you return)');
  const exp = el('input');
  exp.placeholder = (d.cases && d.cases[0] ? d.cases[0].expectedRaw : '') || '';
  const noteLab = el('label', null, 'note (optional)');
  const note = el('input');
  form.append(expLab, exp, noteLab, note);
  form.append(el('div', 'hint',
    'Values use the same notation as the examples above: JSON for arrays, quotes for strings.'));
  const bar = el('div', 'rowbtns');
  const save = el('button', 'btn primary', 'Add case');
  save.onclick = async () => {
    const payload = {
      action: 'add',
      inputs: fields.map(f => ({ name: f.name, type: f.type, rawValue: f.input.value })),
      expected: exp.value.trim(), note: note.value.trim(),
    };
    try {
      await api('api/cases/' + encodeURIComponent(d.id), {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
    } catch (e) { alert(e.message); return; }
    const fresh = await api('api/problems/' + encodeURIComponent(d.id));
    state.current.customCases = fresh.customCases;
    state.showCaseForm = false;
    renderCases(); paintMyCases();
  };
  const cancel = el('button', 'btn', 'Cancel');
  cancel.onclick = () => { state.showCaseForm = false; renderCases(); };
  bar.append(save, cancel);
  form.append(bar);
  host.append(form);
}

/* Adding or deleting a case changes exactly one thing in the workbench: whether
   `My cases` has anything to run. Re-rendering the whole workbench for that
   threw the editor away and built a new one from the last copy the SERVER had
   - so a paste that had not been saved yet came back as the older version, out
   of nowhere, because you added a test case. Repaint the button instead. */
function paintMyCases() {
  const btn = $('#myCasesBtn');
  if (!btn) return;
  const n = ((state.current || {}).customCases || []).length;
  btn.disabled = !btn.dataset.runnable || !n;
  btn.title = n ? 'Run only the cases you added' : 'Add a case on the left first';
}

/* -------------------------------------------------------- stored solution */
function renderSolution() {
  const d = state.current;
  const host = $('#solutionHost');
  if (!host) return;
  host.textContent = '';
  const sol = d.solution;
  if (!sol) {
    host.append(el('div', 'hint',
      'No reference solution is stored for this problem yet. The bank ships none — ' +
      'the ones here were written and checked against each problem\u2019s visible examples.'));
    return;
  }
  const box = el('details', 'disclosure');
  const sum = el('summary');
  const badge = el('span', 'stamp' + (sol.verified ? '' : ' pending'),
                   sol.verified ? 'verified ' + (sol.cases || '') : 'unverified');
  sum.append(badge, el('span', null, 'Reference solution'),
             el('span', 'hint', sol.verified
               ? 'passes every visible example — open only when you want it spoiled'
               : 'stored but not confirmed against the examples'));
  box.append(sum);
  const inner = el('div', 'inner');
  const pre = el('pre'); pre.textContent = sol.code;
  const bar = el('div', 'rowbtns');
  const load = el('button', 'btn ghost', 'Load into the editor');
  load.onclick = () => { if (state.editor) { state.editor.setValue(sol.code); state.editor.focus(); } };
  bar.append(load, el('span', 'spacer'),
             el('span', 'hint', sol.checkedAt ? 'checked ' + sol.checkedAt : ''));
  inner.append(bar, pre);
  box.append(inner);
  host.append(box);
}

/* ------------------------------------------------------------- persistence */
/* Your code, notes and test cases are server-side state. Three rules make that
 * trustworthy:
 *   · what gets saved is captured WHEN YOU TYPE, not when the debounce fires -
 *     otherwise switching problems mid-debounce writes your code onto the
 *     problem you just left;
 *   · anything still pending is flushed before navigating away and on page
 *     hide, with sendBeacon, which survives unload where fetch does not;
 *   · the header says saved / saving / not saved, so you never have to guess.
 */
const saver = {
  pending: {},          // key -> {id, body}; one slot per problem+kind
  timer: null,

  queue(key, id, body, delay) {
    this.pending[key] = { path: 'api/progress/' + encodeURIComponent(id), body: body };
    this.paint('saving');
    clearTimeout(this.timer);
    this.timer = setTimeout(() => this.flush(), delay == null ? 600 : delay);
  },

  async flush() {
    clearTimeout(this.timer);
    const items = Object.entries(this.pending);
    if (!items.length) return true;
    this.pending = {};
    let ok = true;
    for (const [key, item] of items) {
      try {
        await api(item.path, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item.body),
        });
      } catch (e) {
        ok = false;
        this.pending[key] = item;            // keep it and try again
      }
    }
    this.paint(ok ? 'saved' : 'failed');
    if (!ok) setTimeout(() => this.flush(), 4000);
    return ok;
  },

  flushSync() {
    clearTimeout(this.timer);
    const items = Object.values(this.pending);
    this.pending = {};
    if (!items.length || !navigator.sendBeacon) return;
    items.forEach(item => {
      try {
        navigator.sendBeacon(url(item.path),
          new Blob([JSON.stringify(item.body)], { type: 'application/json' }));
      } catch (e) {}
    });
  },

  /* the study space saves the same way, to its own endpoint */
  queueTo(key, path, body, delay) {
    this.pending[key] = { path: path, body: body };
    this.paint('saving');
    clearTimeout(this.timer);
    this.timer = setTimeout(() => this.flush(), delay == null ? 600 : delay);
  },

  paint(name) {
    const box = $('#savestate');
    if (!box) return;
    box.hidden = false;
    box.className = 'savestate ' + name;
    box.textContent = name === 'saving' ? 'saving…'
      : name === 'failed' ? 'not saved — retrying' : 'saved';
  },
};

window.addEventListener('beforeunload', () => saver.flushSync());
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') saver.flushSync();
});

/* The sandbox badge. Three tiers, because there are three: the full one, the
   one on a machine that will not let the sandbox have its own network
   namespace, and no sandbox at all. Every run reports which one ran it, so a
   demotion that happens while the app is up still reaches this badge. */
const SANDBOX_LABEL = {
  'bubblewrap': 'sandboxed',
  'bubblewrap-shared-net': 'sandboxed · shared network',
  'subprocess': 'limited sandbox',
};

function paintEnv(kind, note) {
  const env = state.env || {};
  const box = $('#env');
  if (!box || !kind) return;
  box.textContent = SANDBOX_LABEL[kind] || kind;
  box.classList.toggle('warn', kind !== 'bubblewrap');
  box.title = (note ? note + '. ' : '') +
    env.wallTimeout + 's wall, ' + env.cpuSeconds + 's CPU, ' + env.memoryMB + ' MB' +
    (env.java ? '' : '. No JDK, so Java is read-only') +
    (env.pandas ? '' : '. No pandas, so pandas is read-only') + '.';
  if (state.env) { state.env.sandbox = kind; if (note) state.env.sandboxNote = note; }
}

/* A run that came back from a different sandbox than the badge claims means the
   server re-worked out what this machine allows. Say so where it is visible. */
function noteSandbox(out) {
  if (out && out.sandbox && state.env && out.sandbox !== state.env.sandbox)
    paintEnv(out.sandbox, out.sandboxNote);
}

/* bwrap failing is not your code failing, and must not be dressed up as it. */
function sandboxFailure(out, results) {
  if (!out || !out.sandboxError) return false;
  const box = el('div', 'case fail');
  box.append(el('div', 'case-head', '✗ the sandbox could not start'));
  box.append(el('div', 'hint',
    'Your code never ran, and nothing is wrong with it. This machine would not ' +
    'let the runner build the namespaces it isolates your code with. The server ' +
    'has re-checked what is allowed here — run it again and it will use the best ' +
    'sandbox this machine does allow, and the badge in the header will say which.'));
  const pre = el('pre'); pre.textContent = out.error; box.append(pre);
  results.append(box);
  $('#verdict').innerHTML = '<span class="no">sandbox failed</span>';
  return true;
}

function scheduleSave() {
  const d = state.current;
  if (!d || !state.editor) return;
  const code = state.editor.getValue();
  state.buffers[d.id + ':' + state.lang] = code;
  saver.queue('code:' + d.id + ':' + state.lang, d.id,       // captured now
              { language: state.lang, code: code });
}

function scheduleNotes(text) {
  const d = state.current;
  if (!d) return;
  saver.queue('notes:' + d.id, d.id, { notes: text });
}

/* ------------------------------------------------------- results (drawer) */
function resultRow(p, index) {
  const b = el('button', 'result' + (state.current && state.current.id === p.id ? ' active' : ''));
  b.dataset.id = p.id;

  const title = el('div', 'title');
  title.append(el('span', 'num', '#' + (index + 1)));
  const pr = p.progress || {};
  if (pr.status) title.append(Object.assign(el('span', 'dot ' + pr.status), {title: pr.status}));
  else if (pr.bookmarked) title.append(Object.assign(el('span', 'dot bookmarked'), {title: 'bookmarked'}));
  title.append(el('span', null, p.title || p.id));
  b.append(title);

  const sub = el('div', 'sub');
  if (p.company) sub.append(el('span', 'tag company', p.company));
  if (p.difficulty) sub.append(el('span', 'tag ' + p.difficulty, p.difficulty));
  (p.stages || []).slice(0, 2).forEach(s => sub.append(el('span', 'tag stage', s)));
  if (p.format === 'tabular') sub.append(el('span', 'tag plain', 'SQL'));
  if (p.seenCount > 1) sub.append(el('span', 'tag count', 'seen ' + p.seenCount + '×'));
  sub.append(el('span', 'when', p.lastSeenMax || ''));
  b.append(sub);

  b.onclick = () => { openProblem(p.id); closeDrawer(); };
  return b;
}

function renderList(append) {
  const host = $('#list');
  if (!append) host.textContent = '';
  if (!state.items.length && !append) {
    host.append(el('div', 'nothing', 'Nothing matches those filters.'));
  }
  const from = append ? host.querySelectorAll('.result').length : 0;
  state.items.slice(from).forEach((p, i) => host.append(resultRow(p, from + i)));

  $('#count').innerHTML = '<b>' + state.total.toLocaleString() + '</b> problem' +
    (state.total === 1 ? '' : 's');

  const more = $('#more');
  more.textContent = '';
  if (state.items.length < state.total) {
    const b = el('button', 'btn', 'Load ' +
      Math.min(state.limit, state.total - state.items.length) + ' more');
    b.onclick = loadMore;
    more.append(b, el('div', 'hint', state.items.length + ' of ' + state.total.toLocaleString() + ' shown'));
  } else if (state.total > 12) {
    more.append(el('div', 'hint', 'All ' + state.total.toLocaleString() + ' shown.'));
  }
}

async function reload() {
  state.offset = 0;
  renderChips(); pushUrl();
  const data = await api('api/problems?' + queryString({ limit: state.limit, offset: 0 }));
  state.total = data.total; state.items = data.items;
  renderList(false);
  const rl = $('#results'); if (rl) rl.scrollTop = 0;
  renderPosition();
}

async function loadMore() {
  state.offset += state.limit;
  const data = await api('api/problems?' + queryString({ limit: state.limit, offset: state.offset }));
  state.items = state.items.concat(data.items);
  state.total = data.total;
  renderList(true);
}

/* --------------------------------------------------------------- the drawer */
function openDrawer() {
  $('#drawer').hidden = false;
  $('#scrim').hidden = false;
  setTimeout(() => $('#q').focus(), 30);
}
function closeDrawer() {
  $('#drawer').hidden = true;
  $('#scrim').hidden = true;
  if (state.editor) state.editor.focus();
}
const drawerOpen = () => !$('#drawer').hidden;

/* ------------------------------------------------------------ problem pane */
function kvLine(k, v, cls) {
  const frag = document.createDocumentFragment();
  frag.append(el('div', 'k', k), el('div', 'v' + (cls ? ' ' + cls : ''), v));
  return frag;
}

function exampleBlock(ex, i) {
  const box = el('div', 'example');
  box.append(el('div', 'example-label', 'Example ' + (ex.id != null ? ex.id : i + 1)));
  const kv = el('div', 'kv');
  (ex.inputText || []).forEach(inp => {
    kv.append(kvLine((inp.inputName || '?') + '  ' + (inp.inputType || ''), inp.inputValue || ''));
  });
  kv.append(kvLine('→ output  ' + (ex.outputType || ''), ex.outputText || '', 'out'));
  box.append(kv);
  if (ex.explanation) {
    const why = el('div', 'why');
    why.innerHTML = ex.explanation;
    box.append(why);
  }
  return box;
}

function dataTable(cols, rows, limit) {
  const t = el('table', 'datatable');
  const hr = el('tr');
  (cols || []).forEach(c => hr.append(el('th', null, String(c))));
  t.append(hr);
  (rows || []).slice(0, limit || 40).forEach(r => {
    const tr = el('tr');
    (r || []).forEach(v => tr.append(el('td', null, v === null ? 'NULL' : String(v))));
    t.append(tr);
  });
  return t;
}

const GAP_TEXT = {
  'constraints': 'no constraints were captured',
  'only one example': 'only one worked example',
  'worked explanation': 'no explanation of the example',
  'starter code': 'no starter code — the Python signature is generated from the example types',
  'function name': 'no function name',
  'topics': 'no topics',
  'difficulty': 'no difficulty',
  'source screenshots': 'no screenshots of the original assessment',
  'visible cases': 'no visible cases',
  'table schema': 'no table schema',
  'result contract': 'no result contract',
  'statement': 'no statement text',
  'examples': 'no examples',
};

function renderProblem() {
  const d = state.current;
  const host = $('#problem');
  host.textContent = '';

  /* --- sticky head: title, what it is, where you are with it --- */
  const head = el('div', 'problem-head');
  head.append(el('h1', null, d.title || d.id));
  const meta = el('div', 'meta-row');
  if (d.company) meta.append(el('span', 'tag company', d.company));
  if (d.difficulty) meta.append(el('span', 'tag ' + d.difficulty, d.difficulty));
  (d.problemTypes || []).forEach(s => meta.append(el('span', 'tag stage', s)));
  (d.employmentTypes || []).forEach(s => meta.append(el('span', 'tag plain', s)));
  if (d.assessmentPlatform) meta.append(el('span', 'tag plain', d.assessmentPlatform));
  if (d.practiceFormat === 'tabular') meta.append(el('span', 'tag plain', 'SQL / tabular'));
  if (d.seenCount) meta.append(el('span', 'tag count', 'seen ' + d.seenCount + '×'));
  head.append(meta);

  /* what this problem is about: each one opens its chapter in the study space */
  const study = (d.studyTopics || []);
  if (study.length) {
    const row = el('div', 'meta-row topics-row');
    row.append(el('span', 'rowlabel', 'Topics'));
    study.forEach(t => {
      const a = el('button', 'tag topic link', t.title);
      a.title = 'Study ' + t.title + ' — ' + t.count + ' problems here';
      a.onclick = () => Study.open(t.slug);
      row.append(a);
    });
    head.append(row);
  }

  const bar = el('div', 'statusbar');
  const pr = d.progress || {};
  [['attempted', 'Attempted'], ['solved', 'Solved'], ['review', 'Review']].forEach(([s, label]) => {
    const b = el('button', 'statusbtn ' + s, label);
    b.setAttribute('aria-pressed', pr.status === s ? 'true' : 'false');
    b.onclick = () => setProgress({ status: pr.status === s ? 'none' : s });
    bar.append(b);
  });
  const bm = el('button', 'statusbtn mark', pr.bookmarked ? '★ Bookmarked' : '☆ Bookmark');
  bm.setAttribute('aria-pressed', pr.bookmarked ? 'true' : 'false');
  bm.onclick = () => setProgress({ bookmarked: !pr.bookmarked });
  bar.append(bm, el('span', 'idchip', d.id));
  head.append(bar);
  host.append(head);

  /* --- body --- */
  const body = el('div', 'problem-body');

  const gaps = (d.gaps || []).filter(g => GAP_TEXT[g]);
  if (gaps.length) {
    const n = el('div', 'callout');
    n.innerHTML = '<b>Not in the source:</b> ' + gaps.map(g => esc(GAP_TEXT[g])).join(' · ') +
      ((d.generatedCases || []).length && gaps.indexOf('only one example') >= 0
        ? ' — the ' + d.generatedCases.length + ' generated cases below make up for the last one.' : '.');
    body.append(n);
  }
  if (d.sourceNote) {
    const n = el('div', 'callout info');
    n.innerHTML = '<b>Source note.</b> ' + esc(d.sourceNote);
    body.append(n);
  }

  body.append(el('h2', 'section', 'Problem'));
  const st = el('div', 'prose');
  st.innerHTML = d.problemStatement || '<p class="hint">No statement recorded.</p>';
  body.append(st);

  if (d.constraints) {
    body.append(el('h2', 'section', 'Constraints'));
    const c = el('div', 'prose'); c.innerHTML = d.constraints; body.append(c);
  }

  if (d.practiceFormat === 'tabular') {
    const tab = d.tabular || {};
    body.append(el('h2', 'section', 'Tables'));
    const wrap = el('div');
    (tab.inputSchema || []).forEach(t => {
      const box = el('div', 'schema');
      box.append(el('h4', null, t.name));
      if (t.description) box.append(el('div', 'desc', t.description));
      const table = el('table', 'datatable');
      (t.columns || []).forEach(c => {
        const tr = el('tr');
        tr.append(el('td', null, c.name), el('td', 'type', c.type),
                  el('td', null, c.nullable ? 'nullable' : ''));
        table.append(tr);
      });
      box.append(table);
      wrap.append(box);
    });
    body.append(wrap);

    const rc = tab.resultContract || {};
    if (rc.columns) {
      body.append(el('h2', 'section', 'Expected result'));
      const box = el('div', 'schema');
      const table = el('table', 'datatable');
      rc.columns.forEach(c => {
        const tr = el('tr');
        tr.append(el('td', null, c.name), el('td', 'type', c.type));
        table.append(tr);
      });
      box.append(table, el('div', 'desc', 'row order: ' + (rc.rowOrder || 'exact') +
        (rc.numericTolerance ? ' · tolerance ' + rc.numericTolerance : '')));
      body.append(box);
    }

    body.append(el('h2', 'section', 'Visible cases'));
    (tab.visibleCases || []).forEach((c, i) => {
      const box = el('div', 'example');
      box.append(el('div', 'example-label', 'Case ' + (c.id || i + 1)));
      Object.entries(c.input || {}).forEach(([name, rows]) => {
        box.append(el('div', 'hint', name));
        const cols = ((tab.inputSchema || []).find(t => t.name === name) || {}).columns || [];
        box.append(dataTable(cols.map(x => x.name), rows));
      });
      box.append(el('div', 'hint', 'expected'));
      box.append(dataTable((c.expectedResult || {}).columns, (c.expectedResult || {}).rows));
      if (c.explanation) { const w = el('div', 'why'); w.innerHTML = c.explanation; box.append(w); }
      body.append(box);
    });
  } else {
    body.append(el('h2', 'section', 'Examples'));
    (d.examples || []).forEach((ex, i) => body.append(exampleBlock(ex, i)));
    if (!(d.examples || []).length) body.append(el('div', 'hint', 'No examples recorded.'));
  }

  if ((d.images || []).length) {
    body.append(el('h2', 'section', 'Source screenshots'));
    const shots = el('div', 'shots');
    d.images.forEach((_, i) => {
      const fig = el('figure');
      const img = el('img');
      img.loading = i < 3 ? 'eager' : 'lazy';
      img.src = url('api/images/' + encodeURIComponent(d.id) + '/' + i);
      img.alt = 'source screenshot ' + (i + 1);
      img.onclick = () => lightbox(img.src);
      img.onerror = () => { fig.textContent = '';
        fig.append(el('div', 'hint', 'screenshot ' + (i + 1) + ' could not be loaded')); };
      fig.append(img, el('figcaption', null, 'click to enlarge'));
      shots.append(fig);
    });
    body.append(shots);
  }

  body.append(el('h2', 'section', 'Test cases'));
  const casesHost = el('div'); casesHost.id = 'casesHost';
  body.append(casesHost);

  body.append(el('h2', 'section', 'Reference solution'));
  const solHost = el('div'); solHost.id = 'solutionHost';
  body.append(solHost);

  body.append(el('h2', 'section', 'Sightings'));
  const dates = el('div', 'dates');
  (d.lastSeen || []).forEach((x, i) => dates.append(el('span', 'date' + (i ? '' : ' first'), x)));
  if (!(d.lastSeen || []).length) dates.append(el('span', 'hint', 'no dates recorded'));
  body.append(dates);
  if (d.seenCount) body.append(el('div', 'hint', 'reported ' + d.seenCount + ' times'));

  body.append(el('h2', 'section', 'Notes'));
  const notes = el('textarea'); notes.id = 'notes';
  notes.placeholder = 'What pattern is this? What did you miss? Kept in progress.db.';
  notes.value = pr.notes || '';
  const saved = el('span', 'saved', '');
  notes.oninput = () => {
    if (state.current && state.current.progress) state.current.progress.notes = notes.value;
    scheduleNotes(notes.value);
  };
  body.append(notes, el('span', 'saved', 'saved as you type, in progress.db'));

  host.append(body);
  host.scrollTop = 0;
  renderCases();
  renderSolution();
}

/* ------------------------------------------------------------- workbench */
function renderWorkbench() {
  const d = state.current;
  const host = $('#workbench');
  /* Whatever is in the editor has to be read BEFORE the old one is thrown
     away with the rest of the workbench - see row 2 for why it matters. */
  if (state.editor && state.editorKey) state.buffers[state.editorKey] = state.editor.getValue();
  host.className = 'workbench';
  host.textContent = '';
  state.editor = null;

  const spec = d.languages.find(l => l.id === state.lang) || d.languages[0];
  if (!spec) { host.append(el('div', 'hint', 'No editor for this problem.')); return; }

  /* --- row 1: language + editor tools, always visible --- */
  const top = el('div', 'wb-top');
  const tabs = el('div', 'langtabs');
  d.languages.forEach(l => {
    const b = el('button', 'langtab' + (l.runnable ? '' : ' readonly'),
                 l.label + (l.runnable ? '' : ' · read-only'));
    b.setAttribute('aria-pressed', l.id === spec.id ? 'true' : 'false');
    b.title = l.note || '';
    b.onclick = () => { state.lang = l.id; renderWorkbench(); };
    tabs.append(b);
  });
  top.append(tabs);

  const tools = el('div', 'toolgroup');
  const vimBtn = el('button', 'tool', 'Vim');
  vimBtn.setAttribute('aria-pressed', state.vim ? 'true' : 'false');
  vimBtn.title = 'Vim keybindings — Ctrl-Alt-V';
  const mode = el('span', 'vimmode', '');
  vimBtn.onclick = () => {
    state.vim = !state.vim; remember('vim', state.vim ? '1' : '0');
    vimBtn.setAttribute('aria-pressed', state.vim ? 'true' : 'false');
    if (state.editor) { state.editor.setVim(state.vim); state.editor.focus(); }
    if (!state.vim) mode.textContent = '';
  };
  const relBtn = el('button', 'tool', 'Rel №');
  relBtn.setAttribute('aria-pressed', state.relno ? 'true' : 'false');
  relBtn.title = 'Relative line numbers — Ctrl-Alt-R';
  relBtn.onclick = () => {
    state.relno = !state.relno; remember('relno', state.relno ? '1' : '0');
    relBtn.setAttribute('aria-pressed', state.relno ? 'true' : 'false');
    if (state.editor) { state.editor.setRelative(state.relno); state.editor.focus(); }
  };
  const fs = el('span', 'fontsize');
  const fsVal = el('b', null, String(state.fontSize));
  const bump = (d2) => {
    state.fontSize = Math.max(10, Math.min(24, state.fontSize + d2));
    remember('fs', String(state.fontSize));
    fsVal.textContent = String(state.fontSize);
    if (state.editor) state.editor.setFontSize(state.fontSize);
  };
  const minus = el('button', 'tool icon', 'A−'); minus.onclick = () => bump(-1); minus.title = 'Smaller';
  const plus = el('button', 'tool icon', 'A+'); plus.onclick = () => bump(1); plus.title = 'Bigger';
  fs.append(minus, fsVal, plus);
  tools.append(vimBtn, relBtn, fs);
  top.append(tools, mode, el('span', 'spacer'));

  const resetBtn = el('button', 'tool', 'Reset');
  resetBtn.title = 'Back to the starter code';
  resetBtn.onclick = () => { if (state.editor) { state.editor.setValue(spec.starter || ''); state.editor.focus(); } };
  const copyBtn = el('button', 'tool', 'Copy');
  copyBtn.onclick = () => {
    navigator.clipboard.writeText(state.editor ? state.editor.getValue() : '');
    copyBtn.textContent = 'Copied'; setTimeout(() => { copyBtn.textContent = 'Copy'; }, 1200);
  };
  const more = el('div', 'toolgroup');

  /* The note is the same sentence on every Python problem, so it does not get
     to keep a strip of the editor for itself: it hides behind an ⓘ, and stays
     hidden until you ask for it. A note that explains why Run is disabled is a
     different animal - that one is a warning and stays on screen. */
  let noteRow = null;
  if (spec.note) {
    noteRow = el('div', 'wb-note' + (spec.runnable ? '' : ' warn'));
    noteRow.textContent = spec.note;
    if (spec.runnable) {
      noteRow.hidden = localStorage.getItem('fp:wbnote') !== '1';
      const info = el('button', 'tool icon', 'ⓘ');
      info.title = spec.note;
      const paintInfo = () => info.setAttribute('aria-pressed', noteRow.hidden ? 'false' : 'true');
      info.onclick = () => {
        noteRow.hidden = !noteRow.hidden;
        remember('wbnote', noteRow.hidden ? '0' : '1');
        paintInfo();
        if (state.editor) state.editor.refresh();
      };
      paintInfo();
      more.append(info);
    }
  }

  more.append(resetBtn, copyBtn);
  top.append(more);
  host.append(top);
  if (noteRow) host.append(noteRow);

  /* --- row 2: the editor itself, filling the space --- */
  const edWrap = el('div', 'wb-editor');
  const ta = el('textarea');
  const saved = (d.progress && d.progress.submissions && d.progress.submissions[spec.id]) || null;

  /* What was last in the editor for THIS problem and THIS language outranks
     what the server last stored. Saving is debounced, so the server copy is
     routinely a few hundred milliseconds behind what you typed, and anything
     that rebuilds the workbench in that window would otherwise hand you back
     the older text. Keyed by problem+language, so the Java tab still gets the
     Java code - and switching to it and back still gets your Python edits,
     which the stored copy alone would not have. Cleared when you open another
     problem, by which point the server has flushed and is authoritative. */
  const key = d.id + ':' + spec.id;
  const live = state.buffers[key];
  state.editorKey = key;

  ta.value = live != null ? live : ((saved && saved.code) || spec.starter || '');
  edWrap.append(ta);
  host.append(edWrap);

  /* --- row 3: actions, pinned above the output --- */
  const run = el('div', 'wb-run');
  const runBtn = el('button', 'btn primary', '▶  Run tests');
  runBtn.title = 'Ctrl-Enter';
  runBtn.disabled = !spec.runnable;
  runBtn.onclick = () => runCode('all');
  /* The one that just runs it. Without this, seeing a print means inventing an
     expression for Scratch, which is a strange thing to have to do to read a
     loop you are debugging. */
  const scriptBtn = el('button', 'btn', '▶  Run code');
  const canScript = spec.runnable && spec.mode === 'python';
  scriptBtn.disabled = !canScript;
  scriptBtn.title = canScript
    ? 'Run your code as a program and show everything it prints — Alt-Enter'
    : 'Only Python runs as a program here';
  scriptBtn.onclick = () => runPlain();
  const mineBtn = el('button', 'btn', 'My cases');
  mineBtn.id = 'myCasesBtn';
  if (spec.runnable) mineBtn.dataset.runnable = '1';
  mineBtn.onclick = () => runCode('custom');
  const fuzzBtn = el('button', 'btn', 'Random');
  const canFuzz = spec.runnable && spec.mode === 'python' &&
                  d.solution && d.solution.verified && d.practiceFormat !== 'tabular';
  fuzzBtn.disabled = !canFuzz;
  fuzzBtn.title = canFuzz ? 'Generated inputs, your code against the verified reference'
                          : 'Needs a verified reference solution';
  fuzzBtn.onclick = () => runFuzz();
  const solBtn = el('button', 'btn ghost', 'Solution');
  solBtn.title = d.solution ? 'Show the reference solution'
                            : 'No reference solution is stored for this problem';
  solBtn.onclick = () => showSolution();
  const scratchBtn = el('button', 'btn ghost', 'Scratch');
  scratchBtn.title = 'Evaluate an expression against your code — Shift-Ctrl-Enter';
  scratchBtn.onclick = () => toggleScratch();
  const verdict = el('span', 'verdict'); verdict.id = 'verdict';
  if (saved && saved.total != null) {
    verdict.innerHTML = '<span class="muted">last run</span> ' + (saved.passed === saved.total
      ? '<span class="ok">' + saved.passed + '/' + saved.total + '</span>'
      : '<span class="no">' + saved.passed + '/' + saved.total + '</span>');
  }
  run.append(runBtn, scriptBtn, mineBtn, fuzzBtn, solBtn, scratchBtn, verdict);
  host.append(run);
  paintMyCases();

  /* --- row 4: scratch + output --- */
  const scratch = el('div'); scratch.id = 'scratchBox'; scratch.hidden = true;
  const sin = el('textarea'); sin.id = 'scratchIn'; sin.spellcheck = false;
  sin.placeholder = (d.functionName || 'solve') + '(' +
    ((d.cases && d.cases[0] ? d.cases[0].inputs : []) || []).map(i => i.rawValue).join(', ') + ')';
  sin.onkeydown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); runScratch(); }
  };
  const sbar = el('div', 'rowbtns');
  const sgo = el('button', 'btn', 'Evaluate');
  sgo.onclick = () => runScratch();
  sbar.append(sgo, el('span', 'hint', 'runs your editor code first, then this'));
  scratch.append(sin, sbar);

  const hsplit = el('div'); hsplit.id = 'hsplit';
  hsplit.title = 'Drag to resize the output — double-click to reset';
  const out = el('div', 'wb-out'); out.id = 'wbOut';
  const runOut = el('div'); runOut.id = 'runOut';
  out.append(scratch, runOut);      // scratch stays put; only #runOut is cleared
  host.append(hsplit, out);
  wireOutputSplitter(hsplit, out);
  showOutput(false);                // nothing to read yet, so no room taken

  state.editor = window.PyEditor.create(ta, {
    vim: state.vim, relative: state.relno, fontSize: state.fontSize,
    onRun: () => runCode('all'), onScratch: () => { toggleScratch(true); runScratch(); },
    onRunPlain: () => runPlain(),
    onChange: () => scheduleSave(),
    onModeChange: (m) => { if (state.vim) mode.textContent = '-- ' + m + ' --'; },
  });
  if (!spec.runnable) state.editor.setReadOnly(true);
  setTimeout(() => state.editor && state.editor.refresh(), 0);
}

/* The reference solution, shown where you are working rather than buried at
   the bottom of the problem pane - and honest when there is not one. */
function showSolution() {
  const d = state.current;
  const box = outputPanel('Reference solution');
  const sol = d.solution;

  if (!sol) {
    const card = el('div', 'case info');
    const head = el('div', 'case-head');
    head.append(el('span', 'badge', 'NONE'),
                el('span', 'name', 'no reference solution for this problem'));
    card.append(head);
    const p = el('pre');
    const stats = (state.env && state.env.solutions) || state.solutionStats || null;
    p.textContent =
      'The bank ships no solutions. Every one here was written for this repo and kept only\n' +
      'if it passes that problem\u2019s visible examples' +
      (stats ? ', and ' + stats.verified.toLocaleString() + ' of 3,533 problems have one\n' +
               '(the most repeated and the most recent were done first).'
             : '.') +
      '\n\nTick \u201chas a reference solution\u201d in the Problems drawer to list the ones that do.';
    card.append(p);
    const bar = el('div', 'rowbtns');
    const find = el('button', 'btn', 'Show me problems that have one');
    find.onclick = () => { state.hasSolution = true; renderFilters(); reload(); openDrawer(); };
    bar.append(find);
    card.append(bar);
    box.append(card);
    return;
  }

  const card = el('div', 'case ' + (sol.verified ? 'pass' : 'info'));
  const head = el('div', 'case-head');
  head.append(el('span', 'badge', sol.verified ? 'VERIFIED' : 'UNVERIFIED'),
              el('span', 'name', sol.verified
                ? 'passes every visible example (' + (sol.cases || '') + ')'
                : 'stored, but not confirmed against the examples'));
  card.append(head);
  const pre = el('pre');
  pre.textContent = sol.code;
  card.append(pre);
  const bar = el('div', 'rowbtns');
  const load = el('button', 'btn', 'Load into the editor');
  load.onclick = () => {
    if (!state.editor) return;
    state.editor.setValue(sol.code);
    state.editor.focus();
    scheduleSave();
  };
  const copy = el('button', 'btn ghost', 'Copy');
  copy.onclick = () => {
    navigator.clipboard.writeText(sol.code);
    copy.textContent = 'Copied'; setTimeout(() => { copy.textContent = 'Copy'; }, 1200);
  };
  bar.append(load, copy, el('span', 'hint', sol.checkedAt ? 'checked ' + sol.checkedAt : ''));
  card.append(bar);
  box.append(card);
}

/* Drag the boundary between the editor and its output; double-click resets. */
function wireOutputSplitter(handle, out) {
  let on = false, startY = 0, startH = 0;
  handle.onmousedown = (e) => {
    on = true; startY = e.clientY; startH = out.getBoundingClientRect().height;
    e.preventDefault();
    handle.classList.add('dragging'); document.body.classList.add('dragging-v');
  };
  handle.ondblclick = () => {
    out.style.height = '';
    remember('outh', '');
    if (state.editor) state.editor.refresh();
  };
  window.addEventListener('mousemove', (e) => {
    if (!on) return;
    const pane = document.getElementById('editorPane').getBoundingClientRect();
    const h = Math.min(pane.height - 170, Math.max(56, startH - (e.clientY - startY)));
    out.style.height = h + 'px';
    remember('outh', String(Math.round(h)));
    if (state.editor) state.editor.refresh();
  });
  window.addEventListener('mouseup', () => {
    if (!on) return;
    on = false;
    handle.classList.remove('dragging'); document.body.classList.remove('dragging-v');
    if (state.editor) state.editor.refresh();
  });
  const saved = parseInt(localStorage.getItem('fp:outh') || '0', 10);
  if (saved > 56) out.style.height = saved + 'px';
}

function toggleScratch(forceOpen) {
  const box = $('#scratchBox');
  if (!box) return;
  box.hidden = forceOpen ? false : !box.hidden;
  if (!box.hidden) { showOutput(true); $('#scratchIn').focus(); }
  else if (!$('#runOut').children.length) showOutput(false);
}

/* The output takes a third of the pane, so it does not get to take it while it
   is empty - and it was: #wbOut always holds the scratch pad, so the `:empty`
   rule that was meant to collapse it never once matched, and a third of the
   editor was reserved for nothing from the moment a problem opened. */
function showOutput(on) {
  const out = $('#wbOut'), split = $('#hsplit');
  if (!out) return;
  out.hidden = !on;
  if (split) split.hidden = !on;
  if (state.editor) state.editor.refresh();
}

/* ONE output container for every mode - runs, Random, Scratch, Solution.
   It is #runOut, a child of #wbOut, so clearing it never destroys the scratch
   pad that sits beside it. (Two containers is how the Solution card ended up
   rendering somewhere the results were not.) */
function outputPanel(title) {
  const out = $('#runOut');
  if (!out) return $('#wbOut');
  out.textContent = '';
  showOutput(true);
  const head = el('div', 'outhead');
  if (title) head.append(el('h3', null, title));
  head.append(el('span', 'spacer'));
  const hide = el('button', 'tool icon', '✕');
  hide.title = 'Hide the output and give the room back to the editor';
  hide.onclick = () => {
    out.textContent = '';
    if ($('#scratchBox').hidden) showOutput(false);
  };
  head.append(hide);
  out.append(head);
  return out;
}

async function openProblem(id) {
  await saver.flush();               // never carry pending edits onto the next problem
  state.buffers = {};                // ...and never carry the buffers either
  const d = await api('api/problems/' + encodeURIComponent(id));
  state.current = d;
  state.lang = (d.languages.find(l => l.runnable) || d.languages[0] || {}).id;
  document.querySelectorAll('.result').forEach(c =>
    c.classList.toggle('active', c.dataset.id === id));
  paintProblem();
  pushUrl();
  Timer.onProblemOpened();
}

function paintProblem() {
  const d = state.current;
  $('#crumb').innerHTML = '<b>' + esc(d.title || d.id) + '</b>';
  renderProblem();
  renderWorkbench();
  renderPosition();
}

function renderPosition() {
  const ids = state.items.map(i => i.id);
  const at = state.current ? ids.indexOf(state.current.id) : -1;
  $('#position').textContent = at >= 0
    ? (at + 1) + ' / ' + state.total.toLocaleString()
    : (state.total ? state.total.toLocaleString() + ' listed' : '');
  $('#prevBtn').disabled = at <= 0;
  $('#nextBtn').disabled = at < 0 || at >= ids.length - 1;
}

async function step(delta) {
  const ids = state.items.map(i => i.id);
  const at = state.current ? ids.indexOf(state.current.id) : -1;
  if (at < 0) return;
  const next = at + delta;
  if (next < 0) return;
  if (next >= ids.length && state.items.length < state.total) {
    await loadMore();
    return step(delta);
  }
  if (next >= ids.length) return;
  await openProblem(ids[next]);
}

async function runFuzz() {
  const d = state.current;
  const results = outputPanel('');
  const verdict = $('#verdict');
  verdict.textContent = 'generating inputs…';
  let out;
  try {
    out = await api('/api/fuzz', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problemId: d.id, code: state.editor.getValue() }),
    });
  } catch (e) {
    verdict.innerHTML = '<span class="no">could not run</span>';
    results.append(Object.assign(el('div', 'case fail'), { textContent: e.message }));
    return;
  }

  noteSandbox(out);
  if (sandboxFailure(out, results)) return;

  if (out.error) {
    verdict.innerHTML = '<span class="no">did not run</span>';
    const box = el('div', 'case fail');
    const pre = el('pre'); pre.textContent = out.error; box.append(pre);
    results.append(box);
    return;
  }

  if (!out.failed) {
    verdict.innerHTML = '<span class="ok">agreed on ' + out.checked + ' random inputs</span>';
    const box = el('div', 'case pass');
    box.append(el('div', 'case-head', '✓ no disagreement found'));
    box.append(el('div', 'hint',
      'Your code matched the reference on ' + out.checked + ' generated inputs' +
      (out.skipped ? ' (' + out.skipped + ' more were rejected by the reference and skipped)' : '') +
      '. Evidence, not proof — the generator is random, not adversarial.'));
    box.append(el('div', 'hint', out.caveat));
    results.append(box);
    return;
  }

  verdict.innerHTML = '<span class="no">counterexample found</span>';
  const box = el('div', 'case fail');
  box.append(el('div', 'case-head', out.crash ? '✗ your code raised' : '✗ disagreement'));
  const pre = el('pre');
  pre.innerHTML = '<span class="lbl">input    </span>' + esc(out.input) +
    (out.crash ? '\n<span class="lbl">error    </span><span class="got">' + esc(out.got) + '</span>'
               : '\n<span class="lbl">expected </span><span class="exp">' + esc(out.expected) +
                 '</span>\n<span class="lbl">you      </span><span class="got">' + esc(out.got) + '</span>');
  box.append(pre);
  const bar = el('div', 'rowbtns');
  const keep = el('button', 'btn ghost', '＋ Keep this as a test case');
  keep.onclick = async () => {
    const inputs = (out.inputValues || []).map((v, i) => ({
      name: (out.inputNames || [])[i], type: (out.inputTypes || [])[i], rawValue: v }));
    await api('/api/cases/' + encodeURIComponent(d.id), {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'add', inputs: inputs,
                             expected: out.crash ? '' : out.expected,
                             note: 'found by Random' }),
    });
    const fresh = await api('/api/problems/' + encodeURIComponent(d.id));
    state.current.customCases = fresh.customCases;
    keep.textContent = 'kept'; keep.disabled = true;
    renderCases();
  };
  bar.append(keep, el('span', 'spacer'), el('span', 'hint', 'checked ' + out.checked +
    (out.skipped ? ', skipped ' + out.skipped : '')));
  box.append(bar);
  results.append(box);
}

/* Just run it: no cases, no expression to invent - the print-debugging button.
   Everything the program printed comes back in order, and a traceback points
   at the reader's own line numbers because the harness drops its own frame. */
async function runPlain() {
  const d = state.current;
  const spec = d.languages.find(l => l.id === state.lang);
  if (!spec || !spec.runnable || spec.mode !== 'python') return;
  const results = outputPanel('');
  const verdict = $('#verdict');
  verdict.textContent = 'running…';
  let out;
  try {
    out = await api('api/script', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problemId: d.id, code: state.editor.getValue() }),
    });
  } catch (e) {
    verdict.innerHTML = '<span class="no">could not run</span>';
    results.append(Object.assign(el('div', 'case fail'), { textContent: e.message }));
    return;
  }

  noteSandbox(out);
  if (sandboxFailure(out, results)) return;

  const bad = !!(out.error || out.timeout);
  const box = el('div', 'case ' + (bad ? 'fail' : 'info'));
  box.append(el('div', 'case-head', out.timeout ? '✗ still running when the clock ran out'
                                  : out.error ? '✗ your code raised'
                                  : '▶ your code ran'));
  const pre = (label, text) => {
    const n = el('pre');
    n.innerHTML = '<span class="lbl">' + label + '</span>\n' + esc(text);
    box.append(n);
  };
  if (out.printed) pre('stdout', out.printed);
  if (out.stderr) pre('stderr', out.stderr);
  if (out.error) { const n = el('pre'); n.textContent = out.error; box.append(n); }
  if (out.exit) box.append(el('div', 'hint', 'It called sys.exit(' + out.exit + ').'));
  if (!out.printed && !out.stderr && !out.error) {
    box.append(el('div', 'hint', (out.defined || []).length
      ? 'Nothing was printed. You defined ' + out.defined.join(', ') +
        ' — nothing called it. Add a print, or use Scratch to call it with an argument.'
      : 'Nothing was printed.'));
  }
  verdict.innerHTML = bad ? '<span class="no">raised</span>' : '<span class="muted">ran</span>';
  results.append(box);
}

async function runScratch() {
  const d = state.current;
  const snippet = ($('#scratchIn') || {}).value || '';
  if (!snippet.trim()) return;
  const results = outputPanel('');
  const verdict = $('#verdict');
  verdict.textContent = 'evaluating…';
  let out;
  try {
    out = await api('/api/scratch', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problemId: d.id, code: state.editor.getValue(), snippet }),
    });
  } catch (e) {
    verdict.innerHTML = '<span class="no">scratch failed</span>';
    results.append(Object.assign(el('div', 'case fail'), { textContent: e.message }));
    return;
  }
  noteSandbox(out);
  if (sandboxFailure(out, results)) return;
  verdict.innerHTML = out.error ? '<span class="no">scratch</span>' : '<span class="ok">scratch</span>';
  const box = el('div', 'case ' + (out.error ? 'fail' : 'info'));
  if (out.printed) {
    const p = el('pre'); p.innerHTML = '<span class="lbl">stdout</span>\n' + esc(out.printed);
    box.append(p);
  }
  if (out.value) {
    const p = el('pre'); p.innerHTML = '<span class="lbl">value </span>' + esc(out.value);
    box.append(p);
  }
  if (out.error) { const p = el('pre'); p.textContent = out.error; box.append(p); }
  if (!box.children.length) box.append(el('div', 'hint', '(no output)'));
  results.append(box);
}

async function runCode(include) {
  const d = state.current;
  const spec = d.languages.find(l => l.id === state.lang);
  if (!spec || !spec.runnable) return;
  const results = outputPanel('');
  const verdict = $('#verdict');
  verdict.textContent = 'running…';
  let out;
  try {
    out = await api('/api/run', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problemId: d.id, language: spec.id, include: include || 'all',
                             code: state.editor.getValue() }),
    });
  } catch (e) {
    verdict.innerHTML = '<span class="no">could not run</span>';
    results.append(Object.assign(el('div', 'case fail'), { textContent: e.message }));
    return;
  }
  renderResults(out);
  const fresh = await api('/api/problems/' + encodeURIComponent(d.id));
  state.current.progress = fresh.progress;
}

function renderResults(out) {
  const results = outputPanel('');
  const verdict = $('#verdict');

  noteSandbox(out);
  if (sandboxFailure(out, results)) return;

  if (out.error && !(out.results || []).length) {
    verdict.innerHTML = '<span class="no">did not run</span>';
    const box = el('div', 'case fail');
    box.append(el('div', 'case-head', out.timeout ? 'Stopped' : 'Error'));
    const pre = el('pre'); pre.textContent = out.error; box.append(pre);
    results.append(box);
    return;
  }

  const all = out.passed === out.total && out.total > 0;
  verdict.innerHTML = (all ? '<span class="ok">' : '<span class="no">') +
    out.passed + ' / ' + out.total + ' visible examples passed</span>' +
    ' · sandbox: ' + esc(out.sandbox);

  (out.results || []).forEach((r, i) => {
    const informational = r.ok === null || r.ok === undefined;
    const box = el('div', 'case ' + (informational ? 'info' : (r.ok ? 'pass' : 'fail')));
    const h = el('div', 'case-head');
    const badge = el('span', 'badge', informational ? 'RAN' : (r.ok ? 'PASS' : 'FAIL'));
    h.append(badge, el('span', 'name', 'case ' + (r.id != null ? r.id : i + 1)));
    if (r.custom) h.append(el('span', 'pill', 'mine'));
    if (r.generated) h.append(el('span', 'pill', 'generated'));
    if (r.note) h.append(el('span', 'hint', ' ' + r.note));
    box.append(h);
    if (informational && r.got !== undefined) {
      const g = el('pre');
      g.innerHTML = '<span class="lbl">returned </span>' + esc(r.got);
      box.append(g);
    }

    if (r.error) { const p = el('pre'); p.textContent = r.error; box.append(p); }
    if (r.expected !== undefined && r.expected !== null) {
      const g = el('pre'); g.innerHTML = '<span class="lbl">expected </span><span class="exp">' +
        esc(r.expected) + '</span>\n<span class="lbl">got      </span><span class="got">' +
        esc(r.got) + '</span>';
      box.append(g);
    }
    if (r.columns) {                       // tabular result
      const grid = el('div', 'grid2');
      const a = el('div'); a.append(el('div', 'hint', 'your rows'), dataTable(r.columns, r.rows));
      const b = el('div'); b.append(el('div', 'hint', 'expected rows'),
                                    dataTable(r.expectedColumns, r.expectedRows));
      grid.append(a, b); box.append(grid);
      if (r.rowOrder) box.append(el('div', 'hint', 'row order: ' + r.rowOrder));
    }
    if (r.stdout) {
      const p = el('pre'); p.innerHTML = '<span class="lbl">stdout</span>\n' + esc(r.stdout);
      box.append(p);
    }
    if (r.explanation) { const e = el('div', 'why'); e.innerHTML = r.explanation; box.append(e); }
    results.append(box);
  });
}

async function setProgress(fields, quiet) {
  const d = state.current;
  const body = Object.assign({}, fields);
  const updated = await api('/api/progress/' + encodeURIComponent(d.id), {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  d.progress = Object.assign({}, d.progress, updated);
  if (!quiet) { paintProblem(); reload(); }
}


/* ------------------------------------------------------------ sort control */
/* One entry per sortable field plus a direction button, instead of a fixed
   list of one-way sorts: every field can be read in either order. */
const DIR_LABEL = {
  recent:     { desc: 'newest first',      asc: 'oldest first' },
  frequent:   { desc: 'most seen first',   asc: 'least seen first' },
  difficulty: { asc: 'easiest first',      desc: 'hardest first' },
  title:      { asc: 'A → Z',              desc: 'Z → A' },
  company:    { asc: 'A → Z',              desc: 'Z → A' },
  default:    { asc: 'bank order',         desc: 'reverse bank order' },
  relevance:  { desc: 'best match first',  asc: 'best match first' },
};

function sortFields() {
  const fromServer = (state.facets && state.facets.sorts) || [];
  const list = fromServer.map(s => ({ key: s.key, label: s.label,
                                      def: s.defaultDirection || 'desc' }));
  list.push({ key: 'relevance', label: 'relevance (search)', def: 'desc' });
  return list;
}

function currentDirection() {
  if (state.dir === 'asc' || state.dir === 'desc') return state.dir;
  const f = sortFields().find(x => x.key === state.sort);
  return f ? f.def : 'desc';
}

function paintDirButton() {
  const d = currentDirection(), btn = $('#dir');
  if (!btn) return;
  btn.textContent = d === 'asc' ? '↑' : '↓';
  const labels = DIR_LABEL[state.sort] || {};
  btn.title = (labels[d] || d) + ' — click to reverse (r)';
  btn.disabled = state.sort === 'relevance';
}

function flipDirection() {
  state.dir = currentDirection() === 'asc' ? 'desc' : 'asc';
  paintDirButton();
}

function renderSortControl() {
  const sel = $('#sort');
  sel.textContent = '';
  sortFields().forEach(f => {
    const o = el('option', null, f.label);
    o.value = f.key;
    sel.append(o);
  });
  if (!sortFields().some(f => f.key === state.sort)) state.sort = 'recent';
  sel.value = state.sort;
  paintDirButton();
}


function lightbox(src) {
  const lb = $('#lightbox');
  lb.querySelector('img').src = src;
  lb.hidden = false;
}

/* --------------------------------------------------------- splitter drag */
function wireSplitter() {
  const sp = $('#splitter'), left = $('#problemPane'), ws = $('#workspace');
  let on = false;
  sp.onmousedown = (e) => {
    on = true; e.preventDefault();
    sp.classList.add('dragging'); document.body.classList.add('dragging');
  };
  sp.ondblclick = () => {
    left.style.flex = '0 0 46%';
    remember('split', '46');
    if (state.editor) state.editor.refresh();
  };
  window.addEventListener('mousemove', (e) => {
    if (!on) return;
    const r = ws.getBoundingClientRect();
    const pct = Math.min(72, Math.max(24, (e.clientX - r.left) / r.width * 100));
    left.style.flex = '0 0 ' + pct + '%';
    remember('split', String(Math.round(pct)));
    if (state.editor) state.editor.refresh();      // keep the code laid out while dragging
  });
  window.addEventListener('mouseup', () => {
    if (!on) return;
    on = false;
    sp.classList.remove('dragging'); document.body.classList.remove('dragging');
    if (state.editor) state.editor.refresh();
  });
  const saved = parseInt(localStorage.getItem('fp:split') || '0', 10);
  if (saved >= 24 && saved <= 72) left.style.flex = '0 0 ' + saved + '%';
}

/* -------------------------------------------------------------------- boot */
async function boot() {
  const wanted = readUrl();
  $('#q').value = state.q;

  const boot = window.__BOOT__ || null;
  const env = boot ? boot.environment : (await api('api/health')).environment;
  state.env = env;
  paintEnv(env.sandbox, env.sandboxNote);

  state.facets = boot ? boot.facets : await api('api/facets');
  renderSortControl();
  renderFilters();
  if (boot && boot.list) {
    state.total = boot.list.total; state.items = boot.list.items;
    renderChips(); renderList(false);
  } else {
    await reload();
  }

  if (boot && boot.detail) {
    state.current = boot.detail;
    state.lang = (boot.detail.languages.find(l => l.runnable) || boot.detail.languages[0] || {}).id;
    paintProblem();
  } else if (wanted) {
    openProblem(wanted).catch(() => {});
  } else {
    renderPosition();
    if (!state.wantTopic && !state.wantTopicList) openDrawer();
  }

  wireSplitter();
  Study.wire();
  Timer.wire();
  if (state.wantTopic) Study.open(state.wantTopic);
  else if (state.wantTopicList) Study.openIndex();

  let t = null;
  $('#q').oninput = (e) => {
    state.q = e.target.value;
    if (state.q && state.sort === 'recent') { state.sort = 'relevance'; $('#sort').value = 'relevance'; }
    if (!state.q && state.sort === 'relevance') { state.sort = 'recent'; $('#sort').value = 'recent'; }
    paintDirButton();
    clearTimeout(t); t = setTimeout(reload, 180);
  };
  $('#sort').onchange = (e) => { state.sort = e.target.value; state.dir = ''; paintDirButton(); reload(); };
  $('#dir').onclick = () => { flipDirection(); reload(); };
  $('#menuBtn').onclick = () => (drawerOpen() ? closeDrawer() : openDrawer());
  $('#studyBtn').onclick = () => (state.studyOpen ? Study.close() : Study.openIndex());
  $('#drawerClose').onclick = closeDrawer;
  $('#scrim').onclick = closeDrawer;
  $('#prevBtn').onclick = () => step(-1);
  $('#nextBtn').onclick = () => step(1);
  $('#clearAll').onclick = () => {
    MULTI.forEach(k => state.filters[k].clear());
    SINGLE.forEach(k => { if (k !== 'sort') state[k] = ''; });
    FLAGS.forEach(k => { state[k] = false; });
    $('#q').value = '';
    renderFilters(); reload();
  };
  $('#lightbox').onclick = () => { $('#lightbox').hidden = true; };

  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.altKey && (e.key === 'v' || e.key === 'V')) {
      e.preventDefault();
      const b = document.querySelector('.toolgroup .tool'); if (b) b.click();
      return;
    }
    if (e.ctrlKey && e.altKey && (e.key === 'r' || e.key === 'R')) {
      e.preventDefault();
      const bs = document.querySelectorAll('.toolgroup .tool');
      if (bs[1]) bs[1].click();
      return;
    }
    if (e.key === 'Escape') {
      if (Timer.onEscape()) return;
      if (!$('#lightbox').hidden) { $('#lightbox').hidden = true; return; }
      if (drawerOpen()) { closeDrawer(); return; }
      if (state.studyOpen) Study.close();
      return;
    }
    const typing = e.target.matches('input,textarea,select') ||
                   e.target.closest('.CodeMirror');
    if (e.key === '/' && !typing) { e.preventDefault(); openDrawer(); return; }
    if (typing) return;
    if (e.key === 's') { state.studyOpen ? Study.close() : Study.openIndex(); return; }
    if (e.key === 't') { Timer.toggle(); return; }
    if (e.key === 'j') step(1);
    if (e.key === 'k') step(-1);
    if (e.key === 'r' && drawerOpen()) { flipDirection(); reload(); }
  });
}

boot().catch(e => {
  document.body.innerHTML = '<pre style="padding:32px;color:#ff8a8a;font:13px/1.6 monospace">' +
    esc('Could not start: ' + (e && e.message || e)) + '</pre>';
});
