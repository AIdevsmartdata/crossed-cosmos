#!/usr/bin/env python3
"""SU(3) HMC D=3 — JAX (adapted from su2_hmc_jax.py).

Mission (2026-05-24) : tester α(SU(3), D=3) = 3/4 prédite par le framework
géométrique κ(D) = 1/(2(D-1)) ⟹ α(D) = (2D-3)/(2(D-1)).

Pipeline :
  1) HMC SU(3) D=3 thermalization à β ∈ {β_i}
  2) Pour chaque config finale, calcul ⟨P⟩ (plaquette spacing a)
  3) Block-spin Migdal-Kadanoff 2→1 (déterministe, polar projection)
  4) Calcul ⟨P⟩_a/2 (plaquette spacing 2a sur lattice block-spinned)
  5) Δ⟨P⟩MK = ⟨P⟩_a - ⟨P⟩_a/2
  6) Fit α via -slope log Δ⟨P⟩MK vs log β

Conventions :
  - Wilson action : S_W(U) = β · Σ_p (1 - (1/N) Re tr U_p), N=3
  - Algebra su(3) : 8 générateurs Gell-Mann normalisés T_a = λ_a/2,
    tr(T_a T_b) = (1/2) δ_ab
  - HMC momenta : 8-vecteurs réels p_a, hamiltonien
    H = (1/2) Σ p_a² + S_W(U)
  - Leapfrog : pas symplectique avec proj retraction exp(i ε Σ_a F_a T_a)·U
  - Force F_a = -∂S/∂p_a calculée via auto-diff sur la paramétrisation
    U_new = exp(i Σ p_a T_a) U_old

Anti-fab :
  - SU(3) Haar : QR avec Mezzadri trick (det phase fix) — référence
    F. Mezzadri 2007 "How to generate random matrices from the classical
    compact groups", Notices AMS 54(5):592-604.
  - Gell-Mann normalisation : tr(T_a T_b) = δ_ab/2 (convention Yndurain
    1996 §2.3, standard QCD textbook).
  - Strong coupling β→0 limit : ⟨P⟩ → 1/N - 1/(N²) β + O(β²) ≈ 1/3 for β=0.
    Free limit β→∞ : ⟨P⟩ → 1 - 8/(βN²) à grands β.
"""
import os
# Force CPU (this script is light, CPU enough for L=4..8 D=3)
os.environ.setdefault("JAX_PLATFORMS", "cpu")

import jax
import jax.numpy as jnp
import numpy as np
import time
import json
import argparse


# ============================================================================
#  SU(3) constants : Gell-Mann generators, complex dtype
# ============================================================================

CDTYPE = jnp.complex64
RDTYPE = jnp.float32
N = 3
NDIM = 3      # D=3 spacetime
N_GEN = 8     # dim(su(3)) = 8

# Gell-Mann matrices λ_a (a=1..8). Conventions standard (Yndurain 1996,
# Particle Data Group). T_a = λ_a / 2.
_LAMBDA = np.zeros((8, 3, 3), dtype=np.complex64)
_LAMBDA[0] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
_LAMBDA[1] = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]])
_LAMBDA[2] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
_LAMBDA[3] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]])
_LAMBDA[4] = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]])
_LAMBDA[5] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
_LAMBDA[6] = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]])
_LAMBDA[7] = (1.0 / np.sqrt(3.0)) * np.array(
    [[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=np.complex64
)
# T_a = λ_a / 2 → tr(T_a T_b) = δ_ab / 2 (verified by hand on all pairs)
T_GEN = jnp.array(0.5 * _LAMBDA, dtype=CDTYPE)  # shape (8, 3, 3)


# ============================================================================
#  SU(3) matrix utilities
# ============================================================================

def random_su3(key, shape=()):
    """Haar-random SU(3) via QR with Mezzadri det-phase fix.

    Algorithm : Mezzadri 2007 (Notices AMS 54:592). Given Z = X + iY where X,Y
    are real N(0,1) Gaussian, QR(Z) = Q R with Q unitary. Multiply Q columns
    by (diag(R) / |diag(R)|) to get Q ~ Haar(U(N)). Divide by det(Q)^(1/N) to
    project to SU(N) (this is allowed because U(N) = SU(N) × U(1)/Z_N).
    """
    n_mat = int(np.prod(shape)) if shape else 1
    # Generate complex Gaussian (3,3)
    k1, k2 = jax.random.split(key)
    A_re = jax.random.normal(k1, (n_mat, 3, 3))
    A_im = jax.random.normal(k2, (n_mat, 3, 3))
    A = (A_re + 1j * A_im).astype(CDTYPE)
    Q, R = jnp.linalg.qr(A)
    # Mezzadri trick : multiply each column by diag(R)/|diag(R)|
    d = jnp.diagonal(R, axis1=-2, axis2=-1)  # (n_mat, 3)
    phase = d / jnp.maximum(jnp.abs(d), 1e-15)
    Q = Q * phase[:, None, :]   # broadcast phase on columns
    # Project U(3) → SU(3) : divide by det^(1/3)
    det = jnp.linalg.det(Q)
    det_phase = det / jnp.maximum(jnp.abs(det), 1e-15)
    # Take 1/3 root by extracting angle
    angle = jnp.angle(det_phase)
    cube_root_phase = jnp.exp(1j * angle / 3.0)
    Q_su3 = Q / cube_root_phase[:, None, None]
    if shape:
        return Q_su3.reshape(shape + (3, 3))
    else:
        return Q_su3[0]


@jax.jit
def sun_mul(A, B):
    return jnp.einsum('...ij,...jk->...ik', A, B)


@jax.jit
def sun_dagger(U):
    return jnp.conj(jnp.swapaxes(U, -1, -2))


@jax.jit
def project_sun(U):
    """Project a near-SU(3) matrix back to SU(3) via SVD polar + det-phase fix.

    Use SVD : U = V Σ W†, then proj = V W† is unitary.
    Then divide by det(proj)^(1/3) for SU(3).
    """
    Vmat, _, WH = jnp.linalg.svd(U)
    proj = sun_mul(Vmat, WH)
    det = jnp.linalg.det(proj)
    det_phase = det / jnp.maximum(jnp.abs(det), 1e-15)
    angle = jnp.angle(det_phase)
    cube_root_phase = jnp.exp(1j * angle / 3.0)
    return proj / cube_root_phase[..., None, None]


@jax.jit
def antiherm_from_vec(p):
    """Build anti-hermitian su(3) matrix from 8-vector.

    Returns X = i Σ_a p_a T_a, which is anti-hermitian and traceless.
    Shape : p (..., 8) → X (..., 3, 3) complex.
    """
    # X = 1j * (p . T)  where T is (8,3,3)
    X = 1j * jnp.einsum('...a,aij->...ij', p.astype(CDTYPE), T_GEN)
    return X


@jax.jit
def matrix_exp_taylor(X, n_terms=15):
    """exp(X) via truncated Taylor series with fixed scaling (X assumed small).

    For our HMC use case, the typical ||ε X||_F is bounded by ε * |p|_2 ~
    0.1 * sqrt(8) ~ 0.3. With n_terms=15, the Taylor remainder is
    O(0.3^16/16!) ~ 10^{-22}, well below complex64 precision. The fixed
    scaling avoids JIT-time conditional control flow.

    For safety we apply ONE scaling-and-squaring step (scale X → X/2, square
    once) which adds margin if ||X|| > 1.
    """
    Xs = X / 2.0  # safety scale
    I = jnp.eye(3, dtype=CDTYPE)
    result = jnp.zeros_like(Xs) + I
    term = jnp.zeros_like(Xs) + I
    for k in range(1, n_terms + 1):
        term = sun_mul(term, Xs) / k
        result = result + term
    # Square once (since we divided by 2)
    return sun_mul(result, result)


@jax.jit
def expmap_su3(p):
    """exp(i Σ p_a T_a) — group exponential map for su(3) element from 8-vector."""
    X = antiherm_from_vec(p)
    return matrix_exp_taylor(X)


# ============================================================================
#  Lattice (3D periodic) — neighbour table and link layout
# ============================================================================

def build_neighbors_3D(L):
    """Build neighbour index for 3D periodic lattice.

    Returns nbr : (3, 2, V) where nbr[mu, 0, site] = site + ê_μ,
                                  nbr[mu, 1, site] = site - ê_μ.
    """
    V = L ** 3
    nbr = np.zeros((3, 2, V), dtype=np.int32)
    coords = np.stack(np.unravel_index(np.arange(V), (L,) * 3), axis=1)
    for mu in range(3):
        for direc, sign in [(0, 1), (1, -1)]:
            shifted = coords.copy()
            shifted[:, mu] = (shifted[:, mu] + sign) % L
            nbr[mu, direc] = np.ravel_multi_index(
                tuple(shifted[:, k] for k in range(3)), (L,) * 3
            )
    return jnp.array(nbr)


# ============================================================================
#  Wilson action and observables (3D, SU(3))
# ============================================================================

def make_compute_action(L, beta, nbr):
    """S_W(U) = β Σ_p (1 - (1/N) Re tr U_p), 3 pairs (mu<nu) in D=3.

    Note: returns a real scalar; uses jnp.real after trace.
    """
    V = L ** 3

    @jax.jit
    def S(U):
        # U shape (3*V, 3, 3)
        total = jnp.zeros((), dtype=RDTYPE)
        sites = jnp.arange(V)
        for mu in range(3):
            for nu in range(mu + 1, 3):
                x_mu = nbr[mu, 0, sites]   # site + ê_μ
                x_nu = nbr[nu, 0, sites]   # site + ê_ν
                P = sun_mul(U[mu * V + sites], U[nu * V + x_mu])
                P = sun_mul(P, sun_dagger(U[mu * V + x_nu]))
                P = sun_mul(P, sun_dagger(U[nu * V + sites]))
                trP = (P[..., 0, 0] + P[..., 1, 1] + P[..., 2, 2]).real
                total = total + jnp.sum(1.0 - trP / 3.0)
        return beta * total

    return S


def make_compute_plaquette_avg(L, nbr):
    V = L ** 3

    @jax.jit
    def plaq(U):
        total = jnp.zeros((), dtype=RDTYPE)
        npairs = 0
        sites = jnp.arange(V)
        for mu in range(3):
            for nu in range(mu + 1, 3):
                x_mu = nbr[mu, 0, sites]
                x_nu = nbr[nu, 0, sites]
                P = sun_mul(U[mu * V + sites], U[nu * V + x_mu])
                P = sun_mul(P, sun_dagger(U[mu * V + x_nu]))
                P = sun_mul(P, sun_dagger(U[nu * V + sites]))
                trP = (P[..., 0, 0] + P[..., 1, 1] + P[..., 2, 2]).real
                total = total + jnp.sum(trP / 3.0)
                npairs += V
        return total / npairs

    return plaq


# ============================================================================
#  HMC step — symplectic leapfrog on SU(3)^{n_links}
# ============================================================================
#
# Parametrise updates by 8-vectors p_a per link. The hamiltonian is
#
#     H(p, U) = (1/2) Σ_links Σ_a p_a^2  + S_W(U)
#
# Force is the gradient of S_W under U → exp(i Σ p_a T_a) U at p = 0.
# We compute this via jax.grad on a "shadow vector" lifted near p=0 at each step.
#
# Concretely : define
#     S_shadow(δp; U) = S_W(  exp(i Σ δp_a T_a) · U  )
# Then  F_a(link, U) = ∂ S_shadow / ∂ δp_a   evaluated at δp = 0.
#
# Leapfrog step τ = ε * n_md with adaptive ε. Standard structure :
#   p ← p − (ε/2) F(U)
#   U ← exp(i ε Σ p_a T_a) U
#   for i in 1..n_md-1 :
#     p ← p − ε F(U)
#     U ← exp(i ε Σ p_a T_a) U
#   p ← p − (ε/2) F(U)
#
# Metropolis accept/reject on ΔH at end.

def make_hmc_step(L, beta, nbr, n_md, eps):
    """Build a JIT-compiled HMC step function."""
    V = L ** 3
    n_links = 3 * V
    S = make_compute_action(L, beta, nbr)

    def S_shadow_p_at(U, delta_p):
        """S_W(exp(i Σ δp T_a) U). delta_p shape (n_links, 8)."""
        # Build (n_links, 3, 3) matrices exp(i δp · T)
        delta_U = expmap_su3(delta_p)
        U_new = sun_mul(delta_U, U)
        return S(U_new)

    # Force = ∂ S_shadow / ∂ δp at δp=0
    grad_S_p = jax.jit(jax.grad(S_shadow_p_at, argnums=1))

    def compute_force(U):
        # We need F(U) = grad at δp=0. Use a zero vector.
        zero_p = jnp.zeros((n_links, 8), dtype=RDTYPE)
        return grad_S_p(U, zero_p)

    compute_force = jax.jit(compute_force)

    @jax.jit
    def hmc_step(U, key):
        key, k_p, k_acc = jax.random.split(key, 3)
        # Refresh momenta : Normal(0, 1)^{n_links × 8}
        p = jax.random.normal(k_p, (n_links, 8), dtype=RDTYPE)
        # Save initial K0 from refreshed momenta (BEFORE half-step)
        K0 = 0.5 * jnp.sum(p * p)
        S0 = S(U)
        H0 = K0 + S0
        # Initial half-step momentum kick
        F = compute_force(U)
        p = p - 0.5 * eps * F

        # Leapfrog loop via fori_loop (constant compile time wrt n_md)
        def leapfrog_body(i, state):
            U_c, p_c = state
            # Position update
            dU = expmap_su3(eps * p_c)
            U_c = sun_mul(dU, U_c)
            U_c = project_sun(U_c)
            # Momentum update (full ε)
            F_c = compute_force(U_c)
            p_c = p_c - eps * F_c
            return (U_c, p_c)

        # n_md-1 full steps
        U_curr, p_curr = jax.lax.fori_loop(0, n_md - 1, leapfrog_body, (U, p))

        # Final position step
        delta_U = expmap_su3(eps * p_curr)
        U_curr = sun_mul(delta_U, U_curr)
        U_curr = project_sun(U_curr)
        # Final half-step momentum
        F_final = compute_force(U_curr)
        p_curr = p_curr - 0.5 * eps * F_final

        # End energy
        K1 = 0.5 * jnp.sum(p_curr * p_curr)
        S1 = S(U_curr)
        H1 = K1 + S1

        dH = H1 - H0
        # Metropolis accept
        u = jax.random.uniform(k_acc)
        accept = (u < jnp.exp(-dH)) | (dH < 0)
        # Conditional select (since this is jitted)
        U_out = jnp.where(accept, U_curr, U)
        return U_out, key, dH, accept

    return hmc_step, compute_force, S


# ============================================================================
#  Migdal-Kadanoff naive block-spin 2→1 (3D, SU(3))
# ============================================================================

def block_spin_naive_3D(U_flat, L, nbr):
    """Naive MK block-spin : tilde{U} = U_1 · U_2 projected to SU(3).

    Decimation along straight 2-link path : at each coarse site X=(X0,X1,X2),
    coarse link in direction μ is U[μ](2X) · U[μ](2X + ê_μ).

    Returns U_coarse_flat shape (3 * L_c^3, 3, 3) where L_c = L/2.
    Requires L even.
    """
    assert L % 2 == 0, f"L={L} must be even for 2→1 block-spin"
    L_c = L // 2
    V_c = L_c ** 3
    V = L ** 3

    # Build coarse link layout
    U_coarse = np.zeros((3 * V_c, 3, 3), dtype=np.complex64)
    U_np = np.array(U_flat)  # to host

    for mu in range(3):
        for X0 in range(L_c):
            for X1 in range(L_c):
                for X2 in range(L_c):
                    x0, x1, x2 = 2 * X0, 2 * X1, 2 * X2
                    f1 = x0 * L * L + x1 * L + x2
                    xs = [x0, x1, x2]
                    xs[mu] = (xs[mu] + 1) % L
                    f2 = xs[0] * L * L + xs[1] * L + xs[2]
                    U1 = U_np[mu * V + f1]
                    U2 = U_np[mu * V + f2]
                    Uprod = U1 @ U2
                    # Polar projection to SU(3)
                    Vmat, _, WH = np.linalg.svd(Uprod)
                    proj = Vmat @ WH
                    det = np.linalg.det(proj)
                    phase = det / max(abs(det), 1e-15)
                    angle = np.angle(phase)
                    proj = proj / np.exp(1j * angle / 3.0)
                    c_idx = X0 * L_c * L_c + X1 * L_c + X2
                    U_coarse[mu * V_c + c_idx] = proj
    return jnp.array(U_coarse)


def plaquette_avg_3D_numpy(U_flat, L):
    """Compute <P> on a lattice of size L^3 (numpy, simple, used post-block)."""
    V = L ** 3
    U_np = np.array(U_flat)
    total = 0.0
    npairs = 0
    for x0 in range(L):
        for x1 in range(L):
            for x2 in range(L):
                site = x0 * L * L + x1 * L + x2
                for mu in range(3):
                    for nu in range(mu + 1, 3):
                        xs_mu = [x0, x1, x2]
                        xs_mu[mu] = (xs_mu[mu] + 1) % L
                        x_mu_idx = xs_mu[0] * L * L + xs_mu[1] * L + xs_mu[2]
                        xs_nu = [x0, x1, x2]
                        xs_nu[nu] = (xs_nu[nu] + 1) % L
                        x_nu_idx = xs_nu[0] * L * L + xs_nu[1] * L + xs_nu[2]
                        U1 = U_np[mu * V + site]
                        U2 = U_np[nu * V + x_mu_idx]
                        U3 = U_np[mu * V + x_nu_idx].conj().T
                        U4 = U_np[nu * V + site].conj().T
                        P = U1 @ U2 @ U3 @ U4
                        total += (P[0, 0] + P[1, 1] + P[2, 2]).real / 3.0
                        npairs += 1
    return total / npairs


# ============================================================================
#  Pipeline : run HMC, save config, then MK
# ============================================================================

def run_hmc_one_beta(L, beta, n_therm, n_meas, n_md, eps, seed, verbose=True):
    """Run HMC SU(3) D=3 at fixed beta. Returns (U_final, <P>, acc_rate)."""
    V = L ** 3
    nbr = build_neighbors_3D(L)
    key = jax.random.PRNGKey(seed)

    # Initialize hot
    keys = jax.random.split(key, 3)
    U = random_su3(keys[0], (3 * V,))
    key = keys[1]

    hmc_step, force_fn, S_fn = make_hmc_step(L, beta, nbr, n_md, eps)
    plaq_fn = make_compute_plaquette_avg(L, nbr)

    P_init = float(plaq_fn(U))
    if verbose:
        print(f"  [β={beta}] init  <P>={P_init:.4f}  (hot)")

    # Thermalize
    n_acc = 0
    dHs = []
    t0 = time.time()
    for step in range(n_therm):
        U, key, dH, accept = hmc_step(U, key)
        n_acc += int(accept)
        dHs.append(float(dH))
        if verbose and (step + 1) % max(1, n_therm // 5) == 0:
            cur_P = float(plaq_fn(U))
            print(f"  [β={beta}] therm {step+1}/{n_therm}  <P>={cur_P:.4f}"
                  f"  acc={n_acc/(step+1):.2f}  dH={float(dH):+.2f}  "
                  f"t={time.time()-t0:.0f}s")
    therm_acc = n_acc / n_therm

    # Measure
    P_meas = []
    n_acc_m = 0
    for step in range(n_meas):
        for _ in range(2):  # 2 inter-meas sweeps
            U, key, dH, accept = hmc_step(U, key)
            n_acc_m += int(accept)
        P_meas.append(float(plaq_fn(U)))
    meas_acc = n_acc_m / (n_meas * 2)
    P_mean = float(np.mean(P_meas))
    P_err = float(np.std(P_meas) / np.sqrt(max(1, len(P_meas))))
    if verbose:
        print(f"  [β={beta}] DONE  <P>={P_mean:.4f}±{P_err:.4f}  "
              f"therm_acc={therm_acc:.2f} meas_acc={meas_acc:.2f}  "
              f"t={time.time()-t0:.0f}s")

    return U, P_mean, P_err, therm_acc, meas_acc, P_meas


def run_mk_one_config(U_fine, L, beta):
    """Block-spin once (L→L/2), compute <P>_coarse, return delta = <P>_a - <P>_a/2.

    Returns dict with <P>_fine (numpy direct), <P>_coarse, Δ.
    """
    P_fine_np = plaquette_avg_3D_numpy(U_fine, L)
    if L < 4 or L % 2 != 0:
        return {"L_fine": L, "L_coarse": None, "P_fine": float(P_fine_np),
                "P_coarse": None, "delta_MK": None,
                "note": f"L={L} too small or not even for 2:1 block"}
    U_coarse = block_spin_naive_3D(U_fine, L, None)
    L_c = L // 2
    P_coarse_np = plaquette_avg_3D_numpy(U_coarse, L_c)
    delta = P_fine_np - P_coarse_np
    return {
        "L_fine": L,
        "L_coarse": L_c,
        "P_fine": float(P_fine_np),
        "P_coarse": float(P_coarse_np),
        "delta_MK": float(delta),
    }


def fit_alpha_loglog(betas, deltas):
    """Fit α from -d log Δ⟨P⟩MK / d log β via linear regression.

    Δ⟨P⟩MK ≈ C · β^{-α}  ⟹  log Δ = log C - α log β
    Returns (α, σ_α, intercept, R²).
    """
    betas = np.array(betas, dtype=float)
    deltas = np.array(deltas, dtype=float)
    # Only fit datapoints with delta > 0 (positive on physical grounds)
    mask = (deltas > 0) & np.isfinite(deltas)
    if mask.sum() < 2:
        return None, None, None, None
    lb = np.log(betas[mask])
    ld = np.log(deltas[mask])
    n = lb.size
    # Linear regression : ld = m * lb + c, then α = -m
    m, c = np.polyfit(lb, ld, 1)
    yhat = m * lb + c
    ss_res = float(np.sum((ld - yhat) ** 2))
    ss_tot = float(np.sum((ld - np.mean(ld)) ** 2))
    R2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    # Standard error on slope
    s_resid = np.sqrt(ss_res / max(1, n - 2))
    s_xx = np.sum((lb - np.mean(lb)) ** 2)
    sigma_m = s_resid / np.sqrt(s_xx) if s_xx > 0 else float("inf")
    return float(-m), float(sigma_m), float(c), float(R2)


# ============================================================================
#  Main : β-scan + MK + α fit
# ============================================================================

def main(betas, L=6, n_therm=200, n_meas=25, n_md=20, eps=None, seed=42,
         outdir=None, log_path=None):
    print("=" * 78)
    print(f"SU(3) HMC D=3 — JAX β-scan + Migdal-Kadanoff α fit")
    print(f"L={L}  V={L**3}  n_links={3*L**3}  betas={betas}")
    print(f"n_therm={n_therm}  n_meas={n_meas}  n_md={n_md}")
    print(f"Framework prediction : α = 1 - 1/(2·(D-1)) = 1 - 1/4 = 3/4 = 0.750")
    print("=" * 78)

    if outdir is None:
        outdir = "/tmp/voie1_calcs"
    os.makedirs(outdir, exist_ok=True)

    results = []
    t_start = time.time()

    for beta in betas:
        # Adaptive ε : standard HMC eps ~ 0.1 / √β at large β
        # Anti-fab : avoid overshoot at large β by ε ~ 0.15 / √(1+β/10)
        if eps is None:
            eps_use = float(0.15 / np.sqrt(1.0 + beta / 10.0))
        else:
            eps_use = float(eps)

        print(f"\n[β = {beta}]  eps = {eps_use:.4f}")
        try:
            U_final, P_mean, P_err, t_acc, m_acc, P_series = run_hmc_one_beta(
                L=L, beta=beta, n_therm=n_therm, n_meas=n_meas,
                n_md=n_md, eps=eps_use, seed=seed + int(beta), verbose=True,
            )
            mk = run_mk_one_config(U_final, L, beta)
            results.append({
                "beta": float(beta),
                "P_mean": P_mean,
                "P_err": P_err,
                "P_series": P_series,
                "therm_acc": t_acc,
                "meas_acc": m_acc,
                "eps": eps_use,
                "MK": mk,
            })
            print(f"  MK : <P>_fine={mk['P_fine']:.4f}  <P>_coarse={mk.get('P_coarse')}  "
                  f"Δ={mk.get('delta_MK')}")
        except Exception as e:
            print(f"  ERROR at β={beta} : {e}")
            results.append({"beta": float(beta), "error": str(e)})

    # Fit α from log Δ⟨P⟩MK vs log β
    betas_ok = [r["beta"] for r in results if "MK" in r and r["MK"].get("delta_MK")
                is not None]
    deltas_ok = [r["MK"]["delta_MK"] for r in results if "MK" in r
                 and r["MK"].get("delta_MK") is not None]

    alpha_fit = sigma_alpha = R2 = None
    if len(betas_ok) >= 2:
        # Filter to positive deltas only (anti-fab : negative Δ would mean
        # block-spin INCREASES plaquette, unphysical for naive MK)
        bs = []
        ds = []
        for b, d in zip(betas_ok, deltas_ok):
            if d > 0:
                bs.append(b); ds.append(d)
        if len(bs) >= 2:
            alpha_fit, sigma_alpha, _, R2 = fit_alpha_loglog(bs, ds)

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    for r in results:
        if "error" in r:
            print(f"  β={r['beta']:>6}  ERROR : {r['error']}")
            continue
        mk = r["MK"]
        d = mk.get("delta_MK")
        d_str = f"{d:+.4f}" if d is not None else "n/a"
        d_pct = f"{100*d/mk['P_fine']:+.2f}%" if d is not None and mk["P_fine"] > 0 else "n/a"
        print(f"  β={r['beta']:>6}  <P>={r['P_mean']:.4f}±{r['P_err']:.4f}  "
              f"acc={r['meas_acc']:.2f}  ΔMK={d_str} ({d_pct})")

    if alpha_fit is not None:
        match = abs(alpha_fit - 0.75) < (0.1 + sigma_alpha)
        print()
        print(f"  α (fit log-log) = {alpha_fit:.3f} ± {sigma_alpha:.3f}  (R²={R2:.3f})")
        print(f"  Framework prediction α = 3/4 = 0.750")
        print(f"  Δ = {alpha_fit - 0.75:+.3f}  =>  {'MATCH 3/4 ✓' if match else 'MISMATCH ✗'}")
    else:
        print("\n  α : insufficient datapoints (need ≥ 2 positive Δ)")

    out_json = os.path.join(outdir, f"su3_hmc_d3_L{L}_results.json")
    with open(out_json, "w") as f:
        json.dump({
            "L": L, "betas": list(betas),
            "n_therm": n_therm, "n_meas": n_meas, "n_md": n_md,
            "framework_pred_alpha": 0.75,
            "alpha_fit": alpha_fit,
            "sigma_alpha": sigma_alpha,
            "R2": R2,
            "results": results,
            "wall_time_sec": time.time() - t_start,
        }, f, indent=2)
    print(f"\nSaved → {out_json}")

    if log_path:
        with open(log_path, "w") as f:
            f.write(f"SU(3) HMC D=3 — L={L}  betas={betas}\n")
            f.write(f"n_therm={n_therm}  n_meas={n_meas}  n_md={n_md}\n\n")
            for r in results:
                if "error" in r:
                    f.write(f"β={r['beta']:>6}  ERROR : {r['error']}\n")
                    continue
                mk = r["MK"]
                d = mk.get("delta_MK")
                d_str = f"{d:+.4f}" if d is not None else "n/a"
                f.write(f"β={r['beta']:>6}  <P>={r['P_mean']:.4f}±{r['P_err']:.4f}  "
                        f"acc={r['meas_acc']:.2f}  ΔMK={d_str}\n")
            if alpha_fit is not None:
                f.write(f"\nα (fit log-log) = {alpha_fit:.3f} ± {sigma_alpha:.3f}\n")
                f.write(f"Framework prediction α = 3/4 = 0.750\n")
                f.write(f"Δ vs 3/4 = {alpha_fit - 0.75:+.3f}\n")
            f.write(f"\nWall time = {time.time()-t_start:.1f} s\n")
        print(f"Saved log → {log_path}")

    return results, alpha_fit, sigma_alpha


# ============================================================================
#  CLI
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--betas", type=float, nargs="+",
                        default=[10.0, 25.0, 50.0, 100.0, 200.0])
    parser.add_argument("--L", type=int, default=6)
    parser.add_argument("--n_therm", type=int, default=200)
    parser.add_argument("--n_meas", type=int, default=25)
    parser.add_argument("--n_md", type=int, default=20)
    parser.add_argument("--eps", type=float, default=None,
                        help="HMC step (auto if None)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--outdir", type=str, default="/tmp/voie1_calcs")
    parser.add_argument("--log", type=str,
                        default="/tmp/voie1_calcs/su3_hmc_d3_test_2026-05-24.log")
    parser.add_argument("--smoke", action="store_true",
                        help="Quick smoke test L=4 β=10 small therm")
    args = parser.parse_args()

    if args.smoke:
        print("SMOKE TEST : L=4 β=10 n_therm=20 n_meas=5")
        main(betas=[10.0], L=4, n_therm=20, n_meas=5, n_md=10,
             eps=args.eps, seed=args.seed,
             outdir=args.outdir, log_path=args.log + ".smoke")
    else:
        main(betas=args.betas, L=args.L,
             n_therm=args.n_therm, n_meas=args.n_meas,
             n_md=args.n_md, eps=args.eps, seed=args.seed,
             outdir=args.outdir, log_path=args.log)
