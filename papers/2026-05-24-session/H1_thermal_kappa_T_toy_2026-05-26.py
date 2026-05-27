#!/usr/bin/env python3
"""
H1 — Toy calc : κ_EE(T) thermique pour SU(3) via mapping N→T_eff.

L'idée : le crossover N=4→5 statique à T=0 correspond à un crossover thermique
à T~T_c pour SU(3) fixé. Mapping :
    "régime dilué" (N≤4 ou T<T_c) → κ_EE ≈ (1-1/N²)·ζ(3)/√π
    "régime dense" (N≥5 ou T>T_c) → κ_EE ≈ 0.518·√N − 0.458

Pour le thermal, on remplace N par N_eff(T) où :
    N_eff(T) = N_phys + ΔN(T/T_c)
avec ΔN(T) = step function smoothée à T_c.

Prédiction : κ_EE(T) doit chuter brusquement à T_c (déconfinement libère les
ddl et fait revenir au régime dilué).

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import numpy as np
import json

# Constants
ZETA3 = 1.2020569
KAPPA_INF = ZETA3 / np.sqrt(np.pi)  # = 0.6782


def kappa_dilute(N):
    """Régime dilué N≤4 : κ = (1-1/N²)·ζ(3)/√π"""
    return (1 - 1/N**2) * KAPPA_INF


def kappa_dense(N):
    """Régime dense N≥5 : κ = 0.518·√N − 0.458"""
    return 0.518 * np.sqrt(N) - 0.458


def kappa_smooth_crossover(N, N_c=4.5, width=0.5):
    """Smooth crossover entre dilué et dense centré N_c."""
    # Sigmoid weighting
    w_dense = 1.0 / (1 + np.exp(-(N - N_c) / width))
    return (1 - w_dense) * kappa_dilute(N) + w_dense * kappa_dense(N)


def N_eff_thermal(T, T_c=150.0, N_phys=3, dN_max=2.5, T_width=30.0):
    """N_eff(T) : monte de N_phys=3 (dilué) à 3+dN_max au-dessus de T_c.

    Interprétation : à T>T_c, les degrés de liberté de jauge se libèrent,
    accroissant l'effective dimension du groupe pour la mesure d'intrication.
    Mais notre crossover est INVERSE — à T>T_c on retourne au DILUÉ, pas au dense.
    """
    # ATTENTION : pour le thermique, c'est l'INVERSE :
    # T<T_c (confiné) ↔ N≥5 dense
    # T>T_c (déconfiné) ↔ N≤4 dilué (libération ddl individuels)
    # Donc on diminue N_eff avec T.
    w_deconf = 1.0 / (1 + np.exp(-(T - T_c) / T_width))
    return 5.0 - (5.0 - N_phys) * w_deconf  # 5 à T<<T_c, 3 à T>>T_c


def main():
    print("="*70)
    print("H1 — Toy calc thermal κ_EE(T) for SU(3) QCD")
    print("="*70)

    # Sweep T from 50 to 400 MeV
    T_array = np.linspace(50, 400, 36)
    T_c = 150.0  # Lattice QCD value (Bazavov, HotQCD, etc.)

    results = []
    for T in T_array:
        N_eff = N_eff_thermal(T, T_c=T_c)
        kappa = kappa_smooth_crossover(N_eff)
        results.append({'T_MeV': float(T), 'N_eff': float(N_eff), 'kappa_EE': float(kappa)})

    # Print results
    print(f"\n{'T (MeV)':<10} {'N_eff':<10} {'κ_EE':<10}")
    print("-" * 30)
    for r in results[::3]:  # Every 3rd point
        print(f"{r['T_MeV']:<10.0f} {r['N_eff']:<10.3f} {r['kappa_EE']:<10.4f}")

    # Find inflection / max-derivative
    kappa_arr = np.array([r['kappa_EE'] for r in results])
    T_arr = np.array([r['T_MeV'] for r in results])
    dkappa_dT = np.gradient(kappa_arr, T_arr)
    idx_max = np.argmax(np.abs(dkappa_dT))
    T_inflection = T_arr[idx_max]

    print(f"\n--- KEY METRICS ---")
    print(f"Régime confined (T=50 MeV)    : κ_EE = {results[0]['kappa_EE']:.4f}  N_eff = {results[0]['N_eff']:.2f}")
    print(f"Régime déconfined (T=400 MeV) : κ_EE = {results[-1]['kappa_EE']:.4f}  N_eff = {results[-1]['N_eff']:.2f}")
    print(f"Δκ_EE = {results[0]['kappa_EE'] - results[-1]['kappa_EE']:.4f}")
    print(f"T_inflection = {T_inflection:.1f} MeV (vs T_c lattice = {T_c} MeV)")

    # Sanity check : la H1 prédit un drop net à T_c
    drop_size = results[0]['kappa_EE'] - results[-1]['kappa_EE']
    print(f"\nH1 PREDICTION SUMMARY :")
    print(f"  Drop magnitude Δκ_EE = {drop_size:.4f}")
    print(f"    Si > 0.10 : signal détectable lattice")
    print(f"    Si < 0.05 : trop subtil pour méthode BP2008b")
    print(f"  Position T_inflection = {T_inflection:.0f} MeV")
    print(f"    Si match T_c=150 MeV ±50% : confirme H1")
    print(f"    Si trop loin : H1 falsified")

    # Save
    out = {
        'parameters': {'T_c_MeV': T_c, 'kappa_inf': KAPPA_INF},
        'sweep': results,
        'T_inflection_MeV': float(T_inflection),
        'delta_kappa_drop': float(drop_size),
        'verdict_prelim': 'TESTABLE — predicts Δκ~{:.2f} drop at T~{:.0f} MeV'.format(drop_size, T_inflection),
        'next_step': 'Mesurer S_EE(T) lattice QCD SU(3) NT∈{4,6,8,10,12} (cf Boyd 1996, HotQCD Bazavov 2017)',
        'falsifiable': 'Si κ_EE(T) lisse / pas de drop à T_c, H1 fausse'
    }
    with open('/tmp/H1_thermal_kappa_T_toy_2026-05-26.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\n→ Saved /tmp/H1_thermal_kappa_T_toy_2026-05-26.json")
    print(f"\nH1 verdict prelim : {out['verdict_prelim']}")
    print(f"Falsifiable test : {out['falsifiable']}")


if __name__ == '__main__':
    main()
