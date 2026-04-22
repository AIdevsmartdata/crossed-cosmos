# v6 Gap Analysis — Remaining Derivations, Literature Alignment, Attack Surface

**Prepared:** 2026-04-22 | **Rules:** V6-1, V6-4, PRINCIPLES rule 1, rule 12
**Baseline:** FAILED.md 17 entries (F-1 through F-19); no closed bridge re-proposed here.

---

## A. Additional Derivations That Would Strengthen v6 Before JHEP Submission

### A1. Proof of M1 as a Type-II Theorem

**Status: open, highest priority.** F-1 records that the equality form of the main bound was
ruled out by three independent derivation agents; the re-open condition stated there is precisely
a type-II theorem that *identifies* (not merely bounds) the modular-commutator source with
κ_R C_k. The gap between "bound under M1 ansatz" and "type-II theorem" is the single largest
vulnerability in v6. No paper in the 2024–2026 literature surveyed closes this gap directly.
The nearest anchor is Kirklin (2025, JHEP07:192, arXiv:2412.01903), which proves the GSL beyond
semiclassical regime using null-translation invariance and dynamical cuts, but does not introduce
a complexity source term — it proves a *monotonicity* result, not a complexity rate law.

**What is needed.** A rigorous identification, within the semifinite type-II factor A_R of CLPW/
DEHK, of the internal-entropy-production operator ∂_τ K_R |_{modular-commutator} with κ_R C_k
up to a positive remainder. This would require: (i) a spectral decomposition of the modular
Hamiltonian flow generator on the type-II trace; (ii) operator-growth estimates showing the
dominant contribution is the k-design complexity functional of Ma–Huang (2025); (iii) a
Fan-saturation-compatible rescaling of C_k^max that keeps the logistic envelope (Prop. 1)
tight. None of steps (i)–(iii) is achievable by ansatz; each requires a direct type-II
operator-algebraic argument.

**Interim mitigation.** v6 already labels M1 explicitly as POSTULATE and prints the internal
derivation audit verdict (Appendix, computation note). No further prose change is needed unless
a preprint on operator growth in type-II semifinite factors appears between now and submission —
in which case the audit pipeline must flag it via weekly V6-5 surveillance.

### A2. Full CLT Theorem for M2 (Beyond N = 20 Numerical Check)

**Status: open, medium priority.** The dequantisation map (§3) establishes δn as mean-zero and
covariant under modular flow; M2 postulates Gaussian recovery by a CLT/LLN argument on the
unobserved QRF degrees of freedom. The numerical check at N ∈ {12, 16, 20} (V6-dequantisation-
map.py) is a scaffold, not a theorem.

**Pathway.** The most direct route is the quantum CLT of Goderis–Vets–Verbaere (1989 / 1990)
and its operator-algebraic refinements for type-II$_1$ factors (Petz 1990, Junge–Xu 2003). A
rigorous statement would read: for the coarse-graining map Tr_R[ρ_R ⊗^{N} · ] with N
independent QRF copies, the normalised fluctuation field N^{-1/2} Σ_i δn_i converges in
distribution (w.r.t. the tracial state on A_R) to a Gaussian quantum process. The key
hypothesis is a type-II analogue of the classical Lindeberg condition; for bounded local
observables n̂(x) on a finite lattice, this condition is automatic. For field-theoretic δn(x)
with UV smearing at scale σ_cg, convergence holds within the smeared sector by standard results.

**Scope decision (rule 12).** A full proof in the infinite-dimensional type-II_∞ case (CLPW/
DEHK) requires functional-analytic care beyond the scope of a 7-page paper. The honest framing
is: (a) state the CLT as a theorem for the finite-N toy model (N copies, bounded observables);
(b) state M2 as a postulate for the infinite-dimensional field-theoretic case, citing the finite-N
result as evidence. This is what v6.0.3 already does; the gap is that step (a) has not been
formally written as a Theorem+Proof in the paper. Adding a Theorem 2 (CLT for bounded
observables, N-copy toy model) with a proof sketch citing Goderis–Vets–Verbaere would close the
easy half of this gap before JHEP submission.

### A3. First-Principles Anchor for α in M3

**Status: partially addressed, clarification needed.** The current prose (Ass. M3) states:
"inspired by the Barrow–Δ ≲ 0.1 fractal-horizon bound." This is the correct motivating
reference — Barrow (2020), Phys. Lett. B 808, 135643 showed that quantum-gravitational fractal
corrections to the horizon give S ~ A^{1+Δ/2} with 0 ≤ Δ ≤ 1, and observational constraints
push Δ ≲ 0.1 (Anagnostopoulos et al. 2020, Phys. Lett. B 807, 135552; Jusufi et al. 2021).
The identification α = Δ/2 (up to normalisation convention) gives α ∈ (0, 0.05], tighter than
the (0, 0.1] stated in M3.

**Gap.** The citation is present in spirit but v6.0.3 does not explicitly cite Barrow (2020)
by DOI or bib-key, nor does it state the α ↔ Δ/2 mapping in prose. Under PRINCIPLES rule 3
(bib discipline) and rule 1 (honesty gate), the Barrow cite must be verified and added to
v6.bib before submission. The observational constraint Δ ≲ 0.1 tightens the M3 prior to
α ≲ 0.05 — this should be stated as a prior anchor, not a derivation. The α = 0.095 fiducial
used in the phenomenological companion (v5) sits just at the edge of this bound and may need
a note flagging that the Barrow anchor gives α ≲ 0.05 while the chameleon calibration gives
0.095; the two are compatible only if the fractal and screening parameters are not the same α.

**Action before submission.** Add `Barrow2020` bib entry (doi:10.1016/j.physletb.2020.135643).
Add one sentence to M3 stating the Barrow–Δ mapping and the observational prior. No equation
moves.

### A4. Extension of KS-Microlocal Covariance Beyond Compact dS Static Patch — FLRW

**Status: open, medium priority.** The GKS 2012 (Guillermou–Kashiwara–Schapira) sheaf
quantisation theorem used in §3 (dequantisation section) requires two hypotheses on the
Hamiltonian isotopy Φ_{τ_R}: (i) homogeneity of degree 1 in the cotangent coordinate;
(ii) compact support of Φ_{τ_R} − id. Both hold for the Bisognano–Wichmann modular flow
at the dS Killing horizon (cosmological Killing vector vanishes at the horizon, giving
compact-support behaviour in the static patch). In FLRW spacetimes, hypothesis (ii) fails
generically: the comoving observer's causal diamond is expanding, the Killing vector is not
static, and the isotopy has non-compact support in the cotangent bundle over the full lightcone.

**Partial positive result.** Kudler-Flam–Leutheusser–Satishchandran (2024, arXiv:2406.01669,
"Algebraic Observational Cosmology") construct a type-II algebra for a comoving FLRW observer
(type II_1 in empty dS, type II_∞ in inflationary FLRW), with von Neumann entropy equal to
the generalized entropy of the causal diamond. This confirms that the crossed-product setup of
v6 §2 extends to FLRW at the algebraic level. However, they do not prove a KS-microlocal
covariance result for the PH_k functor in FLRW; that would require showing GKS 2012 applies to
the expanding-diamond isotopy.

**Honest framing for v6.** The KS covariance result is currently conditional on M2 and the dS
static-patch geometry. A footnote or remark in §3 should state: "The GKS quantisation requires
compact-support hypothesis (ii) on the isotopy; this holds in the dS static patch but not in
generic FLRW causal diamonds, where the PH_k covariance under modular flow remains an open
extension." This is the correct scoping under rule 12 (no claim larger than the derivation).
The Kudler-Flam et al. 2024 paper is a natural new citation for the FLRW algebraic setup.

### A5. Explicit Connection to Ceyhan–Faulkner 2020 for the Pinsker Step

**Status: adequately cited, proof sketch could be sharpened.** The proof sketch (§3, Pinsker
step) cites Ceyhan–Faulkner (2020, arXiv:1812.04683, Commun. Math. Phys. 377:999) for the
half-sided modular pushforward that bounds −dS_rel/dτ_R ≤ |d⟨K_R⟩/dτ_R|. This is the
correct citation: CF 2020 prove that for half-sided modular inclusions, the relative entropy
flow satisfies a Wall-type inequality via the ANEC, and the Longo positivity bound
supplementing it is arXiv:1904.10024.

**Gap.** The v6 proof sketch does not make explicit *which* theorem of CF 2020 is invoked.
The relevant result is their Theorem 1.2 (half-sided modular inclusion + finite ANEC ⟹
monotonicity of relative entropy along modular flow). For JHEP review, a referee familiar with
CF 2020 will ask: does the type-II crossed-product of CLPW/DEHK satisfy the half-sided modular
inclusion hypothesis of CF Thm 1.2? The answer is: yes, by construction — the CLPW nested
algebra A_R ⊆ A_{R'} is a standard half-sided inclusion in the Borchers sense, and the
Connes cocycle fixes the modular data. Adding a parenthetical "(Ceyhan–Faulkner Thm 1.2, using
the CLPW nested inclusion as the half-sided modular inclusion hypothesis)" closes this gap at
zero cost.

A further recent note: arXiv:2503.04651 (2025) "A New Proof of the QNEC" (Comm. Math. Phys.
2025) strengthens the CF machinery for general half-sided inclusions without the explicit ANEC
finiteness assumption. Citing this as a "see also" would make the Pinsker step more robust.

### A6. Submultiplicativity Lemma — Upgrade from Sympy-Toy to Type-II Theorem?

**Status: sympy verification on 8+8 qubit toy, not a type-II theorem.** Lemma (submult, §3)
states that RHS(R ∪ R') ≤ κ_R C_k[ρ_R] C_k[ρ_{R'∖R}] min(Θ_R, Θ_{R'∖R}), verified
numerically (N_R = N_{R'∖R} = 4 qubits, XXZ, β=1; all three asserts pass to < 10^{-8}).

**Upgrade pathway.** The C_k submultiplicativity step rests on the purity inequality
Tr(ρ_{R∪R'}^2) ≥ Tr(ρ_R^2) Tr(ρ_{R'∖R}^2) via Cauchy–Schwarz on the CLPW conditional
expectation. For the 2-Rényi surrogate of k-design complexity used in v6, this is a
*mathematical fact* (Cauchy–Schwarz in the Hilbert–Schmidt inner product of the type-II trace)
that holds in any semifinite von Neumann algebra with a faithful normal trace, not just for
finite-dimensional qubits. A one-paragraph proof in the paper (no sympy needed) invoking:
(a) Cauchy–Schwarz for the type-II trace (standard, e.g. Takesaki Vol. II, §IX); (b) the
Ma–Huang PRU complexity ≤ purity^{-1} (by definition of the 2-Rényi complexity surrogate);
(c) Yip et al. 2024 nesting property for PH_k on filtered simplicial complexes —
would elevate the lemma from "numerical verification" to "theorem under sub-postulate of M1
in the bipartite regime." The Ma–Huang paper does not state submultiplicativity for type-II
factors; the step (b) above is a sub-postulate, explicitly stated as such in v6 prose. The
upgrade is achievable before JHEP submission.

### A7. Does the KS-Microlocal Functor F Enable a Full Proof of the Main Theorem?

**Status: conditional under M2, cannot be upgraded without closing M2.** Agent 9 (v8 synthesis,
v8_ks_modular_covariance_report.md) showed that the GKS 2012 sheaf quantisation gives a
categorical identity F ∘ σ^R_{τ_R} = Q_{Φ_{τ_R}} ∘ F at the level of sub-level filtrations,
making PH_k-covariance under modular flow *derived* under M2 rather than separately postulated.
This is a genuine structural result already incorporated in v6.0.3 §3.

The functor F does not, however, bypass M1: it operates on the dequantised field δn (output of
M2), not on the quantum state ρ_R directly. The chain is: ρ_R →(M2)→ δn →(F)→ PH_k. A full
proof of Eq. (1) from first principles would require M2 to be a theorem (see A2 above) and M1
to be a theorem (A1). The KS functor closes only the topological-activator link, which was
already the weakest of the three postulates. Net assessment: the KS functor result is correctly
incorporated and correctly scoped; it does not enable a full proof, and PRINCIPLES rule 12
prevents claiming otherwise.

---

## B. Published Formal GSL Results 2024–2026 That Align With v6

### B1. Faulkner–Speranza 2024 (arXiv:2405.00847, JHEP11(2024)099)
*Already cited in v6.* Derives GSL for arbitrary cuts of Killing horizons from crossed-product
gravitational algebras; crossed-product entropy = generalised entropy in semiclassical limit;
reproduces Wall's monotonicity as a corollary. Direct precursor to v6: the (L1) Θ→1 limit of
Eq. (1) recovers precisely the Faulkner–Speranza bound. **Alignment: direct anchor.**

### B2. Kirklin 2025 (arXiv:2412.01903, JHEP07(2025)192)
*Already cited.* Proves GSL beyond semiclassical regime, to all perturbative orders, without
UV cutoff, using null-translation invariance and dynamical cuts (quantum reference frames for
horizon location). The modified GSL bounds ΔS_gen by a free-energy term of the cut degrees of
freedom. This is a stronger result than Faulkner–Speranza but still does not introduce a
complexity source: the bound is in terms of free energy of QRF cuts, not k-design C_k.
**Alignment: v6 extends this line by identifying the source term with C_k (under M1).**

### B3. Liu et al. / Subregion Algebras 2026 (arXiv:2601.07915, Jan 2026)
*Not yet cited in v6.* Studies type-II_∞ subregion algebras for null-surface horizon cuts;
proves GSL for non-stationary linearised perturbations of Killing horizons via nesting of
one-parameter families of horizon subalgebras; proves quantum focusing conjecture (QFC) in
perturbative quantum gravity using half-sided modular inclusion. **Key alignment:** the
nesting-implies-GSL structure is precisely the algebraic mechanism v6 exploits in the
submultiplicativity Lemma (A6). The QFC proof via half-sided modular inclusion reinforces the
Pinsker step (A5). **Action:** add `Liu2026Subregion` bib entry (arXiv:2601.07915) and cite
in §3 (Pinsker step and Lemma).

### B4. Kudler-Flam–Leutheusser–Satishchandran 2024 (arXiv:2406.01669)
*Not yet cited in v6.* Constructs type-II algebra for comoving FLRW observer, confirms
S_vN = S_gen for semiclassical states. Directly relevant to A4 (FLRW extension). **Action:**
add `KudlerFlam2024AlgCosm` bib entry and cite in §2 footnote on FLRW scope.

### B5. New Proof of the QNEC 2025 (arXiv:2503.04651, Commun. Math. Phys. 2025)
*Not yet cited.* Strengthens the Ceyhan–Faulkner half-sided modular inclusion machinery,
removing the ANEC finiteness assumption. Relevant to the Pinsker step (A5). **Action:** add
as "see also" in the proof-sketch footnote.

### B6. No 2026 Paper Found on Type-II GSL + Complexity Rate
The web survey (conducted 2026-04-22) found no 2026 arXiv preprint that simultaneously:
proves a type-II GSL inequality, identifies the source with a complexity functional, and
makes the modular-time differential statement of Eq. (1). The closest is arXiv:2503.10753
("Quantum complexity in gravity, QFT, and quantum information," review, 2025), which surveys
the landscape but does not prove a new bound. **v6 is not pre-scooped as of 2026-04-22.**
Weekly V6-5 surveillance (PRINCIPLES V6-5) must continue until arXiv submission.

---

## C. Published Results That Contradict or Compete With v6

### C1. Equality Claims — None Found
No published paper (2024–2026) claims dS_gen/dτ_R = κ_R C_k Θ as an equality for type-II
algebras. The equality form was internally ruled out (FAILED.md F-1). The Fan (2022) log-
Krylov equality applies to ordinary-time Krylov complexity in a specific spreading regime, not
to modular-time type-II generalised entropy; v6 recovers Fan as a saturating limit, not as a
competitor. **No external contradiction on this point.**

### C2. Alternative Complexity Functionals
Several programmes propose different source terms for entropy rate bounds:
- **Complexity = Volume (Susskind 2014):** geometric volume of Einstein-Rosen bridge; not
  directly in conflict — v6 operates on the modular-time algebraic side, C=V on the
  holographic geometric side. The two are complementary, as stated in §3 (§sec:compgrav).
- **Complexity = Action (Brown–Susskind 2016):** same complementarity argument.
- **Carrasco–Pedraza–Svesko–Weller-Davies 2023 (CPSD 2023):** variational complexity/volume
  first-law identity reproducing linearised Einstein equations as an equality. This is a static
  first-variation equality on a bulk slice; v6 is a temporal differential inequality on A_R.
  Already cited and contextualised in §3 (§sec:compgrav). **Not a contradiction.**
- **Caputa–Magan–Patramanis–Tonni 2024 (arXiv:2024):** spread complexity under modular
  flow — this is the identification v6 adopts as M1' sub-postulate. **Alignment, not
  competition.**
- **Bianconi 2025:** cited in v6 footnote as using a Lagrange-multiplier field in relative-
  entropy action distinct from v6's Θ activator. No conflict.

### C3. Verlinde 2011/2017 Entropic Gravity
Verlinde's framework derives Newton's law from entropy gradients; it operates at the
thermodynamic level without a complexity source term. It does not claim a rate inequality for
generalised entropy along modular flow. No direct conflict with v6. The web survey found no
2025–2026 paper that uses Verlinde's framework to refute a complexity-bounded GSL. **Not a
competitor.**

### C4. No Refutation Framework Found
The web survey found no 2025–2026 paper proposing a competing framework that: (i) uses type-II
crossed-product algebras, (ii) identifies a different (non-complexity) source for dS_gen/dτ_R,
and (iii) makes quantitatively sharper predictions in the dS static-patch regime. The closest
potential competitor is Kirklin 2025 (B2), whose free-energy cut bound is *a different
observable* (free energy of horizon cut QRF) not a complexity functional — the two bounds are
likely compatible (both ≥ 0 and both below some common ceiling), though a direct comparison
inequality has not been proved.

---

## D. Publications That v6 May Invalidate or Supersede

### D1. Brown–Susskind Second Law of Complexity (arXiv:1701.01107, PRD 97:086015, 2018)
Brown–Susskind conjecture that quantum complexity grows monotonically until exponential
saturation at C_max ~ exp(S). This is a *conjecture* (no type-II proof), and they work with
circuit complexity in ordinary time, not modular time. v6 Eq. (1) **extends** the Brown–
Susskind ansatz to the modular-time type-II setting; it does not invalidate B-S, it postulates
B-S as M1. **No supersession — M1 is explicitly a Brown–Susskind analogy, not a derivation.**

### D2. Fan 2022 Logarithmic Krylov Form
Fan (2022) states an equality $\dot S_K = \dot C_K / C_K$ in the logarithmic Krylov growth
regime. v6 Prop. 1 logistic envelope shows that the Fan equality emerges as the leading-order
expansion of the logistic at C_k → C_k^max; Fan is recovered as a *saturating limit*, not
contradicted. v6 does not supersede Fan — it contextualises Fan within a broader inequality.

### D3. Earlier EGJ Applications Assuming Equality
The Eling–Guedens–Jacobson (EGJ) 2006 framework writes dS = δQ/T + d_iS as an equality for
the internal production term. v6 takes the strict inequality form for d_iS ≤ κ_R C_k Θ rather
than equality. This is not an invalidation of EGJ — EGJ's d_iS is a geometric quantity (shear
squared of the null congruence), which is a different object from C_k. The (L4) EGJ limit in
§4 of v6 shows the two are compatible: in the strict classical limit (δn → 0), v6 reduces to
the Clausius form without contradicting EGJ's equality for the geometric contribution.

### D4. No "equality form" Paper to Supersede
The survey found no 2024–2026 paper claiming dS_gen/dτ_R = [complexity term] as an equality
in the type-II modular-flow setting. Therefore v6 does not supersede any published equality
claim — it simply does not make one (V6-1).

---

## E. Open Questions v6 Explicitly Defers

1. **M1 as a type-II theorem** (A1 above). The paper states "no type-II theorem is claimed"
   in Ass. M1. Remains open post-submission.
2. **Full CLT for M2 in the infinite-dimensional type-II_∞ case** (A2). Paper defers to "full
   proof outside scope."
3. **First-principles derivation of α** (A3). M3 is CONJECTURAL; α is a fit parameter anchored
   by Barrow and chameleon calibration but not derived.
4. **FLRW extension** of KS covariance (A4). Static-patch only; FLRW is explicitly out of scope.
5. **Operational measurement protocol** for C_k or Θ. §6 outlook notes the Einstein-analogy
   framing is motivation, not protocol. No proposal for experimental access to k-design C_k
   along modular flow.
6. **Holographic embedding.** v6 works on the algebra-level without an explicit holographic
   dictionary to a bulk dual. Whether the modular flow parameter τ_R corresponds to a geometric
   radial coordinate in a bulk description remains open (cf. arXiv:2410.23334 "Spread Complexity
   Rate as Proper Momentum" for one direction).

---

## F. Attack on v6 From 2025–2026 Literature — Systematic Check

The following are the adversarial attack surfaces surveyed against the 2024–2026 literature.

**Attack F1: Equality counter-example in type-II algebra.**
Threat: a type-II algebra with a modular flow that *saturates* Eq. (1) to an equality for all
states, contradicting the strict-inequality interpretation.
Literature verdict: no such counter-example found. The Kirklin 2025 and Faulkner–Speranza 2024
results prove monotonicity (ΔS_gen ≥ 0) but never claim equality in the differential form.
The Fan 2022 equality is a *different* regime (Krylov, not modular-flow type-II). **No
active threat.** V6-1 is safe.

**Attack F2: A paper proving the GSL takes a *sharper* form than Eq. (1).**
Threat: a bound dS_gen/dτ_R ≤ f(C_k) with f strictly below κ_R C_k Θ.
Literature verdict: the Kirklin 2025 free-energy bound is a different observable; no paper
derives a sharper complexity-specific upper bound. The logistic envelope Prop. 1 is already a
tightening within v6. **No active threat.**

**Attack F3: A paper showing C_k is not well-defined for type-II factors.**
Threat: the Ma–Huang 2025 PRU complexity is defined for finite-dimensional Hilbert spaces;
a type-II_∞ factor has no finite-dimensional PRU.
Assessment: this is a *known* issue already flagged in the v6 proof sketch — the spread-
complexity identification (M1') uses the Caputa–Magan 2024 modular-flow version evaluated on
the tracial vacuum, which is formally defined even in infinite-dimensional factors via the
Lanczos algorithm truncated at the Haferkamp scale. The Ma–Huang finite-dimensional definition
is used only for the saturation scale C_k^max ~ exp(S_R), where S_R is the type-II von Neumann
entropy (well-defined in CLPW/DEHK). A referee could push on this; the honest response is that
C_k is defined by its operational properties (M1 sub-postulate), not by a unique formula.
**Potential referee objection, not a literature counter-example.** Mitigation: add a clarifying
sentence to the C_k definition paragraph in §2.

**Attack F4: FLRW type-II algebra does not satisfy the GKS 2012 compact-support hypothesis.**
Confirmed in A4 above. This is a genuine scope limitation, not a contradiction within scope.
v6 is scoped to the dS static patch; the FLRW extension is open. **Acknowledged, contained.**

**Attack F5: The Barrow α anchor is observationally disfavoured.**
The 2026 paper "Barrow and Tsallis entropies after the DESI DR2 BAO data" (arXiv:2504.12205)
was found in the web survey. It applies Barrow entropy to Friedmann cosmology and finds
updated constraints on Δ from DESI DR2. If this paper finds Δ compatible with zero (standard
BH entropy, no fractal correction), the Barrow prior for α in M3 is weakened. However, v6
uses Barrow only as a motivational anchor for the prior range α ∈ (0, 0.1]; the formal
inequality (1) requires only α > 0. **The observational status of Barrow entropy does not
invalidate v6 formally; it only weakens one motivational anchor for M3.**
Action: check arXiv:2504.12205 constraints before submission and update M3 prose if Δ = 0
is now strongly favoured (it would make α purely a fit parameter with no external anchor).

**Attack F6: Pedraza–Svesko–Weller-Davies scoop risk.**
PRINCIPLES V6-5 names Pedraza–Svesko–Weller-Davies as the group most likely to publish a
time-differential gravity-from-complexity statement. The web survey found no 2025–2026 paper
by these authors that states a modular-time differential inequality for type-II S_gen with a
complexity source. The CPSD 2023 paper is a static first-variation equality; v6 addresses a
different axis. **No active scoop as of 2026-04-22.** Surveillance must continue.

---

## G. Summary of Actions Before JHEP Submission

| Priority | Action | Rule |
|---|---|---|
| HIGH | Add `Barrow2020` bib entry (doi:10.1016/j.physletb.2020.135643); state α ↔ Δ/2 mapping in M3 | rule 1, rule 3 |
| HIGH | Add `Liu2026Subregion` (arXiv:2601.07915) for Pinsker step and Lemma in §3 | rule 1, rule 3 |
| HIGH | Add `KudlerFlam2024AlgCosm` (arXiv:2406.01669) for FLRW scope note in §2 | rule 1, rule 3 |
| MEDIUM | Add `NewProofQNEC2025` (arXiv:2503.04651) as "see also" in Pinsker footnote | rule 3 |
| MEDIUM | Elevate submultiplicativity Lemma to formal proof-sketch using Cauchy–Schwarz on type-II trace (A6) | rule 12 |
| MEDIUM | Add Theorem 2 (CLT, bounded observables, N-copy toy model) citing Goderis–Vets–Verbaere (A2) | rule 12 |
| MEDIUM | Add footnote on GKS compact-support failure in FLRW (A4) | rule 12 |
| LOW | Add parenthetical citing CF 2020 Thm 1.2 + CLPW nested inclusion in Pinsker step (A5) | rule 12 |
| LOW | Clarify C_k definition for type-II_∞ case (Attack F3 mitigation) | rule 12 |
| MONITORING | Check arXiv:2504.12205 Barrow/DESI DR2 constraint on Δ | V6-4 (no cosmology in v6), rule 1 |
| MONITORING | Weekly V6-5 scoop surveillance until arXiv submission | V6-5 |

---

*File: paper/_internal_rag/v6_gap_analysis.md | Lines: ~390 | Do not commit without bib-DOI verification of all new entries listed in §G.*
