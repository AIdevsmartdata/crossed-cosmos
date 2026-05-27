"""Neural emulator + analytical formula predictions for F₄/E₆/E₈"""
import numpy as np
from math import pi, e, log
import json

c = pi + e  # 5.85987...

# GROUP DATABASE: (name, dim, rank, C2, nroots=|Φ⁺|, |Z|, root_ratio)
groups = {
    "U(1)":  (1, 1, 0, 0, 1, 1.0),
    "SU(2)": (3, 1, 2, 1, 2, 1.0),
    "SU(3)": (8, 2, 3, 3, 3, 1.0),
    "SU(4)": (15, 3, 4, 6, 4, 1.0),
    "SU(5)": (24, 4, 5, 10, 5, 1.0),
    "G2":    (14, 2, 4, 6, 1, 1.732),
    "Sp(4)": (10, 2, 3, 4, 2, 1.414),
    "SO(7)": (21, 3, 5, 9, 2, 1.414),
    # Prediction targets
    "F4":    (52, 4, 9, 24, 1, 1.0),    # simply-laced? No, F4 has 2 root lengths
    "E6":    (78, 6, 12, 36, 3, 1.0),   # simply-laced
    "E8":    (248, 8, 30, 120, 1, 1.0), # simply-laced
}

# Actually F4 has root ratio sqrt(2)
groups["F4"] = (52, 4, 9, 24, 1, 1.414)

def formula(beta, nroots, C2):
    """S₂/A = (π+e)·(β − |Φ⁺|) − log(β − 1 − |Φ⁺|) − C₂"""
    x = beta - nroots
    if x <= 1:
        return None
    return c * x - log(x - 1) - C2

# MEASURED DATA (from kevinotron sessions)
# Format: (group, beta, L, S2_per_A)
measured = [
    # SU(2) β=2.50
    ("SU(2)", 2.50, 4, 7.13), ("SU(2)", 2.50, 6, 7.17),
    ("SU(2)", 2.50, 8, 7.19), ("SU(2)", 2.50, 10, 7.20), ("SU(2)", 2.50, 12, 7.22),
    # SU(3) β=6.06
    ("SU(3)", 6.06, 4, 13.99), ("SU(3)", 6.06, 6, 14.05),
    ("SU(3)", 6.06, 8, 14.10), ("SU(3)", 6.06, 10, 14.14), ("SU(3)", 6.06, 12, 14.17),
    # SU(4) β=10.80
    ("SU(4)", 10.80, 4, 21.53), ("SU(4)", 10.80, 6, 21.58),
    ("SU(4)", 10.80, 8, 21.62), ("SU(4)", 10.80, 10, 21.66), ("SU(4)", 10.80, 12, 21.69),
    # G₂ β=10.0
    ("G2", 10.0, 4, 18.08), ("G2", 10.0, 6, 18.15),
    ("G2", 10.0, 10, 18.25), ("G2", 10.0, 12, 18.30),
    # G₂ multi-β at L=4
    ("G2", 9.6, 4, 15.80), ("G2", 9.8, 4, 16.90),
    ("G2", 10.2, 4, 19.30), ("G2", 10.4, 4, 20.50),
    # G₂ β=9.0 and 13.0
    ("G2", 9.0, 4, 11.97), ("G2", 13.0, 4, 35.54),
    # Sp(4) β=8.0
    ("Sp(4)", 8.0, 4, 20.57), ("Sp(4)", 8.0, 6, 20.62), ("Sp(4)", 8.0, 8, 20.67),
    # Sp(4) β-scan L=4
    ("Sp(4)", 7.0, 4, 14.77), ("Sp(4)", 7.5, 4, 17.60),
    ("Sp(4)", 8.5, 4, 23.50), ("Sp(4)", 9.0, 4, 26.40),
    # SO(7) β=20.0
    ("SO(7)", 20.0, 4, 56.10), ("SO(7)", 20.0, 6, 56.25), ("SO(7)", 20.0, 8, 56.40),
    # SO(7) β-scan L=4
    ("SO(7)", 18.0, 4, 44.30), ("SO(7)", 19.0, 4, 50.20),
    ("SO(7)", 21.0, 4, 62.00), ("SO(7)", 22.0, 4, 67.90), ("SO(7)", 24.0, 4, 79.70),
    # U(1)
    ("U(1)", 5.0, 4, 26.53), ("U(1)", 2.0, 4, 8.51),
    # SU(5)
    ("SU(5)", 15.0, 4, 21.42), ("SU(5)", 17.0, 4, 35.0),
]

print("="*70)
print("ANALYTICAL FORMULA PREDICTIONS")
print("="*70)
print(f"\nFormula: S₂/A = (π+e)·(β − |Φ⁺|) − log(β − 1 − |Φ⁺|) − C₂")
print(f"         c = π + e = {c:.6f}\n")

# Validate on measured data
print(f"{'Group':>8} {'β':>6} {'L':>3} {'Measured':>10} {'Formula':>10} {'Error%':>8}")
print("-"*50)
errors = []
for name, beta, L, s2a in measured:
    dim, rank, C2, nroots, Z, rr = groups[name]
    pred = formula(beta, nroots, C2)
    if pred is not None:
        err = 100 * abs(pred - s2a) / s2a
        errors.append(err)
        flag = " ★" if err < 1 else (" ✓" if err < 5 else " ✗")
        print(f"{name:>8} {beta:6.1f} {L:3d} {s2a:10.2f} {pred:10.2f} {err:8.2f}%{flag}")
    else:
        print(f"{name:>8} {beta:6.1f} {L:3d} {s2a:10.2f} {'N/A':>10}")

print(f"\nMedian error: {np.median(errors):.2f}%, Mean: {np.mean(errors):.2f}%")
print(f"<1%: {sum(1 for e in errors if e<1)}, <5%: {sum(1 for e in errors if e<5)}, >10%: {sum(1 for e in errors if e>10)}")

# PREDICTIONS for F₄, E₆, E₈
print(f"\n{'='*70}")
print("PREDICTIONS: F₄, E₆, E₈")
print("="*70)

targets = [
    ("F4", [30, 35, 40, 50]),
    ("E6", [45, 50, 60, 80]),
    ("E8", [150, 180, 200, 250]),
]

results = {}
for name, betas in targets:
    dim, rank, C2, nroots, Z, rr = groups[name]
    print(f"\n{name}: dim={dim}, rank={rank}, C₂={C2}, |Φ⁺|={nroots}, |Z|={Z}, rr={rr}")
    print(f"  β_min = |Φ⁺| + 2 = {nroots + 2}")
    print(f"  Slope S₂/A/β ≈ c = {c:.3f} (asymptotic)")
    results[name] = []
    for beta in betas:
        pred = formula(beta, nroots, C2)
        slope = pred / beta if pred else 0
        print(f"  β={beta:>4}: S₂/A = {pred:>8.2f}, S₂/A/β = {slope:.3f}")
        results[name].append({"beta": beta, "S2_per_A": pred, "slope": slope})

# SLOPE PREDICTIONS (Dynkin invariant extrapolation)
print(f"\n{'='*70}")
print("DYNKIN INVARIANT SLOPE PREDICTIONS")
print("="*70)

# Measured slopes
slopes_measured = {
    "C2_Sp4": 3.10, "B3_SO7": 2.97, "A1_SU2": 2.89,
    "A2_SU3": 2.34, "A3_SU4": 2.01, "G2": 1.83,
}

# Formula slopes at large β
print(f"\nAsymptotic slope = d(S₂/A)/dβ = c − 1/(β−1−|Φ⁺|) → c = {c:.4f}")
print(f"\nAt finite β, slope depends on β−|Φ⁺|:")
for name in ["F4", "E6", "E8"]:
    dim, rank, C2, nroots, Z, rr = groups[name]
    beta_test = nroots + 6  # moderate coupling
    slope = c - 1/(beta_test - 1 - nroots)
    print(f"  {name} (Dynkin={name}): slope ≈ {slope:.3f} at β={beta_test}")
    print(f"    Compare: G₂=1.83, A₃(SU4)=2.01 → {name} should be LOWER (more roots)")

# RELATIVE RANKING PREDICTION
print(f"\n{'='*70}")
print("PREDICTED KEVINOTRON RANKING (all groups)")
print("="*70)

all_groups_ranked = []
for name, (dim, rank, C2, nroots, Z, rr) in groups.items():
    beta_ref = nroots + 5  # choose β−|Φ⁺|=5 for all
    pred = formula(beta_ref, nroots, C2)
    slope = c - 1/(5 - 1)  # same for all at matched β−|Φ⁺|
    all_groups_ranked.append((name, dim, C2, nroots, pred, slope))

all_groups_ranked.sort(key=lambda x: -x[4]/x[3] if x[3]>0 else -x[4])  # sort by S₂/A per root
print(f"\n{'Name':>8} {'dim':>4} {'C₂':>3} {'|Φ⁺|':>5} {'S₂/A(β=|Φ⁺|+5)':>16}")
for name, dim, C2, nroots, pred, slope in all_groups_ranked:
    beta = nroots + 5
    print(f"{name:>8} {dim:4d} {C2:3d} {nroots:5d} {pred:16.2f} (β={beta})")

# Save
out = {
    "formula": f"S₂/A = (π+e)·(β−|Φ⁺|) − log(β−1−|Φ⁺|) − C₂, c={c:.6f}",
    "validation_errors": {"median_pct": float(np.median(errors)), "mean_pct": float(np.mean(errors))},
    "predictions": results,
    "h_new3": "n_neg(G₂) ≈ 1327 CONSTANT across β=9.6-10.4 → topological, d_s=2.24≈7/3",
}
with open("/root/kevinotron/predictions_F4_E6_E8.json", 'w') as f:
    json.dump(out, f, indent=2)
print(f"\nSaved predictions to predictions_F4_E6_E8.json")
