#!/usr/bin/env python3
"""
G_2 Lattice Gauge Theory — Metropolis Monte Carlo.

G_2 = Aut(O) is the 14-dimensional exceptional Lie group, embedded in SO(7).
Lattice links are 7x7 real orthogonal matrices satisfying the G_2 constraint
(preserving the octonion cross product).

Implementation follows:
- Bruno-Caselle-Panero-Pellegrini (arXiv:1409.8305, JHEP 2015)
- Holland-Pepe-Wiese (hep-lat/0302023)

Key differences from SU(N):
- β = 7/g² (NOT 2N/g²)
- Fundamental rep is 7-dim REAL (not complex)
- Z(G_2) = {1} (trivial center)
- G_2/SU(3) ≅ S⁶

Algorithm: Metropolis with Lie algebra perturbations.

Author: Kévin Rémondière (ORCID 0009-0008-2443-7166)
"""
import numpy as np
from scipy.linalg import expm
import time
import argparse

# ============================================================
# G_2 Lie algebra generators in the 7-dim fundamental rep
# ============================================================

def g2_generators():
    """
    Return the 14 generators of g_2 ⊂ so(7) as 7x7 antisymmetric matrices.

    Construction via octonion structure constants.
    The 7 imaginary octonion units e_1,...,e_7 satisfy:
        e_i · e_j = f_{ijk} e_k - δ_{ij}
    where f_{ijk} is totally antisymmetric, nonzero for 7 triples
    (Fano plane / cyclic convention):
        (1,2,3), (1,4,5), (2,4,6), (3,4,7), (1,6,7), (2,5,7), (3,5,6)

    G_2 generators split into:
    - 7 generators L_a: (L_a)_{bc} = f_{abc} (left multiplication)
    - 7 generators R_a from the symmetric part (quadratic Casimir)

    Together they span the 14-dim g_2 subalgebra of so(7).
    """
    # G_2 associative 3-form (Bryant convention):
    # φ = e^{123} + e^{145} + e^{167} + e^{246} - e^{257} - e^{347} - e^{356}
    # Signed Fano triples (1-indexed, with orientation sign):
    signed_triples = [
        (1, 2, 3, +1), (1, 4, 5, +1), (1, 6, 7, +1), (2, 4, 6, +1),
        (2, 5, 7, -1), (3, 4, 7, -1), (3, 5, 6, -1)
    ]

    # Build structure constants f_{ijk} (0-indexed internally)
    f = np.zeros((7, 7, 7))
    for (i, j, k, sign) in signed_triples:
        i0, j0, k0 = i-1, j-1, k-1
        f[i0, j0, k0] = sign
        f[j0, k0, i0] = sign
        f[k0, i0, j0] = sign
        f[j0, i0, k0] = -sign
        f[k0, j0, i0] = -sign
        f[i0, k0, j0] = -sign

    # Find g_2 ⊂ so(7) via SVD null space of the 3-form preservation system.
    # The constraint (L_D φ)(i,j,k) = 0 for all triples gives a 35×21 linear
    # system whose 14-dim kernel is exactly g_2.
    from numpy.linalg import svd

    so7_pairs = [(p, q) for p in range(7) for q in range(p+1, 7)]
    triples = [(i, j, k) for i in range(7) for j in range(i+1, 7) for k in range(j+1, 7)]

    M = np.zeros((len(triples), len(so7_pairs)))
    for t_idx, (i, j, k) in enumerate(triples):
        for g_idx, (p, q) in enumerate(so7_pairs):
            val = 0.0
            if i == p: val += f[q, j, k]
            if i == q: val -= f[p, j, k]
            if j == p: val += f[i, q, k]
            if j == q: val -= f[i, p, k]
            if k == p: val += f[i, j, q]
            if k == q: val -= f[i, j, p]
            M[t_idx, g_idx] = val

    _, S, Vh = svd(M)
    null_dim = np.sum(S < 1e-10)
    assert null_dim == 14, f"Expected 14 g_2 generators, got {null_dim}"

    null_space = Vh[-null_dim:]
    g2_gens = []
    for v in null_space:
        G = np.zeros((7, 7))
        for idx, (p, q) in enumerate(so7_pairs):
            G[p, q] = v[idx]
            G[q, p] = -v[idx]
        g2_gens.append(G)

    # Normalize: Tr(T_a T_b) = -2 δ_{ab}
    normalized = []
    for T in g2_gens:
        norm = np.sqrt(-np.trace(T @ T))
        if norm > 1e-10:
            normalized.append(T / norm * np.sqrt(2))
        else:
            normalized.append(T)

    return normalized


# ============================================================
# G_2 group element operations
# ============================================================

def expm_antisym_7(A):
    """Fast exact matrix exponential for 7×7 antisymmetric matrices.
    Uses eigendecomposition: since A is real antisymmetric, iA is Hermitian,
    so eigh gives exact eigenvalues. ~50× faster than scipy.linalg.expm."""
    evals, U = np.linalg.eigh(1j * A)
    return np.real((U * np.exp(-1j * evals)) @ U.conj().T)


def random_g2_element(generators, epsilon=0.1):
    """Random G_2 element near identity via Lie algebra exponential."""
    coeffs = np.random.normal(0, epsilon, size=len(generators))
    X = sum(c * T for c, T in zip(coeffs, generators))
    return expm_antisym_7(X)


def random_g2_full(generators, n_steps=20):
    """Random G_2 element by composing many small steps (for initialization)."""
    U = np.eye(7)
    for _ in range(n_steps):
        U = U @ random_g2_element(generators, epsilon=0.5)
    return U


def project_g2(U, generators):
    """Project a 7x7 matrix onto G_2 by extracting g_2 components and re-exponentiating."""
    # First project to SO(7): U → (U - U^T)/2 then expm
    A = (U - U.T) / 2  # antisymmetric part of log
    # Project onto g_2 subalgebra
    coeffs = np.array([np.trace(A @ T.T) / np.trace(T @ T.T) for T in generators])
    A_g2 = sum(c * T for c, T in zip(coeffs, generators))
    return expm(A_g2)


# ============================================================
# Lattice setup
# ============================================================

class G2Lattice:
    def __init__(self, L, D=4, beta=10.0):
        self.L = L
        self.D = D
        self.beta = beta  # β = 7/g²
        self.shape = tuple([L] * D)
        self.generators = g2_generators()

        # Initialize links: identity (cold start)
        self.links = np.zeros(self.shape + (D, 7, 7))
        for idx in np.ndindex(self.shape):
            for mu in range(D):
                self.links[idx + (mu,)] = np.eye(7)

    def hot_start(self):
        """Initialize with random G_2 elements."""
        for idx in np.ndindex(self.shape):
            for mu in range(self.D):
                self.links[idx + (mu,)] = random_g2_full(self.generators)

    def get_link(self, site, mu):
        return self.links[site + (mu,)]

    def set_link(self, site, mu, U):
        self.links[site + (mu,)] = U

    def shift(self, site, mu, direction=1):
        """Shift site by ±1 in direction mu with periodic BC."""
        s = list(site)
        s[mu] = (s[mu] + direction) % self.L
        return tuple(s)

    def staple_sum(self, site, mu):
        """Compute the sum of staples around the link U_mu(site)."""
        S = np.zeros((7, 7))
        for nu in range(self.D):
            if nu == mu:
                continue
            # Forward staple: U_nu(x+mu) U_mu(x+nu)^T U_nu(x)^T
            x_mu = self.shift(site, mu)
            x_nu = self.shift(site, nu)
            U_nu_xmu = self.get_link(x_mu, nu)
            U_mu_xnu = self.get_link(x_nu, mu)
            U_nu_x = self.get_link(site, nu)
            S += U_nu_xmu @ U_mu_xnu.T @ U_nu_x.T

            # Backward staple: U_nu(x+mu-nu)^T U_mu(x-nu)^T U_nu(x-nu)
            x_mu_mnu = self.shift(x_mu, nu, -1)
            x_mnu = self.shift(site, nu, -1)
            U_nu_xmu_mnu = self.get_link(x_mu_mnu, nu)
            U_mu_xmnu = self.get_link(x_mnu, mu)
            U_nu_xmnu = self.get_link(x_mnu, nu)
            S += U_nu_xmu_mnu.T @ U_mu_xmnu.T @ U_nu_xmnu

        return S

    def local_action(self, site, mu, U=None):
        """Local contribution to Wilson action from link U_mu(site).
        S_local = -(β/7) Re Tr(U · K†) where K = staple sum."""
        if U is None:
            U = self.get_link(site, mu)
        K = self.staple_sum(site, mu)
        return -(self.beta / 7.0) * np.trace(U @ K)

    def metropolis_update(self, site, mu, epsilon=0.15):
        """Single-link Metropolis update."""
        U_old = self.get_link(site, mu)
        S_old = self.local_action(site, mu, U_old)

        # Propose: U_new = R · U_old where R is near-identity G_2
        R = random_g2_element(self.generators, epsilon)
        U_new = R @ U_old

        S_new = self.local_action(site, mu, U_new)
        dS = S_new - S_old

        if dS < 0 or np.random.random() < np.exp(-dS):
            self.set_link(site, mu, U_new)
            return True
        return False

    def sweep(self, epsilon=0.15):
        """One full sweep over all links."""
        accepted = 0
        total = 0
        for idx in np.ndindex(self.shape):
            for mu in range(self.D):
                if self.metropolis_update(idx, mu, epsilon):
                    accepted += 1
                total += 1
        return accepted / total

    def plaquette(self):
        """Average plaquette ⟨P⟩ = (1/7) ⟨Re Tr(U_plaq)⟩."""
        P_sum = 0.0
        count = 0
        for idx in np.ndindex(self.shape):
            for mu in range(self.D):
                for nu in range(mu+1, self.D):
                    x_mu = self.shift(idx, mu)
                    x_nu = self.shift(idx, nu)
                    U1 = self.get_link(idx, mu)
                    U2 = self.get_link(x_mu, nu)
                    U3 = self.get_link(x_nu, mu)
                    U4 = self.get_link(idx, nu)
                    plaq = U1 @ U2 @ U3.T @ U4.T
                    P_sum += np.trace(plaq) / 7.0
                    count += 1
        return P_sum / count

    def polyakov_loop(self, direction=0):
        """Average Polyakov loop in given direction."""
        P_sum = 0.0
        count = 0
        spatial_shape = list(self.shape)
        spatial_shape[direction] = 1

        for idx in np.ndindex(tuple(spatial_shape)):
            site = list(idx)
            U = np.eye(7)
            for t in range(self.L):
                site[direction] = t
                U = U @ self.get_link(tuple(site), direction)
            P_sum += np.abs(np.trace(U) / 7.0)
            count += 1
        return P_sum / count


# ============================================================
# Main simulation
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='G_2 Lattice Monte Carlo')
    parser.add_argument('--L', type=int, default=4, help='Lattice size')
    parser.add_argument('--beta', type=float, default=10.0, help='β = 7/g²')
    parser.add_argument('--n_therm', type=int, default=200, help='Thermalization sweeps')
    parser.add_argument('--n_meas', type=int, default=100, help='Measurement sweeps')
    parser.add_argument('--n_skip', type=int, default=5, help='Sweeps between measurements')
    parser.add_argument('--epsilon', type=float, default=0.15, help='Metropolis step size')
    parser.add_argument('--cold', action='store_true', help='Cold start (default)')
    parser.add_argument('--hot', action='store_true', help='Hot start')
    args = parser.parse_args()

    print("=" * 60)
    print(f"G_2 Lattice Monte Carlo — {args.L}^4, β = {args.beta}")
    print(f"  β = 7/g² → g² = {7.0/args.beta:.4f}")
    print(f"  Thermalization: {args.n_therm} sweeps")
    print(f"  Measurements: {args.n_meas} (skip {args.n_skip})")
    print(f"  Metropolis ε: {args.epsilon}")
    print("=" * 60)

    # Build generators
    print("Building G_2 generators (14 = dim g_2 ⊂ so(7))...")
    t0 = time.time()
    lat = G2Lattice(args.L, D=4, beta=args.beta)

    if args.hot:
        print("Hot start...")
        lat.hot_start()
    else:
        print("Cold start (identity links)...")

    print(f"Lattice initialized in {time.time()-t0:.1f}s")

    # Sanity: cold start plaquette should be 1.0
    P0 = lat.plaquette()
    print(f"Initial ⟨P⟩ = {P0:.6f} (cold: should be 1.0)")

    # Thermalization
    print(f"\nThermalization ({args.n_therm} sweeps)...")
    for i in range(args.n_therm):
        acc = lat.sweep(args.epsilon)
        if (i+1) % 20 == 0:
            P = lat.plaquette()
            print(f"  sweep {i+1:4d}: ⟨P⟩ = {P:.6f}, acc = {acc:.3f}")

    # Measurement
    print(f"\nMeasurement ({args.n_meas} × {args.n_skip} sweeps)...")
    plaq_values = []
    poly_values = []
    for i in range(args.n_meas):
        for _ in range(args.n_skip):
            lat.sweep(args.epsilon)
        P = lat.plaquette()
        L_poly = lat.polyakov_loop()
        plaq_values.append(P)
        poly_values.append(L_poly)
        if (i+1) % 10 == 0:
            print(f"  meas {i+1:4d}: ⟨P⟩ = {P:.6f}, |L| = {L_poly:.6f}")

    plaq_arr = np.array(plaq_values)
    poly_arr = np.array(poly_values)

    print(f"\n{'='*60}")
    print(f"RESULTS: G_2 L={args.L}^4, β={args.beta}")
    print(f"{'='*60}")
    print(f"  ⟨P⟩       = {plaq_arr.mean():.6f} ± {plaq_arr.std()/np.sqrt(len(plaq_arr)):.6f}")
    print(f"  |⟨L⟩|     = {poly_arr.mean():.6f} ± {poly_arr.std()/np.sqrt(len(poly_arr)):.6f}")

    # Expected values (Bruno+ 2015):
    # β=9.6: σa²=0.134 → weak coupling
    # β=10.0: σa²=0.047 → deeper in scaling
    # Strong coupling ⟨P⟩ ≈ β/(7·2D·7) for small β
    # Weak coupling ⟨P⟩ → 1 - const/β
    sc_pred = args.beta / (7 * 2 * 4 * 7)  # naive strong coupling
    print(f"\n  Strong-coupling prediction: ⟨P⟩_SC ≈ {sc_pred:.6f}")
    print(f"  (valid only for β << 9.45)")

    # Save results
    outfile = f"g2_L{args.L}_beta{args.beta:.1f}.npz"
    np.savez(outfile,
             L=args.L, beta=args.beta,
             plaquette=plaq_arr, polyakov=poly_arr,
             n_therm=args.n_therm, n_meas=args.n_meas)
    print(f"\n  Saved to {outfile}")


if __name__ == '__main__':
    main()
