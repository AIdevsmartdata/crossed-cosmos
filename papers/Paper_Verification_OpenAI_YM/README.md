# Independent recompilation and axiom audit of the public Lean development on four-dimensional Yang–Mills existence (v1.1)

A reproducibility report on the public Lean development `yang-mills-group/OpenAI-YM-20261028` (commit
`3456e5e75cf8d4cd558955a5c7638fba2d68f464`): what was recompiled and checked on 11 November 2026 (and the state of the lean4lean reruns read on 12 November), with which results, and what was not
checked. It does **not** assess the mathematics or the faithfulness of the formal statement, and makes no priority claim. The checked
proposition is an existence statement; nothing here concerns a mass gap. Prepared with AI assistance (see the statement at the end of the
note). Not refereed; no human has checked the proofs. Licence of this folder: CC-BY-4.0 (our text, scripts and logs).

## Layout
- `note/` — `verification_openai_ym_v1_1.tex` and its PDF.
- `supplement/envoi/` — our scripts as run on the rented machine (`prepare.sh`, `setup_root.sh`, `pilote_vast.sh`, `pilote2.sh`,
  `outils/interne_*.sh`) and our Lean control files `nos/Verif.lean`, `nos/Temoin.lean`, `nos/TemoinNanoda.lean`; `nos/SHA256SUMS_SOURCES`
  = the 9508 expected SHA-256 values of the repository files. Paths `/work/...` are those of the (destroyed) rented container. One block
  of the two controllers, which compiled two files unrelated to this report, was replaced by a comment (see the comment in the scripts).
  `Verif.lean` quotes three lines of `ChallengeSpec.lean` (Apache-2.0, OpenAI) to check them against the submitted term.
- `supplement/nanoda_diagnostic/` — `patch.diff` (progress printing only, against nanoda 0.4.32; see `NOTICE.md`), the scripts that built
  and ran the instrumented copy, `Chrono.lean`/`Chrono_run.lean` and their outputs.
- `supplement/journaux/` — logs and return codes (`*.rc`), outputs of the axiom checks, `CompactCheck`, `VerifyJoint`, `Usage`, build
  summaries, export statistics, nanoda witness logs. Logs above 300 kB are not copied: see `GROS_JOURNAUX_EMPREINTES.tsv`.
- `supplement/empreintes/` — hashes: export of the proof closure, tool binaries, dependency revisions, toolchain archives, head commit,
  manifests of the compiled project objects (gzip).
- `supplement/lean4lean/` — report, calibration logs, and the full pass (`complet/`: `FIN2`, `rc_par_module.tsv`, the seven postponed
  modules in `reportes/`, `lourds*.txt`) and `relances/` (reruns of the seven postponed modules, state read on 12 November 2026 at 05:20 CET; the reruns were still in progress).
- `supplement/arene/` — scripts and logs of the two Lean Kernel Arena kernels run on the export (`NOTES.md` summarises them).
- `supplement/portage_4350/` — `SUIVI.tsv`, `ITERATION15.txt` and `NOTES.md` (state of the partial port to Lean 4.35.0, stopped on the evening of 11 November).
- `supplement/rejeu_non_auteur/` — the replay of the fast controls by a party that did not run the campaign (`REPLAY_BY_NON_AUTHOR.md`,
  scripts, logs).
- `SHA256SUMS` — `sha256sum -c SHA256SUMS`.

Not included, on purpose: code of the repository under study, of nanoda, of lean4export, of lean4lean, of the arena kernels (each is
obtained from its own repository at the commit named in the note), the 3.2 GB export (its SHA-256 and size are given), and the logs of
the heavy runs (hash and size given).

## How to replay each control
Linux x86-64, an unprivileged user, the official Lean toolchains (archive hashes in `supplement/empreintes/toolchains.log`), the repository
at the commit above, and the project compiled once with `lake build WilsonReference WilsonConstruction` under Lean 4.32.0 (and once under
4.32.2). Memory: about 30 GB for `VerifyJoint`, 10 GB for the others. Ready-made versions with the paths of the rented machine are in
`supplement/rejeu_non_auteur/scripts/`.
1. **Source hashes**: in the repository, `sha256sum -c SOURCES.sha256` (9507 lines; plus the file itself = 9508 files) and
   `sha256sum -c supplement/envoi/nos/SHA256SUMS_SOURCES`. The two digests of `PublicTheory.lean`: compare line 1 of `verification/challenge.sha256`
   with line 1 of `verification/verified-sources.sha256`.
2. **Axioms and deliberately false witnesses**: `lean -DmaxHeartbeats=0 -DmaxRecDepth=4096 supplement/envoi/nos/Verif.lean`, then `lean supplement/envoi/nos/Temoin.lean`
   (inside the compiled project, e.g. `lake env lean ...`).
3. **CompactCheck**: `lake env lean -j1 verification/CompactCheck.lean`.
4. **VerifyJoint, Usage**: `lake env lean -j1 -DmaxHeartbeats=0 -DmaxRecDepth=4096 VerifyJoint.lean` (about 20 to 35 min); `lake env lean -j1 -DmaxHeartbeats=0 verification/Usage.lean`.
5. **Export**: `supplement/envoi/outils/interne_export.sh joint YangMills.jointExistence YangMills.constructed YangMills.su2Theory`
   (lean4export `v4.32.0`, commit `4e7915201d3f9f04470d9eae002fa695f7cdc589`). Expected SHA-256
   `f1ff87d70c21f2f2d620d23bb0596a6947cabc3e32ff7ec5725c7a0e7089a06c`, 3 224 695 689 bytes, 58 605 083 lines, 145 151 declarations.
6. **nanoda** (commit `0da9f98feadd3a0a2ef4b3dbcf52a298a6fef929`): `interne_temoins_nanoda.sh` (one true witness accepted, three false refused);
   `interne_nanoda.sh joint 24 ...` for the full replay (about 4 hours, up to 145 GB; ends with a capacity panic, see the note).
7. **Kernel timings**: `lake env lean -DmaxHeartbeats=0 -DmaxRecDepth=4096 supplement/nanoda_diagnostic/Chrono_run.lean`.
8. **Metaprogram count**: count the rows of `verification/declaration-usage.tsv` whose second column begins with `Vintage.` (208, 174 `used`;
   156 and 146 outside the module `YM.UVExtension.Orchard.First`); `supplement/rejeu_non_auteur/scripts/h_vintage.sh`.
9. **lean4lean** (revision `408edad8930c1d9d974f93fcbe4a304a174b2b6f`): `lean4lean <Module>` per module, `supplement/lean4lean/complet/worker.sh`; report in `supplement/lean4lean/RAPPORT.md`.
10. **Arena kernels**: scripts `supplement/arene/b_*.sh` (build), `cal_*.sh` (witnesses), `run_*.sh` (export), `tr.sh`, `ue.sh`; commits in the note.
