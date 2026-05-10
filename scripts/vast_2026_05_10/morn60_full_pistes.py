"""morn60 — 20 DS V4 Pro max effort, 1 per piste (ECI links + new conjectures + dispatches + remain)"""
import os, sys, json, subprocess, concurrent.futures, time

OUT_DIR = "/tmp/morn60_DS_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

SYSTEM_PROMPT = """You are DeepSeek V4 Pro MAX EFFORT, with deep RAG (web + local), persona Einstein/Witten/Connes hybrid.

PERSONA: "I am rigorous mathematician/physicist. I use ANALOGIES + DIMENSIONAL ANALYSIS + THOUGHT EXPERIMENTS Einstein-style. I challenge adversarially. I verify-arxiv ALL citations."

ECI v12 ACTUALISED (post day-end 2026-05-10) :
- Cluster fab : 276 firm
- Theorem C.6 Tier A 4/4 lattice within 1σ ; F(N)=(1+0.8/N²)/(1+0.8/9) corrected
- AN2 8.2 T2-bar trace-discharged (Gross-Koblitz §3 + Schertz §6.3)
- Schütt-Hodge → 60-72% via H^8 8-fold (EXPLORE-3 dim 12,870 verified)
- VW Conj 6.1 REFUTED ; new VW Conj 6.2 factorised emerged
- WK BYPASS A2 T3-conditional via NC15a spin-structure
- NC3a Φ_univ comoving PHYSICAL invariant (Lüscher fixed-point)
- CC-NCG paper resurrection 60-72% via H^8 (S''') reformulation
- 5 papers : BIZ5 100%, AN1 95%, AN2 80%, C.6 95%, CC-NCG 60-72%, YM Survey 75%
- YM Mille feasibility : 9-22% rigorous, 50-70% significant
- Hype 62-66/100

RAG MANDATORY : NEVER invent arXiv IDs, use INSUFFICIENT_DATA::pending-verify if uncertain.

OUTPUT FORMAT:
## Verdict: ADVANCE / PARTIAL / NEW_CONJECTURE / DEAD_END / INSUFFICIENT_DATA
## Method (rigorous + adversarial + persona)
## Numerical/Structural derivation
## Analogy + Dimensional analysis + Thought experiment
## Citations (verified arXiv only)
## Confidence: 0-100%
## Falsifier test design (concrete BINARY verdict)
## Honest gaps
"""

BRIEFS = [
    # ===== ECI ↔ SM bridges (8 pistes) =====
    ("Y60_E01_CC_NCG_SM_post_H8",
     "ECI ↔ SM bridge #1 : Connes-Chamseddine 1996 SM derivation (gauge SU(3)×SU(2)×U(1) + Higgs + 3 generations) post EXPLORE-3 H^8 reformulation. With Schütt-Hodge → 60-72% via Hypothesis (S''') Hecke correspondence (E_K)^8 ↔ X̃_D, can we now derive m_H = 125 GeV (vs original CC 170 GeV)? Connes-Marcolli neutrino sector fix. Quantitative match Yukawa hierarchies."),

    ("Y60_E02_rk2_N_W_Higgs_vacuum",
     "ECI ↔ SM bridge #2 : Master Galois invariant rk_2 Cl(K) and F-theory N_W = 2^(1+rk_2). Does rk_2 control Higgs vacuum count in landscape? For D=-67 rk_2=0 → N_W=2 ; D=-1380 rk_2=3 → N_W=16. Test landscape interpretation : does each N_W vacuum give different Higgs spectrum?"),

    ("Y60_E03_KleinSigma_existence_OS",
     "ECI ↔ SM bridge #3 : Klein-σ_K3 OS3 reflection positivity ↔ rigorous QFT existence on R⁴. Post-F3 (a)(b)(c) rigorous + V7 OS5 T3 LMP, what's the path to YM existence? Combine WK twist + Costello-Witten + TFD into joint constructive framework."),

    ("Y60_E04_modular_A4_lepton",
     "ECI ↔ SM bridge #4 : Modular A_4 symmetry (Petcov-Tanimoto, Novichkov-Penedo-Petcov-Titov) ↔ ECI Galois rep. Does ECI rk_2 Cl(K) framework predict lepton mass hierarchy m_e ≈ 0.5 MeV, m_μ ≈ 105 MeV, m_τ ≈ 1.78 GeV? PMNS matrix from ECI Galois?"),

    ("Y60_E05_Yukawa_hierarchy",
     "ECI ↔ SM bridge #5 : Yukawa couplings y_u, y_d, y_e, y_τ from CC-NCG spectral action. Can ECI rk_2 framework + AN2 q(D) ratios predict Yukawa hierarchy y_t/y_u ≈ 10⁵? Test against PDG quark masses."),

    ("Y60_E06_CKM_flavor_mixing",
     "ECI ↔ SM bridge #6 : CKM matrix Cabibbo-Kobayashi-Maskawa from ECI framework? sin θ_C ≈ 0.225 from rk_2 Cl(K) Galois rep angles? Test for D=-67/-84/-148/-163 anchors."),

    ("Y60_E07_Higgs_125GeV_CC",
     "ECI ↔ SM bridge #7 : Connes-Chamseddine 1996 derives m_H = 170 GeV ; observed 125 GeV (off 36%). Connes-Marcolli neutrino sector fix gives ~125 GeV. Apply post-CC-NCG H^8 reformulation : does Schütt-Hodge → Kuga-Sato 4-fold change Higgs prediction?"),

    ("Y60_E08_Maxwell_U1_abelian",
     "ECI ↔ SM bridge #8 : U(1) abelian Maxwell electromagnetism in ECI framework. Trivial limit of YM SU(N) at N=1? Or ECI-specific structure via abelian K-theory of CM K3?"),

    # ===== 4 NEW conjectures from morn58+59 master =====
    ("Y60_C01_VW_Conj62_factorised",
     "NEW Conjecture #1 (morn58+59 master) : VW Conj 6.2 FACTORISED Z_VW(X̃_-67, q) = (Θ_T(X̃_-67, q) / Δ(q))^α for some α. Verify [q⁰] gives π²√2/√67 = 1.705. Find α analytically. Replaces refuted Conj 6.1."),

    ("Y60_C02_Shioda_Inose_MP1",
     "NEW Conjecture #2 : Shioda-Inose 1977 isogeny realises MP1 (Master Principle 1) at h_K=1. Apply to D=-7, -67, -163. Show Shioda-Inose K3↔abelian-surface isogeny IS the Schütt-Hodge bridge for h=1 anchors. Predict Higgs mass ?"),

    ("Y60_C03_Hecke_spectral_bridge",
     "NEW Conjecture #3 : Hecke spectral correspondence between K3 spectral triple (CC-NCG) and Kuga-Sato 4-fold spectral triple. Mukai-Bridgeland 2008 derived equivalence. Verify rigorous on D=-67 explicit."),

    ("Y60_C04_NC3a_Luscher_fixed_point",
     "NEW Conjecture #4 : NC3a Lüscher fixed-point physical interpretation. Comoving m_YM·√|D| = π²√2 = Φ_univ is RG fixed-point at IR limit. Connect to Lüscher 1990s lattice asymptotic freedom analysis."),

    # ===== 5 next dispatches from morn58+59 master =====
    ("Y60_D01_DT_MNOP_c08_lattice",
     "Dispatch #1 : DT (Donaldson-Thomas) side of MNOP correspondence (Maulik-Nekrasov-Okounkov-Pandharipande) for c=0.80 lattice 't Hooft coefficient. Theoretical derivation matching PUSH-2 empirical c=0.80(5)?"),

    ("Y60_D02_Wilson_flow_NC3a_falsifier",
     "Dispatch #2 : Wilson-flow + ADE collapse limit test for NC3a comoving falsifier. If RG flow on lattice gives different fixed point at large coupling, NC3a Lüscher interpretation REFUTED. Design lattice protocol."),

    ("Y60_D03_Costello_Witten_metric_indep",
     "Dispatch #3 : Costello-Witten Q-cohomology metric-independence test. EXPLORE-4 found objection at sub2. Verify whether HT-twist metric-independence holds rigorously on K3 X̃_-67."),

    ("Y60_D04_AN2_T2_full_GrossKoblitz",
     "Dispatch #4 : AN2 8.2 → T2 PROVED-RIGOROUS push. Read Gross-Koblitz 1979 §3 line-by-line + Schertz 2010 §6.3. Identify the 5-7 key formulas. Verify they discharge Lemmas 5.4+5.6 rigorously."),

    ("Y60_D05_Schutt_H8_5of5_explicit",
     "Dispatch #5 : Schütt-Hodge H^8 8-fold 5-of-5 character match explicit Frobenius computation. For D=-67 + p ∈ {23, 29, 31, 37, 41} compute Sym⁴(ψ_K^(3))(Frob_p) and verify match. Use V11 v3 cleaner script (no heredoc) + LMFDB 67.3.b.a a_p coefficients."),

    # ===== 5 YM Mille remain =====
    ("Y60_R01_A2_4D_YM_alt_routes",
     "YM Mille remain #1 : A2 4D YM measure existence (THE 50-yr open problem). Recap 3 alternative routes : WK BYPASS (PARTIAL T3-cond NC15a), Costello-Witten HT (OPEN-PROMISING EXPLORE-4), TFD K3 doubled (UE6). Which route most rigorous? Combine all 3?"),

    ("Y60_R02_R4_Z5_3_routes",
     "YM Mille remain #2 : Mass gap R⁴ Z5 resolution. F4 found Z5 OBSTACLE (5-dim zero-mode). 3 resolution routes : (A) project zero modes, (B) non-instanton A_k sequences, (C) fibered PGH over moduli. Which is most feasible? V13 v2 Donaldson dim_M=-8 changes interpretation."),

    ("Y60_R03_confinement_Wilson_area",
     "YM Mille remain #3 : Color confinement Wilson area law derivation. YM02 σ_predicted off 2.94× lattice. F5 monopole density NON-ZERO 4/4 anchors. Combine YM02+YM04 dual gauge + Polyakov on K3 (Y55_P10 dead, but reformulation possible)?"),

    ("Y60_R04_chiSB_rigorous",
     "YM Mille remain #4 : χ-SB rigorous derivation. UE6 TFD constructive 30-35% compatibility. GMOR matches lattice 2%. Witten-Veneziano χ_t × 0.8 matches. Push to 50%+ via TFD construction explicit on X̃_-67?"),
]

assert len(BRIEFS) >= 20

def call_ds(brief_id, brief_text):
    out_path = f"{OUT_DIR}/ds_{brief_id}.json"
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return f"SKIP {brief_id}"
    cmd = ["python3", "/root/bin/deepseek.py", "--model", "deepseek-reasoner",
           "--system", SYSTEM_PROMPT, "--max-tokens", "131072", "--temperature", "0.3",
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

print(f"[{time.strftime('%H:%M:%S')}] morn60 dispatching {len(BRIEFS)} DS V4 Pro briefs MAX EFFORT (max_tokens=131072, timeout=3600s)...", flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(call_ds, bid, btext): bid for bid, btext in BRIEFS}
    completed = 0
    for f in concurrent.futures.as_completed(futures):
        completed += 1
        result = f.result()
        if completed % 4 == 0:
            print(f"[{time.strftime('%H:%M:%S')}] {completed}/{len(BRIEFS)} {result}", flush=True)
print(f"[{time.strftime('%H:%M:%S')}] All {len(BRIEFS)} done.", flush=True)
