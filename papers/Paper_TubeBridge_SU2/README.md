# An elementary twist-ratio bound for the SU(2) Wilson lattice, formalised in Lean 4 on the objects of OpenAI's four-dimensional development

Version 1.0 (12 November 2026; DRAFT, not published, not deposited). Author: Kévin Rémondière (ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)).

A technical note and 23 Lean 4 declarations on a classical tool (multiplying by −1 all links of a "column" and averaging over independent column signs). It is not a mass-gap result and no priority is claimed (the tool is classical: Tomboulis–Yaffe 1985; the paper of Borgs 1985 could not be read).

## What the note says, and does not say
- Abstract bound `|⟨W⟩| ≤ tanh(κ)^|A|` and its sharpness (Lean). Elementary area law `tanh(β|F|)^area` on (rectangular plate) × (finite fibre F) for Wilson-type actions with a central involution (Lean).
- Torus: plaquette signs multiply to 1 and every even assignment is realised (Lean); twist-ratio bound `|Z₀ − Z₁| ≤ tanh(κ)^N (Z₀ + Z₁)` (Lean).
- **Head theorem, on OpenAI's objects** (Lean, compiled inside their project): for every `l ≥ 2` and `β ≥ 0`, `|Z₀ − Z₁| ≤ tanh(β l²)^(l²) (Z₀ + Z₁)` for their periodic lattice, their Wilson energy and their SU(2), where `Z₁` has the sign of the trace term of the plaquettes of the plane of axes 0,1 at one base point (all positions along axes 2,3) reversed (`TubeBridge.openai_su2_twist_ratio`).
- On paper only (checked by AI models only, not formalised): `λ₁/λ₀ ≤ tanh(β L²)^l` for the odd and even centre-parity sectors of a tube transfer matrix (Section 5).
- **Not claimed**: any mass gap; anything uniform in the transverse section (the bound tends to 1 as `l` or `|F|` grows at fixed β); anything in the weak-coupling regime, in infinite volume or in the continuum; any gap in the neutral sector; the sharpness of the constant for SU(2). The argument uses only a central involution and `|χ| ≤ 1`, so it holds verbatim for U(1) and Z₂ gauge theories.
- Written by AI models and read by other AI models (roles in the note); not refereed; no human has checked the proofs.

## Contents
- `note/` : `tube_bridge_su2_v1_0.tex` and `.pdf` (16 pages), `shatable.tex` (included by the note), LaTeX logs.
- `lean/TubePont_pont_6.lean` : the cumulative file with all 23 declarations (3 091 lines, sha256 `e0a70f80…8bb6`); it imports `Mathlib`, `PublicWilson`, `ConcreteSU2` and is compiled inside OpenAI's project. `lean/etapes/` : the eight stage files (one per proof loop). `lean/pieds/` : the statements frozen before each loop and the verification footers (never written by the proving model). `lean/journaux/` : compilation logs (Lean 4.32.0 and 4.32.2), the independent-kernel logs (nanoda 0.4.32), certificate of 11 November 2026 (`CERTIFICAT_fr.md`, in French). `lean/MANIFEST.txt` : sha256 of the nine Lean files.
- `CONCORDANCE_TEXTE_LEAN.md` (in French): statement of the text opposite the Lean statement, for each of the 23 items, with line numbers and verdicts. `RELECTURES.md` (in French): drafting by DeepSeek, one read-only review by GPT-6.1 Sol, corrections applied.
- `SHA256SUMS` : `sha256sum -c SHA256SUMS`.

## Licence and OpenAI's code
The note is under CC-BY-4.0. The Lean files are under Apache-2.0 (`lean/LICENSE-Apache-2.0.txt`, `lean/NOTICE`). **No file of OpenAI's repository is copied.** The Lean file imports two of its modules and refers to its declarations by name; one definition (`signedWilsonEnergy`) adapts the two-line body of their `wilsonEnergy` (Apache-2.0, repository `yang-mills-group/OpenAI-YM-20261028`, commit `3456e5e7`, Lean 4.32.0). Fetch that repository separately.

## How to check
1. In a clone of the OpenAI repository at commit `3456e5e7` with Lean 4.32.0 (and its pinned Mathlib, `81a5d257`): `lake env lean /path/to/lean/TubePont_pont_6.lean`. Expected: no error, the `#print axioms` lines show `[propext, Classical.choice, Quot.sound]`; compare with `lean/journaux/certificat/etape8/olean_pont.out` (return code 0, 24 axiom lines). Lean 4.32.2 gives the same.
2. Independent kernel: export the closure with `lean4export` and check with nanoda 0.4.32 (see `lean/journaux/certificat/verif_complementaire*.sh`); logged result: "Checked 40099 declarations with no errors".
3. The note: `pdflatex` three passes in `note/`.

## Reproducibility status (honest)
The Lean files were compiled on 11 November 2026 on a rented machine by the project's scripts driven by an AI model. **Replay by a non-author, 12 November 2026 (03:54-04:08 UTC)**: Claude Sonnet 5.5 (not the author of the statements, proofs or note) rebuilt `lean/TubePont_pont_6.lean` from the `git archive` of this folder (tree of the folder `b1d1e6ed…`, of `lean/` `7634d3da…`; archive sha256 `b8229a82…ac9bec`) on the same rented machine, in the same already compiled environment (Lean 4.32.0, Mathlib and OpenAI's project as compiled on 11 November): return code 0, no error, 18 linter warnings, 24 axiom lines all `[propext, Classical.choice, Quot.sound]`, no forbidden token; nanoda (unmodified binary) re-checked the exported closure: "Checked 40099 declarations with no errors" (five `TubeBridge` declarations) and "Checked 40630" (the 23 declarations). **Not redone**: Lean 4.32.2 (not installed there); the closure of OpenAI's `YangMills.su2Theory`; a rebuild of Mathlib and of OpenAI's project from source, and a check of their commit (no git metadata there; `lake` reported local changes in the mathlib folder); the nanoda export digest differs from 11 November's with equal line and declaration counts (not investigated). The replayer is an AI model of the pilot's family, not an independent human or laboratory. Scripts, logs, identifiers: `rejeu_depuis_arbre_git_2026-11-12/`. A check of the latest public archives of the works cited in the note's anteriority section remains to be done on the day of release.
