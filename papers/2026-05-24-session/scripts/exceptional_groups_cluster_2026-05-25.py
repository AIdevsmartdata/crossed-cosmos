"""
Test : les clusters /p correspondent-ils aux dim des Lie groupes exceptionnels ?
=================================================================================
E6 fund = 27 → match /27 cluster trouvé
F4 fund = 26
E7 fund = 56
G2 dim = 14, fund = 7
E8 dim = 248
ainsi que :
  K3 b_2 = 22 (+1 trivial = 23 → match /23 cluster)
  Niemeier 24 lattices
"""
import numpy as np
from math import gcd
from collections import Counter

SM = {
    'm_H/v':       0.50808,
    'm_Z/v':       0.37035,
    'm_W/v':       0.32644,
    '(m_H/m_Z)²':  1.88210,
    '(m_W/m_Z)²':  0.77695,
    '(m_t/m_Z)²':  3.58145,
    'm_H/m_Z':     1.37190,
    'sin²θ_W':     0.23121,
    'sin θ_W':     0.48084,
    'cos²θ_W':     0.76879,
    'cos θ_W':     0.87681,
    'α_s':         0.118,
    'α_em(MZ)':    1/127.952,
    'y_top':       0.99119,
    'y_top²':      0.98246,
    'y_b':         0.02401,
    'y_τ':         0.01021,
    'A_CKM':       0.826,
    'A_CKM²':      0.6823,
    'λ_CKM':       0.225,
    'λ²':          0.05063,
    'ρ̄':           0.159,
    'η̄':           0.348,
    'sin δ_CKM':   0.91212,
    'cos δ_CKM':   0.40992,
    'δ_CKM/π':     0.36556,
    'sin²θ₁₂':     0.30319,
    'sin²θ₂₃':     0.57131,
    'sin²θ₁₃':     0.022,
    'θ₂₃/π':       0.27278,
    'θ₁₂/π':       0.18560,
    'θ₁₃/π':       0.04744,
    'n_s':         0.9649,
    'Ω_b/Ω_DM':    0.18657,
    'Ω_DM/Ω_b':    5.36,
}

# Magic denominators from exceptional groups + arithmetic geometry
MAGIC_DENOMS = {
    'G2 fund':       7,
    'G2 dim':       14,
    'F4 fund':      26,
    'F4 dim':       52,
    'E6 fund':      27,
    'E6 dim':       78,
    'E7 fund':      56,
    'E7 dim':      133,
    'E8 dim':      248,
    'K3 b_2':       22,
    'K3 b_2 + 1':   23,
    'Niemeier':     24,
    'su(3) dim':     8,
    'su(3) cube':   27,   # = 3³ also E6 fund
    'su(2)⊗su(2)':  12,   # 4 with degeneracies
    'so(10) dim':   45,
    'so(10) fund':  10,
    'Weinberg':     13,
    'Mystery':      17,
}

def matches_p_over_q(target, q, max_err=0.005, p_max=None):
    if p_max is None:
        p_max = max(int(5*q), 30)
    matches = []
    for p in range(1, p_max+1):
        if gcd(p, q) == 1:
            err = abs(p/q - target)/target
            if err < max_err:
                matches.append((p, p/q, err*100))
    if matches:
        matches.sort(key=lambda x: x[2])
        return matches[0]
    return None

print("="*80)
print("CLUSTER STRUCTURE — observations groupées par dénominateur magique")
print("="*80)

cluster_counts = {}
for name, q in MAGIC_DENOMS.items():
    matched_obs = []
    for obs_name, val in SM.items():
        m = matches_p_over_q(val, q, max_err=0.005)
        if m:
            p, pq_val, err = m
            matched_obs.append((obs_name, val, p, pq_val, err))
    cluster_counts[name] = len(matched_obs)
    if matched_obs:
        print(f"\n  /{q} ({name}) : {len(matched_obs)} observables")
        for obs_name, val, p, pq_val, err in matched_obs[:10]:
            print(f"    {obs_name:15s} : {val:.5f} ≈ {p}/{q} = {pq_val:.5f}  ({err:.2f}%)")

print("\n" + "="*80)
print("RANKING")
print("="*80)
sorted_clusters = sorted(cluster_counts.items(), key=lambda x: -x[1])
for name, count in sorted_clusters:
    q = MAGIC_DENOMS[name]
    if count > 0:
        print(f"  {count:2d} obs : /{q:3d} ({name})")

print("\n" + "="*80)
print("PRÉDICTION : exceptional Lie group structure")
print("="*80)

# Build narrative
e6_count = cluster_counts.get('E6 fund', 0)  # /27
k3_count = cluster_counts.get('K3 b_2 + 1', 0)  # /23
g2_count = cluster_counts.get('G2 fund', 0) + cluster_counts.get('G2 dim', 0)  # /7 + /14
f4_count = cluster_counts.get('F4 fund', 0)  # /26
e7_count = cluster_counts.get('E7 fund', 0)  # /56
e8_count = cluster_counts.get('E8 dim', 0)  # /248
mystery_count = cluster_counts.get('Mystery', 0)  # /17

print(f"""
  E6 (27)  : {e6_count} obs  ← (m_Z/v=10/27, sin θ_W=13/27, ...)
  K3 (23)  : {k3_count} obs  ← (A_CKM=19/23, η_bar=8/23, sin δ_CKM=21/23)
  G_2 ({MAGIC_DENOMS['G2 dim']}+{MAGIC_DENOMS['G2 fund']})  : {g2_count} obs  ← (DM candidate ?)
  F_4 (26) : {f4_count} obs
  E_7 (56) : {e7_count} obs
  E_8 (248) : {e8_count} obs
  /17 (Myst) : {mystery_count} obs
""")

if e6_count + k3_count + g2_count >= 10:
    print(f"""
  ★ STRUCTURE EXCEPTIONNELLE ÉMERGENTE :
    Le SM est paramétré par les dimensions de représentations fondamentales de
    GROUPES EXCEPTIONNELS et K3-cohomology.

    Hypothèse : ECI(M = K3, G_total = SU(3)×SU(2)×U(1)×E_6_GUT×G_2_dark)
                où :
                  - K3 fournit la cohomologie /23 pour CKM
                  - E_6 fournit la /27 pour EW (Weinberg, m_Z/v)
                  - G_2 fournit la dim G_dark = 14

    Prédit GUT-like E_6 unification AT HIGH ENERGY (~10^16 GeV).
""")
else:
    print(f"""
  Verdict partiel : 27 émerge comme dénominateur dominant.
  Pourrait être ECI(M=K3) avec /23 cohomologique mais /27 reste à expliquer.
""")

# Plus précis : compter combien fittent à <0.3% strict
print("\n" + "="*80)
print("STRICT — matches à <0.3% par dénominateur magique")
print("="*80)
strict_counts = {}
for name, q in MAGIC_DENOMS.items():
    count = 0
    for obs_name, val in SM.items():
        m = matches_p_over_q(val, q, max_err=0.003)
        if m:
            count += 1
    strict_counts[name] = count

sorted_strict = sorted(strict_counts.items(), key=lambda x: -x[1])
print("Cluster strict (<0.3%) :")
for name, count in sorted_strict:
    if count > 0:
        q = MAGIC_DENOMS[name]
        print(f"  {count:2d} obs : /{q:3d} ({name})")

# Adversarial check : tirer 100 sets random uniformes même taille SM, compter clusters
print("\n" + "="*80)
print("ADVERSARIAL : pour 100 sets random uniformes (taille 35), distribution clusters")
print("="*80)
np.random.seed(2026)
n_trials = 100
cluster_random = {name: [] for name in MAGIC_DENOMS.keys()}
for trial in range(n_trials):
    random_set = np.random.uniform(0.02, 5.5, size=len(SM))
    for name, q in MAGIC_DENOMS.items():
        count = sum(1 for v in random_set if matches_p_over_q(v, q, max_err=0.005))
        cluster_random[name].append(count)

print(f"Random expectations (mean ± std) pour {len(SM)} obs uniformes en [0.02, 5.5] :")
significant = []
for name, q in MAGIC_DENOMS.items():
    obs_count = cluster_counts.get(name, 0)
    rand_mean = np.mean(cluster_random[name])
    rand_std = np.std(cluster_random[name])
    z = (obs_count - rand_mean) / max(rand_std, 0.1)
    marker = "★" if z > 2 else ""
    if z > 1.5:
        significant.append((name, q, obs_count, rand_mean, z))
    print(f"  {marker:2s} /{q:3d} ({name:15s}) : obs={obs_count:2d}, random {rand_mean:.1f}±{rand_std:.1f} → Z={z:+.2f}")

print("\nRÉSULTAT FINAL :")
print(f"  Clusters significants (Z>1.5) : {len(significant)}")
for name, q, obs, rmean, z in sorted(significant, key=lambda x: -x[4]):
    print(f"    Z={z:+.2f} : /{q} ({name}) obs={obs} vs random {rmean:.1f}")
