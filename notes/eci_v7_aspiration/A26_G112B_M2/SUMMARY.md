# A26 — G1.12.B Milestone M2 (off-diagonal Y_u SVD at W1 τ*)

**Date:** 2026-05-05 mid-day
**Owner:** Sonnet sub-agent A26 (parent persisted)
**Hallu count entering / leaving:** 78 / 78 (held; no fabrications)

## Verdict

**M2 BINARY GATE PASS (5/5)**. Fit machine-zero to AHS targets at 1e-9% precision. M3 handoff complete.

## Inputs

- τ* = -0.1897 + 1.0034i (W1 verdict)
- LYD20 Model VI Eq. M_q6 (rows: weight 1, 2, 5)
- AHS GUT targets (arXiv:2510.01312, Antusch-Hinze-Saad NOT Wang-Zhang): y_t=0.4454, y_c/y_t=2.725e-3, y_u/y_c=2.05e-3

## Modular forms at τ*

Y_1 = 1.836 + 0.073i, Y_2 = -0.807 - 0.157i, Y_3 = 2.040 - 0.230i; constraint Y_1²+2Y_2Y_3 = 1e-15 (clean).

## Fit (α_u=1)

- **β_u/α_u = 152.42**
- **γ_u/α_u = 305.38**
- χ²_up (2 obs) = 6.7e-20 (machine zero — 2 params fit 2 obs exactly)
- α_u overall = 1.890e-6

## Singular values at GUT scale

- y_u = 2.488e-6
- y_c = 1.214e-3
- y_t = 4.454e-1
- **m_c/m_t = 2.725e-3 (Δ = -1e-9% vs AHS target)**
- m_u/m_c = 2.050e-3 likewise exact

## U_L (mass-ascending columns)

```
[ 0.201+0.980i   0.0038-0.0010i   ~1e-6           ]
[ 0.0036+0.0017i -0.360+0.933i   -0.0101+0.0016i  ]
[~1e-5           0.0032-0.0097i  -0.978+0.207i   ]
```

## U_R (mass-ascending columns)

```
[ 0.263          0.655          -0.709         ]
[-0.381+0.689i   0.441-0.335i    0.265-0.053i  ]
[-0.426+0.359i  -0.515+0.021i   -0.633+0.153i  ]
```

Unitarity: ||U_L U_L^† - I||_max = 4.6e-16, ||U_R U_R^† - I||_max = 2.2e-16, ||recon||_max = 6.9e-11.

## 5 Binary Gates

A. χ²_up < 1: PASS (6.7e-20). B. |Δy_c/y_t|<1%: PASS (1e-9%). C. U_L unitary: PASS (5e-16). D. U_R unitary: PASS (2e-16). E. SVD recon: PASS (7e-11).

## Handoff to M3

- `svd_results.json` contains M_u (α=1), U_L, U_R, all fit params — ready for Patel-Shukla Eq.(8) 1-loop matching
- M3 will need to also fit (β_d, γ_d1, γ_d2) at same τ* (W1 already did χ²_ckm=7.34) and combine with f^{ij}(τ*) from A22 for 45_H 1-loop correction
- Free params for M3: g_5 ~ 0.7 (α_5 ~ 1/40 at M_GUT = 2e16), M_T5, M_T45

## Files

- `m_u_svd.py` (17 KB, standalone)
- `svd_results.json` (3 KB, M3 handoff)
- `run.log` (4 KB)
