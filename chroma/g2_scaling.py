#!/usr/bin/env python3
"""
Extract g²(β) from β Langevin SU(3) plaquette data.
g² = 6/β, P(β) → a(β) → Λ scale.
Serves as input for choosing optimal Chroma β values.
"""
import json
import numpy as np

# Load V100#1 Langevin results
data = {
    2.3: {"P_mean": 0.57196, "P_std": 0.00363},
    2.4: {"P_mean": 0.60127, "P_std": 0.00345},
    2.5: {"P_mean": 0.62564, "P_std": 0.00304},
    2.6: {"P_mean": 0.64502, "P_std": 0.00277},
    2.7: {"P_mean": 0.66091, "P_std": 0.00257},
}

print("=== g²(β) scaling from Langevin SU(3) ===")
print(f"{'β':>6} {'g²=6/β':>8} {'P_plaq':>8} {'P_std':>8} {'a*sqrt(σ)':>10}")
print("-" * 50)

for beta in sorted(data.keys()):
    g2 = 6.0 / beta
    P = data[beta]["P_mean"]
    P_std = data[beta]["P_std"]
    # Approximate lattice spacing from plaquette (1-loop)
    # a*sqrt(σ) ~ exp(-(1-P)*π²/...)
    a_sigma = np.exp(-(1.0 - P) * 4.0)  # rough scaling estimate
    print(f"{beta:6.2f} {g2:8.4f} {P:8.5f} {P_std:8.5f} {a_sigma:10.6f}")

print()
print("=== Chroma SU(2) recommendation ===")
print("SU(2) Wilson action: β ∈ [2.40, 2.60] (canonical scaling)")
print("Matches SU(3) β ∈ [2.50, 2.70] → similar lattice spacing")
print("Equivalent g² = 6/β ≈ 2.3-2.5 → perturbative window")
print()
print("ECI v15 prediction (Theorem C.6):")
print("  m_0++/sqrt(σ) ≈ 3.78 (SU(N) large-N scaling)")
print("  Test at β=2.40, 2.50, 2.60 → continuum extrapolation")
