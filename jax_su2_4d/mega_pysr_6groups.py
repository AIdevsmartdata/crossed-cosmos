#!/usr/bin/env python3
"""
MEGA PySR — 6 gauge groups + Dynkin invariant + ECI anchors
============================================================
Feeds ALL Kevinotron data + ECI Big Table into PySR symbolic regression.
Searches for the formula connecting root system geometry to EE.

Kévin Rémondière (ORCID 0009-0008-2443-7166)
"""

import numpy as np
from scipy.optimize import curve_fit
import json

# ============================================================
# DATASET 1: Kevinotron EE measurements (6 groups)
# ============================================================

# Group properties database
groups = {
    'SU2':  {'dynkin':'A1', 'dim':3,  'C2':2, 'Z':2, 'd_f':2, 'rank':1, 'n_roots':1,  'n_pos_roots':1,  'root_ratio':1.0,  'laced':'simply'},
    'SU3':  {'dynkin':'A2', 'dim':8,  'C2':3, 'Z':3, 'd_f':3, 'rank':2, 'n_roots':6,  'n_pos_roots':3,  'root_ratio':1.0,  'laced':'simply'},
    'SU4':  {'dynkin':'A3', 'dim':15, 'C2':4, 'Z':4, 'd_f':4, 'rank':3, 'n_roots':12, 'n_pos_roots':6,  'root_ratio':1.0,  'laced':'simply'},
    'Sp4':  {'dynkin':'C2', 'dim':10, 'C2':3, 'Z':2, 'd_f':4, 'rank':2, 'n_roots':8,  'n_pos_roots':4,  'root_ratio':1.414,'laced':'doubly'},
    'SO7':  {'dynkin':'B3', 'dim':21, 'C2':5, 'Z':2, 'd_f':7, 'rank':3, 'n_roots':18, 'n_pos_roots':9,  'root_ratio':1.414,'laced':'doubly'},
    'G2':   {'dynkin':'G2', 'dim':14, 'C2':4, 'Z':1, 'd_f':7, 'rank':2, 'n_roots':12, 'n_pos_roots':6,  'root_ratio':1.732,'laced':'triply'},
}

# Weyl group orders
weyl_orders = {'A1':2, 'A2':6, 'A3':24, 'C2':8, 'B3':48, 'G2':12}
for g, props in groups.items():
    props['weyl_order'] = weyl_orders[props['dynkin']]
    props['dual_coxeter'] = props['C2']  # h_v = C2(adj) for simply-connected
    props['n_short'] = props['n_pos_roots'] if props['laced'] == 'simply' else -1  # TODO

# EE data: S2/A at various (beta, L)
# Format: (group, beta, L, S2/A)
ee_data = [
    # SU(2) production (5 volumes)
    ('SU2', 2.50, 4, 7.215), ('SU2', 2.50, 6, 7.165), ('SU2', 2.50, 8, 7.131),
    ('SU2', 2.50, 10, 7.155), ('SU2', 2.50, 12, 7.134),
    # SU(3) production (5 volumes)
    ('SU3', 6.06, 4, 14.169), ('SU3', 6.06, 6, 14.026), ('SU3', 6.06, 8, 14.033),
    ('SU3', 6.06, 10, 14.002), ('SU3', 6.06, 12, 13.985),
    # SU(4) production (5 volumes)
    ('SU4', 10.80, 4, 21.688), ('SU4', 10.80, 6, 21.528), ('SU4', 10.80, 8, 21.528),
    ('SU4', 10.80, 10, 21.536), ('SU4', 10.80, 12, 21.539),
    # G2 production (4 volumes + multi-beta)
    ('G2', 10.0, 4, 18.303), ('G2', 10.0, 6, 18.085), ('G2', 10.0, 10, 18.080), ('G2', 10.0, 12, 18.087),
    ('G2', 9.6, 4, 15.993), ('G2', 9.6, 6, 15.673), ('G2', 9.6, 8, 15.648),
    ('G2', 9.8, 4, 17.226), ('G2', 9.8, 6, 16.931), ('G2', 9.8, 8, 16.863),
    ('G2', 10.2, 4, 19.213), ('G2', 10.2, 6, 19.185), ('G2', 10.2, 8, 19.242),
    ('G2', 10.4, 4, 20.481), ('G2', 10.4, 6, 20.368), ('G2', 10.4, 8, 20.389),
    # Sp(4) production (3 volumes)
    ('Sp4', 8.0, 4, 20.674), ('Sp4', 8.0, 6, 20.617), ('Sp4', 8.0, 8, 20.566),
    # Sp(4) beta scan (L=4 quick estimates from Simpson)
    ('Sp4', 6.0, 4, 10.29), ('Sp4', 10.0, 4, 33.72), ('Sp4', 12.0, 4, 44.86), ('Sp4', 14.0, 4, 55.59),
    # SO(7) production (3 volumes)
    ('SO7', 20.0, 4, 56.383), ('SO7', 20.0, 6, 56.105), ('SO7', 20.0, 8, 56.197),
    # SO(7) beta scan (L=4 quick estimates)
    ('SO7', 10.0, 4, 9.67), ('SO7', 15.0, 4, 30.18), ('SO7', 25.0, 4, 89.85),
    ('SO7', 30.0, 4, 116.53), ('SO7', 40.0, 4, 170.06),
]

# ============================================================
# COMPUTE DERIVED QUANTITIES
# ============================================================

print("=" * 70)
print("MEGA ANALYSIS — 6 GAUGE GROUPS")
print("=" * 70)

# 1. S2/A/beta (Dynkin invariant) — use L>=6 points for stability
print("\n--- DYNKIN INVARIANT: S2/A/beta ---")
for gname, ginfo in groups.items():
    pts = [(b, s) for g, b, L, s in ee_data if g == gname and L >= 6]
    if len(pts) >= 2:
        betas = np.array([p[0] for p in pts])
        s2a = np.array([p[1] for p in pts])
        slope = np.mean(s2a / betas)
        slope_std = np.std(s2a / betas)
        ginfo['slope'] = slope
        print(f"  {gname:>4} ({ginfo['dynkin']:>2}): S2/A/β = {slope:.4f} ± {slope_std:.4f}  "
              f"(dim={ginfo['dim']}, C2={ginfo['C2']}, |Z|={ginfo['Z']}, rank={ginfo['rank']}, "
              f"root_ratio={ginfo['root_ratio']:.3f}, |W|={ginfo['weyl_order']})")

# 2. Test formulas for the slope
print("\n--- FORMULA SEARCH for S2/A/beta ---")
slopes = []
features = []
for gname in ['SU2','SU3','SU4','Sp4','SO7','G2']:
    g = groups[gname]
    if 'slope' in g:
        slopes.append(g['slope'])
        features.append([g['dim'], g['C2'], np.log(max(g['Z'],1)), g['rank'],
                        g['n_pos_roots'], g['root_ratio'], g['weyl_order'],
                        g['d_f'], g['dim']/g['d_f']])

slopes = np.array(slopes)
features = np.array(features)
labels = ['dim','C2','lnZ','rank','n_pos_roots','root_ratio','|W|','d_f','dim/d_f']

# Try each single feature
print("\n  Single-feature correlations with S2/A/β:")
for i, label in enumerate(labels):
    x = features[:, i]
    if np.std(x) > 1e-10:
        corr = np.corrcoef(slopes, x)[0, 1]
        print(f"    {label:>12}: r = {corr:+.4f}")

# Try ratios and products
print("\n  Derived feature correlations:")
derived = {
    'dim/C2': features[:,0]/features[:,1],
    'C2/rank': features[:,1]/features[:,3],
    'dim/rank': features[:,0]/features[:,3],
    'd_f/rank': features[:,7]/features[:,3],
    'root_ratio*rank': features[:,5]*features[:,3],
    '1/n_pos_roots': 1.0/features[:,4],
    'dim/(|W|*root_ratio)': features[:,0]/(features[:,6]*features[:,5]),
    'C2*root_ratio': features[:,1]*features[:,5],
    'd_f*root_ratio/dim': features[:,7]*features[:,5]/features[:,0],
}
for name, x in derived.items():
    if np.std(x) > 1e-10:
        corr = np.corrcoef(slopes, x)[0, 1]
        if abs(corr) > 0.7:
            print(f"    {name:>25}: r = {corr:+.4f} ***")
        else:
            print(f"    {name:>25}: r = {corr:+.4f}")

# 3. Best linear model
print("\n--- BEST LINEAR MODEL ---")
from itertools import combinations
best_r2 = -1
best_model = None
n = len(slopes)
for ncols in [1, 2, 3]:
    for cols in combinations(range(len(labels)), ncols):
        X = np.column_stack([features[:, c] for c in cols])
        X = np.column_stack([X, np.ones(n)])
        try:
            coeffs, res, _, _ = np.linalg.lstsq(X, slopes, rcond=None)
            pred = X @ coeffs
            ss_res = np.sum((slopes - pred)**2)
            ss_tot = np.sum((slopes - np.mean(slopes))**2)
            r2 = 1 - ss_res / ss_tot
            if r2 > best_r2:
                best_r2 = r2
                best_model = (cols, coeffs, r2)
                best_labels = [labels[c] for c in cols]
        except:
            pass

cols, coeffs, r2 = best_model
print(f"  Best model (R²={r2:.6f}):")
formula = " + ".join([f"{coeffs[i]:.4f}*{best_labels[i]}" for i in range(len(cols))])
formula += f" + {coeffs[-1]:.4f}"
print(f"  S2/A/β = {formula}")

for i, gname in enumerate(['SU2','SU3','SU4','Sp4','SO7','G2']):
    if 'slope' in groups[gname]:
        X_row = np.array([features[i, c] for c in cols] + [1.0])
        pred = X_row @ coeffs
        obs = slopes[i]
        print(f"    {gname:>4}: pred={pred:.4f}  obs={obs:.4f}  Δ={100*(obs-pred)/obs:+.1f}%")

# ============================================================
# DATASET 2: ECI Big Table anchors
# ============================================================
print("\n" + "=" * 70)
print("ECI ANCHORS — checking if Dynkin slope connects to SM")
print("=" * 70)

# Known ECI relations involving gauge groups
eci_anchors = {
    'm_H/v = kappa(SU(2))': {'group': 'SU2', 'value': 0.5080, 'obs': 125.10/246.22, 'delta_pct': 0.016},
    'sin2_theta_W = 3/13': {'value': 3/13, 'obs': 0.23122, 'delta_pct': 0.06},
    'alpha_s = 2/17': {'value': 2/17, 'obs': 0.1179, 'delta_pct': 0.13},
}

# Can we relate slope(A1)=2.89 to kappa(SU(2))=0.508 ?
slope_su2 = groups['SU2'].get('slope', 2.89)
kappa_su2 = 0.5080
print(f"\n  slope(SU(2)) = {slope_su2:.4f}")
print(f"  kappa(SU(2)) = {kappa_su2:.4f}")
print(f"  slope/kappa = {slope_su2/kappa_su2:.4f}")
print(f"  slope * kappa = {slope_su2*kappa_su2:.4f}")
print(f"  slope / (2*pi) = {slope_su2/(2*np.pi):.4f}")
print(f"  slope / dim(SU2) = {slope_su2/3:.4f}")

# Check if slope ratios match any known constants
print("\n  Slope ratios between groups:")
for g1 in ['SU2','SU3','SU4','Sp4','SO7','G2']:
    for g2 in ['SU2','SU3','SU4','Sp4','SO7','G2']:
        if g1 >= g2:
            continue
        s1 = groups[g1].get('slope', 0)
        s2 = groups[g2].get('slope', 0)
        if s1 > 0 and s2 > 0:
            r = s1/s2
            print(f"    {g1}/{g2} = {r:.4f}", end="")
            # Check against simple rationals p/q with p,q <= 10
            for p in range(1, 11):
                for q in range(1, 11):
                    if abs(r - p/q) < 0.02:
                        print(f"  ≈ {p}/{q} ({100*abs(r-p/q)/(p/q):.2f}%)", end="")
            print()

# ============================================================
# SAVE FOR PYSR
# ============================================================
print("\n" + "=" * 70)
print("PYSR-READY DATASET SAVED")
print("=" * 70)

pysr_data = {
    'groups': {k: v for k, v in groups.items()},
    'ee_data': ee_data,
    'slopes': {gname: groups[gname].get('slope', None) for gname in groups},
}
with open('/root/cc-private/jax_su2_4d/pysr_6groups_data.json', 'w') as f:
    json.dump(pysr_data, f, indent=2, default=str)
print("  Saved to pysr_6groups_data.json")
print(f"  {len(ee_data)} EE data points, 6 groups, {len(labels)} features")
