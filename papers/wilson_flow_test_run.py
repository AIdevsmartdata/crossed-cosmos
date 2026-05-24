#!/usr/bin/env python3
"""End-to-end pipeline test : HMC thermalize -> Wilson flow -> smoothed plaquette.

Runs the full chain documented in the mission brief :
  1. Thermalize SU(3) HMC D=3 at a small beta (default 25) on a small L
     (default L=4) using su3_hmc_d3_jax.py.
  2. For each saved config, Wilson-flow it from t=0 to t=t_max (default 2.0)
     with the Luscher RK3 integrator from wilson_flow_su3_d3.py.
  3. Record E(t) trajectory (plaquette proxy) for each config.
  4. Compute the SMOOTHED plaquette  <P(t_ref)>  at a fixed reference flow
     time t_ref (default 1.0) for downstream alpha extraction.

Output : /tmp/voie1_calcs/wilson_flow_test_run.json

This script is the *integration* test that closes the loop with HMC. The
unit / sanity tests for the Wilson-flow integrator are in
`wilson_flow_su3_d3.py` (`if __name__ == '__main__'` block); the present
script verifies the two modules play well together and produces a
representative E(t) curve at a single beta as a starting point for the
overnight gamer-PC GPU run.

Author : K. Remondiere (ORCID 0009-0008-2443-7166)
Date   : 2026-05-24
"""
from __future__ import annotations

import os
os.environ.setdefault("JAX_PLATFORMS", "cpu")

import sys
import time
import json
import argparse

import numpy as np
import jax
import jax.numpy as jnp

# Make the HMC and flow modules importable.
sys.path.insert(0, "/tmp/voie1_calcs")
sys.path.insert(0, os.path.expanduser("/root/cc-private/papers"))

import wilson_flow_su3_d3 as wf
import su3_hmc_d3_jax as hmc_mod


def _flatten_configs(traj_list):
    """Convert list of jnp arrays to numpy stacks (saving)."""
    return [np.array(U) for U in traj_list]


def run_one_beta(beta, L, n_therm, n_meas, n_md, eps_hmc,
                 t_max, eps_flow, t_ref, seed, verbose=True):
    """Thermalize HMC + Wilson-flow each measurement config."""
    print(f"\n{'='*78}")
    print(f"PIPELINE  beta={beta}  L={L}  n_therm={n_therm}  n_meas={n_meas}")
    print(f"          t_max={t_max}  eps_flow={eps_flow}  t_ref={t_ref}")
    print(f"{'='*78}\n", flush=True)

    V = L ** 3
    nbr_hmc = hmc_mod.build_neighbors_3D(L)
    nbr_flow = wf.build_neighbors_3D(L)

    # ---------- HMC thermalize ----------
    key = jax.random.PRNGKey(seed)
    keys = jax.random.split(key, 3)
    U = hmc_mod.random_su3(keys[0], (3 * V,))
    key = keys[1]

    hmc_step, _, S_fn = hmc_mod.make_hmc_step(L, beta, nbr_hmc, n_md, eps_hmc)
    plaq_fn = hmc_mod.make_compute_plaquette_avg(L, nbr_hmc)

    P_init = float(plaq_fn(U))
    print(f"  [HMC] init <P>={P_init:.4f} (hot)", flush=True)

    t0 = time.time()
    n_acc = 0
    for step in range(n_therm):
        U, key, dH, accept = hmc_step(U, key)
        n_acc += int(accept)
        if verbose and (step + 1) % max(1, n_therm // 5) == 0:
            cur_P = float(plaq_fn(U))
            print(f"  [HMC] therm {step+1}/{n_therm} <P>={cur_P:.4f} "
                  f"acc={n_acc/(step+1):.2f} t={time.time()-t0:.0f}s",
                  flush=True)
    therm_acc = n_acc / n_therm
    print(f"  [HMC] thermalized in {time.time()-t0:.0f}s, acc={therm_acc:.2f}",
          flush=True)

    # ---------- Wilson flow measurements ----------
    flow_step_fn = wf.make_wilson_flow_step(L, nbr_flow)
    E_plaq_fn = wf.make_energy_density_plaquette_3D(L, nbr_flow)
    E_clover_fn = wf.make_clover_energy_density_3D(L, nbr_flow)

    # Precompute flow time grid
    n_flow_steps = int(round(t_max / eps_flow))
    t_arr_master = np.arange(n_flow_steps + 1) * eps_flow

    E_plaq_all = []
    E_clover_all = []
    t2E_plaq_all = []
    t2E_clover_all = []
    P_at_tref = []

    # We record E every step (cheap)
    n_acc_meas = 0
    t_meas = time.time()
    for cfg in range(n_meas):
        # 2 HMC sweeps between measurements (decorrelation)
        for _ in range(2):
            U, key, dH, accept = hmc_step(U, key)
            n_acc_meas += int(accept)

        # Flow this config
        U_flow = U
        E_plaq_curve = [float(E_plaq_fn(U_flow))]
        E_clover_curve = [float(E_clover_fn(U_flow))]
        idx_tref = None
        for step in range(1, n_flow_steps + 1):
            U_flow = flow_step_fn(U_flow, eps_flow)
            E_plaq_curve.append(float(E_plaq_fn(U_flow)))
            E_clover_curve.append(float(E_clover_fn(U_flow)))
            if idx_tref is None and (step * eps_flow >= t_ref):
                idx_tref = step
                # smoothed plaquette
                sites = jnp.arange(V)
                total = jnp.zeros((), dtype=jnp.float32)
                npairs = 0
                for mu in range(3):
                    for nu in range(mu + 1, 3):
                        x_mu = nbr_flow[mu, 0, sites]
                        x_nu = nbr_flow[nu, 0, sites]
                        P = wf.sun_mul(U_flow[mu * V + sites],
                                       U_flow[nu * V + x_mu])
                        P = wf.sun_mul(P, wf.sun_dagger(U_flow[mu * V + x_nu]))
                        P = wf.sun_mul(P, wf.sun_dagger(U_flow[nu * V + sites]))
                        tr = (P[..., 0, 0] + P[..., 1, 1] + P[..., 2, 2]).real
                        total = total + jnp.sum(tr / 3.0)
                        npairs += V
                P_tref = float(total / npairs)
                P_at_tref.append(P_tref)

        E_plaq_curve = np.array(E_plaq_curve)
        E_clover_curve = np.array(E_clover_curve)
        E_plaq_all.append(E_plaq_curve)
        E_clover_all.append(E_clover_curve)
        t2E_plaq_all.append((t_arr_master ** 2) * E_plaq_curve)
        t2E_clover_all.append((t_arr_master ** 2) * E_clover_curve)

        if verbose:
            print(f"  [flow] config {cfg+1:3d}/{n_meas}  "
                  f"E_plaq(0)={E_plaq_curve[0]:.3f}  "
                  f"E_plaq({t_max})={E_plaq_curve[-1]:.3f}  "
                  f"P(t_ref={t_ref})={P_at_tref[-1]:.4f}  "
                  f"t={time.time()-t_meas:.0f}s",
                  flush=True)

    meas_acc = n_acc_meas / (n_meas * 2)
    print(f"\n  [meas] meas_acc={meas_acc:.2f}, "
          f"total t={time.time()-t_meas:.0f}s", flush=True)

    # Mean trajectories
    E_plaq_mean = np.mean(np.stack(E_plaq_all), axis=0)
    E_plaq_err = np.std(np.stack(E_plaq_all), axis=0) / np.sqrt(max(1, n_meas))
    E_clover_mean = np.mean(np.stack(E_clover_all), axis=0)
    E_clover_err = np.std(np.stack(E_clover_all), axis=0) / np.sqrt(max(1, n_meas))
    t2E_plaq_mean = np.mean(np.stack(t2E_plaq_all), axis=0)
    t2E_clover_mean = np.mean(np.stack(t2E_clover_all), axis=0)

    return {
        "beta": float(beta), "L": int(L),
        "n_therm": int(n_therm), "n_meas": int(n_meas),
        "therm_acc": float(therm_acc), "meas_acc": float(meas_acc),
        "t_arr": t_arr_master.tolist(),
        "E_plaq_mean": E_plaq_mean.tolist(),
        "E_plaq_err": E_plaq_err.tolist(),
        "E_clover_mean": E_clover_mean.tolist(),
        "E_clover_err": E_clover_err.tolist(),
        "t2E_plaq_mean": t2E_plaq_mean.tolist(),
        "t2E_clover_mean": t2E_clover_mean.tolist(),
        "t_ref": float(t_ref),
        "P_at_tref_per_config": P_at_tref,
        "P_at_tref_mean": float(np.mean(P_at_tref)),
        "P_at_tref_err": float(np.std(P_at_tref) / np.sqrt(max(1, len(P_at_tref)))),
        "eps_flow": float(eps_flow),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--beta", type=float, default=25.0,
                   help="Wilson beta for HMC thermalization")
    p.add_argument("--L", type=int, default=4)
    p.add_argument("--n_therm", type=int, default=100,
                   help="HMC thermalization sweeps")
    p.add_argument("--n_meas", type=int, default=5,
                   help="Number of Wilson-flow measurement configs")
    p.add_argument("--n_md", type=int, default=15,
                   help="HMC leapfrog substeps")
    p.add_argument("--eps_hmc", type=float, default=None,
                   help="HMC step (auto from beta if None)")
    p.add_argument("--t_max", type=float, default=2.0,
                   help="Final Wilson flow time")
    p.add_argument("--eps_flow", type=float, default=0.02,
                   help="Wilson flow RK3 step")
    p.add_argument("--t_ref", type=float, default=1.0,
                   help="Reference flow time for smoothed <P>")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", type=str,
                   default="/tmp/voie1_calcs/wilson_flow_test_run.json")
    args = p.parse_args()

    eps_hmc = args.eps_hmc if args.eps_hmc is not None \
        else float(0.15 / np.sqrt(1.0 + args.beta / 10.0))

    print("=" * 78)
    print("Wilson flow test run -- SU(3) D=3, HMC + Luscher flow pipeline")
    print(f"  beta={args.beta}  L={args.L}  eps_hmc={eps_hmc:.4f}")
    print(f"  eps_flow={args.eps_flow}  t_max={args.t_max}  t_ref={args.t_ref}")
    print(f"  n_therm={args.n_therm}  n_meas={args.n_meas}  n_md={args.n_md}")
    print("=" * 78)

    t0 = time.time()
    result = run_one_beta(
        beta=args.beta, L=args.L,
        n_therm=args.n_therm, n_meas=args.n_meas,
        n_md=args.n_md, eps_hmc=eps_hmc,
        t_max=args.t_max, eps_flow=args.eps_flow, t_ref=args.t_ref,
        seed=args.seed, verbose=True,
    )
    result["wall_time_sec"] = float(time.time() - t0)

    # Summary
    t_arr = np.array(result["t_arr"])
    E_pl = np.array(result["E_plaq_mean"])
    E_cl = np.array(result["E_clover_mean"])
    t2E_pl = np.array(result["t2E_plaq_mean"])
    t2E_cl = np.array(result["t2E_clover_mean"])

    print("\n" + "=" * 78)
    print("SUMMARY  (mean over configs)")
    print("=" * 78)
    print(f"  {'t':>6}  {'E_plaq':>10}  {'E_clover':>10}  {'t^2 E_pl':>10}  {'t^2 E_cl':>10}")
    sample_idx = [0, len(t_arr)//8, len(t_arr)//4, len(t_arr)//2,
                  3*len(t_arr)//4, len(t_arr)-1]
    for i in sample_idx:
        print(f"  {t_arr[i]:>6.3f}  {E_pl[i]:>10.4e}  {E_cl[i]:>10.4e}  "
              f"{t2E_pl[i]:>10.4e}  {t2E_cl[i]:>10.4e}")

    print(f"\n  <P(t_ref={result['t_ref']})> = "
          f"{result['P_at_tref_mean']:.4f} +/- {result['P_at_tref_err']:.4f}")
    print(f"  (averaged over {len(result['P_at_tref_per_config'])} configs)")
    print(f"\n  wall time = {result['wall_time_sec']:.0f} s")

    # Save
    with open(args.out, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved -> {args.out}")


if __name__ == "__main__":
    main()
