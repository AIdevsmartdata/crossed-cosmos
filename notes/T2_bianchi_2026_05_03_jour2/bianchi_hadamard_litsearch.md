# Bianchi V / IX Hadamard Literature Search — Deliverable

**Date** 2026-05-02. **Method**: INSPIRE-HEP API + arXiv abstract WebFetch (arXiv API blocked HTTP 429 from VPS; INSPIRE used as primary). All abstracts verbatim. Local PDF extraction of 2305.11388 (44 pp) and 1302.3174 (22 pp) for theorem quotes. NO LLM-recall.

## 1. Top 10 papers (verified arXiv IDs)

| # | arXiv | Title (verbatim) | Relevance (1 line) |
|---|---|---|---|
| 1 | **2305.11388** | "States of Low Energy on Bianchi I spacetimes" (Banerjee, Niedermaier) | Reference SLE Hadamard on Bianchi I T³; explicit conclusion §6 line 2338-2350: extension to Bianchi II-IX "relevant and feasible" but NOT done. |
| 2 | **1302.3174** | "States of Low Energy in Homogeneous and Inhomogeneous, Expanding Spacetimes" (Them, Brum) | Theorem (PDF L1212-1215): SLE Hadamard for any GH spacetime with `ds²=dt²−c(t)²hᵢⱼdxⁱdxʲ` + compact Cauchy. Covers ISOTROPIC Bianchi V/IX, NOT anisotropic. |
| 3 | **math-ph/0109010** | "Adiabatic vacuum states on general spacetime manifolds" (Junker, Schrohe) | Adiabatic→Hadamard on any GH + compact Cauchy. Abstract existence covers Bianchi V/IX, no explicit construction. |
| 4 | **1212.6180** | "Explicit harmonic and spectral analysis in Bianchi I-VII type cosmologies" (Avetisyan, Verch) | Plancherel + Laplacian eigenfunctions on Bianchi I-VII (incl. V). Mathematical input only; no Hadamard. |
| 5 | **1212.2408** | "A unified mode decomposition method for physical fields in homogeneous cosmology" (Avetisyan) | Mode decomposition on all Bianchi types incl. S³. Companion infrastructure paper. |
| 6 | **0704.2986** | "States of Low Energy on Robertson-Walker Spacetimes" (Olbermann) | Original SLE on RW (k=−1,0,+1) — covers isotropic Bianchi V/IX limits. |
| 7 | **0812.4033** | "Distinguished quantum states in a class of cosmological spacetimes and their Hadamard property" (Dappiaggi, Moretti, Pinamonti) | Verbatim: "specialising to **open FRW models**, we ... prove that the preferred state is of Hadamard form." Bulk-to-boundary; covers isotropic Bianchi V (k=−1). |
| 8 | **2509.13162** | "Asymptotic velocity domination in quantized polarized Gowdy cosmologies" (Niedermaier, Sedighi, Sep 2025) | BN23 follow-up — extends to **inhomogeneous Gowdy T³**, NOT Bianchi V/IX. 1 of only 4 INSPIRE citations of 2305.11388. |
| 9 | **1602.00930** | "Hadamard states for the Klein-Gordon equation on Lorentzian manifolds of bounded geometry" (Gérard, Oulghazi, Wrochna) | Pure Hadamard via pseudo-differential calculus; existence covers Bianchi V/IX in principle but no minimization-defined state. |
| 10 | **2311.11043** | "Hadamard states for linearized gravity on spacetimes with compact Cauchy surfaces" (Gérard, CMP 2024) | Linearized gravity Hadamard existence on any Einstein + compact Cauchy. Tangential. |

## 2. Verdict per Bianchi type

- **Bianchi V (compact H³)**: ISOTROPIC ✓ YES (Brum-Them, Olbermann, Dappiaggi-Moretti-Pinamonti). ANISOTROPIC ✗ NO. INSPIRE 0 hits "Hadamard state"+"Bianchi V". Bianchi V is type B → no symmetry-reduced Lagrangian → extra complication.
- **Bianchi IX (S³)**: ISOTROPIC ✓ YES (Brum-Them, Olbermann). ANISOTROPIC ✗ NO. INSPIRE 0 hits "Hadamard state"+"Bianchi IX". Bianchi IX is type A → BN23 variational setup transfers directly.
- **Mixmaster (BKL)**: ✗ NO papers. INSPIRE 0 hits. Existing Mixmaster QFT (1311.6004, 1501.02174) treats gravity quantization, not matter QFT on fixed Mixmaster background.

## 3. Best path forward + effort estimate

- **Bianchi IX anisotropic — MOST TRACTABLE, ~2-4 months.** Recipe: (i) Peter-Weyl on SU(2)≅S³ (Wigner D-matrices, λⱼ=j(j+2), degeneracy (j+1)²); (ii) Bianchi IX wave eq with mode-mixing C^a_bc; (iii) bSLE variational setup transfers verbatim from BN23 §2 (Bianchi A); (iv) Hadamard via Brum-Them §4.2 Sobolev WF-set bound + S³ Weyl law N(λ)~λ^(3/2)/6π². Single-author paper feasible. Title: "States of Low Energy on Bianchi IX spacetimes".
- **Bianchi V anisotropic — HARDER, ~3-5 months.** First do conformally-isotropic case via direct Brum-Them application. Then use Avetisyan-Verch 1212.6180 mode basis with type-B Lagrangian adaptation.
- **Mixmaster — out of scope.** Requires uniform estimates across Kasner bounces; new analytic tools needed.

## 4. Honest negative coverage

INSPIRE zero-hits: ("Hadamard state" + "Bianchi V"), ("Hadamard state" + "Bianchi IX"), ("Hadamard state" + "Mixmaster"), ("Hadamard state" + "open FRW"), ("Hadamard state" + "hyperbolic spatial"), ("Hadamard" + "Bianchi" + "homogeneous" + "cosmology"). Total INSPIRE corpus "Hadamard"+"Bianchi" = **5 papers** (only Bernard 1986 and BN23 are Bianchi-substantive). BN23 has only **4 INSPIRE citations**; **none** extend to Bianchi V or IX. **Banerjee-Niedermaier's own conclusions §6 explicitly flag the Bianchi V/IX extension as feasible — and 18 months later nobody has done it.**

## 5. Key recommendation

**Pursue Bianchi IX anisotropic SLE construction as direct sequel to arXiv:2305.11388.** ~2-4 months of focused work; closes BN23's own §6 future-work item AND T2-Bianchi IX gap simultaneously. Bianchi V residual gap then flagged as separate +3-5 months. Mixmaster gap honestly declared out of scope. Consider contacting Niedermaier (he flagged this as feasible) for sanity check / co-authorship.

**Files**: `/tmp/bianchi_hadamard_litsearch.md` (this) + `/tmp/bianchi_hadamard_litsearch.json` (machine-readable).
