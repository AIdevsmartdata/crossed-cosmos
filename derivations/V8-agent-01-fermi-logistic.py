"""
V8-agent-01-fermi-logistic.py
==============================
MaxEnt derivation: Gibbs ensemble on complexity-labeled states →
logistic envelope (1 - C/C^max) for the entropy-rate observable.
Fermi-Dirac analogy assessment.

Author: agent-01 (2026-04-22)
Rules enforced: PRINCIPLES rule 1 (no claim beyond derivation),
                rule 12 (no claim larger than derivation supports),
                V6-1 (inequality, not equality).
"""

import numpy as np
import sympy as sp

# ────────────────────────────────────────────────────────────────────────────
# PART 1 — SYMBOLIC DERIVATION (sympy)
# ────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("PART 1: Symbolic MaxEnt derivation")
print("=" * 70)

beta, n, N, lam, mu = sp.symbols('beta n N lambda mu', real=True)

# Gibbs ensemble: p_n = exp(-beta*n) / Z,  n = 0,...,N
# Z = sum_{n=0}^{N} exp(-beta*n) — geometric series
Z = sp.summation(sp.exp(-beta * n), (n, 0, N))
Z = sp.factor(Z)
print("\n[1] Partition function Z =", Z)

# Mean complexity <C> = -d(log Z)/d(beta)
log_Z = sp.log(Z)
mean_C = -sp.diff(log_Z, beta)
mean_C = sp.simplify(mean_C)
print("\n[2] Mean complexity <C> = -d(log Z)/dbeta =", mean_C)

# Gibbs entropy S_G = log Z + beta * <C>  [from S = -sum p_n log p_n]
# Legendre identity: dS_G / d<C> = beta  (holding N fixed)
# Proof: S_G = log Z + beta*<C>
#        d/d<C> [log Z + beta*<C>] = d/d<C>[log Z] + beta + <C>*d(beta)/d<C>
# Since <C> = -d(log Z)/d(beta), differentiating the constraint:
#   d<C>/d<C> = 1 = -d²(log Z)/d(beta²) * d(beta)/d<C>
#   => d(beta)/d<C> = -1 / (d²(log Z)/d(beta²))
# Also d(log Z)/d<C> = d(log Z)/d(beta) * d(beta)/d<C> = (-<C>) * d(beta)/d<C>
# So dS_G/d<C> = (-<C>)*d(beta)/d<C> + beta + <C>*d(beta)/d<C> = beta  ✓
print("\n[3] Legendre identity: dS_Gibbs / d<C> = beta  (exact, from convexity of log Z)")
print("    Proof: S_G = log Z + beta*<C>, and beta = beta(<C>) by inversion of <C>(beta).")
print("    dS_G/d<C> = (d log Z/d beta)*(d beta/d<C>) + beta + <C>*(d beta/d<C>)")
print("             = (-<C>)*(d beta/d<C>) + beta + <C>*(d beta/d<C>) = beta  QED")

# Corollary: dS_G/dtau_R = beta * d<C>/dtau_R
print("\n[4] Corollary: dS_G/dtau_R = beta * d<C>/dtau_R")

# ────────────────────────────────────────────────────────────────────────────
# PART 2 — RATE OPERATOR AND LOGISTIC ENVELOPE
# ────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("PART 2: Rate operator and logistic envelope")
print("=" * 70)

print("""
Definition (Capacity-limited rate operator):
  Define R_hat with eigenvalues R_n = (C_max - C_n) / C_max
  on state |n> with complexity C_n = n * delta_C.

  Physical motivation: the rate of complexity growth is limited by
  remaining capacity (C_max - C_n)/C_max — the fraction of the budget
  not yet consumed. This parallels the FD blocking factor (1 - f_n).

Claim: <R_hat> = 1 - <C>/C_max  (exactly, by linearity of expectation).

Proof: <R_hat> = sum_n p_n * (C_max - C_n)/C_max
              = 1/C_max * (C_max - sum_n p_n C_n)
              = 1 - <C>/C_max  QED
""")

print("""
Entropy-rate bound (under M1 complexity postulate):
  If d<C>/dtau_R <= kappa * <C>  (linear-growth regime, M1-partial),
  then  dS_G/dtau_R = beta * d<C>/dtau_R <= beta * kappa * <C>.

  Tightened form (under full logistic postulate):
  If d<C>/dtau_R <= kappa * <C> * (1 - <C>/C_max),
  then  dS_G/dtau_R <= beta * kappa * <C> * (1 - <C>/C_max).

  Identifying kappa_R := beta * kappa (absorbed into the bound coefficient),
  this recovers the logistic envelope of Prop. 1 (v6.1 eq:logistic):

      dS_gen[R]/dtau_R  <=  kappa_R * C_k * (1 - C_k/C_k^max)  [times Theta]

  The logistic factor (1 - C/C_max) = <R_hat> in the Gibbs ensemble.
""")

print("""
Fermi-Dirac analogy (precision statement):
  FD is the MaxEnt distribution for BINARY occupation (0 or 1) of levels:
      f_n = 1 / (exp(beta*(E_n - mu)) + 1)
  The factor (1 - f_n) = exp(beta*(E_n-mu)) * f_n appears in:
    - Pauli blocking (single-level exclusion)
    - FD entropy: S_FD = -sum[f_n log f_n + (1-f_n) log(1-f_n)]

  MAPPING to our ensemble:
    FD level occupation f_n  <-->  p_n (Gibbs weight)
    Chemical potential mu    <-->  complexity threshold ~ C_max/2
    Pauli factor (1-f_n)     <-->  rate factor R_n = (C_max - n)/C_max
    at MEAN-FIELD level:  (1 - f_mu) = 1/2  <-->  1 - <C>/C_max  at <C>=C_max/2

  ANALOGY STRENGTH: the logistic envelope (1 - C/C_max) is the GLOBAL
  capacity-fraction analogue of the FD blocking factor (1-f_n) at the
  single-level. At mean-field level (<C> → C_max/2, beta→0), both
  factors equal 1/2. The correspondence is an analogy (mean-field
  isomorphism), NOT an exact algebraic identity.

  WHAT MAXENT DELIVERS (without additional postulate):
    - Exact: dS_Gibbs/d<C> = beta  (Legendre identity)
    - Exact: <R_hat> = 1 - <C>/C_max  (linearity of expectation)
    - Conditional: dS/dtau <= kappa_R * C*(1-C/C_max)  IF the rate law
      d<C>/dtau <= kappa * <C> * <R_hat> is physically postulated (M1).
""")

# ────────────────────────────────────────────────────────────────────────────
# PART 3 — NUMERICAL CROSS-CHECK
# ────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("PART 3: Numerical cross-check")
print("=" * 70)

N_levels = 50  # C_max = 50

print(f"\nGibbs ensemble on n=0,...,{N_levels}  (C_max = {N_levels})")
print(f"{'beta':>8} {'<C>':>8} {'dS/d<C>':>12} {'expected beta':>14} {'<R_hat>':>10} {'1-<C>/C_max':>12}")
print("-" * 70)

errors_legendre = []
errors_rate = []

for bv in [0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0]:
    ns = np.arange(0, N_levels + 1, dtype=float)
    log_w = -bv * ns
    log_w -= log_w.max()
    ps = np.exp(log_w)
    ps /= ps.sum()
    mean_C = np.sum(ps * ns)
    S_G = np.log(ps.sum()) + bv * mean_C  # = log Z + beta*<C>, log Z=0 after normalisation
    # Actually S_G via log Z: Z = sum exp(-beta*n), log Z = log(sum exp(-beta*n))
    log_Z_val = np.log(np.sum(np.exp(-bv * ns)))
    S_G = log_Z_val + bv * mean_C

    # Finite-difference dS_G/d<C>
    eps = 1e-4
    ns2 = ns
    log_w2 = -(bv + eps) * ns2
    log_w2 -= log_w2.max()
    ps2 = np.exp(log_w2)
    ps2 /= ps2.sum()
    mean_C2 = np.sum(ps2 * ns2)
    log_Z2 = np.log(np.sum(np.exp(-(bv + eps) * ns2)))
    S_G2 = log_Z2 + (bv + eps) * mean_C2

    dS_dC = (S_G2 - S_G) / (mean_C2 - mean_C) if abs(mean_C2 - mean_C) > 1e-12 else float('nan')

    # Rate observable <R_hat> = 1 - <C>/N
    mean_R = np.sum(ps * (1 - ns / N_levels))
    one_minus_ratio = 1 - mean_C / N_levels

    err_leg = abs(dS_dC - bv) / bv if bv > 0 else 0
    err_rate = abs(mean_R - one_minus_ratio)
    errors_legendre.append(err_leg)
    errors_rate.append(err_rate)

    print(f"{bv:>8.2f} {mean_C:>8.3f} {dS_dC:>12.6f} {bv:>14.6f} {mean_R:>10.6f} {one_minus_ratio:>12.6f}")

print()
print(f"Max relative error in Legendre identity: {max(errors_legendre):.2e}  (numerical only)")
print(f"Max absolute error in <R_hat> = 1-<C>/C_max: {max(errors_rate):.2e}  (exact by linearity)")

# ────────────────────────────────────────────────────────────────────────────
# PART 4 — VERDICT
# ────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("PART 4: VERDICT")
print("=" * 70)
print("""
VERDICT: CONDITIONAL-YES (logistic envelope from MaxEnt + rate postulate)

Step-by-step:
  (a) MaxEnt on n=0,...,C_max with <C>=fixed gives Gibbs p_n=exp(-βn)/Z.
  (b) Legendre: dS_Gibbs/d<C> = β  [EXACT — no additional assumption].
  (c) Rate operator R̂ with R_n = (C_max-n)/C_max has <R̂> = 1-<C>/C_max
      [EXACT — linearity of expectation, no additional assumption].
  (d) If d<C>/dτ_R ≤ κ·<C>·<R̂>  [POSTULATE — physically motivated as
      capacity-limited complexity growth; this is M1 in v6.1 language]:
      dS/dτ_R = β · d<C>/dτ_R ≤ β·κ · C_k · (1 - C_k/C_k^max).
  (e) Identifying κ_R := β·κ yields Prop. 1 (eq:logistic) of v6.1.

Fermi-Dirac analogy status: ANALOGY (not isomorphism).
  - FD MaxEnt (binary levels) gives f_n with Pauli blocking (1-f_n).
  - Our Gibbs MaxEnt gives capacity factor (1-<C>/C_max) = <R̂>.
  - At mean-field level both equal 1/2 at half-filling/half-complexity.
  - The analogy is motivating and structurally sound as an ANALOGY;
    it should not be promoted to an exact mathematical identification.

Implication for v6.1:
  Prop. 1 logistic envelope is SUPPORTED by a 2-step MaxEnt argument
  (Legendre + capacity-rate postulate). The derivation strengthens M1
  from "Brown-Susskind analogy" to "MaxEnt + capacity-limited rate law".
  The step (d) remains a postulate (M1); the MaxEnt framing makes it
  more transparent, not less necessary.

  The inequality form (≤) is preserved throughout — V6-1 compliant.
  No cosmological prediction is made — V6-4 compliant.
  Claims are bounded by the derivation — rule 12 compliant.
""")
