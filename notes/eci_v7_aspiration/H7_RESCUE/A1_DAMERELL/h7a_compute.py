"""
H7-A: Compute L(f, m) for the weight-5 CM newform 4.5.b.a (level 4, char chi_{-4}, CM by Q(i)).

The form is f = sum a_n q^n with q-expansion (from LMFDB live):
  q - 4 q^2 + 16 q^4 - 14 q^5 - 64 q^8 + 81 q^9 + 56 q^10 - 238 q^13
    + 256 q^16 + 322 q^17 - 324 q^18 - 224 q^20 + ...

This is a CM newform: f corresponds to a Hecke Grossencharacter psi of Q(i)
of infinity type (k-1, 0) = (4, 0), so for primes p split in Q(i) (p == 1 mod 4),
a_p = psi(p) + conjugate(psi(p)) = pi^4 + bar(pi)^4 where p = pi*bar(pi);
for primes p inert (p == 3 mod 4), a_p = 0;
for ramified prime p=2, a_2 = -4 (from the q-expansion).

We use this to compute a_p for all primes up to a cutoff, then use the
approximate functional equation / Euler product partial sums to evaluate
L(f, m) for m = 1, 2, 3, 4.

Critical strip / functional equation (LMFDB-confirmed):
- weight k = 5, level N = 4, sign = +1, conductor 4
- Lambda(s) = N^{s/2} (2 pi)^{-s} Gamma(s) L(s)
- Functional equation: Lambda(s) = epsilon * Lambda(k - s) = Lambda(5 - s)
- So L(f, m) and L(f, 5-m) are related via the gamma factor ratio.
- Integer critical points (Deligne): m in {1, 2, 3, 4}.

Cardy targets: rho = c/12 for c in {1, 1/2, 7/10, 4/5}:
  c=1   -> rho = 1/12  ~ 0.08333...
  c=1/2 -> rho = 1/24  ~ 0.04167...
  c=7/10-> rho = 7/120 ~ 0.05833...
  c=4/5 -> rho = 4/60 = 1/15 ~ 0.06667...
"""

from mpmath import mp, mpf, mpc, sqrt, pi, exp, log, gamma, quad, nsum, inf, fabs, power
from sympy import isprime, primerange, factorint, Rational
from sympy.ntheory import primefactors

mp.dps = 40  # 40 decimal digits of precision

# ---------------------------------------------------------------------------
# Step 1: build a_n for the form 4.5.b.a using CM structure.
# ---------------------------------------------------------------------------

def hecke_a_p_split(p):
    """For p == 1 mod 4 (split in Q(i)), find pi = a + b i with N(pi) = p,
    return a_p = pi^4 + conj(pi)^4 = 2 Re(pi^4).
    Choice of pi up to units {1, i, -1, -i} and conjugation; the form is
    fixed by the LMFDB normalization. Try both signs and pick the one
    matching the q-expansion."""
    # Find a, b with a^2 + b^2 = p, a odd > 0, b even (Gauss normalization);
    # this fixes pi uniquely up to conjugation.
    for a in range(1, int(p**0.5) + 1, 2):  # a odd
        b2 = p - a*a
        if b2 < 0:
            continue
        b = int(round(b2 ** 0.5))
        if b*b == b2 and b % 2 == 0:
            # pi = a + b i
            pi_c = complex(a, b)
            # a_p = 2 Re(pi^4)
            val = 2 * (pi_c ** 4).real
            return int(round(val))
    return None

def build_a_n(N_max):
    """Return dict a[n] for n = 1..N_max."""
    a = {1: 1}
    # Compute a_p first
    a_p = {}
    for p in primerange(2, N_max + 1):
        if p == 2:
            a_p[p] = -4   # from q-expansion (q-coefficient for q^2 is -4)
        elif p % 4 == 3:
            a_p[p] = 0    # inert
        else:
            # p % 4 == 1, split
            val = hecke_a_p_split(p)
            a_p[p] = val
    # Sanity: check small primes against q-expansion
    # q-expansion: a_5 = -14, a_13 = -238, a_17 = 322, a_29 = ?, a_37 = ?
    expected = {2: -4, 3: 0, 5: -14, 7: 0, 11: 0, 13: -238, 17: 322}
    for p, v in expected.items():
        assert a_p[p] == v, f"a_{p}: got {a_p[p]}, expected {v}"
    # Build a_n via Hecke multiplicativity for prime powers:
    #   a_{p^{r+1}} = a_p * a_{p^r} - chi(p) p^{k-1} a_{p^{r-1}}
    # Character chi_{-4} (mod 4): chi(odd) = (-1)^((p-1)/2), chi(even) = 0.
    # k = 5 so p^{k-1} = p^4.
    def chi(p):
        if p % 2 == 0:
            return 0
        return 1 if p % 4 == 1 else -1
    # Build prime power table
    a_pp = {}  # a_pp[(p, r)] = a_{p^r}
    for p in a_p:
        a_pp[(p, 0)] = 1
        a_pp[(p, 1)] = a_p[p]
        r = 1
        while p ** (r + 1) <= N_max:
            a_pp[(p, r+1)] = a_p[p] * a_pp[(p, r)] - chi(p) * (p**4) * a_pp[(p, r-1)]
            r += 1
    # Now build a_n for composite n by multiplicativity over coprime factors
    for n in range(2, N_max + 1):
        fac = factorint(n)
        v = 1
        for p, r in fac.items():
            v *= a_pp[(p, r)]
        a[n] = v
    return a

# Quick verification
N_TEST = 25
a_test = build_a_n(N_TEST)
expected_qexp = {1:1, 2:-4, 4:16, 5:-14, 8:-64, 9:81, 10:56, 13:-238,
                 16:256, 17:322, 18:-324, 20:224}
# NOTE: q-expansion as given was "+ 56 q^10" but a_2 a_5 = (-4)(-14) = 56. Good.
# "-224 q^20": a_4 a_5 = 16 * (-14) = -224. The LMFDB string had -224, good.
# "-324 q^18": a_2 a_9 = (-4)(81) = -324. Good.
print("Verification a_n vs q-expansion:")
for n in sorted(expected_qexp):
    got = a_test[n]
    exp_v = expected_qexp[n]
    ok = "OK" if got == exp_v else f"MISMATCH (expected {exp_v})"
    print(f"  a_{n} = {got}  {ok}")

# ---------------------------------------------------------------------------
# Step 2: evaluate L(f, m) via the approximate functional equation.
# ---------------------------------------------------------------------------
#
# For an L-function with completed form
#   Lambda(s) = N^{s/2} (2 pi)^{-s} Gamma(s) L(s),
# functional equation Lambda(s) = epsilon * Lambda(k-s) (here epsilon = +1, k=5),
# the standard approximate functional equation gives, for any cutoff X > 0:
#
#   L(s) = sum_{n>=1} a_n / n^s * G_+(n, s, X)
#        + epsilon * (gamma factor ratio) * sum_{n>=1} a_n / n^{k-s} * G_-(n, s, X)
#
# where G_+, G_- are smoothing functions involving incomplete gamma. For
# numerical work we use the Riemann-style smoothing
#   G_+(n, s, X) = Gamma(s, 2 pi n X / sqrt(N)) / Gamma(s)
#   G_-(n, s, X) = Gamma(k-s, 2 pi n / (X sqrt(N))) / Gamma(k-s)
# and we take X = 1 (symmetric split).
#
# Full reference: Iwaniec-Kowalski, "Analytic Number Theory", Thm 5.3.

mp.dps = 50
N_LEVEL = mpf(4)
WEIGHT = 5
EPSILON = mpf(1)
SQRT_N = sqrt(N_LEVEL)
TWO_PI = 2 * pi

def incomplete_gamma_upper(s, x):
    """Upper incomplete gamma Gamma(s, x) = int_x^inf t^{s-1} e^{-t} dt."""
    # mpmath's gammainc(s, a, b) computes int_a^b ... ; with regularized=False
    # gammainc(s, a) = int_a^inf t^{s-1} e^{-t} dt
    from mpmath import gammainc
    return gammainc(s, x)

def L_value(s, N_terms=2000, X=mpf(1)):
    """Compute L(f, s) via approximate functional equation."""
    s = mpf(s) if not isinstance(s, (mpc, complex)) else s
    k = mpf(WEIGHT)
    # Build a_n once
    a = build_a_n(N_terms)
    # Sum 1: sum a_n / n^s * Gamma(s, 2 pi n X / sqrt(N)) / Gamma(s)
    total1 = mpf(0)
    Gs = gamma(s)
    cutoff1 = TWO_PI * X / SQRT_N
    for n in range(1, N_terms + 1):
        an = a[n]
        if an == 0:
            continue
        x_arg = cutoff1 * n
        term = mpf(an) / mpf(n)**s * incomplete_gamma_upper(s, x_arg) / Gs
        total1 += term
    # Sum 2: epsilon * (gamma-factor ratio) * sum a_n / n^{k-s} * Gamma(k-s, 2 pi n / (X sqrt(N))) / Gamma(k-s)
    # The gamma-factor ratio for Lambda(s) = (sqrt(N)/(2pi))^s Gamma(s) L(s) is:
    #   ratio = (sqrt(N)/(2pi))^{k-2s}  -- this comes from Lambda(k-s)/Lambda(s) on L-side
    # Working it out:
    #   L(s) = (term1 from upper sum) + epsilon * (sqrt(N)/(2pi))^{k-2s} * Gamma(k-s)/Gamma(s) * (term2 base sum)
    # Wait — cleaner derivation: define lambda(s) = (sqrt(N)/(2pi))^s Gamma(s).
    # Then Lambda(s) = lambda(s) L(s). FE: lambda(s) L(s) = eps lambda(k-s) L(k-s).
    # So L(s) = eps (lambda(k-s)/lambda(s)) L(k-s).
    # The approximate FE writes
    #   L(s) = sum_n a_n/n^s * V_s(n) + eps (lambda(k-s)/lambda(s)) sum_n a_n/n^{k-s} * V_{k-s}(n)
    # where V_s(n) = (1/Gamma(s)) Gamma(s, 2 pi n X / sqrt(N)).
    # Reference: Iwaniec-Kowalski (5.16) with M=1, q=1.
    Gks = gamma(k - s)
    cutoff2 = TWO_PI / (X * SQRT_N)
    total2 = mpf(0)
    for n in range(1, N_terms + 1):
        an = a[n]
        if an == 0:
            continue
        x_arg = cutoff2 * n
        term = mpf(an) / mpf(n)**(k - s) * incomplete_gamma_upper(k - s, x_arg) / Gks
        total2 += term
    lam_ratio = (SQRT_N / TWO_PI)**(k - 2*s) * Gks / Gs
    L = total1 + EPSILON * lam_ratio * total2
    return L

# Sanity: compute L(5/2) and compare to LMFDB's 0.5200744676
print("\nSanity check L(f, 5/2):")
val_half = L_value(mpf(5)/2, N_terms=1500)
print(f"  L(5/2) computed = {val_half}")
print(f"  LMFDB           = 0.5200744676")

# Now compute integer critical values
print("\nL(f, m) for integer m in {1,2,3,4}:")
results = {}
for m in [1, 2, 3, 4]:
    v = L_value(mpf(m), N_terms=1500)
    results[m] = v
    print(f"  L(f, {m}) = {v}")

# ---------------------------------------------------------------------------
# Step 3: Shimura periods.
# Per Deligne / Shimura, for a CM form of weight k with CM by imaginary
# quadratic K = Q(sqrt(-d)) and Hecke character psi of infinity type (k-1, 0),
# the periods are essentially powers of the elliptic period of an associated
# CM elliptic curve. For K = Q(i), the canonical period is
#   Omega_K = Gamma(1/4)^2 / (2 sqrt(2 pi))   (Chowla-Selberg)
# and L(psi^j, j) ~ Omega_K^{2j-1} * (algebraic) for various j.
#
# More concretely (Damerell 1971, Shimura 1976), for f of weight k with
# CM by K = Q(i) and conductor 4:
#   L(f, m) = (algebraic) * (2 pi)^m * Omega_K^{??}  for m integer in [1, k-1].
#
# Rather than re-derive Shimura's formula, we COMPUTE the ratios
#   L(f, m) / Omega_K^a / pi^b
# and look for SIMPLE RATIONALS, which is the empirical test we need anyway
# for the Cardy bridge.
# ---------------------------------------------------------------------------

# Chowla-Selberg period for Q(i):
Omega_K = gamma(mpf(1)/4)**2 / (2 * sqrt(2 * pi))
print(f"\nOmega_K (Chowla-Selberg for Q(i)) = {Omega_K}")

# ---------------------------------------------------------------------------
# Step 4: Cardy match.
# ---------------------------------------------------------------------------

cardy_targets = {
    "c=1   (free boson)":    Rational(1, 12),
    "c=1/2 (Ising)":          Rational(1, 24),
    "c=7/10 (tricritical)":   Rational(7, 120),
    "c=4/5 (3-state Potts)":  Rational(1, 15),
}

print("\nCardy targets rho = c/12:")
for k_name, q in cardy_targets.items():
    print(f"  {k_name:30s} rho = {q} = {mpf(q.p)/mpf(q.q)}")

# Search: for each m in {1,2,3,4} and each Cardy target, is there a
# small rational p/q such that (p/q) * L(f, m) ~ rho_target?
# Equivalently, is rho_target / L(f, m) a small rational?

from fractions import Fraction
def best_rational(x, max_denom=200):
    """Find best p/q approximation to x with denominator <= max_denom."""
    # Use mpmath's pslq or sympy's nsimplify; we'll do continued fractions.
    fx = Fraction(str(float(x))).limit_denominator(max_denom)
    err = abs(mpf(fx.numerator) / mpf(fx.denominator) - x)
    return fx, err

print("\n=== Cardy-bridge search: rho_target / L(f, m) as rational ===")
hits = []
for m in [1, 2, 3, 4]:
    Lm = results[m]
    if abs(Lm) < mpf(10)**-30:
        print(f"  L(f, {m}) ~ 0, skipping ratio")
        continue
    for cname, rho in cardy_targets.items():
        rho_f = mpf(rho.p) / mpf(rho.q)
        ratio = rho_f / Lm
        bf, err = best_rational(ratio, max_denom=200)
        # Also try rho/(L*pi^j), rho/(L*Omega_K^j)
        msg = f"  m={m}, {cname:30s}: rho/L = {float(ratio):+.6f} ~ {bf} (err={float(err):.2e})"
        print(msg)
        if err < mpf("1e-6") and max(abs(bf.numerator), bf.denominator) < 50:
            hits.append((m, cname, bf, err))

# Also check L(f,m) / Omega_K^a for a in 1..6
print("\n=== Algebraic part: L(f, m) / (pi^a * Omega_K^b) ===")
for m in [1, 2, 3, 4]:
    Lm = results[m]
    print(f"\n  m = {m}, L(f, {m}) = {float(Lm):+.10f}")
    for a in range(0, 6):
        for b in range(0, 8):
            if a == 0 and b == 0:
                continue
            denom = pi**a * Omega_K**b
            r = Lm / denom
            bf, err = best_rational(r, max_denom=100)
            if err < mpf("1e-8") and max(abs(bf.numerator), bf.denominator) < 100:
                print(f"    L(f,{m}) / (pi^{a} * Omega_K^{b}) ~ {bf}  (err={float(err):.2e})")

print("\n=== END H7-A computation ===")
