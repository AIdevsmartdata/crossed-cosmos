#!/usr/bin/env python3
"""morn61 — 5 DS V4 Pro MAX EFFORT dispatches per Opus master morn60 §6 top 5 next."""
import os, json, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/tmp/morn61_DS_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

SYSTEM_PROMPT = """You are DeepSeek V4 Pro MAX EFFORT, persona Einstein/Witten/Connes hybrid.
ECI v12 ACTUALISED 2026-05-10 21:00 (post morn60 master digest):
- Cluster fab: 287 firm (+11 morn60)
- D04 AN2 T2 92% (Gross-Koblitz §3 + Schertz §6.3 discharge of Lemmas 5.4+5.6)
- D05 Schütt H^8 5-of-5 explicit Frobenius MATCH D=−67 p∈{23,29,31,37,41} via Chebyshev T_4(a_p/2p)
- C04 NC3a Lüscher fixed-point 60% NEW_CONJECTURE with β-function falsifier
- E08 Maxwell U(1) ADVANCE 70% (only ECI↔SM bridge that worked)
- E04 modular A_4 leptons FALSIFIED (rk_2 framework doesn't apply)
- YM Mille feasibility 9-22% rigorous unchanged

RAG MANDATORY: NEVER invent arXiv IDs. Use INSUFFICIENT_DATA::pending-verify if uncertain.
Verify-arxiv-py post-hoc filter is final word.

OUTPUT FORMAT:
## Verdict: ADVANCE / PARTIAL / NEW_CONJECTURE / DEAD_END / INSUFFICIENT_DATA
## Method (rigorous + adversarial)
## Numerical/structural derivation
## Citations (verified arXiv only — use INSUFFICIENT_DATA if uncertain)
## Confidence: 0-100%
## Falsifier test design (binary verdict)
## Honest gaps
"""

BRIEFS = [
    ("Y61_N01_D04_AN2_S82_crosscheck",
     """Top dispatch #1: D04 + AN2 §8.2 cross-check for full PROVED-RIGOROUS T2 promotion.
D04 (morn60) achieved 92% confidence on Gross-Koblitz §3 + Schertz §6.3 discharge of Lemmas 5.4+5.6 in AN2 Theorem 8.2. We need:
1. Read AN2 Theorem 8.2 statement: q(D) = 3^δ · |D|^⌈h/2⌉ for δ ∈ {0, 1, 2}
2. Verify each of the 5-7 key formulas from Gross-Koblitz §3 used in Lemma 5.4 discharge
3. Verify each of the 5-7 key formulas from Schertz §6.3 used in Lemma 5.6 discharge
4. Identify any remaining gap that prevents 92% → 100% (PROVED-RIGOROUS)
5. Concrete counterexample search: find any D where T2-bar trace might not discharge

If 92%→100% achievable via 1-2 specific lemma additions, ADVANCE. If gap is structural, NEW_CONJECTURE."""),

    ("Y61_N02_C04_D02_NC3a_beta_function",
     """Top dispatch #2: C04 + D02 NC3a β-function explicit one-loop computation.
C04 NC3a Lüscher fixed-point 60% (NEW_CONJECTURE morn60). D02 Wilson-flow falsifier design.
Compute one-loop β-function for the comoving coupling on Inose K3 X̃_-67:
1. Standard YM β_0 = (11/3)C_A - (4/3)T_F·n_f for SU(N), C_A = N
2. CM K3 modification via Hecke trace (Sym^4 ψ_K)
3. Wilson-flow t-derivative dg(t)/dt = -β(g(t))
4. Fixed point g* where β(g*) = 0 and m_YM(g*)·sqrt(67) = π²√2
5. Predict deviation from standard SU(N) β_0 — should be small (<5%) if Lüscher hypothesis holds

Use Lüscher 1010.4357 (Wilson flow) and Bär-Lüscher 1006.4518 (real arXiv refs verified).
If β_NC3a(g*) - β_SU(2)(g*) < 5% → ADVANCE. If > 20% → DEAD_END."""),

    ("Y61_N03_D05_8primes_D163_extension",
     """Top dispatch #3: D05 Schütt H^8 5-of-5 → 8+ primes + cross-test D=−163.
D05 morn60 verified 5/5 split primes for D=−67 via Chebyshev T_4(a_p/2p) match.
Now extend to:
1. For D=−67: add primes p ∈ {43, 47, 53, 59, 61, 71, 73} (all split in Q(√−67), bringing total to 12 primes)
2. Cross-test D=−163: verify same Chebyshev T_4(a_p/2p) match at split primes p ∈ {7, 11, 17, 23, 29, 31, 41, 43}
3. If 12/12 D=−67 + 8/8 D=−163 match within PARI 50-digit precision → Schütt-Hodge T2 PROVED-NUMERICAL
4. Use PARI mfeigenbasis(67.3.b.a) AND mfeigenbasis(163.3.b.a) — if mfinit dim returns 0 (PARI 2.17.2 bug), fall back to LMFDB API direct

Falsifier: any single p with deviation > 1e-30 → PARTIAL/DEAD_END.
PROVED-NUMERICAL across both D + 20 primes → ADVANCE."""),

    ("Y61_N04_E08_Maxwell_U1_LHC_paper",
     """Top dispatch #4: E08 Maxwell U(1) LHC falsifier prep + paper draft outline.
E08 Maxwell U(1) ADVANCE 70% (ONLY ECI↔SM bridge to advance morn60).
The hypothesis: U(1) Maxwell electromagnetism in ECI framework arises from K-theory K_0(C(X̃_-67)) of CM K3 algebra, NOT trivial limit of YM SU(N) at N=1.

1. Derive QED fine-structure α(M_Z)^{-1} = 127.952 ± 0.009 from K-theory class group structure
2. Predict deviation: does ECI predict different α-running than standard SM at LHC scales?
3. Concrete LHC falsifier: Drell-Yan dimuon at sqrt(s)=14 TeV — what's the ECI prediction vs SM?
4. Outline 8-page paper for Phys. Rev. D / JHEP: Title, Abstract, §1 Intro (CM K3 K-theory), §2 Derivation, §3 LHC predictions, §4 Falsifier
5. Identify rigorous gaps remaining for 70% → 100%

Cite ECI v12 actualised baseline + Connes (NCG) + Vafa (heterotic K3)."""),

    ("Y61_N05_R02_fractional_Ak_R4",
     """Top dispatch #5: R02 fractional A_k explicit construction on R⁴.
R02 (morn60) ADVANCE 40% on R⁴ Z5 zero-mode resolution via fractional A_k sequences.
The Z5 obstacle (5-dim zero-mode moduli on Kummer K3) is the key blocker for mass gap on R⁴.
3 resolution routes (per morn58/59):
- (A) project zero modes via Yagger trace
- (B) non-instanton A_k sequences (FRACTIONAL, NEW)
- (C) fibered Picard-Garibaldi-Heinzner over moduli

Focus on Route (B): construct fractional A_k Yang-Mills connections on R⁴ explicitly.
1. Standard A_k singularity: C²/Z_k orbifold with metric resolution
2. Fractional A_k: A_{p/q} for p/q ∈ Q irrational sequence
3. ASD instanton equations on fractional A_{p/q} resolution
4. Show zero-mode count NOT = 5 for fractional limits
5. Convergence as p/q → standard A_k

If construction yields zero-mode count ≠ 5 in limit → ADVANCE Z5 resolution.
If zero-mode count stays 5 → fractional approach DEAD_END."""),
]

assert len(BRIEFS) >= 5

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
    print(f"[{time.strftime('%H:%M:%S')}] morn61 dispatching {len(BRIEFS)} DS top-5 MAX EFFORT (max_tokens=131072, timeout=3600)...", flush=True)
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(call_ds, bid, btext): bid for bid, btext in BRIEFS}
        for f in as_completed(futs):
            print(f"[{time.strftime('%H:%M:%S')}] {f.result()}", flush=True)
    print(f"[{time.strftime('%H:%M:%S')}] morn61 done.", flush=True)
