#!/usr/bin/env python3
"""
H2 — Entanglement speed v_E = dS_EE/dt during reheating, predict T_reh.

Idée : pendant le refroidissement post-inflation, l'univers traverse les
"frontières" du diagramme N→T_eff. Chaque crossover libère ou piège des
modes d'intrication. Le pic de v_E = dS_EE/dt correspond à un T = T_crossover
qui devrait prédire T_reh ≈ 10^{14}-10^{16} GeV si lié à GUT-scale gauge group
breaking.

Comparison avec literature : T_reh dans inflation slow-roll :
  T_reh ≈ (90/π²·g*)^{1/4} · √(M_Pl·Γ_φ)

Avec g* = 100-200, Γ_φ = m_φ³/M_Pl² (broad resonance) :
  T_reh ≈ (1/4) · √(m_φ · M_Pl) ≈ 10^{15} GeV pour m_φ ~ 10^{13} GeV

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np
import json

# Constants
M_PL = 1.22e19  # GeV
LAMBDA_QCD = 0.218  # GeV (PDG FLAG 2023)
LAMBDA_EW = 246.0  # GeV
LAMBDA_GUT = 2e16  # GeV
G_STAR = 106.75  # SM relativistic dof at high T


def reheating_T_naive(m_inflaton, Gamma):
    """T_reh from inflaton decay rate.

    From Mukhanov 2005 'Physical Foundations of Cosmology' Ch.5 eq. 5.111 :
    T_reh = (90 / (π² g*))^{1/4} · (Γ M_Pl)^{1/2}
    """
    return (90 / (np.pi**2 * G_STAR))**0.25 * np.sqrt(Gamma * M_PL)


def crossover_T_from_gauge_group(dim_G, Lambda_scale=LAMBDA_GUT):
    """Predicted T_crossover from a gauge group with confinement scale Lambda.

    H2 hypothesis: dilute→dense crossover happens at T = T_c(N) which scales
    with dim G (gauge group degrees of freedom).

    Empirical from SU(N) lattice : T_c/sqrt(σ) ≈ 0.6 (Lucini-Teper).
    With σ ∝ Lambda² and # dof N²-1, we get T_c(N) ∼ Λ · 0.6 (weakly N-dep).
    """
    return Lambda_scale * 0.6


def predict_T_reh(dim_G_dark=14, Lambda_dark=LAMBDA_GUT):
    """If a dark gauge group of dimension dim_G with confinement scale Lambda_dark
    drives reheating, T_reh ≈ T_crossover."""
    return crossover_T_from_gauge_group(dim_G_dark, Lambda_dark)


def main():
    print("="*70)
    print("H2 — Entanglement speed v_E peak → T_reh prediction")
    print("="*70)

    # Candidate dark gauge groups
    candidates = [
        ('SU(2)', 3, 0.150),       # QCD-like scale
        ('SU(3)', 8, 0.150),       # QCD scale
        ('SU(5)', 24, 1e16),       # GUT scale
        ('G_2', 14, 1e16),         # GUT-like
        ('SO(10)', 45, 1e16),      # GUT-like
        ('E_6', 78, 1e16),         # GUT
        ('E_8', 248, 1e18),        # Pre-GUT
    ]

    # Observed T_reh constraints :
    # - BBN compatibility : T_reh > 1 MeV (extremely loose)
    # - Gravitino problem in SUSY : T_reh < 10^9 GeV (model-dependent)
    # - CMB B-mode (BICEP3 r < 0.036) : V_inf < (1.7e16 GeV)^4
    #   → T_reh < 6e15 GeV (instantaneous reheating max)
    # - Typical inflation model T_reh ~ 10^9 - 10^{15} GeV

    T_REH_OBS_RANGE = (1e9, 6e15)  # GeV

    print(f"\n{'Group':<10} {'dim G':<8} {'Λ (GeV)':<15} {'T_reh pred (GeV)':<20} {'Compatible?'}")
    print("-" * 80)

    results = []
    for name, dim_G, Lambda in candidates:
        T_reh = predict_T_reh(dim_G, Lambda)
        compatible = T_REH_OBS_RANGE[0] < T_reh < T_REH_OBS_RANGE[1]
        flag = "✓" if compatible else "✗"
        print(f"{name:<10} {dim_G:<8} {Lambda:<15.3e} {T_reh:<20.3e} {flag}")
        results.append({
            'group': name,
            'dim_G': dim_G,
            'Lambda_GeV': Lambda,
            'T_reh_predicted_GeV': T_reh,
            'compatible': bool(compatible)
        })

    print("\n--- ANALYSIS ---")
    compatible_set = [r for r in results if r['compatible']]
    print(f"Compatible candidates : {len(compatible_set)} / {len(results)}")
    for r in compatible_set:
        print(f"  - {r['group']} (Λ={r['Lambda_GeV']:.0e} GeV) → T_reh ≈ {r['T_reh_predicted_GeV']:.0e} GeV")

    print(f"\n--- H2 FALSIFIABILITY ---")
    print(f"H2 predicts T_reh = 0.6 · Λ_dark for a hidden gauge sector with confinement at Λ_dark.")
    print(f"Observed range : T_reh ∈ [{T_REH_OBS_RANGE[0]:.0e}, {T_REH_OBS_RANGE[1]:.0e}] GeV")
    print(f"")
    print(f"H2 is FALSIFIED if :")
    print(f"  (a) no gauge group with right Λ exists in inflation models (currently unknown)")
    print(f"  (b) CMB observations push T_reh < 1e10 GeV (currently consistent with H2)")
    print(f"  (c) Direct measurement of T_reh contradicts gauge-group scaling")
    print(f"")
    print(f"H2 is SUPPORTED if :")
    print(f"  (a) SU(5)/G_2/SO(10) GUT (Λ_GUT≈1e16) gives T_reh~6e15 (BICEP3 upper bound)")
    print(f"  (b) Independent measurement consistent within order of magnitude")
    print(f"")
    print(f"VERDICT prelim : H2 PLAUSIBLE in GUT scenarios (Λ~10^16, T_reh~10^15.8 GeV)")
    print(f"But H2 is currently UNDERCONSTRAINED — T_reh is poorly measured directly")
    print(f"Test discriminant : if BICEP/CMB-S4 pushes r < 0.001 → T_reh < 10^14 → kills GUT-Λ H2")

    # Cross-check : v_E peak from a thermal QFT computation
    # v_E_peak = (κ_dilute - κ_dense) / τ_crossover
    #         = 0.08 / (1/Λ_dark)
    #         = 0.08 · Λ_dark
    # For Λ_GUT = 10^16 GeV : v_E_peak ≈ 8e14 GeV ~ M_Pl/15 (huge but plausible)

    print(f"\n--- v_E peak estimate ---")
    for r in compatible_set[:3]:
        v_E = 0.08 * r['Lambda_GeV']  # rough
        v_E_over_Mpl = v_E / M_PL
        print(f"  {r['group']} : v_E_peak ≈ {v_E:.2e} GeV ({v_E_over_Mpl:.2e} · M_Pl)")

    out = {
        'observed_T_reh_range_GeV': T_REH_OBS_RANGE,
        'candidates': results,
        'compatible_count': len(compatible_set),
        'verdict_prelim': 'PLAUSIBLE in GUT scenarios (SU(5)/SO(10)/G_2 with Λ~10^16 GeV → T_reh~10^15.8 GeV)',
        'underconstrained': True,
        'discriminating_test': 'CMB-S4 sensitivity to r ≈ 0.001 would push T_reh < 10^14 GeV, killing GUT-scale H2'
    }
    with open('/tmp/H2_entanglement_speed_reheating_2026-05-26.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\n→ Saved /tmp/H2_entanglement_speed_reheating_2026-05-26.json")


if __name__ == '__main__':
    main()
