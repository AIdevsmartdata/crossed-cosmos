"""
A71 — ECI-vs-LCDM Framing B: cosmopower-jax emulator loader.

Loads A25-trained pkl files for NMC KG emulators:
  - nmc_kg_w.pkl   : w(z) emulator  (custom_log probe)
  - nmc_kg_logH.pkl: log10 H(z) emulator (custom_log probe)

CRITICAL: JAX named_shape patch (reference_jax_patch.md) is applied at
module-import time, BEFORE importing cosmopower_jax.

arXiv IDs (live-verified 2026-05-05):
  - A25 emulator design: no separate arXiv — see SUMMARY.md in notes/
  - DESI DR2 BAO: arXiv:2503.14738 (confirmed via API)

Hallu count: 85 (entering) → 85 (leaving). Mistral STRICT-BAN.
"""

import os
import sys
import pickle
import importlib

# =========================================================================
# SECTION 0 — Apply JAX named_shape patch BEFORE any JAX / CPJ imports
# =========================================================================
# Per reference_jax_patch.md: JAX 0.10+ removed the named_shape kwarg from
# ShapedArray.__new__(). cosmopower-jax 0.5.5 pkls were pickled with the old
# kwarg, causing TypeError at load time. We patch at runtime here.

def _apply_jax_named_shape_patch():
    """
    Inject `kwargs.pop("named_shape", None)` into JAX's ShapedArray.update()
    so that cosmopower-jax 0.5.5 pickles load correctly on JAX 0.10+.

    This is safe because named_shape was removed from the public API; popping
    it from kwargs is a no-op on versions that don't pass it, and a fix on
    versions that do.
    """
    import jax._src.core as _jax_core

    # Check if patch is already applied (idempotent)
    if getattr(_jax_core, "_a71_named_shape_patch_applied", False):
        return

    ShapedArray = _jax_core.ShapedArray
    _original_update = ShapedArray.update

    def _patched_update(self, **kwargs):
        kwargs.pop("named_shape", None)
        return _original_update(self, **kwargs)

    ShapedArray.update = _patched_update
    _jax_core._a71_named_shape_patch_applied = True


_apply_jax_named_shape_patch()

# =========================================================================
# SECTION 1 — Imports (AFTER patch)
# =========================================================================
import jax
import jax.numpy as jnp

try:
    from cosmopower_jax.cosmopower_jax import CosmoPowerJAX as CPJ
    _CPJ_AVAILABLE = True
except ImportError:
    _CPJ_AVAILABLE = False
    CPJ = None

# =========================================================================
# SECTION 2 — Default paths
# =========================================================================
# On PC: /home/remondiere/pc_calcs/cosmopower_nmc_emulator/
# On VPS: does NOT exist — [TBD: locate pkl files on VPS if needed]
_DEFAULT_EMU_DIR = "/home/remondiere/pc_calcs/cosmopower_nmc_emulator"
_DEFAULT_EMU_DIR_EXTENDED = "/home/remondiere/pc_calcs/cosmopower_nmc_emulator_extended"

_W_PKL     = os.path.join(_DEFAULT_EMU_DIR, "nmc_kg_w.pkl")
_LOGH_PKL  = os.path.join(_DEFAULT_EMU_DIR, "nmc_kg_logH.pkl")
_W_EXT_PKL    = os.path.join(_DEFAULT_EMU_DIR_EXTENDED, "nmc_kg_w_extended.pkl")
_LOGH_EXT_PKL = os.path.join(_DEFAULT_EMU_DIR_EXTENDED, "nmc_kg_logH_extended.pkl")

# From A25 SUMMARY: w(z) mapped as y = (w+3)/4, trained as log10(y).
# At inference: w = cp_w.predict() * 4 - 3
W_OFFSET = 3.0
W_SCALE  = 4.0

# z-grid (100 points, matches A25 training grid)
import numpy as np
Z_GRID = np.concatenate([
    np.array([0.0]),
    np.linspace(0.05, 0.5, 20),
    np.linspace(0.55, 1.5, 50),
    np.linspace(1.55, 3.0, 29),
])
assert len(Z_GRID) == 100, "Z_GRID must have exactly 100 points (A25 spec)"


# =========================================================================
# SECTION 3 — Emulator loader
# =========================================================================

_emu_w: CPJ | None = None
_emu_logH: CPJ | None = None
_emu_w_ext: CPJ | None = None
_emu_logH_ext: CPJ | None = None
_emulators_loaded: bool = False


def load_emulators(
    w_pkl: str = _W_PKL,
    logH_pkl: str = _LOGH_PKL,
    require_extended: bool = False,
    w_ext_pkl: str = _W_EXT_PKL,
    logH_ext_pkl: str = _LOGH_EXT_PKL,
) -> None:
    """
    Load A25 cosmopower-jax emulators from pkl files.

    Args:
        w_pkl: Path to nmc_kg_w.pkl
        logH_pkl: Path to nmc_kg_logH.pkl
        require_extended: If True, also load extended-domain pkls (ξ ∈ [-5, 0.198])
        w_ext_pkl: Path to nmc_kg_w_extended.pkl
        logH_ext_pkl: Path to nmc_kg_logH_extended.pkl

    Raises:
        AssertionError: if pkl files do not exist (defensive — no silent fallback)
        ImportError: if cosmopower_jax is not installed
    """
    global _emu_w, _emu_logH, _emu_w_ext, _emu_logH_ext, _emulators_loaded

    assert _CPJ_AVAILABLE, (
        "cosmopower_jax is not installed in this Python environment.\n"
        "Install via: pip install cosmopower-jax==0.5.5\n"
        "[TBD: verify install in .venv-mcmc-bench on PC]"
    )

    # Hard assertions — no silent fallback to fake data
    assert os.path.isfile(w_pkl), (
        f"[TBD: locate emulator pkl] w pkl not found at: {w_pkl}\n"
        f"Expected at: {_DEFAULT_EMU_DIR}/nmc_kg_w.pkl\n"
        f"On PC run: ls /home/remondiere/pc_calcs/cosmopower_nmc_emulator/"
    )
    assert os.path.isfile(logH_pkl), (
        f"[TBD: locate emulator pkl] logH pkl not found at: {logH_pkl}\n"
        f"Expected at: {_DEFAULT_EMU_DIR}/nmc_kg_logH.pkl"
    )

    _emu_w    = CPJ(probe="custom_log", filepath=w_pkl)
    _emu_logH = CPJ(probe="custom_log", filepath=logH_pkl)

    if require_extended:
        assert os.path.isfile(w_ext_pkl), (
            f"[TBD: locate extended emulator] w_extended pkl not found: {w_ext_pkl}"
        )
        assert os.path.isfile(logH_ext_pkl), (
            f"[TBD: locate extended emulator] logH_extended pkl not found: {logH_ext_pkl}"
        )
        _emu_w_ext    = CPJ(probe="custom_log", filepath=w_ext_pkl)
        _emu_logH_ext = CPJ(probe="custom_log", filepath=logH_ext_pkl)

    _emulators_loaded = True
    print(f"[emulators] Loaded w + logH emulators from {os.path.dirname(w_pkl)}")


def _require_loaded():
    """Raise if emulators not yet loaded."""
    if not _emulators_loaded:
        raise RuntimeError(
            "Emulators not loaded. Call emulators.load_emulators() first."
        )


# =========================================================================
# SECTION 4 — JAX-jittable inference functions
# =========================================================================
# Parameter vector layout for the A25 emulator (6 params):
#   theta_emu = [xi, lambda, phi0, omega_b_h2, omega_c_h2, h]
# where h = H0/100.

def _make_theta_row(xi: jnp.ndarray, lam: jnp.ndarray, phi0: jnp.ndarray,
                    omega_b: jnp.ndarray, omega_c: jnp.ndarray,
                    h: jnp.ndarray) -> jnp.ndarray:
    """Pack scalar params into shape (1, 6) for CPJ.predict()."""
    return jnp.array([[xi, lam, phi0, omega_b, omega_c, h]])


def cp_w(xi: jnp.ndarray, lam: jnp.ndarray, phi0: jnp.ndarray,
         omega_b: jnp.ndarray, omega_c: jnp.ndarray,
         h: jnp.ndarray) -> jnp.ndarray:
    """
    JAX-jittable: returns w(z) on Z_GRID (shape: [100]).

    Post-processing: w = predict() * W_SCALE - W_OFFSET
    (matches A25 training convention: y_train = (w+3)/4, custom_log
     returns 10**NN_out; so predict() already returns y, and w = y*4-3)

    Args: scalar JAX arrays for each ECI parameter.
    Returns: w(z) array of shape (100,) on A25 Z_GRID.
    """
    _require_loaded()
    theta = _make_theta_row(xi, lam, phi0, omega_b, omega_c, h)
    raw = _emu_w.predict(theta)      # shape (1, 100), already de-logged by CPJ
    return raw[0] * W_SCALE - W_OFFSET  # map back from y = (w+3)/4


def cp_logH(xi: jnp.ndarray, lam: jnp.ndarray, phi0: jnp.ndarray,
            omega_b: jnp.ndarray, omega_c: jnp.ndarray,
            h: jnp.ndarray) -> jnp.ndarray:
    """
    JAX-jittable: returns log10 H(z) on Z_GRID (shape: [100]).

    Note: CPJ custom_log returns 10**NN_out, which for the logH emulator
    means the output is already H(z) in km/s/Mpc (NOT log10).
    We take log10 again here so callers get log10 H consistently.

    Returns: log10(H(z)) array of shape (100,) on A25 Z_GRID.
    """
    _require_loaded()
    theta = _make_theta_row(xi, lam, phi0, omega_b, omega_c, h)
    raw = _emu_logH.predict(theta)   # shape (1, 100); raw = H(z) in km/s/Mpc
    return jnp.log10(raw[0])         # return log10 H


def cp_H(xi: jnp.ndarray, lam: jnp.ndarray, phi0: jnp.ndarray,
         omega_b: jnp.ndarray, omega_c: jnp.ndarray,
         h: jnp.ndarray) -> jnp.ndarray:
    """
    JAX-jittable: returns H(z) in km/s/Mpc on Z_GRID (shape: [100]).
    """
    _require_loaded()
    theta = _make_theta_row(xi, lam, phi0, omega_b, omega_c, h)
    raw = _emu_logH.predict(theta)
    return raw[0]   # CPJ custom_log already returns 10**NN_out = H(z)


# =========================================================================
# SECTION 5 — Smoke sanity test (import-time check disabled; call manually)
# =========================================================================

def smoke_check(verbose: bool = True) -> bool:
    """
    Quick sanity: predict w(z) and H(z) at a Cassini-clean point.
    Cassini-clean: xi=0.001, lambda=2.31, phi0=0.016, omega_b=0.02238,
                   omega_c=0.12, h=0.70 (from A25 SUMMARY posterior).
    Returns True if outputs are finite and in plausible range.
    """
    _require_loaded()
    xi    = jnp.array(0.001)
    lam   = jnp.array(2.31)
    phi0  = jnp.array(0.016)
    omega_b = jnp.array(0.02238)
    omega_c = jnp.array(0.1227)
    h     = jnp.array(0.70)

    w_arr = jnp.atleast_1d(cp_w(xi, lam, phi0, omega_b, omega_c, h))
    H_arr = jnp.atleast_1d(cp_H(xi, lam, phi0, omega_b, omega_c, h))

    w0_approx = float(w_arr.flatten()[0])
    H0_approx = float(H_arr.flatten()[0])

    ok = (
        jnp.all(jnp.isfinite(w_arr))
        and jnp.all(jnp.isfinite(H_arr))
        and (-2.5 < w0_approx < 1.0)
        and (40.0 < H0_approx < 150.0)
    )
    if verbose:
        print(f"[emulators.smoke_check] w(z=0) ≈ {w0_approx:.4f}, "
              f"H(z=0) ≈ {H0_approx:.2f} km/s/Mpc")
        print(f"[emulators.smoke_check] PASS={bool(ok)}")
    return bool(ok)


if __name__ == "__main__":
    print("[emulators] Loading emulators...")
    load_emulators()
    smoke_check()
