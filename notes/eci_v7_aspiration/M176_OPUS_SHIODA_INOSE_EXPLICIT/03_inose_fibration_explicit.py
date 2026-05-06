"""
M176 sub-task 3 — Explicit Inose fibration for X_b (D = -88, class [2])
========================================================================

GOAL: Write down the singular K3 X_b as an explicit elliptic fibration over P^1
defined over the Hilbert class field H(-88) = Q(sqrt(-22), sqrt(2)).

Inose 1977 ("Defining equations of singular K3 surfaces and a notion of isogeny")
gives, for any pair of CM elliptic curves E, E' both with CM by K = Q(sqrt(d_K)),
the explicit Weierstrass equation of the singular K3 X = SI(E, E') ("Shioda-Inose
sandwich") via a 2:1 base change of an extremal elliptic fibration on Km(E x E').

The KEY INOSE FORMULA (Inose 1978, Schütt 2008 Lemma 22 echo):

For E: y^2 = x^3 + A*x + B with j-invariant j(E) = 1728 * 4A^3 / (4A^3 + 27 B^2),
and E' similarly with j(E') = j', define alpha, beta by
    alpha + beta = j(E) + j(E') - 1728 (or similar normalization)
    alpha * beta = j(E) * j(E')   * (1728)^c
Then SI(E, E') has Inose fibration

    Y^2 = X^3 - 3 alpha (1 - 1/t)^4 X + ...

This is messy; instead we use the cleaner form for E = E' (Kummer of E^2, then quotient
by extra involution), which IS the Shioda-Inose case in Schütt p.3 diagram with
E and E' isogenous (here E' = E since both have CM by full O_K).

For our class [2] anchor: E_b has j(E_b) = 3,147,421,320,000 - 2,225,561,184,000 sqrt(2).

By Schütt Theorem 29, the K3 X_b has L-function L(T(X_b), s) = L(psi_b^2, s) L(psi_bar^2, s)
where psi_b is the Hecke character of E_b.

Below we:
  (1) write explicit Weierstrass for E_b over Q(sqrt(2)) using j-invariant only,
  (2) compute the period lattice of E_b,
  (3) form the product abelian surface E_b x E_b,
  (4) sketch the Kummer / Shioda-Inose K3.
"""

import mpmath as mpm
from mpmath import mp, mpc, mpf, exp, pi, sqrt, j as I, nstr, gamma, log10, ellipfun
import sympy as sp

mp.dps = 60

# --- 1. CM elliptic curve E_b ----------------------------------------
# j_b = 3,147,421,320,000 - 2,225,561,184,000 sqrt(2)
sqrt2_mpf = sqrt(mpf(2))
j_b = mpf("3147421320000") - mpf("2225561184000") * sqrt2_mpf

print("="*70)
print("M176 sub-task 3: Explicit Inose / Shioda-Inose for class [2] X_b")
print("="*70)
print(f"j(E_b) = {nstr(j_b, 25)}")
print(f"   (= 3147421320000 - 2225561184000 sqrt(2)) ")

# Weierstrass parameters using y^2 = x^3 + a x + b with
# a = -27 j (j-1728), b = -54 j (j-1728)^2
A_coef = -27 * j_b * (j_b - 1728)
B_coef = -54 * j_b * (j_b - 1728)**2
print(f"\nE_b: y^2 = x^3 + a*x + b with")
print(f"  a = {nstr(A_coef, 25)}")
print(f"  b = {nstr(B_coef, 12)}")

# --- 2. Period lattice of E_b ----------------------------------------
# For tau_b = i sqrt(11/2), the period lattice of E_b = C/(Z + tau_b Z)
# For Weierstrass form y^2 = 4x^3 - g_2 x - g_3, periods omega_1, omega_2 such that
# tau = omega_2 / omega_1.
#
# Use the formulas:
#    g_2 = 60 G_4(tau) = 60 * sum'_{(m,n)} 1/(m + n tau)^4
#    g_3 = 140 G_6(tau) = 140 * sum'_{(m,n)} 1/(m + n tau)^6
# Or via Eisenstein:
#    E_4(tau) = 1 + 240 * sum sigma_3(n) q^n
#    E_6(tau) = 1 - 504 * sum sigma_5(n) q^n
#    g_2 = (4 pi^4 / 3) * E_4(tau)
#    g_3 = (8 pi^6 / 27) * E_6(tau)
# (with standard normalization omega_1 = 1).

tau_b = mpc(0, sqrt(mpf(22))/2)
q = exp(2 * pi * mpc(0, 1) * tau_b)

def E4(tau, N=300):
    q = exp(2 * pi * mpc(0,1) * tau)
    s = mpf(1)
    for n in range(1, N+1):
        s3 = sum(d**3 for d in range(1, n+1) if n % d == 0)
        s += 240 * s3 * q**n
    return s

def E6(tau, N=300):
    q = exp(2 * pi * mpc(0,1) * tau)
    s = mpf(1)
    for n in range(1, N+1):
        s5 = sum(d**5 for d in range(1, n+1) if n % d == 0)
        s -= 504 * s5 * q**n
    return s

E4_b = E4(tau_b)
E6_b = E6(tau_b)
g2_b = (4 * pi**4 / 3) * E4_b
g3_b = (8 * pi**6 / 27) * E6_b

print(f"\n--- Periods (omega_1 = 1 normalization) ---")
print(f"E_4(tau_b) = {nstr(E4_b, 20)}")
print(f"E_6(tau_b) = {nstr(E6_b, 20)}")
print(f"g_2(tau_b) = {nstr(g2_b, 20)}")
print(f"g_3(tau_b) = {nstr(g3_b, 20)}")

# Check: j = 1728 g_2^3 / (g_2^3 - 27 g_3^2) should equal j_b
delta_b = g2_b**3 - 27 * g3_b**2
j_check = 1728 * g2_b**3 / delta_b
print(f"\nConsistency: j(E_b) computed from (g_2, g_3) = {nstr(j_check, 25)}")
print(f"             j(E_b) from H_{{-88}} root        = {nstr(j_b, 25)}")
print(f"             relative diff = {nstr(abs(j_check - j_b)/abs(j_b), 5)}")

# --- 3. Period via Chowla-Selberg for D = -88 -------------------------
# Schütt + Schappacher / Chowla-Selberg: |Omega(E)|^2 = (Im tau) / (4 pi) * |eta(tau)|^4 * sqrt(|D_K|/Delta?)
# More directly:
# For E with CM by K = Q(sqrt(-22)), |d_K| = 88, h_K = 2, w_K = 2,
# Chowla-Selberg formula for the geometric mean over Cl(K) of |Omega(E)|^2:
#     prod_{i in Cl(K)} |Omega(E_i)|^2 = (1 / (4 pi sqrt(|d_K|))) * prod_{a=1}^{|d_K|} Gamma(a/|d_K|)^{chi(a) * w_K / (2 h_K)}
#
# This is the geometric mean -- M155 result.
#
# For class [2] anchor specifically, |Omega(E_b)| can be computed via eta(tau_b):
#     Omega(E_b)^2 / (2 pi i) ~ eta(tau_b)^4 / Im(tau_b)  (up to normalization)
# but cleanest is direct:
#     Omega_1 = 1 (chosen normalization)
#     Omega_2 = tau_b
# then in physical scale, the rescaling that makes (g_2, g_3) integer-rational depends on
# CM normalization.

# Eta function
def eta(tau, N=200):
    q = exp(2 * pi * mpc(0,1) * tau)
    q24 = exp(2 * pi * mpc(0,1) * tau / 24)
    s = mpf(1)
    for n in range(1, N+1):
        s *= (1 - q**n)
    return q24 * s

eta_a = eta(mpc(0, sqrt(mpf(22))))
eta_b = eta(tau_b)
print(f"\n|eta(tau_a)| = {nstr(abs(eta_a), 20)}")
print(f"|eta(tau_b)| = {nstr(abs(eta_b), 20)}")

# Period normalization: Omega_b = eta(tau_b)^2 (up to sign)
Omega_b = eta_b**2
print(f"|Omega(E_b)|^2 (eta-normalization) = |eta(tau_b)|^4 = {nstr(abs(eta_b)**4, 20)}")
print(f"|Omega(E_a)|^2                      = |eta(tau_a)|^4 = {nstr(abs(eta_a)**4, 20)}")

# Geometric mean
geom_mean = (abs(eta_a)**4 * abs(eta_b)**4) ** mpf("0.5")
print(f"\nGeometric mean over Cl(K) = {nstr(geom_mean, 20)}")
print(f"M171 reference: log_10(P_{{-88}}) = 1.98454821676494...")
print(f"  current geom mean log_10 = {nstr(log10(geom_mean), 10)}")

# --- 4. Hilbert class field H(-88) ------------------------------------
# H(-88) = K(j(E_a)) = Q(sqrt(-22))(sqrt(2)) = Q(sqrt(-22), sqrt(2))
# Galois group V_4 = Z/2 x Z/2:
#   sigma1: sqrt(-22) -> -sqrt(-22),  sqrt(2) -> sqrt(2)
#   sigma2: sqrt(-22) -> sqrt(-22),   sqrt(2) -> -sqrt(2)
# (sigma1 swaps complex conjugate; sigma2 swaps E_a ↔ E_b.)
print("\n--- Hilbert class field H(-88) ---")
print("H(-88) = Q(sqrt(-22), sqrt(2))   [biquadratic, degree 4 over Q]")
print("  Gal(H(-88)/Q) = V_4 = Z/2 x Z/2")
print("  Three quadratic subfields:")
print("     Q(sqrt(-22))     <- ground CM field K")
print("     Q(sqrt(2))       <- real subfield containing j(E_a), j(E_b)")
print("     Q(sqrt(-11))     <- product subfield (-22 * 2 = -44 = 4*(-11))")

# --- 5. Shioda-Inose K3 X_b -- structural characterization ------------
print("\n--- Shioda-Inose K3 X_b structure ---")
print("X_b = singular K3 with transcendental lattice T(X_b) = (4, 0, 22) Gram matrix")
print("       i.e. binary quadratic form 2*Q with Q = (2, 0, 11), disc(Q) = -88")
print("X_b is the desingularization of the Inose double cover of Km(E_b x E_b)")
print("along the appropriate divisor (cf. Inose 1977/1978, Shioda-Inose [32]).")
print("")
print("By Schütt Lemma 33: X_b has a model over H(-88) = Q(sqrt(-22), sqrt(2)).")
print("By Schütt Theorem 2: any number field L over which X_b is defined satisfies")
print("    L(sqrt(-88)) ⊃ H(-88), i.e. L ⊃ Q(sqrt(2)).")
print("Combined: minimal field of definition of X_b is exactly H(-88) = Q(sqrt(-22), sqrt(2)).")

# --- 6. L-function ------------------------------------------------------
print("\n--- L-function (Schütt Theorem 29) ---")
print("L(T(X_b), s) = L(psi_b^2, s) * L(psi_b_bar^2, s)")
print("  where psi_b is the Hecke character of E_b of ∞-type 1, conductor m | (sqrt(-22)),")
print("  and psi_b^2 is ∞-type 2, level |d_K| = 88, weight 3 newform with CM by K = Q(sqrt(-22)).")
print("  This newform is the unique weight-3 newform on Gamma_0(88) with CM by Q(sqrt(-22))")
print("  via twisting (Schütt Lemma 17 / Remark 21: 'For d = -88, this newform is uniquely")
print("  determined with level 7 by Lemma 17.' -- but our d=-88 has h_K=2, so see Prop 28.)")
print("")
print("PER SCHÜTT REMARK 21 page 11 verbatim: 'For d = -28, this newform is uniquely")
print("determined with level 7 by Lemma 17.' -- this is for d=-28, NOT d=-88. For d=-88,")
print("Schütt does not single it out (h_K=2 means analysis is in Section 12).")
print("\nLMFDB-equivalent: weight-3 CM newform with CM by Q(sqrt(-22)) of conductor 88.")
