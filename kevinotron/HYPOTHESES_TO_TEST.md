# Kevinotron — Hypotheses to Test
# Kévin Rémondière (ORCID 0009-0008-2443-7166)
# 2026-05-27

Based on 6 groups, 50+ data points, formula S₂/A = c·(β−|Φ⁺|) − log(β−1−|Φ⁺|) − C₂

## TIER 1 — Testable this week (existing Kevinotron, no new code)

### H1: SU(5) follows the formula exactly
- Predict: S₂/A(SU(5), β=15.0, L=4) = 5.86·(15−10) − log(15−1−10) − 5 = 29.3 − 1.39 − 5 = 22.9
- |Φ⁺| = 10, C₂ = 5
- Run: `kevinotron --group su5 --ls 4 --beta 15.0` (needs SU(5) impl, ~100 lines Rust)
- PASS if within 5% of 22.9. FAIL if >10% off.

### H2: Slope S₂/A/β converges to c = 5.86 at large β for ALL groups
- At β >> |Φ⁺|, the log and C₂ terms become subleading, slope → c
- Test: run G₂ at β=15,20,25 and check if slope approaches 5.86 from 1.80
- PASS if slope(β=25) > 4.0. FAIL if still < 2.5.

### H3: Area law coefficient at matched σa² is UNIVERSAL across Dynkin families
- Current data: SU(3)=14.17, Sp(4)=14.77, SO(7)=13.10 at σa²≈0.10
- Test: measure SU(2) at β where σa²≈0.10 (need β~2.2-2.3)
- PASS if SU(2) gives S₂/A = 13-15. FAIL if < 10 or > 18.

### H4: The −1 in log(β−1−|Φ⁺|) is the Lepage-Mackenzie tadpole
- Prediction: with tadpole-improved action (replace β → β_improved = β × ⟨P⟩), the −1 disappears
- Test: plot S₂/A vs β·⟨P⟩ − |Φ⁺| instead of β − |Φ⁺|. Should linearize better.
- PASS if R² improves from 0.997 to >0.999. FAIL if worse.

## TIER 2 — Testable this month (needs new code or longer runs)

### H5: FP adjoint d_s(G₂) ≠ covariant Laplacian d_s(G₂)
- Covariant Laplacian (fundamental) gives d_s = 5.1
- FP operator (adjoint, 14×14 per site) should give different d_s
- Build Ad(U) from stored configs → 7168×7168 matrix → GPU diag
- PASS if d_s(FP) < 4.0 (closer to 7/3 = 2.33). FAIL if d_s(FP) ≈ 5.

### H6: Per-gluon entropy S₂/(A·dim) at matched σa² approaches a constant for large groups
- Current: 2.41 (SU2), 1.77 (SU3), 1.45 (SU4), 1.31 (G₂)
- Prediction: S₂/(A·dim·σa²) → constant at large N (large-N factorization)
- Test: SU(5), SU(6) at matched σa²
- PASS if SU(5) per-gluon < SU(4) and trend saturates. FAIL if increases.

### H7: G₂ at matched σa² falls on the SAME curve as SU(N)
- G₂ at β=10.0 has σa²=0.131 (coarser than SU(3) at 0.103)
- Need G₂ at β≈12-13 for σa²≈0.10
- If S₂/A(G₂, σa²=0.10) ≈ 14 (= SU(3)), universality is total
- PASS if within ±10% of SU(3). FAIL if >20% different.

### H8: Creutz ratio σa²(β) follows two-loop asymptotic freedom for each group
- σa² = Λ² × f(g²) where f encodes the β-function
- Measure σa²(β) at 5+ β values per group → extract β-function
- Compare with perturbative b₀ = 11C₂/(48π²), b₁ = 34C₂²/(3·(16π²)²)
- PASS if 2-loop matches within 20% in scaling window. FAIL if qualitatively wrong.

## TIER 3 — Testable in 3 months (needs significant effort)

### H9: The formula predicts EE for ANY simple Lie group
- Untested groups: F₄ (dim=52, C₂=9, |Φ⁺|=24), E₆ (dim=78, C₂=12, |Φ⁺|=36)
- F₄ is the hardest: 26-dim fundamental rep, need full F₄ Metropolis code
- PASS if formula within 10% for F₄. Would be spectacular confirmation.

### H10: Adding fermions modifies the formula predictably
- With N_f quarks: |Φ⁺| → |Φ⁺| − N_f·T(R)/something
- The fermion contribution subtracts from the ghost sector
- Test: SU(3) with N_f=2 staggered fermions vs pure gauge
- PASS if the modification is proportional to N_f × C_2(fund)/C_2(adj).

### H11: The slope S₂/A/β predicts the deconfinement temperature
- At T_c, the system transitions from confined to deconfined
- Hypothesis: T_c ∝ 1/slope = β/(S₂/A) — slower slope = lower T_c
- G₂ has lowest slope (1.80) and known T_c/√σ ≈ 0.86 (Bruno 2015)
- SU(3) has higher slope (2.31) and T_c/√σ ≈ 0.63
- PASS if T_c/√σ correlates with 1/slope across 4+ groups.

### H12: Continuum limit — the formula structure survives a→0
- At β→∞: S₂/A → c·β (linear divergence, UV artifact)
- Physical quantity: S₂/A − c·β + c·|Φ⁺| = −log(β−1−|Φ⁺|) − C₂ → finite
- This combination should have a continuum limit
- Test: measure at β = 6, 6.5, 7, 7.5 for SU(3) and check convergence
- PASS if −log(β−1−3) − 3 converges. FAIL if diverges or oscillates.

## FALSIFICATION CRITERIA

The formula S₂/A = c·(β−|Φ⁺|) − log(β−1−|Φ⁺|) − C₂ is FALSIFIED if:
1. Any group gives S₂/A more than 15% off the prediction at same β
2. The log term has the wrong sign (S₂/A increases faster than linear in β)
3. SU(5) or F₄ deviate by more than 10%
4. The area law breaks (S₂/A not constant in L at fixed β)

## PRIORITY ORDER

H4 (tadpole improvement) → pure analysis, no new runs, immediate
H1 (SU(5)) → needs ~100 lines Rust, 1h run
H7 (G₂ matched) → 1 run at β=12-13
H2 (slope convergence) → 3 runs at high β
H5 (FP d_s) → JAX code ready, needs Ad(U) construction
H12 (continuum) → 4 runs SU(3) β-scan
