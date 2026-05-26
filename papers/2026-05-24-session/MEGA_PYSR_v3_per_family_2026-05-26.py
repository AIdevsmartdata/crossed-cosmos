#!/usr/bin/env python3
"""
MEGA PySR v3 — per-family symbolic regression (correct approach).

3 families with per-row varying features :
  F1 : Charged leptons mass hierarchy (m_e, m_μ, m_τ) — feature : generation index
  F2 : Quark mass hierarchy (m_d/u, m_s/c, m_b/t) — feature : isospin + generation
  F3 : Lattice anchors κ_EE(N) cross-N — feature : N

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np
import pandas as pd
from pysr import PySRRegressor
import json

# ============================================================
# F1 : Charged leptons m_l / v  (3 datapoints)
# ============================================================
F1_data = [
    (1, 0.5110e-3/246.22, 0.000002),     # electron
    (2, 0.10566/246.22,    0.000002),    # muon
    (3, 1.7768/246.22,     0.0001),      # tau
]

# F2 : Up-type quarks  m_q / v
F2_up = [
    (1, 2.16e-3/246.22, 5e-7),    # up
    (2, 1.27/246.22,    0.02/246.22),  # charm
    (3, 172.57/246.22,  0.30/246.22),  # top
]

# F3 : Down-type quarks
F3_down = [
    (1, 4.67e-3/246.22, 5e-7),    # down
    (2, 93.4e-3/246.22, 8e-7),    # strange
    (3, 4.18/246.22,    0.03/246.22),  # bottom
]

# F4 : Lattice anchors κ_EE(N)
F4_lattice = [
    (2, 0.508,   0.005),
    (3, 0.603,   0.005),
    (4, 0.633,   0.004),
    (5, 0.7012,  0.006),
    (6, 0.810,   0.005),
    (7, 0.9107,  0.0054),
    (8, 1.0416,  0.0046),
    (9, 1.1764,  0.0047),
    (10, 1.3307, 0.0048),
]


def run_pysr_family(family_name, data, extra_feats=None):
    """Run PySR on one family with index as varying feature."""
    print(f"\n{'='*70}\nFamily : {family_name}  ({len(data)} points)\n{'='*70}")
    Ns = np.array([d[0] for d in data], dtype=float)
    Ys = np.array([d[1] for d in data])
    Es = np.array([d[2] for d in data])
    weights = 1.0/Es**2

    # Features : varying per row
    feats = {
        'gen':   Ns,           # generation/N index
        'g_sq':  Ns**2,
        'inv_g': 1/Ns,
        'g_log': np.log(Ns),
        'g_exp': np.exp(-Ns),
        'g_53':  Ns**(5/3),    # K41 candidate
        'g_dim': Ns**2 - 1,    # dim su(N)
        'g_sqrt': np.sqrt(Ns),
    }
    if extra_feats:
        feats.update(extra_feats(Ns))
    X_df = pd.DataFrame(feats)

    model = PySRRegressor(
        niterations=150,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sqrt", "log", "exp", "square"],
        maxsize=15,
        maxdepth=6,
        populations=30,
        population_size=40,
        ncycles_per_iteration=500,
        elementwise_loss="(prediction, target, weight) -> weight * (prediction - target)^2",
        progress=False,
        random_state=42,
        deterministic=True,
        parallelism="serial",
        output_directory=f"/tmp/MEGA_PYSR_v3_{family_name}_out",
        run_id=f"{family_name}",
    )
    model.fit(X_df, Ys, weights=weights)
    print(f"\n=== TOP 8 formulas for {family_name} ===")
    print(model.equations_[['complexity', 'loss', 'equation']].head(8).to_string())
    return model.equations_[['complexity', 'loss', 'equation']].head(8).to_dict('records')


def main():
    results = {}
    results['leptons'] = run_pysr_family('leptons', F1_data)
    results['up_quarks'] = run_pysr_family('up_quarks', F2_up)
    results['down_quarks'] = run_pysr_family('down_quarks', F3_down)
    results['lattice_kappa'] = run_pysr_family('lattice_kappa', F4_lattice)

    with open('/tmp/MEGA_PYSR_v3_per_family_summary.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n→ Saved /tmp/MEGA_PYSR_v3_per_family_summary.json")


if __name__ == '__main__':
    main()
