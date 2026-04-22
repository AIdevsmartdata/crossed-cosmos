# GROUND_TRUTH.md — What the ECI paper actually defends (v4.6)

*Purpose.* A single-author, no-hedging-soup statement of the thesis, its load
bearers, and its honestly-labelled weaknesses. Any editing agent writing into
`paper/*.tex` after v4.6 must read this file first, DECISIONS.md second,
PRINCIPLES.md third, `_internal_rag/INDEX.md` fourth, and `_rag/INDEX.md`
last.

---

## Part A — The thesis

ECI (Entanglement–Complexity–Information) is an **architectural synthesis**,
not a derivation. It assembles six independently-established research
programs from 2022–2026 into one predictive canvas with a shared scalar
sector and a shared Jordan-frame NMC Lagrangian, and reads out a handful of
falsifiable phenomenological consequences at late times (dark energy, H₀
tension, dark matter, solar-system gravity, large-scale structure
perturbations). The six programs are: (i) observer-dependent type-II
crossed-product von Neumann algebras for QRFs (Chandrasekaran–Longo–
Penington–Witten 2023; De Vuyst–Eccles–Höhn–Kirklin 2025a,b); (ii) DESI DR2
dynamical-dark-energy preference at 2.6–3.9σ (DESI Coll. 2503.14738)
addressed by NMC thawing quintessence ξ_χ R χ²/2 (Ye 2025, Wolf et al. 2025,
Pan & Ye 2026); (iii) the H₀ tension reduced to ∼2σ by axion-like Early
Dark Energy with f_EDE = 0.09 ± 0.03 (Poulin–Smith 2026 + ACT DR6
Calabrese 2025); (iv) the Dark Dimension scenario with species-scale
exponent c' = 1/6 (Montero–Vafa–Valenzuela 2022; Anchordoqui–Antoniadis–
Lüst 2023) as a microscopic DM candidate via the KK tower; (v) Cryptographic
Censorship (Engelhardt–Gesteau–Harlow et al.) as a working conjecture on
admissible bulk geometries, made operational in cosmology only through an
explicit toy dictionary isolated in Appendix A; (vi) persistent-homology
diagnostics of primordial non-Gaussianity (Matsubara 2003 baseline;
Yip 2024, Calles 2025 for the PH_k refinement).

**What ECI is claiming (v4.6).** That the six programs admit a joint
Lagrangian-level description (A1–A6 + the two-field (φ, χ) action of §2)
whose background-level phenomenology is *internally consistent* and *sits
at a quantitatively specified distance* from DESI DR2+DESY5; that this
distance is **not** an ECI-specific failure but a property of the entire
non-phantom thawing family (3.29σ for ECI vs 3.33σ for the Scherrer–Sen
minimal-coupling line under the reconstructed DR2+DESY5 covariance); that
§3.5–§3.7 contain **predictions** with explicit numerical widths (the NMC
w_a-track half-width Δw_a^ECI ≈ 1.1×10⁻² at χ₀ = M_P/10; the linear-
perturbation |Δf σ₈ / f σ₈| ≲ 0.4% at Cassini saturation; the PPN bound
|ξ_χ|(χ₀/M_P) ≲ 2.4×10⁻³) to be compared against DR3/LSST Y10/Euclid; and
that §3.6 contains a **structural result** — the Swampland×NMC shared-
cutoff hypothesis drives |ξ_χ| ≲ 8.4×10⁻¹⁹ at c' = 1/6, sixteen orders of
magnitude tighter than Cassini, forcing one of three explicit model-
building resolutions.

**What ECI is not claiming.** (1) A first-principles derivation of any
axiom from deeper physics. The axioms combine; they are not co-derived.
(2) Any statement about the cosmological validity of Cryptographic
Censorship beyond what is made explicit as a working conjecture in
Appendix A. (3) Any MCMC-level Bayesian preference over ΛCDM. No full
(ξ_χ, α, f_EDE, z_c) posterior has been computed; the paper is framework-
genre, not data-analysis-genre. (4) Any observable NMC signature at
DR2 precision — ECI is explicitly indistinguishable from minimal-coupling
wCDM inside the DR2+DESY5 band. The predictive handle is DR3/LSST Y10.
(5) Any claim of discovery or of tension-resolution via the A3 dictionary;
all §5-style narrative statements (Big Bang as decodability boundary;
inflation as algebraic necessity; Weyl curvature revisited) are quarantined
to Appendix A and explicitly marked (D) as dependent on Eq. (toy-dict).

The predictive core is §3.1–§3.7 plus §4. The speculative layer is
Appendix A (the A3 toy dictionary). Anything that reaches for a claim
beyond this division is out-of-scope for v4.6.

**v4.7 addition (2026-04-22).** A §1.5 "organising reading" is now
\input after §1: the six axioms admit a common observer-dependent reading
in the late-time quasi-dS regime ($\Omega_\Lambda\gtrsim 0.7$), with
A4/A5/A6 re-read as QRF-frame-labelled quantities and A3 as the self-
consistency condition on the subregion where the QRF crossed product of
A1 remains well-defined. The reading is scoped — it does NOT cover the
pre-recombination sector (EDE axion at $z_c\sim 3500$; BBN $\xi_\chi$
bound) — and is explicitly not a derivation. No equation is moved; no
numerical value changes. Frame qualifiers are attached in prose to §3.5
(Cassini bound, solar-system frame), §3.6 (EFT heuristic, causal-diamond
regime), §A6 (Matsubara form, observer ensemble average), and
Appendix A (QRF-subregion link). The Ma--Huang 2024 construction of PRUs
from quantum one-way functions (arXiv:2410.10116, STOC'25) upgrades the
A3 pseudorandomness premise at the CFT level from "effective existence"
to "existence"; the cosmological transposition of A3 remains a working
conjecture quarantined in Appendix A (PRINCIPLES §8).

## Part B — The six axioms, honestly labelled

**A1 — Observer-dependent algebra.** Asserts that each QRF carries a
type-II crossed-product von Neumann algebra (II₁ for static dS,
II_∞ for SdS Killing horizons) and that generalised entropy S_gen[R] =
A/(4G_N) + S_matter is a functor on the QRF category. **Motivation:
established theorem** in the dS static-patch case (CLPW 2023 is a real
theorem; DEHK 2025a,b extend the framework). If A1 is wrong, the paper's
framework narrative loses its anchor but none of §3.1–§3.7 fails: the
phenomenological predictions live at the Lagrangian level of §2 and do
not invoke the algebraic structure beyond declaring it exists.

**A2 — Emergent geometry.** Asserts Einstein equations from Jacobson's
δQ = T_U δS_gen on local Rindler horizons, with the non-perturbative GSL
of Faulkner–Speranza 2024 and Kirklin 2025. **Motivation: established
derivation** in the stationary-horizon case (Jacobson 1995 is textbook);
non-perturbative GSL is **review-stage** for non-stationary FLRW —
Faulkner–Speranza and Kirklin establish it for the regimes relevant to
A1. If A2 is wrong, Lagrangian-level gravity is not threatened; the
thermodynamic-gravity reading of the framework is lost.

**A3 (working conjecture) — Cryptographic Censorship.** Asserts that
holographic CFT states whose boundary-restricted dynamics is ε-approximately
a k-design admit bulk duals containing event horizons. **Motivation:
established theorem in AdS/CFT** (CryptoCensorship reference). Its
cosmological transposition to de Sitter or FLRW horizons is **speculative
bridge**: there is no proven pseudo-Riemannian modular-reconstruction
analogue and no boundary causal-wedge reconstruction theorem outside
AdS. v4.6 isolates the cosmological use of A3 to Appendix A and a single
toy dictionary Eq.(toy-dict). If A3 cosmology is wrong, nothing in the
predictive core is affected: §3.1–§3.7 and §4 stand independently.

**A4 — Two-field scalar sector with non-minimal coupling.** Asserts
a two-field sector: the axion-like EDE field φ with V_φ ∝ [1−cos(φ/f)]³
active at z_c ∼ 3500 (Poulin 2019); the late thawing χ with exponential
V_χ = V₀ exp(−αχ/M_P) and NMC ξ_χ R χ²/2 (Ye 2025, Wolf 2025, Pan–Ye
2026). **Motivation: phenomenological posit** backed by recent peer-
reviewed literature; the NMC coupling is a textbook scalar-tensor
operator (Faraoni 2004). If A4 is wrong — i.e. if no such effective scalar
exists in the universe — the paper's dark-energy phenomenology collapses
but the axiom is precisely the one the data are currently probing.

**A5 — Dark Dimension.** Asserts the species-scale tower cutoff
Λ_sp(H) = M_P (H/M_P)^c' with c' = 1/6 (derived from Montero Eq. 2.2 via
H² ∼ Λ/M_P², verified in V1 §4 to 0.1%), and a mesoscopic extra dimension
ℓ ∈ [0.1, 10] μm with meV-scale KK gravitons as the DM candidate.
**Motivation: review-stage conjecture.** Montero–Vafa–Valenzuela and
AAL 2023 are serious Swampland papers; the phenomenology is tightly
constrained by ACT DR6 (N_eff = 2.86 ± 0.13, Calabrese 2025) and by
fifth-force tests (c' < 0.2). If A5 is wrong in the sense that the tower
exponent is not 1/6, the §3.6 cross-constraint simply moves on the (c', ξ)
plane; the architectural conclusion (A4+A5 need an explicit resolution)
survives for any c' ≳ 0.05.

**A6 — Persistent-homology complexity.** Asserts that PH_k on density
super-level sets is a finer f_NL estimator than Betti numbers, with the
leading-order Matsubara-2003 Euler-characteristic shift Eq.(A6-euler)
serving as the analytical baseline. **Motivation: phenomenological
posit** — the Matsubara form is textbook; the PH_k refinement
(Yip 2024, Calles 2025) is active literature. If A6 is wrong as an
optimal-estimator claim, CMB-S4 / LiteBIRD still sees f_NL through the
standard bispectrum; ECI's Prediction 2 merely loses its sharpest
diagnostic, not its content.

## Part C — The phenomenological predictions

**§3.1 DESI DR2 w₀, wₐ.** NMC thawing χ with ξ_χ ≠ 0 crosses w = −1
without ghost pathology (Barcelo–Visser 2000). DESI DR2 central values
w₀ ≈ −0.752, wₐ ≈ −0.86. ECI NMC band half-width Δwₐ^ECI ≈ 1.1×10⁻² at
χ₀ = M_P/10 using B_num(0.7) = 9.05 from D13; compare σ_{wₐ}^DR2 = 0.215,
i.e. the band is ∼5% of 1σ. Mahalanobis distance to DR2+DESY5 mean under
reconstructed covariance (D10, V2-verified to 0.01σ): ECI 3.29σ,
Scherrer–Sen 3.33σ, ΛCDM 4.36σ. **Verdict: disfavoured but non-
discriminating.** The 3.3σ tension is a joint property of the non-phantom
thawing family; DR2+DESY5 prefers the phantom-crossing region that no
thawing model populates. ECI is not singled out. **Horizon:** DR3
(σ_{wₐ} ∼ 0.07, 2028) and LSST Y10 (σ_{wₐ} ∼ 0.05, 2032) is where the
band width (∼13–22% of 1σ) starts being separable.

**§3.2 H₀ tension (EDE).** f_EDE = 0.09 ± 0.03, H₀ = 71.0 ± 1.1 km/s/Mpc
under ACT DR6 + DESI DR2 + Planck + Pantheon+ (Poulin–Smith 2026 combined
with Calabrese 2025). Residual SH0ES tension ∼2σ. **Verdict: consistent
with current data**; ECI inherits the Poulin–Smith result wholesale.
**Horizon:** SO + SPT-3G D2 at 2027–2028 with forecast σ(f_EDE) ∼ 0.01 —
Prediction 3 falsifier is f_EDE ∉ [0.06, 0.12].

**§3.3 Cosmological constant attractor.** V_χ = V₀ exp(−αχ/M_P) admits an
accelerating quintessence attractor for α < √2; Halliwell 1987 +
Copeland–Liddle–Wands 1998. Reduced-Planck numerics give
ρ_Λ / M_P⁴ ∼ 8×10⁻¹²¹ at χ₀/M_P ∼ 120/α, consistent with the Ooguri–Vafa
Swampland Distance Conjecture. D12 symbolically reproduces w_φ(α=0)=−1,
w_φ(√2)=−1/3, w_φ(√3)=0. **Verdict: consistent.** The α < √2 bound is
standard literature; the only ECI-specific content is its placement as
an axiom-level attractor. **Horizon:** none; this is a consistency check,
not a prediction.

**§3.4 Dark matter (KK).** Dark Dimension KK tower at m ∼ meV, c' = 1/6
primary (c' ≈ 0.05 kept only as a parenthetical de-Sitter-slope
comparison), ISL tests at ℓ ∈ [0.1, 10] μm, Ġ/G = (−5.0 ± 9.6)×10⁻¹⁵ yr⁻¹
from LLR (Biskupek–Müller–Torre 2021). **Verdict: consistent at current
ACT DR6 precision**; N_eff = 2.86 ± 0.13 is compatible with the DD tower.
**Horizon:** Eöt-Wash next-gen ISL deviation in the quoted ℓ window
(Prediction 4, 2028+), KM3NeT + IceCube-Gen2 sub-keV signatures
(Prediction 6, 2028+), and atomic-clock |\dotα/α| < 2×10⁻¹⁹/yr
(Prediction 5, ongoing).

**§3.5 Cassini + NMC Scherrer–Sen.** PPN γ−1 = −4 ξ²χ₀²/M_P² at leading
order (D7; Chiba 1999, Damour–Esposito-Farèse 1993, Wolf 2025
coefficient match). Cassini (Bertotti–Iess–Tortora 2003, |γ−1| ≤
2.3×10⁻⁵) gives |ξ_χ|(χ₀/M_P) ≤ 2.4×10⁻³, i.e. |ξ_χ|_max ≈ 2.4×10⁻² at
χ₀ = M_P/10. The NMC extension of Scherrer–Sen is
wₐ = −A(Ω_Λ)(1+w₀) + B(Ω_Λ) ξ_χ √(1+w₀) (χ₀/M_P) + O(ξ²), with A(0.7) =
1.58, B_num(0.7) = 9.05 ± 1.18 (D13 numerical), B_heur = 7.30 (old
(8/√3)A heuristic; off by ∼25% at Ω_Λ = 0.7, ∼43% at 0.8; flat
∼9 across [0.5, 0.8]). **Verdict: consistent (null-result-pending).
Horizon:** DR3/LSST Y10 (Prediction 1b, 2028–2032).

**§3.6 Swampland × NMC.** Under the shared-cutoff hypothesis (χ is a
bulk mode of the DD sector) the heuristic EFT bound δM_P² ≤ Λ² gives
|ξ_χ|(χ₀/M_P)² ≤ (H₀/M_P)^{2c'}. At c' = 1/6 and χ₀ = M_P/10:
|ξ_χ| ≤ 8.4×10⁻¹⁹ (V1 arithmetic verified to 0.1%). That is sixteen
orders of magnitude tighter than Cassini. Three resolutions are
compatible with the axioms: (i) χ is a 4D zero-mode in a separate sector
— A4, A5 logically independent; (ii) chameleon/symmetron screening
(D15: α_min ≃ 0.095, ρ_c ≃ 1.3×10⁻⁸ g/cm³; the minimum-viable slope
sits just below the Khoury–Weltman 2004 chameleon-viable band α ∈
[1/8, 1/3]); (iii) ξ_χ saturates at ∼10⁻¹⁹ and the NMC DE signature is
lost. **Verdict: structural result (not a data fit).** Paper chooses (i)
as primary; (ii) is the open model-building lane; (iii) is consistent
but phenomenologically empty. **Horizon:** none observational;
discrimination is theoretical (UV-completion choice).

**§3.7 NMC perturbations.** Closed-form sub-horizon quasi-static
observables (D14, BEFPS 2000): G_eff/G_N = 1 + ξ_χ χ²/M_P² + O(ξ²),
η = 1 − 4 ξ² χ²/M_P² + O(ξ³). At Cassini saturation and χ₀ = M_P/10:
|Δf σ₈ / f σ₈| ≤ 0.4%, ΔG_eff at a=1 ∈ [−0.21%, +0.15%], |η−1| ≤
2×10⁻⁴ — all sub-threshold at Euclid / LSST Y10. **Verdict: null-
result at current forecast precision. This is documented as a feature,
not a bug**: the NMC perturbation signature is explicitly below Euclid
reach unless χ₀ ≳ 0.5 M_P or the Cassini bound is breached.

## Part D — The honest weaknesses

The 6/6 peer-reviewer consensus (v1: Claude + Gemini 2.5 Pro + Magistral-
medium; v2: GPT-5.4 + Gemini 3.1 Pro + Grok 4) and the adversarial
reviews V1, V3, V5, V6, V7, V8 landed the following weaknesses. They
are catalogued here so no future agent reintroduces them.

1. **A3 cosmological extension is speculative.** Six of six reviewers
   (unanimous across both v1 and v2 passes) named A3/§5 as the single
   weakest element. v4.5 tried to rescue A3 by adding a toy dictionary;
   v4.6 quarantined §5 to Appendix A "Speculative". Status: contained,
   not fixed.
2. **The EFT bound δM_P² ≤ Λ² is heuristic.** V1 and GPT-5.4 both
   flagged this. The prose now says "heuristic" out loud three times in
   §3.6 (body + Caveat 1); the numerical 10⁻¹⁹ figure should not be
   re-quoted without the heuristic qualifier.
3. **The chameleon screening in §3.6 Resolution (ii) is a
   parametrisation choice.** D15 picks the Θ(ρ) = exp[−(ρ/ρ_c)^α]
   family and reports α_min ≃ 0.095, ρ_c ≃ 1.3×10⁻⁸ g/cm³. The
   α ∈ [1/8, 1/3] band quoted as compatible with Khoury–Weltman 2004
   is itself a parametrisation-dependent comparison. Do not re-quote
   as a "prediction".
4. **The χ₀ scaling is a choice.** χ₀ = M_P/10 used identically in
   §3.5 and §3.6 as the fiducial thawing amplitude. Smaller χ₀ weakens
   the Cassini bound linearly; larger χ₀ tightens it. The fiducial
   is defensible (characteristic thawing excursion in the last e-fold)
   but it is a choice and v4.4 D9 noted a residual χ₀-nonlinearity in
   B_local (14 at χ₀=0.05, 9.5 at χ₀=0.1, 7.3 at χ₀=0.2).
5. **No MCMC.** No (ξ_χ, α, f_EDE, z_c) joint posterior exists. The
   editorial note (§Editorial) states plainly that the publishable
   version in PRD / JCAP requires this work, currently out-of-scope.
6. **No GUDHI/Ripser PH_k forecast.** The A6 axiom is analytically
   anchored in Matsubara 2003 + Yip 2024 + Calles 2025 but no numerical
   PH_k-vs-bispectrum discrimination study exists in this repo. This was
   flagged in v4.0.1 self-audit and is still open.
7. **No RevTeX→svjour3 port.** eci.tex compiles under revtex4-2 targeting
   EPJ C, but the actual svjour3 submission port is not done.
8. **§3.6 figure still marks c' = 0.05 as primary.** A FIGURE-UPDATE-
   PENDING marker has been sitting in section_3_6 since v4.3; the sweep
   is correct but the annotation is not. Non-blocking but should be
   cleaned before submission.
9. **Negative literature claim in §3.5.** The sentence "to our knowledge
   has not appeared in the NMC-thawing literature surveyed" was flagged
   by V8 as hard-to-falsify. Consider softening before submission.
10. **§3.5 figure caption ambiguity.** Table tab:B_of_OmegaL caption
   writes "ξ_χ ∈ {…} × χ_0 ∈ {…}" with `×` read by default as a
   Cartesian product (5×3 = 15 trajectories per Ω_Λ). V8 flagged the
   ambiguity as a NIT. Spelling this out ("grid of 5×3 trajectories")
   is a zero-risk clarity win at submission time.
11. **No per-(Ω_Λ, χ₀) tabulation of B.** D9 observed a χ₀-local
   variation (B_local ≈ 14 at χ₀=0.05, 9.5 at 0.1, 7.3 at 0.2);
   D13's headline table reports B_num(Ω_Λ) only, averaged across the
   χ₀ grid. At the DR3 verdict level this is immaterial, but a 2D
   (Ω_Λ, χ₀) tabulation would be honest if a referee pushes on
   sub-leading χ₀-dependence. D9-report §"Caveat — χ₀ non-linearity"
   documents the choice.
12. **Prediction 5 (|\dot α/α|) is phrased as a prediction but is really
   a limit.** v4.0.1 self-audit caught this; we have not re-worded the
   table since. Low stakes — "ECI-consistent with optical-clock bound"
   is the honest phrasing.
13. **Prediction 7 (r < 10⁻³ axionic) is too generic.** Most slow-roll
   models comply. v4.0.1 self-audit recommended recasting as a
   correlated signature (r, n_s, PH_k). Not done.

## Part E — What we chose NOT to claim

1. **A rigorous pseudo-Riemannian modular-reconstruction proof of the
   A3 cosmological transposition.** All three v2 reviewers (GPT-5.4,
   Gemini 3.1 Pro, Grok 4) demanded this; we declined. Building a
   one-sided modular-reconstruction theorem for an FLRW causal diamond
   without an AdS boundary is a multi-paper program, not a §5
   paragraph. The honest response is quarantine (v4.6 Step 1), not a
   half-baked proof sketch.
2. **A full Matsubara-2003 + Yip-2024 numerical Hermite-coefficient
   calculation for the PH_k Euler-characteristic shift.** D5 is a
   scaffold only. The A6 equation cites the closed form and the PH_k
   refinement; a numerical f_NL-vs-PH_k-signal study on mock catalogues
   is explicitly on the v4.2+ roadmap and has not been executed.
3. **A full CLASS-NMC Boltzmann-code patch.** Gemini CLI (v1 peer) and
   Claude Q4 (v1 self) both asked for a joint (ξ_χ, f_EDE) χ² grid.
   The CLASS patch required is weeks of C coding; it is not in scope
   for a framework paper and is explicitly deferred to the editorial
   note.
4. **A Bayesian model preference of ECI over ΛCDM or wCDM.** We chose
   not to infer from the 3.29σ vs 4.36σ Mahalanobis distances that
   ECI is "preferred". The comparison is between two-dof distances, not
   posterior odds; it would be statistically illiterate to convert one
   to the other without a full likelihood.
5. **Any claim of NMC detection.** §3.7 shows the NMC perturbation
   signature sits below Euclid / LSST Y10 precision at Cassini
   saturation. The honest read is "null-result at forecast precision".

## Part E-bis — Further things we considered and declined

Several specific items came up in peer-v1 and peer-v2 discussion that we
did not incorporate and whose absence is intentional:

- **Joint (ξ_χ, f_EDE, z_c) χ² grid vs DR2 + Pantheon+ + Planck TT/TE/EE.**
  Claude-self Q4 at peer-v1 asked for a 20×20×10 background-only
  Boltzmann grid. This sits between a full MCMC (which is out of scope)
  and the current Mahalanobis calculation (which is all we need for the
  framework-genre claim). Adding a grid without a likelihood promotes
  a goodness-of-fit statement we cannot support at framework level;
  doing it properly requires Cobaya + CLASS + an NMC patch that is not
  written. Declined until the CLASS-NMC patch exists.

- **Einstein-frame mapping of the NMC sector.** The §3.5 linear
  expansion in ξ_χ breaks down near the conformal point ξ = 1/6, where
  an Einstein-frame treatment is required. We flag this in Caveat 2 of
  §3.5; within the Cassini-allowed range |ξ_χ| ≲ 2.4×10⁻² ≪ 1/6 the
  linear expansion is controlled, so we do not lose anything by
  declining to do the Einstein-frame calculation.

- **BBN-level constraint on ξ_χ.** Wolf et al. 2025 quote
  ξ_χ(χ₀/M_P)² ≲ 6×10⁻⁶ from a full DESI DR2 Bayesian analysis, which
  is tighter than our Cassini bound at the fiducial χ₀ = M_P/10 by a
  factor ∼60. We cite Wolf 2025 and reproduce the quadratic PPN
  scaling that sets their bound, but we do not re-fit. The Cassini
  bound we quote is the one we derive; the Wolf bound is the one the
  literature quotes as the consolidated constraint. Both are in the
  prose at §3.5 (eq:gamma_PPN_lead and the Wolf attribution paragraph).

- **A full 3D super-level-set PH_k numerical bench against bispectrum.**
  Flagged in v4.0.1 self-audit as v4.2 scope; has not been executed.
  The A6 axiom stands on the Matsubara 2003 analytical baseline + the
  Yip 2024 / Calles 2025 PH_k refinement, but no quantitative
  discrimination study lives in this repo. Do not claim PH_k
  superiority in prose without a numerical anchor.

## Part F — The editorial target

**EPJ C** (SCOAP3 open access, Springer, framework-section) is the
primary target. **Foundations of Physics** (Springer) is the backup.
PRD and JCAP are explicitly excluded until (and unless) the MCMC of §E.3
is performed: both journals would reject a framework paper without a
full likelihood. The editorial note (eci.tex §Editorial) states this
plainly. The v4.6 tag is the submission-ready snapshot under the
framework-genre reading; submission itself requires the svjour3 port
(weakness §D.7) and a final bib sweep.
