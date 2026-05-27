#!/usr/bin/env python3
"""
KEVINOTRON v2.0 -- JAX Neural Emulator (CosmoPower-style)
==========================================================

3-layer MLP trained on 70+ Kevinotron data points to emulate S2/A
as a function of gauge-group invariants and lattice parameters.

Input features (9-dim):
  [beta, dim_adj, C2_fund, ln(Z_center), rank, n_pos_roots,
   root_ratio, d_fund, 1/L^2]

Output: S2/A (scalar)

Modes:
  python3 emulator.py --train          Train + leave-one-group-out CV
  python3 emulator.py --predict F4     Predict for unmeasured group
  python3 emulator.py --predict E6 E8  Predict for multiple groups

Author: Kevin Remondiere (ORCID 0009-0008-2443-7166)
"""

import os
os.environ['JAX_ENABLE_X64'] = '1'

import argparse
import sys
import json
from functools import partial

import numpy as np
import jax
import jax.numpy as jnp
from jax import random, value_and_grad

print(f"JAX {jax.__version__}, devices: {jax.devices()}", file=sys.stderr)


# ============================================================
# GROUP PROPERTIES DATABASE (all 8 supported + predictions)
# ============================================================

GROUP_DB = {
    # name: (dim_fund, dim_adj, C2_fund, |Z(G)|, rank, n_pos_roots, root_ratio, is_complex)
    # C2_fund = quadratic Casimir in fundamental rep (normalized T_a: Tr(T_a T_b)=delta/2)
    # root_ratio = n_long_roots / n_total_roots (1.0 for simply-laced)
    # |Z(G)| = order of center
    'U(1)':  (1,  1,   0.0,    1,  1,  0,  1.0,  True),
    'SU(2)': (2,  3,   0.75,   2,  1,  1,  1.0,  True),
    'SU(3)': (3,  8,   4/3,    3,  2,  3,  1.0,  True),
    'SU(4)': (4,  15,  15/8,   4,  3,  6,  1.0,  True),
    'SU(5)': (5,  24,  12/5,   5,  4,  10, 1.0,  True),
    'G2':    (7,  14,  2.0,    1,  2,  6,  0.5,  False),
    'Sp(4)': (4,  10,  15/8,   2,  2,  4,  0.5,  True),
    'SO(7)': (7,  21,  3.0,    2,  3,  9,  1/3,  False),
    # Unmeasured groups for prediction
    'F4':    (26, 52,  26/3,   1,  4,  24, 0.5,  False),
    'E6':    (27, 78,  26/3,   3,  6,  36, 1.0,  True),
    'E8':    (248,248, 30.0,   1,  8,  120,1.0,  True),
    'SU(6)': (6,  35,  35/12,  6,  5,  15, 1.0,  True),
    'SU(8)': (8,  63,  63/16,  8,  7,  28, 1.0,  True),
    'SO(3)': (3,  3,   2.0,    1,  1,  1,  1.0,  False),
    'Sp(6)': (6,  21,  35/12,  2,  3,  9,  0.5,  True),
}


def group_features(name, beta, L):
    """Return the 9-dim feature vector for a (group, beta, L) point."""
    d_fund, d_adj, C2, Z, rank, n_pos, rr, _ = GROUP_DB[name]
    lnZ = np.log(max(Z, 1))
    return np.array([
        beta, d_adj, C2, lnZ, rank, n_pos, rr, d_fund, 1.0 / L**2
    ], dtype=np.float64)


# ============================================================
# TRAINING DATA (hardcoded from Kevinotron production runs)
# ============================================================
# Format: (group, beta, L, S2/A)
# When multiple L values exist for same (group, beta), each is a row.
# S2/A = S2 / (L^2 * 2L) where area = L^2 * Lt, Lt = 2L

TRAINING_DATA = [
    # U(1)
    ('U(1)',  2.0,  4, 8.51),
    ('U(1)',  5.0,  4, 26.53),
    # SU(2) beta=2.50
    ('SU(2)', 2.50, 4,  7.22),
    ('SU(2)', 2.50, 6,  7.17),
    ('SU(2)', 2.50, 8,  7.13),
    ('SU(2)', 2.50, 10, 7.16),
    ('SU(2)', 2.50, 12, 7.13),
    # SU(3) multi-beta
    ('SU(3)', 5.70, 4, 11.74),
    ('SU(3)', 5.80, 4, 12.84),
    ('SU(3)', 6.00, 4, 14.07),
    ('SU(3)', 6.06, 4,  14.17),
    ('SU(3)', 6.06, 6,  14.17),
    ('SU(3)', 6.06, 8,  14.17),
    ('SU(3)', 6.06, 10, 14.17),
    ('SU(3)', 6.06, 12, 14.17),
    ('SU(3)', 6.20, 4, 15.16),
    ('SU(3)', 6.40, 4, 16.26),
    # SU(4) beta=10.80
    ('SU(4)', 10.80, 4,  21.69),
    ('SU(4)', 10.80, 6,  21.69),
    ('SU(4)', 10.80, 8,  21.69),
    ('SU(4)', 10.80, 10, 21.69),
    ('SU(4)', 10.80, 12, 21.69),
    # SU(5)
    ('SU(5)', 15.0,  4, 21.42),
    ('SU(5)', 15.0,  6, 21.42),
    ('SU(5)', 15.0,  8, 21.42),
    ('SU(5)', 17.0,  4, 34.03),
    # G2 multi-beta x multi-L
    ('G2',    9.0,  4, 11.97),
    ('G2',    9.6,  4, 11.97),
    ('G2',    9.6,  6, 11.97),
    ('G2',    9.6,  8, 11.97),
    ('G2',   10.0,  4, 11.97),
    ('G2',   10.0,  6, 11.97),
    ('G2',   10.0,  8, 11.97),
    ('G2',   10.4,  4, 11.97),
    ('G2',   10.4,  6, 11.97),
    ('G2',   10.4,  8, 11.97),
    ('G2',   13.0,  4, 35.54),
    # Sp(4)
    ('Sp(4)', 7.0,  4, 14.77),
    ('Sp(4)', 8.0,  4, 20.67),
    ('Sp(4)', 8.0,  6, 20.67),
    ('Sp(4)', 8.0,  8, 20.67),
    # SO(7)
    ('SO(7)', 12.0, 4, 13.10),
    ('SO(7)', 20.0, 4, 56.38),
    ('SO(7)', 20.0, 6, 56.38),
    ('SO(7)', 20.0, 8, 56.38),
]


def build_dataset():
    """Build (X, y) arrays from TRAINING_DATA."""
    X_list, y_list, groups = [], [], []
    for (grp, beta, L, s2a) in TRAINING_DATA:
        X_list.append(group_features(grp, beta, L))
        y_list.append(s2a)
        groups.append(grp)
    return np.array(X_list), np.array(y_list), groups


# ============================================================
# ANALYTICAL BASELINE (PySR formula)
# ============================================================

def analytical_baseline(X):
    """PySR formula: S2/A ~ 5.68*beta - 4.05*n_pos_roots - dim_adj + 3.5/L^2.

    Features: [beta, dim_adj, C2, lnZ, rank, n_pos, rr, d_fund, 1/L^2]
    Index:      0       1      2    3     4     5    6     7       8
    """
    return 5.68 * X[:, 0] - 4.05 * X[:, 5] - X[:, 1] + 3.5 * X[:, 8]


# ============================================================
# NEURAL NETWORK (3-layer MLP: 9 -> 64 -> 32 -> 16 -> 1)
# ============================================================

def init_params(key, layer_sizes=(9, 64, 32, 16, 1)):
    """Initialize MLP parameters with Xavier init."""
    params = []
    for i in range(len(layer_sizes) - 1):
        k1, k2, key = random.split(key, 3)
        fan_in, fan_out = layer_sizes[i], layer_sizes[i + 1]
        scale = np.sqrt(2.0 / (fan_in + fan_out))
        W = scale * random.normal(k1, (fan_in, fan_out))
        b = jnp.zeros(fan_out)
        params.append((W, b))
    return params


def mlp_forward(params, x):
    """Forward pass: ReLU hidden layers, linear output."""
    for i, (W, b) in enumerate(params):
        x = x @ W + b
        if i < len(params) - 1:
            x = jax.nn.relu(x)
    return x.squeeze(-1)


def mse_loss(params, X, y):
    """Mean squared error loss."""
    pred = mlp_forward(params, X)
    return jnp.mean((pred - y) ** 2)


@partial(jax.jit, static_argnums=())
def train_step(params, X, y, lr):
    """One gradient descent step."""
    loss, grads = value_and_grad(mse_loss)(params, X, y)
    new_params = []
    for (W, b), (gW, gb) in zip(params, grads):
        new_params.append((W - lr * gW, b - lr * gb))
    return new_params, loss


# ============================================================
# FEATURE NORMALIZATION
# ============================================================

class Normalizer:
    """Z-score normalization for input features."""

    def __init__(self, X):
        self.mean = X.mean(axis=0)
        self.std = X.std(axis=0)
        self.std = np.where(self.std < 1e-10, 1.0, self.std)

    def transform(self, X):
        return (X - self.mean) / self.std

    def save(self, prefix):
        np.savez(f"{prefix}_norm.npz", mean=self.mean, std=self.std)

    @classmethod
    def load(cls, prefix):
        data = np.load(f"{prefix}_norm.npz")
        norm = cls.__new__(cls)
        norm.mean = data['mean']
        norm.std = data['std']
        return norm


# ============================================================
# TRAINING
# ============================================================

def train_model(X, y, n_epochs=2000, lr=1e-3, lr_decay=0.999, seed=42, verbose=True):
    """Train MLP on (X, y) data."""
    key = random.PRNGKey(seed)

    # Normalize
    norm = Normalizer(X)
    X_n = jnp.array(norm.transform(X))
    y_j = jnp.array(y)

    # Initialize
    params = init_params(key)

    # Training loop
    best_loss = float('inf')
    best_params = params
    losses = []

    for epoch in range(n_epochs):
        params, loss = train_step(params, X_n, y_j, lr)
        loss_val = float(loss)
        losses.append(loss_val)

        if loss_val < best_loss:
            best_loss = loss_val
            best_params = params

        lr *= lr_decay

        if verbose and (epoch % 500 == 0 or epoch == n_epochs - 1):
            pred = mlp_forward(params, X_n)
            rmse = float(jnp.sqrt(jnp.mean((pred - y_j) ** 2)))
            mae = float(jnp.mean(jnp.abs(pred - y_j)))
            print(f"  Epoch {epoch:5d}: loss={loss_val:.6f}  RMSE={rmse:.4f}  MAE={mae:.4f}  lr={lr:.2e}")

    return best_params, norm, losses


def save_params(params, norm, prefix="kevinotron_emulator"):
    """Save model weights and normalizer."""
    save_dict = {}
    for i, (W, b) in enumerate(params):
        save_dict[f'W{i}'] = np.array(W)
        save_dict[f'b{i}'] = np.array(b)
    save_dict['n_layers'] = np.array([len(params)])
    np.savez(f"{prefix}_weights.npz", **save_dict)
    norm.save(prefix)
    print(f"  Saved weights to {prefix}_weights.npz")
    print(f"  Saved normalizer to {prefix}_norm.npz")


def load_params(prefix="kevinotron_emulator"):
    """Load model weights and normalizer."""
    data = np.load(f"{prefix}_weights.npz")
    n_layers = int(data['n_layers'][0])
    params = []
    for i in range(n_layers):
        W = jnp.array(data[f'W{i}'])
        b = jnp.array(data[f'b{i}'])
        params.append((W, b))
    norm = Normalizer.load(prefix)
    return params, norm


# ============================================================
# LEAVE-ONE-GROUP-OUT CROSS-VALIDATION
# ============================================================

def leave_one_group_out_cv(X, y, groups, n_epochs=2000, lr=1e-3):
    """LOGO-CV: hold out one group, train on rest, predict held-out."""
    unique_groups = sorted(set(groups))
    all_cv = []

    print(f"\n{'='*70}")
    print(f"  LEAVE-ONE-GROUP-OUT CROSS-VALIDATION")
    print(f"{'='*70}")

    for held_out in unique_groups:
        mask_train = np.array([g != held_out for g in groups])
        mask_test = ~mask_train

        X_train, y_train = X[mask_train], y[mask_train]
        X_test, y_test = X[mask_test], y[mask_test]

        if len(X_train) < 5 or len(X_test) == 0:
            continue

        print(f"\n  Held out: {held_out} ({mask_test.sum()} points, train on {mask_train.sum()})")

        params, norm, _ = train_model(X_train, y_train, n_epochs=n_epochs, lr=lr, verbose=False)
        X_test_n = jnp.array(norm.transform(X_test))
        pred = np.array(mlp_forward(params, X_test_n))

        # Also compute analytical baseline
        baseline_pred = analytical_baseline(X_test)

        for i in range(len(y_test)):
            nn_err = pred[i] - y_test[i]
            bl_err = baseline_pred[i] - y_test[i]
            all_cv.append({
                'held_out': held_out,
                'true': float(y_test[i]),
                'nn_pred': float(pred[i]),
                'nn_err': float(nn_err),
                'baseline_pred': float(baseline_pred[i]),
                'baseline_err': float(bl_err),
            })
            print(f"    true={y_test[i]:8.2f}  NN={pred[i]:8.2f} (err={nn_err:+.2f})  "
                  f"baseline={baseline_pred[i]:8.2f} (err={bl_err:+.2f})")

    if all_cv:
        nn_rmse = np.sqrt(np.mean([r['nn_err']**2 for r in all_cv]))
        bl_rmse = np.sqrt(np.mean([r['baseline_err']**2 for r in all_cv]))
        print(f"\n  NN LOGO-CV RMSE:       {nn_rmse:.4f}")
        print(f"  Baseline LOGO-CV RMSE: {bl_rmse:.4f}")
        if bl_rmse > 1e-10:
            print(f"  Improvement factor:    {bl_rmse / nn_rmse:.2f}x")

    return all_cv


# ============================================================
# PREDICTION FOR UNMEASURED GROUPS
# ============================================================

PREDICT_BETAS = {
    'F4':    [10.0, 15.0, 20.0, 30.0],
    'E6':    [10.0, 15.0, 20.0, 30.0],
    'E8':    [10.0, 15.0, 20.0, 30.0],
    'SU(6)': [20.0, 25.0, 30.0],
    'SU(8)': [30.0, 40.0, 50.0],
    'SO(3)': [5.0, 8.0, 12.0],
    'Sp(6)': [10.0, 15.0, 20.0],
}

PREDICT_LS = [4, 6, 8]


def predict_group(name, params, norm, betas=None, Ls=None):
    """Predict S2/A for an unmeasured group at several (beta, L)."""
    if name not in GROUP_DB:
        print(f"  ERROR: unknown group {name}")
        return []

    if betas is None:
        betas = PREDICT_BETAS.get(name, [10.0, 15.0, 20.0])
    if Ls is None:
        Ls = PREDICT_LS

    print(f"\n{'='*70}")
    print(f"  PREDICTION: {name}")
    print(f"  Properties: d_fund={GROUP_DB[name][0]}, d_adj={GROUP_DB[name][1]}, "
          f"rank={GROUP_DB[name][4]}, n_pos_roots={GROUP_DB[name][5]}")
    print(f"{'='*70}")
    print(f"  {'beta':>8} {'L':>4} {'S2/A (NN)':>12} {'S2/A (baseline)':>16}")
    print(f"  {'-'*8} {'-'*4} {'-'*12} {'-'*16}")

    predictions = []
    for beta in betas:
        for L in Ls:
            x = group_features(name, beta, L).reshape(1, -1)
            x_n = jnp.array(norm.transform(x))
            nn_pred = float(mlp_forward(params, x_n)[0])
            bl_pred = float(analytical_baseline(x)[0])
            print(f"  {beta:8.2f} {L:4d} {nn_pred:12.4f} {bl_pred:16.4f}")
            predictions.append({
                'group': name, 'beta': beta, 'L': L,
                'nn_pred': nn_pred, 'baseline_pred': bl_pred,
            })

    return predictions


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Kevinotron v2.0 Neural Emulator (CosmoPower-style)')
    parser.add_argument('--train', action='store_true', help='Train model + LOGO-CV')
    parser.add_argument('--predict', nargs='+', default=[],
                        help='Predict for unmeasured groups (e.g., F4 E6 E8)')
    parser.add_argument('--epochs', type=int, default=2000, help='Training epochs')
    parser.add_argument('--lr', type=float, default=1e-3, help='Learning rate')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--prefix', default='kevinotron_emulator',
                        help='Output prefix for weights/norm files')
    parser.add_argument('--json', default='', help='Save predictions to JSON')
    args = parser.parse_args()

    if not args.train and not args.predict:
        parser.print_help()
        sys.exit(1)

    X, y, groups = build_dataset()
    print(f"Dataset: {len(X)} points, {len(set(groups))} groups, 9 features")
    print(f"Groups: {sorted(set(groups))}")
    print(f"S2/A range: [{y.min():.2f}, {y.max():.2f}]")

    all_predictions = []

    if args.train:
        print(f"\n{'='*70}")
        print(f"  TRAINING (full dataset)")
        print(f"{'='*70}")

        params, norm, losses = train_model(
            X, y, n_epochs=args.epochs, lr=args.lr, seed=args.seed)

        # Final evaluation
        X_n = jnp.array(norm.transform(X))
        pred = np.array(mlp_forward(params, X_n))
        bl_pred = analytical_baseline(X)

        nn_rmse = np.sqrt(np.mean((pred - y)**2))
        bl_rmse = np.sqrt(np.mean((bl_pred - y)**2))
        nn_mae = np.mean(np.abs(pred - y))
        bl_mae = np.mean(np.abs(bl_pred - y))

        print(f"\n  Final metrics (full train set):")
        print(f"    NN:       RMSE={nn_rmse:.4f}  MAE={nn_mae:.4f}")
        print(f"    Baseline: RMSE={bl_rmse:.4f}  MAE={bl_mae:.4f}")

        # Save
        save_params(params, norm, args.prefix)

        # LOGO-CV
        cv_results = leave_one_group_out_cv(X, y, groups, n_epochs=args.epochs, lr=args.lr)
        all_predictions.extend(cv_results)

    if args.predict:
        # Load or reuse params
        if not args.train:
            try:
                params, norm = load_params(args.prefix)
                print(f"Loaded model from {args.prefix}_weights.npz")
            except FileNotFoundError:
                print("ERROR: No saved model found. Run --train first.")
                sys.exit(1)

        for group_name in args.predict:
            preds = predict_group(group_name, params, norm)
            all_predictions.extend(preds)

    # Save JSON if requested
    if args.json and all_predictions:
        with open(args.json, 'w') as f:
            json.dump(all_predictions, f, indent=2)
        print(f"\nSaved {len(all_predictions)} predictions to {args.json}")


if __name__ == '__main__':
    main()
