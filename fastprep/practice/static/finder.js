/* Find this problem: paste a statement from anywhere and get the bank's
 * closest problems, scored and explained.
 *
 * Loaded before app.js; borrows $, el, esc, api, state and openProblem. */
'use strict';

const Finder = {
  open() {
    if (state.studyOpen) Study.close();
    state.finderOpen = true;
    $('#finder').hidden = false;
    $('#workspace').hidden = true;
    $('#findBtn').setAttribute('aria-pressed', 'true');
    document.body.classList.add('finding');
    setTimeout(() => $('#findText').focus(), 0);
  },

  close() {
    state.finderOpen = false;
    $('#finder').hidden = true;
    $('#workspace').hidden = state.studyOpen;
    $('#findBtn').setAttribute('aria-pressed', 'false');
    document.body.classList.remove('finding');
  },

  toggle() { state.finderOpen ? this.close() : this.open(); },

  async find() {
    const text = $('#findText').value;
    const host = $('#findResults');
    const hint = $('#findHint');
    if (text.trim().length < 8) { hint.textContent = 'Paste a little more than that.'; return; }
    host.textContent = '';
    hint.textContent = 'searching…';
    $('#findGo').disabled = true;
    let out;
    try {
      out = await api('api/match', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, limit: 12 }),
      });
    } catch (e) {
      hint.textContent = e.message;
      $('#findGo').disabled = false;
      return;
    }
    $('#findGo').disabled = false;
    const q = out.query || {};
    hint.textContent = q.candidates + ' candidates · ' + q.terms + ' terms' +
      (q.literals ? ' · ' + q.literals + ' example values' : '') +
      (q.magnitudes && q.magnitudes.length ? ' · bounds ' + q.magnitudes.join(', ') : '') +
      (q.topics && q.topics.length ? ' · reads as ' + q.topics.slice(0, 3).join(', ') : '');
    this.paint(out.results || []);
  },

  paint(results) {
    const host = $('#findResults');
    host.textContent = '';
    if (!results.length) {
      host.append(el('div', 'callout warn', 'Nothing in the bank shares wording, values or a signature with that.'));
      return;
    }
    const best = results[0];
    if (best.score < 35) {
      host.append(el('div', 'callout warn',
        'No close match. The best candidates are below, but none of them is clearly this problem — ' +
        'it may not be in the bank, or the paste may need its examples or constraints.'));
    }
    const list = el('div', 'find-list');
    results.forEach((r, i) => {
      const card = el('div', 'find-card ' + labelClass(r.label));
      const top = el('div', 'find-top');
      const score = el('div', 'find-score');
      score.append(el('b', null, String(r.score)));
      const bar = el('span', 'find-bar-track');
      const fill = el('i'); fill.style.width = r.score + '%';
      bar.append(fill);
      score.append(bar);
      top.append(score);
      const mid = el('div', 'find-mid');
      const title = el('button', 'find-title', r.title);
      title.onclick = async () => { Finder.close(); await openProblem(r.id); };
      mid.append(title);
      const tags = el('div', 'find-tags');
      tags.append(el('span', 'tag ' + labelClass(r.label), r.label));
      if (r.difficulty) tags.append(el('span', 'tag ' + r.difficulty, r.difficulty));
      if (r.company) tags.append(el('span', 'tag company', r.company));
      if (r.status) tags.append(el('span', 'tag ' + (r.status === 'solved' ? 'easy' : 'plain'), r.status));
      mid.append(tags);
      if (r.why && r.why.length) {
        const why = el('ul', 'find-why');
        r.why.forEach(w => why.append(el('li', null, w)));
        mid.append(why);
      }
      if (r.also && r.also.length) {
        const also = el('div', 'find-also');
        also.append(el('span', 'hint', 'also at: '));
        r.also.forEach(a => {
          const b = el('button', 'chip', (a.company || a.id) + ' · ' + a.score);
          b.onclick = async () => { Finder.close(); await openProblem(a.id); };
          also.append(b);
        });
        mid.append(also);
      }
      top.append(mid);
      card.append(top);
      list.append(card);
    });
    host.append(list);
  },

  wire() {
    $('#findBtn').onclick = () => this.toggle();
    $('#finderCloseBtn').onclick = () => this.close();
    $('#findGo').onclick = () => this.find();
    $('#findClear').onclick = () => { $('#findText').value = ''; $('#findResults').textContent = ''; $('#findHint').textContent = 'Ctrl-Enter to search'; };
    $('#findText').addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); this.find(); }
    });
  },
};

function labelClass(label) {
  if (label === 'same problem') return 'same';
  if (label === 'probably the same') return 'probable';
  if (label === 'related') return 'related';
  return 'weak';
}
