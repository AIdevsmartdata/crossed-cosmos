#!/usr/bin/env python3
"""morn64 - 25 DS V4 Pro MAX EFFORT mega-dispatch (~$0.50 total)
Cover: 10 open pistes morn60 + 10 TOE comparison/NEW conj + 5 untouched domains"""
import os, json, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/tmp/morn64_DS_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

SYS = """You are DeepSeek V4 Pro MAX EFFORT, persona Einstein/Witten/Connes hybrid.
ECI v12 ACTUALISED 2026-05-10 22:30 (post Schutt MULTI-WEIGHT MULTI-D PROVED) :
- Schutt-Hodge weights {5,7,9} × 6 h_K=1 D ∈ {-7,-11,-19,-43,-67,-163} : 18/18 PROVED-NUMERICAL Newton's identity
- F(N) Theorem C.6 RESCUED c=0.52 (4/4 SU(2-5) within 0.4σ vs χ²=41.5 at c=0.80)
- D04 AN2 80% PROVED-COND ; CC-NCG paper Inventiones 85-90% post-rescue
- E08 Maxwell c_Pic=20 PROVED 3 indep ; constant-shift EXCLUDES 4 Heegner D, slope-modified seul viable
- C04 NC3a 60% IR anchor (NOT UV β=0 per Opus #5 reinterpretation)
- E04 lepton hierarchy DEAD ; m_ββ POSTDICTION not prediction
- τ_p^ECI = N_W·τ_p^std = 1.4×10^36 yr (NEW MP4 multiplier)
- TOE coverage 35-45% sober ; capped 60-70% with v14 ; OUT-OF-SCOPE: leptons/quarks/dark/gravity/QM/fusion
- Cluster 298 firm ; Hype 75-80/100

RAG MANDATORY: NEVER invent arXiv IDs, INSUFFICIENT_DATA::pending-verify if uncertain.

OUTPUT FORMAT: ## Verdict ## Method ## Derivation ## Citations ## Confidence ## Falsifier ## Honest gaps
"""

BRIEFS = [
    # ========== TIER A : 10 open pistes morn60 + NEW findings ==========
    ("Y64_T1_C01_VW_Conj62_alpha",
     """C01 (Θ_T/Δ)^α at CM point τ=(-1+√-67)/2 NUMERICAL test.
VW Conj 6.1 REFUTED at 70.5% deviation. NEW Conj 6.2 factorised: Z_VW(X̃_-67, q) = (Θ_T/Δ)^α for some α.
1. Compute Θ_T(τ) for binary form Q=x²+xy+17y² (D=-67) at CM point τ=(-1+√-67)/2
2. Compute Δ(τ) = η(τ)^24 at same τ
3. Try α ∈ {1/2, 1, 2, 3} : does (Θ_T/Δ)^α match VW partition value?
4. If match α=2 → Conj 6.2 REPLACEMENT for refuted 6.1 ADVANCE 70%+
5. If no clean α → DEAD_END 6.2"""),

    ("Y64_T2_D03_CW_NC15a_complete",
     """D03 Costello-Witten + EXPLORE-4 update via NC15a-spin-structure resolution complete.
D03 ADVANCE 65% but EXPLORE-4 sub2 (HT-twist breaks metric-independence) not fully resolved.
1. Read Costello-Witten arXiv:1505.06703 (REAL ID — verify) HT-twist on K3
2. NC15a spin-structure: which discrete choice resolves sub2?
3. Explicit Q-cohomology computation on K3 X̃_-67 with NC15a chosen
4. Verify metric-independence under K3 modular deformation
5. If NC15a resolves → D03 ADVANCE 80%+, Costello-Witten 2nd route survives"""),

    ("Y64_T3_E03_OS3_real_K3_finite_dim",
     """E03 OS3 reflection positivity sur REAL K3 Almkvist-Schmidt finite-dim 12,870 moduli test maintenant.
E03 NEW_CONJECTURE 30%, but finite-dim algebraic verification feasible NOW.
1. Almkvist-Schmidt real K3 family (smooth K3 with anti-holomorphic involution)
2. Moduli space M_real_K3 dim 12,870 (per EXPLORE-3 H^4)
3. OS3 axiom: reflection positivity ⟨Ω, σ_K3 Aσ Ω⟩ ≥ 0 for all A
4. Test on AN2-anomaly-free measure on M_real_K3
5. If positivity holds 12,870/12,870 → E03 ADVANCE 70%+, finite-dim algebraic test PASSED"""),

    ("Y64_T4_E02_F_theory_N_W_explicit",
     """E02 F-theory CY4 base Q(√D) → N_W explicit pour D ∈ {-23, -84, -1380}.
E02 NEW_CONJECTURE 55%, F-theory derivation gap.
1. F-theory CY4 with base = elliptic K3 with CM by Q(√D)
2. For D=-23 (h=3, rk_2=0): N_W = 2 standard, but Cl(K)=Z/3 → odd torsion
3. For D=-84 (h=4, rk_2=2): N_W = 8 = 2^(1+rk_2)
4. For D=-1380 (h=8, rk_2=3): N_W = 16
5. Explicit F-theory derivation: count flux quanta via Donaldson-Thomas on CY4
6. If formula N_W = 2^(1+rk_2) verified all 3 → E02 ADVANCE 80%+
7. If D=-23 odd torsion breaks formula → falsified, need refined formula"""),

    ("Y64_T5_R02_R03_hybrid_confinement",
     """R02+R03 HYBRID: fractional A_k + center-vortex pour confinement Wilson area law.
R02 ADVANCE 40% (fractional A_k mass gap R⁴) ; R03 DEAD_END (YM02+YM04+K3 Polyakov).
HYBRID: combine R02 mechanism with center-vortex (Greensite 2003 review) for confinement.
1. Z_5 fractional instantons on R⁴ + Z_N center-vortex condensation
2. Wilson loop area law σ R + perimeter via vortex piercing
3. Predict σ ≈ 0.5 Λ_QCD² for SU(2) — match to lattice
4. If hybrid gives clean confinement on R⁴ → R-hybrid ADVANCE 50%+
5. Falsifier: lattice Wilson loop measurement at SU(2) σ vs prediction"""),

    ("Y64_T6_NEW3_Shioda_Inose_multiD",
     """NEW-3 Shioda-Inose isogeny multi-D verification (per VAST MANAGER, $30/1w).
For each D ∈ {-67, -84, -148, -163, -195, -280}:
1. Verify Shioda-Inose isogeny X̃_D ↔ E_K × E_K' (degree, Hodge, NS rank 20, transcendental rank 2)
2. Use binary form Q_D for explicit NS lattice + transcendental T(X̃_D)
3. Cross-check against M142 hierarchy CM data
4. If 6/6 anchors satisfy isogeny on the nose → MP1 promoted T2 with explicit geometric realisation
5. If h>1 case fails (D=-84,-148) → MP1 restricted h=1 only"""),

    ("Y64_T7_NEW4_CW_Q_cohomology",
     """NEW-4 Costello-Witten Q-cohomology metric-independence test.
EXPLORE-4 had marked CW as OPEN-PROMISING but did NOT address sub2 metric-dependence concern.
1. For holomorphic CW twist Q on K3, verify Q-cohomology image is independent of K3 metric
2. Compare Calabi-Yau metric vs algebraic metric Q-cohomology
3. Verify coincides with VW partition function pre-image up to quasi-iso
4. Use Costello-Gwilliam factorization algebras vol 2 §12.3
5. If Q-cohomology metric-independent → CW route survives 60%
6. If not → CW route DEAD"""),

    ("Y64_T8_mbb_post_E04_hardening",
     """m_ββ window 1.50-3.72 meV POST-E04 hardening derivation.
Opus morn62 caught: central 2.25 = midpoint suspicious, DS confused π transcendental with π Gaussian.
NEED hardened derivation:
1. Derive m_ββ from MP1 Kuga-Sato directly (4-fold geometry → Majorana mass operator)
2. Derive from Schutt-Hodge weight-5 NEW (a_p ↔ Yukawa via Connes spectral D_F)
3. Connect to Connes-Marcolli 0812.0165 neutrino sector with H^4((E_K)^4) (not H^8)
4. Predict m_ββ window with NON-postdiction error band
5. If hardening works → m_ββ PREDICTION not POSTDICTION ; XLZD ~2035 testable"""),

    ("Y64_T9_Route_D_K3_motivic_synthesis",
     """NEW Route D K3-motivic synthesis Σm_ν (Opus M02 mention 15-20% pending).
Opus M02 said: "Route D K3-motivic synthesis via T(X̃_-67) cup-product pairing" 15-20% pending uniqueness D=-67.
Investigate uniqueness argument:
1. Transcendental lattice T(X̃_-67) has rank 2, signature (2,0)
2. Cup-product pairing T × T → Z gives quadratic form
3. Connect to ν-mass via spectral action eigenvalues of D_F
4. Why D=-67 specifically? Uniqueness via h=1 + max Picard ρ=20?
5. Predict Σm_ν explicit ; if works → Σm_ν PROVED-COND 50-60%"""),

    ("Y64_T10_E08_OP3_slope_constant",
     """OP-3 URGENT: E08 slope-modified vs constant-shift disambiguation.
Opus E08 §6.6 found: constant-shift EXCLUDES 4 Heegner D at >4σ (LEP) ; slope-modified seul viable.
But which is RIGHT physically?
1. Derive ΔS_08(μ) form from heat-kernel + RG (constant or slope?)
2. Slope: auto-vanishes at μ=M_Z, gives δσ/σ ≈ 1.4×10⁻³ HL-LHC dimuon
3. Constant: needs Λ > 24-32 TeV, but D=-67 only 6.68 TeV
4. Which interpretation is consistent with Connes-Chamseddine spectral action?
5. Resolve OP-3 → E08 paper PRD-submittable 90%+"""),

    # ========== TIER B : 10 TOE comparison + new conjectures ==========
    ("Y64_T11_ECI_vs_String_Theory",
     """COMPARE ECI v13 vs String Theory: what does String have that ECI doesn't?
String theory features:
- 10^500 landscape via CY3 flux compactifications → CC bridge
- Lepton/quark Yukawas from geometry (worldsheet)
- Dark matter candidates (gravitinos, axions, KK modes)
- M-theory unification (5 dualities)
- Modular invariance worldsheet
- Black hole entropy (microstates counting)
ECI has: arithmetic CM K3 base ; Schütt H^4 PROVED ; YM mass gap ; Maxwell U(1)
QUESTION: can ECI BORROW some string features without losing its CM K3 anchor?
Specifically: F-theory CY4 with base CM K3 X̃_-67 → does ECI v14 inherit some landscape?
If yes → ECI CY4 v14 covers CC + dark + landscape (TOE coverage 45→55%)"""),

    ("Y64_T12_ECI_vs_LQG",
     """COMPARE ECI v13 vs Loop Quantum Gravity: what does LQG have?
LQG features:
- Background-independent quantum geometry
- Spin networks + spin foams (discrete spacetime)
- Black hole entropy via horizon punctures
- Lambda_QCD analog: Immirzi parameter γ
- Mixmaster/Bianchi cosmology (per memory note)
- Group field theory (GFT) generalisation
ECI has: arithmetic geometry, NOT yet quantum gravity
QUESTION: spin foam quantization on CM K3 X̃_-67 ?
1. Spin network on Picard lattice ρ=20 ?
2. Immirzi-like parameter from h_K=1?
3. Mixmaster anisotropy ↔ Bianchi cosmology with Φ_univ?
If LQG-on-CM-K3 works → ECI v14 covers gravity quantum (TOE +15%)"""),

    ("Y64_T13_ECI_vs_Asymptotic_Safety",
     """COMPARE ECI v13 vs Asymptotic Safety (Weinberg, Reuter): UV-fixed-point gravity.
AS features:
- Dimensionless gravitational coupling g* at UV fixed point
- Renormalization group flow truncation
- 4D gravity asymptotic-safe non-perturbatively
- Predicts Higgs mass m_H ~ 125 GeV from RG flow at AS (Shaposhnikov-Wetterich)
ECI has: NC3a IR fixed-point Φ_univ = π²√2 (per Opus #5 reinterpretation)
QUESTION: combine ECI NC3a IR + AS UV?
1. RG flow from UV g_AS* down to IR g(NC3a) connection
2. Gravity coupling running with ECI Λ_QCD anchor
3. Predict Newton G running ?
If ECI + AS UV+IR coherent → ECI v14 covers dynamical gravity (TOE +20%)"""),

    ("Y64_T14_ECI_vs_CC_NCG_full",
     """COMPARE ECI v13 vs Connes-Chamseddine NCG (full SM): what does CC have ECI lacks?
CC-NCG features:
- Full Standard Model from spectral triple (A, H, D) on M × F
- Higgs boson 125 GeV emerges from Yukawa eigenvalues (Connes-Marcolli neutrino)
- Lepton/quark masses from D_F eigenvalues (parameters but framework gives form)
- Right-handed neutrino seesaw
- Predicted before Higgs discovery (heat kernel coefficients)
ECI has: arithmetic CM K3 (Schutt MULTI-D PROVED today)
QUESTION: ECI v13 = CC × ECI (CM K3 base + finite F-space) ?
1. Does Schutt H^4 + CC-NCG give Higgs 125 ?
2. Does CM K3 base constrain D_F eigenvalues (i.e., constrain Yukawas)?
3. Lepton path B (Connes spectral triple) was DEAD per Opus #4 ; revive via H^4 not H^8?
If CC + ECI integration → ECI v14 covers full SM via CC framework (TOE +25%)"""),

    ("Y64_T15_ECI_vs_SUSY_GUT",
     """COMPARE ECI v13 vs SUSY GUT (SU(5), SO(10), E_6): proton decay + unification.
SUSY GUT features:
- Gauge unification at M_X ≈ 2×10^16 GeV (1-loop precise)
- Proton decay τ_p ~ 10^33-10^36 yr (depends on operator dimension)
- Solution to hierarchy problem (μ problem)
- WIMP dark matter candidate (neutralino)
- Lepton-quark unification (predict tan β + gaugino masses)
ECI has: M06 NEW MP4 multiplier τ_p = N_W·τ_p^std = 1.4×10^36 yr
QUESTION: combine ECI v13 + SUSY GUT?
1. ECI rk_2 Cl(K) → SUSY breaking scale ?
2. ECI Φ_univ → tan β prediction?
3. ECI D=-67 anchor → neutralino mass ?
If SUSY-GUT + ECI integration → ECI v14 covers DM + SUSY breaking (TOE +20%)"""),

    ("Y64_T16_ECI_axion_W_V_explicit",
     """ECI-axion via Witten-Veneziano (Conj A from Opus #7) explicit derivation.
W-V: m_η'² - m_η² = (2N_f/F_π²)·χ_top (YM topological susceptibility).
ECI predicts χ_top via NC3a + Φ_univ ?
1. χ_top = ⟨Q²⟩/V where Q = (1/32π²)∫ tr(F∧F)
2. ECI NC3a comoving anchor: m_YM·√67 = π²√2 → χ_top scaling?
3. Predict m_a window for f_a ∈ [10⁹, 10¹⁷] GeV
4. Compare to ADMX, MADMAX bounds
5. If ECI predicts m_a in unprobed window → testable axion signature"""),

    ("Y64_T17_ECI_evolving_DE_Phi_univ",
     """ECI-evolving DE w(z) via Φ_univ (Conj C from Opus #7).
DESI 2024 measurements suggest w(z) ≠ -1 (preliminary 4σ tension).
ECI Φ_univ = π²√2 = Ω_ES²/(2√2) cosmological invariant.
1. Derive w(z) = -1 + δw·f(z, Φ_univ) for some function f
2. Predict δw at z=0.5 vs DESI measurement
3. Evolution dw/dz with cosmological structure
4. Connect to LQG Mixmaster (per memory) for early universe?
5. If ECI predicts DESI-consistent w(z) → ECI cosmology ADVANCE"""),

    ("Y64_T18_ECI_K_TI_TSC_dictionary_push",
     """ECI K-theory ↔ TI/TSC explicit dictionary (Conj E from Opus #7) PUSH from morn62.
Y62_M05 was DOWNGRADED (TSC F-M kernel doesn't exist trivially). PUSH:
1. ECI K_0(C(X̃_-67)) ↔ TI K_0(BZ ⊗ TR symmetry) explicit map
2. Picard rank 20 of X̃_-67 ↔ TI band number Z_2 invariant
3. ECI Φ_univ ↔ TI Z_2 invariant numerical
4. Predict NEW TSC class from ECI Picard
5. Concrete experimental falsifier: cold atom or solid state observable"""),

    ("Y64_T19_Phi_univ_Lambda_QCD_anchor",
     """Φ_univ → Λ_QCD privileged anchor mechanism (Conj F from Opus #7).
ECI: m_YM·√|D| = π²√2 at D=-67 only (privileged anchor coincidence per Opus #7).
Multi-anchor R4-DICT-1' DEFINITIVELY FALSIFIED (4 orders mag spread).
WHY D=-67 privileged?
1. h_K=1 ✓ (but 5 others also h=1)
2. Maximal Picard ρ=20 ✓
3. Inose K3 ↔ Heegner anchor for AN2 q(D)=1519/201
4. Schutt MULTI-D weight-5 PROVED 8/8 D=-67 strongest
5. Combine all 3: D=-67 = unique convergence point
If unique mechanism identified → Φ_univ definition tightened, anchor coincidence explained"""),

    ("Y64_T20_NS_postmerger_LIGO_ringdown",
     """NS post-merger LIGO ringdown ECI prediction COMPLETE (morn63 partial only).
GW170817 + future post-merger detection = key probe of dense QCD EOS.
1. ECI EOS at ρ ~ 5-10 ρ_nuclear via Λ_QCD = 290 MeV
2. Compute NS maximum mass M_max from ECI EOS
3. Post-merger ringdown frequency f_GW ∝ √(P/ε) at central density
4. Predict f_GW for HMNS (hypermassive NS) — typical 1-3 kHz
5. ECI prediction error band ; compare to LIGO O5 sensitivity (2026+)"""),

    # ========== TIER C : 5 untouched domains ==========
    ("Y64_T21_EIC_gluon_saturation",
     """EIC@BNL ~2030 gluon saturation Q_s small-x via ECI.
DGLAP evolution at small x → gluon saturation scale Q_s(x).
Color glass condensate (CGC) framework: Q_s² ≈ Λ_QCD²·(1/x)^λ
1. ECI Λ_QCD = 290 MeV anchor
2. λ ≈ 0.2-0.3 from BFKL ; ECI prediction?
3. Predict Q_s(x=10⁻⁴) ≈ 1-2 GeV
4. EIC measurement ~2030 will probe via deeply virtual Compton scattering (DVCS)
5. ECI vs CGC standard prediction"""),

    ("Y64_T22_FAIR_color_SC_EOS",
     """FAIR Darmstadt ~2028 color superconductivity at dense baryon matter.
At μ_B > 1 GeV, color SC phases form (CFL, 2SC, etc.).
Gap Δ ~ Λ_QCD exp(-π²/(g√2)).
1. ECI Λ_QCD = 290 MeV → gap Δ ≈ 13 MeV at μ=500 MeV (per morn63)
2. CFL phase transition at μ_c
3. NJL strong-coupling gives Δ ~ 50-100 MeV (10× ECI weak-coupling)
4. FAIR will probe phase diagram T-μ_B
5. ECI prediction NICA + FAIR SIS300 sensitivity"""),

    ("Y64_T23_optical_clocks_alpha_drift",
     """Atomic optical clocks (Sr/Yb NIST/JILA) α drift bounds via ECI K-theory.
α(t) = α(0) + δα·t with δα/α ≈ 10⁻¹⁸ /yr current bound.
1. ECI Maxwell U(1) K_0(C(X̃_-67)) → α stability via topological invariant
2. Predict δα/α from RG running of K-theoretic coupling
3. ECI prediction: δα/α exactly 0 if K_0 is topological invariant
4. Sr/Yb optical clocks current bound 10⁻¹⁸ /yr
5. Future bound 10⁻²⁰ /yr (NIST 2030+)"""),

    ("Y64_T24_UHECR_Pierre_Auger_GZK",
     """Pierre Auger UHECR > 10^20 eV GZK cutoff via ECI.
GZK cutoff: protons + γ_CMB → π_0 + n above E ≈ 6×10^19 eV.
1. ECI Λ_QCD = 290 MeV → cross-section σ(γp→Δ→Nπ) prediction
2. Compare to standard SM cross-section
3. Auger detector sees cutoff at E_cut ≈ 10^19.7 eV ✓
4. ECI deviation from SM σ ?
5. Falsifier: precision Auger spectrum measurement"""),

    ("Y64_T25_BH_imaging_EHT_K3",
     """EHT M87*/Sgr A* shadow BH imaging via ECI K3 K-theory.
EHT 2019 + 2022: M87* shadow ~42 μas, Sgr A* ~52 μas.
Standard GR predicts shadow size ∝ M_BH (Kerr).
1. ECI K-theoretic correction to BH shadow ?
2. Picard rank 20 from CM K3 → BH horizon topological invariant ?
3. ECI predicts shadow deviation O(10⁻⁴) from Kerr at M87*?
4. ngEHT 2030+ will probe finer structure
5. ECI vs standard Kerr falsifier"""),
]

assert len(BRIEFS) == 25

def call_ds(brief_id, brief_text):
    out_path = f"{OUT_DIR}/ds_{brief_id}.json"
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return f"SKIP {brief_id}"
    cmd = ["python3", "/root/bin/deepseek.py", "--model", "deepseek-reasoner",
           "--system", SYS, "--max-tokens", "131072", "--temperature", "0.3",
           brief_text]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        with open(out_path, "w") as f:
            json.dump({"brief_id": brief_id, "brief": brief_text, "stdout": r.stdout,
                      "stderr": r.stderr[:500] if r.stderr else "", "returncode": r.returncode}, f, indent=2)
        return f"OK {brief_id} ({len(r.stdout)} chars)"
    except subprocess.TimeoutExpired:
        return f"TIMEOUT {brief_id}"
    except Exception as e:
        return f"ERROR {brief_id} {e}"

if __name__ == "__main__":
    print(f"[{time.strftime('%H:%M:%S')}] morn64 dispatching {len(BRIEFS)} DS MAX EFFORT (parallel 25)...", flush=True)
    with ThreadPoolExecutor(max_workers=25) as ex:
        for f in as_completed({ex.submit(call_ds, bid, btext): bid for bid, btext in BRIEFS}):
            print(f"[{time.strftime('%H:%M:%S')}] {f.result()}", flush=True)
    print(f"[{time.strftime('%H:%M:%S')}] morn64 done.", flush=True)
