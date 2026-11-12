# The transfer-matrix gap of four-dimensional SU(2) lattice gauge theory tends to zero at weak coupling, with an explicit rate in infinite volume

Version 1.3 (12 November 2026; first deposit). Author: Kévin Rémondière (ORCID [0009-0008-2443-7166](https://orcid.org/0009-0008-2443-7166)). A technical note with proofs written in full (35 pages).

## What the note says, and does not say
- For the SU(2) Wilson lattice gauge theory on Z⁴ and every family μ_β of translation-invariant Gibbs states that are reflection positive for the time reflection through a hyperplane of sites, the gap m(μ_β) = −log‖T|_{Ω⊥}‖ of the one-step transfer operator tends to 0 as β → ∞ (β = Wilson coupling). For each fixed integer t ≥ 1, limsup m ≤ B(t) = (2/t) log(c(0)/c(t)) = O((log t)/t). Same in the gauge-invariant sector, on the positive spectrum, under cubic symmetry, and after removing the eigenspaces at ±1.
- **New in 1.3: an explicit rate.** For β ≥ 10²²⁸ and every such state, m ≤ 24 β^(−1/120) log β (and 36 β^(−1/120) log β for the positive part). The proof quantifies the Gaussian free-Maxwell limit by Stein's method for the conditional law in a box that grows with β. The bound is below 1 only for β of order 10⁴⁵⁵ and beyond, and is far above the expected exponentially small gap: it is a rate in the sense of order in β, not a numerically useful bound.
- **Not claimed**: neither assertion of Problem 5.1 of Chatterjee; no exponential rate; nothing at moderate β; no confinement statement (the bound holds also for U(1) in its Coulomb phase); no continuum mass gap. The theorem of Bhattacharjee et al. at fixed lattice size with rate O((log β)/β) is a different statement; neither implies the other (Section 1.3 of the note, conversion of β included). Historical novelty is not established.
- Written by AI models and read by other AI models (roles in "Use of AI"); not refereed; no human has checked the proofs.

## Contents
- `note/` : `.tex`, `.pdf`, three `pdflatex` logs.
- `reproduction/` : the six programs of version 1.0 with their first outputs and the replay of 11 November.
- `rejeu_v1_3/` : replay of 12 November by an agent other than the authors (sandbox without privileges or network): Opus's programs for the Stokes appendix and the rate (unchanged, outputs and comparison), a second independent implementation of the Stokes test (`ma_stokes/`), the exact-arithmetic recomputation of every constant (`comptabilite/`), outputs in `sorties/`.
- `relectures/` : reviews by models of other families (GPT-6.1 Sol, DeepSeek V4 Pro): task part of the prompts and answers. Two standard blocks of the project were removed from the prompts.
- `CHAINE_DE_PREUVE.md` : which lemma was redone line by line, which only read; `ANTERIORITE_v1_3.md`.
- `SHA256SUMS` : `sha256sum -c SHA256SUMS`.

Build: `pdflatex` three times on `note/gap_vanishes_weak_coupling_v1_3.tex`.

## Notes on the programs and reference outputs in `rejeu_v1_3/`
- `programmes_opus_stokes/run1.py ... run7.py` are complete, self-contained programs (library + driver + parameters concatenated); they are the ones to run. `programmes_opus_stokes/fragments_non_autonomes/` holds the pieces they were concatenated from: `stokes_lib.py` is a library with no output of its own, and `drv_run1.py`, `drv_su2.py`, `drv_su2b.py`, `drv_L4.py` are NOT self-contained (they crash alone with `NameError`). `drv_run1.py` and `drv_L4.py` run after `cat stokes_lib.py drv_X.py > X.py` (checked in the sandbox: they reproduce `run1` and `run7`); `drv_su2.py` and `drv_su2b.py` are templates that also need the parameter lines (`FAMS, NCONF, SEED, STEPS_FIRST, NEG, TLIM, DTYPE`) placed before them, as in `run2.py` to `run6.py`, which are the complete versions.
- `ma_stokes/stokes_ma.py` is the generic program of the second, independent implementation of the Stokes test (arguments: box side and number of configurations); its outputs are those of the three parameter files derived from it: `ma_L2.py`, `ma_L4.py`, `ma_L2_dfs_longdouble.py`, `ma_L4_kruskal_longdouble.py`. `stokes_ma.py` itself has no reference output of its own.
- `sorties/ma_L2_dfs_longdouble.stdout.txt` and `sorties/ma_L4_kruskal_longdouble.stdout.txt` are the outputs of the corrected extended-precision runs (matrices renormalised in extended precision; residual maxima 5.5e-16 and 9.6e-16). An earlier run, whose matrices were renormalised in double precision (residual 1.03e-12), has been removed because it is not a valid extended-precision run.
- `sorties/run5.stdout.txt` is the output of the replay from the git archive of the package, 12 November 2026 (432 loops, max residual 1.201e-15, no violation). `sorties/run5.first_replay_TRUNCATED_at_time_limit_353_of_432_loops.stdout.txt` is the first replay, which stopped at the time limit after 353 of 432 loops (max residual 1.129e-15); it is kept for the record.
