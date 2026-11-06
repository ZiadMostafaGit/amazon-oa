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
    if (!this.data && !this.map) host.innerHTML = '<div class="hint pad">Loading your path…</div>';
    try {
      const m = await api('api/roadmap');
      this.map = (m.nodes || []).some(n => (n.ladder || []).length) ? m : null;
      if (!this.map) this.data = await api('api/path');
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
    if (this.map) return this.paintTree();
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
      left.append(el('div', 'pn-title', cleanTitle(d.next.title)));
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

  /* ------------------------------------------------------------ the tree */
  paintTree() {
    const m = this.map;
    const host = $('#pathPane');
    host.textContent = '';
    const page = el('div', 'path-page tree-page');
    const byId = Object.fromEntries(m.nodes.map(n => [n.id, n]));

    const head = el('header', 'path-hero');
    head.append(el('div', 'eyebrow', 'Your DSA roadmap'));
    head.append(el('h1', null, 'Learn a pattern, then meet it the way companies ask it.'));
    const next = el('div', 'path-next');
    if (m.next) {
      const left = el('div', 'pn-left');
      left.append(el('div', 'pn-label', 'Next up · ' + m.next.order + '. ' + m.next.nodeTitle + (m.next.teaches ? ' · teaches ' + m.next.teaches : '')));
      left.append(el('div', 'pn-title', cleanTitle(m.next.title)));
      const go = el('button', 'btn primary big', 'Continue  →');
      go.onclick = () => this.go(m.next.id);
      next.append(left, go);
    } else {
      next.append(el('div', 'pn-title', 'Every topic is done. Re-solves and the practice sets are what is left.'));
    }
    head.append(next);
    const meter = el('div', 'path-meter');
    meter.append(el('span', null, m.solved + ' of ' + m.total + ' roadmap problems solved'));
    const bar = el('div', 'bar'); const fill = el('i'); fill.style.width = (m.total ? Math.round(100 * m.solved / m.total) : 0) + '%'; bar.append(fill);
    meter.append(bar);
    head.append(meter);
    if (Study.reviews && (Study.reviews.due || []).length) {
      const rv = el('button', 'linkbtn due', Study.reviews.due.length + ' re-solves due today →');
      rv.onclick = () => { this.close(); Study.openIndex(); };
      head.append(rv);
    }
    page.append(head);

    const how = el('details', 'path-how');
    how.append(el('summary', null, 'How to work a topic'));
    const ol = el('ol');
    [
      ['Read the chapter', 'Only the parts that build the idea; it ends with exercises you do by hand. Then write its code from memory once.'],
      ['Learn each technique', 'Every technique is taught by one problem, picked because it shows that idea most clearly. Solve them in order; the first ones are the clearest.'],
      ['Then practise', 'The practice problems wrap the same techniques in OA stories. Give each 25 minutes before a hint.'],
      ['Re-solve', 'Solved problems come back at 3, 10, 30 and 90 days. A topic unlocks the ones below it once most of its core problems are solved.'],
    ].forEach(([b, t]) => { const li = el('li'); li.append(el('b', null, b + '. '), document.createTextNode(t)); ol.append(li); });
    how.append(ol);
    page.append(how);

    /* rows by depth: a topic sits one row below its deepest prerequisite */
    const level = {};
    const depth = (n) => level[n.id] != null ? level[n.id]
      : (level[n.id] = n.parents.length ? 1 + Math.max(...n.parents.map(p => depth(byId[p]))) : 0);
    m.nodes.forEach(depth);
    const rows = [];
    m.nodes.forEach(n => { (rows[level[n.id]] = rows[level[n.id]] || []).push(n); });
    /* order each row by where its parents sit (fewer crossing arrows), then by number */
    const xpos = {};
    rows.forEach((r, ri) => {
      if (ri === 0) r.sort((a, b) => a.order - b.order);
      else {
        const key = n => n.parents.reduce((s, p) => s + (xpos[p] ?? 0.5), 0) / n.parents.length;
        r.sort((a, b) => (key(a) - key(b)) || (a.order - b.order));
      }
      r.forEach((n, i) => { xpos[n.id] = (i + 0.5) / r.length; });
    });

    const current = m.next ? m.next.node : null;
    if (!this.selected) this.selected = current || m.nodes[0].id;
    const wrap = el('div', 'tree-wrap');
    const tree = el('div', 'tree');
    const svgNS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(svgNS, 'svg');
    svg.setAttribute('class', 'tree-edges');
    svg.setAttribute('aria-hidden', 'true');
    tree.append(svg);
    rows.forEach(r => {
      const row = el('div', 'tree-row');
      r.forEach(n => {
        const b = el('button', 'tnode phase-' + n.phase + (n.done ? ' done' : '') + (n.id === current ? ' current' : '') +
                     (!n.unlocked && !n.done ? ' locked' : '') + (n.id === this.selected ? ' sel' : ''));
        b.dataset.node = n.id;
        b.append(el('span', 'tn-num', String(n.order)), el('span', 'tn-title', n.title));
        const pb = el('span', 'tn-bar'); const pf = el('i');
        pf.style.width = (n.ladder.length ? Math.round(100 * n.solved / n.ladder.length) : 0) + '%';
        pb.append(pf); b.append(pb);
        b.title = n.title + ' — ' + n.solved + '/' + n.ladder.length + ' solved' + (n.unlocked ? '' : ' (needs: ' + n.parents.map(p => byId[p].title).join(', ') + ')');
        b.onclick = () => { this.selected = n.id; this.paintTree(); const pn = $('#nodePanel'); if (pn) pn.scrollIntoView({ block: 'start', behavior: 'smooth' }); };
        row.append(b);
      });
      tree.append(row);
    });
    wrap.append(tree);
    const legend = el('div', 'tree-legend');
    [['A', 'OA core'], ['B', 'Interview core'], ['C', 'Depth']].forEach(([k, t]) => {
      const s = el('span', 'lg phase-' + k); s.append(el('i'), document.createTextNode(t)); legend.append(s);
    });
    page.append(wrap, legend);

    page.append(this.nodePanel(byId[this.selected], byId));
    host.append(page);

    /* the arrows, drawn once the boxes have their final positions */
    const draw = () => {
      const tb = tree.getBoundingClientRect();
      svg.setAttribute('width', tb.width); svg.setAttribute('height', tb.height);
      svg.setAttribute('viewBox', '0 0 ' + tb.width + ' ' + tb.height);
      svg.textContent = '';
      const pos = {};
      tree.querySelectorAll('.tnode').forEach(b => { const r = b.getBoundingClientRect(); pos[b.dataset.node] = { x: r.left - tb.left + r.width / 2, top: r.top - tb.top, bottom: r.bottom - tb.top }; });
      m.nodes.forEach(n => n.parents.forEach(p => {
        const a = pos[p], c = pos[n.id]; if (!a || !c) return;
        const path = document.createElementNS(svgNS, 'path');
        const my = (a.bottom + c.top) / 2;
        path.setAttribute('d', 'M' + a.x + ',' + a.bottom + ' C' + a.x + ',' + my + ' ' + c.x + ',' + my + ' ' + c.x + ',' + c.top);
        path.setAttribute('class', 'edge' + (n.id === this.selected || p === this.selected ? ' hot' : ''));
        svg.append(path);
      }));
    };
    requestAnimationFrame(draw);
    if (this._onResize) window.removeEventListener('resize', this._onResize);
    this._onResize = () => requestAnimationFrame(draw);
    window.addEventListener('resize', this._onResize);
  },

  nodePanel(n, byId) {
    const box = el('section', 'node-panel');
    box.id = 'nodePanel';
    const h = el('div', 'np-head');
    h.append(el('span', 'tn-num big', String(n.order)));
    const t = el('div');
    t.append(el('h2', null, n.title));
    const sub = el('div', 'np-sub');
    sub.append(el('span', 'wk', 'KHATT W' + n.weeks.map(w => String(w).padStart(2, '0')).join('–W')));
    if (n.parents.length) sub.append(el('span', null, 'needs ' + n.parents.map(p => byId[p].title).join(', ')));
    sub.append(el('span', null, n.solved + '/' + n.ladder.length + ' solved'));
    t.append(sub);
    h.append(t);
    box.append(h);

    /* 1. learn */
    const learn = el('div', 'np-step');
    learn.append(el('div', 'np-label', '1 · Read'));
    const chips = el('div', 'np-chips');
    n.chapters.forEach((c, i) => {
      const b = el('button', 'chip' + (i === 0 ? ' main' : '') + (c.hasArticle ? '' : ' empty'), c.title);
      b.title = c.hasArticle ? 'Open the chapter' : 'No chapter written yet: the problems still teach it';
      b.onclick = () => { this.close(); Study.open(c.slug); };
      chips.append(b);
    });
    learn.append(chips);
    box.append(learn);

    /* 2. techniques, each with the problems that teach it */
    const core = n.ladder.filter(x => x.level === 'core');
    const tech = el('div', 'np-step');
    tech.append(el('div', 'np-label', '2 · Learn the techniques, in order'));
    if (!n.ladder.length) tech.append(el('p', 'hint', 'This topic is not curated yet.'));
    const byTech = {};
    core.forEach(x => (byTech[x.teaches] = byTech[x.teaches] || []).push(x));
    const listed = new Set();
    const tl = el('ol', 'tech-list');
    n.techniques.forEach(tq => {
      const li = el('li', 'tech');
      const probs = byTech[tq] || [];
      li.append(el('div', 'tq', tq));
      if (probs.length) {
        const ul = el('ul', 'plist');
        probs.forEach(p => { ul.append(this.ladderRow(p)); listed.add(p.id); });
        li.append(ul);
      } else {
        li.append(el('div', 'tq-none', 'taught inside the practice problems below'));
      }
      tl.append(li);
    });
    // core problems whose technique is phrased differently
    core.filter(x => !listed.has(x.id)).forEach(p => {
      const li = el('li', 'tech'); li.append(el('div', 'tq', p.teaches || 'also core'));
      const ul = el('ul', 'plist'); ul.append(this.ladderRow(p)); li.append(ul); tl.append(li);
    });
    tech.append(tl);
    box.append(tech);

    /* 3. practice and stretch */
    const rest = n.ladder.filter(x => x.level !== 'core');
    if (rest.length) {
      const pr = el('div', 'np-step');
      pr.append(el('div', 'np-label', '3 · Practise: the same ideas, the way OAs ask them'));
      const ul = el('ul', 'plist');
      rest.forEach(p => ul.append(this.ladderRow(p, true)));
      pr.append(ul);
      box.append(pr);
    }
    return box;
  },

  ladderRow(p, showTech) {
    const li = el('li', 'prow lrow' + (p.status ? ' s-' + p.status : ''));
    const b = el('button');
    b.append(el('span', 'dot', ''));
    const mid = el('span', 'lmid');
    mid.append(el('span', 'pt', cleanTitle(p.title)));
    if (p.why) mid.append(el('span', 'why', (showTech && p.teaches ? p.teaches + ' — ' : '') + p.why));
    b.append(mid);
    const meta = el('span', 'pm');
    if (p.level === 'stretch') meta.append(el('span', 'kind stretch', 'stretch'));
    meta.append(el('span', 'diff ' + p.difficulty, p.difficulty));
    if (p.company) meta.append(el('span', 'co', p.company));
    b.append(meta);
    b.onclick = () => this.go(p.id);
    li.append(b);
    return li;
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
    b.append(el('span', 'dot', ''), el('span', 'pt', cleanTitle(p.title)));
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
