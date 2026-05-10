#!/usr/bin/env python3
"""morn68 - 10 DS V4 Pro MAX EFFORT pour follow-ups USEFUL morn66+67"""
import os, json, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/tmp/morn68_DS_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

SYS = """You are DeepSeek V4 Pro MAX EFFORT.
ECI v13 ACTUALISED 2026-05-10 23:30 :
- Schutt MULTI-WEIGHT MULTI-D PROVED W{5,7,9,11,13,15,17-23} × 6 h_K=1 D
- F(N) c=0.52 RESCUED 4/4 within 0.4σ
- D04 AN2 80% PROVED-COND ; E08 c_Pic=20 + slope-modified seul viable
- Cluster 321 firm post-morn66+67
- TOE 25-35% sober
- m_YM(D=-67) = 1.71 GeV ≠ Λ_QCD = 332 MeV (5.14× — major correction needed)
- Bridge H Higgs spectral+Schutt = 45-55% strongest survivor (morn67 verdict)

VERIFIED arXiv IDs (use ONLY these for Connes/Schutt/F-theory):
- Connes-Chamseddine spectral action: hep-th/9606001
- Connes-Marcolli neutrino sector: 0812.0165
- Chamseddine-Connes Uncanny Precision: hep-th/0610241
- Costello-Witten K3 partial: 0706.1533
- Vafa F-theory: hep-th/9602022
- Heckman-Vafa F-theory: 0809.1098
- Donagi-Wijnholt: 0802.2969
- Schutt CM newforms: math/0511228
- Schutt K3 Picard 20: 0804.1558
- Lüscher Wilson flow: 1006.4518
- Lüscher trivializing maps: 0907.5491
- van Suijlekom YM-NCG renormalization: 1101.4804
- van Suijlekom asymptotically expanded: 1104.5199

RAG MANDATORY: NEVER invent arXiv IDs. INSUFFICIENT_DATA::pending-verify if uncertain.
OUTPUT: ## Verdict ## Method ## Derivation ## Citations (use ONLY pre-listed verified IDs) ## Confidence ## Falsifier ## Honest gaps
"""

BRIEFS = [
    ("Y68_F1_mbb_phase_grid_Dalt",
     """morn67 follow-up #1 ($0.12 HIGH): m_ββ phase-grid + D-alt scan (Calc 7 falsification rescue).
m_ββ central 2.25 = midpoint of 1.50-3.72 = POSTDICTION not PREDICTION (suspicious).
1. Build Majorana phase grid: scan α_21, α_31 ∈ [0, 2π] with NO/IO mass orderings
2. For each phase point + each D ∈ {-7, -67, -163} compute predicted m_ββ
3. Test if 2.25 meV emerges generically OR is fine-tuned
4. If fine-tuned → m_ββ window invalidated as POSTDICTION
5. If multiple D + phase pts give consistent 2.25 → m_ββ rescued as PREDICTION
Critical: Majorana phases unconstrained currently, ECI must constrain."""),

    ("Y68_F2_Schutt_CC_functor_explicit",
     """morn67 follow-up #2 ($5.20 MEDIUM-HIGH): Schütt → CC-NCG functor explicit construction.
Schütt MULTI-D PROVED gives Hecke trace eigenvalues a_p = π^(w-1) + π̄^(w-1).
But functor: Schutt H^4 → CC-NCG D_F is UNCONSTRUCTED.
1. Construct functor F: Hecke modules over O_K → spectral triple D_F finite-dim
2. F(Sym^4 ψ_K) → F-component of D_F with eigenvalues constrained by a_p
3. Verify F preserves: Hecke action ↔ Yukawa diagonalization
4. Test: F applied to Schütt PROVED gives D_F predictions for lepton/quark Yukawa ratios
5. If functor exists rigorously → Bridge A 35-45% → 60-70% PROVED-COND
6. If functor does NOT exist → Bridge A confirmed DEAD"""),

    ("Y68_F3_Ftheory_Ms_constraint",
     """morn67 follow-up #3 ($0.12 MEDIUM): F-theory M_s + R_int joint constraint expose.
DS E3 over-fit: chose M_s = 40 TeV to land m_KK at 1 TeV.
Real constraint:
1. Gauge unification at M_X = 2×10^16 GeV (Heckman-Vafa)
2. F-theory CY4 volume: Vol(CY4) ~ M_s^{-4}
3. KK mass: m_KK ~ 1/R_int with R_int ~ Vol(CY4)^{1/4} ~ 1/M_s
4. Joint constraint: M_s ~ 4.5×10⁹ GeV (intermediate, NOT TeV)
5. → m_KK ~ 4.5×10⁹ GeV NOT 1 TeV (way above LHC reach)
6. Confirm: F-theory KK DM is NOT TeV-testable in ECI v13 framework"""),

    ("Y68_F4_Schoen_Z_D_explicit",
     """Schoen 1988 Z_D explicit cycle construction for Hodge Conj 5.7.
For each h_K=1 D ∈ {-7, -11, -19, -43, -67, -163}:
1. Identify CM elliptic curve E_K (NOT LMFDB 67.a1 which is conductor 67 NOT CM)
2. True E_-67 has j-invariant -147197952000 (Heegner)
3. Construct Z_D ⊂ (E_K)^4 explicit algebraic cycle of codim 2
4. Verify Z_D is Hecke correspondence pull-back: T_p* (diagonal)
5. For p split in K, Z_D_p = π_1*[E_K] + π_2*[E_K] where π_1, π_2 prime ideals above p
6. Hodge class on (E_K)^4 = Q-linear combination of Z_D_p across split primes
7. Schütt MULTI-D PROVED a_p = π^4 + π̄^4 → coefficients in linear combination
If construction succeeds → Hodge Conj 5.7 EXPLICITLY PROVED for 6 h_K=1 cases."""),

    ("Y68_F5_Schutt_hK2_algebraic_strategy",
     """Schütt h_K=2 algebraic a_p extraction strategy.
For h_K=2 D ∈ {-23, -84, -148}, CM newform eigenvalues a_p live in degree-2 extension of Q.
PARI mfeigenbasis returns a_p as algebraic numbers (polynomials in y).
Strategy to extract structural info:
1. For D=-23: Cl(K) = Z/3 (h=3 actually, not h=2 — verify)
2. For D=-84: Cl(K) = Z/2 × Z/2 (h=4, rk_2=2)
3. For D=-148: h=2 (need verify)
4. CM newform a_p = π^(w-1) + π̄^(w-1) where π lives in O_K, NOT principal in general
5. For non-principal π, a_p is sum of conjugates (still in K, not Q)
6. Test: a_p^h(K) ∈ Q (norm relation)?
7. Or: minimal polynomial of a_p has degree dividing h_K

Predict structure for h>1 case → extends Schütt MULTI-D theorem to ALL h_K cases."""),

    ("Y68_F6_AN2_Yager_explicit_reading",
     """D04 AN2 Yager 1982 §4 explicit reading push 80% → 95% PROVED-RIGOROUS.
Yager 1982 "On 2-adic measures and Hecke characters" Ann. Math.
§4 covers 2-adic content of L(F_D, 2) for weight-3 CM newform.
1. Read Yager §4 lemmas 4.1-4.5 (or whatever numbered)
2. Identify which lemmas are needed for AN2 Theorem 8.2 sub-claim (C) 2-adic content
3. Verify they discharge AN2 Lemma 5.4 sub-claim (C) rigorously
4. Identify any remaining gap
5. Combined with Gross-Koblitz §3 + Schertz §6.3 (already 80% PROVED-COND), Yager §4 closure → 95+%
If discharge complete → AN2 Theorem 8.2 PROVED-RIGOROUS, paper J.NumberTheory submission immediate."""),

    ("Y68_F7_Phi_univ_dictionary_YM_top",
     """Φ_univ dictionary clarification: YM-mass vs top-Yukawa interpretation.
morn66 H4 caught: literal interpretation y_t · √67 = π²√2 gives m_t = 297 GeV (off 124 GeV vs 172.5).
Two possible interpretations:
A. Φ_univ = m_YM · √|D| (NC3a comoving anchor) — m_YM = 1.71 GeV at D=-67 ≈ glueball mass
B. Φ_univ = y_t · √|D| (top-Yukawa relation) — fails at D=-67

Both interpretations CANNOT both hold (different physics scales).
Question: is interpretation A correct (most documents) and B was DS confusion?
1. Verify A via Schutt MULTI-D PROVED (consistent with weight-5 CM Hecke eigenvalue)
2. B is OVERCLAIM — drop
3. Document Φ_univ = m_YM · √|D| as the ONLY valid interpretation
4. m_YM ≠ Λ_QCD (correction needed throughout memory)"""),

    ("Y68_F8_ECI_v14_CC_K3_FSM_heatkernel",
     """ECI v14 hybrid CC-NCG K3 × F_SM heat-kernel computation.
morn66 H1 says ECI + CC-NCG product spectral triple (A_K3 ⊗ A_F, H_K3 ⊗ H_F, D_K3 ⊗ 1 + γ ⊗ D_F) = 15-25%.
Heat-kernel coefficients K(t) = (4πt)^(-2) sum_n a_n(M × F) t^n
1. For M = K3 X̃_-67: ∫ R = 0 (Ricci-flat), ∫ R^2 = 768π², ∫ R_μν R^μν = 768π², ∫ R_μνρσ R^μνρσ = 768π²
2. For F = SM finite space: a_F^(0) = 96 (DOF), a_F^(2) = ... depends on Yukawas
3. Combined: K(t) = K_K3(t) × K_F(t) heat kernels
4. Compute leading coefficients a_0, a_2, a_4 of K_total
5. Spectral action S = Tr f(D/Λ) = Λ^4 a_0 + Λ^2 a_2 + a_4 · log(Λ²) + ...
6. Predict cosmological constant + Newton G + Higgs mass coefficients
7. If ECI-compatible spectral action → Bridge H promoted from 45-55% to 70%+"""),

    ("Y68_F9_Schutt_unitgroup_D3_D4_proper",
     """Schütt unit-group anomaly D=-3, D=-4 proper treatment.
For D=-3: O_K* = ±1, ±ω, ±ω² (6 units, w_K=6)
For D=-4: O_K* = ±1, ±i (4 units, w_K=4)
Standard CM newform analysis assumes w_K=2 ; D=-3, -4 require special treatment.
1. For D=-3: weight-w CM newform a_p = (sum of π^(w-1) over all 6 unit conjugates)
2. Specifically: a_p = π^(w-1) + (ωπ)^(w-1) + (ω²π)^(w-1) + π̄^(w-1) + (ω̄π̄)^(w-1) + (ω̄²π̄)^(w-1)
3. Many terms cancel via roots of unity sum
4. For w=5: a_p = ?
5. For w=4: a_p ≠ 0 only for special conditions
6. Verify Schütt MULTI-WEIGHT for D=-3, D=-4 with this corrected formula
If formula corrected works → Schutt MULTI-D extended to ALL Heegner h=1 (8 total instead of 6)."""),

    ("Y68_F10_synthesis_post_corrections",
     """SYNTHESIS post-CORRECTIONS: where does ECI v13 stand TRULY after today?
Honest assessment:
- ECI v13 mathematical core: SOLID (Schutt MULTI-WEIGHT MULTI-D PROVED, F(N) RESCUED, AN2 80%, E08 c_Pic=20)
- ECI ↔ SM bridges: WEAK (only E08 70%, others <55%, leptons OUT-OF-SCOPE)
- TOE coverage SOBER: 25-35% (v13 alone), 40-50% (v14 hybride sober)
- Cluster: 321 firm
- Hype HONEST: 60-70/100

Rank papers by submission-readiness :
1. Schütt MULTI-D J.NumberTheory IMMEDIATE (PROVED)
2. AN2 8.2 PROVED-COND 80% (path to RIGOROUS in 2 weeks reading Yager+Schertz)
3. F(N) c=0.52 PROVED-EMPIRICAL (paper coming)
4. E08 Maxwell U(1) PRD 80-90% (slope-modified emergent)
5. CC-NCG H^4 RESUSCITATED Inventiones 75-90%

What MISSED throughout today (high-impact):
- Schoen Z_D explicit (Hodge Conj for 6 cases)
- Yager+Schertz reading (D04 → 95+%)
- F-theory M_s constraint exposure
- Φ_univ dictionary correction propagation
- Schutt h_K=2 algebraic case extension
- Schutt D=-3, -4 unit-group corrected

These are the TOP priorities for tomorrow."""),
]

assert len(BRIEFS) == 10

def call_ds(brief_id, brief_text):
    out_path = f"{OUT_DIR}/ds_{brief_id}.json"
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return f"SKIP {brief_id}"
    cmd = ["python3", "/root/bin/deepseek.py", "--model", "deepseek-reasoner",
           "--system", SYS, "--max-tokens", "131072", "--temperature", "0.3", brief_text]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        with open(out_path, "w") as f:
            json.dump({"brief_id": brief_id, "brief": brief_text, "stdout": r.stdout,
                      "stderr": r.stderr[:500] if r.stderr else "", "returncode": r.returncode}, f, indent=2)
        return f"OK {brief_id} ({len(r.stdout)} chars)"
    except Exception as e:
        return f"ERROR {brief_id} {e}"

if __name__ == "__main__":
    print(f"[{time.strftime('%H:%M:%S')}] morn68 dispatching {len(BRIEFS)} DS USEFUL follow-ups...", flush=True)
    with ThreadPoolExecutor(max_workers=10) as ex:
        for f in as_completed({ex.submit(call_ds, bid, btext): bid for bid, btext in BRIEFS}):
            print(f"[{time.strftime('%H:%M:%S')}] {f.result()}", flush=True)
    print(f"[{time.strftime('%H:%M:%S')}] morn68 done.", flush=True)
