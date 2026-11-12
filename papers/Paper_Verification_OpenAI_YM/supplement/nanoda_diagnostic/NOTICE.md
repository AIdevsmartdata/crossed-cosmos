# Diagnostic patch for nanoda 0.4.32 (progress printing only)

**What this is.** `patch.diff` is a unified diff against `src/tc.rs` of `nanoda_lib` 0.4.32
(upstream `https://github.com/ammkrn/nanoda_lib`, commit `0da9f98feadd3a0a2ef4b3dbcf52a298a6fef929`, Apache-2.0).
It adds three lines around the existing call `self.check_declar(declar)` in the worker loop: a timer, one line
`DEBUT <index> <name>` printed to standard error before the call, and one line `FIN <index> <seconds>` after it.
Nothing else changes: the checking logic, the declaration order, the permitted axioms and the exit codes are untouched.
`patch_progression.py` applies exactly this edit (it asserts that the original text occurs exactly once);
`preparer.sh` builds the instrumented copy in a separate directory (the official binary is not touched).

**What it is for.** The official (unmodified) replay of the exported closure did not finish in three hours with one worker
still active. The instrumented binary identifies which item never reports `FIN`. It is a *diagnostic*: its run is **not** a
verdict and the results of the unmodified binary are the ones reported as the replay result in the note.

**Who wrote it.** The patch was written during the campaign of 11 November 2026 by the pilot (a language model; the campaign log names it Fable 5.2); neither a human nor a model of another family reviewed it before use (to be confirmed by the authors of the note). The patch is small enough to be read in a minute: please read it.

**Files.**
- `patch.diff`, `patch_progression.py`, `preparer.sh`, `lancer_diag.sh`, `garde_memoire.sh` (memory guard armed on the official replay: it can stop only that one process, by PID; the diagnostic run has its own guard inside `lancer_diag.sh`: 50 GB or 50 minutes), `sources_origine.sha256` (hashes of the upstream sources before the edit).
- `diag.suivi` (progress every 10 s; last line: 187925 starts, 187924 finishes), `diag.rc` (143: stopped by the pilot).
- `diag.err.zst.sha256_taille.txt`: size and SHA-256 of the full compressed diagnostic log (2.3 MB, not included).
- `Chrono.lean`, `Chrono_run.lean`, `chrono.out`, `chrono.time`: timing of Lean's own kernel on the five slowest declarations
  (re-adds a copy of a declaration under another name with `addDecl`, synchronously).
