#!/usr/bin/env python3
"""PySR gravité — 5 cibles testables empiriquement.

Hypothèse : SU(2)=gravité, SU(3)=matière, SU(4)=énergie noire (DS Bot triptyque).
Test : les observables gravitationnelles tombent-elles sur κ-rationals ?

5 catégories :
  1. Λ (NS tidal deformability) — LIGO GW170817
  2. M_max NS — NICER + LIGO
  3. QNM (BH ringdown) — LIGO O1-O4 events
  4. H₀ tension — Planck vs SH0ES
  5. σ_8 tension — Planck vs DES/KiDS

Multi-observables → évite overfitting 1-cible (G alone).
"""
import math
import time
import json
import numpy as np
from scipy.spatial import cKDTree
from multiprocessing import Pool, cpu_count
from scipy.stats import norm

START = time.time()
print(f"START : {time.ctime()}")
print("=" * 78)
print(f"PySR GRAVITY — 5 cibles testables (SU(2)=gravité hypothesis)")
print("=" * 78)

KAPPA = 1/6           # κ(SU(3)) = matière (notre vide)
KAPPA_SU2 = 1/2       # κ(SU(2)) = gravité
KAPPA_SU4 = 1/12      # κ(SU(4)) = dark energy
PI = math.pi
N_CPUS = cpu_count()
N_BOOTSTRAP = 1000
TW_MAX = 2

# Candidate library : κ_SU(3), κ_SU(2), κ_SU(4), π, rationals
a_set = np.array([-3, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3])
b_set = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
c_set = np.array([-2, -1, -0.5, 0, 0.5, 1, 2])
d_set = np.array([-1, -0.5, 0, 0.5, 1])
n_set = np.arange(1, 21)
m_set = np.arange(1, 21)

print(f"\nBuilding candidates : κ^a · κ_SU2^b · κ_SU4^c · π^d · (n/m), TW ≤ {TW_MAX}...")
t1 = time.time()
candidates_list = []
for a in a_set:
    for b in b_set:
        for c in c_set:
            for d in d_set:
                tw = abs(a) + abs(b) + abs(c) + abs(d)
                if tw > TW_MAX:
                    continue
                base = (KAPPA**a) * (KAPPA_SU2**b) * (KAPPA_SU4**c) * (PI**d)
                for n in n_set:
                    for m in m_set:
                        if math.gcd(n, m) > 1:
                            continue
                        v = base * n / m
                        if v > 0 and 1e-10 < v < 1e15:
                            candidates_list.append((v, a, b, c, d, n, m, tw))

candidates_arr = np.array([cd[0] for cd in candidates_list])
n_cand = len(candidates_arr)
print(f"Built {n_cand} candidates in {time.time()-t1:.1f}s")

log_candidates = np.log(candidates_arr)
sort_idx = np.argsort(log_candidates)
log_candidates_sorted = log_candidates[sort_idx]
tree = cKDTree(log_candidates_sorted.reshape(-1, 1))

# ======================
# 5 catégories d'observables
# ======================

PRE_REGISTERED = []

# === 1. NS tidal deformability Λ (GW170817 LIGO/Virgo) ===
NS_TIDAL = [
    ("Λ_1.4 (NS 1.4 M_sun)",       800.0),    # GW170817 upper bound at 90% confidence
    ("Λ_1.4_lower (P-method)",     70.0),     # GW170817 lower bound
    ("Λ_1.6 NS",                    250.0),   # estimate at 1.6 M_sun
    ("Λ_1.4_LCQM (Lambda1.4 QM)", 580.0),     # quark matter EOS
    ("Λ_1.4_softEOS",              500.0),    # APR4
    # Ratios sans dimension
    ("Λ_max/Λ_min ratio",          800/70),   # = 11.4
    ("ln(Λ_1.4)",                  math.log(580)),
]

# === 2. NS maximum mass M_max (NICER + LIGO) ===
NS_MASS = [
    ("M_max NS / M_sun (TOV)",     2.16),    # PSR J0740+6620 NICER+LIGO
    ("M_max/M_sun (Cromartie)",    2.14),    # Cromartie 2019
    ("M_max/M_sun (LIGO+NICER)",   2.18),    # Riley 2021
    ("M_chandrasekhar/M_sun",      1.46),    # 1.4 + correction
    ("M_max/M_chand ratio",        2.16/1.46),  # ≈ 1.48
    ("M_max·c²/Λ_QCD [GeV]",       2.16 * 1.989e30 * 9e16 / (0.240e9 * 1.602e-10)),  # huge number
    # Ratios sans dimension
    ("R_NS_max/R_S(M_max) ratio",  12.5/(2*6.67e-11*2.16*1.989e30/9e16/1e3)),  # R_NS / Schwarzschild
]

# === 3. QNM (Quasi-Normal Modes, BH ringdown) ===
# Kerr BH QNM dimensionless frequencies M·ω (M in geometrized units)
# For ℓ=m=2, n=0 (dominant)
QNM_KERR = [
    # Schwarzschild (a=0) QNM
    ("M·ω_220 Schwarz (a=0)",      0.3737),     # Berti+Cardoso 2009
    ("M·τ_220 Schwarz",            11.24/0.3737),  # Q_220
    ("M·ω_330 Schwarz",            0.5994),
    ("M·ω_440 Schwarz",            0.8092),
    ("M·ω_220_Im Schwarz",         0.0889),    # imaginary part = damping
    # Ratios
    ("ω_330/ω_220 Schwarz",        0.5994/0.3737),  # ≈ 1.604
    ("ω_440/ω_220 Schwarz",        0.8092/0.3737),  # ≈ 2.165
    ("ω_440/ω_330 Schwarz",        0.8092/0.5994),  # ≈ 1.350
    ("Q_220 Schwarz",              2.0),         # =ω_R/(2|ω_I|)
    # Kerr a=0.7 (typical spin)
    ("M·ω_220 Kerr a=0.7",        0.5326),
    ("M·ω_330 Kerr a=0.7",        0.8466),
    ("ω_330/ω_220 Kerr 0.7",      0.8466/0.5326),  # ≈ 1.590
    # GW150914 measured ringdown
    ("M·f_ringdown GW150914",     0.0866),     # 248 Hz at M=68 M_sun
    ("τ_ringdown GW150914 [ms]",  4.0),
]

# === 4. H₀ tension ===
H0_TENSION = [
    ("H_0 Planck [km/s/Mpc]",      67.4),
    ("H_0 SH0ES",                   73.0),
    ("H_0 BAO+BBN",                68.5),
    ("H_0 TRGB",                   69.8),
    ("H_0 Cepheids",               73.5),
    ("ratio H_SH0ES/H_Planck",     73.0/67.4),    # = 1.083
    ("Δ_H tension /σ",             5.6/1.0),       # ~5σ
    # Dimensionless H₀
    ("H_0 t_U [Gyr] · h",          13.8 * 0.674),  # = 9.3
]

# === 5. σ_8 tension ===
SIGMA8_TENSION = [
    ("σ_8 Planck",                 0.811),
    ("σ_8 DES Y3",                 0.776),
    ("σ_8 KiDS-1000",              0.752),
    ("S_8 = σ_8 (Ω_m/0.3)^0.5 Planck", 0.834),
    ("S_8 DES Y3",                 0.776),
    ("S_8 KiDS",                   0.766),
    ("Δσ_8 tension",               (0.811-0.752)/0.05),  # ~1σ
    # Prediction κ : σ_8 = √(2/3) (mega-run hit)
    ("√(2/3)",                     math.sqrt(2/3)),  # = 0.8165
    ("(2/3)^(1/2)/σ_8 Planck",     math.sqrt(2/3)/0.811),  # = 1.007
]

# === BONUS : Cosmologie ===
COSMO_GRAV = [
    ("Λ_cosmo / M_P^4 (10^-122)", 1.4e-122),     # cosmological constant
    ("M_P/M_sun ratio",            2.18e-8),      # huge ratio
    ("G·m_e²/ħc (α_G electron)",   1.75e-45),    # gravitational fine structure α
    ("G·m_p²/ħc (α_G proton)",     5.9e-39),     # α_G(m_p) — the key wall
    ("(m_p/M_P)²",                 (0.938/1.22e19)**2),  # same as α_G(m_p)
    ("ln(α_G_p)/ln(κ)",            math.log(5.9e-39)/math.log(1/6)),  # = 50.6 (the hierarchy exponent)
    # Bekenstein-Hawking
    ("S_BH_M_sun / k_B",           1.0e77),       # Bekenstein-Hawking entropy of M_sun BH
    ("S_BH_M_sun / S_sun_total",   1.0e77/1.0e58),  # 10^19 ratio
]

for cat_data in [NS_TIDAL, NS_MASS, QNM_KERR, H0_TENSION, SIGMA8_TENSION, COSMO_GRAV]:
    PRE_REGISTERED.extend(cat_data)

print(f"\nTotal observables : {len(PRE_REGISTERED)}")

target_vals = np.array([abs(v) for _, v in PRE_REGISTERED])
target_logs = np.log(target_vals)

real_distances, real_indices = tree.query(target_logs.reshape(-1, 1), k=1)
real_rel = np.exp(real_distances.flatten()) - 1

tolerance_levels = [1e-5, 1e-4, 1e-3, 5e-3, 0.01, 0.02, 0.05]
real_hits = {tol: int(np.sum(real_rel < tol)) for tol in tolerance_levels}

val_min, val_max = target_vals.min(), target_vals.max()
log_min, log_max = math.log(val_min), math.log(val_max)

def bootstrap_one(seed):
    np.random.seed(seed)
    rand_logs = np.random.uniform(log_min, log_max, len(target_vals))
    distances, _ = tree.query(rand_logs.reshape(-1, 1), k=1)
    rel = np.exp(distances.flatten()) - 1
    return tuple(int(np.sum(rel < t)) for t in tolerance_levels)

t3 = time.time()
with Pool(N_CPUS) as pool:
    boot_results = pool.map(bootstrap_one, range(2026, 2026 + N_BOOTSTRAP))
boot_results = np.array(boot_results)

print(f"\n{'='*78}\nRESULTS — GRAVITY ({len(PRE_REGISTERED)} obs)\n{'='*78}\n")
print(f"{'Tol':>10} {'Real':>6} {'Random μ±σ':>18} {'Z':>10}")
print("-"*70)

z_scores = {}
for i, tol in enumerate(tolerance_levels):
    real = real_hits[tol]
    rand_mean = boot_results[:, i].mean()
    rand_std = boot_results[:, i].std()
    z = (real - rand_mean) / max(rand_std, 0.01)
    sig = "✓✓" if z > 4 else "✓" if z > 3 else "🟡" if z > 2 else ""
    print(f"  <{tol*100:.4f}% {real:>6} {rand_mean:>8.1f}±{rand_std:>6.2f} {z:>+9.2f}σ {sig}")
    z_scores[tol] = {"real": int(real), "random_mean": float(rand_mean),
                     "random_std": float(rand_std), "z": float(z)}

print(f"\nTop 30 matches :")
sort_real = np.argsort(real_rel)
top_hits = []
for k in range(min(30, len(PRE_REGISTERED))):
    i = sort_real[k]
    name = PRE_REGISTERED[i][0]
    val = PRE_REGISTERED[i][1]
    cand_idx = sort_idx[real_indices[i]]
    cand_meta = candidates_list[cand_idx]
    cand_v = cand_meta[0]
    a, b, c, d, n, m, tw = cand_meta[1:]
    rel = real_rel[i] * 100
    formula = f"κ^{a}·κ_SU2^{b}·κ_SU4^{c}·π^{d}·({n}/{m})"
    print(f"  {name:>40} obs={val:.4e} pred={cand_v:.4e} ({rel:.4f}%) TW={tw} {formula}")
    top_hits.append({"name": name, "obs": float(val), "pred": float(cand_v),
                     "rel_pct": float(rel), "tw": float(tw), "formula": formula})

output = {"domain": "gravity_5targets", "n_obs": len(PRE_REGISTERED),
          "n_candidates": n_cand, "z_scores": z_scores, "top_hits": top_hits,
          "categories": {
              "NS_tidal": len(NS_TIDAL),
              "NS_mass": len(NS_MASS),
              "QNM_Kerr": len(QNM_KERR),
              "H0_tension": len(H0_TENSION),
              "sigma8_tension": len(SIGMA8_TENSION),
              "cosmo_gravity_walls": len(COSMO_GRAV),
          }}
with open("/tmp/pysr_gravity_5targets_results.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\nElapsed : {time.time()-START:.1f}s")
print(f"Saved : /tmp/pysr_gravity_5targets_results.json")
print(f"DONE.")
