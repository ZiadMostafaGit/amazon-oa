/* The study space: 17 subjects, 150 chapters filed under them as a prerequisite
 * tree, the problems that practise each one, and the state of your reading -
 * all of it kept server-side like everything else.
 *
 * Loaded before app.js; it borrows $, el, esc, api, url, state and openProblem
 * from there, which is safe because nothing here runs before boot(). */
'use strict';

const Study = {
  index: null,           // {topics, subjects, ...}
  current: null,         // the open chapter's payload
  subject: null,         // the open subject's payload (when no chapter is open)
  reviews: null,         // {due, later}: spaced re-solves
  filter: '',
  folded: null,          // Set of subject slugs folded shut in the sidebar
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
    if (slug.startsWith('subject:')) return this.openSubject(slug.slice(8));
    show(true);
    state.studyOpen = true;
    state.topic = slug;
    await this.load();
    this.unfoldFor(slug);
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
    this.subject = null;
    this.paintTopic();
    pushUrl();
  },

  /* a subject is everything about one thing - Graphs is BFS, DFS, topological
   * sort and the rest - shown as the path through its chapters */
  async openSubject(slug) {
    show(true);
    state.studyOpen = true;
    state.topic = 'subject:' + slug;
    await this.load();
    this.folded.delete(slug); this.rememberFolds();
    this.paintList();
    const pane = $('#topic');
    pane.textContent = '';
    pane.append(el('div', 'hint pad', 'Loading ' + slug + '…'));
    try {
      const boot = window.__BOOT__;
      if (boot && boot.subject && boot.subject.slug === slug) {
        this.subject = boot.subject;
        boot.subject = null;
      } else {
        this.subject = await api('api/subjects/' + encodeURIComponent(slug));
      }
    } catch (e) {
      pane.textContent = '';
      pane.append(el('div', 'callout warn', 'Could not open that subject: ' + e.message));
      return;
    }
    this.current = null;
    this.paintSubject();
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
    if (!this.reviews) {
      try { this.reviews = (boot && boot.reviews) || await api('api/reviews'); } catch (e) {}
    }
    if (!this.folded) {
      let saved = [];
      try { saved = JSON.parse(localStorage.getItem('fp:studyfold') || '[]'); } catch (e) {}
      this.folded = new Set(Array.isArray(saved) ? saved : []);
    }
    return this.index;
  },

  rememberFolds() {
    try { localStorage.setItem('fp:studyfold', JSON.stringify(Array.from(this.folded))); }
    catch (e) {}
  },

  subjectOf(slug) {
    return (this.index.subjects || []).find(s => s.chapters.some(c => c.slug === slug));
  },

  unfoldFor(slug) {
    const s = this.subjectOf(slug);
    if (s && this.folded.has(s.slug)) { this.folded.delete(s.slug); this.rememberFolds(); }
  },

  /* ----------------------------------------------------------- the list */
  paintList() {
    const host = $('#topicList');
    host.textContent = '';
    const q = this.filter.trim().toLowerCase();
    const bySlug = {};
    this.index.topics.forEach(t => { bySlug[t.slug] = t; });
    const openSubject = state.topic.startsWith('subject:') ? state.topic.slice(8) : '';
    let shown = 0;
    (this.index.subjects || []).forEach(sub => {
      const subHit = !q || sub.name.toLowerCase().indexOf(q) >= 0;
      const rows = sub.chapters.map(c => Object.assign({ depth: c.depth }, bySlug[c.slug]))
        .filter(t => t.slug && (subHit || !q ||
          (t.title + ' ' + t.slug + ' ' + (t.covers || []).join(' ')).toLowerCase().indexOf(q) >= 0));
      if (q && !rows.length) return;
      shown += rows.length;
      /* a filter opens every group it touches; otherwise the fold is yours */
      const folded = !q && this.folded.has(sub.slug) && openSubject !== sub.slug;

      const head = el('div', 'tn-subject' + (openSubject === sub.slug ? ' on' : '') +
                                            (folded ? ' folded' : ''));
      const fold = el('button', 'tn-fold', folded ? '▸' : '▾');
      fold.title = folded ? 'Show its chapters' : 'Hide its chapters';
      fold.onclick = (e) => {
        e.stopPropagation();
        if (this.folded.has(sub.slug)) this.folded.delete(sub.slug); else this.folded.add(sub.slug);
        this.rememberFolds(); this.paintList();
      };
      const name = el('button', 'tn-subject-name');
      name.append(el('span', 'tn-title', sub.name));
      const meta = el('span', 'tn-sub');
      meta.append(el('span', 'tn-count', sub.chapters.length + ' chapters · ' +
                                         sub.count.toLocaleString() + ' problems'));
      if (sub.mastered) meta.append(el('span', 'tn-solved', sub.mastered + '/' + sub.chapters.length + ' mastered'));
      else if (sub.done) meta.append(el('span', 'tn-solved', sub.done + '/' + sub.chapters.length + ' read'));
      name.append(meta);
      name.title = 'Open the subject: its chapters in order, and one practice queue';
      name.onclick = () => Study.openSubject(sub.slug);
      head.append(fold, name);
      host.append(head);
      if (folded) return;

      rows.forEach((t, i) => {
        const row = el('button', 'tn-row d' + Math.min(t.depth || 0, 3) +
                                 (t.slug === state.topic ? ' on' : ''));
        row.append(el('span', 'tn-rank', t.kind === 'craft' ? '·' : String(i + 1)));
        row.title = t.kind === 'craft' ? 'method chapter' : '#' + t.rank + ' in the bank by use';
        const mid = el('span', 'tn-mid');
        mid.append(el('span', 'tn-title', t.title));
        const sub = el('span', 'tn-sub');
        if (t.rare) sub.append(el('span', 'tn-rare', 'rare — no problem here uses it'));
        else if (t.kind === 'craft') sub.append(el('span', 'tn-badge', 'method'));
        else sub.append(el('span', 'tn-count', nProblems(t.count)));
        if (t.solved) sub.append(el('span', 'tn-solved', t.solved + ' solved'));
        if (!t.hasArticle) sub.append(el('span', 'tn-todo', 'no chapter yet'));
        mid.append(sub);
        row.append(mid);
          if (t.mastery && t.mastery.of) {
          row.append(t.mastery.done === t.mastery.of ? el('span', 'tn-done', '✓')
                                                     : masteryBar(t.mastery, false));
        }
        row.onclick = () => Study.open(t.slug);
        host.append(row);
      });
    });
    const count = $('#topicCount');
    count.textContent = shown + (q ? ' of ' + this.index.topics.length : '') +
      ' chapters in ' + (this.index.subjects || []).length + ' subjects';
    if (!q) {
      const all = (this.index.subjects || []).map(s => s.slug);
      const allFolded = all.every(x => this.folded.has(x));
      const btn = el('button', 'tn-foldall', allFolded ? 'unfold all' : 'fold all');
      btn.onclick = () => {
        this.folded = new Set(allFolded ? [] : all);
        this.rememberFolds(); this.paintList();
      };
      count.append(btn);
    }
    /* keep what is open in view, under its sticky subject header */
    const on = host.querySelector('.tn-row.on, .tn-subject.on');
    if (on && !q) {
      /* the subject header is sticky, so leave room for it above the row */
      let head = on.previousElementSibling;
      while (head && !head.classList.contains('tn-subject')) head = head.previousElementSibling;
      const place = () => {
        const lead = on.classList.contains('tn-row') ? (head ? head.offsetHeight + 16 : 64) : 8;
        const top = on.offsetTop - host.offsetTop - lead;
        if (top < host.scrollTop || on.offsetTop - host.offsetTop > host.scrollTop + host.clientHeight - 80) {
          host.scrollTop = Math.max(0, top);
        }
      };
      place();
      requestAnimationFrame(place);          // again once fonts have settled the heights
    }
  },

  /* -------------------------------------------------------- one subject */
  paintSubject() {
    const d = this.subject;
    const pane = $('#topic');
    pane.textContent = '';
    pane.scrollTop = 0;

    const head = el('header', 'topic-head');
    const line = el('div', 'meta-row');
    line.append(el('span', 'tag plain', 'subject'));
    line.append(el('span', 'tag count', d.chapters.length + ' chapters · ' +
      d.count.toLocaleString() + ' of ' + d.problems.toLocaleString() + ' problems'));
    const written = d.chapters.filter(c => c.hasArticle).length;
    line.append(el('span', 'tag plain', written + ' written'));
    const read = d.chapters.filter(c => c.status === 'done').length;
    if (read) line.append(el('span', 'tag easy', read + ' read'));
    if (d.solved) line.append(el('span', 'tag easy', d.solved + ' solved'));
    head.append(el('h1', null, d.name), line);
    if (d.blurb) head.append(el('p', 'lede', d.blurb));
    if (state.current) {
      const bar = el('div', 'statusbar');
      const back = el('button', 'statusbtn mark', '← back to ' + state.current.title);
      back.onclick = () => Study.close();
      bar.append(back);
      head.append(bar);
    }
    pane.append(head);

    if (d.before.length) {
      const box = el('div', 'related');
      box.append(el('h2', 'section', 'Know these first'));
      box.append(el('p', 'hint', 'Chapters in other subjects that this one builds on.'));
      box.append(chipRow(d.before, 'needs'));
      pane.append(box);
    }

    const path = el('section', 'path');
    path.append(el('h2', 'section', 'The path through it'));
    path.append(el('p', 'hint', 'In order: a chapter never comes before one it needs. ' +
      'Indented chapters build on the one above them.'));
    const list = el('ol', 'path-list');
    d.chapters.forEach((c, i) => {
      const li = el('li', 'pcard d' + Math.min(c.depth || 0, 3) +
                          (c.status === 'done' ? ' done' : ''));
      const btn = el('button', 'pcard-btn');
      const top = el('div', 'pcard-top');
      top.append(el('span', 'pcard-n', c.status === 'done' ? '✓' : String(i + 1)));
      top.append(el('span', 'pcard-title', c.title));
      const tags = el('span', 'pcard-tags');
      if (c.kind === 'craft') tags.append(el('span', 'tag stage', 'method'));
      else if (c.rare) tags.append(el('span', 'tag warnish', 'rare here'));
      else tags.append(el('span', 'tag count', nProblems(c.count)));
      if (c.solved) tags.append(el('span', 'tag easy', c.solved + ' solved'));
      if (c.status === 'reading') tags.append(el('span', 'tag medium', 'reading'));
      if (!c.hasArticle) tags.append(el('span', 'tag plain', 'no chapter yet'));
      else tags.append(el('span', 'tag plain', fmtWords(c.words)));
      if (c.mastery && c.mastery.of) tags.append(masteryBar(c.mastery, false));
      top.append(tags);
      btn.append(top);
      if (c.summary) btn.append(el('div', 'pcard-sum', c.summary));
      if (c.covers && c.covers.length) {
        btn.append(el('div', 'pcard-covers', 'also covers: ' + c.covers.join(' · ')));
      }
      btn.onclick = () => Study.open(c.slug);
      li.append(btn);
      list.append(li);
    });
    path.append(list);
    pane.append(path);

    if (d.beyond.length) {
      const box = el('div', 'related');
      box.append(el('h2', 'section', 'Filed elsewhere, but about this'));
      box.append(el('p', 'hint', 'Chapters in other subjects that lean on this one — ' +
        'read them when the path above is done.'));
      box.append(chipRow(d.beyond, 'next'));
      pane.append(box);
    }

    if ((d.reviewsDue || []).length) pane.append(reviewList(d.reviewsDue, 'Owed a re-solve in ' + d.name));

    if ((d.mistakes || []).length) {
      const box = el('section', 'mistakes');
      box.append(el('h2', 'section', 'Where it goes wrong for you'));
      box.append(el('p', 'hint', 'From the post-mortems you wrote on this subject\u2019s problems.'));
      const most = d.mistakes[0][1];
      d.mistakes.forEach(([kind, n]) => {
        const row = el('div', 'mrow');
        row.append(el('span', 'mkind', MISTAKE_LABEL[kind] || kind));
        const bar = el('span', 'mbar');
        const fill = el('i'); fill.style.width = Math.round(100 * n / most) + '%';
        bar.append(fill);
        row.append(bar, el('span', 'mnum', String(n)));
        box.append(row);
      });
      pane.append(box);
    }

    pane.append(this.subjectQueue());
  },

  subjectQueue() {
    const d = this.subject;
    const box = el('section', 'queue');
    box.append(el('h2', 'section', 'Practise the whole subject'));
    if (!d.queue.length) {
      box.append(el('div', 'hint', 'No problem in the bank uses this subject.'));
      return box;
    }
    const done = d.queue.filter(q => q.status === 'solved').length;
    box.append(el('div', 'hint', d.queue.length + ' problems, the ones several chapters ' +
      'claim first' + (d.queueTotal > d.queue.length ? ' (of ' + d.queueTotal + ')' : '') +
      ' · ' + done + ' solved'));
    const list = el('div', 'qlist');
    d.queue.forEach(q => {
      const row = el('button', 'qrow' + (q.status ? ' ' + q.status : ''));
      row.append(el('span', 'qmark', q.status === 'solved' ? '✓' : q.status ? '·' : ''));
      row.append(el('span', 'qtitle', q.title));
      const tags = el('span', 'qtags');
      if (q.difficulty) tags.append(el('span', 'tag ' + q.difficulty, q.difficulty));
      if (q.company) tags.append(el('span', 'tag company', q.company));
      if (q.chapters > 1) tags.append(el('span', 'tag plain', q.chapters + ' chapters'));
      if (q.hasSolution) tags.append(el('span', 'tag count', 'solution'));
      row.append(tags);
      row.onclick = async () => { Study.close(); await openProblem(q.id); };
      list.append(row);
    });
    box.append(list);
    return box;
  },

  /* -------------------------------------------------------- one chapter */
  paintTopic() {
    const d = this.current;
    const pane = $('#topic');
    pane.textContent = '';
    pane.scrollTop = 0;

    const head = el('header', 'topic-head');
    const line = el('div', 'meta-row');
    const cat = el('button', 'tag topic link', d.category);
    cat.title = 'Everything in ' + d.category + ', in order';
    cat.onclick = () => Study.openSubject(d.subject);
    line.append(cat);
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
    if (d.mastery && d.mastery.of) head.append(masteryBar(d.mastery, true));
    pane.append(head);

    /* attempt before reading: a chapter read as the answer to a question you
     * have already struggled with sticks; one read cold does not */
    const tried = ((d.study || {}).extra || {}).tried;
    const gated = !!(d.article && d.tryFirst && !tried);
    if (d.tryFirst) pane.append(this.tryFirst(gated));

    if (!d.article) {
      pane.append(callout('warn', 'This chapter has not been written yet.',
        'The topic is mapped and its practice queue below is live; the article is pending.'));
    } else {
      const wrap = el('div', 'chapter-wrap' + (gated ? ' gated' : ''));
      if (d.article.toc.length > 3) wrap.append(toc(d.article.toc));
      const body = el('article', 'chapter prose');
      body.innerHTML = d.article.html;
      wrap.append(body);
      pane.append(wrap);
      this.wireArticle(body);
      if (gated) {
        const lift = el('button', 'btn gate-lift', 'Read without trying first');
        lift.onclick = () => this.markTried({ pid: d.tryFirst.id, skipped: true, at: new Date().toISOString() });
        wrap.append(lift);
      }
    }

    if (d.drill && d.drill.length) pane.append(this.drill());

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

  tryFirst(gated) {
    const d = this.current;
    const t = d.tryFirst;
    const tried = ((d.study || {}).extra || {}).tried;
    const box = el('section', 'tryfirst' + (gated ? ' hot' : ''));
    const line = el('div', 'tf-head');
    line.append(el('span', 'tn-badge', gated ? 'before you read' : 'you tried first'));
    box.append(line);
    const row = el('button', 'qrow');
    row.append(el('span', 'qmark', t.status === 'solved' ? '✓' : t.status ? '·' : ''));
    row.append(el('span', 'qtitle', t.title));
    const tags = el('span', 'qtags');
    if (t.difficulty) tags.append(el('span', 'tag ' + t.difficulty, t.difficulty));
    if (t.company) tags.append(el('span', 'tag company', t.company));
    if (t.hasSolution) tags.append(el('span', 'tag count', 'solution'));
    row.append(tags);
    row.onclick = () => this.goTry(t);
    if (gated) {
      box.append(el('p', 'hint',
        'Give this fifteen minutes before the chapter. Struggling first and then reading ' +
        'is how the idea sticks; it does not matter whether you solve it.'));
      box.append(row);
      const go = el('button', 'btn primary', 'Open it with a 15-minute clock');
      go.onclick = () => this.goTry(t);
      const goRow = el('div', 'rowbtns'); goRow.append(go); box.append(goRow);
    } else {
      box.append(row);
      if (tried && tried.skipped) box.append(el('span', 'hint', 'skipped the attempt — it is still worth doing'));
    }
    return box;
  },

  goTry(t) {
    const d = this.current;
    const tried = ((d.study || {}).extra || {}).tried;
    if (!tried || tried.skipped) {
      this.markTried({ pid: t.id, at: new Date().toISOString() }, true);
    }
    if (window.Timer) Timer.start(15 * 60000);
    Study.close();
    openProblem(t.id);
  },

  markTried(tried, quiet) {
    const d = this.current;
    d.study.extra = Object.assign({}, d.study.extra || {}, { tried: tried });
    saver.queueTo('studyextra:' + d.slug, 'api/study/' + encodeURIComponent(d.slug),
                  { extra: { tried: tried } }, 0);
    if (!tried.skipped && d.mastery) { d.mastery.steps.tried = true; d.mastery.done += 1; }
    if (!quiet) this.paintTopic();
  },

  saveExtra(patch) {
    const d = this.current;
    d.study.extra = Object.assign({}, d.study.extra || {}, patch);
    saver.queueTo('studyextra:' + d.slug, 'api/study/' + encodeURIComponent(d.slug),
                  { extra: patch }, 0);
  },

  /* recognition: this topic's problems mixed with its neighbours' */
  drill() {
    const d = this.current;
    const box = el('section', 'drill');
    box.append(el('h2', 'section', 'Is it this topic?'));
    const prev = ((d.study || {}).extra || {}).drill;
    box.append(el('p', 'hint',
      'Half of these want ' + d.title + '; half are neighbours that look like it. ' +
      'Decide from the opening lines, the way you would in the first minute of an interview.' +
      (prev ? ' Last time: ' + prev.score + ' of ' + prev.total + '.' : '')));
    const answers = {};
    const cards = el('div', 'drill-cards');
    const score = el('div', 'drill-score');
    const finish = () => {
      const total = d.drill.length;
      const right = d.drill.filter(x => answers[x.id] === x.isTopic).length;
      score.textContent = right + ' of ' + total + ' right';
      score.className = 'drill-score ' + (right >= total - 1 ? 'good' : 'meh');
      this.saveExtra({ drill: { score: right, total: total, at: new Date().toISOString() } });
      if (d.mastery) {
        const was = d.mastery.steps.drilled;
        d.mastery.steps.drilled = right >= total - 1;
        if (!was && d.mastery.steps.drilled) d.mastery.done += 1;
        const bar = $('.mastery', $('#topic'));
        if (bar) bar.replaceWith(masteryBar(d.mastery, true));
      }
    };
    d.drill.forEach(x => {
      const c = el('div', 'drill-card');
      const top = el('div', 'drill-top');
      top.append(el('span', 'pcard-title', x.title));
      const tags = el('span', 'pcard-tags');
      if (x.difficulty) tags.append(el('span', 'tag ' + x.difficulty, x.difficulty));
      if (x.company) tags.append(el('span', 'tag company', x.company));
      top.append(tags);
      c.append(top, el('p', 'drill-text', x.excerpt));
      const btns = el('div', 'rowbtns');
      const yes = el('button', 'btn', 'Yes, ' + d.title);
      const no = el('button', 'btn', 'No, something else');
      const verdict = el('span', 'drill-verdict');
      const answer = (v) => {
        if (x.id in answers) return;
        answers[x.id] = v;
        const ok = v === x.isTopic;
        verdict.textContent = ok ? '✓ right' : ('✗ it is ' + (x.isTopic ? '' : 'not ') + d.title);
        verdict.className = 'drill-verdict ' + (ok ? 'good' : 'bad');
        c.classList.add(ok ? 'right' : 'wrong');
        const open = el('button', 'btn ghost', 'open it');
        open.onclick = async () => { Study.close(); await openProblem(x.id); };
        btns.append(open);
        if (Object.keys(answers).length === d.drill.length) finish();
      };
      yes.onclick = () => answer(true);
      no.onclick = () => answer(false);
      btns.append(yes, no, verdict);
      c.append(btns);
      cards.append(c);
    });
    box.append(cards, score);
    const again = el('button', 'btn ghost', 'Another set');
    again.onclick = async () => {
      try {
        const fresh = await api('api/topics/' + encodeURIComponent(d.slug));
        d.drill = fresh.drill;
        box.replaceWith(this.drill());
      } catch (e) {}
    };
    const againRow = el('div', 'rowbtns'); againRow.append(again); box.append(againRow);
    return box;
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
        const spec = d.article.snippets[idx] || {};
        const recalled = (((d.study || {}).extra || {}).recall || {})[idx];
        let recalling = false;
        const memBadge = el('span', 'snippet-recalled', recalled ? '✓ written from memory' : '');
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
            /* the block's own asserts are the grader: clean exit from a body
             * you typed yourself, with no `...` left in it, is a recall */
            if (!r.error && recalling && code.textContent.indexOf('...  # write it') < 0) {
              recalling = false;
              const recall = Object.assign({}, ((d.study || {}).extra || {}).recall || {});
              recall[idx] = true;
              Study.saveExtra({ recall: recall });
              memBadge.textContent = '✓ written from memory';
              if (d.mastery && !d.mastery.steps.recalled) {
                d.mastery.steps.recalled = true; d.mastery.done += 1;
                const bar = $('.mastery', $('#topic'));
                if (bar) bar.replaceWith(masteryBar(d.mastery, true));
              }
            }
          } catch (e) {
            out.className = 'snippet-out bad';
            out.textContent = e.message;
          }
          run.disabled = false; run.textContent = 'Run';
        };
        let fromMemory = null;
        if (spec.stub) {
          fromMemory = el('button', 'snippet-reset', 'From memory');
          fromMemory.title = 'Blank the function bodies; the asserts grade what you type';
          fromMemory.onclick = () => {
            code.textContent = spec.stub;
            recalling = true;
            out.hidden = true;
            code.focus();
          };
        }
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
        bar.append(run);
        if (fromMemory) bar.append(fromMemory);
        bar.append(reset, toEditor, memBadge);
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

function nProblems(n) {
  return n + (n === 1 ? ' problem' : ' problems');
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

function chipRow(items, kind) {
  const wrap = el('div', 'chips');
  items.forEach(r => {
    const b = el('button', 'chip ' + (kind === 'needs' ? 'pre' : 'next'));
    b.append(el('span', 'chip-kind', r.subjectName || kind), el('span', null, r.title));
    if (!r.hasArticle) b.append(el('span', 'chip-kind', 'pending'));
    b.onclick = () => Study.open(r.slug);
    wrap.append(b);
  });
  return wrap;
}

const MISTAKE_LABEL = {
  'misread': 'misread the statement', 'wrong-tool': 'picked the wrong tool',
  'wrong-state': 'wrong state or invariant', 'off-by-one': 'off by one',
  'edge-case': 'missed an edge case', 'complexity': 'too slow', 'bug': 'plain bug',
  'none': 'nothing went wrong',
};

/* n of m steps, as a row of pips; the long form names them */
function masteryBar(m, long) {
  const names = { tried: 'tried a problem first', read: 'read the chapter',
                  recalled: 'wrote the code from memory', drilled: 'told it apart from its neighbours',
                  solved: 'solved ' + m.solvedOf + ' of its problems' };
  const box = el('span', 'mastery' + (long ? ' long' : ''));
  box.title = m.done + ' of ' + m.of + ' mastery steps';
  Object.entries(m.steps).forEach(([k, v]) => {
    if (v === null) return;
    const pip = el('i', 'pip' + (v ? ' on' : ''));
    pip.title = names[k] + (k === 'solved' && !v ? ' (' + m.solved + ' so far)' : '');
    if (long) {
      const lab = el('span', 'pip-label' + (v ? ' on' : ''));
      lab.append(pip, document.createTextNode(names[k]));
      box.append(lab);
    } else box.append(pip);
  });
  return box;
}

function reviewList(due, title) {
  const box = el('section', 'reviews');
  box.append(el('h2', 'section', title));
  box.append(el('p', 'hint', 'Solved once is forgotten in two weeks. Re-solve each from a blank editor; ' +
    'say honestly whether you needed help, and it comes back sooner or later accordingly.'));
  const list = el('div', 'qlist');
  due.forEach(r => {
    const row = el('div', 'qrow review-row');
    const open = el('button', 'qtitle', r.title);
    open.onclick = async () => { Study.close(); await openProblem(r.id); };
    const tags = el('span', 'qtags');
    if (r.difficulty) tags.append(el('span', 'tag ' + r.difficulty, r.difficulty));
    if (r.subject) tags.append(el('span', 'tag plain', r.subject));
    tags.append(el('span', 'tag count', 'stage ' + (r.stage + 1) + (r.lapses ? ' · ' + r.lapses + ' lapses' : '')));
    const pass = el('button', 'btn', 'Re-solved it');
    const fail = el('button', 'btn ghost', 'Needed help');
    const mark = async (passed) => {
      pass.disabled = fail.disabled = true;
      try {
        await api('api/reviews/' + encodeURIComponent(r.id), {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ passed: passed }),
        });
        row.classList.add(passed ? 'solved' : 'attempted');
        tags.append(el('span', 'tag ' + (passed ? 'easy' : 'medium'),
                       passed ? 'next in ' + [10, 30, 90, 90][Math.min(r.stage, 3)] + ' days' : 'back tomorrow'));
      } catch (e) { pass.disabled = fail.disabled = false; }
    };
    pass.onclick = () => mark(true); fail.onclick = () => mark(false);
    row.append(el('span', 'qmark', '↻'), open, tags, pass, fail);
    list.append(row);
  });
  box.append(list);
  return box;
}

function welcome(index) {
  const box = el('div', 'welcome');
  box.append(el('h1', null, 'Study space'));
  const subs = index.subjects || [];
  box.append(el('p', 'lede',
    subs.length + ' subjects, ' + index.topics.length + ' chapters, each filed under ' +
    'what it builds on. ' + index.withArticles + ' chapters written. Pick a subject to see ' +
    'everything in it in the order to learn it, or a chapter on the left.'));

  /* today's work first: what is owed, then a problem you cannot pre-classify */
  const reviews = (window.__BOOT__ && window.__BOOT__.reviews) || Study.reviews;
  if (reviews && reviews.due && reviews.due.length) {
    box.append(reviewList(reviews.due, reviews.due.length + ' owed a re-solve today'));
  } else if (reviews && reviews.later) {
    box.append(el('p', 'hint', 'Nothing owed a re-solve today; ' + reviews.later + ' scheduled.'));
  }
  const mixed = el('section', 'mixed');
  const mbtn = el('button', 'btn primary', 'Mixed drill: one problem, tool unknown');
  const mhint = el('span', 'hint', 'Drawn from the subjects you have started. Choosing the tool is the interview.');
  mbtn.onclick = async () => {
    mbtn.disabled = true;
    try {
      const r = await api('api/mixed');
      if (!r.problem) { mhint.textContent = 'No mixed drill yet: ' + r.reason + '.'; mbtn.disabled = false; return; }
      if (window.Timer) Timer.start(30 * 60000);
      Study.close(); await openProblem(r.problem.id);
    } catch (e) { mhint.textContent = e.message; mbtn.disabled = false; }
  };
  mixed.append(mbtn, mhint);
  box.append(mixed);
  const grid = el('div', 'welcome-grid');
  subs.forEach(s => {
    const card = el('button', 'wcard');
    card.append(el('div', 'wcard-title', s.name));
    card.append(el('div', 'wcard-sub', s.chapters.length + ' chapters · ' +
      s.count.toLocaleString() + ' problems' +
      (s.done ? ' · ' + s.done + ' read' : '')));
    if (s.blurb) card.append(el('div', 'wcard-sum', s.blurb));
    card.onclick = () => Study.openSubject(s.slug);
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
