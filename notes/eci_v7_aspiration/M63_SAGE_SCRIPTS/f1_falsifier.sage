##############################################################################
# f1_falsifier.sage
# F1 Falsifier — Conjecture M13.1(a) FE-symmetric 2-adic interpolation
#
# PROTOCOL (M44 falsifiers.md, F1):
#   Test whether the Bertolini-Darmon Heegner 2-adic distribution L_2^± for
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
#   Estimated effort: 30-60 h specialist (Buyukboduk / Lei) for BDP machinery.
#
# SAGE VERSION: tested syntax targets SageMath >= 10.0
# DEPENDENCIES NOT IN SAGE STDLIB:
#   (1)  BDP = Bertolini-Darmon-Prasanna 2-adic Heegner distribution code
#        (no canonical Sage package as of May 2026; closest: Magma BDP routines)
#   (2)  AnticyclotomicGalois — custom class (scaffold below)
#   (3)  anticyclotomic_character — evaluates chi_m on Gamma
#   (4)  bertolini_darmon_2adic — builds L_2^± as p-adic Iwasawa function
#
# FALSIFYING OUTCOME (M44 F1):
#   If for any m in {1,2,3,4}:
#       v_2( integral_+ - predicted[m] ) < 20
#   then Conjecture M13.1(a) FE-symmetric interpolation is FALSIFIED.
#
# PASSING OUTCOME:
#   All four discrepancies have 2-adic valuation >= 20 — M13.1(a) supported.
#
# REFERENCES:
#   - Bertolini-Darmon "Heegner points on Mumford-Tate curves", JAMS 2001
#   - Bertolini-Darmon-Prasanna "Generalized Heegner cycles", Duke Math. J. 2013
#     (arXiv:1002.4071)
#   - M44 falsifiers.md, section F1 (50 CPU-hr estimate)
#   - M52 SUMMARY.md, Damerell table (PARI 80-digit verified)
#   - M13 / M32_M131_FORMAL for M13.1(a) statement
##############################################################################

from sage.all import (
    NumberField, QQ, ZZ, PolynomialRing,
    Newforms, DirichletGroup,
    Qp,  # 2-adic field
)

print("=" * 70)
print("F1 FALSIFIER — Conjecture M13.1(a) FE-symmetric 2-adic interpolation")
print("Status: SKELETON. Fill TODO subroutines before running.")
print("=" * 70)

# ---------------------------------------------------------------------------
# 0.  BASE FIELD AND CM NEWFORM
# ---------------------------------------------------------------------------

R = PolynomialRing(QQ, 'x')
x = R.gen()

K = NumberField(x**2 + 1, 'i')
i_K = K.gen()  # sqrt(-1)

# Fundamental discriminant d_K = -4; class number h_K = 1
# Conductor of the Hecke Grossencharacter: (1+i)^2 in O_K = Z[i]
# Infinity-type: z^4 (weight k=5, so (k-1, 0) = (4, 0))
conductor_elem = (1 + i_K)**2   # = 2i in Z[i], norm = 4

# Reference newform: LMFDB label 4.5.b.a
#   Level N = 4, weight k = 5, character chi_{-4} (Dirichlet char mod 4)
#   Hecke eigenvalue a_2 = -4 (Steinberg edge: a_p = -p^{(k-1)/2} = -4)
#   CM by K = Q(i)

chi_group = DirichletGroup(4, QQ)
# chi_group[1] should be the non-trivial character mod 4 (Kronecker symbol)
chi_neg4 = chi_group[1]

S_forms = Newforms(4, 5, character=chi_neg4, names='a')
assert len(S_forms) >= 1, "Expected at least one newform at level 4 weight 5 chi_{-4}"
f = S_forms[0]

# Sanity: Steinberg edge anchor
a2 = f.q_expansion(3)[2]   # coefficient of q^2
expected_a2 = -4            # = -2^{(5-1)/2} = -2^2
assert a2 == expected_a2, (
    f"Steinberg edge CHECK FAILED: a_2 = {a2}, expected {expected_a2}"
)
print(f"[OK] f = 4.5.b.a confirmed: a_2 = {a2}")

# ---------------------------------------------------------------------------
# 1.  DAMERELL CRITICAL VALUES  (M52 F2 v6, PARI 80-digit verified)
# ---------------------------------------------------------------------------
# alpha_m = L(f, m) / Omega_f^{2m-1}  (normalized Damerell values)
# For f = 4.5.b.a, alpha_m in {1/10, 1/12, 1/24, 1/60} (all in Q).
# These are the F1-renormalised ladders per M22 / falsifiers.md F2.

alpha_m = {
    1: QQ(1, 10),   # = 1/10
    2: QQ(1, 12),   # = 1/12
    3: QQ(1, 24),   # = 1/24
    4: QQ(1, 60),   # = 1/60
}
print(f"[OK] Damerell ladder loaded: alpha = {alpha_m}")

# F1 Conjecture M13.1(a) prediction: FE-symmetric mean
# k = 5, so k - m runs through {4, 3, 2, 1} as m runs through {1, 2, 3, 4}
predicted_plus = {}
predicted_minus = {}
for m in [1, 2, 3, 4]:
    # L_2^+ interpolates the FE-symmetric combination (alpha_m + alpha_{k-m})/2
    predicted_plus[m]  = (alpha_m[m] + alpha_m[5 - m]) / 2
    # L_2^- interpolates the FE-antisymmetric combination (alpha_m - alpha_{k-m})/2
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
#   - p = 2 is RAMIFIED in K/Q (since d_K = -4 = -4 = -(2)^2)
#   - The anticyclotomic Z_2-tower is a Z_2-extension of K where complex
#     conjugation acts as inversion on Gamma.
#   - Topological generator gamma_gen acts on characters via m-th power.
#
# CAUTION (from M44 F5 falsifier — EXECUTED, FALSIFIED):
#   Standard IMC theorems (Hsieh 2014, Chida-Hsieh 2015, Arnold 2007,
#   Pollack-Weston 2011) ALL exclude p=2 ramified in K or p supersingular
#   with k odd. This means the BDP distribution L_2^± EXISTS as a formal
#   construction but its Iwasawa-theoretic properties are NOT guaranteed by
#   existing theorems. The falsifier tests the interpolation property directly.
#
# TODO #1 [SPECIALIST, ~5 h]:
#   Implement AnticyclotomicGalois(K, 2) returning:
#     .gen()  -- topological generator gamma with gamma^{2^n} = id on K_n
#     .char_at_n(m, n)  -- the m-th character at level-n approximation
#
# Scaffold (placeholder class):

class AnticyclotomicGaloisScaffold:
    """
    Placeholder for Gal(K_infty^{anti} / K), K = Q(i), p = 2.

    TODO #1: Implement using CM theory and the explicit Lubin-Tate / formal
    group construction for ramified p=2 in Q(i). See:
      - de Shalit "Iwasawa Theory of Elliptic Curves with CM" (Academic Press 1987)
      - Rubin "The 'main conjectures' of Iwasawa theory..." (Invent. Math. 103)
      - Bertolini-Darmon 2001 §2
    """
    def __init__(self, K, p):
        self.K = K
        self.p = p
        self._prec = 20   # target: 2^{-20} in Qp(2)

    def gen(self):
        # Returns formal topological generator gamma as a symbol.
        # Real implementation: element of Z_2^* acting on K_infty^{anti}.
        raise NotImplementedError(
            "TODO #1: Implement anticyclotomic topological generator via CM theory."
        )

    def character(self, m):
        """
        Return the m-th anticyclotomic character chi_m: Gamma -> Z_2^*.
        Satisfies chi_m(gamma) = <N(gamma)>^m in Iwasawa language.
        """
        raise NotImplementedError(
            "TODO #1: Implement chi_m as continuous character of Z_2-extension."
        )

Gamma = AnticyclotomicGaloisScaffold(K, 2)
print("[SCAFFOLD] AnticyclotomicGaloisScaffold initialized (TODO #1 not implemented).")

# ---------------------------------------------------------------------------
# 3.  HECKE GROSSENCHARACTER psi  (SKELETON — TODO #2)
# ---------------------------------------------------------------------------
# psi: A_K^* -> C^* a Hecke Grossencharacter of K = Q(i) with:
#   conductor  = (1+i)^2   (equiv. to ideal (2) in O_K, since (1+i)^2 = 2i)
#   infinity-type (4, 0): psi_infty(z) = z^4 for z in K tensor_Q R = C
#   Galois rep: rho_f = Ind_{G_K}^{G_Q} psi_min (dihedral representation)
#
# In SageMath, HeckeCharacters live in HeckeCharGroup or CRT-based group.
# As of Sage 10.x, there is limited native support for Grossencharacters
# on imaginary quadratic fields. Magma has more mature routines.
#
# TODO #2 [~3 h, can use existing sage.modular.hecke_grossencharacter if available,
#           or construct psi via lattice-sum / modular-form CM theory]:
#
#   Option A: sage.rings.number_field.HeckeCharGroup — check if available
#   Option B: Compute psi(p) = a_p(f) for p split in K; verify psi(sigma) = a_p(f)
#             using PARI lfuncheckfeq or explicit Hecke eigenvalue check
#   Option C: Use echelon form of Hecke algebra at level 4 (already done via f above)

# Minimal scaffold: psi encoded via its L-series (= L(f, s)):
# For the falsifier, psi appears implicitly through f's L-function.
# The BDP distribution is constructed from Heegner points attached to psi.

print("[SCAFFOLD] Hecke Grossencharacter psi encoded implicitly via L(f,s).")
print("           TODO #2: explicit psi for BDP Heegner input.")

# ---------------------------------------------------------------------------
# 4.  BERTOLINI-DARMON-PRASANNA 2-ADIC DISTRIBUTION  (TODO #3, CORE)
# ---------------------------------------------------------------------------
# L_2^+(f) and L_2^-(f) are the plus/minus Bertolini-Darmon-Prasanna (BDP)
# 2-adic L-functions attached to f and K.
#
# They live in the Iwasawa algebra Lambda = Z_2[[Gamma]] and interpolate:
#   integral_{Gamma} chi_m dL_2^+(f) = (interpolation formula at chi_m)
#
# For supersingular p=2 (since a_2(f) = -4, |a_2| = 4 = 2^2, so 2 | a_2 —
# actually a_2 = -4 means f is at the Steinberg EDGE, not strictly supersingular;
# the condition is v_2(a_2) >= 1, which gives v_2(-4) = 2 >= 1: SUPERSINGULAR),
# the standard BDP theory must be adapted using the ±-formalism of
# Kobayashi (2003) and Pollack (2003).
#
# KEY OBSTRUCTION (from M44 F5): Existing IMC theorems exclude p=2 ramified.
# However, BDP 2013 (arXiv:1002.4071) Theorem 3.10 constructs L_p^{BDP}
# under: p unramified in K, p > k-1. BOTH fail here (p=2 ramified, p<k-1=4).
# The distribution may still be defined via a direct Heegner-point construction;
# this is the Kriz 2021 regime (p-adic L-functions in the supersingular case).
#
# TODO #3 [SPECIALIST, ~20-30 h, Buyukboduk or Lei]:
#   (a) Implement BDP Heegner-point measure mu_{psi} on Gamma at p=2
#   (b) Decompose into mu^+ + mu^- using Kobayashi ± subgroups
#   (c) Integrate chi_m against mu^± to 2-adic precision 2^{-20}
#
# Relevant code references:
#   - Pollack-Stevens (overconvergent modular symbols, Sage addon 2011-2014)
#   - Bellaiche-Dasgupta p-adic L-functions (GitHub, 2020s)
#   - Kriz "Supersingular p-adic L-functions..." arXiv:1912.02308
#   - Buyukboduk-Lei "Anticyclotomic p-adic L-functions" arXiv:1709.02912

def bertolini_darmon_2adic_plus(f, K, psi, Gamma, prec=20):
    """
    TODO #3: Return L_2^+(f) as an element of Z_2[[Gamma]] to precision 2^{-prec}.

    Expected interface:
      - f: SageMath Newform object
      - K: NumberField Q(i)
      - psi: Hecke Grossencharacter (TODO #2)
      - Gamma: AnticyclotomicGaloisScaffold (TODO #1)
      - prec: 2-adic precision

    Returns: callable chi -> Qp(2)(chi integral against L_2^+)
    """
    raise NotImplementedError(
        "TODO #3: Implement BDP Heegner distribution.\n"
        "  Estimated effort: 20-30 h specialist (Buyukboduk / Lei)\n"
        "  See BDP 2013 arXiv:1002.4071 §3 + Kriz arXiv:1912.02308"
    )

def bertolini_darmon_2adic_minus(f, K, psi, Gamma, prec=20):
    """
    TODO #3: Return L_2^-(f) as an element of Z_2[[Gamma]] to precision 2^{-prec}.
    Same interface as above, minus-branch.
    """
    raise NotImplementedError("TODO #3: See bertolini_darmon_2adic_plus above.")

def integrate_against_character(L_2_branch, chi):
    """
    TODO #3 (sub): Evaluate integral_{Gamma} chi dL_2_branch.
    Returns element of Qp(2) to current precision of L_2_branch.
    """
    raise NotImplementedError(
        "TODO #3 (sub): Iwasawa pairing integral."
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
        If False, attempt to call all subroutines (will raise NotImplementedError
        until TODO #1-#3 are implemented).

    Returns
    -------
    dict  keys = 1,2,3,4  values = dict with keys
            'integral_plus', 'integral_minus',
            'predicted_plus', 'predicted_minus',
            'discrepancy_plus_v2', 'discrepancy_minus_v2'
    str   'PASS' / 'FAIL' / 'NOT_RUN'
    """
    if dry_run:
        print("\n[DRY RUN] F1 falsifier scaffold summary:")
        print("  Predicted values (M13.1(a) FE-symmetric means):")
        for m in [1, 2, 3, 4]:
            print(f"    m={m}: predicted_plus = {predicted_plus[m]},  "
                  f"predicted_minus = {predicted_minus[m]}")
        print("\n  TODO #1: AnticyclotomicGalois (5 h specialist)")
        print("  TODO #2: Hecke Grossencharacter psi explicit (3 h)")
        print("  TODO #3: BDP Heegner distribution L_2^± (20-30 h specialist)")
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
            "integral_plus":      int_plus,
            "integral_minus":     int_minus,
            "predicted_plus":     pred_p,
            "predicted_minus":    pred_m,
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
    all_pass = pass_plus and pass_minus

    verdict = "PASS" if all_pass else "FAIL"
    return results, verdict


# ---------------------------------------------------------------------------
# 6.  MAIN ENTRY POINT
# ---------------------------------------------------------------------------

results, verdict = run_f1_falsifier(dry_run=True)

print("\n" + "=" * 70)
print(f"F1 EXECUTED: {verdict}")
print("Conjecture M13.1(a): NOT_TESTED (skeleton only)")
print("=" * 70)

print("""
SUBROUTINE SUMMARY (what must be implemented before a live run):
  TODO #1  AnticyclotomicGalois(K=Q(i), p=2)
           - CM theory, de Shalit / Rubin, Bertolini-Darmon 2001 §2
           - Estimated effort: ~5 h (specialist Iwasawa theorist)

  TODO #2  Hecke Grossencharacter psi (conductor (1+i)^2, type (4,0))
           - Can be verified against LMFDB 4.5.b.a Galois rep
           - Estimated effort: ~3 h (graduate-level number theory)

  TODO #3  BDP Heegner 2-adic distribution L_2^±(f)
           - Core subroutine; hardest piece
           - Requires BDP 2013 arXiv:1002.4071 §3 + Kriz 2021 arXiv:1912.02308
             for the p=2 supersingular / ramified adaptation
           - No canonical Sage package; Magma code may exist (contact
             Buyukboduk or Lei for copy / collaboration)
           - Estimated effort: 20-30 h specialist

  TOTAL estimated specialist effort: ~30-40 h
  Compute cost once implemented: ~50 CPU-hr (matches M44 F1 estimate)

OBSTRUCTION NOTE (M44 F5 outcome):
  p=2 is RAMIFIED in K=Q(i) and SUPERSINGULAR for f (v_2(a_2)=2 >= 1).
  Existing IMC theorems (Hsieh 2014, Chida-Hsieh 2015, Arnold 2007,
  Pollack-Weston 2011) ALL require at least one of:
    - p unramified in K, OR
    - p > k+1, OR
    - p ordinary
  None hold here. The BDP DISTRIBUTION exists in principle (Kriz regime),
  but the Iwasawa main conjecture controlling its interpolation is [TBD].
  F1 falsifier tests the interpolation DIRECTLY and is independent of IMC.
""")
