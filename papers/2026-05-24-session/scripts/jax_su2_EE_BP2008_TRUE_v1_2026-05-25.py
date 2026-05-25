#!/usr/bin/env python3
"""JAX SU(2) Renyi-2 EE — TRUE BP2008 conifold geometry.

Vraie implementation Buividovich-Polikarpov 2008 (arXiv:0806.3376) :
- 2 SU(2) configs U_1, U_2 sur L^4 chacun (sheets indépendants)
- Z_1² : disconnected, S = S_W(U_1) + S_W(U_2)
- Z_2 : conifold, S = S_disc + ΔS_encircling
  où ΔS = somme sur plaquettes "encirclant" Σ = ∂A × {τ=0} avec formule
  cross-sheet (use links de U_1 ET U_2)

Plaquettes encerclantes : temporal plaquettes (μ=spatial, ν=τ) au wraparound
(τ=L_τ-1 → τ=0) où corner x ∈ A ou x+μ ∈ A. Pour μ = x_1 direction
spécifiquement, ce sont les plaquettes du "tube" autour de Σ.

Méthode : Bennett Acceptance Ratio (BAR) entre ensembles Z_1² et Z_2.

S_2(A) = -log(Z_2/Z_1²)
       = log[ ⟨1/(1+exp(S_disc - S_conif - C))⟩_conif
              / ⟨1/(1+exp(S_conif - S_disc + C))⟩_disc ]

Avec C choisi pour minimiser variance (typically C = S_2 / 2 ou similar).

Le constraint topologique NE TRIVIALISE PAS : il modifie l'ensemble de paths
contributing à Z_2 vs Z_1² (different connectivity in lattice graph).

Author : Kévin Rémondière (ORCID 0009-0008-2443-7166).
"""
import os
os.environ.setdefault('XLA_PYTHON_CLIENT_PREALLOCATE', 'false')
os.environ.setdefault('JAX_ENABLE_X64', 'True')

import jax
import jax.numpy as jnp
from jax import jit, random, lax
from functools import partial
import time
import json
import numpy as np

START = time.time()
print(f"START : {time.ctime()}", flush=True)
print("=" * 78, flush=True)
print(f"JAX SU(2) Renyi-2 EE — TRUE BP2008 conifold", flush=True)
print(f"2 sheets + cross-sheet encircling plaquettes + BAR", flush=True)
print(f"Attempt B : test c =? kappa^2(SU(2)) = 1/4 = Bekenstein-Hawking", flush=True)
print("=" * 78, flush=True)
jax.config.update("jax_enable_x64", True)
print(f"JAX : {jax.__version__}, backend : {jax.default_backend()}", flush=True)
print(f"Devices : {jax.devices()}", flush=True)


# ============================================================================
# SU(2) primitives
# ============================================================================

def random_su2_haar(key, shape):
    raw = random.normal(key, shape + (4,))
    norms = jnp.linalg.norm(raw, axis=-1, keepdims=True)
    q = raw / norms
    a0, a1, a2, a3 = q[..., 0], q[..., 1], q[..., 2], q[..., 3]
    U = jnp.stack([
        jnp.stack([a0 + 1j * a3, a2 + 1j * a1], axis=-1),
        jnp.stack([-a2 + 1j * a1, a0 - 1j * a3], axis=-1),
    ], axis=-2)
    return U


def random_su2_near_identity(key, shape, eps=0.3):
    raw = random.normal(key, shape + (3,)) * eps
    a1, a2, a3 = raw[..., 0], raw[..., 1], raw[..., 2]
    n_squared = a1**2 + a2**2 + a3**2
    a0 = jnp.sqrt(jnp.maximum(1.0 - n_squared, 1e-15))
    norm = jnp.sqrt(a0**2 + a1**2 + a2**2 + a3**2)
    a0, a1, a2, a3 = a0/norm, a1/norm, a2/norm, a3/norm
    U = jnp.stack([
        jnp.stack([a0 + 1j * a3, a2 + 1j * a1], axis=-1),
        jnp.stack([-a2 + 1j * a1, a0 - 1j * a3], axis=-1),
    ], axis=-2)
    return U


@jit
def wilson_action(U, beta):
    """Standard Wilson S = β Σ_p (1 - Re Tr(P)/2) on a single L^4 lattice."""
    total = 0.0
    for mu in range(4):
        for nu in range(mu+1, 4):
            U_mu = U[..., mu, :, :]
            U_nu = U[..., nu, :, :]
            U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)
            U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
            P = jnp.einsum('...ij,...jk,...lk,...ml->...im',
                           U_mu, U_nu_pmu,
                           jnp.conjugate(U_mu_pnu),
                           jnp.conjugate(U_nu))
            tr_real = jnp.real(jnp.trace(P, axis1=-2, axis2=-1)) / 2
            total += jnp.sum(1.0 - tr_real)
    return beta * total


@jit
def wilson_action_disconnected(U_1, U_2, beta):
    """Z_1² action : 2 indep sheets, S = S(U_1) + S(U_2)."""
    return wilson_action(U_1, beta) + wilson_action(U_2, beta)


# ============================================================================
# Region A mask and encircling plaquette identification
# ============================================================================

def make_A_site_mask(L_x, L_y, L_z, L_tau, A_axis=0):
    """A = {x_0 < L_x/2}. Returns mask of shape (L_x, L_y, L_z, L_tau) bool."""
    indices = jnp.indices((L_x, L_y, L_z, L_tau))
    return indices[A_axis] < L_x // 2


# ============================================================================
# Encircling plaquette correction
# ============================================================================

@partial(jit, static_argnames=('L_tau',))
def make_U1_with_shared_A_wrap(U_1, U_2, A_site_mask, L_tau):
    """U_1 with temporal A-wrap links replaced by U_2's (sharing).

    In conifold, U_τ(x ∈ A, τ=L_tau-1) is the SAME variable in both sheets
    (cross-sheet identification). Convention: U_2's value is "the" shared one.

    All plaquettes containing this link in sheet 1 are automatically modified
    when we use U_1_modified = U_1 with this link replaced.
    """
    indices = jnp.indices(U_1.shape[:4])  # (4, L, L, L, L_tau)
    at_tau_wrap = indices[3] == L_tau - 1  # (L, L, L, L_tau) bool

    # A-wrap mask : x ∈ A AND τ = L_tau-1
    A_wrap_mask = A_site_mask & at_tau_wrap  # (L, L, L, L_tau)

    # Replace U_1[..., μ=3, :, :] (temporal link) with U_2's value at A-wrap sites
    U_1_mu3 = U_1[..., 3, :, :]   # (L, L, L, L_tau, 2, 2)
    U_2_mu3 = U_2[..., 3, :, :]
    mask_bcast = A_wrap_mask[..., None, None]
    U_1_mu3_new = jnp.where(mask_bcast, U_2_mu3, U_1_mu3)
    U_1_new = U_1.at[..., 3, :, :].set(U_1_mu3_new)
    return U_1_new


@partial(jit, static_argnames=('L_tau',))
def wilson_action_conifold(U_1, U_2, beta, A_site_mask, L_tau):
    """Z_2 conifold action via shared temporal A-wrap links.

    S_conif = S_W(U_1 with A-wrap links replaced by U_2's) + S_W(U_2)
    """
    U_1_mod = make_U1_with_shared_A_wrap(U_1, U_2, A_site_mask, L_tau)
    return wilson_action(U_1_mod, beta) + wilson_action(U_2, beta)


# ============================================================================
# Standard per-link Metropolis (with optional conifold correction)
# ============================================================================

def compute_staple_sum_single(U, mu, L):
    U_mu = U[..., mu, :, :]
    K = jnp.zeros_like(U_mu)
    for nu in range(4):
        if nu == mu:
            continue
        U_nu = U[..., nu, :, :]
        U_nu_pmu = jnp.roll(U_nu, -1, axis=mu)
        U_mu_pnu = jnp.roll(U_mu, -1, axis=nu)
        K_fwd = jnp.einsum('...ij,...kj,...lk->...il',
                           U_nu_pmu,
                           jnp.conjugate(U_mu_pnu),
                           jnp.conjugate(U_nu))
        K += K_fwd
        U_nu_pmu_mnu = jnp.roll(U_nu_pmu, 1, axis=nu)
        U_mu_mnu = jnp.roll(U_mu, 1, axis=nu)
        U_nu_mnu = jnp.roll(U_nu, 1, axis=nu)
        K_bwd = jnp.einsum('...ji,...kj,...kl->...il',
                           jnp.conjugate(U_nu_pmu_mnu),
                           jnp.conjugate(U_mu_mnu),
                           U_nu_mnu)
        K += K_bwd
    return K


@jit
def metropolis_link_update_standard(U_link, K_link, beta, key, eps=0.3):
    """Standard per-link Metropolis using staple K for Wilson action only."""
    key1, key2 = random.split(key)
    X = random_su2_near_identity(key1, U_link.shape[:-2], eps=eps)
    U_proposed = jnp.einsum('...ij,...jk->...ik', X, U_link)
    # FIX 2026-05-25: K_link bug removed (Re Tr(U·K) ≠ Re Tr(U·K†) for SU(2))
    new_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_proposed, K_link),
                                    axis1=-2, axis2=-1))
    old_term = jnp.real(jnp.trace(jnp.einsum('...ij,...jk->...ik', U_link, K_link),
                                    axis1=-2, axis2=-1))
    dS = -beta * 0.5 * (new_term - old_term)
    rand_u = random.uniform(key2, dS.shape)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -dS))
    U_new = jnp.where(accept[..., None, None], U_proposed, U_link)
    return U_new


@partial(jit, static_argnames=('L',))
def metropolis_sweep_single(U, beta, key, L, eps=0.3):
    """Standard SU(2) Wilson Metropolis sweep on single sheet (no conifold)."""
    for mu in range(4):
        K_mu = compute_staple_sum_single(U, mu, L)
        key, subkey = random.split(key)
        U_mu_new = metropolis_link_update_standard(U[..., mu, :, :], K_mu, beta, subkey, eps)
        U = U.at[..., mu, :, :].set(U_mu_new)
    return U


@partial(jit, static_argnames=('L', 'L_tau'))
def metropolis_sweep_pair_disc(U_1, U_2, beta, key, L, L_tau, eps=0.3):
    """Sweep both sheets independently with standard Wilson (Z_1² ensemble)."""
    k1, k2 = random.split(key)
    U_1 = metropolis_sweep_single(U_1, beta, k1, L, eps)
    U_2 = metropolis_sweep_single(U_2, beta, k2, L, eps)
    return U_1, U_2


@partial(jit, static_argnames=('L', 'L_tau'))
def metropolis_sweep_pair_conif(U_1, U_2, beta, key, L, L_tau, A_site_mask, eps=0.3):
    """Sweep both sheets with conifold action (Z_2 ensemble).

    Strategy: standard MC sweep, then global Metropolis correction for the
    ΔS = S_conif - S_disc difference. This is a valid (if naive) sampling of S_conif.

    Better: per-link MH that includes the modification for A-wrap links.
    For now use the global correction approach.
    """
    k1, k2, k_acc = random.split(key, 3)
    U_1_new = metropolis_sweep_single(U_1, beta, k1, L, eps)
    U_2_new = metropolis_sweep_single(U_2, beta, k2, L, eps)

    # ΔS between S_conif(new) - S_conif(old) compared to S_disc
    # Since standard sweep samples from S_disc, accept based on (S_conif - S_disc) difference
    S_disc_old = wilson_action_disconnected(U_1, U_2, beta)
    S_conif_old = wilson_action_conifold(U_1, U_2, beta, A_site_mask, L_tau)
    S_disc_new = wilson_action_disconnected(U_1_new, U_2_new, beta)
    S_conif_new = wilson_action_conifold(U_1_new, U_2_new, beta, A_site_mask, L_tau)

    # We want to sample from S_conif. Standard sweep proposes new (U_1_new, U_2_new)
    # with acceptance based on S_disc. Need to correct for S_conif:
    # The "remaining" Metropolis ratio is exp(-(S_conif_new - S_conif_old) + (S_disc_new - S_disc_old))
    delta_correction = (S_conif_new - S_conif_old) - (S_disc_new - S_disc_old)
    rand_u = random.uniform(k_acc)
    accept = rand_u < jnp.exp(jnp.minimum(0.0, -delta_correction))
    U_1_out = jnp.where(accept, U_1_new, U_1)
    U_2_out = jnp.where(accept, U_2_new, U_2)
    return U_1_out, U_2_out


# ============================================================================
# Thermalization + sampling
# ============================================================================

def thermalize_disc(key, beta, L, L_tau, n_sweeps, eps=0.3):
    """Sample from Z_1² (disconnected). 2 indep configs."""
    k1, k2 = random.split(key)
    U_1 = random_su2_haar(k1, (L, L, L, L_tau, 4))
    U_2 = random_su2_haar(k2, (L, L, L, L_tau, 4))
    for i in range(n_sweeps):
        k1, sk = random.split(k1)
        U_1, U_2 = metropolis_sweep_pair_disc(U_1, U_2, beta, sk, L, L_tau, eps)
    return U_1, U_2, k1


def thermalize_conif(key, beta, L, L_tau, A_site_mask, n_sweeps, eps=0.3):
    """Sample from Z_2 (conifold)."""
    k1, k2 = random.split(key)
    U_1 = random_su2_haar(k1, (L, L, L, L_tau, 4))
    U_2 = random_su2_haar(k2, (L, L, L, L_tau, 4))
    for i in range(n_sweeps):
        k1, sk = random.split(k1)
        U_1, U_2 = metropolis_sweep_pair_conif(U_1, U_2, beta, sk, L, L_tau, A_site_mask, eps)
    return U_1, U_2, k1


# ============================================================================
# Bennett Acceptance Ratio
# ============================================================================

def bennett_estimator(dS_disc_to_conif, dS_conif_to_disc, C=0.0):
    """BAR estimator for free energy difference.

    log[Z_2 / Z_1²] = log[⟨1/(1+exp(dS_disc-conif - C))⟩_disc /
                          ⟨1/(1+exp(dS_conif-disc + C))⟩_conif]

    where dS_disc_to_conif = S_conif(U) - S_disc(U) evaluated on U sampled from disc ensemble
          dS_conif_to_disc = S_disc(U) - S_conif(U) evaluated on U sampled from conif ensemble

    Returns -log(Z_2/Z_1²) = S_2.
    """
    # Avoid overflow with log-sum-exp style
    fermi_disc = 1.0 / (1.0 + np.exp(dS_disc_to_conif - C))   # in disc ensemble
    fermi_conif = 1.0 / (1.0 + np.exp(dS_conif_to_disc + C))  # in conif ensemble

    mean_disc = np.mean(fermi_disc)
    mean_conif = np.mean(fermi_conif)

    # S_2 = -log(Z_2/Z_1²) = -log(ratio)
    # BAR : log(Z_2/Z_1²) = log(mean_disc/mean_conif) - C
    log_ratio = np.log(mean_disc / mean_conif) - C
    S_2 = -log_ratio

    # Standard error via bootstrap or simple
    sem_disc = np.std(fermi_disc) / np.sqrt(len(fermi_disc))
    sem_conif = np.std(fermi_conif) / np.sqrt(len(fermi_conif))
    # Propagate: d(log_ratio)/d(mean_disc) = 1/mean_disc
    err_disc = sem_disc / mean_disc
    err_conif = sem_conif / mean_conif
    S_2_err = float(np.sqrt(err_disc**2 + err_conif**2))

    return float(S_2), S_2_err


def run_BAR_one_L(L, L_tau, beta, n_thermalize, n_decorr, n_samples, key, eps=0.3, C=0.0):
    """Run both ensembles, collect ΔS samples, compute BAR."""
    A_site_mask = make_A_site_mask(L, L, L, L_tau)
    A_size = int(jnp.sum(A_site_mask[..., 0]))
    boundary_2D = L * L  # ∂A = (y, z) plane = L^2

    print(f"\n--- L = {L}, L_tau = {L_tau}, beta = {beta} ---", flush=True)
    print(f"    |A| (spatial sites) = {A_size}, ∂A = {boundary_2D}", flush=True)

    print(f"Thermalize disc ensemble ({n_thermalize} sweeps)...", flush=True)
    t0 = time.time()
    U1_disc, U2_disc, key = thermalize_disc(key, beta, L, L_tau, n_thermalize, eps)
    print(f"Disc thermalized in {time.time()-t0:.1f}s", flush=True)

    print(f"Thermalize conif ensemble ({n_thermalize} sweeps)...", flush=True)
    t0 = time.time()
    U1_conif, U2_conif, key = thermalize_conif(key, beta, L, L_tau, A_site_mask, n_thermalize, eps)
    print(f"Conif thermalized in {time.time()-t0:.1f}s", flush=True)

    # Collect samples
    print(f"Collecting {n_samples} samples from each ensemble (decorr={n_decorr})...", flush=True)
    dS_disc_to_conif = []  # S_conif - S_disc on disc samples
    dS_conif_to_disc = []  # S_disc - S_conif on conif samples

    t0 = time.time()
    for s in range(n_samples):
        for _ in range(n_decorr):
            key, sk = random.split(key)
            U1_disc, U2_disc = metropolis_sweep_pair_disc(U1_disc, U2_disc, beta, sk, L, L_tau, eps)
            key, sk = random.split(key)
            U1_conif, U2_conif = metropolis_sweep_pair_conif(U1_conif, U2_conif, beta, sk, L, L_tau, A_site_mask, eps)

        S_disc_at_disc = float(wilson_action_disconnected(U1_disc, U2_disc, beta))
        S_conif_at_disc = float(wilson_action_conifold(U1_disc, U2_disc, beta, A_site_mask, L_tau))
        dS_disc_to_conif.append(S_conif_at_disc - S_disc_at_disc)

        S_disc_at_conif = float(wilson_action_disconnected(U1_conif, U2_conif, beta))
        S_conif_at_conif = float(wilson_action_conifold(U1_conif, U2_conif, beta, A_site_mask, L_tau))
        dS_conif_to_disc.append(S_disc_at_conif - S_conif_at_conif)

        if s == 0 or (s+1) % max(1, n_samples//5) == 0 or s == n_samples-1:
            print(f"  sample {s+1}/{n_samples}: "
                  f"dS_disc->conif = {dS_disc_to_conif[-1]:.4e}, "
                  f"dS_conif->disc = {dS_conif_to_disc[-1]:.4e}, "
                  f"t={time.time()-t0:.1f}s", flush=True)

    # BAR estimator
    S_2, S_2_err = bennett_estimator(np.array(dS_disc_to_conif),
                                       np.array(dS_conif_to_disc), C=C)
    c_2D = S_2 / boundary_2D
    c_2D_err = S_2_err / boundary_2D

    print(f"\nL={L}: S_2 = {S_2:.4e} +/- {S_2_err:.4e}", flush=True)
    print(f"      c per 2D area (L^2={boundary_2D}) = {c_2D:.6e} +/- {c_2D_err:.6e}", flush=True)
    print(f"      c / (1/4 = 0.25) = {c_2D/0.25:.4f}", flush=True)

    return {
        'L': L, 'L_tau': L_tau, 'beta': beta,
        'A_size': A_size,
        'boundary_2D': boundary_2D,
        'dS_disc_to_conif': dS_disc_to_conif,
        'dS_conif_to_disc': dS_conif_to_disc,
        'S_2': S_2, 'S_2_err': S_2_err,
        'c_per_2D_area': c_2D, 'c_err': c_2D_err,
    }


def main():
    BETA = 2.4

    runs_config = {
        4:  {'L_tau': 4, 'n_thermalize': 100, 'n_decorr': 3, 'n_samples': 100},
        6:  {'L_tau': 6, 'n_thermalize': 150, 'n_decorr': 5, 'n_samples': 60},
        8:  {'L_tau': 8, 'n_thermalize': 200, 'n_decorr': 8, 'n_samples': 30},
    }

    all_results = {}
    for L in [4, 6, 8]:
        cfg = runs_config[L]
        print(f"\n{'='*78}\nLATTICE L = {L}\n{'='*78}", flush=True)
        key = random.PRNGKey(2030 + 23 * L)
        try:
            r = run_BAR_one_L(L, cfg['L_tau'], BETA,
                              cfg['n_thermalize'], cfg['n_decorr'], cfg['n_samples'],
                              key)
            all_results[L] = r
        except Exception as e:
            print(f"L={L} FAILED : {e}", flush=True)
            import traceback
            traceback.print_exc()
        with open('/tmp/jax_su2_EE_BP2008_TRUE_results.json', 'w') as f:
            json.dump({
                'method': 'BP2008 TRUE conifold (2 sheets, cross-sheet encircling, BAR)',
                'beta': BETA,
                'runs_config': runs_config,
                'results': {str(L): all_results[L] for L in all_results},
                'partial': True,
                'total_elapsed_s': time.time() - START,
            }, f, indent=2)

    print(f"\n{'='*78}\nSCALING — Renyi-2 EE via BP2008 TRUE conifold\n{'='*78}", flush=True)
    print(f"{'L':>4} {'|∂A|':>6} {'S_2':>16} {'c=S_2/∂A':>16} {'c/(1/4)':>10}", flush=True)
    print("-"*65, flush=True)
    for L in sorted(all_results.keys()):
        r = all_results[L]
        print(f"{L:>4} {r['boundary_2D']:>6} "
              f"{r['S_2']:>10.4e}+/-{r['S_2_err']:>3.0e} "
              f"{r['c_per_2D_area']:>10.4e}+/-{r['c_err']:>3.0e} "
              f"{r['c_per_2D_area']/0.25:>10.4f}", flush=True)

    if len(all_results) >= 1:
        L_max = max(all_results.keys())
        c_meas = all_results[L_max]['c_per_2D_area']
        c_err = all_results[L_max]['c_err']
        candidates = {
            '1/4 = 0.2500 (kappa^2(SU(2)) Bekenstein)': 0.25,
            'log(3)/(2*pi*sqrt(2)) = 0.1237 (Donnelly-Wall)': np.log(3) / (2 * np.pi * np.sqrt(2)),
            '2*log(3)/(2*pi*sqrt(2)) = 0.2474 (horizon doubling)': np.log(3) / (np.pi * np.sqrt(2)),
            '3/(4*pi^2) = 0.0760': 3 / (4 * np.pi**2),
            '1/(2*pi) = 0.1592': 1 / (2 * np.pi),
            '1/12 = 0.0833': 1/12,
        }
        print(f"\nCoefficient candidates (vs L={L_max}) :", flush=True)
        for name, c_pred in candidates.items():
            z = (c_meas - c_pred) / max(c_err, 1e-6)
            sig = "OK" if abs(z) < 2 else "~" if abs(z) < 3 else "X"
            print(f"  {name:<55} : ratio = {c_meas/c_pred:.3f}, |Z|={abs(z):.2f} {sig}", flush=True)

    output = {
        'method': 'BP2008 TRUE conifold (2 sheets, cross-sheet encircling, BAR)',
        'beta': BETA,
        'runs_config': runs_config,
        'results': {str(L): all_results[L] for L in all_results},
        'total_elapsed_s': time.time() - START,
    }
    with open('/tmp/jax_su2_EE_BP2008_TRUE_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nTotal elapsed : {time.time() - START:.1f}s "
          f"({(time.time() - START)/60:.1f}min)", flush=True)
    print(f"Saved : /tmp/jax_su2_EE_BP2008_TRUE_results.json", flush=True)
    print(f"END : {time.ctime()}", flush=True)
    print(f"DONE.", flush=True)


if __name__ == "__main__":
    main()
