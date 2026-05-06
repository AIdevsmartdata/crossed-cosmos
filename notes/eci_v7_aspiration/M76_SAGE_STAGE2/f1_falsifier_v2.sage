##############################################################################
# f1_falsifier_v2.sage
# F1 Falsifier — Conjecture M13.1(a) FE-symmetric 2-adic interpolation
#
# VERSION: v2  (M76 Sage 10.7 compatibility pass, 2026-05-06)
# CHANGES from v1 (M63):
#   - ADDED: `--smoke` flag support via sys.argv
#   - ADDED: smoke_test() function for --smoke dry-run (imports + newform only)
#   - UPDATED: Sage 10.7 module status comments on each TODO
#   - KEPT: all TODO markers and NotImplementedError stubs unchanged
#   - CORRECTED: import list reviewed against Sage 10.7 stdlib
#   - NOTE: f1_falsifier.sage v1 imports were already correct for Sage 10.7.
#     (NumberField, Newforms, DirichletGroup, Qp are all in Sage 10.7 stdlib.)
#     The import that FAILED in the R3 script was ModularCurve — not present here.
#
# PROTOCOL (M44 falsifiers.md, F1):
#   Test whether the Bertolini-Darmon Heegner 2-adic distribution L_2^+/- for
#   f = 4.5.b.a (Q(i) CM, weight 5, conductor 4) satisfies
#
#       integral_{Gamma} chi_m dL_2^+(f) = (alpha_m + alpha_{5-m}) / 2
#
#   for m in {1,2,3,4}, where Gamma = anticyclotomic Z_2-Galois group of
#   Q(i)_infty^{anti}, and alpha_m are the Damerell critical values confirmed
#   by PARI/GP in M52 F2 v6.
#
# STATUS: SKELETON — NOT RUNNABLE WITHOUT SUBROUTINE IMPLEMENTATIONS.
#   See TODO markers below for missing pieces.
#   Estimated specialist effort: 30-40 h (Buyukboduk / Lei for BDP machinery).
#
# SAGE 10.7 MODULE STATUS:
#   AVAILABLE in Sage 10.7 stdlib (can be used now):
#     - NumberField, QQ, ZZ, PolynomialRing: yes
#     - Newforms, DirichletGroup: yes
#     - Qp (p-adic field): yes
#   PARTIAL support:
#     - Hecke Grossencharacters on imaginary quadratic fields: limited
#       (HeckeCharGroup exists but support for infinity-type is thin)
#   NOT IN STDLIB / SPECIALIST NEEDED:
#     - BDP Heegner 2-adic distribution (Buyukboduk-Lei arXiv:1709.02912)
#     - Anticyclotomic Z_2-tower construction for ramified p=2
#     - Kobayashi +/- subgroup decomposition for supersingular p=2
#
# RUN:  sage f1_falsifier_v2.sage           # full scaffold (dry run)
#       sage f1_falsifier_v2.sage --smoke   # minimal smoke test
##############################################################################

import sys

SMOKE = "--smoke" in sys.argv

from sage.all import (
    NumberField, QQ, ZZ, PolynomialRing,
    Newforms, DirichletGroup,
    Qp,  # 2-adic field — confirmed in Sage 10.7 stdlib
)

print("=" * 70)
print("F1 FALSIFIER v2 — Conjecture M13.1(a) FE-symmetric 2-adic interpolation")
print("Sage 10.7 compatibility pass (M76, 2026-05-06)")
print("Status: SKELETON. Fill TODO subroutines before running.")
if SMOKE:
    print("[MODE] --smoke: minimal dry-run, no raises, exit after summary.")
print("=" * 70)

# ---------------------------------------------------------------------------
# 0.  BASE FIELD AND CM NEWFORM
# ---------------------------------------------------------------------------

R = PolynomialRing(QQ, 'x')
x = R.gen()

K = NumberField(x**2 + 1, 'i')
i_K = K.gen()  # sqrt(-1)

# Fundamental discriminant d_K = -4; class number h_K = 1
# Conductor of Hecke Grossencharacter: (1+i)^2 in O_K = Z[i]
# Infinity-type: z^4 (weight k=5, so (k-1, 0) = (4, 0))
conductor_elem = (1 + i_K)**2   # = 2i in Z[i], norm = 4

# Reference newform: LMFDB label 4.5.b.a
#   Level N=4, weight k=5, character chi_{-4} (Kronecker symbol mod 4)
#   Hecke eigenvalue a_2 = -4 (Steinberg edge)
#   CM by K = Q(i)

chi_group = DirichletGroup(4, QQ)
# chi_group[1] is the non-trivial character mod 4 (Kronecker symbol (-4/·))
chi_neg4 = chi_group[1]

S_forms = Newforms(Gamma1(4), 5, names='a')
assert len(S_forms) >= 1, "Expected at least one newform at level 4 weight 5 chi_{-4}"
f = S_forms[0]

# Steinberg edge anchor: a_2(f) = -2^{(k-1)/2} = -2^2 = -4
a2 = f.q_expansion(3)[2]
expected_a2 = -4
assert a2 == expected_a2, (
    f"Steinberg edge CHECK FAILED: a_2 = {a2}, expected {expected_a2}"
)
print(f"[OK] f = 4.5.b.a confirmed: a_2 = {a2}")

if SMOKE:
    print("\n[SMOKE] NumberField, Newforms, DirichletGroup, Qp: all import OK in Sage 10.7.")
    print("[SMOKE] Newform f = 4.5.b.a confirmed: a_2 = -4. Scaffold loads cleanly.")
    print("[SMOKE] Exiting after smoke test (no specialist TODO calls).")
    print("[SMOKE] RESULT: f1_falsifier_v2.sage smoke test PASSED.")
    sys.exit(0)

# ---------------------------------------------------------------------------
# 1.  DAMERELL CRITICAL VALUES  (M52 F2 v6, PARI 80-digit verified)
# ---------------------------------------------------------------------------
# alpha_m = L(f, m) / Omega_f^{2m-1}  (normalized Damerell values)
# For f = 4.5.b.a, alpha_m in {1/10, 1/12, 1/24, 1/60} (all rational).
# These are the F1-renormalised ladders per M22 / falsifiers.md F2.

alpha_m = {
    1: QQ(1)/QQ(10),   # 1/10
    2: QQ(1)/QQ(12),   # 1/12
    3: QQ(1)/QQ(24),   # 1/24
    4: QQ(1)/QQ(60),   # 1/60
}
print(f"[OK] Damerell ladder loaded: alpha = {alpha_m}")

# F1 Conjecture M13.1(a) prediction: FE-symmetric mean
# k = 5, so k - m runs through {4, 3, 2, 1} as m runs through {1, 2, 3, 4}
predicted_plus = {}
predicted_minus = {}
for m in [1, 2, 3, 4]:
    predicted_plus[m]  = (alpha_m[m] + alpha_m[5 - m]) / 2
    predicted_minus[m] = (alpha_m[m] - alpha_m[5 - m]) / 2

print("[OK] M13.1(a) predictions:")
for m in [1, 2, 3, 4]:
    print(f"     m={m}: predicted_plus = {predicted_plus[m]},  "
          f"predicted_minus = {predicted_minus[m]}")

# ---------------------------------------------------------------------------
# 2.  ANTICYCLOTOMIC Z_2-TOWER  (SKELETON — TODO #1)
# ---------------------------------------------------------------------------
# Gamma = Gal(K_infty^{anti} / K) where K_infty^{anti} is the anticyclotomic
# Z_2-extension of K = Q(i).
#
# For Q(i) at p = 2:
#   - p = 2 is RAMIFIED in K/Q (d_K = -4)
#   - Complex conjugation acts as inversion on Gamma
#   - Topological generator gamma acts on characters via m-th power
#
# CAUTION (from M44 F5 falsifier — EXECUTED, FALSIFIED):
#   Standard IMC theorems (Hsieh 2014, Chida-Hsieh 2015, Arnold 2007,
#   Pollack-Weston 2011) ALL exclude p=2 ramified in K or p supersingular
#   with k odd. The BDP distribution L_2^+/- EXISTS as a formal construction
#   but Iwasawa-theoretic properties are NOT guaranteed by existing theorems.
#   The falsifier tests the interpolation DIRECTLY.
#
# SAGE 10.7 STATUS:
#   - NumberField, Qp: available (can compute conductors, units)
#   - Explicit anticyclotomic tower via Lubin-Tate / CM theory: NOT in stdlib
#   - de Shalit formal group: NOT in Sage stdlib natively
#
# TODO #1 [SPECIALIST, ~5 h]:
#   Status: SPECIALIST NEEDED (Iwasawa theorist, p=2 ramified CM case)
#   Implement AnticyclotomicGalois(K, 2) returning:
#     .gen()  -- topological generator gamma
#     .char_at_n(m, n)  -- m-th character at level-n approximation
#   References:
#     - de Shalit "Iwasawa Theory of Elliptic Curves with CM" (1987) §1-2
#     - Rubin "The 'main conjectures' of Iwasawa theory..." Invent. Math. 103
#     - Bertolini-Darmon 2001 §2

class AnticyclotomicGaloisScaffold:
    """
    Placeholder for Gal(K_infty^{anti} / K), K = Q(i), p = 2.

    TODO #1 [SPECIALIST, ~5 h]: Implement using CM theory and the explicit
    Lubin-Tate / formal group construction for ramified p=2 in Q(i).

    Sage 10.7 note: base object uses K = NumberField(x^2+1, 'i') and Qp(2).
    """
    def __init__(self, K, p):
        self.K = K
        self.p = p
        self._prec = 20   # target: 2^{-20} in Qp(2)

    def gen(self):
        """Topological generator gamma of anticyclotomic Z_2-extension."""
        raise NotImplementedError(
            "TODO #1 [SPECIALIST]: Anticyclotomic topological generator via CM theory.\n"
            "  See de Shalit 1987 §1-2; Rubin Invent. Math. 103; BDP 2001 §2."
        )

    def character(self, m):
        """
        Return the m-th anticyclotomic character chi_m: Gamma -> Z_2^*.
        Satisfies chi_m(gamma) = <N(gamma)>^m in Iwasawa language.
        """
        raise NotImplementedError(
            "TODO #1 [SPECIALIST]: chi_m as continuous character of Z_2-extension."
        )

Gamma = AnticyclotomicGaloisScaffold(K, 2)
print("[SCAFFOLD] AnticyclotomicGaloisScaffold initialized (TODO #1, specialist needed).")

# ---------------------------------------------------------------------------
# 3.  HECKE GROSSENCHARACTER psi  (SKELETON — TODO #2)
# ---------------------------------------------------------------------------
# psi: A_K^* -> C^* a Hecke Grossencharacter of K = Q(i) with:
#   conductor  = (1+i)^2   (ideal (2) in O_K, norm 4)
#   infinity-type (4, 0): psi_infty(z) = z^4 for z in K tensor_Q R = C
#   Galois rep: rho_f = Ind_{G_K}^{G_Q} psi_min (dihedral representation)
#
# SAGE 10.7 STATUS: PARTIAL.
#   - HeckeCharGroup(K): exists in Sage 10.7 (sage.rings.number_field)
#     but support for infinity-type specifications is THIN as of May 2026.
#   - Option A (recommended): use f.character() + eigenvalue Hecke check
#     to verify psi(p) = a_p(f) for primes p split in K.
#   - Option B: construct psi explicitly via HeckeCharGroup if it supports
#     infinity types for imaginary quadratic fields
#   - Option C: use LFunctions module to cross-check L(psi, s) = L(f, s)
#
# TODO #2 [SAGE-DOABLE, ~3 h]:
#   Status: SAGE-DOABLE (graduate-level number theory, no specialist needed)
#   Implement psi via eigenvalue check:
#     for p split in K (p = 1 mod 4, p != 2):
#       psi(p) = a_p(f)   (up to choice of prime above p in O_K)
#   This is sufficient for the BDP construction input.
#   Full Grossencharacter object: use HeckeCharGroup or verify against LMFDB.

print("[SCAFFOLD] Hecke Grossencharacter psi: implicit via L(f,s) (TODO #2, ~3 h).")
print("           Sage 10.7: HeckeCharGroup partial support; eigenvalue check feasible.")

# ---------------------------------------------------------------------------
# 4.  BERTOLINI-DARMON-PRASANNA 2-ADIC DISTRIBUTION  (TODO #3, CORE)
# ---------------------------------------------------------------------------
# L_2^+/-(f) live in the Iwasawa algebra Lambda = Z_2[[Gamma]] and interpolate:
#   integral_{Gamma} chi_m dL_2^+(f) = (interpolation formula at chi_m)
#
# Supersingularity note: a_2(f) = -4, v_2(-4) = 2 >= 1 => f is SUPERSINGULAR at 2.
# Plus, 2 is RAMIFIED in K = Q(i) (the BDP 2013 Theorem 3.10 requires
# p unramified and p > k-1; both fail here).
# The distribution is defined in the Kriz 2021 regime (arXiv:1912.02308).
#
# SAGE 10.7 STATUS: NOT IN STDLIB.
#   - Pollack-Stevens overconvergent modular symbols (Sage addon 2011-2014):
#     partially available via sage.modular.pollack_stevens
#     (check sage.modular.pollack_stevens.space.PollackStevensModularSymbols)
#   - Kobayashi ± subgroups: NOT natively available
#   - BDP Heegner-point measure: NOT available; specialist Magma code exists
#
# TODO #3 [SPECIALIST, ~20-30 h, Buyukboduk or Lei]:
#   Status: SPECIALIST NEEDED (hardest piece)
#   (a) Implement BDP Heegner-point measure mu_{psi} on Gamma at p=2
#   (b) Decompose into mu^+/- using Kobayashi +/- subgroups
#   (c) Integrate chi_m against mu^+/- to 2-adic precision 2^{-20}
#   Outreach: Kazim Buyukboduk (UCD Dublin), Antonio Lei (Ottawa)
#   Reference: Buyukboduk-Lei arXiv:1709.02912; Kriz arXiv:1912.02308

def bertolini_darmon_2adic_plus(f, K, psi, Gamma, prec=20):
    """
    TODO #3 [SPECIALIST, ~20-30 h]: L_2^+(f) in Z_2[[Gamma]] to 2^{-prec}.

    SAGE 10.7 STATUS: NOT IN STDLIB.
    Requires BDP/Kriz construction for p=2 ramified supersingular case.
    Outreach: Buyukboduk (kazim.buyukboduk@ucd.ie), Lei (antonio.lei@uottawa.ca)
    """
    raise NotImplementedError(
        "TODO #3 [SPECIALIST]: BDP Heegner distribution L_2^+(f).\n"
        "  Estimated effort: 20-30 h specialist (Buyukboduk / Lei).\n"
        "  See BDP 2013 arXiv:1002.4071 §3 + Kriz arXiv:1912.02308."
    )

def bertolini_darmon_2adic_minus(f, K, psi, Gamma, prec=20):
    """
    TODO #3 [SPECIALIST, ~20-30 h]: L_2^-(f) in Z_2[[Gamma]] to 2^{-prec}.
    Same interface as bertolini_darmon_2adic_plus, minus-branch.
    """
    raise NotImplementedError("TODO #3 [SPECIALIST]: See bertolini_darmon_2adic_plus.")

def integrate_against_character(L_2_branch, chi):
    """
    TODO #3 (sub) [SPECIALIST]: Evaluate integral_{Gamma} chi dL_2_branch.
    Returns element of Qp(2) to current precision of L_2_branch.
    """
    raise NotImplementedError(
        "TODO #3 (sub) [SPECIALIST]: Iwasawa pairing integral."
    )

# ---------------------------------------------------------------------------
# 5.  F1 TEST LOOP  (orchestration — runnable once TODOs #1-3 are filled)
# ---------------------------------------------------------------------------

p_adic_field = Qp(2, prec=25)   # 2-adic field to precision 2^{-25}

def run_f1_falsifier(dry_run=True):
    """
    Execute the F1 falsifier protocol.

    Parameters
    ----------
    dry_run : bool
        If True, print scaffold status and skip TODO raises.
        If False, attempt all subroutines (raises until TODO #1-#3 implemented).

    Returns
    -------
    dict  keys = 1,2,3,4  values = dict with keys
            'integral_plus', 'integral_minus',
            'predicted_plus', 'predicted_minus',
            'discrepancy_plus_v2', 'discrepancy_minus_v2'
    str   'PASS' / 'FAIL' / 'NOT_RUN'
    """
    if dry_run:
        print("\n[DRY RUN] F1 falsifier v2 scaffold summary:")
        print("  Predicted values (M13.1(a) FE-symmetric means):")
        for m in [1, 2, 3, 4]:
            print(f"    m={m}: predicted_plus = {predicted_plus[m]},  "
                  f"predicted_minus = {predicted_minus[m]}")
        print("\n  Sage 10.7 TODO status:")
        print("  TODO #1: AnticyclotomicGalois (~5 h, SPECIALIST)")
        print("  TODO #2: Hecke Grossencharacter psi explicit (~3 h, SAGE-DOABLE)")
        print("  TODO #3: BDP Heegner distribution L_2^+/- (~20-30 h, SPECIALIST)")
        print("\n  PASS CRITERION: v_2(integral - predicted) >= 20 for all m")
        print("  FAIL CRITERION: v_2 < 20 for any m  --> M13.1(a) FALSIFIED")
        return {}, "NOT_RUN"

    # --- Live run (requires TODO #1-3 implemented) ---
    try:
        L_plus  = bertolini_darmon_2adic_plus(f, K, None, Gamma, prec=25)
        L_minus = bertolini_darmon_2adic_minus(f, K, None, Gamma, prec=25)
    except NotImplementedError as e:
        print(f"[ABORT] {e}")
        return {}, "NOT_RUN"

    results = {}
    for m in [1, 2, 3, 4]:
        try:
            chi_m = Gamma.character(m)
        except NotImplementedError as e:
            print(f"[ABORT] chi_{m}: {e}")
            return results, "NOT_RUN"

        int_plus  = integrate_against_character(L_plus,  chi_m)
        int_minus = integrate_against_character(L_minus, chi_m)

        pred_p = p_adic_field(predicted_plus[m])
        pred_m = p_adic_field(predicted_minus[m])

        disc_plus_v2  = (int_plus  - pred_p).valuation()
        disc_minus_v2 = (int_minus - pred_m).valuation()

        results[m] = {
            "integral_plus":        int_plus,
            "integral_minus":       int_minus,
            "predicted_plus":       pred_p,
            "predicted_minus":      pred_m,
            "discrepancy_plus_v2":  disc_plus_v2,
            "discrepancy_minus_v2": disc_minus_v2,
        }
        print(f"  m={m}: disc_plus v_2 = {disc_plus_v2},  "
              f"disc_minus v_2 = {disc_minus_v2}")

    threshold = 20
    pass_plus  = all(results[m]["discrepancy_plus_v2"]  >= threshold
                     for m in [1, 2, 3, 4])
    pass_minus = all(results[m]["discrepancy_minus_v2"] >= threshold
                     for m in [1, 2, 3, 4])
    verdict = "PASS" if (pass_plus and pass_minus) else "FAIL"
    return results, verdict


# ---------------------------------------------------------------------------
# 6.  MAIN ENTRY POINT
# ---------------------------------------------------------------------------

results, verdict = run_f1_falsifier(dry_run=True)

print("\n" + "=" * 70)
print(f"F1 EXECUTED: {verdict}")
print("Conjecture M13.1(a): NOT_TESTED (skeleton only, Stage 2 specialist-blocked)")
print("=" * 70)

print("""
SUBROUTINE SUMMARY (Sage 10.7 status per TODO):

  TODO #1  AnticyclotomicGalois(K=Q(i), p=2)
           Status: SPECIALIST NEEDED (~5 h).
           Sage 10.7: NOT IN STDLIB for ramified p=2 CM case.
           References: de Shalit 1987; Rubin Invent. Math. 103; BDP 2001 §2.

  TODO #2  Hecke Grossencharacter psi (conductor (1+i)^2, type (4,0))
           Status: SAGE-DOABLE (~3 h).
           Sage 10.7: HeckeCharGroup partial support; eigenvalue check feasible.
           Can verify psi(p) = a_p(f) for split primes via LMFDB 4.5.b.a.

  TODO #3  BDP Heegner 2-adic distribution L_2^+/-(f)
           Status: SPECIALIST NEEDED (~20-30 h). CORE SUBROUTINE.
           Sage 10.7: NOT IN STDLIB. Requires BDP/Kriz p=2 ramified adaptation.
           pollack_stevens module partial; Kobayashi +/- NOT available.
           Outreach: Buyukboduk (kazim.buyukboduk@ucd.ie)
                     Lei (antonio.lei@uottawa.ca)
           Key references:
             - BDP 2013 arXiv:1002.4071 §3
             - Kriz 2021 arXiv:1912.02308 (supersingular p-adic L-functions)
             - Buyukboduk-Lei arXiv:1709.02912 (anticyclotomic p-adic L-functions)

  TOTAL specialist effort: ~25-35 h (TODOs #1, #3)
  TOTAL Sage-doable effort: ~3 h (TODO #2)
  Compute cost once implemented: ~50 CPU-hr (matches M44 F1 estimate)

OBSTRUCTION NOTE (M44 F5 outcome):
  p=2 RAMIFIED in K=Q(i) AND SUPERSINGULAR for f (v_2(a_2)=2 >= 1).
  Existing IMC theorems (Hsieh 2014, Chida-Hsieh 2015, Arnold 2007,
  Pollack-Weston 2011) ALL require at least one of:
    - p unramified in K, OR
    - p > k+1, OR
    - p ordinary.
  None hold here. The BDP distribution exists in principle (Kriz 2021 regime),
  but the Iwasawa main conjecture controlling interpolation is OPEN.
  F1 falsifier tests the interpolation DIRECTLY and is independent of IMC.
""")
