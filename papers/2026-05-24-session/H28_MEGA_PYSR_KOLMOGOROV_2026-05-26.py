#!/usr/bin/env python3
"""
H28 — MEGA PySR sur κ_EE(N) avec features Kolmogorov-motivées.

Données : SU(2-8) post-THERM5000 plateau values.

Features physiquement motivées :
- N           : group rank
- sqrt_N      : KAolmogorov √ (string network rigide)
- N_53        : N^{5/3} Kolmogorov K41
- N_23        : N^{2/3} (related K41)
- dim_G       : N²-1 (dimension de l'algèbre)
- inv_N       : 1/N (subleading correction)
- inv_N2      : 1/N² (1-1/N²) factor for dilute
- C2          : Casimir 2nd-order (N²-1)/(2N)
- log_N       : log(N)
- one_m_invN2 : 1 - 1/N² (dilute prefactor)
- zeta3_sqrt_pi : ζ(3)/√π = κ_∞ dilute asymptote
- dim_root    : √(N²-1)
- Casimir_adj : N (Casimir adjoint)

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np
from pysr import PySRRegressor
import json

# Latest plateau data
KAPPA_DATA = [
    (2, 0.508, 0.005),
    (3, 0.603, 0.005),
    (4, 0.633, 0.004),
    (5, 0.7012, 0.0060),
    (6, 0.810, 0.005),
    (7, 0.9107, 0.0054),
    (8, 1.0416, 0.0046),
]

ZETA3 = 1.2020569
KAPPA_INF = ZETA3 / np.sqrt(np.pi)


def make_features(Ns):
    """Build feature matrix from list of N values."""
    Ns = np.asarray(Ns, dtype=float)
    return {
        'Nc': Ns,
        'sqrtNc': np.sqrt(Ns),
        'Nc_53': Ns**(5/3),
        'Nc_23': Ns**(2/3),
        'dimG': Ns**2 - 1,
        'invNc': 1/Ns,
        'invNc2': 1/Ns**2,
        'C2_fund': (Ns**2 - 1)/(2*Ns),
        'logNc': np.log(Ns),
        'one_m_invNc2': 1 - 1/Ns**2,
        'kappa_dilute': KAPPA_INF * (1 - 1/Ns**2),
        'sqrt_dimG': np.sqrt(Ns**2 - 1),
        'Nc_minus_2': Ns - 2,
        'log_dimG': np.log(Ns**2 - 1 + 1e-6),
        # f^{abc} cascade features (color turbulence)
        'dimG_56': (Ns**2 - 1)**(5/6),  # = N^{5/3} for large N
        'dimG_23': (Ns**2 - 1)**(2/3),  # K41 ε^{2/3} signature
        'roots_count': Ns * (Ns-1),  # |Φ+| positive roots
    }


def main():
    Ns = np.array([d[0] for d in KAPPA_DATA], dtype=float)
    kappas = np.array([d[1] for d in KAPPA_DATA])
    kappa_errs = np.array([d[2] for d in KAPPA_DATA])

    feats = make_features(Ns)
    # X matrix : rows = data points, cols = features
    feature_names = list(feats.keys())
    X = np.column_stack([feats[k] for k in feature_names])

    print(f"Data points: {len(Ns)}, features: {len(feature_names)}")
    print(f"κ data: {kappas}")
    print(f"Features used: {feature_names}")

    # PySR config — focus on simple formulas
    model = PySRRegressor(
        niterations=200,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sqrt", "log", "exp", "square"],
        maxsize=20,
        maxdepth=8,
        populations=30,
        population_size=50,
        ncycles_per_iteration=500,
        elementwise_loss="(prediction, target, weight) -> weight * (prediction - target)^2",
        progress=False,
        random_state=42,
        deterministic=True,
        parallelism="serial",  # avoid race in jit cache
        output_directory="/tmp/H28_pysr_out",
        run_id="MEGA_KAPPA_KOLMOGOROV",
    )

    print("Starting PySR mega run...")
    import pandas as pd
    X_df = pd.DataFrame(X, columns=feature_names)
    model.fit(X_df, kappas, weights=1/kappa_errs**2)

    # Best results
    print("\n=== Best formulas ===")
    print(model.equations_.to_string())

    # Test predictions for SU(9), SU(10)
    print("\n=== Predictions for SU(9), SU(10), SU(11), SU(12) ===")
    Npred = np.array([9, 10, 11, 12], dtype=float)
    Xpred_df = pd.DataFrame({k: make_features(Npred)[k] for k in feature_names})
    Xpred = Xpred_df.values

    for i in range(min(8, len(model.equations_))):
        eq = model.equations_.iloc[i]
        try:
            pred = model.predict(Xpred_df, index=i)
            print(f"  Complexity {eq.complexity}: loss={eq.loss:.6f}")
            print(f"    Eq: {eq.equation}")
            print(f"    SU(9)={pred[0]:.4f}, SU(10)={pred[1]:.4f}, SU(11)={pred[2]:.4f}, SU(12)={pred[3]:.4f}")
        except Exception as e:
            print(f"  Prediction error: {e}")

    # Save summary
    summary = {
        'data': KAPPA_DATA,
        'kappa_inf_dilute_constant': KAPPA_INF,
        'predictions_5_3_fit': {
            9: 1.1745, 10: 1.3191, 11: 1.4736, 12: 1.6379
        },
        'predictions_affine_fit': {
            9: 1.131, 10: 1.224
        },
        'note': 'Best PySR formula should be tested against SU(9), SU(10) lattice measurements (running)'
    }
    with open('/tmp/H28_MEGA_PYSR_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\n→ Saved /tmp/H28_MEGA_PYSR_summary.json")


if __name__ == '__main__':
    main()
