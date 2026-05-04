"""extend_2hat5.py — extend the H2/G15 Hecke eigenvalue computation
for 2̂(5) and 3̂,2(5) of S'_4 to higher primes (G1.6 follow-up).

For 2̂(5) we want to confirm the cuspidal sequence does NOT match any
LMFDB level-4/8/16 weight-5 form at higher primes (10+ values).

For 3̂,2(5) we want to confirm the 4.5.b.a CM match holds at higher
primes (it should, by uniqueness from Sturm bound; but verify).

Outputs to /home/remondiere/pc_calcs/extended_eigenvalues.json
"""
from fractions import Fraction
from sympy import S, Rational, sqrt as Ssqrt, simplify, Integer
import json, time

N = 1500   # q_4-truncation, larger than G15 default 400

# ----- q_4-expansions of theta, epsilon (NPP20 eq. 3.3) ------
def theta_q4(N):
    out = {n: Fraction(0) for n in range(N + 1)}
    out[0] = Fraction(1)
    k = 1
    while True:
        e = (2 * k) ** 2
        if e > N: break
        out[e] += Fraction(2)
        k += 1
    return out

def epsilon_q4(N):
    out = {n: Fraction(0) for n in range(N + 1)}
    k = 1
    while True:
        e = (2 * k - 1) ** 2
        if e > N: break
        out[e] += Fraction(2)
        k += 1
    return out

def mul_series(a, b, N):
    out = {n: Fraction(0) for n in range(N + 1)}
    for i, ai in a.items():
        if ai == 0 or i > N: continue
        for j, bj in b.items():
            if bj == 0 or i + j > N: continue
            out[i + j] += ai * bj
    return out

def power_series(a, k, N):
    if k == 0:
        return {n: Fraction(1) if n == 0 else Fraction(0) for n in range(N + 1)}
    if k == 1:
        return {n: a.get(n, Fraction(0)) for n in range(N + 1)}
    result = {n: a.get(n, Fraction(0)) for n in range(N + 1)}
    for _ in range(k - 1):
        result = mul_series(result, a, N)
    return result

def add_scaled(*pairs, N):
    out = {n: S(0) for n in range(N + 1)}
    for ca, d in pairs:
        for n in range(N + 1):
            v = d.get(n, 0)
            if v == 0: continue
            out[n] = out[n] + ca * v
    return out

def sympy_dict(d, N):
    out = {}
    for n in range(N + 1):
        f = d.get(n, Fraction(0))
        out[n] = Rational(f.numerator, f.denominator)
    return out

# ----- multiplets per NPP20 App D ------
def build_2hat_5(N):
    """Y_2̂^(5)(τ) = ((3/2)(ε³θ⁷ - ε⁷θ³); (√3/4)(εθ⁹ - ε⁹θ))"""
    th = sympy_dict(theta_q4(N), N); ep = sympy_dict(epsilon_q4(N), N)
    th3 = power_series(th, 3, N); th5 = power_series(th, 5, N)
    th7 = mul_series(th5, power_series(th, 2, N), N)
    th9 = mul_series(th7, power_series(th, 2, N), N)
    ep3 = power_series(ep, 3, N); ep5 = power_series(ep, 5, N)
    ep7 = mul_series(ep5, power_series(ep, 2, N), N)
    ep9 = mul_series(ep7, power_series(ep, 2, N), N)
    e3t7 = mul_series(ep3, th7, N); e7t3 = mul_series(ep7, th3, N)
    et9  = mul_series(ep, th9, N);  e9t  = mul_series(ep9, th, N)
    half3 = Rational(3, 2); sqrt3 = Ssqrt(3); qrt = Rational(1, 4)
    Y1 = add_scaled((half3, e3t7), (-half3, e7t3), N=N)
    Y2 = add_scaled((sqrt3 * qrt, et9), (-sqrt3 * qrt, e9t), N=N)
    return [Y1, Y2]

# Note: build_3hat_2_5 mirrors H2's reconstruction. Skip for now, verify
# 2̂(5) at high primes. Could add 3̂,2(5) later.

# ----- Hecke T(p) ------
def chi4(p):
    if p % 2 == 0: return 0
    return 1 if p % 4 == 1 else -1

def hecke_Tp(coeffs, p, k, N):
    out = {}
    pkm1 = Integer(p) ** (k - 1)
    for m in range(N + 1):
        t1 = coeffs.get(p * m, S(0)) if p * m <= N else S(0)
        t2 = pkm1 * coeffs.get(m // p, S(0)) if m % p == 0 else S(0)
        out[m] = simplify(t1 + t2)
    return out

def find_eigenvalue(f, Tpf, max_check):
    lam = None; pivot = None
    for n in range(max_check + 1):
        c = simplify(f.get(n, S(0)))
        if c == 0: continue
        candidate = simplify(Tpf.get(n, S(0)) / c)
        lam = candidate; pivot = n; break
    if lam is None:
        return False, None
    for n in range(max_check + 1):
        c = simplify(f.get(n, S(0)))
        t = simplify(Tpf.get(n, S(0)))
        if simplify(t - lam * c) != 0:
            return False, lam
    return True, lam

# ----- main ------
def main():
    t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] Building Y_2̂(5) at N={N}...", flush=True)
    Y2hat = build_2hat_5(N)
    print(f"  done in {time.time()-t0:.1f}s.  components={len(Y2hat)}", flush=True)

    primes = [5, 13, 17, 29, 37, 41, 53, 61, 73, 89, 97, 101, 109, 113]
    primes_class3 = [3, 7, 11, 19, 23, 31, 43, 47, 59, 67]

    results = {"2hat_5": {"primes_class1": {}, "primes_class3_obstructed": {}}}

    print(f"\n[{time.strftime('%H:%M:%S')}] 2̂(5) Hecke eigenvalues, p ≡ 1 mod 4:", flush=True)
    for p in primes:
        max_check = N // p - 1
        if max_check < 5: continue
        per_comp_lams = []
        for f in Y2hat:
            Tpf = hecke_Tp(f, p, k=5, N=N)
            ok, lam = find_eigenvalue(f, Tpf, max_check)
            per_comp_lams.append((ok, lam))
        all_ok = all(x[0] for x in per_comp_lams)
        lams = [x[1] for x in per_comp_lams if x[0] and x[1] is not None]
        common = (len(lams) == len(per_comp_lams)
                  and all(simplify(lams[0] - lj) == 0 for lj in lams))
        lam = lams[0] if common else None
        results["2hat_5"]["primes_class1"][p] = {
            "closed": all_ok, "common": common,
            "lambda": str(lam) if lam else None,
            "max_check": max_check,
        }
        print(f"  p={p:>4}  closed={all_ok} common={common}  λ(p)={lam}  (max_check={max_check})", flush=True)

    print(f"\n[{time.strftime('%H:%M:%S')}] 2̂(5) sanity check, p ≡ 3 mod 4 (expect obstruction):", flush=True)
    for p in primes_class3:
        max_check = N // p - 1
        if max_check < 5: continue
        f0 = Y2hat[0]
        Tpf = hecke_Tp(f0, p, k=5, N=N)
        ok, lam = find_eigenvalue(f0, Tpf, max_check)
        results["2hat_5"]["primes_class3_obstructed"][p] = {
            "closed_comp0": ok,
        }
        print(f"  p={p:>4}  comp[0] eigenform? {ok} ({'OBSTRUCTED' if not ok else '!!UNEXPECTED CLOSURE!!'})", flush=True)

    out_path = "/home/remondiere/pc_calcs/extended_2hat5_eigenvalues.json"
    with open(out_path, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\n[{time.strftime('%H:%M:%S')}] Total time = {time.time()-t0:.1f}s", flush=True)
    print(f"  Saved to {out_path}")

if __name__ == "__main__":
    main()
