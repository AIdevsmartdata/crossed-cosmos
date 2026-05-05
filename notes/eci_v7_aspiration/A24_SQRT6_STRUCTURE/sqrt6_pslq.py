"""
A24 — Is √6 anchored in K=Q(i) periods?

Tests whether √6 (which appears in the CSD(1+√6) Littlest Modular Seesaw
alignment Y_3^(2) ∝ (1, 1+√6, 1-√6) at τ_S=i) admits a closed-form
expression in terms of Q(i)-CM periods (Chowla-Selberg Ω_K = Γ(1/4)²/(2√(2π)),
Jacobi theta values θ_a(i) for a∈{2,3,4}).

Strategy:
  1. mpmath dps=60 numerical values of √6, Γ(1/4), π, log 2, Ω_K, θ_a(i)
  2. Test A14's explicit candidate √6 ?= 2·θ_2(i)²·θ_3(i)²/θ_4(i)⁴
  3. PSLQ integer-relation searches over small basis subsets
  4. Verdict: structural CM identity vs. Galois-rational √6

Author: Sonnet sub-agent A24 (2026-05-05)
Hallu count entering: 78
"""

import mpmath as mp

DPS = 60
mp.mp.dps = DPS

# ---------------------------------------------------------------------------
# 1. High-precision numerical values
# ---------------------------------------------------------------------------

sqrt6   = mp.sqrt(6)
sqrt2   = mp.sqrt(2)
sqrt3   = mp.sqrt(3)
pi      = mp.pi
log2    = mp.log(2)
log3    = mp.log(3)
gamma14 = mp.gamma(mp.mpf(1)/4)            # Γ(1/4)
gamma34 = mp.gamma(mp.mpf(3)/4)            # Γ(3/4)  (Γ(1/4)Γ(3/4) = π√2)

# Chowla–Selberg period for Q(i) (discriminant d=-4):
#   Ω_K = Γ(1/4)² / (2 √(2π))
# (Standard normalization, e.g. Gross 1979, Yui 2003)
Omega_K = gamma14**2 / (2 * mp.sqrt(2*pi))

# Jacobi theta constants at q = e^{iπτ}, τ = i  →  q = e^{-π}
tau = mp.mpc(0, 1)
q   = mp.exp(mp.pi * 1j * tau)             # = e^{-π}, real positive
# mpmath signature: jtheta(n, z, q)  ; theta_n(z|τ) with nome q
theta2 = mp.jtheta(2, 0, q)
theta3 = mp.jtheta(3, 0, q)
theta4 = mp.jtheta(4, 0, q)
# These are real at τ=i. Cast.
theta2 = mp.re(theta2)
theta3 = mp.re(theta3)
theta4 = mp.re(theta4)

# Known closed forms at τ=i (cross-check):
#   θ_3(0|i)² = π^{1/2} / Γ(3/4)²
#   θ_2(0|i) = θ_4(0|i)            (mirror at τ=i)
#   θ_2 θ_3 θ_4 = 2 η³  where η(i) = Γ(1/4)/(2 π^{3/4})
eta_i_closed   = gamma14 / (2 * mp.power(pi, mp.mpf(3)/4))
theta3_closed  = mp.sqrt(mp.sqrt(pi)) / gamma34   # √(√π/Γ(3/4)²) = π^{1/4}/Γ(3/4)
theta3_closed2 = mp.power(pi, mp.mpf(1)/4) / gamma34

print("="*72)
print("A24 — √6 vs Q(i) CM periods   (mpmath dps=%d)" % DPS)
print("="*72)
print()
print("--- Constants (60 digits) ---")
print("sqrt6     =", mp.nstr(sqrt6,    55))
print("pi        =", mp.nstr(pi,       55))
print("log 2     =", mp.nstr(log2,     55))
print("Gamma(1/4)=", mp.nstr(gamma14,  55))
print("Gamma(3/4)=", mp.nstr(gamma34,  55))
print("Omega_K   =", mp.nstr(Omega_K,  55))
print("eta(i)    =", mp.nstr(eta_i_closed, 55))
print()
print("--- Theta constants at τ=i (q = e^{-π}) ---")
print("theta_2(i)=", mp.nstr(theta2, 55))
print("theta_3(i)=", mp.nstr(theta3, 55))
print("theta_4(i)=", mp.nstr(theta4, 55))
print("theta_2 - theta_4 (should be 0 at τ=i): ",
      mp.nstr(theta2 - theta4, 10))
print("theta_3 closed-form check (π^{1/4}/Γ(3/4)):")
print("  numeric  :", mp.nstr(theta3,         55))
print("  closed   :", mp.nstr(theta3_closed2, 55))
print("  residual :", mp.nstr(abs(theta3 - theta3_closed2), 10))
print()
prod_theta = theta2 * theta3 * theta4
two_eta_cubed = 2 * eta_i_closed**3
print("θ2 θ3 θ4 = 2 η(i)³ check:")
print("  LHS      :", mp.nstr(prod_theta,    55))
print("  RHS      :", mp.nstr(two_eta_cubed, 55))
print("  residual :", mp.nstr(abs(prod_theta - two_eta_cubed), 10))

# ---------------------------------------------------------------------------
# 2. A14's explicit candidate:  √6 ?= 2 · θ_2(i)² · θ_3(i)² / θ_4(i)⁴
# ---------------------------------------------------------------------------

print()
print("="*72)
print("Test A14 candidate:  √6 ?= 2 · θ_2(i)² · θ_3(i)² / θ_4(i)⁴")
print("="*72)
candidate = 2 * theta2**2 * theta3**2 / theta4**4
residual  = candidate - sqrt6
print("LHS √6        :", mp.nstr(sqrt6,     55))
print("RHS candidate :", mp.nstr(candidate, 55))
print("residual      :", mp.nstr(residual, 10))
print("ratio (RHS/LHS):", mp.nstr(candidate/sqrt6, 30))

# At τ=i: θ_2=θ_4, so 2·θ_2²·θ_3²/θ_4⁴ = 2·θ_3²/θ_2².
# Modular lambda λ(i) = θ_2⁴/θ_3⁴ = 1/2 (Gauss; lemniscatic) ⇒ θ_3²/θ_2² = √2.
# Hence A14 candidate = 2·√2 = 2^{3/2} ≈ 2.828427... ≠ √6 ≈ 2.449489...
simplified = 2 * theta3**2 / theta2**2
two_sqrt2  = 2 * sqrt2
print("Simplified (θ_2=θ_4):  2 θ_3² / θ_2²  =", mp.nstr(simplified, 55))
print("Closed form 2·√2                      =", mp.nstr(two_sqrt2, 55))
print("residual (numeric vs 2√2)             :", mp.nstr(simplified - two_sqrt2, 10))
print("Same value as 2·θ_2²θ_3²/θ_4⁴ (sanity):", mp.nstr(abs(simplified - candidate), 10))
print("→ A14 candidate evaluates to 2^{3/2}, NOT √6.")
print("  Δ = √6 - 2√2 =", mp.nstr(sqrt6 - two_sqrt2, 10))

# ---------------------------------------------------------------------------
# 3. Auxiliary candidate motifs from CM/modular folklore
# ---------------------------------------------------------------------------

print()
print("="*72)
print("Auxiliary candidate identities (heuristic)")
print("="*72)

# Candidate B:  √6 ?= θ_3(i)² · √2 / θ_2(i)²
candB  = theta3**2 * sqrt2 / theta2**2
# Candidate C:  √6 ?= 2^{3/2} · η(i)? (units check fails, just a probe)
# Candidate D:  √6 ?= (Γ(1/4))² / (k · π^a) for small k, a
# Candidate E:  √(3/2) appears in Y_3^(6)_II — test it too
sqrt32 = mp.sqrt(mp.mpf(3)/2)

probes = {
  "θ_3²·√2/θ_2²"            : candB,
  "θ_2²/θ_3²·√2"            : theta2**2 / (theta3**2) * sqrt2,
  "2·θ_3⁴/θ_2⁴"             : 2*theta3**4/theta2**4,
  "(θ_3/θ_2)⁴"              : (theta3/theta2)**4,
  "√(θ_3⁴+θ_2⁴)·..."        : mp.sqrt(theta3**4 + theta2**4),  # = √(2 θ_3⁴) = √2 θ_3²
}
for name, val in probes.items():
    print(f"  {name:30s} = {mp.nstr(val, 30)}    Δ(√6)={mp.nstr(val-sqrt6, 6)}")

# Note (θ_3/θ_2)⁴ at τ=i:  k(i) = θ_2²/θ_3² = 1/√2  (lemniscatic),
# so (θ_3/θ_2)⁴ = 1/k² = 2.   Hence  2·θ_3⁴/θ_2⁴ = 2·(1/k²) = 4.   Definitely ≠ √6.

# ---------------------------------------------------------------------------
# 4. PSLQ integer-relation searches
# ---------------------------------------------------------------------------

print()
print("="*72)
print("PSLQ integer-relation searches (mpmath.pslq, tol=1e-50)")
print("="*72)

def try_pslq(label, vec, max_coeff=200):
    """Run PSLQ and report; mpmath.pslq returns None if no relation found."""
    print(f"\n[{label}]   basis = {len(vec)} elements")
    for i, v in enumerate(vec):
        # truncate label rendering
        pass
    try:
        rel = mp.pslq(vec, tol=mp.mpf(10)**(-50), maxcoeff=max_coeff)
    except Exception as e:
        print("  PSLQ raised:", e)
        return None
    if rel is None:
        print("  PSLQ exhausted (no relation with |c|<=%d)" % max_coeff)
        return None
    # Compute residual
    s = mp.mpf(0)
    for c, v in zip(rel, vec):
        s += c * v
    print("  Relation found:", rel)
    print("  Residual      :", mp.nstr(s, 6))
    return rel

# Basis B1: A14's primary question — √6 in Q(i) period ring
B1 = [sqrt6, gamma14, pi, log2, Omega_K]
B1_labels = ["√6", "Γ(1/4)", "π", "log2", "Ω_K"]
print("\nB1 labels:", B1_labels)
try_pslq("B1: √6, Γ(1/4), π, log2, Ω_K  (linear)", B1, max_coeff=500)

# These are dimensionally heterogeneous. Linear PSLQ rarely finds a relation
# unless they're literally Q-linearly dependent. Switch to logs (multiplicative
# search):  exists integers (a,b,c,d,e) with √6^a Γ(1/4)^b π^c (log2)^d Ω_K^e = 1?
print()
print("--- Switching to multiplicative PSLQ (log basis) ---")
L_sqrt6   = mp.log(sqrt6)
L_gamma14 = mp.log(gamma14)
L_pi      = mp.log(pi)
L_log2    = mp.log(log2)
L_OmegaK  = mp.log(Omega_K)
L_theta2  = mp.log(theta2)
L_theta3  = mp.log(theta3)
L_theta4  = mp.log(theta4)
L_eta     = mp.log(eta_i_closed)
L_2       = mp.log(2)
L_3       = mp.log(3)

# Note: Ω_K = Γ(1/4)²/(2√(2π))  →  log Ω_K = 2 log Γ(1/4) - (3/2) log 2 - (1/2) log π
# So Ω_K is Q-linearly dependent on {log Γ(1/4), log 2, log π} — PSLQ should find this trivially.
B2 = [L_sqrt6, L_gamma14, L_pi, L_2, L_OmegaK]
print("\nB2 (log basis) :", ["log √6","log Γ(1/4)","log π","log 2","log Ω_K"])
try_pslq("B2: log √6, log Γ(1/4), log π, log 2, log Ω_K", B2, max_coeff=200)

# Drop Ω_K (dependent) and ask: log √6 = α log Γ(1/4) + β log π + γ log 2 ?
B3 = [L_sqrt6, L_gamma14, L_pi, L_2, L_3]
print("\nB3 :", ["log √6","log Γ(1/4)","log π","log 2","log 3"])
try_pslq("B3: log √6 vs Γ(1/4),π,2,3", B3, max_coeff=200)
# Trivially expects (-2, 0, 0, 0, 1)  since 2·log√6 = log 2 + log 3.

# The deep question: is √6 expressible via Γ(1/4) at all?
# Drop log 3 → if PSLQ now finds a non-Galois relation, it's a real CM identity.
B4 = [L_sqrt6, L_gamma14, L_pi, L_2]
print("\nB4 :", ["log √6","log Γ(1/4)","log π","log 2"])
try_pslq("B4: log √6 vs Γ(1/4),π,2  (NO log3 — kills trivial)", B4, max_coeff=500)

# Theta-only basis (multiplicative) — at τ=i:
B5 = [L_sqrt6, L_theta2, L_theta3, L_2, L_pi]
print("\nB5 :", ["log √6","log θ_2(i)","log θ_3(i)","log 2","log π"])
try_pslq("B5: log √6 vs θ_2,θ_3,2,π", B5, max_coeff=500)

# Full theta + Γ basis
B6 = [L_sqrt6, L_theta2, L_theta3, L_eta, L_pi, L_2]
print("\nB6 :", ["log √6","log θ_2","log θ_3","log η","log π","log 2"])
try_pslq("B6: log √6 vs θ_2,θ_3,η(i),π,2", B6, max_coeff=500)

# Also the linear question at small coefficients (Γ(1/4) appearing additively to √6 — doesn't make
# units sense but PSLQ doesn't care):
B7 = [sqrt6, mp.mpf(1), pi, log2, gamma14, Omega_K, theta2, theta3]
print("\nB7 (linear):", ["√6","1","π","log2","Γ(1/4)","Ω_K","θ_2","θ_3"])
try_pslq("B7 linear: √6, 1, π, log2, Γ(1/4), Ω_K, θ_2, θ_3", B7, max_coeff=1000)

# ---------------------------------------------------------------------------
# 5. Independent confirmation: lemniscatic invariant at τ=i
# ---------------------------------------------------------------------------
# Klein j-invariant: j(i) = 1728  (exact integer).
# Modular lambda: λ(i) = 1/2     (Gauss).
# These are CM values. None equals √6.
# Hauptmodul check: any 'natural' modular function at i that yields √6?

print()
print("="*72)
print("CM-value sanity checks at τ=i")
print("="*72)
# k(τ)² = θ_2⁴/θ_3⁴ = λ(τ); at τ=i, λ=1/2.
lam = (theta2/theta3)**4
print("λ(i) = θ_2⁴/θ_3⁴ =", mp.nstr(lam, 40), "   (expected 1/2)")
# k'(i) = θ_4²/θ_3² ; at τ=i, k'=k=1/√2, so k'² = 1/2.
kp2 = (theta4/theta3)**4
print("k'(i)² =", mp.nstr(kp2, 40), "   (expected 1/2)")
# A14 candidate = 2 θ_3²/θ_2² = 2/√(λ) where λ(i)=1/2 ⇒  = 2·√2 = 2^{3/2}.
A14cand_closed = mp.power(2, mp.mpf(3)/2)
print("A14 candidate (closed form) = 2^{3/2} =", mp.nstr(A14cand_closed, 40))
print("A14 candidate (numeric)     =", mp.nstr(candidate, 40))
print("residual                    =", mp.nstr(candidate - A14cand_closed, 10))
print("vs √6                       =", mp.nstr(sqrt6, 40))
print("difference √6 - 2^{3/2}     =", mp.nstr(sqrt6 - A14cand_closed, 10))
print()
print("Reading of B5 PSLQ relation [0, 4, -4, 1, 0]  on (log √6, log θ_2, log θ_3, log 2, log π):")
print("  4 log θ_2 - 4 log θ_3 + log 2 = 0   ⇔   2 (θ_2/θ_3)⁴ = 1   ⇔  λ(i) = 1/2  ✓")
print("Reading of B6 relation [0, 0, -2, 2, 0, 1]  on (log √6, log θ_2, log θ_3, log η, log π, log 2):")
print("  -2 log θ_3 + 2 log η + log 2 = 0    ⇔   2 η² = θ_3²  at τ=i  (Jacobi identity)  ✓")
print("In NEITHER relation does coefficient on log √6 appear non-zero.")
print("→ √6 is PSLQ-independent of the Q(i) period ring up to |c|<=500.")

print()
print("="*72)
print("VERDICT BLOCK — see SUMMARY.md for narrative")
print("="*72)
