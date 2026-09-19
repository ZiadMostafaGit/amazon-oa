/* The challenge timer: pick a length, race it, and be told when it is over.
 *
 * Loaded before app.js; it borrows $, el, state and remember from there, which
 * is safe because nothing here runs before boot() calls Timer.wire().
 *
 * The clock is a deadline, not a counter. Every tick reads Date.now() and
 * subtracts, so a throttled background tab, a laptop that slept, or a reload
 * mid-attempt cannot make it lie - what is stored is the deadline itself (or,
 * while paused, what was left), which is why reloading picks the run back up
 * instead of quietly handing you extra time. */
'use strict';

const Timer = {
  KEY: 'fp:timer',
  DEFAULT: 45 * 60000,          // a per-problem length, not a whole-OA one
  MIN: 5000,
  MAX: 6 * 3600000,
  PRESETS: [15, 20, 30, 45, 60, 90],

  deadline: 0,      // ms epoch while running; 0 otherwise
  left: 0,          // ms still to run - set while paused, and while staged
  duration: 0,      // the length this run was started with, for the bar and reruns
  fired: false,     // time is up and has not been acknowledged
  sound: true, notify: false, auto: false,
  ac: null, alarm: null, prevTitle: '', beats: 0,

  /* ----------------------------------------------------------------- wiring */
  wire() {
    this.sound = localStorage.getItem('fp:timersound') !== '0';
    this.notify = localStorage.getItem('fp:timernotify') === '1';
    this.auto = localStorage.getItem('fp:timerauto') === '1';
    $('#timerSound').checked = this.sound;
    $('#timerNotify').checked = this.notify;
    $('#timerAuto').checked = this.auto;

    const presets = $('#timerPresets');
    this.PRESETS.forEach(m => {
      const b = el('button', 'chip', m + ' min');
      b.onclick = () => { this.start(m * 60000); this.closePanel(); };
      presets.append(b);
    });

    $('#timerBtn').onclick = () => this.toggle();
    $('#timerToggle').onclick = () => {
      if (this.deadline) this.pause();
      else this.start(this.left || this.duration);
    };
    $('#timerPlus').onclick = () => this.extend(5 * 60000);
    $('#timerReset').onclick = () => this.reset();
    $('#timerSet').onclick = () => this.startCustom();
    $('#timerCustom').onkeydown = (e) => {
      if (e.key === 'Enter') { e.preventDefault(); this.startCustom(); }
    };
    $('#timerSound').onchange = (e) => {
      this.sound = e.target.checked;
      remember('timersound', this.sound ? '1' : '0');
      if (this.sound) this.ring();                 // so you hear what you just chose
    };
    $('#timerNotify').onchange = (e) => {
      this.notify = e.target.checked;
      remember('timernotify', this.notify ? '1' : '0');
      if (this.notify) this.askNotify();
    };
    $('#timerAuto').onchange = (e) => {
      this.auto = e.target.checked;
      remember('timerauto', this.auto ? '1' : '0');
    };

    $('#timeupOk').onclick = () => this.dismiss();
    $('#timeupMore').onclick = () => this.extend(5 * 60000);
    $('#timeupAgain').onclick = () => this.start(this.duration);

    /* a click anywhere else closes the panel, the way the drawer's scrim does */
    document.addEventListener('mousedown', (e) => {
      if (!$('#timerPanel').hidden && !e.target.closest('#timerWrap')) this.closePanel();
    });

    this.restore();
    setInterval(() => this.onTick(), 250);
    this.onTick();
  },

  /* -------------------------------------------------------------- the clock */
  remaining() {
    if (this.deadline) return Math.max(0, this.deadline - Date.now());
    return this.fired ? 0 : this.left;
  },

  running() { return this.deadline > 0; },
  staged() { return !this.deadline && !this.fired && this.left > 0; },

  start(ms) {
    const len = this.clamp(ms || this.duration || this.DEFAULT, this.MIN, this.MAX);
    this.ensureAudio();                 // a click is the only chance to unlock audio
    this.duration = len;
    this.deadline = Date.now() + len;
    this.left = 0;
    this.clearUp();
    this.save(); this.paint();
  },

  startCustom() {
    const ms = this.parse($('#timerCustom').value);
    const err = $('#timerErr');
    if (!ms) {
      err.textContent = 'Give minutes (45), a clock (12:30, or 1:30:00 for hours), ' +
                        'or a unit (90s, 2h).';
      err.hidden = false;
      return;
    }
    err.hidden = true;
    this.start(ms);
    this.closePanel();
  },

  pause() {
    if (!this.deadline) return;
    this.left = this.remaining();
    this.deadline = 0;
    this.save(); this.paint();
  },

  /* +5 means five more minutes wherever you are: running, paused, staged, or
     staring at the alarm. The length grows with it, so the bar stays honest. */
  extend(ms) {
    if (this.fired) {
      this.clearUp();
      this.duration = this.clamp(this.duration + ms, this.MIN, this.MAX);
      this.deadline = Date.now() + ms;
    } else if (this.deadline) {
      this.deadline += ms;
      this.duration = this.clamp(this.duration + ms, this.MIN, this.MAX);
    } else if (this.left) {
      this.left = this.clamp(this.left + ms, this.MIN, this.MAX);
      this.duration = this.clamp(this.duration + ms, this.MIN, this.MAX);
    } else {
      /* nothing to add to, so it stages a run of exactly this much */
      this.left = this.duration = this.clamp(ms, this.MIN, this.MAX);
    }
    this.save(); this.paint();
  },

  reset() {
    this.deadline = 0; this.left = 0;
    this.clearUp();
    this.save(); this.paint();
  },

  onTick() {
    if (this.deadline && Date.now() >= this.deadline) this.fire();
    this.paint();
  },

  /* ------------------------------------------------------------- time is up */
  fire() {
    this.deadline = 0; this.left = 0; this.fired = true;
    this.save();
    this.show(false);
  },

  show(silent) {
    const d = state.current;
    $('#timeupClock').textContent = this.fmt(this.duration);
    $('#timeupNote').textContent =
      (this.duration ? 'The ' + this.fmt(this.duration) + ' you gave yourself is gone'
                     : 'Time is up') +
      (d ? ' on ' + (d.title || d.id) : '') +
      '. Whatever is in the editor now is what you would have submitted.';
    $('#timeup').hidden = false;
    if (!silent) this.startAlarm();
    this.paint();
  },

  clearUp() {
    this.fired = false;
    $('#timeup').hidden = true;
    this.stopAlarm();
  },

  /* Three rising beeps, repeated - loud enough to notice, and it gives up on
     the noise after half a minute so a forgotten tab does not scream all day.
     The title keeps flashing until you acknowledge it, which is the part that
     still reaches you when the tab is in the background. */
  startAlarm() {
    this.prevTitle = this.prevTitle || document.title;
    this.beats = 0;
    clearInterval(this.alarm);
    const beat = () => {
      if (!this.fired) { this.stopAlarm(); return; }
      if (this.beats < 20) this.ring();
      document.title = (this.beats % 2) ? this.prevTitle : '⏰ Time is up';
      this.beats++;
    };
    beat();
    this.alarm = setInterval(beat, 1500);
    this.notifyNow();
  },

  stopAlarm() {
    clearInterval(this.alarm);
    this.alarm = null;
    if (this.prevTitle) { document.title = this.prevTitle; this.prevTitle = ''; }
  },

  dismiss() { this.reset(); },

  /* ------------------------------------------------------------------ noise */
  /* No audio file: a few oscillators are smaller than any beep you could ship,
     and this app has no assets it did not have to have. */
  ensureAudio() {
    if (!this.sound) return;
    try {
      const C = window.AudioContext || window.webkitAudioContext;
      if (!this.ac && C) this.ac = new C();
      if (this.ac && this.ac.state === 'suspended') this.ac.resume();
    } catch (e) { this.ac = null; }
  },

  ring() {
    if (!this.sound) return;
    this.ensureAudio();
    if (!this.ac) return;
    const t0 = this.ac.currentTime + 0.01;
    [880, 1100, 1320].forEach((hz, i) => this.beep(t0 + i * 0.2, hz, 0.16));
  },

  beep(at, hz, dur) {
    try {
      const ac = this.ac;
      const osc = ac.createOscillator(), gain = ac.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(hz, at);
      gain.gain.setValueAtTime(0.0001, at);
      gain.gain.linearRampToValueAtTime(0.22, at + 0.015);
      gain.gain.exponentialRampToValueAtTime(0.0001, at + dur);
      osc.connect(gain).connect(ac.destination);
      osc.start(at);
      osc.stop(at + dur + 0.05);
    } catch (e) {}
  },

  askNotify() {
    try {
      if ('Notification' in window && Notification.permission === 'default')
        Notification.requestPermission();
    } catch (e) {}
  },

  notifyNow() {
    if (!this.notify) return;
    try {
      if ('Notification' in window && Notification.permission === 'granted') {
        const d = state.current;
        new Notification('Time is up', {
          body: this.fmt(this.duration) + ' — ' + (d ? (d.title || d.id) : 'FastPrep practice'),
          tag: 'fp-timer',
        });
      }
    } catch (e) {}
  },

  /* ------------------------------------------------------------------ paint */
  /* One word describes the whole clock, and the button, the bar and the panel's
     readout all wear it: run, warn (under five minutes), crit (under one), hold
     (paused), up (over). */
  tone() {
    const rem = this.remaining();
    if (this.fired) return 'up';
    if (this.running()) return rem <= 60000 ? 'crit' : rem <= 300000 ? 'warn' : 'run';
    return this.staged() ? 'hold' : '';
  },

  paint() {
    const rem = this.remaining();
    const tone = this.tone();
    const live = tone !== '';

    const btn = $('#timerBtn');
    $('#timerFace').textContent = this.fired ? 'Time up' : live ? this.fmt(rem) : 'Timer';
    btn.className = 'iconbtn timerbtn' + (tone ? ' ' + tone : '');
    btn.title = this.fired ? 'Time is up — click for the timer  (press t)'
      : tone === 'hold' ? this.fmt(rem) + ' left, paused  (press t)'
      : this.running() ? this.fmt(rem) + ' left of ' + this.fmt(this.duration) + '  (press t)'
      : 'Challenge timer — pick a length and race it  (press t)';

    const bar = $('#timerBar');
    bar.hidden = !(live && this.duration > 0);
    if (!bar.hidden) {
      bar.className = tone;
      bar.firstElementChild.style.width =
        (100 * Math.min(1, rem / this.duration)).toFixed(2) + '%';
    }

    const big = $('#timerBig');
    big.textContent = live ? this.fmt(rem) : '--:--';
    big.className = 'tp-big' + (tone ? ' ' + tone : '');
    $('#timerOf').textContent = this.fired ? 'time is up'
      : this.running() ? 'of ' + this.fmt(this.duration) + ' · running'
      : this.staged() ? 'of ' + this.fmt(this.duration) + ' · paused'
      : this.duration ? 'nothing running · last length ' + this.fmt(this.duration)
      : 'nothing running';
    $('#timerToggle').textContent = this.running() ? 'Pause' : this.staged() ? 'Resume' : 'Start';
    $('#timerReset').disabled = !live;
  },

  /* ------------------------------------------------------------------ panel */
  toggle() { $('#timerPanel').hidden ? this.openPanel() : this.closePanel(); },

  openPanel() {
    $('#timerPanel').hidden = false;
    $('#timerBtn').setAttribute('aria-expanded', 'true');
    $('#timerErr').hidden = true;
    if (!$('#timerCustom').value && this.duration)
      $('#timerCustom').value = String(Math.round(this.duration / 60000));
    this.paint();
    $('#timerCustom').focus();
    $('#timerCustom').select();
  },

  closePanel() {
    $('#timerPanel').hidden = true;
    $('#timerBtn').setAttribute('aria-expanded', 'false');
  },

  /* Esc walks the timer first: the alarm, then the panel. */
  onEscape() {
    if (!$('#timeup').hidden) { this.dismiss(); return true; }
    if (!$('#timerPanel').hidden) { this.closePanel(); return true; }
    return false;
  },

  /* --------------------------------------------------------------- the hook */
  /* Opening a problem is the start of an attempt, so it is the one place a
     fresh clock may begin on its own - only when asked to, and never on top of
     a run already in flight. */
  onProblemOpened() {
    if (!this.auto || this.deadline || this.fired) return;
    this.start(this.duration || this.DEFAULT);
  },

  /* ---------------------------------------------------------------- storage */
  save() {
    try {
      localStorage.setItem(this.KEY, JSON.stringify({
        deadline: this.deadline, left: this.left,
        duration: this.duration, fired: this.fired,
      }));
    } catch (e) {}
  },

  restore() {
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(this.KEY) || 'null'); } catch (e) {}
    if (!saved || typeof saved !== 'object') return;
    this.duration = this.clamp(saved.duration, 0, this.MAX);
    if (saved.deadline > Date.now()) {
      this.deadline = saved.deadline;              // still running - carry on
    } else if (saved.deadline || saved.fired) {
      /* it ran out while the page was closed. Say so, but silently: a beep for
         something that happened an hour ago is only startling. */
      this.fired = true;
      this.show(true);
    } else {
      this.left = this.clamp(saved.left, 0, this.MAX);
    }
  },

  /* --------------------------------------------------------------- numbers */
  clamp(n, lo, hi) { return Math.max(lo, Math.min(hi, Math.round(n || 0))); },

  /* Remaining time rounds up, so a 45-minute run reads 45:00 the moment it
     starts and 00:00 only when it really is over. */
  fmt(ms) {
    const t = Math.ceil(Math.max(0, ms || 0) / 1000);
    const pad = (n) => String(n).padStart(2, '0');
    const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), s = t % 60;
    return h ? h + ':' + pad(m) + ':' + pad(s) : pad(m) + ':' + pad(s);
  },

  /* "45" is minutes - that is what anyone typing a length means. A clock reads
     as a clock (12:30 is twelve and a half minutes, 1:30:00 an hour and a
     half), and an explicit unit wins over both. */
  parse(text) {
    const s = String(text == null ? '' : text).trim().toLowerCase();
    if (!s) return 0;
    const clock = s.match(/^(\d+):([0-5]?\d)(?::([0-5]?\d))?$/);
    if (clock) {
      const a = +clock[1], b = +clock[2];
      return clock[3] == null ? (a * 60 + b) * 1000
                              : (a * 3600 + b * 60 + +clock[3]) * 1000;
    }
    const m = s.match(
      /^(\d+(?:\.\d+)?)\s*(h|hr|hrs|hour|hours|m|min|mins|minute|minutes|s|sec|secs|second|seconds)?$/);
    if (!m) return 0;
    const unit = (m[2] || 'm')[0];
    const scale = unit === 'h' ? 3600000 : unit === 's' ? 1000 : 60000;
    const ms = Math.round(parseFloat(m[1]) * scale);
    return ms >= 1000 ? ms : 0;
  },
};
