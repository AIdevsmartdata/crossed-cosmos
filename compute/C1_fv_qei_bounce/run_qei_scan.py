#!/usr/bin/env python3
"""Driver: scan FV-QEI violations across bounce models and smearing-time grids.

Usage:
    python run_qei_scan.py --bounce loop_quantum  --grid 128 --output results/lqc.h5
    python run_qei_scan.py --bounce pre_big_bang  --grid 128 --output results/pbb.h5
    python run_qei_scan.py --bounce matter_bounce --grid 128 --output results/mb.h5
"""
from __future__ import annotations
import argparse
from pathlib import Path

import h5py
import jax.numpy as jnp

from bounce_models import get_model
from qei_kernel import violation_scan


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bounce", required=True,
                    choices=["loop_quantum", "pre_big_bang", "matter_bounce"])
    ap.add_argument("--grid", type=int, default=128, help="number of τ values")
    ap.add_argument("--tau-min", type=float, default=1e-2)
    ap.add_argument("--tau-max", type=float, default=1.0)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    a_fn = get_model(args.bounce)
    tau_grid = jnp.geomspace(args.tau_min, args.tau_max, args.grid)
    out = violation_scan(a_fn, tau_grid)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with h5py.File(args.output, "w") as f:
        for k, v in out.items():
            f.create_dataset(k, data=jnp.asarray(v))
        f.attrs["bounce"] = args.bounce
        f.attrs["grid"] = args.grid

    n_violated = int(jnp.sum(out["is_violated"]))
    print(f"[{args.bounce}] τ-grid={args.grid}, violated at {n_violated}/{args.grid} τ values")
    if n_violated > 0:
        idx = int(jnp.argmin(out["violation"]))
        print(f"  worst violation: τ={out['tau'][idx]:.4e}, "
              f"E={out['E_smeared'][idx]:.4e}, bound={out['fv_bound'][idx]:.4e}")


if __name__ == "__main__":
    main()
