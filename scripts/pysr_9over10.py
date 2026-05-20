#!/usr/bin/env python3
"""PySR symbolic regression — find closed‑form expression for c=0.9 in F(N)=c·(1+1/N²)

Input:  invariant_dataset_9over10.csv (from PARI)
Output: candidate formulas for c = 9/10

Piste 1 du plan ML 9/10.
"""

import pandas as pd
import numpy as np
from pysr import PySRRegressor

# ── Load PARI dataset ──────────────────────────────────────────────────────
df = pd.read_csv("/tmp/invariant_dataset.csv")

# Features: all invariants except D, hK_target
feature_cols = [
    "h_K", "rk2", "zK2", "Vol", "Lchi1", "zeta_ratio"
]
X = df[feature_cols].values.astype(np.float64)

# Target: F(N) = (9/10)(N²+1)/N² evaluated at h_K
# We want to RECOVER this formula from invariants
y = df["FN_target"].values.astype(np.float64)

# Filter: only rows where h_K ∈ {1,2,3,4,5,6} (the lattice anchors)
# plus h_K large for extrapolation test
mask_anchors = df["h_K_target"].isin([1, 2, 3, 4, 5, 6])
mask_large = df["h_K_target"] >= 7
mask = mask_anchors | mask_large

X_train = X[mask]
y_train = y[mask]

print(f"Training points: {len(y_train)} (anchors: {mask_anchors.sum()}, large: {mask_large.sum()})")
print(f"Features: {feature_cols}")
print()

# ── PySR symbolic regression ──────────────────────────────────────────────
model = PySRRegressor(
    niterations=100,           # genetic algorithm iterations
    populations=30,            # parallel populations
    binary_operators=["+", "-", "*", "/", "^"],
    unary_operators=[
        "sqrt", "log", "exp", "abs",
        "sin", "cos",           # periodic (catch modular forms)
    ],
    constraints={
        "^": (4, -1),           # allow x^(1/2), x^(1/3) etc.
    },
    model_selection="best",     # pick best Pareto front
    loss="L2",                  # squared error
    maxsize=30,                 # max expression complexity
    ncycles_per_iteration=500,
    procs=4,                    # parallel CPU
)

print("Running PySR...")
model.fit(X_train, y_train)

# ── Results ────────────────────────────────────────────────────────────────
print()
print("=== BEST EQUATIONS ===")
print(model.sympy())

# Check if 9/10 emerges as a simple expression
for i, eq in enumerate(model.equations_[:5]):
    print(f"\nEq #{i}: {eq['equation']}")
    print(f"  Loss: {eq['loss']:.6f}, Complexity: {eq['complexity']}")

# ── Verification: check candidate formulas ────────────────────────────────
print()
print("=== VERIFICATION ===")
print("Expected: F(N) = 0.9 * (N²+1)/N²")
print("At N=3: F=1.0, N=∞: F=0.9")
print()
print("Candidate closed-form expressions for c=0.9:")
print("  (1) c = 3²/(3²+1) = 9/10  — normalization artifact")
print("  (2) c = Z_0(3)/(Z_0(3)+Z_1)  — DW genus at SU(3)")
print("  (3) c = ?  — to be discovered by PySR")
