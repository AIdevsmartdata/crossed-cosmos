"""
MEGA PySR — cross-insights ECI session 2026-05-25
====================================================
Feature space :
  - κ(SU(N)) lattice measured N=2,3,(4,5,6 predicted)
  - κ_∞ candidate ζ(3)/√π
  - M_24 dim irreps (20 values)
  - Σ first k premiers (k=1..14)
  - Lie group dims (SU, G_2, F_4, E_6, E_7, E_8)
  - Class numbers h(D) for selected D
  - b_2(K3) = 22
  - Mathematical constants π, e, ζ(3), √π

Targets : 9 Yukawa, m_H/v, m_Z/v, m_W/v, m_t/v, sin²θ_W, α_s, α_em,
          CKM Wolfenstein, PMNS angles, cosmo Λ/η_B/n_s
"""
import numpy as np
from pysr import PySRRegressor
import time
import json

# ============================================================================
# FEATURE VECTORS
# ============================================================================
# Each "row" = one observable target.
# Features common to all observables :
PI = np.pi
E_ = np.e
ZETA3 = 1.2020569032
SQRT_PI = np.sqrt(PI)
KAPPA_INF = ZETA3 / SQRT_PI  # 0.6782

# Lattice κ measured
KAPPA_SU2 = 0.5065
KAPPA_SU3 = 0.5956

# Σ premiers cumulative
SUM_PRIMES = {1:2, 2:5, 3:10, 4:17, 5:28, 6:41, 7:58, 8:77, 9:100,
              10:129, 11:160, 12:197, 13:238, 14:281, 15:328}

# Dim Lie groups
DIM_SU2 = 3
DIM_SU3 = 8
DIM_SU4 = 15
DIM_SU5 = 24
DIM_G2 = 14
DIM_G2_FUND = 7
DIM_F4 = 52
DIM_E6 = 78
DIM_E7 = 133
DIM_E8 = 248

# M_24 dim irreps
M24_DIMS = [1, 23, 45, 231, 252, 253, 483, 770, 990, 1035,
            1265, 1771, 2024, 2277, 3312, 3520, 5313, 5544, 5796, 10395]

# Class numbers h(D) for "ECI-selected" D
H_D_23 = 3       # SU(2)
H_D_95 = 8       # SU(3)
H_D_215 = 14     # G_2

# K3 invariants
B_2_K3 = 22

# All observables
v = 246.22
mH = 125.10
mZ = 91.1876
mW = 80.377
mt = 172.57
mb = 4.18
mc = 1.27
mtau = 1.77686
mmu = 0.10566
me = 0.51099895e-3
mu = 2.16e-3
md = 4.67e-3
ms = 93.4e-3
sin2W = 0.23121
alpha_s = 0.118
alpha_em_0 = 1/137.036
alpha_em_MZ = 1/127.952
lam_CKM = 0.225
A_CKM = 0.826
rho_b = 0.159
eta_b = 0.348
delta_CKM = np.deg2rad(65.8)
sin2_th12 = 0.30319
sin2_th23 = 0.57131
sin2_th13 = 0.022
n_s = 0.9649
eta_B = 6.12e-10
Lambda_MP4 = 1.105e-122
Omega_DM_b = 5.36
M_Pl = 1.22091e19

# Targets dict
TARGETS = {
    'mH_over_v': mH/v,
    'mZ_over_v': mZ/v,
    'mW_over_v': mW/v,
    'mt_over_v': mt/v,
    'mb_over_v': mb/v,
    'mtau_over_v': mtau/v,
    'mmu_over_v': mmu/v,
    'me_over_v': me/v,
    'mc_over_v': mc/v,
    'ms_over_v': ms/v,
    'mu_over_v': mu/v,
    'md_over_v': md/v,
    'mH2_over_mZ2': mH**2/mZ**2,
    'mW2_over_mZ2': mW**2/mZ**2,
    'mt_over_mb': mt/mb,
    'mc_over_mtau': mc/mtau,
    'sin2_thetaW': sin2W,
    'alpha_s': alpha_s,
    '1_over_alpha_em_0': 137.036,
    '1_over_alpha_em_MZ': 127.952,
    'lambda_CKM': lam_CKM,
    'A_CKM': A_CKM,
    'rho_bar_CKM': rho_b,
    'eta_bar_CKM': eta_b,
    'delta_CKM_over_pi': delta_CKM/PI,
    'sin2_th12_PMNS': sin2_th12,
    'sin2_th23_PMNS': sin2_th23,
    'sin2_th13_PMNS': sin2_th13,
    'n_s_cosmo': n_s,
    'log10_eta_B_neg': -np.log10(eta_B),  # 9.21
    'log10_Lambda_neg': -np.log10(Lambda_MP4),  # 121.96
    'log_MPl_v': np.log(M_Pl/v),  # 38.45
    'Omega_DM_over_b': Omega_DM_b,
}

print(f"\n{'='*72}")
print("MEGA PySR — Features and targets")
print('='*72)
print(f"\nFeatures available: {15} types")
print(f"  κ_lattice, κ_∞, π, e, ζ(3), √π")
print(f"  Σ premiers (k=1..14)")
print(f"  Dim Lie : SU(2,3,4,5), G_2, F_4, E_6")
print(f"  M_24 dims (20 values)")
print(f"  Class numbers h(D)")
print(f"  b_2(K3)")
print(f"\nTargets to search: {len(TARGETS)} observables")

# ============================================================================
# Pour PySR : input/output pairs
# Construct fake "datapoints" where each row = different formula
# Actually PySR fits y(x), so we need vector data
# Approach : prendre features comme variables et chercher formule
# Mais ici on cherche pour CHAQUE target SÉPARÉMENT
# ============================================================================

print(f"\n{'='*72}")
print("Approche : pour chaque target, fit avec features list")
print('='*72)

# Pour chaque target, on cherche y_target = f(features) où features
# sont les valeurs scalaires (κ_inf, π, etc.)
# Pas vraiment du PySR classique car n_samples=1
# Plutôt : pour chaque target, brute-force combinations of features

# Approche alternative : créer "samples" via paramétrisation
# 1 sample = (constants list, target)
# PySR cherche formule x ← y
# avec x = bookkeeping symbolique

# Pour PySR, on génère DATA-ARTIFICIELLE : un seul sample par target
# avec features comme variables. PySR cherche formule constante.
# Problem : 1 sample → infinité de formules.

# Solution : Multi-target PySR. Pour each target, find shortest formula
# in terms of feature constants such that output matches obs.

# Simple brute-force search of formula candidates:
features = {
    'kappa_SU2': KAPPA_SU2,
    'kappa_SU3': KAPPA_SU3,
    'kappa_inf': KAPPA_INF,
    'pi': PI,
    'e': E_,
    'zeta3': ZETA3,
    'sqrt_pi': SQRT_PI,
    'b2_K3': B_2_K3,
    'dim_SU2': DIM_SU2,
    'dim_SU3': DIM_SU3,
    'dim_SU4': DIM_SU4,
    'dim_G2': DIM_G2,
    'dim_G2_fund': DIM_G2_FUND,
    'dim_E6': DIM_E6,
    'Sigma_8': SUM_PRIMES[8],
    'Sigma_14': SUM_PRIMES[14],
    'M24_252': 252,
    'M24_10395': 10395,
    'M24_1265': 1265,
    'M24_1771': 1771,
    'M24_45': 45,
    'M24_770': 770,
    'M24_5796': 5796,
    'M24_2024': 2024,
    'M24_2277': 2277,
    'M24_483': 483,
    'h_23': 3,
    'h_95': 8,
    'h_215': 14,
}

# For each target, find best symbolic formula via brute search
# Formula generators : ratios, products, powers of features
print(f"\nBrute force formula search per target (top 5 candidates):")
results = {}
for tgt_name, tgt_val in TARGETS.items():
    candidates = []
    # 1. Direct feature match
    for fn, fv in features.items():
        if fv > 0:
            err = abs(fv - tgt_val)/abs(tgt_val) if tgt_val != 0 else abs(fv)
            if err < 0.02:
                candidates.append((f"{fn}", fv, err))
    # 2. Ratios of features
    for fn1, fv1 in features.items():
        for fn2, fv2 in features.items():
            if fn1 != fn2 and fv2 > 0:
                v_test = fv1 / fv2
                if v_test > 0:
                    err = abs(v_test - tgt_val)/abs(tgt_val) if tgt_val != 0 else abs(v_test)
                    if err < 0.02:
                        candidates.append((f"{fn1}/{fn2}", v_test, err))
    # 3. Simple integers * feature
    for fn, fv in features.items():
        for n in [1, 2, 3, 4, 5, 6, 7, 8]:
            for d in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                v_test = n * fv / d
                if v_test > 0:
                    err = abs(v_test - tgt_val)/abs(tgt_val) if tgt_val != 0 else abs(v_test)
                    if err < 0.005:
                        candidates.append((f"{n}*{fn}/{d}", v_test, err))
    # 4. Products of features (pairs)
    f_list = list(features.items())
    for i, (fn1, fv1) in enumerate(f_list):
        for fn2, fv2 in f_list[i+1:]:
            v_test = fv1 * fv2
            if v_test > 0:
                err = abs(v_test - tgt_val)/abs(tgt_val) if tgt_val != 0 else abs(v_test)
                if err < 0.005:
                    candidates.append((f"{fn1}*{fn2}", v_test, err))
    
    # Sort by error, keep top 3
    candidates.sort(key=lambda x: x[2])
    results[tgt_name] = candidates[:3]

# Print results
print(f"\n{'Target':<25s} {'Best formula':<40s} {'Value':>12s} {'Obs':>12s} {'Err %':>8s}")
print('-'*100)
for tgt_name, cands in results.items():
    tgt_val = TARGETS[tgt_name]
    if cands:
        f, v_pred, err = cands[0]
        flag = "★★" if err < 0.001 else ("★" if err < 0.005 else "")
        print(f"  {tgt_name:<23s} {f:<40s} {v_pred:>12.4g} {tgt_val:>12.4g} {err*100:>6.2f}% {flag}")
    else:
        print(f"  {tgt_name:<23s} {'no match <2%':<40s} {' ':>12s} {tgt_val:>12.4g}")

# Save results
with open('/tmp/mega_pysr_results.json', 'w') as f:
    json_results = {k: [{'formula': c[0], 'value': float(c[1]), 'err_rel': float(c[2])} for c in v] for k, v in results.items()}
    json.dump(json_results, f, indent=2)

print(f"\nResults saved to /tmp/mega_pysr_results.json")
