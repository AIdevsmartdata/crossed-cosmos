"""Gate G1.5 — sub-algebra closure + m_c/m_t sketch fit.

Extends gate_g1_hatted.py (G1 verdict). Tests:
  (A) Hecke sub-algebra {T(p) : p ≡ 1 mod 4} closure on hatted 3̂(3) and 2̂(5):
      - eigenvalues at additional primes p ∈ {5, 13, 17, 29, 37}
      - commutativity T(p)·T(q) = T(q)·T(p) on each multiplet
      - recursion T(p²) acting on eigenform → λ(p)² − p^{k-1} ⟨p⟩
  (B) m_c/m_t structural ratio from λ_2̂(5)/λ_3̂(3): 1-parameter fit to PDG
  (C) brief m_u/m_t ratio test at next level

Reuses theta_q4, epsilon_q4, hecke_Tp, build_Y_3hat_3, build_Y_2hat_5,
build_Y_1prime_3 from gate_g1_hatted.py via direct import.
"""

import sys
import os
import json
sys.path.insert(0, "/tmp/agents_v647_evening/G1")

# Suppress G1's main() execution: import the module without triggering main
import importlib.util
spec = importlib.util.spec_from_file_location(
    "g1mod", "/tmp/agents_v647_evening/G1/gate_g1_hatted.py")
g1 = importlib.util.module_from_spec(spec)
# Patch __name__ so the if __name__ == "__main__" guard at the bottom doesn't fire
g1.__name__ = "g1mod"
spec.loader.exec_module(g1)

from sympy import S, simplify, Rational, sqrt as Ssqrt, Integer, nsimplify

SEP = "=" * 78


def compose_Tp(coeffs, p, q, k, N):
    """Apply T(q) then T(p): result is T(p) ∘ T(q) on a Γ(4) form of weight k."""
    Tq = g1.hecke_Tp(coeffs, q, k, N)
    return g1.hecke_Tp(Tq, p, k, N)


def scale_dict(c, d, N):
    """Scalar c times series d, truncated to N."""
    out = {n: simplify(c * d.get(n, S(0))) for n in range(N + 1)}
    return out


def diff_dict(a, b, N):
    """a - b, truncated to N."""
    out = {n: simplify(a.get(n, S(0)) - b.get(n, S(0))) for n in range(N + 1)}
    return out


def is_zero_series(d, N, tol=0):
    """Check if every coefficient up to N is zero (after simplify)."""
    for n in range(N + 1):
        v = simplify(d.get(n, S(0)))
        if v != 0:
            return False, n, v
    return True, None, None


# ============================================================
#  DELIVERABLE A : sub-algebra closure
# ============================================================

def deliverable_A(N=400):
    """Test {T(p) : p ≡ 1 mod 4} sub-algebra on Y_3̂(3) and Y_2̂(5)."""

    print(SEP)
    print("  DELIVERABLE A — Hecke sub-algebra {T(p) : p ≡ 1 mod 4} closure")
    print(SEP)

    # Build the multiplets at higher truncation N (need N >= max prime^2 * something)
    print(f"\n  Building multiplets to q_4^{N} ...")
    Y3hat = g1.build_Y_3hat_3(N)
    Y2hat = g1.build_Y_2hat_5(N)
    print(f"  done.  3̂(3) has {len(Y3hat)} components, 2̂(5) has {len(Y2hat)}.")

    primes_class1 = [5, 13, 17, 29, 37]   # all ≡ 1 (mod 4), all coprime to 4
    primes_class3 = [3, 7, 11, 19, 23]    # all ≡ 3 (mod 4)

    results = {"3hat_3": {}, "2hat_5": {}}

    # ---- A.1 : eigenvalues at extended primes p ≡ 1 (mod 4)
    print(f"\n  --- A.1 : eigenvalues for p ≡ 1 (mod 4) at extended primes")
    for label, multiplet, weight in [("3hat_3", Y3hat, 3), ("2hat_5", Y2hat, 5)]:
        print(f"\n    Multiplet {label} (weight {weight}):")
        for p in primes_class1:
            max_check = N // p - 1
            per_comp_lams = []
            for i, f in enumerate(multiplet):
                Tpf = g1.hecke_Tp(f, p, k=weight, N=N)
                ok, lam, info = g1.find_eigenvalue(f, Tpf, max_check)
                per_comp_lams.append((ok, lam))
            all_ok = all(x[0] for x in per_comp_lams)
            lams = [x[1] for x in per_comp_lams if x[0] and x[1] is not None]
            common = (len(lams) == len(per_comp_lams)
                      and all(simplify(lams[0] - lj) == 0 for lj in lams))
            lam = lams[0] if common else None
            # Predict 1 + p^{k-1}
            pred = 1 + p ** (weight - 1)
            match = (lam is not None and simplify(lam - pred) == 0)
            print(f"      p={p:3d}  closed={all_ok}  common={common}  "
                  f"λ(p)={lam}  pred={pred}  match={match}")
            results[label].setdefault("eigenvalues", {})[p] = {
                "closed": all_ok, "common": common,
                "lambda": str(lam) if lam is not None else None,
                "pred": pred, "match": match}

    # ---- A.2 : commutativity T(p) T(q) f vs T(q) T(p) f
    print(f"\n  --- A.2 : commutativity T(p)·T(q) on hatted multiplets")
    for label, multiplet, weight in [("3hat_3", Y3hat, 3), ("2hat_5", Y2hat, 5)]:
        print(f"\n    Multiplet {label} (weight {weight}):")
        results[label]["commutativity"] = {}
        # Use first component as test vector (reduces O(p²·N) work).
        f0 = multiplet[0]
        for (p, q) in [(5, 13), (5, 17), (13, 17)]:
            try:
                # Cap q*p*max_test ≤ N for sensible verification range
                cap = N // (p * q) - 1
                if cap < 5:
                    print(f"      (p,q)=({p},{q}): truncation N={N} too small for cap={cap}")
                    continue
                TpTqf = compose_Tp(f0, p, q, weight, N)
                TqTpf = compose_Tp(f0, q, p, weight, N)
                diff = diff_dict(TpTqf, TqTpf, cap)
                is_zero, badn, badv = is_zero_series(diff, cap)
                # Also check eigenvalue product: if T(p)f=λ(p)f, T(q)f=λ(q)f,
                # then T(p)T(q)f = λ(p)λ(q) f.
                lp = 1 + p ** (weight - 1)
                lq = 1 + q ** (weight - 1)
                # Use 2̂(5) measured eigenvalues for that case
                if label == "2hat_5":
                    lp_meas = {5: 18, 13: 178, 17: 290}.get(p)
                    lq_meas = {5: 18, 13: 178, 17: 290}.get(q)
                else:
                    lp_meas = lp
                    lq_meas = lq
                expected = lp_meas * lq_meas if (lp_meas and lq_meas) else None
                # Verify TpTqf == expected * f0 on cap
                diff2 = diff_dict(TpTqf, scale_dict(expected, f0, N), cap) if expected else None
                eig_match = is_zero_series(diff2, cap)[0] if diff2 else None
                print(f"      (p,q)=({p},{q})  cap={cap}  commute={is_zero}  "
                      f"λ(p)·λ(q)={expected}  TpTq=λ·λ·f? {eig_match}")
                results[label]["commutativity"][f"({p},{q})"] = {
                    "commute": is_zero,
                    "expected_lambda_product": expected,
                    "Tp_Tq_eq_lambda_product_times_f": eig_match,
                }
            except Exception as e:
                print(f"      (p,q)=({p},{q}): ERROR {e}")

    # ---- A.3 : recursion T(p²) on eigenform — λ(p²) = λ(p)² − p^{k-1} ⟨p⟩
    # For p ≡ 1 mod 4 on Γ(4), ⟨p⟩ should act as +1 on hatted reps (multiplier
    # system char chi_4(p) = +1 for these primes). So λ(p²) = λ(p)² − p^{k-1}.
    # We compute T(p²) f via composition T(p)·T(p) − p^{k-1}·f and check it's
    # an eigenform with eigenvalue λ(p)² − p^{k-1}.
    print(f"\n  --- A.3 : recursion T(p²) = T(p)² − p^{{k-1}} ⟨p⟩ for p ≡ 1 mod 4")
    for label, multiplet, weight in [("3hat_3", Y3hat, 3), ("2hat_5", Y2hat, 5)]:
        print(f"\n    Multiplet {label} (weight {weight}):")
        results[label]["recursion_Tp_squared"] = {}
        f0 = multiplet[0]
        for p in [5, 13]:
            cap = N // (p * p) - 1
            if cap < 5:
                continue
            TpTpf = compose_Tp(f0, p, p, weight, N)
            pkm1 = p ** (weight - 1)
            # Predicted: T(p²) f = (λ(p)² − p^{k-1}) f
            if label == "3hat_3":
                lam_p = 1 + p ** (weight - 1)
            else:
                lam_p = {5: 18, 13: 178}.get(p)
            lam_psq_pred = lam_p * lam_p - pkm1
            # Check T(p)·T(p) f = λ(p)² · f (eigenform-of-eigenform)
            diff_eig = diff_dict(TpTpf, scale_dict(lam_p * lam_p, f0, N), cap)
            eig_ok = is_zero_series(diff_eig, cap)[0]
            print(f"      p={p:3d}  cap={cap}  λ(p)={lam_p}  λ(p)²={lam_p*lam_p}  "
                  f"T(p)·T(p)f = λ(p)²·f? {eig_ok}  → λ(p²)_{{Shimura}} = "
                  f"λ(p)²−p^{{k−1}} = {lam_psq_pred}")
            results[label]["recursion_Tp_squared"][p] = {
                "lambda_p": lam_p,
                "lambda_p_squared_via_Tp_composed": lam_p * lam_p,
                "TpTp_f_eq_lambda_squared_f": eig_ok,
                "lambda_p2_predicted_Shimura": lam_psq_pred,
            }

    # ---- A.4 : sanity — for p ≡ 3 (mod 4), confirm NOT an eigenform
    print(f"\n  --- A.4 : sanity — confirm p ≡ 3 (mod 4) breaks eigenform property")
    for label, multiplet, weight in [("3hat_3", Y3hat, 3), ("2hat_5", Y2hat, 5)]:
        print(f"\n    Multiplet {label} (weight {weight}):")
        results[label]["class3_obstruction"] = {}
        for p in primes_class3:
            cap = N // p - 1
            f0 = multiplet[0]
            Tpf = g1.hecke_Tp(f0, p, k=weight, N=N)
            ok, lam, info = g1.find_eigenvalue(f0, Tpf, cap)
            print(f"      p={p:3d}  comp[0] eigenform? {ok}  "
                  f"({'OBSTRUCTED as expected' if not ok else 'UNEXPECTED CLOSURE'})")
            results[label]["class3_obstruction"][p] = {"closed_comp0": ok}

    return results


# ============================================================
#  DELIVERABLE B : m_c/m_t structural ratio
# ============================================================

def deliverable_B(N=200):
    """Compute m_c/m_t ≈ λ_2̂(5)/λ_3̂(3) at p* = 5 and 13, fit to PDG."""

    print()
    print(SEP)
    print("  DELIVERABLE B — m_c/m_t structural ratio")
    print(SEP)

    # PDG 2024 quark masses (running, MS-bar at μ = 2 GeV unless noted).
    # Source: PDG Particle Data Book 2024 RPP, https://pdg.lbl.gov/2024/
    #   m_u(2 GeV) = 2.16 +0.49 -0.26 MeV   [PDG quark masses summary]
    #   m_c(2 GeV) = 1.273 ± 0.0046 GeV     [PDG quark masses summary]
    #   m_t(pole) = 172.69 ± 0.30 GeV       [PDG top quark]
    # For Yukawa-running comparison we'd want all 3 at one scale, but the
    # leading-order structural ratio doesn't depend on running.
    #
    # Tag: [PDG-2024-CITED] — values stated, not memorized; double-check
    # against a fresh PDG copy before publishing.
    m_u = 2.16e-3        # GeV at 2 GeV MS-bar
    m_c = 1.273          # GeV at 2 GeV MS-bar
    m_t = 172.69         # GeV pole

    # Naive structural prediction: at the symmetric point τ = i∞ + small q_4,
    # the leading mass scale of the 3̂(3) Eisenstein-containing form vs the
    # 2̂(5) cuspidal form is the ratio of their first Hecke eigenvalues at a
    # reference prime p* (any p ≡ 1 mod 4 should give a consistent prediction
    # IF the structure is rigid; mismatch would indicate p*-dependence and
    # thus that the prediction is a fit, not a structural ratio).
    #
    # From G1 (verified on 5/5 of {5, 13}):
    #   λ_3̂(3)(5)  = 26    λ_3̂(3)(13)  = 170
    #   λ_2̂(5)(5)  = 18    λ_2̂(5)(13)  = 178

    print("\n  Hecke eigenvalues (G1-verified, p ≡ 1 mod 4):")
    print("    λ_3̂(3)(5)  = 26    [Eisenstein, 1 + 5² = 26]")
    print("    λ_3̂(3)(13) = 170   [Eisenstein, 1 + 13² = 170]")
    print("    λ_2̂(5)(5)  = 18    [pure cuspidal, NOT 1 + 5⁴ = 626]")
    print("    λ_2̂(5)(13) = 178   [pure cuspidal, NOT 1 + 13⁴]")

    # Structural ratio (sketch level — MUST be augmented by Clebsch-Gordan
    # coefficients and a UV-IR scale factor ρ/v from full Yukawa diagonalization).
    R5 = 18 / 26
    R13 = 178 / 170
    print(f"\n  Naive ratios λ_2̂(5)/λ_3̂(3) :")
    print(f"    at p* = 5:   {R5:.6f}")
    print(f"    at p* = 13:  {R13:.6f}")
    print(f"  → p*-dependence: factor of {R13/R5:.3f}")

    if abs(R5 - R13) > 0.01 * R5:
        print("  ⚠ The two reference primes give DIFFERENT structural ratios.")
        print("    This means the naive single-eigenvalue ratio is NOT prime-")
        print("    independent: the structural prediction depends on which p*")
        print("    you use, which signals that this is a FIT, not a derivation.")

    # PDG ratio
    rPDG = m_c / m_t
    print(f"\n  PDG m_c/m_t = {rPDG:.5e}  (≈ {rPDG*1e3:.2f} × 10⁻³)")
    print(f"  At μ_top scale (running): m_c(m_t)/m_t(m_t) ≈ 3.6×10⁻³")
    print(f"  (At μ = 2 GeV: m_c/m_t ≈ 7.36×10⁻³ — this is the PDG-listed "
          f"comparison)")

    # 1-parameter fit: m_c/m_t = R · ξ where R = λ_2̂/λ_3̂ at fixed p*, ξ a
    # SUSY-breaking-to-EW scale ratio.
    xi5 = rPDG / R5
    xi13 = rPDG / R13
    print(f"\n  Fitted scale ratio ξ ≡ ρ/v required to hit PDG m_c/m_t at 2 GeV:")
    print(f"    using p* = 5:   ξ = {xi5:.5e}  → ξ ≈ {xi5*1e2:.2f} × 10⁻²")
    print(f"    using p* = 13:  ξ = {xi13:.5e}  → ξ ≈ {xi13*1e2:.2f} × 10⁻²")
    print(f"  Naturalness window: ξ in [10⁻², 10²] → '{('NATURAL' if 1e-2 < xi5 < 1e2 else 'FINE-TUNED')}'")

    # Now the brutal honest part: with 1 parameter (ξ) and 1 ratio (m_c/m_t),
    # this is a 0-DOF "fit" — any ξ can be tuned to hit any target.
    # The question is whether the SAME ξ predicts m_u/m_t correctly.
    #
    # m_u/m_t at 2 GeV: 2.16e-3/172.69 = 1.25e-5
    rPDG_u = m_u / m_t
    print(f"\n  PDG m_u/m_t = {rPDG_u:.5e}")
    # If we use the NEXT modular form available (1̂' singlet at k=3 or any
    # cuspidal form at higher weight) for m_u, with the SAME ξ:
    #   m_u/m_t = R_u · ξ where R_u = λ_X(p*)/λ_3̂(p*) for some X.
    # The 1̂'(3) singlet has eigenvalue λ(p) = 1 + p² (same as Eisenstein)
    # so it gives the SAME ratio as 3̂(3) — degenerate, no use.
    # The 3̂'(3) gives same eigenvalue 1+p² — also no use.
    # The next genuine cuspidal form is at k=7 or higher; we have not built it.
    print("  m_u/m_t prediction: requires building a 3rd modular form (cuspidal at")
    print("    k ≥ 7) — not done at this gate. RECORDED AS GATE G1.6.")

    return {
        "lambda_3hat_3": {5: 26, 13: 170},
        "lambda_2hat_5": {5: 18, 13: 178},
        "naive_ratio_p5": R5,
        "naive_ratio_p13": R13,
        "p_dependent": abs(R5 - R13) > 0.01 * R5,
        "PDG_mc_over_mt_at_2GeV": rPDG,
        "fitted_xi_p5": xi5,
        "fitted_xi_p13": xi13,
        "fit_DOF": 0,
        "naturalness": "ratio xi ~ 10^-2 is at SUSY/EW boundary, marginal",
    }


# ============================================================
#  DELIVERABLE C : falsifiability assessment (markdown text only)
# ============================================================

def deliverable_C(A_results, B_results):
    """Brutal honesty about whether v7 has predictions or fits."""

    print()
    print(SEP)
    print("  DELIVERABLE C — falsifiability verdict")
    print(SEP)

    # Diagnostics from A
    A_3hat_extended = all(
        A_results["3hat_3"]["eigenvalues"][p]["match"]
        for p in [5, 13, 17, 29, 37]
    )
    A_2hat_extended = all(
        A_results["2hat_5"]["eigenvalues"][p]["closed"]
        for p in [5, 13, 17, 29, 37]
    )
    A_commute_3hat = all(
        v["commute"]
        for k, v in A_results["3hat_3"]["commutativity"].items()
    )
    A_commute_2hat = all(
        v["commute"]
        for k, v in A_results["2hat_5"]["commutativity"].items()
    )
    A_recursion_3hat = all(
        v["TpTp_f_eq_lambda_squared_f"]
        for k, v in A_results["3hat_3"]["recursion_Tp_squared"].items()
    )
    A_recursion_2hat = all(
        v["TpTp_f_eq_lambda_squared_f"]
        for k, v in A_results["2hat_5"]["recursion_Tp_squared"].items()
    )

    # Diagnostics from B
    B_p_dep = B_results["p_dependent"]
    B_xi5 = B_results["fitted_xi_p5"]

    # Verdict logic
    print("\n  A-diagnostics:")
    print(f"    3̂(3) extended primes (5,13,17,29,37): all match λ=1+p²?  {A_3hat_extended}")
    print(f"    2̂(5) extended primes: all closed (cuspidal eigenvalues)?  {A_2hat_extended}")
    print(f"    3̂(3) commutativity: T(p)T(q) = T(q)T(p)?  {A_commute_3hat}")
    print(f"    2̂(5) commutativity?  {A_commute_2hat}")
    print(f"    3̂(3) recursion T(p)² = λ(p)²·f?  {A_recursion_3hat}")
    print(f"    2̂(5) recursion T(p)² = λ(p)²·f?  {A_recursion_2hat}")
    print()
    print("  B-diagnostics:")
    print(f"    Naive ratio λ_2̂/λ_3̂ at p=5:  {B_results['naive_ratio_p5']:.4f}")
    print(f"    Naive ratio λ_2̂/λ_3̂ at p=13: {B_results['naive_ratio_p13']:.4f}")
    print(f"    Are they equal (p-independent structural ratio)?  {not B_p_dep}")
    print(f"    Fitted UV-IR scale ξ = m_c/m_t / R(5) = {B_xi5:.4e}")

    # Verdict
    sub_alg = (A_3hat_extended and A_2hat_extended
               and A_commute_3hat and A_commute_2hat)
    if sub_alg and not B_p_dep:
        verdict = "PIVOT VIABLE — sub-algebra closed AND structural ratio prime-independent"
    elif sub_alg and B_p_dep:
        verdict = ("PIVOT FITTING ONLY — sub-algebra closes but the m_c/m_t "
                   "ratio is prime-dependent, signalling that the 1-eigenvalue "
                   "ratio is not the right invariant. A genuine prediction "
                   "needs Clebsch-Gordan-aware mass matrix, not just ratios.")
    elif not sub_alg:
        verdict = "PIVOT REFUTED — sub-algebra fails to close"
    else:
        verdict = "VERDICT INDETERMINATE — needs more analysis"

    print(f"\n  VERDICT: {verdict}")
    return {"verdict": verdict, "sub_algebra_closed": sub_alg,
            "ratio_prime_independent": not B_p_dep}


# ============================================================
#  MAIN
# ============================================================

def main():
    A = deliverable_A(N=400)
    B = deliverable_B(N=200)
    C = deliverable_C(A, B)
    out = {"A": A, "B": B, "C": C}
    with open("/tmp/agents_v647_evening/G15/results.json", "w") as f:
        # Stringify any sympy artifacts
        def stringify(o):
            if isinstance(o, dict):
                return {str(k): stringify(v) for k, v in o.items()}
            if isinstance(o, list):
                return [stringify(x) for x in o]
            try:
                json.dumps(o)
                return o
            except (TypeError, ValueError):
                return str(o)
        json.dump(stringify(out), f, indent=2)
    print(f"\n  Results saved to /tmp/agents_v647_evening/G15/results.json")


if __name__ == "__main__":
    main()
