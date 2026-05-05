# ECI / crossed-cosmos — Opus 4.7 Meta-Synthesis (Mid-Day 2026-05-05)

**Author:** Opus 4.7 (1M context), meta-synthesis agent
**Project owner:** Kévin Remondière (ORCID 0009-0008-2443-7166, GitHub `AIdevsmartdata`)
**Anchor version:** ECI v6.0.53.1 (GitHub `8ef001f`, Zenodo DOI `10.5281/zenodo.20034969`)
**Hallu counter:** **77** (last increment was A3 catching the Opus V2-Cor "exact zero" over-claim earlier today)
**Anti-hallucination posture:** every arXiv ID below was already cross-checked in a prior live agent (A1/A2/A5/A6/A8/W1/W4 today, plus the strategic synthesis stack). **No new arXiv ID is introduced** in this document. Mistral large-latest **STRICT-BANNED** for citations; OK only for code-level cross-check.

**Tags:**
SOLID = referee-defensible mathematical content; STRUCTURAL = framework-organising; PHENOMENOLOGICAL = ranking analysis; NULL = no signal beyond prior; CONJECTURED = explicitly tagged as such; OPEN = active gate; CLOSED = definitively refuted.

---

## §1 — Executive Vision (one page)

### What ECI / crossed-cosmos *is* in one sentence

ECI is a research programme that takes the Witten/CLPW/DEHK type-II∞ crossed product as the algebraic skeleton of generally-covariant QFT-with-observer, and asks whether the same algebraic data — modular flow, KMS at β=2π, Bisognano-Wichmann, the past-light-cone diamond — can simultaneously (a) **organise** the modular flavour Yukawa landscape (S′₄ at the CM point τ = i, anchored by the LMFDB CM newform 4.5.b.a), (b) **reproduce** Cardy density ρ = c/12 in 2D CFTs and its Hawking analogue in BEC, and (c) sit as a structurally-motivated **Cassini-clean wedge** of the wider scalar-tensor / NMC quintessence landscape (Wolf 2025, Karam-Palatini, ΛCDM).

### What it *isn't*

- It is **not** a particle-physics prediction engine. After A5's K-specificity downgrade, after the V2 no-go for strict τ = i in the quark sector, after the H7-Damerell-CS refutation at half-integer s = k/2, after the Opus V2-cor "exact 0" hallucination today (hallu 77), **zero** SM observable is currently a clean PREDICTION (zero data input).
- It is **not** a Nobel-cosmology contender. Levier #1B + C4 v5 OVERNIGHT triply confirmed ξ_χ ≈ 0 NULL at Cassini; ECI does **not** beat ΛCDM in cosmological log-Bayes; it sits in a structurally-motivated wedge alongside Wolf's ξ = 2.31 and Karam-Palatini.
- It is **not** the (∞,2)-functor U conjecture of the v7 manifesto: that was REFUTED by Krylov 2π × rational MTC incompatibility.
- It is **not** an end-to-end ToE; the framework provably defers numerical values to additional structure (Theorem 1, structure-vs-values gap, KFLS-corroborated).

### What success looks like at 6 / 12 / 24-month horizon

**6 months — math-physics consolidation (achievable with current resources, ~80% probability).**
- 4-5 of the 8 standalone papers in pre-print: P-NT (BLMS-ready), Cardy ρ = c/12 (LMP-ready), V2 no-go (JHEP letter), v7.4 amendment (LMP), Modular Shadow (LMP); plus the AWCH Bianchi IX with Lemma A.1 (CMP). All bulletproofed against the post-A1/A3/A5 retraction discipline.
- Zenodo + GitHub trail intact, ORCID established, first community engagement (Nägerl outreach, Schäfer-Nameki SymTFT scoping, IHES-via-Marcolli letter).
- A8 G1.14 joint MCMC verdict on two-tau pre-registered. G1.12 SU(5) RGE+off-diag work committed.

**12 months — Foundational Prize-grade contribution if any of three doors close.**
- (a) G1.12.B SU(5) 5_H + 45_H modular RGE closure produces a parameter-free proton-decay partial-width prediction Hyper-K/DUNE can hit by ~2030.
- (b) ER=EPR Week 4 spectrum-matching E_n^chord = E_n(K_R) closes at semi-classical order, lifting A6's Case B from 50% conditional theorem to v6.2 S2 publication.
- (c) Modular Shadow conjecture proves on a finite-rank type-II∞ truncation (M4 in strategic synthesis), giving the first operator-algebraic identification of the MSS chaos bound λ_L ≤ 2π T/ℏ with Krylov modular complexity.

**24 months — Foundational Prize / Breakthrough Prize ambition only.**
- Realistic ceiling: a **mathematical-physics** contribution (modular shadow + Cardy + LMFDB/S′₄) recognised as the canonical algebraic-foundational layer for the modular-flavour and crossed-product-algebra literatures. **Not** a Nobel-cosmology scenario (ξ_χ NULL is locked in).
- Foundational Prize is an honest aspiration if Hurwitz/Bernoulli K=Q(i) "thin coincidence" + BIX Lemma A.1 + V2 no-go + Modular Shadow form a coherent package.

---

## §2 — Open Doors (with evidence + next gate)

Each door: **claim — evidence so far — next concrete gate (cost+ETA) — failure mode.**

### O1. v7.4 CM-anchored ATTRACTOR (W1 + A8)
- **Claim.** S′₄ modular flavour with τ_lepton near i (not strict), with ECI's CM-by-Q(i) anchor for 4.5.b.a as the algebraic motivation; v7.3 → v7.4 rewords τ = i from "fixed point" to "attractor basin."
- **Evidence.** W1 (PC overnight): single-τ scan over 7 fermion observables finds basin at τ* = −0.1897 + 1.0034 i with χ²/dof = 1.05; LYD20 published best fit was at τ = −0.21 + 1.52i (factor ≈3 farther from i). A8 G1.14 joint NUTS MCMC pre-registered: VIABLE iff χ²_min < 30 AND P(|τ_l − i| < 0.3) > 0.5 AND P(|τ_q − i| < 0.3) > 0.5. **Currently RUNNING on PC GPU PID 201729; ETA 30-60 min.**
- **Next gate.** Wait for A8 verdict (today). If VIABLE, draft v7.4 amendment (already drafted as `V74_AMENDMENT/v74_amendment.tex`, 672 lines, LMP target) with W1 + A8 numerics integrated. If MARGINAL or REFUTED, downgrade v7.4 paper to "two-modulus precedented (Tanimoto-Yamamoto 2209.08796, Ding 2212.10666); ECI's distinguishing contribution is the Q(i) CM anchor for τ_lepton."
- **Failure mode.** A8 χ² > 50 → two-tau picture itself fails on this observable set; v7.4 anchor degrades to **mathematical-only** (4.5.b.a identification stands; physics interpretation paused).

### O2. G1.12 SU(5) 5_H + 45_H tree-OPEN (A2 verified)
- **Claim.** The +19.5% gap between LYD20 H3 GUT-scale ratio (y_c/y_t = 2.725×10⁻³) and SM 2-loop Wang-Zhang target (3.256×10⁻³) is closeable in non-SUSY SU(5) with 5_H + 45_H Georgi-Jarlskog mechanism.
- **Evidence.** A2 (today): 31×31×31 = 29 791-point 3D scan with closed-form δr/r = 8(ξη)² L_45 − 4(ξη) L_5. Best closure: M_T₄₅ = 3.16×10¹⁴ GeV, ξ = 0.640, η = 1.132 → δr/r = +19.498% (residual <0.01 pp). 292 natural-region points (ξ ≤ 1, η ≤ 1) hit ≥+19.5%. Per-paper anchors: Patel-Shukla 2310.16563, Antusch-Spinrath 0804.0717, Wang-Zhang 2510.01312 (all live-verified).
- **Next gate.** **G1.12.B** — model-build the 45_H modular f^{ij} matrix in LYD20 Model VI at τ = i, replace the diagonal `threshold_correction_ratio` with full 3×3 matrix, re-run with off-diagonal Y_u from LYD20. **3-6 months**, sub-agent campaign. Cost: 0$ (local CPU); time: weeks of modular model-building + days of compute.
- **Failure mode.** Off-diagonal couplings re-introduce the 19.5% gap (currently absorbed in the natural region by ξ, η free) → G1.12 collapses to fit, not prediction; alternatively the 45_H Yukawa pattern is incompatible with τ = i CM constraint → reverts to two-tau quark sector with τ_q ≠ i.

### O3. H7-A integer-point Damerell ladder (A1 standard literature; A5 K-specific)
- **Claim.** L(f, m) · π^(4−m) / Ω_K⁴ ∈ {1/10, 1/12, 1/24, 1/60} for 4.5.b.a at integer m ∈ {1,2,3,4}; α₂ = 1/12 = ρ_Cardy(c=1) is one parameter-free hit; α₃ = 1/24 is its Γ-shadow forced by Γ(3)/Γ(2) = 2 (NOT independent).
- **Evidence.** A1 lit-check (today): H_4 = 1/10 is the **lemniscatic Hurwitz number** (Hurwitz 1899 Math. Ann. 51), α₂ = 1/12 = B_2/2 is the Bernoulli half-value transported to Q(i) via Chowla-Selberg (Chowla-Selberg 1949; Damerell 1971; Shimura 1976 Comm. Pure Appl. Math. 29; Harder-Schappacher 1986 Springer LNM 1399). Standard literature; the ladder itself is NOT new mathematics. A5 cross-K test (today): α₂ = 1/12 holds **only** for K = Q(i); for K = Q(√−2/−3/−7/−11) the period-free invariant 12·α₂·√|D_K| produces K-specific Bernoulli-Hurwitz rationals (9/5, 4/5, 64/35, 18/11 vs 2 for Q(i)). DOWNGRADE: thin coincidence + Γ-shadow, **not** universal CM↔CFT identity.
- **Next gate.** v7.4 amendment paper §3 already adopts the A5 wording (downgrade from "two parameter-free Cardy hits" to "one K=Q(i)-anchored thin coincidence + Γ-shadow"). LMP submission as soon as A8 returns.
- **Failure mode.** Hostile reviewer rejects the "thin coincidence" framing as not novel enough → fall back to **mathematical-only** P-NT paper (LMFDB IDs as the standalone math.NT contribution; v7.4 amendment becomes a follow-up note).

### O4. ER=EPR Week 3 modular-rigidified Stinespring partial (A6)
- **Claim.** Constructed C_BS = "modular-rigidified Stinespring isometric embedding" V: H_HPS → H_DEHK with chord vacuum |0⟩ → analytic vector |ξ_n⟩ in the natural positive cone of (M_R, σ); P1 (state-matching), P2 (modular flow intertwining), P3 (Connes-cocycle equivariance) all hold semi-classically. Uses CMPT 2306.14732 universal modular Lyapunov 2π + HOPSW 2510.13986 chord ↔ bulk dictionary.
- **Evidence.** A6 (today): explicit construction at semi-classical 1/N → 0 order; FH-II (Faulkner-Hollands 2010.05513) provides the type-changing recovery channel R_BS even though source is type-I (HPS chord) and target is type-II∞ (DEHK crossed product). Updated A/B/C probabilities: 25/50/25 (was 20/45/35; mass shifted C → B).
- **Next gate.** **Week 4 (A6 hand-off):** verify spectrum-matching E_n^chord = E_n(K_R) using HOPSW arXiv:2510.13986 + HPS arXiv:2412.17785 + DEHK arXiv:2412.15502 + Vardian arXiv:2602.02675 sections 2-4 each. If positive → **Case B becomes a theorem at v6.2 S2 publication standard**, ER=EPR Araki paper publishable. ~2 weeks of careful read + 1 finite-q DSSYK numerical truncation on PC.
- **Failure mode.** Spectrum mismatch → C_BS only formal, no operator-algebraic theorem; falls back to "consistency note" status (MVT2-class deliverable).
- **Catch noted (hallu 77 protective):** A6 caught **two mis-attributions in my brief**: arXiv:2412.15502 = de Vuyst-Eccles-Hoehn-Kirklin (NOT de Boer-Engelhardt-Hertog-Kar); arXiv:1610.02038 = Couch-Fischler-Nguyen (NOT Jefferson-Myers). These are **brief-internal**, not Opus fabrications, but propagating them would have been an 8th catch this 24h. Acronym DEHK is OK but the names attached to 2412.15502 must be corrected in any follow-up.

### O5. Cosmopower NMC emulator (real Klein-Gordon backend pending)
- **Claim.** A proper NMC emulator with full Klein-Gordon scalar-field backend (not closed-form w(z)) gives correct H₀ for ECI-NMC posterior (currently artefactually low at H₀ ≈ 64-65 in C4 v5 OVERNIGHT due to closed-form approximation).
- **Evidence.** C4 v5 OVERNIGHT (eve 2026-05-04, 12 min, 5-model joint GPU MCMC): ECI_NMC ξ NULL Cassini-clean reconfirmed (Levier #1B verrouillé). All NMC variants give H₀ ≈ 64-65 (artefact of closed-form). JAX named_shape patch + cosmopower-jax 0.5.5 give 386 cp predictions/s on RTX 5060 Ti — pipeline ready.
- **Next gate.** **~1-2h GPU on PC** to write & test cosmopower NMC emulator with proper Klein-Gordon backend. Run C4 v6 with 11 models including Karam-Palatini.
- **Failure mode.** H₀ stays low even with proper backend → ECI-NMC has internal H₀ tension; either (i) ECI must invoke the bifurcated EDE+late-NMC scenario (Bella-Poulin-Vagnozzi-Knox 2604.13535) or (ii) accept that the Cassini-clean wedge sits at H₀ ≈ 64-65 (incompatible with SH0ES, compatible with Planck-only) and the NMC sector cannot resolve H₀ tension.

### O6. 8-9 standalone papers in pipeline
- **Status as of 2026-05-05 noon:**
  | # | Paper | Status | Target | Anchor evidence |
  |---|-------|--------|--------|-----------------|
  | 1 | P-NT "Two LMFDB IDs for hatted weight-5 S′₄ multiplets" | BLMS-ready (POLISH_REPORT done; 9-10pp) | Bull. Lond. Math. Soc. | LMFDB live-verified for both 4.5.b.a and 16.5.c.a, root number +1 corrected, NPP20/LYD20/dMVP26 bib fixed |
  | 2 | Cardy ρ = c/12 (incl. para-fermion ρ_p,k) | LMP-ready (5 CFTs verified to 4 digits + para-fermion to 10⁻²⁰) | LMP / J. Phys. A | PC2 D-series result pending; Solnyshkov 2017 + Steinhauer 2021 DOIs to verify |
  | 3 | V2 no-go τ=i Cabibbo | Drafted (487 lines, A3 Cor 3.4 retracted today) | JHEP letter / PRD comment | sin θ_C ≤ 0.005 sympy + MC; convention-independent; A3 caught the V2-cor over-claim before propagation |
  | 4 | Modular Shadow LMP | Drafted (`MODULAR_SHADOW/modular_shadow_LMP.tex`) | LMP | FS24 + CMPT verified; now M4 in strategic synthesis |
  | 5 | AWCH Bianchi IX with Lemma A.1 | Closure note done (Lemma A.1 measure-zero crossings, 6/6 sympy PASS) | CMP | Kato + Heinzle-Uggla anchors verified |
  | 6 | P-KS microlocal sheaves and PH_k | Drafted | Geom. Top. | Kashiwara-Schapira 2018 Thm 1.4 + Berkouk-Ginot 2018 |
  | 7 | P-DSSYK FRW Krylov diamond | Drafted | LMP | Heller-Papalini-Schuhmann + Caputa-Magán-Patramanis-Tonni |
  | 8 | ER=EPR Araki dS_gen/dτ_R = ⟨K_R⟩_ρ | A13_2 memo + tex skeleton; Week 3 partial bridge | LMP | Araki 1976 + Pusz-Woronowicz 1978 + DEHK 2412.15502 + A6 modular-rigidified Stinespring |
  | 9 | v7.4 amendment LMP | Drafted (672 lines) | LMP | A1 standard literature confirms ladder; A5 K-specificity downgrade applied |
- **Next gate.** Submit P-NT first (highest leverage per strategic synthesis §7), then Cardy + V2 in parallel; v7.4 amendment after A8 verdict.
- **Failure mode.** Single-author submission load is real; reviewer push-back on "thin coincidence" framing for v7.4 likely. Mitigation: anchor each paper on its own SOLID core (LMFDB IDs, Cardy 5-line proof, V2 no-go) and treat the modular-flavour interpretation as an explicitly tagged speculation in §6 of each paper.

### O7. Modular Shadow as math-ph theorem (M4 in strategic synthesis)
- **Claim.** The §sec:mss-shadow identification S_gen ↔ Krylov modular complexity is provable as a math-ph theorem on a finite-rank truncation of the type-II∞ crossed product.
- **Evidence.** Combines FS24 modular GSL + CMPT modular Krylov universality + Heller-Papalini-Schuhmann 2412.17785 chord algebra. WORKING-CONJECTURE explicitly tagged in eci.tex §sec:mss-shadow; no published work has explicitly identified the saturation slope with the MSS chaos bound via Krylov modular complexity.
- **Next gate.** 4-6 weeks math-ph note, target LMP. Could be done in parallel with M5 (two-τ verification) since both are at ≤4-week scale.
- **Failure mode.** Counter-example exists where finite-rank type-II∞ algebra fails the identification → result publishable as anti-result.

### O8. Bianchi VIII Hadamard SLE construction (M1 in strategic synthesis)
- **Claim.** Explicit Hadamard SLE construction on Bianchi VIII closes the 9-Bianchi-types AWCH table cleanly (currently rigorous-pending-Hadamard).
- **Evidence.** Template = Banerjee-Niedermaier 2305.11388 for Bianchi I + the Olver-style WKB lemma being written for Bianchi V matter. Bianchi VIII structure group is non-compact with 4-dim isometry group; explicit SLE not in literature.
- **Next gate.** 4-6 weeks of WKB/SLE construction. Yield: closes 9-type programme; converts thm:T2BVIII from "rigorous pending Hadamard" to "rigorous."
- **Failure mode.** No SLE construction exists → publishable obstruction theorem identifying which Bianchi VIII features block the SLE. Both outcomes math-ph publishable.

### O9. Quantum cryptography ↔ type-II crossed product (X1 in strategic synthesis)
- **Claim.** A non-trivial QKD interpretation of DEHK QRF-functorial type II → type II transitions exists; the algebra type changes when Alice and Bob's QRF differs, and the modular Hamiltonian / secret-sharing entropy changes accordingly.
- **Evidence.** SPECULATIVE; ECI's Cryptographic Censorship axiom (A3 in eci.tex §1) draws on Akers-Bouland-Chen-Ozols 2023 but the QKD angle is genuinely unexplored.
- **Next gate.** 4-week scoping memo; output: VIABLE / WEAK / DEAD-END verdict on whether QKD security under DEHK functorial transformations is non-trivial.
- **Failure mode.** Most likely WEAK BRIDGE; if DEAD-END, parked permanently. Highest-EV genuinely-new direction in the project per strategic synthesis §3.2.4.
- **CAVEAT (per project memory):** the previous "Wave 5" verdict said type-II is on the wrong side of Tsirelson for ECI ↔ standard QKD direct linking; if so, this door is structurally CLOSED, not OPEN. **I cannot independently verify the Tsirelson claim from the W5 directory** (W5 is empty in the current notes tree). Flagging as **need to verify W5 status before pursuing X1**.

### O10. Innsbruck Cs-133 ρ_p,k=2 = 1/18 outreach (P1 in strategic synthesis)
- **Claim.** ECI predicts ρ_p,k=2 = 1/18 for parastatistics order 2; falsifier is any measured ρ outside [4%, 7%].
- **Evidence.** Innsbruck Cs-133 anyonization Nature 642, 53 (2025), DOI 10.1038/s41586-025-09016-9, arXiv:2412.21131 platform exists; the Nature paper measured 1D anyonic correlations from spin-charge separation, NOT direct ρ_p,k. Adjacent platform, dedicated follow-up needed.
- **Next gate.** Send A5 protocol design doc to Hanns-Christoph Nägerl after P-NT in pre-print. 24-36 month timeline to data.
- **Failure mode.** Innsbruck not interested → polariton 1/12 Steinhauer 2019 G^(2) re-extraction (P2 fallback).

### O11. SymTFT (Schäfer-Nameki) ↔ S′₄ Hecke closure (X2 in strategic synthesis)
- **Claim.** The H_1 = {T(p) : p ≡ 1 mod 4} sub-algebra closure on S′₄ metaplectic forms admits a SymTFT (Freed-Moore-Teleman 2024, Gaitsgory-Raskin 2024) reformulation.
- **Evidence.** SPECULATIVE structural bridge; H_1 closure is an algebraic corollary of the χ_4 nebentypus (proven in S2 of strategic synthesis), and SymTFT is the correct abstract home for residual symmetry on the type-II crossed product.
- **Next gate.** 4-month scoping study with Sakura Schäfer-Nameki (Oxford), but only AFTER P-NT in pre-print as calling card.
- **Failure mode.** No bridge → parked as math-physics open problem; H_1 closure stays as algebraic-corollary statement in P-NT.

---

## §3 — Closed Doors (definitive refutations)

These doors do **not** re-open without genuinely new published external input.

### C1. Strict τ = i for both quark and lepton sectors (V2 no-go theorem, multi-path RGE)
- **Refutation.** V2 audit (2026-05-04 evening) — convention-independent group-theoretic forcing of d^c, s^c row collinearity in M_d → sin θ_C ≤ 0.005 (vs PDG 0.2253), factor ≈45 below experiment. Now reinforced by W1 attractor finding (the χ² minimum is at τ ≠ i, not at τ = i). Two-tau picture is the only escape (Tanimoto-Yamamoto 2209.08796, Ding 2212.10666 precedent).
- **Closure rigour.** DEFINITIVE. Convention-independent. **Do NOT re-open.**

### C2. Cosmology Nobel scenario (ξ_χ NULL at Cassini, triply confirmed)
- **Refutation.** Levier #1B → C4 v5 OVERNIGHT → C4 v5 (5-model joint GPU MCMC eve 2026-05-04). ξ_χ ≈ 0 NULL is Cassini-enforced; ECI does not beat ΛCDM in cosmology.
- **Closure rigour.** DEFINITIVE for the **Nobel-cosmology** framing. The Cassini-clean wedge interpretation (P1 in strategic synthesis) survives but is NOT a Nobel-class result. **Do NOT re-frame as Nobel-cosmology.**

### C3. Quantum crypto ↔ ECI direct linking (W5 STATEMENT IN BRIEF)
- **Refutation.** Per the brief: type-II crossed product is on the **wrong side of Tsirelson** for direct QKD coupling.
- **Closure rigour.** **CANNOT INDEPENDENTLY VERIFY** in this session — W5 directory is empty in the notes tree. Treating this as **provisionally CLOSED** per the brief but flagging as needing verification before O9 (the SPECULATIVE crypto open door) is pursued. If the W5 verdict is solid, X1 collapses to DEAD-END.

### C4. EHT ↔ ECI (W3: no length scale)
- **Refutation.** W3 (2026-05-04): ECI introduces no dimensional length scale that could enter the photon sphere radius; ρ_p,k is dimensionless. EHT resolution ≈ 10% of shadow size; Planck-scale correction ≈ 10⁻⁴⁰ (39 orders of magnitude apart). The closest literature (FS24, DEHK 2412.15502, Liu 2026 = arXiv:2601.07915 = Chandrasekaran-Flanagan) confirms zero EHT-testable predictions from any algebraic-type-II BH paper.
- **Closure rigour.** DEFINITIVE structurally. **Re-opens only if** ECI ever produces a concrete metric ansatz with a new length parameter.

### C5. Riemann/CCM ↔ ECI (P-RIE: structural mismatch)
- **Refutation.** P-RIE memo (2026-05-04): CCM 2025 (Connes-Consani-Moscovici, "Zeta Spectral Triples", arXiv:2511.22755) has **no modular flow / KMS / Tomita-Takesaki structure** to connect to ECI's H2; ECI's H_σ is underdetermined; Bost-Connes is type III (ECI is type II). All three are structurally incompatible.
- **Closure rigour.** DEFINITIVE for the v6.0.x §sec:limits item 9(h) "Riemann modular zeta" speculation. **Do NOT re-open.** Re-opens only if (a) explicit H_σ computation for the ECI diamond crossed product appears, or (b) Weil quadratic form Q_W of CCM 2025 is shown to be a modular Hamiltonian. Neither exists.

### C6. H7 strict Damerell-CS at s = k/2 (G1.15: out of algebraicity domain for k = 5 odd)
- **Refutation.** G1.15 audit (2026-05-04, Zenodo `10.5281/zenodo.20030684`): the half-integer s = k/2 = 5/2 lies **outside** the Damerell/Shimura/Deligne archimedean algebraicity domain for odd weight k = 5. The original H7 axiom of v7.3 was over-claimed.
- **Closure rigour.** DEFINITIVE. v7.4 amendment replaces it with H7-A (integer-point Damerell ladder, A1 verified standard literature) + H7-C (BDP anti-cyclotomic p-adic L-values for the central point if needed).

### C7. A3 V2 Cor 3.4 "exactly 0" (hallu 77, today)
- **Refutation.** A3 (2026-05-05 morning): Opus drafted a corollary to V2 paper claiming the cosines between the c^c-row and t^c-row of LYD20 Model VI M_u at τ = i are exactly 0. A3 verified at mp.dps = 80: |cos| = 5.5×10⁻⁵ (NOT structural zero); Groebner reduction modulo Y_1²+2Y_2Y_3 = 0 gives a non-zero residual sextic polynomial. **Caught BEFORE V2 paper propagation.** Hallu count incremented from 76 to 77; V2 paper unchanged (the no-go rests on M_d {d,s}-block alone, which is solid).
- **Closure rigour.** DEFINITIVE for the corollary. The V2 no-go itself is unaffected.

### C8. "Two parameter-free Cardy hits" (A5 K=Q(i)-specific downgrade)
- **Refutation.** A5 cross-K test (today): α₂ = 1/12 holds **only** for K = Q(i); the period-free invariant 12·α₂·√|D_K| = 9/5, 4/5, 64/35, 18/11 vs 2 for Q(i) for the analogous CM weight-5 newforms over Q(√−2/−3/−7/−11). The "two hits" are not universal CM↔CFT; they are one K=Q(i)-anchored thin coincidence + one Γ-functional-equation shadow (α₃ = α₂/2 forced).
- **Closure rigour.** DEFINITIVE downgrade. v7.4 amendment paper §3 already adopts the wording.

### C9. v6.0.10 (b) firewall PBH C_jump (rock-solid prior closure)
- **Refutation.** Three fatal issues + Bisognano-Wichmann universality.
- **Closure rigour.** STRUCTURALLY CLOSED. **Do NOT re-open.**

### C10. v6.0.10 (c) Bell signed I_σ (KRLP monotonicity)
- **Refutation.** Klein-Ruskai-Lieb-Petz monotonicity argument is structural; SGB target I_σ < 0 has no AQFT realisation.
- **Closure rigour.** STRUCTURALLY CLOSED. **Do NOT re-open.**

### C11. v7 manifesto (∞,2)-functor U conjecture (Krylov 2π × rational MTC)
- **Refutation.** Parker et al. PRX 9 041017 Krylov 2π saturation incompatible with rational MTC target (Rabinovici JHEP 03 (2022) 211 has b_n → b_∞ < ∞).
- **Closure rigour.** REFUTED in current form. Reformulation possible (non-semisimple MTC, 6-9 months + math.CT co-author) but **do not pursue from this project's resources**; suggest Schäfer-Nameki-style outreach via SymTFT bridge X2.

### C12. v6.0.48 PIVOT VIABLE m_c/m_t prediction
- **Refutation.** G1.8/9/10/11 + I1.5/2/3/6 + V1-V4: the "13% off PDG" claim was a y_t(M_GUT) cherry-pick at y_t = 1.0 (IR fixed-point regime); honest 1-loop result is −18.9%; 2-loop calibrated to Wang-Zhang within 0.3% gives essentially the same result. Retracted in v6.0.49.
- **Closure rigour.** DEFINITIVE. The 16% intrinsic gap at GUT scale is the OPEN G1.12 SU(5) door (O2 above), not a free parameter to dial.

### C13. "ECI v7 ToE" framing (suspended pending KMS-Maass / GUT / two-τ predictions)
- **Refutation.** Strategic synthesis explicitly suspended this framing pending parameter-free retrodiction at <5% precision from at least one of {KMS↔Maass-form bridge, GUT threshold derivation, two-τ picture}.
- **Closure rigour.** SUSPENDED, not refuted. Re-opens iff one of the three closes (G1.12.B is the most concrete candidate).

---

## §4 — Linkage to Current Physics Models

For each framework: (a) how ECI connects, (b) what it adds, (c) what it doesn't address. Honesty over enthusiasm.

### 4.1 ΛCDM cosmology (Planck PR4 + DESI DR2/DR3 + Pantheon+ + KiDS-Legacy + ACT DR6)
- **Connection.** ECI's NMC sector is a deformation of ΛCDM with one extra coupling ξ_χ; at ξ_χ = 0 it reduces to ΛCDM exactly.
- **What ECI adds.** A structurally-motivated *wedge* — the Cassini-clean limit |ξ_χ|·(χ_0/M_P)² ≲ 6×10⁻⁶ — anchored in operator-algebra (type II∞ crossed product on the past-light-cone diamond), not in phenomenology. Provides the "no-screening control" of the NMC parameter space.
- **What ECI doesn't address.** H₀ tension (ECI is neutral; current H₀ ≈ 64-65 in C4 v5 OVERNIGHT is closed-form artefact pending the cosmopower-NMC backend O5). S₈ tension (KiDS-Legacy 0.73σ from Planck — essentially dissolved post-2025; ECI is neutral). Σmν, JWST z>10 — neutral.
- **Verdict.** PHENOMENOLOGICAL contribution; not a unique winner; correctly positioned as a "Cassini-clean wedge" in the C4 10-model joint MCMC.

### 4.2 Wolf 2025 NMC quintessence ξ = 2.31 (PRL 135 081001, arXiv:2504.07679)
- **Connection.** ECI's ξ_χ ≈ 0 (Cassini-enforced) and Wolf's ξ = 2.31 (large coupling, requires Vainshtein screening) sit at *mutually exclusive* posterior peaks of the same scalar-tensor parameter space.
- **What ECI adds vs Wolf.** Algebraic foundation (CLPW + DEHK + FS) for the small-ξ wedge; Wolf has no such foundation, but Wolf has a far stronger observational signal (log B = +7.34 vs ΛCDM, vs ECI's −1.37 slight ΛCDM preference).
- **Complement, not competitor.** Reframing: Wolf is the screened-large-ξ wedge; ECI is the unscreened-small-ξ wedge; Karam-Palatini (arXiv:2510.14941, log B = +5.52) is the metric-affine wedge that interpolates. C4 v5 OVERNIGHT confirms all four are structurally distinct points.
- **Verdict.** Honest reframing established eve 2026-05-04; no Nobel-class collision.

### 4.3 Karam-Palatini scalar-tensor (arXiv:2510.14941)
- **Connection.** Palatini formulation of NMC analytically suppresses Cassini fifth-force constraints (Ricci tensor algebraic, scalar field doesn't propagate on solar-system scales).
- **What ECI adds.** A potential bridge between Wolf's large-ξ regime and ECI's Cassini-clean wedge: in the Palatini formulation, ξ = 2.31 could in principle survive Cassini without Vainshtein screening.
- **Concrete next step.** Recast ECI's NMC sector in Palatini formulation; include as 11th model in C4 production MCMC.
- **Verdict.** Open phenomenological piste; high EV per strategic synthesis.

### 4.4 Modular flavour (Feruglio 2017 → NPP20 → LYD20 → dMVP26)
- **Connection.** ECI provides an algebraic motivation (CM by Q(i) via 4.5.b.a) for choosing τ_lepton at or near the S-fixed point τ = i. The LMFDB identifications S2 (3̂,2(5) ≡ 4.5.b.a, 2̂(5) ≡ 16.5.c.a) and the H_1 = {T(p) : p ≡ 1 mod 4} sub-algebra closure are genuinely new contributions to the modular-flavour literature.
- **What ECI adds (post A1+A5 nuance).** Two genuinely new observations:
  1. The hatted weight-5 multiplets of S′₄ are *classical* CM newforms in disguise (4-path verified).
  2. The H_1 sub-algebra closure is an algebraic corollary of χ_4 nebentypus — first explicit observation in the metaplectic flavour literature.
- **What ECI doesn't add (honest).** It does **not** improve the numerical fit over LYD20 / dMVP26. The "Hecke-locked Yukawa retrodiction" of v7.0 was refuted (885% error for m_e/m_μ in Test B). The thin Hurwitz/Bernoulli K=Q(i) coincidence is **organisational**, not predictive.
- **Verdict.** ECI is a **fit reorganizer** in the modular-flavour space, NOT a prediction engine. The mathematical contribution (LMFDB IDs + H_1 closure) is publishable independently of ECI physics framing.

### 4.5 SU(5) GUT (Georgi-Glashow + Georgi-Jarlskog 5_H + 45_H) — A2 G1.12 OPEN at tree
- **Connection.** A2 (today) confirms the +19.5% gap between LYD20 H3 GUT-scale ratio and SM 2-loop is closeable in non-SUSY SU(5) with 5_H + 45_H, at natural-region (ξ, η ≤ 1) for M_T₄₅ across [10¹², 10¹⁵] GeV.
- **What ECI adds.** A potential predictive handle: if G1.12.B closes (3-6 months), the model produces a parameter-free proton-decay partial-width prediction that Hyper-K / DUNE will test by ~2030.
- **What ECI doesn't address (yet).** The 45_H modular f^{ij} matrix in LYD20 Model VI at τ = i is not yet model-built; off-diagonal Y_u not done; KSTTT S_3 SU(5) and dMVP26 S′₄ Hecke closure verifications still open.
- **Verdict.** OPEN at TREE. Highest-EV particle-physics gate next 6 months. If it closes → first parameter-free prediction in the modular-flavour pillar.

### 4.6 ER=EPR (Maldacena-Susskind 2013, HPS, DEHK)
- **Connection.** A6 Week 3 (today): explicit semi-classical Stinespring isometric embedding C_BS: H_HPS → H_DEHK with state matching, modular flow intertwining, Connes-cocycle equivariance via CMPT modular Berry rigidification. Type-changing recovery channel R_BS via FH-II.
- **What ECI adds.** A concrete operator-algebraic bridge between type-I DSSYK chord algebra and type-II∞ DEHK crossed product, partially resolving Obstruction O2'.
- **What ECI doesn't address (yet).** Spectrum-matching E_n^chord = E_n(K_R) at semi-classical order (Week 4); 1/N corrections (full quantum gravity); non-perturbative gravitational dressing of observer clock.
- **Verdict.** Partially OPEN. If Week 4 closes, ER=EPR Araki paper is publishable at v6.2 S2 standard.

### 4.7 AdS/CFT modular flow (CLPW 2022, JLMS, Bisognano-Wichmann)
- **Connection.** ECI's algebraic foundation IS the CLPW + DEHK type-II crossed product applied to past-light-cone diamonds; Bisognano-Wichmann β = 2π is the postulated KMS state.
- **What ECI adds.** The §sec:mss-shadow conjecture (T2 in strategic synthesis): ECI saturation slope (1/S_gen)dS_gen/dτ|_sat = 2π T_H/ℏ identical to MSS chaos bound λ_L ≤ 2π T/ℏ via Faulkner-Speranza-Witten S_gen ↔ Krylov modular complexity identification. Genuinely novel framing.
- **What ECI doesn't address.** The connection is at the level of bound-saturation, not metric deformation; M4 (4-6 weeks) would convert the conjecture to a math-ph theorem on a finite-rank truncation.
- **Verdict.** STRUCTURAL contribution. Modular Shadow paper is the LMP target.

### 4.8 Kashiwara-Schapira microlocal sheaves (P-KS paper)
- **Connection.** Kashiwara-Schapira 2018 Theorem 1.4 + Berkouk-Ginot 2018: for tame f, sub-level constructible sheaf F_t has dim H^k(F_t) = PH_k Betti.
- **What ECI adds.** Removes one of ECI's standing axioms (PH_k as "motivated, not derived" per eci.tex §sec:limits item 5) by deriving it from BFV functoriality.
- **What ECI doesn't address.** No new physical prediction; this is a methodological cleanup.
- **Verdict.** P-KS paper drafted; target Geom. Top.

### 4.9 DSSYK / sine-dilaton (Lin-Stanford, HOPSW)
- **Connection.** Heller-Papalini-Schuhmann (PRL 135 151602, arXiv:2412.17785) establish the chord algebra; HOPSW (arXiv:2510.13986) maps chord length L̂ to extremal timelike volumes in dS at semi-classical order. CMPT (arXiv:2306.14732) gives the universal modular Lyapunov 2π that rigidifies the Berry connection.
- **What ECI adds.** The Krylov-complexity-as-observable interpretation of ECI saturation; the modular-rigidified Stinespring channel C_BS partially bridges chord algebra (type-I) to DEHK crossed product (type-II∞).
- **What ECI doesn't address.** The full b_n = πn + O(log n) Lanczos linear growth in the type-II∞ FRW setting is not yet computed analytically; this is a 4-6 week task per strategic synthesis §3.4.3.
- **Verdict.** P-DSSYK FRW paper drafted.

### 4.10 Cardy modular invariance (Cardy 1986 Nucl. Phys. B270 186-204)
- **Connection.** ECI's BEC-analogue prediction ρ = c/12 is exact for full [0,∞) integral via 5-line Euler-Mercator + Cardy proof; para-fermion extension ρ_p,k = k/(12(k+1)) verified to 10⁻²⁰.
- **What ECI adds.** First curated inventory of three falsifiable lab platforms (BEC analogue Hawking, polariton condensates, Innsbruck Cs-133 anyonization) with quantitative predictions per Cardy ρ.
- **What ECI doesn't address.** The c = 7/10 (tricritical Ising) and c = 4/5 (Potts) values do NOT cleanly hit the integer Damerell ladder; these are open per v7.4 amendment §6.
- **Verdict.** Cardy paper LMP-ready (PC2 D-series result pending).

### 4.11 Bianchi IX (AWCH classification)
- **Connection.** ECI's AWCH (Algebraic Weyl Curvature Hypothesis) — past Big Bang inductive-limit algebra has no Hadamard cyclic-separating vector — is now covered for all 9 Bianchi types with sharp conditional-vs-rigorous labels.
- **What ECI adds.** Lemma A.1 (BIX_CLOSURE, today): eigenvalue crossings of M_j(t) on BKL attractor have Lebesgue measure zero (Kato + Heinzle-Uggla 2009 + sympy 6/6 PASS). Closes `rem:Hadamard-BIX-gap`.
- **What ECI doesn't address.** Full unconditional Hadamard SLE on Bianchi VIII (M1 in strategic synthesis, 4-6 weeks).
- **Verdict.** AWCH Bianchi IX paper with Lemma A.1 ready for CMP submission.

---

## §5 — Strategic Priorities Next 3 / 6 / 12 Months

Ranking by **Expected Value of Information × Probability of Success** (EV ratio, qualitative high/medium/low).

### Next 3 months (priority queue, EV-ranked)

| # | Action | Cost | Time | P(succ) | EV | Rationale |
|---|--------|------|------|---------|----|-----------|
| 1 | **Submit P-NT** ("Two LMFDB IDs for hatted weight-5 S′₄") to BLMS / Math. Res. Lett. | $0 (drafted) | 1 week | 95% | **HIGH** | Bulletproof; survives every audit; calling card for all subsequent outreach (§7 of strategic synthesis) |
| 2 | **Submit Cardy ρ = c/12 paper** to LMP / J. Phys. A | $0 + PC2 D-series ($0) | 2 weeks | 90% | HIGH | Standalone math-ph; para-fermion result is genuinely novel |
| 3 | **Submit V2 no-go** to JHEP letter / PRD comment | $0 (drafted, A3 corollary retracted) | 1 week | 85% | HIGH | Convention-independent group-theoretic result; counter-result to dMVP26/NPP20/LYD20 lineage |
| 4 | **Wait for A8 G1.14 verdict + submit v7.4 amendment** to LMP | $0 (running on PC GPU) | 1 week post-A8 | 70% (verdict-dependent) | HIGH | If VIABLE, anchors entire v7.4 axiom system; if MARGINAL, falls back to math-only LMFDB IDs |
| 5 | **Write & test cosmopower-NMC backend** with proper Klein-Gordon | $0 (PC GPU) | 1-2 days | 90% | MEDIUM-HIGH | Unblocks H₀ artefact; rerun C4 v6 with 11 models including Karam-Palatini |
| 6 | **Bianchi VIII Hadamard SLE construction** (M1) | $0 | 4-6 weeks | 60% | MEDIUM | Closes 9-Bianchi-types AWCH cleanly; either way publishable |
| 7 | **ER=EPR Week 4 spectrum-match** (HOPSW + HPS + DEHK + Vardian §§) | $0 | 2 weeks | 50% (per A6) | MEDIUM-HIGH | If positive, Case B becomes theorem at v6.2 S2 publication standard |
| 8 | **Modular Shadow as math-ph theorem** (M4) | $0 | 4-6 weeks | 65% | MEDIUM | LMP-class novel framing |
| 9 | **Two-τ picture verification** (M5; complementary to A8) | $0 | 2-4 weeks | 75% | MEDIUM | Verifies V2 no-go is τ-pair-independent |
| 10 | **AWCH Bianchi IX with Lemma A.1** to CMP | $0 (drafted) | 1 week | 90% | MEDIUM | Most mature companion paper; ready when math-ph queue allows |

### Next 6 months

11. **G1.12.B SU(5) modular RGE + off-diag Y_u** — 3-6 months sub-agent campaign on modular f^{ij} matrix; if closes → parameter-free proton-decay prediction. **HIGHEST single-shot EV** for a particle-physics deliverable.
12. **C4 v6 11-model joint MCMC on Vast.ai (~$551)** — only after #5 completes; pre-registered design doc in `compute/C4_joint_mcmc/preregistration/`. Adds Karam-Palatini, double-axion EDE.
13. **ER=EPR Araki dS_gen/dτ_R = ⟨K_R⟩_ρ paper** — submit to LMP after Week 4 closes; explicit FH-II type-changing recovery bound.
14. **P-KS Microlocal sheaves and PH_k** (M3) — submit to Geom. Top.; closes one ECI standing axiom.
15. **P-DSSYK FRW Krylov diamond paper** — Lett. Math. Phys.
16. **Outreach: Nägerl (Innsbruck) + Schäfer-Nameki (Oxford SymTFT) + Marcolli (IHES bridge to Connes)** — only after pre-prints land.

### Next 12 months

17. **Either G1.12.B closes (proton-decay prediction) OR alternative bridge mechanism for modular-flavour predictivity emerges** — if neither, the "v7 ToE" suspension stays in place; ECI is a math-physics framework, not a particle-physics prediction engine.
18. **C4 v6 production results** — establishes ECI's Cassini-clean wedge interpretation in the published literature.
19. **First conference talk** (GR24, GR25, or modular-symmetry workshop) on the LMFDB / S′₄ / H_1 closure result + V2 no-go.
20. **BIX VIII Hadamard SLE published** OR documented obstruction (M1 outcome).
21. **Quantum-crypto X1 scoping memo** — ONLY if W5 Tsirelson verdict can be independently reverified. If Tsirelson side-blocking is solid, X1 stays DEAD-END.

### Resource envelope

- **First 3 months: $0-100** (verification compute) + author's time. PC GPU sufficient for all MCMC at this scale.
- **Months 3-6: ~$551 Vast.ai for C4 v6 production** + ~$50 Sonnet sub-agents for verification queue.
- **Months 6-12: depends on G1.12.B trajectory.** If RGE work needs Vast.ai for SU(5) RGE running with full off-diagonal modular f^{ij}, ~$200-500.

---

## §6 — Honest Framing

### What we know solidly
- **Mathematical contributions** (publishable independent of ECI physics framing):
  - LMFDB IDs 4.5.b.a (CM by Q(i)) and 16.5.c.a (level 16, χ_4) for the hatted weight-5 multiplets of S′₄ (4-path + 11-prime verified, root number +1 corrected).
  - H_1 = {T(p) : p ≡ 1 mod 4} sub-algebra closure on hatted multiplets (algebraic corollary of χ_4 nebentypus).
  - V2 no-go: at strict τ = i in LYD20 Model VI, sin θ_C ≤ 0.005 (factor ≈45 below PDG).
  - Bianchi IX Lemma A.1: eigenvalue crossings of M_j(t) on BKL attractor have measure zero (Kato + Heinzle-Uggla; sympy 6/6 PASS).
  - Cardy ρ = c/12 universality for unitary diagonal-MIP CFTs (5-line proof; 4 CFTs verified to 4 digits).
  - Para-fermion ρ_p,k = k/(12(k+1)) (Mercator-Euler; verified to 10⁻²⁰).
  - Hurwitz H_4 = 1/10 + Bernoulli B_2/2 = 1/12 standard literature anchors for 4.5.b.a algebraic L-values at integer critical points (A1 today).
- **Hallu discipline**: 8 catches in last 24h; running counter at 77 (was 76 yesterday morning, +1 today from A3 catching the V2-cor over-claim, plus several brief-internal mis-attributions caught and *not* incremented). The 3-strikes rule + Mistral-strict-ban + arXiv-API-live-verify protocol is empirically working.
- **GPU pipeline**: JAX named_shape patch + cosmopower-jax 0.5.5 + RTX 5060 Ti at 386 cp predictions/s. Local infrastructure is sufficient for all near-term MCMC at this scale.

### What we suspect but haven't proved
- **G1.12.B RGE-level closure** — A2 today shows tree-level OPEN with closure at natural-region (ξ, η ≤ 1) for M_T₄₅ across [10¹², 10¹⁵] GeV; full off-diagonal Y_u with 45_H modular f^{ij} matrix is 3-6 months out. Probability of clean closure: ~40-60%.
- **Single-modulus τ ≈ i predictive** — W1 says VIABLE at χ²/dof = 1.05; A8 G1.14 joint MCMC will pre-registered settle today. If MARGINAL, two-modulus picture is necessary (precedented by 2209.08796, 2212.10666 but introduces 2 free moduli).
- **Modular Shadow conjecture** — published in eci.tex §sec:mss-shadow as WORKING-CONJECTURE; M4 finite-rank truncation theorem 4-6 weeks away.
- **ER=EPR semi-classical theorem** — A6 Week 4 spectrum-match is the binary gate.

### What's wishful thinking we should drop
- **"Two parameter-free Cardy hits"** — A5 K-specific downgrade demands this be re-worded throughout. Already corrected in v7.4 amendment paper §3, but any remaining v6.0.x prose mentioning "two independent CM↔CFT identities" should be retracted.
- **"ECI predicts m_c/m_t to 1.5%"** — the v6.0.48 PIVOT VIABLE claim was retracted in v6.0.49. Any residual references in companion notes or social-media drafts need to be retracted.
- **"V2 paper Cor 3.4 exact orthogonality"** — caught today (hallu 77); A3 closed the door before V2 paper propagation. V2 paper unchanged.
- **"ECI predicts a Nobel-cosmology signal"** — Cassini ξ_χ NULL is triply-confirmed. Drop any framing that suggests cosmology is the prize axis.
- **"v7 (∞,2)-functor U as the unification target"** — REFUTED. Any residual v7-manifesto prose should be archived not published.
- **"MCC/CCF brand"** — RETIRED per project memory. Do NOT publish under that brand.
- **"Krylov complexity ↔ rational MTC"** — REFUTED (Parker × Rabinovici incompatibility). Any rational-MTC target language should be replaced with non-semisimple language or dropped.

---

## §7 — Risks

### R1. Disconnect / data loss (low risk, well-mitigated)
- **Mitigation in place:** GitHub commits per major wave; Zenodo deposit per release (v6.0.53.1 → DOI `10.5281/zenodo.20034969` published today via direct API). PC GPU runs use absolute paths + `setsid nohup` per `feedback_disconnection_resilience`. Tailscale shield re-applied via `sudo bash /home/remondiere/pc_calcs/tailscale_shield.sh` after PC reboot.
- **Residual risk:** A8 G1.14 MCMC is currently running on PC GPU; if SSH drops mid-run, results recoverable from `g114_joint_mcmc_chain.npz` on PC.

### R2. Hallucination resurgence (medium risk, monitored)
- **Status:** 8 catches in last 24h (A3 V2-cor + A1 OEIS A001675 erratum + A6 brief-internal name mis-attributions ×2 + plus ~4 prior catches yesterday). Discipline is holding.
- **Mitigation:** Mistral large-latest STRICT-BAN; every new arXiv ID via live API verification; sub-agent cross-check before manuscript propagation; LLM-cited references re-verified against CrossRef/arXiv-API.
- **Residual risk:** A new "convenient reference" pattern from a non-Mistral LLM could slip through. The empirically-validated protective practice (3-strikes rule per claim, ~$5 of verification compute per published claim) should be the standard going forward.

### R3. Reviewer push-back on "thin coincidence" framing (medium risk)
- **Status:** v7.4 amendment paper § Abstract explicitly downgrades "two parameter-free Cardy hits" to "one K=Q(i)-anchored thin coincidence + Γ-shadow." A5 has done the work.
- **Mitigation:** Anchor each paper on its own SOLID core; the LMFDB IDs (P-NT) and Cardy 5-line proof and V2 no-go are bulletproof and don't depend on the thin-coincidence framing. The thin-coincidence is the *bridge* in v7.4 amendment, but if rejected the standalone math contributions survive.
- **Residual risk:** Hostile referee on v7.4 amendment could request retraction of "Bernoulli-anchored" claim; fall-back is to make it a "numerical observation with explicit K-specificity caveat."

### R4. G1.12.B 3-6 month timeline could slip (medium-high risk)
- **Status:** A2 confirms tree-level OPEN; the 45_H modular f^{ij} matrix is the bottleneck.
- **Mitigation:** G1.12.B can be sub-agent-distributed (one agent per LYD20 model or per modular form transcription); milestones at weeks 4, 8, 12 to detect slip early.
- **Residual risk:** If G1.12.B slips beyond 6 months and no other parameter-free prediction emerges, the "v7 ToE" suspension stays in place permanently → ECI is locked as math-physics-only.

### R5. Single-author submission load (high risk)
- **Status:** 8-9 papers in pipeline, single author (Kévin solo modulo Opus/Sonnet drafting assistance).
- **Mitigation:** Stagger submissions (P-NT first, then Cardy + V2 in parallel, then v7.4 amendment, then AWCH BIX). Use Zenodo for DOI persistence between revisions. Don't try to land all 8 in 3 months; 2-3 per quarter is realistic.
- **Residual risk:** Reviewer turn-around on math-ph papers can be 6-12 months; some of these may not appear in print until 2027.

### R6. Cosmology backend artefact in C4 v5 OVERNIGHT (low risk, fixable)
- **Status:** All NMC variants give H₀ ≈ 64-65 in C4 v5 OVERNIGHT; this is closed-form approximation artefact, not a real ECI prediction.
- **Mitigation:** O5 cosmopower-NMC emulator with proper Klein-Gordon (~1-2h GPU) is in queue.
- **Residual risk:** None for the published papers (which haven't claimed H₀); residual risk is reputational if someone screenshots the C4 v5 OVERNIGHT log without context.

### R7. W5 Tsirelson verdict not independently verified (medium risk for X1)
- **Status:** W5 directory is empty in the notes tree as of this synthesis. The brief states type-II is on the wrong side of Tsirelson for ECI ↔ standard QKD; cannot independently verify.
- **Mitigation:** Before pursuing X1 quantum-crypto scoping memo (4 weeks), reverify W5 status. If solid → X1 is DEAD-END (do not pursue). If unverified → 1-day W5-redo first, then decide.

### R8. Brief-internal mis-attributions (low risk, vigilance discipline)
- **Status:** A6 caught 2 mis-attributions in my Week 3 brief (DEHK author confusion + Jefferson-Myers vs Couch-Fischler-Nguyen ID confusion). These were NOT Opus fabrications, but they *would* have propagated had A6 not flagged them.
- **Mitigation:** Brief-writing discipline: any author-name + arXiv-ID pair must be re-verified at the brief-write step, not just at the agent-execute step. Add "brief-internal mis-attribution" to the failure-mode catalog.

---

## CONCISE SUMMARY (for parent agent — under 400 words)

ECI v6.0.53.1 (Zenodo `10.5281/zenodo.20034969`, GitHub `8ef001f`, hallu 77 after A3 catch today) sits at a clean inflection point. The framework's mathematical core is genuinely defensible: (i) LMFDB identifications 4.5.b.a (CM by Q(i)) and 16.5.c.a for hatted weight-5 S′₄ multiplets, 4-path verified; (ii) H_1 = {T(p) : p ≡ 1 mod 4} sub-algebra closure; (iii) V2 no-go τ = i for LYD20 Model VI Cabibbo (sin θ_C ≤ 0.005); (iv) Bianchi IX Lemma A.1 (eigenvalue crossings measure zero, sympy 6/6); (v) Cardy ρ = c/12 + para-fermion ρ_p,k. The physics interpretation is now honestly downgraded: A1 confirms Damerell ladder (1/10, 1/12, 1/24, 1/60) is standard literature (Hurwitz 1899 + Chowla-Selberg + Damerell + Shimura + Harder-Schappacher), and A5 shows α_2 = 1/12 holds **only** for K = Q(i) — one thin coincidence + one Γ-shadow, not two universal CM↔CFT hits. W1 reframes τ = i from "fixed point" to "ATTRACTOR" (basin at τ* = −0.19 + 1.00i with χ²/dof = 1.05); A8 G1.14 joint MCMC is currently RUNNING on PC GPU PID 201729 to settle the two-tau hypothesis.

Open doors with concrete next gates: (1) v7.4 amendment LMP submission post-A8; (2) G1.12 SU(5) 5_H + 45_H — A2 confirms tree-OPEN with closure at natural-region (ξ, η ≤ 1) for M_T₄₅ ∈ [10¹², 10¹⁵] GeV, G1.12.B modular RGE work is 3-6 months and the highest-EV particle-physics gate; (3) ER=EPR Week 3 modular-rigidified Stinespring partial (A6, A/B/C = 25/50/25, Week 4 spectrum-match decisive); (4) cosmopower-NMC backend (~1-2h GPU); (5) 8-paper pipeline (P-NT BLMS-ready, Cardy LMP-ready, V2 JHEP letter, V74 amendment LMP, BIX A.1 CMP, P-KS Geom. Top., P-DSSYK LMP, ER=EPR Araki LMP).

Closed doors: strict τ = i (V2), cosmology Nobel (ξ_χ NULL Cassini), EHT (no length scale), Riemann/CCM (structural mismatch), H7 strict Damerell-CS at half-integer (G1.15), V2 Cor 3.4 "exact zero" (today's hallu 77), "two parameter-free Cardy hits" (A5 K-specific), v7 (∞,2)-functor U (Krylov × rational MTC).

Strategic posture: math-physics consolidation (6 mo) → Foundational Prize aspiration only (24 mo). **Nobel cosmology RULED OUT.** Honest ceiling for 2026: 4-5 standalone math-ph papers + Cassini-clean wedge interpretation + algebraic-foundational layer for modular-flavour and crossed-product literatures.
