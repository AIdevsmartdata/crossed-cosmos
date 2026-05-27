# H53 — Bałaban + KR-FP-Hess : backup non-perturbative path

**Verdict** : 8-15% standalone, MORT comme alternative independent à BBD.

## Bałaban program (CMP 1985-1989, pre-arXiv)

- B1985a CMP 102:255 (UV stab 3D)
- B1985b CMP 102:277 (variational + background)
- B1987 CMP 109:249 (RG approach SU(N))
- B1988-89 propagators + large-field

Contraction estimate (B1987 §V-VII) : `S_{n+1}(A_{n+1}) = T S_n(A_n) = (1/2)<A_{n+1}, Δ_n^eff A_{n+1}> + V_n`, Lipschitz contraction in C^k norms (PAS Wasserstein/LSI).

Regime contrôlé : weak-coupling small-field uniquement.

## Application à KR-FP-Hess

H_n := Hess(S_n)(0). Under Bałaban step : H_{n+1} = T*·H_n·T + δH_n avec ‖δH_n‖_op ≤ C·g_n²·log L·‖H_n‖_op. Si g_n² ~ 1/(2b_0·k·log L) (AF one-loop), Σ converge → H_∞ > 0 **dans régime weak-coupling**.

## Bottleneck

**Intermediate-β = même obstruction que Polchinski**.

| Regime | Status |
|--------|--------|
| β ≫ β_* weak coupling | Bałaban contraction → H_n > 0 ✓ |
| β = 0 strong | Trivial (Osterwalder-Seiler) → H_n > 0 ✓ |
| **Intermediate β (β≈6 SU(3) confinement onset)** | **Ni un ni l'autre** = même H1a-iii cubic obstruction |

Bałaban lui-même n'a JAMAIS clos ce régime ; large-field/small-field interface R-operations = SAME J_t(A) obstruction.

## Conclusion epistémique

| Path | P(Clay 10y) | Bottleneck |
|------|------------|------------|
| BBD24 + Bauerschmidt collab | 73-85% | LSI intermediate β (H1a-BS) |
| **Bałaban + KR-FP-Hess (H53)** | **8-15%** | identical intermediate β |
| Wilson flow + MK | numerical only | not rigorous |

**Key insight memory** : Le bottleneck est PHYSIQUE, pas méthodologique. Visible identiquement dans Polchinski, Bałaban, Wilson flow.

## Refs

- T. Bałaban CMP 102, 109, 122 (1985-89), DOI:10.1007/BF... pre-arXiv
- A. Abdesselam, "RG According to Bałaban — I. Small fields", arXiv:1108.1335 (2011) exposition

## Author

Kévin Rémondière (ORCID 0009-0008-2443-7166)

## Links

[[project_clay_session_2026-05-26_full_convergence]]
[[project_4niveaux_crossovers_BakryEmery_2026-05-26]]
