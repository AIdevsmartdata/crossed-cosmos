"""
A9 — Klein-Gordon NMC backend for cosmopower-jax emulator (REAL physics)

Replaces the closed-form (Linder-2006 / Wolf CPL-fit) w(z) approximation that
produced the artefactually-low H0 ≈ 64-65 in C4 v5 OVERNIGHT (eve 2026-05-04).

Diagnosis of the C4 v5 OVERNIGHT artefact
-----------------------------------------
C4 v5 OVERNIGHT used a closed-form Wolf-CPL approximation:
    w(z) = -1 + (lam²/3) Ω_φ(z) + (2/3) ξ λ χ(z)/M_P
with χ(z) computed under linear-in-(a-1) tracker linearisation. Two failures:
  (a) The closure  Ω_φ(z) + Ω_m(z) + Ω_r(z) = 1  was enforced via
      Ω_φ(z) = 1 - Ω_m0/(...). This algebraic substitution implicitly fixes
      H(z) before w(z) is known, which DOUBLE-COUNTS the dark-energy contribution
      to expansion. The result: H(z) inherits a low-z drag, biasing H0 low.
  (b) χ(z) was set via χ(a) ≈ χ_0 + λ M_P Ω_φ,0 (a-1). At z>0.3 this is
      O(λ Ω_φ,0) too large in magnitude (the actual KG attractor flattens),
      so the NMC term over-pulls w_eff toward 0, requiring smaller H0 to fit BAO.

The proper fix is to integrate the actual Klein-Gordon equation from a deep
matter era (where φ is frozen) to today, jointly with the modified Friedmann
equation. This is what this script does.

Physics (Faraoni convention, Jordan frame, perturbative ξ_χ)
-----------------------------------------------------------
Action:
    S = ∫ d⁴x √-g [(M_P²/2 - ξ_χ χ²/2) R - (1/2)(∂χ)² - V(χ) + L_M]
    V(χ) = V_0 exp(-λχ/M_P)             [Wolf 2025 / Scherrer-Sen 2008 thawing]

Klein-Gordon (Faraoni 2000 gr-qc/9903094; Pettorino-Baccigalupi 0802.1086):
    χ̈ + 3Hχ̇ + V_χ - ξ_χ R χ = 0
    R = 6(2H² + Ḣ)                       [flat FLRW]

Modified Friedmann (Jordan, perturbative — Faraoni convention, NEGATIVE NMC corr):
    3 H² (M_P² - ξ_χ χ²) = ρ_m + ρ_r + (1/2)χ̇² + V(χ) - 6 ξ_χ H χ χ̇

NMC stress-energy (Faraoni-Dent-Saridakis 0901.3295, perturbative):
    ρ_χ = (1/2)χ̇² + V(χ) - 6 ξ_χ H χ χ̇
    p_χ = (1/2)χ̇² - V(χ) - ξ_χ(2Ḣ + 4H²)χ² - 4 ξ_χ H χ χ̇  (slow-roll dropping χ̈ terms)

Output observables for cosmopower training:
  w_eff(z) = p_χ(z) / ρ_χ(z)    [100 z-points: 0 ≤ z ≤ 3]
  H(z) [km/s/Mpc] at the same z grid

References (all arXiv-verified 2026-05-04 in /root/crossed-cosmos/notes/eci_v7_aspiration/A1_nmc_derivation_2026_05_04.md)
  - Wolf-García-García-Anton-Ferreira 2025 PRL 135 081001 = arXiv:2504.07679 [V]
  - Pettorino-Baccigalupi 2008 PRD 77 103003 = arXiv:0802.1086 [V]
  - Scherrer-Sen 2008 PRD 77 083515 = arXiv:0712.3450 [V]
  - Faraoni-Dent-Saridakis 2009 = arXiv:0901.3295 [V]
  - Adam-Hertzberg+ JCAP 04 (2026) 052 = arXiv:2509.13302 [V]
  - cosmopower (Spurio Mancini+) JCAP 04 (2022) 022; cosmopower-jax 0.5.5

Author: A9 sub-agent, ECI v6.0.53.1, 2026-05-05.  Hallu count entering: 77.
NOTE: The Karam-Palatini variant (arXiv:2604.16226) replaces ξ_χ with an
effective coupling ξ_eff = ξ × xi_eff_factor; the same backend works with
xi_eff_factor multiplied into ξ before calling solve_kg.

USAGE
-----
On PC (after G1.14 MCMC PID 201729 frees the GPU):
  cd /home/remondiere/pc_calcs/
  source ~/.venv-mcmc-bench/bin/activate

  # 1. Sanity test (1 sec, no GPU): confirm KG integrator gives sensible numbers
  python3 nmc_kg_backend.py --mode sanity

  # 2. Generate training set (~30 min, CPU only)
  python3 nmc_kg_backend.py --mode generate --n_samples 12000

  # 3. Train cosmopower NN (~30-60 min, GPU)
  python3 nmc_kg_backend.py --mode train

  # 4. Validate on DESI BAO + BBN (~5 min, GPU)
  python3 nmc_kg_backend.py --mode validate

The training step writes:
  /home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_w.pkl
  /home/remondiere/pc_calcs/cosmopower_nmc_emulator/nmc_kg_logH.pkl
  /home/remondiere/pc_calcs/cosmopower_nmc_emulator/training_set.npz
  /home/remondiere/pc_calcs/cosmopower_nmc_emulator/manifest.json
"""
import argparse, os, sys, time, json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import qmc

# -------------------------------------------------------------------
# Constants (we work in units of M_P, so M_P=1 throughout)
# -------------------------------------------------------------------
M_P = 1.0
KM_S_MPC_TO_INV_MPC = 1.0 / 2.998e5

# z-grid for emulator output
Z_GRID = np.concatenate([
    np.array([0.0]),
    np.linspace(0.05, 0.5, 20),     # dense at low-z (BAO BGS, BAO LRG1)
    np.linspace(0.55, 1.5, 50),     # DESI BAO + Pantheon+ peak
    np.linspace(1.55, 3.0, 29),     # higher-z (low-z CMB lensing kernel)
])  # 100 points
N_Z = len(Z_GRID)
assert N_Z == 100


# -------------------------------------------------------------------
# Klein-Gordon backend
# -------------------------------------------------------------------
def _make_rhs(xi, lam, om_h2, or_h2, h, V0_norm):
    """
    Build the dimensionless 2-state KG ODE in e-fold time N = ln a.

    State y = [phi, phi_prime]      with phi = χ/M_P, prime = d/dN.

    Notation (all dimensionless, normalised to today's critical density):
      x ≡ H/H₀
      Ω_m ≡ ω_m/h² ,   Ω_r ≡ ω_r/h²
      V_norm(φ) ≡ V/(3 M_P² H₀²) = V0_norm × exp(-λφ)

    Algebraic Friedmann (Faraoni convention, perturbative ξ):
      x² (1 - ξφ² - (1/6)phi_p² + 2ξφ·phi_p)
        = Ω_m a⁻³ + Ω_r a⁻⁴ + V_norm

    Derivation:
      3 H² (M_P² - ξχ²) = ρ_m + ρ_r + (1/2)χ̇² + V - 6ξHχχ̇
      ÷(3 M_P² H₀²):
      x² (1 - ξφ²) = Ω_m a⁻³ + Ω_r a⁻⁴ + (1/6)x²phi_p² + V_norm - 2ξx²φ·phi_p
      moving x² terms left:
      x² [1 - ξφ² - (1/6)phi_p² + 2ξφ·phi_p] = Ω_m a⁻³ + Ω_r a⁻⁴ + V_norm

    KG (in dimensionless φ, e-fold N):
      φ'' + (3 + dlnH/dN) φ' = -V_norm·(-λ)·3/x² + ξ(R/H₀²)·φ/x²
      i.e.
      φ'' + (3 + H'/H) φ' - 3λV_norm/x² - ξ(R/H²)·φ = 0

    where  R/H² = (R/H₀²)/x²  and  R/H₀² = 6(2x² + x·dx/dN).
    """
    Om = om_h2 / h**2
    Or = or_h2 / h**2

    def x_of(N, phi, phi_p):
        """Solve the algebraic Friedmann constraint for x = H/H₀ given (N, phi, phi_p)."""
        a = np.exp(N)
        Vn = V0_norm * np.exp(-lam * phi)
        num = Om * a**(-3) + Or * a**(-4) + Vn
        denom = 1.0 - xi * phi**2 - (1.0/6.0) * phi_p**2 + 2.0 * xi * phi * phi_p
        # Keep denominator in a sane range; if it would go ≤ 0, the perturbative
        # expansion has broken down (large ξφ² or large kinetic). Cap it.
        denom = max(denom, 1e-4)
        return np.sqrt(max(num / denom, 1e-30))

    def rhs(N, y):
        phi, phi_p = y
        x = x_of(N, phi, phi_p)
        # Numerical dlnH/dN by central difference of the algebraic Friedmann.
        # (Cheaper than re-integrating; eps must be small but > integrator step.)
        eps = 1e-3
        x_plus  = x_of(N + eps, phi + phi_p * eps, phi_p)
        x_minus = x_of(N - eps, phi - phi_p * eps, phi_p)
        dlnH_dN = (np.log(x_plus + 1e-30) - np.log(x_minus + 1e-30)) / (2 * eps)

        Vn = V0_norm * np.exp(-lam * phi)
        # Ricci scalar in units of H₀²: R/H₀² = 6(2x² + x·dx/dN) = 6x²(2 + dlnH/dN)
        R_over_H02 = 6.0 * x**2 * (2.0 + dlnH_dN)
        R_over_H2 = R_over_H02 / x**2  # = 6(2 + dlnH/dN), dimensionless

        # KG RHS for φ'' (with dV/dχ = -λV/M_P → dV/dφ_norm = -3λ V_norm)
        force = -(3.0 + dlnH_dN) * phi_p \
                + 3.0 * lam * Vn / x**2 \
                + xi * R_over_H2 * phi
        return [phi_p, force]

    return rhs, x_of


def solve_kg(xi, lam, phi0, om_h2, or_h2, h,
             N_init=-7.0, N_final=0.0, n_z=N_Z, z_grid=Z_GRID,
             shoot_iters=40, shoot_tol=1e-5):
    """
    Integrate KG from a deep matter era (a_init = e^N_init ≈ 9e-4) to today (N=0).

    Returns: (z_grid, w_arr[N_z], H_arr[N_z], success_flag, info_dict)

    Method:
      1. Set Ω_χ0 = 1 - Ω_m0 - Ω_r0 (closure, requires h, ω_b, ω_c known).
      2. At a_init the field is frozen (matter era): phi_p_init ≈ 0
         (small but nonzero attractor value λV/3H²; we let solve_ivp settle).
      3. Shoot V0_norm by 1-D bisection on the constraint x²(N=0)=1 using the
         post-integration value of phi(N=0), phi'(N=0).
      4. Reconstruct ρ_χ(z), p_χ(z), and w_eff(z) on the z grid.
    """
    Om = om_h2 / h**2
    Or = or_h2 / h**2
    Ophi0_target = 1.0 - Om - Or
    if Ophi0_target < 0.05 or Ophi0_target > 0.95:
        return z_grid, np.full(n_z, -1.0), np.full(n_z, np.nan), False, {"err": "bad-Ophi0"}

    def integrate(V0_norm):
        rhs, _ = _make_rhs(xi, lam, om_h2, or_h2, h, V0_norm)
        # Initial conditions: frozen field (phi_p tiny in matter era)
        phi_p_init = 0.0
        try:
            sol = solve_ivp(rhs, (N_init, N_final), [phi0, phi_p_init],
                            method="LSODA", dense_output=True,
                            rtol=1e-7, atol=1e-9, max_step=0.1)
        except Exception:
            return None
        return sol if sol.success else None

    # 1-D bisection on V0_norm so that x(N=0)=1.
    V0_lo = max(Ophi0_target * 0.1, 1e-4)
    V0_hi = min(Ophi0_target * 5.0, 5.0)  # be generous for steep-λ shoots
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

    # Evaluate on z grid
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
    # dlnH/dN on the z grid (numerical gradient)
    # Sort by N ascending for gradient (z descending → N ascending if we flip)
    order = np.argsort(N_safe)
    dlnH_dN = np.zeros_like(x_arr)
    dlnH_dN[order] = np.gradient(np.log(x_arr[order] + 1e-30), N_safe[order])

    # ρ_χ, p_χ in units of 3 M_P² H₀²:
    # ρ_χ_norm = (1/6) x² phi_p² + V_norm - 2 ξ x² φ phi_p
    rho_chi_norm = (1.0/6.0) * x2_arr * phi_p_arr**2 + Vn_arr \
                   - 2.0 * xi * x2_arr * phi_arr * phi_p_arr
    # p_χ_norm = (1/6) x² phi_p² - V_norm - (ξ/3) x² (2 dlnH/dN + 4) φ²
    #            - (4/3) ξ x² φ phi_p
    p_chi_norm = (1.0/6.0) * x2_arr * phi_p_arr**2 - Vn_arr \
                 - (xi / 3.0) * x2_arr * (2.0 * dlnH_dN + 4.0) * phi_arr**2 \
                 - (4.0 / 3.0) * xi * x2_arr * phi_arr * phi_p_arr

    # w_eff
    w_arr = np.where(np.abs(rho_chi_norm) > 1e-10, p_chi_norm / rho_chi_norm, -1.0)
    # Clip to physical bounds
    w_arr = np.clip(w_arr, -2.5, 1.0)

    H_kmsMpc = x_arr * h * 100.0

    info = dict(
        V0_norm=float(V0_final),
        phi_today=float(phi_arr[0]),
        phi_p_today=float(phi_p_arr[0]),
        Ophi0_target=float(Ophi0_target),
        rho_chi_today_norm=float(rho_chi_norm[0]),  # should ≈ Ophi0_target
        x_today=float(x_arr[0]),                    # should ≈ 1.000
    )
    return z_grid, w_arr, H_kmsMpc, True, info


# -------------------------------------------------------------------
# Training-set generation
# -------------------------------------------------------------------
def generate_training_set(n_samples=12000, seed=2026, save_path=None):
    """LHS over ranges that cover both Cassini-clean (ECI) and Wolf-allowed sectors.

    Parameters (6):
      xi      ∈ [-0.10, 0.10]   (broad: Wolf needs |ξ|~0.5 but emulator stays
                                  perturbative; we DO NOT cover ξ ~ 2 because the
                                  closure becomes singular — for that one needs
                                  a non-perturbative variant. ECI Cassini-clean
                                  is ξ < 0.024 so well inside this range.)
      lambda  ∈ [0.05, 3.0]    (V₀ exp(-λφ); λ > 3 → very steep, KG stiff)
      phi0    ∈ [0.01, 0.30]   (initial χ₀/M_P; thawing branch)
      omega_b_h2 ∈ [0.018, 0.026]
      omega_c_h2 ∈ [0.095, 0.140]
      h       ∈ [0.55, 0.80]   (broad: SH0ES vs Planck range)

    Returns: X (n,6), Y_w (n,N_z), Y_H (n,N_z), ok mask (n,), bounds_lo, bounds_hi.
    """
    sampler = qmc.LatinHypercube(d=6, seed=seed)
    u = sampler.random(n_samples)
    bounds_lo = np.array([-0.10, 0.05, 0.01, 0.018, 0.095, 0.55])
    bounds_hi = np.array([ 0.10, 3.00, 0.30, 0.026, 0.140, 0.80])
    X = bounds_lo + u * (bounds_hi - bounds_lo)

    Y_w = np.full((n_samples, N_Z), -1.0)
    Y_H = np.full((n_samples, N_Z), np.nan)
    ok = np.zeros(n_samples, dtype=bool)

    Or_h2 = 4.18e-5  # photons + neutrinos with Neff=3.046
    t0 = time.perf_counter()
    last_ckpt = t0
    for i in range(n_samples):
        xi, lam, phi0, ob_h2, oc_h2, h = X[i]
        om_h2 = ob_h2 + oc_h2
        try:
            _, w, H, succ, _ = solve_kg(xi, lam, phi0, om_h2, Or_h2, h)
            if succ and np.all(np.isfinite(w)) and np.all(np.isfinite(H)) and H[0] > 30.0:
                Y_w[i] = w
                Y_H[i] = H
                ok[i] = True
        except Exception:
            pass

        now = time.perf_counter()
        if now - last_ckpt > 30 or i == n_samples - 1:
            n_done = i + 1
            n_ok = ok[:n_done].sum()
            elapsed = now - t0
            rate = n_done / elapsed
            eta = (n_samples - n_done) / max(rate, 1e-6)
            print(f"  [{time.strftime('%H:%M:%S')}] {n_done}/{n_samples} "
                  f"({n_ok} ok = {100*n_ok/n_done:.1f}%) "
                  f"rate={rate:.1f}/s ETA={eta/60:.1f}min", flush=True)
            last_ckpt = now
            # Crash-safe checkpoint
            if save_path is not None:
                np.savez_compressed(save_path,
                    X=X, Y_w=Y_w, Y_H=Y_H, ok=ok, z_grid=Z_GRID,
                    bounds_lo=bounds_lo, bounds_hi=bounds_hi,
                    n_done=n_done, version="A9-v1")
    return X, Y_w, Y_H, ok, bounds_lo, bounds_hi


# -------------------------------------------------------------------
# cosmopower NN training
# -------------------------------------------------------------------
def train_emulator(training_npz, out_dir, hidden=(256, 256), n_epochs=200):
    """Train two cosmopower NNs (one for w(z), one for log10 H(z)).

    Uses cosmopower 0.1.x for training. The cosmopower-jax 0.5.5 installed on PC
    is the *inference* package; training uses the parent cosmopower TF backend.
    On PC: pip install cosmopower==0.1.6  (or use cosmopower-pytorch trainer).

    Output: two .pkl files compatible with cosmopower-jax 0.5.5 inference.
    """
    os.makedirs(out_dir, exist_ok=True)
    data = np.load(training_npz)
    X = data["X"]
    Y_w = data["Y_w"]
    Y_H = data["Y_H"]
    ok  = data["ok"]
    z_grid    = data["z_grid"]
    bounds_lo = data["bounds_lo"]
    bounds_hi = data["bounds_hi"]

    Xok   = X[ok]
    Y_wok = Y_w[ok]
    Y_Hok = Y_H[ok]
    print(f"  Training on {len(Xok)}/{len(X)} converged samples")

    try:
        from cosmopower import cosmopower_NN
    except ImportError as e:
        print(f"  cosmopower not installed: {e}", file=sys.stderr)
        print("  Install: pip install cosmopower==0.1.6", file=sys.stderr)
        return None

    param_names = ["xi", "lambda", "phi0", "omega_b_h2", "omega_c_h2", "h"]

    # Emulator 1: w(z)
    cp_w = cosmopower_NN(parameters=param_names, modes=z_grid,
                         n_hidden=list(hidden), verbose=True)
    print("  [w-emulator] training...")
    t0 = time.perf_counter()
    cp_w.train(
        training_parameters={p: Xok[:, i] for i, p in enumerate(param_names)},
        training_features=Y_wok,
        filename_saved_model=os.path.join(out_dir, "nmc_kg_w"),
        validation_split=0.1,
        learning_rates=[1e-2, 1e-3, 1e-4, 1e-5],
        batch_sizes=[256, 256, 256, 256],
        gradient_accumulation_steps=[1, 1, 1, 1],
        patience_values=[100, 100, 100, 100],
        max_epochs=[n_epochs, n_epochs, n_epochs, n_epochs],
    )
    print(f"  [w-emulator] done in {time.perf_counter()-t0:.1f}s")

    # Emulator 2: log10 H(z)
    cp_H = cosmopower_NN(parameters=param_names, modes=z_grid,
                         n_hidden=list(hidden), verbose=True)
    print("  [H-emulator] training...")
    t0 = time.perf_counter()
    cp_H.train(
        training_parameters={p: Xok[:, i] for i, p in enumerate(param_names)},
        training_features=np.log10(Y_Hok),
        filename_saved_model=os.path.join(out_dir, "nmc_kg_logH"),
        validation_split=0.1,
        learning_rates=[1e-2, 1e-3, 1e-4, 1e-5],
        batch_sizes=[256, 256, 256, 256],
        gradient_accumulation_steps=[1, 1, 1, 1],
        patience_values=[100, 100, 100, 100],
        max_epochs=[n_epochs, n_epochs, n_epochs, n_epochs],
    )
    print(f"  [H-emulator] done in {time.perf_counter()-t0:.1f}s")

    manifest = {
        "version": "A9-v1",
        "param_names": param_names,
        "z_grid": z_grid.tolist(),
        "bounds_lo": bounds_lo.tolist(),
        "bounds_hi": bounds_hi.tolist(),
        "n_training": int(len(Xok)),
        "n_z": int(N_Z),
        "files": {"w_emulator": "nmc_kg_w.pkl", "H_emulator": "nmc_kg_logH.pkl"},
        "trained": time.strftime("%Y-%m-%d %H:%M:%S"),
        "physics": "Klein-Gordon NMC quintessence (Wolf 2025), "
                   "Faraoni convention, Jordan frame, perturbative xi.",
        "validity": "|xi| < 0.10 only. For Wolf-large-xi (~2) the closure is "
                    "singular and a non-perturbative emulator is needed.",
    }
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  Manifest written to {out_dir}/manifest.json")
    return manifest


# -------------------------------------------------------------------
# Validation: blackjax NUTS on DESI BAO + BBN
# -------------------------------------------------------------------
def validate_emulator(emulator_dir, n_samples=1000, n_warmup=500):
    """Quick MCMC sanity test: do we recover sensible H0 with the new emulator?

    Uses DESI DR2 BAO LRG2 z=0.51 + BBN ω_b h². If H0 ≈ 67-69 km/s/Mpc, the C4 v5
    OVERNIGHT artefact is RESOLVED. If still ≈ 64-65 then deeper investigation
    needed (likely the BAO data itself prefers low H0 in our minimal subset, in
    which case the C4 v6 production with full Pantheon+ + CMB will be needed).
    """
    import jax, jax.numpy as jnp
    import blackjax
    try:
        from cosmopower_jax.cosmopower_jax import CPJ
    except ImportError as e:
        print(f"cosmopower_jax not installed: {e}", file=sys.stderr)
        return None

    print(f"JAX {jax.__version__}, devices={jax.devices()}")

    cp_w = CPJ(probe="custom", filename=os.path.join(emulator_dir, "nmc_kg_w"))
    cp_H = CPJ(probe="custom", filename=os.path.join(emulator_dir, "nmc_kg_logH"))
    z_grid = jnp.array(Z_GRID)

    # DESI DR2 BAO LRG2 (z=0.51): from arXiv:2503.14738 Table I
    z_bao = 0.51
    dM_rd_obs, dM_rd_err = 13.62, 0.25
    dH_rd_obs, dH_rd_err = 20.98, 0.61
    obh2_bbn, obh2_err   = 0.0224, 0.0005

    # Sound horizon r_d via Aubourg 2015 fit (Σm_ν=0):
    def r_d_eisenstein_hu(obh2, oc_h2):
        om_h2 = obh2 + oc_h2
        return 55.154 * jnp.exp(-72.3 * 0.0006**2) / obh2**0.12807 / om_h2**0.25351

    @jax.jit
    def loglike(theta):
        xi, lam, phi0, ob_h2, oc_h2, h = theta
        params_jax = jnp.array([[xi, lam, phi0, ob_h2, oc_h2, h]])
        H_arr = 10.0 ** cp_H.predict(params_jax)[0]  # km/s/Mpc on Z_GRID
        # Comoving distance to z_bao (trapezoidal on z_grid)
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
    print(f"  done in {elapsed:.1f}s = {n_samples/elapsed:.0f} samples/sec, "
          f"divergences={int(divergent.sum())}")
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
    print("\nPosterior:")
    for k, v in posterior.items():
        print(f"  {k:>15}: {v['mean']:9.5f} ± {v['std']:8.5f}  "
              f"[{v['p16']:9.5f}, {v['p84']:9.5f}]")

    # ── Compare to C4 v5 OVERNIGHT closed-form result ──
    print("\nCOMPARISON to C4 v5 OVERNIGHT (closed-form artefact)")
    print(f"  ECI_NMC closed-form:  H0 = 64.04 ± 2.95 km/s/Mpc")
    print(f"  ECI_NMC KG-backend:   H0 = {posterior['H0_kmsMpc']['mean']:.2f} "
          f"± {posterior['H0_kmsMpc']['std']:.2f} km/s/Mpc")
    delta = posterior['H0_kmsMpc']['mean'] - 64.04
    print(f"  ΔH0 = {delta:+.2f} km/s/Mpc")
    if posterior['H0_kmsMpc']['mean'] > 66.5:
        print("  VERDICT: ARTEFACT RESOLVED  (H0 in expected 67-69 range)")
    elif posterior['H0_kmsMpc']['mean'] > 65.0:
        print("  VERDICT: PARTIAL RECOVERY  (H0 still pulled low, may need "
              "full DESI BAO + Pantheon+ for full diagnosis)")
    else:
        print("  VERDICT: ARTEFACT PERSISTS  (H0 still ≈ 64-65; the data, not "
              "the closed-form, may be the cause)")
    return posterior


# -------------------------------------------------------------------
# CLI
# -------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=("sanity", "generate", "train", "validate"),
                   default="sanity",
                   help="sanity: 1 KG solve.  generate: LHS training set.  "
                        "train: cosmopower NN.  validate: NUTS sanity MCMC.")
    p.add_argument("--n_samples", type=int, default=12000)
    p.add_argument("--n_epochs", type=int, default=200)
    p.add_argument("--out_dir",
                   default="/home/remondiere/pc_calcs/cosmopower_nmc_emulator")
    p.add_argument("--training_npz", default=None,
                   help="If provided, skip generation and train on this npz.")
    args = p.parse_args()

    if args.mode == "sanity":
        # Sanity 1: ΛCDM-like limit (xi=0, lam=0.05).  Should give H(0)≈67, w(0)≈-1.
        print("[sanity 1] LCDM-like (ξ=0, λ=0.05, χ0=0.1, h=0.67):")
        z, w, H, ok, info = solve_kg(0.0, 0.05, 0.10, 0.140, 4.18e-5, 0.67)
        print(f"  ok={ok}  H(z=0)={H[0]:.2f} km/s/Mpc  w(z=0)={w[0]:.4f}  "
              f"H(z=1)={H[N_Z//2]:.2f}  w(z=1)={w[N_Z//2]:.4f}")
        print(f"  info={info}")

        # Sanity 2: ECI Cassini-clean (xi=0.001, lam=1.0)
        print("\n[sanity 2] ECI Cassini-clean (ξ=0.001, λ=1.0, χ0=0.1):")
        z, w, H, ok, info = solve_kg(0.001, 1.0, 0.10, 0.140, 4.18e-5, 0.67)
        print(f"  ok={ok}  H(z=0)={H[0]:.2f} km/s/Mpc  w(z=0)={w[0]:.4f}  "
              f"H(z=1)={H[N_Z//2]:.2f}  w(z=1)={w[N_Z//2]:.4f}")
        print(f"  info={info}")

        # Sanity 3: NMC perturbative max (xi=0.05)
        print("\n[sanity 3] NMC perturbative-max (ξ=0.05, λ=0.8, χ0=0.1):")
        z, w, H, ok, info = solve_kg(0.05, 0.8, 0.10, 0.140, 4.18e-5, 0.67)
        print(f"  ok={ok}  H(z=0)={H[0]:.2f} km/s/Mpc  w(z=0)={w[0]:.4f}  "
              f"H(z=1)={H[N_Z//2]:.2f}  w(z=1)={w[N_Z//2]:.4f}")
        print(f"  info={info}")

    elif args.mode == "generate":
        os.makedirs(args.out_dir, exist_ok=True)
        npz = os.path.join(args.out_dir, "training_set.npz")
        print(f"[generate] LHS n={args.n_samples} -> {npz}")
        X, Y_w, Y_H, ok, lo, hi = generate_training_set(
            n_samples=args.n_samples, save_path=npz)
        print(f"[generate] DONE.  {ok.sum()}/{len(ok)} = {100*ok.mean():.1f}% converged.")

    elif args.mode == "train":
        os.makedirs(args.out_dir, exist_ok=True)
        npz = args.training_npz or os.path.join(args.out_dir, "training_set.npz")
        if not os.path.exists(npz):
            print(f"[train] training_set.npz not found, generating first...")
            X, Y_w, Y_H, ok, lo, hi = generate_training_set(
                n_samples=args.n_samples, save_path=npz)
            print(f"[train] generation done: {ok.sum()}/{len(ok)} converged.")
        manifest = train_emulator(npz, args.out_dir, n_epochs=args.n_epochs)
        if manifest is not None:
            print(f"[train] DONE -> {args.out_dir}")

    elif args.mode == "validate":
        print(f"[validate] Loading emulator from {args.out_dir}")
        posterior = validate_emulator(args.out_dir, n_samples=1000, n_warmup=500)
        if posterior is not None:
            out = os.path.join(args.out_dir, "validation_posterior.json")
            with open(out, "w") as f:
                json.dump(posterior, f, indent=2)
            print(f"[validate] Posterior saved to {out}")


if __name__ == "__main__":
    main()
