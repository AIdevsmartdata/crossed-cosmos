---
name: M33 Pre-submission adversarial review (Opus 4.7, 6 min)
description: Brutal but valuable review of 7 papers. 3 NEEDS-MAJOR-REVISION + 4 MINOR-FIX. CRITICAL 10 future-dated arXiv IDs flagged for live-verify before any submission
type: project
---

# M33 — Pre-submission adversarial review (Opus 4.7, 6 min)

**Date:** 2026-05-06
**Owner:** Sub-agent M33 (Opus 4.7, max-effort independent reviewer)
**Hallu count entering / leaving:** 85 / 85 (M33 introduced 0 new fabrications; flagged 10 IDs for parent verification)

---

## Severity matrix (7 papers)

| # | Paper | Severity | Hostile risk |
|---|---|---|---|
| 1 | P-NT BLMS | NEEDS-MINOR-FIX | LOW |
| 2 | **v7.6 amendment** | **NEEDS-MAJOR-REVISION** | **HIGH** |
| 3 | ER=EPR LMP | NEEDS-MINOR-FIX | LOW-MED |
| 4 | Modular Shadow LMP v2.5 | NEEDS-MINOR-FIX | MED |
| 5 | Cardy LMP | NEEDS-MINOR-FIX | MED |
| 6 | **BEC LMP** | **NEEDS-MAJOR-REVISION** | **HIGH** |
| 7 | **Proton-decay PRD** | **NEEDS-MAJOR-REVISION** | **HIGH** |

**Net: 3-4 truly close (P-NT, ER=EPR, Modular Shadow + maybe Cardy); 3 not ready (v7.6, BEC, PRD).**

---

## 🚨 CRITICAL: 10 future-dated arXiv IDs to live-verify

Project memory pattern: 6+ historical fabrications. These 10 IDs are exactly the danger zone (LLMs hallucinate "near-real" 2024-2026 IDs).

| arXiv ID | Cited in | Topic |
|---|---|---|
| 2602.02675 | Modular Shadow + ER=EPR | Vardian Modular Krylov |
| 2603.01664 | Modular Shadow §6 | Solnyshkov polariton merger |
| 2604.02075 | BEC + Modular Shadow | Chandran-Fischer entanglement neg. |
| 2604.11277 | Modular Shadow §1 | Govindarajan-Sadanandan |
| 2604.01275 | Modular Shadow §1 | Benjamin-Fitzpatrick-Li-Thaler |
| 2604.16226 | v7.6 §2 | KSTD Karam-Palatini |
| 2604.01422 | P-NT + v7.6 + PRD | dMVP26 |
| 2604.13854 | v7.6 + paper-2 | Büyükboduk-Neamti |
| 2604.08449 | v7.6 §Q6 | Antusch-King-Wang DESI |
| 2603.18502 | PRD | Domingo DUNE |

**Single arXiv-API pass required before ANY external submission.**

---

## 3 MAJOR-REVISION issues

### v7.6 amendment: "not a paper, 25-page audit memo"
- 11 axioms, 4 grafts, 1 retraction (A46 99,061× χ²), smoke test cosmology with 3.1σ θ_MC bias
- Conjecture M13.1 §11 has 3 [TBD: prove] on load-bearing claims
- Sub-agent IDs (A22, M13, S5...) "Phase 3 Wave 12" peppered throughout = unprofessional
- **Recommendation**: SPLIT en 3 papers + Zenodo errata. NE PAS soumettre.
  1. P-NT companion (already separate)
  2. CSD(1+√6) leptogenesis short note (LMP, 6-8pp)
  3. Cassini-Palatini + KSTD reference (PRD, 4-6pp)
  4. Rest → Zenodo v6.0.54 amendment

### BEC LMP: "ECI internal note, NOT a paper"
- Title "Proposal Note, ECI v6.0.53"
- Author "ECI Collaboration internal note"
- §7 retraction v6.0.10 inside paper (incompatible with publication)
- KD Theorem 4 disambiguation = internal versioning leak
- **Recommendation**: merge §3-6 dans Modular Shadow §6 (4-5pp application section), discard scaffolding

### PRD: κ_u fine-tuning NOT owned + interference phase NOT disclosed
- M23 audit found B_Higgs = 1.077 (pas 2.06 parameter-free!)
- Lift to 2.06 requires constructive gauge-Higgs interference at M_T45 ≈ 10^14 GeV
- 1/4000 cancellation Y_5 ↔ Y_45 → "modular naturalness" appelé non-derived
- B-ratio range [0.98, 5.54] reflecting destructive vs constructive — to disclose
- **Recommendation**: disclose fine-tuning + interference phase honestly in abstract + §6

---

## 4 MINOR-FIX details

### P-NT BLMS
1. Add 3-line dim formula Cohen-Oesterlé giving dim S₅ⁿᵉʷ(Γ₀(4),χ₄) = 1
2. Remove A72 mention from abstract (off-topic for math.NT venue)
3. Live-verify dMVP26 arXiv:2604.01422

### ER=EPR LMP
1. Strengthen Prop 1 proof: 1 paragraph on spectral-measure decomposition for bounded-band sub-case
2. Live-verify Vardian arXiv:2602.02675
3. §6 explicit: Vardian 2026 = "AdS/CFT only"

### Modular Shadow LMP v2.5
1. Add 1 page to Appendix A.2 Step 2: explicit Mellin saddle / moment computation
2. Live-verify 5 future-dated IDs (Govindarajan-Sadanandan, Benjamin-Fitzpatrick-Li-Thaler especially)
3. §6 BEC caveat: "assuming BEC exterior phonon algebra admits finite-rank type-II_∞ truncation"

### Cardy LMP
1. Add 2 paragraphs to Theorem 2 proof: Virasoro mode-counting argument
2. Polariton ρ range "priority check before journal submission" must be verified or removed
3. Falsifier values (§6) inconsistency: clarify window vs ρ_∞ for each platform

---

## Action items (priority order)

### IMMEDIATE (before any arXiv upload)
1. **Live-verify the 10 future-dated arXiv IDs** — single curl pass, ~30 min
2. **Decide BEC paper fate**: merge into Modular Shadow §6 OR rewrite standalone
3. **PRD letter**: revise abstract + §6 to disclose κ_u fine-tuning + B-ratio range

### BEFORE journal submission
4. **v7.6 amendment**: split into 3 papers + Zenodo errata
5. **Cardy paper**: 2-paragraph Theorem 2 fix + polariton verification
6. **Modular Shadow**: 1-page Appendix A.2 Step 2 fix
7. **ER=EPR**: 1-paragraph Prop 1 fix
8. **P-NT BLMS**: 3-line dim formula + remove A72 from abstract

## Discipline

- Hallu count: 85 → 85 (M33 introduced 0 new fabrications; only flagged for parent verification)
- Mistral STRICT-BAN observed
- 7 paper reviews delivered as text (sub-agent protocol)
- 10 future-dated IDs flagged for verification (NOT fabricated by M33)
- NO drift to settings.json analysis despite skill injection

## Files in this directory
- `SUMMARY.md` — this file (consolidated review)

(Detailed per-paper reviews in M33's response are merged here for compactness;
expand to 7 separate files if needed for specific submission workflows.)
