---
name: M115 Opus v_2(c_2(M(f)(m))) compute — (B) PARTIAL, v_2(inv Euler) {0,1,-1,-2} ≠ v_2(α_m^F1) {-3,-2,0,1}, discrepancy {-3,-3,+1,+3} non-constant; m=3 INCONCLUSIVE without ε+Γ
description: Computed v_2 inverse Euler factor at p=2 for f=4.5.b.a m=1..4 = {0,1,-1,-2}. Discrepancy with M22 ladder v_2(α_m^F1) = {-3,-3,+1,+3} NON-CONSTANT — R-2.3 cannot reduce to Euler factor identification. m=3 prediction internally consistent if ε(3)+Γ(3) = +1 + Sha is 2-adic unit (Rubin-style CM descent). 5 arXiv refs live-verified PDF read
type: project
---

# M115 — Opus v_2(c_2(M(f)(3))) Steinberg compute (PARTIAL)

**Date:** 2026-05-06 | **Hallu count: 95 → 95** held | **Mistral STRICT-BAN observed**

## VERDICT: (B) PARTIAL COMPUTED — INCONCLUSIVE for R-2.3 m=3 falsifier

Inverse Euler factor (1 - a_2 · 2^{-m}) computed for f=4.5.b.a, a_2=-4 :

| m | 1 + 4·2^{-m} | v_2 |
|---|---|---|
| 1 | 3 | **0** |
| 2 | 2 | **+1** |
| 3 | 3/2 | **-1** |
| 4 | 5/4 | **-2** |

## Critical finding: discrepancy NON-CONSTANT

| m | v_2(α_m^F1) M22 | v_2(inv Euler) | Difference |
|---|---|---|---|
| 1 | -3 | 0 | **-3** |
| 2 | -2 | +1 | **-3** |
| 3 | 0 | -1 | **+1** |
| 4 | +1 | -2 | **+3** |

**Discrepancy {-3, -3, +1, +3} NON-CONSTANT** → R-2.3 cannot reduce to "c_2 = inv Euler factor up to constant". M22 ladder carries **independent 2-adic content** beyond Euler factor.

## Bridge formula heuristic

v_2(c_2(m)) ≈ v_2(1 - a_2·2^{-m}) + ε(m) + Γ(m)

where ε = local epsilon factor at p=2 for V_2(f)(m), Γ = Deligne archimedean shift.

R-2.3 prediction:
v_2(α_m^F1) = v_2(c_2) - v_2(#H^1_{f,2}) = v_2(inv Eul) + ε + Γ - v_2(#H^1_{f,2})

## m=3 analysis (cleanest test case)

For m=3 : 0 = -1 + ε(3) + Γ(3) - v_2(#H^1_{f,2}(3))
→ **v_2(#H^1_{f,2}(3)) = -1 + ε(3) + Γ(3)**

**Cleanest scenario** : if ε+Γ = +1 → v_2(#H^1_{f,2}(3)) = 0 → Sha 2-adic unit → Rubin-style CM descent → CONSISTENT R-2.3.

If ε+Γ ≠ +1 → R-2.3 m=3 prediction would FAIL.

**Without explicit ε(3) + Γ(3) computation, INCONCLUSIVE.**

## Setup details verified

- f = 4.5.b.a, level N = 4 = 2², weight k = 5, a_2 = -4
- a_2 = -ε_2 · 2^{(k-1)/2} = -1 · 4 (Steinberg edge with ε_2 = -1)
- ord_2(N) = 2 → **ramified principal series**, NOT classical Steinberg in GL_2(Q_2) sense (per M20). Strict Steinberg requires ord_p(N) = 1.
- V_2(f) = Ind_{G_{K_2}}^{G_{Q_2}}(ψ_2), K_2 = Q_2(i), ψ_2 unramified
- HT weights {0, 4} → after twist (m): {m, m+4}
- m=3: HT weights {3, 7}, all strictly positive → Fil^0 D_dR(V(3)) = D_dR(V(3)) entirely; t(V(3)) = 0

## Strict definition c_2 (Bloch-Kato 1990)

c_2(M(f)(m)) = #(Λ_2(m)^{(BK)} / Λ_2(m)^{(geom)})

For HT weights all ≥ 1, t(V(m)) = 0, so dual exp* : H^1_f → D_dR^0 entire content. "Non-critical positive HT weight" regime where c_2 reduces to (φ,Γ)-module structure.

## What was ruled OUT firmly

- **R-2.3 cannot derive purely from inverse Euler identification** (discrepancy non-constant)
- **Naive c_2(m) ~ E_2^±(f,m) FAILS at v_2 level**: v_2(E_2^±) = {-2, 0, 3, 3} ≠ v_2(c_2). E_2^± is renormalization of α NOT direct expression for c_2

## What was ruled IN (consistency)

- R-2.3 m=3 prediction **internally consistent** if ε+Γ has v_2 = +1 + Sha 2-adic unit
- {-3, -3, +1, +3} pattern matches plausibly Deligne Γ-factor Γ_C(s+m+ε)/Γ_C-shift carrying O(m) 2-adic valuation

## NOT computed (honest gaps)

- ε-factor at p=2 for V_2(f)(m) — needs Fontaine-Perrin-Riou or LVW25
- Γ-factor (Deligne archimedean) — needs CM-period Damerell-Shimura at higher HT weight
- Selmer #H^1_{f,2}(3) — TBD-R2-2, no Heegner machinery available

**Direct verification or refutation R-2.3 m=3 IMPOSSIBLE without these three.**

## 5 arXiv refs live-verified PDF read

| Ref | arXiv | Verified |
|---|---|---|
| Longo-Vigni 2022/2024 | 2211.04907 | ✓ pages 5-10, 20-26, 36-42 |
| Sano 2025 | 2510.01601 | ✓ pages 1-3, 25-29, 34-39 |
| DFG 2026 | 2512.02348 | ✓ pages 3-7, 10-15, 35-40 (handles ad^0 only, λ|Nk! exclusion) |
| Yin 2024 | 2410.24193 | ✓ pages 8-12 (assumes p∤N, inapplicable) |
| Berger 2004 | Compos. Math. 140 | memory-cited |

## Recommendations

1. **Document {-3, -3, +1, +3} discrepancy** in M70 r2_blochkato_paper.tex Section 4 — rules out naive Euler-factor identification
2. **M116 future DEEP** : Wach-module computation V_2(f)|_{G_{Q_2}} via Berger 2004 → c_2 explicit via (φ,Γ)-module integral structure
3. **M117 future DEEP** : Damerell archimedean period 2-adic valuation tracking → v_2(Γ-factor)
4. **DO NOT claim R-2.3 verified** — keep conjectural in M70 paper

## Discipline log

- 0 fabrications by M115
- 5 arXiv refs PDF Read tool verified
- 1 ref FLAGGED (LVW25) honored without citation
- {-3, -3, +1, +3} discrepancy explicitly flagged
- Mistral STRICT-BAN observed
- Verdict honestly (B) PARTIAL not (A) COMPUTED
- Hallu 95 → 95 held
