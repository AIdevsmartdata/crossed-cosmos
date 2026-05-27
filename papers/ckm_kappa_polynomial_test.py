#!/usr/bin/env python3
"""Test : les éléments CKM matchent-ils des polynômes simples en κ ?
Hypothèse DS Bot : amplitudes de transition = polynomes en κ sans π."""
import math

kappa = 1/6
alpha = 5/6  # 1-κ
pi_const = math.pi

# CKM PDG 2024
ckm = {
    "V_ud": (0.97370, 0.00014),
    "V_us": (0.22501, 0.00068),
    "V_ub": (0.00377, 0.00020),
    "V_cd": (0.22487, 0.00068),
    "V_cs": (0.97320, 0.00011),
    "V_cb": (0.04183, 0.00079),
    "V_td": (0.00876, 0.00018),
    "V_ts": (0.04117, 0.00074),
    "V_tb": (0.99911, 0.00007),
}

# Wolfenstein parametrization : V_us ≈ λ, V_cb ≈ Aλ², V_ub ≈ Aλ³(ρ-iη)

# Build candidate κ-polynomials (NO π, only κ + integers)
candidates = []
# Linear
candidates.append(("κ", kappa))                  # 0.1667
candidates.append(("1-κ", 1-kappa))              # 0.8333
candidates.append(("κ²", kappa**2))              # 0.0278
candidates.append(("1-κ²", 1-kappa**2))          # 0.9722
candidates.append(("κ³", kappa**3))              # 0.00463
candidates.append(("1-κ³", 1-kappa**3))          # 0.99537
candidates.append(("κ⁴", kappa**4))              # 0.000772
candidates.append(("(1-κ)²", (1-kappa)**2))      # 0.6944
candidates.append(("(1-κ)³", (1-kappa)**3))      # 0.5787
candidates.append(("(1-κ)⁴", (1-kappa)**4))      # 0.4823
# √κ and √(1-κ)
candidates.append(("√κ", math.sqrt(kappa)))      # 0.4082
candidates.append(("√(1-κ)", math.sqrt(1-kappa)))# 0.9129
candidates.append(("κ·(1-κ)", kappa*(1-kappa)))  # 5/36 = 0.1389
candidates.append(("(1-κ)/κ", (1-kappa)/kappa))  # 5
candidates.append(("κ/(1-κ)", kappa/(1-kappa)))  # 1/5 = 0.2
candidates.append(("(1-κ)·κ²", (1-kappa)*kappa**2))  # 5·κ²/6
candidates.append(("(1-κ)·κ³", (1-kappa)*kappa**3))  # = 5/(6·216) = 5/1296 ≈ 0.00386
candidates.append(("κ·(1-κ)²", kappa*(1-kappa)**2))  # κ·(5/6)²
candidates.append(("κ²·(1-κ)²", kappa**2*(1-kappa)**2))
candidates.append(("3κ²/2", 1.5*kappa**2))       # 3/2·(1/36) = 1/24 = 0.04167
candidates.append(("2κ²", 2*kappa**2))           # 2/36 = 1/18
candidates.append(("κ²/2", 0.5*kappa**2))
candidates.append(("3κ²", 3*kappa**2))           # 3/36 = 1/12
candidates.append(("κ²·3/2 = 1/24", kappa**2 * 3/2))
candidates.append(("√(2)·κ", math.sqrt(2)*kappa))  # = 0.2357
candidates.append(("√(2κ)", math.sqrt(2*kappa)))   # = √(1/3) = 0.5774
candidates.append(("√(3κ)/2", math.sqrt(3*kappa)/2))  # = √(1/2)/2 = 1/(2√2)
candidates.append(("κ + κ²", kappa + kappa**2))     # 7/36 = 0.1944
candidates.append(("2κ", 2*kappa))                  # 1/3
candidates.append(("3κ/2", 1.5*kappa))              # 1/4 = 0.25
candidates.append(("4κ²", 4*kappa**2))              # 4/36 = 1/9
candidates.append(("κ + κ³", kappa + kappa**3))
candidates.append(("3(1-κ)²/2", 1.5*(1-kappa)**2))
candidates.append(("√(7/8)·(1-κ)", math.sqrt(7/8)*(1-kappa)))
candidates.append(("(1-κ)·√(1-κ)", (1-kappa)**1.5))
candidates.append(("1/√(1+κ)", 1/math.sqrt(1+kappa)))
candidates.append(("(1+κ²)/2", (1+kappa**2)/2))
candidates.append(("(1+κ)/2", (1+kappa)/2))
# Some with √
candidates.append(("√(1-κ²)", math.sqrt(1-kappa**2)))  # √(35/36)
candidates.append(("√((1-κ)/(1+κ))", math.sqrt((1-kappa)/(1+kappa))))
candidates.append(("κ·(1+κ)", kappa*(1+kappa)))   # = 7/36

# Dedupe
seen = set()
candidates_dedupe = []
for n, v in candidates:
    key = round(v, 5)
    if key not in seen:
        seen.add(key)
        candidates_dedupe.append((n, v))
candidates = candidates_dedupe

print(f"Candidates κ-polynomes : {len(candidates)}")

# Test each CKM element
print(f"\n{'CKM':>8} {'mesuré':>12} {'err':>10} {'Best κ formula':>30} {'pred':>12} {'σ_match':>10} {'rel %':>8}")
print("-"*100)
results = []
for name, (val, err) in ckm.items():
    best = (float('inf'), None, 0)
    for cn, cv in candidates:
        if cv <= 0:
            continue
        diff = abs(val - cv)
        rel = diff / val * 100
        sigma = diff / err
        if rel < best[0]:
            best = (rel, cn, cv)
    sigma_match = abs(val - best[2]) / err
    print(f"{name:>8} {val:>12.5f} {err:>10.5f} {best[1]:>30} {best[2]:>12.5f} {sigma_match:>9.2f}σ {best[0]:>7.2f}%")
    results.append((name, val, err, best[1], best[2], sigma_match, best[0]))

# Specific high-precision tests
print("\n" + "="*78)
print("SPECIFIC TESTS")
print("="*78)

# V_ud = 1 - κ² ?
v_ud_pred = 1 - kappa**2
v_ud_obs = ckm["V_ud"][0]
v_ud_err = ckm["V_ud"][1]
print(f"\nV_ud = 1 - κ² = 35/36 = {v_ud_pred:.5f}")
print(f"V_ud obs = {v_ud_obs:.5f} ± {v_ud_err:.5f}")
print(f"σ match = {abs(v_ud_obs - v_ud_pred)/v_ud_err:.2f}σ")
print(f"rel diff = {abs(v_ud_obs - v_ud_pred)/v_ud_obs*100:.3f}%")

# V_cb = 3κ²/2 = 1/24 ?
v_cb_pred = 1/24
v_cb_obs = ckm["V_cb"][0]
v_cb_err = ckm["V_cb"][1]
print(f"\nV_cb = 3κ²/2 = 1/24 = {v_cb_pred:.5f}")
print(f"V_cb obs = {v_cb_obs:.5f} ± {v_cb_err:.5f}")
print(f"σ match = {abs(v_cb_obs - v_cb_pred)/v_cb_err:.2f}σ")
print(f"rel diff = {abs(v_cb_obs - v_cb_pred)/v_cb_obs*100:.3f}%")

# V_ub = (1-κ)·κ³ = 5/1296 ?
v_ub_pred = (1-kappa)*kappa**3
v_ub_obs = ckm["V_ub"][0]
v_ub_err = ckm["V_ub"][1]
print(f"\nV_ub = (1-κ)·κ³ = 5/1296 = {v_ub_pred:.5f}")
print(f"V_ub obs = {v_ub_obs:.5f} ± {v_ub_err:.5f}")
print(f"σ match = {abs(v_ub_obs - v_ub_pred)/v_ub_err:.2f}σ")
print(f"rel diff = {abs(v_ub_obs - v_ub_pred)/v_ub_obs*100:.3f}%")

# V_us = √2·κ = √2/6 ?
v_us_pred = math.sqrt(2)*kappa
v_us_obs = ckm["V_us"][0]
v_us_err = ckm["V_us"][1]
print(f"\nV_us = √2·κ = √2/6 = {v_us_pred:.5f}")
print(f"V_us obs = {v_us_obs:.5f} ± {v_us_err:.5f}")
print(f"σ match = {abs(v_us_obs - v_us_pred)/v_us_err:.2f}σ")
print(f"rel diff = {abs(v_us_obs - v_us_pred)/v_us_obs*100:.3f}%")

# Unitarité : V_ud² + V_us² + V_ub² = 1 ?
sum_sq_row1 = v_ud_obs**2 + v_us_obs**2 + v_ub_obs**2
print(f"\nUnitarité ligne 1 : V_ud² + V_us² + V_ub² = {sum_sq_row1:.6f} (devrait être 1)")
print(f"Déviation : {(1-sum_sq_row1)*1e3:.3f} × 10⁻³ (Cabibbo anomaly known)")

# Test : V_ud² + (√2·κ)² + V_ub² = (1-κ²)² + 2κ² + κ⁶(1-κ)²
# = 1 - 2κ² + κ⁴ + 2κ² + κ⁶(1-κ)²
# = 1 + κ⁴ + κ⁶(1-κ)²
# = 1 + 1/1296 + 25/(1296·216) ≈ 1.000783
# Not 1 exactly !
# Predicted deviation : 7.8e-4
pred_unitarity_def = kappa**4 + kappa**6*(1-kappa)**2
print(f"\nPrédiction unitarité (avec V_us=√2κ, V_ub=κ³(1-κ)) :")
print(f"  Δ(unitarity) = κ⁴ + κ⁶(1-κ)² = {pred_unitarity_def:.6e}")
print(f"  Observé Cabibbo anomaly : {1-sum_sq_row1:.6e}")

# ===========================================================
# PMNS angles test
# ===========================================================
print("\n" + "="*78)
print("PMNS MIXING ANGLES")
print("="*78)

# PDG 2024 PMNS (sin² of mixing angles)
pmns = {
    "sin²θ12_pmns": (0.307, 0.013),
    "sin²θ23_pmns": (0.561, 0.020),
    "sin²θ13_pmns": (0.022, 0.0007),
    "δ_CP_PMNS / (2π)": (197/360, 27/360),  # in units of 2π
}

print(f"\n{'Mixing':>20} {'mesuré':>12} {'err':>10} {'Best κ':>25} {'pred':>10} {'%':>8}")
print("-"*85)
for name, (val, err) in pmns.items():
    best = (float('inf'), None, 0)
    for cn, cv in candidates:
        if cv <= 0:
            continue
        diff = abs(val - cv)
        rel = diff / val * 100
        if rel < best[0]:
            best = (rel, cn, cv)
    print(f"{name:>20} {val:>12.5f} {err:>10.5f} {best[1]:>25} {best[2]:>10.5f} {best[0]:>7.2f}%")

# Specific : sin²θ12 ≈ (1-κ)/3 = 5/18 ≈ 0.278? observed 0.307 → 9% off
# sin²θ23 ≈ κ·π²/3 = 0.548? observed 0.561 → 2.4%
# sin²θ13 ≈ κ² = 0.028? observed 0.022 → 26% off

print(f"\n=== Compact summary ===")
print(f"\nCKM matches (κ-polynomes only, no π) :")
print(f"  V_ud = 1 - κ²            : {abs(0.97370 - (1-1/36))/0.97370*100:.3f}% (0.15%)")
print(f"  V_cs = 1 - κ²            : {abs(0.97320 - (1-1/36))/0.97320*100:.3f}% (0.10%)")
print(f"  V_tb = 1 - κ⁶ ?          : {abs(0.99911 - (1-kappa**6))/0.99911*100:.3f}% (test)")
v_tb_pred = 1 - kappa**6
print(f"    V_tb = 1 - κ⁶ = 1 - 1/46656 = {v_tb_pred:.7f}")
print(f"    V_tb obs = 0.99911, diff = {abs(0.99911 - v_tb_pred)*100:.4f}% (in %)")
print(f"  V_us = √2·κ              : {abs(0.22501 - math.sqrt(2)/6)/0.22501*100:.3f}% (5.4%)")
print(f"  V_cd = √2·κ              : {abs(0.22487 - math.sqrt(2)/6)/0.22487*100:.3f}% (5.5%)")
print(f"  V_cb = 3κ²/2 = 1/24      : {abs(0.04183 - 1/24)/0.04183*100:.3f}% (0.39%)")
print(f"  V_ts = 3κ²/2 = 1/24      : {abs(0.04117 - 1/24)/0.04117*100:.3f}% (1.20%)")
print(f"  V_ub = κ³(1-κ) = 5/1296  : {abs(0.00377 - 5/1296)/0.00377*100:.3f}% (2.3%)")
print(f"  V_td = ? near κ³(1-κ)·... :")

# Try V_td
v_td_obs = 0.00876
for cn, cv in candidates:
    if abs(v_td_obs - cv)/v_td_obs < 0.05 and cv > 0:
        print(f"    V_td = {cn} : {cv:.5f}, diff {abs(v_td_obs-cv)/v_td_obs*100:.3f}%")
        break

# Try π hybrid for V_us
print(f"\n=== Maybe V_us needs π factor after all ===")
print(f"V_us = π/14 = {math.pi/14:.5f}, diff {abs(0.22501 - math.pi/14)/0.22501*100:.3f}%")
print(f"V_us = 2κ·√(7/4) = {2*kappa*math.sqrt(7/4):.5f}")
print(f"V_us = κ + κ² + κ³ = {kappa+kappa**2+kappa**3:.5f}")
print(f"V_us = 4κ/3 = {4*kappa/3:.5f}, diff {abs(0.22501 - 4*kappa/3)/0.22501*100:.3f}%")

# Cabibbo angle in radians : V_us = sin(θ_C), θ_C ≈ 13°
print(f"\nθ_C = arcsin(V_us) = {math.degrees(math.asin(0.22501)):.3f}° = {math.asin(0.22501):.5f} rad")
print(f"θ_C / π = {math.asin(0.22501)/math.pi:.5f}, candidate 1/14 = {1/14:.5f}, diff {abs(math.asin(0.22501)/math.pi - 1/14)*100:.3f}")
print(f"Or θ_C = κ·... ?")

print("\nDONE.")
