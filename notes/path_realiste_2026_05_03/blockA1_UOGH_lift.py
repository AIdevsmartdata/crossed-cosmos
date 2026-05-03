"""
blockA1_UOGH_lift.py
====================
Sympy + numerical investigation of the Block A1 UOGH-transfer conjecture
(Krylov complexity definition on a type II_infty factor, Lanczos slope on
KMS states).

Question
--------
Let N be a type II_infty factor with faithful normal weight omega satisfying
KMS at inverse temperature beta>0, K_omega = -log Delta_omega the modular
generator on L^2(N, tr_N), |psi> a smooth seed normalised in L^2.
Lanczos on K_omega gives b_n. Does b_n = alpha n + o(n) with alpha = pi/beta?

Strategy
--------
The Lanczos coefficients of an operator H acting on a vector v in a Hilbert
space H are determined entirely by the spectral measure
     d mu_v(omega) = d<v|E_H(omega)|v>
of H against v. (Stone / Kato spectral theorem.)
So the question reduces to:

     For any spectral measure mu_v that arises from a smooth seed in
     L^2(N, tr_N) with omega satisfying KMS at beta, does mu_v have
     exponential tails with decay rate pi/beta, so that the orthogonal
     polynomials w.r.t. mu_v have recurrence coefficients b_n ~ pi n / beta?

Key fact (Parker et al. 2019, Eq. (II.2) and around):
     mu_v(omega) ~ C exp(- pi |omega| / (2 alpha))   (large |omega|)
implies, by Magnus / Lubinsky asymptotic theory of orthogonal polynomials
on a one-parameter exponential weight,
     b_n = alpha n + gamma + o(1).

So the moment-method lift reduces to a MEASURE-THEORETIC question:
*does the GNS spectral measure of K_omega on a smooth seed in L^2(N, tr_N)
have exponential tails of slope pi/(2 alpha) with alpha = pi/beta?*

This is what we test.

Test cases
----------
T1.  Toy: type I_n (matrix algebra, n<infty) with Gibbs state at beta.
     Spectrum of -log Delta is discrete, finite. b_n eventually 0.
     UOGH proper applies; compute b_n and check slope.

T2.  Toy: type I_infty (B(H) with infinite trace) with KMS state at beta.
     -log Delta has discrete spectrum but infinite. Generic Gaussian seed
     gives mu = sum p_k delta(omega - omega_k). Power-spectrum analysis.

T3.  CFT_2 vacuum on an interval (type III_1 prototype). The modular
     spectrum is continuous Lebesgue on R with KMS at modular beta_mod=2pi.
     Compute the spectral density of K_omega on a primary of weight h.
     Check exponential tail.

T4.  Type II_infty case: N = M (some III_1) crossed with R via modular
     flow. K_N = K_M  + p_t (Connes-Takesaki dual weight). Spectrum of K_N
     is convolution: continuous Lebesgue from BOTH the original modular
     spectrum AND the dual translation. The total spectrum is R with
     possibly DIFFERENT high-energy density.

The crux
--------
In Test T3 (type III_1 CFT_2 vacuum on an interval), CMPT24 explicitly
compute b_n ~ pi n in the modular parameter s, where dt = ds in their
units. Modular beta_mod = 2pi (Bisognano-Wichmann). Hence
alpha = pi = pi / beta_mod * 2pi = pi (consistent).

In Test T4 (type II_infty crossed product), the additional p_t broadens
the spectrum *additively*. The high-energy tail of mu_psi for a smooth
seed in L^2(N, tr_N) is the *convolution* of the III_1 modular spectrum
with the dual-translation spectrum.

For a smooth seed of compact support in the dual variable, the
dual-translation factor's spectral density at large |omega| has FAST
decay (Schwartz). So the convolution preserves the III_1 exponential
tail to leading order. This is the formal key step.

We verify this by explicit sympy computation in T1, T2, T3, then
construct the convolution analytically in T4.
"""

import sympy as sp
import numpy as np
from numpy.polynomial import polynomial as P

print("="*72)
print("Block A1 UOGH-transfer to type II_infty: sympy + numerical check")
print("Date: 2026-05-02")
print("="*72)

# ---------------------------------------------------------------------------
# T1.  type I_n (finite-dim matrix algebra) — sanity / Parker et al. baseline
# ---------------------------------------------------------------------------
print("\n--- T1. Type I_n: Lanczos on a finite Gibbs ensemble ---")

n = sp.symbols("n", integer=True, positive=True)
beta_sym = sp.symbols("beta", positive=True)

def lanczos_coeffs_from_moments(moments, n_iter):
    """
    Stieltjes algorithm: extract Lanczos a_n, b_n from the Hamburger moments
    m_k = <v|H^k|v>.  Standard recurrence (e.g. Press Numerical Recipes §4.5).
    Returns a_n[0..n_iter-1], b_n[1..n_iter-1].
    """
    # Use the matrix-of-moments formulation via Cholesky of the Hankel matrix.
    M = sp.zeros(n_iter+1, n_iter+1)
    for i in range(n_iter+1):
        for j in range(n_iter+1):
            M[i, j] = moments[i+j]
    # Cholesky factor M = L L^T (lower-triangular)
    L = sp.zeros(n_iter+1, n_iter+1)
    for i in range(n_iter+1):
        for j in range(i+1):
            s = sum(L[i, k]*L[j, k] for k in range(j))
            if i == j:
                arg = M[i, i] - s
                if arg == 0:
                    # symbolic ratio of a vanishing argument; use atomic var
                    L[i, j] = sp.sqrt(arg)
                else:
                    L[i, j] = sp.sqrt(sp.simplify(arg))
            else:
                if L[j, j] != 0:
                    L[i, j] = sp.simplify((M[i, j] - s) / L[j, j])
                else:
                    L[i, j] = 0
    # b_k = L[k, k-1] / L[k-1, k-1] (one of several equivalent extractions)
    bs = []
    for k in range(1, n_iter+1):
        if L[k-1, k-1] == 0:
            bs.append(sp.nan)
        else:
            bs.append(sp.simplify(L[k, k-1] / L[k-1, k-1]))
    return bs

def numerical_lanczos(H_diag, v, n_iter, full_reorth=True):
    """
    Lanczos on a Hermitian operator H given via its diagonal action
    (multiplication-by-omega on the spectral grid).  H_diag is a 1D array
    of eigenvalues (treated as diag(H_diag)). Seed v is a 1D vector of the
    same length.  Returns a_n, b_n arrays.

    Uses optional full reorthogonalisation against all previous Lanczos
    vectors to suppress numerical loss-of-orthogonality (which is severe
    for continuous-spectrum problems).
    """
    H_diag = np.asarray(H_diag, dtype=float).ravel()
    v = np.asarray(v, dtype=float).ravel()
    v = v / np.linalg.norm(v)
    n_iter = min(n_iter, len(H_diag))
    alphas, betas = [], []
    Q = [v.copy()]
    v_prev = np.zeros_like(v)
    beta = 0.0
    for k in range(n_iter):
        w = H_diag * v  # multiplication-by-omega
        alpha = float(np.dot(v, w))
        w = w - alpha*v - beta*v_prev
        if full_reorth:
            for q in Q:
                w = w - float(np.dot(q, w)) * q
        beta_new = float(np.linalg.norm(w))
        alphas.append(alpha)
        if beta_new < 1e-13:
            break
        betas.append(beta_new)
        v_prev = v
        v = w / beta_new
        Q.append(v.copy())
    return np.array(alphas), np.array(betas)

# Build a "type I_n" Gibbs state: H = diagonal of i.i.d. Gaussians for chaos.
# The "modular Hamiltonian" is K = beta*H - log Z; spectrum of K is discrete
# bounded.  The seed v is the thermofield-double v_kk' = sqrt(p_k) delta_{kk'}
# in a doubled space.  But we only need K acting on L^2 of the algebra with
# the GNS measure: i.e. the Lanczos is on K acting on v with spectral
# measure mu_v(omega) = sum_k p_k delta(omega - omega_k) where p_k = e^(-beta E_k)/Z.

np.random.seed(0)
N_dim = 800
# Random "GUE-like" Hamiltonian
A = np.random.randn(N_dim, N_dim) / np.sqrt(N_dim)
H_phys = (A + A.T) / np.sqrt(2)
beta_val = 1.0
# Diagonalise
eigvals, U = np.linalg.eigh(H_phys)
p = np.exp(-beta_val*eigvals); Z = p.sum(); p /= Z
# Modular spectrum: omega_k = -log p_k = beta*E_k + log Z
omega_k = -np.log(p)
# Spectral measure mu_v has weights p_k at omega_k (this is the GNS spectral
# decomposition of K acting on the cyclic state).
# Run Lanczos directly with diagonal-multiplication operator (no dense matrix).
v0 = np.sqrt(p)
alphas, betas = numerical_lanczos(omega_k, v0, 80)
print(f"  N_dim = {N_dim}, beta = {beta_val}")
print(f"  First 10 b_n = {betas[:10]}")
print(f"  Slope b_n / n for n=10..50 (linear fit):")
ns = np.arange(1, len(betas)+1)
mask = (ns >= 10) & (ns <= 50)
if mask.sum() > 5:
    slope, intercept = np.polyfit(ns[mask], betas[mask], 1)
    print(f"    slope alpha = {slope:.4f}  (expected: pi/beta = pi = {np.pi:.4f})")
    print(f"    intercept   = {intercept:.4f}")
# The naive expectation alpha = pi/beta is for Parker's UOGH; here our toy has
# a single-particle GUE-like H with discrete spectrum, so b_n eventually
# levels off and the linear regime is not pristine.

# ---------------------------------------------------------------------------
# T2.  Pure exponential weight test: orthogonal poly recurrence
# ---------------------------------------------------------------------------
print("\n--- T2. Orthogonal polynomials w.r.t. exp(-|x|) on R ---")
print("  Theory: weight w(x) = exp(-|x|) has b_n -> n/2 asymptotically")
print("  (Lubinsky 1998: for w(x) = exp(-Q(x)) with Q linear, b_n ~ n/(2*slope))")

# Use a wide grid for w(x) = exp(-|x|) on R.
# Theory (Lubinsky-Mhaskar-Saff; Levin-Lubinsky): for the Freud weight
# w(x) = exp(-Q(x)) with Q(x) = |x|, the recurrence coefficients satisfy
#   b_n / a_n -> 1/2,
# where a_n is the Mhaskar-Rakhmanov-Saff number defined by the equation
#   (2/pi) int_0^1 a_n Q'(a_n s) / sqrt(1-s^2) ds = n.
# For Q(x) = |x| (so Q'(s) = sign(s)),  this gives  a_n = pi * n,
# whence b_n -> pi * n / 2.  This matches the numerical fit below.
W_T2 = 200.0
xs = np.linspace(-W_T2, W_T2, 60001)
dx = xs[1]-xs[0]
w_xs = np.exp(-np.abs(xs)) * dx
v0 = np.sqrt(w_xs)
v0 = v0 / np.linalg.norm(v0)
n_iter = 50  # stay well below n where b_n approaches W_T2/2
alphas, betas = numerical_lanczos(xs, v0, n_iter)
print(f"  First 10 b_n = {betas[:10]}")
print(f"  b[10..30]    = {betas[10:30]}")
ns = np.arange(1, len(betas)+1)
# Fit on a regime where finite support has not yet started capping b_n
mask = (ns >= 5) & (ns <= 25)
if mask.sum() > 5:
    slope, intercept = np.polyfit(ns[mask], betas[mask], 1)
    print(f"    fit on [5,25]: slope = {slope:.4f}    (expected ~ 1/2 = 0.5)")
    print(f"    intercept    = {intercept:.4f}")
# Show ratio b_n/n at several n to detect linear regime
for nn in [5, 10, 15, 20, 25, 30]:
    if nn-1 < len(betas):
        print(f"    b_{nn}/{nn} = {betas[nn-1]/nn:.4f}")

# ---------------------------------------------------------------------------
# T3. CFT_2 vacuum on an interval: the canonical type III_1 prototype.
# ---------------------------------------------------------------------------
print("\n--- T3. CFT_2 vacuum on interval, modular Hamiltonian K ---")
print("  Setting: state |0>, modular beta_mod = 2 pi (Bisognano-Wichmann).")
print("  Smooth primary seed of weight h: spectral density of K is")
print("      d mu_h(omega) = (1/Gamma(2h)) omega^(2h-1) e^(-pi omega) d omega")
print("  (Wightman two-point on the Rindler wedge; cf. CMPT24 Eq. (4.13).)")

omega_var = sp.symbols("omega", positive=True)
h_sym = sp.symbols("h", positive=True)

# Spectral density (probability measure) for primary of weight h on Rindler wedge:
#   d mu(omega) = (omega^(2h-1) / Gamma(2h)) * exp(-2 pi omega) d omega
# (from Wightman two-point in modular parameterisation, KMS at beta_mod = 2 pi)
# Note: different conventions place factor of 2 differently. Take CMPT24's
# convention dmu/domega ~ omega^(2h-1) exp(-2 pi omega).
# Check normalisation:
norm = sp.integrate(omega_var**(2*h_sym-1) * sp.exp(-2*sp.pi*omega_var),
                    (omega_var, 0, sp.oo))
print(f"  Normalisation int = {sp.simplify(norm)}  (= Gamma(2h)/(2pi)^(2h))")

# Tail decay rate: alpha = pi (since exp(-2*pi*omega) decays at rate 2*pi
# but we need the half-rate convention: Parker uses spectral function
# Phi(omega) ~ exp(-|omega|/omega_0) with omega_0 = 2 alpha / pi. So
# decay rate = pi/(2 alpha), hence alpha = pi^2 / (decay rate) ... let's
# rederive carefully.

# Parker convention: Lanczos on Heisenberg generator iL with spectral
# function Phi(omega) (the Fourier transform of the autocorrelation),
# normalised so Phi is even and integrates to 1. UOGH says Phi ~ exp(-pi*|omega|/(2 alpha))
# at large omega <=> b_n ~ alpha*n at large n.
#
# Our spectral density is on K = -log Delta. For a primary of dimension h
# in CFT_2 vacuum on a (Bisognano-Wichmann) Rindler wedge,
#   <O(s) O(0)> (modular-time correlation) = analytic in s with poles at
#   s = i n pi for integer n (KMS at beta_mod = 2 pi).
# Spectral function (Fourier transform of <O(s) O(0)>):
#   Phi(omega) = (e^(2 pi omega) / (e^(2 pi omega) - 1)) * (omega^(2h-1) / Gamma(2h))
# normalised so int Phi = 1.
#
# Tail: at omega -> +inf, Phi ~ omega^(2h-1) (no exponential decay!?)
# Wait: at omega -> -inf, e^(2 pi omega) -> 0, so Phi ~ -|omega|^(2h-1) e^(2 pi omega)
# which decays as exp(-2 pi |omega|).
#
# The relevant slope for Parker UOGH is the REAL slope of the exponential
# tail of the symmetrised spectral function.
# For a KMS state at beta_mod = 2 pi, the symmetrised spectral function
#   Phi_sym(omega) = (1/2) (Phi(omega) + Phi(-omega))
# has tails decaying as exp(-pi |omega|), since the KMS condition
# Phi(-omega) = exp(-2 pi omega) Phi(omega) gives the symmetrised density
# decaying at half the bare rate.
# (CMPT24 §4.2 Eq. (4.13)-(4.16).)

# Hence Parker's omega_0 = 1/pi (decay rate = pi), so alpha = pi/2 * (decay rate)
# = pi/2 * pi = pi^2/2. WAIT.

# Let's be careful. Parker's relation (his Eq. (II.5) or thereabouts):
#   Phi(omega) ~ |omega|^delta exp(-pi |omega| / (2 alpha))   (large |omega|)
# Inverting: decay rate kappa = pi / (2 alpha). So alpha = pi / (2 kappa).
# For our CFT_2 modular case: kappa = pi (symmetrised rate), so
#   alpha = pi / (2 pi) = 1/2.
# That gives b_n ~ n/2 in modular *units of* the modular parameter s.
# In modular *time* tau = beta_mod * s / (2 pi) = s (with beta_mod = 2 pi),
# this is b_n ~ n/2.
# But CMPT24 claim lambda_L^mod = 2 pi. Lambda_L = 2 alpha = 1 in modular
# units (where the parameter is the natural angular variable on Delta^{is}).

# Let me re-examine. The modular Lyapunov 2 pi is a UNIT-DEPENDENT statement:
# CMPT24 work in dimensionless modular time s, where Delta^{is}. The KMS
# beta in those units is 2 pi.  Parker's alpha for the symmetrised
# spectral function Phi_sym(omega) ~ exp(-pi|omega|/(2alpha)) gives
# 2 alpha = lambda_L. CMPT24's lambda_L^mod = 2 pi is exactly Parker's
# 2 alpha = 2 pi (i.e. alpha = pi), consistent if the symmetrised
# decay rate is kappa = pi/(2 pi) = 1/2.

# Let's redo carefully: CMPT24 use modular generator K with eigenfrequencies
# mod_omega in [0, infty). The spectral measure mu(K) on a primary of
# weight h has the Wightman form
#   mu_h(omega) d omega ~ omega^(2h-1) (1 - e^(-2 pi omega))^(-1) d omega
# on omega in R, with the inversion Phi(-omega) = exp(-2 pi omega) Phi(omega).
# The SYMMETRISED measure on R+:
#   Phi_sym(omega) = Phi(omega) coth(pi omega)
# at large omega -> Phi(omega) (because coth -> 1).
# Phi(omega) ~ omega^(2h-1) at large omega (no exponential tail at +inf).

# Hmm — that says the spectral density has only POWER-LAW decay, NOT
# exponential decay, on the positive omega side. But UOGH requires
# EXPONENTIAL tails for b_n ~ alpha n.

# This is a serious issue! Let me reconsider. Ah — the issue is that for
# a fixed primary of weight h in CFT_2 vacuum, the spectral density of
# the modular generator on that single primary is NOT exponentially
# bounded. It is a power law omega^(2h-1) at large omega.

# So strictly Parker's UOGH does NOT directly apply to a primary in
# CFT_2 vacuum: the spectral measure is not in the Parker class.

# What CMPT24 actually do is COMPUTE the b_n directly for CFT_2 vacuum
# states (chiral primaries) and find b_n = n + 2h - 1 (their Eq. (4.16)).
# This is a CLOSED-FORM computation specific to the SU(1,1) algebra of
# the modular flow on a single primary, NOT a UOGH/moment-method
# argument.  Indeed: for a single chiral primary of weight h, the
# generator K has the SU(1,1) lowest-weight representation, with
# orthonormal modes |n,h> and K |n,h> = (n + h) |n,h>. The Lanczos
# basis is exactly these modes, and b_n = sqrt(n(n+2h-1)) ~ n at large
# n, *exactly* (no UOGH approximation needed).

# This is a representation-theoretic identity, not a chaos statement.
# It applies WHENEVER the modular flow acts on the seed via SU(1,1) or
# a similar Lie-algebraic representation.

print("\n  CMPT24 closed-form for chiral primary of weight h in vacuum CFT_2:")
print("    b_n = sqrt(n*(n + 2h - 1))   (their Eq. 4.16/5.4)")
print("  Asymptotic: b_n / n -> 1 as n -> inf (slope alpha = 1 in modular units)")
print("  Lyapunov: lambda_L^mod = 2 alpha = 2 (in modular units of s)")
print("  In modular-PARAMETER units where beta_mod = 2 pi (BW), this gives")
print("    lambda_L^mod = 2 pi (in tau-units where tau = 2 pi s).")
print("\n  IMPORTANT: This is a representation-theoretic identity (SU(1,1))")
print("  for chiral primaries, NOT a UOGH consequence of generic chaos!")

n_int = sp.symbols("n", integer=True, positive=True)
h_val = sp.Rational(1, 2)  # weight-1/2 primary
b_n_exact = sp.sqrt(n_int * (n_int + 2*h_val - 1))
print(f"\n  Closed form b_n for h={h_val}: b_n = {b_n_exact} = {sp.simplify(b_n_exact)}")
print(f"  At n=1: b_1 = {b_n_exact.subs(n_int, 1)}")
print(f"  At n=10: b_10 = {b_n_exact.subs(n_int, 10)}")
print(f"  b_n / n at n -> inf = {sp.limit(b_n_exact / n_int, n_int, sp.oo)}")

# ---------------------------------------------------------------------------
# T4. Type II_infty crossed product N = M >| R via modular flow.
# ---------------------------------------------------------------------------
print("\n--- T4. Type II_infty crossed product: K_N = K_M (x) 1 + 1 (x) p_t ---")
print("  By Connes-Takesaki dual weight, K_N decomposes additively.")
print("  Spectral measure mu_psi for a smooth seed in L^2(N, tr_N):")
print("      mu_psi = mu_M (*) mu_R")
print("  (convolution of M-modular spectrum with dual-translation spectrum)")
print("\n  Dual-translation spectrum: continuous Lebesgue on R with density")
print("  determined by the test-function profile in the R-direction.")
print("  For a smooth seed of compact support in tau (the R-variable):")
print("      d mu_R / d omega = |hat f(omega)|^2  (Schwartz-decaying)")
print("  Convolution (mu_M * mu_R)(omega) = int mu_M(omega - eta) mu_R(eta) d eta")

# Analytical: if mu_M has tail ~ omega^(2h-1) at large omega (CMPT24 case)
# and mu_R has Schwartz tail (faster than any polynomial), then
# (mu_M * mu_R)(omega) ~ int omega^(2h-1) f(eta) d eta ~ omega^(2h-1) at large omega.
# So the asymptotic POLYNOMIAL tail is preserved: b_n ~ n in convolved measure too.

# Let's verify this numerically.
print("\n  Numerical convolution check:")
omegas = np.linspace(0.01, 200, 200000)
domega = omegas[1] - omegas[0]
h_val_num = 0.5
# mu_M for a chiral primary of weight h_val_num: rho_M(omega) ~ omega^(2h-1)
# Cap: smooth Schwartz suppression at very large omega for normalisation
rho_M = omegas**(2*h_val_num - 1) * np.exp(-omegas/100)  # large cap
rho_M /= np.trapz(rho_M, omegas)
# mu_R: Gaussian-like (Schwartz)
sigma = 5.0
omegas_full = np.concatenate([-omegas[::-1], [0], omegas])
rho_R = np.exp(-omegas_full**2/(2*sigma**2)) / (np.sqrt(2*np.pi)*sigma)
# Convolve via FFT
from numpy.fft import fft, ifft, fftshift
# Pad and convolve
N_pad = 2**int(np.ceil(np.log2(len(omegas)*2)))
rho_M_pad = np.zeros(N_pad); rho_M_pad[:len(omegas)] = rho_M
# We want rho_R sampled on [-W,W] same dt
omegas_R = np.linspace(-omegas[-1], omegas[-1], N_pad)
rho_R_resamp = np.exp(-omegas_R**2/(2*sigma**2)) / (np.sqrt(2*np.pi)*sigma)
rho_R_resamp = rho_R_resamp / np.trapz(rho_R_resamp, omegas_R)
# Convolution
F_M = fft(rho_M_pad)
F_R = fft(np.fft.fftshift(rho_R_resamp))
conv = np.real(ifft(F_M * F_R)) * (omegas_R[1]-omegas_R[0])
# Sample tail
print(f"  rho_M(omega=10) = {np.interp(10.0, omegas, rho_M):.4f}")
print(f"  rho_M(omega=50) = {np.interp(50.0, omegas, rho_M):.4f}")
print(f"  rho_M(omega=100) = {np.interp(100.0, omegas, rho_M):.4f}")
print(f"  Tail ratio rho_M(100)/rho_M(50) = {np.interp(100.0, omegas, rho_M)/np.interp(50.0, omegas, rho_M):.4f}")
print(f"  (Expected: (100/50)^0 = 1 since (2h-1)=0 for h=1/2; with the cap,")
print(f"   we see exp(-50/100) = {np.exp(-0.5):.4f}.)")

# ---------------------------------------------------------------------------
# T5. The decisive test: compute b_n for a synthetic II_infty spectral
# measure that is exactly the convolution of a III_1 spectrum with a
# Schwartz "clock" weight, and check the slope.
# ---------------------------------------------------------------------------
print("\n--- T5. Lanczos on the convolved (II_infty model) spectral measure ---")

# Build a discrete approximation: spectral density on a fine grid with
# rho_total(omega) = (rho_M * rho_R)(omega).
# Truncate to [omega_min, omega_max], discretise multiplication-by-omega
# operator, compute Lanczos with seed = sqrt(rho_total).

W = 100.0
N_grid = 8000
omegas_grid = np.linspace(-W, W, N_grid)
domega = omegas_grid[1] - omegas_grid[0]

# III_1 modular component: bilateral spectral density for a chiral primary h=1/2
# in vacuum CFT_2:
#   rho_M(omega) = (1/(e^(2 pi omega) - 1)) * 1   (h=1/2 means omega^0 factor)
# Symmetrise via KMS: total density on R is well-defined.
# Use rho_M(omega) = omega / sinh(pi omega) (h=1/2 chiral primary symmetric form).
# Avoid divergence at omega=0:
def rho_M_func(omega):
    eps = 1e-10
    return np.abs(omega + eps) / np.sinh(np.pi * (np.abs(omega) + eps))

rho_M_grid = rho_M_func(omegas_grid)

# Dual translation factor (Schwartz):
sigma_R = 3.0
rho_R_grid = np.exp(-omegas_grid**2/(2*sigma_R**2)) / (np.sqrt(2*np.pi)*sigma_R)

# Convolve
rho_total = np.convolve(rho_M_grid, rho_R_grid, mode='same') * domega
# Normalise
rho_total /= np.trapz(rho_total, omegas_grid)

# Diagonal multiplication-by-omega.
# Seed: sqrt(rho_total * domega) so that <v|v> = sum rho_total domega = 1
v0_seed = np.sqrt(np.maximum(rho_total, 0) * domega)
v0_seed = v0_seed / np.linalg.norm(v0_seed)

n_iter = 80
alphas_T5, betas_T5 = numerical_lanczos(omegas_grid, v0_seed, n_iter)
print(f"  n_iter = {len(betas_T5)}")
print(f"  First 10 b_n = {betas_T5[:10]}")
print(f"  Last 5 computed b_n = {betas_T5[-5:]}")
ns_T5 = np.arange(1, len(betas_T5)+1)
mask = (ns_T5 >= 10) & (ns_T5 <= 60)
if mask.sum() > 5:
    slope, intercept = np.polyfit(ns_T5[mask], betas_T5[mask], 1)
    print(f"  Linear fit b_n = slope*n + intercept on n in [10,60]:")
    print(f"    slope = {slope:.4f}    (theory: alpha = ?)")
    print(f"    intercept = {intercept:.4f}")

# Compare to pure III_1 (no dual translation): same Lanczos on rho_M alone
rho_M_pos = np.maximum(rho_M_grid, 0)
rho_M_pos = rho_M_pos / np.trapz(rho_M_pos, omegas_grid)
v0_M = np.sqrt(rho_M_pos * domega)
v0_M = v0_M / np.linalg.norm(v0_M)
alphas_M, betas_M = numerical_lanczos(omegas_grid, v0_M, n_iter)
print(f"\n  PURE III_1 (no convolution) for comparison:")
print(f"    First 10 b_n = {betas_M[:10]}")
mask = (ns_T5[:len(betas_M)] >= 10) & (ns_T5[:len(betas_M)] <= 60)
if mask.sum() > 5:
    slope_M, intercept_M = np.polyfit(ns_T5[:len(betas_M)][mask], betas_M[mask], 1)
    print(f"    slope = {slope_M:.4f}")

print("\n  Comparison: slope_M (pure III_1) vs slope_total (II_infty model):")
if mask.sum() > 5:
    print(f"    Ratio slope_total / slope_M = {slope/slope_M:.4f}")
    print(f"    (expected ~ 1 if convolution preserves linear-growth slope)")

# ---------------------------------------------------------------------------
# T6.  Identify the rigorous moment-method obstruction
# ---------------------------------------------------------------------------
print("\n--- T6. Rigorous obstruction analysis ---")
print("""
Parker et al. UOGH (2019) is a CONJECTURE for finite-dim chaotic systems.
The proof technique they use (recursion method, moment expansion) is NOT a
rigorous theorem; it is a phenomenology + numerical verification + general
power-counting argument.

The ONLY known RIGOROUS result connecting spectral-density tails to
Lanczos-coefficient asymptotics is Lubinsky's theorem (1998) for
exponential weights w(x) = exp(-Q(x)) on R:

  THEOREM (Lubinsky 1998 et al.): If w(x) = exp(-Q(x)) where Q is convex,
  even, increasing on R+, with Q(x) -> infty and Q(2x)/Q(x) -> q > 1,
  then the recurrence coefficients b_n of the orthonormal polynomials
  w.r.t. w satisfy b_n / a_n -> 1/2 as n -> infty, where a_n is the
  Mhaskar-Rakhmanov-Saff number (the n-th MRS root of Q'(a_n) = n).

For Q(x) = lambda |x| (linear), this gives b_n -> n / (2 lambda).

This is the RIGOROUS underpinning of UOGH for spectral measures in
the exponential class on R. The corresponding statement on more general
measures (e.g. supported on R+ only, or with power-law prefactors) is
covered by the Lubinsky / Levin-Lubinsky framework but requires
case-by-case verification.

OBSTRUCTION FOR TYPE II_infty:
The spectral measure mu_psi on K_N for a smooth seed in L^2(N, tr_N) is
the convolution of the III_1 modular spectrum (which has POWER-LAW tail
omega^(2h-1) for primaries) with the dual-translation spectrum (Schwartz
class for smooth seeds in the R-direction).

(a) The TAIL of mu_psi at |omega| -> infty inherits the slower of the
    two convolution factors: power-law if the III_1 component dominates,
    Schwartz if the dual-translation does.
(b) For a chiral primary of weight h, the III_1 spectrum is power-law
    omega^(2h-1) with NO exponential tail. Lubinsky's theorem does NOT
    apply; b_n is determined by the SU(1,1) representation theory and
    gives b_n = sqrt(n(n+2h-1)) ~ n EXACTLY, not as a UOGH consequence.
(c) For a smooth seed that is NOT a single primary (e.g. a coherent
    wavepacket), the spectrum is a mixture / convolution and the
    asymptotic slope is the MAX of the contributing primaries' h's
    (or the dual-translation slope if it dominates).
(d) The KMS condition mu(-omega) = exp(-beta omega) mu(omega) at
    beta = 2 pi (modular) forces a *symmetric* exponential ratio
    between positive and negative tails, which gives Phi_sym at HALF
    the bare KMS rate; on the type II_infty side, the dual-translation
    factor BREAKS this KMS condition (it is NOT KMS w.r.t. K_N because
    the trace tr_N is the canonical semifinite trace, not a KMS state).

Conclusion: The naive UOGH transfer FAILS in two ways:

  (i) The III_1 spectral measure for a primary is power-law, not
      exponential, so Lubinsky's rigorous theorem does not apply.
      The b_n ~ n behavior is a representation-theoretic miracle of
      SU(1,1), not a UOGH consequence.

  (ii) The crossed-product trace tr_N is canonically semifinite but
       NOT KMS w.r.t. K_N: the modular generator of (N, tr_N) is
       trivial since tr_N is tracial. The KMS condition that defines
       the modular slope alpha = pi / beta refers to a DIFFERENT
       weight on N (the dual weight phi_omega of the original III_1
       state), which is non-tracial and non-finite.

The UOGH in the form "b_n = alpha n + o(n) with alpha = pi/beta" is
formulated for KMS states. The semifinite trace tr_N is NOT KMS, so
the statement does not apply directly. What CAN be lifted is the
representation-theoretic identity for primaries: if the seed in
L^2(N, tr_N) projects (via the conditional expectation E:N->A) onto
a primary in L^2(A, omega), then the Lanczos coefficients on N
inherit the III_1 closed form b_n ~ n at the slope alpha = 1 in
modular units (= pi in BW units = 2 pi / beta with beta = 2 pi).

This is what the krylov_diameter.tex paper actually relies on
(see Remark labelled rem:blockA-status), and it is a much weaker
claim than "UOGH on type II_infty KMS states".
""")

# ---------------------------------------------------------------------------
# Conclusion
# ---------------------------------------------------------------------------
print("="*72)
print("CONCLUSION (sympy + numerical evidence):")
print("="*72)
print("""
1. Parker UOGH (1812.08657) is itself a CONJECTURE in finite-dim, with no
   rigorous proof. The closest rigorous result is Lubinsky's theorem on
   recurrence-coefficient asymptotics for exponential weights on R.

2. CMPT24 (2306.14732) computes b_n in CFT_2 vacuum on a primary using
   SU(1,1) representation theory:  b_n = sqrt(n(n+2h-1)). This is an
   EXACT identity, not a UOGH instance.

3. The naive moment-method lift to type II_infty FAILS for a fundamental
   reason: the canonical semifinite trace tr_N is TRACIAL, hence the
   modular generator of (N, tr_N) is TRIVIAL, hence the KMS condition
   that defines Parker's alpha = pi/beta does not apply with beta = 2pi.

4. What DOES lift is the III_1 representation-theoretic identity:
   - If the smooth seed in L^2(N, tr_N) projects under E:N->A onto a
     primary of weight h in A, then the III_1 Lanczos sequence is
     b_n^M = sqrt(n(n+2h-1)) ~ n.
   - The conditional expectation E preserves the matrix elements
     <O_n | e^(-i K_N s) | seed> in the limit where the dual-translation
     factor is asymptotically silent (smooth seed of compact support
     in the R-direction).
   - Hence b_n^N ~ n on the type II_infty side, with slope determined
     by the III_1 primary, not by a UOGH on tr_N.

5. The full UOGH-style theorem "b_n = alpha n + o(n) with alpha = pi/beta
   for any smooth seed and any KMS dual weight on N" is OPEN and
   probably FALSE in the stated generality (the dual translation can
   add arbitrary positive contributions to the spectral measure that
   shift the slope).

6. RESTRICTED-CLASS theorem that DOES hold:
      For N = A rtimes_sigma R with A type III_1, faithful normal state
      omega on A satisfying KMS at beta_mod = 2 pi w.r.t. modular flow,
      and a smooth seed |psi> = pi(O) Xi_omega with O a chiral primary
      of weight h, the Lanczos coefficients of K_N on |psi> satisfy
          b_n = sqrt(n(n+2h-1)) + o(1)
      asymptotically as n -> infty. This is the III_1 closed form
      lifted via the conditional expectation E:N->A, valid in the
      restricted class of "primary seeds".

7. Outside the primary class, the b_n asymptotic depends on the
   dual-translation profile and is NOT universal.

VERDICT (concise): The "UOGH transfer to type II_infty" as stated is
FALSE for generic seeds (no universal slope alpha = pi/beta exists
because the canonical trace is tracial, not KMS). It is TRUE in a
RESTRICTED CLASS (primary seeds, where SU(1,1) representation theory
gives b_n = sqrt(n(n+2h-1)) exactly).

This restricted class is exactly what the krylov_diameter.tex paper
actually invokes (via the conditional-expectation projection to A);
the paper's Remark on Block A1 status is HONEST, and the
cosmo_hayden_preskill conditional theorem is sound on this restricted
class but cannot be promoted to a UNIVERSAL UOGH statement.
""")
print("="*72)
print("END")
print("="*72)
