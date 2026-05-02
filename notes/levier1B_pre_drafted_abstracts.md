# Levier #1B — Pre-Drafted Abstracts (Three Scenarios)

**Date:** 2026-05-02
**Purpose:** Ready-to-edit abstracts for each outcome of the Levier #1B MCMC run.
All bracketed PLACEHOLDER fields must be filled with actual posterior numbers
before any submission or public sharing. Do not circulate with placeholders.

**Reference run:** Levier #1B — 10-param NMC+w₀w_a joint fit, Planck 2018
(lowl.TT + lowl.EE + NPIPE CamSpec TTTEEE + lensing) + DESI DR2 BAO +
Pantheon+ + KiDS-1000 S₈, Cassini wall ON, ACT penalty OFF.

**Comparison anchor:** Wolf, Amon, Taylor & Peacock (2025), PRL,
arXiv:2504.07679. "Assessing cosmological evidence for non-minimal coupling."
log B = 7.34 ± 0.6 for NMC vs ΛCDM (Planck PR4 + DESI DR2 BAO + Pantheon+).

---

## Abstract A — Scenario A: PRD Letter (Detection Candidate)

**Trigger conditions:** ξ_χ ≠ 0 at ≥ 2σ (95% CI excludes zero)
AND H₀ retreats from Planck anchor toward SH0ES
AND S₈ tension with KiDS-1000 is reduced.

**Target venue:** Physical Review D, Letters section (~4 pages rapid communication).

---

We perform a joint Bayesian analysis of non-minimal coupling (NMC) between dark
energy and gravity using the Planck 2018 CMB power spectra (TT,TE,EE + lowl +
lensing), DESI DR2 BAO, Pantheon+ Type Ia supernovae, and the KiDS-1000
weak-lensing S₈ measurement. Our model parameterises the scalar-tensor coupling
through a dimensionless parameter ξ_χ and a thawing field amplitude χ_initial,
with a hard Cassini-Bertotti-Iess-Tortora (2003) prior enforcing solar-system
consistency. We find

  ξ_χ = [PLACEHOLDER] ± [PLACEHOLDER]  (68% CL)
  ξ_χ ∈ [[PLACEHOLDER], [PLACEHOLDER]] (95% CL, excludes zero at [PLACEHOLDER]σ)

with a Savage-Dickey Bayes factor of log B = [PLACEHOLDER] ± [PLACEHOLDER]
(statistical KDE uncertainty) favouring NMC over ΛCDM, broadly consistent with
Wolf et al. (2025, arXiv:2504.07679) who report log B = 7.34 ± 0.6 on Planck PR4
without KiDS-1000. Adding the KiDS-1000 S₈ prior tightens the growth-sector
constraints without biasing ξ_χ (consistent with the no-S₈ run of Wolf et al.),
providing an independent check. The H₀ tension with SH0ES (Riess et al. 2022,
73.04 ± 1.04 km/s/Mpc) reduces from [PLACEHOLDER]σ (ΛCDM with the same dataset)
to [PLACEHOLDER]σ, while the S₈ tension with KiDS-1000 (0.766 ± 0.020) reduces
from [PLACEHOLDER]σ to [PLACEHOLDER]σ. This is the first joint analysis combining
the NMC framework with weak-lensing S₈ data, and provides an independent
cross-check of Wolf et al. (2025) using a different CMB likelihood (Planck 2018
plik vs PR4 NPIPE) and an extended observational baseline.

---

**Honest caveats to include in the paper (not the abstract):**

1. Our log B estimate uses the Savage-Dickey density ratio with a Gaussian KDE.
   This approximates nested-sampling evidence; the systematic uncertainty in the
   KDE is ≳ 0.5 dex and should be stated explicitly.

2. The CMB likelihood here (Planck 2018 plik CamSpec TTTEEE) differs from
   Wolf+2025's (Planck PR4 NPIPE). NPIPE has lower noise at ℓ > 1000; our log B
   may differ from theirs by ~1-2 dex due to this alone. Frame the comparison as
   "consistent order of magnitude" not "independent confirmation at the quoted
   precision."

3. The tension-reduction claims (H₀, S₈) are derived from marginal 1-D posteriors
   using quadrature combination of uncertainties. Proper joint-posterior tension
   metrics (e.g., suspiciousness statistic) should be computed before the PRD
   submission.

4. If the ξ_χ detection is at exactly 2σ, describe it as "marginal evidence" not
   "detection." The threshold for a PRL-style detection claim is 3σ with two
   independent methods.

---

## Abstract B — Scenario B: JCAP (Mixed Result)

**Trigger conditions:** Exactly one of {H₀ tension reduction, S₈ tension
reduction} is observed, OR ξ_χ is marginal (< 2σ) while a background-expansion
shift is seen. Three sub-scenarios exist (B1/B2/B3 from
`notes/posterior_levier1B_README.md`).

**Target venue:** Journal of Cosmology and Astroparticle Physics (~12 pages,
methodological + observational contribution).

---

We present a joint Markov Chain Monte Carlo analysis of non-minimal coupling
(NMC) between dark energy and gravity incorporating, for the first time, the
KiDS-1000 weak-lensing S₈ measurement alongside Planck 2018 CMB, DESI DR2 BAO,
and Pantheon+ supernovae data. The NMC scalar field ξ_χ modifies the effective
gravitational coupling G_eff(k) and the post-Newtonian parameter γ_PPN, the
latter constrained by the Cassini-Bertotti-Iess-Tortora (2003) bound which we
enforce as a hard prior. We obtain

  ξ_χ = [PLACEHOLDER] ± [PLACEHOLDER]  (68% CL)

consistent with [zero / a non-zero value at [PLACEHOLDER]σ — FILL FROM ACTUAL
RESULT]. Our primary finding is that KiDS-1000 does not independently constrain
ξ_χ — confirming the result of Wolf et al. (2025, arXiv:2504.07679) that Planck's
sensitivity to CMB power-spectrum modifications drives any NMC Bayes factor — but
the joint S₈ constraint [FILL: does / does not] reduce the residual tension with
KiDS-1000 relative to the Planck-only NMC posterior. The [H₀ / S₈ — FILL] tension
with [SH0ES / KiDS-1000 — FILL] [is / is not] appreciably reduced. We discuss
the implications for the full Levier #1 analysis (adding early dark energy and a
dark-dimension sector) and for the robustness of NMC as a unified tension resolver.
Our analysis provides an independent consistency check of Wolf et al. (2025) using
Planck 2018 plik rather than Planck PR4 NPIPE and extends their dataset to
include growth-structure constraints.

---

**Honest caveats for the paper:**

1. A Scenario B result does NOT rule out NMC as a physical framework. It
   establishes that the 10-parameter sub-model studied here does not resolve both
   tensions simultaneously; the full Levier #1 (12-param, with EDE) may do so.

2. If ξ_χ < 2σ from zero in this run but Wolf+2025 found log B = 7.34, the
   discrepancy most likely comes from the CMB likelihood version (2018 plik vs PR4
   NPIPE). Do not frame this as a contradiction — frame it as a dataset dependence
   that motivates future work.

3. If S₈ retreats but H₀ does not: this is sub-scenario B2. The most natural
   interpretation is that the NMC coupling modifies the growth rate (G_eff < 1 at
   late times lowers σ₈ while leaving the expansion history H(z) near Planck). Be
   precise about which physical mechanism is responsible.

4. The Savage-Dickey log B from this run should be treated as illustrative, not
   competitive with MultiNest. Do not table-compare to Wolf+2025 at face value;
   state explicitly that the methods differ and give ≳ 1 dex systematic.

---

## Abstract C — Scenario C: Null Result Note

**Trigger conditions:** ξ_χ consistent with zero at 95% AND no tension reduction
for either H₀ or S₈.

**Target venue:** Not a standalone paper — this result would be documented as
an internal note and used to motivate the full Levier #1 run. If published,
suitable as a brief MNRAS Letter framed as a null result and upper bound.

**Framing principle:** A null result with Planck + KiDS is a meaningful constraint,
not a failure. Wolf+2025's positive detection was on Planck PR4 NPIPE; if our
Planck 2018 run finds a null, that is a dataset-version comparison result worth
documenting.

---

We report constraints on non-minimal coupling (NMC) between dark energy and
gravity from a joint analysis of Planck 2018 CMB, DESI DR2 BAO, Pantheon+
supernovae, and KiDS-1000 weak-lensing data. The NMC coupling parameter ξ_χ
characterises modifications to the effective gravitational constant G_eff(k);
its solar-system consistency is enforced via the Cassini-Bertotti-Iess-Tortora
bound as a hard prior. We find

  ξ_χ = [PLACEHOLDER] ± [PLACEHOLDER]  (68% CL, consistent with zero)
  |ξ_χ| < [PLACEHOLDER]  (95% upper bound)

and a Savage-Dickey Bayes factor of log B = [PLACEHOLDER], [inconclusive / mildly
favouring ΛCDM — FILL]. The H₀ tension with SH0ES (Riess et al. 2022) and the S₈
tension with KiDS-1000 are not significantly reduced in the NMC framework without
early dark energy. This result is [consistent with / in mild tension with — FILL]
Wolf et al. (2025, arXiv:2504.07679), who find log B = 7.34 ± 0.6 using Planck PR4
NPIPE; the discrepancy, if present, is attributed to the difference between the
Planck 2018 plik and PR4 NPIPE likelihoods at ℓ > 1000, where NPIPE achieves
lower noise and tighter G_eff constraints. We report the [PLACEHOLDER]-σ upper
bound on |ξ_χ| as a new constraint from the combined Planck 2018 + KiDS-1000 + DESI
DR2 dataset, and use this null result to motivate a full analysis including early
dark energy (EDE) and dark dimension parameters, which may be necessary for NMC
to simultaneously resolve the H₀ and S₈ tensions.

---

**Honest caveats for this scenario:**

1. If this run is null but Wolf+2025 is positive, the most likely cause is the CMB
   likelihood (2018 plik vs PR4 NPIPE). Do not claim the null invalidates Wolf+2025.
   Instead, treat this as a dataset sensitivity study.

2. A null Savage-Dickey log B (near 0 or negative) means the data neither favour
   nor disfavour NMC. This is agnostic, not a refutation.

3. Before concluding Scenario C, verify that the Planck likelihoods loaded and
   coupled to CLASS correctly. If the Cl_TT/Cl_TE/Cl_EE columns in the timing log
   show < 1 second per evaluation (suggesting the Planck likelihood was not called),
   the run has a wiring bug, not a physics null.

4. Upper bound: an |ξ_χ| < X at 95% from this run is a genuine new constraint from
   the Planck 2018 + KiDS dataset that Wolf+2025 did not report. Highlight it.

---

## Filling Instructions

When chains converge (R-1 < 0.02):

1. Run `python3 scripts/analysis/posterior_levier1B.py --chain-prefix /root/crossed-cosmos/eci_levier1B --burnin 0.3 --outdir notes/posterior_levier1B_<DATE>`
2. Read `notes/posterior_levier1B_<DATE>/summary.md`
3. Identify which scenario applies (check the "Scenario classification" section)
4. Copy the relevant abstract template above
5. Replace all PLACEHOLDER fields with actual numbers
6. Add the "Honest caveats" section as a paragraph in the Introduction/Discussion
7. Do not submit with un-filled PLACEHOLDER text

**Citation format for Wolf+2025:**
Wolf, M., Amon, A., Taylor, A. N., & Peacock, J. A. (2025). arXiv:2504.07679.
"Assessing cosmological evidence for non-minimal coupling." Physical Review Letters.
log B = 7.34 ± 0.6 (NMC vs ΛCDM, Planck PR4 + DESI DR2 BAO + Pantheon+).
*Do not cite a different log B value or a different arXiv number for this paper.*
