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
const FLAGS = ['hasImages', 'bookmarked', 'hasNotes'];

const state = {
  filters: Object.fromEntries(MULTI.map(k => [k, new Set()])),
  q: '', sort: 'recent', dir: '', seenFrom: '', seenTo: '', seenOnFrom: '', seenOnTo: '',
  minSeen: '', maxSeen: '', status: '', hasImages: false, bookmarked: false, hasNotes: false,
  offset: 0, limit: 50, total: 0, items: [], current: null, facets: null,
  env: null, lang: null, dirty: false,
};

function queryString(extra) {
  const p = new URLSearchParams();
  MULTI.forEach(k => state.filters[k].forEach(v => p.append(k, v)));
  SINGLE.forEach(k => { if (state[k]) p.set(k, state[k]); });
  FLAGS.forEach(k => { if (state[k]) p.set(k, '1'); });
  Object.entries(extra || {}).forEach(([k, v]) => p.set(k, v));
  return p.toString();
}

async function api(path, opts) {
  const r = await fetch(path, opts);
  const body = await r.json().catch(() => ({ error: r.statusText }));
  if (!r.ok) throw new Error(body.error || ('HTTP ' + r.status));
  return body;
}

/* ------------------------------------------------------------- url syncing */
function pushUrl() {
  const qs = queryString(state.current ? { id: state.current.id } : {});
  history.replaceState(null, '', qs ? '?' + qs : location.pathname);
}
function readUrl() {
  const p = new URLSearchParams(location.search);
  MULTI.forEach(k => p.getAll(k).forEach(v => state.filters[k].add(v)));
  SINGLE.forEach(k => { if (p.get(k)) state[k] = p.get(k); });
  FLAGS.forEach(k => { if (p.get(k)) state[k] = true; });
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
   ['hasImages', 'has source screenshots']].forEach(([key, label]) => {
    const lab = el('label', 'opt');
    const cb = el('input'); cb.type = 'checkbox'; cb.checked = !!state[key];
    cb.onchange = () => { state[key] = cb.checked; reload(); };
    lab.append(cb, el('span', null, label));
    if (key === 'hasImages') lab.append(el('span', 'n', String(f.meta.withImages)));
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

/* -------------------------------------------------------------------- list */
function card(p) {
  const c = el('div', 'card' + (state.current && state.current.id === p.id ? ' active' : ''));
  c.dataset.id = p.id;
  c.append(el('div', 't', p.title || p.id));
  const m = el('div', 'meta');
  if (p.company) m.append(el('span', 'tag co', p.company));
  if (p.difficulty) m.append(el('span', 'tag ' + p.difficulty, p.difficulty));
  (p.stages || []).forEach(s => m.append(el('span', 'tag stage', s)));
  if (p.format === 'tabular') m.append(el('span', 'tag', 'SQL / tabular'));
  if (p.seenCount) m.append(el('span', 'tag', 'seen ' + p.seenCount + '×'));
  const pr = p.progress || {};
  if (pr.status) m.append(el('span', 'tag mark ' + pr.status, pr.status));
  if (pr.bookmarked) m.append(el('span', 'tag mark bookmark', '★'));
  m.append(el('span', 'when', p.lastSeenMax || ''));
  c.append(m);
  c.onclick = () => openProblem(p.id);
  return c;
}

function renderList(append) {
  const host = $('#list');
  if (!append) host.textContent = '';
  if (!state.items.length && !append) {
    host.append(el('div', 'empty-msg', 'Nothing matches those filters.'));
  }
  const slice = append ? state.items.slice(host.children.length) : state.items;
  slice.forEach(p => host.append(card(p)));

  $('#count').innerHTML = '<b>' + state.total.toLocaleString() + '</b> problem' +
    (state.total === 1 ? '' : 's');
  const more = $('#more');
  more.textContent = '';
  if (state.items.length < state.total) {
    const b = el('button', null, 'Load ' +
      Math.min(state.limit, state.total - state.items.length) + ' more  (' +
      state.items.length + ' of ' + state.total.toLocaleString() + ')');
    b.onclick = loadMore;
    more.append(b);
  } else if (state.total) {
    more.append(el('div', 'hint', 'End of results — ' + state.total.toLocaleString() + ' shown.'));
  }
}

async function reload() {
  state.offset = 0;
  renderChips(); pushUrl();
  const data = await api('/api/problems?' + queryString({ limit: state.limit, offset: 0 }));
  state.total = data.total; state.items = data.items;
  renderList(false);
  $('#listPane').scrollTop = 0;
}

async function loadMore() {
  state.offset += state.limit;
  const data = await api('/api/problems?' + queryString({ limit: state.limit, offset: state.offset }));
  state.items = state.items.concat(data.items);
  state.total = data.total;
  renderList(true);
}

/* ------------------------------------------------------------------ detail */
function kvRow(k, v) {
  const frag = document.createDocumentFragment();
  frag.append(el('div', 'k', k), el('div', 'v', v));
  return frag;
}

function exampleBlock(ex, i) {
  const box = el('div', 'example');
  box.append(el('div', 'eh', 'Example ' + (ex.id != null ? ex.id : i + 1)));
  const kv = el('div', 'kv');
  (ex.inputText || []).forEach(inp => {
    kv.append(kvRow((inp.inputName || '?') + ' (' + (inp.inputType || '?') + ')',
                    inp.inputValue || ''));
  });
  kv.append(kvRow('→ output (' + (ex.outputType || '?') + ')', ex.outputText || ''));
  box.append(kv);
  if (ex.explanation) {
    const e = el('div', 'expl'); e.innerHTML = ex.explanation; box.append(e);
  }
  return box;
}

function tableBlock(t) {
  const box = el('div', 'tbl');
  box.append(el('h4', null, t.name));
  if (t.description) box.append(el('div', 'desc', t.description));
  const table = el('table');
  (t.columns || []).forEach(c => {
    const tr = el('tr');
    tr.append(el('td', null, c.name));
    tr.append(el('td', 'ty', c.type));
    tr.append(el('td', 'nn', c.nullable ? 'nullable' : ''));
    table.append(tr);
  });
  box.append(table);
  return box;
}

function caseTable(cols, rows) {
  const t = el('table');
  const hr = el('tr');
  (cols || []).forEach(c => hr.append(el('th', null, String(c))));
  t.append(hr);
  (rows || []).slice(0, 40).forEach(r => {
    const tr = el('tr');
    (r || []).forEach(v => tr.append(el('td', null, v === null ? 'NULL' : String(v))));
    t.append(tr);
  });
  return t;
}

async function openProblem(id) {
  const d = await api('/api/problems/' + encodeURIComponent(id));
  state.current = d;
  state.lang = (d.languages.find(l => l.runnable) || d.languages[0] || {}).id;
  document.querySelectorAll('.card').forEach(c =>
    c.classList.toggle('active', c.dataset.id === id));
  renderDetail();
  pushUrl();
  $('#detailPane').scrollTop = 0;
}

function renderDetail() {
  const d = state.current, pane = $('#detailPane');
  pane.classList.remove('empty');
  pane.textContent = '';

  /* ---- header ---- */
  const head = el('div', 'dhead');
  head.append(el('h1', null, d.title || d.id));
  const meta = el('div', 'dmeta');
  if (d.company) meta.append(el('span', 'tag co', d.company));
  if (d.difficulty) meta.append(el('span', 'tag ' + d.difficulty, d.difficulty));
  (d.problemTypes || []).forEach(s => meta.append(el('span', 'tag stage', s)));
  (d.employmentTypes || []).forEach(s => meta.append(el('span', 'tag', s)));
  if (d.assessmentPlatform) meta.append(el('span', 'tag', d.assessmentPlatform));
  if (d.practiceFormat === 'tabular') meta.append(el('span', 'tag', 'tabular'));
  if (d.seenCount) meta.append(el('span', 'tag', 'seen ' + d.seenCount + '×'));
  if ((d.images || []).length) meta.append(el('span', 'tag img',
    (d.images.length) + ' screenshot' + (d.images.length === 1 ? '' : 's')));
  (d.topics || []).forEach(t => meta.append(el('span', 'tag', t)));
  head.append(meta);

  const actions = el('div', 'dactions');
  const pr = d.progress || {};
  ['attempted', 'solved', 'review'].forEach(s => {
    const b = el('button', 'btn' + (pr.status === s ? ' on' : ''), s);
    b.onclick = () => setProgress({ status: pr.status === s ? 'none' : s });
    actions.append(b);
  });
  const bm = el('button', 'btn' + (pr.bookmarked ? ' on' : ''),
                pr.bookmarked ? '★ bookmarked' : '☆ bookmark');
  bm.onclick = () => setProgress({ bookmarked: !pr.bookmarked });
  actions.append(bm);
  const idChip = el('span', 'tag', d.id);
  actions.append(idChip);
  head.append(actions);
  pane.append(head);

  /* ---- body ---- */
  const body = el('div', 'dbody');

  if (d.sourceNote) {
    const n = el('div', 'note');
    n.innerHTML = '<b>Source note.</b> ' + esc(d.sourceNote);
    body.append(n);
  }

  body.append(el('h2', null, 'Problem'));
  const st = el('div', 'statement');
  st.innerHTML = d.problemStatement || '<p class="hint">No statement recorded.</p>';
  body.append(st);

  if (d.constraints) {
    body.append(el('h2', null, 'Constraints'));
    const c = el('div', 'statement'); c.innerHTML = d.constraints; body.append(c);
  }

  if (d.practiceFormat === 'tabular') {
    const tab = d.tabular || {};
    body.append(el('h2', null, 'Tables'));
    const tables = el('div', 'tables');
    (tab.inputSchema || []).forEach(t => tables.append(tableBlock(t)));
    body.append(tables);

    const rc = tab.resultContract || {};
    if (rc.columns) {
      body.append(el('h2', null, 'Expected result'));
      const box = el('div', 'tbl');
      const table = el('table');
      (rc.columns || []).forEach(c => {
        const tr = el('tr');
        tr.append(el('td', null, c.name), el('td', 'ty', c.type));
        table.append(tr);
      });
      box.append(table);
      box.append(el('div', 'desc', 'row order: ' + (rc.rowOrder || 'exact') +
        (rc.numericTolerance ? ' · numeric tolerance ' + rc.numericTolerance : '')));
      body.append(box);
    }

    body.append(el('h2', null, 'Visible cases'));
    (tab.visibleCases || []).forEach((c, i) => {
      const box = el('div', 'example');
      box.append(el('div', 'eh', 'Case ' + (c.id || i + 1)));
      Object.entries(c.input || {}).forEach(([name, rows]) => {
        box.append(el('div', 'desc', name));
        const cols = ((tab.inputSchema || []).find(t => t.name === name) || {}).columns || [];
        box.append(caseTable(cols.map(x => x.name), rows));
      });
      box.append(el('div', 'desc', 'expected'));
      box.append(caseTable((c.expectedResult || {}).columns, (c.expectedResult || {}).rows));
      if (c.explanation) box.append(el('div', 'expl', c.explanation));
      body.append(box);
    });
  } else {
    body.append(el('h2', null, 'Examples'));
    (d.examples || []).forEach((ex, i) => body.append(exampleBlock(ex, i)));
    if (!(d.examples || []).length) body.append(el('div', 'hint', 'No examples recorded.'));
  }

  if ((d.images || []).length) {
    body.append(el('h2', null, 'Source screenshots'));
    body.append(el('div', 'hint',
      'Screenshots of the original assessment. The first view fetches them from fastprep.io and caches them locally.'));
    const shots = el('div', 'shots');
    d.images.forEach((_, i) => {
      const fig = el('figure');
      const img = el('img');
      /* at most a handful per problem, and they are the point of the section:
         lazy loading only means a blank box until you scroll past it */
      img.loading = i < 3 ? 'eager' : 'lazy';
      img.src = '/api/images/' + encodeURIComponent(d.id) + '/' + i;
      img.alt = 'source screenshot ' + (i + 1);
      img.onclick = () => lightbox(img.src);
      img.onerror = () => { fig.textContent = ''; fig.append(el('div', 'hint',
        'screenshot ' + (i + 1) + ' could not be loaded (offline?)')); };
      fig.append(img, el('figcaption', null, 'screenshot ' + (i + 1) + ' — click to enlarge'));
      shots.append(fig);
    });
    body.append(shots);
  }

  body.append(el('h2', null, 'Sightings'));
  const dates = el('div', 'dates');
  (d.lastSeen || []).forEach((x, i) => dates.append(el('span', 'date' + (i ? '' : ' first'), x)));
  if (!(d.lastSeen || []).length) dates.append(el('span', 'hint', 'no dates recorded'));
  body.append(dates);
  if (d.seenCount) body.append(el('div', 'hint', 'reported ' + d.seenCount + ' times'));

  /* ---- editor ---- */
  body.append(el('h2', null, 'Your solution'));
  const bar = el('div', 'langbar');
  d.languages.forEach(l => {
    const b = el('button', 'btn' + (l.id === state.lang ? ' on' : ''),
                 l.label + (l.runnable ? '' : ' (read-only)'));
    b.title = l.note || '';
    b.onclick = () => { state.lang = l.id; renderEditor(); };
    bar.append(b);
  });
  body.append(bar);
  const editorHost = el('div'); editorHost.id = 'editorHost';
  body.append(editorHost);

  /* ---- notes ---- */
  body.append(el('h2', null, 'Notes'));
  const notes = el('textarea'); notes.id = 'notes';
  notes.placeholder = 'What pattern is this? What did you miss? Written here, kept in progress.db.';
  notes.value = pr.notes || '';
  const savedMsg = el('span', 'saved', '');
  let t = null;
  notes.oninput = () => {
    clearTimeout(t); savedMsg.textContent = 'saving…';
    t = setTimeout(async () => {
      await setProgress({ notes: notes.value }, true);
      savedMsg.textContent = 'saved';
      setTimeout(() => { savedMsg.textContent = ''; }, 1500);
    }, 600);
  };
  body.append(notes, savedMsg);

  pane.append(body);
  renderEditor();
}

function renderEditor() {
  const d = state.current;
  const host = $('#editorHost');
  if (!host) return;
  host.textContent = '';
  const spec = d.languages.find(l => l.id === state.lang) || d.languages[0];
  if (!spec) { host.append(el('div', 'hint', 'No editor for this problem.')); return; }

  document.querySelectorAll('.langbar .btn').forEach((b, i) =>
    b.classList.toggle('on', d.languages[i] && d.languages[i].id === spec.id));

  if (spec.note) {
    const n = el('div', 'note' + (spec.runnable ? '' : ' warn'));
    n.textContent = spec.note;
    host.append(n);
  }

  const saved = (d.progress && d.progress.submissions && d.progress.submissions[spec.id]) || null;
  const ta = el('textarea'); ta.id = 'editor'; ta.spellcheck = false;
  ta.value = (saved && saved.code) || spec.starter || '';
  ta.readOnly = !spec.runnable;
  ta.onkeydown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const s = ta.selectionStart, en = ta.selectionEnd;
      ta.value = ta.value.slice(0, s) + '    ' + ta.value.slice(en);
      ta.selectionStart = ta.selectionEnd = s + 4;
    }
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); runCode(); }
  };
  host.append(ta);

  const runbar = el('div', 'runbar');
  const runBtn = el('button', 'btn run', '▶ Run visible examples  (Ctrl-Enter)');
  runBtn.disabled = !spec.runnable;
  runBtn.onclick = runCode;
  const resetBtn = el('button', 'btn', 'Reset to starter');
  resetBtn.onclick = () => { ta.value = spec.starter || ''; };
  runbar.append(runBtn, resetBtn, el('span', 'spacer'));
  const verdict = el('span', 'verdict'); verdict.id = 'verdict';
  if (saved && saved.total != null) {
    verdict.innerHTML = 'last run: ' + (saved.passed === saved.total
      ? '<span class="ok">' + saved.passed + '/' + saved.total + '</span>'
      : '<span class="no">' + saved.passed + '/' + saved.total + '</span>') +
      ' · ' + esc(saved.ranAt || '');
  }
  runbar.append(verdict);
  host.append(runbar);

  const disclaimer = el('div', 'note warn');
  disclaimer.textContent = 'These are the problem’s visible examples only. This bank ships ' +
    'no hidden tests and no reference solution, so passing every case does not mean your ' +
    'solution is correct.';
  host.append(disclaimer);
  host.append(el('div', 'results'));
}

async function runCode() {
  const d = state.current;
  const spec = d.languages.find(l => l.id === state.lang);
  if (!spec || !spec.runnable) return;
  const results = $('#editorHost .results');
  const verdict = $('#verdict');
  results.textContent = '';
  verdict.textContent = 'running…';
  let out;
  try {
    out = await api('/api/run', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problemId: d.id, language: spec.id, code: $('#editor').value }),
    });
  } catch (e) {
    verdict.innerHTML = '<span class="no">could not run</span>';
    results.append(Object.assign(el('div', 'res fail'), { textContent: e.message }));
    return;
  }
  renderResults(out);
  const fresh = await api('/api/problems/' + encodeURIComponent(d.id));
  state.current.progress = fresh.progress;
}

function renderResults(out) {
  const results = $('#editorHost .results');
  const verdict = $('#verdict');
  results.textContent = '';

  if (out.error && !(out.results || []).length) {
    verdict.innerHTML = '<span class="no">did not run</span>';
    const box = el('div', 'res fail');
    box.append(el('div', 'rh', out.timeout ? 'Stopped' : 'Error'));
    const pre = el('pre'); pre.textContent = out.error; box.append(pre);
    results.append(box);
    return;
  }

  const all = out.passed === out.total && out.total > 0;
  verdict.innerHTML = (all ? '<span class="ok">' : '<span class="no">') +
    out.passed + ' / ' + out.total + ' visible examples passed</span>' +
    ' · sandbox: ' + esc(out.sandbox);

  (out.results || []).forEach((r, i) => {
    const box = el('div', 'res ' + (r.ok ? 'pass' : 'fail'));
    const h = el('div', 'rh');
    const badge = el('span', 'badge', r.ok ? 'PASS' : 'FAIL');
    h.append(badge, document.createTextNode('case ' + (r.id != null ? r.id : i + 1)));
    box.append(h);

    if (r.error) { const p = el('pre'); p.textContent = r.error; box.append(p); }
    if (r.expected !== undefined) {
      const g = el('pre'); g.innerHTML = '<span class="lbl">expected </span><span class="exp">' +
        esc(r.expected) + '</span>\n<span class="lbl">got      </span><span class="got">' +
        esc(r.got) + '</span>';
      box.append(g);
    }
    if (r.columns) {                       // tabular result
      const grid = el('div', 'grid2');
      const a = el('div'); a.append(el('div', 'lbl', 'your rows'), caseTable(r.columns, r.rows));
      const b = el('div'); b.append(el('div', 'lbl', 'expected rows'),
                                    caseTable(r.expectedColumns, r.expectedRows));
      grid.append(a, b); box.append(grid);
      if (r.rowOrder) box.append(el('div', 'lbl', 'row order: ' + r.rowOrder));
    }
    if (r.stdout) {
      const p = el('pre'); p.innerHTML = '<span class="lbl">stdout</span>\n' + esc(r.stdout);
      box.append(p);
    }
    if (r.explanation) { const e = el('div', 'expl'); e.innerHTML = r.explanation; box.append(e); }
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
  if (!quiet) { renderDetail(); reload(); }
}

function lightbox(src) {
  const lb = $('#lightbox');
  lb.querySelector('img').src = src;
  lb.hidden = false;
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

/* -------------------------------------------------------------------- boot */
async function boot() {
  const wanted = readUrl();
  $('#q').value = state.q;

  /* The server inlines the first screen (see serve.py::_index), so the list is
     painted in the first frame; fall back to fetching when it is absent. */
  const boot = window.__BOOT__ || null;
  const env = boot ? boot.environment : (await api('/api/health')).environment;
  state.env = env;
  const envEl = $('#env');
  envEl.textContent = 'sandbox: ' + env.sandbox +
    ' · java ' + (env.java ? 'on' : 'off') + ' · pandas ' + (env.pandas ? 'on' : 'off');
  if (env.sandbox !== 'bubblewrap') envEl.classList.add('warn');
  envEl.title = 'User code runs under ' + env.sandbox + ', limited to ' +
    env.wallTimeout + 's wall / ' + env.cpuSeconds + 's CPU / ' + env.memoryMB + ' MB.';

  state.facets = boot ? boot.facets : await api('/api/facets');
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
    document.querySelectorAll('.card').forEach(c =>
      c.classList.toggle('active', c.dataset.id === boot.detail.id));
    renderDetail();
  } else if (wanted) {
    openProblem(wanted).catch(() => {});
  }

  let t = null;
  $('#q').oninput = (e) => {
    state.q = e.target.value;
    if (state.q && state.sort === 'recent') { state.sort = 'relevance'; $('#sort').value = 'relevance'; }
    if (!state.q && state.sort === 'relevance') { state.sort = 'recent'; $('#sort').value = 'recent'; }
    paintDirButton();
    clearTimeout(t); t = setTimeout(reload, 180);
  };
  $('#sort').onchange = (e) => {
    state.sort = e.target.value;
    state.dir = '';                       // back to that field's natural order
    paintDirButton(); reload();
  };
  $('#dir').onclick = () => { flipDirection(); reload(); };
  $('#menuBtn').onclick = () => $('#filters').classList.toggle('hidden');
  $('#clearAll').onclick = () => {
    MULTI.forEach(k => state.filters[k].clear());
    SINGLE.forEach(k => { if (k !== 'sort') state[k] = ''; });
    FLAGS.forEach(k => { state[k] = false; });
    $('#q').value = '';
    renderFilters(); reload();
  };
  $('#lightbox').onclick = () => { $('#lightbox').hidden = true; };
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') $('#lightbox').hidden = true;
    if (e.target.matches('input,textarea,select')) return;
    if (e.key === '/') { e.preventDefault(); $('#q').focus(); }
    if (e.key === 'f') { e.preventDefault(); $('#filters').classList.toggle('hidden'); }
    if (e.key === 'r') { e.preventDefault(); flipDirection(); reload(); }
  });
}

boot().catch(e => {
  document.body.innerHTML = '<pre style="padding:30px;color:#ff8a8a">' +
    esc('Could not start: ' + e.message) + '</pre>';
});
