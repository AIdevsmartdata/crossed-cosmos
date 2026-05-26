#!/usr/bin/env python3
"""
MEGA PySR v2 — search rational/structural formulas for SM observables.

Targets : 25 SM observables (masses, couplings, CKM, PMNS, cosmo, lattice anchors).
Features : 40 structural (SU(N), K3, Casimirs, primes, transcendentals).

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np
import pandas as pd
from pysr import PySRRegressor
import json

# Targets : (name, value, σ)
OBS = [
    # Lattice anchors (high precision)
    ('kappa_FP',        1/6,        0.001),
    ('F_inf',           9/10,       0.005),
    ('xi_star',         2/3,        0.005),
    ('K41_exp',         5/3,        0.005),
    # Higgs
    ('m_H_over_v',      125.10/246.22,  0.0005),
    ('m_W_over_v',      80.379/246.22,  0.0001),
    ('m_Z_over_v',      91.1876/246.22, 0.0001),
    ('m_t_over_v',      172.57/246.22,  0.003),
    ('m_b_over_v',      4.18/246.22,    0.0008),
    ('m_tau_over_v',    1.7768/246.22,  0.0001),
    ('m_mu_over_v',     0.10566/246.22, 0.000002),
    # Couplings (PDG @ M_Z)
    ('alpha_em_MZ',     1/127.951,      0.0001),
    ('alpha_s_MZ',      0.1179,         0.001),
    ('sin2_theta_W',    0.23121,        0.00004),
    # CKM
    ('lambda_wolf',     0.22500,        0.00067),
    ('A_wolf',          0.826,          0.012),
    ('Vus',             0.2253,         0.0008),
    ('Vcb',             0.0410,         0.0014),
    # PMNS
    ('sin2_th12_pmns',  0.307,          0.013),
    ('sin2_th23_pmns',  0.546,          0.021),
    ('sin2_th13_pmns',  0.0220,         0.0007),
    # Cosmo
    ('n_s',             0.965,          0.004),
    ('h',               0.674,          0.005),
    ('Omega_DM_over_b', 5.36,           0.15),
    ('h2_Omega_DM',     0.120,          0.001),
]

# Features : Group/topology/transcendental data
def make_features(n_rows):
    # All features as scalar constants (one per obs) since we don't have per-obs scaling
    # Standard SU(N) data for N=2..10 + special groups
    base = {
        # Powers of small integers
        'two':         np.full(n_rows, 2.0),
        'three':       np.full(n_rows, 3.0),
        'four':        np.full(n_rows, 4.0),
        'five':        np.full(n_rows, 5.0),
        'six':         np.full(n_rows, 6.0),
        'seven':       np.full(n_rows, 7.0),
        'eight':       np.full(n_rows, 8.0),
        'nine':        np.full(n_rows, 9.0),
        'thirteen':    np.full(n_rows, 13.0),
        # Group dims
        'dim_SU2':     np.full(n_rows, 3.0),
        'dim_SU3':     np.full(n_rows, 8.0),
        'dim_SU4':     np.full(n_rows, 15.0),
        'dim_SU5':     np.full(n_rows, 24.0),
        'dim_G2':      np.full(n_rows, 14.0),
        'dim_F4':      np.full(n_rows, 52.0),
        'dim_E6':      np.full(n_rows, 78.0),
        'dim_E7':      np.full(n_rows, 133.0),
        'dim_E8':      np.full(n_rows, 248.0),
        # State spaces (SU(N) total)
        'st_SU3':      np.full(n_rows, 13.0),  # 3+8+2
        'st_SU5':      np.full(n_rows, 33.0),  # 5+24+4
        # K3 invariants
        'b2_K3':       np.full(n_rows, 22.0),
        'chi_K3':      np.full(n_rows, 24.0),
        # Transcendentals
        'pi_inv':      np.full(n_rows, 1/np.pi),
        'inv_4pi2':    np.full(n_rows, 1/(4*np.pi**2)),
        'zeta3':       np.full(n_rows, 1.2020569),
        'kappa_inf':   np.full(n_rows, 1.2020569/np.sqrt(np.pi)),
        # Inverses of small ints
        'inv2':        np.full(n_rows, 0.5),
        'inv3':        np.full(n_rows, 1/3),
        'inv4':        np.full(n_rows, 0.25),
        'inv6':        np.full(n_rows, 1/6),
        'inv8':        np.full(n_rows, 1/8),
        'inv13':       np.full(n_rows, 1/13),
        'inv24':       np.full(n_rows, 1/24),
        'inv25':       np.full(n_rows, 1/25),
        # Mass-scale ratios (lattice quantities)
        'log_mP':      np.full(n_rows, np.log(1.22e19)),
        # K41
        'p_K41':       np.full(n_rows, 5/3),
        # b_0 SU(3) one-loop
        'b0_SU3':      np.full(n_rows, 11/(3)),
        # Casimirs SU(N)
        'C2F_SU3':     np.full(n_rows, 4/3),  # (3²-1)/(2·3)
        'C2A_SU3':     np.full(n_rows, 3.0),  # N
    }
    return base


def main():
    names = [o[0] for o in OBS]
    vals = np.array([o[1] for o in OBS])
    errs = np.array([o[2] for o in OBS])
    weights = 1 / errs**2

    print(f"MEGA PySR v2 launched")
    print(f"Targets : {len(OBS)} SM observables")

    feats = make_features(len(OBS))
    X_df = pd.DataFrame(feats)
    feature_names = list(feats.keys())
    print(f"Features : {len(feature_names)} structural")

    model = PySRRegressor(
        niterations=300,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sqrt", "log", "exp", "square"],
        maxsize=25,
        maxdepth=10,
        populations=40,
        population_size=60,
        ncycles_per_iteration=500,
        elementwise_loss="(prediction, target, weight) -> weight * (prediction - target)^2",
        progress=False,
        random_state=42,
        deterministic=True,
        parallelism="serial",
        output_directory="/tmp/MEGA_PYSR_v2_out",
        run_id="MEGA_v2_SM",
    )

    print("Starting PySR mega-run v2...")
    model.fit(X_df, vals, weights=weights)

    print("\n=== TOP 15 FORMULAS (par loss) ===")
    print(model.equations_[['complexity', 'loss', 'equation']].head(15).to_string())

    # Save summary
    eq_list = model.equations_[['complexity', 'loss', 'equation']].to_dict('records')
    summary = {
        'targets': [(n, v, e) for n, v, e in OBS],
        'features': feature_names,
        'equations_top15': eq_list[:15],
    }
    with open('/tmp/MEGA_PYSR_v2_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n→ Saved /tmp/MEGA_PYSR_v2_summary.json")


if __name__ == '__main__':
    main()
