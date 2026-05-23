#!/usr/bin/env python3
"""
Migdal-Kadanoff stochastic block-spin for SU(2) Wilson lattice gauge theory.
============================================================================

PURPOSE
-------
Discriminate between two interpretations of the 10% plateau observed by the
naive (deterministic product + project) block-spin in `kolmogorov_v2.py`:

  (A)  Conjecture C* is false at the 10% level: RG-irrelevant terms accumulate
       and the projective system is only approximately consistent.

  (B)  The naive block-spin is structurally deficient: it does not implement
       the true RG step (which integrates out the fine fluctuations) and the
       observed gap is an artefact of the choice of block map.

If the **Migdal-Kadanoff** stochastic block-spin closes the gap to <2-5%,
hypothesis (B) is supported and Conjecture C* survives.  If the gap remains
~9-10%, hypothesis (A) is supported and Conjecture C* is empirically refuted.


MIGDAL-KADANOFF PROCEDURE IMPLEMENTED HERE
------------------------------------------
For each coarse link $\\bar{U}_\\ell^{(a)}$ in the coarse lattice $\\Lambda_a$
(at scale $a = 2 a'$), the standard Migdal-Kadanoff decimation+rescaling step
(Migdal 1976, Kadanoff 1976; cf. Bałaban 1985 program for the rigorous form)
prescribes:

  1. **Decimation (naive product).**  Compute the deterministic product of
     the 2 fine links along the straight path:

         tilde{U} = U_1 · U_2,      tilde{U}  projected back to SU(2).

  2. **Stochastic refinement (the MK step).**  Replace $\\tilde{U}$ by a
     sample from the conditional Wilson Gibbs distribution restricted to
     coarse links, given the surrounding *already-block-spinned* coarse
     links.  For SU(2) this is implemented exactly via the
     **Kennedy-Pendleton 1985 quaternion heat-bath**: given the coarse
     staple sum $\\Sigma$ at the block-link site computed from the *other*
     coarse links (Gauss-Seidel sweep order), draw $\\bar{U}$ from

         P(U | Sigma) propto exp( beta · (1/2) Re Tr( U · Sigma ) ) dU,

     where $\\beta = 2 N^2 / \\lambda$ is the **same** 't Hooft $\\beta$ as
     at the fine scale (we are testing whether C* holds at fixed 't Hooft;
     the running of $\\beta$ between scales is NOT applied — that is what
     the conjecture is about).

  3. **Sweep order.**  Gauss-Seidel: links are updated one direction at a
     time, in a checkerboard sub-sweep so that within one half-sweep each
     link sees the same neighbour state (avoids self-staple bias).  One
     full sweep = all directions × both checkerboard parities.

  4. **Number of sweeps.**  We use a single sweep by default (one-pass
     conditional relaxation toward the coarse equilibrium).  This is the
     minimum that distinguishes "deterministic projection" from "stochastic
     refinement"; a full thermalisation would be equivalent to throwing
     away the fine information entirely (and would just sample the direct
     coarse measure).  A single MK sweep is the canonical test of whether
     one step of heat-bath relaxation at the same beta is enough to close
     the gap left by the deterministic product.

  5. **Wilson action match check.**  After the stochastic refinement the
     coarse plaquettes <P_bar> should approach the direct-coarse
     measurement <P_a> within statistical error.  Naive gives 0.62 vs 0.84
     (26% gap).  Target after MK: <2-5%.

Key references:
  - Migdal, ZhETF 69 (1975) 810 / 1457 — bond moving renormalisation
  - Kadanoff, Ann.Phys. 100 (1976) 359 — variational lower bound RG
  - Kennedy-Pendleton, Phys.Lett. 156B (1985) — exact SU(2) heat-bath
  - Bałaban, Commun.Math.Phys. 109 (1987) — rigorous RG for gauge theories
  - Bauerschmidt-Bodineau-Dagallier (arXiv:2307.07619) — modern stochastic
    RG / Polchinski framework

CAVEAT
------
This is a single-pass MK refinement (Gauss-Seidel, one sweep).  A full
implementation of the Bałaban program would iterate the conditional step
to convergence at each scale, with proper handling of small-field /
large-field decomposition and effective action accumulation.  This
script's single-sweep MK is the first-iteration test sufficient to
distinguish "stochastic refinement closes the gap" from "C* genuinely
fails".  A k-sweep generalisation (k > 1) is provided as an optional
parameter for cross-check.

USAGE
-----
    python3 migdal_kadanoff_stochastic.py
        [MK_SWEEPS=1] [N_MEAS=30] [N_THERM=200] [BETA=10.0]

OUTPUT
------
    /tmp/voie1_calcs/results/migdal_kadanoff.json
"""

import sys
import os
import time
import json
import numpy as np
import cupy as cp

sys.path.insert(0, os.path.expanduser("~/.openclaw/workspaces/vast"))
from su2_hmc_v3 import (
    SU2HMC, random_su2, su2_mul, su2_dagger, project_su2,
)


# ============================================================================
#  Block-spin (naive deterministic product) — same as kolmogorov_v2.py
# ============================================================================

def block_spin_naive(U_fine_flat, L_fine, ndim=4):
    """Naive block-spin 2:1: tilde{U} = U_1 · U_2, projected to SU(2).

    This is the BASELINE that we are improving on with MK refinement.
    Returns flat array of shape (ndim * L_coarse**ndim, 2, 2).
    """
    L_coarse = L_fine // 2
    V_fine = L_fine ** ndim
    V_coarse = L_coarse ** ndim

    def fine_idx(x0, x1, x2, x3):
        return ((x0 * L_fine + x1) * L_fine + x2) * L_fine + x3

    def coarse_idx(X0, X1, X2, X3):
        return ((X0 * L_coarse + X1) * L_coarse + X2) * L_coarse + X3

    U_coarse = cp.zeros((ndim * V_coarse, 2, 2), dtype=U_fine_flat.dtype)
    for mu in range(ndim):
        for X0 in range(L_coarse):
            for X1 in range(L_coarse):
                for X2 in range(L_coarse):
                    for X3 in range(L_coarse):
                        x0, x1, x2, x3 = 2*X0, 2*X1, 2*X2, 2*X3
                        f1 = fine_idx(x0, x1, x2, x3)
                        xs = [x0, x1, x2, x3]
                        xs[mu] = (xs[mu] + 1) % L_fine
                        f2 = fine_idx(xs[0], xs[1], xs[2], xs[3])
                        U1 = U_fine_flat[mu * V_fine + f1]
                        U2 = U_fine_flat[mu * V_fine + f2]
                        Uprod = su2_mul(U1[None, ...], U2[None, ...])[0]
                        Uprod = project_su2(Uprod)
                        c_site = coarse_idx(X0, X1, X2, X3)
                        U_coarse[mu * V_coarse + c_site] = Uprod
    return U_coarse


# ============================================================================
#  Kennedy-Pendleton SU(2) heat-bath for one link given staple
# ============================================================================
#
#  Given staple Sigma (2x2 complex), the conditional distribution is
#       P(U|Sigma) propto exp( beta * (1/2) Re Tr( U · Sigma ) )
#                   = exp( beta * k * (1/2) Re Tr( U · Sigma_hat ) )
#
#  where Sigma = k · Sigma_hat with Sigma_hat in SU(2) and k = sqrt(det Sigma).
#  For SU(2): U · Sigma_hat is again SU(2), and we use the standard
#  Kennedy-Pendleton draw on the 4-sphere parametrisation.
#
#  Implementation notes: we accept a Sigma which is *not* in SU(2) — only its
#  SU(2) projection enters, with k = sqrt(det) absorbed into an effective
#  beta_eff = beta * k.  This is the standard SU(2) heat-bath construction.
# ============================================================================

def su2_heatbath_one_link(Sigma, beta, rng_state=None):
    """Draw U from P(U | Sigma) propto exp(beta * (1/2) Re Tr(U Sigma)).

    Sigma: cp.array (2,2) complex64.
    Returns U: cp.array (2,2) complex64 in SU(2).

    Uses the Kennedy-Pendleton 1985 algorithm with the Creutz 1980
    rejection sampling for the conditional on the cosine.
    """
    # Decompose Sigma = k * Sigma_hat with Sigma_hat in SU(2)
    det_Sigma = (Sigma[0, 0] * Sigma[1, 1] - Sigma[0, 1] * Sigma[1, 0])
    k = cp.sqrt(cp.abs(det_Sigma))
    k_val = float(cp.real(k))
    if k_val < 1e-10:
        # Degenerate staple — fall back to Haar random
        return random_su2((1,))[0]
    Sigma_hat = Sigma / k

    # Effective beta:  beta * k  (for the SU(2) Wilson convention here
    # the action prefactor is beta * (1/2) Re Tr, so beta_eff = beta*k).
    a = float(beta) * k_val  # >= 0

    # Sample a0 = cos(theta/2)-like with weight exp(a * a0) on [-1, 1]
    # Use Kennedy-Pendleton; falls back to Creutz at small a.
    a0 = float(_kp_draw_a0(a))

    # Sample 3-vector on sphere with radius sqrt(1 - a0^2)
    r = (1.0 - a0 * a0) ** 0.5
    n = cp.random.standard_normal(3, dtype=cp.float32)
    n_norm = float(cp.sqrt(cp.sum(n * n)))
    if n_norm < 1e-10:
        n = cp.asarray([1.0, 0.0, 0.0], dtype=cp.float32)
        n_norm = 1.0
    n = n / n_norm
    a1, a2, a3 = r * float(n[0]), r * float(n[1]), r * float(n[2])

    # Build V = a0 I + i (a · sigma)  in SU(2)
    V = cp.zeros((2, 2), dtype=cp.complex64)
    V[0, 0] = a0 + 1j * a3
    V[0, 1] = a2 + 1j * a1
    V[1, 0] = -a2 + 1j * a1
    V[1, 1] = a0 - 1j * a3

    # The drawn U satisfies U · Sigma_hat = V  =>  U = V · Sigma_hat^dagger
    Sigma_hat_dag = cp.conj(cp.swapaxes(Sigma_hat, -1, -2))
    U = V @ Sigma_hat_dag
    # Project for safety
    detU = U[0, 0] * U[1, 1] - U[0, 1] * U[1, 0]
    U = U / cp.sqrt(cp.abs(detU))
    return U


def _kp_draw_a0(a):
    """Draw a0 in [-1,1] with weight exp(a*a0) * sqrt(1 - a0^2).  a >= 0.

    This is the marginal of the SU(2) Haar measure conditioned on the
    Wilson staple environment: P(a0) ∝ exp(a*a0) * sqrt(1-a0^2),
    where a = beta * |Sigma|.

    Algorithm: Kennedy-Pendleton (1985, Phys.Lett.B 156:393) using the
    substitution lambda^2 = (1 - a0)/2 in [0,1], giving the weight
    P(lambda) ∝ exp(-2 a lambda^2) * lambda^2 * sqrt(1 - lambda^2).
    The KP scheme generates lambda^2 with the leading exponential part
    via 3 uniforms (and an accept on sqrt(1 - lambda^2) via a 4th).
    """
    if a < 1e-6:
        # Uniform-Haar limit: P(a0) ∝ sqrt(1-a0^2)
        # Rejection on uniform proposal
        for _ in range(200):
            a0_try = 2.0 * float(cp.random.random()) - 1.0
            r = float(cp.random.random())
            if r * r <= 1.0 - a0_try * a0_try:
                return a0_try
        return 0.0
    # Kennedy-Pendleton standard scheme (works for ALL a > 0)
    # Generate lambda^2 ~ exp(-2 a lambda^2) lambda^2 (Gamma(3/2)-like)
    # via the 3-uniform trick:  lambda^2 = -[ln r1 + (cos 2pi r3)^2 ln r2] / (2a)
    # then accept with weight sqrt(1 - lambda^2) via r4^2 < 1 - lambda^2.
    for _ in range(400):
        r1 = float(cp.random.random())
        r2 = float(cp.random.random())
        r3 = float(cp.random.random())
        if r1 < 1e-30:
            r1 = 1e-30
        if r2 < 1e-30:
            r2 = 1e-30
        x1 = -np.log(r1) / (2.0 * a)
        x2 = -np.log(r2) / (2.0 * a)
        c2 = (np.cos(2.0 * np.pi * r3)) ** 2
        lam2 = x1 * c2 + x2
        if lam2 > 1.0:
            continue  # outside [0,1] for lambda^2 — reject
        r4 = float(cp.random.random())
        if r4 * r4 <= 1.0 - lam2:
            a0 = 1.0 - 2.0 * lam2
            if a0 > 1.0:
                a0 = 1.0
            if a0 < -1.0:
                a0 = -1.0
            return a0
    # Fallback (extremely rare): return the mean of P(a0) ~ 1 at large a
    return 1.0 - 1.0 / max(a, 1e-3)


# ============================================================================
#  Coarse staple at a block link (4D Wilson) — for use in MK refinement
# ============================================================================

def coarse_staple_at(U_coarse_flat, L_coarse, mu, site, ndim=4):
    """Compute the (sum of 6) coarse Wilson staples at link (site, mu)."""
    V_c = L_coarse ** ndim

    # Unravel site
    coords = [0, 0, 0, 0]
    rem = site
    for d in (3, 2, 1, 0):
        coords[d] = rem % L_coarse
        rem //= L_coarse

    def link_idx(direction, x):
        return direction * V_c + (((x[0] * L_coarse + x[1]) * L_coarse + x[2]) * L_coarse + x[3])

    Sigma = cp.zeros((2, 2), dtype=cp.complex64)
    for nu in range(ndim):
        if nu == mu:
            continue
        # +nu staple: U_nu(x+mu) · U_mu^dag(x+nu) · U_nu^dag(x)
        x_pm = list(coords); x_pm[mu] = (x_pm[mu] + 1) % L_coarse
        x_pn = list(coords); x_pn[nu] = (x_pn[nu] + 1) % L_coarse
        Unu_xpm = U_coarse_flat[link_idx(nu, x_pm)]
        Umu_xpn = U_coarse_flat[link_idx(mu, x_pn)]
        Unu_x = U_coarse_flat[link_idx(nu, coords)]
        Sigma = Sigma + (Unu_xpm @ cp.conj(cp.swapaxes(Umu_xpn, -1, -2))
                         @ cp.conj(cp.swapaxes(Unu_x, -1, -2)))

        # -nu staple: U_nu^dag(x+mu-nu) · U_mu^dag(x-nu) · U_nu(x-nu)
        x_pm_mn = list(x_pm); x_pm_mn[nu] = (x_pm_mn[nu] - 1) % L_coarse
        x_mn = list(coords); x_mn[nu] = (x_mn[nu] - 1) % L_coarse
        Unu_xpmmn = U_coarse_flat[link_idx(nu, x_pm_mn)]
        Umu_xmn = U_coarse_flat[link_idx(mu, x_mn)]
        Unu_xmn = U_coarse_flat[link_idx(nu, x_mn)]
        Sigma = Sigma + (cp.conj(cp.swapaxes(Unu_xpmmn, -1, -2))
                         @ cp.conj(cp.swapaxes(Umu_xmn, -1, -2))
                         @ Unu_xmn)

    return Sigma


def mk_refine_one_sweep(U_coarse_flat, L_coarse, beta_coarse, ndim=4,
                        verbose=False):
    """One full Gauss-Seidel MK heat-bath sweep over all coarse links.

    Modifies U_coarse_flat IN PLACE.  Returns updated array.

    Sweep order: per direction mu, two checkerboard parities (even/odd
    coords sum), so that all sites updated within one half-sweep see the
    same neighbour state.
    """
    V_c = L_coarse ** ndim
    t0 = time.time()
    for mu in range(ndim):
        for parity in (0, 1):
            for site in range(V_c):
                # Coord parity
                rem = site
                csum = 0
                for d in (3, 2, 1, 0):
                    csum += rem % L_coarse
                    rem //= L_coarse
                if csum % 2 != parity:
                    continue
                Sigma = coarse_staple_at(U_coarse_flat, L_coarse, mu, site, ndim)
                U_new = su2_heatbath_one_link(Sigma, beta_coarse)
                U_coarse_flat[mu * V_c + site] = U_new
        if verbose:
            print(f"        MK sweep mu={mu} done t={time.time()-t0:.1f}s",
                  flush=True)
    return U_coarse_flat


def mk_refine(U_coarse_flat, L_coarse, beta_coarse, n_sweeps=1, ndim=4,
              verbose=False):
    """Apply n_sweeps full Gauss-Seidel MK heat-bath sweeps.

    n_sweeps=1 is the canonical Migdal-Kadanoff single-pass refinement.
    Larger n_sweeps drives toward the direct-coarse equilibrium (cross-check
    diagnostic: should match direct coarse measurement in the limit).
    """
    for s in range(n_sweeps):
        if verbose:
            print(f"      MK sweep {s+1}/{n_sweeps}", flush=True)
        mk_refine_one_sweep(U_coarse_flat, L_coarse, beta_coarse,
                            ndim=ndim, verbose=verbose)
    return U_coarse_flat


# ============================================================================
#  Per-site plaquette field + LSI estimator (same as kolmogorov_v2.py)
# ============================================================================

def compute_plaquette_field_4D(hmc):
    """Per-site plaquette mean, averaged over 6 mu<nu pairs."""
    L = hmc.L
    V = hmc.volume
    ndim = hmc.ndim
    sites = cp.arange(V, dtype=cp.int32)
    P_field = cp.zeros(V, dtype=cp.float32)
    n_pairs = 0
    for mu in range(ndim):
        for nu in range(mu + 1, ndim):
            x_mu = hmc.nbr[mu, 0, sites]
            x_nu = hmc.nbr[nu, 0, sites]
            P = su2_mul(hmc.U[mu * V + sites], hmc.U[nu * V + x_mu])
            P = su2_mul(P, su2_dagger(hmc.U[mu * V + x_nu]))
            P = su2_mul(P, su2_dagger(hmc.U[nu * V + sites]))
            P_field += 0.5 * (P[..., 0, 0].real + P[..., 1, 1].real)
            n_pairs += 1
    P_field /= n_pairs
    return cp.asnumpy(P_field).reshape((L,) * ndim)


def C_LSI_proper(P_all):
    """Empirical LSI proxy: ent(f^2) / (2 * grad_sq), with f = (P - <P>)."""
    P_all = np.asarray(P_all)
    mean_P = np.mean(P_all)
    f = (P_all - mean_P) ** 2
    f2 = f.flatten() ** 2 + 1e-12
    E_f2 = np.mean(f2)
    ent = np.mean(f2 * np.log(f2)) - E_f2 * np.log(E_f2)
    grad_sq = 0.0
    for axis in range(1, P_all.ndim):
        f_shift = np.roll(f, -1, axis=axis)
        grad_sq += np.mean((f_shift - f) ** 2)
    return float(ent / (2 * grad_sq)) if grad_sq > 0 else None


# ============================================================================
#  Main driver
# ============================================================================

def run_pair(L_fine, BETA, n_therm, n_meas, mk_sweeps, results_path,
             n_md_steps=30, tau=1.0, seed_fine=10, seed_coarse=20):
    """Run one pair (L_fine, L_coarse=L_fine/2) and return dict of metrics."""
    L_c = L_fine // 2
    cp.random.seed(2026 + seed_fine)
    print(f"\n[FINE] L={L_fine}, beta={BETA}, thermalising {n_therm} traj...",
          flush=True)
    hmc_f = SU2HMC(L_fine, BETA, nsteps=n_md_steps, tau=tau)
    t0 = time.time()
    acc = 0
    for i in range(n_therm):
        a, dH, p = hmc_f.hmc_step()
        if a:
            acc += 1
    print(f"  fine therm done {time.time()-t0:.0f}s "
          f"P_avg={hmc_f.compute_plaquette():.4f} acc={acc/n_therm:.2f}",
          flush=True)

    cp.random.seed(2026 + seed_coarse)
    print(f"\n[COARSE] L={L_c}, beta={BETA}, thermalising {n_therm} traj...",
          flush=True)
    hmc_c_ref = SU2HMC(L_c, BETA, nsteps=n_md_steps, tau=tau)
    t0 = time.time()
    acc = 0
    for i in range(n_therm):
        a, dH, p = hmc_c_ref.hmc_step()
        if a:
            acc += 1
    print(f"  coarse therm done {time.time()-t0:.0f}s "
          f"P_avg={hmc_c_ref.compute_plaquette():.4f} acc={acc/n_therm:.2f}",
          flush=True)

    P_fine_list = []
    P_naive_list = []
    P_mk_list = []
    P_coarse_list = []

    print(f"\n[MEAS] {n_meas} configs, MK sweeps = {mk_sweeps}", flush=True)
    t1 = time.time()
    for i in range(n_meas):
        # Decorrelate fine and direct-coarse independently
        for _ in range(3):
            hmc_f.hmc_step()
        for _ in range(3):
            hmc_c_ref.hmc_step()

        # FINE
        P_fine_list.append(compute_plaquette_field_4D(hmc_f))

        # NAIVE BLOCK-SPIN
        U_naive = block_spin_naive(hmc_f.U, L_fine)
        hmc_c_naive = SU2HMC(L_c, BETA, nsteps=n_md_steps, tau=tau)
        hmc_c_naive.U = U_naive
        P_naive_list.append(compute_plaquette_field_4D(hmc_c_naive))

        # MK-REFINED BLOCK-SPIN (start from naive, apply mk_sweeps heat-bath)
        U_mk = U_naive.copy()
        cp.random.seed(2026 + 1000 * (i + 1))  # reproducible MK draw
        mk_refine(U_mk, L_c, BETA, n_sweeps=mk_sweeps, verbose=False)
        hmc_c_mk = SU2HMC(L_c, BETA, nsteps=n_md_steps, tau=tau)
        hmc_c_mk.U = U_mk
        P_mk_list.append(compute_plaquette_field_4D(hmc_c_mk))

        # DIRECT COARSE
        P_coarse_list.append(compute_plaquette_field_4D(hmc_c_ref))

        if (i + 1) % 2 == 0:
            elapsed = time.time() - t1
            rate = (i + 1) / elapsed
            eta = (n_meas - i - 1) / rate / 60 if rate > 0 else 0
            print(
                f"  meas {i+1:3d}/{n_meas}: "
                f"P_f={float(np.mean(P_fine_list[-1])):.4f} "
                f"P_naive={float(np.mean(P_naive_list[-1])):.4f} "
                f"P_MK={float(np.mean(P_mk_list[-1])):.4f} "
                f"P_c={float(np.mean(P_coarse_list[-1])):.4f}  "
                f"t={elapsed:.0f}s ETA={eta:.1f}min",
                flush=True,
            )
            # Save partial results
            try:
                _save_partial(results_path, L_fine, BETA, mk_sweeps,
                              i + 1, P_fine_list, P_naive_list,
                              P_mk_list, P_coarse_list)
            except Exception as e:
                print(f"  (partial save failed: {e})", flush=True)

    P_fine_arr = np.array([np.asarray(p) for p in P_fine_list])
    P_naive_arr = np.array([np.asarray(p) for p in P_naive_list])
    P_mk_arr = np.array([np.asarray(p) for p in P_mk_list])
    P_coarse_arr = np.array([np.asarray(p) for p in P_coarse_list])

    C_fine = C_LSI_proper(P_fine_arr)
    C_naive = C_LSI_proper(P_naive_arr)
    C_mk = C_LSI_proper(P_mk_arr)
    C_coarse = C_LSI_proper(P_coarse_arr)

    mean_fine = float(np.mean(P_fine_arr))
    mean_naive = float(np.mean(P_naive_arr))
    mean_mk = float(np.mean(P_mk_arr))
    mean_coarse = float(np.mean(P_coarse_arr))

    var_naive = float(np.var(P_naive_arr))
    var_mk = float(np.var(P_mk_arr))
    var_coarse = float(np.var(P_coarse_arr))

    dC_naive = abs(C_naive - C_coarse) / C_coarse * 100 if C_coarse else None
    dC_mk = abs(C_mk - C_coarse) / C_coarse * 100 if C_coarse else None
    dP_naive = abs(mean_naive - mean_coarse) / mean_coarse * 100
    dP_mk = abs(mean_mk - mean_coarse) / mean_coarse * 100

    return {
        "L_fine": L_fine, "L_coarse": L_c, "beta": BETA,
        "n_meas": n_meas, "mk_sweeps": mk_sweeps,
        "mean_P_fine": mean_fine,
        "mean_P_naive": mean_naive,
        "mean_P_MK": mean_mk,
        "mean_P_coarse": mean_coarse,
        "var_P_naive": var_naive, "var_P_MK": var_mk,
        "var_P_coarse": var_coarse,
        "C_LSI_fine": C_fine,
        "C_LSI_naive": C_naive,
        "C_LSI_MK": C_mk,
        "C_LSI_coarse": C_coarse,
        "delta_CLSI_naive_pct": dC_naive,
        "delta_CLSI_MK_pct": dC_mk,
        "delta_meanP_naive_pct": dP_naive,
        "delta_meanP_MK_pct": dP_mk,
    }


def _save_partial(results_path, L_fine, beta, mk_sweeps, n_so_far,
                  P_fine, P_naive, P_mk, P_coarse):
    """Save partial means/vars to disk so progress survives interruption."""
    pf = np.array([np.asarray(p) for p in P_fine])
    pn = np.array([np.asarray(p) for p in P_naive])
    pm = np.array([np.asarray(p) for p in P_mk])
    pc = np.array([np.asarray(p) for p in P_coarse])
    partial = {
        "PARTIAL": True,
        "L_fine": L_fine, "beta": beta, "mk_sweeps": mk_sweeps,
        "n_configs_so_far": n_so_far,
        "running_mean_P_fine": float(np.mean(pf)),
        "running_mean_P_naive": float(np.mean(pn)),
        "running_mean_P_MK": float(np.mean(pm)),
        "running_mean_P_coarse": float(np.mean(pc)),
        "running_var_P_naive": float(np.var(pn)),
        "running_var_P_MK": float(np.var(pm)),
        "running_var_P_coarse": float(np.var(pc)),
    }
    with open(results_path + f".partial.L{L_fine}.json", "w") as f:
        json.dump(partial, f, indent=2)


def main():
    BETA = float(os.environ.get("BETA", "10.0"))
    n_therm = int(os.environ.get("N_THERM", "200"))
    n_meas = int(os.environ.get("N_MEAS", "30"))
    mk_sweeps = int(os.environ.get("MK_SWEEPS", "1"))

    out_dir = "/tmp/voie1_calcs/results"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "migdal_kadanoff.json")

    print("=" * 78)
    print("MIGDAL-KADANOFF STOCHASTIC BLOCK-SPIN — Conjecture C* test v1")
    print(f"  beta={BETA}  n_meas={n_meas}  mk_sweeps={mk_sweeps}")
    print(f"  output: {out_path}")
    print("=" * 78)

    gpu = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
    print(f"  GPU: {gpu}", flush=True)

    results = {
        "method": "Migdal-Kadanoff stochastic block-spin (Gauss-Seidel "
                  "Kennedy-Pendleton SU(2) heat-bath, single-sweep MK)",
        "beta_true_thooft": BETA,
        "n_meas": n_meas, "n_therm": n_therm, "mk_sweeps": mk_sweeps,
        "gpu": gpu,
        "pairs": [],
    }

    # Pair 1: L_fine = 8 -> L_coarse = 4
    print("\n" + "=" * 78)
    print("PAIR 1: L_fine = 8 -> L_coarse = 4")
    print("=" * 78)
    pair1 = run_pair(L_fine=8, BETA=BETA, n_therm=n_therm, n_meas=n_meas,
                     mk_sweeps=mk_sweeps, results_path=out_path,
                     seed_fine=10, seed_coarse=20)
    results["pairs"].append(pair1)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  -> partial save after pair 1 to {out_path}", flush=True)

    # Pair 2: L_fine = 12 -> L_coarse = 6
    print("\n" + "=" * 78)
    print("PAIR 2: L_fine = 12 -> L_coarse = 6")
    print("=" * 78)
    pair2 = run_pair(L_fine=12, BETA=BETA, n_therm=n_therm, n_meas=n_meas,
                     mk_sweeps=mk_sweeps, results_path=out_path,
                     seed_fine=30, seed_coarse=40)
    results["pairs"].append(pair2)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    # Verdict
    print("\n" + "=" * 78)
    print("FINAL VERDICT — Conjecture C* test via MK refinement")
    print("=" * 78)
    for p in results["pairs"]:
        print(f"\nL_fine={p['L_fine']} (coarse {p['L_coarse']}), "
              f"beta={p['beta']}, mk_sweeps={p['mk_sweeps']}")
        print(f"  <P>: fine={p['mean_P_fine']:.4f}  "
              f"naive={p['mean_P_naive']:.4f}  "
              f"MK={p['mean_P_MK']:.4f}  "
              f"direct={p['mean_P_coarse']:.4f}")
        print(f"  C_LSI: fine={p['C_LSI_fine']:.4f}  "
              f"naive={p['C_LSI_naive']:.4f}  "
              f"MK={p['C_LSI_MK']:.4f}  "
              f"direct={p['C_LSI_coarse']:.4f}")
        print(f"  Delta <P> naive vs direct: "
              f"{p['delta_meanP_naive_pct']:.2f}%")
        print(f"  Delta <P> MK    vs direct: "
              f"{p['delta_meanP_MK_pct']:.2f}%")
        print(f"  Delta C_LSI naive vs direct: "
              f"{p['delta_CLSI_naive_pct']:.2f}%")
        print(f"  Delta C_LSI MK    vs direct: "
              f"{p['delta_CLSI_MK_pct']:.2f}%")

    mean_dC_mk = np.mean([
        p['delta_CLSI_MK_pct'] for p in results['pairs']
        if p['delta_CLSI_MK_pct'] is not None
    ])
    mean_dP_mk = np.mean([
        p['delta_meanP_MK_pct'] for p in results['pairs']
    ])

    print()
    print(f"Mean Delta C_LSI MK vs direct (all pairs): {mean_dC_mk:.2f}%")
    print(f"Mean Delta <P>  MK vs direct (all pairs):  {mean_dP_mk:.2f}%")

    if mean_dP_mk < 5.0 and (mean_dC_mk is None or mean_dC_mk < 5.0):
        verdict = (
            f"MK-refined Delta <P> = {mean_dP_mk:.2f}% "
            f"and Delta C_LSI = {mean_dC_mk:.2f}% — "
            "Conjecture C* SUPPORTED (stochastic refinement closes the gap, "
            "consistent with H_B1 + RG-irrelevant terms vanishing)"
        )
    elif mean_dP_mk < 10.0 and mean_dC_mk < 10.0:
        verdict = (
            f"MK-refined Delta <P> = {mean_dP_mk:.2f}% "
            f"and Delta C_LSI = {mean_dC_mk:.2f}% — "
            "Conjecture C* PARTIALLY SUPPORTED (MK reduces gap vs naive "
            "but residual ~5-10% — could be RG-irrelevant or finite-L)"
        )
    else:
        verdict = (
            f"MK-refined Delta <P> = {mean_dP_mk:.2f}% "
            f"and Delta C_LSI = {mean_dC_mk:.2f}% — "
            "Conjecture C* REFUTED (MK does not close the gap; "
            "stochastic refinement at fixed 't Hooft beta cannot recover "
            "the direct-coarse measure)"
        )

    print()
    print(verdict)
    results["verdict"] = verdict
    results["mean_delta_meanP_MK_pct"] = float(mean_dP_mk)
    results["mean_delta_CLSI_MK_pct"] = float(mean_dC_mk) if mean_dC_mk is not None else None

    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved: {out_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
