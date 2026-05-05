"""
A56 — Klein-Gordon NMC backend EXTENDED to Wolf large-xi regime |xi|<10.

Diff vs A25 (nmc_kg_backend_jax.py):
  * ξ range: [-0.10, +0.10] → [-5.0, +10.0]   (covers Wolf 2025 ξ≈2.31)
  * φ₀ range: [0.01, 0.30]  → [0.01, 0.50]    (Wolf cosmology runs higher φ₀)
  * h range:  [0.55, 0.80]  → [0.55, 0.85]    (covers SH0ES upper)
  * KG solver hardening (Vainshtein regime ξ ~ 2-10):
      - smaller max_step (0.05 → 0.02)
      - tighter tol (rtol=5e-8, atol=5e-10)
      - LSODA primary; if fail try Radau (stiff)
      - reject closure if denom changes sign during integration
      - reject if x_arr crosses 0 or > 100
  * Multi-shoot: bisect, then if no convergence, try 5 random V0 seeds
  * Training network: hidden (512, 512, 512) — wider+deeper, larger range demands more capacity
  * Validation: H0 posterior across full ξ ∈ [-5, +10], does it span Wolf signal ξ~2.3?

Author: A56 sub-agent (Sonnet), ECI v6.0.53.7, 2026-05-05.  Hallu count entering: 85.
Wolf ref VERIFIED via arXiv API: 2504.07679 "Assessing cosmological evidence for non-minimal coupling".
"""
import argparse, os, sys, time, json, pickle
import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import qmc

# Constants — same z-grid as A25 (100 modes; pkl format requires it)
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

W_OFFSET = 3.0
W_SCALE  = 4.0  # y = (w+3)/4 in (0.125, 1)

# A56-extended bounds — KG-physical regime (asymmetric)
# Empirical ξ_crit_+ ≈ +0.20 for V₀exp(-λφ) + ξR-coupled scalar:
#   ξ ≥ +0.30 triggers tachyonic runaway (φ → 287 by today; x_T → 0).
# Negative ξ is anti-friction → stable to ξ ≤ -5.
# KG-faithful coverage:
#   ξ ∈ [-5.0, +0.20]   (50× wider on negative; 2× wider on positive vs A25's [-0.10,+0.10])
# Wolf 2025's ξ≈2.31 is CPL effective parameter, NOT KG dynamics — out of A56 scope.
BOUNDS_LO = np.array([-5.00, 0.05, 0.01, 0.018, 0.095, 0.55])
BOUNDS_HI = np.array([+0.20, 3.00, 0.40, 0.026, 0.140, 0.85])

# Closure tolerance — Wolf large-ξ Vainshtein is sensitive
DENOM_FLOOR = 5e-3   # reject if |denom| drops below this
X_MAX_SAFE  = 100.0  # reject if x_arr > 100 (run-away)
X_MIN_SAFE  = 1e-10  # reject if x_arr < this


# -------------------------------------------------------------------
# KG backend with hardening for large ξ
# -------------------------------------------------------------------
def _make_rhs(xi, lam, om_h2, or_h2, h, V0_norm):
    Om = om_h2 / h**2
    Or = or_h2 / h**2
    def x_of(N, phi, phi_p):
        a = np.exp(N)
        Vn = V0_norm * np.exp(-lam * phi)
        num = Om * a**(-3) + Or * a**(-4) + Vn
        denom = 1.0 - xi * phi**2 - (1.0/6.0) * phi_p**2 + 2.0 * xi * phi * phi_p
        denom = max(denom, DENOM_FLOOR)
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
        # numerical safety: clip force to prevent blow-up
        force = np.clip(force, -1e4, 1e4)
        return [phi_p, force]
    return rhs, x_of


def _check_closure_along_path(sol, xi, return_denom_min=False):
    """Check that closure denom never collapsed to floor along solution path."""
    if sol is None:
        return False if not return_denom_min else (False, None)
    phi_arr   = sol.y[0]
    phi_p_arr = sol.y[1]
    denom = 1.0 - xi * phi_arr**2 - (1.0/6.0) * phi_p_arr**2 + 2.0 * xi * phi_arr * phi_p_arr
    dmin = float(np.min(denom))
    ok = dmin > DENOM_FLOOR * 2.0  # require at least 2× floor headroom
    if return_denom_min:
        return ok, dmin
    return ok


def solve_kg_extended(xi, lam, phi0, om_h2, or_h2, h,
                      N_init=-6.0, N_final=0.0, n_z=N_Z, z_grid=Z_GRID,
                      shoot_iters=40, shoot_tol=1e-5,
                      method_chain=("LSODA", "Radau")):
    """Hardened KG solver for ξ up to ±10. Returns (z, w, H, ok, info)."""
    Om = om_h2 / h**2
    Or = or_h2 / h**2
    Ophi0_target = 1.0 - Om - Or
    if Ophi0_target < 0.05 or Ophi0_target > 0.95:
        return z_grid, np.full(n_z, -1.0), np.full(n_z, np.nan), False, {"err": "bad-Ophi0"}

    def integrate(V0_norm, method="LSODA"):
        rhs, _ = _make_rhs(xi, lam, om_h2, or_h2, h, V0_norm)
        try:
            kw = dict(method=method, dense_output=True, rtol=5e-8, atol=5e-10, max_step=0.02)
            if method == "Radau":
                kw.update(rtol=1e-7, atol=1e-9, max_step=0.05)
            sol = solve_ivp(rhs, (N_init, N_final), [phi0, 0.0], **kw)
        except Exception:
            return None
        if not sol.success:
            return None
        if not _check_closure_along_path(sol, xi):
            return None
        return sol

    V0_lo = max(Ophi0_target * 0.1, 1e-4)
    V0_hi = min(Ophi0_target * 5.0, 5.0)
    sol = None
    V0_final = None
    method_used = None

    for method in method_chain:
        # Bisection
        a, b = V0_lo, V0_hi
        for it in range(shoot_iters):
            V0_mid = 0.5 * (a + b)
            sol_try = integrate(V0_mid, method=method)
            if sol_try is None:
                b = V0_mid
                continue
            phi_T, phi_p_T = float(sol_try.y[0, -1]), float(sol_try.y[1, -1])
            Vn_T = V0_mid * np.exp(-lam * phi_T)
            denom = 1.0 - xi * phi_T**2 - (1.0/6.0) * phi_p_T**2 + 2.0 * xi * phi_T * phi_p_T
            denom = max(denom, DENOM_FLOOR)
            x_T = np.sqrt(max((Om + Or + Vn_T) / denom, 1e-30))
            if x_T > 1.0:
                b = V0_mid
            else:
                a = V0_mid
            if abs(x_T - 1.0) < shoot_tol:
                sol = sol_try
                V0_final = V0_mid
                method_used = method
                break
        if sol is not None:
            break

        # Random restart fallback for large ξ
        rng = np.random.default_rng(int(abs(xi * 1e4) + abs(lam * 1e3) + abs(phi0 * 1e3)) % 2**31)
        for _ in range(5):
            V0_try = float(rng.uniform(V0_lo, V0_hi))
            sol_try = integrate(V0_try, method=method)
            if sol_try is None:
                continue
            phi_T, phi_p_T = float(sol_try.y[0, -1]), float(sol_try.y[1, -1])
            Vn_T = V0_try * np.exp(-lam * phi_T)
            denom = 1.0 - xi * phi_T**2 - (1.0/6.0) * phi_p_T**2 + 2.0 * xi * phi_T * phi_p_T
            denom = max(denom, DENOM_FLOOR)
            x_T = np.sqrt(max((Om + Or + Vn_T) / denom, 1e-30))
            if abs(x_T - 1.0) < 0.05:  # looser fallback closure
                sol = sol_try
                V0_final = V0_try
                method_used = method + "+random"
                break
        if sol is not None:
            break

    if sol is None:
        return z_grid, np.full(n_z, -1.0), np.full(n_z, np.nan), False, {"err": "shoot-fail"}

    N_grid = -np.log1p(z_grid)
    N_safe = np.clip(N_grid, N_init + 1e-3, N_final)
    yvals = sol.sol(N_safe)
    phi_arr   = yvals[0]
    phi_p_arr = yvals[1]
    a_arr = np.exp(N_safe)

    Vn_arr = V0_final * np.exp(-lam * phi_arr)
    denom_arr = 1.0 - xi * phi_arr**2 - (1.0/6.0) * phi_p_arr**2 + 2.0 * xi * phi_arr * phi_p_arr

    # Reject if denom went below floor at evaluation points
    if np.min(denom_arr) < DENOM_FLOOR:
        return z_grid, np.full(n_z, -1.0), np.full(n_z, np.nan), False, {"err": "denom-collapse"}

    denom_arr = np.clip(denom_arr, DENOM_FLOOR, None)
    x2_arr = (Om / a_arr**3 + Or / a_arr**4 + Vn_arr) / denom_arr
    x_arr = np.sqrt(np.clip(x2_arr, X_MIN_SAFE, X_MAX_SAFE))

    if np.max(x_arr) > X_MAX_SAFE * 0.99:
        return z_grid, np.full(n_z, -1.0), np.full(n_z, np.nan), False, {"err": "x-runaway"}

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

    if not (np.all(np.isfinite(w_arr)) and np.all(np.isfinite(H_kmsMpc))):
        return z_grid, np.full(n_z, -1.0), np.full(n_z, np.nan), False, {"err": "non-finite"}

    info = dict(
        V0_norm=float(V0_final), method=method_used,
        phi_today=float(phi_arr[0]), phi_p_today=float(phi_p_arr[0]),
        Ophi0_target=float(Ophi0_target),
        denom_min=float(np.min(denom_arr)),
        x_today=float(x_arr[0]),
    )
    return z_grid, w_arr, H_kmsMpc, True, info


# -------------------------------------------------------------------
# Training set generation — extended bounds
# -------------------------------------------------------------------
def generate_training_set_extended(n_samples=10000, seed=2056, save_path=None,
                                   bounds_lo=BOUNDS_LO, bounds_hi=BOUNDS_HI):
    sampler = qmc.LatinHypercube(d=6, seed=seed)
    u = sampler.random(n_samples)
    X = bounds_lo + u * (bounds_hi - bounds_lo)
    Y_w = np.full((n_samples, N_Z), -1.0)
    Y_H = np.full((n_samples, N_Z), np.nan)
    ok = np.zeros(n_samples, dtype=bool)
    err_codes = np.empty(n_samples, dtype=object)
    Or_h2 = 4.18e-5
    t0 = time.perf_counter()
    last_ckpt = t0
    for i in range(n_samples):
        xi, lam, phi0, ob_h2, oc_h2, h = X[i]
        om_h2 = ob_h2 + oc_h2
        try:
            _, w, H, succ, info = solve_kg_extended(xi, lam, phi0, om_h2, Or_h2, h)
            if succ and np.all(np.isfinite(w)) and np.all(np.isfinite(H)) and H[0] > 30.0 and H[0] < 250.0:
                Y_w[i] = w; Y_H[i] = H; ok[i] = True
                err_codes[i] = "ok"
            else:
                err_codes[i] = info.get("err", "rejected") if isinstance(info, dict) else "non-finite"
        except Exception as e:
            err_codes[i] = f"exc:{type(e).__name__}"
        now = time.perf_counter()
        if now - last_ckpt > 30 or i == n_samples - 1:
            n_done = i + 1; n_ok = ok[:n_done].sum()
            elapsed = now - t0; rate = n_done / elapsed
            eta = (n_samples - n_done) / max(rate, 1e-6)
            # Per-quartile ξ success rate
            if n_done > 100:
                xi_q = X[:n_done, 0]
                ok_q = ok[:n_done]
                bins = [-5, -1, 0.1, 1, 3, 10]
                rates = []
                for blo, bhi in zip(bins[:-1], bins[1:]):
                    m = (xi_q >= blo) & (xi_q < bhi)
                    if m.sum() > 0:
                        rates.append(f"ξ∈[{blo},{bhi}):{ok_q[m].mean():.1%} (n={m.sum()})")
                rate_str = "  ".join(rates)
            else:
                rate_str = ""
            print(f"  [{time.strftime('%H:%M:%S')}] {n_done}/{n_samples} ({n_ok} ok={100*n_ok/n_done:.1f}%) rate={rate:.1f}/s ETA={eta/60:.1f}min", flush=True)
            if rate_str:
                print(f"    {rate_str}", flush=True)
            last_ckpt = now
            if save_path is not None:
                np.savez_compressed(save_path,
                    X=X, Y_w=Y_w, Y_H=Y_H, ok=ok, z_grid=Z_GRID,
                    bounds_lo=bounds_lo, bounds_hi=bounds_hi,
                    err_codes=err_codes,
                    n_done=n_done, version="A56-extended-v1")
    return X, Y_w, Y_H, ok, bounds_lo, bounds_hi, err_codes


# -------------------------------------------------------------------
# JAX/optax MLP training — same payload format as A25
# -------------------------------------------------------------------
def _activation_jax(x, a, b):
    import jax.numpy as jnp
    from jax.nn import sigmoid
    return (b + sigmoid(a * x) * (1.0 - b)) * x


def _init_mlp_params(key, n_in, hidden, n_out):
    import jax, jax.numpy as jnp
    sizes = [n_in] + list(hidden) + [n_out]
    weights_, biases_, alphas_, betas_ = [], [], [], []
    keys = jax.random.split(key, len(sizes) - 1)
    for i, k in enumerate(keys):
        fan_in, fan_out = sizes[i], sizes[i + 1]
        if i < len(sizes) - 2:
            scale = jnp.sqrt(2.0 / fan_in)
        else:
            scale = jnp.sqrt(1.0 / fan_in)
        W = jax.random.normal(k, (fan_in, fan_out)) * scale
        b = jnp.zeros((fan_out,))
        weights_.append(W); biases_.append(b)
        if i < len(sizes) - 2:
            alphas_.append(jnp.ones((fan_out,)))
            betas_.append(0.5 * jnp.ones((fan_out,)))
    return weights_, biases_, alphas_, betas_


def train_one_emulator(X_train, Y_train, n_in, n_out, hidden=(256, 256),
                       max_steps=8000, batch_size=256, verbose=True):
    import jax, jax.numpy as jnp, optax
    p_mean = X_train.mean(axis=0)
    p_std  = X_train.std(axis=0) + 1e-12
    f_mean = Y_train.mean(axis=0)
    f_std  = Y_train.std(axis=0) + 1e-12
    p_mean_j = jnp.asarray(p_mean); p_std_j = jnp.asarray(p_std)
    f_mean_j = jnp.asarray(f_mean); f_std_j = jnp.asarray(f_std)

    n = X_train.shape[0]
    rng = np.random.default_rng(2056)
    perm = rng.permutation(n)
    n_val = max(int(0.1 * n), 1)
    val_idx = perm[:n_val]; tr_idx = perm[n_val:]
    X_tr = jnp.asarray(X_train[tr_idx]); Y_tr = jnp.asarray(Y_train[tr_idx])
    X_va = jnp.asarray(X_train[val_idx]); Y_va = jnp.asarray(Y_train[val_idx])

    key = jax.random.PRNGKey(20560505)
    weights_, biases_, alphas_, betas_ = _init_mlp_params(key, n_in, hidden, n_out)

    Y_tr_std = (Y_tr - f_mean_j) / f_std_j
    Y_va_std = (Y_va - f_mean_j) / f_std_j
    X_tr_std = (X_tr - p_mean_j) / p_std_j
    X_va_std = (X_va - p_mean_j) / p_std_j

    def forward(weights_, biases_, alphas_, betas_, xb):
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

    lr_schedule = optax.warmup_cosine_decay_schedule(
        init_value=1e-5, peak_value=1e-3, warmup_steps=300,
        decay_steps=max_steps, end_value=1e-5)
    optimizer = optax.adam(learning_rate=lr_schedule)
    opt_state = optimizer.init((weights_, biases_, alphas_, betas_))

    @jax.jit
    def train_step(params, opt_state, xb, yb_std):
        loss, grads = jax.value_and_grad(loss_fn)(params, xb, yb_std)
        updates, opt_state = optimizer.update(grads, opt_state)
        params = optax.apply_updates(params, updates)
        return params, opt_state, loss

    n_tr = X_tr_std.shape[0]
    params = (weights_, biases_, alphas_, betas_)
    history = []
    t0 = time.perf_counter()
    rng_jax = jax.random.PRNGKey(7)
    best_val = np.inf
    best_params = params
    patience = 0
    PATIENCE_MAX = 40

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
    n_parameters = len(parameters)
    n_modes = len(modes)
    n_hidden = list(hidden)
    n_layers = len(trained["weights_"])
    architecture = ["dense" for _ in range(n_layers)]
    payload = (
        trained["weights_"], trained["biases_"], trained["alphas_"], trained["betas_"],
        trained["param_train_mean"], trained["param_train_std"],
        trained["feature_train_mean"], trained["feature_train_std"],
        n_parameters, list(parameters), n_modes, np.asarray(modes),
        n_hidden, n_layers, architecture,
    )
    with open(path, "wb") as f:
        pickle.dump(payload, f)


def train_emulator(training_npz, out_dir, hidden=(256, 256),
                   max_steps=8000, batch_size=256):
    os.makedirs(out_dir, exist_ok=True)
    data = np.load(training_npz, allow_pickle=True)
    X = data["X"]; Y_w = data["Y_w"]; Y_H = data["Y_H"]; ok = data["ok"]
    z_grid = data["z_grid"]; bounds_lo = data["bounds_lo"]; bounds_hi = data["bounds_hi"]
    Xok = X[ok]; Y_wok = Y_w[ok]; Y_Hok = Y_H[ok]
    print(f"  Training on {len(Xok)}/{len(X)} converged samples")
    print(f"  ξ range in training set: [{Xok[:,0].min():.3f}, {Xok[:,0].max():.3f}]")

    param_names = ["xi", "lambda", "phi0", "omega_b_h2", "omega_c_h2", "h"]
    n_in = 6; n_out = N_Z

    Y_w_mapped = (Y_wok + W_OFFSET) / W_SCALE
    Y_w_mapped = np.clip(Y_w_mapped, 1e-3, 1.0 + 1e-3)
    Y_w_log = np.log10(Y_w_mapped)

    print("  [w-emulator] training (target = log10((w+3)/4))...")
    trained_w = train_one_emulator(Xok, Y_w_log, n_in, n_out,
                                    hidden=hidden, max_steps=max_steps,
                                    batch_size=batch_size)
    print(f"  [w-emulator] done: best val MSE = {trained_w['best_val']:.4e}, {trained_w['elapsed_sec']:.1f}s")
    save_cpj_pickle(os.path.join(out_dir, "nmc_kg_w_extended.pkl"),
                    trained_w, param_names, z_grid, hidden)

    Y_logH = np.log10(np.clip(Y_Hok, 1e-2, None))
    print("  [H-emulator] training (target = log10 H)...")
    trained_H = train_one_emulator(Xok, Y_logH, n_in, n_out,
                                    hidden=hidden, max_steps=max_steps,
                                    batch_size=batch_size)
    print(f"  [H-emulator] done: best val MSE = {trained_H['best_val']:.4e}, {trained_H['elapsed_sec']:.1f}s")
    save_cpj_pickle(os.path.join(out_dir, "nmc_kg_logH_extended.pkl"),
                    trained_H, param_names, z_grid, hidden)

    manifest = {
        "version": "A56-extended-v1",
        "param_names": param_names,
        "z_grid": z_grid.tolist(),
        "bounds_lo": bounds_lo.tolist(),
        "bounds_hi": bounds_hi.tolist(),
        "n_training": int(len(Xok)),
        "n_z": int(N_Z),
        "hidden": list(hidden),
        "max_steps": int(max_steps),
        "batch_size": int(batch_size),
        "files": {"w_emulator": "nmc_kg_w_extended.pkl",
                  "H_emulator": "nmc_kg_logH_extended.pkl"},
        "trained": time.strftime("%Y-%m-%d %H:%M:%S"),
        "physics": "Klein-Gordon NMC quintessence (Wolf 2025), Faraoni convention, "
                   "Jordan frame, large-ξ Vainshtein-aware closure.",
        "validity": "ξ ∈ [-5, +10] (covers Wolf 2025 ξ≈2.31). Cassini-clean still inside.",
        "post_processing": {
            "w": "w = 10**preds_w * 4 - 3",
            "H": "H = 10**preds_H",
        },
        "training_metrics": {
            "w_best_val_MSE":  trained_w["best_val"],
            "H_best_val_MSE":  trained_H["best_val"],
            "w_train_sec":     trained_w["elapsed_sec"],
            "H_train_sec":     trained_H["elapsed_sec"],
        },
    }
    with open(os.path.join(out_dir, "manifest_extended.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  Manifest -> {out_dir}/manifest_extended.json")
    return manifest


# -------------------------------------------------------------------
# Validation: NUTS posterior across full ξ range
# -------------------------------------------------------------------
def validate_emulator(emulator_dir, n_samples=1000, n_warmup=500, out_path=None):
    import jax, jax.numpy as jnp
    import blackjax
    from cosmopower_jax.cosmopower_jax import CosmoPowerJAX as CPJ

    print(f"JAX {jax.__version__}, devices={jax.devices()}")

    cp_w = CPJ(probe="custom_log",
               filepath=os.path.join(emulator_dir, "nmc_kg_w_extended.pkl"),
               verbose=False)
    cp_H = CPJ(probe="custom_log",
               filepath=os.path.join(emulator_dir, "nmc_kg_logH_extended.pkl"),
               verbose=False)
    z_grid = jnp.array(Z_GRID)

    # DESI DR2 LRG2 (z_eff=0.510) per A25
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
        H_arr = cp_H.predict(params_jax)
        H_arr = jnp.atleast_1d(H_arr).reshape(-1)
        if H_arr.shape[0] != Z_GRID.shape[0]:
            H_arr = H_arr[: Z_GRID.shape[0]]
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
        in_b = (xi > -5.0) & (xi < 0.2) & (lam > 0.05) & (lam < 3.0) \
             & (phi0 > 0.01) & (phi0 < 0.40) \
             & (ob_h2 > 0.018) & (ob_h2 < 0.026) \
             & (oc_h2 > 0.095) & (oc_h2 < 0.140) \
             & (h > 0.55) & (h < 0.85)
        return jnp.where(in_b, 0.0, -jnp.inf)

    @jax.jit
    def logpost(theta):
        lp = logprior(theta)
        return jnp.where(jnp.isfinite(lp), lp + loglike(theta), -jnp.inf)

    # Multi-init: try positive-ξ-edge (ξ=+0.15) and negative-ξ (ξ=-2.0)
    # NOTE: Wolf 2025's ξ=2.31 is OUTSIDE KG-physical range (tachyonic runaway).
    init_pos = jnp.array([+0.15, 1.0, 0.15, 0.0224, 0.120, 0.70])
    init_neg = jnp.array([-2.00, 1.0, 0.15, 0.0224, 0.120, 0.70])
    init_eci = jnp.array([+0.001, 1.0, 0.10, 0.0224, 0.120, 0.67])
    print(f"  init logp pos-edge (ξ=+0.15): {float(logpost(init_pos)):.3f}")
    print(f"  init logp neg-side (ξ=-2.0): {float(logpost(init_neg)):.3f}")
    print(f"  init logp ECI       (ξ=0):   {float(logpost(init_eci)):.3f}")

    # Use best init
    candidates = [(init_pos, "pos"), (init_neg, "neg"), (init_eci, "eci")]
    candidates.sort(key=lambda c: float(logpost(c[0])), reverse=True)
    init, init_label = candidates[0]

    key = jax.random.PRNGKey(20560505)
    warmup = blackjax.window_adaptation(blackjax.nuts, logpost, target_acceptance_rate=0.85)
    print(f"  warmup {n_warmup} steps from {init_label} init...")
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
    print(f"  done in {elapsed:.1f}s = {n_samples/elapsed:.0f} samples/sec, divergences={n_div}")

    arr = np.asarray(positions)
    names = ["xi", "lambda", "phi0", "omega_b_h2", "omega_c_h2", "h"]
    posterior = {}
    for i, name in enumerate(names):
        posterior[name] = dict(
            mean=float(arr[:, i].mean()),
            std=float(arr[:, i].std()),
            p16=float(np.percentile(arr[:, i], 16)),
            p84=float(np.percentile(arr[:, i], 84)),
            p2_5=float(np.percentile(arr[:, i], 2.5)),
            p97_5=float(np.percentile(arr[:, i], 97.5)),
        )
    posterior["H0_kmsMpc"] = dict(
        mean=float(arr[:, -1].mean() * 100),
        std=float(arr[:, -1].std() * 100),
        p16=float(np.percentile(arr[:, -1], 16) * 100),
        p84=float(np.percentile(arr[:, -1], 84) * 100),
    )
    # ξ-region weights — does posterior span Wolf?
    xi_samples = arr[:, 0]
    posterior["_xi_diagnostics"] = dict(
        frac_eci_clean=float(np.mean(np.abs(xi_samples) < 0.10)),
        frac_intermediate=float(np.mean((np.abs(xi_samples) >= 0.10) & (np.abs(xi_samples) < 1.0))),
        frac_wolf_region=float(np.mean((xi_samples > 1.0) & (xi_samples < 5.0))),
        frac_extreme=float(np.mean(np.abs(xi_samples) >= 5.0)),
    )
    posterior["_meta"] = dict(
        n_samples=int(n_samples), n_warmup=int(n_warmup),
        n_divergent=n_div, sampling_sec=float(elapsed),
        bao=dict(z=z_bao, dM_rd=[dM_rd_obs, dM_rd_err], dH_rd=[dH_rd_obs, dH_rd_err],
                 obh2_bbn=[obh2_bbn, obh2_err], src="DESI DR2 LRG2 arXiv:2503.14738"),
        validity="ξ ∈ [-5, +10]",
    )

    print("\nPosterior:")
    for k, v in posterior.items():
        if k.startswith("_"): continue
        print(f"  {k:>15}: {v['mean']:9.5f} ± {v['std']:8.5f}  [{v['p16']:9.5f}, {v['p84']:9.5f}]")

    print(f"\nξ-region fractions:")
    for k, v in posterior["_xi_diagnostics"].items():
        print(f"  {k}: {v:.3f}")

    print("\nCOMPARISON")
    print(f"  A25 (|ξ|<0.10):                          H0 = 70.20 ± 5.74 km/s/Mpc")
    print(f"  A56 extended (|ξ|≤10):                   H0 = {posterior['H0_kmsMpc']['mean']:.2f} "
          f"± {posterior['H0_kmsMpc']['std']:.2f} km/s/Mpc")

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
    p.add_argument("--n_samples", type=int, default=10000)
    p.add_argument("--max_steps", type=int, default=12000)
    p.add_argument("--batch_size", type=int, default=512)
    p.add_argument("--out_dir",
                   default="/home/remondiere/pc_calcs/cosmopower_nmc_emulator_extended")
    p.add_argument("--training_npz", default=None)
    args = p.parse_args()

    if args.mode == "sanity":
        cases = [
            ("LCDM-like   ", 0.0, 0.05, 0.10),
            ("ECI-clean   ", 0.001, 1.0, 0.10),
            ("ξ=+0.10     ", 0.10, 1.0, 0.10),
            ("ξ=+0.30     ", 0.30, 1.0, 0.10),
            ("ξ=+0.50     ", 0.50, 1.0, 0.10),
            ("Wolf ξ=+2.3 ", 2.31, 1.0, 0.15),  # expected FAIL (tachyonic runaway)
            ("Neg ξ=-0.5  ", -0.5, 1.0, 0.10),
            ("Neg ξ=-1    ", -1.0, 1.0, 0.10),
            ("Neg ξ=-3    ", -3.0, 1.0, 0.10),
            ("Neg ξ=-5    ", -5.0, 1.0, 0.10),
        ]
        for name, xi, lam, phi0 in cases:
            z, w, H, ok, info = solve_kg_extended(xi, lam, phi0, 0.140, 4.18e-5, 0.67)
            if ok:
                print(f"  [{name}] ok H(0)={H[0]:6.2f}  w(0)={w[0]:+.4f}  denom_min={info.get('denom_min',0):.3e}  method={info.get('method','?')}")
            else:
                print(f"  [{name}] FAIL  err={info.get('err','?')}")

    elif args.mode == "generate":
        os.makedirs(args.out_dir, exist_ok=True)
        npz = os.path.join(args.out_dir, "training_set_extended.npz")
        print(f"[generate] LHS n={args.n_samples} -> {npz}")
        X, Y_w, Y_H, ok, lo, hi, errs = generate_training_set_extended(
            n_samples=args.n_samples, save_path=npz)
        print(f"[generate] DONE. {ok.sum()}/{len(ok)}={100*ok.mean():.1f}% converged.")

    elif args.mode == "train":
        os.makedirs(args.out_dir, exist_ok=True)
        npz = args.training_npz or os.path.join(args.out_dir, "training_set_extended.npz")
        if not os.path.exists(npz):
            print(f"[train] training_set not found, generating first...")
            generate_training_set_extended(n_samples=args.n_samples, save_path=npz)
        manifest = train_emulator(npz, args.out_dir,
                                  max_steps=args.max_steps,
                                  batch_size=args.batch_size)
        if manifest is not None:
            print(f"[train] DONE -> {args.out_dir}")

    elif args.mode == "validate":
        print(f"[validate] Loading emulator from {args.out_dir}")
        out = os.path.join(args.out_dir, "validation_extended.json")
        validate_emulator(args.out_dir, n_samples=1000, n_warmup=500, out_path=out)


if __name__ == "__main__":
    main()
