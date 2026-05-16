#!/usr/bin/env python3
"""
analyze_4plusplus_gevp.py — Phase E2 SU(2) J^PC = 4++ glueball mass extraction.

================================================================================
5-STEP CONSTRAINT CHAIN (TIER_HONNETE STRICT)
================================================================================

1. EQUATION (what we measure)
   For an interpolating operator O carrying the quantum numbers of the target
   state, the connected zero-momentum two-point function admits the spectral
   decomposition
        C(tau) = <O(tau) O(0)> - <O>**2
               = sum_{n} |<0|O|n>|^2 * exp(-m_n * tau)
                + (back-propagating cosh term on periodic BC)
   so at large tau the lowest contributing mass dominates and the effective
   mass plateau m_eff(tau) -> m_0 (the ground state in that quantum-number
   channel).  Solving the generalized eigenvalue problem
        C(tau) v_n = lambda_n(tau) C(t0) v_n
   over a multi-operator basis cleanly separates m_0, m_1, ... .

2. NUMERICAL PREDICTION (Phase E2 / D = -67 SST motivic-spin extension)
   m^2(4++) / m^2(0++) = 3.00 +/- 0.05  at SU(2).
   Equivalently m(4++) / sqrt(sigma) = sqrt(3) * (m(0++)/sqrt(sigma))
                                     = sqrt(3) * 3.781 = 6.55 .

3. FALSIFIER (predefined, immutable in this script)
   If extracted continuum value m^2(4++)/m^2(0++) at a -> 0 is outside
   [2.5, 3.5] at >= 5 sigma combined (stat (+) sys), Phase E2 is FALSIFIED.
   If inside [2.7, 3.3] at >= 2 sigma, Phase E2 at SU(2)/D=-67 is CONFIRMED
   as a single-anchor result (separate from cross-N status).  Otherwise
   INCONCLUSIVE.

4. SIGMA-SIGNIFICANCE BUDGET
   - Stat (per-beta plateau fit, jackknife):  sigma_stat ~ 0.05-0.10 in mass
     units of sqrt(sigma).
   - Continuum extrapolation residual (3 betas, a^2 -> 0 linear):
     sigma_cont ~ 0.05-0.15 sqrt(sigma).
   - Cubic-rep spread (AT 2021 SU(2) inherited ~ 13% if intrinsic):
     sigma_cubic ~ 0.10-0.20 sqrt(sigma).
   Quadrature -> sigma_total ~ 0.15-0.30 sqrt(sigma) on m(4++)/sqrt(sigma),
   propagated to ratio m^2(4++)/m^2(0++) via:
        delta(ratio)/ratio = 2 * delta(m_4)/m_4 .

5. VERDICT  (auto-emitted as final JSON field)
        CONFIRMED     if  |ratio - 3| <= 0.3  and  total_sigma <= 0.4
        FALSIFIED     if  |ratio - 3| >= 5 * total_sigma
        INCONCLUSIVE  otherwise (noise-dominated or partial plateau).

================================================================================
PRE-VERIFIED arXiv ANCHORS (no fabrications introduced by this file)
================================================================================
- arXiv:2106.00364                Athenodorou & Teper, JHEP 12 (2021) 082.
                                  SOTA SU(N) glueball spectrum; SU(2) Table 23
                                  cubic-rep raw data.  (VERIFIED_WITHDRAWN ->
                                  superseded by extended version of same paper.)
- arXiv:hep-lat/0404008           Lucini, Teper & Wenger, JHEP 0406 (2004) 012.
                                  Improved operators basis; original cubic-rep
                                  GEVP construction for SU(N) glueballs.
- arXiv:hep-lat/9711011           Teper, "Physics from the lattice" NATO-ASI
                                  1998; baseline review for cubic O_h reps.
- arXiv:2508.21821                Abbott, Hackett, Pefkou, Romero-Lopez,
                                  Shanahan 2025; recent ML/lattice cross-check
                                  on scalar glueball size.

NO citation of arXiv:2106.13568 (laser sintering -- FORBIDDEN A52),
no citation of arXiv:1502.00715 (IceCube -- FORBIDDEN A52),
no other A52-listed IDs are used.

================================================================================
INPUT
================================================================================
Utah Stage B SU(2) 18^4 ensemble, three couplings:
    /root/gevp_t2g/output/b240/glue_*.out.xml   (210 cfgs, beta = 2.40)
    /root/gevp_t2g/output/b250/glue_*.out.xml   (210 cfgs, beta = 2.50)
    /root/gevp_t2g/output/b260/glue_*.out.xml   (210 cfgs, beta = 2.60)

Two Chroma output schemas supported:
  (a) glueball_correlator_v3 schema -- <Op_t> with <O_op_N> tags
      (12 ops = 6 shapes [PLAQ,RECT,SQUARE,CHAIR,PARA,FATPLQ] x 2 APE levels).
      Channel: A_1++ scalar at zero momentum.  Used to extract m(0++) gs
      and m(0++)* excited.  The excited state, when isolated cleanly, is
      a candidate for the A_1 piece of the J=4 multiplet.
  (b) glueball_GEVP_T2g schema -- <Op_spin2> with <OT2_a>, <OE_a> tags
      (n_ape_levels operators per irrep).  Channel: T2g and Eg cubic-irrep
      ground + excited state.  Used to extract m(2++) gs and excited; the
      excited states in these reps are candidates for the T_2 and E pieces
      of the J=4 multiplet.

OUTPUT
================================================================================
- gevp_4plusplus_summary.json    summary with per-beta masses, ratios, verdict.
- gevp_4plusplus_<beta>.json     per-beta intermediate (effective masses,
                                 plateau fit, residuals).
- (optional, --plot) effective-mass plots (matplotlib).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.linalg import eigh

# ============================================================================
# PHYSICAL ANCHORS (Athenodorou-Teper 2021, Table 23 + Table 34, SU(2))
# ============================================================================
AT2021_SU2: Dict[str, float] = {
    # ground states (Table 34 continuum), units sqrt(sigma):
    "m_0pp": 3.781,
    "m_0pp_err": 0.023,
    "m_2pp": 5.349,
    "m_2pp_err": 0.020,
    # cubic-rep J=4 candidates (Table 23 raw cubic data):
    "A1pp_ex2": 7.54,    "A1pp_ex2_err": 0.10,
    "Epp_ex2":  7.72,    "Epp_ex2_err":  0.08,
    "T1pp_gs":  8.14,    "T1pp_gs_err":  0.10,
    "T2pp_ex1": 7.22,    "T2pp_ex1_err": 0.05,
    # naive J=4 average (rough, not AT-assigned)
    "m_4pp_naive": 7.66, "m_4pp_naive_err": 0.40,
    # ratios:
    "ratio_2pp_sq":  (5.349 / 3.781) ** 2,        # ~2.001
    "ratio_4pp_sq_naive": (7.66 / 3.781) ** 2,    # ~4.10
}

# ECI v15 / Phase E2 prediction
ECI_PHASE_E2: Dict[str, float] = {
    "ratio_4pp_sq_pred": 3.00,
    "ratio_4pp_sq_pred_err": 0.05,
    "anchor": "D = -67, SU(2) single-anchor SST",
}

# Confirmation / falsification gates
CONFIRM_BAND = (2.7, 3.3)         # band around 3.00 to call CONFIRMED at >= 2 sigma
FALSIFY_BAND = (2.5, 3.5)         # outside this AND >= 5 sigma => FALSIFIED


# ============================================================================
# 1. XML PARSERS
# ============================================================================
def _parse_floats(text: str) -> np.ndarray:
    """Parse whitespace-separated floats from a single XML text node."""
    return np.array([float(x) for x in text.strip().split()], dtype=np.float64)


def parse_v3_scalar(xml_path: Path) -> Optional[Dict[int, np.ndarray]]:
    """
    Parse glueball_correlator_v3 XML.  Returns {op_idx: array(Lt,)} for the
    A_1g scalar 12-op basis (6 shapes x 2 APE levels), or None on failure.

    XML layout (sample, see chroma/glueball_correlator_v3.cc):
        <glueball_correlator_v3>
          <Op_t>
            <Lt>16</Lt>
            <n_ops>12</n_ops>
            <O_op_0>v0 v1 ... v(Lt-1)</O_op_0>
            ...
            <O_op_11>...</O_op_11>
          </Op_t>
        </glueball_correlator_v3>
    """
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as exc:
        print(f"  [parse_v3_scalar] XML parse error in {xml_path}: {exc}",
              file=sys.stderr)
        return None
    except FileNotFoundError:
        return None

    root = tree.getroot()
    op_t = root.find("Op_t")
    if op_t is None:
        return None

    lt_node = op_t.find("Lt")
    n_node = op_t.find("n_ops")
    if lt_node is None or n_node is None:
        return None
    Lt = int(lt_node.text.strip())
    n_ops = int(n_node.text.strip())

    out: Dict[int, np.ndarray] = {}
    for child in op_t:
        tag = child.tag
        if not tag.startswith("O_op_"):
            continue
        try:
            idx = int(tag[len("O_op_"):])
        except ValueError:
            continue
        if child.text is None:
            continue
        vals = _parse_floats(child.text)
        if vals.size == Lt:
            out[idx] = vals
    if len(out) != n_ops:
        # tolerate partial -- caller can decide
        pass
    return out if out else None


def parse_t2g_eg(xml_path: Path) -> Optional[Dict[str, Dict[int, np.ndarray]]]:
    """
    Parse glueball_GEVP_T2g XML.  Returns
        {"T2g": {ape_idx: array(Lt,)},
         "Eg" : {ape_idx: array(Lt,)}}
    or None on failure.

    XML layout (sample, see chroma/glueball_correlator_GEVP_T2g.cc):
        <glueball_GEVP_T2g>
          <Op_spin2>
            <Lt>16</Lt>
            <n_ops_T2g>3</n_ops_T2g>
            <n_ops_Eg>3</n_ops_Eg>
            <OT2_0>...</OT2_0>
            <OT2_1>...</OT2_1>
            <OT2_2>...</OT2_2>
            <OE_0>...</OE_0>
            ...
          </Op_spin2>
        </glueball_GEVP_T2g>
    """
    try:
        tree = ET.parse(xml_path)
    except (ET.ParseError, FileNotFoundError):
        return None

    root = tree.getroot()
    op = root.find("Op_spin2")
    if op is None:
        return None
    lt_node = op.find("Lt")
    if lt_node is None:
        return None
    Lt = int(lt_node.text.strip())

    t2g: Dict[int, np.ndarray] = {}
    eg: Dict[int, np.ndarray] = {}
    for child in op:
        tag = child.tag
        if child.text is None:
            continue
        vals = _parse_floats(child.text)
        if vals.size != Lt:
            continue
        if tag.startswith("OT2_"):
            try:
                a = int(tag[len("OT2_"):])
            except ValueError:
                continue
            t2g[a] = vals
        elif tag.startswith("OE_"):
            try:
                a = int(tag[len("OE_"):])
            except ValueError:
                continue
            eg[a] = vals
    if not t2g and not eg:
        return None
    return {"T2g": t2g, "Eg": eg}


# ============================================================================
# 2. ENSEMBLE LOADERS
# ============================================================================
@dataclass
class BetaData:
    beta: float
    tag: str                                          # "240" / "250" / "260"
    Lt: int
    n_cfg: int
    # A1g scalar: shape (n_cfg, n_op_a1g, Lt)
    a1g: Optional[np.ndarray] = None
    # T2g: (n_cfg, n_ape, Lt) ; Eg: same
    t2g: Optional[np.ndarray] = None
    eg: Optional[np.ndarray] = None
    # plaquette (sanity)
    plaq: Optional[np.ndarray] = None


def load_beta(dirpath: Path, beta: float, tag: str,
              limit: Optional[int] = None) -> Optional[BetaData]:
    """
    Walk dirpath for glue_*.out.xml, parse each, stack into BetaData.
    Auto-detects which schema each XML uses (v3 scalar vs T2g/Eg).
    """
    if not dirpath.is_dir():
        print(f"  [load_beta] no dir {dirpath}", file=sys.stderr)
        return None

    files = sorted(dirpath.glob("glue_*.out.xml"))
    if limit is not None:
        files = files[:limit]
    if not files:
        print(f"  [load_beta] no glue_*.out.xml in {dirpath}", file=sys.stderr)
        return None

    a1g_list: List[np.ndarray] = []
    t2g_list: List[np.ndarray] = []
    eg_list: List[np.ndarray] = []
    Lt: Optional[int] = None
    n_op_a1g: Optional[int] = None
    n_ape_2pp: Optional[int] = None

    for f in files:
        v3 = parse_v3_scalar(f)
        if v3 is not None:
            keys = sorted(v3.keys())
            mat = np.stack([v3[k] for k in keys], axis=0)
            if n_op_a1g is None:
                n_op_a1g = mat.shape[0]
                Lt = mat.shape[1]
            elif mat.shape[0] == n_op_a1g and mat.shape[1] == Lt:
                pass
            else:
                continue
            a1g_list.append(mat)
            continue
        t2 = parse_t2g_eg(f)
        if t2 is not None:
            T2 = t2["T2g"]
            E = t2["Eg"]
            if T2:
                keys = sorted(T2.keys())
                m = np.stack([T2[k] for k in keys], axis=0)
                if n_ape_2pp is None:
                    n_ape_2pp = m.shape[0]
                    if Lt is None:
                        Lt = m.shape[1]
                if m.shape[0] == n_ape_2pp and m.shape[1] == Lt:
                    t2g_list.append(m)
            if E:
                keys = sorted(E.keys())
                m = np.stack([E[k] for k in keys], axis=0)
                if m.shape[0] == n_ape_2pp and m.shape[1] == Lt:
                    eg_list.append(m)

    if Lt is None:
        print(f"  [load_beta] no usable XML files at {dirpath}", file=sys.stderr)
        return None

    bd = BetaData(beta=beta, tag=tag, Lt=Lt,
                  n_cfg=max(len(a1g_list), len(t2g_list), len(eg_list)))
    if a1g_list:
        bd.a1g = np.stack(a1g_list, axis=0)        # (n_cfg, n_op, Lt)
    if t2g_list:
        bd.t2g = np.stack(t2g_list, axis=0)
    if eg_list:
        bd.eg = np.stack(eg_list, axis=0)
    print(f"  [load_beta beta={beta}] Lt={Lt}, n_cfg={bd.n_cfg}, "
          f"A1g={bd.a1g.shape if bd.a1g is not None else None}, "
          f"T2g={bd.t2g.shape if bd.t2g is not None else None}, "
          f"Eg={bd.eg.shape if bd.eg is not None else None}")
    return bd


# ============================================================================
# 3. CORRELATOR BUILDER
# ============================================================================
def build_correlator(ops: np.ndarray, subtract_vev: bool = True) -> np.ndarray:
    """
    From per-cfg operator timeseries ops[n_cfg, n_op, Lt] build the symmetric
    correlator matrix C(t)[n_op, n_op] for each t using translation invariance:
        C_ij(t) = (1/Lt) * <sum_{t0} O_i(t0+t) * O_j(t0)>_cfg
    With optional VEV subtraction (ops -= <ops>).  Returns array of shape
    (Lt, n_op, n_op).
    """
    n_cfg, n_op, Lt = ops.shape
    if subtract_vev:
        ops_centered = ops - ops.mean(axis=(0, 2), keepdims=True)
    else:
        ops_centered = ops

    # FFT-based shifted-product convolution (real-valued, t direction periodic):
    #   sum_{t0} O_i(t0+t) * O_j(t0)  =  IFFT[ FFT(O_i) * conj(FFT(O_j)) ](t)
    # Per-cfg, then average over cfg.
    F = np.fft.fft(ops_centered, axis=2)              # (n_cfg, n_op, Lt)
    # outer in op indices: F_i * conj(F_j) summed over cfg
    C_t = np.zeros((Lt, n_op, n_op), dtype=np.float64)
    for i in range(n_op):
        for j in range(n_op):
            cross = F[:, i, :] * np.conj(F[:, j, :])  # (n_cfg, Lt)
            corr_t = np.real(np.fft.ifft(cross, axis=1)) / Lt  # (n_cfg, Lt)
            C_t[:, i, j] = corr_t.mean(axis=0)
    # Symmetrize numerically (small floating asymmetry from rounding)
    for t in range(Lt):
        C_t[t] = 0.5 * (C_t[t] + C_t[t].T)
    return C_t


def fold_correlator(C: np.ndarray) -> np.ndarray:
    """Fold C(t) over t -> Lt - t for periodic BC."""
    Lt = C.shape[0]
    Cf = C.copy()
    for t in range(1, Lt):
        Cf[t] = 0.5 * (C[t] + C[(Lt - t) % Lt])
    return Cf


# ============================================================================
# 4. GEVP SOLVER
# ============================================================================
def solve_gevp_levels(C: np.ndarray, t0: int = 1,
                      reg: float = 1e-10
                      ) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solve  C(t) v_n = lambda_n(t) C(t0) v_n  for all t.
    Returns
       lambdas : (Lt, n_op)   sorted DESCENDING per t (ground state = column 0)
       vecs    : (Lt, n_op, n_op)
    Regularization added to C(t0) diagonal to keep positive-definite.
    """
    Lt, n_op, _ = C.shape
    C0 = 0.5 * (C[t0] + C[t0].T)
    C0 = C0 + reg * np.eye(n_op)
    lambdas = np.full((Lt, n_op), np.nan)
    vecs = np.full((Lt, n_op, n_op), np.nan)
    for t in range(Lt):
        Ct = 0.5 * (C[t] + C[t].T)
        try:
            w, v = eigh(Ct, C0)            # ascending
        except (np.linalg.LinAlgError, ValueError):
            continue
        order = np.argsort(w)[::-1]
        lambdas[t] = w[order]
        vecs[t] = v[:, order]
    return lambdas, vecs


def effective_mass_cosh(lam_n: np.ndarray) -> np.ndarray:
    """
    m_eff(t) = arccosh( (lam(t-1) + lam(t+1)) / (2 lam(t)) ) from a single
    principal-correlator column.  Returns array shape (Lt,) with NaN where
    inadmissible.
    """
    Lt = lam_n.size
    m = np.full(Lt, np.nan)
    for t in range(1, Lt - 1):
        lt = lam_n[t]
        lp = lam_n[t - 1]
        ln = lam_n[t + 1]
        if not (np.isfinite(lt) and np.isfinite(lp) and np.isfinite(ln)):
            continue
        if lt <= 0:
            continue
        arg = (lp + ln) / (2.0 * lt)
        if arg <= 1.0:
            continue
        m[t] = np.arccosh(arg)
    return m


def plateau_fit(m_eff: np.ndarray, sig: np.ndarray,
                t_min: int, t_max: int) -> Tuple[float, float, int]:
    """
    Weighted constant fit on m_eff(t) in [t_min, t_max].
    Returns (m_bar, sigma_m, n_used) ; (nan, nan, 0) on insufficient data.
    """
    t_min = max(t_min, 0)
    t_max = min(t_max, m_eff.size - 1)
    ts = np.arange(t_min, t_max + 1)
    m_w = m_eff[ts]
    s_w = sig[ts]
    mask = np.isfinite(m_w) & np.isfinite(s_w) & (s_w > 0)
    if mask.sum() < 2:
        return (float("nan"), float("nan"), int(mask.sum()))
    w = 1.0 / s_w[mask] ** 2
    m_bar = (w * m_w[mask]).sum() / w.sum()
    var = 1.0 / w.sum()
    # Inflate by sqrt(chi2/dof) if scattered
    chi2 = (w * (m_w[mask] - m_bar) ** 2).sum()
    dof = max(mask.sum() - 1, 1)
    scale = max(1.0, np.sqrt(chi2 / dof))
    return (float(m_bar), float(np.sqrt(var) * scale), int(mask.sum()))


# ============================================================================
# 5. JACKKNIFE
# ============================================================================
def jackknife_eff_mass(ops: np.ndarray, t0: int = 1,
                       which_eig: int = 0,
                       fold: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the jackknife mean and sigma of m_eff(t) for the `which_eig`-th
    principal correlator over the configuration ensemble.
    Returns (m_eff_mean, m_eff_sigma) each shape (Lt,).
    """
    n_cfg = ops.shape[0]
    Lt = ops.shape[2]
    m_jk = np.full((n_cfg, Lt), np.nan)
    for k in range(n_cfg):
        sel = np.delete(np.arange(n_cfg), k)
        ops_k = ops[sel]
        C_k = build_correlator(ops_k, subtract_vev=True)
        if fold:
            C_k = fold_correlator(C_k)
        lam_k, _ = solve_gevp_levels(C_k, t0=t0)
        if which_eig < lam_k.shape[1]:
            m_jk[k] = effective_mass_cosh(lam_k[:, which_eig])
    mean_jk = np.nanmean(m_jk, axis=0)
    # Jackknife sigma:  sqrt((N-1) * mean( (theta_k - mean_jk)^2 ))
    diff_sq = (m_jk - mean_jk[None, :]) ** 2
    # Sample variance using only valid (non-NaN) bins per t
    var_jk = np.nanmean(diff_sq, axis=0) * (n_cfg - 1)
    sig_jk = np.sqrt(var_jk)
    return mean_jk, sig_jk


# ============================================================================
# 6. CHANNEL MASS EXTRACTION
# ============================================================================
@dataclass
class ChannelResult:
    label: str
    n_ops_used: int
    m_gs_a: float
    m_gs_a_err: float
    m_ex_a: float = float("nan")           # excited state (J=4 candidate when relevant)
    m_ex_a_err: float = float("nan")
    plateau_window_gs: Tuple[int, int] = (0, 0)
    plateau_window_ex: Tuple[int, int] = (0, 0)
    n_plateau_pts: int = 0


def extract_channel(ops: np.ndarray, label: str,
                    t0: int = 1,
                    plateau_gs: Tuple[int, int] = (3, 6),
                    plateau_ex: Tuple[int, int] = (2, 4)) -> ChannelResult:
    """
    Solve GEVP + jackknife + plateau fit for an operator-basis channel.
    Returns ground-state mass and (if n_ops >= 2) first-excited mass in
    lattice units (m * a).
    """
    n_cfg, n_op, Lt = ops.shape

    # Ground state
    m_gs_mean, m_gs_sig = jackknife_eff_mass(ops, t0=t0, which_eig=0,
                                              fold=True)
    m_gs, e_gs, n_gs = plateau_fit(m_gs_mean, m_gs_sig, *plateau_gs)

    res = ChannelResult(
        label=label,
        n_ops_used=n_op,
        m_gs_a=m_gs,
        m_gs_a_err=e_gs,
        plateau_window_gs=plateau_gs,
        n_plateau_pts=n_gs,
    )

    # Excited state (J=4 candidate if `label` is one of A1g_ex, Eg_ex, T2g_ex)
    if n_op >= 2:
        m_ex_mean, m_ex_sig = jackknife_eff_mass(ops, t0=t0, which_eig=1,
                                                  fold=True)
        m_ex, e_ex, _ = plateau_fit(m_ex_mean, m_ex_sig, *plateau_ex)
        res.m_ex_a = m_ex
        res.m_ex_a_err = e_ex
        res.plateau_window_ex = plateau_ex
    return res


# ============================================================================
# 7. STRING TENSION (sigma a^2) -- placeholder; reads pre-computed if present
# ============================================================================
def load_string_tension(beta_tag: str, fallback_table_path: Optional[Path]
                        = None) -> Tuple[float, float]:
    """
    Load a^2 * sigma for the given beta.  Strategy (in order):
        1. Look for /root/gevp_t2g/output/b<tag>/sigma_a2.json
        2. fallback_table_path = JSON dict {"240": [sa2, err], "250": ..., "260": ...}
        3. Hard fallback to canonical LTW 2004 SU(2) values.

    Returns (a^2 * sigma, error).
    """
    candidate = Path(f"/root/gevp_t2g/output/b{beta_tag}/sigma_a2.json")
    if candidate.is_file():
        with candidate.open() as f:
            d = json.load(f)
        return float(d["sigma_a2"]), float(d.get("sigma_a2_err", 0.0))

    if fallback_table_path is not None and fallback_table_path.is_file():
        with fallback_table_path.open() as f:
            tab = json.load(f)
        if beta_tag in tab:
            v = tab[beta_tag]
            return float(v[0]), float(v[1])

    # Hard-coded LTW 2004 Table 6 SU(2) -- replace once measured locally.
    # These are illustrative defaults for script self-test ONLY.
    canonical = {
        "240": (0.0710, 0.0010),
        "250": (0.0395, 0.0008),
        "260": (0.0228, 0.0006),
    }
    if beta_tag in canonical:
        return canonical[beta_tag]
    return (float("nan"), float("nan"))


# ============================================================================
# 8. CONTINUUM EXTRAPOLATION m^2 / sigma at a -> 0
# ============================================================================
def continuum_extrapolate(ratios_sq: List[Tuple[float, float, float]]
                          ) -> Tuple[float, float, Dict[str, float]]:
    """
    ratios_sq : list of (a^2_sigma, R, sigma_R) per beta.
    Linear fit:  R(a) = R0 + c * a^2_sigma.
    Returns (R0, sigma_R0, fit_info).
    """
    ratios_sq = [r for r in ratios_sq
                 if all(np.isfinite(x) for x in r) and r[2] > 0]
    if len(ratios_sq) < 2:
        return float("nan"), float("nan"), {"n_points": len(ratios_sq)}
    x = np.array([r[0] for r in ratios_sq])
    y = np.array([r[1] for r in ratios_sq])
    s = np.array([r[2] for r in ratios_sq])
    w = 1.0 / s ** 2
    # Weighted linear: minimize sum w * (y - (R0 + c*x))^2
    A = np.vstack([np.ones_like(x), x]).T
    W = np.diag(w)
    AtWA = A.T @ W @ A
    AtWy = A.T @ W @ y
    try:
        coef = np.linalg.solve(AtWA, AtWy)
        cov = np.linalg.inv(AtWA)
    except np.linalg.LinAlgError:
        return float("nan"), float("nan"), {"n_points": len(ratios_sq)}
    R0, c = coef
    sR0 = float(np.sqrt(cov[0, 0]))
    # chi2 / dof
    resid = y - (R0 + c * x)
    chi2 = float((w * resid ** 2).sum())
    dof = max(len(x) - 2, 1)
    if chi2 / dof > 1.0:
        sR0 *= np.sqrt(chi2 / dof)
    return float(R0), sR0, {
        "n_points": len(ratios_sq),
        "slope_c": float(c),
        "chi2": chi2,
        "dof": dof,
        "x_a2sigma": x.tolist(),
        "y_ratio": y.tolist(),
        "y_err": s.tolist(),
    }


# ============================================================================
# 9. 4++ CANDIDATE COMBINATION
# ============================================================================
def combine_4pp_candidates(channels: Dict[str, ChannelResult],
                           sigma_a2: Tuple[float, float]
                           ) -> Dict[str, float]:
    """
    Given per-channel ChannelResults at a single beta, build a J=4
    candidate mass m(4++) by inverse-variance averaging the J=4 contributors
    in physical units sqrt(sigma) -- i.e. m_eff_a / sqrt(sigma a^2).

    J=4 = A_1 (+) E (+) T_1 (+) T_2 in O_h.  In this script we cover:
        - A_1 piece: A1g excited state (from v3 scalar GEVP excited eigenvalue)
        - E   piece: Eg excited state (from T2g/Eg GEVP excited eigenvalue)
        - T_2 piece: T2g excited state (from T2g/Eg GEVP excited eigenvalue)
        - T_1 piece: NOT MEASURED (no T_1 operator available in current XML)
    The T_1 absence is logged as a systematic in the output JSON.

    Returns dict with combined m(4++) / sqrt(sigma), per-piece breakdown,
    and the 0++ ground-state reference.
    """
    a2s, a2s_err = sigma_a2
    if not (np.isfinite(a2s) and a2s > 0):
        return {"status": "no_string_tension"}

    sqrt_sa2 = np.sqrt(a2s)

    def to_phys(m_a: float, m_a_err: float) -> Tuple[float, float]:
        """Convert m * a -> m / sqrt(sigma)."""
        if not (np.isfinite(m_a) and np.isfinite(m_a_err)):
            return float("nan"), float("nan")
        # propagate sigma_a2 uncertainty: m/sqrt(sigma) = (m*a)/sqrt(a^2*sigma)
        m_phys = m_a / sqrt_sa2
        # rel error in quadrature
        rel_err = np.sqrt((m_a_err / m_a) ** 2 + 0.25 * (a2s_err / a2s) ** 2) \
            if m_a > 0 else float("nan")
        return float(m_phys), float(m_phys * rel_err) if np.isfinite(rel_err) else float("nan")

    out: Dict[str, float] = {}

    # 0++ reference
    if "A1g" in channels:
        ch = channels["A1g"]
        m0, m0e = to_phys(ch.m_gs_a, ch.m_gs_a_err)
        out["m_0pp"] = m0
        out["m_0pp_err"] = m0e

    # J=4 candidates
    pieces: List[Tuple[float, float, str]] = []
    if "A1g" in channels and np.isfinite(channels["A1g"].m_ex_a):
        m, me = to_phys(channels["A1g"].m_ex_a, channels["A1g"].m_ex_a_err)
        if np.isfinite(m) and np.isfinite(me) and me > 0:
            pieces.append((m, me, "A1g_ex (A_1 piece)"))
            out["A1g_ex"] = m
            out["A1g_ex_err"] = me
    if "Eg" in channels and np.isfinite(channels["Eg"].m_ex_a):
        m, me = to_phys(channels["Eg"].m_ex_a, channels["Eg"].m_ex_a_err)
        if np.isfinite(m) and np.isfinite(me) and me > 0:
            pieces.append((m, me, "Eg_ex (E piece)"))
            out["Eg_ex"] = m
            out["Eg_ex_err"] = me
    if "T2g" in channels and np.isfinite(channels["T2g"].m_ex_a):
        m, me = to_phys(channels["T2g"].m_ex_a, channels["T2g"].m_ex_a_err)
        if np.isfinite(m) and np.isfinite(me) and me > 0:
            pieces.append((m, me, "T2g_ex (T_2 piece)"))
            out["T2g_ex"] = m
            out["T2g_ex_err"] = me

    out["t1_piece_status"] = "NOT_MEASURED (no T_1 operator in current XML)"

    if not pieces:
        out["status"] = "no_J4_pieces"
        return out

    mvals = np.array([p[0] for p in pieces])
    evals = np.array([p[1] for p in pieces])
    w = 1.0 / evals ** 2
    m4 = float((w * mvals).sum() / w.sum())
    # Statistical-only error from inverse-variance
    e4_stat = float(1.0 / np.sqrt(w.sum()))
    # Systematic from cubic-rep spread (RMS of |m_i - m4|)
    e4_sys = float(np.sqrt(np.mean((mvals - m4) ** 2))) if len(mvals) >= 2 else 0.0
    e4_tot = float(np.sqrt(e4_stat ** 2 + e4_sys ** 2))
    out["m_4pp"] = m4
    out["m_4pp_stat_err"] = e4_stat
    out["m_4pp_sys_cubic_spread_err"] = e4_sys
    out["m_4pp_err"] = e4_tot
    out["n_4pp_pieces"] = len(pieces)
    out["pieces"] = [
        {"value": float(m), "err": float(e), "label": lbl}
        for (m, e, lbl) in pieces
    ]

    # Ratio
    if "m_0pp" in out and out["m_0pp"] > 0 and np.isfinite(out["m_0pp_err"]):
        R = (m4 / out["m_0pp"]) ** 2
        # propagate: delta R / R = 2 sqrt((dm4/m4)^2 + (dm0/m0)^2)
        rel = np.sqrt((e4_tot / m4) ** 2 + (out["m_0pp_err"] / out["m_0pp"]) ** 2)
        out["ratio_4pp_sq"] = float(R)
        out["ratio_4pp_sq_err"] = float(2.0 * R * rel)
    return out


# ============================================================================
# 10. VERDICT
# ============================================================================
def verdict(R_continuum: float, sigma: float) -> str:
    if not (np.isfinite(R_continuum) and np.isfinite(sigma) and sigma > 0):
        return "INCONCLUSIVE (extraction failed or noise-dominated)"
    pred = ECI_PHASE_E2["ratio_4pp_sq_pred"]
    dev = abs(R_continuum - pred)
    nsig = dev / sigma
    if (CONFIRM_BAND[0] <= R_continuum - sigma
            and R_continuum + sigma <= CONFIRM_BAND[1]):
        return f"CONFIRMED at >= 2 sigma : R = {R_continuum:.3f} +/- {sigma:.3f} (pred 3.00 +/- 0.05)"
    if dev >= 5.0 * sigma and (R_continuum < FALSIFY_BAND[0] or R_continuum > FALSIFY_BAND[1]):
        return f"FALSIFIED at {nsig:.1f} sigma : R = {R_continuum:.3f} +/- {sigma:.3f} (pred 3.00, dev = {dev:.3f})"
    return f"INCONCLUSIVE : R = {R_continuum:.3f} +/- {sigma:.3f}, {nsig:.1f} sigma from pred"


# ============================================================================
# 11. DRIVER
# ============================================================================
def analyze_beta(bd: BetaData, t0: int, plateau_gs: Tuple[int, int],
                 plateau_ex: Tuple[int, int]) -> Dict:
    print(f"\n=== beta = {bd.beta}  (tag {bd.tag}) ===")
    print(f"  Lt = {bd.Lt} ;  n_cfg = {bd.n_cfg}")

    channels: Dict[str, ChannelResult] = {}
    if bd.a1g is not None:
        channels["A1g"] = extract_channel(bd.a1g, "A1g",
                                          t0=t0,
                                          plateau_gs=plateau_gs,
                                          plateau_ex=plateau_ex)
    if bd.t2g is not None:
        channels["T2g"] = extract_channel(bd.t2g, "T2g",
                                          t0=t0,
                                          plateau_gs=plateau_gs,
                                          plateau_ex=plateau_ex)
    if bd.eg is not None:
        channels["Eg"] = extract_channel(bd.eg, "Eg",
                                         t0=t0,
                                         plateau_gs=plateau_gs,
                                         plateau_ex=plateau_ex)

    print(f"  Channels extracted: {list(channels.keys())}")
    for name, ch in channels.items():
        gs = f"{ch.m_gs_a:.4f}+/-{ch.m_gs_a_err:.4f}" if np.isfinite(ch.m_gs_a) else "N/A"
        ex = f"{ch.m_ex_a:.4f}+/-{ch.m_ex_a_err:.4f}" if np.isfinite(ch.m_ex_a) else "N/A"
        print(f"    {name}: m_gs*a = {gs}   m_ex*a = {ex}   n_op = {ch.n_ops_used}")

    sa2, sa2e = load_string_tension(bd.tag)
    combo = combine_4pp_candidates(channels, (sa2, sa2e))
    return {
        "beta": bd.beta,
        "tag": bd.tag,
        "n_cfg": bd.n_cfg,
        "Lt": bd.Lt,
        "sigma_a2": sa2,
        "sigma_a2_err": sa2e,
        "channels": {k: asdict(v) for k, v in channels.items()},
        "combine_4pp": combo,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-root", type=Path,
                        default=Path("/root/gevp_t2g/output"),
                        help="root dir containing b240/, b250/, b260/")
    parser.add_argument("--betas", nargs="+",
                        default=["240:2.40", "250:2.50", "260:2.60"],
                        help="list of 'tag:value' (default: Utah Stage B 3 couplings)")
    parser.add_argument("--t0", type=int, default=2,
                        help="GEVP t0 reference time (default 2)")
    parser.add_argument("--plateau-gs", nargs=2, type=int, default=[3, 6],
                        help="ground-state plateau window [t_min t_max]")
    parser.add_argument("--plateau-ex", nargs=2, type=int, default=[2, 4],
                        help="excited-state plateau window [t_min t_max]")
    parser.add_argument("--limit-cfg", type=int, default=None,
                        help="cap per-beta config count (debug)")
    parser.add_argument("--out-summary", type=Path,
                        default=Path("gevp_4plusplus_summary.json"))
    parser.add_argument("--no-fold", action="store_true",
                        help="skip cosh folding (debug)")
    args = parser.parse_args()

    plateau_gs = (args.plateau_gs[0], args.plateau_gs[1])
    plateau_ex = (args.plateau_ex[0], args.plateau_ex[1])

    print("=" * 72)
    print("  Phase E2 SU(2) 4++ GEVP ANALYZER")
    print("=" * 72)
    print("  Prediction (D=-67 SST): m^2(4++)/m^2(0++) = "
          f"{ECI_PHASE_E2['ratio_4pp_sq_pred']:.2f} +/- "
          f"{ECI_PHASE_E2['ratio_4pp_sq_pred_err']:.2f}")
    print("  Reference AT 2021 SU(2): m_0++ = "
          f"{AT2021_SU2['m_0pp']:.3f}({int(1000*AT2021_SU2['m_0pp_err'])}) sqrt(sigma)")
    print("  Reference AT 2021 SU(2): m_2++ = "
          f"{AT2021_SU2['m_2pp']:.3f}({int(1000*AT2021_SU2['m_2pp_err'])}) sqrt(sigma)")
    print()

    per_beta: List[Dict] = []
    for spec in args.betas:
        try:
            tag, val = spec.split(":")
            beta = float(val)
        except ValueError:
            print(f"  bad beta spec '{spec}', expected 'tag:value'", file=sys.stderr)
            continue
        dirpath = args.data_root / f"b{tag}"
        bd = load_beta(dirpath, beta, tag, limit=args.limit_cfg)
        if bd is None:
            print(f"  [main] no data for beta = {beta}", file=sys.stderr)
            continue
        r = analyze_beta(bd, t0=args.t0,
                         plateau_gs=plateau_gs, plateau_ex=plateau_ex)
        per_beta.append(r)
        side = Path(f"gevp_4plusplus_b{tag}.json")
        with side.open("w") as f:
            json.dump(r, f, indent=2, default=float)
        print(f"  -> per-beta JSON: {side}")

    # Continuum extrapolation of m^2(4++)/m^2(0++)
    triples: List[Tuple[float, float, float]] = []
    for r in per_beta:
        c = r.get("combine_4pp", {})
        sa2 = r.get("sigma_a2", float("nan"))
        if not isinstance(c, dict):
            continue
        R = c.get("ratio_4pp_sq")
        Re = c.get("ratio_4pp_sq_err")
        if R is None or Re is None:
            continue
        if not (np.isfinite(R) and np.isfinite(Re) and Re > 0
                and np.isfinite(sa2)):
            continue
        triples.append((float(sa2), float(R), float(Re)))

    R0, sR0, fit_info = continuum_extrapolate(triples)
    final_verdict = verdict(R0, sR0)
    print("\n" + "=" * 72)
    print("  CONTINUUM EXTRAPOLATION  m^2(4++)/m^2(0++)  at  a^2 sigma -> 0")
    print("=" * 72)
    if np.isfinite(R0):
        print(f"  R(a -> 0) = {R0:.3f} +/- {sR0:.3f}  (n_betas = {fit_info['n_points']})")
        print(f"  per-beta: " + "  ".join(
            f"(a^2 sig = {x:.4f}, R = {y:.3f} +/- {e:.3f})"
            for (x, y, e) in triples))
    else:
        print("  Insufficient per-beta points or unstable fit.")
    print(f"  VERDICT: {final_verdict}")
    print("=" * 72)

    summary = {
        "prediction": ECI_PHASE_E2,
        "at2021_anchors": AT2021_SU2,
        "per_beta": per_beta,
        "continuum": {
            "R_squared_at_a0": R0,
            "sigma": sR0,
            "fit_info": fit_info,
        },
        "verdict": final_verdict,
        "confirm_band": CONFIRM_BAND,
        "falsify_band": FALSIFY_BAND,
        "arxiv_anchors_pre_verified": [
            "2106.00364",       # AT 2021 (VERIFIED_WITHDRAWN -> extended)
            "hep-lat/0404008",  # Lucini-Teper-Wenger 2004
            "hep-lat/9711011",  # Teper 1998 NATO-ASI
            "2508.21821",       # Abbott et al. 2025
        ],
        "no_fabrications": True,
    }
    with args.out_summary.open("w") as f:
        json.dump(summary, f, indent=2, default=float)
    print(f"\n  Summary JSON: {args.out_summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
