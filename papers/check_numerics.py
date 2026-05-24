"""
Quick numerics check for the brief's claims.
"""
import math

kappa = 1/6
print(f"kappa = 1/6 = {kappa}")
print(f"1-kappa = 5/6 = {1-kappa}")
print(f"1+kappa = 7/6 = {1+kappa}")
print()

# Brief claim: 6pi/5 ~ (7/2)*sqrt(7/6) (diff 0.26%)
v1 = 6*math.pi/5
v2 = (7/2)*math.sqrt(7/6)
print(f"6pi/5 = {v1:.6f}")
print(f"(7/2)*sqrt(7/6) = {v2:.6f}")
print(f"Diff: {abs(v1-v2)/v1*100:.3f}%")
print()

# Brief claim: V_us = pi/14 ~ 2/(5*sqrt(pi)) (diff 0.57%)
v3 = math.pi/14
v4 = 2/(5*math.sqrt(math.pi))
print(f"pi/14 = {v3:.6f}")
print(f"2/(5*sqrt(pi)) = {v4:.6f}")
print(f"Diff: {abs(v3-v4)/v3*100:.3f}%")
print()

# V_us PDG ~ 0.2243
v_us_pdg = 0.2243
print(f"V_us PDG = {v_us_pdg}")
print(f"Dev from pi/14: {(v_us_pdg-v3)/v3*100:.3f}%")
print(f"Dev from 2/(5*sqrt(pi)): {(v_us_pdg-v4)/v4*100:.3f}%")
print()

# delta_CP/(2pi)
delta_cp = 177  # degrees, NuFit
delta_cp_rad = math.radians(delta_cp)
print(f"delta_CP/(2pi) = {delta_cp_rad/(2*math.pi):.5f}")
print(f"pi/14 = {math.pi/14:.5f}")
print(f"Brief claim delta_CP/(2pi) ~ pi/14: needs check")
print(f"delta_CP = 177 deg = {delta_cp_rad:.4f} rad = {delta_cp_rad/math.pi:.4f}*pi")
print(f"So delta_CP/(2pi) = {delta_cp_rad/(2*math.pi):.4f}; pi/14 = {math.pi/14:.4f}")
print(f"These are NOT equal numerically. Likely brief means delta_CP ~ 59*pi/60.")
print()

# pi/14 in degrees
print(f"pi/14 rad = {math.degrees(math.pi/14):.2f} deg")
print(f"  This is the angle, not delta_CP/2pi.")
print()

# 59pi/60 in degrees
print(f"59pi/60 = {59*math.pi/60:.4f} rad = {math.degrees(59*math.pi/60):.2f} deg")
print(f"Per T2.9: delta_CP = 177deg = 59pi/60. Brief says pi/14. These differ.")
print(f"pi/14 / 2pi = 1/28")
print()

# Number of cusps of Gamma_0(N): for prime p, it's 2 (cusps 0 and infty)
# For X_0(7): genus 0, 2 cusps
# Brief: V_us = pi/(2N) with N=7 gives pi/14 ~ V_us via "half-cusp loop"

print("="*60)
print("Pattern exponent census")
print("="*60)

# Patterns from synthesis + PAPER_KOIDE + PAPER_PI_KAPPA_HADRONIC

patterns = [
    # (label, value, formula_form, (a,b,c,d, rat))
    # Koide
    ("K_charged_leptons", 2/3, "4*kappa", (1, 0, 0, 0, 4)),
    ("K_up_quarks", 5/6, "1-kappa", (0, 1, 0, 0, 1)),
    ("K_neutrinos_NH", 7/12, "(1+kappa)/2", (0, 0, 1, 0, 1/2)),
    # T1
    ("alpha_LSI", 5/6, "1-kappa", (0, 1, 0, 0, 1)),
    ("y_t", 1/math.sqrt(2), "1/sqrt(2)", (0, 0, 0, 0, 1/math.sqrt(2))),  # OUTSIDE template
    ("lambda_H", 1/8, "1/8", (0, 0, 0, 0, 1/8)),  # OUTSIDE template
    ("sigma_8", math.sqrt(2/3), "sqrt(2/3)", (1/2, 0, 0, 0, 2)),  # = sqrt(4*kappa) = 2*sqrt(kappa)
    # n_s, delta_CP
    ("n_s", 0.9648, "1-kappa/4.7", None),  # NOT in template
    ("delta_CP/pi", 59/60, "59/60", None),  # NOT in template
    # Glueballs
    ("m_2++/m_0++", math.sqrt(2), "sqrt(2)", (0, 0, 0, 0, math.sqrt(2))),  # outside template (irrational rat)
    ("m_0-+/m_0++", 3/2, "3/2", (0, 0, 0, 0, 3/2)),
    # PI_KAPPA_HADRONIC
    ("m_p/Lambda_Nf0", 6*math.pi/5, "pi/(1-kappa)", (0, -1, 0, 1, 1)),
    ("m_p/cond^1/3", 6*math.pi/5, "pi/(1-kappa)", (0, -1, 0, 1, 1)),
    ("|mu_Sigma+/mu_Xi-|", 3.7775, "pi/(1-kappa)", (0, -1, 0, 1, 1)),
    ("V_ud", 35/36, "1-kappa^2", (0, 0, 0, 0, 35/36)),  # = (1-k)(1+k)*1 → b=1,c=1,rat=1? No: = 1-k^2 NOT factored
    # Note: (1-k)(1+k) = (5/6)(7/6) = 35/36 ✓✓✓ exponent (b=1, c=1)
    # Brief conjectures
    ("V_us_predict", math.pi/14, "pi/14 = pi/(2N) with N=7", None),
    # T2.9
    ("Xi^0/p", (1+1/6)/(1-1/6), "(1+k)/(1-k)=7/5", (0, -1, 1, 0, 1)),
]

print(f"{'label':<25} {'value':>10} {'formula':<28} {'(a,b,c,d,r)'}")
for label, val, formula, exps in patterns:
    if exps:
        a, b, c, d, r = exps
        pred = (1/6)**a * (5/6)**b * (7/6)**c * math.pi**d * r
        dev = (val-pred)/pred*100 if pred != 0 else float('nan')
        match = "PRED" if abs(dev)<0.5 else "?"
    else:
        pred = None
        match = "outside template"
    print(f"{label:<25} {val:>10.5f} {formula:<28} {exps}")

# V_ud check
print()
print(f"(1-k)(1+k) = {(5/6)*(7/6):.5f} = 35/36 = {35/36:.5f}")
print(f"So V_ud = (1-k)(1+k) = b=1, c=1, a=d=0, rat=1: (0,1,1,0,1)")
print()
print(f"sigma_8 = sqrt(2/3) = {math.sqrt(2/3):.5f}")
print(f"  = sqrt(4*kappa) = 2*sqrt(kappa): (1/2, 0, 0, 0, 2)")
print()
# x = 2*sqrt(kappa) with k=1/6 -> 2/sqrt(6) = sqrt(4/6) = sqrt(2/3) ✓
