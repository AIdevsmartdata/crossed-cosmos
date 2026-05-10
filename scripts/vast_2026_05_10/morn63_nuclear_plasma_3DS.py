#!/usr/bin/env python3
"""morn63 — 3 DS V4 Pro MAX EFFORT on ECI ↔ nuclear/plasma/heavy-ion bridges"""
import os, json, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/tmp/morn63_DS_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

SYSTEM_PROMPT = """You are DeepSeek V4 Pro MAX EFFORT, persona theoretical physicist + nuclear experimentalist hybrid.
ECI v12 ACTUALISED 2026-05-10 21:45:
- Schutt-Hodge MULTI-D PROVED-NUMERICAL 6/6 h_K=1 discriminants {-7,-11,-19,-43,-67,-163} weight-5
- F(N) Theorem C.6 RESCUED with c=0.52 (not PUSH-2 c=0.80) ; 4/4 SU(2-5) anchors within 0.4σ ; predictions SU(6-10) {3.40,3.38,3.37,3.37,3.36}
- m_YM·sqrt(67) = π²√2 ≈ 13.96 (NC3a comoving anchor at D=-67)
- Λ_QCD ≈ 290 MeV (n_f=4 PDG) ; m_YM ≈ 1.71 GeV (or 290 MeV reanalysis Opus #5)
- Cluster 295 firm

RAG MANDATORY: NEVER invent arXiv IDs.

OUTPUT FORMAT:
## Verdict: ADVANCE / PARTIAL / NEW_CONJECTURE / DEAD_END / INSUFFICIENT_DATA
## Method
## Numerical/structural derivation
## Citations (verified arXiv only)
## Confidence: 0-100%
## Falsifier test
## Honest gaps
"""

BRIEFS = [
    ("Y63_QGP_Tc_etaS",
     """Mission #1: ECI ↔ QGP critical temperature T_c + shear viscosity η/s
Standard lattice QCD: T_c ≈ 156 MeV (chiral) / 170 MeV (Polyakov loop).
QGP transport: η/s ratio at T_c ≈ 0.1-0.4 (RHIC), bounded below by 1/(4π) ≈ 0.0796 (Kovtun-Son-Starinets).
ECI v12 predicts m_YM, Λ_QCD, glueball masses via Theorem C.6 + NC3a.

DERIVE explicitly:
1. T_c from ECI : T_c ∝ m_YM × ζ where ζ ≈ 0.10 from lattice fit. For ECI m_YM(D=-67), what's T_c?
2. η/s from ECI : Φ_univ = π²√2 ↔ holographic bound 1/(4π) — does ECI saturate the bound?
3. Heavy-ion observables : v_2, v_3 collective flow, jet quenching dE/dx
4. Falsifier: ALICE/RHIC measurements at √s_NN = 5.02 TeV vs ECI prediction
5. EIC@BNL ~2030 will probe gluon saturation at small x → ECI prediction?

Cite verified : Kovtun-Son-Starinets hep-th/0405231, Bernhard-Moreland-Bass 1605.03954, Aamodt et al ALICE 1011.3914."""),

    ("Y63_solar_neutrino_ppchain",
     """Mission #2: ECI ↔ solar neutrinos via p-p fusion chain
p-p chain: 4 protons → He-4 + 2 e+ + 2 ν_e + 26.7 MeV
Solar ν_e flux at Earth: Φ ≈ 6.5×10^10 /cm²/s (pp), 5×10^9 /cm²/s (B-8)
Super-K: confirmed ν oscillations Δm²_31 ≈ 2.5×10^-3 eV², θ_13 ≈ 8.5°
Hyper-K + JUNO + DUNE will improve precision 10× by 2030

ECI v12 predicts m_ν via cosmological Σm_ν ∈ [60, 100] meV (Opus #7 TOP-4 bridge 5/10).
Question: derive solar neutrino observables from ECI :
1. Survival probability P(ν_e → ν_e) at solar core E ~ 1 MeV via MSW + ECI mixing matrix
2. Day-night asymmetry A_DN at Super-K
3. Σm_ν from ECI MP3 Φ_univ = π²√2 cosmological derivation
4. Predict NEW solar ν observable testable with Hyper-K (10× SK statistics)
Cite verified arXiv only."""),

    ("Y63_color_SC_dense_baryon",
     """Mission #3: ECI ↔ Color superconductivity at dense baryon matter (FAIR/NS post-merger)
Color superconductivity: at very high baryon density μ_B > 1 GeV, quark Cooper pairs form
Color-flavor-locked (CFL) phase: gap Δ ~ Λ_QCD exp(-π²/(g√2))
Neutron star post-merger: density ~ 5-10 ρ_nuclear, possible CFL core
FAIR (Darmstadt ~2028) will probe QCD phase diagram T-μ_B at mid-density

ECI v12 predicts Λ_QCD ≈ 290 MeV (NC3a) + g(μ) one-loop running.
DERIVE:
1. CFL gap Δ at μ_B = 500 MeV via ECI Λ_QCD + 't Hooft coupling
2. NS EOS at dense regime : pressure P(ρ) for ECI lattice QCD prediction
3. Predict NS post-merger ringdown frequency f_GW ~ Δ ⟨...⟩ / M_NS
4. Falsifier: LIGO post-merger spectrum + FAIR phase diagram measurement
Cite verified arXiv only."""),
]

assert len(BRIEFS) == 3

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

if __name__ == "__main__":
    print(f"[{time.strftime('%H:%M:%S')}] morn63 dispatching {len(BRIEFS)} DS nuclear/plasma...", flush=True)
    with ThreadPoolExecutor(max_workers=3) as ex:
        for f in as_completed({ex.submit(call_ds, bid, btext): bid for bid, btext in BRIEFS}):
            print(f"[{time.strftime('%H:%M:%S')}] {f.result()}", flush=True)
    print(f"[{time.strftime('%H:%M:%S')}] morn63 done.", flush=True)
