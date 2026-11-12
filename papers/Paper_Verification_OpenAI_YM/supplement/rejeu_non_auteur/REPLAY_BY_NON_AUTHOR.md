# Replay of the fast controls by a non-author (night of 11-12 November 2026)

Done by an agent (Claude Sonnet 5.5) that wrote neither the report nor the campaign scripts, on the rented machine (user `lean`, nice 10,
at most 8 Lean threads), from the files of this supplement. The reference compilations (Lean 4.32.0 and 4.32.2) were used read-only;
`LEAN_PATH` was built by hand in the order printed by `lake env printenv LEAN_PATH` and `lean` called directly. Scripts: `scripts/`; logs: `journaux/`.

| Control | Script | Return code | Result | Against the note |
|---|---|---|---|---|
| Source hashes | `a_empreintes.sh` | 0 | HEAD 3456e5e7; 9507/9507 OK (`SOURCES.sha256`); 9508/9508 OK (our list); `PublicTheory.lean` 94111ad2...fff8; `challenge.sha256` l.1 and `SOURCES.sha256` l.10 give it, `verified-sources.sha256` l.1 and `joint-check.log` l.5 give 3940e8dd...a55; 19 of 20 lines of `verified-sources.sha256` agree; the second hash occurs only in those two files | as stated |
| Versions, tools | `a2_versions.sh` | 0 | Lean commits 8c9756b2 (4.32.0), f3b06c70 (4.32.2), eb6cafb7 (4.35.0); nine dependency revisions unmodified; lean4export e5736998...66b0, nanoda_bin ce46eaff...d2c1; 9470 project objects under both versions, none empty; 8639 library objects under 4.32.2 | as stated |
| `Verif.lean`, 4.32.0 and 4.32.2 | `b_verif.sh` | 0, 0 | `jointExistence`, `constructed`, `su2Theory`: [propext, Classical.choice, Quot.sound]; outputs identical | as stated |
| `Temoin.lean`, both | `b_verif.sh` | 0, 0 | [sorryAx] and [temoinAxiome]; identical | as stated |
| `CompactCheck`, both | `c_compact.sh` | 0, 0 | the two `COMPACT_ESTIMATE` lines; identical | as stated |
| `VerifyJoint`, 4.32.0 | `d_joint.sh` | 0 | `TYPE_MATCH`, 17 `ENDPOINT_AXIOMS`, `REPLAY_PASS project=100168 external=14364 endpoints=17 duplicateAliases=0`; identical; 19 min 36 s, 28 414 248 kB | as stated (duration shorter: load) |
| `Usage`, 4.32.0 | `d_joint.sh` | 0 | `USAGE_PASS headlines=17 project=250319 used=100168 outside=150151 modules=9469 modulesWithNoUsedDeclaration=2946` | as stated |
| Export | `e_export.sh` | 0 | SHA-256 f1ff87d70c21f2f2d620d23bb0596a6947cabc3e32ff7ec5725c7a0e7089a06c; 3 224 695 689 bytes; 58 605 083 lines; 145 151 declarations; 0 PANIC; 0 `Vintage`; 0 build path; 4 min 55 s, 15.7 GB | as stated |
| nanoda witnesses | `f_nanoda_temoins.sh` | 0 | true: "Checked 584 declarations with no errors"; sorry, axiom: refused (1, 1); poisoned: panic `assertion failed: self.def_eq(u, v)` (101) | as stated |
| `Chrono_run.lean` | `g_chrono.sh` | 0 | node counts identical; kernel times 4 ms (`uniformE`), 375 ms, 629 ms, 17 672 ms, 1 525 ms (recorded 12, 989, 1 046, 88 601, 7 547 ms) | structure as stated; durations 1.7 to 5 times shorter (load) |
| `Vintage` count | `h_vintage.sh` | 0 | 208 / 174 in five modules; 156 / 146 outside `Orchard.First`; witness of all 174: `YM.SharpGram.habitat`; only `Barrel.lean` (71 lines) imports `Lean` among `YM/` and the 13 root files; 0 `native_decide`, `implemented_by`, `skipKernelTC`, `simproc`, `declare_syntax_cat`; 2 `partial def` (private, in `Barrel.lean`); `maxHeartbeats = 0`, `maxRecDepth = 4096` | as stated |

Not replayed: complete builds (4.32.0 twice, 4.32.2), comparison of the compiled objects, full and diagnostic nanoda runs, lean4lean full pass, arena kernels,
4.35.0 trials and port, the 37 trial transformations of `PublicTheory.lean`, the reading of the nanoda source. Limits: same machine, same reference
objects and tool binaries as the campaign; one agent. Toolchain archive hashes could not be recomputed (archives deleted): only the commits printed by `lean --version` were checked.
