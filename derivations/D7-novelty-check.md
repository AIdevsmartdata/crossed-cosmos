# D7 Novelty Check — PPN bound and NMC Scherrer–Sen extension

Night session 2026-04-21. Method: WebFetch on arXiv abs/HTML pages; one paper per 3 s per
domain. Failed/partial fetches marked UNKNOWN. Cache: `paper/_novelty_cache/`.

## Claim (a): `γ−1 = −4 ξ² χ₀² / M_P²` + Cassini bound `|ξ_χ|(χ₀/M_P) ≲ 2.4×10⁻³`

| Ref | Verdict | Key finding |
|---|---|---|
| **Chiba 1999** (arXiv:gr-qc/9903094) | **MATCHES D7 (qualitatively)** | Abstract itself states "solar system experiments put a constraint on the non-minimal coupling: \|ξ\| ≲ 10⁻²" for the `ξRφ²` quintessence coupling. Full PPN derivation is in §II–III (we could not fetch the body; text tex not downloaded). This is the *original* paper for our bound. |
| **Damour–Esposito-Farèse 1993** (PRD 48, 3436) | **MATCHES framework** | Eq. (5.18) of DEF provides exactly the scalar–tensor PPN formula `γ−1 = −F'²/(ZF+(3/2)F'²)` that D7 applies. DEF does not specialise to `F=M_P²−ξχ²`; that substitution is straightforward. No DOI; cited inline. |
| **Faraoni 2000 review** (arXiv:gr-qc/0002091) | RELATED | Reviews NMC quintessence / inflation balance; no explicit PPN-gamma formula surfaced in abstract. UNKNOWN whether body re-derives γ−1. |
| **Boisseau–EF–Polarski–Starobinsky 2000** (arXiv:gr-qc/0001066) | RELATED, not same | Scalar–tensor reconstruction from dL(z); no PPN/Cassini derivation in abstract. |
| **Pettorino–Baccigalupi 2008** (arXiv:0802.1086) | RELATED, not same | Extended Quintessence Jordan/Einstein frames + perturbations; no explicit PPN γ bound in abstract. |
| **Wolf, García-García, Anton, Ferreira 2025** (arXiv:2504.07679, PRL 135, 081001) | **MATCHES D7 (numerically)** | Eq. (2): `F(φ) ≈ 1 − ξ(φ²/M_Pl²)`. Uses Cassini `γ_PPN−1 = (2.1±2.3)×10⁻⁵` → quotes `ξ(φ₀/M_Pl)² ≤ 6×10⁻⁶`. That is our Eq. (3.5.3) up to a factor of 4 from the `F'²` piece. Published April 2025, before our D7. **This is effectively our bound, with DESI DR2 already analysed.** |
| **Pan–Ye 2026** (arXiv:2503.19898) | RELATED, not same | DESI DR2 EFTofDE; does not quote PPN/Cassini bound. |
| **Ye et al. 2025** (arXiv:2407.15832) | RELATED, not same | DESI+NMC "thawing gravity"; Horndeski framework, no explicit `ξRχ²` PPN. |

## Claim (b): `wₐ = −A(1+w₀) + B·ξ·√(1+w₀)·(χ₀/M_P)`, `A(0.7)=1.58`, `B(0.7)=7.30`

| Ref | Verdict | Key finding |
|---|---|---|
| **Scherrer–Sen 2008** (arXiv:0712.3450, PRD 77, 083515) | **MATCHES zeroth order only** | Original `wₐ(w₀)` thawing track. `A(Ω_Λ)` and `A(0.7)≃1.58` are theirs. D7's `ξ=0` limit *is* their result. |
| **Wolf 2025** (2504.07679) | RELATED, not same | Numerical Bayesian fit; no analytic wₐ(w₀,ξ) formula. |
| **Pan–Ye 2026**, **Ye 2025** | RELATED, not same | Numerical / EFTofDE; no `(1+w₀)^{1/2}` first-order analytic expansion in ξ. |
| Literature search for "thawing Scherrer Sen non-minimal coupling wa" | **No direct hit found.** | The specific closed form (Eq. D7.2) with `B = (8/√3)A` scaling does **not** appear in the surveyed literature. Heuristic derivation (D4→Ω_Λ=0.7) is ours. |

## Verdict

**D7 = PARTIALLY RE-DERIVED.**

- Claim (a) **is essentially re-derivation** of Chiba 1999 (the bound) plus Wolf et al. 2025
  (the numerical Cassini → ξ(χ₀/M_P)² envelope, with DESI DR2). Our contribution is the
  compact sympy derivation and the explicit leading-order coefficient `4`. **The paper's
  original-claim framing must be softened.**
- Claim (b) **appears novel in its closed analytic form** (first-order ξ correction to
  Scherrer–Sen with `B(Ω_Λ) = (8/√3)A(Ω_Λ)` scaling). Not found in Scherrer–Sen 2008,
  Wolf 2025, Ye 2025, or Pan–Ye 2026 in the material we could reach. The heuristic
  `Ω_Λ` propagation is acknowledged as tentative already in the caveat.

## Refs not in `eci.bib` (flag for owner)

- `Chiba1999` — arXiv:gr-qc/9903094, PRL 82 (1999) 1836 — **REQUIRED citation for (a)**.
- `DamourEspositoFarese1993` — PRD 48, 3436 — already cited inline; would benefit from bib entry.
- Optional: `Faraoni2000` (gr-qc/0002091), `BoisseauEFPS2000` (gr-qc/0001066), `PettorinoBaccigalupi2008` (0802.1086) for completeness.

Wolf2025, ScherrerSen2008, PanYe2026, Ye2025, BertottiIessTortora2003 already present in `eci.bib`.
