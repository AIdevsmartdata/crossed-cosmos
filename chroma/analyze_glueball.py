#!/usr/bin/env python3
"""
Phase 3 analyzer — SU(2) Yang-Mills scaling test from Chroma output.

INPUTS (per config):
  /root/results/b{TAG}/wflow_{N}.log     # contains 'WFLOW t gact4i gactij' lines
  /root/results/b{TAG}/wflow_{N}.out.xml # contains <wils_loop1> spatial loops W(r,t)

EXTRACTS (per beta):
  - t_0/a²  via   t²<E(t)>|_{t=t_0} = 0.3
  - w_0/a   via   t·d/dt(t²<E(t)>)|_{t=w_0²} = 0.3   (BMW 2012 definition)
  - σa²     from V(r) fit  V(r) = -e/r + σ·r + c
  - dimensionless ratio  w_0·√σ   (continuum SU(2) ≈ 1.05, Teper 1999)

OUTPUT:
  /root/results/summary.txt
  stdout: per-beta means + jackknife errors
"""

import xml.etree.ElementTree as ET
import numpy as np
from pathlib import Path
from scipy.optimize import curve_fit
import sys, re

RESDIR = Path("/root/results")
BETAS  = ["2.40", "2.45", "2.50", "2.60"]   # all 4 beta values

# Wilson flow target
WFLOW_TARGET = 0.3

# Wilson-loop static-potential fit window (lattice units)
V_FIT_R_MIN = 2
V_FIT_R_MAX = 7   # up to L/2 typically — for L=16 take r<=7 to avoid finite-volume contamination
T_FIT       = 4   # t at which to evaluate V(r) = -log(W(r,t)/W(r,t-1))
T_FIT_PREV  = T_FIT - 1


# =========================================================================
# WILSON FLOW — log file parsing
# =========================================================================
WFLOW_RE = re.compile(r"^WFLOW\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)")

def parse_wflow_log(log_path):
    """Return arrays t, E(t) (using gact4i) for one config; None if missing."""
    ts, Es = [], []
    try:
        with open(log_path) as f:
            for line in f:
                m = WFLOW_RE.match(line)
                if m:
                    try:
                        t = float(m.group(1))
                        E = float(m.group(2))   # gact4i (plaquette action density)
                        ts.append(t); Es.append(E)
                    except ValueError:
                        pass
    except FileNotFoundError:
        return None
    if len(ts) < 5:
        return None
    return np.array(ts), np.array(Es)


def extract_w0_t0(t, E):
    """Return (t_0/a², w_0/a) for one config, or (None, None) if curves don't cross."""
    Y = t * t * E                       # t² E(t)
    # 1) t_0:  Y(t_0) = 0.3
    idx = np.where(Y >= WFLOW_TARGET)[0]
    if len(idx) == 0 or idx[0] == 0:
        t0 = None
    else:
        i = idx[0]
        y0, y1 = Y[i-1], Y[i]
        t0 = t[i-1] + (WFLOW_TARGET - y0) * (t[i] - t[i-1]) / (y1 - y0)

    # 2) w_0² :  t · dY/dt = 0.3
    dYdt = np.gradient(Y, t)
    W = t * dYdt
    idx2 = np.where(W >= WFLOW_TARGET)[0]
    if len(idx2) == 0 or idx2[0] == 0:
        w0sq = None
    else:
        i = idx2[0]
        w0, w1 = W[i-1], W[i]
        w0sq = t[i-1] + (WFLOW_TARGET - w0) * (t[i] - t[i-1]) / (w1 - w0)

    w0_over_a = np.sqrt(w0sq) if w0sq is not None else None
    return t0, w0_over_a


# =========================================================================
# WILSON LOOPS — XML parsing
# =========================================================================
def parse_wils_loop1(xml_path):
    """Return W(r,t) as a (lengthr, lengthr) numpy array from <wils_loop1>.
       Rows = r (spatial), cols = t (1..lengthr).
       Return None if not found."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception:
        return None
    for wls in root.iter("wils_loop1"):
        Lr_el = wls.find("lengthr")
        if Lr_el is None:
            continue
        Lr = int(Lr_el.text.strip())
        W = np.full((Lr, Lr), np.nan)
        wl1 = wls.find("wloop1")
        if wl1 is None:
            continue
        for elem in wl1.findall("elem"):
            r_el = elem.find("r"); loop_el = elem.find("loop")
            if r_el is None or loop_el is None:
                continue
            r = int(r_el.text.strip())
            vals = [float(x) for x in loop_el.text.split()]
            if 0 <= r < Lr:
                # vals are W(r, t) for t = 1..len(vals)
                for j, v in enumerate(vals):
                    if j < Lr:
                        W[r, j] = v
        return W
    return None


def extract_V_r(W, t_fit=T_FIT):
    """Effective static potential V(r) = -log(W(r, t_fit) / W(r, t_fit-1))."""
    if W is None: return None, None
    Lr = W.shape[0]
    if t_fit >= Lr or t_fit - 1 < 0: return None, None
    Wt   = W[:, t_fit]      # W(r, t_fit)   (column t_fit-1 in 0-indexed → idx t_fit-1)
    Wtm1 = W[:, t_fit - 1]  # W(r, t_fit-1) (idx t_fit-2)
    # Watch off-by-one: W[r, j] holds W(r, t=j+1).  So W(r, t)=W[r, t-1].
    Wt   = W[:, t_fit - 1]    # W(r, t = t_fit)
    Wtm1 = W[:, t_fit - 2]    # W(r, t = t_fit-1)
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = Wt / Wtm1
        V = -np.log(np.where(ratio > 0, ratio, np.nan))
    r = np.arange(Lr)
    return r, V


def cornell(r, e, sigma, c):
    return -e / np.maximum(r, 1e-9) + sigma * r + c


def fit_sigma(r, V, r_min=V_FIT_R_MIN, r_max=V_FIT_R_MAX):
    """Fit V(r) = -e/r + σ·r + c on r∈[r_min, r_max]. Return σ or None."""
    mask = (r >= r_min) & (r <= r_max) & np.isfinite(V)
    if mask.sum() < 3: return None
    rr = r[mask].astype(float)
    VV = V[mask]
    try:
        p0 = [0.3, 0.05, 0.5]
        popt, _ = curve_fit(cornell, rr, VV, p0=p0, maxfev=5000)
        return popt[1]   # sigma
    except Exception:
        return None


# =========================================================================
# PER-BETA AGGREGATION
# =========================================================================
def beta_tag(b):
    return b.replace(".", "")


def jackknife(arr):
    """Return (mean, jackknife error of mean) of a 1D array."""
    arr = np.asarray(arr, dtype=float)
    arr = arr[np.isfinite(arr)]
    n = len(arr)
    if n == 0: return float("nan"), float("nan")
    if n == 1: return float(arr[0]), float("nan")
    mean = arr.mean()
    # jackknife: leave-one-out
    sum_all = arr.sum()
    jk = (sum_all - arr) / (n - 1)
    err = np.sqrt((n - 1) * np.mean((jk - mean) ** 2))
    return float(mean), float(err)


def analyze_beta(beta):
    tag = beta_tag(beta)
    bdir = RESDIR / f"b{tag}"
    if not bdir.exists():
        return None
    logs = sorted(bdir.glob("wflow_*.log"))
    xmls = sorted(bdir.glob("wflow_*.out.xml"))
    print(f"\n=== β = {beta}  (dir {bdir}, {len(logs)} logs, {len(xmls)} XMLs) ===")
    t0_list, w0_list, sig_list = [], [], []
    for log in logs:
        # Use only logs whose chroma run completed successfully
        try:
            tail = log.read_text()[-1000:]
            if "ran successfully" not in tail:
                continue
        except Exception:
            continue
        wf = parse_wflow_log(log)
        if wf is None: continue
        t, E = wf
        t0, w0 = extract_w0_t0(t, E)
        if t0 is not None: t0_list.append(t0)
        if w0 is not None: w0_list.append(w0)

        # parse corresponding xml
        idx = log.stem.replace("wflow_", "")
        xml = bdir / f"wflow_{idx}.out.xml"
        W = parse_wils_loop1(xml)
        if W is None: continue
        r, V = extract_V_r(W, T_FIT)
        if r is None: continue
        s = fit_sigma(r, V)
        if s is not None and np.isfinite(s) and s > 0:
            sig_list.append(s)

    if len(w0_list) == 0:
        print("  (no usable measurements)")
        return None

    t0_mean, t0_err = jackknife(t0_list)
    w0_mean, w0_err = jackknife(w0_list)
    sig_mean, sig_err = jackknife(sig_list)

    print(f"  N(w0)={len(w0_list)}   N(σ)={len(sig_list)}")
    print(f"  t_0/a²       = {t0_mean:.4f} ± {t0_err:.4f}")
    print(f"  w_0/a        = {w0_mean:.4f} ± {w0_err:.4f}")
    print(f"  σ a²         = {sig_mean:.5f} ± {sig_err:.5f}")
    if np.isfinite(sig_mean) and sig_mean > 0 and np.isfinite(w0_mean):
        ratio = w0_mean * np.sqrt(sig_mean)
        # error via independent-error propagation (w0 and σ are uncorrelated configs to first order)
        rel_err = np.sqrt((w0_err / w0_mean) ** 2 + (0.5 * sig_err / sig_mean) ** 2)
        print(f"  w_0·√σ       = {ratio:.4f} ± {ratio * rel_err:.4f}   "
              f"(SU(2) continuum ≈ 1.05, Teper 1999)")
    return {
        "beta": beta,
        "N_w0": len(w0_list), "N_sigma": len(sig_list),
        "t0":  (t0_mean, t0_err),
        "w0":  (w0_mean, w0_err),
        "sig": (sig_mean, sig_err),
    }


def main():
    rows = []
    for b in BETAS:
        r = analyze_beta(b)
        if r is not None: rows.append(r)

    out = RESDIR / "summary.txt"
    with open(out, "w") as f:
        f.write("# β   N_w0   N_σ   t_0/a²   ±err   w_0/a   ±err   σ·a²   ±err   w_0·√σ   ±err\n")
        for r in rows:
            t0m, t0e = r["t0"]; w0m, w0e = r["w0"]; sm, se = r["sig"]
            if np.isfinite(sm) and sm > 0:
                ratio = w0m * np.sqrt(sm)
                rerr = ratio * np.sqrt((w0e/w0m)**2 + (0.5*se/sm)**2)
            else:
                ratio, rerr = float("nan"), float("nan")
            f.write(f"{r['beta']}  {r['N_w0']:3d}  {r['N_sigma']:3d}  "
                    f"{t0m:.4f} {t0e:.4f}  {w0m:.4f} {w0e:.4f}  "
                    f"{sm:.5f} {se:.5f}  {ratio:.4f} {rerr:.4f}\n")
    print(f"\nSummary written to {out}")


if __name__ == "__main__":
    main()
