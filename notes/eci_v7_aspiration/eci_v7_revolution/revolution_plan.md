# ECI v7.0.0 — Revolution Plan (Roadmap)

**Today:** 2026-05-04. Target v7.0.0 release: 2027-07-31 (14 months).

The brief asked for a 6-month roadmap. **Honest answer: 6 months is enough for Paper-A submission and the cosmological MCMC re-fit; the *full* v7.0.0 release with three papers in the pipeline takes 14 months.** Below I give both a 6-month sub-plan (Paper-A) and the full 14-month plan to v7.0.0.

---

## Quarter-by-quarter schedule (14 months)

### 2026 Q2 — May to June (6 weeks remaining in the quarter)

**Goal**: extend Hecke-closure verification beyond E2; run the GPU NUTS cosmology MCMC once.

| Task | Owner | Effort | Output | Cost |
|---|---|---|---|---|
| Sympy: Hecke closure for S′₄ triplet 3̂ at weight 2 (cusp form, dim 3) | Sub-agent (sympy) | 2 weeks | `notes/eci_v7_aspiration/B3_sp4_quark_hecke/triplet_closure.py + .md` | 0 |
| Sympy: Hecke test for hatted doublet 2̂ at weight 3 (test χ_4(p)+p conjecture) | Sub-agent (sympy) | 2 weeks | `notes/eci_v7_aspiration/B3_sp4_quark_hecke/hatted_2bar.py + .md` | 0 |
| Run E1 GPU NUTS on full 6-lever ECI scan, Vast.ai Profile L (RTX 4090 × 24h) | Kevin + sub-agent (GPU) | 1 day prep + 24 h run | `mcmc/eci_v7_nuts_run1/` posterior_summary.json | $300–500 |
| Add Wolf-NMC vs ECI-NMC log-B comparison at the *converged* ξ_χ = 0.05 working point | Sub-agent (cosmology) | 1 week | `notes/eci_v7_aspiration/A4_wolf_eci_structural_v2.md` | 0 |
| Begin Paper-A (Hecke closure of S′₄ doublet & triplet) draft | Kevin + Opus | 2 weeks | `paper/papers/v7/paperA_hecke_closure/draft.tex` | 0 |

**End-of-Q2 milestone**: Hecke closure verified for unhatted 2 (already done E2), triplet 3̂, hatted 2̂. Paper-A first draft.

### 2026 Q3 — July to September

**Goal**: Submit Paper-A. Begin Yukawa-fit pipeline.

| Task | Owner | Effort | Output | Cost |
|---|---|---|---|---|
| Polish Paper-A; internal cross-check vs LMFDB level-4 weight-2 catalogue | Kevin + Opus | 4 weeks | Paper-A v1.0 | 0 |
| Submit Paper-A to JHEP | Kevin | 1 day | arXiv ID + JHEP submission | 0 |
| Build sympy + 1-loop RGE pipeline for S′₄ Yukawa textures (modulus τ free, c_α coefficients fixed by Hecke-closure) | Sub-agent (RGE) | 4 weeks | `numerics/eci_v7_yukawa/rge.py` | 0 |
| Test pipeline on dMVP26 (arXiv:2604.01422) reference fit (Hecke-closure off) — reproduce their best-fit | Sub-agent (RGE) | 2 weeks | reproduce dMVP26 (m_u, m_c, m_t) within 20% | 0 |
| Pre-register Hecke-locked Yukawa fit prediction (commit predicted m_c/m_t to repo before fit) | Kevin | 1 day | `notes/eci_v7_aspiration/preregistration.md` | 0 |

**End-of-Q3 milestone**: Paper-A submitted. Yukawa-fit pipeline running on the *unconstrained* dMVP26 reference. **6-month sub-plan ends here.**

### 2026 Q4 — October to December

**Goal**: Produce m_c/m_t prediction; compare to PDG.

| Task | Owner | Effort | Output | Cost |
|---|---|---|---|---|
| Run Hecke-closure-constrained Yukawa fit (full sympy + 1-loop RGE) | Sub-agent (RGE) | 6 weeks | predicted (m_u, m_c, m_t) at M_GUT, evolved to M_Z | 0 |
| Compare to PDG; quantify σ-discrepancy | Kevin + Opus | 1 week | PDG comparison table | 0 |
| Predict Cabibbo angle θ_C with Hecke-locked m_d/m_s | Sub-agent (RGE) | 2 weeks | θ_C ± δ prediction | 0 |
| Begin Maass-form ↔ KMS finite-truncation construction | Sub-agent (math.OA) | 4 weeks | `notes/eci_v7_aspiration/maass_kms_finite_N.py` | 0 |
| Begin Paper-B draft (Yukawa fit) | Kevin + Opus | 2 weeks | Paper-B v0.5 draft | 0 |

**End-of-Q4 milestone**: m_c/m_t predicted; θ_C predicted. Paper-B half-drafted.

### 2027 Q1 — January to March

**Goal**: Submit Paper-B. Run A₄ neutrino sector at level 3.

| Task | Owner | Effort | Output | Cost |
|---|---|---|---|---|
| Polish Paper-B; cross-check via independent re-derivation | Kevin + Opus + audit agent | 6 weeks | Paper-B v1.0 | 0 |
| Submit Paper-B to PRD or JHEP | Kevin | 1 day | arXiv ID + journal submission | 0 |
| Run Hecke-closure constraint on A₄ triplet at level 3 (Feruglio's lepton sector) | Sub-agent (sympy) | 4 weeks | `numerics/eci_v7_lepton/a4_lepton.py` | 0 |
| Predict Δm²_atm/Δm²_sol with Hecke constraint; compare to current global fit | Sub-agent (lepton) | 2 weeks | lepton mass-ratio prediction | 0 |
| Continue Paper-C (algebraic side: Hecke-equivariant inclusion of M̃(D)) | Kevin + Opus | 4 weeks | Paper-C v0.5 draft | 0 |

**End-of-Q1-2027 milestone**: Paper-B submitted. Lepton predictions in hand.

### 2027 Q2 — April to June

**Goal**: Submit Paper-C. Compile v7.0.0 release.

| Task | Owner | Effort | Output | Cost |
|---|---|---|---|---|
| Polish Paper-C (Comm.Math.Phys. target) | Kevin + Opus + audit | 6 weeks | Paper-C v1.0 | 0 |
| Submit Paper-C | Kevin | 1 day | arXiv ID + Comm.Math.Phys. submission | 0 |
| Compile v7.0.0 manuscript: integrate Paper-A, Paper-B, Paper-C summaries into eci.tex | Kevin + Opus | 4 weeks | eci.tex v7.0.0 | 0 |
| Internal v7.0.0 audit (Opus + Gemini cross-check, follow v6 audit protocol) | audit agent | 2 weeks | audit ledger | 0 |

**End-of-Q2-2027 milestone**: Paper-C submitted. v7.0.0 manuscript ready.

### 2027 Q3 — July (release month)

| Task | Owner | Effort | Output |
|---|---|---|---|
| Final v7.0.0 polish | Kevin + Opus | 2 weeks | ready manuscript |
| **v7.0.0 release: arXiv + Zenodo CoreTrustSeal + GitHub tag** | Kevin | 1 day | v7.0.0 published |

**End-of-Q3-2027 milestone**: **v7.0.0 RELEASED** (target date 2027-07-31).

---

## Resource estimates

### Compute

| Category | Estimate | Vast.ai equivalent |
|---|---|---|
| GPU NUTS cosmology MCMC (E1 pipeline, 1 full scan) | 24 GPU·h on RTX 4090 | $20–40 / scan; budget 5 scans = $200 |
| Yukawa-fit RGE pipeline (sympy on CPU) | ~100 CPU·h total | $50 (or local PC) |
| Maass-form ↔ KMS finite-rank construction (sympy + numpy) | ~50 CPU·h | $25 (or local PC) |
| Subtotal compute | | **~$300–500** |

### Sub-agent runs

| Wave | Count | Per-run cost (Anthropic API) | Subtotal |
|---|---|---|---|
| Sympy verifications (Hecke closure for triplet 3̂, hatted 2̂, A₄ triplet) | 6 runs | $5 | $30 |
| RGE pipeline build + tests | 4 runs | $10 | $40 |
| Yukawa fit + θ_C prediction | 4 runs | $15 | $60 |
| Maass-form ↔ KMS construction | 4 runs | $20 | $80 |
| Paper drafting + audit cross-checks | 12 runs | $15 | $180 |
| Subtotal sub-agents | | | **~$390** |

### Total v7.0.0 budget (compute + agents) = **~$700–900**.

This is well below Kevin's typical Vast.ai budget ($500–1500 per quarter from past patterns).

---

## Critical path & milestones

```
Today (2026-05-04)
  |
  | Q2: Hecke triplet 3̂ + hatted 2̂ (4 weeks) ────────┐
  |                                                       │
  | Q3: Paper-A draft + RGE pipeline (8 weeks) ────────┤───→ Paper-A submitted (2026-09)
  |                                                       │      ↓
  | Q4: Yukawa fit (m_c/m_t, θ_C) (8 weeks) ───────────┤      Paper-A reviewed
  |                                                       │
  | Q1-2027: Paper-B draft + lepton sector (12 weeks) ─┤───→ Paper-B submitted (2027-03)
  |                                                       │      ↓
  | Q2-2027: Paper-C polish + v7.0.0 compile (12 weeks) ┤      Paper-C submitted
  |                                                       │      ↓
  | Q3-2027 (Jul): v7.0.0 release ─────────────────────┘──→ v7.0.0 RELEASED
```

### Milestone go/no-go gates

| Gate | When | Pass condition | Fail action |
|---|---|---|---|
| **G1**: Triplet 3̂ Hecke-closes | 2026-Q2 (week 4) | Schur+sympy gives M_3̂(p) = λ_3̂(p)·I_3 with λ_3̂(p) matching LMFDB level-4 weight-2 newform a(p) | If fails, S′₄ flavour assignment is broken; revert to S₄ at level 3 (no metaplectic cover) — Paper-A reduces to A₄/S₄ |
| **G2**: Yukawa fit reproduces dMVP26 | 2026-Q3 (week 8) | predicted (m_u,m_c,m_t) within 20% of dMVP26 best-fit (Hecke off) | Pipeline bug; debug before Hecke-on run |
| **G3**: Hecke-locked m_c/m_t within 3σ of PDG | 2026-Q4 (week 6) | predicted m_c/m_t in [0.0070, 0.0078] | If outside: Paper-B becomes a *negative-result* paper showing S′₄ Hecke closure is incompatible with PDG; this is still publishable but downgrades the v7 narrative significantly |
| **G4**: Cabibbo θ_C prediction within 1° of 13.0° | 2026-Q4 (week 8) | predicted θ_C ∈ [12.0°, 14.0°] | similar to G3; downgrade narrative |
| **G5**: Maass-form ↔ KMS finite-truncation construction at N=10 | 2027-Q1 (week 8) | explicit Y_N(τ) with Hecke eigenvalues matching modular sub-algebra inclusion | If fails: Paper-C reduces to a structural-conjecture paper rather than a theorem |
| **G6**: All three papers accepted by Q3-2027 | 2027-Q3 | 3 acceptance letters | Push v7.0.0 release to 2027-Q4 if needed |

---

## Risk register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Triplet 3̂ Hecke-closure fails (G1) | 15% | high | Paper-A becomes a doublet-only result; reduce S′₄ → S₄ in narrative |
| m_c/m_t prediction off PDG by >5σ (G3) | 25% | high | Acknowledge as a *negative result* in Paper-B; reframe v7 around the structural Hecke result without claiming Yukawa fit |
| LISA-Ξ external falsifier rules out ECI's H4 → Ξ=1 prediction | 10% (only by 2034) | high but distant | Document v7's H4 prediction; await LISA |
| User loses interest before Paper-A submission | low | low | 6-month sub-plan delivers Paper-A; this is a fully-contained deliverable even if v7 stalls |
| Sympy run exceeds memory / runtime budget on triplet 3̂ | 5% | low | Use Vast.ai high-RAM instance ($50 backup) |
| Compute cost overrun on GPU NUTS scans | 10% | low | Cap at $1000 total compute; revert to CPU scan if needed |

---

## What v7.0.0 contains (target Table of Contents)

```
1. Introduction (3 pp): the threaded architecture v6, the v7 structural pivot
2. Type-II crossed product as Hecke-equivariant inclusion (Paper-C summary, 5 pp)
3. S′₄ Hecke-closed Yukawa textures (Paper-A summary, 5 pp)
4. Hecke-locked Yukawa fit: PDG retrodiction (Paper-B summary, 4 pp)
5. The six threaded programmes — status as of 2027-Q2 (5 pp)
   — NMC: inherits Wolf 2025 evidence; ξ_χ ≃ 0 working point unchanged
   — EDE: f_EDE ≃ 0.09 ± 0.03 phenomenological input
   — Dark Dimension: c'_DD ≃ 0.05 imposed
   — Cryptographic Censorship A3: speculative appendix unchanged
   — Persistent-homology cosmology: structural diagnostic unchanged
   — Type-II observer algebra: now extended via Hecke inclusion (NEW v7)
6. Falsifiable predictions (3 pp): m_c/m_t retrodiction; Cabibbo retrodiction;
   CKM γ phase forward prediction; LHCb Run 4 D⁰ observable forward
7. Structural limitations / open questions (2 pp)
8. Editorial note v7 + audit ledger (1 pp)
```

Total v7.0.0 length: ~30 pages compiled (similar to v6.0.47).

---

## What v7.0.0 does NOT contain

Per the brief's anti-hallucination calibration:

- **No JWST z>10 section** (E6 deferred to v6.1).
- **No FRB DM-z section** (E5 deferred to v6.0.50).
- **No α-attractor inflation prediction**.
- **No "MCC/CCF v7" branding**: Q_arith ill-defined, λ_arith numerological, U-conjecture refuted.
- **No "5σ DESI DR3 NMC discovery" claim**: E4 has shown <1σ at the working point; v7 acknowledges the Lakatos failure on the cosmology axis.
- **No claim that the Type-II × Connes-Marcolli bridge is closed**: Paper-C frames it as an explicit conjecture (Hecke-equivariant inclusion) with finite-rank evidence (G5), not a theorem.
- **No claim that m_u (or any single quark mass) is *predicted* from first principles**: ECI v7 *constrains* the Yukawa textures via Hecke closure but does not claim to derive the numerical values without input.
- **No Nobel-narrative posturing**: per the eci_nobel_audit findings, ECI is on a Foundational/Breakthrough Prize trajectory, not a Nobel trajectory; v7 does not change this honest assessment.

---

## Single most important next action

**This week (2026-05-05 to 05-11)**: launch the sympy sub-agent for the **triplet 3̂ Hecke closure at S′₄ level 4 weight 2** (gate G1). This is the single highest-value 2-week task: it determines whether Paper-A is a doublet-only short letter (reduced impact) or a doublet+triplet+singlet full closure (intended impact). It costs $5 in agent runs and 0 in compute. **Do it first.**

After G1 passes (assumed 85% probability), the rest of the 6-month plan (Paper-A submission by 2026-09) follows mechanically.
