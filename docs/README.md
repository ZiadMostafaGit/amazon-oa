# Write-ups

These are the parts of the old, hand-built practice app that are **not** in the FastPrep bank
and could not be regenerated from it. The 56 problems transcribed from screenshots were replaced
by the bank (3,533 problems with real metadata); the prose around them was kept.

| File | What it is |
|---|---|
| [attempt-postmortem.md](attempt-postmortem.md) | A real 60-minute MovieDB debugging assessment, rebuilt frame by frame from a 42:52 screen recording. 18 stills, each stamped with both clocks — position in the video and time left on the exam. Ends with the corrected `get_recommendations` and a minute-by-minute playbook. **0 of 6 tests were passing when time expired**, and the write-up explains exactly why. |
| [debugging-projects.md](debugging-projects.md) | Five full-stack debugging assessments (MovieDB search and recommendations, Workflow team and issues, Banking RBAC): a Django/React app with one broken feature and a fixed budget. |
| [siemens-hackerearth.md](siemens-hackerearth.md) | The Siemens HackerEarth Java set, with worked solutions. Not in the FastPrep bank. |
| [work-simulation.md](work-simulation.md) | The non-coding half of the Amazon OA: the inbox exercise and the work-style survey. |
| [field-notes.md](field-notes.md) | Notes written while preparing. |

`attempt-stills/` holds the 57 images these reference.

One piece of method from the old app is worth carrying forward, because it cost eleven wrong
solutions to learn: **execute every solution against its own published examples before believing
it, and fuzz it against a brute force where you can afford one.** That discipline is now
automated — `fastprep/practice/tools/verify.py` is the gate, and nothing ships without passing it.
