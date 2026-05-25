"""
Verify Koide formula: K = (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 /
                          (m_e + m_mu + m_tau)
The denominator is NOT 3*(sum_m) but just sum_m. Then K = 2/3.

Or equivalently: K = 2/3 * (sum sqrt(m))^2 / (3 * sum m) ?
No, the standard form is:
  K = (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 /
      (m_e + m_mu + m_tau) * (1/3 of something?)

Actually Koide's exact statement:
  K = (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 /
      [3 * (m_e + m_mu + m_tau)] = 2/3

But that gives (sum sqrt)^2 / (3 sum m) = 2/3
  <=> (sum sqrt)^2 = 2 * sum m

So my python computed K = 0.5 = sum_sqrt^2 / (3 * sum m) means
  sum_sqrt^2 = 1.5 * sum m, which contradicts Koide 2/3.

Wait - I had it backwards. Let's recompute carefully.
"""
import numpy as np

m_e = 0.000510999
m_mu = 0.105658
m_tau = 1.77686

sum_m = m_e + m_mu + m_tau
sum_sqrt = np.sqrt(m_e) + np.sqrt(m_mu) + np.sqrt(m_tau)

K_ratio = sum_sqrt**2 / sum_m  # without the 3
print(f"sum sqrt(m_i) = {sum_sqrt:.6f}")
print(f"sum m_i = {sum_m:.6f}")
print(f"sum_sqrt^2 = {sum_sqrt**2:.6f}")
print(f"Ratio (sum sqrt)^2 / (sum m) = {K_ratio:.6f}")
print(f"This should be 2 (Koide says K = 2/3 of this = 2/3 of the ratio after dividing by 3)")
print()
print(f"Koide's K = (sum sqrt)^2 / [3 * sum m] = {sum_sqrt**2 / (3 * sum_m):.6f}")
print(f"Expected Koide: 2/3 = 0.6667")
print(f"Got: {sum_sqrt**2 / (3 * sum_m):.6f}")
print()
print("Hmm - got 0.5 instead of 2/3. Let me check with MS-bar masses vs pole masses.")
print()
# Try pole masses (different convention)
m_e_pole = 0.000510999
m_mu_pole = 0.10566
m_tau_pole = 1.77686
# Same values - issue must be elsewhere
print(f"Sum of squares of sqrt: {m_e + m_mu + m_tau} = {sum_m}")
print(f"Square of sum of sqrt: ({np.sqrt(m_e)} + {np.sqrt(m_mu)} + {np.sqrt(m_tau)})^2 = {sum_sqrt**2}")
print(f"Ratio = {sum_sqrt**2 / sum_m}")
print()
# Standard Koide formula: Q_lepton = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2
# Then Q = 2/3
Q = sum_m / sum_sqrt**2
print(f"Q = sum m / (sum sqrt)^2 = {Q:.6f}")
print(f"This is 1/{1/Q:.4f}")
print(f"Koide states Q = 2/3? No, Koide says (sum sqrt)^2 = (2/3) * 3 * sum m = 2 * sum m")
print(f"Equivalently (sum sqrt)^2 / sum m = 2 exactly")
print(f"Got {sum_sqrt**2 / sum_m:.6f}")
print()
# So K = (sum sqrt)^2 / (3 * sum m) = 2/3
# Wait, that's what I computed and got 0.5. Let me re-check more carefully...

# Try with electron mass in MeV
m_e_MeV = 0.510999
m_mu_MeV = 105.658
m_tau_MeV = 1776.86
sum_m_MeV = m_e_MeV + m_mu_MeV + m_tau_MeV
sum_sqrt_MeV = np.sqrt(m_e_MeV) + np.sqrt(m_mu_MeV) + np.sqrt(m_tau_MeV)
K_MeV = sum_sqrt_MeV**2 / (3 * sum_m_MeV)
print(f"With MeV: sum_sqrt = {sum_sqrt_MeV:.4f}, sum_m = {sum_m_MeV:.4f}")
print(f"K = (sum sqrt)^2 / (3 sum m) = {K_MeV:.6f}")
# Should match expected 2/3
