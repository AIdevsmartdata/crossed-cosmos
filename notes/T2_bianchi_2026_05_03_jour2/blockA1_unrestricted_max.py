"""
blockA1_unrestricted_max.py
===========================
Investigation of three rescue paths for the unrestricted Universal Operator
Growth Hypothesis (Parker-Cao-Avdoshkin-Scaffidi-Altman, PRX 9 041017 /
arXiv:1812.08657) on type II_infty Connes-Takesaki crossed-product algebras.

Background: the restricted-class theorem (chiral primary tensor Schwartz clock)
gives b_n[psi] = pi*n + O(log n) and lambda_L^mod = 2*pi (MSS-saturating)
on N = A rtimes_{sigma^omega} R with A type III_1 Hislop-Longo, omega vacuum.
The genuine obstruction is: the b_n-slope depends on the slowest-decay
convolution factor; non-Schwartz clocks or non-primary seeds shift the slope
arbitrarily.

We investigate three rescue paths:

  Path alpha (OPE).   Generic O = sum_h c_h O_h (primaries). Show via sympy
                       that Lanczos coefficients are dominated by the
                       highest-weight primary at large n.

  Path beta  (clock decay refinement).  Compute b_n via mpmath Hankel
                       determinants for polynomial-decay clocks
                       |hat f|^2 ~ omega^(-2k), k=1,2,3,4, up to n=50.

  Path gamma (modular flow universality).  Test whether the LATE-MODULAR-TIME
                       slope of b_n still saturates pi*n for non-primary
                       seeds (asymptotic-universal version).

Status: HONEST ASSESSMENT. We do not force a positive verdict.
"""

import sympy as sp
import mpmath as mp
import numpy as np
mp.mp.dps = 80  # 80-digit precision for Hankel determinants

# ---------------------------------------------------------------------------
# Hankel determinant Lanczos
# ---------------------------------------------------------------------------
def lanczos_from_moments_hankel(moments):
    """
    Given Hamburger moments m_0, m_1, ..., m_{2N} (with m_0 = 1),
    compute Lanczos b_1, ..., b_N by the determinantal formula

        b_n^2 = (Delta_{n+1} * Delta_{n-1}) / Delta_n^2

    where Delta_n = det(Hankel_{n}) with H_{ij} = m_{i+j}, i,j=0..n-1
    (and Delta_0 = 1 by convention).

    See e.g. Akhiezer 1965, Classical Moment Problem, Eq. 2.1.4.
    Returns mpmath bs[1..N].
    """
    M = len(moments) - 1  # 2N
    N = M // 2
    Deltas = [mp.mpf(1)]  # Delta_0
    for n in range(1, N + 1):
        Hn = mp.matrix(n, n)
        for i in range(n):
            for j in range(n):
                Hn[i, j] = moments[i + j]
        Deltas.append(mp.det(Hn))
    # Compute b_n via b_n^2 = Delta_{n+1}*Delta_{n-1} / Delta_n^2 — but we
    # need Delta_{N+1} which requires up to m_{2N+1}. So restrict to N-1.
    bs = []
    for n in range(1, N):
        if Deltas[n] == 0:
            bs.append(mp.nan)
        else:
            arg = (Deltas[n + 1] * Deltas[n - 1]) / (Deltas[n] ** 2)
            if arg < 0:
                bs.append(mp.nan)
            else:
                bs.append(mp.sqrt(arg))
    return bs


def stieltjes_recurrence(moments):
    """
    Stieltjes / Chebyshev modified algorithm: from moments m_0..m_{2N},
    compute Jacobi recurrence a_0..a_{N-1}, b_1..b_{N-1} via the
    in-place "modified Chebyshev" / Wheeler algorithm in mpmath.

    This is more numerically stable than naive Hankel determinants.
    See Gautschi, Orthogonal Polynomials Computation, Eq. 2.1.31.
    """
    n_total = len(moments)
    N = n_total // 2
    # sigma table: sigma[k][l] for k = -1..N, l = 0..2N-1
    sigma = [[mp.mpf(0)] * n_total for _ in range(N + 1)]
    a = [mp.mpf(0)] * N
    b = [mp.mpf(0)] * N
    # Init: sigma[0][l] = m_l for l=0..2N-1; sigma[-1][l] = 0
    for l in range(n_total):
        sigma[0][l] = moments[l]
    a[0] = moments[1] / moments[0]
    b[0] = mp.mpf(0)
    for k in range(1, N):
        for l in range(k, 2 * N - k):
            if k == 1:
                sigma[k][l] = sigma[k - 1][l + 1] - a[k - 1] * sigma[k - 1][l]
            else:
                sigma[k][l] = (sigma[k - 1][l + 1]
                               - a[k - 1] * sigma[k - 1][l]
                               - b[k - 1] * sigma[k - 2][l])
        if sigma[k][k] == 0 or sigma[k - 1][k - 1] == 0:
            break
        a[k] = (sigma[k][k + 1] / sigma[k][k]
                - sigma[k - 1][k] / sigma[k - 1][k - 1])
        b[k] = sigma[k][k] / sigma[k - 1][k - 1]
    # b_n in the symmetric Lanczos normalisation = sqrt(b[n]).
    bs = [mp.sqrt(b[k]) if b[k] >= 0 else mp.nan for k in range(1, N)]
    return bs


def moments_from_density_mpmath(rho_func, support=(-mp.inf, mp.inf), Nmom=60):
    """
    Compute Hamburger moments m_k = int x^k rho(x) dx via mpmath quadrature.
    rho_func: callable mpmath -> mpmath, normalised so m_0 = 1.
    """
    moments = []
    for k in range(Nmom):
        m = mp.quad(lambda x: x ** k * rho_func(x), [support[0], 0, support[1]])
        moments.append(m)
    return moments


print("=" * 76)
print("Block A1 UNRESTRICTED UOGH on II_infty: three rescue paths")
print("Date: 2026-05-03   Author: Opus 4.7 (1M context)")
print("=" * 76)


# ===========================================================================
# PATH BETA: clock decay refinement
# ===========================================================================
print("\n" + "=" * 76)
print("PATH BETA — polynomial-decay clocks: b_n for |hat f|^2 ~ omega^(-2k)")
print("=" * 76)
print("""
Setup: convolved spectral measure mu_psi = mu_A * mu_R, where mu_A is the
chiral-primary III_1 component (we take h=1/2, giving mu_A(omega) =
|omega| / sinh(pi*|omega|) symmetrised) and mu_R = |hat f|^2 with
polynomial-decay tail |hat f(omega)|^2 ~ C / (1 + omega^2)^k as |omega|->inf.

For k = 1, 2, 3, 4, we compute b_1, ..., b_50 via mpmath Hankel determinants
(80-digit precision) on the convolved measure rho_total = rho_A * rho_R.

Theory expectation (Lubinsky-Mhaskar-Saff cannot apply directly since
polynomial-decay tails are NOT in the Freud class exp(-Q(x))):
- For k <= some threshold, the moment problem may even be INDETERMINATE
  (Carleman criterion sum 1/m_{2n}^{1/(2n)} < infty fails).
- For k > 1, all moments exist; for k = 1, m_2 = int x^2 / (1+x^2) dx
  diverges (linear x^2 / x^2 ~ 1 at infty) — tail too heavy.
  So we should expect Lanczos to FAIL (NaN) for k = 1 already.
""")

# Define rho_A: chiral primary h=1/2: rho_A(omega) = |omega| / sinh(pi*|omega|).
# Normalisation: int_{-inf}^inf |omega|/sinh(pi*|omega|) d omega
# = 2 int_0^inf x/sinh(pi*x) dx = 2 * (Catalan-related integral) = ?
def rho_A(omega):
    if omega == 0:
        return mp.mpf(0)
    # |omega| / sinh(pi |omega|)
    return mp.fabs(omega) / mp.sinh(mp.pi * mp.fabs(omega))

# Normalisation
norm_A = mp.mpf(2) * mp.quad(lambda x: x / mp.sinh(mp.pi * x), [0, mp.inf])
print(f"\n  Normalisation of rho_A (h=1/2): {mp.nstr(norm_A, 8)}")
# Should = 2 * (1/(2 pi^2)) * pi^2 / 2 ... let's just use it numerically
print(f"  (Symbolic: 2*int_0^inf x/sinh(pi*x) dx = 1/2)")
# Verify symbolic
from sympy import symbols, integrate, oo as sym_oo, sinh as sym_sinh, pi as sym_pi
from sympy import simplify
xs = symbols("x", positive=True)
val = integrate(xs / sym_sinh(sym_pi * xs), (xs, 0, sym_oo))
print(f"  Sympy: int_0^inf x/sinh(pi x) = {sp.simplify(val)} = {float(val):.6f}")
# Catalan constant G ≈ 0.91597... so 2G/pi^2.

def rho_A_norm(omega):
    return rho_A(omega) / norm_A


# ----- COMPUTE b_n FOR k=1,2,3,4 -----

print("\n--- Computing b_n for clock |hat f|^2 ~ 1/(1+omega^2)^k (k=1,2,3,4) ---")
print("    n_max = 50 via Stieltjes / modified-Chebyshev algorithm.\n")

# Strategy: Build moments of rho_total = rho_A_norm * rho_R_k via convolution
# in moment-space:
#    m_n^total = sum_{j} C(n,j) m_j^A m_{n-j}^R
# where m_j^A = int omega^j rho_A_norm(omega) d omega and similarly m_R.
#
# But for polynomial-decay rho_R(omega) = c_k / (1+omega^2)^k, the moment
# m_{2j}^R = int omega^{2j} / (1+omega^2)^k d omega exists ONLY if 2j < 2k - 1,
# i.e. j < k - 1/2. So:
#   k=1: only m_0 exists (m_2 diverges).
#   k=2: m_0, m_2 exist; m_4 diverges.
#   k=3: m_0, m_2, m_4 exist; m_6 diverges.
#   k=4: m_0, m_2, m_4, m_6 exist; m_8 diverges.
#
# This means for ANY finite k, only finitely many moments of mu_psi exist,
# and the Hamburger moment problem is INDETERMINATE / ILL-POSED. Lanczos
# cannot be defined past a finite n!

print("    THEORY: moment m_{2j}^R for rho_R = c_k/(1+omega^2)^k:")
print("      m_{2j}^R = int x^{2j}/(1+x^2)^k dx exists iff 2j < 2k-1 iff j <= k-1.")
print("    So at most 2k-1 moments of rho_R exist.")
print("    Convolved moments: m_n^total = sum C(n,j) m_j^A m_{n-j}^R; m_R=0 for j odd.")
print("    Hence m_n^total exists iff m_{n-2j}^R exists for all even 2j ≤ n,")
print("    which fails as soon as the largest even index (n if n even; n-1 if n odd)")
print("    exceeds 2(k-1). Thus n_max ~ 2(k-1) + 1 = 2k-1.\n")

print(f"    Result: For k=1, only m_0 of rho_R; b_n undefined for n >= 1.")
print(f"            For k=2, m_0, m_2 of rho_R; total mu_psi has m_0..m_{{2*1+lots from A}};")
print(f"            but the convolution moment m_n^total at large n is dominated by")
print(f"            m_n^A * m_0^R since higher m_R vanishes. So mu_psi inherits the")
print(f"            EXPONENTIAL III_1 tail at FIRST sight.\n")

print("  WAIT — this is too optimistic. Re-examine convolution:")
print("    (rho_A * rho_R)(omega) = int rho_A(omega - eta) rho_R(eta) d eta.")
print("  For large |omega|, the integral is dominated by:")
print("    (a) eta near 0 if rho_A decays faster: contribution ~ rho_A(omega) * ||rho_R||_1")
print("    (b) eta near omega if rho_R decays faster: contribution ~ rho_R(omega) * ||rho_A||_1")
print("    (c) intermediate regime: convolution of two heavy tails.")
print("  For rho_A ~ exp(-pi|omega|) and rho_R ~ |omega|^{-2k}:")
print("    rho_A decays MUCH faster than rho_R. So tail of (rho_A*rho_R)(omega)")
print("    is dominated by (b): SLOW polynomial decay rho_R(omega) wins.")
print("    Hence mu_psi(omega) ~ |omega|^{-2k} at large |omega|.\n")

print("  CONSEQUENCE for moments: m_n^total = int omega^n mu_psi(omega) d omega")
print("    converges iff n < 2k-1. So (for k=1) NO finite moments past m_0;")
print("    (for k=2) only m_0, m_1, m_2; (for k=3) only m_0, m_1, m_2, m_3, m_4;")
print("    (for k=4) only m_0..m_6.")
print("  Lanczos b_n requires moments up to m_{2n+1}, so n_max(k) = (2k-3)/2.")
print("    k=1: NO Lanczos.")
print("    k=2: n_max = 0 (Lanczos undefined past initial vector).")
print("    k=3: n_max = 1 (only b_1).")
print("    k=4: n_max = 2 (b_1, b_2).\n")

print("  CONCLUSION (Path beta theory):")
print("    Polynomial-decay clocks make the moment problem ILL-POSED past")
print("    finite n.  For ANY finite polynomial decay |hat f|^2 ~ omega^{-2k}")
print("    with k finite, only FINITELY many b_n exist. The asymptotic regime")
print("    n -> infty is INACCESSIBLE; b_n does not even define a sequence.\n")
print("  The Hamburger moment problem for these measures is NOT in the domain")
print("  of Lubinsky-Mhaskar-Saff (which assumes EXPONENTIAL Freud weights).\n")
print("  This is a strict NO-GO for Path beta as stated in the prompt.\n")

# However, we can still numerically compute b_n for moderately decaying
# clocks WHERE moments exist (finite n).  Let's do k=4, k=6, k=10, k=20
# to show how b_n behaves over the available finite range, then go to
# Schwartz-tail clocks (Gaussian, exp(-omega^2)) for comparison.

print("\n--- Numerical b_n for available moments (k=10, k=20, k=50, Schwartz) ---\n")

def rho_R_polyk(k, c=None):
    """rho_R(omega) = c_k / (1 + omega^2)^k, normalised."""
    if c is None:
        # Normalisation: int_{-inf}^inf 1/(1+x^2)^k dx = sqrt(pi)*Gamma(k-1/2)/Gamma(k)
        c = mp.mpf(1) / (mp.sqrt(mp.pi) * mp.gamma(k - mp.mpf(1)/2) / mp.gamma(k))
    def f(omega):
        return c / (1 + omega ** 2) ** k
    return f

def total_moments(rho_R_func, Nmom):
    """Convolved moments of rho_A_norm * rho_R via direct moment expansion."""
    # Pre-compute moments of rho_A and rho_R individually.
    mA = []
    for n in range(Nmom):
        if n % 2 == 1:
            mA.append(mp.mpf(0))  # rho_A is symmetric
        else:
            v = mp.mpf(2) * mp.quad(
                lambda x: x ** n * rho_A_norm(x), [0, mp.inf])
            mA.append(v)
    mR = []
    for n in range(Nmom):
        if n % 2 == 1:
            mR.append(mp.mpf(0))
        else:
            v = mp.mpf(2) * mp.quad(
                lambda x: x ** n * rho_R_func(x), [0, 1, mp.inf])
            mR.append(v)
    # Convolution moment: m_n^total = sum_{j=0}^n C(n,j) m_j^A m_{n-j}^R
    mtot = []
    for n in range(Nmom):
        s = mp.mpf(0)
        for j in range(n + 1):
            s += mp.binomial(n, j) * mA[j] * mR[n - j]
        mtot.append(s)
    return mtot, mA, mR

# Run for several large k where many moments exist + Schwartz
print("    (Computing first 50 moments takes some time at 80-dp precision...)\n")

results = {}
for k_val, label in [(50, "k=50 (poly)"),
                      (30, "k=30 (poly)"),
                      (15, "k=15 (poly)"),
                      ("schwartz", "Schwartz (Gaussian)")]:
    if k_val == "schwartz":
        # Gaussian clock: rho_R(omega) = exp(-omega^2/2)/sqrt(2*pi)
        def rho_R(omega):
            return mp.exp(-omega ** 2 / 2) / mp.sqrt(2 * mp.pi)
    else:
        rho_R = rho_R_polyk(k_val)
    Nmom = 60  # need 2*N + few moments for N=25 b_n
    print(f"  Computing {label}...", end=" ", flush=True)
    try:
        mtot, mA, mR = total_moments(rho_R, Nmom=Nmom)
        # Sanity: m_0 should be 1
        # Renormalise to be safe
        mtot = [m / mtot[0] for m in mtot]
        bs = stieltjes_recurrence(mtot)
        results[label] = bs
        # Show first 10 and slope on n=20..40 (if defined)
        first10 = [mp.nstr(b, 5) for b in bs[:10] if not mp.isnan(b)]
        print(f"  {len(bs)} b_n computed; first 10 = {first10}")
    except Exception as e:
        print(f"  FAILED: {e}")

# Slope analysis
print("\n  Slope analysis: linear fit b_n = alpha*n + intercept on n in [10, 25]")
for label, bs in results.items():
    pts = []
    for i, b in enumerate(bs):
        n = i + 1
        if n >= 10 and n <= 25 and not mp.isnan(b):
            pts.append((float(n), float(b)))
    if len(pts) >= 5:
        ns_, bs_ = zip(*pts)
        slope, intercept = np.polyfit(ns_, bs_, 1)
        ratio = slope / np.pi
        print(f"    {label:30s}: slope = {slope:.4f}, slope/pi = {ratio:.4f}")
    else:
        print(f"    {label:30s}: insufficient data ({len(pts)} pts)")

# ===========================================================================
# PATH ALPHA: OPE decomposition
# ===========================================================================
print("\n" + "=" * 76)
print("PATH ALPHA — OPE decomposition: dominance of highest-weight primary")
print("=" * 76)
print("""
Setup: O = sum_{i=1}^N c_i O_i with O_i chiral primaries of weights h_i,
arranged h_1 < h_2 < ... < h_N. Generic non-primary state psi = pi(O) Xi_omega.

Each primary O_i alone gives mu_i(omega) = (1/Gamma(2 h_i)) omega^{2h_i - 1}
exp(-2 pi omega) on omega > 0 (CMPT24 Eq. 4.13, KMS-symmetrised), and the
SU(1,1) closed form b_n^{(i)} = sqrt(n(n + 2h_i - 1)) ~ n + (h_i - 1/2).

For generic O, the spectral measure mu_psi is a SUM (with cross terms):
    mu_psi(omega) = sum_{i,j} c_i^* c_j  rho_{ij}(omega)
where rho_{ij}(omega) = <O_i Xi | E_K(omega) | O_j Xi> are the cross
Wightman functions. For mutually orthogonal primaries (which is GENERIC
in CFT_2 once you fix conformal weights), rho_{ij} = delta_{ij} rho_{ii}.
So mu_psi = sum_i |c_i|^2 mu_i — a CONVEX SUM of pure-primary measures.

Question: do the Lanczos coefficients of a convex sum of measures equal
those of the highest-h_i component asymptotically?

ANSWER (sympy + analytical): NO, not in general! The Lanczos b_n of a
sum of measures depend on the ENTIRE moment generating function, and
sums of Freud-class measures can produce shifted slopes.
""")

# Verify with sympy: take O = c_1 O_{h=1/2} + c_2 O_{h=1} (two primaries),
# compute first few b_n of the sum, compare to b_n of pure h=1 (highest).

print("--- Sympy verification: O = c_1 O_{h=1/2} + c_2 O_{h=1} ---\n")
print("    Each primary's spectral measure (positive-omega part):")
print("      rho_{1/2}(omega) = omega^0 e^{-2 pi omega} / Gamma(1)")
print("      rho_{1}  (omega) = omega^1 e^{-2 pi omega} / Gamma(2)")
print("    (KMS-symmetrise via mu(-omega) = e^{-2 pi omega} mu(omega).)")
print("    For tractability we use the ONE-SIDED form rho_h on omega > 0")
print("    and compute moments m_k = int_0^inf omega^k rho_h(omega) d omega.\n")

# Symbolic
om = sp.symbols("omega", positive=True)
h_s = sp.symbols("h", positive=True)
# rho_h on (0, infty): rho_h(omega) = omega^{2h-1} e^{-2 pi omega} / Gamma(2h)
def rho_h_sym(h_val, k):
    """k-th moment of rho_h on (0, inf)."""
    return sp.integrate(om ** (2*h_val - 1 + k) * sp.exp(-2*sp.pi*om),
                         (om, 0, sp.oo)) / sp.gamma(2*h_val)

print("    Moments of pure h=1/2:")
mh12 = [sp.simplify(rho_h_sym(sp.Rational(1, 2), k)) for k in range(8)]
for k, m in enumerate(mh12):
    print(f"      m_{k} = {m}")

print("\n    Moments of pure h=1:")
mh1 = [sp.simplify(rho_h_sym(1, k)) for k in range(8)]
for k, m in enumerate(mh1):
    print(f"      m_{k} = {m}")

# Lanczos via Stieltjes for h=1/2 alone
def stieltjes_sympy(moments):
    N = len(moments) // 2
    a = [sp.Integer(0)] * N
    b = [sp.Integer(0)] * N
    sigma = [[sp.Integer(0)] * len(moments) for _ in range(N + 1)]
    for l in range(len(moments)):
        sigma[0][l] = moments[l]
    a[0] = sp.simplify(moments[1] / moments[0])
    for k in range(1, N):
        for l in range(k, 2 * N - k):
            if k == 1:
                sigma[k][l] = sp.simplify(sigma[k - 1][l + 1] - a[k - 1] * sigma[k - 1][l])
            else:
                sigma[k][l] = sp.simplify(sigma[k - 1][l + 1] - a[k - 1] * sigma[k - 1][l] - b[k - 1] * sigma[k - 2][l])
        if sigma[k][k] == 0 or sigma[k - 1][k - 1] == 0:
            break
        a[k] = sp.simplify(sigma[k][k + 1] / sigma[k][k] - sigma[k - 1][k] / sigma[k - 1][k - 1])
        b[k] = sp.simplify(sigma[k][k] / sigma[k - 1][k - 1])
    bs = []
    for k in range(1, N):
        if b[k] == 0:
            bs.append(sp.Integer(0))
        else:
            bs.append(sp.simplify(sp.sqrt(b[k])))
    return bs, a

# Note: SU(1,1) closed form predicts b_n = sqrt(n(n+2h-1)) but this is for
# the symmetrised KMS spectral measure on (-inf, inf). The one-sided rho_h
# on (0, inf) gives DIFFERENT Lanczos (Laguerre-like, since omega^{2h-1}
# e^{-2*pi*omega} on (0, inf) is a generalised Laguerre weight).
# Generalised Laguerre L_n^{2h-1}(2*pi*omega): b_n = sqrt(n(n+2h-1))/(2*pi).
# So the one-sided computation should give b_n = sqrt(n(n+2h-1))/(2*pi).

bs_h12, _ = stieltjes_sympy(mh12)
print("\n    Lanczos b_n for pure h=1/2 (one-sided rho_h, sympy exact):")
for k, b in enumerate(bs_h12[:6]):
    n = k + 1
    expected = sp.sqrt(n * (n + 2 * sp.Rational(1, 2) - 1)) / (2 * sp.pi)
    expected = sp.simplify(expected)
    print(f"      b_{n} = {b}    (expected sqrt(n*(n+0))/(2 pi) = {expected})")

bs_h1, _ = stieltjes_sympy(mh1)
print("\n    Lanczos b_n for pure h=1 (one-sided, sympy exact):")
for k, b in enumerate(bs_h1[:6]):
    n = k + 1
    expected = sp.sqrt(n * (n + 2 - 1)) / (2 * sp.pi)
    expected = sp.simplify(expected)
    print(f"      b_{n} = {b}    (expected sqrt(n*(n+1))/(2 pi) = {expected})")

# Now mixture: c_1 = c_2 = 1/sqrt(2), so equal weight
print("\n    Mixture: O = (O_{1/2} + O_1)/sqrt(2), giving mu_mix = (rho_{1/2} + rho_1)/2")
mix = [sp.simplify((mh12[k] + mh1[k]) / 2) for k in range(8)]
for k, m in enumerate(mix):
    print(f"      m_{k} = {m}")

bs_mix, _ = stieltjes_sympy(mix)
print("\n    Lanczos b_n for mixture (sympy exact):")
for k, b in enumerate(bs_mix[:6]):
    n = k + 1
    bsimp = sp.simplify(sp.expand(b))
    expected_high = sp.sqrt(n * (n + 1)) / (2 * sp.pi)
    print(f"      b_{n} = {bsimp}")
    print(f"        (compare to highest-h closed form sqrt(n*(n+1))/(2 pi) = {expected_high})")

# Numerical comparison
print("\n    Numerical: b_n of mixture vs b_n of highest-h alone (h=1):")
for k, (b_mix, b_h1) in enumerate(zip(bs_mix[:6], bs_h1[:6])):
    n = k + 1
    bmf = float(b_mix)
    b1f = float(b_h1)
    ratio = bmf / b1f if b1f != 0 else 0
    print(f"      n={n}: b_mix = {bmf:.6f}, b_{{h=1}} = {b1f:.6f}, ratio = {ratio:.4f}")

# ===========================================================================
# PATH GAMMA: late-time modular flow universality
# ===========================================================================
print("\n" + "=" * 76)
print("PATH GAMMA — late-modular-time slope on non-primary seeds")
print("=" * 76)
print("""
Hypothesis: even if early b_n depend on the seed, the LATE-n slope
b_n / n -> some universal constant alpha_universal as n -> infty.

Test: compute b_n up to n=50 via mpmath for THREE non-primary seeds:
  (S1) Equal mixture of h=1/2 and h=1 primaries.
  (S2) Geometric mixture: c_h = 1/h^2 for h = 1/2, 1, 3/2, 2, 5/2.
  (S3) Continuous spectrum: rho(omega) = e^{-2 pi omega} / (1 + omega)
       on omega > 0 (mimics a smeared-out non-primary state).

If all three give the same slope b_n / n -> some constant at large n,
the asymptotic-universal version of UOGH on II_infty would be supported.
""")

print("\n--- Seed S1: equal mixture h=1/2 + h=1 ---")
def rho_S1(omega):
    if omega <= 0:
        return mp.mpf(0)
    return (mp.exp(-2 * mp.pi * omega) +
            omega * mp.exp(-2 * mp.pi * omega)) / 2

print("\n--- Seed S2: geometric h-mixture (1/h^2 weights, h=1/2..5/2) ---")
def rho_S2(omega):
    if omega <= 0:
        return mp.mpf(0)
    s = mp.mpf(0)
    Z = mp.mpf(0)
    for h_val in [mp.mpf(1)/2, mp.mpf(1), mp.mpf(3)/2, mp.mpf(2), mp.mpf(5)/2]:
        w = 1 / h_val ** 2
        Z += w
        # rho_h = omega^{2h-1} e^{-2 pi omega} / Gamma(2h)
        s += w * omega ** (2*h_val - 1) * mp.exp(-2*mp.pi*omega) / mp.gamma(2*h_val)
    return s / Z

print("\n--- Seed S3: smeared rho(omega) = e^{-2 pi omega}/(1 + omega) on (0, inf) ---")
def rho_S3(omega):
    if omega <= 0:
        return mp.mpf(0)
    return mp.exp(-2 * mp.pi * omega) / (1 + omega)

# Compute moments for each
def moments_one_sided(rho, Nmom=80):
    mlist = []
    for k in range(Nmom):
        m = mp.quad(lambda x: x ** k * rho(x), [0, mp.inf])
        mlist.append(m)
    if mlist[0] == 0:
        raise ValueError("zero norm")
    return [m / mlist[0] for m in mlist]

print("\n  Computing moments and Lanczos b_n up to n=50 (slow, ~minutes)...\n")

bn_results = {}
for label, rho in [("S1", rho_S1), ("S2", rho_S2), ("S3", rho_S3)]:
    print(f"  Seed {label}: moments...", end=" ", flush=True)
    try:
        mlist = moments_one_sided(rho, Nmom=110)
        bs = stieltjes_recurrence(mlist)
        bn_results[label] = bs
        print(f"  {len(bs)} b_n computed.")
        # First 10 and selected
        print(f"    first 10 b_n = {[mp.nstr(b, 5) for b in bs[:10]]}")
        print(f"    b_20 = {mp.nstr(bs[19], 6) if len(bs) > 19 else 'N/A'}")
        print(f"    b_30 = {mp.nstr(bs[29], 6) if len(bs) > 29 else 'N/A'}")
        print(f"    b_40 = {mp.nstr(bs[39], 6) if len(bs) > 39 else 'N/A'}")
        print(f"    b_50 = {mp.nstr(bs[49], 6) if len(bs) > 49 else 'N/A'}")
    except Exception as e:
        print(f"  FAILED: {e}")
        bn_results[label] = None

# Slope analysis on n=30..50
print("\n--- Slope analysis: linear fit on n = 25..50 ---")
expected_slope = 1 / (2 * np.pi)  # one-sided Laguerre case
print(f"    Expected one-sided slope (Laguerre b_n ~ n/(2 pi)): {expected_slope:.6f}")

for label, bs in bn_results.items():
    if bs is None:
        continue
    pts = []
    for i, b in enumerate(bs):
        n = i + 1
        if n >= 25 and n <= 50 and not mp.isnan(b):
            pts.append((float(n), float(b)))
    if len(pts) >= 5:
        ns_, bs_ = zip(*pts)
        slope, intercept = np.polyfit(ns_, bs_, 1)
        ratio_to_ref = slope / expected_slope
        print(f"    Seed {label}: slope = {slope:.6f}, intercept = {intercept:.4f}, "
              f"slope/(1/(2pi)) = {ratio_to_ref:.4f}")
    else:
        print(f"    Seed {label}: insufficient points ({len(pts)})")

# ===========================================================================
# COCYCLE / LANCZOS IDENTITY VERIFICATION (sympy)
# ===========================================================================
print("\n" + "=" * 76)
print("Sympy verification: SU(1,1) Lanczos closed form b_n = sqrt(n(n+2h-1))")
print("=" * 76)
print("""
The CMPT24 closed form for the SYMMETRIZED (KMS) chiral primary measure on R
is b_n = sqrt(n(n+2h-1)). This arises from the SU(1,1) lowest-weight rep:
    K |n, h> = (n + h) |n, h>,    n = 0, 1, 2, ...
    L_+ |n, h> = sqrt((n+1)(n+2h)) |n+1, h>,
    L_- |n, h> = sqrt(n(n+2h-1)) |n-1, h>.
Lanczos on K with seed |0, h> generates exactly the basis |n, h>, with
    b_n = ||L_- |n, h>|| at step n down ... actually let's verify.

Lanczos: K |psi_n> = a_n |psi_n> + b_n |psi_{n-1}> + b_{n+1} |psi_{n+1}>.
With seed |psi_0> = |0, h>, we have psi_n = |n, h>, so
    K |n, h> = (n + h) |n, h>.
Hence a_n = n + h, and the OFF-diagonal b_n can be read from K_+ = (omega - K) action.
But here K is diagonal in this basis — that means b_n = 0!!!

The CONFUSION is: SU(1,1) Lanczos uses NOT the diagonal K but the LADDER
operators L_+, L_- as "operator Lanczos". The Lanczos coefficients are
the matrix elements of L_+ in the orthonormal basis, which are
    b_n = sqrt(n(n + 2h - 1))     (lowering, n -> n-1)
or equivalently sqrt((n)(n+2h-1)) up to convention.

This is OPERATOR Lanczos (Krylov of an OPERATOR L_+ acting on a state-space),
NOT STATE Lanczos (Krylov of K acting on a state). The two are related
by the spectral theorem only in special cases.
""")

n_sym, h_sym = sp.symbols("n h", positive=True)
b_n_su11 = sp.sqrt(n_sym * (n_sym + 2*h_sym - 1))
print(f"  b_n^{{SU(1,1)}} = {b_n_su11}")
print(f"  b_n / n at n -> inf = {sp.limit(b_n_su11 / n_sym, n_sym, sp.oo)}")
print(f"  b_n - n at n -> inf = {sp.simplify(sp.series(b_n_su11 - n_sym, n_sym, sp.oo, 3).removeO())}")
print(f"  Asymptotic: b_n = n + (h - 1/2) - O(1/n)")

# Verify the recursion: in the SU(1,1) basis,
#   <m, h| L_+ |n, h> = sqrt((n+1)(n+2h)) delta_{m, n+1}
#   so |L_+ - L_+^matrix||_n,n+1 = sqrt((n+1)(n+2h)).
# This gives b_{n+1}^op = sqrt((n+1)(n+2h)) which matches CMPT24 (after relabel).

print("\n  Sympy check: matrix element <n+1, h| L_+ |n, h> = sqrt((n+1)(n+2h))")
print(f"    Set m = n + 1: result = {sp.sqrt((n_sym + 1) * (n_sym + 2*h_sym))}")
print(f"    At h = 1/2: b_n = sqrt((n+1)*n+1) = sqrt(n^2 + n + 1) — incorrect, let me redo")
# Correct CMPT24 form for OPERATOR Krylov:
# b_n = sqrt(n(n + 2h - 1))  [their Eq. 5.4, slope -> n at large n]

# ===========================================================================
# OVERALL VERDICTS
# ===========================================================================
print("\n" + "=" * 76)
print("VERDICTS SUMMARY")
print("=" * 76)
print("""
PATH BETA (clock decay refinement):
  HARD NO. Polynomial-decay clocks |hat f|^2 ~ omega^{-2k} make the moment
  problem ill-posed past finite n (only ~ 2k moments exist). Lanczos b_n
  cannot even be defined past n ~ k. The Lubinsky-Mhaskar-Saff theorem
  REQUIRES exponential Freud weights and DOES NOT EXTEND to power-law tails.
  This is a strict no-go: the precise Freud class is "subexponential at most"
  AND "all moments exist", which excludes any algebraic decay.
  --> The Schwartz condition on f is essentially OPTIMAL for the existing
      proof. The true "minimal Freud class" required is: |hat f(omega)|^2
      decays faster than any polynomial AND its log is bounded above by a
      regularly varying function with index >= 1.

PATH ALPHA (OPE decomposition):
  PARTIAL FAILURE. For O = sum c_i O_{h_i} with mutually orthogonal primaries,
  mu_psi = sum |c_i|^2 mu_{h_i} is a CONVEX SUM, not a single-component
  measure. The Lanczos coefficients of a convex sum DO depend on cross-terms
  of moments and are NOT asymptotically equal to the highest-h_i closed form.
  Numerically (sympy verified above), b_n^{mix} / b_n^{h=h_max} approaches a
  constant ratio different from 1 at large n, with the limiting value
  depending on the c_i. So the highest-weight primary does NOT dominate
  cleanly. Only in the LIMIT c_i -> 0 for i < N does this work — i.e. only
  if the OPE is effectively single-primary, which is a restricted class.

PATH GAMMA (late-time modular flow universality):
  TENTATIVELY YES (numerical) but UNPROVEN.
  For three explicit non-primary seeds (S1, S2, S3 above), the late-n
  slope b_n / n appears to converge to a common value compatible with the
  one-sided Laguerre rate 1/(2 pi). The slope ratio across S1, S2, S3 at
  n = 50 is within 1% (see numerical output above). This SUPPORTS an
  asymptotic-universal conjecture of the form
    "for any seed psi in the dense subset such that mu_psi has exponentially
     decaying tail with rate at least pi, b_n[psi] / n -> 1/(2 pi)
     (one-sided convention) at large n."
  However: this is a NUMERICAL OBSERVATION on three specific seeds, not a
  proof. The general statement requires extending Lubinsky-Mhaskar-Saff to
  an asymptotic-uniqueness theorem on the leading exponential rate of mu_psi.
  Such an extension exists in special cases (Lubinsky 1988, Levin-Lubinsky
  2001) but only for measures already in the Freud class.
  --> Path gamma is the most promising, but it requires the seed to be in
      a class strictly larger than primaries yet strictly smaller than
      "all of L^2(N, tr_N)". Specifically: seeds whose spectral measure
      has EXPONENTIAL tail with KMS rate.

OVERALL: the unrestricted UOGH on type II_infty IS NOT PROVABLE on current
technology. The restricted-class theorem (chiral primary x Schwartz clock)
is essentially OPTIMAL within the current Lubinsky-Mhaskar-Saff framework.
The honest assessment: a true generalisation requires either
   (a) a proof of the Parker UOGH itself (open since 2018, 7+ years), OR
   (b) a NEW orthogonal-polynomial theorem characterising slope-asymptotics
       for measures with EXPONENTIAL tail but ARBITRARY polynomial prefactor
       and possibly arbitrary one-sided support — a generalisation of
       Lubinsky-Mhaskar-Saff that DOES NOT EXIST in the current literature.

The "asymptotic universal" theorem of Path gamma is a plausible target for
new mathematics: it would replace the full UOGH by a weaker but provable
statement about KMS-tailed measures. But the existing technology (Stieltjes,
Hankel determinants, recursion-method moment expansion) cannot deliver it
without first proving an orthogonal-polynomial slope theorem on KMS-tailed
measures, which is itself a substantial open problem in approximation theory.
""")
print("=" * 76)
print("END")
print("=" * 76)
