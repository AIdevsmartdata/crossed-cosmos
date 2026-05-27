"""
kevinotron_dataset.py — Compile ALL measurements into one dataset.
This is the input for PySR, the Decoder Graph updater, and tension analysis.

LOOP: Kevinotron → Dataset → PySR → Graph → Hypotheses → Kevinotron
"""
import json
import numpy as np

# ═══════════════════════════════════════════════
# GROUP DATABASE — all Lie-algebraic invariants
# ═══════════════════════════════════════════════

GROUPS = {
    "U1":  {"d_fund":1,  "d_adj":0,  "phi":0,  "hv":0,  "Z":1, "rank":1, "rr":1.0,   "type":"abelian"},
    "SU2": {"d_fund":2,  "d_adj":3,  "phi":1,  "hv":2,  "Z":2, "rank":1, "rr":1.0,   "type":"A1"},
    "SU3": {"d_fund":3,  "d_adj":8,  "phi":3,  "hv":3,  "Z":3, "rank":2, "rr":1.0,   "type":"A2"},
    "SU4": {"d_fund":4,  "d_adj":15, "phi":6,  "hv":4,  "Z":4, "rank":3, "rr":1.0,   "type":"A3"},
    "SU5": {"d_fund":5,  "d_adj":24, "phi":10, "hv":5,  "Z":5, "rank":4, "rr":1.0,   "type":"A4"},
    "G2":  {"d_fund":7,  "d_adj":14, "phi":6,  "hv":4,  "Z":1, "rank":2, "rr":1.732, "type":"G2"},
    "Sp4": {"d_fund":4,  "d_adj":10, "phi":4,  "hv":3,  "Z":2, "rank":2, "rr":1.414, "type":"C2"},
    "SO7": {"d_fund":7,  "d_adj":21, "phi":9,  "hv":5,  "Z":2, "rank":3, "rr":1.414, "type":"B3"},
    "F4":  {"d_fund":26, "d_adj":52, "phi":24, "hv":9,  "Z":1, "rank":4, "rr":1.414, "type":"F4"},
    "E6":  {"d_fund":27, "d_adj":78, "phi":36, "hv":12, "Z":3, "rank":6, "rr":1.0,   "type":"E6"},
}

# ═══════════════════════════════════════════════
# ALL MEASUREMENTS — from this session + prior
# ═══════════════════════════════════════════════

MEASUREMENTS = [
    # (group, beta, L, Lt, observable, value, error, source)
    # EE measurements
    ("SU2", 2.50, 4, 8, "S2_per_A", 7.20, 0.15, "kevinotron_v1"),
    ("SU3", 5.80, 4, 8, "S2_per_A", 12.71, 0.02, "multi_beta"),
    ("SU3", 6.00, 4, 8, "S2_per_A", 13.91, 0.02, "multi_beta"),
    ("SU3", 6.06, 4, 8, "S2_per_A", 14.00, 0.15, "kevinotron_v1"),
    ("SU3", 6.20, 4, 8, "S2_per_A", 14.94, 0.02, "multi_beta"),
    ("SU3", 6.40, 4, 8, "S2_per_A", 16.13, 0.02, "multi_beta"),
    ("SU4", 10.80, 4, 8, "S2_per_A", 21.60, 0.15, "kevinotron_v1"),
    ("SU5", 15.00, 4, 8, "S2_per_A", 21.42, 0.15, "kevinotron_v1"),
    ("G2",  10.00, 4, 8, "S2_per_A", 18.10, 0.15, "kevinotron_v1"),
    ("Sp4", 8.00,  4, 8, "S2_per_A", 20.60, 0.15, "kevinotron_v1"),
    ("SO7", 20.00, 4, 8, "S2_per_A", 56.10, 0.15, "kevinotron_v1"),
    ("F4",  30.00, 4, 8, "S2_per_A", 101.78, 0.32, "worldfirst"),
    ("F4",  35.00, 4, 8, "S2_per_A", 125.61, 0.32, "beta_scan"),
    ("F4",  40.00, 4, 8, "S2_per_A", 151.01, 0.38, "beta_scan"),
    ("E6",  45.00, 4, 8, "S2_per_A", 194.58, 0.48, "worldfirst"),
    ("U1",  5.00,  4, 8, "S2_per_A", 26.53, 0.15, "kevinotron_v1"),

    # Polyakov loop
    ("SU3", 6.06, 4, 8, "polyakov_mod", 0.271, 0.01, "v3"),
    ("G2",  10.00, 4, 8, "polyakov_mod", 0.188, 0.01, "v3"),
    ("F4",  10.00, 4, 8, "polyakov_mod", 0.035, 0.01, "v3"),
    ("E6",  45.00, 4, 8, "polyakov_mod", 0.587, 0.01, "worldfirst"),

    # Topological charge
    ("SU3", 6.06, 4, 8, "Q_topo", 0.030, 0.05, "v3"),
    ("G2",  10.00, 4, 8, "Q_topo", 0.015, 0.05, "v3"),
    ("E6",  45.00, 4, 8, "Q_topo", -0.023, 0.05, "worldfirst"),

    # Plaquette
    ("SU3", 6.06, 4, 8, "plaquette", 0.611, 0.01, "v3"),
    ("G2",  10.00, 4, 8, "plaquette", 0.755, 0.01, "v3"),
    ("F4",  30.00, 4, 8, "plaquette", 0.713, 0.01, "worldfirst"),
    ("E6",  45.00, 4, 8, "plaquette", 0.787, 0.01, "worldfirst"),

    # FP spectral (post-bugfix: ALL n_neg=0)
    ("SU2", 2.50, 4, 8, "fp_gap", 1.788, 0.01, "fixed"),
    ("SU3", 6.06, 4, 8, "fp_gap", 1.645, 0.01, "fixed"),
    ("G2",  10.00, 4, 8, "fp_gap", 1.757, 0.01, "fixed"),
    ("Sp4", 8.00, 4, 8, "fp_gap", 1.246, 0.01, "fixed"),
    ("SO7", 20.00, 4, 8, "fp_gap", 0.937, 0.01, "fixed"),
    ("F4",  30.00, 4, 8, "fp_gap", 1.024, 0.01, "fixed"),

    # FP spectral dimension
    ("SU2", 2.50, 4, 8, "fp_ds", 5.96, 0.17, "fixed"),
    ("SU3", 6.06, 4, 8, "fp_ds", 5.87, 0.17, "fixed"),
    ("G2",  10.00, 4, 8, "fp_ds", 5.98, 0.17, "fixed"),
    ("Sp4", 8.00, 4, 8, "fp_ds", 5.63, 0.17, "fixed"),
    ("SO7", 20.00, 4, 8, "fp_ds", 4.91, 0.17, "fixed"),
    ("F4",  30.00, 4, 8, "fp_ds", 5.07, 0.17, "fixed"),

    # Creutz ratio SU(3)
    ("SU3", 6.06, 8, 16, "creutz_44", 0.043, 0.005, "kevinotron_v1"),

    # Thermal scan SU(2) β=2.3
    ("SU2", 2.30, 8, 2, "polyakov_mod", 0.644, 0.02, "thermal"),
    ("SU2", 2.30, 8, 3, "polyakov_mod", 0.498, 0.02, "thermal"),
    ("SU2", 2.30, 8, 4, "polyakov_mod", 0.440, 0.02, "thermal"),
    ("SU2", 2.30, 8, 5, "polyakov_mod", 0.424, 0.02, "thermal"),
    ("SU2", 2.30, 8, 6, "polyakov_mod", 0.426, 0.02, "thermal"),
    ("SU2", 2.30, 8, 12, "polyakov_mod", 0.423, 0.02, "thermal"),

    # HMC acceptance rates
    ("SU2", 2.30, 4, 8, "hmc_acceptance", 0.37, 0.05, "hmc_dt0.02"),
    ("SU3", 6.00, 4, 8, "hmc_acceptance", 0.88, 0.05, "hmc_dt0.005"),
    ("G2",  10.00, 4, 8, "hmc_acceptance", 0.92, 0.05, "hmc_dt0.003"),

    # Fermion γ₅-hermiticity
    ("SU2", 10.00, 4, 8, "g5_herm_err", 3.03e-15, 0, "fermion"),
    ("SU3", 6.06, 4, 8, "g5_herm_err", 2.84e-15, 0, "fermion"),
    ("G2",  10.00, 4, 8, "g5_herm_err", 7.00e-15, 0, "fermion"),
    ("Sp4", 8.00, 4, 8, "g5_herm_err", 6.43e-15, 0, "fermion"),
    ("F4",  10.00, 4, 8, "g5_herm_err", 3.61e-14, 0, "fermion"),
]

# ═══════════════════════════════════════════════
# BUILD FLAT TABLE FOR PySR
# ═══════════════════════════════════════════════

from math import pi, e, log

rows = []
for group, beta, L, Lt, obs, val, err, src in MEASUREMENTS:
    g = GROUPS[group]
    # Formula prediction
    x = beta - g["phi"]
    formula = (pi+e)*x - log(x-1) - g["hv"] if x > 1 else None
    beta_c = g["phi"] + 1
    
    row = {
        "group": group,
        "type": g["type"],
        "d_fund": g["d_fund"],
        "d_adj": g["d_adj"],
        "phi_plus": g["phi"],
        "h_dual": g["hv"],
        "center_Z": g["Z"],
        "rank": g["rank"],
        "root_ratio": g["rr"],
        "beta": beta,
        "beta_c": beta_c,
        "beta_over_beta_c": beta / beta_c if beta_c > 0 else beta,
        "L": L,
        "Lt": Lt,
        "observable": obs,
        "value": val,
        "error": err,
        "source": src,
        "formula_pred": formula,
    }
    rows.append(row)

# Save as JSON
with open("/root/kevinotron/kevinotron_dataset.json", "w") as f:
    json.dump(rows, f, indent=2)

# Summary
obs_counts = {}
for r in rows:
    obs_counts[r["observable"]] = obs_counts.get(r["observable"], 0) + 1

print(f"KEVINOTRON DATASET: {len(rows)} measurements")
print(f"  {len(GROUPS)} groups, {len(obs_counts)} observable types")
print()
for obs, count in sorted(obs_counts.items()):
    print(f"  {obs:.<25} {count:>3} measurements")

# PySR-ready CSV for S2/A specifically
print(f"\n=== PySR-READY: S2/A dataset ===")
s2a_rows = [r for r in rows if r["observable"] == "S2_per_A"]
print(f"  {len(s2a_rows)} S2/A data points across {len(set(r['group'] for r in s2a_rows))} groups")

# Tensions / anomalies
print(f"\n=== TENSIONS ===")
for r in s2a_rows:
    if r["formula_pred"] is not None:
        ratio = r["value"] / r["formula_pred"]
        if abs(ratio - 1.0) > 0.1:
            print(f"  {r['group']:>4} β={r['beta']:>5.1f}: measured={r['value']:.1f} formula={r['formula_pred']:.1f} ratio={ratio:.2f}")

# Missing measurements
print(f"\n=== GAPS (what to measure next) ===")
measured_groups = set(r["group"] for r in rows if r["observable"] == "S2_per_A")
measured_fp = set(r["group"] for r in rows if r["observable"] == "fp_gap")
measured_poly = set(r["group"] for r in rows if r["observable"] == "polyakov_mod" and r["Lt"] == 8)
measured_hmc = set(r["group"] for r in rows if r["observable"] == "hmc_acceptance")

for g in GROUPS:
    gaps = []
    if g not in measured_fp: gaps.append("fp_gap")
    if g not in measured_poly: gaps.append("polyakov")
    if g not in measured_hmc: gaps.append("hmc")
    if gaps:
        print(f"  {g:>4}: missing {', '.join(gaps)}")
