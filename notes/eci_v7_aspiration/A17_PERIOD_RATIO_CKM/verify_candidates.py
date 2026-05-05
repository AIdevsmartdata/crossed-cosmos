"""Verify the two clean candidates from the strict screen."""
from mpmath import mp, mpf, sqrt
mp.dps = 60

# Candidate 1: |V_us| = 9/40 (from m=1 ladder * 9/4)
v_us = mpf("0.22500")
ratio = mpf(9)/mpf(40)
print(f"Candidate 1: |V_us| ?= 9/40")
print(f"  9/40            = {ratio}")
print(f"  |V_us| (PDG)    = {v_us}")
print(f"  rel err         = {float(abs(ratio - v_us)/v_us * 100)}%")
print(f"  PDG quoted error: 0.7%")
print()

# Candidate 2: |V_cb|^2 = 1/600 (from m=4 ladder * 1/10)
v_cb2 = mpf("0.001668")
ratio2 = mpf(1)/mpf(600)
print(f"Candidate 2: |V_cb|^2 ?= 1/600")
print(f"  1/600           = {ratio2}")
print(f"  |V_cb|^2 (HFLAV)= {v_cb2}")
print(f"  rel err         = {float(abs(ratio2 - v_cb2)/v_cb2 * 100)}%")
print(f"  HFLAV error: ±3.4% (0.140 on 4.085 -> ±0.000282 on |V_cb|^2)")
print()

# Equivalent: |V_cb| = sqrt(1/600)
v_cb_pred = sqrt(mpf(1)/600)
print(f"  Equivalently |V_cb| = sqrt(1/600)")
print(f"  sqrt(1/600)     = {v_cb_pred}")
print(f"  |V_cb| (HFLAV)  = 0.04085 ± 0.0007")
print(f"  rel err         = {float(abs(v_cb_pred - mpf(0.04085))/mpf(0.04085) * 100)}%")
print()

# Structural meaning:
# 1/600 = (1/60) * (1/10) = ladder(m=4) * ladder(m=1)
print("Structural decomposition:")
print(f"  1/600 = 1/60 * 1/10")
print(f"        = L(f,4)/Omega_K^4 * 10 * L(f,1)*pi^3/Omega_K^4 / 10")
print(f"        = L(f,1)*L(f,4) * pi^3 / Omega_K^8 (WITH 10 factor needed)")
print()

# Try another decomposition: 1/600 = 1/(60·10) and also 1/(24·25)
# Group-theoretic: 60 = |A_5|, 10 = |dihedral(5)| order or "5 fingers"
print("Number-theoretic note on 1/600:")
print(f"  600 = 2^3 * 3 * 5^2 = 24 * 25 = 60 * 10 = 120 * 5 = 200 * 3")
print(f"  600 = |2 x S_5|/2 not standard. |S_5| = 120, |A_5| = 60.")
print(f"  600 = order of binary icosahedral times 5? |2I| = 120 — no.")
print()

# Look at the m=2 alternative: q=11/18 -> sin^2_thetaC ~0.45% - that's at the 0.5% boundary.
# The cleaner one: m=2, q=2/19 -> |V_ub/V_cb|^2 0.365% — not clean either.
# The really clean ones are |V_us| = 9/40 (0.000%) and |V_cb|^2 = 1/600 (0.080%).
print("CLEAN HITS at K=Q(i) Damerell ladder a=4:")
print("  m=1 (1/10):     |V_us|     = 9/4 * 1/10 = 9/40     (rel err 0.000% vs PDG 0.225)")
print("  m=4 (1/60):     |V_cb|^2   = 1/10 * 1/60 = 1/600   (rel err 0.080% vs HFLAV)")
print()
print("Combined:        |V_us|^2 * |V_cb|^2 = 81/1600 * 1/600 = 81/960000")
print(f"                                  = {float(mpf(81)/mpf(960000))}")
print()

# Belle II 2027 |V_cb| target: 0.5% precision -> |V_cb| = 0.04085 ± 0.0002
# Our prediction: |V_cb| = sqrt(1/600) = 0.04082...
v_cb_belle = mpf("0.04085")
v_cb_err_belle = mpf("0.000204")  # 0.5%
print(f"Belle II 2027 prediction (PDG-anchored): |V_cb| = {v_cb_belle} ± {v_cb_err_belle}")
print(f"  ECI-Q(i) prediction: |V_cb| = sqrt(1/600) = {v_cb_pred}")
diff_sigma = abs(v_cb_pred - v_cb_belle) / v_cb_err_belle
print(f"  Distance: |delta| / sigma_Belle = {float(diff_sigma):.3f} sigma")
print(f"  -> {'WITHIN 1-sigma; experiment cannot distinguish' if diff_sigma < 1 else 'TESTABLE at >1 sigma'}")

# More interesting decomposition: |V_us| = 9/40
# 9/40 = (3/2)^2 / 10 = 9/40
# = sqrt(81/1600)
# The |V_us|^2 = 81/1600 = 9^2 / (40)^2
print()
print("Algebraic structure of 9/40:")
print("  9/40 = 3^2 / (2^3 * 5) = 9/40")
print("  9 = 3^2 (small Cabibbo invariant?)")
print("  40 = 8 * 5 = 2^3 * 5")
print("  |V_us|^2 = 81/1600 = 3^4/(2^6 * 5^2) — clean")
print()
print("Note: 9/40 in continued-fraction = [0; 4, 2, 4]")
print("vs PDG midpoint 0.22500 = exactly 9/40 — the PDG value is in fact often")
print("written as sin theta_C ~ 0.225 (this is the rounded value).")
print()
print("CRITICAL CHECK: is the PDG 0.225 actually a rounded version of the full")
print("data, or is it the central value? PDG 2024: |V_us| = 0.22501(68)")
print("So 9/40 = 0.22500 is *inside* the 1-sigma error bar.")
