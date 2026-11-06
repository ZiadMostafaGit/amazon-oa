/* The DSA path: topics in the order to learn them, problems in the order to solve them.
 *
 * One page, one column, one obvious next step. Each stage is a pattern: read its chapter,
 * solve the classic form, then the OA forms easy -> hard, then "more practice". The KHATT
 * plan schedules the same problems week by week (the W03 tag on each stage).
 *
 * Loaded before app.js; borrows $, el, esc, api, state, openProblem and Study from there. */
'use strict';

const Path = {
  data: null,
  open: new Set(),        // stage slugs expanded by hand
  loaded: false,

  async show() {
    if (state.studyOpen) Study.close();
    if (state.finderOpen) Finder.close();
    state.pathOpen = true;
    $('#pathView').hidden = false;
    $('#workspace').hidden = true;
    $('#pathBtn').setAttribute('aria-pressed', 'true');
    document.body.classList.add('pathing');
    if (typeof closeDrawer === 'function') closeDrawer();
    pushUrl();
    await this.load();
    this.paint();
  },

  close() {
    state.pathOpen = false;
    $('#pathView').hidden = true;
    $('#workspace').hidden = state.studyOpen || state.finderOpen;
    $('#pathBtn').setAttribute('aria-pressed', 'false');
    document.body.classList.remove('pathing');
    pushUrl();
  },

  toggle() { state.pathOpen ? this.close() : this.show(); },

  async load() {
    const host = $('#pathPane');
    if (!this.data) host.innerHTML = '<div class="hint pad">Loading your path…</div>';
    try {
      this.data = await api('api/path');
    } catch (e) {
      host.innerHTML = '';
      host.append(el('div', 'callout warn', 'Could not load the path: ' + e.message));
    }
    try { this.open = new Set(JSON.parse(localStorage.getItem('fp:path:open') || '[]')); } catch (e) { /* private mode */ }
  },

  remember() {
    try { localStorage.setItem('fp:path:open', JSON.stringify([...this.open])); } catch (e) { /* private mode */ }
  },

  async go(id) {
    this.close();
    await openProblem(id);
  },

  paint() {
    const d = this.data;
    const host = $('#pathPane');
    if (!d) return;
    host.textContent = '';
    const page = el('div', 'path-page');

    /* ---- the one thing to do next ---- */
    const head = el('header', 'path-hero');
    head.append(el('div', 'eyebrow', 'Your DSA path'));
    head.append(el('h1', null, 'Learn a pattern, then meet it the way companies ask it.'));
    const pct = d.planTotal ? Math.round(100 * d.planSolved / d.planTotal) : 0;
    const next = el('div', 'path-next');
    if (d.next) {
      const left = el('div', 'pn-left');
      left.append(el('div', 'pn-label', 'Next up · Stage ' + d.next.number + ' · ' + d.next.stageTitle));
      left.append(el('div', 'pn-title', d.next.title));
      const go = el('button', 'btn primary big', 'Continue  →');
      go.onclick = () => this.go(d.next.id);
      next.append(left, go);
    } else {
      next.append(el('div', 'pn-title', 'Every plan problem is solved. The "more practice" lists are next.'));
    }
    head.append(next);
    const meter = el('div', 'path-meter');
    meter.append(el('span', null, d.planSolved + ' of ' + d.planTotal + ' path problems solved'));
    const bar = el('div', 'bar'); const fill = el('i'); fill.style.width = pct + '%'; bar.append(fill);
    meter.append(bar);
    head.append(meter);
    if (Study.reviews && (Study.reviews.due || []).length) {
      const rv = el('button', 'linkbtn due', (Study.reviews.due.length) + ' re-solves due today →');
      rv.onclick = () => { this.close(); Study.openIndex(); };
      head.append(rv);
    }
    page.append(head);

    /* ---- how to use it, short ---- */
    const how = el('details', 'path-how');
    how.append(el('summary', null, 'How to work a stage'));
    const ol = el('ol');
    [
      ['Read the chapter', 'and do its drill. It takes 30–60 minutes and makes the rest cheap.'],
      ['Solve the classic form first', 'The clean textbook version, so you learn the pattern without a story in the way.'],
      ['Then the OA forms, easy → hard', 'The same pattern wrapped in a story, as companies ask it. Give each 25 minutes before opening a hint; the hints open one at a time and name the pattern last.'],
      ['Mark it solved, or "needed help"', 'Solved problems come back for a re-solve at 3, 10, 30 and 90 days; "needed help" brings it back tomorrow. Re-solving from a blank editor is what makes it stick.'],
      ['Done with the set?', 'Open "more practice" for the same pattern, or move on. Each stage is one week of the KHATT plan.'],
    ].forEach(([b, t]) => { const li = el('li'); li.append(el('b', null, b + '. '), document.createTextNode(t)); ol.append(li); });
    how.append(ol);
    page.append(how);

    /* ---- the phases ---- */
    const current = d.next ? d.next.stage : null;
    d.phases.forEach((ph) => {
      const sec = el('section', 'path-phase');
      const h = el('div', 'phase-head');
      h.append(el('h2', null, ph.title), el('p', null, ph.about));
      sec.append(h);
      ph.stages.forEach((st) => sec.append(this.stage(st, st.slug === current)));
      page.append(sec);
    });

    /* ---- practice sets: the plan's mixed and company weeks ---- */
    if ((d.sets || []).length) {
      const sec = el('section', 'path-phase');
      const h = el('div', 'phase-head');
      h.append(el('h2', null, 'Practice sets'),
               el('p', null, 'Mixed and company weeks from the KHATT plan: no new pattern, so they test recognition. Do them timed.'));
      sec.append(h);
      const grid = el('div', 'set-grid');
      d.sets.forEach((s) => {
        const det = el('details', 'set');
        const sm = el('summary');
        sm.append(el('span', 'wk', 'W' + String(s.week).padStart(2, '0')),
                  el('span', 'set-title', s.label),
                  el('span', 'set-count', s.solved + '/' + s.problems.length));
        det.append(sm);
        const list = el('ol', 'plist');
        s.problems.forEach((p) => list.append(this.row(p)));
        det.append(list);
        grid.append(det);
      });
      sec.append(grid);
      page.append(sec);
    }
    host.append(page);
    /* past the first stages, open on the one you are in; before that the
       "continue" card is the place to start */
    const cur = host.querySelector('.stage.current');
    if (cur && !this.scrolled && d.next && d.next.number > 2) {
      this.scrolled = true;
      cur.scrollIntoView({ block: 'start' });
    }
  },

  stage(st, isCurrent) {
    const box = el('details', 'stage' + (isCurrent ? ' current' : '') + (st.solved === st.plan.length && st.plan.length ? ' done' : ''));
    box.open = isCurrent || this.open.has(st.slug);
    box.addEventListener('toggle', () => {
      if (box.open) this.open.add(st.slug); else this.open.delete(st.slug);
      this.remember();
    });
    const sm = el('summary');
    sm.append(el('span', 'num', String(st.number)));
    const mid = el('span', 'st-mid');
    mid.append(el('span', 'st-title', st.title));
    const sub = el('span', 'st-sub');
    sub.append(el('span', 'wk', 'KHATT W' + String(st.week).padStart(2, '0')));
    if (st.amazonShare != null) sub.append(el('span', 'share', st.amazonShare + '% of recent Amazon OAs · ' + st.oaShare + '% of all OAs'));
    mid.append(sub);
    const prog = el('span', 'st-prog');
    prog.append(el('span', 'count', st.solved + '/' + st.plan.length));
    const bar = el('span', 'bar'); const fill = el('i');
    fill.style.width = (st.plan.length ? Math.round(100 * st.solved / st.plan.length) : 0) + '%';
    bar.append(fill); prog.append(bar);
    sm.append(mid, prog);
    box.append(sm);

    const body = el('div', 'st-body');
    if ((st.chapters || []).length) {
      const read = el('div', 'st-read');
      read.append(el('span', 'step', '1'), el('span', 'lab', 'Read first'));
      st.chapters.slice(0, 3).forEach((c) => {
        const b = el('button', 'chip', c.title);
        b.onclick = () => { this.close(); Study.open(c.slug); };
        read.append(b);
      });
      body.append(read);
    }
    const lab = el('div', 'st-listhead');
    lab.append(el('span', 'step', '2'), el('span', 'lab', 'Solve in this order'));
    body.append(lab);
    const list = el('ol', 'plist');
    st.plan.forEach((p, i) => list.append(this.row(p, i < (st.classics || 0) ? 'classic' : (p.oa ? 'OA' : ''))));
    body.append(list);
    if ((st.more || []).length) {
      const more = el('details', 'st-more');
      more.append(el('summary', null, 'More practice on this pattern · ' + st.moreSolved + '/' + st.more.length + ' solved'));
      const ml = el('ol', 'plist');
      st.more.forEach((p) => ml.append(this.row(p, p.oa ? 'OA' : '')));
      more.append(ml);
      body.append(more);
    }
    box.append(body);
    return box;
  },

  row(p, kind) {
    const li = el('li', 'prow' + (p.status ? ' s-' + p.status : ''));
    const b = el('button');
    b.append(el('span', 'dot', ''), el('span', 'pt', p.title));
    const meta = el('span', 'pm');
    if (kind) meta.append(el('span', 'kind ' + kind.toLowerCase(), kind));
    meta.append(el('span', 'diff ' + p.difficulty, p.difficulty));
    if (p.company) meta.append(el('span', 'co', p.company));
    b.append(meta);
    b.title = p.status ? 'Status: ' + p.status : 'Not started';
    b.onclick = () => this.go(p.id);
    li.append(b);
    return li;
  },
};
