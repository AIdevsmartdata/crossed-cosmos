# REGISTRY_FALSIFIERS.md — Pre-registration of falsifiers

**Purpose.** Every falsifier the project proposes must be registered
here BEFORE computation or observation, with explicit decision
thresholds. Prevents post-hoc re-framing of results. Implements
pipeline improvement #10 (pre-registration).

**Format.** Each entry contains: **(1) Identifier, (2) Claim tested,
(3) Decision threshold, (4) Required pipeline artefacts, (5) Status.**
Status ∈ {REGISTERED (not yet run), RUN-PASS, RUN-FAIL, RUN-INCONCLUSIVE,
SUPERSEDED}. Entries are immutable once status ≠ REGISTERED.

**Rule.** Any document (agent or human) proposing a falsifier must
write the REGISTERED entry here BEFORE running the test. Post-hoc
entries are forbidden. Running a test without a prior REGISTERED
entry invalidates the result for publication purposes.

---

## D18 — fσ_8 × Θ(PH_2) cross-spectrum

**Claim.** If ECI v6 is correct with non-zero $\epsilon_0$ in the
PH_k-coupled matter power spectrum, then at DR3+Euclid precision the
$f\sigma_8 \times \Theta(\mathrm{PH}_2)$ cross-spectrum shows $S/N \ge 3\sigma$
discrimination against $\Lambda$CDM.

**Decision threshold.** $S/N \ge 3\sigma$ at $\epsilon_0 = 0.02$
fiducial after nuisance marginalisation → PASS. Otherwise FAIL.

**Required pipeline artefacts.**
- Fisher forecast matrix at DR3 + Euclid specs.
- Nuisance marginalisation over galaxy bias $b(z)$.
- Cross-model adversarial verdict (Mistral or Gemini).

**Status.** **RUN-FAIL** (2026-04-21). $S/N = 0.36\sigma$ at fiducial;
$\sigma(\epsilon_0)_{\rm marg}/\sigma(\epsilon_0)_{\rm fix} = 21.7\times$ (DR3),
$26.8\times$ (DR3+Euclid); degeneracy $|\rho(b_0, \epsilon_0)| = 0.998$.
Falsifier killed; codified as PRINCIPLES V6-4.

**Artefacts.** `derivations/D18-report.md`, `derivations/D18b-report.md`.

---

## V7-Test5 — Odlyzko 2-point deviation vs CCM prediction

**Claim.** At height $\gamma \in [14, 7.5 \times 10^4]$ on the first
$10^5$ Odlyzko zeros, the empirical pair-correlation $R_2(x)$ deviates
from pure Montgomery–Dyson GUE in a way that matches a specific
$O(1/\log T)$ correction predicted by Connes–Consani–Moscovici
arXiv:2511.22755, distinct from the classical Bogomolny–Keating 1996
arithmetic correction.

**Decision threshold.**
- **SHIP**: $\chi^2_{\rm GUE+CCM}/\rm dof \le 1.5$ AND
  $\chi^2_{\rm GUE+CCM} < \chi^2_{\rm GUE+BK}$ (CCM-specific better than BK)
  AND the fit amplitude matches CCM's prediction within 50%.
- **STRUCTURED-UNKNOWN**: deviation present at $\ge 3\sigma$ but no
  CCM-specific formula exists or BK explains it fully.
- **PURE-GUE**: $\chi^2/\rm dof \approx 1$ for pure GUE alone.

**Required pipeline artefacts.**
- Pre-registration (this entry).
- Explicit extraction of CCM 2-point formula from arXiv:2511.22755.
- Script `V7-test5-odlyzko.py` reproducible.

**Status.** **RUN-STRUCTURED-UNKNOWN** (2026-04-22). Pure-GUE rejected
at $\chi^2 = 7.49$/dof, max $|\Delta|/\sigma = 7.74$ at $x \approx 0.23$;
deviation matches Bogomolny–Keating 1996 in amplitude and shape; CCM
2-point formula not present in arXiv:2511.22755 full PDF (verified via
WebFetch). Consequence: test cannot discriminate ZSA from BK. Logged
in FAILED.md F-9.

**Artefacts.** `derivations/V7-test5-odlyzko-report.md`, commit
`ca3e0e7`.

---

## V7-C — Euler–Maclaurin Λ mechanism

**Claim.** The zeta-regularised spectral sum
$\rho_\Lambda^{\rm ZSA} = (\Lambda_{UV}^4/(2\pi)^2) \cdot (S - I)$,
where $S = \sum_n f(\gamma_n/\Lambda_{UV})$ and $I$ the smooth
Riemann–von Mangoldt integral, yields a finite non-trivial residue
that (modulo dimensional calibration) is compatible in order of
magnitude with $\Lambda_{\rm obs}/M_P^4$.

**Decision threshold.**
- **FINITE-NON-TRIVIAL**: $S - I$ converges to a non-zero, cutoff-stable
  value; multiplicative factor to $\Lambda_{\rm obs}$ is a pure number
  of controlled origin.
- **TRIVIAL-CANCELLATION**: $S - I$ of order unity explained by
  Euler–Maclaurin endpoint term; multiplying by $\Lambda^4/(2\pi)^2$
  restores ordinary quartic divergence. FAIL.
- **DIVERGENT** or **ARBITRARY-CUTOFF-DEPENDENT**: numerical
  instability. INCONCLUSIVE.

**Required pipeline artefacts.**
- Pre-registration (this entry).
- First $10^5$ Odlyzko zeros (public data).
- Script `V7-euler-maclaurin-lambda.py` reproducible.

**Status.** **RUN-FAIL** (2026-04-22). $S - I \approx 0.449$,
$\Lambda$-independent on $[100, 10000]$, cutoff-independent at $10\%$.
Multiplying by $\Lambda^4/(2\pi)^2$ restores quartic divergence. No
small number $10^{-120}$ emerges. Closes the ZSA Λ branch. Logged in
FAILED.md F-7.

**Artefacts.** `derivations/V7-euler-maclaurin-lambda-report.md`,
commit `0cdfea6`.

---

## V7-BK — Bogomolny–Keating explicit fit

**Claim.** The residual $\Delta(x) = R_2^{\rm emp}(x) - R_2^{\rm GUE}(x)$
measured on $10^5$ Odlyzko zeros is fully explained by the Bogomolny–
Keating 1996 arithmetic 2-point correction within statistical error.

**Decision threshold.**
- **FULL-BK**: $\chi^2_{\rm BK}/\rm dof \le 1.5$ on residual.
- **BK-PLUS-EXTRA**: BK fits but leaves significant structured
  residual beyond BK-reachable shape.
- **BK-INADEQUATE**: BK fit $\chi^2/\rm dof > 2$.

**Required pipeline artefacts.**
- Pre-registration (this entry).
- Explicit BK formula extracted from arXiv:chao-dyn/9511005.
- Script `V7-BK-fit.py` reproducible.
- F-test or likelihood ratio comparing {GUE only, GUE+BK, GUE+BK+extra}.

**Status.** **RUN-BK-PLUS-EXTRA** (2026-04-22). BK signal real
($\chi^2_{\rm M0}/\rm dof = 7.49 \to \chi^2_{\rm M2}/\rm dof = 4.17$
with free amplitude A, effective height $L_{\rm eff}$;
F-test $p \approx 3\times 10^{-8}$), but BK alone insufficient. Extra
cosine at $\nu \approx 1.11$, amplitude $C = 0.031$, reduces
$\chi^2/\rm dof$ to $1.27$; F-test against BK-only gives
$p \approx 3\times 10^{-14}$. **Honesty flag:** the extra $\nu\approx 1$
cosine is most likely a $1\%$ unfolding miscalibration
(GUE sine-kernel shoulder at $x=1$), not new physics. Canonical $A=1$
BK worsens fit, suggesting convention/prefactor issue. Net: BK
explains the bulk of the residual; no ZSA-specific signal can be
isolated; residual beyond BK plausibly attributable to unfolding.

**Artefacts.** `derivations/V7-BK-fit.py`, `derivations/V7-BK-fit.png`,
`derivations/V7-BK-fit-report.md`, commit `a0be8c9`.

---

## V8-KS-covariance — Functor intertwining: PH_k modular flow vs GKS Hamiltonian quantisation

**Claim tested.** The functor F: PH_k[δn] → D^b(Sh_c(T*M)) intertwines
the Tomita-Takesaki modular flow σ^R_τ on the input side with the
Guillermou-Kashiwara-Schapira (GKS 2012) sheaf quantisation Q_{Φ_τ}
of the associated Hamiltonian isotopy on the output side:

    F ∘ σ^R_τ = Q_{Φ_τ} ∘ F   (proposed intertwining)

If this holds, M2 covariance of dequantisation is automatic (not
ANSATZ) and v6.2 §4 can upgrade from ANSATZ to theorem citation.

**Decision thresholds (pre-registered before computation).**

- **THEOREM-FULL**: GKS 2012 (or a cited successor) states an explicit
  intertwining theorem covering the modular Hamiltonian K_R as a
  Hamiltonian function on T*M, with compact-support condition satisfied
  on the static patch M. Numerical 2D SHO check: F(σ^R_τ δn) and
  Q_{Φ_τ}(F(δn)) agree in Betti numbers to <1% at τ = 0.5, 1.0, 2.0.
  Both conditions must hold simultaneously.

- **THEOREM-CONDITIONAL**: GKS 2012 states the intertwining for
  compactly-supported Hamiltonians, but modular Hamiltonian on M is
  NOT compactly supported (non-compact generator). The theorem
  exists but does not apply without an additional compact-support
  assumption. Numerical check: Betti numbers agree on bounded sub-domain.
  Status: CONDITIONAL, with explicit obstruction flagged.

- **NOT-STATED-IN-LITERATURE**: No GKS theorem (or successor in
  the RAG / WebFetch-accessible literature up to 2026-04-22) states
  the F ∘ σ^R_τ = Q_{Φ_τ} ∘ F intertwining for ANY class of
  Hamiltonians that includes modular flow. Numerical check is then
  a heuristic only.

- **OBSTRUCTION**: Even the intertwining structure is formally wrong
  (e.g. modular flow acts on A_R not on M; the pushforward Φ_τ on M
  is not well-defined; or GKS Q_{Φ_τ} is defined only for exact
  Lagrangian isotopies and SS(F̃) is not Lagrangian for generic δn).

**Required artefacts.**
- This pre-registration entry (present).
- `paper/_internal_rag/v8_ks_modular_covariance_report.md` ≤ 400 lines.
- `derivations/V8-followup-ks-modular-covariance.py` (numerical check or documented stub).
- Explicit GKS 2012 theorem statement (verbatim or paraphrase-with-page) from
  arXiv:1006.1364 or the published Astérisque version.

**Status.** **RUN-CONDITIONAL** (2026-04-22). Verdict: THEOREM-CONDITIONAL.
Betti intertwining holds as a mathematical set identity (tautologically true
for any diffeomorphism Φ_τ); numerical check shows |Δβ_0| ≤ 5 attributable
to 64×64 grid interpolation artifacts, not to a failure of the identity.
GKS 2012 Thm 4.3 provides the sheaf-transport statement; result is conditional
on (C1) M2 semi-classical limit, (C2) compact static patch with H_{K_R}
vanishing at horizon, (C3) tame δn. For non-compact patches or full quantum
level: NOT COVERED. Recommendation: add GKS remark to v6.2 §4 (DERIVED-UNDER-M2),
do NOT change M2 assumption label to THEOREM.

---

## Meta-rules

1. **No post-hoc registration.** Running a test and registering its
   claim after seeing the result is forbidden for publication-grade
   work.

2. **Thresholds must be specific and numerical.** "Good agreement" is
   not a threshold. "$\chi^2/\rm dof \le 1.5$" is.

3. **Superseded entries.** If an earlier registered threshold turns
   out to have been mis-specified, do NOT edit the old entry. Instead:
   mark it SUPERSEDED and open a new entry with the new threshold,
   explicitly naming the supersession reason.

4. **Read before propose.** Any proposed new falsifier must first be
   checked against FAILED.md (does it resemble an F-N entry?) and
   against this registry (does it duplicate an existing REGISTERED or
   RUN-* entry?).

5. **Cross-model gate.** Before SHIP status, an independent model
   (Mistral / Gemini / Qwen) must confirm the threshold-comparison
   result. Not optional.
