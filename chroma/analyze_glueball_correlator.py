#!/usr/bin/env python3
"""
Phase 4 — extract a*m_0++ from glueball-operator time series.

Inputs (per config):
  /root/results_phase4/b{TAG}/glue_{N}.out.xml   # contains <O>O(0) ... O(Lt-1)</O>

Per beta:
  1. Read O(t) arrays for all successful configs.
  2. Subtract config-average <O(t)>.
  3. Build connected correlator C(tau) = (1/N_t) sum_t [ <O(t)O(t+tau)> - <O(t)><O(t+tau)> ]
     averaged over time origins.
  4. Bin-jackknife: estimate C(tau) mean and jackknife sigma.
  5. Effective mass m_eff(tau) = arcosh[(C(tau-1)+C(tau+1)) / (2 C(tau))]
     (cosh form because of periodic boundary in time).
  6. Plateau fit on a chosen window -> a*m_0++.
  7. Combine with sigma a^2 from Phase 3 (Wilson loops) to give m_0++/sqrt(sigma).
     Compare to Teper 1999 SU(2): m_0++/sqrt(sigma) = 3.55 +/- 0.08.

Outputs:
  /root/results_phase4/glueball_summary.txt
"""
import xml.etree.ElementTree as ET
import numpy as np
from pathlib import Path
import re, sys

RES_PHASE4 = Path("/root/results_phase4")
RES_PHASE3 = Path("/root/results")       # phase 2 v1 dir (sigma a^2 fits)
BETAS = ["2.40", "2.45", "2.50", "2.60"]
T_FIT_MIN = 2
T_FIT_MAX = 5     # adjust depending on signal-to-noise; for L_t=16, typical window 2..5
TEPER_SU2_RATIO = 3.55   # m_0++ / sqrt(sigma), Teper hep-lat/9909124 SU(2)


# ----------------------------------------------------------------------
# XML parsing
# ----------------------------------------------------------------------
def parse_glueball_xml(xml_path):
    """Return numpy array O[t] of length Lt, or None."""
    try:
        tree = ET.parse(xml_path); root = tree.getroot()
    except Exception:
        return None
    for op in root.iter("Op_t"):
        Lt_el = op.find("Lt")
        O_el  = op.find("O")
        if Lt_el is None or O_el is None: continue
        Lt = int(Lt_el.text.strip())
        vals = [float(x) for x in O_el.text.split()]
        if len(vals) == Lt:
            return np.array(vals)
    return None


# ----------------------------------------------------------------------
# Correlator on a stack of O(t) arrays (one per config)
# ----------------------------------------------------------------------
def time_average_correlator(O_configs):
    """
    O_configs: numpy array shape (N_cfg, Lt).
    Returns C(tau) shape (Lt,):
       C(tau) = mean over (config, t) of [ O(t) O(t+tau) ] - mean(O)**2
    """
    Nc, Lt = O_configs.shape
    mean_O = O_configs.mean()  # subtract overall offset for connected piece
    O0 = O_configs - mean_O
    # correlator
    C = np.zeros(Lt)
    for tau in range(Lt):
        prod = O0 * np.roll(O0, -tau, axis=1)   # shape (Nc, Lt)
        C[tau] = prod.mean()
    return C


def jackknife_correlator(O_configs):
    """Jackknife on configurations.
       Returns C(tau) and jackknife sigma C(tau)."""
    Nc, Lt = O_configs.shape
    C_full = time_average_correlator(O_configs)
    if Nc < 2:
        return C_full, np.full(Lt, np.nan)
    C_jk = np.zeros((Nc, Lt))
    idx = np.arange(Nc)
    for i in range(Nc):
        C_jk[i] = time_average_correlator(O_configs[idx != i])
    mean_jk = C_jk.mean(axis=0)
    sig_jk  = np.sqrt((Nc - 1) * np.mean((C_jk - mean_jk) ** 2, axis=0))
    return C_full, sig_jk


# ----------------------------------------------------------------------
# Effective mass (cosh form because of periodic BC)
# ----------------------------------------------------------------------
def m_eff_cosh(C):
    Lt = len(C)
    m = np.full(Lt, np.nan)
    for tau in range(1, Lt - 1):
        if C[tau] == 0: continue
        arg = (C[tau - 1] + C[tau + 1]) / (2.0 * C[tau])
        if arg > 1:
            m[tau] = np.arccosh(arg)
    return m


def plateau_fit(m, sigma_m, t_min, t_max):
    """Constant fit weighted by 1/sigma^2. Return (mean, error)."""
    mask = np.arange(len(m))
    in_window = (mask >= t_min) & (mask <= t_max) & np.isfinite(m) & np.isfinite(sigma_m) & (sigma_m > 0)
    if not in_window.any():
        return float("nan"), float("nan")
    m_w = m[in_window]; s_w = sigma_m[in_window]
    w = 1.0 / s_w**2
    m_bar  = (w * m_w).sum() / w.sum()
    s_bar  = 1.0 / np.sqrt(w.sum())
    return float(m_bar), float(s_bar)


# ----------------------------------------------------------------------
# sigma a^2 from Phase 3 (re-read summary.txt)
# ----------------------------------------------------------------------
def read_sigma_a2(beta):
    """Return (sigma_a2, err) for beta or (None, None)."""
    p = RES_PHASE3 / "summary.txt"
    if not p.exists(): return None, None
    for line in p.read_text().splitlines():
        if line.startswith("#"): continue
        parts = line.split()
        if not parts: continue
        if parts[0] == beta and len(parts) >= 9:
            try:
                return float(parts[7]), float(parts[8])
            except Exception:
                return None, None
    return None, None


# ----------------------------------------------------------------------
# Per-beta analysis
# ----------------------------------------------------------------------
def analyze_beta(beta):
    tag = beta.replace(".", "")
    bdir = RES_PHASE4 / f"b{tag}"
    if not bdir.exists(): return None
    O_list = []
    for xml in sorted(bdir.glob("glue_*.out.xml")):
        # require log to confirm success
        log = bdir / xml.stem.replace(".out", "") / ""  # not used
        log_path = bdir / xml.name.replace(".out.xml", ".log")
        try:
            if "ran successfully" not in log_path.read_text()[-500:]:
                continue
        except Exception:
            continue
        O = parse_glueball_xml(xml)
        if O is not None: O_list.append(O)
    if not O_list: return None
    O_arr = np.stack(O_list)   # (N_cfg, Lt)
    Nc, Lt = O_arr.shape
    print(f"\n=== β = {beta}  ({Nc} configs, Lt={Lt}) ===")

    C, sigC = jackknife_correlator(O_arr)
    print("  C(tau) (first 6):")
    for tau in range(min(6, Lt)):
        print(f"    τ={tau}: {C[tau]:+.4e} ± {sigC[tau]:.2e}")

    m = m_eff_cosh(C)
    # propagate to m_eff error via finite-difference jackknife (coarse approx)
    # Use C jackknife sigma directly to get sigma_m via local linearisation.
    sigm = np.full(Lt, np.nan)
    for tau in range(1, Lt - 1):
        if not np.isfinite(m[tau]) or C[tau] == 0: continue
        # ∂(m)/∂(C[tau-1]) and ∂(m)/∂(C[tau+1]) at first order
        # m = arccosh((Cp + Cm) / (2 C))
        Cp = C[tau + 1]; Cm = C[tau - 1]; C0 = C[tau]
        arg = (Cp + Cm) / (2.0 * C0)
        if arg <= 1: continue
        denom = np.sqrt(arg**2 - 1)
        d_dCm  = 1.0 / (2 * C0 * denom)
        d_dCp  = 1.0 / (2 * C0 * denom)
        d_dC0  = -(Cp + Cm) / (2 * C0**2) / denom
        var = (d_dCm * sigC[tau - 1])**2 + (d_dCp * sigC[tau + 1])**2 + (d_dC0 * sigC[tau])**2
        sigm[tau] = np.sqrt(var)
    print("  m_eff(τ):")
    for tau in range(1, min(7, Lt - 1)):
        if np.isfinite(m[tau]):
            print(f"    τ={tau}: a·m = {m[tau]:.4f} ± {sigm[tau]:.4f}")

    m_glue, m_glue_err = plateau_fit(m, sigm, T_FIT_MIN, T_FIT_MAX)
    print(f"  a·m_0++ (plateau [τ={T_FIT_MIN}..{T_FIT_MAX}]) = {m_glue:.4f} ± {m_glue_err:.4f}")

    # combine with sigma a^2 from Phase 3
    s_a2, s_a2_err = read_sigma_a2(beta)
    ratio = None
    ratio_err = None
    if s_a2 and np.isfinite(m_glue) and s_a2 > 0:
        ratio = m_glue / np.sqrt(s_a2)
        rel = np.sqrt((m_glue_err / m_glue)**2 + (0.5 * s_a2_err / s_a2)**2)
        ratio_err = ratio * rel
        print(f"  σa² = {s_a2:.5f} ± {s_a2_err:.5f}")
        print(f"  m_0++ / √σ = {ratio:.3f} ± {ratio_err:.3f}   "
              f"(Teper 1999 SU(2) = {TEPER_SU2_RATIO:.2f} ± 0.08)")

    return {
        "beta":      beta,
        "Nc":        Nc,
        "am_0pp":    (m_glue, m_glue_err),
        "sigma_a2":  (s_a2, s_a2_err),
        "ratio":     (ratio, ratio_err),
    }


def main():
    rows = []
    for b in BETAS:
        r = analyze_beta(b)
        if r is not None: rows.append(r)
    out = RES_PHASE4 / "glueball_summary.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        f.write("# β   N    a·m_0++   ±err   σa²       ±err     m_0++/√σ   ±err\n")
        for r in rows:
            am, ame = r["am_0pp"]; s, se = r["sigma_a2"]; rt, rte = r["ratio"]
            s_fmt  = f"{s:.5f}"   if s  is not None else "nan"
            se_fmt = f"{se:.5f}"  if se is not None else "nan"
            rt_fmt = f"{rt:.3f}"  if rt is not None else "nan"
            rte_fmt= f"{rte:.3f}" if rte is not None else "nan"
            f.write(f"{r['beta']}  {r['Nc']:3d}  {am:.4f} {ame:.4f}  "
                    f"{s_fmt} {se_fmt}  {rt_fmt} {rte_fmt}\n")
    print(f"\nSummary written to {out}")


if __name__ == "__main__":
    main()
