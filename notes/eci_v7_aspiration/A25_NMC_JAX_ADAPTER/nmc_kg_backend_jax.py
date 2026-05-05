"""
A25 — Klein-Gordon NMC backend with cosmopower-jax-compatible JAX/optax trainer.

Adaptation of A9's nmc_kg_backend.py (eve 2026-05-05).
KEY CHANGE vs A9: A9 expected to call `from cosmopower import cosmopower_NN` (TF
backend), but standard `cosmopower` could not be installed on PC (pip dep loop).
Only `cosmopower-jax 0.5.5` (inference-only) is available.

Solution implemented here: train a JAX MLP using optax that mirrors the EXACT
forward pass and pickle layout cosmopower-jax expects when loaded via
    CPJ(probe='custom_log', filepath=...)
This avoids any TF / cosmopower-train dependency.

Format expected by cosmopower-jax `custom_log` (verified by reading
`/.venv-mcmc-bench/lib/python3.12/site-packages/cosmopower_jax/cosmopower_jax.py`
lines 354-403):
    pickle.dump((weights_, biases_, alphas_, betas_,
                 param_train_mean, param_train_std,
                 feature_train_mean, feature_train_std,
                 n_parameters, parameters,
                 n_modes, modes,
                 n_hidden, n_layers, architecture), f)

with weights_[i] shape (n_in, n_out)  (NOT transposed; CPJ does .T internally),
biases_[i]  shape (n_out,)
alphas_[i], betas_[i] shape (n_out,) for i = 0..n_layers-2
Output layer (last weights_, biases_) has shape (n_in_last, n_modes), (n_modes,)

Activation per CPJ source (cosmopower_jax.py:391):
    g(x; a, b) = (b + sigmoid(a*x)*(1-b)) * x
Final layer is linear  (no activation).
For probe='custom_log', CPJ returns 10**(NN_output * feature_train_std + feature_train_mean).
So we train on log10(target) when target is strictly positive, otherwise we
train on (target) itself with feature_train_mean/std rescaling and use
custom_log with output already in linear units (the 10** is then undone by
training the network on log10(linear_target)).

For this script:
  - log10 H(z)         → custom_log emulator (always positive)
  - w(z) ∈ [-2.5, 1.0] → NOT log-friendly. We map y = (w + 3)/4 ∈ (0.125, 1.0)
    and train a custom_log emulator on log10(y), then post-process at
    inference: w = 10**preds * 4 - 3. The post-processing is added on top of
    CPJ in the validator (loglike).

USAGE
-----
On PC:
  source /home/remondiere/crossed-cosmos/.venv-mcmc-bench/bin/activate
  cd /home/remondiere/pc_calcs/

  # 1. Sanity (CPU only, ~5 sec)
  python3 nmc_kg_backend_jax.py --mode sanity

  # 2. Train (GPU, light ~5-15 min)  — uses existing training_set.npz
  python3 nmc_kg_backend_jax.py --mode train

  # 3. Validate (GPU, ~3 min)
  python3 nmc_kg_backend_jax.py --mode validate

DELIVERABLES (after train + validate):
  /home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_w.pkl
  /home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_logH.pkl
  /home/remondiere/pc_calcs/cosmopower_nmc_emulator/manifest.json
  /home/remondiere/pc_calcs/cosmopower_nmc_emulator/validation.json

Author: A25 sub-agent (Sonnet), ECI v6.0.53.2, 2026-05-05.  Hallu count entering: 78.
"""
import argparse, os, sys, time, json, pickle
import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import qmc

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
M_P = 1.0
KM_S_MPC_TO_INV_MPC = 1.0 / 2.998e5

Z_GRID = np.concatenate([
    np.array([0.0]),
    np.linspace(0.05, 0.5, 20),
    np.linspace(0.55, 1.5, 50),
    np.linspace(1.55, 3.0, 29),
])  # 100 points
N_Z = len(Z_GRID)
assert N_Z == 100

# w(z) post-processing (training-time): y = (w + W_OFFSET) / W_SCALE  in (0,1]
W_OFFSET = 3.0
W_SCALE  = 4.0  # so y in (0.125, 1.0) for w in [-2.5, 1.0]


# -------------------------------------------------------------------
# Klein-Gordon backend (UNCHANGED FROM A9)
# -------------------------------------------------------------------
def _make_rhs(xi, lam, om_h2, or_h2, h, V0_norm):
    Om = om_h2 / h**2
    Or = or_h2 / h**2
    def x_of(N, phi, phi_p):
        a = np.exp(N)
        Vn = V0_norm * np.exp(-lam * phi)
        num = Om * a**(-3) + Or * a**(-4) + Vn
        denom = 1.0 - xi * phi**2 - (1.0/6.0) * phi_p**2 + 2.0 * xi * phi * phi_p
        denom = max(denom, 1e-4)
        return np.sqrt(max(num / denom, 1e-30))

    def rhs(N, y):
        phi, phi_p = y
        x = x_of(N, phi, phi_p)
        eps = 1e-3
        x_plus  = x_of(N + eps, phi + phi_p * eps, phi_p)
        x_minus = x_of(N - eps, phi - phi_p * eps, phi_p)
        dlnH_dN = (np.log(x_plus + 1e-30) - np.log(x_minus + 1e-30)) / (2 * eps)
        Vn = V0_norm * np.exp(-lam * phi)
        R_over_H02 = 6.0 * x**2 * (2.0 + dlnH_dN)
        R_over_H2 = R_over_H02 / x**2
        force = -(3.0 + dlnH_dN) * phi_p \
                + 3.0 * lam * Vn / x**2 \
                + xi * R_over_H2 * phi
        return [phi_p, force]
    return rhs, x_of


def solve_kg(xi, lam, phi0, om_h2, or_h2, h,
             N_init=-7.0, N_final=0.0, n_z=N_Z, z_grid=Z_GRID,
             shoot_iters=40, shoot_tol=1e-5):
    Om = om_h2 / h**2
    Or = or_h2 / h**2
    Ophi0_target = 1.0 - Om - Or
    if Ophi0_target < 0.05 or Ophi0_target > 0.95:
        return z_grid, np.full(n_z, -1.0), np.full(n_z, np.nan), False, {"err": "bad-Ophi0"}

    def integrate(V0_norm):
        rhs, _ = _make_rhs(xi, lam, om_h2, or_h2, h, V0_norm)
        try:
            sol = solve_ivp(rhs, (N_init, N_final), [phi0, 0.0],
                            method="LSODA", dense_output=True,
                            rtol=1e-7, atol=1e-9, max_step=0.1)
        except Exception:
            return None
        return sol if sol.success else None

    V0_lo = max(Ophi0_target * 0.1, 1e-4)
    V0_hi = min(Ophi0_target * 5.0, 5.0)
    sol = None
    V0_final = None
    for it in range(shoot_iters):
        V0_mid = 0.5 * (V0_lo + V0_hi)
        sol_try = integrate(V0_mid)
        if sol_try is None:
            V0_hi = V0_mid
            continue
        phi_T, phi_p_T = float(sol_try.y[0, -1]), float(sol_try.y[1, -1])
        Vn_T = V0_mid * np.exp(-lam * phi_T)
        denom = 1.0 - xi * phi_T**2 - (1.0/6.0) * phi_p_T**2 + 2.0 * xi * phi_T * phi_p_T
        denom = max(denom, 1e-4)
        x_T = np.sqrt(max((Om + Or + Vn_T) / denom, 1e-30))
        if x_T > 1.0:
            V0_hi = V0_mid
        else:
            V0_lo = V0_mid
        if abs(x_T - 1.0) < shoot_tol:
            sol = sol_try
            V0_final = V0_mid
            break
    if sol is None:
        sol = integrate(0.5 * (V0_lo + V0_hi))
        V0_final = 0.5 * (V0_lo + V0_hi)
        if sol is None:
            return z_grid, np.full(n_z, -1.0), np.full(n_z, np.nan), False, {"err": "ivp-fail"}

    N_grid = -np.log1p(z_grid)
    N_safe = np.clip(N_grid, N_init + 1e-3, N_final)
    yvals = sol.sol(N_safe)
    phi_arr   = yvals[0]
    phi_p_arr = yvals[1]
    a_arr = np.exp(N_safe)

    Vn_arr = V0_final * np.exp(-lam * phi_arr)
    denom_arr = 1.0 - xi * phi_arr**2 - (1.0/6.0) * phi_p_arr**2 + 2.0 * xi * phi_arr * phi_p_arr
    denom_arr = np.clip(denom_arr, 1e-4, None)
    x2_arr = (Om / a_arr**3 + Or / a_arr**4 + Vn_arr) / denom_arr
    x_arr = np.sqrt(np.clip(x2_arr, 1e-30, None))
    order = np.argsort(N_safe)
    dlnH_dN = np.zeros_like(x_arr)
    dlnH_dN[order] = np.gradient(np.log(x_arr[order] + 1e-30), N_safe[order])

    rho_chi_norm = (1.0/6.0) * x2_arr * phi_p_arr**2 + Vn_arr \
                   - 2.0 * xi * x2_arr * phi_arr * phi_p_arr
    p_chi_norm = (1.0/6.0) * x2_arr * phi_p_arr**2 - Vn_arr \
                 - (xi / 3.0) * x2_arr * (2.0 * dlnH_dN + 4.0) * phi_arr**2 \
                 - (4.0 / 3.0) * xi * x2_arr * phi_arr * phi_p_arr
    w_arr = np.where(np.abs(rho_chi_norm) > 1e-10, p_chi_norm / rho_chi_norm, -1.0)
    w_arr = np.clip(w_arr, -2.5, 1.0)
    H_kmsMpc = x_arr * h * 100.0

    info = dict(V0_norm=float(V0_final),
        phi_today=float(phi_arr[0]), phi_p_today=float(phi_p_arr[0]),
        Ophi0_target=float(Ophi0_target),
        rho_chi_today_norm=float(rho_chi_norm[0]),
        x_today=float(x_arr[0]))
    return z_grid, w_arr, H_kmsMpc, True, info


# -------------------------------------------------------------------
# Training set generation (UNCHANGED from A9 — used only if regenerated)
# -------------------------------------------------------------------
def generate_training_set(n_samples=12000, seed=2026, save_path=None):
    sampler = qmc.LatinHypercube(d=6, seed=seed)
    u = sampler.random(n_samples)
    bounds_lo = np.array([-0.10, 0.05, 0.01, 0.018, 0.095, 0.55])
    bounds_hi = np.array([ 0.10, 3.00, 0.30, 0.026, 0.140, 0.80])
    X = bounds_lo + u * (bounds_hi - bounds_lo)
    Y_w = np.full((n_samples, N_Z), -1.0)
    Y_H = np.full((n_samples, N_Z), np.nan)
    ok = np.zeros(n_samples, dtype=bool)
    Or_h2 = 4.18e-5
    t0 = time.perf_counter()
    last_ckpt = t0
    for i in range(n_samples):
        xi, lam, phi0, ob_h2, oc_h2, h = X[i]
        om_h2 = ob_h2 + oc_h2
        try:
            _, w, H, succ, _ = solve_kg(xi, lam, phi0, om_h2, Or_h2, h)
            if succ and np.all(np.isfinite(w)) and np.all(np.isfinite(H)) and H[0] > 30.0:
                Y_w[i] = w; Y_H[i] = H; ok[i] = True
        except Exception:
            pass
        now = time.perf_counter()
        if now - last_ckpt > 30 or i == n_samples - 1:
            n_done = i + 1; n_ok = ok[:n_done].sum()
            elapsed = now - t0; rate = n_done / elapsed
            eta = (n_samples - n_done) / max(rate, 1e-6)
            print(f"  [{time.strftime('%H:%M:%S')}] {n_done}/{n_samples} ({n_ok} ok={100*n_ok/n_done:.1f}%) rate={rate:.1f}/s ETA={eta/60:.1f}min", flush=True)
            last_ckpt = now
            if save_path is not None:
                np.savez_compressed(save_path,
                    X=X, Y_w=Y_w, Y_H=Y_H, ok=ok, z_grid=Z_GRID,
                    bounds_lo=bounds_lo, bounds_hi=bounds_hi,
                    n_done=n_done, version="A9-v1")
    return X, Y_w, Y_H, ok, bounds_lo, bounds_hi


# -------------------------------------------------------------------
# JAX/optax MLP training — outputs cosmopower-jax-compatible pkl
# -------------------------------------------------------------------
def _activation_jax(x, a, b):
    """CPJ activation: g(x;a,b) = (b + sigmoid(a*x)*(1-b)) * x   (CPJ source line 391)"""
    import jax.numpy as jnp
    from jax.nn import sigmoid
    return (b + sigmoid(a * x) * (1.0 - b)) * x


def _forward_jax(params, x):
    """Forward pass mirroring CPJ._predict (probe='custom_log' BEFORE the 10**)."""
    import jax.numpy as jnp
    weights_, biases_, alphas_, betas_, p_mean, p_std, f_mean, f_std = params
    # Standardise input
    z = (x - p_mean) / p_std
    # Hidden layers
    for i in range(len(weights_) - 1):
        z = jnp.dot(z, weights_[i]) + biases_[i]
        z = _activation_jax(z, alphas_[i], betas_[i])
    # Output layer (linear)
    z = jnp.dot(z, weights_[-1]) + biases_[-1]
    # Inverse-standardise output (NN learns standardised log10 targets)
    return z * f_std + f_mean


def _init_mlp_params(key, n_in, hidden, n_out):
    """Initialise an MLP with He init for hidden layers, Glorot for output, alpha~1, beta~0.5."""
    import jax, jax.numpy as jnp
    sizes = [n_in] + list(hidden) + [n_out]
    weights_ = []
    biases_  = []
    alphas_  = []
    betas_   = []
    keys = jax.random.split(key, len(sizes) - 1)
    for i, k in enumerate(keys):
        fan_in, fan_out = sizes[i], sizes[i + 1]
        # He / Glorot
        if i < len(sizes) - 2:
            scale = jnp.sqrt(2.0 / fan_in)   # He (matches non-linear regime)
        else:
            scale = jnp.sqrt(1.0 / fan_in)   # smaller for linear output
        W = jax.random.normal(k, (fan_in, fan_out)) * scale
        b = jnp.zeros((fan_out,))
        weights_.append(W)
        biases_.append(b)
        if i < len(sizes) - 2:  # one alpha/beta per hidden layer
            alphas_.append(jnp.ones((fan_out,)))
            betas_.append(0.5 * jnp.ones((fan_out,)))
    return weights_, biases_, alphas_, betas_


def train_one_emulator(X_train, Y_train, n_in, n_out, hidden=(256, 256),
                       max_steps=8000, batch_size=512, lr_schedule=None, verbose=True):
    """Train one emulator. Y_train is ALREADY log10-transformed (or post-processed).

    Returns dict with: weights_, biases_, alphas_, betas_,
                       param_train_mean, param_train_std,
                       feature_train_mean, feature_train_std, history.
    """
    import jax, jax.numpy as jnp, optax

    # Standardisation
    p_mean = X_train.mean(axis=0)
    p_std  = X_train.std(axis=0) + 1e-12
    f_mean = Y_train.mean(axis=0)
    f_std  = Y_train.std(axis=0) + 1e-12

    p_mean_j = jnp.asarray(p_mean)
    p_std_j  = jnp.asarray(p_std)
    f_mean_j = jnp.asarray(f_mean)
    f_std_j  = jnp.asarray(f_std)

    # Train/val split 90/10
    n = X_train.shape[0]
    rng = np.random.default_rng(2026)
    perm = rng.permutation(n)
    n_val = max(int(0.1 * n), 1)
    val_idx = perm[:n_val]; tr_idx = perm[n_val:]
    X_tr = jnp.asarray(X_train[tr_idx]); Y_tr = jnp.asarray(Y_train[tr_idx])
    X_va = jnp.asarray(X_train[val_idx]); Y_va = jnp.asarray(Y_train[val_idx])

    # Init params
    key = jax.random.PRNGKey(20260505)
    weights_, biases_, alphas_, betas_ = _init_mlp_params(key, n_in, hidden, n_out)

    # Standardised targets
    Y_tr_std = (Y_tr - f_mean_j) / f_std_j
    Y_va_std = (Y_va - f_mean_j) / f_std_j

    def forward(weights_, biases_, alphas_, betas_, xb):
        # xb already standardised here, returns standardised prediction
        z = xb
        for i in range(len(weights_) - 1):
            z = jnp.dot(z, weights_[i]) + biases_[i]
            z = _activation_jax(z, alphas_[i], betas_[i])
        z = jnp.dot(z, weights_[-1]) + biases_[-1]
        return z

    def loss_fn(params, xb, yb_std):
        weights_, biases_, alphas_, betas_ = params
        pred_std = forward(weights_, biases_, alphas_, betas_, xb)
        return jnp.mean((pred_std - yb_std) ** 2)

    # LR schedule: cosine decay 1e-3 -> 1e-5 with warmup
    if lr_schedule is None:
        lr_schedule = optax.warmup_cosine_decay_schedule(
            init_value=1e-5, peak_value=1e-3, warmup_steps=200,
            decay_steps=max_steps, end_value=1e-5)
    optimizer = optax.adam(learning_rate=lr_schedule)
    opt_state = optimizer.init((weights_, biases_, alphas_, betas_))

    @jax.jit
    def train_step(params, opt_state, xb, yb_std):
        loss, grads = jax.value_and_grad(loss_fn)(params, xb, yb_std)
        updates, opt_state = optimizer.update(grads, opt_state)
        params = optax.apply_updates(params, updates)
        return params, opt_state, loss

    # Standardise X for training
    X_tr_std = (X_tr - p_mean_j) / p_std_j
    X_va_std = (X_va - p_mean_j) / p_std_j

    n_tr = X_tr_std.shape[0]
    params = (weights_, biases_, alphas_, betas_)
    history = []
    t0 = time.perf_counter()
    rng_jax = jax.random.PRNGKey(7)
    best_val = np.inf
    best_params = params
    patience = 0
    PATIENCE_MAX = 30  # in eval intervals

    for step in range(max_steps):
        rng_jax, sk = jax.random.split(rng_jax)
        idx = jax.random.choice(sk, n_tr, shape=(batch_size,), replace=False)
        xb = X_tr_std[idx]; yb = Y_tr_std[idx]
        params, opt_state, loss = train_step(params, opt_state, xb, yb)
        if (step + 1) % 200 == 0:
            val_pred_std = forward(*params, X_va_std)
            val_loss = float(jnp.mean((val_pred_std - Y_va_std) ** 2))
            train_loss = float(loss)
            history.append((step + 1, train_loss, val_loss))
            if verbose:
                print(f"    step {step+1}/{max_steps}  train={train_loss:.4e}  val={val_loss:.4e}  "
                      f"({(time.perf_counter()-t0):.1f}s)", flush=True)
            if val_loss < best_val:
                best_val = val_loss
                best_params = jax.tree_util.tree_map(lambda a: a.copy(), params)
                patience = 0
            else:
                patience += 1
                if patience >= PATIENCE_MAX:
                    if verbose:
                        print(f"    early stop at step {step+1} (best val={best_val:.4e})", flush=True)
                    break

    weights_, biases_, alphas_, betas_ = best_params
    return dict(
        weights_=[np.asarray(w) for w in weights_],
        biases_=[np.asarray(b) for b in biases_],
        alphas_=[np.asarray(a) for a in alphas_],
        betas_=[np.asarray(b) for b in betas_],
        param_train_mean=np.asarray(p_mean),
        param_train_std=np.asarray(p_std),
        feature_train_mean=np.asarray(f_mean),
        feature_train_std=np.asarray(f_std),
        history=history,
        best_val=float(best_val),
        elapsed_sec=float(time.perf_counter() - t0),
    )


def save_cpj_pickle(path, trained, parameters, modes, hidden):
    """Save in cosmopower-jax `custom_log` pickle format.

    weights_[i] shape (n_in, n_out)  — CPJ does .T at load (line 343)
    biases_[i]  shape (n_out,)
    alphas_[i], betas_[i] shape (n_out,) for i = 0..n_layers-2
    """
    n_parameters = len(parameters)
    n_modes = len(modes)
    n_hidden = list(hidden)
    n_layers = len(trained["weights_"])  # = len(hidden) + 1
    architecture = ["dense" for _ in range(n_layers)]
    payload = (
        trained["weights_"],
        trained["biases_"],
        trained["alphas_"],
        trained["betas_"],
        trained["param_train_mean"],
        trained["param_train_std"],
        trained["feature_train_mean"],
        trained["feature_train_std"],
        n_parameters,
        list(parameters),
        n_modes,
        np.asarray(modes),
        n_hidden,
        n_layers,
        architecture,
    )
    with open(path, "wb") as f:
        pickle.dump(payload, f)


def train_emulator(training_npz, out_dir, hidden=(256, 256), max_steps=8000, batch_size=512):
    os.makedirs(out_dir, exist_ok=True)
    data = np.load(training_npz)
    X = data["X"]; Y_w = data["Y_w"]; Y_H = data["Y_H"]; ok = data["ok"]
    z_grid = data["z_grid"]; bounds_lo = data["bounds_lo"]; bounds_hi = data["bounds_hi"]
    Xok = X[ok]; Y_wok = Y_w[ok]; Y_Hok = Y_H[ok]
    print(f"  Training on {len(Xok)}/{len(X)} converged samples")

    param_names = ["xi", "lambda", "phi0", "omega_b_h2", "omega_c_h2", "h"]
    n_in = 6; n_out = N_Z

    # ── Emulator 1: w(z) via mapped log ──
    # y = (w + W_OFFSET) / W_SCALE  in (0.125, 1.0)
    Y_w_mapped = (Y_wok + W_OFFSET) / W_SCALE
    # Numerical guard: clip to (1e-3, 1+1e-3)
    Y_w_mapped = np.clip(Y_w_mapped, 1e-3, 1.0 + 1e-3)
    Y_w_log = np.log10(Y_w_mapped)

    print("  [w-emulator] training (target = log10((w+3)/4))...")
    trained_w = train_one_emulator(Xok, Y_w_log, n_in, n_out,
                                    hidden=hidden, max_steps=max_steps,
                                    batch_size=batch_size)
    print(f"  [w-emulator] done: best val MSE = {trained_w['best_val']:.4e}, "
          f"{trained_w['elapsed_sec']:.1f}s")
    save_cpj_pickle(os.path.join(out_dir, "nmc_kg_w.pkl"),
                    trained_w, param_names, z_grid, hidden)

    # ── Emulator 2: log10 H(z) ──
    Y_logH = np.log10(np.clip(Y_Hok, 1e-2, None))
    print("  [H-emulator] training (target = log10 H)...")
    trained_H = train_one_emulator(Xok, Y_logH, n_in, n_out,
                                    hidden=hidden, max_steps=max_steps,
                                    batch_size=batch_size)
    print(f"  [H-emulator] done: best val MSE = {trained_H['best_val']:.4e}, "
          f"{trained_H['elapsed_sec']:.1f}s")
    save_cpj_pickle(os.path.join(out_dir, "nmc_kg_logH.pkl"),
                    trained_H, param_names, z_grid, hidden)

    manifest = {
        "version": "A25-jax-v1",
        "param_names": param_names,
        "z_grid": z_grid.tolist(),
        "bounds_lo": bounds_lo.tolist(),
        "bounds_hi": bounds_hi.tolist(),
        "n_training": int(len(Xok)),
        "n_z": int(N_Z),
        "hidden": list(hidden),
        "max_steps": int(max_steps),
        "batch_size": int(batch_size),
        "files": {"w_emulator": "nmc_kg_w.pkl", "H_emulator": "nmc_kg_logH.pkl"},
        "trained": time.strftime("%Y-%m-%d %H:%M:%S"),
        "physics": "Klein-Gordon NMC quintessence (Wolf 2025), Faraoni convention, "
                   "Jordan frame, perturbative xi.",
        "validity": "|xi| < 0.10 only.",
        "post_processing": {
            "w": "w = 10**preds_w * 4 - 3   (preds_w from CPJ custom_log)",
            "H": "H = 10**preds_H            (preds_H from CPJ custom_log)",
        },
        "training_metrics": {
            "w_best_val_MSE":  trained_w["best_val"],
            "H_best_val_MSE":  trained_H["best_val"],
            "w_train_sec":     trained_w["elapsed_sec"],
            "H_train_sec":     trained_H["elapsed_sec"],
        },
    }
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  Manifest -> {out_dir}/manifest.json")
    return manifest


# -------------------------------------------------------------------
# Validation: blackjax NUTS on DESI BAO LRG2 + BBN
# -------------------------------------------------------------------
def validate_emulator(emulator_dir, n_samples=1000, n_warmup=500, out_path=None):
    import jax, jax.numpy as jnp
    import blackjax
    from cosmopower_jax.cosmopower_jax import CosmoPowerJAX as CPJ

    print(f"JAX {jax.__version__}, devices={jax.devices()}")

    # Load both emulators (we use filepath, not filename, to point to /home/...)
    cp_w = CPJ(probe="custom_log", filepath=os.path.join(emulator_dir, "nmc_kg_w.pkl"),
               verbose=False)
    cp_H = CPJ(probe="custom_log", filepath=os.path.join(emulator_dir, "nmc_kg_logH.pkl"),
               verbose=False)
    z_grid = jnp.array(Z_GRID)

    # DESI DR2 LRG2 (z_eff=0.510): values from arXiv:2503.14738 Table I.
    # (A9 used identical numbers; we keep them for direct comparison.)
    z_bao = 0.51
    dM_rd_obs, dM_rd_err = 13.62, 0.25
    dH_rd_obs, dH_rd_err = 20.98, 0.61
    obh2_bbn, obh2_err   = 0.0224, 0.0005

    def r_d_eisenstein_hu(obh2, oc_h2):
        om_h2 = obh2 + oc_h2
        return 55.154 * jnp.exp(-72.3 * 0.0006**2) / obh2**0.12807 / om_h2**0.25351

    @jax.jit
    def loglike(theta):
        xi, lam, phi0, ob_h2, oc_h2, h = theta
        params_jax = jnp.array([[xi, lam, phi0, ob_h2, oc_h2, h]])
        # CPJ custom_log returns 10**preds. So:
        # H = cp_H.predict() directly (preds were log10 H)
        # w = cp_w.predict() * W_SCALE - W_OFFSET   (preds were log10((w+3)/4))
        H_arr = cp_H.predict(params_jax)              # already 10**, → H itself
        H_arr = jnp.atleast_1d(H_arr).reshape(-1)
        # safety: if shape is (1, n) take row 0
        if H_arr.shape[0] != Z_GRID.shape[0]:
            H_arr = H_arr[: Z_GRID.shape[0]]
        # Comoving distance to z_bao via trapezoidal on z_grid
        invH = 1.0 / H_arr
        dz = jnp.diff(z_grid)
        seg = 0.5 * (invH[1:] + invH[:-1]) * dz
        cum = jnp.concatenate([jnp.array([0.0]), jnp.cumsum(seg)])
        d_M = 2.998e5 * jnp.interp(z_bao, z_grid, cum)
        H_at = jnp.interp(z_bao, z_grid, H_arr)
        d_H = 2.998e5 / H_at
        r_d = r_d_eisenstein_hu(ob_h2, oc_h2)
        chi2 = ((d_M / r_d - dM_rd_obs) / dM_rd_err) ** 2 \
             + ((d_H / r_d - dH_rd_obs) / dH_rd_err) ** 2 \
             + ((ob_h2 - obh2_bbn) / obh2_err) ** 2
        return -0.5 * chi2

    @jax.jit
    def logprior(theta):
        xi, lam, phi0, ob_h2, oc_h2, h = theta
        in_b = (jnp.abs(xi) < 0.10) & (lam > 0.05) & (lam < 3.0) \
             & (phi0 > 0.01) & (phi0 < 0.30) \
             & (ob_h2 > 0.018) & (ob_h2 < 0.026) \
             & (oc_h2 > 0.095) & (oc_h2 < 0.140) \
             & (h > 0.55) & (h < 0.80)
        return jnp.where(in_b, 0.0, -jnp.inf)

    @jax.jit
    def logpost(theta):
        lp = logprior(theta)
        return jnp.where(jnp.isfinite(lp), lp + loglike(theta), -jnp.inf)

    init = jnp.array([0.0, 1.0, 0.1, 0.0224, 0.120, 0.67])
    print(f"  init logp = {float(logpost(init)):.3f}")

    key = jax.random.PRNGKey(20260505)
    warmup = blackjax.window_adaptation(blackjax.nuts, logpost,
                                        target_acceptance_rate=0.85)
    print(f"  warmup {n_warmup} steps...")
    t0 = time.perf_counter()
    (state, params), _ = warmup.run(key, init, num_steps=n_warmup)
    print(f"  warmup done in {time.perf_counter()-t0:.1f}s")

    kernel = blackjax.nuts(logpost, **params).step
    @jax.jit
    def step(carry, key):
        s = carry
        s, info = kernel(key, s)
        return s, (s.position, info.is_divergent)
    keys = jax.random.split(jax.random.fold_in(key, 1), n_samples)
    print(f"  sampling {n_samples} steps...")
    t0 = time.perf_counter()
    state_f, (positions, divergent) = jax.lax.scan(step, state, keys)
    state_f.position.block_until_ready()
    elapsed = time.perf_counter() - t0
    n_div = int(divergent.sum())
    print(f"  done in {elapsed:.1f}s = {n_samples/elapsed:.0f} samples/sec, "
          f"divergences={n_div}")

    arr = np.asarray(positions)
    names = ["xi", "lambda", "phi0", "omega_b_h2", "omega_c_h2", "h"]
    posterior = {}
    for i, name in enumerate(names):
        posterior[name] = dict(
            mean=float(arr[:, i].mean()),
            std=float(arr[:, i].std()),
            p16=float(np.percentile(arr[:, i], 16)),
            p84=float(np.percentile(arr[:, i], 84)),
        )
    posterior["H0_kmsMpc"] = dict(
        mean=float(arr[:, -1].mean() * 100),
        std=float(arr[:, -1].std() * 100),
        p16=float(np.percentile(arr[:, -1], 16) * 100),
        p84=float(np.percentile(arr[:, -1], 84) * 100),
    )
    posterior["_meta"] = dict(
        n_samples=int(n_samples), n_warmup=int(n_warmup),
        n_divergent=n_div, sampling_sec=float(elapsed),
        bao=dict(z=z_bao, dM_rd=[dM_rd_obs, dM_rd_err], dH_rd=[dH_rd_obs, dH_rd_err],
                 obh2_bbn=[obh2_bbn, obh2_err], src="DESI DR2 LRG2 arXiv:2503.14738"),
    )

    print("\nPosterior:")
    for k, v in posterior.items():
        if k.startswith("_"): continue
        print(f"  {k:>15}: {v['mean']:9.5f} ± {v['std']:8.5f}  [{v['p16']:9.5f}, {v['p84']:9.5f}]")

    print("\nCOMPARISON")
    print(f"  ECI_NMC closed-form (C4 v5 OVERNIGHT):  H0 = 64.04 ± 2.95 km/s/Mpc")
    print(f"  A9 direct-KG MCMC (no emulator):        H0 = 67.69 ± 5.59 km/s/Mpc")
    print(f"  A25 NMC KG-emulator (this run):         H0 = {posterior['H0_kmsMpc']['mean']:.2f} "
          f"± {posterior['H0_kmsMpc']['std']:.2f} km/s/Mpc")
    if posterior['H0_kmsMpc']['mean'] > 66.5:
        print("  VERDICT: ARTEFACT RESOLVED")
    elif posterior['H0_kmsMpc']['mean'] > 65.0:
        print("  VERDICT: PARTIAL RECOVERY")
    else:
        print("  VERDICT: ARTEFACT PERSISTS")

    if out_path is not None:
        with open(out_path, "w") as f:
            json.dump(posterior, f, indent=2)
        print(f"  -> {out_path}")
    return posterior


# -------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=("sanity", "generate", "train", "validate"),
                   default="sanity")
    p.add_argument("--n_samples", type=int, default=12000)
    p.add_argument("--max_steps", type=int, default=8000)
    p.add_argument("--batch_size", type=int, default=512)
    p.add_argument("--out_dir",
                   default="/home/remondiere/pc_calcs/cosmopower_nmc_emulator")
    p.add_argument("--training_npz", default=None)
    args = p.parse_args()

    if args.mode == "sanity":
        print("[sanity 1] LCDM-like (xi=0, lam=0.05, phi0=0.1, h=0.67):")
        z, w, H, ok, info = solve_kg(0.0, 0.05, 0.10, 0.140, 4.18e-5, 0.67)
        print(f"  ok={ok}  H(z=0)={H[0]:.2f}  w(z=0)={w[0]:.4f}  info={info}")
        print("\n[sanity 2] ECI Cassini-clean (xi=0.001, lam=1.0):")
        z, w, H, ok, info = solve_kg(0.001, 1.0, 0.10, 0.140, 4.18e-5, 0.67)
        print(f"  ok={ok}  H(z=0)={H[0]:.2f}  w(z=0)={w[0]:.4f}  info={info}")
        print("\n[sanity 3] NMC perturbative-max (xi=0.05, lam=0.8):")
        z, w, H, ok, info = solve_kg(0.05, 0.8, 0.10, 0.140, 4.18e-5, 0.67)
        print(f"  ok={ok}  H(z=0)={H[0]:.2f}  w(z=0)={w[0]:.4f}  info={info}")

    elif args.mode == "generate":
        os.makedirs(args.out_dir, exist_ok=True)
        npz = os.path.join(args.out_dir, "training_set.npz")
        print(f"[generate] LHS n={args.n_samples} -> {npz}")
        X, Y_w, Y_H, ok, lo, hi = generate_training_set(
            n_samples=args.n_samples, save_path=npz)
        print(f"[generate] DONE. {ok.sum()}/{len(ok)}={100*ok.mean():.1f}% converged.")

    elif args.mode == "train":
        os.makedirs(args.out_dir, exist_ok=True)
        npz = args.training_npz or os.path.join(args.out_dir, "training_set.npz")
        if not os.path.exists(npz):
            print(f"[train] training_set.npz not found, generating first...")
            X, Y_w, Y_H, ok, lo, hi = generate_training_set(
                n_samples=args.n_samples, save_path=npz)
            print(f"[train] generation done: {ok.sum()}/{len(ok)} converged.")
        manifest = train_emulator(npz, args.out_dir,
                                   max_steps=args.max_steps,
                                   batch_size=args.batch_size)
        if manifest is not None:
            print(f"[train] DONE -> {args.out_dir}")

    elif args.mode == "validate":
        print(f"[validate] Loading emulator from {args.out_dir}")
        out = os.path.join(args.out_dir, "validation.json")
        posterior = validate_emulator(args.out_dir, n_samples=1000, n_warmup=500,
                                       out_path=out)


if __name__ == "__main__":
    main()
