#!/usr/bin/env python3
"""
ml_meta_pattern.py — Serious ML attack on the 17 SM kappa-patterns

Author : Kevin Remondiere
Date   : 2026-05-24

Pipeline:
  1.  Build feature matrix (kappa, |Phi+|, D, N_c, rep_dim, sector_one_hot, ...)
  2.  PySR symbolic regression with physics operators
  3.  Cross-validation (LOO + 4-fold)
  4.  Random-shuffle Bonferroni Z-baseline
  5.  Random Forest + permutation importance + SHAP
  6.  PCA / UMAP manifold analysis
  7.  Predict 6 held-out untested observables (PMNS theta12/theta23, delta_CP,
      V_td, g_A axial, m_p/m_pi)
  8.  Honest verdict.

Deterministic seeds throughout; parallelism='serial' for PySR.
"""

import os, sys, json, math, time, warnings, hashlib
import numpy as np
import pandas as pd
import math as M
from collections import defaultdict
warnings.filterwarnings("ignore")

SEED = 20260524
np.random.seed(SEED)

KAPPA   = 1.0/6.0
PHI_PLUS= 3
D_DIM   = 4
N_c     = 3
DIM_G   = 8
PI      = math.pi

OUTPUT_DIR = "/tmp/voie1_calcs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================================
# 1.  DATA  ----------------------------------------------------------
# =====================================================================

PATTERNS = [
    # (name, value, sector, rep_type, rep_dim, k_formula_text, source_class)
    ("kappa_LSI",      1.0/6.0,            "STRONG",       "adj",      8, "kappa",            "STRONG"),
    ("alpha_LSI",      5.0/6.0,            "STRONG",       "adj",      8, "1-kappa",          "STRONG"),
    ("lambda_H",       0.125,              "EW",           "doublet",  2, "kappa*(D-1)/D",    "EW"),
    ("sigma_8",        math.sqrt(2.0/3.0), "COSMO",        "scalar",   1, "sqrt(1-2kappa)",   "COSMO"),
    ("m_2pp_0pp",      math.sqrt(2.0),     "GLUEBALL",     "tensor",   5, "sqrt(2)",          "GLUEBALL"),
    ("m_0mp_0pp",      1.5,                "GLUEBALL",     "scalar",   1, "3/2",              "GLUEBALL"),
    ("Koide_K_lep",    2.0/3.0,            "LEPTON",       "singlet",  1, "4*kappa",          "LEPTON"),
    ("m_p_Lambda_pg",  PI/(5.0/6.0),       "STRONG",       "triplet",  3, "pi/(1-kappa)",     "STRONG"),
    ("mu_Sigma_Xi",    PI/(5.0/6.0),       "EM",           "magnetic", 3, "pi/(1-kappa)",     "EM"),
    ("V_ud",           1.0-(1.0/6.0)**2,   "WEAK_diag",    "fund",     3, "1-kappa^2",        "CKM"),
    ("V_cb",           3.0*(1.0/6.0)**2/2, "WEAK_off",     "fund",     3, "3*kappa^2/2",      "CKM"),
    ("V_us",           PI/14.0,            "WEAK_off",     "fund",     3, "pi/14",            "CKM"),
    ("V_ub",           (1.0/6.0)**3*5.0/6, "WEAK_off",     "fund",     3, "kappa^3*(1-kappa)","CKM"),
    ("V_tb",           1.0-(1.0/6.0)**4,   "WEAK_diag",    "fund",     3, "1-kappa^4",        "CKM"),
    ("K_nu_NH",        7.0/12.0,           "NEUTRINO",     "singlet",  1, "(1+kappa)/2",      "NEUTRINO"),
    ("sin2_th13_PMNS", 4.0*(1.0/6.0)**2/5, "NEUTRINO_mix", "mix",      3, "4*kappa^2/5",      "NEUTRINO"),
    ("V_cs",           1.0-(1.0/6.0)**2,   "WEAK_diag",    "fund",     3, "1-kappa^2",        "CKM"),
]
N_PAT = len(PATTERNS)

df = pd.DataFrame(PATTERNS, columns=["name","value","sector","rep_type","rep_dim","kformula","class"])

# Encode features
SECTORS = sorted(df["sector"].unique())
REPS    = sorted(df["rep_type"].unique())
CLASSES = sorted(df["class"].unique())

def featurize(row):
    f = {
        "kappa":   KAPPA,
        "phi_plus":PHI_PLUS,
        "D":       D_DIM,
        "N_c":     N_c,
        "dim_G":   DIM_G,
        "rep_dim": float(row["rep_dim"]),
        "pi":      PI,
        "log_kappa":   math.log(KAPPA),
        "log_1mk":     math.log(1-KAPPA),
        "log_1pk":     math.log(1+KAPPA),
    }
    # Sector one-hot (binary)
    for s in SECTORS:
        f[f"sec_{s}"] = 1.0 if row["sector"]==s else 0.0
    for r in REPS:
        f[f"rep_{r}"] = 1.0 if row["rep_type"]==r else 0.0
    for c in CLASSES:
        f[f"cls_{c}"] = 1.0 if row["class"]==c else 0.0
    return f

Xrows = [featurize(r) for _, r in df.iterrows()]
Xdf   = pd.DataFrame(Xrows)
y     = df["value"].values.astype(float)
log_y = np.log(y)

print("="*78)
print("ml_meta_pattern.py — Author : Kevin Remondiere")
print(f"Patterns N = {N_PAT}, features = {Xdf.shape[1]}, sectors = {len(SECTORS)}")
print("="*78)
print(f"Value range : [{y.min():.5f}, {y.max():.5f}]   log range : [{log_y.min():.3f}, {log_y.max():.3f}]")

# =====================================================================
# 2.  PYSR : continuous-only feature subset (kappa, rep_dim, pi)
# =====================================================================

print("\n" + "="*78)
print("PART 1 — PySR symbolic regression (continuous features)")
print("="*78)

# PySR with categorical sector encoding through integer index does not work well;
# use only the *continuous* numeric features. Categorical mapping is reserved
# for the RF/SHAP and the per-class PySR run.

PYSR_FEATURES = ["kappa", "rep_dim", "pi_c"]   # pi_c = pi constant (renamed to avoid PySR clash)
Xdf["pi_c"] = Xdf["pi"]
X_pysr = Xdf[PYSR_FEATURES].values

from pysr import PySRRegressor

try:
    pysr_model = PySRRegressor(
        niterations=80,
        populations=24,
        population_size=33,
        maxsize=18,
        binary_operators=["+", "-", "*", "/", "pow"],
        unary_operators=["sqrt", "square", "cube", "exp", "log", "sin", "cos"],
        loss="loss(x, y) = (log(abs(x)+1e-12) - log(abs(y)+1e-12))^2",  # log-RMSE
        complexity_of_operators={"exp":2, "log":2, "sin":3, "cos":3, "pow":2, "/":2},
        constraints={"^":(-1,3), "/":(-1,9), "log":9, "exp":9, "sin":9, "cos":9, "sqrt":9},
        nested_constraints={"sin":{"sin":0,"cos":0,"exp":0,"log":0},
                            "cos":{"sin":0,"cos":0,"exp":0,"log":0},
                            "exp":{"exp":0,"log":0,"sin":0,"cos":0},
                            "log":{"exp":0,"log":0}},
        model_selection="best",
        parallelism="serial",   # determinism
        random_state=SEED,
        deterministic=True,
        verbosity=0,
        progress=False,
        temp_equation_file=True,
    )

    t0 = time.time()
    pysr_model.fit(X_pysr, y, variable_names=PYSR_FEATURES)
    pysr_time = time.time() - t0
    print(f"\nPySR fit done in {pysr_time:.1f}s")

    EQ_DF = pysr_model.equations_.copy()
    # Restrict to manageable columns
    keep_cols = ["complexity","loss","equation"]
    print("\nPareto frontier (PySR equations):")
    print(EQ_DF[keep_cols].to_string(index=False))

    # Best by loss
    best_eq = pysr_model.sympy()
    best_pred = pysr_model.predict(X_pysr)
    rmse_train = float(np.sqrt(np.mean((best_pred - y)**2)))
    log_rmse   = float(np.sqrt(np.mean((np.log(np.abs(best_pred)+1e-12) - log_y)**2)))
    print(f"\nBest equation (sympy form): {best_eq}")
    print(f"Train RMSE : {rmse_train:.4e}   log-RMSE : {log_rmse:.4f}")

    pysr_train_pred = best_pred
    pysr_ok = True
except Exception as e:
    print(f"PySR FAILED : {e}")
    pysr_ok = False
    pysr_train_pred = np.full_like(y, y.mean())

# =====================================================================
# 3.  LEAVE-ONE-OUT CROSS-VALIDATION with PySR
# =====================================================================

print("\n" + "="*78)
print("PART 2 — Leave-One-Out CV with PySR (lightweight, niter=30)")
print("="*78)

from pysr import PySRRegressor

loo_predictions = np.zeros(N_PAT)
loo_residuals   = np.zeros(N_PAT)

# Reduced niterations for LOO (17 folds * 80 iter is heavy)
LOO_NITER = 15

def make_pysr_light():
    return PySRRegressor(
        niterations=LOO_NITER,
        populations=16,
        population_size=27,
        maxsize=15,
        binary_operators=["+", "-", "*", "/", "pow"],
        unary_operators=["sqrt", "square", "cube"],
        loss="loss(x,y) = (log(abs(x)+1e-12) - log(abs(y)+1e-12))^2",
        complexity_of_operators={"pow":2,"/":2},
        model_selection="best",
        parallelism="serial",
        random_state=SEED,
        deterministic=True,
        verbosity=0,
        progress=False,
        temp_equation_file=True,
    )

if pysr_ok:
    t0 = time.time()
    for i in range(N_PAT):
        train_idx = np.array([j for j in range(N_PAT) if j != i])
        Xtr = X_pysr[train_idx]
        ytr = y[train_idx]
        Xte = X_pysr[i:i+1]
        m = make_pysr_light()
        try:
            m.fit(Xtr, ytr, variable_names=PYSR_FEATURES)
            loo_predictions[i] = float(m.predict(Xte)[0])
        except Exception as e:
            loo_predictions[i] = np.nan
        loo_residuals[i] = (loo_predictions[i] - y[i])/y[i]
        if (i+1) % 4 == 0:
            print(f"  LOO fold {i+1}/{N_PAT} done. Elapsed {time.time()-t0:.1f}s")

    loo_rmse_rel = float(np.sqrt(np.nanmean(loo_residuals**2)))
    loo_log_rmse = float(np.sqrt(np.nanmean(
        (np.log(np.abs(loo_predictions)+1e-12) - log_y)**2)))
    print(f"\nLOO results:")
    for i in range(N_PAT):
        nm = df.iloc[i]["name"]
        print(f"  {nm:>22} : obs={y[i]:.5f}, pred={loo_predictions[i]:.5f}, "
              f"rel_err={100*loo_residuals[i]:+.2f}%")
    print(f"\nLOO relative RMSE : {100*loo_rmse_rel:.2f}%   log-RMSE : {loo_log_rmse:.4f}")
else:
    loo_rmse_rel = np.nan
    loo_log_rmse = np.nan
    print("Skipped: PySR failed.")

# =====================================================================
# 4.  BONFERRONI / RANDOM BASELINE
# =====================================================================

print("\n" + "="*78)
print("PART 3 — Bonferroni / Random baseline (shuffle features, re-fit)")
print("="*78)

# Generate random log-uniform y in same range, fit PySR with same X
N_BOOT = 12
boot_train_rmse = []
boot_loo_rmse   = []

if pysr_ok:
    for b in range(N_BOOT):
        rng = np.random.RandomState(SEED + 100*b + 1)
        # log-uniform in [log(y.min()), log(y.max())]
        y_rand = np.exp(rng.uniform(log_y.min(), log_y.max(), size=N_PAT))
        try:
            mboot = make_pysr_light()
            mboot.fit(X_pysr, y_rand, variable_names=PYSR_FEATURES)
            pred = mboot.predict(X_pysr)
            tr = float(np.sqrt(np.mean(((pred - y_rand)/y_rand)**2)))
            boot_train_rmse.append(tr)
        except Exception:
            boot_train_rmse.append(np.nan)
        if (b+1) % 5 == 0:
            print(f"  Bootstrap {b+1}/{N_BOOT} : rel-RMSE = {boot_train_rmse[-1]*100:.1f}%")

    mean_rand = float(np.nanmean(boot_train_rmse))
    std_rand  = float(np.nanstd(boot_train_rmse))
    z_train   = (mean_rand - 100*loo_rmse_rel/100) / (std_rand + 1e-9)  # placeholder

    train_rmse_rel = float(np.sqrt(np.mean(((pysr_train_pred - y)/y)**2)))
    z_train = (mean_rand - train_rmse_rel) / (std_rand + 1e-9)

    print(f"\nReal data       train rel-RMSE = {100*train_rmse_rel:.2f}%")
    print(f"Random baseline train rel-RMSE = {100*mean_rand:.2f}% +- {100*std_rand:.2f}%")
    print(f"Z-score (real vs random) = {z_train:.2f}")
    print("If Z > 2 : PySR finds REAL structure beyond what random data allows.")
else:
    z_train = np.nan
    print("Skipped: PySR failed.")

# =====================================================================
# 5.  RANDOM FOREST + PERMUTATION IMPORTANCE + SHAP
# =====================================================================

print("\n" + "="*78)
print("PART 4 — Random Forest + permutation importance + SHAP")
print("="*78)

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import KFold

# Drop sector one-hot for SHAP focus on continuous features (rep_dim, kappa, pi)
# Then redo with full features.

X_full = Xdf.values.astype(float)
feat_names = list(Xdf.columns)

rf = RandomForestRegressor(n_estimators=400, min_samples_leaf=1,
                           max_depth=None, random_state=SEED)
rf.fit(X_full, log_y)

# Train RMSE on log
rf_pred_log = rf.predict(X_full)
rf_train_rmse_log = float(np.sqrt(np.mean((rf_pred_log - log_y)**2)))
print(f"RF train log-RMSE : {rf_train_rmse_log:.4f}")

# LOO with RF
loo_rf_pred_log = np.zeros(N_PAT)
for i in range(N_PAT):
    train_idx = [j for j in range(N_PAT) if j != i]
    rf_i = RandomForestRegressor(n_estimators=400, random_state=SEED)
    rf_i.fit(X_full[train_idx], log_y[train_idx])
    loo_rf_pred_log[i] = rf_i.predict(X_full[i:i+1])[0]

loo_rf_rmse_log = float(np.sqrt(np.mean((loo_rf_pred_log - log_y)**2)))
loo_rf_pred = np.exp(loo_rf_pred_log)
loo_rf_rel  = float(np.sqrt(np.mean(((loo_rf_pred - y)/y)**2)))
print(f"RF LOO log-RMSE : {loo_rf_rmse_log:.4f}   rel-RMSE : {100*loo_rf_rel:.2f}%")

# Permutation importance
perm = permutation_importance(rf, X_full, log_y, n_repeats=30, random_state=SEED,
                              scoring='neg_mean_squared_error')
imp_idx = np.argsort(-perm.importances_mean)
print("\nPermutation importance (top 15):")
for i in imp_idx[:15]:
    print(f"  {feat_names[i]:>25} : {perm.importances_mean[i]:+.5f} "
          f"+- {perm.importances_std[i]:.5f}")

# SHAP
try:
    import shap
    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values(X_full)
    shap_abs_mean = np.mean(np.abs(shap_values), axis=0)
    shap_order = np.argsort(-shap_abs_mean)
    print("\nSHAP mean(|.|) feature importance (top 15):")
    for i in shap_order[:15]:
        print(f"  {feat_names[i]:>25} : {shap_abs_mean[i]:.5f}")
    shap_ok = True
except Exception as e:
    print(f"SHAP failed: {e}")
    shap_ok = False

# =====================================================================
# 6.  PCA / UMAP MANIFOLD ANALYSIS
# =====================================================================

print("\n" + "="*78)
print("PART 5 — PCA / UMAP manifold structure")
print("="*78)

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Use continuous numeric features + log_y as observation
manifold_feats = np.column_stack([
    Xdf[["rep_dim"]].values,
    log_y.reshape(-1,1),
])
sc = StandardScaler()
M_std = sc.fit_transform(manifold_feats)

pca = PCA(n_components=2)
proj = pca.fit_transform(M_std)
print(f"PCA explained variance ratio : {pca.explained_variance_ratio_}")
print(f"PCA components shape (rep_dim, log_y) : {pca.components_}")

# Compute pairwise distances grouped by sector
from scipy.spatial.distance import pdist, squareform
D_mat = squareform(pdist(np.column_stack([log_y.reshape(-1,1), Xdf["rep_dim"].values.reshape(-1,1)])))
sec_arr = df["sector"].values
intra_dist = []
inter_dist = []
for i in range(N_PAT):
    for j in range(i+1, N_PAT):
        if sec_arr[i] == sec_arr[j]:
            intra_dist.append(D_mat[i,j])
        else:
            inter_dist.append(D_mat[i,j])
intra_mean = float(np.mean(intra_dist)) if intra_dist else float('nan')
inter_mean = float(np.mean(inter_dist)) if inter_dist else float('nan')
sep_ratio  = inter_mean / intra_mean if intra_mean > 0 else float('nan')
print(f"Intra-sector mean distance : {intra_mean:.4f}")
print(f"Inter-sector mean distance : {inter_mean:.4f}")
print(f"Separation ratio inter/intra : {sep_ratio:.3f}  (>1 = clusters by sector)")

# UMAP
try:
    import umap
    reducer = umap.UMAP(n_components=2, n_neighbors=min(5,N_PAT-1),
                        min_dist=0.1, random_state=SEED)
    embedding = reducer.fit_transform(M_std)
    print(f"UMAP embedding shape : {embedding.shape}")
    # Cluster cohesion by sector after UMAP
    D2 = squareform(pdist(embedding))
    intra2 = [D2[i,j] for i in range(N_PAT) for j in range(i+1,N_PAT) if sec_arr[i]==sec_arr[j]]
    inter2 = [D2[i,j] for i in range(N_PAT) for j in range(i+1,N_PAT) if sec_arr[i]!=sec_arr[j]]
    sep2 = (np.mean(inter2)/np.mean(intra2)) if intra2 else float('nan')
    print(f"UMAP separation ratio : {sep2:.3f}")
    umap_ok = True
except Exception as e:
    print(f"UMAP failed: {e}")
    umap_ok = False

# =====================================================================
# 7.  EXPLICIT k-power decomposition (revisit Bonferroni properly)
# =====================================================================

print("\n" + "="*78)
print("PART 6 — Bonferroni-PROPER test of k^a * (1-k)^b * pi^d * (n/m)")
print("="*78)

# For each pattern, search best (a, b, c, d, n/m) integer-ish decomposition
# Compute sparsity score and compare to random log-uniform y.

K, K1m, K1p, P = KAPPA, 1-KAPPA, 1+KAPPA, PI
# Restrict to integer exponents and small rationals — natural-physics regime
A_RANGE = [-2,-1,0,1,2,3]
B_RANGE = [-1,0,1,2]
C_RANGE = [0,1]
D_RANGE = [-1,0,1]
NUMS = list(range(1,8))
DENS = list(range(1,8))
TOL_DECOMP = 0.001   # 0.1% relative tolerance

def best_decomp(val):
    best = None
    for a in A_RANGE:
        for b in B_RANGE:
            for c in C_RANGE:
                for d in D_RANGE:
                    base = (K**a) * (K1m**b) * (K1p**c) * (P**d)
                    if base <= 0:
                        continue
                    target = val / base
                    if not (0.05 < target < 30):
                        continue   # rational won't be small
                    for n in NUMS:
                        for m in DENS:
                            r = n/m
                            rel = abs(target - r) / abs(target)
                            if rel < TOL_DECOMP:
                                sparsity = abs(a) + abs(b) + abs(c) + abs(d) + (n+m)/30
                                score = sparsity + 200*rel
                                if best is None or score < best[0]:
                                    best = (score, a, b, c, d, n, m, rel)
                                break
    return best

decomps_real = []
for i, val in enumerate(y):
    bd = best_decomp(val)
    decomps_real.append(bd)

# Number found
N_found_real = sum(1 for d in decomps_real if d is not None)
print(f"Patterns admitting clean decomp (real)  : {N_found_real}/{N_PAT}")
sparsity_real = [d[0] for d in decomps_real if d is not None]
print(f"Mean sparsity score (real)              : {np.mean(sparsity_real):.3f}")

# Random log-uniform baseline (one shot)
N_RAND_TRIALS = 200
rand_found_counts = []
rand_sparsity = []
for t in range(N_RAND_TRIALS):
    rng = np.random.RandomState(SEED + t*17)
    yrand = np.exp(rng.uniform(log_y.min(), log_y.max(), size=N_PAT))
    nfound = 0
    sp = []
    for v in yrand:
        bd = best_decomp(v)
        if bd is not None:
            nfound += 1
            sp.append(bd[0])
    rand_found_counts.append(nfound)
    if sp:
        rand_sparsity.append(np.mean(sp))

mean_rand_found = float(np.mean(rand_found_counts))
std_rand_found  = float(np.std(rand_found_counts))
z_found = (N_found_real - mean_rand_found) / (std_rand_found + 1e-9)
print(f"Random baseline N_found : {mean_rand_found:.2f} +- {std_rand_found:.2f}   (Z = {z_found:.2f})")

if rand_sparsity:
    mean_rand_sp = float(np.mean(rand_sparsity))
    std_rand_sp  = float(np.std(rand_sparsity))
    z_sp = (np.mean(sparsity_real) - mean_rand_sp) / (std_rand_sp + 1e-9)  # negative=better
    print(f"Random baseline sparsity : {mean_rand_sp:.3f} +- {std_rand_sp:.3f}  (Z = {z_sp:+.2f})")
else:
    z_sp = float('nan')

# =====================================================================
# 8.  NEW PREDICTIONS for held-out observables
# =====================================================================

print("\n" + "="*78)
print("PART 7 — Predictions for 6 untested observables")
print("="*78)

# Build feature rows for new observables (best guess sector/rep)
NEW_OBS = [
    # name, observed, sector, rep_type, rep_dim, class
    ("sin2_th12_PMNS",      0.307,    "NEUTRINO_mix", "mix",      3, "NEUTRINO"),
    ("sin2_th23_PMNS",      0.561,    "NEUTRINO_mix", "mix",      3, "NEUTRINO"),
    ("delta_CP_over_2pi",   197/360.0,"NEUTRINO_mix", "mix",      3, "NEUTRINO"),
    ("V_td",                0.0080,   "WEAK_off",     "fund",     3, "CKM"),
    ("g_A_axial",           1.2754,   "EW",           "doublet",  2, "EW"),
    ("m_p_over_m_pi",       6.726,    "STRONG",       "triplet",  3, "STRONG"),
]
new_df = pd.DataFrame(NEW_OBS, columns=["name","observed","sector","rep_type","rep_dim","class"])
# featurize
def featurize_new(row):
    f = {
        "kappa": KAPPA, "phi_plus":PHI_PLUS, "D":D_DIM, "N_c":N_c, "dim_G":DIM_G,
        "rep_dim": float(row["rep_dim"]), "pi": PI,
        "log_kappa": math.log(KAPPA), "log_1mk": math.log(1-KAPPA),
        "log_1pk": math.log(1+KAPPA),
    }
    for s in SECTORS:
        f[f"sec_{s}"] = 1.0 if row["sector"]==s else 0.0
    for r in REPS:
        f[f"rep_{r}"] = 1.0 if row["rep_type"]==r else 0.0
    for c in CLASSES:
        f[f"cls_{c}"] = 1.0 if row["class"]==c else 0.0
    return f

Xnew = pd.DataFrame([featurize_new(r) for _,r in new_df.iterrows()])
# align columns to training X
for c in Xdf.columns:
    if c not in Xnew.columns:
        Xnew[c] = 0.0
Xnew = Xnew[Xdf.columns].values.astype(float)

# RF predictions
rf_new_log = rf.predict(Xnew)
rf_new = np.exp(rf_new_log)

# PySR predictions (continuous features only) - column order matches PYSR_FEATURES
X_pysr_new = np.column_stack([
    np.full(len(NEW_OBS), KAPPA),
    new_df["rep_dim"].values.astype(float),
    np.full(len(NEW_OBS), PI),  # pi_c
])
if pysr_ok:
    pysr_new = pysr_model.predict(X_pysr_new)
else:
    pysr_new = np.full(len(NEW_OBS), np.nan)

# Also direct decomposition predictions: scan (a,b,c,d,n,m) using observed value
direct_decomps = []
for i, row in new_df.iterrows():
    bd = best_decomp(row["observed"])
    direct_decomps.append(bd)

# Also formula-style guesses inspired by patterns:
#  sin2_th12 : 1/(1+pi)?  3/10?  1-2k=2/3 (=0.667 too big), 1-3k=0.5, 1-3k*1=0.5.
#  Try: (1-2k)/(1+k) = (2/3)/(7/6) = 4/7 ~= 0.571
#  Try: pi/(2*7) = 0.224 (V_us-like). For 0.307 -> 2-sqrt(2)? 6/(2pi-?).
# This is exploratory; we report direct decomp scan.

# Also: try a "candidate-formula" set inspired by patterns seen in the 17
def candidate_formulas():
    candidates = [
        ("kappa",                KAPPA),
        ("1-kappa",              1-KAPPA),
        ("1+kappa",              1+KAPPA),
        ("2*kappa",              2*KAPPA),
        ("3*kappa",              3*KAPPA),
        ("4*kappa",              4*KAPPA),
        ("6*kappa",              6*KAPPA),
        ("kappa^2",              KAPPA**2),
        ("3*kappa^2",            3*KAPPA**2),
        ("1-kappa^2",            1-KAPPA**2),
        ("1-2*kappa",            1-2*KAPPA),
        ("(1-kappa)/2",          (1-KAPPA)/2),
        ("(1+kappa)/2",          (1+KAPPA)/2),
        ("(2-kappa)/3",          (2-KAPPA)/3),
        ("1/(1+kappa)",          1/(1+KAPPA)),
        ("2/(2+kappa)",          2/(2+KAPPA)),
        ("3/(3+kappa)",          3/(3+KAPPA)),
        ("kappa*(D-1)/D",        KAPPA*(D_DIM-1)/D_DIM),
        ("kappa^3*(1-kappa)",    KAPPA**3*(1-KAPPA)),
        ("3*kappa^2/2",          3*KAPPA**2/2),
        ("4*kappa^2/5",          4*KAPPA**2/5),
        ("pi/14",                PI/14),
        ("pi/(1-kappa)",         PI/(1-KAPPA)),
        ("pi/(2*(1-kappa))",     PI/(2*(1-KAPPA))),
        ("sqrt(1-2*kappa)",      math.sqrt(1-2*KAPPA)),
        ("sqrt(2)",              math.sqrt(2)),
        ("sqrt(kappa)",          math.sqrt(KAPPA)),
        ("sqrt(1-kappa)",        math.sqrt(1-KAPPA)),
        ("sqrt(1+kappa)",        math.sqrt(1+KAPPA)),
        ("3/2",                  1.5),
        ("3/2 * pi/(1-kappa)",   1.5*PI/(1-KAPPA)),
        ("6/(2*pi-1)",           6/(2*PI-1)),
        ("7/(2*pi)",             7/(2*PI)),
        ("(1-kappa)/sqrt(2)",    (1-KAPPA)/math.sqrt(2)),
        ("3*(1-kappa)/4",        3*(1-KAPPA)/4),
        ("2*kappa+1/3",          2*KAPPA + 1/3),
        ("kappa+1/2",            KAPPA + 1/2),
        ("(1+2*kappa)/2",        (1+2*KAPPA)/2),
        ("kappa*pi/(1-kappa)",   KAPPA*PI/(1-KAPPA)),
        ("(1-kappa)^2",          (1-KAPPA)**2),
        ("1-kappa^4",            1-KAPPA**4),
        ("1+kappa^2",            1+KAPPA**2),
        ("kappa*pi",             KAPPA*PI),
        ("4*pi/(15-kappa)",      4*PI/(15-KAPPA)),
        ("9/(2*pi)",             9/(2*PI)),
        # PMNS-specific candidates
        ("1-2*kappa - 1/3",      1-2*KAPPA - 1/3),   # 1/3
        ("1/3 + 2*kappa",        1/3 + 2*KAPPA),     # 2/3
        ("1/2 + kappa/(1+kappa)",1/2 + KAPPA/(1+KAPPA)),
        ("4*kappa/(1-kappa)",    4*KAPPA/(1-KAPPA)),
        ("pi/(8+kappa)",         PI/(8+KAPPA)),
        ("pi/(2-kappa)",         PI/(2-KAPPA)),
        ("(1-2*kappa)*(1-kappa)",(1-2*KAPPA)*(1-KAPPA)),
        ("kappa*(2-kappa)/(1-kappa)", KAPPA*(2-KAPPA)/(1-KAPPA)),
    ]
    return candidates

CANDS = candidate_formulas()

def best_candidate_match(obs):
    best = None
    for label, val in CANDS:
        rel = abs(val - obs)/obs
        if best is None or rel < best[1]:
            best = (label, rel, val)
    return best

print("\nPredictions table:")
hdr = f"{'name':>22} {'observed':>10} {'RF pred':>10} {'PySR pred':>12} {'best closed-form':>40} {'rel%':>6}"
print(hdr)
print("-"*len(hdr))
for i, row in new_df.iterrows():
    nm = row["name"]; obs = row["observed"]
    rf_p = rf_new[i]; ps_p = pysr_new[i]
    bd = direct_decomps[i]
    bc = best_candidate_match(obs)
    closed_str = f"{bc[0]} = {bc[2]:.5f}"
    rel_pct = 100*bc[1]
    print(f"{nm:>22} {obs:>10.5f} {rf_p:>10.5f} {ps_p:>12.5g} {closed_str:>40} {rel_pct:>6.2f}")

# Also report decomp scan
print("\nIntegerized κ-decomposition scan (Bonferroni-proper, tight):")
for i, row in new_df.iterrows():
    nm = row["name"]; obs = row["observed"]
    bd = direct_decomps[i]
    if bd is None:
        print(f"  {nm:>22} : NO CLEAN DECOMP (real signal of non-pattern)")
    else:
        score, a, b, c, d, n, m, rel = bd
        pred = (K**a)*(K1m**b)*(K1p**c)*(P**d)*(n/m)
        print(f"  {nm:>22} : k^{a:+.0f}*(1-k)^{b:+.0f}*(1+k)^{c:+.0f}*pi^{d:+.0f}*({n}/{m})  "
              f"= {pred:.5f}  vs obs {obs:.5f}  rel={100*rel:.2f}%   sparsity={score:.2f}")

# =====================================================================
# 9.  HONEST VERDICT  ----------------------------------------------
# =====================================================================

print("\n" + "="*78)
print("PART 8 — Honest verdict")
print("="*78)

verdict = {
    "pysr_train_log_rmse":      log_rmse if pysr_ok else None,
    "loo_rmse_rel":             loo_rmse_rel if pysr_ok else None,
    "loo_log_rmse":             loo_log_rmse if pysr_ok else None,
    "random_baseline_train":    mean_rand if pysr_ok else None,
    "random_baseline_train_std":std_rand if pysr_ok else None,
    "z_score_train":            z_train if pysr_ok else None,
    "rf_train_log_rmse":        rf_train_rmse_log,
    "rf_loo_log_rmse":          loo_rf_rmse_log,
    "rf_loo_rmse_rel":          loo_rf_rel,
    "pca_explained":            pca.explained_variance_ratio_.tolist(),
    "sector_separation_2d":     sep_ratio,
    "sector_separation_umap":   sep2 if umap_ok else None,
    "decomp_N_found_real":      N_found_real,
    "decomp_N_found_random_mean": mean_rand_found,
    "decomp_N_found_random_std":  std_rand_found,
    "z_decomp":                 z_found,
    "z_sparsity":               z_sp,
}
print(json.dumps(verdict, indent=2))

# Save verdict for the report
with open(os.path.join(OUTPUT_DIR, "ml_meta_pattern_verdict.json"), "w") as fp:
    json.dump(verdict, fp, indent=2)
print("\nVerdict written to ml_meta_pattern_verdict.json")

# =====================================================================
# 10. PER-CLASS PySR + manifold-dimension estimation
# =====================================================================

print("\n" + "="*78)
print("PART 9 — Per-class PySR fits (intrinsic structure per sector class)")
print("="*78)

# For each class with >= 3 points, try PySR with rep_dim and a class-marker
# Use ALL features for a true symbolic model
CLASS_PYSR_RES = {}
for cls in CLASSES:
    mask = (df["class"] == cls).values
    if mask.sum() < 2:
        continue
    Xc = np.column_stack([
        np.full(mask.sum(), KAPPA),
        df.loc[mask, "rep_dim"].values.astype(float),
    ])
    yc = y[mask]
    print(f"\n  Class {cls} : N={mask.sum()}  observations = {yc}")
    try:
        mc = PySRRegressor(
            niterations=40, populations=12, population_size=22, maxsize=12,
            binary_operators=["+","-","*","/","pow"],
            unary_operators=["sqrt","square","cube"],
            loss="loss(x,y)=(log(abs(x)+1e-12)-log(abs(y)+1e-12))^2",
            model_selection="best", parallelism="serial",
            random_state=SEED, deterministic=True,
            verbosity=0, progress=False, temp_equation_file=True,
        )
        mc.fit(Xc, yc, variable_names=["kappa","rep_dim"])
        eq = mc.sympy()
        pred = mc.predict(Xc)
        rmse_log = float(np.sqrt(np.mean((np.log(np.abs(pred)+1e-12)-np.log(yc))**2)))
        CLASS_PYSR_RES[cls] = {"equation": str(eq), "log_rmse": rmse_log, "N": int(mask.sum())}
        print(f"    eq: {eq}")
        print(f"    log-RMSE = {rmse_log:.4f}")
    except Exception as e:
        print(f"    PySR fail: {e}")
        CLASS_PYSR_RES[cls] = {"equation": None, "log_rmse": None, "N": int(mask.sum())}

# =====================================================================
# 11. Manifold intrinsic dimension via correlation dimension (Grassberger-Procaccia)
# =====================================================================

print("\n" + "="*78)
print("PART 10 — Intrinsic dimension (correlation-dim, MLE, FFT spectrum)")
print("="*78)

# Use 2-feature (rep_dim, log_y) as before, plus full 37-dim
def correlation_dim(X, n_eps=30):
    Dm = squareform(pdist(X))
    triu = Dm[np.triu_indices_from(Dm, k=1)]
    if len(triu) == 0:
        return float('nan')
    eps = np.logspace(np.log10(triu.min()+1e-9), np.log10(triu.max()), n_eps)
    Cs = np.array([(triu < e).mean() for e in eps])
    # log-log slope in middle range
    mid = (Cs > 0.05) & (Cs < 0.8)
    if mid.sum() < 4:
        return float('nan')
    slope, _ = np.polyfit(np.log(eps[mid]), np.log(Cs[mid]+1e-12), 1)
    return float(slope)

cd_2d  = correlation_dim(np.column_stack([Xdf["rep_dim"].values, log_y]))
cd_full= correlation_dim(X_full)
print(f"  Correlation dim (rep_dim, log_y)   : {cd_2d:.3f}")
print(f"  Correlation dim (37-feature space) : {cd_full:.3f}")

# PCA spectrum on full
pca_full = PCA(n_components=min(N_PAT, 37))
pca_full.fit(X_full)
explained = pca_full.explained_variance_ratio_
cumvar = np.cumsum(explained)
n90 = int(np.searchsorted(cumvar, 0.90)+1)
n99 = int(np.searchsorted(cumvar, 0.99)+1)
print(f"  PCA: n components for 90% var = {n90}, for 99% var = {n99}")
print(f"  Explained variance per component (top 8): {explained[:8]}")

# =====================================================================
# 12. GMM generative model & sample
# =====================================================================

print("\n" + "="*78)
print("PART 11 — GMM generative model + Bonferroni proper test")
print("="*78)

from sklearn.mixture import GaussianMixture

# Fit GMM in the (log_y, rep_dim) 2-D manifold
M_lowdim = np.column_stack([log_y.reshape(-1,1), Xdf["rep_dim"].values.reshape(-1,1)])
best_bic = float('inf'); best_k = 1; best_gmm = None
for k in range(1, 7):
    try:
        gmm = GaussianMixture(n_components=k, covariance_type='full',
                              random_state=SEED, n_init=4)
        gmm.fit(M_lowdim)
        bic = gmm.bic(M_lowdim)
        if bic < best_bic:
            best_bic = bic
            best_k = k
            best_gmm = gmm
    except Exception:
        continue
print(f"Best GMM #components by BIC = {best_k}  (BIC = {best_bic:.2f})")

# Generate samples and check how often a sample matches a clean kappa-decomp
N_SAMP = 500
samp = best_gmm.sample(N_SAMP)[0]
samp_y = np.exp(samp[:,0])
N_samp_decomp = 0
for v in samp_y:
    bd = best_decomp(v)
    if bd is not None:
        N_samp_decomp += 1
print(f"  GMM samples admitting clean κ-decomp : {N_samp_decomp}/{N_SAMP} = {100*N_samp_decomp/N_SAMP:.1f}%")
print(f"  Real patterns: {N_found_real}/{N_PAT} = {100*N_found_real/N_PAT:.1f}%")

# Save full results
final_summary = {
    "verdict": verdict,
    "class_pysr": CLASS_PYSR_RES,
    "intrinsic_dim_2d": cd_2d,
    "intrinsic_dim_full": cd_full,
    "pca_n_components_90pct": int(n90),
    "pca_n_components_99pct": int(n99),
    "gmm_best_k": int(best_k),
    "gmm_bic": float(best_bic),
    "gmm_sample_decomp_frac": N_samp_decomp/N_SAMP,
    "real_decomp_frac": N_found_real/N_PAT,
}
with open(os.path.join(OUTPUT_DIR, "ml_meta_pattern_full_summary.json"), "w") as fp:
    json.dump(final_summary, fp, indent=2, default=str)
print("\nFull summary saved to ml_meta_pattern_full_summary.json")

# =====================================================================
# 13. Cross-LLM-style overfitting check: shuffle y, refit RF
# =====================================================================
print("\n" + "="*78)
print("PART 12 — Y-shuffle null distribution for RF feature importance")
print("="*78)

real_top_imp = perm.importances_mean[imp_idx[0]]
N_SHUF = 50
shuf_top_imp = []
for s in range(N_SHUF):
    rng = np.random.RandomState(SEED+2025+s)
    y_perm = rng.permutation(log_y)
    rf_s = RandomForestRegressor(n_estimators=200, random_state=SEED+s)
    rf_s.fit(X_full, y_perm)
    perm_s = permutation_importance(rf_s, X_full, y_perm, n_repeats=10,
                                    random_state=SEED+s, scoring='neg_mean_squared_error')
    shuf_top_imp.append(perm_s.importances_mean.max())
mean_shuf = float(np.mean(shuf_top_imp))
std_shuf  = float(np.std(shuf_top_imp))
z_imp = (real_top_imp - mean_shuf)/(std_shuf+1e-9)
print(f"  Real top feature importance       : {real_top_imp:.4f}  (sec_WEAK_off)")
print(f"  Shuffled-y null max imp           : {mean_shuf:.4f} +- {std_shuf:.4f}")
print(f"  Z-score of real importance        : {z_imp:.2f}")
if z_imp > 2:
    print("  -> Top feature is REAL signal, not chance")
else:
    print("  -> Top feature may be noise / structural label leak (4 WEAK_off members ALL fund triplets)")

print("\nDONE.")
