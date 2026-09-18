/* The study space: 150 chapters, the problems that practise each one, and the
 * state of your reading - all of it kept server-side like everything else.
 *
 * Loaded before app.js; it borrows $, el, esc, api, url, state and openProblem
 * from there, which is safe because nothing here runs before boot(). */
'use strict';

const Study = {
  index: null,           // {topics, categories, ...}
  current: null,         // the open chapter's payload
  filter: '',
  ran: {},               // snippet index -> last output element

  /* ------------------------------------------------------------- opening */
  async openIndex() {
    show(true);
    state.studyOpen = true;
    state.topic = '';
    await this.load();
    this.paintList();
    $('#topic').innerHTML = '';
    $('#topic').append(welcome(this.index));
    pushUrl();
  },

  async open(slug) {
    show(true);
    state.studyOpen = true;
    state.topic = slug;
    await this.load();
    this.paintList();
    const pane = $('#topic');
    pane.textContent = '';
    pane.append(el('div', 'hint pad', 'Loading ' + slug + '…'));
    try {
      const boot = window.__BOOT__;
      if (boot && boot.topic && boot.topic.slug === slug) {
        this.current = boot.topic;
        boot.topic = null;                 // only good for the first paint
      } else {
        this.current = await api('api/topics/' + encodeURIComponent(slug));
      }
    } catch (e) {
      pane.textContent = '';
      pane.append(el('div', 'callout warn', 'Could not open that topic: ' + e.message));
      return;
    }
    this.paintTopic();
    pushUrl();
  },

  close() {
    show(false);
    state.studyOpen = false;
    state.topic = '';
    pushUrl();
  },

  async load() {
    const boot = window.__BOOT__;
    if (!this.index && boot && boot.topics) this.index = boot.topics;
    if (!this.index) this.index = await api('api/topics');
    return this.index;
  },

  /* ----------------------------------------------------------- the list */
  paintList() {
    const host = $('#topicList');
    host.textContent = '';
    const q = this.filter.trim().toLowerCase();
    let shown = 0;
    let lastCat = null;
    this.index.topics.forEach(t => {
      if (q && (t.title + ' ' + t.slug + ' ' + t.category + ' ' + (t.covers || []).join(' '))
          .toLowerCase().indexOf(q) < 0) return;
      shown++;
      if (t.category !== lastCat) {
        host.append(el('div', 'tn-cat', t.category));
        lastCat = t.category;
      }
      const row = el('button', 'tn-row' + (t.slug === state.topic ? ' on' : ''));
      row.append(el('span', 'tn-rank', t.kind === 'craft' ? '·' : String(t.rank)));
      const mid = el('span', 'tn-mid');
      mid.append(el('span', 'tn-title', t.title));
      const sub = el('span', 'tn-sub');
      if (t.rare) sub.append(el('span', 'tn-rare', 'rare — no problem here uses it'));
      else if (t.kind === 'craft') sub.append(el('span', 'tn-badge', 'method'));
      else sub.append(el('span', 'tn-count', t.count + ' problems'));
      if (t.solved) sub.append(el('span', 'tn-solved', t.solved + ' solved'));
      if (!t.hasArticle) sub.append(el('span', 'tn-todo', 'no chapter yet'));
      mid.append(sub);
      row.append(mid);
      if (t.status === 'done') row.append(el('span', 'tn-done', '✓'));
      row.onclick = () => Study.open(t.slug);
      host.append(row);
    });
    $('#topicCount').textContent = shown + (q ? ' of ' + this.index.topics.length : '') + ' topics';
  },

  /* -------------------------------------------------------- one chapter */
  paintTopic() {
    const d = this.current;
    const pane = $('#topic');
    pane.textContent = '';
    pane.scrollTop = 0;

    const head = el('header', 'topic-head');
    const line = el('div', 'meta-row');
    line.append(el('span', 'tag plain', d.category));
    if (d.kind === 'craft') line.append(el('span', 'tag stage', 'method chapter'));
    else if (d.rare) line.append(el('span', 'tag warnish', 'rare here — 0 of ' +
      (Study.index.problems || 0) + ' problems use it'));
    else line.append(el('span', 'tag count', '#' + d.rank + ' by use · ' + d.count + ' problems'));
    if (d.article) line.append(el('span', 'tag plain', fmtWords(d.article.words)));
    head.append(el('h1', null, d.title), line);
    if (d.covers && d.covers.length) {
      head.append(el('div', 'hint', 'also covers: ' + d.covers.join(' · ')));
    }

    const bar = el('div', 'statusbar');
    const st = (d.study || {}).status;
    [['reading', 'Reading'], ['done', 'Read']].forEach(([s, label]) => {
      const b = el('button', 'statusbtn ' + (s === 'done' ? 'solved' : 'attempted'), label);
      b.setAttribute('aria-pressed', st === s ? 'true' : 'false');
      b.onclick = () => {
        const next = st === s ? '' : s;
        d.study.status = next;
        const t = Study.index.topics.find(x => x.slug === d.slug);
        if (t) t.status = next;
        saver.queueTo('study:' + d.slug, 'api/study/' + encodeURIComponent(d.slug),
                      { status: next }, 0);
        Study.paintTopic(); Study.paintList();
      };
      bar.append(b);
    });
    if (state.current) {
      const back = el('button', 'statusbtn mark', '← back to ' + state.current.title);
      back.onclick = () => Study.close();
      bar.append(back);
    }
    head.append(bar);
    pane.append(head);

    if (!d.article) {
      pane.append(callout('warn', 'This chapter has not been written yet.',
        'The topic is mapped and its practice queue below is live; the article is pending.'));
    } else {
      if (d.article.toc.length > 3) pane.append(toc(d.article.toc));
      const body = el('article', 'chapter prose');
      body.innerHTML = d.article.html;
      pane.append(body);
      this.wireArticle(body);
    }

    if (d.related.length) {
      const rel = el('div', 'related');
      rel.append(el('h2', 'section', 'Read around it'));
      const wrap = el('div', 'chips');
      d.related.forEach(r => {
        const b = el('button', 'chip ' + (r.kind === 'prerequisite' ? 'pre' : 'next'));
        b.append(el('span', 'chip-kind', r.kind === 'prerequisite' ? 'needs' : 'next'),
                 el('span', null, r.title));
        if (!r.hasArticle) b.append(el('span', 'chip-kind', 'pending'));
        b.onclick = () => Study.open(r.slug);
        wrap.append(b);
      });
      rel.append(wrap);
      pane.append(rel);
    }

    pane.append(this.queue());

    pane.append(el('h2', 'section', 'Your notes on this topic'));
    const notes = el('textarea', 'topic-notes');
    notes.placeholder = 'The version of this you would write for yourself.';
    notes.value = (d.study || {}).notes || '';
    notes.oninput = () => {
      d.study.notes = notes.value;
      saver.queueTo('studynotes:' + d.slug, 'api/study/' + encodeURIComponent(d.slug),
                    { notes: notes.value });
    };
    pane.append(notes, el('span', 'saved', 'saved as you type, in progress.db'));
  },

  /* practice queue: the problems in this bank that drill the topic */
  queue() {
    const d = this.current;
    const box = el('section', 'queue');
    box.append(el('h2', 'section', 'Practise it'));
    if (!d.queue.length) {
      box.append(el('div', 'hint', d.kind === 'craft'
        ? 'No queue: this chapter is about how you work, so practise it on every problem.'
        : 'No problem in the bank uses this topic. It is rare here — worth knowing, ' +
          'but nothing to drill against locally.'));
      return box;
    }
    const done = d.queue.filter(q => q.status === 'solved').length;
    box.append(el('div', 'hint', d.queue.length + ' problems, easiest first' +
      (d.queueTotal > d.queue.length ? ' (of ' + d.queueTotal + ')' : '') +
      ' · ' + done + ' solved'));
    const list = el('div', 'qlist');
    d.queue.forEach(q => {
      const row = el('button', 'qrow' + (q.status ? ' ' + q.status : ''));
      row.append(el('span', 'qmark', q.status === 'solved' ? '✓' : q.status ? '·' : ''));
      row.append(el('span', 'qtitle', q.title));
      const tags = el('span', 'qtags');
      if (q.difficulty) tags.append(el('span', 'tag ' + q.difficulty, q.difficulty));
      if (q.company) tags.append(el('span', 'tag company', q.company));
      if (q.hasSolution) tags.append(el('span', 'tag count', 'solution'));
      row.append(tags);
      row.onclick = async () => { Study.close(); await openProblem(q.id); };
      list.append(row);
    });
    box.append(list);
    return box;
  },

  /* runnable snippets and self-check answers inside the article */
  wireArticle(root) {
    const d = this.current;
    const scratch = (d.study || {}).scratch || {};

    root.querySelectorAll('.snippet').forEach(box => {
      const idx = box.getAttribute('data-snippet');
      const code = box.querySelector('code');
      const saved = scratch[idx];
      if (saved != null) code.textContent = saved;
      const bar = el('div', 'snippet-bar');
      bar.append(el('span', 'snippet-lang', box.getAttribute('data-lang') || 'text'));
      if (box.classList.contains('runnable')) {
        code.setAttribute('contenteditable', 'plaintext-only');
        code.spellcheck = false;
        code.addEventListener('input', () => {
          const s = Object.assign({}, (Study.current.study || {}).scratch || {});
          s[idx] = code.textContent;
          Study.current.study.scratch = s;
          saver.queueTo('studyscratch:' + d.slug,
                        'api/study/' + encodeURIComponent(d.slug), { scratch: s });
        });
        const run = el('button', 'snippet-run', 'Run');
        const out = el('pre', 'snippet-out');
        out.hidden = true;
        run.onclick = async () => {
          run.disabled = true; run.textContent = 'running…';
          out.hidden = false; out.className = 'snippet-out';
          out.textContent = '';
          try {
            const r = await api('api/scratch', {
              method: 'POST', headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ snippet: code.textContent }),
            });
            const text = [r.printed || '', r.value ? '=> ' + r.value : '',
                          r.error || ''].filter(Boolean).join('\n').trim();
            out.textContent = text || '(no output)';
            if (r.error) out.className = 'snippet-out bad';
          } catch (e) {
            out.className = 'snippet-out bad';
            out.textContent = e.message;
          }
          run.disabled = false; run.textContent = 'Run';
        };
        const reset = el('button', 'snippet-reset', 'Reset');
        reset.title = 'Put the chapter’s version back';
        reset.onclick = () => {
          const s = Object.assign({}, (Study.current.study || {}).scratch || {});
          delete s[idx];
          Study.current.study.scratch = s;
          saver.queueTo('studyscratch:' + d.slug,
                        'api/study/' + encodeURIComponent(d.slug), { scratch: s }, 0);
          const fresh = (d.article.snippets[idx] || {}).code || '';
          code.textContent = fresh;
        };
        const toEditor = el('button', 'snippet-reset', 'To editor');
        toEditor.title = 'Copy this into the problem editor';
        toEditor.onclick = () => {
          if (!state.editor) { toEditor.textContent = 'open a problem first'; return; }
          state.editor.setValue(code.textContent);
          Study.close();
        };
        bar.append(run, reset, toEditor);
        box.append(bar, out);
      } else {
        box.append(bar);
      }
    });

    const checked = new Set(((d.study || {}).checked) || []);
    root.querySelectorAll('.check').forEach(box => {
      const n = box.getAttribute('data-check');
      const btn = box.querySelector('.reveal');
      const ans = box.querySelector('.a');
      if (checked.has(Number(n))) { ans.hidden = false; btn.textContent = 'Hide answer'; }
      btn.onclick = () => {
        ans.hidden = !ans.hidden;
        btn.textContent = ans.hidden ? 'Show answer' : 'Hide answer';
        if (ans.hidden) checked.delete(Number(n)); else checked.add(Number(n));
        Study.current.study.checked = Array.from(checked);
        saver.queueTo('studychecks:' + d.slug, 'api/study/' + encodeURIComponent(d.slug),
                      { checked: Array.from(checked) }, 0);
      };
    });

    /* [[topic]] links render as ?topic=slug; keep them inside the app */
    root.querySelectorAll('a.tlink').forEach(a => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        const slug = (a.getAttribute('href') || '').replace(/^\?study=/, '');
        if (slug) Study.open(slug);
      });
    });
  },

  wire() {
    const q = $('#topicQ');
    q.oninput = () => { Study.filter = q.value; Study.paintList(); };
    $('#studyCloseBtn').onclick = () => Study.close();
    wireStudySplitter();
  },
};

/* -------------------------------------------------------------- helpers */
function show(on) {
  $('#study').hidden = !on;
  $('#workspace').hidden = on;
  $('#studyBtn').setAttribute('aria-pressed', on ? 'true' : 'false');
  document.body.classList.toggle('studying', on);
}

function fmtWords(n) {
  return n >= 1000 ? Math.round(n / 100) / 10 + 'k words' : n + ' words';
}

function callout(kind, title, text) {
  const c = el('div', 'callout ' + kind);
  c.innerHTML = '<b>' + esc(title) + '</b> ' + esc(text || '');
  return c;
}

function toc(items) {
  const box = el('nav', 'toc');
  box.append(el('div', 'toc-head', 'In this chapter'));
  const list = el('div', 'toc-list');
  items.filter(i => i.level === 2).forEach(i => {
    const a = el('button', 'toc-link', i.text);
    a.onclick = () => {
      const t = document.getElementById(i.id);
      if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    list.append(a);
  });
  box.append(list);
  return box;
}

function welcome(index) {
  const box = el('div', 'welcome');
  box.append(el('h1', null, 'Study space'));
  const written = index.withArticles;
  box.append(el('p', 'lede',
    index.topics.length + ' topics, ranked by how many of the ' +
    index.problems.toLocaleString() + ' problems in this bank actually use them. ' +
    written + ' chapters written. Pick one on the left, or start at the top.'));
  const grid = el('div', 'welcome-grid');
  index.topics.filter(t => t.kind !== 'craft').slice(0, 12).forEach(t => {
    const card = el('button', 'wcard');
    card.append(el('div', 'wcard-title', t.title));
    card.append(el('div', 'wcard-sub', t.count + ' problems · #' + t.rank));
    if (t.summary) card.append(el('div', 'wcard-sum', t.summary));
    card.onclick = () => Study.open(t.slug);
    grid.append(card);
  });
  box.append(grid);
  const rare = index.topics.filter(t => t.rare);
  if (rare.length) {
    box.append(el('h2', 'section', 'Rare here'));
    box.append(el('p', 'hint',
      'Nothing in this bank uses these. They are in the canon because interviews ' +
      'elsewhere do use them, and the chapters say so plainly.'));
    const wrap = el('div', 'chips');
    rare.forEach(t => {
      const b = el('button', 'chip', t.title);
      b.onclick = () => Study.open(t.slug);
      wrap.append(b);
    });
    box.append(wrap);
  }
  return box;
}

/* the same drag-to-resize as the workspace, on its own key */
function wireStudySplitter() {
  const bar = $('#studySplit'), main = $('#study');
  const KEY = 'fp:studysplit';
  const apply = (px) => main.style.gridTemplateColumns = px + 'px 6px 1fr';
  const saved = parseInt(localStorage.getItem(KEY) || '0', 10);
  if (saved > 180) apply(saved);
  let dragging = false;
  bar.addEventListener('mousedown', (e) => { dragging = true; e.preventDefault();
    document.body.classList.add('dragging'); });
  window.addEventListener('mousemove', (e) => {
    if (!dragging) return;
    const px = Math.max(220, Math.min(e.clientX - main.getBoundingClientRect().left,
                                      window.innerWidth - 420));
    apply(px); remember('studysplit', String(px));
  });
  window.addEventListener('mouseup', () => {
    dragging = false; document.body.classList.remove('dragging');
  });
  bar.addEventListener('dblclick', () => { apply(320); remember('studysplit', '320'); });
}
