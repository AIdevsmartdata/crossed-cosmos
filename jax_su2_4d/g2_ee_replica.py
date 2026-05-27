#!/usr/bin/env python3
"""
G_2 Entanglement Entropy via Replica Trick (BP2008b method).

Measures the Renyi-2 entanglement entropy S_2 for G_2 lattice gauge theory
using the α-integration method of Buividovich-Polikarpov (arXiv:0802.4247).

Method:
  S_2 = -log(Tr(ρ_A²))
  where ρ_A is the reduced density matrix on region A.

  Using replica trick with deformed connectivity:
  S_2 = -log(Z(α=1)/Z(α=0))
      = -∫₀¹ dα ∂/∂α log Z(α)
      = -∫₀¹ dα ⟨∂S/∂α⟩_α

  α parametrizes the interpolation between normal (α=0) and
  swapped (α=1) boundary conditions on ∂A.

The entangling region A is taken as the half-lattice x₁ < L/2.
The boundary ∂A has area (L/2)^(D-1) in D=4 dimensions (actually L^2 × T
for our L³×2L geometry... but we use L⁴ symmetric for simplicity first).

Expected result:
  S_2 = κ_EE × Area(∂A)  + sub-leading

where κ_EE(G_2) is the quantity we want to measure. Predictions:
  - Formula 1: (1-1/N²)·ζ(3)/√π with N=rank+1=3 → κ = 0.603
  - Formula 2: (1-1/dim)·ζ(3)/√π with dim=14    → κ = 0.630
  - Formula 3: 0.518·√(rank) - 0.458 with rank=2  → κ = 0.275
  - Formula 4: κ_FP = 1/(2|Φ⁺|) = 1/12           → κ = 0.083

Author: Kévin Rémondière (ORCID 0009-0008-2443-7166)
"""
import numpy as np
from scipy.linalg import expm
import time
import argparse
from g2_metropolis_lattice import G2Lattice


class G2LatticeEE(G2Lattice):
    """Extended G_2 lattice with replica trick for entanglement entropy."""

    def __init__(self, L, D=4, beta=10.0, T_factor=2):
        """Initialize with L^(D-1) × T geometry where T = T_factor * L."""
        self.T_factor = T_factor
        self.T = T_factor * L
        super().__init__(L, D, beta)
        # Override shape: L^3 × T for D=4
        self.shape = tuple([L] * (D-1) + [self.T])
        self.links = np.zeros(self.shape + (D, 7, 7))
        for idx in np.ndindex(self.shape):
            for mu in range(D):
                self.links[idx + (mu,)] = np.eye(7)

    def is_boundary_link(self, site, mu):
        """Check if link (site, mu) crosses the entangling surface.
        Entangling surface: x_0 = L//2 (half-lattice cut in direction 0).
        A boundary link is one in direction mu=0 that starts at x_0 = L//2 - 1."""
        return mu == 0 and site[0] == self.L // 2 - 1

    def deformed_action(self, site, mu, U, alpha):
        """Action with α-deformation on boundary links.
        For α=0: normal action. For α=1: swapped replicas.
        Interpolation: on boundary links, multiply staple contribution by (1-α)."""
        K = self.staple_sum(site, mu)
        base = -(self.beta / 7.0) * np.trace(U @ K)

        if self.is_boundary_link(site, mu):
            # Deform: reduce coupling at boundary by factor (1-α)
            return (1 - alpha) * base
        return base

    def metropolis_update_alpha(self, site, mu, alpha, epsilon=0.15):
        """Metropolis update with α-deformed action."""
        U_old = self.get_link(site, mu)
        S_old = self.deformed_action(site, mu, U_old, alpha)

        R = self._random_g2_near_identity(epsilon)
        U_new = R @ U_old

        S_new = self.deformed_action(site, mu, U_new, alpha)
        dS = S_new - S_old

        if dS < 0 or np.random.random() < np.exp(-dS):
            self.set_link(site, mu, U_new)
            return True
        return False

    def _random_g2_near_identity(self, epsilon):
        """Random G_2 element near identity."""
        coeffs = np.random.normal(0, epsilon, size=len(self.generators))
        X = sum(c * T for c, T in zip(coeffs, self.generators))
        return expm(X)

    def sweep_alpha(self, alpha, epsilon=0.15):
        """Full sweep with α-deformed action."""
        acc = 0
        total = 0
        for idx in np.ndindex(self.shape):
            for mu in range(self.D):
                if self.metropolis_update_alpha(idx, mu, alpha, epsilon):
                    acc += 1
                total += 1
        return acc / total

    def measure_dS_dalpha(self, alpha):
        """Measure ⟨∂S/∂α⟩_α = derivative of action w.r.t. α.
        For our deformation: ∂S/∂α = +base_action on boundary links."""
        dS = 0.0
        for idx in np.ndindex(self.shape):
            for mu in range(self.D):
                if self.is_boundary_link(idx, mu):
                    U = self.get_link(idx, mu)
                    K = self.staple_sum(idx, mu)
                    base = -(self.beta / 7.0) * np.trace(U @ K)
                    dS += base  # ∂/∂α [(1-α)·base] = -base
        return -dS  # note the minus from derivative of (1-α)

    def measure_boundary_plaquettes(self):
        """Average plaquette on boundary links only."""
        P_sum = 0.0
        count = 0
        for idx in np.ndindex(self.shape):
            if idx[0] == self.L // 2 - 1:
                for nu in range(1, self.D):
                    x_mu = self.shift(idx, 0)
                    x_nu = self.shift(idx, nu)
                    U1 = self.get_link(idx, 0)
                    U2 = self.get_link(x_mu, nu)
                    U3 = self.get_link(x_nu, 0)
                    U4 = self.get_link(idx, nu)
                    plaq = U1 @ U2 @ U3.T @ U4.T
                    P_sum += np.trace(plaq) / 7.0
                    count += 1
        return P_sum / count if count > 0 else 0.0


def run_alpha_integration(L, beta, n_alpha=11, n_therm=300, n_meas=100,
                          n_skip=5, epsilon=0.15, T_factor=2):
    """Run the full α-integration for S_2.

    S_2 = ∫₀¹ dα ⟨∂S/∂α⟩_α

    using trapezoidal rule over n_alpha points.
    """
    alphas = np.linspace(0, 1, n_alpha)
    dS_values = np.zeros(n_alpha)
    dS_errors = np.zeros(n_alpha)

    print(f"{'='*60}")
    print(f"G_2 EE Replica — L={L}, β={beta}, T={T_factor*L}")
    print(f"  α points: {n_alpha}")
    print(f"  Therm: {n_therm}, Meas: {n_meas} (skip {n_skip})")
    print(f"{'='*60}")

    for i, alpha in enumerate(alphas):
        print(f"\n--- α = {alpha:.2f} ({i+1}/{n_alpha}) ---")

        lat = G2LatticeEE(L, D=4, beta=beta, T_factor=T_factor)

        # Thermalization
        for s in range(n_therm):
            lat.sweep_alpha(alpha, epsilon)
            if (s+1) % 100 == 0:
                P = lat.plaquette()
                print(f"  therm {s+1}: ⟨P⟩ = {P:.4f}")

        # Measurement
        measurements = []
        for m in range(n_meas):
            for _ in range(n_skip):
                lat.sweep_alpha(alpha, epsilon)
            val = lat.measure_dS_dalpha(alpha)
            measurements.append(val)

        arr = np.array(measurements)
        dS_values[i] = arr.mean()
        dS_errors[i] = arr.std() / np.sqrt(len(arr))
        print(f"  ⟨∂S/∂α⟩ = {dS_values[i]:.6f} ± {dS_errors[i]:.6f}")

    # Trapezoidal integration
    S2 = np.trapz(dS_values, alphas)
    # Error propagation (approximate)
    dalpha = alphas[1] - alphas[0]
    S2_err = dalpha * np.sqrt(np.sum(dS_errors**2))

    # Boundary area: cut at x_0 = L//2
    # In D=4 with L^3 × T: area = L^2 × T (3 transverse directions)
    # But our cut is in direction 0, so boundary = L^(D-2) × T = L^2 × T
    T = T_factor * L
    area = L**(3-1) * T  # L² × T for D=4

    # Actually for the LINK-based boundary:
    # Number of boundary links = L^(D-1) = L^3 (at fixed x_0, all directions except 0)
    # But the AREA of ∂A in lattice units is L^(D-2) for spatial cut
    # For D=4 symmetric L^4: area(∂A) = L^2 (2D area of the 3D cut surface)
    # More precisely: for L^3 × T, cut at x_0=L/2:
    # ∂A has L^(D-2) × T/a... this needs care.

    # Simplest: κ_EE = S_2 / (number of boundary plaquettes)
    n_boundary_plaq = L**(2) * T * 3  # 3 orientations containing μ=0

    print(f"\n{'='*60}")
    print(f"RESULTS: G_2 EE Replica")
    print(f"{'='*60}")
    print(f"  S_2          = {S2:.6f} ± {S2_err:.6f}")
    print(f"  Area(∂A)     = {area} (lattice units)")
    print(f"  S_2/Area     = {S2/area:.6f} ± {S2_err/area:.6f}")
    print(f"  n_bdy_plaq   = {n_boundary_plaq}")
    print(f"  S_2/n_plaq   = {S2/n_boundary_plaq:.6f}")

    print(f"\n  Predictions:")
    preds = [
        ("(1-1/N²)·ζ(3)/√π, N=3", 0.603),
        ("(1-1/dim)·ζ(3)/√π, dim=14", 0.630),
        ("0.518√rank-0.458, rank=2", 0.275),
        ("κ_FP = 1/12", 0.083),
    ]
    for name, val in preds:
        print(f"    {name:40s}: κ = {val:.3f}")

    # Save
    outfile = f"g2_ee_L{L}_beta{beta:.1f}.npz"
    np.savez(outfile,
             L=L, beta=beta, T=T,
             alphas=alphas, dS_values=dS_values, dS_errors=dS_errors,
             S2=S2, S2_err=S2_err, area=area)
    print(f"\n  Saved to {outfile}")

    return S2, S2_err, area


def main():
    parser = argparse.ArgumentParser(description='G_2 Entanglement Entropy')
    parser.add_argument('--L', type=int, default=4)
    parser.add_argument('--beta', type=float, default=10.0)
    parser.add_argument('--n_alpha', type=int, default=11)
    parser.add_argument('--n_therm', type=int, default=300)
    parser.add_argument('--n_meas', type=int, default=100)
    parser.add_argument('--n_skip', type=int, default=5)
    parser.add_argument('--epsilon', type=float, default=0.15)
    parser.add_argument('--T_factor', type=int, default=2)
    args = parser.parse_args()

    run_alpha_integration(
        args.L, args.beta, args.n_alpha, args.n_therm,
        args.n_meas, args.n_skip, args.epsilon, args.T_factor
    )


if __name__ == '__main__':
    main()
