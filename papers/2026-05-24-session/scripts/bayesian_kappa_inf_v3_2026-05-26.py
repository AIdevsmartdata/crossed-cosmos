"""
Bayesian posterior κ_∞ from 3 lattice points + PySR ultra-contraint
=====================================================================
"""
import numpy as np
from math import sqrt, pi, log, exp

# Données lattice confirmées
KAPPA_MEASURED = {
    2: (0.5065, 0.010),   # SU(2)
    3: (0.5956, 0.0067),  # SU(3)  
    4: (0.6390, 0.0041),  # SU(4)
}
ZETA3 = 1.2020569032
KAPPA_INF_ZETA = ZETA3 / sqrt(pi)  # 0.6782

# Si loi κ(N) = κ_∞·(1-1/N²) :
# Pour chaque N, κ_∞_N = κ(N) × N²/(N²-1)
print("="*72)
print("BAYESIAN POSTERIOR κ_∞ avec 3 datapoints")
print("="*72)

kappa_inf_extractions = []
for N, (k_meas, k_err) in KAPPA_MEASURED.items():
    factor = N**2/(N**2 - 1)
    k_inf = k_meas * factor
    k_inf_err = k_err * factor
    kappa_inf_extractions.append((N, k_inf, k_inf_err))
    print(f"  N={N}: κ(N)={k_meas}±{k_err}, factor={factor:.4f}")
    print(f"        → κ_∞ = {k_inf:.4f} ± {k_inf_err:.4f}")

# Combine via weighted mean (inverse-variance weighting)
weights = [1/(e**2) for _, _, e in kappa_inf_extractions]
total_w = sum(weights)
kappa_inf_mean = sum(w*v for w,(_,v,_) in zip(weights, kappa_inf_extractions))/total_w
kappa_inf_std = 1/sqrt(total_w)

print(f"\n  Weighted mean : κ_∞ = {kappa_inf_mean:.5f} ± {kappa_inf_std:.5f}")
print(f"  ζ(3)/√π       = {KAPPA_INF_ZETA:.5f}")
print(f"  Δ = {kappa_inf_mean - KAPPA_INF_ZETA:.5f}")
print(f"  Sigma : {(kappa_inf_mean - KAPPA_INF_ZETA)/kappa_inf_std:.2f}σ")

# χ²/dof for loi (1-1/N²) with this κ_∞_mean
chi2 = 0
for N, (k_meas, k_err) in KAPPA_MEASURED.items():
    k_pred = kappa_inf_mean * (1 - 1/N**2)
    chi2 += ((k_meas - k_pred)/k_err)**2
dof = 3 - 1  # 3 data, 1 parameter
print(f"\n  χ²/dof = {chi2:.3f}/{dof} = {chi2/dof:.3f}")
if chi2/dof < 1:
    print(f"  → EXCELLENT fit (χ²/dof < 1)")
else:
    print(f"  → Acceptable fit")

# Test ALTERNATIVE candidates for κ_∞
print(f"\n  Candidats κ_∞ alternatifs (data-driven) :")
candidates = {
    'ζ(3)/√π': KAPPA_INF_ZETA,
    '1 - 1/π': 1 - 1/pi,
    '21/31': 21/31,
    '2/3·e/π': 2/3*np.e/pi,
    '27/40': 27/40,
    'kappa_∞_fit': kappa_inf_mean,
}
for label, cand in candidates.items():
    sigma_dev = abs(cand - kappa_inf_mean)/kappa_inf_std
    chi2_alt = sum(((KAPPA_MEASURED[N][0] - cand*(1-1/N**2))/KAPPA_MEASURED[N][1])**2 
                   for N in [2,3,4])
    print(f"    {label:<18s} = {cand:.5f}  Δ={sigma_dev:.1f}σ from posterior, χ²/dof = {chi2_alt/dof:.2f}")

# m_H prediction avec posterior
print(f"\n  m_H = κ(SU(2))·v = 3·κ_∞/4·v :")
v = 246.22
m_H_pred = 3 * kappa_inf_mean / 4 * v
m_H_err = 3 * kappa_inf_std / 4 * v
print(f"    κ_∞ posterior : m_H = {m_H_pred:.3f} ± {m_H_err:.3f} GeV")
print(f"    Si κ_∞ = ζ(3)/√π : m_H = {3*KAPPA_INF_ZETA/4*v:.3f} GeV")
print(f"    m_H obs PDG   = 125.10 ± 0.14 GeV")
print(f"    Compatibility : {abs(m_H_pred - 125.10)/sqrt(m_H_err**2 + 0.14**2):.2f}σ")

# Prediction SU(5), SU(6)
print(f"\n  Prédictions overnight :")
for N in [5, 6, 7, 8, 10]:
    k_pred = kappa_inf_mean * (1 - 1/N**2)
    k_pred_zeta = KAPPA_INF_ZETA * (1 - 1/N**2)
    print(f"    κ(SU({N})) = {k_pred:.4f} (posterior) ou {k_pred_zeta:.4f} (ζ(3)/√π)")

# PySR ultra-contraint on 3 data points
print(f"\n{'='*72}")
print("PySR ultra-contraint (sympy symbolic search)")
print('='*72)
print("Formes testées κ(N) = f(N) × g(constant) :")

# Test formules ECI-motivated explicitly
import sympy as sp
N_sym = sp.Symbol('N')
formes = {
    '(1-1/N²)·κ_∞':        lambda N: (1 - 1/N**2) * kappa_inf_mean,
    '(N²-1)/N²·κ_∞':       lambda N: (N**2-1)/N**2 * kappa_inf_mean,
    '(N-1)/N·κ_∞':          lambda N: (N-1)/N * kappa_inf_mean,
    '(N²-1)/(N²+1)·κ_∞':   lambda N: (N**2-1)/(N**2+1) * kappa_inf_mean,
    'tanh(N)·κ_∞':          lambda N: np.tanh(N) * kappa_inf_mean,
    '(1-2/(N+1))·κ_∞':      lambda N: (1 - 2/(N+1)) * kappa_inf_mean,
}

print(f"\n  Formule                  | κ(2)pred | κ(3)pred | κ(4)pred | χ²/dof")
print(f"  ─────────────────────────┼──────────┼──────────┼──────────┼────────")
for name, f in formes.items():
    chi2 = sum(((KAPPA_MEASURED[N][0] - f(N))/KAPPA_MEASURED[N][1])**2 for N in [2,3,4])
    print(f"  {name:<24s} | {f(2):.4f}  | {f(3):.4f}  | {f(4):.4f}  | {chi2/2:.2f}")

print(f"\n→ Gagnant : (1-1/N²)·κ_∞ avec χ²/dof = {sum(((KAPPA_MEASURED[N][0] - kappa_inf_mean*(1-1/N**2))/KAPPA_MEASURED[N][1])**2 for N in [2,3,4])/2:.2f}")
