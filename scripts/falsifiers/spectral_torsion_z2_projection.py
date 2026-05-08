#!/usr/bin/env python3
"""Compute Z_2-projection of Dąbrowski-Mukhopadhyay-Požar torsion functional at τ=i.

Check if |proj| < 1% threshold. Output proj norm + PASS/FAIL.
"""
import sys
import json
import logging
import time
from pathlib import Path

import sympy as sp
import mpmath as mp
import numpy as np
from joblib import Parallel, delayed
from diskcache import Cache
from tqdm import tqdm

CACHE_DIR = Path.home() / '.cache' / 'spectral_torsion_z2'
cache = Cache(str(CACHE_DIR))

# ----- constants -----
TAU_I = sp.I
THRESHOLD = 0.01   # 1 %

def compute_projection(dps=200):
    """Return the norm of the Z_2-projection."""
    mp.mp.dps = dps
    # CITE_NEEDED::Dąbrowski-Mukhopadhyay-Požar torsion functional explicit formula
    raise NotImplementedError(
        "NEEDS LOOKUP from project source: torsion functional at τ=i"
    )
    # return proj_norm

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger(__name__)
    start = time.monotonic()

    result = {
        "test": "spectral_torsion_z2_projection",
        "status": "FAIL",
        "reason": "",
        "details": {}
    }

    try:
        cache_key = "proj_norm"
        proj_norm = cache.get(cache_key)
        if proj_norm is None:
            with tqdm(total=1, desc="Projection norm") as pbar:
                proj_norm = compute_projection(dps=200)
                pbar.update(1)
            cache.set(cache_key, proj_norm, expire=3600 * 24)

        result["details"]["proj_norm"] = round(proj_norm, 12)
        if abs(proj_norm) < THRESHOLD:
            result["status"] = "PASS"
            result["reason"] = "|proj| < 1% threshold, M177.1 protected"
        else:
            result["reason"] = f"|proj| = {proj_norm:.6f} >= 1% threshold, M177.1 threatened"
    except NotImplementedError as e:
        result["status"] = "NOT_IMPLEMENTED"
        result["reason"] = str(e)
    except Exception as e:
        logger.exception("Computation failed")
        result["status"] = "ERROR"
        result["reason"] = str(e)

    elapsed = time.monotonic() - start
    result["elapsed_seconds"] = round(elapsed, 2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
