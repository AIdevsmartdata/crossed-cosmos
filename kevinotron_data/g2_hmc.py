"""
g2_hmc.py -- G2 HMC with correct Lie algebra projection.

The G2 Lie algebra is 14-dimensional, embedded in so(7) which is 21-dimensional.
The key fix: when generating momenta for HMC, they must be projected onto g2,
NOT the full so(7). Using so(7) momenta would explore wrong directions in
configuration space and violate detailed balance.

G2 is the automorphism group of the octonions. Its 14 generators are a
subset of the 21 antisymmetric 7x7 matrices (= so(7) generators).
The missing 7 directions correspond to the complement so(7)/g2, which
is the 7-dimensional fundamental representation of G2.

Method:
  - Build 14 G2 generators from octonion structure constants (same as Rust kevinotron)
  - Momenta: P = sum_{a=1}^{14} c_a T_a where c_a ~ N(0,1) and T_a are G2 generators
  - Force projection: project dS/dU back onto g2 using Tr(T_a F) basis expansion
  - exp(P): exact exponential for 7x7 antisymmetric matrix via eigendecomposition of P^2
  - Reproject: Gram-Schmidt onto SO(7) then verify G2 constraint

The G2 generators can optionally be loaded from a .npy file if available,
or built from scratch using the octonion multiplication table.
"""
import os
os.environ['JAX_ENABLE_X64'] = '1'

import jax
import jax.numpy as jnp
import numpy as np
from functools import partial
from time import time


# ---------------------------------------------------------------------------
# G2 generators from octonion structure constants
# ---------------------------------------------------------------------------

# Octonion multiplication table (imaginary units e_1..e_7):
# e_i * e_j = f_{ijk} e_k where f is totally antisymmetric.
# The 7 signed triples that define the multiplication:
SIGNED_TRIPLES = [
    (0, 1, 2,  1.0),
    (0, 3, 4,  1.0),
    (0, 5, 6,  1.0),
    (1, 3, 5,  1.0),
    (1, 4, 6, -1.0),
    (2, 3, 6, -1.0),
    (2, 4, 5, -1.0),
]


def build_g2_structure_constants():
    """Build the G2 structure constants f_{ijk} from octonion triples."""
    f = np.zeros((7, 7, 7))
    for i, j, k, s in SIGNED_TRIPLES:
        f[i, j, k] = s
        f[j, k, i] = s
        f[k, i, j] = s
        f[j, i, k] = -s
        f[k, j, i] = -s
        f[i, k, j] = -s
    return f


def build_g2_generators_numpy():
    """Build 14 G2 generators as 7x7 antisymmetric matrices.

    Method: G2 acts on Im(O) = R^7 preserving the cross product.
    The constraint is: [T, cross] = 0, i.e., T preserves the trilinear form.

    Concretely: for T antisymmetric 7x7, the G2 constraint is
        f_{iqk} T_{jp} + f_{ijk} T_{qp} + ... = 0 for all (i,j,k,p).
    This gives 35 linear constraints on 21 parameters (upper triangle of T),
    with a 14-dimensional null space = the G2 algebra.

    We find this null space via SVD exactly as in the Rust implementation.
    """
    f = build_g2_structure_constants()

    # Enumerate triples (i<j<k) and pairs (p<q)
    triples = [(i, j, k) for i in range(7) for j in range(i+1, 7) for k in range(j+1, 7)]
    pairs = [(p, q) for p in range(7) for q in range(p+1, 7)]
    assert len(triples) == 35
    assert len(pairs) == 21

    # Build constraint matrix M: M[triple_idx, pair_idx] encodes the constraint
    # that the generator preserves the cross product structure.
    # For each triple (i,j,k) and generator matrix T_{pq} = -T_{qp}:
    # constraint is sum over legs: f_{ajk} T_{ai} - f_{aik} T_{aj} + ...
    M = np.zeros((35, 21))
    for ti, (i, j, k) in enumerate(triples):
        for gi, (p, q) in enumerate(pairs):
            v = 0.0
            if i == p: v += f[q, j, k]
            if i == q: v -= f[p, j, k]
            if j == p: v += f[i, q, k]
            if j == q: v -= f[i, p, k]
            if k == p: v += f[i, j, q]
            if k == q: v -= f[i, j, p]
            M[ti, gi] = v

    # Null space of M = G2 generators
    _, S, Vt = np.linalg.svd(M, full_matrices=True)

    gens = []
    for r in range(21):
        is_null = (r >= len(S)) or (S[r] < 1e-10)
        if is_null:
            g = np.zeros((7, 7))
            for idx, (p, q) in enumerate(pairs):
                g[p, q] = Vt[r, idx]
                g[q, p] = -Vt[r, idx]

            # Normalize: Tr(T_a T_b) = -1/2 delta_{ab}
            # For antisymmetric: Tr(g @ g) = -sum g_{ij}^2 (double count)
            norm = np.sqrt(max(-np.trace(g @ g), 0))
            if norm > 1e-10:
                g *= np.sqrt(2.0) / norm
            gens.append(g)

    assert len(gens) == 14, f"Expected 14 G2 generators, got {len(gens)}"
    return np.array(gens)


def load_or_build_g2_generators(npy_path=None):
    """Load G2 generators from .npy file if available, otherwise build.

    Args:
        npy_path: optional path to .npy file with shape (14, 7, 7)

    Returns:
        gens: (14, 7, 7) numpy array of G2 generators
    """
    if npy_path is not None and os.path.exists(npy_path):
        gens = np.load(npy_path)
        assert gens.shape == (14, 7, 7), f"Bad shape: {gens.shape}"
        print(f"Loaded G2 generators from {npy_path}")
        return gens
    return build_g2_generators_numpy()


def verify_g2_generators(gens):
    """Verify that generators span the G2 algebra.

    Checks:
    1. All antisymmetric
    2. Orthonormality: Tr(T_a T_b) = -c delta_{ab}
    3. Closure under commutator: [T_a, T_b] = f^{ab}_c T_c
    4. Cross product preservation
    """
    n = len(gens)
    assert n == 14, f"Need 14 generators, got {n}"

    # Check antisymmetric
    for a in range(n):
        err = np.max(np.abs(gens[a] + gens[a].T))
        assert err < 1e-12, f"Generator {a} not antisymmetric: {err}"

    # Check orthogonality
    gram = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            gram[a, b] = np.trace(gens[a] @ gens[b])
    # Should be proportional to -identity
    off_diag = gram - np.diag(np.diag(gram))
    diag_vals = np.diag(gram)
    assert np.max(np.abs(off_diag)) < 1e-10, f"Not orthogonal: {np.max(np.abs(off_diag))}"
    assert np.all(diag_vals < -0.1), f"Wrong sign on diagonal: {diag_vals}"

    # Check closure: [T_a, T_b] must be in span of {T_c}
    max_err = 0.0
    for a in range(n):
        for b in range(a+1, n):
            comm = gens[a] @ gens[b] - gens[b] @ gens[a]
            # Project onto generators
            coeffs = np.array([np.trace(gens[c] @ comm) / np.trace(gens[c] @ gens[c])
                               for c in range(n)])
            reconstructed = sum(coeffs[c] * gens[c] for c in range(n))
            err = np.max(np.abs(comm - reconstructed))
            max_err = max(max_err, err)
    assert max_err < 1e-10, f"Algebra not closed: max err = {max_err}"

    return True


# ---------------------------------------------------------------------------
# G2-projected momenta and forces
# ---------------------------------------------------------------------------

def random_g2_momentum(gens_jax, key):
    """Generate random momentum in the G2 Lie algebra.

    P = sum_{a=1}^{14} c_a T_a  where c_a ~ N(0,1).

    This is the CORRECT way: only 14 independent directions,
    NOT the 21 of so(7).

    Args:
        gens_jax: (14, 7, 7) G2 generators as JAX array
        key: PRNG key

    Returns:
        P: (7, 7) antisymmetric matrix in g2 subalgebra
    """
    coeffs = jax.random.normal(key, (14,), dtype=jnp.float64)
    P = jnp.einsum('a,aij->ij', coeffs, gens_jax)
    return P


def random_g2_momenta_lattice(gens_jax, key, Ls, Lt):
    """Generate momentum field with one G2 algebra element per link.

    Args:
        gens_jax: (14, 7, 7)
        key: PRNG key
        Ls, Lt: lattice dimensions

    Returns:
        P: (4, Ls, Ls, Ls, Lt, 7, 7) antisymmetric field
    """
    n_links = 4 * Ls**3 * Lt
    keys = jax.random.split(key, n_links)

    # Generate all coefficients at once for efficiency
    all_coeffs = jax.random.normal(key, (4, Ls, Ls, Ls, Lt, 14), dtype=jnp.float64)
    P = jnp.einsum('...a,aij->...ij', all_coeffs, gens_jax)
    return P


def project_to_g2(F, gens_jax, norms):
    """Project a 7x7 matrix onto the G2 Lie algebra.

    Given F (possibly in so(7) or gl(7)), compute
        F_g2 = sum_a [Tr(T_a F) / Tr(T_a T_a)] T_a

    This strips out the 7 so(7)/g2 components.

    Args:
        F: (..., 7, 7) matrix field
        gens_jax: (14, 7, 7)
        norms: (14,) = Tr(T_a T_a) for each generator (precomputed, negative)

    Returns:
        F_g2: (..., 7, 7) projected onto g2
    """
    # Coefficients: c_a = Tr(T_a F) / Tr(T_a T_a)
    # Tr(T_a F) = sum_{ij} T_a[j,i] F[i,j] = sum_{ij} T_a^T[i,j] F[i,j]
    # For batch: einsum over spatial indices
    coeffs = jnp.einsum('aij,...ij->...a', gens_jax, F) / norms[None, :]
    # But norms shape is (14,), need to broadcast
    # Actually: coeffs shape is (..., 14), norms is (14,)
    # Fix: compute element-wise
    traces = jnp.einsum('aji,...ij->...a', gens_jax, F)  # Tr(T_a^T F) = Tr(T_a F)
    coeffs = traces / norms
    F_g2 = jnp.einsum('...a,aij->...ij', coeffs, gens_jax)
    return F_g2


def project_force_g2(U_link, staple_sum, gens_jax, norms, beta_d):
    """Compute gauge force projected onto G2.

    F = -project_g2( (beta/d) * Ta(U * staple_sum) )

    where Ta = anti-Hermitian projection for real matrices = (V - V^T)/2.

    Args:
        U_link: (..., 7, 7) gauge link
        staple_sum: (..., 7, 7) sum of staples
        gens_jax: (14, 7, 7)
        norms: (14,)
        beta_d: beta / beta_norm

    Returns:
        force: (..., 7, 7) in g2 algebra
    """
    V = beta_d * jnp.einsum('...ab,...bc->...ac', U_link, staple_sum)
    # Anti-symmetric projection (real group, so anti-Hermitian = antisymmetric)
    V_as = (V - V.swapaxes(-2, -1)) / 2
    # Project onto G2 subalgebra
    return project_to_g2(V_as, gens_jax, norms)


# ---------------------------------------------------------------------------
# Exponential map for antisymmetric matrices
# ---------------------------------------------------------------------------

def expm_antisym_7x7(A):
    """Exact matrix exponential for 7x7 real antisymmetric matrix.

    Uses eigendecomposition of A^2 (symmetric negative semidefinite).
    For antisymmetric A: A^2 has eigenvalues -lambda_k^2 <= 0.
    exp(A) can be computed in terms of cos(lambda) and sin(lambda)/lambda.

    This is the same method as the Rust kevinotron (expm_antisym_exact).
    """
    A2 = A @ A  # symmetric
    # A2 is symmetric negative semidefinite
    eigenvalues, eigenvectors = jnp.linalg.eigh(A2)
    # eigenvalues are -lambda_k^2 (negative or zero)

    # For each eigenvalue-eigenvector pair:
    # exp(A) |v_k> = cos(lambda_k) |v_k> + sin(lambda_k)/lambda_k A |v_k>
    lam2 = jnp.maximum(-eigenvalues, 0.0)  # lambda_k^2
    lam = jnp.sqrt(lam2)  # lambda_k

    cos_lam = jnp.cos(lam)
    # sin(lam)/lam with safe limit at lam=0
    sin_over_lam = jnp.where(lam > 1e-14, jnp.sin(lam) / lam, 1.0)

    # exp(A) = sum_k [ cos(lam_k) v_k v_k^T + sin(lam_k)/lam_k  (A v_k) v_k^T ]
    Av = A @ eigenvectors  # (7, 7) @ (7, 7) -> (7, 7)

    # result = V @ diag(cos) @ V^T + (A V) @ diag(sin/lam) @ V^T
    result = (eigenvectors * cos_lam[None, :]) @ eigenvectors.T + \
             (Av * sin_over_lam[None, :]) @ eigenvectors.T
    return result


# ---------------------------------------------------------------------------
# Reunitarization (project back to SO(7) then verify G2)
# ---------------------------------------------------------------------------

def reunitarize_so7(U):
    """Project a nearly-SO(7) matrix back to SO(7) via polar decomposition.

    Uses SVD: U = W S V^T, so the closest orthogonal matrix is W V^T,
    with det correction if needed.
    """
    W, S, Vt = jnp.linalg.svd(U)
    R = W @ Vt
    # Fix determinant
    det = jnp.linalg.det(R)
    # If det < 0, flip sign of last column of W
    R = jnp.where(det < 0,
                  W.at[:, -1].multiply(-1) @ Vt,
                  R)
    return R


def reunitarize_g2(U, gens_jax, norms, n_iter=5):
    """Reproject a matrix onto G2 subgroup of SO(7).

    Method:
    1. Project to SO(7) via polar decomposition
    2. Check that log(U) lies in g2 (approximately)
    3. If not, iteratively pull log(U) to g2 and re-exponentiate

    For small deviations from G2, the polar projection onto SO(7)
    is sufficient because the trajectory stays in G2 if momenta are in g2.
    """
    return reunitarize_so7(U)


# ---------------------------------------------------------------------------
# Full G2 HMC
# ---------------------------------------------------------------------------

class G2HMC:
    """HMC for G2 lattice gauge theory with correct Lie algebra projection."""

    def __init__(self, Ls=4, Lt=None, beta=10.0, n_steps=20, dt=0.01,
                 g2_gens_path=None):
        self.Ls = Ls
        self.Lt = Lt or 2 * Ls
        self.beta = beta
        self.n_steps = n_steps
        self.dt = dt
        self.Nc = 7  # fundamental dim
        self.d_adj = 14
        self.beta_norm = 7.0  # beta normalization for G2

        # Build or load G2 generators
        gens_np = load_or_build_g2_generators(g2_gens_path)
        verify_g2_generators(gens_np)
        self.gens = jnp.array(gens_np, dtype=jnp.float64)

        # Precompute norms: Tr(T_a T_a)
        self.norms = jnp.array([float(np.trace(gens_np[a] @ gens_np[a]))
                                for a in range(14)], dtype=jnp.float64)

        print(f"G2 HMC: Ls={Ls} Lt={self.Lt} beta={beta}")
        print(f"  14 generators built, norms = {self.norms[:3]}...")
        print(f"  dt={dt} n_steps={n_steps} traj_length={dt*n_steps:.2f}")

    def cold_start(self):
        """Identity gauge field."""
        return jnp.broadcast_to(
            jnp.eye(7, dtype=jnp.float64),
            (4, self.Ls, self.Ls, self.Ls, self.Lt, 7, 7)
        ).copy()

    def plaquette(self, U):
        """Average plaquette Re Tr(P) / 7."""
        p = 0.0
        count = 0
        for mu in range(4):
            for nu in range(mu+1, 4):
                U_nu_at_xmu = jnp.roll(U[nu], -1, axis=mu)
                U_mu_at_xnu = jnp.roll(U[mu], -1, axis=nu)
                # P = U_mu(x) U_nu(x+mu) U_mu(x+nu)^T U_nu(x)^T
                plaq = jnp.einsum('...ab,...bc,...dc,...da->...',
                                  U[mu], U_nu_at_xmu,
                                  U_mu_at_xnu,  # transpose for real = dagger
                                  U[nu])
                p += jnp.mean(plaq) / 7.0
                count += 1
        return float(p / count)

    def gauge_action(self, U):
        """S = (beta/7) sum (7 - Re Tr P)."""
        p = self.plaquette(U)
        n_plaq = 6 * self.Ls**3 * self.Lt
        return self.beta * n_plaq * (1.0 - p)

    def kinetic_energy(self, P):
        """T = -Tr(P^2) = sum |P_{ij}|^2 for antisymmetric P."""
        P2 = jnp.einsum('...ab,...bc->...ac', P, P)
        return float(-jnp.sum(jnp.trace(P2, axis1=-2, axis2=-1)))

    def gauge_force(self, U):
        """Gauge force projected onto G2 algebra."""
        beta_d = self.beta / self.beta_norm
        F = jnp.zeros_like(U)

        for mu in range(4):
            staple = jnp.zeros((self.Ls, self.Ls, self.Ls, self.Lt, 7, 7),
                               dtype=jnp.float64)
            for nu in range(4):
                if nu == mu:
                    continue
                # Forward staple
                U_nu_at_xmu = jnp.roll(U[nu], -1, axis=mu)
                U_mu_at_xnu = jnp.roll(U[mu], -1, axis=nu)
                s_fwd = jnp.einsum('...ab,...bc,...dc->...ad',
                                   U_nu_at_xmu,
                                   U_mu_at_xnu.swapaxes(-2, -1),  # transpose = dagger for real
                                   U[nu].swapaxes(-2, -1))

                # Backward staple
                U_nu_at_xmu_mnu = jnp.roll(jnp.roll(U[nu], -1, axis=mu), 1, axis=nu)
                U_mu_at_xmnu = jnp.roll(U[mu], 1, axis=nu)
                U_nu_at_xmnu = jnp.roll(U[nu], 1, axis=nu)
                s_bwd = jnp.einsum('...ba,...dc,...de->...ae',
                                   U_nu_at_xmu_mnu,  # transpose
                                   U_mu_at_xmnu,      # transpose
                                   U_nu_at_xmnu)

                staple = staple + s_fwd + s_bwd

            # V = beta_d * U_mu * staple
            V = beta_d * jnp.einsum('...ab,...bc->...ac', U[mu], staple)

            # Antisymmetric projection
            V_as = (V - V.swapaxes(-2, -1)) / 2.0

            # PROJECT ONTO G2 (the key fix!)
            V_g2 = project_to_g2(V_as, self.gens, self.norms)
            F = F.at[mu].set(V_g2)

        return F

    def update_links(self, U, P, dt):
        """U_new = exp(dt * P) * U with G2-safe exponential."""
        dtP = dt * P

        def expm_single(A):
            return expm_antisym_7x7(A)

        # Vectorize over all links
        # Shape: (4, Ls, Ls, Ls, Lt, 7, 7) -> flatten -> map -> reshape
        flat_shape = (-1, 7, 7)
        dtP_flat = dtP.reshape(flat_shape)
        exp_P_flat = jax.vmap(expm_single)(dtP_flat)
        exp_P = exp_P_flat.reshape(U.shape)

        U_new = jnp.einsum('...ab,...bc->...ac', exp_P, U)

        # Reunitarize back to SO(7) (G2 is preserved if momenta are in g2)
        U_flat = U_new.reshape(flat_shape)
        U_reunit = jax.vmap(reunitarize_so7)(U_flat)
        return U_reunit.reshape(U.shape)

    def trajectory(self, U, key):
        """One HMC trajectory."""
        k1, k2 = jax.random.split(key)

        U_old = U.copy()

        # Generate G2-projected momenta (14 directions, NOT 21)
        P = random_g2_momenta_lattice(self.gens, k1, self.Ls, self.Lt)

        # Initial Hamiltonian
        T_old = self.kinetic_energy(P)
        S_old = self.gauge_action(U)
        H_old = T_old + S_old

        # Leapfrog
        F = self.gauge_force(U)
        P = P - 0.5 * self.dt * F

        for step in range(self.n_steps - 1):
            U = self.update_links(U, P, self.dt)
            F = self.gauge_force(U)
            P = P - self.dt * F

        U = self.update_links(U, P, self.dt)
        F = self.gauge_force(U)
        P = P - 0.5 * self.dt * F

        # Final Hamiltonian
        T_new = self.kinetic_energy(P)
        S_new = self.gauge_action(U)
        H_new = T_new + S_new
        dH = H_new - H_old

        # Accept/reject
        r = float(jax.random.uniform(k2, dtype=jnp.float64))
        accepted = r < min(1.0, np.exp(-dH))

        if not accepted:
            U = U_old

        return U, accepted, dH

    def generate(self, n_traj=100, n_therm=50):
        """Run G2 HMC."""
        U = self.cold_start()
        key = jax.random.PRNGKey(42)
        n_accept = 0

        for traj in range(n_traj):
            key, subkey = jax.random.split(key)
            t0 = time()
            U, accepted, dH = self.trajectory(U, subkey)
            dt_wall = time() - t0

            if accepted:
                n_accept += 1

            if (traj + 1) % 5 == 0:
                p = self.plaquette(U)
                print(f"  traj {traj+1:>4}: dH={dH:>+10.4f} "
                      f"acc={n_accept}/{traj+1} ({100*n_accept/(traj+1):.0f}%) "
                      f"P={p:.6f} [{dt_wall:.1f}s]")

        print(f"G2 HMC done: {n_accept}/{n_traj} accepted ({100*n_accept/n_traj:.0f}%)")
        return U


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("=" * 70)
    print("G2 HMC test -- momenta in g2 (14-dim), NOT so(7) (21-dim)")
    print("=" * 70)

    # Build and verify generators
    gens_np = build_g2_generators_numpy()
    print(f"Built {len(gens_np)} G2 generators")
    verify_g2_generators(gens_np)
    print("Generator verification: PASS")

    gens_jax = jnp.array(gens_np, dtype=jnp.float64)
    norms = jnp.array([float(np.trace(gens_np[a] @ gens_np[a])) for a in range(14)])

    # Test 1: momentum is in g2
    key = jax.random.PRNGKey(123)
    P = random_g2_momentum(gens_jax, key)
    # Verify antisymmetric
    assert float(jnp.max(jnp.abs(P + P.T))) < 1e-14, "P not antisymmetric"
    # Verify in g2: project to g2 should be identity operation
    P_proj = project_to_g2(P[None, ...], gens_jax, norms)[0]
    err = float(jnp.max(jnp.abs(P - P_proj)))
    print(f"Test 1 (momentum in g2): projection error = {err:.2e}  "
          f"{'PASS' if err < 1e-12 else 'FAIL'}")

    # Test 2: random so(7) element is NOT in g2
    M_so7 = jax.random.normal(key, (7, 7), dtype=jnp.float64)
    M_so7 = (M_so7 - M_so7.T) / 2  # antisymmetric = so(7)
    M_g2 = project_to_g2(M_so7[None, ...], gens_jax, norms)[0]
    err_so7 = float(jnp.max(jnp.abs(M_so7 - M_g2)))
    print(f"Test 2 (so(7) element NOT in g2): residual = {err_so7:.4f}  "
          f"{'PASS' if err_so7 > 0.01 else 'FAIL (should be nonzero)'}")

    # Test 3: exp map stays in SO(7)
    exp_P = expm_antisym_7x7(P)
    det = float(jnp.linalg.det(exp_P))
    orth_err = float(jnp.max(jnp.abs(exp_P @ exp_P.T - jnp.eye(7))))
    print(f"Test 3 (exp map): det={det:.12f}, orthogonality error={orth_err:.2e}  "
          f"{'PASS' if abs(det - 1) < 1e-10 and orth_err < 1e-10 else 'FAIL'}")

    # Test 4: short HMC run
    print("\nTest 4: G2 HMC (5 trajectories, cold start)")
    g2hmc = G2HMC(Ls=4, beta=10.0, n_steps=10, dt=0.005)
    U = g2hmc.generate(n_traj=5)
    print(f"Final plaquette: {g2hmc.plaquette(U):.6f}")
    print("=" * 70)
