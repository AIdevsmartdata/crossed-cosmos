#!/usr/bin/env python3
"""
MEGA v3 — MAX d'observables avec UNITES explicites.

Stratégie : 150+ observables physiques avec catégories dimensionnelles,
puis brute-force search pour relations Σ premiers, rationnels, et
combinations de constantes universelles.

Inspiré par MEGA-RUN 166 obs Z=+14.65σ de la session 2026-05-24.

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os, numpy as np, json, time
from sympy import sieve

print(f"=== MEGA v3 - max obs + units ===", flush=True)
print(f"Start : {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)

primes = list(sieve.primerange(2, 250))
cumsum_p = np.cumsum(primes[:30])

# ============================
# DIMENSIONAL CATEGORIES
# ============================
# Each observable tagged with units to enable dimensional analysis
# DIM = (M_Pl, GeV, dimensionless, etc.)

OBSERVATIONS = [
    # (name, value, sigma, unit_category, conjecturedDimG, source)
    # === LATTICE κ_EE(N) cross-N (8 dense) ===
    ('kappa_SU2',     0.508,  0.010, 'dimensionless', 3, 'BP2008b'),
    ('kappa_SU3',     0.603,  0.010, 'dimensionless', 8, 'BP2008b'),
    ('kappa_SU4',     0.6358, 0.005, 'dimensionless', 15, 'BP2008b'),
    ('kappa_SU5',     0.7012, 0.006, 'dimensionless', 24, 'BP2008b'),
    ('kappa_SU6',     0.810,  0.005, 'dimensionless', 35, 'BP2008b'),
    ('kappa_SU7',     0.9107, 0.005, 'dimensionless', 48, 'BP2008b'),
    ('kappa_SU8',     1.0416, 0.005, 'dimensionless', 63, 'BP2008b'),
    ('kappa_SU9',     1.1764, 0.005, 'dimensionless', 80, 'BP2008b'),
    ('kappa_SU10',    1.3307, 0.005, 'dimensionless', 99, 'BP2008b'),
    ('kappa_SU11',    1.5008, 0.005, 'dimensionless', 120, 'BP2008b'),
    ('kappa_SU12',    1.6707, 0.005, 'dimensionless', 143, 'BP2008b'),

    # === EW PARAMETERS (GeV) ===
    ('v_EW',          246.22, 0.05,  'GeV', 3, 'PDG'),
    ('m_Higgs',       125.10, 0.14,  'GeV', 3, 'PDG'),
    ('m_W',           80.379, 0.012, 'GeV', 3, 'PDG'),
    ('m_Z',           91.187, 0.002, 'GeV', 3, 'PDG'),
    ('Gamma_W',       2.085,  0.042, 'GeV', None, 'PDG'),
    ('Gamma_Z',       2.4952, 0.0023,'GeV', None, 'PDG'),

    # === QUARKS (GeV) ===
    ('m_t',           173.21, 0.51,  'GeV', None, 'PDG'),
    ('m_b',           4.183,  0.007, 'GeV', None, 'PDG'),
    ('m_c',           1.273,  0.0046,'GeV', None, 'PDG'),
    ('m_s',           0.0934, 0.0086,'GeV', None, 'PDG'),
    ('m_d',           0.00467,0.0005,'GeV', None, 'PDG'),
    ('m_u',           0.00216,0.0005,'GeV', None, 'PDG'),

    # === LEPTONS (GeV) ===
    ('m_tau',         1.77686,0.00012,'GeV', None, 'PDG'),
    ('m_mu',          0.10566,1e-7,  'GeV', None, 'PDG'),
    ('m_e',           0.000511,1e-9, 'GeV', None, 'PDG'),

    # === HADRONS (GeV) ===
    ('m_proton',      0.93827,1e-6,  'GeV', None, 'PDG'),
    ('m_neutron',     0.93957,1e-6,  'GeV', None, 'PDG'),
    ('m_pion',        0.13957,1e-5,  'GeV', None, 'PDG'),
    ('m_kaon',        0.49368,1e-5,  'GeV', None, 'PDG'),
    ('m_eta',         0.5479, 0.0005,'GeV', None, 'PDG'),
    ('m_omega',       0.78266,1e-4,  'GeV', None, 'PDG'),
    ('m_rho',         0.7755, 0.0005,'GeV', None, 'PDG'),
    ('m_Jpsi',        3.0969, 1e-5,  'GeV', None, 'PDG'),
    ('m_Upsilon',     9.4603, 0.0003,'GeV', None, 'PDG'),

    # === COUPLINGS (dimensionless) ===
    ('alpha_em_inv',  137.036, 0.00001,'dimensionless', None, 'PDG'),
    ('alpha_s_mZ',    0.1180,  0.0009,'dimensionless', 8, 'PDG'),
    ('alpha_s_mt',    0.108,   0.002, 'dimensionless', 8, 'PDG'),
    ('alpha_W',       0.03392, 0.0002,'dimensionless', 3, 'PDG'),
    ('sin2_thetaW',   0.23122, 0.00004,'dimensionless', 3, 'PDG'),
    ('cos2_thetaW',   0.76878, 0.00004,'dimensionless', 3, 'PDG'),
    ('tan_thetaW',    0.5475,  0.0001, 'dimensionless', 3, 'PDG'),
    ('GF_inv',        1.16638e-5,1e-9,'GeV^-2', None, 'PDG'),

    # === YUKAWA (dimensionless) ===
    ('y_top',         0.9914, 0.003, 'dimensionless', None, 'PDG-deriv'),
    ('y_bot',         0.0240, 0.0001,'dimensionless', None, 'PDG-deriv'),
    ('y_charm',       0.00731,1e-5,  'dimensionless', None, 'PDG-deriv'),
    ('y_tau',         0.01018,1e-7,  'dimensionless', None, 'PDG-deriv'),
    ('y_mu',          6.05e-4,1e-7,  'dimensionless', None, 'PDG-deriv'),

    # === CKM ===
    ('Vus',           0.2243, 0.0008,'dimensionless', None, 'PDG'),
    ('Vcb',           0.0422, 0.0008,'dimensionless', None, 'PDG'),
    ('Vub',           0.00382,2e-4,  'dimensionless', None, 'PDG'),
    ('A_CKM',         0.836,  0.014, 'dimensionless', None, 'PDG'),
    ('lambda_CKM',    0.2245, 0.0008,'dimensionless', None, 'PDG'),
    ('rho_bar',       0.122,  0.018, 'dimensionless', None, 'PDG'),
    ('eta_bar',       0.355,  0.011, 'dimensionless', None, 'PDG'),
    ('delta_CKM',     1.196,  0.045, 'radians', None, 'PDG'),

    # === PMNS ===
    ('sin2_theta12_PMNS',0.307, 0.013,'dimensionless', None, 'PDG'),
    ('sin2_theta23_PMNS',0.575, 0.025,'dimensionless', None, 'PDG'),
    ('sin2_theta13_PMNS',0.0224,0.0007,'dimensionless', None, 'PDG'),

    # === COSMOLOGY ===
    ('Lambda_obs',    1.105e-122, 1e-124,'M_Pl4', 14, 'Planck'),
    ('eta_B',         6.12e-10, 4e-12, 'dimensionless', 21, 'Planck'),
    ('Omega_DM_h2',   0.1200, 0.0012,'dimensionless', None, 'Planck'),
    ('Omega_b_h2',    0.02237,0.00015,'dimensionless', None, 'Planck'),
    ('Omega_DM_b',    5.36,   0.05, 'dimensionless', None, 'Planck-deriv'),
    ('Omega_Lambda',  0.6847, 0.0073,'dimensionless', None, 'Planck'),
    ('Omega_m',       0.3153, 0.0073,'dimensionless', None, 'Planck'),
    ('h_Hubble',      0.6736, 0.0054,'dimensionless', None, 'Planck'),
    ('n_s',           0.9649, 0.0042,'dimensionless', None, 'Planck'),
    ('r_tensor',      0.06,   None,  'dimensionless', None, 'Planck-bound'),
    ('A_s',           2.10e-9,0.03e-9,'dimensionless', None, 'Planck'),
    ('Sum_mnu',       0.06,   None,  'eV', None, 'Planck-bound'),

    # === SCALES ===
    ('M_Pl',          2.435e18, 1e15,'GeV', None, 'derived'),
    ('M_GUT_naive',   2e16,    0,    'GeV', None, 'derived'),
    ('Lambda_QCD',    0.341,   0.012,'GeV', None, 'PDG'),

    # === BINDING / RADIUS ===
    ('m_e_over_v',    2.075e-6,1e-9, 'dimensionless', None, 'derived'),
    ('m_p_over_v',    3.811e-3,1e-6, 'dimensionless', None, 'derived'),
    ('rH_proton',     0.8409,  0.004,'fm', None, 'PDG'),
    ('mu_proton',     2.79285, 1e-7, 'mu_N', None, 'PDG'),

    # === RATIOS (dimensionless, key for symbolic regression) ===
    ('mt_over_mb',    173.21/4.183,  0.05,'dimensionless', None, 'derived'),
    ('mb_over_mtau',  4.183/1.77686, 0.005,'dimensionless', None, 'derived'),
    ('mtau_over_mmu', 1.77686/0.10566,0.001,'dimensionless', None, 'derived'),
    ('mmu_over_me',   0.10566/0.000511,0.05,'dimensionless', None, 'derived'),
    ('mp_over_me',    0.93827/0.000511,0.1,'dimensionless', None, 'derived'),
    ('mW_over_mZ',    80.379/91.187, 0.0002,'dimensionless', None, 'derived'),
    ('mH_over_mZ',    125.10/91.187, 0.002,'dimensionless', None, 'derived'),
    ('mH_over_v',     125.10/246.22, 0.001,'dimensionless', 3, 'derived'),
    ('alpha_em_alpha_s',0.00729/0.1180,1e-5,'dimensionless', None, 'derived'),

    # === GLUEBALLS lattice ===
    ('m_glueball_0pp', 1.71,   0.05, 'GeV', None, 'lattice'),
    ('m_glueball_2pp', 2.39,   0.07, 'GeV', None, 'lattice'),
    ('m_glueball_0mp', 2.56,   0.05, 'GeV', None, 'lattice'),

    # === LATTICE QCD scales ===
    ('sqrt_sigma',    0.42,   0.01, 'GeV', None, 'lattice'),  # string tension
    ('r0_inv',        0.477,  0.012,'GeV', None, 'Sommer'),
    ('f_pi',          0.0930, 0.0001,'GeV', None, 'PDG'),
    ('f_K',           0.1561, 0.0002,'GeV', None, 'PDG'),

    # === COSMOLOGICAL DERIVED ===
    ('ln_MPl_over_v', np.log(2.435e18/246.22), 0.01,'dimensionless_ln', 8, 'derived'),
    ('ln_MPl4_Lambda',-np.log(1.105e-122),1.0,'dimensionless_ln', 14, 'derived'),
    ('ln_inv_etaB',   -np.log(6.12e-10), 0.01,'dimensionless_ln', 21, 'derived'),

    # === NEW : Wilson coupling ratios cross-N ===
    ('beta_lat_SU5_over_N2', 15.0/25,   None,'dimensionless', None, 'lattice-setup'),
    ('beta_lat_SU6_over_N2', 21.6/36,   None,'dimensionless', None, 'lattice-setup'),
    ('beta_lat_SU7_over_N2', 29.4/49,   None,'dimensionless', None, 'lattice-setup'),

    # === N_eff cosmology, BAO ===
    ('N_eff',         3.046,  0.01,  'dimensionless', None, 'theory'),

    # === FLAVOR : κ_EE / something ===
    ('kappa_inf_emp', 0.6782, 0.01,  'dimensionless', None, 'fit-asymptote'),
]

print(f"Total observables loaded: {len(OBSERVATIONS)}", flush=True)
# Group by unit
units_count = {}
for o in OBSERVATIONS:
    u = o[3]
    units_count[u] = units_count.get(u, 0) + 1
print(f"By unit category:", flush=True)
for u, n in sorted(units_count.items(), key=lambda x:-x[1]):
    print(f"  {u:20s}: {n}", flush=True)

# ============================
# UNIVERSAL CONSTANTS LIBRARY
# ============================
constants = {
    'pi': np.pi,
    '2pi': 2*np.pi,
    'pi2': np.pi**2,
    'pi3': np.pi**3,
    'pi4': np.pi**4,
    '1/pi': 1/np.pi,
    '4/pi2': 4/np.pi**2,
    'e_euler': np.e,
    '1/e': 1/np.e,
    'log2': np.log(2),
    'log3': np.log(3),
    'log5': np.log(5),
    'log7': np.log(7),
    'log10': np.log(10),
    'zeta3': 1.2020569,
    'zeta5': 1.0369277,
    'gamma_euler': 0.5772157,
    'phi_gold': 1.6180339887,
    'kappa_FP': 1/6,
    'xi_star': 2/3,
    'c_BH': 1/4,
    'b_0_coeff': 11/3,
    'kappa_inf_zeta3pi': 1.2020569 / np.sqrt(np.pi),
    'sqrt2': np.sqrt(2),
    'sqrt3': np.sqrt(3),
    'sqrt5': np.sqrt(5),
    'sqrt7': np.sqrt(7),
}

# ============================
# BRUTE FORCE TEMPLATES
# ============================
def test_relation(name, value, sigma):
    """Try MANY relation templates : Σ_k premiers, rationals p/q, constants ratios."""
    if value is None or value <= 0:
        return []
    matches = []
    abs_v = abs(value)

    # Σ premiers
    for k in range(1, 30):
        s = cumsum_p[k-1] if k-1 < len(cumsum_p) else 0
        if s == 0: continue
        # ln(value) ≈ Σ_k
        for sign in [1, -1, 2, -2, 0.5, -0.5]:
            target_sk = sign * s
            if abs(np.log(abs_v) - target_sk) / (abs(target_sk)+1) < 0.05:
                matches.append({
                    'template': f"ln(X) = {sign}*Σ_{k}premiers",
                    'k': k, 'sigma_k': int(s), 'sign': sign,
                    'predicted': float(np.exp(target_sk)),
                    'rel_error': abs(value - np.exp(target_sk))/value
                })
    # Rationals p/q
    for q in range(1, 35):
        for p in range(1, 6*q+1):
            r = p/q
            if 0.5*abs_v < r < 2*abs_v:
                rel = abs(value - r) / abs(value)
                if rel < 0.005:  # <0.5%
                    matches.append({'template': f"X = {p}/{q}", 'rel_error': float(rel), 'predicted': float(r)})
    # Constants ratios (1- or 2-constant combinations)
    cnames = list(constants.keys())
    for ci in cnames:
        cv = constants[ci]
        for cj in cnames:
            if ci >= cj: continue
            cw = constants[cj]
            for op_name, op in [('×', lambda a,b: a*b), ('÷', lambda a,b: a/b)]:
                try:
                    test = op(cv, cw)
                    if 0.5*abs_v < test < 2*abs_v:
                        rel = abs(value - test) / abs(value)
                        if rel < 0.005:
                            matches.append({'template': f"X = {ci}{op_name}{cj}", 'rel_error': float(rel), 'predicted': float(test)})
                except:
                    pass
    # Single constant ratio
    for ci in cnames:
        cv = constants[ci]
        for power in [1, -1, 2, -2, 0.5, -0.5, 3, -3]:
            try:
                test = cv**power
                if 0.5*abs_v < test < 2*abs_v:
                    rel = abs(value - test) / abs(value)
                    if rel < 0.005:
                        matches.append({'template': f"X = {ci}^{power}", 'rel_error': float(rel), 'predicted': float(test)})
            except: pass
    # n_observable * constant
    for ci in cnames:
        cv = constants[ci]
        if cv > 0:
            ratio = value / cv
            # Check if ratio matches simple rational
            for q in range(1, 30):
                for p in range(1, 6*q+1):
                    if abs(ratio - p/q) / ratio < 0.005:
                        matches.append({'template': f"X = ({p}/{q})·{ci}",
                                       'rel_error': float(abs(ratio - p/q)/ratio),
                                       'predicted': float((p/q)*cv)})
    # Sort by error
    matches.sort(key=lambda m: m['rel_error'])
    return matches[:5]  # top 5 only


# ============================
# RUN brute force on ALL observables
# ============================
print("\n" + "="*70, flush=True)
print("RUN brute force matching all observables", flush=True)
print("="*70, flush=True)

all_results = {}
high_quality_matches = []
for obs in OBSERVATIONS:
    name, val, sigma, unit, dim_G, source = obs
    matches = test_relation(name, val, sigma)
    all_results[name] = {
        'value': float(val) if val else None,
        'sigma': float(sigma) if sigma else None,
        'unit': unit,
        'dim_G_conjecture': dim_G,
        'source': source,
        'top_matches': matches[:3]
    }
    if matches and matches[0]['rel_error'] < 0.001:
        high_quality_matches.append({
            'name': name, 'value': val,
            'best': matches[0]
        })

# Report high quality matches
print(f"\n=== HIGH-QUALITY MATCHES (rel error < 0.1%) : {len(high_quality_matches)} ===", flush=True)
high_quality_matches.sort(key=lambda x: x['best']['rel_error'])
for hq in high_quality_matches[:30]:
    print(f"  {hq['name']:25s} = {hq['value']:.4e} → {hq['best']['template']}, pred={hq['best']['predicted']:.4e}, rel={hq['best']['rel_error']*100:.4f}%", flush=True)

# Quality stats
n_excellent = sum(1 for m in high_quality_matches if m['best']['rel_error'] < 0.0001)
n_very_good = sum(1 for m in high_quality_matches if m['best']['rel_error'] < 0.0005)
print(f"\nStats:", flush=True)
print(f"  Total observables: {len(OBSERVATIONS)}", flush=True)
print(f"  Excellent matches (<0.01%): {n_excellent}", flush=True)
print(f"  Very good matches (<0.05%): {n_very_good}", flush=True)
print(f"  Good matches (<0.1%): {len(high_quality_matches)}", flush=True)

# Save
out = {
    'date': '2026-05-26',
    'author': 'Kévin Rémondière (ORCID 0009-0008-2443-7166)',
    'description': 'MEGA v3 brute-force symbolic search max-obs with units',
    'n_observables': len(OBSERVATIONS),
    'units_breakdown': units_count,
    'high_quality_matches': high_quality_matches,
    'all_results': all_results,
    'stats': {
        'n_excellent': n_excellent,
        'n_very_good': n_very_good,
        'n_good': len(high_quality_matches),
    }
}
with open('/tmp/MEGA_v3_results.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f"\n→ Saved /tmp/MEGA_v3_results.json", flush=True)
print(f"End : {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
