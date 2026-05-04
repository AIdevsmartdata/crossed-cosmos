# POLISH REPORT — paper_lmfdb_s4prime.tex
**Date:** 2026-05-04  |  Days 3–7 polish pass

---

## 1. LMFDB Verification Table (live fetch 2026-05-04)

### 4.5.b.a
| Property | Paper claim | LMFDB live | Status |
|---|---|---|---|
| Level/Weight/Dim | 4/5/1 | 4/5/1 | CONFIRMED |
| CM | Q(i) | Q(√-1)=Q(i), inner twist 4.b | CONFIRMED |
| a(5), a(13), a(17), a(29), a(37) | -14, -238, +322, +82, +2162 | -14, -238, +322, +82, +2162 | CONFIRMED |
| Root number | "Fricke −1" (old) | **+1** (LMFDB L-fn page) | **CORRECTED** |

**q-expansion verbatim:** `q - 4q² + 16q⁴ - 14q⁵ - 64q⁸ + 81q⁹ + 56q¹⁰ - 238q¹³ + 256q¹⁶ + 322q¹⁷ - 324q¹⁸ - 224q²⁰ - 429q²⁵ + 952q²⁶ + 82q²⁹ + ... + 2162q³⁷ + ...`  
**Eta product:** `f(z) = η(z)⁴η(2z)²η(4z)⁴`

### 16.5.c.a
| Property | Paper | LMFDB live | Status |
|---|---|---|---|
| Level/Weight/Dim | 16/5/2 | 16/5/2 | CONFIRMED |
| Coeff field | Q(√-3) | Q(√-3), poly x²-x+1 | CONFIRMED |
| CM | not CM | not CM | CONFIRMED |
| 11 eigenvalues (p≤97) | Table 1 | all match | CONFIRMED |

**q-expansion verbatim (β=8√-3):** `q - βq³ + 18q⁵ + 2βq⁷ - 111q⁹ + 9βq¹¹ + 178q¹³ - 18βq¹⁵ - 126q¹⁷ ... - 1422q²⁹ ...`

---

## 2. Dimension Check (LMFDB live, no SageMath available)

- Level 4, weight 5: exactly **1 orbit** (4.5.b.a, dim=1). CONFIRMED.
- Level 16, weight 5: two orbits — **16.5.c.a** (dim=2, char 16.c) and 16.5.f.a (dim=14, char 16.f). Uniqueness of the dim-2 orbit in char 16.c confirmed.

---

## 3. Ŷ₃,₂(5) Re-derivation

**Result: NOTATION MISMATCH ONLY — no formula error.**

LYD20 (arXiv:2006.10722, verified live) uses basis Y₁,Y₂,Y₃ (not ε,θ) and labels the weight-5 triplet `Y^(5)_{3̂}` and `Y^(5)_{3̂',I/II}`. The paper's `Y_3̂,2^(5)` formula (eq. 3hat25) comes from NPP20 App D, reconstructed correctly in H2. The H2 Python formula:

```
comp[0] = (3/2)(εθ⁹ − 2ε⁵θ⁵ + ε⁹θ)
comp[1] = (√3/2)(−ε²θ⁸ + ε⁶θ⁴)
comp[2] = (√3/2)(−ε⁴θ⁶ + ε⁸θ²)
```

matches eq.(3hat25) exactly. **Section 3.1 stands.**

---

## 4. dMVP26 arXiv:2604.01422 Verification

**Authors (live):** Ivo de Medeiros Varzielas and Manuel Paiva (2 authors).  
**Title (live):** "Quark masses and mixing from Modular S'₄ with Canonical Kähler Effects"  
**Submitted:** 1 April 2026.  
**Original bibliography error:** Had listed Penedo and Petcov as co-authors, wrong title. **CORRECTED.**

---

## 5. Hostile-Reviewer Findings — Fixes Applied

| # | Severity | Issue | Fix |
|---|---|---|---|
| 1 | HIGH | Root number stated −1; LMFDB gives +1. For χ₄(−1)=−1, w₄²=−1 so w₄ is not an involution. | Changed to +1 in abstract, §3.1, corollary; added w₄²=−1 explanation. |
| 2 | HIGH | NPP20: 4 authors listed, wrong title, wrong journal | Corrected to 3 authors, "Double Cover of Modular S₄ for Flavour Model Building", Nucl. Phys. B 963 (2021) 115301. |
| 3 | HIGH | dMVP26: wrong authors (Penedo/Petcov), wrong title | Corrected to de Medeiros Varzielas + Paiva, correct title. |
| 4 | MEDIUM | LYD20 title wrong | Corrected to "Modular Invariant Quark and Lepton Models in Double Covering of S₄ Modular Group". |
| 5 | MEDIUM | Dim-1 assertion in Thm 1 proof lacked live-verify citation | Proof now cites LMFDB live search + classical formula. |
| 6 | LOW | Thm 3 lists Eisenstein hhat{3}(3) alongside cuspidal forms | No change; §5.4 already flags it; not mathematically wrong. |

---

## 6. BLMS Submission Readiness Checklist

| Item | Status |
|---|---|
| Both LMFDB labels live-verified (verbatim q-expansion) | ✓ |
| Root number corrected (+1) | ✓ |
| NPP20 / LYD20 / dMVP26 bibliography corrected | ✓ |
| All [NEEDS-LIVE-VERIFY] markers removed | ✓ |
| 14-prime 2̂(5) eigenvalues verified against LMFDB | ✓ |
| 5-prime 3̂,2(5) eigenvalues verified | ✓ |
| Sturm bounds stated and correct | ✓ |
| Page length (~9–10 pp amsart) ≤ 12 pp | ✓ |
| Zenodo DOI in cover letter | **Pending** — add once record created |
| BLMS instructions URL (lms.ac.uk / Wiley) | **Blocked** in session; use known limit ≤ 12 pp |
| Institutional affiliation | Optional — currently "Independent researcher" |
